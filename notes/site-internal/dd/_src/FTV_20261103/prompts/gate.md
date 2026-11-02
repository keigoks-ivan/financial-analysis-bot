你是 DD 管線 v20 的判斷層閘（gate），標的 FTV（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1107.5 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi1_revenue_intelligent_oper`（q1_business）｜Revenue — Intelligent Operating Solutions＝767.1 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi2_revenue_advanced_healthc`（q1_business）｜Revenue — Advanced Healthcare Solutions＝340.4 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi3_gaap_operating_profit`（q1_business）｜GAAP operating profit＝235.9 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi4_adjusted_ebitda`（q1_business）｜Adjusted EBITDA＝338.8 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi5_ios_adjusted_operating_p`（q1_business）｜IOS adjusted operating profit＝258.1 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi6_ahs_adjusted_operating_p`（q1_business）｜AHS adjusted operating profit＝82.3 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_peer_ftv_gross_margin_pct`（q2_moat）｜FTV 毛利率＝63.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FTV.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ftv_operating_margin_pct`（q2_moat）｜FTV 營業利益率＝19.63 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FTV.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ftv_fcf_margin_pct`（q2_moat）｜FTV FCF 利潤率＝27.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FTV.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ame_gross_margin_pct`（q2_moat）｜AME 毛利率＝36.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AME.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ame_operating_margin_pct`（q2_moat）｜AME 營業利益率＝25.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AME.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_keys_gross_margin_pct`（q2_moat）｜KEYS 毛利率＝64.69 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KEYS.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_keys_operating_margin_pct`（q2_moat）｜KEYS 營業利益率＝20.25 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KEYS.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_rok_gross_margin_pct`（q2_moat）｜ROK 毛利率＝54.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_rok_fcf_margin_pct`（q2_moat）｜ROK FCF 利潤率＝16.76 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_dov_gross_margin_pct`（q2_moat）｜DOV 毛利率＝39.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DOV.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_dov_fcf_margin_pct`（q2_moat）｜DOV FCF 利潤率＝13.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DOV.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.12 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.31 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.56 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_kpi10_guidance_fy2026_adjusted`（q1_business）｜Guidance: FY2026 adjusted diluted EPS＝3.10–3.14 USD｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
  - 註記：共識 FY1 EPS 3.12（來源：dd_numbers_extra.py consensus_revision，2026-10-31 快照）；中點約 +15% YoY
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4433.07 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝4588.56 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝2.01 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.49 → 3.56）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_kpi8_free_cash_flow`（q1_business）｜Free cash flow＝283.8 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_kpi9_stock_based_compensation`（q1_business）｜Stock-based compensation（前九個月累計）＝66.1 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，Fortive 官方 IR 新聞稿原文）https://www.sec.gov/Archives/edgar/data/0001659166/000165916626000039/ftv-q3x2026xearningsxpress.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-10-28））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3222.8 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 3600.1、現金 377.3（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝297.64 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.373 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝67.11 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.51 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.12，分子＝快照價 67.11｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.81 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝99.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝99.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝80.7 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.28 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝84.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.0 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 3.0 → 3.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝11.96 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝57.96 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（5 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱多個served markets 面臨低成本製造地區新進入競爭者與市場整併，競爭加劇；管理層自認在多數市場居領導地位，但無法彙總衡量競爭地位。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business—Competition（as_of 2026-02-25）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：風險因素載明若無法有效競爭可能導致需求與市占下降並被迫降價；部分通路夥伴也銷售競爭對手產品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：moat_trend、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：關稅影響進口至美國的原料與零組件成本；2025 年營收成長含為抵銷不利關稅影響所採取的定價行動，毛利端不利關稅影響已由對策抵銷。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 / Item 7（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：約 44% 銷售來自美國以外；風險因素點名美中貿易政策不確定性及 IEEPA 裁決後可能重新課徵類似關稅。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FTV 10-K 風險因子稱其產業技術變化快、新品頻繁推出；若不能及時推出創新產品，現有產品會隨時間過時，競爭地位與財務將受損。未點名任何具體替代技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":121.9,"bear_5y_price":49.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":28.8,"ev5y_pct":25.4,"irr_base_pct":5.2,"asym_ratio":2.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.12,"pe":21.51,"basis":"起點用 FY1（FY2026E）共識調整後 EPS，起點倍數＝判斷日股價÷FY1 EPS；終端倍數同樣套在當年度（FY2031E）調整後 EPS，口徑一致"},"eps":{"bull":[3.4,3.8,4.25,4.75,5.3],"base":[3.33,3.6,3.9,4.22,4.55],"bear":[3.02,2.8,2.95,3.12,3.28]},"pe":{"bull":23,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.373,"net_buyback":4.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FTV_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CEO｜guidance：CEO 宣布上調 2026 全年調整後 EPS 指引至 $2.95–$3.05。（原話："2026 adjusted EPS guidance to $2.95 to $3.05"）
- 2026-07-29｜CFO｜guidance：CFO 將全年核心成長預期由 2%–3% 上調至約 4%。（原話："we now expect full year core growth of approximately 4%"）
- 2026-07-29｜CFO｜guidance：CFO 指 Q3 調整後 EBITDA 利潤率預期略低於 Q2。（原話："Q3 adjusted EBITDA margins to be slightly below Q2 levels"）
- 2026-07-29｜CFO｜guidance：CFO 說調整後 EPS 預期偏重第四季。（原話："EPS delivery to be weighted towards the fourth quarter"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q4 銷售日比去年少 4 天，影響營收占比。（原話："4 fewer selling days in the quarter versus prior year"）
- 2026-07-29｜CFO｜guidance：CFO 更新稅率：Q3 有效稅率改為中段十幾趴。（原話："We now expect a Q3 effective tax rate in the mid-teens"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q4 的利潤率展望比 Q3 好。（原話："better, actually, margin outlook in the fourth quarter"）
- 2026-07-29｜CFO｜guidance：CFO 說企業費用每季約 $26–27 百萬。（原話："think about corporate costs in the $26 million to $27"）
- 2026-07-29｜CFO｜margin：CFO 說明毛利率年減約 100bp 的主因是產品組合。（原話："primarily driven by product mix dynamics resulting from"）
- 2026-07-29｜CFO｜margin：CFO 說 IEEPA 關稅退款不計入調整後指標，並預告後續還有退款。（原話："we exclude the impact of IEEPA"）
- 2026-07-29｜CFO｜margin：CFO 預告後續季度另有約 $20–25 百萬關稅退款。（原話："another roughly $20 million to $25 million of tariff refunds"）
- 2026-07-29｜CFO｜margin：CFO 說本季價格成本為正。（原話："price cost was positive for us in the quarter."）
- 2026-07-29｜CFO｜margin：CFO 稱 CertiFiber Max 等新品利潤率不低於整體。（原話："margins at or better than the fleet."）
- 2026-07-29｜CFO｜commitment：CFO 重申 EBITDA 利潤率每年擴張 50–100bp 的框架。（原話："50 to 100 basis point EBITDA margin expansion framework"）
- 2026-07-29｜CFO｜commitment：CFO 說 2026 與 2027 都會在 50–100bp 區間內。（原話："and we expect to do that in 2027 as well"）
- 2026-07-29｜CFO｜commitment：CFO 說今年核心成長走在 Investor Day 框架偏高端。（原話："it seems to be trending, at least for this year"）
- 2026-07-29｜CFO｜commitment：CFO 表示 2027 年起成長高於框架的願景在視野內。（原話："grow faster than our framework in sort of 2027 and beyond"）
- 2026-07-29｜CEO｜commitment：CEO 說對 2026–2027 財務框架的信心不變。（原話："our confidence in the 2026-2027 financial framework"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說明自分拆以來買回近 20 億美元股票。（原話："we have deployed nearly $2 billion to share repurchases"）
- 2026-07-29｜CEO｜capital_allocation：CEO 重申資本配置優先順序，首項為投資有機成長。（原話："priorities remain clear: invest in organic growth"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說已執行的併購預期偏向最大品牌。（原話："you see them skew towards our biggest brands where we're"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說軟體併購可能但路徑很窄。（原話："software bolt-ons are possible, but it's a very narrow path"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說併購會偏向硬體。（原話："going to skew towards hardware in the M&A that we do"）
- 2026-07-29｜CEO｜product：CEO 稱 CertiFiber Max 需求遠高於計畫，並帶動其他資料中心產品。（原話："demand for CertiFiber Max is way above our plan"）
- 2026-07-29｜CEO｜product：CEO 回答分析師：Fluke 不是資料中心公司。（原話："is not a data center company"）
- 2026-07-29｜CEO｜product：CEO 說 AI 投入金額不大，因 AI 卓越中心已存在多年。（原話："The investment level has not been significant for us"）
- 2026-07-29｜CEO｜product：CEO 說 AI 變現方式之一是依成效計價。（原話："And in some cases, those are outcome-based."）
- 2026-07-29｜CEO｜product：CEO 說 STERRAD 獲 FDA 核准擴大載重，預期提高贏單率。（原話："show up as increased win rates and expansion in our funnel"）
- 2026-07-29｜CEO｜product：CEO 說 ASP 資本設備業務本季回到成長。（原話："that capital business returned to growth this quarter"）
- 2026-07-29｜CEO｜customer：CEO 說 Fluke 經常性收入已連續多季雙位數成長。（原話："recurring revenue at Fluke growing double digits now for"）
- 2026-07-29｜CEO｜customer：CEO 說明 Fluke 訂單成長略快於營收，訂單出貨比明顯高於 1。（原話："so book-to-bill was nicely above 1"）
- 2026-07-29｜CEO｜customer：CEO 說明客戶基礎規模約 10 萬家。（原話："we do more for the 100,000 customers we have"）
- 2026-07-29｜CFO｜risk：CFO 說 EMEA 營收因總經不確定性小幅下滑。（原話："declined modestly due to macroeconomic uncertainty"）
- 2026-07-29｜CEO｜risk：CEO 把 Fluke 歐洲疲弱歸因於通路客戶延後採購，並提到歐洲 POS 為六季最佳。（原話："POS in Europe, it was actually the best we had"）
- 2026-07-29｜CFO｜risk：CFO 說記憶體晶片與稀土取得變難，正在做多重供應來源。（原話："rare earths and memory chips become harder to come by"）
- 2026-07-29｜CEO｜risk：CEO 回答 ACA 補貼到期的問題，說 ASP 處於復甦中並已納入考量。（原話："which is it's in recovery"）

### 問答異常語氣（迴避／改口／保留）
- FTV_Q2_2026_Earnings_Call_20260729.md｜問：Chris Snyder（Morgan Stanley）：下半年各部門利潤率是否持平到下滑，驅動因素為何｜答法：CFO 未直接確認或否認部門利潤率走勢，改談 50–100bp 全年框架、Q3 比較基期、組合效應與企業費用
- FTV_Q2_2026_Earnings_Call_20260729.md｜問：Jamie Cook（Truist）：今年 EBITDA 利潤率擴張是否落在 50bp 低端｜答法：CFO 未回答是否落在低端，只重申 50–100bp 區間與全年 EBITDA 利潤率約 30%
- FTV_Q2_2026_Earnings_Call_20260729.md｜問：Chigusa Katoku（JPMorgan）：今年看似落在低端，為何 2027 能做到 50–100bp，是否有 AI 投資的利潤率壓力｜答法：CFO 未回應是否落在低端，也未正面答 AI 投資壓力，改說 50–100bp 是公司可掌控的框架、成長優於預期
- FTV_Q2_2026_Earnings_Call_20260729.md｜問：Deane Dray（RBC）：能否量化 AI 投入規模與效益衡量｜答法：CEO 只說投入「not significant」，未給金額，也未給效益的具體數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 1 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 2 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 5 | 3 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Fortive Accelerated 把 core growth 從 2-3% 結構性推到 4-5%，且不是靠一次性比較基期（最關鍵的結構性假設）"},{"id":"H2","text":"adj EBITDA margin 每年擴張 50-100bp，且擴張來自組合升級與營運槓桿，不只是離散成本節省（成長兌現的操作性假設）"},{"id":"H3","text":"資本配置維持「回購優先、併購只做小型 bolt-on」的紀律，使每年淨股數收縮 4-5%（估值修復與每股複利的市場假設）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Q3-Q4 的利潤率擴張落在框架低端，市場把「50-100bp」重新理解為「50bp」——管理層已預告 Q3 adj EBITDA margin 低於 Q2、Q3 OpEx 比較基期較難、Q3 EPS 僅微幅成長；三位賣方分析師在同一場 Q&amp;A 連續質疑全年只會落在 50bp"},{"id":"R2","text":"adj 毛利率的組合侵蝕由「一次性混合效應」變成結構性下移，且與 AHS 的量能逆風疊加——Q2 合併 −100bp、IOS −100bp（多點零售客戶的低毛利策略性產品）、AHS −110bp（資本設備回升＋大客戶策略性投資）。AHS 這一腿有一條獨立的政策傳導鏈：ACA 加強版保費補貼已於 2026-01-01 到期且國會未展延，醫院端追蹤數據顯示選擇性住院手術量 −6%、門診手術 −3.4%（Intuitive Surgical 在 2026 Q2 法說亦將美國程序量放緩部分歸因於此）——ASP 卡匣耗材與 Provation 的 GI 文件量都是程序量的函數，這可能就是 AHS core +5.3%（低於 IOS +7.4%）與分部利潤率 −80bp 的共同成因"},{"id":"R3","text":"資本配置回頭走溢價併購路線，把每股複利引擎換成商譽——執行長剛被拿掉成長敘事、併購團隊剛就位、且自述會「偏向差異化硬體」（硬體標的比軟體便宜，但也更難創造 10%+ 的增量資本報酬）"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價 ≤$53（PEG 回到 2.0）或 FY2028 共識 EPS ≥$3.60（同價位使 PEG 降至 2.0）；兩者任一成立即重跑裁決。","irr_base_pct":10.0,"ev5y_pct":46.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.5,"ev5y_pct":46.9,"irr_base_pct":10.0,"max_dd_pct":-45.0,"bull_5y_price":124.0,"bear_5y_price":43.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"價 ≤$53（PEG 回到 2.0）或 FY2028 共識 EPS ≥$3.60（同價位使 PEG 降至 2.0）；兩者任一成立即重跑裁決。","price_at_dd":59.54,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FTV","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Fortive Corporation"},"oneliner":"Fortive 有機成長連五季加速，全年指引兩度上調，生意比七月更好；但股價先漲 13%，前瞻本益比 21.5 倍只對應約 7% 的後續每股盈餘成長。等 $58 以下，或 FY2027 指引確認後再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTV_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是現場技術人員、工安主管與醫院無菌供應室為可靠量測與合規付的錢；錢卡在品牌儀器與裝機基礎之後的耗材、訂閱與工作流程軟體這一節","reasoning":"最新一季營收 11.08 億美元。IOS 7.67 億，約占 69%，包括 Fluke 專業儀器、設施與資產生命週期軟體、氣體偵測；AHS 3.40 億，約占 31%，包括 ASP 滅菌設備與耗材、Provation 醫療文件軟體。分部調整後營益率 IOS 約 33.6%、AHS 約 24.2%；GAAP 營業利益 2.36 億，營益率約 21.3%；調整後 EBITDA 利潤率 30.6%。TTM 毛利率 63.5%、營益率 19.6%、自由現金流率 27.1%。單點依賴：沒有客戶集中，客戶約 10 萬家，10-K 稱應收帳款沒有重大信用集中；最大的依賴是 Fluke 品牌本身。產業時鐘在擴張段：Fluke 訂單在 Q2 已強的基礎上再加速，訂單出貨比大於 1；核心成長連五季逐季加速，各區域都有成長，只有中國仍不穩。供需持久性以週期性為主：資料中心與國防是結構性需求，但目前只占營收低個位數，景氣轉弱時需求會回落。產業態勢是雙向拉鋸：競爭面，10-K 自述低成本地區新進者增加；結構面，資料中心、國防與手術移往門診手術中心帶來新需求；政策面，關稅反覆，IEEPA 被判無效後政府改用其他授權課稅。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_revenue_intelligent_oper","f_kpi2_revenue_advanced_healthc","f_kpi3_gaap_operating_profit","f_kpi4_adjusted_ebitda","f_kpi5_ios_adjusted_operating_p","f_kpi6_ahs_adjusted_operating_p","f_peer_ftv_gross_margin_pct","f_peer_ftv_operating_margin_pct","f_peer_ftv_fcf_margin_pct"],"verdict_values":{"revenue_quality":"兩個分部的經常性收入都在成長，但 Q3 非經常性硬體成長更快，主要來自 Fluke。管理層稱 Fluke 訂單連續多年成長，耐久度不輸經常性收入。另有一處要留意：ServiceChannel 的代收代付型合約會把營收灌大，這部分毛利率偏低。","unit_econ_note":"IOS 調整後營益率約 33.6%，AHS 約 24.2%。AHS 走刮鬍刀加刀片模式，先賣 STERRAD 滅菌設備，再靠耗材回收；管理層今年刻意擴大裝機，換取之後的耗材流量。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率高（約 63%）、資產輕、自由現金流高於淨利，每股盈餘靠回購墊高；組合是工業儀器加工作流程軟體"},"industry":{"clock_phase":"II","sd_verdict_source":"以週期性為主，帶小比例結構性成分。工業儀器與醫院資本設備需求跟著景氣走，目前在上升段；資料中心與國防屬結構性需求，但只占營收低個位數。依據：2026-10-28 Q3 法說、2026-07-29 Q2 法說","bargaining":{"up":"上游是一般邏輯晶片、記憶體與電子零件，不用高頻寬記憶體；公司多來源採購，遇到瓶頸會提前備貨。Q3 零件與運費通膨上升，價格成本差仍為正","down":"客戶分散，約 10 萬家，應收帳款沒有信用集中。部分通路夥伴同時賣競品，醫院端預算仍受限","geo":"約 44% 營收在美國以外，中東約 2%，中國不穩、由印度補上；2018 年以來自中國進口的曝險已降 70%"},"profit_pool_dir":"利潤池往軟體與經常性收入移動，例如 eMaint、ServiceChannel、Provation、iNet 訂閱，以及氣體偵測的硬體即服務。量化占比事實表未涵蓋","tam_table":{"expanded":false,"reason":"FTV 的主體是成熟的專業儀器與醫療滅菌市場，不屬於低滲透或新品類。資料中心是潛在第二曲線，但只占營收低個位數，五年內撐不起整體估值；TAM 與滲透率事實表也未涵蓋"}}}},"q2_moat":{"verdict":"護城河穩定（→）。品牌儀器與裝機基礎讓公司在零件與運費通膨下仍維持正的價格成本差，兩個分部同時有量有價。但毛利率連兩季年減，也沒有市占或報酬率利差數據可以證明護城河在擴大","reasoning":"機制有四塊：Fluke 的品牌信任與通路；ASP 裝機帶耗材的刮鬍刀模式；ServiceChannel、Gordian、eMaint、Provation 這些嵌進客戶工作流程的軟體；以及氣體偵測的 iNet 訂閱。同業報酬率利差與市占數據事實表未涵蓋，所以改看定價與利潤率。定價面，Q3 AHS 價格貢獻約 280bp（Q2 約 190bp），CFO 預期約 200bp 可延續到 2027 年；電子零件與運費通膨上升，價格成本差仍為正，兩個分部都是量價齊升。利潤率面，毛利率 63.5%，與 KEYS 同屬同業最高一級，遠高於 AME 與 DOV；但營益率 19.6% 低於 AME 的 25.9%，高毛利有一大塊被業務與研發費用吃掉。負面證據：調整後毛利率連兩季年減，管理層歸因於組合；10-K 也自述低成本新進者與市場整併讓競爭加劇，可能被迫降價。執行力給 7、定價力給 8，等級 B。方向判穩定而非擴大，因為缺市占或報酬率利差的證據。","fact_refs":["f_peer_ftv_gross_margin_pct","f_peer_ftv_operating_margin_pct","f_peer_ftv_fcf_margin_pct","f_peer_ame_gross_margin_pct","f_peer_ame_operating_margin_pct","f_peer_keys_gross_margin_pct","f_peer_keys_operating_margin_pct","f_peer_rok_gross_margin_pct","f_peer_rok_fcf_margin_pct","f_peer_dov_gross_margin_pct","f_peer_dov_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"品牌儀器（Fluke）的信任與通路，加上裝機基礎帶動的耗材（STERRAD）、訂閱（iNet）與嵌入式工作流程軟體（ServiceChannel、Gordian、eMaint、Provation）的轉換成本","execution":7,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：核心成長連五季逐季加速，全年指引連兩季上調。定價力穩定：AHS 價格貢獻由約 190bp 升到約 280bp，管理層預期約 200bp 延續到 2027 年，價格成本差為正；但調整後毛利率連兩季年減（Q2 −100bp、Q3 −80bp，屬組合效應）。兩者合起來判穩定。沒有市占或報酬率利差證據，不給擴大","competitor_notes":[{"name":"AME","strategy_note":"毛利率遠低於 Fortive，營業利益率反而更高，是費用效率的對照標竿；Fortive 的高毛利還沒完全轉成營業利益"},{"name":"ROK","strategy_note":"工業自動化同業，毛利率、營益率都接近 Fortive 的下緣，自由現金流率明顯較低，景氣敏感度較高"},{"name":"KEYS","strategy_note":"毛利率與 Fortive 同級，研發密度約為三倍，靠技術領先競爭；Fortive 則更靠品牌與通路"},{"name":"DOV","strategy_note":"多元工業，毛利率與自由現金流率都明顯低於 Fortive，反襯出 Fortive 產品組合的定價力較高"}],"peer_na_reason":"同業報酬率利差事實表未涵蓋，只收了利潤率；改用毛利率、營益率、自由現金流率與價格貢獻作可比軸","threats":[{"level":"🟡","text":"低成本製造地區的新進者加上市場整併，使競爭加劇；10-K 自述可能失去份額或被迫降價，而且通路夥伴同時賣競品。這屬點對點競爭，目前價格貢獻仍約 200bp，尚未看到降價","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"產業技術更迭快、新品頻繁，創新跟不上產品就會過時。10-K 沒有點名具體的替代技術；Fluke 本季仍推出 iSee Pro、CertiFiber Max 等新品，顯示創新還在進行","p":"20%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"AI 可能改變軟體商業模式，Q3 法說有分析師追問這點。FAL 與 Provation 的軟體有被 AI 原生工具繞過的風險。管理層稱 AI 建在自有資料與工作流程上，例如 Provation 累積 30 年的專有資料庫，但沒有給 AI 收入數字","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"利益率高；周轉率事實表未涵蓋，因為投入資本沒有收錄。公司長期靠併購組成，商譽可能偏高，推定為高利益率×低周轉，需要查再投資負擔","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是現場技術人員與工安人員，決策者是維修或工安主管，付款者是企業，三個角色方向一致。電氣測試、氣體偵測、器械滅菌是合規與安全的必需品，延後購買的代價是停機或違規。代理讀數：Fluke 訂單多年持續成長，Q3 訂單再加速；醫療程序量整體健康"},{"item":"決策層級","level":"🟡","text":"硬體按單台、單一工地採購，最小決策單位小；通路夥伴同時賣競品，低成本新進者可以逐台搶單。軟體與裝機基礎的轉換成本較高，例如 eMaint 平台遷移、iNet 偵測器車隊管理、STERRAD 裝機帶耗材。代理讀數：價格貢獻約 200bp，量仍在成長，漲價沒有造成可見的流失。續約率與流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟢","text":"儀器與耗材占客戶總支出的比重小，卻牽動停機、安全與合規成本，所以公司拿得到定價。上游零件多來源，公司會提前備貨，沒有單一供應商卡位；Q3 電子零件與運費通膨仍被吸收，價格成本差為正。弱點是 ServiceChannel 代收代付合約這一段，利潤率低"},{"item":"社會容忍度","level":"🟡","text":"工業工具沒有社會敏感性。AHS 約占 31% 營收，客戶是預算仍受限的醫院；Q3 價格貢獻約 280bp，持續漲價可能遇到採購壓力。公司的定價權不依賴監管授權"}],"roiic":"事實表未涵蓋：投入資本與歷年收購金額沒有收錄，算不出增量報酬","reinvest_rate":"低（定性判斷）：再投資主要是費用化的研發與業務擴編，收購只有小型補強，自由現金流大多拿去回購。精確比率事實表未涵蓋","endo_ceiling":5.0,"formula_note":"增量報酬×再投資率所需的數字缺，改用有機核心成長代理內生上界：投資人日框架 3–4%，FY2026 實際略高於 5%，取 5%（年增率 %）。回購與利潤率擴張帶來的每股盈餘成長不算內生"}}}},"q3_growth":{"verdict":"成長跑道中等（🟡）。專業儀器與氣體偵測屬成熟市場；第二條曲線資料中心目前只占營收低個位數，還不足以撐起五年後的成長","reasoning":"成長來源是量、價加回購。核心成長略高於 5%，其中價格約 2pp，其餘是量；調整後 EBITDA 利潤率每年擴張 50–100bp；淨回購每年減股約 3–5%；併購只做補強。共識三年 EPS 年複合約 9.5%（FY2025A 約 2.71 → FY2028E 3.56），但扣掉 FY2026 因回購墊高的一年，FY2026E→FY2028E 只有約 6.8%。內生上界取 5%，缺口約 4.5pp：淨回購約 3–4pp（Q3 買回 3 億美元，年化約市值 6%，扣掉併購與股價上漲因素後估 3–4%），利潤率擴張約 1–2pp。缺口可以歸因，不依賴倍數重估。衰退信號亮兩項：毛利率連兩季年減，以及 FY2026 EPS 成長約 15%、營收成長約 6.6%，落差超過 5pp。兩項都有已知成因（組合效應、回購），所以長期成長性給中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi10_guidance_fy2026_adjusted","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量價並進，再加回購。核心成長約 5%，其中價格約 2pp；調整後 EBITDA 利潤率每年擴張 50–100bp；淨回購每年減股約 3–5%；併購只做補強","runway_years":"事實表未涵蓋滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的內生上界 5%（以有機核心成長代理）。共識三年 EPS 年複合約 9.5%，缺口約 4.5pp，歸因淨回購約 3–4pp、利潤率擴張約 1–2pp；可歸因，不依賴倍數重估","segments":[{"item":"IOS（智慧營運方案）","value":"Q3 營收 7.67 億美元，約占 69%，核心成長 9.1%，調整後營益率約 33.6%。Fluke、FAL 軟體、氣體偵測三塊成長速度接近，Fluke 略快；訂單出貨比大於 1"},{"item":"AHS（先進醫療方案）","value":"Q3 營收 3.40 億美元，約占 31%，核心成長 3.1%（年初至今 4.5%），調整後營益率約 24.2%。分部 EBITDA 年減 5%，管理層稱今年是擴大裝機的限期投資"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"note":"調整後毛利率 Q2 −100bp、Q3 −80bp"},{"item":"EPS 成長顯著高於營收成長（差距大於 5pp）","lit":true,"note":"FY2026 EPS 約 +15%，營收約 +6.6%；落差主要來自回購"},{"item":"核心市占縮減","lit":false,"note":"事實表未涵蓋市占數據"},{"item":"提價後銷量下滑","lit":false,"note":"兩個分部量價齊升"},{"item":"自由現金流對淨利小於 0.75 連 2 年","lit":false,"note":"轉換率遠高於 100%"},{"item":"股權激勵占營收大於 5% 且上升","lit":false,"note":"年化約 2%"},{"item":"TAM 萎縮或被替代","lit":false,"note":"10-K 只泛稱技術更迭快，沒有點名替代技術"},{"item":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維持性資本支出占自由現金流大於 60%","lit":false,"note":"資產輕"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"研發與業務擴編持續投入，營收成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置以回購為主，紀律清楚：自由現金流高於淨利，股權激勵約占營收 2%。但股價走高後回購報酬下降，管理層開始把併購擺到更大的比重","reasoning":"現金去向：Q3 回購 3 億美元，分拆後累計回購 23 億美元，約占 13% 股數；股息規模小，Q3 調升 17%，殖利率約 0.4%；併購只有 Aeroqual、UV Smart 等小型補強，管理層稱表現符合併購案預期，但沒有揭露報酬率；資本支出事實表未涵蓋。現金轉換：TTM 自由現金流超過 10 億美元，對淨利的轉換遠高於 100%；Q3 自由現金流 2.84 億美元，其中含 1,800 萬美元一次性關稅退款。槓桿：總債務對調整後 EBITDA 2.6 倍，比上季略降，政策區間約 2.5 倍；淨負債約 32 億美元。股權激勵前九個月 6,610 萬美元，年化約占營收 2%，回購之後淨股數仍持續下降。","fact_refs":["f_kpi8_free_cash_flow","f_kpi9_stock_based_compensation","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_ftv_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"近期只有 Aeroqual、UV Smart 等小型補強，管理層稱符合併購案預期；已實現的投入資本報酬與加權資金成本，事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"23 億美元買回約 13% 股數，推算均價約 $51–59（依分母口徑而定），對 FY2026E 調整後 EPS 3.12 的盈餘殖利率約 5.3–6.1%；10 年期公債殖利率事實表未涵蓋，無法對照門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九個月股權激勵 6,610 萬美元，年化約 8,800 萬美元，約市值 0.4%，低於每年 1.5% 的門檻；回購之後淨股數持續下降"}],"grade":null},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近五季資本主要流向回購，併購只有小型補強，對營收貢獻小"}}}},"q5_valuation":{"verdict":"現價要求 FY2026 之後每股盈餘每年成長約 7% 以上，而且倍數守在 21 倍以上。我相信生意會繼續變好，但不認為現價給了足夠補償","reasoning":"共識 FY2027 只成長 6.1%、FY2028 成長 7.6%。用管理層框架推算（核心成長 3–4%、利潤率每年擴張 50–100bp、加上回購）可以到 8–10%，所以基準情境略高於共識。但即使照走，只要倍數小幅收斂到 19 倍，五年年化報酬只有約 5–6%。PEG 以前瞻本益比 21.5 倍除以三年 EPS 年複合約 9.5%，約 2.3；扣掉回購墊高的 FY2026，同口徑約 3.2。分母口徑：GAAP 與調整後 EPS 差距大，但自由現金流高於調整後淨利，調整後口徑有現金支撐。歷史位置只有四個年度端點，而且早年含分拆前的業務，只當輔助。賣方目標價均值約 $63–65，低於現價。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_current","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 調整後 EPS）加 PEG（三年 EPS 年複合）","tier":"高毛利工業儀器加工作流程軟體","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，同業表只有利潤率，無法做倍數對照"},"fwd_pe":21.51,"peg":2.26,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 21.5 倍，FY2025A→FY2028E 共識 EPS 年複合約 9.5%，PEG 約 2.3，大於 2 屬偏貴；扣掉 FY2026 回購墊高的一年，後續兩年共識年複合只有約 6.8%，同口徑 PEG 約 3.2。基準情境五年年化約 5–6%，低於 8%。五年連續分位事實表未涵蓋；四個年度端點的 trailing 分位偏高，但混入分拆前口徑，只當輔助。綜合判斷偏貴，但沒有到極端","upside_short_pct":-0.8,"upside_mid_pct":28.8,"denominator_disputed":false,"denominator_note":"GAAP 與調整後 EPS 差距大：FY2025 GAAP 稀釋 EPS 1.73，調整後約 2.71，主因是收購無形資產攤銷與分拆成本。自由現金流高於調整後淨利，調整後口徑有現金支撐，所以不視為爭點。關稅退款已由公司自行排除在調整後盈餘之外"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把景氣特別好的一年當成結構性加速。陷阱風險屬輕度，原因是毛利率連兩季年減，加上每股盈餘成長大幅領先營收","reasoning":"三個反向故事都寫在反證紀錄：景氣回頭讓 EPS 停在 3 美元出頭；資本轉向高價併購；價格已經先反映。最大回撤估 −30%～−45%：倍數由 21.5 倍回到 15 倍，再加上景氣年 EPS 回落約 10%。歷史最大回撤、空方報告與訴訟金額，事實表都未涵蓋。10-K 稱現有訴訟沒有重大影響；近 12 個月 8-K 只有兩份融資類重大事項，沒有併購、財報重編或調查。","fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy1","f_peer_ftv_gross_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"輕度：毛利率連兩季年減，每股盈餘成長大幅領先營收（落差來自回購）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.12,"pe":21.51,"basis":"起點用 FY1（FY2026E）共識調整後 EPS，起點倍數＝判斷日股價÷FY1 EPS；終端倍數同樣套在當年度（FY2031E）調整後 EPS，口徑一致"},"eps":{"bull":[3.4,3.8,4.25,4.75,5.3],"base":[3.33,3.6,3.9,4.22,4.55],"bear":[3.02,2.8,2.95,3.12,3.28]},"pe":{"bull":23,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.37,"net_buyback":4.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-45,"hi":-30,"basis":"事實表沒有收錄歷史最大回撤，改用倍數與盈餘兩段推估。只有倍數修正（21.5 倍→15 倍）約 −30%；再疊加景氣下行年 EPS 回落約 10%（3.12→2.80），約 −37%；股價目前在 52 週均線上方約 16%，回吐空間再加一段，深端取 −45%","trigger_time":null},"basis":{"bull":"Fluke 的資料中心與國防業務持續擴大，核心成長維持 6% 以上，利潤率每年擴張約 100bp，回購每年減股約 5%，EPS 年複合約 11%；品質溢價擴大，倍數給 23 倍","base":"核心成長回到 4–5%，利潤率每年擴張 50–100bp，淨回購每年約 3–4%。前兩年貼近共識（3.31、3.56），之後約 8%，EPS 年複合約 7.8%；倍數由 21.5 倍收斂到 19 倍。EPS 是每股口徑，已含回購效果。同業前瞻倍數事實表未涵蓋，終端倍數以自身現值為錨","bear":"工業景氣轉弱，毛利率的組合侵蝕變成結構性，AHS 的投資不見回報：FY2027–28 EPS 回落到 2.8–3.0，FY2031 才回到 3.28；成長熄火到約 5%，倍數給 15 倍。機率 30% 的依據：管理層承認今年部分市場特別強，毛利率連兩季年減，而且共識 EPS 成長已超過有機內生上界"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CEO 在 Q3 法說承認部分終端市場今年特別強；Q4 少 4 個銷售日；10-K 自述低成本地區新進者增加、技術更迭快；調整後毛利率連兩季年減","assumption":"今年略高於 5% 的核心成長，有相當部分來自景氣與比較基期，而不是新策略的結構性成果","consequence":"工業景氣轉弱時，IOS 核心成長回到 0–2%，AHS 維持低個位數，EPS 五年卡在 $3.0–3.3，倍數回到 15 倍，股價約 $45–50（−25%～−33%）。要虧 50%，倍數得掉到約 11 倍，可能性低","ruling":"部分採納。景氣成分確實存在，用 30% 的悲觀機率反映。但兩個分部同時量價齊升、各區域都在成長、Fluke 訂單連續多年成長，不支持「全是景氣」的說法","watch":"IOS 核心成長、Fluke 訂單出貨比、2027 年 2 月的 FY2027 指引","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"],"fact_refs":["f_kpi1_revenue_intelligent_oper","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"約 44% 營收在美國以外，風險因素點名中美政策不確定，以及 IEEPA 判決後政府可能用其他方式重新課稅；2025 年營收成長有一部分是轉嫁關稅的漲價；Q3 電子零件與運費通膨上升","assumption":"價格成本差可以一直維持正值","consequence":"如果新關稅或零件通膨超過漲價能力，毛利率年減擴大到 100bp 以上，利潤率擴張的假設就失效","ruling":"列為監測，不做預測。吸收失敗的判斷標準：價格成本差轉負，或調整後毛利率年減超過 100bp","watch":"每季價格成本差評論、調整後毛利率年變化、關稅政策","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":["f_peer_ftv_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 法說 CFO 表示希望併購占更大比重，併購團隊已重整；股價比前份判斷高約 13%，回購買到的盈餘殖利率下降；ServiceChannel 代收代付合約把營收灌大但毛利低；2025 年部分成長來自轉嫁關稅的漲價","assumption":"成長加速成立，但錢被花在高價併購或低毛利營收上，每股價值沒有同步增加","consequence":"營收與 EBITDA 照指引走，但回購減速加上併購攤薄，每股盈餘只成長 4–6%，低於現價隱含的約 7%","ruling":"採納為監測項。目前只有管理層的意向表述，沒有實際交易；單筆超過 10 億美元的併購出現就重跑判斷","watch":"併購金額與估值倍數、每季回購金額、毛利率組合","evidence_refs":["reg_tariff_export#0"],"fact_refs":["f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"前瞻本益比 21.5 倍；FY2026E→FY2028E 共識 EPS 年複合約 6.8%；賣方目標價均值約 $63–65，低於現價；26 週上漲約 12%，股價在 52 週均線上方約 16%","assumption":"市場已經把連兩次上調指引與資料中心題材算進價格","consequence":"即使基準情境照走，倍數小幅收斂會吃掉部分盈餘成長，五年年化報酬只剩約 5–6%","ruling":"採納，這是本次不進場的主因。資料中心目前只占營收低個位數，題材再熱也撐不起整體倍數","watch":"股價 $58 以下，或 FY2028 共識 EPS 升到 $3.70 以上","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy3","f_week26_return_pct","f_ma_w52","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 59.54 → 本次 67.11（+12.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=59.54","side_b":"本次 price_at_dd=67.11","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 59.54 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 59.54 美元：Bull 價 124、Bear 價 43，五年期望值 +46.9%，基準年化 10.0%，不對稱比 3.5","side_b":"本次情境、股價仍用 59.54 美元：Bull 價 121.9、Bear 價 49.2，五年期望值 +41.3%，基準年化 7.7%，不對稱比 5.03","ruling":"先換情境、股價不動：五年期望值少 5.6 個百分點，基準年化少 2.3 個百分點。不對稱比由 3.5 變為 5.03。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 59.54 美元：五年期望值 +41.3%，基準年化 7.7%，不對稱比 5.03","side_b":"本次情境、股價 67.11 美元：五年期望值 +25.4%，基準年化 5.2%，不對稱比 2.55","ruling":"再換股價、情境不動：起點價上漲 12.7%，五年期望值少 15.9 個百分點，基準年化少 2.5 個百分點，不對稱比由 5.03 降到 2.55。合計五年期望值比前份少 21.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：營運加速有多方證據","cause":null,"side_a":"Q3 財報新聞稿：核心成長 7.2%，調整後 EPS 年增 13%，全年指引上調到 $3.10–3.14","side_b":"Q3 法說：Fluke 訂單再加速，訂單出貨比大於 1，各區域都在成長；兩個分部量價齊升","ruling":"兩邊一致，不需要裁決","evidence_level":"高（財報新聞稿與法說原文）","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#0","capital_markets_pricing#0"]},{"axis":"營運動能 vs 估值（⚖）","cause":null,"side_a":"現在就買的最強論證：共識 FY2027 只成長 6.1%，低於框架加回購推得的 8–10%；指引已連兩季上調，Fluke 訂單仍在加速。若 FY2027 指引給到 $3.45，共識上修會把 PEG 壓回 2.0，現在不買，可能永遠等不到 $58","side_b":"現價前瞻 21.5 倍、PEG 約 2.3，基準情境五年年化約 5–6%，低於 8% 的及格線；賣方目標價均值低於現價；另有兩項衰退信號亮燈（毛利率、EPS 與營收落差）","ruling":"選 B 側。這是程度差異，可以調和：生意判斷與價格判斷不衝突，只是價格先走了。依據是基準年化報酬低於 8% 這個硬數字。執行上，等價格或指引任一條件成立","evidence_level":"高（財報新聞稿、法說原文與共識快照）","settle_metric":"FY2027 調整後 EPS 指引中點（2027 年 2 月）","if_then":["若股價回到 $58 以下、FY2027 指引還沒公布：重跑判斷，通過才首倉 2%","若 2027 年 2 月 FY2027 調整後 EPS 指引中點 ≥$3.45，且核心成長指引 ≥4%：股價在 $67 以下就首倉 2%","反向：若股價先漲過 $75，而指引與共識沒有跟上：不追","反向：若指引中點低於 $3.31：停止建倉計畫，價格門檻下修到 $52"],"evidence_refs":[]},{"axis":"毛利率：管理層說法 vs 數據","cause":null,"side_a":"Q3 法說 CFO：毛利率是同業最高一級，長期維持紀律；年減來自組合，包括 ServiceChannel 代收代付合約與新興市場耗材，代收代付的影響不會再擴大","side_b":"調整後毛利率 Q2 年減 100bp、Q3 年減 80bp，連兩季下滑；電子零件與運費通膨上升；10-K 自述競爭可能迫使降價","ruling":"對管理層的一次性歸因不採信、也不否定，標為未證實、持續監測。先登記判準：FY2026 Q4 與 FY2027 Q1 若仍年減 50bp 以上，組合歸因就算證偽","evidence_level":"中（只有管理層口頭歸因，沒有組合拆解數字）","settle_metric":"調整後毛利率年變化（FY2026 Q4、FY2027 Q1）","if_then":["若連四季年減 50bp 以上：長期信心降為低；若已持有，減碼一半","反向：若 FY2027 Q1 年減收窄到 30bp 以下：撤銷這項風險"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"AHS 投資的性質：成長投資還是守成成本","cause":null,"side_a":"Q3 法說 CEO：今年是限期、刻意的投資年，擴大裝機、增加業務人力、加碼研發，之後會帶來多年的成長加速與利潤率擴張","side_b":"JPMorgan 分析師指出 AHS 利潤率已持平好幾年；Q3 分部 EBITDA 年減 5%，利潤率年減 230bp（其中約 100bp 是去年一次性利益的基期）；10-K 自述競爭加劇","ruling":"未證實，持續監測。先登記判準：FY2027 AHS 調整後 EBITDA 利潤率若比 FY2026 擴張不到 100bp，就判定這筆投資是守成成本","evidence_level":"中","settle_metric":"FY2027 AHS 調整後 EBITDA 利潤率","if_then":["若擴張 ≥100bp 且 AHS 核心成長 ≥4%：利潤率擴張的假設加強，基準機率上調 5 個百分點","若擴張不到 100bp：AHS 改按低成長資產估值，基準 EPS 路徑下修約 3%"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"axis":"資本配置：前後兩季說法","cause":null,"side_a":"Q2 法說（2026-07-29）CEO：已做的併購偏向最大品牌與硬體，軟體併購的路徑很窄","side_b":"Q3 法說（2026-10-28）CFO：過去五季偏重回購，已重整併購團隊與流程，希望併購成為更大的一塊；股價上漲後，回購的吸引力下降","ruling":"可以調和，方向一致，只是程度加大。沒有實際大額交易之前不扣分","evidence_level":"高（兩場法說原文）","settle_metric":"單筆併購金額與每季回購金額","if_then":["若宣布單筆超過 10 億美元的併購：重跑判斷，期間停止任何建倉計畫","若每季回購降到 1.5 億美元以下、又沒有併購：每股複利的假設削弱"],"evidence_refs":[]},{"axis":"前份風險退休：利潤率擴張落在框架下緣","cause":null,"side_a":"前份第一風險：全年利潤率擴張只會落在 50–100bp 的下緣；Q2 法說三位分析師連續追問，CFO 沒有正面回答。前份第二風險的醫療程序量疑慮也一併列出","side_b":"Q3 法說 CFO：全年調整後 EBITDA 利潤率擴張約在區間中點；Q3 利潤率年增 50bp，已吸收約 50bp 的去年一次性基期。Q3 CEO 稱醫療程序量整體健康，醫院資本支出比去年改善，但仍受限","ruling":"前份第一風險退休，已被證據否定。醫療程序量疑慮降級，併入 AHS 投資監測；毛利率組合侵蝕保留，列為本次第一風險","evidence_level":"高（兩場法說原文）","settle_metric":"全年調整後 EBITDA 利潤率擴張幅度","if_then":["若 FY2026 實際擴張不到 50bp：恢復這項風險，並下修基準利潤率路徑"],"evidence_refs":[]},{"axis":"前份漂移：估值結論、等級、裁決、機率與回撤範圍","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-30，股價 $59.54）：偏貴，等級 B，觀望；樂觀 25%、悲觀 30%；最大回撤 −45%","side_b":"本次（股價 $67.11，+12.7%）：股價漲幅大於 FY1 共識上修（約 +4%），但 FY2028 共識也上修，PEG 由約 2.25 變成約 2.26，估值結論維持偏貴、等級 B；機率維持 25／45／30；回撤範圍 −30%～−45%","ruling":"股價上漲與盈餘上修大致抵銷，結論不變。不因營運轉好而提高樂觀機率，因為漲幅已先反映","evidence_level":"高","settle_metric":"PEG（前瞻本益比÷三年 EPS 年複合）","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價值陷阱風險由低升為輕度","cause":"新證據","prior_field":["trap"],"side_a":"前份：陷阱風險低（🟢），當時只有 Q2 一季毛利率年減 100bp","side_b":"本次：Q3 調整後毛利率再年減 80bp，構成連兩季年減；FY2026 EPS 年增約 15%、營收約 6.6%，差距超過 5pp（主要來自回購）。兩項衰退信號亮燈，調為輕度（🟡）","ruling":"新證據導致調升。兩項信號都有已知成因（組合效應、回購），所以停在輕度","evidence_level":"高（財報新聞稿與法說）","settle_metric":"調整後毛利率年變化","if_then":["若毛利率連四季年減：升為高度"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"前份漂移：護城河方向、成長跑道、公司類型、景氣位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河穩定、跑道中等、品質複利成長、未定景氣位置","side_b":"本次全部維持不變。新證據支持定價力穩定：AHS 價格貢獻約 280bp、兩個分部量價齊升、Fluke 訂單出貨比大於 1。資料中心仍只占營收低個位數，不足以把跑道升級","ruling":"新證據方向一致，維持原判","evidence_level":"高","settle_metric":"價格貢獻與資料中心營收占比","if_then":[],"evidence_refs":["end_markets#0"]},{"axis":"前份漂移：估值重啟門檻（進場首倉條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價 ≤$53（PEG 回到 2.0）或 FY2028 共識 EPS ≥$3.60（同價位使 PEG 降至 2.0）；兩者任一成立即重跑裁決。","side_b":"價 ≤$58（PEG 約 2.0、五年基準年化約 8.5%）或 FY2028 共識 EPS ≥$3.70（現價下 PEG 約 2.0）；任一成立即重跑判斷","ruling":"舊門檻→新門檻。FY1 共識由約 3.00 升到 3.12，FY2028 共識由 3.49 升到 3.56，PEG 2.0 對應的價格由 $53 上移到約 $59；取 $58，同時讓 PEG 約 1.96、基準年化約 8.5%。第二條件：現價由 $59.54 漲到 $67.11，要讓 PEG 回到 2.0，FY2028 EPS 須由 $3.60 升到 $3.70。方法不變，只換輸入；條件成立後先重跑判斷，再決定是否進場首倉","evidence_level":"高","settle_metric":"股價與 FY2028 共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）由空白改為設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（空白）","side_b":"2027 年 2 月公布的 FY2027 全年指引：調整後 EPS 中點低於 $3.31，或核心成長指引低於 3%","ruling":"本次依規則補上。選 FY2027 指引的原因：倍數是最大的單一敏感度，而指引是倍數最直接的開關","evidence_level":"中","settle_metric":"FY2027 調整後 EPS 指引中點","if_then":["若觸發：價格門檻下修到 $52；若同時毛利率連四季年減，改為迴避"],"evidence_refs":[]},{"axis":"減碼與清倉指標由空白改為設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定減碼、清倉指標（空白）","side_b":"本次設五條：毛利率連四季年減 ≥50bp；IOS 核心成長連兩季低於 3%；FY2027 指引中點低於 $3.31；總債務對 EBITDA 超過 3.0 倍；FY2027 AHS 利潤率沒有擴張。若已建倉，前兩條任一觸發就減碼一半，三條以上同時觸發就清倉","ruling":"前份第一風險已被 Q3 證據解除，改由毛利率指標接手；其餘指標對應本次各項風險","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 $58 以下：重跑判斷，評估進場首倉","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤$58","action":"重跑判斷，通過則首倉 2%","source_freq":"每日收盤","date":null},{"n":2,"text":"FY2028 共識 EPS 升到 $3.70 以上：現價下 PEG 回到約 2.0，重跑判斷","type":"估值rearm","maps_to":"H1","metric":"FY2028 共識調整後 EPS","threshold":"≥$3.70","action":"重跑判斷","source_freq":"每月共識快照","date":null},{"n":3,"text":"FY2027 全年指引：調整後 EPS 中點低於 $3.31，或核心成長指引低於 3%","type":"Single Thing","maps_to":"single_thing","metric":"FY2027 調整後 EPS 指引中點與核心成長指引","threshold":"<$3.31 或 <3%","action":"價格門檻下修到 $52；若同時毛利率連四季年減，改為迴避","source_freq":"Q4 財報（每年一次）","date":"2027-02"},{"n":4,"text":"FY2027 指引中點 ≥$3.45 且核心成長指引 ≥4%：加速得到確認","type":"假設驗證","maps_to":"H1","metric":"FY2027 調整後 EPS 指引中點與核心成長指引","threshold":"≥$3.45 且 ≥4%","action":"股價在 $67 以下時首倉 2%","source_freq":"Q4 財報（每年一次）","date":"2027-02"},{"n":5,"text":"調整後毛利率在 FY2026 Q4 與 FY2027 Q1 仍年減 50bp 以上：組合歸因證偽","type":"風險","maps_to":"R1","metric":"調整後毛利率年變化","threshold":"連四季年減 ≥50bp","action":"長期信心降為低；若已持有，減碼一半","source_freq":"每季財報","date":"2027-04","evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"FY2027 AHS 調整後 EBITDA 利潤率沒有擴張，或 AHS 價格貢獻低於 100bp","type":"風險","maps_to":"R2","metric":"AHS 調整後 EBITDA 利潤率、AHS 價格貢獻","threshold":"利潤率擴張 <100bp 或價格貢獻 <100bp","action":"AHS 改按低成長資產估值，基準 EPS 下修約 3%","source_freq":"每季財報","date":"2028-02","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"n":7,"text":"價格成本差轉負，或新關稅使調整後毛利率年減超過 100bp","type":"風險","maps_to":"R3","metric":"價格成本差、調整後毛利率年變化","threshold":"轉負或年減 >100bp","action":"停止建倉計畫；若已持有，減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":8,"text":"IOS 核心成長連兩季低於 3%，或 Fluke 訂單出貨比低於 1：景氣回頭","type":"風險","maps_to":"R4","metric":"IOS 核心成長、Fluke 訂單出貨比","threshold":"連兩季 <3% 或 <1","action":"基準機率下調 10 個百分點，轉入悲觀；若已持有，減碼一半","source_freq":"每季財報","date":null},{"n":9,"text":"單筆併購超過 10 億美元，或槓桿超過 3.0 倍","type":"風險","maps_to":"R5","metric":"單筆併購金額、總債務對調整後 EBITDA","threshold":">10 億美元或 >3.0 倍","action":"重跑判斷，期間停止建倉計畫","source_freq":"8-K 與每季法說","date":null},{"n":10,"text":"FY2026 Q4 財報與 FY2027 指引公布後複審","type":"複審日期","maps_to":null,"metric":"全份判斷","threshold":"公布後一週內","action":"重跑判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"調整後毛利率年變化","bear_threshold":"連四季年減 ≥50bp","window":"FY2026 Q2–FY2027 Q1","source":"季度財報新聞稿與法說","last_status":"warning"},{"metric":"IOS 核心營收成長","bear_threshold":"連兩季低於 3%","window":"至 FY2027 Q4","source":"季度財報新聞稿","last_status":"ok"},{"metric":"FY2027 調整後 EPS 指引中點","bear_threshold":"低於 $3.31（現行共識）","window":"2027 年 2 月公布","source":"Q4 財報新聞稿","last_status":"unknown"},{"metric":"總債務對調整後 EBITDA","bear_threshold":"超過 3.0 倍（政策區間約 2.5 倍）","window":"每季","source":"季度法說","last_status":"ok"},{"metric":"AHS 調整後 EBITDA 利潤率","bear_threshold":"FY2027 比 FY2026 擴張不到 100bp","window":"FY2027 全年","source":"季度財報新聞稿","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"價 ≤$58（PEG 約 2.0、五年基準年化約 8.5%）或 FY2028 共識 EPS ≥$3.70（現價下 PEG 約 2.0）；任一成立即重跑判斷","exec_line":"目前未持有。兩項條件任一成立，先重跑判斷，通過才首倉 2%；FY2027 指引中點 ≥$3.45、且毛利率年減收窄後，再加到 4%。股價先漲過 $75 而指引沒有跟上，就不追","holding_cap":"≤4%（最大回撤估 −30%～−45%；論點沒受損時，不因波動減碼）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 $58 以下（前瞻約 18.6 倍、PEG 約 2.0）；或 2027 年 2 月 FY2027 指引中點 ≥$3.45，且帶動 FY2028 共識 EPS 升到 $3.70 以上","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=11.96, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"有機加速是結構性的：靠創新、資料中心與國防的業務擴編、經常性收入，讓核心成長維持在投資人日框架（3–4%）之上，不只是單一景氣年","2y":"FY2027 核心成長 ≥4.5%，IOS ≥5%，Fluke 訂單出貨比大於 1","5y":null,"10y":null,"threshold":"FY2027 全年核心成長 ≥4.5%","source":"季度財報新聞稿與法說：核心成長分部拆解、Fluke 訂單評論、全年指引","drift_rule":"TTM 核心成長連 2 季低於門檻 5% 以上（<4.3%）＝削弱；連 3 季低於門檻 10% 以上（<4.05%）＝反轉"},{"id":"H2","text":"毛利率守得住，利潤率靠營運槓桿擴張：調整後 EBITDA 利潤率每年擴張 50–100bp，毛利率的年減只是組合效應","2y":null,"5y":"FY2030 調整後 EBITDA 利潤率比 FY2026 高 200bp 以上，調整後毛利率守在 62% 以上","10y":null,"threshold":"調整後 EBITDA 利潤率每年擴張 ≥50bp；調整後毛利率年減 ≤50bp，且不連四季年減","source":"財報新聞稿的分部調整後 EBITDA 與毛利率、法說的價格成本評論","drift_rule":"連 4 季 TTM 利潤率擴張不到 50bp，或毛利率連 4 季年減＝削弱；連 6 季＝反轉"},{"id":"H3","text":"資本配置維持每股複利：以自由現金流回購為主，每年淨減股 3% 以上；併購只做補強，槓桿留在約 2.5 倍","2y":null,"5y":"FY2030 稀釋股數比 FY2026 Q3 的 3.02 億股減少 12% 以上，總債務對調整後 EBITDA ≤2.8 倍","10y":null,"threshold":"年度淨減股 ≥3%；單筆併購低於 10 億美元（約市值 5%）；槓桿 ≤2.8 倍","source":"10-Q 與 10-K 的稀釋股數、法說的槓桿揭露、8-K 併購公告","drift_rule":"連 4 季年化淨減股低於門檻 5% 以上（<2.85%）＝削弱；連 6 季低於門檻 10% 以上（<2.7%），或出現超過 10 億美元的併購＝反轉"}],"R":[{"id":"R1","text":"毛利率年減從組合效應變成結構性：Q2 調整後毛利率年減 100bp、Q3 年減 80bp，電子零件與運費通膨上升；管理層歸因於 ServiceChannel 代收代付合約與新興市場耗材的組合","h_ref":"H2","clock":"⚡","threshold":"FY2026 Q4 與 FY2027 Q1 調整後毛利率仍年減 ≥50bp，即組合歸因證偽","evidence_refs":["competitive_share_entrants#1"]},{"id":"R2","text":"競爭與技術替代侵蝕定價力：10-K 自述低成本製造地區的新進者增加、可能被迫降價、技術更迭快。AHS 利潤率多年持平，今年分部 EBITDA 年減 5%；管理層稱是限期投資，但也可能是守住成長所需的常態成本","h_ref":"H2","clock":"🔥","threshold":"FY2027 AHS 調整後 EBITDA 利潤率比 FY2026 擴張不到 100bp，或 AHS 價格貢獻低於 100bp","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"id":"R3","text":"關稅與中美貿易政策：約 44% 營收在美國以外，2025 年成長有一部分是轉嫁關稅的漲價。IEEPA 被判無效後，政府改用其他授權課徵新關稅；退款屬一次性，公司已排除在調整後盈餘之外","h_ref":"H2","clock":"🔥","threshold":"價格成本差轉負，或因新關稅使調整後毛利率年減超過 100bp","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"景氣循環回頭：Q3 法說 CEO 承認部分終端市場今年特別強，Q4 又少 4 個銷售日；工業景氣轉弱時，IOS 核心成長會回到 0–2%","h_ref":"H1","clock":"🔥","threshold":"IOS 核心成長連 2 季低於 3%，或 Fluke 訂單出貨比低於 1","evidence_refs":[]},{"id":"R5","text":"資本配置轉向較大的併購：Q3 法說（2026-10-28）CFO 說希望併購占更大比重、併購團隊已重整；股價上漲後，回購的報酬下降。Q2 法說（2026-07-29）時 CEO 還說併購偏硬體、軟體路徑很窄","h_ref":"H3","clock":"🐢","threshold":"單筆併購超過 10 億美元，或總債務對調整後 EBITDA 超過 3.0 倍","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月公布的 FY2027 全年指引：調整後 EPS 中點低於 $3.31（現行共識），或核心成長指引低於 3%。這等於承認今年 5% 以上的加速主要是景氣","why_fatal":"現價 21.5 倍前瞻本益比的前提，是加速可以延續。指引若退回框架下緣，倍數會被拉回 17–18 倍，對應股價約 $54–60（−11%～−19%）；股價下跌也會削弱回購對每股盈餘的墊高效果，盈餘與倍數兩頭一起縮","if_happens":"維持不進場，價格門檻下修到 $52；若同時毛利率連四季年減，改為迴避","how_monitor":"看 2027 年 2 月的 Q4 財報與全年指引；在那之前，以每季 Fluke 訂單出貨比、IOS 核心成長、歐洲與北美經銷商出貨評論作為前導","probability":"25%。依據：FY2026 Q4 有 4 個銷售日的逆風，管理層也承認部分市場今年特別強；但指引已連兩季上調，Fluke 訂單仍在加速"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":20.27,"peg_fy2":2.97,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":2.71,"FY2026E":3.12,"FY2027E":3.31,"FY2028E":3.56},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（非 GAAP，排除收購無形資產攤銷與 IEEPA 關稅退款）。FY2026E 至 FY2028E 取 2026-10-31 的 Koyfin 共識快照，家數未載；另有追蹤站顯示 FY2026 EPS 有 19 位分析師。FY2025A 事實表沒有直接收錄，由 Q3 法說「FY2026 指引中點年增略高於 15%」反推：3.12÷1.15，約 2.71"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 FY2027 全年指引","impact":"高","watch":"EPS 指引中點對 $3.31 共識、核心成長指引、調整後毛利率年變化"},{"date":"2027-04","date_precision":"month","type":"other","event":"FY2027 Q1 財報：毛利率連四季年減的檢驗點","impact":"中","watch":"調整後毛利率年減是否收窄到 30bp 以下、AHS 利潤率"},{"date":null,"date_precision":null,"type":"macro","event":"美國以其他授權重新課徵關稅，或中美貿易政策變動","impact":"中","watch":"價格成本差、毛利率年減幅度"}]}
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
