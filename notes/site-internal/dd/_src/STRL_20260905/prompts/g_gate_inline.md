你是 stock-analyst v17 的**判斷層閘（gate）**，標的 STRL（20260905）。你未參與寫判斷，這是一次跨模型冷讀。你的任務只有一件：**依下列 ①–⑦ 逐條複核判斷物，計數判斷級 🔴**。

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

## 輸出（一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20260905/gate_audit.md`，格式固定，下游機械解析）

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

**輪次上限 `6` 輪。** 一次 Write 完成，寫完即回報，不要回讀自己寫的 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20260905/gate_audit.md`。

## 回報（≤100 字）

判斷級 🔴 = N、🟡 = M，以及 🔴 各條的軸別與指向欄位。


===== BUNDLE =====

## ① 任務頭

標的：STRL　日期：20260905　角色：stock-analyst v16.2 三步制的判斷層 critic（gate） agent。

輸出 critic gate 判定（PASS／PASS-with-fixes／FAIL）與逐條 finding，依 `references/critic-gates.md` 全文的 checklist 逐項作答。

---

## ③ Evidence 緊湊版

ticker=STRL　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 486.49, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-08-03", "trading_days_since": 25, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 4, "current": 33.12, "high": {"value": 34.03, "date": "2025-12-31"}, "low": {"value": 9.19, "date": "2022-12-31"}, "current_percentile_within_annual_points": 96.3}, "ps": {"n_points": 4, "current": 4.33, "high": {"value": 3.97, "date": "2025-12-31"}, "low": {"value": 0.55, "date": "2022-12-31"}, "current_percentile_within_annual_points": 100.0}, "ev_s": {"n_points": 4, "current": 4.29, "high": {"value": 3.95, "date": "2025-12-31"}, "low": {"value": 0.73, "date": "2022-12-31"}, "current_percentile_within_annual_points": 100.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 732.94, "fy1_eps": 18.72, "fwd_pe": 39.15}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 860.84, "fy1_eps": 18.72, "fwd_pe": 45.99}, {"snapshot_date": "2026-06-04", "price_used": 882.43, "fy1_eps": 18.74, "fwd_pe": 47.09}, {"snapshot_date": "2026-06-23", "price_used": 804.76, "fy1_eps": 18.92, "fwd_pe": 42.53}, {"snapshot_date": "2026-07-16", "price_used": 638.56, "fy1_eps": 19.31, "fwd_pe": 33.07}, {"snapshot_date": "2026-07-30", "price_used": 596.77, "fy1_eps": 19.1, "fwd_pe": 31.24}, {"snapshot_date": "2026-08-13", "price_used": 576.48, "fy1_eps": 20.03, "fwd_pe": 28.78}, {"snapshot_date": "2026-08-28", "price_used": 486.49, "fy1_eps": 20.03, "fwd_pe": 24.29}, {"snapshot_date": "2026-09-04", "price_used": 486.49, "fy1_eps": 20.03, "fwd_pe": 24.29}], "current": 24.29, "high": 47.09, "low": 24.29, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": -44.87, "return_26w_pct": 23.13, "excess_return_13w_pct": -49.4, "excess_return_26w_pct": 8.61, "benchmark": "^GSPC", "rsi14": 40.85, "rsi14_usable": true, "distance_from_52w_high_pct": -51.04, "distance_from_52w_low_pct": 71.56, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 20.03, "fy2": 25.4, "fy3": 28.91}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 20.03, "fy2": 25.4, "fy3": 28.91}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 18.74, "fy2": 22.89, "fy3": 20.76}, "fy1": {"revision_pct": 0.0, "from": 20.03, "to": 20.03, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 0.0, "from": 25.4, "to": 25.4, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 0.0, "from": 28.91, "to": 28.91, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 6.88, "fy2_revision_90d_pct": 10.97, "fy3_revision_90d_pct": 39.26, "stale": false, "note": null}, "peer_financials": {"STRL": {"gross_margin_pct": 23.81, "operating_margin_pct": 18.13, "fcf_margin_pct": 14.02, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "EME": {"gross_margin_pct": 19.43, "operating_margin_pct": 9.6, "fcf_margin_pct": 6.3, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "FIX": {"gross_margin_pct": 25.66, "operating_margin_pct": 16.45, "fcf_margin_pct": 19.24, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "PWR": {"gross_margin_pct": 15.46, "operating_margin_pct": 6.12, "fcf_margin_pct": 7.27, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "MTZ": {"gross_margin_pct": 12.91, "operating_margin_pct": 5.14, "fcf_margin_pct": 1.52, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-08-04", "url": "https://www.sec.gov/Archives/edgar/data/874238/000087423826000103/strl-20260630.htm", "excerpt": null, "note": "filing 全文內找不到 concentration／customer concentration 相關段落"}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 FY2026（三個月期間至 2026-06-30，公告於 2026-08-03）", "items": [{"metric": "營收（GAAP）", "value": 1170.0, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "consensus 約 $963.25M（Yahoo Finance／Zacks 引用之 Wall Street 估計，來源非公司本身）；實際優於估計", "prior_quarter": "Q1 FY2026: $825.7M（QoQ +41.7%）；YoY +90%（原文口徑）"}, {"metric": "Non-GAAP（調整後）營業利益", "value": 251.8, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus 調整後營業利益", "prior_quarter": "Q1 FY2026: $158.2M"}, {"metric": "Non-GAAP（調整後）營業利益率", "value": 21.6, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus 調整後營業利益率", "prior_quarter": "Q1 FY2026: 19.2%"}, {"metric": "GAAP 營業利益", "value": 219.3, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus GAAP 營業利益", "prior_quarter": "Q1 FY2026: $137.8M"}, {"metric": "GAAP 營業利益率", "value": 18.8, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus GAAP 營業利益率", "prior_quarter": "Q1 FY2026: 16.7%"}, {"metric": "自由現金流（FCF，推算）", "value": 112.4, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "推算：六個月營運現金流 $328.0M（公司新聞稿）減六個月資本支出 $69.6M（10-Q，公司未直接揭露單季 FCF），再減去已知 Q1 營運現金流 $165.6M 與 Q1 資本支出 $19.6M 反推 Q2 單季（OCF $162.4M − Capex $50.0M）", "vs_consensus": "查無 consensus FCF", "prior_quarter": "Q1 FY2026: 推算 FCF 約 $146.0M（OCF $165.6M − Capex $19.6M）"}, {"metric": "FCF Margin（推算）", "value": 9.6, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "推算：FCF $112.4M / 營收 $1,170M", "vs_consensus": null, "prior_quarter": "Q1 FY2026: 約 17.7%（$146.0M / $825.7M）"}, {"metric": "SBC 占營收 %", "value": 0.69, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿／10-Q：SBC $8.1M；占營收 $1,170M", "vs_consensus": null, "prior_quarter": "Q1 FY2026: SBC $7.5M，占營收 $825.7M ≈ 0.91%"}, {"metric": "全年 2026 財測（管理層指引，本次上修）", "value": "營收 $4.00B–$4.15B；調整後稀釋 EPS $19.70–$20.30；調整後 EBITDA $891M–$916M", "unit": "mixed", "as_of": "隨 Q2 FY2026 財報同步發布，2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "上修前（Q1 財報時，2026-05-04）：營收 $3.70B–$3.80B；調整後稀釋 EPS $18.40–$19.05；調整後 EBITDA $843M–$873M", "prior_quarter": null}, {"metric": "調整後稀釋 EPS", "value": 5.8, "unit": "US$", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "consensus 約 $4.99（Yahoo Finance 引用 Wall Street 估計，非公司揭露）；Beat +$0.81", "prior_quarter": "Q1 FY2026: $3.59"}, {"metric": "簽約在手訂單（Signed Backlog）", "value": 4.33, "unit": "US$ billion", "as_of": "季末 2026-06-30，公告於 2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": null, "prior_quarter": "Q1 FY2026 (2026-03-31): $3.80B；YoY +116%"}, {"metric": "合併在手訂單（Combined Backlog，含未簽約 awarded）", "value": 5.62, "unit": "US$ billion", "as_of": "季末 2026-06-30，公告於 2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": null, "prior_quarter": "Q1 FY2026 (2026-03-31): $5.15B；YoY +150%"}, {"metric": "E-Infrastructure 分部營收", "value": 905.0, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "YoY +192%；分部調整後營業利益率 23.3%；資料中心／半導體／製造業專案占該分部在手訂單 92%", "prior_quarter": null}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-05-06 | Sterling's E-Infrastructure segment revenue accelerated 174% YoY in Q1 2026 (company-wide revenue +90%); segment is now ~60% of total revenue at ~24% margin and is guided for 40%+ full-year 2026 revenue growth, driven by hyperscaler/AI data-center demand. | Yahoo Finance - "Will Sterling's 125% Data Centre Growth Extend Into 2026?", https://finance.yahoo.com/news/sterlings-125-data-centre-growth-152200180.html | moat_trend,thesis.H,valuation |
| competitive_share_entrants#1 | + | 2026-08-01 | Sterling raised FY2026 revenue guidance to $3.7-3.8 billion (a 20% increase from the prior guidance midpoint); signed backlog climbed 78% YoY to $3.8 billion and combined backlog rose 131% to $5.2 billion, with total visibility near $6.5 billion — management attributes this to Sterling's integrated site-development-plus-electrical positioning (via the CEC acquisition) strengthening its competitive standing as data-center capex expands. | Yahoo Finance - "Sterling and Data Centers: The Integrated Buildout Trade", https://finance.yahoo.com/markets/stocks/articles/sterling-data-centers-integrated-buildout-150700712.html | thesis.H,decision_inputs.bull,valuation,triggers |
| competitive_share_entrants#2 | 0 | 2026-09-01 | Sterling's identified competitors in mission-critical/data-center construction include Quanta Services and EMCOR (both also reporting robust hyperscaler-driven demand), plus Fluor, Granite Construction, Skanska USA, MasTec, AECOM, Kiewit, Webcor and Turner — a broad field of large diversified peers rather than a single disruptive new entrant. | ZoomInfo - "Sterling Infrastructure Competitors & Alternatives (2026)"; Yahoo Finance - "3 Infrastructure Stocks Fueling the Data Center Building Boom" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#3 | - | 2026-08-15 | YTD 2026 stock performance shows Sterling (STRL) +68.7% vs closest AI-infrastructure comp Comfort Systems (FIX) +77.4%, while Quanta Services +49.5% and EMCOR +22.6% — all outperforming the Zacks Construction sector (+7-11%) and S&P 500 (+10.9-11.8%), but Comfort Systems specifically outpacing Sterling on the same AI-buildout theme. | Zacks via Yahoo Finance - "Sterling vs. Comfort Systems: Which AI Infrastructure Stock Wins?", https://finance.yahoo.com/technology/ai/articles/sterling-vs-comfort-systems-ai-135400134.html | valuation,thesis.R,decision_inputs.bear |
| customer_second_source#0 | - | 2026-05-01 | Sterling's E-Infrastructure customer concentration was last disclosed at 35% of segment revenue from four customers (fiscal 2022); the company has not disclosed updated concentration figures in its Q4 2025 or Q1 2026 earnings materials even though the E-Infrastructure segment has more than doubled in size since, and analysts note customer identities are not disclosed, making single-source risk hard for investors to verify directly. | Beating the Tide - "Sterling Infrastructure (STRL) Q1 2026 Update: Tsunami Confirmed, Asymmetry Spent", https://www.beatingthetide.com/p/sterling-infrastructure-strl-q1-2026-update-target-1010 | thesis.R,decision_inputs.bear,moat_trend |
| customer_second_source#1 | 0 | 2026-09-01 | No direct evidence found of any named Sterling customer actively adding a second/competing site-development or electrical contractor, or bringing that scope of work in-house. The 2026 hyperscale data-center GC market instead remains concentrated among a small set of program managers (Turner, DPR, Mortenson, Hensel Phelps, Holder, Clayco) with specialized MEP subcontractors (e.g., Rosendin Electric) self-performing the electrical package (30-40% of total construction cost) — i.e. the observed industry pattern is trade-specialist self-performance within GC-led teams, not owner-side insourcing away from contractors like Sterling. | Buildermuse - "Top 20 Data Center Construction Contractors in 2026", https://buildermuse.com/commercial/the-top-20-data-center-construction-contractors/; Maktinta - "Who Builds AI Data Centers (and Who's Hiring) in 2026", https://www.maktinta.com/post/ai-data-center-construction-and-hiring-2026 | thesis.R,decision_inputs.bear |
| customer_concentration_credit#0 | + | 2025-12-31 | E-Infrastructure Solutions segment top-4-customer revenue concentration has declined over three years: 40% in FY2023, 31% in FY2024, 27% in FY2025 (per FY2025 10-K disclosure). | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | moat_trend,decision_inputs.bear |
| customer_concentration_credit#1 | - | 2025-12-31 | Transportation Solutions segment top-4-customer concentration (state DOTs) has risen: 50% in FY2023, 47% in FY2024, 58% in FY2025. | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | thesis.R,decision_inputs.bear |
| customer_concentration_credit#2 | 0 | 2025-12-31 | In FY2025, no single customer accounted for more than 10% of Sterling's consolidated revenue, though the 10-K discloses that loss of a top customer in either segment could have a material adverse effect. | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | decision_inputs.bear |
| customer_concentration_credit#3 | 0 | 2022-12-31 | Historical baseline: in FY2022, the top four customers accounted for 35% of E-Infrastructure segment revenue (segment has more than doubled in size since, per subsequent 10-K disclosures showing declining concentration ratio). | Simply Wall St News, "Should Data Center-Fueled E-Infrastructure Expansion and CEC Deal Require Action From Sterling Infrastructure (STRL) Investors?", citing Sterling FY2022 10-K | moat_trend |
| customer_concentration_credit#4 | 0 | 2026-07-24 | Moody's (reported by CNBC, 2026-07-24) said 'unprecedented' AI capex spending threatens the credit quality of Amazon, Meta, Alphabet, Microsoft, Oracle and CoreWeave -- all customers/counterparties in the hyperscale data center buildout that Sterling's E-Infrastructure segment serves -- but noted Microsoft, Alphabet, Amazon and Meta retain among the strongest corporate balance sheets globally with no imminent investment-grade downgrade risk. | CNBC, "Moody's says 'unprecedented' AI spending threatens credit quality of Amazon, Meta, Alphabet and others", cnbc.com/2026/07/24/moodys-ai-spending-credit-quality-amazon-meta-alphabet.html | thesis.R,decision_inputs.bear |
| customer_concentration_credit#5 | - | 2025-11-01 | Oracle -- a major hyperscale/AI-infrastructure capex spender -- is the weakest-credit name among large AI capex spenders: rated Baa2 with negative outlook (two notches above junk), net leverage above 3.5x, ~500% debt-to-equity; Barclays warned in November 2025 that Oracle's debt could be downgraded to BBB-, the lowest investment-grade rating before junk status. | 24/7 Wall St, "Bad News for NVIDIA, Amazon, and Microsoft: There's No Longer Enough Cash for AI"; Barclays Oracle debt downgrade coverage | thesis.R,decision_inputs.bear |
| supply_demand_durability#0 | + | 2026-06-30 | At June 30, 2026, Sterling's signed backlog rose 116% year-over-year to $4.3 billion, and combined backlog (signed + awarded not signed) rose 150% year-over-year to $5.6 billion, driven by E-Infrastructure demand. | Zacks (via Globe and Mail / TradingView), "Can Sterling's Backlog Strengthen Its Infrastructure Growth Prospects?" | thesis.H,supply_demand_durability |
| supply_demand_durability#1 | + | 2026-06-30 | In Q2 2026 (quarter ended June 30, 2026), Sterling's E-Infrastructure segment revenue grew 192% year-over-year and signed backlog grew 165% year-over-year, with mission-critical (data center/semiconductor) projects accounting for 92% of the segment's backlog; legacy site development revenue alone grew 111%. | Zacks (via Globe and Mail / TradingView), "Is Sterling's 192% E-Infrastructure Growth Just Getting Started Now?" / "Can Sterling's Backlog Strengthen Its Infrastructure Growth Prospects?" | thesis.H,moat_trend |
| supply_demand_durability#2 | + | 2026-06-30 | Following record Q2 2026 results, Sterling raised full-year 2026 guidance, targeting roughly 25% revenue growth for 2026; management ties the outlook to structurally expanding end markets (large-scale data centers, semiconductor fabs, advanced manufacturing) with hyperscaler customers now scoping campus projects lasting up to 12 years. | PR Newswire, "Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance"; Seeking Alpha, "Sterling Infrastructure Q2 2026 Review: A Triple Beat Sold On The Mix" | thesis.H,decision_inputs.bear |
| supply_demand_durability#3 | - | 2026-07-24 | Moody's (per CNBC, 2026-07-24) flagged 'unprecedented' AI capex spending as a threat to hyperscaler credit quality; separately, analysts note the AI capex cycle (aggregate hyperscaler capex ~$700B in 2026, projected ~$820B in 2027 per Moody's, and up to $1.15T cumulative 2025-2027 per Goldman Sachs) could run ahead of monetization -- the bear case is that Sterling's E-Infrastructure demand durability is contingent on hyperscalers continuing to fund a capex cycle that some analysts flag as increasingly debt- and off-balance-sheet-financed rather than purely cash-flow funded. | CNBC, "Moody's says 'unprecedented' AI spending threatens credit quality of Amazon, Meta, Alphabet and others", cnbc.com/2026/07/24/moodys-ai-spending-credit-quality-amazon-meta-alphabet.html | thesis.R,decision_inputs.bear,triggers |
| regulatory_antitrust | - | - | (status=none；無 findings) |  |  |
| reg_tariff_export#0 | - | 2026-04-06 | 2026年4月2日總統公告重整鋼鐵/鋁/銅第232條關稅，4月6日生效：鋼鐵/鋁/銅製品加徵50%關稅，衍生品加徵25%關稅，且計稅基礎改為進口品全額完稅價值（含衍生品）；6月再調整擴大低稅率適用範圍並將美國原產金屬含量門檻從95%降至85%。 | Perkins Coie "Restructured and Additional Section 232 Tariffs on Aluminum, Steel, and Copper"; White & Case "United States modifies steel, aluminum, and copper Section 232 tariffs" | thesis.R,decision_inputs.bear,valuation |
| reg_tariff_export#1 | - | 2026-08-01 | STRL 為重型土木與混凝土承包商，對瀝青、混凝土、鋼鐵等主要營建原料價格波動高度暴露；在固定價格合約下，原料或人工成本意外上漲會侵蝕毛利並影響專案獲利能力。 | Simply Wall St — Sterling Infrastructure (Nasdaq:STRL) Stock Analysis risk disclosure | thesis.R,decision_inputs.bear |
| reg_tariff_export#2 | + | 2026-08-04 | 儘管面臨關稅逆風，STRL 2026 Q2（2026-08-04 發布）營收年增90%至11.68億美元、調整後EPS年增116%至5.80美元，均優於市場預期（EPS優於預期16.2%、營收優於預期21.5%）；已簽約在手訂單年增116%至43億美元，合併在手訂單達56億美元；E-Infrastructure（資料中心/半導體相關）營收年增192%，利潤率維持24%；公司上修2026全年營收指引至40-41.5億美元。 | Sterling Infrastructure Q2 2026 earnings release/call coverage — Investing.com "Sterling Infrastructure Q2 2026 slides: 90% revenue jump, shares fall"; The Motley Fool Q2 2026 earnings call transcript (2026-08-10) | thesis.H,moat_trend,decision_inputs.bear |
| geo_supply_chain#0 | - | 2026-03-02 | Sterling 的 E-Infrastructure（資料中心）主力專案地理上集中於德州、亞利桑那州與卡羅來納州三個市場,尚未見到全國性分散的揭露,屬國內專案地理集中風險（非離岸地緣風險）。 | FinancialContent/Finterra, 'The Infrastructure Renaissance: A Deep Dive into Sterling Infrastructure (STRL)' | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | + | 2026-03-02 | 同篇分析指出「friend-shoring」（供應鏈回流美國本土/友岸國家）趨勢對 Sterling 構成長期結構性需求利多,因其資料中心/半導體廠營造工程全數為美國境內施作,不涉及海外製造據點曝險。 | FinancialContent/Finterra, 'The Infrastructure Renaissance: A Deep Dive into Sterling Infrastructure (STRL)' | thesis.H,moat_trend |
| geo_supply_chain#2 | 0 | 2026-08-01 | Sterling 資料中心與晶圓廠營造客戶群為少數超大規模業者（hyperscaler）與半導體廠商,單一專案規模持續擴大,部分園區型專案簽約可長達 12 年。 | Yahoo Finance, 'Sterling Infrastructure (STRL) Is Recasting Its Business Around Data Centers And Chip Plants' | thesis.R |
| end_markets#0 | + | 2026-08-10 | 2026年第2季 E-Infrastructure Solutions 營收年增192%達9.05億美元；公司將2026全年 E-Infrastructure 營收成長指引上修至逾100%（含 CEC 與 Stone Ridge 併購貢獻）；已簽約在手訂單逾90%為資料中心、大型製造與半導體等task-critical工程；管理層重申資料中心需求可望持續。 | PRNewswire, 'Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance'; The Globe and Mail, "Is Sterling's 192% E-Infrastructure Growth Just Getting Started Now?" | thesis.H,growth,valuation |
| end_markets#1 | 0 | 2026-08-10 | 分析師預估 E-Infrastructure 2027年成長率放緩至約25%（較2026年108.6%大幅趨緩），但公司合併在手訂單較去年成長131%達52億美元，並提及「未來階段」可見度上看約65億美元，資料中心專案規模擴大且部分延長至5-8年以上。 | Yahoo Finance, "STRL's Backlog Visibility: What It Means for 2026-2027 Growth" | growth,valuation |
| end_markets#2 | 0 | 2026-08-10 | 2026年第2季 Transportation Solutions 營收年減20%，主因公司主動將資源移轉至毛利率較高的 E-Infrastructure 業務；管理層預期2026全年營收下滑7%至10%；惟該季調整後營業利益率逆勢擴張逾500個基點至19.5%，顯示營收下滑主因是資源配置策略而非單純終端市場需求疲弱。 | Investing.com, 'Earnings call transcript: Sterling Infrastructure beats Q2 2026 estimates, shares fall' | thesis.H,growth |
| end_markets#3 | - | 2026-08-10 | Transportation Solutions季底在手訂單9.69億美元，年增35%，主要反映未簽約backlog轉為已簽約backlog；惟公司合併在手訂單較2025年底下滑11%。 | Investing.com, 'Earnings call transcript: Sterling Infrastructure beats Q2 2026 estimates, shares fall' | thesis.R,growth |
| end_markets#4 | - | 2026-08-10 | 受購屋可負擔性壓力導致住宅需求走弱影響，Building Solutions 2026上半年營業利益由去年同期2220萬美元降至1470萬美元；公司在手訂單維持30.1億美元的紀錄水準，可見度延伸至2027年。 | PRNewswire / strlco.com, 'Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance' | thesis.R,decision_inputs.bear,growth |
| substitute_technology#0 | - | 2026-01 | 全球模組化／預製建築市場預估 2026 年達 1834 億美元、2027 年達 1939 億美元；在資料中心等高成長領域，模組化施工可將專案工期縮短 30%–50%，將部分現場人力工作轉移至工廠端預製。 | Future Market Insights, "Modular & Prefabricated Construction Market" report (亦見 epicflow.com "Key Technology Trends in the Construction Industry in 2026") | moat_trend,thesis.R |
| channel_business_model_shift#0 | + | 2026-08 | STRL 的 Transportation Solutions 分部正從量驅動的低價競標模式，轉為紀律性選案／組合優化，聚焦 design-build、機場、鐵路與另類交付（alternative-delivery）等高技術含量、較高毛利專案；管理層並將德州低價競標高速公路業務的收斂列為毛利改善的結構性驅動因素之一。 | Nasdaq.com, "Sterling's Transportation Margins Rebound: A Structural Shift?" | thesis.H,moat_trend,decision_inputs.bear |
| channel_business_model_shift#1 | + | 2026-Q1 | STRL 以 5.616 億美元收購 CEC Facilities Group，取得專業電氣與機電服務能量，將營運範圍從單純的場地整備（site development）延伸至資料中心、半導體廠、先進製造廠等專案生命週期的更多階段，不再於場地整備完成後即把工作轉交給其他專業承包商；截至 2026 年第一季末，任務關鍵型（mission-critical）專案已占 E-Infrastructure 在手訂單逾 90%。 | TradingView/Zacks, "Can Sterling's Vertical Integration Push Margins Even Higher?" | moat_trend,thesis.H |
| channel_business_model_shift#2 | 0 | 2026-01 | 針對「超大規模業者（hyperscaler）是否正繞過總承包商、直接與專業分包商簽約」的查證，找到的產業資料顯示超大規模資料中心營建仍普遍採傳統多承包商協調模式（含 OFCI／業主自供設備由承包商安裝），未查到 hyperscaler 直接繞過總承包商模式已structurally 成形的證據。 | Giatec Scientific, "Data Center Construction Guide for GCs"；StruxHub, "Hyperscale Data Center Construction Management" | thesis.R |
| capital_markets_pricing#0 | + | 2026-08-03 | STRL 於 2026-08-03 公布 Q2 2026 財報並上修全年 guidance：營收由先前區間上修至 $4.0-4.15B、調整後 EPS 上修至 $19.70-$20.30，高於當時分析師共識 $19.10；營收年增 90%（含 CEC／Stone Ridge 併購貢獻＋約 50% 有機成長），簽約在手訂單年增 116% 至 $4.3B、合併在手訂單年增 150% 至 $5.6B | The Globe and Mail, "Sterling Infrastructure Reports Record Q2 Results, Raises Guidance"; StockTitan 8-K filing summary | thesis.H,valuation,triggers |
| capital_markets_pricing#1 | - | 2026-08-03 | 儘管財報三重優於預期（營收/EPS/guidance 皆上修），STRL 股價於財報公布後仍下跌約 10%，原因是 E-Infrastructure 分部調整後營益率因低毛利電氣工程業務（CEC）佔比上升而下滑約 420 個基點（該分部整體毛利率仍優於 Transportation Solutions，但混合效應稀釋） | ts2.tech, "Sterling Infrastructure (NASDAQ:STRL) Shares Drop 10% After Earnings Report as Electrical Segment Alters Margins" | thesis.R,moat_trend,decision_inputs.bear |
| capital_markets_pricing#2 | - | 2026-08-21 | KeyCorp（KeyBanc）於 2026-08-05 將 STRL 目標價由 $922 下修至 $754（原因與財報後市場對利潤率組合的疑慮同期），同月稍後 DA Davidson 於 2026-08-21 首次覆蓋給予 Buy 評等、目標價 $700 | TipRanks/TheFly, "sterling infrastructure price target raised to 460 from 355 at da davidson" 頁面內含之同批目標價異動記錄（KeyCorp $922→$754 8/5/2026；DA Davidson 首評 $700 8/21/2026） | valuation,decision_inputs.bear |
| capital_markets_pricing#3 | + | 2026-09-04 | 截至查詢當下，8 位分析師（S&P Global 彙整）給予 STRL「Strong Buy」共識評等、平均目標價 $876；另一彙整（15 位分析師）平均目標價 $971.73；Simply Wall St 綜合公允價值估計約 $941.17（較前次 $938.17 微幅上修，引用 KeyBanc 目標價上修至 $922 與 Oppenheimer 首評 $950 為上修理由）——三組目標價估計皆遠高於 `numbers.price_at_dd` $486.49（2026-09-04 收盤），顯示賣方目標價尚未完全反映近月股價修正 | stockanalysis.com STRL forecast page（S&P Global 8-analyst 共識）；WallStreetZen STRL forecast page（15-analyst 平均）；Simply Wall St STRL future page（綜合公允價值） | valuation,thesis.H |
| capital_markets_pricing#4 | - | 2026-08-21 | STRL 股價自 2026-07-22 約 $719 高點下跌，至 2026-08-21 收盤 $516.81（30 日跌幅約 28%），主因為估值與利潤率組合疑慮而非需求或營運面惡化；市場對財報後訂單／利潤率能見度提出更嚴格要求 | Tickeron, "Sterling Infrastructure (STRL) Declines -28% in 30 Days as Valuation Concerns Take Hold"; ts2.tech, "Sterling Infrastructure (NASDAQ:STRL) Faces Tougher Earnings Expectations Following 9.7% Weekly Drop" | thesis.R,decision_inputs.bear,valuation |
| major_events#0 | + | 2025-11-01 | Sterling Infrastructure completed acquisition of CEC Facilities Group (Irving, TX-based specialty electrical and mechanical contractor); upfront purchase price at closing totaled $505 million ($450M cash + $55M Sterling common stock), plus an earn-out contingent on operating income targets through Dec 31, 2029. | Sterling Announces Agreement to Acquire CEC Facilities Group, https://www.strlco.com/news/sterling-announces-agreement-to-acquire-cec-facilities-group/ | moat_trend,thesis.H,valuation |
| major_events#1 | + | 2026-01-01 | Sterling closed acquisition of Stone Ridge Contracting, LLC (Pocatello, ID-based site development contractor), joining Sterling's E-Infrastructure Solutions segment; Stone Ridge projected to generate $180M-$200M revenue for full year 2026 with mid-teens EBITDA margins, and has an earn-out contingent on EBITDA targets through Dec 31, 2031. | Sterling Announces Acquisition of Stone Ridge Contracting, LLC., https://www.strlco.com/news/sterling-announces-acquisition-of-stone-ridge-contracting-llc/ | moat_trend,thesis.H,valuation,decision_inputs.bear |
| major_events#2 | 0 | 2026-09-05 | No securities fraud class action, shareholder litigation, or investor lawsuit specific to Sterling Infrastructure (STRL) was found; search results for 'Sterling' litigation returned only unrelated cases against Sterling Bancorp (NASDAQ: SBT), a different company. | WebSearch aggregate (no STRL-specific litigation source found) | thesis.R,decision_inputs.bear |
| major_events#3 | + | 2026-01-01 | Sterling Infrastructure's 2026 Sustainability Report (covering FY2025 performance) reported a Total Recordable Incident Rate of 0.46 and zero fatalities, described as part of a strengthening safety-first culture; no warning letters, recalls, or safety incidents involving STRL were found. | Sterling Infrastructure (STRL) shows 2025 growth, safer jobsites and stronger ESG focus, https://www.stocktitan.net/sec-filings/STRL/8-k-sterling-infrastructure-inc-reports-material-event-8ab9700aef5a.html | moat_trend,thesis.R |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "STRL Sterling Infrastructure acquisition merger 2025 2026",
   "Sterling Infrastructure STRL acquisition merger 2025 2026"
  ],
  "findings": [
   {
    "claim": "Sterling Infrastructure completed acquisition of CEC Facilities Group; upfront purchase price at closing $505 million ($450M cash + $55M Sterling common stock), plus earn-out contingent on operating income targets through Dec 31, 2029.",
    "source": "Sterling Announces Agreement to Acquire CEC Facilities Group, https://www.strlco.com/news/sterling-announces-agreement-to-acquire-cec-facilities-group/",
    "as_of": "2025-11-01",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H",
     "valuation"
    ]
   },
   {
    "claim": "Sterling closed acquisition of Stone Ridge Contracting, LLC, joining the E-Infrastructure Solutions segment; projected $180M-$200M FY2026 revenue with mid-teens EBITDA margins, earn-out contingent on EBITDA targets through Dec 31, 2031.",
    "source": "Sterling Announces Acquisition of Stone Ridge Contracting, LLC., https://www.strlco.com/news/sterling-announces-acquisition-of-stone-ridge-contracting-llc/",
    "as_of": "2026-01-01",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H",
     "valuation"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL class action lawsuit securities fraud",
   "\"Sterling Infrastructure\" investor lawsuit OR \"securities litigation\" OR \"shareholder suit\""
  ],
  "findings": [],
  "note": "Search results returned only unrelated litigation involving Sterling Bancorp (NASDAQ: SBT), a distinct, unrelated company; no STRL-specific securities fraud or shareholder class action found."
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL clinical trial FDA approval 2025 2026",
   "Sterling Infrastructure STRL FDA"
  ],
  "findings": [],
  "note": "非藥品/器材業務（STRL 為重型土木／電力基礎設施承包商），已查證無相關監管動作；此軸對本標的不適用（no FDA/clinical exposure in core business lines）。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL warning letter recall safety incident 2025 2026",
   "Sterling Infrastructure STRL product launch recall warning letter"
  ],
  "findings": [
   {
    "claim": "Sterling Infrastructure's FY2025 Sustainability Report reported Total Recordable Incident Rate of 0.46 and zero fatalities; no product recalls or regulatory warning letters found for STRL in the search window.",
    "source": "Sterling Infrastructure (STRL) shows 2025 growth, safer jobsites and stronger ESG focus, https://www.stocktitan.net/sec-filings/STRL/8-k-sterling-infrastructure-inc-reports-material-event-8ab9700aef5a.html",
    "as_of": "2026-01-01",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   }
  ],
  "note": "No recall/warning-letter events found; the one finding surfaced is a positive safety-record data point, not a recall/warning."
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL SEC investigation restatement",
   "Sterling Infrastructure STRL SEC investigation restatement 2025 2026"
  ],
  "findings": [],
  "note": "No SEC investigation or financial restatement found for STRL; search returned only routine SEC filings (10-K, DEF 14A, 8-K credit facility amendment) with no indication of investigation or restatement."
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_STRL_20260505.html",
 "date": "20260505",
 "schema": "v12.3",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 529.49,
 "revlog": {
  "status": "unavailable"
 },
 "prior_meta": {
  "ticker": "STRL",
  "name": "Sterling Infrastructure",
  "date": "2026-05-05",
  "schema": "v12.3",
  "price_at_dd": 529.49,
  "inception_dd": "DD_STRL_20260505.html",
  "inception_date": "2026-05-05",
  "next_yoy_review": "2027-05-05",
  "signal": "B",
  "trap": "🟡",
  "trap_label": "觀察期",
  "moat": "B",
  "moat_score": 6.9,
  "moat_execution": 7.5,
  "moat_pricing_power": 6.0,
  "val": "🟡",
  "ma": "✅",
  "regime": "正常",
  "fpe_fy2": 27.2,
  "pct_5y": 68,
  "peg_fy2": 0.68,
  "upside_short_pct": -6,
  "upside_mid_pct": 10,
  "upside_5y_pct": 55,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "growth_durability": 8,
  "quality_score": 7,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "B（衛星候選 / 觀望偏進場）",
  "oneliner": "Q1 26 三軸強化（Rev+92%/Adj EPS+120%/E-Infra+174%）+FY26 guide+36%／估值🟡 PEG 0.86+MA✅但 BB+19%/4w+57% 動能透支／B 級 moat 6.9（exec 7.5+pricing 6.0）+Cutillo $92M 減持 trap🟡／等回測 $410/$336 進場"
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
    "text": "AI Capex 結構性 super-cycle 持續至 FY28+：Hyperscaler combined capex YoY 維持 25%+ 至 FY28，STRL E-Infra 維持 50%+ YoY",
    "columns": {
     "2Y 驗證點": "FY27 E-Infra Rev > $4.5B（YoY +50%）",
     "5Y 驗證點": "FY30 STRL Total Rev > $8B，E-Infra > $6B",
     "10Y 驗證點": "FY35 AI capex 進入 maintenance 模式但 STRL 已從中累積 $50B+ 累計合約",
     "sourced floor（具體數字 + 來源）": "FY26 Hyperscaler combined capex ≥ $690B（Dell'Oro 2026 base case，CreditSights confirm）；FY27 ≥ $700B（sell-side 共識）；E-Infra Rev YoY 2Y 連 2 季 ≥ 60%（TTM 基）",
     "漂移觸發條件（QC-34 / QC-35）": "連 2 季 TTM E-Infra YoY"
    }
   },
   {
    "id": "H2",
    "text": "CEC turnkey 模式擴大客戶 ARPU + 鎖定：每客戶 Rev 從 $50M / 年擴張至 $150M+（site + electrical 雙包）",
    "columns": {
     "2Y 驗證點": "FY27 CEC 整合營收 > $700M，turnkey 校區數 > 10",
     "5Y 驗證點": "FY30 turnkey 模式涵蓋 80% E-Infra 合約",
     "10Y 驗證點": "FY35 STRL turnkey 為行業 default，類似 GE 全包能源 EPC 地位",
     "sourced floor（具體數字 + 來源）": "CEC 收購 $505M（PRNewswire 2025-09-01）；Q1 26 CEC 貢獻 $156M Rev / 兩個 turnkey 校區交叉銷售（Sterling Q1 26 release）；FY26-27 預期 130-138M / 全年 600M imply",
     "漂移觸發條件（QC-34 / QC-35）": "turnkey 校區 6Q 未達 6 個或 CEC organic + cross-sell Rev 連 2 季"
    }
   },
   {
    "id": "H3",
    "text": "單位經濟拐點不可逆：E-Infra Adj OM 維持 22%+，整體 OM 從 16.6%（FY25）擴張至 18-20%",
    "columns": {
     "2Y 驗證點": "FY27 E-Infra Adj OM 維持 21%+",
     "5Y 驗證點": "FY30 整體 Adj OM 達 19-20%",
     "10Y 驗證點": "FY35 ROIC 持續 > 25%（cycle through）",
     "sourced floor（具體數字 + 來源）": "Q1 26 E-Infra Adj OM 22.4%（Sterling Q1 26 release）；整體 Adj OM 16.6% FY25 → 22% mid FY26 guide；ROIC 22% FY25 vs 14% FY23 趨勢",
     "漂移觸發條件（QC-34 / QC-35）": "連 2 季 E-Infra Adj OM"
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
    "text": "Hyperscaler capex digestion 週期",
    "columns": {
     "對應": "H1",
     "時間尺度": "🔥 中期（4-6 季）",
     "監測指標": "AMZN/MSFT/META/GOOGL 季度 capex guidance、AI workload utilization",
     "警戒閾值": "combined capex YoY"
    }
   },
   {
    "id": "R2",
    "text": "客戶集中度 + 任一 Hyperscaler 退出",
    "columns": {
     "對應": "H1 + H2",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "個別客戶 Rev 占比、新客戶簽約速度、bidding pipeline",
     "警戒閾值": "top 1 客戶 Rev 占比 single-quarter > 35% 且 backlog 集中"
    }
   },
   {
    "id": "R3",
    "text": "動能反身性 + estimation reset",
    "columns": {
     "對應": "估值 + 短期",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "NTM Fwd PE、4w 漂移、analyst PT 上修速度",
     "警戒閾值": "NTM Fwd PE > 50x 且 PEG > 2.0；或 4w +30%+ 動能透支"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_STRL_20260505.html",
  "date": "20260505",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_STRL_20260505.html",
  "date": "20260505",
  "days_from_365d_mark": 242
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "STRL",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-05-05",
  "freshness": "aging",
  "source": "docs/dd/DD_STRL_20260505.html"
 },
 "decision_history": [
  {
   "date": "2026-05-05",
   "verdict": null,
   "role": null,
   "price_at_decision": 529.49,
   "fundamental_grade": "B",
   "to_date_pct": -42.41,
   "days": 118,
   "source_report": "docs/dd/DD_STRL_20260505.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/STRL.md\n[internal-note] 2026-05-17  v12.3 Cold Review Batch 17 — SPOT / STM / STRL / STX / TER\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_BATCH17_20260517.md\n[internal-note] 2026-05-17  v12.3 Cold Review — STRL (DD_STRL_20260505.html)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_STRL_20260517.md\n[dca] 2026-05-14  STRL Deep Conviction|2026-05-14\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_STRL_20260514.md\n[dd] 2026-05-05  DD_STRL_20260505 — Sterling Infrastructure 深度研究 v12.3\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_STRL_20260505.md"
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

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/STRL/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "CFO announces an increase to full-year 2025 guidance ranges.",
      "quote": "We are increasing our guidance ranges to:",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "New full-year diluted EPS guidance range given.",
      "quote": "diluted EPS of $8.73 to $8.87",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "New full-year EBITDA guidance range given.",
      "quote": "EBITDA of $448 million to $453 million;",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states consolidated gross profit margin expanded year over year in Q3.",
      "quote": "Our gross profit margins expanded 280 basis",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO gives full-year E-Infrastructure segment adjusted operating margin outlook including CEC.",
      "quote": "margins for E-Infrastructure should approximate 25%",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO gives full-year Transportation Solutions adjusted operating margin outlook versus prior year.",
      "quote": "margins in the 13.5% to 14% range compared to 9.6% in 2024.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO cites a prior tuck-in acquisition (dry conduit business) as an example of margin improvement from combining with site development.",
      "quote": "margins improve 40% just by combining that with the site",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states the company will pass on megaprojects if pricing or margins are not right.",
      "quote": "I don't want anybody to be surprised if we pass on one of",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses year-to-date share repurchase amount and average price paid.",
      "quote": "primarily driven by share repurchases of $48.5 million",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses remaining availability under the existing share repurchase authorization.",
      "quote": "existing repurchase authorization is $80.9 million.",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO characterizes the balance sheet position as strong.",
      "quote": "We are in great shape from a balance sheet perspective.",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the CEC acquisition closed during the quarter.",
      "quote": "We are pleased to have closed the CEC acquisition during",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO states permitting timelines have lengthened versus pre-COVID.",
      "quote": "the permitting process certainly is longer today",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO quantifies how much longer permits now take versus historically.",
      "quote": "permit now takes 3 months. Maybe 5 in certain markets.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO attributes Building Solutions demand weakness to homebuyer affordability challenges.",
      "quote": "potential buyers struggle with affordability challenges.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO reports a revenue decline in the legacy residential business.",
      "quote": "our legacy residential business declined 17%",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO notes the current federal transportation funding bill (IIJA) is scheduled to end in September 2026.",
      "quote": "the existing bill ends at the end of September of 2026.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO describes 'The Sterling Way' as the company's stated commitment covering people, environment, investors and communities.",
      "quote": "The Sterling Way, which is our commitment to take care of",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO expresses confidence in leveraging the combined site development and electrical services capability heading into 2026.",
      "quote": "a high degree of confidence in our ability to leverage the",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states customers are discussing multiyear capital deployment plans for data center site development.",
      "quote": "multiyear capital deployment plans and our focus",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "CEO describes hyperscaler and chip-plant customers as forward-looking in anticipating capacity needs.",
      "quote": "hyperscalers, and even these big chip plants have been",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "competition",
      "claim": "CEO attributes customer value to Sterling's project management and on-schedule delivery capability.",
      "quote": "superior project management and ability to finish jobs",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes e-commerce distribution center projects as increasingly resembling data center projects in infrastructure complexity.",
      "quote": "an e-commerce distribution center is starting to look a",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "Company initiated FY2026 revenue guidance range.",
      "quote": "Revenue of $3.05 billion to $3.2 billion",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "Company initiated FY2026 EBITDA guidance range.",
      "quote": "EBITDA of $587 million to $620 million.",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided E-Infrastructure segment revenue growth for 2026.",
      "quote": "E-Infrastructure revenue growth of 40% or higher.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided Transportation Solutions revenue growth for 2026.",
      "quote": "revenue growth in the low to mid-single digits in 2026",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided Building Solutions revenue decline for 2026.",
      "quote": "revenue will decline in the high single to low double digits",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "margin",
      "claim": "CEO guided E-Infrastructure adjusted operating margin range for 2026.",
      "quote": "expected to be in the 23% to 24% range.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "margin",
      "claim": "CEO stated FY2025 full-year gross margin and adjusted EBITDA margin levels achieved.",
      "quote": "margins reached 23% and adjusted EBITDA margins exceeded 20%",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "competition",
      "claim": "When asked how Sterling compares to peers on AI adoption, CEO said he does not know where competitors stand.",
      "quote": "I don't know where our peers are.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "product",
      "claim": "CEO described the size of CEC's new modular electrical build facility.",
      "quote": "the new facility is over 300,000 square feet.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "risk",
      "claim": "CEO cited home affordability challenges as impacting Building Solutions demand.",
      "quote": "potential buyers struggle with affordability challenges.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "risk",
      "claim": "CEO said residential market conditions will remain difficult in the first half of 2026.",
      "quote": "I think it's going to be tough,",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO described \"The Sterling Way\" as the company's stated commitment to people, environment, investors and communities.",
      "quote": "The Sterling Way, which is our commitment to take care of",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO stated remaining availability under the existing share repurchase authorization.",
      "quote": "repurchase authorization is $374 million.",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO said capital allocation focus is not on adding a new (\"fourth leg\") business line.",
      "quote": "our focus won't be necessarily on a fourth leg.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "customer",
      "claim": "CEO said the majority of the $1B+ future phase pipeline is tied to major hyperscaler customers.",
      "quote": "the lion's share of that are with the big name hyperscalers",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "customer",
      "claim": "CEO said future phase work is tied to existing customers, with occasional new customer additions.",
      "quote": "It's tied to existing customers, but we're always getting a",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 revenue guidance raised to $3.7-3.8B, up 20% at the midpoint from prior guidance.",
      "quote": "Revenue of $3.7 billion to $3.8 billion, which at the midpoint is a 20% increase over previous guidance",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 adjusted diluted EPS guidance raised to $18.40-$19.05, up 36% at the midpoint from prior guidance.",
      "quote": "Adjusted diluted EPS of $18.40 to $19.05, which at the midpoint is a 36% increase from previous guidance",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "Full-year 2026 E-Infrastructure segment revenue is guided to grow 80% or higher including CEC.",
      "quote": "For the full year 2026, we expect to deliver E-Infrastructure revenue growth of 80% or higher, including the full year contribution of CEC.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "Legacy (ex-CEC) E-Infrastructure business is guided to grow approaching 60% or higher in 2026.",
      "quote": "We anticipate that the legacy business will grow at rates approaching 60% or higher as several of our larger projects accelerate.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "E-Infrastructure adjusted operating profit margin is guided to the mid-20% range for 2026.",
      "quote": "Adjusted operating profit margins for E-Infrastructure are expected to be in the mid-20% range.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Management expects CEC margins to expand 300-500bp over the next 12-18 months as low-margin end markets are exited.",
      "quote": "we're still extremely bullish that we're going to see 300 to 500 basis points of margin in really 12 to 18 months",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Q1 2026 adjusted EBITDA margin hit a first-quarter record of 20%, up more than 150bps YoY.",
      "quote": "Adjusted EBITDA more than doubled with margins expanding over 150 basis points year-over-year to reach a new first quarter record of 20%.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Management states margin expansion is not coming from raising prices with customers.",
      "quote": "Everybody keeps asking us if we're getting more price. The answer is no, we're not getting more price.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes Sterling's competitive positioning in winning the semiconductor fab campus bid as overwhelming versus other bidders.",
      "quote": "There was no one else in the room that was going to have a chance at this.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "competition",
      "claim": "Management expects to become the preferred site-development partner for future U.S. semiconductor fab projects, similar to its position in data centers.",
      "quote": "we feel very confident that just like in data centers, we will be the supplier of choice for every chip plant that comes out in the future",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Q1 2026 share repurchases totaled $12 million at an average price of $305.14; $362 million remains under the buyback authorization.",
      "quote": "share repurchases of $12 million at an average price of $305.14 per share. Remaining availability under the existing repurchase authorization is $362 million.",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Sterling ended Q1 2026 in a net cash position of $224 million ($512M cash vs $287M debt).",
      "quote": "We ended the quarter with $512 million of cash and debt of $287 million for a cash net of debt balance of $224 million.",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Management sees a better-quality M&A pipeline now than a year ago and cites balance sheet strength to pursue deals.",
      "quote": "We are seeing more high-quality acquisition targets in the market today than a year ago. Our significant balance sheet firepower positions us to take advantage of these opportunities.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "Sterling signed a lease to triple its modular construction build capacity.",
      "quote": "We just locked down a lease to triple the size of our modular build capabilities.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "An internal AI deployment aimed at project managers yielded roughly a 15% capacity gain.",
      "quote": "The AI project we did first was focused on project managers. We picked up about 15% capacity in project managers.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "Management emphasizes a risk-averse project selection philosophy as a driver of margin stability.",
      "quote": "We won't take on high-risk jobs that are going to get us in trouble.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says the company is turning down customer requests to enter new markets faster than current capacity allows.",
      "quote": "Right now, our biggest challenge is they would like to have us in 2 or 3 or 4 new markets tomorrow. We've had to say no to some of those.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "customer",
      "claim": "Hyperscaler customers are urgently pushing Sterling to expand into new geographies faster than before, citing planned capital spending.",
      "quote": "They're more than pulling now. They're kind of screaming to get into these markets faster with what they see coming in capital spending they're going to do.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "commitment",
      "claim": "Mission-critical projects (data centers, large manufacturing, semiconductor) made up over 90% of E-Infrastructure signed backlog at quarter-end.",
      "quote": "Mission-critical work, including data centers, large manufacturing projects and semiconductor represented over 90% of E-Infrastructure signed backlog at the end of the quarter.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "commitment",
      "claim": "Signed backlog reached $3.8 billion (+78% YoY) and combined backlog reached $5.2 billion (+131% YoY).",
      "quote": "Signed backlog at the end of the quarter totaled $3.8 billion, a 78% year-over-year increase and combined backlog grew 131% to reach $5.2 billion.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Analyst asked whether a new (\"fourth leg\") business line is something Sterling should be considering as part of its capital allocation, given active buybacks and M&A interest.",
      "response_pattern": "CEO says focus 'won't be necessarily on a fourth leg' but then states 'if the right fourth leg came along, we wouldn't aggressively go after it' — internally inconsistent phrasing (context suggests he meant the opposite), leaving stance on new business-line M&A ambiguous.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "question": "Given the larger Q1 order intake, how should we think about legacy E-Infrastructure year-over-year growth rates over the remaining 3 quarters to reach the ~60% full-year target?",
      "response_pattern": "CEO declined to give a quarter-by-quarter breakdown, citing timing variability in project starts and repeating 'I just don't -- I don't have that.'",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "question": "How much do you expect Texas to account for as a percentage of revenue in the site development business (ex-CEC), and where was it last year?",
      "response_pattern": "CEO declined to give a percentage, saying 'it's really hard to say' and 'I'll only be wrong if I try to give you an answer,' pivoting instead to qualitative commentary about other regions also growing fast.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    }
  ]
}

```

---

## judgment.json 全文

```json
{
  "meta": {
    "ticker": "STRL",
    "date": "2026-09-05",
    "schema": "v15.0",
    "company_name": "Sterling Infrastructure, Inc."
  },
  "oneliner": "AI 資料中心與晶圓廠的場地整備＋電氣承包商：Q2 營收 +90%、簽約在手訂單 $4.33B（+116%）、淨現金；股價自高點 −51% 後前瞻本益比 24.3x／PEG 1.45 回到合理；護城河 B 級靠執行與稀缺產能，定價權有限；賭的是超大規模業者 capex 不在 2027 年消化——進場但只當衛星。",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": "循環/商品（capex 建設子型：AI 資料中心與晶圓廠 capex 週期；循環鏡頭規則檔不在本輪證據包內，未換尺，只以情境樹 Bear 機率與倉位上限反映）",
    "confidence": "中",
    "fingerprint": "毛利 23.8%／營業利益率 18.1%／FCF 率 14.0%（TTM 至 2026-06-30）、SBC 僅營收 0.69%、資本支出約營收 3.5%、淨現金——資本輕、客戶預付款支應營運資金的專案型承包商，盈餘品質像品質複利，但需求來源是單一 capex 週期"
  },
  "thesis": {
    "headline": "在 AI 基礎建設 capex 週期裡，Sterling 是少數能同時做場地整備與電氣、被超大規模業者拉著進新市場的承包商；只要 2027 年 capex 不進入消化期，在手訂單就能把 EPS 從 $20 推到 $34 以上，現價 24.3x 是合理價、不是便宜價。",
    "holding_period": {
      "horizon": "中期 2–5 年（衛星）",
      "driver": "在手訂單轉化速度、E-Infrastructure 調整後營業利益率能否回到 25%、超大規模業者 2027 年 capex 指引",
      "signal_vs_noise": "持有期 >2 年，季度財報的單季利潤率波動（CEC 混合效應）是噪音；簽約在手訂單年增方向與超大規模業者 capex 指引方向是訊號；股價 30 天 −28% 本身不是訊號"
    },
    "H": [
      {
        "id": "H1",
        "text": "任務關鍵型需求（資料中心／半導體／大型製造）撐住 E-Infrastructure 至少到 FY2028：園區型專案 5–12 年續階，簽約在手訂單維持在 FY26 營收一倍以上",
        "2y": "FY2027 E-Infrastructure 營收年增 ≥20%（FY26 指引該分部 >100% 之後的第二年）；FY27 年底簽約在手訂單 ≥$4.0B",
        "5y": "FY2030 E-Infrastructure 營收 ≥$5B；任務關鍵型專案仍占分部在手訂單 ≥80%",
        "10y": "至 FY2035 園區型客戶（含晶圓廠）仍有續階合約，E-Infrastructure 未出現任何一年營收 −30% 以上",
        "threshold": "簽約在手訂單（2026-06-30：$4.33B，+116%）與合併在手訂單（$5.62B，+150%）TTM 年增不轉負；E-Infrastructure TTM 營收年增 ≥15%",
        "source": "公司季度新聞稿（在手訂單、分部營收）；超大規模業者季度 capex 指引；Moody's／Goldman 之 capex 總量估計",
        "drift_rule": "E-Infrastructure TTM 營收年增連 2 季 <15% 或簽約在手訂單 TTM 年增連 2 季 <0% ＝削弱；連 3 季合併在手訂單年減 ≥10% ＝反轉"
      },
      {
        "id": "H2",
        "text": "CEC 電氣整合把單一客戶錢包份額做大，且分部利潤率 12–18 個月內回補：E-Infrastructure 調整後營業利益率從 Q2 的 23.3% 回到 25% 以上，合併調整後營業利益率站穩 21% 以上",
        "2y": "FY2027 E-Infrastructure 調整後營業利益率 ≥25%（管理層 FY26 指引為 mid-20%，來源：摘要）；合併調整後營業利益率 ≥21%（Q2 FY26：21.6%）",
        "5y": "FY2030 合併調整後營業利益率 ≥22%；CEC 第 3 年（FY2028）稅後營業利益 ≥$50M（＝$505M 收購價的 10%）",
        "10y": "穿越一輪 capex 消化期後 ROIC 仍 >15%",
        "threshold": "E-Infrastructure 調整後營業利益率季度值 ≥23%（不低於 Q2 FY26 的 23.3%）；管理層承諾的 300–500bp 回補在 FY27 Q4 前見到 ≥200bp",
        "source": "公司季度新聞稿分部表；法說逐字稿 CEC 利潤率 Q&A（來源：摘要）",
        "drift_rule": "E-Infrastructure 調整後營業利益率 TTM 連 2 季低於 22% ＝削弱；連 3 季低於 20% ＝反轉（混合效應之外的結構性稀釋）"
      },
      {
        "id": "H3",
        "text": "資本配置維持高報酬：回購只在內在價值之下執行、併購只買能與場地整備交叉銷售的專業承包商、淨現金不變成淨負債",
        "2y": "FY2027 年底仍為淨現金（Q1 FY26：淨現金 $224M，來源：摘要）；新併購總價不超過年度 FCF 的 1.5 倍",
        "5y": "FY2030 累計併購（含 CEC、Stone Ridge）已實現 ROIIC ≥10%；股數淨減少或持平",
        "10y": "無稀釋性增資；SBC 占營收維持 <2%",
        "threshold": "淨現金 ≥0；SBC／營收 <2%（Q2 FY26：0.69%）；回購均價低於本報告 Base 5 年目標價的一半（$340）以下才算紀律",
        "source": "10-Q 現金與債務；季度新聞稿回購金額與均價；併購新聞稿",
        "drift_rule": "淨負債／EBITDA 跨 2 個年度 >1.0x ＝削弱；跨 3 個年度 >2.0x 或任一次增資 ＝反轉"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "超大規模業者 capex 消化期：AI 支出愈來愈靠舉債與表外融資，Moody's 已點名信用品質受威脅；Oracle 為最弱信用（Baa2 負向）。一旦 2027 年 capex 指引年增轉負，新園區授標停滯、在手訂單見頂",
        "h_ref": "H1",
        "clock": "🔥",
        "threshold": "四大超大規模業者合併 capex 指引年增 <+10%（連 2 季）；或任一主要客戶宣布延後園區續階",
        "evidence_refs": [
          "supply_demand_durability#3",
          "customer_concentration_credit#5",
          "customer_concentration_credit#4"
        ]
      },
      {
        "id": "R2",
        "text": "CEC 電氣包稀釋利潤率且回補落空：Q2 E-Infrastructure 調整後營業利益率因電氣工程占比上升較去年同期下滑約 420bp，市場以財報後 −10%、30 天 −28% 回應，KeyBanc 目標價 $922→$754；若 300–500bp 回補在 FY27 未兌現，市場會把「混合效應」改讀成「結構性稀釋」",
        "h_ref": "H2",
        "clock": "⚡",
        "threshold": "E-Infrastructure 調整後營業利益率連 2 季 <22%；或合併調整後營業利益率連 2 季 <20%",
        "evidence_refs": [
          "capital_markets_pricing#1",
          "capital_markets_pricing#4",
          "capital_markets_pricing#2"
        ]
      },
      {
        "id": "R3",
        "text": "兩個非 AI 分部同步走弱：Transportation Q2 營收 −20%、合併在手訂單較 2025 年底 −11%、前四大客戶（州 DOT）集中度升至 58%，且 IIJA 於 2026-09 底到期（來源：摘要）；Building Solutions 上半年營業利益自 $22.2M 降至 $14.7M。若 E-Infrastructure 同時放緩，沒有第二支柱緩衝",
        "h_ref": "H1",
        "clock": "🐢",
        "threshold": "Transportation 調整後營業利益率隨營收一起下滑（連 2 季 <15%）＝「主動選案」說法證偽；Building 在手訂單自 $3.01B 年減 >10%",
        "evidence_refs": [
          "end_markets#3",
          "end_markets#4",
          "customer_concentration_credit#1"
        ]
      },
      {
        "id": "R4",
        "text": "原料成本與固定價合約：2026-04-06 起鋼鋁銅 232 關稅 50%（衍生品 25%），重型土木與混凝土承包商對瀝青、混凝土、鋼鐵價格高度暴露，固定價合約下成本上漲直接吃毛利",
        "h_ref": "H2",
        "clock": "🔥",
        "threshold": "合併毛利率 TTM 較 FY25 的 23% 下滑 >150bp 且同業（FIX／EME）同期未同步下滑",
        "evidence_refs": [
          "reg_tariff_export#0",
          "reg_tariff_export#1"
        ]
      }
    ],
    "single_thing": {
      "description": "任一前三大超大規模業者（Microsoft／Amazon／Alphabet／Meta 之一）在季度財報中把下一年度 capex 指引改為年減，或公開宣布延後已規劃園區",
      "why_fatal": "E-Infrastructure 已占營收約七成、分部在手訂單 92% 為任務關鍵型專案，且未來階段管線「絕大多數綁定大型超大規模業者」（來源：摘要）；一家帶頭削減，其餘會跟進，授標停滯會在 2–3 季內反映到簽約在手訂單，Bear 路徑（FY28 EPS $17.5）立即成為 Base",
      "if_happens": "不等在手訂單數字，衛星部位減至首倉三分之一；若第二家跟進削減，清倉",
      "how_monitor": "每季四大超大規模業者財報 capex 指引（1–2 月、4–5 月、7–8 月、10–11 月）；Moody's／CNBC 對 AI 融資結構的追蹤",
      "probability": "12–24 個月內約 25%（2026 年 capex 仍在加速、2027 年估計續增至約 $820B，但融資結構已轉向舉債，一次盈利失望即可能觸發）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "ID gap：AI 資料中心營建（證據包 canonical_id 為 gap，無可對帳的產業報告）。自判 Phase II 擴張：超大規模業者合併 capex 2026 約 $700B、2027 估 $820B（Moody's），仍在加速；Sterling 簽約在手訂單 +116%、客戶「喊著要我們更快進新市場」（來源：摘要）；但融資結構已轉向舉債與表外（Moody's 2026-07-24），是擴張期後段的典型訊號，非過熱頂部",
    "bargaining": {
      "up": "上游＝鋼鋁銅、瀝青、混凝土與專業工班；232 關稅 2026-04 起 50%；固定價合約下成本風險在承包商身上，但公司以選案紀律（不接高風險工作，來源：摘要）與客戶預付款結構部分轉嫁",
      "down": "下游＝少數超大規模業者與晶圓廠；E-Infrastructure 前四大客戶占分部營收 27%（FY25，自 FY23 的 40% 下降），無單一客戶 >10% 合併營收；客戶身分未揭露；Transportation 前四大（州 DOT）58% 且上升；議價權在客戶端，公司靠稀缺產能與準時完工換取選案權而非價格（管理層明言「沒有拿到更多價格」，來源：摘要）",
      "geo": "全部美國境內施工，無離岸曝險；專案集中德州、亞利桑那、卡羅來納三州（國內地理集中）；friend-shoring 與晶圓廠回流為結構性順風"
    },
    "profit_pool_dir": "資料中心營建利潤池自總承包商（Turner／DPR／Mortenson 等）流向自行施作的專業分包（電氣包占總造價 30–40%，Rosendin 等），場地整備＋電氣打包者拿到更多；Sterling 藉 CEC 由單一環節延伸到兩個環節，5 年環節占比為淨流入（sourced：E-Infrastructure 分部調整後營業利益率 23–25% 對比 PWR 6.1%／EME 9.6%）；本標的環節 5 年利潤池精確占比證據包未涵蓋，以分部利潤率對同業差距判無 ≥5pp 淨流出",
    "tam_table": [
      {
        "segment": "E-Infrastructure（場地整備＋電氣，FY26E 約七成營收）",
        "tam_now": "超大規模業者 capex 2026 約 $700B（Moody's）；其中土建與電氣營建占比證據包未涵蓋",
        "tam_5y": "2027 約 $820B（Moody's）；2025–2027 累計最高 $1.15T（Goldman）；2028 年後無 sourced 估計",
        "sam": "美國德州／亞利桑那／卡羅來納園區型資料中心、晶圓廠、大型製造的場地整備與電氣包",
        "penetration": "FY26E 分部營收約 $2.9B 對比年度 capex 總量 <1%；在其三州場地整備細分市場的份額證據包未涵蓋",
        "cagr": "分部 FY26 指引 >100%（含 CEC）；分析師估 2027 放緩至約 25%",
        "position": "總承包商之下、業主之上的專業承包環節；打包場地＋電氣後往上游延伸",
        "pool_shift": "自總承包商流向自行施作的專業分包；Sterling 為淨流入",
        "ceiling": "天花板＝capex 週期見頂與三州以外複製能力（產能受限，已拒絕客戶進 2–4 個新市場的要求，來源：摘要）；被替代路徑＝模組化／預製把現場人力移到工廠（Sterling 自身正三倍擴大模組廠，來源：摘要）"
      },
      {
        "segment": "Transportation Solutions（公路／機場／鐵路，FY26E 約 17% 營收）",
        "tam_now": "IIJA 聯邦公路資金至 2026-09 到期（來源：摘要）；規模數字證據包未涵蓋",
        "tam_5y": "取決於續法案；公司指引 FY26 分部營收 −7% 至 −10%",
        "sam": "德州等州 DOT 的設計施工、機場、鐵路等高技術含量專案",
        "penetration": "證據包未涵蓋",
        "cagr": "FY26 −7% 至 −10%（主動退出低價競標公路）；分部調整後營業利益率 Q2 19.5%（+500bp）",
        "position": "州 DOT 直接承包；前四大客戶 58%",
        "pool_shift": "公司主動把資源移往 E-Infrastructure，利潤率上升、營收下降",
        "ceiling": "天花板＝聯邦資金續法案；替代路徑無，屬政策驅動需求"
      },
      {
        "segment": "Building Solutions（住宅混凝土基礎與配管，FY26E 約 10% 營收）",
        "tam_now": "美國住宅新建；可負擔性壓力下需求走弱（來源：摘要）",
        "tam_5y": "FY26 指引分部營收高個位數至低雙位數下滑",
        "sam": "德州／亞利桑那建商",
        "penetration": "證據包未涵蓋",
        "cagr": "上半年營業利益 $22.2M→$14.7M",
        "position": "建商的專業分包",
        "pool_shift": "利潤池隨住宅週期收縮",
        "ceiling": "天花板＝利率與可負擔性；在手訂單 $3.01B 提供 2027 能見度"
      }
    ]
  },
  "moat": {
    "execution": 8,
    "pricing": 6,
    "combined": 7.0,
    "grade": "B",
    "score": 7.0,
    "trend": "↑",
    "trend_evidence": "執行面擴大：CEC（2025 Q3 收購，$505M）把服務範圍從場地整備延伸到電氣機電，任務關鍵型專案占分部在手訂單 92%（2026-06-30）；簽約在手訂單 +116% 至 $4.33B、E-Infrastructure 營收 +192%；前四大客戶集中度 FY23 40%→FY25 27%（FY25 10-K）；客戶主動要求進入新市場而公司產能受限（來源：摘要）；Q1 2026 標得首座晶圓廠園區並自稱「房間裡沒有別人有機會」（來源：摘要）。定價面持平：管理層明言沒有拿到更多價格、利潤率靠選案與混合（來源：摘要），Q2 分部利潤率因 CEC 混合 −420bp。前瞻 2–3 年：只要產能仍是瓶頸、園區續階綁既有承包商，份額走向為升；capex 消化期一到，執行面優勢仍在但被需求淹沒",
    "spread_table": [
      {
        "metric": "營業利益率（TTM 至 2026-06-30）",
        "self": 18.13,
        "peer": "FIX 16.45／EME 9.60／PWR 6.12／MTZ 5.14",
        "spread_pp": 1.7,
        "trend": "擴大（合併調整後營業利益率 Q1 19.2%→Q2 21.6%）",
        "note": "對最強直接同業 FIX 之差距 +1.7pp；對 EME +8.5pp"
      },
      {
        "metric": "毛利率（TTM）",
        "self": 23.81,
        "peer": "FIX 25.66／EME 19.43／PWR 15.46／MTZ 12.91",
        "spread_pp": -1.85,
        "trend": "持平（FY25 全年 23%，來源：摘要）",
        "note": "低於 FIX，高於其餘三家"
      },
      {
        "metric": "FCF 率（TTM）",
        "self": 14.02,
        "peer": "FIX 19.24／EME 6.30／PWR 7.27／MTZ 1.52",
        "spread_pp": -5.2,
        "trend": "收窄（Q2 單季 9.6%，模組廠資本支出上升）",
        "note": "對 FIX 為負差距；FCF 率門檻 15% 未達"
      },
      {
        "metric": "ROIC 對同業 spread",
        "self": 22.0,
        "peer": "同業 ROIC 證據包未涵蓋",
        "spread_pp": null,
        "trend": "自身擴大（FY23 14%→FY25 22%，前份報告引用）",
        "note": "閘一：合併分 7.0 未達 8，不觸發 spread 強制檢查"
      }
    ],
    "threats": [
      {
        "level": "🔴",
        "text": "需求端單一週期：AI capex 融資轉向舉債與表外（Moody's），Oracle 為最弱信用；消化期一到，執行護城河擋不住授標停滯",
        "p": "25%（12–24 個月）",
        "evidence_refs": [
          "supply_demand_durability#3",
          "customer_concentration_credit#5"
        ]
      },
      {
        "level": "🟡",
        "text": "CEC 電氣包屬競爭較多的專業分包（Rosendin 等自行施作電氣包占造價 30–40%），混合效應把分部利潤率壓低 420bp；若回補落空，打包溢價不存在",
        "p": "30%",
        "evidence_refs": [
          "capital_markets_pricing#1"
        ]
      },
      {
        "level": "🟡",
        "text": "模組化／預製施工把 30–50% 工期與部分現場人力移到工廠端，長期削弱以現場執行為核心的優勢；Sterling 以三倍擴大自有模組廠應對（來源：摘要），屬點對點威脅",
        "p": "20%（5 年）",
        "evidence_refs": [
          "substitute_technology#0"
        ]
      },
      {
        "level": "🟡",
        "text": "232 關稅（鋼鋁銅 50%）與原料價格在固定價合約下侵蝕毛利；公司無定價權可轉嫁（管理層自承未拿到更多價格）",
        "p": "35%（合併毛利率 TTM −150bp）",
        "evidence_refs": [
          "reg_tariff_export#0",
          "reg_tariff_export#1"
        ]
      },
      {
        "level": "🟡",
        "text": "大型多元同業（Quanta／EMCOR／Fluor／Kiewit／Turner）資本量級遠大於 Sterling，一旦決定自建場地整備能量可在一輪週期內追上；目前無單一顛覆性新進者",
        "p": "20%",
        "evidence_refs": [
          "competitive_share_entrants#2"
        ]
      }
    ],
    "competitors": [
      {
        "name": "Comfort Systems（FIX）",
        "rev_growth": "證據包未涵蓋",
        "gm": 25.66,
        "om": 16.45,
        "rd_intensity": "不適用",
        "fcf_margin": 19.24,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "機電（MEP）承包商，同樣吃資料中心電氣與機械包；利潤率與 FCF 率均高於 Sterling，是最強直接對照；YTD 股價表現亦優於 Sterling（2026-08-15 讀數）——同主題下市場給 FIX 更高信任"
      },
      {
        "name": "EMCOR（EME）",
        "rev_growth": "證據包未涵蓋",
        "gm": 19.43,
        "om": 9.6,
        "rd_intensity": "不適用",
        "fcf_margin": 6.3,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "大型電氣機電承包商，超大規模業者需求同樣強勁；規模遠大於 Sterling 但利潤率低一半，屬理性競爭者而非價格破壞者"
      },
      {
        "name": "Quanta（PWR）",
        "rev_growth": "證據包未涵蓋",
        "gm": 15.46,
        "om": 6.12,
        "rd_intensity": "不適用",
        "fcf_margin": 7.27,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "電網與電力基礎設施龍頭，在資料中心電力接入環節與 Sterling 上下游相鄰；利潤率結構完全不同"
      },
      {
        "name": "MasTec（MTZ）",
        "rev_growth": "證據包未涵蓋",
        "gm": 12.91,
        "om": 5.14,
        "rd_intensity": "不適用",
        "fcf_margin": 1.52,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "通訊與能源基礎設施承包商，低利潤率高槓桿，是「破壞性競爭」時最可能跟跌價格的玩家"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率 × 高周轉（以營建業尺度）：稅後營業利益率約 13.6%（18.1%×0.75），資本支出僅營收 3.5%，營運資金由客戶預付款支應（上半年營運現金流 $328M 高於淨利）；併購（CEC $505M）把商譽計入投入資本後周轉率下降，實際 ROIC FY25 22%（前份報告引用），投入資本周轉率精確值證據包未涵蓋",
      "checkpoints": [
        {
          "name": "需求基礎值",
          "light": "🟡",
          "evidence": "需要型（資料中心不蓋就沒有算力），使用者／決策者／付款者三角在超大規模業者內部完整；但急迫性 ≠ 持久性——需求由 AI 投資報酬預期驅動，Moody's 已指融資結構轉向舉債",
          "proxy": "簽約在手訂單 $4.33B（+116%）；園區續階 5–12 年（來源：公司新聞稿）"
        },
        {
          "name": "決策層級",
          "light": "🟢",
          "evidence": "客戶在「園區層」而非「單一工程」做選擇：續階工作綁定既有承包商（未來階段管線絕大多數為既有客戶，來源：摘要）；客戶要求 Sterling 進新市場而非另找承包商",
          "proxy": "未來階段管線 >$1B 綁既有客戶；無任何客戶改用第二承包商或內製的證據（customer_second_source 軸）"
        },
        {
          "name": "價值鏈分配",
          "light": "🟢",
          "evidence": "專業分包環節分到的利潤高於總承包：E-Infrastructure 分部調整後營業利益率 23.3% 對比 PWR 6.1%／EME 9.6%；CEC 使公司同時拿場地與電氣兩段",
          "proxy": "分部利潤率對同業差距 +7 至 +17pp"
        },
        {
          "name": "社會容忍度",
          "light": "🟢",
          "evidence": "營建承包不涉公共利益定價、無監管授權依賴；風險在反面——資料中心用電與用水的地方政治阻力會拉長許可（許可期已由歷史數週拉長到 3–5 個月，來源：摘要）",
          "proxy": "許可週期 3–5 個月（來源：摘要）"
        }
      ],
      "roiic": "約 59%（FY24→FY26E 兩年基礎：ΔNOPAT ≈ (840−250)×0.75 ≈ $440M ÷ ΔIC ≈ CEC $505M＋Stone Ridge＋資本支出淨額＋營運資金 ≈ $750M；含併購，非可持續）；有機口徑約 40%",
      "reinvest_rate": "FY26E 約 35%（資本支出 $140M − 折舊約 $70M ＋ 營運資金與小型併購 ≈ $220M）÷ NOPAT 約 $630M；FY25 含 CEC 為 >100%",
      "endo_ceiling": 14,
      "formula_note": "內生成長天花板＝有機 ROIIC 40% × 再投資率 35% ＝ 14%；客戶預付款使 CCC 為負，標準公式低估，但即使以 ROIIC 為上界，共識 FY26→FY28 EPS 複利 20.1% 仍高於 14%——缺口 6pp 歸因：CEC 利潤率回補 300–500bp（sourced，來源：摘要）與在手訂單已簽約的轉化（需求端預付，非公司再投資）；仍標「超出⚠」，Bear 機率下限 30%"
    }
  },
  "growth": {
    "runway_years": 7,
    "runway_post_y5": "🟡",
    "seven_questions": [
      "①結構性或週期反彈：主要是 capex 週期（AI 資料中心），疊加結構性的 friend-shoring 與晶圓廠回流；週期成分大於結構成分",
      "②資本投入多少：很少——資本支出約營收 3.5%，營運資金由客戶預付款支應，主要投入是併購（CEC $505M）",
      "③增量 ROIC 是否 >資金成本：是，有機 ROIIC 約 40%、含併購約 59%，遠高於 WACC 約 9–10%",
      "④成長變現金流或被下輪擴張吃掉：變現金——上半年營運現金流 $328M，FCF 率 TTM 14%；但 Q2 單季 9.6% 顯示模組廠擴建開始吃現金",
      "⑤競爭者會否被吸引：會——EMCOR／Quanta／Fluor 等資本量級更大，電氣包本就競爭激烈；場地整備靠地緣產能與客戶關係短期難複製",
      "⑥股價反映多少期待：前瞻本益比 24.3x（FY26）／19.2x（FY27）、PEG 1.45，反映 FY28 前約 20% 複利、之後放緩；未反映 capex 消化情境",
      "⑦成長率下修估值撐得住嗎：撐不住——成長降至 10% 情境本益比 14x，對現價 −48%；最弱的一題＝⑦，與陷阱定性 🟡 一致"
    ],
    "segments": [
      {
        "name": "E-Infrastructure（場地整備＋CEC 電氣）",
        "fy0": "FY25 約 $1.3B（由 Q1/Q2 FY26 年增率 174%／192% 回推，含 CEC Q4 貢獻）",
        "driver": "量：園區數 × 每園區階段數；價：無（管理層明言未加價）；CEC 併入為無機成分",
        "fy1e": "FY26 約 $2.9B（指引分部成長 >100%）",
        "fy2e": "FY27 約 $3.5B（+20%，分析師估 25%，打折）",
        "fy3e": "FY28 約 $4.0B（+15%）",
        "om_path": "調整後營業利益率 23.3%（Q2）→ 25%（FY27，CEC 回補）→ 24%",
        "eps_contrib_pct": "約 80%"
      },
      {
        "name": "Transportation Solutions",
        "fy0": "FY25 約 $0.75B（推算）",
        "driver": "量：主動減少低價競標公路；價：選案提升利潤率（Q2 調整後營業利益率 19.5%）",
        "fy1e": "FY26 −7% 至 −10%（指引）",
        "fy2e": "FY27 持平（IIJA 續法案不確定）",
        "fy3e": "FY28 +3%",
        "om_path": "13.5–14%（FY25）→ 17–19%",
        "eps_contrib_pct": "約 14%"
      },
      {
        "name": "Building Solutions",
        "fy0": "FY25 約 $0.4B（推算）",
        "driver": "量：住宅開工；價：持平",
        "fy1e": "FY26 高個位數至低雙位數下滑（指引）",
        "fy2e": "FY27 持平",
        "fy3e": "FY28 +5%",
        "om_path": "上半年營業利益 $14.7M（去年 $22.2M）",
        "eps_contrib_pct": "約 6%"
      }
    ],
    "decay_signals": [
      "盈餘品質：EPS 複利顯著高於營收複利——FY26 EPS +128% 對比營收 +68%，差距 >5pp（利潤率擴張＋CEC）；亮燈",
      "隱性資本密集：Q2 單季 FCF 率降至 9.6%（Q1 17.7%），資本支出由 $19.6M 升至 $50.0M（模組廠）；尚未達維持性資本支出占 FCF >60%，觀察",
      "產業結構：Transportation 合併在手訂單較 2025 年底 −11%、Building 營業利益 −34%；非核心分部 TAM 收縮，亮燈",
      "護城河侵蝕：E-Infrastructure 分部利潤率 −420bp（混合效應）；合併毛利率未連 2 季下滑，不亮",
      "SBC／營收 0.69%，不亮；FCF／淨利上半年約 1.1x，不亮"
    ],
    "trap_rating": "🟡（2 個信號亮燈：EPS 對營收複利差距、非核心分部收縮）"
  },
  "quality": {
    "three_year": [
      {
        "metric": "毛利率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋（Q3 FY25 年增 +280bp，來源：摘要）",
        "fy25_ttm": "FY25 23%（來源：摘要）／TTM 23.8%",
        "peer_median": "FIX 25.7／EME 19.4／PWR 15.5／MTZ 12.9（中位約 17.4）",
        "assessment": "高於同業中位 6pp，僅次於 FIX"
      },
      {
        "metric": "調整後 EBITDA 率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "FY25 >20%（來源：摘要）／FY26 指引 $891–916M ÷ $4.0–4.15B ≈ 22%",
        "peer_median": "證據包未涵蓋",
        "assessment": "擴張中"
      },
      {
        "metric": "ROIC",
        "fy23": "14%（前份報告引用）",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "22%（前份報告引用）",
        "peer_median": "證據包未涵蓋",
        "assessment": "8pp 擴張；超過 WACC 約 12pp"
      },
      {
        "metric": "SBC／營收",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "Q1 FY26 0.91%／Q2 FY26 0.69%",
        "peer_median": "證據包未涵蓋",
        "assessment": "極低，非稀釋來源"
      },
      {
        "metric": "營運現金流／淨利",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "上半年 FY26 $328M ÷ 約 $291M ≈ 1.13x",
        "peer_median": "證據包未涵蓋",
        "assessment": "客戶預付款支應，現金轉換優於淨利"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 率",
        "value": "約 13.6%（營業利益率 18.13% × (1−25%)）",
        "note": "TTM 至 2026-06-30"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（含 CEC 商譽後估約 1.6x）",
        "note": "由 ROIC 22%（FY25）÷ NOPAT 率反推"
      },
      {
        "component": "ROIC",
        "value": "22%（FY25，前份報告引用）",
        "note": "FY23 14% → FY25 22%，驅動來源＝利潤率（Transportation 9.6%→13.5–14%、E-Infrastructure 23–25%）而非周轉"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO",
        "value": "證據包未涵蓋",
        "note": "10-Q 未在證據包內摘出應收／合約資產負債明細"
      },
      {
        "metric": "CCC 方向",
        "value": "負或近零（推斷）",
        "note": "上半年營運現金流 $328M 高於淨利約 $291M；承包商的「超額計費」（合約負債）為營運資金來源"
      },
      {
        "metric": "債務到期",
        "value": "Q1 FY26 債務 $287M、現金 $512M、淨現金 $224M（來源：摘要）",
        "note": "8-K 有信用額度修訂紀錄（events 軸）；到期年份與利率證據包未涵蓋"
      }
    ],
    "buyback": {
      "authorization": "剩餘授權 $362M（Q1 FY26，來源：摘要）；2025 年 11 月時為 $80.9M，Q4 FY25 增至 $374M",
      "q1_capital_return": "Q1 FY26 回購 $12M，均價 $305.14（來源：摘要）；2025 年迄 Q3 回購 $48.5M（來源：摘要）；Q2 FY26 回購金額證據包未涵蓋",
      "buyback_to_fcf": "Q1 $12M ÷ Q1 FCF $146M ≈ 8%，遠低於 80% 警示線；資本主要流向併購（CEC $505M、Stone Ridge）",
      "avg_price_vs_now": "Q1 均價 $305.14 對比現價 $486.49，低 37%；回購時盈餘殖利率 20.03÷305.14 ≈ 6.6%，高於 10 年期殖利率＋2% 的門檻",
      "eps_cagr_ex_buyback": "淨回購約 0.5%／年，剔除後 FY26→FY28 EPS 複利約 19.6%（對比含回購 20.1%），差距 <5pp"
    },
    "lumpiness": {
      "fcf_5y": "五年逐年 FCF 證據包未涵蓋；FY26 上半年 FCF ≈ $258M（Q1 $146.0M＋Q2 $112.4M），TTM FCF 率 14.0%",
      "maint_capex_method": "以折舊約當維持性資本支出（保守法，年約 $70M）；FY26 總資本支出年化約 $140M，其中模組廠擴建為成長性支出",
      "owner_earnings": "FY26E 約 營運現金流 $650M − 維持性資本支出 $70M ≈ $580M（每股約 $18.7，以約 31M 股）",
      "verdict": "🟡 需關注：專案型承包商的 FCF 隨合約負債進出而季度波動（Q1 17.7% → Q2 9.6%）；現金轉換本身健康，波動來自營運資金時點而非品質"
    }
  },
  "governance": {
    "capalloc_grade": "A",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC（CEC 第 3 年＝FY2028）",
        "value": "尚未到第 3 年，不計；Q1 FY26 CEC 貢獻營收 $156M（前份報告引用），管理層預期 12–18 個月回補 300–500bp 利潤率（來源：摘要）；早年乾式導管小型併購與場地整備合併後利潤率 +40%（來源：摘要）",
        "pass": null
      },
      {
        "item": "回購買入收益率 ≥ 10 年期殖利率＋2%",
        "value": "Q1 FY26 均價 $305.14 → 盈餘殖利率約 6.6%（FY26 EPS 20.03）≥ 約 6.3%",
        "pass": true
      },
      {
        "item": "SBC 淨稀釋率 ≤1.5%／年",
        "value": "SBC 占營收 0.69%（Q2 FY26）；淨稀釋遠低於 1.5%",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "回購",
        "detail": "2025 年迄 Q3 $48.5M；Q1 FY26 $12M（均價 $305.14）；剩餘授權 $362M（來源：摘要）"
      },
      {
        "type": "併購",
        "detail": "CEC Facilities Group $505M（$450M 現金＋$55M 股票，earn-out 至 2029）；Stone Ridge Contracting（2026-01，FY26 營收 $180–200M、EBITDA 率 mid-teens，earn-out 至 2031）；管理層稱高品質標的比一年前多、不追求「第四條腿」（來源：摘要）"
      },
      {
        "type": "股息",
        "detail": "無"
      },
      {
        "type": "內部人交易／薪酬",
        "detail": "近 12 個月內部人交易與薪酬結構證據包未涵蓋（數據限制）；前份報告記 CEO Cutillo 減持 $92M，本輪無更新資料"
      }
    ],
    "sbc": {
      "pct_revenue": 0.69,
      "pct_gaap_oi": 3.7,
      "trend": "Q1 FY26 0.91% → Q2 FY26 0.69%（SBC $7.5M → $8.1M，營收成長更快）",
      "note": "SBC $8.1M ÷ GAAP 營業利益 $219.3M ≈ 3.7%；非稀釋來源。股權結構（雙重股權、創辦人持股）證據包未涵蓋"
    }
  },
  "valuation": {
    "tier": "專業營建承包商（資料中心／機電）——同 tier 對照 FIX／EME／PWR／MTZ；同業前瞻本益比證據包未涵蓋，溢折價獨立推導",
    "peers": [
      {
        "name": "Comfort Systems（FIX）",
        "fwd_pe": "證據包未涵蓋",
        "note": "同主題最強對照；營業利益率 16.5%、FCF 率 19.2%"
      },
      {
        "name": "EMCOR（EME）",
        "fwd_pe": "證據包未涵蓋",
        "note": "營業利益率 9.6%"
      },
      {
        "name": "Quanta（PWR）",
        "fwd_pe": "證據包未涵蓋",
        "note": "營業利益率 6.1%"
      }
    ],
    "fwd_pe": 24.29,
    "peg": 1.45,
    "percentile_5y": 96,
    "val_light": "🟡",
    "val_light_derivation": "PEG：前瞻本益比 24.29（$486.49 ÷ FY26 共識 $20.03）÷ 3 年 EPS 複利 16.7%（FY26→FY28 共識複利 20.1%，FY29 外推 +10%）＝1.45 → 合理。分位：本站五年高低點為 trailing 口徑、僅 4 個年度點（FY22 年底 9.19x 至 FY25 年底 34.03x），現值 33.12x 落第 96 分位 → 機械讀數為過熱；但 FY22 低點對應的是低利潤率土木承包時期，樣本被業務轉型污染，且短窗前瞻本益比 24.29x 是 2026-05 以來最低（高點 47.09x）。兩把尺方向相反，依品質複利尺以前瞻本益比與 PEG 為優先尺 → 🟡 合理。不觸發盲點救援（非 🟠）；共識 FY2 近 90 天 +10.97% 作旁證支持不落 🔴",
    "targets": {
      "short_1y": {
        "eps": 25.4,
        "pe": 22,
        "price": 558.8,
        "upside_pct": 14.9,
        "basis": "FY27 共識 EPS × 22x（護城河 B、成長 🟡、FY27 仍 +27%）"
      },
      "mid_2y": {
        "eps": 28.91,
        "pe": 21,
        "price": 607.1,
        "upside_pct": 24.8,
        "basis": "FY28 共識 EPS × 21x（成長放緩至 14%）"
      },
      "five_y": {
        "eps": 34.0,
        "pe": 20,
        "price": 680.0,
        "upside_pct": 39.8,
        "basis": "Base FY30 EPS × 長期 20x"
      },
      "bear_anchor": {
        "eps": 18.03,
        "pe": 14,
        "price": 252.4,
        "downside_pct": -48.1,
        "basis": "Bear EPS＝FY26 共識 20.03 × 0.9；Bear 本益比＝成長降至 10% 情境 14x；下行 48% >15% 正常可用，無數學假象"
      },
      "sell_side": "8 位分析師共識 Strong Buy、平均目標價 $876；15 位平均 $971.73；KeyBanc 8/5 由 $922 下修至 $754；DA Davidson 8/21 首評 Buy $700；Simply Wall St 公允價值約 $941——全距 $700–$972（最高／最低 1.4x，無兩極分歧）；現價 $486.49 低於全部目標價，市場已比賣方悲觀，續漲不需要共識上修，而需要 capex 消化疑慮被證偽"
    },
    "upside_short_pct": 14.9,
    "upside_mid_pct": 24.8
  },
  "trap_analysis": {
    "pattern": "週期頂部盈餘誤當長期複利（峰頂盈餘陷阱）：承包商在 capex 高峰的利潤率與在手訂單看起來像結構性護城河，週期一轉即同時失去營收與倍數",
    "evidence_against": "簽約在手訂單 $4.33B（+116%）、合併 $5.62B（+150%），相當於 FY26 營收指引的 1.05–1.4 倍；園區型合約 5–12 年續階；淨現金 $224M（Q1）；資本支出僅營收 3.5%、SBC 0.69%，即使營收腰斬也不會現金失血；管理層在 2025-11 即公開說會拒接利潤率不對的巨型專案（來源：摘要），FY25 起 Transportation 主動縮量提利潤率證明選案紀律是真的",
    "evidence_for": "需求 100% 來自單一 capex 週期，且融資結構已轉向舉債與表外（Moody's）；E-Infrastructure 分部利潤率 −420bp 顯示打包後的邊際業務利潤率更低；兩個非 AI 分部同步收縮，沒有第二支柱；EPS +128% 對營收 +68% 的差距是利潤率擴張，週期下行時會反向放大",
    "bear_case": "空頭最強一擊（18 個月內 −30% 以上的路徑）：2027 年 1–2 月超大規模業者財報把 2027 capex 指引降到年增個位數或年減，同時 Sterling FY27 指引 E-Infrastructure 成長 <15%、CEC 利潤率回補未見；市場把本益比從 24x 壓到 14–15x、FY27 EPS 共識自 $25.4 下修到 $21，股價落到 $300 附近（−38%）。監測指標：四大 capex 指引年增、簽約在手訂單季度環比、E-Infrastructure 調整後營業利益率",
    "monitor": [
      "簽約在手訂單季度環比：連 2 季下滑＝陷阱正在發生",
      "E-Infrastructure 調整後營業利益率：連 2 季 <22%＝混合效應變結構性",
      "四大超大規模業者合併 capex 指引年增：<+10%＝需求週期見頂",
      "營運現金流／淨利：<0.8x 連 2 季＝合約負債開始回吐（客戶不再預付＝新專案枯竭的領先訊號）"
    ],
    "verdict": "🟡",
    "label": "觀察期"
  },
  "appendix_a": {
    "signal": "B",
    "moat_score": 7.0,
    "growth_durability": 7,
    "quality_score": 7.0,
    "ai_risk": "🟢",
    "long_term_confidence": "中",
    "val": "🟡",
    "ma": "-",
    "fpe_fy2": 19.15,
    "pct_5y": 96,
    "peg_fy2": 1.15,
    "upside_short_pct": 14.9,
    "upside_mid_pct": 24.8,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "B"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY26": 20.03,
      "FY27": 24.8,
      "FY28": 28.5,
      "FY29": 31.5,
      "FY30": 34.0
    },
    "fy_end_month": 12,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-11",
      "date_precision": "month",
      "type": "guidance",
      "event": "Q3 FY2026 財報：在手訂單、E-Infrastructure 調整後營業利益率、FY26 指引第三次上修與否",
      "impact": "高",
      "watch": "簽約在手訂單是否 ≥$4.33B；分部利潤率是否 ≥23.3%"
    },
    {
      "date": "2026-09",
      "date_precision": "month",
      "type": "regulatory",
      "event": "IIJA 聯邦公路資金於 2026-09 底到期，續法案進度決定 Transportation 2027 能見度（來源：摘要）",
      "impact": "中",
      "watch": "續法案是否通過或延長；Transportation 在手訂單方向"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "guidance",
      "event": "FY2026 全年財報與 FY2027 指引：E-Infrastructure 成長率、CEC 利潤率回補進度、併購動向",
      "impact": "高",
      "watch": "FY27 E-Infrastructure 指引 ≥+20% 且分部利潤率 ≥25% ＝論點增強；<15% ＝削弱"
    },
    {
      "date": "2027-02",
      "date_precision": "month",
      "type": "macro",
      "event": "四大超大規模業者 Q4 財報公布 2027 年 capex 指引（1–2 月）",
      "impact": "高",
      "watch": "合併 capex 指引年增 ≥+10% 續撐；轉負即為清倉級訊號"
    },
    {
      "date": "2027-06",
      "date_precision": "quarter",
      "type": "capacity",
      "event": "模組廠三倍擴建投產（來源：摘要）與晶圓廠園區專案進入主體施工",
      "impact": "中",
      "watch": "資本支出是否回落至營收 3–4%；E-Infrastructure 非資料中心（半導體）占比"
    }
  ],
  "decision_inputs": {
    "signal": "B",
    "trap": "🟡",
    "val": "🟡",
    "ma": "-",
    "runway_post_y5": "🟡",
    "moat_trend": "↑",
    "moat": "B",
    "capalloc_grade": "A",
    "archetype": "品質複利成長",
    "cycle_position": "中循環",
    "cycle_verdict": null,
    "asym_ratio": 1.85,
    "irr_base_pct": 6.9,
    "ev5y_pct": 32.5,
    "price_at_dd": 486.49,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": 23.13,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 10.97
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "9b",
    "pacing": [],
    "holding_cap": null,
    "requires_critic": [
      "QC-41：裁決強方向（進場）且護城河趨勢方向性（↑）、屬 B2B 客戶集中型與 capex 循環敏感型，需跨模型複核「需求 durability 🔴 是否被在手訂單數字掩蓋」",
      "QC-19／單日事件：財報後 −10%、30 天 −28% 已歸因為利潤率混合效應而非基本面惡化，複核歸因是否過度採信管理層"
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
        "basis": "moat_trend='↑', moat='B'"
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
        "basis": "signal='B'"
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
        "basis": "signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=23.13, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"
      },
      {
        "row": "11.4b-denom",
        "condition": "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
        "hit": false,
        "basis": "輸入缺(val_denominator_disputed=null)，依保守方向處理：不視為觸發（沿用 val 機械讀數）",
        "input_gap": [
          "val_denominator_disputed"
        ]
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
        "hit": false,
        "basis": "signal='B', val='🟡', ma='-'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": true,
        "basis": "signal='B', val='🟡', ma='-'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": false,
        "basis": "signal='B', val='🟡', ma='-'"
      },
      {
        "row": "QC-49",
        "condition": "90 天內翻面須引前次已發火觸發器，否則承繼前次裁決",
        "hit": false,
        "basis": "輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）",
        "input_gap": [
          "qc49_inherit_prior"
        ]
      }
    ],
    "rearm_trigger": "加碼第二階：股價 <$420（FY26 21x）或 FY27 指引 E-Infrastructure ≥+20% 且分部利潤率 ≥25%",
    "exec_line": "新資金：現價買首階三分之一（衛星上限 3% 之 1%）；第二階掛 <$420 或 FY27 指引論點增強（2027-02）；第三階掛 CEC 利潤率回補 ≥200bp 確認。已持有者：不加碼、不清倉，持有至 FY27 指引；觸發清倉級訊號（任一超大規模業者 capex 年減）即減至首倉"
  },
  "triggers": [
    {
      "n": 1,
      "text": "E-Infrastructure TTM 營收年增與簽約在手訂單方向（H1）",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "E-Infrastructure TTM 營收年增；簽約在手訂單 TTM 年增",
      "threshold": "營收年增連 2 季 <15% 或在手訂單年增連 2 季 <0% ＝削弱；合併在手訂單連 3 季年減 ≥10% ＝反轉",
      "action": "削弱＝停止加碼；反轉＝減至首倉",
      "source_freq": "公司季度新聞稿／每季",
      "date": "2026-11-05",
      "evidence_refs": [
        "supply_demand_durability#3"
      ]
    },
    {
      "n": 2,
      "text": "E-Infrastructure 調整後營業利益率回到 25%（H2）",
      "type": "假設驗證",
      "maps_to": "H2",
      "metric": "E-Infrastructure 調整後營業利益率（季度）",
      "threshold": "TTM 連 2 季 <22% ＝削弱；連 3 季 <20% ＝反轉；FY27 ≥25% ＝論點增強",
      "action": "削弱＝停止加碼；反轉＝減至首倉；增強＝加第二階",
      "source_freq": "公司季度新聞稿分部表／每季",
      "date": "2027-02-25",
      "evidence_refs": [
        "capital_markets_pricing#1",
        "capital_markets_pricing#4"
      ]
    },
    {
      "n": 3,
      "text": "超大規模業者 capex 消化（R1）",
      "type": "風險",
      "maps_to": "R1",
      "metric": "四大超大規模業者合併 capex 指引年增",
      "threshold": "連 2 季 <+10% ＝減碼；任一家指引年減＝清倉級（見第 7 條）",
      "action": "減碼至首倉",
      "source_freq": "四大季度財報／每季",
      "date": "2027-02-05",
      "evidence_refs": [
        "supply_demand_durability#3",
        "customer_concentration_credit#5"
      ]
    },
    {
      "n": 4,
      "text": "非 AI 分部與關稅成本（R3／R4）",
      "type": "風險",
      "maps_to": "R3, R4",
      "metric": "Transportation 調整後營業利益率；合併毛利率 TTM",
      "threshold": "Transportation 連 2 季 <15% 且營收續降；合併毛利率 TTM 較 23% 下滑 >150bp 而 FIX／EME 未同步",
      "action": "任一觸發＝停止加碼並重審 H2",
      "source_freq": "季度新聞稿／每季",
      "date": "2027-02-25",
      "evidence_refs": [
        "end_markets#3",
        "end_markets#4",
        "customer_concentration_credit#1",
        "reg_tariff_export#0",
        "reg_tariff_export#1"
      ]
    },
    {
      "n": 5,
      "text": "任一前三大超大規模業者把下一年度 capex 指引改為年減或宣布延後園區",
      "type": "Single Thing",
      "maps_to": "Single Thing",
      "metric": "超大規模業者 capex 指引（年增／年減）與園區公告",
      "threshold": "一家年減＝減至首倉；第二家跟進＝清倉",
      "action": "不等在手訂單數字即執行",
      "source_freq": "四大季度財報與公告／每季",
      "date": "2027-02-05",
      "evidence_refs": [
        "supply_demand_durability#3",
        "customer_concentration_credit#4"
      ]
    },
    {
      "n": 6,
      "text": "第二階加碼：價格回檔或論點增強（雙軌）",
      "type": "加碼",
      "maps_to": "估值／H1／H2",
      "metric": "股價；FY27 指引",
      "threshold": "股價 <$420（FY26 21x、FY27 16.5x）；或 FY27 指引 E-Infrastructure ≥+20% 且分部利潤率 ≥25%",
      "action": "加第二個三分之一；第三階待 CEC 利潤率回補 ≥200bp",
      "source_freq": "日價／FY27 指引（2027-02）",
      "date": "2027-02-25",
      "evidence_refs": [
        "capital_markets_pricing#2"
      ]
    },
    {
      "n": 7,
      "text": "清倉：需求週期反轉且利潤率同步失守",
      "type": "清倉",
      "maps_to": "H1／H2／Single Thing",
      "metric": "合併在手訂單 TTM 年增；E-Infrastructure 調整後營業利益率",
      "threshold": "合併在手訂單年減 ≥10% 連 2 季 且 分部利潤率連 2 季 <20%；或 Single Thing 第二家跟進",
      "action": "清倉；重啟條件＝在手訂單重回年增且四大 capex 指引轉正（2-of-2），重啟後重跑報告、角色 ≤衛星首倉",
      "source_freq": "季度新聞稿／每季",
      "date": null,
      "evidence_refs": [
        "supply_demand_durability#3"
      ]
    },
    {
      "n": 8,
      "text": "減碼：在手訂單環比連續下滑",
      "type": "減碼",
      "maps_to": "H1",
      "metric": "簽約在手訂單季度環比",
      "threshold": "連 2 季環比下滑（自 $4.33B 高點）",
      "action": "減至首倉三分之一",
      "source_freq": "季度新聞稿／每季",
      "date": null,
      "evidence_refs": [
        "end_markets#3"
      ]
    },
    {
      "n": 9,
      "text": "複審日期：FY26 全年財報與 FY27 指引之後",
      "type": "複審日期",
      "maps_to": "全部",
      "metric": "FY27 指引與四大 capex 指引齊備",
      "threshold": "—",
      "action": "重跑報告，重判角色",
      "source_freq": "一次",
      "date": "2027-03-05"
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單與矛盾拓撲",
      "side_a": "方向一致：在手訂單與營收動能極強（簽約 +116%、合併 +150%、E-Infrastructure +192%）；盈餘品質好（營運現金流／淨利 1.13x、SBC 0.69%、淨現金）；估值自 47x 回到 24.3x、PEG 1.45 合理；共識 FY2 近 90 天 +10.97%",
      "side_b": "矛盾拓撲＝集中單一軸：需求 durability——AI capex 週期何時消化（Moody's 舉債融資警訊 對 12 年園區合約）；利潤率混合效應與非 AI 分部走弱是程度差異",
      "ruling": "爭議集中→點名需求 durability 為 binding 軸；信心不整體下修，但角色限衛星、上限 3%、Bear 30%",
      "evidence_level": "L1",
      "settle_metric": "四大超大規模業者 2027 capex 指引年增（2027-02）與簽約在手訂單環比方向",
      "if_then": [
        "若 2027 capex 指引年增 ≥+10% 且 FY27 E-Infrastructure 指引 ≥+20% → 加第二階",
        "若任一家 capex 指引年減 → 減至首倉，不等在手訂單"
      ],
      "evidence_refs": [
        "supply_demand_durability#3"
      ]
    },
    {
      "axis": "三重超預期對比財報後 −10%、30 天 −28%：混合效應或結構性稀釋",
      "side_a": "A 側（管理層與 L1 數字）：E-Infrastructure 分部利潤率 −420bp 是 CEC 電氣包占比上升的混合效應；分部營業利益絕對額大增、合併調整後營業利益率反而由 19.2% 升至 21.6%；管理層預期 12–18 個月回補 300–500bp（來源：摘要）",
      "side_b": "B 側（市場）：打包後的邊際業務利潤率更低，證明整合溢價不存在；KeyBanc 目標價 $922→$754；市場對訂單與利潤率能見度要求更嚴",
      "ruling": "可調和（程度差異）。站 L1：合併利潤率上升是已實現事實，分部 −420bp 為 mix；但依管理層歸因 escrow 原則，不採信也不否定——「回補」列為未證、監測，H2 門檻與第 2 條觸發器預登記證偽期限（FY27 年底前 ≥200bp）",
      "evidence_level": "L1 對 L3",
      "settle_metric": "E-Infrastructure 調整後營業利益率 FY27 各季（≥25% 證實、<22% 證偽）",
      "if_then": [
        "若 FY27 Q2 前分部利潤率回到 ≥25% → 混合說法成立，加第二階",
        "若 FY27 連 2 季 <22% → 結構性稀釋，減至首倉並重審護城河定價維度"
      ],
      "evidence_refs": [
        "capital_markets_pricing#1",
        "capital_markets_pricing#4",
        "capital_markets_pricing#2"
      ]
    },
    {
      "axis": "需求 durability：12 年園區合約與 +150% 在手訂單 對比 Moody's 舉債融資警訊",
      "side_a": "A 側：在手訂單 $5.62B、園區續階 5–12 年、客戶催促進新市場（來源：摘要）、2027 capex 估續增至 $820B",
      "side_b": "B 側：AI capex 已威脅超大規模業者信用品質，Oracle 兩級距離垃圾等級，Goldman 估三年累計 $1.15T 可能跑在變現之前；承包商在手訂單是落後指標，授標停滯要 2–3 季後才反映",
      "ruling": "不可調和（方向相反）。我選 A 側為 Base 但把 B 側定價進 Bear 30% 與倉位上限：依據＝四大現金流最強者無立即降評風險（Moody's 同一份報告），2026–2027 capex 為已公告數字（L2），而消化期為時點未知的 L2 前瞻；「不可裁決至 2027-02」——settle 數據（2027 capex 指引）尚未存在，故現在只付首倉、不付滿倉。現在就賣的最強論證：承包商在 capex 高峰的本益比從來不便宜，24x 買在訂單峰頂＝買在盈餘峰頂；回應＝股價已自高點 −51%、FY27 本益比 19x 已把「2028 放緩」定價一半，但未定價「2027 消化」，故留三分之二彈藥掛觸發器而非現在滿倉",
      "evidence_level": "L2 對 L2",
      "settle_metric": "四大超大規模業者 2027 capex 指引（2027-02）；Sterling 簽約在手訂單 2026-12-31 讀數",
      "if_then": [
        "若 2027 capex 指引合計年增 ≥+10% → B 側暫時證偽，加第二階",
        "若任一家年減或延後園區 → 減至首倉；第二家跟進 → 清倉"
      ],
      "evidence_refs": [
        "supply_demand_durability#3",
        "customer_concentration_credit#5",
        "customer_concentration_credit#4"
      ]
    },
    {
      "axis": "Transportation「主動選案」對比在手訂單 −11% 與 DOT 集中度 58%",
      "side_a": "A 側：Q2 營收 −20% 是資源移往 E-Infrastructure 的主動選擇，分部調整後營業利益率逆勢 +500bp 至 19.5%",
      "side_b": "B 側：合併在手訂單較 2025 年底 −11%、前四大州 DOT 集中度 47%→58%、IIJA 2026-09 到期——縮量也可能是拿不到案子",
      "ruling": "可調和。利潤率同步上升支持 A 側（L1）；但把 B 側轉為期限閘：若營收與利潤率同時下滑則 A 側證偽（第 4 條觸發器）",
      "evidence_level": "L1",
      "settle_metric": "Transportation 調整後營業利益率與營收方向同季對照",
      "if_then": [
        "若利潤率維持 ≥15% 而營收續降 → 接受選案說法，不動",
        "若利潤率與營收同降連 2 季 → 停止加碼，重審 R3"
      ],
      "evidence_refs": [
        "end_markets#3",
        "customer_concentration_credit#1",
        "end_markets#4"
      ]
    },
    {
      "axis": "估值多尺矛盾：trailing 本益比第 96 分位 對比 前瞻本益比短窗最低與 PEG 1.45",
      "side_a": "trailing 口徑 33.1x 在 4 個年度點中落第 96 分位（FY22 年底 9.2x 至 FY25 年底 34.0x）→ 過熱",
      "side_b": "前瞻本益比 24.3x 為 2026-05 以來最低（高點 47.1x）、FY27 本益比 19.2x、PEG 1.45 → 合理",
      "ruling": "依品質複利尺，前瞻本益比與 PEG 為優先尺 → 🟡；trailing 分位樣本被業務轉型污染（FY22 為低利潤率土木時期）且 EPS 正以三位數成長使 trailing 分母過時。分母爭議檢查：「合理」的分母是 FY26 共識 $20.03，與需求 durability 爭點相關但 FY26 已由指引 $19.70–20.30 鎖定，非本章爭點，不設分母爭議旗標",
      "evidence_level": "L1",
      "settle_metric": "FY27 共識 EPS 方向（現 $25.4）",
      "if_then": [
        "若 FY27 共識上修 ≥+10% 且股價不動 → PEG 落 <1.2，加第二階",
        "若 FY27 共識下修 ≥−15% → PEG 走高、trailing 讀數變成正確的那把尺，減至首倉"
      ],
      "evidence_refs": [
        "capital_markets_pricing#4"
      ]
    },
    {
      "axis": "與上一份報告（2026-05-05）的交叉矛盾：等回測 $410／$336 對比 現價 $486 進場",
      "side_a": "前份：B 級衛星候選、觀望偏進場，等回測 $410 或 $336；當時價 $529.49、FY2 本益比 27.2x、PEG 0.68、4 週 +57% 動能透支",
      "side_b": "本次：進場衛星首階；價 $486.49（−8.1%）、FY27 本益比 19.15x、PEG 1.45",
      "ruling": "翻面主因＝共識盈餘上修（FY26 指引兩度上修、FY2 共識 90 天 +11%、FY3 +39%）把 FY27 本益比自 27x 壓到 19x，價格只回了 8%；前份等的是價格回測，本次以盈餘上修取代價格回測作為進場理由；動能已從透支變成 13 週 −45%。跨 90 天（118 天），不受承繼閘保護；前份無決策層裁決欄，屬方法論版本差異",
      "evidence_level": "L1",
      "settle_metric": "FY27 指引與共識方向",
      "if_then": [
        "若股價回到前份 $410 觸發區 → 依第 6 條加第二階",
        "若 FY27 共識轉為下修 → 回到前份的觀望立場，減至首倉"
      ],
      "evidence_refs": [
        "capital_markets_pricing#2"
      ]
    },
    {
      "axis": "同形狀 peer 對帳與產業報告對帳",
      "side_a": "30 天內無 FIX／EME／PWR／MTZ 之本站裁決可對照，一句帶過不阻斷；證據包 canonical_id 為 gap，無產業報告機器欄可對帳（ID gap：AI 資料中心營建）",
      "side_b": "FIX 為同主題最強對照且利潤率、FCF 率、YTD 股價表現皆優於 Sterling；若日後 FIX 取得不同裁決，差異理由應落在「場地整備稀缺產能 對比 機電規模」",
      "ruling": "無近期 peer 裁決；建議日後補跑 FIX 以對帳",
      "evidence_level": "L3",
      "settle_metric": "—",
      "if_then": [
        "若 FIX 日後判進場核心而本檔衛星 → 差異須以 FCF 率 19% 對 14% 與需求分散度解釋",
        "若 FIX 判迴避 → 重審本檔 H1"
      ]
    },
    {
      "axis": "前份漂移：dca_verdict",
      "prior_field": "dca_verdict",
      "side_a": "本次＝進場",
      "side_b": "前份＝無此欄（v12.3 無決策層，文字裁決為「觀望偏進場」）",
      "ruling": "方法論驅動為主（前份無矩陣裁決）；基本面次之（共識上修）；價格第三（−8%）"
    },
    {
      "axis": "前份漂移：dca_role",
      "prior_field": "dca_role",
      "side_a": "本次＝衛星",
      "side_b": "前份＝無此欄（文字為「衛星候選」）",
      "ruling": "方法論驅動（前份無此欄）；角色方向與前份文字一致"
    },
    {
      "axis": "前份漂移：signal",
      "prior_field": "signal",
      "side_a": "本次＝B",
      "side_b": "前份＝B",
      "ruling": "無漂移；品質分 7.0 與前份 6.9 同帶"
    },
    {
      "axis": "前份漂移：val",
      "prior_field": "val",
      "side_a": "本次＝🟡（PEG 1.45、前瞻本益比 24.3x）",
      "side_b": "前份＝🟡（PEG 0.68、FY2 本益比 27.2x、分位 68）",
      "ruling": "燈號無漂移；內部數字變動主因＝方法論（本次 3 年複利以前瞻錨定 16.7%，前份以受 CEC 污染的 trailing 基期算出高複利）；價格次之"
    },
    {
      "axis": "前份漂移：ma",
      "prior_field": "ma",
      "side_a": "本次＝-（證據包無週線均線資料）",
      "side_b": "前份＝✅ 強勢進場",
      "ruling": "資料可得性驅動（方法論）為主；價格驅動為次——股價自 52 週高點 −51%、13 週 −45%，實際週線狀態極可能已非強勢，但不得推測填值"
    },
    {
      "axis": "前份漂移：trap",
      "prior_field": "trap",
      "side_a": "本次＝🟡 觀察期",
      "side_b": "前份＝🟡 觀察期",
      "ruling": "無漂移；陷阱模式由「動能透支」改為「峰頂盈餘」，屬基本面情境變化"
    },
    {
      "axis": "前份漂移：moat_trend",
      "prior_field": "moat_trend",
      "side_a": "本次＝↑",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）；基本面支持——CEC 整合、在手訂單 +116%、集中度下降"
    },
    {
      "axis": "前份漂移：runway_post_y5",
      "prior_field": "runway_post_y5",
      "side_a": "本次＝🟡",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：asym_ratio",
      "prior_field": "asym_ratio",
      "side_a": "本次＝1.85",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：ev5y_pct",
      "prior_field": "ev5y_pct",
      "side_a": "本次＝+32.5%",
      "side_b": "前份＝無此欄（upside_5y 55%）",
      "ruling": "方法論驅動（機率加權 對 單點）；基本面次之——本次 Bear 30% 含 capex 消化"
    },
    {
      "axis": "前份漂移：irr_base_pct",
      "prior_field": "irr_base_pct",
      "side_a": "本次＝6.9%",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：max_dd_pct",
      "prior_field": "max_dd_pct",
      "side_a": "本次＝−55%（範圍 −35% 至 −55%）",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：bull_5y_price",
      "prior_field": "bull_5y_price",
      "side_a": "本次＝$1,104",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：bear_5y_price",
      "prior_field": "bear_5y_price",
      "side_a": "本次＝$208",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：p_bull_pct",
      "prior_field": "p_bull_pct",
      "side_a": "本次＝25%",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：p_bear_pct",
      "prior_field": "p_bear_pct",
      "side_a": "本次＝30%",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）；30% 依內生天花板超出規則"
    },
    {
      "axis": "前份漂移：rearm_trigger",
      "prior_field": "rearm_trigger",
      "side_a": "本次＝加碼第二階 <$420 或 FY27 指引論點增強",
      "side_b": "前份＝無此欄（文字為等回測 $410／$336）",
      "ruling": "方法論驅動（新欄）；價格門檻與前份 $410 接近，屬延續"
    },
    {
      "axis": "前份漂移：price_at_dd",
      "prior_field": "price_at_dd",
      "side_a": "本次＝$486.49",
      "side_b": "前份＝$529.49",
      "ruling": "價格驅動：−8.1%；期間曾至約 $993 高點再回落 51%"
    },
    {
      "axis": "前份漂移：archetype",
      "prior_field": "archetype",
      "side_a": "本次＝品質複利成長（次型循環 capex 建設）",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）"
    },
    {
      "axis": "前份漂移：cycle_position",
      "prior_field": "cycle_position",
      "side_a": "本次＝中循環",
      "side_b": "前份＝無此欄",
      "ruling": "方法論驅動（新欄）；基本面依據＝capex 仍加速但融資轉向舉債"
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "客戶身分未揭露：E-Infrastructure 前四大客戶 27%（FY25）但不知道是誰，無法判斷是否同時押在最弱信用（Oracle）上；FY22 的 35% 揭露已被 10-K 三年序列取代，但「是誰」的盲點沒變",
        "evidence_refs": [
          "customer_second_source#0",
          "customer_concentration_credit#5"
        ]
      },
      {
        "text": "地理集中：專案集中德州、亞利桑那、卡羅來納三州，管理層拒答德州占比（來源：摘要 Q&A）；一州的電網或許可政治即可拖慢多個園區",
        "evidence_refs": [
          "geo_supply_chain#0"
        ]
      },
      {
        "text": "最新一季（Q2 FY2026，2026-08-03）法說逐字稿不在證據包內，Q&A 語氣與 CEC 回補時程的最新說法只能靠新聞稿與第三方轉述；Q3 FY25 逐字稿亦缺檔僅有摘要",
        "evidence_refs": [
          "capital_markets_pricing#1"
        ]
      },
      {
        "text": "模組化施工的長期影響：公司三倍擴建模組廠（來源：摘要）代表它相信現場人力會被工廠端取代——這既是應對也是自證威脅存在",
        "evidence_refs": [
          "substitute_technology#0"
        ]
      },
      {
        "text": "在手訂單是落後指標：授標停滯到簽約在手訂單下滑有 2–3 季時差；所有觸發器中只有超大規模業者 capex 指引是領先的",
        "evidence_refs": [
          "supply_demand_durability#3",
          "end_markets#3"
        ]
      }
    ],
    "failure_story": "五年後虧 50%：2027 年 Q4 起超大規模業者把 2028 capex 指引轉為年減，園區續階延後；Sterling 簽約在手訂單自 $4.3B 兩年內縮到 $2B，E-Infrastructure 營收 −30%、分部利潤率跌到 18%，FY29 EPS $15，市場給 13x → $200。此故事直接撞上 Single Thing（超大規模業者 capex 年減）✅，不改 Single Thing",
    "second_failure": "成功但劣化：H1 完全兌現（在手訂單續增、營收 FY30 達 $6B），但以「電氣包占比過半、分部利潤率 18%、每年靠一筆併購維持成長」的形態兌現；市場把估值框架從「AI 基礎建設複利」切換到「一般機電承包商」（EME 式 15x），FY30 EPS $30 × 15x ＝ $450，5 年報酬 −7%。機率不可忽略（約 20%），已反映在 Base 終端倍數 20x 而非維持 24x",
    "max_dd": {
      "lo": -55,
      "hi": -35,
      "path_risk": "🔴",
      "trigger_time": "最可能觸發時點＝2027 年 1–2 月超大規模業者 2027 capex 指引季（若指引令人失望）或 2027-02 FY27 指引 E-Infrastructure <15%；恢復峰值時間＝若為消化期，需下一輪 capex 週期（3–4 年）；若為混合效應誤讀，2–4 季。路徑風險 🔴 但論點完整（護城河 ↑、非估值依賴），依規則不因波動砍倉，改註記「深回撤心理準備」＋衛星上限 3%"
    }
  },
  "kill_metrics": [
    {
      "metric": "簽約在手訂單季度環比",
      "bear_threshold": "連 2 季環比下滑（自 $4.33B）",
      "window": "每季",
      "source": "公司季度新聞稿",
      "last_status": "ok"
    },
    {
      "metric": "E-Infrastructure 調整後營業利益率",
      "bear_threshold": "連 2 季 <22%；連 3 季 <20% 清倉級",
      "window": "每季",
      "source": "公司季度新聞稿分部表",
      "last_status": "ok"
    },
    {
      "metric": "四大超大規模業者合併 capex 指引年增",
      "bear_threshold": "連 2 季 <+10%；任一家年減＝清倉級",
      "window": "每季",
      "source": "四大季度財報",
      "last_status": "ok"
    },
    {
      "metric": "營運現金流／淨利",
      "bear_threshold": "<0.8x 連 2 季（合約負債回吐）",
      "window": "每季",
      "source": "10-Q",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "指紋：毛利 23.8%、營業利益率 18.1%、FCF 率 14.0%、SBC 0.69%、資本支出／營收 3.5%、淨現金——盈餘品質符合品質複利；但營收來源＝AI 資料中心 capex 單一週期（E-Infrastructure 約七成營收、分部在手訂單 92% 任務關鍵型）→ 主型品質複利、次型循環 capex 建設，信心中。循環鏡頭規則檔未在證據包內，未換尺；以 Bear 30%＋衛星上限 3% 承接循環成分。",
    "thesis": "H1 需求：簽約在手訂單 $4.33B ≈ FY26 營收指引 $4.0–4.15B 的 1.05x → 12 個月能見度已鎖；園區 5–12 年續階撐 2 年門檻。H2 利潤率：Q2 分部 23.3%（−420bp 混合）對管理層 mid-20% 指引 → 差 200bp，回補 300–500bp 為未證承諾。H3 資本：回購均價 $305 對現價 $486、併購 $505M 對年 FCF 約 $580M → 紀律在。Single Thing 選超大規模業者 capex 年減：敏感度最大（Bear 路徑 FY28 EPS $17.5 對 Base $28.5 ＝ −39%）。",
    "industry": "Phase II：capex 2026 約 $700B → 2027 約 $820B（+17%）仍加速；但融資轉向舉債（Moody's）＝擴張後段。利潤池：分部調整後營業利益率 23.3% 對 PWR 6.1%／EME 9.6% → 專業分包環節淨流入，不觸發 Runway 降檔。單位經濟 mix-shift：E-Infrastructure（24%）占比 60%→70%、Transportation（19.5%）17%、Building（低）10% → 合併營業利益率結構性 +100 至 +150bp／年，與 H2 一致。",
    "moat": "執行 8：任務關鍵型 92% 在手、客戶催促進新市場、晶圓廠園區得標、集中度 40%→27%。定價 6：管理層自承未加價，利潤率靠選案；分部 −420bp 混合。合併 (8+6)/2 ＝ 7.0 → B。趨勢 ↑：執行擴大（CEC、在手 +116%）、定價持平 → 取關鍵維度執行 → ↑，12 個月內 sourced 點＝2026-06-30 在手訂單。閘一不觸發（<8）；閘二毛利率未連 2 季下滑；閘三對手絕對美元新增證據包未涵蓋。§5.R：NOPAT 率 13.6%、有機 ROIIC 40% × 再投資 35% ＝ 14% 天花板 < 共識 20.1% → 超出⚠。",
    "growth": "Runway 7 年：園區 5–12 年續階＋晶圓廠第二曲線（Q1 2026 得標），但 capex 週期 2028 後無 sourced 估計 → Y5 後 🟡。分部加總：E-Infrastructure $2.9B→$4.0B（FY28）、Transportation $0.69B→$0.71B、Building $0.36B→$0.38B → FY28 合計 $5.1B（+8%／年）；EPS 複利 20.1% 高於營收複利 12% → 差距來自利潤率（+150bp／年）與 CEC 回補，與 §3 mix-shift 對得上。熄火壓測：成長降至 15%／10%／5% → 本益比 18x／14x／11x → 對現價 −26%／−42%／−55%。",
    "quality": "營運現金流／淨利 1.13x（上半年 $328M ÷ 約 $291M）→ 現金轉換好；FCF 率 TTM 14.0% 差 15% 門檻 1pp；Q2 單季 9.6% 因資本支出 $19.6M→$50.0M。Munger 三維：ROIC 22% ✓、FCF 率 14% ✗（邊緣）、護城河 7.0 ✗ → 🔴 一項達標，弱在護城河與 FCF 邊緣。品質分＝(7.0+7)/2 ＝ 7.0；五項體質檢核 0 項不過（毛利率未降、FCF／淨利 >0.7、FY1 共識 90 天 +6.9%、營收年增正、淨現金）→ B。",
    "governance": "回購買入收益率：20.03 ÷ 305.14 ＝ 6.6% ≥ 4.3%＋2% ✓；SBC 淨稀釋 0.69% 營收 ≤1.5% ✓；M&A ROIIC 第 3 年（FY28）未到不計 → 適用 2 項全過 → A。內部人交易與薪酬證據包未涵蓋（數據限制），前份記 CEO 減持 $92M 未更新，不足以降級。",
    "valuation": "前瞻本益比 486.49 ÷ 20.03 ＝ 24.29；3 年複利：(28.91÷20.03)^(1/2)−1 ＝ 20.1%，FY29 +10% → 31.8，(31.8÷20.03)^(1/3)−1 ＝ 16.7%；PEG 24.29 ÷ 16.7 ＝ 1.45 → 🟡。分位 (33.12−9.19)÷(34.03−9.19) ＝ 96%（trailing、n=4）→ 機械 🔴，被前瞻尺覆蓋 → 🟡。目標價：1Y 25.4×22 ＝ $559（+14.9%）；2Y 28.91×21 ＝ $607（+24.8%）；5Y 34.0×20 ＝ $680（+39.8%）；Bear 18.03×14 ＝ $252（−48.1%）。三分量：Base IRR 6.9% ＝ EPS 複利 11.2%／年 × re-rate −3.8%／年 × 回購 0.5% → 非估值依賴。AR ＝ (0.25×126.9)÷(0.30×57.2) ＝ 1.85 平庸。",
    "trap_analysis": "模式＝峰頂盈餘。反證：在手訂單 1.05x 營收、淨現金、資本支出 3.5%。正證：需求單一週期、EPS +128% 對營收 +68% 差距 60pp 為利潤率擴張、非 AI 分部同步收縮。衰退信號 2 個亮燈 → 🟡 觀察期。空頭一擊：capex 指引失望 → 本益比 24x→14x 且 FY27 EPS 25.4→21 → $300（−38%）。",
    "premortem": "Max DD 範圍 −35% 至 −55%（寬 20pp）：下界＝Bear 5 年價 $208 對現價 −57% 的路徑中點附近；上界＝成長降至 15% 情境 −26% 加共識下修。🔴 但護城河 ↑、非估值依賴 → 不砍裁決，倉位上限 3%＋深回撤註記。第二敗局（機電化）機率約 20% → Base 終端 20x 而非 24x。"
  },
  "evidence_dismissed": [
    {
      "ref": "competitive_share_entrants#3",
      "reason": "內容為 YTD 相對股價表現（FIX +77% 對 Sterling +69%），不是營運或份額證據；且讀數截至 2026-08-15，其後 Sterling 又跌至 13 週 −45%，數字已過時。FIX 作為對照的營運差距已由 peer_financials（FCF 率 19.2% 對 14.0%）承接在護城河對手表"
    }
  ],
  "plain": {
    "verdict_line": "進場，但只當衛星，先買三分之一。",
    "verdict_sub": "現價買第一份，剩下兩份等股價回到 $420 以下，或明年二月公司給出更強的 2027 指引再加。",
    "five": {
      "how_it_makes_money": "幫 Microsoft、Amazon 這類公司把資料中心和晶圓廠的地整平、管線與電氣做好，按專案收錢。生意的關鍵不是報價高，而是別人做不了這麼大、這麼快。",
      "why_now": "股價從高點腰斬，但公司今年獲利指引還在往上修。前瞻本益比從 47 倍掉到 24 倍，第一次進入合理區。",
      "why_this_size": "所有訂單都來自同一個 AI 資本支出週期，週期一轉整家公司同時失去營收和估值。這種公司只能當衛星，上限三個百分點。",
      "biggest_fear": "怕的是 2027 年大型雲端業者把資本支出指引改成年減。Moody's 已經警告他們愈來愈靠借錢蓋資料中心。",
      "how_to_act": "新資金先買三分之一，其餘掛在價格回檔或指引轉強兩個條件上。已持有的人不加不減，等明年二月再看。"
    },
    "business": {
      "what_to_whom": "把場地整備和電氣工程打包賣給超大規模雲端業者、晶圓廠和大型製造業，另有公路機場與住宅基礎兩個小分部。",
      "why_customers_stay": "園區型專案一蓋五到十二年，續階工程幾乎都回到原承包商手上。客戶現在是催著公司進新市場，而不是找替代者。",
      "moat_direction": "護城河 B 級、方向向上，靠執行力和稀缺產能。最弱的地方是定價權，管理層自己說沒有拿到更高的價格。"
    },
    "bets": [
      {
        "claim": "我押資料中心與晶圓廠需求至少撐到 2028 年，在手訂單不會見頂。",
        "wrong_when": "簽約在手訂單連續兩季環比下滑，或大型雲端業者資本支出指引年增低於一成。"
      },
      {
        "claim": "我押 CEC 電氣業務的利潤率會回補，分部利潤率回到 25%。",
        "wrong_when": "分部調整後營業利益率連續兩季低於 22%，混合效應變成結構性稀釋。"
      },
      {
        "claim": "我押管理層守住選案紀律和淨現金，不會為了成長亂買公司。",
        "wrong_when": "淨現金轉成淨負債，或公路分部營收和利潤率一起往下掉。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "大型雲端業者 2027 年資本支出進入消化期，訂單停滯兩三季後才在數字上看到。"
      },
      {
        "clock": "⚡",
        "text": "電氣業務拉低分部利潤率 420 個基點的混合效應，被證明是永久性的。"
      },
      {
        "clock": "🐢",
        "text": "公路與住宅兩個分部同時萎縮，公路前四大客戶集中度已升到 58%，聯邦資金法案九月底到期。"
      }
    ],
    "market_wrong": "市場把財報後的利潤率下滑讀成護城河變薄，我認為那是電氣工程占比升高的混合效應，整體利潤率其實在升。市場也還沒定價 2027 年資本支出消化的情境，所以我不滿倉。分歧在利潤率的性質，不在需求。",
    "growth_funding": "公司自己的錢每年最多撐 14% 的成長，共識卻要 20%。差額靠客戶預付款和電氣利潤率回補，所以 Bear 機率壓到三成。",
    "stories": {
      "bull": "雲端資本支出 2027 年後繼續雙位數成長，晶圓廠園區變成第二條曲線，電氣利潤率回補。五年後每股獲利 $46、本益比 24 倍。",
      "base": "在手訂單分年轉化、2028 年起放緩，公司獲利複利一成出頭，本益比從 24 倍慢慢降到 20 倍。五年後每股獲利 $34。",
      "bear": "2027 年下半年資本支出消化，新園區停擺，關稅推高成本。每股獲利跌到 $16、本益比 13 倍，股價剩 $208。"
    },
    "change_my_mind": [
      {
        "what": "任一大型雲端業者的下一年度資本支出指引",
        "threshold": "改成年減，或宣布延後園區",
        "then": "立刻減到首倉；第二家跟進就清倉",
        "when": "2027-02-05"
      },
      {
        "what": "公司 2027 年指引與電氣利潤率",
        "threshold": "分部成長至少兩成且利潤率回到 25%",
        "then": "加第二個三分之一",
        "when": "2027-02-25"
      },
      {
        "what": "簽約在手訂單環比",
        "threshold": "連續兩季下滑",
        "then": "減到首倉",
        "when": "—"
      }
    ],
    "prior_compare_reason": "上一份等回測 $410 才進場，這次在 $486 進場，主因是獲利上修把明年本益比從 27 倍壓到 19 倍，價格本身只回了 8%。方法論也不同，上一份沒有決策矩陣。",
    "how_to_lose": "第一種死法是資本支出週期反轉，營收和倍數一起掉，最深可能跌五成五。第二種死法是論點成立但公司變成一般機電承包商，市場只給 15 倍，五年下來白忙一場。",
    "evidence_quality": "十一個覆蓋軸全有結果，數字以 2026 年第二季為準。逐字稿沒有親讀任何一季，最新一季法說不在證據包內，其餘三季只有摘要。"
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


