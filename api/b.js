// Vercel serverless function: renders a publicly-shared Dexeon binder.
//
// Wired via vercel.json:  /b/:id  ->  /api/b?id=:id
// Reads the world-readable Firestore doc publicBinders/{id} over the REST API
// (no secrets needed) and returns server-rendered HTML with Open Graph tags so
// shared links unfurl with a preview. Prices are hidden behind a "Show prices"
// toggle.

const PROJECT_ID = "dexeontcg";
// Public web API key (safe to expose; same value shipped in the iOS app).
const API_KEY = "AIzaSyC60umpwGL77wiBuXuENyHDQEB_AmQ9_BA";

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
    html += `<div class="grid" style="grid-template-columns:repeat(${binder.gridSize},1fr)">`;
    for (const slot of pageSlots) {
      const price = slot.marketPrice != null
        ? `<span class="price">${esc(usd(slot.marketPrice))}</span>` : "";
      const img = slot.imageURL
        ? `<img src="${esc(slot.imageURL)}" alt="${esc(slot.name || "Card")}" loading="lazy"/>`
        : `<div class="empty"></div>`;
      html += `<div class="cell">${img}${price}</div>`;
    }
    html += `</div>`;
  }
  return html;
}

module.exports = async (req, res) => {
  const id = (req.query && req.query.id) ? String(req.query.id) : "";
  const binder = id ? await fetchBinder(id) : null;

  if (!binder) {
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.status(404).end(`<!doctype html><meta charset="utf-8"><title>Binder not found · Dexeon</title>
      <body style="font-family:-apple-system,system-ui,sans-serif;text-align:center;padding:80px 20px;color:#333">
      <h1>Binder not found</h1><p>This share link may have been removed.</p></body>`);
    return;
  }

  const name = binder.name || "Binder";
  const cardCount = (binder.slots || []).filter((s) => s.cardID).length;
  const preview = (binder.slots || []).find((s) => s.imageURL);
  const title = `${name} · Dexeon`;
  const description = `A Pokémon binder with ${cardCount} card${cardCount === 1 ? "" : "s"}.`;
  const ogImage = preview ? preview.imageURL : "";

  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="${esc(title)}"/>
<meta property="og:description" content="${esc(description)}"/>
${ogImage ? `<meta property="og:image" content="${esc(ogImage)}"/>` : ""}
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="${esc(title)}"/>
<meta name="twitter:description" content="${esc(description)}"/>
<style>
  :root { color-scheme: light dark; }
  body { font-family:-apple-system,system-ui,sans-serif; max-width:900px; margin:0 auto; padding:24px; }
  h1 { font-size:28px; font-weight:800; margin:0 0 4px; }
  .sub { color:#888; font-size:14px; margin:0 0 16px; }
  button { padding:8px 14px; border-radius:10px; border:1px solid #ccc; background:transparent; font-weight:600; cursor:pointer; margin-bottom:16px; }
  .grid { display:grid; gap:10px; margin-bottom:24px; }
  .cell { position:relative; aspect-ratio:0.716; }
  .cell img { width:100%; height:100%; object-fit:contain; border-radius:8px; }
  .cell .empty { width:100%; height:100%; background:rgba(128,128,128,0.12); border-radius:8px; }
  .price { display:none; position:absolute; bottom:6px; left:6px; padding:2px 6px; border-radius:999px; background:rgba(0,0,0,0.72); color:#fff; font-size:12px; font-weight:700; }
  body.show-prices .price { display:inline; }
  footer { color:#888; font-size:12px; margin-top:32px; }
</style>
</head>
<body>
  <h1>${esc(name)}</h1>
  <p class="sub">${esc(String(cardCount))} card${cardCount === 1 ? "" : "s"}</p>
  <button onclick="document.body.classList.toggle('show-prices'); this.textContent = document.body.classList.contains('show-prices') ? 'Hide prices' : 'Show prices';">Show prices</button>
  ${renderGrid(binder)}
  <footer>Shared from Dexeon</footer>
</body>
</html>`;

  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=300, stale-while-revalidate=600");
  res.status(200).end(html);
};
