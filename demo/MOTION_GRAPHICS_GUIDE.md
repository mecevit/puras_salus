# Motion Graphics — Ürün Tanıtım Videoları İçin Best Practice Referansı

Bu doküman, Puras/Salus tanıtım animasyonları için bir **referans**. Amaç: "düz
web sitesi animasyonu" hissinden çıkıp **sinematik, derinlikli, yönlendirilmiş**
bir motion graphics dili kurmak. Her bölümün sonunda bizim GSAP + Playwright
kurulumumuza **somut uygulama** notu var.

> TL;DR — Bir animasyonu "flat" yapan 3 şey: (1) kamera hareketsiz, (2) her şey
> aynı düzlemde/aynı anda hareket ediyor, (3) easing yok ya da lineer. Bu üçünü
> düzeltmek görüntü kalitesinin %80'ini verir.

---

## 0. Zihniyet: "Layout animasyonu" değil, "yönetmenlik"

Web animasyonu elementleri yerine oturtur. Motion graphics **bir hikâye anlatır**:
bir kamera vardır, bir odak vardır, izleyicinin gözü **yönlendirilir**. Fark:

| Flat web animasyonu | Sinematik motion graphics |
|---|---|
| Element fade/slide ile gelir, durur | Kamera push-in yapar, özneye yaklaşır |
| Her şey tek düzlemde | Ön plan / arka plan / parallax katmanları |
| Sabit çerçeve | Kamera nefes alır (drift, Ken Burns) |
| Lineer veya tek easing | Her harekete uygun easing eğrisi |
| Hepsi aynı anda | Staging: tek seferde tek olay |

---

## 1. Animasyonun 12 Prensibi (Disney) → Motion/UI karşılığı

Johnston & Thomas, *The Illusion of Life* (1981). UI/motion'a uyarlaması:

1. **Squash & Stretch** — Buton/kart "press"te hafif ezilir, geri açılır. Hayat hissi.
2. **Anticipation (Hazırlık)** — Bir olaydan önce küçük bir geri/ön hareket. Cursor tıklamadan önce hafif duraklar; node aktifleşmeden önce hafif "yüklenir".
3. **Staging (Sahneleme)** — En kritik. Aynı anda her şey oynarsa göz hiçbir yere odaklanamaz. **Tek seferde bir olay.** Birincil CTA parlarken ikincil elemanlar geri çekilir.
4. **Straight-ahead vs Pose-to-pose** — Biz pose-to-pose: anahtar pozları (keyframe) belirleyip arasını easing'e bırakırız (GSAP timeline tam bu).
5. **Follow-through & Overlapping action** — Hareket eden parçalar **aynı anda durmaz**. Kart geldiğinde içindeki başlık birkaç frame sonra yerine oturur. En çok ihmal edilen, en çok "pahalı" hissi veren prensip.
6. **Slow in & Slow out (Easing)** — Gerçek nesneler ani hızlanıp durmaz. Lineer hareket = robotik. (Bölüm 3.)
7. **Arc (Yay)** — Doğal hareket düz çizgi değil, hafif yay çizer. Cursor ve uçuşan elementler düz değil eğri gitsin.
8. **Secondary action (İkincil hareket)** — Ana hareketi destekleyen küçük detaylar: tıklamada ripple, node aktifken dönen spinner, glow nabzı. Micro-interaction'ların temeli.
9. **Timing (Zamanlama)** — Frame sayısı duyguyu belirler. Hızlı = enerjik/teknik, yavaş = güvenilir/premium. (Bölüm 4.)
10. **Exaggeration (Abartma)** — Gerçeğe birebir sadık kalmak donuk durur; hareketleri bir tık abart (overshoot, back-ease).
11. **Solid drawing (Hacim/derinlik)** — Düzlem değil mekân hissi: gölge, parallax, perspektif, depth-of-field. (Bölüm 5–6.)
12. **Appeal (Çekicilik)** — Tutarlı görsel dil, hoş renk/ışık, gereksizden arınmış kompozisyon.

**Uygulama:** Timeline yazarken her beat için sor: *anticipation var mı? overlap var mı? easing doğru mu? staging temiz mi?*

---

## 2. Staging & görsel hiyerarşi (zamanda)

- **Sahnede TEK aksiyon (staging'in özü).** Bir sahnede aynı anda tek bir şey olur
  (biri yazar VEYA bir buton tıklanır VEYA bir panel kurulur). İzleyici aynı anda
  2-3 şeyi takip edemez (bilişsel yük). İki şey ilişkiliyse **uzayda yan yana
  değil, zamanda sırayla** göster (önce yaz, sonra sonucu göster). Kamera o tek
  aksiyona zoom edip **takip eder**; bitince geri çekilip sonucu gösterir.
- **Tek odak noktası.** Her an tek eleman en parlak/keskin/büyük/hareketli olsun;
  gerisi soluk/blur/küçük. Odak özne karenin ~⅓–½'ini doldursun. Gözü kontrast,
  ışık ve yönlendirici çizgilerle odak noktasına taşı.
- **Tek seferde bir mesaj.** Sahneyi beat'lere böl; her beat'te göz tek bir yere gitsin.
- **Giriş sırası anlam taşır.** Elemanları stagger ile sırayla getir (kartlar 60–120ms arayla). Hepsi birden gelmesin.
- **Kontrastla yönlendir.** Aktif eleman parlak/büyük/keskin; gerisi soluk/blur/küçük.
- **Negatif alan.** Boşluk lükstür; her pikseli doldurma.
- **Maskeleme/reveal.** Şekil/clip ile parçalı açılış merak uyandırır (ör. dairesel maske ile reveal).

---

## 3. Easing (en kritik teknik detay)

Lineer hareketten kaçın. Material 3'ün dört eğrisi pratikte yeterli:

| Amaç | CSS cubic-bezier (yaklaşık) | GSAP karşılığı |
|---|---|---|
| **Standard** (yer değiştirme, her ikisi de) | `cubic-bezier(0.2, 0, 0, 1)` | `power3.inOut` |
| **Decelerate / Ease-out** (ekrana **girerken**) | `cubic-bezier(0, 0, 0, 1)` | `power3.out` / `expo.out` |
| **Accelerate / Ease-in** (ekrandan **çıkarken**) | `cubic-bezier(0.3, 0, 1, 1)` | `power3.in` |
| **Emphasized** (kahraman hareketleri) | `cubic-bezier(0.2, 0, 0, 1)` (uzun) | `power4.inOut` |
| **Overshoot / canlı giriş** | spring/back | `back.out(1.5–2)`, `elastic.out` (idareli) |

Kurallar:
- **Giren** eleman ease-**out** (hızlı gelir, yumuşak oturur). **Çıkan** eleman ease-**in** (yumuşak başlar, hızla gider). Bu tek kural bile çok şey değiştirir.
- Kamera hareketleri için `sine.inOut` veya `power2.inOut` — yumuşak, sinematik.
- `back.out` ve `elastic` sadece "kahraman" anlarda; her yerde kullanma, ucuzlaşır.
- **Lineer (`none`) sadece** sürekli dönen spinner / sonsuz döngü içindir.

---

## 4. Timing, ritim ve hold süreleri

- **UI mikro-hareket:** 200–500ms ideal (mobil 200–300, masaüstü 300–450). Çok hızlı = fark edilmez; çok yavaş = bekletir.
- **Mesafeye göre süre.** Uzağa giden eleman daha uzun sürmeli; sabit süre kullanma.
- **Okunabilir metin hold'u:** Bir yazı yerine oturduktan sonra en az **0.5 sn** sabit dursun (kinetic typography kuralı). Önemli cümlelerde 1–2 sn.
- **Ritim/beat.** Sahneleri müzikteki gibi vuruşlara böl; monoton tempo sıkıcıdır — yavaş kur, hızlı öde, sonra nefes aldır.
- **Nefes payı.** Yoğun bir andan sonra 0.5–1 sn sakin "hold" koy; izleyici sindirir.

---

## 5. Kamera dili (bu projede eksik olan ana şey)

Kamera, flat hissi kıran en güçlü araç. Teknikler:

- **Push-in / Dolly-in (yaklaşma):** Özneye yavaş yaklaşma. Dikkati toplar, önemi artırır. *(Bizde: input'a/terminale/dosyaya close-up.)* "Zoom"dan farkı: parallax ile derinlik hissi verir.
- **Pull-out / Dolly-out (uzaklaşma):** Geri çekilip bağlamı/bütünü gösterme. Sahne kapanışlarında güçlü.
- **Pan / Tilt (yatay/dikey kaydırma):** Çerçeveyi kaydırarak gözü yeni bir bölgeye taşır. Aksiyonu **takip et** (ör. soldan sağa aktifleşen node'ları izle).
- **Tracking / Follow (takip):** Hareket eden özneyi kamerayla izle. *(Bizde: yazarken caret'i takip etmek — tam istenen şey.)*
- **Whip pan / hızlı geçiş:** Sahneler arası enerjik, blur'lü hızlı kaydırma (geçiş örtüsü olarak).
- **Ken Burns / yavaş drift:** "Sabit" planlarda bile çok hafif sürekli zoom/pan — kare asla ölü durmaz.
- **Rack focus (odak kayması):** Ön plandan arka plana odağı kaydır (blur ile). Dikkati taşır.

**Altın kural:** Kamera **amaçla** hareket eder — izleyicinin bakması gereken yere onu götürür. Amaçsız sürekli hareket baş döndürür; her kamera hareketinin bir gerekçesi olmalı (yeni özne, vurgu, geçiş).

**Uygulama (GSAP):** Tüm sahne içeriğini tek bir `#world` katmanına sar; kamerayı bu katmana uygulanan `transform: translate(tx,ty) scale(s)` ile modelle. Bir dünya-noktasını `(wx,wy)` ekran merkezine `s` ölçeğinde getirmek için: `tx = 960 − s·wx`, `ty = 540 − s·wy`. `transform-origin: 0 0`. Kamerayı bir proxy obje `{x,y,s}` üzerinde `gsap.to(...)` ile sür, `onUpdate`'te transform'u yaz. Easing: `sine.inOut` / `power2.inOut`.

---

## 6. Derinlik & parallax

Mekân hissi = katmanlar farklı hızda.

- **Parallax:** Yakın katman hızlı, uzak katman yavaş hareket eder. Kamera pan/push yaparken arka plan (grid/orb) daha az kıpırdarsa derinlik doğar. *(Bizde bedava parallax: `#stage` gradient'i sabit kalırken `#world` kamerayla hareket eder.)*
- **Depth of field (alan derinliği):** Odaktaki keskin, gerisi blur. Close-up'ta arka planı hafif blur'la + karart.
- **Gölge & yükseklik:** Kartlara yumuşak, geniş gölge (elevation). Düz gölge ucuz durur.
- **Vignette:** Kenarları hafif karartmak gözü merkeze çeker, sinematik çerçeve verir.
- **Işık/glow:** Aktif/önemli elementte yumuşak glow nabzı; abartma.

---

## 7. Kinetic typography (yazı animasyonu)

- **Okunaklı font** (Inter/Roboto/Helvetica). İnce script ve aşırı dekoratif fontlardan kaçın — harekette okunmaz.
- **Yerine oturunca en az 0.5 sn sabit dur.** Hareket halinde okutma.
- **Bir bölümde tek "kinetic an".** Her cümleyi uçurma; vurgu kaybolur.
- **Harf/satır stagger.** Kelime/satır sırayla gelsin; ama monospace "typing" efektinde caret'i gerçekçi yanıp söndür.
- **3Hz üstü flaş yok** (erişilebilirlik / nöbet riski).
- **Kontrast yeterli** olsun; blur/glow okunabilirliği bozmasın.

---

## 8. Ürün/yazılım demoları için özel notlar

- **Cursor sinematiği:** Cursor düz değil yay çizerek, ease ile gelsin; tıklamadan önce hafif yavaşlasın (anticipation), tıklamada **ripple + buton squash**.
- **Tıklamada otomatik zoom:** Tıklanan/önemli bölgeye kamera yaklaşsın (Screen Studio, FocuSee gibi araçların yaptığı). İzleyici nereye bakacağını bilir.
- **Smooth cursor:** Ham fare hareketi titrektir; spring/interpolasyon ile yumuşat.
- **Gerçekçi içerik:** Sahte ama inandırıcı veri (gerçek log satırları, gerçek komut). Lorem ipsum değil.
- **Terminal/komut:** Karakter karakter yaz, enter'da çıktı **satır satır** gecikmeli düşsün.
- **State geçişleri:** loading → spinner → success (check + yeşil). Her node "çalışıyor"u görünür kıl.

---

## 9. Renk, ışık, kompozisyon

- **Sınırlı palet** + 1–2 vurgu rengi. Marka rengini aksiyona sakla.
- **Koyu tema** tech/premium hissi verir; glow ve derinlik koyu zeminde parlar.
- **Tutarlı köşe yarıçapı, boşluk, çizgi kalınlığı** (design token mantığı).
- **Kontrast & odak:** Aktif eleman en parlak; geri plan bastırılmış.
- **Hizalama ızgarası:** Elemanlar görünmez bir grid'e otursun.

---

## 10. Teknik üretim (bu projeye özel)

- **Deterministik render:** Tüm hareket tek bir GSAP timeline'da; CSS `@keyframes`/`transition` **kullanma** (duvar-saatine bağlı, seek edilemez). Renderer `tl.time(t)` ile kare kare ilerler.
- **FPS:** 30 (web/demo) yeterli; 60 daha akıcı ama 2× kare/maliyet. Hareket çok hızlıysa 60 düşün.
- **Çözünürlük:** 1920×1080. Zoom/push-in'de metin yumuşamasın diye, agresif yakınlaşmada renderer'da `deviceScaleFactor: 2` ile çekip ffmpeg'de küçültmek keskinlik verir (maliyeti 2×).
- **Motion blur:** Hızlı geçişlerde hafif blur (whip pan) hareketi yumuşatır; ffmpeg `tblend`/`minterpolate` ile de eklenebilir.
- **Encode:** H.264 `-crf 17 -preset slow -pix_fmt yuv420p -movflags +faststart`. Daha küçük dosya için crf 20–23.
- **Hold frame'ler:** Başta/sonda 0.3–0.5 sn sabit kare bırak (donuk kesim olmasın).

---

## 11. Hızlı checklist (her render öncesi)

- [ ] Kamera **amaçlı** hareket ediyor mu? Hiç ölü/sabit kare var mı?
- [ ] Her **giren** ease-out, her **çıkan** ease-in mi?
- [ ] Lineer hareket kalmış mı? (Sadece spinner lineer olmalı.)
- [ ] **Her sahnede TEK aksiyon mu?** Aynı anda 2+ rakip hareket varsa böl.
- [ ] Her an tek odak noktası var mı, kamera onu takip ediyor mu?
- [ ] Marka logosu/wordmark'ı gerçek mi (yanlış/jenerik logo değil)?
- [ ] Overlap/follow-through var mı, yoksa her şey aynı anda mı duruyor?
- [ ] Metin oturduktan sonra ≥0.5 sn okunabiliyor mu?
- [ ] Derinlik var mı (parallax / gölge / DOF / vignette)?
- [ ] Anticipation + tıklama feedback'i (ripple/squash) var mı?
- [ ] Tempo nefes alıyor mu, yoksa monoton mu?
- [ ] Palet tutarlı, vurgu rengi aksiyona saklanmış mı?

## 12. Anti-pattern'ler (kaçın)

- Her şeyin aynı anda fade-in olması.
- Sabit, hareketsiz kamera (flat hissin 1 numaralı sebebi).
- Lineer easing / tek tip easing her yerde.
- Aşırı `elastic`/`bounce` — ucuz ve yorucu.
- Çok hızlı geçen okunamaz metin.
- Amaçsız sürekli zoom/sallanan kamera (baş döndürür).
- Tek düzlem, derinliksiz kompozisyon.
- Lorem ipsum / inandırıcı olmayan sahte veri.

---

## Kaynaklar

- [Staging in Animation (single focal point, one action) — Animotions Studio](https://animotionsstudio.com/animation-staging/)
- [Staging — Darvideo dictionary](https://darvideo.tv/dictionary/staging/)
- [The Psychology of Camera Movement — Rocket House Pictures](https://rockethousepictures.com/blog/the-psychology-of-camera-movement-in-video-production.html)
- [Motion Graphics for Attention (cognitive load) — Number Analytics](https://www.numberanalytics.com/blog/motion-graphics-for-attention)
- [Disney's 12 Principles applied to UI Animation — Interaction Design Foundation](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)
- [12 Principles of Animation: A Guide to Motion Design — Uxcel](https://uxcel.com/blog/12-principles-of-animation-a-guide-to-motion-design-133)
- [A Guide to Motion Design Principles — Toptal](https://www.toptal.com/designers/ux/motion-design-principles)
- [10 Principles of Motion Design — VMG Studios](https://blog.vmgstudios.com/10-principles-motion-design)
- [12 Principles of Animation — Superside](https://www.superside.com/blog/12-principles-of-animation)
- [Easing and duration — Material Design 3](https://m3.material.io/styles/motion/easing-and-duration)
- [Duration & easing — Material Design (M1)](https://m1.material.io/motion/duration-easing.html)
- [Different Types of Camera Movements in Film — StudioBinder](https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/)
- [Parallax Effect Explained — Filmora](https://filmora.wondershare.com/video-creative-tips/what-is-parallax-effect.html)
- [Typography in Motion: 7 Design Principles — Upskillist](https://www.upskillist.com/blog/typography-in-motion-7-design-principles/)
- [Kinetic Typography Guide — IK Agency](https://www.ikagency.com/graphic-design-typography/kinetic-typography/)
- [Screen Studio — cinematic screen recordings](https://screen.studio/)
- [FocuSee — Auto Zoom & Cursor Animation](https://focusee.imobie.com/features/auto-zoom-and-cursor-animation.htm)
