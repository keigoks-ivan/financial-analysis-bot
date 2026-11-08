你是 DD 管線 v20 的判斷層閘（gate），標的 CAH（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝67513 USD m｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益＝1001 USD m｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝753 USD m｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_kpi6_fy2027_non_gaap_eps`（q1_business）｜FY2027 non-GAAP EPS 指引＝12.8～13.0 USD｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：共識 FY1 EPS 12.56（財報前快照 2026-11-07 xlsx，指引下緣已高於共識；來源 dd_numbers_extra.py consensus_revision）
- `f_peer_cah_gross_margin_pct`（q2_moat）｜CAH 毛利率＝3.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_operating_margin_pct`（q2_moat）｜CAH 營業利益率＝1.26 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_fcf_margin_pct`（q2_moat）｜CAH FCF 利潤率＝1.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_gross_margin_pct`（q2_moat）｜MCK 毛利率＝3.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_operating_margin_pct`（q2_moat）｜MCK 營業利益率＝1.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_fcf_margin_pct`（q2_moat）｜MCK FCF 利潤率＝1.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cor_gross_margin_pct`（q2_moat）｜COR 毛利率＝4.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cor_operating_margin_pct`（q2_moat）｜COR 營業利益率＝1.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cor_fcf_margin_pct`（q2_moat）｜COR FCF 利潤率＝0.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hsic_gross_margin_pct`（q2_moat）｜HSIC 毛利率＝31.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HSIC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝12.56 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝14.06 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝15.61 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝266074.5 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝282369.46 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_non_gaap_eps`（q4_capital）｜Non-GAAP 稀釋 EPS＝3.26 USD｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_kpi4_1_398_157`（q4_capital）｜自由現金流（營業現金流 1,398 − 資本支出 157，自算）＝1241 USD m｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_kpi5_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝10.9 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得（新聞稿未列共識，未另查證）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝231.14 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3551.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 8815.0、現金 5264.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.756 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝271.72 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.63 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 12.56，分子＝快照價 271.72｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝15.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝48.62 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 271.72 / W52 219.16 / W104 180.24 / W250 122.33 / W250 13週斜率 2.81%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝219.16 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝180.24 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：FY2026 10-K 列出主要對手：Pharma 為 McKesson、Cencora 等；GMPD 為 Medline、Owens & Minor 等；並稱新進入者、新商業模式與產業整併可能加劇競爭壓力、壓縮利潤，客戶整併可能導致從兩家既有供應商中只選一家而流失客戶。未揭露具體份額數字或具名新進入者。
  - 來源：SEC EDGAR 10-K FY2026 Competition（as_of 2026-08-11）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：最大客戶 CVS Health 占 FY2026 營收 28%，前五大客戶合計 43%（集中度高）。
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-11）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：CVS Health 為最大客戶，占 FY2026 營收 28%、期末應收帳款毛額 22%；前五大客戶合計占營收 43%；10-K 自述銷售與信用集中度顯著，若主要客戶減少採購、違約或不續約，營運與財務可能受不利影響。
  - 來源：SEC EDGAR｜Cardinal Health 10-K FY2026（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：DOJ 於 2023-11 發出 CID，調查 2022 年收購 GPO 與風濕科 MSO 少數股權交易是否違反反回扣法與 False Claims Act；公司配合調查，屬非反壟斷事項。
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：自2025年2月起CAH已支付約2億美元IEEPA關稅，主要在GMPD部門；最高法院2026年2月裁定IEEPA關稅違法。
  - 來源：SEC EDGAR 10-K FY2026 MD&A Tariffs（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：GMPD持續承受Section 122/232/301及Smoot-Hawley 308關稅帶來的成本增加，調價未能完全抵銷。
  - 來源：SEC EDGAR 10-K FY2026 MD&A Tariff Environment（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：2026年4月總統公告對品牌藥及相關原料進口課關稅，Pharma部門可能受影響。
  - 來源：SEC EDGAR 10-K FY2026 MD&A Tariff Environment（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：總統聲明學名藥2028年起課100%、2029年起課200%關稅，實施仍高度不確定，可能影響Pharma部門成本或供給。
  - 來源：SEC EDGAR 10-K FY2026 MD&A Tariff Environment（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K 揭露 2024 年 4 月 FDA 對 CAH 發警告信：向中國第三方製造商採購的塑膠針筒缺乏適當 510(k) 許可
  - 來源：Cardinal Health Form 10-K FY2026 (SEC)（as_of 2026-08-15）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 警示：供應商不合規或生產地點轉移過去曾、未來可能導致營運實質修改
  - 來源：Cardinal Health Form 10-K FY2026 (SEC)（as_of 2026-08-15）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FY2026 10-K 揭露競爭壓力可能因新商業模式、新進入者等而加劇，並持續面臨定價壓力影響毛利；未點名具體替代技術。
  - 來源：SEC EDGAR 10-K FY2026 全文（as_of 2026-08-11）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#0`（channel_business_model_shift｜方向 -｜狀態 ok）：10-K 指出競爭壓力可能因新商業模式、新進入者、法規變動而加劇，產業整併與製造商直接配送給客戶亦構成競爭。
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-11）｜affects：moat_trend、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：IVC 濾器產品責任訴訟持續：2023-04 和解約 4,375 件 $2.75 億，其餘案件續辯；2026-06-30 應計 $2,900 萬
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-11）｜affects：decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：Webcol 大型酒精棉片因微生物污染自願召回（FDA 公告 2026-03-20）
  - 來源：pulse.bot 轉載 Cardinal Health 公告（as_of 2026-03-20）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：IVC 產品責任訴訟持續；搜尋未見2026新證券集體訴訟（Cordis 案 $1.09 億已於2023-09 final approval）
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-11）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：Webcol 酒精棉片微生物污染召回（2026-03-20）
  - 來源：pulse.bot（as_of 2026-03-20）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":512.4,"bear_5y_price":182.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":36.8,"ev5y_pct":26.2,"irr_base_pct":6.5,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":12.9,"pe":21.06,"basis":"FY1 口徑：FY2027（2027-06 止）公司指引中值 12.90，終端倍數同為當年度前瞻口徑；共識 12.56 是財報前快照，已低於指引下緣。"},"eps":{"bull":[14.8,16.9,19.2,21.7,24.4],"base":[14.3,15.85,17.45,19.05,20.65],"bear":[13.0,13.2,13.4,13.7,14.0]},"pe":{"bull":21,"base":18,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.756,"net_buyback":0.9},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAH_Q4_2026_Earnings_Call_20260811.md
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 EPS 指引區間（原話："expect fiscal '27 EPS to be between $12.40 and $12.60"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 EPS 成長指引 13–15%（對基準）；長期 12–14% 重申（原話："EPS growth rate guidance of 12% to 14% per year"）
- 2026-08-11｜CFO Aaron Alt｜margin：FY27 基準 EPS 排除 Q4 一次性 $0.31 關稅退款（原話："So the baseline adjusted non-GAAP EPS number is $10.95."）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 營收 FY27 成長 3–5%（原話："Pharma segment revenue to show 3% to 5% growth"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 部門利潤 FY27 成長 8–11%（原話："we expect the Pharma segment to deliver 8% to 11% growth"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 利潤成長節奏：Q1 接近區間高端（含 Solaris）（原話："we expect Q1 profit growth to be near the high end of our"）
- 2026-08-11｜CFO Aaron Alt｜guidance：已宣布併購貢獻 Pharma 利潤成長 2–3 個百分點（原話："M&A is expected to contribute 2 to 3 percentage points"）
- 2026-08-11｜CFO Aaron Alt｜guidance：GMPD FY27 部門利潤指引 $200–220M（原話："expected segment profit of $200 million to"）
- 2026-08-11｜CFO Aaron Alt｜guidance：GMPD Q1 FY27 利潤約為 FY26 Q1 的一半，後段加權（原話："roughly half of the Q1 fiscal 2026 result"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Other 群組營收成長指引 11–13%，並於年內加速（原話："we anticipate 11% to 13% growth in revenue"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Other 群組利潤成長指引 15–18%（原話："We expect segment profit to deliver 15% to 18% growth in the"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 利息及其他費用指引（原話："interest and other expense to be $240 million to $290"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 有效稅率指引 19–20%（原話："tax rate to be 19% to 20% for the year"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 調整後自由現金流指引 $3.5–4B（原話："between $3.5 billion and $4 billion in adjusted free"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 資本支出預期 $700M（原話："we expect capital expenditures of $700 million"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 至少 $10 億回購（原話："least $1 billion in share repurchases"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：董事會增加 $50 億回購授權（原話："has authorized a $5 billion increase to our share repurchase"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：新授權被形容為補充彈藥（原話："our new authorization effectively recharges the battery"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 不假設重大併購，保留小型併購彈性（原話："not assuming material M&A, but have reserved modest"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：可能考慮策略性併購或額外資本回饋（原話："consider strategic M&A or incremental return of capital"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY26 回購總額與均價（原話："totaled $1.35 billion of share repurchase during the year"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：新 $40 億循環信貸取代三個舊額度（原話："a new $4 billion revolver program, replacing 3"）
- 2026-08-11｜CFO Aaron Alt｜margin：Q4 GMPD 認列一次性 IEEPA 退款淨營業利益 $1 億（原話："a onetime $100 million net operating earnings benefit"）
- 2026-08-11｜CFO Aaron Alt｜margin：Q4 EPS 中 $0.31 來自 IEEPA 退款（原話："$0.31 of the EPS is due to recording the IEEPA tariff refund"）
- 2026-08-11｜CFO Aaron Alt｜margin：管理層稱退款屬非經常性（原話："We view the refund as nonrecurring"）
- 2026-08-11｜CFO Aaron Alt｜risk：取代 IEEPA 的關稅仍持續產生成本（原話："incur costs from the tariffs that replaced IEEPA"）
- 2026-08-11｜CFO Aaron Alt｜margin：GMPD Q4 部門利潤扣除退款後為 $5,000 萬（原話："GMPD segment profit was $50 million, normalized for the"）
- 2026-08-11｜CFO Aaron Alt｜product：Cardinal Health 自有品牌排除關稅影響後連續第六季至少中單位數成長（原話："the sixth consecutive quarter of at least mid-single-digit"）
- 2026-08-11｜CFO Aaron Alt｜margin：Pharma 營收中 GLP-1 順風與 IRA WACC 逆風各約 500 bp，大致抵銷（原話："IRA WACC changes, each worth approximately 500 basis points"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 IRA 價格變動對營收影響與 FY26 下半年相近，且無利潤不利影響（原話："to have no adverse profit impact"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 營收假設：強勁但非超額需求（原話："strong demand, but not the outsized demand we experienced"）
- 2026-08-11｜CFO Aaron Alt｜customer：Pharma 客戶續約含 Kroger 長期延長（原話："long-term extension with Kroger"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Specialty 營收含有機與已宣布併購，雙位數成長（原話："all organic and already announced inorganic efforts"）
- 2026-08-11｜CEO Jason Hollar｜customer：GMPD 最大客戶長期續約（原話："long-term renewal of our largest customer"）
- 2026-08-11｜CEO Jason Hollar｜customer：3PL 取得兩項基因療法商業化協議；細胞與基因治療市占（原話："exclusively service nearly half the cell and gene market"）
- 2026-08-11｜CEO Jason Hollar｜product：Theranostics 與 PET 成長率（原話："PET growing over 20% and Theranostics growing nearly 30%"）
- 2026-08-11｜CEO Jason Hollar｜product：ADS 整合綜效高於預期（原話："where we are seeing greater than anticipated synergies"）
- 2026-08-11｜CEO Jason Hollar｜commitment：Biopharma Solutions 2028 年 $10 億目標，稱進度符合（原話："getting that business to $1 billion by '28"）
- 2026-08-11｜CEO Jason Hollar｜product：Biopharma Solutions 成長 20% 以上（原話："20-plus percent growth expected and realized"）
- 2026-08-11｜CEO Jason Hollar｜risk：IRA/340B 等監管：管理層認為不應改變其報酬（原話："don't believe our compensation should change"）
- 2026-08-11｜CEO Jason Hollar｜risk：340B 對醫院客戶影響可能大於對公司影響（原話："customer impact is likely to be greater than our impact"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：FY27 投資優先順序框架與去年相同（原話："commentary certainly is exactly the same"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：擴產以瓶頸（冷凍冷藏）與自動化為導向，非先建後等客（原話："not like we're a build-it-and-they-will-come strategy"）
- 2026-08-11｜CEO Jason Hollar｜competition：分銷模式可能演變，管理層稱將調整（原話："So the model will change. It will evolve."）
- 2026-08-11｜CEO Jason Hollar｜margin：企業整體彙總利潤率約 1%（原話："our margin at 1% overall aggregate margins"）
- 2026-08-11｜CEO Jason Hollar｜margin：Other 群組三個事業毛利結構差異；OptiFreight 利潤率較高（原話："services business has an overall higher rate"）
- 2026-08-11｜CFO Aaron Alt｜margin：學名藥轉換帶來較高獲利，並預期 FY27 續有貢獻（原話："we prefer the profitability that comes with a generic"）
- 2026-08-11｜CFO Aaron Alt｜risk：GLP 量成長但放緩（原話："growing but moderating GLP volumes"）
- 2026-08-11｜CEO Jason Hollar｜risk：油價/商品成本壓力：若全年居高，GMPD 落在指引低端（原話："closer to that bottom end of our guidance range for GMPD"）
- 2026-08-11｜CFO Aaron Alt｜risk：若伊朗衝突拖長，GMPD 利潤傾向指引低端（原話："Should the conflicts in Iran prove protracted"）
- 2026-08-11｜CEO Jason Hollar｜commitment：GMPD 改善計畫維持（原話："the GMPD improvement plan remains in place"）
- 2026-08-11｜CEO Jason Hollar｜guidance：FY27 學名藥量成長仍未達長期規劃 2–3% 的上緣（原話："still not in the 2% to 3% range for '27"）
- 2026-08-11｜CFO Aaron Alt｜guidance：稅率 19% 預期延續至 FY27；更長期稅率延後說明（原話："19% anticipated rate for '26 to be durable into '27"）
- 2026-08-11｜CEO Jason Hollar｜commitment：管理層稱過去四年達成所說的事（原話："we have done what we said we would and more"）

### 問答異常語氣（迴避／改口／保留）
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Kevin Caliendo（UBS）：量化「超額需求」與「強勁需求」差異｜答法：Aaron Alt 表示不提供數學公式（'we're not going to provide you with a mathematical'）；Jason Hollar 改以 Specialty 與學名藥量舉例，未給界線數字
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Allen Lutz（BofA）：品牌轉學名藥對營收與 EBIT 加速各貢獻多少｜答法：Aaron 稱學名藥為正貢獻但未給數字；Jason 稱 'not so much that we're going to break out that number'，僅說遠低於 500 bp
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Lisa Gill（JPM）：IRA 之外的監管風險與 340B 對醫院客戶量的影響｜答法：Jason 以通則回答（與各方密切接觸、支持可及性與可負擔性），未給 340B 量的影響數字
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Stephen Baxter（Wells）：新聞稿未點名 Nuclear 為利潤成長驅動的原因｜答法：Aaron 稱 'I wouldn't read too much into the order of prioritization'，未直接說明未點名原因
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Kevin Caliendo（UBS）：19–20% 稅率是否為長期基準｜答法：Aaron 確認 FY27 稅率，長期稅率 'defer comments' 留待之後

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 1 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 2 | 3 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 5 | 0 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 衛星候選","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Specialty 業務超越基底分銷，貢獻 OI 25%+","columns":{"2Y 驗證點":"Specialty 營收 YoY ≥ 18%","5Y 驗證點":"Specialty OI ≥ 25% 全公司 OI","10Y 驗證點":"Specialty + MSO 平台 OI ≥ 40% 全公司 OI","具體門檻":"FY26: Specialty 營收 +20% YoY (Q3 已達)；FY28 Specialty OI 占比 ≥ 22%","來源":"FY26 法說會、mgmt Investor Day 2025 9/2025","漂移觸發":"連 2 季 TTM 偏離 ≥ 5% → 削弱（2Y 假設）"}},{"id":"H2","text":"Pharma 段 OI margin 穩定在 1.4%+","columns":{"2Y 驗證點":"連續 4 季 OI margin ≥ 1.35%","5Y 驗證點":"5Y 滾動均 OI margin ≥ 1.40%","10Y 驗證點":"10Y 平均 OI margin ≥ 1.35%（即使遇 cycle 低谷）","具體門檻":"FY25: Pharma OI margin = 1.42%；FY26 guide 維持 +OPI growth 9-11%","來源":"FY25 10-K、Q3 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱（5Y 假設）"}},{"id":"H3","text":"大客戶結構保持穩定（CVS、Walmart 維持合約）","columns":{"2Y 驗證點":"無大客戶流失公告","5Y 驗證點":"Top 10 客戶占比 ≥ 60%（穩定）","10Y 驗證點":"無新 vertical PBM 整合導致分銷結構重組","具體門檻":"FY25 10-K 揭露 5 大客戶占比 50%+；無公開 contract 更動","來源":"FY25 10-K","漂移觸發":"單一客戶流失公告 → 立即重評（不需連兩季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大客戶流失（CVS / Walmart 等轉投 MCK）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期","監測指標":"季度 8-K 客戶留存公告 + Pharma 營收 YoY","警戒閾值":"季度 Pharma 營收 YoY 跌破 5%（暗示大客戶流失，已知 baseline ~9%）"}},{"id":"R2","text":"關稅 + manufacturer 議價權壓縮 Pharma OI margin","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"Pharma segment OI margin（季度）","警戒閾值":"連兩季 ≤ 1.35%（FY25 = 1.42%，跌 5bp 即削弱 H2）"}},{"id":"R3","text":"GLP-1 處方量見頂 / 被新藥取代 + biosimilar 滲透加速","columns":{"對應假設":"H1","時間尺度":"🐢 長期","監測指標":"GLP-1 weekly scripts、biosimilar share、specialty mix","警戒閾值":"2027-2028 期間 Specialty 整體 YoY 連 4 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":200.68,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CAH","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cardinal Health"},"oneliner":"CVS 續到 2032 年、財測再上修，生意比半年前更穩；但股價已由 201 美元漲到 272 美元，倍數由約 17 倍升到 21 倍。基本面沒壞，五年年化報酬只剩約 7%，等 232 美元以下再買。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺藥廠、藥局與醫療體系之間的配送和採購價差，錢卡在全美三強寡占的配送節點，再靠學名藥採購、專科服務和 Other 三個事業加厚；最大單點依賴是 CVS。","reasoning":"FY2026 營收 2,542 億美元，Pharma 2,348 億占約 92%，部門利潤 28 億美元、年增 23%；GMPD 營收 127 億，部門利潤 2.58 億，其中 1 億是不會重複的關稅退款。FY27 Q1 營收 675 億美元，非 GAAP 營業利益 10.01 億；Pharma、GMPD、Other 部門利潤分別是 7.83 億、0.33 億、1.93 億。TTM 毛利率 3.9%、營業利益率 1.26%。集中度：CVS 占 FY2026 營收 28%，前五大 43%，CVS 已以具約束力意向書延到 2032-06-30，但尚未定案。供需判斷是結構性持久：專科 Q1 年增 18%，學名藥量略高於長期目標。GLP-1 帶來約 500 基點營收，10-Q 稱對部門利潤沒有實質貢獻，IRA 標價調整扣掉約 400 基點，所以要看利潤，不能看營收。產業態勢屬雙向拉鋸：競爭面 10-K 只有一般性風險描述、未見具名新進者；結構面專科與學名藥專利到期有利；其他面關稅和 340B 政策仍未定。客戶別利潤、單價與量的結構化數字事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi6_fy2027_non_gaap_eps","f_peer_cah_gross_margin_pct","f_peer_cah_operating_margin_pct"],"verdict_values":{"revenue_quality":"配送屬經常性收入，近 12 個月續約涵蓋近三分之二企業營收，多數是長約；營收成長受 GLP-1 與 IRA 標價調整扭曲，品質要看部門利潤。","unit_econ_note":"每 100 美元營收約 3.9 美元毛利、1.26 美元營業利益（TTM）；Q1 毛利年增 12%、營業費用年增 9%，營業槓桿來自毛利結構。","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"三強寡占配送，低利益率、現金流充裕，管理層長期 EPS 年增目標 12–14%，需求受醫療剛性支撐"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：擴張期依據是專科單位需求與學名藥量，FY27 Q1 專科年增 18%、學名藥量略高於長期目標，未見供給過剩；來源為 2026-11-05 法說財務長發言與 FY2026 10-K。","bargaining":{"up":"品牌藥價格由藥廠決定，配送商靠服務費與採購量賺差價；學名藥端透過 Red Oak 與 CVS 合組採購，議價力較強。","down":"CVS 占營收 28%、前五大 43%，買方集中，續約時會要價；FY27 指引已納入 CVS 續約影響。","geo":"地理營收占比事實表未涵蓋；CEO 2025-07 稱約一成產品來自中國，關稅與供應商合規風險集中在 GMPD。"},"profit_pool_dir":"利潤往專科、學名藥採購和 Other 三個事業移動；FY27 Q1 Other 占三部門利潤 19%。五年歷史占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與五年營業利益池占比，無法展開；成長判斷改用分部利潤拆解。"}}}},"q2_moat":{"verdict":"穩定（→）：規模物流與 Red Oak 採購撐住三強寡占，CVS 續到 2032 年證明份額沒掉，但續約要讓利，營業利益率仍比 McKesson 低 41 基點，看不到護城河變寬。","reasoning":"機制是全國配送網加上聯合採購，單位成本低於小對手，客戶要換商得搬整個藥局或院所網絡，轉換多半只在合約到期時發生。投入資本事實表未涵蓋，無法算同業 ROIC 差距，方向改看最大客戶份額：CVS 服務範圍不變延長，搜尋未見第二供應商或自建配送，份額持平。留客有代價，2026-11-05 財務長 Aaron Alt 說 FY27 原始指引已納入續約影響。CAH 營業利益率由 FY2023 的 0.87% 升到 FY2026 的 1.25%，TTM 1.26% 仍低於 MCK 的 1.67%、COR 的 1.44%；對 MCK 的落差全來自營業費用率（2.64% 對 2.00%），原因是業務組合還是效率事實表未涵蓋。再投資報酬同樣因缺投入資本算不出，利潤率上升不等於增量報酬高。","fact_refs":["f_peer_cah_gross_margin_pct","f_peer_cah_operating_margin_pct","f_peer_cah_fcf_margin_pct","f_peer_mck_gross_margin_pct","f_peer_mck_operating_margin_pct","f_peer_mck_fcf_margin_pct","f_peer_cor_gross_margin_pct","f_peer_cor_operating_margin_pct","f_peer_cor_fcf_margin_pct","f_peer_hsic_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"全國配送規模加上 Red Oak 學名藥聯合採購，形成三強寡占與只在合約到期時才發生的轉換成本。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定偏強：近 12 個月續下近三分之二營收，Pharma 與 GMPD 各前兩大客戶都續約。定價面穩定：10-K 自述持續有定價壓力，續約影響已進指引，但 IRA 標價調整未傷利潤。兩面都沒有變寬的數字證據，份額與同業 ROIC 差距事實表未涵蓋，所以標穩定。","competitor_notes":[{"name":"MCK","strategy_note":"TTM 營業利益率 1.67%，三強最高，FCF 利潤率 1.64%；法說中分析師提到其往臨床試驗延伸，與 CAH 重押 MSO 和居家的路線不同。"},{"name":"COR","strategy_note":"毛利率 4.12% 三強最高，營業利益率 1.44%，但 TTM FCF 利潤率只有 0.47%，現金轉換三強最低。"},{"name":"HSIC","strategy_note":"毛利率 31.59%，遠高於藥品配送三強，產品結構不同，不列入同層對照。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營業利益率與 FCF 利潤率代替。","threats":[{"level":"🟡","text":"新商業模式、藥廠直配與新進者：10-K 列為風險，但未揭露份額或具名對手；2026-08-11 CEO Jason Hollar 也說配送模式會演變。","p":"15%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","channel_business_model_shift#0"]},{"level":"🟡","text":"客戶集中：CVS 占營收 28%、應收帳款毛額 22%，前五大 43%；CVS 2028 年分拆後議價主體會變。","p":"20%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"level":"🟡","text":"關稅進入藥品供應鏈：品牌藥關稅已公告，學名藥 2028 年 100%、2029 年 200% 的聲明若實施，會改變採購成本和學名藥供給。","p":"25%","evidence_refs":["reg_tariff_export#3","reg_tariff_export#4"]}],"roic_durability":{"quadrant":"低利益率×高周轉（周轉率未量化：投入資本與營運週轉天數事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是病人，決策者是處方醫師，付款者是保險和政府，三者都成立。用藥延後代價高，FY27 Q1 專科年增 18%，學名藥量略高於長期目標。藥要送到是不變的問題，目前解法是三強配送，短期沒有替代。GLP-1 需求 10-Q 自稱難預測，但對部門利潤本來就沒有實質貢獻。"},{"item":"決策層級","level":"🟡","text":"替代性要在整個連鎖或院所網絡的合約層級看。三家全國配送商都能接單，買方一次決定就能搬走大量營收；10-K 提到客戶整併可能從兩家留一家。代理讀數：CVS 合約延到 2032-06-30，近 12 個月續約近三分之二營收且多為長約。漲價後流失率與分客群續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"配送環節只拿 TTM 3.9% 毛利、1.26% 營業利益，上游藥廠定價、下游 CVS 占 28%，兩頭都強。IRA 標價調整扣營收約 400 基點，管理層稱對利潤沒有不利影響，報酬機制目前守得住。Red Oak 讓學名藥端有議價力，但合約 2029 年到期，尚未展延。"},{"item":"社會容忍度","level":"🟡","text":"藥價政治敏感，IRA、340B、OPPS 都在變動，CEO 2026-11-05 稱政策影響多在醫療服務提供端，對公司屬第二層影響。配送商整體利潤率約 1%，不是藥價爭議的主要目標，但持有 MSO 後直接暴露在給付政策和反回扣調查。CEO 沒有量化 340B 的量移轉。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。折舊、營運資金變動與投入資本都不在本包，只知 FY27 資本支出約 7 億美元、Solaris 約 19 億、Strive 與 AdaptHealth 糖尿病業務約 3.6 億，不足以計算，不推估，所以上界留空。共識對照改用拆解：三年 EPS 年化 12.5%，營收約 5.4%（FY1 到 FY2 為 6.1%），淨回購約 0.9 點，兩項合計 6.3–7.0 點，其餘 5.5–6.2 點要靠利潤率擴張、稅率和併購，其中併購不屬內生。共識是否超過內生上界無法確認，所以情境保守處理：Base 年化 9.9%，低於共識；Bear 機率 30%，理由之一就是這個缺口。"}}}},"q3_growth":{"verdict":"中等（🟡）：核心配送沒有滲透空間，五年後要靠專科、MSO 和 Other 接棒；曲線已在長，但 TAM、滲透率與併購報酬都沒有數字可驗。","reasoning":"FY27 指引 EPS 年增 17–19%（基期 10.95），Pharma 部門利潤年增 10–12%，其中已宣布併購貢獻 2–3 點（2026-08-11 財務長 Aaron Alt），其餘主要來自專科與學名藥的量。共識三年 EPS 年化 12.5%（10.95 到 FY2029E 15.61，若用含退款的 11.26 為 11.5%），但 FY1 共識 12.56 是財報前快照，已低於指引下緣 12.80。內生上界因投入資本缺資料算不出，缺口改用拆解：營收共識 FY1 到 FY2 年增 6.1%，淨回購約 0.9 點（年回購 10 億美元扣 SBC 後除以市值），其餘約 5 點要靠利潤率擴張、稅率和併購，主因歸在利潤率擴張。第二曲線證據：專科 Q1 年增 18%，Other FY27 利潤指引上調到 17–20%，Theranostics 近 30%、PET 逾 20%（2026-08-11 CEO Jason Hollar），MSO 市場仍分散。若 Other 占三部門利潤升破 25% 且併購有報酬數字，才升為寬。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_fy2027_non_gaap_eps"],"verdict_values":{"growth":{"driver_mix":"量（專科與學名藥單位）為主，併購次之，回購淨貢獻約 0.9 點，藥價幾乎沒有貢獻。","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊與營運資金變動事實表未涵蓋，內生上界無法計算；改以營收、淨回購和利潤率拆解共識成長。","segments":[{"item":"Pharma","value":"FY2026 營收 2,348 億美元（+15%），部門利潤 28 億（+23%）；FY27 Q1 營收 626 億（+6%），利潤 7.83 億（+17%）；FY27 指引營收 +3–5%、利潤 +10–12%。"},{"item":"GMPD","value":"FY2026 營收 127 億（+1%），部門利潤 2.58 億，扣 1 億退款約 1.58 億；FY27 Q1 利潤 0.33 億；FY27 指引 2.0–2.2 億，管理層稱偏向下緣。"},{"item":"Other","value":"FY27 Q1 營收 18 億（+7%），利潤 1.93 億（+16%）；FY27 指引營收 +12–14%、利潤 +17–20%；占三部門利潤 19%。"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q1 毛利年增 12%，快於營收 5%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"未見流失；市占數字事實表未涵蓋"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"配送商不主導藥價，不適用"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 點","lit":true,"note":"共識三年 EPS 12.5% 對營收約 5.4%，差約 7 點"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY2025 1.19 倍、FY2026 2.64 倍"},{"item":"SBC／營收逾 5% 且上升","lit":false,"note":"Q1 約 0.16%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"10-K 未點名替代技術"},{"item":"產業倍數近 3 年系統性下移","lit":false,"note":"本檔倍數上移；同業倍數事實表未涵蓋"},{"item":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"FY27 資本支出約 7 億美元，約為調整後自由現金流指引的兩成，且未區分維護性"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"St. Louis、Sacramento 新設施在建"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金創造強、回饋穩定；三項資本配置檢查只有股權稀釋確定過關，併購和回購報酬缺資料，暫列中等。","reasoning":"FY2026 FCF 45.25 億美元，是 GAAP 淨利 17.14 億的 2.64 倍；FY2025 為 18.5 億、1.19 倍，兩年落差大，事實表未拆原因，FY27 調整後自由現金流指引 35–40 億較能代表常態。Q1 營業現金流 13.98 億，資本支出 1.57 億，回購 5 億，股息約 1.25 億。SBC 占非 GAAP 營業利益 10.9%，年化約 4.4 億美元，占營收 0.16%，占市值約 0.7%。董事會新增 50 億美元回購授權，FY27 至少回購 10 億。近三年現金四分去向、債務到期與回購均價事實表未涵蓋。","fact_refs":["f_kpi3_non_gaap_eps","f_kpi4_1_398_157","f_kpi5_sbc_non_gaap","f_shares_diluted_m","f_net_debt_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Solaris 約 19 億美元、Strive 與 AdaptHealth 糖尿病業務約 3.6 億美元；2026-11-05 財務長稱 Solaris 結果至少符合商業計畫，但增量利潤與投入資本數字事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"FY2026 回購 13.5 億美元，FY27 Q1 加速回購 5 億；均價與 10 年期殖利率事實表未涵蓋。以現價算盈餘收益率約 4.7%（指引中值 12.90 除以 271.72）。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q1 SBC 占非 GAAP 營業利益 10.9%，約 1.09 億美元，年化 4.4 億，除以市值 628 億約 0.7%，低於每年 1.5%；FY27 稀釋股數指引 231–232 百萬股，低於 Q1 的 233 百萬股。"}]},"governance":{"capital_returns":[{"item":"FY2026 回購","value":"13.5 億美元"},{"item":"FY27 Q1 回購","value":"5 億美元加速回購"},{"item":"FY27 回購承諾","value":"至少 10 億美元，董事會新增授權 50 億美元"},{"item":"FY27 Q1 股息","value":"約 1.25 億美元"},{"item":"FY27 資本支出","value":"約 7 億美元"},{"item":"近年併購","value":"Solaris 約 19 億美元（約 75% 股權，宣布於 2025-08）；Strive 與 AdaptHealth 糖尿病業務約 3.6 億美元"}]}}},"q5_valuation":{"verdict":"現價要求五年 EPS 年增約 12.8% 且終端仍有 18 倍，或倍數一直維持 21 倍；前者等於公司五年都達成 12–14% 目標，我只信到約 10%，所以不追。","reasoning":"以年化 10% 報酬反推：股息 0.76% 之外股價要年增 9.2%，五年後約 423 美元。終端 18 倍需要 EPS 23.5 美元，較指引中值 12.90 年增 12.8%；維持 21 倍則只需年增 9.2%。Base 假設 EPS 年增 9.9%、終端 18 倍，股價年化約 6.5%，加股息約 7.2%，屬弱區；EPS 路徑已含回購，報酬不應再加一次。股價比前份判斷上漲 35%，用 8 月財報前共識 12.05 近似前份當時分母，盈餘預期上修只有約 7%，其餘是倍數由約 17 倍升到 21 倍。PEG 1.72（Fwd P/E 21.63 除以三年 EPS 年化 12.55%）。共識 12.56 是財報前快照，改用指引中值的倍數是 21.06 倍。五年分位與同業倍數事實表未涵蓋，只能對照本檔自身。RSI 資料標為不可用，四週漲幅未提供，動能是否過熱不做判斷。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_kpi6_fy2027_non_gaap_eps","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_dividend_yield_ttm","f_ma_state"],"verdict_values":{"valuation":{"basis":"Fwd P/E 與 PEG，起點用 FY2027 指引中值 12.90","tier":"藥品配送三強","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不得自行補值；終端倍數只能對照本檔現值與前份當時倍數。"},"fwd_pe":21.63,"peg":1.72,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"21 倍對 PEG 1.72 本身不算離譜，偏貴來自三點：Base 年化約 7%，低於 8%；上下檔比約 1.8 倍，低於 2；半年內倍數升約 26%，盈餘只上修約 7%。","upside_short_pct":5.3,"upside_mid_pct":10.8,"denominator_disputed":false,"denominator_note":"起點分母已改用指引中值，基期排除 FY2026 一次性關稅退款 0.31 美元。Trailing GAAP 分母波動極大（FY2023 EPS 1.00、FY2026 7.23），4 個年度端點的分位不採用。非 GAAP 與 GAAP 的差距仍大（FY27 Q1 營業利益 10.01 億對 7.53 億），列入反證。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是倍數：若續約讓利和併購風險都比想的輕，21 倍撐得住，等回檔就會錯過；反過來 Red Oak 或 CVS 出事，下跌會超過本次假設區間。","reasoning":"反證與裁定見反證紀錄，這裡只補敏感度：Pharma 部門利潤率每少 5 基點，以 FY2032 營收約 3,430 億美元、稅率 19%、約 220 百萬股估算，EPS 少約 0.63 美元，約占 Base 終端 EPS 3%，以 18 倍計股價少約 11 美元。歷史最大回撤與空方數字事實表未涵蓋。法說問答中管理層未量化的項目包括 340B 與 OPPS 的量移轉、超額需求與強勁需求的差距、學名藥專利到期對利潤的貢獻。","fact_refs":["f_week26_return_pct","f_ma_w52","f_ma_w104","f_price_at_dd","f_rev_consensus_fy2_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱風險低至中：十項衰退信號亮一項，共識 EPS 年增比營收快約 7 點"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":12.9,"pe":21.06,"basis":"FY1 口徑：FY2027（2027-06 止）公司指引中值 12.90，終端倍數同為當年度前瞻口徑；共識 12.56 是財報前快照，已低於指引下緣。"},"eps":{"bull":[14.8,16.9,19.2,21.7,24.4],"base":[14.3,15.85,17.45,19.05,20.65],"bear":[13.0,13.2,13.4,13.7,14.0]},"pe":{"bull":21,"base":18,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.76,"net_buyback":0.9},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-45,"hi":-30,"basis":"現價 271.72 美元。回到前份價位 200.68 跌 26%，到 104 週均線 180.24 跌 34%，FY27 指引中值 12 倍約 155 美元跌 43%；取 −30% 到 −45%，下緣涵蓋 Bear 終點跌幅 33%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"FY2032 EPS 24.40，年化 13.6%：達成管理層 12–14% 長期目標，2029 年起專利到期潮放大學名藥利潤，Other 與專科維持雙位數；終端 21 倍等於維持現有倍數。","base":"FY2032 EPS 20.65，年化 9.9%：低於管理層目標，反映續約讓利和基期變高；終端 18 倍介於前份當時約 17 倍與現價 21 倍之間。同業現值倍數事實表未涵蓋，只能對照本檔自身。","bear":"FY2032 EPS 14.00，年化 1.7%：Red Oak 或大客戶條款變差、關稅難轉嫁，成長降到低個位數，終端 13 倍。機率 30%：內生上界算不出、共識靠利潤率擴張，且管理層已預告 Q2、Q3 放緩；CVS 鎖到 2032 年是不再調高的原因。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CVS 占營收 28%、前五大 43%，10-K 稱客戶整併可能從兩家供應商只留一家；Red Oak 是獨立合約，CEO 2026-11-05 說還有工作要做；CVS 2028 年分拆。","assumption":"分拆後的 CVS 零售仍把配送和學名藥採購都留給 Cardinal。","consequence":"五年虧 50% 最可能的路徑：Red Oak 破局，Pharma 部門利潤率跌破 1.0%，EPS 停在 13–14 美元，倍數掉到 10–11 倍，股價落在 130–155 美元。","ruling":"反駁但保留：CVS 剛以具約束力意向書延到 2032 年，短期不太可能發生；與 Single Thing 同一路徑，不另立。","watch":"CVS 正式合約、Red Oak 展延公告。","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","competitive_share_entrants#0"],"fact_refs":["f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"專科靠 MSO 併購：Solaris 約 19 億美元，CEO 說還會再整併，司法部的反回扣調查正是針對 MSO 和 GPO 的交易；FY27 Q1 非 GAAP 與 GAAP 營業利益差 2.48 億美元，占非 GAAP 約 25%。","assumption":"併購報酬高於資金成本，非 GAAP 排除項不會常態化。","consequence":"EPS 達標，但現金被併購吃掉，GAAP 盈餘追不上，市場給的倍數下移。","ruling":"採納為觀察項：報酬數字揭露前，併購不計入護城河加分。","watch":"併購金額、增量利潤揭露、GAAP 對非 GAAP 比率、司法部調查進度。","evidence_refs":["regulatory_antitrust#0"],"fact_refs":["f_kpi1_non_gaap","f_kpi2_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"GMPD 持續承受替代關稅成本且調價未完全抵銷；品牌藥關稅已公告，學名藥 2028 年起的關稅聲明仍不確定；OPPS 的 340B 給付規則 2026-11-04 晚間定案，CEO 說現在預測量的移轉還太早。","assumption":"成本能轉嫁，流出醫院的量會按市占回到公司的其他通路。","consequence":"營收成長維持，但利潤率被關稅或給付變動侵蝕。","ruling":"不採信也不否定，標為未證、監測。OPPS 規則不足一季，尚未看到反映在賣方模型的證據，首個財報數據出來前不加碼。","watch":"FY27 Q2 Pharma 部門利潤率與醫院客戶量；GMPD 全年利潤是否低於 2.0 億美元。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4"],"fact_refs":["f_kpi6_fy2027_non_gaap_eps"]},{"view":"價格已反映太多","evidence":"26 週上漲 48.6%，現價比 52 週均線 219 美元高 24%，倍數半年內由約 17 倍升到 21 倍；8 月平均目標價 253 美元、最高 275 美元，現價高於平均，但目標價是財報前資料。","assumption":"21 倍的定價要公司五年都達成 12–14% 目標。","consequence":"任何一季放緩都可能讓倍數回到 18 倍，股價約 232 美元，跌 15%。","ruling":"採納，這是本次不追的主因；管理層已預告 Q2、Q3 放緩。","watch":"FY27 Q2、Q3 Pharma 部門利潤年增率與財報後賣方上修幅度。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_ma_w52","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 200.68 → 本次 271.72（+35.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=200.68","side_b":"本次 price_at_dd=271.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 200.68 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 200.68 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 200.68 美元：Bull 價 512.4、Bear 價 182，五年期望值 +70.9%，基準年化 13.1%，不對稱比 11.12","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 11.12。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 200.68 美元：五年期望值 +70.9%，基準年化 13.1%，不對稱比 11.12","side_b":"本次情境、股價 271.72 美元：五年期望值 +26.2%，基準年化 6.5%，不對稱比 1.79","ruling":"再換股價、情境不動：起點價上漲 35.4%，五年期望值少 44.7 個百分點，基準年化少 6.7 個百分點，不對稱比由 11.12 降到 1.79。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"續約是護城河證明還是讓利","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO Jason Hollar：近 12 個月續約涵蓋近三分之二企業營收，CVS 延到 2032 年。","side_b":"2026-11-05 CFO Aaron Alt：FY27 原始利潤指引已大致納入 CVS 續約影響，Q2、Q3 放緩部分來自續約時點。","ruling":"可調和，差別在程度：客戶留下來了，價格也讓了一些。護城河判穩定，不判變寬。管理層的時點解釋未證，列入監測。","evidence_level":"公司法說，尚無逐客戶利潤數字","settle_metric":"FY27 Q2、Q3、Q4 Pharma 部門利潤年增率","if_then":["若 Q2、Q3 連兩季低於 6%，減碼一半","若 Q4 未回到 12% 以上，時點解釋不成立，停止加碼","若 Q4 回到 12% 以上，時點解釋成立，維持原判斷"],"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"axis":"學名藥量的說法三個月內轉強","cause":null,"prior_field":null,"side_a":"2026-08-11 CEO Jason Hollar：FY27 學名藥量成長仍未到 2–3% 區間。","side_b":"2026-11-05 CFO Aaron Alt：學名藥量成長略高於長期目標。","ruling":"可調和但要看持續性：只有一季，FY27 指引以強勁需求延續為前提。2029 年起專利到期潮是第二個支撐，要到 FY29 才能驗證。","evidence_level":"公司法說","settle_metric":"FY27 Q2、Q3 法說對學名藥量的描述與 Pharma 部門利潤","if_then":["若下兩季學名藥量回到長期目標以下且 Pharma 利潤指引未上修，停止加碼"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"共識 12.56 還沒更新，指引下緣 12.80 已高於共識；Q1 EPS 超預期約 11%，Pharma 利潤指引上修；CVS 鎖到 2032 年，2029 年起專利到期潮有利學名藥。","side_b":"指引中值計 21 倍，Base 年化約 7%，上下檔比約 1.8 倍；半年倍數升約 26%，管理層又預告 Q2、Q3 放緩。","ruling":"可調和，好生意與好價格是兩件事。限制條件只有價格，不追現價，232 美元以下才買。","evidence_level":"事實表與公司法說","settle_metric":"收盤價與 FY28 EPS 指引中值","if_then":["若股價續漲而 Pharma 部門利潤尚未驗證，不追","若股價跌到 232 美元以下且基本面門檻未觸發，分批反買，先買三分之一","反向條件：若 2027-08 FY28 EPS 指引中值 ≥14.2 美元且 Q4 Pharma 部門利潤年增 ≥12%，進場價上移到 256 美元後分批反買"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"歷史分位互相衝突","cause":null,"prior_field":null,"side_a":"Trailing P/E 在 4 個年度端點的分位 15.4，看起來便宜。","side_b":"P/S 與 EV/S 分位 100，看起來最貴。","ruling":"兩邊都不採用。4 個點不是五年分位，FY2023 GAAP EPS 只有 1.00，把過去的本益比墊高；營收分母又受 GLP-1 與 IRA 標價影響。","evidence_level":"程式計算，樣本 4 點","settle_metric":"連續五年前瞻本益比序列，事實表未涵蓋","if_then":["取得連續序列前，不以分位作為買賣依據"],"evidence_refs":[]},{"axis":"併購成長的增量報酬","cause":null,"prior_field":null,"side_a":"2026-11-05 CFO Aaron Alt：Solaris 結果至少符合商業計畫；CEO Jason Hollar 稱 MSO 還有整併機會。","side_b":"併購後增量利潤與投入資本都未揭露，增量報酬算不出來。","ruling":"不可裁決，要等公司揭露併購後增量利潤或事實表補齊投入資本。在此之前併購不列入護城河加分，長期信心上限為中。","evidence_level":"管理層說法，無數字","settle_metric":"併購投入金額與併購後部門利潤增量","if_then":["若 FY28 有機 Pharma 部門利潤年增低於 7% 且併購支出續增，停止加碼"],"evidence_refs":["ma_merger#0"]},{"axis":"前份漂移：股價帶動的估值變化","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 200.68 美元，估值中性，訊號評級 B。","side_b":"本次股價 271.72 美元，上漲 35%，倍數由約 17 倍升到 21 倍，估值轉為偏貴，訊號評級維持 B。","ruling":"漲幅中盈餘上修只占約 7%，主因是倍數擴張；評級不因上漲調升，也因基本面轉強而不調降。","evidence_level":"事實表","settle_metric":"股價除以 FY27 指引中值","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價值陷阱判斷","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱判斷為🟢。","side_b":"本次為🟡：共識 EPS 年增比營收快約 7 點，衰退信號亮一項。","ruling":"差距來自利潤率與稅率，指引上修的 0.40 美元中約 0.08 美元來自稅率下調 0.5 點；不是生意變差，但成長品質需要多打折。","evidence_level":"事實表與公司法說","settle_metric":"EPS 與營收成長差距、Pharma 部門利潤率","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：前份未填欄位本次首度填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空。","side_b":"本次首度填入：護城河方向穩定、五年後跑道中等、類型為品質複利成長、中循環、最大回撤 −30% 到 −45%、機率 20／50／30；裁決與角色由程式產生。","ruling":"屬格式與方法補齊，不代表基本面變動。各欄依據不同：護城河方向看續約與利潤率，五年後跑道看專科、MSO 和 Other 的接棒，類型與循環位置看三強寡占結構和專科、學名藥需求，最大回撤和機率是本次情境假設；前份沒有值，無從比較變動幅度。","evidence_level":"判斷輸出","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻：清倉、減碼與重新進場條件","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份未設清倉、減碼門檻與重新進場條件（欄位為空）。","side_b":"清倉：Red Oak 到期前未展延；減碼：Pharma 部門利潤年增率連兩季 <6% 或利潤率連兩季 <1.15%；重新進場：收盤 ≤232 美元且基本面門檻未觸發。","ruling":"新設門檻，232 美元約為 FY27 指引中值 18 倍，在此價位 Base 年化約 10.8%、上下檔比約 3.7 倍。","evidence_level":"本次情境推算","settle_metric":"收盤價、Pharma 部門利潤年增率與利潤率","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（欄位為空）。","side_b":"Single Thing：Red Oak 合資在 2029 年到期前未能展延，或 CVS 2028 年分拆時條款被實質縮減。","ruling":"CVS 配送合約已有具約束力意向書，Red Oak 是剩下未決的最大單一事件；具體利潤占比事實表未涵蓋。","evidence_level":"公司法說","settle_metric":"Red Oak 展延公告","if_then":["若終止，清倉","若條款實質縮減，減碼一半"],"evidence_refs":["customer_second_source#1"]},{"axis":"R1 門檻：由營收改看利潤（減碼條件）","cause":"新證據","prior_field":["R1"],"side_a":"季度 Pharma 營收 YoY 跌破 5%（暗示大客戶流失，已知 baseline ~9%）","side_b":"FY27 Q2、Q3 Pharma 部門利潤年增率連兩季 <6% 則減碼一半。","ruling":"舊門檻已失效：公司 FY27 指引就是營收年增 3–5%，IRA 標價調整扣掉約 400 基點，營收低於 5% 不代表客戶流失，改看利潤。","evidence_level":"公司法說與 FY27 指引","settle_metric":"Pharma 部門利潤年增率","if_then":[],"evidence_refs":["customer_second_source#0"]},{"axis":"R2 與 H2 門檻：利潤率基準修正（減碼條件）","cause":"方法變動","prior_field":["R2","H2"],"side_a":"連兩季 ≤ 1.35%（FY25 = 1.42%，跌 5bp 即削弱 H2）","side_b":"Pharma 部門利潤率連兩季 <1.15% 則減碼一半（FY27 Q1 1.25%，FY26 約 1.19%）。","ruling":"前份 1.42% 的基準對不上本次資料：以 FY2026 10-K 營收 2,348 億、年增 15%，利潤 28 億、年增 23% 回推，FY25 約 1.1%，FY26 約 1.19%，都低於 1.35%。照用舊門檻等於一直處於警戒，屬基準問題，不是利潤率惡化；前份口徑本包無法查證。","evidence_level":"10-K 數字回推，營收與利潤皆為四捨五入值","settle_metric":"Pharma 部門利潤率","if_then":[],"evidence_refs":[]},{"axis":"H1 與 R3 門檻：專科的驗證方式","cause":"方法變動","prior_field":["H1","R3"],"side_a":"FY28 Specialty OI 占比 ≥ 22%；Specialty 營收 YoY ≥ 18%；2027-2028 期間 Specialty 整體 YoY 連 4 季","side_b":"專科營收年增連 4 季 <10% 則削弱並停止加碼；專科營業利益占比維持為資料缺口。","ruling":"專科營業利益占比本包沒有揭露，保留指標但標資料缺口。營收年增門檻由 18% 降到 10%，依據是公司 FY27 指引的雙位數，且 Solaris 在 Q2 滿週年後基期變高。GLP-1 與生物相似藥的舊風險退休，因 10-Q 已說 GLP-1 對部門利潤沒有實質貢獻。","evidence_level":"公司法說與 10-Q","settle_metric":"專科營收年增率","if_then":[],"evidence_refs":[]},{"axis":"H3 門檻：客戶占比","cause":"新證據","prior_field":["H3"],"side_a":"Top 10 客戶占比 ≥ 60%（穩定）；FY25 10-K 揭露 5 大客戶占比 50%+","side_b":"前五大客戶營收占比 ≥40%（FY2026 43%）；CVS 服務範圍不變；Red Oak 到期前展延。","ruling":"前十大占比本包沒有，保留為資料缺口，改用 10-K 有揭露的前五大。前份的 50% 以上與 FY2026 的 43% 差距，本包無法判斷是客戶結構變動還是口徑不同。","evidence_level":"FY2026 10-K","settle_metric":"10-K 前五大客戶營收占比","if_then":[],"evidence_refs":["customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"FY27 Q2、Q3 Pharma 部門利潤年增率連兩季低於 6%，判定續約讓利超過預期。","type":"假設驗證","maps_to":"H1","metric":"Pharma 部門利潤年增率","threshold":"連兩季 <6%","action":"減碼一半並停止加碼","source_freq":"季報／每季","date":"2027-05","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":2,"text":"關稅成本吸收失敗：GMPD 全年利潤低於指引下緣，或學名藥關稅實施後 Pharma 利潤率跌破門檻。","type":"風險","maps_to":"R2","metric":"GMPD 部門利潤、Pharma 部門利潤率","threshold":"GMPD FY27 <2.0 億美元；或 Pharma 部門利潤率連兩季 <1.15%","action":"停止加碼；兩條同時成立則減碼一半","source_freq":"季報／每季","date":"2027-08","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4"]},{"n":3,"text":"Red Oak 未展延，或 CVS 分拆時條款被實質縮減。","type":"Single Thing","maps_to":"Single Thing","metric":"Red Oak 合約狀態","threshold":"2029 年到期前未展延，或條款實質縮減","action":"終止則清倉，縮減則減碼一半","source_freq":"法說與 8-K／不定期","date":"2029","evidence_refs":["customer_second_source#0"]},{"n":4,"text":"股價回到 232 美元以下，約 FY27 指引中值 18 倍，且基本面門檻未觸發。","type":"估值rearm","maps_to":"H1","metric":"收盤價與 Pharma 部門利潤年增率","threshold":"收盤 ≤232 美元，且第 1 條未觸發","action":"分批反買，先買三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"FY27 Q4 財報確認放緩只是時點，且 FY28 指引 EPS 年增不低於 10%。","type":"加碼","maps_to":"H1","metric":"FY27 Q4 Pharma 部門利潤年增率、FY28 EPS 指引中值","threshold":"Q4 ≥12% 且 FY28 指引中值 ≥14.2 美元","action":"進場價上移到 256 美元後分批反買","source_freq":"2027-08 財報","date":"2027-08","evidence_refs":[]},{"n":6,"text":"股價達 FY27 指引中值 25 倍而利潤指引未同步上修，已持有者減碼。","type":"減碼","maps_to":"H1","metric":"收盤價除以 FY27 指引中值","threshold":"收盤 ≥322 美元且 Pharma 利潤成長指引未上修","action":"減碼三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":7,"text":"司法部反回扣調查轉為正式提告或刑事程序；IVC 訴訟出現超出應計金額的不利和解。程序目前為民事調查，受影響營收事實表未涵蓋，無解決日期。","type":"清倉","maps_to":"R4","metric":"司法部調查程序狀態、和解金額","threshold":"轉刑事；民事提告或和解逾 5 億美元則減碼","action":"轉刑事清倉，民事不利和解減碼一半","source_freq":"10-Q 與 8-K／每季","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"GMPD 再出現涉及主要產品的 FDA 警告信或全國召回，代表供應商合規問題未解決。","type":"風險","maps_to":"R5","metric":"FDA 警告信與全國召回件數","threshold":"12 個月內再發生 1 起","action":"停止加碼","source_freq":"FDA 公告與 10-Q／不定期","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","major_events#3","product_recall_warning#0"]},{"n":9,"text":"FY27 Q2 財報後複審第 1 條門檻。","type":"複審日期","maps_to":"H1","metric":"FY27 Q2 Pharma 部門利潤年增率","threshold":"2027 年 2 月財報發布","action":"若未觸發門檻且股價高於 232 美元，維持不追","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"Pharma 部門利潤年增率","bear_threshold":"FY27 Q2、Q3 連兩季 <6%，減碼一半","window":"FY27 Q2–Q3","source":"公司季報新聞稿","last_status":"ok"},{"metric":"Pharma 部門利潤率（部門利潤除以部門營收）","bear_threshold":"連兩季 <1.15%，減碼一半（FY27 Q1 1.25%）","window":"每季滾動","source":"公司季報新聞稿","last_status":"ok"},{"metric":"GMPD 部門利潤","bear_threshold":"FY27 全年 <2.0 億美元，停止加碼","window":"FY27 全年","source":"公司季報；2026-11-05 財務長稱已往指引下緣靠近","last_status":"warning"},{"metric":"調整後自由現金流","bear_threshold":"FY27 <35 億美元，停止加碼","window":"FY27 全年","source":"公司季報與法說","last_status":"ok"},{"metric":"Red Oak 合資展延","bear_threshold":"2029 年到期前未展延則清倉；條款實質縮減則減碼一半","window":"至 2029 年","source":"法說、8-K","last_status":"unknown"},{"metric":"CVS 配送協議定案","bear_threshold":"2027-06-30 前未轉成正式合約，停止加碼","window":"至 2027-06-30","source":"8-K、10-Q","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"收盤價≤232美元（約FY27指引中值18倍），且FY27 Q2、Q3 Pharma部門利潤年增率未連兩季低於6%","exec_line":"不追現價；收盤 ≤232 美元且基本面門檻未觸發時分批買進，先買三分之一，下一季財報確認後補足。已持有者續抱不加碼，收盤 ≥322 美元且利潤指引未上修時減碼三分之一。","holding_cap":null},"evidence_dismissed":[{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"對照共識 12.5% 的部分已補進此欄的公式說明。不採納的只有要算出增量 ROIC、再投資率和內生上界這一半：審查把缺資料讀成漏算，但這三個數都要用投入資本、折舊與營運資金變動，事實表都沒有。資本支出和併購金額只是再投資的一部分，據此填數字就是編造，所以維持無資料的寫法。"},{"ref":"$.counter_evidence.contradictions","reason":"供需持久性的負向發現是審查拿到的資料沒有列出，不是判斷漏接，審查自己也查無漏接。業務段的結構性持久以專科年增 18%、學名藥量略高於長期目標為據，續約與關稅的下行已寫進 Bear 情境。這輪看不到該軸的原始發現，硬加一條矛盾沒有根據，所以不新增。"},{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"這個欄位問的是買進論點有沒有靠市場看錯，審查把它讀成必須寫出市場錯在哪。本判斷不主張現價買進，232 美元是等價格，不是等市場認錯，所以這欄維持否。現價隱含 EPS 年增約 12.8%、我只信到約 10% 的落差已寫在估值段，等待條件也具體可驗，不必另立市場看錯的理由。"}]},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等收盤價回到 232 美元以下（約 FY27 指引中值 18 倍），且 FY27 Q2、Q3 Pharma 部門利潤年增率未連兩季低於 6%；或 2027-08 財報確認 FY28 指引中值不低於 14.2 美元後，進場價上移到該指引的 18 倍。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"Pharma 部門利潤成長能吸收 CVS 等大客戶續約讓利，靠專科與學名藥量維持高於 9% 的年增","2y":"FY27 年增 10–12%，FY28 不低於 9%","5y":null,"10y":null,"threshold":"FY27 全年 Pharma 部門利潤年增 ≥10%；FY28 ≥9%；部門利潤率維持在 1.15% 以上（FY27 Q1 1.25%，FY26 約 1.19%）","source":"公司季報新聞稿、法說與 10-K","drift_rule":"TTM 偏離門檻 ≥5% 連 2 季削弱，≥10% 連 3 季反轉"},{"id":"H2","text":"Other 三個事業與專科接棒成為第二成長曲線，五年後降低對傳統配送的依賴","2y":null,"5y":"Other 占三部門利潤由 19% 升到 25% 以上，專科營收維持雙位數年增","10y":null,"threshold":"FY2031 Other 占三部門利潤 ≥25%；專科營收年增 ≥10%；專科營業利益占比為資料缺口，待公司揭露","source":"10-K 與 10-Q 分部揭露、法說","drift_rule":"TTM 偏離門檻 ≥5% 連 4 季削弱，≥10% 連 6 季反轉"},{"id":"H3","text":"CVS 與 Red Oak 的關係穿越 2028 年 CVS 分拆與 2029 年合資到期，合約基礎不變","2y":null,"5y":"CVS 正式合約持續至 2032-06-30，Red Oak 展延到 2029 年之後","10y":null,"threshold":"前五大客戶營收占比 ≥40%（FY2026 43%）；CVS 服務範圍不變；Red Oak 於 2029 年到期前完成展延","source":"10-K、8-K 與法說","drift_rule":"CVS 正式合約未在 2027-06-30 前完成視同削弱；Red Oak 未展延或條款實質縮減即反轉"},{"id":"H4","text":"GMPD 改善計畫把部門利潤拉回，關稅與品質問題不再拖累","2y":"FY27 部門利潤 2.0–2.2 億美元，FY28 高於 FY27","5y":null,"10y":null,"threshold":"FY27 ≥2.0 億美元（FY2026 扣退款約 1.58 億）；FY28 年增為正","source":"公司季報與法說","drift_rule":"TTM 偏離門檻 ≥5% 連 2 季削弱，≥10% 連 3 季反轉"}],"R":[{"id":"R1","text":"續約讓利比指引假設更重，Q2、Q3 放緩不只是時點；CFO Aaron Alt 2026-11-05 的時點解釋未證","h_ref":"H1","clock":"⚡","threshold":"FY27 Q2、Q3 Pharma 部門利潤年增率連兩季 <6% 則減碼；Q4 未回到 12% 以上，時點解釋視為不成立","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"id":"R2","text":"關稅與成本轉嫁失敗：GMPD 的替代關稅、品牌藥關稅與學名藥 2028 年起 100% 的聲明","h_ref":"H1","clock":"🔥","threshold":"GMPD FY27 部門利潤 <2.0 億美元；或學名藥關稅實施後 Pharma 部門利潤率連兩季 <1.15%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4"]},{"id":"R3","text":"新商業模式、藥廠直配或新進者削弱配送環節分潤；CEO Jason Hollar 2026-08-11 說配送模式會演變，2026-11-05 改為強調核心配送耐久，兩次都沒給量化指標","h_ref":"H3","clock":"🐢","threshold":"TTM 營業利益率對 MCK 的差距擴大到 60 基點以上（現 41 基點），或前五大客戶占比跌破 40%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","channel_business_model_shift#0"]},{"id":"R4","text":"法律與監管：司法部 2023-11 起的反回扣民事調查涉及 MSO 與 GPO 少數股權交易，IVC 濾器訴訟續辯（應計 2,900 萬美元）","h_ref":"H2","clock":"🐢","threshold":"轉刑事則清倉；民事提告或和解逾 5 億美元則減碼；受影響營收事實表未涵蓋","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"id":"R5","text":"GMPD 品質與供應商合規：中國代工針筒的 FDA 警告信、酒精棉片召回，可能迫使營運調整","h_ref":"H4","clock":"🔥","threshold":"12 個月內再出現涉及 GMPD 主要產品的 FDA 警告信或全國召回，停止加碼","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","major_events#3","product_recall_warning#0"]},{"id":"R6","text":"MSO 併購撐成長但報酬不明，整合失誤或高價收購會吃掉現金","h_ref":"H2","clock":"🔥","threshold":"FY28 起有機 Pharma 部門利潤年增 <7% 且併購支出續增，或單筆併購逾市值 5% 且未揭露報酬目標","evidence_refs":["ma_merger#0"]}],"single_thing":{"description":"Red Oak 合資在 2029 年到期前未能展延，或 CVS 2028 年分拆時條款被實質縮減。","why_fatal":"財務長 2026-08-11 說學名藥轉換的獲利較佳，Red Oak 是學名藥採購規模的來源；CVS 配送已鎖到 2032 年，剩下未決的最大單一事件就是這份獨立合約。學名藥利潤占比事實表未涵蓋，無法給精確金額，CVS 占營收 28% 只能當影響範圍參考。","if_happens":"採購成本優勢縮水，Pharma 部門利潤率下滑，Base EPS 路徑失效。合資終止則清倉，條款實質縮減則減碼一半並重算情境。","how_monitor":"每季法說與 8-K。CEO 2026-11-05 說會相對很快處理這份合約，若 2028-06 前仍無展延公告，列為警訊。","probability":"12–24 個月內約 5–10%"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.33,"peg_fy2":1.54,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":10.95,"FY2027E":12.56,"FY2028E":14.06,"FY2029E":15.61},"fy_end_month":6,"eps_basis":"非 GAAP 稀釋 EPS；FY2026A 用排除一次性關稅退款後的 10.95（公告值 11.26）；FY2027E–FY2029E 為 2026-11-07 Koyfin 共識，FY2027E 是財報前快照，已低於公司新指引 12.80–13.00；EPS 預估家數事實表未涵蓋。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 Q2 財報（月份依往年推估）","impact":"高","watch":"Pharma 部門利潤年增率是否低於 6%"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"AdaptHealth 糖尿病業務交割，管理層只說在跨年之後","impact":"低","watch":"整合進度與 Other 利潤"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 Q3 財報（月份依往年推估）","impact":"高","watch":"連兩季門檻是否成立"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與 FY28 指引","impact":"高","watch":"Q4 Pharma 部門利潤年增是否回到 12% 以上，FY28 EPS 指引中值是否達 14.2 美元"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"St. Louis 3PL 與冷鏈設施預計 2027 年底前營運","impact":"低","watch":"BioPharma Solutions 產能與新合約"},{"date":null,"date_precision":null,"type":"other","event":"CVS 2028 年分拆，法說未給月份","impact":"高","watch":"分拆後配送與 Red Oak 條款是否變動"},{"date":null,"date_precision":null,"type":"regulatory","event":"學名藥 2028 年起 100% 關稅的聲明，實施仍不確定","impact":"高","watch":"正式公告內容與 Pharma 部門利潤率"},{"date":null,"date_precision":null,"type":"other","event":"Red Oak 合資 2029 年到期前的展延","impact":"高","watch":"展延公告與條款"}],"decision_out":{"role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=48.62, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
