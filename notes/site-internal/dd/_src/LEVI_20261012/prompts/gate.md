你是 DD 管線 v20 的判斷層閘（gate），標的 LEVI（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

## 任務

依 bundle 內 `gate_card.md` 的 ①–⑧ checklist 逐條複核 `judgment.json`，只揪判斷級的錯，不判斷寫得好不好。判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級問題（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡；無實質問題給 🟢。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：`gate_card.md`（①–⑧ checklist 全文與 🔴／🟡／🟢 口徑）、被引用事實與負向條目子集（核對 `fact_refs` 用）、`scenario_meta.json`（情境樹權威值，對帳 `decision_inputs.irr_base_pct`／`ev5y_pct` 用）、`judgment.json` 全文（被審對象，原樣）。

## 禁

- 禁 WebSearch／WebFetch、禁開 bundle 以外任何檔（包含 `docs/dd/`、`.dd_build/` 下的其他產物）。
- 禁跑任何腳本（`validate_judgment.py`／`dd_decision.py`／`dd_scenario.py` 已在判斷端跑過，機械層不歸你）。
- 禁提整段改寫判斷、禁自己動手修補 `judgment.json`——你只出稽核，修補是另一支流程的事。
- 證據包裡沒有的東西不得臆測補白，只講證據包內找得到依據的話。


===== BUNDLE =====

## ① gate_card.md（判斷層閘卡）

<!-- source: scripts/dd_prompts/gate_contract.md sha256:90928128665c694a; .claude/skills/stock-analyst/references/critic-gates.md sha256:8dff4ac45280acfd git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

你是 DD 管線 v20 的判斷層閘（gate），sonnet，單輪、無工具。你未參與寫判斷，這是一次跨模型冷讀。
輸入：`judgment.json`（待審判斷物）＋ `facts.json`（事實表，每軸 finding 帶 source／as_of／direction）。
任務只有一件：依下列 checklist 逐條複核 `judgment.json`，只揪**判斷級**的錯，不判斷寫得好不好。
判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡。
禁 WebSearch／WebFetch、禁讀輸入以外任何檔、禁改 `judgment.json`，只出稽核清單。

## checklist（①–⑧ 全出，不得跳號、不得「同上」帶過）

① 競爭惡化——份額流失／新進入者／客戶 second-source／大客戶轉單。查 facts.json 對應軸（competitive_share_entrants／customer_second_source／customer_concentration_credit）裡負向、或應被引用的 finding，核對 judgment.json 的 `moat.threats`／`moat.competitors`／`contradictions[]`／`decision_inputs.bear` 是否接住；被引用=N 卻是負向的 finding 即漏接。[gate_contract §①]

② 供需 durability——緊缺或過剩是結構還是週期，供給可逆性是否寫進 bear 機率。facts.json 的 supply_demand_durability 軸負向 finding，若未被引用且未列 `evidence_dismissed`，須在 `premortem`／`decision_inputs.bear` 找到對應處理，找不到即 🔴。[gate_contract §②]

③ 其他結構變數（開放軸）——法規／政策／關稅／反壟斷／補貼、通路重構、商業模式轉移、替代技術、客戶結構轉移。找 facts.json 覆蓋總覽裡「有 finding 卻沒人接住」的軸，對照 `contradictions[]`／`premortem.blind_spots`／`triggers[]`；閘禁搜尋，不重新查有沒有漏掉的產業變化。[gate_contract §③]

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。判斷寫「不追／等價格」而裁決是進場、`decision_inputs.wait_for_price` 卻沒填 true ＝ 矛盾；填了 true 時裁決落觀望是規則結果，不算矛盾，只看 `wait_for_price_condition` 是否具體可驗。[gate_contract §④]

⑤ 覆蓋面掃描（強制）——facts.json 逐軸點名 status="none"／"not_applicable" 的每一軸：理由站得住嗎？查詢是否切題且足以支撐該軸結論（不以查詢次數計）？**缺軸本身即 🔴，不需先證明結論錯**。[gate_contract §⑤]

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤，缺軸本身即 🔴。
(b) 量化模組完整性抽查：ROIC×再投資率真算與否、內生天花板對帳共識 CAGR、情境樹 Bull/Base/Bear EPS 價差是否實質、IRR 內部對帳，做法同 checklist ⑥。
(c) 數字可回溯：判斷引用的歷史數字逐一核對 facts.json 原文的期間與單位；反證條目要查採納理由與後果是否成立，不能只因編號存在就算過。[gate.md.tmpl 2026-09-11 註腳]

## 🔴／🟡／🟢 口徑

判斷級 🔴 限下列三種形狀：

1. **證據包已有而判斷未接**——證據包內存在的 finding／數字，判斷物完全沒接進 `contradictions`／`moat.threats`／`premortem`／`triggers`／`thesis.R`，也沒寫進 `evidence_dismissed[]`；
2. **算術或機率防線失守**——推導不可複算、內部恆等式不對帳、情境樹退化、機率與其自身依據矛盾；
3. **裁決與自身輸入矛盾**——`decision_inputs`／`scenario_meta`／`decision_out` 三者互斥，或裁決與判斷物自己寫下的理由相反。

**資料級不算 🔴**（證據包本身缺料、來源不夠新、某軸查不到）——那是 Stage 0 的問題，最多給 🟡 並在附註點名。無實質問題給 🟢；有實質但不改裁決方向的給 🟡。

## 輸出格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```


---

## ②b 被引用的事實與負向條目（v19；閘要查數字時不必猜）

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_net_revenues_gaap`（q1_business）｜Net revenues (GAAP)＝1609.7 US$M（YoY +4.3% 報告、+4.5% 有機；去年同期 1,543.4）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_kpi1_adjusted_ebit`（q1_business）｜Adjusted EBIT＝248.7 US$M（利益率 15.5%，去年同期 11.8%）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝222.3 US$M（利益率 13.8%，去年同期 10.8%）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_kpi3_gross_margin`（q1_business）｜Gross margin＝66.2 %（YoY +450bps，去年同期 61.7%）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_kpi4_adjusted_diluted_eps`（q1_business）｜Adjusted diluted EPS＝0.48 US$｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
  - 註記：consensus 0.36（來源：EarningsWhispers，非 IR；僅供參考）
- `f_kpi8_fy2026_guidance_2026_10_`（q1_business）｜FY2026 guidance（2026-10-07 更新）＝報告營收 ~+7.0%；有機 ~+6.0%；毛利率 +130bps；adj EBIT margin ~12.1%；稅率 ~23%；adj EPS 1.54–1.56 text｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-07 date｜期間與口徑：2026-10-07／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-07）
- `f_peer_levi_gross_margin_pct`（q2_moat）｜LEVI 毛利率＝61.72 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEVI.gross_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_levi_operating_margin_pct`（q2_moat）｜LEVI 營業利益率＝11.06 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEVI.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_levi_fcf_margin_pct`（q2_moat）｜LEVI FCF 利潤率＝8.46 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEVI.fcf_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ktb_gross_margin_pct`（q2_moat）｜KTB 毛利率＝48.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KTB.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ktb_operating_margin_pct`（q2_moat）｜KTB 營業利益率＝12.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KTB.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ktb_fcf_margin_pct`（q2_moat）｜KTB FCF 利潤率＝13.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KTB.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pvh_gross_margin_pct`（q2_moat）｜PVH 毛利率＝58.78 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PVH.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pvh_operating_margin_pct`（q2_moat）｜PVH 營業利益率＝8.05 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PVH.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gap_gross_margin_pct`（q2_moat）｜GAP 毛利率＝43.26 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GAP.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gap_operating_margin_pct`（q2_moat）｜GAP 營業利益率＝10.99 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GAP.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rl_gross_margin_pct`（q2_moat）｜RL 毛利率＝70.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rl_operating_margin_pct`（q2_moat）｜RL 營業利益率＝16.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.54 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.71 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.98 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（1.54 → 1.54）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（1.71 → 1.71）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（1.98 → 1.98）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_kpi5_adjusted_free_cash_flow`（q1_business）｜Adjusted free cash flow＝44.3 US$M（去年同期 -39.4；年初至今 427.3）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_kpi6_stock_based_compensation`（q1_business）｜Stock-based compensation（年初至今 9 個月）＝58.8 US$M（新聞稿未揭露單季，亦未直接給占營業利益％）｜期間與口徑：Q3 FY2026（季末 2026-08-30，公告於 2026-10-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Exhibit 99.1 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0000094845/000009484526000048/exhibit991-3q2026pressrele.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-08-30，公告於 2026-10-07））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.07 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝18.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.102 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝18.7 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝12.14 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 1.54，分子＝快照價 18.7｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝12.3 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝6.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝6.7 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝18.8 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.31 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝9.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝9.6 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 1.54 → 1.54（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-16.76 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝30.69｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：FY2024 10-K：公司已開始整併合約製造商數量（供應端集中度風險，非客戶端 second-source）。
  - 來源：Levi Strauss & Co Form 10-K FY2024（as_of 2025-01-31）｜affects：thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2015 10-K 風險因素：與批發客戶無長期合約、採逐單採購；主要批發客戶破產或財務惡化可能造成營收重大損失。
  - 來源：LEVI STRAUSS & CO - Form 10-K - FY2015 (SEC EDGAR)（as_of 2016-01-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-Q：多數產品產地（孟加拉、柬埔寨、巴基斯坦、越南）曾受被廢除的 IEEPA 關稅，且受新的預期關稅約束。
  - 來源：LEVI STRAUSS & CO Form 10-Q FY2026（as_of 2026-10-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：產業面：2026-02 IEEPA 被推翻後改為暫時性 10% Section 122 關稅（至 2026-07-24），其後 Section 301 新關稅（10%–12.5%、逾 80 國）自 2026-07-24 起；單一倡議團體來源，需對照官方公告。
  - 來源：Business & Human Rights Resource Centre: tracking the impact of forced labour tariffs on apparel footwear supply chains（as_of 2026-07-24）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：二手來源稱主要供應商國家含孟加拉、柬埔寨、埃及、巴基斯坦、斯里蘭卡、越南，2025年4月受10–49%對等關稅；第三方估年化關稅成本$25–30M（非公司數字）
  - 來源：Simply Wall St narrative（搜尋摘要）（as_of 2025-04-02）｜affects：thesis.R、decision_inputs.bear
- `channel_business_model_shift#0`（channel_business_model_shift｜方向 -｜狀態 ok）：FY2026 Q3：DTC 淨營收僅 +2%（報告與有機），占總營收 45%，管理層稱 DTC 低於內部預期，預期 Q4 中個位數成長；e-commerce +10%
  - 來源：Levi Strauss & Co. Reports Third-Quarter Results (Business Wire/Morningstar, 2026-10-07)（as_of 2026-10-07）｜affects：moat_trend、thesis.H、valuation

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":45.6,"bear_5y_price":15.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":65.5,"ev5y_pct":60.1,"irr_base_pct":10.6,"asym_ratio":6.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.54,"pe":12.14,"basis":"FY2026E 共識調整後 EPS（含 0.04 美元淨關稅退款），與終端倍數同為下一個會計年度的預估本益比口徑"},"eps":{"bull":[1.76,2.05,2.32,2.58,2.85],"base":[1.68,1.88,2.05,2.22,2.38],"bear":[1.5,1.52,1.55,1.58,1.62]},"pe":{"bull":16,"base":13,"bear":9.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.102,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEVI_Q2_2026_Earnings_Call_20260708.md
- 2026-07-08｜CFO｜guidance：全年調整後稀釋 EPS 指引上調為約 1.46–1.52 美元（原 1.42–1.48）（原話："range of approximately $1.46 to $1.52, up from"）
- 2026-07-08｜CFO｜guidance：全年有機營收指引上調為 +5.5% 至 +6%（帳面 +7% 至 +7.5%）（原話："7% to 7.5% and organic net revenues to be up 5.5% to 6%."）
- 2026-07-08｜CFO｜guidance：Q3 營收指引：帳面與有機皆 +4% 至 +5%，無匯率助益（原話："organic net revenues to be up 4% to 5% for the quarter"）
- 2026-07-08｜CFO｜guidance：Q3 調整後 EPS 指引約 0.34–0.36 美元，含稅率與匯率對毛利率的 0.02–0.03 美元逆風（原話："approximately $0.34 to $0.36, which includes a"）
- 2026-07-08｜CFO｜guidance：全年調整後 EBIT 利潤率指引 12%（原話："We expect adjusted EBIT margin to be 12% for the full year"）
- 2026-07-08｜CFO｜margin：全年毛利率指引：預期擴張約 10 個基點（原話："now expected to expand approximately 10 basis points"）
- 2026-07-08｜CFO｜guidance：指引的關稅假設：中國 30%、其餘 20%（原話："U.S. tariffs on imports from China at a 30% rate"）
- 2026-07-08｜CFO｜guidance：指引未計入潛在關稅退款（原話："does not assume any benefit from potential tariff refunds"）
- 2026-07-08｜CFO｜guidance：CFO 承認下半年指引隱含的放緩屬保守設定（原話："it is prudent. It is conservatism and it's probably"）
- 2026-07-08｜CFO｜margin：H2 EBIT 利潤率擴張集中在 Q4，並列出四項驅動（關稅基期、匯率壓力、A&P 正常化、重複配送成本減少）（原話："more pronounced in Q4 as we begin to lap the full impact"）
- 2026-07-08｜CFO｜margin：CFO 以 Q4 約 14% EBIT 作為口徑說明（回到 2024 年基期）（原話："let's say, circa it's about 14% EBIT"）
- 2026-07-08｜CFO｜margin：CFO 稱 Q4 2024 是 Q4 2026 的良好參照，因去年關稅拖累約 100 個基點以上（原話："Q4 '24 is a good proxy for Q4 2026"）
- 2026-07-08｜CFO｜margin：Q2 毛利率擴張 10 個基點至 62.7%（原話："expanded 10 basis points to 62.7%"）
- 2026-07-08｜CFO｜margin：Q2 調整後 EBIT 利潤率擴張 70 個基點至 9%（原話："adjusted EBIT margin expanded 70 basis points to 9%"）
- 2026-07-08｜CFO｜margin：CFO 拆解 Q2 SG&A 增幅：三分之一來自匯率（原話："1/3 of the SG&A increase was contributed by"）
- 2026-07-08｜CFO｜margin：營收成長中單位數與均價（AUR）的拆解：Q2 為 2/3 對 1/3（原話："2/3 of the growth was contributed by units and 1/3 by AUR"）
- 2026-07-08｜CFO｜guidance：全年單位數與 AUR 的貢獻預期改為約各半（Q1 約各半、2025 為 2/3 對 1/3）（原話："Our expectation for the year is more 50-50."）
- 2026-07-08｜CFO｜margin：管理層將 AUR 提升歸因於減少促銷與全價銷售占比提高（原話："reduced promotional levels and cost efficiency"）
- 2026-07-08｜CFO｜risk：關稅退款約 8,000 萬美元已付，管理層稱金額可觀但尚未決定如何處理（原話："We are not incorporating it in our guidance, but it's"）
- 2026-07-08｜CFO｜risk：關稅降稅對成本的利益因庫存周轉約 2 次而遞延，Q2 邊際、Q3 少量（原話："Q2 was marginal. Q3 will be a little bit"）
- 2026-07-08｜CEO｜risk：CEO 提及仍留意外部環境（原話："While we remain mindful of the external environment, the"）
- 2026-07-08｜CFO｜commitment：長期目標重申：營收 100 億美元與 15% 營業利潤率（原話："path to $10 billion in revenue and 15% operating margin"）
- 2026-07-08｜CFO｜commitment：全年淨新開店 50–60 家，多數落在下半年（原話："50 to 60 net new doors this year"）
- 2026-07-08｜CFO｜commitment：全年存貨金額預期略高於去年但低於銷售成長（原話："slightly above last year but below expected sales growth"）
- 2026-07-08｜CFO｜commitment：美國 Hebron 配送中心移交 Maersk 預計於 Q4 初完成，進度較原計畫慢（原話："The transition has taken longer than planned as we"）
- 2026-07-08｜CFO｜commitment：CFO 說明延後 Hebron 關閉的額外成本僅數百萬美元（原話："The cost is a couple of millions"）
- 2026-07-08｜CFO｜commitment：全球 ERP 整合：歐洲與其餘拉美國家預計 2027 年中完成（原話："countries are on track for completion by mid-2027"）
- 2026-07-08｜CFO｜commitment：CFO 提到 ERP 完成後具備重新思考會計年度行事曆的基礎（原話："we have the foundation to get that to at least think through"）
- 2026-07-08｜CFO｜capital_allocation：資本配置架構：將自由現金流的 55%–65% 以上回饋股東（原話："at least 55% to 65% of free cash flow to shareholders"）
- 2026-07-08｜CFO｜capital_allocation：Q3 季度股利調升 0.02 美元至 0.16 美元（原話："quarterly dividend by $0.02 to $0.16 per share"）
- 2026-07-08｜CEO｜product：擴大後的可觸及市場（TAM）貢獻約三分之一營收成長（原話："roughly 1/3 of our top line growth in the quarter"）
- 2026-07-08｜CEO｜product：CEO 稱轉向全身丹寧生活風格使可觸及市場擴大 15 倍（原話："our addressable market by the tune of 15x."）
- 2026-07-08｜CEO｜product：CEO 引述丹寧品類預期成長速度（原話："grow mid-single digits annually through 2030"）
- 2026-07-08｜CEO｜product：Blue Tab 價位帶：下身 200–350 美元（原話："price points like in bottoms from $200 to $350"）
- 2026-07-08｜CEO｜product：CEO 稱 Blue Tab 長期規模可達 1–2 億美元以上（目前規模較小）（原話："there's no reason why this can't be $100 million, $200"）
- 2026-07-08｜CEO｜product：Beyond Yoga 開店處於早期，門市不到 20 家（原話："We have less than 20 stores"）
- 2026-07-08｜CEO｜customer：Signature 價值品牌 H2 預期加速至高個位數到低雙位數（原話："high single digits, low double digits"）
- 2026-07-08｜CFO｜customer：歐洲批發預訂單 H2 成長高個位數，用以支持全年歐洲中個位數成長（原話："high single-digit wholesale preorder growth for H2"）
- 2026-07-08｜CFO｜customer：歐洲 DTC H2（Q3、Q4）預期中到高個位數成長（原話："expect DTC to be mid- to high single digits"）
- 2026-07-08｜CEO｜customer：CEO 說明 Q2 超預期主要來自批發（原話："wholesale actually contributed more to the beat if you will"）
- 2026-07-08｜CEO｜customer：CEO 對中國市場的描述：回到成長的初步跡象（原話："we're encouraged by a return to growth and improving"）
- 2026-07-08｜CEO｜competition：CEO 針對促銷環境回應：Levi's 線上減少促銷、全價銷售增加（原話："more full-price selling"）

### 問答異常語氣（迴避／改口／保留）
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Vasilescu 問 Signature 前季高十位數、本季僅低個位數，是否反映價值型消費者疲弱｜答法：CEO 改以上半年合計 +9% 與下半年預期回答，未直接說明 Q2 低個位數的原因；CFO 於後段稱「largely timing」
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Boruchow 問營收超預期約 300 基點、營業利潤率僅達指引高端的流量轉換不足｜答法：CFO 回應轉向毛利率、SG&A 三分之一來自匯率與上半年調整後口徑，未直接量化流量轉換缺口
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Toscano 問上季所述 3,500 萬美元關稅成本利益與 0.07 美元 EPS 是否已在 Q2 顯現、Q3 預期｜答法：CFO 稱 Q2 邊際、Q3 少量，未給數字；關稅退款 8,000 萬美元稱「substantial」但表示尚未決定如何處理
- LEVI_Q2_2026_Earnings_Call_20260708.md｜問：Kogan 追問季初至今（QTD）表現是接近 Q2 還是符合 Q3 指引 4%–5%｜答法：CFO 表示不提供季中更新，僅稱趨勢支持 Q3 與全年指引、無明顯需求變化，未給量化比較

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | none | 0 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 5 | 3 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 1 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **competitive_share_entrants**（none）：Levi Strauss market share gaining 2026；Levi Strauss new entrant OR competitor denim threat 2026 American Eagle Gap Abercrombie；Levi Strauss vs apparel peers market share trend 2025 2026 Circana jeans
- **regulatory_antitrust**（none）：Levi Strauss antitrust OR monopoly investigation 2026；Levi Strauss regulation OR regulatory scrutiny apparel tariffs 2026；Levi Strauss DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）：Levi Strauss denim substitute threat athleisure 2026；denim industry alternative technology disruption 2026 2027 waterless dye laser finishing

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260522","verdict":"B（衛星候選，分批 + 等回測 Bollinger 中軌 $20.88 或 Fwd PE 13x ~$19.50）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"DTC 通路（含 e-commerce）持續擴張並成為主導通路 + ASP 結構性提升驅動 GM 維持在 60%+","columns":{"2Y 驗證點":"DTC channel 占比從 52% 升至 55% by FY27；DTC comp sales +5% YoY","5Y 驗證點":"DTC 占比達 60% by FY30；e-commerce 占 DTC 30%+","10Y 驗證點":"DTC + 直營實體 占 70%；批發降至 30%","具體數字門檻":"FY26 DTC: 52% → 55% (FY27) → 60% (FY30)；GM 維持 ≥ 60%","信息來源":"Q1 FY26 法說會 + 2024 Investor Day 公司公開目標","漂移觸發條件":"連 2 季 TTM DTC growth"}},{"id":"H2","text":"Beyond Yoga 成功放大成女裝 / athleisure 第二曲線，年化從 $170M 達 $500M by FY28","columns":{"2Y 驗證點":"Beyond Yoga 年化 ≥ $250M by FY27；organic growth ≥ +20% YoY","5Y 驗證點":"達 $500M-$700M by FY30；國際擴張啟動（歐洲 / 亞洲）","10Y 驗證點":"Beyond Yoga 為 $1B+ 獨立次品牌，貢獻集團 12-15% revenue","具體數字門檻":"當前年化 ~$170M（Q1 FY26 $43.3M × 4）→ $250M (FY27) → $500M (FY30)","信息來源":"Q1 FY26 earnings call + 公司分項披露","漂移觸發條件":"連 2 季 organic"}},{"id":"H3","text":"Project Fuel 重組 + 通路升級 + Dockers 出售後，集團 Adj EBIT margin 從 11.3% (FY24) 擴張至 13% (FY28) → 估值倍數從 14.5x → 17x","columns":{"2Y 驗證點":"FY26 Adj EBIT margin ≥ 12%（公司 guidance）；FY27 ≥ 12.5%","5Y 驗證點":"FY28-30 達 13-14%（peer-leading）","10Y 驗證點":"持續維持 13%+ 是 brand-led 的證明","具體數字門檻":"Adj EBIT margin: FY24 11.3% → FY26E 12% → FY28E 13%","信息來源":"FY26 raised guidance + Q1 法說會明確 path","漂移觸發條件":"連 2 季 Adj EBIT margin 年化"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Denim 品類降溫，athleisure / leggings 在 2027-2028 強勢回歸","columns":{"對應假設":"H1, H2","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Lululemon / Alo / Vuori 季 YoY 成長 vs LEVI 季 YoY；NPD 數據 denim share 走勢","警戒閾值":"連 4 季 LEVI vs Lulu growth spread > 15pp 不利"}},{"id":"R2","text":"Tariff 升級（China 60% / Vietnam 35% / Mexico 25%）超 FY26 guidance 假設","columns":{"對應假設":"H3","時間尺度標記":"⚡ 短期（1-2 季）","監測指標":"季度 GM trajectory；公司 tariff 註腳更新；川普 / 國會貿易政策進展","警戒閾值":"連 2 季 GM YoY 壓縮 > 200bp 且公司歸因 tariff"}},{"id":"R3","text":"Beyond Yoga 整合 / 擴張失敗，第二曲線失速","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年）","監測指標":"Beyond Yoga 季 organic growth；DTC vs wholesale mix；公司是否將其 spin out","警戒閾值":"需 ≥ 50% 機率才砍倉；連 4 季 organic"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":21.75,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LEVI","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Levi Strauss & Co."},"oneliner":"預估本益比 12 倍、殖利率 3.1% 買到丹寧龍頭的利益率擴張；Q3 美歐直營失速與配送中心延宕是真瑕疵，勝負在 2027 年 1 月財測能否守住 12.1% 利益率新基期。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球消費者為 Levi's 品牌與版型付的溢價，錢卡在品牌與通路兩個節點：直營占營收四成五到五成、其餘走批發。最新一季營收 16.1 億美元、年增 4%（有機 5%），毛利率 66.2%（剔除關稅退款約 62.5%），調整後 EBIT 利益率 15.5%（剔除後約 12.2%）。","reasoning":"分區：Q3 美洲 +2%（拉美 +10%，美國直營拖累）、歐洲 +5%、亞洲 +10%；通路：批發 +6%、直營 +2%（占 45%）、電商雙位數。營收分部占比事實表未涵蓋，只能用成長率判讀。Q3 調整後 EPS 0.48 美元含 0.11 美元關稅退款淨效益，剔除後年增 9%，來自利益率擴張與回購。產業時鐘判在擴張期：丹寧品類管理層與第三方都估年增低至中個位數，公司年內三度上調 EPS 財測，但 CEO 承認競爭轉強、Q3 動用節慶促銷，尚未到過熱。供需持久性：品類需求屬結構性慢成長，版型週期（寬鬆轉低腰）造成的份額移動可逆；上游丹寧布產能過剩對品牌端是成本順風。單點依賴：無單一客戶達營收 10%，前十大批發客戶占比 FY2025 為 24% 且逐年下降；供應端約 32 國、單一國家不超過 30%，集中度風險低，但公司已開始整併代工家數。","fact_refs":["f_kpi0_net_revenues_gaap","f_kpi1_adjusted_ebit","f_kpi2_gaap_operating_income","f_kpi3_gross_margin","f_kpi4_adjusted_diluted_eps","f_kpi8_fy2026_guidance_2026_10_","f_earnings_recency"],"verdict_values":{"revenue_quality":"有機成長 5%，量價並進（2026-07-08 CFO：全年單位數與均價貢獻約各半）；Q3 有 7,860 萬美元關稅退款一次性墊高利益率與淨利，約四分之三再投入行銷、物流與促銷，全年淨效益僅 0.04 美元 EPS。","unit_econ_note":"亞洲營業利益率年初至今 16.7%（+240bp），規模擴大帶動利益率；美國配送中心雙軌運行加火災推高物流成本，Hebron 已於 Q3 末關閉，效益延至 2027 年。門市層級獲利數字事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"成熟品牌、毛利率六成、營收中個位數成長、EPS 成長倚賴利益率修復與回購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性慢成長、份額週期可逆：丹寧品類管理層稱至 2030 年每年中個位數成長，第三方估值分歧但多為低至中個位數；印度丹寧布產能過剩約 20–25%（來源未標日期）壓低布料成本；版型潮流造成的流量轉移屬短週期，可逆性高。","bargaining":{"up":"對上游強：約 32 國獨立代工、單一國家不超過 30%；但公司正整併代工家數，上游議價力可能小幅回升。","down":"對下游中強：前十大批發客戶占比由 FY2023 27% 降至 FY2025 24%，無單一客戶達 10%；但與批發客戶無長期合約、逐單採購。","geo":"主要產地為孟加拉、柬埔寨、巴基斯坦、越南，受 2026-07-24 起 Section 301 新關稅約束；中國占產量約 1%。"},"profit_pool_dir":"品牌端利潤池擴大：毛利率 FY2022 57.5% 升至 FY2025 61.7%，直營擴張把原屬零售商的價差收回；關稅是政府從利潤池抽成的新變數，IEEPA 被推翻後改為 Section 301。","tam_table":[{"item":"全球丹寧市場（第三方一）","value":"2024 年底約 867 億美元，預估 2030 年 1,217.6 億美元（市調報告，非共識）"},{"item":"全球丹寧市場（第三方二）","value":"2026 年約 914 億美元、年複合 5.48%；另一來源 1,031.6 億美元，口徑分歧"},{"item":"品類成長（管理層）","value":"2026-07-08 CEO：丹寧品類至 2030 年每年中個位數成長"},{"item":"可觸及市場擴大","value":"2026-07-08 CEO：轉向全身丹寧生活風格使可觸及市場擴大 15 倍（管理層說法，未經第三方驗證）"},{"item":"高端丹寧滲透","value":"超高端丹寧市占不到 1%（2026-10-07 CEO；Q2 法說稱 0.4%），Blue Tab 價位 200–500 美元"},{"item":"利潤池占比 5 年前→現","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河持平，等級 B：美國男女裝與青少年丹寧第一的品牌定價權撐住六成毛利，但直營與物流執行拖累利益率，營業利益率對同業並不領先。","reasoning":"機制是品牌與版型話語權：TTM 毛利率 61.7%，高於 PVH 58.8%、KTB 48.2%、GAP 43.3%，僅次 RL 70.3%；但營業利益率 11.1% 與 KTB 12.0%、GAP 11.0% 相當，FCF 利益率 8.5% 低於 KTB 13.6%，代表品牌溢價被直營門市與物流成本吃掉。定價權評 8：Q3 同業降價時公司沒有降價，只在節慶檔促銷；Q2 法說稱均價上升來自減少促銷與全價銷售。執行評 6：Q3 直營只成長 2%、美國返校檔行銷主打寬鬆版型失準、配送中心轉換延宕又遇火災、任期 14 年的 CFO 交接。方向：執行面縮減、定價面穩定，綜合判持平而非下滑——批發 +6%、亞洲 +10%，管理層稱美國男女裝份額擴大（未經第三方驗證）。同業 ROIC 事實表未涵蓋，無法做報酬差，故不給 8 分以上。","fact_refs":["f_peer_levi_gross_margin_pct","f_peer_levi_operating_margin_pct","f_peer_levi_fcf_margin_pct","f_peer_ktb_gross_margin_pct","f_peer_ktb_operating_margin_pct","f_peer_ktb_fcf_margin_pct","f_peer_pvh_gross_margin_pct","f_peer_pvh_operating_margin_pct","f_peer_gap_gross_margin_pct","f_peer_gap_operating_margin_pct","f_peer_rl_gross_margin_pct","f_peer_rl_operating_margin_pct","f_kpi3_gross_margin"],"verdict_values":{"moat":{"mechanism":"品牌與版型話語權：丹寧品類第一的心智占有讓公司不必降價，並把品牌延伸到上身、高端 Blue Tab 與亞洲市場。","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價面穩定：毛利率 FY2022 57.5% 到 FY2025 61.7% 連升，Q3 剔除退款仍 +80bp、未降價；執行面縮減：直營 Q1 +16%、Q2 +11%、Q3 +2% 連續減速，物流效益延後。兩向抵銷，判持平。","competitor_notes":[{"name":"KTB","strategy_note":"Wrangler 與 Lee 母公司，毛利率低十多個百分點但營益率與自由現金流率較高，走批發為主的輕資產路線，是丹寧的直接對手。"},{"name":"PVH","strategy_note":"Calvin Klein 與 Tommy Hilfiger，毛利率接近但營益率低約 3 個百分點，顯示同樣的品牌溢價沒能留到營業利益。"},{"name":"GAP","strategy_note":"大眾價位自有通路，毛利率低近兩成，營益率與 LEVI 相當，代表通路效率可以彌補品牌溢價差距。"},{"name":"RL","strategy_note":"高端生活風格品牌，毛利率與營益率皆最高，是 LEVI 用 Blue Tab 往高端延伸要追的標竿。"}],"peer_na_reason":"同業 ROIC 與研發占比事實表未涵蓋，只能用毛利率、營業利益率、FCF 利益率三軸對照。","threats":[{"level":"🟡","text":"丹寧競爭加劇與新進者（2026-10-07 CEO 自述），低腰版型潮流中公司一度失準，迫使行銷與促銷費用上升；點對點競爭，不扣分。","p":"35%","evidence_refs":[]},{"level":"🟡","text":"代工廠整併：供應端集中度上升，大型代工的議價力可能提高，壓縮產品成本下降空間。","p":"20%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"關稅改制：主要產地孟加拉、柬埔寨、巴基斯坦、越南受 Section 301 新關稅約束，退款屬一次性，後續稅率由政策決定。","p":"50%","evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟢","text":"丹寧是耐久品類，管理層與第三方都估至 2030 年低至中個位數成長；使用者、決策者、付款者多為同一消費者，轉換鏈短。版型潮流（寬鬆轉低腰）改變的是品類內份額而非品類需求，Q3 美國批發仍正成長即為證據。"},{"item":"決策層級","level":"🟡","text":"替代性在單一版型與檔期層級就會發生：Q3 返校檔主打寬鬆版型失準，流量在兩個月內轉弱；但全價銷售比例提高、均價上升且未跟隨降價，顯示品牌層級的忠誠度仍在。轉換成本低，靠持續的版型創新與行銷維持。"},{"item":"價值鏈分配","level":"🟢","text":"品牌環節拿走最大一塊：毛利率六成以上，代工分散於約 32 國、單一國家不超過 30%，前十大批發客戶占比逐年下降至 24%；直營占比四成五到五成，把零售價差收回。風險是代工整併與關稅抽成。"},{"item":"社會容忍度","level":"🟢","text":"服飾非必需品，不存在政治性的價格天花板，也不依賴監管授權；政策風險集中在關稅，已列為風險而非社會容忍度問題。"}],"roiic":"事實表未涵蓋（缺投入資本口徑，無法計算增量報酬）","reinvest_rate":"事實表未涵蓋；2026-07-08 CFO 稱自由現金流至少 55–65% 回饋股東，可推知留在公司的自由現金流不超過約四成五（與定義的再投資率口徑不同）","endo_ceiling":null,"formula_note":"當期 ROIC 需稅後營業利益率×投入資本周轉率，事實表只有利益率、缺投入資本，象限無法判定；只能確認高毛利、營業利益率約 11–12%。成長主要靠利益率擴張與回購，而非新增資本，屬高報酬低再投資型。"}}}},"q3_growth":{"verdict":"跑道中等：丹寧主業是年增中個位數的成熟品類，第二曲線（上身品類、Blue Tab、亞洲直營）有成長證據但規模仍小、主要靠管理層說法；共識 EPS 成長高於營收的部分來自利益率擴張與回購，可歸因但時程已見延後。","reasoning":"三年共識 EPS：FY2026E 1.54、FY2027E 1.71、FY2028E 1.98 美元，近三個月零修正。以 FY2025 GAAP 稀釋 EPS 1.45 為基期，三年年增約 10.9%；以 FY2026E 為起點，兩年年增約 13.4%。營收面 FY2026 有機約 6%，管理層長期框架為中個位數。缺口約 5–7 個百分點，歸因利益率擴張（12.1% 走向 15% 目標）與淨回購，屬可歸因；但 7 月法說稱 Q4 約 14% 利益率、10 月指引剔除退款只剩約 13.2–13.4%，路徑已延後。基期口徑注意：FY2025 淨利 5.78 億美元較 FY2024 2.11 億美元跳升，與營業利益率變化不成比例，疑含非營業項目，事實表未拆分，10.9% 可能低估調整後口徑成長。十項衰退信號亮一項（EPS 成長明顯快於營收），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi8_fy2026_guidance_2026_10_","f_kpi0_net_revenues_gaap"],"verdict_values":{"growth":{"driver_mix":"量與價約各半（2026-07-08 CFO：全年單位數與均價貢獻約 50／50），疊加利益率擴張與小幅淨回購；無併購，Dockers 為出售。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法以事實表算出（缺投入資本與增量報酬）。結構推論：營收中個位數成長所需再投資不高，自由現金流過半配回股東；共識 FY2026→FY2028 EPS 年增約 13% 高出營收成長的部分來自利益率擴張與回購，而非再投資驅動，故視為超出內生成長。","segments":[{"item":"美洲（Q3）","value":"營收 +2%，拉美 +10%；營業利益率 29.9%（含退款淨效益，+640bp）"},{"item":"歐洲（Q3）","value":"營收 +5%，批發雙位數；營業利益率 22.8%（+150bp）；2027 春夏批發預訂高個位數成長"},{"item":"亞洲（Q3）","value":"營收 +10%，連三季雙位數；營業利益率 14.2%（+220bp），年初至今 16.7%"},{"item":"品牌","value":"Levi's 品牌 +4%、Signature +13%、Beyond Yoga +9%；Blue Tab 雙位數成長但規模小"},{"item":"通路","value":"批發 +6%、直營 +2%（占 45%）、電商雙位數；管理層預期 Q4 直營中個位數"},{"item":"品類","value":"丹寧下身以外品類貢獻 Q3 約一半成長，上身 +7%、女裝上身 +10%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 +10bp、Q3 +450bp（剔除退款 +80bp）"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱美國男女裝份額擴大，未經第三方驗證"},{"item":"提價後銷量下滑","lit":false,"note":"Q2 批發量增、全年量價約各半"},{"item":"EPS 成長顯著高於營收成長（差距>5pp）","lit":true,"note":"共識 EPS 年增約 11–13% 對營收中個位數"},{"item":"FCF／淨利<0.75 連 2 年","lit":false,"note":"FY2024 3.19 打斷；FY2025 0.53 單年偏低，監測"},{"item":"SBC／營收>5% 且上升","lit":false,"note":"前九月 SBC 5,880 萬美元，約營收 1% 出頭"},{"item":"TAM 萎縮或被替代","lit":false,"note":"第三方與管理層皆估品類成長"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋，無法判定"},{"item":"維持性資本支出占 FCF>60%","lit":false,"note":"事實表未涵蓋"},{"item":"停止投資新產能且收入下滑","lit":false,"note":"全年淨新增 50–60 家門市，營收成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上：自由現金流過半配回股東，Q3 股利年增 11%，另以 1 億美元加速回購；但近四年自由現金流對淨利的轉換很不穩定。","reasoning":"FCF／淨利：FY2022 −0.07、FY2023 0.49、FY2024 3.19、FY2025 0.53（年報 FCF÷淨利），波動大；FY2025 淨利跳升疑含非營業項目，轉換率可能被低估。Q3 調整後自由現金流 4,430 萬美元（去年同期 −3,940 萬），年初至今 4.27 億美元。SBC 前九月 5,880 萬美元，年化約 7,800 萬美元。回饋政策：2026-07-08 CFO 稱至少把自由現金流的 55–65% 回饋股東，Q3 季股利調升至 0.16 美元，Q3 發出股利 6,200 萬美元。現金去向四分（再投資、併購、股利、回購）與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi5_adjusted_free_cash_flow","f_kpi6_stock_based_compensation","f_ps_current","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表內近年資本動作是出售 Dockers（賣方），無新收購可評增量報酬"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"加速回購約在 18.7 美元執行，對應 FY2026E 盈餘殖利率約 8.2%（1.54÷18.7）；10 年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 7,800 萬美元；市值以 P/S 1.07 倍×FY2025 營收 62.8 億美元粗估約 67 億美元，毛稀釋約 1.2%／年，扣除回購後淨稀釋更低，低於 1.5%"}],"grade":null},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自有機營收與利益率，不靠併購；回饋政策與本季股利、回購數字已寫在判斷理由"}}}},"q5_valuation":{"verdict":"現價只要求利益率守在 12% 上下、EPS 每年中個位數成長就划算：12 倍預估本益比加 3.1% 殖利率，大致已把利益率不再擴張定價進去。我信這個下限，但不信 15% 利益率會準時到，所以只用 13 倍與低於共識的 EPS 估值。","reasoning":"FY2026E 共識 1.54 美元對應 12.1 倍，trailing 12.3 倍落在近四個年度端點 6.7 百分位，P/S 與 EV/S 也在 9.6–18.8 百分位，處近年低檔。PEG 以三年 EPS 年增 10.9% 計約 1.11。短期上檔：FY2027E 1.71 美元×13 倍約 22.2 美元，+19%；中期：基準 FY2031E 2.38 美元×13 倍約 30.9 美元，+65%。賣方目標價平均約 26–28 美元、區間 14–34 美元（高低比約 2.4 倍），7 月底有一家降評至持有、目標 25 美元；我們的 12 個月估值低於賣方均值，支持分批而非追價。分母 FY2026E 含 0.04 美元淨關稅退款，剔除後 1.50–1.52 美元、倍數 12.3–12.5 倍，不改結論。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"預估本益比（FY2026E 共識調整後 EPS 1.54 美元）搭配 PEG 與殖利率","tier":"成熟服飾品牌","peers":{"expanded":false,"reason":"事實表同業對照只有毛利率、營業利益率、FCF 利益率，沒有倍數；同業本益比事實表未涵蓋"},"fwd_pe":12.14,"peg":1.11,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"預估本益比 12.1 倍、trailing 12.3 倍在近四個年度端點 6.7 百分位，P/S 18.8、EV/S 9.6 百分位；PEG 1.11 合理偏便宜；殖利率 3.1%。事實表只有年度端點分位、沒有五年連續序列，故五年分位留空不外推。","upside_short_pct":19,"upside_mid_pct":65,"denominator_disputed":false,"denominator_note":"FY2026E 含 0.04 美元淨關稅退款，剔除後 1.50–1.52 美元，倍數約 12.3–12.5 倍，便宜結論不變。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 Q3 直營失速當成天氣與單一檔期的一次性問題，而它其實是版型週期轉換下品牌熱度降溫的開端；其次是利益率新基期守不住。價值陷阱風險中等。","reasoning":"依據見反證紀錄三條：論點失敗（直營連三季減速、競爭加劇）、股東經濟變差（行銷與物流費用常態化）、價格已反映太多（反駁）。26 週股價下跌 16.8%、RSI 30.7，市場已部分反映直營疑慮。十項衰退信號亮一項：EPS 成長明顯快於營收。管理層 7 月對 Q4 利益率與配送中心時程的說法，到 10 月均已下修，對其一次性歸因採未證、監測處理。","fact_refs":["f_week26_return_pct","f_rsi14","f_kpi0_net_revenues_gaap","f_kpi1_adjusted_ebit"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退信號亮燈：EPS 成長明顯快於營收，倚賴利益率擴張"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.54,"pe":12.14,"basis":"FY2026E 共識調整後 EPS（含 0.04 美元淨關稅退款），與終端倍數同為下一個會計年度的預估本益比口徑"},"eps":{"bull":[1.76,2.05,2.32,2.58,2.85],"base":[1.68,1.88,2.05,2.22,2.38],"bear":[1.5,1.52,1.55,1.58,1.62]},"pe":{"bull":16,"base":13,"bear":9.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.1,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-45,"hi":-25,"basis":"下緣 −45%：FY2026E EPS 打七五折（參照 FY2022 到 FY2023 GAAP EPS 由 1.41 降到 0.62 的衰退期，取溫和版）乘 9 倍約 10.4 美元；上緣 −25%：直營失速使 EPS 打九折、倍數壓到 10 倍約 14 美元。現價已在近四年估值低檔，倍數再壓縮空間有限，下緣不取 −50% 以上。","trigger_time":null},"basis":{"bull":"直營回到高個位數、亞洲與 Blue Tab 放大，FY2030 前達 15% 營業利益率；倍數回到 16 倍（前份論點曾設 17 倍，同業倍數事實表未涵蓋，以自身歷史年度端點為錨）","base":"有機營收年增 4–5%、利益率每年擴張約 40–50bp（FY2028 約 13%，低於共識隱含路徑）、淨回購 0.5%；倍數 13 倍＝前份分批價位所用倍數，略高於現值 12.1 倍","bear":"美國直營續弱、Section 301 關稅與促銷常態化，利益率停在 11–12%，EPS 年增約 1%；倍數 9.5 倍取成長熄火至 10% 以下時的壓縮錨，低於近四個年度端點"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 直營只成長 2%（Q1 +16%、Q2 +11%），CEO 承認丹寧競爭加劇、有新進者，美國返校檔需靠重拍廣告與促銷救流量；FY2022 到 FY2023 GAAP EPS 曾由 1.41 降到 0.62。","assumption":"直營失速是歐洲天氣與美國單一檔期行銷失誤，九月已回正。","consequence":"若是品牌熱度轉弱，利益率卡在 11–12%、倍數壓到 9 倍，五年報酬可能接近 −40%。","ruling":"部分採納：一次性歸因未證，熊市機率設 30%。與唯一致命點（FY2027 利益率指引）部分重疊——直營失速是利益率失守最可能的成因，已合併進清倉條件監測。","watch":"Q4 FY2026 全球與美國直營年增；2027-01 財測","not_applicable_reason":null,"evidence_refs":["channel_business_model_shift#0"],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi4_adjusted_diluted_eps"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 表明行銷費率已在 7% 以上、未來還要加碼；配送中心雙軌成本與火災使效益延至 2027；公司同時整併代工家數，供應端集中度上升。","assumption":"營收與毛利率達標，但為維持品牌熱度須長期提高行銷與促銷，物流效益遲遲不到。","consequence":"營收成長達標而 EPS 只跟營收走，倍數無法上修，股東只拿到股息與小幅回購。","ruling":"採納為主要中期風險：基準路徑利益率只設到 FY2028 約 13%，低於共識隱含水準。","watch":"廣告占營收比例、調整後 SG&A 率（FY2026 指引約 51%）、Groveport 配送中心效率","not_applicable_reason":null,"evidence_refs":["customer_second_source#1"],"fact_refs":["f_kpi1_adjusted_ebit","f_kpi2_gaap_operating_income"]},{"view":"價格已反映太多","evidence":"共識 FY2028 EPS 1.98 美元（兩年年增約 13%）可能偏樂觀，12 倍的便宜可能建立在高估的分母上。","assumption":"現價已反映利益率走到 15%。","consequence":"若共識高估，便宜只是估值錯覺，下檔大於上檔。","ruling":"反駁：以我們低於共識的基準 FY2028 1.88 美元計，現價仍不到 10 倍；trailing 本益比在近四個年度端點 6.7 百分位、殖利率 3.1%，現價反映的是利益率停滯而非擴張。比較可能的錯誤方向是太悲觀。","watch":"預估本益比若回到 15 倍以上而 EPS 未上修，重評","not_applicable_reason":null,"evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_dividend_yield_ttm","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 21.75 → 本次 18.7（-14.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=21.75","side_b":"本次 price_at_dd=18.7","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 21.75 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 21.75 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 21.75 美元：Bull 價 45.6、Bear 價 15.39，五年期望值 +37.7%，基準年化 7.3%，不對稱比 3.12","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.12。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 21.75 美元：五年期望值 +37.7%，基準年化 7.3%，不對稱比 3.12","side_b":"本次情境、股價 18.7 美元：五年期望值 +60.1%，基準年化 10.6%，不對稱比 6.77","ruling":"再換股價、情境不動：起點價下跌 14.0%，五年期望值多 22.5 個百分點，基準年化多 3.3 個百分點，不對稱比由 3.12 升到 6.77。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：訊號與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-22，股價 21.75 美元）：訊號 B、估值便宜；等回測 20.88 美元或預估本益比 13 倍約 19.50 美元分批。","side_b":"本次股價 18.70 美元，已低於前份兩個分批價位；FY2026E 共識 1.54 美元對應 12.1 倍，估值結論仍為便宜，訊號維持 B。","ruling":"維持不升級：價格下跌讓估值更便宜，但同期出現直營失速、配送中心延宕、CFO 交接等新負面證據，兩者抵銷。","evidence_level":"事實表股價與共識","settle_metric":"2027-01 財報的直營年增與 FY2027 利益率指引","if_then":["若股價續跌至 16.50 美元以下而直營未觸發失速門檻，分批反買三分之一","若直營連 2 季年增低於 3%，停止加碼並減碼至半倉"],"evidence_refs":[]},{"axis":"前份漂移：舊格式未輸出的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份為舊格式，這些欄位皆為空值。","side_b":"本次：護城河持平、五年後跑道中等、類型為品質複利成長（次類轉機）、非循環股不判循環位置、最大回撤 −25% 到 −45%、多頭 25／空頭 30 機率；回撤與機率由程式從本次情境算出。","ruling":"屬方法變動，非基本面漂移；本次首度給值，後續以本次為比較基準。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價值陷阱判讀","cause":"方法變動","prior_field":["trap"],"side_a":"前份價值陷阱 🟢。","side_b":"本次 🟡：十項衰退信號中「EPS 成長明顯快於營收」亮燈（共識 EPS 年增約 11–13% 對營收中個位數）。","ruling":"結構本來就在，本次改用逐項清單才顯現；不代表基本面轉壞，代表 EPS 成長倚賴利益率擴張，已對應到利益率論點與唯一致命點。","evidence_level":"共識 EPS 與財測","settle_metric":"FY2027 利益率指引","if_then":["若 FY2027 指引利益率低於 12.1%，陷阱判讀升為 🔴 並減碼一半"],"evidence_refs":[]},{"axis":"行動門檻新設：重啟條件、清倉與減碼","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件、清倉門檻與減碼門檻（空值）。","side_b":"本次：清倉＝FY2027 EBIT 利益率指引低於 12.1% 且全球直營連 2 季年增低於 3%；減碼＝剔除關稅退款的毛利率連 2 季年減超過 100bp，或直營連 2 季低於 3%；重啟第二批＝2027-01 財報確認直營年增至少 4% 且指引至少 12.1%。","ruling":"新設，不沿用前份；理由是本季管理層首次給出 12.1% 新基期與直營中個位數承諾，可直接轉成可驗證門檻。","evidence_level":"2026-10-07 法說會","settle_metric":"2027-01 財報","if_then":["若兩項清倉條件同時成立，清倉","若僅一項成立，減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點。","side_b":"FY2027 財測的調整後 EBIT 利益率低於 2026-10-07 CFO 宣稱的 12.1% 新基期。","ruling":"新證據：CFO 明言 12.1% 為新基期、本年加碼的行銷與物流費用明年不會重複；這是終端 EPS 敏感度最大的單一變數，且在 2027 年 1 月以單一事件揭曉。","evidence_level":"2026-10-07 法說會 CFO 原話","settle_metric":"FY2027 EBIT 利益率指引","if_then":["若低於 12.1%，減碼一半","若至少 12.1% 且直營至少 4%，補第二批"],"evidence_refs":[]},{"axis":"假設與風險門檻改寫","cause":"新證據","prior_field":null,"side_a":"前份 H2＝Beyond Yoga FY2027 年化至少 2.5 億美元；R1＝連 4 季對 Lululemon 成長差超過 15pp；R2＝連 2 季毛利率年減超過 200bp 且歸因關稅。","side_b":"本次假設改為有機營收至少 4%、EBIT 利益率路徑、毛利率至少 61.7%；風險改為直營連 2 季低於 3%、剔除退款毛利率連 2 季年減超過 100bp。","ruling":"IEEPA 關稅已在 2026-02-20 被最高法院推翻並改為 Section 301 新關稅，舊 200bp 門檻對應的稅率情境已不存在；Beyond Yoga 本季 +9%、事實表無年化營收，無法驗證舊門檻，改追蹤整體利益率。","evidence_level":"10-Q 與 2026-10-07 法說","settle_metric":null,"if_then":[],"evidence_refs":["reg_tariff_export#1"]},{"axis":"管理層說法前後落差：Q4 利益率與配送中心","cause":null,"prior_field":null,"side_a":"2026-07-08 CFO：Q4 2024 是 Q4 2026 的良好參照，約 14% EBIT 利益率；Hebron 移交預計 Q4 初完成，延後成本僅數百萬美元。","side_b":"2026-10-07：Q4 EBIT 指引 11.4–11.6%，含 180bp 退款再投入，剔除後約 13.2–13.4%；配送中心效益延至 2027，另有火災干擾。","ruling":"可調和（程度差異）：採信新數字，對 15% 目標的時程打折，基準路徑 FY2028 利益率只設 13%。","evidence_level":"兩場法說會原話","settle_metric":"Q4 FY2026 實際 EBIT 利益率","if_then":["若 Q4 實際低於 11.4%，視為管理層連兩季過度樂觀，停止加碼","若 Q4 達 11.6% 以上且 FY2027 指引至少 12.5%，基準利益率路徑上調"],"evidence_refs":[]},{"axis":"直營失速：一次性還是品牌熱度轉弱","cause":null,"prior_field":null,"side_a":"管理層：歐洲天氣過熱、美國返校檔主打寬鬆版型失準，九月已回正，Q4 直營中個位數、全年高個位數。","side_b":"直營 Q1 +16%、Q2 +11%、Q3 +2% 連續減速；CEO 承認競爭加劇、新進者入場，Q3 動用促銷清庫存。2026-07-08 CFO 曾預期歐洲直營下半年中到高個位數。","ruling":"管理層一次性歸因不採信也不否定，標未證、監測；預登記：Q4 FY2026 與 Q1 FY2027 全球直營年增皆低於 3%，即視為歸因證偽。","evidence_level":"季報與法說","settle_metric":"全球直營有機年增","if_then":["若連 2 季低於 3%，減碼至半倉","若 Q4 至少 4%，維持分批計畫"],"evidence_refs":["channel_business_model_shift#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭：2026-10-07 CEO 稱丹寧競爭加劇、有新進者；結構：品牌毛利率 FY2022 57.5% 升至 FY2025 61.7%，批發連兩年成長且獲利。","side_b":"其他結構變數：關稅由 IEEPA 改為 Section 301 新關稅（2026-07-24 起），主要產地皆受約束；直營與批發從直營主導轉回兩條腿並行。","ruling":"雙向拉鋸：競爭惡化與品牌結構轉好同時成立，關稅改制是第三個變數，淨效果短期偏中性。","evidence_level":"法說與 10-Q","settle_metric":"剔除退款毛利率與直營年增","if_then":[],"evidence_refs":["reg_tariff_export#4"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"直營連三季減速、任期 14 年的 CFO 離職、配送中心效益一延再延、7 月說 Q4 約 14% 利益率如今剔除退款只剩約 13.3%；管理層連續兩季對短期執行過度樂觀，12 倍可能是價值陷阱。","side_b":"批發 +6%、亞洲 +10%、剔除退款毛利率仍 +80bp、EPS 財測年內三度上調、存貨年減 3%；失誤集中在美歐直營單一通路與物流時程，並非全面性。","ruling":"不賣、分批買：負面集中在單一通路與執行時程，基本盤與估值支持小部位；但不追價，第二批等 2027-01 財報。","evidence_level":"季報與法說","settle_metric":"2027-01 財報","if_then":["若 Q4 全球直營至少 4% 且 FY2027 EBIT 指引至少 12.1%，加至目標部位三分之二","若 FY2027 指引低於 12.1%，減碼一半，不等下一季"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"有機營收成長守住中個位數","type":"假設驗證","maps_to":"H1","metric":"有機營收年增（季）","threshold":"FY2027 各季至少 4%","action":"連 2 季低於 4% 停止加碼","source_freq":"季報（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"FY2027 財測利益率低於 12.1% 新基期","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 調整後 EBIT 利益率指引","threshold":"低於 12.1%","action":"減碼一半；若同時直營連 2 季低於 3% 則清倉","source_freq":"年度財測（每年 1 月）","date":"2027-01","evidence_refs":[]},{"n":3,"text":"美歐直營失速延續","type":"風險","maps_to":"R1","metric":"全球直營有機年增","threshold":"Q4 FY2026 與 Q1 FY2027 皆低於 3%","action":"減碼至半倉","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["channel_business_model_shift#0"]},{"n":4,"text":"關稅成本吸收失敗","type":"風險","maps_to":"R2","metric":"剔除關稅退款的毛利率年變化","threshold":"連 2 季年減超過 100bp 且公司歸因關稅","action":"減碼","source_freq":"季報（每季）","date":null,"evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]},{"n":5,"text":"股價再下探而基本面未壞","type":"加碼","maps_to":"H2","metric":"股價","threshold":"16.50 美元以下（約 FY2027E 共識 9.6 倍）且直營未觸發失速門檻","action":"分批反買三分之一","source_freq":"每日","date":null,"evidence_refs":[]},{"n":6,"text":"第二批進場的確認條件","type":"估值rearm","maps_to":"H1","metric":"Q4 FY2026 全球直營年增與 FY2027 EBIT 利益率指引","threshold":"直營至少 4% 且指引至少 12.1%","action":"補第二批至目標部位三分之二","source_freq":"季報","date":"2027-01","evidence_refs":[]},{"n":7,"text":"清倉條件","type":"清倉","maps_to":"H2","metric":"FY2027 EBIT 利益率指引＋全球直營年增","threshold":"指引低於 12.1% 且直營連 2 季低於 3%","action":"清倉","source_freq":"季報","date":"2027-04","evidence_refs":[]},{"n":8,"text":"批發客戶信用與供應端集中","type":"風險","maps_to":"R4","metric":"主要批發客戶財務狀況、前十大批發客戶占比","threshold":"任一主要批發客戶破產，或前十大占比回升至 27% 以上","action":"減碼","source_freq":"年報與新聞","date":null,"evidence_refs":["customer_concentration_credit#1","customer_second_source#1"]},{"n":9,"text":"財報後複審","type":"複審日期","maps_to":null,"metric":"Q4 FY2026 財報與 FY2027 財測","threshold":"財報公布後一週內","action":"重跑判斷","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"FY2027 調整後 EBIT 利益率指引","bear_threshold":"低於 12.1%（CFO 宣稱的新基期）","window":"2027-01 財報","source":"公司 Q4 FY2026 財報新聞稿與法說","last_status":"unknown"},{"metric":"全球直營有機營收年增","bear_threshold":"連 2 季低於 3%","window":"Q4 FY2026 至 Q1 FY2027","source":"季報新聞稿通路數字","last_status":"warning"},{"metric":"剔除關稅退款的毛利率年變化","bear_threshold":"連 2 季年減超過 100bp 且歸因關稅","window":"FY2027 各季","source":"季報與法說拆解","last_status":"ok"},{"metric":"有機營收年增（TTM）","bear_threshold":"低於 3%","window":"FY2027","source":"季報新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027-01 財報確認全球直營年增至少 4% 且 FY2027 EBIT 利益率指引至少 12.1%，補第二批","exec_line":"現價 18.70 美元先建目標部位三分之一；跌至 16.50 美元以下且直營未觸發失速門檻再加三分之一；2027-01 財報確認新基期後補足；唯一致命點觸發即減半","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Q3 美歐直營失速與 CFO 交接當成品牌轉弱，但批發 +6%、亞洲 +10%、剔除關稅退款的毛利率仍擴張 80bp；12 倍預估本益比隱含利益率不再擴張，而管理層已給出可在 2027 年 1 月驗證的 12.1% 新基期。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Q3 美歐直營失速與 CFO 交接當成品牌轉弱，但批發 +6%、亞洲 +10%、剔除關稅退款的毛利率仍擴張 80bp；12 倍預估本益比隱含利益率不再擴張，而管理層已給出可在 2027 年 1 月驗證的 12.1% 新基期。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-16.76, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"美國以外（亞洲、拉美）與批發撐住中個位數有機成長，抵銷美國直營波動。","2y":"FY2027 有機營收年增至少 4%，亞洲營收年增至少 8%","5y":null,"10y":null,"threshold":"FY2026 有機約 6%（財測）→ FY2027 至少 4% → FY2028 至少 4%","source":"季報新聞稿分區與通路數字；2026-10-07 法說會","drift_rule":"TTM 有機成長低於門檻 5% 以上連 2 季為削弱，低於 10% 以上連 3 季為反轉"},{"id":"H2","text":"利益率從 12.1% 新基期逐年擴張，配送中心轉換效益 2027 年起兌現，走向 15% 營業利益率。","2y":null,"5y":"FY2028 調整後 EBIT 利益率至少 13%，FY2030 至少 14.5%","10y":null,"threshold":"FY2026 約 12.1%（含 30bp 淨關稅退款）→ FY2027 至少 12.5% → FY2028 至少 13%","source":"公司財測與法說（2026-10-07 CFO 稱 12.1% 為新基期；2026-07-08 重申 15% 目標）","drift_rule":"TTM 調整後 EBIT 利益率低於門檻路徑 5% 以上連 4 季為削弱，10% 以上連 6 季為反轉"},{"id":"H3","text":"品牌定價權：不靠降價維持並緩升毛利率，高端 Blue Tab 與上身品類拉高均價。","2y":null,"5y":null,"10y":"每個會計年度毛利率（剔除一次性關稅退款）至少 61.7%；Blue Tab 年營收達 1–2 億美元（2026-07-08 CEO 說法）","threshold":"年度毛利率至少 61.7%（FY2025 水準）","source":"年度財報毛利率；季報均價說明","drift_rule":"跨 2 個會計年度低於 61.7% 為削弱，跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"美歐直營流量疲弱不是天氣與單一檔期問題，而是版型週期轉換下品牌熱度降溫。","h_ref":"H1","clock":"⚡","threshold":"Q4 FY2026 與 Q1 FY2027 全球直營有機年增皆低於 3%","evidence_refs":["channel_business_model_shift#0"]},{"id":"R2","text":"Section 301 新關稅（主要產地孟加拉、柬埔寨、巴基斯坦、越南約 10–12.5%，有效稅率各來源不一）吸收失敗，毛利率回吐。","h_ref":"H3","clock":"🔥","threshold":"剔除關稅退款的毛利率連 2 季年減超過 100bp 且公司歸因關稅","evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]},{"id":"R3","text":"競爭加劇使行銷與促銷費用常態化，12.1% 新基期守不住。","h_ref":"H2","clock":"🔥","threshold":"FY2027 調整後 EBIT 利益率低於 12.1%，或廣告費率連 2 年高於 FY2026 而利益率未擴張","evidence_refs":[]},{"id":"R4","text":"批發客戶無長期合約、逐單採購，主要客戶財務惡化，或代工整併後供應端議價轉強。","h_ref":"H1","clock":"🐢","threshold":"任一主要批發客戶破產，或前十大批發客戶占比回升至 27% 以上","evidence_refs":["customer_concentration_credit#1","customer_second_source#1"]}],"single_thing":{"description":"2027 年 1 月公布的 FY2027 財測，調整後 EBIT 利益率低於 2026-10-07 CFO 宣稱的 12.1% 新基期。","why_fatal":"基準情境 EPS 年增約 9% 中近一半來自利益率擴張；新基期守不住代表今年為救流量加的行銷、促銷與物流費用不是一次性，EPS 只能跟營收中個位數走，倍數也失去上修理由。這是情境樹中對終端 EPS 敏感度最大的單一變數。","if_happens":"減碼一半；若同時全球直營連 2 季年增低於 3%，清倉。","how_monitor":"Q4 FY2026 實際 EBIT 利益率對比 11.4–11.6% 指引；2027-01 財測的利益率與廣告費率說明；新任 CFO 首份財測口徑。","probability":"約 30%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":10.94,"peg_fy2":1.0,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":1.45,"FY2026E":1.54,"FY2027E":1.71,"FY2028E":1.98},"fy_end_month":11,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識調整後稀釋 EPS；FY2025A 1.45 為年報 GAAP 稀釋 EPS，事實表未提供 FY2025 調整後值，兩者口徑不完全同源"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 首份財測（新任 CFO 上任後首份）","impact":"高","watch":"FY2027 EBIT 利益率指引是否至少 12.1%；Q4 全球直營是否達中個位數"},{"date":"2027","date_precision":null,"type":"capacity","event":"Hebron 配送中心關閉後，美國物流成本效益開始兌現","impact":"中","watch":"調整後 SG&A 率中的物流成本是否下降"},{"date":"2027","date_precision":null,"type":"product","event":"levi.com 全面改版與平台遷移全球上線","impact":"中","watch":"電商成長與轉換率"},{"date":null,"date_precision":null,"type":"regulatory","event":"Section 301 新關稅（2026-07-24 起）後續稅率調整","impact":"中","watch":"剔除退款的毛利率年變化與公司關稅說明"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
