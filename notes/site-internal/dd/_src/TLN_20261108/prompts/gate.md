你是 DD 管線 v20 的判斷層閘（gate），標的 TLN（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1327 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi1_gaap`（q1_business）｜營業利益（GAAP）＝255 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi2_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司定義，無 non-GAAP 營業利益揭露）＝669 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi4_adjusted_free_cash_flow`（q1_business）｜Adjusted Free Cash Flow（公司定義）＝433 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi7`（q1_business）｜發電量／容量因數＝23.9 TWh｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi8`（q1_business）｜對沖比例（占預期發電量）＝80 %（2026 Q4）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_peer_tln_gross_margin_pct`（q2_moat）｜TLN 毛利率＝42.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TLN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tln_operating_margin_pct`（q2_moat）｜TLN 營業利益率＝15.33 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TLN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tln_fcf_margin_pct`（q2_moat）｜TLN FCF 利潤率＝6.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TLN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vst_gross_margin_pct`（q2_moat）｜VST 毛利率＝37.99 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VST.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vst_operating_margin_pct`（q2_moat）｜VST 營業利益率＝19.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VST.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vst_fcf_margin_pct`（q2_moat）｜VST FCF 利潤率＝11.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VST.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ceg_gross_margin_pct`（q2_moat）｜CEG 毛利率＝21.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CEG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ceg_operating_margin_pct`（q2_moat）｜CEG 營業利益率＝14.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CEG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nrg_gross_margin_pct`（q2_moat）｜NRG 毛利率＝18.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NRG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nrg_operating_margin_pct`（q2_moat）｜NRG 營業利益率＝6.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NRG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝16.99 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝27.7 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝39.62 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4363.61 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5056.96 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_gaap`（q1_business）｜歸屬股東淨利（GAAP）＝138 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi5_sbc_g_a`（q4_capital）｜SBC（損益表 G&A）＝51 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi6_2026_adjusted_ebitda_adj`（q4_capital）｜管理層指引：2026 全年 Adjusted EBITDA／Adj FCF＝— 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（SEC 8-K 附件）https://www.sec.gov/Archives/edgar/data/0001622536/000162253626000084/a20261103q32026earningsrel.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝9230.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 9569.0、現金 339.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝338.64 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.93 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 16.99，分子＝快照價 338.64｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝23962.64 USD m｜期間與口徑：2026-11-08／市值 14732.64 ＋ 淨負債 9230.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.49 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝47.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝57.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-12.35 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝49.79｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-20.38 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 21.34 → 16.99（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：競爭對手可能擁有更多資源、較新機組或較低成本；州或聯邦干預（補貼、公用事業電廠納入費率基礎）可能壓低容量與能源價格。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：相反觀點：有來源指公用事業承諾約 100 GW 新容量至 2030，第三方估計實際需求僅約 50 GW，指向可能過度建設；渦輪機訂單可能 2028 才交付
  - 來源：CreditSights podcast 'utilities the great data center overbuild'; DCD（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：PJM 市場監督人要求 FERC 駁回 Talen–Capital Power 電廠交易案，或附市場力承諾後重送。
  - 來源：pulse.bot：Reject Talen-Energy Capital Power Plant Deal, PJM Market Monitor Tells FERC（as_of 2026-04-02）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Talen 10-K 風險因子：新增或提高的關稅、貿易限制可能實質墊高燃料、材料、設備、零件成本或影響取得，未量化；無出口管制／Entity List 相關內容。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：核燃料及其部分原料／零組件供應商數量有限，供應中斷可能造成非計畫停機或燃料成本上升；Susquehanna 燃料循環已簽約至 2028 換料，2029 年超過 50%、2030 年超過 20%。
  - 來源：Talen Energy Form 10-K FY2025（as_of 2026-02-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Talen 在 Q1 2025 法說會表示供應鏈吃緊與關稅（尤其歐洲採購設備）使新建電廠更貴、近期更難交付；產業面大型燃氣渦輪交期逾五年、大型變壓器交期可達四年。
  - 來源：TLN Q1 2025 Earnings Call (allmind.ai); Utility Dive 5-year waits gas turbine（as_of 2025-05-08）｜affects：thesis.R、valuation
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：2026 年業界報導：Bloom 固態氧化物燃料電池（如 AEP 約 26.5 億美元、至多 1GW）與 SMR 被推為資料中心自備電力替代方案；多為聚合站/商業媒體，部分為框架協議，SMR 商轉多在 2030 後，未見直接指名 TLN。
  - 來源：enkiai.com / cleaner-energy-solutions 等聚合報導（低權威）（as_of 2026-09-30）｜affects：moat_trend、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：IEEFA 分析師指 AES、Calpine、Dynegy、NRG、Talen 在 2015 年股價下跌約 30%～66%（2014–2020 IPP 下行期）
  - 來源：IEEFA, Independent power producers after tough 2015 will seek ways to stick ratepayers in new year（as_of 2016-01-01）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Utility Dive 2019 稱 IPP 處境約三年前轉壞、之後幾無改善；投資等級最早在 2020 下半年或 2021 初才可考慮（下行期持續數年）
  - 來源：Utility Dive, The cold truth: today's market conditions are hurting independent power producers（as_of 2019-12-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：TLN 自 2024 年上市以來最深回撤為較前高低 33.8%，2025-03-10 落底（回撤追蹤站數據）；本公司無 2014–2020 週期的獨立上市價格史
  - 來源：ChartRow TLN drawdown / Trefis TLN（as_of 2026-11-01）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1092,"bear_5y_price":144,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":77.2,"ev5y_pct":59.1,"irr_base_pct":12.1,"asym_ratio":2.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":16.99,"pe":19.93,"basis":"FY1（FY2026E）共識 EPS，與終端年以當年度 EPS 計價同口徑"},"eps":{"bull":[30,46,58,68,78],"base":[27,38,43,46,50],"bear":[24,28,26,20,18]},"pe":{"bull":14,"base":12,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TLN_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：2026 調整後 EBITDA 財測區間上調（含 Cornerstone、市場更新、Keystone 出售抵減）（原話："EBITDA range for 2026 has increased to $2.025 billion to"）
- 2026-08-05｜CFO｜guidance：2026 調整後自由現金流財測區間上調為 12 億至 13.5 億美元（原話："free cash flow range to $1.2 billion to $1.35 billion"）
- 2026-08-05｜CFO｜guidance：2027 基準情境 FCF/股維持 34 美元，2028 升至 40 美元（原話："outlook remains $34 per share, increasing to $40 per share"）
- 2026-08-05｜CFO｜guidance：計入買回後，2027 FCF/股約 37 美元（原話："forecast 2027 cash flow at approximately $37 a share"）
- 2026-08-05｜CFO｜guidance：Cornerstone 交易宣布時給的 2027 pro forma EBITDA 約 26 億，本次表示已超過（原話："pro forma 2027 EBITDA of approximately $2.6 billion"）
- 2026-08-05｜CEO｜guidance：財測節奏：每年秋季給下一年度財測與後兩年展望（原話："provide guidance for the upcoming year each fall"）
- 2026-08-05｜President｜guidance：2028 PPL 與 ADHUB 遠期 spark spread 較 2025 年 7 月投資人日價格上升（原話："2028 PPL spark spreads are up 28%,"）
- 2026-08-05｜President｜guidance：管理層指出 PPL 基差擴大原因之一為南向輸電工程停電（原話："Two main drivers will work to compress that basis"）
- 2026-08-05｜President｜margin：PPL 相對 West Hub 折價由約 9 美元擴大到約 20 美元/MWh（原話："we have seen the basis grow to approximately $20 per"）
- 2026-08-05｜CFO｜margin：基差敏感度經驗法則：每改善 1 美元約增加 1 美元 FCF/股（原話："every $1 improvement in zonal basis across our portfolio"）
- 2026-08-05｜CFO｜margin：財測已採用反映擴大基差的 PPL 現行遠期價（原話："recent PPL marks that reflect the widened basis"）
- 2026-08-05｜CFO｜margin：AWS 滿載後長約毛利占比由 10% 升至 35%（原話："our long-term contracted margin increases from 10% to 35%"）
- 2026-08-05｜CFO｜margin：假設再增約 2GW 同類長約，示意毛利組合長約占比可達 60%（原話："60% of our gross margin mix under long-term contracts"）
- 2026-08-05｜President｜margin：年初至今 FCF 轉換率落在 60% 中段（原話："free cash flow conversion rate in the mid-60% range"）
- 2026-08-05｜CFO｜margin：Cornerstone 資產位於 ADHUB 而非 PPL，說明 2028 展望上調需同時看兩區（原話："those Cornerstone assets are in ADHUB and not PPL"）
- 2026-08-05｜CEO｜margin：本季調整後 EBITDA 3.74 億美元（原話："we delivered $374 million of adjusted"）
- 2026-08-05｜CEO｜capital_allocation：Q2 回購 55 萬股，維持把 70% 調整後 FCF 回饋股東的目標（原話："committed to our target of returning 70% of adjusted"）
- 2026-08-05｜CFO｜capital_allocation：預計至 2028 年底回饋股東至少 70% 的 FCF，共 28 億美元（原話："returning at least 70% of this cash, $2.8"）
- 2026-08-05｜CFO｜capital_allocation：現有買回授權剩 17 億美元，後續需董事會核准（原話："has $1.7 billion remaining"）
- 2026-08-05｜CFO｜capital_allocation：買回後仍有逾 13 億美元超額現金供其他用途（原話："This leaves more than $1.3 billion of excess cash"）
- 2026-08-05｜CFO｜capital_allocation：淨槓桿目標維持 3.5 倍（原話："continuing to target our net leverage ratio at 3.5x"）
- 2026-08-05｜President｜capital_allocation：併購以股票回購為門檻比較基準（原話："the share repurchase program is our hurdle"）
- 2026-08-05｜CEO｜capital_allocation：管理層稱曾用發股、舉債等工具做併購（原話："we've been flexible. We've issued shares to do deals."）
- 2026-08-05｜CEO｜capital_allocation：6 月完成 Waterford、Darby、Lawrenceburg 收購（原話："we closed on the Waterford, Darby and Lawrenceburg plants"）
- 2026-08-05｜CFO｜capital_allocation：Keystone 權益出售待完成，已反映於財測（原話："offset due to the pending sale of our interest in Keystone"）
- 2026-08-05｜CFO｜commitment：管理層承諾資本紀律，聚焦增加每股 FCF 的槓桿（原話："we will continue to maintain capital discipline"）
- 2026-08-05｜President｜commitment：新增容量專案須先達門檻報酬才會推進（原話："we'll have to clear the right hurdle"）
- 2026-08-05｜CEO｜commitment：不做 behind-the-meter 方案（原話："The one we're not doing is behind the meter."）
- 2026-08-05｜CEO｜commitment：管理層表示不預期未來頻繁更新多年展望，除非有重大業務變化（原話："provide guidance for the upcoming year each fall"）
- 2026-08-05｜CEO｜competition：管理層主張前表（front-of-the-meter）混合方案成本低於 behind-the-meter（原話："less expensive than any behind-the-meter solution"）
- 2026-08-05｜CEO｜competition：管理層稱 IRAS 實質上是 Connect and Manage（原話："IRAS is just Connect and Manage"）
- 2026-08-05｜CEO｜competition：管理層稱混合策略可作為 Connect and Manage 的安全港（原話："provides a safe harbor to"）
- 2026-08-05｜CEO｜competition：555 美元上限為平均值形成的軟上限（原話："the 555 cap, which is sort of a soft cap because"）
- 2026-08-05｜CEO｜risk：PPL 基差難以避險：交易不深、成本可能偏高（原話："It might become expensive to do it."）
- 2026-08-05｜CEO｜risk：雙邊市場長天期容量報價為薄量（原話："these are thinly traded"）
- 2026-08-05｜CEO｜risk：IRAS 細節未出，管理層稱影響難評估（原話："It's a bit of a hypothetical until we get proposal"）
- 2026-08-05｜President｜risk：PPL 區無資源充足性問題，發電過剩是基差原因（原話："PPL zone does not have a resource adequacy problem"）
- 2026-08-05｜CEO｜product：新增容量管線聚焦電池、尖峰機組與增容（原話："batteries, peakers and uprates"）
- 2026-08-05｜President｜product：設備供給可得，問題在價格（原話："The supply is there. It's available."）
- 2026-08-05｜President｜product：併購後新增燃氣廠增容項目納入新建容量管線（原話："we do have some upgrades that we're looking at"）
- 2026-08-05｜CFO｜customer：約 4GW 具電網負載承諾的資料中心站點（原話："advantaged data center sites with utility load commitments"）
- 2026-08-05｜CFO｜customer：潛在客戶擴及 co-locator、neo-cloud 與大型 C&I（原話："beyond hyperscalers to include Co-locators, Neo-clouds"）
- 2026-08-05｜CEO｜customer：管理層稱超大規模客戶決策時程為何時而非是否（原話："it's a matter of when, not if is the real point here"）
- 2026-08-05｜CEO｜customer：管理層稱無單一 gating 事項（原話："I don't know that there's any one particular gating item."）
- 2026-08-05｜CEO｜customer：超大規模客戶尋求 2028 年即可交付的容量（原話："all looking for something that can be done exactly in '28"）
- 2026-08-05｜CEO｜customer：長約遠期價已逼近先前與超大規模客戶討論的約 80 美元水準（原話："forwards have finally caught a bid"）
- 2026-08-05｜CEO｜customer：PJM 近三次容量拍賣均以價格上限結清（原話："the last 3 base residual capacity auctions clearing at"）
- 2026-08-05｜CEO｜customer：管理層稱遠期曲線開始反映供給緊俏（原話："we have seen bids at the cap level for the early"）
- 2026-08-05｜CEO｜guidance：避險：2028 年避險比率季增約 5% 至 25–30%（原話："quarter-over-quarter, 25% to 30%"）
- 2026-08-05｜President｜guidance：避險使用將結果區間圍起來的工具，並保留部分上行參與（原話："some instruments that allow us to fence in outcomes"）
- 2026-08-05｜CEO｜capital_allocation：收購動機：認為能量與容量被低估（原話："we felt as though energy and capacity was underpriced"）
- 2026-08-05｜President｜product：車隊容量因子 51%，較去年高 14 個百分點（原話："achieving a 51% fleet-wide capacity factor"）

### 問答異常語氣（迴避／改口／保留）
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Storozynski 問氣電資產長約價差相對遠期的溢價是否壓縮｜答法：未給數字，以玩笑帶過並稱 willing buyer/willing seller，改談混合方案價值
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Moses Sutton 追問 2028 FCF/股由 36 升至 40 的橋接項目（OpEx、協同、發電量）｜答法：未拆解各項貢獻，回答為整體企業模型與遠期價更新，僅 CFO 補充 ADHUB 影響
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Constantine Lednev 問 4GW 是否與前一季相比有變動｜答法：CFO 稱不評論專案數量，只說持續推進與擴充
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Carly Davenport 問是否參與 RBP 中央採購或雙邊流程｜答法：稱計畫參與但不保證，並說仍在研讀 695 頁文件
- TLN_Q2_2026_Earnings_Call_20260805.md｜問：Michael Sullivan 問 IRAS 對未來容量拍賣的影響｜答法：稱未聽清並表示須等內容出來再判斷，未直接回答

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 5 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 3 | 2 |
| cyclical_supply_discipline_capacity | found | 4 | 2 |
| cyclical_inventory_price_position | found | 3 | 2 |
| cyclical_prior_downcycle_behavior | found | 3 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Talen Energy largest customer Amazon contract 2026 diversify OR self-supply OR in-house；Talen Energy Amazon data center customer concentration risk 2026 hyperscaler contract；Amazon AWS nuclear SMR OR self-build power Susquehanna Talen contract amended behind-the-meter FERC 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260612","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"PJM 結構性缺電使容量價 + spark spread 維持高位（非曇花一現）","columns":{"2Y 驗證點":"2028/29 BRA 清算價守在高檔","5Y 驗證點":"容量價在去上限後仍 &gt;$200/MW-day","10Y 驗證點":"PJM 負載成長持續 &gt; 新供給","具體數字門檻":"27/28 BRA $333/MW-day（cap）；目標 2028/29 &gt;$200","信息來源":"PJM BRA 報告 / 法說","漂移觸發條件":"連 1 次 BRA &lt;$150 → 削弱（容量週期屬慢變數）"}},{"id":"H2","text":"AWS 1,920 MW PPA 如期爬坡 + FTM 結構規避 FERC 風險","columns":{"2Y 驗證點":"2026H1 co-lo 轉 FTM 完成（傳輸升級後）","5Y 驗證點":"2029 爬坡達 840-1,200 MW","10Y 驗證點":"2032 達 1,680-1,920 MW，~$18B 收入兌現","具體數字門檻":"2029 ≥ 840 MW；契約至 2042","信息來源":"Talen 6/11/25 PR；AWS PPA","漂移觸發條件":"FTM 結構遭新監管挑戰 或 爬坡延後 &gt;12 月 → 削弱"}},{"id":"H3","text":"三併購（~5.4 GW）以增值倍數整合，FCF/share 持續累積 + 槓桿可控","columns":{"2Y 驗證點":"2027 FCF/share ~$34 兌現；淨槓桿 &lt;3.5x","5Y 驗證點":"2028 FCF/share $36→$41（含回購）","10Y 驗證點":"併購資產 ROIIC &gt; WACC 經週期驗證","具體數字門檻":"2027 FCF/share ≥$30；淨槓桿 ≤3.5x","信息來源":"Q1'26 法說 guidance","漂移觸發條件":"淨槓桿 &gt;3.5x 連 2 季，或 FCF/share 下修 &gt;15% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PJM 容量價上限鬆綁 / 回落（新供給回應 + 行政上限到期）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"BRA 清算價","警戒閾值":"2028/29 BRA &lt;$200/MW-day"}},{"id":"R2","text":"Spark spread 隨新氣電產能 + 天然氣價波動回落","columns":{"對應假設":"H1/H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"前向 spark spread 曲線 vs guidance","警戒閾值":"實現 spread 連 2 季低於 guidance &gt;10%"}},{"id":"R3","text":"監管/政治：FERC 對 co-location 與資料中心併網的限制擴大（電費轉嫁公眾爭議）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"FERC/PJM 規則制定、州 PUC 動向","警戒閾值":"FTM 結構被新規則納管 或 新增 ISA 全面凍結"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟢","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":360.54,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TLN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Talen Energy"},"oneliner":"PJM 缺電讓 Talen 2027 至 2029 年每股現金大增，但 AWS 滿載後合約毛利也只占約 35%，其餘仍看電價、容量上限與區域基差；指引上調，獲利卻可能接近循環高段，等 2027 年 5 月容量規則定案再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TLN_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺 PJM 電能與容量市場的錢，AWS 是唯一已簽的大型長約，利潤卡在既有可調度機組與併網位置這一節點。","reasoning":"2026 Q3 營收 13.27 億美元、營業利益 2.55 億美元（營益率 19.2%）、調整後 EBITDA 6.69 億美元、調整後自由現金流 4.33 億美元，發電 23.9 TWh；TTM 毛利率 42.67%、營益率 15.33%。分部只取得 2026 Q2：能源及其他 7.22 億美元、容量 2.37 億美元，Q3 分部事實表未涵蓋。避險比例是賺錢方式的關鍵：2026 Q4 約 80%，2027 約 70%，2028 約 35%，2029 除 AWS 外大致未對沖，所以遠期曲線一動，2028 年後的現金就跟著動。單點依賴：AWS 是唯一已簽的大型長約，也壓在 Susquehanna 單一站址；單一客戶占營收比例事實表未涵蓋。供需判斷：缺口到約 2029 至 2030 年是結構性的，之後供給可逆性提高。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_adjusted_ebitda_non_gaap","f_kpi4_adjusted_free_cash_flow","f_kpi7","f_kpi8","f_peer_tln_gross_margin_pct","f_peer_tln_operating_margin_pct"],"verdict_values":{"revenue_quality":"容量約占能源加容量營收四分之一（2026 Q2 為 24.7%），單價受拍賣上限約束；其餘電能收入隨遠期曲線與區域基差波動，AWS 滿載前合約占比低。","unit_econ_note":"Q3 中間型機組容量因數由約 36% 升到 52%，量價同向。新建複循環全包成本逾每 MWh 120 美元（2026-11-03 CEO）是合約價上緣，長天期遠期約 80 美元（2026-08-05 CEO）是目前參考。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"2021、2022、2025 三個 GAAP 虧損年，毛利率由 13.58% 到 42.67%，收入主要由電價與容量價決定，符合商品型；AWS 長約是另計的長期部位。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久到約 2029 至 2030 年：PJM 連續拍賣未達可靠度要求，渦輪交期把新複循環併網推到 2030 年或更晚；之後供給可逆性提高，過度建設疑慮與 2029 年遠期曲線逆價差都指向這段窗口有終點。","bargaining":{"up":"渦輪與設備商議價力強，關稅與交期抬高新建與維修成本；核燃料供應商有限。","down":"電能與容量由市場定價，公司是價格接受者；AWS 為長約，超大規模客戶對價格敏感（2026-11-03 CEO、President）。","geo":"資產集中 PJM，已賣出 ERCOT 資產，區域規則變動無法分散。"},"profit_pool_dir":"利潤池向既有發電資產集中，但上限制度與州級干預限制上行；合約化會把部分利潤移到買方可議價的區間。","tam_table":{"expanded":false,"reason":"資產型發電商的成長看電價、容量價與回購，不看滲透率；事實表未涵蓋 TAM 與五年營業利益池序列。"}}}},"q2_moat":{"verdict":"護城河方向穩定：既有機組位置與併網權的稀缺性在提高，但價格上限、區域基差與買方議價同步壓住可收割的部分。","reasoning":"機制是時間與成本門檻，不是客戶鎖定或技術優勢。同業 ROIC 事實表未涵蓋，改看可比利潤率：TLN 毛利率 42.67%，高於 VST 37.99%、CEG 21.43%、NRG 18.8%；營益率 15.33%，低於 VST 19.38%、高於 CEG 14.34% 與 NRG 6.28%；FCF 率 6.27%，低於 VST 11.74%。同業數字只到 2026-06，TLN 到 2026-09，且各家營收組成不同，差距不能直接當護城河差距。執行面穩定，定價面穩定：容量價連續貼上限，但上限同時封住上行，AWS 之後還沒有第二筆長約。","fact_refs":["f_peer_tln_gross_margin_pct","f_peer_tln_operating_margin_pct","f_peer_tln_fcf_margin_pct","f_peer_vst_gross_margin_pct","f_peer_vst_operating_margin_pct","f_peer_vst_fcf_margin_pct","f_peer_ceg_gross_margin_pct","f_peer_ceg_operating_margin_pct","f_peer_nrg_gross_margin_pct","f_peer_nrg_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"既有可調度機組、併網權與資料中心用地的稀缺性：新建複循環全包成本逾每 MWh 120 美元、併網可能到 2030 年或更晚，時間門檻是主要障礙。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面穩定：三年回購約三分之一股本，收購逾 70 億美元後 2028 展望再升。定價面穩定：容量價連三次貼上限，但 2027/28 若無上限約 530 美元、實際約 333 美元；PPL 基差由約 9 美元擴大到約 20 美元；AWS 之後尚無新長約。","competitor_notes":[{"name":"CEG","strategy_note":"毛利率 21.43%、營益率 14.34%，收購 Calpine 後規模更大；營收組成事實表未涵蓋，利潤率差距僅供參考。"},{"name":"VST","strategy_note":"營益率 19.38%、FCF 率 11.74%，都高於 TLN；擬收購 Cogentrix，是資產收購市場的競爭對手。"},{"name":"NRG","strategy_note":"毛利率 18.8%、營益率 6.28%，利潤率明顯較低；業務組成事實表未涵蓋，僅供參考。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用毛利率、營益率與 FCF 率比較。","threats":[{"level":"🔴","text":"州與聯邦干預（上限、補貼、公用事業電廠納入費率基礎）壓低容量與能源價格，影響整個市場的獲利結構；2026-11-03 法說已提到春季可能再設上限。","p":"35%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"新供給與過度建設：公用事業承諾新增容量高於第三方需求估計，競爭者可能有較新機組或較低成本。","p":"30%","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1"]},{"level":"🟡","text":"燃料電池與小型模組化核電等自備電力替代，來源多為聚合報導與框架協議，小型核電多在 2030 年後，未見直接指名 TLN；機率按破壞性競爭下限取 30%。","p":"30%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"市場力審查：PJM 市場監督人曾要求 FERC 駁回 Capital Power 資產交易或附承諾，該案已於 2026-06 取得核准，但下一筆 PJM 收購會更難。","p":"30%","evidence_refs":["regulatory_antitrust#3"]}],"roic_durability":{"quadrant":"高利益率×低周轉（投入資本事實表未涵蓋，依資產密集型態定性）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心，決策者是超大規模業者與開發商，付款者最終含一般電費用戶，三者利益不一致。需求目前成立：PJM 2027/28 預測尖峰增量約 5,250 MW，其中近 5,100 MW 來自資料中心；PPL 區到 2031 年合約負載 10.7GW，其中 6GW 在建。實際通電量的資料還不夠。"},{"item":"決策層級","level":"🟡","text":"替代性要在每個站址與併網時點衡量：AWS 合約約 17 年，2029 年最低承諾 840 MW，轉換難度高；但其餘約 65% 毛利是全 PJM 電能與容量，替代性高，President 也說 PPL 區沒有資源充足問題（2026-08-05）。"},{"item":"價值鏈分配","level":"🟡","text":"新建複循環全包逾每 MWh 120 美元是合約上緣，長天期遠期約 80 美元是目前參考，中間價值由發電商、設備商與買方分。管理層自己說買方對價格敏感，氣電長約至今未出現，2026-08-05 被問溢價是否壓縮時也未給數字。"},{"item":"社會容忍度","level":"🔴","text":"容量價上限本身就是政治定價：2027/28 若無上限約 530 美元，實際約 333 美元，少約 37%。賓州行政命令、費率保護承諾與春季再設上限的傳聞都在同一方向，實際價格上限取經濟與政治兩者較低者。"}],"roiic":15.5,"reinvest_rate":30,"endo_ceiling":4.7,"formula_note":"增量報酬＝（2027 調整後自由現金流指引中點 16.25 億美元－FY2025 申報自由現金流 4.98 億美元）÷收購總額約 72.5 億美元＝約 15.5%；混用調整後與申報口徑，又含電價上漲，視為上限。併購標的個別 EBITDA 與投入資本事實表未涵蓋。再投資率未照標準公式（資本支出、折舊、營運資金事實表未涵蓋），以未來配發 70% 後剩下的 30% 代替；過去兩年收購金額遠高於此。內生上界＝15.5%×30%＝約 4.7%。"}}}},"q3_growth":{"verdict":"五年後跑道中等：AWS 爬坡與回購提供能見度，第二條成長曲線（第二筆長約與 4GW 用地）還沒簽下來。","reasoning":"FY1 至 FY3 共識 EPS 由 16.99 美元到 39.62 美元，兩年 CAGR 約 52.7%；FY2025 為虧損，無法計算三年 CAGR；EPS 家數事實表未涵蓋，營收共識為 13 至 15 位分析師。內生上界約 4.7%，缺口約 48 個百分點，可以歸因：第一是電價與容量價帶來的利潤率擴張（2028 ADHUB、PPL 遠期價差年初以來升近 30%），第二是收購資產全年貢獻，第三是淨回購（2027 自由現金流指引中點的 70% 除以市值，每年約 7.7%）；FY1 分母偏低也放大了 CAGR。管理層 2029 基準每股現金中點 48 美元與 2028 相同，含回購才到 56 至 60 美元，代表 2029 年的成長主要靠縮股。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"2026 至 2029 年以電價與容量價為主，其次是併購全年貢獻與回購；量來自中間型機組運轉時數與 AWS 爬坡。","runway_years":6,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 4.7%＝增量報酬約 15.5%×未來再投資率約 30%，推導見護城河段；共識 CAGR 遠高於此，差額來自價格、併購全年化與回購。","segments":[{"item":"能源及其他營收（2026 Q2）","value":"7.22 億美元"},{"item":"容量營收（2026 Q2）","value":"2.37 億美元"},{"item":"2026 Q3 分部","value":"事實表未涵蓋"},{"item":"長約毛利占比","value":"AWS 滿載後約 35%；再簽 2GW 的示意情境可到 60% 以上，未計入基準展望"}],"decay_signals":["已亮：EPS 成長高於營收成長逾 5 個百分點（FY1 至 FY2 EPS 增 63%、營收增 15.9%）","未亮：SBC 占營收 3.8%，低於 5%","未亮：未見提價後銷量下滑，Q3 中間型機組容量因數由約 36% 升到 52%","未亮：需求市場未見萎縮","未亮：新產能投資持續，管線 3GW 以上","無法判定：毛利率連兩季年減、核心市占、FCF 對淨利比連兩年、產業倍數下移、維護性資本支出占比（事實表未涵蓋）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置積極且有紀律，但回購與收購都用槓桿放大，而且集中在循環上行段。","reasoning":"FCF 對淨利 Q3 為 3.1 倍（4.33 億對 1.38 億美元），但淨利受衍生品與折舊影響，這個比率不能直接當品質證據。SBC 占營收 3.8%（5,100 萬對 13.27 億美元），未達警戒。現金去向四分事實表未涵蓋；前九個月調整後自由現金流 9.95 億美元，目標約 70% 回饋股東。淨負債 92.3 億美元對 2026 EBITDA 指引中點 21.25 億美元約 4.3 倍，對 2027 中點 26.75 億美元約 3.5 倍，管理層目標是 2027 下半年回到 3.5 倍。容量收入提前變現是否計入淨負債，事實表未涵蓋。申報口徑 TTM 自由現金流率只有 6.27%，和調整後數字差距大，調整項明細事實表未涵蓋。","fact_refs":["f_kpi4_adjusted_free_cash_flow","f_kpi3_gaap","f_kpi5_sbc_g_a","f_kpi0_gaap","f_kpi6_2026_adjusted_ebitda_adj","f_net_debt_m","f_peer_tln_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"收購總額約 72.5 億美元，粗估增量報酬上限約 15.5%，含電價順風；資金成本與個別資產貢獻事實表未涵蓋，無法判定是否已實現高於資金成本。"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"以 2027 基準每股現金 38 美元對現價 338.64 美元，收益率約 11.2%；十年期殖利率事實表未涵蓋，須高於 9.2% 才不過，判定通過，但分子是循環上行段數字。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 5,100 萬美元，年化 2.04 億美元，占市值 147.33 億美元約 1.4%；管理層稱 ASR 完成後累計回購約三分之一股本。Cornerstone 發行約 240 萬股屬併購，另計。"}]},"governance":{"capital_returns":[{"item":"收購累計","value":"Freedom、Guernsey 約 38 億美元（2025-11），Waterford、Darby、Lawrenceburg 約 34.5 億美元（2026-06，含約 240 萬股）"},{"item":"回購","value":"授權上調至 30 億美元、至 2028 年底，內含 15 億美元 ASR；約 380 萬股已先註銷，預計 2027 Q1 完成"},{"item":"配發目標","value":"約 70% 調整後自由現金流，至 2029 年累計回購逾 40 億美元"},{"item":"融資來源","value":"ASR 由容量收入提前變現支應，義務 2027-06 至 2029-05 攤還；金額事實表未涵蓋"},{"item":"股權發行","value":"Cornerstone 發行 2,399,998 股，約占目前股數 5.5%"}]}}},"q5_valuation":{"verdict":"現價要求 2027 至 2029 年每股現金指引大致兌現，且倍數在循環後段守住約 12 倍；我信 2027 年，2029 年後只信一半。","reasoning":"現價 338.64 美元對 FY1 EPS 16.99 美元為 19.93 倍，對 FY2 EPS 27.7 美元為 12.23 倍；EV 239.6 億美元對 2027 EBITDA 指引中點 26.75 億美元約 9.0 倍，對 FY1 營收 5.49 倍。每股現金收益率：2027 約 11.2%，2028 基準約 14.2%；管理層說的 2029 約 17% 已含回購，不含回購約 14.2%。PEG 0.38 看起來很低，但 EPS 基期受壓、公司屬循環型，不作便宜依據。12 個月上檔以 2028 基準每股現金 48 美元×8 倍＝384 美元，約 +13.4%；中期以 FY2029 基準 EPS 43 美元×12 倍＝516 美元，約 +52.4%。同業前瞻倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_m","f_ev_s_fwd","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"FY1、FY2 本益比與每股調整後自由現金流收益率；商品型優先看股價淨值比，但事實表未涵蓋。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻倍數，無法作承重對照；終端倍數改以自身 FY2 的 12.23 倍對照，並標為資料缺口。"},"fwd_pe":19.93,"peg":0.38,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 19.93 倍、第二年 12.23 倍，2027 基準每股現金收益率約 11.2%，單看偏便宜；但分母是循環上行段的數字，2028 年只對沖約 35%，2029 年除 AWS 外大致未對沖。P/S 與 EV/S 在僅有的年度端點分別落 47.6% 與 57.9%，位置在中段。五年分位無法計算（上市未滿五年，只有四個年度端點）。結論定為合理，不因低本益比給便宜。","upside_short_pct":13.4,"upside_mid_pct":52.4,"denominator_disputed":true,"denominator_note":"分母爭點有兩層：FY1 EPS 受 GAAP 評價與收購影響，三個月下修 20.38%；2027 至 2029 每股現金則是循環上行段且部分未對沖的數字。低本益比與高現金收益率都不能當便宜的論證。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 2027 至 2029 年的高段現金當常態，估值陷阱風險中等。","reasoning":"最強空方數字是 FY1 共識三個月下修 20.38%、TTM 申報自由現金流率 6.27%、淨負債 92.3 億美元；下行期歷史見反證紀錄。管理層有幾次沒正面回答：2026-08-05 法說未拆解 2028 每股現金由 36 升到 40 美元的橋接項目（問者 Sutton），也未量化氣電長約溢價（問者 Storozynski）；2026-11-03 CFO Muller 被問哪項上行最有把握時，自己承認沒有直接回答。訴訟方面，Winter Storm Uri 賠償以保險給付為限，未見證券集體訴訟。反面看法：若 2027 年約 70% 對沖部位如期落袋，短期現金並不脆弱，這個陷阱要到 2028 年後才會顯現。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_peer_tln_fcf_margin_pct","f_net_debt_m","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高段現金被當成常態，亮一項衰退訊號"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":16.99,"pe":19.93,"basis":"FY1（FY2026E）共識 EPS，與終端年以當年度 EPS 計價同口徑"},"eps":{"bull":[30,46,58,68,78],"base":[27,38,43,46,50],"bear":[24,28,26,20,18]},"pe":{"bull":14,"base":12,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"max_dd":{"lo":-66,"hi":-40,"basis":"下限取 IEEFA 記錄的 2015 年獨立發電商最深約 −66%，並深於情境樹最差終點約 −57.5%（18 美元×8 倍＝144 美元）；上限 −40% 略深於 TLN 上市以來最深回撤 −33.8%，因為淨負債 92.3 億美元且 2028 年只對沖約 35%。","trigger_time":null},"basis":{"bull":"再簽 2GW 長約、PPL 基差每 MWh 收斂約 5 美元（每股現金約加 5 美元）、曲線轉平（加 2 至 3 美元）、AWS 提前一年（加約 2 美元），合約毛利升到 60% 以上後倍數給 14 倍。","base":"2027、2028 年略低於共識（2026-09-30 後基差再擴大），2029 年對應管理層含回購每股現金 56 至 60 美元，2030 年後靠 AWS 爬坡與回購抵消曲線回落；每股路徑已含回購，殖利率欄填 0 防止重複計算；終端 12 倍比照目前第二年 12.23 倍，同業前瞻倍數事實表未涵蓋。","bear":"2029 年後新供給與上限改制把容量價壓到每 MW-日 200 美元以下、遠期價差回落，2028 年只有約 35% 對沖保護，回購因槓桿暫停。機率 35% 的依據：路徑高於內生成長上界、過去獨立發電商下行持續數年、管理層自己的 2029 基準不再成長。終端 8 倍約為目前第二年倍數的三分之二，反映成長熄火；同業前瞻倍數事實表未涵蓋。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2015 年獨立發電商股價跌約 30% 到 66%，下行期持續數年；TLN 上市以來最深回撤 33.8%，沒有經歷過完整下行期的上市價格史；公用事業承諾新增約 100GW，第三方估計需求僅約 50GW。","assumption":"資料中心負載如期落地，供給要到 2030 年前後才跟上。","consequence":"容量價跌破每 MW-日 200 美元、遠期價差回落時，2028 年後未對沖部位一起重定價；淨負債 92.3 億美元放大股權跌幅，五年虧五成的路徑成立。","ruling":"採納，納入 35% 悲觀機率與 −66% 回撤下限；與唯一致命點是同一條傳導線。","watch":"PJM 拍賣清算價、2028 與 2029 年 ADHUB、PPL 遠期價差、PPL 區資料中心實際通電量。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#2"]},{"view":"論點成功但股東經濟變差","evidence":"上限讓 2027/28 容量價停在約 333 美元（無上限約 530 美元）；賓州行政命令與費率保護承諾要求新增容量；管理層說超大規模客戶對價格敏感；ASR 由容量收入提前變現支應。","assumption":"缺電成立時，超額利潤大多留在發電商。","consequence":"社會容忍度是實際定價上限，電價越高干預越強；長約可能要搭配電池與尖峰機組，報酬被稀釋；回購在循環高段以預支現金買進，每股現金上升但安全邊際下降。","ruling":"採納，定價力評分壓在 5，合約溢價未計入基準路徑。","watch":"第二筆長約的價格與附帶新增容量要求、2027-05 拍賣規則、ASR 最終均價與 2027-06 起的攤還。"},{"view":"論點成功但股東經濟變差","evidence":"2026 前九個月調整後自由現金流 9.95 億美元，申報口徑 TTM 自由現金流率只有 6.27%，以 TTM 營收約 44.8 億美元估約 2.8 億美元；調整項明細事實表未涵蓋。","assumption":"調整後自由現金流能完整轉成可分配現金。","consequence":"若差額多為持續性支出，70% 配發與每股現金目標都被高估。","ruling":"不採信也不否定，標為未證、監測；預登記連四季申報自由現金流低於調整後數字一半，即視為調整項不是一次性。","watch":"10-Q 現金流量表與財報新聞稿的調整項對帳。"},{"view":"價格已反映太多","evidence":"2028 ADHUB、PPL 遠期價差年初以來漲近 30%，TTM 毛利率 42.67% 高於近四個年度；管理層 17% 收益率已含回購；FY1 共識三個月下修 20.38%。","assumption":"目前遠期曲線是合理常態。","consequence":"2029 基準每股現金與 2028 中點一樣是 48 美元，成長已靠回購，便宜的只是高段數字。","ruling":"部分反駁：26 週跌 12.35%、P/S 與 EV/S 在年度端點中段，沒有過熱；但便宜論證不成立，結論定為合理。","watch":"2027 指引中點、2029 遠期曲線形狀。"}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 360.54 → 本次 338.64（-6.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=360.54","side_b":"本次 price_at_dd=338.64","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 360.54 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 360.54 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 360.54 美元：Bull 價 1,092、Bear 價 144，五年期望值 +49.4%，基準年化 10.7%，不對稱比 1.93","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.93。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 360.54 美元：五年期望值 +49.4%，基準年化 10.7%，不對稱比 1.93","side_b":"本次情境、股價 338.64 美元：五年期望值 +59.1%，基準年化 12.1%，不對稱比 2.21","ruling":"再換股價、情境不動：起點價下跌 6.1%，五年期望值多 9.7 個百分點，基準年化多 1.4 個百分點，不對稱比由 1.93 升到 2.21。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份空欄首次落值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","p_bull_pct","p_bear_pct","max_dd_pct","archetype","cycle_position"],"side_a":"前份這些欄都是空值，沒有護城河方向、五年後跑道、情境機率、回撤範圍、公司類型與循環位置。","side_b":"本次護城河方向穩定、五年後跑道中等、機率樂觀 20／基準 45／悲觀 35、回撤 −40% 至 −66%、循環/商品、中循環；裁決與角色由程式依輸入落值。","ruling":"屬研究框架補齊，不代表基本面在這些欄位改變。","evidence_level":"方法說明","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"訊號等級與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號等級 B、陷阱風險中等，股價 360.54 美元。","side_b":"本次維持 B 與中等：正面是 2027 基準每股現金由 34 升到約 38 美元、2028 由 40 升到 48 美元；負面是 FY1 共識三個月下修 20.38%、2029 基準不再成長。","ruling":"兩側大致抵銷，維持不變。","evidence_level":"公司財測與共識快照","settle_metric":"2027 年初法說的 2027 指引與實現價差","if_then":["若 2027 指引中點連兩季上修且申報自由現金流跟上，陷阱風險降為低。","若中點下修逾 10%，減碼一半。"],"evidence_refs":[]},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份估值結論為便宜，股價 360.54 美元。","side_b":"本次結論為合理，股價 338.64 美元，下跌 6.1%。","ruling":"股價下跌本身應該讓估值更便宜；結論反而轉為合理，原因是本次把每股現金視為循環上行段數字，改看年度端點分位與情境結果，不再只看低本益比。","evidence_level":"事實表估值分位與共識","settle_metric":"2027 至 2029 每股現金實現度","if_then":["若 2027 年 5 月規則定案且 2029 遠期曲線逆價差收斂，估值結論改回便宜。"],"evidence_refs":[]},{"axis":"假設與風險門檻","cause":"新證據","prior_field":["thesis.H1","thesis.H3","thesis.R1","thesis.R2"],"side_a":"舊門檻：H1 目標 2028/29 拍賣高於 200 美元、連 1 次低於 150 美元削弱；H3 2027 每股現金不低於 30 美元、淨槓桿連 2 季高於 3.5 倍削弱；R1 2028/29 拍賣低於 200 美元；R2 實現價差連 2 季低於指引逾 10%。","side_b":"新門檻：H1 改看 2026-12 與 2027-05 兩次拍賣，任一次低於 200 美元削弱、連兩次低於 150 美元反轉；H3 2027 基準每股現金不低於 34 美元、2027 下半年淨槓桿不高於 3.5 倍；R1 容量清算價低於 200 美元；R2 保留原門檻，另加 PPL 基差連兩季高於每 MWh 25 美元。","ruling":"舊→新理由：2028/29 拍賣已清在約 325 美元，驗證點後移；每股現金指引上調，門檻隨之提高。前份淨槓桿條件已觸發：收購後至少連兩季高於 3.5 倍，以 2026 指引中點計約 4.3 倍，H3 的槓桿部分判定削弱。本次改為 2027 下半年回到 3.5 倍，是放寬，依據是管理層公布的攤還時程；未回到 3.5 倍則停止加碼，高於 3.75 倍減碼一半。","evidence_level":"公司財測與 PJM 報告","settle_metric":"2027 年第三、四季淨槓桿","if_then":["若 2027 下半年淨槓桿高於 3.75 倍，減碼一半。","若淨槓桿在 3.5 至 3.75 倍之間，停止加碼。"],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設進場重啟條件（空值）。","side_b":"2027 年 5 月容量拍賣規則定案且清算價不低於每 MW-日 250 美元，觸發後重跑研究才進場。","ruling":"本次點名的約束是 2029 年後容量定價規則未定，重啟條件就是這項約束解除。","evidence_level":"事件條件","settle_metric":"2027-05 拍賣規則與結果","if_then":["若條件成立，重跑研究後首倉不超過 3%。","若股價先漲而條件未成立，不追。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼或清倉的數字門檻（空值）。","side_b":"容量清算價低於每 MW-日 200 美元減碼一半；低於 150 美元且第二筆長約未簽則清倉；2027 基準每股現金指引中點低於 34 美元減碼一半。","ruling":"把前份的風險門檻變成可執行的減碼與清倉動作。","evidence_level":"方法說明","settle_metric":"PJM 拍賣結果與每季指引","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點為空值，未設定。","side_b":"PJM 在 2027 年 5 月拍賣前調降或重設容量價上限，使 Talen 清算價跌破每 MW-日 200 美元","ruling":"本次首次設定 Single Thing，選擇依據是離散事件中對每股現金敏感度最大的一項。","evidence_level":"法說與 PJM 報告","settle_metric":"2027-05 拍賣規則與清算價","if_then":["若清算價低於 200 美元，減碼一半。","若低於 150 美元且第二筆長約未簽，清倉。"],"evidence_refs":[]},{"axis":"結構性缺電與商品循環","cause":null,"prior_field":null,"side_a":"2026-11-03 CEO：這不只是又一個商品循環，需求在，供給不在。PJM 連續兩次拍賣未達可靠度要求，2028/29 再短缺約 6,831 MW，渦輪積壓約 80GW，新複循環併網到 2030 年或更晚。","side_b":"2029 遠期曲線逆價差，年減逾每 MWh 2 美元；管理層 2029 基準每股現金中點 48 美元與 2028 相同；CreditSights 指公用事業承諾約 100GW，第三方需求估計約 50GW；2026 初在建氣電超過 29GW。","ruling":"裁定兩者時間窗不同：缺口到 2029 至 2030 年是結構性的，之後按循環處理，所以基準路徑在 2029 年後放緩，終端倍數只給 12 倍。產業態勢裁定雙向拉鋸：競爭未見惡化，同業以收購為主；結構轉好來自連續拍賣短缺；其他結構變數是容量上限與大型負載規則正在改寫。決勝數據 2027 年 5 月才有，在那之前不可裁決。","evidence_level":"PJM 報告與公司財測為高，過度建設來源為中","settle_metric":"2027-05 拍賣清算價與 2029 遠期曲線形狀","if_then":["若 2027-05 清算不低於每 MW-日 250 美元且 2029 曲線不再逆價差，重跑研究後首倉不超過 3%。","若任一次拍賣清算低於 200 美元，減碼一半。","反向條件：股價先漲到 475 美元（2027 基準每股現金收益率 8%）而規則未定，不追。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"全區缺電與 PPL 區過剩","cause":null,"prior_field":null,"side_a":"2026-11-03 President：市場越來越需要可靠發電，PPL 基差收斂是上行槓桿，原因是區內負載爬升與輸電升級。","side_b":"2026-08-05 President：PPL 區沒有資源充足問題，發電過剩是基差原因，基差由約 9 美元擴大到約 20 美元；2026-11-03 Wells Fargo 提問指 9 月底後再擴大；2026-08-05 CEO 也說基差避險可能很貴。","ruling":"管理層的暫時性歸因不採信也不否定，標為未證、監測。預登記期限：連四季 PPL 基差未回到每 MWh 15 美元以下，歸因證偽，2028 至 2029 每股現金按當時基差下修。每 MWh 5 美元約等於每股 5 美元，約占 2028 基準一成。","evidence_level":"法說原話，基差最新數字事實表未涵蓋","settle_metric":"PPL 對 West Hub 基差","if_then":["若連四季未回到 15 美元以下，減碼三分之一。","若收斂到 12 美元以下且區內資料中心通電，停止減碼並上修每股現金路徑。"],"evidence_refs":[]},{"axis":"EPS 下修與現金上修","cause":null,"prior_field":null,"side_a":"FY1 共識 EPS 三個月由 21.34 美元降到 16.99 美元，下修 20.38%。","side_b":"2028 基準每股調整後自由現金流由 40 升到 48 美元，約升兩成。","ruling":"可調和但未解決：GAAP EPS 受衍生品評價、收購與折舊影響，現金方向較可信；但申報自由現金流率僅 6.27%，暫不把調整後數字全額當可分配現金。FY1 至 FY3 最近兩次快照沒有變動，Q3 新指引可能還沒進賣方模型，加碼先凍結到下一次法說。","evidence_level":"共識快照與公司財測","settle_metric":"申報自由現金流占調整後自由現金流比例","if_then":["若連四季申報自由現金流低於調整後數字一半，減碼三分之一。","若比例回到七成以上，解除加碼凍結。"],"evidence_refs":[]},{"axis":"第二筆長約的時間","cause":null,"prior_field":null,"side_a":"2026-08-05 CEO：超大規模客戶是何時而不是是否。2026-11-03 CEO：不會為別人的時間表犧牲價值，其他資源的合約正在來。","side_b":"除 AWS 外至今沒有新長約；2026-11-03 Barclays 問 2 月雙邊窗口，CFO 答不受時程約束；Seaport 指氣電長約遲遲未見；President 說買方不會不計價。","ruling":"基準路徑不計第二筆長約。連續兩季說法一致但沒有成交，視為尚未兌現的說法，合約溢價不進倍數。","evidence_level":"法說原話","settle_metric":"2027 年底前新簽長約規模","if_then":["若 2027 年底前簽下至少 1GW 且合約毛利朝 60% 前進，加碼至 5%。","若 2027 年底仍未成交，基準終端倍數不上調，停止加碼。"],"evidence_refs":[]},{"axis":"賣方目標價與本次等待","cause":null,"prior_field":null,"side_a":"賣方平均目標價 460.08 美元（2026-10-06，Q3 前），高於現價約 36%，8 買進、3 中立、1 賣出；另一來源區間 411 至 510 美元（日期不明），全距窄。","side_b":"本次不追，12 個月上檔只估約 13%。","ruling":"賣方方向反對本結論。分歧在倍數假設：賣方把循環上行段現金當可持續。Q3 後目標價調整事實表未涵蓋。股價已跌 12.35% 不是安全邊際。","evidence_level":"賣方彙整，非原始報告","settle_metric":"Q3 後目標價更新與 2027-05 拍賣","if_then":["若 2027-05 清算守住 250 美元以上，本次過度保守，依重啟條件進場。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"2027 年約 70% 已對沖，每股現金 38 美元對現價收益率約 11.2%，淨槓桿將回到 3.5 倍，管理層基準不含任何新長約，第二筆合約、基差收斂、AWS 提前都是未計入的選擇權；26 週跌 12.35%，賣方目標約 460 美元。","side_b":"決定 2029 年以後現金的容量規則在 2027-05 前不會定案；2028 年只對沖約 35%，9 月底後基差再擴大尚未反映；第二筆長約沒有時間表。","ruling":"維持等待事件，不設進場價；這是論點未決，不是估值太貴。","evidence_level":"法說與事實表","settle_metric":"2027-05 拍賣規則與結果","if_then":["若股價先漲而拍賣規則未落地，不追。","若股價跌破 270 美元（2027 基準每股現金收益率約 14%）而 2027 指引與容量規則沒有變壞，分批反買，單筆不超過 1%。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2026 年 12 月 PJM 容量拍賣結果確認價格維持在上限附近","type":"假設驗證","maps_to":"H1","metric":"PJM 基本剩餘拍賣清算價（每 MW-日）","threshold":"不低於 250 美元；低於 200 美元轉為減碼條件","action":"低於 200 美元減碼一半；其餘不動作","source_freq":"PJM 拍賣報告，逐次","date":"2026-12"},{"n":2,"text":"PJM 在 2027 年 5 月拍賣前調降或重設上限，使清算價跌破 200 美元","type":"Single Thing","maps_to":"Single Thing","metric":"2027-05 拍賣規則與清算價","threshold":"低於每 MW-日 200 美元","action":"減碼一半；低於 150 美元且第二筆長約未簽則清倉","source_freq":"PJM、FERC 公告，逐次","date":"2027-05"},{"n":3,"text":"PPL 區基差未如管理層所說收斂","type":"風險","maps_to":"R2","metric":"PPL 對 West Hub 基差（每 MWh）","threshold":"連兩季高於 25 美元，或連四季未回到 15 美元以下","action":"減碼三分之一，下修 2028 每股現金路徑","source_freq":"法說與避險揭露，每季","date":"2027-11"},{"n":4,"text":"容量規則定案，解除本次等待的約束","type":"估值rearm","maps_to":"H1","metric":"2027-05 拍賣規則與清算價","threshold":"規則定案且清算價不低於每 MW-日 250 美元","action":"重跑研究，不直接建倉；通過後首倉不超過 3%","source_freq":"PJM 公告，逐次","date":"2027-05"},{"n":5,"text":"簽下第二筆大型長約","type":"加碼","maps_to":"H2","metric":"新簽長約規模與長約毛利占比","threshold":"至少 1GW，且長約毛利朝 60% 前進","action":"已持有且重啟條件成立時加碼至 5%","source_freq":"公司公告，逐次","date":"2027-12"},{"n":6,"text":"2027 每股現金指引下修","type":"減碼","maps_to":"H3","metric":"2027 基準每股調整後自由現金流指引中點","threshold":"低於 34 美元（目前約 38 美元）","action":"減碼一半","source_freq":"法說，每季","date":"2027-02"},{"n":7,"text":"容量價崩落且槓桿未回落","type":"清倉","maps_to":"H1/H3","metric":"容量清算價與淨槓桿","threshold":"清算價低於每 MW-日 150 美元，且 2027 下半年淨槓桿高於 4 倍","action":"清倉","source_freq":"PJM 報告與 10-Q","date":"2027-11"},{"n":8,"text":"下一次法說更新指引、避險與基差","type":"複審日期","maps_to":"H3","metric":"2027 指引、2028 避險比例、PPL 基差","threshold":"法說後更新情境路徑","action":"解除或延長加碼凍結","source_freq":"法說，每季","date":"2027-02"},{"n":9,"text":"PPL 區資料中心通電落後，需求基礎轉弱","type":"風險","maps_to":"R3","metric":"PPL 區 6GW 在建資料中心實際通電量","threshold":"2028 年底通電不到 3GW","action":"減碼三分之一","source_freq":"PPL 與公司法說，每季","date":"2028-12","evidence_refs":["supply_demand_durability#2"]},{"n":10,"text":"CEO 交棒後資本配置改變","type":"風險","maps_to":"R5","metric":"配發比例與收購規模","threshold":"四季內把 70% 配發目標下調，或宣布超過市值 10% 且未增厚每股現金的收購","action":"停止加碼","source_freq":"公司公告與法說","date":"2027-11"}],"kill_metrics":[{"metric":"PJM 基本剩餘拍賣清算價（每 MW-日）","bear_threshold":"低於 200 美元減碼一半；低於 150 美元且無第二筆長約清倉","window":"2026-12 與 2027-05 兩次拍賣","source":"PJM 拍賣報告","last_status":"ok"},{"metric":"2027 基準每股調整後自由現金流指引中點","bear_threshold":"低於 34 美元（目前約 38 美元）","window":"每季，至 2027 年底","source":"公司法說與財測","last_status":"ok"},{"metric":"PPL 對 West Hub 區域基差（每 MWh）","bear_threshold":"連兩季高於 25 美元，或連四季未回到 15 美元以下","window":"每季，至 2027 年底","source":"公司法說；2026-08-05 約 20 美元","last_status":"warning"},{"metric":"淨槓桿（管理層口徑）","bear_threshold":"2027 下半年高於 3.75 倍","window":"2027 Q3 至 Q4","source":"10-Q 與法說","last_status":"warning"},{"metric":"申報自由現金流占調整後自由現金流比例","bear_threshold":"連四季低於 50%","window":"每季滾動四季","source":"10-Q 現金流量表與財報新聞稿","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027 年 5 月容量拍賣規則定案且清算價不低於每 MW-日 250 美元","exec_line":"約束是 2029 年後容量定價規則未定；條件成立後重跑研究，首倉不超過 3%；股價先漲而條件未成立不追；第二筆長約只提高持倉上限，不單獨構成進場條件。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 5 月容量拍賣規則定案且清算價不低於每 MW-日 250 美元；這是事件條件，不設進場價，條件成立後重跑研究。"},"thesis":{"H":[{"id":"H1","text":"PJM 缺電讓容量價與價差在 2029 年前維持高於中週期","2y":"2026-12 與 2027-05 兩次拍賣清算都不低於每 MW-日 250 美元","5y":"取消上限後容量價仍高於 200 美元","10y":"PJM 負載成長持續高於新供給","threshold":"2026-12 拍賣在約 325 美元上限附近；2027-05 不低於 250 美元；任一次低於 200 美元轉弱","source":"PJM 拍賣報告、公司法說附錄","drift_rule":"任一次清算低於 200 美元為削弱；連兩次低於 150 美元為反轉；容量屬慢變數，逐次看，不看 TTM 偏離。"},{"id":"H2","text":"AWS 依最低承諾爬坡，滿載後長約毛利約 35%，第二筆長約決定倍數能否上移","2y":"2028 年約 480 MW；2027 年底前第二筆至少 1GW（未簽不破論點，但倍數不上調）","5y":"2029 年最低承諾 840 MW；2032 年 1,680 至 1,920 MW","10y":"合約至 2042 年、名目約 180 億美元兌現","threshold":"2029 年不低於 840 MW；合約最高 1,920 MW、至 2042 年","source":"AWS 合約公告、公司法說","drift_rule":"爬坡落後最低承諾或延後逾 12 個月為削弱；併網供電結構被新規則納管為削弱；解約或最低承諾下修為反轉。"},{"id":"H3","text":"收購與回購把現金轉成每股複利，淨槓桿回到 3.5 倍","2y":"2027 基準每股調整後自由現金流不低於 34 美元，2027 下半年淨槓桿回到 3.5 倍","5y":"2029 含回購每股 56 至 60 美元的中點下修不超過 15%","10y":"併購資產增量報酬高於資金成本，經一個完整循環驗證","threshold":"2027 基準每股現金不低於 34 美元（指引約 38）；2028 基準不低於 43 美元（指引 48）；2027 下半年淨槓桿不高於 3.5 倍","source":"公司財測、法說、10-Q","drift_rule":"指引中點連兩季偏離 5% 以上為削弱；連三季偏離 10% 以上為反轉；2027 下半年淨槓桿高於 3.75 倍為削弱。"}],"R":[{"id":"R1","text":"PJM 容量上限調降或規則改寫，含州與聯邦干預","h_ref":"H1","clock":"🔥","threshold":"容量清算價低於每 MW-日 200 美元","evidence_refs":["competitive_share_entrants#1"]},{"id":"R2","text":"遠期價差與 PPL 區基差不利，2028 年後未對沖部位重定價","h_ref":"H1/H3","clock":"⚡","threshold":"實現價差連兩季低於指引逾 10%；PPL 基差連兩季高於每 MWh 25 美元","evidence_refs":[]},{"id":"R3","text":"資料中心需求落空或新供給超預期，含過度建設與自備電力","h_ref":"H1","clock":"🐢","threshold":"PPL 區 6GW 在建資料中心 2028 年底通電不到 3GW","evidence_refs":["supply_demand_durability#2","substitute_technology#2"]},{"id":"R4","text":"監管與政治：併網供電結構、大型負載規則、賓州行政命令、市場力審查限制併購","h_ref":"H2","clock":"🐢","threshold":"併網供電結構被新規則納管，或新增併網協議全面凍結，或下一筆收購遭 FERC 否決","evidence_refs":["regulatory_antitrust#3"]},{"id":"R5","text":"CEO McFarland 交棒後資本配置改變；交棒時程與細節事實表未涵蓋","h_ref":"H3","clock":"🔥","threshold":"四季內 70% 配發目標下調，或宣布超過市值 10% 且未增厚每股現金的收購","evidence_refs":[]},{"id":"R6","text":"Susquehanna 單一站址、核燃料供應商有限，以及關稅與設備交期墊高成本","h_ref":"H2","clock":"🐢","threshold":"Susquehanna 非計畫停機連續 30 天以上；2029、2030 年燃料簽約比例低於目前的逾 50%、逾 20%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]}],"single_thing":{"description":"PJM 在 2027 年 5 月拍賣前調降或重設容量價上限，使 Talen 清算價跌破每 MW-日 200 美元","why_fatal":"容量是最大的單一離散變數：每 MW-日 100 美元，以 2026/27 清出的 6,702 MW 計約 2.45 億美元、每股約 5.7 美元；以控制的 13.1GW 計上限約每股 11 美元，都高於或接近基差每 MWh 5 美元對應的每股 5 美元。它同時打到 H1 與 H3，也削弱簽長約的議價基礎。電價是連續變數，放在風險門檻管理。","if_happens":"減碼一半；若清算價低於 150 美元且第二筆長約未簽，清倉。情境機率轉向悲觀，終端倍數改用 8 倍。","how_monitor":"PJM 與 FERC 的上限申請、2026-12 及 2027-05 拍賣參數與結果、公司法說的容量假設。","probability":"12 至 24 個月約 15% 至 20%。三次拍賣連續貼上限，管理層也承認春季傳出再設上限，但過去多為設上限而非大幅調降，系統短缺 6.6 至 6.8GW 限制調降幅度。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":12.23,"peg_fy2":0.23,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":-4.79,"FY2026E":16.99,"FY2027E":27.7,"FY2028E":39.62},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識；FY2025A 取 yfinance GAAP 稀釋 EPS，為負值，故 CAGR 改以 FY1 至 FY3 兩年計算（約 52.7%）；EPS 受衍生品評價與收購影響，口徑爭議見估值分母說明。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"PJM 基本剩餘容量拍賣，管理層預期清在上限附近","impact":"中","watch":"清算價、Talen 清出 MW"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"RBP 雙邊合約窗口截止，確切日期事實表未涵蓋","impact":"中","watch":"是否出現新長約"},{"date":"2027-02","date_precision":"quarter","type":"guidance","event":"2026 Q4 法說，更新 2027 指引與避險比例","impact":"高","watch":"每股現金、基差、淨槓桿"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"15 億美元 ASR 預計完成","impact":"低","watch":"最終股數與均價"},{"date":"2027-05","date_precision":"month","type":"regulatory","event":"下一次容量拍賣與價格上限規則定案","impact":"高","watch":"上限延長或調降、清算價"},{"date":"2027-12","date_precision":"quarter","type":"guidance","event":"淨槓桿預計在 2027 下半年回到 3.5 倍","impact":"中","watch":"容量提前變現的攤還進度"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-12.35, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
