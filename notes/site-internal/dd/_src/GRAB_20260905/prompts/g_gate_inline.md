你是 stock-analyst v17 的**判斷層閘（gate）**，標的 GRAB（20260905）。你未參與寫判斷，這是一次跨模型冷讀。你的任務只有一件：**依下列 ①–⑦ 逐條複核判斷物，計數判斷級 🔴**。

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

## 輸出（一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20260905/gate_audit.md`，格式固定，下游機械解析）

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

**輪次上限 `6` 輪。** 一次 Write 完成，寫完即回報，不要回讀自己寫的 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20260905/gate_audit.md`。

## 回報（≤100 字）

判斷級 🔴 = N、🟡 = M，以及 🔴 各條的軸別與指向欄位。


===== BUNDLE =====

## ① 任務頭

標的：GRAB　日期：20260905　角色：stock-analyst v16.2 三步制的判斷層 critic（gate） agent。

輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。

---

## ③ Evidence 緊湊版

ticker=GRAB　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 3.42, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-08-03", "trading_days_since": 25, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 1, "current": 31.09, "high": {"value": 84.67, "date": "2025-12-31"}, "low": {"value": 84.67, "date": "2025-12-31"}, "current_percentile_within_annual_points": 50.0}, "ps": {"n_points": 4, "current": 3.75, "high": {"value": 9.24, "date": "2022-12-31"}, "low": {"value": 5.4, "date": "2023-12-31"}, "current_percentile_within_annual_points": 0.0}, "ev_s": {"n_points": 4, "current": 2.54, "high": {"value": 8.83, "date": "2022-12-31"}, "low": {"value": 4.4, "date": "2023-12-31"}, "current_percentile_within_annual_points": 0.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 3.51, "fy1_eps": 0.09, "fwd_pe": 39.0}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 3.54, "fy1_eps": 0.09, "fwd_pe": 39.33}, {"snapshot_date": "2026-06-04", "price_used": 3.34, "fy1_eps": 0.09, "fwd_pe": 37.11}, {"snapshot_date": "2026-06-23", "price_used": 3.55, "fy1_eps": 0.09, "fwd_pe": 39.44}, {"snapshot_date": "2026-07-16", "price_used": 3.57, "fy1_eps": 0.08, "fwd_pe": 44.62}, {"snapshot_date": "2026-07-30", "price_used": 3.5, "fy1_eps": 0.08, "fwd_pe": 43.75}, {"snapshot_date": "2026-08-13", "price_used": 3.62, "fy1_eps": 0.13, "fwd_pe": 27.85}, {"snapshot_date": "2026-08-28", "price_used": 3.42, "fy1_eps": 0.13, "fwd_pe": 26.31}, {"snapshot_date": "2026-09-04", "price_used": 3.42, "fy1_eps": 0.13, "fwd_pe": 26.31}], "current": 26.31, "high": 44.62, "low": 26.31, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": 2.4, "return_26w_pct": -14.07, "excess_return_13w_pct": -2.14, "excess_return_26w_pct": -28.59, "benchmark": "^GSPC", "rsi14": 42.06, "rsi14_usable": true, "distance_from_52w_high_pct": -46.98, "distance_from_52w_low_pct": 4.59, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 0.13, "fy2": 0.14, "fy3": 0.19}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 0.13, "fy2": 0.14, "fy3": 0.19}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 0.09, "fy2": 0.14, "fy3": 0.2}, "fy1": {"revision_pct": 0.0, "from": 0.13, "to": 0.13, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 0.0, "from": 0.14, "to": 0.14, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 0.0, "from": 0.19, "to": 0.19, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 44.44, "fy2_revision_90d_pct": 0.0, "fy3_revision_90d_pct": -5.0, "stale": false, "note": null}, "peer_financials": {"GRAB": {"gross_margin_pct": 43.63, "operating_margin_pct": 8.9, "fcf_margin_pct": -4.99, "rd_intensity_pct": 11.18, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "SE": {"gross_margin_pct": 44.27, "operating_margin_pct": 8.42, "fcf_margin_pct": 19.06, "rd_intensity_pct": 4.6, "fiscal_period_as_of": "TTM ending 2026-03-31（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "UBER": {"gross_margin_pct": 42.31, "operating_margin_pct": 12.13, "fcf_margin_pct": 18.32, "rd_intensity_pct": 6.77, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "DASH": {"gross_margin_pct": 51.41, "operating_margin_pct": 4.8, "fcf_margin_pct": 13.46, "rd_intensity_pct": 10.74, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "MELI": {"gross_margin_pct": 42.68, "operating_margin_pct": 8.26, "fcf_margin_pct": 35.27, "rd_intensity_pct": 7.33, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}}, "edgar_concentrations": {"filing_type": null, "filing_date": null, "url": null, "excerpt": null, "note": "GRAB 無 10-Q/10-K（可能為外國私募發行人，改申報 20-F/6-K），本項留 null"}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 2026（季度截至 2026-06-30，新聞稿發布於 2026-08-04）", "items": [{"metric": "GAAP 營收", "value": 997, "unit": "US$M", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "Grab Holdings 官方新聞稿《Grab Reports Record Second Quarter 2026 Results》SEC 6-K https://www.sec.gov/Archives/edgar/data/0001855612/000185561226000123/a2026q2-earningspressrelea.htm；同步稿 grab.com/sg/press", "vs_consensus": "分析師共識約 $989.9M–$1.00B（來源分歧：Yahoo Finance 引 $989.86M／Zacks 引 $1.00B），實際 $997M 落於共識附近，依來源不同為小勝或小幅未達", "prior_quarter": "Q1 2026: $955M（QoQ +4.4%）；YoY +22%（固定匯率 +21%）。分部：Deliveries $531M(+21%)／Mobility $331M(+12%)／Financial Services $134M(+59%)"}, {"metric": "Adjusted EBITDA 利益率（Grab 主要非GAAP獲利指標，未單獨揭露『non-GAAP營業利益率』）", "value": 16.9, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "同上 Grab Q2 2026 新聞稿；Adjusted EBITDA $168M ÷ 營收 $997M", "vs_consensus": "新聞稿未附第三方共識值；YoY 大幅擴張（13.3%→16.9%），Adjusted EBITDA 金額 YoY +54%", "prior_quarter": "Q1 2026: 16.2%（Adjusted EBITDA $154M ÷ 營收 $955M，YoY +46%）"}, {"metric": "GAAP 營業利益率", "value": 1.9, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "同上 Grab Q2 2026 新聞稿；GAAP 營業利益 $19M ÷ 營收 $997M", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "Q1 2026: 2.3%（營業利益 $22M ÷ 營收 $955M）；Q2 2025 為 0.9%（營業利益 $7M），YoY 營業利益金額由 $7M 增至 $19M"}, {"metric": "自由現金流（Adjusted Free Cash Flow）", "value": 73, "unit": "US$M", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "同上 Grab Q2 2026 新聞稿現金流量表與非GAAP調節表", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "Q1 2026 Adjusted FCF: $98M（Q1 營運現金流為 -$59M，季節性年度獎金/供應商付款所致）；TTM（至2026-06-30）Adjusted FCF: $450M；Q2 單季營運現金流 $56M"}, {"metric": "股權薪酬（SBC，equity-settled share-based payments）占營收比重", "value": 6.22, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "同上 Grab Q2 2026 新聞稿現金流量表揭露 SBC $62M；占比為 $62M ÷ 營收 $997M 自算", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "Q1 2026: SBC $78M ÷ 營收 $955M = 8.17%（Q1 因年度股權授予季節性高峰）；SBC 金額 QoQ -21%、YoY +2%（Q2 2025 SBC 約 $60.8M，換算自新聞稿揭露的 YoY +2% 敘述）"}, {"metric": "管理層 FY2026 全年指引（本季上修）", "value": null, "unit": "US$B revenue（區間）／US$M Adjusted EBITDA（區間）", "as_of": "公告於 2026-08-04，涵蓋 FY2026 全年（截至 2026-12-31）", "source": "同上 Grab Q2 2026 新聞稿；區間：營收 $4.10B–$4.15B（YoY +22%~+23%）、Adjusted EBITDA $720M–$740M（YoY +44%~+48%）", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "此前指引（2026-05-05 隨 Q1 2026 發布）：營收 $4.04B–$4.10B、Adjusted EBITDA $700M–$720M；本次為上修"}, {"metric": "Monthly Transacting Users（MTU，平台活躍度指標，類 MAU）", "value": 54, "unit": "百萬 users（新聞稿標題數；分部加總後精確值 53.9M）", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-08-04）", "source": "同上 Grab Q2 2026 新聞稿", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "Q1 2026: 51.6M（QoQ +4.7%）；YoY +17%"}, {"metric": "On-Demand GMV per MTU（類 ARPU 指標，六個月累計口徑）", "value": 261, "unit": "US$（六個月期，非單季數字）", "as_of": "六個月期至 2026-06-30（公告於 2026-08-04）", "source": "Grab Q2 2026 法說會逐字稿／新聞稿補充揭露（Motley Fool／Globe and Mail 轉載逐字稿）", "vs_consensus": "新聞稿未附第三方共識值", "prior_quarter": "去年同期六個月期至 2025-06-30: $249，YoY +5%；單季 On-Demand GMV per MTU 口徑 YoY +3%。分部：Deliveries GMV/MTU（六個月）$286（YoY+5%）／Mobility GMV/MTU（六個月）$133（YoY+2%）"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-01-28 | Grab strengthened its regional food delivery leadership, growing GMV market share to ~55% in 2025 (up from 53.8% in 2024) as Southeast Asia food delivery GMV grew 18% to US$22.7B; ShopeeFood overtook foodpanda in GMV terms to become the regional #2 platform. | Momentum Works, "Southeast Asia food delivery GMV grew 18% to hit US$22.7B in 2025" (thelowdown.momentum.asia) | moat_trend,thesis.H |
| competitive_share_entrants#1 | 0 | 2025-12-11 | Indonesia's antitrust regulator KPPU issued its strongest-yet warning over the rumored Grab-GoTo merger, stating it can cancel any deal found to substantially lessen competition; regulator flagged risk to pricing and driver incentives, noting a combined entity would exceed 90% share of Indonesian ride-hailing and push HHI far above conventional antitrust thresholds. | MLex, "Indonesia's antitrust chief issues stern warning over rumored GoTo–Grab merger" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#2 | 0 | 2026-04-01 | Grab-GoTo merger talks remain unresolved: Bloomberg reported in January 2026 that the deal had snagged on issues involving state-backed shareholder Danantara's stake in GoTo; as of April 2026 the deal status was described as in limbo, with market consensus expecting a resolution (approval with conditions, or abandonment) by late 2026. | Bloomberg (Jan 2026) reporting as referenced in MLex/Jakarta Globe coverage of the Grab-GoTo merger | moat_trend,decision_inputs.bear,triggers |
| competitive_share_entrants#3 | - | 2025-10-01 | inDrive (reverse-bidding model, ~10% commission) is the fastest-growing ride-hailing challenger in the Philippines: it had transported passengers 7x versus its own prior-year base during 2025, reached ~16,000 active drivers by October 2025, and confirmed plans to launch in two additional Philippine cities in 2026 — competing directly with Grab's ~90% dominant Philippines ride-hailing share (held since acquiring Uber's SEA operations in 2018). | NoypiGeeks, "inDrive transported 7x more passengers in the Philippines this 2025" | moat_trend,thesis.R |
| competitive_share_entrants#4 | - | 2026-05-01 | Bolt entered Thailand with EV ride-hailing service in May 2026, adding to competition from LINE MAN against Grab's estimated ~50% Thailand ride-hailing share. | Brineweb, "Grab vs. Uber: Who's Winning the Southeast Asian Market in 2026?" | thesis.R,moat_trend |
| customer_second_source#0 | - | 2026-01-01 | Running on multiple food-delivery platforms (Grab, foodpanda, ShopeeFood/GoFood) simultaneously is now standard practice for Southeast Asian restaurant merchants, used to reduce dependency on any single platform and negotiate better commission terms — the functional equivalent of 'second-sourcing' on the merchant side of Grab's two-sided marketplace. | Eats365 POS, "Best Food Delivery Platform for Malaysian Restaurants Compared 2026" | moat_trend,thesis.R |
| customer_second_source#1 | - | 2026-01-01 | High commissions (cited range 15-35%) charged by delivery platforms are squeezing restaurant-owner margins in Southeast Asia, pushing owners toward hybrid multi-platform strategies for survival rather than remaining single-platform (Grab-only) merchants. | Creative For More, "Food Delivery Marketing in Asia: Grab, foodpanda, and Deliveroo Compared" | moat_trend,decision_inputs.bear |
| customer_second_source#2 | + | 2026-01-01 | Grab's counter to merchant multi-homing is the 'GrabSignatures' program, which signs restaurant brands to be exclusively available on Grab (i.e., not listed on foodpanda, Deliveroo, or ShopeeFood), working against the industry-wide merchant diversification trend rather than tolerating it. | Creative For More, "Food Delivery Marketing in Asia: Grab, foodpanda, and Deliveroo Compared" | moat_trend |
| customer_concentration_credit#0 | 0 | 2023-12-31 | Grab 20-F（FY2023）風險揭露原文：因服務對象橫跨多地區的廣泛客群，公司認定沒有任何單一客戶或客戶群佔已認列營收的顯著比重（未觸及 10% 集中度揭露門檻）。 | SEC EDGAR — Grab Holdings Ltd Form 20-F FY2023 (sec.gov/Archives/edgar/data/1855612/000095017024037611/ck0001855612-20231231.htm) | decision_inputs.bear,thesis.R |
| customer_concentration_credit#1 | + | 2026-05-01 | Grab 旗下數位銀行合資體 GXS（新加坡）/GX Bank（馬來西亞）放款組合於 2026Q1 年增 130% 至約 US$14.38億（GXS 單體 2025 年較 2024 年成長 323%、突破 S$10億），但預期信用損失率（ECL ratio）同期由 6.8% 降至 4.6%，管理層歸因於運用 Grab 生態系交易數據做全信用週期風險評分。 | Fintech Singapore「Grab's Loanbook Exceeds US$1 Billion in Single Quarter for The First Time」＋ DealStreetAsia「GXS loan book rises 4x in 2025 riding on Grab's ecosystem muscle」 | thesis.H,decision_inputs.bear,moat_trend |
| supply_demand_durability#0 | + | 2026-01-01 | 東南亞線上外送市場預測 2023-2027 CAGR 約 17.54%，2027 年市場規模達 US$455.3 億；另一組預測外送 GMV 由 2025 年 US$230 億成長至 2030 年 US$360 億（CAGR 9.4%），顯示需求端仍處結構性擴張階段。 | Statista Market Insights — 'Online Food Delivery: Southeast Asia' outlook | thesis.H,valuation |
| supply_demand_durability#1 | 0 | 2025-11-01 | 2026 年東南亞叫車/外送競爭格局被描述為已『成熟』，同業普遍收斂激進司機/商戶補貼；但 Q3 2025 財報顯示補貼仍佔 GMV 約 10%，若補貼率上升 100bp 將增加約 US$2.2 億年化成本，顯示獲利對競爭強度（供給端補貼紀律）仍高度敏感、尚非完全脫鉤的結構性狀態。 | GabGrowth — 'Grab Holdings: The 2026 Thesis' | thesis.H,decision_inputs.bear,moat_trend |
| supply_demand_durability#2 | 0 | 2026-04-01 | Indonesia 競爭委員會（KPPU）對 Grab–GoTo 合併案示警定價、司機誘因與市場競爭風險；截至 2026 年 4 月，該併購案因一家國營背景股東持股問題仍卡關未決，市場普遍預期年底前才會有結果——若合併後放緩補貼戰，供給端競爭壓力可望結構性下降，但目前仍屬未實現的監理不確定性。 | The Jakarta Post op-ed（2026-01-08）＋ Kapronasia／DigitalInAsia 對 Grab-GoTo 併購進度的報導 | thesis.R,decision_inputs.bear,triggers |
| supply_demand_durability#3 | - | 2026-08-01 | Rakuten Insight 調查（N=1,003）顯示 82% 受訪者表示若油價推升叫車/外送價格將調整使用頻率；inDrive 觀察到消費者對價格更敏感、行程更挑剔，但日常代步剛性需求仍支撐整體叫車量未崩落，顯示需求面對價格具韌性但非全然無彈性。 | New Straits Times — 'Ride-hailing, delivery demand holds despite cost squeeze' | thesis.H,decision_inputs.bear |
| regulatory_antitrust#0 | - | 2026-05 | Indonesia's President Prabowo Subianto announced in May 2026 a cut to ride-hailing platform commissions (including Grab) to a maximum of 8% of fares, down from around 20% previously; Indonesia generates about 23% of Grab's revenue and an analyst estimated 5-10% downside risk to 2026 EBITDA from the change. | Nikkei Asia / KrASIA, "Grab faces regulatory headwinds in Indonesia, its key ride-hailing market" | thesis.R,decision_inputs.bear,valuation |
| regulatory_antitrust#1 | - | 2026-07-21 | Grab's proposed acquisition of foodpanda's Taiwan business is under review by Taiwan's Fair Trade Commission; a Taiwanese legislator publicly called the deal 'fake competition and real monopoly,' and critics raised national-security concerns tied to Grab's mapping partnership with Huawei's Petal Maps, ties to Chinese autonomous-vehicle firm WeRide, and an R&D center in Beijing. | CommonWealth Magazine, "Grab's Taiwan Gamble: A Regulatory Gauntlet, a Subsidy War, and an Eight-Year Bet" | thesis.R,decision_inputs.bear,moat_trend |
| regulatory_antitrust#2 | 0 | 2026 | Grab and Gojek together hold over 91% of Indonesian ride-hailing; a rumoured Grab acquisition of GoTo's on-demand services has drawn antitrust scrutiny from Indonesia's competition regulator, and the Grab-GoTo merger talks have stalled amid mounting antitrust concerns over unprecedented market concentration. | Asian Legal Business, "THE BRIEFS: Grab-GoTo merger stalls as antitrust scrutiny mounts" | thesis.R,moat_trend,decision_inputs.bear |
| regulatory_antitrust#3 | + | 2025-03 | Malaysia's Court of Appeal in March 2025 dismissed the Malaysia Competition Commission's (MyCC) appeal seeking to reinstate a proposed RM86.77 million (~US$19.5M) fine against Grab entities for alleged abuse of dominant position (restrictive driver-advertising clauses), ruling MyCC's handling of the investigation was 'cavalier'; the case originated from a 2019 investigation. | MLex / Competition Policy International, "Grab wins Malaysian antitrust legal battle as regulator's appeal dismissed" | thesis.R,decision_inputs.bear |
| reg_tariff_export | - | - | (status=none；無 findings) |  |  |
| geo_supply_chain#0 | - | 2026-05-01 | Indonesian President Prabowo Subianto signed a presidential regulation (announced 2026-05-01) cutting the maximum commission ride-hailing platforms (Grab, Gojek) can take from drivers on motorcycle (GrabBike) rides from 20% to 8%, effective for Grab from 2026-07-01; market commentary estimated a 5-10% downside risk to Grab's 2026 EBITDA, though the direct hit is concentrated in Indonesia's motorcycle segment rather than Grab's full mobility book (Malaysia relies more on GrabCar). | Jakarta Globe, "Grab and Gojek Cut Motorcycle Ride Commissions to 8% Following Prabowo's Pressure"; Nikkei Asia, "Grab faces regulatory headwinds in Indonesia, its key ride-hailing market" | thesis.R,decision_inputs.bear,valuation |
| geo_supply_chain#1 | - | 2024-12-31 | Grab's FY2024 revenue was geographically concentrated in three Southeast Asian markets: Malaysia 29.2%, Indonesia 23.0%, Singapore 20.7%, together contributing over 70% of total revenue — meaning a single-country regulatory action (e.g. Indonesia's commission cap) carries outsized consolidated impact rather than being diversified across many markets. | compoundwithrene.com, "Deep Dive: Grab Holdings Ltd ($GRAB) – Part 4" (citing Grab FY2024 geographic revenue breakdown) | thesis.R,moat_trend,decision_inputs.bear |
| end_markets#0 | + | 2026-08-04 | Mobility segment: Q2 2026 GMV grew 18% YoY to $2,214M and revenue grew 12% YoY to $331M, with transactions up 28% YoY outpacing GMV growth on adoption of affordable/saver product tiers; management guided to resilient full-year 2026 Mobility GMV growth with Adjusted EBITDA margins held within historical ranges, and raised full-year guidance. | Grab Holdings, "Grab Reports Record Second Quarter 2026 Results, Raises Full-Year Guidance and Announces $750 Million Share Repurchase Program" (Grab IR / Q2 2026 Earnings Prepared Remarks, Aug 4 2026) | thesis.H,decision_inputs.bear |
| end_markets#1 | - | 2026-08-04 | Mobility segment: elevated regional fuel prices pressured margins in Q2 2026, requiring $7M in driver support programs; this caused Mobility revenue growth (12% YoY) to lag GMV growth (18% YoY) and transaction growth (28% YoY) via take-rate compression from lower ticket sizes and higher incentives. | Grab Holdings Q2 2026 Earnings Prepared Remarks (Grab IR, Aug 4 2026) | thesis.R,decision_inputs.bear |
| end_markets#2 | + | 2026-08-04 | Deliveries segment: Q2 2026 revenue grew 21% YoY to $531M and GMV grew 22% YoY, driven by GMV expansion and continued momentum in the advertising business. | Grab Holdings Q2 2026 Earnings Prepared Remarks / Press Release (Grab IR, Aug 4 2026) | thesis.H |
| end_markets#3 | 0 | 2026-03-24 | Deliveries segment / market expansion: Grab agreed to acquire Delivery Hero's foodpanda Taiwan delivery business for $600M (cash-free, debt-free); foodpanda Taiwan generated approximately $1.8B GMV and was profitable on an adjusted EBITDA basis in 2025. The deal is Grab's first market entry outside Southeast Asia, into a Taiwan delivery market that remains a duopoly (Uber Eats / foodpanda) after Taiwan's Fair Trade Commission blocked Uber's 2024 bid to acquire foodpanda over concerns the combined entity would control ~90% of the market. | Grab press release, "Grab to Acquire Delivery Hero's foodpanda Delivery Business in Taiwan"; TNGlobal, "Grab's Foodpanda Taiwan deal offers scale and new growth options - Maybank" | thesis.H,decision_inputs.bear |
| end_markets#4 | + | 2026-08-04 | Financial Services segment: Q2 2026 revenue grew 59% YoY to $134M; total loans disbursed grew 72% YoY to an all-time high of $1.2B; Gross Loan Portfolio scaled 197% YoY to $2.3B; digital bank deposits across GXS Bank (Singapore), GXBank (Malaysia) and Superbank (Indonesia, control obtained May 2026) grew to $2.5B. Management guides Financial Services to reach Adjusted EBITDA profitability in 2H2026 and Gross Loan Portfolio to exceed $3B by year-end 2026 following Superbank consolidation and the Stash acquisition. | Grab Holdings Q2 2026 Earnings Prepared Remarks / Press Release (Grab IR, Aug 4 2026) | thesis.H,moat_trend |
| substitute_technology#0 | 0 | 2026-04-01 | Grab and Chinese robotaxi operator WeRide launched Southeast Asia's first public driverless ride-hailing service in April 2026, running an 11-vehicle autonomous fleet along two approved routes in Singapore's Punggol neighborhood via Grab's app (branded Ai.R), with WeRide's autonomous driving tech integrated into Grab's fleet management, vehicle matching and routing system. | Bloomberg, "Singapore Gets Robotaxis as Grab, WeRide Launch Driverless Cars" | moat_trend,thesis.H |
| substitute_technology#1 | + | 2025-08-01 | Grab made an investment in WeRide (announced August 2025, expected to finalize mid-2026) to accelerate deployment and commercialization of Level 4 robotaxis and shuttles across Southeast Asia, positioning Grab as WeRide's regional platform/deployment partner rather than being disintermediated by it. | Asia Tech Review, "Grab races after autonomous vehicle tech after making its largest investment bet ever" | moat_trend,thesis.H |
| substitute_technology#2 | - | 2026-01-01 | Rival Singapore taxi operator ComfortDelGro separately partnered with Pony.ai to launch driverless rides on a 12km Singapore route pending regulatory approval, and Baidu is reported to plan entry into Singapore and Malaysia with its own robotaxi service — meaning multiple non-Grab-affiliated autonomous-driving operators are entering Grab's core Southeast Asia ride-hailing markets in parallel. | Zag Daily, "Singapore's robotaxi rivalry grows as Pony AI opens bookings"; Finance Yahoo/Zacks, "China's AV Push: BIDU, PONY & WRD Lead the Robotaxi Revolution" | thesis.R,decision_inputs.bear,moat_trend |
| substitute_technology#3 | + | 2026-01-01 | Autonomous vehicles deploying in Southeast Asia face region-specific operational limits not present in the US/China: flash flooding in megacities like Jakarta, Manila and Bangkok can alter routing on short notice and break an AV's pre-mapped operational design domain, and ride-hailing driving income is a politically sensitive livelihood issue that regional governments are prioritizing protecting — both factors slow the pace at which AVs can scale to substitute Grab's human-driver network. | The Driverless Digest, "AVs Are Coming to Southeast Asia. The Global Playbook is Not" | thesis.R,decision_inputs.bear |
| channel_business_model_shift#0 | + | 2026-05-31 | Grab is consolidating PT Superbank Indonesia into its digital-banking subsidiary GXS Bank after Singtel Alpha Investments transferred its Superbank stake to GXS Bank, lifting Grab's combined ownership above 50% and bringing Superbank's results into Grab's Financial Services segment — a structural shift of Grab's business mix from pure ride-hailing/delivery take-rate toward embedded digital banking. | The Asian Banker, "Grab takes control of Indonesia's Superbank, deepening SEA fintech push" | thesis.H,moat_trend,decision_inputs.bear |
| channel_business_model_shift#1 | + | 2026-05-31 | Grab's Financial Services segment (fintech/digital banking) now accounts for over 30% of Grab's total revenue, with a combined digital-bank loan book exceeding US$1.5 billion by end of 2025, and the segment is targeted to reach break-even in the second half of 2026 — evidence the platform's revenue mix is shifting materially away from mobility/delivery take-rates alone. | Simply Wall St News, "Will Consolidating Superbank into GXS Bank Shift Grab Holdings' (GRAB) Superapp and Fintech Narrative?" | thesis.H,valuation |
| channel_business_model_shift#2 | 0 | 2025-11-17 | Merger talks between Grab and Indonesian rival GoTo (which would consolidate an estimated 85-90% of Indonesian ride-hailing and reshape channel/competitive structure via a combined Danantara-linked entity) resurfaced through 2025-2026 but remain unconfirmed: GoTo stated as of November 2025 there have been "no decisions or agreements made," and no definitive merger agreement had been announced as of the latest available reporting. | The Diplomat, "Is the GoTo-Grab Merger Finally Going to Happen?"; IDN Financials, "GOTO opens up about merger rumours with Grab" | thesis.H,decision_inputs.bear,triggers |
| capital_markets_pricing#0 | + | 2026-08-04 | Grab 於 Q2 2026 法說上調 FY2026 全年財測：Group revenue 由原先 $4.04B-$4.10B（YoY +20-22%）上修至 $4.10B-$4.15B（YoY +22-23%）；Adjusted EBITDA 由 $700M-$720M 上修至 $720M-$740M，同時宣布 $750M 新股票回購計畫。 | Grab press release: "Grab Reports Record Second Quarter 2026 Results, Raises Full-Year Guidance and Announces $750 Million Share Repurchase Program" (grab.com/sg/press) | thesis.H,valuation,decision_inputs.bear |
| capital_markets_pricing#1 | + | 2026-08-04 | Grab Q2 2026 實際結果：營收年增 22% 至 $997M，Adjusted EBITDA 年增 54% 至 $168M，EBITDA margin 擴張 360bp 至 16.9%；月活躍交易用戶（MTU）創新高達 5,400 萬，on-demand GMV 年增 21% 至 $6.5B——為財測上修之依據。 | Grab Q2 2026 earnings press release / summarized in Gurufocus "Grab Holdings Ltd (GRAB) (Q2 2026) Earnings Call Highlights" | thesis.H,moat_trend |
| capital_markets_pricing#2 | + | 2026-08 | 財測上修後，賣方共識 FY2026 營收預估由 US$4.12B 上修至 US$4.19B，略高於公司自身財測中值 $4.125B（顯示分析師較公司官方 guidance 略更樂觀）；FY2026 EPS 共識由 US$0.10 上修至 US$0.145。共識目標價則大致持平於 US$5.89。 | Yahoo Finance / Simply Wall St: "Grab Holdings (GRAB) Raises 2026 Guidance, Is The Stock Still Below Fair Value?" | valuation,thesis.H |
| capital_markets_pricing#3 | + | 2026-08-26 | S&P Global 彙整 26 位分析師對 Grab 的評等為 "Strong Buy" 共識，平均目標價 $5.86，區間 $4.60（最低）至 $8.00（最高）；目標價 $5.86 vs `numbers.price_at_dd` $3.42（2026-09-04 收盤）意味共識隱含大幅溢價空間。 | stockanalysis.com/stocks/grab/forecast | valuation,decision_inputs.bear |
| major_events#0 | + | 2026-02-12 | Grab signed a definitive agreement to acquire 100% of Stash Financial, Inc. (US digital investing platform), with payment for a 50.1% equity interest at an enterprise value of US$425 million; deal expected to close in Q3 2026. | Grab Investor Relations press release (investors.grab.com), "Grab Accelerates Financial Services Roadmap with Acquisition of Digital Investing Platform, Stash Financial, Inc." | thesis.H,moat_trend |
| major_events#1 | + | 2026-03-23 | Grab agreed to acquire Delivery Hero's foodpanda Taiwan delivery business for US$600 million cash (cash-free, debt-free basis), marking Grab's entry into Taiwan as its first market outside Southeast Asia; deal is subject to regulatory approval with completion expected in 2H2026 and full platform migration targeted for early 2027. | Grab Investor Relations 6-K / TechCrunch, "Grab to buy Foodpanda Taiwan from Delivery Hero for $600 million" | thesis.H,decision_inputs.bear |
| major_events#2 | 0 | 2026-01-23 | Grab-GoTo merger talks (on-and-off for years) hit a snag over Indonesian carrier Telkomsel's ~2% stake in GoTo, with Telkomsel unwilling to sell at current valuation; no definitive merger agreement has been signed, and reports on negotiation status have been conflicting (including a Grab statement denying active negotiations at one point, followed by resurfaced talk after reports SoftBank and other shareholders sought to replace GoTo's CEO). | Bloomberg, "Grab-GoTo Deal Hits Snag Caused by State-Backed Holder's Stake"; DealStreetAsia, "Grab-GoTo merger talks called off once again" | thesis.H,decision_inputs.bear,triggers |
| major_events#3 | + | 2026-03-25 | The SPAC-era securities class action In re Grab Holdings Limited Securities Litigation (S.D.N.Y., Case No. 1:22-cv-02189-JLR; class period Nov 12 2021 - Mar 3 2022, tied to Grab's post-SPAC-merger Q4 2021 disclosures of a 44% sequential revenue decline and $1.1B loss) was settled for $80 million, with settlement checks mailed to authorized claimants. | grabsecuritiessettlement.com joint declaration (S.D.N.Y. filing); claimdepot.com, "Grab Holdings Limited settles SEC class action for $80 million" | decision_inputs.bear |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "GRAB Holdings acquisition merger 2025 2026",
   "Grab GoTo merger talks 2026 status",
   "Grab foodpanda Taiwan acquisition completed 2026"
  ],
  "findings": [
   {
    "claim": "Grab signed a definitive agreement to acquire 100% of Stash Financial, Inc. (US digital investing platform), with payment for a 50.1% equity interest at an enterprise value of US$425 million; deal expected to close in Q3 2026.",
    "source": "Grab Investor Relations press release (investors.grab.com), \"Grab Accelerates Financial Services Roadmap with Acquisition of Digital Investing Platform, Stash Financial, Inc.\"",
    "as_of": "2026-02-12",
    "direction": "+",
    "affects": [
     "thesis.H",
     "moat_trend"
    ]
   },
   {
    "claim": "Grab agreed to acquire Delivery Hero's foodpanda Taiwan delivery business for US$600 million cash, marking Grab's entry into Taiwan as its first market outside Southeast Asia; deal subject to regulatory approval, completion expected 2H2026.",
    "source": "Grab Investor Relations 6-K / TechCrunch, \"Grab to buy Foodpanda Taiwan from Delivery Hero for $600 million\"",
    "as_of": "2026-03-23",
    "direction": "+",
    "affects": [
     "thesis.H",
     "decision_inputs.bear"
    ]
   },
   {
    "claim": "Grab-GoTo merger talks hit a snag over Indonesian carrier Telkomsel's ~2% stake in GoTo (unwilling to sell at current valuation); no definitive merger agreement signed, with conflicting reports on whether negotiations are active.",
    "source": "Bloomberg, \"Grab-GoTo Deal Hits Snag Caused by State-Backed Holder's Stake\"; DealStreetAsia, \"Grab-GoTo merger talks called off once again\"",
    "as_of": "2026-01-23",
    "direction": "0",
    "affects": [
     "thesis.H",
     "decision_inputs.bear",
     "triggers"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "found",
  "queries_run": [
   "GRAB Holdings class action lawsuit securities fraud",
   "GRAB Holdings SEC investigation restatement"
  ],
  "findings": [
   {
    "claim": "The SPAC-era securities class action In re Grab Holdings Limited Securities Litigation (S.D.N.Y., Case No. 1:22-cv-02189-JLR; class period Nov 12 2021 - Mar 3 2022) was settled for $80 million; settlement checks were mailed to authorized claimants.",
    "source": "grabsecuritiessettlement.com joint declaration (S.D.N.Y. filing); claimdepot.com, \"Grab Holdings Limited settles SEC class action for $80 million\"",
    "as_of": "2026-03-25",
    "direction": "+",
    "affects": [
     "decision_inputs.bear"
    ]
   }
  ],
  "note": "查證期間內未發現另有新提起的訴訟；此為 2022 年舊案（SPAC 合併後揭露爭議）於近 12 個月內完成和解金發放。"
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Grab Holdings FDA clinical trial approval",
   "Grab Holdings product launch recall warning letter regulator 2025 2026"
  ],
  "findings": [],
  "note": "非藥品/器材業務（叫車、外送、數位金融服務平台），已查證無相關臨床試驗或 FDA 監管動作，此軸不適用。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Grab Holdings product launch recall warning letter regulator 2025 2026",
   "GRAB Holdings acquisition merger 2025 2026"
  ],
  "findings": [],
  "note": "查證期間內未發現 Grab 產品下架、召回或監管警告信事件（搜尋結果僅出現無關的同名 \"Vapor Grab\" 電子煙品牌警告信）。"
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "GRAB Holdings SEC investigation restatement",
   "GRAB Holdings class action lawsuit securities fraud"
  ],
  "findings": [],
  "note": "查證期間內未發現 Grab 遭 SEC 正式調查或財報重編事件；唯一相關的 SEC/證券法議題是 2022 年 SPAC 揭露爭議衍生的私人證券集體訴訟（已列入 lawsuit_class_action），非監管機關調查。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_GRAB_20260505.html",
 "date": "20260505",
 "schema": "v12.3",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 3.62,
 "revlog": {
  "status": "unavailable"
 },
 "prior_meta": {
  "ticker": "GRAB",
  "name": "Grab Holdings",
  "date": "2026-05-05",
  "schema": "v12.3",
  "price_at_dd": 3.62,
  "inception_dd": "DD_GRAB_20260505.html",
  "inception_date": "2026-05-05",
  "next_yoy_review": "2027-05-05",
  "signal": "B",
  "trap": "🟡",
  "trap_label": "觀察期",
  "moat": "B",
  "moat_score": 8,
  "moat_execution": 7,
  "moat_pricing_power": 5,
  "val": "🟡",
  "ma": "🟠",
  "regime": "正常",
  "fpe_fy2": 24.5,
  "pct_5y": 5,
  "peg_fy2": 0.49,
  "upside_short_pct": 23,
  "upside_mid_pct": 64,
  "upside_5y_pct": 176,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "growth_durability": 8,
  "quality_score": 7,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "B（衛星候選 / 等 V 反轉確認）",
  "oneliner": "Q1 26 三軸強化(Rev+24%/EBITDA+46%/Loan+130%)但 guide 不上修；估值🟡PEG 0.49+P/S 5Y 5%；MA❌→🟠盲點 2 救援；Single Thing=FinSvc H2 26 breakeven；B 護城河 8/10(execution 7+pricing 5)；等 W104 $4.49"
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
    "text": "SEA super-app 三邊網絡飛輪持續加速：Mobility + Deliveries + GrabPay 整合產生 NDR 效應，MTU + GMV 維持雙位數 YoY",
    "columns": {
     "2Y 驗證": "FY27 MTU > 60M / GMV > $30B",
     "5Y 驗證": "FY30 MTU > 80M / GMV > $50B / Rev > $7B",
     "10Y 驗證": "FY35 GRAB 為 SEA 數位生活 default 平台",
     "指標": "MTU YoY、GMV YoY、各 segment 增速",
     "來源": "2Y: §6 / 5Y: §8 / 10Y: §11"
    }
   },
   {
    "id": "H2",
    "text": "Financial Services 第二曲線兌現：GXBank / GXS / GrabPay 成為獨立利潤引擎，Adj EBITDA 從虧損轉正",
    "columns": {
     "2Y 驗證": "H2 26 Financial Services Adj EBITDA breakeven（管理層承諾）；FY27 Loan portfolio > $3B",
     "5Y 驗證": "FY30 Financial Services Rev > $1B / Adj EBITDA $300M+",
     "10Y 驗證": "FY35 GRAB 為 SEA 多國數位銀行 top-3",
     "指標": "Loan portfolio、deposits、Financial Services Adj EBITDA",
     "來源": "2Y: §6 / 5Y: §11 / 10Y: §11"
    }
   },
   {
    "id": "H3",
    "text": "單位經濟拐點不可逆 + 估值 reset：Adj EBITDA margin 從 16% 擴至 20%+，市場給予 cycle-through 25-30x PE",
    "columns": {
     "2Y 驗證": "FY27 Adj EBITDA $1B / margin 22%",
     "5Y 驗證": "FY30 Adj EBITDA $1.5-2B / 80% FCF conv",
     "10Y 驗證": "FY35 GAAP NI margin > 15% / cycle-through PE 維持",
     "指標": "Adj EBITDA margin、Adj FCF / Rev、市場 PE 認可",
     "來源": "2Y: §10 / 5Y: §13 / 10Y: §13"
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
    "text": "Indonesia 監管擴大（commission cap 從 ojol 擴至 4-wheel + 外資限制）",
    "columns": {
     "對應": "H1 + 結構",
     "時間尺度": "中期（2-3 年）",
     "監測": "KPPU 公告、印尼國會 ride-hailing 立法",
     "警戒": "commission cap 擴至 4-wheel 即 H1 直接削弱 -10-15% Mobility GMV"
    }
   },
   {
    "id": "R2",
    "text": "Financial Services breakeven 推延 + 監管阻擾",
    "columns": {
     "對應": "H2",
     "時間尺度": "短期（12 月）",
     "監測": "Q2/Q3 26 Financial Services Adj EBITDA 軌跡",
     "警戒": "H2 26 仍虧損 → H2 thesis 大幅削弱"
    }
   },
   {
    "id": "R3",
    "text": "動能反身性 + V 反轉失敗",
    "columns": {
     "對應": "估值",
     "時間尺度": "短期（12 月）",
     "監測": "Pure MA 狀態、4w 漂移、跌破 $3.48 52W 低",
     "警戒": "跌破 $3.0 → 失守支撐，盲點 2 救援失效；反向突破 W104 $4.49 → 進場觸發"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_GRAB_20260505.html",
  "date": "20260505",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_GRAB_20260323.html",
  "date": "20260323",
  "days_from_365d_mark": 199
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "GRAB",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-05-05",
  "freshness": "aging",
  "source": "docs/dd/DD_GRAB_20260505.html"
 },
 "decision_history": [
  {
   "date": "2026-04-27",
   "verdict": null,
   "role": null,
   "price_at_decision": 3.9,
   "fundamental_grade": "X",
   "to_date_pct": -6.81,
   "days": 126,
   "source_report": "docs/dd/DD_GRAB_20260427.html"
  },
  {
   "date": "2026-05-05",
   "verdict": null,
   "role": null,
   "price_at_decision": 3.62,
   "fundamental_grade": "B",
   "to_date_pct": -8.06,
   "days": 118,
   "source_report": "docs/dd/DD_GRAB_20260505.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/GRAB.md\n[internal-note] 2026-05-17  Cold Review v12.3 — GRAB (Grab Holdings)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_GRAB_20260517.md\n[comparison] 2026-05-13  MS MELI vs SE vs GRAB 2026-05-13 | 多標的對比分析\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/comparisons/MS_MELIvsSEvsGRAB_20260513.md\n[dca] 2026-05-11  DCA_GRAB_20260511 — Grab Holdings 深度定見分析\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_GRAB_20260511.md\n[dca] 2026-05-08  DCA|GRAB Grab Holdings|2026-05-08\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_GRAB_20260508.md\n[dd] 2026-05-05  DD_GRAB_20260505 — Grab Holdings 深度研究 v12.3\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_GRAB_20260505.md\n[dd] 2026-04-27  DD|GRAB Grab Holdings|2026-04-27\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_GRAB_20260427.md\n[dd] 2026-03-23  DD Report — GRAB | 2026-03-23\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_GRAB_20260323.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "gap"
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/GRAB/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "CFO raises full-year 2025 group adjusted EBITDA guidance range.",
      "quote": "our EBITDA guidance to the $490 million and $500 million",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO reiterates full-year on-demand GMV growth will accelerate versus 2024.",
      "quote": "on-demand GMV growth to accelerate from 2024 levels",
      "speaker": "CEO (Anthony Tan)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "COO says Q4 on-demand GMV expected to grow sequentially from Q3.",
      "quote": "we expect fourth quarter on-demand GMV to grow sequentially",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "COO restates long-term segment margin targets for deliveries and mobility.",
      "quote": "deliverers to 4% plus and mobility to 9% plus",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CFO cites operating leverage improvement in regional corporate costs as percentage of revenue.",
      "quote": "150 basis points improvement in operating leverage",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "COO characterizes Indonesia delivery margin as stable despite continued growth investment.",
      "quote": "the margin is stable, we're actually able to generate",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "COO says Malaysia has already reached the company's steady-state delivery margin target.",
      "quote": "we've already reached our steady state margin target",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "competition",
      "claim": "COO describes Indonesia as remaining a very competitive market.",
      "quote": "It remains a very competitive market.",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "competition",
      "claim": "COO states comfort with Grab's market position and penetration in Indonesia.",
      "quote": "we're very comfortable with what we're doing",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO restates the three-pillar capital allocation framework is unchanged.",
      "quote": "our focus as always on three pillars",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO cites the WeRide and May Mobility deals as examples of selective, high-bar M&A in autonomous vehicles.",
      "quote": "You've seen the announcement that we made with WeRide",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO describes Q3 loan disbursal growth on an annualized basis as a capital deployment example.",
      "quote": "Q3 alone was up roughly about 56% on a year-over-year",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO says excess capital beyond organic growth and M&A will be returned to shareholders.",
      "quote": "we'll obviously look at returning it to our shareholders",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "product",
      "claim": "COO describes GrabMore, a feature letting food-delivery users add grocery items to the same order.",
      "quote": "GrabMore where a food user can just add on a grocery order",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "product",
      "claim": "COO describes early-stage quick-commerce experiments using Jaya grocery store assets in Malaysia.",
      "quote": "experimenting with quick commerce around certain Jaya stores",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "product",
      "claim": "COO calls GrabUnlimited the largest paid subscription program in Southeast Asia, up 14% YoY.",
      "quote": "GrabUnlimited is the biggest subscription program",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO states Southeast Asia labor costs remain low relative to the U.S., delaying AV unit-economics parity.",
      "quote": "Southeast Asia is still behind in the cost curve",
      "speaker": "CEO (Anthony Tan)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "COO acknowledges rising expected credit losses in Financial Services from the models used to provision for growth.",
      "quote": "an increase in the expected credit losses",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "COO says about a third of financial-services borrowers previously had no credit bureau data before borrowing from Grab.",
      "quote": "About 1/3 of our customers could not access data",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "COO says Saver deliveries account for nearly a third of new delivery MTUs joining the platform.",
      "quote": "almost 1/3 of our deliveries MTUs",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "COO reaffirms the goal to exceed a $1 billion loan book (ex. credit loss provisions) by end of 2025.",
      "quote": "we are reaffirming our goal to exceed a $1 billion loan book",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "COO reiterates Financial Services segment will reach breakeven overall in the second half, with banks breaking even in Q4.",
      "quote": "we will breakeven overall as a segment in the second half",
      "speaker": "COO (Alex Hungate)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO commits the IR team to an upcoming roadshow across multiple regions.",
      "quote": "We'll be on the road together with the IR team",
      "speaker": "CFO (Peter Oey)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 group revenue guided to grow 20-22% YoY to $4.04-4.1B",
      "quote": "we expect group revenues to grow between 20% to 22%",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 adjusted EBITDA guided to grow 40-44% YoY to $700-720M",
      "quote": "we expect to grow by 40% to 44% year-on-year",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "guidance",
      "claim": "New 3-year target: adjusted EBITDA to triple from 2025 to $1.5B by 2028 on 20% revenue CAGR",
      "quote": "EBITDA tripling from 2025 to reach $1.5 billion in 2028",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "margin",
      "claim": "Management reiterated long-term steady-state margin targets of 9%+ for Mobility and 4%+ for Deliveries",
      "quote": "steady-state margins of 9% plus of Mobility and 4% plus",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "margin",
      "claim": "Financial Services segment expected to reach EBITDA breakeven in H2 2026",
      "quote": "firmly on track to achieve EBITDA breakeven in the second",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "margin",
      "claim": "Adjusted free cash flow conversion targeted to rise from 58% in 2025 to 80% by 2028",
      "quote": "to move from 58% in 2025 to a target of 80%",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "competition",
      "claim": "Management frames AI/LLM chatbots as a channel that scales Grab's model rather than a disintermediation threat, citing physical fulfillment assets as the moat",
      "quote": "we view the evolution of AI not as a threat to the Superapp",
      "speaker": "Ping Yeow Tan",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "competition",
      "claim": "Management states the Indonesian government has not proposed any ride-hailing commission cap changes, despite media speculation",
      "quote": "government have not proposed any changes in commission caps",
      "speaker": "Alexander Charles Hungate",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "New $500 million share repurchase program announced this quarter, bringing total buyback commitment to $1 billion",
      "quote": "a new $500 million share repurchase program this quarter",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Despite the U.S.-based Stash acquisition, management says core capital allocation strategy remains rooted in Southeast Asia",
      "quote": "our long-term strategy remains very rooted in Southeast",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "commitment",
      "claim": "Stash acquisition expected to close in Q3 or Q4",
      "quote": "in Q3 or Q4. It's a great team.",
      "speaker": "Peter Oey",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "product",
      "claim": "GrabMart delivery growth is outpacing GrabFood by 1.7x",
      "quote": "GrabMart is growing 1.7x faster than GrabFood",
      "speaker": "Alexander Charles Hungate",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "commitment",
      "claim": "Management set a goal to exit 2026 with a gross loan book of over $2 billion, up from $1.3 billion at end of 2025",
      "quote": "exit 2026 with a gross loan book of over $2 billion",
      "speaker": "Alexander Charles Hungate",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "risk",
      "claim": "Management says it does not expect Indonesia margins to be hit by higher driver welfare/social program costs in 2026",
      "quote": "do not expect margins to be impacted by the social programs",
      "speaker": "Alexander Charles Hungate",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "customer",
      "claim": "Overall annual transacting user (ATU) base has grown to 129 million users",
      "quote": "the overall base has grown even further to 129 million users",
      "speaker": "Alexander Charles Hungate",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "commitment",
      "claim": "Management reiterates commitment to transitioning driver partners into new roles as the fleet shifts toward autonomous vehicles",
      "quote": "our commitment to transitioning our driver partners into new",
      "speaker": "Ping Yeow Tan",
      "date": "2026-02-12",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層重申 2026 全年集團營收 $4.04-4.10B、調整後 EBITDA $700-720M 指引不變。",
      "quote": "we reiterate our 2026 full year guidance.",
      "speaker": "Ping Yeow Tan (CEO/Anthony Tan)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "Financial Services 分部下半年 2026 損益兩平目標於 Q&A 中再次重申。",
      "quote": "second half 2026 breakeven target for financial services",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層表示 Q1 司機端獎勵支出應為全年高峰，非常態run-rate。",
      "quote": "this first quarter to be a peak in the driver incentives",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "管理層預期區域企業成本（regional corporate costs）將於 Q1 水準持平，不再進一步跳升。",
      "quote": "expecting any further step-ups from regional cooper costs",
      "speaker": "Ping Yeow Tan (Executives)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Financial Services 分部營收成長加速至年增 43%（固定匯率 38%）。",
      "quote": "Revenue growth accelerated 43% year-on-year",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "管理層將印尼騎乘傭金上限法規的直接曝險定性為範圍高度侷限。",
      "quote": "the immediate regulatory exposure is highly specific",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "管理層將 O2O（二輪）司機營收量化為總 Mobility GMV 不到 6%，作為印尼新規衝擊有限的依據。",
      "quote": "less than 6% of our total mobility GMV",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層將 $400M 加速股票回購計畫定性為對 Grab 長期價值的信心展現。",
      "quote": "reflection of our conviction in Grab's long-term value",
      "speaker": "Ping Yeow Tan (Executives)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 在被問及印尼整併機率是否提高時，重申併購交易維持高門檻的一貫立場。",
      "quote": "we always have a very high bar when it comes to M&A",
      "speaker": "Peter Oey (CFO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "採用 Turbo AI 駕駛模式的司機夥伴，每上線小時收入較未採用者提升 23%。",
      "quote": "a 23% uplift in earnings per online hour",
      "speaker": "Ping Yeow Tan (CEO/Anthony Tan)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "商家 AI 助理 Mai 上線一年內滲透約半數單店商家，帶動有使用商家 GMV 提升 15%。",
      "quote": "driving a 15% uplift in GMV for engaged users",
      "speaker": "Ping Yeow Tan (CEO/Anthony Tan)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "competition",
      "claim": "針對自駕車（AV）競爭態勢，管理層表示近期內不預期人類司機網路會被顯著取代式顛覆。",
      "quote": "we do not expect anyone to be able to deploy impactful",
      "speaker": "Ping Yeow Tan (CEO/Anthony Tan)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "commitment",
      "claim": "泰國電動車（EV）車隊供給已跨過 30,000 輛門檻，作為降低司機油價波動曝險的中期承諾之一。",
      "quote": "our total fleet supply has crossed 30,000 EVs",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "customer",
      "claim": "GrabMart 生鮮雜貨的 MTU 成長速度達外送食品 MTU 成長速度的 2.6 倍。",
      "quote": "MTUs going into grocery at 2.6x the rate of food MTU growth",
      "speaker": "Alexander Charles Hungate (COO)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "customer",
      "claim": "活躍司機夥伴總數季增 4%、年增 16%，於總體不確定環境下創歷史新高。",
      "quote": "active driver partners increased 4% quarter-on-quarter",
      "speaker": "Ping Yeow Tan (CEO/Anthony Tan)",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Delivery Hero announces divestment of its Taiwan food delivery operations to Grab for cash.",
      "quote": "to Grab for USD 600 million in cash",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO frames the Taiwan sale to Grab as Delivery Hero's fifth asset monetization to date.",
      "quote": "This is our fifth asset monetization to date",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives expected closing timeline for the Grab-Taiwan transaction.",
      "quote": "the transaction will close in the second half of 2026",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "commitment",
      "claim": "Delivery Hero commits to a transitional services period supporting the Taiwan business after close.",
      "quote": "a migration period of up to 12 months following the close",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "margin",
      "claim": "CFO states the EBITDA and cash flow impact of losing the Taiwan business will be marginal for Delivery Hero during the TSA period.",
      "quote": "the impact on the EBITDA and cash flow would be marginal",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "competition",
      "claim": "CEO contrasts Uber's prior in-market Taiwan bid with Grab's market-entry position when discussing deal multiple.",
      "quote": "Uber was and still is operating in the market",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO characterizes the agreed deal terms as favorable for Grab with further upside.",
      "quote": "a good deal that is a good boost for Grab",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "competition",
      "claim": "CEO asserts the Taiwan business (being sold to Grab) holds a strong competitive position in its market.",
      "quote": "we have a very strong position in the Taiwan market",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes geographically uneven share split between the Taiwan business and Uber.",
      "quote": "There will be some areas where they will be slightly larger",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "risk",
      "claim": "CFO indicates Delivery Hero's Singapore tech hub operations will need resizing over time following the Taiwan divestment.",
      "quote": "there will definitely be a process of adjusting",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "product",
      "claim": "CFO discloses FY2025 GMV scale of the Taiwan business being acquired by Grab.",
      "quote": "generated a GMV of EUR 1.5 billion",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO states the Taiwan sale proceeds reduce Delivery Hero's net leverage ratio.",
      "quote": "reducing our net leverage from approximately 2.7x to 2.2x",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "risk",
      "claim": "CEO signals the Taiwan sale is only the first of several ongoing Delivery Hero portfolio reviews, implying more divestment candidates could later reach the market.",
      "quote": "it is just one of several ongoing reviews",
      "speaker": "L. Östberg (CEO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO reiterates that raised term loan and sale proceeds are earmarked toward existing debt repayment.",
      "quote": "to focus on repaying existing debt",
      "speaker": "Marie-Anne Popp (CFO, Delivery Hero)",
      "date": "2026-03-23",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Goldman Sachs analyst asked for specific color/metrics on the growth Grab has achieved in Indonesia specifically, given the 24% YoY group on-demand growth.",
      "response_pattern": "COO did not provide an Indonesia-specific growth figure; instead said 'you can't see these in the numbers, but I can tell you that there's strong growth in Indonesia' and pivoted to qualitative commentary on product strategy and 'strong sequential margin improvement' without quantifying either.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "question": "Alicia Yap (Citi) three-part question: 2028 revenue breakdown by segment, Deliveries EBITDA margin by 2028, and confirmation of Financial Services breakeven by H2 2026",
      "response_pattern": "Peter Oey addressed segment growth drivers and only confirmed Fintech breakeven after the call moderator (Ken Vin Lek) had to remind him he had skipped a question ('I've lost track to that'); no specific numeric answer was given for the Deliveries EBITDA margin by 2028 part of the question.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "question": "JPMorgan (Ranjan Sharma) / Bernstein (Venu Gopal) asked for Stash's financial metrics including burn, near-term earnings, and the valuation/price paid for the acquisition",
      "response_pattern": "Peter Oey answered with strategic rationale and stated Stash is EBITDA-positive, FCF-positive, and targets $60M EBITDA by 2028, but did not disclose burn figures, near-term earnings detail, or the purchase valuation/price paid that was explicitly asked.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q4_2025_Earnings_Call_20260212.md"
    },
    {
      "question": "印尼 8% 傭金上限之後，印尼市場整併機率是否提高？此政策轉變是否改變公司近中期投資或資本配置優先順序？",
      "response_pattern": "CFO 未直接回應整併機率是否提高的問題，轉而談論公司一貫的併購高門檻與資本配置紀律等通用敘述，未正面觸及印尼整併可能性本身。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "question": "區域企業成本增加至 $114M，其中 AI 基礎建設成本（雲端 tokenization vs 一般通膨與匯率）各佔多少比例？",
      "response_pattern": "管理層僅以質性方式描述成本驅動因子（AI tokenization stack、雲端容量、美元走弱的匯率逆風），未提供各因子貢獻比例的量化拆分。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "question": "Foodpanda 台灣收購案的進度、待觀察的關鍵里程碑與可能時程為何？",
      "response_pattern": "管理層僅簡短表示目前仍在監管審批流程中、今日沒有實質更新，將待後續有進展時再提供，未回答里程碑或時程的具體內容。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "question": "Why issue a $1.4B term loan, roughly $600M more than the stated convert buyback need, and why sit on such a large cash balance?",
      "response_pattern": "CFO repeats generic prior messaging ('strengthen capital structure', 'repay existing debt', 'remain flexible for future opportunities') without addressing the specific ~$600M gap the analyst asked about.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    },
    {
      "question": "Does the Taiwan sale unlock a larger evolution/reduction in central and tech (Singapore hub) costs over time?",
      "response_pattern": "CFO does not confirm, deny, or quantify any central-cost reduction; reiterates that hub sizing is 'an ongoing process' and support continues through the TSA period.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GRAB/GRAB_Delivery_Hero_SE_Grab_Holdings_Limited_M_A_Call_20260323.md"
    }
  ]
}

```

---

## judgment.json 全文

```json
{
  "meta": {
    "ticker": "GRAB",
    "date": "2026-09-05",
    "schema": "v15.2",
    "company_name": "Grab Holdings"
  },
  "oneliner": "東南亞超級 App 龍頭在營收 +22%、調整後 EBITDA 利益率 16.9% 且上修指引之際，股價落在 52 週低點附近（−47% 自高點）；印尼傭金上限與金融服務信用週期未證，故以衛星分批進場、不當長期核心。",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": "未獲利高成長（GAAP 剛轉正、以調整後 EBITDA 為主尺的平台）",
    "confidence": "中",
    "fingerprint": "GAAP 營業利益率 1.9%、調整後 EBITDA 利益率 16.9%、營收 +22%、SBC 占營收 6.2%、淨現金、負營運資金週期；獲利尺仍以調整後 EBITDA 與 EV/EBITDA 為主，GAAP EPS 為輔"
  },
  "thesis": {
    "headline": "密度領先（外送 55% 份額、5,400 萬 MTU）正轉成營運槓桿，金融服務是第二曲線；市場把印尼監管與信用風險當成全書問題定價",
    "holding_period": {
      "horizon": "中長期 3–5 年",
      "driver": "調整後 EBITDA 由 FY25 約 $0.5B 走向管理層 2028 年 $1.5B 目標，以及金融服務 2H26 轉正後的利潤貢獻",
      "signal_vs_noise": "單季獎勵支出、油價補貼、匯率屬噪音；on-demand GMV 年增率、集團 take rate、ECL 比率、獎勵占 GMV 為訊號"
    },
    "H": [
      {
        "id": "H1",
        "text": "需求飛輪持續：MTU 與 on-demand GMV 維持中雙位數成長，份額續升（外送 55%）",
        "2y": "FY2027 MTU ＞ 6,000 萬、集團營收 ≥ $5.0B",
        "5y": "FY2030 營收 ≥ $8B、on-demand GMV 年增仍 ≥ 12%",
        "10y": "FY2035 MTU ＞ 1 億、為東南亞日常消費預設平台",
        "threshold": "on-demand GMV TTM 年增 ＜ 12% 連 2 季＝削弱；＜ 8% 連 3 季＝反轉",
        "source": "季報 6-K（GMV／MTU）；Momentum Works 年度份額",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥ 5% 削弱、連 3 季 ≥ 10% 反轉；5Y 連 4 季 ≥ 5% 削弱"
      },
      {
        "id": "H2",
        "text": "營運槓桿兌現：調整後 EBITDA 三年翻三倍至 2028 年 $1.5B（管理層目標），自由現金流轉換率由 58% 升至 80%",
        "2y": "FY2027 調整後 EBITDA ≥ $1.0B、利益率 ≥ 20%",
        "5y": "FY2030 調整後 EBITDA ≥ $2.0B、調整後 FCF 轉換率 ≥ 80%",
        "10y": "FY2035 GAAP 營業利益率 ≥ 15%",
        "threshold": "調整後 EBITDA 利益率 TTM ＜ 14% 連 2 季＝削弱；獎勵占 GMV ＞ 12% 連 2 季＝反轉",
        "source": "季報非 GAAP 調節表；Q4 2025 法說三年目標（來源：摘要）",
        "drift_rule": "2Y 連 2 季偏離 ≥ 5% 削弱；5Y 連 4 季 ≥ 5% 削弱、連 6 季 ≥ 10% 反轉"
      },
      {
        "id": "H3",
        "text": "金融服務成為獨立利潤引擎：2H26 分部轉正、放款餘額年底 ＞ $3B、ECL 維持 5% 以下",
        "2y": "FY2027 金融服務調整後 EBITDA ≥ $100M、ECL ＜ 6%",
        "5y": "FY2030 金融服務營收 ＞ $1B、分部利益率 ≥ 25%",
        "10y": "FY2035 為東南亞三大數位銀行之一",
        "threshold": "Q4 2026 分部仍虧損＝削弱；ECL ＞ 7% 或放款成長 ＜ 30%＝反轉",
        "source": "季報分部揭露；GXS／GXBank／Superbank 年報",
        "drift_rule": "2Y 連 2 季偏離削弱；5Y 連 4 季偏離削弱、連 6 季反轉"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "印尼監管擴大：二輪 8% 傭金上限（2026-07-01 生效）延伸至四輪或外送；印尼占營收 23%，前三國合計逾 70%",
        "h_ref": "H2",
        "clock": "🔥",
        "threshold": "總統令或部會規章把上限擴至四輪／外送＝清倉級；印尼 Mobility 營收連 2 季年減＝減碼",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "geo_supply_chain#0",
          "geo_supply_chain#1"
        ]
      },
      {
        "id": "R2",
        "text": "金融服務信用週期：放款餘額年增 197% 未經完整週期，ECL 由 4.6% 回升即侵蝕第二曲線",
        "h_ref": "H3",
        "clock": "🔥",
        "threshold": "ECL ＞ 7% 或撥備增速連 2 季高於放款增速＝減碼；分部 2H26 未轉正＝削弱",
        "evidence_refs": []
      },
      {
        "id": "R3",
        "text": "競爭與多平台上架：inDrive（菲律賓，約 10% 傭金）、Bolt（泰國）進場，商家同時上架多平台已是常態，傭金 15–35% 受擠壓",
        "h_ref": "H1",
        "clock": "🐢",
        "threshold": "外送份額跌破 50% 或獎勵占 GMV ＞ 12% 連 2 季＝減碼",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "competitive_share_entrants#4",
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      },
      {
        "id": "R4",
        "text": "資本配置漂移：$600M 台灣 foodpanda（監管審查含國安疑慮、與 Uber Eats 補貼戰）與 $425M 美國 Stash，皆在東南亞主場之外",
        "h_ref": "H2",
        "clock": "🐢",
        "threshold": "台灣整合首年調整後 EBITDA 拖累 ＞ $100M 或 Stash 減損＝降級資本配置評級",
        "evidence_refs": [
          "regulatory_antitrust#1"
        ]
      },
      {
        "id": "R5",
        "text": "油價與價格敏感度：Q2 油價需 $7M 司機補貼，Mobility 營收 +12% 落後 GMV +18%；82% 受訪者稱漲價會調整使用頻率",
        "h_ref": "H2",
        "clock": "⚡",
        "threshold": "Mobility take rate 連 2 季年減 ＞ 50bp＝減碼警戒",
        "evidence_refs": [
          "end_markets#1",
          "supply_demand_durability#3"
        ]
      }
    ],
    "single_thing": {
      "description": "印尼政府把平台傭金上限自二輪擴至四輪與外送（可觀測的單一法規事件）",
      "why_fatal": "印尼占營收 23%，二輪僅占 Mobility GMV 不到 6%（管理層口徑）故可吸收；擴至四輪與外送則直接打到 H2 營運槓桿與 H1 密度變現，且示範效應可能外溢至馬來西亞、泰國",
      "if_happens": "清倉級：集團調整後 EBITDA 路徑改走 Bear（$0.8–0.9B），終端倍數同步壓縮；不等待財報驗證",
      "how_monitor": "印尼總統令／交通部規章公告、KPPU 聲明、季報中印尼 Mobility 與外送 GMV 及 take rate；Q3 2026 財報（2026-11）為首個含上限季度",
      "probability": "12–24 個月約 20%（Q4 2025 法說管理層曾稱政府未提案，三個月後即簽總統令，政策可預測性低）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "無對應產業報告（ID gap：東南亞平台經濟）；自判：外送 GMV 2025 年 +18%、補貼收斂、foodpanda 退出台灣與 GoTo 弱化屬擴張期整併，非過熱",
    "bargaining": {
      "up": "供給端（司機／商家）：活躍司機年增 16% 創新高，供給充裕；但油價需補貼、商家多平台上架常態化、傭金受監管封頂，平台對供給端議價力受政治因素壓制",
      "down": "消費端：82% 受訪者對漲價會調頻，但日常代步剛性需求撐住量；saver 產品拉低客單、交易量 +28% 快於 GMV +18%",
      "geo": "馬來西亞 29.2%、印尼 23.0%、新加坡 20.7%（FY2024）合計逾 70%；單一國家監管即為集團級事件"
    },
    "profit_pool_dir": "利潤池流向平台端（補貼收斂、對手退出／整併），但監管抽走一部分（印尼傭金上限）——淨流入、幅度被政策折扣",
    "tam_table": [
      {
        "segment": "Deliveries（外送＋GrabMart）",
        "tam_now": "東南亞外送 GMV 2025 年 US$22.7B",
        "tam_5y": "2030 年約 US$36B（CAGR 9.4%）；另一預測 2027 年 US$45.5B",
        "sam_share": "Grab GMV 份額約 55%（2024 年 53.8%）",
        "penetration": "低；GrabMart 成長為外送 1.7–2.6 倍（來源：摘要）",
        "segment_cagr": "Q2 營收 +21%、GMV +22%",
        "pool_trend": "流入：ShopeeFood 升第二、foodpanda 退居第三",
        "ceiling_note": "天花板＝傭金監管與商家多平台上架；替代路徑＝電商平台（Shopee）以流量補貼外送"
      },
      {
        "segment": "Mobility",
        "tam_now": "證據包未涵蓋（東南亞叫車市場規模）；Grab Q2 GMV $2.21B 年化約 $9B",
        "tam_5y": "證據包未涵蓋",
        "sam_share": "菲律賓約 90%、泰國約 50%、印尼與 Gojek 合計逾 91%",
        "penetration": "中；交易量 +28% 靠平價方案",
        "segment_cagr": "GMV +18%、營收 +12%",
        "pool_trend": "受政策折扣：印尼二輪傭金 20%→8%",
        "ceiling_note": "天花板＝政府傭金上限；替代路徑＝自駕車隊（WeRide 合作 vs Pony／Baidu 自營）"
      },
      {
        "segment": "Financial Services",
        "tam_now": "證據包未涵蓋（東南亞未受銀行服務人口與消費金融規模）；放款餘額 $2.3B、存款 $2.5B",
        "tam_5y": "年底放款餘額 ＞ $3B（管理層）",
        "sam_share": "三國數位銀行牌照（新加坡／馬來西亞／印尼 Superbank 控股）",
        "penetration": "極低；三分之一借款人先前無信用紀錄（來源：摘要）",
        "segment_cagr": "營收 +59%、放款餘額 +197%",
        "pool_trend": "流入：生態系數據使 ECL 由 6.8% 降至 4.6%",
        "ceiling_note": "天花板＝資本充足與信用週期；替代路徑＝Sea（SeaMoney）與傳統銀行數位化"
      }
    ]
  },
  "moat": {
    "execution": 8,
    "pricing": 5,
    "combined": 6.5,
    "grade": "C",
    "score": 6.5,
    "trend": "→",
    "trend_evidence": "執行面擴大：外送份額 53.8%→55%（Momentum Works，2026-01）、MTU 5,400 萬新高、活躍司機 +16%、對手退出（foodpanda 售台灣）；定價面收縮：印尼二輪傭金 20%→8%（2026-07-01 生效）、Mobility 營收 +12% 落後 GMV +18%。一擴一縮，五年報酬更繫於 take rate 與利益率（H2），故取 → 而非 ↑",
    "spread_table": [
      {
        "metric": "營業利益率（TTM，資料源同尺）",
        "grab": "8.9%",
        "se": "8.4%",
        "uber": "12.1%",
        "dash": "4.8%",
        "meli": "8.3%",
        "read": "與 SE／MELI 同級、低於 UBER；GAAP 季度口徑僅 1.9%，差異來自資料源定義"
      },
      {
        "metric": "自由現金流利益率（TTM）",
        "grab": "−5.0%（含銀行放款增長的營運現金流出）",
        "se": "19.1%",
        "uber": "18.3%",
        "dash": "13.5%",
        "meli": "35.3%",
        "read": "最弱；調整後 FCF TTM $450M（約 12%）才是可比口徑，spread 為負且未擴大"
      },
      {
        "metric": "毛利率（TTM）",
        "grab": "43.6%",
        "se": "44.3%",
        "uber": "42.3%",
        "dash": "51.4%",
        "meli": "42.7%",
        "read": "同級；無定價溢價證據"
      },
      {
        "metric": "研發強度",
        "grab": "11.2%",
        "se": "4.6%",
        "uber": "6.8%",
        "dash": "10.7%",
        "meli": "7.3%",
        "read": "最高；營運槓桿空間在此，也是區域企業成本跳升（AI 基礎建設）的來源"
      },
      {
        "metric": "ROIC 對最強直接對手 spread",
        "grab": "證據包未涵蓋（ROIC 未提供）",
        "se": "—",
        "uber": "—",
        "dash": "—",
        "meli": "—",
        "read": "以 OM／FCF margin 代理：spread 為負，未滿足合併分 ≥ 8 的閘一，故合併分 6.5"
      }
    ],
    "threats": [
      {
        "level": "🔴",
        "text": "生態攻擊：Shopee 以電商流量補貼 ShopeeFood 升至區域第二；商家多平台上架成常態、傭金 15–35% 受擠壓，GrabSignatures 獨家計畫是反制但逆勢",
        "p": "40%",
        "evidence_refs": [
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      },
      {
        "level": "🟡",
        "text": "點對點：inDrive（反向競價、約 10% 傭金）菲律賓載客量 7 倍、2026 年再開兩城；Bolt 2026-05 進泰國電動車叫車",
        "p": "60%（已發生，影響邊際市場）",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "competitive_share_entrants#4"
        ]
      },
      {
        "level": "🔴",
        "text": "監管替代定價：印尼二輪傭金上限 8%，示範效應可外溢；台灣公平會審查含「假競爭真壟斷」與國安疑慮",
        "p": "20%（擴大）",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "regulatory_antitrust#1",
          "geo_supply_chain#0"
        ]
      },
      {
        "level": "🟡",
        "text": "架構替代（長期）：ComfortDelGro×Pony.ai、Baidu 自營自駕進新加坡／馬來西亞；Grab 以 WeRide 夥伴身分卡位，但頭部自駕商可能繞過平台。東南亞人力成本低、水患與司機生計政治敏感，延緩替代",
        "p": "15%（五年內實質分流）",
        "evidence_refs": [
          "substitute_technology#2"
        ]
      }
    ],
    "competitors": [
      {
        "name": "Sea（ShopeeFood／SeaMoney）",
        "rev_growth": "證據包未涵蓋",
        "gm": 44.27,
        "om": 8.42,
        "rd_intensity": 4.6,
        "fcf_margin": 19.06,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "以電商流量與金融交叉補貼外送，區域第二；FCF 體質遠強於 Grab，有能力打補貼戰"
      },
      {
        "name": "Uber",
        "rev_growth": "證據包未涵蓋",
        "gm": 42.31,
        "om": 12.13,
        "rd_intensity": 6.77,
        "fcf_margin": 18.32,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "台灣外送在位者（Uber Eats），將是 Grab 首個東南亞外戰場；成熟平台倍數為本檔終端倍數錨"
      },
      {
        "name": "DoorDash",
        "rev_growth": "證據包未涵蓋",
        "gm": 51.41,
        "om": 4.8,
        "rd_intensity": 10.74,
        "fcf_margin": 13.46,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "非直接對手；作外送單一業務的利益率對照（毛利高、OM 低）"
      },
      {
        "name": "MercadoLibre",
        "rev_growth": "證據包未涵蓋",
        "gm": 42.68,
        "om": 8.26,
        "rd_intensity": 7.33,
        "fcf_margin": 35.27,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "新興市場平台＋金融第二曲線的成功樣板；FCF 35% 顯示 Grab 金融服務若走通的終局形態"
      },
      {
        "name": "GoTo（Gojek／GoFood）",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "證據包未涵蓋",
        "strategy_note": "印尼與 Grab 合計逾 91% 叫車份額；併購談判卡在國營股東持股與 KPPU 反壟斷，年底前有結果"
      }
    ],
    "roic_durability": {
      "quadrant": "低利益率 × 高周轉（負營運資金週期的平台，NOPAT 利益率約 1.5%）→ 正往中利益率移動（調整後 EBITDA 利益率 13.3%→16.9%）",
      "checkpoints": [
        {
          "name": "需求基礎值",
          "light": "🟢",
          "evidence": "代步與三餐屬「需要」型：油價擠壓下叫車與外送需求未崩（New Straits Times，2026-08）；交易量 +28%"
        },
        {
          "name": "決策層級",
          "light": "🟡",
          "evidence": "消費端以超級 App 與 GrabUnlimited（東南亞最大訂閱，+14%，來源：摘要）綁定；商家端多平台上架已是標準做法，替代性在商家層很高"
        },
        {
          "name": "價值鏈分配",
          "light": "🟡",
          "evidence": "Mobility 營收 +12% 落後 GMV +18%，油價補貼 $7M；獎勵仍約 GMV 10%，補貼率每升 100bp 年化成本約 $2.2 億（GabGrowth，2025-11）"
        },
        {
          "name": "社會容忍度",
          "light": "🔴",
          "evidence": "司機生計政治敏感：印尼總統令（2026-05-01 公告）把二輪傭金上限 20%→8%；法源＝總統規章，修法程序短、可預測性低"
        }
      ],
      "roiic": "約 19%（代理：FY25→FY26E 調整後 EBITDA 增量約 $230M ÷ 同期新增投入約 $1.2B〔Stash $425M＋台灣 $600M＋資本支出〕）",
      "reinvest_rate": "＞100%（併購 $1.0B 以上 vs NOPAT 約 $0.1B，標準公式失效；負營運資金週期下改以增量報酬為內生上界）",
      "endo_ceiling": 19,
      "formula_note": "內生成長天花板＝增量 EBITDA 報酬 19% × 再投資率上限 100% ≈ 19%；Base 情境 EPS CAGR 約 22.6% 高於天花板，缺口歸因營運槓桿（EBITDA 利益率 17%→25%），非新曲線，故情境樹 Bear 機率 ≥ 30%"
    }
  },
  "growth": {
    "runway_years": 10,
    "runway_post_y5": "🟢",
    "seven_questions": [
      "①結構性：外送 GMV 2025 年 +18%、平台交易用戶 1.29 億（來源：摘要），非週期反彈",
      "②資本投入：平台本身輕資產，但金融服務放款餘額 $2.3B 與 $1.0B 併購吃掉現金",
      "③增量 ROIC：代理約 19%，高於資金成本但未經信用週期驗證——最弱的一題",
      "④變現金流：調整後 FCF TTM $450M、轉換率 58% 目標 80%；但 yfinance 口徑 FCF 為負（放款成長）",
      "⑤競爭吸引：是——inDrive、Bolt、ShopeeFood 皆被吸引，靠密度與補貼紀律守",
      "⑥股價反映：26 週 −14%、距高點 −47%，EV/EBITDA 約 13 倍，期待已大幅回落",
      "⑦下修承受度：成長降至 10% 時終端倍數 14 倍、股價約 $1.96（−43%），承受度中等"
    ],
    "segments": [
      {
        "name": "Deliveries",
        "weight_pct": 53.3,
        "fy0_rev": "Q2 2026 $531M（年化約 $2.1B）",
        "driver": "GMV +22%（量）＋廣告（價）",
        "fy1e": "+20%",
        "fy2e": "+17%",
        "fy3e": "+15%",
        "om_path": "分部穩態利益率目標 4%＋（GMV 口徑，來源：摘要），馬來西亞已達標",
        "eps_contrib_pct": "約 45%"
      },
      {
        "name": "Mobility",
        "weight_pct": 33.2,
        "fy0_rev": "Q2 2026 $331M（年化約 $1.3B）",
        "driver": "交易量 +28%、GMV +18%（量），take rate 受油價補貼與印尼上限壓縮（價 −）",
        "fy1e": "+12%",
        "fy2e": "+12%",
        "fy3e": "+12%",
        "om_path": "穩態 9%＋（GMV 口徑）；印尼二輪上限影響 ＜ 6% Mobility GMV",
        "eps_contrib_pct": "約 40%"
      },
      {
        "name": "Financial Services",
        "weight_pct": 13.4,
        "fy0_rev": "Q2 2026 $134M（年化約 $0.5B）",
        "driver": "放款餘額 +197%、Superbank 併表（量）、NIM（價）",
        "fy1e": "+50%",
        "fy2e": "+40%",
        "fy3e": "+30%",
        "om_path": "2H26 轉正 → FY28 分部利益率 15–20%",
        "eps_contrib_pct": "約 15%（FY28 起）"
      }
    ],
    "decay_signals": [
      "SBC／營收 ＞ 5%：命中（6.22%）但年減（Q1 8.17%、去年同期約 7.4%），半亮",
      "FCF／NI ＜ 0.75：口徑分歧——yfinance TTM FCF 為負、調整後 FCF 為正；GAAP 淨利極小，比率不具意義，記 🟡",
      "GM 連 2 季年減：證據包未涵蓋逐季毛利率，TTM 43.6% 無惡化證據，未亮",
      "核心份額縮減：未亮（外送份額 53.8%→55%）",
      "提價後銷量下滑：未亮（交易量 +28%）",
      "EPS CAGR 高於營收 CAGR ＞ 5pp：FY1→FY3 EPS CAGR 約 21% vs 營收約 20%，未亮",
      "產業倍數系統性下移：P/S 由 2022 年 9.2 倍降至 3.75 倍，但屬轉盈後正常化，記 🟡",
      "維護性資本支出占 FCF ＞ 60%：未亮（輕資產）",
      "TAM 萎縮：未亮",
      "停止投資後收入下滑：未亮"
    ],
    "trap_rating": "🟡（1–2 個信號：SBC 半亮、FCF 口徑分歧）"
  },
  "quality": {
    "three_year": [
      {
        "metric": "調整後 EBITDA 利益率",
        "fy2024": "證據包未涵蓋",
        "fy2025": "約 14.8%（$490–500M ÷ 約 $3.37B）",
        "fy2026e": "約 17.6%（$720–740M ÷ $4.10–4.15B）",
        "peer_median": "OM 同尺 8.4%（SE／MELI／UBER／DASH 中位）",
        "assessment": "擴張中；Q2 單季 16.9%（+360bp）"
      },
      {
        "metric": "SBC／營收",
        "fy2024": "證據包未涵蓋",
        "fy2025": "Q2 2025 約 7.4%",
        "fy2026e": "Q2 2026 6.22%（Q1 8.17% 為授予高峰）",
        "peer_median": "證據包未涵蓋",
        "assessment": "下降中但仍 ＞ 5%"
      },
      {
        "metric": "調整後 FCF 轉換率",
        "fy2024": "證據包未涵蓋",
        "fy2025": "58%（來源：摘要）",
        "fy2026e": "TTM 調整後 FCF $450M；目標 2028 年 80%",
        "peer_median": "FCF margin 中位 18.7%",
        "assessment": "落後同業，改善路徑有管理層承諾"
      },
      {
        "metric": "GAAP 營業利益率",
        "fy2024": "證據包未涵蓋",
        "fy2025": "Q2 2025 0.9%",
        "fy2026e": "Q2 2026 1.9%（Q1 2.3%）",
        "peer_median": "8.4%",
        "assessment": "薄；差距來自 SBC 與 D&A"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利益率",
        "value": "約 1.5%（GAAP 營業利益率 1.9% × 0.8）",
        "trend": "由負轉正、擴張中",
        "note": "調整後 EBITDA 利益率 16.9% 為經營口徑"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本未提供）",
        "trend": "負營運資金週期使周轉率極高",
        "note": "銀行併表後投入資本將被放款餘額推高，周轉率結構性下降"
      },
      {
        "component": "ROIC",
        "value": "低個位數（NOPAT 小、淨現金大）",
        "trend": "↑",
        "note": "第一象限化的關鍵在利益率而非周轉率"
      }
    ],
    "ccc": [
      {
        "year": "2026 Q2",
        "dso": "證據包未涵蓋",
        "dio": "不適用（平台）",
        "dpo": "證據包未涵蓋",
        "ccc": "負（先收後付：Q1 營運現金流 −$59M 因年度獎金與供應商付款季節性）",
        "note": "負營運資金週期為平台特徵；銀行併表後現金流量表口徑混入放款"
      }
    ],
    "buyback": {
      "program": "2026-08 新增 $750M；2026-02 $500M（累計承諾 $1B）；Q1 2026 $400M 加速回購（來源：摘要）",
      "buyback_to_fcf": "$750M vs 調整後 FCF TTM $450M ＞ 100%——由淨現金部位支應而非當期 FCF",
      "ex_buyback_eps_cagr": "證據包未涵蓋股數變動；SBC 年化約 $260M（約 1.9% 市值）與回購相抵後淨稀釋約 0–1%",
      "avg_price_vs_now": "證據包未涵蓋回購均價；現價 $3.42 低於 Q1 2026 加速回購期間股價（約 $3.5–3.6）",
      "revenue_cagr_same_period": "FY26E +22–23%"
    },
    "lumpiness": {
      "fcf_by_year": "證據包未涵蓋五年序列；已知 Q1 2026 調整後 FCF $98M（營運現金流 −$59M）、Q2 $73M（營運現金流 $56M）、TTM $450M",
      "maint_capex_method": "證據包未涵蓋；平台型以資本支出全數視為維護性（保守）",
      "owner_earnings": "約等於調整後 FCF $450M TTM",
      "nature": "季節性（Q1 年度獎金與授予）＋銀行併表口徑噪音",
      "verdict": "🟡 需關注：yfinance FCF margin −5% 與調整後 FCF 正值的口徑差需每季對帳"
    }
  },
  "governance": {
    "capalloc_grade": "B",
    "scorecard": [
      {
        "item": "併購已實現 ROIIC",
        "value": "N/A（Stash 與台灣 foodpanda 尚未交割；WeRide 投資 2026 年中完成）",
        "pass": "不計",
        "note": "兩案合計逾 $1.0B、約市值 7%，屬重大併購，三年後回填"
      },
      {
        "item": "回購買入收益率",
        "value": "以 FY1 EPS 0.13 ÷ $3.42 ≈ 3.8%；以 EBITDA yield 約 7.7%（$730M ÷ EV 約 $9.4B）代理",
        "pass": "邊界（10Y 殖利率證據包未涵蓋）",
        "note": "GAAP 口徑不過、EBITDA 口徑過"
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 約 1.9% 市值／年，回購 $400M 已執行、$750M 新增，淨稀釋估 ≤ 1%",
        "pass": "過",
        "note": "股數序列證據包未涵蓋，以金額推估"
      }
    ],
    "capital_returns": [
      {
        "year": "2026-02",
        "type": "回購",
        "amount": "$500M 新計畫（累計 $1B）",
        "note": "Q4 2025 法說宣布（來源：摘要）"
      },
      {
        "year": "2026 Q1",
        "type": "回購",
        "amount": "$400M 加速回購",
        "note": "管理層稱為長期價值信心展現（來源：摘要）"
      },
      {
        "year": "2026-08",
        "type": "回購",
        "amount": "$750M 新計畫",
        "note": "隨 Q2 財報宣布"
      },
      {
        "year": "2026-02",
        "type": "併購",
        "amount": "Stash（美國數位投資平台）EV $425M、先取 50.1%",
        "note": "Q3 2026 交割；法說未揭露對價與燒錢（來源：摘要 Q&A）"
      },
      {
        "year": "2026-03",
        "type": "併購",
        "amount": "foodpanda 台灣 $600M 現金",
        "note": "2H26 交割、待公平會；首個東南亞外市場"
      },
      {
        "year": "2025-08",
        "type": "投資",
        "amount": "WeRide（金額證據包未涵蓋，稱最大單筆投資）",
        "note": "自駕平台夥伴"
      },
      {
        "year": "—",
        "type": "股利",
        "amount": "無",
        "note": "—"
      }
    ],
    "sbc": {
      "q2_2026_pct": 6.22,
      "q1_2026_pct": 8.17,
      "trend": "金額年增 +2%、占營收比年減；Q1 為授予高峰",
      "gaap_vs_nongaap": "GAAP 營業利益 $19M vs 調整後 EBITDA $168M，差額主要為 SBC $62M 與 D&A",
      "structure_note": "股權結構（雙層股權、創辦人持股）、薪酬結構與近 12 個月內部人交易：證據包未涵蓋（數據限制）；SPAC 時期證券集體訴訟已以 $80M 和解、和解金已發放"
    }
  },
  "valuation": {
    "tier": "平台型（叫車／外送＋嵌入式金融）；同層錨＝UBER（成熟平台）、SE／MELI（新興市場平台＋金融）；無理想同層，溢折價獨立推導",
    "peers": [
      {
        "name": "SE",
        "fwd_pe": "證據包未涵蓋",
        "om": 8.42,
        "fcf_margin": 19.06,
        "note": "同區域直接對手"
      },
      {
        "name": "UBER",
        "fwd_pe": "證據包未涵蓋",
        "om": 12.13,
        "fcf_margin": 18.32,
        "note": "終端倍數錨（成熟平台）"
      },
      {
        "name": "MELI",
        "fwd_pe": "證據包未涵蓋",
        "om": 8.26,
        "fcf_margin": 35.27,
        "note": "平台＋金融終局樣板"
      },
      {
        "name": "DASH",
        "fwd_pe": "證據包未涵蓋",
        "om": 4.8,
        "fcf_margin": 13.46,
        "note": "外送單業務對照"
      }
    ],
    "fwd_pe": 24.43,
    "peg": 1.16,
    "percentile_5y": 0,
    "val_light": "🟡",
    "val_light_derivation": "分位：P/S 3.75 倍低於四個年度點的最低值 5.4 倍、EV/S 2.54 倍低於最低 4.4 倍、fwd PE 26.3 倍為 9 份快照窗最低——分位 0%（＜ 30% 為便宜）；PEG：FY2 fwd PE 24.4 ÷ EPS CAGR 約 21%（FY1 0.13→FY3 0.19）＝ 1.16（1.0–2.0 為合理）。兩尺取較嚴者＝🟡。交叉：EV/EBITDA 約 13 倍（EV ≈ 2.54 × TTM 營收 ≈ $9.4B ÷ FY26 指引中值 $730M）對 EBITDA +44–48%，不需依賴 GAAP 分母亦支持 🟡 偏便宜",
    "targets": {
      "short_1y": "$4.20（FY2 EPS 0.14 × 30 倍；成長 20%＋的合理倍數）",
      "mid_2y": "$4.94（FY3 EPS 0.19 × 26 倍）",
      "five_y": "$6.48（Base FY31 EPS 0.36 × 18 倍）",
      "bear_anchor": "Bear EPS 0.117（0.13 × 0.9）× 熄火 15 倍 ＝ $1.76（−49%）；淨現金約每股 $1.1（EV/S÷P/S 推得淨現金約 32% 市值）為實質地板，情境樹 Bear $1.96",
      "consensus": "26 位分析師平均目標 $5.86（$4.60–$8.00，離散 1.7 倍），現價低於均值 42%——續漲不需共識上修，市場比賣方悲觀"
    },
    "upside_short_pct": 23,
    "upside_mid_pct": 44
  },
  "trap_analysis": {
    "pattern": "「成長轉利潤但 GAAP 永遠不到位」——營運槓桿被 SBC、監管傭金上限與補貼戰吸收，估值長期停在低倍數",
    "evidence_against": "調整後 EBITDA +54%、利益率 16.9%（+360bp）、指引上修（營收 $4.10–4.15B／EBITDA $720–740M）、調整後 FCF TTM $450M、$750M 回購、SBC 占比年減至 6.22%、外送份額升至 55%",
    "evidence_for": "GAAP 營業利益率僅 1.9%；yfinance 口徑 FCF margin −5%；Mobility 營收 +12% 落後 GMV +18%（take rate 壓縮）；印尼傭金上限剛生效尚無一季實績；$1.0B 以上併購投向主場外",
    "bear_case": "18 個月內 −30% 以上的最可能路徑：印尼把傭金上限擴至四輪／外送＋ShopeeFood／GoTo 補貼戰重啟（獎勵占 GMV 回到 12%）＋金融服務 ECL 回升至 7%——EBITDA 指引下修、金融服務轉正跳票，股價回到 $2.0–2.4；監測：印尼 Mobility GMV 與 take rate、獎勵占 GMV、ECL 比率、分部 EBITDA",
    "monitor": [
      "集團獎勵占 GMV（季報）：＞ 12% 連 2 季＝陷阱正在發生",
      "Mobility take rate（營收÷GMV）：連 2 季年減 ＞ 50bp",
      "金融服務 ECL 比率：＞ 7%；撥備增速連 2 季高於放款增速",
      "調整後 EBITDA 利益率 TTM：＜ 14% 連 2 季",
      "GAAP 營業利益率：FY2027 仍 ＜ 3%＝GAAP 不到位假說成立"
    ],
    "verdict": "🟡",
    "label": "觀察期"
  },
  "appendix_a": {
    "signal": "B",
    "moat_score": 6.5,
    "growth_durability": 8,
    "quality_score": 7.25,
    "ai_risk": "🟡",
    "long_term_confidence": "中",
    "val": "🟡",
    "ma": "❌",
    "fpe_fy2": 24.43,
    "pct_5y": 0,
    "peg_fy2": 1.16,
    "upside_short_pct": 23,
    "upside_mid_pct": 44,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "B"
  },
  "scenario_ref": ".dd_build/runs/GRAB_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY2026": 0.13,
      "FY2027": 0.15,
      "FY2028": 0.19,
      "FY2029": 0.25,
      "FY2030": 0.3,
      "FY2031": 0.36
    },
    "fy_end_month": 12,
    "eps_basis": "GAAP 攤薄 EPS（US$，共識口徑 2026-09-04 快照：FY1 0.13／FY2 0.14／FY3 0.19）"
  },
  "catalysts": [
    {
      "date": "2026-11",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q3 2026 財報：首個含印尼二輪傭金上限的季度；金融服務虧損收窄幅度；獎勵占 GMV",
      "impact": "高",
      "watch": "印尼 Mobility GMV／take rate、分部 EBITDA、全年指引是否維持"
    },
    {
      "date": "2026-Q3",
      "date_precision": "quarter",
      "type": "other",
      "event": "Stash 交割（50.1%）",
      "impact": "低",
      "watch": "揭露對價與獲利能力；管理層稱 EBITDA 與 FCF 為正、2028 年 EBITDA $60M（來源：摘要）"
    },
    {
      "date": "2026-H2",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "台灣公平會對 foodpanda 台灣收購的裁定",
      "impact": "中",
      "watch": "附條件核准／否決；否決＝$600M 現金保留，反而移除補貼戰風險"
    },
    {
      "date": "2026-12",
      "date_precision": "month",
      "type": "regulatory",
      "event": "Grab–GoTo 合併案結果（市場預期年底前核准附條件或放棄）",
      "impact": "高",
      "watch": "KPPU 條件（定價／司機誘因）；成局＝印尼補貼結構性下降，不成＝維持現狀"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q4 2026 財報：金融服務 2H26 轉正驗證、放款餘額 ＞ $3B、FY2027 指引",
      "impact": "高",
      "watch": "分部調整後 EBITDA ≥ 0；ECL；FY27 EBITDA 指引是否對齊 2028 年 $1.5B 路徑"
    }
  ],
  "decision_inputs": {
    "signal": "B",
    "trap": "🟡",
    "val": "🟡",
    "ma": "❌",
    "runway_post_y5": "🟢",
    "moat_trend": "→",
    "moat": "C",
    "capalloc_grade": "B",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 5.17,
    "irr_base_pct": 13.6,
    "ev5y_pct": 93.7,
    "price_at_dd": 3.42,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": -14.07,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 44.44,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "held_now": false
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "9（MA❌例外）",
    "pacing": [
      "row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"
    ],
    "holding_cap": null,
    "requires_critic": [
      "產業態勢：裁決為強方向（進場）且屬法規敏感（印尼傭金上限）與競爭動態（ShopeeFood／inDrive／Bolt）型——請冷讀印尼監管外溢機率與補貼戰重啟機率是否被低估",
      "資本配置：$600M 台灣＋$425M Stash 皆在主場外且法說迴避對價問題，B 級評等是否過寬",
      "護城河等級 C 與前份 B 的差異屬方法論（二維加權）＋基本面（傭金上限）並列，請確認未重複扣分"
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
        "basis": "moat_trend='→', moat='C'"
      },
      {
        "row": "4",
        "condition": "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）",
        "hit": true,
        "basis": "ma='❌'"
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
        "basis": "signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-14.07, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"
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
        "basis": "signal='B', val='🟡'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": true,
        "basis": "signal='B', val='🟡', ma='❌'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": false,
        "basis": "signal='B', val='🟡', ma='❌'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": false,
        "basis": "signal='B', val='🟡', ma='❌'"
      },
      {
        "row": "9-verdict",
        "condition": "命中 row9 → 進場",
        "hit": true,
        "basis": "MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，verdict=進場（row4 pacing 已疊加，見上）"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": null,
    "exec_line": "衛星上限 3%。首階 1/3 於現價 $3.42 附近；第二階待 Q3 2026 財報（2026-11）確認印尼上限衝擊在指引內且金融服務虧損續收窄；第三階待金融服務 Q4 2026 轉正（2027-02）或週線站回 W104。已持有者：不加碼至第二階條件成立；新資金：只建首階。"
  },
  "triggers": [
    {
      "n": 1,
      "text": "H1 需求飛輪",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "on-demand GMV TTM 年增",
      "threshold": "＜ 12% 連 2 季削弱；＜ 8% 連 3 季反轉",
      "action": "削弱→停止加碼；反轉→減碼至首階",
      "source_freq": "季報",
      "date": "2026-11"
    },
    {
      "n": 2,
      "text": "H2 營運槓桿",
      "type": "假設驗證",
      "maps_to": "H2",
      "metric": "調整後 EBITDA 利益率 TTM／獎勵占 GMV",
      "threshold": "利益率 ＜ 14% 連 2 季；獎勵 ＞ 12% 連 2 季",
      "action": "任一命中→減碼一半",
      "source_freq": "季報",
      "date": "2027-02"
    },
    {
      "n": 3,
      "text": "H3 金融服務轉正",
      "type": "假設驗證",
      "maps_to": "H3",
      "metric": "金融服務分部調整後 EBITDA",
      "threshold": "Q4 2026 仍 ＜ 0",
      "action": "第三階不加；連 2 季未轉正→減碼",
      "source_freq": "季報",
      "date": "2027-02"
    },
    {
      "n": 4,
      "text": "R1 印尼監管擴大",
      "type": "清倉",
      "maps_to": "R1／Single Thing",
      "metric": "印尼傭金上限適用範圍",
      "threshold": "擴至四輪或外送（總統令／部會規章）",
      "action": "清倉，不等財報",
      "source_freq": "事件（即時）",
      "date": "—",
      "evidence_refs": [
        "regulatory_antitrust#0",
        "geo_supply_chain#0",
        "geo_supply_chain#1"
      ]
    },
    {
      "n": 5,
      "text": "R2 信用週期",
      "type": "減碼",
      "maps_to": "R2",
      "metric": "ECL 比率；撥備增速 vs 放款增速",
      "threshold": "ECL ＞ 7%；或撥備增速連 2 季高於放款增速",
      "action": "減碼至首階",
      "source_freq": "季報",
      "date": "2026-11"
    },
    {
      "n": 6,
      "text": "R3 競爭與多平台",
      "type": "風險",
      "maps_to": "R3",
      "metric": "外送 GMV 份額；獎勵占 GMV",
      "threshold": "份額 ＜ 50%；獎勵 ＞ 12% 連 2 季",
      "action": "減碼",
      "source_freq": "Momentum Works 年報／季報",
      "date": "2027-01",
      "evidence_refs": [
        "competitive_share_entrants#3",
        "competitive_share_entrants#4",
        "customer_second_source#0",
        "customer_second_source#1"
      ]
    },
    {
      "n": 7,
      "text": "R4 資本配置",
      "type": "風險",
      "maps_to": "R4",
      "metric": "台灣整合 EBITDA 拖累；Stash 減損",
      "threshold": "拖累 ＞ $100M／年或減損",
      "action": "資本配置降 C 級→持有年限上限中期、停止加碼",
      "source_freq": "季報／年報",
      "date": "2027-08",
      "evidence_refs": [
        "regulatory_antitrust#1"
      ]
    },
    {
      "n": 8,
      "text": "R5 油價與 take rate",
      "type": "風險",
      "maps_to": "R5",
      "metric": "Mobility 營收÷GMV",
      "threshold": "連 2 季年減 ＞ 50bp",
      "action": "警戒，暫停加碼",
      "source_freq": "季報",
      "date": "2026-11",
      "evidence_refs": [
        "end_markets#1",
        "supply_demand_durability#3"
      ]
    },
    {
      "n": 9,
      "text": "加碼：論點增強",
      "type": "加碼",
      "maps_to": "H3／H2",
      "metric": "金融服務轉正＋FY27 EBITDA 指引",
      "threshold": "分部 EBITDA ≥ 0 且 FY27 指引 ≥ $1.0B",
      "action": "第三階加至衛星上限 3%",
      "source_freq": "季報",
      "date": "2027-02"
    },
    {
      "n": 10,
      "text": "加碼：價格",
      "type": "加碼",
      "maps_to": "估值",
      "metric": "股價",
      "threshold": "回檔至 $3.0 以下且 1–3 項無削弱",
      "action": "第二階提前",
      "source_freq": "週線",
      "date": "—"
    },
    {
      "n": 11,
      "text": "估值過熱 trim",
      "type": "減碼",
      "maps_to": "估值",
      "metric": "FY2 fwd PE",
      "threshold": "＞ 45 倍（自身快照窗高點 44.6 倍以上）",
      "action": "最多 trim 三分之一，不清倉",
      "source_freq": "月度共識快照",
      "date": "—"
    },
    {
      "n": 12,
      "text": "複審",
      "type": "複審日期",
      "maps_to": "全部",
      "metric": "半年複審",
      "threshold": "—",
      "action": "重跑判斷",
      "source_freq": "—",
      "date": "2027-03-05"
    }
  ],
  "contradictions": [
    {
      "axis": "估值分母：GAAP EPS 便宜 vs GAAP 品質薄",
      "side_a": "PEG 1.16、P/S 與 EV/S 皆在自身歷史最低——便宜",
      "side_b": "GAAP 營業利益率 1.9%，EPS 內含淨現金利息收入，PE 分母品質差",
      "ruling": "選 A 側但換尺：分母爭議成立於 GAAP 口徑，故改以 EV/EBITDA 約 13 倍（對 EBITDA +44–48%）作主錨，結論不變；不把 GAAP PEG 當唯一依據",
      "evidence_level": "L1（已實現 EBITDA 與指引）＞ L3（GAAP 永不到位敘事）",
      "settle_metric": "FY2027 GAAP 營業利益率是否 ≥ 3%",
      "if_then": [
        "若 FY27 GAAP 營業利益率 ≥ 3% 且 SBC 占比 ＜ 5% → 換回 PE 尺、加碼至上限",
        "若 FY27 GAAP 營業利益率仍 ＜ 3% → 減碼至首階，估值只認 EV/EBITDA 且終端倍數降 16 倍"
      ]
    },
    {
      "axis": "印尼傭金上限衝擊幅度",
      "side_a": "分析師估 2026 EBITDA 下行 5–10%；印尼占營收 23%",
      "side_b": "管理層：二輪僅占 Mobility GMV 不到 6%（來源：摘要）；上限 7 月生效後 8 月仍上修全年指引",
      "ruling": "選 B 側：指引上修是 L1 事實、發生在上限生效之後；但把「擴大範圍」列為唯一清倉級觸發器，管理層 2 月稱政府未提案、5 月即簽令，其判斷不可作為擴大機率的依據",
      "evidence_level": "L1（上修指引）＞ L2（分析師估計）",
      "settle_metric": "Q3 2026 印尼 Mobility GMV 與 take rate",
      "if_then": [
        "若 Q3 印尼 Mobility 營收年增仍 ≥ 5% → 第二階加碼",
        "若總統令擴至四輪／外送 → 清倉"
      ],
      "evidence_refs": [
        "regulatory_antitrust#0",
        "geo_supply_chain#0",
        "geo_supply_chain#1"
      ]
    },
    {
      "axis": "競爭：份額上升 vs 多平台上架與新進者",
      "side_a": "外送份額 53.8%→55%、MTU 5,400 萬新高、對手退出",
      "side_b": "商家多平台上架成常態、傭金擠壓、inDrive 菲律賓 7 倍、Bolt 進泰國、ShopeeFood 升第二",
      "ruling": "可調和（程度差異）：份額數據（L1）勝過新進者敘事（L3），但定價權維度確實封頂——故護城河執行 8／定價 5、趨勢 →，不給 ↑",
      "evidence_level": "L1 份額 vs L3 敘事",
      "settle_metric": "2026 年外送 GMV 份額（Momentum Works，2027-01）與獎勵占 GMV",
      "if_then": [
        "若份額 ≥ 55% 且獎勵占 GMV ≤ 10% → 護城河趨勢改 ↑",
        "若份額 ＜ 52% 或獎勵 ＞ 12% 連 2 季 → 減碼"
      ],
      "evidence_refs": [
        "competitive_share_entrants#3",
        "competitive_share_entrants#4",
        "customer_second_source#0",
        "customer_second_source#1"
      ]
    },
    {
      "axis": "自駕：夥伴卡位 vs 對手繞過",
      "side_a": "Grab×WeRide 新加坡首個公開自駕叫車、投資 WeRide",
      "side_b": "ComfortDelGro×Pony.ai、Baidu 自營進新加坡／馬來西亞；頭部自駕商可能不需要平台",
      "ruling": "可調和：五年內東南亞人力成本與監管（司機生計）使自駕難以規模化替代（CEO 亦稱成本曲線落後，來源：摘要），列長期威脅 🟡，不進情境樹",
      "evidence_level": "L2（試點）vs L3（長期推演）",
      "settle_metric": "新加坡自駕車隊規模與 Grab 是否為主要分派平台",
      "if_then": [
        "若 2028 年前非 Grab 平台自駕車隊 ＞ 1,000 輛 → 護城河重評",
        "若 Grab 平台承接多家自駕商 → 執行分維持 8"
      ],
      "evidence_refs": [
        "substitute_technology#2"
      ]
    },
    {
      "axis": "資本配置：回購信心 vs 主場外併購",
      "side_a": "$750M 回購、累計承諾逾 $1.6B",
      "side_b": "$600M 台灣（監管敵意、補貼戰）＋$425M Stash（美國），法說迴避對價與燒錢問題",
      "ruling": "不可調和（方向相反）：選「B 級、非 A 也非 C」——回購與併購並行，併購金額約市值 7% 未達毀滅級；但持有年限與加碼掛台灣整合實績",
      "evidence_level": "L1（回購執行）vs L2（併購未交割）",
      "settle_metric": "台灣整合首年調整後 EBITDA 拖累",
      "if_then": [
        "若台灣拖累 ＞ $100M／年或 Stash 減損 → 資本配置降 C、持有年限上限中期、停止加碼",
        "若台灣 2027 年分部轉正 → 解除限制"
      ],
      "evidence_refs": [
        "regulatory_antitrust#1"
      ]
    },
    {
      "axis": "共識對照",
      "side_a": "26 位分析師平均目標 $5.86，現價低於均值 42%",
      "side_b": "共識 FY1 EPS 三個月上修 44%（0.09→0.13）但 FY3 下修 5%——長期路徑未上修",
      "ruling": "對照支持本裁決：續漲不需共識上修；目標離散 1.7 倍未達兩極分歧門檻。上修屬 stale=false 的可溯數字，但非本裁決依據",
      "evidence_level": "L2",
      "settle_metric": "FY3 共識是否止跌",
      "if_then": [
        "若 FY3 共識連 2 個月上修 → 論點增強",
        "若 FY3 共識再下修 ＞ 10% → 停止加碼"
      ]
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "SE／UBER／MELI 為同層 peer",
      "side_b": "近 30 天 peer 裁決：證據包未涵蓋",
      "ruling": "一句帶過：無近期 peer 裁決可對帳，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若後續 SE 判迴避 → 補寫差異理由",
        "若 SE 判進場 → 一致"
      ]
    },
    {
      "axis": "前份對照：裁決承繼",
      "side_a": "前份（2026-05-05）B 級、等 W104 $4.49 V 反轉確認才進場",
      "side_b": "本次進場｜衛星",
      "ruling": "前份距今 123 天、不受 90 天承繼保護；且前份約束（週線反轉為進場前提）在現行矩陣已降為節奏調節，屬已退役之閘所致觀望，本次依現行規則重裁",
      "evidence_level": "方法論",
      "settle_metric": "—",
      "if_then": [
        "若週線站回 W104 → 第三階加碼",
        "若跌破 $3.0 且 1–3 項無削弱 → 第二階提前"
      ],
      "prior_field": "dca_verdict"
    },
    {
      "axis": "前份漂移：角色",
      "side_a": "本次：衛星",
      "side_b": "前份：無（v12.3 格式無角色欄，敘述為衛星候選）",
      "ruling": "主因方法論（v17 新增角色欄）；基本面與價格次之",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "dca_role"
    },
    {
      "axis": "前份漂移：週線狀態",
      "side_a": "本次：❌（現價距 52 週高點 −47%、52 週低點上方 4.6%，低於長期均線；W250 斜率實值證據包未涵蓋）",
      "side_b": "前份：🟠（❌ 經救援降級）",
      "ruling": "主因價格（3.62→3.42、跌破前份 $3.48 警戒線）；其次方法論（本次護城河 6.5 不滿足救援條件 ≥ 8）",
      "evidence_level": "L1",
      "settle_metric": "週收站回 W104",
      "if_then": [
        "站回 W104 → 第三階",
        "跌破 $3.0 → 第二階提前（前提 1–3 項無削弱）"
      ],
      "prior_field": "ma"
    },
    {
      "axis": "前份漂移：裁決價",
      "side_a": "本次：$3.42",
      "side_b": "前份：$3.62",
      "ruling": "價格變了（−5.5%）；基本面同期轉強（Q2 上修指引），故估值訊號不變",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "price_at_dd"
    },
    {
      "axis": "前份漂移：護城河趨勢",
      "side_a": "本次：→",
      "side_b": "前份：無此欄",
      "ruling": "首次建立；基本面（份額升／傭金上限）並列",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "moat_trend"
    },
    {
      "axis": "前份漂移：五年後跑道",
      "side_a": "本次：🟢",
      "side_b": "前份：無此欄",
      "ruling": "首次建立；方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "runway_post_y5"
    },
    {
      "axis": "前份漂移：類型",
      "side_a": "本次：品質複利成長",
      "side_b": "前份：無此欄",
      "ruling": "首次建立；方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "archetype"
    },
    {
      "axis": "前份漂移：重啟觸發",
      "side_a": "本次：無（進場）",
      "side_b": "前份：無此欄",
      "ruling": "方法論驅動",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "rearm_trigger"
    },
    {
      "axis": "前份漂移：情境六欄 bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／upside_5y_pct／ev5y_pct／irr_base_pct／asym_ratio／max_dd_pct",
      "side_a": "本次：Bull $12.48／Bear $1.96／25%／30%／Base +89%／期望值 +94%／IRR 13.6%／不對稱 5.2／回撤 −30%～−48%",
      "side_b": "前份：v12.3 僅有 upside_5y_pct 176%，其餘無此欄",
      "ruling": "主因方法論（情境樹確定性計算器＋GAAP EPS 路徑取代舊 5 年上行）；價格與基本面次之",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—"
      ],
      "prior_field": "ev5y_pct"
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "印尼政策可預測性：管理層 2026-02 稱政府未提案、2026-05 即簽總統令；我對「上限止於二輪」的判斷依賴同一批管理層的口徑",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "geo_supply_chain#0"
        ]
      },
      {
        "text": "金融服務放款餘額年增 197% 未經完整信用週期；ECL 下降可能是新放款稀釋分母的統計效果而非風控能力",
        "evidence_refs": []
      },
      {
        "text": "台灣公平會若附嚴苛條件核准，Grab 進入與 Uber Eats 的補貼戰而非取得利潤；法說對進度與里程碑迴避",
        "evidence_refs": [
          "regulatory_antitrust#1"
        ]
      },
      {
        "text": "地區集中：三國占營收逾 70%，馬來西亞若跟進印尼式傭金上限，本判斷全面失效",
        "evidence_refs": [
          "geo_supply_chain#1"
        ]
      },
      {
        "text": "週線均線實值（W52／W104／W250 與斜率）證據包未涵蓋，❌ 為推論；若實際為 🟠 節奏應更積極",
        "evidence_refs": []
      },
      {
        "text": "Q3 2025 法說 Q&A 對印尼成長拒給數字；區域企業成本 $114M 的 AI 基建占比未拆（來源：摘要）——營運槓桿可能被 AI 成本吃掉一部分",
        "evidence_refs": []
      }
    ],
    "failure_story": "五年後虧 50% 的故事：印尼把傭金上限擴至四輪與外送，馬來西亞跟進；補貼戰重啟使獎勵回到 GMV 12%；金融服務在區域信用週期中 ECL 升破 7%，EBITDA 停在 $0.8B，市場給 14 倍，股價 $1.96——此故事直接撞上 Single Thing（印尼擴大）✅，不需改寫",
    "second_failure": "成功但劣化：EBITDA 如期達 2028 年 $1.5B，但主要靠金融服務放款擴張兌現，市場把估值框架從「平台倍數」切換到「新興市場消費金融銀行倍數」（P/B 與信用週期定價），終端倍數 12–14 倍而非 18 倍，五年報酬由 +89% 降至約 +30%；此形態機率不可忽略，已反映在 Bull 終端 24 倍（非 30 倍）與 Base 18 倍",
    "max_dd": {
      "lo": -48,
      "hi": -30,
      "path_risk": "🟡",
      "trigger_time": "2026-11 至 2027-02（首個含印尼上限的季度＋金融服務轉正驗證）；恢復峰值時間：若論點完整約 12–18 個月，若 Single Thing 觸發則論點已破"
    }
  },
  "kill_metrics": [
    {
      "metric": "印尼傭金上限適用範圍",
      "bear_threshold": "擴至四輪或外送",
      "window": "事件即時",
      "source": "總統令／交通部規章／KPPU",
      "last_status": "ok"
    },
    {
      "metric": "金融服務 ECL 比率",
      "bear_threshold": "＞ 7%（現 4.6%）",
      "window": "任一季",
      "source": "季報分部揭露",
      "last_status": "ok"
    },
    {
      "metric": "金融服務分部調整後 EBITDA",
      "bear_threshold": "Q4 2026 仍 ＜ 0",
      "window": "2027-02 財報",
      "source": "季報",
      "last_status": "unknown"
    },
    {
      "metric": "集團獎勵占 GMV",
      "bear_threshold": "＞ 12% 連 2 季（現約 10%）",
      "window": "連 2 季",
      "source": "季報",
      "last_status": "ok"
    },
    {
      "metric": "調整後 EBITDA 利益率 TTM",
      "bear_threshold": "＜ 14% 連 2 季（現 16.9%）",
      "window": "連 2 季",
      "source": "季報",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "輸入：營收 +22%、調整後 EBITDA 利益率 16.9%、GAAP 營業利益率 1.9%、FY1 EPS 0.13 ＞ 0、淨現金。\n判斷：GAAP 已轉正故用 PE／PEG 尺，但獲利品質仍以調整後 EBITDA 為主，故主類品質複利成長、副類未獲利高成長（EV/EBITDA 交叉）。\n下游：估值以 PEG 為主尺、EV/EBITDA 為交叉錨；不走循環錶。",
    "thesis": "輸入：外送份額 55%、MTU 5,400 萬、EBITDA 三年翻三倍目標、金融服務 2H26 轉正承諾。\n判斷：三個假設各對應密度變現、營運槓桿、第二曲線；風險以印尼監管（可擴大、可觀測）為唯一清倉級。\n下游：Single Thing＝印尼上限擴大（12–24 個月約 20%），H2 為情境樹主軸。",
    "industry": "輸入：外送 GMV 2025 年 +18%、補貼收斂、foodpanda 退出台灣、GoTo 弱化、印尼傭金上限。\n判斷：擴張期（II）整併中，利潤池淨流入平台端但被政策折扣；社會容忍度為四檢查點中唯一 🔴。\n下游：熄火情境含監管而非需求崩落；Bear 機率 30%。",
    "moat": "輸入：執行 8（份額升、司機 +16%、對手退出）、定價 5（傭金上限、多平台上架、inDrive 10% 傭金）；同業 OM／FCF spread 為負。\n計算：均值（8＋5）÷2＝6.5 → C 級；閘一（spread 正）不過故不得 ≥ 8；趨勢一擴一縮取 H2 關鍵維度→ →。\n下游：C 級＋→ 不觸發硬否決；角色上限衛星、長期信心中。",
    "growth": "輸入：交易用戶 1.29 億（來源：摘要）、外送 TAM $22.7B→$36B、GrabMart 為外送 1.7–2.6 倍、金融服務放款 $2.3B→$3B。\n判斷：跑道 ≥ 10 年、五年後仍有金融服務與 GrabMart 第二曲線且滲透率低→🟢；衰退信號 1–2 個（SBC 半亮、FCF 口徑）→🟡。\n下游：成長持久性 8；品質分（6.5＋8）÷2＝7.25→B 級。",
    "quality": "輸入：Q2 調整後 EBITDA $168M／營收 $997M＝16.9%；SBC $62M÷$997M＝6.22%；調整後 FCF TTM $450M；yfinance FCF margin −5%。\n判斷：經營口徑改善明確，但 GAAP 與現金流口徑受 SBC 與銀行併表干擾；體質五項否決 0 項不過。\n下游：品質分 7.25 不降級；FCF 口徑對帳列監測。",
    "governance": "輸入：回購 $400M 執行＋$500M＋$750M 承諾；併購 Stash EV $425M＋台灣 $600M；SBC 約 1.9% 市值。\n計算：併購 ROIIC N/A、回購收益率邊界（GAAP 3.8%／EBITDA 7.7%）、SBC 淨稀釋 ≤ 1% 過→適用 2 項過 1 項＝B。\n下游：不觸發持有年限上限；台灣整合實績為降 C 級觸發。",
    "valuation": "輸入：現價 3.42、FY1 0.13／FY2 0.14／FY3 0.19；P/S 3.75 vs 年度最低 5.4；EV/S 2.54 vs 最低 4.4。\n計算：fwd PE FY2＝3.42÷0.14＝24.4；CAGR＝(0.19÷0.13)^(1/2)−1≈21%；PEG＝24.4÷21＝1.16→🟡；分位 0%→🟢；取較嚴＝🟡。EV≈2.54×TTM 營收≈$9.4B÷FY26 EBITDA 中值 $730M≈13 倍。\n下游：估值不是約束；1Y $4.20（+23%）、2Y $4.94（+44%）、5Y $6.48（+89%）；Bear 錨 $1.76 但淨現金約每股 $1.1 為地板。",
    "trap_analysis": "輸入：GAAP 營業利益率 1.9% vs 調整後 EBITDA 利益率 16.9%；Mobility 營收 +12% vs GMV +18%；指引上修。\n判斷：陷阱模式＝GAAP 永不到位；L1 事實（上修、+54% EBITDA）壓過敘事，但上限剛生效無實績→觀察期 🟡。\n下游：最強空頭一擊＝印尼擴大＋補貼戰＋ECL，18 個月 −30% 至 $2.0–2.4；監測獎勵占 GMV 與 take rate。",
    "premortem": "輸入：Bear 終端 $1.96（−43%）、現價已距高點 −47%、52 週低點上方 4.6%。\n計算：Max DD 範圍 −30%～−48%（寬 18pp），下界取 Bear 情境略高於終端跌幅因淨現金地板；路徑 🟡。\n下游：論點完整不因波動砍倉；觸發時點 2026-11 至 2027-02，故第二、三階掛該兩次財報。"
  },
  "evidence_dismissed": [],
  "plain": {
    "verdict_line": "現在可以小量進場當衛星，別當長期核心。",
    "verdict_sub": "先買三分之一，等十一月財報確認印尼傭金上限沒傷到指引，再買第二筆。",
    "five": {
      "how_it_makes_money": "叫車與外送抽成，加上訂閱、廣告，以及三國數位銀行的放款利差。營收每年成長約 22%。",
      "why_now": "業績上修、份額還在升，但股價已從高點跌了近一半。市場把印尼監管當成全公司的問題在定價。",
      "why_this_size": "定價權被政府和多平台上架封頂，護城河只有中等。所以是衛星，上限 3%。",
      "biggest_fear": "印尼把傭金上限從機車擴到汽車與外送。印尼占營收 23%，一旦擴大就清倉。",
      "how_to_act": "現價附近買三分之一。十一月財報過關再買一筆，明年二月金融服務轉正再補滿。"
    },
    "business": {
      "what_to_whom": "賣給東南亞城市居民日常的代步、三餐和小額金融，每月有 5,400 萬人在用。",
      "why_customers_stay": "同一個 App 解決三件事，訂閱與點數把人留住。商家和司機則因為單量最多而留下。",
      "moat_direction": "等級中等，方向持平。最弱處是定價：政府能一紙命令把抽成砍掉一半，商家也同時上架對手。"
    },
    "bets": [
      {
        "claim": "密度優勢會變成利潤，三年內獲利翻三倍。",
        "wrong_when": "獲利率連兩季掉到 14% 以下，或補貼占交易額回到 12% 以上。"
      },
      {
        "claim": "印尼傭金上限止於機車，影響不到 6% 的叫車交易額。",
        "wrong_when": "總統令擴到汽車或外送。"
      },
      {
        "claim": "數位銀行今年下半年轉正，壞帳率守在 5% 以下。",
        "wrong_when": "明年二月財報仍虧損，或壞帳率升破 7%。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "印尼監管擴大到汽車與外送，示範效應外溢到馬來西亞。"
      },
      {
        "clock": "🔥",
        "text": "放款一年增加近兩倍還沒經過景氣循環，壞帳率從 4.6% 反彈。"
      },
      {
        "clock": "🐢",
        "text": "花了逾 10 億美元買台灣外送與美國理財平台，都在主場之外。"
      }
    ],
    "market_wrong": "市場假設印尼傭金上限會蔓延到整本帳，且放款會在下一輪循環爆掉。但上限生效後管理層仍上修全年指引，壞帳率也在下降。以獲利倍數看，現在只有約 13 倍，卻對應四成以上的獲利成長。",
    "growth_funding": "內部能養出的成長上限約 19%，基準情境要 22.6%，缺口靠獲利率擴張補。若擴張不來，就退回悲觀情境。",
    "stories": {
      "bull": "補貼戰不再重演，金融服務變成第二個利潤引擎，台灣整合順利。五年後每股獲利 0.52，股價約 12.48。",
      "base": "營收每年成長約 17%，獲利率慢慢升到 25%。五年後每股獲利 0.36，股價約 6.48，年化報酬約 13.6%。",
      "bear": "印尼監管擴大加上補貼戰與壞帳升溫，獲利五年不成長。股價約 1.96，虧四成多。"
    },
    "change_my_mind": [
      {
        "what": "印尼傭金上限的適用範圍",
        "threshold": "擴到汽車或外送",
        "then": "清倉，不等財報",
        "when": "—"
      },
      {
        "what": "金融服務分部是否轉正",
        "threshold": "明年二月財報仍虧損",
        "then": "不加碼，連兩季未轉正就減碼",
        "when": "2027-02"
      },
      {
        "what": "壞帳率與補貼",
        "threshold": "壞帳率破 7%，或補貼占交易額連兩季超過 12%",
        "then": "減碼回第一筆的量",
        "when": "2026-11"
      }
    ],
    "prior_compare_reason": "上一份要等週線反轉才進場，這次改為分批進場。主因是方法論改變，週線只影響節奏不擋裁決；其次是業績上修而股價更低。",
    "how_to_lose": "第一種死法是印尼監管擴大加補貼戰，獲利停滯、倍數壓到 14 倍。第二種是獲利如期達標，但靠放款撐出來，市場改用銀行的方式估值，五年只賺三成。",
    "evidence_quality": "覆蓋競爭、監管、地緣、終端市場、替代技術與資本市場軸，數字為 2026 年第二季。最新一季逐字稿缺檔，四季內容皆讀摘要，管理層口徑的信心度較低。"
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


