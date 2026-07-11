/* dd-livebar.js — LIVE STALENESS BAR for DD reports
 * Self-contained, no external deps. Injected via <script src="/assets/dd-livebar.js" defer>.
 * Reads the page's own <script id="dd-meta"> JSON (ticker / date / price_at_dd / verdict),
 * fetches /dd-screener/latest.json for the current snapshot price (stock.ma.price) and
 * as-of date, then renders a slim non-sticky bar at the top of the report content.
 * Degrades gracefully (age-only) when the ticker is absent from the snapshot or the fetch fails.
 */
(function () {
  "use strict";
  if (window.__ddLivebarDone) return;
  window.__ddLivebarDone = true;

  var SNAPSHOT_URL = "/dd-screener/latest.json";

  // ---- 1. read this page's dd-meta ----
  function readMeta() {
    var el = document.getElementById("dd-meta");
    if (!el) return null;
    try {
      return JSON.parse(el.textContent || el.innerText || "");
    } catch (e) {
      return null;
    }
  }

  // ---- helpers ----
  function daysBetween(fromISO, to) {
    var d = new Date(fromISO + "T00:00:00");
    if (isNaN(d.getTime())) return null;
    var ms = to.getTime() - d.getTime();
    return Math.floor(ms / 86400000);
  }

  function fmtNum(n) {
    if (n == null || isNaN(n)) return "—";
    return Number(n).toLocaleString("en-US", { maximumFractionDigits: 2 });
  }

  function fmtPct(p) {
    if (p == null || isNaN(p)) return "";
    var s = p >= 0 ? "+" : "";
    return s + p.toFixed(1) + "%";
  }

  // verdict: prefer dca_verdict (裁決) for v13/v14, else legacy signal/verdict (訊號)
  function pickVerdict(meta) {
    if (meta.dca_verdict) return { label: "裁決", value: String(meta.dca_verdict).trim() };
    if (meta.signal) return { label: "訊號", value: String(meta.signal).trim() };
    if (meta.verdict) {
      var v = String(meta.verdict).trim();
      if (v.length > 24) v = v.slice(0, 24) + "…";
      return { label: "訊號", value: v };
    }
    return null;
  }

  // ---- 2. one-time style injection (奶油海軍藍×金) ----
  function injectStyle() {
    if (document.getElementById("dd-livebar-style")) return;
    var css =
      ".dd-livebar{font-family:'Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;" +
      "font-size:12.5px;line-height:1.5;color:#243b53;background:#FBF8F1;border:1px solid #E3D9C4;" +
      "border-left:3px solid #B8924A;border-radius:5px;padding:8px 12px;margin:0 0 16px;" +
      "display:flex;flex-wrap:wrap;align-items:center;gap:5px 8px;}" +
      ".dd-livebar .seg{display:inline-flex;align-items:baseline;gap:4px;white-space:nowrap;}" +
      ".dd-livebar .div{color:#C9BFA6;user-select:none;}" +
      ".dd-livebar .num{font-family:'IBM Plex Mono','SFMono-Regular',Menlo,monospace;font-weight:600;" +
      "font-variant-numeric:tabular-nums;letter-spacing:-.01em;}" +
      ".dd-livebar .lbl{color:#6b7a8d;}" +
      ".dd-livebar .up{color:#15803d;}" +
      ".dd-livebar .down{color:#b91c1c;}" +
      ".dd-livebar .verdict{font-weight:700;color:#1E3A5F;}" +
      ".dd-livebar .warn{font-weight:600;}" +
      ".dd-livebar.stale-amber{background:#FEF6E0;border-color:#F0D48A;border-left-color:#D9902B;}" +
      ".dd-livebar.stale-amber .warn{color:#9A6412;}" +
      ".dd-livebar.stale-red{background:#FCEDEA;border-color:#F0C2B7;border-left-color:#C0392B;}" +
      ".dd-livebar.stale-red .warn{color:#A93226;}" +
      "@media(max-width:640px){.dd-livebar{font-size:12px;}}";
    var s = document.createElement("style");
    s.id = "dd-livebar-style";
    s.textContent = css;
    document.head.appendChild(s);
  }

  // ---- element builders ----
  function seg() {
    var d = document.createElement("span");
    d.className = "seg";
    for (var i = 0; i < arguments.length; i++) {
      var a = arguments[i];
      if (typeof a === "string") d.appendChild(document.createTextNode(a));
      else if (a) d.appendChild(a);
    }
    return d;
  }
  function span(cls, txt) {
    var s = document.createElement("span");
    if (cls) s.className = cls;
    s.textContent = txt;
    return s;
  }
  function divider() {
    return span("div", "｜");
  }

  // ---- 3. render ----
  function render(meta, snap) {
    injectStyle();
    var now = new Date();
    var age = daysBetween(meta.date, now);

    var bar = document.createElement("div");
    bar.className = "dd-livebar";
    if (age != null && age > 180) bar.classList.add("stale-red");
    else if (age != null && age > 90) bar.classList.add("stale-amber");

    var parts = [];

    // publish + age
    if (age != null) {
      parts.push(seg("本報告發布於 ", span("num", meta.date), "（" + age + " 天前）"));
    } else {
      parts.push(seg("本報告發布於 ", span("num", String(meta.date || "—"))));
    }

    // price comparison (only when we have both baseline and current snapshot)
    var haveBase = meta.price_at_dd != null && !isNaN(meta.price_at_dd);
    var cur = snap && snap.price != null && !isNaN(snap.price) ? Number(snap.price) : null;
    if (haveBase && cur != null) {
      var base = Number(meta.price_at_dd);
      var pct = base ? ((cur - base) / base) * 100 : null;
      var dir = pct == null ? "" : pct >= 0 ? "up" : "down";
      parts.push(
        seg(
          "發布時股價 ",
          span("num", fmtNum(base)),
          " → 最新快照 ",
          span("num", fmtNum(cur)),
          "（",
          span("num " + dir, fmtPct(pct)),
          "）"
        )
      );
    }

    // verdict
    var v = pickVerdict(meta);
    if (v) {
      parts.push(seg(span("lbl", v.label + "："), span("verdict", v.value), "（以發布日為準）"));
    }

    // snapshot date (so reader knows comparison price isn't real-time)
    if (haveBase && cur != null && snap && snap.as_of) {
      parts.push(seg(span("lbl", "快照日期 "), span("num", snap.as_of)));
    }

    // stale warning
    if (age != null && age > 180) {
      parts.push(seg(span("warn", "內文數字已過時，僅供研究脈絡")));
    }

    // assemble with dividers
    for (var i = 0; i < parts.length; i++) {
      if (i) bar.appendChild(divider());
      bar.appendChild(parts[i]);
    }

    // insert at top of report content
    var host =
      document.querySelector(".wrap") ||
      document.querySelector(".container") ||
      document.querySelector("main") ||
      document.querySelector("article") ||
      document.body;
    host.insertBefore(bar, host.firstChild);
  }

  // ---- 4. boot ----
  function boot() {
    var meta = readMeta();
    if (!meta || !meta.date) return; // nothing to anchor on
    var ticker = meta.ticker ? String(meta.ticker).trim() : null;

    if (!ticker) {
      render(meta, null); // age-only
      return;
    }

    fetch(SNAPSHOT_URL, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("http " + r.status);
        return r.json();
      })
      .then(function (data) {
        var snap = null;
        var stocks = (data && data.stocks) || [];
        for (var i = 0; i < stocks.length; i++) {
          if (String(stocks[i].ticker).trim() === ticker) {
            var maObj = stocks[i].ma;
            var px = maObj && maObj.price != null ? maObj.price : null;
            snap = { price: px, as_of: data.as_of || null };
            break;
          }
        }
        render(meta, snap); // snap null => graceful age-only
      })
      .catch(function () {
        render(meta, null); // fetch failed => age-only
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
