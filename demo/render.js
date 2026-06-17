import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/* ----- config via env -----
   PREVIEW=1            → fast, small (960x540, SS=1, ultrafast). For iteration.
   (default / FULL)     → 1920x1080, SS=2 supersampled, crf17 slow. For delivery.
   Override anything:  FPS, SS, OUT_W, OUT_H, CRF, PRESET, OUT             */
const PREVIEW = process.env.PREVIEW === '1';
const FPS    = Number(process.env.FPS || 30);
const SS     = Number(process.env.SS || (PREVIEW ? 1 : 2));      // supersampling for crisp zoom
const OUT_W  = Number(process.env.OUT_W || (PREVIEW ? 960 : 1920));
const OUT_H  = Number(process.env.OUT_H || (PREVIEW ? 540 : 1080));
const CRF    = String(process.env.CRF || (PREVIEW ? 26 : 17));
const PRESET = String(process.env.PRESET || (PREVIEW ? 'veryfast' : 'slow'));
const OUT    = process.env.OUT || (PREVIEW ? 'salus-demo-preview.mp4' : 'salus-demo.mp4');

const W = 1920, H = 1080;                       // logical stage size (always 1080p layout)
const framesDir = path.join(__dirname, 'frames');
const outFile = path.join(__dirname, 'out', OUT);

if (existsSync(framesDir)) rmSync(framesDir, { recursive: true, force: true });
mkdirSync(framesDir, { recursive: true });
mkdirSync(path.join(__dirname, 'out'), { recursive: true });

const url = 'file://' + path.join(__dirname, 'index.html') + '?render=1';

const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SS });
await page.goto(url, { waitUntil: 'networkidle' });

const duration = await page.evaluate(() => window.__DURATION__);
const totalFrames = Math.ceil(duration * FPS);
console.log(`${PREVIEW ? 'PREVIEW' : 'FULL'} · ${duration.toFixed(2)}s · ${FPS}fps · ${totalFrames} frames · ${OUT_W}x${OUT_H} · SS${SS} → ${OUT}`);

for (let f = 0; f < totalFrames; f++) {
  const t = f / FPS;
  await page.evaluate((tt) => window.__seek(tt), t);
  // let layout/paint settle deterministically
  await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  const name = String(f).padStart(5, '0') + '.png';
  await page.screenshot({ path: path.join(framesDir, name), clip: { x: 0, y: 0, width: W, height: H } });
  if (f % 30 === 0) process.stdout.write(`\r  frame ${f}/${totalFrames}`);
}
process.stdout.write(`\r  frame ${totalFrames}/${totalFrames}\n`);
await browser.close();

console.log('Encoding with ffmpeg…');
const args = [
  '-y', '-framerate', String(FPS),
  '-i', path.join(framesDir, '%05d.png'),
  '-vf', `scale=${OUT_W}:${OUT_H}:flags=lanczos`,
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
  '-crf', CRF, '-preset', PRESET,
  '-movflags', '+faststart',
  outFile,
];
const r = spawnSync('ffmpeg', args, { stdio: 'inherit' });
if (r.status !== 0) { console.error('ffmpeg failed'); process.exit(1); }
console.log('Done →', outFile);
