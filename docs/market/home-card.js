/* home-card.js — 市況主控台卡片（首頁與 /market/ 共用）
 * 資料：state.json 的 home_card（schema market-home-card-v1），由 scripts/build_market_state.py 產生。
 * 本檔只負責呈現，不算數字。對外介面 window.MarketHomeCard：
 *   isValid(card)                      是否為可渲染的 home_card
 *   renderHeadline(card)               ① 一句結論＋一行日期（renderDates 只出日期那一行）
 *   renderGroups(card)                 ② 依主張分組的證據
 *   renderMomentum(card)               ③ 資產動能 2×2
 *   renderGauges(card, opts)           ④ 儀表：「現在」「接下來一個月」
 *   renderAll(card, opts)              ①～④ 全部
 *   bind(container)                    儀表卡點擊導頁（卡片可能包在 <a> 內，所以用 data-href）
 * opts.spark：儀表卡內放 sparkline 掛載點（首頁用）；opts.detail：顯示儀表的補充說明（/market/ 用）。
 */
(function (global) {
  "use strict";

  var CSS = [
    ".hc{--hc-text:var(--text,#0c1521);--hc-sec:var(--text-sec,var(--text-secondary,#2a3a52));--hc-muted:var(--muted,var(--text-muted,#717a8a));",
    "--hc-soft:var(--bg-soft,var(--bg-card2,#fbf8f1));--hc-line:var(--border-soft,var(--border-light,#efe9da));--hc-accent:var(--accent,#0d2244);color:var(--hc-text)}",
    ".hc *{min-width:0}",
    ".hc-head{margin:0 0 .65rem}",
    ".hc-headline{font-size:.95rem;font-weight:600;line-height:1.6;margin:0;max-width:60ch;color:var(--hc-text)}",
    ".hc-dates{font-family:'IBM Plex Mono',monospace;font-size:.66rem;color:var(--hc-muted);margin-top:.2rem}",
    ".hc-dates b{font-weight:600;color:var(--hc-sec)}",
    ".hc-groups{display:grid;grid-template-columns:minmax(0,1fr);gap:.6rem 1.6rem;margin:0 0 .85rem}",
    "@media(min-width:900px){.hc-groups{grid-template-columns:repeat(2,minmax(0,1fr))}}",
    ".hc-group{padding-top:.5rem;border-top:1px solid var(--hc-line)}",
    ".hc-claim{font-size:.82rem;font-weight:600;line-height:1.55;margin:0 0 .25rem;color:var(--hc-text)}",
    ".hc-line{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 .45rem;font-size:.74rem;line-height:1.65;color:var(--hc-sec)}",
    ".hc-line .l{font-weight:500}",
    ".hc-line .v{font-family:'IBM Plex Mono',monospace;font-size:.74rem;font-weight:700;color:var(--hc-text)}",
    ".hc-line .p{color:var(--hc-muted);font-size:.7rem}",
    ".hc-line .r{color:var(--hc-muted);font-size:.7rem}",
    ".hc-line .h{flex-basis:100%;color:var(--hc-muted);font-size:.68rem;line-height:1.5}",
    ".hc-sec-h{font-size:.72rem;font-weight:700;color:var(--hc-sec);margin:0 0 .4rem;display:flex;flex-wrap:wrap;gap:.2rem .6rem;align-items:baseline}",
    ".hc-sec-h small{font-family:'IBM Plex Mono',monospace;font-size:.64rem;font-weight:500;color:var(--hc-muted)}",
    ".hc-mom{margin:0 0 .85rem}",
    ".hc-mom-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.5rem}",
    "@media(max-width:639px){.hc-mom-grid{grid-template-columns:minmax(0,1fr)}}",
    ".hc-cell{background:var(--hc-soft);border-radius:8px;padding:.45rem .6rem .5rem}",
    ".hc-cell-t{font-size:.7rem;font-weight:700;color:var(--hc-sec);margin-bottom:.3rem}",
    ".hc-chips{display:flex;flex-wrap:wrap;gap:.3rem}",
    ".hc-chip{display:inline-flex;align-items:baseline;gap:.25rem;font-size:.72rem;line-height:1.5;color:var(--hc-text);",
    "background:var(--card,var(--bg-card,#fff));border:1px solid var(--hc-line);border-radius:999px;padding:.08rem .5rem}",
    ".hc-chip i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:.62rem;color:var(--hc-muted)}",
    ".hc-tag{font-style:normal;font-size:.6rem;font-weight:600;line-height:1.4;padding:0 .3rem;border-radius:4px;border:1px solid var(--hc-accent)}",
    ".hc-tag.on{background:var(--hc-accent);color:#fff}",
    ".hc-tag.near{background:transparent;color:var(--hc-accent)}",
    ".hc-none{font-size:.7rem;color:var(--hc-muted)}",
    ".hc-mom-note{font-size:.68rem;color:var(--hc-muted);line-height:1.55;margin-top:.4rem}",
    ".hc-gauges{display:grid;grid-template-columns:minmax(0,1fr);gap:.7rem 1.6rem}",
    "@media(min-width:900px){.hc-gauges{grid-template-columns:minmax(0,3fr) minmax(0,2fr)}}",
    ".hc-gset-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,9.5rem),1fr));gap:.5rem}",
    ".hc-gauge{background:var(--hc-soft);border-radius:8px;padding:.45rem .6rem .5rem;display:flex;flex-direction:column;gap:.1rem}",
    ".hc-gauge[data-href]{cursor:pointer}.hc-gauge[data-href]:hover{filter:brightness(.97)}",
    ".hc-g-name{font-size:.68rem;color:var(--hc-muted)}",
    ".hc-g-val{font-size:.8rem;font-weight:700;color:var(--hc-text);line-height:1.45}",
    ".hc-g-val b{font-family:'IBM Plex Mono',monospace;font-size:.92rem;font-weight:700}",
    ".hc-g-val span{font-weight:600;font-size:.74rem;color:var(--hc-sec)}",
    ".hc-g-note{font-size:.66rem;line-height:1.5;color:var(--hc-muted)}",
    ".hc-g-detail{font-size:.66rem;line-height:1.5;color:var(--hc-sec)}",
    ".hc-spark{display:block;width:100%;line-height:0;margin-top:.2rem}.hc-spark svg{display:block;width:100%;height:26px}",
    ".hc-old{font-size:.68rem;color:var(--hc-muted);margin-left:.4rem;font-weight:400}"
  ].join("");

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function md(d) {
    var m = /^\d{4}-(\d{2})-(\d{2})/.exec(String(d || ""));
    return m ? m[1] + "-" + m[2] : "";
  }
  function injectCss() {
    if (document.getElementById("hc-style")) return;
    var s = document.createElement("style");
    s.id = "hc-style";
    s.textContent = CSS;
    document.head.appendChild(s);
  }
  function isValid(card) {
    return !!(card && card.schema === "market-home-card-v1" && card.headline);
  }

  function renderDates(card) {
    var dates = [];
    if (card.data_as_of) dates.push("資料 " + md(card.data_as_of));
    if (card.read_as_of && card.read_as_of !== card.data_as_of && !card.read_expired) dates.push("判讀 " + md(card.read_as_of));
    return '<div class="hc-dates">' + esc(dates.join(" · ")) +
      (card.read_expired ? (dates.length ? " · " : "") + "判讀已過期，顯示機械摘要" : "") + "</div>";
  }
  function renderHeadline(card) {
    return '<div class="hc-head"><p class="hc-headline">' + esc(card.headline) + "</p>" + renderDates(card) + "</div>";
  }

  function renderLine(l) {
    var h = '<div class="hc-line"' + (l.hint ? ' title="' + esc(l.hint) + '"' : "") + ">" +
      '<span class="l">' + esc(l.label) + "</span>" +
      '<span class="v">' + esc(l.value_text) + "</span>";
    if (l.read_value_text && l.read_value_text !== l.value_text) {
      h += '<span class="r">（判讀時 ' + esc(l.read_value_text) + "）</span>";
    }
    if (l.position_text) h += '<span class="p">' + esc(l.position_text) + "</span>";
    return h + "</div>";
  }
  function renderGroups(card) {
    var groups = card.groups || [];
    if (!groups.length) return "";
    return '<div class="hc-groups">' + groups.map(function (g) {
      return '<div class="hc-group"><p class="hc-claim">' + esc(g.claim) + "</p>" +
        (g.lines || []).map(renderLine).join("") + "</div>";
    }).join("") + "</div>";
  }

  function renderChip(it) {
    var title = [];
    if (it.change && it.change.text) title.push(it.change.text);
    if (it.streak_days != null) title.push("在這格 " + it.streak_days + " 個交易日" + (it.streak_capped ? "以上" : ""));
    var tag = "";
    if (it.change) {
      tag = it.change.status === "confirmed" ? '<em class="hc-tag on">已確認</em>' : '<em class="hc-tag near">未站穩</em>';
    }
    return '<span class="hc-chip" title="' + esc(title.join("；")) + '">' + esc(it.label) +
      (it.ticker ? " <i>" + esc(it.ticker) + "</i>" : "") + tag + "</span>";
  }
  function renderMomentum(card) {
    var m = card.momentum;
    if (!m || !m.cells) return "";
    var order = ["strong_up", "strong_down", "weak_up", "weak_down"];
    var stale = m.as_of && card.data_as_of && m.as_of < card.data_as_of;
    var head = '<div class="hc-sec-h">資產動能' + (stale ? "<small>動能到 " + esc(md(m.as_of)) + "</small>" : "") + "</div>";
    var cells = order.map(function (k) {
      var c = m.cells[k];
      if (!c) return "";
      var items = c.items || [];
      return '<div class="hc-cell" data-cell="' + k + '"><div class="hc-cell-t">' + esc(c.title) + "</div>" +
        (items.length ? '<div class="hc-chips">' + items.map(renderChip).join("") + "</div>" : '<span class="hc-none">—</span>') + "</div>";
    }).join("");
    return '<div class="hc-mom">' + head + '<div class="hc-mom-grid">' + cells + "</div>" +
      (m.note ? '<div class="hc-mom-note">' + esc(m.note) + "</div>" : "") + "</div>";
  }

  function renderGauge(g, opts) {
    var href = g.href ? (g.href.charAt(0) === "#" ? "/" + g.href : g.href) : "";
    return '<div class="hc-gauge" data-key="' + esc(g.key) + '"' + (href ? ' data-href="' + esc(href) + '"' : "") + ">" +
      '<div class="hc-g-name">' + esc(g.name) + "</div>" +
      '<div class="hc-g-val"><b>' + esc(g.value_text) + "</b>" + (g.label ? " <span>" + esc(g.label) + "</span>" : "") + "</div>" +
      (opts.spark && /^(stress|alert|risk_gauge)$/.test(g.key) ? '<span class="hc-spark" data-spark="' + esc(g.key) + '"></span>' : "") +
      (g.note ? '<div class="hc-g-note">' + esc(g.note) + "</div>" : "") +
      (g.detail && opts.detail ? '<div class="hc-g-detail">' + esc(g.detail) + "</div>" : "") +
      "</div>";
  }
  function renderGauges(card, opts) {
    opts = opts || {};
    var g = card.gauges;
    if (!g) return "";
    function set(title, list) {
      if (!list || !list.length) return "";
      return "<div><div class=\"hc-sec-h\">" + esc(title) + '</div><div class="hc-gset-cards">' +
        list.map(function (x) { return renderGauge(x, opts); }).join("") + "</div></div>";
    }
    var inner = set("現在", g.now) + set("接下來一個月", g.next_month);
    return inner ? '<div class="hc-gauges">' + inner + "</div>" : "";
  }

  function renderAll(card, opts) {
    injectCss();
    return '<div class="hc">' + renderHeadline(card) + renderGroups(card) + renderMomentum(card) + renderGauges(card, opts) + "</div>";
  }

  function bind(container) {
    if (!container || container.__hcBound) return;
    container.__hcBound = true;
    container.addEventListener("click", function (ev) {
      var c = ev.target.closest && ev.target.closest(".hc-gauge[data-href]");
      if (!c || !container.contains(c)) return;
      ev.preventDefault();
      ev.stopPropagation();
      var h = c.getAttribute("data-href");
      if (h.indexOf("/#") === 0 && location.pathname === "/") {
        var t = document.querySelector(h.slice(1));
        if (t) { t.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
      }
      location.href = h;
    });
  }

  injectCss();
  global.MarketHomeCard = {
    isValid: isValid, renderDates: renderDates, renderHeadline: renderHeadline, renderGroups: renderGroups,
    renderMomentum: renderMomentum, renderGauges: renderGauges, renderAll: renderAll, bind: bind
  };
})(window);
