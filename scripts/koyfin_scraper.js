// koyfin_scraper.js
//
// Standalone extraction of .claude/skills/refresh-eps-screener-web/SKILL.md
// v2.0 Step 1 (grabAll/pass, header-driven), Step 1.5 (horizontal multi-segment
// scan), Step 2 (KROW canonical row build) and Step 4 (djb2 fingerprint) —
// same algorithm, same column order (F), same canonicalization, same sort,
// so fingerprints produced here are directly comparable to the manual
// javascript_tool runs (e.g. the 2026-09-18 largecap run: rows=160,
// bytes=66677, djb2=3646933340).
//
// Loaded into the page via Playwright's page.add_script_tag(path=...) (see
// scripts/koyfin_scrape.py), which defines window.__koyfinScrape. Playwright
// then calls page.evaluate("([opts]) => window.__koyfinScrape(opts)") and
// awaits the returned promise.
//
// Differences from the manual skill flow (both non-semantic, both explained
// inline below):
//   1. The manual flow fires the segment loop "fire and forget" and polls
//      window.__running/__passLog from separate javascript_tool calls because
//      Chrome throttles background-tab timers severely (see SKILL.md Step 1.5
//      gotcha). Playwright drives the page directly (no separate "background
//      tab" concept the same way), so __koyfinScrape awaits the whole scan in
//      one page.evaluate call instead — Python just needs a generous timeout.
//   2. grabAll() additionally records every ticker-column cell it sees (valid
//      or not fully-rendered) into window.__tickerColumn, independent of
//      whether a full row of cells was captured into window.__eps. This is
//      pure additive bookkeeping (does not change window.__eps, F, canon, or
//      djb2 in any way) that feeds the Step 3 reconciliation koyfin_scrape.py
//      does after each scrape (row count vs. grid ticker-column count).
//
// CSS class hashes (table__headerCell___*, table__row___*, table__dataCell___*,
// table__scrollContainer___*) rotate on Koyfin redeploys — this file uses the
// same prefix selectors ([class*="table__headerCell___"] etc.) the skill uses,
// which are immune to suffix rotation. If Koyfin changes the *middle* segment
// of these class names too (not just the hash suffix), headerCount will come
// back 0 and this file needs re-calibration against a fresh javascript_tool
// session — see the note file this task also produces.

window.__koyfinScrape = async function (opts) {
  opts = opts || {};
  const horizStep = opts.horizStep || 1500;      // px, per skill Step 1.5
  const vertStep = opts.vertStep || 340;          // px, per skill Step 1 (< ~630px viewport, overlap so no missed rows)
  const horizSleepMs = opts.horizSleepMs || 400;  // per skill __pass()
  const vertSleepMs = opts.vertSleepMs || 120;    // per skill __pass() (nominal; real Koyfin render latency varies)

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // Same globals the skill uses (window.__eps / window.__hdrs), so a
  // javascript_tool session inspecting a Playwright-driven page mid-run sees
  // the identical shape a manual run would.
  window.__eps = {};
  window.__hdrs = new Set();
  window.__tickerColumn = new Set();

  const sc = document.querySelector('[class*="table__scrollContainer___"]');
  if (!sc) {
    return { error: "NO_SCROLL_CONTAINER" };
  }
  window.__epsSC = sc;

  // 8 chars: 99SMART / TAKAFUL-length tickers, per skill.
  const TICK_RE = /^[•\s]*([A-Z0-9]{1,8}(?:\.[A-Z]{1,3})?)$/;

  function grabAll() {
    const heads = [...document.querySelectorAll('[class*="table__headerCell___"]')]
      .map((h) => h.innerText.replace(/\s+/g, " ").trim());
    heads.forEach((h) => h && window.__hdrs.add(h));
    const ti = heads.indexOf("Ticker");
    if (ti < 0) return -1;
    let n = 0;
    document.querySelectorAll('[class*="table__row___"]').forEach((row) => {
      const cells = [...row.querySelectorAll('[class*="table__dataCell___"]')]
        .map((c) => c.innerText.replace(/\s+/g, " ").trim());
      const rawTick = cells[ti];
      const m = (rawTick || "").match(TICK_RE);
      if (m) window.__tickerColumn.add(m[1]);   // reconciliation bookkeeping only
      if (cells.length < heads.length) return;
      if (!m) return;
      const rec = window.__eps[m[1]] || (window.__eps[m[1]] = {});
      heads.forEach((h, i) => {
        if (h && h !== "Ticker" && cells[i] !== undefined && cells[i] !== "") rec[h] = cells[i];
      });
      n++;
    });
    return n;
  }

  async function pass(left, step) {
    const H = sc.scrollHeight;
    sc.scrollLeft = left;
    sc.dispatchEvent(new Event("scroll", { bubbles: true }));
    await sleep(horizSleepMs);
    window.__curLeft = left;
    window.__y = 0;
    while (window.__y <= H + 400) {
      sc.scrollTop = window.__y;
      sc.dispatchEvent(new Event("scroll", { bubbles: true }));
      await sleep(vertSleepMs);
      grabAll();
      window.__y += step;
    }
  }

  // Segment calculation per skill Step 1.5: use actual clientWidth to correct
  // the last segment instead of a blind ceil(scrollWidth/1500)+1.
  const maxScroll = sc.scrollWidth - sc.clientWidth;
  const segs = [];
  for (let l = 0; l < maxScroll; l += horizStep) segs.push(l);
  segs.push(maxScroll);

  window.__running = true;
  window.__passLog = [];
  for (const L of segs) {
    await pass(L, vertStep);
    window.__passLog.push([L, Object.keys(window.__eps).length, window.__hdrs.size]);
  }
  window.__running = false;

  // Column order F = xlsx header contract table's "Koyfin 表頭" column, in
  // order (53 entries: the 56 non-Ticker contract rows minus the 3 build-
  // computed growth/CAGR columns [rows 5/6/7, never scraped from Koyfin]).
  // MUST be the exact rendered short table-header text (grabAll() uses this
  // as the object key) — NOT the longer Column-Selection-dialog description.
  // Verbatim from .claude/skills/refresh-eps-screener-web/SKILL.md Step 6
  // table, cross-checked against scripts/koyfin_xlsx_from_raw.py's build_row()
  // f[1]..f[53] index order.
  const F = [
    "EPS Norm - Est Avg (FY1E)",
    "EPS Norm - Est Avg (FY2E)",
    "EPS Norm - Est Avg (FY3E)",
    "ROIC (LTM)",
    "FCF Margin % (LTM)",
    "ROIC (5YAVG)",
    "EBIT Margin % (LTM)",
    "ROIC (3YAVG)",
    "Effective Tax Rate - (Ratio) (FY)",
    "Total Revenues (FY)",
    "Total Revenues (-3FY)",
    "EBIT (FY)",
    "EBIT (-3FY)",
    "Inv. Cap. (FY)",
    "Inv. Cap. (-3FY)",
    "Country",                              // QA/reconciliation only — not written to xlsx (f[16])
    "Total Revenues (-0FQYoYFQ)",
    "Total Revenues (-1FQYoYFQ)",
    "Total Revenues (-2FQYoYFQ)",
    "Total Revenues (-3FQYoYFQ)",
    "Gross Profit Margin % (LTM)",
    "Gross Profit Margin % (-1FY)",
    "Gross Profit Margin % (-2FY)",
    "Gross Profit Margin % (-3FY)",
    "Total Revenues (LTM)",
    "EBIT (LTM)",
    "Net Debt / EBITDA (LTM)",
    "Total Revenues (-0FYYoYFQ)",
    "EBIT (-0FYYoYFQ)",
    "Avg Diluted Shares Out (FY)",
    "Avg Diluted Shares Out (-3FY)",
    "Total Stock-Based Compensation (LTM)",
    "Capital Expenditure (LTM)",
    "FCF (LTM)",
    "Net Debt (LTM)",
    "Cash Conversion Cycle (Average Days) (LTM)",
    "P/E (NTM)",
    "P/E (5YAVGNTM)",
    "P/B (LTM)",
    "P/B (5YAVG)",
    "RSI",
    "Price Chg. % (6M)",
    "Repurchase of Common Stock (LTM)",
    "Price Target - High",
    "Price Target - Low",
    "Price Target",
    "Net Income Margin % (LTM)",
    "Est Rev CAGR (3Y)",
    "Est EPS CAGR (3Y)",
    "Below 52W High %, Adj",
    "Last Price",
    "Short Int. (%)",
    "Insider Tr Shrs Net 3M",
  ];

  // Step 2 / Step 4: sorted keys, canonical pipe-joined lines, djb2 over the
  // newline-joined canon string — identical algorithm to the skill's browser-
  // side fingerprint block.
  const keys = Object.keys(window.__eps).sort();
  const lines = keys.map((k) => {
    const rec = window.__eps[k];
    return [k, ...F.map((f) => rec[f] || "")].join("|");
  });
  const canon = lines.join("\n");
  let h = 5381;
  for (let i = 0; i < canon.length; i++) {
    h = ((h << 5) + h + canon.charCodeAt(i)) >>> 0;
  }

  const missingTickers = [...window.__tickerColumn].filter((t) => !window.__eps[t]).sort();

  return {
    rows: keys.length,
    bytes: canon.length,
    djb2: h,
    lines: lines,
    headerCount: window.__hdrs.size,
    tickerColumnCount: window.__tickerColumn.size,
    missingTickers: missingTickers,
    segments: segs,
  };
};
