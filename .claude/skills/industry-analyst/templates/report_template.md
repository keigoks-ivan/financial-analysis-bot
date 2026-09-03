# 產業深度報告 HTML Template v4 — 八段錨點・白話正文・紀律進折疊

單檔 `ID_{Theme}_{YYYYMMDD}.html`，取代 v3 inline `<style>`（外掛 `docs/assets/id-v4.css`，省每檔 ~19KB）。閱讀線＝外資報告動線：Page-1 決策卡 → Thesis → Key Debates → 產業機制與供需 → 估值 → 風險證偽 → 個股 → 附錄；**正文全白話，claim tag／T 級／版本戳一律收進折疊層或 `<meta>`，不上主閱讀線**。品質由必交決策物 D1–D13 把關（見 SKILL.md），不是字數。

## 檔名規則

`docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`

- Theme_CamelCase 範例：GlassSubstrate / HBM_Supercycle / AIASIC_vs_GPU / GLP1_Landscape / EUV_NextGen
- 單檔即全部，不產 `_full.html`。

## id-meta 放置規則（`<head>` 內，schema 不變）

- `<meta name="id-skill-version | id-theme | id-publish-date">` 三標 ＋ `<script id="id-meta" type="application/json">` JSON block，一律放本檔 `<head>` 內。單檔＝SSOT，索引／screener／validator 全認這份。
- 欄位 schema 沿用（`validate_id_meta.py` 強制）：`now_state` / `future_state` / `action` / `sd_verdict` / `clock_phase` / `conviction` / `priced_in` / `kill_metrics[]` / `demand_5y_multiple` / `related_tickers[]` 等，v4 **零改動**。
- 版號戳一律隨 SKILL.md frontmatter，template 內以 `{{SKILL_VERSION}}` 佔位，不得寫死。**版本號只出現在 `<meta name="id-skill-version">` 與頁尾 colophon 一行**，正文不印 `skill_version`／`sub_group`／`Method:` 這類機器欄字面。

## 章節機器錨點（固定，白話主標題＋英文小字）

| 錨點 | 白話主標題 | 英文小字 | 這段唯一的工作 | 可見字目標 |
|---|---|---|---|---:|
| `summary` | 一頁看完 | Page-1 | 決策卡：燈號五格＋三句話＋KEY CALL＋三條帶現值的 kill＋PM 行動（四個） | 700–1,000 |
| `thesis` | 核心判斷 | Investment Thesis | thesis 完整講一次；其餘章節只准「見 §1」 | 1,200–1,800 |
| `debates` | 市場哪裡看錯 | Key Debates | 3–5 張分歧卡（≥1 張替代威脅），steel-man 住卡內 | 2,000–2,800 |
| `mechanics` | 機制與供需 | Industry Mechanics | 3.1 需求／3.2 供給／3.3 為什麼是現在／3.4 裁決，固定四節 | 4,000–5,500 |
| `valuation` | 現在貴不貴 | Valuation | unit economics＋priced-in 位置，校準點名的軸集中一處 | 1,200–1,800 |
| `risks` | 我怎麼知道我錯了 | Risks & Falsification | 一張 kill 表＋催化劑雙路徑；不另列監測點 | 900–1,300 |
| `stocks` | 誰受影響 | Stock Implications | 🔴🟡🟢 表＋非顯而易見受益者＋營運槓桿最大者；不放估值面總結 | 800–1,200 |
| `appendix` | 背景、歷史與來源 | Appendix | 白話定義、歷史轉折、類比先例、來源總表 | 1,200–2,000 |

主題需要額外機制小節（如某輪供給側新變數）加在 `mechanics` 內為 3.5 追加 `h3`，**不得**取代上表四個固定小節、不得新增頂層錨點。

## rating strip ↔ id-meta 五格對應（白話主字＋英文小字，全部鏡像同步）

第一頁燈號**只有五格**（v3 的 Sector View／Focus Names／避開特徵三格散文欄退役，併入 KEY CALL／debates 散文），每格 `<span data-field="..." data-value="{{...}}">白話</span>`，值必須與 `<head>` id-meta JSON **一字不差**同步：

| 格（白話） | `data-field` | 顯示字（白話對照，四選一或帶值） |
|---|---|---|
| 供需 | `sd_verdict` | 短缺／平衡／過剩／分裂 |
| 時鐘 | `clock_phase` | 擴張初段／擴張中段／高原／收縮（對應 Phase I–IV） |
| 信心 | `conviction` | 高／中／低 |
| 已定價 | `priced_in` | 還沒反映／部分反映／大多反映 |
| 5 年需求倍數 | `demand_5y_multiple` | ×N |

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
  "theme": "{{THEME_EN}}", "skill_version": "{{SKILL_VERSION}}", "id_version": "{{ID_VERSION}}",
  "publish_date": "{{PUBLISH_DATE}}", "thesis_type": "{{THESIS_TYPE}}", "ai_exposure": "{{AI_EXPOSURE}}",
  "oneliner": "{{ONELINER}}", "now_state": "{{NOW_STATE}}", "future_state": "{{FUTURE_STATE}}", "action": "{{ACTION}}",
  "related_tickers": [
    {"ticker": "{{TICKER_1}}", "role": "{{TICKER_1_ROLE}}", "depth": "{{TICKER_1_DEPTH}}", "beneficiary": true, "mcap_bucket": "{{TICKER_1_MCAP}}"}
  ],
  "sd_verdict": "{{SD_VERDICT}}", "clock_phase": "{{CLOCK_PHASE}}", "conviction": "{{CONVICTION}}", "priced_in": "{{PRICED_IN}}",
  "kill_metrics": [
    {"metric": "{{KILL_METRIC_1}}", "bear_threshold": "{{KILL_METRIC_1_BEAR}}", "window": "{{KILL_METRIC_1_WINDOW}}"}
  ],
  "demand_5y_multiple": {{DEMAND_5Y_MULTIPLE}}, "tam_usd_2030": {{TAM_USD_2030}}, "cagr_pct_5y": {{CAGR_PCT_5Y}},
  "growth_phase": "{{GROWTH_PHASE}}", "value_chain_position": "{{VALUE_CHAIN_POSITION}}", "industry_structure": "{{INDUSTRY_STRUCTURE}}",
  "quality_tier": "{{QUALITY_TIER}}", "mega": "{{MEGA}}", "sub_group": "{{SUB_GROUP}}", "sister_ids": ["{{SISTER_ID_1}}"],
  "sections_refreshed": {"technical": "{{PUBLISH_DATE}}", "market": "{{PUBLISH_DATE}}", "judgment": "{{PUBLISH_DATE}}"}
}
</script>

<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Noto+Serif+TC:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/id-v4.css">
</head>
<body id="top">
<!-- canonical site header：現跑現貼 site_nav.py full_nav_block('research','id') 輸出，取代此佔位符；規則見下方「站內 nav 注入區塊照抄規則」 -->
{{SITE_NAV_FULL_BLOCK}}

<div class="report-sheet">

<!-- PAGE 1 · 一頁看完（決策卡，不是摘要） -->
<header id="summary" class="masthead" style="scroll-margin-top:96px">
  <div class="masthead-strip">
    <span><span class="brand">InvestMQuest Research</span>&nbsp;&nbsp;·&nbsp;&nbsp;產業深度研究</span>
    <span>{{SECTOR_LABEL}}&nbsp;&nbsp;·&nbsp;&nbsp;{{DATE_CITY_LINE}}</span>
  </div>
  <div class="report-kicker">產業深度報告<small>Industry Deep Report</small></div>
  <h1 class="report-title">{{TITLE_MAIN}}<em>{{TITLE_EM}}</em>{{TITLE_TAIL}}</h1>
  <p class="report-deck">{{DECK}}</p>
  <div class="report-byline">
    <span>發布日 {{PUBLISH_DATE}} ｜ 涵蓋股票 {{N_TICKERS}} 檔</span>
    <span class="data-window" data-asof="{{DATA_ASOF}}">資料截至 {{DATA_ASOF}}</span>
  </div>

  <!-- rating strip：五格＝id-meta 五欄機器鏡像，值必須與 head 內 id-meta JSON 一字不差同步 -->
  <div class="rating-strip">
    <div class="rating-cell"><span class="k">供需<small>Supply/Demand</small></span><span class="v" data-field="sd_verdict" data-value="{{SD_VERDICT}}">{{SD_VERDICT_DISPLAY}}</span><span class="s">{{SD_VERDICT_NOTE}}</span></div>
    <div class="rating-cell"><span class="k">時鐘<small>Clock Phase</small></span><span class="v" data-field="clock_phase" data-value="{{CLOCK_PHASE}}">{{CLOCK_PHASE_DISPLAY}}</span><span class="s">Phase {{CLOCK_PHASE}} ｜ {{CLOCK_PHASE_NOTE}}</span></div>
    <div class="rating-cell"><span class="k">信心<small>Conviction</small></span><span class="v" data-field="conviction" data-value="{{CONVICTION}}">{{CONVICTION_DISPLAY}}</span><span class="s">{{CONVICTION_NOTE}}</span></div>
    <div class="rating-cell"><span class="k">已定價<small>Priced-in</small></span><span class="v" data-field="priced_in" data-value="{{PRICED_IN}}">{{PRICED_IN_DISPLAY}}</span><span class="s">{{PRICED_IN_NOTE}}</span></div>
    <div class="rating-cell"><span class="k">5 年需求倍數<small>Demand 5Y Multiple</small></span><span class="v" data-field="demand_5y_multiple" data-value="{{DEMAND_5Y_MULTIPLE}}">×{{DEMAND_5Y_MULTIPLE}}</span><span class="s">{{DEMAND_MULTIPLE_SCOPE}}</span></div>
  </div>

  <div class="key-call">
    <div class="kc-label">一句話結論<small>Key Call</small></div>
    <p>{{KEY_CALL_PROSE}}</p>
  </div>

  <div class="view-grid">
    <div class="view-card is-now"><div class="view-tag">現在</div><p>{{NOW_STATE_PROSE}}</p></div>
    <div class="view-card is-next"><div class="view-tag">未來</div><p>{{FUTURE_STATE_PROSE}}</p></div>
    <div class="view-card is-act"><div class="view-tag">怎麼做</div><p>{{ACTION_PROSE}}</p></div>
  </div>

  <div class="section-no">三條要盯的否證指標</div>
  <ul class="kill-brief">
    <li><strong>{{KILLBRIEF_1_METRIC}}</strong>　現值 {{KILLBRIEF_1_NOW}}（{{KILLBRIEF_1_ASOF}}）→ 破 {{KILLBRIEF_1_BEAR}} 論點作廢</li>
    <li><strong>{{KILLBRIEF_2_METRIC}}</strong>　現值 {{KILLBRIEF_2_NOW}}（{{KILLBRIEF_2_ASOF}}）→ 破 {{KILLBRIEF_2_BEAR}} 論點作廢</li>
    <li><strong>{{KILLBRIEF_3_METRIC}}</strong>　現值 {{KILLBRIEF_3_NOW}}（{{KILLBRIEF_3_ASOF}}）→ 破 {{KILLBRIEF_3_BEAR}} 論點作廢</li>
  </ul>

  <!-- judgment-card：全檔恰一次，只在這裡出現 -->
  <div class="judgment-card">
    <div class="j-head">怎麼做<small>PM Action</small></div>
    <ul>
      <li>① {{PM_ACTION_1}}</li>
      <li>② {{PM_ACTION_2}}</li>
      <li>③ {{PM_ACTION_3}}</li>
      <li>④ {{PM_ACTION_4}}</li>
    </ul>
  </div>

  <div class="crosslink">
    母題與姊妹報告：{{CROSSLINK_INTRO}}<a href="/id/{{SISTER_ID_1}}">{{SISTER_ID_1_TITLE}}</a>（{{SISTER_ID_1_SCOPE}}）
  </div>
</header>

<!-- sticky TOC，錨點固定不得改名 -->
<nav class="toc-bar" aria-label="section navigation">
  <a href="#summary">一頁看完</a><a href="#thesis">1 核心判斷</a><a href="#debates">2 市場哪裡看錯</a><a href="#mechanics">3 機制與供需</a><a href="#valuation">4 現在貴不貴</a><a href="#risks">5 我怎麼知道錯了</a><a href="#stocks">6 誰受影響</a><a href="#appendix">附錄</a>
</nav>

<!-- 1 · 核心判斷（thesis 只在這裡完整講一次；其餘章節見 §1） -->
<section id="thesis" class="section">
  <div class="section-no">Section 1</div>
  <h2>核心判斷<small>Investment Thesis</small></h2>
  <div class="section-lede">{{THESIS_LEDE}}</div>

  <p>{{THESIS_PARA_1}}</p>
  <p>{{THESIS_PARA_2}}</p>
  <p><strong>供需怎麼判</strong>：{{SD_VERDICT_PARA}}</p>
  <p><strong>投資時鐘</strong>：現在處於{{CLOCK_PHASE_DISPLAY}}（Phase {{CLOCK_PHASE}}）。換相的兩個條件與資本週期證據見 §3.4。</p>

  <div class="thesis-box">
    <span class="label">一句話講完</span><br>
    <strong>{{ONELINER_PROSE}}</strong>
  </div>

  <div class="exhibit">
    <div class="exhibit-head">{{THESIS_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{THESIS_EXHIBIT_COL_1}}</th><th>{{THESIS_EXHIBIT_COL_2}}</th><th>{{THESIS_EXHIBIT_COL_3}}</th></tr></thead>
        <tbody>
          <tr><td>{{THESIS_EXHIBIT_ROW_1}}</td><td class="num">{{THESIS_EXHIBIT_ROW_1_B}}</td><td>{{THESIS_EXHIBIT_ROW_1_C}}</td></tr>
          <tr><td>{{THESIS_EXHIBIT_ROW_2}}</td><td class="num">{{THESIS_EXHIBIT_ROW_2_B}}</td><td>{{THESIS_EXHIBIT_ROW_2_C}}</td></tr>
          <!-- 列數依承重內容調整，複製本列增列 -->
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{THESIS_EXHIBIT_SOURCES}}［#{{THESIS_EXHIBIT_CITE}}］</p>

  <details class="evidence-fold">
    <summary>推導與考證</summary>
    <div class="fold-body">
      <p><span class="derive">推導：{{THESIS_DERIVATION}}</span></p>
      <p>{{THESIS_FOLD_PROSE}} 🔵 [X: base {{THESIS_BASE_CASE}}；bull {{THESIS_BULL_CASE}}；bear {{THESIS_BEAR_CASE}}]</p>
    </div>
  </details>
</section>

<!-- 2 · 市場哪裡看錯（3 張卡骨架，第 3 張帶 external-threat； 3-5 張，需要更多張複製 debate-card 區塊即可） -->
<section id="debates" class="section">
  <div class="section-no">Section 2</div>
  <h2>市場哪裡看錯<small>Key Debates</small></h2>
  <div class="section-lede">{{DEBATES_LEDE}}</div>

  <div class="debate-card">
    <div class="debate-head"><span class="dt"><span class="dn">分歧 1</span>{{DEBATE_1_TITLE}}</span><span class="badge is-{{DEBATE_1_CONF_CLASS}}">信心：{{DEBATE_1_CONF}}</span></div>
    <div class="debate-row is-market"><div class="dr-k">市場最強版本</div><div class="dr-v">{{DEBATE_1_MARKET_VIEW}}</div></div>
    <div class="debate-row is-view"><div class="dr-k">我們認為</div><div class="dr-v">{{DEBATE_1_OUR_VIEW}}已反映：{{DEBATE_1_PRICED_IN}}。</div></div>
    <div class="debate-row is-signal"><div class="dr-k">看什麼分勝負</div><div class="dr-v"><span class="path-pos">{{DEBATE_1_SIGNAL_POS}}</span> → {{DEBATE_1_POS_READ}}；<span class="path-neg">{{DEBATE_1_SIGNAL_NEG}}</span> → {{DEBATE_1_NEG_READ}}。⚠ {{DEBATE_1_FALSIFIER}}。</div></div>
  </div>

  <!-- 分歧 2 起：複製上一張 debate-card 區塊，重新編號 DEBATE_N 與 dn 顯示序號；3-5 張，最後一張帶 external-threat -->

  <!-- 必填：圈外／替代威脅卡，見下方「Key Debates 硬規則」 -->
  <div class="debate-card" data-debate="external-threat">
    <div class="debate-head"><span class="dt"><span class="dn">分歧 3</span>{{DEBATE_OUTSIDE_TITLE}}</span><span class="badge is-{{DEBATE_OUTSIDE_CONF_CLASS}}">信心：{{DEBATE_OUTSIDE_CONF}}</span></div>
    <div class="debate-row is-market"><div class="dr-k">市場最強版本</div><div class="dr-v">{{DEBATE_OUTSIDE_MARKET_VIEW}}</div></div>
    <div class="debate-row is-view"><div class="dr-k">我們認為</div><div class="dr-v">{{DEBATE_OUTSIDE_OUR_VIEW}}已反映：{{DEBATE_OUTSIDE_PRICED_IN}}。</div></div>
    <div class="debate-row is-signal"><div class="dr-k">看什麼分勝負</div><div class="dr-v"><span class="path-pos">{{DEBATE_OUTSIDE_SIGNAL_POS}}</span> → {{DEBATE_OUTSIDE_POS_READ}}；<span class="path-neg">{{DEBATE_OUTSIDE_SIGNAL_NEG}}</span> → {{DEBATE_OUTSIDE_NEG_READ}}。⚠ {{DEBATE_OUTSIDE_FALSIFIER}}。</div></div>
  </div>

  <p><strong>市場最低估的風險</strong>：{{MOST_UNDERPRICED_RISK}}</p>

  <div class="callout is-implication"><span class="co-label">對投資的意義</span>{{DEBATES_IMPLICATION}}</div>

  <details class="evidence-fold">
    <summary>推導與考證</summary>
    <div class="fold-body">
      <p><span class="derive">推導：{{DEBATES_DERIVATION}}</span></p>
      <p>{{DEBATES_FOLD_PROSE}} 🟢 [F: {{DEBATES_FOLD_FACT}}]</p>
    </div>
  </details>
</section>

<!-- 3 · 機制與供需（固定四小節：3.1 需求／3.2 供給／ 3.3 為什麼是現在／3.4 裁決；主題需要時可追加 3.5，不得刪固定四節） -->
<section id="mechanics" class="section">
  <div class="section-no">Section 3</div>
  <h2>機制與供需<small>Industry Mechanics</small></h2>
  <div class="section-lede">{{MECHANICS_LEDE}}</div>

  <h3>3.1 需求：{{DEMAND_H3_TITLE}}</h3>
  <p>{{DEMAND_CURRENT_PROSE}}</p>

  <div class="exhibit">
    <div class="exhibit-head">需求三角對帳<small>{{DEMAND_TRIANGULATION_TITLE}}</small></div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{DEMAND_TRI_COL_1}}</th><th>{{DEMAND_TRI_COL_2}}</th><th>{{DEMAND_TRI_COL_3}}</th></tr></thead>
        <tbody>
          <tr><td>{{DEMAND_TRI_ROW_1}}</td><td class="num">{{DEMAND_TRI_ROW_1_VAL}}</td><td>{{DEMAND_TRI_ROW_1_DIR}}</td></tr>
          <!-- 列數依需求彈性調整（通常 2-3 列），複製本列增列 -->
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{DEMAND_TRI_SOURCES}}［#{{DEMAND_TRI_CITE}}］</p>
  <p class="exhibit-note"><span class="derive">推導：{{DEMAND_TRI_RECONCILE}}</span>（上下兩條路徑差 >20% 需解釋缺口）</p>

  <div class="exhibit">
    <div class="exhibit-head">{{TAM_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>情境</th><th>{{TAM_YEAR_NEAR}}E</th><th>{{TAM_YEAR_FAR}}E</th><th>假設</th><th>權重（主觀）</th></tr></thead>
        <tbody>
          <tr><td>Base</td><td class="num">{{TAM_BASE_NEAR}}</td><td class="num">{{TAM_BASE_FAR}}</td><td>{{TAM_BASE_ASSUMPTION}}</td><td class="num">{{TAM_BASE_WEIGHT}}</td></tr>
          <tr><td>Bull</td><td class="num">{{TAM_BULL_NEAR}}</td><td class="num">{{TAM_BULL_FAR}}</td><td>{{TAM_BULL_ASSUMPTION}}</td><td class="num">{{TAM_BULL_WEIGHT}}</td></tr>
          <tr><td>Bear</td><td class="num">{{TAM_BEAR_NEAR}}</td><td class="num">{{TAM_BEAR_FAR}}</td><td>{{TAM_BEAR_ASSUMPTION}}</td><td class="num">{{TAM_BEAR_WEIGHT}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research 推導；{{TAM_SOURCES}}［#{{TAM_CITE}}］</p>
  <p class="exhibit-note"><span class="derive">推導：{{TAM_BASE_DERIVATION}}</span>（權重為主觀評估，三情境加總 100，5 點步進）</p>

  <h3>3.2 供給：{{SUPPLY_H3_TITLE}}</h3>
  <div class="exhibit">
    <div class="exhibit-head">{{SUPPLY_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{SUPPLY_COL_1}}</th><th>現在</th><th>{{SUPPLY_COL_NEAR}}</th><th>{{SUPPLY_COL_FAR}}</th></tr></thead>
        <tbody>
          <tr><td>{{SUPPLY_ROW_1}}</td><td>{{SUPPLY_ROW_1_NOW}}</td><td>{{SUPPLY_ROW_1_NEAR}}</td><td>{{SUPPLY_ROW_1_FAR}}</td></tr>
          <!-- 列數依玩家數調整，複製本列增列 -->
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{SUPPLY_SOURCES}}［#{{SUPPLY_CITE}}］</p>
  <p class="exhibit-note">{{SUPPLY_READ}}</p>

  <div class="exhibit">
    <div class="exhibit-head">利潤池<small>{{PROFIT_POOL_TITLE}}</small></div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>環節</th><th>利潤池占比</th><th>走向</th></tr></thead>
        <tbody>
          <tr><td>{{POOL_ROW_1}}</td><td class="num">{{POOL_ROW_1_PCT}}</td><td>{{POOL_ROW_1_DIR}}</td></tr>
          <!-- 列數依價值鏈環節數調整，複製本列增列 -->
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{POOL_SOURCES}}［#{{POOL_CITE}}］</p>

  <p><strong>成本曲線</strong>：{{COST_CURVE_PROSE}}（誰是邊際生產者、價格跌到哪個水準誰先停產；結構成長型可省略，一句寫理由）。</p>

  <h3>3.3 為什麼是現在：{{TECH_H3_TITLE}}</h3>
  <pre class="figure-ascii">{{S_CURVE_ASCII}}</pre>
  <p>{{S_CURVE_SENTENCE_1}}{{S_CURVE_SENTENCE_2}}{{S_CURVE_SENTENCE_3}}</p>
  <p><strong>誰是造王者</strong>：{{KINGMAKER_SENTENCE}}</p>

  <h3>3.4 裁決：供需裁決與三視野推估</h3>
  <p><strong>資本週期</strong>：{{CAPCYCLE_NUM_1}}；{{CAPCYCLE_NUM_2}}。{{CAPCYCLE_SYNTHESIS}}</p>

  <div class="exhibit">
    <div class="exhibit-head">三視野 × 三情境推估</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>時間窗</th><th>Base</th><th>Bull</th><th>Bear</th><th>權重（主觀）</th><th>觸發指標</th></tr></thead>
        <tbody>
          <tr><td><strong>12M</strong></td><td>{{H12M_BASE}}</td><td>{{H12M_BULL}}</td><td>{{H12M_BEAR}}</td><td class="num">{{H12M_WEIGHT}}</td><td>{{H12M_TRIGGER}}</td></tr>
          <tr><td><strong>3Y</strong></td><td>{{H3Y_BASE}}</td><td>{{H3Y_BULL}}</td><td>{{H3Y_BEAR}}</td><td class="num">{{H3Y_WEIGHT}}</td><td>{{H3Y_TRIGGER}}</td></tr>
          <tr><td><strong>5Y+</strong></td><td>{{H5Y_BASE}}</td><td>{{H5Y_BULL}}</td><td>{{H5Y_BEAR}}</td><td class="num">{{H5Y_WEIGHT}}</td><td>{{H5Y_TRIGGER}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research 推導；{{HORIZONS_SOURCES}}［#{{HORIZONS_CITE}}］</p>
  <p class="exhibit-note">各期權重主觀評估、三情境加總 100，5 點步進；觸發指標須可回溯查證，禁模糊詞。</p>

  <p><strong>投資時鐘換相雙閘</strong>：必要條件＝{{PHASE_SHIFT_NECESSARY}}（領先看：{{LEADING_INDICATORS}}）；<strong>並且</strong>充分條件＝{{PHASE_SHIFT_SUFFICIENT}}（需兩個獨立訊號同時滿足才算數）。</p>

  <!-- 可選 3.5：主題需要時追加供給新變數，h3，不得取代上述固定四節 -->

  <details class="evidence-fold">
    <summary>推導與考證</summary>
    <div class="fold-body">
      <p><span class="derive">推導：{{MECHANICS_DERIVATION}}</span></p>
      <p><strong>Bear 情境長什麼樣</strong>：{{BEAR_NARRATIVE_PROSE}}</p>
      <p>{{MECHANICS_FOLD_PROSE}} 🔵 [X: {{MECHANICS_SCENARIO_TAG}}]</p>
    </div>
  </details>
</section>

<!-- 4 · 現在貴不貴 -->
<section id="valuation" class="section">
  <div class="section-no">Section 4</div>
  <h2>現在貴不貴<small>Valuation</small></h2>
  <div class="section-lede">{{VALUATION_LEDE}}</div>

  <div class="exhibit">
    <div class="exhibit-head">{{UNIT_ECON_EXHIBIT_TITLE}}</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>{{UNIT_ECON_COL_1}}</th><th>毛利驅動</th><th>未來 2 年</th><th>抗商品化能力</th></tr></thead>
        <tbody>
          <tr><td>{{UNIT_ECON_ROW_1}}</td><td>{{UNIT_ECON_ROW_1_B}}</td><td>{{UNIT_ECON_ROW_1_C}}</td><td>{{UNIT_ECON_ROW_1_D}}</td></tr>
          <tr><td>{{UNIT_ECON_ROW_2}}</td><td>{{UNIT_ECON_ROW_2_B}}</td><td>{{UNIT_ECON_ROW_2_C}}</td><td>{{UNIT_ECON_ROW_2_D}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{UNIT_ECON_SOURCES}}［#{{UNIT_ECON_CITE}}］</p>

  <p><strong>估值怎麼傳導</strong>：{{VALUATION_PASSTHROUGH_PROSE}}。敏感度：{{VALUATION_SENSITIVITY_ANCHOR}}。</p>

  <h3>Priced-in 位置：核心標的現在貴不貴</h3>
  <div class="exhibit">
    <div class="exhibit-head">核心標的現行倍數 vs 歷史帶</div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>Ticker</th><th>現行倍數</th><th>5 年歷史帶</th><th>估值分位</th></tr></thead>
        <tbody>
          <tr><td><strong>{{PRICEDIN_TICKER_1}}</strong></td><td class="num">{{PRICEDIN_TICKER_1_MULT}}</td><td class="num">{{PRICEDIN_TICKER_1_RANGE}}</td><td class="num">{{PRICEDIN_TICKER_1_PCTL}}</td></tr>
          <tr><td><strong>{{PRICEDIN_TICKER_2}}</strong></td><td class="num">{{PRICEDIN_TICKER_2_MULT}}</td><td class="num">{{PRICEDIN_TICKER_2_RANGE}}</td><td class="num">{{PRICEDIN_TICKER_2_PCTL}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{PRICEDIN_SOURCES}}［#{{PRICEDIN_CITE}}］</p>
  <p>{{PRICEDIN_MOMENTUM_SENTENCE}}（26 週漲幅／擁擠度）。{{PRICEDIN_IMPLIED_GROWTH_SENTENCE}}（現價隱含成長）。收斂：low {{PRICEDIN_LOW}}／mid {{PRICEDIN_MID}}／high {{PRICEDIN_HIGH}}。</p>

  <details class="evidence-fold">
    <summary>推導與考證</summary>
    <div class="fold-body">
      <p><span class="derive">推導：{{VALUATION_DERIVATION}}</span></p>
      <p>{{VALUATION_FOLD_PROSE}}</p>
    </div>
  </details>
</section>

<!-- 5 · 我怎麼知道我錯了 -->
<section id="risks" class="section">
  <div class="section-no">Section 5</div>
  <h2>我怎麼知道我錯了<small>Risks &amp; Falsification</small></h2>
  <div class="section-lede">{{RISKS_LEDE}}</div>

  <div class="exhibit">
    <div class="exhibit-head">否證指標對帳表<small>Kill Metrics</small></div>
    <div class="exhibit-body">
      <table class="kill-table">
        <thead><tr><th>指標</th><th>現值（as-of）</th><th>熊線（thesis 作廢點）</th><th>來源／頻率</th><th>領先幾季</th><th>可否操縱</th><th>破線後姿態</th></tr></thead>
        <tbody>
          <tr><td>{{KILL_1_METRIC}}</td><td class="cv">{{KILL_1_NOW}}（{{KILL_1_ASOF}}）</td><td><strong>{{KILL_1_BEAR}}</strong></td><td>{{KILL_1_SRC_FREQ}}</td><td class="num">{{KILL_1_LEAD_Q}}</td><td>{{KILL_1_MANIPULABLE}}</td><td>{{KILL_1_POSTURE}}</td></tr>
          <tr><td>{{KILL_2_METRIC}}</td><td class="cv">{{KILL_2_NOW}}（{{KILL_2_ASOF}}）</td><td><strong>{{KILL_2_BEAR}}</strong></td><td>{{KILL_2_SRC_FREQ}}</td><td class="num">{{KILL_2_LEAD_Q}}</td><td>{{KILL_2_MANIPULABLE}}</td><td>{{KILL_2_POSTURE}}</td></tr>
          <tr><td>{{KILL_3_METRIC}}</td><td class="cv">{{KILL_3_NOW}}（{{KILL_3_ASOF}}）</td><td><strong>{{KILL_3_BEAR}}</strong></td><td>{{KILL_3_SRC_FREQ}}</td><td class="num">{{KILL_3_LEAD_Q}}</td><td>{{KILL_3_MANIPULABLE}}</td><td>{{KILL_3_POSTURE}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：{{KILL_TABLE_SOURCES}}［#{{KILL_TABLE_CITE}}］。≥1 條須為市場撮合價；本表與 id-meta <code>kill_metrics[]</code> 逐條同步。</p>

  <h3>催化劑：如果對了 vs 如果錯了</h3>
  <div class="event-line">
    <p><span class="event-date">{{CATALYST_1_DATE}}</span>{{CATALYST_1_EVENT}}。<span class="path-pos">{{CATALYST_1_POS}}</span> → {{CATALYST_1_POS_ACTION}}；<span class="path-neg">{{CATALYST_1_NEG}}</span> → {{CATALYST_1_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_2_DATE}}</span>{{CATALYST_2_EVENT}}。<span class="path-pos">{{CATALYST_2_POS}}</span> → {{CATALYST_2_POS_ACTION}}；<span class="path-neg">{{CATALYST_2_NEG}}</span> → {{CATALYST_2_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_3_DATE}}</span>{{CATALYST_3_EVENT}}。<span class="path-pos">{{CATALYST_3_POS}}</span> → {{CATALYST_3_POS_ACTION}}；<span class="path-neg">{{CATALYST_3_NEG}}</span> → {{CATALYST_3_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_4_DATE}}</span>{{CATALYST_4_EVENT}}。<span class="path-pos">{{CATALYST_4_POS}}</span> → {{CATALYST_4_POS_ACTION}}；<span class="path-neg">{{CATALYST_4_NEG}}</span> → {{CATALYST_4_NEG_ACTION}}。</p>
    <p><span class="event-date">{{CATALYST_5_DATE}}</span>{{CATALYST_5_EVENT}}。<span class="path-pos">{{CATALYST_5_POS}}</span> → {{CATALYST_5_POS_ACTION}}；<span class="path-neg">{{CATALYST_5_NEG}}</span> → {{CATALYST_5_NEG_ACTION}}。</p>
  </div>
</section>

<!-- 6 · 誰受影響（不放估值面總結，已在 §4） -->
<section id="stocks" class="section">
  <div class="section-no">Section 6</div>
  <h2>誰受影響<small>Stock Implications</small></h2>
  <div class="section-lede">{{STOCKS_LEDE}}</div>

  <div class="exhibit">
    <div class="exhibit-head">關聯個股 · 🔴 核心｜🟡 中度相關｜🟢 邊緣相關<small>{{TICKER_TABLE_TIME_SCOPE}}</small></div>
    <div class="exhibit-body">
      <table>
        <thead><tr><th>Ticker</th><th>深度</th><th>受益／受害</th><th>純度</th><th>市值級距</th></tr></thead>
        <tbody>
          <tr><td><strong>{{TICKER_1}}</strong></td><td>{{TICKER_1_TIER}}</td><td>{{TICKER_1_DIRECTION}}</td><td class="num">{{TICKER_1_PURITY_PCT}}</td><td>{{TICKER_1_MCAP}}</td></tr>
          <tr><td><strong>{{TICKER_2}}</strong></td><td>{{TICKER_2_TIER}}</td><td>{{TICKER_2_DIRECTION}}</td><td class="num">{{TICKER_2_PURITY_PCT}}</td><td>{{TICKER_2_MCAP}}</td></tr>
          <tr><td><strong>{{TICKER_3}}</strong></td><td>{{TICKER_3_TIER}}</td><td>{{TICKER_3_DIRECTION}}</td><td class="num">{{TICKER_3_PURITY_PCT}}</td><td>{{TICKER_3_MCAP}}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <p class="exhibit-source">資料來源：InvestMQuest Research；{{TICKER_TABLE_SOURCES}}［#{{TICKER_TABLE_CITE}}］</p>
  <p class="exhibit-note"><span class="derive">推導：{{TICKER_PURITY_DERIVATION}}</span></p>

  <p><strong>不明顯的受益者</strong>：{{NONOBVIOUS_PROSE}}</p>
  <p><strong>營運槓桿最大的是誰</strong>：{{OPERATING_LEVERAGE_PROSE}}</p>

  <p class="section-lede">{{STOCKS_NONRECOMMEND_NOTE}}——本表只給特徵與分類，買賣由個股 DD 與系統訊號決定，非買入推薦。</p>
</section>

<!-- 附錄 · 背景、歷史與來源（正文直接可讀，只有 claim 標記說明折疊） -->
<section id="appendix" class="section">
  <div class="section-no">Appendix</div>
  <h2>背景、歷史與來源<small>Appendix</small></h2>
  <div class="section-lede">產業白話定義、歷史脈絡與來源總表——支撐正文判斷的背景層。</div>

  <p>{{APPENDIX_PLAIN_DEFINITION}}</p>
  <p><strong>邊界界定</strong>：{{APPENDIX_SCOPE}}（in-scope vs out-of-scope、為何這樣切、姊妹母題怎麼分工）。</p>

  <p>第一次轉折：<mark class="time">{{TURN_1_DATE}}</mark> {{TURN_1_EVENT}}；第二次：<mark class="time">{{TURN_2_DATE}}</mark> {{TURN_2_EVENT}}；第三次：<mark class="time">{{TURN_3_DATE}}</mark> {{TURN_3_EVENT}}（每個轉折須具體日期＋≥1 量化錨點）。</p>

  <div class="exhibit">
    <div class="exhibit-head">歷史類比<small>{{ANALOGY_EXHIBIT_TITLE}}</small></div>
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
  <p class="exhibit-source">資料來源：{{ANALOGY_SOURCES}}［#{{ANALOGY_CITE}}］</p>
  <p class="exhibit-note">{{ANALOGY_CYCLE_STATS}}（產業有 ≥2 輪 cycle 附統計表；無 cycle 一句註明）</p>

  <table class="src-table">
    <caption>來源總表<small>Sources</small></caption>
    <thead><tr><th>#</th><th>段落</th><th>T 級</th><th>來源</th><th>as-of</th></tr></thead>
    <tbody>
      <tr><td class="num">1</td><td>{{SRC_1_SECTION}}</td><td><span class="tier">{{SRC_1_TIER}}</span></td><td><a href="{{SRC_1_URL}}">{{SRC_1_TITLE}}</a></td><td class="num">{{SRC_1_ASOF}}</td></tr>
      <tr><td class="num">2</td><td>{{SRC_2_SECTION}}</td><td><span class="tier">{{SRC_2_TIER}}</span></td><td><a href="{{SRC_2_URL}}">{{SRC_2_TITLE}}</a></td><td class="num">{{SRC_2_ASOF}}</td></tr>
      <tr><td class="num">3</td><td>{{SRC_3_SECTION}}</td><td><span class="tier">{{SRC_3_TIER}}</span></td><td><a href="{{SRC_3_URL}}">{{SRC_3_TITLE}}</a></td><td class="num">{{SRC_3_ASOF}}</td></tr>
    </tbody>
  </table>
  <p class="exhibit-source">正文以［#n］對應本表列號；T1 佔比依主題型別（硬體／製造 60%、快速演變或 macro 型 45%）。</p>

  <details class="evidence-fold">
    <summary>claim 標記說明</summary>
    <div class="fold-body">
      <p>折疊層與來源表內用 4 類標記：<strong>[F:]</strong> 事實｜<strong>[I:]</strong> 推論（A→B）｜<strong>[X:]</strong> 情境（base/bull/bear）｜<strong>[A:]</strong> 假設。機率用「很可能／可能／不太可能」詞彙級，不用精確百分比（TAM／三視野的「權重（主觀）」欄除外，見 §3.1／§3.4，5 點步進、加總 100）。</p>
    </div>
  </details>
</section>

<!-- closing -->
<div class="pull-quote">
  <div class="pq-label">The One Line</div>
  <p>{{ONE_LINE_CLOSER}}</p>
</div>

<section class="section" style="margin-top:24px">
  <h3 style="margin-top:0">這份報告刻意不做的三件事</h3>
  <ol>
    <li>不告訴你哪一檔該買——表格是「特徵的代表案例」，買賣由你的個股 DD 與 Pure MA 系統決定，本報告非買入推薦。</li>
    <li>{{NOT_DOING_2}}</li>
    <li>{{NOT_DOING_3}}</li>
  </ol>
</section>

<div class="disclosures">
  <div class="dh">Disclosures &amp; Important Information</div>
  本報告由 InvestMQuest Research 內部買方研究流程產生，僅供研究與投資決策參考，不構成要約、招攬或個別投資建議。資料來源含公司公告與第三方研究（{{DISCLOSURE_SOURCE_LIST}}）；前瞻性陳述（base/bull/bear）含不確定性。{{DISCLOSURE_EXTRA}}持倉揭露：本研究流程關聯帳戶可能持有文中標的部位。個股買賣由個股 DD 與系統訊號決定，本報告表格為產業特徵分類、非買入推薦。© {{YEAR}} InvestMQuest Research.
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

## Key Debates 硬規則

- debate-card **3–5 張**；每張三列固定：`is-market`（**市場最強版本**，帶數字，非媒體標語）／`is-view`（**我們認為**，含「已反映：…」一句 priced-in 檢驗）／`is-signal`（**看什麼分勝負**，雙路徑＋⚠ 證偽條件，可量化）。
- **≥1 張「圈外／替代威脅」卡為必填**——來自本產業鏡頭外的替代技術、替代商業模式或新進入陣營。該卡最外層 div 必帶 `data-debate="external-threat"`（機械檢查標記）。缺此卡 critic 直接抓。
- 分歧對但已 priced → 在「我們認為」列標「不可操作」。

## 折疊層規則（`<details class="evidence-fold">`，每節至多一個）

正文閱讀線＝決策與論證的白話結論；claim tag（`[F:]`/`[I:]`/`[X:]`/`[A:]`）與 T 級字樣**只准在折疊或 `src-table` 內出現**，主閱讀線一律白話無標記。

- `thesis` / `debates` / `mechanics` / `valuation` 各一個折疊，收「推導行（`<span class="derive">`）＋ claim 標記＋長考證」；不收來源清單（來源全部收斂到附錄單一 `src-table`，正文與折疊用 `［#n］` 對應）。
- `risks` / `stocks` 不設折疊（內容已經是決策必讀，不該藏）。
- `appendix` 本身已是背景層、直接可讀；唯一的折疊只收「claim 標記說明」（給 critic／校對用的圖例，不是投資判斷）。

## Exhibit 編號與資料來源行規則

- Exhibit 編號用 **CSS counter 自動編號**（`.exhibit` 依 DOM 順序，含附錄內 Exhibit）——不要手寫「Exhibit N」，插刪表格編號自動重排。`src-table`（附錄來源總表）**不算 Exhibit**，用 `<caption>` 當標題列，不消耗 counter——它是參考清單不是承重表。
- 每張 `.exhibit` 後**必跟** `<p class="exhibit-source">資料來源：…［#n］</p>`（`#n` 對應附錄 `src-table` 列號；純自算寫「InvestMQuest Research 推導」，可不掛 `#n`）。
- `exhibit-note` 只在**需要判讀時一句**（不是「怎麼讀／對投資的意義」固定三句樣板）；推導行放這裡或折疊內，不重複兩處。
- 無 source 的 % 改定性（主導／均勢／次要）；禁 Q×4 推估。
- **唯一敘述規則**：核心判斷只在 `thesis` 完整出現，其餘章節提到同一判斷只准寫「見 §1」；investment clock 的雙閘推導只在 §3.4 完整出現，`thesis` 只點出當前 phase 並指向 §3.4；PM 行動與 `judgment-card` 全檔只在 `summary` 出現一次。
- **資料窗唯一**：整份報告一個資料窗日期，`.data-window` 只在 `summary` 出現一次；refresh 若只更新部分章節，仍須把第一頁與 kill 表現值一併更到同一窗。
- **權重欄**：TAM 三情境表與三視野 × 三情境表的「權重（主觀）」欄，5 點步進、三情境加總 100，標明是主觀評估非精確機率；散文事件機率維持詞彙級（很可能／可能／不太可能）。

## 站內 nav 注入區塊照抄規則

`<body>` 開頭的 canonical site header（`<style id="imq-nav-style">` ＋ `<header class="imq-nav-root">` ＋ dropdown `<script>`）由 `scripts/site_nav.py full_nav_block('research','id')` 生成——產檔時**現跑現貼整塊**（取代 `{{SITE_NAV_FULL_BLOCK}}` 佔位符），不要手改、不要憑記憶重寫；site_nav.py 變更後既有頁面由 re-inject 流程重生。頁內 sticky TOC（`.toc-bar`）offset 依 `--nav-h:45px`，行動版轉 static 迴避重疊。`inject_report_primer.py` 的「怎麼讀這份報告」白話導讀塊會插在 nav header 之後、masthead 之前——本 template 不要自帶這個塊，保持該位置乾淨可插入。

## 其他硬規則

- 中文內容標點一律**全形**（，。：；「」）；commit 前 `python3 scripts/qc.py`。
- **主閱讀線禁字**：`NC#`、`AT_RISK`、`INTACT`、`QC-`、`Gate`、`skill_version`、`sub_group`、`Method:`、「本版補齊」、「呈現版」等版本／流程散文一律不得出現在讀者看得到的文字裡；masthead 不印 `sub_group` 值與 `Method` 標籤，版本號只放 `<meta name="id-skill-version">` 與頁尾 colophon 一行。
- 個股非推薦：`stocks` 節 lede、closing「刻意不做的三件事」第 1 條必含「特徵／分類、買賣由個股 DD ＋ 系統決定、非買入推薦」字句。
- Emoji 僅語意用途（🔴🟡🟢 深度、🟢🔵 claim tag、⚠ 證偽），禁裝飾性 emoji。
- light-only（`color-scheme:light` ＋ meta 宣告）；`@media print` 隱藏 nav／TOC／back-top。
- 版號一律 `{{SKILL_VERSION}}`（隨 SKILL.md frontmatter），出現在 `<meta name="id-skill-version">`、id-meta JSON `skill_version`、colophon 三處，三處同值。
- **篇幅**：主閱讀線可見字 11,000–14,000；HTML ≤55KB（CSS 外掛 `/assets/id-v4.css`，不 inline）。超過只警告不擋。
