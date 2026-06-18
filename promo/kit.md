# Promo craft KIT — primitives only, NO timeline

This is your **craft kit**, not a script. It gives you the polished tokens,
helpers and components. **There is no scene flow here on purpose** — you invent
the timeline from the brief's own concept. Lift what you need; ignore the rest.

> ⛔ Do NOT reproduce the old default flow (logo → prompt card → "Scaffolding…"
> gerund loader → 3–4 glowing nodes → editor+checklist → logo). That skeleton is
> banned as a default. Invent a different timeline every brief.

---

## 1) Design tokens (pick a theme that fits the BRAND)

```css
:root{
  /* LIGHT theme */
  --paper:#F2ECE1; --paper2:#EDE6D8; --ink:#211D17; --muted:#8C8473; --line:#E1D9C9;
  /* DARK theme (use for dev/tech/night brands) */
  --night:#0B0C0F; --night2:#101218; --ink-d:#E9EDF7; --muted-d:#8A93A6; --line-d:rgba(255,255,255,.10);
  --accent:#C96442;        /* the SINGLE accent = accent_color (brand) */
  --glow:#5FD2C2;          /* a secondary glow for reveals, brand-tinted */
  --serif:'Copernicus','Georgia',serif; --sans:'Inter',system-ui,sans-serif;
  --mono:ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,monospace;
}
```
Rules: ONE accent, saved for the key action/highlight. Serif for wordmark/
headlines/the italic loader word; sans for UI; mono for code. Match light vs dark
to the brand.

## 2) Boilerplate shell (empty stage, all wiring done — you add scenes)

```html
<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:var(--night);font-family:var(--sans)}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden}
.bg{position:absolute;inset:0;z-index:0}
#world{position:absolute;inset:0;width:1920px;height:1080px;transform-origin:0 0;will-change:transform}
.scene{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}
#vignette{position:absolute;inset:0;z-index:9;pointer-events:none;opacity:0;
  background:radial-gradient(125% 125% at 50% 47%,transparent 50%,rgba(0,0,0,.55))}
#cursor{position:absolute;left:0;top:0;width:38px;height:38px;z-index:20;opacity:0;
  filter:drop-shadow(0 5px 8px rgba(0,0,0,.35))}
#cripple{position:absolute;width:80px;height:80px;border-radius:50%;border:2px solid var(--accent);
  z-index:19;margin:-40px 0 0 -40px;opacity:0}
/* …your component CSS here… */
</style></head><body>
<div id="stage">
  <div class="bg" id="bg"></div>
  <div id="world"><!-- your scenes go here as .scene blocks --></div>
  <div id="vignette"></div>
  <svg id="cursor" viewBox="0 0 24 24"><path d="M4 2 L20 12 L13 13 L17 21 L14 22 L10 14 L4 18 Z" fill="#1a1a1a" stroke="#fff" stroke-width="1.3" stroke-linejoin="round"/></svg>
  <div id="cripple"></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script>
const $=s=>document.querySelector(s);
const tl=gsap.timeline({paused:true,defaults:{ease:"power3.inOut"}});

/* camera: frame one element at a time and FOLLOW the action */
const world=$("#world"),cam={x:960,y:540,s:1};
const setCam=()=>{const s=cam.s;world.style.transform=
  `translate(${(960-s*cam.x).toFixed(2)}px,${(540-s*cam.y).toFixed(2)}px) scale(${s})`;};setCam();
function camTo(at,dur,x,y,s,e="sine.inOut"){tl.to(cam,{x,y,s,duration:dur,ease:e,onUpdate:setCam},at);}
function wc(el){let x=el.offsetWidth/2,y=el.offsetHeight/2,n=el;
  while(n&&n.id!=='world'){x+=n.offsetLeft;y+=n.offsetTop;n=n.offsetParent;}return{x,y};}
/* cursor */
function curTo(at,dur,sel){const c=wc($(sel));tl.to('#cursor',{left:c.x,top:c.y,duration:dur,ease:'power3.inOut'},at);}
function curClick(at){tl.to('#cursor',{scale:.82,duration:.08},at).to('#cursor',{scale:1,duration:.18},at+.08);
  tl.fromTo('#cripple',{opacity:.8,scale:.3,left:gsap.getProperty('#cursor','left'),top:gsap.getProperty('#cursor','top')},{opacity:0,scale:1.1,duration:.5},at);}
/* type into an element, char by char */
function typeInto(el,text,start,cps){const step=1/cps;for(let i=1;i<=text.length;i++){
  tl.call(()=>{$(el).innerHTML=text.slice(0,i).replace(/\n/g,"<br>");},null,start+(i-1)*step);}return start+text.length*step;}
/* blink a caret between [from,to] */
function blink(el,from,to){let t=from;while(t<to-.25){tl.set(el,{opacity:1},t);tl.set(el,{opacity:0},t+.28);t+=.56;}tl.set(el,{opacity:1},to);}
/* brand spark — PURAS/CLAUDE ONLY. other brands: draw their own mark instead */
function sparkSVG(){let s='';for(let i=0;i<12;i++){const a=i*30,l=i%3===0;
  s+=`<line x1=50 y1=50 x2=50 y2=${l?12:20} transform="rotate(${a} 50 50)" stroke="currentColor" stroke-width=${l?7:5} stroke-linecap="round"/>`;}
  return `<svg viewBox="0 0 100 100">${s}</svg>`;}

/* ===== BUILD YOUR SCENES on `tl` here ===== */
/* …compose the timeline that tells THIS brief's story… */

window.__DURATION__=tl.duration()+0.5;
window.__seek=t=>tl.time(Math.min(t,tl.duration()),false);
window.__BLUR_SEGMENTS__=[/* [a,b] fast windows: fast moves/zooms only */];
if(!location.search.includes("render"))tl.play(0);
</script></body></html>
```

## 3) Component catalog (drop-in; restyle to the brand; combine freely)

Each is a `.scene` you place in `#world`; animate with `tl`. Pick only the ones
THIS story needs — you rarely need more than 2–3 distinct component types.

- **Window chrome** `<div class="win"><div class="bar"><i·i·i> title</div><div class="body">…</div></div>` — soft shadow, rounded; for app/editor/dashboard.
- **Code editor** — `.body` with line-number gutter + mono code + a caret span you `typeInto`.
- **Terminal** — black `.body`, green `$`, mono; lines drop in one at a time.
- **Node + connector** — rounded box with label + a glowing border (`box-shadow:0 0 40px -6px var(--glow)`); connectors = thin lines whose `width` you tween 0→100%; a "packet" dot travels along.
- **KPI counter** — a big mono/serif number you tween via a proxy `{v:0}`→target with `onUpdate`.
- **Card / chip** — rounded surface, 1px border, soft shadow; flies in with `back.out(1.4)` + motion blur.
- **Phone frame** — 380×800 rounded-rect, notch, screen inside; for mobile products.
- **Bar chart** — fl/grid of bars whose `height`/`scaleY` tween in, stagger.
- **Loader pill** *(OPTIONAL, brand mark + italic-serif gerund)* — use ONLY if it fits; not required.
- **Checklist row** *(OPTIONAL)* — ✓ box + label; tick one at a time.
- **Wordmark lockup** — the BRAND's real mark + name (serif/sans to match). Spark only for puras/claude.

## 4) Compose YOUR OWN timeline

There is no required order. Decide the scenes, count, layout and transitions from
the brief's concept (see SKILL.md → *Concept first* + *Direction* rules). Keep:
ONE action per scene · one focal point · camera follows it · real brand identity ·
deterministic contract (`__DURATION__`/`__seek`/`__BLUR_SEGMENTS__`, no CSS keyframes).
