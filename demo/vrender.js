// Targeted motion-blur renderer.
// Most of the timeline is rendered 1 sample/frame (fast). Only the windows the
// animation declares in window.__BLUR_SEGMENTS__ get M sub-samples averaged into
// the frame (real temporal motion blur — directional/radial). ~5x fewer frames
// than uniform MBLUR while keeping blur exactly where motion happens.
//
//   MBLUR=10 SS=1 node vrender.js          # full
//   MBLUR=10 WN=4 node vrender.js          # parallel (split output frames)
//   MBLUR=10 MAXT=12 node vrender.js       # quick look
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FPS   = Number(process.env.FPS || 30);
const M     = Number(process.env.MBLUR || 10);          // sub-samples inside fast windows
const SS    = Number(process.env.SS || 1);
const FMT   = (process.env.FMT || 'jpeg').toLowerCase();
const ext   = FMT === 'jpeg' ? 'jpg' : 'png';
const JQ    = Number(process.env.JQ || 97);
const CRF   = String(process.env.CRF || 17);
const PRESET= String(process.env.PRESET || 'slow');
const OUT   = process.env.OUT || 'salus-demo.mp4';
const SRC   = process.env.SRC || 'index.html';
const MAXT  = Number(process.env.MAXT || 0);
const WN    = Number(process.env.WN || 1);              // workers
const WI    = Number(process.env.WI || 0);              // this worker
const CAPTURE = process.env.CAPTURE === '1';
const ENCODE  = process.env.ENCODE === '1';

const W = 1920, H = 1080;
const finalDir = path.join(__dirname, 'final');
const subDir = path.join(__dirname, 'subtmp', String(WI));
const outFile = path.join(__dirname, 'out', OUT);

if (!CAPTURE && !ENCODE && existsSync(finalDir)) rmSync(finalDir, { recursive: true, force: true });
mkdirSync(finalDir, { recursive: true });
mkdirSync(path.join(__dirname, 'out'), { recursive: true });

const shot = FMT === 'jpeg'
  ? { type: 'jpeg', quality: JQ, clip: { x: 0, y: 0, width: W, height: H } }
  : { type: 'png', clip: { x: 0, y: 0, width: W, height: H } };

if (!ENCODE) {
  if (existsSync(subDir)) rmSync(subDir, { recursive: true, force: true });
  mkdirSync(subDir, { recursive: true });

  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SS });
  await page.goto('file://' + path.join(__dirname, SRC) + '?render=1', { waitUntil: 'networkidle' });

  let duration = await page.evaluate(() => window.__DURATION__);
  if (MAXT > 0) duration = Math.min(duration, MAXT);
  const segs = await page.evaluate(() => window.__BLUR_SEGMENTS__ || []);
  const isFast = (t) => segs.some(([a, b]) => t >= a && t < b);
  const N = Math.ceil(duration * FPS);
  const tag = CAPTURE ? `w${WI}/${WN}` : 'render';
  if (WI === 0) console.log(`${tag} · ${duration.toFixed(1)}s · ${N} frames · blur windows: ${segs.length} · M=${M}`);

  async function grab(t, file) {
    await page.evaluate((tt) => window.__seek(tt), t);
    await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    await page.screenshot({ ...shot, path: file });
  }

  const t0 = Date.now(); let done = 0;
  for (let n = 0; n < N; n++) {
    if (CAPTURE && (n % WN) !== WI) continue;
    const t = n / FPS;
    const finalFile = path.join(finalDir, String(n).padStart(5, '0') + '.' + ext);
    if (!isFast(t)) {
      await grab(t, finalFile);                       // single sample
    } else {
      const inArgs = [];                              // M sub-samples across the frame's shutter
      for (let k = 0; k < M; k++) {
        const sf = path.join(subDir, 's' + String(k).padStart(2, '0') + '.' + ext);
        await grab(t + (k / M) / FPS, sf);
        inArgs.push('-i', sf);
      }
      const r = spawnSync('ffmpeg', ['-y', ...inArgs, '-filter_complex', `mix=inputs=${M}`, '-frames:v', '1', finalFile], { stdio: 'ignore' });
      if (r.status !== 0) { console.error('mix failed @', n); process.exit(1); }
    }
    if (++done % 20 === 0 && WI === 0) process.stdout.write(`\r  ${tag} ${n}/${N} (${((Date.now()-t0)/1000).toFixed(0)}s)`);
  }
  if (WI === 0) process.stdout.write(`\r  ${tag} ${done} frames (${((Date.now()-t0)/1000).toFixed(0)}s)\n`);
  await browser.close();
}

if (CAPTURE) process.exit(0);

console.log('Encoding…');
const r = spawnSync('ffmpeg', [
  '-y', '-framerate', String(FPS), '-i', path.join(finalDir, '%05d.' + ext),
  '-vf', `scale=${W}:${H}:flags=lanczos`,
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', CRF, '-preset', PRESET,
  '-movflags', '+faststart', outFile,
], { stdio: 'inherit' });
if (r.status !== 0) { console.error('ffmpeg failed'); process.exit(1); }
console.log('Done →', outFile);
