/* imq-badge.js — 品質 × 時機 四格徽章 ＋ 品質×時機矩陣 共用元件
 * 設計稿：notes/site-internal/root/_quality_timing_matrix_design_20260908.md
 *
 * 定位（設計稿 §0）：純瀏覽器端把既有 JSON 接起來畫，不落新名單檔、不新增
 * build 腳本輸出。所有資料一律 fetch 既有端點：
 *   /engine/arena.json         擁有層分／席位／DD 裁決／ROIC／FCF（own_board 母體）
 *   /stages/data/lamp.json     全母體時機碼（今日）
 *   /stages/data/latest.json  轉強～領先四段的天數／來路／RS 等細節（S1–S4 才有）
 *   /stages/data/history.json 250 個交易日的每日階段字串（算 Δ／本週新進／命中率）
 *   /dd-screener/latest.json  DD 裁決（日更，優先於 arena 週更快照）＋財務數字備援
 *
 * 品質閘＝v2（scripts/engine/grp.py::quality_gate）：ROIC≥15% 且 FCF≥10%，
 * 或資本週期豁免（ROIC≥25% 且 FCF≥0）。core_seats／sat_seats／core_bench 三個
 * 席位陣列自帶算好的 grp.quality（優先直接讀）；own_board／dd-screener 只給
 * 原始 roic／fcf 數字，本檔在瀏覽器端用同一條公式重算（README 對照見設計稿 §2
 * 「若欄位不存在則用最接近的既有欄位」——own_board 沒有 grp.quality 子物件）。
 *
 * 四格徽章「同一檔在任何頁面長得一樣」（§3）：本檔自帶固定色盤（imq-badge.css
 * 的 --qtm-* token），不吃各主頁自己的設計系統變數。
 */
(function (global) {
  "use strict";
  var IMQ = global.IMQBadge = global.IMQBadge || {};

  // ── 常數 ──────────────────────────────────────────────────────────
  var Q_ROIC_MIN = 15, Q_FCF_MIN = 10, Q_ROIC_EXEMPT = 25;
  var STAGE_LABEL = { S0: "弱勢", S1: "轉強", S2: "築底", S3: "收縮完成", S4: "領先", S9: "過渡" };
  var STAGE_ROLE  = { S4: "pos", S3: "pos", S1: "accent", S2: "sec", S0: "neg", S9: "mut" };
  var STAGE_ORDER = ["S4", "S3", "S2", "S1", "S0"]; // 矩陣列序：領先／收縮完成／築底／轉強／弱勢
  var QCOLS = ["pass", "fail", "none"];
  var QCOL_LABEL = { pass: "品質過", fail: "品質未過", none: "無品質資料" };
  var DD_CLS = { "進場": "dd-in", "觀望": "dd-watch", "迴避": "dd-avoid" };
  var SEAT_LABEL = { C: "核心席", S: "衛星席", B: "板凳" };
  var URLS = {
    arena: "/engine/arena.json",
    lamp: "/stages/data/lamp.json",
    stages: "/stages/data/latest.json",
    history: "/stages/data/history.json",
    dd: "/dd-screener/latest.json"
  };

  // ── 小工具 ────────────────────────────────────────────────────────
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function fmt1(n) { return (n == null || isNaN(n)) ? "—" : (Math.round(n * 10) / 10).toFixed(1); }
  function getJSON(url) {
    return fetch(url, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).catch(function () { return null; });
  }

  // ── 品質閘（scripts/engine/grp.py::quality_gate 的瀏覽器端重算，見檔頭說明）─
  function qualityFromRoicFcf(roic, fcf) {
    if (roic == null && fcf == null) {
      return { pass: null, why: [], exempt: false, roic: null, fcf: null };
    }
    var base = (roic != null && roic >= Q_ROIC_MIN) && (fcf != null && fcf >= Q_FCF_MIN);
    var exempt = !base && (roic != null && roic >= Q_ROIC_EXEMPT) && (fcf != null && fcf >= 0);
    var why = [];
    if (!base && !exempt) {
      if (roic == null || roic < Q_ROIC_MIN) {
        why.push("ROIC " + (roic == null ? "缺" : (fmt1(roic) + "%，差 " + fmt1(Q_ROIC_MIN - roic) + " 個百分點")));
      }
      if (fcf == null || fcf < Q_FCF_MIN) {
        why.push("FCF " + (fcf == null ? "缺" : (fmt1(fcf) + "%，差 " + fmt1(Q_FCF_MIN - fcf) + " 個百分點")));
      }
    }
    return { pass: !!(base || exempt), why: why, exempt: exempt, roic: roic, fcf: fcf };
  }
  function qualityBucketKey(q) {
    if (!q || q.pass == null) return "none";
    return q.pass ? "pass" : "fail";
  }

  // ── 資料載入＋建索引（全站共用一份，記憶體快取一次）───────────────────
  var _dataPromise = null;
  function loadData() {
    if (_dataPromise) return _dataPromise;
    _dataPromise = Promise.all([
      getJSON(URLS.arena), getJSON(URLS.lamp), getJSON(URLS.stages),
      getJSON(URLS.history), getJSON(URLS.dd)
    ]).then(function (r) { return buildIndex(r[0], r[1], r[2], r[3], r[4]); });
    return _dataPromise;
  }

  function buildIndex(arena, lamp, stagesLatest, history, dd) {
    var idx = {
      ok: {
        arena: !!(arena && Array.isArray(arena.own_board)),
        lamp: !!(lamp && lamp.lamp),
        stages: !!(stagesLatest && Array.isArray(stagesLatest.rows)),
        history: !!(history && history.stages && history.dates),
        dd: !!(dd && Array.isArray(dd.stocks))
      },
      quality: {}, dd: {}, seat: {}, ownScore: {}, gMethod: {},
      timingCode: {}, timingDetail: {}, boardSet: {},
      historyDates: (history && history.dates) || [],
      historyStages: (history && history.stages) || {},
      lampAsOf: lamp && lamp.as_of,
      stagesAsOf: stagesLatest && stagesLatest.as_of,
      arenaAsOf: arena && arena.run_timestamp,
      ddAsOf: dd && dd.as_of
    };

    if (idx.ok.arena) {
      (arena.own_board || []).forEach(function (r) {
        if (!r || !r.ticker) return;
        idx.boardSet[r.ticker] = true;
        idx.quality[r.ticker] = qualityFromRoicFcf(r.roic, r.fcf);
        idx.quality[r.ticker].source = "own_board";
        if (r.score != null && !isNaN(r.score)) idx.ownScore[r.ticker] = r.score;
        if (r.g_method) idx.gMethod[r.ticker] = r.g_method;
        if (r.verdict || r.dd_path) idx.dd[r.ticker] = { verdict: r.verdict || null, dd_path: r.dd_path || null, source: "arena" };
      });
      function seatRow(list, tag) {
        (list || []).forEach(function (r) {
          if (!r || !r.ticker) return;
          idx.seat[r.ticker] = tag;
          var g = r.grp || {};
          if (g.quality) {
            idx.quality[r.ticker] = {
              pass: g.quality.pass, why: g.quality.why || [], exempt: !!g.quality.exempt,
              roic: g.quality.roic, fcf: g.quality.fcf, source: "grp"
            };
          } else if (!idx.quality[r.ticker]) {
            idx.quality[r.ticker] = qualityFromRoicFcf(r.roic, r.fcf);
            idx.quality[r.ticker].source = "own_board";
          }
          var ownScore = (g.own && g.own.score != null) ? g.own.score : (r.score != null ? r.score : null);
          if (ownScore != null) idx.ownScore[r.ticker] = ownScore;
          if (r.g_method) idx.gMethod[r.ticker] = r.g_method;
          if (r.verdict || r.dd_path) idx.dd[r.ticker] = { verdict: r.verdict || null, dd_path: r.dd_path || null, source: "arena" };
        });
      }
      seatRow(arena.core_seats, "C");
      seatRow(arena.sat_seats, "S");
      seatRow(arena.core_bench, "B");
    }

    if (idx.ok.dd) {
      dd.stocks.forEach(function (r) {
        if (!r || !r.ticker) return;
        // dd-screener 日更、比 arena 週更快照新鮮，DD 裁決優先用它
        idx.dd[r.ticker] = { verdict: r.dca_verdict || null, dd_path: r.dd_path || null, source: "dd-screener" };
        if (!idx.quality[r.ticker]) {
          idx.quality[r.ticker] = qualityFromRoicFcf(r.roic, r.fcf);
          idx.quality[r.ticker].source = "dd-screener";
        }
      });
    }

    if (idx.ok.lamp) {
      Object.keys(lamp.lamp).forEach(function (tk) { idx.timingCode[tk] = lamp.lamp[tk]; });
    }
    if (idx.ok.stages) {
      stagesLatest.rows.forEach(function (r) {
        if (!r || !r.ticker) return;
        idx.timingDetail[r.ticker] = r;
        if (!idx.timingCode[r.ticker]) idx.timingCode[r.ticker] = r.stage; // lamp 缺該檔時用 latest.json 補
      });
    }
    return idx;
  }

  // ── 時機／天數（S0／S9 latest.json 無逐檔明細，退回 history 字串自算連續天數）─
  function historyRunLength(idx, ticker) {
    var s = idx.historyStages[ticker];
    if (!s || !s.length) return null;
    var n = s.length, c = s.charAt(n - 1), k = 1;
    while (n - 1 - k >= 0 && s.charAt(n - 1 - k) === c) k++;
    return k;
  }
  function stageOf(idx, ticker) { return idx.timingCode[ticker] || "S9"; }
  function daysInStage(idx, ticker) {
    var code = stageOf(idx, ticker);
    var det = idx.timingDetail[ticker];
    if (det && det.stage === code && det.days_in_stage != null) return det.days_in_stage;
    return historyRunLength(idx, ticker);
  }
  function prevStageInfo(idx, ticker) {
    var det = idx.timingDetail[ticker];
    var code = stageOf(idx, ticker);
    if (det && det.stage === code && det.prev_stage) {
      return { label: STAGE_LABEL[det.prev_stage] || det.prev_stage, days: det.prev_stage_ended };
    }
    return null;
  }
  function ddInfo(idx, ticker) {
    var d = idx.dd[ticker];
    if (!d || !d.verdict) return { verdict: "無 DD", cls: "dd-none", path: d ? d.dd_path : null };
    return { verdict: d.verdict, cls: DD_CLS[d.verdict] || "dd-none", path: d.dd_path };
  }

  // ── 四格內容（品質／擁有層分／時機／DD）──────────────────────────────
  function qualityCellHTML(idx, ticker) {
    var q = idx.quality[ticker];
    if (!q || q.pass == null) return { cls: "q-mut", label: "無資料", sub: "還沒有財務資料可判，不是未過" };
    if (q.pass) return { cls: "q-pos", label: q.exempt ? "過（資本週期豁免）" : "過", sub: "" };
    return { cls: "q-neg", label: "未過", sub: (q.why && q.why[0]) || "" };
  }
  function timingCellHTML(idx, ticker) {
    var code = stageOf(idx, ticker);
    var label = STAGE_LABEL[code] || code;
    var role = STAGE_ROLE[code] || "mut";
    var d = daysInStage(idx, ticker);
    return { cls: "q-" + role, label: label + (d != null ? "·第 " + d + " 天" : ""), code: code };
  }
  function ddCellHTML(idx, ticker) {
    var info = ddInfo(idx, ticker);
    var cls = info.verdict === "進場" ? "q-pos" : (info.verdict === "觀望" ? "q-warn" : (info.verdict === "迴避" ? "q-neg" : "q-mut"));
    return { cls: cls, label: info.verdict, path: info.path };
  }

  // 名單頁小徽章只有一種尺寸：四格各一個色點＋2 字短標，肉眼可辨、不靠 hover；
  // 完整說明（差多少、來自哪段、第幾天）留給點擊後的彈出小卡（renderPopupBody）。
  var Q_SHORT = { pass: "過", fail: "未過", none: "缺" };
  var STAGE_SHORT = { S0: "弱勢", S1: "轉強", S2: "築底", S3: "收縮", S4: "領先", S9: "過渡" };
  var DD_SHORT = { "進場": "進場", "觀望": "觀望", "迴避": "迴避" };
  function renderStrip(idx, ticker) {
    var qb = qualityBucketKey(idx.quality[ticker]);
    var qCls = qb === "pass" ? "q-pos" : (qb === "fail" ? "q-neg" : "q-mut");
    var code = stageOf(idx, ticker);
    var tCls = "q-" + (STAGE_ROLE[code] || "mut");
    var own = idx.ownScore[ticker];
    var ownTxt = own == null ? "—" : fmt1(own);
    var d = ddInfo(idx, ticker);
    var dCls = d.verdict === "進場" ? "q-pos" : (d.verdict === "觀望" ? "q-warn" : (d.verdict === "迴避" ? "q-neg" : "q-mut"));
    return (
      '<span class="qtm-cell ' + qCls + '"><i class="qtm-dot"></i>' + esc(Q_SHORT[qb]) + "</span>" +
      '<span class="qtm-cell q-mut"><i class="qtm-dot"></i>' + esc(ownTxt) + "</span>" +
      '<span class="qtm-cell ' + tCls + '"><i class="qtm-dot"></i>' + esc(STAGE_SHORT[code] || code) + "</span>" +
      '<span class="qtm-cell ' + dCls + '"><i class="qtm-dot"></i>' + esc(DD_SHORT[d.verdict] || "無") + "</span>"
    );
  }

  // ── 彈出小卡（md 版：矩陣與名單頁徽章共用）───────────────────────────
  function popupRow(k, valueHtml, subHtml) {
    return '<div class="qtm-pop-row"><div class="qtm-pop-k">' + esc(k) + '</div>' +
      '<div class="qtm-pop-v">' + valueHtml + (subHtml ? ('<span class="qtm-pop-sub">' + subHtml + "</span>") : "") + "</div></div>";
  }
  function renderPopupBody(idx, ticker) {
    var qc = qualityCellHTML(idx, ticker);
    var own = idx.ownScore[ticker];
    var singleYear = idx.gMethod[ticker] === "FY1→FY2 單年";
    var t = timingCellHTML(idx, ticker);
    var prev = prevStageInfo(idx, ticker);
    var d = ddCellHTML(idx, ticker);
    var seat = idx.seat[ticker];
    var chip = function (c) { return '<span class="qtm-cell ' + c.cls + '" style="display:inline-flex"><i class="qtm-dot"></i>' + esc(c.label) + "</span>"; };
    var html = "";
    html += popupRow("品質", chip(qc), qc.sub ? esc(qc.sub) : "");
    html += popupRow(
      "擁有層分",
      own == null ? "—" : ("<b>" + fmt1(own) + "</b>" + (seat ? (" " + esc(SEAT_LABEL[seat])) : "")),
      singleYear ? "單年成長法" : ""
    );
    html += popupRow("時機", chip(t), prev ? ("來自" + esc(prev.label) + "，" + prev.days + " 天前") : "");
    html += popupRow("DD 裁決", chip(d), "");
    return html;
  }

  var _popEl = null;
  function ensurePop() {
    if (_popEl) return _popEl;
    _popEl = document.createElement("div");
    _popEl.className = "qtm-pop qtm-root";
    _popEl.innerHTML =
      '<div class="qtm-pop-head"><span class="qtm-pop-tk"></span>' +
      '<button type="button" class="qtm-pop-close" aria-label="關閉">×</button></div>' +
      '<div class="qtm-pop-body"></div><div class="qtm-pop-links"></div>';
    document.body.appendChild(_popEl);
    _popEl.querySelector(".qtm-pop-close").addEventListener("click", closePop);
    document.addEventListener("click", function (e) {
      if (_popEl.classList.contains("open") && !_popEl.contains(e.target) && !e.target.closest("[data-qtm-tk]")) closePop();
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closePop(); });
    return _popEl;
  }
  function closePop() { if (_popEl) _popEl.classList.remove("open"); }
  function positionPop(pop, anchorEl) {
    pop.style.transform = "";
    if (!anchorEl || typeof anchorEl.getBoundingClientRect !== "function") {
      pop.style.top = "20%"; pop.style.left = "50%"; pop.style.transform = "translateX(-50%)";
      return;
    }
    var r = anchorEl.getBoundingClientRect();
    var vw = document.documentElement.clientWidth || 1024, vh = document.documentElement.clientHeight || 768;
    var w = 280;
    var left = Math.min(Math.max(r.left, 8), Math.max(vw - w - 8, 8));
    var top = (r.bottom + 268 > vh) ? Math.max(r.top - 268, 8) : (r.bottom + 8);
    pop.style.left = left + "px";
    pop.style.top = top + "px";
  }
  function openPop(idx, ticker, anchorEl) {
    var pop = ensurePop();
    pop.querySelector(".qtm-pop-tk").textContent = ticker;
    pop.querySelector(".qtm-pop-body").innerHTML = renderPopupBody(idx, ticker);
    var dd = ddInfo(idx, ticker);
    var stageCode = stageOf(idx, ticker);
    var listPage = stageCode === "S1" ? "/rs-turn/" : "/stages/";
    var listLabel = stageCode === "S1" ? "看它在轉強觀察 →" : "看它在個股階段雷達 →";
    var linksEl = pop.querySelector(".qtm-pop-links");
    var links = "";
    if (dd.path) links += '<a href="' + esc(dd.path) + '">看 DD 報告 →</a>';
    links += '<a href="' + esc(listPage) + '">' + esc(listLabel) + "</a>";
    linksEl.innerHTML = links;
    pop.classList.add("open");
    positionPop(pop, anchorEl);
    // /t/{T}.html 存在才顯示——彈出時才做一次 HEAD 判斷，不預先對每個徽號探測
    var hubUrl = "/t/" + encodeURIComponent(ticker) + ".html";
    fetch(hubUrl, { method: "HEAD" }).then(function (r) {
      if (r.ok && pop.classList.contains("open") && pop.querySelector(".qtm-pop-tk").textContent === ticker) {
        var a = document.createElement("a");
        a.href = hubUrl; a.textContent = "看個股頁 →";
        linksEl.insertBefore(a, linksEl.firstChild);
      }
    }).catch(function () {});
  }

  // ── 徽章：頁面呼叫 IMQ.tag() 埋佔位，再呼叫 decorateAll() 統一填色/掛事件 ──
  // 只有一種尺寸（設計拍板：badge 不分 sm/md，點擊一律開同一張彈出小卡）。
  IMQ.tag = function (ticker) {
    if (!ticker) return "";
    return '<span class="qtm-badge-slot" data-qtm-tk="' + esc(ticker) + '"></span>';
  };
  IMQ.decorateAll = function (root) {
    root = root || document;
    return loadData().then(function (idx) {
      var els = root.querySelectorAll("[data-qtm-tk]:not([data-qtm-mtx])");
      Array.prototype.forEach.call(els, function (el) {
        var tk = el.getAttribute("data-qtm-tk");
        el.innerHTML = renderStrip(idx, tk);
        el.classList.add("qtm-badge", "qtm-root");
        if (el.tagName !== "BUTTON") { el.setAttribute("role", "button"); el.setAttribute("tabindex", "0"); }
        if (!el.__qtmWired) {
          el.__qtmWired = true;
          el.addEventListener("click", function (ev) { ev.stopPropagation(); openPop(idx, tk, el); });
          el.addEventListener("keydown", function (ev) {
            if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openPop(idx, tk, el); }
          });
        }
      });
      return idx;
    });
  };

  // ── 矩陣 ──────────────────────────────────────────────────────────
  function sortTickers(idx, list) {
    return list.slice().sort(function (a, b) {
      var sa = idx.ownScore[a], sb = idx.ownScore[b];
      if (sa == null && sb == null) return a < b ? -1 : (a > b ? 1 : 0);
      if (sa == null) return 1;
      if (sb == null) return -1;
      if (sb !== sa) return sb - sa;
      return a < b ? -1 : (a > b ? 1 : 0);
    });
  }
  function stage5DaysAgo(idx, ticker) {
    var s = idx.historyStages[ticker];
    if (!s || s.length < 6) return null;
    return "S" + s.charAt(s.length - 6);
  }
  // v2（同 scripts/build_stages.py::build_transitions_table）：不看「60 日內
  // 是否曾觸及」，改看第 60 日當天的 end_stage，以及期間（跳過 S9 過渡日）
  // 到過的最高 peak_stage——避免把「剛脫離深回檔、第 60 日前仍貼過一天 200
  // 日均線下」誤記成一次完整的跌回弱勢。
  var STAGE_DIGIT_RANK = { "0": 0, "1": 1, "2": 2, "3": 3, "4": 4 };
  function computeHitRates(idx) {
    var dates = idx.historyDates || [];
    var n = dates.length;
    var maxI = n - 1 - 60;
    var specs = [
      { code: "S1", qb: "pass", label: "品質過 × 轉強" },
      { code: "S0", qb: "pass", label: "品質過 × 弱勢" },
      { code: "S4", qb: "fail", label: "品質未過 × 領先" },
      { code: "S0", qb: "fail", label: "品質未過 × 弱勢" }
    ];
    if (maxI < 1) return specs.map(function (s) { return { label: s.label, n: 0, detail: "" }; });
    return specs.map(function (spec) {
      var ch = spec.code.replace("S", "");
      var count = 0, endS3S4 = 0, endS0 = 0, peakS3plus = 0;
      Object.keys(idx.historyStages).forEach(function (tk) {
        var s = idx.historyStages[tk];
        if (!s || s.length !== n) return;
        if (qualityBucketKey(idx.quality[tk]) !== spec.qb) return;
        for (var i = 1; i <= maxI; i++) {
          if (s.charAt(i) !== ch || s.charAt(i - 1) === ch) continue;
          count++;
          var endCh = s.charAt(i + 60);
          if (endCh === "3" || endCh === "4") endS3S4++;
          if (endCh === "0") endS0++;
          var peakRank = -1;
          for (var k = i + 1; k <= i + 60; k++) {
            var c = s.charAt(k);
            if (c === "9") continue;
            var r = STAGE_DIGIT_RANK[c];
            if (r !== undefined && r > peakRank) peakRank = r;
          }
          if (peakRank >= STAGE_DIGIT_RANK["3"]) peakS3plus++;
        }
      });
      var detail = "";
      if (count > 0) {
        detail = "第 60 日在收縮完成或領先 " + fmt1(endS3S4 / count * 100) +
          "%、期間曾到收縮完成以上 " + fmt1(peakS3plus / count * 100) +
          "%、第 60 日在弱勢 " + fmt1(endS0 / count * 100) + "%";
      }
      return { label: spec.label, n: count, detail: detail };
    });
  }

  var ROLE_MAP = {
    "S1|pass": { label: "最該看", role: "accent" },
    "S0|pass": { label: "持股警訊", role: "neg" },
    "S4|fail": { label: "研究隊列：動能有、基本面沒", role: "warn" },
    "S0|fail": { label: "略過", role: "mut", collapse: true }
  };

  function mountMatrix(targetOrId, opts) {
    opts = opts || {};
    var el = (typeof targetOrId === "string") ? document.getElementById(targetOrId) : targetOrId;
    if (!el) return;
    el.classList.add("qtm-root");
    el.innerHTML = '<div class="qtm-matrix"><div class="qtm-empty">載入中…</div></div>';
    var state = { universe: opts.universe === "all" ? "all" : "board", onlyDD: false, onlySeat: false, expandS9: false };
    var wired = false;

    function membersFor(idx) {
      var out = [];
      if (state.universe === "board") {
        if (!idx.ok.arena) return null;
        Object.keys(idx.boardSet).forEach(function (tk) { out.push(tk); });
      } else {
        if (!idx.ok.lamp) return null;
        Object.keys(idx.timingCode).forEach(function (tk) { out.push(tk); });
      }
      if (state.onlyDD) out = out.filter(function (tk) { var d = idx.dd[tk]; return d && d.verdict; });
      if (state.onlySeat) out = out.filter(function (tk) { return !!idx.seat[tk]; });
      return out;
    }
    function bucketize(members) {
      var buckets = {};
      STAGE_ORDER.concat(["S9"]).forEach(function (s) { buckets[s] = { pass: [], fail: [], none: [] }; });
      members.forEach(function (tk) {
        var code = stageOf(idxRef, tk);
        if (!buckets[code]) buckets[code] = { pass: [], fail: [], none: [] };
        buckets[code][qualityBucketKey(idxRef.quality[tk])].push(tk);
      });
      return buckets;
    }
    function bucketizePrevCounts(members) {
      var buckets = {};
      STAGE_ORDER.concat(["S9"]).forEach(function (s) { buckets[s] = { pass: 0, fail: 0, none: 0 }; });
      members.forEach(function (tk) {
        var code = stage5DaysAgo(idxRef, tk);
        if (!code) return;
        if (!buckets[code]) buckets[code] = { pass: 0, fail: 0, none: 0 };
        buckets[code][qualityBucketKey(idxRef.quality[tk])]++;
      });
      return buckets;
    }
    function tickerChipHTML(ticker) {
      var idx = idxRef;
      var d = ddInfo(idx, ticker);
      var seat = idx.seat[ticker];
      var days = daysInStage(idx, ticker);
      var isNew = days != null && days <= 5;
      var cls = "qtm-tk " + d.cls + (isNew ? " new-week" : "");
      var seatBadge = seat ? ('<span class="qtm-seat">' + esc(seat) + "</span>") : "";
      var titleTxt = ticker + "：DD " + d.verdict + (isNew ? "（本週新進此格）" : "");
      return '<span class="' + cls + '" data-qtm-tk="' + esc(ticker) + '" data-qtm-mtx="1" tabindex="0" role="button" title="' + esc(titleTxt) + '">' + esc(ticker) + seatBadge + "</span>";
    }
    function cellHTML(stageCode, qb, tickers, prevCount) {
      var roleKey = stageCode + "|" + qb;
      var role = ROLE_MAP[roleKey];
      var hasSeat = tickers.some(function (tk) { return !!idxRef.seat[tk]; });
      var cls = "qtm-cellbox" + (role ? (" role role-" + role.role) : "") + ((role && role.role === "neg" && hasSeat) ? " seat-warn" : "");
      var collapsedDefault = !!(role && role.collapse);
      var sorted = sortTickers(idxRef, tickers);
      var visible = sorted.slice(0, 8), rest = sorted.slice(8);
      var deltaHtml = "";
      if (prevCount != null) {
        var delta = tickers.length - prevCount;
        if (delta !== 0) deltaHtml = '<span class="qtm-cell-delta ' + (delta > 0 ? "up" : "down") + '">' + (delta > 0 ? "+" : "") + delta + "</span>";
      }
      var body;
      if (!tickers.length) {
        body = '<div style="color:var(--qtm-muted);font-size:.74rem;margin-top:.3rem">目前沒有名字</div>';
      } else {
        var tkListHtml = visible.map(tickerChipHTML).join("");
        var moreHtml = rest.length
          ? ('<button type="button" class="qtm-more" data-qtm-more>更多 ' + rest.length + '</button>' +
             '<span class="qtm-tk-list" data-qtm-rest hidden>' + rest.map(tickerChipHTML).join("") + "</span>")
          : "";
        body = '<span class="qtm-tk-list">' + tkListHtml + "</span>" + moreHtml;
      }
      var roleTag = role ? ('<span class="qtm-role-tag role-' + role.role + '">' + esc(role.label) + "</span><br>") : "";
      var toggleBtn = collapsedDefault ? '<button type="button" class="qtm-toggle-collapse" data-qtm-toggle>展開名單</button>' : "";
      return '<div class="' + cls + (collapsedDefault ? " qtm-collapsed" : "") + '" data-qtm-colname="' + esc(QCOL_LABEL[qb]) + '">' +
        roleTag +
        '<span class="qtm-cell-count">' + tickers.length + "</span>" + deltaHtml + " " + toggleBtn +
        body +
        "</div>";
    }
    function controlsHTML() {
      return '<div class="qtm-controls">' +
        '<button type="button" class="qtm-chip' + (state.universe === "board" ? " on" : "") + '" data-qtm-chip="uni-board">陣容母體</button>' +
        '<button type="button" class="qtm-chip' + (state.universe === "all" ? " on" : "") + '" data-qtm-chip="uni-all">全市場</button>' +
        '<button type="button" class="qtm-chip' + (state.onlyDD ? " on" : "") + '" data-qtm-chip="only-dd">只看有 DD</button>' +
        '<button type="button" class="qtm-chip' + (state.onlySeat ? " on" : "") + '" data-qtm-chip="only-seat">只看席位與候補</button>' +
        "</div>";
    }
    function renderHitRate() {
      var idx = idxRef;
      if (!idx.ok.history) {
        return '<div class="qtm-hitrate"><h4>命中率</h4><div class="qtm-empty">資料尚未產出（階段歷史 /stages/data/history.json 缺檔）</div></div>';
      }
      var rates = computeHitRates(idx);
      var rowsHtml = rates.map(function (r) {
        var lowTag = r.n < 20 ? ' <span class="qtm-hit-lowsample">（樣本不足）</span>' : "";
        return '<div class="qtm-hit-row"><b>' + esc(r.label) + "</b>：過去 250 個交易日進入此格 n＝" + r.n + lowTag +
          (r.n > 0 ? "，" + esc(r.detail) : "") + "</div>";
      }).join("");
      return '<div class="qtm-hitrate"><h4>命中率</h4>' + rowsHtml +
        '<p class="qtm-foot">過去 250 個交易日回算，品質以今日判定回推；描述現況，不預測。</p></div>';
    }

    var idxRef = null;
    function render(idx) {
      idxRef = idx;
      var members = membersFor(idx);
      var gridSection, s9Toggle = "", asOfNote = "";
      if (members === null) {
        var missing = state.universe === "board" ? "陣容資料 /engine/arena.json" : "個股階段雷達 /stages/data/lamp.json";
        gridSection = '<div class="qtm-empty">資料尚未產出（' + esc(missing) + "）</div>";
      } else if (!members.length) {
        gridSection = '<div class="qtm-empty">目前沒有符合篩選的名字</div>';
      } else {
        var buckets = bucketize(members);
        var bucketsPrev = idx.ok.history ? bucketizePrevCounts(members) : null;
        var rows = STAGE_ORDER.slice();
        if (state.expandS9) rows.push("S9");
        var gridHtml = '<div class="qtm-gh"></div>' +
          '<div class="qtm-gh">品質過<small>ROIC≥15% 且 FCF≥10%（或資本週期豁免）</small></div>' +
          '<div class="qtm-gh">品質未過</div>' +
          '<div class="qtm-gh">無品質資料<small>還沒有財務資料可判，不是未過</small></div>';
        rows.forEach(function (stageCode) {
          gridHtml += '<div class="qtm-row-label">' + esc(STAGE_LABEL[stageCode]) + "</div>";
          QCOLS.forEach(function (qb) {
            var tickers = buckets[stageCode][qb];
            var prevCount = bucketsPrev ? bucketsPrev[stageCode][qb] : null;
            gridHtml += cellHTML(stageCode, qb, tickers, prevCount);
          });
        });
        if (!state.expandS9) {
          var s9n = buckets.S9 ? (buckets.S9.pass.length + buckets.S9.fail.length + buckets.S9.none.length) : 0;
          s9Toggle = '<div style="margin-top:.6rem"><button type="button" class="qtm-chip" data-qtm-chip="s9">顯示過渡列（' + s9n + '）</button></div>';
        }
        var uniLabel = state.universe === "board"
          ? ("資料來源：擁有層引擎" + (idx.arenaAsOf ? ("（" + String(idx.arenaAsOf).slice(0, 10) + "）") : ""))
          : ("資料來源：個股階段雷達（" + (idx.lampAsOf || "—") + "）");
        asOfNote = '<p style="font-size:.68rem;color:var(--qtm-muted);margin:.5rem 0 0">母體 ' + members.length + " 檔 · " + esc(uniLabel) + "</p>";
        gridSection = '<div class="qtm-scroll"><div class="qtm-grid">' + gridHtml + "</div></div>" + s9Toggle + asOfNote;
      }
      el.innerHTML =
        '<div class="qtm-matrix">' +
        "<h3>品質 × 時機</h3>" +
        '<p class="qtm-lede">橫看基本面過不過閘，直看現在走到生命週期哪一段。多層都亮的格子是觀察池，只亮一邊的格子是研究隊列，兩邊都不亮的略過。它只回答「看誰」。</p>' +
        controlsHTML() +
        gridSection +
        renderHitRate() +
        "</div>";
      if (!wired) {
        wired = true;
        el.addEventListener("click", function (ev) {
          var chip = ev.target.closest("[data-qtm-chip]");
          if (chip) {
            var k = chip.getAttribute("data-qtm-chip");
            if (k === "uni-board") state.universe = "board";
            else if (k === "uni-all") state.universe = "all";
            else if (k === "only-dd") state.onlyDD = !state.onlyDD;
            else if (k === "only-seat") state.onlySeat = !state.onlySeat;
            else if (k === "s9") state.expandS9 = true;
            render(idxRef);
            return;
          }
          var more = ev.target.closest("[data-qtm-more]");
          if (more) {
            more.style.display = "none";
            var rest = more.nextElementSibling;
            if (rest) rest.hidden = false;
            return;
          }
          var toggle = ev.target.closest("[data-qtm-toggle]");
          if (toggle) {
            var box = toggle.closest(".qtm-cellbox");
            if (box) box.classList.remove("qtm-collapsed");
            return;
          }
          var tk = ev.target.closest("[data-qtm-tk]");
          if (tk) { ev.stopPropagation(); openPop(idxRef, tk.getAttribute("data-qtm-tk"), tk); }
        });
      }
    }

    loadData().then(render);
  }
  IMQ.mountMatrix = mountMatrix;
  IMQ.loadData = loadData;
})(window);
