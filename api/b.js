// Vercel serverless function: renders a publicly-shared Dexeon binder in the
// Dexeon marketing-site visual style (manga/newsprint). Reads the world-readable
// Firestore doc publicBinders/{id} over the REST API (no secrets needed).
//
// Wired via vercel.json:  /b/:id  ->  /api/b?id=:id

const PROJECT_ID = "dexeontcg";
// Public web API key (safe to expose; same value shipped in the iOS app).
const API_KEY = "AIzaSyC60umpwGL77wiBuXuENyHDQEB_AmQ9_BA";
const SITE = "https://dexeontcg.com";

function fsValue(v) {
  if (v == null) return null;
  if ("stringValue" in v) return v.stringValue;
  if ("integerValue" in v) return Number(v.integerValue);
  if ("doubleValue" in v) return Number(v.doubleValue);
  if ("booleanValue" in v) return v.booleanValue;
  if ("nullValue" in v) return null;
  if ("arrayValue" in v) return (v.arrayValue.values || []).map(fsValue);
  if ("mapValue" in v) return fsFields(v.mapValue.fields || {});
  return null;
}
function fsFields(fields) {
  const out = {};
  for (const k of Object.keys(fields)) out[k] = fsValue(fields[k]);
  return out;
}
function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function usd(n) {
  return n.toLocaleString("en-US", { style: "currency", currency: "USD" });
}
function firstName(name) {
  const n = (name || "").trim();
  return n ? n.split(/\s+/)[0] : "";
}
function initials(name) {
  const parts = (name || "").trim().split(/\s+/).filter(Boolean).slice(0, 2);
  return parts.map((p) => p[0]).join("").toUpperCase() || "•";
}

async function fetchBinder(id) {
  const url =
    `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)` +
    `/documents/publicBinders/${encodeURIComponent(id)}?key=${API_KEY}`;
  const res = await fetch(url);
  if (!res.ok) return null;
  const doc = await res.json();
  if (!doc.fields) return null;
  return fsFields(doc.fields);
}

function renderGrid(binder) {
  const perPage = Math.max(1, binder.gridSize * binder.gridSize);
  const pages = Math.max(1, binder.pageCount);
  const slots = (binder.slots || []).slice().sort((a, b) => a.index - b.index);
  let html = "";
  for (let p = 0; p < pages; p++) {
    const pageSlots = slots.slice(p * perPage, p * perPage + perPage);
    if (pages > 1) html += `<div class="plabel">Page ${p + 1}</div>`;
    html += `<div class="page tone"><div class="slots" style="grid-template-columns:repeat(${binder.gridSize},1fr)">`;
    for (const slot of pageSlots) {
      const price = slot.marketPrice != null
        ? `<span class="price">${esc(usd(slot.marketPrice))}</span>` : "";
      const cell = slot.imageURL
        ? `<img src="${esc(slot.imageURL)}" alt="${esc(slot.name || "Card")}" loading="lazy"/>${price}`
        : `<span class="dash"></span>`;
      const cls = slot.isChase ? "slot chase" : "slot";
      html += `<div class="${cls}">${cell}</div>`;
    }
    html += `</div></div>`;
  }
  return html;
}

function sharedByHTML(binder) {
  const name = firstName(binder.ownerName);
  if (!name && !binder.ownerPhotoURL) return "";
  const avatar = binder.ownerPhotoURL
    ? `<img class="pfp" src="${esc(binder.ownerPhotoURL)}" alt="" referrerpolicy="no-referrer"/>`
    : `<span class="pfp mono">${esc(initials(binder.ownerName))}</span>`;
  return `<div class="sharedby">${avatar}<span>Shared by <b>${esc(name || "a collector")}</b></span></div>`;
}

module.exports = async (req, res) => {
  const id = (req.query && req.query.id) ? String(req.query.id) : "";
  const binder = id ? await fetchBinder(id) : null;

  if (!binder) {
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.status(404).end(page404());
    return;
  }

  const name = binder.name || "Binder";
  const cardCount = (binder.slots || []).filter((s) => s.cardID).length;
  const preview = (binder.slots || []).find((s) => s.imageURL);
  const title = `${name} · Dexeon`;
  const who = firstName(binder.ownerName);
  const description = who
    ? `${who}'s Pokémon binder — ${cardCount} card${cardCount === 1 ? "" : "s"}.`
    : `A Pokémon binder with ${cardCount} card${cardCount === 1 ? "" : "s"}.`;
  const ogImage = preview ? preview.imageURL : `${SITE}/assets/og.png`;

  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Dexeon"/>
<meta property="og:title" content="${esc(title)}"/>
<meta property="og:description" content="${esc(description)}"/>
<meta property="og:image" content="${esc(ogImage)}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="${esc(title)}"/>
<meta name="twitter:description" content="${esc(description)}"/>
<meta name="twitter:image" content="${esc(ogImage)}"/>
<meta name="theme-color" content="#C8322E"/>
<link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>
  :root{
    --paper:#F2F3EF; --paper-2:#FFFFFF; --ink:#121114; --ink-soft:#4A484E;
    --tone:#B9BCB5; --tone-2:#DDDFD8; --red:#C8322E; --red-deep:#AC322F;
    --green:#2FA44F;
    --shadow-ink:8px 8px 0 var(--ink); --shadow-ink-sm:4px 4px 0 var(--ink);
    --display:"Anton","Impact","Arial Narrow",sans-serif;
    --body:"M PLUS Rounded 1c","Nunito",system-ui,sans-serif;
    color-scheme:light;
  }
  @media (prefers-color-scheme:dark){:root{
    --paper:#131316; --paper-2:#1B1B1F; --ink:#F1F0EA; --ink-soft:#B8B6BE;
    --tone:#3A3A40; --tone-2:#2A2A2F; --red:#E0463F; --red-deep:#C8322E; color-scheme:dark;
  }}
  *,*::before,*::after{box-sizing:border-box}
  body{margin:0; background:var(--paper); color:var(--ink); font-family:var(--body); font-weight:500; -webkit-font-smoothing:antialiased; overflow-x:hidden}
  img{max-width:100%; display:block}
  a{color:inherit}
  .wrap{width:min(1080px, calc(100% - 40px)); margin-inline:auto}
  .display{font-family:var(--display); font-weight:400; text-transform:uppercase; letter-spacing:.01em; line-height:.92}
  .tone{background-image:radial-gradient(var(--tone) 1px, transparent 1.3px); background-size:7px 7px}

  .nav{position:sticky; top:0; z-index:50; background:var(--paper); border-bottom:3px solid var(--ink)}
  .nav .wrap{display:flex; align-items:center; justify-content:space-between; height:64px; gap:16px}
  .logo{display:flex; align-items:center; gap:11px; text-decoration:none}
  .logo img{width:36px; height:36px; border-radius:9px; border:2px solid var(--ink)}
  .logo b{font-family:var(--display); font-weight:400; font-size:24px; line-height:1}
  .logo small{display:block; font-size:9px; font-weight:900; letter-spacing:.3em; color:var(--red); line-height:1; margin-top:2px}
  .btn{display:inline-flex; align-items:center; gap:8px; text-decoration:none; font-weight:900; font-size:14px; letter-spacing:.02em; padding:10px 18px; border:3px solid var(--ink); background:var(--red); color:#fff; box-shadow:var(--shadow-ink-sm); transition:transform .12s ease, box-shadow .12s ease; cursor:pointer}
  .btn:hover{transform:translate(-2px,-2px); box-shadow:6px 6px 0 var(--ink)}
  .btn.ghost{background:var(--paper-2); color:var(--ink)}

  header.top{border-bottom:3px solid var(--ink); position:relative; overflow:hidden}
  header.top .wrap{padding:44px 0 40px; position:relative; z-index:2}
  .kana-bg{position:absolute; inset:0; z-index:0; display:flex; align-items:center; justify-content:flex-end; font-family:var(--body); font-weight:900; letter-spacing:.12em; font-size:clamp(90px,20vw,240px); color:transparent; -webkit-text-stroke:2px var(--tone); opacity:.5; pointer-events:none; user-select:none}
  h1.title{font-size:clamp(40px,7vw,80px); margin:10px 0 0; transform:skewX(-6deg); text-shadow:3px 3px 0 var(--paper), 6px 6px 0 var(--ink)}
  .eyebrow{display:inline-flex; align-items:center; gap:10px; font-size:12px; font-weight:900; letter-spacing:.18em; text-transform:uppercase}
  .eyebrow::before{content:""; width:26px; height:3px; background:var(--red)}
  .meta{margin-top:16px; display:flex; align-items:center; gap:18px; flex-wrap:wrap}
  .sharedby{display:inline-flex; align-items:center; gap:10px; font-size:15px; font-weight:700; color:var(--ink-soft)}
  .sharedby b{color:var(--ink)}
  .pfp{width:40px; height:40px; border-radius:50%; border:3px solid var(--ink); object-fit:cover; box-shadow:var(--shadow-ink-sm); background:var(--paper-2)}
  .pfp.mono{display:grid; place-items:center; font-family:var(--display); font-weight:400; font-size:18px; color:var(--red)}
  .count{font-size:13px; font-weight:900; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-soft)}

  main{padding:32px 0 64px}
  .toolbar{display:flex; justify-content:flex-end; margin-bottom:20px}
  .page{border:3px solid var(--ink); box-shadow:var(--shadow-ink); background:var(--paper-2); padding:14px; margin-bottom:26px}
  .plabel{font-size:12px; font-weight:900; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin:0 0 8px}
  .slots{display:grid; gap:12px}
  .slot{position:relative; aspect-ratio:0.716}
  .slot img{width:100%; height:100%; object-fit:contain; border-radius:8px}
  /* Chase (wishlist) cards render in black & white to read as "want, not have". */
  .slot.chase img{filter:grayscale(1); opacity:.9}
  .slot .dash{position:absolute; inset:0; border:2px dashed var(--tone); border-radius:8px}
  .slot .price{display:none; position:absolute; bottom:6px; left:6px; padding:2px 7px; border-radius:999px; background:var(--ink); color:var(--paper-2); font-size:12px; font-weight:800}
  body.show-prices .slot .price{display:inline-block}

  footer{background:var(--ink); color:var(--paper); border-top:3px solid var(--ink)}
  footer .wrap{padding:30px 0 40px; display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap}
  footer .mark{font-family:var(--display); font-weight:400; font-size:22px; letter-spacing:.04em}
  footer a.home{display:inline-flex; align-items:center; gap:8px; text-decoration:none; font-weight:900; letter-spacing:.04em; color:var(--paper)}
  footer a.home:hover{color:#F7C728}
  footer small{display:block; color:color-mix(in srgb, var(--paper) 60%, transparent); font-size:12px; max-width:60ch; margin-top:8px}
</style>
</head>
<body>
  <header class="nav">
    <div class="wrap">
      <a class="logo" href="${SITE}" aria-label="Dexeon home">
        <img src="/assets/icon.png" alt="" width="36" height="36"/>
        <span><b>DEXEON</b><small>デクセオン</small></span>
      </a>
      <a class="btn" href="${SITE}">Get Dexeon</a>
    </div>
  </header>

  <header class="top tone">
    <div class="kana-bg" aria-hidden="true">バインダー</div>
    <div class="wrap">
      <span class="eyebrow">Shared binder</span>
      <h1 class="title display">${esc(name)}</h1>
      <div class="meta">
        ${sharedByHTML(binder)}
        <span class="count">${cardCount} card${cardCount === 1 ? "" : "s"}</span>
      </div>
    </div>
  </header>

  <main>
    <div class="wrap">
      <div class="toolbar">
        <button class="btn ghost" id="priceToggle">Show prices</button>
      </div>
      ${renderGrid(binder)}
    </div>
  </main>

  <footer>
    <div class="wrap">
      <div>
        <div class="mark">DEXEON</div>
        <small>Track all 1025 and sleeve every card. Unofficial fan-made app; not affiliated with Nintendo, The Pokémon Company, Creatures, or Game Freak.</small>
      </div>
      <a class="home" href="${SITE}">Shared from Dexeon ↗</a>
    </div>
  </footer>

  <script>
    (function(){
      var b = document.getElementById('priceToggle');
      if(!b) return;
      b.addEventListener('click', function(){
        var on = document.body.classList.toggle('show-prices');
        b.textContent = on ? 'Hide prices' : 'Show prices';
      });
    })();
  </script>
</body>
</html>`;

  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=600");
  res.status(200).end(html);
};

function page404() {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Binder not found · Dexeon</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=M+PLUS+Rounded+1c:wght@500;800&display=swap">
<style>body{margin:0;background:#F2F3EF;color:#121114;font-family:"M PLUS Rounded 1c",system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;text-align:center;padding:24px}
h1{font-family:"Anton",sans-serif;font-weight:400;font-size:48px;transform:skewX(-6deg);margin:0 0 8px}
a{color:#C8322E;font-weight:900;text-decoration:none}
@media(prefers-color-scheme:dark){body{background:#131316;color:#F1F0EA}}</style>
</head><body><div><h1>BINDER NOT FOUND</h1>
<p>This share link may have been removed.</p>
<p><a href="${SITE}">Go to Dexeon ↗</a></p></div></body></html>`;
}
