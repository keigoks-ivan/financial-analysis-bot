你是 stock-analyst v17 的**判斷層閘（gate）**，標的 WDAY（20260905）。你未參與寫判斷，這是一次跨模型冷讀。你的任務只有一件：**依下列 ①–⑦ 逐條複核判斷物，計數判斷級 🔴**。

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

## 輸出（一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDAY_20260905/gate_audit.md`，格式固定，下游機械解析）

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

**輪次上限 `6` 輪。** 一次 Write 完成，寫完即回報，不要回讀自己寫的 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDAY_20260905/gate_audit.md`。

## 回報（≤100 字）

判斷級 🔴 = N、🟡 = M，以及 🔴 各條的軸別與指向欄位。


===== BUNDLE =====

## ① 任務頭

標的：WDAY　日期：20260905　角色：stock-analyst v16.2 三步制的判斷層 critic（gate） agent。

輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。

---

## ③ Evidence 緊湊版

ticker=WDAY　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 195.79, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-08-27", "trading_days_since": 7, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 3, "current": 42.2, "high": {"value": 139.43, "date": "2025-01-31"}, "low": {"value": 56.57, "date": "2024-01-31"}, "current_percentile_within_annual_points": 0.0}, "ps": {"n_points": 4, "current": 4.65, "high": {"value": 10.77, "date": "2024-01-31"}, "low": {"value": 4.57, "date": "2026-01-31"}, "current_percentile_within_annual_points": 1.2}, "ev_s": {"n_points": 4, "current": 4.68, "high": {"value": 10.95, "date": "2024-01-31"}, "low": {"value": 4.82, "date": "2026-01-31"}, "current_percentile_within_annual_points": 0.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 146.19, "fy1_eps": 10.72, "fwd_pe": 13.64}, {"snapshot_date": "2026-06-04", "price_used": 144.28, "fy1_eps": 10.73, "fwd_pe": 13.45}, {"snapshot_date": "2026-06-23", "price_used": 124.21, "fy1_eps": 10.73, "fwd_pe": 11.58}, {"snapshot_date": "2026-07-16", "price_used": 144.78, "fy1_eps": 10.74, "fwd_pe": 13.48}, {"snapshot_date": "2026-07-30", "price_used": 160.34, "fy1_eps": 10.77, "fwd_pe": 14.89}, {"snapshot_date": "2026-08-13", "price_used": 198.68, "fy1_eps": 10.77, "fwd_pe": 18.45}, {"snapshot_date": "2026-08-28", "price_used": 195.79, "fy1_eps": 10.76, "fwd_pe": 18.2}, {"snapshot_date": "2026-09-04", "price_used": 195.79, "fy1_eps": 11.06, "fwd_pe": 17.7}], "current": 17.7, "high": 18.45, "low": 11.58, "current_percentile_within_window": 89.1, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 8 份快照（2026-05-26 (incremental updates over 2026-05-25 base) ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": 35.7, "return_26w_pct": 29.63, "excess_return_13w_pct": 31.17, "excess_return_26w_pct": 15.11, "benchmark": "^GSPC", "rsi14": 56.13, "rsi14_usable": true, "distance_from_52w_high_pct": -20.95, "distance_from_52w_low_pct": 74.04, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 11.06, "fy2": 13.21, "fy3": 15.42}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 10.76, "fy2": 12.64, "fy3": 14.67}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 10.73, "fy2": 12.64, "fy3": 14.66}, "fy1": {"revision_pct": 2.79, "from": 10.76, "to": 11.06, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 4.51, "from": 12.64, "to": 13.21, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 5.11, "from": 14.67, "to": 15.42, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 3.08, "fy2_revision_90d_pct": 4.51, "fy3_revision_90d_pct": 5.18, "stale": false, "note": null}, "peer_financials": {"WDAY": {"gross_margin_pct": 75.77, "operating_margin_pct": 11.73, "fcf_margin_pct": 30.16, "rd_intensity_pct": 27.62, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "PLTR": {"gross_margin_pct": 84.8, "operating_margin_pct": 42.8, "fcf_margin_pct": 54.55, "rd_intensity_pct": 10.42, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "CRM": {"gross_margin_pct": 77.64, "operating_margin_pct": 21.87, "fcf_margin_pct": 34.23, "rd_intensity_pct": 14.38, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "MSFT": {"gross_margin_pct": 67.94, "operating_margin_pct": 46.78, "fcf_margin_pct": 20.19, "rd_intensity_pct": 10.72, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "NOW": {"gross_margin_pct": 74.77, "operating_margin_pct": 11.4, "fcf_margin_pct": 31.03, "rd_intensity_pct": 22.14, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-08-27", "url": "https://www.sec.gov/Archives/edgar/data/1327811/000132781126000044/wday-20260731.htm", "excerpt": "Subscription services revenues accounted for approximately 93% of our total revenues for the three and six months ended July 31, 2026, and represented 97% of our total unearned revenue as of July 31, 2026. Subscription services revenues are driven primarily by the number of customers, the number of workers at each customer, the specific applications subscribed to by each customer, and the price of our applications. The mix of applications to which each customer subscribes can affect our financial performance due to price differentials in our applications. Pricing for our applications varies based on many factors, including the complexity and maturity of the application and its acceptance in the marketplace. New products or services offerings by competitors in the future could also impact the mix and pricing of our offerings. Subscription services revenues are recognized over time as services are delivered, beginning on the date our service is made available to the customer. Our subscription contracts typically have a term of three years or longer and are generally noncancelable. We generally invoice our customers annually in advance for subscription services. We may provide certain customers flexible payment terms and the timing of revenue recognition may differ from the timing of invoicing to our customers. Our professional services consulting engagements are billed on a time and materials or fixed price basis. We generally invoice our customers as the work is performed for time and materials arrangements, and in advance for fixed price arrangements. For contracts billed on a time and materials basis, revenues are recognized over time as the professional services are performed. For contracts billed on a fixed price basis, revenues are recognized over time based on the proportion of the professional services performed. In some cases, we supplement our consulting teams by subcontracting resources from our service partners and deploying them on customer engagements. As the Workday-related consulting practices of our partner firms continue to develop, we expect these partners to increasingly contract directly with our subscription customers for services engagements. Subscription Revenue Backlog Our subscription revenue backlog, which is also referred to as remaining performance obligations for subscription contracts, represents contracted subscription services revenues that have not yet been recognized and includes billed and unbilled amounts.", "note": null}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "items": [{"metric": "總營收（GAAP）", "value": 2649, "unit": "$M", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿 investor.workday.com/news-and-events/press-releases/news-details/2026/Workday-Announces-Fiscal-2027-Second-Quarter-Financial-Results", "vs_consensus": "YoY +12.8%；consensus 約 $2.63B（Zacks，經 finance.yahoo.com 報導轉引），實際超出約 0.6%", "prior_quarter": "Q1 FY2027（季末 2026-04-30）：$2.542B，YoY +13.5%；QoQ +4.2%"}, {"metric": "Non-GAAP 營業利益率", "value": 31.1, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（Non-GAAP operating income $824M／revenue $2.649B）", "vs_consensus": "無揭露單獨市場一致預期；公司同時將 FY27 全年 non-GAAP 營業利益率財測由 Q1 時的 30.5% 上修至 31.0%", "prior_quarter": "Q1 FY2027：31.8%（non-GAAP op income $809M／revenue $2.542B）"}, {"metric": "GAAP 營業利益率", "value": 11.8, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（GAAP operating income $313M／revenue $2.649B；去年同期 $248M／10.6%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：13.3%（GAAP op income $338M／revenue $2.542B）"}, {"metric": "自由現金流（FCF）", "value": 460, "unit": "$M", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（營運現金流 $520M 減資本支出）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：FCF $616M（營運現金流 $696M）；FY27 全年 FCF 財測（Q1 時）約 $3.18B（營運現金流 $3.45B－capex 約 $270M），Q2 未見更新財測數字"}, {"metric": "SBC 占總營收 %", "value": 17.44, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "自算：公司新聞稿揭露 SBC $462M ÷ 總營收 $2.649B", "vs_consensus": null, "prior_quarter": "查無 Q1 FY2027 SBC 金額（未列入本輪 web_search 結果，未填造）"}, {"metric": "FY2027 全年財測（訂閱營收／non-GAAP 營業利益率，隨 Q2 財報上修）", "value": "訂閱營收 $9.940–9.950B（+13% YoY）；non-GAAP 營業利益率 31.0%", "unit": "guidance", "as_of": "Q2 FY2027 財報隨附財測，公告於 2026-08-27", "source": "公司新聞稿 investor.workday.com Q2 FY27 press release", "vs_consensus": null, "prior_quarter": "Q1 FY2027 時財測（2026-05-21）：訂閱營收 $9.925–9.950B（+13%），non-GAAP 營業利益率 30.5%"}, {"metric": "Q3 FY2027 財測（訂閱營收／non-GAAP 營業利益率）", "value": "訂閱營收 $2.515B（+12% YoY）；non-GAAP 營業利益率 30.0%", "unit": "guidance", "as_of": "Q2 FY2027 財報隨附財測，公告於 2026-08-27", "source": "公司新聞稿 investor.workday.com Q2 FY27 press release", "vs_consensus": null, "prior_quarter": null}, {"metric": "cRPO（12個月訂閱營收 backlog）", "value": 9.034, "unit": "$B", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（12-month subscription revenue backlog，YoY +14.2%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：$8.806B，YoY +15.5%（YoY 成長率於 Q2 由 15.5% 降至 14.2%，屬減速訊號）"}, {"metric": "Total RPO（訂閱營收 backlog 總額）", "value": 27.403, "unit": "$B", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（Total subscription revenue backlog，YoY +8.0%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：$27.294B，YoY +10.9%（YoY 成長率於 Q2 由 10.9% 降至 8.0%）"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-09-02 | Workday named a Leader in the 2026 Gartner Magic Quadrant for Cloud HCM Suites for 1,000+ Employee Enterprises for the eleventh consecutive year | Workday Newsroom press release, "Workday Named a Leader in 2026 Gartner Magic Quadrant for Cloud HCM Suites...Eleventh Consecutive Year" (newsroom.workday.com) | moat_trend,thesis.H |
| competitive_share_entrants#1 | - | 2026-08 | In the mid-market segment, Workday most often loses competitive deals to Rippling, HiBob, and Dayforce | Yahoo Finance, "Workday (WDAY) Faces an AI Threat. Is the Investment Case Broken?" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#2 | - | 2026-08 | Some net-new large-enterprise deals are taking longer to close, particularly in Federal, state/local/education (SLED), healthcare, and parts of the commercial market; market is pricing in a software-wide AI reset after Workday's own FY2027 subscription revenue growth guidance slowed to 12%-13% | Yahoo Finance, "Workday (WDAY) Faces an AI Threat. Is the Investment Case Broken?" (citing Workday FY2027 guidance commentary) | thesis.R,decision_inputs.bear,triggers |
| competitive_share_entrants#3 | - | 2026 | Andreessen Horowitz published an essay titled "Workday's Last Workday?" arguing AI agents (that can automate HR/finance workflows directly) pose a structural threat to seat-based SaaS incumbents like Workday | a16z.com, "Workday's Last Workday?" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#4 | + | 2026 | Workday holds roughly 19.8%-23.2% share of the dedicated Human Capital Management (HCM) software market, well ahead of SAP SuccessFactors HCM's ~5% share, per 6sense install-base tracking; FY2026 (ended Jan 2026) subscription revenue reached approximately $8.0 billion, growing ~16% YoY | 6sense, "Workday - Market Share, Competitor Insights in Human Capital Management" (6sense.com/tech/human-capital-management/workday-market-share) | moat_trend,thesis.H |
| competitive_share_entrants#5 | 0 | 2026 | In the broader ERP category (not just HCM), Workday's tracked install-base share (12.81%) trails Microsoft Dynamics (23.59%), SAP ERP (10.97% for legacy ECC) and SAP S/4HANA (9.96%) is close behind | 6sense, "Workday - Market Share, Competitor Insights in Enterprise Resource Planning (ERP)" | moat_trend |
| competitive_share_entrants#6 | 0 | 2026 | SAP SuccessFactors and Workday are described as the two enterprise HRIS finalists in most 2026 RFPs, with Workday generally winning on unified HR+Finance data model and payroll, while SuccessFactors wins where the buyer already runs SAP S/4HANA (ecosystem lock-in) | Redress Compliance, "SAP SuccessFactors vs Workday 2026. HRIS Decision" | moat_trend,thesis.R |
| customer_second_source#0 | 0 | 2026-08 | Workday's gross revenue retention rate remained stable at 97% through Q4 FY2026 and again at 97% in Q2 FY2027, indicating no broad-based customer attrition, second-sourcing, or in-housing trend among the existing customer base during this period | Workday Q4 FY2026 earnings call transcript (Motley Fool, fool.com) and Workday Q2 FY2027 investor materials (investing.com, "Workday Q2 FY27 slides: AI drives 25% of new sales, margins expand") | moat_trend,decision_inputs.bear |
| customer_second_source#1 | 0 | 2026-09-05 | No named large enterprise customer of Workday (e.g. Walmart, CVS Health, McKesson, Apple) was found to have publicly announced adding a second HCM/ERP vendor alongside Workday or moving core HR/Finance systems in-house in 2026 | Multiple queries against news/press-release indexes (erpresearch.com customer list, appsruntheworld.com Workday HCM customer database) returned no such announcement | decision_inputs.bear |
| customer_concentration_credit#0 | 0 | 2025-11-26 | WDAY Q3 FY2026 10-Q（期末2025-10-31）揭露：無單一客戶占總營收比重超過10%，三個月與九個月期間（2025或2024同期）皆同一結論 | https://investor.workday.com/files/doc_financials/2026/q3/WDAY-Workday-Inc-10-Q-2025-11-26-pdf_.pdf | decision_inputs.bear,moat_trend |
| customer_concentration_credit#1 | 0 | 2025-08-21 | WDAY Q2 FY2026 10-Q（期末2025-07-31）揭露：無單一客戶占應收帳款淨額或總營收超過10%（截至2025-07-31或2025-01-31止，及三/六個月期間2025或2024同期） | https://investor.workday.com/files/doc_financials/2026/q2/a690cd13-1e99-40eb-aff7-7e8efb886f75.pdf | decision_inputs.bear,moat_trend |
| supply_demand_durability#0 | - | 2026-05-21 | Cantor Fitzgerald 於2026-05將WDAY目標價由$200下修至$160（維持Overweight），理由為『市場預期偏保守且通路查核顯示中性偏負面』 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | thesis.R,valuation,decision_inputs.bear |
| supply_demand_durability#1 | - | 2026-05-21 | 同篇報導指出結構性疑慮：能自動化HR/財務任務的AI agent可能侵蝕WDAY傳統『按員工人數計費』的訂閱模式；企業正將支出從傳統企業應用重新配置到AI專案 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | thesis.R,moat_trend,decision_inputs.bear |
| supply_demand_durability#2 | - | 2026-05-21 | WDAY股價截至2026-05-21約較年初下跌40%，遠期FY2027本益比約12.3倍，較整體軟體類股折價，反映市場已部分計入AI破壞疑慮 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | valuation,decision_inputs.bear |
| supply_demand_durability#3 | + | 2026-05-21 | WDAY FY2027 Q1（期末2026-04-30，發布於2026-05-21）實績：訂閱營收$23.54億，年增14.3%；12個月訂閱訂單餘額$88.06億，年增15.5%；總訂閱訂單餘額$272.94億，年增10.9%——目前需求動能尚未出現AI替代造成的萎縮跡象 | https://newsroom.workday.com/2026-05-21-Workday-Announces-Fiscal-2027-First-Quarter-Financial-Results | thesis.H,decision_inputs.bear |
| supply_demand_durability#4 | 0 | 2026-05-21 | WDAY FY2027全年財測（2026-05-21發布）：訂閱營收指引$99.25-99.50億，年增12-13%，非GAAP營業利益率上修至30.5% | https://newsroom.workday.com/2026-05-21-Workday-Announces-Fiscal-2027-First-Quarter-Financial-Results | thesis.H |
| supply_demand_durability#5 | 0 | 2026 | 產業研究機構（NextMSC）評估：ERP/HCM雲端＋AI轉型現階段被定性為結構性擴張期而非週期性反彈，美國ERP市場規模預估自2026年約690億美元成長至2030年1180-1250億美元（CAGR 13-14%），但2024-2026年年成長率已降至5%以下，稱為『加速前的暫緩期』 | https://www.nextmsc.com/blogs/how-is-ai-cloud-surge-redrawing-the-2026-erp-software-market | thesis.H,decision_inputs.bear |
| regulatory_antitrust#0 | - | 2026-03-01 | 在 Mobley v. Workday 集體訴訟中，聯邦法官於 2026 年 3 月初裁定原告的《反年齡就業歧視法》(ADEA) 集體訴訟指控可繼續進行，指控 Workday 的 AI 求職者篩選工具對 40 歲以上求職者造成歧視性拒絕。 | The Mobley v. Workday Case Didn't End. It Escalated. Here's Where It Stands. (aigovernanceforhr.com) | decision_inputs.bear,thesis.R |
| regulatory_antitrust#1 | - | 2026-06-22 | 加州法官於 2026 年 6 月 22 日裁定原告在 Mobley v. Workday 案中的加州州法（FEHA）歧視指控可繼續進行，Workday 未能駁回該部分訴訟；法院文件指出 Workday 的求職篩選軟體在涵蓋期間處理約 11 億份工作申請，使單一演算法訴訟可能擴大為大規模集體訴訟。 | Workday can't shake California AI discrimination claims (HR Dive, hrdive.com) | decision_inputs.bear,thesis.R,moat_trend |
| reg_tariff_export | - | - | (status=none；無 findings) |  |  |
| geo_supply_chain#0 | - | 2026-07-31 | Workday 於 SEC 申報（10-Q，期末 2026-07-31）揭露其在全球依賴第三方代管基礎設施夥伴（含 AWS、Google LLC、Microsoft Corporation）提供服務，任一夥伴發生中斷或干擾都可能影響其營運，此列為公司自揭露之風險因子（'Infrastructure Provider Concentration'）。 | Workday, Inc. Form 10-Q FY2026 (SEC EDGAR, https://www.sec.gov/Archives/edgar/data/0001327811/000132781126000044/wday-20260731.htm) | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | + | 2026-07-31 | 為降低單一設施中斷風險，Workday 將應用程式代管於美國、加拿大、歐洲及亞太地區多個第三方資料中心，並有內部程序可在單一設施發生災難時將服務轉移至其他地區——屬多地理區域分散揭露，非單一地緣風險區域集中。 | Workday, Inc. Form 10-Q FY2026 (SEC EDGAR, https://www.sec.gov/Archives/edgar/data/0001327811/000132781126000044/wday-20260731.htm) | thesis.R,decision_inputs.bear |
| end_markets#0 | + | 2025 | [HCM 終端市場] Workday 在 2025 年 HCM（人力資本管理）軟體市場的全球市占率約 22%；Workday、SAP SuccessFactors、Oracle HCM Cloud 三家合計囊括該市場近 58% 營收，Workday 為單一最大廠商。 | Workday 官方引用頁 'Workday US Leads in HCM and Payroll Market Shares'（forms.workday.com）及產業市場研究彙整（Fortune Business Insights／Polaris Market Research HCM market reports） | moat_trend,thesis.H |
| end_markets#1 | + | 2026 | [HCM 終端市場] 全球 HCM 軟體市場規模預估由 2026 年約 $37.52B 成長至 2034 年 $77.37B，2026–2034 CAGR 約 8.5%，成長動能來自 AI 整合與企業雲端採用擴大。 | Fortune Business Insights, 'Human Capital Management (HCM) Market Size, Share'（fortunebusinessinsights.com） | thesis.H,growth,valuation |
| end_markets#2 | + | 2025 | [Financial Management 終端市場] Workday Financial Management 所屬之財務管理軟體市場規模預估由 2025 年約 $3.92B 成長至 2034 年 $10.47B，2026–2034 CAGR 約 11.5%；北美為最大區域市場，2025 年規模約 $1.50B（占 38.2%）。 | Verified Market Reports, 'Global Workday Financial Management Service Market Size, Industry Share, Growth Trends & Forecast 2026-2034'（verifiedmarketreports.com） | thesis.H,growth |
| end_markets#3 | + | 2026-01-31 | [整體訂閱營收] Workday 整體訂閱服務營收（涵蓋 HCM 與 Financial Management 等產品線，公司未於申報中拆分個別產品線營收）FY2026 較 FY2025 成長 14.45%，自 $7.72B 增至 $8.83B。 | Bullfincher, 'Workday Revenue Breakdown By Segment'（bullfincher.io）；與 Workday FY2026 全年財報新聞稿一致 | thesis.H,growth,valuation |
| end_markets#4 | + | 2025-11-25 | [AI/Illuminate 產品線] Workday FY2026 Q3 財報（發布日 2025-11-25）法說指出 Illuminate AI agents 與企業端解決方案為當季營收成長動能之一，公司該季財報優於分析師預期並上修全年 non-GAAP 營益率展望。 | Workday newsroom, 'Workday Announces Fiscal 2026 Third Quarter Financial Results'（newsroom.workday.com, 2025-11-25）；InfotechLead, 'Workday AI Powers Q3 Fiscal-2026 Revenue Growth with Illuminate Agents and Enterprise Solutions' | thesis.H,growth |
| end_markets#5 | + | 2025-09-16 | [Adaptive Planning / Illuminate 產品線] Workday 於 2025-09-16 宣布擴大 Illuminate AI agents 陣容至 HR、Finance 與特定產業；其中 Adaptive Planning 的 Planning Agent 在早期使用客戶端可將資料探索與分析所需時間減少約 30%（約每月 100 小時）。 | Workday newsroom, 'Workday Illuminate™ Expands with New AI Agents for HR, Finance, and Industry'（newsroom.workday.com, 2025-09-16）；CFO Shortlist, 'Workday Adaptive Guide 2026: Enterprise FP&A' | thesis.H,growth |
| end_markets#6 | + | 2026-05-21 | [AI ARR 整體] Workday AI 相關年化經常性收入（AI ARR）已突破 $400M，年增率達三位數（triple-digit YoY）；報導與公司近期一次 Q1 財報（法說會 2026-05-21）AI agent 動能揭露同期。 | ERP Today, 'Workday's AI Agent Push Started Showing Up in its Q1 Earnings Numbers'（erp.today） | thesis.H,growth,valuation |
| substitute_technology#0 | - | 2026-02-25 | Workday stock fell sharply despite beating Q4 estimates as investors priced in fears that agentic AI could erode the seat-based licensing model underlying Workday's HCM/finance suite. | FinancialContent/MarketMinute, "The SaaSpocalypse of 2026: Workday Stock Plummets as Agentic AI Fears Overshadow Q4 Beat" | thesis.R,decision_inputs.bear,moat_trend |
| substitute_technology#1 | - | 2026-02-24 | Analyst commentary framed early 2026 as an 'AI inflection point' for Workday, with post-earnings volatility driven by questions over whether agentic AI substitutes could take over HR/Finance workflow tasks Workday currently monetizes per seat. | FinancialContent/Finterra, "The AI Inflection Point: A Deep Dive into Workday (WDAY) Amid Post-Earnings Volatility" | thesis.R,valuation |
| substitute_technology#2 | - | 2025-08-26 | Commentary noted that AI tools can automate tasks previously performed by employees, which directly threatens Workday's seat-based pricing model since licensing revenue is linked to headcount that AI adoption could shrink. | The Motley Fool, "Workday: Are AI Disruption Fears Real? Should You Buy the Stock?" | thesis.R,moat_trend,decision_inputs.bear |
| channel_business_model_shift#0 | + | 2025-11-19 | Workday announced an expansion of Workday GO, an all-in-one packaged offering aimed at businesses of all sizes (not just large enterprise), with the next release (Deployment Agent, Workday GO Global Payroll, Workday GO Partner Network integrations) rolling out February 2026 across the U.S., Canada, U.K., Ireland, Germany and additional regions — a structural shift from Workday's historical large-enterprise direct-sales motion toward a packaged, partner-resold mid-market channel. | Workday Newsroom press release, "Workday Expands Workday GO, the All-in-One 'Workday for All' Solution, to Support Businesses of All Sizes" | thesis.H,valuation |
| channel_business_model_shift#1 | 0 | 2025-11-21 | The Workday GO Partner Network launch includes named implementation/resale partners (TopBloc, Benefit Harbor, BNB, HR Path, Kainos, OneSource Virtual, Remote, Three Link Solutions) selling a lighter version of Workday to mid-market companies that don't need the full enterprise suite, indicating Workday is deliberately building a partner-led go-to-market layer distinct from its traditional direct enterprise sales force. | Enterprise Times, "Workday targets medium sized businesses to Grow with Workday Go" | thesis.H,decision_inputs.bear |
| capital_markets_pricing#0 | + | 2026-08-27 | Workday 2026-08-27公布FY2027第二季財報時上修FY2027訂閱營收指引至$9.940B–$9.950B(年增13%)，並將FY2027 non-GAAP營業利益率指引上修至31.0%；當季agentic AI產品新增ACV逾$100M，占當季全部新簽ACV逾25%。 | Workday newsroom press release 'Workday Announces Fiscal 2027 Second Quarter Financial Results' (newsroom.workday.com), 2026-08-27 | thesis.H,decision_inputs.bear,valuation |
| capital_markets_pricing#1 | 0 | 2026-08-27 | 財報公布當日(2026-08-27)股價收$193.57(+1.48%)，盤後波動輕微；報導解讀為市場視此次優於預期結果為『穩健執行』而非驚喜，反應偏中性。 | Investing.com, 'Workday Q2 FY27 slides: AI drives 25% of new sales, margins expand' | valuation,triggers |
| capital_markets_pricing#2 | 0 | 2026-09-01 | 財報後約一週內(2026年8月底至9月初)賣方目標價出現同時上修與下修：BTIG降評至中立(原買進)並撤回原$175目標價；Deutsche Bank降評至持有並下修目標價至$145(原$185)；Goldman Sachs上修目標價至$164(原$151)；Cantor Fitzgerald維持增持評等但下修目標價至$205(原$220)；Bernstein上修目標價至$238並維持優於大盤評等，理由為利益率展望轉正與FY2027指引更新。目標價區間$145–$238 vs numbers.price_at_dd，顯示賣方對本次財報後估值方向的分歧擴大。 | Investing.com/Yahoo Finance/Benzinga analyst-ratings coverage aggregated in 'These Analysts Revise Their Forecasts On Workday Following Q2 Results' (Benzinga) and 'Cantor Fitzgerald cuts Workday stock price target on guidance miss' (Investing.com) | valuation,thesis.R,decision_inputs.bear |
| capital_markets_pricing#3 | 0 | 2026-09-05 | 不同資料源對賣方目標價共識落差異常大：一來源引S&P Global統計41位分析師均值目標價$188.21、共識評等Buy；另一來源(51位分析師)則引中位數目標價達$280(區間$92–$326)。兩者中樞相差逾$90，反映Q2財報後賣方對合理估值的看法高度不一致，目標價區間本身 vs numbers.price_at_dd 需謹慎解讀。 | MarketScreener 'Workday Inc.: Target Price Consensus and Analysts Recommendations'; stockanalysis.com 'Workday (WDAY) Stock Forecast & Analyst Price Targets' | valuation,decision_inputs.bear |
| major_events#0 | + | 2026-08-13 | Reuters 於 2026-08-13 報導私募股權公司 Silver Lake 正與 Workday 洽談收購，消息帶動股價一度盤中飆漲近 30%、觸發交易暫停，市值一度推升至逾 $51B；Reuters Breakingviews 模擬每股 $227（30% 收購溢價）的假設性報價，隱含約 $53.8B 估值（約 2027E 營收 5 倍），交易仍在洽談中未有定案 | CNBC "Workday shares post best day in 10 years on Silver Lake takeover report" (2026-08-13); Axios "Silver Lake eyes Workday take-private" (2026-08-14) | triggers,capital_markets_pricing,decision_inputs.bear |
| major_events#1 | 0 | 2025-09-16 | Workday 於 2025-09-16 簽署最終協議以約 $1.1B 收購 AI 招募新創 Sana，預計於 Workday FY2026 第四季（截至 2026-01-31）完成交割 | Workday Newsroom "Workday Signs Definitive Agreement to Acquire Sana"; Workday Form 8-K (SEC EDGAR, filed 2025-09-16) | moat_trend,thesis.H |
| major_events#2 | 0 | 2025-11-01 | Workday 另收購求職者體驗 AI agent 公司 Paradox（AI 招募），預計於 Workday FY2026 第三季（截至 2025-10-31）完成交割；同期間亦於 2025 年 11 月收購雲端 API 整合平台 Pipedream | TipRanks "Workday announces acquisition of AI firm Paradox"; SeekingAlpha "Workday to acquire candidate experience AI agent Paradox"; Tracxn acquisitions list | moat_trend,thesis.H |
| major_events#3 | - | 2025-08-26 | Workday 於 2025-08-23 確認發生資料外洩事件，起因於第三方應用程式 Salesloft Drift（串接 Salesforce）遭駭客竊取 OAuth 憑證並用於在客戶 Salesforce 環境內執行搜尋；外洩範圍限於商業聯絡資訊、支援案件細節、租戶屬性（如 tenant/data center 名稱、產品名稱、服務、訓練紀錄、事件日誌），Workday 強調核心客戶租戶本身未被直接存取或入侵；此為波及逾 700 家組織的供應鏈級外洩事件（Salesloft Drift OAuth 憑證遭竊），Google、Salesloft 等多家公司同批受影響 | cybersecuritynews.com "Workday Confirms Data Breach"; BlackFog "The Salesforce Breach Wave Of 2025" | thesis.R,decision_inputs.bear |
| major_events#4 | - | 2025-09-01 | 因 2025 年 Salesloft Drift／Salesforce 資料外洩事件，已有消費者集體訴訟指控 Workday 與 Salesforce 未能妥善保護消費者個資，該訴訟於加州聯邦法院提出 | topclassactions.com "Workday, Salesforce class action claims companies failed to protect consumer data" | thesis.R,decision_inputs.bear |
| major_events#5 | - | 2026-08-19 | 受 Silver Lake 潛在收購案消息影響，多家股東權益律所（Kaskela Law、Schall Brown & Schwartz LLP、SBS Law）於 2026-08 中旬起宣布對 Workday 展開調查，主旨在確認若公司出售給 Silver Lake，董事會是否已善盡受託責任、股東是否能取得足額對價；此類為律所徵求潛在原告的訴前調查公告，非法院已受理之集體訴訟判決，且與傳統財報不實型證券詐欺求償性質不同 | BusinessWire "WDAY Investors Have Opportunity to Join Workday, Inc. Fraud Investigation with SBS Law" (2026-08-16); BusinessWire "Kaskela Law Firm Announces Investigation of Workday, Inc. (WDAY)" (2026-08-19) | triggers,decision_inputs.bear |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "Workday WDAY acquisition merger 2025 2026",
   "Workday Silver Lake acquisition talks buyout August 2026"
  ],
  "findings": [
   {
    "claim": "Reuters 於 2026-08-13 報導私募股權公司 Silver Lake 正與 Workday 洽談收購（take-private），消息帶動股價盤中一度飆漲近 30%、觸發交易暫停，市值一度推升至逾 $51B；Breakingviews 模擬假設性報價每股 $227（30% 溢價）隱含約 $53.8B 估值，若成交將為軟體業史上最大收購案之一，交易仍在洽談中、無成交保證",
    "source": "CNBC \"Workday shares post best day in 10 years on Silver Lake takeover report\" (2026-08-13); Axios \"Silver Lake eyes Workday take-private\" (2026-08-14)",
    "as_of": "2026-08-13",
    "direction": "+",
    "affects": [
     "triggers",
     "capital_markets_pricing",
     "decision_inputs.bear"
    ]
   },
   {
    "claim": "Workday 於 2025-09-16 簽署最終協議以約 $1.1B 收購 AI 招募新創 Sana（預計 FY2026 Q4 交割），另收購 Paradox（AI 求職者體驗 agent，預計 FY2026 Q3 交割）與 Pipedream（雲端 API 整合平台，2025-11 完成），為近 12 個月內三筆已公告/完成之併購案",
    "source": "Workday Newsroom \"Workday Signs Definitive Agreement to Acquire Sana\" (2025-09-16); TipRanks \"Workday announces acquisition of AI firm Paradox\"",
    "as_of": "2025-09-16",
    "direction": "0",
    "affects": [
     "moat_trend",
     "thesis.H"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "found",
  "queries_run": [
   "Workday WDAY class action lawsuit securities fraud",
   "Workday data breach 2025 Salesforce Drift customer data compromised"
  ],
  "findings": [
   {
    "claim": "因 2025 年 Salesloft Drift／Salesforce 資料外洩事件，已有消費者集體訴訟指控 Workday 與 Salesforce 未能妥善保護消費者個資，該訴訟於加州聯邦法院提出",
    "source": "topclassactions.com \"Workday, Salesforce class action claims companies failed to protect consumer data\"",
    "as_of": "2025-09-01",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear"
    ]
   },
   {
    "claim": "受 Silver Lake 潛在收購案消息影響，多家股東權益律所（Kaskela Law、Schall Brown & Schwartz LLP、SBS Law）於 2026-08 中旬起宣布對 Workday 董事會展開受託責任調查（訴前徵求潛在原告階段，尚非已受理之集體訴訟），聚焦股東若出售給 Silver Lake 是否取得足額對價",
    "source": "BusinessWire \"WDAY Investors Have Opportunity to Join Workday, Inc. Fraud Investigation with SBS Law\" (2026-08-16); BusinessWire \"Kaskela Law Firm Announces Investigation of Workday, Inc. (WDAY)\" (2026-08-19)",
    "as_of": "2026-08-19",
    "direction": "-",
    "affects": [
     "triggers",
     "decision_inputs.bear"
    ]
   }
  ],
  "note": ""
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Workday WDAY FDA clinical trial approval drug device 2025 2026",
   "Workday clinical trial FDA approval 2025 2026"
  ],
  "findings": [],
  "note": "非藥品/器材業務，已查證無相關監管動作（Workday 為人力資本/財務管理雲端軟體公司，非藥廠或醫材商，查無 FDA 或臨床試驗相關事項）。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Workday WDAY product recall outage warning letter regulatory 2025 2026",
   "WDAY product launch recall warning letter"
  ],
  "findings": [],
  "note": "查無 Workday 產品召回或主管機關警告信紀錄；唯一相關資安事件（Salesloft Drift 第三方外洩）已列入 lawsuit_class_action 與 major_events 軸，性質為資料外洩非產品召回。"
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Workday WDAY SEC investigation restatement",
   "Workday accounting restatement SEC enforcement action 10-K amendment"
  ],
  "findings": [],
  "note": "查無 Workday 遭 SEC 正式調查或財報重編紀錄；股東權益律所所稱之「investigation」為私人律所徵求潛在原告之訴前調查（與 Silver Lake 收購案受託責任相關），非 SEC 主管機關調查，已另列於 lawsuit_class_action。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_WDAY_20260522.html",
 "date": "20260522",
 "schema": "v12.4",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 121.85,
 "revlog": {
  "status": "unavailable"
 },
 "prior_meta": {
  "ticker": "WDAY",
  "schema": "v12.4",
  "date": "2026-05-22",
  "price_at_dd": 121.85,
  "currency": "USD",
  "market_cap_b": 30.4,
  "signal": "B",
  "trap": "🟢",
  "trap_label": "非陷阱",
  "moat": "B",
  "moat_score": 8.0,
  "moat_execution": 7,
  "moat_pricing_power": 9,
  "val": "🟢",
  "ma": "🟠",
  "ai_risk": "🟡",
  "industry_wind": "🟡",
  "fpe_fy1": 11.58,
  "fpe_fy2": 9.79,
  "pct_5y": 3,
  "peg_fy2": 0.93,
  "peg_3y": 0.71,
  "peg_5y": 0.64,
  "eps_cagr_3y": 16.4,
  "eps_source": "yfinance (FY+1/+2 consensus, FY+3 §8 logic; not in Excel snapshot)",
  "fcf_margin": 29.1,
  "nrr": 110,
  "rr_short": 2.1,
  "rr_mid": 3.76,
  "rr_5y": 9.87,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "upside_short_pct": 47,
  "upside_mid_pct": 84,
  "upside_5y_pct": 220,
  "target_short": 178.8,
  "target_mid": 224.1,
  "target_5y": 390.0,
  "bear_price": 94.7,
  "growth_durability": 8,
  "quality_score": 8,
  "long_term_confidence": "高",
  "verdict": "B 觀望（thesis 完整、估值極便宜，但 Pure MA 🟠 暫不；待站回 W104 後 4 週確認）",
  "inception_dd": "DD_WDAY_20260522.html",
  "inception_date": "2026-05-22",
  "oneliner": "WDAY 5Y 分位 3%／PEG 0.71／Q1 FY27 Op Margin 1.8%→13.3%＋cRPO +15.5%加速＋Bhusri 回鍋 reset．護城河 B(8) 估值🟢+1→A；MA ❌→🟠盲點2救援．訊號 B 觀望，等站回 W104($220) 後 4 週進場．"
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
    "text": "cRPO（12 個月 sub rev backlog）持續加速 — Workday 業務動能未被 AI native 蠶食，enterprise 換代週期仍持續",
    "columns": {
     "2Y 驗證點": "Q2-Q4 FY27 cRPO YoY ≥ 13.5%（公司 guide）",
     "5Y 驗證點": "FY29 cRPO 達 -B+（從 FY26 .85B 起算 18% CAGR）",
     "10Y 驗證點": "FY31 sub rev .5-22B（10Y 從 FY26 .4B 起算 12% CAGR）",
     "具體數字門檻": "FY27 全年 cRPO 退出 ≥ 14% YoY；FY28 sub rev guide 仍 ≥ +11%",
     "信息來源": "WDAY Q1 FY27 8-K + 5/21 earnings call",
     "漂移觸發條件": "連 2 季 cRPO YoY &lt; 12% → 削弱（2Y 假設適用 QC-34 季節性、QC-35 漂移分級）"
    }
   },
   {
    "id": "H2",
    "text": "Non-GAAP Operating Margin 持續擴張至 35%+ — operational leverage 兌現，Bhusri reset 後 OpEx 紀律",
    "columns": {
     "2Y 驗證點": "FY27 退出 Non-GAAP OpMargin ≥ 31%（vs guide 30.5%）",
     "5Y 驗證點": "FY29 Non-GAAP OpMargin ≥ 33-34%",
     "10Y 驗證點": "FY31 Non-GAAP OpMargin 達 35%+ steady state",
     "具體數字門檻": "FY27 退出率 ≥ 30.5%；FY28 入場 guide ≥ 31%；R&D opex YoY ≤ rev YoY",
     "信息來源": "WDAY FY27 guide raised + 5/21 earnings call",
     "漂移觸發條件": "連 2 季 Non-GAAP OpMargin YoY 下降 ≥ 100bp → 削弱"
    }
   },
   {
    "id": "H3",
    "text": "Illuminate Agents 平台從 4,000 → 10,000+ active 客戶 — AI 戰略 兌現，pricing power 護城河加深",
    "columns": {
     "2Y 驗證點": "Q4 FY27 Illuminate active customer ≥ 8,000（QoQ 持續加倍）",
     "5Y 驗證點": "FY29 全客戶基數中 ≥ 60% 用 Illuminate（vs 現 ~20%）",
     "10Y 驗證點": "Illuminate ARR 成為獨立 line item 揭露 ≥ -B",
     "具體數字門檻": "連 2 季 Illuminate active customer QoQ &lt; 50% growth → 削弱；連 2 季客戶數絕對下降 → 反轉",
     "信息來源": "5/21 earnings call Bhusri 開場聲明",
     "漂移觸發條件": "2Y 假設適用 connected 2 quarter rule；5Y 假設適用 4 季滯後"
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
    "text": "AI native HRIS 突破 enterprise 上岸戰，連續 3 季搶下大型客戶",
    "columns": {
     "對應假設": "H1",
     "時間尺度": "🔥 中期（4-6 季）",
     "監測指標": "競爭對手公開報導的 enterprise wins；Workday 新客戶 ACV 趨勢",
     "警戒閾值": "Rippling/Deel 任一拿下 ≥ -50M ACV 公開案例 ≥ 2 件；Workday 新客戶 ACV 連 2 季 YoY 下降"
    }
   },
   {
    "id": "R2",
    "text": "OpEx 紀律失守，Bhusri 在「AI reset」名義下擴張研發費用",
    "columns": {
     "對應假設": "H2",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "R&D / Sales OpEx YoY% vs Revenue YoY%",
     "警戒閾值": "連 2 季 R&D + S&M OpEx YoY% &gt; Rev YoY%；FY27 退出 Non-GAAP OpMargin &lt; 29%"
    }
   },
   {
    "id": "R3",
    "text": "Bhusri 接班 / 治理連續性失效，hyperscaler 自建 in-house HCM agent",
    "columns": {
     "對應假設": "H3",
     "時間尺度": "🐢 長期（2+ 年慢變數）",
     "監測指標": "2027/2 FY28 sub rev guide 是否仍能 raise；Apple/MSFT/AMZN 是否公告 in-house HCM",
     "警戒閾值": "Bhusri 在 2027/2 前未公布 permanent successor（≥ 50% 機率才砍倉）；任一 hyperscaler 公告 in-house HCM 計畫"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_WDAY_20260522.html",
  "date": "20260522",
  "schema": "v12.4"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_WDAY_20260522.html",
  "date": "20260522",
  "days_from_365d_mark": 259
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "WDAY",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-05-22",
  "freshness": "aging",
  "source": "docs/dd/DD_WDAY_20260522.html"
 },
 "decision_history": [
  {
   "date": "2026-05-22",
   "verdict": null,
   "role": null,
   "price_at_decision": 121.85,
   "fundamental_grade": "B",
   "to_date_pct": 52.79,
   "days": 101,
   "source_report": "docs/dd/DD_WDAY_20260522.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/WDAY.md\n[dd] 2026-05-22  DD|WDAY Workday|2026-05-22|v12.4\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_WDAY_20260522.md\n[dca] 2026-05-22  DCA|WDAY Deep Conviction Analysis|2026-05-22\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_WDAY_20260522.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "ok",
 "primary": {
  "theme": "生產力 Copilot / AI 辦公整合",
  "path": "docs/id/ID_ProductivityCopilot_20260427.html",
  "skill_version": "v2.3",
  "as_of": "2026-04-27",
  "facts": {
   "status": "ok",
   "sections": {
    "supply": "PART III · SUPPLY SIDE\n 供給側：分發玩家矩陣，利潤往捆綁與資料集中\n 反直覺但可操作的結論：生產力 AI 的利潤往「握分發通路 + 專屬資料 + 成功轉型計費」的 incumbent 集中——純單點工具被免費捆綁與 agent 取代。\n\n 供給端是「分發 incumbent + 垂直專屬資料 + 受脅單點」三層。分發 incumbent：Microsoft（365 Copilot，345M 席次基底的捆綁）、Google（Workspace + Gemini 免費捆綁）——它們把 AI 內建進已有的 office suite，分發成本近零。垂直專屬資料：Salesforce（Slack + Agentforce per-action）、Adobe（Acrobat AI）、Atlassian（Rovo）、Workday（Illuminate HR/財務）、DocuSign（Iris 合約）——靠專屬資料與工作流守住。受脅單點：Zoom（AI Companion 免費送）、HubSpot（mid-market 被擠）——難對 AI 單獨收費。利潤明顯往「分發 + 專屬資料 + 成功轉計費」集中。\n\n \n Inference · 供給\n 分發 incumbent 與專屬資料者贏，純單點工具被吞\n 前提：分發 incumbent 近零成本捆綁 AI（MSFT/GOOGL）+ 專屬資料/workflow 高轉換成本（CRM/ADBE/WDAY）+ 單點工具無護城河、被免費捆綁/agent 取代 + 計費轉 consumption → 利潤往分發端 + 專屬資料端集中\n 當 AI 變成 suite 的內建功能，分發 incumbent（MSFT/GOOGL）靠既有席次基底近零成本獲客；握專屬資料與工作流者（CRM/ADBE/WDAY/TEAM）有高轉換成本、且能轉 consumption/outcome 計費；純單點工具（會議、筆記、mid-market CRM）對 AI 功能很難單獨收費，被免費捆綁與 agent 取代。MSFT 365 Copilot 20M 席次（產品有機成長、非併購灌入）證明分發捆綁的威力。\n 可證偽條件：若某純 AI-native 生產力新創用「跨 suite、AI-first」獨立長成大廠（不被捆綁吞），或開源/通用 agent 讓專屬資料優勢被抹平，則「分發+資料集中」論的某一面失效。\n \n\n \n 分發玩家矩陣 · 定位與動能\n \n玩家 | 定位 / 最新動能 | 遷移 | 角色\nMSFT | 365 Copilot 20M 席次、Cowork 計量計費 | ↑ | 分發王（捆綁 + 轉 consumption）\nGOOGL | Workspace + Gemini 免費捆綁 | ↑ | 分發 + 多雲 agentic\nCRM / ADBE / TEAM | Agentforce per-action / Acrobat AI / Rovo | ↑ | 專屬資料 + 轉型計費先驅\nDOCU / BOX / WDAY | 合約 / 文件 / HR 專屬資料 AI | ↑ | 垂直專屬資料\nZM / HUBS | AI Companion 免費 / mid-market 被擠 | ↓ | 單點受脅（捆綁/agent）\n\n \n 怎麼讀：分發 incumbent（MSFT/GOOGL）與專屬資料者（CRM/ADBE/TEAM/DOCU/BOX/WDAY）在 ↑，純單點工具（ZM/HUBS）在 ↓（被免費捆綁/agent 擠）。成本曲線省略說明：軟體無實體產能成本曲線；但有關鍵變動成本——Copilot 背後的推論 token 成本（見子題「Token 經濟學」），這正是逼著計費從 per-seat 轉 consumption 的根源。",
    "demand": "PART IV · DEMAND SIDE\n 需求側：採用爆發 vs ROI gap 的落地缺口\n 需求最剛性的是「員工已經在用 AI」——88% 員工常用、20M 付費席次；但最大的變數是「用了不等於有 ROI」——僅 39% 認得到可量化 EBIT 影響，落地門檻高。\n\n 第一引擎：採用爆發（現需）。需求已從試點變成普及：MSFT 365 Copilot 付費席次破 2,000 萬、單季 +500 萬、逾 60% Fortune 500 有 ≥1 萬席、Copilot 每用戶查詢數季增近 20%、每週使用黏著度已達 Outlook 等級。員工要的是「嵌在既有工作流裡、自動做掉雜事」。第二引擎：ROI gap（反需求/篩選器）。同時微軟自己的 Work Trend Index 顯示：88% 員工常用 AI、但只有 39% 認得到可量化的 EBIT 影響（49pp 落差）；AI 工具的「licensed 席次 vs active 使用」落差是所有軟體裡最大的。這個缺口既篩掉「買了沒用」的虛胖席次，也創造「證明 ROI、變更管理、agent 治理」的新需求。\n\n \n 需求三角驗證 · 採用 vs 營收 vs ROI\n \n視角 | 數值 | 口徑\n採用（bottom-up） | M365 Copilot 20M 付費席次（T1）、60% F500 ≥10k 席（第三方） | MSFT 法說 + 第三方統計\n營收 run-rate | ~$7.2B 年化（折扣後估 $1.5–2.5B real） | 推估（折扣 40–60%）\n落地篩選器 | 88% 用 AI / 僅 39% 有 EBIT 影響（49pp） | MSFT Work Trend Index\n\n \n 怎麼讀：採用（20M 席次）證明需求真實、分發 incumbent 吃得到；但 run-rate 名目（$7.2B）與折扣後實際（$1.5–2.5B）差很大、ROI gap（88%/39%）說明「用了不等於有價值」。採信「付費席次 + EBIT 兌現」作需求真實性的最硬證據，而非名目 run-rate。\n\n \n 多空為何都對\n 多頭測的是採用需求（20M 席次、88% 用、黏著度等同 Outlook），這幾乎沒爭議；空頭測的是商業模式與 ROI（per-seat→consumption 相變、seat compression、ROI gap 49pp）。兩者可同時為真：採用是真爆發（多頭對），但 per-seat 模式被自家 agent 侵蝕、且多數企業還沒兌現 EBIT（空頭對）。本報告因此把重心放在「模式相變下誰捕獲價值」，而非「Copilot 會不會被採用」。"
   }
  },
  "machine": {
   "sd_verdict": "balanced",
   "clock_phase": "II",
   "priced_in": null,
   "conviction": "high",
   "for_stage2_only": true
  }
 },
 "candidates": [
  {
   "theme": "生產力 Copilot / AI 辦公整合",
   "path": "docs/id/ID_ProductivityCopilot_20260427.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-27",
   "sd_verdict": "balanced",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  },
  {
   "theme": "Agentic AI 平台",
   "path": "docs/id/ID_AgenticAIPlatform_20260903.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-03",
   "sd_verdict": "split",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "mid",
   "for_stage2_only": true
  }
 ],
 "note": "primary 由 conviction desc + publish_date desc 排序機械選出，非人工裁定——ticker 掛在多個產業主題下時，Stage 1 判斷層應覆核 candidates 是否有更貼題者。"
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/WDAY/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "Workday raised FY26 subscription revenue guidance to $8.815 billion, 14% growth, reflecting the Paradox acquisition impact.",
      "quote": "FY '26 subscription revenue guidance to $8.815 billion",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "Zane Rowe gave Q3 FY26 subscription revenue guidance of approximately $2.235 billion, also 14% growth.",
      "quote": "expect Q3 FY '26 subscription revenue to be approximately",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "Zane Rowe guided Q3 cRPO growth of 15%-16%, explicitly excluding the Paradox acquisition impact.",
      "quote": "We expect cRPO to increase between 15% and 16% in Q3.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Carl Eschenbach stated Q2 non-GAAP operating margin was 29%, alongside 14% subscription revenue growth.",
      "quote": "non-GAAP operating margin of 29%",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Zane Rowe raised FY26 non-GAAP operating margin guidance to approximately 29%, citing ongoing efficiencies.",
      "quote": "our FY '26 non-GAAP operating margin to approximately 29%",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Zane Rowe guided Q3 non-GAAP operating margin of 28%, and noted GAAP margins run ~17-21 points lower.",
      "quote": "For Q3, we expect non-GAAP operating margin of 28%.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday repurchased $299 million of shares during the quarter.",
      "quote": "repurchased $299 million of our shares during the quarter",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday ended the quarter with $8.2 billion in cash and marketable securities.",
      "quote": "$8.2 billion in cash and marketable securities",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday had $1.2 billion in remaining buyback authorization as of July 31.",
      "quote": "$1.2 billion in remaining authorization as of July 31",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Workday signed a definitive agreement to acquire Paradox, a conversational-AI candidate experience agent, expected to close in Q3.",
      "quote": "signed a definitive agreement to acquire Paradox",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Carl Eschenbach disclosed Workday also recently acquired Flowise, a low-code platform for building AI agents.",
      "quote": "we also recently acquired Flowise, a leading low-code",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Workday launched Workday Government as a wholly owned subsidiary dedicated to the U.S. government sector.",
      "quote": "we launched Workday Government, a wholly owned subsidiary",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "competition",
      "claim": "Responding to a question about AI-driven SaaS disruption, Carl Eschenbach called the negative impact on seat-based models overblown.",
      "quote": "impact on seat-based models are completely overblown",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "competition",
      "claim": "Carl Eschenbach cited winning customers in Germany located near larger competitors' home base as evidence of international competitive strength.",
      "quote": "right in the backyard of some of our bigger competitors",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Carl Eschenbach acknowledged a headwind in the state and local government portion of the SLED business.",
      "quote": "we did see a little bit of headwind in that market",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Carl Eschenbach flagged that higher education customers are under funding pressure, including loss of federal funding.",
      "quote": "higher ed is clearly under pressure",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Despite analyst questions about tariffs and geopolitical cross-currents, Carl Eschenbach said Workday has not seen international macro headwinds this quarter.",
      "quote": "we haven't necessarily seen any blowback or headwinds",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "customer",
      "claim": "Carl Eschenbach stated Workday serves more than 65% of the Fortune 500.",
      "quote": "We are proud to serve more than 65% of the Fortune 500",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "customer",
      "claim": "Zane Rowe reported gross revenue retention remained healthy at 97%.",
      "quote": "gross revenue retention rates remained healthy at 97%.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "commitment",
      "claim": "Zane Rowe reaffirmed Workday is tracking well against deliverables tied to the previously flagged DIA (Defense Intelligence Agency) contract.",
      "quote": "talked all year long about the deliverables tied to the DIA",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "commitment",
      "claim": "Zane Rowe said management will host a Financial Analyst Day on September 16 to share the framework for future growth and margin expansion.",
      "quote": "our upcoming Financial Analyst Day on September 16",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 FY26 訂閱營收指引 $8.828B、成長 14%",
      "quote": "FY '26 subscription revenue of $8.828 billion, growth of 14%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 Q4 訂閱營收指引 $2.355B、成長 15%",
      "quote": "subscription revenue of $2.355 billion, growth of 15%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 重申 FY27 訂閱營收成長約 13%（與 9 月 Analyst Day 一致）",
      "quote": "subscription revenue growth of approximately 13%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明 Q3 non-GAAP 營益率為 28.5%",
      "quote": "a non-GAAP operating margin of 28.5%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 給出全年 non-GAAP 營益率指引約 29%",
      "quote": "approximately 29% for the full year",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 說明 Q3 執行庫藏股買回 $803M",
      "quote": "repurchasing $803 million of our shares during the quarter",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 說明未來將再買回 $3.6B，累計達 $5B 總回購目標",
      "quote": "leading to $5 billion in total repurchases",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 揭露截至 10/31 現有授權額度剩餘 $4.4B",
      "quote": "$4.4 billion remaining under our current authorization",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 上修 FY26 營運現金流指引至 $2.90B",
      "quote": "operating cash flow outlook to $2.90 billion",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說明超過 75% 核心客戶正在使用 Workday Illuminate AI",
      "quote": "our core customers are using Workday Illuminate AI",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "product",
      "claim": "CEO 提到今年平台上 AI actions 已超過 10 億次",
      "quote": "well over 1 billion AI actions on the Workday platform",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 指出 Q3 一半以上全球新簽約同時包含 HR 與財務模組",
      "quote": "all net new global deals in Q3 included both HR and finance",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 指出客戶端員工人數持續溫和成長",
      "quote": "our customers' headcount levels continued to grow modestly",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 在 Q&A 重申客戶群整體人數年增率為正",
      "quote": "the headcount of our customer base is up year-over-year",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "risk",
      "claim": "CEO 承認高度依賴聯邦補助的機構（主要是高等教育）出現個別衝擊",
      "quote": "institutions that rely heavily on federal grants",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 承認聯邦與 SLED 業務因財政資金問題受到一些衝擊",
      "quote": "did see some impact in Fed and SLED tied to fiscal funding",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 回應分析師關於 AI 新創威脅的提問，重申上季說法是對的",
      "quote": "a completely overblown narrative, and I thought it was flat",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 主張客戶最終還是回頭選擇他們信任的既有供應商",
      "quote": "they're ultimately coming back to the vendors they trust",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 舉例一家保險公司回頭簽下全套 10 年合約",
      "quote": "choosing our full suite with a 10-year commitment",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 提到正就 DIA 平台擴大合作進行下一階段洽談",
      "quote": "negotiating a follow-on to take that platform to the next",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives FY27 subscription revenue guidance range.",
      "quote": "$9.925 billion to $9.950 billion, growth of 12% to 13%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives Q1 FY27 cRPO growth guidance range.",
      "quote": "cRPO to increase between 14.5% and 15.5% in Q1",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO gives FY27 non-GAAP operating margin guidance.",
      "quote": "non-GAAP operating margin of approximately 30%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO says the FY27 margin outlook reflects stepped-up AI investment spend.",
      "quote": "an accelerated pace of AI investment",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO attributes part of Q4 margin strength to a slower hiring ramp.",
      "quote": "a slightly slower ramp in hiring",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses Q4 share repurchase amount.",
      "quote": "We repurchased $1.5 billion of our shares",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses remaining buyback authorization at quarter end.",
      "quote": "$2.9 billion in remaining authorization",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses year-end cash and marketable securities balance.",
      "quote": "$5.4 billion in cash and marketable securities",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products cites full-year AI action volume across the platform.",
      "quote": "1.7 billion AI actions across the Workday platform",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states the count of new organic role-based agents moving to GA.",
      "quote": "12 new organically developed role-based agents",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states the GA date for Sana Core and Sana Enterprise.",
      "quote": "Sana Core and Sana Enterprise went into GA on February 15",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states current ARR run-rate from emerging AI solutions.",
      "quote": "ARR from these solutions is now over $400 million",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes some third-party vendors as free-riding on Workday's underlying system of record.",
      "quote": "at some level, parasites on Workday",
      "speaker": "Aneel Bhusri",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "competition",
      "claim": "CEO names AI leaders that run Workday as part of an argument that AI is built on top of cloud incumbents rather than replacing them.",
      "quote": "Anthropic, Google and OpenAI, all run Workday",
      "speaker": "Aneel Bhusri",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "President and Chief Commercial Officer names customer expansions in the quarter.",
      "quote": "customers like Anthropic, Ally Financial and Otis Elevator",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "CFO states gross revenue retention rate for the period.",
      "quote": "Gross revenue retention rates remained strong at 97%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "commitment",
      "claim": "President and Chief Commercial Officer names early adopters of the new Flex Credits pricing model.",
      "quote": "Accenture, Nike and Merck are among the first",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "President and Chief Commercial Officer flags elongation in large enterprise deal closing.",
      "quote": "large enterprise deals are taking longer to close",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "President and Chief Commercial Officer names the segments most affected by deal elongation.",
      "quote": "particularly in Fed, SLED and health care",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "CFO notes average contract duration declined year-over-year.",
      "quote": "contract duration in the quarter was down year-over-year",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites gross retention of 97-98% across the >11,000-customer installed base as evidence customers are not leaving.",
      "quote": "a gross retention rate of 97% to 98%.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states Workday software sits on the desktop of 73 million end users.",
      "quote": "We are on the desktop of 73 million users, 73 million users.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states 75% of customers already use AI features bundled into the core platform subscription, without an added AI upcharge.",
      "quote": "75% of our customers are using AI that's in the platform",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes Workday's AI differentiation as building first-party, enterprise-focused domain-specific agents.",
      "quote": "we're building first-party agents, our own agents",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO says Workday has announced 13 first-party AI agents to be showcased at the upcoming user conference.",
      "quote": "We have 13 of them we've announced.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO frames the Agent System of Record as the orchestration layer for onboarding third-party AI agents like employees.",
      "quote": "the Agent System of Record as the orchestration layer",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "CEO recalls repeated existential threats to VMware from open-source hypervisors that never materialized, drawing a parallel to today's AI-disruption narrative.",
      "quote": "We were going out of business.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "Discussion references the earlier market debate that AWS would commoditize software as a historical analogue to the current AI-commoditization fear.",
      "quote": "AWS is going to commoditize software debate",
      "speaker": "Kasthuri Rangan, Analyst",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "CEO says Workday is model-agnostic and treats LLM providers as interchangeable rather than betting on one winner.",
      "quote": "they're interchangeable for us from an LLM perspective.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO states Workday has acquired 4 AI companies in the last 1.5 years as part of an inorganic AI build-out.",
      "quote": "in the last 1.5 years, we bought now 4 AI companies",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the most recent acquisition is Paradox, a conversational AI platform aimed at frontline workers.",
      "quote": "we announced an acquisition of a company called Paradox",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO describes launching a dedicated Workday Government subsidiary to invest in and target the U.S. federal market.",
      "quote": "we launched actually the Workday Government subsidiary",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges AI will drive further economies of scale, implying pressure on customer headcount/seat growth even as he disputes it being AI-driven job cuts.",
      "quote": "AI will drive further economies of scale",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "risk",
      "claim": "CEO gives an ambiguous, self-qualifying statement on customer headcount growth trend immediately before saying overall headcount still grows.",
      "quote": "It's moderating. It's not growing.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says Workday will provide a further update on its AI pricing and monetization strategy at the upcoming Financial Analyst Day.",
      "quote": "we'll provide a further update on our AI pricing strategy",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states the AI business is growing 100% year-over-year.",
      "quote": "our AI business 100% year-over-year",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO repeatedly defers quantification of the AI book of business to the following week's Financial Analyst Day.",
      "quote": "Come next week.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to keeping Flowise, the acquired agent-building platform, open source going forward.",
      "quote": "we are going to keep an open source platform.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 公布 FY28 財務框架，訂閱營收 CAGR 依低/中/高情境設定區間。",
      "quote": "that ranges from 12% to 15% in each of these scenarios",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "同一 FY28 框架下，非 GAAP 營業利益率區間為 33%-36%。",
      "quote": "and that ranges from 33% to 36%.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層設定 FY28 非 GAAP rule of 48% 目標（成長+利潤率合計）。",
      "quote": "our target here is a non-GAAP rule of 48%.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 特別把分析師注意力錨定在 FY27 訂閱營收成長 13%（框架中值下緣）。",
      "quote": "And I want to anchor you to the 13% number.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 說明 FY28 財務框架不含近期宣布的 Sana Labs 收購案。",
      "quote": "none of the guidance you see here includes our most recent",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "本財年非 GAAP 營業利益率預期較去年提升 3 個百分點至 29%。",
      "quote": "climb 3 points on a year-over-year basis to 29%",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "股權薪酬占營收比重本財年降至 17%，較去年下降 1 個百分點。",
      "quote": "expecting 17%, off 1 point year-over-year",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "FY28 目標為非 GAAP rule 扣除 SBC 後之 rule of 35%。",
      "quote": "committing a target rule of 35%",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "董事會核准新增 40 億美元庫藏股額度，累計至 FY27 將執行 50 億美元回購。",
      "quote": "we're going to be buying back $5 billion through FY '27.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "資本配置哲學第一順位是有機投資（尤其 AI），其次才是併購與庫藏股。",
      "quote": "primary focus is organic investment, in particular, in AI",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "公司設定 FY28 每股自由現金流目標為 15 美元。",
      "quote": "targeting free cash per share of $15 in FY '28.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 直接反駁「AI 正在吞噬軟體業」的市場敘事，稱其過度渲染。",
      "quote": "AI is eating the software world is completely overblown",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "面對 AI 原生新創威脅的提問，產品長主張 Workday 上萬名工程師用 AI 工具提速後可壓過小型新創。",
      "quote": "outrun any start-up with 10 people going 10x faster.",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "回應「SaaS 將被 AI 架構取代」的看法時，產品長主張是既有業務流程驅動 AI、而非反過來。",
      "quote": "It's not like the AI is driving the process",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "CEO 定位 Sana Labs 收購案為 Workday 全新 AI 原生入口／使用者介面。",
      "quote": "This is the new front door. The new UI for Workday is AI.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "公司發表 Flex Credits，一種以用量計費的新定價模式。",
      "quote": "Flex Credits, a consumption-based pricing model",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "CTO 說明開放平台策略中，agent 對外介面採用 MCP 協議標準。",
      "quote": "For agents, we're embracing MCP.",
      "speaker": "Peter Bailis",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "過去一年 AI 相關營收動能自 2.5 億美元成長至逾 4.5 億美元。",
      "quote": "from over $250 million to greater than $450 million",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "特定 agentic AI SKU 的 ARR 在過去一年自不到 5,000 萬美元成長至逾 1.5 億美元。",
      "quote": "less than $50 million to more than $150 million in ARR",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 強調公司在 11,000 個客戶基礎與 97% 留存率上具有獨特定位以迎接 AI 轉型。",
      "quote": "11,000 customers, 97% retention rate",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 說明其財務框架的低情境假設是總體經濟轉弱、成長引擎放緩。",
      "quote": "a stable macro similar to what we're experiencing today",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "risk",
      "claim": "回應分析師提問時，CFO 表示若成長放緩，公司會在未見到預期回報的領域收回投入資源。",
      "quote": "we'll continue to find opportunities to pull back",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "commitment",
      "claim": "被問及 2023 年裁員後回聘承諾時，CFO 表示目前仍在招募，但強調招募地點與方式會改變。",
      "quote": "We are hiring right now, and how we hire and where we hire",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 說明即便持續下修股權薪酬占比，仍須用股票留才以吸引頂尖人才。",
      "quote": "leverage equity and stock to get them to join Workday.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier sizes Workday's total addressable market at roughly $200 billion.",
      "quote": "the TAM that we're operating in is roughly $200",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier says a roughly $3 billion frontline-work market segment exists where Workday currently has a narrow offering.",
      "quote": "on the planet are falling in the frontline work category",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Kazmaier says Workday's mid-market win rates are roughly the same as its large-enterprise win rates.",
      "quote": "specifically in mid-market, we actually -- we have the same",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "guidance",
      "claim": "Kazmaier says Workday will increase margin per the framework it previously guided, by realizing more operating leverage.",
      "quote": "we guided in the framework that we gave out",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "Kazmaier says Workday has lots of operating leverage across its entire operating expense base.",
      "quote": "we have lots of operating leverage across everything",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "Kazmaier says Workday delivered on its margin goals while also investing in organic innovation.",
      "quote": "delivered on our margin goals, and we invested",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Kazmaier says Workday pursued aggressive M&A in the same period it delivered on its margin goals.",
      "quote": "We pursued aggressive M&A.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Kazmaier says Workday acquired Sana because it is a leading AI experience.",
      "quote": "Now we acquired Sana because it is truly a",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "competition",
      "claim": "Responding to a question framing rivals as newer, Kazmaier says many competitors are actually older than Workday.",
      "quote": "Actually, many of them are older, right?",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "competition",
      "claim": "Kazmaier says accuracy is the number one criterion that defines enterprise acceptance of AI.",
      "quote": "There is one #1 criteria which defines the acceptance of AI",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Kazmaier says customers are seeing fantastic results (reduced service-center contact rates) from AI-driven employee service delivery.",
      "quote": "they're seeing fantastic results with that, right?",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "risk",
      "claim": "Kazmaier frames the debate over the future of SaaS/system-of-record vendors as a path from system of record to system of action.",
      "quote": "path is from system of record to system of action.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "commitment",
      "claim": "Kazmaier commits to Workday remaining acquisitive going forward.",
      "quote": "And we're going to remain acquisitive, right? I'm",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier says Workday launched \"Flex Credits\" as a new usage-based monetization concept for AI features.",
      "quote": "So what we launched is a concept called Flex Credits.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier describes a new no-code agent builder letting people quickly build agentic automation, paired with the Pipedream acquisition for connectivity.",
      "quote": "people can build very quickly in a nontechnical way, agentic",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Kash Rangan (Goldman Sachs) followed up asking for Carl Eschenbach's viewpoint on Sam Altman/OpenAI's comment about entering SaaS.",
      "response_pattern": "Carl Eschenbach did not engage with the substance, saying he had no viewpoint because he did not know what OpenAI meant, then pivoted to a generic line that 'AI is software' rather than addressing the competitive implication raised.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Karl Keirstead (UBS) asked Zane Rowe to roughly size the basis-point upside to cRPO from elevated early renewals in the quarter.",
      "response_pattern": "Zane Rowe did not give a specific bps figure, instead saying it was 'probably above the range' and that early renewals were 'a big contributor,' avoiding quantification of the specific number requested.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Raimo Lenschow (Barclays) pressed Zane Rowe to reconcile the math: a Q2 beat of roughly $9 million plus $15 million from Paradox should imply a larger guidance raise than what was given.",
      "response_pattern": "Zane Rowe did not directly reconcile the arithmetic the analyst laid out, instead repeating general reassurance ('a lot that goes into our forecast,' 'we feel great about the year') without addressing the specific dollar gap questioned.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Karl Keirstead 追問 Q4 cRPO 15%-16% 中約 2.25 個百分點來自 tenant/Paradox/Sana 一次性因素的拆解算法是否正確",
      "response_pattern": "Zane Rowe 只用「sort of generally in line」等模糊字眼確認方向，未逐項驗證或訂正精確拆解數字，隨後轉談另一個指標（Sana/Paradox 對訂閱營收成長的貢獻）而非直接答 cRPO 拆解",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "question": "John DiFucci (Guggenheim) pressed on why the Q1 FY27 subscription guide implies roughly a $25 million sequential decline when the previously disclosed DIA nonrecurring benefit was only about $15-20 million, saying the math does not add up for a subscription model.",
      "response_pattern": "Zane Rowe repeated the DIA contract roll-off and fewer-days-in-Q1 explanations across two consecutive answers without reconciling the specific dollar gap DiFucci pointed to; on the second follow-up he closed with 'nothing more than that' rather than walking through a numeric bridge.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Alex Zukin (Wolfe Research) asked directly whether the 35% FY28 operating margin target set at the prior Financial Analyst Day is still on the table.",
      "response_pattern": "Zane Rowe did not confirm or deny the 35% figure; he deflected to 'update later on in the year at our next financial analyst update' and reframed the priority as driving growth over hitting the operating margin target, without restating or affirming the number.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Michael Turrin (Wells Fargo) asked if there is a way to size the cRPO impact from the Q4 large-deal elongation Rob Enslin described in his prepared remarks.",
      "response_pattern": "Robert Enslin did not give a number or range for the cRPO impact; he said the deals are 'elongated' rather than lost and pivoted to discussing nonorganic agent sales and Flex Credits consumption momentum instead of quantifying the impact asked about.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Analyst asks whether seat-based/headcount growth pressure tied to AI is structural or just a correction from pandemic-era overhiring (noted as the same question asked on the earnings call three weeks earlier).",
      "response_pattern": "CEO calls the narrative 'completely overblown', pivots to an anecdote about a Fortune 10 CIO and a TAM-expansion argument rather than giving specific seat/logo growth figures, and gives internally inconsistent phrasing ('It's moderating. It's not growing.') immediately before stating overall customer headcount continues to grow.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "question": "Analyst asks the CEO to quantify the AI book of business, referencing that peer SaaS companies already disclose such a metric.",
      "response_pattern": "CEO declines to give any current figure and instead responds twice with 'Come next week', deferring quantification to the Financial Analyst Day rather than answering on the spot.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "question": "Karl Keirstead (UBS)：把 FY27 成長目標從 15% 下修到 13%，是因為聽取建議想更保守，還是環境真的變得比預期更艱難？",
      "response_pattern": "CFO 未直接回答「是否環境變艱難」這個二選一問題，改談框架設計哲學、傾聽建議、以及對數字有信心，全程未正面承認或否認總體環境轉差。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "question": "Brent Thill (Jefferies)：公司裁員 1,750 人中已回聘約 1,000 人，是否仍承諾回聘剩餘人數，或會放慢招募步調？",
      "response_pattern": "CFO 回答「目前仍在招募」但自承先前對回聘時程「說得比較模糊」，未給出具體剩餘人數的回補時間表或是否維持原承諾。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "question": "Analyst (Raimo Lenschow) asked how management balances pressure to deliver margin expansion against the amount of work still needed on Workday's technology/product side, after having earlier raised the same worry as a joke about Kazmaier's R&D budget getting cut.",
      "response_pattern": "Kazmaier's first response to the earlier framing of this concern was a joking deflection (\"All investors as concerned as you are about my well being. I love it.\") rather than a direct answer; the analyst had to restate the question before Kazmaier gave a substantive response.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "question": "Analyst asked, using a P-times-Q framing, whether AI/agents reducing the number of employee seats could create a revenue offset problem given Workday's historically per-employee pricing model.",
      "response_pattern": "Kazmaier answered qualitatively (asserted it will not be a black-and-white/tectonic shift and cited the global market index still showing growth) without providing any quantified split, percentage, or offset estimate between seat-based and usage-based (Flex Credits) revenue.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    }
  ]
}

```

---

## judgment.json 全文

```json
{
  "meta": {
    "ticker": "WDAY",
    "date": "2026-09-05",
    "schema": "v15.0",
    "company_name": "Workday, Inc."
  },
  "oneliner": "WDAY：13% 訂閱成長＋31% 非 GAAP 利潤率＋97% 留存的 HCM 龍頭，前瞻本益比 17.7x／PEG 0.9 落五年低檔；AI 席次壓縮與 Silver Lake 私有化事件是兩個未決變數——進場但只給衛星，首倉 1/3，其餘掛事件與 cRPO 觸發。",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": null,
    "confidence": "高",
    "fingerprint": "毛利率 75.8%、FCF 利潤率 30.2%、訂閱佔營收 93%、三年以上不可取消合約、年度預收——典型訂閱型複利指紋；唯一雜訊是 SBC 佔營收 17.4% 讓 GAAP 營業利益率只有 11.8%"
  },
  "thesis": {
    "headline": "好生意、合理價、兩個未決變數：AI 是否蠶食席次，以及私有化是否把複利換成一次性溢價",
    "holding_period": {
      "horizon": "長期 5-10 年（衛星角色）",
      "driver": "AI 變現淨增量（AI ARR 對席次壓縮的補回）與訂閱成長是否守住雙位數；利潤率擴張與回購是第二引擎",
      "signal_vs_noise": "持有期 >2 年，訊號＝cRPO 年增、GRR、AI 新簽 ACV 佔比、SBC 佔營收；噪音＝單季營收小幅超預期、賣方目標價互砍、私有化傳聞的日內波動"
    },
    "H": [
      {
        "id": "H1",
        "text": "訂閱成長守住雙位數——AI 未蠶食按員工計費基礎，企業 HR／財務系統換代與 HR＋財務全套化持續",
        "2y": "FY27 訂閱營收 $9.94-9.95B（+13%）如期；FY28 指引 ≥+11%；cRPO 年增每季 ≥12%",
        "5y": "FY31 訂閱營收年增仍 ≥10%；GRR 維持 ≥96%",
        "10y": "FY36 訂閱營收 ≥ FY26 的 2.5 倍（10 年 CAGR ≥9.6%）",
        "threshold": "FY27 退出 cRPO 年增 ≥12%；FY28 訂閱指引 ≥+11%；GRR ≥96%",
        "source": "季度新聞稿 cRPO／訂閱營收；年報 GRR",
        "drift_rule": "cRPO 年增連 2 季 <12% → 削弱；連 3 季 <10% → 反轉"
      },
      {
        "id": "H2",
        "text": "營運槓桿兌現——非 GAAP 營業利益率自 31% 走向 FY28 框架 33-36%，SBC 佔營收逐年降 1pp，GAAP 營業利益率同步抬升",
        "2y": "FY27 退出非 GAAP 營業利益率 ≥31%；FY28 指引 ≥33%；SBC 佔營收 ≤16%",
        "5y": "FY31 非 GAAP 營業利益率 ≥34%；GAAP 營業利益率 ≥18%",
        "10y": "FY36 GAAP 營業利益率 ≥25%（SBC 佔營收 ≤10%）",
        "threshold": "非 GAAP 營業利益率年增 ≥+100bp／年；SBC 佔營收年降 ≥1pp",
        "source": "季度新聞稿非 GAAP 營業利益率與 SBC；Financial Analyst Day 框架更新",
        "drift_rule": "非 GAAP 營業利益率連 2 季年減 ≥100bp → 削弱；FY28 框架下修至 <33% → 反轉"
      },
      {
        "id": "H3",
        "text": "AI 變現淨增量為正——AI ARR 自 $400M 以上翻倍、agentic 新簽 ACV 佔比守 25%、Flex Credits 消費計費補回席次壓縮",
        "2y": "FY28 末 AI ARR ≥$800M；agentic 新簽 ACV 佔比連 4 季 ≥20%",
        "5y": "FY31 AI ARR ≥$2B（佔訂閱營收 ≥12%）",
        "10y": "消費計費佔訂閱營收 ≥30%，按員工計費不再是唯一基礎",
        "threshold": "AI ARR 年增 ≥60%；agentic 新簽 ACV 佔比 ≥20%",
        "source": "季度新聞稿／法說會 AI ARR 與 agentic ACV 揭露",
        "drift_rule": "AI ARR 年增連 2 季 <40% 或 agentic ACV 佔比連 2 季 <15% → 削弱；公司停止揭露 AI ARR → 反轉"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "agentic AI 蠶食席次：客戶以更少 HR／財務人力跑更多流程，按員工計費基礎縮減快於 Flex Credits 補回；管理層對「席次 vs 消費」拆分持續迴避量化（來源：摘要，Barclays 2025-12、Goldman 2025-09 問答）",
        "h_ref": "H1／H3",
        "clock": "🔥",
        "threshold": "cRPO 年增連 2 季 <12%，或客戶端員工數年增轉負（法說揭露）→ 停止加碼；連 4 季 → 減至首倉",
        "evidence_refs": [
          "substitute_technology#0",
          "substitute_technology#1",
          "substitute_technology#2",
          "supply_demand_durability#1",
          "competitive_share_entrants#3"
        ]
      },
      {
        "id": "R2",
        "text": "新簽動能失速：大型交易在聯邦／州地方教育／醫療拉長、中型市場輸給 Rippling／HiBob／Dayforce、合約期年減；Cantor 5 月通路查核中性偏負",
        "h_ref": "H1",
        "clock": "⚡",
        "threshold": "cRPO 年增連 2 季低於總 RPO 年增 2pp 以上（早期續約充數）或總 RPO 年增 <6% → 減倉",
        "evidence_refs": [
          "competitive_share_entrants#1",
          "competitive_share_entrants#2",
          "supply_demand_durability#0"
        ]
      },
      {
        "id": "R3",
        "text": "AI 招募產品的法律責任：Mobley 案 ADEA 與加州 FEHA 指控皆獲准續行，涵蓋約 11 億份申請；加上 Salesloft Drift 外洩衍生消費者集體訴訟——限制 AI 招募線（HiredScore／Paradox）變現並帶來和解成本",
        "h_ref": "H3",
        "clock": "🐢",
        "threshold": "集體認證成立且和解金 >$500M，或法院禁令限制 AI 篩選功能 → 減半；刑事或監管介入 → 清倉",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "regulatory_antitrust#1",
          "major_events#3",
          "major_events#4",
          "lawsuit_class_action#0"
        ]
      },
      {
        "id": "R4",
        "text": "Silver Lake 私有化事件雙向風險：定案（假設性 $227）把 5-10 年複利換成一次性 16% 溢價；破局則 8/13 起約 24% 的事件溢價回吐；股東律所已啟動受託責任訴前調查",
        "h_ref": "H1",
        "clock": "⚡",
        "threshold": "定案 ≥$220 → 部位轉為併購套利、價差 <3% 出清；破局 → 不追、等回落 ≤$170 分批補第二個 1/3",
        "evidence_refs": [
          "major_events#0",
          "major_events#5",
          "lawsuit_class_action#1",
          "capital_markets_pricing#1"
        ]
      }
    ],
    "single_thing": {
      "description": "Workday 在下一次 Financial Analyst Day（管理層稱 2026 年內更新）撤回或下修 FY28 財務框架的訂閱成長區間至 <12%",
      "why_fatal": "框架是管理層對「AI 不蠶食席次」的自我承諾；下修即公司自己承認按員工計費基礎在縮，Base 的 EPS 複利 10.6%／年直接失去成長引擎，只剩利潤率與回購",
      "if_happens": "減至首倉 1/3 並重跑判斷；若同時下修營業利益率目標 → 清倉",
      "how_monitor": "Financial Analyst Day 簡報框架頁；季度法說 CFO 是否重申 12-15%",
      "probability": "12-24 個月內約 25%（CFO 於 2026-02 已拒絕重申 35% 利潤率目標，來源：摘要）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "產業物理供需＝balanced（ID：生產力 Copilot／AI 辦公整合，as-of 2026-04-27）；候選 ID Agentic AI 平台（2026-09-03）判 split、priced_in mid。Phase II 經自身位置閘交叉驗證：HCM 雲端滲透仍在擴張（HCM 市場 2026-2034 CAGR 8.5%）、資本支出週期不適用、無庫存；但軟體倍數三年系統性下移，屬「擴張中被重新定價」的 Phase II，非過熱",
    "bargaining": {
      "up": "上游＝三家超大規模雲（AWS／Google／Microsoft）代管與模型供應商；公司自稱模型可互換（來源：摘要），但代管集中是 10-Q 自揭風險因子，且這三家同時是 AI 分發層的競爭者",
      "down": "下游分散：11,000+ 客戶、無單一客戶 >10%（10-Q）、三年以上不可取消合約、年度預收、GRR 97%——議價權在 Workday；例外是聯邦／州地方教育／醫療受預算拖累拉長交易",
      "geo": "美加歐亞多區資料中心＋災難轉移程序（10-Q）；無關稅／出口管制曝險；資料主權法規為潛在但未 sourced 的變數"
    },
    "profit_pool_dir": "HCM／ERP 應用層利潤池往「握專屬資料＋成功轉消費計費」的既有廠商集中（ID 供給側結論），AI 層新增利潤池部分流向分發者（MSFT／GOOGL）與模型商；本標的環節 5 年池占比精確數字證據包未涵蓋，以 HCM 三家合計 58% 且 Workday 為最大單一廠商判無 ≥5pp 淨流出",
    "tam_table": [
      {
        "segment": "HCM（核心）",
        "tam_now": "2026 全球 HCM 軟體約 $37.5B",
        "tam_5y": "2034 約 $77.4B（CAGR 8.5%）",
        "sam": "1,000 人以上企業雲端 HCM 套件",
        "penetration": "2025 全球 HCM 份額約 22%，三家合計 58%",
        "cagr": "8.5%（市場）vs Workday 訂閱 13%",
        "position": "系統紀錄層＋應用層（利潤最厚環節）",
        "pool_shift": "自地端 SAP／Oracle 流向雲端三強；Workday 為最大單一廠商",
        "ceiling": "天花板＝大型企業雲端滲透飽和；被替代路徑＝agentic AI 直接執行流程、繞過按席次應用層"
      },
      {
        "segment": "財務管理（Financials／Adaptive Planning）",
        "tam_now": "2025 約 $3.9B（第三方口徑，信心低）",
        "tam_5y": "2034 約 $10.5B（CAGR 11.5%）",
        "sam": "已用 Workday HCM 的客戶交叉銷售（Q3 FY26 半數以上新簽含 HR＋財務，來源：摘要）",
        "penetration": "證據包未涵蓋（公司不拆產品線營收）",
        "cagr": "11.5%",
        "position": "與 HCM 同一資料模型，統一平台是主要賣點",
        "pool_shift": "自 Oracle／SAP ERP 財務模組流入",
        "ceiling": "天花板＝大型企業財務核心換代週期長；被替代路徑＝SAP S/4HANA 生態綁定（已跑 SAP 的買方）"
      },
      {
        "segment": "AI／agentic（Illuminate、Sana、Flex Credits）",
        "tam_now": "公司自稱整體 TAM 約 $200B（來源：摘要，Barclays 2025-12）",
        "tam_5y": "證據包未涵蓋",
        "sam": "既有 11,000+ 客戶基礎的加購",
        "penetration": "AI ARR >$400M vs 訂閱營收約 $10B＝4%；75% 核心客戶已用內建 AI（來源：摘要）",
        "cagr": "三位數年增（Q1 FY27 揭露）",
        "position": "第一方 agent＋Agent System of Record 編排層",
        "pool_shift": "新增池；與 MSFT／GOOGL 分發層分食",
        "ceiling": "天花板＝消費計費能否補回席次壓縮；被替代路徑＝通用 agent 平台直接讀寫 Workday 資料（管理層稱之為寄生者，來源：摘要）"
      },
      {
        "segment": "中型市場（Workday GO）與前線工作者（Paradox）",
        "tam_now": "前線工作者類別約 $3B（來源：摘要）",
        "tam_5y": "證據包未涵蓋",
        "sam": "夥伴轉售的輕量版套件",
        "penetration": "起步階段（2026-02 上線美加英愛德）",
        "cagr": "證據包未涵蓋",
        "position": "夥伴主導通路，非直銷",
        "pool_shift": "與 Rippling／HiBob／Dayforce 正面競爭",
        "ceiling": "天花板＝中型市場對價格敏感；被替代路徑＝AI 原生 HRIS 以更低價切入"
      }
    ]
  },
  "moat": {
    "execution": 7,
    "pricing": 8,
    "combined": 7.5,
    "grade": "B",
    "score": 7.5,
    "trend": "→",
    "trend_evidence": "執行面穩定：Gartner 雲端 HCM 領導者連續第 11 年（2026-09-02）、GRR 97%（Q2 FY27）、agentic 新簽 ACV >$100M 佔當季新簽 >25%（2026-08-27）；定價面承壓：中型市場輸給 Rippling／HiBob／Dayforce、合約期年減、按員工計費模型被 AI 席次壓縮敘事打折。一穩一壓，對 thesis 更關鍵的是定價維度，故取 →；前瞻 2-3 年份額：大型企業守住、中型市場緩失",
    "spread_table": [
      {
        "metric": "GAAP 營業利益率（TTM）",
        "self": 11.73,
        "peer": "CRM 21.87／NOW 11.4",
        "spread_pp": -10.14,
        "trend": "WDAY Q2 FY26 10.6% → Q2 FY27 11.8%（+120bp），對 NOW 持平、對 CRM 落後；三年趨勢證據包未涵蓋",
        "note": "差距主因 SBC 佔營收 17.4%（CRM 口徑證據包未涵蓋）；非 GAAP 營業利益率 31.1% 對 NOW 同級"
      },
      {
        "metric": "FCF 利潤率（TTM）",
        "self": 30.16,
        "peer": "CRM 34.23／NOW 31.03／PLTR 54.55／MSFT 20.19",
        "spread_pp": -4.07,
        "trend": "前份 29.1%→30.2% 微升",
        "note": "現金轉換與同業同級，非護城河差異來源"
      },
      {
        "metric": "毛利率（TTM）",
        "self": 75.77,
        "peer": "CRM 77.64／NOW 74.77",
        "spread_pp": -1.87,
        "trend": "證據包未涵蓋逐季（無連 2 季年減 >1.5pp 證據）",
        "note": "閘二未觸發"
      },
      {
        "metric": "研發強度（TTM）",
        "self": 27.62,
        "peer": "NOW 22.14／CRM 14.38／PLTR 10.42",
        "spread_pp": 5.48,
        "trend": "AI 投資加速（FY27 指引口徑，來源：摘要）",
        "note": "研發強度最高，若無法轉成 AI ARR 即是利潤率拖累"
      }
    ],
    "threats": [
      {
        "level": "⛔ 架構替代",
        "text": "agentic AI 直接執行 HR／財務流程、繞過按席次應用層（a16z「Workday's Last Workday?」；2026-02 財報後市場以 SaaS 重定價回應）；扣 2 分已反映在執行 7／定價 8 的上限，不再於 trend 重複記帳",
        "p": "25-30%（5 年內按員工計費基礎實質縮減）",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "substitute_technology#0",
          "substitute_technology#1",
          "supply_demand_durability#1"
        ]
      },
      {
        "level": "🔴 生態攻擊",
        "text": "中型市場輸給 Rippling／HiBob／Dayforce；SAP S/4HANA 生態綁定在已跑 SAP 的買方勝出；Workday GO 以夥伴通路反攻但起步階段",
        "p": "40%（中型市場份額緩失）",
        "evidence_refs": [
          "competitive_share_entrants#1",
          "competitive_share_entrants#2"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "超大規模雲同時是代管供應商與 AI 分發層競爭者（Copilot／Gemini 捆綁）；目前無任一超大規模雲公告自建 HCM",
        "p": "15%",
        "evidence_refs": [
          "geo_supply_chain#0"
        ]
      },
      {
        "level": "🟡 法律",
        "text": "Mobley 案（AI 篩選歧視）若集體認證成立，限制 AI 招募線變現並提高客戶採用門檻",
        "p": "30%（集體認證）",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "regulatory_antitrust#1"
        ]
      }
    ],
    "competitors": [
      {
        "name": "CRM（Salesforce，資料持有型 SaaS 對照）",
        "rev_growth": "證據包未涵蓋",
        "gm": 77.64,
        "om": 21.87,
        "rd_intensity": 14.38,
        "fcf_margin": 34.23,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "Agentforce 按動作計費先行者；營業利益率高 WDAY 10pp，研發強度低一半——成熟期紀律對照組，經濟體質優於 WDAY"
      },
      {
        "name": "NOW（ServiceNow，工作流平台對照）",
        "rev_growth": "證據包未涵蓋",
        "gm": 74.77,
        "om": 11.4,
        "rd_intensity": 22.14,
        "fcf_margin": 31.03,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "與 WDAY 最同形狀（GAAP 營業利益率 11.4% vs 11.7%、FCF 31% vs 30%、研發 22% vs 28%）；同樣面對 agentic 重定價，是 WDAY 最直接的估值與體質尺"
      },
      {
        "name": "MSFT（分發層／潛在超大規模雲競爭者）",
        "rev_growth": "證據包未涵蓋",
        "gm": 67.94,
        "om": 46.78,
        "rd_intensity": 10.72,
        "fcf_margin": 20.19,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "365 Copilot 近零成本捆綁（ID）；結構性成本更低且 FCF 足以攻擊——依賽局結構規則（結構性成本更低且有攻擊力的對手存在），WDAY 定價分數上限設 8 而非更高"
      },
      {
        "name": "SAP SuccessFactors／Oracle HCM（直接 HCM 對手）",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "證據包未涵蓋",
        "strategy_note": "RFP 決賽常客；SAP 靠 S/4HANA 生態綁定勝出，Workday 靠 HR＋財務統一資料模型與薪資勝出；HCM 份額 SAP 約 5% vs Workday 20-23%（6sense）"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率 × 高周轉（非 GAAP 口徑）——收入隨客戶員工數與模組數成長、資本支出僅佔營收約 2.5%、年度預收讓營運資金為負；GAAP 口徑因 SBC 落到中利益率，象限判讀以現金為準",
      "checkpoints": [
        {
          "name": "需求基礎值",
          "light": "🟢",
          "evidence": "需要型：HR／薪資／財務核心是法遵與發薪必需，停用即業務停擺；使用者（員工）、決策者（CHRO／CFO）、付款者（IT 預算）三角完整；65% 財富 500 強為客戶（來源：摘要）。惟客戶要解決的問題（跑流程）與目前方案（按席次應用）可分離——這是 AI 威脅的落點",
          "proxy": "GRR 97%（Q2 FY27）；客戶端員工數仍溫和成長（來源：摘要，Q3 FY26）"
        },
        {
          "name": "決策層級",
          "light": "🟢",
          "evidence": "決策單位是整套 HR＋財務系統紀錄（資料遷移、薪資切換、員工重訓），非單一功能；三年以上不可取消合約、年度預收（10-Q）；一家保險公司回頭簽 10 年全套（來源：摘要）",
          "proxy": "合約期（Q4 FY26 年減，來源：摘要）；早期續約比例"
        },
        {
          "name": "價值鏈分配",
          "light": "🟡",
          "evidence": "應用層留住多數利益（FCF 30%），但 AI 層需向模型商與超大規模雲付推論成本，且分發層（MSFT／GOOGL）以捆綁分食；管理層稱第三方 agent 是寄生者（來源：摘要）顯示利益分配正被爭奪",
          "proxy": "AI ARR 毛利率（證據包未涵蓋）；研發強度 27.6% 是否下降"
        },
        {
          "name": "社會容忍度",
          "light": "🟡",
          "evidence": "必要性高、政治敏感度中：AI 招募篩選已引來 Mobley 集體訴訟（ADEA＋FEHA 續行，涵蓋約 11 億份申請）；無依賴監管授權的優勢，但 AI 用於僱用決策的法規（加州、歐盟 AI Act）可能限制變現；未見大幅提價引發反制",
          "proxy": "Mobley 案程序里程碑；各州 AI 僱用法規"
        }
      ],
      "roiic": "約 20%（區間 15-33%）",
      "reinvest_rate": "約 45%（含併購；剔除併購僅約 10%）",
      "endo_ceiling": 9.0,
      "formula_note": "ROIIC：Q2 FY27 非 GAAP 營業利益較 Q2 FY26 增 $143M（$824M−$681M）→年化 $570M×(1−20%)＝$456M；GAAP 口徑增 $65M（$313M−$248M）→年化 $208M；分母＝近一年新增投入資本約 $1.4B（Sana $1.1B＋Paradox／Pipedream／Flowise 未揭露金額＋資本支出約 $270M−折舊≈0）→ 非 GAAP 33%／GAAP 15%，取中值 20%。再投資率＝$1.4B÷非 GAAP NOPAT 約 $2.6B（$3.2B×0.8）≈45%；剔除併購約 10%。內生天花板＝20%×45%＝9%。共識 FY27→FY30 EPS CAGR 16.3% 缺口 7pp 歸因：利潤率擴張 31%→34%（約 +3%／年）＋淨回購（約 1-1.5%／年）＋併購貢獻（Sana／Paradox）——可歸因，不標依賴 re-rate"
    }
  },
  "growth": {
    "runway_years": 10,
    "runway_post_y5": "🟢",
    "seven_questions": [
      "①結構性或週期反彈：結構性——雲端 HCM／財務換代仍在進行（HCM 市場 2026-2034 CAGR 8.5%），無週期反彈成分；但 2024-2026 美國 ERP 市場年增降至 5% 以下的『加速前暫緩期』是需求層逆風",
      "②資本投入多少：極低——資本支出約 $270M 佔營收 2.5%；成長資本主要是研發（27.6%）與併購（近 1.5 年四家 AI 公司，Sana $1.1B）",
      "③增量 ROIC 是否 >資金成本：非 GAAP 口徑 33% 是；GAAP 口徑 15% 勉強——差距全是 SBC，這是本檔最弱的一題",
      "④成長變現金流或被吃掉：變現金流——FY27 FCF 指引 $3.18B、$5B 回購至 FY27；併購 $1.1B 級別是唯一大額回收",
      "⑤競爭者會否被吸引：已被吸引——AI 原生 HRIS（Rippling／HiBob）在中型市場、通用 agent 平台在 AI 層；大型企業核心暫未失守",
      "⑥股價反映多少期待：不多——前瞻本益比 17.7x／PEG 0.9、trailing 倍數在五年區間最低檔；但 8/13 起含私有化溢價",
      "⑦成長率下修估值撐得住嗎：成長降至 10% 時合理倍數 13-15x，對應 $144-166（−15~−26%）；降至 5% 時 11x 對應 $131（−33%）——撐得住不崩，但 5 年報酬歸零"
    ],
    "segments": [
      {
        "name": "訂閱服務（HCM＋財務，93% 營收）",
        "fy0": "FY26 $8.83B（+14.5%）",
        "driver": "量：客戶數×每客戶員工數×模組數；價：定價事件證據包未涵蓋，Flex Credits 為新計費軸",
        "fy1e": "FY27 $9.94-9.95B（+13%，指引）",
        "fy2e": "FY28 約 $11.1B（+11-12%）",
        "fy3e": "FY29 約 $12.3B（+11%）",
        "om_path": "非 GAAP 營業利益率 31%→34%（合併）",
        "eps_contrib_pct": "約 95%"
      },
      {
        "name": "專業服務（約 7% 營收）",
        "fy0": "FY26 約 $0.7B",
        "driver": "量：新客戶導入；趨向夥伴直接承接（10-Q）",
        "fy1e": "持平至微降",
        "fy2e": "持平",
        "fy3e": "持平",
        "om_path": "接近損益兩平",
        "eps_contrib_pct": "約 0%"
      },
      {
        "name": "AI／agentic（訂閱內子集）",
        "fy0": "AI ARR >$400M（FY26 末）",
        "driver": "量：agentic 新簽 ACV >$100M／季、佔新簽 >25%；價：Flex Credits 消費計費（Accenture／Nike／Merck 首批，來源：摘要）",
        "fy1e": "AI ARR 約 $600-700M",
        "fy2e": "約 $0.9-1.0B",
        "fy3e": "約 $1.3B",
        "om_path": "推論成本壓毛利率（數字證據包未涵蓋）",
        "eps_contrib_pct": "約 5%（增量）"
      }
    ],
    "decay_signals": [
      "護城河侵蝕｜毛利率連 2 季年減：未亮（逐季證據包未涵蓋，TTM 75.8% 對前份無惡化）",
      "護城河侵蝕｜核心市佔縮減：未亮（HCM 領導者第 11 年；中型市場輸單屬非核心）",
      "護城河侵蝕｜提價後銷量下滑：未亮（定價事件證據包未涵蓋）",
      "盈餘品質｜EPS CAGR 高於營收 CAGR >5pp：邊界亮（共識 EPS 16.3% vs 訂閱 13%，差 3.3pp；FY27→FY29 兩年 18.1% 則差 5.1pp）——歸因利潤率擴張＋回購，可解釋",
      "盈餘品質｜FCF／NI 轉換率 <0.75 連 2 年：未亮（FCF 遠高於 GAAP 淨利）",
      "盈餘品質｜SBC／營收 >5% 且逐年上升：未亮但高位——17.4%，年降 1pp（來源：摘要）",
      "產業結構｜TAM 萎縮或被替代技術壓縮：半亮——agentic AI 壓縮按席次 TAM 的敘事已被市場定價，實績（GRR 97%、客戶員工數仍增）尚未證實",
      "產業結構｜產業倍數近 3 年系統性下移：亮——2026-02『SaaSpocalypse』後軟體倍數重定價，WDAY 前瞻本益比自年初至 5 月一度僅 12.3x",
      "隱性資本密集｜維持性資本支出佔 FCF >60%：未亮（約 8%）",
      "隱性資本密集｜停止投資新產能收入下滑：未亮"
    ],
    "trap_rating": "🟡（2 個亮燈：產業倍數下移、EPS／營收 CAGR 差距邊界；長期成長性綜合 🟡 中等——跑道 ≥10 年但成長品質最弱在 GAAP 增量 ROIC）"
  },
  "quality": {
    "three_year": [
      {
        "metric": "FCF 利潤率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋（前份 29.1%）",
        "fy25_ttm": "30.16（TTM 至 2026-04）；FY27 指引約 30%（$3.18B）",
        "peer_median": "NOW 31.03／CRM 34.23／MSFT 20.19",
        "assessment": "同級偏上"
      },
      {
        "metric": "非 GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "FY25 約 26%（FY26 29% 為年增 3pp 推回，來源：摘要）",
        "fy25_ttm": "FY26 29%；Q2 FY27 31.1%；FY27 指引 31.0%",
        "peer_median": "證據包未涵蓋",
        "assessment": "擴張中，每年約 +200bp"
      },
      {
        "metric": "GAAP 營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "Q2 FY26 10.6%",
        "fy25_ttm": "TTM 11.73；Q2 FY27 11.8%",
        "peer_median": "NOW 11.4／CRM 21.87",
        "assessment": "與 NOW 同級、遠落後 CRM；SBC 是缺口"
      },
      {
        "metric": "SBC 佔營收",
        "fy23": "證據包未涵蓋",
        "fy24": "FY25 約 18%",
        "fy25_ttm": "FY26 17%；Q2 FY27 17.44%",
        "peer_median": "證據包未涵蓋",
        "assessment": "高位緩降，是品質的主要扣分"
      },
      {
        "metric": "ROIC－WACC",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "證據包未涵蓋（投入資本數字不在證據包）",
        "peer_median": "證據包未涵蓋",
        "assessment": "以 FCF 利潤率 30% 與資本支出 2.5% 代理，現金報酬遠高於資金成本"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利潤率",
        "value": "GAAP 11.7%×(1−20%)≈9.4%；非 GAAP 31.1%×0.8≈24.9%",
        "note": "兩口徑差 15pp 全為 SBC（$462M／季）"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本數字不在證據包）",
        "note": "年度預收使營運資金為負、資本支出僅營收 2.5%，周轉率結構上偏高"
      },
      {
        "component": "ROIC",
        "value": "證據包未涵蓋",
        "note": "象限判讀以現金口徑歸「高利益率×高周轉」，GAAP 口徑落中利益率"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO／CCC 三年逐年",
        "value": "證據包未涵蓋",
        "note": "訂閱年度預收（未實現收入 97% 為訂閱，10-Q）→ 現金先於收入；Q4 為開票旺季，DSO 季節性高"
      }
    ],
    "buyback": {
      "authorization": "FY26 末剩餘授權 $2.9B（來源：摘要）；董事會加碼 $4B 後至 FY27 累計回購目標 $5B",
      "q1_capital_return": "FY26 逐季回購 $299M／$803M／$1.5B（來源：摘要）；Q2 FY27 金額證據包未涵蓋",
      "buyback_to_fcf": "$5B 兩年目標 vs FY26-27 FCF 約 $6B → 約 80%，觸及警示線但同時淨現金充裕（FY26 末 $5.4B，來源：摘要）",
      "avg_price_vs_now": "回購均價證據包未涵蓋；FY26 Q4 $1.5B 執行期間股價區間明顯低於現價 $195.79",
      "eps_cagr_ex_buyback": "淨回購約 1-1.5%／年（毛回購約 5%／年減 SBC 稀釋約 3.8%），剔除後 EPS CAGR 約 15%，差距 <5pp"
    },
    "lumpiness": {
      "fcf_5y": "五年逐年證據包未涵蓋；FY27 指引 FCF $3.18B（營運現金流 $3.45B−資本支出約 $270M）；Q1 FY27 $616M、Q2 $460M（季節性，Q4 為收款旺季）",
      "maint_capex_method": "資本支出全數視為維持性（保守法，約 $270M）",
      "owner_earnings": "FY27 約 $3.45B−$0.27B≈$3.18B；每股約 $12.7（依約 2.5 億股估）",
      "verdict": "🟢 正常（現金轉換穩定、資本支出佔 FCF <10%；唯一注意 SBC 是真實成本，owner earnings 扣 SBC 後約 $1.3B）"
    }
  },
  "governance": {
    "capalloc_grade": "B",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC（Sana $1.1B、Paradox、Pipedream、Flowise，1.5 年四家 AI 公司）",
        "value": "第 3 年 NOPAT 貢獻尚不可觀測（Sana 2026-02-15 才 GA）；管理層稱『積極併購、將持續併購』（來源：摘要）→ 未證，不計過",
        "pass": false
      },
      {
        "item": "回購買入收益率",
        "value": "現價 FY27 盈餘殖利率 5.6%（11.06÷195.79）；10 年期公債殖利率證據包未涵蓋，若以 4% 計門檻為 6%——現價未過，但 FY26 回購執行價低於現價，實際買入收益率高於 5.6% → 有保留地判過",
        "pass": true
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 約 $1.85B／年（17.4%×約 $10.6B 營收）vs 回購 $2.5B／年 → 淨稀釋 ≤0，過；但 SBC 絕對額仍是同業最高等級",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "回購",
        "detail": "FY26 $299M／$803M／$1.5B 逐季加速；$5B 至 FY27 目標；FY26 末剩餘授權 $2.9B（來源：摘要）"
      },
      {
        "type": "股息",
        "detail": "無"
      },
      {
        "type": "併購",
        "detail": "Sana $1.1B（AI 前門／UI，2026-02 GA）、Paradox（前線招募 agent）、Pipedream（API 整合）、Flowise（低程式碼 agent 平台，維持開源）；資本配置第一順位為有機 AI 投資（來源：摘要）"
      },
      {
        "type": "治理事件",
        "detail": "共同創辦人 Aneel Bhusri 於 FY26 Q4 法說以 CEO 身分發言（前任 Carl Eschenbach，來源：摘要）——創辦人回鍋重設；Silver Lake 私有化洽談中，股東律所已啟動受託責任訴前調查"
      }
    ],
    "sbc": {
      "pct_revenue": 17.44,
      "pct_gaap_oi": 147.6,
      "trend": "FY25 約 18% → FY26 17%（年降 1pp，來源：摘要）→ Q2 FY27 17.4%",
      "note": "管理層明言仍須用股票留才（來源：摘要）；管理層薪酬結構與近 12 個月內部人交易證據包未涵蓋（數據限制）；股權結構：無雙重股權揭露於證據包"
    }
  },
  "valuation": {
    "tier": "SaaS 訂閱型（系統紀錄層）；同 tier 尺＝NOW（最同形狀）、CRM；MSFT／PLTR 不同層級不作 anchor",
    "peers": [
      {
        "name": "NOW",
        "fwd_pe": "證據包未涵蓋",
        "note": "GAAP 營業利益率 11.4／FCF 31.0 與 WDAY 同形狀，是最合適的倍數尺"
      },
      {
        "name": "CRM",
        "fwd_pe": "證據包未涵蓋",
        "note": "營業利益率 21.9 高一截，倍數應高於 WDAY"
      },
      {
        "name": "SAP／Oracle",
        "fwd_pe": "證據包未涵蓋",
        "note": "直接 HCM 對手，財務證據包未涵蓋"
      }
    ],
    "fwd_pe": 17.7,
    "peg": 0.91,
    "percentile_5y": 1,
    "val_light": "🟢",
    "val_light_derivation": "五年分位：trailing 本益比現值 42.2x 在年度樣本點（n=3，高 139.4／低 56.6）分位 0%；P/S 4.65 分位 1.2%；EV/S 分位 0% → 分位 <30%。PEG：FY28 前瞻本益比 14.82x÷FY27→FY30 EPS CAGR 16.3%（FY30 以 FY29 共識 15.42×1.13 外推）＝0.91 <1.0；以 FY27 前瞻 17.7x 計為 1.09。兩尺取較嚴仍 🟢。旁註：本站短窗前瞻本益比（2026-05 起 8 份快照）現值 17.7x 在窗內分位 89%，屬 4 個月短窗非五年分位，不改燈色但提醒現價已自 6 月低點 11.6x 重估 50%",
    "targets": {
      "short_1y": {
        "eps": 13.21,
        "pe": 17,
        "price": 224.6,
        "upside_pct": 14.7,
        "basis": "FY28 共識 EPS×合理 17x（護城河 B、成長 12-13%、利潤率擴張中）"
      },
      "mid_2y": {
        "eps": 15.42,
        "pe": 17,
        "price": 262.1,
        "upside_pct": 33.9,
        "basis": "FY29 共識 EPS×17x"
      },
      "five_y": {
        "eps": 18.3,
        "pe": 17,
        "price": 311.1,
        "upside_pct": 58.9,
        "basis": "Base FY31 EPS×長期 17x"
      },
      "bear_anchor": {
        "eps": 9.95,
        "pe": 13,
        "price": 129.4,
        "downside_pct": -33.9,
        "basis": "Bear EPS＝FY27 共識 11.06×0.9；Bear 本益比＝成長降至 10% 情境 13x；下行 34% >15% 正常可用"
      },
      "sell_side": "財報後目標價 $145（Deutsche，降評持有）至 $238（Bernstein，優於大盤），Goldman $164、Cantor $205、BTIG 撤回 $175 降中立；共識中樞兩來源相差逾 $90（$188 均值 vs $280 中位數），目標價全距 1.6x 未達 2.5x 離散警戒。現價 $195.79 高於 $188 均值 4%——續漲需要共識上修，結構上是逆風，本檔押的是市場尚未定價的 AI 淨增量為正"
    },
    "upside_short_pct": 14.7,
    "upside_mid_pct": 33.9
  },
  "trap_analysis": {
    "pattern": "「便宜的成熟軟體」模式——估值低不是市場錯，而是市場提前把按席次 SaaS 重定價為成熟軟體（Oracle／Medtronic 式 12-14x 十年不回）",
    "evidence_against": "GRR 97%（Q2 FY27）；FY27 訂閱指引上修至 $9.94-9.95B（+13%）；非 GAAP 營業利益率指引上修至 31.0%；agentic 新簽 ACV >$100M 佔新簽 >25%；共識 FY27／FY28／FY29 EPS 財報後一週上修 2.8%／4.5%／5.1%；FCF 利潤率 30%——實績沒有一項在惡化",
    "evidence_for": "cRPO 年增 15.5%→14.2%、總 RPO 年增 10.9%→8.0%、合約期年減（來源：摘要）、大型交易拉長；CFO 拒絕重申 35% 利潤率目標、對 Q1 指引數學缺口未對帳（來源：摘要）；SBC 佔營收 17.4% 讓 GAAP 營業利益率僅 11.8%——『便宜』是以非 GAAP 分子計的",
    "bear_case": "18 個月內虧 30% 的路徑：Silver Lake 破局（−15~−20% 回吐）疊加 Q3／Q4 FY27 cRPO 年增跌破 12%、FY28 指引 ≤+10%，市場以 12x FY28 EPS 定價 → 約 $150；監測指標＝私有化進展、cRPO 年增、FY28 指引",
    "monitor": [
      "cRPO 年增（連 2 季 <12%＝陷阱正在發生）",
      "總 RPO 年增與 cRPO 年增之差（早期續約充數的導數級警訊）",
      "GRR（<95%＝席次壓縮已波及留存）",
      "SBC 佔營收（回升至 >18%＝利潤率擴張是假的）",
      "FY28 框架是否重申 12-15%／33-36%"
    ],
    "verdict": "🟡",
    "label": "觀察期（便宜是否為 AI 重定價的帳單）"
  },
  "appendix_a": {
    "signal": "B",
    "moat_score": 7.5,
    "growth_durability": 7,
    "quality_score": 7.3,
    "ai_risk": "🟡",
    "long_term_confidence": "中",
    "val": "🟢",
    "ma": "-",
    "fpe_fy2": 14.82,
    "pct_5y": 1,
    "peg_fy2": 0.91,
    "upside_short_pct": 14.7,
    "upside_mid_pct": 33.9,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "B"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDAY_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY27": 11.06,
      "FY28": 12.9,
      "FY29": 14.7,
      "FY30": 16.5,
      "FY31": 18.3
    },
    "fy_end_month": 1,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-11",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q3 FY27 財報（管理層慣例 11 月下旬）",
      "impact": "高",
      "watch": "cRPO 年增 ≥12%；Q3 訂閱營收 $2.515B 指引兌現；agentic 新簽 ACV 佔比；FY27 訂閱指引是否再上修"
    },
    {
      "date": "2026-Q4",
      "date_precision": "quarter",
      "type": "other",
      "event": "Silver Lake 私有化洽談定案或破局",
      "impact": "高",
      "watch": "定案價 vs 假設性 $227；破局後股價是否回落 ≤$170"
    },
    {
      "date": "2026-Q4",
      "date_precision": "quarter",
      "type": "guidance",
      "event": "Financial Analyst Day 框架更新（CFO 稱 2026 年內，來源：摘要）",
      "impact": "高",
      "watch": "FY28 訂閱成長 12-15%／營業利益率 33-36%／每股 FCF $15 是否重申；AI 定價策略更新"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q4 FY27 財報＋FY28 指引",
      "impact": "高",
      "watch": "FY28 訂閱指引 ≥+11%；非 GAAP 營業利益率指引 ≥33%；SBC 佔營收 ≤16%"
    },
    {
      "date": "2027-Q2",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "Mobley 案集體認證與加州 FEHA 程序里程碑",
      "impact": "中",
      "watch": "集體認證是否成立；和解金額；是否限制 AI 篩選功能"
    },
    {
      "date": "2026-Q4",
      "date_precision": "quarter",
      "type": "product",
      "event": "Workday GO 中型市場夥伴通路首年成績",
      "impact": "低",
      "watch": "中型市場勝率是否如管理層所稱與大型企業相同（來源：摘要）"
    }
  ],
  "decision_inputs": {
    "signal": "B",
    "trap": "🟡",
    "val": "🟢",
    "ma": "-",
    "runway_post_y5": "🟢",
    "moat_trend": "→",
    "moat": "B",
    "capalloc_grade": "B",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 4.3,
    "irr_base_pct": 9.7,
    "ev5y_pct": 59.1,
    "price_at_dd": 195.79,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": 29.63,
    "momentum_overheated": true,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 4.5,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "prior_verdict": "觀望",
    "prior_role": null,
    "held_now": null
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "9b",
    "pacing": [
      "row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"
    ],
    "holding_cap": null,
    "requires_critic": [
      "QC-41：裁決強方向（進場）且屬競爭動態型（AI 替代／中型市場份額），需跨模型複核 agentic 替代軸的 🔴 是否被低估",
      "QC-19／playbook 12：8/13 單日近 30% 事件已歸因私有化傳聞而非基本面，複核首倉 1/3 是否仍偏高"
    ],
    "audit_rows": [
      {
        "row": "1",
        "condition": "基本面評級 signal = X → 迴避",
        "hit": false,
        "basis": "signal='B'"
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
        "basis": "moat_trend='→', moat='B'"
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
        "hit": true,
        "basis": "momentum_overheated=True"
      },
      {
        "row": "6",
        "condition": "基本面評級 signal = C → ≥ 觀望",
        "hit": false,
        "basis": "signal='B'"
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
        "basis": "signal='B', runway='🟢', val='🟢', moat_trend='→', week26=29.63, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"
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
        "basis": "signal='B', val='🟢'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": false,
        "basis": "signal='B', val='🟢', ma='-'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": true,
        "basis": "signal='B', val='🟢', ma='-'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": false,
        "basis": "signal='B', val='🟢', ma='-'"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": "首倉後加碼：Silver Lake 破局且股價 ≤$170 且 Q3 cRPO ≥12%；或 FY28 框架重申 12-15% 且 AI ARR ≥$600M",
    "exec_line": "新邊際資金：現價建首倉 1/3（約 1%），凍結加碼至 2026-11 Q3 財報確認 cRPO ≥12%；第二個 1/3 掛私有化破局回落 ≤$170，第三個 1/3 掛 FY28 框架重申＋AI ARR ≥$600M。已持有者：不加碼、不減碼；私有化定案 ≥$220 轉併購套利出清。不選清倉：實績（GRR 97%、指引上修）無一惡化；不選加碼至核心：護城河 B、AI 淨增量未證、8/13 起含事件溢價"
  },
  "triggers": [
    {
      "n": 1,
      "text": "cRPO 年增守 12%（H1）",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "12 個月訂閱 backlog 年增",
      "threshold": "連 2 季 <12% → 削弱；連 3 季 <10% → 反轉",
      "action": "削弱＝停止加碼；反轉＝減至首倉",
      "source_freq": "季度新聞稿／每季",
      "date": "2026-11-30",
      "evidence_refs": [
        "competitive_share_entrants#2"
      ]
    },
    {
      "n": 2,
      "text": "AI 淨增量（H3／R1）",
      "type": "假設驗證",
      "maps_to": "H3",
      "metric": "AI ARR 年增；agentic 新簽 ACV 佔比",
      "threshold": "AI ARR 年增 <40% 或 agentic 佔比 <15% 連 2 季",
      "action": "削弱＝停止加碼並重審護城河定價分數",
      "source_freq": "季度法說／每季",
      "date": "2027-02-28",
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#1",
        "substitute_technology#2",
        "supply_demand_durability#1"
      ]
    },
    {
      "n": 3,
      "text": "新簽動能與早期續約充數（R2）",
      "type": "風險",
      "maps_to": "R2",
      "metric": "總 RPO 年增；cRPO 與總 RPO 年增之差",
      "threshold": "總 RPO 年增 <6%，或 cRPO 年增高於總 RPO 年增 8pp 以上連 2 季（續約充數）",
      "action": "減倉至首倉",
      "source_freq": "季度新聞稿／每季",
      "date": "2026-11-30",
      "evidence_refs": [
        "competitive_share_entrants#1",
        "competitive_share_entrants#2",
        "supply_demand_durability#0"
      ]
    },
    {
      "n": 4,
      "text": "FY28 財務框架撤回（Single Thing）",
      "type": "Single Thing",
      "maps_to": "H1／H2",
      "metric": "Financial Analyst Day 或法說對 12-15% 訂閱成長框架的重申",
      "threshold": "下修至 <12%",
      "action": "減至首倉並重跑判斷；若營業利益率目標同步下修 → 清倉",
      "source_freq": "Financial Analyst Day／年度；法說／每季",
      "date": "2026-12-31",
      "evidence_refs": [
        "competitive_share_entrants#2"
      ]
    },
    {
      "n": 5,
      "text": "私有化事件（R4）",
      "type": "清倉",
      "maps_to": "R4",
      "metric": "Silver Lake 交易公告",
      "threshold": "定案價 ≥$220",
      "action": "部位轉併購套利，價差 <3% 時出清（複利論點終止）",
      "source_freq": "公司公告／事件",
      "date": "2026-12-31",
      "evidence_refs": [
        "major_events#0",
        "major_events#5",
        "lawsuit_class_action#1"
      ]
    },
    {
      "n": 6,
      "text": "加碼軌一（回檔）",
      "type": "加碼",
      "maps_to": "R4／H1",
      "metric": "股價；Q3 cRPO",
      "threshold": "私有化破局且股價 ≤$170 且 Q3 cRPO 年增 ≥12%",
      "action": "加第二個 1/3",
      "source_freq": "事件＋季度",
      "date": "2026-12-31",
      "evidence_refs": [
        "supply_demand_durability#2"
      ]
    },
    {
      "n": 7,
      "text": "加碼軌二（論點增強）",
      "type": "加碼",
      "maps_to": "H2／H3",
      "metric": "FY28 框架；AI ARR",
      "threshold": "框架重申 12-15%／33-36% 且 AI ARR ≥$600M",
      "action": "加第三個 1/3 至衛星上限",
      "source_freq": "Financial Analyst Day＋季度",
      "date": "2027-02-28"
    },
    {
      "n": 8,
      "text": "留存斷裂（thesis 級清倉）",
      "type": "清倉",
      "maps_to": "H1",
      "metric": "GRR；cRPO 年增",
      "threshold": "GRR <95% 且 cRPO 年增 <8% 連 2 季",
      "action": "清倉",
      "source_freq": "季度法說／每季",
      "date": null
    },
    {
      "n": 9,
      "text": "AI 僱用訴訟程序階梯（R3）",
      "type": "風險",
      "maps_to": "R3",
      "metric": "Mobley 案集體認證／和解；資料外洩集體訴訟",
      "threshold": "集體認證＋和解 >$500M 或功能禁令 → 減半；刑事／監管介入 → 清倉",
      "action": "減半或清倉",
      "source_freq": "法院 docket／事件",
      "date": "2027-06-30",
      "evidence_refs": [
        "regulatory_antitrust#0",
        "regulatory_antitrust#1",
        "major_events#3",
        "major_events#4",
        "lawsuit_class_action#0"
      ]
    },
    {
      "n": 10,
      "text": "估值過熱修剪",
      "type": "減碼",
      "maps_to": "H1",
      "metric": "FY28 前瞻本益比",
      "threshold": ">28x（自身短窗高 18.5x 上修 50%）",
      "action": "修剪至衛星下限，不單獨清倉",
      "source_freq": "月度",
      "date": null
    },
    {
      "n": 11,
      "text": "複審日期",
      "type": "複審日期",
      "maps_to": "H1／H2／H3",
      "metric": "Q4 FY27 財報＋FY28 指引後全面複審",
      "threshold": "—",
      "action": "重跑判斷；首倉凍結期至 2026-11 Q3 財報解除",
      "source_freq": "年度",
      "date": "2027-03-05"
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單與矛盾拓撲",
      "side_a": "方向一致：訂閱型現金機器（FCF 30%、GRR 97%、三年以上合約）；估值兩尺皆便宜（分位 <2%、PEG 0.9）；利潤率擴張與回購是可靠的第二引擎；共識財報後上修",
      "side_b": "矛盾拓撲＝集中單一軸：agentic AI 是否蠶食按員工計費基礎（護城河定價維度）；其餘（新簽拉長、SBC）為程度差異",
      "ruling": "爭議集中→點名定價維度為 binding 軸；信心不整體下修，但角色限衛星、Bear 30%",
      "evidence_level": "L1",
      "settle_metric": "cRPO 年增與 AI ARR 對席次壓縮的淨增量",
      "if_then": [
        "若 FY28 指引 ≥+11% 且 AI ARR ≥$800M → 角色可升核心候選",
        "若 cRPO 年增連 3 季 <10% → 減至首倉"
      ]
    },
    {
      "axis": "估值便宜 vs AI 結構性重定價（不可調和）",
      "side_a": "A 側：五年分位 <2%、PEG 0.9、指引上修、GRR 97%——市場錯在把『AI 會用軟體』讀成『AI 取代軟體』，Workday 是被 AI 讀寫的系統紀錄，Anthropic／OpenAI／Google 都跑 Workday（來源：摘要）",
      "side_b": "B 側：a16z 與 2026-02 財報後的 SaaS 重定價認為席次是 AI 的直接受害者；cRPO 減速、合約期年減、管理層在四場問答對席次 vs 消費拆分全數迴避（來源：摘要）；5 月前瞻本益比曾至 12.3x",
      "ruling": "選 A 側但打折：L1 實績（留存、指引、AI ACV）勝於 L3 敘事（a16z 文章）；以 L2 sourced 減速數據反駁 L1 的理由是『減速尚在雙位數、且部分來自聯邦預算而非 AI』。執行路徑：進場但衛星、首倉 1/3、Bear 30%。現在就賣的最強論證：(1) 8/13 起的價格是私有化溢價不是基本面；(2) 席次壓縮一旦顯影在 GRR 就來不及；(3) SBC 17% 讓 GAAP 分子只有非 GAAP 三分之一——逐點回應：(1) 標準情境 FY28 13.21×16-17x＝$211-225 仍高於現價，溢價回吐是加碼機會非清倉理由；(2) 故用 cRPO 與總 RPO 之差當導數級早警，不等 GRR；(3) 估值 PEG 以非 GAAP 計，但 FCF 口徑（每股 owner earnings 約 $12.7）給的便宜結論一致",
      "evidence_level": "L1 vs L3",
      "settle_metric": "FY28 指引與 AI ARR",
      "if_then": [
        "若 Q3 cRPO ≥12% 且私有化破局回落 ≤$170 → 加第二個 1/3",
        "若 cRPO 連 2 季 <12% → 停止加碼；連 3 季 <10% → 減至首倉"
      ],
      "evidence_refs": [
        "substitute_technology#0",
        "substitute_technology#1",
        "substitute_technology#2",
        "competitive_share_entrants#3",
        "supply_demand_durability#1",
        "supply_demand_durability#2",
        "competitive_share_entrants#2"
      ]
    },
    {
      "axis": "8/13 單日近 30% 事件歸因（私有化 vs 基本面）",
      "side_a": "13 週漲幅 35.7% 中約 24 個百分點來自 8/13 Silver Lake 報導（7/30 $160.34 → 8/13 $198.68），財報日 8/27 僅 +1.5%——價格事件屬併購傳聞，非基本面重估",
      "side_b": "同期共識 FY28 EPS 上修 4.5%、指引上修，基本面也在改善",
      "ruling": "歸因為事件主導：未定案前不讓事件改變裁決方向，只改節奏——首倉降至 1/3、凍結加碼至 Q3 財報；定案即複利論點終止（轉套利），破局即回檔加碼窗。股東律所受託責任調查屬訴前徵求原告，不改裁決",
      "evidence_level": "L1",
      "settle_metric": "Silver Lake 交易公告或撤回",
      "if_then": [
        "定案 ≥$220 → 併購套利出清",
        "破局且 ≤$170 → 加第二個 1/3；破局但股價不回落 → 不追"
      ],
      "evidence_refs": [
        "major_events#0",
        "major_events#5",
        "lawsuit_class_action#1",
        "capital_markets_pricing#1"
      ]
    },
    {
      "axis": "賣方分歧層級：事實 vs 框架",
      "side_a": "Deutsche 降持有 $145、BTIG 降中立、Cantor 5 月因『通路查核中性偏負』砍目標價——賣方為『高成長 SaaS』框架辦喪事",
      "side_b": "Bernstein $238、Goldman 上修——押利潤率與 AI 變現框架",
      "ruling": "分歧在框架層非事實層（雙方引用同一份 Q2 數字）；本檔論點是『成熟現金牛＋AI 選擇權』，不是賣方降評的高成長框架，故降評潮製造的是進場價而非反證。目標價全距 1.6x 未達離散警戒；共識中樞兩來源相差 $90 → 降低對自身 IRR 點估計的信心，角色限衛星",
      "evidence_level": "L2",
      "settle_metric": "FY28 指引",
      "if_then": [
        "若 FY28 指引 ≥+11% → 框架之爭由本檔勝",
        "若 ≤+9% → 賣方降評框架對，減至首倉"
      ],
      "evidence_refs": [
        "supply_demand_durability#0"
      ]
    },
    {
      "axis": "管理層指引可信度（來源：摘要）",
      "side_a": "FY26 逐季上修、FY27 兩次上修、FY28 框架 12-15%／33-36%——兌現紀錄良好",
      "side_b": "CFO 對 Q1 FY27 指引的 $25M 環比缺口未對帳、拒絕重申 35% 利潤率目標、把 FY27 成長從 15% 錨到 13% 卻不承認環境轉差；CEO 兩度以『下週再說』推遲 AI 數字",
      "ruling": "可調和：兌現紀錄勝於問答閃避，但閃避集中在『席次 vs 消費』與利潤率上限——正是 binding 軸。H2 信心設中；框架重申列 Single Thing",
      "evidence_level": "L2",
      "settle_metric": "Financial Analyst Day 框架重申",
      "if_then": [
        "重申 → H2 信心升高",
        "下修 → 減至首倉"
      ]
    },
    {
      "axis": "產業對帳（ID）",
      "side_a": "ID 生產力 Copilot（2026-04-27）：balanced、Phase II、Workday 列『垂直專屬資料』↑；ID Agentic AI 平台（2026-09-03）：split、priced_in mid",
      "side_b": "本檔：Workday 是被 AI 讀寫的資料持有者（與 ID 供給側一致），但 ID 的 ↑ 是分類層級判斷，未考慮按員工計費被席次壓縮的個股層風險——本檔 moat 趨勢取 → 非 ↑",
      "ruling": "與 ID 一致度高，分歧僅在個股層的計費模型風險；⚠分歧未達重跑 ID 門檻。機械選出的 primary 為生產力 Copilot；本檔判斷 Agentic AI 平台（較新、split）對 AI 替代軸更貼題，兩份並讀",
      "evidence_level": "L2",
      "settle_metric": "AI ARR 對席次壓縮淨增量",
      "if_then": [
        "淨增量為正 → 與 ID ↑ 收斂",
        "為負 → 建議重跑 ID 生產力 Copilot 的 Workday 定位"
      ]
    },
    {
      "axis": "前次觀望後漲 52.8%（錯過成本）",
      "side_a": "前份（2026-05-22，$121.85）判 B 觀望，等站回 W104 後 4 週；至今 +52.8%",
      "side_b": "本次翻為進場（條件式衛星）",
      "ruling": "上次觀望後漲 52.8%，本次翻面理由是：①前次 binding constraint 是週線位置的機械節奏閘，現行矩陣中週線只調節奏不擋裁決——前次觀望係已退役之閘所致，本次依現行規則重裁；②估值仍 🟢（PEG 0.9），實績（指引上修、AI ACV）改善；③不是因為『漲了所以追』——首倉只 1/3 且凍結至 Q3。跨 90 天（106 天），不受承繼保護",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "若私有化破局回落 → 以前次錯過價位區間（$150-170）補倉",
        "若定案 → 承認錯過複利、以套利收尾"
      ]
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "NOW／CRM 為同 tier",
      "side_b": "近 30 天 peer 裁決證據包未涵蓋",
      "ruling": "一句帶過，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：dca_verdict",
      "prior_field": "dca_verdict",
      "side_a": "本次＝進場（條件式衛星）",
      "side_b": "前份＝格式無此欄（verdict 文字為 B 觀望）",
      "ruling": "主因＝方法論變了（前次觀望係已退役之週線閘所致，現行矩陣重裁）；次因＝基本面（指引上修、AI ACV 揭露）；價格漲 60% 反而是逆風",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：dca_role",
      "prior_field": "dca_role",
      "side_a": "本次＝衛星",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（前份格式無角色欄）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：signal",
      "prior_field": "signal",
      "side_a": "本次 B",
      "side_b": "前份 B",
      "ruling": "無漂移",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：val",
      "prior_field": "val",
      "side_a": "本次 🟢",
      "side_b": "前份 🟢",
      "ruling": "無漂移；價格漲 60% 但 PEG 仍 <1，共識同步上修",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：ma",
      "prior_field": "ma",
      "side_a": "本次 -（證據包未涵蓋週線均線，不以推估填色）",
      "side_b": "前份 🟠",
      "ruling": "主因＝方法論／資料可得性（本輪證據包無 W52／W104／W250），非趨勢判斷改變；現價低於 52 週高 21%、26 週 +29.6%",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：trap",
      "prior_field": "trap",
      "side_a": "本次 🟡 觀察期",
      "side_b": "前份 🟢 非陷阱",
      "ruling": "主因＝基本面（cRPO／總 RPO 減速、合約期年減、產業倍數系統性下移為新亮燈）；次因＝方法論（本輪衰退表逐項對帳）",
      "evidence_level": "L1",
      "settle_metric": "cRPO 年增",
      "if_then": []
    },
    {
      "axis": "前份漂移：moat_trend",
      "prior_field": "moat_trend",
      "side_a": "本次 →",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動（前份格式無此欄）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：runway_post_y5",
      "prior_field": "runway_post_y5",
      "side_a": "本次 🟢",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：asym_ratio",
      "prior_field": "asym_ratio",
      "side_a": "本次 4.3",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：ev5y_pct",
      "prior_field": "ev5y_pct",
      "side_a": "本次 59.1%",
      "side_b": "前份無此欄（upside_5y 220% 為單一目標價口徑）",
      "ruling": "主因＝方法論（機率加權 vs 單點）；次因＝價格漲 60%",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：irr_base_pct",
      "prior_field": "irr_base_pct",
      "side_a": "本次 9.7%",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：max_dd_pct",
      "prior_field": "max_dd_pct",
      "side_a": "本次 −35~−50%",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：bull_5y_price",
      "prior_field": "bull_5y_price",
      "side_a": "本次 $528",
      "side_b": "前份無此欄（target_5y $390 單點）",
      "ruling": "方法論驅動（情境樹）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：bear_5y_price",
      "prior_field": "bear_5y_price",
      "side_a": "本次 $131",
      "side_b": "前份無此欄（bear_price $94.7 為短期錨）",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：p_bull_pct",
      "prior_field": "p_bull_pct",
      "side_a": "本次 25",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：p_bear_pct",
      "prior_field": "p_bear_pct",
      "side_a": "本次 30",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動（內生天花板超出 → 下限 30%）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：rearm_trigger",
      "prior_field": "rearm_trigger",
      "side_a": "本次＝加碼觸發（破局回落／框架重申）",
      "side_b": "前份＝等站回 W104 後 4 週（散文）",
      "ruling": "方法論驅動：週線閘退役，改事件與論點錨",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：price_at_dd",
      "prior_field": "price_at_dd",
      "side_a": "本次 $195.79",
      "side_b": "前份 $121.85",
      "ruling": "主因＝價格變了（+60.7%）：約 24 個百分點來自 8/13 私有化傳聞、其餘來自 6 月低點後的軟體板塊反彈與兩次指引上修；基本面同期共識 FY28 EPS 僅上修 4.5%",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：archetype",
      "prior_field": "archetype",
      "side_a": "本次 品質複利成長",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    },
    {
      "axis": "前份漂移：cycle_position",
      "prior_field": "cycle_position",
      "side_a": "本次 null（非循環）",
      "side_b": "前份無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": []
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "AI 淨增量檢驗式尚無分母：AI ARR >$400M 是分子，被席次壓縮蠶食的收入線沒人揭露；管理層在四場問答對『席次 vs 消費』拆分全數迴避（來源：摘要）。前提『淨增量為正』若不成立，Base 的 10%+ 訂閱成長要打到 5-7%",
        "evidence_refs": [
          "substitute_technology#2",
          "supply_demand_durability#1"
        ]
      },
      {
        "text": "超大規模雲雙重角色：代管集中於 AWS／Google／Microsoft 是 10-Q 自揭風險，而這三家同時是 AI 分發層競爭者——供應商可以決定 Workday agent 的推論成本與整合優先序",
        "evidence_refs": [
          "geo_supply_chain#0"
        ]
      },
      {
        "text": "Mobley 案規模：加州法院指出涵蓋約 11 億份申請，單一演算法訴訟可能擴成大規模集體訴訟；AI 招募線（HiredScore／Paradox）是 H3 的一部分",
        "evidence_refs": [
          "regulatory_antitrust#1",
          "regulatory_antitrust#0"
        ]
      },
      {
        "text": "SaaS 整合供應鏈資安：Salesloft Drift OAuth 外洩波及 700+ 組織，Workday 核心租戶未被入侵但已衍生消費者集體訴訟；Pipedream 併購後整合面更廣，攻擊面同步擴大",
        "evidence_refs": [
          "major_events#3",
          "major_events#4",
          "lawsuit_class_action#0"
        ]
      },
      {
        "text": "私有化受託責任調查：若定案價偏低（如假設性 $227 僅 16% 溢價），股東訴訟可能拖延交割，部位卡在套利價差中",
        "evidence_refs": [
          "major_events#5",
          "lawsuit_class_action#1"
        ]
      },
      {
        "text": "週線結構證據包未涵蓋：本檔未能判定價相對 W104／W250 位置，節奏依事件錨而非技術錨；若價實際低於 W250 且斜率轉負，首倉應再降",
        "evidence_refs": []
      }
    ],
    "failure_story": "5 年後虧 50%：agentic AI 讓客戶以更少 HR／財務人力跑更多流程，按員工計費基礎年年縮 3-5%，Flex Credits 補不到一半；訂閱成長降到個位數、利潤率卡 31%、市場給 10-11x，股價 $110-130。此故事的觸發＝FY28 框架撤回，與 Single Thing 直接撞上✅",
    "second_failure": "核心論點兌現但劣化：留存守住、利潤率到 36%、AI ARR 達 $1B——卻以『成熟現金牛』形態兌現（訂閱成長 8-9%），市場把估值框架從成長型 SaaS 切到成熟軟體 12-14x（Oracle／Medtronic 式十年不回），5 年報酬約 0~+20%。機率不可忽略，已反映在 Base 終端倍數只給 17x（不給 20x）與 Bull 只 25%",
    "max_dd": {
      "lo": -50,
      "hi": -35,
      "path_risk": "🟡",
      "trigger_time": "最可能觸發：2026 Q4 至 2027 Q1——私有化破局（−15~−20%）疊加 Q3／Q4 FY27 cRPO 跌破 12% 與 FY28 指引 ≤+10%，兩者同時發生時回到 $100-130 區間（2026-06 低點 $112 為 sourced 地板）；恢復峰值需 FY28 框架重申或 AI ARR 翻倍，估 18-30 個月；若 GRR 跌破 95% 則 thesis 已破不會恢復。範圍寬 15pp"
    }
  },
  "kill_metrics": [
    {
      "metric": "cRPO 年增",
      "bear_threshold": "連 2 季 <12% 警示；連 3 季 <10% 反轉",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "GRR",
      "bear_threshold": "<95%",
      "window": "每季",
      "source": "季度法說",
      "last_status": "ok"
    },
    {
      "metric": "agentic 新簽 ACV 佔比",
      "bear_threshold": "連 2 季 <15%",
      "window": "每季",
      "source": "季度法說",
      "last_status": "ok"
    },
    {
      "metric": "FY28 框架訂閱成長區間",
      "bear_threshold": "下修至 <12%",
      "window": "Financial Analyst Day",
      "source": "公司簡報",
      "last_status": "ok"
    },
    {
      "metric": "SBC 佔營收",
      "bear_threshold": ">18% 回升",
      "window": "每季",
      "source": "季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "Mobley 案程序",
      "bear_threshold": "集體認證＋和解 >$500M 或功能禁令",
      "window": "事件",
      "source": "法院 docket",
      "last_status": "warning"
    }
  ],
  "reasoning": {
    "archetype": "指紋：毛利 75.8%、FCF 利潤率 30.2%（TTM）、訂閱 93%、資本支出約 2.5% 營收 → 訂閱型品質複利（信心高）。\n雜訊：SBC 17.4% 讓 GAAP 營業利益率僅 11.8%，非 GAAP 31.1%——兩口徑差 19pp，品質度量以現金與 GAAP 雙看。\n對下游：用品質複利預設尺（PEG／前瞻本益比），不換尺。",
    "thesis": "H1 訂閱雙位數：FY27 指引 +13%、cRPO +14.2%（但自 15.5% 減速）→ 2 年門檻 cRPO ≥12%。\nH2 利潤率：31%→FY28 框架 33-36%、SBC 年降 1pp → GAAP 營業利益率 15%+。\nH3 AI 淨增量：AI ARR >$400M 三位數增、agentic ACV >25% 新簽 → 分母（席次蠶食）未揭露，故 Single Thing 設為框架撤回（最大 EPS 敏感度項）。",
    "industry": "HCM 市場 $37.5B→$77.4B（CAGR 8.5%）、Workday 份額約 22%、三強 58% → Phase II 擴張但倍數被重定價。\nID 對帳：生產力 Copilot balanced／Phase II，Workday 列垂直專屬資料 ↑；Agentic AI 平台 split——本檔取 → 因個股層計費模型風險。\n三軸裁決：雙向拉鋸——A 競爭惡化（中型市場、agentic 替代敘事）vs B 結構轉好（雲端換代、AI 加購）；利潤池未見 ≥5pp 淨流出。",
    "moat": "執行 7（Gartner 第 11 年、GRR 97%、但交易拉長、中型市場輸單）＋定價 8（97% 留存、按員工計費、賽局＝理性寡占；MSFT 成本更低且 FCF 足以攻擊 → 上限 8）→ 合併 7.5 → B。\n閘一：GAAP 營業利益率對 NOW 持平、對 CRM −10pp，spread 不為正且擴大 → 合併分不得 ≥8，一致。\n趨勢 →：執行穩、定價承壓，取對 thesis 更關鍵的定價維度；12 個月內 data point＝agentic ACV >25%（2026-08-27）與中型市場輸單（2026-08）。ROIC durability：ROIIC 20%×再投資 45%＝內生 9%，共識 16.3% 缺口歸因利潤率＋回購＋併購。",
    "growth": "跑道：訂閱約 $10B vs 公司 TAM $200B（來源：摘要）滲透 5%；即使以 HCM $37.5B 計亦僅 26% → ≥10 年、五年後 🟢（滲透 ≤35% 且 sourced 第二曲線：Sana 2026-02 GA、Flex Credits、Workday GO 2026-02）。\n分部：訂閱 FY27 +13% → FY28 +11-12% → FY29 +11%，加總與 Base 路徑 12.9／14.7 對得上（差 <5pp）。\n熄火壓測：成長降 15%／10%／5% → 倍數 16／13／11x → 對 FY28 EPS 13.21 為 $211／$172／$145（+8%／−12%／−26%）。衰退燈 2 個 → 🟡。",
    "quality": "FCF 利潤率 30.2% 對 NOW 31.0／CRM 34.2 同級；GAAP 營業利益率 11.7% 對 NOW 11.4 持平、對 CRM 21.9 落後——缺口全是 SBC（$462M／季＝GAAP 營業利益 148%）。\n營收與營業利益增速差：Q2 營收 +12.8% vs GAAP 營業利益 +26%（$248M→$313M）→ 負值＝利潤率擴張。\n回購：$5B／2 年對 FCF 約 $6B＝80% 觸警示但淨現金 $5.4B（來源：摘要）；淨回購約 1-1.5%／年，剔除後 EPS CAGR 約 15%。",
    "governance": "計分卡：M&A ROIIC 未證（Sana 2026-02 GA，第 3 年不可觀測）；回購收益率 5.6% 有保留過；SBC 淨稀釋 ≤0 過 → 1 明確＋1 保留 → B（保守取 B 非 A）。\n治理事件：創辦人 Bhusri 回鍋 CEO（來源：摘要）、Silver Lake 私有化洽談、股東律所訴前調查——無 SEC 調查／重編。\n薪酬結構與內部人交易證據包未涵蓋（數據限制）。",
    "valuation": "前瞻本益比＝195.79÷11.06＝17.7x（FY27）、÷13.21＝14.82x（FY28）。\nCAGR＝(15.42×1.13÷11.06)^(1/3)−1＝16.3% → PEG FY28 0.91、FY27 1.09；五年分位 trailing 本益比 0%／P/S 1.2%／EV/S 0% → 🟢（取較嚴仍 🟢）。\n目標：1Y 13.21×17＝$224.6（+14.7%）；2Y 15.42×17＝$262.1（+33.9%）；Bear 9.95×13＝$129.4（−33.9%）。三分量：Base IRR 9.7%＝EPS 10.6%＋re-rate −0.8%（17.7→17x）＋淨回購 1.2%，re-rate 佔比負 → 非估值依賴型。",
    "trap_analysis": "模式＝便宜的成熟軟體（市場提前重定價）。\n反證：GRR 97%、指引兩次上修、共識上修 4.5%、AI ACV >25%——實績無一惡化。\n正證：cRPO 15.5→14.2%、總 RPO 10.9→8.0%、合約期年減、CFO 閃避——減速真實但仍雙位數 → 🟡 觀察期，監測 cRPO 與總 RPO 之差。",
    "premortem": "失敗故事＝席次壓縮 → 成長個位數 → 10-11x → $110-130（與 Single Thing 撞上✅）。\n第二敗局＝兌現但以現金牛形態、框架切成熟軟體 12-14x → 已壓 Base 終端 17x。\nMax DD −35~−50%：破局回吐 15-20% 疊加 cRPO 跌破 12%，地板＝2026-06 $112；🟡 路徑風險，thesis 完整不因波動砍倉，註記深回撤心理準備。"
  },
  "evidence_dismissed": [],
  "plain": {
    "verdict_line": "進場，但只當衛星：首倉三分之一，其餘等事件與數字說話。",
    "verdict_sub": "現價買一小份，等私有化定案或破局、以及十一月財報的訂單數字，再決定補不補後兩份。",
    "five": {
      "how_it_makes_money": "賣企業的人資、薪資與財務雲端系統，按員工人數收年費，合約三年以上不可取消。九成三收入是訂閱，客戶留存率九成七。",
      "why_now": "股價只有明年獲利的十七倍多，五年來最便宜的一段。市場怕 AI 讓企業少用人、少付席次費，但實績沒有一項在惡化。",
      "why_this_size": "護城河只有中上、AI 是否真的蠶食席次還沒有答案。八月中起的股價又含了私有化傳聞的溢價，所以只給衛星、先買三分之一。",
      "biggest_fear": "AI 代理人讓客戶用更少人跑更多流程，按人頭計費的基礎年年縮。管理層在四場問答都迴避拆分席次與用量收入，這是最大的問號。",
      "how_to_act": "現價買三分之一，十一月財報前不加碼。私有化破局跌到一百七十以下再補一份，公司重申中期成長框架再補最後一份。"
    },
    "business": {
      "what_to_whom": "把大企業的人資、薪資、財務流程搬到同一套雲端系統，客戶是財富五百強的六成五以上，一萬一千多家。",
      "why_customers_stay": "換系統要搬資料、換薪資、重訓員工，合約三年起跳、年度預收。留存率九成七，有保險公司回頭簽了十年。",
      "moat_direction": "等級中上、方向持平。執行面穩（連續十一年被評為領導者），最弱處在定價：中型市場輸給新創，AI 席次壓縮的敘事正在打折按人頭計費。"
    },
    "bets": [
      {
        "claim": "訂閱收入未來三年守住每年一成以上的成長。",
        "wrong_when": "十二個月訂單餘額年增連兩季低於一成二。"
      },
      {
        "claim": "利潤率繼續每年擴張兩個百分點，股票薪酬佔比逐年下降。",
        "wrong_when": "公司在分析師日把中期利潤率目標從三成三到三成六往下修。"
      },
      {
        "claim": "AI 產品帶來的新收入大於被壓縮的席次收入。",
        "wrong_when": "AI 年化收入成長連兩季掉到四成以下，或公司不再揭露這個數字。"
      }
    ],
    "fears": [
      {
        "clock": "⚡",
        "text": "私有化破局，八月中以來約兩成四的事件溢價回吐；或定案在二百二十七附近，五到十年的複利換成一次性一成六。"
      },
      {
        "clock": "🔥",
        "text": "AI 蠶食席次：訂單餘額年增從一成五降到一成四已在減速，若連兩季跌破一成二就是警訊。"
      },
      {
        "clock": "🐢",
        "text": "AI 招募工具的歧視訴訟涵蓋約十一億份申請，若集體認證成立、和解超過五億美元，AI 招募線的變現會被綁住。"
      }
    ],
    "market_wrong": "市場把「AI 會用軟體」讀成「AI 取代軟體」。Workday 是被 AI 讀寫的系統紀錄，連 AI 公司自己都跑 Workday。共識假設席次壓縮會顯影在留存與訂單，但留存仍九成七、指引兩次上修。我押的是 AI 新收入補得回席次壓縮，而市場押的是補不回。",
    "growth_funding": "內生成長天花板約百分之九，共識獲利年增一成六，缺口靠利潤率擴張、回購與併購補，不靠估值重估。",
    "stories": {
      "bull": "AI 年化收入翻倍再翻倍、用量計費補回席次壓縮，訂閱成長回到一成五、利潤率三成六。市場把它重新歸類為 AI 受惠的資料持有者，五年翻近三倍。",
      "base": "訂閱成長一成三慢慢降到一成，利潤率走到三成四，回購每年抵掉一點稀釋。倍數持平，五年約六成報酬，年化接近一成。",
      "bear": "客戶用更少人跑更多流程，按人頭計費的基礎年年縮，訂閱成長剩個位數。市場改用成熟軟體的十一倍定價，五年跌三成。"
    },
    "change_my_mind": [
      {
        "what": "十二個月訂單餘額年增",
        "threshold": "連兩季低於一成二",
        "then": "停止加碼；連三季低於一成就減回首倉",
        "when": "2026-11 起逐季"
      },
      {
        "what": "客戶留存率與訂單餘額同時斷裂",
        "threshold": "留存低於九成五且訂單年增連兩季低於百分之八",
        "then": "清倉",
        "when": "—"
      },
      {
        "what": "私有化交易公告",
        "threshold": "定案價二百二十以上",
        "then": "部位轉為套利、價差收斂到三個百分點內就出清",
        "when": "2026-12-31 前"
      }
    ],
    "prior_compare_reason": "主因是方法論：前份觀望是被週線位置的節奏閘擋住，現行規則裡週線只調節奏不擋裁決。次因是基本面：指引兩次上修、AI 新簽佔比首次揭露。",
    "how_to_lose": "第一種死法：AI 席次壓縮讓成長掉到個位數，市場給十一倍，股價回到一百一到一百三。第二種死法：一切都兌現，但以成熟現金牛的形態兌現，估值框架切到成熟軟體的十二到十四倍，五年報酬接近零。還有一種不算虧的失敗：私有化定案，複利換成一次性溢價。",
    "evidence_quality": "覆蓋十二軸，關稅與臨床軸不適用；營運數字全部是二零二六年七月底的最新一季。最新一季法說逐字稿檔案缺失，前四季與三場會議只讀了摘要，管理層閃避問答的判斷來自摘要而非親讀。"
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


