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
  var STAGE_LABEL = { S0: "弱勢", S1: "轉強", S2: "築底", S5: "高檔整理", S3: "收縮完成", S4: "領先", S9: "過渡" };
  // S5 高檔整理（2026-09-09 owner decision）介於 S2 築底與 S3 收縮完成之間，色階
  // 也介於 sec（S2）與 pos（S3/S4）之間，故給它自己的 accent-muted token
  // （imq-badge.css 的 --qtm-accent-muted，與 --qtm-sec／--qtm-pos 同色階邏輯）。
  var STAGE_ROLE  = { S4: "pos", S3: "pos", S5: "accent-muted", S1: "accent", S2: "sec", S0: "neg", S9: "mut" };
  var STAGE_ORDER = ["S4", "S3", "S5", "S2", "S1", "S0"]; // 矩陣列序：領先／收縮完成／高檔整理／築底／轉強／弱勢
  var QCOLS = ["pass", "fail", "none"];
  var QCOL_LABEL = { pass: "品質過", fail: "品質未過", none: "無品質資料" };
  var DD_CLS = { "進場": "dd-in", "觀望": "dd-watch", "迴避": "dd-avoid" };
  var SEAT_LABEL = { C: "核心席", S: "衛星席", B: "板凳" };
  var URLS = {
    arena: "/engine/arena.json",
    lamp: "/stages/data/lamp.json",
    stages: "/stages/data/latest.json",
    history: "/stages/data/history.json",
    dd: "/dd-screener/latest.json",
    universe: "/engine/universe_board.json"
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
      getJSON(URLS.history), getJSON(URLS.dd), getJSON(URLS.universe)
    ]).then(function (r) { return buildIndex(r[0], r[1], r[2], r[3], r[4], r[5]); });
    return _dataPromise;
  }

  function buildIndex(arena, lamp, stagesLatest, history, dd, universeBoard) {
    var idx = {
      ok: {
        arena: !!(arena && Array.isArray(arena.own_board)),
        lamp: !!(lamp && lamp.lamp),
        stages: !!(stagesLatest && Array.isArray(stagesLatest.rows)),
        history: !!(history && history.stages && history.dates),
        dd: !!(dd && Array.isArray(dd.stocks)),
        universe: !!(universeBoard && Array.isArray(universeBoard.rows))
      },
      quality: {}, dd: {}, seat: {}, ownScore: {}, gMethod: {},
      timingCode: {}, timingDetail: {}, boardSet: {}, researchSet: {},
      historyDates: (history && history.dates) || [],
      historyStages: (history && history.stages) || {},
      historyDeep: (history && history.deep) || {},
      lampAsOf: lamp && lamp.as_of,
      stagesAsOf: stagesLatest && stagesLatest.as_of,
      arenaAsOf: arena && arena.run_timestamp,
      ddAsOf: dd && dd.as_of,
      universeAsOf: universeBoard && universeBoard.as_of,
      universeN: universeBoard && universeBoard.n,
      // 三態母體切換鈕上要顯示的即時檔數（設計拍板：labels with live counts）——
      // 席位榜讀 own_board 列數、研究母體讀 universe_board 列數、全市場讀
      // lamp.json 檔數，資料缺檔時維持 null（controlsHTML 顯示「—」）。
      boardN: (arena && Array.isArray(arena.own_board)) ? arena.own_board.length : null,
      researchN: (universeBoard && Array.isArray(universeBoard.rows)) ? universeBoard.rows.length : null,
      allN: (lamp && lamp.lamp) ? Object.keys(lamp.lamp).length : null
    };

    if (idx.ok.arena) {
      (arena.own_board || []).forEach(function (r) {
        if (!r || !r.ticker) return;
        idx.boardSet[r.ticker] = true;
        idx.quality[r.ticker] = qualityFromRoicFcf(r.roic, r.fcf);
        idx.quality[r.ticker].source = "own_board";
        if (r.score != null && !isNaN(r.score)) idx.ownScore[r.ticker] = r.score;
        if (r.g_method) idx.gMethod[r.ticker] = r.g_method;
        if (r.verdict || r.dd_path) idx.dd[r.ticker] = { verdict: r.verdict || null, dd_path: r.dd_path || null, dd_tag: r.dd_tag || null, source: "arena" };
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
          if (r.verdict || r.dd_path) idx.dd[r.ticker] = { verdict: r.verdict || null, dd_path: r.dd_path || null, dd_tag: r.dd_tag || null, source: "arena" };
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
        idx.dd[r.ticker] = { verdict: r.dca_verdict || null, dd_path: r.dd_path || null, dd_tag: null, source: "dd-screener" };
        if (!idx.quality[r.ticker]) {
          idx.quality[r.ticker] = qualityFromRoicFcf(r.roic, r.fcf);
          idx.quality[r.ticker].source = "dd-screener";
        }
      });
    }

    // ── 研究母體（/engine/universe_board.json，DD 池美股＋QGM 品質池＋可選但先不
    //    入席候選，即 arena.json universe_n 計數的同一份 ~277 檔全母體）：只補位
    //    ——任何欄位若已被 arena／dd-screener 設過就不覆蓋，這裡只把「board 母體
    //    以外」原本空白的名字（研究母體特有的候選/隊列名字）填上品質／DD／席位／
    //    擁有層分，讓「研究母體」切換能用同一套通用 render 函式運作，不用另開
    //    一套資料路徑。quality 直接讀 row.quality（伺服器已算好，不在瀏覽器端
    //    重算）；DD 讀 verdict／dd_tag；席位讀 seat；時機仍統一讀 lamp.json
    //    （universe_board 本身不帶階段欄）。────────────────────────────────
    if (idx.ok.universe) {
      universeBoard.rows.forEach(function (r) {
        if (!r || !r.ticker) return;
        idx.researchSet[r.ticker] = true;
        if (!idx.quality[r.ticker]) {
          var q = r.quality || {};
          idx.quality[r.ticker] = {
            pass: q.pass, why: q.why || [], exempt: !!q.exempt, roic: q.roic, fcf: q.fcf,
            source: "universe-board"
          };
        }
        if (!idx.dd[r.ticker] && (r.verdict || r.dd_path)) {
          idx.dd[r.ticker] = { verdict: r.verdict || null, dd_path: r.dd_path || null, dd_tag: r.dd_tag || null, source: "universe-board" };
        }
        if (idx.ownScore[r.ticker] == null && r.score != null && !isNaN(r.score)) idx.ownScore[r.ticker] = r.score;
        if (!idx.gMethod[r.ticker] && r.g_method) idx.gMethod[r.ticker] = r.g_method;
        if (!idx.seat[r.ticker] && r.seat) idx.seat[r.ticker] = r.seat;
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
    if (!d || !d.verdict) return { verdict: "無 DD", cls: "dd-none", path: d ? d.dd_path : null, tag: d ? d.dd_tag : null };
    return { verdict: d.verdict, cls: DD_CLS[d.verdict] || "dd-none", path: d.dd_path, tag: d.dd_tag || null };
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
    return { cls: cls, label: info.verdict, path: info.path, tag: info.tag };
  }

  // 名單頁小徽章只有一種尺寸：四格各一個色點＋2 字短標，肉眼可辨、不靠 hover；
  // 完整說明（差多少、來自哪段、第幾天）留給點擊後的彈出小卡（renderPopupBody）。
  var Q_SHORT = { pass: "過", fail: "未過", none: "缺" };
  var STAGE_SHORT = { S0: "弱勢", S1: "轉強", S2: "築底", S5: "高檔", S3: "收縮", S4: "領先", S9: "過渡" };
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
    html += popupRow("DD 裁決", chip(d), (d.tag && d.tag !== d.label) ? esc(d.tag) : "");
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
  // 本週清單專用排序：席位標記（C／S／B）優先，同層再依擁有層分排序——
  // 與 sortTickers 共用擁有層分邏輯，只多一層「有沒有席位」的優先鍵。
  function sortTickersSeatFirst(idx, list) {
    return list.slice().sort(function (a, b) {
      var sa = idx.seat[a] ? 1 : 0, sb = idx.seat[b] ? 1 : 0;
      if (sa !== sb) return sb - sa;
      var oa = idx.ownScore[a], ob = idx.ownScore[b];
      if (oa == null && ob == null) return a < b ? -1 : (a > b ? 1 : 0);
      if (oa == null) return 1;
      if (ob == null) return -1;
      if (ob !== oa) return ob - oa;
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
  // lifecycle order S0<S1<S2<S5<S3<S4 (2026-09-09 owner decision, mirrors
  // scripts/build_stages.py::ORDERED_STAGES) — a peak that only reaches S5
  // does NOT count toward peakS3plus below, same treatment S2 already got.
  var STAGE_DIGIT_RANK = { "0": 0, "1": 1, "2": 2, "5": 3, "3": 4, "4": 5 };
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
      // 領先／收縮完成本身已在頂段，「期間曾到收縮完成以上」對這兩段近乎必然成立
      // （剛進場當下就已站在那個高度），印出來是廢話——這兩段只印進場後第 60 日
      // 還在不在頂段、有沒有跌回弱勢；轉強／築底／弱勢三段維持原本三個數字
      // （2026-09-09 owner 走查回饋）。
      var topTier = spec.code === "S3" || spec.code === "S4";
      var detail = "";
      if (count > 0) {
        detail = topTier
          ? ("第 60 日仍在收縮完成或領先 " + fmt1(endS3S4 / count * 100) +
             "%、第 60 日在弱勢 " + fmt1(endS0 / count * 100) + "%")
          : ("第 60 日在收縮完成或領先 " + fmt1(endS3S4 / count * 100) +
             "%、期間曾到收縮完成以上 " + fmt1(peakS3plus / count * 100) +
             "%、第 60 日在弱勢 " + fmt1(endS0 / count * 100) + "%");
      }
      return { label: spec.label, n: count, detail: detail };
    });
  }

  // ── 轉強配對對照組（scripts/build_stages.py::build_control_deep_pullback
  //    的瀏覽器端重放，identical definition）：只重放「同一天配對」的比對邏
  //    輯，深回檔旗標本身（pullback_pct／dist_high_pct／eligible）已經在伺
  //    服器端算好、直接讀 history.deep 字串，不在瀏覽器重抓價格重算。graceful
  //    ：舊 history.json 沒有 deep 欄位時 idx.historyDeep 是空物件，這裡自然
  //    回傳 n=0，呼叫端顯示「資料不足」。──────────────────────────────────
  var CONTROL_NOT_S1_LOOKBACK_DAYS = 5;
  function computeControlDeepPullback(idx) {
    var dates = idx.historyDates || [];
    var n = dates.length;
    var maxI = n - 1 - 60;
    var out = { n: 0, peakS3plusPct: null, endS0Pct: null };
    if (maxI < 1) return out;
    var stagesByTk = idx.historyStages || {};
    var deepByTk = idx.historyDeep || {};
    var tickers = Object.keys(stagesByTk);
    // 1) 找出「至少一檔在當天轉強」的日子集合（不分品質，同伺服器端
    //    _s1_entry_days：collapse 到唯一日期，不逐 S1 事件重複）。
    var entryDays = [];
    for (var i = 1; i <= maxI; i++) {
      var any = false;
      for (var ti = 0; ti < tickers.length; ti++) {
        var s0 = stagesByTk[tickers[ti]];
        if (!s0 || s0.length !== n) continue;
        if (s0.charAt(i) === "1" && s0.charAt(i - 1) !== "1") { any = true; break; }
      }
      if (any) entryDays.push(i);
    }
    // 2) 每個轉強配對日 t：同一天 deep=1、當天不是轉強、且過去 5 個交易日內
    //    也不是轉強的其他標的，逐一 (ticker, t) 計一個對照事件。
    var count = 0, peakS3plus = 0, endS0 = 0;
    entryDays.forEach(function (i) {
      var lbStart = Math.max(0, i - CONTROL_NOT_S1_LOOKBACK_DAYS);
      tickers.forEach(function (tk) {
        var s = stagesByTk[tk];
        var d = deepByTk[tk];
        if (!s || s.length !== n || !d || d.length !== n) return;
        if (d.charAt(i) !== "1") return;
        if (s.charAt(i) === "1") return;
        for (var k = lbStart; k < i; k++) {
          if (s.charAt(k) === "1") return;
        }
        count++;
        var endCh = s.charAt(i + 60);
        if (endCh === "0") endS0++;
        var peakRank = -1;
        for (var k2 = i + 1; k2 <= i + 60; k2++) {
          var c = s.charAt(k2);
          if (c === "9") continue;
          var r = STAGE_DIGIT_RANK[c];
          if (r !== undefined && r > peakRank) peakRank = r;
        }
        if (peakRank >= STAGE_DIGIT_RANK["3"]) peakS3plus++;
      });
    });
    out.n = count;
    if (count > 0) {
      out.peakS3plusPct = peakS3plus / count * 100;
      out.endS0Pct = endS0 / count * 100;
    }
    return out;
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
    // 三態母體：board＝席位榜（own_board，約 60 檔）／research＝研究母體（universe_board，
    // 約 277 檔，cockpit 預設）／all＝全市場（lamp.json，約 1,400 檔，階段雷達頁預設）。
    var state = {
      universe: opts.universe === "all" ? "all" : (opts.universe === "board" ? "board" : "research"),
      onlyDD: false, onlySeat: false, expandS9: false
    };
    var wired = false;

    // ignoreToggles：本週清單只吃母體切換，不吃「只看有 DD」「只看席位與候補」
    // 兩個 chip（那兩個 chip 明訂只篩完整矩陣，見設計拍板與 controlsHTML 旁註）。
    function membersFor(idx, ignoreToggles) {
      var out = [];
      if (state.universe === "board") {
        if (!idx.ok.arena) return null;
        Object.keys(idx.boardSet).forEach(function (tk) { out.push(tk); });
      } else if (state.universe === "research") {
        Object.keys(idx.researchSet).forEach(function (tk) { out.push(tk); });
      } else {
        if (!idx.ok.lamp) return null;
        Object.keys(idx.timingCode).forEach(function (tk) { out.push(tk); });
      }
      if (!ignoreToggles) {
        if (state.onlyDD) out = out.filter(function (tk) { var d = idx.dd[tk]; return d && d.verdict; });
        if (state.onlySeat) out = out.filter(function (tk) { return !!idx.seat[tk]; });
      }
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
    // opts.hideMismatchBadge：本週清單③論點矛盾整格都是 mismatch，「DD 進場・
    // 品質未過」文字重覆 32 遍反而難掃——外框樣式（qtm-mismatch 的 box-shadow）
    // 與 title 說明照舊保留，只把行內文字徽章關掉。其餘呼叫端（格子、①②④）不
    // 傳 opts，行為不變。
    function tickerChipHTML(ticker, opts) {
      var idx = idxRef;
      var d = ddInfo(idx, ticker);
      var seat = idx.seat[ticker];
      var days = daysInStage(idx, ticker);
      var isNew = days != null && days <= 5;
      // DD 進場但品質未過：DD 判斷過進場，但現在的財務數字過不了品質閘——
      // 這批是最值得重新檢查論點的名字（見矩陣說明句與規則區塊）。
      var q = idx.quality[ticker];
      var mismatch = d.verdict === "進場" && q && q.pass === false;
      var cls = "qtm-tk " + d.cls + (isNew ? " new-week" : "") + (mismatch ? " qtm-mismatch" : "");
      var seatBadge = seat ? ('<span class="qtm-seat">' + esc(seat) + "</span>") : "";
      var hideMismatchBadge = !!(opts && opts.hideMismatchBadge);
      var mismatchBadge = (mismatch && !hideMismatchBadge) ? '<span class="qtm-warnflag">DD 進場・品質未過</span>' : "";
      var ddLabel = d.tag || d.verdict;
      var titleTxt = ticker + "：" + ddLabel + (isNew ? "（本週新進此格）" : "")
        + (mismatch ? "；DD 進場但品質未過，值得重新檢查論點" : "");
      return '<span class="' + cls + '" data-qtm-tk="' + esc(ticker) + '" data-qtm-mtx="1" tabindex="0" role="button" title="' + esc(titleTxt) + '">' + esc(ticker) + seatBadge + mismatchBadge + "</span>";
    }
    // 本週清單的名單渲染：同一顆 tickerChipHTML（外框、標記、彈出小卡皆共用），
    // 只是排版脈絡不同（清單而非格子）；沿用格子相同的「前 8 個＋更多 N」節流，
    // 「更多」按鈕吃的是既有全域 data-qtm-more／data-qtm-rest 點擊委派，不用另外接線。
    function weeklyChipsHTML(tickers, emptyMsg, chipOpts) {
      if (!tickers.length) {
        return '<div class="qtm-weekly-empty">' + esc(emptyMsg) + "</div>";
      }
      var chipFn = function (tk) { return tickerChipHTML(tk, chipOpts); };
      var visible = tickers.slice(0, 8), rest = tickers.slice(8);
      var tkListHtml = visible.map(chipFn).join("");
      var moreHtml = rest.length
        ? ('<button type="button" class="qtm-more" data-qtm-more>更多 ' + rest.length + '</button>' +
           '<span class="qtm-tk-list" data-qtm-rest hidden>' + rest.map(chipFn).join("") + "</span>")
        : "";
      return '<span class="qtm-tk-list">' + tkListHtml + "</span>" + moreHtml;
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
      // 空格（0 檔）沒有名單可展開，不印「展開名單」（2026-09-09 owner 走查回饋）
      var toggleBtn = (collapsedDefault && tickers.length) ? '<button type="button" class="qtm-toggle-collapse" data-qtm-toggle>展開名單</button>' : "";
      return '<div class="' + cls + (collapsedDefault ? " qtm-collapsed" : "") + '" data-qtm-colname="' + esc(QCOL_LABEL[qb]) + '">' +
        roleTag +
        '<span class="qtm-cell-count">' + tickers.length + "</span>" + deltaHtml + " " + toggleBtn +
        body +
        "</div>";
    }
    // 兩組分開（2026-09-09 owner 走查回饋：手機上分不清品質×時機的母體切換
    // 與篩選 chip 是同一件事還是兩件事）——組 A「母體」單選三顆、組 B「篩選」
    // 兩顆且標明只作用在完整矩陣（故本週清單旁原本的提醒句變多餘，一併拿掉，
    // 見 renderWeeklyStrip）。母體 chip 上的即時檔數讀 idx.boardN／researchN／
    // allN（buildIndex 已算好，缺資料顯示「—」）。
    function fmtN(n) { return n == null ? "—" : String(n); }
    function controlsHTML() {
      var idx = idxRef;
      return '<div class="qtm-controls">' +
        '<div class="qtm-control-group"><span class="qtm-control-label">母體</span>' +
        '<button type="button" class="qtm-chip' + (state.universe === "board" ? " on" : "") + '" data-qtm-chip="uni-board">席位榜（' + esc(fmtN(idx.boardN)) + '）</button>' +
        '<button type="button" class="qtm-chip' + (state.universe === "research" ? " on" : "") + '" data-qtm-chip="uni-research">研究母體（' + esc(fmtN(idx.researchN)) + '）</button>' +
        '<button type="button" class="qtm-chip' + (state.universe === "all" ? " on" : "") + '" data-qtm-chip="uni-all">全市場（' + esc(fmtN(idx.allN)) + '）</button>' +
        "</div>" +
        '<div class="qtm-control-group"><span class="qtm-control-label">篩選（只作用在完整矩陣）</span>' +
        '<button type="button" class="qtm-chip' + (state.onlyDD ? " on" : "") + '" data-qtm-chip="only-dd">只看有 DD</button>' +
        '<button type="button" class="qtm-chip' + (state.onlySeat ? " on" : "") + '" data-qtm-chip="only-seat">只看席位與候補</button>' +
        "</div>" +
        "</div>";
    }
    function renderHitRate() {
      var idx = idxRef;
      if (!idx.ok.history) {
        return '<div class="qtm-hitrate"><h4>命中率</h4><div class="qtm-empty">資料尚未產出（階段歷史 /stages/data/history.json 缺檔）</div></div>';
      }
      var rates = computeHitRates(idx);
      var control = computeControlDeepPullback(idx);
      var rowsHtml = rates.map(function (r) {
        var lowTag = r.n < 20 ? ' <span class="qtm-hit-lowsample">（樣本不足）</span>' : "";
        var controlHtml = "";
        if (r.label === "品質過 × 轉強") {
          if (control.n > 0) {
            var ctrlLowTag = control.n < 20 ? "（樣本不足）" : "";
            controlHtml = '<div class="qtm-hit-control">對照（同樣深回檔未轉強）：' +
              fmt1(control.peakS3plusPct) + "%／" + fmt1(control.endS0Pct) + "%，n＝" + control.n + ctrlLowTag + "</div>";
          } else {
            controlHtml = '<div class="qtm-hit-control">對照（同樣深回檔未轉強）：資料不足</div>';
          }
        }
        return '<div class="qtm-hit-row"><b>' + esc(r.label) + "</b>：過去 250 個交易日進入此格 n＝" + r.n + lowTag +
          (r.n > 0 ? "，" + esc(r.detail) : "") + "</div>" + controlHtml;
      }).join("");
      return '<div class="qtm-hitrate"><h4>命中率</h4>' + rowsHtml +
        '<p class="qtm-foot">過去 250 個交易日回算，品質以今日判定回推；描述現況，不預測。對照數字依序為期間曾到收縮完成以上／第 60 日在弱勢。</p></div>';
    }

    // ── 規則與注意事項：白話說明矩陣怎麼讀，開卡即展開、不藏在 hover 後面
    //    （2026-09-09 owner 走查回饋）。列的說明用 STAGE_ROW_ORDER／STAGE_DESC
    //    這組資料驅動——「高檔整理」（S5）已併入 STAGE_LABEL，這裡排在弱勢→
    //    轉強→築底→高檔整理→收縮完成→領先的順序。────────────────────────
    var STAGE_DESC = {
      S0: "股價在 50 日和 200 日均線下方，近三個月落後大盤。",
      S1: "剛從深回檔（跌破年高 25% 以上）翻上來，轉強六項條件同時滿足。",
      S2: "站上 50 日均線、多數模板條件通過，但離年高還有一段距離（−25%～−8%），還沒真正突破。",
      S5: "模板條件全過、離年高在 8% 以內，但相對強度還不到最強一群、波動量能也還沒像收縮完成那樣收斂——高檔盤整消化的階段。",
      S3: "模板條件全過、離年高在 8% 以內，波動與量能都在收縮，隨時可能突破。",
      S4: "模板條件全過、相對強度排在全市場前二成、離年高在 8% 以內——目前最強的一群。"
    };
    var STAGE_ROW_ORDER = ["S0", "S1", "S2", "S5", "S3", "S4"];
    function renderRulesBlock(idx) {
      var stageLines = STAGE_ROW_ORDER
        .filter(function (code) { return STAGE_DESC[code] && STAGE_LABEL[code]; })
        .map(function (code) {
          return "<li>" + esc(STAGE_LABEL[code]) + "：" + esc(STAGE_DESC[code]) + "</li>";
        }).join("");
      var uniN = idx.universeN != null ? idx.universeN : "約 277";
      return (
        '<details class="qtm-rules" open><summary>規則與注意事項</summary><div class="qtm-rules-body">' +
        "<p><b>欄的意思</b>：品質過＝ROIC 15% 以上且自由現金流率 10% 以上（重資本擴張期豁免：ROIC 25% 以上且自由現金流不為負；金融股不判定）；" +
        "品質未過＝差哪一條，點徽章看差多少；無品質資料＝沒有財務資料可判，不是未過。</p>" +
        "<p><b>列的意思</b>：每一段一行，過渡＝不符合以上任何一段的殘差態（資料不足、流動性不夠或分類不到），預設收合、可展開查看。</p>" +
        "<ul>" + stageLines + "</ul>" +
        "<p><b>四個有標籤的格子</b>：最該看（品質過×轉強）——基本面過關、動能剛翻上來，這批最值得花時間看。" +
        "持股警訊（品質過×弱勢）——基本面過關但動能轉弱，若是手上持股要留意。" +
        "研究隊列（品質未過×領先）——動能很強但財務數字還沒達標，值得研究但不是現成標的。" +
        "略過（品質未過×弱勢）——兩邊都沒亮，預設收合、不用花時間。" +
        "這是注意力導引，不是買賣指令，也不是排名。</p>" +
        "<p><b>不限格子的小標</b>：代號旁若掛著「DD 進場・品質未過」，是 DD 判斷過進場、但現在財務數字過不了品質閘的名字，任何格子都可能出現，完整名單見上方本週清單③論點矛盾。</p>" +
        "<p><b>標記圖例</b>：C／S／B＝核心席／衛星席／候補，數字是席次序；外框實線＝進場、空心＝觀望、虛線＝無 DD、劃線＝迴避；" +
        "底線＝本週新進此格；Δ＝較 5 個交易日前的家數變化；「更多」可展開看完整名單。</p>" +
        "<p><b>母體切換</b>：席位榜（現任與候補，約 60 檔）／研究母體（DD 池美股加品質池加缺三年成長預估的隊列，約 " + esc(String(uniN)) + " 檔——" +
        "席位不用先有 DD，但成長預估要是三年期，只有單年預估的才排在隊列）／" +
        "全市場（約 1,400 檔）。海外雙掛牌名字（如日股、KL 掛牌）沒有階段資料，一律落在過渡。</p>" +
        "<p><b>命中率怎麼算</b>：算的是進入某格後，第 60 個交易日在哪一段、期間曾到過的最高段；品質用今天的判定回推，不是進入當時的舊資料。" +
        "樣本數低於 20 標「樣本不足」。轉強格另外附一組對照——同樣深回檔但當天沒有轉強的股票，比較兩邊誰的後續表現好（對照資料不足會標明）。" +
        "這些數字描述過去，不是預測。</p>" +
        "<p><b>更新時間</b>：階段（縱軸）每個交易日美股收盤後更新，目前資料日 " + esc(idx.lampAsOf || "—") + "；" +
        "品質、擁有層分、席位（橫軸與標記）每週日隨選股引擎更新，目前資料日 " +
        esc(idx.arenaAsOf ? String(idx.arenaAsOf).slice(0, 10) : "—") + "；" +
        "DD 裁決隨新報告發布更新，目前資料日 " + esc(idx.ddAsOf || "—") + "。</p>" +
        "<p class=\"qtm-rules-close\">名單只回答「看誰」，不回答「買不買」與「何時」。</p>" +
        "</div></details>"
      );
    }

    // ── 標記圖例（一直顯示，2026-09-09 owner 走查回饋）：放在切換鈕下方、
    //    本週清單上方，用真實樣式的示例 chip（不只文字描述）讓手機讀者秒懂
    //    代號旁那圈框線與底線分別代表什麼。規則與注意事項內的完整版（含 Δ、
    //    「更多」、母體切換說明）維持不動、不重覆——這裡只挑六條最常撞到的
    //    標記，語句照 owner 指定的白話版本（「沒有 DD」而非「無 DD」等）。
    var LEGEND_SAMPLE = "示例";
    function legendChip(cls) {
      return '<span class="qtm-tk qtm-legend-chip ' + cls + '">' + esc(LEGEND_SAMPLE) + "</span>";
    }
    function renderLegend() {
      return '<div class="qtm-legend">' +
        '<span class="qtm-legend-item">' + legendChip("dd-in") + "＝DD 進場</span>" +
        '<span class="qtm-legend-item">' + legendChip("dd-watch") + "＝DD 觀望</span>" +
        '<span class="qtm-legend-item">' + legendChip("dd-none") + "＝沒有 DD</span>" +
        '<span class="qtm-legend-item">' + legendChip("dd-avoid") + "＝DD 迴避</span>" +
        '<span class="qtm-legend-item"><span class="qtm-seat">C</span>核心席／<span class="qtm-seat">S</span>衛星席／' +
        '<span class="qtm-seat">B</span>候補，數字＝席次</span>' +
        '<span class="qtm-legend-item">' + legendChip("new-week") + "＝本週新進</span>" +
        "</div>";
    }

    // ── 本週清單：把矩陣收斂成固定順序的四步（2026-09-09 owner 回饋——18 格
    //    表格讀者不知道怎麼用）。四步都用 membersFor(idx, true) 取母體，忽略
    //    「只看有 DD」「只看席位與候補」兩個 chip（那兩個只篩完整矩陣），只吃
    //    母體切換（席位榜／研究母體／全市場）。ticker 清單一律 sortTickersSeat-
    //    First（席位標記優先，同層再依擁有層分）＋既有 tickerChipHTML（外框／
    //    標記／彈出小卡與完整矩陣共用）。────────────────────────────────────
    function renderWeeklyStrip(idx) {
      var stripMembers = membersFor(idx, true);
      if (stripMembers === null) {
        var missingSrc = state.universe === "board" ? "陣容資料 /engine/arena.json"
          : state.universe === "research" ? "選股引擎研究母體 /engine/universe_board.json"
          : "個股階段雷達 /stages/data/lamp.json";
        return '<div class="qtm-weekly"><h4>本週清單</h4><div class="qtm-empty">資料尚未產出（' + esc(missingSrc) + "）</div></div>";
      }
      var buckets = bucketize(stripMembers);

      // ① 持股警訊：品質過×弱勢，只列帶席位標記的名字。
      var step1 = sortTickersSeatFirst(idx, (buckets.S0 ? buckets.S0.pass : []).filter(function (tk) { return !!idx.seat[tk]; }));
      // ② 最該看：品質過×轉強，全部。
      var step2 = sortTickersSeatFirst(idx, buckets.S1 ? buckets.S1.pass.slice() : []);
      // ③ 論點矛盾：全母體中「DD 進場・品質未過」的名字，不限階段，按所在階段分組列出。
      var step3Groups = [];
      STAGE_ORDER.concat(["S9"]).forEach(function (code) {
        var list = [];
        stripMembers.forEach(function (tk) {
          if (stageOf(idx, tk) !== code) return;
          var d = ddInfo(idx, tk);
          var q = idx.quality[tk];
          if (d.verdict === "進場" && q && q.pass === false) list.push(tk);
        });
        if (list.length) step3Groups.push({ code: code, list: sortTickersSeatFirst(idx, list) });
      });
      var step3Count = step3Groups.reduce(function (n, g) { return n + g.list.length; }, 0);
      // ④ 席位正常：品質過×（高檔整理／築底／收縮完成／領先），只列帶席位標記的名字。
      var step4 = [];
      ["S5", "S2", "S3", "S4"].forEach(function (code) {
        if (buckets[code]) {
          buckets[code].pass.forEach(function (tk) { if (idx.seat[tk]) step4.push(tk); });
        }
      });
      step4 = sortTickersSeatFirst(idx, step4);

      var s1 = '<li class="qtm-weekly-step"><div class="qtm-weekly-head"><span class="qtm-weekly-num">①</span>' +
        '<span class="qtm-weekly-title">持股警訊</span><span class="qtm-weekly-count">' + step1.length + " 檔</span></div>" +
        '<p class="qtm-weekly-desc">本來就想擁有的名字掉進弱勢了。動作是去看它的 DD 有沒有觸發證偽條件，不是賣。</p>' +
        weeklyChipsHTML(step1, "本週沒有席位掉進弱勢") + "</li>";

      var s2 = '<li class="qtm-weekly-step"><div class="qtm-weekly-head"><span class="qtm-weekly-num">②</span>' +
        '<span class="qtm-weekly-title">最該看</span><span class="qtm-weekly-count">' + step2.length + " 檔</span></div>" +
        '<p class="qtm-weekly-desc">基本面過關、回檔剛結束。去看 DD 裁決與板機。轉強本身沒有統計優勢（見下方對照組），這格只回答先看誰。</p>' +
        weeklyChipsHTML(step2, "這週沒有名字") + "</li>";

      var step3Body = !step3Count
        ? '<div class="qtm-weekly-empty">這週沒有名字</div>'
        : step3Groups.map(function (g) {
            return '<div class="qtm-weekly-substage"><b>' + esc(STAGE_LABEL[g.code] || g.code) + "</b>" +
              weeklyChipsHTML(g.list, "", { hideMismatchBadge: true }) + "</div>";
          }).join("");
      var s3 = '<li class="qtm-weekly-step"><div class="qtm-weekly-head"><span class="qtm-weekly-num">③</span>' +
        '<span class="qtm-weekly-title">論點矛盾</span><span class="qtm-weekly-count">' + step3Count + " 檔</span></div>" +
        '<p class="qtm-weekly-desc">你判斷過可以進場，但現在的財務數字過不了品質閘。重讀那份 DD：是資本週期暫時壓低，還是論點壞了。</p>' +
        step3Body + "</li>";

      var s4 = '<li class="qtm-weekly-step"><div class="qtm-weekly-head"><span class="qtm-weekly-num">④</span>' +
        '<span class="qtm-weekly-title">席位正常</span><span class="qtm-weekly-count">' + step4.length + " 檔</span></div>" +
        '<p class="qtm-weekly-desc">席位在正常狀態，不用動。</p>' +
        weeklyChipsHTML(step4, "這週沒有名字") + "</li>";

      return '<div class="qtm-weekly"><h4>本週清單</h4>' +
        '<ol class="qtm-weekly-steps">' + s1 + s2 + s3 + s4 + "</ol></div>";
    }

    var idxRef = null;
    function render(idx) {
      idxRef = idx;
      // 研究母體 404／缺檔的優雅降級：退回席位榜，不讓整塊矩陣壞掉（設計稿與
      // owner 指示——切換鈕狀態也一併回正，不留著「研究母體」亮著但畫的是別的資料）。
      if (state.universe === "research" && !idx.ok.universe) state.universe = "board";
      var members = membersFor(idx);
      var gridSection, s9Toggle = "", asOfNote = "";
      if (members === null) {
        var missing = state.universe === "board" ? "陣容資料 /engine/arena.json"
          : state.universe === "research" ? "選股引擎研究母體 /engine/universe_board.json"
          : "個股階段雷達 /stages/data/lamp.json";
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
          : state.universe === "research"
          ? ("資料來源：選股引擎研究母體" + (idx.universeAsOf ? ("（" + idx.universeAsOf + "）") : ""))
          : ("資料來源：個股階段雷達（" + (idx.lampAsOf || "—") + "）");
        asOfNote = '<p style="font-size:.68rem;color:var(--qtm-muted);margin:.5rem 0 0">母體 ' + members.length + " 檔 · " + esc(uniLabel) + "</p>";
        gridSection = '<div class="qtm-scroll"><div class="qtm-grid">' + gridHtml + "</div></div>" + s9Toggle + asOfNote;
      }
      el.innerHTML =
        '<div class="qtm-matrix">' +
        "<h3>品質 × 時機</h3>" +
        '<p class="qtm-lede">橫看基本面過不過閘，直看現在走到生命週期哪一段；多層都亮的格子是觀察池，只亮一邊的格子是研究隊列，兩邊都不亮的略過。它只回答「看誰」，不是買賣指令。</p>' +
        controlsHTML() +
        renderLegend() +
        renderWeeklyStrip(idx) +
        '<details class="qtm-full-matrix"><summary>完整矩陣（6 段 × 3 欄）</summary><div class="qtm-full-matrix-body">' +
        gridSection +
        renderRulesBlock(idx) +
        renderHitRate() +
        "</div></details>" +
        "</div>";
      if (!wired) {
        wired = true;
        el.addEventListener("click", function (ev) {
          var chip = ev.target.closest("[data-qtm-chip]");
          if (chip) {
            var k = chip.getAttribute("data-qtm-chip");
            if (k === "uni-board") state.universe = "board";
            else if (k === "uni-research") state.universe = "research";
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
