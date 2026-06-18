# Salus / Puras — Tanıtım Filmi Storyboard (saniye saniye)

Bu storyboard, kullanıcının verdiği senaryonun genişletilmiş halidir ve
`MOTION_GRAPHICS_GUIDE.md` ilkelerine göre yazılmıştır. `index.html` birebir
bunu uygular. Süreler **saniye** cinsinden, tek bir GSAP master timeline'a oturur.

**Orijinal senaryo:** boş ekran + şekiller → SKILL.md dosyası beliriyor (İngilizce
içerik) → dosya gidip terminal açılıyor, `pip install puras` → skill 5 node'lu
pipeline'a dönüşüp tek tek aktifleşiyor → bitiş.

**Genişletmeler:** referans "skillpack anatomisi" kart dili (PROMPT/TOOL/EVAL/
TYPED I/O), extreme close-up typing (ekranı dolduran yazı + dev cursor), motion
blur, sinematik kamera (push-in / dolly-out / track / Ken Burns), staging (tek
seferde tek olay), overlap/follow-through, anticipation, derinlik (parallax +
vignette + DOF).

**Toplam süre:** ~25 sn · 1920×1080 · 30 fps · motion blur (MBLUR×2) · 2× SS.

**Renk dili:** PROMPT `#8b6dff` (mor) · TOOL `#f0a93c` (amber) · EVAL `#3ddc97`
(yeşil) · TYPED I/O `#46b6e8` (mavi). Marka rengi (mor) aksiyona/akışa saklanır.

---

## Akış haritası (act'ler)

| Act | Süre | Başlık | Amaç |
|---|---|---|---|
| 1 | 0.0–3.4 | The Spark | Yokluktan fikre: şekiller belirir, cursor'a dönüşür |
| 2 | 3.4–7.8 | Writing the Skill | SKILL.md'yi **extreme close-up** yazma |
| 3 | 7.2–12.5 | Anatomy of a Skillpack | Dolly-out → kartlar dizilir (referans grid) |
| 4 | 12.5–16.6 | Install | **Extreme close-up** `pip install puras` |
| 5 | 16.6–22.4 | Go Live | Pipeline çalışır: kartlar sırayla aktifleşir |
| 6 | 22.4–25.0 | Resolve | Geniş plana çekiliş, "live", kapanış |

---

## ACT 1 — The Spark (0.0–3.4)

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 0.0 | Siyah ekran. `puras` wordmark sol-üstte fade-in (0.0–0.7) | s=1.05, hafif drift başlar | `sine.inOut` | Ken Burns (kare ölü değil) |
| 0.3 | 5 geometrik şekil (kare, daire, halka, üçgen, artı) derinlikten **parallax** ile, dağınık konumlarda scale+fade ile gelir; stagger 0.12 | yavaş drift | giriş `back.out(1.5)` (ease-out) | Staging, stagger, derinlik |
| 1.4 | Şekiller hafifçe süzülür (float), farklı hızlarda | drift | `sine.inOut` | Overlap/parallax |
| 2.0 | Şekiller merkeze yakınsar, döner, küçülür | hafif push | çıkış `power3.in` (ease-in) | Arc, exaggeration |
| 2.8 | Tek bir noktaya çöker → yanıp sönen **caret**'e dönüşür; küçük scale flash | — | `power4.in` | Geçiş örtüsü |
| 3.0–3.4 | Caret kalır, editor'e bağlanır (whip-blend) | s→1.0 | motion blur'lu geçiş | Whip pan |

---

## ACT 2 — Writing the Skill · EXTREME CLOSE-UP (3.4–7.8)

> Ekranı dolduran dev monospace yazı + ekran boyu **block cursor**. Sadece yazı
> ve cursor görünür. (Kamera zoom yerine native büyük font → keskin kalır.)

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 3.4 | Editor tam açık; dev mor block caret yanıp söner (3.4–3.9) | sabit, hafif drift | blink (step) | Kinetic typo, caret |
| 3.9 | Satır satır yazılır: `## triage` ⏎ `## research` ⏎ `## draft` (cps≈13) | caret'i **takip eden** çok hafif aşağı drift | typing (step) | Tracking/follow |
| 6.2 | Yazım biter; caret yanıp söner, metin sabit **≥1 sn okunur** | sabit | — | Hold/okunabilirlik |
| 7.2 | Dolly-out başlar (Act 3'e bağlanır) | geri çekiliş | `power3.in` | Pull-out |

İçerik (İngilizce, referansla aynı): `## triage` / `## research` / `## draft`.

---

## ACT 3 — Anatomy of a Skillpack (7.2–12.5)

> Dev yazı, SKILL.md **PROMPT** kartına küçülerek girer; etrafına bileşen
> kartları dizilir. Referans görseldeki grid birebir.

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 7.2 | Editor küçülüp kart yuvasına **motion blur** ile girer; opacity→0 (7.2–8.1) | dolly-out, s 1.0 | `power3.in` | Pull-out, motion blur |
| 7.35 | Container + SKILL.md kartı çözünür (crossfade); kart metni hazır | settle | `power3.out` | Crossfade |
| 8.2 | `search.py` (TOOL) uçarak gelir; **label kart'tan 0.12 sn sonra** oturur | — | `back.out(1.5)` | Overshoot + follow-through |
| 8.42 | `fetch.py` (TOOL) gelir | — | `back.out(1.5)` | Stagger |
| 8.64 | `grounded` (EVAL) gelir | — | `back.out(1.5)` | Stagger |
| 8.86 | `schema` (TYPED I/O) gelir | — | `back.out(1.5)` | Stagger |
| 9.6 | Container kenarı tamam; caption: *"One file → tools, evals, typed I/O"* (9.6–12.0) | yavaş **push-in** (Ken Burns) s→1.07 | `sine.inOut` | Appeal, hold |
| 11.8 | Nefes (hold) | sabit | — | Nefes payı |

Kartlar: `SKILL.md/PROMPT` · `search.py/TOOL (def search(q) → results)` ·
`fetch.py/TOOL (def fetch(url) → text)` · `grounded/EVAL (assert cited, score ≥ 0.9)` ·
`schema/TYPED I/O (in: question, out: answer)`.

---

## ACT 4 — Install · EXTREME CLOSE-UP (12.5–16.6)

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 12.5 | Skillpack **blur + geri itilir**, fade (DOF) (12.5–13.2) | dolly-back | `power3.in` | Rack focus/DOF |
| 12.9 | Terminal close-up açılır; dev yeşil caret blink (13.0–13.4) | sabit | blink | Staging |
| 13.4 | `$ pip install puras` dev punto yazılır (cps≈15) | hafif sağa drift | typing | Tracking, gerçekçi komut |
| 14.6 | Enter beat (caret blink) | — | — | Anticipation |
| 14.9 | Close-up küçülüp terminal kartına döner (blur) | dolly-out | `power3.in` | Pull-out |
| 15.4 | Çıktı **satır satır** düşer: `Collecting…` / `Installing…` (overlap) | — | `power3.out` | Follow-through |
| 16.1 | `Successfully installed puras-1.0.0` + ✓ (overshoot) | — | `back.out(1.6)` | State: success |
| 16.1 | caption: *"Install once"* (13.2–15.0) / hold | — | — | Hold |

---

## ACT 5 — Go Live · Pipeline Run (16.6–22.4)

> Skill dosyası **çalışan pipeline'a** dönüşür. Kartlar arası akış çizgileri
> belirir; node'lar (kartlar) **tek tek** aktifleşir: anticipation → spinner →
> ✓ success. Kamera aktif node'u **takip eder** (track/pan).

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 16.6 | Terminal kartı geri çekilir (blur+fade) (16.6–17.2) | — | `power3.in` | Geçiş |
| 16.9 | Skillpack keskin geri döner (fade/scale) | s→1.0 | `power3.out` | Reset |
| 17.2 | Kartlar arası **connector** çizgileri çizilir | — | `power2.out` | Akış/derinlik |
| 17.6 | **SKILL.md** aktif: hafif dip (anticipation) → glow + spinner → ✓; packet `search`e akar | aktif karta **pan** s≈1.1 | spinner `none`, badge `back.out` | Secondary action, tracking |
| 18.5 | **search.py** aktif → ✓; packet `fetch`e | pan | aynı | Tek seferde bir olay |
| 19.4 | **fetch.py** aktif → ✓ | pan | aynı | — |
| 20.3 | **grounded** aktif → ✓ | pan | aynı | — |
| 21.2 | **schema** aktif → ✓ (çıktı) | pan | aynı | — |
| 22.0 | Geniş plana **pull-out**, tüm pipeline ışıklı | s→1.0 | `power2.out` | Pull-out/resolve |

Akış sırası = skill'in runtime'ı: plan (SKILL.md) → search → fetch → grounded
(eval) → schema (typed output).

---

## ACT 6 — Resolve (22.4–25.0)

| t (sn) | Olay | Kamera | Easing | Prensip |
|---|---|---|---|---|
| 22.2 | `● live — run complete` chip belirir (overshoot) | — | `back.out(1.7)` | Kapanış vurgusu |
| 22.9 | Çok yavaş **push-in** (Ken Burns); marka kalır | s→1.05 | `sine.inOut` | Nefes, hold |
| 25.0 | Bitiş (son 0.4 sn sabit hold) | sabit | — | Hold frame |

---

## Teknik notlar (uygulama)

- Tüm hareket tek master timeline'da; CSS animasyon/transition yok (deterministik seek).
- Close-up'lar `#world` (kamera) **dışında** tam-ekran katman → her zaman keskin.
- Motion blur: `MBLUR×2` (render 60 fps → ffmpeg `tmix` → 30 fps). Daha sinematik için ×3.
- Parallax: `#stage` gradient sabit, `#world` kamerayla hareket → bedava derinlik.
- Render: `node render.js` (full: 1080p, 2× SS, crf17). Hızlı önizleme: `PREVIEW=1`.
