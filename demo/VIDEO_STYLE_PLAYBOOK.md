# Puras Tanıtım Videosu — Stil & Üretim Playbook'u

Bu doküman, beğenilen son videonun (**Anthropic "Claude Design" dili**) stilini ve
geliştirme sürecinde verilen **tüm feedback'leri** kalıcı kurallara çevirir.
**Yeni bir video yapmadan önce bu dosyayı oku ve uygula.** Canonical uygulama:
`demo/index.html` (GSAP timeline + Playwright + ffmpeg).

İlgili dosyalar: `MOTION_GRAPHICS_GUIDE.md` (genel motion ilkeleri),
`STORYBOARD.md` (saniye-saniye şablon), `render.js` (render pipeline).

---

## 0. Altın kurallar (feedback'lerden damıtılmış)

Kullanıcının iterasyonlarda söylediği her şey, somut kural olarak:

1. **Fade in/out ile geçiştirme — MORPH yap.** "Basit fade out/in ile çözmüşüm"
   denildi. Objeler birbirine **dönüşmeli**: input kutusu Send'e basınca **küçülüp
   loader pill'ine morph olur** (aynı kutu shrink). Bkz. §4 "Morph pattern".
2. **Kamera sakin olmalı, zig-zag YOK.** "Kamera çok zig-zag yapıyor, insanın başı
   dönüyor." → Sahne içinde kart-kart atlama yapma. Sadece **yavaş, merkezi, tek
   yönlü** push-in / pan / zoom-out. Hareketin gözü ışık/aktif eleman yönlendirir.
3. **Bir liste/öğeler dizilirken kamera close-up + aşağı pan, bitince smooth
   zoom-out.** "Parse skill / generate… alt alta sıralanırken kamera oraya closeup
   yapabilir, liste bitince smooth zoom-out'la tüm pencereyi görebiliriz." Bkz. §4.
4. **Motion blur GÖRÜNÜR olmalı.** ffmpeg frame-blend (×2) çok zayıf kaldı; iki kez
   "motion blur yok" dendi. → **Engine-içi** blur: hareket eden objeye hareket
   anında `filter:blur()` bindir (giriş/çıkış/kayma). Bkz. §5.
5. **Render HIZLI olmalı.** "Render süresi çok uzun, iterasyon hızımız yavaşlıyor."
   → Preview: **jpeg + yarı çözünürlük (dsf 0.5) + tek rAF**, ve `MAXT=N` ile kısa
   bakış. ~5dk → ~70-90sn. Bkz. §6.
6. **Extreme close-up'lar.** Yazı yazılırken "input ekranı doldursun, cursor ekran
   boyu olsun, sadece yazı + cursor". Büyük native font ya da güçlü push-in.
7. **Gerçek referansa birebir sadık kal.** Bir referans verilince (görsel/video)
   onu kare kare incele, paleti/tipografiyi/UI'ı **birebir** yakala — yaklaşık değil.
8. **Önce hızlı preview, onay sonra full render.** Her iterasyonu küçük render'la
   göster; onaylanınca 1080p/2×SS final al.

---

## 1. Görsel dil — "Claude Design" stili

Beğenilen videonun DNA'sı (Anthropic ürün filmi):

### Palet
| Rol | Hex | Kullanım |
|---|---|---|
| Paper (sıcak fildişi) | `#F2ECE1` / `#EDE6D8` | Ana light zemin |
| Ink | `#211D17` | Light üstü metin |
| **Clay / terracotta** | `#C96442` (hover `#B5543A`) | **Vurgu**: Send/Deploy butonu, spark, highlight |
| Night | `#0B0C0F` / `#101218` | Dramatik sonuç sahnesi |
| Teal | `#5FD2C2` (`#2F9C8E`) | Dark sahnede glow / akış / "running" |
| Muted | `#8C8473` | İkincil metin |
| Line | `#E1D9C9` | İnce kenarlık |

> **Tek vurgu rengi** (terracotta) aksiyona saklanır; sonuç sahnesinde teal glow.

### Tipografi
- **Serif (display):** `Copernicus, Georgia, serif`. Wordmark, başlıklar, **italic
  serif gerund loader** ("Scaffolding…"), sonuç başlığı.
- **Sans (UI):** `Styrene, Inter, system-ui`. Butonlar, label'lar, panel.
- **Mono:** dosya adları, kod, terminal, node etiketleri.

### İmza öğeler (bunlar olmazsa stil tutmaz)
1. **✷ Spark / asterisk** — terracotta sunburst mark (12 ışın). Wordmark'ta ve
   loader spinner'ında. `sparkSVG()` ile üretilir (index.html).
2. **Gerund loader** — dönen spark + **italic serif** kelime, cycling:
   "Scaffolding… → Grounding… → Wiring… → Compiling…". Referansta "Designing…/
   Soldering…/Dimming…". En karakteristik öğe.
3. **Gerçek ürün UI'ı** — yuvarlak köşeli kartlar, yumuşak gölge, gerçek butonlar
   (Send, Import, Deploy), input alanı, app penceresi (traffic-light dots + üst bar).
4. **Cursor etkileşimi** — gerçek mouse cursor; yay çizerek gelir, **tıklamada
   buton basılır (scale .95) + ripple halkası**. Yazıyı cursor "yazar".
5. **light → dark → light** ritmi: prompt (light) → loader → **dramatik dark
   reveal** (glow) → editor (light) → kapanış (light).
6. **Plan checklist** (Claude-Code tarzı) — "✓ Parse… / ✓ Generate…" alt alta
   tick'lenir, "Progress n/5".

### His
Sakin, premium, minimal. Bol negatif alan. Vignette (dark sahnede). Yavaş kamera.

---

## 2. Anlatı yapısı (beat'ler)

Puras'a uyarlanmış akış (`index.html`):

1. **Intro** — `✷ puras` serif wordmark, fildişi zemin. Spark back.out ile gelir.
2. **Prompt** — "Describe the skill you want to ship" italic serif label + temiz
   input kartı. Cursor girer, prompt'u **yazar**, Send'e **tıklar** (basma+ripple).
   Yazarken hafif push-in.
3. **Morph → Loader** — kart **küçülüp pill'e dönüşür**; spark döner + gerund cycler.
   Zemin night'a geçer.
4. **Result (dark reveal)** — teal glow'lu pipeline: `SKILL.md → search → fetch →
   grounded → schema` node'ları **sırayla yanar**, bağlantılar çizilir. Serif başlık
   "From one file to a *running* skill". Çok yavaş push.
5. **Editor / Plan** — light app penceresi (üst bar: Logs/Comment/Deploy). Sol'da
   glowing globe + serif başlık; sağda **Plan checklist** tick'lenir. Kamera
   checklist'e **close-up + aşağı pan**, bitince **zoom-out** → tüm pencere. Cursor
   Deploy'a tıklar.
6. **End** — `✷ puras` wordmark, fildişi. Yavaş push, hold.

Süre ~30 sn. Her sahne arası **morph veya kamera geçişi** (fade değil).

---

## 3. Teknik altyapı (özet)

- Tek **GSAP master timeline** (`paused`), renderer `tl.time(t)` ile kare kare seek.
  **CSS animation/transition YOK** (deterministik olmalı).
- **Kamera** = `#world` katmanına `translate(960−s·x, 540−s·y) scale(s)` (origin 0 0).
  `camTo(at,dur,x,y,s,ease)` proxy obje + `onUpdate`. Easing `sine/power.inOut`.
  **Aynı `cam` objesinde tween'ler ÜST ÜSTE binmemeli** (jitter yapar).
- Close-up'lar / overlay'ler `#world` dışında olabilir (kameradan etkilenmez, keskin).
- Parallax: `#stage` arka planı sabit, `#world` kamerayla hareket.
- Render: Playwright headless Chromium → kare → ffmpeg H.264.

---

## 4. Kod desenleri (kopyala-kullan)

### Spark (asterisk)
```js
function sparkSVG(){ let s='';
  for(let i=0;i<12;i++){const a=i*30,l=i%3===0;
    s+=`<line x1=50 y1=50 x2=50 y2=${l?12:20} transform="rotate(${a} 50 50)"
        stroke="currentColor" stroke-width=${l?7:5} stroke-linecap="round"/>`;}
  return `<svg viewBox="0 0 100 100">${s}</svg>`; }
document.querySelectorAll('.spark').forEach(e=>e.innerHTML=sparkSVG());
```

### MORPH pattern (obje → obje dönüşümü, fade değil)
Aynı kabın içine iki içerik koy (örn. `#promptInner` + `#loadInner`); kabı küçült,
içerikleri crossfade et:
```js
const morphAt=clickAt+0.45;
tl.set("#morph",{height:()=>$("#morph").offsetHeight}, morphAt);   // auto height'i kilitle
tl.to("#promptInner",{opacity:0,duration:.22}, morphAt);           // eski içerik çık
tl.to("#morph",{width:380,height:104,borderRadius:22,duration:.62,ease:"power4.inOut"}, morphAt+0.18);
tl.to("#loadInner",{opacity:1,duration:.3}, morphAt+0.52);          // yeni içerik gir
```
Genel kural: bir öğe diğerine "dönüşecekse" ya **tek kabı resize+crossfade** et, ya
da kaynağı hedefin pozisyon/boyutuna `scale`+`x/y` ile taşıyıp blur'la kapat.

### Cursor (gerçek tıklama hissi)
```js
function curTo(at,dur,el){const c=wc($(el)); tl.to("#cursor",{left:c.x,top:c.y,duration:dur,ease:"power3.inOut"},at);}
function curClick(at){ tl.to("#cursor",{scale:.82,duration:.08},at).to("#cursor",{scale:1,duration:.18},at+.08);
  tl.fromTo("#cripple",{opacity:.8,scale:.3},{opacity:0,scale:1.1,duration:.5},at); }   // ripple
```
`wc(el)` = elemanın **world** merkezi (offsetParent zincirini #world'e kadar toplar;
transform'lardan etkilenmez) → cursor UI'a tam oturur.

### Liste close-up + zoom-out (feedback #3)
```js
const a=wc($("#pr1")), e=wc($("#pr5"));
camTo(edAt+0.4,0.9, a.x, a.y+20, 1.5);        // listeye close-up
camTo(edAt+1.3,1.9, a.x, e.y-10, 1.5);        // item'lar dizilirken AŞAĞI pan
// ... item'lar tick'lenir (stagger 0.5) ...
camTo(edAt+3.5,1.4, 960,540, 0.94,"power3.inOut");  // bitince SMOOTH ZOOM-OUT (tüm pencere)
```

### Motion blur (engine-içi, görünür — feedback #4)
Hızlı giriş/çıkışa blur bindir; rest'te 0:
```js
gsap.set(card,{opacity:0,y:92,scale:.8,filter:"blur(16px)"});
tl.to(card,{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.6,ease:"back.out(1.4)"});
```

---

## 5. Render komutları

```bash
cd demo
# Hızlı iterasyon önizlemesi (~70-90s): 960x540 jpeg, dsf 0.5, tek rAF
PREVIEW=1 node render.js
# Sadece ilk N saniyeye bak (çok hızlı):
PREVIEW=1 MAXT=6 node render.js
# Teslim: 1080p, 2× supersampling, crf17 (birkaç dk)
node render.js
# İstenirse ekstra sinematik blur: MBLUR=2/3 (yavaşlatır)
```
Knob'lar: `FPS SS FMT JQ OUT_W OUT_H CRF PRESET MBLUR MAXT OUT` (bkz. render.js).

---

## 6. Yeni video checklist'i (render öncesi)

- [ ] Palet: fildişi zemin + **tek** terracotta vurgu + serif display?
- [ ] Spark + **italic serif gerund loader** var mı?
- [ ] Geçişler **morph / kamera** mı, yoksa kaçınılması gereken **fade in/out** mu?
- [ ] Kamera **sakin** mi — zig-zag / amaçsız atlama yok mu?
- [ ] Liste dizilirken close-up + pan, bitince **zoom-out** var mı?
- [ ] Motion blur **görünür** mü (engine-içi, hızlı hareketlerde)?
- [ ] Gerçek UI + cursor **tıklama feedback'i** (basma + ripple)?
- [ ] Extreme close-up'larda yazı + cursor yeterince büyük mü?
- [ ] light → dark reveal → light ritmi korunuyor mu?
- [ ] Önce **hızlı preview**, onay sonra full render?
- [ ] CSS animation/transition kullanılmadı (sadece GSAP timeline)?
