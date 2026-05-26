/* InvestMQuest — Supply Chain Map engine v1
 * Each topic HTML sets <body data-topic="xxx"> and includes this file.
 * The engine fetches:
 *   data/{topic}.json  — node graph for the topic
 *   data/_dd_links.json — ticker → DD report path (built by scripts/build_supply_chain_dd_index.py)
 *   data/_topics.json  — manifest of all topics + active flag, drives tab strip
 */
(function () {
const COMP = {
  monopoly:   { label:"壟斷",     en:"Monopoly",    cssVar:"--c-monopoly"   },
  oligopoly:  { label:"寡占",     en:"Oligopoly",   cssVar:"--c-oligopoly"  },
  redocean:   { label:"紅海競爭", en:"Red Ocean",   cssVar:"--c-redocean"   },
  highgrowth: { label:"高速增長", en:"High Growth", cssVar:"--c-highgrowth" },
  emerging:   { label:"新興萌芽", en:"Emerging",    cssVar:"--c-emerging"   },
};
const FLAG = { TW:"🇹🇼", US:"🇺🇸", JP:"🇯🇵", CN:"🇨🇳", KR:"🇰🇷", EU:"🇪🇺",
  NL:"🇳🇱", DE:"🇩🇪", FR:"🇫🇷", AT:"🇦🇹", SG:"🇸🇬", IL:"🇮🇱", CH:"🇨🇭",
  UK:"🇬🇧", HK:"🇭🇰", DK:"🇩🇰", GLOBAL:"🌐" };

const SP_TOOLTIP = {
  header: "⚑ 客戶獨家／關鍵單點 — 4 種子情況之 union",
  buckets: [
    ["近乎獨佔", "全球市佔 >70%、無有效第二源（如 Disco、ABF 膜、家登 EUV pod）"],
    ["客戶獨家", "對 TSMC / NVDA 等關鍵客戶的某段製程唯一供應，全球市佔可能不大"],
    ["鎖喉點", "製程與客戶內製深度綁定，結構上難以替代（TSMC CoWoS、CoW）"],
    ["封裝級單點", "與主製程同步設計、被整進客戶平台（健策 lid、旭化成 PSPI）"],
  ],
  note: "與『競爭態勢』badge 正交 — 一個 oligopoly 節點也可能因客戶獨家而被標 ⚑",
};

let TOPIC = null;
let DD_LINKS = {};
let TOPICS_MANIFEST = [];
let activeFilter = null;
let singleFilter = false;
let activeNodeId = null;
let searchTerm = "";

/* ---------- tiny helpers ---------- */
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const compOf = n => COMP[n.competition] || COMP.emerging;
const colorOf = n => `var(${compOf(n).cssVar})`;
const flagOf = c => c.country && FLAG[c.country] ? FLAG[c.country] : "";
const parseShare = s => { if (!s) return null; const m = String(s).match(/(\d+(\.\d+)?)/); return m ? parseFloat(m[1]) : null; };
const maxShareIn = cos => { let mx = 0; cos.forEach(c => { const p = parseShare(c.share); if (p != null && p > mx) mx = p; }); return mx; };
const hostOf = u => { try { return new URL(u).hostname.replace(/^www\./,""); } catch(e) { return u; } };
const cssEsc = s => String(s).replace(/"/g,'\\"');
const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

function ddLinkFor(tickerStr) {
  if (!tickerStr) return null;
  const tokens = String(tickerStr).split(/[\s/,]+/).map(s => s.trim()).filter(Boolean);
  for (const t of tokens) {
    if (DD_LINKS[t]) return { ticker:t, href:DD_LINKS[t] };
  }
  return null;
}

/* ---------- tabs ---------- */
function renderTabs() {
  const wrap = document.getElementById("topicTabs");
  if (!wrap) return;
  wrap.innerHTML = "";
  TOPICS_MANIFEST.forEach(t => {
    const isActive = t.id === TOPIC.id;
    if (t.active) {
      const a = el("a", "topic-tab" + (isActive ? " active" : ""), t.tab);
      a.href = `${t.id}.html`;
      wrap.appendChild(a);
    } else {
      const btn = el("span", "topic-tab soon", `${t.tab}<span class="badge">即將推出</span>`);
      wrap.appendChild(btn);
    }
  });
}

/* ---------- header ---------- */
function renderHeader() {
  const t = document.getElementById("topicTitle");
  const s = document.getElementById("topicSub");
  if (t) t.innerHTML = `<span class="spark"></span>${TOPIC.title}`;
  if (s) s.textContent = TOPIC.subtitle || "";
  if (TOPIC.title && document.title.indexOf(TOPIC.title) === -1) {
    document.title = `${TOPIC.title} — InvestMQuest Research`;
  }
}

/* ---------- legend ---------- */
function renderLegend() {
  const wrap = document.getElementById("legend");
  if (!wrap) return;
  const used = new Set(TOPIC.nodes.map(n => n.competition).filter(Boolean));
  let html = `<span class="lg-title">競爭態勢</span>`;
  Object.keys(COMP).forEach(k => {
    if (!used.has(k)) return;
    const c = COMP[k];
    html += `<span class="lg" data-k="${k}"><span class="dot" style="background:var(${c.cssVar})"></span><span>${c.label}</span></span>`;
  });
  const tipBuckets = SP_TOOLTIP.buckets.map(b => `<dt>${b[0]}</dt><dd>${b[1]}</dd>`).join("");
  html += `<span class="lg-single" data-k="single">⚑ 客戶獨家／關鍵單點
    <span class="sp-tip">
      <h5>${SP_TOOLTIP.header}</h5>
      <dl>${tipBuckets}</dl>
      <div style="margin-top:7px;font-size:10.5px;color:#A5B4FC;line-height:1.5">${SP_TOOLTIP.note}</div>
    </span>
  </span>`;
  html += `<span class="lg-hint">點圖例篩選 · 點節點看上下游 · 滑鼠移上看連線</span>`;
  wrap.innerHTML = html;
  wrap.querySelectorAll(".lg").forEach(l => {
    l.onclick = () => {
      const k = l.dataset.k;
      activeFilter = activeFilter === k ? null : k;
      singleFilter = false;
      updateFilterChips();
      applyFilter();
    };
  });
  wrap.querySelector(".lg-single").onclick = (e) => {
    if (e.target.closest(".sp-tip")) return;
    singleFilter = !singleFilter;
    activeFilter = null;
    updateFilterChips();
    applyFilter();
  };
}
function updateFilterChips() {
  document.querySelectorAll(".lg").forEach(x => {
    x.classList.toggle("active", activeFilter === x.dataset.k);
    x.classList.toggle("dim", activeFilter && activeFilter !== x.dataset.k);
  });
  const s = document.querySelector(".lg-single");
  s.classList.toggle("active", singleFilter);
  s.classList.toggle("dim", activeFilter && !singleFilter);
}
function applyFilter() {
  document.querySelectorAll(".node").forEach(n => {
    const id = n.dataset.id;
    const node = TOPIC._map[id];
    if (!node) return;
    let hidden = false;
    if (activeFilter && node.competition !== activeFilter) hidden = true;
    if (singleFilter && !node.single) hidden = true;
    if (searchTerm) {
      const blob = (node.name + " " + (node.nameEn||"") + " " +
        (node.companies||[]).map(c => (c.name||"") + " " + (c.ticker||"")).join(" ")).toLowerCase();
      if (!blob.includes(searchTerm)) hidden = true;
    }
    n.classList.toggle("dim", hidden);
  });
}

/* ---------- stats ---------- */
function renderStats() {
  const wrap = document.getElementById("statsRow");
  if (!wrap) return;
  const stats = TOPIC.stats || [];
  wrap.innerHTML = stats.map((s,i) => {
    const cls = s.hot ? " hot" : (i === 0 ? "" : (i === 1 ? " green" : ""));
    return `<div class="stat-card${cls}">
      <div class="k">${s.k}</div>
      <div class="v">${s.v}${s.sub ? `<small>${s.sub}</small>` : ""}</div>
    </div>`;
  }).join("");
}

/* ---------- grid ---------- */
function renderGrid() {
  const grid = document.getElementById("grid");
  if (!grid) return;
  grid.innerHTML = "";
  const rows = TOPIC.rows || [];
  const maxCol = Math.max(1, ...TOPIC.nodes.map(n => (n.col||1) + ((n.span||1) - 1)));
  grid.style.gridTemplateColumns = `repeat(${maxCol}, minmax(165px, 1fr))`;

  rows.forEach((row, ri) => {
    const band = el("div", "band" + (row.main ? " main" : ""), `<span class="bdot"></span>${row.label}`);
    band.style.gridRow = `${ri * 2 + 1}`;
    band.style.gridColumn = "1 / -1";
    grid.appendChild(band);

    TOPIC.nodes.filter(n => n.row === row.id).forEach(n => {
      const card = buildNode(n);
      card.style.gridRow = `${ri * 2 + 2}`;
      card.style.gridColumn = `${n.col} / span ${n.span || 1}`;
      grid.appendChild(card);
    });
  });
}

function buildNode(n) {
  const cc = colorOf(n);
  const comp = compOf(n);
  const card = el("div", `node kind-${n.kind || "stage"}`);
  card.style.setProperty("--cc", cc);
  card.dataset.id = n.id;
  card.dataset.comp = n.competition || "";

  const cos = n.companies || [];
  const chips = cos.slice(0, 3).map(c => {
    const dd = ddLinkFor(c.ticker);
    const mark = dd ? `<span class="dd-mark" title="有對應 DD 報告">●</span>` : "";
    const firstName = (c.name||"").split(/[\s/]/)[0];
    const safeName = String(c.name||"").replace(/"/g,"");
    return `<span class="chip" title="${safeName}">${flagOf(c) ? flagOf(c) + " " : ""}${firstName}${mark}</span>`;
  }).join("");
  const more = cos.length > 3 ? `<span class="chip more">+${cos.length - 3}</span>` : "";
  const growth = n.growth ? `<span class="g">↑ ${n.growth}</span>` : "";
  const ms = n.marketSize ? `<span class="ms">${n.marketSize}</span>` : "";

  card.innerHTML = `
    ${n.single ? `<div class="n-single" title="${String(n.single).replace(/"/g,"&quot;")}">⚑</div>` : ""}
    <div class="n-top">
      <div>
        <div class="n-name">${n.name}</div>
        ${n.nameEn ? `<div class="n-en">${n.nameEn}</div>` : ""}
      </div>
      <span class="n-badge">${comp.label}</span>
    </div>
    <div class="n-companies">${chips}${more}</div>
    ${(growth || ms) ? `<div class="n-foot">${growth}${ms}</div>` : ""}
  `;
  card.onclick = () => openDrawer(n.id);
  card.onmouseenter = () => highlightPath(n.id, true);
  card.onmouseleave = () => { if (!activeNodeId) highlightPath(null, false); };
  return card;
}

/* ---------- edges ---------- */
function svgDefs() {
  return `<defs>
    <marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#94A3B8"></path></marker>
    <marker id="ahHot" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="var(--accent)"></path></marker>
  </defs>`;
}
function drawEdges() {
  const canvas = document.getElementById("mapCanvas");
  const svg = document.getElementById("edges");
  if (!canvas || !svg || !TOPIC.edges) return;
  const W = canvas.scrollWidth, H = canvas.scrollHeight;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("width", W);
  svg.setAttribute("height", H);
  svg.innerHTML = svgDefs();
  const base = canvas.getBoundingClientRect();

  TOPIC.edges.forEach(e => {
    const from = e[0] || e.from, to = e[1] || e.to;
    const a = document.querySelector(`.node[data-id="${cssEsc(from)}"]`);
    const b = document.querySelector(`.node[data-id="${cssEsc(to)}"]`);
    if (!a || !b) return;
    const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    const A = { x: ra.left - base.left + canvas.scrollLeft, y: ra.top - base.top + canvas.scrollTop, w: ra.width, h: ra.height };
    const B = { x: rb.left - base.left + canvas.scrollLeft, y: rb.top - base.top + canvas.scrollTop, w: rb.width, h: rb.height };
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", pathBetween(A, B));
    p.setAttribute("marker-end", "url(#ah)");
    p.dataset.from = from;
    p.dataset.to = to;
    svg.appendChild(p);
  });
  if (activeNodeId) highlightPath(activeNodeId, true);
}
function pathBetween(A, B) {
  const ca = { x: A.x + A.w/2, y: A.y + A.h/2 };
  const cb = { x: B.x + B.w/2, y: B.y + B.h/2 };
  const dx = cb.x - ca.x, dy = cb.y - ca.y;
  let x1,y1,x2,y2,c1x,c1y,c2x,c2y;

  // Cross-row (stacked): one box clearly above the other → vertical S-curve.
  const aAboveB = B.y >= A.y + A.h * 0.6;
  const bAboveA = A.y >= B.y + B.h * 0.6;
  if (aAboveB || bAboveA) {
    if (aAboveB) { x1 = ca.x; y1 = A.y + A.h; x2 = cb.x; y2 = B.y; }
    else         { x1 = ca.x; y1 = A.y;       x2 = cb.x; y2 = B.y + B.h; }
    const ddy = y2 - y1, sgn = ddy >= 0 ? 1 : -1;
    const off = Math.max(26, Math.abs(ddy) * 0.5);
    c1x = x1; c1y = y1 + sgn * off; c2x = x2; c2y = y2 - sgn * off;
    return `M${x1},${y1} C${c1x},${c1y} ${c2x},${c2y} ${x2},${y2}`;
  }

  // Same row, skipping over intermediate cards → bow up & over.
  if (Math.abs(dx) > A.w * 1.55) {
    const dir = dx >= 0 ? 1 : -1;
    x1 = ca.x; y1 = A.y; x2 = cb.x; y2 = B.y;
    const bow = 46 + Math.abs(dx) * 0.10;
    c1x = ca.x + dir * 20; c1y = y1 - bow;
    c2x = cb.x - dir * 20; c2y = y2 - bow;
    return `M${x1},${y1} C${c1x},${c1y} ${c2x},${c2y} ${x2},${y2}`;
  }

  // Same row, adjacent → exit bottom of A, dip into the row gap, enter bottom of B
  const dir = dx >= 0 ? 1 : -1;
  x1 = ca.x + dir * (A.w/2 - 14); y1 = A.y + A.h;
  x2 = cb.x - dir * (B.w/2 - 14); y2 = B.y + B.h;
  const drop = 18;
  c1x = x1; c1y = y1 + drop; c2x = x2; c2y = y2 + drop;
  return `M${x1},${y1} C${c1x},${c1y} ${c2x},${c2y} ${x2},${y2}`;
}

/* ---------- highlight ---------- */
function highlightPath(id, on) {
  const svg = document.getElementById("edges");
  if (!svg) return;
  const paths = svg.querySelectorAll("path");
  if (!on || !id) {
    paths.forEach(p => { p.classList.remove("hot","dim"); p.setAttribute("marker-end","url(#ah)"); });
    document.querySelectorAll(".node").forEach(n => n.classList.remove("active"));
    return;
  }
  paths.forEach(p => {
    const touch = p.dataset.from === id || p.dataset.to === id;
    p.classList.toggle("hot", touch);
    p.classList.toggle("dim", !touch);
    p.setAttribute("marker-end", touch ? "url(#ahHot)" : "url(#ah)");
  });
  document.querySelectorAll(".node").forEach(n => {
    n.classList.toggle("active", n.dataset.id === id);
  });
}

/* ---------- drawer ---------- */
function openDrawer(id) {
  const n = TOPIC._map[id];
  if (!n) return;
  activeNodeId = id;
  highlightPath(id, true);

  const cc = colorOf(n);
  const comp = compOf(n);
  const drawer = document.getElementById("drawer");
  drawer.style.setProperty("--cc", cc);
  drawer.querySelector(".dr-head").style.setProperty("--cc", cc);
  drawer.setAttribute("aria-hidden","false");

  document.getElementById("drBadgeText").textContent = `${comp.label} · ${comp.en}`;
  document.getElementById("drTitle").textContent = n.name;
  document.getElementById("drEn").textContent = n.nameEn || "";

  const body = document.getElementById("drBody");
  body.innerHTML = "";

  if (n.desc) body.appendChild(section("環節說明", `<div class="dr-desc">${n.desc}</div>`));

  const metrics = [];
  if (n.marketSize) metrics.push(["市場規模 / 地位", n.marketSize]);
  if (n.growth)     metrics.push(["年增率 / CAGR", n.growth]);
  if (metrics.length)
    body.appendChild(section("關鍵指標",
      `<div class="metrics">${metrics.map(m => `<div class="metric"><div class="k">${m[0]}</div><div class="v">${m[1]}</div></div>`).join("")}</div>`));

  if (n.analysis)
    body.appendChild(section(`競爭態勢分析 · ${comp.label}`,
      `<div class="dr-analysis">${n.analysis}</div>`));

  if (n.single)
    body.appendChild(section("關鍵單點 / 客戶獨家",
      `<div class="dr-single"><span class="ic">⚑</span><span>${n.single}</span></div>`));

  if (n.companies && n.companies.length) {
    const maxS = maxShareIn(n.companies);
    const rows = n.companies.map(c => {
      const pct = parseShare(c.share);
      const bar = pct != null && maxS ? `<div class="co-bar"><i style="width:${Math.max(6, (pct/maxS)*100)}%;background:${cc}"></i></div>` : "";
      const prod = c.products ? `<span class="co-prod">🔧 ${c.products}</span>` : "";
      const csrc = c.src ? ` <a href="${c.src}" target="_blank" rel="noopener" class="src-icon" title="來源">↗</a>` : "";
      const dd = ddLinkFor(c.ticker);
      const ddBtn = dd ? ` <a href="${dd.href}" class="dd-link" target="_blank" rel="noopener" title="開啟 DD 報告">DD ↗</a>` : "";
      const tickerHTML = c.ticker ? `<span class="tk">${c.ticker}</span>` : "";
      return `<tr>
        <td><span class="co-name"><span class="co-flag">${(FLAG[c.country] || "")}</span>${c.name}${tickerHTML}${ddBtn}</span></td>
        <td><span class="co-share">${c.share || "—"}</span>${bar}</td>
        <td><span class="co-note">${c.note || ""}${csrc}</span>${prod}</td>
      </tr>`;
    }).join("");
    body.appendChild(section(`主要廠商 (${n.companies.length})　<span style="font-weight:600;text-transform:none;letter-spacing:0;color:var(--ink-faint)">依國別標示 · <span style="color:${cc}">●</span> = 有對應 DD 報告</span>`,
      `<table class="co-table"><thead><tr><th>公司</th><th>市佔／地位</th><th>角色／產品</th></tr></thead><tbody>${rows}</tbody></table>`));
  }

  const up = (n.upstream || []).map(flowTag).join("");
  const down = (n.downstream || []).map(flowTag).join("");
  if (up || down) {
    let html = `<div class="flow-chips">`;
    if (up)   html += `<div class="flow-line"><span class="lbl">↑ 上游</span><span class="flow-tags">${up}</span></div>`;
    if (down) html += `<div class="flow-line"><span class="lbl">↓ 下游</span><span class="flow-tags">${down}</span></div>`;
    html += `</div>`;
    body.appendChild(section("上下游連結", html));
  }

  if (n.sources && n.sources.length) {
    const links = n.sources.map(s => {
      const url = s.url || s; const label = s.label || hostOf(url);
      return `<a class="src-link" href="${url}" target="_blank" rel="noopener"><span>🔗</span><span>${label}</span><span class="u">${hostOf(url)}</span></a>`;
    }).join("");
    body.appendChild(section("資料來源 Sources", `<div class="dr-sources">${links}</div>`));
  }

  document.getElementById("scrim").classList.add("show");
  drawer.classList.add("show");
}
function flowTag(item) {
  if (typeof item === "string") return `<span class="flow-tag">${item}</span>`;
  const target = TOPIC._map[item.id];
  if (target) return `<span class="flow-tag" data-jump="${item.id}">${item.label || target.name}</span>`;
  return `<span class="flow-tag">${item.label || item.id}</span>`;
}
function section(title, html) {
  const s = el("div", "dr-section", `<h4>${title}</h4>${html}`);
  setTimeout(() => s.querySelectorAll("[data-jump]").forEach(j => j.onclick = () => openDrawer(j.dataset.jump)), 0);
  return s;
}
function closeDrawer() {
  activeNodeId = null;
  document.getElementById("scrim").classList.remove("show");
  const dr = document.getElementById("drawer");
  dr.classList.remove("show");
  dr.setAttribute("aria-hidden","true");
  highlightPath(null, false);
}

/* ---------- definitions block (footer card) ---------- */
function renderDefinitions() {
  const slot = document.getElementById("defBlock");
  if (!slot) return;
  const colors = ["", "b", "c", "d"];  // matches .def-card.b/.c/.d in CSS
  const cards = SP_TOOLTIP.buckets.map((b, i) => `
    <div class="def-card ${colors[i] || ""}"><div class="k">${b[0]}</div><div class="v">${b[1]}</div></div>
  `).join("");
  slot.innerHTML = `
    <h3><span class="ico">⚑</span>客戶獨家 / 關鍵單點 — 定義</h3>
    <p class="lede">節點上的 <em>⚑</em> 旗標代表「投資視角的脆弱依賴點」 — <em>跟左上角「競爭態勢」badge 正交</em>，由作者依下列 4 種子情況之一手動標註：</p>
    <div class="def-grid">${cards}</div>
    <p style="margin-top:12px;font-size:11px;color:var(--ink-faint);line-height:1.55">
      ${SP_TOOLTIP.note}。圖例中的 ⚑ 籤可以滑鼠移上看快速定義、點擊則切換「只看單點」篩選。
    </p>
  `;
}

/* ---------- search ---------- */
function bindSearch() {
  const input = document.getElementById("sc-search-input");
  if (!input) return;
  let t;
  input.addEventListener("input", () => {
    clearTimeout(t);
    t = setTimeout(() => {
      searchTerm = input.value.trim().toLowerCase();
      applyFilter();
    }, 80);
  });
}

/* ---------- boot ---------- */
async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.json();
}
async function boot() {
  const topicId = document.body.dataset.topic;
  if (!topicId) {
    console.error("[supply-chain] missing <body data-topic=…>");
    return;
  }
  try {
    const [topic, ddLinks, manifest] = await Promise.all([
      fetchJSON(`data/${topicId}.json`),
      fetchJSON(`data/_dd_links.json`).catch(() => ({})),
      fetchJSON(`data/_topics.json`).catch(() => ({ topics: [{ id: topicId, tab: topicId, active: true }] })),
    ]);
    TOPIC = topic;
    DD_LINKS = ddLinks;
    TOPICS_MANIFEST = manifest.topics || [];

    TOPIC._map = {};
    TOPIC.nodes.forEach(n => TOPIC._map[n.id] = n);

    renderTabs();
    renderHeader();
    renderLegend();
    renderStats();
    renderGrid();
    renderDefinitions();
    bindSearch();
    const dc = document.getElementById("drClose"); if (dc) dc.onclick = closeDrawer;
    const sc = document.getElementById("scrim");   if (sc) sc.onclick = closeDrawer;
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeDrawer(); });
    window.addEventListener("resize", debounce(drawEdges, 120));
    requestAnimationFrame(() => requestAnimationFrame(drawEdges));

    // ?open=<node-id> deep-links a drawer
    const openId = new URLSearchParams(location.search).get("open");
    if (openId && TOPIC._map[openId]) setTimeout(() => openDrawer(openId), 200);
  } catch (e) {
    console.error("[supply-chain] boot failed:", e);
    const grid = document.getElementById("grid");
    if (grid) grid.innerHTML = `<div style="padding:40px;color:#B91C1C;font-size:14px">無法載入供應鏈資料：${e.message}</div>`;
  }
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
})();
