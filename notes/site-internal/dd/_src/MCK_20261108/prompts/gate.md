你是 DD 管線 v20 的判斷層閘（gate），標的 MCK（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝110957 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：新聞媒體稱營收低於共識（finanzen.net，未取得數字，待核）
- `f_kpi1_non_gaap_adjusted_operat`（q1_business）｜Non-GAAP (adjusted) operating profit＝1852 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin（推算＝1,852÷110,957）＝1.67 %｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（利益率為自行以公布數字推算）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_kpi8_operating_segment_revenu`（q1_business）｜Operating segment revenue: Oncology & Multispecialty＝14980 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_kpi6_adjusted_eps`（q1_business）｜Adjusted EPS＝11.68 USD｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：媒體稱優於共識（finanzen.net，未取得數字，待核）
- `f_peer_mck_gross_margin_pct`（q2_moat）｜MCK 毛利率＝3.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_operating_margin_pct`（q2_moat）｜MCK 營業利益率＝1.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_fcf_margin_pct`（q2_moat）｜MCK FCF 利潤率＝1.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_gross_margin_pct`（q2_moat）｜CAH 毛利率＝3.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_operating_margin_pct`（q2_moat）｜CAH 營業利益率＝1.26 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_fcf_margin_pct`（q2_moat）｜CAH FCF 利潤率＝1.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
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
- `f_peer_hsic_operating_margin_pct`（q2_moat）｜HSIC 營業利益率＝5.79 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HSIC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝44.66 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝50.63 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝57.72 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_kpi7_guidance_fy2027_adjusted`（q1_business）｜Guidance: FY2027 adjusted EPS（上修）＝45.60–46.40 USD｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：consensus_revision fy1 = 44.66（財報前快照，已落在新區間之下）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝434899.73 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝464859.08 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝115.46 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_free_cash_flow`（q1_business）｜Free cash flow（單季）＝2947 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝4674.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 11202.0、現金 6528.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.321 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝127155.04 USD m｜期間與口徑：2026-11-08／市值 122481.04 ＋ 淨負債 4674.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1060.84 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝23.75 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 44.66，分子＝快照價 1060.84｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝27.36 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝44.43 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.09 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 44.62 → 44.66（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_w52`（q5_valuation）｜52 週均線＝860.18 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝767.33 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝562.73 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（18 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：越來越多新競爭進入者在資料分析、機器學習、AI 等技術上比公司更有經驗。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-08）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：MCK FY2026 10-K：最大客戶 CVS 占營收約 24%、應收約 21%；前十大客戶占約 73%；與 CVS 的配銷合作已延至 2027 年 6 月。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素：客戶可能減少採購或不續約，單一或多個大客戶減量、不續約可能對業務造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-08）｜affects：thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 前十大客戶占營收約73%、占應收約43%；最大客戶CVS占營收約24%、占應收約21%；次兩大客戶各占11%與10%。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 自述銷售與信用集中度顯著，單一大客戶重大違約、減量或流失可能對財務、營運與流動性造成重大不利影響；與CVS合約延至2027年6月。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：IRA drug price cuts pricing pressure expected to persist through FY27
  - 來源：Chartmill/Zacks, Retain McKesson Stock（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：McKesson FY2026 10-K 風險因子列明政府行動（含貿易制裁、關稅與其他貿易限制）可造成供應中斷，且替代貨源不一定完全成功，可能面臨延遲或較高採購成本；並稱貿易環境仍高度動態且不確定。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：報導稱學名藥分階段關稅政策可能對三大美國藥品經銷商產生重大影響（McKesson 為其一屬搜尋結果推論，來源是否明指待核）。
  - 來源：FreightWaves（as_of 2026-07-22）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：MCK FY2024 10-K 風險因素列舉供應中斷成因，含供應商財務困難、天災、內亂或戰爭、流行病；曾因供應商無法交貨受影響（搜尋摘要轉述，未讀原頁）
  - 來源：McKesson Form 10-K FY2024 (SEC)（as_of 2024-05-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：產業層級：美國學名藥 API 設施逾 92% 在海外（主要印度、中國、義大利）；MCK 為連接印中製造商與美國通路的三大經銷商之一；學名藥關稅報導計畫 2028 起（尚非定案）。未見 MCK 自身對關稅或地緣曝險的揭露（搜尋摘要轉述）
  - 來源：FreightWaves / PharmExec (2026-07-22)（as_of 2026-07-22）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：WAC下降部分抵銷處方量成長；公司預期FY27定價逆風延續
  - 來源：McKesson Form 10-Q (period 2026-09-30)（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素揭露：競爭對手包含製造商直銷、第三方物流與大型付款方，客戶或製造商可能自建供應管理能力取代 MCK 服務；也可能面對更快採用新興技術的公司。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-05-08）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：第三方分析稱製造商直銷模式是中期較可信的威脅，AI 降低藥廠自建專科藥 hub 服務的營運負擔；Prescription Technology Solutions 為最可能被 AI 顛覆的部門（低可信度來源）。
  - 來源：pitchgrade: mckesson ai margin pressure（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：產業文章稱 2026 年中品牌平台處方占比上升，顯示直接面向病患通路遷移（廠商視角），未量化對批發商影響。
  - 來源：Pharmaceutical Commerce, Mid-year check-in: how direct-to-patient momentum is accelerating（as_of 2026-07-29）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：FY2026 10-K 揭露 McKesson 仍為數百件鴉片類私人原告案件被告，並有 Omni Healthcare qui tam（False Claims Act）案。
  - 來源：SEC EDGAR 10-K FY2026 Item 8 Note 17（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：FDA 執法紀錄顯示 McKesson 為 UDENYCA 預充填針劑 Class I 藥品召回（D-0353-2026）的召回廠，2026-01-16 啟動，116 箱，原因為儲存不當。摘要未提供可逐字複製原文。
  - 來源：FDA recall D-0353-2026（ai-analytics.org 彙整）（as_of 2026-01-16）｜affects：thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 揭露仍有數百件鴉片類私人原告訴訟；與其他兩家經銷商已與急性照護醫院及部分第三方付款人達成集體和解。搜尋未見近12個月新的證券集體訴訟（2018 年案已於 2022 年達成保險全額涵蓋之和解原則）。
  - 來源：SEC EDGAR 10-K FY2026 Item 8（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：McKesson 為 UDENYCA Class I 召回（D-0353-2026）召回廠，2026-01-16 啟動，116 箱，儲存不當。查無 2026 年新警告信（前次為 2019 DSCSA、2024 年針筒相關）。
  - 來源：FDA recall D-0353-2026（ai-analytics.org 彙整）（as_of 2026-01-16）｜affects：thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":2316.0,"bear_5y_price":700.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":50.8,"ev5y_pct":42.2,"irr_base_pct":8.6,"asym_ratio":2.9,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":46.0,"pe":23.06,"basis":"FY1 口徑：FY27 財測中點 46 美元，取代已過時的財報前共識 44.66 美元；終端倍數同為前瞻一年口徑。"},"eps":{"bull":[54.5,63.5,73.5,84.5,96.5],"base":[52.0,58.5,65.5,72.5,80.0],"bear":[47.0,45.5,46.0,48.0,50.0]},"pe":{"bull":24,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.321,"net_buyback":3.0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MCK_Q1_2027_Earnings_Call_20260805.md
- 2026-08-05｜Brian Tyler｜guidance：FY27 調整後 EPS 財測上調至 $44.20–45.00（原話："guidance to $44.20 to $45.00 from the prior range of"）
- 2026-08-05｜Kenny Cheung｜guidance：財測隱含調整後 EPS 成長（排除挪威出售與 USON 股權出售利得）（原話："It implies adjusted EPS growth of 13%"）
- 2026-08-05｜Kenny Cheung｜guidance：FY27 營收與營業利益成長財測（原話："5% to 9% and operating profit growth of 9% to 13%."）
- 2026-08-05｜Kenny Cheung｜guidance：北美藥品批發營業利益成長落在原區間高端（原話："growth at the high end of the previous range"）
- 2026-08-05｜Kenny Cheung｜guidance：腫瘤與多專科營收財測維持不變（原話："We continue to anticipate revenue growth of 14.5% to 18.5%"）
- 2026-08-05｜Kenny Cheung｜guidance：RxTS 營收成長財測（原話："revenue to increase by 2.5% to 6.5%"）
- 2026-08-05｜Kenny Cheung｜guidance：MedSurg 營收成長財測（原話："We anticipate revenue growth of 1% to 6%"）
- 2026-08-05｜Kenny Cheung｜guidance：利息費用財測（原話："interest expense to be in the range of $380 million to"）
- 2026-08-05｜Kenny Cheung｜guidance：全年稅率財測較前次略升（原話："a slight increase from the prior guidance range"）
- 2026-08-05｜Kenny Cheung｜guidance：FY27 自由現金流財測（原話："cash flow of approximately $4.5 billion to $4.9 billion"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：FY27 回購約 $50 億，Q1 已完成 $25 億（原話："of which $2.5 billion was completed in the first quarter."）
- 2026-08-05｜Kenny Cheung｜capital_allocation：加權平均稀釋股數財測（原話："range of 115.5 million to 117.5 million."）
- 2026-08-05｜Kenny Cheung｜capital_allocation：董事會批准股息調升 15%（原話："approved a 15% increase to our quarterly dividend"）
- 2026-08-05｜Kenny Cheung｜commitment：管理層承諾股息成長與長期獲利成長目標相稱（原話："committed to dividend growth that is commensurate with"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：資本配置優先順序宣稱不變（原話："We remain focused on investing in our strategic priorities"）
- 2026-08-05｜Kenny Cheung｜commitment：新任 CFO 說明其角色標準：say-do ratio（原話："maintain what I call a strong say-do ratio"）
- 2026-08-05｜Kenny Cheung｜margin：NAP 品牌藥 WAC 下降影響營收但對營業利益無顯著影響（原話："they did not have a meaningful impact on operating profit"）
- 2026-08-05｜Kenny Cheung｜margin：品牌藥 95% 以上為服務費模式（口徑說明）（原話："more than 95% of our branded drugs are fee-for-service"）
- 2026-08-05｜Kenny Cheung｜margin：營業費用占毛利比率年減約 150bp（原話："gross profit improved by approximately 150 basis points"）
- 2026-08-05｜Kenny Cheung｜margin：NAP 營業利益成長快於營收（利潤率結構）（原話："AOP did grow faster than revenue"）
- 2026-08-05｜Kenny Cheung｜margin：管理層列出 NAP 利潤率變動的驅動因素（原話："operating margin changes in the segment can be driven by"）
- 2026-08-05｜Kenny Cheung｜product：GLP-1 配送營收 $150 億（原話："GLP-1 medications distribution were $15 billion in the"）
- 2026-08-05｜Kenny Cheung｜guidance：GLP-1 全年持續成長但單季有波動（原話："with quarter-to-quarter variability."）
- 2026-08-05｜Brian Tyler｜product：7 月起支援 CMS Medicare GLP-1 Bridge 計畫（原話："began supporting the CMS Medicare GLP-1 Bridge program"）
- 2026-08-05｜Brian Tyler｜customer：GLP-1 承保面的討論未明顯移動（原話："it really hasn't moved super significantly"）
- 2026-08-05｜Kenny Cheung｜guidance：管理層稱財測為平衡觀點、非最佳情境（原話："a balanced view of the year, not a best case scenario"）
- 2026-08-05｜Kenny Cheung｜guidance：財測較前次中點高 $0.40（原話："the reason why we guided $0.40 above the last"）
- 2026-08-05｜Kenny Cheung｜guidance：6 月為當季最強月份（原話："June was the strongest month of the quarter."）
- 2026-08-05｜Brian Tyler｜risk：學名藥有利因素提前到本年初，以後續季度為代價（原話："That obviously will come at the expense of later quarters"）
- 2026-08-05｜Brian Tyler｜risk：學名藥有利因素提前出現（原話："favorability in the generics portion of the business"）
- 2026-08-05｜Kenny Cheung｜guidance：下半年加速投資（成長與 AI）已納入 NAP 財測（原話："focused on growth and also AI"）
- 2026-08-05｜Kenny Cheung｜commitment：管理層稱投資報酬時點最可能在 2028 年初（原話："return timing will most likely be the beginning of 2028"）
- 2026-08-05｜Kenny Cheung｜margin：O&M 排除 Core Ventures 後營業利益成長口徑（逐字稿記為 50%，與他處 15% 不同）（原話："roughly 50%, which is in line with the long-term targets"）
- 2026-08-05｜Brian Tyler｜customer：Florida Cancer 整合表現（原話："we are on the high end of the guidance range"）
- 2026-08-05｜Brian Tyler｜capital_allocation：不預期有 FCS 規模的併購，但有小型併購（原話："opportunities for kind of the scale of adding additional FCS"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Kenny 稱會有一些 tuck-in 併購（原話："there will be some M&A along the way,"）
- 2026-08-05｜Brian Tyler｜product：AI 工具被視為擴大醫師看診量的成長動能（原話："expand our capacity to see patients"）
- 2026-08-05｜Brian Tyler｜risk：340B 改革：提案仍在評論期，現在談財務影響言之過早（原話："premature to speculate on the financial impact"）
- 2026-08-05｜Brian Tyler｜risk：IRA Part D 不確定性：MFP 水準未知（原話："We don't know what the MFP will be."）
- 2026-08-05｜Brian Tyler｜risk：IRA Part D 生效時點（原話："until January of 2028"）
- 2026-08-05｜Brian Tyler｜risk：GLOBE 示範計畫對診所無影響的說明（原話："with no impact on the provider practice itself"）
- 2026-08-05｜Brian Tyler｜capital_allocation：MedSurg 將更名 Wellverse（原話："formally operating as Wellverse starting in January 2027"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Apollo 持有 MedSurg 約 13% 少數股權（原話："Apollo Funds, which now holds approximately 13% minority"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：ASR 初始平均價格（原話："initial average price of approximately $755 per share"）
- 2026-08-05｜Kenny Cheung｜margin：MedSurg 營業利益年減 20%（原話："decreased 20% to $195 million, driven by product mix"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Q1 自由現金流為負（原話："We had negative free cash flow of $372 million"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：近 12 個月自由現金流（原話："free cash flow remained strong at approximately $6.1 billion"）
- 2026-08-05｜Kenny Cheung｜guidance：FCF 財測維持不變、未上調（原話："sticking with the current guide"）
- 2026-08-05｜Kenny Cheung｜guidance：管理層稱營運資金改善有機會優於財測（原話："opportunities along the way to beat that off"）
- 2026-08-05｜Kenny Cheung｜guidance：季度節奏：Q4 為最大季（原話："Q4 will be the biggest quarter for us"）
- 2026-08-05｜Kenny Cheung｜guidance：Q2 對比去年 $51M 出售股權利得（原話："lapping prior year gains of $51 million"）

### 問答異常語氣（迴避／改口／保留）
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Kevin Caliendo 追問自由現金流兩年來成長落後獲利、何時加速｜答法：未給具體加速時點或數字，回答維持原財測並稱「More to come on this one」，改談 Q1 較去年改善與營運資金結構性改善
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Michael Cherny 追問 NAP 下半年比較基期與路徑｜答法：Brian 提到學名藥有利因素提前、將以後續季度為代價；Kenny 轉談新產品時點與下半年加速投資，未給下半年季度數字
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Lisa Gill 追問 340B 變動對北美業務影響｜答法：管理層稱提案仍在評論期、推測財務影響言之過早，未給數字
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Kenny 回答 Elizabeth Anderson 時稱 O&M 排除 Core Ventures 後營業利益成長約 50%｜答法：該數字與準備稿的約 15% 不一致，後續 Kenny 亦稱「The 15% growth I mentioned earlier」；原稿未更正

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 3 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 1 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"A 核心候選 / 觀望偏進場（pullback 中）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"U.S. Pharmaceutical 段保持 11-13% Rev CAGR + Pharma OI margin ≥ 1.4%","columns":{"2Y 驗證":"FY27 全年 Rev +12% + Pharma OI margin ≥ 1.4%","5Y 驗證":"FY30 Rev $590B + Pharma OI margin 1.5-1.6%","10Y 驗證":"FY32+ 維持市佔 41-43%","具體數字門檻":"季 Rev YoY ≥ 10%；季 Pharma OI margin ≥ 1.4%","信息來源":"MCK FY26 10-K + mgmt FY27 guide","漂移觸發":"連 2 季 Pharma Rev YoY &lt; 8% → 削弱"}},{"id":"H2","text":"Oncology & Multispecialty + Specialty Solutions 段保持 +20-25% Rev YoY + OP margin ≥ 3%","columns":{"2Y 驗證":"FY27 全年 Oncology Rev +25% + OP margin ≥ 3.5%","5Y 驗證":"FY30 Oncology Rev $60B + OP margin 4-5%","10Y 驗證":"FY32+ MSO 平台 physicians ≥ 5,000","具體數字門檻":"季 Oncology YoY ≥ 20%；OP margin ≥ 3%","信息來源":"MCK 2025 investor day + FY26 Q4 update","漂移觸發":"連 2 季 Oncology YoY &lt; 15% → 削弱；OP margin &lt; 2.5% → 反轉"}},{"id":"H3","text":"MedSurg 分拆 2027 完成 + spinco 創造 unlock value（MCK 估值 multiple 維持或擴張）","columns":{"2Y 驗證":"2027 MedSurg spin-off / split-off 完成 + Apollo $1.25B 退場 / 轉換","5Y 驗證":"分拆後 MCK + spinco 合計市值 &gt; 當前 $95B + 25%","10Y 驗證":"分拆後 MCK 獨立 Pharma + Specialty 報表清晰，multiple expansion 至 20x","具體數字門檻":"2027-06 前完成 spin；spinco IPO 或合約完成","信息來源":"MCK Q1 FY26 announcement + Apollo deal 2026-04-20","漂移觸發":"分拆延後 6+ 個月 → 警戒；分拆放棄 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"MedSurg 分拆執行失敗或大幅延後","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"SEC 8-K + 公司 announcement + Apollo 出場條件","警戒閾值":"分拆延後 6 個月以上 OR Apollo 公開退出 OR financial restatement → 立即重評"}},{"id":"R2","text":"OptumRx 大單反向流失或 in-house in-house","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"季財報 segment 細節 + Optum / UNH 公開合約 disclosure","警戒閾值":"OptumRx 合約變動公告 → 立即重評；MCK 大客戶 disclosure 變化 → 警戒"}},{"id":"R3","text":"Direct-to-pharmacy / Lilly Direct 類模式擴大壓 distributor margin","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Lilly / Pfizer / Novo Direct 業務 disclosure；GLP-1 distribution 模式變化","警戒閾值":"連 4 季 Specialty Rx margin 下滑超 50bp → 結構性壓力；direct 模式占 GLP-1 30%+ → thesis 部分推翻"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"🟢","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":766.08,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MCK","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"McKesson Corporation"},"oneliner":"配送三強中營益率最高，專科藥與營運槓桿推動 FY27 調整後 EPS 年增 17–19%；但 26 週股價漲 44%，多數來自倍數由約 17 倍升到 23 倍。現價要賺年化 12%，五年 EPS 需年化約 15%，生意好，價格等回到 920 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/scenario.json","answers":{"q1_business":{"verdict":"McKesson 賺的是藥廠與下游藥局之間的配送服務費，以及專科藥附加服務的錢。營收八成在北美藥品配送，獲利增量愈來愈靠專科藥、腫瘤網絡與藥品可及性服務。","reasoning":"FY27 第二季營收 1,109.57 億美元，調整後營業利益 18.52 億美元，營益率 1.67%，毛利約 39 億美元，毛利率約 3.5%。北美藥品營收 914 億美元，營業利益由合併數回推約 10.4 億美元，利益率約 1.14%，占分部營業利益約 52%。腫瘤與多專科營收 149.8 億美元、營業利益 4.27 億美元，利益率 2.85%，占約 21%。處方科技營收 15 億美元、營業利益 3.07 億美元，占營收 1.4%，卻占分部營業利益約 15%。醫材營收 31 億美元、營業利益 2.25 億美元，占約 11%。錢卡在兩個節點：品牌藥九成五以上按服務費收取（2026-08-05 Kenny Cheung），所以 2026 年 1 月 WAC 下降使北美藥品營收成長少約 4 個百分點，營業利益沒有重大影響；專科藥通路與診所網絡的利益率則高於基礎配送。⚑單點依賴：CVS 占營收約 24%，次兩大客戶占 11% 與 10%，前十大約 73%。CVS 續約到 2032 年 6 月，管理層 2026-11-04 確認已計入財測，短期續約風險解除，集中度本身沒有變。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_adjusted_operat","f_kpi2_non_gaap_operating_margi","f_kpi8_operating_segment_revenu","f_kpi6_adjusted_eps","f_peer_mck_gross_margin_pct"],"verdict_values":{"revenue_quality":"營收多為藥價轉手，品質要看毛利與營業利益。GLP-1 單季配送營收約 160 億美元（年增 26%）稀釋毛利率，FY23 到 FY26 毛利率由 4.47% 降到 3.61%，同期營益率僅由 1.66% 微降到 1.60%，TTM 回到 1.67%。","unit_econ_note":"單位經濟看每張處方的服務費與費用效率。第二季營業費用占毛利比率年改善約 141 個基點。單一客戶與單一藥品的利潤率事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"低毛利、需求跟處方量走，靠營運槓桿與回購把個位數營收成長放大成雙位數 EPS 成長。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：處方量穩定成長，專科新藥推動需求，同店就診人次為近幾季高點（2026-11-04 逐字稿）。GLP-1 單季有波動，配送供給由三家寡占，可逆性低。","bargaining":{"up":"品牌藥以服務費為主，藥廠有直連通路可選，目前規模未見量化。","down":"前十大客戶占營收約 73%，議價權偏客戶；CVS 同時與 Cardinal 延約到 2032 年。","geo":"海外約占營收 4%，風險集中在學名藥上游原料依賴海外與關稅。"},"profit_pool_dir":"公司內部利潤往專科藥、腫瘤網絡與可及性服務移動；產業五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表沒有市場規模、滲透率與五年利潤池占比，本輪不補，成長判斷改靠分部實績與公司財測。"}}}},"q2_moat":{"verdict":"護城河方向持平，等級 B：規模與服務可靠度鎖住三強地位，定價權受大客戶集中限制。","reasoning":"機制是全國配送網的規模成本，加上腫瘤網絡與嵌入開立處方流程的連線，支付方網絡涵蓋美國 96% 處方量。可證方向：MCK 營益率 1.67%，高於 Cencora 1.44% 與 Cardinal 1.26%；毛利率 3.67% 卻是三家最低，優勢來自費用效率，定價沒有優勢。第二季北美藥品營業利益年增 22%，營收年增 6%。同業 ROIC 與市占事實表未涵蓋，無法驗證差距是否擴大，所以不標擴大。反方向的可能：若三家的利益率差距只是專科組合的時間差，優勢可能比數字看起來窄。","fact_refs":["f_peer_mck_gross_margin_pct","f_peer_mck_operating_margin_pct","f_peer_mck_fcf_margin_pct","f_peer_cah_gross_margin_pct","f_peer_cah_operating_margin_pct","f_peer_cah_fcf_margin_pct","f_peer_cor_gross_margin_pct","f_peer_cor_operating_margin_pct","f_peer_cor_fcf_margin_pct","f_peer_hsic_gross_margin_pct","f_peer_hsic_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"全國藥品配送規模與服務可靠度，加上社區腫瘤網絡與處方流程連線形成的轉換成本。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營益率在三強最高，第二季營運槓桿延續；CVS 維持與 Cardinal 雙供應，份額方向無資料，直連通路尚未量化，兩邊都不足以改變方向。","competitor_notes":[{"name":"Cencora","strategy_note":"毛利率三家最高，FCF 利潤率最低，專科與藥廠服務是最直接的對手，現金落差是否一次性事實表未涵蓋。"},{"name":"Cardinal Health","strategy_note":"營益率三家最低，FCF 利潤率高於 MCK，同樣拿到 CVS 延約，是 CVS 雙供應的另一端。"},{"name":"Henry Schein","strategy_note":"牙科與醫材通路，毛利結構不同，只能當醫材分拆後的參考，不能當藥品配送的基準。"}],"peer_na_reason":"同業 ROIC、市占與投入資本事實表未涵蓋，本輪只能比較利潤率，不判斷報酬率差距。","threats":[{"level":"🟡","text":"藥廠直連病患平台把部分處方移出批發通路。目前只有產業文章，未量化對批發商的影響；同期 GLP-1 配送營收仍年增 26%。","p":"30%","evidence_refs":["channel_business_model_shift#2","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"10-K 自承部分對手與新進者在資料分析與 AI 上經驗更多。受影響的是處方科技段，實體配送不受影響。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"level":"🟡","text":"大型連鎖、付款方或藥廠自建供應管理能力，取代部分配送服務。","p":"15%","evidence_refs":["substitute_technology#0","customer_second_source#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"用藥屬必需，使用者、開立者與付款者三方都成立。第二季處方量成長，腫瘤網絡同店就診人次為近幾季高點。"},{"item":"決策層級","level":"🟡","text":"決策單位是連鎖與醫療體系的整約，前十大客戶占營收約 73%。合約長達數年，轉換成本高，但 CVS 同時用兩家供應商，替代性在合約層真實存在。"},{"item":"價值鏈分配","level":"🟡","text":"配送只拿約 3.7% 毛利，品牌藥服務費與 WAC 下降脫鉤的情況已維持兩季。藥廠直連與下游議價是兩端的壓力，專科段拿到的比例較高。"},{"item":"社會容忍度","level":"🟡","text":"藥價、透明度與 340B 仍是國會議題，FTC 與 HHS 2024 年曾就批發商對學名藥短缺的影響徵詢意見，之後無進一步行動。配送營益率僅 1.67%，並非政治焦點的主要利潤池，鴉片訴訟則顯示社會責任成本存在。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"投入資本、折舊與營運資金變動都未收錄，當期 ROIC、增量報酬與內生成長上界無法計算，不估。象限依 1.67% 營益率與配送業性質判斷，周轉率未計算。唯一可見的增量報酬是管理層對 Precision Medicine 的預估：22.5 億美元換第三年底每股增益 1.60–1.80 美元，以 116.5 百萬股計，稅後約 8.8%，含綜效、尚未實現。"}}}},"q3_growth":{"verdict":"五年後跑道中等：核心配送成熟，腫瘤與專科是看得到的第二曲線，但有機成長未拆出，也沒有滲透率資料。","reasoning":"FY26 調整後 EPS 約 38.98 美元，由 FY27 財測 45.60–46.40 美元與年增 17–19% 回推；到 FY29 共識 57.72 美元，三年年化約 14.0%。這組共識是財報前快照，FY1 的 44.66 美元已低於新財測下緣。共識營收 FY26 到 FY28 年化約 7.3%，EPS 比營收快約 6.7 個百分點。落差歸因：淨回購每年約 3–4 個百分點（第二季稀釋股數年減 6%，FY27 回購約 50 億美元，約占市值 4.1%）；PMG 第三年底 1.60–1.80 美元的增益，折合每年約 1 個百分點；其餘約 2–3 個百分點來自營業利益率擴張。現價回購每一美元買到的股數，比上半年均價 818 美元時少約 23%，這部分成長會降速。FY27 腫瘤段財測由營收 14.5–18.5% 上調到 20–24%，其中 PMG 貢獻未揭露。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_guidance_fy2027_adjusted","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"營收成長（量與專科組合）約 7 個百分點，淨回購約 3–4 個百分點，併購約 1 個百分點，營業利益率擴張約 2–3 個百分點。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊與營運資金變動事實表未涵蓋，內生上界無法計算。保守處理為共識成長超出內生上界，因為 EPS 成長中至少 3–4 個百分點來自回購，不屬於營運再投資。","segments":[{"item":"北美藥品","value":"第二季營收 914 億美元，年增 6%；營業利益約 10.4 億美元（回推），年增 22%；FY27 財測營收 +5–9%、營業利益 +14–18%。"},{"item":"腫瘤與多專科","value":"第二季營收 149.8 億美元，年增 24%；營業利益 4.27 億美元，年增 8%，排除去年利得後 23%；FY27 財測營收 +20–24%、營業利益 +18–22%。"},{"item":"處方科技","value":"第二季營收 15 億美元，年增 10%；營業利益 3.07 億美元，年增 18%；FY27 財測營收 +2.5–6.5%、營業利益 +11–15%。"},{"item":"醫材","value":"第二季營收 31 億美元，年增 5%；營業利益 2.25 億美元，年減 10%；FY27 財測營收 +1–6%、營業利益 −4% 到持平。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"第二季毛利年增 10%，高於營收 8%。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"市占事實表未涵蓋，未見流失證據。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"配送業不適用。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"差約 6.7 個百分點，主要由回購、利益率與 WAC 下降造成。"},{"signal":"FCF 對淨利連 2 年低於 0.75","lit":false,"note":"FY26 約 1.14，FY27 以調整後淨利估約 0.88。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"金額事實表未涵蓋，稀釋股數持續下降。"},{"signal":"市場萎縮或被替代技術壓縮","lit":false,"note":"處方量成長，直連影響未量化。"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"自身倍數處於四個年度端點最高位。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"第二季資本支出 1.23 億美元，FCF 29.47 億美元。"},{"signal":"停止投資且營收下滑","lit":false,"note":"持續投資，營收成長。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏好但未驗證：回購紀律佳，今年重點轉向兩筆新領域投資，報酬要到 FY29–FY30 才看得出來。","reasoning":"FCF 對淨利的轉換率 FY23 到 FY26 分別為 129%、121%、159%、114%。FY27 財測 FCF 45–49 億美元沒有隨 EPS 上修，以調整後淨利約 53.6 億美元估算，轉換率約 88%。FY27 資金需求：回購約 50 億美元、PMG 22.5 億美元、Option Care 14 億美元、股息約 3.9 億美元，合計約 90 億美元；來源是 FCF 約 47 億美元與 Apollo 約 12.5 億美元，缺口約 31 億美元，若 Option Care 落到 FY28 則缺口約 17 億美元，靠現金與新債支應。季末現金 65 億美元是 PMG 付款前的數字，事實表淨負債 46.74 億美元要調高到約 69 億美元才反映現況。SBC 金額事實表未涵蓋。","fact_refs":["f_kpi5_free_cash_flow","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"歷年併購的已實現增量報酬事實表未涵蓋；PMG 管理層預估第三年底稅後約 8.8%，含綜效、未實現；資金成本事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"上半年回購均價約 818 美元，以 FY27 財測中點 46 美元計盈餘殖利率約 5.6%；10 年期公債殖利率事實表未涵蓋，無法比較。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第二季稀釋加權股數 116.7 百萬股，年減 6%，淨股數持續下降；SBC 金額事實表未涵蓋。"}]},"governance":{"capital_returns":[{"item":"回購","value":"FY27 計畫約 50 億美元，上半年 34 億美元，均價約 818 美元。"},{"item":"併購","value":"Precision Medicine Group 約 22.5 億美元，現金支付，2026 年 11 月完成。"},{"item":"少數股權投資","value":"Option Care Health 49% 約 14 億美元，預計 2027 上半年完成，權益法認列，財測未計入。"},{"item":"股息","value":"殖利率 0.321%，約 3.9 億美元（殖利率乘市值）；2026 年 8 月調升 15%。"},{"item":"外部資金","value":"Apollo 以約 12.5 億美元取得醫材段約 13% 少數股權，FY27 少數股東損益財測 2.9–3.2 億美元。"}]}}},"q5_valuation":{"verdict":"現價要賺年化 12%，以 20 倍終端倍數計，FY2032 EPS 要到約 93.5 美元，五年年化約 15.2%，接近管理層長期目標 13–16% 的上緣。未來兩年我相信做得到，五年都維持我不相信，估值偏貴。","reasoning":"股價 1,060.84 美元，對 FY27 財測中點 46 美元是 23.06 倍；事實表的 23.75 倍用的是財報前共識 44.66 美元，分母已過時。26 週前股價約 734.5 美元，對當時財測中點 44.20 美元約 16.6 倍。這 26 週股價漲 44.4%，FY27 EPS 預期只上修約 4%，其餘都是倍數擴張。Trailing 本益比 27.36 倍位於四個年度端點的最高位，五年分位事實表未涵蓋。現價高於 FN2 目標價共識約 999 美元 6.2%，方向支持不追，但多數目標價早於本次財報，證據力有限；已知目標價區間 812–1,200 美元，高低比 1.48，分歧不大。反方向的可能：若 FY28 財測再度明顯高於共識，23 倍會比看起來便宜。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi7_guidance_fy2027_adjusted","f_ma_w52","f_ma_w104"],"verdict_values":{"valuation":{"basis":"FY1 前瞻本益比，以公司財測中點 46 美元為分母；同業倍數事實表未涵蓋。","tier":"美國藥品配送三強","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，不自行補數；倍數改以自身 26 週前約 16.6 倍與現值 23.06 倍對照。"},"peg":1.65,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 約 23.06 倍，對三年 EPS 年化 14.0% 的 PEG 為 1.65，介於合理區間偏上。基本情境股價年化約 8.6%，加股息約 8.9%。PEG 未破 2 且基本情境仍有正報酬，所以不列最貴一級。短期目標：FY28 基本 EPS 52 美元乘 21 倍，1,092 美元，上行 2.9%。中期目標：FY29 基本 EPS 58.5 美元乘 20.5 倍，1,199 美元，上行 13.0%。","upside_short_pct":2.9,"upside_mid_pct":13.0,"denominator_disputed":false,"denominator_note":"第二季含淨稅務利益 1.05 億美元，約每股 0.90 美元，幾乎等於本季超出預期的 0.93 美元，是否已在共識內事實表未涵蓋。全年營業利益財測上調 3 個百分點，約可解釋全年 EPS 財測中點上調 1.40 美元，分母沒有爭議。稅率每升 1 個百分點，FY27 EPS 約少 0.6 美元。"}}},"q6_how_wrong":{"verdict":"最可能看錯三處：把目前 14–22% 的北美藥品獲利成長當常態、低估政策落地的時間點、把 23 倍當新常態。","reasoning":"推翻論點的路徑是 340B 回扣制與 IRA 價格落地後客戶行為改變，北美藥品成長回到低個位數，倍數回到 14–17 倍。法說迴避點：上一季 FCF 何時加速沒給時點；下半年北美藥品路徑沒給季度數字；340B 當時沒給數字，本季說不預期重大影響但也說不知道客戶會怎麼做；腫瘤段成長率 50% 與 15% 的不一致在原稿未更正。本季分析師問北美藥品要怎樣才會回到長期目標，管理層只重申目標。歷史最大回撤、鴉片訴訟金額與開庭時點事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_price_at_dd","f_ma_w104","f_ma_w250","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退訊號亮燈，EPS 成長明顯快於營收，來源可解釋，目前不像價值陷阱。"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":46.0,"pe":23.06,"basis":"FY1 口徑：FY27 財測中點 46 美元，取代已過時的財報前共識 44.66 美元；終端倍數同為前瞻一年口徑。"},"eps":{"bull":[54.5,63.5,73.5,84.5,96.5],"base":[52.0,58.5,65.5,72.5,80.0],"bear":[47.0,45.5,46.0,48.0,50.0]},"pe":{"bull":24,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.321,"net_buyback":3.0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"max_dd":{"lo":-47,"hi":-28,"basis":"倍數回到 26 週前約 16.6 倍、EPS 46 美元不變，約 764 美元，跌 28%，接近 104 週線 767 美元；EPS 打九折、倍數 15 倍，約 621 美元，跌 41%；極端情況跌到 250 週線 563 美元，跌 47%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"腫瘤與專科維持 20% 上下，北美藥品營運槓桿延續，EPS 五年年化約 16%，等於長期目標上緣；24 倍接近現值，代表市場持續給品質溢價。同業前瞻倍數事實表未涵蓋。","base":"FY28 約 13%，略高於財報前共識，之後因回購效果下降與政策逆風逐步降到約 10%，五年年化約 11.7%；20 倍介於現值 23 倍與 26 週前約 16.6 倍之間。假設醫材分拆對股東價值中性，EPS 路徑未扣分拆影響。","bear":"IRA 與 340B 落地後服務費重議，加上一個前三大客戶以較差條件續約，EPS 在 FY29 回落後低速成長，FY32 約 50 美元。成長率降到 10% 時倍數約 16.6 倍，降到 5% 以下取 14 倍。機率 30%：內生上界無法驗證且共識成長含回購；CVS 已續約是有力反證，所以不再往上加。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"前十大客戶占營收約 73%，WAC 下降與 IRA 定價壓力延續，340B 回扣制可能 2027 年 1 月上路，管理層承認不知道客戶會如何反應。第二季北美藥品獲利成長的來源正好是專科配送、醫療體系與策略客戶。","assumption":"北美藥品獲利成長維持高於長期目標，服務費不隨藥價政策重議。","consequence":"五年後虧 50% 最可能的路徑：政策在 2027–2028 落地，大客戶續約條件轉差，EPS 停在 50 美元，倍數跌到 10.6 倍，股價約 530 美元。情境樹空頭跌 34% 是較可能的版本。","ruling":"部分採納，放進 30% 空頭機率。與唯一致命點在客戶條件上部分重疊，政策路徑另以觸發條件監控。反駁點是 CVS 已續約到 2032 年，WAC 下降兩季未傷營業利益。","watch":"北美藥品營業利益年增率、340B 上路後醫療體系用量、2028 年 1 月 IRA 價格。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","supply_demand_durability#2","end_markets#2"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"FY27 EPS 財測本年度兩次上修，FCF 45–49 億美元沒動。資金轉向 PMG 與 Option Care，現價回購的盈餘殖利率約 4.3%，上半年均價 818 美元時約 5.6%。少數股東損益 FY27 財測 2.9–3.2 億美元。醫材約占分部營業利益 11%，分拆後 EPS 基期會變小。","assumption":"EPS 成長等於股東可拿到的現金成長。","consequence":"EPS 達標，但每股 FCF 只有 EPS 的八到九成，回購買到的股數變少，分拆後的 EPS 基期需要重算；共識是否已反映分拆事實表未涵蓋。","ruling":"採納。基本情境的 EPS 成長逐年降到約 10%，並以 FCF 轉換率作為第三個假設的檢驗。","watch":"FY27 FCF、每股 FCF、分拆條件與換股方式、PMG 增益進度。","evidence_refs":[],"fact_refs":["f_kpi5_free_cash_flow","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"26 週股價漲 44.4%，FY1 倍數由約 16.6 倍升到 23.06 倍，同期 FY27 EPS 預期上修約 4%。現價高於多數財報前的賣方目標價。","assumption":"23 倍是專科轉型帶來的新倍數，不會回落。","consequence":"倍數回到 16.6 倍，即使 EPS 不變也跌 28%。賺年化 12% 需要五年 EPS 年化約 15.2%，等於要求長期目標上緣維持五年。","ruling":"採納。這是本次唯一的限制條件，價格回到 920 美元以下才重新進場。","watch":"股價對 FY28 基本 EPS 的倍數、FY28 財測區間。","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_price_at_dd","f_fwd_pe_latest","f_ma_w104"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 766.08 → 本次 1060.84（+38.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=766.08","side_b":"本次 price_at_dd=1060.84","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 766.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 766.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 766.08 美元：Bull 價 2,316、Bear 價 700，五年期望值 +97.0%，基準年化 15.9%，不對稱比 19.55","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 19.55。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 766.08 美元：五年期望值 +97.0%，基準年化 15.9%，不對稱比 19.55","side_b":"本次情境、股價 1,060.84 美元：五年期望值 +42.2%，基準年化 8.6%，不對稱比 2.9","ruling":"再換股價、情境不動：起點價上漲 38.5%，五年期望值少 54.7 個百分點，基準年化少 7.3 個百分點，不對稱比由 19.55 降到 2.9。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與進場訊號","cause":"價格變動","prior_field":["signal","val"],"side_a":"2026-05-25 股價 766.08 美元，估值中性，進場訊號 A，結論觀望偏進場。","side_b":"2026-11-06 股價 1,060.84 美元，FY1 約 23.06 倍，估值偏貴，進場訊號降為 B。","ruling":"前份之後股價漲 38.5%，EPS 預期上修約 4%，其餘是倍數由約 17.3 倍升到 23.06 倍。前份在 766 美元偏向進場事後看是對的，本次不翻成追價：基本面確實變好，但只解釋一小部分漲幅。","evidence_level":"事實表股價與公司財測","settle_metric":"股價對 FY28 基本情境 EPS 的倍數","if_then":["若股價續漲而 EPS 財測未再上修，則不追","若股價達 1,300 美元以上而財測未再上修，則減碼","若股價跌到 920 美元以下且北美藥品營業利益年增仍達 10%，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱判斷","cause":"新證據","prior_field":["trap"],"side_a":"前份判定無陷阱跡象。","side_b":"本次一項衰退訊號亮燈：共識 EPS 年化約 14.0%，營收年化約 7.3%，差約 6.7 個百分點。","ruling":"差距可解釋：第二季北美藥品營收受 WAC 下降拖累約 4 個百分點，其餘來自回購與利益率，所以只列輕度警示。前份摘要沒有逐項清點，無法確認當時是否已計入。","evidence_level":"事實表共識與逐字稿","settle_metric":"EPS 與營收成長差、FCF 轉換率","if_then":["若 FCF 對調整後淨利連 2 年低於 75%，則停止加碼","若成長差回到 5 個百分點內且 FCF 轉換率達 90%，則解除停止加碼"],"evidence_refs":[]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空。","side_b":"本次填入護城河方向持平、五年後跑道中等、公司類型為品質複利成長；本檔非循環股，循環位置留空；機率與最大回撤由情境樹產生。","ruling":"前份沒有留下數值，無從比較方向變化，不把本次數值視為基本面變動。","evidence_level":"無前值可比","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場門檻。","side_b":"股價 ≤920 美元（約 FY28 基本情境 EPS 17.7 倍，基本情境年化約 12%）。","ruling":"本次卡住的只有價格，重新進場條件因此是價格錨。門檻依基本情境 FY32 股價 1,600 美元回推。","evidence_level":"情境假設","settle_metric":"股價","if_then":["若股價 ≤920 美元且基本面未破，則分批反買","若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元"],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標。","side_b":"本次設五項：北美藥品營業利益年增連 3 季低於 5%、腫瘤段營收年增連 2 季低於 10%、前三大客戶流失、FCF 轉換率連 2 年低於 75%、直連占 GLP-1 處方達 30%。","ruling":"前份只有風險閾值，本次把會改變持股的條件寫成明確的清倉指標，保留前份直連 30% 的門檻。","evidence_level":"判斷設定","settle_metric":"五項指標","if_then":["若任兩項同時成立，則清倉","若僅一項成立，則減碼"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"前三大客戶中任一家不續約或大幅降價轉單。","ruling":"客戶事件是單一事件中 EPS 敏感度最大的一項；終端倍數敏感度更大，但不是單一事件，放在反證處理。","evidence_level":"10-K 客戶集中度與回推","settle_metric":"8-K 與 10-K 客戶揭露","if_then":["若事件發生，則減碼至半倉","若兩季內未由新客戶補回，則清倉"],"evidence_refs":["customer_second_source#0"]},{"axis":"北美藥品假設門檻","cause":"新證據","prior_field":["thesis.H1"],"side_a":"季 Rev YoY ≥ 10%；季 Pharma OI margin ≥ 1.4%；連 2 季 Pharma Rev YoY < 8% 削弱。","side_b":"單季營業利益年增 ≥10%，營業費用占毛利比率年改善。","ruling":"WAC 下降使北美藥品營收成長少約 4 個百分點，第二季營收年增 6%，按舊門檻已削弱，同季營業利益卻年增 22%，營收不再是合適指標。舊的 1.4% 利益率與回推的 1.14% 差距大，前份分部範圍可能不同，無法核對。","evidence_level":"2026-11-04 逐字稿","settle_metric":"北美藥品營業利益年增率","if_then":["若 TTM 年增連 3 季低於 5%，則清倉","若單季年增低於 10%，則停止加碼"],"evidence_refs":["end_markets#2"]},{"axis":"腫瘤段假設門檻","cause":"新證據","prior_field":["thesis.H2"],"side_a":"季 Oncology YoY ≥ 20%；OP margin ≥ 3%；連 2 季 YoY < 15% 削弱；OP margin < 2.5% 反轉。","side_b":"單季營收年增 ≥15%；利益率 ≥2.5%；FY28 營業利益年增 ≥15%。","ruling":"第二季營收年增 24%，利益率 2.85%，低於舊的 3% 但高於 2.5% 反轉線。專科配送放量會壓低利益率，所以門檻改看營業利益成長，反轉線保留。","evidence_level":"10-Q 與逐字稿","settle_metric":"腫瘤段營業利益年增率與利益率","if_then":["若利益率低於 2.5%，則減碼","若營收年增連 2 季低於 10%，則清倉"],"evidence_refs":[]},{"axis":"第三個假設改寫","cause":"方法變動","prior_field":["thesis.H3"],"side_a":"MedSurg 分拆 2027 完成，2027-06 前完成 spin；分拆延後 6+ 個月警戒，放棄則反轉。","side_b":"併購與回購轉成每股現金成長，FCF 對調整後淨利 ≥90%；分拆移到風險項，保留舊門檻。","ruling":"分拆進度正常，2027 年 1 月將以 Wellverse 名稱營運，對股東價值的主要爭點已轉到資本配置與現金轉換。","evidence_level":"2026-08-05 逐字稿","settle_metric":"分拆公告與 FCF 轉換率","if_then":["若分拆延後 6 個月以上，則停止加碼"],"evidence_refs":[]},{"axis":"EPS 上修而 FCF 未上修","cause":null,"prior_field":null,"side_a":"2026-08-05 Kenny Cheung 說營運資金改善有機會優於財測，並把 say-do ratio 當作標準。","side_b":"2026-11-04 EPS 財測再上調，FCF 財測 45–49 億美元不變，低於 FY26 的 54.1 億美元。","ruling":"性質：可調和，時間性差異未證、監測。先認定為季底日期與營運資金時點，預先設定連 2 個財年 FCF 低於調整後淨利 90%，時間性的說法即不成立。","evidence_level":"逐字稿與財報","settle_metric":"FY27 與 FY28 的 FCF 對調整後淨利","if_then":["若 FY27 FCF 低於 45 億美元，則停止加碼","若 FY27 FCF 達 55 億美元以上，則解除停止加碼"],"evidence_refs":[]},{"axis":"併購節奏","cause":null,"prior_field":null,"side_a":"2026-08-05 Brian Tyler 稱不預期 FCS 規模的併購，Kenny Cheung 稱會有一些小型併購。","side_b":"2026-08-25 宣布 22.5 億美元買 Precision Medicine，10 月再簽約以 14 億美元買 Option Care 49%；Brian Tyler 2026-11-04 表示 CRO 部分對公司是新業務。","ruling":"性質：可調和但要記一筆。摘錄只有片段，原話可能只針對診所類併購，無法判定改口。PMG 預估稅後約 8.8%，高於現價回購約 4.3%，但含綜效。Option Care 由 CD&R 經營，公司是少數股東，分析師提到的買下其餘股權選擇權管理層未正面回應。","evidence_level":"逐字稿摘錄","settle_metric":"PMG 第三年底每股增益","if_then":["若 FY28 再有 20 億美元以上跨入新領域的併購且 PMG 進度落後，則停止加碼","若 PMG 增益按進度且 FCF 達標，則維持 920 美元的進場價"],"evidence_refs":[]},{"axis":"長期目標與實際成長","cause":null,"prior_field":null,"side_a":"Kenny Cheung 2026-11-04 重申 EPS 長期目標 13–16%。","side_b":"FY27 排除一次項的 EPS 成長 19–21%，分析師直指長期目標過低，管理層未回答要怎樣才會回到目標內。","ruling":"性質：可調和。長期目標偏保守有依據，也可能只是壓低預期。基本情境取年化約 11.7%，低於長期目標；多頭 16% 等於上緣。","evidence_level":"2026-11-04 逐字稿","settle_metric":"FY28 財測 EPS 成長區間（約 2027 年 5 月）","if_then":["若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元並分批反買","若 FY28 財測中點年增低於 10%，則停止加碼並把進場價下修到 800 美元"],"evidence_refs":[]},{"axis":"WAC 與 IRA 對獲利的影響","cause":null,"prior_field":null,"side_a":"Kenny Cheung 2026-08-05 與 11-04 都說 WAC 下降只影響營收，品牌藥九成五以上是服務費。","side_b":"10-Q 與媒體指定價逆風延續；IRA 價格水準未知（2026-08-05 Brian Tyler），2028 年 1 月才生效。","ruling":"性質：程度差異。兩季實績支持管理層，但證據的時間窗沒有涵蓋 2028 年，不能說風險已解，裁定為不可判斷，要等 IRA 價格公布。","evidence_level":"10-Q 與逐字稿","settle_metric":"IRA 價格公布後北美藥品營業利益年增率","if_then":["若管理層改口稱對營業利益有重大影響，則減碼","若 2028 年兩季內營業利益年增仍達 10%，則解除此項警示"],"evidence_refs":["end_markets#2","supply_demand_durability#2"]},{"axis":"下半年北美藥品路徑","cause":null,"prior_field":null,"side_a":"2026-08-05 Brian Tyler 說學名藥有利因素提前，會犧牲後面季度。","side_b":"2026-11-04 北美藥品全年營業利益財測上調到 14–18%，第二季年增 22%，下半年加速投資。","ruling":"性質：可調和。財測已隱含下半年減速，第二季的強勁不能外推，這也是基本情境 FY28 只放 13% 的原因之一。","evidence_level":"逐字稿","settle_metric":"第三、四季北美藥品營業利益年增率","if_then":["若下半年年增低於 10%，則停止加碼","若下半年年增達 18%，則進場價上調到 1,000 美元"],"evidence_refs":[]},{"axis":"共識資料時點","cause":null,"prior_field":null,"side_a":"事實表 FY1 共識 44.66 美元，近 3 個月修正 0.09%，最近兩份快照修正 0%。","side_b":"2026-11-04 公司把 FY27 財測上調到 45.60–46.40 美元，共識已低於新區間下緣。","ruling":"快照早於財報反映，修正 0% 不代表賣方沒動作。情境樹起點改用財測中點，三年共識仍列舊值並註明過時；舊分母使前瞻本益比高估約 0.7 倍。","evidence_level":"事實表與新聞稿","settle_metric":"下一份快照 FY1 是否達 45.60 美元","if_then":["若下一份快照 FY1 仍低於 45.60 美元，則不追，先確認資料來源"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：三強格局未變，新進者與藥廠直連是慢變數，未見量化傷害。結構轉好：專科藥與社區照護需求持續，醫療體系與專科量帶動獲利。","side_b":"其他結構變數：340B 回扣制、IRA 2028、藥品關稅、Medicare GLP-1 Bridge 計畫都在變動。","ruling":"雙向拉鋸：需求結構轉好，政策軸變動中，競爭軸靜態。依據是 2026-11-04 逐字稿與 FY2026 10-K。","evidence_level":"公司揭露","settle_metric":"北美藥品營業利益年增率與 340B 上路後用量","if_then":["若 340B 上路後北美藥品營業利益年增連 2 季低於 10%，則停止加碼"],"evidence_refs":["channel_business_model_shift#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"EPS 連續上修，長期目標明顯保守，現價對 FY28 基本 EPS 約 20.4 倍；若 EPS 維持年增 18%，一年後倍數自然消化，前份 766 美元的經驗顯示等回檔可能等不到。","side_b":"現價要求五年 EPS 年化約 15.2% 才賺 12%，公司自己上半年的回購均價是 818 美元。","ruling":"不追。等待的代價是股價不回來就錯過，這個代價可以接受。為避免用過時 EPS 錨定，FY28 財測若夠強，進場價會上調。","evidence_level":"情境推算","settle_metric":"FY28 財測與股價","if_then":["若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元並分批反買","若股價續漲而財測未上修，則不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 920 美元以下，重新評估首筆進場","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤920 美元","action":"分批反買","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"北美藥品營業利益成長低於財測或假設門檻","type":"假設驗證","maps_to":"H1","metric":"北美藥品營業利益年增率","threshold":"FY27 全年低於 14% 或單季低於 10%","action":"停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":["end_markets#2"]},{"n":3,"text":"腫瘤與多專科成長或利益率跌破門檻","type":"假設驗證","maps_to":"H2","metric":"腫瘤段營收年增率與利益率","threshold":"營收年增低於 15% 或利益率低於 2.5%","action":"利益率破線減碼，營收低於 15% 停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":[]},{"n":4,"text":"FCF 持續落後 EPS","type":"假設驗證","maps_to":"H3","metric":"FCF 對調整後淨利","threshold":"低於 90% 連 2 個財年","action":"停止加碼","source_freq":"每年財報","date":"2027-05","evidence_refs":[]},{"n":5,"text":"340B 回扣制上路後醫療體系與專科用量轉弱","type":"風險","maps_to":"R2","metric":"北美藥品營業利益年增率","threshold":"上路後連 2 季低於 10%","action":"停止加碼","source_freq":"每季財報、政策公告","date":"2027-01","evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"n":6,"text":"前三大客戶任一家不續約或大幅降價轉單","type":"Single Thing","maps_to":"R1","metric":"客戶揭露與營收占比","threshold":"任一前三大客戶流失，或 10-K 揭露占比單年降 3 個百分點以上","action":"減碼至半倉，兩季未補回則清倉","source_freq":"8-K、每年 10-K","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":7,"text":"再度發生嚴重藥品召回或 FDA 警告信，表示配送品質出問題","type":"風險","maps_to":"R1","metric":"Class I 召回或 FDA 警告信件數","throughput":null,"threshold":"12 個月內再有 1 件 Class I 召回或 1 封警告信","action":"停止加碼","source_freq":"FDA 公告","date":null,"evidence_refs":["major_events#3","product_recall_warning#0"]},{"n":8,"text":"鴉片相關訴訟出現大額新增準備或刑事程序","type":"風險","maps_to":"R6","metric":"新增和解或準備金額","threshold":"達 10 億美元減碼，出現刑事程序清倉","action":"減碼或清倉","source_freq":"10-Q 與 10-K 附註","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":9,"text":"關稅或供應中斷的成本未能轉嫁","type":"風險","maps_to":"R5","metric":"合併毛利年增率減營收年增率","threshold":"連 2 季為負，且管理層歸因關稅或採購成本","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"n":10,"text":"股價跌到 52 週線附近且假設未破，持有者可增加部位","type":"加碼","maps_to":"H1","metric":"股價與北美藥品營業利益年增率","threshold":"股價 ≤860 美元，且單季年增達 10%","action":"分批反買","source_freq":"每日收盤、每季財報","date":null,"evidence_refs":[]},{"n":11,"text":"股價繼續上行但財測未跟上","type":"減碼","maps_to":"H1","metric":"股價對 FY28 基本 EPS 倍數","threshold":"股價 ≥1,300 美元（25 倍），且 FY28 基本 EPS 未上修","action":"減碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":12,"text":"兩項以上清倉指標同時成立","type":"清倉","maps_to":"H1","metric":"清倉指標成立數","threshold":"五項中任兩項成立","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":[]},{"n":13,"text":"FY28 財測公布時複審情境與進場價","type":"複審日期","maps_to":"H3","metric":"FY28 EPS、FCF 與分部財測","threshold":"財測公布","action":"依財測中點年增調整進場價：達 16% 上調到 1,000 美元，低於 10% 下修到 800 美元","source_freq":"年度財報","date":"2027-05","evidence_refs":[]}],"kill_metrics":[{"metric":"北美藥品營業利益 TTM 年增率","bear_threshold":"低於 5%","window":"連 3 季","source":"每季財報分部數字","last_status":"ok"},{"metric":"腫瘤與多專科營收年增率","bear_threshold":"低於 10%","window":"連 2 季","source":"每季財報分部數字","last_status":"ok"},{"metric":"前三大客戶續約狀況","bear_threshold":"任一家流失或不續約","window":"事件發生即成立","source":"8-K、10-K 客戶集中度揭露","last_status":"unknown"},{"metric":"FCF 對調整後淨利","bear_threshold":"低於 75%","window":"連 2 個財年","source":"新聞稿 FCF 與調整後 EPS","last_status":"warning"},{"metric":"藥廠直連通路占 GLP-1 處方比例","bear_threshold":"達 30%（保留前份門檻）","window":"滾動 12 個月","source":"藥廠揭露；目前為資料缺口","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤920 美元（約 FY28 基本情境 EPS 17.7 倍，基本情境年化約 12%）","exec_line":"未持有者不追；股價 920 美元以下且基本面未破，分批建立首筆。已持有者續抱、停止加碼；股價 1,300 美元以上且財測未再上修則減碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 920 美元以下；基本面沒有需要等的事件，卡住的是價格。"},"thesis":{"H":[{"id":"H1","text":"北美藥品配送的獲利成長持續快於營收，靠專科藥組合與營運槓桿，不靠藥價。","2y":"FY28 北美藥品營業利益年增 ≥10%（FY27 財測 14–18%）","5y":"到 FY32 營業利益年化 ≥8%","10y":null,"threshold":"單季營業利益年增 ≥10%；營業費用占毛利比率年改善","source":"每季新聞稿與法說逐字稿的分部數字","drift_rule":"TTM 年增偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉"},{"id":"H2","text":"腫瘤與多專科平台成為第二成長引擎，營業利益占比持續上升。","2y":"FY28 營業利益年增 ≥15%，利益率 ≥2.5%","5y":"FY32 占分部營業利益 ≥30%（現約 21%）","10y":null,"threshold":"單季營收年增 ≥15%；利益率 ≥2.5%","source":"每季財報分部損益；有機成長未揭露，列資料缺口","drift_rule":"TTM 偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉；利益率低於 2.5% 直接反轉"},{"id":"H3","text":"併購與回購能轉成每股現金成長，調整後 EPS 達長期目標，FCF 跟得上。","2y":"FY28 調整後 EPS ≥51 美元，FCF 對調整後淨利 ≥90%","5y":"FY32 調整後 EPS ≥80 美元；PMG 第三年底增益 ≥1.60 美元","10y":null,"threshold":"FCF 對調整後淨利 ≥90%；PMG 第三年底增益 ≥1.60 美元","source":"新聞稿 FCF 與 EPS、併購進度揭露","drift_rule":"TTM 偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉"}],"R":[{"id":"R1","text":"大客戶集中：前十大占營收約 73%，CVS 已續約到 2032 年，其餘大客戶到期日不明，條件轉差比流失更可能。","h_ref":"H1","clock":"🔥","threshold":"任一前三大客戶流失，或 10-K 揭露前十大占比單年降 3 個百分點以上；OptumRx 合約變動公告立即重評（保留前份門檻）","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"藥價政策：IRA、WAC 下降與 340B 回扣制可能改變服務費基礎或客戶行為。兩季實績未傷營業利益，但 2028 年的 IRA 價格與 340B 後的客戶行為都未知。","h_ref":"H1","clock":"🔥","threshold":"管理層改口稱對營業利益有重大影響，或北美藥品營業利益年增連 4 季低於 10%","evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"id":"R3","text":"藥廠直連與自建通路擴大，壓縮配送環節。","h_ref":"H1","clock":"🐢","threshold":"直連占 GLP-1 處方達 30%（保留前份門檻，資料缺口）；專科藥利益率連 4 季下滑超過 50 個基點（保留前份門檻）；GLP-1 配送營收連 2 季環比下滑且產業量未降","evidence_refs":["channel_business_model_shift#2","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"醫材分拆執行失敗、延後，或分拆條件傷害每股價值。","h_ref":"H3","clock":"⚡","threshold":"分拆延後 6 個月以上，或 Apollo 公開退出，或財報重編，立即重評（保留前份門檻）","evidence_refs":[]},{"id":"R5","text":"關稅與上游原料依賴海外造成供應中斷或成本上升。海外業務僅約 4%，曝險在學名藥上游，公司自身曝險未量化。","h_ref":"H1","clock":"🔥","threshold":"合併毛利年增率低於營收年增率連 2 季，且管理層歸因關稅或採購成本","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"鴉片相關私人原告訴訟仍有數百件，另有 False Claims Act 案；金額與時點事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"新增和解或準備達 10 億美元減碼，出現刑事程序清倉","evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"id":"R7","text":"PMG 與 Option Care 跨入新領域，整合與報酬未驗證；Option Care 由 CD&R 主導，公司只有少數股權。","h_ref":"H3","clock":"🔥","threshold":"PMG 第三年底增益低於 1.60 美元，或 FY28 再有 20 億美元以上跨入新領域的併購且 PMG 進度落後","evidence_refs":[]}],"single_thing":{"description":"前三大客戶中任一家不續約或大幅降價轉單。CVS（約 24%）已續約到 2032 年 6 月，剩下的是占營收 11% 與 10% 的兩家，名稱與到期日事實表未涵蓋。","why_fatal":"這是單一事件中對 EPS 敏感度最大的一項。以北美藥品平均利益率約 1.14% 粗估，失去 11% 營收的客戶約少 5 億美元營業利益、每股約 3.5 美元，約占 FY27 EPS 的 8%。單客實際利潤率未揭露，可能偏離平均。","if_happens":"EPS 下修約 8%，倍數同步下移，股價先看跌 25–30%。立即減碼至半倉，兩季內未由新客戶補回則清倉。","how_monitor":"8-K、每年 10-K 客戶集中度揭露、法說中的續約與客戶異動說明。","probability":"12–24 個月約 10%，屬主觀估計：CVS 已續約是有力反證，其餘兩家到期日未知。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.95,"peg_fy2":1.5,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":38.98,"FY2027E":44.66,"FY2028E":50.63,"FY2029E":57.72},"fy_end_month":3,"eps_basis":"調整後稀釋 EPS，財年截至 3 月。FY2026A 事實表未直接收錄，由 FY27 財測 45.60–46.40 美元與年增 17–19% 回推；FY2027E 至 FY2029E 為財報前 Koyfin 共識，FY2027E 已低於新財測下緣。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"regulatory","event":"340B 回扣制可能上路","impact":"高","watch":"醫療體系與專科用量、客戶是否轉換通路"},{"date":"2027-01","date_precision":"month","type":"other","event":"醫材事業預計以 Wellverse 名稱營運，推進分拆","impact":"中","watch":"分拆方式、時程、對 EPS 基期的影響"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第三季財報（時間為預估）","impact":"中","watch":"北美藥品營業利益是否如預期減速、下半年投資幅度"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第四季財報與 FY28 財測（時間為預估）","impact":"高","watch":"EPS 成長區間、FCF 財測、PMG 進度"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"Option Care Health 49% 股權預計於 2027 上半年完成","impact":"中","watch":"股東與監管核准、權益法收益"},{"date":"2028-01","date_precision":"month","type":"regulatory","event":"IRA 相關價格生效","impact":"高","watch":"價格水準、管理層對營業利益影響的說法"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=44.43, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
