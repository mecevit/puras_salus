"""promo.render_video — render a self-contained GSAP HTML animation to MP4
inside the Puras worker, and store it in the workspace drive.

Runtime facts (probed): playwright is importable; the chromium browser is NOT
pre-installed but `playwright install chromium` works (egress is open); a static
ffmpeg comes from the `imageio-ffmpeg` pip package; the job cwd has a `drive/`
symlink to the workspace drive, so writing `drive/<path>` persists the file.

The HTML must expose:  window.__DURATION__ (sec),  window.__seek(t),  and
optional window.__BLUR_SEGMENTS__ = [[a,b],…]  (fast windows for targeted motion
blur). It may load GSAP from `vendor/gsap.min.js` — we drop a copy next to it.
"""
from __future__ import annotations

import os
import sys
import shutil
import tempfile
import subprocess
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1920, 1080


def _ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _ensure_chromium() -> None:
    """Launch once; if the browser binary is missing, install it (cached per worker)."""
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            b.close()
        return
    except Exception:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True, timeout=600,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )


def run(html: str, fps: int = 30, mblur: int = 8, max_seconds: float = 45.0) -> dict:
    from playwright.sync_api import sync_playwright

    if not html or "__seek" not in html:
        raise ValueError("html must be a self-contained page exposing window.__seek / window.__DURATION__")

    fps = max(8, min(int(fps or 30), 60))
    mblur = max(1, min(int(mblur or 8), 16))
    ff = _ffmpeg()
    _ensure_chromium()

    work = Path(tempfile.mkdtemp(prefix="promo_"))
    (work / "vendor").mkdir(parents=True, exist_ok=True)
    gsap = HERE / "vendor" / "gsap.min.js"
    if gsap.is_file():
        shutil.copy(gsap, work / "vendor" / "gsap.min.js")
    (work / "index.html").write_text(html, encoding="utf-8")
    fdir = work / "final"; fdir.mkdir()
    sdir = work / "sub"; sdir.mkdir()

    with sync_playwright() as pw:
        b = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--force-color-profile=srgb", "--disable-lcd-text"],
        )
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto((work / "index.html").as_uri() + "?render=1", wait_until="networkidle")

        dur = pg.evaluate("() => window.__DURATION__")
        if not dur:
            b.close(); raise ValueError("window.__DURATION__ is missing/0 — the HTML did not initialise")
        dur = min(float(dur), float(max_seconds))
        segs = pg.evaluate("() => window.__BLUR_SEGMENTS__ || []") or []

        def is_fast(t: float) -> bool:
            return any(float(a) <= t < float(bb) for a, bb in segs)

        def grab(t: float, path: Path) -> None:
            pg.evaluate("(tt) => window.__seek(tt)", t)
            pg.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            pg.screenshot(path=str(path), type="jpeg", quality=95, clip={"x": 0, "y": 0, "width": W, "height": H})

        n_frames = int(round(dur * fps))
        for n in range(n_frames):
            t = n / fps
            out = fdir / f"{n:05d}.jpg"
            if mblur <= 1 or not is_fast(t):
                grab(t, out)
            else:  # average mblur sub-samples → real (directional) motion blur, only in fast windows
                ins = []
                for k in range(mblur):
                    sf = sdir / f"s{k:02d}.jpg"
                    grab(t + (k / mblur) / fps, sf)
                    ins += ["-i", str(sf)]
                subprocess.run(
                    [ff, "-y", *ins, "-filter_complex", f"mix=inputs={mblur}", "-frames:v", "1", str(out)],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
        b.close()

    out_mp4 = work / "out.mp4"
    subprocess.run(
        [ff, "-y", "-framerate", str(fps), "-i", str(fdir / "%05d.jpg"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
         "-movflags", "+faststart", str(out_mp4)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # persist into the workspace drive (cwd has a `drive/` symlink → workspace drive)
    rel = f"promo/{uuid.uuid4().hex[:12]}.mp4"
    dest = Path("drive") / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_mp4, dest)

    video_url = None
    try:
        from puras import drive
        video_url = drive.url(rel, ttl=30 * 24 * 3600)
    except Exception:
        video_url = None

    size = os.path.getsize(out_mp4)
    shutil.rmtree(work, ignore_errors=True)
    return {
        "drive_path": rel,
        "video_url": video_url,
        "duration_sec": round(dur, 2),
        "frames": n_frames,
        "fps": fps,
        "bytes": size,
    }
