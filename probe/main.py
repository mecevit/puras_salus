import sys, os, platform, subprocess, json


def run(**inputs):
    rep = {"python": sys.version.split()[0], "platform": platform.platform(), "cwd": os.getcwd()}
    rep["drive_exists"] = os.path.exists("drive")
    rep["drive_islink"] = os.path.islink("drive") if os.path.lexists("drive") else False

    # ffmpeg from pip (static binary, no system install)
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        line = subprocess.run([exe, "-version"], capture_output=True, text=True, timeout=20).stdout.splitlines()[0]
        rep["imageio_ffmpeg"] = line
    except Exception as e:
        rep["imageio_ffmpeg"] = f"no: {type(e).__name__}: {str(e)[:200]}"

    # chromium launch via playwright (install at runtime if needed)
    def try_launch():
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            pg = b.new_page(viewport={"width": 320, "height": 200})
            pg.set_content("<h1 style='font-family:serif'>ok</h1>")
            n = len(pg.screenshot())
            b.close()
            return n
    try:
        rep["chromium_launch"] = f"OK ({try_launch()} bytes)"
    except Exception as e:
        rep["chromium_launch_1"] = f"{type(e).__name__}: {str(e)[:200]}"
        try:
            inst = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"],
                                  capture_output=True, text=True, timeout=240)
            rep["playwright_install_rc"] = inst.returncode
            rep["playwright_install_tail"] = (inst.stdout + inst.stderr)[-300:]
            rep["chromium_launch"] = f"OK after install ({try_launch()} bytes)"
        except Exception as e2:
            rep["chromium_launch"] = f"no: {type(e2).__name__}: {str(e2)[:250]}"

    return {"report": json.dumps(rep, ensure_ascii=False, indent=2)}
