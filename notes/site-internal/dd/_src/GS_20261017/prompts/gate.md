你是 DD 管線 v20 的判斷層閘（gate），標的 GS（20261017）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_net_revenues_gaap`（q1_business）｜Net revenues（GAAP）＝18679 US$ million｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 earnings results 8-K（sec.gov，公司正式財報稿）（numbers.latest_quarter_kpis.items[0]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：YoY +23%（3Q25: 15,184）；QoQ -8%（2Q26: 20,338）
- `f_kpi1_pre_tax_earnings_pre_tax`（q1_business）｜Pre-tax earnings／pre-tax margin（銀行無 non-GAAP 營業利益；以稅前利益代營業利益）＝7003 US$ million｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K；pre-tax margin 37.5% 為由 7,003/18,679 自算（numbers.latest_quarter_kpis.items[1]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：未取得
- `f_kpi2_total_operating_expenses`（q1_business）｜Total operating expenses＝11308 US$ million｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[2]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：未取得
- `f_kpi5_compensation_benefits_ra`（q1_business）｜Compensation & benefits ratio（自算：5,122/18,679）＝27.4 %｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K 數字自算（numbers.latest_quarter_kpis.items[5]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：未取得
- `f_kpi9_assets_under_supervision`（q1_business）｜Assets under supervision（期末）＝4097 US$ billion｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[9]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：YoY 對 3Q25 3,452
- `f_kpi11_management_guidance`（q1_business）｜Management guidance＝無明確財測｜期間與口徑：3Q26（公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：GS 3Q26 8-K：未提供營收／獲利／費用指引；僅提及 investment banking fees backlog 較 2Q26 下降、較 2025 年底略降（numbers.latest_quarter_kpis.items[11]，as_of 3Q26（公告於 2026-10-13））
  - 註記：n/a
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-13 date｜期間與口徑：2026-10-13／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-13）
- `f_kpi7_annualized_roe`（q1_business）｜Annualized ROE＝18.7 %｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[7]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：9M26 ROE 20.7%
- `f_kpi8_cet1_ratio_standardized_`（q1_business）｜CET1 ratio（standardized，preliminary）＝12.4 %｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[8]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：advanced 13.6%（持平）
- `f_kpi3_net_earnings`（q1_business）｜Net earnings＝5294 US$ million｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[3]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：未取得
- `f_kpi10_share_repurchases_divide`（q1_business）｜Share repurchases／dividends＝3.0 US$ billion（回購；股利 1.49B）｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（回購 2.9M 股、均價 $1,048.73；4Q26 股利 $5.00／股）（numbers.latest_quarter_kpis.items[10]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：注意：稿載均價 $1,048.73 高於 price_at_dd 881.26，需核對是否為抽取誤差
- `f_peer_gs_fcf_margin_pct`（q2_moat）｜GS FCF 利潤率＝-62.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jpm_fcf_margin_pct`（q2_moat）｜JPM FCF 利潤率＝-83.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JPM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ms_fcf_margin_pct`（q2_moat）｜MS FCF 利潤率＝-25.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bac_fcf_margin_pct`（q2_moat）｜BAC FCF 利潤率＝73.37 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BAC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wfc_fcf_margin_pct`（q2_moat）｜WFC FCF 利潤率＝22.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WFC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝67.78 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝72.67 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝76.73 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝72675.61 USD m｜期間與口徑：2026-10-17／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-17）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝73812.04 USD m｜期間與口徑：2026-10-17／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-17）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.043 %｜期間與口徑：2026-10-17／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-17）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝291.17 m shares｜期間與口徑：2026-10-17／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-17）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝881.26 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝13.21 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 67.78，分子＝快照價 895.32｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝12.67 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝30.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝30.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.61 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝48.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.22 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-16（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-5.43 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 71.67 → 67.78（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-3.67 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（70.36 → 67.78）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-3.94 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-16（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.33｜期間與口徑：2026-10-16（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-16（RTH 收盤，UTC））
- `f_kpi6_provision_for_credit_los`（q1_business）｜Provision for credit losses＝368 US$ million｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GS 3Q26 8-K（numbers.latest_quarter_kpis.items[6]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-13））
  - 註記：未取得

### findings_digest 中方向為負或來源衝突的條目（7 條）
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：GS 2026年6月30日 10-Q 揭露：2021年起的信用違約交換（CDS）結算價格反壟斷集體訴訟仍在進行，最新列示步驟為被告於2025-10-10提出的判決於訴狀動議；另稱集團內單位面臨其他未具名的監管調查與審查。
  - 來源：SEC EDGAR, Goldman Sachs Group 10-Q (period ended 2026-06-30)（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：法院案件列表顯示一件私人反壟斷訴訟 Simon v. The Goldman Sachs Group 於2026-04-30提起；列表未載明實質指控。未查到政府機關（DOJ/FTC/EU）對GS的新反壟斷調查。
  - 來源：案件列表（api.ai-analytics.org/case/73273024）（as_of 2026-04-30）｜affects：decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Platform Solutions 營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合markdown
  - 來源：Goldman Sachs 3Q26 earnings (as reported)（as_of 2026-10-13）｜affects：thesis.R
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：2026Q3 全球 M&A 量較前三個月下滑41%至9,930億美元，美國IPO自夏季後動能減弱
  - 來源：The Star: Wall Street banks see strong pipeline amid volatility（as_of 2026-10-16）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：財報前30天內EPS預估17次下修、0次上修（IG／LSEG 財報預覽）
  - 來源：IG 'Goldman Sachs stock Q3 2026 earnings preview'（as_of 2026-10-12）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：1MDB 證券集體訴訟（Sjunde AP-Fonden v. Goldman Sachs）仍在審理；SDNY 於 2025-09-04 裁定認證集體，適用 2016-12-22 至 2018-11-08 買入普通股的投資人；搜尋未見和解或實質裁決。
  - 來源：KTMC court-approved class notice (Feb 2026)（as_of 2025-09-04）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：1MDB 證券集體訴訟仍待審；SDNY 2025-09-04 裁定認證集體（買入期間 2016-12-22 至 2018-11-08），2026 年 2 月有法院核定的集體通知。
  - 來源：KTMC court-approved class notice (Feb 2026)（as_of 2025-09-04）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1530.0,"bear_5y_price":630.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":19.9,"ev5y_pct":16.1,"irr_base_pct":3.7,"asym_ratio":1.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":67.78,"pe":13.0,"basis":"FY2026 共識 EPS 67.78（Koyfin 2026-10-08），起點本益比＝881.26÷67.78≈13.0；終端倍數套在終端年 EPS 上，與起點同為當年度 EPS 口徑；同業現值本益比事實表未涵蓋，以本公司 trailing 12.67 倍與前瞻 13.2 倍為對照錨"},"eps":{"bull":[76.0,82.0,88.0,95.0,102.0],"base":[70.0,73.0,76.5,80.5,84.5],"bear":[60.0,46.0,50.0,55.0,60.0]},"pe":{"bull":15.0,"base":12.5,"bear":10.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.043,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GS_Q2_2026_Earnings_Call_20260714.md
- 2026-07-14｜Denis Coleman｜guidance：全年另類募資預期上修至超過1,250億美元（原話："we now expect full-year fundraising to exceed $125 billion"）
- 2026-07-14｜Denis Coleman｜guidance：Platform Solutions 下半年各季營收預期與第二季大致持平（原話："for the remainder of the year to be broadly consistent with"）
- 2026-07-14｜Denis Coleman｜guidance：績效費預期下半年大幅增加（原話："We expect these fees to increase materially for the"）
- 2026-07-14｜Denis Coleman｜guidance：全年有效稅率仍預期約20%（原話："we continue to expect an effective tax rate of"）
- 2026-07-14｜Denis Coleman｜guidance：投行前景樂觀，贊助商業務仍低於歷史均值（原話："We remain optimistic on the investment banking outlook"）
- 2026-07-14｜Denis Coleman｜margin：上半年效率比58.8%，較去年同期改善320bp（原話："with an efficiency ratio of 58.8%, improving 320 basis"）
- 2026-07-14｜Denis Coleman｜margin：薪酬比（扣除撥備）降至31%（原話："decline in our compensation ratio net of provisions to 31%."）
- 2026-07-14｜Denis Coleman｜margin：營收成長約40%，薪酬費用成長30%、非薪酬22%（原話："We've been able to grow our revs at about 40%"）
- 2026-07-14｜Denis Coleman｜margin：管理層稱費用基礎無結構性變化（原話："any structural change in our expense base at this point"）
- 2026-07-14｜Denis Coleman｜margin：FICC與股票融資營收45億美元，占兩者合計37%（原話："revenues of $4.5 billion rose 62% versus the prior year and"）
- 2026-07-14｜Denis Coleman｜capital_allocation：CET1 12.9%，高於現行要求150bp（原話："Common equity Tier 1 ratio was 12.9% at the end of the"）
- 2026-07-14｜David Solomon｜capital_allocation：季股息提高至每股5美元，年增25%（原話："quarterly dividend to $5 a share, representing a 25%"）
- 2026-07-14｜David Solomon｜capital_allocation：本季回購40億美元普通股（原話："We also repurchased $4 billion of common stock in the"）
- 2026-07-14｜David Solomon｜capital_allocation：無法部署資本時會快速還給股東（原話："going to nimbly get it back to shareholders as quickly as"）
- 2026-07-14｜Denis Coleman｜capital_allocation：資產負債表擴張的意願有上限（原話："Ultimately, there will be a limit to our appetite to expand"）
- 2026-07-14｜Denis Coleman｜capital_allocation：管理層稱對監管改革方向表示期待 Basel III 定案（原話："we look forward to swift progress towards Basel III"）
- 2026-07-14｜Denis Coleman｜commitment：CET1營運模式維持高於要求50至100bp（原話："sort of, call it, plus 50 to 100 basis points. We're"）
- 2026-07-14｜Denis Coleman｜commitment：另類募資年度目標750億至1,000億美元（原話："have a target of $75 billion to $100 billion of annual"）
- 2026-07-14｜David Solomon｜commitment：承諾持續達成AWM成長目標（原話："you can expect us to continue to deliver on those growth"）
- 2026-07-14｜David Solomon｜commitment：AWM併購：門檻高但會持續尋找（原話："The bar is always high to do anything inorganic."）
- 2026-07-14｜David Solomon｜risk：AI投資週期不會直線前進，短期可能有重新調整（原話："not there can be recalibrations, in the short term"）
- 2026-07-14｜David Solomon｜risk：管理層承認週期必有重置與回落（原話："you will have a recalibration, a reset, a drawdown, and"）
- 2026-07-14｜Denis Coleman｜risk：金融需求超過公司願意提供的量（原話："are outstripping what we think is the appropriate quantum."）
- 2026-07-14｜David Solomon｜risk：IPO量僅在十年均值或以下（原話："IPO volumes in this quarter were kind of at or below"）
- 2026-07-14｜David Solomon｜risk：另類產業部分區塊承壓（原話："despite some pressure in segments of the industry, investor"）
- 2026-07-14｜Denis Coleman｜competition：亞洲股票業務過去被視為競爭短板，已投資補強（原話："capture what we viewed as a competitive shortcoming in Asia"）
- 2026-07-14｜Denis Coleman｜competition：主經紀業務存在定價槓桿，部分同業更節制（原話："opportunities for pricing leverage."）
- 2026-07-14｜David Solomon｜customer：贊助商交易尚未加速，是潛在上行（原話："has not accelerated, and candidly, it's going to come at"）
- 2026-07-14｜David Solomon｜customer：大型併購量上半年成長90%（原話："corporate M&A volumes up 90% through the first half of 2026."）
- 2026-07-14｜David Solomon｜customer：獲任管理Lockheed Martin等退休金計畫（合計700億美元）（原話："and Lockheed Martin's retirement plans, which collectively"）
- 2026-07-14｜David Solomon｜product：投行積壓訂單創五年新高（原話："our backlog increased to its highest level in 5 years"）
- 2026-07-14｜David Solomon｜product：加速投資超高淨值財富業務（原話："We've accelerated our investment."）
- 2026-07-14｜Denis Coleman｜product：人力策略：目前不是結構性重整人力的時刻（原話："structural rework of our human capital footprint."）
- 2026-07-14｜David Solomon｜product：AI不會取代公司的核心人才（原話："change how work gets done, it will not replace what matters"）

### GS_Shareholder_Analyst_Call_The_Goldman_Sachs_Group_Inc_20260429.md
- 2026-04-29｜David Solomon｜margin：管理層列示2025年全年財務結果（原話："grew our earnings per share by 27% to $51.32 and"）
- 2026-04-29｜David Solomon｜margin：管理層列示2025年營收與ROE變化（原話："improved our return on equity by 230 basis points to 15%."）
- 2026-04-29｜David Solomon｜margin：管理層對2019–2025累計成果的口徑（原話："grown earnings per share by 144%"）
- 2026-04-29｜David Solomon｜capital_allocation：管理層稱2019–2025總股東報酬率居同業之首（原話："total shareholder return of over 340%"）
- 2026-04-29｜David Solomon｜product：宣布One GS 3.0以AI驅動的營運模式（原話："launch of One Goldman Sachs 3.0, our operating model"）
- 2026-04-29｜David Solomon｜guidance：管理層對One GS 3.0長期效益的表述，無量化目標（原話："One GS 3.0 will drive stronger operating leverage,"）
- 2026-04-29｜David Solomon｜risk：管理層點名的外部環境風險（原話："uncertainty in parts of private credit"）
- 2026-04-29｜David Solomon｜competition：管理層稱不確定時期客戶轉向高盛（原話："clients turn to Goldman Sachs as a trusted adviser"）
- 2026-04-29｜David Solomon｜commitment：管理層稱持續投資於人才（原話："we remain focused on continuing to invest in them."）
- 2026-04-29｜David Solomon｜customer：管理層稱2026年第一季為史上第二高的營收、盈餘與EPS（原話："second highest net revenues, net earnings and earnings"）
- 2026-04-29｜Drew Jorgensen｜risk：股東提案方稱25%召開特別股東會門檻不可達成（原話："the current 25% figure is unattainable."）
- 2026-04-29｜Yumi Narita｜capital_allocation：NYC審計長提案要求揭露能源供給比率；稱JPMorgan與Citi已揭露（原話："Goldman peers JPMorgan and Citi disclosed their ESR,"）
- 2026-04-29｜Yumi Narita｜commitment：第7項提案稱高盛游說揭露落後同業（原話："existing disclosures lag peers and can be enhanced."）
- 2026-04-29｜Jamie Greenberg｜risk：say-on-pay支持率約70%（原話："received the support of votes representing approximately 70%"）
- 2026-04-29｜Jamie Greenberg｜risk：特別股東會門檻提案獲約37%支持而未通過（原話："received the support of approximately 37% of the"）

### 問答異常語氣（迴避／改口／保留）
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Mayo：併購領先帶來的跨業務乘數效應是多少？｜答法：Solomon 明說不給百分比，改談框架
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Fannon：績效費大幅增加的量化與依據｜答法：Coleman 只說與已知特定交易有關，未給金額
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Cassidy：交易業績中 OneGS 與市場波動各占多少｜答法：Solomon 稱無法以單季量化，改引2020年起前百大客戶排名
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Cassidy：與網路泡沫／2021年比較AI貢獻｜答法：Solomon 稱不確定能給好答案，改談公司更多元
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Bolu：SLR已為同業最低，能壓多低｜答法：Coleman 未給數字，稱多重限制動態管理
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Erika Penala：亞洲超大型股交易貢獻占比與回檔是否擔憂｜答法：Coleman 未回答占比，改談廣泛基礎的活動

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | none | 0 | 2 |
| geo_supply_chain | none | 0 | 2 |
| end_markets | found | 7 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Goldman Sachs largest client concentration risk single-source customer diversify 2026；Goldman Sachs clients in-house insourcing capital markets trading desks 2026
- **reg_tariff_export**（none）：Goldman Sachs tariff impact investment banking capital markets 2026；Goldman Sachs China trade restriction OR export control OR entity list 2026
- **geo_supply_chain**（none）：Goldman Sachs geopolitical risk exposure China Taiwan 2026；Goldman Sachs operational resilience third-party concentration risk 10-K 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260615","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"GBM（投行+交易）維持 league-table 前二、through-the-cycle 市占不流失","columns":{"2Y 驗證點":"FICC+Equities 合計市占持平/微升","5Y 驗證點":"顧問費市占穩居前二","10Y 驗證點":"做市規模優勢維持","具體數字門檻":"Equities 連續創 record；Advisory 市占前二","信息來源":"Coalition Greenwich 市占榜 + 公司法說","漂移觸發":"市占連 2 季流失 → 削弱（2Y 假設連 2 季）"}},{"id":"H2","text":"AWM 把波動投行收入逐步換成可預期管理費，ROTCE 結構性墊高至 mid-teens","columns":{"2Y 驗證點":"管理費 YoY &gt; +8%；AWM pre-tax margin 維持 mid-20s","5Y 驗證點":"替代資產 AUS &gt; $800B；through-cycle ROTCE ≥ 15%","10Y 驗證點":"費用收入占比 &gt; 30%","具體數字門檻":"AUS $3.7T（Q1'26 record）；alt $625B；募資 $75-100B/年","信息來源":"公司 Q1'26 法說 + Investor Day target","漂移觸發":"管理費 YoY &lt; +5% 連 2 季 → 削弱（5Y 假設連 4 季才反轉）"}},{"id":"H3","text":"市場願意維持「轉型後」估值溢價（P/TBV 不回到 1x 時代）","columns":{"2Y 驗證點":"P/TBV 維持 &gt; 2x","5Y 驗證點":"5Y 均 P/TBV &gt; 1.8x","10Y 驗證點":"估值中樞高於 2015-2020 的 1.0-1.3x","具體數字門檻":"當前 P/TBV 3.10x（史上最高）","信息來源":"GuruFocus/YCharts 5Y P/TBV band","漂移觸發":"P/TBV 跌破 1.5x 連 2 季 → 反轉（估值 thesis 破裂）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資本市場週期反轉，交易/IB 從 record 回落（Q1'26 record trading 是「市場混亂」的週期峰值）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"GBM 季度淨收入 YoY","警戒閾值":"連 2 季 YoY &lt; −15% → 減倉"}},{"id":"R2","text":"管理層再次「為成長」進入低 ROIC 領域（消費金融前科），或 AWM 募資不及 $75B 目標","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"替代資產年度募資；新業務 capital 投入","警戒閾值":"年度募資 &lt; $60B 連 2 年，或啟動新非核心擴張"}},{"id":"R3","text":"估值倍數結構性重估（P/TBV 從 3.1x 回歸歷史中段），即使 EPS 不跌股價也跌","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"P/TBV 5Y 中樞","警戒閾值":"P/TBV 跌破 1.5x（需 ≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":1082.57,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GS","date":"2026-10-17","schema":"v15.2","contract":"v19","company_name":"The Goldman Sachs Group, Inc."},"oneliner":"高盛是資本市場裡最強的顧問與做市平台之一，耐久型收入已占近半；但 2026 年的獲利處在週期高處，13 倍本益比談不上便宜。先等兩季財報證明谷底已經抬高，再考慮進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/scenario.json","answers":{"q1_business":{"verdict":"賺三種人的錢：企業付顧問與承銷費，機構與對沖基金付交易價差與融資利息，富人與機構付管理費。錢卡在頂級顧問關係和資產負債表交會的那一個節點，而這個節點本身隨資本市場週期大幅擺動。","reasoning":"3Q26 淨營收 186.8 億美元，年增 23%、季減 8%。分部約 72% 為 Global Banking & Markets（134.6 億，年增 32%），其中股票 64.4 億（年增 72%）、FICC 34.7 億（年增率接近零）、顧問 17 億創單季紀錄；約 27% 為 Asset & Wealth Management（50.5 億，年增 14%）；Platform Solutions 只剩 1.7 億，年減 72%。銀行沒有毛利率口徑，以稅前利益率代營業利益率：7,003÷18,679＝37.5%；前三季效率比 59.4%，扣撥備後薪酬比 30%。依管理層口徑，耐久型收入（管理費、融資、私人銀行）約占年初至今營收 45%，融資收入占 FICC＋股票營收逾 40%。產業時鐘判在 III：CEO 自己說活動從 5–6 月的前十分位降到前四分位，3Q26 全球 M&A 量季減 41%，聯準會 9 月升息，投行積壓較 Q2 末下降；營收仍在高位，但動能已轉弱。供需持久性：週期性將反轉，耐久收入只能緩衝回落幅度，無法抵銷。單點依賴：沒有單一客戶營收集中度揭露（10-K 只揭露放款組合約 81% 在美洲）；真正的單點是資本市場活動本身。公司未提供營收或獲利指引。","fact_refs":["f_kpi0_net_revenues_gaap","f_kpi1_pre_tax_earnings_pre_tax","f_kpi2_total_operating_expenses","f_kpi5_compensation_benefits_ra","f_kpi9_assets_under_supervision","f_kpi11_management_guidance","f_earnings_recency"],"verdict_values":{"revenue_quality":"約 45% 為耐久型收入（管理及其他費用 3Q26 為 36 億美元、年增 22%，加上股票與 FICC 融資、私人銀行放款），其餘 55% 是投行費用與做市的交易型收入，對資本市場活動高度敏感","unit_econ_note":"3Q26 稅前利益率 37.5%（7,003÷18,679）；單季薪酬比 27.4%，前三季扣撥備後薪酬比 30%，效率比 59.4%，較前一年改善 270bp；非薪酬費用年增 30%，主要是交易相關費用","archetype":{"primary":"金融","secondary":"循環/商品","confidence":"高","fingerprint":"約七成收入來自投行與交易，隨資本市場週期擺動；近三成來自資產與財富管理費；資本受監管比率約束的資產負債表業者"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：Solomon 在 2026-10-13 法說稱活動從前十分位降到前四分位；3Q26 全球 M&A 宣布量季減 41% 至 9,930 億美元；8-K 載明投行積壓較 2Q26 末下降、較 2025 年底略降；耐久收入約 45% 只能減緩回落","bargaining":{"up":"上游是人才：Coleman 稱頂尖業務與工程人才的爭奪更激烈；薪酬比降到 30% 是業務組合偏向融資的結果，並不代表人才議價力下降","down":"下游企業可以在多家投行之間挑顧問，但最大型交易集中在前兩名；股票融資需求超過產業供給，高盛握有定價權並可挑客戶","geo":"亞洲股票融資是新的增量來源；中東衝突帶來的能源與利率波動，是交易延後的主要外部風險"},"profit_pool_dir":"利潤池正往融資（動用資產負債表）與另類資產（管理費）移動，純顧問與承銷的占比下降；高盛在兩邊都有位置，是少數同時具備顧問、承銷、分銷與自有資金池的業者","tam_table":{"expanded":false,"reason":"投行與交易是成熟市場，成長取決於活動週期與份額，不是滲透率；另類資產與財富管理的市場規模與滲透率在事實表未涵蓋，無法展開"}}}},"q2_moat":{"verdict":"護城河方向穩定（→）：顧問關係網與做市規模仍居第一梯隊，主經紀定價權在擴大；但投行費用總額落後 JPMorgan，EMEA 領先差距也在縮小，兩邊相互抵銷。","reasoning":"機制是三件事互相加乘：董事會層級的顧問關係（年初至今 M&A 宣布量領先第二名約 4,300 億美元，管理層稱是史上最大差距）、做市與融資的資產負債表規模（股票融資營收年增 96% 創紀錄，Coleman 稱需求超過產業供給）、以及能把交易分配給自有公私募資金池的資產管理平台（AUS 4.1 兆美元，長期淨流入連續 35 季）。可證方向：份額軸偏正，2026 上半年 EMEA M&A 份額為 2018 年以來同期最高、全球 M&A 份額 38%，3Q26 股票營收也高於大摩與小摩；偏負的是 2025 年 LSEG 投行費用總額排第二（82 億對 JPMorgan 101 億），且 EMEA 對 JPMorgan 的領先比 2025 上半年的 11 個百分點更窄。執行力評 8、定價力評 7，等級 B：銀行業允許綜合評分，但同業 ROIC spread 取不到，不給到 8 分以上。報酬持續期：3Q26 年化 ROE 18.7%、前三季 20.7%，屬高利益率×低周轉，主要靠槓桿撐起；再投資空間有限，內生成長上界約 2.8%，多數盈餘以股利與回購退回股東。","fact_refs":["f_kpi7_annualized_roe","f_kpi8_cet1_ratio_standardized_","f_kpi3_net_earnings","f_kpi10_share_repurchases_divide","f_peer_gs_fcf_margin_pct","f_peer_jpm_fcf_margin_pct","f_peer_ms_fcf_margin_pct","f_peer_bac_fcf_margin_pct","f_peer_wfc_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"董事會層級顧問關係＋做市與融資的資產負債表規模＋自有公私募資金池，三者互相加乘：顧問帶出融資與承銷，融資與承銷的部位再分配進資產管理","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力穩定：M&A 宣布量年初至今第一且領先差距創紀錄，股票營收三家最高。定價力擴大：主經紀融資供不應求。份額略受擠壓：EMEA 對 JPMorgan 的領先縮小，2025 年投行費用總額落後 JPMorgan。三者合計判為穩定","competitor_notes":[{"name":"JPM","strategy_note":"2025 年投行費用總額第一（101 億美元，高盛 82 億），EMEA M&A 份額差距正在縮小，是最直接的份額威脅；3Q26 股票營收約 50 億美元，年增 49%"},{"name":"MS","strategy_note":"3Q26 股票營收 58 億美元，年增 41%，低於高盛的 64.4 億；財富管理規模更大，是資產與財富管理端的主要對照"},{"name":"BAC","strategy_note":"全能型銀行，靠存款成本支撐融資，在大型顧問案上不是主戰場對手；表內 FCF 利潤率為正，反映的是存放款結構，與競爭力無關"},{"name":"WFC","strategy_note":"以商業銀行業務為主，投行份額小，對高盛的顧問與做市核心幾乎不構成威脅"}],"spread_notes":null,"peer_na_reason":"同業對照只有 FCF 利潤率，而銀行與券商的自由現金流被交易資產與放款變動主導（高盛 −62.7%、JPMorgan −83.4%、美銀 +73.4%），不能代表 ROIC；同業 ROE／ROTCE 事實表未涵蓋","threats":[{"level":"🟡","text":"JPMorgan 在投行費用總額領先，並在 EMEA 縮小 M&A 份額差距；屬點對點的份額競爭，尚未動搖第一名地位","p":"30%","evidence_refs":["competitive_share_entrants#0","end_markets#6","competitive_share_entrants#1"]},{"level":"🟡","text":"代幣化、預測市場與代理式交易可能侵蝕做市價差；Solomon 稱目前規模很小，高盛已參與 DTCC 代幣化服務並自建 GS DAP，屬可吸收的技術變化","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"公開債市承銷往私募信貸移轉，可能壓低承銷費率；高盛同時擁有私募 IG 與另類資產平台，兩邊都接得住，風險在費率而非份額","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"企業併購與融資需求真實存在（AI 資料中心建設估計到 2032 年需逾 10 兆美元），但可以延後：Solomon 坦言 9 月有幾檔 IPO 因估值比預期低 10–15% 而暫緩，私募贊助商也選擇用延續基金延後退場"},{"item":"決策層級","level":"🟢","text":"顧問的選擇權在董事會與執行長手上，看的是關係與聯盟排名，不看報價；年初至今 M&A 宣布量領先第二名約 4,300 億美元，顯示最大型交易的替代性很低"},{"item":"價值鏈分配","level":"🟡","text":"融資端定價權在高盛（股票融資需求超過產業供給）；顧問與承銷端，大型交易常由多家共同顧問分費，私募信貸也在分走債務承銷的利潤，整條價值鏈的分配並非單向有利"},{"item":"社會容忍度","level":"🟡","text":"超額報酬依賴監管資本規則：Basel III 終局與 G-SIB 重提案目前往放寬方向走，CFO 希望年底前定案，但期中選舉後政策可能轉向；1MDB 證券集體訴訟已認證集體，CDS 反壟斷案仍在進行，屬政策與法律容忍度風險"}],"roiic":18.7,"reinvest_rate":15,"endo_ceiling":2.8,"formula_note":"銀行不適用資本支出公式，改用保留盈餘率代替再投資率。3Q26 淨利 52.94 億美元，扣普通股股利 14.9 億與回購 30 億，保留 8.04 億，保留率約 15%（未扣優先股股利）。增量報酬以 3Q26 年化 ROE 18.7% 代替，因為增量值事實表未涵蓋。內生成長上界＝18.7%×15%≈2.8%；加上回購年化約 4.7% 的減股效果，每股上界約 7.5%"}}}},"q3_growth":{"verdict":"五年後的成長空間中等（🟡）：交易與投行是成熟市場，長期跟著 GDP 與股市市值走；第二曲線是另類資產與財富管理，但已是規模化業務，不是新的 S 曲線。","reasoning":"成長來源以量為主（交易量、融資餘額、AUS），價為次（主經紀定價），再加上小規模的資產管理收購與回購減股。三年共識 EPS CAGR 為 14.3%（FY2025A 51.32 → FY2028E 76.73，Koyfin 2026-10-08 快照；分析師家數事實表未涵蓋），但其中多數來自 2026 年單年 +32% 的週期跳升；2026→2028 只有約 6.4%/年。內生上界 2.8%，缺口約 11.5pp，可以歸因：回購約 4–5pp，其餘來自利潤率擴張與週期性營收上揚（效率比改善 270bp、薪酬比降到 30%）。2026 年之後的共識 6.4%，大致落在每股上界約 7.5% 以內。Solomon 在 3Q 法說自己說，不認為未來五年營收還能維持 2022 年以來 11% 的年複合成長。衰退信號亮一個：2025 年 EPS 年增 26.6%、營收只增 8.9%，差距大於 5pp。長期成長性與價值陷阱風險都判 🟡。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi9_assets_under_supervision","f_kpi10_share_repurchases_divide"],"verdict_values":{"growth":{"driver_mix":"量（交易量、融資餘額、AUS 淨流入）為主，價（主經紀定價）次之，回購每年減股約 4–5%，資產管理收購的貢獻小","runway_years":"事實表未涵蓋滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界 2.8%＝增量報酬 18.7%（以 3Q26 年化 ROE 代替）×保留率 15%；加上回購約 4.7% 後，每股上界約 7.5%","segments":[{"item":"Global Banking & Markets","value":"3Q26 淨營收 134.6 億美元，年增 32%、季減 13%；前三季 segment ROE 23.5%；週期敏感"},{"item":"Asset & Wealth Management","value":"3Q26 淨營收 50.5 億美元，年增 14%；管理及其他費用 36 億美元，年增 22%；另類 AUS 4,910 億美元，年增 26%；全年募資預期約 1,500 億美元"},{"item":"Platform Solutions","value":"3Q26 淨營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合減值；消費金融持續縮減中"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長（差距大於 5pp）","lit":true,"text":"2025 年 EPS 年增 26.6%（40.54→51.32），營收年增 8.9%"},{"item":"FCF/NI 連兩年低於 0.75","lit":false,"text":"數字上連三年為負，但銀行的自由現金流被交易資產與放款變動主導，這個訊號不適用"},{"item":"核心市占近 12 個月縮減","lit":false,"text":"M&A 宣布量領先差距創紀錄；只有 EMEA 對 JPMorgan 的領先縮小，屬部分訊號"},{"item":"產業估值倍數近三年系統性下移","lit":null,"text":"事實表未涵蓋"},{"item":"SBC/營收大於 5% 且逐年上升","lit":null,"text":"事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等偏弱：股利與回購用掉約 85% 的季淨利，但回購均價 1,049 美元對應的盈餘收益率約 6.5%，低於 7% 的門檻；收購規模小，報酬未揭露。","reasoning":"3Q26 普通股股利 14.9 億美元加回購 30 億，合計 44.9 億，約占淨利 52.94 億的 85%。回購從 Q2 的 40 億放慢到 30 億，CET1 從 12.9% 降到 12.4%，高於要求的緩衝從 150bp 縮到 100bp，仍在管理層承諾的 50–100bp 區間上緣。季股利 5 美元，年增 25%。法說上有分析師直接質疑公司在約 3 倍有形淨值的價位大量回購。資產管理收購（Industry Ventures 6.65 億美元另加至多 3 億或有對價、Innovator 約 20 億，NEOS 與 LCN 金額未揭露）已知合計約占市值 1%，不承重。前一輪消費金融擴張以出售 Apple Card、GM 卡收場，Platform Solutions 3Q26 仍在認列減值。銀行的 FCF/NI 沒有意義；SBC 金額事實表未涵蓋。","fact_refs":["f_kpi10_share_repurchases_divide","f_kpi3_net_earnings","f_kpi8_cet1_ratio_standardized_","f_dividend_yield_ttm","f_shares_diluted_m","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"近期資產管理收購（Industry Ventures、Innovator、NEOS、LCN）尚無已實現報酬揭露；前一輪消費金融擴張以退場收場，Platform Solutions 3Q26 營收年減 72%；已實現 ROIIC 事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"3Q26 回購均價 1,048.73 美元，FY2026 共識 EPS 67.78，盈餘收益率約 6.5%；10 年期公債約 5%（Solomon 2026-10-13 法說口述）加 2% 為 7%，未過"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 金額與授予股數事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主體是內生的交易、融資與管理費；已知金額的收購合計約 27 億美元，約占市值 1%，不承重"}}}},"q5_valuation":{"verdict":"現價要求 2026 年約 68 美元的 EPS 是新的常態，之後每年再成長約 6%。這只有一半可信：耐久收入確實抬高了谷底，但今年的獲利有相當部分來自前十分位的市場活動。","reasoning":"前瞻本益比 13.0 倍（881.26÷67.78），trailing 12.67 倍，在四個年度端點中分位 30%；EV/S 對銀行沒有意義。分母本身就是爭點：若獲利回到 2025 年的 51.32 美元，現價本益比是 17.2 倍，不是 13 倍。以三年共識 CAGR 14.3% 計算的 PEG 為 0.91，看似便宜，但 14.3% 是被 2026 單年的週期跳升墊高的；改用 2026→2028 的 6.4%，PEG 約 2.0。股息殖利率 2.04%。同業本益比與 P/TBV 事實表未涵蓋。本研究的 Base 情境：一年後 70 美元×13 倍＝910 美元（+3.3%），五年後 84.5 美元×12.5 倍＝1,056 美元（+19.8%）。估值結論中性。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm","f_ps_current","f_ev_s_current"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026 共識 EPS），輔以 trailing 本益比的年度端點分位；同業本益比與有形淨值倍數事實表未涵蓋","tier":"大型投行與券商（與 MS、JPM 投行部門同一層級）","peers":{"expanded":false,"reason":"事實表的同業對照只有 FCF 利潤率，對銀行沒有估值意義；同業本益比與 P/TBV 事實表未涵蓋"},"fwd_pe":13.0,"peg":0.91,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 13.0 倍、trailing 12.67 倍，四個年度端點分位 30%（五年分位事實表未涵蓋）；以 2025 年 EPS 計為 17.2 倍。PEG 0.91 被週期跳升墊高，以 2026→2028 成長率計約 2.0。便宜與否取決於分母，結論中性 🟡","upside_short_pct":3.3,"upside_mid_pct":19.8,"denominator_disputed":true,"denominator_note":"FY2026 共識 EPS 67.78 包含上半年前十分位的資本市場活動，以及 3Q 偏高的績效費；若回到 FY2025 的 51.32，現價本益比是 17.2 倍而非 13 倍，因此不採用便宜的論證"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把 2026 年的週期高處獲利當成常態；其次是把融資業務當作耐久收入，實際上它放大了週期與信用風險。","reasoning":"三個方向見反證紀錄：一是資本市場收縮讓 EPS 掉回 46–50 美元、倍數同步壓縮；二是耐久收入靠資產負債表撐起，去槓桿時融資收入、信用損失與資本緩衝會同時惡化；三是 13 倍看似便宜，但分母有爭議，共識在財報前三個月已下修 5.4%。股價 26 週跌 3.9%，RSI 34，沒有過熱，但也還沒有出現投降式賣壓。訴訟方面，1MDB 證券集體訴訟已認證集體、CDS 反壟斷案仍在進行，金額與時點都在事實表未涵蓋。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_week26_return_pct","f_rsi14","f_kpi6_provision_for_credit_los"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高處的獲利被誤當常態"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":67.78,"pe":13.0,"basis":"FY2026 共識 EPS 67.78（Koyfin 2026-10-08），起點本益比＝881.26÷67.78≈13.0；終端倍數套在終端年 EPS 上，與起點同為當年度 EPS 口徑；同業現值本益比事實表未涵蓋，以本公司 trailing 12.67 倍與前瞻 13.2 倍為對照錨"},"eps":{"bull":[76.0,82.0,88.0,95.0,102.0],"base":[70.0,73.0,76.5,80.5,84.5],"bear":[60.0,46.0,50.0,55.0,60.0]},"pe":{"bull":15.0,"base":12.5,"bear":10.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.04,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-50,"hi":-28,"basis":"下檔情境谷底 FY2028 EPS 46 美元×谷底本益比 10 倍≈460 美元，自 881 美元下跌約 48%；溫和版為 EPS 58 美元×11 倍≈640 美元，約 −27%；因此取 −28% 至 −50%。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"AI 基建融資與私募贊助商退場（贊助商 M&A 仍低於歷史均值）接力，活動維持在前四分位，管理費年增逾 10%，EPS 年增約 8.5%；市場給耐久收入溢價，本益比 15 倍","base":"交易活動從前四分位慢慢回到中位附近，管理費年增約 8%，回購每年減股 3–4%，EPS 年增約 4.5%，略低於共識，因為 Solomon 自己說未來五年營收不會再年增 11%；EPS 路徑已含回購減股效果，淨回購殖利率填 0 以免重複計算","bear":"2027–2028 年資本市場收縮（類似 2022–2023 年），EPS 跌到 46 美元後回升到 60 美元，市場把倍數壓到 10.5 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"3Q26 全球 M&A 量季減 41%；投行積壓較 2Q 末下降；聯準會 9 月升息、市場預期再緊縮約 75bp；10 年期公債一季上升約 75bp","assumption":"活動只是從前十分位降到前四分位，不會跌破中位數","consequence":"若 2027–2028 年像 2022–2023 年一樣收縮，EPS 會從 68 美元掉到 46–50 美元，倍數壓到 10 倍，股價約 460–500 美元；從現價算虧約 45%，若加上之前從 1,082 美元的跌幅，接近虧一半。這個故事與唯一致命點相同","ruling":"採納：Bear 機率定為 30%，並把唯一致命點設在單季營收跌破 140 億美元","watch":"每季淨營收與投行積壓方向；每月全球 M&A 宣布量","evidence_refs":["end_markets#5","supply_demand_durability#0","supply_demand_durability#3"],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi11_management_guidance"]},{"view":"論點成功但股東經濟變差","evidence":"融資收入占 FICC＋股票營收逾 40%；放款組合季增 6% 至 2,760 億美元；3Q26 撥備 3.68 億美元含個別減值；CET1 緩衝從 150bp 縮到 100bp；CFO 稱 SLR 的大幅延展已經完成","assumption":"耐久收入的增加不需要更多槓桿，也不會帶來更多信用損失","consequence":"即使耐久收入占比真的升到五成，它也是靠資產負債表換來的；去槓桿時融資收入、撥備與資本緩衝會同時惡化，ROE 的谷底未必如管理層所說那麼高。過去的消費金融擴張也是成長了、股東卻賠錢的例子","ruling":"部分採納：Poonawala 在法說上提出同樣的質疑，Solomon 只回答要看 3–5 年，沒有給出下行時的數字；列為 R3 並設撥備門檻","watch":"單季撥備是否超過 7.5 億美元；CET1 緩衝是否低於 50bp；融資收入季減幅度","evidence_refs":["end_markets#3"],"fact_refs":["f_kpi6_provision_for_credit_los","f_kpi8_cet1_ratio_standardized_"]},{"view":"價格已反映太多","evidence":"前瞻本益比 13 倍是用週期高處的分母算的，以 2025 年 EPS 計為 17.2 倍；財報前 30 天 EPS 預估 17 次下修、0 次上修；FY1 共識三個月下修 5.4%；分析師稱股價約為有形淨值 3 倍","assumption":"市場會用今年的 EPS 給倍數","consequence":"如果市場改用跨週期 EPS 定價，就算 EPS 不跌，倍數也會被壓縮","ruling":"採納：便宜的論證不成立，不追價，改等事件證據","watch":"財報後的共識快照是否回補；股價對有形淨值的倍數（資料缺口）","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_pe_current","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1082.57 → 本次 881.26（-18.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1082.57","side_b":"本次 price_at_dd=881.26","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,082.57 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,082.57 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 1,082.57 美元：Bull 價 1,530、Bear 價 630，五年期望值 −5.5%，基準年化 −0.5%，不對稱比 0.66","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.66。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,082.57 美元：五年期望值 −5.5%，基準年化 −0.5%，不對稱比 0.66","side_b":"本次情境、股價 881.26 美元：五年期望值 +16.1%，基準年化 3.7%，不對稱比 1.72","ruling":"再換股價、情境不動：起點價下跌 18.6%，五年期望值多 21.6 個百分點，基準年化多 4.2 個百分點，不對稱比由 0.66 升到 1.72。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與綜合訊號，前份對本份","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-06-15，股價 1,082.57 美元）估值結論 🔴，綜合訊號 B","side_b":"本份股價 881.26 美元，FY2026 共識本益比約 13 倍；估值結論改為 🟡，綜合訊號維持 B","ruling":"估值轉為中性，完全來自股價下跌約 19%；基本面沒有變好到值得升級，也沒有壞到需要降級。分母有爭議，所以價格下跌不轉成加分","evidence_level":"硬數據","settle_metric":"4Q26 與 1Q27 季淨營收","if_then":["若兩季淨營收各 ≥160 億美元，則估值結論可往偏便宜方向重評","若單季淨營收跌破 140 億美元，則以 2025 年 EPS 為分母重算，估值結論回到偏貴"],"evidence_refs":[]},{"axis":"前份未產出的欄位改由本份方法填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","rearm_trigger","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位皆為空值（舊格式未產出）","side_b":"本份：護城河方向 →、五年後成長空間 🟡、類型為金融、循環位置為晚循環、重新進場條件為事件錨；情境機率 20／50／30 與最大回撤 −28% 至 −50% 由本份情境樹產生；定期投入的裁決與角色由程式產出","ruling":"不是判斷改變，而是前份沒有這些欄位；本份是首次給值，下一份起才能比較漂移","evidence_level":"方法說明","settle_metric":null,"if_then":["若下一份任一欄與本份不同，則逐欄歸因到價格、新證據或方法"],"evidence_refs":[]},{"axis":"價值陷阱風險由 🟢 改為 🟡","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險 🟢","side_b":"本份 🟡：2025 年 EPS 成長 26.6%，遠高於營收的 8.9%；財報前 EPS 預估 17 次下修、0 次上修；3Q26 全球 M&A 量季減 41%；投行積壓已從五年高點回落","ruling":"採 🟡：一個衰退信號亮燈，加上活動轉弱的新證據；還不到 🔴，因為 3Q26 EPS 17.01 美元遠高於共識，管理費仍年增 22%","evidence_level":"硬數據","settle_metric":"FY2027 共識 EPS 在財報後是否續降","if_then":["若財報後共識再下修超過 5%，則改判 🔴，並把 Bear 機率調到 35%","若財報後共識回補到 70 美元以上，則維持 🟡"],"evidence_refs":["capital_markets_pricing#2","end_markets#5"]},{"axis":"Single Thing 由空白改為單季營收門檻","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"某一季全公司淨營收跌破 140 億美元（低於 2025 年季均約 146 億）","ruling":"Single Thing 新設：情境樹裡最大的單一敏感項是營收週期，所以用季營收的水位做二元事件；發生時減碼至半倉並重跑研究","evidence_level":"方法說明","settle_metric":"每季 8-K 淨營收","if_then":["若單季淨營收跌破 140 億美元，則減碼至半倉並重跑研究","若連兩季 ≥160 億美元，則依重新進場條件處理"],"evidence_refs":[]},{"axis":"減碼與清倉門檻、重新進場條件的變動","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份風險一的警戒：GBM 季度淨收入連 2 季 YoY < −15% → 減倉；風險二：年度募資 < 600 億美元連 2 年；風險三：P/TBV 跌破 1.5 倍；前份未設正式減碼門檻與重新進場條件","side_b":"全公司季淨營收連 2 季年減 >15% → 減碼；單季跌破 140 億美元 → 減碼至半倉；管理費年增 < 5% 連 2 季、年度募資 < 600 億美元連 2 年、P/TBV 跌破 1.5 倍三條沿用前份；新增撥備 > 7.5 億美元與 CET1 緩衝 < 50bp。重新進場改為：4Q26 與 1Q27 季淨營收各 ≥160 億美元且積壓不再下降","ruling":"把 GBM 口徑改成全公司口徑，因為全公司數字已含耐久收入的緩衝，更能反映股東實際承受的波動；前份三條門檻全部保留，其中 P/TBV 因事實表未涵蓋有形淨值，標為資料缺口而不退休；清倉只保留給訴訟出現刑事介入","evidence_level":"方法說明","settle_metric":"每季 8-K","if_then":["若連 2 季全公司營收年減 >15%，則減碼","若出現刑事介入或和解金額超過 50 億美元，則清倉檢討"],"evidence_refs":[]},{"axis":"投行積壓的說法：管理層對財報稿","cause":"新證據","prior_field":null,"side_a":"Q2 法說（2026-07-14，Solomon）：投行積壓升到五年最高；Q3 法說（2026-10-13，Solomon、Coleman）：積壓仍非常強勁，顧問的高額認列大致被股權承銷的補充抵銷","side_b":"3Q26 8-K：投行費用積壓較 2Q26 末下降，也較 2025 年底略降","ruling":"可調和，屬程度差異：以申報文件為準，積壓已從高點回落，管理層的用語偏樂觀。結論是 2027 年投行費用的年增會明顯放慢","evidence_level":"硬數據","settle_metric":"4Q26 投行費用與財報稿的積壓描述","if_then":["若 4Q26 財報稿稱積壓再降，則 Bear 機率調到 35%","若稱積壓回升，則維持現有機率"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"共識下修與財報大幅超預期","cause":"新證據","prior_field":null,"side_a":"財報前 30 天 EPS 預估 17 次下修、0 次上修；FY1 共識三個月內從 71.67 降到 67.78","side_b":"3Q26 EPS 17.01 美元，遠高於 LSEG 共識 13.02 美元；扣除慈善捐款前約 18 美元","ruling":"可調和：共識快照停在財報前的 10-08，尚未反映財報後的回補；但超預期部分包含偏高的績效費（管理層預期 4Q 仍偏高），可持續性未證。不採信也不否定，記為監測","evidence_level":"硬數據","settle_metric":"財報後下一份共識快照的 FY2026 與 FY2027 EPS","if_then":["若下一份快照的 FY2027 EPS 低於 70 美元，則確認下修趨勢，價值陷阱改判 🔴","若回到 73 美元以上，則撤回下修疑慮"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"]},{"axis":"Platform Solutions 指引落空","cause":"新證據","prior_field":null,"side_a":"Q2 法說（2026-07-14，Coleman）：Platform Solutions 下半年各季營收與 Q2 大致相當","side_b":"3Q26 Platform Solutions 營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合減值","ruling":"管理層的指引落空，但金額不到全公司營收 1%；記為前一輪資本配置失誤的尾巴，納入資本紀律風險的監測，不改變論點","evidence_level":"硬數據","settle_metric":"Apple Card 轉移完成與後續減值","if_then":["若 4Q26 再認列減值且金額超過 5 億美元，則資本配置評語下修","若轉移完成且無新減值，則結案"],"evidence_refs":["end_markets#3"]},{"axis":"觀望，或現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：3Q26 EPS 17.01 美元對共識 13.02 美元；耐久收入約 45%；M&A 領先差距創紀錄；贊助商 M&A 仍低於歷史均值，是尚未兌現的上行；全年募資上修到約 1,500 億美元；股價已從 6 月的 1,082 美元跌 19%，RSI 34","side_b":"等待的理由：分母處在週期高處，以 2025 年 EPS 計為 17.2 倍；投行積壓與全球 M&A 量已在回落；聯準會升息；Base 五年報酬年化只有約 5–6%，上下檔不對稱比率不到 2","ruling":"不可調和，選擇觀望。關鍵限制是不知道今年的獲利是不是週期頂點，而這要靠兩季財報的營收水位來解，不是靠價格","evidence_level":"硬數據","settle_metric":"4Q26 與 1Q27 季淨營收與投行積壓方向","if_then":["若 4Q26 與 1Q27 季淨營收各 ≥160 億美元且積壓不再下降，則重跑研究並建立首倉","若股價先漲回 1,000 美元以上而營收條件未到，則不追","若股價跌破約 763 美元（FY2027 共識 EPS 的 10.5 倍），而季營收仍 ≥150 億美元且撥備 ≤7.5 億美元，則分批反買","若季營收連 2 季年減 >15%，則不進場，並把 Bear 機率調到 35%"],"evidence_refs":["end_markets#5","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"季淨營收守在 150 億美元以上，驗證這是降溫而不是崩落","type":"假設驗證","maps_to":"H1","metric":"全公司季淨營收","threshold":"≥150 億美元","action":"維持觀望，等重新進場條件","source_freq":"每季 8-K","date":"2027-01"},{"n":2,"text":"資本市場回落轉為收縮","type":"風險","maps_to":"R1","metric":"全公司季淨營收年增率","threshold":"連 2 季 < −15%","action":"減碼；未持有則不進場","source_freq":"每季 8-K","date":null,"evidence_refs":["end_markets#5"]},{"n":3,"text":"單季營收跌回 2025 年季均以下","type":"Single Thing","maps_to":"Single Thing","metric":"全公司季淨營收","threshold":"單季 < 140 億美元","action":"減碼至半倉並重跑研究","source_freq":"每季 8-K","date":null,"evidence_refs":["end_markets#5"]},{"n":4,"text":"兩季財報證明谷底已經抬高","type":"估值rearm","maps_to":"H1","metric":"季淨營收與投行積壓方向","threshold":"4Q26 與 1Q27 各 ≥160 億美元，且積壓不再下降","action":"重跑研究後建立首倉","source_freq":"每季 8-K 與法說","date":"2027-04"},{"n":5,"text":"融資與放款的信用成本上升","type":"風險","maps_to":"R3","metric":"信用損失撥備","threshold":"單季 > 7.5 億美元","action":"停止加碼","source_freq":"每季 8-K","date":null},{"n":6,"text":"1MDB 證券集體訴訟或 CDS 反壟斷案出現不利和解或判決","type":"風險","maps_to":"R4","metric":"和解或判決金額","threshold":"> 50 億美元，或政府機關新立案","action":"減碼；若有刑事介入則清倉檢討","source_freq":"10-Q 法律程序揭露","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#1"]},{"n":7,"text":"資本紀律失守：大型收購或資本緩衝過薄","type":"風險","maps_to":"R2","metric":"單筆收購對價、CET1 高於要求的緩衝","threshold":"單筆 > 市值 5%（約 128 億美元），或緩衝 < 50bp","action":"停止加碼","source_freq":"8-K 與季報","date":null,"evidence_refs":["end_markets#3"]},{"n":8,"text":"價格先跌、基本面未壞時分批反買","type":"加碼","maps_to":"H1","metric":"股價與季淨營收、撥備","threshold":"股價 < 約 763 美元，且季營收 ≥150 億美元、撥備 ≤7.5 億美元","action":"分批反買","source_freq":"每日股價、每季 8-K","date":null},{"n":9,"text":"4Q26 財報後複審","type":"複審日期","maps_to":null,"metric":"全年財報與投行積壓","threshold":"財報公布","action":"重跑研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"全公司季淨營收","bear_threshold":"單季 < 140 億美元（低於 2025 年季均約 146 億）","window":"單季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"全公司季淨營收年增率","bear_threshold":"連 2 季 < −15%","window":"2 季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"管理及其他費用年增率","bear_threshold":"< +5% 連 2 季（沿用前份）","window":"2 季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"CET1 高於監管要求的緩衝","bear_threshold":"< 50bp","window":"單季","source":"每季 8-K 與法說","last_status":"ok"},{"metric":"信用損失撥備","bear_threshold":"單季 > 7.5 億美元","window":"單季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"另類資產年度募資","bear_threshold":"< 600 億美元連 2 年（沿用前份）","window":"2 年","source":"法說與 8-K","last_status":"ok"},{"metric":"股價對有形淨值倍數","bear_threshold":"跌破 1.5 倍連 2 季（沿用前份）","window":"2 季","source":"資料缺口：事實表未涵蓋有形淨值","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"4Q26 與 1Q27 季淨營收各 ≥160 億美元，且財報稿稱投行積壓不再下降","exec_line":"觀望：證據到齊後重跑研究，首倉不超過標準倉位的三分之一；價格先漲而證據未到則不追"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 4Q26 與 1Q27 財報：季淨營收各 ≥160 億美元，且投行積壓不再下降，證明 2026 年的獲利不是週期頂點"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-3.94, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資本市場從前十分位回到前四分位，是降溫而不是崩落：全公司季淨營收守在 150 億美元以上，M&A 宣布量維持第一","2y":"FY2027 全年淨營收 ≥600 億美元（FY2025 為 583 億）","5y":null,"10y":null,"threshold":"季淨營收 ≥150 億美元；年初至今 M&A 宣布量排名第一","source":"每季 8-K 財報稿與法說；全球 M&A 宣布量排行","drift_rule":"兩年期：TTM 淨營收低於 600 億美元，連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉"},{"id":"H2","text":"耐久型收入（管理費、融資收入）持續上升，把獲利谷底抬高","2y":"管理及其他費用季年增 ≥8%","5y":"管理及其他費用年化 ≥200 億美元；融資收入占 FICC 加股票營收跨週期維持 ≥40%","10y":null,"threshold":"3Q26 管理及其他費用 36 億美元，年增 22%；前三季融資收入 127 億美元，占比逾 40%；長期淨流入連續 35 季","source":"每季 8-K 與法說（Coleman，2026-10-13）","drift_rule":"五年期：管理費年增低於 8%，連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H3","text":"管理層守住資本紀律：跨週期 ROE ≥15%，多出來的資本退回股東，而不是再買進低回報的業務","2y":null,"5y":"五年平均 ROE ≥15%（2025 年為 15%，前三季 20.7%）","10y":null,"threshold":"滾動四季 ROE ≥15%；CET1 高於要求 50–100bp；單筆收購小於市值 5%","source":"每季 8-K；股東會（2026-04-29，Solomon）；10-Q","drift_rule":"五年期：滾動 ROE 低於 15%，連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本市場活動從前四分位繼續下滑：M&A 量已季減 41%，聯準會升息，IPO 動能在夏季後轉弱","h_ref":"H1","clock":"⚡","threshold":"全公司季淨營收連 2 季年減 >15% 則減碼","evidence_refs":["end_markets#5"]},{"id":"R2","text":"資本配置偏離：為了衝資產管理規模付出高價收購，或再度進入低回報業務；Platform Solutions 3Q26 仍在認列 Apple Card 減值，是前一輪擴張失誤的尾巴","h_ref":"H3","clock":"🔥","threshold":"單筆收購超過市值 5%，或 AWM 稅前利益率連 4 季低於 25%","evidence_refs":["end_markets#3"]},{"id":"R3","text":"股票融資與 AI 基建融資把資產負債表推大：一旦對沖基金去槓桿或大型融資案出問題，所謂的耐久收入會跟著週期一起下滑，信用損失也同時上升","h_ref":"H2","clock":"🔥","threshold":"單季撥備超過 7.5 億美元，或融資收入季減超過 15%","evidence_refs":[]},{"id":"R4","text":"法律與監管：1MDB 證券集體訴訟已認證集體（購買期間 2016-12-22 至 2018-11-08），CDS 結算價反壟斷案仍在進行，另有一件私人反壟斷訴訟與未具名的監管調查；金額與結案時點都在事實表未涵蓋","h_ref":"H3","clock":"🐢","threshold":"和解或判決金額超過 50 億美元，或政府機關新立案則減碼；刑事介入則清倉檢討","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#0"]}],"single_thing":{"description":"某一季全公司淨營收跌破 140 億美元（低於 2025 年季均約 146 億），代表資本市場從前四分位跌到中位數以下","why_fatal":"淨營收約七成來自投行與交易，費用又有剛性；營收回到 2025 年以下時，EPS 會從 68 美元掉到 46–50 美元，市場同時把倍數壓到約 10 倍，股價約 460–500 美元，比現價低約 45%。這是情境樹裡最大的單一敏感項","if_happens":"持有則減碼至半倉並重跑研究；未持有則延後任何進場，直到營收連兩季止跌","how_monitor":"每季 8-K 的淨營收；每月全球 M&A 宣布量與美國 IPO 件數；財報稿對投行積壓方向的描述","probability":"約 20%（12–24 個月）：M&A 量已季減 41%、聯準會升息、積壓從高點回落；但耐久收入約 45%，加上 3Q26 營收仍有 186.8 億美元，離門檻還有距離"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.13,"peg_fy2":0.85,"stress":{"pass":6,"total":7}},"eps_meta":{"base_eps_path":{"FY2025A":51.32,"FY2026E":67.78,"FY2027E":72.67,"FY2028E":76.73},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取自 Koyfin 2026-10-08 快照，分析師家數事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉","impact":"中","watch":"選後監管與併購審查態度是否轉向；Solomon 稱客戶並未因選舉觀望"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"Basel III 終局與 G-SIB 重提案是否在年底前定案","impact":"中","watch":"資本要求下降的幅度，以及回購空間是否擴大"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q26 財報與法說","impact":"高","watch":"季淨營收是否 ≥160 億美元、投行積壓方向、績效費與第二筆慈善捐款"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"1Q27 財報與法說","impact":"高","watch":"重新進場條件的第二季驗證；贊助商 M&A 是否開始回升"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
