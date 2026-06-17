# Salus / Puras — Motion Graphics Demo

HTML tabanlı, **deterministik** ürün tanıtım animasyonu → frame-perfect mp4.

Tek bir GSAP timeline her sahneyi saniyeye oturtur; Playwright (headless
Chromium) timeline'ı kare kare `seek` edip PNG yakalar; ffmpeg H.264 mp4'e
birleştirir. Render hızından bağımsız, tekrar alınca birebir aynı çıkar.

## Senaryo (mevcut)

1. Boş ekran — geometrik şekiller belirir, merkeze toplanıp kaybolur.
2. `SKILL.md` dosyası belirir: *"Read the documents and split them into categories."*
3. Dosya blur ile sola kayar; terminal açılır, `pip install puras` yazılıp enter'lanır.
4. Skill dosyası **5 node'lu pipeline**'a dönüşür (Ingest · Parse · Read · Classify · Output).
5. Node'lar tek tek aktifleşir, çalışır ve tamamlanır.

## Çalıştırma

```bash
cd demo
npm install
npx playwright install chromium      # ilk sefer
# apt-get install -y ffmpeg          # ffmpeg yoksa

FPS=30 node render.js                 # → out/salus-demo.mp4
```

- Canlı önizleme: `index.html`'i tarayıcıda aç (otomatik oynar).
- Render modu: renderer `?render=1` ile açar; timeline duraklatılır ve `window.__seek(t)` ile sürülür.

## Yapı

```
demo/
  index.html      # sahneler + GSAP master timeline
  render.js       # Playwright kare yakalama + ffmpeg encode
  vendor/gsap.min.js
  out/            # üretilen mp4
```

## Düzenleme

Tüm zamanlama `index.html` içindeki tek timeline'da (saniye cinsinden). Yeni
beat eklemek için ilgili `tl.to(...)` satırını uygun `at` değerine ekle —
süre `window.__DURATION__` ile otomatik hesaplanır.
