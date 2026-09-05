你是 stock-analyst v17 的**判斷層閘（gate）**，標的 AVGO（20260905）。你未參與寫判斷，這是一次跨模型冷讀。你的任務只有一件：**依下列 ①–⑦ 逐條複核判斷物，計數判斷級 🔴**。

## 讀

gate bundle 全文附於本訊息最後（「===== BUNDLE =====」之後），**不要 Read 任何檔**，直接依其內容複核。

這份 gate bundle 已包含你需要的全部輸入：
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
⑧ **QC-49 前份漂移歸因**——`prior_dd.prior_meta` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都在 `contradictions[]` 有帶 `prior_field` 的獨立條目、且有三元歸因排序主因；漏欄或無歸因＝🔴。前份不存在時填 🟢 並註「無前份」。

每條的「指向欄位」必須具體：judgment JSON 路徑（如 `contradictions[3]`、`moat.roic_durability.endo_ceiling`、`decision_inputs.valuation_dependent`）或覆蓋軸編號（`axis#7`）。指不出欄位的意見不要寫進表。

## 輸出（一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/gate_audit.md`，格式固定，下游機械解析）

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

**輪次上限 `6` 輪。** 一次 Write 完成，寫完即回報，不要回讀自己寫的 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/gate_audit.md`。

## 回報（≤100 字）

判斷級 🔴 = N、🟡 = M，以及 🔴 各條的軸別與指向欄位。


===== BUNDLE =====

## ① 任務頭

標的：AVGO　日期：20260905　角色：stock-analyst v16.2 三步制的判斷層 critic（gate） agent。

輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。

---

## ③ Evidence 緊湊版

ticker=AVGO　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 357.89, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-09-02", "trading_days_since": 3, "flag_within_3d": true, "note": "距最近財報僅 3 個交易日（≤3）——估值層須用財報後價格（postMarketPrice/preMarketPrice），共識 EPS 標「財報前快照」"}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 4, "current": 45.48, "high": {"value": 135.24, "date": "2024-10-31"}, "low": {"value": 16.57, "date": "2022-10-31"}, "current_percentile_within_annual_points": 24.4}, "ps": {"n_points": 4, "current": 19.11, "high": {"value": 26.4, "date": "2025-10-31"}, "low": {"value": 5.6, "date": "2022-10-31"}, "current_percentile_within_annual_points": 64.9}, "ev_s": {"n_points": 4, "current": 19.51, "high": {"value": 27.16, "date": "2025-10-31"}, "low": {"value": 6.42, "date": "2022-10-31"}, "current_percentile_within_annual_points": 63.1}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 413.49, "fy1_eps": 11.38, "fwd_pe": 36.33}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 446.06, "fy1_eps": 11.36, "fwd_pe": 39.27}, {"snapshot_date": "2026-06-04", "price_used": 385.12, "fy1_eps": 11.62, "fwd_pe": 33.14}, {"snapshot_date": "2026-06-23", "price_used": 365.02, "fy1_eps": 11.62, "fwd_pe": 31.41}, {"snapshot_date": "2026-07-16", "price_used": 370.83, "fy1_eps": 11.62, "fwd_pe": 31.91}, {"snapshot_date": "2026-07-30", "price_used": 389.28, "fy1_eps": 11.63, "fwd_pe": 33.47}, {"snapshot_date": "2026-08-13", "price_used": 392.99, "fy1_eps": 11.63, "fwd_pe": 33.79}, {"snapshot_date": "2026-08-28", "price_used": 357.89, "fy1_eps": 11.63, "fwd_pe": 30.77}, {"snapshot_date": "2026-09-04", "price_used": 357.89, "fy1_eps": 11.63, "fwd_pe": 30.77}], "current": 30.77, "high": 39.27, "low": 30.77, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": -7.07, "return_26w_pct": 8.7, "excess_return_13w_pct": -11.6, "excess_return_26w_pct": -5.82, "benchmark": "^GSPC", "rsi14": 38.05, "rsi14_usable": true, "distance_from_52w_high_pct": -25.56, "distance_from_52w_low_pct": 22.17, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 11.63, "fy2": 19.33, "fy3": 30.0}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 11.63, "fy2": 19.5, "fy3": 26.43}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 11.62, "fy2": 19.06, "fy3": 25.65}, "fy1": {"revision_pct": 0.0, "from": 11.63, "to": 11.63, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": -0.87, "from": 19.5, "to": 19.33, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 13.51, "from": 26.43, "to": 30.0, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 0.09, "fy2_revision_90d_pct": 1.42, "fy3_revision_90d_pct": 16.96, "stale": false, "note": null}, "peer_financials": {"AVGO": {"gross_margin_pct": 68.28, "operating_margin_pct": 44.06, "fcf_margin_pct": 43.41, "rd_intensity_pct": 15.89, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "_note": "未給 --peers 且 --evidence 無 numbers.peer_valuation 可回退，只算自身一列", "NVDA": {"gross_margin_pct": 74.15, "operating_margin_pct": 64.02, "fcf_margin_pct": 46.97, "rd_intensity_pct": 8.22, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "MRVL": {"gross_margin_pct": 51.5, "operating_margin_pct": 16.41, "fcf_margin_pct": 19.06, "rd_intensity_pct": 25.46, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "AMD": {"gross_margin_pct": 53.2, "operating_margin_pct": 15.71, "fcf_margin_pct": 20.34, "rd_intensity_pct": 22.74, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "QCOM": {"gross_margin_pct": 54.23, "operating_margin_pct": 23.28, "fcf_margin_pct": 23.64, "rd_intensity_pct": 22.45, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-06-09", "url": "https://www.sec.gov/Archives/edgar/data/1730168/000173016826000054/avgo-20260503.htm", "excerpt": "Direct sales to one semiconductor solutions customer, which is a distributor, accounted for 42% of our net revenue for each of the fiscal quarter and two fiscal quarters ended May 3, 2026, and 29% of our net revenue for each of the fiscal quarter and two fiscal quarters ended May 4, 2025. We believe aggregate sales to our top five end customers, through all channels, accounted for approximately 45% of our net revenue for each of the fiscal quarter and two fiscal quarters ended May 3, 2026 and 40% of our net revenue for each of the fiscal quarter and two fiscal quarters ended May 4, 2025. We expect to continue to experience significant customer concentration in future periods. The loss of, or significant decrease in demand from, any of our top five end customers could have a material adverse effect on our business, results of operations and financial condition. From time to time, some of our key semiconductor customers place large orders or delay orders, causing our quarterly net revenue to fluctuate significantly. This is particularly true of our products used in AI and wireless applications as fluctuations may be magnified by the timing of customer deployments, as well as product launches. For infrastructure software, the relative volume of customer contracts signed with the right to terminate causes variations in revenue recognized in each period. 26 Table of Contents The following tables set forth net revenue by segment for the periods presented: Fiscal Quarter Ended Two Fiscal Quarters Ended Net Revenue by Segment May 3, 2026 May 4, 2025 $ Change % Change May 3, 2026 May 4, 2025 $ Change % Change (Dollars in millions) Semiconductor solutions $ 15,009 $ 8,408 $ 6,601 79 % $ 27,524 $ 16,620 $ 10,904 66 % Infrastructure software 7,178 6,596 582 9 % 13,974 13,300 674 5 % Total net revenue $ 22,187 $ 15,004 $ 7,183 48 % $ 41,498 $ 29,920 $ 11,578 39 % Fiscal Quarter Ended Two Fiscal Quarters Ended Net Revenue by Segment May 3, 2026 May 4, 2025 May 3, 2026 May 4, 2025 (As a percentage of net revenue) Semiconductor solutions 68 % 56 % 66 % 56 % Infrastructure software 32 44 34 44 Total net revenue 100 % 100 % 100 % 100 % Net revenue from our semiconductor solutions segment increased in the fiscal quarter and two fiscal quarters ended May 3, 2026 compared to the prior year fiscal periods due to strong demand for our networking solutions, primarily custom AI accelerators and AI networking products. Net revenue from our infrastructure software segment increased in the fiscal quarter and two fiscal quarters ended May 3, 2026 compared to the prior year fiscal periods primarily due to strong demand for our VMware Cloud Foundation (“VCF”) product.", "note": null}, "latest_quarter_kpis": {"_required": true, "quarter": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "items": [{"metric": "營收（GAAP）", "value": 29591, "unit": "US$ million", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com「Broadcom Inc. Announces Third Quarter Fiscal Year 2026 Financial Results and Quarterly Dividend」", "vs_consensus": "consensus 約 $29.36B–$29.47B（來源：web_search 綜合 LSEG／賣方彙整），實際 $29.591B 小幅超標", "prior_quarter": "Q2 FY2026: $22,187M（QoQ +33.4%）；YoY +86%（隱含 Q3 FY2025 約 $15.9B）"}, {"metric": "Non-GAAP 營業利益／利益率", "value": 67.9, "unit": "%", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release（Non-GAAP operating income $20,095M ÷ revenue $29,591M）", "vs_consensus": "未查得單季 non-GAAP 營益率 consensus 數字，僅有 guidance 對比（見下方 guidance 項）", "prior_quarter": "Q2 FY2026: 67.3%（$14,928M ÷ $22,187M）"}, {"metric": "GAAP 營業利益／利益率", "value": 53.9, "unit": "%", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release（GAAP operating income $15,955M ÷ revenue $29,591M）", "vs_consensus": null, "prior_quarter": "Q2 FY2026: 48.6%（$10,788M ÷ $22,187M）"}, {"metric": "自由現金流（FCF）", "value": 13665, "unit": "US$ million", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release（營運現金流 $14,197M － capex $532M）", "vs_consensus": null, "prior_quarter": "Q2 FY2026: $10,262M（占營收 46%）；Q3 占營收 46.2%，margin 持平"}, {"metric": "SBC 占營收／占 GAAP 營業利益 %", "value": 6.8, "unit": "% of revenue", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release（總 SBC $2,019M；占營收 6.8%，占 GAAP 營業利益 12.7%＝2019/15955）", "vs_consensus": null, "prior_quarter": "Q2 FY2026: SBC $2,092M＝占營收 9.4%、占 GAAP 營業利益 19.4%（2092/10788）——SBC 占營益比重季比明顯下降，主因營收/營益基期快速放大而 SBC 金額持平略降"}, {"metric": "管理層下季（Q4 FY2026）指引", "value": 34.8, "unit": "US$ billion revenue guidance", "as_of": "guidance given 2026-09-02，對應 Q4 FY2026（季末約 2026-11-01）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release：「Fourth quarter revenue guidance of approximately $34.8 billion」＋「non-GAAP operating income guidance of approximately 66 percent of projected revenue」", "vs_consensus": "Street revenue 預期約 $35.03B——guidance 約低於共識 0.7%，為財報後股價承壓的敘事來源之一", "prior_quarter": "Q3 FY2026 實際: revenue $29,591M／non-GAAP 營益率 67.9%；Q4 guidance 隱含 YoY +93%、non-GAAP 營益率略降至 ~66%"}, {"metric": "AI 半導體營收（segment KPI，非六項必填但為 AVGO 核心敘事錨）", "value": 16.7, "unit": "US$ billion", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release：Q3 AI semiconductor revenue $16.7B（YoY +221%，QoQ +54%）", "vs_consensus": null, "prior_quarter": "Q2 FY2026: AI 半導體營收 $10.8B（YoY +143%）；Q4 FY2026 guidance：AI 營收約 $21.7B（YoY +236%）"}, {"metric": "半導體解決方案／基礎設施軟體分部營收", "value": null, "unit": "US$ million", "as_of": "Q3 FY2026（季末 2026-08-02，公告於 2026-09-02）", "source": "公司新聞稿 investors.broadcom.com Q3 FY26 press release：Semiconductor solutions $20,839M（YoY +127%）；Infrastructure software $8,752M（YoY +29%）", "vs_consensus": null, "prior_quarter": "Q2 FY2026: Semiconductor solutions $15,009M；Infrastructure software $7,178M（與 10-Q/edgar_concentrations 既有數字一致）"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-09-03 | Broadcom's AI semiconductor (XPU) revenue reached $16.7B in Q3 FY2026, up 221% YoY; company guided toward tripling ASIC shipments, with ASIC-based AI server shipments projected to reach 27.8% of the market in 2026, growing 44.6% YoY versus 16.1% projected growth for merchant GPUs. | TechTimes, "Broadcom Custom AI Chip Revenue Surges 221% to $16.7B, Q4 Guidance Disappoints" (techtimes.com/articles/326405); Barchart, "Get Ready for ASIC Shipments to Triple With This Leading AI Stock" | moat_trend,thesis.H |
| competitive_share_entrants#1 | + | 2026-01-26 | Counterpoint Research (published 2026-01-26) projects Broadcom will remain the top AI server compute ASIC design partner, holding about 60% market share by 2027, despite growing competition from the Google-MediaTek alliance; ASIC shipments among the top 10 hyperscalers projected to triple between 2024 and 2027. | Counterpoint Research, "AI Server Compute ASIC Shipments to Triple by 2027 as Custom Silicon Enters Hyper-Growth Phase"; syndicated via Yahoo Finance/Benzinga "Broadcom Set To Dominate Custom AI Chip Market With 60% Share By 2027" | moat_trend,thesis.H |
| competitive_share_entrants#2 | - | 2026-07-31 | MediaTek raised its target on 2026-07-31 to capture 15%-20% share of an estimated $80B custom AI-chip market by 2027; its first AI accelerator for a major US cloud provider (a Google TPU inference chip, internally 'Zebrafish', built at 20-30% lower cost than Broadcom's design) is entering production in Q4 2026, with MediaTek expecting more than $2B in 2026 data-center revenue. | Yahoo Finance, "MediaTek Wants 20% of Custom AI Chips. Alphabet (GOOGL) Could Win Before Broadcom (AVGO) Loses" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#3 | - | 2026-08-20 | Google is deliberately assembling a four-partner custom chip supply chain for its TPU roadmap (Broadcom building the TPU v8 training chip 'Sunfish', MediaTek building the inference chip 'Zebrafish', Marvell in talks for a memory-processing unit and inference TPU, Intel handling Xeon/infrastructure processors) — described as intentional redundancy since dependence on any single partner creates pricing, capacity, and strategic-vulnerability risk; Marvell formalized its role via a commercial agreement with Google signed 2026-07-29. | TrendForce, "Marvell, AMD Reportedly Shake Up Google TPU Race, Putting Broadcom, MediaTek Under Pressure"; TheNextWeb, "Google assembles four-partner chip supply chain with Broadcom, MediaTek, Marvell to challenge Nvidia in inference" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#4 | + | 2026-06-24 | OpenAI and Broadcom unveiled their first tangible jointly developed silicon, the 'Jalapeño' AI accelerator, on 2026-06-24, part of a multi-year collaboration (announced October 2025) to deploy 10 gigawatts of OpenAI-designed custom AI accelerators between 2H2026 and the end of 2029 — a new design win expanding Broadcom's custom-silicon customer base. | Broadcom Inc. investor press release, "OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators" (investors.broadcom.com); OpenAI, same title (openai.com) | moat_trend,thesis.H |
| customer_second_source#0 | - | 2026-08-20 | Google's TPU v8 strategy (targeting TSMC 2nm, late 2027) explicitly splits design work across multiple qualified partners rather than relying solely on Broadcom: Broadcom builds the training chip ('Sunfish') while MediaTek builds the inference chip ('Zebrafish') at 20-30% lower cost — deliberately giving Google negotiating leverage from having each partner know a qualified alternative exists. | TrendForce, "Marvell, AMD Reportedly Shake Up Google TPU Race, Putting Broadcom, MediaTek Under Pressure"; TheNextWeb, "Google assembles four-partner chip supply chain with Broadcom, MediaTek, Marvell to challenge Nvidia in inference" | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#1 | - | 2026-07-29 | Marvell Technology entered a commercial agreement with Google on 2026-07-29 for development of custom semiconductor products, formally establishing Marvell as an additional qualified second-source design partner in Google's TPU/inference-chip supply chain alongside Broadcom and MediaTek. | KuCoin, "Marvell Enters Custom Chip Agreement with Google, Baidu Maintains Core TPU Value"; TrendForce (same article as above) | moat_trend,thesis.R |
| customer_second_source#2 | - | 2026-08-26 | Analysis published 2026-08-26 notes Broadcom's AI semiconductor revenue is built for six core customers, and each major hyperscaler customer (Google, Meta, Microsoft, Amazon, etc.) is simultaneously investing in its own internal chip-design capabilities that could eventually reduce dependence on Broadcom as an ASIC design partner; the relationships are characterized as "deep and sticky, but not permanent." | Trefis, "Broadcom's Real Risk Is Its Customer List" (trefis.com/stock/avgo/articles-v3/613000); syndicated via Yahoo Finance | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#3 | + | 2026-04-14 | Meta committed (announced 2026-04-14, alongside Broadcom CEO Hock Tan's decision to leave Meta's board) to deploying 1 gigawatt of custom in-house MTIA AI accelerators co-designed with Broadcom, extending the existing Meta-Broadcom ASIC co-design partnership through 2029 — Meta's chip IP remains in-house (MTIA) but Broadcom continues as the design/production partner rather than being displaced by a fully internal solution. | CNBC, "Meta commits to 1 gigawatt of custom chips with Broadcom as Hock Tan decides to leave board" | moat_trend,thesis.H |
| customer_concentration_credit#0 | - | 2026-05-03 | Broadcom's 10-Q for the two fiscal quarters ended 2026-05-03 discloses aggregate sales to the top five end customers at approximately 45% of net revenue, and sales to distributors at approximately 56% of net revenue. | SEC EDGAR, Broadcom Inc. Form 10-Q (avgo-20260503.htm) | thesis.R,decision_inputs.bear |
| customer_concentration_credit#1 | - | 2025-12-18 | Broadcom's FY2025 Form 10-K (filed 2025-12-18) discloses distributors at approximately 48% of net revenue and the top five end customers at approximately 40% of net revenue. | Broadcom Investor Relations, Form 10-K filed 12/18/2025 | thesis.R |
| customer_concentration_credit#2 | - | 2026-05-03 | Broadcom's SEC filings risk factors state that top customers, including AI solutions customers, may cancel, reduce, or delay orders due to reduced capex spending, a business downturn, being designated a 'supply chain risk' by a government, purchasing from competitors, or developing customer-owned tooling instead of buying from Broadcom; top AI customers may also push for leasing/alternative financing models over outright purchase. | Broadcom SEC filings (10-K/10-Q risk factors) | thesis.R,decision_inputs.bear |
| customer_concentration_credit#3 | - | 2026-05-08 | OpenAI — a disclosed Broadcom custom AI chip partner under the 'Project Nexus' program to build an inference chip codenamed 'Jalapeno' — was unable to close roughly $18 billion of financing tied to the deal as of early May 2026; reporting states OpenAI is on track to lose about $14 billion in 2026 and burn more than $200 billion cumulatively through 2029, and that lenders are increasingly wary of AI infrastructure deals tied to projected OpenAI revenue. | DataCenterDynamics / Winbuzzer / Sherwood News reporting on OpenAI-Broadcom financing snag | thesis.R,decision_inputs.bear,triggers |
| customer_concentration_credit#4 | - | 2026-05-08 | Per the same reporting, Broadcom is reportedly willing to fund only the first phase of the OpenAI chip project unless Microsoft agrees to buy about 40% of the chips (to be installed in Microsoft data centers and rented back to OpenAI); OpenAI's head of compute reportedly called that structure 'financially unattractive' and 'likely unworkable,' and Broadcom separately relaxed its dollar-for-dollar capital-matching requirement, agreeing to front more capital than OpenAI itself. | Winbuzzer / Sherwood News reporting on OpenAI-Broadcom deal financing structure | thesis.R,decision_inputs.bear |
| supply_demand_durability#0 | + | 2026-06-26 | TSMC's CoWoS-L/S advanced packaging capacity is reported sold out through all of 2026 per TSMC CEO C.C. Wei; monthly CoWoS capacity is targeted to reach roughly 125,000-140,000 wafers/month by end-2026, up from about 35,000 wafers/month at end-2024, implying roughly 80%/year capacity growth still trailing demand. | SiliconAnalysts, "TSMC CoWoS Capacity 2026: Sold Out, 2nm Booked" / "TSMC CoWoS-L Capacity Reported Sold Out Through 2026" | thesis.H,decision_inputs.bear |
| supply_demand_durability#1 | 0 | 2026-06-15 | TrendForce reports the TSMC CoWoS supply-demand gap is expected to narrow from approximately 20% currently to approximately 10% by end-2026, with further improvement expected in 2027 as capacity expands — indicating the current packaging shortage is being closed by supply additions over a multi-year horizon rather than persisting indefinitely. | TrendForce, "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026" | thesis.H,valuation |
| supply_demand_durability#2 | - | 2025-12-10 | NVIDIA has booked over half of TSMC's CoWoS-L capacity for 2026-27 as of a December 2025 disclosure; Mizuho subsequently raised its forecast for TSMC's 2027 monthly CoWoS capacity to 190,000-200,000 wafers (from a 2026 target of ~140,000), signaling continued capacity competition between GPU and custom-ASIC packaging demand through 2027. | DigiTimes, "TSMC expands CoWoS capacity with Nvidia booking over half for 2026-27"; Mizuho forecast via Yahoo Finance | thesis.R,decision_inputs.bear |
| regulatory_antitrust#0 | - | 2026-02-06 | European Commission opened a formal antitrust investigation into how Broadcom handles VMware access, pricing, and contract terms for EU infrastructure customers, following complaints from cloud providers and trade group CISPE calling for Digital Markets Act scrutiny. | Bloomberg, "Broadcom Faces Mounting EU Scrutiny Over VMware Licensing Curbs" | moat_trend,thesis.R,decision_inputs.bear |
| regulatory_antitrust#1 | - | 2026-08 | Broadcom sued EU antitrust authorities to block a document request that included confidential legal advice related to the VMware acquisition; the EU General Court rejected Broadcom's application, and Broadcom lost this specific court bid. | Investing.com / gurufocus.com, "Broadcom loses EU court bid over VMware antitrust documents" | thesis.R,decision_inputs.bear |
| regulatory_antitrust#2 | - | 2026-07-16 | U.S. regulators opened a separate antitrust probe into VMware licensing practices after Broadcom completed the VMware acquisition. | Simply Wall St News, "Broadcom (AVGO) Faces VMware Antitrust Probe And AI Server Patent Investigation" | thesis.R,decision_inputs.bear |
| regulatory_antitrust#3 | - | 2026-07-16 | The U.S. International Trade Commission launched a separate probe into alleged infringement of Netlist memory-chip patents by Broadcom and partners including Google and Nvidia (an IP/patent investigation distinct from the VMware antitrust matter). | Simply Wall St News, "Broadcom (AVGO) Faces VMware Antitrust Probe And AI Server Patent Investigation" | thesis.R |
| regulatory_antitrust#4 | - | 2026-01-19 | China targeted VMware in a new regulatory crackdown, using national-security rhetoric to push for removal of American software such as VMware's core virtualization layer from Chinese enterprise environments; Broadcom shares slid on the news. | FinancialContent/MarketMinute, "Broadcom Shares Slide as China Targets VMware in New Regulatory Crackdown" | thesis.R,decision_inputs.bear,moat_trend |
| regulatory_antitrust#5 | - | 2026 | China banned the use of Broadcom's cybersecurity solutions within its jurisdiction, a separate regulatory action from the VMware licensing dispute. | Yahoo Finance, "China Just Banned Broadcom's Cybersecurity Solutions. What Does That Mean for AVGO Stock?" | thesis.R,decision_inputs.bear |
| reg_tariff_export#0 | - | 2026-01-15 | On January 15, 2026, the U.S. president issued Proclamation 11002 under Section 232, imposing a new 25% ad valorem tariff on certain high-end semiconductors and their derivative products (Commerce Dept. found imports threaten to impair U.S. national security); NVIDIA H200 and AMD MI325X are cited as example covered devices, and coverage of Broadcom's specific AI ASIC products depends on classification. | EY Global Tax News, "US Section 232 proclamation imposes 25% tariff on certain semiconductors"; CBP CSMS #67400472 | decision_inputs.bear,triggers |
| reg_tariff_export#1 | - | 2026-05-03 | Broadcom's own SEC 8-K filings (FY2026 series) acknowledge continuing uncertainty related to tariffs and trade restrictions/tensions as a disclosed risk factor. | SEC EDGAR, Broadcom Inc. Form 8-K exhibits (FY2026, e.g. avgo-05032026x8kxex99.htm / avgo-08022026x8kxex99.htm) | decision_inputs.bear |
| reg_tariff_export#2 | 0 | 2026-01-15 | BIS (Bureau of Industry and Security) published a final rule effective January 15, 2026 revising export license review policy for advanced AI/computing semiconductors destined for China and Macau: applications now reviewed case-by-case instead of under a presumption of denial, but exporters must still confirm no restricted/Entity List/Military End-User parties are involved. | Morgan Lewis, "BIS Revises Export Review Policy for Advanced AI Chips Destined for China and Macau" | thesis.H,decision_inputs.bear,triggers |
| reg_tariff_export#3 | - | 2026 | A U.S. ban on Chinese-made optical transceivers could reduce demand for DSPs used in those transceivers, with Broadcom named among AI-infrastructure suppliers potentially affected by this trade restriction. | TradingView News, "Weekly Recap: Google AI ASIC deal and Broadcom Inc. silicon & networking" | decision_inputs.bear,thesis.R |
| reg_tariff_export#4 | - | 2026 | Broadcom derives a meaningful portion of revenue from China, and ongoing US-China trade tensions are described as a persistent headline risk for the company's semiconductor and networking business. | TradingView News, "Weekly Recap: Google AI ASIC deal and Broadcom Inc. silicon & networking" | decision_inputs.bear |
| geo_supply_chain#0 | - | 2026 | Broadcom is fabless and depends on TSMC in Taiwan for manufacturing of its advanced chips (including custom AI accelerators); Broadcom's own risk disclosures identify geopolitical instability, including China-Taiwan relations, as a risk factor given that semiconductor manufacturing and sourcing are heavily concentrated in Asia. | The Strategy Story, "Broadcom PESTEL Analysis 2026" | moat_trend,thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | - | 2026 | TSMC controls approximately 70% of global foundry revenue and over 90% of the world's most advanced chip production at leading-edge nodes (3nm and below); TSMC's CoWoS advanced packaging, which is critical for every major AI accelerator including Broadcom's XPUs, is fully booked through 2026 with demand growing 113% annually, making advanced packaging (not wafer capacity) the primary chokepoint for AI chip supply. | EnkiAI, "AI Chip Supply Chain Risk 2026: Your Essential Guide"; Longyield Substack, "The Taiwan Semiconductor Risk" | moat_trend,thesis.R,decision_inputs.bear,triggers |
| geo_supply_chain#2 | - | 2026 | Broadcom executives have flagged a 2026 chip supply squeeze, warning that TSMC capacity has moved from 'almost unlimited' to a bottleneck, with shortages spreading beyond leading-edge wafers to laser/optical devices and printed circuit boards — a company-acknowledged supply constraint limiting near-term AI revenue fulfillment. | Astute Group, "Broadcom flags 2026 chip supply squeeze as TSMC capacity tightens under AI demand"; Bitget News | thesis.R,decision_inputs.bear,triggers |
| geo_supply_chain#3 | 0 | 2026-04 | Foundry diversification efforts are underway (TSMC's $165B Arizona expansion producing 3nm chips from late 2026, plus Japan and Germany fabs), but these address only a small fraction of total advanced-node capacity; reshoring is expected to take a decade to meaningfully reduce dependence on Taiwan-based production. | Sourceability, "Geopolitics Are Reshaping Semiconductor Supply Chain Risk in 2026"; The Hilltop, "Taiwan Strait Tensions Push Countries to Diversify Semiconductor Supply Chains" | moat_trend |
| end_markets#0 | + | 2026-09 | [Semiconductor solutions — AI/custom accelerators & networking] Broadcom's AI semiconductor revenue (custom XPU accelerators plus AI networking) reached $16.7B in fiscal Q3 2026, up 221% year-over-year and 54% sequentially; management guided fiscal 2026 AI semiconductor revenue of $58B (up 186% YoY) and stated it has 'line of sight' to $115B in AI semiconductor revenue in fiscal 2027 (roughly double FY2026), driven by multi-year deployment commitments from Google, Meta, OpenAI and Anthropic. | Converge Digest, "Broadcom's AI Business Hits $16.7B as XPUs, Ethernet and Optics Accelerate"; TradingView/Zacks, "AI Accelerators and Networking Fuel Broadcom's Growth" | thesis.H,moat_trend,valuation |
| end_markets#1 | + | 2026-06 | [Infrastructure software — VMware Cloud Foundation] Infrastructure software revenue grew 9% YoY to $7.2B in fiscal Q2 2026, with Broadcom guiding an acceleration to approximately $8.9B (up 31% YoY) in fiscal Q3 2026; management continues to expect low-double-digit growth for infrastructure software in FY2026, with VCF-based annual recurring revenue up 17% YoY as enterprises adopt VCF to manage AI workload complexity (CPUs/GPUs/storage/networking under one private-cloud control plane). | Yahoo Finance, "VCF is Becoming Broadcom's Growth Engine: More Upside Ahead?"; Futurum Group, "Broadcom Q1 FY 2026 Earnings Driven by XPU Momentum" | thesis.H,valuation |
| end_markets#2 | 0 | 2026-03 | [Semiconductor solutions — non-AI: broadband, wireless, server storage, networking/connectivity] Non-AI semiconductor revenue was $4.1B in fiscal Q1 2026, flat year-over-year: enterprise networking, broadband, and server storage revenues were up YoY, offset by a seasonal decline in wireless — indicating the legacy semiconductor businesses are stable/mixed rather than a growth driver, in contrast to the AI segment. | Investing.com, "Broadcom FY25 presentation: $64B revenue, AI growth accelerates"; The Strategy Story, "Broadcom Business Model 2026" | thesis.H,valuation |
| substitute_technology#0 | - | 2026-08 | MediaTek 將其目標上修至搶佔 2027 年估計 800 億美元客製 AI 晶片市場的 15%-20%，首款為美國主要雲端業者設計的 AI 加速器將於 2026 Q4 量產，預估 2026 年資料中心營收逾 20 億美元；此舉可能為 Alphabet 帶來 Broadcom 以外的第二設計夥伴。 | Yahoo Finance / MarketWatch report, "MediaTek Wants 20% of Custom AI Chips. Alphabet (GOOGL) Could Win Before Broadcom (AVGO) Loses" | moat_trend,thesis.R,decision_inputs.bear |
| substitute_technology#1 | - | 2026-05 | 業界分析指出雲端業者正採取多來源（multi-sourcing）策略設計客製 AI ASIC——Google 已示範此模式——對 Broadcom 目前的主導地位構成威脅；即便如此，Broadcom 預計在 2027 年仍以 60% 市佔率保有 AI 伺服器運算 ASIC 首選設計夥伴地位，但市場觀察認為若客戶（如 Google、Meta）發展出完全自主的晶片能力，Broadcom 的 ASIC 特許業務可能在 3-5 年內受侵蝕。 | Hudson Labs, "Top Broadcom Competitors and Peers in 2026 ($AVGO)"; Tom's Hardware, "The custom AI ASIC state of play (May 2026)" | moat_trend,thesis.R,decision_inputs.bear,triggers |
| substitute_technology#2 | 0 | 2026-05-13 | 光學 AI 加速器（optical/photonic computing）市場正快速成長，Ayar Labs、LightOn、Luminous Computing、Q.ANT、Salience Labs、Lightmatter、Optalysys 等新創正開發顛覆性架構，光學矩陣乘法引擎可在晶片層級以皮秒等級完成神經網路核心線性代數運算、耗能遠低於等效 GPU 運算，商用部署預期落在 2027-2031 年區間；Broadcom 本身也將光子能力納入其 AI 產品組合（如封裝內光學 I/O）。 | GlobeNewswire, "Optical AI Accelerator Market, 2026-2040 Industry Trends and Global Forecasts"; yieldWerx, "2026 Trends and Challenges in Photonics & Optical I/O Innovations" | moat_trend,thesis.R |
| channel_business_model_shift#0 | + | 2026-06 | Broadcom 已將 VMware 超過 8,000 個 SKU 目錄簡化為少數訂閱綑綁方案（旗艦為 VMware Cloud Foundation／VCF 與 vSphere Foundation），採每核心訂閱制計價以拉高平均交易金額；截至 2026 年年中，Broadcom 已將其 10,000 個最大 VMware 帳戶中逾 90% 遷移至訂閱制 VCF 綑綁方案。 | Redress Compliance, "Broadcom VMware Pricing Report 2026"; TierPoint, "Broadcom VMware Licensing Changes" | thesis.H,moat_trend,decision_inputs.bear |
| channel_business_model_shift#1 | - | 2026-01 | 2026 年 1 月 Broadcom 終止 VMware Cloud Service Provider（VCSP）合約，改為邀請制、以 VMware Cloud Foundation 為核心的新夥伴計畫；逾 400 家 VCSP 夥伴（多為長期經銷商）自 2026 年起無法再為既有客戶採購新授權或承接新客戶，官方鼓勵夥伴在 2026 年 3 月底前完成既有專案。 | LightEdge, "Broadcom VCSP 2026: What CSPs and Customers Need to Know"; Techzine Global, "Broadcom thins out VMware partner channel: forced migrations feared" | thesis.R,decision_inputs.bear,channel_business_model_shift |
| channel_business_model_shift#2 | 0 | 2026 | Broadcom 於 2026 年將其具爭議性的 VMware 夥伴計畫改造擴大推行至 EMEA 地區，新計畫要求夥伴須具備可交易並支援 VCF 的實證能力、投入實質技術與服務資源，並能管理客戶生命週期而非僅做單點產品交易；採計點數制認證 VCF／vSphere Foundation 資格。 | SDxCentral, "Broadcom's VMware partner program overhaul targets EMEA" | thesis.H,channel_business_model_shift |
| capital_markets_pricing#0 | + | 2026-09-02 | AVGO FY2026 Q3（2026-09-02 公布）營收 $29.59B、調整後 EPS $3.32，均超越財報前分析師共識（營收共識 $29.36B、EPS 共識 $3.24），為 beat-and-raise 型財報 | CNBC, "Broadcom (AVGO) Q3 earnings report 2026" (https://www.cnbc.com/2026/09/02/broadcom-avgo-q3-earnings-report-2026.html) | decision_inputs.bear,valuation,triggers |
| capital_markets_pricing#1 | + | 2026-09-02 | 公司財測（guidance）：Q4 FY2026 營收預期 $34.8B；AI 半導體營收預期加速至 $21.7B（yoy +236%）；FY2026 全年 AI 營收預期上修至 $58B（yoy +186%）；並首次揭露 FY2027 AI 營收指引約 $115B、FY2028 約 $230B（較 Q3 實際 AI 營收 $16.7B、yoy +221% 進一步加速） | BigGo Finance, "[Broadcom Q3 2026 Earnings Call] AI Revenue Triples to $16.7B as Broadcom Guides FY2027 to $115B and FY2028 to $230B" (https://finance.biggo.com/news/US_AVGO_2026-09-02) | thesis.H,decision_inputs.bear,valuation,triggers |
| capital_markets_pricing#2 | + | 2026-09-05 | 財報後至查詢當下，57 位分析師目標價均值 $520.03，過去 3 個月已上修 9.34%；買進評等佔比達 84%（分析師普遍將目標價定在 numbers.price_at_dd 之上） | ChartMill, "AVGO Forecast, Price Target & Analyst Ratings" (https://www.chartmill.com/stock/quote/AVGO/analyst-ratings) | valuation,decision_inputs.bear |
| capital_markets_pricing#3 | + | 2026-09-03 | 財報後個別分析師上修目標價：BMO Capital 由 $455 升至 $575（維持 Outperform）；Cantor Fitzgerald 由 $525 升至 $600（維持 Overweight）；Raymond James 由 $450 升至 $475（維持 Outperform）——上修方向與公司上修 FY2027/FY2028 AI 營收指引同步 | Benzinga, "These Analysts Increase Their Forecasts On Broadcom Following Upbeat Q3 Earnings" (https://www.benzinga.com/analyst-stock-ratings/price-target/26/09/61600199/these-analysts-increase-their-forecasts-on-broadcom-following-upbeat-q3-earnings) | valuation,triggers |
| major_events#0 | 0 | 2026-01-28 | Fidelity Investments 與 Broadcom 就『業務關鍵』軟體存取權爭議達成和解；Fidelity 原於2025年11月在麻州州法院對Broadcom提起訴訟指控其威脅切斷系統存取，該案已於和解後撤回 | Yahoo Finance / Finviz, "Fidelity Resolves Legal Dispute Around 'Business-Critical' Broadcom Software Access" | thesis.R,decision_inputs.bear |
| major_events#1 | - | 2025-08 | VMware（Broadcom子業務）高風險零日漏洞CVE-2025-41244（影響VMware Aria Operations與VMware Tools）遭中國國家背景駭客組織UNC5174自2024年底起持續利用進行權限提升攻擊，Broadcom已釋出關鍵修補程式因應 | TradingView News, "Broadcom patches VMware zero-day exploited by Chinese hackers" | moat_trend,thesis.R |
| major_events#2 | - | 2025-11-20 | Broadcom內部系統遭Clop勒索軟體集團透過Oracle E-Business Suite零日漏洞（CVE-2025-61882，CVSS 9.8）入侵，Clop於2025-11-20對外宣布掌握機敏資料並發出勒索威脅 | cybersecuritynews.com, "Broadcom Allegedly Breached by Clop Ransomware via Oracle E-Business Suite 0-Day Hack"; gbhackers.com corroborating report | thesis.R,decision_inputs.bear |
| major_events#3 | - | 2025-05-12 | 另一起員工資料外洩事件源自供應鏈廠商遭駭，竊得資料於2024年12月已現於網路上，但Broadcom直到2025-05-12才取得該資料副本並確認外洩範圍 | breachsense.com, "Broadcom Data Breach in 2025" | thesis.R |
| major_events#4 | 0 | 2025-11-02 | 近12個月無新重大併購案；上一樁重大交易（VMware收購）已於2023年11月完成，且VMware旗下EUC業務已於2024年7月出售予KKR，兩者皆在本次12個月查證窗口之外 | Broadcom FY2025 10-K (SEC EDGAR, avgo-20251102.htm); investors.broadcom.com press releases | decision_inputs.bear,valuation |
| major_events#5 | 0 | 2025-12-18 | Broadcom FY2025（12/18/2025提交）與FY2026 10-K封面之§240.10D-1(b)重編/高管獎酬追回分析勾選欄均為未勾選，顯示期內無構成重編（restatement）之錯誤更正、亦無觸發高管獎酬追回程序 | Broadcom Form 10-K filings (investors.broadcom.com static-files, filed 12/18/2025); SEC EDGAR avgo-20260201.htm, avgo-20260503.htm | decision_inputs.bear |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "none",
  "queries_run": [
   "AVGO Broadcom acquisition merger 2025 2026",
   "Broadcom acquisition target 2026 deal announcement semiconductor",
   "Broadcom AVGO acquisition merger 2025 2026",
   "Broadcom Fidelity lawsuit November 2025 breach of contract",
   "Broadcom AVGO chip defect recall data breach 2025"
  ],
  "findings": [],
  "note": "未查得近12個月新增併購案。VMware收購已於2023-11完成，VMware EUC業務出售予KKR已於2024-07完成，兩者皆早於本次12個月查證窗口。"
 },
 "lawsuit_class_action": {
  "status": "found",
  "queries_run": [
   "Broadcom AVGO class action lawsuit securities fraud 2025",
   "Broadcom Netflix lawsuit patent infringement 2026",
   "Broadcom class action lawsuit securities fraud 2025 2026",
   "Broadcom Fidelity lawsuit November 2025 breach of contract",
   "Broadcom WARN Act layoff Palo Alto October 2025",
   "Broadcom AVGO class action lawsuit securities fraud 2025 2026",
   "Broadcom CLOP data breach November 2025 class action lawsuit",
   "Broadcom \"$102.5 million\" settlement lawsuit"
  ],
  "findings": [
   {
    "claim": "Fidelity Investments與Broadcom之軟體存取權合約爭議訴訟（2025年11月麻州州法院提起）已於2026-01-28和解並撤回，非證券詐欺集體訴訟性質",
    "source": "Yahoo Finance / Finviz, \"Fidelity Resolves Legal Dispute Around 'Business-Critical' Broadcom Software Access\"",
    "as_of": "2026-01-28",
    "direction": "0",
    "affects": [
     "thesis.R",
     "decision_inputs.bear"
    ]
   }
  ],
  "note": "未查得新的證券詐欺集體訴訟（唯一歷史性證券集體訴訟案為2006年股票選擇權回溯記日案，已於2009-2010年和解了結，非本查證窗口事件）。查得的唯一近期訴訟為Fidelity軟體授權合約爭議，已和解，非集體訴訟。"
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Broadcom AVGO FDA clinical trial pharmaceutical device 2025",
   "Broadcom AVGO product launch recall warning letter chip defect 2025 2026",
   "Broadcom product recall warning letter FDA 2025 2026",
   "Broadcom SEC investigation restatement 2025 2026",
   "Broadcom AVGO clinical trial FDA approval 2025 2026",
   "Broadcom AVGO FDA clinical trial 2025 2026"
  ],
  "findings": [],
  "note": "Broadcom為半導體與基礎設施軟體公司，非藥品或醫療器材業務，已查證無相關臨床試驗、FDA核准或警告事項。"
 },
 "product_recall_warning": {
  "status": "found",
  "queries_run": [
   "Broadcom AVGO product recall warning letter chip defect 2025 2026",
   "Broadcom acquisition target 2026 deal announcement semiconductor",
   "Broadcom product recall warning letter FDA 2025 2026",
   "Broadcom AVGO acquisition merger 2025 2026",
   "Broadcom AVGO product launch recall warning letter",
   "Broadcom AVGO product recall warning letter 2025 2026",
   "Broadcom AVGO chip defect recall data breach 2025"
  ],
  "findings": [
   {
    "claim": "VMware高風險零日漏洞CVE-2025-41244（VMware Aria Operations／VMware Tools受影響）遭中國國家背景駭客組織UNC5174自2024年底起持續利用，Broadcom發布緊急修補公告與patch",
    "source": "TradingView News, \"Broadcom patches VMware zero-day exploited by Chinese hackers\"; Seeking Alpha, \"Broadcom falls amid VMware security vulnerability reports\"",
    "as_of": "2025-08",
    "direction": "-",
    "affects": [
     "moat_trend",
     "thesis.R",
     "triggers"
    ]
   },
   {
    "claim": "Broadcom內部系統經Oracle E-Business Suite零日漏洞（CVE-2025-61882，CVSS 9.8）遭Clop勒索軟體集團入侵，2025-11-20對外宣布並發出資料勒索威脅",
    "source": "cybersecuritynews.com, \"Broadcom Allegedly Breached by Clop Ransomware via Oracle E-Business Suite 0-Day Hack\"",
    "as_of": "2025-11-20",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear"
    ]
   }
  ],
  "note": "未查得傳統FDA/CPSC式產品召回；本組findings為半導體/軟體業最接近之類比——產品級安全漏洞揭露與緊急修補公告（VMware零日漏洞、Oracle E-Business Suite零日入侵），皆為2025年下半年事件。"
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Broadcom AVGO SEC investigation restatement 2025 2026",
   "Broadcom 10-K \"error correction\" OR \"immaterial correction\" restatement filing 2025",
   "Broadcom SEC investigation restatement 2025 2026",
   "Broadcom class action lawsuit securities fraud 2025 2026",
   "Broadcom 10-K restatement error correction incentive compensation recovery 2025"
  ],
  "findings": [],
  "note": "未查得SEC調查或財報重編。Broadcom FY2025（12/18/2025）與最新10-K封面§240.10D-1(b)重編/高管獎酬追回分析勾選欄均未勾選，顯示期內無構成重編之錯誤更正。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_AVGO_20260903.html",
 "date": "20260903",
 "schema": "v15.0",
 "dca_verdict": "進場",
 "dca_role": "衛星",
 "price_at_dd": 367.24,
 "revlog": {
  "status": "ok",
  "text": "版本修訂紀錄：v15.0首次全套重寫（自v14.2升級）。相較2026-06-23報告（進場｜核心持倉，price $391.51）：①最新Q3 FY26財報（2026-09-02）確認AI半導體營收+221%YoY、FY27/28 AI營收guidance首次量化為$115B/$230B（原僅定性「&gt;$100B」）；②財報後股價回檔至$367.24（Fwd PE 18.8x，較2026-06-23的21.8x進一步壓縮），估值端更具吸引力；③moat_trend由→降為↓（MediaTek取得Google次世代Triggerfish v9訓練＋推論同封裝獨家設計權、Marvell已簽約，供應商結構稀釋已從估計升級為sourced事實）；④新增EU CISPE反壟斷調查後續進展（美國VMware授權調查亦浮現）列入R3監測；⑤新增XPV平台（Apollo/Blackstone）融資結構分析，表外曝險達$29B（自陳）至$42B（BofA模型）、全量名目上看$370B，非單純量級可控。裁決維持進場，惟倉位角色由核心降為衛星。Inception DD：DD_AVGO_20260323.html（2026-03-23）。\n2026-09-03複審修訂：護城河趨勢改判、情境樹重建、角色調整。"
 },
 "prior_meta": {
  "ticker": "AVGO",
  "schema": "v15.0",
  "date": "2026-09-03",
  "price_at_dd": 367.24,
  "signal": "A+",
  "trap": "🟢",
  "trap_label": "🟢 非陷阱",
  "moat": "A",
  "val": "🟢",
  "ma": "✅",
  "fpe_fy2": 18.83,
  "pct_5y": 15.0,
  "peg_fy2": 0.33,
  "upside_short_pct": 11.5,
  "upside_mid_pct": 43.9,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "moat_score": 8.5,
  "growth_durability": 8.5,
  "quality_score": 8.5,
  "ai_risk": "🟢",
  "long_term_confidence": "低",
  "verdict": "A+",
  "oneliner": "客製AI ASIC龍頭＋AI網通＋VMware三引擎；FY27/28 AI營收guide再上修至$115B/$230B；財報後回檔至Fwd PE 18.8x（PEG 0.33）；惟MediaTek取得Google次世代訓練＋推論同封裝獨家設計權、Marvell已簽約，moat_trend降為↓，裁決進場｜衛星。",
  "dca_verdict": "進場",
  "dca_role": "衛星",
  "moat_trend": "↓",
  "runway_post_y5": "🟡",
  "ev5y_pct": 125.1,
  "irr_base_pct": 15.9,
  "max_dd_pct": -58.0,
  "asym_ratio": 6.0,
  "bull_5y_price": 1560.0,
  "bear_5y_price": 170.0,
  "p_bull_pct": 30.0,
  "p_bear_pct": 30.0,
  "archetype": "品質複利成長",
  "catalysts": [
   {
    "date": "2026-12-09",
    "type": "guidance",
    "event": "Q4 FY26財報＋FY27展望更新",
    "impact": "高",
    "watch": "FY27 AI營收guidance $115B是否維持或上修"
   },
   {
    "date": "2027-03-31",
    "date_precision": "quarter",
    "type": "regulatory",
    "event": "EU CISPE／VMware反壟斷調查後續進展",
    "impact": "中",
    "watch": "若裁定強制改變授權模式→軟體毛利率與ARR下修"
   },
   {
    "date": "2027-06-30",
    "date_precision": "quarter",
    "type": "capacity",
    "event": "新加坡先進封裝／基板廠量產爬坡",
    "impact": "中",
    "watch": "若延後→供給瓶頸緩解不如預期，出貨guidance承壓"
   },
   {
    "date": "2027-12-31",
    "date_precision": "quarter",
    "type": "other",
    "event": "Anthropic IPO時程",
    "impact": "中",
    "watch": "IPO完成改善XPV平台信用結構；延後則觀察擔保曝險"
   },
   {
    "date": "2027-06-30",
    "date_precision": "quarter",
    "type": "regulatory",
    "event": "美國對中國總部企業海外AI晶片授權新規（2026-06實施）執行細則落地",
    "impact": "低",
    "watch": "ByteDance相關5nm客製ASIC專案出貨是否受許可限制影響"
   }
  ],
  "base_eps_path": {
   "FY26": 11.63,
   "FY27": 19.5,
   "FY28": 26.43
  },
  "fy_end_month": 11,
  "eps_basis": "non-gaap-usd",
  "capalloc_grade": "A",
  "moat_execution": 9.0,
  "moat_pricing_power": 8.0,
  "upside_5y_pct": 109.5,
  "industry_clock_phase": "II",
  "kill_metrics": [
   {
    "metric": "Broadcom於Google客製晶片營收份額",
    "bear_threshold": "任一年度較Macquarie基準路徑（2026~95%→2027~80%→2028~65%）低逾10pp，或2027年度<75%→護城河重審",
    "window": "每年",
    "last_status": "ok"
   },
   {
    "metric": "FY27 AI半導體營收兌現度（guide $115B）",
    "bear_threshold": "連2季追蹤進度落後guide逾10%→減碼",
    "window": "2季",
    "last_status": "ok"
   },
   {
    "metric": "半導體方案分部營業利益率",
    "bear_threshold": "跌破55%（現61%，Q3 FY26 +440bp YoY）連2季→margin結構性壓縮警示",
    "window": "2季",
    "last_status": "ok"
   },
   {
    "metric": "VMware ARR年增率",
    "bear_threshold": "跌破10%（現15%，19%→17%→15%下滑中）連2季→軟體引擎減弱、H2假設降級",
    "window": "2季",
    "last_status": "ok"
   },
   {
    "metric": "Anthropic／OpenAI實際XPU出貨GW vs 公司自身guide",
    "bear_threshold": "FY27實際出貨低於自身guide 10GW逾20%→H1核心假設削弱",
    "window": "每季",
    "last_status": "ok"
   },
   {
    "metric": "XPV平台RVG名目擔保規模",
    "bear_threshold": "20GW全量擴張下BofA模型名目達$370B區間且信用展望維持負向連2季→表外槓桿重審",
    "window": "每季",
    "last_status": "ok"
   },
   {
    "metric": "v9 Triggerfish投產/放量進度",
    "bear_threshold": "2027年底如期投產、2028如期放量，且Broadcom未同步取得v10或後續世代設計權→moat等級重審",
    "window": "每季",
    "last_status": "ok"
   }
  ],
  "scenario_tree": {
   "terminal_label": "FY2031E",
   "start": {
    "eps": 19.5,
    "pe": 18.83,
    "eps_label": "FY2027E"
   },
   "eps": {
    "bull": [
     19.5,
     26.5,
     36.0,
     47.5,
     60.0
    ],
    "base": [
     19.5,
     20.88,
     25.6,
     31.4,
     38.47
    ],
    "bear": [
     19.5,
     19.0,
     18.2,
     17.5,
     17.0
    ]
   },
   "pe": {
    "bull": 26.0,
    "base": 20.0,
    "bear": 10.0
   },
   "p": {
    "bull": 30,
    "base": 40,
    "bear": 30
   },
   "yield_pct": {
    "dividend": 0.7,
    "net_buyback": 0.3
   },
   "second_stage": null,
   "valuation_dependent": false
  }
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
    "text": "客製AI ASIC設計領導地位維持，6大客戶群持續放量且分散化抵銷單一客戶份額稀釋",
    "columns": {
     "2Y驗證點": "FY27 AI營收達guide $115B±10%",
     "5Y驗證點": "FY28 AI營收達guide $230B±15%，Anthropic/OpenAI成為第1/2大客戶",
     "10Y驗證點": "客製ASIC對merchant GPU份額持續維持30%+（產業層級）",
     "具體數字門檻": "見§13 E12 #1（相對Macquarie路徑門檻，非單一絕對數字）",
     "信息來源": "公司法說＋Macquarie/SemiAnalysis產業研究",
     "漂移觸發條件": "連2季backlog兌現度落後guide逾10%→削弱"
    }
   },
   {
    "id": "H2",
    "text": "VMware軟體高黏性現金流持續成長，分散晶片週期波動",
    "columns": {
     "2Y驗證點": "ARR年增率不跌破12%（現15%，19%→17%→15%下滑中）",
     "5Y驗證點": "VMware Private AI Cloud成為企業AI推論第二成長曲線",
     "10Y驗證點": "軟體業務占總營收比重維持25-35%（現30%）",
     "具體數字門檻": "ARR連2季&lt;10%→H2削弱",
     "信息來源": "AVGO財報＋VCF採用數據",
     "漂移觸發條件": "ARR連2季&lt;10%YoY→削弱；EU CISPE裁定強制改授權模式→反轉"
    }
   },
   {
    "id": "H3",
    "text": "市場對AI複利成長給予合理（非過度）估值，PEG維持1以下區間",
    "columns": {
     "2Y驗證點": "Fwd PE（FY+2基準）不系統性壓縮至15x以下且無基本面惡化",
     "5Y驗證點": "5年後估值倍數normalize至20-25x仍反映moat與durability",
     "10Y驗證點": "—",
     "具體數字門檻": "Fwd PE連4季&lt;14x且非EPS上修驅動→削弱",
     "信息來源": "web共識＋Excel snapshot",
     "漂移觸發條件": "連4季TTM Fwd PE偏離5Y區間逾10%→削弱"
    }
   }
  ]
 },
 "R": {
  "status": "ok",
  "format": "table",
  "rows": [
   {
    "id": "R1",
    "text": "Google端份額稀釋快於預期——MediaTek已取得下一代Triggerfish（v9）獨家設計權（訓練＋推論同封裝，2027年底投產、2028年放量）；Marvell已於2026-07-29與Google簽約（Google取得最高$12.2B認股權證，對應Marvell至多$120B潛在營收，聚焦推論/週邊，非主力訓練TPU）；Intel已成第四家客製晶片夥伴；市場傳聞AMD洽談v10。反向L1：Broadcom與Google於2026-04簽署「未來世代TPU」長期協議，效期至2031，仍為主要設計夥伴，Anthropic並經此協議自2027年起取用約3.5GW算力（以Anthropic持續商業成功為前提，與§12 XPV表外擔保同源）",
    "columns": {
     "對應假設": "H1",
     "時間尺度": "🔥中期（4-6季）",
     "監測與警戒閾值": "見§13 E12 #1"
    }
   },
   {
    "id": "R2",
    "text": "四大雲端AI capex集體降溫（ROI疑慮兌現）→XPU訂單push-out，backlog兌現度不如guide",
    "columns": {
     "對應假設": "H1/H3",
     "時間尺度": "🔥中期",
     "監測與警戒閾值": "見§13 E12 #2"
    }
   },
   {
    "id": "R3",
    "text": "EU CISPE反壟斷調查＋美國VMware授權調查升溫→強制改變授權模式，軟體毛利率／ARR受壓",
    "columns": {
     "對應假設": "H2",
     "時間尺度": "🐢長期",
     "監測與警戒閾值": "見§13 E12 #10（延伸監測）"
    }
   }
  ]
 },
 "triggers": {
  "status": "ok",
  "format": "table",
  "rows": [
   {
    "n": "1",
    "觸發器": "Google客製晶片份額（相對路徑）",
    "類型": "風險",
    "對應": "R1/H1",
    "指標與門檻": "較Macquarie路徑低逾10pp，或2027&lt;75%（路徑95→80→65見§1）",
    "命中後動作": "重審moat等級，或觸強制迴避",
    "資料源／頻率": "產業研究／每年",
    "⏰": "2027-06-30",
    "status_now": null
   },
   {
    "n": "2",
    "觸發器": "FY27 AI半導體營收兌現度",
    "類型": "假設驗證",
    "對應": "H1",
    "指標與門檻": "連2季落後guide $115B逾10%",
    "命中後動作": "減碼",
    "資料源／頻率": "公司財報／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "3",
    "觸發器": "半導體分部OM",
    "類型": "風險",
    "對應": "財務品質",
    "指標與門檻": "跌破55%（現61%）連2季",
    "命中後動作": "margin結構性壓縮警示",
    "資料源／頻率": "公司財報／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "4",
    "觸發器": "VMware ARR年增率",
    "類型": "假設驗證",
    "對應": "H2",
    "指標與門檻": "跌破10%（現15%）連2季",
    "命中後動作": "減碼，H2降級",
    "資料源／頻率": "公司財報／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "5",
    "觸發器": "Anthropic/OpenAI實際XPU出貨GW",
    "類型": "假設驗證",
    "對應": "H1",
    "指標與門檻": "低於自身guide 10GW逾20%",
    "命中後動作": "H1核心假設削弱",
    "資料源／頻率": "公司財報／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "6",
    "觸發器": "XPV平台RVG擔保規模",
    "類型": "風險",
    "對應": "表外槓桿",
    "指標與門檻": "20GW全量下名目達$370B且信用展望連2季負向",
    "命中後動作": "表外槓桿重審",
    "資料源／頻率": "BofA模型／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "7",
    "觸發器": "v9投產/放量（下行）",
    "類型": "風險",
    "對應": "R1/H1",
    "指標與門檻": "2027底投產、2028放量如期，Broadcom未同步拿下v10",
    "命中後動作": "moat等級重審，或觸強制迴避",
    "資料源／頻率": "法說＋產業研究／每季",
    "⏰": "2027-12-31",
    "status_now": null
   },
   {
    "n": "8",
    "觸發器": "上行：v10或GW出貨超前",
    "類型": "假設驗證（上行）",
    "對應": "H1",
    "指標與門檻": "Broadcom取得v10，或GW出貨超前guide逾10%",
    "命中後動作": "重審角色，可能回核心",
    "資料源／頻率": "法說／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "9",
    "觸發器": "估值rearm：Fwd PE回落至歷史低點以下",
    "類型": "估值rearm",
    "對應": "H3",
    "指標與門檻": "Fwd PE（FY+2基準）跌破15x且基本面未惡化",
    "命中後動作": "加碼至目標倉位",
    "資料源／頻率": "自算／每季",
    "⏰": "",
    "status_now": null
   },
   {
    "n": "10",
    "觸發器": "EU CISPE／VMware調查裁定",
    "類型": "風險",
    "對應": "R3/H2",
    "指標與門檻": "強制改變授權模式或裁罰",
    "命中後動作": "重審H2假設",
    "資料源／頻率": "歐盟公告",
    "⏰": "2027-03-31",
    "status_now": null
   },
   {
    "n": "11",
    "觸發器": "新加坡封裝爬坡／ByteDance出口管制細則",
    "類型": "風險",
    "對應": "供給+政策",
    "指標與門檻": "前者若延後；後者落地限制ByteDance出貨",
    "命中後動作": "供給瓶頸不如預期／重審客戶集中度",
    "資料源／頻率": "公司揭露＋商務部公告",
    "⏰": "2027-06-30",
    "status_now": null
   },
   {
    "n": "12",
    "觸發器": "Anthropic IPO時程",
    "類型": "風險",
    "對應": "XPV信用",
    "指標與門檻": "完成或延後",
    "命中後動作": "改善或惡化XPV信用結構",
    "資料源／頻率": "公開市場",
    "⏰": "2027-12-31",
    "status_now": null
   },
   {
    "n": "13",
    "觸發器": "Q4 FY26財報＋FY27展望更新",
    "類型": "複審日期",
    "對應": "—",
    "指標與門檻": "—",
    "命中後動作": "重跑DD",
    "資料源／頻率": "公司財報／一次性",
    "⏰": "2026-12-09",
    "status_now": null
   }
  ]
 },
 "inception_dd": {
  "path": "docs/dd/DD_AVGO_20260418.html",
  "date": "20260418",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_AVGO_20260323.html",
  "date": "20260323",
  "days_from_365d_mark": 199
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "AVGO",
 "current_verdict": {
  "verdict": "進場",
  "fundamental_grade": "A+",
  "date": "2026-09-03",
  "freshness": "fresh",
  "source": "docs/dd/DD_AVGO_20260903.html"
 },
 "decision_history": [
  {
   "date": "2026-04-18",
   "verdict": null,
   "role": null,
   "price_at_decision": 406.54,
   "fundamental_grade": "A",
   "to_date_pct": -11.83,
   "days": 135,
   "source_report": "docs/dd/DD_AVGO_20260418.html"
  },
  {
   "date": "2026-06-04",
   "verdict": null,
   "role": null,
   "price_at_decision": 479.23,
   "fundamental_grade": "B",
   "to_date_pct": -7.07,
   "days": 88,
   "source_report": "docs/dd/DD_AVGO_20260604.html"
  },
  {
   "date": "2026-06-10",
   "verdict": null,
   "role": null,
   "price_at_decision": 392.16,
   "fundamental_grade": "A",
   "to_date_pct": -6.18,
   "days": 82,
   "source_report": "docs/dd/DD_AVGO_20260610.html"
  },
  {
   "date": "2026-06-22",
   "verdict": "進場",
   "role": "核心持倉",
   "price_at_decision": 411.35,
   "fundamental_grade": "A",
   "to_date_pct": -1.95,
   "days": 70,
   "source_report": "docs/dd/DD_AVGO_20260622.html"
  },
  {
   "date": "2026-06-23",
   "verdict": "進場",
   "role": "核心持倉",
   "price_at_decision": 391.51,
   "fundamental_grade": "A",
   "to_date_pct": -1.95,
   "days": 69,
   "source_report": "docs/dd/DD_AVGO_20260623.html"
  },
  {
   "date": "2026-09-03",
   "verdict": "進場",
   "role": "衛星",
   "price_at_decision": 367.24,
   "fundamental_grade": "A+",
   "to_date_pct": 0.0,
   "days": -3,
   "source_report": "docs/dd/DD_AVGO_20260903.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/AVGO.md\n[dd] 2026-09-03  DD Broadcom Inc.(AVGO)— 2026-09-03(統一裁決:進場)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260903.md\n[internal-note] 2026-09-03  Cold Review — DD_AVGO_20260903（v15.0, price $367.24, 裁決 進場｜核心）\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_AVGO_20260903.md\n[dd] 2026-06-23  DD AVGO Broadcom — 2026-06-23(統一裁決:進場)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260623.md\n[dd] 2026-06-22  DD|AVGO 博通 — v13 深度個股報告(2026-06-22)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260622.md\n[dd] 2026-06-10  DD|AVGO Broadcom — v12.5 深度研究 2026-06-10\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260610.md\n[dca] 2026-06-10  DCA|AVGO Broadcom — 深度定見分析 2026-06-10(v1.5)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_AVGO_20260610.md\n[dd] 2026-06-04  DD|AVGO Broadcom v12.4|2026-06-04\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260604.md\n[dca] 2026-06-04  DCA|AVGO Broadcom 定見|2026-06-04\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_AVGO_20260604.md\n[internal-note] 2026-05-17  v12.3 Cold Review — AVGO (Broadcom)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_AVGO_20260517.md\n[comparison] 2026-05-13  MS 2330TW vs NVDA vs AVGO 2026-05-13 | 多標的對比分析\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/comparisons/MS_2330TWvsNVDAvsAVGO_20260513.md\n[dca] 2026-05-11  DCA|AVGO|2026-05-11|Deep Conviction Analysis\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_AVGO_20260511.md\n[dca] 2026-05-07  AVGO Deep Conviction Analysis | 2026-05-07\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_AVGO_20260507.md\n[dd] 2026-04-18  DD AVGO - 2026-04-18\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260418.md\n[dd] 2026-04-16  DD_AVGO_20260416|Broadcom 深度研究\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260416.md\n[dd] 2026-04-12  DD Report — AVGO (Broadcom) | 2026-04-12\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260412.md\n[dd] 2026-04-11  DD_AVGO_20260411 — Broadcom 深度研究\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260411.md\n[dd] 2026-04-10  DD 報告|AVGO Broadcom Inc.|2026-04-10\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260410.md\n[dd] 2026-03-23  AVGO 深度研究報告 | 買側 DD\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_AVGO_20260323.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "ok",
 "primary": {
  "theme": "Hyperscaler 雲端三巨頭 — AWS / Azure / GCP",
  "path": "docs/id/ID_HyperscalerCloudBigThree_20260505.html",
  "skill_version": "v2.3",
  "as_of": "2026-05-05",
  "facts": {
   "status": "ok",
   "sections": {
    "supply": "PART III · SUPPLY SIDE\n 供給側：三巨頭分化與自研晶片利潤池\n 反直覺但可操作的結論：三巨頭的供給能力分化（成長/毛利/規模各有所長），且自研晶片把一塊原屬 NVDA 的利潤池移到 AVGO/MRVL 與 hyperscaler 自身。\n\n 供給端是「三巨頭 + 第四勢力 + 晶片供應」。三巨頭各有所長：GCP（+63%、加速最快、TPU 領先、Apple/Anthropic TPU deal）、Azure（+40%、op margin 最厚、$80B 受電力限的滿手需求、OpenAI/Anthropic 進駐、Maia ASIC）、AWS（30% 份額規模最大、但 +19% 落後、Trainium/Project Rainier ~500K）。第四勢力：ORCL（OCI、OpenAI Stargate、增速快毛利薄）、META（非 cloud seller 但 capex $125–145B 體量等同）、中國 BABA/騰訊。晶片供應：NVDA（主供 GPU）、AVGO（TPU base die + 客製 ASIC ~70%（hyperscaler 整體、業內估，非單一 TPU））、MRVL（Trainium base die）、AMD（dual-source）。利潤往「成長/毛利贏家 + 自研 ASIC 套利者」集中。\n\n \n Inference · 供給\n 三巨頭分化、自研晶片把利潤從 NVDA 移到 ASIC 套利者\n 前提：三巨頭成長/毛利/規模分化 + 自研 ASIC 25–30% 且升（GCP TPU/AWS Trainium/Azure Maia）+ ASIC 設計外包 AVGO/MRVL → 估值該分化、且一塊 GPU 利潤池移到 ASIC 套利者 + hyperscaler 自身\n 三巨頭不是同質籃子——GCP 賣成長 + TPU 自研優勢、Azure 賣毛利 + 受限需求、AWS 賣規模；估值該按此分化。同時自研 ASIC（25–30% 且升）把原本全給 NVDA 的加速器採購，分一塊給 AVGO（TPU base die ~70%、客製加速器 +140% YoY）、MRVL（Trainium base die ~55–60%），並降 hyperscaler 自身推論成本（強化雲端毛利）。NVDA 仍主供但 2027–28 面臨結構性份額侵蝕。\n 可證偽條件：若 NVDA 下一代（Rubin）效能/TCO 大幅領先使自研 ASIC 經濟性消失、或某一家 hyperscaler 成長/毛利同時碾壓另兩家（分化收斂成單一贏家），則「分化 + ASIC 套利」論的某一面失效。\n \n\n \n 三巨頭 + 晶片供應矩陣 · 定位與動能\n \n玩家 | 定位 / 動能（Q1'26） | 遷移 | 角色\nGCP（GOOGL） | +63%、RPO >$70B、TPU 領先 | ↑ | 成長 + 自研矽雙引擎\nAzure（MSFT） | +40%、毛利最厚、$80B 受電力限 | ↑ | 毛利 + 受限需求\nAWS（AMZN） | 30% 份額、+19%、AI run-rate >$15B | → | 規模最大但成長落後\nASIC 套利 AVGO/MRVL | TPU/Trainium base die、+140% YoY | ↑ | 自研晶片真套利者\nNVDA | 主供 GPU（GB300/Rubin） | → | 仍主供但份額被自研侵蝕\n\n \n 怎麼讀：GCP/Azure 在 ↑（成長/毛利），AWS 持平（規模大成長落後），AVGO/MRVL 在 ↑（自研 ASIC 套利），NVDA 持平（仍主供但份額被侵蝕）。成本曲線省略說明：雲端無單一產能成本曲線；關鍵是「每單位算力的折舊 + 電力成本」——自研 ASIC 與電力效率決定誰的雲端毛利撐得住。",
    "demand": "PART IV · DEMAND SIDE\n 需求側：AI 算力受限與 ROI 兌現\n 需求最反直覺的特徵是「不是賣不掉、是蓋不出來」——三家都算力受限（Azure $80B 訂單卡在電力）；最大的變數是這些 capex 的 ROI 何時、能否兌現。\n\n 第一引擎：AI 算力受限需求（現需）。需求不是問題——三巨頭都「compute-constrained」：Azure 有約 $80B 訂單因電力（非需求）無法交付、GCP RPO >$70B（多年期 AI 承諾）、AWS AI run-rate >$15B 三位數增。客戶要算力、hyperscaler 蓋不夠快，瓶頸在電力與先進封裝（見「Token 經濟學」）。第二引擎：ROI 兌現（核心賭注）。$380B+ capex、約 2/3 餵壽命短 GPU——折舊會打進成本線、壓縮雲端毛利。bull：算力受限 = 定價權，租金抵銷折舊；bear：折舊跑贏營收加速、毛利壓縮。payback 只有「雲端營收續加速」才成立——這是本主題最該盯的證偽點。\n\n \n 需求三角驗證 · 受限需求 vs capex vs ROI\n \n視角 | 數值 | 口徑\n受限需求（現需） | Azure $80B backlog（電力限）、GCP RPO >$70B、AWS AI >$15B | Q1'26 法說（T1）\ncapex（投入） | Big4 2026 $380B+（vs '25 ~$246B）、2/3 餵 GPU | 彙整估計（公司級口徑）\nROI 證偽 | 雲端營收加速 vs 折舊（定價權 vs 毛利壓縮） | 每季法說（趨勢）\n\n \n 怎麼讀：需求受限（蓋不出來，非賣不掉）證明需求真實、且給算力定價權；但 $380B+ capex 的 ROI 未證——折舊 vs 定價權的拉鋸，payback 看雲端營收能否續加速。採信「雲端營收加速 vs capex/折舊」作 ROI 的最硬證據，而非 capex 絕對額。\n\n \n 多空為何都對\n 多頭測AI 算力需求（受限、定價權），這幾乎沒爭議；空頭測capex ROI（折舊壓毛利、payback 未證）。兩者可同時為真：需求是真的、算力受限給定價權（多頭對），但 $380B+ 折舊若跑贏雲端營收加速、毛利會壓縮（空頭對）。本報告把重心放在「分化 + ROI 兌現」，而非「AI 雲端會不會成長」。"
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
   "theme": "Hyperscaler 雲端三巨頭 — AWS / Azure / GCP",
   "path": "docs/id/ID_HyperscalerCloudBigThree_20260505.html",
   "skill_version": "v2.3",
   "as_of": "2026-05-05",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  },
  {
   "theme": "CUDA / ROCm Software Moat",
   "path": "docs/id/ID_CUDARocmMoat_20260501.html",
   "skill_version": "v2.3",
   "as_of": "2026-05-01",
   "sd_verdict": "balanced",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  },
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
  },
  {
   "theme": "Token 經濟學 / AI 推論商業化",
   "path": "docs/id/ID_TokenEconomics_20260427.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-27",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  },
  {
   "theme": "AI Accelerator Demand",
   "path": "docs/id/ID_AIAcceleratorDemand_20260905.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-05",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "mid",
   "for_stage2_only": true
  },
  {
   "theme": "AdvancedPackaging",
   "path": "docs/id/ID_AdvancedPackaging_20260905.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-05",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "high",
   "for_stage2_only": true
  },
  {
   "theme": "CUDA / ROCm Moat",
   "path": "docs/id/ID_CUDARocmMoat_20260905.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-05",
   "sd_verdict": "split",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "high",
   "for_stage2_only": true
  },
  {
   "theme": "HBM 超級循環",
   "path": "docs/id/ID_HBM_Supercycle_20260904.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-04",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "high",
   "for_stage2_only": true
  },
  {
   "theme": "AI 算力資本週期",
   "path": "docs/id/ID_AIComputeCapexCycle_20260903.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-03",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "high",
   "for_stage2_only": true
  },
  {
   "theme": "AI Inference Economics",
   "path": "docs/id/ID_AIInferenceEconomics_20260720.html",
   "skill_version": "v3.0",
   "as_of": "2026-07-20",
   "sd_verdict": "split",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "mid",
   "for_stage2_only": true
  },
  {
   "theme": "AI Networking",
   "path": "docs/id/ID_AINetworking_20260419.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-19",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": null,
   "for_stage2_only": true
  },
  {
   "theme": "Advanced Packaging",
   "path": "docs/id/ID_AdvancedPackaging_20260419.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-19",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": null,
   "for_stage2_only": true
  }
 ],
 "note": "primary 由 conviction desc + publish_date desc 排序機械選出，非人工裁定——ticker 掛在多個產業主題下時，Stage 1 判斷層應覆核 candidates 是否有更貼題者。"
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AVGO/AVGO_Q4_2025_Earnings_Call_20251211.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/AVGO/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "AVGO_Q4_2025_Earnings_Call_20251211.md",
    "AVGO_Q1_2026_Earnings_Call_20260304.md",
    "AVGO_Q2_2026_Earnings_Call_20260603.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "Broadcom guides Q1 FY26 AI semiconductor revenue to roughly double year-on-year.",
      "quote": "our AI revenue to double year-on-year to $8.2 billion",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "CFO guides Q1 consolidated gross margin down sequentially on higher AI mix.",
      "quote": "down approximately 100 basis points sequentially",
      "speaker": "Kirsten Spears",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Board raises quarterly dividend 10% to $0.65/share for FY26.",
      "quote": "an increase of 10% from the prior quarter",
      "speaker": "Kirsten Spears",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "commitment",
      "claim": "Total AI-related order backlog (XPUs, switches, DSPs, lasers) exceeds $73B for delivery over 18 months.",
      "quote": "total order on hand in excess of $73 billion today",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "product",
      "claim": "AI switch order backlog (Tomahawk 6) exceeds $10B.",
      "quote": "order backlog for AI switches exceeds $10 billion",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Broadcom secured a fifth XPU customer via a $1B order for late-2026 delivery.",
      "quote": "acquired a fifth XPU customer through a $1 billion order",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "competition",
      "claim": "Hock dismisses the idea that hyperscalers will bring XPU tooling fully in-house as overstated.",
      "quote": "this concept of customer tooling is an overblown hypothesis",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "risk",
      "claim": "Non-AI semiconductor demand described as stable, not yet in a sustainable recovery outside broadband.",
      "quote": "We don't see a sharp recovery that is sustainable yet",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "Management expects gross margin % to decline with AI/system mix but gross margin dollars and operating margin dollars to rise.",
      "quote": "gross margin dollars will go up, margins will go down",
      "speaker": "Kirsten Spears",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Share repurchase authorization extended, $7.5B remaining capacity through end of CY2026.",
      "quote": "$7.5 billion remains, through the end of calendar year 2026",
      "speaker": "Kirsten Spears",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 outlook: non-AI semiconductor revenue expected to be stable while AI drives growth.",
      "quote": "non-AI semiconductor revenue to be stable",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Hock explicitly declines to confirm or deny that the $1B fifth-customer order is OpenAI.",
      "quote": "I did not answer it and I'm not answering it either",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Silicon photonics acknowledged as a future direction but not near-term ready for deployment.",
      "quote": "We're not quite there yet",
      "speaker": "Hock Tan",
      "date": "2025-12-11",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "topic": "guidance",
      "claim": "Q2 FY26 consolidated revenue guided to approximately $22 billion.",
      "quote": "consolidated revenue of approximately $22 billion",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "Q2 AI semiconductor revenue growth guided to accelerate sharply to 140% y/y.",
      "quote": "accelerate very sharply to 140% year-on-year",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "Google demand cited as strong for the 7th-gen Ironwood TPU, expected to strengthen further from 2027.",
      "quote": "strong demand for the seventh-generation Ironwood TPU",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "Anthropic 2027 TPU compute demand expected to surge past 3 gigawatts.",
      "quote": "surge in excess of 3 gigawatts of compute",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "competition",
      "claim": "Hock pushes back on analyst reports questioning Meta's MTIA custom accelerator roadmap.",
      "quote": "Meta's custom accelerator MTIA road map is alive and well",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "OpenAI named as sixth XPU customer, expected to deploy first-gen XPU at 1GW+ scale in 2027.",
      "quote": "OpenAI deploying in volume their first-generation XPU",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "Broadcom states it has fully secured key component supply (wafers, HBM, substrate) for '26 through '28.",
      "quote": "secured capacity of these components for '26 through '28",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "Broadcom states line of sight to AI chip revenue exceeding $100B in 2027.",
      "quote": "in excess of $100 billion in 2027",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "product",
      "claim": "AI networking revenue grew 60% y/y in Q1, about a third of total AI revenue.",
      "quote": "Q1 AI networking revenue grew 60% year-on-year",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "risk",
      "claim": "Management positions infrastructure software (VMware/VCF) as insulated from AI-driven disruption.",
      "quote": "our Infrastructure Software is not disrupted by AI",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Board authorizes an additional $10B for the share repurchase program through end of CY2026.",
      "quote": "an additional $10 billion for our share repurchase program",
      "speaker": "Kirsten Spears",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Q1 capital return: $10.9B returned to shareholders via dividends and buybacks.",
      "quote": "returned $10.9 billion to shareholders",
      "speaker": "Kirsten Spears",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "competition",
      "claim": "Hock states Broadcom will not see meaningful COT (customer-owned tooling) competition for years.",
      "quote": "we will not see competition in COT for many years to come",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "Hock forcefully rejects the premise that rack/system sales will structurally compress AI gross margin.",
      "quote": "Hate to tell you that you must be a bit hallucinating",
      "speaker": "Hock Tan",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "Charlie Kawwas notes multiyear supply security is built on deep multiyear custom-silicon engagements with 6 customers.",
      "quote": "we build custom silicon for 6 customers",
      "speaker": "Charlie Kawwas",
      "date": "2026-03-04",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "Q3 FY26 AI semiconductor revenue guided to accelerate to $16B, up over 200% y/y.",
      "quote": "AI semiconductor revenue to accelerate to $16 billion",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "guidance",
      "claim": "FY26 AI semiconductor revenue guided to $56 billion, up ~180% from FY25.",
      "quote": "AI semiconductor revenue of $56 billion",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "guidance",
      "claim": "Broadcom reiterates FY27 AI semiconductor revenue guidance in excess of $100 billion.",
      "quote": "in excess of $100 billion",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "Google long-term agreement (announced April) covers multiple generations of TPUs and AI networking.",
      "quote": "agreement to develop and supply multiple generations",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "Anthropic agreement adds access to another 5 gigawatts of next-gen TPU compute starting 2027.",
      "quote": "another 5 gigawatts of next-generation TPU-based compute",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "OpenAI has a contractual commitment to deploy 1.3 gigawatts in 2027 within the larger 10GW-by-2029 deal.",
      "quote": "contractual commitment to deploy 1.3 gigawatts in 2027",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "Meta agreement calls for deploying 3 gigawatts of MTIA capacity through end of 2028.",
      "quote": "expect to deploy 3 gigawatts through the end of 2028",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "product",
      "claim": "Broadcom positions its CPO/optical DSP and laser technology as the de facto industry standard.",
      "quote": "we are the de facto standard in the industry",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "New AI XPV platform with Apollo/Blackstone targets deploying over 20 gigawatts of compute capacity through 2028.",
      "quote": "more than 20 gigawatts of compute capacity through 2028",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "First tranche of the XPV financing platform valued at $35 billion, being launched by Apollo.",
      "quote": "The first tranche of this platform valued at $35 billion",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "Management frames Q3 gross margin decline to ~74% as mix-driven, not a structural semiconductor margin change.",
      "quote": "does not represent a structural change",
      "speaker": "Kirsten Spears",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "Management recommends modeling semiconductor and infrastructure software margins separately going forward.",
      "quote": "semiconductor and infrastructure software margins separately",
      "speaker": "Kirsten Spears",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "Non-AI semiconductor bookings above $6B cited as a sign of a fuller cyclical recovery underway.",
      "quote": "on the path towards a full cyclical recovery",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "product",
      "claim": "VCF 9.1 adds heterogeneous compute support spanning AMD, Intel and NVIDIA platforms.",
      "quote": "compute support across GPUs and CPU architectures",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "Hock says supply-chain visibility has extended out to 2028, up from 2027 three months earlier.",
      "quote": "Our visibility runs all the way to 2028 right now",
      "speaker": "Hock Tan",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "CFO Kirsten Spears announced as retiring June 12, with Amie Thuener joining as incoming CFO.",
      "quote": "Kirsten will be retiring June 12",
      "speaker": "Ji Yoo",
      "date": "2026-06-03",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    }
  ],
  "qa_flags": [
    {
      "question": "whether the $1 billion fifth-customer order is indeed OpenAI",
      "response_pattern": "explicitly declines to confirm or deny ('I did not answer it and I'm not answering it either')",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "question": "whether the OpenAI 10-gigawatt announcement is a binding agreement similar to NVIDIA/AMD deals",
      "response_pattern": "does not directly confirm or deny bindingness; reframes as an 'agreement and alignment' for 2027-2029 and downplays 2026 contribution",
      "file": "AVGO_Q4_2025_Earnings_Call_20251211.md"
    },
    {
      "question": "how much of the Anthropic deal dollar value is chips versus racks",
      "response_pattern": "explicitly declines to break out the split, redirects to 'we're good on our dollars and margin'",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "question": "whether the OpenAI ramp (10GW by 2029) implies a sharp inflection in 2028",
      "response_pattern": "long strategic narrative response about customer commitment and visibility without directly confirming or quantifying the 2028 inflection",
      "file": "AVGO_Q1_2026_Earnings_Call_20260304.md"
    },
    {
      "question": "the total dollar value of the long-term Google TPU/networking agreement and whether it is fixed or share-based",
      "response_pattern": "declines to give a number, repeats vague superlative language ('very, very substantial amount of dollars') without specifics",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    },
    {
      "question": "whether the rack-versus-chip revenue mix question is now fully clarified",
      "response_pattern": "curt repeated denial ('No racks... We're in the chip business only... Only chips') that reads as a shift from the prior quarter's 'system sale' / rack-selling language",
      "file": "AVGO_Q2_2026_Earnings_Call_20260603.md"
    }
  ]
}
```

---

## judgment.json 全文

```json
{
  "meta": {
    "ticker": "AVGO",
    "date": "2026-09-05",
    "schema": "v15.0",
    "company_name": "Broadcom Inc."
  },
  "oneliner": "客製 AI ASIC 龍頭＋AI 網通＋VMware 三引擎；Q3 FY26 AI 營收 $16.7B（+221%）、FY27／FY28 AI 指引 $115B／$230B；財報後回檔至 FY27 本益比 18.5x、PEG 0.31；惟 Google 刻意四夥伴分單、MediaTek 推論晶片 Q4 量產，護城河趨勢↓；裁決進場｜衛星、上限 3%。",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": null,
    "confidence": "高",
    "fingerprint": "FCF 利潤率 46%、非 GAAP 營業利益率 67.9%、資本支出占營收 <2%、營收 YoY +86%：輕資產設計＋高黏性軟體的複利體質，惟成長由 AI 資本週期驅動帶循環色彩"
  },
  "thesis": {
    "headline": "六客戶客製 XPU 平台把雲端自研晶片的利潤池搬到 Broadcom 手上；風險不在需求而在 Google 分單與 2028 後資本週期",
    "holding_period": {
      "horizon": "中期 2-5 年（長期持有信心低，護城河趨勢↓且 Max DD 🔴）",
      "driver": "FY27／FY28 AI 營收指引兌現度＋Google 份額路徑＋半導體分部營業利益率",
      "signal_vs_noise": "訊號＝年度 AI 營收兌現度、Google 世代設計權歸屬、分部營業利益率趨勢；噪音＝單季指引與街頭差 <1%、單季合併毛利率 mix 波動"
    },
    "H": [
      {
        "id": "H1",
        "text": "客製 AI ASIC 設計領導地位維持：六大客戶群持續放量，客戶分散化抵銷 Google 單一客戶份額稀釋",
        "2y": "FY27 AI 半導體營收落在 $115B 指引 ±10%；OpenAI 2027 出貨 ≥1.3GW 合約量",
        "5y": "FY28 AI 營收 ≥$185B（指引 $230B 打八折）；Anthropic／OpenAI／Meta 合計占 AI 營收 ≥40%",
        "10y": "客製 ASIC 對 merchant GPU 出貨份額維持 30% 以上（產業層級），Broadcom 設計夥伴份額 ≥50%",
        "threshold": "TTM AI 營收落後指引路徑逾 10% 連 2 季→削弱；連 3 季逾 10%→反轉",
        "source": "公司財報／法說（每季）＋Counterpoint／TrendForce 份額研究（每年）",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉；5Y 假設連 4 季 ≥5% 削弱"
      },
      {
        "id": "H2",
        "text": "VMware 訂閱制轉換完成後，基礎設施軟體以低雙位數成長提供跨週期現金流",
        "2y": "基礎設施軟體營收 YoY ≥10%（Q3 FY26 $8.75B、+29%）；VCF ARR 年增不跌破 12%",
        "5y": "軟體占總營收 20-30%、分部營業利益率維持 70% 以上；VCF 成為企業私有 AI 推論控制平面",
        "10y": "軟體現金流足以覆蓋全部股息＋淨回購，成為半導體循環的緩衝",
        "threshold": "ARR 年增連 2 季 <10%→削弱；EU／美反壟斷裁定強制改授權模式→反轉",
        "source": "公司財報分部數字（每季）＋歐盟／DOJ 公告",
        "drift_rule": "2Y 假設連 2 季偏離 ≥5% 削弱；反壟斷裁定屬離散事件，命中即重審 H2"
      },
      {
        "id": "H3",
        "text": "市場以複利股而非循環股給倍數：FY+2 本益比維持 15-25x 區間，PEG 不系統性偏離 1 以下",
        "2y": "FY+2 本益比不連 4 季 <14x 且無基本面惡化；共識 FY28 EPS 不連續下修",
        "5y": "5 年後估值倍數 normalize 至 18-22x 仍反映護城河與成長持續期",
        "10y": "—",
        "threshold": "FY+2 本益比連 4 季 <14x 且非 EPS 上修驅動→削弱（市場已切換循環股框架）",
        "source": "本站共識快照 data/eps-estimates（每兩週）",
        "drift_rule": "連 4 季 FY+2 本益比偏離 15-25x 區間逾 10%→削弱"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "Google 端份額稀釋快於預期：Google 刻意建四夥伴供應鏈（Broadcom 訓練 Sunfish、MediaTek 推論 Zebrafish 成本低 20-30%、Marvell 2026-07-29 簽約、Intel 處理器），MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場、Zebrafish Q4 2026 量產。反向證據：Broadcom 與 Google 多世代 TPU 長約、Counterpoint 估 2027 仍持 60% 設計夥伴份額",
        "h_ref": "H1",
        "clock": "🔥",
        "threshold": "Google 份額較 95→80→65 路徑低逾 10pp，或 2027 年度 <75%；Broadcom 未取得 TPU v9／v10 訓練晶片設計權",
        "evidence_refs": [
          "competitive_share_entrants#2",
          "competitive_share_entrants#3",
          "customer_second_source#0",
          "customer_second_source#1",
          "customer_second_source#2",
          "substitute_technology#1"
        ]
      },
      {
        "id": "R2",
        "text": "AI 客戶信用與資本週期：OpenAI 2026-05 無法關閉約 $18B 融資、Broadcom 被報導只願出資第一階段並放寬對等出資要求；XPV 平台（Apollo／Blackstone）首批 $35B、20GW 全量名目上看 $370B；四大雲端 AI 資本支出若 2028 進入消化期，backlog 兌現度不如指引",
        "h_ref": "H1／H3",
        "clock": "🔥",
        "threshold": "OpenAI／Anthropic 實際出貨 GW 低於公司自身指引逾 20%；XPV 信用展望連 2 季負向",
        "evidence_refs": [
          "customer_concentration_credit#3",
          "customer_concentration_credit#4",
          "customer_concentration_credit#0",
          "customer_concentration_credit#2"
        ]
      },
      {
        "id": "R3",
        "text": "VMware 監管與通路：歐盟 2026-02 正式反壟斷調查、Broadcom 敗訴文件請求案、美國另開授權調查；2026-01 終止 400 餘家 VCSP 夥伴合約引發被迫遷移；中國以國安為由要求移除 VMware 並禁用 Broadcom 資安方案",
        "h_ref": "H2",
        "clock": "🐢",
        "threshold": "歐盟發異議書或裁定強制改授權模式；ARR 年增連 2 季 <10%",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "regulatory_antitrust#1",
          "regulatory_antitrust#2",
          "channel_business_model_shift#1",
          "regulatory_antitrust#4",
          "regulatory_antitrust#5"
        ]
      }
    ],
    "single_thing": {
      "description": "Google 公告下一代主力訓練 TPU（v9 Triggerfish 或 v10）主設計權授予 MediaTek 或其他夥伴，Broadcom 失去 Google 訓練晶片主設計權",
      "why_fatal": "Google 是 AI 營收最大單一來源且訓練晶片是最高價值環節；失去主設計權＝護城河等級由 A 直接重審至 B 以下，且觸發護城河趨勢↓＋等級 ≤B 的強制迴避",
      "if_happens": "清倉級：不等財報，先減至 0 並重跑 DD；市場會把估值框架從複利股切到循環代工股（12-15x）",
      "how_monitor": "Google 法說／TSMC 2nm 投片報導／TrendForce、Counterpoint 設計夥伴研究（每季），公司法說對「多世代協議」措辭變化",
      "probability": "12-24 個月內 20-25%（多世代長約至 2031 為反向錨；但 Google 已明示要每個環節都有合格替代者）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "產業物理供需＝shortage（ID：AI Accelerator Demand，as-of 2026-09-05；機械選出的 primary 為 Hyperscaler 雲端三巨頭 as-of 2026-05-05 亦為 shortage／Phase II，惟前者較貼題，建議覆核 primary）。Phase II 已經自身位置閘交叉驗證：AI 訂單 backlog >$73B（來源：摘要）、供給能見度延至 2028、CoWoS 缺口 20%→10%（供給正在追上，屬擴張後段而非過熱頂部）",
    "bargaining": {
      "up": "對上游弱：先進製程與 CoWoS 近乎單一來源 TSMC（先進節點 >90%），NVIDIA 已預訂 2026-27 過半 CoWoS-L；Broadcom 稱 26-28 年晶圓／HBM／基板產能已鎖定（來源：摘要），但雷射與 PCB 缺口蔓延",
      "down": "對下游中等偏弱：前五大終端客戶占營收 45%（10-Q，2026-05-03；前一年 40%）、經銷商單一客戶 42%；Google 明示以多夥伴取得議價槓桿；反向：多年期承諾（Google 至 2031、OpenAI 10GW 至 2029、Meta 3GW 至 2028）",
      "geo": "生產 100% 依賴台灣先進節點與封裝；美國 Section 232 對高階半導體課 25% 關稅（產品分類決定是否涵蓋）；中國禁 Broadcom 資安方案、要求移除 VMware；美國禁中國光收發器可能壓 DSP 需求"
    },
    "profit_pool_dir": "流入：自研 ASIC 把原屬 merchant GPU 的利潤池分一塊給設計夥伴（ID 供給側：AVGO 客製加速器 +140% YoY、ASIC 出貨 2024-27 三倍）；但 Google 內部以多夥伴壓縮設計夥伴分潤，池在放大、單一夥伴份額在縮",
    "tam_table": [
      {
        "segment": "客製 AI 加速器（XPU）",
        "tam_now": "2027E 約 $80B（MediaTek 引用之客製 AI 晶片市場估計）",
        "tam_5y": "證據包未涵蓋（公司 SAM 口徑不在本輪證據包）",
        "sam": "六客戶多年期承諾：OpenAI 10GW、Anthropic 3.5GW＋5GW、Meta 3GW、Google 多世代",
        "penetration": "設計夥伴份額約 60%（Counterpoint，2027E）",
        "cagr": "FY26 $58B→FY27 $115B→FY28 $230B（公司指引，含網通）",
        "position": "設計＋IP 平台（SerDes／CoWoS 整合），客戶擁有架構",
        "pool_shift": "5 年前 ~0→現為半導體分部主體；流向設計夥伴與雲端自身",
        "ceiling": "天花板＝雲端資本支出 ROI 兌現；被替代路徑＝客戶自有工具鏈（COT）與 MediaTek 低成本設計"
      },
      {
        "segment": "AI 網通（Tomahawk 6／DSP／光學）",
        "tam_now": "Q1 FY26 約占 AI 營收三分之一、YoY +60%（來源：摘要）",
        "tam_5y": "證據包未涵蓋",
        "sam": "AI 交換器 backlog >$10B（來源：摘要）",
        "penetration": "自稱 CPO／DSP 事實標準（來源：摘要，未第三方驗證）",
        "cagr": "隨 XPU 集群同步；矽光子「尚未到位」",
        "position": "Ethernet 陣營標準制定者",
        "pool_shift": "自 InfiniBand 向 Ethernet 流入",
        "ceiling": "NVIDIA Spectrum-X 與客戶自研交換晶片"
      },
      {
        "segment": "基礎設施軟體（VMware VCF）",
        "tam_now": "Q3 FY26 $8.75B（+29% YoY）",
        "tam_5y": "證據包未涵蓋",
        "sam": "前 10,000 大客戶逾 90% 已轉訂閱制 VCF",
        "penetration": "已轉換帳戶為主，成長轉為 ARR 擴張",
        "cagr": "管理層：低雙位數；VCF ARR +17%（2026-06 報導口徑）",
        "position": "私有雲控制平面，訂閱制每核心計價",
        "pool_shift": "自通路夥伴與舊授權模式流向 Broadcom 直銷",
        "ceiling": "歐盟／美國反壟斷、客戶遷移至 Nutanix／公有雲"
      },
      {
        "segment": "非 AI 半導體（寬頻／無線／儲存／企業網通）",
        "tam_now": "Q1 FY26 $4.1B 季度、YoY 持平",
        "tam_5y": "證據包未涵蓋",
        "sam": "Q2 FY26 訂單 >$6B、管理層稱循環復甦中（來源：摘要）",
        "penetration": "成熟寡占",
        "cagr": "低個位數，循環性",
        "position": "多品類寡占者",
        "pool_shift": "持平",
        "ceiling": "無線客戶集中（Apple）與消費電子週期"
      }
    ]
  },
  "moat": {
    "execution": 9.0,
    "pricing": 8.0,
    "combined": 8.5,
    "grade": "A",
    "score": 8.5,
    "trend": "↓",
    "trend_evidence": "12 個月內 sourced：Google 2026-08-20 報導刻意組四夥伴供應鏈、MediaTek Zebrafish Q4 2026 量產且成本低 20-30%、Marvell 2026-07-29 與 Google 簽約。執行面擴大（六客戶、供給鎖定至 2028、AI 營收 +221%），定價面縮減（最大客戶明示要每環節有替代者）；取對論點更關鍵的定價／份額維度→↓。閘 A：最大客戶份額路徑 95→80→65 下滑（sourced）→不得標↑。三分解：方向未受損（設計夥伴份額仍 ~60%）、速度放緩（Google 新增量分給對手）、失守範圍＝Google 推論晶片。攻擊者資本量級：MediaTek 資料中心營收 2026E >$2B，約為 AVGO AI 營收 3%，屬點對點而非生態級；但 Google 本身資本無上限。記帳紀律：負面證據只記在趨勢，等級維持 A 不重複扣",
    "spread_table": [
      {
        "metric": "營業利益率（GAAP TTM）",
        "self": 44.06,
        "peer": "MRVL 16.41（最直接客製 ASIC 對手）",
        "spread_pp": 27.65,
        "trend": "MRVL 三年趨勢證據包未涵蓋；AVGO 半導體分部營業利益率 +440bp YoY→視為擴大",
        "note": "NVDA 64.02 為 merchant GPU 不同層級，不作等級門檻對照"
      },
      {
        "metric": "FCF 利潤率（TTM）",
        "self": 43.41,
        "peer": "MRVL 19.06；AMD 20.34；QCOM 23.64",
        "spread_pp": 24.35,
        "trend": "擴大（AVGO Q3 FCF 占營收 46.2%，QoQ 持平於高檔）",
        "note": "來源 peer_financials"
      },
      {
        "metric": "毛利率（GAAP TTM）",
        "self": 68.28,
        "peer": "NVDA 74.15；MRVL 51.5；AMD 53.2",
        "spread_pp": 16.78,
        "trend": "合併毛利率因 XPU mix 下滑（管理層：金額升、比率降，來源：摘要）；同業擴張而本標的下滑→閘二對照：屬 mix 非結構，記管理層承諾列入監測",
        "note": "R&D 強度 15.89% 低於 MRVL 25.46／AMD 22.74，反映規模攤薄"
      }
    ],
    "threats": [
      {
        "level": "🔴 生態攻擊",
        "text": "Google 四夥伴供應鏈：MediaTek 推論 Zebrafish（Q4 2026 量產、成本低 20-30%）、Marvell 商業協議（2026-07-29）、Intel 處理器；Google 藉此取得定價與產能槓桿",
        "p": "60-70%（份額稀釋已在發生）",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      },
      {
        "level": "🔴 生態攻擊",
        "text": "MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場（$80B 估計），2026 資料中心營收 >$2B",
        "p": "50%",
        "evidence_refs": [
          "competitive_share_entrants#2"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "六大客戶各自投資內部設計能力，關係「深而黏但非永久」；風險因子明列客戶可能改採自有工具鏈（COT）或租賃模式",
        "p": "3-5 年 30%",
        "evidence_refs": [
          "customer_second_source#2",
          "customer_concentration_credit#2",
          "substitute_technology#1"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "VMware 資安事件（Aria Operations 零日遭中國國家背景組織利用；Clop 經 Oracle EBS 零日入侵 Broadcom 內部）削弱軟體信任",
        "p": "20%（信任型流失）",
        "evidence_refs": [
          "major_events#1",
          "major_events#2",
          "product_recall_warning#0",
          "product_recall_warning#1"
        ]
      }
    ],
    "competitors": [
      {
        "name": "MRVL（Marvell）",
        "rev_growth": "證據包未涵蓋",
        "gm": 51.5,
        "om": 16.41,
        "rd_intensity": 25.46,
        "fcf_margin": 19.06,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "Trainium base die ~55-60% 份額（ID 供給側），2026-07-29 取得 Google 客製協議（推論／周邊）；營業利益率不到 AVGO 四成，R&D 強度高＝以投入換份額，經濟體質弱但攻擊意願強"
      },
      {
        "name": "NVDA（NVIDIA）",
        "rev_growth": "證據包未涵蓋",
        "gm": 74.15,
        "om": 64.02,
        "rd_intensity": 8.22,
        "fcf_margin": 46.97,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "merchant GPU 主供，預訂 2026-27 過半 CoWoS-L；與 AVGO 爭封裝產能而非設計案；Rubin 若 TCO 大幅領先會削弱自研 ASIC 經濟性（ID 可證偽條件）"
      },
      {
        "name": "AMD",
        "rev_growth": "證據包未涵蓋",
        "gm": 53.2,
        "om": 15.71,
        "rd_intensity": 22.74,
        "fcf_margin": 20.34,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "雙來源 GPU；市場傳聞洽談 Google v10，屬未證傳聞"
      },
      {
        "name": "MediaTek",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "證據包未涵蓋",
        "strategy_note": "Google 推論 TPU Zebrafish Q4 2026 量產、成本低 20-30%；2027 目標 15-20% 份額。財務數字不在 peer_financials，體質判斷留待補軸"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率×低周轉（VMware 商譽與無形資產墊高投入資本；剔除收購無形資產後屬高利益率×高周轉）",
      "checkpoints": [
        {
          "name": "需求基礎值",
          "light": "🟢",
          "evidence": "需要型：雲端算力受限（ID：Azure $80B backlog 受電力限、GCP RPO >$70B）；Broadcom AI backlog >$73B、能見度至 2028（來源：摘要）。惟急迫≠持久：需求是 ROI 兌現的函數",
          "proxy": "多年期承諾 GW 數（OpenAI 10GW／Anthropic 8.5GW／Meta 3GW）"
        },
        {
          "name": "決策層級",
          "light": "🟡",
          "evidence": "客戶在架構層決策（自有架構＋Broadcom 設計平台），切換需 18-24 個月 tape-out 週期；但 Google 已示範同架構下多夥伴分單，替代性在「世代」層級而非「產品」層級",
          "proxy": "各客戶世代設計權歸屬（v8 Sunfish／Zebrafish 分拆）"
        },
        {
          "name": "價值鏈分配",
          "light": "🟡",
          "evidence": "利益留在 Broadcom（非 GAAP 營業利益率 67.9%、半導體分部 +440bp YoY）；但買方集中（前五大 45%、單一經銷商 42%）且客戶自建能力上升，Google 明示以替代者取得議價槓桿",
          "proxy": "半導體分部營業利益率、前五大集中度"
        },
        {
          "name": "社會容忍度",
          "light": "🟡",
          "evidence": "半導體端低敏感；軟體端高敏感：VMware 漲價已引來歐盟正式調查、美國授權調查、CISPE 投訴與中國移除令；經濟上限與政治上限已相交",
          "proxy": "歐盟程序階段（調查→異議書→裁定）"
        }
      ],
      "roiic": 80,
      "reinvest_rate": 6,
      "endo_ceiling": 5.0,
      "formula_note": "ROIIC(3Y) 代理≈ΔNOPAT÷Δ投入資本：非 GAAP 營業利益年化自 FY23 約 $22B 升至 Q3 FY26 年化 $80B（Δ≈$58B），Δ投入資本以 VMware $69B＋有機約 $3B 計≈$72B→約 80%。再投資率＝(資本支出−折舊攤銷＋ΔWC＋收購淨額)÷NOPAT：年化資本支出約 $2.1B 對 NOPAT 約 $65B≈3%，加營運資金約 6%（收購攤銷不計）。內生天花板≈80%×6%≈5%。Base EPS CAGR 15.4% 超出天花板⚠→Bear 機率下限 30%；缺口歸因＝客戶承擔產能資本的新 S 曲線（XPU backlog sourced）＋營業槓桿，非 re-rate"
    }
  },
  "growth": {
    "runway_years": "5-7 年（AI 營收 FY26 $58B→FY28 $230B 指引後，2029 起增速取決於雲端資本支出第二輪；非 AI 與軟體提供低雙位數底盤）",
    "runway_post_y5": "🟡",
    "seven_questions": [
      "①結構性或週期反彈：結構性（雲端自研 ASIC 滲透 25-30% 且升）疊加資本週期（capex $380B+ ROI 未證）——兩者同時為真",
      "②資本投入：極低，資本支出占營收 <2%，產能資本由 TSMC 與客戶承擔",
      "③增量 ROIC >資金成本：是，代理 ROIIC 約 80%",
      "④成長變現金流或被吃掉：變現金流，Q3 FCF $13.7B 占營收 46%；但 XPV 表外平台把部分資本承諾移到平台",
      "⑤競爭者是否被吸引：是——MediaTek、Marvell、Intel 已進 Google 供應鏈，這是最弱的一題",
      "⑥股價反映多少期待：FY27 本益比 18.5x、PEG 0.31，反映的是「成長會在 2028 後急降」而非「指引兌現」",
      "⑦成長率下修估值撐得住嗎：成長降至 15% 給 20x 仍有正報酬；降至 5% 給 12x 則 −50%"
    ],
    "segments": [
      {
        "name": "AI 半導體（XPU＋網通）",
        "fy0": "FY26E $58B（指引，+186%）",
        "driver": "量：GW 部署（OpenAI 1.3GW 2027、Anthropic 3GW+5GW、Meta 3GW）；價：系統級含量提升",
        "fy1e": "FY27 $115B（指引；本檔 Base 取 100%）",
        "fy2e": "FY28 $230B 指引；本檔 Base 取 $185B（八折）",
        "fy3e": "FY29 +15-20%",
        "om_path": "半導體分部 61%→58-60%（mix）",
        "eps_contrib_pct": "約 75%"
      },
      {
        "name": "基礎設施軟體",
        "fy0": "Q3 FY26 $8.75B（+29%）",
        "driver": "訂閱制轉換完成後 ARR 擴張（VCF ARR +17%，2026-06 口徑）",
        "fy1e": "低雙位數",
        "fy2e": "低雙位數",
        "fy3e": "高個位數至低雙位數",
        "om_path": "70%+ 維持",
        "eps_contrib_pct": "約 20%"
      },
      {
        "name": "非 AI 半導體",
        "fy0": "Q1 FY26 $4.1B 季度、持平",
        "driver": "循環復甦（Q2 訂單 >$6B，來源：摘要）",
        "fy1e": "低個位數至中個位數",
        "fy2e": "低個位數",
        "fy3e": "低個位數",
        "om_path": "持平",
        "eps_contrib_pct": "約 5%"
      }
    ],
    "decay_signals": [
      "合併毛利率連季 YoY 下滑（XPU／系統 mix，管理層稱非結構性，來源：摘要）——亮燈但歸因 mix",
      "核心客戶份額縮減（Google 份額路徑 95→80→65，MediaTek／Marvell 進場）——亮燈",
      "SBC／營收 6.8%（Q3 FY26）>5% 但季比下降（9.4%→6.8%）——不亮燈",
      "其餘七項未亮燈（FCF／NI、TAM、產業倍數、維持性資本支出）"
    ],
    "trap_rating": "🟡（2 訊號：合併毛利率下滑屬 mix、Google 份額稀釋屬真實侵蝕）"
  },
  "quality": {
    "three_year": [
      {
        "metric": "FCF 利潤率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "43.41（TTM 至 2026-04）／Q3 FY26 46.2",
        "peer_median": "MRVL 19.06／AMD 20.34／QCOM 23.64／NVDA 46.97",
        "assessment": "頂尖，僅次 NVDA"
      },
      {
        "metric": "營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "GAAP 44.06（TTM）／Q3 FY26 GAAP 53.9、非 GAAP 67.9",
        "peer_median": "MRVL 16.41／AMD 15.71／QCOM 23.28／NVDA 64.02",
        "assessment": "Q3 非 GAAP 營業利益率 QoQ +60bp；營收 YoY +86% 對營業利益 YoY 更高＝營業槓桿為正（發散 <0）"
      },
      {
        "metric": "SBC／營收",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "Q3 FY26 6.8%（Q2 9.4%）",
        "peer_median": "證據包未涵蓋",
        "assessment": "金額持平 $2.0B／季，比率因營收放大而降"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利潤率",
        "value": "非 GAAP 營業利益率 67.9%（Q3 FY26）；GAAP 53.9%",
        "note": "GAAP 與非 GAAP 差距主要為收購無形資產攤銷與 SBC"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本明細不在本輪數字包）",
        "note": "VMware $69B 商譽／無形資產使帳面周轉率低；剔除後為高周轉輕資產"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO／CCC 三年逐年",
        "value": "證據包未涵蓋",
        "note": "10-Q 提及 AI 與無線客戶大單造成季度營收波動；營運資金結構須回補軸"
      }
    ],
    "buyback": {
      "authorization": "剩餘 $7.5B（至 2026 年底）＋2026-03 加碼 $10B（來源：摘要）",
      "q1_capital_return": "Q1 FY26 回饋股東 $10.9B（股息＋回購，來源：摘要）",
      "buyback_to_fcf": "Q1 回饋 $10.9B 對 Q1 FCF 證據包未涵蓋；以 Q3 FCF $13.7B 為尺，回饋比率約 60-80% 區間，未觸 >80% 警示",
      "avg_price_vs_now": "證據包未涵蓋",
      "eps_cagr_ex_buyback": "淨回購約 0.3%／年，對 EPS CAGR 貢獻 <1pp，剔除後差距遠低於 5pp 警示"
    },
    "lumpiness": {
      "fcf_5y": "證據包未涵蓋（僅有 Q2 $10.26B、Q3 $13.67B）",
      "maint_capex_method": "以季度資本支出 $532M 全數視為維持性（保守法）",
      "owner_earnings": "Q3 營運現金流 $14.2B − $0.53B ≈ $13.7B",
      "verdict": "🟢 正常（資本支出占 FCF <4%）"
    }
  },
  "governance": {
    "capalloc_grade": "A",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC（VMware $69B，2023-11）",
        "value": "基礎設施軟體 Q3 FY26 營收 $8.75B、分部營業利益率約 70%+→年化營業利益約 $25B÷$69B≈35%",
        "pass": true
      },
      {
        "item": "回購買入收益率",
        "value": "回購均價證據包未涵蓋；以現價 FY27 盈餘殖利率 5.4%（1÷18.5）近似 ≥ 10Y 殖利率＋2%",
        "pass": true
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 年化約 $8B 對市值約 $1.68T≈0.5%／年，加 $17.5B 回購額度後為淨減少",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "股息",
        "detail": "季配 $0.65（FY26 +10%，來源：摘要）；殖利率約 0.7%"
      },
      {
        "type": "回購",
        "detail": "剩餘 $7.5B＋新增 $10B 至 2026 年底（來源：摘要）"
      },
      {
        "type": "表外",
        "detail": "XPV 平台首批 $35B（Apollo）、目標 20GW 至 2028（來源：摘要）；自陳曝險 $29B、BofA 模型 $42B、全量名目 $370B（前份報告口徑）"
      }
    ],
    "sbc": {
      "pct_revenue": 6.8,
      "pct_gaap_oi": 12.7,
      "trend": "Q2 9.4%→Q3 6.8%（金額持平 $2.0-2.1B）",
      "note": "CFO 交接：Kirsten Spears 2026-06-12 退休、Amie Thuener 接任（來源：摘要）→ 2026-12-09 為新 CFO 首個完整季度複審點；內部人交易近 12 個月：證據包未涵蓋"
    }
  },
  "valuation": {
    "tier": "Turnkey ASIC／IP 平台＋基礎設施軟體混合；同 tier 直接 peer＝MRVL，NVDA 為 merchant GPU 不同 tier，⚠ 無 ideal peer group，溢折價獨立推導",
    "peers": [
      {
        "name": "MRVL",
        "fwd_pe": "證據包未涵蓋",
        "note": "營業利益率 16.41 vs AVGO 44.06，倍數不可比"
      },
      {
        "name": "NVDA",
        "fwd_pe": "證據包未涵蓋",
        "note": "不同 tier"
      },
      {
        "name": "AMD",
        "fwd_pe": "證據包未涵蓋",
        "note": "—"
      },
      {
        "name": "QCOM",
        "fwd_pe": "證據包未涵蓋",
        "note": "—"
      }
    ],
    "fwd_pe": 30.77,
    "peg": 0.51,
    "percentile_5y": 24.4,
    "val_light": "🟢",
    "val_light_derivation": "五年分位：trailing 本益比 45.48 對 4 個年度樣本點高 135.24／低 16.57→(45.48−16.57)÷(135.24−16.57)＝24.4%（樣本僅 4 點，標「年度樣本」）；短窗 fwd 本益比 30.77 位於 2026-05 起 9 份快照最低（0 分位，非五年）。PEG：FY26 基準 30.77÷60.6%（FY26→FY28 共識 2 年 CAGR）＝0.51；FY27 基準 18.51÷60.6%＝0.31。分位 <30% 且 PEG <1.0→兩尺皆 🟢，取較嚴仍 🟢。分母爭議：FY27 共識 19.33 受 $73B backlog 覆蓋，非本章爭點；FY28 起才是",
    "targets": {
      "short_1y": {
        "eps": 19.33,
        "pe": 22,
        "price": 425,
        "upside_pct": 18.8,
        "basis": "FY27 共識 EPS × 合理 22x（護城河 A 但趨勢↓折價）"
      },
      "mid_2y": {
        "eps": 26.0,
        "pe": 22,
        "price": 572,
        "upside_pct": 59.8,
        "basis": "本檔 Base FY28 EPS 26.0（指引八折）× 22x"
      },
      "five_y": {
        "eps": 39.5,
        "pe": 20,
        "price": 790,
        "upside_pct": 120.7,
        "basis": "Base 情境 FY31 EPS × 長期 20x"
      },
      "bear_anchor": {
        "eps": 17.4,
        "pe": 15,
        "price": 261,
        "downside_pct": -27.0,
        "basis": "Bear EPS＝FY27 共識×0.9；Bear 本益比＝成長降至 10% 情境 15x；下行 27% >15% 正常可用"
      },
      "sell_side": "57 位分析師目標價均值 $520（過去 3 個月上修 9.3%，買進評等 84%）；財報後 BMO $575、Cantor $600、Raymond James $475。現價低於均值 31%→支持本裁決；全距 max／min 證據包未涵蓋"
    },
    "upside_short_pct": 18.8,
    "upside_mid_pct": 59.8
  },
  "trap_analysis": {
    "pattern": "最可能的陷阱模式＝「週期頂部的低 PEG」：AI 資本週期在 2028 見頂，FY28 EPS 30 成為峰值盈餘，低倍數反映的是市場已把它當循環股",
    "evidence_against": "Q3 FY26 營收 +86%、AI 營收 +221%、FCF $13.7B（46%）、非 GAAP 營業利益率 67.9% 續升；backlog >$73B 覆蓋 18 個月；共識 FY28 EPS 近一週上修 13.5% 至 30.0、90 天 +17%——盈餘與現金同步、且共識仍在追指引而非下修",
    "evidence_for": "前五大客戶 45%、單一經銷商 42%；Google 刻意分單、MediaTek Q4 量產；OpenAI 融資 $18B 未關閉、XPV 名目 $370B；合併毛利率因 mix 下滑——這些都是「峰值盈餘品質」的典型前兆",
    "bear_case": "空頭最強一擊（18 個月 −30%+）：2027 中雲端下修 2028 資本支出＋Google 公布 v9 訓練晶片交 MediaTek→FY28 共識自 30 砍至 22、倍數自 18.5x 壓至 12x→股價 $260（−27%）至 $230（−36%）。監測：Google 世代設計權公告、四大雲端 capex 指引、半導體分部營業利益率",
    "monitor": [
      "共識 FY28 EPS 方向（連 2 次下修＝陷阱正在發生）",
      "半導體分部營業利益率跌破 55% 連 2 季",
      "Google 份額路徑與 v9／v10 設計權",
      "XPV 平台信用展望與 OpenAI 融資關閉進度"
    ],
    "verdict": "🟢",
    "label": "🟢 非陷阱（2 個衰退訊號皆有 sourced 反駁：mix 與份額稀釋被絕對金額 +221% 覆蓋；觀察期指標已列）"
  },
  "appendix_a": {
    "signal": "A+",
    "moat_score": 8.5,
    "growth_durability": 8.0,
    "quality_score": 8.3,
    "ai_risk": "🟢",
    "long_term_confidence": "低",
    "val": "🟢",
    "ma": "✅",
    "fpe_fy2": 18.51,
    "pct_5y": 24.4,
    "peg_fy2": 0.31,
    "upside_short_pct": 18.8,
    "upside_mid_pct": 59.8,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "A+"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY26": 11.63,
      "FY27": 19.33,
      "FY28": 30.0
    },
    "fy_end_month": 11,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-12-09",
      "type": "guidance",
      "event": "Q4 FY26 財報＋FY27 展望更新（新 CFO 首個完整季度）",
      "impact": "高",
      "watch": "Q4 AI 營收 ≥$21.7B 指引兌現；FY27 $115B 是否維持或上修；半導體分部營業利益率"
    },
    {
      "date": "2026-12-31",
      "date_precision": "quarter",
      "type": "product",
      "event": "MediaTek Google 推論 TPU Zebrafish 量產",
      "impact": "高",
      "watch": "量產規模與 Google 推論採購分配；Broadcom 對 Google 出貨是否同步下修"
    },
    {
      "date": "2027-03-31",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "歐盟 VMware 反壟斷調查程序進展（異議書與否）",
      "impact": "中",
      "watch": "若發異議書→軟體 ARR 與毛利率下修風險；程序階梯對應減碼"
    },
    {
      "date": "2027-06-30",
      "date_precision": "quarter",
      "type": "product",
      "event": "OpenAI Jalapeño 首代 XPU 2027 出貨 1.3GW 合約量兌現",
      "impact": "高",
      "watch": "融資關閉進度、Microsoft 承購結構是否落地"
    },
    {
      "date": "2027-06-30",
      "date_precision": "quarter",
      "type": "capacity",
      "event": "TSMC CoWoS 供需缺口 2026 底縮至 10% 後 2027 續改善",
      "impact": "中",
      "watch": "缺口收斂＝供給可逆性上升，Bear 機率不得下調"
    },
    {
      "date": "2027-12-31",
      "date_precision": "quarter",
      "type": "product",
      "event": "Google TPU v8 Sunfish（2nm）投產、v9 Triggerfish 設計權歸屬明朗",
      "impact": "高",
      "watch": "Broadcom 是否同步取得 v9／v10 訓練晶片設計權；命中即為清倉級觸發"
    },
    {
      "date": "2026-12-31",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "Section 232 高階半導體 25% 關稅產品分類細則",
      "impact": "低",
      "watch": "Broadcom XPU 是否被列入涵蓋範圍"
    },
    {
      "date": "2027-12-31",
      "date_precision": "quarter",
      "type": "other",
      "event": "Anthropic IPO 與 XPV 平台第二批融資",
      "impact": "中",
      "watch": "改善或惡化表外平台信用結構"
    }
  ],
  "decision_inputs": {
    "signal": "A+",
    "trap": "🟢",
    "val": "🟢",
    "ma": "✅",
    "runway_post_y5": "🟡",
    "moat_trend": "↓",
    "moat": "A",
    "capalloc_grade": "A",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 6.76,
    "irr_base_pct": 18.2,
    "ev5y_pct": 134.1,
    "price_at_dd": 357.89,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": 8.7,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 1.42,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "prior_verdict": "進場",
    "prior_role": "衛星",
    "held_now": null
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "10",
    "pacing": [],
    "holding_cap": null,
    "requires_critic": [
      "QC-41 產業態勢：裁決強方向（進場）＋護城河趨勢方向性（↓）＋B2B 客戶集中型（前五大 45%）——三條件皆命中，必跑；重點覆核 Google 分單是否已從「推論」蔓延到「訓練」世代",
      "QC-41 附帶：本輪證據包未含最新一季（Q3 FY26）逐字稿與週線均線資料，均線狀態沿用前份 2026-09-03 量測，請閘覆核"
    ],
    "audit_rows": [
      {
        "row": "1",
        "condition": "基本面評級 signal = X → 迴避",
        "hit": false,
        "basis": "signal='A+'"
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
        "basis": "moat_trend='↓', moat='A'"
      },
      {
        "row": "4",
        "condition": "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）",
        "hit": false,
        "basis": "ma='✅'"
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
        "basis": "signal='A+'"
      },
      {
        "row": "7",
        "condition": "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）",
        "hit": false,
        "basis": "runway_post_y5='🟡'"
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
        "basis": "capalloc_grade='A'"
      },
      {
        "row": "8a",
        "condition": "無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）",
        "hit": false,
        "basis": "signal='A+', runway='🟡', val='🟢', moat_trend='↓', week26=8.7, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↓', cycle_gates_pass=None"
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
        "basis": "signal='A+', val='🟢'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": false,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": false,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": true,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "10-verdict",
        "condition": "命中 row10 → 進場",
        "hit": true,
        "basis": "row_hit=10"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": "FY27 本益比 <15x（約 $290）且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修→加碼至衛星上限",
    "exec_line": "新資金：現價建 1.5%（衛星上限 3% 之半），其餘掛 12-09 財報論點增強或 <$290 回檔。已持有：維持（不加碼至 Google 份額數據點證偽前；不減碼因無 thesis 級觸發；清倉僅限 Google 訓練晶片設計權移轉）"
  },
  "triggers": [
    {
      "n": 1,
      "text": "Google 客製晶片份額（相對 95→80→65 路徑）",
      "type": "風險",
      "maps_to": "R1／H1",
      "metric": "Broadcom 於 Google TPU 採購份額",
      "threshold": "較路徑低逾 10pp，或 2027 年度 <75%",
      "action": "重審護城河等級；等級降至 B 即觸強制迴避",
      "source_freq": "TrendForce／Counterpoint／每年",
      "date": "2027-06-30",
      "evidence_refs": [
        "competitive_share_entrants#2",
        "competitive_share_entrants#3",
        "customer_second_source#0",
        "customer_second_source#1"
      ]
    },
    {
      "n": 2,
      "text": "FY27 AI 半導體營收兌現度",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "TTM AI 營收對 $115B 路徑進度",
      "threshold": "連 2 季落後逾 10%",
      "action": "減碼至衛星上限之半",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 3,
      "text": "半導體分部營業利益率（管理層 mix 歸因託管閘）",
      "type": "風險",
      "maps_to": "財務品質／H3",
      "metric": "半導體分部營業利益率",
      "threshold": "跌破 55%（現 61%）連 2 季→mix 歸因證偽",
      "action": "結構性壓縮警示、減碼 1/3",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 4,
      "text": "VMware ARR 年增率與通路重構",
      "type": "假設驗證",
      "maps_to": "H2／R3",
      "metric": "VCF ARR YoY",
      "threshold": "跌破 10% 連 2 季",
      "action": "H2 降級、減碼",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": [
        "channel_business_model_shift#1"
      ]
    },
    {
      "n": 5,
      "text": "OpenAI／Anthropic 實際出貨 GW 對公司指引",
      "type": "假設驗證",
      "maps_to": "H1／R2",
      "metric": "實際部署 GW（OpenAI 2027 合約 1.3GW）",
      "threshold": "低於自身指引逾 20%，或 OpenAI 融資關閉延後逾 2 季",
      "action": "H1 核心假設削弱、凍結加碼",
      "source_freq": "公司法說＋融資報導／每季",
      "date": "2027-06-30",
      "evidence_refs": [
        "customer_concentration_credit#3",
        "customer_concentration_credit#4"
      ]
    },
    {
      "n": 6,
      "text": "XPV 表外平台信用",
      "type": "風險",
      "maps_to": "R2",
      "metric": "XPV 名目擔保規模與信用展望",
      "threshold": "20GW 全量名目達 $370B 且信用展望連 2 季負向",
      "action": "表外槓桿重審、減碼",
      "source_freq": "BofA 模型／評等機構／每季",
      "date": "",
      "evidence_refs": [
        "customer_concentration_credit#3"
      ]
    },
    {
      "n": 7,
      "text": "Google 主力訓練 TPU 設計權移轉（唯一清倉級）",
      "type": "Single Thing",
      "maps_to": "單一致命事件",
      "metric": "v9 Triggerfish／v10 訓練晶片設計權歸屬",
      "threshold": "Google 公告主設計權授予 MediaTek 或其他夥伴",
      "action": "清倉並重跑 DD",
      "source_freq": "Google 法說／產業研究／每季",
      "date": "2027-12-31",
      "evidence_refs": [
        "competitive_share_entrants#3",
        "customer_second_source#0"
      ]
    },
    {
      "n": 8,
      "text": "上行：取得 v10 或 GW 出貨超前",
      "type": "加碼",
      "maps_to": "H1",
      "metric": "設計權公告／GW 出貨",
      "threshold": "Broadcom 取得 v10，或 GW 出貨超前指引逾 10%（論點增強，非價格）",
      "action": "重審角色可回核心、加碼至衛星上限",
      "source_freq": "公司法說／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 9,
      "text": "估值回補",
      "type": "估值rearm",
      "maps_to": "H3",
      "metric": "FY+2 本益比",
      "threshold": "<15x（約 $290）且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修",
      "action": "加碼至衛星上限 3%",
      "source_freq": "自算／每兩週",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 10,
      "text": "歐盟／美國 VMware 反壟斷程序階梯",
      "type": "風險",
      "maps_to": "R3／H2",
      "metric": "程序階段",
      "threshold": "異議書→trim 1/3；裁定強制改授權模式或裁罰→H2 重審、減碼至半",
      "action": "依階梯",
      "source_freq": "歐盟／DOJ 公告",
      "date": "2027-03-31",
      "evidence_refs": [
        "regulatory_antitrust#0",
        "regulatory_antitrust#1",
        "regulatory_antitrust#2"
      ]
    },
    {
      "n": 11,
      "text": "關稅、出口管制與中國政策",
      "type": "風險",
      "maps_to": "R3／地緣",
      "metric": "Section 232 分類、光收發器禁令、中國 VMware 移除令",
      "threshold": "Broadcom XPU 納入 25% 關稅；中國軟體營收流失可量化",
      "action": "重算成本吸收（合併毛利率 −2pp 為吸收失敗判定閘）",
      "source_freq": "商務部／CBP／每季",
      "date": "2026-12-31",
      "evidence_refs": [
        "reg_tariff_export#0",
        "reg_tariff_export#3",
        "regulatory_antitrust#4",
        "regulatory_antitrust#5"
      ]
    },
    {
      "n": 12,
      "text": "TSMC／CoWoS 供給鏈與台灣風險",
      "type": "風險",
      "maps_to": "供給",
      "metric": "CoWoS 分配、雷射／PCB 缺口、台海事件",
      "threshold": "供給約束使季度 AI 營收落後指引逾 10%；台海衝突為 thesis 已破",
      "action": "前者列入兌現度追蹤；後者清倉",
      "source_freq": "TSMC 法說／每季",
      "date": "",
      "evidence_refs": [
        "geo_supply_chain#0",
        "geo_supply_chain#1",
        "geo_supply_chain#2",
        "supply_demand_durability#2"
      ]
    },
    {
      "n": 13,
      "text": "資安事件與軟體信任",
      "type": "風險",
      "maps_to": "H2",
      "metric": "重大漏洞／入侵事件與客戶流失",
      "threshold": "事件導致 ARR 年增跌破 10%",
      "action": "併入觸發器 4",
      "source_freq": "CISA／公司公告",
      "date": "",
      "evidence_refs": [
        "major_events#1",
        "major_events#2",
        "product_recall_warning#0",
        "product_recall_warning#1"
      ]
    },
    {
      "n": 14,
      "text": "客戶集中度與自研能力",
      "type": "風險",
      "maps_to": "R1／R2",
      "metric": "前五大占營收（10-Q 45%）、客戶自有工具鏈進展",
      "threshold": "前五大 >55% 且任一客戶宣布自有工具鏈取代 Broadcom",
      "action": "集中度升 🔴、減碼",
      "source_freq": "10-Q／每季",
      "date": "",
      "evidence_refs": [
        "customer_concentration_credit#0",
        "customer_concentration_credit#2",
        "customer_second_source#2",
        "substitute_technology#1"
      ]
    },
    {
      "n": 15,
      "text": "估值 trim 天花板",
      "type": "減碼",
      "maps_to": "H3",
      "metric": "FY+2 本益比",
      "threshold": ">30x（自身短窗高點 39x 下修校準）",
      "action": "最多 trim 1/3，不單獨清倉",
      "source_freq": "自算／每兩週",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 16,
      "text": "Q4 FY26 財報＋新 CFO 首季",
      "type": "複審日期",
      "maps_to": "—",
      "metric": "—",
      "threshold": "—",
      "action": "重跑 DD",
      "source_freq": "公司財報／一次性",
      "date": "2026-12-09",
      "evidence_refs": []
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單",
      "side_a": "方向一致：AI 需求真實且受供給約束（backlog >$73B、能見度 2028、CoWoS 售罄）；現金轉換頂尖（FCF 46%）；資本配置紀律 A；估值兩尺皆便宜",
      "side_b": "矛盾拓撲＝集中單一軸：Google 分單與客戶自研（護城河軸），其餘軸為程度差異",
      "ruling": "爭議集中→點名護城河軸為 binding 軸，信心不整體下修但角色降衛星",
      "evidence_level": "L1",
      "settle_metric": "Google 世代設計權歸屬",
      "if_then": [
        "若 Broadcom 取得 v9／v10 訓練設計權→角色回核心",
        "若 v9 訓練交 MediaTek→清倉"
      ]
    },
    {
      "axis": "AI 指引加速 vs Google 份額稀釋",
      "side_a": "FY27 $115B／FY28 $230B 指引、Q3 +221%——絕對金額爆發",
      "side_b": "Google 刻意四夥伴、MediaTek 成本低 20-30%、Marvell 簽約——份額路徑 95→80→65",
      "ruling": "可調和（程度差異）：份額稀釋與絕對金額成長同時為真；Base 對 FY28 指引打八折吸收稀釋，不採全額指引",
      "evidence_level": "L1 財報 vs L2 產業報導",
      "settle_metric": "Google 於 AI 營收占比與 FY28 AI 營收實績",
      "if_then": [
        "若 FY27 AI 營收 ≥$115B 且 Google 占比降但金額升→維持",
        "若 FY27 落後指引逾 10% 連 2 季→減碼"
      ],
      "evidence_refs": [
        "competitive_share_entrants#2",
        "competitive_share_entrants#3"
      ]
    },
    {
      "axis": "合約承諾 vs 客戶融資能力（不可調和）",
      "side_a": "OpenAI 1.3GW 2027 合約承諾、Anthropic 8.5GW、Meta 3GW；Q3 營收 $29.6B 已印",
      "side_b": "OpenAI 2026-05 無法關閉 $18B 融資、2026 預虧 $14B；Broadcom 只願出資第一階段、放寬對等出資；XPV 名目 $370B",
      "ruling": "選 A 側：L1（已實現營收＋合約）高於 L2（融資報導，已 4 個月且其後 Q3 仍超標）；但把出貨 GW 與融資關閉列為獨立觸發器，Bear 機率因此守 30% 不降",
      "evidence_level": "L1 vs L2",
      "settle_metric": "OpenAI 2027 實際部署 GW 與融資關閉公告",
      "if_then": [
        "若 2027 上半年 OpenAI 融資關閉且首批出貨→其餘 1/2 倉位解鎖",
        "若融資延後逾 2 季或 Broadcom 出資比例再升→減碼至衛星上限之半"
      ],
      "evidence_refs": [
        "customer_concentration_credit#3",
        "customer_concentration_credit#4"
      ]
    },
    {
      "axis": "Steelman：現在就賣的最強論證",
      "side_a": "①最大客戶已公開要每個環節都有替代者，而替代者成本低 20-30%，這是護城河定價面的結構性上限；②FY28 EPS 30 若是資本週期峰值，18.5x 是循環股頂部倍數不是便宜；③前五大 45%＋單一經銷商 42%＋$370B 表外名目，任一環節斷鏈都是 −50% 級；④合併毛利率已在下滑，管理層要求「分開建模」是敘事管理的典型前兆",
      "side_b": "逐點回應：①份額稀釋已計入 Base 八折與 Bear 30%，且執行面（六客戶、供給鎖定）在擴大，記帳在趨勢不在等級；②共識 FY28 一週上修 13.5% 至 30、90 天 +17%，峰值論尚無下修證據，Bear 錨（15×12）已定價週期回落；③集中度是衛星角色與 3% 上限的原因，不是迴避的原因——迴避須 thesis 級失敗證據；④半導體分部營業利益率 +440bp YoY、非 GAAP 營業利益率 QoQ 續升，mix 歸因暫採信並託管於觸發器 3",
      "ruling": "進場維持，但賣方論證 ①③ 直接決定角色與上限，非僅記錄",
      "evidence_level": "L1／L2 混合",
      "settle_metric": "半導體分部營業利益率與 Google 設計權",
      "if_then": [
        "若分部營業利益率 <55% 連 2 季→賣方論證 ④ 成立，減碼 1/3",
        "若 FY28 共識連 2 次下修→賣方論證 ② 成立，減碼至半"
      ]
    },
    {
      "axis": "與前份報告（2026-09-03）交叉：裁決與方法",
      "side_a": "本次：進場｜衛星、上限 3%",
      "side_b": "前份：進場｜衛星（自 2026-06-23 核心降衛星）",
      "ruling": "方向與角色一致，未翻面；90 天內無觸發器發火，亦無承繼需求。差異僅在倉位上限明示 3%（前份未明示）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若 12-09 財報論點增強→上限可回 5%",
        "若 Google 份額數據點證偽→維持 3% 並凍結"
      ]
    },
    {
      "axis": "前份漂移：price_at_dd",
      "prior_field": "price_at_dd",
      "side_a": "本次 357.89（2026-09-04 收盤）",
      "side_b": "前份 367.24",
      "ruling": "主因＝價格變了（−2.5%，財報後續回檔）；基本面未變；方法論未變",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "若價格續跌至 $290→估值回補觸發",
        "若反彈逾 $450→停止加碼"
      ]
    },
    {
      "axis": "前份漂移：ev5y_pct",
      "prior_field": "ev5y_pct",
      "side_a": "本次 134.1%",
      "side_b": "前份 125.1%",
      "ruling": "主因排序：①基本面（共識 FY28 EPS 26.43→30.0 上修 13.5%，Base 路徑終端 38.47→39.5）②價格（−2.5% 使同一終端價報酬率升）③方法論未變（同三情境、同機率）",
      "evidence_level": "L2 共識",
      "settle_metric": "FY28 共識方向",
      "if_then": [
        "若共識 FY28 續升→Base 上修",
        "若下修→回 125% 以下"
      ]
    },
    {
      "axis": "前份漂移：irr_base_pct",
      "prior_field": "irr_base_pct",
      "side_a": "本次約 18.2%（含息）",
      "side_b": "前份 15.9%",
      "ruling": "主因＝基本面（FY28 共識上修帶動 Base 終端 EPS 39.5 vs 38.47）與價格（−2.5%）；方法論未變。注意：Base 不含息 IRR >15% 觸發罕見警示，機率分配已守 30／40／30 未放寬",
      "evidence_level": "L2",
      "settle_metric": "FY28 共識",
      "if_then": [
        "若 FY27 兌現→維持",
        "若落後→重算"
      ]
    },
    {
      "axis": "前份漂移：asym_ratio",
      "prior_field": "asym_ratio",
      "side_a": "本次 6.76",
      "side_b": "前份 6.0",
      "ruling": "主因＝價格（現價較低使 Bull 上行放大、Bear 下行縮小）；Bear 終端 180 vs 170 屬方法論微調（Bear 本益比 10x→12x，因共識未下修、Bear 地板尚平穩）。護城河趨勢↓下，此比率僅作參考、不作進場依據",
      "evidence_level": "—",
      "settle_metric": "共識 FY28 是否連續下修（Bear 地板是否下移）",
      "if_then": [
        "若共識連 2 次下修→比率標失效",
        "否則維持參考"
      ]
    },
    {
      "axis": "前份漂移：bear_5y_price",
      "prior_field": "bear_5y_price",
      "side_a": "本次 180（15×12）",
      "side_b": "前份 170（17×10）",
      "ruling": "主因＝方法論（Bear 終端 EPS 15 較前份 17 更深，但終端倍數 12x 較 10x 高：Bear 故事改為「循環股定價」而非「無成長折價」；淨效果 +$10）；基本面與價格非主因",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若 2028 資本週期見頂訊號出現→Bear 倍數回 10x",
        "否則維持"
      ]
    },
    {
      "axis": "前份漂移：pct_5y",
      "prior_field": "pct_5y",
      "side_a": "本次 24.4%",
      "side_b": "前份 15.0%",
      "ruling": "主因＝方法論（本輪以 valuation_history trailing 年度 4 點樣本計算；前份口徑不同）；燈號結論不變（皆 🟢）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若分位 >30% 且 PEG >1→燈號降",
        "否則維持"
      ]
    },
    {
      "axis": "均線狀態沿用",
      "prior_field": "ma",
      "side_a": "本次 ✅（沿用前份 2026-09-03 量測）",
      "side_b": "前份 ✅",
      "ruling": "本輪證據包未含週線 W52／W104／W250 資料，價僅較前份低 2.5%，狀態視為未變；標「證據包未涵蓋」請閘覆核",
      "evidence_level": "—",
      "settle_metric": "週線資料",
      "if_then": [
        "若價 <W52→狀態改 🟢或🟠，節奏調節不改裁決",
        "否則維持"
      ]
    },
    {
      "axis": "ID 對帳",
      "side_a": "ID：AI Accelerator Demand（as-of 2026-09-05）shortage／Phase II／priced_in mid；ID：Hyperscaler（2026-05-05）shortage／Phase II",
      "side_b": "本檔：Phase II、供需 durability 裁決＝供給可逆性高（CoWoS 缺口 2026 底縮至 10%，緊缺脆弱、下行更猛）",
      "ruling": "一致，無分歧；priced_in mid 與本檔估值 🟢 略有張力，以本檔自身估值尺為準（ID 為產業層）",
      "evidence_level": "L2",
      "settle_metric": "CoWoS 缺口與雲端 capex 指引",
      "if_then": [
        "若 ID 更新為 Phase III→Bear 機率上調",
        "否則維持"
      ]
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "證據包無 30 天內 NVDA／MRVL／AMD 裁決紀錄",
      "side_b": "—",
      "ruling": "一句帶過：無近期 peer 裁決可對帳，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ]
    },
    {
      "axis": "賣方共識對照",
      "side_a": "57 位分析師目標價均值 $520、財報後多家上修；現價低於均值 31%",
      "side_b": "本檔 1 年目標 $425 較均值保守 18%",
      "ruling": "現價低於共識均值→續漲不需共識上修＝結構順風，支持進場；本檔更保守之處在 Google 份額與 2028 資本週期假設；市場錯在哪：共識把 FY28 $230B 指引近乎全額印進 EPS 30，卻同時給 18.5x——隱含「2028 後急降」；本檔認為錯的是倍數而非盈餘方向，故 Base 八折盈餘配 20x",
      "evidence_level": "L2",
      "settle_metric": "FY28 實績與倍數",
      "if_then": [
        "若 FY28 兌現 ≥$185B→re-rate 至 22-25x",
        "若 FY28 <$150B→共識對、本檔錯，減碼"
      ],
      "evidence_refs": [
        "customer_concentration_credit#0"
      ]
    },
    {
      "axis": "樞紐變數與共同顯影指標",
      "side_a": "雲端 AI 資本支出 ROI 兌現同時打 H1（量）與 H3（倍數框架）；R1 與 R2 兩條失敗向量非獨立（Google 分單與客戶融資皆由「客戶議價與資本壓力」驅動）",
      "side_b": "共同財報級顯影指標＝半導體分部營業利益率（份額稀釋與客戶壓價都先在此顯影）",
      "ruling": "監測首位＝半導體分部營業利益率（觸發器 3）；Bear 機率不以獨立事件相乘，直接取 30%",
      "evidence_level": "L1",
      "settle_metric": "半導體分部營業利益率",
      "if_then": [
        "若 <55% 連 2 季→減碼 1/3",
        "若 ≥60% 續 4 季→凍結解除"
      ]
    },
    {
      "axis": "監管量化與程序階梯",
      "side_a": "歐盟正式調查（2026-02）、文件案敗訴（2026-08）、美國授權調查（2026-07）、中國移除令",
      "side_b": "受影響營收：歐洲基礎設施軟體占比證據包未涵蓋，無法量化",
      "ruling": "標「證據包未涵蓋」；程序階梯寫入觸發器 10（異議書→trim 1/3；裁定→減至半）；不以定性一句話帶過",
      "evidence_level": "L1 程序",
      "settle_metric": "歐盟異議書",
      "if_then": [
        "異議書→trim 1/3",
        "無異議書且 ARR ≥12%→維持"
      ],
      "evidence_refs": [
        "regulatory_antitrust#0",
        "regulatory_antitrust#1",
        "regulatory_antitrust#2",
        "regulatory_antitrust#4",
        "regulatory_antitrust#5"
      ]
    },
    {
      "axis": "利空新鮮度與倉位",
      "side_a": "Google 四夥伴（2026-08-20）、MediaTek 目標上修（2026-07-31）皆 <1 季",
      "side_b": "賣方財報後（2026-09-03）仍上修目標價→已部分進入模型",
      "ruling": "初始倉位仍下修一級（首階 1/2 而非全額）並凍結加碼至 Zebrafish 量產後首個份額數據點",
      "evidence_level": "L2",
      "settle_metric": "Q4 2026 Google 份額數據點",
      "if_then": [
        "數據點未證偽→解凍",
        "證偽→維持凍結並減碼"
      ],
      "evidence_refs": [
        "competitive_share_entrants#3",
        "competitive_share_entrants#2"
      ]
    },
    {
      "axis": "精英指標未穿越週期",
      "side_a": "非 GAAP 營業利益率 67.9% 與 FCF 46% 處歷史高檔，未穿越完整 AI 資本週期",
      "side_b": "結構性成分＝軟體 70%+ 分部與規模攤薄 R&D 15.9%；週期性成分＝XPU 系統含量與客戶預付；殘差無法拆",
      "ruling": "殘差不選邊，定價進 Bear 30% 與衛星角色；品質分不滿額（成長持久性 8.0 非 8.5）",
      "evidence_level": "L1",
      "settle_metric": "2028 後分部營業利益率",
      "if_then": [
        "若 2028 分部營業利益率守 58%+→品質分回 8.5",
        "若 <55%→降"
      ]
    },
    {
      "axis": "前份漂移：rearm_trigger",
      "side_a": "前份 2026-09-03 報告未填再進場條件（前一版格式沒有這個欄位）",
      "side_b": "本次填入衛星加碼條件（FY27 本益比 <15x 約 $290 且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修）",
      "ruling": "方法論驅動：欄位由空變有，非資訊變化；歸因主因＝方法論（v17 必填），次因＝無",
      "evidence_level": "前後兩份報告的機器欄逐欄對照",
      "settle_metric": "不適用",
      "if_then": [
        "若前份實有再進場條件而擷取遺漏 → 改列資訊變化並重新歸因"
      ],
      "prior_field": "rearm_trigger",
      "evidence_refs": []
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "假設①Google 多世代長約（至 2031）保證訓練晶片主設計權——若協議是份額制而非固定量（管理層拒答金額與結構，來源：摘要），前提不成立則 Google 營收在 2028 可能減半",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "customer_second_source#0"
        ]
      },
      {
        "text": "假設②OpenAI／Anthropic 承諾可融資——若融資市場對 AI 基建轉冷，10GW＋8.5GW 承諾縮水、XPV 平台成為 Broadcom 表外信用曝險",
        "evidence_refs": [
          "customer_concentration_credit#3",
          "customer_concentration_credit#4"
        ]
      },
      {
        "text": "假設③TSMC／CoWoS 供給能如期擴張且台海無事——供給鏈 100% 集中台灣，雷射／PCB 缺口已蔓延；NVIDIA 預訂過半 CoWoS-L",
        "evidence_refs": [
          "geo_supply_chain#0",
          "geo_supply_chain#1",
          "geo_supply_chain#2",
          "supply_demand_durability#2"
        ]
      },
      {
        "text": "假設④管理層對合併毛利率下滑的 mix 歸因為真——若客戶壓價已在半導體分部顯影，則 61% 分部營業利益率是峰值",
        "evidence_refs": []
      },
      {
        "text": "本輪證據缺口：最新一季（Q3 FY26）逐字稿未親讀，只有財報數字與前三季摘要；週線均線資料、投入資本與營運資金明細、同業前瞻本益比皆未涵蓋",
        "evidence_refs": []
      },
      {
        "text": "敏感度排序：Google 份額每低 10pp 對 FY28 EPS 約 −8%；雲端 capex 2028 下修 20% 對 FY28 EPS 約 −15%；分部營業利益率 −5pp 對 EPS 約 −8%——最大單一敏感度為 capex 週期，但其為漸進非離散事件，故單一致命事件取 Google 設計權（第二大且離散）",
        "evidence_refs": []
      }
    ],
    "failure_story": "五年後虧 50%：2028 雲端資本支出進入消化期，同時 Google 把訓練世代也交 MediaTek、OpenAI 融資斷鏈使 10GW 縮至 3GW；AI 營收 2028 停在 $150B 後回落，EPS 自 27 跌回 15，市場改給 12x。與單一致命事件關係：⚠ 部分重疊（Google 為主軸、融資為次軸）→ 次軸已補為觸發器 5／6",
    "second_failure": "thesis 完全兌現但以「系統／機架與客戶自有 IP 代工」形態兌現：AI 營收達 $230B，但半導體分部營業利益率自 61% 壓至 50%、Broadcom 被市場重新歸類為客製代工而非設計 IP 平台，估值框架自 25x 切換到 15x，5 年報酬約 +40% 而非 +120%。機率不可忽略→Bull 終端倍數壓在 26x（非 30x）",
    "max_dd": {
      "lo": -58.0,
      "hi": -40.0,
      "path_risk": "🔴",
      "trigger_time": "最可能觸發：2027 下半年至 2028 上半年（雲端 FY28 capex 指引與 Google v9 設計權明朗期重疊）；恢復峰值：若 thesis 完整需 18-30 個月，若 Google 訓練設計權移轉則 thesis 已破不假設恢復。🔴 且 thesis 脆弱（護城河趨勢↓）→倉位上限自 6% 下修至 3%、持有年限標中期並警示中途出場風險"
    }
  },
  "kill_metrics": [
    {
      "metric": "Broadcom 於 Google 客製晶片份額（相對路徑 95→80→65）",
      "bear_threshold": "較路徑低逾 10pp，或 2027 年度 <75%→護城河重審",
      "window": "每年",
      "source": "TrendForce／Counterpoint",
      "last_status": "ok"
    },
    {
      "metric": "FY27 AI 半導體營收兌現度（指引 $115B）",
      "bear_threshold": "連 2 季落後指引進度逾 10%→減碼",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "半導體分部營業利益率",
      "bear_threshold": "跌破 55%（現 61%）連 2 季→結構性壓縮警示",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "VMware VCF ARR 年增率",
      "bear_threshold": "跌破 10% 連 2 季→H2 降級",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "OpenAI／Anthropic 實際出貨 GW 對指引",
      "bear_threshold": "低於自身指引逾 20%→H1 削弱",
      "window": "每季",
      "source": "公司法說",
      "last_status": "ok"
    },
    {
      "metric": "XPV 平台名目擔保與信用展望",
      "bear_threshold": "名目達 $370B 且信用展望連 2 季負向→表外槓桿重審",
      "window": "每季",
      "source": "BofA 模型／評等",
      "last_status": "ok"
    },
    {
      "metric": "Google v9／v10 訓練晶片設計權歸屬",
      "bear_threshold": "主設計權授予 MediaTek 或其他夥伴→清倉",
      "window": "每季",
      "source": "Google 法說／產業研究",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "輸入：FCF 利潤率 46%（Q3 FY26）、非 GAAP 營業利益率 67.9%、資本支出 $532M 對營收 $29.6B（1.8%）、營收 YoY +86%→輕資產高現金複利體質，非循環商品定價（無 spot 價格）、非金融、已獲利→品質複利成長，信心高；AI 資本週期色彩以 Bear 機率 30% 與供給可逆性裁決承接，不換尺",
    "thesis": "H1 門檻取自指引 $115B／$230B（capital_markets_pricing#1）與 Google 份額路徑 95→80→65；H2 取自 Q3 軟體 $8.75B（+29%）與 VCF ARR +17%（2026-06 口徑）；H3 取自 FY27 本益比 18.5x 與短窗高點 39x→15-25x 區間。單一致命事件由敏感度排序取第二大但唯一離散者（Google 設計權），機率 20-25% 以多世代長約為反向錨",
    "industry": "Phase II 由 ID（AI Accelerator Demand 2026-09-05）載入，經自身位置閘：backlog >$73B、能見度 2028、CoWoS 缺口 20%→10%→擴張後段非過熱頂部。供需 durability 裁決＝供給可逆性高（缺口正在閉合、NVIDIA 預訂過半 CoWoS-L 顯示競爭產能）→Bear 機率 30% 不得下調。議價權：上游弱（TSMC 單一）、下游中偏弱（前五大 45%、單一經銷商 42%，10-Q 2026-05-03）",
    "moat": "執行 9（六客戶、供給鎖定至 2028、AI 營收 +221%、設計夥伴份額 ~60%）×定價 8（Google 明示替代者、MediaTek 成本低 20-30%、合併毛利率 mix 下滑閘二扣 0 至 −0.5）→合併 8.5→等級 A（執行加權 0.6 得 8.6 進位 9）。趨勢：一擴一縮取論點更關鍵的份額維度→↓；閘 A 因最大客戶份額下滑不得↑。閘一：營業利益率對 MRVL 差 +27.7pp、分部 +440bp YoY→擴大，可打 ≥8。閘三：對手絕對美元新增（MediaTek 2026E >$2B）遠低於 AVGO AI 新增（YoY +$11.5B）→未觸規模質變。記帳一次：負面證據記趨勢不記等級→不觸強制迴避",
    "growth": "Runway 5-7 年：AI 營收 $58B→$230B（FY28 指引）後增速取決於第二輪 capex；Y5 末客製 ASIC 對雲端加速器滲透估 35-50%（ID：自研 25-30% 且升）且無 sourced 第二 S 曲線（矽光子「尚未到位」，來源：摘要）→🟡。內生天花板：ROIIC 代理 80%×再投資率 6%≈5%；Base EPS CAGR 15.4% 超出⚠→Bear ≥30%；缺口歸因＝客戶承擔資本的 XPU 新 S 曲線（backlog sourced）＋營業槓桿，非 re-rate。衰退訊號 2 個（mix 毛利率、Google 份額）→🟡觀察、五問後定性 🟢 非陷阱",
    "quality": "Q3 FY26：FCF $13,665M÷營收 $29,591M＝46.2%（Q2 46.0%，持平高檔）；非 GAAP 營業利益 $20,095M÷$29,591M＝67.9%（Q2 67.3%）；SBC $2,019M＝營收 6.8%、GAAP 營業利益 12.7%（Q2 9.4%／19.4%）。營收 YoY +86% 對 GAAP 營業利益率 48.6%→53.9% QoQ 擴張→發散 <0（營業槓桿正）。三年逐年、DuPont 投入資本、CCC 不在證據包→標未涵蓋，品質分以 TTM 與最新季替代並在分數扣 0.2",
    "governance": "計分卡：VMware ROIIC≈軟體年化營業利益 $25B÷$69B≈35% 過；回購收益率以 FY27 盈餘殖利率 5.4%（1÷18.5）近似過（均價未涵蓋）；SBC 淨稀釋≈$8B÷$1.68T≈0.5%／年過→3／3→A。股息 +10%、回購額度 $17.5B 至 2026 底（來源：摘要）。CFO 交接（Spears→Thuener，2026-06-12）設 2026-12-09 有日期複審；內部人交易未涵蓋標數據限制。無併購、無重編、無證券集體訴訟（events 軸）→🟢",
    "valuation": "FY27 本益比＝357.89÷19.33＝18.51；FY26 基準 30.77。3Y EPS CAGR 以 FY26→FY28 共識（11.63→30.0）2 年化 60.6%（無 FY29 共識，標 2 年口徑）→PEG 0.31（FY27）／0.51（FY26）。五年分位 24.4%（trailing 4 年度樣本）。兩尺 🟢。1 年目標 19.33×22＝$425（+18.8%）；2 年 26.0×22＝$572（+59.8%）；Bear 錨 17.4×15＝$261（−27%）。Base 5Y：39.5×20＝$790（+120.7%）、IRR 不含息 17.2%＋息 1.0%；EPS 貢獻 15.4%／年、re-rate 1.6%／年（20÷18.51）→re-rate 占比約 9% <40%→非估值依賴型",
    "trap_analysis": "低 PEG 的三種解釋：週期峰值盈餘、份額侵蝕帳單、市場錯價。反證：共識 FY28 一週 +13.5%、90 天 +17%（consensus_revision，stale=false），FCF 與盈餘同步，backlog 覆蓋 18 個月→前兩者尚無數據支持；正證：前五大 45%、Google 分單、OpenAI 融資→列觀察期指標。空頭一擊路徑：FY28 共識 30→22 且倍數 18.5x→12x→$260-230（−27% 至 −36%）。定性 🟢 非陷阱，2 訊號記為 🟡 觀察",
    "premortem": "Max DD：AVGO 自身 2022 與 2025 上半年回撤約 −30% 至 −40%（前份口徑），疊加 thesis 級事件（Google 設計權）估 −40% 至 −58%（寬度 18pp ≥10）→🔴；觸發時點 2027H2-2028H1；🔴且趨勢↓→上限 6%→3%。失敗故事與單一致命事件部分重疊→次軸補觸發器 5／6。第二敗局（代工化）反映在 Bull 終端 26x 非 30x。Bull 30／Base 40／Bear 30：Bear 依 searched durability（CoWoS 缺口閉合、供給可逆）與內生天花板超出，非 pattern 外推"
  },
  "evidence_dismissed": [
    {
      "ref": "customer_concentration_credit#1",
      "reason": "FY2025 10-K（2025-12-18）前五大 40%／經銷商 48% 已被 2026-05-03 10-Q 更新一季數字（45%／56%）取代，依最新一季優先序不重複引用"
    },
    {
      "ref": "reg_tariff_export#1",
      "reason": "8-K 制式風險因子文字，無新增量化資訊，內容已由 reg_tariff_export#0 的 Section 232 具體條款覆蓋，屬重複計"
    },
    {
      "ref": "reg_tariff_export#4",
      "reason": "「中國占營收 meaningful portion」未給占比數字，且 edgar_concentrations 未揭露地區集中度，口徑不可回溯無法量化"
    },
    {
      "ref": "regulatory_antitrust#3",
      "reason": "來源為單一二手彙整（Simply Wall St），未附 ITC docket 編號與涉案產品線，Broadcom 為多被告之一且屬記憶體模組專利，無法對應到營收軸"
    },
    {
      "ref": "major_events#3",
      "reason": "員工資料經供應商外洩，資料出現於 2024-12（12 個月窗外），屬人資資料非客戶或產品層事件，與 thesis 無接線"
    },
    {
      "ref": "substitute_technology#0",
      "reason": "與 competitive_share_entrants#2 為同一篇報導的中文轉述（MediaTek 15-20% 目標），已在 R1 與觸發器 1 記帳一次，避免重複扣分"
    }
  ],
  "plain": {
    "verdict_line": "進場，但只當衛星，倉位不超過三分之一的常規上限",
    "verdict_sub": "現價先建一半，另一半等十二月財報確認或股價跌到二百九十以下再補。",
    "five": {
      "how_it_makes_money": "幫 Google、Meta、OpenAI 這些雲端巨頭設計專屬 AI 晶片，再加上網路晶片與 VMware 軟體訂閱。客戶出架構，博通出設計與整合，工廠由台積電代工。",
      "why_now": "財報剛超標卻回檔，用明年盈餘算本益比只有十八倍多。共識還在上修，市場給的是循環股價格。",
      "why_this_size": "最大客戶 Google 正刻意扶植第二、第三家設計夥伴。這件事已經在發生，所以只能當衛星，不當核心。",
      "biggest_fear": "Google 把下一代訓練晶片的主設計權交給聯發科。這是唯一會讓我直接清倉的事。",
      "how_to_act": "現價買一半，十二月九日財報若 AI 營收達標再補另一半。跌破二百九十且基本面沒壞也可補。"
    },
    "business": {
      "what_to_whom": "賣客製 AI 加速器與網路晶片給六家雲端與模型公司，賣私有雲軟體訂閱給大型企業。前五大客戶占營收快一半。",
      "why_customers_stay": "換設計夥伴要重跑一到兩年的晶片流程，而且博通手上有台積電先進封裝與高速傳輸的整合能力。軟體端則是換掉 VMware 的遷移成本很高。",
      "moat_direction": "等級 A，方向往下。最弱的地方在定價：Google 已公開要每個環節都有替代者，聯發科的推論晶片還便宜兩三成。"
    },
    "bets": [
      {
        "claim": "明年 AI 晶片營收能兌現一千一百五十億的指引，六家客戶一起放量。",
        "wrong_when": "連續兩季進度落後指引一成以上，我就錯了。"
      },
      {
        "claim": "Google 分單只影響推論晶片，訓練晶片主設計權還在博通手上。",
        "wrong_when": "Google 公告下一代訓練晶片交給別人，我就錯了。"
      },
      {
        "claim": "毛利率下滑只是產品組合，半導體部門獲利率守得住。",
        "wrong_when": "半導體部門營業利益率連兩季跌破五成五，我就錯了。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "Google 份額比預期掉得快，二〇二七年低於七成五，或下一代訓練晶片易主。"
      },
      {
        "clock": "🔥",
        "text": "OpenAI 融資關不了，一百八十億缺口拖累十 GW 承諾，表外平台名目上看三千七百億。"
      },
      {
        "clock": "🐢",
        "text": "歐盟反壟斷調查發異議書，VMware 被迫改授權模式，軟體現金流變薄。"
      }
    ],
    "market_wrong": "共識把二〇二八年兩千三百億的指引幾乎全額算進盈餘，卻只給十八倍多。這等於同時相信指引又相信之後會急跌。我認為盈餘該打八折，但倍數該回到二十倍。錯的是倍數，不是方向。",
    "growth_funding": "公司自己幾乎不用花錢擴產，內生成長天花板約百分之五。共識盈餘年增一成五以上，差額來自客戶出錢的專屬晶片新曲線，不靠估值上修。",
    "stories": {
      "bull": "六家客戶如期部署，博通連下一代 Google 訓練晶片也拿到。二〇三一年盈餘六十美元，市場給二十六倍。",
      "base": "指引兌現八成，Google 份額慢慢從九成五降到六成五，但金額仍在漲。二〇三一年盈餘近四十美元，倍數二十倍。",
      "bear": "二〇二八年雲端資本支出進入消化期，Google 推論轉聯發科，OpenAI 承諾縮水。盈餘退回十五美元，市場當循環股給十二倍。"
    },
    "change_my_mind": [
      {
        "what": "Google 下一代訓練晶片主設計權",
        "threshold": "公告交給聯發科或其他夥伴",
        "then": "清倉並重跑研究",
        "when": "2027-12-31 前明朗"
      },
      {
        "what": "明年 AI 晶片營收進度",
        "threshold": "連兩季落後指引一成以上",
        "then": "減碼到衛星上限的一半",
        "when": "2026-12-09 起逐季"
      },
      {
        "what": "半導體部門營業利益率",
        "threshold": "跌破五成五連兩季",
        "then": "減碼三分之一",
        "when": "—"
      }
    ],
    "prior_compare_reason": "與兩天前的報告裁決相同，都是進場加衛星。差別只在價格再低了兩個多百分點，以及後年共識盈餘上修，五年期望報酬略升。",
    "how_to_lose": "第一種死法是雲端資本支出二〇二八年見頂，同時 Google 把訓練晶片也分出去，盈餘與倍數一起縮。第二種是論點全對但博通變成低毛利的代工角色，賺到營收卻賺不到估值。第三種是台海事件，那不是風險是結束。",
    "evidence_quality": "十七軸都有查到，數字用到剛公布的本季財報。逐字稿只有前三季摘要，本季法說沒親讀；週線均線與營運資金明細這輪沒拿到。"
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


