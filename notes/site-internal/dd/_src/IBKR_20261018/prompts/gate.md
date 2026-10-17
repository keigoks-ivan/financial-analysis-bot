你是 DD 管線 v20 的判斷層閘（gate），標的 IBKR（20261018）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（33 條）
- `f_kpi0_gaap_yoy_15_6`（q1_business）｜GAAP 淨營收（YoY +15.6%）＝1914 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi6_yoy_19`（q1_business）｜淨利息收入（YoY +19%）＝1154 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi7_yoy_12`（q1_business）｜佣金收入（YoY +12%）＝602 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi3_gaap`（q1_business）｜稅前利益率（GAAP 與調整後皆）＝78 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi2_gaap`（q1_business）｜GAAP 稅前利益＝1496 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi8`（q1_business）｜客戶帳戶數＝5.576 百萬｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi9`（q1_business）｜客戶權益＝964.7 十億美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi10_darts`（q1_business）｜客戶 DARTs＝4.273 百萬｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi11`（q1_business）｜客戶保證金貸款餘額＝105.2 十億美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_peer_ibkr_operating_margin_pct`（q2_moat）｜IBKR 營業利益率＝86.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hood_operating_margin_pct`（q2_moat）｜HOOD 營業利益率＝46.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ibkr_gross_margin_pct`（q2_moat）｜IBKR 毛利率＝90.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hood_gross_margin_pct`（q2_moat）｜HOOD 毛利率＝81.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_schw_fcf_margin_pct`（q2_moat）｜SCHW FCF 利潤率＝41.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SCHW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi4`（q1_business）｜淨利（含非控制權益）＝1348 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_kpi12_0_0875`（q4_capital）｜季股息（由 0.0875 調升）＝0.15 美元／股｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[12]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1703.82 m shares｜期間與口徑：2026-10-18／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.7 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.26 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.71 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.25 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 2.59 → 2.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_kpi5_eps_gaap`（q4_capital）｜稀釋 EPS（GAAP／調整後）＝0.69 / 0.67 美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-15）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 3Q2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001381197/000138119726000154/ibkr-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-15））
  - 註記：查無共識數字（未採集）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.406 %｜期間與口徑：2026-10-18／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-18）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-94763.0 USD m｜期間與口徑：2026-10-18／yfinance 最新一季：總債務 35230.0、現金 129993.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_ibkr_fcf_margin_pct`（q2_moat）｜IBKR FCF 利潤率＝142.84 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝82.69 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.56 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝32.54 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 2.7，分子＝快照價 87.87｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝46125.51 USD m｜期間與口徑：2026-10-18／市值 140888.51 ＋ 淨負債 -94763.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝7438.69 USD m｜期間與口徑：2026-10-18／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝37.61｜期間與口徑：2026-10-16（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-16（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝1.39 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-16（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：IBKR FY2025 10-K 稱預期直接市場接取經紀業務競爭將持續加劇，競爭者含自建電子交易工具的 prime broker 及線上股票、選擇權／期貨經紀商
  - 來源：IBKR Form 10-K FY2025（as_of 2026-02-27）｜affects：decision_inputs.bear、moat_trend
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：二手來源稱 Interactive Brokers LLC 2025 年 7 月與 OFAC 以約 1,183 萬美元和解制裁違規（2016–2024）；來源為次級網站，未對照 OFAC 原文。
  - 來源：policyrisk.com IBKR 公司頁 / brokerchooser 監管頁（as_of 2025-07-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：搜尋中無 2026 年任何出口管制或實體清單點名 IBKR；唯一相關為 2025-07 OFAC 約 1,180 萬美元裁罰（對制裁地區人士提供經紀服務，含交易中國軍工複合體相關證券）
  - 來源：搜尋結果彙整（OFAC 2025-07 penalty，未取得原始頁面）（as_of 2025-07-01）｜affects：decision_inputs.bear、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因子列有「宏觀、地緣與其他挑戰與不確定性」及國際營運曝險（政治或經濟不穩、監管與央行政策變動），稱可能對業務、財務與經營結果造成重大不利影響；搜尋未見資料中心集中度或實體生產地的具體描述
  - 來源：SEC EDGAR, Interactive Brokers Group Form 10-K FY2025（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2020-12 IBKR 發生多段服務中斷，公司稱起因為第三方供應商提供的「高可用性」資料儲存系統故障，並將系統模組改接備援復原中心；匿名消息稱硬體故障位於 Equinix NY5（公司未證實）。為歷史事件，非現況單點認定
  - 來源：Bloomberg Law, Interactive Brokers Says Vendor Issue Tangled Trading; Bloomberg 2020-12-08（as_of 2020-12-08）｜affects：decision_inputs.bear、thesis.R
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：利率敏感度：10-Q 估計美元利率上升0.25%將使年化淨利息收入增加約8,100萬美元（反向降息則對淨利息收入不利）。
  - 來源：IBKR Form 10-Q for period ended 2026-06-30（as_of 2026-07-31）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：零佣金交易使定價壓力成為結構性，IBKR 雖未以免費為品牌仍處於此環境
  - 來源：Motley Fool: Can Interactive Brokers Maintain Its Edge in a Changing Brokerage Industry?（as_of 2026-02-28）｜affects：moat_trend、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 年報揭露：OFAC 制裁案於 2025 年 7 月結案，罰款 1,180 萬美元
  - 來源：Interactive Brokers Group Form ARS FY2025 (SEC)（as_of 2025-07-31）｜affects：decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 年報揭露：關於平倉部位的集體訴訟，和解協議於 2026 年 1 月簽署，公平聽證訂 2026-06-17（聽證結果未查到）
  - 來源：Interactive Brokers Group Form ARS FY2025 (SEC)（as_of 2026-01-31）｜affects：decision_inputs.bear
- `financial_capital_credit_cycle#0`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：IBKR 客戶應收款備抵信用損失於 2026 年 6 月底為 2,600 萬美元，2025 年底為 1,800 萬美元，增速快於應收款本身（二手分析，非 10-Q 原文）
  - 來源：finhacker.cz《Interactive Brokers v polovině roku 2026》（as_of 2026-06-30）｜affects：decision_inputs.bear、triggers
- `financial_capital_credit_cycle#1`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：FINRA 客戶保證金餘額 2026 年 7 月降至 1.417 兆美元，自 6 月紀錄高點 1.502 兆美元回落，為有紀錄以來最大單月降幅（二手轉載）
  - 來源：cryptobriefing《US margin debt drops $85B in July, largest monthly decline on record》（as_of 2026-07-31）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：平倉部位集體訴訟於 2026 年 1 月簽署和解協議，公平聽證訂 2026-06-17
  - 來源：Interactive Brokers Group Form ARS FY2025 (SEC)（as_of 2026-01-31）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":162.0,"bear_5y_price":51.2,"p_bull_pct":25,"p_bear_pct":25,"upside_5y_pct":25.6,"ev5y_pct":27.2,"irr_base_pct":4.7,"asym_ratio":2.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.7,"pe":30.63,"basis":"FY1（FY2026E）共識 EPS 2.70 美元，現價 82.69 美元；終端倍數以終端年 EPS 為分母，同為前瞻年度口徑"},"eps":{"bull":[3.35,3.95,4.6,5.3,6.0],"base":[3.2,3.62,4.0,4.36,4.72],"bear":[2.85,2.75,2.9,3.05,3.2]},"pe":{"bull":27,"base":22,"bear":16},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.406,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### IBKR_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜Paul Brody｜guidance：CFO 給出利率敏感度：Fed funds 升降 25bp 對年化淨利息收入影響各 8,100 萬美元（以 6/30 餘額為基準）（原話："$81 million increase in annual net interest income"）
- 2026-07-21｜Paul Brody｜guidance：非美元基準利率升降 25bp 對年化淨利息收入影響 3,800 萬美元（原話："by $38 million"）
- 2026-07-21｜Nancy Stuebe｜margin：稅前利潤率 77%，連續第七季高於 70%（原話："marking the seventh"）
- 2026-07-21｜Paul Brody｜margin：CFO 的毛交易利潤率口徑：執行清算成本佔佣金 17%，扣除 2,900 萬非交易成本（主要市場資料費）後算出 83%（原話："for a gross"）
- 2026-07-21｜Paul Brody｜margin：SEC 規費重啟使執行清算費用增加 1,900 萬至 3,400 萬，扣除後成長 7%；因轉嫁而不影響利潤（原話："do not impact profits"）
- 2026-07-21｜Paul Brody｜margin：薪酬佔調整後淨收入 10%，去年為 11%；員工 3,265 人（原話："Our head count at June 30 was 3,265."）
- 2026-07-21｜Paul Brody｜margin：G&A 成長，廣告擴張為因素之一（原話："continued expansion of advertising a contributing factor"）
- 2026-07-21｜Paul Brody｜margin：母公司調整後有效稅率 14.7%，低於常態區間，因股價上漲對員工股權計畫的稅務效果（原話："adjusted effective tax rate was 14.7%"）
- 2026-07-21｜Paul Brody｜margin：Fed funds 均值年減 70bp，但融資利息收入仍增 39%、隔離現金利息增 7%，皆由餘額支撐（原話："our margin loan"）
- 2026-07-21｜Paul Brody｜margin：證券借貸全口徑淨收入 3.43 億美元，年增 37%（含隔離現金中的證券借貸利息）（原話："would have been $343 million this quarter, up 37%"）
- 2026-07-21｜Paul Brody｜margin：NIM 表淨利息 11 億美元（年增 28%），與 GAAP 淨利息差在部分歸類於其他費用或其他收入的項目（原話："We include for NIM purposes, certain income"）
- 2026-07-21｜Paul Brody｜margin：投資組合存續期維持 30 天以內，因美元殖利率曲線短中段轉正而略拉長（原話："pushing out our duration a bit"）
- 2026-07-21｜Nancy Stuebe｜customer：新帳戶成長 34%，客戶閒置現金年增 27% 至創紀錄 1,820 億美元（原話："34% growth in new"）
- 2026-07-21｜Nancy Stuebe｜customer：客戶權益年增 40% 至 9,300 億美元（原話："Client equity rose 40% to $930 billion."）
- 2026-07-21｜Paul Brody｜customer：客戶 DARTs 為 480 萬筆／日，年增 36%；每筆可清算佣金訂單 2.64 美元，略低於去年（原話："up 36% from the prior year"）
- 2026-07-21｜Milan Galik｜customer：介紹經紀商管道：連續第四或五季有兩位數整合上線，進行中與已承諾整合數都多於上季；新進機構類型轉向既有業務公司（原話："The type of institutions we have been onboarding"）
- 2026-07-21｜Milan Galik｜customer：中國監管整頓 Tiger 與 Futu 後，IBKR 收到的轉戶帳戶與資產明顯增加，多為既有帳戶搬移資產；是否持續難說（原話："Hard to say whether"）
- 2026-07-21｜Milan Galik｜customer：管理層說明新帳戶成長下 DARTs 與每單佣金未稀釋，部分來自強勢環境，另受大型對沖基金與小帳戶介紹經紀商組合波動影響（原話："partially due to the strong environment."）
- 2026-07-21｜Milan Galik｜customer：被問帳戶成長區域，答覆為全球、全帳戶類型皆成長，未拆分韓國貢獻（原話："We are growing everywhere globally, all the regions"）
- 2026-07-21｜Nancy Stuebe｜product：IBKR 為首家開放韓國交易所與 Nextrade 的線上券商；韓國記憶體晶片股受客戶追捧（原話："We became the first e-broker to offer trading in Korea"）
- 2026-07-21｜Nancy Stuebe｜product：與 Anthropic、OpenAI、xAI 合作推出 IBKR Connector，客戶可將 AI 聊天機器人連接帳戶（原話："we released IBKR Connector in"）
- 2026-07-21｜Milan Galik｜product：AI 下單採 human-in-the-loop，客戶須核准後才成為可執行訂單（原話："we utilize the so-called human-in-the-loop"）
- 2026-07-21｜Milan Galik｜commitment：管理層表示未來某時點會提供完全自主的代理式交易，並設護欄與客戶測試，無時程（原話："We are going to be offering at some"）
- 2026-07-21｜Nancy Stuebe｜product：推出 IBKR Prediction Markets，整合 ForecastEx、CME 與 Kalshi，訂單路由至最佳淨價（原話："unified destination for trading event contracts"）
- 2026-07-21｜Milan Galik｜product：預測市場仍不提供體育與娛樂合約，專注於可能影響客戶投組的事件（原話："we still do not offer sports"）
- 2026-07-21｜Thomas Peterffy｜product：ForecastEx 將持續聚焦天氣類合約，正加入颶風登陸合約（原話："continue to concentrate on weather-related contracts"）
- 2026-07-21｜Milan Galik｜product：加密貨幣永續合約約佔加密貨幣交易量三分之一（原話："roughly 1/3 of the trading that we see is now coming"）
- 2026-07-21｜Nancy Stuebe｜product：夜盤交易量年增近三倍，由 380 萬筆增至 1,090 萬筆（原話："Overnight trading volumes nearly tripled year-over-year"）
- 2026-07-21｜Nancy Stuebe｜commitment：取得 OCC 對全國信託銀行執照的初步有條件核准，計畫年底前完成並上線（原話："We plan to have"）
- 2026-07-21｜Milan Galik｜capital_allocation：扣除各項緩衝後超額資本約 103 億美元，較上季增加約 11 億（原話："is around $10.3"）
- 2026-07-21｜Milan Galik｜capital_allocation：併購：投行寄來的標的信件大增，但目前沒有值得追求者（原話："nothing so far stood out as worthy pursuing it"）
- 2026-07-21｜Paul Brody｜capital_allocation：無長期債務；資產負債表設計為支持成長並考量整體資本配置（原話："We continue to"）
- 2026-07-21｜Thomas Peterffy｜competition：行銷支出提高後報酬率與以往大致相同，並未更高（原話："It is roughly the same."）
- 2026-07-21｜Thomas Peterffy｜risk：被問融資餘額快速成長是否有過度承險，答覆持續監控、對現有水準感到安心，未給數字（原話："we feel"）
- 2026-07-21｜Nancy Stuebe｜risk：客戶承擔更多風險（融資或衍生品部位），交易量成長（原話："clients taking on more risk through either"）
- 2026-07-21｜Milan Galik｜risk：對中國大陸監管：IBKR 不在大陸廣告，並檢查帳戶須證明居住地在大陸以外（原話："We do not"）
- 2026-07-21｜Thomas Peterffy｜commitment：管理層對帳戶成長率拒絕承諾，回憶過去給出 30% 目標後成長率反降至 20%（原話："we don't like to promise"）

### 問答異常語氣（迴避／改口／保留）
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Chubak：行銷策略演進是否支持帳戶成長結構性高於 20% 常態｜答法：Peterffy 先稱行銷報酬率與以往大致相同，再答「Yes, but we don't like to promise」，拒絕給成長率數字
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Chubak：融資餘額高速成長是否有過度承險跡象｜答法：Peterffy 僅答持續監控與「comfortable」，未提供任何指標或數字
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Budish：證券借貸強勁中 SpaceX 佔多少、對 Q3/Q4 的意涵｜答法：Brody 稱難以預測，未拆分 SpaceX 貢獻，改談借貸驅動因素與 stock yield enhancement
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Fannon：帳戶成長的區域來源、韓國是否為主要貢獻｜答法：Galik 答「全球皆成長」，未拆分區域或韓國貢獻
- IBKR_Q2_2026_Earnings_Call_20260721.md｜問：Hawken：韓國開放交易的量化影響｜答法：Galik 稱不提供按地區的交易量細節，僅定性描述「a line that goes straight up」

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 2 | 3 |
| financial_capital_credit_cycle | found | 3 | 3 |
| financial_regulatory_capital_rules | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Interactive Brokers Group IBKR largest customer concentration second-source OR in-house 2026；Interactive Brokers IBKR 10-K customer concentration clearing in-house technology proprietary 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260722","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"結構性帳戶複利延續：全球專業/散戶結構性增長 + B2B IB 通路上移 + 跨資產平台化，帳戶維持 >25% 成長、驅動 EPS 從 FY26 $2.60 至 FY28 $3.39","columns":{"2Y 驗證點":"帳戶 YoY 維持 >25%；客戶權益 YoY >20%","5Y 驗證點":"帳戶基數擴大後 YoY 自然放緩至 15-20% 但客戶權益複利延續","10Y 驗證點":"全球電子券商滲透續升、trust charter 託管 + 新資產類別擴 TAM","數字門檻":"帳戶 YoY >25% / 客戶權益 YoY >20% / FY28 EPS ≥ $3.3","來源":"Q2 26 帳戶 +34%、客戶權益 $930B +40%、Peterffy 重申 >30%（駁 20% 常態說）","漂移觸發":"帳戶 YoY 連 2 季"}},{"id":"H2","text":"NII 韌性：即使 Fed 降息，客戶餘額量增（margin loan、cash）抵消 rate 壓縮，NII 不結構性萎縮","columns":{"2Y 驗證點":"降息週期中季度 NII 不連 2 季 QoQ 下滑；margin loan/cash 餘額續增","5Y 驗證點":"NII 隨資產基數擴大而長期成長，rate 只是週期波動","10Y 驗證點":"NII 與 commission 雙引擎穿越 rate 週期皆成長","數字門檻":"NII QoQ 不連 2 季負；每 25bp −$81M 由量增抵消","來源":"Q2 26 NII $1.0B +23% YoY（avg funds −70bp 下仍增，量增抵）；sensitivity $81M/25bp USD","漂移觸發":"降息中 NII 連 2 季 QoQ 下滑（量增未抵）→ 削弱"}},{"id":"H3","text":"估值：市場為 34% 帳戶成長 + 77% 利潤的品質付 30x+，且此溢價可維持（不 de-rate）","columns":{"2Y 驗證點":"Fwd PE 維持 28x+（不跌破 5Y 中上緣）","5Y 驗證點":"倍數隨成長放緩自然回落至 5Y 中位 ~22x（re-rate 為報酬拖累）","10Y 驗證點":"成熟後倍數收斂至優質金融 18-22x","數字門檻":"Fwd PE ≥ 28x（樂觀維持）；本報告 Base 假設回 22x","來源":"賣方共識目標 ~$95-100（≈現價，無安全邊際）；5Y 分位 ~85%","漂移觸發":"共識 EPS 下修 + PE 跌破 22x → H3 反轉（進場窗開）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NII 週期反轉：Fed 2026H2–2027 加速降息（−100~150bp）壓 NII（−$320~480M 年化），若交易量同步退潮（無量增對沖）→ EPS 增速降、倍數重設","columns":{"對應假設":"H2/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fed funds 路徑、季度 NII QoQ、margin loan/cash 餘額增速、管理層 sensitivity 表","警戒閾值":"降息中 NII 連 2 季 QoQ 下滑 → 削弱；EPS 共識連 2 季下修 → 立即重評倍數"}},{"id":"R2","text":"估值均值回歸：Fwd PE 自 85 分位 / 31x 下修回 5Y 中位 ~22x（即使 EPS 續增，倍數壓縮吞報酬）","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fwd PE 5Y 分位、共識 EPS 修正方向、賣方目標 vs 現價","警戒閾值":"PE 跌破 25x 且 EPS 未同步上修 → de-rating 進行中"}},{"id":"R3","text":"交易量週期 + 成長品質：DARTs 目前受市場熱度（波動、SpaceX IPO）拉高，退潮則走平；marketing yield 未隨支出提升（成長非來自行銷效率）→ 帳戶增速若減，複利敘事鬆動；China 資產轉入（Tiger/Futu）durability 管理層自認「難說」","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"DARTs、commission/order、帳戶淨增、marketing yield","警戒閾值":"DARTs 連 2 季下滑 + 帳戶 YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","irr_base_pct":7.0,"ev5y_pct":39.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":39.0,"irr_base_pct":7.0,"max_dd_pct":-45.0,"bull_5y_price":175.0,"bear_5y_price":58.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","price_at_dd":94.42,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"IBKR","date":"2026-10-18","schema":"v15.0","contract":"v19","company_name":"Interactive Brokers Group"},"oneliner":"全球低成本券商，帳戶年增 35%、稅前利益率 78%，生意品質一流；但現價對 FY2026 共識為 30.6 倍本益比，已計入三年約 19% 的盈餘成長。交易熱度退潮與利率轉向是主要下行，等 72 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/scenario.json","answers":{"q1_business":{"verdict":"賺全球主動投資人與介紹經紀商的錢，錢卡在兩個節點：客戶融資與客戶現金的利差（淨利息收入約占淨營收 60%），以及交易佣金（約 31%）。","reasoning":"Q3 GAAP 淨營收 19.14 億美元，年增 15.6%。其中淨利息收入 11.54 億美元（+19%），佣金 6.02 億美元（+12%），其他費用與服務 8,800 萬美元（+33%）。稅前利益率 78%，連續八季高於 70%；薪酬只占調整後淨收入 9%，員工 3,286 人服務 557.6 萬戶。產業時鐘判在 II 擴張：帳戶年增 35%、客戶權益年增 27%、融資餘額年增 36%，仍在擴張；但交易熱度自 2026 年 6 月高點降溫（DARTs 年增率由 6 月 53% 降到 9 月 6%，法說會稱每戶交易降到近期低點且全客群皆然），屬擴張後段。供需持久性分兩層：帳戶與客戶資產屬結構性持久，交易量與融資餘額屬週期性、將隨市場熱度反轉。議價權：上游交易所與監管費用多數轉嫁客戶（Q3 SEC 規費 3,000 萬美元同時推高佣金與成本，不影響利潤）；下游客戶價格敏感，公司的議價力來自最低成本，而不是加價能力。單點依賴：無單一客戶集中（10-K 稱無營業常規以外的重大信用集中），真正的集中風險是利率——每 25bp 對年化淨利息收入約 8,300 萬美元（美元）加 3,500 萬美元（非美元）。","fact_refs":["f_kpi0_gaap_yoy_15_6","f_kpi6_yoy_19","f_kpi7_yoy_12","f_kpi3_gaap","f_kpi2_gaap","f_kpi8","f_kpi9","f_kpi10_darts","f_kpi11"],"verdict_values":{"revenue_quality":"以經常性利差為主，由客戶餘額與利率雙驅動；佣金隨交易熱度波動，每單佣金 2.59 美元年減 4%。","unit_econ_note":"稅前利益率 78%、毛交易利潤率 83%、薪酬比 9%；高度自動化使新增帳戶的邊際成本極低。","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"高","fingerprint":"券商：利差加佣金雙引擎、單一全球平台、高自動化低成本、無長期負債"},"industry":{"clock_phase":"II","sd_verdict_source":"帳戶與客戶資產屬結構性持久；交易量與融資餘額屬週期性，將反轉（FINRA 全市場融資餘額 7 月創紀錄單月降幅）","bargaining":{"up":"交易所與監管費用多數轉嫁客戶，上游無法擠壓利潤","down":"客戶為價格敏感的主動交易者，公司以最低收費定位，議價力來自成本","geo":"約 30% 利率敏感餘額為非美元；各地區營收占比事實表未涵蓋"},"profit_pool_dir":"零售券商利潤往規模化、低成本平台集中；公司營業利益率 86.5%，Robinhood 為 46%","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球線上券商帳戶總數與滲透率，無法建 TAM 表；以帳戶、客戶權益與融資餘額增速代替份額擴張證據"}}}},"q2_moat":{"verdict":"穩定：低成本自動化的規模優勢在執行面仍在擴大，但每單佣金下滑讓定價面小幅縮減，兩者相抵。","reasoning":"機制只有一條：單一全球平台加上高度自動化，使每多服務一戶的成本趨近於零，進而能以最低價搶客並維持 78% 稅前利益率。可證方向的同業對照：營業利益率公司 86.5%、Robinhood 46%，毛利率 90.2% 對 81.5%；事實表無同業 ROIC，也無 Schwab 的營業利益率。執行面擴大的證據：帳戶年增 35%；介紹經紀商管道連續數季穩定上線（韓國 Daol 白牌平台 Q3 上線）；夜盤交易量由 350 萬筆增至逾 1,000 萬筆。定價面縮減的證據：每單佣金年減 4%，公司歸因於單筆規模變小；零佣金環境下定價壓力屬結構性。報酬持續期方面，年化 ROE 約 23%，判在高利益率、低周轉象限（資產 2,430 億美元、權益 233 億美元）；四個檢查點兩綠兩黃。再投資方面，股息約占淨利 19%、無回購，再投資率約 81%，內生上界約 18.8%；但超額監管資本 142 億美元遠高於需求 36 億美元，保留盈餘多數並未被業務使用，這個上界高估了實際可用的再投資機會。","fact_refs":["f_peer_ibkr_operating_margin_pct","f_peer_hood_operating_margin_pct","f_peer_ibkr_gross_margin_pct","f_peer_hood_gross_margin_pct","f_peer_schw_fcf_margin_pct","f_kpi3_gaap","f_kpi8","f_kpi4","f_kpi12_0_0875","f_shares_diluted_m"],"verdict_values":{"moat":{"mechanism":"單一全球多資產平台加高度自動化，帶來最低成本；介紹經紀商白牌接入後遷移成本高","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：帳戶年增 35%、介紹經紀商管道穩定、Daol 白牌上線。定價面小幅縮減：每單佣金 2.59 美元，年減 4%。兩者相抵為穩定。","competitor_notes":[{"name":"Charles Schwab","strategy_note":"大型既有業者，以顧問託管與存款利差為主，是價格競爭與 RIA 託管的主要對手；事實表只有 FCF 利潤率 41%，無法比營業利益率"},{"name":"Robinhood","strategy_note":"營業利益率 46%，對公司的 86.5% 有成本結構差距；以簡化開戶與產品速度搶美國年輕散戶，與公司的國際及機構客群重疊小"},{"name":"Fidelity","strategy_note":"對 RIA 設 1 億美元資產門檻，2027 年中生效（2026-10-15 法說會 Galik 引述），小型 RIA 需另找託管，對公司是份額窗口"},{"name":"Coinbase","strategy_note":"申請代幣化股票，屬增量威脅；公司以穩定幣入金回應，代幣化對公司是疊加在既有清算與保證金系統上的服務"}],"peer_na_reason":"事實表無同業 ROIC 與 Schwab 營業利益率，改以 Robinhood 營業利益率與毛利率對照","threats":[{"level":"🟡","text":"零佣金環境的結構性定價壓力，加上 10-K 稱直接市場接取業務競爭將持續加劇；每單佣金已年減 4%","p":"25%","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"level":"🟡","text":"加密原生平台推代幣化股票，若散戶轉向以代幣化方式持股，可能繞過傳統券商","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"系統中斷：2020 年 12 月曾因第三方儲存系統故障多段停擺；全自動平台一旦停擺，客戶信任受損","p":"10%","evidence_refs":["geo_supply_chain#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多為同一個主動投資人；全球投資人想直接持有美國科技股並低成本換匯，屬「需要」而非「想要」。代理讀數：帳戶 557.6 萬戶（+35%）、客戶權益 9,647 億美元（+27%）"},{"item":"決策層級","level":"🟡","text":"在單一客戶層級換券商成本低，零佣金對手隨手可得；但對需要全球多資產接取、保證金與證券借貸的主動交易者難以替代。介紹經紀商整合後遷移成本高。流失率與續約率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟢","text":"交易所與監管費用轉嫁客戶，公司自營清算、託管與融資，拿走利差與佣金；稅前利益率 78% 顯示在價值鏈中分配位置強"},{"item":"社會容忍度","level":"🟡","text":"公司刻意壓低收費，未把價格推到經濟上限；但跨境經營依賴各地監管授權：OFAC 制裁案 1,180 萬美元和解、中國大陸整頓同業、日本帳戶遷移仍在與監管溝通，政策風險屬中等"}],"roiic":"約 23%（年化 Q3 淨利 53.9 億美元 ÷ 帳面權益 233 億美元，以平均報酬近似；增量口徑事實表未涵蓋）","reinvest_rate":"約 81%（年股息 0.60 美元 × 17.04 億股 ≈ 10.2 億美元，約占淨利 19%；無回購、無併購）","endo_ceiling":18.8,"formula_note":"內生上界＝23.1% × 81% ≈ 18.8%。券商盈餘成長主要由客戶餘額與利率驅動，自有資本多為監管緩衝（超額 142 億美元），上界只作參考，不代表資本的實際使用效率"}}}},"q3_growth":{"verdict":"五年後跑道中等：帳戶增速會隨基數放大自然放緩；RIA 與介紹經紀商是看得見的第二通路，但規模仍小（RIA 稅務感知策略資產約 3 億美元），尚不足以判為下一條成長曲線。","reasoning":"成長來源以量為主：帳戶、客戶資產、融資與現金餘額。利率屬價格因素，為輔；沒有併購，也沒有回購。三年共識 EPS 由 FY2025 實際 2.22 美元到 FY2028 3.71 美元，年複合約 18.7%（Koyfin 2026-10-08 快照），與內生上界約 18.8% 幾乎重合，缺口約為零，不需要靠倍數重估解釋。但這組盈餘對交易熱度與利率高度敏感：Q2 DARTs 480 萬筆、年增 36%，Q3 降到 427 萬筆、年增 18%，9 月只剩年增 6%。管理層把 Q2 的熱度部分歸因於 IPO 與市場環境（2026-07-21 法說會 Galik），Q3 又以期中選舉波動作為回升理由，屬未證歸因。第二通路：Fidelity 2027 年中對小型 RIA 設門檻，公司自認是明顯的承接者；介紹經紀商管道與前兩季相近；預測市場與 AI 自主交易仍在早期。滲透率事實表未涵蓋，跑道年數無法量化。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi8","f_kpi9","f_kpi11","f_kpi10_darts"],"verdict_values":{"growth":{"driver_mix":"量（帳戶與餘額）為主、利率為輔；無併購、無回購","runway_years":"事實表未涵蓋全球滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 18.8%（年化 ROE 約 23% × 再投資率約 81%）；三年共識 EPS 年複合約 18.7%，落在上界內","segments":{"expanded":false,"reason":"公司不分部揭露；收入由淨利息（約 60%）、佣金（約 31%）、其他費用（約 5%）組成，已寫在怎麼賺錢一題，利潤由利率與餘額決定，而非分部組合"},"decay_signals":["毛利率連兩季年減：未亮（稅前利益率 78%，連八季高於 70%）","核心市占縮減：未亮（帳戶年增 35%）","提價後銷量下滑：不適用（公司未提價）","EPS 成長顯著高於營收成長：未亮（FY2022–2025 EPS 年複合約 33%，營收約 35%）","FCF 對淨利低於 0.75：不適用（券商現金流含客戶餘額變動，FCF 利潤率 142% 無意義）","SBC 占營收高於 5% 且上升：資料缺口（事實表未涵蓋）","TAM 萎縮或被替代：未亮（代幣化屬增量威脅）","產業倍數系統性下移：資料缺口","維護性資本支出占 FCF 過高：不適用","停止投資且營收下滑：未亮"],"trap_rating":"🟢"}}},"q4_capital":{"verdict":"資本配置以保留盈餘擴充資本加股息為主：股息改按市值 0.5%–1% 的指引大幅調升，無回購、無併購、無長期負債。","reasoning":"季股息由 0.0875 美元調升至 0.15 美元（+71%），年化 0.60 美元，以現價計殖利率約 0.73%。Peterffy 說明股息依市值 0.5%–1% 指引，此前落後所以補上，並稱想像不到會減息的情境（2026-10-15 法說會）。公司權益年增 19% 至 233 億美元，無長期負債。6 月底各營運子公司合計超額監管資本 142 億美元。Q2 法說會稱扣除緩衝後超額資本約 103 億美元，併購標的雖多但無值得追求者。FCF 對淨利的轉換率在券商不具意義：FCF 利潤率 142% 來自客戶餘額流入，不是自由現金。SBC 與股數年增率事實表未涵蓋，稀釋項目無法判定通過與否。","fact_refs":["f_kpi12_0_0875","f_kpi5_eps_gaap","f_dividend_yield_ttm","f_net_debt_m","f_peer_ibkr_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無重大併購；Q2 法說會稱標的多但無值得追求者"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無回購計畫，資本回饋只走股息（年 0.60 美元）"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"事實表未涵蓋 SBC 與總股數年增率；A 類股數增加主要來自 LLC 單位轉換，不等於經濟稀釋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有股息，回購為零，現金去向結構單純"}}}},"q5_valuation":{"verdict":"現價要求 FY2026–2028 EPS 年增約 19% 兌現，且倍數守在 25 倍上下；盈餘路徑可信，倍數不可信，結論偏貴。","reasoning":"現價 82.69 美元，對 FY2026 共識 EPS 2.70 美元為 30.6 倍，對 FY2027 共識 3.26 美元為 25.4 倍；trailing 本益比 31.6 倍，高於事實表四個年度端點的全部（分位 100，非五年分位）。券商尺：帳面權益 233 億美元，市值 1,409 億美元，P/B 約 6.0 倍；年化 ROE 約 23%，以資金成本 10%、長期成長 7% 推出合理 P/B 約 5.3 倍，現價略高；但長期成長若取 8%，合理值升到 7.5 倍，結論對成長假設很敏感。基準情境終端 22 倍下，年化報酬約 5%，未達 8%。賣方目標價分歧大：10 月初 Benzinga 平均約 80 美元（全距 25–116 美元），9 月頁面平均約 110 美元，最高與最低相差逾 2.5 倍，因此本判斷的報酬估計信心下調。近 3 個月 FY2026 共識上修 4.25%，盈餘方向向上，壓力在倍數不在盈餘。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_dividend_yield_ttm","f_consensus_rev_3m_fy1_pct","f_ev_m","f_rev_consensus_fy1_m"],"verdict_values":{"valuation":{"basis":"Fwd P/E 為主；P/B 對 ROE 為輔（券商）","tier":"優質券商","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，無同業 Fwd P/E 或 P/B；終端倍數改以優質金融 18–22 倍區間與自身歷史端點對照，屬資料缺口"},"fwd_pe":30.6,"peg":1.64,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 本益比 30.6 倍、FY2027 本益比 25.4 倍；三年 EPS 年複合 18.7%，PEG 約 1.6。trailing 本益比高於四個年度端點全部（只有四點，無法算五年分位，故分位留空）。P/B 約 6.0 倍，高於以 ROE 23%、成長 7% 推出的 5.3 倍。基準情境年化報酬約 5%，未到 8%；一年後以 FY2027 基準 EPS 3.20 美元 × 26 倍計約 83 美元，幾乎無上檔。結論：偏貴，未到泡沫","upside_short_pct":0.6,"upside_mid_pct":5.1,"denominator_disputed":false,"denominator_note":"EPS 分母無一次性爭議（GAAP 0.69 美元與調整後 0.67 美元的差異來自貨幣分散策略損益）。營收倍數分母口徑不一：年度營收含總利息收入，共識為淨營收，P/S 與 EV/S 不作估值錨"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把 2026 年中的交易熱度與融資高峰當成長期基準，而倍數早已按這個基準定價。","reasoning":"主要風險有兩個方向。其一，交易熱度退潮與融資去槓桿同時發生：9 月 DARTs 只年增 6%，股票成交量年減 24%，全市場融資 7 月創紀錄單月降幅，公司客戶信用損失備抵由 1,800 萬升到 2,600 萬美元。其二，聯準會若從 9 月升息急轉為降息，淨利息收入的敏感度會反向放大。管理層迴避紀錄：Q2 被問融資快速成長是否過度承險，只答持續監控、感到安心，未給任何指標；被問帳戶成長能否結構性高於 20%，拒絕承諾；被問區域與韓國貢獻，不拆分。Q3 被問其他國家擴張計畫，拒答。動能面：RSI 37.6，26 週報酬 1.4%，沒有過熱。","fact_refs":["f_rsi14","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_kpi10_darts","f_kpi11"],"verdict_values":{"trap":{"verdict":"🟢","label":"非價值陷阱：盈餘來自帳戶與餘額的實質成長，衰退信號未亮；風險在倍數與週期，不在生意變質"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.7,"pe":30.63,"basis":"FY1（FY2026E）共識 EPS 2.70 美元，現價 82.69 美元；終端倍數以終端年 EPS 為分母，同為前瞻年度口徑"},"valuation_basis":"eps_pe","eps":{"bull":[3.35,3.95,4.6,5.3,6.0],"base":[3.2,3.62,4.0,4.36,4.72],"bear":[2.85,2.75,2.9,3.05,3.2]},"pe":{"bull":27,"base":22,"bear":16},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.73,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":8},"max_dd":{"lo":-55,"hi":-35,"basis":"Bear 終點約 −38% 為參考下限。路徑上倍數可能先於盈餘崩落：30.6 倍若壓至 Bear 的 16 倍，同時 EPS 回落至約 2.75 美元，價格約 44 美元（約 −47%）。交易與融資同步退潮的那一季最可能觸發。事實表未涵蓋歷史最大回撤，無法用實績校準，故區間放寬到 20pp","trigger_time":null},"basis":{"bull":"帳戶年增維持 25% 以上，介紹經紀商與 RIA 新通路放量，利率持平偏升；EPS 年複合約 17%，終端 27 倍","base":"前兩年略低於共識（交易熱度退潮），其後帳戶增速自然放緩，EPS 年增降到約 8%；倍數回到優質金融的 22 倍","bear":"聯準會轉向降息，交易與融資同步退潮，FY2028 EPS 回落；終端 EPS 3.20 美元低於 FY2027 共識，倍數以成長降至約 5% 的成長熄火情境定為 16 倍"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"9 月 DARTs 只年增 6%（6 月為 53%）；每戶交易降到近期低點，且全客群皆然；全市場融資 7 月創紀錄單月降幅；公司客戶信用損失備抵由 1,800 萬升到 2,600 萬美元；利率每 25bp 約影響 8,300 萬美元淨利息收入","assumption":"帳戶與餘額的結構性成長足以抵消交易熱度與利率的週期反轉","consequence":"交易退潮、融資去槓桿、降息三者同時發生，佣金與淨利息收入同步下滑，倍數由 30 倍壓到 15–16 倍，五年後虧損接近 50%","ruling":"部分採納。帳戶年增 35%、客戶權益年增 27% 提供緩衝，但倍數壓縮風險真實；Bear 機率維持 25%，回撤區間下限取 −55%。與唯一致命點部分重疊（急降息是共同觸發），本條補上交易與信用兩條路徑","watch":"月度 DARTs 年增率、期末融資餘額季變動、信用損失備抵、Fed funds 路徑","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#4"],"fact_refs":["f_kpi10_darts","f_kpi11","f_kpi6_yoy_19"]},{"view":"論點成功但股東經濟變差","evidence":"G&A 增加主因是廣告擴張；Q2 Peterffy 稱行銷報酬率與以往大致相同，Q3 稱 X 合作帶來的新客價值較高但數量較少；每單佣金年減 4%；零佣金環境下定價壓力屬結構性","assumption":"帳戶成長不需要靠持續加碼行銷與降價購買","consequence":"帳戶數照樣成長，但每戶佣金與獲客成本惡化，利益率從 78% 往下滑，股東拿到的每股盈餘成長慢於帳戶成長","ruling":"反駁為主。薪酬比 9%、G&A 僅 7,800 萬美元，廣告增量相對 19 億美元的季營收很小；每單佣金下滑公司歸因於單筆規模變小，屬未證、監測。若連兩季稅前利益率低於 70%，即代表本歸因被證偽","watch":"稅前利益率、每單佣金、G&A 占淨營收比","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"],"fact_refs":["f_kpi3_gaap","f_kpi7_yoy_12"]},{"view":"價格已反映太多","evidence":"FY2026 本益比 30.6 倍；trailing 本益比高於四個年度端點全部；P/B 約 6.0 倍，高於以 ROE 推出的約 5.3 倍；10 月初賣方平均目標價約 80 美元，低於現價","assumption":"市場會持續為 35% 的帳戶成長與 78% 的利益率付 25 倍以上","consequence":"即使 EPS 照共識成長，倍數回到 22 倍也會吃掉大部分報酬，基準年化報酬只剩約 5%","ruling":"採納，這是本次的主要約束。股價雖已較前份下跌 12%，盈餘也上修，仍不足以讓基準報酬達到 8%","watch":"FY2027 共識 EPS 與股價的比值；股價 72 美元","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 94.42 → 本次 82.69（-12.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=94.42","side_b":"本次 price_at_dd=82.69","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 94.42 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 94.42 美元：Bull 價 175、Bear 價 58，五年期望值 +39.0%，基準年化 7.0%，不對稱比 3.0","side_b":"本次情境、股價仍用 94.42 美元：Bull 價 162、Bear 價 51.2，五年期望值 +11.4%，基準年化 1.9%，不對稱比 1.56","ruling":"先換情境、股價不動：五年期望值少 27.6 個百分點，基準年化少 5.1 個百分點。不對稱比由 3.0 變為 1.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 94.42 美元：五年期望值 +11.4%，基準年化 1.9%，不對稱比 1.56","side_b":"本次情境、股價 82.69 美元：五年期望值 +27.2%，基準年化 4.7%，不對稱比 2.52","ruling":"再換股價、情境不動：起點價下跌 12.4%，五年期望值多 15.8 個百分點，基準年化多 2.7 個百分點，不對稱比由 1.56 升到 2.52。合計五年期望值比前份少 11.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"帳戶成長對交易熱度","cause":null,"prior_field":null,"side_a":"帳戶年增 35%、客戶權益年增 27%，創新高","side_b":"DARTs 季減 11%，9 月只年增 6%；法說會稱每戶交易降到近期低點且全客群皆然","ruling":"可調和，屬程度差異。帳戶是結構，交易熱度是週期；EPS 對淨利息收入的敏感度大於佣金，因此盈餘受交易退潮的傷害有限，但倍數會受影響","evidence_level":"高（公司季報與月度指標）","settle_metric":"季度 DARTs 季變動與帳戶年增率","if_then":["若 DARTs 季度再降 ≥10% 且帳戶年增仍 ≥25%，則維持論點、不追價","若帳戶年增也跌破 25%，則停止任何加碼計畫"],"evidence_refs":["end_markets#1","end_markets#2"]},{"axis":"融資餘額口徑","cause":null,"prior_field":null,"side_a":"期末融資餘額 1,052 億美元，低於 6 月底約 1,085–1,089 億美元，季減約 3%","side_b":"2026-10-15 法說會 Paul Brody 稱融資餘額年增 47%、季增 8%（應為平均餘額口徑）","ruling":"可調和：平均餘額與期末餘額的差異，表示季中衝高、季末回落，與全市場 7 月去槓桿方向一致。不可據此稱去槓桿已結束","evidence_level":"中（期末為新聞稿，平均為口述）","settle_metric":"Q3 10-Q 的平均與期末融資餘額","if_then":["若 Q4 期末融資餘額再季減 ≥5%，則把融資去槓桿視為進行中，Bear 機率上調至 30%","若回升至 1,100 億美元以上，則維持現有機率"],"evidence_refs":["financial_capital_credit_cycle#2","financial_capital_credit_cycle#1"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭面惡化：10-K 稱直接市場接取業務競爭將持續加劇，零佣金定價壓力屬結構性，每單佣金年減 4%","side_b":"結構面轉好：Fidelity 將對 1 億美元以下 RIA 設門檻，中國大陸整頓 Tiger、Futu 帶來轉戶；其他結構變數方面，利率由降轉升（聯準會 9 月中升息）","ruling":"雙向拉鋸。競爭壓力只壓每單價格，未壓帳戶份額；RIA 與轉戶是可觀察的份額窗口","evidence_level":"中","settle_metric":"帳戶年增率與每單佣金","if_then":["若每單佣金年減擴大到 10% 以上且帳戶增速同步放緩，則把護城河趨勢下修一檔"],"evidence_refs":["competitive_share_entrants#2","substitute_technology#2","supply_demand_durability#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：帳戶年增 35%、稅前利益率 78%、無長期負債；FY2027 本益比 25.4 倍對三年 19% 成長，PEG 約 1.4；聯準會 9 月升息對淨利息收入是順風；Fidelity 的 RIA 門檻提供份額窗口；股價已較前份下跌 12%，RSI 37.6","side_b":"等待方：基準情境終端 22 倍下年化報酬約 5%，未達 8%；倍數高於歷史端點；交易熱度正在退潮","ruling":"選等待方。依據是基準報酬未過 8%，這是價格問題，不是論點問題，兩邊可調和","evidence_level":"中","settle_metric":"股價對 FY2027 共識的倍數","if_then":["若股價 ≤72 美元（約 FY2027 共識 22 倍）且帳戶年增 ≥25%，則建首倉 2%","反向：若 FY2027 共識上修到 ≥3.5 美元而股價仍 ≤85 美元，同樣建首倉 2%","若股價先漲到 95 美元以上而 FY2027 共識未上修，則不追"],"evidence_refs":[]},{"axis":"賣方目標價分歧","cause":null,"prior_field":null,"side_a":"Benzinga 2026-10-07：16 位分析師平均目標價約 80 美元，全距 25–116 美元","side_b":"Benzinga 2026-09：12 位分析師平均約 110 美元；UBS 101 美元、Barclays 115 美元","ruling":"不可裁決，來源未說明差異原因。最高與最低相差逾 2.5 倍，因此本判斷的報酬估計信心下調，不引用共識目標價作進場依據","evidence_level":"低","settle_metric":"下一次賣方目標價彙整","if_then":["若主流券商目標價下修至現價以下且 EPS 共識同時下修，則 Bear 機率上調至 30%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-07-21 Q2 法說會：Paul Brody 給出美元每 25bp 8,100 萬、非美元 3,800 萬的敏感度；Galik 把 DARTs 強勢部分歸因於環境；Peterffy 稱行銷報酬率與以往相同","side_b":"2026-10-15 Q3 法說會：敏感度改為 8,300 萬與 3,500 萬；Galik 把交易放緩歸因於 IPO 延後，並預期期中選舉帶來波動；Peterffy 稱 X 合作新客數量少","ruling":"說法一致、未改口；敏感度變動來自餘額基準。交易回升歸因於選舉波動屬未證，預登記：若 2026 年 11–12 月月度 DARTs 年增仍低於 10%，即視為此歸因被證偽","evidence_level":"中","settle_metric":"2026 年 11–12 月月度 DARTs 年增率","if_then":["若 11–12 月 DARTs 年增 <10%，則把 FY2027 基準 EPS 由 3.20 美元下修至 3.10 美元重跑"],"evidence_refs":[]},{"axis":"前份漂移：價格變動","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 94.42 美元，FY2026 EPS 約 2.60 美元，本益比約 36 倍，估值偏貴；機率 25/50/25；最大回撤 −45%","side_b":"本次股價 82.69 美元（−12%），FY2026 共識 2.70 美元，本益比 30.6 倍，估值仍偏貴；機率維持 25/50/25；回撤改為區間 −35%～−55%（涵蓋前份 −45%）","ruling":"價格下跌與盈餘上修共同壓低倍數，但未跨過合理門檻；裁決與角色由決策矩陣依本次輸入重算","evidence_level":"高","settle_metric":"FY2026 本益比","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：新證據","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"前份：訊號 B、陷阱低、護城河穩定、五年後跑道中等","side_b":"Q3 新資料（帳戶 +35%、稅前利益率 78%、每單佣金 −4%、9 月 DARTs +6%、RIA 稅務感知策略資產 3 億美元）未推翻任何一欄，四欄皆維持","ruling":"維持。新證據兩面都有，執行面擴大與定價面縮減相抵","evidence_level":"高","settle_metric":"帳戶年增率與每單佣金","if_then":[],"evidence_refs":["end_markets#2","substitute_technology#2"]},{"axis":"前份漂移：方法沿用","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：金融類；循環位置未設","side_b":"本次沿用金融類券商尺（Fwd P/E 為主、P/B 對 ROE 為輔），不套循環股的位置判斷","ruling":"不變。公司盈餘雖受交易週期影響，但核心是餘額與利差，不屬商品循環","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件變動","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","side_b":"股價 ≤72 美元（基準年化報酬回到 8%，約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS ≥3.5 美元而股價 ≤85 美元","ruling":"估值rearm 改為單一價格錨並綁定論點驗證。原因：主要約束是價格，觀望錨應為價格錨。移除技術線分支（價格已到 82 美元附近，但基準報酬仍不足）。移除淨利息收入韌性分支（Q3 已證明，不再是約束）。新增盈餘上修分支作為反向的加碼路徑","evidence_level":"中","settle_metric":"股價與 FY2027 共識","if_then":["觸及任一分支，則建首倉 2%，第二批等 Q4 財報確認帳戶年增 ≥25% 再加碼"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Single Thing：危機型衝擊觸發聯準會急降息，Fed funds 於 12 個月內降至 2% 以下","ruling":"新設。淨利息收入約占營收 60%，利率是 EPS 對單一變數最大的敏感度，大於佣金波動","evidence_level":"高（公司揭露的敏感度）","settle_metric":"Fed funds 有效利率","if_then":["若發生，則減碼至三分之一"],"evidence_refs":["end_markets#4"]},{"axis":"kill 指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標（null）","side_b":"新設五條：帳戶年增連 2 季 <20%、淨利息收入年增轉負且連 2 季季減、Fed funds 12 個月內降至 2% 以下、月度 DARTs 年增連 3 個月 <0、信用損失備抵單季增 ≥1 億美元","ruling":"補上前份缺少的減碼與清倉門檻，持有時以此執行","evidence_level":"中","settle_metric":"各指標","if_then":["帳戶與淨利息收入兩條同時觸發，則清倉；任一條觸發，則減碼至半倉"],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"風險假設改寫","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份 R1：聯準會 2026H2–2027 加速降息 100–150bp，壓淨利息收入","side_b":"Q3 法說會 Paul Brody 稱聯準會 9 月中升息、多國央行 9 月升息，敏感度基準 Fed funds 3.88%；降息風險由主情境降為尾部，改寫為利率路徑風險與唯一致命點","ruling":"利率方向已由降轉升，前份的降息主情境被新證據推翻；風險保留，但門檻改為累計降 ≥100bp 且淨利息收入連 2 季季減","evidence_level":"高","settle_metric":"Fed funds 與季度淨利息收入","if_then":["若 12 個月內累計降息 ≥100bp 且淨利息收入連 2 季季減，則減碼至半倉"],"evidence_refs":["end_markets#4"]},{"axis":"前份觸發器已發火","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份重啟條件中的「淨利息收入經降息證明韌性」分支，以及「回測 82 美元附近」分支","side_b":"Q3 淨利息收入年增 19%，同期 Fed funds 均值年減 63bp，量增已抵消；股價 82.69 美元，落在前份技術線附近。兩分支已發火","ruling":"依前份規則，觸發後要重跑判斷而非直接建倉；本次重跑後基準年化報酬約 5%，仍未達 8%，因此不據此進場","evidence_level":"高","settle_metric":"基準情境年化報酬","if_then":["若股價 ≤72 美元，則建首倉 2%"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"帳戶年增率跌破 25%，連續 2 季","type":"假設驗證","maps_to":"H1","metric":"客戶帳戶年增率","threshold":"連 2 季 <25%","action":"停止加碼；連 3 季 <20% 則減碼至半倉","source_freq":"公司月度指標／季報","date":null,"evidence_refs":[]},{"n":2,"text":"交易熱度轉為負成長：月度 DARTs 年增率連 3 個月為負","type":"風險","maps_to":"R1","metric":"月度 DARTs 年增率","threshold":"連 3 個月 <0","action":"未持有則不追；持有則減碼至半倉","source_freq":"公司月度指標","date":null,"evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"n":3,"text":"融資去槓桿或信用損失擴大","type":"風險","maps_to":"R2","metric":"期末融資餘額季變動／信用損失備抵","threshold":"融資餘額季減 ≥15% 或備抵單季增加 ≥1 億美元","action":"減碼至半倉","source_freq":"季報與 10-Q","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":4,"text":"危機型衝擊觸發聯準會急降息，Fed funds 12 個月內降至 2% 以下","type":"Single Thing","maps_to":"R3","metric":"Fed funds 有效利率","threshold":"12 個月內 ≤2%（9/30 為 3.88%）","action":"減碼至三分之一","source_freq":"FOMC 每次會議","date":null,"evidence_refs":["end_markets#4"]},{"n":5,"text":"股價回到基準報酬 8% 的位置，且帳戶成長仍成立","type":"估值rearm","maps_to":"H3","metric":"股價與帳戶年增率","threshold":"股價 ≤72 美元且帳戶年增 ≥25%","action":"建首倉 2%","source_freq":"每日股價／月度指標","date":null,"evidence_refs":[]},{"n":6,"text":"盈餘上修而股價未跟上","type":"加碼","maps_to":"H3","metric":"FY2027 共識 EPS","threshold":"≥3.5 美元且股價 ≤85 美元","action":"建首倉 2%，Q4 財報確認後加碼至 4%","source_freq":"Koyfin 月度快照","date":null,"evidence_refs":[]},{"n":7,"text":"監管或法律事件升級：單一罰款金額大，或主要市場被限制開戶","type":"風險","maps_to":"R4","metric":"監管罰款金額／主要市場開戶限制","threshold":"單一罰款 ≥1 億美元，或日本、中國客戶群被限制開戶","action":"停止加碼；涉及刑事程序則清倉","source_freq":"8-K／10-Q 法律程序段","date":null,"evidence_refs":["major_events#0","regulatory_antitrust#2","reg_tariff_export#1","major_events#1","lawsuit_class_action#0","geo_supply_chain#0"]},{"n":8,"text":"Q4 財報複審：帳戶、淨利息收入、DARTs 與選舉波動歸因驗證","type":"複審日期","maps_to":"H2","metric":"季報","threshold":null,"action":"依觸發器 1–7 執行","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"客戶帳戶年增率","bear_threshold":"連 2 季 <20%","window":"2 季","source":"公司月度指標與季報","last_status":"ok"},{"metric":"季度淨利息收入","bear_threshold":"年增轉負且連 2 季季減","window":"2 季","source":"季報 8-K","last_status":"ok"},{"metric":"Fed funds 有效利率","bear_threshold":"12 個月內降至 2% 以下","window":"12 個月","source":"FOMC 決議","last_status":"ok"},{"metric":"月度 DARTs 年增率","bear_threshold":"連 3 個月 <0","window":"3 個月","source":"公司月度指標","last_status":"warning"},{"metric":"客戶信用損失備抵","bear_threshold":"單季增加 ≥1 億美元","window":"1 季","source":"10-Q","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價 ≤72 美元（基準年化報酬回到 8%，約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS ≥3.5 美元而股價 ≤85 美元","exec_line":"未持有：不追，等重啟條件。觸及後分兩批，首批 2%，第二批等 Q4 財報確認帳戶年增 ≥25% 再加碼至 4%。已持有：不加碼，按 kill 指標執行減碼與清倉"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤72 美元（約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS 上修至 ≥3.5 美元而股價 ≤85 美元","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=1.39, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"帳戶複利：全球主動投資人與介紹經紀商持續轉入，帳戶與客戶資產維持高成長","2y":"帳戶年增 >25%、客戶權益年增 >20%","5y":null,"10y":null,"threshold":"帳戶年增 >25%／客戶權益年增 >20%","source":"公司月度指標與季報；Q3 帳戶 557.6 萬戶（+35%）、客戶權益 9,647 億美元（+27%）","drift_rule":"帳戶年增連 2 季 <25% 為削弱；連 3 季 <20% 為反轉"},{"id":"H2","text":"淨利息收入由餘額驅動，跨利率週期仍能成長","2y":null,"5y":"淨利息收入年增 ≥10%，降息時由融資與現金餘額增量抵消","10y":null,"threshold":"淨利息收入年增 ≥10%，且季變動不連 2 季為負","source":"Q3 淨利息收入 11.54 億美元（+19%），同期 Fed funds 均值年減 63bp；CFO 揭露美元每 25bp 約 8,300 萬、非美元約 3,500 萬美元","drift_rule":"年增連 4 季 <10% 為削弱；連 6 季年增為負為反轉"},{"id":"H3","text":"盈餘兌現：交易熱度退潮下，共識兩年 EPS 仍能達成","2y":"FY2027 EPS ≥3.2 美元、FY2028 ≥3.6 美元","5y":null,"10y":null,"threshold":"FY2027 EPS ≥3.2 美元／FY2028 ≥3.6 美元","source":"Koyfin 共識 2026-10-08：FY2026 2.70、FY2027 3.26、FY2028 3.71 美元；近 3 個月 FY2026 上修 4.25%","drift_rule":"FY2027 共識連 2 季下修累計 ≥5% 為削弱；連 3 季累計 ≥10% 為反轉"}],"R":[{"id":"R1","text":"交易熱度退潮與定價壓力：DARTs 年增率由 6 月 53% 降至 9 月 6%，每單佣金年減 4%，股票成交量年減 24%；若轉為負成長，佣金走平，EPS 增速降到 10% 以下","h_ref":"H3","clock":"⚡","threshold":"月度 DARTs 年增連 3 個月 <0，或季度 DARTs 再季減 ≥10%","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"id":"R2","text":"融資與信用週期：融資餘額 1,052 億美元仍高，全市場融資 7 月創紀錄單月降幅，公司信用損失備抵由 1,800 萬升到 2,600 萬美元；急跌時穿倉損失與餘額縮水同時出現","h_ref":"H2","clock":"🔥","threshold":"期末融資餘額季減 ≥15%，或信用損失備抵單季增加 ≥1 億美元","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"id":"R3","text":"利率路徑：淨利息收入約占營收 60%，美元每 25bp 約影響 8,300 萬、非美元約 3,500 萬美元；聯準會 9 月剛升息，降息已成尾部情境，但一旦急轉，敏感度最大","h_ref":"H2","clock":"🔥","threshold":"Fed funds 自 3.88% 累計降 ≥100bp，且淨利息收入連 2 季季減","evidence_refs":["end_markets#4"]},{"id":"R4","text":"跨境監管與法律：OFAC 制裁案 1,180 萬美元和解（2025 年 7 月）、平倉部位集體訴訟和解（聽證結果未查到）、國際營運的地緣與監管風險、日本帳戶遷移仍在與監管溝通","h_ref":"H1","clock":"🐢","threshold":"單一罰款 ≥1 億美元，或主要市場被限制開戶","evidence_refs":["major_events#0","regulatory_antitrust#2","reg_tariff_export#1","major_events#1","lawsuit_class_action#0","geo_supply_chain#0"]}],"single_thing":{"description":"危機型衝擊觸發聯準會急降息，Fed funds 於 12 個月內由 3.88% 降至 2% 以下","why_fatal":"淨利息收入約占淨營收 60%；公司揭露 Fed funds 每 25bp 對年化淨利息收入約 8,300 萬美元（9/30 基準），降至 2% 約少 6.2 億美元。急降息通常伴隨崩盤與融資去槓桿，餘額會同步縮水。這是 EPS 對單一變數最大的敏感度","if_happens":"EPS 回到 FY2025 的 2.2 美元附近，倍數壓縮，價格落入 Bear 區 45–55 美元；持有則減碼至三分之一","how_monitor":"FOMC 決議與 Fed funds 期貨；每季公司利率敏感度表；季度淨利息收入與融資餘額","probability":"約 10%（聯準會 9 月剛升息，12–24 個月內急轉到 2% 以下需要危機型衝擊）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.4,"peg_fy2":1.36,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.22,"FY2026E":2.7,"FY2027E":3.26,"FY2028E":3.71},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（A 類股）；共識為 Koyfin 2026-10-08 快照"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉，管理層預期波動上升帶動交易","impact":"中","watch":"11–12 月月度 DARTs 年增率是否回到 10% 以上"},{"date":"2026-12","date_precision":"month","type":"macro","event":"FOMC 利率決議（9 月升息後的路徑）","impact":"高","watch":"Fed funds 方向與淨利息收入敏感度"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"OCC 全國信託銀行執照（Q2 法說會稱計畫年底前完成上線）","impact":"中","watch":"是否如期取得正式核准"},{"date":"2026-11","date_precision":"month","type":"product","event":"Cboe 單一公司 KPI 二元期權上線，公司接入","impact":"低","watch":"預測市場交易量"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 財報","impact":"高","watch":"帳戶年增、淨利息收入、DARTs、期末融資餘額"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"Fidelity 對 1 億美元以下 RIA 的門檻生效","impact":"中","watch":"RIA 帳戶與資產轉入"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
