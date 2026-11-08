你是 DD 管線 v20 的判斷層閘（gate），標的 PH（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定；來源 gate_contract §⑤／critic-gates ⑤ 同日改成同一條規則（核心軸 none 🔴、非核心 🟡）；重新濃縮時以本卡 ⑤ 為準 -->

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

⑤ 覆蓋面掃描——**燈號由程式判定**（核心軸 none→🔴；只有非核心軸 none→🟡；全 found／not_applicable→🟢），bundle 附程式結果，你回的 ⑤ 燈號會被覆寫。你只評論：facts.json 點名 status="none"／"not_applicable" 的軸，查詢是否切題（不以查詢次數計）、判斷有沒有交代缺口對結論的影響；不得因缺軸自行升 🔴。

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤（燈號由程式判定，你只評論）。
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

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝5992 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi1_adjusted_segment_operati`（q1_business）｜Adjusted segment operating margin (non-GAAP)＝28.6 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi2_total_segment_operating_`（q1_business）｜Total segment operating margin (GAAP)＝24.4 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi6_backlog`（q1_business）｜Backlog＝13.7 USD B｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_peer_ph_gross_margin_pct`（q2_moat）｜PH 毛利率＝37.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ph_operating_margin_pct`（q2_moat）｜PH 營業利益率＝21.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ph_fcf_margin_pct`（q2_moat）｜PH FCF 利潤率＝17.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hon_operating_margin_pct`（q2_moat）｜HON 營業利益率＝16.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_rok_gross_margin_pct`（q2_moat）｜ROK 毛利率＝49.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_rok_operating_margin_pct`（q2_moat）｜ROK 營業利益率＝19.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_emr_gross_margin_pct`（q2_moat）｜EMR 毛利率＝53.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_emr_operating_margin_pct`（q2_moat）｜EMR 營業利益率＝20.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝35.59 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝39.77 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝44.14 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_kpi7_fy2027_guidance_filtrati`（q1_business）｜FY2027 guidance（上調，已含 Filtration Group）＝調整後 EPS 36.45–37.25；GAAP EPS 29.65–30.45 USD｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[7]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：FY1 共識 EPS 35.59（財報前快照，dd_numbers_extra.py consensus_revision）；指引中點 36.85
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝25304.16 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝27065.02 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_free_cash_flow_derived`（q1_business）｜Free cash flow (derived)＝643 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi5_sbc_share_based_compensa`（q4_capital）｜SBC (share-based compensation)＝82 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝16767.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 17478.0、現金 711.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.632 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝917.79 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝25.79 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 35.59，分子＝快照價 917.79｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.53 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝80.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝80.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.91 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝93.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝93.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝132497.37 USD m｜期間與口徑：2026-11-08／市值 115730.37 ＋ 淨負債 16767.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：全球、區域及在地競爭者可能造成降價壓力與毛利率或市占下滑；公司也提到因應措施（如漲價）可能衝擊市占。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-21）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Simply Wall St 社群敘事：電氣化與數位化可能降低 PH 液壓／氣動核心零件長期需求（社群意見，低權威）
  - 來源：Simply Wall St community narrative（as_of 2026-09-01）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Davidson Instruments 對 Parker 提起私人壟斷訴訟；Parker 於 2026-01 向聯邦法官主張修正後起訴狀未構成可信的壟斷或企圖壟斷主張，並聲請駁回；搜尋未見裁決結果。非政府調查。
  - 來源：MLex 報導（經搜尋摘要）（as_of 2026-01-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：非美國銷售地點占淨銷售約 36%；列出關稅、進出口管制、制裁及可能的對中國貿易限制為風險；美中關係與 USMCA 重新談判不確定可能衝擊業務。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-21）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：ITAR／EAR 管制清單範圍變動可能迫使 PH 調整營運、取得額外許可或限制業務；違規可能失去出口特權。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-21）｜affects：thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 Q3 10-Q：最高法院裁定 IEEPA 關稅未獲授權，公司因退款不確定未認列應收；中東衝突（含伊朗）可能影響全球供應鏈並推升大宗、能源、物流成本
  - 來源：Parker-Hannifin 10-Q (period ended 2026-03-31)（as_of 2026-05-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子承認所服務市場技術快速變動、新產品頻繁推出，並點名 AI 技術與資料中心基礎設施需求是需successfully整合/定位的領域；未點名特定替代技術取代核心產品。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-21）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：第三方分析稱行動設備電動化可能以機電系統取代液壓，時間尺度約 10–15 年；液壓約占 Industrial 部門 25–30%（第三方估計）。
  - 來源：PitchGrade research: parker hannifin ai margin pressure（as_of 2026-03-04）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St 社群敘事：看空者擔心電動化與軟體化自動化侵蝕傳統液壓。
  - 來源：Simply Wall St narrative: global electrification will challenge legacy markets（as_of 2026-08-01）｜affects：decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：收購資金安排：2025-12-10 簽 52.5 億（364 天）與 25 億（三年）延遲提款定期貸款，供 Filtration Group 收購部分對價
  - 來源：SEC EDGAR 8-K Item 1.01（as_of 2025-12-10）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1638.0,"bear_5y_price":711.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":34.1,"ev5y_pct":26.0,"irr_base_pct":6.0,"asym_ratio":2.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":36.85,"pe":24.91,"basis":"FY27 調整後 EPS 指引中點（FY1 口徑），終端倍數同樣用調整後 EPS；財報前共識 35.59 美元已過時。"},"eps":{"bull":[38.0,43.5,49.5,56.0,63.0],"base":[37.2,41.0,45.3,49.3,53.5],"bear":[36.45,38.0,35.0,36.5,39.5]},"pe":{"bull":26,"base":23,"bear":18},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.632,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PH_Q4_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 銷售成長指引區間 5.5%–8.5%，中點 7%（原話："Reported sales growth for the year is going to be in the"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 調整後 EPS 指引中點 $34.75（原話："full-year adjusted EPS is going to be $34.75 at the midpoint"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 調整後部門營業利益率指引中點 27.7%（原話："On adjusted segment operating margins, we're guiding 27.7%"）
- 2026-08-06｜CFO Todd Leombruno｜margin：FY27 增量利潤率預期接近 30%–35% 區間上緣（原話："we're forecasting that near the top end of our stated 30%"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：指引不含待完成的 Filtration Group 與 CIRCOR 收購（原話："does not yet include any impact from the pending Filtration"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 第一季 EPS 指引中點 $8.07（原話："adjusted EPS is expected to be just over -- a little over"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 自由現金流指引 34–39 億美元，轉換率約 100%（原話："range of $3.4 billion to $3.9 billion. That is free cash"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：航太 FY27 有機成長中點 8.5%（原話："Aerospace, we expect 8.5% organic growth at the midpoint."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：首度所有終端市場指引皆為正成長（原話："first time ever, we are guiding positive sales growth"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 EPS 橋接含非美元匯兌有利因素不再重現的 $0.14 不利（原話："due to the non-repeat of some favorable foreign currency"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：新利潤率目標：FY31 調整後部門營業利益率 30%（提高 300bp）（原話："We are raising it by 300 basis points to 30% by fiscal year"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：維持循環期有機成長 4–6%、FCF 利潤率 17% 等長期目標（原話："we remain committed to organic growth of 4% to 6% over the"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：新目標已納入尚未完成的收購（原話："Obviously, in these targets, we've included the"）
- 2026-08-06｜CFO Todd Leombruno｜margin：CFO 說明 FY31 利潤率提升在五年間大致平均分布（原話："spread pretty equally across those years, each of the five"）
- 2026-08-06｜CFO Todd Leombruno｜margin：CFO 個人判斷工業部門利潤率擴張幅度會大於航太（原話："would say the North American or the industrial businesses"）
- 2026-08-06｜CFO Todd Leombruno｜margin：第四季調整後部門營業利益率 28.0%，年增 110bp（原話："segment operating margin for the quarter was 28.0%. That is"）
- 2026-08-06｜CFO Todd Leombruno｜margin：定價面：管理層表示要回到正常定價環境（原話："we want to return to a normal pricing environment."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：北美工業成長指引全為量、無價格貢獻（原話："We're back to a normal pricing environment here, and this"）
- 2026-08-06｜CEO Jennifer Parmentier｜margin：航太仍有定價空間，部分談判仍在進行（原話："normal pricing environment. And in Aerospace, there's still"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：訂單口徑改變：FY27 起工業部門改用滾動 12 個月訂單率（原話："we are announcing a move to rolling 12-month order rates"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：管理層對改口徑的解釋之一：國際訂單過去波動大（原話："international orders have been very choppy in the past"）
- 2026-08-06｜CFO Todd Leombruno｜customer：第四季積壓訂單年增 16%，創紀錄 128 億美元（原話："Backlog increased 16% versus prior year and is now a new"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：敘事變化：經銷商復甦由「漸進」說法改稱「擴大中」（原話："a broadening recovery instead of what we've just been"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：管理層明言不認定通路已全面補庫存（原話："Still not calling a restock though."）
- 2026-08-06｜CEO Jennifer Parmentier｜risk：農業與汽車需求仍疲弱（原話："remain where it's been pretty soft and automotive pretty"）
- 2026-08-06｜CFO Todd Leombruno｜risk：下半年比較基期變高，工業有機成長百分比較集中於第一季（原話："the comps in the second half get a little bit tougher."）
- 2026-08-06｜CEO Jennifer Parmentier｜product：資料中心占營收約 1.5%，先前說法為 1%（原話："It's about 1.5% of our sales, and we've been previously"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：電子業國際訂單強於預期，並預期持續強勁（原話："I think it's going to remain strong. I mean, obviously, it"）
- 2026-08-06｜CEO Jennifer Parmentier｜product：FY27 航太指引假設 OE 占比提高至 52%（原話："So we're planning on higher OE mix here."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：油氣預期持平，發電成長更強（原話："Oil and gas, we think it's going to be flat."）
- 2026-08-06｜CFO Todd Leombruno｜capital_allocation：FY26 回饋股東：10 億美元回購加近 10 億美元股利（原話："That is $1 billion in share repurchases and nearly $1"）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：兩筆收購預計日曆年下半年完成，無重大障礙（原話："We still anticipate closing both of them during the second"）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：槓桿可能升至約 3 倍，約需 6 季回到 2 倍（原話："It will take us about 6 quarters to get that back down to 2."）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：CIRCOR 未模擬營收綜效（原話："We have not modeled any revenue synergies."）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：資本支出不預期超出現有指引（原話："but we're not expecting anything more than we've guided to"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：管理層確認將有 Win 4.0，並討論下次投資人日（原話："So there will be a Win 4.0. Definitely, there will be."）
- 2026-08-06｜CFO Todd Leombruno｜customer：管理層否認第四季訂單有拉貨（原話："No. We never really experienced that."）

### PH_Hannifin_Corporation_Shareholder_Analyst_Call_Parker_Hannifin_Corporation_20261028.md
- 2026-10-28｜CEO Jennifer Parmentier｜margin：FY26 營收首度超過 200 億美元，並提前三年超越 FY29 調整後部門營業利益率目標（原話："segment operating margin target 3 years ahead of schedule"）
- 2026-10-28｜CEO Jennifer Parmentier｜margin：FY26 營收首次突破 200 億美元（原話："we also exceeded $20 billion in sales for the first time"）
- 2026-10-28｜CEO Jennifer Parmentier｜product：收購 Curtis Instruments 強化電氣化能力（2025 年 9 月）（原話："acquisition of Curtis Instruments in September 2025"）
- 2026-10-28｜CEO Jennifer Parmentier｜capital_allocation：2026 年 5 月宣布收購 CIRCOR 商用與國防航空業務（待完成）（原話："pending acquisition of CIRCOR's Commercial and Defense"）
- 2026-10-28｜CEO Jennifer Parmentier｜capital_allocation：2026 年 8 月宣布收購 Filtration Group，擴大專有過濾技術（原話："in August 2026, Filtration Group Corporation"）
- 2026-10-28｜CEO Jennifer Parmentier｜guidance：管理層表示 FY27 第一季業績將於 11 月 5 日財報電話會議更新，本場未給數字（原話："our fiscal year '27 first quarter performance"）
- 2026-10-28｜CEO Jennifer Parmentier｜commitment：管理層對延續動能表達信心，未給量化目標（原話："confident in Parker's ability to build on this momentum"）
- 2026-10-28｜CEO Jennifer Parmentier｜risk：管理層稱將在各種條件下專注執行（原話："executing through whatever conditions lie ahead"）
- 2026-10-28｜CEO Jennifer Parmentier｜product：將 FY26 成果歸因於 Win Strategy、投資組合轉型、分權營運與連網技術（原話："disciplined execution of The Win Strategy"）
- 2026-10-28｜CEO Jennifer Parmentier｜customer：提及與客戶的深度關係為 FY26 成果來源之一（原話："connected technologies and deep customer relationships"）

### 問答異常語氣（迴避／改口／保留）
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Nicole DeBlase 問訂單在季內的進展及 7 月是否持續強勁｜答法：未給 7 月訂單數字或趨勢，只說沒有任何事情令其擔憂到不支持指引
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Jeff Sprague 問滾動 12 個月訂單出口 9–10% 與工業成長指引 4–7% 之間的落差｜答法：未解釋落差大小，改說訂單是領先指標但不是精確預測，並提 10% 航太國防占比
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Nathan Jones 問指引是否假設國際與北美訂單強勢持續或趨緩｜答法：未直接回答假設方向，只說指引反映目前訂單進展，並希望隨年度推進能上調

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Aerospace supercycle 至 2030s：Boeing 737 + Airbus A320 雙寡頭增產 + 老化機隊 retrofit + Meggitt aftermarket monopoly → PH Aerospace 業務 2025-2030 CAGR &gt; 10%","columns":{"2Y 驗證點":"Aerospace 有機 +12% (FY26 guide) 達成，backlog &gt; $9B","5Y 驗證點":"Aerospace 5Y CAGR ≥ 10%，aerospace 占比從 33% → 38%；OEM build rates A320 75/月 + 737 52/月 達成","10Y 驗證點":"Aero aftermarket revenue 占 aerospace 60%+；穩定 OEM 平台轉換週期（2030s 進入下一代 narrowbody R&D 階段）","驗證指標":"季度有機營收 + backlog QoQ","來源":"2Y: §6, 5Y: §8.A Runway, 10Y: §8.A + §9"}},{"id":"H2","text":"Win Strategy 3.0 持續 margin expansion：Adjusted Segment OI Margin 從 FY25 26.0% → FY28 28%+，提前達標 5Y 目標","columns":{"2Y 驗證點":"FY26 OI margin 27.2% guide 達成，Industrial NA &gt; 22%","5Y 驗證點":"FY28 整體 segment OI margin ≥ 28%，FCF margin ≥ 17%","10Y 驗證點":"OI margin 維持 28%+ 跨越 10Y 不退讓（even in industrial downturns）","驗證指標":"季度 segment OI margin + FCF/Revenue trend","來源":"2Y: §6, 5Y: §8 + §10, 10Y: §8.A' S 曲線"}},{"id":"H3","text":"Filtration Group 整合成功：$9.25B 收購 $220M cost synergy 兌現 + EBITDA margin 維持 23.5%+ + 12 個月內 EPS accretive","columns":{"2Y 驗證點":"2026 H2-2027 Q1 close；首 12 個月 synergy ≥ 50%","5Y 驗證點":"5Y 後 filtration 占比 8-12%；synergy 完全兌現 → group OI margin +50bps","10Y 驗證點":"Filtration 結構性轉變 PH 為 aftermarket-recurring 模式 (50%+)","驗證指標":"季度 segment reporting + Filtration 揭露","來源":"2Y: §6 + §12, 5Y: §8.B 成長品質, 10Y: §9"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"商用航太 OEM 增產延後 / Boeing 安全事件再起（如 737 MAX、787 quality issues）→ A320 / 737 production rate 跑不到 guidance","columns":{"對應假設":"H1","時間尺度":"中期（2-3 年）","監測指標":"Boeing 737 月產量、Airbus A320 月產量；Boeing safety incidents","警戒閾值":"737 月產量 &lt; 35/月 連 2 季；A320 月產量無法在 2027 達 70/月（當前路徑 55-60/月）"}},{"id":"R2","text":"美中關稅 / supply chain re-shoring 推高 Industrial 業務成本 → Industrial OI margin 收窄 -2pp","columns":{"對應假設":"H2","時間尺度":"短期（12 月內）","監測指標":"Tariff policy；PH 在中國 / 墨西哥工廠占比；Industrial gross margin","警戒閾值":"整體 GM 連 2 季 YoY -1pp；Industrial NA segment OI margin 跌破 22%"}},{"id":"R3","text":"Filtration Group 收購 regulatory block 或 integration synergy 兌現 &lt; 50%","columns":{"對應假設":"H3","時間尺度":"中期（2-3 年）","監測指標":"FTC / 歐盟反壟斷進度；close timeline；首 12 個月 synergy disclosure","警戒閾值":"close 延後超過 2027 Q1；首年 synergy &lt; $100M（vs $220M target）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":33,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":33,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":862.72,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"PH","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Parker-Hannifin Corporation"},"oneliner":"好公司，但價格已先走一步。工業復甦疊上航太，FY27 EPS 指引三個月上調 6%；現價約 FY27 指引 24.9 倍，Base 五年年化只有 6–7%，到 800 美元以下才值得動手。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是設備製造商與機隊營運商的維修替換錢，利潤卡在應用工程師把多項互連技術設計進設備、經銷網再把售後接走這一節。","reasoning":"Q1 FY27 營收 59.92 億美元：北美工業 24.45 億，有機 +9.4%，利潤率 27.6%；國際工業 17.07 億，有機 +11.6%，利潤率 27.7%；航太有機 +14%，利潤率 30.7%。調整後部門利潤率 28.6%，GAAP 部門利潤率 24.4%；TTM 毛利率 37.74%，營業利益率 21.4%。在手訂單 137 億美元，約 75% 在 12 個月內轉成營收。單點依賴不在客戶：FY24 年報單一客戶不超過 4%，FY26 年報稱無信用集中風險。真正的集中是循環，短循環工業決定年度波動。資料中心約占 1.5%，還不足以左右結果。分部資料取自 2026-11-05 法說與新聞稿。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_segment_operati","f_kpi2_total_segment_operating_","f_kpi6_backlog","f_peer_ph_gross_margin_pct","f_peer_ph_operating_margin_pct"],"verdict_values":{"revenue_quality":"售後與長循環比重提高：FY27 航太售後指引占 47%，濾材集團再把濾材售後比重提高 5 個百分點；短循環工業仍是最大波動來源。","unit_econ_note":"2/3 營收來自買 4 項以上技術的客戶，85% 產品有智財保護。單價與量的結構化數字事實表未涵蓋；財務長明說本季有機成長上修來自需求，不是價格。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"營業利益率在營收只增 4.1% 的 FY23–FY25 擴大 4.28 個百分點，FCF 對淨利四年都在 94% 以上，但短循環工業仍決定年度波動。"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張初段：本季是三年多來第一次有機雙位數，滾動 12 個月訂單 +13%，各終端市場全年都指引正成長。供需判斷：工業短循環屬週期性將反轉，時點未知；航太售後屬結構性持久，機隊老化、退役少；美國機械業產能利用率自 2024 年底上升，新產能正在進場。","bargaining":{"up":"原物料與物流仍在漲，公司以定價與供應鏈工具因應，目標是利潤中性。","down":"客戶分散，FY24 單一客戶不超過 4%，中小 OEM 靠經銷商服務；航太仍有部分定價談判在進行。","geo":"非美國銷售地點約占 36%，以在地生產因應關稅與貿易限制。"},"profit_pool_dir":"產業利潤池資料事實表未涵蓋；本季 PH 三個部門的利潤率同創新高。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池資料；公司只揭露併購後濾材年營收約 50 億美元，不足以展開。"}}}},"q2_moat":{"verdict":"護城河穩定（→）：執行面還在變強，但定價權只是穩定，也拿不出相對同業的方向證據，所以不判擴大。","reasoning":"機制：應用工程師加全球經銷網，把互連技術設計進客戶設備，之後的替換需求跟著裝機基數走。當期：TTM 營業利益率 21.4% 是對照同業最高，毛利率 37.74% 在五家只排第四，優勢在費用效率與組合，不在單價；投入資本事實表未涵蓋，ROIC 算不出來，象限依併購商譽推斷。持續期：四項檢查中，決策層級因缺流失率資料只給黃燈。增量：濾材集團事前推算報酬 5.3–6.5%，低於本判斷假設的 8% 資金成本，EPS 增厚靠的是 4.5% 左右的舉債。","fact_refs":["f_peer_ph_gross_margin_pct","f_peer_ph_operating_margin_pct","f_peer_ph_fcf_margin_pct","f_peer_hon_operating_margin_pct","f_peer_rok_gross_margin_pct","f_peer_rok_operating_margin_pct","f_peer_emr_gross_margin_pct","f_peer_emr_operating_margin_pct","f_peer_etn_operating_margin_pct","f_kpi1_adjusted_segment_operati"],"verdict_values":{"moat":{"mechanism":"應用工程師與全球經銷網把多項互連技術設計進客戶設備，替換需求跟著裝機基數走；2/3 營收來自買 4 項以上技術的客戶，85% 產品有智財保護。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：營業利益率由 FY23 的 16.13% 升到 FY26 的 21.55%，大部分發生在營收幾乎不動的期間。定價面穩定：2026-08-06 與 2026-11-05 兩次法說都說工業定價回到正常，財務長說價格對增量利潤率沒有影響。份額、留存與同業時序資料事實表未涵蓋，相對優勢是否擴大無法證明。","competitor_notes":[{"name":"HON","strategy_note":"毛利率接近 PH，營業利益率與 FCF 利潤率都較低；組合差異大，不是液壓氣動的直接對手。"},{"name":"ROK","strategy_note":"毛利率明顯較高，營業利益率略低；事實表無分部資料，重疊程度無法判斷。"},{"name":"EMR","strategy_note":"毛利率與 FCF 利潤率高於 PH，營業利益率接近，是獲利結構最值得對照的一家。"},{"name":"ETN","strategy_note":"毛利率、營業利益率與 FCF 利潤率都低於 PH；事實表無分部資料，重疊程度無法判斷。"},{"name":"Bosch Rexroth、Danfoss、Festo、SMC、Gates","strategy_note":"10-K 點名的主要對手，事實表沒有財務資料可比。"}],"spread_notes":null,"peer_na_reason":"事實表同業對照只有 TTM 利潤率單一時點，沒有投入資本與歷史序列，算不出 ROIC 差距與方向。","threats":[{"level":"🟡","text":"電動化以機電系統取代行動設備液壓，時間尺度約 10–15 年，第三方估液壓占工業部門 25–30%。來源是第三方與社群敘事，權威偏低；公司 2025-09 收購 Curtis 補電氣化能力。","p":"30%","evidence_refs":["substitute_technology#1","substitute_technology#2","competitive_share_entrants#3"]},{"level":"🟡","text":"全球與在地對手的降價壓力，以及 10-K 自承的技術快速變動。目前只有風險揭露，沒有份額流失的量化證據。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設備操作與維修端，決策者是 OEM 工程師與經銷商，付款者是 OEM 與機隊營運商，三者都成立。航太售後占比 47%，機隊老化、退役少，維修需求難以長期延後。"},{"item":"決策層級","level":"🟡","text":"多數營收來自買 4 項以上技術的客戶，決策單位偏系統而非單一零件；但 10-K 自承對手數以百計，漲價後流失率與重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟢","text":"客戶分散，FY24 單一客戶不超過 4%，中小 OEM 透過經銷商採購，買方議價力低；成本上漲可轉嫁，公司目標是利潤中性。"},{"item":"社會容忍度","level":"🟢","text":"未見價格管制或依賴政府授權的證據。併購後濾材規模約 50 億美元，有一般性反壟斷風險，搜尋未見 2026 年政府調查。"}],"roiic":"併購段 5.3–6.5%（上界）：濾材集團年化營收約 21.1 億美元（18.5 億÷10.5×12），乘 30% EBITDA 目標得 6.3 億，扣稅 22.5% 得 4.9 億，除以 92.5 億得 5.3%；營收以 5% 成長四年到 25.7 億，同利潤率得 6.5%。未扣折舊，所以是上界。有機段投入資本事實表未涵蓋。","reinvest_rate":"FY27 單年併購約為 FY26 稅後營業利益的 2.6 倍（92.5 億÷35.9 億）；常態以股利後留存 FCF 約 73% 計（年股利約 10.1 億÷FCF 指引 37.5 億＝27%）。","endo_ceiling":10.7,"formula_note":"內生上界 10.7%＝公司有機目標上緣 6%（資本需求低，FCF 接近或高於淨利）＋併購段報酬 6.5%×留存率 73%。不含利潤率擴張，有機段是目標值，非由投入資本算出。"}}}},"q3_growth":{"verdict":"成長跑道中等（🟡）：有機目標加併購足以撐五年，第五年以後仍要靠持續併購，第二條成長曲線還不夠格。","reasoning":"FY27 報表成長指引中點 17.5%，其中有機 9%、併購約 9%、匯率 −0.5%。財報前共識 FY27E 到 FY29E 年複合 11.4%；FY2026 只有 GAAP 基期，與調整後共識口徑不同，不拿來算 CAGR。內生上界 10.7%，缺口 0.7 個百分點，歸因利潤率擴張（FY27 指引 27.9%，公司 FY31 目標 30%）。Base 由 FY27 到 FY31 年複合 9.5%，在上界以內。TAM 與滲透率事實表未涵蓋，跑道年數無法換算。資料中心約占 1.5%，雙位數成長，但管理層說還不到獨立的垂直市場；生命科學只是濾材集團內成長較快的一塊。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_fy2027_guidance_filtrati","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_backlog"],"verdict_values":{"growth":{"driver_mix":"FY27 報表成長約一半有機、一半併購；有機成長上修來自量，不是價格；EPS 成長再加上利潤率擴張，回購貢獻很小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的 10.7%：有機目標上緣 6% 加併購報酬 6.5% 乘留存率 73%；共識 11.4% 高出 0.7 個百分點，缺口歸因利潤率擴張。","segments":[{"item":"北美工業","value":"Q1 營收 24.45 億美元，有機 +9.4%，利潤率 27.6%；FY27 有機指引中點 8%。"},{"item":"國際工業","value":"Q1 營收 17.07 億美元，有機 +11.6%，亞太 +23.4%，EMEA +4%，拉美 −1%；FY27 有機指引中點 9.5%。"},{"item":"航太","value":"Q1 有機 +14%，利潤率 30.7%，訂單 +14%；FY27 有機指引中點 10%，OE 與售後比重 53／47。"},{"item":"濾材集團","value":"FY27 計入營收 18.5 億美元，約 10.5 個月；歷史中個位數成長；累計成本綜效目標 2.2 億美元，FY27 為 4,000 萬。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率連三年上升，TTM 37.74%。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"事實表未涵蓋份額資料，未見流失報導。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"本季成長由量帶動。"},{"signal":"EPS 年複合顯著高於營收","lit":true,"note":"FY23–FY26 GAAP EPS 年複合 21.1%，營收 4.1%，差 17 個百分點。"},{"signal":"FCF 對淨利低於 0.75 連 2 年","lit":false,"note":"FY25 為 0.95，FY26 為 1.07。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"Q1 為 1.4%。"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"電動化屬 10–15 年尺度，列入觀察。"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋同業倍數歷史。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"Q1 總資本支出約 1.09 億美元，占 FCF 17%。"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"FY26 營收年增 8.31%，管理層稱靠精實生產增加產能。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金流品質好、稀釋很低，但回購報酬不夠，併購報酬還算不出來，資本配置整體中等。","reasoning":"FY26 FCF 39.05 億美元，對淨利 107%，FY23–FY26 都在 94% 以上。Q1 SBC 占營收 1.4%。資金去向：Q1 資本支出約 1.09 億；股利每季 2 美元，連續 306 季；FY26 回購 10 億；最大用途是併購，濾材集團付現 92.5 億。Q1 季底淨負債對調整後 EBITDA 2.7 倍，新債平均利率略高於 4.5%；2026-08-06 管理層說峰值約 3 倍、約 6 季回到 2 倍。近三年完整現金去向、債務到期結構與回購均價事實表未涵蓋。","fact_refs":["f_kpi4_free_cash_flow_derived","f_kpi5_sbc_share_based_compensa","f_net_debt_m","f_dividend_yield_ttm","f_kpi0_net_sales_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"歷次併購的投入資本與已實現報酬事實表未涵蓋，無法判定。濾材集團未滿一年，事前推算 5.3–6.5%，低於假設的 8% 資金成本，要看 FY29 實績。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以現價算，盈餘收益率 GAAP 約 3.3%、調整後約 4.0%。10 年期殖利率事實表未涵蓋，但這個報酬連新債約 4.5% 的平均利率都不到，更達不到殖利率加 2%。回購均價未揭露，以現價代用。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q1 SBC 8,200 萬美元，年化占市值約 0.28%，遠低於 1.5%；本季股數減少貢獻 EPS 0.04 美元。"}]},"governance":{"capital_returns":[{"item":"股利","value":"每季 2 美元，連續 306 季；TTM 殖利率 0.63%。"},{"item":"回購","value":"FY26 10 億美元；均價事實表未涵蓋。"},{"item":"併購","value":"濾材集團現金 92.5 億美元，2026-08-13 完成；CIRCOR 航空業務待完成，金額事實表未涵蓋。"},{"item":"債務","value":"淨負債 167.67 億美元，淨負債對調整後 EBITDA 2.7 倍，目標約 6 季回到 2 倍。"}]}}},"q5_valuation":{"verdict":"917.79 美元要賺到五年年化 10%，FY31 EPS 得到 62.5 美元，或終端倍數維持約 27 倍；這兩項我都不信，所以估值偏貴。","reasoning":"五年年化 10% 扣掉 0.63% 殖利率，股價要到約 1,438 美元。Base 的 FY31 EPS 53.5 美元要配 26.9 倍，或者按 23 倍需要 EPS 62.5 美元，已接近 Bull。短期上檔以 FY28 Base EPS 41.0 美元乘 24 倍得 984 美元，+7.2%；中期以 FY29 的 45.3 美元乘 24 倍得 1,087 美元，+18.5%。PEG 用 FY27E 到 FY29E 共識年複合 11.4%，25.79 倍除以 11.4 得 2.27，屬偏貴。共識快照在財報前，FY1 與 FY2 都還沒反映這次上修。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm","f_kpi7_fy2027_guidance_filtrati","f_ev_m"],"verdict_values":{"valuation":{"basis":"調整後 EPS 前瞻本益比，起點用 FY27 指引中點 36.85 美元，並以 GAAP EPS 與 FCF 殖利率校正。","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，倍數無法比；判斷改靠自身年度端點與情境樹。"},"fwd_pe":25.79,"peg":2.27,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴：FY27 指引中點 24.9 倍（財報前共識 25.8 倍），GAAP 指引中點約 30.5 倍；PEG 2.27；FCF 指引對市值殖利率約 3.2%；本益比與 EV 對營收在年度端點分位 80 與 93.6；Base 五年年化約 6–7%。五年高低點事實表未涵蓋，不計五年分位。","upside_short_pct":7.2,"upside_mid_pct":18.5,"denominator_disputed":false,"denominator_note":"分母不是翻案點：調整後 24.9 倍與 GAAP 30.5 倍都不便宜。要留意共識 35.59 美元是財報前快照；GAAP 與調整後中點差 6.80 美元，對帳細項事實表未涵蓋；FY26 GAAP 含 8,400 萬美元關稅退款，約每股 0.5 美元。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是利潤率有多少是結構性的，其次是濾材集團的資本報酬，再來是 25 倍左右的本益比能否維持。","reasoning":"三項的證據與裁定寫在反證紀錄。十類衰退訊號只有一項亮燈：FY23–FY26 EPS 年複合比營收高 17 個百分點，代表過去的 EPS 主要靠利潤率。訴訟面只有一件私人壟斷案，10-K 稱訴訟不會有重大不利影響。歷史最大回撤與空方最強數字事實表未涵蓋，最大回撤改由情境樹推算。","fact_refs":["f_kpi1_adjusted_segment_operati","f_ev_s_percentile","f_pe_percentile","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"EPS 成長主要靠利潤率擴張，營收成長偏低"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":36.85,"pe":24.91,"basis":"FY27 調整後 EPS 指引中點（FY1 口徑），終端倍數同樣用調整後 EPS；財報前共識 35.59 美元已過時。"},"eps":{"bull":[38.0,43.5,49.5,56.0,63.0],"base":[37.2,41.0,45.3,49.3,53.5],"bear":[36.45,38.0,35.0,36.5,39.5]},"pe":{"bull":26,"base":23,"bear":18},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.63,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":8},"max_dd":{"lo":-43,"hi":-28,"basis":"歷史最大回撤事實表未涵蓋，改由情境樹推算：Bear 低點 EPS 35.0 美元乘 15 倍得 525 美元，跌 42.8%；較淺情境 36.5 美元乘 18 倍得 657 美元，跌 28.4%。","trigger_time":null},"basis":{"bull":"有機成長維持 7–8%，部門利潤率 FY31 到 31%，槓桿回落後重啟併購；終端 26 倍，略高於現在的 24.9 倍，反映售後比重提高。同業前瞻倍數事實表未涵蓋，只能對照自身。","base":"FY27 略高於指引中點；之後有機 5–6.5%，部門利潤率 FY31 到 29.7%，略低於公司 30% 目標，利息隨還債下降，股數微降，淨回購不重複計入；終端 23 倍，較現在收斂約 2 倍。同業現值倍數事實表未涵蓋。","bear":"FY29 前後工業衰退，部門利潤率退到約 25.5%，FY31 EPS 僅 39.5 美元；終端 18 倍，對應成長率降到 5% 左右。機率 30%：共識成長率 11.4% 略高於內生上界 10.7%，利潤率已在高位，五年內遇到一次工業衰退的機率高。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"部門利潤率 28.6% 創新高，同時是三年多來第一次有機雙位數；EV 對營收在年度端點的 93.6 分位。","assumption":"假設利潤率的提升能跨過下一次工業衰退。","consequence":"五年虧 50% 最可能的路徑：FY29 前後工業衰退，EPS 跌到約 35 美元，本益比由約 25 倍掉到 13–15 倍，股價落在 455–525 美元，較現價跌 43–50%。","ruling":"部分採納。營業利益率 FY23–FY25 在營收只增 4.1% 時擴大 4.28 個百分點，這段不是量帶出來的；FY26 的 1.14 個百分點中，0.39 來自關稅退款，其餘 0.75 是量與執行混合。保留 Bear 機率 30%，並以 FY28 利潤率低於 27.0% 作為唯一致命點。","watch":"調整後部門利潤率、滾動 12 個月訂單、北美工業利潤率。","evidence_refs":[],"fact_refs":["f_kpi1_adjusted_segment_operati","f_ev_s_percentile"]},{"view":"論點成功但股東經濟變差","evidence":"濾材集團達到 30% EBITDA 目標後，稅後報酬約 5.3–6.5%，低於本判斷假設的 8% 資金成本。FY27 FCF 指引中點 37.5 億美元低於 FY26 的 39.05 億。GAAP EPS 指引中點比調整後低 6.80 美元。收購資金含 52.5 億 364 天與 25 億三年期延遲提款貸款。","assumption":"假設調整後 EPS 成長等於股東實得。","consequence":"整合全部成功、調整後 EPS 照路徑走，但投入資本賺不到資金成本，每股 FCF 跟不上，市場可能改看目前約 3.2% 的 FCF 殖利率。","ruling":"採納。長期信心只給中。管理層說併購管線仍活躍，2027-05 投資人會議還有消息；下一筆大案前，要先看到槓桿回到 2 倍附近。","watch":"每股 FCF、GAAP 與調整後 EPS 差距、槓桿回落速度。","evidence_refs":["major_events#1"],"fact_refs":["f_kpi7_fy2027_guidance_filtrati","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價約 FY27 指引中點 24.9 倍，GAAP 口徑約 30.5 倍，PEG 約 2.27；Base 五年年化約 6–7%。","assumption":"假設市場會繼續給 25 倍左右的本益比。","consequence":"基本面照 Base 走，報酬也只是盈餘成長扣掉倍數收斂，沒有安全邊際。","ruling":"採納。現價不追，等 800 美元以下。","watch":"股價相對 FY27 與 FY28 指引的倍數。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 862.72 → 本次 917.79（+6.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=862.72","side_b":"本次 price_at_dd=917.79","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 862.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 862.72 美元：五年期望值 +33.0%，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 862.72 美元：Bull 價 1,638、Bear 價 711，五年期望值 +34.0%，基準年化 7.4%，不對稱比 3.41","ruling":"先換情境、股價不動：五年期望值多 1.0 個百分點。前份未列不對稱比，本次為 3.41。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 862.72 美元：五年期望值 +34.0%，基準年化 7.4%，不對稱比 3.41","side_b":"本次情境、股價 917.79 美元：五年期望值 +26.0%，基準年化 6.0%，不對稱比 2.32","ruling":"再換股價、情境不動：起點價上漲 6.4%，五年期望值少 8.0 個百分點，基準年化少 1.3 個百分點，不對稱比由 3.41 降到 2.32。合計五年期望值比前份少 7.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利潤率是結構還是週期","cause":null,"prior_field":null,"side_a":"結構：FY23–FY25 營業利益率由 16.13% 升到 20.41%，營收只增 4.1%；國際工業靠過去兩年重組，本季擴大 270 個基點。","side_b":"週期：本季有機 11.5% 帶來 120 個基點擴張，財務長自己說 Q1 特別好；FY26 的 21.55% 含 8,400 萬美元關稅退款；濾材集團起跳利潤率低於舊業務。","ruling":"可調和，屬程度差異。約 4.3 個百分點可視為結構性，0.75 個百分點是量與執行混合，0.39 個百分點是一次性。結構部分含歷次併購的組合變化，無法再拆，這個殘差已放進 Bear 機率 30%。","evidence_level":"中：年報與法說，無法拆開價格、組合與併購。","settle_metric":"FY28 調整後部門利潤率。","if_then":["若 FY28 低於 27.0%，減碼一半。","若 FY28 高於 28.5% 且有機成長回落到 5% 以下，代表結構性成立，股價不高於 945 美元時分批反買。"],"evidence_refs":[]},{"axis":"調整後 EPS 與現金","cause":null,"prior_field":null,"side_a":"FY27 調整後 EPS 指引上調到 36.85 美元，三個月內上調 2.10 美元。","side_b":"同一份指引的 FCF 中點 37.5 億美元，低於 FY26 的 39.05 億；FCF 利潤率約 14.8%，低於公司 17% 的長期目標與 FY26 的 18.16%；Q1 FCF 只占營收 10.7%。","ruling":"可調和。差距來自新增約 3.5 億美元利息、併購帶來的現金影響與下半年現金集中。GAAP EPS 中點 30.05 美元較貼近現金，所以本判斷用 3.2% 的 FCF 殖利率校正 24.9 倍的印象。FY28 是第一個較乾淨的年度。","evidence_level":"高：公司指引與年度財報。","settle_metric":"FY27 FCF 是否不低於 35 億美元；FY28 FCF 利潤率是否回到 17% 附近。","if_then":["若 FY27 FCF 低於 35 億美元，停止加碼。","若 FY28 FCF 利潤率達 17% 以上，這項疑慮解除，股價不高於 945 美元時分批反買。"],"evidence_refs":[]},{"axis":"指引與訂單的落差，以及訂單口徑更換","cause":null,"prior_field":null,"side_a":"2026-08-06 法說，Jeff Sprague 問滾動訂單 9–10% 與工業指引 4–7% 的落差，管理層沒有解釋大小，只說訂單不是精確預測。","side_b":"2026-11-05 有機指引中點由 7% 上調到 9%，Q1 實績 11.5% 高於原本 8% 的指引，證明當時指引偏保守。但 2026-08-06 執行長 Parmentier 宣布工業部門改用滾動 12 個月訂單，理由之一是國際訂單波動大，這個口徑會把轉折平滑掉。","ruling":"可調和。短期偏多的判斷被驗證，但滾動口徑讓下行訊號晚到，不能只看訂單，要搭配亞太有機成長與經銷商訂單。","evidence_level":"中：法說原話，單季訂單已不揭露。","settle_metric":"滾動 12 個月訂單與單季有機成長是否背離。","if_then":["若滾動訂單仍升而單季有機成長連 2 季下滑，停止加碼。","若兩者同升且股價到 800 美元以下，分批反買。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"賣方平均目標價 1,039.70 美元，高於現價 13.3%，區間 680–1,269，且資料在 7 月底，還沒反映 Q1。指引三個月上調 6%，有機成長加速，舊業務增量利潤率指引在高 30% 到低 40%，財報前共識 35.59 美元明顯過時。","side_b":"平均目標價等於 FY27 指引 28.2 倍，需要市場再給更高倍數；Base 五年年化約 6–7%，Bull 約 13%。","ruling":"賣方全距最高除以最低 1.87 倍，分歧不大，目標價方向反對本裁決，但差距來自倍數，不是盈餘：本判斷 FY28 EPS 41.0 美元已高於過時共識 39.77。市場給 25 倍不算錯，只是買在這裡賺的是盈餘成長減倍數收斂。","evidence_level":"中：目標價為二手彙整。","settle_metric":"2027-08 的 FY28 初始指引與當時股價。","if_then":["若股價續漲而 FY28 指引中點未到 43 美元，不追。","若股價跌到 800 美元以下而基本面門檻都沒踩線，分批反買。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 列出數以百計對手，沒有第三方份額資料，也未見新進入者或對手勝出報導。結構：航太在手訂單由 73.89 億美元增到 84.98 億，濾材售後比重上升。","side_b":"其他：電動化取代液壓屬 10–15 年尺度，來源權威低；併購後濾材年營收約 50 億美元，有反壟斷曝險，但未見政府調查。","ruling":"裁決＝靜態。競爭面沒有惡化證據，改善主要來自公司組合變化，不是產業本身，依據是 FY26 年報競爭段與 2026-11-05 法說。","evidence_level":"低：缺第三方份額資料。","settle_metric":"第三方份額資料，事實表未涵蓋。","if_then":["若出現對手在主要平台勝出的具名報導，停止加碼。","若 Curtis 電氣化產品在主要行動設備 OEM 勝出且液壓營收未降，電動化威脅機率由 30% 下調到 15%。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"axis":"前份留空的欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份裁決、角色、跑道、公司類型、循環位置、最大回撤與情境機率皆未填。","side_b":"本次跑道中等，公司類型為品質複利成長，循環位置早循環，最大回撤 −28% 到 −43%，情境機率 20、50、30。","ruling":"屬填欄差異，不代表看法改變。","evidence_level":"低：前份沒有數字可比。","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"2026-05-18 評級 B，估值偏貴，股價 862.72 美元。","side_b":"本次評級 B，估值偏貴，股價 917.79 美元，上漲 6.4%。","ruling":"股價上漲與 FY27 指引上調 6% 大致相抵，結論不變。","evidence_level":"高：價格與公司指引。","settle_metric":"股價相對 FY27 指引的倍數。","if_then":["若股價回到 800 美元以下，分批反買。"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份方向向上。","side_b":"本次穩定：執行面擴大，定價面穩定。","ruling":"2026-08-06 與 2026-11-05 兩次法說都說工業定價回到正常，財務長說價格對增量利潤率沒有影響；也沒有份額或同業時序資料能證明相對優勢擴大，所以改判穩定。","evidence_level":"中：管理層原話，缺第三方資料。","settle_metric":"同業利潤率時序或第三方份額資料。","if_then":["若同業時序顯示 PH 利潤率領先幅度連 4 季擴大，方向改回向上。"],"evidence_refs":[]},{"axis":"價值陷阱評估","cause":"方法變動","prior_field":["trap"],"side_a":"前份無陷阱疑慮。","side_b":"本次一項衰退訊號亮燈：FY23–FY26 GAAP EPS 年複合 21.1%，營收 4.1%。","ruling":"本輪逐項計算十類訊號才抓出來，不是基本面轉差，但提醒過去的 EPS 主要靠利潤率，這條路不能無限延伸。","evidence_level":"高：年度財報。","settle_metric":"EPS 與營收年複合差距。","if_then":["若 FY28 有機成長低於 5% 而利潤率也不再擴張，停止加碼。"],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件。","side_b":"股價收盤回到 800 美元以下（約 FY27 指引中點 21.7 倍，接近 104 週均線）","ruling":"本次把不追的原因限定為價格，到價後先重跑研究，基本面門檻沒踩線才分批加碼。","evidence_level":"中：情境樹推算。","settle_metric":"收盤價。","if_then":["若到價時利潤率或訂單門檻已踩線，不追。"],"evidence_refs":[]},{"axis":"量化出場指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化出場指標。","side_b":"FY28 調整後部門利潤率低於 27.0%；滾動 12 個月訂單連 2 季下滑且低於 +6%；2028-06 季槓桿高於 2.5 倍；FY27 FCF 低於 35 億美元；FY28 結束累計綜效低於 1 億美元；北美工業利潤率低於 25.5%；整體毛利率連 2 季年減 1 個百分點；737 月產量低於 35 架連 2 季或 A320 在 2027 年到不了 70 架。","ruling":"新增量化標準。第一條踩到就減碼一半，第一條與第三條同時踩到就清倉，其餘踩到停止加碼或減碼三分之一。","evidence_level":"中：門檻為本判斷設定。","settle_metric":"各指標最新季度值。","if_then":["若第一條踩線，減碼一半。"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing。","side_b":"FY28（2028-06 結束）全年調整後部門營業利益率低於 27.0%。","ruling":"本次新設 Single Thing，選五年路徑裡敏感度最大的一項；濾材整合與訂單反轉最後都會反映到這個數字。","evidence_level":"中：敏感度由 Base 路徑推算。","settle_metric":"FY28 全年調整後部門營業利益率。","if_then":["若踩線，減碼一半。"],"evidence_refs":[]},{"axis":"舊風險門檻：北美工業利潤率","cause":"新證據","prior_field":["R2"],"side_a":"整體 GM 連 2 季 YoY -1pp；Industrial NA segment OI margin 跌破 22%","side_b":"整體毛利率連 2 季年減 1 個百分點（保留）；北美工業利潤率低於 25.5%","ruling":"本季北美工業利潤率已到 27.6%，22% 的舊線離現況 5.6 個百分點，等於不設防。新線上移到 25.5%，踩到就減碼三分之一。","evidence_level":"高：新聞稿數字。","settle_metric":"北美工業調整後利潤率。","if_then":["若低於 25.5%，減碼三分之一。"],"evidence_refs":[]},{"axis":"舊風險門檻：濾材集團交割與綜效","cause":"新證據","prior_field":["R3"],"side_a":"close 延後超過 2027 Q1；首年 synergy < $100M（vs $220M target）","side_b":"FY27 綜效低於 4,000 萬美元；FY28 結束累計低於 1 億美元","ruling":"交割已在 2026-08-13 完成，第一項退休。管理層首次揭露 FY27 只排 4,000 萬美元，換算 12 個月約 4,600 萬，按舊門檻字面已低於 1 億美元，也低於前份首 12 個月達 50% 的驗證點。這是前份假設的時程太前，不是整合出事，但綜效與 EPS 增厚都比前份想的晚。新門檻對齊公司時程，未達就減碼三分之一。","evidence_level":"中：管理層揭露，整合實績還沒出來。","settle_metric":"法說揭露的累計綜效。","if_then":["若 FY28 結束累計低於 1 億美元，減碼三分之一。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY27 有機成長守住指引下緣。","type":"假設驗證","maps_to":"H1","metric":"FY27 有機成長率","threshold":"低於 7.5%","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-08"},{"n":2,"text":"FY28 全年調整後部門營業利益率低於 27.0%。","type":"Single Thing","maps_to":"Single Thing","metric":"調整後部門營業利益率","threshold":"FY28 低於 27.0%","action":"減碼一半","source_freq":"季度新聞稿","date":"2028-08"},{"n":3,"text":"FY28 利潤率踩線，同時還債落後。","type":"清倉","maps_to":"Single Thing","metric":"調整後部門營業利益率與淨負債對調整後 EBITDA","threshold":"FY28 低於 27.0%，且 2028-06 季高於 2.5 倍","action":"清倉","source_freq":"季度新聞稿","date":"2028-08"},{"n":4,"text":"股價回到 800 美元以下。","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"不高於 800 美元","action":"重跑研究，利潤率與訂單門檻都沒踩線才分批反買","source_freq":"每日股價","date":null},{"n":5,"text":"復甦提早回落。","type":"風險","maps_to":"R1","metric":"滾動 12 個月訂單；亞太有機成長","threshold":"訂單連 2 季下滑且低於 +6%，或亞太低於 +10%","action":"停止加碼","source_freq":"季度新聞稿與法說","date":null},{"n":6,"text":"濾材集團綜效或還債落後。","type":"風險","maps_to":"R2","metric":"累計綜效；淨負債對調整後 EBITDA","threshold":"FY27 綜效低於 4,000 萬美元，FY27 結束槓桿高於 3.0 倍，或 FY28 結束累計低於 1 億美元","action":"減碼三分之一","source_freq":"季度法說","date":"2027-08"},{"n":7,"text":"關稅與貿易成本吸收失敗。","type":"風險","maps_to":"R3","metric":"調整後部門利潤率、毛利率、北美工業利潤率","threshold":"部門利潤率連 2 季年減 50 個基點以上，毛利率連 2 季年減 1 個百分點，或北美工業低於 25.5%","action":"減碼三分之一","source_freq":"季度新聞稿","date":null},{"n":8,"text":"Davidson Instruments 私人壟斷訴訟：Parker 已聲請駁回，尚未見裁決；受影響營收與求償金額事實表未涵蓋。","type":"風險","maps_to":"R3","metric":"法院對駁回聲請的裁定；公司揭露的可能損失","threshold":"駁回聲請遭否決，且公司揭露可能有重大影響","action":"減碼三分之一；轉為政府調查或刑事介入則清倉","source_freq":"10-Q 訴訟附註，每季","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":9,"text":"航太增產或售後不如預期。","type":"風險","maps_to":"R4","metric":"航太訂單年增率；737 與 A320 月產量","threshold":"航太訂單連 2 季低於 +5%，或 737 低於 35 架連 2 季，或 A320 在 2027 年到不了 70 架","action":"停止加碼","source_freq":"季度法說；月產量為資料缺口","date":null},{"n":10,"text":"股價提前走到 Base 五年終點。","type":"減碼","maps_to":"H2","metric":"收盤價","threshold":"不低於 1,230 美元，約 FY28 Base EPS 的 30 倍","action":"減碼四分之一","source_freq":"每日股價","date":null},{"n":11,"text":"FY28 指引高於 Base 且價格合理。","type":"加碼","maps_to":"H2","metric":"FY28 初始 EPS 指引中點與股價","threshold":"指引中點不低於 43 美元，且股價不高於 945 美元","action":"重跑研究後分批加碼","source_freq":"2027-08 財報","date":"2027-08"},{"n":12,"text":"2027 投資人會議後複審。","type":"複審日期","maps_to":"H3","metric":"新的長期有機成長、利潤率目標與併購規模","threshold":"會議結束","action":"重跑研究，新目標與併購規模納入情境樹","source_freq":"投資人會議","date":"2027-05-13"}],"kill_metrics":[{"metric":"FY28 全年調整後部門營業利益率","bear_threshold":"低於 27.0%","window":"FY2028（2028-06 結束）","source":"公司季度新聞稿","last_status":"ok"},{"metric":"滾動 12 個月訂單","bear_threshold":"連 2 季下滑且低於 +6%","window":"連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"淨負債對調整後 EBITDA","bear_threshold":"2028-06 季高於 2.5 倍","window":"2028-06 季","source":"公司法說","last_status":"ok"},{"metric":"FY27 自由現金流","bear_threshold":"低於 35 億美元","window":"FY2027","source":"公司季度新聞稿","last_status":"unknown"},{"metric":"濾材集團累計成本綜效","bear_threshold":"FY28 結束低於 1 億美元","window":"至 2028-06","source":"公司法說","last_status":"unknown"},{"metric":"北美工業調整後利潤率","bear_threshold":"低於 25.5%","window":"單季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"整體毛利率年變化","bear_threshold":"連 2 季年減 1 個百分點以上","window":"連續 2 季","source":"公司季報","last_status":"ok"},{"metric":"737 與 A320 月產量","bear_threshold":"737 低於 35 架連 2 季；A320 在 2027 年到不了 70 架","window":"至 2027 年底","source":"資料缺口，事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價收盤回到 800 美元以下（約 FY27 指引中點 21.7 倍，接近 104 週均線）","exec_line":"現價不追。股價到 800 美元以下、利潤率與訂單門檻都沒踩線時，先重跑研究，再分批買進，第一筆不超過預定部位的三分之一。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 800 美元以下（約 FY27 指引中點 21.7 倍），Base 年化回報才回到約 9–10%；或 FY28 初始指引中點不低於 43 美元且股價不高於 945 美元。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"工業復甦已從訂單走到出貨，加上航太長循環，FY27 有機成長達到指引中點 9%，之後五年平均不低於公司 4–6% 目標的上半段。","2y":"FY27 有機成長不低於 7.5%，FY28 不低於 5%，滾動 12 個月訂單維持正值。","5y":"FY27–FY31 平均有機成長不低於 5%。","10y":null,"threshold":"FY27 有機成長低於 7.5%，或 FY27–FY28 平均低於 5%。","source":"季度新聞稿的有機成長與滾動 12 個月訂單。","drift_rule":"2 年尺度：TTM 偏離路徑 5% 以上連 2 季算削弱，10% 以上連 3 季算反轉。5 年尺度：5% 以上連 4 季算削弱，10% 以上連 6 季算反轉。"},{"id":"H2","text":"部門利潤率的提升大多是結構性的，納入濾材集團後，仍能從 FY27 指引 27.9% 往公司 FY31 目標 30% 走。","2y":"FY28 調整後部門利潤率不低於 28.0%。","5y":"FY31 不低於 29.5%，FCF 利潤率回到 17%。","10y":"下一次工業衰退期間，單年部門利潤率不低於 26%。","threshold":"FY28 低於 27.0% 即論點失效；FY29 低於 28.0% 算削弱。","source":"季度新聞稿與法說。","drift_rule":"5 年尺度：連 4 季偏離路徑 5% 以上算削弱，連 6 季偏離 10% 以上算反轉。10 年尺度：跨 2 個年度算削弱，跨 3 個年度算反轉。"},{"id":"H3","text":"濾材集團與後續併購要把現金做大，不只把調整後 EPS 做大：2.2 億美元綜效兌現，槓桿按計畫回落。","2y":"FY27 綜效達 4,000 萬美元，FY28 結束累計不低於 1 億美元；2028-06 季淨負債對調整後 EBITDA 不高於 2.2 倍。","5y":"2.2 億美元綜效全數兌現，濾材集團 EBITDA 利潤率超過 30%；FY31 FCF 不低於 54 億美元。","10y":null,"threshold":"FY28 結束累計綜效低於 1 億美元，或 2028-06 季槓桿高於 2.5 倍。","source":"法說揭露的綜效累計數，新聞稿的槓桿與 FCF。","drift_rule":"2 年尺度：偏離路徑 5% 以上連 2 季算削弱，10% 以上連 3 季算反轉。"}],"R":[{"id":"R1","text":"復甦只走幾季就回落。亞太有機 +23.4% 靠電子與半導體拉動，管理層被問到 AI 相關占比時沒有給數字；滾動訂單又比單季訂單慢，轉折會晚看到。","h_ref":"H1","clock":"⚡","threshold":"滾動 12 個月訂單連 2 季下滑且低於 +6%，或亞太有機成長低於 +10%。","evidence_refs":[]},{"id":"R2","text":"濾材集團交易約當市值 8%，資金含 52.5 億美元 364 天與 25 億美元三年期貸款。整合若慢於計畫，利息先到、綜效後到；CIRCOR 還沒交割，槓桿可能升到約 3 倍。","h_ref":"H3","clock":"🔥","threshold":"FY27 綜效低於 4,000 萬美元，FY27 結束槓桿高於 3.0 倍，或 FY28 結束累計綜效低於 1 億美元。","evidence_refs":["major_events#1"]},{"id":"R3","text":"非美國銷售地點約占 36%，關稅、對中貿易限制、出口管制範圍變動與中東衝突墊高的物料物流成本，都可能壓縮利潤率。8,400 萬美元關稅退款已在 FY26 Q4 認列，後續退款金額較小。","h_ref":"H2","clock":"🔥","threshold":"吸收失敗判定：部門利潤率連 2 季年減 50 個基點以上，整體毛利率連 2 季年減 1 個百分點以上，或北美工業利潤率低於 25.5%。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"]},{"id":"R4","text":"航太 OEM 增產不如預期或售後退潮。航太約占營收三成、利潤率最高；管理層不談客戶機型產量，第三方報導訂單由 +18% 放緩到 +14%。","h_ref":"H1","clock":"🔥","threshold":"航太訂單連 2 季低於 +5%；沿用前份：737 月產量低於 35 架連 2 季，或 A320 在 2027 年到不了 70 架（月產量本輪事實表未涵蓋，屬資料缺口）。","evidence_refs":[]}],"single_thing":{"description":"FY28（2028-06 結束）全年調整後部門營業利益率低於 27.0%。","why_fatal":"這是五年路徑裡最大的單一營運敏感項。以 Base FY31 營收約 318 億美元計，部門利潤率每差 1 個百分點，EPS 差約 1.97 美元，占 Base 終端 EPS 3.7%，按 23 倍約 45 美元股價。低於 27.0% 代表濾材綜效加上量的復甦都撐不住利潤率，FY31 的 30% 目標不成立，本益比也會一起往 17–18 倍掉。","if_happens":"減碼一半，停止任何加碼；若 2028-06 季槓桿同時高於 2.5 倍，清倉。","how_monitor":"每季新聞稿的調整後部門利潤率與法說揭露的累計綜效；2027-08 公布 FY28 指引，中點低於 27.5% 就提前警戒。","probability":"12–24 個月約 15%。FY27 指引已含濾材稀釋仍有 27.9%，要跌 90 個基點以上，需要工業量明顯回落。"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.08,"peg_fy2":2.03,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":28.48,"FY2027E":35.59,"FY2028E":39.77,"FY2029E":44.14},"fy_end_month":6,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS，共識三年為調整後 EPS，兩者口徑不同，由 GAAP 基期算出的三年 CAGR 約 15.7% 會高估。本判斷改用 FY27E 到 FY29E 兩年複合 11.4%。共識來自 Koyfin 2026-11-07 快照，尚未反映 2026-11-05 指引上修，家數事實表未列。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"CIRCOR 商用與國防航空業務預計完成收購","impact":"中","watch":"交割後槓桿是否接近 3 倍。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 Q2 財報，公司指引營收近 62 億美元、調整後 EPS 8.82 美元、部門利潤率 27.6%","impact":"高","watch":"單季有機成長是否約 10%，濾材集團稀釋幅度。"},{"date":"2027-05-13","date_precision":null,"type":"guidance","event":"2027 投資人會議，公司將說明未來五年規劃","impact":"高","watch":"新的長期目標與下一階段併購規模。"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 全年財報與 FY28 初始指引","impact":"高","watch":"EPS 指引中點是否達 43 美元，部門利潤率指引是否低於 27.5%。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=4.64, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
