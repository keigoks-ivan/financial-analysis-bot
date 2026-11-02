你是 DD 管線 v20 的判斷層閘（gate），標的 NVT（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（51 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝1514.9 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_kpi1_non_gaap_adjusted_operat`（q1_business）｜Non-GAAP (adjusted) operating income / return on sales＝22.1 %（調整後營業利益 335.4M，YoY +57%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝18.6 %（GAAP 營業利益 282.3M，YoY +70%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝267.9 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_kpi5_guidance_q4_fy2026`（q1_business）｜Guidance: Q4 FY2026＝adjusted EPS 1.30–1.33；GAAP EPS 1.13–1.16 USD/share｜期間與口徑：公告於 2026-10-30／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[5]，as_of 公告於 2026-10-30）
  - 註記：未採集（本檔 consensus_revision 為財報前快照）
- `f_kpi6_guidance_fy2026`（q1_business）｜Guidance: FY2026（上調）＝adjusted EPS 5.36–5.39；GAAP EPS 4.54–4.57 USD/share｜期間與口徑：公告於 2026-10-30／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[6]，as_of 公告於 2026-10-30）
  - 註記：未採集
- `f_kpi7_systems_protection_sales`（q1_business）｜Systems Protection sales / adj. return on sales＝1098.0 USD M（YoY +53%；adj. ROS 23.0%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_kpi8_electrical_connections_s`（q1_business）｜Electrical Connections sales / adj. return on sales＝416.9 USD M（YoY +23%；adj. ROS 28.2%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：未採集
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-30 date｜期間與口徑：2026-10-30／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-30）
- `f_peer_nvt_gross_margin_pct`（q2_moat）｜NVT 毛利率＝36.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvt_operating_margin_pct`（q2_moat）｜NVT 營業利益率＝17.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvt_fcf_margin_pct`（q2_moat）｜NVT FCF 利潤率＝11.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVT.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hubb_gross_margin_pct`（q2_moat）｜HUBB 毛利率＝35.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hubb_operating_margin_pct`（q2_moat）｜HUBB 營業利益率＝20.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hubb_fcf_margin_pct`（q2_moat）｜HUBB FCF 利潤率＝14.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_etn_fcf_margin_pct`（q2_moat）｜ETN FCF 利潤率＝13.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vrt_gross_margin_pct`（q2_moat）｜VRT 毛利率＝38.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝20.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_fcf_margin_pct`（q2_moat）｜VRT FCF 利潤率＝23.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.17 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.78 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.05 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5809.28 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7537.62 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝12.15 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 4.61 → 5.17（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation（前九個月累計，新聞稿未單列 Q3）＝30.9 USD M（9M 2026）｜期間與口徑：前九個月至 2026-09-30，公告於 2026-10-30／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[4]，as_of 前九個月至 2026-09-30，公告於 2026-10-30）
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1224.1 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 2345.9、現金 1121.8（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝161.6 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.671 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.21 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.17，分子＝快照價 125.19｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝125.19 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝30.39 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝75.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝75.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.82 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝62.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝62.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.05 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝54.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝54.1 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.69 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝21454.56 USD m｜期間與口徑：2026-11-03／市值 20230.46 ＋ 淨負債 1224.1｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（5.17 → 5.17）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（6.78 → 6.78）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（8.05 → 8.05）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-22.82 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.62｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 122.23 / W52 136.36 / W104 105.32 / W250 72.52 / W250 13週斜率 2.13%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝136.36 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝105.32 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝72.52 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝2.13 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司面對大型全球對手、區域／在地廠商與低成本製造商，並明言新進入者可能提供競爭產品，可能壓縮利潤並限制維持或提高份額的能力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Vertiv 2026-04 完成收購 Strategic Thermal Labs 以強化液冷工程能力（對手動作）；nVent 稱已部署逾 2GW 液冷容量。
  - 來源：Zacks／Nasdaq: Can AI Data Center Demand Keep Driving nVent Electric's Growth?（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Wood Mackenzie 2025年9月摘要：GSU與電力變壓器交期出現改善跡象但仍在2～3年；另有報導指低壓桿上變壓器可能轉為過剩。
  - 來源：Wood Mackenzie: Making the connection executive summary (Sept 2025) / powerpeakdigest（as_of 2025-09-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：公司列出對鋼、鋁、銅及中國、加拿大、墨西哥製品關稅的暴露；2025 年第二季起新關稅（含中國、墨西哥、歐盟）已公布，後續仍可能調整，最終影響不確定。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：MD&A：2025 年新關稅因緩解措施對財務無重大影響，但預期 2026 年起通膨成本（含關稅）持續，可能衝擊營運結果；2025 年毛利率下滑 2.5 個百分點部分源於含關稅的通膨。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-17）｜affects：thesis.R、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：部分產品屬兩用（dual use）產品，受較嚴格出口管制。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：nVent 揭露依賴美國以外生產的零組件與成品，點名墨西哥與中國，並提及政治或貿易不穩定風險
  - 來源：nVent Electric 10-K FY2025 ARS（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2026 年 10-Q 稱關稅帶來原料、人工、運輸通膨，供應鏈限制可能中斷關鍵零組件取得
  - 來源：nVent Electric 10-Q 2026-09-30（as_of 2026-10-31）｜affects：thesis.R、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 13 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":322.5,"bear_5y_price":93.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":63.8,"ev5y_pct":60.4,"irr_base_pct":10.4,"asym_ratio":5.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.17,"pe":24.21,"basis":"2026 年共識調整後 EPS（Koyfin 財報前快照；已過三季，公司財測中點 5.375）；終端倍數同樣乘在當年度 EPS 上"},"eps":{"bull":[7.1,8.7,10.2,11.6,12.9],"base":[6.75,7.85,8.7,9.5,10.25],"bear":[6.25,5.0,4.95,5.55,6.2]},"pe":{"bull":25,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.671,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVT_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：全年報告營收成長財測自 26%–28% 上調至 37%–39%。（原話："reported sales growth of 37% to 39%, up from 26% to 28% previously."）
- 2026-07-31｜CFO｜guidance：全年有機營收成長財測為 32%–34%，前次為 21%–23%。（原話："We now expect to grow 32% to 34% versus our prior"）
- 2026-07-31｜CFO｜guidance：全年調整後 EPS 區間上調至 $5–$5.10（原 $4.45–$4.55）。（原話："raising our full year adjusted EPS range to $5 to $5.10"）
- 2026-07-31｜CFO｜guidance：第三季報告與有機營收成長財測 32%–35%。（原話："we forecast reported and organic sales growth of 32%"）
- 2026-07-31｜CFO｜guidance：第三季調整後 EPS 財測 $1.35–$1.38，中點成長約 50%。（原話："between $1.35 and $1.38, which at the midpoint reflects 50%"）
- 2026-07-31｜CFO｜guidance：全年自由現金流轉換率維持 90%–95%。（原話："we still expect conversion of 90% to 95%"）
- 2026-07-31｜CFO｜guidance：全年關稅衝擊預估由 $80M 增至約 $100M，管理層稱主因為量大幅成長。（原話："tariff impact is expected to be approximately $100 million"）
- 2026-07-31｜CEO｜guidance：2026 年資料中心總銷售預期超過 $20 億，為去年兩倍以上。（原話："center sales to be more than $2 billion in 2026"）
- 2026-07-31｜CFO｜margin：下半年財測內含的增量利潤率假設為 20% 中段。（原話："which is assuming mid-20s incrementals in the second half"）
- 2026-07-31｜CFO｜margin：CFO 說明中期增量利潤率目標為 20% 中段，目的是留空間投資成長。（原話："our midterm target was mid-20s for incrementals"）
- 2026-07-31｜CFO｜margin：公司整體調整後營業利益率 21.9%，較去年 +110bp；價格加生產力抵銷超過 $50M 通膨（含超過 $30M 關稅）。（原話："Return on sales came in ahead of expectations at 21.9%"）
- 2026-07-31｜CFO｜margin：Electrical Connections 利潤率 27.3%，年減 140bp。（原話："Return on sales of 27.3% was down 140 basis points"）
- 2026-07-31｜CFO｜margin：管理層將 EC 利潤率年減歸因於通膨與產品組合，部分被價格與量抵銷。（原話："performance was impacted by inflation and mix"）
- 2026-07-31｜CFO｜commitment：CFO 表示預期 EC 今年利潤率落在 20% 後段（high 20s）。（原話："that's where I expect it to be this year."）
- 2026-07-31｜CFO｜commitment：管理層持續預期以定價、供應鏈生產力與營運措施抵銷通膨（含關稅）。（原話："impact of inflation, including tariffs through pricing"）
- 2026-07-31｜CFO｜commitment：第三季財測稱定價將抵銷通膨衝擊。（原話："Pricing is expected to offset the impact of inflation"）
- 2026-07-31｜CFO｜capital_allocation：全年資本支出維持約 $1.3 億、年增 40%，多用於資料中心、電力公用事業與供應鏈韌性的新產能。（原話："invest approximately $130 million in CapEx, up 40%"）
- 2026-07-31｜CFO｜capital_allocation：上半年回饋股東 $1.18 億，含回購 $5,000 萬。（原話："we returned $118 million to shareholders"）
- 2026-07-31｜CFO｜capital_allocation：淨槓桿 1.2 倍，低於 2–2.5 倍的目標區間。（原話："net leverage of 1.2x, well below our target range"）
- 2026-07-31｜CEO｜capital_allocation：CEO 稱併購管線良好、維持紀律，目標進一步強化基礎設施布局。（原話："on M&A, we have a very good pipeline"）
- 2026-07-31｜CEO｜capital_allocation：宣布第三個明尼蘇達液冷擴產據點 Blaine 2，預計 2027 上半年啟用。（原話："This facility is expected to open in the first half of 2027"）
- 2026-07-31｜CEO｜capital_allocation：Blaine 1 從簽約到開廠約 100 個工作天。（原話："Blaine site within approximately 100 working days"）
- 2026-07-31｜CEO｜capital_allocation：被問 Blaine 2 能否同樣 100 天內開張，CEO 說太積極。（原話："I think that's too aggressive"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說新增產能可支撐需求至 2027 並進入 2028。（原話："that takes us through '27 and into '28 at this time"）
- 2026-07-31｜CEO｜customer：管理層稱基礎設施方面客戶涵蓋超大規模雲端、neo-cloud、多租戶與經銷夥伴。（原話："a wide range of customers from hyperscalers to neo-clouds"）
- 2026-07-31｜CEO｜customer：客戶採購方式有整套購買，也有只買液冷系統一部分；公司表示可在整條價值鏈彈性供應。（原話："we're working with hyperscalers, we're working with colos"）
- 2026-07-31｜CEO｜customer：本季有機訂單成長為低雙位數，積壓訂單 $25 億。（原話："backlog remained healthy at $2.5 billion"）
- 2026-07-31｜CEO｜customer：CEO 稱資料中心訂單大且不均，第三季至今資料中心訂單強勁。（原話："In fact, we've had strong data center"）
- 2026-07-31｜CFO｜customer：CFO 稱積壓訂單多數在 12 個月以內，期限未拉長。（原話："mostly 12 months or less, and that hasn't extended out."）
- 2026-07-31｜CEO｜customer：CEO 稱客戶未必以更長前置期下單，但公司有取得客戶未來需求能見度。（原話："that not necessarily for the -- in the product portfolios"）
- 2026-07-31｜CEO｜customer：CEO 稱經銷商 sell-in 與 sell-out 平衡，短週期需求為實際需求。（原話："it's actually been well balanced"）
- 2026-07-31｜CEO｜customer：CEO 稱 EC 短週期（經銷通路）訂單為轉折點。（原話："it was just a nice inflection point"）
- 2026-07-31｜CEO｜customer：電力公用事業本季成長雙位數。（原話："power utilities grew double digits for us in the quarter"）
- 2026-07-31｜CEO｜customer：資料中心與電力公用事業產能若有取捨，管理層稱會做審慎決策。（原話："we make prudent decisions if there has to be trade-offs"）
- 2026-07-31｜CEO｜customer：管理層稱資料中心正在歐洲與亞洲擴張，公司正投資當地商務與製造。（原話："data centers are expanding in both Europe and Asia"）
- 2026-07-31｜CEO｜product：新產品貢獻銷售成長超過 30 個百分點。（原話："New products contributed over 30 points to our sales"）
- 2026-07-31｜CEO｜product：新一代模組化液冷平台預計今年秋季推出。（原話："modular platform is going to launch later this fall"）
- 2026-07-31｜CEO｜product：CEO 稱正投入液冷產品的服務能力建設。（原話："And as we are also investing in a service capability to"）
- 2026-07-31｜CEO｜product：管理層對 800V DC 的看法：認為有一定應用，但仍有低壓需求，視為延伸機會。（原話："is going to have some application in data centers"）
- 2026-07-31｜CEO｜competition：CEO 稱液冷目前僅占資料中心冷卻的 10%–15%。（原話："maybe it's now 10% to 15% of cooling in"）
- 2026-07-31｜CEO｜risk：對 Q3 財測，CEO 說因產能爬坡需配置設備、人力與供應商，規劃上採審慎。（原話："But as we look forward, we're just being prudent."）
- 2026-07-31｜CFO｜risk：CFO 稱財測保持審慎以保留執行與投資彈性。（原話："it's important that we're prudent in our guidance"）
- 2026-07-31｜CFO｜risk：CFO 指下半年面對的基期：有機約 20%、EPS 成長約 50%。（原話："we're going to be lapping 20% organic and 50% EPS growth"）
- 2026-07-31｜CEO｜risk：CEO 談長期能見度：與 NVIDIA 等合作至 2030 路線圖，並稱資料中心建置放緩時液冷仍有汰換週期。（原話："NVIDIA and others on their road maps out through 2030"）
- 2026-07-31｜CEO｜risk：CEO 稱客戶能見度達數年。（原話："we've got a visibility several years out"）
- 2026-07-31｜CEO｜risk：分析師問積壓訂單是否為合適水位，CEO 稱約在合適水準。（原話："it's around the right level"）
- 2026-07-31｜CFO｜customer：被問近 12 個月訂單成長是否高於本季低雙位數，CFO 回答是，未給數字。（原話："Yes, Brian, they are."）
- 2026-07-31｜CEO｜commitment：結語稱有多種槓桿可擴大利潤率。（原話："multiple levers to expand margins"）
- 2026-07-31｜CEO｜customer：基礎設施占銷售比重：分拆時 12%、去年 45%、今年上半年近 60%。（原話："expanded to 45% last year and was nearly 60% in the first"）

### NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md
- 2026-03-18｜Gary Corona (CFO)｜guidance：CFO 提出三年期（至2028）新目標：有機成長10%–13%（原話："now expect organic sales growth of 10% to 13%"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：併購每年貢獻超過3個百分點營收，原為約1點（原話："acquisitions to be more than 3 points of sales annually, up"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：調整後EPS成長17%–20%（原話："We now expect adjusted EPS growth of 17% to 20%"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：三年目標：自由現金流轉換率約95%（原話："expect to convert approximately 95% of our earnings into"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：2026年資本支出計畫約1.3億美元（原話："Looking ahead to 2026, we plan to invest approximately $130"）
- 2026-03-18｜Sara Zawoyski｜guidance：Systems Protection 2025年銷售報酬率逾20%，管理層預期2026年再有好表現（原話："Return on sales was over 20%, and we expect another great"）
- 2026-03-18｜Gary Corona (CFO)｜guidance：ROIC目標：2028年前超過15%（原話："investments with ROIC exceeding 15%, an additional 2-point"）
- 2026-03-18｜Aravind Padmanabhan｜guidance：新產品活力長期目標30%，每年貢獻逾3點銷售成長（原話："expect new products to deliver 30% vitality"）
- 2026-03-18｜Gary Corona (CFO)｜margin：營業利潤率目標：三年約擴張2點至約22%（原話："From a margin perspective, we're targeting approximately 2"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：22%利潤率預測與EPS目標都不含併購（原話："the margin forecast does not include M&A nor did the EPS, as"）
- 2026-03-18｜Gary Corona (CFO)｜margin：利潤率擴張來源：定價、高毛利新產品、成長帶來的規模槓桿（原話："driven by disciplined pricing, margin-accretive new products"）
- 2026-03-18｜Gary Corona (CFO)｜margin：增量利潤率口徑：約中段20%（mid-20s）（原話："That's approximately mid-20s from an"）
- 2026-03-18｜Gary Corona (CFO)｜margin：兩個事業部都預期擴張利潤率（原話："Both segments have nice margin improvement plans, and we"）
- 2026-03-18｜Gary Corona (CFO)｜margin：Trachte與EPG利潤率預期向事業部平均靠攏（原話："we're applying our integration playbook, and we expect their"）
- 2026-03-18｜Gary Corona (CFO)｜margin：管理層承認部分逆風會持續（原話："Looking ahead, while some of these headwinds will persist"）
- 2026-03-18｜Brian Coleman｜margin：Electrical Connections 2025年利潤率逾28%、銷售13億美元（原話："Electrical Connections had record sales of $1.3 billion and"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：2025年自由現金流金額與年增（原話："$561 million of free cash flow, up 31% year-over-year"）
- 2026-03-18｜Gary Corona (CFO)｜margin：口徑：2023–2025併購貢獻4點（扣除熱管理出售後）（原話："Organic sales growth of 8% exceeded our targets."）
- 2026-03-18｜Gary Corona (CFO)｜margin：2023年舊框架的有機成長目標為中個位數（原話："calling for mid-single-digit organic growth, 1 point"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：CFO稱自2023年投資人日以來達成或超過每個中期目標（原話："have met or exceeded every midterm target we set"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：管理層對持續擴張利潤率表示有信心（原話："healthy, and we're confident in our ability to continue to"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：併購須三年內報酬率超過資本成本（原話："requirement that acquisitions align with our strategy and"）
- 2026-03-18｜Gary Corona (CFO)｜commitment：CFO表示約六週後會就通膨與關稅提供更多說明（原話："We'll be together in about six weeks,"）
- 2026-03-18｜Beth Wozniak (CEO)｜commitment：管理層表示一向希望成長快於市場（原話："we always want to grow ahead of those targets"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：2023–2025年共部署53億美元資本（原話："From 2023 to 2025, we deployed $5.3 billion of"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：淨槓桿1.6倍，低於2–2.5倍目標區間（原話："we ended 2025 with net leverage of 1.6x, well below our"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：股利自2023年投資人日起增加約20%，並以回購抵銷稀釋（原話："We're committed to a competitive dividend, which has"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：2025年ROIC約13%（原話："ROIC of approximately 13%, up from 2022"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：近期併購成果：部分標的進場時利潤率低於預期（原話："Some of these businesses came into nVent with margins below"）
- 2026-03-18｜Gary Corona (CFO)｜capital_allocation：CFO稱近期併購皆達到報酬目標（原話："and all of the recent deals have met those expectations."）
- 2026-03-18｜Beth Wozniak (CEO)｜capital_allocation：CEO談併購：未來可為較大型的補強併購（原話："can be larger bolt-on deals"）
- 2026-03-18｜Sara Zawoyski｜product：液冷滲透率預估：現約10–15%，2028年逾30%（原話："utilize liquid cooling, which we expect to be over 30% by"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：管理層引用的液冷市場成長率（原話："is expected to grow more than 35%"）
- 2026-03-18｜Sara Zawoyski｜product：液冷產能自2023年中增加逾八倍（原話："liquid cooling production capacity more than eightfold"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：Blaine新廠預計年底前使液冷產能約增一倍（原話："approximately double our liquid cooling capacity by year-end"）
- 2026-03-18｜Aravind Padmanabhan｜product：新CDU宣稱單台可支援多個機櫃（原話："whereas competitors need multiple CDUs to achieve the same"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：首次揭露每百萬瓦約100萬美元的資料中心內容量機會（原話："approximately $1 million per megawatt."）
- 2026-03-18｜Beth Wozniak (CEO)｜product：CEO說明該數字為首次公開（原話："but this is the first time that we've shared that"）
- 2026-03-18｜Sara Zawoyski｜product：資料中心銷售（Systems Protection）逾8億美元、三年成長約40%（原話："million and have grown roughly 40% over the last three years"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：口徑：公司層級白空間約75%、灰空間25%（原話："75% of sales. And the gray space makes up 25%."）
- 2026-03-18｜Sara Zawoyski｜product：口徑：Systems Protection 白空間占比（原話："Systems Protection sales in the white space."）
- 2026-03-18｜Brian Coleman｜product：線槽（WBT）產品線成長率與液冷相當（原話："at rates comparable to liquid cooling"）
- 2026-03-18｜Sara Zawoyski｜product：服務收入預期隨時間累積（原話："service revenue to kind of build over time"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：800V DC：電力連接產品已達800V DC額定（原話："power connections that are already rated to 800-volt DC"）
- 2026-03-18｜Beth Wozniak (CEO)｜product：800V DC：仍需AC系統（原話："there's still going to be a need for AC systems"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：對液冷標準的看法：避免任何人都可自稱有CDU（原話："that they have a CDU, but you may not know for what"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：回應Vertiv、Eaton、Schneider：不須有HVAC才能做液冷（原話："no one has ever said, oh, you're not in HVAC"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：回應Envicool問題：業界在尋找更多供應商（原話："companies are just looking for more and more suppliers"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：對冷板/浸沒技術保持中立（原話："we are agnostic to whether it is a cold plate or immersion"）
- 2026-03-18｜Beth Wozniak (CEO)｜competition：定位在白空間技術冷卻系統而非設施冷卻（原話："we talk about the technology cooling system that is in the"）
- 2026-03-18｜Aravind Padmanabhan｜customer：與NVIDIA夥伴網路關係（原話："companies who are part of NVIDIA's partner network."）
- 2026-03-18｜Beth Wozniak (CEO)｜customer：資料中心需求能見度來自超大規模客戶（原話："we're getting good visibility because we're working with"）
- 2026-03-18｜Beth Wozniak (CEO)｜customer：積壓訂單23億美元，約為一年前3倍（原話："a backlog of $2.3 billion, 3x"）
- 2026-03-18｜Gary Corona (CFO)｜risk：關稅：232金屬為主要關稅影響（原話："232 metals are the primary tariff impact for us"）
- 2026-03-18｜Gary Corona (CFO)｜risk：通膨：年初預估全部含關稅約中個位數（原話："the year, we estimated about mid-single digits all in"）
- 2026-03-18｜Gary Corona (CFO)｜risk：價格轉嫁靠經銷商漲價（原話："delivering the price increases that we need to cover"）
- 2026-03-18｜Sara Zawoyski｜risk：液冷換機週期長度尚未定義（原話："I think it's too early just in terms of where we're at"）

### 問答異常語氣（迴避／改口／保留）
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Sprague：Systems Protection 財測似乎 Q3、Q4 營收較 Q2 持平或略降，是否有供應鏈問題？｜答法：CFO 轉談 2 年疊加成長加速；CEO 回答為「規劃審慎」，未直接說明 Q3 是否有供應鏈限制，也未回應序列走勢。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Joe Ritchie／Nicole DeBlase：積壓訂單年底是否會成長、$25 億是否合適水位？｜答法：CEO 回「hard to say」「probably around the right level」，並自問自答式確認，未給方向。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Nicole DeBlase：Q3 訂單強勁開局是否代表訂單成長較 Q2 加速？｜答法：CEO 未答加速與否，只說有短週期強勢與一些大型不均訂單。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Scott Graham：Q3 有機財測是否有上檔空間、是否由液冷積壓出貨驅動？｜答法：CFO 未回答上檔空間或液冷出貨占比，改談 2 年疊加 50% 與財測審慎。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Scott Graham：下半年增量利潤率 20% 中段，過去提過的 30% 是否仍是延伸目標？｜答法：CFO 未回應 30%，重申 Investor Day 中期目標為 20% 中段，並改談 EPS 為 2024 年兩倍以上。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond：$20 億資料中心營收中液冷與其他的占比？｜答法：CEO 稱尚未拆分，僅稱液冷為顯著貢獻；CFO 改談整體組合廣泛。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond／Joe Ritchie：EC 利潤率後續軌跡是否更高？｜答法：CFO 兩次皆只答預期持續進步、落在 20% 後段，未給具體數字或時點。
- NVT_Q2_2026_Earnings_Call_20260731.md｜問：Brian Drab：近 12 個月訂單成長率是否明顯高於本季低雙位數？｜答法：CFO 僅答「是」，未提供數字。
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Q1財測/訂單趨勢：新聞稿稱第一季優於預期，是什麼意思？｜答法：CEO表示不想評論該季，只說進展順利，未給數字或訂單更新
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：資料中心營收中電力管理與冷卻的比重｜答法：CEO稱未拆分、也未更新，只說液冷最大
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：10%–13%有機成長如何拆到資料中心與公用事業｜答法：CEO指向簡報圖表，只說資料中心最高、公用事業次之，未給拆分數字
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Engineered Building Solutions 的產業成長率與資料中心/公用事業占比｜答法：未給產業成長率；稱成長率與公用事業相近，占比只說多數為公用事業
- NVT_Analyst_Investor_Day_nVent_Electric_plc_20260318.md｜問：Google與Envicool洽談，中國競爭者在美國是否更具威脅｜答法：未直接回答威脅程度，改談需求龐大與廠商尋找更多供應商

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B 衛星候選：thesis 完整（A 級執行 9/10、AI 數據中心液冷超級週期、Trachte/EPG systems integrator 轉型）但估值 🟡 + MA stretched + 短期 R:R 負值 + 4 週 +25.5% 漂移 = 時機不到。等回測 BB 中軌 $127 區 或 Fwd PE 28x $140 區 + Q2/Q3 26 backlog 維持 +100%+ YoY 後分批進場 3-5% 衛星倉。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"液冷超級週期持續 5+ 年，NVT systems integrator 角色拿到 SAM 15-20%","columns":{"2Y 驗證點":"FY26 sales ≥ guide $4.9-5.0B + Q3/Q4 26 backlog YoY 維持 &gt; +100%","5Y 驗證點":"FY28 sales ≥ $6.5B（含液冷 + 模組化 DC）+ data center 占比 ≥ 40%","10Y 驗證點":"FY30 sales ≥ $8.5B + 全球液冷 SAM 滲透 15-20%","具體數字門檻":"FY26 公司 guide / FY27 +20% 共識 / FY30 公司 long-term target","信息來源":"公司 guidance + sell-side consensus + Yole / GMI 液冷市場報告","漂移觸發條件":"連 2 季 TTM revenue &lt; consensus −5% → H1 削弱"}},{"id":"H2","text":"Trachte + EPG 收購整合 18-24 個月後 synergy 兌現至 EPS +$0.50-0.80","columns":{"2Y 驗證點":"Q2-Q4 26 quarterly synergy 揭露 + EPG cross-sell 案例","5Y 驗證點":"2027-28 systems integrator 角色帶 customer lock-in 顯化在 GM / OPM 提升","10Y 驗證點":"合併 entity FY30 OPM ≥ 22%（vs FY25 ~17.5%）","具體數字門檻":"EPG 收購時管理層宣示 $80M synergy / 24 個月；FY30 OPM 22% 為管理層 long-term target","信息來源":"5/1 Q1 26 法說 + 後續法說會跟進","漂移觸發條件":"連 2 季 OPM 增速 &lt; +0.5pp QoQ → H2 削弱"}},{"id":"H3","text":"估值倍數 Fwd PE 33-35x 維持在 28-30x 區間（不再大幅向上）","columns":{"2Y 驗證點":"2026H2 股價回測 $135-150 區，Fwd PE 28-30x","5Y 驗證點":"2027-28 隨 EPS 成長自然 PE 下降至 24-26x","10Y 驗證點":"2030 估值 reset 至 GARP 標準 PE 20-22x","具體數字門檻":"PE 28-30x 是 NVT 結構性高成長期合理上限；&gt; 35x 不可持續","信息來源":"5Y 歷史 Fwd PE band + 同業 VRT / ETN / SU 估值對比","漂移觸發條件":"連 2 季 Fwd PE &gt; 38x → 估值倍數脫鉤"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI hyperscaler capex 2027 提前放緩","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"NVT backlog YoY + hyperscaler capex guidance（MSFT / META / GOOG / AMZN）","警戒閾值":"連 2 季 backlog YoY &lt; +50% + 2 家 hyperscaler 下修 capex → R1 觸發"}},{"id":"R2","text":"Trachte + EPG synergy 不如預期 / 整合失敗 / goodwill impairment","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"EPG 揭露的 cross-sell 案例 + OPM 改善速度 + goodwill 帳面值","警戒閾值":"FY27 OPM 仍卡在 17-18% 未進到 19-20% → H2 削弱"}},{"id":"R3","text":"Vertiv / Schneider 等同業在液冷市場拿走更多 share","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"液冷市場 share 報告（Yole / GMI 年度更新）+ 大型 hyperscaler 訂單揭露","警戒閾值":"2028 全球液冷 NVT share &lt; 8% → R3 觸發 + 估值倍數 reset"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":164.66,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NVT","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"nVent Electric plc"},"oneliner":"資料中心液冷與電力配送帶動營收年增四成、財測三度上修，但有機訂單只年增低雙位數，又在高點舉債併購 Maverick；股價半年跌 24%，FY2027 本益比 18.5 倍，生意好、價格合理，風險集中在 2027 年資料中心訂單會不會轉負。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/scenario.json","answers":{"q1_business":{"verdict":"賣電氣保護與連接產品（機殼、接地與連接件、液冷分配單元、模組化機房，併入 Maverick 後再加開關設備）給資料中心、電網、工業與商辦住宅。錢卡在『規格寫進設計＋經銷通路＋快速擴產交付』這個節點。2026 年基礎設施占營收近六成，資料中心同時是成長與風險的單一來源。","reasoning":"第三季營收 15.15 億美元，報告與有機皆年增 44%；調整後營業利益率 22.1%（年增 190bp），GAAP 營業利益率 18.6%，自由現金流 2.68 億美元。分部方面，Systems Protection 10.98 億美元（年增 53%，ROS 23.0%），Electrical Connections 4.17 億美元（年增 23%，ROS 28.2%）。全年財測為報告營收成長 48–49%、調整後 EPS 5.36–5.39，第四季 1.30–1.33。單點依賴：最大客戶（屬 Systems Protection）約占 2025 年營收 11%、年底應收 11%，2024 年沒有客戶超過 10%，集中度在上升；目前未見該客戶導入第二供應商的具體證據。產業時鐘判擴張期，依據是變壓器與高壓設備交期仍 2–3 年、同業新產能多在 2027–28 年才投產，nVent 自身也還在擴產（Blaine 2 與亞利桑那廠都在 2027 年中投產）。不過有機訂單只年增低雙位數，遠低於營收成長，第四季有機成長財測也降到 26–29%，屬擴張後段的訊號。供需持久性判結構性為主、帶週期，供給可逆性中等。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_non_gaap_adjusted_operat","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow","f_kpi5_guidance_q4_fy2026","f_kpi6_guidance_fy2026","f_kpi7_systems_protection_sales","f_kpi8_electrical_connections_s","f_earnings_recency"],"verdict_values":{"revenue_quality":"長短週期混合。機殼與連接件多經電氣經銷商、承包商與 OEM 短週期出貨，管理層稱 sell-in 與 sell-out 平衡；資料中心液冷與 Maverick 開關設備屬長週期大單，訂單不均。季末在手訂單 26 億美元，約當 5 個月營收，能見度有限。","unit_econ_note":"資料中心內容量：2026-03-18 投資人日首次揭露每百萬瓦約 100 萬美元，2026-10-30 法說稱併入 Maverick 後約 200 萬美元。新品貢獻第三季約 30 個百分點營收成長，新品活力已達投資人日目標 30%。單價與數量的拆分事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"分拆後靠併購轉型、由 AI 資料中心量能推動的電氣設備商：利潤率與現金轉換好，但成長高度集中在資料中心資本支出週期"},"industry":{"clock_phase":"II","sd_verdict_source":"判結構性持久、帶週期。支持面：Rystad（2026-05）稱歐美變壓器與高壓斷路器交期至少 2–3 年，Wood Mackenzie 調查電力變壓器平均交期 128 週，Goldman 與 Citi（二手轉述）估 2026–28 年供給低於需求。反向證據：Wood Mackenzie（2025-09）稱交期已見改善、低壓變壓器可能轉為過剩。公司端在手訂單由 25 億升到 26 億美元、有機訂單年增低雙位數，供給可逆性中等，熊市機率因此取 30%。","bargaining":{"up":"上游議價力偏強：鋼鋁銅受 232 關稅影響，2026 年關稅衝擊約 1.05 億美元；管理層稱供應商也在擴產、要一起放量，第四季財測因供應鏈刻意保守。","down":"下游分兩群。經銷通路分散、規格寫入，議價力弱；超大規模雲端與託管業者直接採購、單案大，會尋求更多供應商，議價力強。最大客戶約占營收 11%。","geo":"依賴墨西哥與中國生產的零組件與成品，有貿易與關稅風險；部分產品屬兩用產品，受出口管制。歐洲、亞洲資料中心正在擴張，公司在當地加碼商務與製造。"},"profit_pool_dir":"利潤池往資料中心電力與散熱移動，nVent 的基礎設施占比由分拆時 12% 升到近 60%。份額數據事實表未涵蓋，只能用成長率間接推斷公司有分到池子。","tam_table":[{"item":"公司稱總可及市場","value":"逾 1,500 億美元（2026-10-30 法說 CEO）"},{"item":"液冷占資料中心冷卻滲透率","value":"目前 10–15%，管理層預估 2028 年逾 30%（2026-03-18 投資人日）"},{"item":"液冷市場成長率","value":"管理層引用逾 35%（2026-03-18 投資人日）"},{"item":"每百萬瓦內容量","value":"約 100 萬美元（投資人日）→併入 Maverick 後約 200 萬美元（2026-10-30 法說）"},{"item":"基礎設施占營收","value":"分拆時 12%→2025 年 45%→2026 年迄今近 60%"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平，等級 B：執行力在擴大，定價力在縮小，兩者相抵。","reasoning":"護城河機制是規格寫入加經銷通路，再加上資料中心液冷的工程能力與擴產速度。10-K 自承不依賴單一專利、客戶或品牌，也點名新進者與低價廠。執行力給 9 分：2026 年三度上修財測、Blaine 1 約 100 個工作天投產、新品活力 30%、Systems Protection ROS 年增 260bp。定價力給 6 分：第三季價格幾乎獨力抵銷約 6,000 萬美元通膨（含約 2,000 萬關稅），但毛利率由 2023 年 40.3% 降到 TTM 37.0%，Electrical Connections ROS 連兩季年減，管理層歸因於產品組合與成長投資。營益率 17.1% 落後 VRT 的 20.4% 與 HUBB 的 20.2%；FCF 率 12.0% 是同業最低，但有口徑爭議，見矛盾段。同業 ROIC 事實表未涵蓋，改以營益率代理，對最強同業落後約 3 個百分點。當期 ROIC 約 13%（2025 年，投資人日 CFO），利潤率高，但併購商譽讓資本周轉偏低。產業態勢判雙向拉鋸。競爭面：Vertiv 2026-04 收購 Strategic Thermal Labs 強化液冷工程，客戶也在找更多供應商。結構面：電力設備交期 2–3 年，新產能 2027–28 年才集中投產。其他結構變數：鋼鋁銅關稅，以及 800V DC 架構轉換（80 多家廠商支持開放規格；nVent 連接件已達 800V DC 額定，Maverick 有 800V DC 機架）。","fact_refs":["f_peer_nvt_gross_margin_pct","f_peer_nvt_operating_margin_pct","f_peer_nvt_fcf_margin_pct","f_peer_hubb_gross_margin_pct","f_peer_hubb_operating_margin_pct","f_peer_hubb_fcf_margin_pct","f_peer_etn_gross_margin_pct","f_peer_etn_operating_margin_pct","f_peer_etn_fcf_margin_pct","f_peer_vrt_gross_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_vrt_fcf_margin_pct","f_kpi7_systems_protection_sales","f_kpi8_electrical_connections_s","f_kpi1_non_gaap_adjusted_operat"],"verdict_values":{"moat":{"mechanism":"規格寫入＋電氣經銷通路＋資料中心液冷與電力的系統工程與快速擴產","execution":9,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面在擴大：2026 年三度上修財測、Blaine 1 約 100 個工作天投產、新品約貢獻 30 個百分點成長、Systems Protection ROS 年增 260bp。定價面在縮小：毛利率 2023 年 40.3%→2025 年 37.7%→TTM 37.0%，Electrical Connections ROS 第二季年減 140bp、第三季年減 180bp，營益率落後 VRT 與 HUBB 約 3 個百分點。兩者相抵，判持平。","competitor_notes":[{"name":"HUBB","strategy_note":"營益率 20.2%、FCF 率 14.1% 都高於 nVent，業務偏電網與公用事業，是 Electrical Connections 的直接標竿；nVent 這一段利潤率在年減，差距沒有縮小。"},{"name":"ETN","strategy_note":"毛利率 35.9%、營益率 17.7% 與 nVent 相近，資料中心電力配送規模大，和新併入的 Maverick 開關設備正面重疊，也是 800V DC 開放規格的支持者之一。"},{"name":"VRT","strategy_note":"毛利率 38.1%、營益率 20.4%、FCF 率 23.7% 全面領先，2026-04 收購 Strategic Thermal Labs 補強液冷工程，是液冷段最強的對手。"},{"name":"SU.PA","strategy_note":"事實表無財務資料；它是設施端電力與散熱的全套供應商，也是 800V DC 開放規格的支持者之一。"}],"spread_notes":{"proxy":"TTM 營業利益率","nvt_pct":17.1,"best_peer":"VRT","best_peer_pct":20.35,"spread_pp":-3.25,"note":"同業 ROIC 事實表未涵蓋。NVT 的 TTM 截至 2026-06，HUBB 與 VRT 截至 2026-09，期間差一季。"},"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用 TTM 營益率與 FCF 率代理；SU.PA 無財務資料。","threats":[{"level":"🔴","text":"生態型攻擊：Vertiv、Schneider、Eaton 能同時賣設施端散熱與電力全套，Vertiv 2026-04 收購 Strategic Thermal Labs 補強液冷工程。若超大規模客戶改採整套採購，nVent 的白空間液冷單品會被打包壓價。","p":0.35,"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#0"]},{"level":"🟡","text":"點對點低價競爭：10-K 點名區域廠、低成本製造商與新進者。投資人日被問到 Envicool 與 Google 洽談時，CEO 沒有正面回答威脅程度，只說客戶在找更多供應商。","p":0.3,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"架構轉換：資料中心配電由 415V AC 轉向 800V DC，可能改寫機櫃電力內容。nVent 連接件已達 800V DC 額定，Maverick 也有 800V DC 機架，目前看機會大於威脅，但還沒有訂單證據。","p":0.2,"evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（機房營運）、決策者（設計與採購工程）、付款者（雲端與託管業者）三者一致。高密度 AI 機櫃的散熱與電力保護是物理上的需要，不是想要；CEO 2026-10-30 稱更多電力就有更多熱、就要更多冷卻。電氣機殼與接地連接多為法規與規格要求。急迫性高不等於持久，時點上的週期風險另列在風險一。"},{"item":"決策層級","level":"🟡","text":"決策的最小單位是超大規模客戶的單一建置案與晶片世代。每一代架構都要重新認證，客戶也在找更多供應商（2026-03-18 投資人日 CEO 回應 Envicool 提問）。最大客戶 2025 年約占營收 11%，2024 年沒有客戶超過 10%，集中度上升。經銷通路的機殼與連接件因規格寫入、單價占專案比重低，轉換誘因小。漲價後流失率、續約率等代理變數事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"AI 機房價值鏈的利潤主要落在晶片端。nVent 每百萬瓦內容量約 100 萬美元，併入 Maverick 後約 200 萬美元。毛利率 37% 與同業 35–38% 相近，營益率落後最強同業約 3 個百分點；關稅靠漲價轉嫁後利潤率仍擴大。這代表這個環節賺得到錢，但不是最難取代的一環。開放規格（800V DC 有 80 多家廠商支持）讓互補品標準化，壓縮差異化空間。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的工業品，沒有消費者價格敏感或政治定價上限，也不依賴監管授權。政策面風險在關稅與兩用產品出口管制，屬成本與市場進入問題，已列在風險三，不構成價格天花板。"}],"roiic":16,"reinvest_rate":90,"endo_ceiling":14.4,"formula_note":"單位為百分比。當期 ROIC 約 13%（2025 年，投資人日 CFO），目標是 2028 年超過 15%。增量 ROIC 粗估 12–20%，取中值 16%：若投入資本三年內因 Maverick（17.5 億美元＋最多 5.5 億）與擴產增加約 40%，ROIC 又由 13% 升到 15%，推得增量報酬約 20%；Maverick 首年利潤率只有中十位數、扣利息後只貢獻幾美分，把下緣壓到 12%。再投資率約 90%＝（資本支出－折舊＋營運資金增加＋併購淨額）÷稅後營業利益，參考 2023–2025 年部署 53 億美元、其中部分資金來自業務出售所得，單年波動極大（2026 年光 Maverick 就超過全年稅後營業利益）。內生上界＝16%×90%≈14.4%。投入資本、折舊與營運資金事實表未涵蓋，以上皆為粗估。"}}}},"q3_growth":{"verdict":"五年後跑道中等：液冷滲透率預計 2028 年就超過 30%，第二條曲線（800V DC 電力、服務）還沒有證實。","reasoning":"成長以量為主，來自資料中心液冷、機櫃與電力產品出貨；再加上併購（2026 年約貢獻 10 個百分點營收成長，2027 年 Maverick 全年併入，年化營收約 8 億美元），以及用價格抵銷通膨。回購貢獻可忽略。共識 EPS：2025 年調整後約 3.36 美元（由 CFO 稱 2026 財測中點年增 60% 回推）→2026 年 5.17→2027 年 6.78→2028 年 8.05（Koyfin 快照，家數未揭露；營收共識 2026 年 8 家、2027 年 10 家），三年年複合約 34%，只看 2026→2028 兩年約 25%。內生上界約 14%（見護城河題），缺口約 19 個百分點。其中一部分可以由併購（2026–27 年合計約 20 個百分點營收）與利潤率擴張（第三季調整後 ROS 由 20.2% 升到 22.1%）解釋；剩下是資料中心量能的週期性放大，無法用再投資歸因，標『依賴re-rate』：若市場照共識外推，價格就要靠倍數撐住。基準情境因此不採用共識的 2028 年 8.05，改用 7.85。跑道方面，液冷目前占資料中心冷卻 10–15%，管理層預估 2028 年超過 30%，照此約 2 年就到 30%；之後滲透率還能往上，但五年後會落在 35–70% 區間。第二條曲線（800V DC 電力機架、服務、電網工程建築）目前還沒有營收證據，所以判中等。衰退訊號十項亮 1 盞（毛利率下滑），產業倍數一項為資料缺口。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_guidance_fy2026","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct","f_kpi0_net_sales_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（資料中心液冷、機櫃、電力產品出貨）＋併購（2026 年約 10 個百分點，2027 年 Maverick 全年併入）＋價格抵銷通膨；回購貢獻可忽略","runway_years":"約 2 年（液冷占資料中心冷卻由 10–15% 升到 30%，管理層預估 2028 年）","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河題的再投資推導：增量 ROIC 約 16%×再投資率約 90%≈14.4%，不另算","segments":[{"item":"Systems Protection 第三季","value":"營收 10.98 億美元，年增 53%（有機 54%），調整後 ROS 23.0%（年增 260bp），其中基礎設施年增約 90%"},{"item":"Electrical Connections 第三季","value":"營收 4.17 億美元，年增 23%，調整後 ROS 28.2%（年減 180bp），管理層歸因於組合與成長投資"},{"item":"基礎設施占營收","value":"分拆時 12%→2025 年 45%→2026 年迄今近 60%"},{"item":"Maverick","value":"2026-10-01 併入 Systems Protection，第四季約貢獻 19 個百分點營收成長（約 2 億美元），利潤率中十位數"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":true,"evidence":"年度毛利率 2023 年 40.3%→2025 年 37.7%→TTM 37.0%；季度毛利率事實表未涵蓋，由 TTM 低於年度推斷仍在年減"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"無份額數據，成長率快於自身歷史"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"價格抵銷通膨的同時營收年增 44%"},{"signal":"EPS成長顯著高於營收成長","lit":false,"evidence":"2025→2027 共識 EPS 年複合約 42%、營收約 39%，差距約 3 個百分點"},{"signal":"FCF/淨利低於0.75連2年","lit":false,"evidence":"2025 年報表口徑 0.52 受處分利益扭曲，2024 年 1.72；2026 財測轉換率 90–95%"},{"signal":"SBC/營收大於5%且逐年上升","lit":false,"evidence":"約 0.7%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"evidence":"公司稱可及市場逾 1,500 億美元；800V DC 目前屬機會"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占FCF大於60%","lit":false,"evidence":"2026 資本支出約 1.4 億美元，多為新產能"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"Blaine 2 與亞利桑那廠擴產中"}],"trap_rating":"價值陷阱風險🟡、長期成長性🟡（亮 1 盞，另 1 項資料缺口）"}}},"q4_capital":{"verdict":"資本配置以併購為主軸：2026 年以現金 17.5 億美元（另有最多 5.5 億績效對價）買下 Maverick，資本支出約 1.4 億、回購 1 億、股利約 1 億。SBC 約占營收 0.7%，現金轉換率財測 90–95%。三項檢核中只有股權稀釋確定過關，併購報酬待證，回購在 24 倍本益比下不划算。","reasoning":"2026 年現金去向：併購是大宗，10-01 以現金約 17.5 億美元完成 Maverick，2027–28 年另有最多 5.5 億美元績效對價；資本支出約 1.4 億美元（年增 50%，多為資料中心、電網與供應鏈韌性的新產能）；前三季回饋股東 2.02 億美元（回購 1 億、股利約 1.02 億，季股利年增 5%）。融資：2026-09 發行 8 億美元 10 年期、票息 6.150% 的優先債。季末現金逾 11 億、總債務約 22 億美元、循環額度 6 億可用，管理層預期年底槓桿落在 2–2.5 倍目標內（2025 年底 1.6 倍、2026 年中 1.2 倍）。現金轉換：第三季 FCF 2.68 億美元，對調整後 EPS 1.52 換算的淨利約 1.1 倍；Q2 法說維持全年轉換率 90–95%。2025 年報表口徑的 FCF÷淨利只有 0.52，但淨利含處分利益，FCF 口徑也與公司自報的 5.61 億不同，見矛盾段。SBC 約占營收 0.7%。三項檢核：股權稀釋過關；回購在 24 倍本益比下盈餘殖利率約 4.1%，不過關；併購報酬管理層自述達標但個案未揭露，Maverick 待驗證，不判過關。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"管理層稱近期併購皆達三年內報酬超過資本成本的要求（2026-03-18 投資人日 CFO），但個案報酬未揭露，部分標的進場時利潤率也低於預期。Maverick（17.5 億美元＋最多 5.5 億績效對價）首季利潤率中十位數，報酬要到 2027–28 年才驗得到。事實表未涵蓋，不判過關。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"2026 年迄今回購 1 億美元。回購均價事實表未涵蓋，以現價前瞻本益比 24.2 倍換算盈餘殖利率約 4.1%；只要 10 年期公債殖利率高於 2.1% 就低於門檻（10 年期殖利率事實表未涵蓋）。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九個月 SBC 3,090 萬美元，以第三季營收年化約占營收 0.7%、約占市值 0.2%；管理層稱以回購抵銷稀釋，淨稀釋遠低於 1.5%。"}]},"governance":{"capital_returns":[{"item":"2026 年迄今回饋股東","value":"2.02 億美元（回購 1 億、股利約 1.02 億），季股利年增 5%"},{"item":"2026 年資本支出","value":"約 1.4 億美元，年增 50%（含 Maverick），前三季已支出 9,500 萬"},{"item":"併購","value":"Maverick 現金約 17.5 億美元＋2027–28 年最多 5.5 億績效對價；管理層預期每年都有交易"},{"item":"融資","value":"2026-09 發行 8 億美元 10 年期 6.150% 優先債；年底槓桿預期 2–2.5 倍"},{"item":"2023–2025 年資本部署","value":"53 億美元（投資人日 CFO）"}],"sbc":{"sbc_9m_musd":30.9,"note":"以第三季營收年化粗估約占營收 0.7%，回購足以抵銷"}}}},"q5_valuation":{"verdict":"現價要求 2027–28 年 EPS 照共識走到 8 美元左右、倍數守在 18–20 倍；這個前提我信，只要資料中心訂單不轉負。估值合理，不便宜。","reasoning":"現價 125.19 美元，等於 2026 年共識 EPS 5.17 的 24.2 倍（以上修後財測中點 5.375 計約 23.3 倍），也等於 2027 年共識 6.78 的 18.5 倍。基準情境假設 2031 年 EPS 10.25、終端 20 倍，等於倍數從 24 倍降到 20 倍，報酬全部來自盈餘成長。三年共識 EPS 年複合約 34%，PEG 約 0.7；改用 2026→2028 兩年約 25% 計算，PEG 約 1.0。歷史倍數只有四個年度端點（本益比 75 分位、股價營收比 62、EV/S 54），不是五年分位，所以五年分位留空。短期上檔 13.2%＝2027 年基準 EPS 6.75×21 倍＝141.75 美元；中期上檔 39.0%＝2029 年基準 EPS 8.70×20 倍＝174 美元。賣方目標價均值 188–204 美元、全距 136–240 美元，但資料是 2026-08 的，早於本季財報與這波下跌，也還沒看到 11 月更新。現價低於最低目標價，方向上支持價格已消化部分減速，但資料陳舊，不當作依據。同業倍數事實表未涵蓋，終端倍數只能用自身前瞻倍數校準，這是本題的資料缺口。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_rev_consensus_fy1_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_kpi6_guidance_fy2026","f_week26_return_pct","f_rsi14","f_ma_state","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2026 年共識調整後 EPS 5.17，財報前快照；公司財測中點 5.375）","tier":"電氣設備與資料中心基礎設施（同業 HUBB、ETN、VRT、Schneider）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV/S；本題以公司自身年度端點分位與共識 EPS 路徑當尺，同業倍數缺口已在理由中點名"},"fwd_pe":24.21,"peg":0.72,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 24.2 倍、2027 年 18.5 倍；PEG 約 0.7（兩年口徑約 1.0）；歷史本益比位於四個年度端點的 75 分位。PEG 看起來便宜，但分子是週期高點附近的資料中心盈餘，訂單成長也已降到低雙位數，所以判合理而非便宜。股價跌到 108 美元以下（2027 年 16 倍）才算便宜。","targets":{"sell_side_avg_low":188.22,"sell_side_avg_high":204.07,"range_low":136,"range_high":240,"as_of":"2026-08","note":"各聚合站數字不一，早於本季財報；全距高低比約 1.8 倍"},"upside_short_pct":13.2,"upside_mid_pct":39.0,"denominator_disputed":false,"denominator_note":"兩處分母要校正。一、2026 年共識 EPS 5.17 是財報前快照，低於上修後財測 5.36–5.39，以財測計前瞻本益比約 23.3 倍。二、EV 用的淨負債 12.24 億美元是 9 月底數字，還沒扣掉 10-01 支付的 Maverick 現金約 17.5 億美元；交割後淨負債約 29.7 億、EV 約 232 億美元，前瞻 EV/S 約 4.0 倍而非 3.69 倍，績效對價最多再加 5.5 億。兩者都不是爭點，校正後估值結論不變。"}}},"q6_how_wrong":{"verdict":"最可能看錯在資料中心建置的時點：若 2027 年訂單轉負，盈餘與倍數會一起下修。陷阱風險中等，最大回撤要準備 −35%～−50%。","reasoning":"壓力測試三組，以共識 2028 年 EPS 8.05 為第三年基礎：成長降到 15% 給 22 倍＝177 美元；降到 10% 給 18 倍＝145 美元；降到 5% 給 14 倍＝113 美元。三組過兩組，只有 5% 那組低於現價 125.19。熊市情境用 15 倍，介於 10% 與 5% 兩組之間，因為熊市路徑的 EPS 年複合只有約 4%。最大回撤推導：熊市情境 2028 年 EPS 約 5.0，乘 16 倍約 80 美元（−36%），乘 12.5 倍約 63 美元（−50%），後者也約等於跌破 250 週均線 72.5 美元後再跌 13%。股價目前低於 52 週均線 136.4、高於 104 週均線 105.3，RSI 34.6，沒有過熱。反證細節見三個視角的反證紀錄，這裡不重寫。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_consensus_eps_fy3","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點盈餘加上毛利率下滑，非典型價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.17,"pe":24.21,"basis":"2026 年共識調整後 EPS（Koyfin 財報前快照；已過三季，公司財測中點 5.375）；終端倍數同樣乘在當年度 EPS 上"},"valuation_basis":"eps_pe","eps":{"bull":[7.1,8.7,10.2,11.6,12.9],"base":[6.75,7.85,8.7,9.5,10.25],"bear":[6.25,5.0,4.95,5.55,6.2]},"pe":{"bull":25,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.67,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-35,"basis":"起點 125.19 美元。高端 −35%（約 80 美元）＝熊市情境 2028 年 EPS 約 5.0 乘 16 倍；低端 −50%（約 63 美元）＝同一盈餘乘 12.5 倍，也約等於跌破 250 週均線 72.5 美元後再跌 13%。佐證：財測三度上修期間，股價仍由 2026-05 的 164.66 美元跌到 125.19 美元（−24%），可見光是情緒面回撤就能到兩成以上；盈餘真的下修時，還會再疊一層倍數壓縮。","trigger_time":null},"basis":{"bull":"資料中心建置延續到 2029 年，液冷滲透率 2028 年過 30% 後續升，Maverick 讓每百萬瓦內容量翻倍並兌現；2027 年有機成長 ≥20%，ROS 升到 24%；終端 25 倍（現值 24.2 倍）","base":"2027 年有機成長收斂到 12–15%，加上 Maverick 全年併入；2028 年起有機成長 8–10%，每年小型併購補幾個百分點；調整後 ROS 21–23%；終端 20 倍（低於現值 24.2 倍；同業倍數事實表未涵蓋，以自身前瞻倍數與成長降速校準）","bear":"2027 下半年資料中心建置進入消化期，2028 年營收年減約一成、遞減利潤率約 35%，EPS 回落到 5 美元後緩步回升；Maverick 利潤率停在中十位數；終端 15 倍，介於成長降到 10%（18 倍）與 5%（14 倍）兩組之間，因為熊市路徑 EPS 年複合只有約 4%"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"第三季有機訂單只年增低雙位數（去年同季 +65%），營收卻年增 44%，連兩季營收成長遠高於訂單；在手訂單 26 億美元約當 5 個月營收；第四季有機成長財測降到 26–29%。Wood Mackenzie 稱電力設備交期已見改善、低壓變壓器可能過剩；同業與 nVent 的新產能集中在 2027–28 年投產。","assumption":"超大規模客戶的資料中心建置延續到 2028 年以後。","consequence":"2027 下半年起資料中心進入消化期，2028 年營收年減約一成、EPS 回落到 5 美元，倍數壓到 12–16 倍；五年後股價仍低於現價，持有期間最深可到 −50%。","ruling":"部分採納。訂單落後營收是真的領先訊號，但有兩個抵銷證據：去年同季訂單基期是 +65%，以及 Q2 法說稱公司刻意消化在手訂單、縮短交期。十月訂單管理層稱非常強，在手訂單也仍在季增。處理方式是熊市機率取 30%、訂單轉負就減碼，現在不砍論點。這個視角與唯一致命點（訂單轉負）是同一件事。","watch":"每季有機訂單年增率與季末在手訂單；2027-02 首次揭露的 Maverick 在手訂單。","evidence_refs":["supply_demand_durability#3","end_markets#3","supply_demand_durability#1"]},{"view":"論點成功但股東經濟變差","evidence":"在週期高點以現金 17.5 億美元＋最多 5.5 億績效對價收購 Maverick，首季利潤率只有中十位數、扣利息後只貢獻幾美分；毛利率三年降約 3 個百分點；Electrical Connections ROS 連兩季年減；2026 年關稅衝擊約 1.05 億美元，10-K 也預期 2026 年通膨持續；營益率落後最強同業約 3 個百分點。","assumption":"營收成長能等比例轉成每股經濟價值。","consequence":"營收照財測成長，但 ROIC 停在 13% 附近、達不到 2028 年 15% 的目標，槓桿升到 2.5 倍以上；EPS 成長慢於營收，倍數往一般工業股靠攏。","ruling":"部分採納。Systems Protection ROS 年增 260bp、整體調整後 ROS 年增 190bp，證明量能有轉成利潤，目前沒有股東經濟變差的證據。但併購報酬要三年才驗得到，所以把 ROIC 15% 與 Maverick 利潤率寫進第三個假設的門檻，2027 年底槓桿高於 2.5 倍就減碼。","watch":"Maverick ROS、淨槓桿、Electrical Connections ROS、全年關稅衝擊。","evidence_refs":["competitive_share_entrants#0","reg_tariff_export#1","geo_supply_chain#1","major_events#0"]},{"view":"價格已反映太多","evidence":"前瞻本益比 24.2 倍，歷史本益比位於四個年度端點的 75 分位；共識 2028 年 EPS 8.05 隱含 2025→2028 年複合約 34%，遠高於投資人日三年目標 17–20%，也高於內生成長上界約 14%。","assumption":"市場用週期高點的成長率外推。","consequence":"即使 EPS 達到共識，倍數只要回到 18 倍，到 2028 年底的報酬只剩約 16%，年化約 7%。","ruling":"部分反駁。股價已從 2026-05 的 164.66 美元跌 24%，2027 年本益比 18.5 倍已計入一部分減速；基準情境本身就假設倍數從 24 倍降到 20 倍，報酬來自盈餘成長而不是重新評價。但共識三年成長確實超過內生上界，所以熊市機率不低於 30%。","watch":"2027 年本益比、共識修正方向（本季財報後應會上修）。","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 164.66 → 本次 125.19（-24.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=164.66","side_b":"本次 price_at_dd=125.19","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 164.66 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 164.66 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 164.66 美元：Bull 價 322.5、Bear 價 93，五年期望值 +21.9%，基準年化 4.5%，不對稱比 1.84","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.84。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 164.66 美元：五年期望值 +21.9%，基準年化 4.5%，不對稱比 1.84","side_b":"本次情境、股價 125.19 美元：五年期望值 +60.4%，基準年化 10.4%，不對稱比 5.11","ruling":"再換股價、情境不動：起點價下跌 24.0%，五年期望值多 38.4 個百分點，基準年化多 5.9 個百分點，不對稱比由 1.84 升到 5.11。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：營收規模","cause":null,"prior_field":null,"side_a":"前份兩年驗證點：2026 年營收不低於當時財測 49–50 億美元","side_b":"2026-10-30 財測報告營收成長 48–49%，以 2025 年 38.93 億美元計約 57.6–58.0 億美元，已提前超過","ruling":"前份第一個假設的兩年門檻已經達成，不構成矛盾；本次把門檻往後移到 2027 年有機成長。","evidence_level":"公司財測","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"axis":"訂單成長與營收成長的落差","cause":null,"prior_field":null,"side_a":"營收年增 44%、全年財測三度上修、十月訂單管理層稱非常強、在手訂單季增到 26 億美元（2026-10-30 法說）","side_b":"有機訂單只年增低雙位數，連兩季營收成長遠高於訂單（UBS 提問）；Q2 法說被問到年底在手訂單方向時，CEO 答難說、大約在合適水位；第四季有機成長財測降到 26–29%","ruling":"可調和，屬程度差異。去年同季訂單 +65% 的高基期，加上刻意縮短交期，解釋得了一部分落差。若 2027 上半年訂單仍落後、在手訂單轉降，就變成方向問題，改判減速確立。","evidence_level":"公司揭露＋分析師提問","settle_metric":"第四季有機訂單年增率與年底在手訂單","if_then":["若第四季有機訂單年增 ≥10% 且在手訂單 ≥26 億美元，則加第二筆至目標倉位三分之二","若任一季有機訂單年減，則減碼至半倉並停止加碼；連兩季則清倉","反向條件：若股價先漲回 150 美元以上而訂單數據還沒出來，不追"],"evidence_refs":["end_markets#3","supply_demand_durability#2","supply_demand_durability#3"]},{"axis":"自由現金流口徑","cause":null,"prior_field":null,"side_a":"事實表年度財報口徑：2025 年 FCF 3.72 億美元、FCF 率 9.6%；TTM FCF 率 12.0% 為四家同業最低","side_b":"投資人日 CFO：2025 年 FCF 5.61 億美元、年增 31%；Q2 法說維持 2026 年轉換率 90–95%；第三季 FCF 2.68 億美元","ruling":"兩個口徑不混用，看趨勢時採公司持續營業口徑。差異可能來自已出售業務的現金流與相關稅負被計入年度報表，但事實表沒有拆分，這只是推測。在驗證前，同業 FCF 率比較暫不當作護城河扣分證據，以 2026 全年轉換率來驗。","evidence_level":"兩個來源口徑衝突、未拆分","settle_metric":"2026 全年 FCF÷調整後淨利","if_then":["若 2026 全年轉換率低於 80%，則把盈餘品質降一級並停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方：訂單落後營收、第四季成長降速、在週期高點舉債併購、毛利率下滑、同業 2027–28 年集中投產；AI 資本支出一旦消化，盈餘與倍數雙殺，現在賣比等數據確認早一步","side_b":"買方：股價已跌 24%、2027 年本益比 18.5 倍、財測三度上修、十月訂單非常強，工業與商辦住宅也加速到高個位數成長","ruling":"賣方論證指向的是 2027 下半年的風險，目前還沒有數據證實。做法是現價只建首倉、保留兩筆，並把訂單轉負設為減碼與清倉條件，用事先定好的條件處理這個風險，而不是靠預測。","evidence_level":"推論＋公司揭露","settle_metric":"2027 年各季有機訂單年增率","if_then":["若 2027 上半年任一季有機訂單年減，則減碼至半倉","若訂單持平以上而股價跌破 108 美元，則分批反買"],"evidence_refs":["supply_demand_durability#3","competitive_share_entrants#2"]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-24，股價 164.66 美元，前瞻本益比約 33–35 倍）：B、估值合理偏貴、時機未到","side_b":"本次股價 125.19 美元（−24%），前瞻 24.2 倍、2027 年 18.5 倍；估值結論仍是合理，但已落到區間下緣；評級維持 B","ruling":"價格下跌改善了估值位置，基本面也續強；但同期訂單增速放緩，公司又在週期高點舉債併購，兩者相抵，評級不升。裁決與倉位角色由程式依新輸入重算。","evidence_level":"價格與共識數據","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份 🟢","side_b":"本次 🟡","ruling":"新證據包括：毛利率由 2023 年 40.3% 降到 TTM 37.0%、Electrical Connections ROS 第二季與第三季分別年減 140bp 與 180bp、有機訂單成長落後營收。衰退訊號亮 1 盞，因此升一級。","evidence_level":"公司揭露與事實表年度財報","settle_metric":"Electrical Connections ROS；年度毛利率","if_then":["若 Electrical Connections ROS 連兩季低於 27%，則停止加碼"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"前份未產出欄位的補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位皆為空（未以本格式產出）","side_b":"本次：護城河方向持平、五年後跑道中等、公司類型為品質複利成長（次類循環）、週期位置中循環、牛／基／熊機率 25／45／30、最大回撤 −35%～−50%","ruling":"這是方法補齊，不是看法改變；前份執行力 9/10 的看法，本次獨立重估後結論相同。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場與加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"等回測 BB 中軌 $127 區 或 Fwd PE 28x $140 區 + Q2/Q3 26 backlog 維持 +100%+ YoY 後分批進場 3-5% 衛星倉","side_b":"2027-02 第四季法說：2027 有機成長財測 ≥10% 且季有機訂單年增 ≥10% 才加碼第二筆；股價 ≤108 美元且訂單未轉負，再分批加碼","ruling":"價格條件已達（125.19 美元、前瞻 24.2 倍），在手訂單年增 100% 的條件沒達到，而且這個門檻本身設計有誤：2025 年底在手訂單已是前一年的 3 倍，公司又刻意消化在手訂單、縮短交期，不可能再倍增。改用有機訂單年增率與在手訂單不下降作確認。價格先到、證據只到一部分，所以只建首倉。","evidence_level":"方法＋公司揭露","settle_metric":"季有機訂單年增率","if_then":["若 2027-02 兩項條件皆達，則加碼至目標倉位三分之二","若條件未達，則維持首倉不加碼"],"evidence_refs":["end_markets#3"]},{"axis":"停損、減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設（原文為空）","side_b":"任一季有機訂單年減→減碼至半倉，連兩季→清倉；在手訂單連兩季下降且低於 24 億美元；2027 全年調整後 ROS 低於 20%；Electrical Connections ROS 連兩季低於 27%；2027 年底淨槓桿高於 2.5 倍→減碼三分之一，高於 3.0 倍→清倉","ruling":"新證據促成新門檻：有機訂單成長已落後營收、Maverick 併購推高槓桿，需要可量測的減碼與清倉條件。","evidence_level":"公司揭露","settle_metric":"季有機訂單年增率；淨槓桿","if_then":[],"evidence_refs":["supply_demand_durability#3","major_events#1"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（原文為空）","side_b":"2027 年任一季公司揭露有機訂單年減（資料中心建置暫停或延後）","ruling":"Single Thing 選訂單轉負，而不是關稅或 Maverick，因為資料中心是 EPS 路徑上敏感度最大的單一變數；促成這個選擇的新證據是訂單成長已降到低雙位數。","evidence_level":"公司揭露","settle_metric":"季有機訂單年增率","if_then":["若發生，則減碼至半倉並停止加碼；下一季仍年減則清倉"],"evidence_refs":["end_markets#3"]},{"axis":"前份假設與風險門檻的退休與改寫","cause":"方法變動","prior_field":["thesis.H","thesis.R"],"side_a":"前份風險一：連 2 季 backlog YoY < +50% + 2 家 hyperscaler 下修 capex → R1 觸發；風險二：FY27 OPM 仍卡在 17-18% 未進到 19-20% → H2 削弱；風險三：2028 全球液冷 NVT share < 8%；假設三：Fwd PE 33-35x 維持在 28-30x 區間","side_b":"風險一改為季有機訂單年減，或在手訂單連兩季下降且低於 24 億美元；風險二併入第二個假設，改用 2027 年調整後 ROS ≥21%；液冷份額 <8% 保留為競爭風險的監測項（事實表無份額數據，資料缺口）；估值不再當生意假設，第三個假設改為併購報酬（2028 年 ROIC ≥15%）","ruling":"前份風險一的在手訂單條件很可能已成立（基期是前一年的 3 倍），但兩家超大規模客戶下修資本支出的條件事實表未涵蓋，不能判定觸發；而且在手訂單年增率受基期與交期縮短扭曲，所以改用訂單年增率。前份風險二的營益率門檻以調整後口徑已經達成（第三季 22.1%），改設更高的門檻。前份假設三的倍數區間已被股價下跌打破（現為 24 倍），倍數判斷移到估值題。","evidence_level":"方法＋公司揭露","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027-02 第四季法說的 2027 全年財測：有機營收成長 ≥10%，且第四季有機訂單年增 ≥10%","type":"假設驗證","maps_to":"H1","metric":"2027 有機成長財測；季有機訂單年增率","threshold":"≥10%；≥10%","action":"兩者皆達→加第二筆至目標倉位三分之二；任一未達→維持首倉不加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"任一季公司揭露有機訂單年減","type":"Single Thing","maps_to":"Single Thing","metric":"季有機訂單年增率","threshold":"<0%","action":"減碼至半倉並停止加碼；連兩季則清倉","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"單季價格加生產力未能抵銷通膨（含關稅），或全年關稅衝擊超過 1.5 億美元","type":"風險","maps_to":"R3","metric":"管理層揭露的價格、生產力與通膨金額；全年關稅衝擊","threshold":"未抵銷；>1.5 億美元（2026 年約 1.05 億）","action":"停止加碼；下一季仍未抵銷則減碼三分之一","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"n":4,"text":"Electrical Connections 調整後 ROS 連兩季低於 27%","type":"風險","maps_to":"R5","metric":"Electrical Connections 調整後 ROS","threshold":"連兩季 <27%","action":"停止加碼","source_freq":"每季新聞稿分部表","date":null},{"n":5,"text":"Maverick 2027 營收成長低於 10%，或 2027 年底淨槓桿高於 2.5 倍","type":"風險","maps_to":"R4","metric":"Maverick 營收成長；淨槓桿","threshold":"<10%；>2.5 倍","action":"減碼三分之一","source_freq":"每季法說","date":"2027-12"},{"n":6,"text":"股價跌到 108 美元以下（約 2027 年共識 6.78 的 16 倍），且有機訂單沒有轉負","type":"估值rearm","maps_to":"估值","metric":"股價；季有機訂單年增率","threshold":"≤108 美元且訂單年增 ≥0%","action":"分批反買，加一筆（目標倉位三分之一）","source_freq":"每日股價＋每季訂單","date":null},{"n":7,"text":"股價升到 200 美元以上（約 2027 年共識 6.78 的 29.5 倍），而訂單沒有再加速","type":"減碼","maps_to":"估值","metric":"股價；季有機訂單年增率","threshold":"≥200 美元且訂單年增 <15%","action":"減碼三分之一","source_freq":"每日股價＋每季訂單","date":null},{"n":8,"text":"Maverick 相關商譽減損，或 2027 年底淨槓桿高於 3.0 倍","type":"清倉","maps_to":"H3","metric":"商譽減損；淨槓桿","threshold":"出現減損；>3.0 倍","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":["major_events#0"]},{"n":9,"text":"第四季財報複審：首次揭露的 Maverick 在手訂單、2027 財測、淨槓桿","type":"複審日期","maps_to":null,"metric":"Maverick 在手訂單；2027 財測；淨槓桿","threshold":null,"action":"依觸發一、二、五重新檢視倉位","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"單季有機訂單年增率（公司法說揭露）","bear_threshold":"轉負（<0%）","window":"任一季，2026Q4–2027Q4","source":"公司季報新聞稿與法說會","last_status":"ok"},{"metric":"季末在手訂單","bear_threshold":"連兩季下降且低於 24 億美元","window":"連續兩季","source":"公司法說會","last_status":"ok"},{"metric":"全年調整後營業利益率（含 Maverick）","bear_threshold":"低於 20%","window":"2027 全年","source":"公司新聞稿","last_status":"ok"},{"metric":"Electrical Connections 調整後 ROS","bear_threshold":"連兩季低於 27%","window":"連續兩季","source":"公司新聞稿分部表","last_status":"warning"},{"metric":"淨槓桿（淨負債÷EBITDA）","bear_threshold":"2027 年底高於 2.5 倍","window":"2027 年底","source":"公司法說會","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027-02 法說：2027 有機成長財測 ≥10% 且第四季有機訂單年增 ≥10%，兩者皆達才加第二筆","exec_line":"現價約 125 美元先建目標倉位三分之一；2027-02 兩項條件達標再加三分之一；股價跌破 108 美元且訂單未轉負，再加最後三分之一；任一季訂單年減就停手，並減碼至半倉","holding_cap":"單檔上限 4%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把訂單成長落後營收讀成 AI 資本支出見頂，但落差有一部分來自去年同季訂單 +65% 的高基期，以及公司刻意縮短交期；十月訂單管理層稱非常強，工業與商辦住宅也同步加速到高個位數。2027 年本益比 18.5 倍只反映有限的成長。這個理由要在 2027-02 法說用訂單數據證實，沒有證實就撤回。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把訂單成長落後營收讀成 AI 資本支出見頂，但落差有一部分來自去年同季訂單 +65% 的高基期，以及公司刻意縮短交期；十月訂單管理層稱非常強，工業與商辦住宅也同步加速到高個位數。2027 年本益比 18.5 倍只反映有限的成長。這個理由要在 2027-02 法說用訂單數據證實，沒有證實就撤回。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-22.82, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心（液冷、電力配送、機櫃與線槽）需求延續到 2028 年，nVent 有機成長維持兩位數","2y":"2027 有機營收成長 ≥10%（不含併購），年底在手訂單 ≥26 億美元","5y":"2031 年營收 ≥95 億美元，基礎設施占比 ≥55%","10y":null,"threshold":"2027 有機營收成長 ≥10%；2027 年底在手訂單 ≥26 億美元","source":"公司季報新聞稿與法說會（有機成長、有機訂單、在手訂單）","drift_rule":"TTM 營收比基準路徑（2027 年約 73 億美元）低 5% 以上連兩季→削弱；低 10% 以上連三季→反轉"},{"id":"H2","text":"價格與生產力持續抵銷通膨與關稅，量能放大轉成利潤率擴張","2y":"2027 調整後 ROS（含 Maverick）≥21%，Electrical Connections ROS ≥28%","5y":"2028 年不含併購的調整後 ROS ≥22%（投資人日目標），Maverick ROS 升到 ≥20%","10y":null,"threshold":"2027 調整後 ROS ≥21%；Electrical Connections ROS ≥28%","source":"公司季報新聞稿分部表與法說會（價格、生產力、通膨金額）","drift_rule":"TTM 調整後 ROS 比門檻低 5% 以上（約 1 個百分點）連兩季→削弱；低 10% 以上連三季→反轉"},{"id":"H3","text":"Maverick 與後續併購能在三年內賺回資本成本，公司 ROIC 由 2025 年約 13% 升到 2028 年 15% 以上","2y":"Maverick 2027 營收成長 ≥15%、ROS 升到 ≥18%；2027 年底淨槓桿 ≤2.0 倍","5y":"2028 年 ROIC ≥15%，併購商譽沒有減損","10y":null,"threshold":"Maverick 2027 營收成長 ≥15%、ROS ≥18%；2027 年底淨槓桿 ≤2.0 倍；2028 年 ROIC ≥15%","source":"法說會與年報（分部、Maverick 揭露、槓桿、ROIC）；ROIC 目標來自 2026-03-18 投資人日 CFO","drift_rule":"Maverick 季度營收成長或 ROS 比門檻低 5% 以上連兩季→削弱；低 10% 以上連三季，或出現商譽減損→反轉"}],"R":[{"id":"R1","text":"AI 資料中心建置在 2027–28 年進入消化期，訂單從放緩變成衰退","h_ref":"H1","clock":"🔥","threshold":"任一季有機訂單年減，或季末在手訂單連兩季下降且低於 24 億美元；前份的兩家超大規模客戶下修資本支出保留為輔助監測（事實表未涵蓋，資料缺口）","evidence_refs":["supply_demand_durability#3","end_markets#3"]},{"id":"R2","text":"液冷與資料中心電力競爭加劇：Vertiv 等全套供應商打包銷售，亞洲低價廠與新進者壓價","h_ref":"H1","clock":"🐢","threshold":"Systems Protection 調整後 ROS 連兩季年減 ≥100bp；前份的 2028 年液冷份額 <8% 保留為監測（事實表無份額數據，資料缺口）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"id":"R3","text":"鋼鋁銅關稅，加上依賴墨西哥與中國生產，造成的成本通膨超過定價能力；兩用產品出口管制也限制部分市場","h_ref":"H2","clock":"⚡","threshold":"單季價格加生產力未抵銷通膨（含關稅），或全年關稅衝擊超過 1.5 億美元（2026 年約 1.05 億）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"Maverick 整合不如預期：在週期高點以現金 17.5 億美元加最多 5.5 億績效對價收購，利潤率停在中十位數、槓桿居高不下","h_ref":"H3","clock":"🔥","threshold":"Maverick 2027 營收成長低於 10%，或 2027 年底淨槓桿高於 2.5 倍","evidence_refs":["major_events#0","ma_merger#0","major_events#1"]},{"id":"R5","text":"Electrical Connections 這個傳統高利潤率段的定價力鬆動","h_ref":"H2","clock":"🔥","threshold":"Electrical Connections 調整後 ROS 連兩季低於 27%（第二季 27.3%、第三季 28.2%，皆年減）","evidence_refs":[]}],"single_thing":{"description":"2027 年任一季公司揭露有機訂單年減（資料中心建置暫停或延後）","why_fatal":"資料中心是營收占比最高的終端，基礎設施已近六成；在手訂單只有約 5 個月營收，訂單轉負兩到三季內就會傳到營收。遞減利潤率約 35%，EPS 與倍數同時下修，股價對應熊市情境的 −25%～−50%。這是 EPS 路徑上敏感度最大的單一變數，大於關稅（約 1 億美元）或 Maverick 利潤率。","if_happens":"減碼至半倉並停止加碼；下一季仍年減就清倉，等訂單連兩季回正再重跑完整研究","how_monitor":"每季財報新聞稿與法說：有機訂單年增率、季末在手訂單、管理層對下一季訂單的口頭描述（例如 2026-10-30 稱十月訂單非常強）","probability":"約 25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.46,"peg_fy2":0.74,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":3.36,"FY2026E":5.17,"FY2027E":6.78,"FY2028E":8.05},"fy_end_month":12,"eps_basis":"調整後（non-GAAP）稀釋 EPS。FY2025A 的 3.36 由 2026-10-30 法說 CFO 稱財測中點年增 60% 回推（5.375÷1.6），事實表未直接收錄；GAAP 稀釋 EPS 4.31 含已停業部門的處分利益，不可比。共識為 Koyfin 快照，分析師家數未揭露。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Supercomputing 展示 Maverick 800V DC 電力機架與新模組化液冷平台","impact":"中","watch":"客戶採用情況與訂單描述"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年財測，首次揭露 Maverick 在手訂單","impact":"高","watch":"2027 有機成長財測是否 ≥10%、第四季有機訂單年增率、淨槓桿"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Blaine 2 液冷廠與亞利桑那工程建築廠投產","impact":"中","watch":"產能爬坡進度與 2027 下半年營收成長"}]}
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
