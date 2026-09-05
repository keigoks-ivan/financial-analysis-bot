你是 stock-analyst v17 的**判斷層閘（gate）**，標的 CDNS（20260905）。你未參與寫判斷，這是一次跨模型冷讀。你的任務只有一件：**依下列 ①–⑦ 逐條複核判斷物，計數判斷級 🔴**。

## 讀（bundle 全文附於本訊息之後，不要 Read 任何檔）

gate bundle 全文接在本訊息最後（「===== BUNDLE =====」分隔行之後），已包含你需要的全部輸入：
- **證據包緊湊版**（numbers／coverage／events／prior_dd／ledger／canonical_id／gaps）
- **judgment.json 全文**（你要複核的對象）
- **最新一季逐字稿全文**＋**其餘三季摘要（digest）**
- **references/critic-gates.md 全文**（checklist 條文權威）

## 禁

- 禁 WebSearch／WebFetch、禁開 bundle 以外任何檔（包含 `docs/dd/`、`.dd_build/` 下的其他產物）。
- 禁跑任何腳本（`validate_judgment.py`／`dd_decision.py`／`dd_scenario.py` 已在判斷端跑過，機械層不歸你）。
- 禁提整段改寫判斷、禁自己動手修補 judgment.json——你只出稽核，修補是另一支 agent 的事。
- 證據包裡沒有的東西，不得臆測補白；只講證據包內找得到依據的話。

## 🔴 的口徑（只給「判斷級」）

判斷級 🔴 限下列三種形狀：

1. **證據包已有而判斷未接**——證據包內存在的 finding／數字，判斷物完全沒接進 `contradictions`／`moat.threats`／`premortem`／`triggers`／`thesis.R`，也沒寫進 `evidence_dismissed[]`；
2. **算術或機率防線失守**——推導不可複算、內部恆等式不對帳、情境樹退化、機率與其自身依據矛盾；
3. **裁決與自身輸入矛盾**——`decision_inputs`／`scenario_meta`／`decision_out` 三者互斥，或裁決與判斷物自己寫下的理由相反。

**資料級不算 🔴**（證據包本身缺料、來源不夠新、某軸查不到）——那是 Stage 0 的問題，最多給 🟡 並在附註點名。無實質問題給 🟢；有實質但不改裁決方向的給 🟡。

## 逐條複核清單（每條必答，不得「同上」帶過）

① 競爭惡化——份額流失／新進入者／客戶 second-source／大客戶轉單，證據包裡有沒有判斷沒接進去的？
② 供需 durability——緊缺或過剩是結構還是週期？供給可逆性寫進 bear 機率了嗎？
③ 其他結構變數——法規／政策／關稅／反壟斷／補貼／通路重構／商模轉移／替代技術／客戶結構轉移，哪一項在 `coverage` 有料卻沒進 `contradictions`／`premortem`／`triggers`？
④ priced-in——共識與賣方目標價 vs 現價，這個裁決是否只是把市場已知的事再說一次？
⑤ **覆蓋面掃描**——`coverage` 中 status="none"／"not_applicable" 的**每一軸**逐軸點名：理由站得住嗎？queries_run 是否 <2 條或不相關？**缺軸本身即 🔴，不需先證明結論錯**。
⑥ **量化模組完整性抽查**——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 是否有 `.formula_note` 實算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與 valuation 隱含共識 EPS CAGR 交叉檢查（天花板 < CAGR＝sanity 失敗，須在 `reasoning` 處理）。(ii) 情境樹 Bull/Base/Bear 的 **EPS** 價差是否實質（Bull 只靠終端倍數、EPS≈Base＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct` 與 `scenario_meta` 是否對帳（不吻合＝🔴）。
⑦ **數字新鮮度**——判斷物引用的每一個營運指標，是否都不比 `numbers.latest_quarter_kpis` 對應項目舊？有一個更舊即 🔴。同時確認 `consensus_revision.stale=true` 沒有被當成唯一依據；引用 digest 內容的欄位有沒有標「來源：摘要」。
⑧ **QC-49 前份漂移歸因**——`prior_dd.prior_meta` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都在 `contradictions[]` 有帶 `prior_field` 的獨立條目、且有三元歸因排序主因；漏欄或無歸因＝🔴；**前份該欄本身為空或缺欄（前一版格式沒有）者不計**，只給 🟡 提醒或 🟢。前份不存在時填 🟢 並註「無前份」。

每條的「指向欄位」必須具體：judgment JSON 路徑（如 `contradictions[3]`、`moat.roic_durability.endo_ceiling`、`decision_inputs.valuation_dependent`）或覆蓋軸編號（`axis#7`）。指不出欄位的意見不要寫進表。

## 輸出（一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/gate_audit.md`，格式固定，下游機械解析）

首行**逐字**照抄下列格式，N 換成你數到的判斷級 🔴 總數（🟡 與 🟢 不計入 N）：

```
## AUDIT: 判斷級🔴 = N
```

空一行後接一張表，欄位順序與表頭不得更動：

```
| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |
|---|---|---|---|---|---|
| 1 | 競爭惡化 | 🟢 | 一句依據 | contradictions[2] | — |
```

- `#` 用 1–8，對應上面 ①–⑧，八列全出，不得跳號、不得多列。
- `燈` 只填 🟢／🟡／🔴 三者之一。
- `依據` 一句話，錨定證據包或 judgment 裡的具體數字／欄位，不寫評語。
- `建議改法` 只在 🟡／🔴 填，一句最小修法（改哪個欄位、改成什麼方向）；🟢 填 `—`。

表後可附**≤200 字**附註（模型組合、🟡 數、資料級疑慮、未能判定的部分）。附註以外不再寫任何段落，不要複述 checklist 條文。

**輪次上限 `6` 輪。** 一次 Write 完成，寫完即回報，不要回讀自己寫的 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/gate_audit.md`。

## 回報（≤100 字）

判斷級 🔴 = N、🟡 = M，以及 🔴 各條的軸別與指向欄位。


===== BUNDLE =====

## ① 任務頭

標的：CDNS　日期：20260905　角色：stock-analyst v16.2 三步制的判斷層 critic（gate） agent。

輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。

---

## ③ Evidence 緊湊版

ticker=CDNS　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 292.7, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-07-27", "trading_days_since": 30, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 4, "current": 60.6, "high": {"value": 78.92, "date": "2024-12-31"}, "low": {"value": 51.67, "date": "2022-12-31"}, "current_percentile_within_annual_points": 32.8}, "ps": {"n_points": 4, "current": 13.83, "high": {"value": 17.93, "date": "2024-12-31"}, "low": {"value": 12.33, "date": "2022-12-31"}, "current_percentile_within_annual_points": 26.8}, "ev_s": {"n_points": 4, "current": 14.02, "high": {"value": 17.91, "date": "2024-12-31"}, "low": {"value": 12.33, "date": "2022-12-31"}, "current_percentile_within_annual_points": 30.3}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 373.59, "fy1_eps": 7.95, "fwd_pe": 46.99}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 374.93, "fy1_eps": 7.95, "fwd_pe": 47.16}, {"snapshot_date": "2026-06-04", "price_used": 376.19, "fy1_eps": 7.95, "fwd_pe": 47.32}, {"snapshot_date": "2026-06-23", "price_used": 377.27, "fy1_eps": 7.96, "fwd_pe": 47.4}, {"snapshot_date": "2026-07-16", "price_used": 330.11, "fy1_eps": 7.96, "fwd_pe": 41.47}, {"snapshot_date": "2026-07-30", "price_used": 340.02, "fy1_eps": 8.15, "fwd_pe": 41.72}, {"snapshot_date": "2026-08-13", "price_used": 324.82, "fy1_eps": 8.14, "fwd_pe": 39.9}, {"snapshot_date": "2026-08-28", "price_used": 292.7, "fy1_eps": 8.14, "fwd_pe": 35.96}, {"snapshot_date": "2026-09-04", "price_used": 292.7, "fy1_eps": 8.14, "fwd_pe": 35.96}], "current": 35.96, "high": 47.4, "low": 35.96, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": -22.19, "return_26w_pct": -1.43, "excess_return_13w_pct": -26.73, "excess_return_26w_pct": -15.95, "benchmark": "^GSPC", "rsi14": 31.05, "rsi14_usable": true, "distance_from_52w_high_pct": -29.71, "distance_from_52w_low_pct": 10.18, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 8.14, "fy2": 9.54, "fy3": 11.14}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 8.14, "fy2": 9.54, "fy3": 11.14}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 7.95, "fy2": 9.38, "fy3": 10.92}, "fy1": {"revision_pct": 0.0, "from": 8.14, "to": 8.14, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 0.0, "from": 9.54, "to": 9.54, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 0.0, "from": 11.14, "to": 11.14, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 2.39, "fy2_revision_90d_pct": 1.71, "fy3_revision_90d_pct": 2.01, "stale": false, "note": null}, "peer_financials": {"CDNS": {"gross_margin_pct": 85.87, "operating_margin_pct": 30.82, "fcf_margin_pct": 28.64, "rd_intensity_pct": 33.02, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "SNPS": {"gross_margin_pct": 73.47, "operating_margin_pct": 9.73, "fcf_margin_pct": 30.35, "rd_intensity_pct": 32.11, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "ARM": {"gross_margin_pct": 97.54, "operating_margin_pct": 17.3, "fcf_margin_pct": 28.55, "rd_intensity_pct": 57.49, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "QCOM": {"gross_margin_pct": 54.23, "operating_margin_pct": 23.28, "fcf_margin_pct": 23.64, "rd_intensity_pct": 22.45, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "688521.SH": {"gross_margin_pct": null, "operating_margin_pct": null, "fcf_margin_pct": null, "rd_intensity_pct": null, "fiscal_period_as_of": null, "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "quarterly_income_stmt 無資料"}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-07-29", "url": "https://www.sec.gov/Archives/edgar/data/813672/000081367226000092/cdns-20260630.htm", "excerpt": "No single customer accounted for 10% or more of total revenue during the three and six months ended June 30, 2026 or June 30, 2025. Recurring revenue includes revenue recognized over time from Cadence’s Core EDA software licensing arrangements, services, royalties, maintenance on IP licenses and hardware, and operating leases of hardware. Other recurring revenue includes revenue recognized at a point in time for short-term software arrangements that are typically renewed at least annually and revenue recognized at varying points in time over the term of other arrangements with non-cancelable commitments, whereby the customer commits to a fixed dollar amount over a specified period of time that can be used to purchase from a list of products. Arrangements that require future decisions on the performance obligations to be delivered do not meet the definition of a revenue contract until the customer executes a separate selection form to identify the products and services that they are purchasing. Each separate selection form under the arrangement is treated as an individual contract and accounted for based on the respective performance obligations. The remainder of Cadence’s revenue is recognized at a point in time and is characterized as up-front revenue. Up-front revenue is primarily generated by sales of hardware, individual IP licenses and SD&A software licenses with a term greater than one year. The percentage of Cadence’s recurring and up-front revenue in any single fiscal period is primarily impacted by delivery of hardware and IP products to its customers. The following table shows the percentage of Cadence’s revenue that is classified as recurring or up-front for the three and six months ended June 30, 2026 and June 30, 2025: Three Months Ended Six Months Ended June 30, 2026 June 30, 2025 June 30, 2026 June 30, 2025 Revenue recognized over time 72 % 73 % 72 % 75 % Other recurring revenue 6 % 5 % 6 % 5 % Recurring revenue 78 % 78 % 78 % 80 % Up-front revenue 22 % 22 % 22 % 20 % Total revenue 100 % 100 % 100 % 100 % 10 Significant Judgments Cadence’s contracts with customers often include promises to transfer to a customer multiple software and/or IP licenses and services, including professional services, technical support services, and rights to unspecified updates. Determining whether licenses and services are distinct performance obligations that should be accounted for separately, or not distinct and thus accounted for together, requires significant judgment.", "note": null}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "items": [{"metric": "營收（GAAP）", "value": 1584, "unit": "百萬美元", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": "consensus ≈$1.58B（Zacks Consensus Estimate，來源：web_search 財報前瞻報導）；實際超出約0.5%", "prior_quarter": "Q2 2025: $1,275M（YoY +24.2%）；Q1 2026: $1,474M（QoQ +7.5%）"}, {"metric": "Non-GAAP 營業利益率", "value": 45.5, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": "公司自身 Q2 guidance 43.5–44.5%（於 Q1 2026 法說給出）；實際 45.5% 優於高標", "prior_quarter": "Q1 2026: 44.7%；Q2 2025: 42.8%（YoY +270bp）"}, {"metric": "GAAP 營業利益率", "value": 28.4, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: 29.3%；Q2 2025: 19.0%（YoY +940bp）"}, {"metric": "自由現金流（FCF）", "value": 582.3, "unit": "百萬美元（FCF margin ≈36.8%；估算值＝6個月YTD OCF $990.7M－Q1 OCF $355.8M，減6個月YTD capex $101.4M－Q1 capex $48.8M，因新聞稿只揭露YTD累計現金流量表、未單獨拆分單季）", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx（Q2單季為YTD減去Q1新聞稿揭露值換算，Q1 OCF $355.8M／capex $48.8M／FCF $307.0M）", "vs_consensus": null, "prior_quarter": "Q1 2026: $307.0M（FCF margin ≈20.8%）"}, {"metric": "SBC 占營收／占GAAP營業利益比", "value": 9.3, "unit": "%（SBC $146.9M ÷ 營收 $1,584M＝9.3%；SBC ÷ GAAP營業利益 $449.9M＝32.7%）", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: SBC $138.2M／營收$1,474M＝9.4%"}, {"metric": "管理層財測（Q3 2026 及 FY2026，Q2財報時給出）", "value": "Q3 2026: non-GAAP EPS $2.01–$2.07、non-GAAP營業利益率43.5–44.5%、GAAP營業利益率27.5–28.5%；FY2026（上修）: 營收$6.26–$6.34B（≈+19% YoY）、non-GAAP營業利益率43.75–44.75%、non-GAAP EPS $8.05–$8.15", "unit": "guidance range", "as_of": "公告於 2026-07-27，隨Q2 2026財報發布", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026法說時的FY2026原guidance：營收$6.125–$6.225B（≈+17% YoY）、non-GAAP EPS $7.85–$7.95 → 本次全面上修"}, {"metric": "Backlog／12個月RPO（SaaS類遞延收入代理指標，Cadence未揭露NRR或ARR客戶數）", "value": "Backlog $8.1B（record）；未來12個月將認列的RPO $4.2B", "unit": "billion USD", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: Backlog $8.0B；12個月RPO $4.0B"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | 0 | 2025-06-01 | 2024 年全球 EDA 市場份額：Synopsys 約 31%、Cadence 約 30%、Siemens EDA 約 13%，三家合計逾九成營收，為高度集中的雙強＋一（Cadence/Synopsys/Siemens）格局，2025-2026 未見結構性洗牌。 | EDA Market Primer (SemiAnalysis newsletter, newsletter.semianalysis.com/p/eda-market-primer) | moat_trend,thesis.H |
| competitive_share_entrants#1 | + | 2026-04-01 | Cadence 核心 EDA 業務 FY2026 Q1 年增 18%，公司上調 2026 全年營收指引至 $6.26-6.34B（原 $6.125-6.225B），股價因 18.7% 年增營收、$8B 積壓訂單（多與 AI 需求相關）而上漲，顯示 Cadence 在整體 EDA 市場擴張中維持份額並受惠於 AI 驅動需求擴大。 | Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand (Yahoo Finance, finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html) | thesis.H,moat_trend |
| competitive_share_entrants#2 | + | 2026-01-01 | Cadence 在多代工廠（TSMC／Samsung／Intel／Rapidus）動態上被評為比 Synopsys 更有利卡位，其半導體 IP 營收 FY2025 Q1 年增達 40%；相對地 Synopsys 已承認 FY26 IP 業務將是清淡的一年（muted year），顯示 IP 這一子區隔 Cadence 相對競爭對手份額走強。 | Synopsys and Cadence: The $160B Unsung Giants of Semiconductor Design (datagravity.dev/p/synopsys-and-cadence-the-160b-unsung) | thesis.H,moat_trend |
| competitive_share_entrants#3 | 0 | 2026-06-01 | 2026 年 DAC（Design Automation Conference）Chips to Systems 大會上，Synopsys、Cadence、Siemens 三大既有對手同步發表全自主 agentic 晶片設計工作流（Synopsys 全自主長流程 agentic workflow、Cadence AuraStack AI Super Agent／ChipStack AI、Siemens 自我驗證 agentic workflow）；查無具規模的全新進入者（non-incumbent new entrant）對 Cadence 構成搶單威脅，2026 年競爭仍集中在既有三大廠之間的 AI 能力軍備競賽。 | Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC (Futurum Group, futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/) | moat_trend,thesis.H |
| customer_second_source#0 | 0 | 2026-01-01 | Intel 為 Cadence 最大單一客戶帳戶（single largest account），且歷史上 Cadence 在 Intel 的滲透相對其在 TSMC／Samsung 的地位偏弱；2026 年 Cadence 正嘗試在 Intel 拓展業務灘頭（gain traction），意味這是一個仍待鞏固而非已鎖定的客戶關係。 | Hudson Labs: Cadence Design Systems (CDNS) Equity Initiation Report (hudson-labs.com/research/cadence-design-systems-cdns-equity-initiation-report) | thesis.R,decision_inputs.bear |
| customer_second_source#1 | + | 2026-04-16 | 超大規模業者（hyperscalers，如 Apple／Amazon／Google／Microsoft）與 Tesla 等正加速建立自有晶片設計團隊、發展客戶自有工具（COT, Customer-Owned Tooling）自研晶片；但查得的證據顯示這些內部設計團隊是**擴大採用並整合** Cadence／Synopsys 既有工具（而非以自研工具取代之），例如某大型超大規模業者已採用 Cadence 數位全流程（digital full flow）完成其首次全 COT AI 晶片流片，Cadence 與 Google 亦整合 Gemini AI 平台與 ChipStack AI Super Agent；查無證據顯示主要客戶正以自製 in-house EDA 工具取代 Cadence 授權，內部晶片設計團隊擴張反而被引述為推升 EDA 授權需求的正面驅動力。 | The Embrace Of AI In Design Transforms Cadence And Its Customers (The Next Platform, nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#2 | - | 2026-01-01 | Cadence 業務揭露其最大風險之一為對少數大型半導體與超大規模運算客戶的營收集中度（customer concentration），主要客戶帳戶延遲或流失重大專案會直接衝擊財報表現；公司未單獨揭露特定客戶佔營收百分比等具體集中度數字。 | Hudson Labs: Cadence Design Systems (CDNS) Equity Initiation Report (hudson-labs.com/research/cadence-design-systems-cdns-equity-initiation-report) | thesis.R,decision_inputs.bear,valuation |
| customer_second_source#3 | + | 2026-07-14 | Cadence FY2026 硬體（emulation／prototyping，即 Dynamic Duo）業務創紀錄，新增 30 家以上客戶、既有客戶回購需求大增，前十大硬體客戶中有 7 家同時採用模擬（emulation）與原型（prototyping）雙產品，顯示 Cadence 在硬體驗證這一環對主要客戶的滲透（而非被 second-source）正在加深，未見主要客戶導入第二供應商替代 Cadence 硬體產品線的證據。 | Cadence Design Systems vs. Synopsys: Which Technology Stock Is a Better Buy in 2026? (The Motley Fool, fool.com/coverage/better-buy/2026/07/14/cadence-design-systems-vs-synopsys-which-technology-stock-is-a-better-buy-in-2026/) | moat_trend,thesis.H |
| customer_concentration_credit#0 | 0 | 2025-09-30 | Cadence 2025 Q3 10-Q 揭露：截至 2025-09-30 無單一客戶占應收帳款 10% 以上；相較截至 2024-12-31 時有一名客戶占應收帳款約 11%，顯示客戶集中度已略降但曾一度接近門檻（此為應收帳款集中度，非營收集中度，10-K 本身未查到具體營收占比數字）。 | Cadence Design Systems Q3 2025 10-Q filing (投資人關係 PDF, s206.q4cdn.com) | thesis.R,decision_inputs.bear |
| customer_concentration_credit#1 | - | 2025-08-05 | Fitch 於 2025-08-05 將 Intel 長期信評自 BBB+ 下調至 BBB、展望負向，原因為獲利能力預期未來 12-18 個月持續疲弱、核心 client/data center 市占流失、晶圓代工業務營運虧損；Intel 為 Cadence 主要 EDA 客戶之一（歷史上位列前幾大客戶）。Fitch 同時指出 Intel 帳上仍有 $212 億現金及短期投資、$70 億未動用循環信貸額度，流動性尚屬穩健。 | CNBC "Intel's credit rating downgraded by Fitch on demand challenges" | thesis.R,decision_inputs.bear |
| customer_concentration_credit#2 | - | 2024-12-11 | S&P 於 2024-12-11 將 Intel 信評自 BBB+ 下調至 BBB，Moody's 亦將 Intel 高級無擔保信評下調至 Baa2（自 Baa1），皆反映 Intel 財務體質動盪，距投資等級底線（junk）僅剩兩級。 | The Register "Intel turmoil prompts S&P Global to downgrade chipmaker's credit rating" | thesis.R |
| customer_concentration_credit#3 | - | 2025-11-13 | Samsung 晶圓代工（Foundry）部門財務壓力預期持續至 2027 年，市場對其獲利轉正時點的預期已由 2027 年遞延至 2028 年（此為部門層級虧損，非 Samsung Electronics 集團整體信評遭下調）。Samsung 為 Cadence 主要客戶之一。 | TrendForce "Samsung Reportedly Eyes Foundry Profitability by 2027 with 20% Market Share"（後續 AnySilicon 報導指出時點已遞延至 2028） | thesis.R |
| customer_concentration_credit#4 | + | 2026-Q1 | Samsung 晶圓代工稼動率於 2026 年第一季升破 80%，為一年高點，顯示該客戶端接單動能回升，部分抵銷部門獲利壓力的負面訊號。 | SemiWiki "More Clients Leads to 80% Utilization at Samsung Foundry in 1Q2026" | thesis.R |
| supply_demand_durability#0 | + | 2026-07-27 | Cadence FY2026 Q2（財報日 2026-07-27）：營收 $15.84 億、年增 24.2%；創紀錄 backlog $81 億；IP 業務年增逾 40%、Core EDA 年增 18%、System Design and Analysis 年增 37%；公司同步上修 2026 全年營收展望至 $62.60-63.40 億、Non-GAAP EPS 展望至 $8.05-8.15。值得注意的是 2026 為公司三年更新週期中續約金額相對較低的一年，backlog 仍創新高顯示需求動能非僅來自續約時點，而是新增業務（本季新增 12 個新客戶）。 | Cadence 8-K CFO commentary (SEC EDGAR, cfocommentary07272026ex9902.htm) / Zacks "Cadence Q2 Earnings Top Estimates on AI Demand, Backlog Hits $8.1B" | thesis.H,decision_inputs.bear,triggers |
| supply_demand_durability#1 | + | 2026 | 產業研究機構預測全球 EDA 市場規模將自 2026 年約 $182 億成長至 2033 年 $335 億（CAGR 9.1%），成長動能歸因於設計複雜度上升、AI/ML 晶片普及、sub-5nm 製程滲透（報告稱逾 65% 新設計案已採用 FinFET/GAAFET 架構），論述定位為結構性而非景氣循環驅動。 | Persistence Market Research "Electronic Design Automation (EDA) Market Size & Forecast, 2033" | thesis.H |
| supply_demand_durability#2 | + | 2026 | 半導體設備業界預期 AI 驅動資本支出持續至 2027 年、晶片設備銷售將創 $1,560 億歷史新高，JPMorgan 與 Goldman Sachs 預估 2027 年 AI 資本支出達 $1 兆以上規模。 | EE Times "AI Drives CapEx Chip Equipment to Record $156B in 2027" | thesis.H |
| supply_demand_durability#3 | - | 2026 | 市場評論警示 AI 基礎建設投資與實際軟體端營收之間存在顯著落差，永續性測試可能於 2027 年（多數大型專案完工、設備銷售觸頂之際）浮現；分析估計 AI 產業需在 2030 年前達到約 $2 兆年營收方能支撐當前投資水準，若 Agentic AI 轉型未能兌現對應生產力增益，行業恐面臨類似 2000 年代初網路泡沫的急遽收縮。 | Pine Tree Macro Research (Substack) "The AI Capex Bubble: Bigger Than You Think" | thesis.R,decision_inputs.bear |
| regulatory_antitrust#0 | 0 | 2025-07 | 公開搜尋未查得任何鎖定 Cadence（CDNS）本身的 2026 年正式反壟斷調查、拆分程序或 DOJ/FTC/EU 競爭調查報導；EDA 產業近期唯一重大競爭結構變動是對手 Synopsys 完成收購 Ansys（約 350 億美元交易），該案在多國（含中國 SAMR）經過延長反壟斷審查後於 2025 年 7 月完成交割，形成首個垂直整合的 device-to-system 設計堆疊，但此案標的為 Synopsys/Ansys 非 Cadence，未見對 Cadence 本身的監管動作 | SemiAnalysis newsletter "EDA Market Primer" (newsletter.semianalysis.com/p/eda-market-primer) | decision_inputs.bear,moat_trend |
| regulatory_antitrust#1 | 0 | 2025-12 | EDA 市場呈現寡占結構：前五大廠商（Synopsys、Cadence、Siemens EDA、Keysight、Zuken）合計約占 AI EDA 市場 70-85% 份額；Cadence 本身約占全球 EDA 市場 30%，與 Synopsys 並列兩大主導廠商——此高集中度本身是產業特性（非近期監管介入結果），但為未來潛在反壟斷關注的市場背景 | MarketsandMarkets "Synopsys, Inc. (US) and Cadence Design Systems, Inc. (US) are Leading Players in the AI EDA Market" (marketsandmarkets.com/ResearchInsight/ai-eda-companies.asp); MatrixBCG competitor analysis (matrixbcg.com/blogs/competitors/cadence) | moat_trend,decision_inputs.bear |
| reg_tariff_export#0 | - | 2025-07-28 | 美國商務部 BIS 對 Cadence 因非法出口 EDA 硬體/軟體與半導體設計技術給 Entity List 上（涉及中國軍事最終用途）的實體，處以 9,500 萬美元行政罰款；同時司法部（DOJ）併行協議追加 4,500 萬美元沒收金，合計逾 1.4 億美元，Cadence 對出口管制違規事實表示認罪 | BIS press release "Cadence Design Systems to Pay $95 Million Penalty to BIS..." (bis.gov/press-release); BIS Final Order (bis.gov/media/documents/cadence-design-systems-final-order-7.28.2025.pdf); San Jose Inside "Cadence Design Systems Admits Selling Design Tools to China, Will Pay Over $140M in Penalties" | decision_inputs.bear,thesis.R,triggers |
| reg_tariff_export#1 | 0 | 2025-07-02 | 2025 年 5 月 23 日 BIS 曾通知 Cadence，其 EDA 軟硬體技術（ECCN 3D991/3E991）出口、再出口或境內轉讓至中國或中國軍事最終用戶方須取得許可證；但 BIS 於同年 7 月 2 日隨即撤銷該許可證要求，即時生效 | Crowell & Moring LLP "Joint Criminal and Civil Export Controls Enforcement: Lessons from the Cadence Case" (crowell.com/en/insights/client-alerts) | thesis.R,triggers |
| reg_tariff_export#2 | 0 | 2025-11-11 | 2025 年 9 月 BIS 發布過渡最終規則，將出口限制擴大適用至由 Entity List 或 Military End-User List 實體持股 50% 以上的關聯公司（俗稱「50% 規則」）；但 BIS 於 2025 年 11 月 11 日公告將該新規則暫停實施一年，目前預定於 2026 年 11 月 9 日到期恢復 | Crowell & Moring LLP client alert; BIS press releases referenced therein | thesis.R,triggers,decision_inputs.bear |
| reg_tariff_export#3 | - | 2025-12-31 | 依 Cadence FY2025 10-K 揭露，中國市場占公司總營收約 13%（2024 年約 12%、2023 年約 17%），為呈現波動但持續重大的地區集中度；公司在風險因子章節將出口管制進一步收緊列為可能大幅移除此營收來源且短期難以替代的風險 | SEC EDGAR, CADENCE DESIGN SYSTEMS INC Form 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | decision_inputs.bear,thesis.R,valuation |
| reg_tariff_export#4 | 0 | 2026-01-15 | 2026 年 1 月 15 日生效的美國 Section 232 半導體關稅（對特定先進半導體徵收 25% 從價稅，鎖定符合特定 Tensor Processing Performance 與 DRAM 頻寬門檻的高效能晶片，如 NVIDIA H200、AMD MI325X）條文與豁免範圍（美國境內資料中心、研發、新創、維修、非資料中心消費/工業用途、公部門）鎖定實體晶片產品，公開資料未見將 EDA 設計軟體本身納入課徵範圍的規定 | White & Case LLP "President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles"; Z2Data "The Section 232 Semiconductor Tariff, Explained" | decision_inputs.bear |
| geo_supply_chain#0 | - | 2026-02 | Cadence 10-K（FY2025）風險因子揭露：公司對美中地緣政治與經貿不確定性存在重大曝險，包括現行及未來美中貿易法規、關稅與其他貿易限制的未知影響，並特別點名台灣作為科技產業供應鏈核心樞紐的地緣政治風險。 | SEC EDGAR: Cadence Design Systems Form 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | - | 2025-07-02 | 美國商務部 BIS 於 2025-05-23 通知 Cadence，對中國或中國軍事最終用戶交易涉及特定 ECCN 分類之 EDA 軟體與技術的出口/再出口/境內轉移須申請許可；2025-07-02 BIS 通知該許可要求即刻撤銷，Cadence 已恢復受影響中國客戶的 EDA 軟體與技術存取。公司揭露該段暫時性許可要求已對同期中國區營收造成負面影響。 | Cadence 10-K FY2025 risk factors, as summarized in company SEC filing disclosure (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear,moat_trend |
| geo_supply_chain#2 | - | 2026-02 | Cadence 於 10-K 明確揭露前瞻風險：鑑於美中持續談判，美國未來可能考慮對 Cadence 之 EDA 軟體與技術或其他產品服務重新施加或擴大此類（或額外）出口管制限制，屬於未解除的政策不確定性。 | Cadence 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear,triggers |
| geo_supply_chain#3 | 0 | 2025-12-31 | 中國區營收於 FY2025 為 $679.97M，占公司總營收 5.31%（同期美洲區占 19.38%、除中日以外亞洲區占 13.17%，皆為對總營收之占比而非互斥地理分組加總 100%）。 | Cadence 10-K FY2025 geographic revenue disclosure, as reported via StockTitan SEC filing summary (stocktitan.net/sec-filings/CDNS/10-k-cadence-design-systems-inc-files-annual-report-6bcef311af10.html) | thesis.R,valuation |
| geo_supply_chain#4 | - | 2025-07-28 | Cadence 因 2015-2021 年間對中國國防科技大學（NUDT，美國 Entity List 軍方大學）非法出口 EDA 設計工具與技術一案，就一項共謀違反出口管制罪名向 DOJ 認罪，並與商務部 BIS 達成民事和解，合計裁罰逾 $140M；此為出口管制刑事/民事執法紀錄，顯示公司過去在中國/軍方終端客戶合規把關上曾出現漏洞。 | DOJ Office of Public Affairs press release (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development) | thesis.R,decision_inputs.bear,moat_trend |
| end_markets#0 | + | 2026-04 | Cadence FY2026 Q1 營收結構：Core EDA 占 71%（年增 18%，主要動能為在指標型客戶的滲透擴大及硬體模擬〔emulation〕創單季歷史新高，由 AI 與 HPC 客戶帶動）；半導體 IP 占 14%（年增 22%，由 AI／HPC／車用工作負載加速需求帶動，並與一家主要晶圓代工客戶簽下鎖定 2 奈米製程節點的創紀錄規模 IP 訂單）；System Design and Analysis 占 15%（年增 18%，3D-IC 與多物理模擬動能強勁，受 AI 驅動的系統複雜度上升帶動）。 | TIKR.com blog: 'Cadence Design Systems Stock Q1 2026 Earnings: Every Segment Grew Double Digits' (tikr.com/blog/cadence-design-systems-stock-q1-2026-earnings-every-segment-grew-double-digits) | thesis.H,moat_trend |
| end_markets#1 | + | 2026-07-27 | 公司將 2026 全年營收展望上修至 $6.125B–$6.225B（GAAP／non-GAAP 營業利益率 27.5–28.5%／43.5–44.5%），Q2 FY2026 營收 $1.584B、年增 24.2%，優於預期；管理層將成長歸因於超大規模業者（hyperscaler）基礎設施與 physical AI 相關的廣泛系統架構設計活動。 | Yahoo Finance: 'Cadence Q2 Earnings Top Estimates, 2026 Revenue Outlook Raised' (finance.yahoo.com/markets/stocks/articles/cadence-q2-earnings-top-estimates-145000369.html) | thesis.H,valuation |
| end_markets#2 | + | 2026-07 | Cadence 進入 2026 年時的訂單積壓（backlog）達創紀錄的 $7.8B；管理層將 agentic AI（如 ChipStack）列為長期持續性成長動能，Q2 新增 12 家硬體客戶並擴大與多家 hyperscaler 及 AI 業者的合作，反映 hyperscaler 自研晶片（custom silicon）趨勢加速，Cadence 同時提供 EDA 工具與 IP 兩端服務。 | Yahoo Finance: 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html) | thesis.H,moat_trend |
| end_markets#3 | 0 | 2026-01 | 全球 EDA 工具市場 2026 年規模約 $20.78B，預估以 CAGR 8.10% 成長至 2031 年 $30.67B（另一機構估算基期不同：EDA 軟體市場 2025 年 $14.28B，以 CAGR 11.5% 成長至 2034 年 $38.05B）；市場集中度高，Synopsys、Cadence、Siemens 三家合計約占全球營收 70%，其中 Synopsys 約 31%、Cadence 約 30% 市占。 | Mordor Intelligence: 'Electronic Design Automation Tools (EDA) Market Analysis'; Precedence Research: 'Electronic Design Automation Software Market Size to Hit USD 34.71 Billion by 2035' | valuation,moat_trend |
| substitute_technology#0 | - | 2026-08-18 | CDNS 股價捲入市場對 AI 顛覆傳統軟體公司獲利模式疑慮所引發的更廣泛軟體股拋售潮，市場憂心 AI 可能自動化部分晶片設計工作流程、降低公司長期可觸及市場的成長率。 | CNBC - "Cadence is a chip stock left behind by the AI boom. Why the CEO says that's a mistake" (https://www.cnbc.com/2026/08/18/cadence-is-a-chip-stock-left-behind-by-the-ai-boom-why-the-ceo-says-thats-a-mistake.html) | thesis.R,decision_inputs.bear,valuation |
| substitute_technology#1 | 0 | 2026-08-18 | Cadence CEO Anirudh Devgan 公開回應軟體股拋售疑慮，主張設計先進晶片需要精確的物理與數學運算，AI 本身無法取代公司核心工具，並將公司基礎工具比喻為「V6/V8 引擎」、AI 為輔助而非替代。 | CNBC - "Cadence is a chip stock left behind by the AI boom. Why the CEO says that's a mistake" (https://www.cnbc.com/2026/08/18/cadence-is-a-chip-stock-left-behind-by-the-ai-boom-why-the-ceo-says-thats-a-mistake.html) | moat_trend,thesis.H |
| substitute_technology#2 | - | 2026-03-26 | Siemens EDA 於 2026 年 Semicon China 展示其 Fuse EDA AI Agent，採用 RAG 框架與多模態 EDA 資料基礎設施，能自主協調前端設計、驗證與量產簽核跨流程工作，主張可將晶片設計週期縮短一半，對 Cadence 傳統 EDA 工具形成競爭壓力。 | Digitimes - "Semicon China 2026: Siemens EDA pushes agentic AI to cut chip design cycles in half" (https://www.digitimes.com/news/a20260326VL206/siemens-eda-design-semicon-china-2026-ic.html) | moat_trend,thesis.R |
| substitute_technology#3 | + | 2026-04-16 | 系統廠商（含 hyperscaler）現占 Cadence EDA 需求的 45%，較兩年前的 40% 上升；一家指標性 hyperscaler 已採用 Cadence 數位全流程完成其首顆全 COT（Customer-Owned Tooling）AI 晶片流片，驗證 Cadence 在最高難度客戶端的數位競爭力，且多筆 COT 流片仍在進行中。 | The Next Platform - "The Embrace Of AI In Design Transforms Cadence And Its Customers" (https://www.nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.H |
| channel_business_model_shift#0 | 0 | 2026-02-05 | EDA 產業雲端部署區隔預期成長最快，雲端運算彈性擴展正拓寬客戶對進階驗證工具的取用管道，但因 IP 敏感性，仍有 69.60% 的設計流程留在地端（on-premise），顯示通路／部署模式轉移速度受限。 | GlobeNewswire - "Electronic Design Automation Tools (EDA) Research Report 2026: Market Share Analysis, Industry Trends & Statistics, Growth Forecasts Report 2025-2031" (https://www.globenewswire.com/news-release/2026/02/05/3233268/28124/en/Electronic-Design-Automation-Tools-EDA-Research-Report-2026-Market-Share-Analysis-Industry-Trends-Statistics-Growth-Forecasts-Report-2025-2031.html) | thesis.R,moat_trend |
| channel_business_model_shift#1 | + | 2026-04-16 | Cadence 銷售通路組合為高接觸度直接企業銷售（針對頂層客戶的專屬客戶團隊與現場應用工程師深入嵌入設計週期）搭配擴大中的雲端與合作夥伴通路以觸及中型市場與區域成長；系統廠商／hyperscaler 客戶占比持續上升（見 substitute_technology 軸 F4：45% 較兩年前 40%），為公司主動朝大型系統廠商直接經營的通路重心轉移。 | The Next Platform - "The Embrace Of AI In Design Transforms Cadence And Its Customers" (https://www.nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.H,triggers |
| capital_markets_pricing#0 | + | 2026-07-27 | Cadence 於 2026-07-27 公布 Q2 2026 財報後上修 FY2026 財測：營收指引由 $6.13-6.23B 上修至 $6.26-6.34B（中值年增 19%）、non-GAAP EPS 指引由 $7.85-7.95 上修至 $8.05-8.15，Q2 本身營收 $1.584B／EPS $2.11 均優於分析師預期，且 backlog 創紀錄達 $8.1B。 | Benzinga — "Cadence Design Systems Beats Q2 Estimates, Raises 2026 Outlook"（investor.cadence.com Q2 2026 財報稿佐證） | thesis.H,valuation,decision_inputs.bear |
| capital_markets_pricing#1 | 0 | 2026-07-28 | 上修後的 FY2026 指引中值（營收 $6.30B／EPS $8.10）仍略低於當時賣方共識（營收 $6.329B／EPS $8.12），顯示公司指引雖上修但未超越市場預期。 | Simply Wall St News — "Cadence Design Systems (CDNS) Lifts 2026 Outlook, Is The Stock Fully Priced?" | valuation,thesis.R |
| capital_markets_pricing#2 | + | 2026-07-28 | Q2 財報後賣方目標價全面上修：BofA Securities 由 $400 調升至 $420（維持 Buy）、KeyBanc 調升至 $425、Stifel 重申 Buy 並維持 $432 目標價。 | ChartMill.com — "Cadence Design Systems (NASDAQ:CDNS) Upgrades Guidance as a High Growth Stock Powered by AI"；Investing.com — "Stifel reiterates Cadence Design stock rating on strong margins" | valuation,decision_inputs.bull |
| capital_markets_pricing#3 | + | 2026-09-02 | 近期（2026-09-01~02）25 位華爾街分析師中位數 12 個月目標價為 $405（區間 $300-$470），對 `numbers.price_at_dd`（$292.7）隱含約 +32% 上檔空間；買進評等占比達 84%。 | WallStreetZen — "Cadence Design Systems Stock Forecast & Predictions: 1Y Price Target $385.00"；Simply Wall St — "Cadence Design Systems (NasdaqGS:CDNS) Stock Forecast & Analyst Predictions" | valuation |
| capital_markets_pricing#4 | 0 | 2026-07-28 | 儘管賣方目標價共識偏多（多數 Buy／Strong Buy），Zacks 量化模型評等維持 Zacks Rank #3（Hold），與賣方分析師普遍樂觀評等形成落差。 | Simply Wall St / 綜合報導引用之 Zacks Rank 資料（見 CDNS 分析師評等彙整頁） | thesis.R,decision_inputs.bear |
| major_events#0 | 0 | 2026-02-23 | Cadence 完成收購 Hexagon 旗下設計與工程（D&E）事業，交易金額約 €2.7B／$3.2B，2026-02-23 完成交割；公司預期該業務 2026 年貢獻約 $160M 營收，非 GAAP 基礎下對 2026 EPS 稀釋約 28 美分，2027 年轉為增益。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Hexagon's Design and Engineering Business, Advancing Leadership in Physical AI and Multiphysics' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-completes-acquisition-of-hexagons-design-and-engineering.html) | thesis.H,decision_inputs.bear,moat_trend |
| major_events#1 | + | 2026-03-05 | Cadence 收購 EMA Design Automation（金額未揭露），強化其 PCB 設計領域布局，2026-03-05 完成。 | Tracxn deal brief: 'Cadence Acquires EMA' (tracxn.com/d/insights/merger-acquisition-deals-brief/cadence-acquires-ema/__2GFeel2DERN2Huua_VuEI8_1eWy4KiZTZGAH09AhLl4) | moat_trend |
| major_events#2 | + | 2025-08-27 | Cadence 完成收購 Arm 的 Artisan foundation IP 業務（標準元件庫、記憶體編譯器、先進製程節點 GPIO），2025-08-27 完成交割，公司表示對 2025 年營收/獲利影響不重大。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Arm Artisan Foundation IP Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-arm-artisan-foundation-ip.html) | moat_trend,thesis.H |
| major_events#3 | + | 2025-11-03 | Cadence 完成收購 Secure-IC（嵌入式資安 IP 廠商），2025-11-03 完成交割，鎖定車用/資料中心/航太國防/行動/IoT 等終端的嵌入式安全需求。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Secure-IC' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-secure-ic.html) | moat_trend |
| major_events#4 | - | 2025-07-28 | Cadence 就 2015-2021 年間銷售 EDA 工具與 IP 予中國國防科技大學（NUDT，美國商務部 Entity List 上的中國軍方大學）一案，與美國 DOJ／商務部 BIS 達成和解：對美國母公司刑事一項共謀違反出口管制罪名認罪，支付刑事罰金約 $72M＋沒收 $45M（DOJ 側），另與 BIS 達成民事和解支付逾 $95M，合計對外揭露總額約 $140M（多家媒體引用 $140.6M 淨額），並承諾三年緩刑期內強化出口合規計畫與年度稽核。（註：此為 DOJ／BIS 出口管制刑事與民事執法案件，非 SEC 調查亦非財報重編，性質上最接近本軸「監管調查」類別故一併揭露。） | DOJ Office of Public Affairs press release: 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development) | thesis.R,decision_inputs.bear,moat_trend |
| major_events#5 | + | 2026-05-31 | Cadence 與 NVIDIA 於 Computex 2026 發表業界首個全自主（Level-5）虛擬工程師 AI agent（ChipStack AI Super Agent 擴展版），結合 NVIDIA Nemotron 模型與 OpenShell runtime，宣稱可將典型五週的驗證流程縮短至一天內、RTL 驗證加速逾 40 倍；Level-5 自主能力預計 2026 下半年提供早期存取客戶。 | Cadence newsroom press release: 'Cadence Unveils Industry's First Fully Autonomous Virtual Engineer for Chip Design, powered by NVIDIA' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-unveils-industrys-first-fully-autonomous-virtual.html) | thesis.H,moat_trend |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "Cadence Design Systems acquisition merger 2025 2026",
   "Cadence completes acquisition Arm Artisan foundation IP business date 2025",
   "Cadence Secure-IC acquisition completed date 2025"
  ],
  "findings": [
   {
    "claim": "Cadence 完成收購 Hexagon 設計與工程（D&E）事業，約 €2.7B／$3.2B，2026-02-23 交割完成，預期 2026 年貢獻約 $160M 營收、非 GAAP EPS 稀釋約 28 美分（2027 年轉增益）。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Hexagon's Design and Engineering Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-completes-acquisition-of-hexagons-design-and-engineering.html)",
    "as_of": "2026-02-23",
    "direction": "0",
    "affects": [
     "thesis.H",
     "decision_inputs.bear",
     "moat_trend"
    ]
   },
   {
    "claim": "Cadence 收購 EMA Design Automation（PCB 設計領域），2026-03-05 完成，金額未揭露。",
    "source": "Tracxn deal brief: 'Cadence Acquires EMA' (tracxn.com/d/insights/merger-acquisition-deals-brief/cadence-acquires-ema/__2GFeel2DERN2Huua_VuEI8_1eWy4KiZTZGAH09AhLl4)",
    "as_of": "2026-03-05",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   },
   {
    "claim": "Cadence 完成收購 Arm Artisan foundation IP 業務（標準元件庫/記憶體編譯器/GPIO），2025-08-27 交割，對 2025 年營收獲利影響不重大。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Arm Artisan Foundation IP Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-arm-artisan-foundation-ip.html)",
    "as_of": "2025-08-27",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H"
    ]
   },
   {
    "claim": "Cadence 完成收購嵌入式資安 IP 廠商 Secure-IC，2025-11-03 交割。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Secure-IC' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-secure-ic.html)",
    "as_of": "2025-11-03",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems class action lawsuit securities fraud",
   "Cadence Design Systems shareholder derivative lawsuit export control settlement 2025"
  ],
  "findings": [],
  "note": "僅查得 1999 年（Spett v. Cadence，1999 Q1 財報相關，已被法院駁回）與 2008-2009 年（$38M 和解，2008 股價重挫相關）兩起歷史證券集體訴訟，均非近 12 個月事件；亦未查得因 2025-07 出口管制和解而起的股東衍生訴訟報導。"
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems acquisition merger 2025 2026",
   "Cadence Design Systems new product launch 2025 2026 AI chip design platform"
  ],
  "findings": [],
  "note": "非藥品/醫療器材業務（Cadence 為半導體電子設計自動化 EDA 軟體公司），已查證無相關臨床試驗/FDA 監管動作；上述查詢及其餘 6 條本輪搜尋亦均未出現任何臨床/FDA 相關訊息。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems new product launch 2025 2026 AI chip design platform",
   "Cadence Design Systems acquisition merger 2025 2026"
  ],
  "findings": [],
  "note": "近 12 個月查得的產品相關新聞均為新品發表（ChipStack AI Super Agent／Level-5 自主虛擬工程師／ViraStack／InnoStack／AgentStack），未查得任何產品下架、召回或監管警告信事件。"
 },
 "sec_investigation_restatement": {
  "status": "found",
  "queries_run": [
   "Cadence Design Systems SEC investigation restatement China export",
   "Cadence Design Systems SEC subpoena investigation 2025 2026"
  ],
  "findings": [
   {
    "claim": "Cadence 因 2015-2021 年間對中國國防科技大學（NUDT，美國商務部 Entity List 上之中國軍方大學）銷售 EDA 軟硬體與 IP，遭美國 DOJ 與商務部 BIS 調查；2025-07-28 達成和解，母公司就一項共謀違反出口管制罪名認罪，DOJ 側罰金+沒收約 $117M（$72M 罰金＋$45M 沒收），另與 BIS 民事和解逾 $95M，對外揭露合計約 $140M（部分媒體引用淨額 $140.6M），並承諾三年緩刑期內強化出口合規與年度稽核。查無獨立的 SEC 會計調查或財報重編事件——此案主體機關為 DOJ／商務部 BIS，非 SEC，且不涉及財報重編，列於本欄位係因五分類中無獨立「出口管制執法」桶、性質最相近之政府調查/裁罰事件。",
    "source": "DOJ Office of Public Affairs: 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development)",
    "as_of": "2025-07-28",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear",
     "moat_trend"
    ]
   }
  ],
  "note": "本條實為 DOJ/BIS 出口管制刑事+民事執法案件，非 SEC 證券監理調查、亦非財報重編；因五分類無專屬桶而歸類於此，判斷層引用時應正確標註機關與性質，不得誤寫為「SEC 調查」或「會計重編」。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_CDNS_20260504.html",
 "date": "20260504",
 "schema": "v12.3",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 340.94,
 "revlog": {
  "status": "ok",
  "text": "版本修訂紀錄\n\n版本 | 日期 | 變更\nv12.2（Inception） | 2026-05-04 | CDNS 首次 v12.2 DD（Q1 26 4/27 Beat 後重新評估）。下次年度對照 2027-05-04。\nv12.3 upgrade | 2026-05-16 | Schema 升至 v12.3（win-20260516-1833-654b）。§9 護城河二維化（execution 8 / pricing power 9）；§5.F Single Thing 新增（Hyperscaler in-house Agentic EDA binary event）；§8.B 定價 vs 量拆分 + 有機/無機 3Y 趨勢；§8.H 客戶結構深度（top-5/10% + 關係類型 + 議價風險）；§11 議價權三段獨立（對上游 / 對下游 / 地緣）；§12 M&A 5Y track record + SBC 剔除 EPS CAGR 計算；§13.4 peer tier 修正（EDA Oligopoly，SNPS 唯一 anchor，移除誤引 AVGO 等）；§10 FCF lumpiness 新增；dd-meta schema → v12.3，stress → 2/2，moat_execution=8, moat_pricing_power=9；§2.E QC-29 4 情境表砍除；§13.0/13.3/13.5/§7 低估值四問砍除。Verdict 維持 A（§1 / §2 H / §13 三處一致）。"
 },
 "prior_meta": {
  "ticker": "CDNS",
  "company": "Cadence Design Systems",
  "date": "2026-05-04",
  "schema": "v12.3",
  "price_at_dd": 340.94,
  "currency": "USD",
  "signal": "A",
  "trap": "🟢",
  "trap_label": "非陷阱",
  "moat": "A",
  "moat_score": 9,
  "moat_execution": 8,
  "moat_pricing_power": 9,
  "val": "🟡",
  "ma": "✅",
  "benchmark_regime": "正常",
  "fpe_fy1": 43.16,
  "fpe_fy2": 35.89,
  "pct_5y": 53,
  "peg_3y": 1.86,
  "peg_fy2": 1.55,
  "rr_short": -0.39,
  "rr_mid": 0.2,
  "rr_long": 1.22,
  "target_short": 277,
  "target_mid": 361,
  "target_5y": 540,
  "upside_short_pct": -19,
  "upside_mid_pct": 6,
  "upside_5y_pct": 58,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "growth_durability": 9,
  "quality_score": 9,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "A（核心候選·Q1 Beat + 上修 FY 指引 + Backlog 8B record 強化 thesis；4 週 +22% 接近警戒，等回測 BB 中軌 ~303）",
  "inception_dd": "DD_CDNS_20260504.html",
  "inception_date": "2026-05-04",
  "next_yoy_review": "2027-05-04",
  "oneliner": "Q1 26 Rev 1.47B(+19%)+EPS 1.96 Beat+OPM 44.7%+Backlog 8B／FY26 raised 6.12-6.22B EPS 7.85-7.95／護城河A EDA雙寡占+Agentic AI／FPE 36-43x PEG 1.55 估值🟡／MA✅但4w+22%／A 等回測303"
 },
 "drift_watch": [
  "dca_verdict",
  "dca_role",
  "signal",
  "val",
  "ma",
  "trap",
  "moat_trend",
  "runway_post_y5",
  "asym_ratio",
  "ev5y_pct",
  "irr_base_pct",
  "max_dd_pct",
  "bull_5y_price",
  "bear_5y_price",
  "p_bull_pct",
  "p_bear_pct",
  "rearm_trigger",
  "price_at_dd",
  "archetype",
  "cycle_position"
 ],
 "H": {
  "status": "ok",
  "format": "table",
  "rows": [
   {
    "id": "H1",
    "text": "EDA 雙寡占穩定，CDNS 維持 ~33% 市佔",
    "columns": {
     "Sourced Floor": "Backlog ≥ 7B 兩季（§6 Backlog $8B record，Q1 26 earnings call）；CDNS 市佔 33% 估算基於 Gartner/IDC EDA TAM $15B × Rev $5.3B",
     "2Y 驗證點": "Backlog 持續 ≥ 7B",
     "5Y 驗證點": "FY30 Rev 8-9B，CAGR 15%",
     "10Y 驗證點": "2036 Rev 12B+，雙寡占未被瓦解"
    }
   },
   {
    "id": "H2",
    "text": "AI Super Agent + Agentic AI 推動 ARR 從 ~80% → 90%（2030）",
    "columns": {
     "Sourced Floor": "ARR 基期 80% 估算來自 §8 訂閱模式說明；AgentStack 2025 發布（Cadence press release 2025）",
     "2Y 驗證點": "FY27 mgmt 揭露 AI 工具 ARR 佔比",
     "5Y 驗證點": "AI 工具占 Rev 30%+",
     "10Y 驗證點": "持續為 EDA 主要 ASP 驅動"
    }
   },
   {
    "id": "H3",
    "text": "Non-GAAP OPM 從 44% → 47% 擴張",
    "columns": {
     "Sourced Floor": "Q1 26 OPM 44.7% record（earnings release）；FY26 mgmt guide 43.5-44.5%；漂移觸發：連 2 季 OPM",
     "2Y 驗證點": "FY27 OPM ≥ 45%",
     "5Y 驗證點": "FY30 OPM 47%",
     "10Y 驗證點": "maintain 45%+"
    }
   }
  ]
 },
 "R": {
  "status": "unavailable"
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_CDNS_20260504.html",
  "date": "20260504",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_CDNS_20260504.html",
  "date": "20260504",
  "days_from_365d_mark": 241
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "CDNS",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "A",
  "date": "2026-05-04",
  "freshness": "aging",
  "source": "docs/dd/DD_CDNS_20260504.html"
 },
 "decision_history": [
  {
   "date": "2026-05-04",
   "verdict": null,
   "role": null,
   "price_at_decision": 340.94,
   "fundamental_grade": "A",
   "to_date_pct": -19.3,
   "days": 119,
   "source_report": "docs/dd/DD_CDNS_20260504.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/CDNS.md\n[internal-note] 2026-05-17  Cold Review — CDNS v12.3 品質稽核\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_CDNS_20260517.md\n[dca] 2026-05-11  DCA|CDNS Cadence Design Systems|2026-05-11\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_CDNS_20260511.md\n[dca] 2026-05-07  DCA · CDNS · 2026-05-07\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_CDNS_20260507.md\n[dd] 2026-05-04  DD|CDNS Cadence Design Systems|2026-05-04\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_CDNS_20260504.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "ok",
 "primary": {
  "theme": "AI EDA + IP",
  "path": "docs/id/ID_AIEDAIP_20260427.html",
  "skill_version": "v2.3",
  "as_of": "2026-04-27",
  "facts": {
   "status": "ok",
   "sections": {
    "supply": "PART III · SUPPLY SIDE\n 供給側：三寡占之上，多了一條 收費模式遷移 暗線\n EDA 的供給故事過去是「SNPS／CDNS／Siemens 三寡占誰工具強」；2025-26 起多了一條暗線——收費模式從 per-seat 跳 per-tapeout／token，把 EDA 廠的營收與 AI 晶片設計活動量直接綁定，同時 ARM 把 IP 從藍圖升級成子系統。\n\n 供給端是 Synopsys（龍頭，~31% 份額、併 Ansys 後寬口徑 ~44%）＋ Cadence（純 EDA pure play，~30%）＋ Siemens EDA（~13%）的三寡占，毛利集體高檔（CDNS non-GAAP op margin ~45%、SNPS 軟體業 GM 80%+）。瓶頸（對後進者而言）是三重鎖定：① foundry 強制簽核工具（Calibre／PrimeTime）；② 多年 ELA 與遷移成本（一顆先進晶片綁定整套工具鏈，換工具＝重跑驗證）；③ AI agent 平台的客戶 NRE lock-in。任一鬆動才可能破寡占，而三者 2026 全部 binding。這是賣方市場的結構基礎，也是「估值有支撐但有機增速要看模式兌現」的同一枚硬幣兩面。\n\n \n Inference · 供給\n 收費模式從 per-seat 跳 per-tapeout／token，把 EDA 的成長天花板拆掉\n 前提：AgentEngineer／AgentStack early-access（H2 2026）＋ Synopsys 續約 ~20% 漲價靠 token ＋ Cerebrus 消費型 SaaS ＋ AI ASIC／chiplet 推升 tapeout 量\n 當收費基底從「設計師人頭」變成「設計活動量」，EDA 營收第一次與 AI 晶片被設計出來的數量直接掛鉤——一個團隊跑更多 AI agent、更多 tapeout＝付更多錢，而不再被「客戶招幾個工程師」封頂。這把 2000 式「下游晶片投資放緩 → EDA 訂單跟著崩」的劇本變難複製（短期靠 backlog 與 ELA 緩衝），同時打開「使用量隨 AI 設計爆發非線性成長」的新天花板。\n 可證偽條件：若 2026-2027 續約漲幅回落至個位數、Synopsys 有機核心 EDA 增速連兩季 &lt; +8%、AI 工具的 token／消費型營收占比不見上升，則「收費模式重定價」只是行銷話術而非定價權，estimate 與估值都要下修——這正是 PART I 監測點 1 的設計理由。\n \n\n \n 利潤池遷移 · 毛利率／成長為各家最新季 T1 實際值 / 區間\n \n環節 | 代表玩家 / 體質 | 遷移 | 搶 / 被搶\nEDA 工具（雙寡占） | SNPS ~31% / CDNS ~30% 份額 | ↑ | AI 工具＋multiphysics 拉高 wallet share\nEDA AI 平台（新層） | AgentStack / AgentEngineer（消費型） | ↑ | 新環節，per-tapeout／token 重定價\nIP 授權（CSS 升級） | ARM CSS royalty rate ~10%（v9 兩倍） | ↑ | 從「賣藍圖」搶到「賣子系統」溢價\n連結 IP（chiplet/SerDes） | Alphawave（已併入 QCOM 2025-12） | ↑ | 224G/UCIe 被高通整併進資料中心\n實體驗證簽核（鎖喉） | Siemens Calibre ~85%+（foundry 強制） | → | 結構性 tenure，難被替代\nAI 晶片設計（買方） | NVDA / AVGO / hyperscaler ASIC | ↓ | EDA/IP 是 COGS；自研設計反壓 IP 議價\n\n \n 怎麼讀：利潤往「EDA 雙寡占＋ARM IP」集中（同享高檔毛利且都在 ↑），但 2025 起出現兩條新分支——EDA AI 平台層把收費從人頭重定價成活動量、ARM CSS把 IP 從藍圖升級成子系統。binary 競爭軸：Synopsys 用 Ansys 開 multiphysics 全 stack 護城河（Cadence／Siemens 落後 18-24 月）vs Cadence 用 AgentStack＋NVIDIA Nemotron 拼 agentic 自動化速度。誰能把「按使用量收費」坐實成定價權，誰就拿到下一輪 wallet share——這是「EDA 從 per-seat 變 per-activity」的供給側證據。對 Siemens Calibre 而言是 small-but-permanent 的 foundry tenure（簽核鎖喉），但非成長主軸。",
    "demand": "PART IV · DEMAND SIDE\n 需求側：AI tapeout 爆發是真的，capex 增速減速也是真的\n 最不可替代的是 hyperscaler 自研 ASIC 與 chiplet 拼接帶來的 tapeout 與 IP 用量爆發（一顆先進 ASIC 的 EDA＋IP 投資從 $50-200M 飛到 $400-600M+）；最脆弱的是「AI capex 持續加速」這個前置訂單邏輯的隱含假設。\n\n 需求源頭是 AI 晶片設計活動：hyperscaler（AWS Graviton／Google Axion／MSFT Cobalt／Meta MTIA）大規模自研 ASIC，疊加 NVDA／AMD 每代加速器，把每顆先進晶片的 EDA＋IP 投資從 2020 的 ~$50-200M（單晶片）推到 2026 的 ~$200-400M（chiplet 跨代拼接），2028+ 同代雙拼 ~$400-600M——這不是「漲價」，是 chiplet 拼接讓每個 chip 的設計／驗證／整合量乘倍。下游出錢方是四大 hyperscaler，2026 AI capex 合計約 $725B。需求廣度（NVDA＋AMD＋hyperscaler ASIC＋主權 AI）稀釋了單一買家放緩的傳導，但增速本身在減速，且大客戶自研設計能力反向壓 IP 議價（AVGO 等 ASIC 大戶內製設計）——這是裁決從純「結構性多」打成「賣方市場但有 kill 未排除」的根源。\n\n \n 需求三角驗證 · top-down vs bottom-up 對帳（口徑不同，量級判斷）\n \n視角 | 數值 | 口徑 / 來源\n下游 AI capex（top-down） | 四大 ~$725B（2026） | 各家曆年 guidance 聚合（個別法說 T1）\nEDA+IP TAM（中游加總） | 純 EDA ~$18B(2025) → ~$28-31B(2030) | SemiAnalysis / 市研機構，CAGR ~8-11%（純 EDA）\n三家頭部 run-rate（bottom-up） | SNPS FY26 ~$9.7B / CDNS ~$6.2B / ARM ~$5B+ | 全公司 rev（含 Ansys／IP／系統），非純 EDA-only\n\n \n 怎麼讀：三家全公司 run-rate（~$21B）大於純 EDA TAM（~$18B）——缺口來自口徑（含 Ansys simulation／IP／系統設計／emulation 硬體），&gt;20% 差異已由「寬 vs 窄口徑」解釋，採信窄口徑純 EDA 算份額、寬口徑算 TAM 上限。真正要對帳的是「capex $725B 能不能持續」——EDA 的 tapeout 用量建立在 AI 設計活動持續爆發上；若 2027 capex 增速顯著降檔甚至反轉，tapeout 量會延後 6-12 個月傳導、續約漲幅與 token 收入都會被重談。短期採信下游 capex（法說承諾最硬＋backlog $8B 鎖死），但這是「採信」不是「確定」。\n\n \n Inference · 需求\n backlog 把短期鎖死，但鎖的是「合約量」不是「續約定價權」\n 前提：CDNS backlog $8B（覆蓋 FY26 rev ~67%）＋ 多年 ELA ＋ hyperscaler 2026 AI capex ~$725B（高基期）但 2027 預期增速降檔 ＋ 大客戶內製設計\n backlog 與多年 ELA 讓 2026-2027 的營收底幾乎是確定事件（合約量已綁），這是 12M 裁決「賣方市場」的硬底。但 backlog 的續約定價假設客戶會持續加碼 tapeout 與 AI 工具用量；一旦 capex 增速反轉或大客戶把設計能力內製，2027-28 的續約漲幅與 token 收入就是談判變數，而非保證。\n 可證偽條件：① 任一 Big-4 hyperscaler 宣布 2027 AI capex YoY 跌破 +20% 甚至負增長；② AVGO／hyperscaler 把更多 IP／設計流程內製、壓 ARM/Synopsys IP 議價；③ 續約出現實質降價或 ELA 縮表。任一發生，「backlog 保護」由緩衝變裂縫。\n \n\n \n 多空為何都對\n 多頭測的是賣方市場黏性（backlog $8B、遷移成本、licensing +29%），空頭測的是定價權兌現與 capex 增速（收費模式能否坐實、AI ROI、capex 能否續加速）——兩者測的不是同一件事，可同時為真：EDA/IP 確實被多年 ELA 鎖死（多頭對），但鎖死不代表續約能永遠雙位數漲價（空頭對）。本報告因此把判斷重心放在「收費模式能否兌現定價權、capex 何時減速」，而非「EDA 估值貴不貴 yes/no」。"
   }
  },
  "machine": {
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "priced_in": null,
   "conviction": "high",
   "for_stage2_only": true
  }
 },
 "candidates": [
  {
   "theme": "AI EDA + IP",
   "path": "docs/id/ID_AIEDAIP_20260427.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-27",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  }
 ],
 "note": null
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/CDNS/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "CEO announces the company is raising its full-year 2025 outlook to approximately 14% revenue growth and 18% EPS growth.",
      "quote": "raising our full year outlook to approximately 14%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives Q4 2025 revenue guidance range.",
      "quote": "revenue in the range of $1.405 billion to $1.435 billion",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives updated full-year 2025 revenue guidance range.",
      "quote": "revenue in the range of $5.262 billion and $5.292 billion",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO explicitly declines to give FY2026 guidance on this call, deferring to a later date.",
      "quote": "we won't guide FY '26 today",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO gives updated full-year 2025 GAAP operating margin guidance range.",
      "quote": "GAAP operating margin in the range of 27.9% to 28.9%.",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO states Q3 2025 actual GAAP operating margin.",
      "quote": "GAAP operating margin was 31.8%",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO explains Q4 opex is partly offset by new expenses from recently closed acquisitions.",
      "quote": "offset a little in Q4 by some new expenses",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst asks how Cadence's strong IP growth squares with a competitor's publicly expressed concerns about its own IP business.",
      "quote": "because your competitor expressed",
      "speaker": "Vivek Arya (Analyst, BofA Securities)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "competition",
      "claim": "CEO argues Cadence's IP business is more profitable than the general IP industry, differentiating it from competitors.",
      "quote": "I think it's much more profitable",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites Q3 expansion of the Samsung partnership across core EDA and system software.",
      "quote": "we meaningfully expanded our partnership with Samsung",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites deepened collaboration with OpenAI on the Palladium emulation platform in Q3.",
      "quote": "We deepened our overall collaboration with OpenAI",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites Samsung's SF2 tape-out using Cadence Cerebrus AI Studio as a customer productivity win.",
      "quote": "Samsung U.S. taped out a SF2 design using Cadence Cerebrus",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites customer-reported verification throughput gains from Verisium SimAI, highlighted by NVIDIA, Samsung and Qualcomm at CadenceLIVE India.",
      "quote": "5x to 10x improvement in verification throughput",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "risk",
      "claim": "CFO states the 2025 outlook assumes today's export control regulations remain substantially similar for the rest of the year.",
      "quote": "export control regulations that exist today remain",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "risk",
      "claim": "When asked about China tariff-related risk to guidance, CFO says reports suggest geopolitical tensions are lower than commonly expected.",
      "quote": "geopolitical tensions are lower than people expect",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO states Q3 2025 share repurchase amount.",
      "quote": "we used $200 million to repurchase Cadence shares",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the definitive agreement to acquire Hexagon's D&E business, including its MSC Software unit.",
      "quote": "signed a definitive agreement to acquire Hexagon's D&E",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO reiterates the 2025 outlook includes using at least 50% of annual free cash flow for buybacks.",
      "quote": "our annual free cash flow to repurchase Cadence shares",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the combined SD&A business run rate should cross $1 billion in 2026 once the Hexagon acquisition closes.",
      "quote": "$1 billion in 2026 if the acquisition closes.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states he would be surprised if the IP business does not grow faster than the corporate average given its profitability profile.",
      "quote": "our IP business does not grow better than Cadence average",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 給出 2026 全年營收指引區間。",
      "quote": "revenue in the range of $5.9 billion to $6 billion",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 給出 Q1 2026 營收指引區間。",
      "quote": "revenue in the range of $1.420 billion to $1.460 billion",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 表示 2026 財年經常性營收佔比預期維持在約 80%，與 2025 一致。",
      "quote": "recurring revenue mix to remain around 80% in fiscal '26",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "margin",
      "claim": "CFO John Wall 引用 2025 年實現的增量營益率數字。",
      "quote": "we achieved incremental margin of 59%, I think",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "margin",
      "claim": "CFO John Wall 給出 2026 年非 GAAP 營業利益率指引區間。",
      "quote": "non-GAAP operating margin in the range of 44.75% to 45.75%",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CEO Anirudh Devgan 回應分析師關於客戶用 AI 取代 EDA/IP 工具的疑慮，表示沒有看到客戶減少使用的討論。",
      "quote": "no discussion with customers of reducing the usage",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CFO John Wall 說明 2026 指引已內建的假設：出口管制法規維持與現況大致相同。",
      "quote": "export control regulations that exist today remain",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CFO John Wall 給出 2026 年中國營收佔比預期區間，與過去兩年相近。",
      "quote": "expect it will be in a similar range, 12% to 13% for 2026",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 回應對新創公司的看法，強調對自身研發團隊的信心。",
      "quote": "we are very confident in our own R&D",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 表示公司在多個產品線的競爭地位有所改善。",
      "quote": "our competitive position has improved",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 表示公司在硬體、IP 等多個主要產品線都在取得市佔率。",
      "quote": "we are taking share in all our major product segments",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "product",
      "claim": "CEO Anirudh Devgan 描述 ChipStack AI Super Agent 帶來的生產力提升幅度。",
      "quote": "provides up to 10x productivity improvement",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "product",
      "claim": "CEO Anirudh Devgan 描述 3D-IC 平台在多晶片架構轉型中的角色。",
      "quote": "a key enabler for the industry's transition to multichip",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 列舉 ChipStack 已獲得的客戶背書名單。",
      "quote": "endorsements from Qualcomm, NVIDIA, Altera and Tenstorrent",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 引用 Samsung U.S. 使用 Cadence Cerebrus AI Studio 流出 SF2 設計的生產力成果。",
      "quote": "achieving 4x productivity improvement",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 引用一家大型跨國電子暨電動車客戶使用 AI 驅動設計遷移得到的佈局效率成果。",
      "quote": "reported a 30% layout efficiency gain",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO John Wall 給出 2026 年自由現金流用於庫藏股回購的預期比例。",
      "quote": "of our free cash flow to repurchase Cadence shares in 2026",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO John Wall 陳述 2025 全年實際用於庫藏股回購的金額。",
      "quote": "used $925 million to repurchase Cadence shares",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO Anirudh Devgan 陳述 2026 年開年時的在手訂單積壓（backlog）金額創新高。",
      "quote": "we began 2026 with a record backlog of $7.8 billion",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO John Wall 揭露 2026 年營收中來自期初在手訂單積壓的占比透明度指標。",
      "quote": "around 67% of 2026 revenue is coming from beginning backlog",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO Anirudh Devgan 回應分析師關於 AI 時代合約年期是否會像 2000 年代那樣縮短的提問，表示目前未見合約年期變化。",
      "quote": "not seeing any change in the duration, so which is good",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 表示上修 2026 全年營收成長展望至 17%",
      "quote": "raising our 2026 revenue growth outlook to 17%",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 2026 全年營收區間指引",
      "quote": "$6.125 billion to $6.225 billion",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 給出 2026 全年 Non-GAAP 營益率指引區間",
      "quote": "Non-GAAP operating margin in the range of 43.5% to 44.5%.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明 Hexagon 併購對 2026 EPS 造成稀釋",
      "quote": "We expect it to be dilutive to the tune of about $0.28.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明近期有機成長的邊際利潤率水準",
      "quote": "closer to 60% these days than 50%.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 針對 AI 是否威脅 EDA 基礎工具可防禦性，表態對自身基礎工具地位有信心",
      "quote": "very confident in our position in the base tool",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 評論基礎工具的競爭地位仍屬業界最佳",
      "quote": "our competitor of the base tool is anyway best-in-class",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說明新推出的三個 AI Super Agent（含 ChipStack）串連整個晶片設計流程",
      "quote": "Together, these solutions span the entire chip design flow",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "product",
      "claim": "CEO 介紹 AgentStack 作為 AI Super Agent 的頭部代理框架",
      "quote": "AgentStack, the head agent framework for our AI Super Agent",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及與某全球晶圓代工大廠簽下 IP 業務史上最大單一合約",
      "quote": "closed a record deal with a leading global foundry",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及某半導體設計大廠大幅增加 Innovus 用量",
      "quote": "significantly increased their Innovus usage",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及一家指標型 AI 基礎設施公司擴大採用簽核解決方案",
      "quote": "a marquee AI infrastructure company expanded their usage",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 指出 2026 財測假設出口管制法規維持現狀不變",
      "quote": "export control regulations that exist today remain",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 說明中國占 Q1 營收比重及全年預期",
      "quote": "China, it was 13% of Q1 revenue",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 揭露 Q1 已動用 2 億美元庫藏股回購",
      "quote": "we used $200 million to repurchase Cadence shares",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 指引 2026 全年約用 50% 自由現金流回購股票",
      "quote": "approximately 50% of our free cash flow to repurchase",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 說明 Hexagon 收購的股票/現金支付結構",
      "quote": "we paid 30% of the acquisition price in shares and 70%",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 預期 Hexagon 併購案將於 2027 年轉為增益",
      "quote": "We'd expect it to be accretive in 2027.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 承諾 2030 年前推出下一代硬體平台 Z4",
      "quote": "we'll have a Z4 system before 2030.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱對 2026 年的能見度與過去持平或更好，過去在軟體端一向能見度較強",
      "quote": "as good, if not better than what we've had before.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱過去 3-5 年平均營收成長約 14%，其中約 2% 來自併購、12% 為有機成長",
      "quote": "we've probably been averaging around 14% revenue growth",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱公司通常以兩位數成長編列預算，實際結果常落在低雙位數(low teens)",
      "quote": "we budget for double-digit revenue growth",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱有機業務目標為 50% 以上增量利潤率，實際約達 60%",
      "quote": "We're probably hitting 60% organically.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱 2024 年未達成 50% 增量利潤率目標，原因是 BETA 併購太晚導致時間不足",
      "quote": "in 2024, we missed that 50% incremental margin target",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱若合併看 2024-2025 兩年，增量利潤率約落在公司長期平均的 53%-54%",
      "quote": "you're probably getting incremental margin of about 53%, which is kind of 53%, 54%",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC（自 Hexagon 拆分之 Design and Engineering 業務）獨立年收入約 2.8 億美元",
      "quote": "I think they were doing about $280 million of revenue stand-alone",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱若將 MSC 多年合約全部轉為年約，年化營收約 2 億美元",
      "quote": "probably a run rate of about $200 million a year",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC 併購後需 12-15 個月萃取綜效",
      "quote": "it will take us 12 to 15 months to extract those",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC 是公司歷來最大的一筆併購案，未來 1-2 年 M&A 重心將放在整合 MSC，其餘僅為小型 tuck-in",
      "quote": "MSC is the biggest thing we've probably ever done",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體模擬更新周期仍處早期階段，因設計複雜度大增使硬體模擬更關鍵",
      "quote": "it still feels like early innings because everything has become so much more complex",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體需求強勁，客戶即使拿不到 Z3 也會要求 Z2 系統",
      "quote": "Customers are asking for our Z2s if we can't get them to Z3.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體交期目標落在 8 到 22 週之間，目前落在中段位置",
      "quote": "We tried to aim for somewhere between 8 and 22 weeks of lead time.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱與台積電關係一向很強，近期在三星、英特爾的合作明顯增加",
      "quote": "we're very, very strong at TSMC, but we've been increasingly engaged in places like Samsung and Intel",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱非 AI 半導體客戶今年出現較大型合作案，似已觸底",
      "quote": "this year, we're seeing bigger engagements and I think they've probably found their base now at this point",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱對中國客戶需求韌性感到意外，限制鬆綁後客戶急欲拿到硬體積壓訂單",
      "quote": "we're surprised with the resilience of China customers",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 稱中國缺乏先進製程帶來的 AI 拉動效應，預期未來 3-5 年成長率略低於公司平均",
      "quote": "we don't see the same AI pull-through there as we're seeing in other regions",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 稱優先出貨中國硬體積壓訂單，使 Q3、Q4 末硬體積壓中中國占比將明顯低於平常",
      "quote": "there'll be much less of a percentage of China in it than there normally is",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "competition",
      "claim": "CFO 稱觀察到競爭對手 Synopsys 近年在 IP 業務上作風變得更偏交易型",
      "quote": "Synopsys maybe over the last few years have become more transactional",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "competition",
      "claim": "CFO 稱客戶不想被 Synopsys 或 ARM 綁死，希望有更多 IP 選擇，預期公司在 IP 市場競爭將隨業務下推而增加",
      "quote": "there'll probably be more competition from us",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 稱公司在 IP 業務上採長期夥伴模式，自稱是「農夫不是獵人」",
      "quote": "We're farmers, not hunters.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 稱回測過去十年，僅一年 Q4 訂單量未超過 Q4 營收，本季度延續強勁開局，預期將以創紀錄的積壓訂單收尾今年",
      "quote": "there's only 1 year where Q4 bookings didn't exceed Q4 revenue",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO confirms record backlog reported at end of Q3.",
      "quote": "We had record backlog.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says all indications point to Q4 ending with another record backlog.",
      "quote": "that we should end up with another record",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states current-year revenue growth is 14%, framed as a combined growth+margin \"rule of 58%\".",
      "quote": "revenue growth is 14%, okay? So that's a rule of 58%.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO says the company has raised margin every year for the past 5-10 years and expects to keep doing so.",
      "quote": "increased margin every year for the last 5, 10 years",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO flags that 2026 incremental margin may run lower before accelerating in 2027.",
      "quote": "in '26. Our incremental margin is a little lower, but '27",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the company continues to target 50%+ incremental margin.",
      "quote": "we are always shooting for 50% plus incremental margin.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the buyback is sized to ensure no net dilution from stock-based comp.",
      "quote": "we want to make sure that there is no dilution",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO reiterates the company returns 50% of cash flow to buy back stock.",
      "quote": "We will take 50% of our cash flow and we buy back our stock",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO says remaining cash may go to opportunistic M&A but the financial model is unchanged.",
      "quote": "it does not change our model, which we have done",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "competition",
      "claim": "CEO responds to the Synopsys-Ansys deal by saying Cadence already competes with them separately.",
      "quote": "already competing with them separately.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "competition",
      "claim": "CEO says the system business has grown roughly 25% a year for the last 5-6 years, pointing to the silicon-system merger thesis he pursued since 2018.",
      "quote": "our system business has grown like, I don't know, 25% a year",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says applying AI to Cadence's own products can deliver at least 10x productivity improvement.",
      "quote": "there's at least 10x productivity improvement we can deliver",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes the Palladium hardware-software emulation systems as core to modern chip design.",
      "quote": "Palladium and these hardware systems became basically",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says the emulator verifies chip designs roughly 1,000x faster than regular silicon.",
      "quote": "it will verify the design like 1,000x faster",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says IP segment is performing well across all reported areas.",
      "quote": "IP is performing well.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "customer",
      "claim": "CEO says roughly 45% of business now comes from system companies rather than traditional semiconductor customers.",
      "quote": "business is coming from system companies",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "customer",
      "claim": "CEO says China's share of EDA/software business has declined from about 16-17% a few years ago to about 11-12% now.",
      "quote": "Now it's like 11%, 12%. Still good",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says some China business shifted from Q2 to Q3 this year due to restrictions, now resolved.",
      "quote": "some of our business moved from Q2",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says geopolitical conditions are hard to predict but currently look stable for China design activity.",
      "quote": "geopolitical, but seems stable for now",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says China revenue came in better than the earlier prudent 'flat' guide, growing this year instead.",
      "quote": "China is growing this year, which is good.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO gives China's current share of total revenue and notes it is down from a few years ago.",
      "quote": "China will be in 11%, 12% of revenue",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states last year's revenue growth rate while discussing the growth+margin 'rule of X' framework.",
      "quote": "our revenue growth last year is 14%.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states this year's operating margin figure.",
      "quote": "our operating margin. This year is about 44.5%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO defines 'real margin' as operating margin minus stock-based compensation.",
      "quote": "real margin is, of course, operating margin minus SBC.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states incremental margin on the organic business.",
      "quote": "incremental margin on our organic business is close to 60%.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO restates the company's long-standing incremental margin goal.",
      "quote": "our goal, of course, is a 50% plus incremental margin",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO says buybacks funded by cash flow exceed the SBC percentage, aimed at avoiding dilution.",
      "quote": "So if we do like 8%, 9% SBC, we buy back more than that.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO states the primary strategic rationale for the Hexagon acquisition.",
      "quote": "the reason for Hexagon was, is primarily for physical AI.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes the acquired Hexagon simulation asset as the market leader in multibody dynamics simulation.",
      "quote": "the best multibody dynamic simulator, #1 in the market.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO says Cadence now has all five key advanced-node IP categories (UCIe, HBM, DDR, PCIe, SerDes).",
      "quote": "we have all the 5 key IPs at the most advanced nodes.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst references a recent stumble by a rival IP vendor as context for the question on Cadence's IP positioning.",
      "quote": "misstep perhaps with a rival recently in this space",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "CEO characterizes the NVIDIA business relationship as expanding.",
      "quote": "our business with NVIDIA is growing.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst asks about a reported nonexclusive collaboration deal between NVIDIA and Synopsys.",
      "quote": "a nonexclusive deal done or collaboration with Synopsys",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges Cadence was subject to a China-related export ban lasting six weeks during the year.",
      "quote": "we were banned for 6 weeks and all that.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "CEO notes a quarter-to-quarter revenue timing shift tied to the China situation.",
      "quote": "some revenue moved from Q2 to Q3.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "customer",
      "claim": "CEO gives the current split of customers between system companies and semiconductor companies.",
      "quote": "about 45% of our customers are now system companies",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states the concentration of revenue among a small set of large customers.",
      "quote": "70% of revenue is coming from about 60 companies",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to a systems business run-rate target, conditioned on M&A closing.",
      "quote": "we will cross like $1 billion run rate in systems",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits that no future M&A will be allowed to undermine the company's margin-expansion financial model.",
      "quote": "we'll not do any M&A that destroy this fundamental financial",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "Analyst raises margin pressure from the shift to annual subscriptions in the SD&A (systems) business as a topic needing explanation.",
      "quote": "a little bit of margin pressure as you transition to annual",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO 把 ChipStack Super Agent 定位為全新產品類別，非既有 GenAI 工具延伸",
      "quote": "This is a new product category, okay?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "ChipStack 首次讓公司具備自動寫 RTL 與 test bench 的能力，過去從未做到",
      "quote": "we have never done is ability to write RTL or test bench",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "Hexagon 併購帶來最準確的機器人模擬器 Adams，用來補強 physical AI 的 sim-to-real 精度",
      "quote": "Hexagon had the most accurate robotic simulator with Adams",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說 physical AI 用的矽（車用、機器人）與 data center AI 用的矽不同，偏混合訊號與低功耗",
      "quote": "physical AI is different than the silicon for data center AI",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "去年整體營收成長約 14%、EPS 成長約 20%",
      "quote": "we grew like 14% and EPS grew around 20%, right?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "公司近年 Rule of 40 落在高 50 幾，CEO 的目標是要突破 60",
      "quote": "we are in the high 50s, right, last few years",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "CEO 明確設定目標：Rule of 40 要跨越 60 這個門檻",
      "quote": "my goal is to crack 60.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "去年營業利益率 45%，但增量利潤率達 59%，即多增 1 億營收可多賺 5,900 萬利潤",
      "quote": "our margin last year was 45%, but incremental margin was 59%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Hexagon 併購今年對財務有影響，但主要落在融資面（稀釋/新增債務）而非營運面",
      "quote": "it is on financing side because there is some dilution",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO 預期 Hexagon 併購明年就能轉為加值（accretive）",
      "quote": "And next year, it should be accretive.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "HBM IP 是透過向 Rambus 收購取得，CEO 稱是一筆好收購",
      "quote": "we did acquire from Rambus. That's a great acquisition.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "除既有大型半導體客戶外，Tesla、Rivian、BYD 等 OEM 廠自研晶片也成為客戶",
      "quote": "now with OEM players like Tesla and Rivian or BYD",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "中國今年設計活動熱絡、physical AI 需求大，環境比去年初更穩定",
      "quote": "the environment seems more stable than beginning of '25",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "competition",
      "claim": "面對中國本土 EDA 業者競爭，CEO 稱一直都有競爭",
      "quote": "there's always some competition, I think.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "Palladium 硬體事業已連續 6 年寫下創紀錄成長",
      "quote": "we have like 6 years in a row of record growth in Palladium",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "risk",
      "claim": "CEO 對今年 Palladium 展望偏樂觀，但公司年初給假設時一貫採取保守態度",
      "quote": "we are more prudent in the assumption",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "risk",
      "claim": "針對 AI 是否顛覆傳統軟體商業模式的疑慮，CEO 回應這是放大而非顛覆",
      "quote": "for us, it's not disruption, it is amplification",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "Agentic EDA（ChipStack）貨幣化模式將採 token-based 計費",
      "quote": "yes, I think it will be token-based",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "公司希望新 agent 產品採基礎訂閱費加 token 用量的計費結構",
      "quote": "we would hope to have a base subscription plus tokens",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 表示 IP 業務已是連續第三年強勁成長，且公司不會提前宣稱未驗證的趨勢",
      "quote": "it's the third year of very good growth we will have",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states Cadence sets guidance one year at a time and characterizes the current year as very strong.",
      "quote": "we guide 1 year at a time.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states Cadence crossed the 'Rule of 60' this year.",
      "quote": "We crossed the rule of 60 this year.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO cites Cadence's incremental margin at 60%.",
      "quote": "Our incremental margin was 60%, okay?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states operating margin is roughly 44-45%, contrasted with the higher 60% incremental margin.",
      "quote": "our operating margin is about 44%, 45%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO asserts Cadence leads in both agentic AI tools and base EDA.",
      "quote": "Agentic, we are ahead. Base EDA, we are ahead.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO states Cadence is taking market share in IP.",
      "quote": "IP, we are taking share.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes Cadence's overall competitive position as the best it has ever been.",
      "quote": "we are in the best position we have ever been.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes focus on building the best 'super agents' across the ChipStack, ViraStack, and InnoStack product lines.",
      "quote": "super agents for ChipStack, ViraStack, this is InnoStack",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites Palladium as a unique hardware platform in Cadence's portfolio.",
      "quote": "Hardware, we have a unique platform with Palladium.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO quantifies internal AI-driven productivity target as at least 30% headcount reduction per project.",
      "quote": "at least 30% reduction in headcount per project",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "CEO describes customer concentration: roughly 60-70 large companies drive 60-70% of Cadence's revenue.",
      "quote": "big 60, 70 companies that drive 60%, 70% of our revenue.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "CEO references NVIDIA's Jensen Huang publicly discussing Cadence at COMPUTEX.",
      "quote": "Jensen talked about Cadence at COMPUTEX.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges the physical AI/robotics market trajectory could still move either direction.",
      "quote": "This may correct, may not correct.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "CEO states the exact timing of physical AI market adoption is hard to predict.",
      "quote": "exact timing is very difficult to say",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to continued hiring in the IP group despite AI-driven productivity gains reducing per-person headcount need.",
      "quote": "we will hire more, but they should be at least.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO sets an internal target of at least 2x productivity improvement in the IP R&D group from applying agentic AI.",
      "quote": "I am expecting at least a 2x productivity from the IP group.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層說今年營收成長已加速到 17% YoY。",
      "quote": "the revenue has accelerated to 17% year-over-year growth",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層說 non-GAAP 營業利益率將推升至 44%。",
      "quote": "op margin is going to push and reach 44%",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層說今年將超越 Rule of 60，是公司歷史紀錄。",
      "quote": "exceeding the Rule of 60 this year",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層重申目標是遞增利潤率北向 50%（含 -- 停頓語氣）。",
      "quote": "drive 50% -- north of 50% incremental margin, okay?",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "competition",
      "claim": "管理層說公司在各業務線都在全面搶市占。",
      "quote": "We are gaining share across the board.",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "competition",
      "claim": "管理層說公司目前是公司史上競爭力最強的時期。",
      "quote": "We're the strongest ever in our company history.",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "product",
      "claim": "管理層說 IP 策略聚焦在他們稱為「star IP」的高價值高成長 IP。",
      "quote": "we call it star IP, the high-value, high-growth IP",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "product",
      "claim": "管理層說過去幾個月已推出 3-4 個 super agent（agentic AI 產品）。",
      "quote": "3 or 4 super agents launched in the past couple of months",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "customer",
      "claim": "管理層說前 60-70 大客戶約占公司多數營收（60%-70%）。",
      "quote": "our top, say, 60, 70 customers, which is maybe a majority",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "customer",
      "claim": "管理層提到前一天剛宣布與 Intel 在 14A 製程上的合作。",
      "quote": "collaborate with Intel on its 14A journey yesterday",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說資本配置哲學一貫是有機投資優先。",
      "quote": "organic is the first order of business, okay?",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說要持續將自由現金流的 50% 以上用於股票回購。",
      "quote": "more than 50% of the free cash flow for share repurchases",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說不做大型變革性併購交易（且無支撐這類交易的 EBITDA 規模）。",
      "quote": "we don't do major transformative deals",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "commitment",
      "claim": "管理層說沒有意圖偏離既有的成長／利潤率／回購三重財務紀律。",
      "quote": "we don't have any intention to deviate from that philosophy",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "risk",
      "claim": "管理層說客戶端設計需求與工程師人力供給之間存在巨大落差。",
      "quote": "demand from our customers and the engineering supply",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "risk",
      "claim": "管理層引述 TSMC 對未來五年電晶體數量成長 48-50 倍的說法，指出設計複雜度壓力。",
      "quote": "48 to 50x kind of transistor growth in the next 5 years",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層說隨著矽與系統整合，SD&A／模擬的 TAM 有潛力隨時間翻倍。",
      "quote": "it could double the TAM over time",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Joseph Quatrochi (Wells Fargo) asked why Q3 opex came in better than expected but Q4 opex looks worse, and whether that relates to Artisan deal timing.",
      "response_pattern": "John Wall's first answer discussed broad-based execution and demand across product categories without addressing the opex timing question; the analyst had to re-ask ('I guess maybe just a question on the OpEx...') and John Wall asked him to repeat the question before giving a specific answer.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "question": "Charles Shi / Yu Shi (Needham) asked directly whether hardware growth could decelerate in year 3 of the current Z3/X3 upgrade cycle, as it did in year 3 of the prior Z2/X2 cycle.",
      "response_pattern": "John Wall responded 'We're trying to unpack it' and pivoted to general commentary on backlog, pipeline strength and revenue-curve shape across quarters, without directly confirming or denying a year-3 deceleration comparable to the prior cycle.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "question": "Gary Mobley (Loop Capital) 追問：SD&A 轉向一年期授權合約是否是 2025 年 SD&A 營收僅成長 13% 的原因？併入 Hexagon（原年化 $240M 營收水準）時是否也會因同樣的合約年期轉換而受限？",
      "response_pattern": "John Wall 承認 BETA 子公司 2025 年刻意轉向年度訂閱、影響年增率比較基期，但未直接量化該轉換對 SD&A 成長率的拖累幅度；對 Hexagon 僅給出約 $200M 年化營收的粗估數字，隨即表示『我們還沒有任何確定數字』並聲明本次指引未納入 Hexagon，未正面回應 $240M 數字是否因授權年期轉換而被下修。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Charles Shi / Yu Shi (Needham) 詢問：那家首次流出 COT 晶片的指標型雲端服務商，未來會如何在其他晶片項目上擴大 COT 比重？目前有多少雲端服務商正在做 COT？",
      "response_pattern": "Anirudh Devgan 明確表示『不會談論特定客戶的細節』，轉而用產業層級的通用敘事（大型雲端服務商自研晶片趨勢日益確立）回答，未直接回應該特定客戶的擴散節奏或時間表這個具體問題。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Gianmarco Conti (Deutsche Bank) 一次問了三個子問題：(1) ChipStack 與 Cerebrus 未來是否會有功能重疊/蠶食；(2) 在 AI 模型開發領域是否看到來自新創的競爭增加；(3) 在更高設計規模下同時跑更多 agent，是否會遇到算力方面的硬性限制。",
      "response_pattern": "Anirudh Devgan 開場先說線路有雜訊、『可能沒有聽全所有重點』，隨後回答了 ChipStack/Cerebrus 分工與新創競爭兩個子問題，但全程未觸及第三個子問題（更多 agent 並行時的算力限制）。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Andrew DeGasperi 追問 physical AI／agentic 貨幣化時程是否已提前於原先講的兩個合約週期",
      "response_pattern": "CEO 先鬆口說有可能提前於 2 個合約週期，隨即補一句「I don't want to predict too much」收回具體時程承諾，未給出可證偽的時間點",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "question": "AI 對 EDA 業務的貢獻能否量化，是否比之前更接近能給出數字的階段？",
      "response_pattern": "CFO 未給出量化數字，改以「很難拆分」帶過，轉談 AI 工具帶動的授權使用量與遞延／分期認列營收的質性描述，未正面回答是否更接近量化。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "question": "非 AI 半導體客戶的 EDA 支出是否會在明年加速？",
      "response_pattern": "CFO 以「很難說」開頭迴避直接判斷，隨即轉向設計複雜度上升、工具日益不可或缺的一般性說法，未針對「是否加速」給出明確答案。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "question": "And should we focus on that nonexclusivity in that deal when thinking about yourselves?",
      "response_pattern": "Management answered at length about the NVIDIA partnership's growth and gave a brief, sentence-cut-off mention of ongoing Intel discussions, but never addressed the specific question about the Synopsys deal's nonexclusivity.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "question": "What sort of margin pressure should we expect?",
      "response_pattern": "Management gave a qualitative, non-quantified answer ('there might be some 1-year impact... not going to be that significant given our scale') rather than a specific margin-pressure figure.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "question": "Has increased design complexity and AI tool adoption actually improved Cadence's pricing power versus history?",
      "response_pattern": "CEO reframes the answer around 'delivering value' and volume-driven growth philosophy without citing any specific pricing power data, price increases, or realized price/value capture metrics.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "question": "How much design activity is Cadence seeing in physical AI/robotics/edge AI, and should investors pay more attention now?",
      "response_pattern": "CEO expresses long-standing directional optimism ('big fan of physical AI... 3 to 7 years') but hedges specifics with 'exact timing is very difficult to say' and 'this may correct, may not correct', avoiding a concrete revenue or timing commitment.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "question": "分析師追問 agentic AI（super agents）產品的變現與營收貢獻，特別是「timing」（潛在時點）該如何預期。",
      "response_pattern": "管理層通篇談定價模式構想（訂閱＋消費制類比租車）、TAM 擴張與早期訊號「非常令人鼓舞」，但全程未給出具體變現時間表或營收貢獻數字，只以「we can be patient in terms of monetizing the top layer」帶過分析師具體問的 timing 提問。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    }
  ]
}

```

---

## judgment.json 全文

```json
{
  "meta": {
    "ticker": "CDNS",
    "date": "2026-09-05",
    "schema": "v15.2",
    "company_name": "Cadence Design Systems"
  },
  "oneliner": "EDA 雙寡占的 AI 放大器：Q2 營收 +24.2%、非 GAAP 營業利益率 45.5%、積壓 $8.1B 創高、全年上修至 +19%；股價自高點 −30% 跌回前份等待的回測帶，FY2027 本益比 30.7x／PEG 1.8 落合理帶；進場·核心，首階三分之一，加碼掛 $260 或 token 營收揭露；清倉級＝對華 EDA 許可制恢復",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": null,
    "confidence": "高",
    "fingerprint": "毛利 85.9%、非 GAAP 營業利益率 45.5%、FCF 利潤率 28.6%（TTM）、研發強度 33%、經常性營收 78%、資本支出佔營收約 3%——典型資本輕、高留存、寡占定價的軟體複利體"
  },
  "thesis": {
    "headline": "AI 晶片設計活動量爆發把 EDA 的收費基底從人頭改成活動量，Cadence 在 IP／硬體驗證／系統模擬三條線同時取份額；市場卻把它當「被 AI 顛覆的軟體股」定價",
    "holding_period": {
      "horizon": "長期 5-10 年",
      "driver": "護城河趨勢與 ROIC 方向為主：多年 ELA、代工廠簽核鎖定、agentic 收費模式兌現；財報單季波動是噪音",
      "signal_vs_noise": "訊號＝積壓年增、Core EDA 有機成長、系統廠客戶佔比、中國營收佔比與許可狀態；噪音＝單季硬體出貨時點、單季 FCF 起伏、軟體股板塊輪動"
    },
    "H": [
      {
        "id": "H1",
        "text": "EDA 雙寡占結構穩定，Cadence 在 IP／硬體／系統三線持續取份額，總營收年增維持雙位數中段以上",
        "2y": "FY2027 營收年增 ≥13%（共識 EPS 9.54 隱含）；積壓每季年增為正；Core EDA 有機成長 ≥12%",
        "5y": "FY2031 營收約 $11-12B（5 年 CAGR 約 13%）；EDA 市佔維持 ≥30%（2024 年約 30%）",
        "10y": "2036 年 EDA＋IP＋系統仍為三寡占，Cadence 份額不低於今日；系統廠客戶佔比 >50%",
        "threshold": "積壓 TTM 年增 <0 連 2 季＝削弱；Core EDA 有機成長 TTM <8% 連 3 季＝反轉",
        "source": "季度新聞稿（積壓／12 個月 RPO）、法說分段成長率；SemiAnalysis EDA 份額",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉；5Y 假設連 4 季 ≥5% 削弱"
      },
      {
        "id": "H2",
        "text": "agentic AI（ChipStack／AgentStack）以「基礎訂閱＋token 用量」計費，把成長天花板從客戶工程師人數解綁，AI 是放大而非顛覆",
        "2y": "FY2027 法說首次揭露 token／消費型營收或 AI 工具 ARR 佔比；客戶合約年期無縮短（管理層 2026-02 稱未見變化，來源：摘要）",
        "5y": "FY2031 AI 工具／消費型營收佔比 ≥20%；Core EDA 成長不因客戶人力減 30% 而降至個位數",
        "10y": "EDA 營收與 AI 晶片流片量掛鉤而非人頭；每顆先進晶片 EDA＋IP 投資持續上升",
        "threshold": "FY2028 仍無任何 token／消費型營收揭露＝削弱；Core EDA 成長連 4 季 <8% 且客戶引述 AI 減席＝反轉",
        "source": "法說與投資人會議管理層揭露；10-K 經常性／一次性營收拆分",
        "drift_rule": "5Y 假設連 4 季 ≥5% 削弱、連 6 季 ≥10% 反轉"
      },
      {
        "id": "H3",
        "text": "增量利潤率 60% 的營運槓桿把非 GAAP 營業利益率自 44-45% 推向 48-50%，Rule of 60 常態化",
        "2y": "FY2027 非 GAAP 營業利益率 ≥46%（Hexagon 轉為增益後）；FY2026 落在 43.75-44.75% 指引內",
        "5y": "FY2031 非 GAAP 營業利益率 ≥48%；SBC 佔營收 ≤9%",
        "10y": "營業利益率 50% 上下、FCF 利潤率 ≥35%",
        "threshold": "非 GAAP 營業利益率 TTM 年減 >100bp 連 2 季＝削弱；增量利潤率 <40% 連 2 年＝反轉",
        "source": "季度新聞稿非 GAAP 營業利益率；法說增量利潤率揭露",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "中國營收 12-13% 曝險於美國出口管制：2025-05 至 07 曾被要求許可六週、2025-07 認罪付 $140M、BIS 50% 規則暫停至 2026-11-09 到期；管理層財測明寫「假設管制維持現狀」",
        "h_ref": "H1",
        "clock": "🔥",
        "threshold": "中國營收佔比 TTM 連 4 季 <9%，或任一季因許可／管制致營收遞延 → 減碼；許可制正式恢復＝清倉級（見唯一事件）",
        "evidence_refs": [
          "reg_tariff_export#0",
          "reg_tariff_export#3",
          "geo_supply_chain#0",
          "geo_supply_chain#1",
          "geo_supply_chain#2",
          "geo_supply_chain#4",
          "major_events#4"
        ]
      },
      {
        "id": "R2",
        "text": "AI 資本支出增速 2027 年降檔：EDA 流片量與續約漲幅落後資本支出 6-12 個月，2026 為三年續約週期的低年、積壓創高靠新客；若 2027 超大規模業者資本支出年增跌破 +20%，token 收入與續約漲幅都要重談",
        "h_ref": "H2",
        "clock": "🔥",
        "threshold": "任一 Big-4 超大規模業者 2027 AI 資本支出指引年增 <+20%，且 Cadence 積壓年增連 2 季轉負 → 減碼；連 4 季 → 大動作",
        "evidence_refs": [
          "supply_demand_durability#3"
        ]
      },
      {
        "id": "R3",
        "text": "客戶集中與信用：約 60 家公司貢獻 70% 營收、系統廠 45%；最大單一帳戶 Intel 信評降至 BBB（距非投資級兩級）、Samsung 代工部門虧損延至 2028；無單一客戶 ≥10%，但前段客戶專案延遲直接打單季",
        "h_ref": "H1",
        "clock": "🐢",
        "threshold": "應收帳款任一客戶 ≥10%（10-Q）或前十大客戶任一破產／重組致營收遞延 >$100M → 減碼；系統廠佔比反轉下降連 2 年 → 重評 H1",
        "evidence_refs": [
          "customer_second_source#2",
          "customer_concentration_credit#1",
          "customer_concentration_credit#2",
          "customer_concentration_credit#3"
        ]
      }
    ],
    "single_thing": {
      "description": "美國商務部 BIS 正式恢復對中國（或中國軍事最終用戶）EDA 軟體與技術的出口許可要求（2025-05-23 那類通知），且未在 90 天內撤銷",
      "why_fatal": "中國佔營收 12-13%、增量利潤率 60% 意味遞減利潤率同樣陡：損失約 $750M 營收對應約 $450M 營業利益（約 16%），FY EPS 下修 15-18%；同時市場把政策風險折價疊上 AI 顛覆折價，倍數與盈餘雙殺",
      "if_happens": "首階倉位清倉，不等財報；重啟條件＝許可撤銷或中國佔比降至 <5% 且積壓仍年增",
      "how_monitor": "BIS 公告（bis.gov）、公司 8-K、每季法說中國佔比；2026-11-09 BIS 50% 規則暫停到期為第一個觀察日",
      "probability": "12-24 個月約 15%（2025 年曾發生一次且六週撤銷；美中談判中 10-K 明列可能重施）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "產業物理供需＝shortage（ID：AI EDA + IP，as-of 2026-04-27，Phase II、信心 high、priced_in 未填）。Phase II 經自身位置閘交叉驗證：積壓 $8.1B 創高、硬體交期 8-22 週中段、2027 設備銷售預期創高但 AI 資本支出增速減速——屬擴張中段偏後而非過熱，載入 II；priced_in 由本檔自判：股價 −30% 後已由「大多反映」退回「部分反映」",
    "bargaining": {
      "up": "上游＝雲端算力與 FPGA／ASIC 供應（Palladium 自研晶片）、模型供應商（NVIDIA Nemotron 合作）；無 top3 >70% 的集中供應揭露，議價權在 Cadence；硬體交期 8-22 週顯示供給端非瓶頸",
      "down": "下游＝約 60 家公司佔 70% 營收，多年 ELA、換工具＝重跑驗證；無單一客戶 ≥10%；系統廠 45%（兩年前 40%）自研晶片反而擴大用量；但 AVGO 與超大規模業者內製設計能力壓 IP 議價；管理層對定價權提問以「交付價值」帶過（來源：摘要）",
      "geo": "中國 12-13% 營收受出口管制、台灣為供應鏈樞紐風險（10-K）；2025 六週許可事件已實證政策可瞬間切斷；Section 232 半導體關稅不含 EDA 軟體"
    },
    "profit_pool_dir": "利潤往 EDA 雙寡占＋ARM IP 集中且皆 ↑（ID 供給側）；新分支＝EDA AI 平台層（per-tapeout／token 重定價）與 IP 子系統化；Cadence 環節 5 年池佔比淨流入（IP 三年高成長、系統業務年增約 25%）→ 非淨流出，Runway 不降檔",
    "tam_table": [
      {
        "segment": "Core EDA（Q1 2026 佔 71%，年增 18%）",
        "tam_now": "純 EDA 2026 約 $18.2B",
        "tam_5y": "2033 約 $33.5B（CAGR 9.1%）；另一口徑 2031 $30.7B（CAGR 8.1%）",
        "sam": "先進節點數位／類比／驗證全流程；代工廠簽核工具",
        "penetration": "Cadence 全球 EDA 份額約 30%（Synopsys 31%、Siemens 13%）",
        "cagr": "市場 8-9% vs Cadence Core EDA 18%",
        "position": "工具層（利潤最厚），簽核鎖喉點由 Siemens Calibre 持有",
        "pool_shift": "從人頭授權流向活動量計費；三寡占集體毛利高檔",
        "ceiling": "天花板＝設計活動量與 AI 資本支出；被替代路徑＝AI-native 設計流程繞過既有工具（目前三大廠自己在做 agent，無新進入者）"
      },
      {
        "segment": "半導體 IP（佔 14%，Q1 年增 22%、Q2 年增逾 40%）",
        "tam_now": "證據包未涵蓋（ID 稱 ARM CSS 權利金率約 10%）",
        "tam_5y": "證據包未涵蓋",
        "sam": "先進節點五大 star IP（UCIe／HBM／DDR／PCIe／SerDes）",
        "penetration": "與一家全球代工大廠簽 IP 史上最大單一合約（2 奈米）；Synopsys 承認 FY26 IP 清淡年",
        "cagr": "連續第三年高成長",
        "position": "從「賣藍圖」升級到「賣子系統」的中游",
        "pool_shift": "自 Synopsys／ARM 流向 Cadence（客戶不想被綁死，來源：摘要）",
        "ceiling": "天花板＝大客戶內製 IP；被替代路徑＝ARM CSS 子系統化與 AVGO 內製"
      },
      {
        "segment": "System Design & Analysis（佔 15%，Q2 年增 37%；含 Hexagon D&E）",
        "tam_now": "SD&A 2026 年化跨 $1B（含 Hexagon 約 $160M）",
        "tam_5y": "管理層稱矽與系統整合可讓 TAM 隨時間翻倍（來源：摘要）",
        "sam": "3D-IC、多物理模擬、physical AI（機器人／車用）模擬",
        "penetration": "Synopsys 併 Ansys 後在 multiphysics 全棧領先 18-24 月（ID）",
        "cagr": "系統業務過去 5-6 年年增約 25%（來源：摘要）",
        "position": "系統層新環節，Cadence 為追趕者",
        "pool_shift": "從 Ansys／Siemens 分食；Hexagon 補機器人模擬",
        "ceiling": "天花板＝physical AI 採用時點「很難說」（CEO，來源：摘要）；被替代路徑＝Synopsys-Ansys 綁定 device-to-system"
      }
    ]
  },
  "moat": {
    "execution": 9,
    "pricing": 8,
    "combined": 8.5,
    "grade": "A",
    "score": 8.5,
    "trend": "↑",
    "trend_evidence": "執行面擴大：IP 年增逾 40%（Q2 2026）對照 Synopsys 自認 FY26 IP 清淡年；硬體 30 家以上新客、前十大硬體客戶 7 家雙產品、Palladium 連續六年紀錄；系統廠客戶 45%（兩年前 40%）；一家超大規模業者以 Cadence 數位全流程完成首顆全 COT AI 晶片流片（2026-04）。定價面穩定：token 計費尚未揭露營收、CEO 對定價權提問以價值帶過（來源：摘要）。皆非縮減、對 thesis 更關鍵的執行維度擴大→↑；前瞻 2-3 年份額：IP／硬體續升、multiphysics 對 Synopsys-Ansys 追趕",
    "spread_table": [
      {
        "metric": "GAAP 營業利益率（TTM）",
        "self": 30.82,
        "peer": "SNPS 9.73／QCOM 23.28／ARM 17.3",
        "spread_pp": 21.09,
        "trend": "Q2 2026 GAAP 28.4% vs Q2 2025 19.0%（+940bp）；SNPS 受 Ansys 攤銷壓低",
        "note": "閘一：對最強直接同業 spread 為正且擴大 → 合併分 ≥8 成立"
      },
      {
        "metric": "毛利率（TTM）",
        "self": 85.87,
        "peer": "SNPS 73.47／ARM 97.54／QCOM 54.23",
        "spread_pp": 12.4,
        "trend": "逐季年減證據包未涵蓋；硬體佔比上升結構性壓毛利但仍 85%+",
        "note": "閘二未觸發（無 >1.5pp 年減證據）"
      },
      {
        "metric": "FCF 利潤率（TTM）",
        "self": 28.64,
        "peer": "SNPS 30.35／ARM 28.55／QCOM 23.64",
        "spread_pp": -1.71,
        "trend": "Q2 2026 單季 36.8%、Q1 20.8%（硬體與 IP 出貨時點）",
        "note": "與 SNPS 同級，非護城河差異來源"
      },
      {
        "metric": "研發強度（TTM）",
        "self": 33.02,
        "peer": "SNPS 32.11／ARM 57.49／QCOM 22.45",
        "spread_pp": 0.91,
        "trend": "與 SNPS 同水位；閘三絕對美元新增對照證據包未涵蓋 SNPS 季度數字",
        "note": "軍備競賽對等，無規模優勢質變警示"
      }
    ],
    "threats": [
      {
        "level": "⛔ 架構替代",
        "text": "AI-native 設計流程繞過既有 EDA 工具、或客戶以 agent 減人力後總支出持平——市場 2026-08 已用軟體股拋售定價此疑慮；Siemens Fuse EDA AI Agent 宣稱設計週期減半。目前三大既有廠都在做 agent、無新進入者，CEO 稱基礎工具是 V6/V8 引擎；扣分反映在定價 8 而非 9，不在趨勢重複記帳",
        "p": "15-20%（5 年內 Core EDA 成長因 AI 減席降至個位數）",
        "evidence_refs": [
          "substitute_technology#0",
          "substitute_technology#2",
          "competitive_share_entrants#3"
        ]
      },
      {
        "level": "🔴 生態攻擊",
        "text": "Synopsys 併 Ansys 後推 device-to-system 全棧（multiphysics 領先 18-24 月）；NVIDIA 與 Synopsys 非獨家合作；Cadence 以 Hexagon（$3.2B）追趕 physical AI",
        "p": "30%（SD&A 份額被 Synopsys-Ansys 壓制）",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "major_events#0"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "超大規模業者自研晶片團隊擴大 COT，目前是擴大採用 Cadence 而非自建工具；中國本土 EDA 業者在成熟節點競爭",
        "p": "10%（5 年內任一 Big-4 自建 EDA 取代 Cadence 全流程）",
        "evidence_refs": [
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      }
    ],
    "competitors": [
      {
        "name": "Synopsys（SNPS）",
        "rev_growth": "證據包未涵蓋（FY26 IP 自認清淡年）",
        "gm": 73.47,
        "om": 9.73,
        "rd_intensity": 32.11,
        "fcf_margin": 30.35,
        "net_cash": "證據包未涵蓋（Ansys 交易 $35B 後負債上升）",
        "strategy_note": "龍頭 31% 份額，併 Ansys 開 multiphysics 全棧；續約靠 token 漲價約 20%（ID）；IP 作風轉交易型（CFO 觀察，來源：摘要）。GAAP 營業利益率被攤銷壓到 9.7%，FCF 與 Cadence 同級——經濟體質相當、資產負債表較重"
      },
      {
        "name": "Siemens EDA（私有）",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "母公司 Siemens",
        "strategy_note": "約 13% 份額，Calibre 簽核 85%+ 為代工廠強制鎖喉點（結構性 tenure，非成長主軸）；2026 推 Fuse EDA AI Agent 主打設計週期減半"
      },
      {
        "name": "ARM（IP 對手）",
        "rev_growth": "證據包未涵蓋",
        "gm": 97.54,
        "om": 17.3,
        "rd_intensity": 57.49,
        "fcf_margin": 28.55,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "CSS 子系統化把 IP 從藍圖升級（權利金率約 10%）；Cadence 買下其 Artisan foundation IP，兩者在 star IP 上互補多於對撞"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率 × 高周轉（非 GAAP NOPAT 利潤率約 36%、資本支出僅營收 3%、年度預收使營運資金為負）；GAAP 投入資本因併購商譽偏重，周轉率被拉低但仍屬資本輕",
      "checkpoints": [
        {
          "item": "需求基礎值",
          "light": "🟢",
          "evidence": "需要型：先進晶片不經簽核不能流片、代工廠強制工具；TSMC 稱五年電晶體數成長 48-50 倍（來源：摘要）；設計需求與工程師供給落差是結構性"
        },
        {
          "item": "決策層級",
          "light": "🟢",
          "evidence": "多年 ELA、換工具＝重跑整套驗證；FY26 營收 67% 來自期初積壓；合約年期未縮短（CEO 2026-02，來源：摘要）；經常性營收 78%"
        },
        {
          "item": "價值鏈分配",
          "light": "🟡",
          "evidence": "EDA＋IP 對超大規模業者是 COGS，AVGO 等 ASIC 大戶內製設計壓 IP 議價（ID）；但每顆先進晶片 EDA＋IP 投資自 $50-200M 升至 $200-400M，總量在漲"
        },
        {
          "item": "社會容忍度",
          "light": "🟡",
          "evidence": "產品必要性高但政治敏感：美國出口管制可在數週內切斷 12-13% 營收（2025-05 至 07 實證）；DOJ 認罪三年緩刑期強化合規稽核；法源＝EAR ECCN 3D991/3E991"
        }
      ],
      "roiic": 17.6,
      "reinvest_rate": 88,
      "endo_ceiling": 15.5,
      "formula_note": "ROIIC(3Y)≈ΔNOPAT÷Δ投入資本：FY2026E NOPAT≈$2.23B（營收 $6.30B×非 GAAP 營業利益率 44.25%×(1−20%)），三年前以 14% 年均成長回推 NOPAT≈$1.37B，ΔNOPAT≈$0.86B；Δ投入資本≈三年併購 $4.9B（Hexagon $3.2B、BETA CAE、Artisan、Secure-IC）＋資本支出減折舊≈0 → 17.6%。再投資率＝併購＋資本支出−折舊 ÷ 三年 NOPAT 合計≈$5.6B ≈ 88%。內生天花板＝17.6%×88%≈15.5%；有機部分資本輕（增量利潤率 60%、負營運資金）標準公式失效，以 ROIIC 為上界。共識 FY1→FY3 EPS CAGR 17.0%＝天花板 15.5%＋淨回購約 1%＋倍數 0 → 邊界內"
    }
  },
  "growth": {
    "runway_years": 12,
    "runway_post_y5": "🟢",
    "seven_questions": [
      "①結構性或週期反彈：結構性為主——EDA 市場 CAGR 8-9%、設計複雜度與 AI 晶片流片量上升；但疊了一層 AI 資本支出週期（2027 為考驗年）",
      "②資本投入多少：有機幾乎不需資本（資本支出佔營收約 3%、增量利潤率 60%）；無機部分重——三年併購約 $4.9B，Hexagon $3.2B 換 $160M 營收",
      "③增量 ROIC 是否 >資金成本：有機遠高於；併購含 Hexagon 的 ROIIC 約 17.6% 仍高於資金成本，但 Hexagon 單案首年遠低於",
      "④成長變現金流或被吃掉：FCF 利潤率 28.6%（TTM）、50% FCF 回購——成長變股東現金，但 2026 併購現金流出 $3.2B 吃掉一年多 FCF",
      "⑤競爭者會否被吸引：三寡占＋簽核鎖喉，新進入者查無；吸引的是既有對手的 AI 軍備競賽與 Synopsys-Ansys 全棧",
      "⑥股價反映多少期待：FY2027 本益比 30.7x、PEG 1.8、四年分位約 33%——反映「雙位數中段成長」但不再反映「AI 放大器」；短窗前瞻本益比 47x→36x 已消化一輪",
      "⑦成長率下修估值撐得住嗎：熄火至 10% 對應本益比 22-24x，自現價再跌 30-40%——撐不住，這是最弱的一題，與陷阱定性「觀察倍數下移」一致"
    ],
    "segments": [
      {
        "name": "Core EDA（71%）",
        "fy0": "FY2025 約 $3.75B（以 FY26 指引中值 $6.30B×71% 回推 FY26≈$4.47B，FY25 以年增 18% 回推）",
        "driver": "量：授權席次×活動量（token）×硬體台數；價：續約漲幅（同業 token 漲價約 20%，本標的未揭露）",
        "fy1e": "FY2026 約 $4.47B（+18%）",
        "fy2e": "FY2027 約 $5.10B（+14%）",
        "fy3e": "FY2028 約 $5.75B（+13%）",
        "om_path": "分段營業利益率證據包未涵蓋；合併非 GAAP 44.25%→46%→47%",
        "eps_contrib_pct": "約 70%"
      },
      {
        "name": "半導體 IP（14%）",
        "fy0": "FY2025 約 $0.72B",
        "driver": "量：先進節點 design win 數（2 奈米代工大單）；價：star IP 溢價",
        "fy1e": "FY2026 約 $0.95B（+30%）",
        "fy2e": "FY2027 約 $1.15B（+20%）",
        "fy3e": "FY2028 約 $1.35B（+17%）",
        "om_path": "CEO 稱比產業 IP 更賺錢（來源：摘要），分段數字證據包未涵蓋",
        "eps_contrib_pct": "約 15%"
      },
      {
        "name": "SD&A（15%，含 Hexagon）",
        "fy0": "FY2025 約 $0.80B",
        "driver": "量：3D-IC／多物理模擬席次＋Hexagon $160M 併入；價：轉年度訂閱短期壓成長",
        "fy1e": "FY2026 約 $1.05B（+31%，其中無機約 $160M）",
        "fy2e": "FY2027 約 $1.22B（+16%）",
        "fy3e": "FY2028 約 $1.40B（+15%）",
        "om_path": "Hexagon 2026 稀釋 EPS $0.28、2027 轉增益",
        "eps_contrib_pct": "約 15%"
      }
    ],
    "decay_signals": [
      "護城河侵蝕｜毛利率連 2 季年減：未亮（TTM 85.9%，逐季證據包未涵蓋）",
      "護城河侵蝕｜核心市佔縮減：未亮（IP／硬體／系統皆取份額）",
      "護城河侵蝕｜提價後銷量下滑：未亮（無定價事件揭露）",
      "盈餘品質｜EPS CAGR 顯著高於營收 CAGR：未亮（EPS 17% vs 營收約 13-15%，差距 <5pp）",
      "盈餘品質｜FCF/NI <0.75 連 2 年：未亮（TTM FCF 利潤率 28.6% vs GAAP 營業利益率 30.8%，轉換率高）",
      "盈餘品質｜SBC/營收 >5% 且逐年上升：未亮（9.3%，較 Q1 9.4% 持平微降；絕對水位高列觀察）",
      "產業結構衰退｜TAM 萎縮或被替代：未亮（TAM CAGR 8-9%；AI 替代屬威脅未實現）",
      "產業結構衰退｜產業倍數近 3 年系統性下移：亮——trailing 本益比 2024 年 78.9x→現 60.6x，2026 軟體股整體重定價",
      "隱性資本密集｜維護資本支出佔 FCF >60%：未亮（資本支出僅營收約 3%）",
      "隱性資本密集｜停止投資新產能致收入下滑：未亮（Z4 硬體 2030 前，來源：摘要）"
    ],
    "trap_rating": "🟡（1 燈：倍數下移）；長期成長性綜合 🟢 高確信——跑道 ≥10 年、有機為主（無機約 2pp）、強化型、ROIC 高檔、信號 1"
  },
  "quality": {
    "three_year": [
      {
        "metric": "FCF 利潤率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "TTM 28.64（Q2 2026 單季 36.8、Q1 20.8）",
        "peer_median": "SNPS 30.35／ARM 28.55／QCOM 23.64",
        "assessment": "同級；季度起伏來自硬體與 IP 一次性出貨"
      },
      {
        "metric": "非 GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "FY2025 約 44.5%（CEO 2025-12，來源：摘要）；Q2 2026 45.5%；FY2026 指引 43.75-44.75%",
        "peer_median": "證據包未涵蓋",
        "assessment": "逐年擴張、增量 60%；2026 因 Hexagon 略低於 2025"
      },
      {
        "metric": "GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "TTM 30.82；Q2 2026 28.4（年增 940bp）",
        "peer_median": "SNPS 9.73／QCOM 23.28",
        "assessment": "遠優於 Synopsys；GAAP 與非 GAAP 差 17pp＝SBC＋攤銷"
      },
      {
        "metric": "SBC 佔營收",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "Q2 2026 9.3%（$146.9M）；佔 GAAP 營業利益 32.7%",
        "peer_median": "證據包未涵蓋",
        "assessment": "高位持平；回購覆蓋稀釋"
      },
      {
        "metric": "ROIC−WACC",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "投入資本數字證據包未涵蓋；以 FCF 利潤率 28.6%、資本支出 3% 代理，現金報酬遠高於資金成本",
        "peer_median": "證據包未涵蓋",
        "assessment": "資本輕高報酬"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利潤率",
        "value": "GAAP 30.8%×(1−20%)≈24.7%；非 GAAP 45.5%×0.8≈36.4%",
        "note": "兩口徑差 12pp 為 SBC 與併購攤銷"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本數字不在證據包）",
        "note": "年度預收→負營運資金、資本支出 3%，周轉率結構上高；併購商譽是唯一重資產"
      },
      {
        "component": "ROIC",
        "value": "證據包未涵蓋",
        "note": "象限判讀：高利益率×高周轉"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO／CCC 三年逐年",
        "value": "證據包未涵蓋",
        "note": "經常性營收 78% 隨時間認列、硬體與 IP 一次性 22% 在出貨時點認列；應收帳款集中度 2024 年末一客戶 11%→2025 Q3 無 ≥10%"
      }
    ],
    "buyback": {
      "authorization": "政策＝每年約 50% 以上 FCF 回購；2025 全年 $925M；Q1 2026 $200M、Q3 2025 $200M（來源：摘要）",
      "q1_capital_return": "Q1 2026 $200M；Q2 2026 金額證據包未涵蓋",
      "buyback_to_fcf": "約 50%（政策），遠低於 80% 警示線；2026 另有 $3.2B Hexagon（30% 股票／70% 現金）",
      "avg_price_vs_now": "回購均價證據包未涵蓋；2025-2026 股價區間 $250-377，現價 $292.7 落區間中低段",
      "eps_cagr_ex_buyback": "淨回購約 1%／年（回購略高於 SBC 8-9%，CEO 稱確保不稀釋，來源：摘要）；剔除後 EPS CAGR 約 16% vs 共識 17%，差距 <5pp"
    },
    "lumpiness": {
      "five_year_fcf": "證據包未涵蓋逐年值；2026 上半年 OCF $990.7M、資本支出 $101.4M、FCF $889M",
      "min_vs_avg": "證據包未涵蓋",
      "maint_capex": "以總資本支出（營收約 3%，含 Palladium 自研硬體）為維護資本支出上限——方法：軟體公司資本支出幾乎全屬維護",
      "owner_earnings": "上半年 OCF−資本支出≈$889M，年化約 $1.8B（FY26 營收中值 $6.30B 的 28-29%）",
      "verdict": "🟢 正常——單季起伏（Q1 20.8%／Q2 36.8%）來自硬體與 IP 出貨時點與稅款時序，非結構性"
    }
  },
  "governance": {
    "capalloc_grade": "B",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC",
        "value": "Hexagon D&E $3.2B（2026-02 交割）換 2026 營收約 $160M、年化約 $200M——20x 營收，首年 EPS 稀釋 $0.28、2027 轉增益；第 3 年 NOPAT 尚不可觀測；BETA CAE（2024）第 3 年貢獻證據包未涵蓋 → 未證，不計過",
        "pass": false
      },
      {
        "item": "回購買入收益率",
        "value": "現價盈餘殖利率 8.14÷292.7＝2.8%；門檻（10 年期公債＋2%，公債殖利率證據包未涵蓋，以 4% 計）≈6% → 未過；2025-2026 回購價區間與現價相近，收益率同樣 <3%",
        "pass": false
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 8-9% 營收，回購 ≥SBC（CEO：買回比 SBC 多，來源：摘要）→ 年化淨稀釋 ≤0，過",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "回購",
        "detail": "2025 $925M；每年約 50% FCF；目標不因 SBC 淨稀釋"
      },
      {
        "type": "股息",
        "detail": "無"
      },
      {
        "type": "併購",
        "detail": "2025-08 Arm Artisan foundation IP；2025-11 Secure-IC；2026-02 Hexagon D&E $3.2B（史上最大）；2026-03 EMA（PCB）；管理層稱未來 1-2 年重心在整合、只做小型 tuck-in、不做變革型交易（來源：摘要）"
      },
      {
        "type": "治理事件",
        "detail": "2025-07-28 就 2015-2021 年對 NUDT 非法出口向 DOJ 認罪、合計逾 $140M（DOJ 罰金＋沒收約 $117M、BIS 民事 $95M 部分重疊）、三年緩刑＋年度出口合規稽核——合規失靈紀錄，非財報重編亦非 SEC 會計調查；無近 12 個月證券集體訴訟"
      }
    ],
    "sbc": {
      "pct_revenue": 9.3,
      "pct_gaap_oi": 32.7,
      "trend": "Q1 2026 9.4% → Q2 9.3%；CEO 定義真實利潤率＝營業利益率減 SBC（來源：摘要）",
      "note": "股東結構（雙重股權／創辦人持股／機構集中度）、管理層薪酬結構、近 12 個月內部人交易：證據包未涵蓋（數據限制）"
    }
  },
  "valuation": {
    "tier": "EDA 寡占（IP company／設計軟體）；同 tier 尺＝SNPS 唯一 anchor；ARM（IP）與 QCOM 不同層級只作體質對照",
    "peers": [
      {
        "name": "SNPS",
        "fwd_pe": "證據包未涵蓋",
        "note": "唯一同 tier；GAAP 營業利益率被 Ansys 攤銷壓低，倍數對照須用非 GAAP"
      },
      {
        "name": "ARM",
        "fwd_pe": "證據包未涵蓋",
        "note": "IP 純 play，倍數通常高於 EDA，不作 anchor"
      },
      {
        "name": "QCOM",
        "fwd_pe": "證據包未涵蓋",
        "note": "客戶而非同業，體質對照用"
      }
    ],
    "fwd_pe": 35.96,
    "peg": 2.12,
    "percentile_5y": 33,
    "val_light": "🟡",
    "val_light_derivation": "分位：trailing 本益比現值 60.6x 在年度樣本點（n=4，高 78.9／低 51.7）分位 32.8%；P/S 13.8x 分位 26.8%；EV/S 分位 30.3%——三尺取本益比 33%，落 30-70% 合理帶（樣本僅 4 個年度點，非連續五年，信心中）。PEG：EPS CAGR 以前瞻窗 FY2026 8.14→FY2028 11.14＝17.0%；FY2026 本益比 35.96x÷17.0＝2.12（偏貴帶）、FY2027 本益比 30.68x÷17.0＝1.80（合理帶）；距財年結束僅四個月，NTM 混合約 32x÷17≈1.9。取較嚴讀法為偏貴，但盲點一救援三條件同時成立（長期成長 🟢 高確信＋FY2027 PEG 1.80 <2.0＋AI 🟢）→ 救回 🟡；盲點三不適用（90 天共識上修 FY1 +2.4%／FY2 +1.7%，遠低於 +10%）。旁註：本站短窗前瞻本益比 2026-05 47.4x→現 36.0x 為窗內最低（四個月短窗，非五年分位）",
    "targets": {
      "short_1y": {
        "eps": 9.54,
        "pe": 33,
        "price": 314.8,
        "upside_pct": 7.6,
        "basis": "FY2027 共識 EPS×合理 33x（護城河 A、成長 15%、Rule of 60）"
      },
      "mid_2y": {
        "eps": 11.14,
        "pe": 33,
        "price": 367.6,
        "upside_pct": 25.6,
        "basis": "FY2028 共識 EPS×33x"
      },
      "five_y": {
        "eps": 15.7,
        "pe": 30,
        "price": 471.0,
        "upside_pct": 60.9,
        "basis": "Base FY2031 EPS×長期 30x（成長降至 12% 時的合理倍數）"
      },
      "bear_anchor": {
        "eps": 7.33,
        "pe": 24,
        "price": 175.8,
        "downside_pct": -39.9,
        "basis": "Bear EPS＝FY2026 共識 8.14×0.9；Bear 本益比＝成長熄火降至 10% 情境 24x；下行 40% >15% 正常可用，短期 R:R 0.19 屬弱、僅參考"
      },
      "sell_side": "Q2 財報後 BofA $420、KeyBanc $425、Stifel $432；2026-09 初 25 位分析師中位數 $405（區間 $300-470，全距 1.6x 未達 2.5x 離散警戒）、買進佔 84%；Zacks 量化 Hold。現價 $292.7 低於中位數 28%——共識目標價仍高於本檔一年目標 $315，本檔比賣方保守，不靠上修也有空間"
    },
    "upside_short_pct": 7.6,
    "upside_mid_pct": 25.6
  },
  "trap_analysis": {
    "pattern": "最可能模式＝「倍數下移中的成長股」——盈餘持續成長但市場把軟體類估值框架整體下調（AI 顛覆敘事），不是盈餘陷阱",
    "evidence_against": "Q2 營收 +24.2%、非 GAAP 營業利益率 45.5% 優於自身指引高標、積壓 $8.1B 與 12 個月 RPO $4.2B 雙創高、全年指引上修至 +19%、共識 90 天上修為正（FY1 +2.4%）；FCF 利潤率 28.6%——盈餘與現金同向、加速中",
    "evidence_for": "trailing 本益比自 2024 年 78.9x 降至 60.6x、短窗前瞻本益比 47x→36x 而盈餘只升 2%——跌的是倍數；2026 為續約低年、積壓創高靠新客，若 2027 AI 資本支出減速，新客動能不可持續；Hexagon 20x 營收的併購是資本配置疑點",
    "bear_case": "18 個月內 −30% 路徑：2027 超大規模業者資本支出指引年增 <+20% → 流片與續約遞延 → FY2027 EPS 由 9.54 下修至 8.6 → 市場以 22-24x 定價成熟軟體 → $190-205。監測：Big-4 資本支出指引（每季）、Cadence 積壓年增、Core EDA 有機成長",
    "monitor": [
      "積壓與 12 個月 RPO 年增（每季新聞稿）：連 2 季轉負＝陷阱顯影",
      "Core EDA 有機成長 TTM（法說）：<10% 連 2 季＝框架切換確認",
      "中國營收佔比與許可狀態（法說／BIS 公告）",
      "短窗前瞻本益比：<28x 且盈餘未下修＝倍數陷阱而非盈餘陷阱，反向加碼"
    ],
    "verdict": "🟢",
    "label": "非陷阱（倍數觀察）"
  },
  "appendix_a": {
    "signal": "A",
    "moat_score": 8.5,
    "growth_durability": 8,
    "quality_score": 8.3,
    "ai_risk": "🟢",
    "long_term_confidence": "高",
    "val": "🟡",
    "ma": "-",
    "fpe_fy2": 30.68,
    "pct_5y": 33,
    "peg_fy2": 1.8,
    "upside_short_pct": 7.6,
    "upside_mid_pct": 25.6,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "A"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY2027": 9.45,
      "FY2028": 10.9,
      "FY2029": 12.4,
      "FY2030": 14.0,
      "FY2031": 15.7
    },
    "fy_end_month": 12,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-10",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q3 2026 財報：非 GAAP EPS 指引 $2.01-2.07、營業利益率 43.5-44.5%；看積壓年增與 Core EDA 有機成長",
      "impact": "中",
      "watch": "積壓 ≥$8.1B、FY26 指引再上修＝H1 強化；ChipStack Level-5 早期存取客戶數"
    },
    {
      "date": "2026-11-09",
      "date_precision": "month",
      "type": "regulatory",
      "event": "BIS 50% 規則暫停到期，恢復或再延；同時是美中談判中 EDA 許可制會否重施的觀察窗",
      "impact": "高",
      "watch": "恢復＋任何 EDA 許可通知＝唯一事件觸發；再延＝R1 降溫"
    },
    {
      "date": "2026-12",
      "date_precision": "quarter",
      "type": "product",
      "event": "ChipStack Level-5 全自主虛擬工程師早期存取（2026 下半年）；token 計費模式首批客戶",
      "impact": "中",
      "watch": "FY2027 法說是否首次揭露 token／消費型營收＝H2 驗證"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q4 2026 財報與 FY2027 指引：Hexagon 轉增益、期初積壓覆蓋率、中國佔比預期",
      "impact": "高",
      "watch": "FY2027 營收指引 ≥+13%、非 GAAP 營業利益率 ≥46%；2027 積壓覆蓋率 ≥65%"
    },
    {
      "date": "2027-01",
      "date_precision": "quarter",
      "type": "macro",
      "event": "Big-4 超大規模業者 2027 資本支出指引（Q4 法說季）",
      "impact": "高",
      "watch": "任一年增 <+20%＝R2 發火；EDA 流片量落後 6-12 個月"
    }
  ],
  "decision_inputs": {
    "signal": "A",
    "trap": "🟢",
    "val": "🟡",
    "ma": "-",
    "runway_post_y5": "🟢",
    "moat_trend": "↑",
    "moat": "A",
    "capalloc_grade": "B",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 3.7,
    "irr_base_pct": 10.7,
    "ev5y_pct": 50.8,
    "price_at_dd": 292.7,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": -1.43,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 2.4,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "prior_verdict": null,
    "prior_role": null,
    "held_now": null
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "9b",
    "pacing": [],
    "holding_cap": null,
    "requires_critic": [
      "QC-41：裁決強方向（進場）＋護城河趨勢 ↑＋法規敏感（對華出口管制）＋B2B 集中型——需跨模型複核「AI 放大而非顛覆」是否低估了架構替代軸，以及 ↑ 是否只靠管理層自述",
      "手冊 27：Synopsys 資本量級大於本標的（併 Ansys $35B），↑ 是否應降為 →——請閘核對 IP +40% 與硬體新客 30 家是否足以撐方向性判定"
    ],
    "audit_rows": [
      {
        "row": "1",
        "condition": "基本面評級 signal = X → 迴避",
        "hit": false,
        "basis": "signal='A'"
      },
      {
        "row": "2",
        "condition": "§11 強制裁決：thesis 不可調和不成立 → 迴避",
        "hit": false,
        "basis": "thesis_irreconcilable=False"
      },
      {
        "row": "3",
        "condition": "moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避",
        "hit": false,
        "basis": "moat_trend='↑', moat='A'"
      },
      {
        "row": "4",
        "condition": "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）",
        "hit": false,
        "basis": "ma='-'"
      },
      {
        "row": "5",
        "condition": "動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）",
        "hit": false,
        "basis": "momentum_overheated=False"
      },
      {
        "row": "6",
        "condition": "基本面評級 signal = C → ≥ 觀望",
        "hit": false,
        "basis": "signal='A'"
      },
      {
        "row": "7",
        "condition": "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）",
        "hit": false,
        "basis": "runway_post_y5='🟢'"
      },
      {
        "row": "7a",
        "condition": "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
        "hit": false,
        "basis": "valuation_dependent=False, market_wrong_reason_given=True"
      },
      {
        "row": "7b",
        "condition": "dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）",
        "hit": false,
        "basis": "capalloc_grade='B'"
      },
      {
        "row": "8a",
        "condition": "無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）",
        "hit": false,
        "basis": "signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=-1.43, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↑', cycle_gates_pass=None"
      },
      {
        "row": "11.4b-denom",
        "condition": "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
        "hit": false,
        "basis": "val_denominator_disputed=False"
      },
      {
        "row": "8",
        "condition": "無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）",
        "hit": false,
        "basis": "signal='A', val='🟡'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": false,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": true,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": false,
        "basis": "signal='A', val='🟡', ma='-'"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": "價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段",
    "exec_line": "新資金：首階三分之一現價建倉，餘掛 $260／token 揭露／BIS 落地三段。已持有：不加不減；清倉只認唯一事件（對華 EDA 許可制恢復），估值偏高最多 trim（前瞻本益比 >50x）"
  },
  "triggers": [
    {
      "n": 1,
      "text": "積壓與 Core EDA 有機成長守住（H1）",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "積壓 TTM 年增；Core EDA 有機成長 TTM",
      "threshold": "積壓年增 <0 連 2 季＝削弱；Core EDA <8% 連 3 季＝反轉",
      "action": "削弱＝停止加碼；反轉＝減至首階",
      "source_freq": "季度新聞稿／法說，每季",
      "date": "2026-10-31",
      "evidence_refs": [
        "competitive_share_entrants#0",
        "supply_demand_durability#0"
      ]
    },
    {
      "n": 2,
      "text": "token／消費型營收揭露（H2）",
      "type": "假設驗證",
      "maps_to": "H2",
      "metric": "AI 工具 ARR 或 token 營收佔比首次揭露；合約年期",
      "threshold": "FY2028 仍無揭露＝削弱；Core EDA 連 4 季 <8% 且客戶引述 AI 減席＝反轉",
      "action": "揭露＝加第二個三分之一（論點增強）；反轉＝減碼一半",
      "source_freq": "法說／投資人會議，每季",
      "date": "2027-02-28",
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#2"
      ]
    },
    {
      "n": 3,
      "text": "非 GAAP 營業利益率擴張（H3）",
      "type": "假設驗證",
      "maps_to": "H3",
      "metric": "非 GAAP 營業利益率 TTM；增量利潤率",
      "threshold": "TTM 年減 >100bp 連 2 季＝削弱；增量 <40% 連 2 年＝反轉",
      "action": "削弱＝停止加碼；反轉＝重評 H3 與終端倍數",
      "source_freq": "季度新聞稿，每季",
      "date": "2027-02-28"
    },
    {
      "n": 4,
      "text": "中國出口管制與佔比（R1）",
      "type": "風險",
      "maps_to": "R1",
      "metric": "中國營收佔比 TTM；BIS 許可／規則狀態",
      "threshold": "佔比連 4 季 <9% 或任一季因管制遞延營收 → 減碼；許可制正式恢復 → 唯一事件",
      "action": "減碼三分之一；恢復許可制＝清倉",
      "source_freq": "法說每季；BIS 公告事件驅動",
      "date": "2026-11-09",
      "evidence_refs": [
        "reg_tariff_export#0",
        "reg_tariff_export#3",
        "geo_supply_chain#0",
        "geo_supply_chain#1",
        "geo_supply_chain#2",
        "geo_supply_chain#4",
        "major_events#4",
        "sec_investigation_restatement#0"
      ]
    },
    {
      "n": 5,
      "text": "AI 資本支出 2027 降檔（R2）",
      "type": "風險",
      "maps_to": "R2",
      "metric": "Big-4 超大規模業者 2027 AI 資本支出指引年增；Cadence 積壓年增",
      "threshold": "任一 <+20% 且積壓年增連 2 季轉負 → 減碼；連 4 季 → 大動作",
      "action": "減碼三分之一；連 4 季減至首階",
      "source_freq": "超大規模業者法說每季（2027-01 起）",
      "date": "2027-01-31",
      "evidence_refs": [
        "supply_demand_durability#3"
      ]
    },
    {
      "n": 6,
      "text": "客戶集中與信用（R3）",
      "type": "風險",
      "maps_to": "R3",
      "metric": "10-Q 應收帳款集中度；前十大客戶重組事件；系統廠佔比",
      "threshold": "任一客戶應收 ≥10% 或前段客戶重組致遞延 >$100M → 減碼；系統廠佔比連 2 年下降 → 重評 H1",
      "action": "減碼三分之一",
      "source_freq": "10-Q 每季；信評事件驅動",
      "date": "2026-10-31",
      "evidence_refs": [
        "customer_second_source#2",
        "customer_concentration_credit#1",
        "customer_concentration_credit#2",
        "customer_concentration_credit#3"
      ]
    },
    {
      "n": 7,
      "text": "對華 EDA 出口許可制恢復",
      "type": "Single Thing",
      "maps_to": "Single Thing",
      "metric": "BIS 通知／最終規則要求 EDA（ECCN 3D991/3E991）對華出口許可，且 90 天內未撤銷",
      "threshold": "正式通知＝觸發",
      "action": "清倉，不等財報；重啟＝撤銷或中國佔比 <5% 且積壓仍年增",
      "source_freq": "BIS 公告、公司 8-K，事件驅動",
      "date": "2026-11-09",
      "evidence_refs": [
        "geo_supply_chain#1",
        "geo_supply_chain#2"
      ]
    },
    {
      "n": 8,
      "text": "加碼雙軌",
      "type": "加碼",
      "maps_to": "估值／論點增強",
      "metric": "價格 vs FY2027 本益比；token 營收揭露",
      "threshold": "價 ≤$260（27x）或 token 營收首次揭露",
      "action": "加第二個三分之一；兩者皆到不重複加",
      "source_freq": "每週價格；法說每季",
      "date": "2027-02-28"
    },
    {
      "n": 9,
      "text": "估值偏高 trim",
      "type": "減碼",
      "maps_to": "估值",
      "metric": "FY1 前瞻本益比",
      "threshold": ">50x 且共識未同步上修 ≥10%",
      "action": "最多 trim 三分之一，不清倉（核心角色長抱分軌）",
      "source_freq": "每週",
      "date": "2027-09-05"
    },
    {
      "n": 10,
      "text": "thesis 級清倉",
      "type": "清倉",
      "maps_to": "H1/H2",
      "metric": "Core EDA 有機成長 TTM；積壓年增；客戶 AI 減席引述",
      "threshold": "Core EDA <8% 連 3 季且積壓年增連 2 季為負",
      "action": "清倉；重啟須重跑 DD",
      "source_freq": "法說每季",
      "date": "2027-08-31",
      "evidence_refs": [
        "substitute_technology#0"
      ]
    },
    {
      "n": 11,
      "text": "複審",
      "type": "複審日期",
      "maps_to": "全部",
      "metric": "Q4 2026 財報與 FY2027 指引後",
      "threshold": "—",
      "action": "重跑判斷：H1-H3 漂移、Hexagon 增益、中國佔比預期",
      "source_freq": "半年",
      "date": "2027-02-28"
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單與矛盾拓撲",
      "side_a": "方向一致：寡占＋簽核鎖定＋多年 ELA（護城河 A）；營收 +24%、營業利益率 45.5%、積壓創高（成長與品質）；估值自高點回落至合理帶；賣方 84% 買進",
      "side_b": "矛盾拓撲＝集中兩軸：①AI 是放大器還是顛覆者（護城河定價維度與終端倍數）；②中國出口管制（政策軸）。其餘（Hexagon 稀釋、Intel 信評、2027 資本支出）為程度差異",
      "ruling": "爭議集中→點名兩軸；信心不整體下修，但進場改分批、唯一事件鎖政策軸",
      "evidence_level": "L1",
      "settle_metric": "Core EDA 有機成長與 token 營收揭露；BIS 2026-11-09",
      "if_then": [
        "若 FY2027 指引 ≥+13% 且 token 營收揭露 → 完成三段建倉",
        "若 Core EDA <8% 連 3 季 → 減至首階"
      ]
    },
    {
      "axis": "AI 放大 vs AI 顛覆（不可調和）",
      "side_a": "A 側：設計先進晶片需要精確物理與數學簽核，AI agent 是 Cadence 自己在賣（ChipStack／Level-5 與 NVIDIA）；客戶沒有減少使用的討論（CEO 2026-02，來源：摘要）；系統廠 45% 擴大採用而非自建；三大廠都在做 agent、無新進入者",
      "side_b": "B 側：2026-08 軟體股拋售把 CDNS 一併重定價，市場怕 AI 自動化設計流程壓縮 TAM；Siemens Fuse 宣稱設計週期減半；CEO 自己也說每專案人力至少減 30%（來源：摘要）——人頭計費基底在縮；token 計費至今無營收揭露，且管理層對變現時點以「可以有耐心」帶過（來源：摘要）",
      "ruling": "選 A 側但打折：L1 實績（+24%、積壓創高、IP／硬體取份額）勝過 L3 敘事（軟體股拋售）；以 L2 反駁 L1 的理由只有「token 未揭露」——這是時間差不是方向。執行：進場但終端倍數以 30x（非 36x）為 Base、Bear 30% 且 Bear 終端 22x 反映框架切換。現在就賣的最強論證：(1) 人頭減 30% 若 token 補不回，Core EDA 成長掉到個位數；(2) 2027 AI 資本支出減速讓積壓創高只是續約低年的錯覺；(3) 中國許可制隨時可回來——逐點回應：(1) 故以 H2 的 FY2028 揭露期限與 Core EDA <8% 連 3 季當清倉閘，不等 GRR 顯影；(2) 12 個月 RPO $4.2B 覆蓋 FY2027 約 60%，減速最快 2027 下半年才傳導，觸發器 5 已掛；(3) 列為唯一事件，觸發即清倉而非減碼",
      "evidence_level": "L1 vs L3",
      "settle_metric": "FY2027-2028 Core EDA 有機成長與 token 營收佔比",
      "if_then": [
        "若 token 營收於 FY2027 揭露且 Core EDA ≥12% → 加第二段",
        "若 Core EDA <8% 連 3 季且積壓年增連 2 季負 → 清倉"
      ],
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#1",
        "substitute_technology#2",
        "customer_second_source#1",
        "substitute_technology#3"
      ]
    },
    {
      "axis": "AI 資本支出泡沫 vs 積壓創高（可調和）",
      "side_a": "永續性測試 2027 浮現、AI 產業需 $2 兆年營收撐當前投資（市場評論）",
      "side_b": "積壓 $8.1B 在續約低年創高、新增 12 客、系統廠自研 ASIC 讓每顆晶片 EDA＋IP 投資倍增（ID）",
      "ruling": "程度差異：積壓鎖合約量不鎖續約定價權（ID 需求側原話）。採信短期（FY2026-27 底部有合約），不採信「2027 一定持續加速」——Base 把 FY2027 EPS 對共識打 1% 折、Bear 情境 FY2027 只 +6%",
      "evidence_level": "L2 vs L3",
      "settle_metric": "Big-4 2027 資本支出指引",
      "if_then": [
        "若任一 Big-4 2027 指引 <+20% → 停止加碼並看積壓",
        "若四家皆 ≥+20% → R2 降為 🐢"
      ],
      "evidence_refs": [
        "supply_demand_durability#3",
        "supply_demand_durability#0",
        "supply_demand_durability#2"
      ]
    },
    {
      "axis": "ID 對帳：AI EDA + IP（as-of 2026-04-27）",
      "side_a": "ID 機器欄：shortage／Phase II／信心 high／priced_in 未填",
      "side_b": "本檔：Phase II 經交叉驗證載入；shortage 只當事實錨；priced_in 本檔自判由「大多反映」退回「部分反映」（股價 −30%、短窗前瞻本益比 47x→36x）",
      "ruling": "一致，無分歧；ID 已四個月餘、寫於股價高點前，其 priced_in 缺值應於下次 refresh 補填——不阻斷",
      "evidence_level": "L2",
      "settle_metric": "ID refresh 的 priced_in 欄",
      "if_then": [
        "若 ID refresh 改判 balanced → Bear 終端倍數不變、Base 成長降 1pp",
        "若 ID 維持 shortage 且 priced_in 判 low → 可提前完成第二段"
      ]
    },
    {
      "axis": "前份對照：裁決承繼與回測帶",
      "side_a": "前份（2026-05-04，v12.3）：A 核心候選、4 週 +22% 接近警戒、「等回測 BB 中軌約 303」；當時無統一裁決欄（決策層尚未併入）",
      "side_b": "本次：價 $292.7 已落 303 之下（前份等待的位置到了），盈餘共識 FY1 自 7.95 升至 8.14；裁決首次正式落「進場·核心」",
      "ruling": "非翻面（前份無正式裁決可翻）；本次進場理由＝前份預設的回測條件已成立＋基本面加速，不是估值更便宜的單一理由。90 天內 hysteresis 不適用（跨 124 天）",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "若 Q3 財報後價回 $330 以上未完成三段 → 不追，剩餘段改掛論點增強",
        "若跌破 $260 且 H1-H3 無損 → 第二段"
      ],
      "prior_field": "dca_verdict"
    },
    {
      "axis": "前份漂移：dca_role／archetype／cycle_position（前份格式無此三欄，首次出現）",
      "side_a": "本次：核心／品質複利成長／不適用（非循環）",
      "side_b": "前份：無此欄（v12.3 無決策層與分類欄）",
      "ruling": "方法論驅動（v12.3→v15.2 新增欄位），非基本面或價格變化",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "dca_role"
    },
    {
      "axis": "前份漂移：price_at_dd",
      "side_a": "本次 $292.7",
      "side_b": "前份 $340.94",
      "ruling": "價格變了（主因，−14%）；基本面反向變好（FY1 共識 +2.4%、指引上修）；方法論不涉。歸因排序：價格 > 基本面（反向）> 方法論",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "price_at_dd"
    },
    {
      "axis": "前份漂移：ma",
      "side_a": "本次「-」（週線均線證據包未涵蓋，不得填燈）",
      "side_b": "前份 ✅ 強勢進場",
      "ruling": "資料／方法論驅動為主（v17 證據包未含週線結構）；價格驅動為次——13 週 −22%、距 52 週高 −30%，✅ 幾乎確定不再成立，最可能落「價低於兩年線、高於五年線」帶，交閘複核",
      "evidence_level": "L1（價格）",
      "settle_metric": "週線 W52／W104／W250 位置",
      "if_then": [
        "若價低於五年線 → 首階仍三分之一但改分四段",
        "若站回兩年線 → 依原三段"
      ],
      "prior_field": "ma"
    },
    {
      "axis": "前份漂移：signal／val／trap（三欄皆未變：A／🟡／🟢）",
      "side_a": "本次 A／🟡／🟢",
      "side_b": "前份 A／🟡／🟢",
      "ruling": "無漂移；val 維持 🟡 的路徑不同——前份靠 PEG 1.55，本次靠盲點一救援（FY2026 PEG 2.12 偏貴、FY2027 PEG 1.80），方法論細節變、結論同",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "signal"
    },
    {
      "axis": "前份漂移：val 路徑（同上）",
      "side_a": "🟡",
      "side_b": "🟡",
      "ruling": "無漂移，見 signal 條目",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "val"
    },
    {
      "axis": "前份漂移：trap（同上）",
      "side_a": "🟢",
      "side_b": "🟢",
      "ruling": "無漂移；成長信號表新亮「倍數下移」一燈但五問定性仍非陷阱",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "trap"
    },
    {
      "axis": "前份漂移：moat_trend／runway_post_y5／rearm_trigger（前份格式無此三欄）",
      "side_a": "本次 ↑／🟢／$260 或 token 揭露",
      "side_b": "前份無此欄（v12.3 只有 moat 二維分 8/9）",
      "ruling": "方法論驅動（新欄）；護城河分由 9 降至 8.5 是本次對定價維度更保守（CEO 對定價權提問迴避，來源：摘要），屬判斷收緊非基本面惡化",
      "evidence_level": "L2",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "moat_trend"
    },
    {
      "axis": "前份漂移：asym_ratio／ev5y_pct／irr_base_pct／max_dd_pct／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct（前份格式無情境樹六欄）",
      "side_a": "本次 3.7／50.8／10.7／−50／$669.6／$206.8／25／30",
      "side_b": "前份無此欄（v12.3 只有 5Y 目標價 $540、upside +58%）",
      "ruling": "方法論驅動（情境樹為 v13 後新增）；可比部分：前份 5Y 目標 $540 vs 本次 Base $471——差異主因終端倍數本次取 30x 更保守，次因基準價下移",
      "evidence_level": "L2",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ],
      "prior_field": "asym_ratio"
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "SNPS／ARM 近 30 天無本站裁決可對",
      "side_b": "—",
      "ruling": "一句帶過：無近期 peer 裁決，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ]
    },
    {
      "axis": "指引上修卻低於共識 vs 賣方目標價全面上修（可調和）",
      "side_a": "FY2026 指引中值營收 $6.30B／EPS $8.10 略低於當時共識 $6.329B／$8.12",
      "side_b": "BofA／KeyBanc／Stifel 上修目標價至 $420-432",
      "ruling": "程度差異：公司一貫「一年一次、年初保守」（來源：摘要），共識已跑在指引前；本檔一年目標 $315 低於賣方，不依賴共識上修",
      "evidence_level": "L1",
      "settle_metric": "FY2027 指引 vs 共識 9.54",
      "if_then": [
        "若 FY2027 指引 <9.2 → 停止加碼",
        "若 ≥9.6 → 第二段"
      ],
      "evidence_refs": [
        "capital_markets_pricing#1",
        "capital_markets_pricing#4"
      ]
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "最新一季（Q2 2026，2026-07-27）法說逐字稿不在證據包，只有新聞稿 KPI；四季摘要止於 Q1 2026——管理層對 8 月軟體股拋售與 token 變現的最新口徑未親讀，AI 顛覆軸的判斷信心因此打折",
        "evidence_refs": [
          "substitute_technology#0"
        ]
      },
      {
        "text": "出口合規紀錄：2015-2021 對軍方大學非法出口、認罪＋$140M、三年緩刑——前提「管理層合規把關已修復」未經第三方驗證；若緩刑期內再違規，罰則與許可制風險同時升高",
        "evidence_refs": [
          "sec_investigation_restatement#0",
          "major_events#4",
          "reg_tariff_export#0"
        ]
      },
      {
        "text": "客戶信用：Intel（最大單一帳戶）BBB 展望負向、Samsung 代工虧損延至 2028——前提「前段客戶專案不延遲」在 2027 資本支出降檔時最脆弱；10-Q 應收集中度 2024 年末曾一客戶 11%",
        "evidence_refs": [
          "customer_concentration_credit#1",
          "customer_concentration_credit#2",
          "customer_concentration_credit#3",
          "customer_second_source#2"
        ]
      },
      {
        "text": "Hexagon $3.2B 換年化 $200M 營收（20x）——前提「physical AI 3-7 年兌現」由 CEO 自己說時點很難說（來源：摘要）；若 2027 未如承諾轉增益，資本配置等級降 C，長期信心上限降中",
        "evidence_refs": [
          "major_events#0"
        ]
      },
      {
        "text": "週線結構與五年連續分位皆證據包未涵蓋（分位只有 4 個年度點）——擇時層是本檔最薄的一層，首階三分之一即為此設計",
        "evidence_refs": [
          "geo_supply_chain#0"
        ]
      }
    ],
    "failure_story": "2027 年超大規模業者 AI 資本支出增速反轉，流片量遞延、續約漲幅歸零；BIS 同時恢復對華 EDA 許可，中國營收腰斬；市場把 EDA 由 AI 受惠者改列成熟軟體，倍數壓到 20x——5 年虧半。與唯一事件對照：⚠ 部分重疊（中國段撞上，資本支出段獨立）→ 已回補 secondary trigger（觸發器 5：Big-4 2027 指引）",
    "second_failure": "核心 thesis 完全兌現但以「AI 讓每專案人力減 30%、token 計費只補回人頭損失」的形態兌現：營收成長落在 8-10% 而非 15%，市場把估值框架從「AI 放大器 35x」切到「成熟工具商 22x」，5 年報酬近零——機率不可忽略，已反映在 Bear 終端 22x 與 Base 終端 30x（非現價 36x）",
    "max_dd": {
      "lo": -50,
      "hi": -35,
      "path_risk": "🟡",
      "trigger_time": "2027 上半年：Big-4 2027 資本支出指引（1-2 月）＋BIS 50% 規則落地後（2026-11）疊加 Q4 財報 FY2027 指引若 <+13%；恢復峰值需 FY2028 盈餘（約 2028 下半年）——若唯一事件觸發則 thesis 已破不談恢復"
    }
  },
  "kill_metrics": [
    {
      "metric": "積壓 TTM 年增",
      "bear_threshold": "連 2 季 <0",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "Core EDA 有機成長 TTM",
      "bear_threshold": "<8% 連 3 季",
      "window": "每季",
      "source": "法說分段成長率",
      "last_status": "ok"
    },
    {
      "metric": "中國營收佔比／許可狀態",
      "bear_threshold": "許可制恢復（唯一事件）；佔比連 4 季 <9%",
      "window": "每季＋事件",
      "source": "法說、BIS 公告",
      "last_status": "warning"
    },
    {
      "metric": "Big-4 2027 AI 資本支出指引年增",
      "bear_threshold": "任一 <+20%",
      "window": "2027-01 法說季",
      "source": "超大規模業者法說",
      "last_status": "unknown"
    },
    {
      "metric": "非 GAAP 營業利益率 TTM",
      "bear_threshold": "年減 >100bp 連 2 季",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "應收帳款客戶集中度",
      "bear_threshold": "任一客戶 ≥10%",
      "window": "每季",
      "source": "10-Q",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "指紋：毛利 85.9%、非 GAAP 營業利益率 45.5%、FCF 利潤率 28.6%、經常性 78%、資本支出約 3% → 資本輕高留存寡占 → 品質複利成長，信心高；無循環子型特徵（積壓 $8.1B 覆蓋 FY26 67%，非訂單型），不需 blend。implication：§4 用複利尺、§10 用前瞻本益比與 PEG。",
    "thesis": "H1 份額：IP +40%（Q2）vs SNPS IP 清淡年、硬體新客 30 家、系統廠 45%（兩年前 40%）→ 取份額有 sourced；H2 收費模式：CEO 稱 token-based＋基礎訂閱（來源：摘要）但無營收揭露 → 列驗證期限 FY2028；H3 槓桿：增量利潤率 59-60%（來源：摘要）、Q2 45.5% 優於指引高標。R1-R3 各對應 15 條負向 finding 中的 12 條，餘 3 條落威脅與盲點。唯一事件取政策軸：2025-05 已發生一次、10-K 明列可能重施、EPS 敏感度 −15-18% 為最大單一項。",
    "industry": "ID shortage／Phase II 以積壓創高、硬體交期中段、2027 設備銷售預期創高交叉驗證後載入；三軸裁決＝雙向拉鋸：A 競爭惡化（Siemens agent、Synopsys-Ansys 全棧）與 B 結構轉好（活動量計費、系統廠自研）並存，C 其他結構變數指名法規軸（BIS 50% 規則 2026-11-09）。閘 B：供需 durability 判結構性持久（TAM CAGR 8-9%、設計複雜度單向），bear 機率不因「產業在缺」壓低。TAM：純 EDA $18.2B→$33.5B（9.1%）。",
    "moat": "執行 9（份額三線同升、Palladium 六年紀錄）×定價 8（rational oligopoly、續約漲價 sourced 只在 SNPS、CEO 迴避定價權提問）→ 8.5 → A。閘一：GAAP 營業利益率 30.8% vs SNPS 9.7%，spread 正且擴大（Q2 +940bp）✓。閘二毛利無 >1.5pp 年減證據；閘三對手絕對美元新增證據包未涵蓋。趨勢 ↑：≥1 個 12 個月內 sourced data point（IP +40% 2026-07；COT 流片 2026-04）；閘 A 無最大客戶份額下滑證據（Intel 是在擴大灘頭）。§5.R：ROIIC 17.6%×再投資 88%＝天花板 15.5%，共識 17% 含淨回購 1% 在邊界內 → endo_ceiling_exceeded=false。",
    "growth": "Runway：EDA 市場 2026 $18.2B→2033 $33.5B，Cadence 30% 份額；以 13% 成長 vs 市場 9%，Y5 末份額約 35%、滲透遠未達 70% → 跑道 12 年、Y5 後 🟢（S 曲線中段＋sourced 第二曲線：ChipStack token 2026 下半年早期存取、physical AI／Hexagon）。分部加總：Core EDA 13-14%＋IP 17-20%＋SD&A 15-16% → 合併約 14%，與 Base EPS 14% 對得上（差 <5pp）。有機 vs 無機：三年併購貢獻約 2pp（CFO：14% 中約 2% 併購，來源：摘要）<30%。熄火壓測：成長降至 15%／10%／5% 對應本益比 30／24／18x → 自現價 −17%／−33%／−50%（以 FY1 EPS）。衰退信號 1 燈（倍數下移）→ 🟡。",
    "quality": "Q2：營收 $1,584M（+24.2%）、非 GAAP 營業利益率 45.5%、GAAP 28.4%、FCF $582.3M（36.8%，YTD 減 Q1 換算）、SBC 9.3%。TTM：GAAP 營業利益率 30.8%、FCF 利潤率 28.6% → FCF/營業利益 ≈0.93，轉換率高。營收 YoY 24.2%−GAAP 營業利益 YoY（19.0%→28.4% 隱含 +85%）→ divergence 深負＝利潤率擴張，無壓縮警示。回購 50% FCF、淨稀釋 ≤0。5 年 FCF 逐年與 CCC 證據包未涵蓋 → 標明，不推估。lumpiness 🟢：Q1 20.8%／Q2 36.8% 為出貨時點。",
    "governance": "計分卡 1/3 過（SBC 淨稀釋過；M&A ROIIC 未證——Hexagon 20x 營收；回購收益率 2.8% <6%）→ B。四項必涵蓋：股權結構／薪酬／內部人交易證據包未涵蓋（數據限制）；資本配置＝50% FCF 回購＋史上最大併購 $3.2B。重大事件：DOJ 認罪 $140M 為合規失靈（非 SEC 調查、非重編），進盲點與 R1；無集體訴訟。B 級不觸發持有年限上限。",
    "valuation": "FY1 8.14／FY2 9.54／FY3 11.14（2026-09-04 快照，stale=false）→ 前瞻本益比 35.96／30.68／26.27x；EPS CAGR (11.14÷8.14)^(1/2)−1＝17.0%；PEG 2.12（FY1）／1.80（FY2）。分位：trailing 本益比 60.6x 在 4 個年度點分位 32.8%（P/S 26.8、EV/S 30.3）→ 🟡 帶。較嚴讀法（FY1 PEG 2.12）落 🟠，盲點一（成長 🟢＋PEG_fy2 1.80 <2＋AI 🟢）救回 🟡；盲點三不成立（90 天上修 +2.4%）。目標：1Y 9.54×33＝$314.8（+7.6%）、2Y 11.14×33＝$367.6（+25.6%）、5Y 15.7×30＝$471（+60.9%）；Bear anchor 7.33×24＝$175.8（−39.9%）。Base IRR 約 10.0% 不含息＋淨回購 0.7 ≈10.7%（中）；re-rate 貢獻為負（36→30x）→ 非估值依賴型。市場錯在哪：把「AI 減人頭」等同「AI 減 EDA 支出」，忽略活動量計費與每顆晶片 EDA＋IP 投資倍增。",
    "trap_analysis": "五問：模式＝倍數下移中的成長股；反證＝營收 +24.2%、積壓 $8.1B、指引上修、共識上修 +2.4%；正證＝trailing 本益比 78.9x→60.6x 而盈餘只升 2%、2026 為續約低年；空頭一擊＝2027 資本支出 <+20% → FY2027 EPS 8.6×22-24x＝$190-205（−30-35%）；持有期判別＝積壓年增連 2 季負＋Core EDA <10% 連 2 季。定性 🟢 非陷阱（倍數觀察）。自我攻擊三點：(1) ↑ 只靠管理層自述？→ 有第三方（datagravity 多代工卡位、Next Platform COT 流片）但仍交閘複核；(2) 進場是否只因跌 30%？→ 否，一年目標 +7.6% 弱、靠 5 年 +61% 與品質，故首階三分之一；(3) 中國風險是否該直接觀望？→ 12-13% 曝險已在唯一事件與 Bear 30% 定價，觀望需 binding constraint 而非多因素模糊——三點皆未推翻。",
    "premortem": "Max DD：Bear anchor −40%、Bear 5Y −29%、2022 年 trailing 本益比低點 51.7x 對現 60.6x 隱含 −15% 倍數＋盈餘下修 10% → 範圍 −35%~−50%（寬 15pp ≥10pp），🟡；觸發 2027 上半年；thesis 完整（趨勢 ↑、跑道 🟢、非估值依賴）→ 不因波動砍倉，註記深回撤心理準備。失敗故事與唯一事件 ⚠ 部分重疊 → 回補觸發器 5。第二敗局成立 → Bear 終端 22x、Base 終端 30x。"
  },
  "evidence_dismissed": [],
  "plain": {
    "verdict_line": "進場，當核心持股，但先買三分之一。",
    "verdict_sub": "現價先建三分之一，跌到 $260 或公司公布 token 營收再加一段，BIS 十一月規則落地無新管制再補最後一段。",
    "five": {
      "how_it_makes_money": "賣晶片設計軟體、驗證硬體與設計 IP 給全球約 60 家大晶片與系統公司，多年合約、78% 是經常性收入。",
      "why_now": "股價從高點跌了 30%，跌到前一份報告等待的位置以下；同時營收年增 24.2%、積壓創高、全年展望上修。市場在怕 AI 顛覆軟體，公司卻在加速。",
      "why_this_size": "五年基本情境年化報酬約 10.7%，屬中等；一年內上檔只有 7.6%、下檔可到 −40%。好生意、價格只是合理，所以核心角色但分三段買。",
      "biggest_fear": "美國恢復對中國的 EDA 出口許可制——中國佔營收 12-13%，2025 年已經發生過一次六週的版本。",
      "how_to_act": "首階三分之一現價買；第二段看 $260 或 token 營收揭露；第三段看 2026-11-09 BIS 規則落地。清倉只認許可制恢復。"
    },
    "business": {
      "what_to_whom": "把設計、驗證、模擬晶片的工具與現成 IP 賣給晶片公司、代工廠與自研晶片的雲端／車廠，約 60 家客戶貢獻 70% 營收。",
      "why_customers_stay": "先進晶片不經簽核工具不能流片；換工具等於整套驗證重跑；合約多年、67% 的今年營收在年初就已鎖在積壓裡。",
      "moat_direction": "護城河 A 級、方向擴大：IP 年增逾 40% 而對手自認清淡年，硬體新增 30 家客戶。最弱處是定價：AI 代理的 token 計費還沒變成營收，執行長對定價權提問也只談交付價值。"
    },
    "bets": [
      {
        "claim": "AI 讓晶片設計活動量增加，Cadence 的收費會跟著活動量走，不會被客戶減人頭拖垮。",
        "wrong_when": "到 2028 年仍看不到任何 token 或消費型營收揭露，且核心 EDA 成長連三季低於 8%。"
      },
      {
        "claim": "三線同時取份額會延續：IP、驗證硬體、系統模擬。",
        "wrong_when": "積壓年增連兩季轉負，或系統廠客戶佔比連兩年下降。"
      },
      {
        "claim": "增量利潤率 60% 會把營業利益率推向 48% 以上。",
        "wrong_when": "非 GAAP 營業利益率連兩季年減超過 100 個基點，或增量利潤率連兩年低於 40%。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "對中國出口管制收緊：中國佔 12-13% 營收，BIS 50% 規則 2026-11-09 到期，許可制若恢復是清倉級。"
      },
      {
        "clock": "🔥",
        "text": "2027 年 AI 資本支出降檔：任一大型雲端業者指引年增低於 20%，流片與續約會延後 6-12 個月傳導。"
      },
      {
        "clock": "🐢",
        "text": "客戶集中與信用：最大單一帳戶 Intel 信評已到 BBB，Samsung 代工虧損延到 2028；約 60 家客戶佔七成營收。"
      }
    ],
    "market_wrong": "市場把「AI 讓每個專案少 30% 工程師」讀成「AI 讓 EDA 支出減少」。但 Cadence 的成長來自設計活動量，不是人頭；自研晶片的雲端業者把每顆晶片的 EDA 與 IP 投資推高一倍。賣方共識目標價中位數 $405 也高於本檔的一年目標 $315，本檔不靠共識上修就成立。",
    "growth_funding": "內生成長天花板約 15.5%（增量報酬 17.6% 乘再投資 88%），共識 17% 的盈餘成長扣掉約 1% 淨回購後落在邊界內，不需要靠估值重評。",
    "stories": {
      "bull": "token 計費在 2027 年變成看得見的營收，Hexagon 的 physical AI 模擬開始賣，成長守住 18-20%，市場維持 36 倍本益比，五年翻一倍多。",
      "base": "成長從 16% 緩降到 12%，營業利益率擴到 48%，本益比從 36 倍降到 30 倍，五年上漲約 61%、年化約 10.7%。",
      "bear": "2027 資本支出降檔加上中國管制回來，盈餘五年只從 8.14 走到 9.4，市場改用成熟軟體 22 倍定價，五年跌 29%。"
    },
    "change_my_mind": [
      {
        "what": "BIS 是否恢復對華 EDA 出口許可制",
        "threshold": "正式通知且 90 天內未撤銷",
        "then": "清倉，不等財報",
        "when": "2026-11-09 起持續"
      },
      {
        "what": "核心 EDA 有機成長與積壓",
        "threshold": "成長低於 8% 連三季且積壓年增連兩季為負",
        "then": "清倉，重啟須重跑報告",
        "when": "2027-08-31"
      },
      {
        "what": "token 營收是否揭露、股價是否到 $260",
        "threshold": "任一成立",
        "then": "加第二個三分之一",
        "when": "2027-02-28"
      }
    ],
    "prior_compare_reason": "與 2026-05-04 前份相比，主因是價格：股價從 $340.94 跌到 $292.7，落到前份等待的回測帶以下；基本面反而更好，方法論新增了決策層與情境樹。",
    "how_to_lose": "第一種死法：2027 年 AI 資本支出反轉加上中國管制回來，盈餘停滯、倍數壓到 20 倍，五年虧一半。第二種死法：AI 真的讓每個專案少 30% 人力，token 計費只補回人頭損失，成長掉到 8-10%，市場把它當成熟工具商用 22 倍定價，五年報酬接近零。",
    "evidence_quality": "十四軸覆蓋，營運數字以 2026 年第二季（7 月 27 日公告）為準；最新一季法說逐字稿缺檔、四季內容全靠摘要（2025 年第三季至 2026 年第一季）與六場投資人會議摘要，沒有親讀任何一季。週線均線與五年連續分位不在證據包。"
  }
}

```

---

## references/critic-gates.md 全文

# references/critic-gates.md｜寫稿後 critic gate 協議全文（條件載入）

> **載入時點**：Part I + Part II 草稿完成後、spawn 任何 critic 之前（QC-41／QC-48／QC-50／QC-51 任一觸發即載入）。核心 SKILL.md 只留各 gate 的觸發條件與 fail-safe 方向;spawn prompt、checklist 全文、查證預算與合併載具條款在本檔。
> **本檔為 v15.1 文本層拆分的搬移件——條文逐字未動**（編號、門檻、失敗方向、模型指派一字未改）。四個 gate 的觸發條件、七軸 checklist、查證預算 ≤10／14、合併載具三條、fail-safe 方向、模型指派同樣一字不動；v15.2 只改下方「輸入與輸出格式」一節（讀法從摘錄改讀全文＋輸出檔頭固定機器可讀區塊）。

### 輸入與輸出格式（v15.2）

**輸入**：`python3 scripts/dd_sections.py text FILE` 全文（不是 HTML、不是摘錄；約 60–80KB）；前份 DD 亦用 `text`（QC-49 觸發器版本對照、QC-51 peer 對帳時適用）。WHY：全文冷讀在 VIK 實測抓到 8 個 🔴，優於舊摘錄規則；critic 端（opus）成本每份僅 7–15M token，本來就不是省 token 的優化對象——省 token 的正確目標是 writer 端修補迴合（詳見 SKILL.md【Token 紀律】與 changelog.md）。

**輸出**：critic 報告存 `notes/site-internal/dd/_critic_{TICKER}_{YYYYMMDD}.md`，**開頭固定機器可讀區塊**：
```
## FINDINGS
| # | 嚴重度 | 段落 id | 一句話 | 最小修法 |
|---|---|---|---|---|
| F1 | 🔴 | s10 | … | … |
## GATE: PASS / PASS-with-fixes / FAIL
```
段落 id 用 canonical id（`s1`…`s14`、`decision`、`s85`、`appA`／`appB`、`revlog`、`sources`、`dashboard`、`dd-meta`）；連動段（dd-meta／dashboard）也列。固定區塊之後才是下方各 gate checklist 的逐軸敘述全文。此區塊供 patch agent（乾淨 context，見 SKILL.md／delta-refresh.md）以 `sed -n` 直接取用 FINDINGS，不需重讀整份 critic 報告。

---

### QC-41｜寫稿後產業態勢獨立 critic（Boris verify-app pattern）
**寫 DD 的 agent ≠ 驗 DD 的 agent**：寫稿後必須由**獨立 critic**（不同 context／不同 model instance）冷讀，專問「這份 DD 漏了或低估了什麼產業變化」。
**何時強制**（任一即觸發）：① 裁決是**強方向**（進場 或 迴避）；② moat_trend 是**方向性**（↑ 或 ↓）；③ 標的屬**競爭動態／循環商品／法規敏感／B2B 客戶集中**型。其餘（穩定內需 + 觀望）→ 建議但可選。
**怎麼跑**（Part I + Part II 草稿完成後、最終 Write HTML 前）：
```
Agent({
  description: "Industry red-team {TICKER} DD",
  subagent_type: "general-purpose",
  model: "opus",            // 跨模型冷讀：writer 現為 sonnet，critic 必為 opus
  prompt: "你是獨立產業 critic（冷讀，未參與寫稿）。以下是 `dd_sections.py text` 全文：{貼上}\n
    請沿 4 軸找出這份 DD **漏掉或低估**的產業結構變化，每軸給「有沒有 sourced 證據顯示報告判錯」：\n
    ① 競爭惡化（份額流失 / 新進入者 / 客戶 second-source / 大客戶轉單）\n
    ② 供需 durability（緊缺/過剩是結構還週期、能否撐住、供給可逆性）\n
    ③ **其他結構變數（法規/政策/關稅/反壟斷/補貼、通路重構、商業模式轉移、替代技術、客戶結構轉移）** ← 開放軸，重點找報告完全沒提到的\n
    ④ priced-in（市場是否已反映；共識/賣方目標價 vs 現價）\n
    **⑤ 覆蓋面掃描（強制）**：逐軸點名「哪一軸整個沒查」——法規／地緣／各主要終端市場／政策。**缺軸本身即 🔴，不需先證明結論錯**。\n
    **⑥ 量化模組完整性抽查（強制）**：逐項驗算——(a) §5.R 增量 ROIC × 再投資率是否**真算**（非「估計約 X%」無推導），內生天花板是否與共識 EPS CAGR 交叉檢查（天花板 < CAGR ＝ sanity 失敗，須處理不得帶過）；(b) 情境樹 Bull/Base/Bear 的**EPS 價差是否實質**（若 Bull 僅靠終端倍數、EPS 幾乎等於 Base ＝ 退化，🔴）；(c) IRR 內部對帳（§10.5 ↔ §10.6 ↔ 5Y/10Y 年化是否自洽）。機械 gate `scripts/verify_dd_math.py` 已在 commit 層確定性重算 dd-meta 的 EV／IRR／AR／Max DD 恆等式／情境樹年期／模組存在性——委派 prompt 附有其輸出時**直接引用、不重複手算**，本項火力集中在腳本驗不了的推導真偽（a）、EPS 價差實質性（b）與正文層分解對帳（c）。\n
    **⑦ QC-54 白話呈現核（強制）**：查 §1 結論與 §13 統一裁決開場是否為 2-4 句白話敘事（這是什麼生意／為何這個裁決／什麼會改變它），非決策矩陣機器語言（row 編號、Hard/Soft Veto 逐項列舉）直接開場；決策矩陣逐 row 檢核表是否已收進 `<details>` 或附錄、正文只留「命中哪條路徑＋一句白話理由」；承重結論是否有任何一處只靠燈號/emoji（val 🟡、MA ✅ 等）表述而無完整白話句。**每違反一項 🟡；§13 開場為機器矩陣、完全無白話敘事開場 ＝ 🔴。**（WHY：2026-08-31 四份首輪 QC-40 合規 0/4，CRM §13 正文渲染整張 row 檢核表。）\n
    輸出每軸：🔴 報告判錯（附 sourced 證據 + 該怎麼改）/ 🟡 報告低估（補強）/ 🟢 報告判讀無虞。只講有 sourced 依據的，不臆測。\n
    **查證預算（強制）**：本次 WebSearch 查證上限 **10 輪**（若本次為多 gate 合併載具，上限 **14 輪**，prompt 會明說）。輪次優先投給 ① 嫌疑最大的覆蓋面缺軸 ② 與強方向裁決相反的證據面。預算用滿仍有未查證的嫌疑軸時**不得硬撐、不得臆測補白**，改在輸出末尾列「未及查證清單」（軸別 ＋ 你想下的查詢詞）。⑤ 與 ⑥ 屬內部驗算，**不佔搜尋預算、不得因預算用罄而跳過**。"
})
```
**查證預算（token 紀律，非 gate 降級）**：單一 critic spawn 的 **WebSearch 查證預算 ≤10 輪**，分配優先序＝① 嫌疑最大的覆蓋面缺軸；② 與強方向裁決相反的證據面（進場 → 查空方；迴避 → 查多方）。預算用滿仍有未查證嫌疑軸 → 於輸出末尾列「未及查證清單」，由 writer 決定是否人工補查（補查與否須在內部自檢留痕，不渲染）。**內部驗算項（⑤⑥）不耗搜尋預算、不得跳過**。查證本身**仍不得取消**（🔴 發現正是查證產出的），本條只封上限、不封下限。
**合併載具條款**：同一份 DD **同時觸發 ≥2 個寫稿後 critic gate**（QC-41／QC-48／QC-50／row 8b 循環 critic）時，**spawn 單一 opus critic**，一次冷讀、依序回答各 gate 的完整 checklist——獨立性的要求是「非 writer 的冷 context ＋ 跨模型」，不是「critic 彼此隔離」。硬性三條：① **每份 checklist 輸出獨立成段、逐項作答**，不得以一句話帶過或以「同上」互相稀釋；② **「無效輸出＝失敗一次，必重試」對每份 checklist 分別適用**——某份答非所問即該份無效，重試可只補跑該份，各 gate 的失敗額度與 fail-safe 方向（QC-48 降 row 8 觀望／QC-50 維持觀望）各自照舊；③ **合併時查證預算放寬為 ≤14 輪**，分配優先序同上。**單一 gate 觸發時照舊單獨 spawn。**（kill condition 已登記 knowledge/rule_ledger.md）
**收到 critic 回覆後**：任一軸 🔴（且附 sourced 證據）→ **回頭實際修正受影響章節**（moat_trend／§2.C 風險／§6.E normalized／§10.5 bear／§13 裁決），改完才 finalize（**尤其 ③ 軸 🔴 ＝抓到模板沒覆蓋的全新形狀**，必須補進 §2.C 並反映到裁決）；🟡 → 補強對應敘述；全 🟢 → 不動 finalize。**QC-40 適用**：渲染的是「修正後的分析」，不是「critic 說 X／我跑了 critic」的過程對帳。**2 次 spawn 仍失敗／critic 無回覆** → 標「獨立 critic 未能執行」於內部自檢，不阻斷 finalize（high-stakes 進場裁決建議人工補一輪）。**無效輸出＝失敗一次，必重試**：讀錯標的檔案／被其他文件污染／答非所問 → 視同該次 spawn 失敗，**必須重 spawn 一次乾淨的**，不得以「標記未能執行」直接跳過；無效次數計入「2 次失敗」額度。
**邊界**：QC-41 是 backstop 不是主力（主力是 QC-39 強迫去搜），不得因為有 QC-41 就鬆懈 QC-39 的三軸搜尋。

### QC-48｜爆發候選 Bull 冷讀 gate（row 8a 命中強制）
**觸發**：row 8a 資格條件（runway 🟢 + 動能位置非爆發尾端〔26 週漲幅錨〕+ 非估值依賴型 + moat ≠ ↓ + 估值 ∈ {🟠, 🔴}，🔴 時另附 F2 式紀律；AR 降為參考資訊）全過時，**必須 spawn 不同 model instance 的獨立 critic**（機制同 QC-41），專門冷讀 §10.5 Bull 列三件事：① Bull 依據是否引用 §3.F 滲透率算術（含關鍵分部量×價骨架），非敘事式 Bull；② P_bull 是否與 §10.7 pattern match 的歷史實現 IRR 相容（歷史 case 5 年 IRR 遠低於本案 Bull 隱含 IRR → 要求解釋差距）；③ §6.A'' runway 🟢 的 sourced 證據（滲透率推導／第二曲線來源）是否真實存在、可回溯。
**收到回覆後**：critic 判「Bull 依據不成立」（任一項 🔴）→ **裁決降 row 8 觀望**，§13 以一句話記錄結論（過程對帳不渲染）。通過 → 頁首裁決晶片副標必標「爆發候選」。**2 次 spawn 失敗 → 標「QC-48 未能執行」，裁決保守降 row 8 觀望**（與 QC-41 的不阻斷不同——8a 是升級路徑，驗證失敗不得升級）。**無效輸出視同失敗一次且必重 spawn**——8a/8b 不存在「critic 無效所以跳過驗證」的路徑：重試後仍無效＝2 次失敗＝降 row 8。
**查證預算與載具同 QC-41**：單獨 spawn 時 ≤10 輪、優先投給與 Bull 依據相反的證據面；合併時走合併載具條款（單一 opus critic、≤14 輪），本 gate 三項 checklist 須獨立成段逐項作答，該段答非所問即該份無效、只補跑該份，「2 次失敗 → 降 row 8 觀望」不變。
**邊界**：QC-48 只驗 Bull 依據與 runway 證據，不重審整份報告（那是 QC-41 的職責）；兩者可同時觸發、各跑各的。**row 8a 的「爆發候選」＝結構型數倍候選**（runway 🟢 的長抱 starter），與 picks 頁的「爆發榜」（循環拐點 × 站上年線型）是兩個概念共用一詞——後者走 §13 row 8b 循環衛星 + 附錄 B，不走 8a/QC-48。

### QC-50｜錯過成本反向 critic（觀望的唯一向上反駁通道）
**定位**：其餘 critic 全是只能往下打的閘，本條是**唯一的向上通道**——讓「觀望」在特定證據形狀下也要接受一次獨立反駁，而不是預設安全。
**觸發**（§13 裁決落為觀望，且任一命中）：① 步驟 1.6 q.py 顯示**前次同 ticker 觀望/迴避且 to-date 報酬 > +30%**；② FY1/FY2 共識 EPS 近 3 個月上修 ≥ +10%（與附錄 A 盲點 3 救援同源資料）。
**動作**：spawn 不同 model instance 的獨立 critic（機制同 QC-41），任務＝**反駁觀望**——用 §3.F 滲透率算術、§10.5 情境、上修資料與循環位置論證「條件式進場是否比觀望更誠實」。critic 只能建議升級為**進場·條件式**（分批 starter＋衛星帽，落 row 8a/8b 對應紀律，含該路徑自身的 critic 閘照跑），**不能強制翻面**；主筆若拒絕升級，§14 複審必須正面回應 critic 的兩個最強論點（不得只覆述原觀望理由）。
**查證預算與載具同 QC-41**：單獨 spawn ≤10 輪、優先投給「反駁觀望」所需的證據面；合併時走合併載具條款（≤14 輪），本 gate checklist 須獨立成段逐項作答——反向 critic 尤其不得被其他 gate 的向下論述稀釋。
**Fail-safe 方向（刻意不對稱）**：spawn 失敗 2 次 → **維持觀望**、標「QC-50 未能執行」，不阻斷輸出。與 QC-48 鏡像：升級路徑驗證失敗不得升級、反駁路徑執行失敗不強制降級。

### QC-51｜同形狀 peer 裁決一致性對帳
§13 定稿前，從步驟 1.6 的 `q.py {TICKER}` 輸出讀「所屬產業/主題」清單，對其中主題跑 `python knowledge/q.py --theme {關鍵字}` 看成員現裁決分布。若**同 archetype（QC-43）或同產業鏈位置的 peer 在 30 天內拿到不同裁決**，§11 交叉矛盾必須明文一句：「{peer} 於 {日期} 判 {裁決} 而本檔判 {裁決}，差異理由＝___（結構差異/循環位置差異/估值差異，須具體）」。**不強制同裁決**，只強制差異被說出來——說不出具體理由本身就是重審訊號。peer 無近期裁決或主題查無 → 一句「QC-51 無 30 天內同形狀 peer 裁決」帶過，不阻斷。


