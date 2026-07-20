# 產業深度報告 HTML Template v3.0 — 外資 sell-side 版式（單檔）

**v3.0 起 dual-output 廢除**：每次跑 `industry-analyst` 只產**一份** `ID_{Theme}_{YYYYMMDD}.html`（本 template），取代 v2.x 的「精煉版（lean_template.md）＋完整考證版（html_template.md `_full.html`）」兩份制。決策與分歧前置、背景與考證後置（折疊），閱讀線＝外資報告資訊架構：Page-1 摘要層 → Thesis → Key Debates → 產業機制與供需 → 估值 → 風險證偽 → 個股 → 附錄。

## 檔名規則

`docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`

- Theme_CamelCase 範例：GlassSubstrate / HBM_Supercycle / AIASIC_vs_GPU / GLP1_Landscape / EUV_NextGen
- **不再產 `_full.html`**。單檔即全部。

## id-meta 放置規則（單檔、head 內）

- id-meta 一律放**本檔 `<head>` 內**：`<meta name="id-skill-version | id-theme | id-publish-date">` 三標 ＋ `<script id="id-meta" type="application/json">` JSON block。單檔＝SSOT，索引／screener／validator 全認這份。
- 欄位 schema 沿 v2.x（`validate_id_meta.py` 強制）：`now_state` / `future_state` / `action` / `sd_verdict` / `clock_phase` / `conviction` / `priced_in`（v2.6+ 必填）/ `kill_metrics[]` / `demand_5y_multiple` / `related_tickers[]` 等。
- 版號戳（`skill_version`、頁首 byline、colophon）一律**隨 SKILL.md frontmatter**，template 內以 `{{SKILL_VERSION}}` 佔位，不得寫死。

## 章節機器錨點（固定，下游與 TOC 依此）

| 錨點 | 章節 |
|---|---|
| `id="summary"` | Page-1 摘要層（masthead ＋ rating strip ＋ Key Points ＋ NOW/NEXT/ACTION） |
| `id="thesis"` | 1 Investment Thesis |
| `id="debates"` | 2 Key Debates |
| `id="mechanics"` | 3 產業機制與供需（內含 3.1 需求／3.2 供給／3.3 技術根／3.4 裁決 四個 h3 小節） |
| `id="valuation"` | 4 估值傳導 |
| `id="risks"` | 5 風險與證偽 |
| `id="stocks"` | 6 個股含意 |
| `id="appendix"` | 附錄（背景與考證，整節預設折疊） |

主題若需要額外機制小節（如某輪供給側新變數），加在 `mechanics` 內為 3.x 追加 h3，**不得**取代上表四個固定小節、不得新增頂層錨點。

## rating strip ↔ id-meta 欄位對應

rating strip 八格中五格為機器欄鏡像，**值必須與 id-meta JSON 一字不差同步**（下游直讀機器欄，矛盾比散文錯更危險）：

| 格 | id-meta 欄位 |
|---|---|
| 供需裁決 | `sd_verdict` |
| 投資時鐘 | `clock_phase` |
| Conviction | `conviction` |
| Priced-in | `priced_in` |
| Demand 5Y Multiple | `demand_5y_multiple` |

其餘三格（Sector View／Focus Names／避開特徵）為散文層，無機器欄。缺值格用 `<span class="v is-empty">—</span>` 並在小字註明去哪讀散文。

## 基本骨架（完整 HTML）

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<meta name="color-scheme" content="only light">
<title>{{THEME}} — {{TITLE_TAGLINE}} | InvestMQuest</title>
<meta name="id-skill-version" content="{{SKILL_VERSION}}">
<meta name="id-theme" content="{{THEME_EN}}">
<meta name="id-publish-date" content="{{PUBLISH_DATE}}">
<script id="id-meta" type="application/json">
{
  "theme": "{{THEME_EN}}",
  "skill_version": "{{SKILL_VERSION}}",
  "id_version": "{{ID_VERSION}}",
  "publish_date": "{{PUBLISH_DATE}}",
  "thesis_type": "{{THESIS_TYPE}}",
  "ai_exposure": "{{AI_EXPOSURE}}",
  "oneliner": "{{ONELINER}}",
  "now_state": "{{NOW_STATE}}",
  "future_state": "{{FUTURE_STATE}}",
  "action": "{{ACTION}}",
  "related_tickers": [
    {
      "ticker": "{{TICKER_1}}",
      "role": "{{TICKER_1_ROLE}}",
      "depth": "{{TICKER_1_DEPTH}}",
      "beneficiary": true,
      "mcap_bucket": "{{TICKER_1_MCAP}}"
    }
  ],
  "sd_verdict": "{{SD_VERDICT}}",
  "clock_phase": "{{CLOCK_PHASE}}",
  "conviction": "{{CONVICTION}}",
  "priced_in": "{{PRICED_IN}}",
  "kill_metrics": [
    {
      "metric": "{{KILL_METRIC_1}}",
      "bear_threshold": "{{KILL_METRIC_1_BEAR}}",
      "window": "{{KILL_METRIC_1_WINDOW}}"
    }
  ],
  "demand_5y_multiple": {{DEMAND_5Y_MULTIPLE}},
  "tam_usd_2030": {{TAM_USD_2030}},
  "cagr_pct_5y": {{CAGR_PCT_5Y}},
  "growth_phase": "{{GROWTH_PHASE}}",
  "value_chain_position": "{{VALUE_CHAIN_POSITION}}",
  "industry_structure": "{{INDUSTRY_STRUCTURE}}",
  "quality_tier": "{{QUALITY_TIER}}",
  "mega": "{{MEGA}}",
  "sub_group": "{{SUB_GROUP}}",
  "sister_ids": ["{{SISTER_ID_1}}"],
  "sections_refreshed": {
    "technical": "{{PUBLISH_DATE}}",
    "market": "{{PUBLISH_DATE}}",
    "judgment": "{{PUBLISH_DATE}}"
  }
}
</script>

<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Noto+Serif+TC:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* ============================================================
   InvestMQuest — sell-side equity research page style
   ⚠ 此 CSS 未來抽出為 docs/id/assets/id.css 共用檔，屆時 template
     改為 <link rel="stylesheet" href="/id/assets/id.css">；
     抽出前每檔 inline（勿改元件命名，抽出時 diff 才乾淨）。
   ============================================================ */
:root{
  /* color tokens */
  --navy-900:#081832;          /* site nav deep navy（與 imq-nav 連貫） */
  --navy-700:#0d2244;          /* primary accent：exhibit header、rating strip 界線 */
  --navy-500:#173564;          /* secondary accent：連結、章節標記 */
  --navy-050:#eef2f8;          /* navy tint 底色（時間標記、選取列） */
  --ink:#141a24;               /* 標題墨色 */
  --body:#28303d;              /* 內文 */
  --muted:#5c6675;             /* 次要文字、來源行 */
  --faint:#8b93a0;             /* 最淡標籤 */
  --paper:#ffffff;             /* 紙面 */
  --paper-soft:#f5f6f8;        /* 頁面底、斑馬紋 */
  --rule:#d9dde3;              /* 細灰分隔線 */
  --rule-strong:#0d2244;       /* 粗界線（navy） */
  --pos:#1e6b4f;               /* 正向 / bull */
  --neg:#9c2f2f;               /* 負向 / bear */
  --warn:#8a6420;              /* 警示 / base */
  --gold:#b8924a;              /* 站內金色點綴（與 nav logo 一致），僅小面積使用 */
  /* type tokens */
  --font-serif:'Source Serif 4','Noto Serif TC',Georgia,'Times New Roman',serif;
  --font-sans:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --font-mono:'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,monospace;
  /* spacing tokens */
  --sp-1:4px;--sp-2:8px;--sp-3:12px;--sp-4:16px;--sp-5:24px;--sp-6:32px;--sp-7:48px;
  --measure:70ch;              /* 內文行長上限 */
  --sheet-max:900px;
  --nav-h:45px;                /* sticky 站內 nav 高度（TOC offset 用） */
}
*{box-sizing:border-box}
html{color-scheme:light}
body{margin:0;background:var(--paper-soft);color:var(--body);font-family:var(--font-sans);font-size:15px;line-height:1.75;-webkit-font-smoothing:antialiased;counter-reset:exhibit}
a{color:var(--navy-500)}

/* ---------- report sheet（紙面） ---------- */
.report-sheet{max-width:var(--sheet-max);margin:28px auto 64px;background:var(--paper);border:1px solid var(--rule);border-top:5px solid var(--navy-700);padding:0 56px 56px;box-shadow:0 1px 4px rgba(8,24,50,.06)}

/* ---------- masthead（銀行式報告頭） ---------- */
.masthead{padding:26px 0 0}
.masthead-strip{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--rule);padding-bottom:10px}
.masthead-strip .brand{color:var(--navy-700);font-weight:600}
.report-kicker{font-family:var(--font-mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--navy-500);font-weight:600;margin:24px 0 10px}
.report-title{font-family:var(--font-serif);font-size:33px;line-height:1.25;font-weight:700;color:var(--ink);margin:0 0 10px;letter-spacing:-.005em}
.report-title em{font-style:italic;color:var(--navy-500)}
.report-deck{font-family:var(--font-serif);font-size:16.5px;font-style:italic;color:var(--muted);line-height:1.6;margin:0 0 16px;max-width:var(--measure)}
.report-byline{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:9px 0;margin-bottom:16px}

/* ---------- rating strip（外資報告首頁評等框） ---------- */
.rating-strip{display:grid;grid-template-columns:repeat(4,1fr);border:1.5px solid var(--rule-strong);margin:0 0 20px}
.rating-cell{padding:10px 13px 9px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.rating-cell:nth-child(4n){border-right:none}
.rating-cell:nth-last-child(-n+4){border-bottom:none}
.rating-cell .k{display:block;font-family:var(--font-mono);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);margin-bottom:4px}
.rating-cell .v{font-family:var(--font-serif);font-size:17px;font-weight:700;color:var(--navy-700);line-height:1.2}
.rating-cell .v.is-empty{color:var(--faint);font-weight:400}
.rating-cell .s{display:block;font-size:11px;color:var(--muted);margin-top:2px;line-height:1.45}

/* ---------- key points ---------- */
.key-points{margin:0 0 20px;border-top:2px solid var(--rule-strong);padding-top:12px}
.key-points h2{font-family:var(--font-mono);font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--navy-700);margin:0 0 10px;border:none;padding:0}
.key-points ul{margin:0;padding-left:0;list-style:none}
.key-points li{position:relative;padding:0 0 9px 22px;font-size:14.5px;line-height:1.7;max-width:none}
.key-points li::before{content:'';position:absolute;left:2px;top:11px;width:8px;height:2px;background:var(--navy-500)}

/* ---------- sticky section TOC ---------- */
.toc-bar{position:sticky;top:var(--nav-h);z-index:900;background:rgba(255,255,255,.97);backdrop-filter:blur(4px);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin:0 -56px 8px;padding:7px 56px;display:flex;flex-wrap:wrap;gap:2px;font-family:var(--font-mono);font-size:10.5px}
.toc-bar a{color:var(--navy-500);text-decoration:none;padding:3px 8px;font-weight:500;letter-spacing:.02em}
.toc-bar a:hover{background:var(--navy-700);color:#fff}

/* ---------- section ---------- */
.section{margin:42px 0 0;scroll-margin-top:96px}
.section-no{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);font-weight:600;margin-bottom:4px}
.section h2{font-family:var(--font-serif);font-size:24px;font-weight:700;color:var(--ink);line-height:1.3;margin:0 0 12px;padding-bottom:10px;border-bottom:2px solid var(--rule-strong)}
.section h2 em{font-style:italic;color:var(--navy-500)}
.section h3{font-family:var(--font-serif);font-size:17.5px;font-weight:600;color:var(--navy-700);margin:26px 0 8px}
.section p{margin:0 0 14px;max-width:var(--measure);font-size:15px;line-height:1.8}
.section ul,.section ol{margin:10px 0 16px;padding-left:22px;max-width:var(--measure)}
.section li{margin:6px 0;line-height:1.72}
.section-lede{font-family:var(--font-serif);font-style:italic;font-size:15.5px;color:var(--muted);line-height:1.65;border-left:3px solid var(--rule-strong);padding:2px 0 2px 16px;margin:0 0 16px;max-width:var(--measure)}
strong{color:var(--ink);font-weight:600}
.section em{color:var(--navy-500)}
mark.time{background:var(--navy-050);color:var(--navy-700);padding:1px 6px;font-family:var(--font-mono);font-size:12px;font-weight:600;white-space:nowrap}
.path-pos{color:var(--pos);font-weight:600}
.path-neg{color:var(--neg);font-weight:600}

/* ---------- view grid（NOW / NEXT / ACTION 決策卡） ---------- */
.view-grid{display:grid;grid-template-columns:repeat(3,1fr);border:1.5px solid var(--rule-strong);margin:0 0 18px}
.view-card{padding:13px 15px;border-right:1px solid var(--rule)}
.view-card:last-child{border-right:none}
.view-tag{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;margin-bottom:8px}
.view-card.is-now .view-tag{color:var(--pos)}
.view-card.is-next .view-tag{color:var(--warn)}
.view-card.is-act .view-tag{color:var(--neg)}
.view-card p{font-size:13px;line-height:1.64;margin:0;max-width:none}

/* ---------- key call ---------- */
.key-call{background:var(--navy-700);color:#eef2f8;padding:22px 26px;margin:18px 0}
.key-call .kc-label{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:10px}
.key-call p{color:#eef2f8;font-size:15px;line-height:1.75;margin:0;max-width:none}
.key-call strong{color:#fff}
.key-call em{color:#d4b576;font-style:italic}

/* ---------- thesis box ---------- */
.thesis-box{border:1px solid var(--rule);border-left:4px solid var(--navy-700);background:var(--paper-soft);padding:16px 20px;margin:18px 0;font-size:14.5px;line-height:1.72;max-width:none}
.thesis-box .label{display:inline-block;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;background:var(--navy-700);color:#fff;padding:2px 10px;font-weight:600;margin-bottom:10px}

/* ---------- debate card（Key Debates 分節框架） ---------- */
.debate-card{border:1px solid var(--rule-strong);margin:18px 0}
.debate-head{background:var(--paper-soft);border-bottom:1px solid var(--rule);padding:10px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.debate-head .dt{font-family:var(--font-serif);font-size:16px;font-weight:700;color:var(--ink)}
.debate-head .dt .dn{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--navy-500);font-weight:600;margin-right:10px}
.debate-row{display:grid;grid-template-columns:118px 1fr;border-bottom:1px solid var(--rule)}
.debate-row:last-child{border-bottom:none}
.debate-row .dr-k{padding:11px 14px;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--muted);background:var(--paper-soft);border-right:1px solid var(--rule)}
.debate-row.is-market .dr-k{color:var(--muted)}
.debate-row.is-view .dr-k{color:var(--navy-500)}
.debate-row.is-signal .dr-k{color:var(--neg)}
.debate-row .dr-v{padding:11px 15px;font-size:13.5px;line-height:1.66}

/* ---------- monitor list（PM 級監測點） ---------- */
.monitor-list{border:1px solid var(--rule-strong);margin:18px 0}
.monitor-list .ml-head{background:var(--navy-700);color:#fff;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;padding:8px 14px;font-weight:600}
.monitor-item{display:grid;grid-template-columns:34px 1fr;padding:11px 14px;border-bottom:1px solid var(--rule)}
.monitor-item:last-child{border-bottom:none}
.monitor-num{font-family:var(--font-mono);font-size:13px;font-weight:600;color:var(--navy-500)}
.monitor-body{font-size:13.5px;line-height:1.62}
.monitor-body strong{color:var(--neg)}

/* ---------- judgment card（推論卡） ---------- */
.judgment-card{border:1px solid var(--rule);border-left:4px solid var(--gold);padding:14px 18px;margin:18px 0;background:#fff}
.judgment-card .j-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-family:var(--font-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--navy-700);margin-bottom:8px}
.badge{display:inline-block;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.08em;padding:2px 8px;font-weight:600;color:#fff}
.badge.is-high{background:var(--pos)}
.badge.is-mid{background:var(--warn)}
.badge.is-low{background:var(--neg)}
.judgment-card ul{margin:6px 0;padding-left:20px}
.judgment-card li{font-size:13.5px;line-height:1.64;margin:5px 0}
.judgment-card .j-logic{font-size:13px;background:var(--paper-soft);border-top:1px solid var(--rule);padding:9px 12px;margin-top:10px;line-height:1.6}

/* ---------- callouts ---------- */
.callout{border:1px solid var(--rule);border-left:4px solid var(--muted);padding:13px 18px;margin:16px 0;font-size:13.5px;line-height:1.66;max-width:none}
.callout .co-label{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;font-weight:600;display:block;margin-bottom:6px}
.callout.is-implication{border-left-color:var(--pos)}
.callout.is-implication .co-label{color:var(--pos)}
.callout.is-risk{border-left-color:var(--neg);background:#fdf7f6}
.callout.is-risk .co-label{color:var(--neg)}
.callout.is-bridge{border-left-color:var(--gold)}
.callout.is-bridge .co-label{color:var(--warn)}

/* ---------- exhibit（sell-side 表格） ---------- */
.exhibit{counter-increment:exhibit;margin:20px 0 4px;border:1px solid var(--rule-strong)}
.exhibit-head{background:var(--navy-700);color:#fff;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;padding:8px 14px;font-weight:600}
.exhibit-head::before{content:"Exhibit " counter(exhibit) "\00a0\00a0·\00a0\00a0";color:#d4b576}
.exhibit-body{overflow-x:auto}
.exhibit table{width:100%;border-collapse:collapse;background:var(--paper);min-width:560px}
.exhibit th{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;text-align:left;padding:9px 13px;border-bottom:2px solid var(--rule-strong);background:var(--paper-soft)}
.exhibit td{padding:9px 13px;border-bottom:1px solid var(--rule);font-size:13.5px;line-height:1.55;vertical-align:top}
.exhibit tbody tr:nth-child(even) td{background:var(--paper-soft)}
.exhibit tbody tr:last-child td{border-bottom:none}
.exhibit td.num,.exhibit td .num{font-family:var(--font-mono);font-size:12.5px}
.exhibit-source{font-size:11px;color:var(--muted);margin:6px 0 2px;line-height:1.5}
.exhibit-note{font-family:var(--font-serif);font-style:italic;font-size:13.5px;color:var(--muted);line-height:1.66;margin:6px 0 18px;max-width:var(--measure)}

/* ---------- figure（ASCII 示意圖） ---------- */
.figure-ascii{background:var(--paper-soft);border:1px solid var(--rule);color:var(--navy-700);padding:14px 16px;font-family:var(--font-mono);font-size:12px;line-height:1.45;white-space:pre;overflow-x:auto;margin:16px 0}

/* ---------- tier list（conviction 分層） ---------- */
.tier-list{border:1px solid var(--rule-strong);margin:18px 0}
.tier-row{display:grid;grid-template-columns:150px 1fr;border-bottom:1px solid var(--rule)}
.tier-row:last-child{border-bottom:none}
.tier-name{padding:13px 15px;background:var(--paper-soft);border-right:1px solid var(--rule)}
.tier-name h4{margin:4px 0 0;font-family:var(--font-serif);font-size:15.5px;font-weight:700;color:var(--ink);line-height:1.3}
.tier-badge{display:inline-block;font-family:var(--font-mono);font-size:9px;letter-spacing:.1em;padding:2px 7px;font-weight:600;color:#fff}
.tier-badge.is-core{background:var(--navy-700)}
.tier-badge.is-swing{background:var(--warn)}
.tier-badge.is-edge{background:var(--muted)}
.tier-detail{padding:13px 16px;font-size:13.5px;line-height:1.64}
.tier-detail .conv{display:block;font-family:var(--font-mono);font-size:10.5px;color:var(--muted);margin-top:6px}

/* ---------- event line（catalyst timeline） ---------- */
.event-line{margin:14px 0 18px;border-left:2px solid var(--rule-strong);padding-left:18px;max-width:var(--measure)}
.event-line p{margin:0 0 12px;font-size:14px;line-height:1.7}
.event-date{display:inline-block;font-family:var(--font-mono);font-size:11px;font-weight:600;background:var(--navy-050);color:var(--navy-700);padding:1px 7px;margin-right:6px;white-space:nowrap}

/* ---------- evidence fold（考證與來源折疊層） ---------- */
.evidence-fold{border:1px solid var(--rule);margin:18px 0 6px;background:#fff}
.evidence-fold summary{cursor:pointer;list-style:none;font-family:var(--font-mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:600;padding:9px 14px;background:var(--paper-soft);user-select:none}
.evidence-fold summary::-webkit-details-marker{display:none}
.evidence-fold summary::before{content:'▸';display:inline-block;margin-right:8px;color:var(--navy-500);transition:transform .12s}
.evidence-fold[open] summary::before{transform:rotate(90deg)}
.evidence-fold[open] summary{border-bottom:1px solid var(--rule)}
.evidence-fold .fold-body{padding:14px 18px 8px}
.evidence-fold .fold-body p{font-size:13.5px;color:var(--body);line-height:1.72;max-width:var(--measure);margin:0 0 12px}
.src-list{margin:8px 0 10px;padding-left:20px;font-size:12px;color:var(--muted);line-height:1.6}
.src-list li{margin:4px 0}
.src-list a{color:var(--navy-500);text-decoration:none}
.src-list .tier{font-family:var(--font-mono);font-size:10px;color:var(--warn);font-weight:600;margin-right:6px}
.src-label{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);font-weight:600;display:block;margin:10px 0 4px}

/* ---------- pull quote（一行結論） ---------- */
.pull-quote{border-top:2px solid var(--rule-strong);border-bottom:2px solid var(--rule-strong);margin:44px 0 20px;padding:24px 8px;text-align:center}
.pull-quote .pq-label{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--faint);margin-bottom:12px}
.pull-quote p{font-family:var(--font-serif);font-size:19px;line-height:1.65;color:var(--ink);margin:0;font-weight:500}
.pull-quote strong{color:var(--navy-700)}

/* ---------- crosslinks ---------- */
.crosslink{border:1px solid var(--rule);background:var(--paper-soft);padding:11px 16px;margin:0 0 16px;font-size:12.5px;line-height:1.7;color:var(--muted)}
.crosslink a{color:var(--navy-500);font-weight:600;text-decoration:none}

/* ---------- disclosures 頁尾 ---------- */
.disclosures{margin-top:44px;border-top:3px double var(--rule-strong);padding-top:16px;font-size:11px;color:var(--muted);line-height:1.65}
.disclosures .dh{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--navy-700);font-weight:600;margin-bottom:6px}
.report-colophon{margin-top:22px;text-align:center;font-family:var(--font-mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);line-height:1.9}
.report-colophon a{color:var(--navy-500);text-decoration:none}

/* ---------- back to top ---------- */
.back-top{position:fixed;right:18px;bottom:18px;z-index:950;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.08em;background:#fff;color:var(--navy-700);border:1px solid var(--rule-strong);padding:7px 12px;text-decoration:none;box-shadow:0 1px 4px rgba(8,24,50,.12)}
.back-top:hover{background:var(--navy-700);color:#fff}

/* ---------- RWD ---------- */
@media (max-width:820px){
  .report-sheet{margin:0;border-left:none;border-right:none;padding:0 20px 40px}
  .toc-bar{position:static;margin:0 -20px 8px;padding:7px 20px}
  .report-title{font-size:26px}
  .section h2{font-size:20px}
  .rating-strip{grid-template-columns:repeat(2,1fr)}
  .rating-cell:nth-child(4n){border-right:1px solid var(--rule)}
  .rating-cell:nth-child(2n){border-right:none}
  .view-grid{grid-template-columns:1fr}
  .view-card{border-right:none;border-bottom:1px solid var(--rule)}
  .view-card:last-child{border-bottom:none}
  .debate-row{grid-template-columns:1fr}
  .debate-row .dr-k{border-right:none;border-bottom:1px solid var(--rule);padding:7px 14px}
  .tier-row{grid-template-columns:1fr}
  .tier-name{border-right:none;border-bottom:1px solid var(--rule)}
}
@media print{
  body{background:#fff}
  .report-sheet{box-shadow:none;border:none;margin:0;max-width:none}
  .toc-bar,.back-top,.imq-nav-root{display:none !important}
  .evidence-fold[open] summary::before{content:''}
}
</style>
</head>
<body id="top">
<!-- ▼▼ canonical site header — 全站統一，由 scripts/site_nav.py full_nav_block('research','id') 生成。
     照抄規則：不要手改；產檔時執行
       python3 -c "import sys; sys.path.insert(0,'scripts'); import site_nav; print(site_nav.full_nav_block('research','id'))"
     把輸出整塊（含 <style id="imq-nav-style"> ＋ <header> ＋ <script>）貼進本區，取代下方三個佔位符。
     nav 結構隨 site_nav.py 演進，以現跑輸出為準；site_nav.py 變更後既有頁面由 re-inject 流程重生。 ▼▼ -->
{{SITE_NAV_FULL_BLOCK}}
<!-- ▲▲ canonical site header 結束 ▲▲ -->

<div class="report-sheet">

<!-- ============================================================
     PAGE 1 · 首頁摘要層（外資報告 page 1）
     ============================================================ -->
<header id="summary" class="masthead" style="scroll-margin-top:96px">
  <div class="masthead-strip">
    <span><span class="brand">InvestMQuest Research</span>&nbsp;&nbsp;·&nbsp;&nbsp;產業深度研究 · Industry Equity Research</span>
    <span>{{SECTOR_LABEL}}&nbsp;&nbsp;·&nbsp;&nbsp;{{DATE_CITY_LINE}}</span>
  </div>
  <div class="report-kicker">Industry Deep Report · {{THEME_EN}}</div>
  <h1 class="report-title">{{TITLE_MAIN}}<em>{{TITLE_EM}}</em>{{TITLE_TAIL}}</h1>
  <p class="report-deck">{{DECK}}</p>
  <div class="report-byline">
    <span>發布日 {{PUBLISH_DATE}} ｜ 涵蓋股票 {{N_TICKERS}}</span>
    <span>sub_group：{{SUB_GROUP}} ｜ Method：{{METHOD_LINE}}</span>
  </div>

  <!-- rating strip：五格為 id-meta 機器欄鏡像（sd_verdict / clock_phase / conviction /
       priced_in / demand_5y_multiple），值必須與 head 內 id-meta JSON 一字不差同步 -->
  <div class="rating-strip">
    <div class="rating-cell"><span class="k">Sector View</span><span class="v">{{SECTOR_VIEW}}</span><span class="s">產業結構觀點，非個股評等</span></div>
    <!-- id-meta: sd_verdict -->
    <div class="rating-cell"><span class="k">供需裁決</span><span class="v">{{SD_VERDICT_DISPLAY}}</span><span class="s">{{SD_VERDICT_NOTE}}</span></div>
    <!-- id-meta: clock_phase -->
    <div class="rating-cell"><span class="k">投資時鐘</span><span class="v">Phase {{CLOCK_PHASE}}</span><span class="s">{{CLOCK_PHASE_NOTE}}</span></div>
    <!-- id-meta: conviction -->
    <div class="rating-cell"><span class="k">Conviction</span><span class="v">{{CONVICTION_DISPLAY}}</span><span class="s">{{CONVICTION_NOTE}}</span></div>
    <!-- id-meta: priced_in -->
    <div class="rating-cell"><span class="k">Priced-in</span><span class="v">{{PRICED_IN_DISPLAY}}</span><span class="s">{{PRICED_IN_NOTE}}</span></div>
    <!-- id-meta: demand_5y_multiple -->
    <div class="rating-cell"><span class="k">Demand 5Y Multiple</span><span class="v">~{{DEMAND_5Y_MULTIPLE}}×</span><span class="s">{{DEMAND_MULTIPLE_SCOPE}}</span></div>
    <div class="rating-cell"><span class="k">Focus Names</span><span class="v">{{FOCUS_NAMES}}</span><span class="s">特徵代表案例，非買入推薦</span></div>
    <div class="rating-cell"><span class="k">避開特徵</span><span class="v">{{AVOID_TRAIT}}</span><span class="s">{{AVOID_TRAIT_NOTE}}</span></div>
  </div>

  <section class="key-points">
    <h2>Key Points</h2>
    <ul>
      <li>{{KEY_POINT_1}}</li>
      <li>{{KEY_POINT_2}}</li>
      <li>{{KEY_POINT_3}}</li>
      <li>{{KEY_POINT_4}}</li>
      <li>{{KEY_POINT_5}}</li>
    </ul>
  </section>

  <div class="exhibit">
    <div class="exhibit-head">關鍵數據一覽</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>指標</th><th>數值</th><th>註記</th></tr></thead>
        <tbody>
          <tr><td>{{STAT_1_NAME}}</td><td class="num">{{STAT_1_VALUE}}</td><td>{{STAT_1_NOTE}}</td></tr>
          <tr><td>{{STAT_2_NAME}}</td><td class="num">{{STAT_2_VALUE}}</td><td>{{STAT_2_NOTE}}</td></tr>
          <tr><td>{{STAT_3_NAME}}</td><td class="num">{{STAT_3_VALUE}}</td><td>{{STAT_3_NOTE}}</td></tr>
          <tr><td>{{STAT_4_NAME}}</td><td class="num">{{STAT_4_VALUE}}</td><td>{{STAT_4_NOTE}}</td></tr>
          <tr><td>{{STAT_5_NAME}}</td><td class="num">{{STAT_5_VALUE}}</td><td>{{STAT_5_NOTE}}</td></tr>
          <tr><td>{{STAT_6_NAME}}</td><td class="num">{{STAT_6_VALUE}}</td><td>{{STAT_6_NOTE}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{PAGE1_EXHIBIT_SOURCES}}；InvestMQuest Research 整理</p>

  <div class="view-grid">
    <div class="view-card is-now">
      <div class="view-tag">現在 / NOW</div>
      <p>{{NOW_STATE_PROSE}}</p>
    </div>
    <div class="view-card is-next">
      <div class="view-tag">未來 / NEXT</div>
      <p>{{FUTURE_STATE_PROSE}}</p>
    </div>
    <div class="view-card is-act">
      <div class="view-tag">行動 / ACTION</div>
      <p>{{ACTION_PROSE}}</p>
    </div>
  </div>

  <div class="crosslink">
    母題與姊妹報告：{{CROSSLINK_INTRO}}<a href="/id/{{SISTER_ID_1}}">{{SISTER_ID_1_TITLE}}</a>（{{SISTER_ID_1_SCOPE}}）／{{CROSSLINK_MORE}}
  </div>
</header>

<!-- ============ STICKY TOC（錨點固定，不得改名） ============ -->
<nav class="toc-bar" aria-label="section navigation">
  <a href="#summary">摘要</a><a href="#thesis">1 Thesis</a><a href="#debates">2 Debates</a><a href="#mechanics">3 機制與供需</a><a href="#valuation">4 估值</a><a href="#risks">5 風險證偽</a><a href="#stocks">6 個股</a><a href="#appendix">附錄</a>
</nav>

<!-- ============================================================
     1 · INVESTMENT THESIS
     ============================================================ -->
<section id="thesis" class="section">
  <div class="section-no">Section 1 · Investment Thesis</div>
  <h2>Investment Thesis</h2>

  <div class="key-call">
    <div class="kc-label">Key Call · 本報告最重要的一個判斷</div>
    <p>{{KEY_CALL_PROSE}}</p>
  </div>

  <p>{{THESIS_STRUCTURE_PARA}}</p>

  <p><strong>供需裁決</strong>：{{SD_VERDICT_PARA}}</p>

  <p><strong>投資時鐘</strong>：當前 <strong>Phase {{CLOCK_PHASE}}</strong>（{{PHASE_LABEL}}）。轉下階段<em>必要條件</em>＝{{PHASE_SHIFT_NECESSARY}}；<em>充分條件</em>＝{{PHASE_SHIFT_SUFFICIENT}}。<strong>領先指標</strong>：{{LEADING_INDICATORS}}。</p>

  <div class="thesis-box">
    <span class="label">核心 Thesis</span><br>
    <strong>{{ONELINER_PROSE}}</strong> 🔵 [X: base 很可能 — {{THESIS_BASE_CASE}}；bull 可能 — {{THESIS_BULL_CASE}}；bear 不太可能 — {{THESIS_BEAR_CASE}}]
  </div>

  <div class="judgment-card">
    <div class="j-head">Portfolio Implication（PM 級行動結論）<span class="badge is-{{PM_CONVICTION_CLASS}}">conviction：{{PM_CONVICTION}}</span></div>
    <ul>
      <li><strong>thesis 方向</strong>：{{PM_THESIS_DIRECTION}}</li>
      <li><strong>個股 conviction tier 變化</strong>：{{PM_TIER_CHANGES}}</li>
      <li><strong>關鍵新監測點</strong>：{{PM_NEW_MONITORS}}</li>
      <li><strong>multiple / 估值 / 週期定位風險</strong>：{{PM_VALUATION_RISK}}</li>
      <li><strong>Entry 時機</strong>：{{PM_ENTRY_TIMING}}</li>
    </ul>
    <div class="j-logic">→ PM 級行動：① {{PM_ACTION_1}}；② {{PM_ACTION_2}}；③ {{PM_ACTION_3}}；④ {{PM_ACTION_4}}</div>
  </div>

  <details class="evidence-fold">
    <summary>考證與來源 · 方法論與口徑</summary>
    <div class="fold-body">
      <p><strong>CLAIM TAXONOMY v1</strong>：本 ID 用 4 類 tag：<strong>[F:]</strong> 事實｜<strong>[I:]</strong> 推論（A→B）｜<strong>[X:]</strong> 情境（base/bull/bear）｜<strong>[A:]</strong> 假設。數字以 range / ~xxx；機率用「很可能 / 可能 / 不太可能」。</p>
      <p><strong>單位與口徑</strong>：{{UNIT_GLOSSARY_PROSE}}</p>
      <p><strong>來源結構說明</strong>：{{SOURCE_STRUCTURE_PROSE}}</p>
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S1_TIER}}]</span><a href="{{S1_URL}}">{{S1_TITLE}}</a></li>
        <li><span class="tier">[{{S1B_TIER}}]</span><a href="{{S1B_URL}}">{{S1B_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     2 · KEY DEBATES（分歧前置）
     debate-card 3-5 張；其中至少 1 張必須是「圈外 / 替代威脅」卡（必填，見規格說明）
     ============================================================ -->
<section id="debates" class="section">
  <div class="section-no">Section 2 · Key Debates</div>
  <h2>Key Debates：{{N_DEBATES}} 條與市場的分歧</h2>
  <div class="section-lede">{{DEBATES_LEDE}}</div>

  <div class="debate-card">
    <div class="debate-head"><span class="dt"><span class="dn">Debate 1</span>{{DEBATE_1_TITLE}}</span><span class="badge is-{{DEBATE_1_CONF_CLASS}}">信心：{{DEBATE_1_CONF}}</span></div>
    <div class="debate-row is-market"><div class="dr-k">市場認為</div><div class="dr-v">{{DEBATE_1_MARKET_VIEW}} 🟢 [F: {{DEBATE_1_MARKET_SOURCE}}]。</div></div>
    <div class="debate-row is-view"><div class="dr-k">我們認為</div><div class="dr-v">{{DEBATE_1_OUR_VIEW}} 🔵 [X: {{DEBATE_1_SCENARIO_TAG}}]。<strong>Priced-in</strong>：{{DEBATE_1_PRICED_IN}}。</div></div>
    <div class="debate-row is-signal"><div class="dr-k">判別訊號</div><div class="dr-v">{{DEBATE_1_SIGNAL}}。<span class="path-pos">{{DEBATE_1_SIGNAL_POS}}</span> → {{DEBATE_1_POS_READ}}；<span class="path-neg">{{DEBATE_1_SIGNAL_NEG}}</span> → {{DEBATE_1_NEG_READ}}。⚠ 證偽：{{DEBATE_1_FALSIFIER}}。</div></div>
  </div>

  <div class="debate-card">
    <div class="debate-head"><span class="dt"><span class="dn">Debate 2</span>{{DEBATE_2_TITLE}}</span><span class="badge is-{{DEBATE_2_CONF_CLASS}}">信心：{{DEBATE_2_CONF}}</span></div>
    <div class="debate-row is-market"><div class="dr-k">市場認為</div><div class="dr-v">{{DEBATE_2_MARKET_VIEW}}</div></div>
    <div class="debate-row is-view"><div class="dr-k">我們認為</div><div class="dr-v">{{DEBATE_2_OUR_VIEW}}<strong>Priced-in</strong>：{{DEBATE_2_PRICED_IN}}。</div></div>
    <div class="debate-row is-signal"><div class="dr-k">判別訊號</div><div class="dr-v">{{DEBATE_2_SIGNAL}}</div></div>
  </div>

  <!-- 必填卡：圈外 / 替代威脅（outside-the-lens / substitution threat）。
       每份 ID 至少一張——來自本產業「鏡頭外」的替代技術 / 替代商業模式 / 新進入陣營，
       市場認為 vs 我們認為 vs 判別訊號 同框架；缺此卡 critic 直接抓。
       data-debate="external-threat" 是 Gate 16 的機器檢查標記，不可省。 -->
  <div class="debate-card" data-debate="external-threat">
    <div class="debate-head"><span class="dt"><span class="dn">Debate {{N_DEBATES}}</span>{{DEBATE_OUTSIDE_TITLE}}</span><span class="badge is-{{DEBATE_OUTSIDE_CONF_CLASS}}">信心：{{DEBATE_OUTSIDE_CONF}}</span></div>
    <div class="debate-row is-market"><div class="dr-k">市場認為</div><div class="dr-v">{{DEBATE_OUTSIDE_MARKET_VIEW}}</div></div>
    <div class="debate-row is-view"><div class="dr-k">我們認為</div><div class="dr-v">{{DEBATE_OUTSIDE_OUR_VIEW}}</div></div>
    <div class="debate-row is-signal"><div class="dr-k">判別訊號</div><div class="dr-v">{{DEBATE_OUTSIDE_SIGNALS}}</div></div>
  </div>

  <p><strong>市場最低估的風險</strong>：{{MOST_UNDERPRICED_RISK}}</p>

  <div class="callout is-implication"><span class="co-label">對投資的意義 · Investment Implication</span>{{DEBATES_IMPLICATION}}</div>

  <details class="evidence-fold">
    <summary>考證與來源</summary>
    <div class="fold-body">
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S2_TIER}}]</span><a href="{{S2_URL}}">{{S2_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     3 · 產業機制與供需（exhibit 驅動）
     固定四小節：3.1 需求 / 3.2 供給 / 3.3 技術根 / 3.4 裁決；
     主題需要時可追加 3.x 小節（如供給側新變數），不得刪固定四節
     ============================================================ -->
<section id="mechanics" class="section">
  <div class="section-no">Section 3 · Industry Mechanics</div>
  <h2>產業機制與供需</h2>
  <div class="section-lede">{{MECHANICS_LEDE}}</div>

  <h3>3.1 需求：{{DEMAND_H3_TITLE}}</h3>
  <p><strong>現需</strong>：{{DEMAND_CURRENT_PROSE}}</p>

  <div class="exhibit">
    <div class="exhibit-head">需求三角驗證 · {{DEMAND_TRIANGULATION_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{DEMAND_TRI_COL_1}}</th><th>{{DEMAND_TRI_COL_2}}</th><th>{{DEMAND_TRI_COL_3}}</th></tr></thead>
        <tbody>
          <tr><td>{{DEMAND_TRI_ROW_1}}</td><td class="num">{{DEMAND_TRI_ROW_1_VAL}}</td><td>{{DEMAND_TRI_ROW_1_DIR}}</td></tr>
          <tr><td>{{DEMAND_TRI_ROW_2}}</td><td class="num">{{DEMAND_TRI_ROW_2_VAL}}</td><td>{{DEMAND_TRI_ROW_2_DIR}}</td></tr>
          <tr><td>{{DEMAND_TRI_ROW_3}}</td><td class="num">{{DEMAND_TRI_ROW_3_VAL}}</td><td>{{DEMAND_TRI_ROW_3_DIR}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{DEMAND_TRI_SOURCES}}；InvestMQuest Research 整理</p>
  <p class="exhibit-note">怎麼讀：{{DEMAND_TRI_READ}}。⚠ 對帳結論：{{DEMAND_TRI_RECONCILE}}（top-down vs bottom-up 差 >20% 必解釋缺口）。</p>

  <div class="exhibit">
    <div class="exhibit-head">{{TAM_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>情境</th><th>{{TAM_YEAR_NEAR}}E</th><th>{{TAM_YEAR_FAR}}E</th><th>假設</th><th>推導</th></tr></thead>
        <tbody>
          <tr><td>Base</td><td class="num">{{TAM_BASE_NEAR}}</td><td class="num">{{TAM_BASE_FAR}}</td><td>{{TAM_BASE_ASSUMPTION}}</td><td>推導：{{TAM_BASE_DERIVATION}}</td></tr>
          <tr><td>Bull</td><td class="num">{{TAM_BULL_NEAR}}</td><td class="num">{{TAM_BULL_FAR}}</td><td>{{TAM_BULL_ASSUMPTION}}</td><td>推導：{{TAM_BULL_DERIVATION}}</td></tr>
          <tr><td>Bear</td><td class="num">{{TAM_BEAR_NEAR}}</td><td class="num">{{TAM_BEAR_FAR}}</td><td>{{TAM_BEAR_ASSUMPTION}}</td><td>推導：{{TAM_BEAR_DERIVATION}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research 推導；{{TAM_SOURCES}}</p>
  <p class="exhibit-note">怎麼讀：{{TAM_READ}}</p>

  <div class="judgment-card">
    <div class="j-head">Inference · 需求<span class="badge is-{{DEMAND_JC_CONF_CLASS}}">信心：{{DEMAND_JC_CONF}}</span></div>
    <ul>
      <li>前提：{{DEMAND_JC_PREMISE}}</li>
      <li>推論：{{DEMAND_JC_INFERENCE}}</li>
    </ul>
    <div class="j-logic">→ ⚠ 證偽：{{DEMAND_JC_FALSIFIERS}}</div>
  </div>

  <div class="callout is-risk"><span class="co-label">{{DEMAND_RISK_LABEL}}</span>{{DEMAND_RISK_PROSE}}</div>

  <h3>3.2 供給：{{SUPPLY_H3_TITLE}}</h3>

  <div class="exhibit">
    <div class="exhibit-head">{{SUPPLY_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{SUPPLY_COL_1}}</th><th>{{SUPPLY_COL_2}}</th><th>{{SUPPLY_COL_3}}</th><th>{{SUPPLY_COL_4}}</th></tr></thead>
        <tbody>
          <tr><td>{{SUPPLY_ROW_1}}</td><td class="num">{{SUPPLY_ROW_1_B}}</td><td>{{SUPPLY_ROW_1_C}}</td><td>{{SUPPLY_ROW_1_D}}</td></tr>
          <tr><td>{{SUPPLY_ROW_2}}</td><td class="num">{{SUPPLY_ROW_2_B}}</td><td>{{SUPPLY_ROW_2_C}}</td><td>{{SUPPLY_ROW_2_D}}</td></tr>
          <tr><td>{{SUPPLY_ROW_3}}</td><td class="num">{{SUPPLY_ROW_3_B}}</td><td>{{SUPPLY_ROW_3_C}}</td><td>{{SUPPLY_ROW_3_D}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{SUPPLY_SOURCES}}；InvestMQuest Research 整理。{{SUPPLY_QC18_NOTE}}</p>
  <p class="exhibit-note">怎麼讀：{{SUPPLY_READ}}。<strong>因果機制</strong>：{{SUPPLY_CAUSAL_MECHANISM}}</p>

  <div class="judgment-card">
    <div class="j-head">Inference · 供給<span class="badge is-{{SUPPLY_JC_CONF_CLASS}}">信心：{{SUPPLY_JC_CONF}}</span></div>
    <ul>
      <li>前提：{{SUPPLY_JC_PREMISE}}</li>
      <li>推論：{{SUPPLY_JC_INFERENCE}}</li>
    </ul>
    <div class="j-logic">→ ⚠ 證偽：{{SUPPLY_JC_FALSIFIERS}}</div>
  </div>

  <p><strong>成本曲線</strong>：{{COST_CURVE_PROSE}}（marginal producer 是誰、價格跌到哪 level 誰先停產；結構成長型可省，一句註明理由）。<strong>因果閉合</strong>：{{CAUSAL_CLOSURE_PROSE}}（附錄 A 提出的結構變數在未來 3-5 年是否仍 binding，≥50 字直接回應）。</p>

  <h3>3.3 技術根：{{TECH_H3_TITLE}}</h3>
  <p>技術因果鏈：{{TECH_CAUSAL_CHAIN}}</p>
  <pre class="figure-ascii">
{{TECH_ASCII_FIGURE}}
  </pre>

  <div class="exhibit">
    <div class="exhibit-head">{{KINGMAKER_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>技術</th><th>作用</th><th>{{KINGMAKER_COL_3}}</th></tr></thead>
        <tbody>
          <tr><td>{{KINGMAKER_ROW_1}}</td><td>{{KINGMAKER_ROW_1_B}}</td><td>{{KINGMAKER_ROW_1_C}}</td></tr>
          <tr><td>{{KINGMAKER_ROW_2}}</td><td>{{KINGMAKER_ROW_2_B}}</td><td>{{KINGMAKER_ROW_2_C}}</td></tr>
          <tr><td>{{KINGMAKER_ROW_3}}</td><td>{{KINGMAKER_ROW_3_B}}</td><td>{{KINGMAKER_ROW_3_C}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{KINGMAKER_SOURCES}}；InvestMQuest Research 整理</p>
  <p class="exhibit-note">怎麼讀：{{KINGMAKER_READ}}</p>

  <h3>3.4 裁決：供需裁決與三視野推估</h3>
  <p><strong>資本週期證據</strong>：① capex／折舊比——{{CAPCYCLE_1}}；② ROIC vs WACC——{{CAPCYCLE_2}}；③ 新產能 lead time——{{CAPCYCLE_3}}。{{CAPCYCLE_SYNTHESIS}}（裁決至少引其中 2 項）。</p>

  <div class="exhibit">
    <div class="exhibit-head">三視野 × 三情境推估</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>Horizon</th><th>Base</th><th>Bull</th><th>Bear</th><th>Trigger metric（推導）</th></tr></thead>
        <tbody>
          <tr><td><strong>12M</strong></td><td>{{H12M_BASE}}</td><td>{{H12M_BULL}}</td><td>{{H12M_BEAR}}</td><td>{{H12M_TRIGGER}}</td></tr>
          <tr><td><strong>3Y</strong></td><td>{{H3Y_BASE}}</td><td>{{H3Y_BULL}}</td><td>{{H3Y_BEAR}}</td><td>{{H3Y_TRIGGER}}</td></tr>
          <tr><td><strong>5Y+</strong></td><td>{{H5Y_BASE}}</td><td>{{H5Y_BULL}}</td><td>{{H5Y_BEAR}}</td><td>{{H5Y_TRIGGER}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research 推導；{{HORIZONS_SOURCES}}</p>
  <p class="exhibit-note">怎麼讀：{{HORIZONS_READ}}（trigger 必須可量化、可回溯，禁「demand booms」這種模糊詞）。庫存／訂單指標：{{INVENTORY_ORDER_INDICATORS}}（軟體服務類改 NRR／backlog／RPO 並說明替代理由）。</p>

  <div class="callout is-implication"><span class="co-label">對投資的意義 · Investment Implication</span>{{MECHANICS_IMPLICATION}}</div>

  <details class="evidence-fold">
    <summary>考證與來源 · {{MECHANICS_FOLD_TITLE}}</summary>
    <div class="fold-body">
      <p><strong>{{MECHANICS_FOLD_TOPIC_1}}</strong>。{{MECHANICS_FOLD_PROSE_1}}</p>
      <p><strong>{{MECHANICS_FOLD_TOPIC_2}}</strong>。{{MECHANICS_FOLD_PROSE_2}}</p>
      <p><strong>Bear 情境長什麼樣（情境敘事化）</strong>。{{BEAR_NARRATIVE_PROSE}}</p>
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S3_TIER}}]</span><a href="{{S3_URL}}">{{S3_TITLE}}</a></li>
        <li><span class="tier">[{{S3B_TIER}}]</span><a href="{{S3B_URL}}">{{S3B_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     4 · 估值傳導
     ============================================================ -->
<section id="valuation" class="section">
  <div class="section-no">Section 4 · Valuation</div>
  <h2>產業經濟學與估值傳導</h2>
  <div class="section-lede">{{VALUATION_LEDE}}</div>

  <div class="exhibit">
    <div class="exhibit-head">{{UNIT_ECON_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{UNIT_ECON_COL_1}}</th><th>毛利驅動</th><th>未來 2Y</th><th>抗 commoditization</th></tr></thead>
        <tbody>
          <tr><td>{{UNIT_ECON_ROW_1}}</td><td>{{UNIT_ECON_ROW_1_B}}</td><td>{{UNIT_ECON_ROW_1_C}}</td><td>{{UNIT_ECON_ROW_1_D}}</td></tr>
          <tr><td>{{UNIT_ECON_ROW_2}}</td><td>{{UNIT_ECON_ROW_2_B}}</td><td>{{UNIT_ECON_ROW_2_C}}</td><td>{{UNIT_ECON_ROW_2_D}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{UNIT_ECON_SOURCES}}</p>
  <p class="exhibit-note">怎麼讀：{{UNIT_ECON_READ}}</p>

  <p><strong>估值傳導</strong>：{{VALUATION_PASSTHROUGH_PROSE}}。敏感度錨點：{{VALUATION_SENSITIVITY_ANCHOR}}。</p>

  <div class="callout is-implication"><span class="co-label">對投資的意義 · Investment Implication</span>{{VALUATION_IMPLICATION}}</div>

  <details class="evidence-fold">
    <summary>考證與來源 · {{VALUATION_FOLD_TITLE}}</summary>
    <div class="fold-body">
      <p><strong>{{VALUATION_FOLD_TOPIC}}</strong>。{{VALUATION_FOLD_PROSE}}</p>
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S4_TIER}}]</span><a href="{{S4_URL}}">{{S4_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     5 · 風險與證偽
     ============================================================ -->
<section id="risks" class="section">
  <div class="section-no">Section 5 · Risks &amp; Falsification</div>
  <h2>風險與證偽</h2>
  <div class="section-lede">{{RISKS_LEDE}}</div>

  <h3>5.1 Catalyst timeline</h3>
  <div class="event-line">
    <p><span class="event-date">{{CATALYST_1_DATE}}</span>{{CATALYST_1_EVENT}}。<span class="path-pos">{{CATALYST_1_POS}}</span> → {{CATALYST_1_POS_ACTION}}。<span class="path-neg">{{CATALYST_1_NEG}}</span> → {{CATALYST_1_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_2_DATE}}</span>{{CATALYST_2_EVENT}}。<span class="path-pos">{{CATALYST_2_POS}}</span> → {{CATALYST_2_POS_ACTION}}。<span class="path-neg">{{CATALYST_2_NEG}}</span> → {{CATALYST_2_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_3_DATE}}</span>{{CATALYST_3_EVENT}}。<span class="path-pos">{{CATALYST_3_POS}}</span> → {{CATALYST_3_POS_ACTION}}。<span class="path-neg">{{CATALYST_3_NEG}}</span> → {{CATALYST_3_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_4_DATE}}</span>{{CATALYST_4_EVENT}}。<span class="path-pos">{{CATALYST_4_POS}}</span> → {{CATALYST_4_POS_ACTION}}。<span class="path-neg">{{CATALYST_4_NEG}}</span> → {{CATALYST_4_NEG_ACTION}}。</p>
  </div>

  <h3>5.2 證偽表（kill metrics）</h3>
  <div class="exhibit">
    <div class="exhibit-head">證偽表（kill metrics）</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>Metric</th><th>Base</th><th>Bull</th><th>Bear（作廢）</th><th>時間窗</th></tr></thead>
        <tbody>
          <tr><td>{{KILL_1_METRIC}}</td><td>{{KILL_1_BASE}}</td><td>{{KILL_1_BULL}}</td><td><strong>{{KILL_1_BEAR}}</strong></td><td class="num">{{KILL_1_WINDOW}}</td></tr>
          <tr><td>{{KILL_2_METRIC}}</td><td>{{KILL_2_BASE}}</td><td>{{KILL_2_BULL}}</td><td><strong>{{KILL_2_BEAR}}</strong></td><td class="num">{{KILL_2_WINDOW}}</td></tr>
          <tr><td>{{KILL_3_METRIC}}</td><td>{{KILL_3_BASE}}</td><td>{{KILL_3_BULL}}</td><td><strong>{{KILL_3_BEAR}}</strong></td><td class="num">{{KILL_3_WINDOW}}</td></tr>
          <tr><td>{{KILL_4_METRIC}}</td><td>{{KILL_4_BASE}}</td><td>{{KILL_4_BULL}}</td><td><strong>{{KILL_4_BEAR}}</strong></td><td class="num">{{KILL_4_WINDOW}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research；{{KILL_TABLE_SOURCES}}</p>
  <p class="exhibit-note">怎麼讀：bear 欄即 thesis 作廢點，每條對應下方一條反方；{{KILL_TABLE_READ}}（本表與 id-meta `kill_metrics[]` 同步，餵 position-thesis-monitor）。</p>

  <h3>5.3 Steel-man 反方（最有力的 3 條）</h3>
  <ul>
    <li><strong>反方 1：{{STEELMAN_1_TITLE}}</strong>。路徑：{{STEELMAN_1_PATH}}。證據：{{STEELMAN_1_EVIDENCE}}。證偽窗口：{{STEELMAN_1_WINDOW}}。</li>
    <li><strong>反方 2：{{STEELMAN_2_TITLE}}</strong>。路徑：{{STEELMAN_2_PATH}}。證據：{{STEELMAN_2_EVIDENCE}}。證偽窗口：{{STEELMAN_2_WINDOW}}。</li>
    <li><strong>反方 3：{{STEELMAN_3_TITLE}}</strong>。路徑：{{STEELMAN_3_PATH}}。證據：{{STEELMAN_3_EVIDENCE}}。證偽窗口：{{STEELMAN_3_WINDOW}}。</li>
  </ul>

  <h3>5.4 PM 級監測點</h3>
  <div class="monitor-list">
    <div class="ml-head">PM 級監測點 · 每季檢查，任一轉弱降一級 conviction</div>
    <div class="monitor-item"><div class="monitor-num">1</div><div class="monitor-body">{{MONITOR_1}}</div></div>
    <div class="monitor-item"><div class="monitor-num">2</div><div class="monitor-body">{{MONITOR_2}}</div></div>
    <div class="monitor-item"><div class="monitor-num">3</div><div class="monitor-body">{{MONITOR_3}}</div></div>
    <div class="monitor-item"><div class="monitor-num">4</div><div class="monitor-body">{{MONITOR_4}}</div></div>
  </div>

  <div class="callout is-implication"><span class="co-label">對投資的意義 · Investment Implication</span>{{RISKS_IMPLICATION}}</div>

  <details class="evidence-fold">
    <summary>考證與來源</summary>
    <div class="fold-body">
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S5_TIER}}]</span><a href="{{S5_URL}}">{{S5_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     6 · 個股含意
     ============================================================ -->
<section id="stocks" class="section">
  <div class="section-no">Section 6 · Stock Implications</div>
  <h2>個股含意與 conviction tier</h2>
  <div class="section-lede">{{STOCKS_LEDE}}（本框架只輸出「特徵」與「分類」，買哪一檔由個股 DD 系統與 Pure MA 訊號決定）。</div>
  <p>本 ID 對應個股（stock-analyst 自動讀本表 + id-meta related_tickers）：</p>

  <div class="exhibit">
    <div class="exhibit-head">關聯個股 · 🔴 核心｜🟡 swing｜🟢 邊緣（{{TICKER_TABLE_TIME_SCOPE}}）</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>Ticker</th><th>深度</th><th>受益 / 受害</th><th>角色</th><th>DD</th></tr></thead>
        <tbody>
          <tr><td><strong>{{TICKER_1}}</strong></td><td>{{TICKER_1_TIER}}</td><td>{{TICKER_1_DIRECTION}}</td><td>{{TICKER_1_ROLE_PROSE}}</td><td>{{TICKER_1_DD_LINK}}</td></tr>
          <tr><td><strong>{{TICKER_2}}</strong></td><td>{{TICKER_2_TIER}}</td><td>{{TICKER_2_DIRECTION}}</td><td>{{TICKER_2_ROLE_PROSE}}</td><td>{{TICKER_2_DD_LINK}}</td></tr>
          <tr><td><strong>{{TICKER_3}}</strong></td><td>{{TICKER_3_TIER}}</td><td>{{TICKER_3_DIRECTION}}</td><td>{{TICKER_3_ROLE_PROSE}}</td><td>{{TICKER_3_DD_LINK}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research；{{TICKER_TABLE_SOURCES}}</p>

  <div class="tier-list">
    <div class="tier-row">
      <div class="tier-name"><span class="tier-badge is-core">CORE 🔴</span><h4>{{CORE_TICKER_1}}</h4></div>
      <div class="tier-detail">{{CORE_TICKER_1_NARRATIVE}}是「{{CORE_TICKER_1_TRAIT}}」特徵。<span class="conv">conviction：{{CORE_TICKER_1_CONV}}</span></div>
    </div>
    <div class="tier-row">
      <div class="tier-name"><span class="tier-badge is-swing">SWING 🟡</span><h4>{{SWING_TICKERS}}</h4></div>
      <div class="tier-detail">{{SWING_TICKERS_NARRATIVE}}是「{{SWING_TRAIT}}」特徵。<span class="conv">conviction：{{SWING_CONV}}</span></div>
    </div>
    <div class="tier-row">
      <div class="tier-name"><span class="tier-badge is-edge">EDGE 🟢</span><h4>{{EDGE_TICKERS}}</h4></div>
      <div class="tier-detail">{{EDGE_TICKERS_NARRATIVE}}是「{{EDGE_TRAIT}}」特徵。<span class="conv">conviction：{{EDGE_CONV}}</span></div>
    </div>
  </div>

  <p><strong>估值面總結</strong>：{{STOCKS_VALUATION_SUMMARY}}</p>

  <div class="callout is-implication"><span class="co-label">對投資的意義 · Investment Implication</span>{{STOCKS_IMPLICATION}}買賣由個股 DD + Pure MA 系統決定，本表只給特徵分類、非買入推薦。</div>

  <details class="evidence-fold">
    <summary>考證與來源 · 非顯而易見受益者</summary>
    <div class="fold-body">
      <p><strong>非顯而易見受益者</strong>：① {{NONOBVIOUS_1}}；② {{NONOBVIOUS_2}}。</p>
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S6_TIER}}]</span><a href="{{S6_URL}}">{{S6_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============================================================
     附錄 · 背景與考證（預設折疊）
     ============================================================ -->
<section id="appendix" class="section">
  <div class="section-no">Appendix · Background</div>
  <h2>附錄：背景與考證</h2>
  <div class="section-lede">產業白話定義、歷史脈絡與歷史類比考證——支撐正文判斷的背景層，預設收合。</div>

  <details class="evidence-fold">
    <summary>附錄 A · 產業白話定義與歷史脈絡</summary>
    <div class="fold-body">
      <p>{{APPENDIX_A_PLAIN_DEFINITION}}</p>
      <p><strong>白話開場</strong>：{{APPENDIX_A_PLAIN_OPENING}}（第一段不准出現未解釋行話；術語首現括號內或破折號後一行白話）。</p>
      <p><strong>邊界界定</strong>：{{APPENDIX_A_SCOPE}}（in-scope vs out-of-scope、為何這樣切、灰色地帶在哪、姊妹母題分工）。</p>
      <p>第一次轉折：<mark class="time">{{TURN_1_DATE}}</mark> {{TURN_1_EVENT}}；第二次：<mark class="time">{{TURN_2_DATE}}</mark> {{TURN_2_EVENT}}；第三次：<mark class="time">{{TURN_3_DATE}}</mark> {{TURN_3_EVENT}}（每個轉折強制具體日期＋≥1 量化錨點）。</p>
    </div>
  </details>

  <details class="evidence-fold">
    <summary>附錄 B · 歷史類比：{{APPENDIX_B_TITLE}}</summary>
    <div class="fold-body">
      <p><strong>歷史類比</strong>。① <strong>{{ANALOGY_1_NAME}}</strong>（{{ANALOGY_1_VERDICT}}）：{{ANALOGY_1_PROSE}}；② <strong>{{ANALOGY_2_NAME}}</strong>（{{ANALOGY_2_VERDICT}}）：{{ANALOGY_2_PROSE}}（每個類比：年份＋主角＋當年關鍵數據＋多頭／空頭錯在哪＋本次量化差異）。</p>

      <div class="exhibit">
        <div class="exhibit-head">{{ANALOGY_EXHIBIT_TITLE}}</div>
        <div class="exhibit-body">
          <table>
            <thead><tr><th>先例</th><th>{{ANALOGY_COL_2}}</th><th>{{ANALOGY_COL_3}}</th><th>贏家</th></tr></thead>
            <tbody>
              <tr><td>{{ANALOGY_ROW_1}}</td><td>{{ANALOGY_ROW_1_B}}</td><td>{{ANALOGY_ROW_1_C}}</td><td>{{ANALOGY_ROW_1_D}}</td></tr>
              <tr><td>{{ANALOGY_ROW_2}}</td><td>{{ANALOGY_ROW_2_B}}</td><td>{{ANALOGY_ROW_2_C}}</td><td>{{ANALOGY_ROW_2_D}}</td></tr>
              <tr><td>{{THEME_ROW}}</td><td class="num">{{THEME_ROW_B}}</td><td>{{THEME_ROW_C}}</td><td>{{THEME_ROW_D}}</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <p class="exhibit-source">資料來源：{{ANALOGY_SOURCES}}；InvestMQuest Research 整理</p>
      <p class="exhibit-note">怎麼讀：{{ANALOGY_READ}}</p>

      <p><em>歷史的投資含義</em>：{{ANALOGY_IMPLICATION}}</p>
      <span class="src-label">本節參考來源</span>
      <ol class="src-list">
        <li><span class="tier">[{{S7_TIER}}]</span><a href="{{S7_URL}}">{{S7_TITLE}}</a></li>
      </ol>
    </div>
  </details>
</section>

<!-- ============ CLOSING ============ -->
<div class="pull-quote">
  <div class="pq-label">The One Line</div>
  <p>{{ONE_LINE_CLOSER}}</p>
</div>

<section class="section" style="margin-top:24px">
  <h3 style="margin-top:0">這份報告刻意不做的三件事</h3>
  <ol>
    <li>不告訴你哪一檔該買——tier 是「特徵的代表案例」，買賣由你的個股 DD 與 Pure MA 系統決定，本報告非買入推薦。</li>
    <li>{{NOT_DOING_2}}</li>
    <li>{{NOT_DOING_3}}</li>
  </ol>
</section>

<div class="disclosures">
  <div class="dh">Disclosures &amp; Important Information</div>
  本報告由 InvestMQuest Research 內部買方研究流程產生，僅供研究與投資決策參考，不構成要約、招攬或個別投資建議。資料來源含公司公告與第三方研究（{{DISCLOSURE_SOURCE_LIST}}）；前瞻性陳述（base/bull/bear）含不確定性。{{DISCLOSURE_EXTRA}}持倉揭露：本研究流程關聯帳戶可能持有文中標的部位。個股買賣由個股 DD 與系統訊號決定，本報告 tier 為產業特徵分類、非買入推薦。© {{YEAR}} InvestMQuest Research.
</div>
<div class="report-colophon">
  產業深度報告 · industry-analyst {{SKILL_VERSION}} · 主題：{{THEME}} · 發布日 {{PUBLISH_DATE}}<br>
  <a href="/research/">回研究首頁</a> · <a href="/id/">所有產業報告</a>
</div>

</div><!-- /report-sheet -->

<a class="back-top" href="#top">↑ TOP</a>

</body>
</html>
```

---

## §0-§9 舊資產 → 新八段映射表

v2.x 兩份制（完整版 §0-§9 ＋ 精煉版 PART I-VI）的每個資產在新架構的落點。**沒有內容被刪除，只有重排與降級**（背景後置為折疊）。

| 新段（錨點） | 舊 §0-§9 來源 |
|---|---|
| `summary`（Page-1 摘要層） | §0 決策摘要層：INVESTMENT SUMMARY 三句話 → view-grid（NOW/NEXT/ACTION）；6-box TL;DR → rating strip ＋「關鍵數據一覽」Exhibit；精煉版 abstract → Key Points bullets；legacy cross-link → crosslink |
| `thesis`（1 Investment Thesis） | §0 KEY CALL → key-call；§0 一句話 thesis box → thesis-box；§0 PM Implication 綠卡 → judgment-card；**§5 供需裁決 bridge ＋ 投資時鐘段前置到此**（裁決結論先行，推導留 3.4）；§0 claim taxonomy banner ＋ unit glossary → 本節 evidence-fold |
| `debates`（2 Key Debates） | §7 Non-Consensus 分歧 judgment-card → debate-card 三列框架（市場認為／我們認為／判別訊號）；§7 priced-in 檢驗併入「我們認為」列；§7「市場最低估的風險」保留；**§7 steel-man 反方移至 `risks` 5.3**（sell-side 慣例反方論證放 Risks，與證偽表逐條對應） |
| `mechanics` 3.1 需求 | §4 需求側全部：現需段＋需求三角驗證表＋TAM 三情境表（含推導鏈）＋需求 judgment-card |
| `mechanics` 3.2 供給 | §3 供給側全部：玩家矩陣／利潤池表＋供給 judgment-card＋成本曲線段＋因果閉合段 |
| `mechanics` 3.3 技術根 | §2 技術成熟度：因果鏈段＋S 曲線（figure-ascii）＋kingmaker 表 |
| `mechanics` 3.4 裁決 | §5 供需裁決推導層：資本週期證據段＋三視野 × 三情境表＋庫存／訂單指標（併入三視野表註） |
| `valuation`（4 估值傳導） | §6 全文：unit economics 表＋估值傳導段＋敏感度錨點 |
| `risks`（5 風險與證偽） | §8 catalyst timeline（event-line）＋證偽表；§7 steel-man 反方（移入）；§0 PM 級監測點 monitor → 5.4 monitor-list |
| `stocks`（6 個股含意） | §9 關聯個股表＋精煉版 tier-list 逐檔敘述＋估值面總結；非顯而易見受益者段收本節 evidence-fold |
| `appendix`（附錄） | **§1 全部降級為折疊**：附錄 A＝白話定義＋白話開場＋邊界界定＋歷史轉折；附錄 B＝歷史類比＋歷史先例表＋cycle 統計（若產業有 ≥2 輪 cycle，cycle 統計表放附錄 B；無 cycle 註明） |
| 收尾 | 精煉版 keystone → pull-quote（The One Line）＋「刻意不做的三件事」＋ disclosures ＋ colophon |
| 不再保留 | 精煉版 footnotes（Selected Sources 總表——與逐節 evidence-fold 來源全集重複）；id-secnav（被 toc-bar 取代）；精煉版 scenario-set／timeline（與三視野 × 三情境表逐格重複，單一 Exhibit 承載） |

## Key Debates 硬規則

- debate-card **3-5 張**；每張三列固定：`is-market`（市場認為，引 ≥1 T3 共識源）／`is-view`（我們認為，含 **Priced-in 檢驗**）／`is-signal`（判別訊號，可量化＋雙路徑＋⚠ 證偽條件）。
- **≥1 張「圈外／替代威脅」卡為必填**——來自本產業鏡頭外的替代技術、替代商業模式或新進入陣營（範例：AI 推論 ID 的「中國 open-weight 模型」卡）。該卡最外層 div 必帶 `data-debate="external-threat"`（**Gate 16 機器檢查標記**）。缺此卡 critic（id-review）直接抓。
- 分歧對但已 priced → 在「我們認為」列標「不可操作」。

## 附錄折疊收什麼

正文閱讀線＝決策與論證；證據層全收 `<details class="evidence-fold">`（預設收合）：

1. **thesis fold**：claim taxonomy、單位與口徑、來源結構說明＋§0 級來源。
2. **mechanics fold**：深機制考證段（如死亡螺旋機制、成本崩跌分解、二階效應）＋ **bear 情境敘事化**（劇本怎麼走、領先訊號）＋ 3.1-3.4 全部來源。
3. **valuation fold**：錯誤定價機制全文＋來源。
4. **debates / risks / stocks fold**：各節來源清單（stocks 另收非顯而易見受益者段）。
5. **附錄 A / B**：白話定義與歷史脈絡、歷史類比全部——依「背景後置」原則整節降級為折疊。

## Exhibit 編號與資料來源行規則

- Exhibit 編號用 **CSS counter 自動編號**（`.exhibit` 依 DOM 順序，含附錄內 Exhibit）——**不要手寫「Exhibit N」**，插刪表格編號自動重排。
- 每張 `.exhibit` 後**必跟** `<p class="exhibit-source">資料來源：…</p>`（來源自該節 evidence-fold 對應條目提上，含機構名＋as-of；純自算寫「InvestMQuest Research 推導」）。
- 表格需判讀時再加 `<p class="exhibit-note">怎麼讀：…</p>`（1-2 句，第 1 句表內事實、第 2 句對判斷的意義）。
- 無 source 的 % 改定性（主導／均勢／次要）——QC-18 沿用；禁 Q×4 推估——QC-17 沿用。

## 站內 nav 注入區塊照抄規則

`<body>` 開頭的 canonical site header（`<style id="imq-nav-style">` ＋ `<header class="imq-nav-root">` ＋ dropdown `<script>`）由 `scripts/site_nav.py full_nav_block('research','id')` 生成——產檔時**現跑現貼整塊**（取代 `{{SITE_NAV_FULL_BLOCK}}` 佔位符），不要手改、不要憑記憶重寫；site_nav.py 變更後既有頁面由 re-inject 流程重生。頁內 sticky TOC（`.toc-bar`）offset 依 `--nav-h:45px`，行動版轉 static 迴避重疊。

## 其他硬規則（v2.x 沿用）

- 中文內容標點一律**全形**（，。：；「」）；commit 前 `python3 scripts/qc.py`。
- 個股非推薦：`stocks` 節 lede、implication callout 與「刻意不做的三件事」第 1 條必含「特徵／分類、買賣由個股 DD ＋ 系統決定、非買入推薦」字句。
- claim tag（[F:]/[I:]/[X:]/[A:]）與 🟢🔵 語意標記沿用；數字 range / ~xxx；機率用詞彙級非百分比。
- Emoji 僅語意用途（🔴🟡🟢 depth、🟢🔵 claim tag），禁裝飾性 emoji——與全站專業化規範一致。
- light-only（`color-scheme:light` ＋ meta 宣告）；`@media print` 隱藏 nav／TOC／back-top。
- 版號一律 `{{SKILL_VERSION}}`（隨 SKILL.md frontmatter），出現在 `<meta name="id-skill-version">`、id-meta JSON `skill_version`、colophon 三處，三處同值。
