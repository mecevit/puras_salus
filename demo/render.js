import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/* ----- config via env -----
   PREVIEW=1   → FAST iteration: 1280x720 (720p) jpeg capture, single rAF, veryfast.
   (default)   → FULL delivery:  1920x1080 png, 2x supersample, crf17 slow.
   Speed knobs: FPS, SS (deviceScaleFactor), FMT (jpeg|png), JQ (jpeg quality),
                MAXT (cap render to N seconds — quick look), MBLUR (frame-blend). */
const PREVIEW = process.env.PREVIEW === '1';
const FPS    = Number(process.env.FPS || (PREVIEW ? 30 : 30));
const MBLUR  = Number(process.env.MBLUR || 1);                  // frame-blend (1=off; motion blur is in-engine)
const SS     = Number(process.env.SS || (PREVIEW ? 2/3 : 2));   // deviceScaleFactor (2/3 → 720p capture)
const FMT    = (process.env.FMT || (PREVIEW ? 'jpeg' : 'png')).toLowerCase();
const JQ     = Number(process.env.JQ || 80);
const OUT_W  = Number(process.env.OUT_W || (PREVIEW ? 1280 : 1920));
const OUT_H  = Number(process.env.OUT_H || (PREVIEW ? 720 : 1080));
const CRF    = String(process.env.CRF || (PREVIEW ? 26 : 17));
const PRESET = String(process.env.PRESET || (PREVIEW ? 'veryfast' : 'slow'));
const OUT    = process.env.OUT || (PREVIEW ? 'salus-demo-preview.mp4' : 'salus-demo.mp4');
const MAXT   = Number(process.env.MAXT || 0);                   // cap seconds (0 = full)
const FROMT  = Number(process.env.FROMT || 0);                  // render only the window [FROMT, TOT]
const TOT    = Number(process.env.TOT || 0);
// parallel rendering: CAPTURE=1 worker (no rm/no encode), ENCODE=1 encode-only; WN workers, WI index
const CAPTURE = process.env.CAPTURE === '1';
const ENCODE  = process.env.ENCODE === '1';
const WN = Number(process.env.WN || 1);
const WI = Number(process.env.WI || 0);

const RFPS = FPS * MBLUR;
const W = 1920, H = 1080;
const ext = FMT === 'jpeg' ? 'jpg' : 'png';
const framesDir = path.join(__dirname, 'frames');
const outFile = path.join(__dirname, 'out', OUT);

// only the coordinator (plain mode) clears the frames dir; workers/encode share it
if (!CAPTURE && !ENCODE && existsSync(framesDir)) rmSync(framesDir, { recursive: true, force: true });
mkdirSync(framesDir, { recursive: true });
mkdirSync(path.join(__dirname, 'out'), { recursive: true });

const SRC = process.env.SRC || 'index.html';
const url = 'file://' + path.join(__dirname, SRC) + '?render=1';

// ---- CAPTURE phase (skipped in encode-only mode) ----
if (!ENCODE) {
  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SS });
  await page.goto(url, { waitUntil: 'networkidle' });

  let duration = await page.evaluate(() => window.__DURATION__);
  if (MAXT > 0) duration = Math.min(duration, MAXT);
  const startT = FROMT > 0 ? FROMT : 0;
  const endT = TOT > 0 ? Math.min(TOT, duration) : duration;
  const span = endT - startT;
  const totalFrames = Math.ceil(span * RFPS);
  const tag = CAPTURE ? `worker ${WI}/${WN}` : (PREVIEW ? 'PREVIEW' : 'FULL');
  console.log(`${tag} · t[${startT.toFixed(1)}–${endT.toFixed(1)}] ${span.toFixed(2)}s · mblur×${MBLUR} · ${totalFrames} frames · cap ${Math.round(W*SS)}x${Math.round(H*SS)} ${FMT}`);

  const shot = FMT === 'jpeg'
    ? { type: 'jpeg', quality: JQ, clip: { x: 0, y: 0, width: W, height: H } }
    : { type: 'png', clip: { x: 0, y: 0, width: W, height: H } };

  const t0 = Date.now();
  let done = 0;
  for (let f = 0; f < totalFrames; f++) {
    if (CAPTURE && (f % WN) !== WI) continue;            // this worker only owns its slice
    const t = startT + f / RFPS;
    await page.evaluate((tt) => window.__seek(tt), t);
    if (PREVIEW) await page.evaluate(() => new Promise(r => requestAnimationFrame(r)));
    else await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    await page.screenshot({ ...shot, path: path.join(framesDir, String(f).padStart(5, '0') + '.' + ext) });
    if (++done % 30 === 0) process.stdout.write(`\r  [${tag}] ${done} frames (${((Date.now()-t0)/1000).toFixed(0)}s)`);
  }
  process.stdout.write(`\r  [${tag}] ${done} frames (${((Date.now()-t0)/1000).toFixed(0)}s)\n`);
  await browser.close();
}

if (CAPTURE) process.exit(0);   // workers stop here; coordinator encodes separately

console.log('Encoding with ffmpeg…');
const vf = [
  MBLUR > 1 ? `tmix=frames=${MBLUR}` : null,
  MBLUR > 1 ? `fps=${FPS}` : null,
  `scale=${OUT_W}:${OUT_H}:flags=lanczos`,
].filter(Boolean).join(',');
const args = [
  '-y', '-framerate', String(RFPS),
  '-i', path.join(framesDir, '%05d.' + ext),
  '-vf', vf,
  '-r', String(FPS),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
  '-crf', CRF, '-preset', PRESET,
  '-movflags', '+faststart',
  outFile,
];
const r = spawnSync('ffmpeg', args, { stdio: 'inherit' });
if (r.status !== 0) { console.error('ffmpeg failed'); process.exit(1); }
console.log('Done →', outFile);
