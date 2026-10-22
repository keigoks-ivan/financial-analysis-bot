你是 DD 管線 v20 的判斷層閘（gate），標的 GE（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝14118 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：調整後營收 $13,285M vs 財報前共識約 $12.84B（來源：itiger 財報預覽，聚合站，僅供參考）
- `f_kpi1_adjusted_revenue_non_gaa`（q1_business）｜Adjusted revenue (non-GAAP)＝13285 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：同上，共識約 $12.84B
- `f_kpi2_operating_profit_non_gaa`（q1_business）｜Operating profit (non-GAAP)＝2988 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：新聞稿無；查無共識
- `f_kpi3_operating_margin_non_gaa`（q1_business）｜Operating margin (non-GAAP)＝22.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：查無
- `f_kpi7_orders`（q1_business）｜Orders＝19.0 USD bn｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：查無
- `f_kpi8_commercial_services_back`（q1_business）｜Commercial services backlog＝170 USD bn（「over」）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（CEO 引述）（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：n/a
- `f_kpi9_segment_operating_profit`（q1_business）｜Segment operating profit CES / DPT＝CES $2,887M（margin 27.9%，-10bps）；DPT $475M（margin 13.7%，+20bps） mixed｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：查無
- `f_kpi10_fy2026_guidance`（q1_business）｜FY2026 guidance（本次上修）＝調整後營收成長約 19–20%；營業利益 $10.9–11.0B；調整後 EPS $8.00–8.10；FCF $9.1–9.4B mixed｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：FY1 EPS 共識 7.96（財報後 10-21 快照，consensus_revision；落在指引下緣之下，尚未完全反映）
- `f_peer_ge_gross_margin_pct`（q2_moat）｜GE 毛利率＝31.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ge_operating_margin_pct`（q2_moat）｜GE 營業利益率＝18.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_rtx_operating_margin_pct`（q2_moat）｜RTX 營業利益率＝11.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RTX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ba_operating_margin_pct`（q2_moat）｜BA 營業利益率＝-7.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tdg_operating_margin_pct`（q2_moat）｜TDG 營業利益率＝46.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TDG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gd_operating_margin_pct`（q2_moat）｜GD 營業利益率＝10.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ge_fcf_margin_pct`（q2_moat）｜GE FCF 利潤率＝16.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.96 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.11 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝10.41 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝50645.4 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝56338.72 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝2042 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿 Q3 2026 earnings release https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：查無
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝10285.0 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 20230.0、現金 9945.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1037.56 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.598 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝295.88 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝37.17 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 7.96，分子＝快照價 295.88｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝2.1 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝74.1 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝5.29 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 7.56 → 7.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_ma_w52`（q5_valuation）｜52 週均線＝318.55 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w104`（q5_valuation）｜104 週均線＝270.94 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w250`（q5_valuation）｜250 週均線＝165.57 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_rsi14`（q5_valuation）｜RSI(14)＝31.81｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝7.39 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年 4 月 GE Aerospace 與美國國務院和解 116 項 AECA/ITAR 疑似違規（涉及對中國未授權技術資料出口），民事罰款 3,600 萬美元，其中 1,800 萬暫緩
  - 來源：Lexology: GE Aerospace to pay $36m for alleged US export breaches（as_of 2026-04-20）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：GE Aerospace 2026-09 同意收購鑄件供應商 Consolidated Precision Products（LEAP、GEnx 關鍵供應商），鑄件產能被視為關鍵瓶頸；仍續與 ATI、Howmet 合作
  - 來源：Leeham News: GE Aerospace Moves to Secure Critical Engine Casting Capacity（as_of 2026-09-09）｜affects：thesis.R、decision_inputs.bear
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Q1 2026：GE維持展望，警示燃油成本上升將使飛行量成長放緩
  - 來源：CP24: GE Aerospace keeps outlook, flags slower flight growth as fuel costs rise（as_of 2026-04-21）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St 敘事（非公司指引）指出電動與氫能推進為 GE 噴射引擎業務的長期競爭風險；氣候政策亦可能削弱引擎與售後需求。
  - 來源：Simply Wall St narrative: Global decarbonization and geopolitical strife will undermine aerospace margins（as_of 2025-06-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 披露兩件股東衍生訴訟（Lindsey、Priest/Tola）仍在紐約州法院待決；Sjunde AP-Fonden 案已於 2025 年 4 月和解。
  - 來源：SEC EDGAR 10-K FY2025 法律事項附註（as_of 2026-01-29）｜affects：decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：FAA 於 2026 年 7 月發布 GEnx-1B/-2B AD 2026-14-03（燃油熱交換器連接軟管缺陷致漏油），2026-08-21 生效，要求更換受影響軟管。
  - 來源：EASA AD 資料庫 AD US-2026-14-03（as_of 2026-08-21）｜affects：thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：兩件股東衍生訴訟（Lindsey、Priest/Tola）在紐約州法院待決；相關 Sjunde AP-Fonden 案 2025 年 4 月和解。搜尋未見 2026 新提起的證券集體訴訟。
  - 來源：SEC EDGAR 10-K FY2025 法律事項附註（as_of 2026-01-29）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：FAA AD 2026-14-03 針對 GEnx-1B/-2B 燃油熱交換器連接軟管缺陷，要求辨識並更換，2026-08-21 生效。
  - 來源：EASA AD 資料庫 AD US-2026-14-03（as_of 2026-08-21）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":557.6,"bear_5y_price":162.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":31.1,"ev5y_pct":22.5,"irr_base_pct":5.6,"asym_ratio":1.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":7.96,"pe":37.17,"basis":"FY1（FY2026E）調整後 EPS 共識 7.96，終端倍數同為當年度調整後 EPS 口徑"},"eps":{"bull":[9.4,11.0,12.7,14.5,16.4],"base":[9.15,10.4,11.55,12.7,13.85],"bear":[8.6,8.2,8.0,8.5,9.0]},"pe":{"bull":34,"base":28,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.598,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GE_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜CFO｜guidance：全年營收財測上調至高個位數後段（high teens），原為低雙位數（原話："revenue to grow high teens, up from prior outlook of low"）
- 2026-07-16｜CFO｜guidance：CES 成長財測上調至約 20%，原為中十位數（原話："We expect CES growth of around 20%, up from prior outlook"）
- 2026-07-16｜CFO｜guidance：CES 營業利潤財測區間上調（原話："CES operating profit is now expected to be in the range of"）
- 2026-07-16｜CFO｜guidance：全年 EPS 財測上調，中點加 0.35 美元（原話："we are raising our EPS guidance to a range of $7.65 to $7.85"）
- 2026-07-16｜CFO｜guidance：自由現金流財測上調（原話："We are also raising our free cash flow guidance to $8.9"）
- 2026-07-16｜CFO｜guidance：稅率預期低於 16.5%（原話："below 16.5% for the year"）
- 2026-07-16｜CEO｜guidance：下半年出勤（departures）預期溫和回升（原話："a gradual return to modest departures growth"）
- 2026-07-16｜CFO｜margin：第二季公司毛利率（營業利潤率）年減 130bp 至 21.7%，管理層歸因（原話："decreased 130 basis points to 21.7% from installed engine"）
- 2026-07-16｜CFO｜margin：CES 利潤率年減 160bp 至 27.3%，歸因含 GE9X（原話："160 basis points to 27.3% from installed engine growth"）
- 2026-07-16｜CFO｜margin：管理層定義 spare parts delinquency 的口徑（原話："which represents shipments that have been delayed due to"）
- 2026-07-16｜CFO｜margin：spare parts delinquency 第二季較上季成長 20%（原話："grew 20% sequentially in the second quarter"）
- 2026-07-16｜CFO｜margin：管理層稱利潤率壓力為時間性而非結構性（原話："There's nothing structural that is causing us to have this"）
- 2026-07-16｜CFO｜margin：GE9X 虧損預期 2028 年見頂（原話："we expect those losses to peak by the time we get into 2028."）
- 2026-07-16｜CFO｜commitment：LEAP 服務利潤率 2028 年與整體服務組合持平（原話："LEAP services margins to be in line with our total services"）
- 2026-07-16｜CFO｜commitment：2028 年起 CES 與公司整體利潤率擴張（原話："would expect margin expansion in '28 and beyond."）
- 2026-07-16｜CFO｜commitment：2026 年 spare parts 目錄價格策略與去年一致（原話："our pricing approach for on spare parts catalog for this"）
- 2026-07-16｜CFO｜margin：較高單價的 shop visit 約 2028–29 年起反映於營收，LEAP 2030 年利潤率回到 CFM56 水準（原話："higher-priced shop visits will start showing up"）
- 2026-07-16｜CEO｜commitment：LEAP-1B 耐久套件全面切換時程（原話："full MRO and new-make cutover expected early next year"）
- 2026-07-16｜CEO｜commitment：2027 年 Commercial Services 維持雙位數成長的中期框架（原話："no reason '27 should diverge from that double-digit"）
- 2026-07-16｜CFO｜commitment：自由現金流隨獲利成長，但轉換率會正常化（原話："So we do expect cash flow to grow here with earnings, but"）
- 2026-07-16｜CFO｜guidance：第三季 95% 以上 spare parts 營收已在 backlog（原話："more than 95% of spare parts revenue in"）
- 2026-07-16｜CFO｜guidance：已下機與計畫拆下引擎超出全年 shop visit 指引 40% 以上（原話："exceed our full year shop visit guide by over 40%."）
- 2026-07-16｜CEO｜customer：上半年出勤大致持平，未見客戶行為改變（原話："First half departures were roughly flat, but we have not"）
- 2026-07-16｜CEO｜risk：管理層稱需求可能變動（原話："demand could evolve from here"）
- 2026-07-16｜CEO｜risk：管理層稱瓶頸在供給端而非需求（原話："it's much more a supply side challenge than it is demand"）
- 2026-07-16｜CFO｜customer：年中 spare parts 訂單約 40% 的高點已出現正常化（原話："Those are exceptional results and kind of honestly"）
- 2026-07-16｜CFO｜product：LEAP 外部通路占比預期 2030 年升至約 30%（原話："we expect that to grow to, say, 30% by the time we get to"）
- 2026-07-16｜CFO｜product：LEAP shop visit 2030 年前年複合成長約 25%（原話："a 25%-ish CAGR from now till 2030"）
- 2026-07-16｜CEO｜product：LEAP-1A 已有逾四成機隊裝耐久套件（原話："we now have over 40% of the fleet equipped with the"）
- 2026-07-16｜CEO｜product：耐久套件不會帶來工作量提前加速（原話："It really won't be something that will trigger an"）
- 2026-07-16｜CEO｜customer：管理層承認客戶對持有成本與翼上時間的疑慮（原話："So not in any way declaring victory here."）
- 2026-07-16｜CFO｜capital_allocation：股數年減 2400 萬股（約 2%），來自先前宣布的資本配置行動（原話："Share count was down 24 million from 2% --"）
- 2026-07-16｜CEO｜competition：第二季後敘事：管理層稱四月不上調財測的決定會重來一次（原話："play April all over again in the same way that we did."）
- 2026-07-16｜CFO｜customer：spare engine 比率因安裝引擎出貨成長而下降，LEAP 終身約 10–12% 成熟水準（原話："very close to 10% to 12%"）
- 2026-07-16｜CFO｜risk：CFM56 工作範圍預期穩定至 2028–29（原話："work scopes should remain stable from now till '28, '29"）
- 2026-07-16｜CEO｜risk：Ryanair 1879 航班調查，CFM 協助（原話："assisting with the investigation into Flight 1879."）
- 2026-07-16｜CEO｜product：XA102 適應循環引擎完成組裝準備審查（原話："We completed an assembly readiness review for the XA102"）

### 問答異常語氣（迴避／改口／保留）
- GE_Q2_2026_Earnings_Call_20260716.md｜問：Seifman：今年強勁是否為提前拉貨（pull forward）？｜答法：Culp 未正面回答是否提前拉貨，改談供應鏈進展與 2027 年框架
- GE_Q2_2026_Earnings_Call_20260716.md｜問：Liwag：是否對 CES 利潤率 >30% 有明確能見度｜答法：Ghai 未給 30% 數字，僅說 2028 年後利潤率擴張並列三項壓力

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 3 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260717","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"裝機基數年金按引擎老化的物理節奏自動兌現——收入來自法規強制的維修義務，不來自客戶的採購意願"},{"id":"H2","text":"2028 年 margin 拐點兌現——GE9X 虧損見頂、LEAP 服務利潤率對齊組合、post-launch 定價入帳，三者同時發生使 CES margin 由收縮轉擴張"},{"id":"H3","text":"終端倍數收斂而非維持——2031 年市場給一家成長減速至約 10% 的成熟航發franchise 約 30x，而非現在的 44.6x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"FR1879 調查導向 CFM56-7B 強制檢查 AD，低毛利合規工作排擠高毛利大修產能。機制：2026-07-10 Ryanair FR1879（737-800，CFM56-7B）非包容性風扇葉片失效，碎片擊碎客艙窗、旅客部分被吸出；北馬其頓 AAIIC 主導，NTSB／FAA／EASA／Boeing／CFM 參與。先例極具體：2018 年西南航空 1380（同型引擎、致命）後 FAA 發出的 AD 要求全機隊風扇葉片榫槽超音波／渦流檢查＋重新設計進氣道，合規期限一路展延至 2028-07-31——這類強制檢查案的執行週期是數年且長期佔用 MRO 產能。而 GE 的 MRO 系統目前超訂 40%、備品延交環比 +20%，沒有任何餘裕吸收插隊工作。直接撞 H2（2028 margin 拐點）。"},{"id":"R2","text":"GE 自建的外部 MRO 通路稀釋自身捕捉的經濟價值——LEAP 第三方 shop visit 占比 2024 年約 10% → 2025 年約 15%（近乎翻倍）→ 2030 年目標約 30%；MTU 沃斯堡新廠 2026-07-08 導入首具 LEAP-1B。這是產能瓶頸下的必要選擇（否則無法消化 25% 年複合的量），但代表越來越大比例的 shop visit 毛利流向第三方。「LEAP shop visit 總量 +25% 年複合」與「GE 自身捕捉的毛利成長」不是同一件事——若把前者當後者用，2028 年後的 margin 擴張斜率會被系統性高估。"},{"id":"R3","text":"航空需求結構性放緩 → 航空公司信用惡化 → shop visit 遞延。已出現的第一個數據點：1H26 departures 大致持平（管理層預期下半年才「回到溫和成長」）；高油價擠壓航空公司（分析師 Scott Mikus 直接就此提問）；CEO 自承航空公司重整「很難想像會在明年下半年或 '28 之前大量出現」——亦即他認為會出現，只是不在 12 個月內。裝機基數決定「是否要修」，departures 決定「何時要修」——而後者驅動 1-2 年的 EPS 節奏，正是 IRR 最敏感的變數。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","irr_base_pct":5.4,"ev5y_pct":19.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.3,"ev5y_pct":19.0,"irr_base_pct":5.4,"max_dd_pct":-50.0,"bull_5y_price":540.75,"bear_5y_price":196.4,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","price_at_dd":345.73,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GE","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"GE Aerospace"},"oneliner":"航空引擎售後年金寡頭，第三季訂單 +49% 並再度上修全年財測；現價對 FY2027 共識約 32.5 倍、Base 年報酬約 7.7%，等 $265 以下或 2027 財測驗證服務成長再進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/scenario.json","answers":{"q1_business":{"verdict":"賺航空公司在 25 年以上機隊壽命內的強制維修錢；錢卡在適航認證零件與大修工時這一節點，新引擎是用虧損換裝機基數","reasoning":"第三季 GAAP 營收 141.18 億美元、調整後營收 132.85 億（年增 18%），調整後營業利益 29.88 億、營益率 22.5%（年增 220bp）；TTM 毛利率 31.0%。分部：CES 營收年增 21%、營業利益 28.87 億、利益率 27.9%（年減 10bp）；DPT 營收年增 7%、營業利益 4.75 億、利益率 13.7%。CES 占兩大分部營業利益約八成六，其中商用服務是主體，2026 年服務營收增量約 55 億（第三季法說 CFO）。商用服務在手訂單逾 1,700 億，進入第四季時 95% 以上備件營收已在訂單裡。產業時鐘判 II 擴張：訂單年增 49%、交付年增逾 20%、供給仍追不上需求，依據是訂單與交機數據，不是股價。供需持久性判結構性持久：IATA 研究稱交機放緩屬結構性限制、再平衡不早於 2030 年代初；Boeing 2026 年 7 月展望稱 2026 年初約 2,000 架供給缺口。單點依賴：客戶端集中在少數機身廠與大型航空公司（10-K 風險段，單一客戶占比事實表未涵蓋）；供給端鑄件是瓶頸，CPP 收購就是在處理這一點。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_adjusted_revenue_non_gaa","f_kpi2_operating_profit_non_gaa","f_kpi3_operating_margin_non_gaa","f_kpi7_orders","f_kpi8_commercial_services_back","f_kpi9_segment_operating_profit","f_kpi10_fy2026_guidance","f_peer_ge_gross_margin_pct"],"verdict_values":{"revenue_quality":"高：營收以售後服務為主，長約（LTSA）占服務在手訂單大宗，備件營收 95% 以上已在訂單；新機交付為次要且低利","unit_econ_note":"新引擎出貨虧損或微利（GE9X 2027 年再增約 3 億美元虧損），靠 25 年以上售後零件與大修回收；LEAP 每次大修金額約為 CFM56 的一半，隨機隊老化與第二次大修上升","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"裝機基數年金＋單一引擎認證寡占＋售後零件定價"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：IATA 供應鏈研究稱再平衡不早於 2030 年代初；Boeing 2026-07 展望約 2,000 架供給缺口、單走道缺口到本十年末","bargaining":{"up":"弱：鑄鍛件前置期 6–18 個月以上，優先供應商物料投入連 10 季成長才勉強跟上；CPP 收購為收回瓶頸","down":"對機身廠強（737MAX 只用 LEAP-1B、777X 只用 GE9X）；對航空公司備件強、大修工時中等（外部維修通路占比上升）","geo":"中國 COMAC 出口許可 2025-07 恢復；與歐盟、英國、日本、韓國有航太零關稅協議；Section 232 談判期至 2027-01"},"profit_pool_dir":"向引擎商與售後零件集中：機身廠 BA TTM 營益率 −7.4%，GE 18.7%，售後零件專利件業者 TDG 46.5%","tam_table":{"expanded":false,"reason":"成長來自既有裝機基數的維修年金，不是滲透率或新品類故事；TAM／SAM 與利潤池占比數字事實表未涵蓋"}}}},"q2_moat":{"verdict":"護城河方向 →：裝機基數與單一引擎地位穩定，執行力改善，但外部維修通路與備件延交讓部分工時外流","reasoning":"機制是裝機基數乘上數十年服務年金：在翼 80,000 具引擎、23 億飛行小時以上資料，零件屬適航認證件，換供應要重新認證。可證方向用營益率差代理（同業 ROIC 事實表未涵蓋）：GE TTM 營益率 18.7%，RTX 11.2%、GD 10.3%、BA −7.4%；GE 自身營益率由 2022 年 12.3% 升到 2025 年 18.9%，差距擴大。執行力評 9：AOG 降到接近零、內部大修週轉比 2025 年底縮短一週以上、LEAP 風扇組件產出翻倍；定價力評 9：零件目錄價策略延續（2026-07-16 CFO），IndiGo 逾 1,000 具 LEAP-1A、土耳其航空逾 300 具 LEAP-1B 加全機隊長約。當期 ROIC 因無投入資本口徑無法算，只能給利益率端；四個持續期檢查點兩綠兩黃。","fact_refs":["f_peer_ge_operating_margin_pct","f_peer_rtx_operating_margin_pct","f_peer_ba_operating_margin_pct","f_peer_tdg_operating_margin_pct","f_peer_gd_operating_margin_pct","f_peer_ge_fcf_margin_pct","f_kpi9_segment_operating_profit"],"verdict_values":{"moat":{"mechanism":"裝機基數×數十年強制維修年金；737MAX 與 777X 單一引擎、A320neo 雙源之一；售後零件為適航認證件，替換需重新認證","execution":9,"pricing":9,"grade":"A","trend":"→","trend_evidence":"執行力擴大（AOG 近零、物料投入連 10 季成長、大修週轉縮短）；定價力穩定（95% 以上備件營收在訂單、零件目錄價策略延續）；但備件延交連兩季季增、LEAP 外部通路占比 2030 年升至約 30%，抵銷部分執行力優勢，整體判穩定","competitor_notes":[{"name":"RTX","strategy_note":"A320neo 上 GTF 與 LEAP-1A 雙源競爭；TTM 營益率 11.2% 低於 GE，IndiGo 逾 1,000 具 LEAP-1A 訂單顯示 LEAP 在雙源機型仍拿份額"},{"name":"BA","strategy_note":"是客戶不是對手；TTM 營益率 −7.4%、FCF 利潤率 −1.2%，機身廠財務弱是 GE 新機交付與 GE9X 認證時程的外部風險"},{"name":"TDG","strategy_note":"售後專利零件標竿，營益率 46.5%，顯示航太售後零件定價上限遠高於 GE 目前水準，也是非原廠零件競爭的代表"},{"name":"GD","strategy_note":"國防與公務機為主，不直接競爭商用引擎；營益率 10.3% 作為國防側利潤率參照"}],"threats":[{"level":"🟡","text":"雙源機型與國防新案的點對點競爭：A320neo 上的 GTF；美國空軍 ACP 無人機引擎授予四隊並明言要多供應商，新進入者 Beehive 入列","p":"20%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"外部維修通路占 LEAP 服務比重由十幾 % 升到 2030 年約 30%，大修工時外流；但外部通路仍向 GE 買零件（第三季備件成長部分來自外部通路），屬點對點","p":"30%","evidence_refs":["channel_business_model_shift#0"]},{"level":"🟡","text":"鑄件產能為全產業瓶頸，GE 以 117.5 億美元收購 CPP 並續用 ATI、Howmet；交割前產能改善靠合約","p":"25%","evidence_refs":["geo_supply_chain#0","supply_demand_durability#4"]},{"level":"🟡","text":"電動與氫能推進的長期替代；GE 自身參與（BETA 混合電動高空飛行、RISE 開放式風扇），窄體主力在 2030 年代中之前難以替代","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是乘客、決策與付款者是航空公司與租賃商；維修是適航法規強制的「需要」，只能延後不能取消。Boeing 估 2026 年初供給缺口約 2,000 架，IATA 稱再平衡不早於 2030 年代初；第三季 CFM56 退役率僅 1.5–2%，停機坪待修引擎年初至今增加 20%"},{"item":"決策層級","level":"🟢","text":"替代性在機型層決定：737MAX 只有 LEAP-1B、777X 只有 GE9X（逾 1,300 具訂單），選定後鎖 25 年以上；換零件來源需重新認證。弱點在下一代窄體招標時會重開"},{"item":"價值鏈分配","level":"🟡","text":"機身廠拿得少（BA 營益率 −7.4%），引擎商拿得多；但鑄鍛件供應商握有產能瓶頸，外部維修通路占比上升分走工時，非原廠零件業者（TDG 營益率 46.5%）在零件端競爭"},{"item":"社會容忍度","level":"🟡","text":"零件提價由航空公司吸收，布蘭特油價約 $111 時航空公司獲利受壓，提價空間受客戶健康度約束；監管面有 FAA 適航指令、ITAR 和解 3,600 萬美元、Section 232 談判期至 2027-01，屬政策風險但未見替代方案"}],"roiic":"事實表未涵蓋投入資本；有機增量投入多走損益表（年研發逾 30 億、GE9X 虧損），資產負債表增量小","reinvest_rate":"有機約 0–10%（2026 年 FCF 轉換率逾 100%）；計入 CPP 117.5 億則 2027 年單年遠超 100%","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；事實表無投入資本口徑，周轉率、ROIC、增量 ROIC 與內生天花板均無法計算，只給利益率端：TTM 營益率 18.7%、FCF 利潤率 16.6%"}}}},"q3_growth":{"verdict":"五年後跑道寬 🟢：LEAP 裝機 2025→2030 翻倍、三分之二 CFM56 機隊未做第二次大修，下一條曲線是 LEAP 第二次大修與寬體工作範圍擴大","reasoning":"成長組成以量與價為主：LEAP 大修到 2030 年年複合約 25%、裝機基數年增低到中個位數、零件目錄價、工作範圍擴大；淨回購約 2%／年；CPP 為產能投資不是成長主力。共識 EPS：FY2026E 7.96、FY2027E 9.11、FY2028E 10.41，兩年年複合 14.4%；共識營收 FY1→FY2 年增 11.2%。內生天花板因無投入資本口徑無法計算；EPS 與營收成長差約 3pp，歸因於 2028 年起利益率擴張（GE9X 虧損回落、LEAP 服務利益率對齊）與淨回購，不歸因於倍數重估。衰退訊號十類未亮燈：毛利率未連兩季年減（第二季年減、第三季回升）、FCF／淨利 2025 年 0.83 且 2026 年逾 1.0、EPS 與營收成長差未超過 5pp。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_commercial_services_back"],"verdict_values":{"growth":{"driver_mix":"量（LEAP 裝機翻倍、大修年複合約 25%）＋價（零件目錄價）＋工作範圍擴大；淨回購約 2%／年；併購非主力","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板事實表無法計算（無投入資本）；共識 FY2026E→FY2028E EPS 年複合 14.4%，缺口歸因利益率擴張與淨回購","segments":[{"item":"CES 第三季","value":"營收年增 21%、營業利益 28.87 億、利益率 27.9%；服務營收年增 17%、設備營收年增 38%"},{"item":"DPT 第三季","value":"營收年增 7%、營業利益 4.75 億、利益率 13.7%；在手訂單逾 300 億"},{"item":"2027 年管理層框架","value":"商用服務低雙位數成長、服務利益率持平、DPT 高個位數成長、GE9X 再增虧約 3 億、整體利益率與 2026 持平"}],"decay_signals":["毛利率連兩季年減：未亮（第二季年減 130bp、第三季年增 220bp）","核心市占縮減：未亮（無 sourced 證據）","主力產品提價後銷量下滑：未亮","EPS 成長高於營收成長逾 5pp：未亮（共識差約 3pp）","FCF／淨利連兩年 <0.75：未亮（2025 年 0.83、2026 年逾 1.0）","SBC 占營收逾 5% 且上升：事實表未涵蓋","TAM 萎縮或被替代：未亮","產業倍數三年系統性下移：事實表未涵蓋","維持性資本支出占 FCF 逾 60%：未亮","停止投資新產能：未亮（CPP、年資本支出逾 10 億）"],"trap_rating":"🟢"}}},"q4_capital":{"verdict":"資本配置中等：股數持續淨減、現金轉換率高，但回購價位偏貴，CPP 收購要等交割後驗證","reasoning":"FCF／淨利：2025 年 FCF 72.64 億 ÷ 淨利 87.04 億＝0.83；2026 年迄今轉換率 105%，全年指引 FCF 91–94 億且轉換率逾 100%（第三季法說 CFO）；2023、2024 年 0.46、0.56 是因淨利含分拆與出售利得。現金去向：股息殖利率 0.6%、回購（股數年減約 2%）、CPP 約 70 億現金加新債（117.5 億−70 億＝約 47.5 億），目前淨負債 102.85 億。SBC 占營收事實表未涵蓋。前一季 CFO 說轉換率會正常化，本季仍維持逾 100%，屬好於預期。","fact_refs":["f_kpi6_free_cash_flow_non_gaap","f_kpi10_fy2026_guidance","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"CPP 117.5 億美元收購預計 2027 下半年交割，尚無已實現增量報酬；過往併購報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購在 FY1 本益比約 35–37 倍執行，盈餘殖利率約 2.7%；只要 10 年期公債殖利率高於 0.7%，就低於公債加 2% 的門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"股數年減約 2,400 萬股（約 2%，2026-07-16 CFO），第三季 EPS 成長部分來自股數減少；淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；CPP 為產能投資，交割（2027 下半年）後再展開報酬檢核"}}}},"q5_valuation":{"verdict":"現價要求 2026–2031 年 EPS 年複合約 12% 且終端仍給 28 倍，才有約 7.7% 年報酬；成長我相信，倍數能否守在 30 倍以上我不信","reasoning":"現價 $295.88，FY1 共識 EPS 7.96（低於公司指引下緣 8.00），FY1 本益比 37.2 倍、FY2027 32.5 倍、FY2028 28.4 倍。PEG 以 FY2026E→FY2028E 共識年複合 14.4% 計約 2.6，屬貴；FY2025 調整後實際 EPS 事實表未涵蓋，故不用三年口徑。五年分位事實表未涵蓋，只有 4 個年度端點：本益比分位 2.1%（早年 GAAP 淨利含分拆利得，失真不採用）、P/S 分位 74.1%。短期上檔：12 個月後以 FY2028E 10.41 乘 29 倍約 $302，約 +2%；中期：Base 五年終端 13.85×28 倍＝$387.8，約 +31%。FY1 共識近三個月上修 5.3%，基本面動能正向，但價格已先反映大部分。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_percentile","f_ps_percentile","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Fwd P/E 與 PEG（品質複利成長）","tier":null,"peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比，無法做倍數錨"},"fwd_pe":37.17,"peg":2.6,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 37.2 倍、FY2027 32.5 倍，PEG 約 2.6 大於 2 屬貴；較前份約 44.6 倍已降一級，但 Base 年報酬約 7.7% 仍低於 8%，故判偏貴而非最貴","upside_short_pct":2.0,"upside_mid_pct":31.1,"denominator_disputed":false,"denominator_note":"分母用調整後 EPS 共識 7.96，與公司指引 8.00–8.10 同口徑，無一次性爭議"}}},"q6_how_wrong":{"verdict":"最可能看錯在油價引發的航空業下行把 2028 年的服務成長打斷，同時倍數由 37 倍壓到 20 倍以下","reasoning":"三視角反證見反證紀錄：論點失敗的路徑是油價與航空公司財務壓力推高退役率、二手可用料回流壓低備件；股東經濟變差的路徑是 CPP 吃掉回購、外部通路分走工時；價格已反映太多的路徑是 PEG 約 2.6 下倍數均值回歸。股價 $295.88 在 52 週均線 318.55 之下、104 週均線 270.94 之上，距 250 週均線 165.57 約 −44%；RSI 31.8、26 週報酬 +7.4%。衰退訊號十類未亮，陷阱風險低。","fact_refs":["f_price_at_dd","f_ma_w52","f_ma_w104","f_ma_w250","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟢","label":"衰退訊號十類未亮，風險在倍數與航空周期而非生意變差"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":7.96,"pe":37.17,"basis":"FY1（FY2026E）調整後 EPS 共識 7.96，終端倍數同為當年度調整後 EPS 口徑"},"eps":{"bull":[9.4,11.0,12.7,14.5,16.4],"base":[9.15,10.4,11.55,12.7,13.85],"bear":[8.6,8.2,8.0,8.5,9.0]},"pe":{"bull":34,"base":28,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.6,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-35,"basis":"下緣：Bear 終端 9.0×18 倍＝$162（−45%），與 250 週均線 165.57（−44%）同一位置，再加航空業衝擊時的超跌一成半至 −60%；上緣：EPS 不變只倍數壓回 FY2027 共識 9.11×21 倍＝$191（−35%）","trigger_time":null},"basis":{"bull":"LEAP 大修維持 25% 以上年複合、2027 起延交下降帶動備件加速、GE9X 虧損 2028 見頂後快速回落、航改發電需求增量；CES 利益率 2028 起逐年擴張","base":"2027–2028 依共識 9.11／10.41，之後服務成長降到約 10%、利益率小幅擴張、回購約 1.5%；終端 28 倍為成熟售後年金寡頭","bear":"油價與航空公司財務壓力使 2028–2029 出勤停滯、CFM56 退役率升到 3% 以上、二手零件回流，加上 CPP 利息與 GE9X 虧損；EPS 五年只到 9.0，倍數壓到 18 倍"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"第三季法說分析師指出布蘭特約 $111、Delta 縮減排班；第一季公司已警示燃油成本使飛行量成長放緩；第三季出勤僅年增 1%","assumption":"2027 年服務成長由在手訂單與已飛週期決定，油價只延後不取消大修","consequence":"若航空公司財務惡化延續到 2028，退役率由 1.5–2% 升到 3–4%，二手可用料回流壓低 CFM56 備件，同時倍數由 37 倍壓到 18 倍，五年後股價可能低於現價一半","ruling":"部分採納：2027 年有 95% 備件在訂單、上半年待修引擎已進廠，短期反駁成立；2028 以後無法排除，Bear 機率由 25% 提到 30%。與唯一致命點（2027 財測下修服務成長）部分重疊，監測指標已回補","watch":"CFM56 年退役率、商用服務訂單年增率、航空公司出勤","evidence_refs":["end_markets#4"],"fact_refs":["f_kpi7_orders","f_kpi8_commercial_services_back"]},{"view":"論點成功但股東經濟變差","evidence":"CPP 117.5 億美元收購（約 70 億現金＋新債），CEO 表明不做自用供應商、續供其他引擎商；LEAP 外部維修通路占比 2030 年升到約 30%；GE9X 2027 年再增虧約 3 億","assumption":"營收與 EPS 成長兌現後，每股價值同步成長","consequence":"現金被併購占用使回購縮小，CPP 若以外部客戶為主，增量報酬可能低於 GE 本業；工時外流使 LEAP 大修量成長不等於 GE 毛利成長","ruling":"採納部分：情境淨回購由約 2% 降到 1.5%；CPP 報酬待交割後驗證","watch":"CPP 交割時程與交割後外部客戶營收、LEAP 外部通路占比","evidence_refs":["geo_supply_chain#0","channel_business_model_shift#0"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 37.2 倍、PEG 約 2.6；第二季上修指引後股價反跌逾 4%，TD Cowen 稱上修幅度可能不夠；Daiwa 目標 $301、中立，警告 2027–2028 共識有風險；賣方平均目標約 $397","assumption":"終端倍數能維持在 30 倍以上","consequence":"即使 EPS 照共識成長，倍數回到 28 倍時 Base 年報酬只有約 7.7%","ruling":"採納：這是觀望的主因，等價格而不是等基本面","watch":"FY2027 共識本益比是否 ≤29 倍（約 $265）","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 345.73 → 本次 295.88（-14.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=345.73","side_b":"本次 price_at_dd=295.88","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 345.73 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 345.73 美元：Bull 價 540.75、Bear 價 196.4，五年期望值 +19.0%，基準年化 5.4%，不對稱比 1.3","side_b":"本次情境、股價仍用 345.73 美元：Bull 價 557.6、Bear 價 162，五年期望值 +4.9%，基準年化 2.3%，不對稱比 0.96","ruling":"先換情境、股價不動：五年期望值少 14.1 個百分點，基準年化少 3.1 個百分點。不對稱比由 1.3 變為 0.96。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 345.73 美元：五年期望值 +4.9%，基準年化 2.3%，不對稱比 0.96","side_b":"本次情境、股價 295.88 美元：五年期望值 +22.5%，基準年化 5.6%，不對稱比 1.63","ruling":"再換股價、情境不動：起點價下跌 14.4%，五年期望值多 17.7 個百分點，基準年化多 3.2 個百分點，不對稱比由 0.96 升到 1.63。合計五年期望值比前份多 3.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：基本面短期全面向上","cause":null,"prior_field":null,"side_a":"第三季訂單 190 億（+49%）、調整後營收 +18%、營益率 22.5%（+220bp）、EPS 2.25（+36%）；全年 EPS 指引上修到 8.00–8.10","side_b":"前一季（2026-07-16 CFO）給的全年上修與 2027 商用服務雙位數成長，本季都兌現並上調為低雙位數；前一季說現金轉換率會正常化，本季仍逾 100%","ruling":"一致，屬好於承諾；不構成看空理由","evidence_level":"公司 8-K 與法說會一手資料","settle_metric":null,"if_then":[],"evidence_refs":["customer_concentration_credit#1","supply_demand_durability#2","capital_markets_pricing#2"]},{"axis":"需求：在手訂單對油價","cause":null,"prior_field":null,"side_a":"服務訂單年增 23%、年初至今 30%，備件訂單更快；上半年待修引擎已進廠、上半年拆換預期年增逾 10%，停機坪待修引擎年初至今 +20%","side_b":"布蘭特約 $111、航空公司縮減排班，第三季出勤僅 +1%；第一季公司警示燃油成本使飛行量成長放緩","ruling":"可調和（時間差）：2027 年由已飛週期與在手訂單決定，選 A 側；2028 以後 B 側的影響尚未進入訂單，Bear 機率 30% 反映此風險","evidence_level":"一手法說與新聞稿；油價為分析師提問引述","settle_metric":"2027-01 財測的商用服務成長率；2027 年第一季服務訂單年增率","if_then":["若 2027-01 財測商用服務成長 <10%：不追、停止加碼，Bear 機率提到 35%，已持有者減碼一半","若 2027 年第一季服務訂單年增仍 ≥15% 且備件延交下降：確認 A 側，股價 ≤$265 時分批反買"],"evidence_refs":["end_markets#4","end_markets#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較前份 $345.73 跌 14%，同期 EPS 指引兩度上修；FY2027 本益比 32.5 倍、RSI 31.8 超賣；2026 年現金流已超過 2028 年目標、利潤接近 2028 年目標；航改發電的 CFM56 零件需求未計入 2028 指引","side_b":"Base 年報酬約 7.7% 仍不到 8%：2027 年 GE9X 再增虧約 3 億、CES 利益率 2027 持平、CPP 動用約 70 億現金；油價壓力未進訂單","ruling":"不可調和，選 B 側：約束條件只有價格。依據是 Base 終端 13.85×28 倍＝$387.8，現價對應年報酬約 7.7%；要到 10% 需股價約 $265","evidence_level":"情境推導，輸入全來自共識與法說","settle_metric":"股價對 FY2027 共識 9.11 的倍數","if_then":["若股價 ≤$265 且第四季財報無服務成長下修：分批反買，首筆三分之一目標倉","若股價回到 $350 以上而 2027 財測未高於共識：不追"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"備件延交持續上升","cause":null,"prior_field":null,"side_a":"優先供應商物料投入連 10 季成長、第三季雙位數年增，LEAP 引擎造成的停飛降到接近零","side_b":"備件延交第二季季增 20%（2026-07-16 CFO），第三季再度季增（2026-10-20 CFO）","ruling":"可調和：需求成長快於供給，短期是訂單能見度；長期若延交不降，客戶轉向外部通路與非原廠零件。CEO 本季表明 2027 年要降延交","evidence_level":"一手法說","settle_metric":"2027 年各季備件延交是否季減","if_then":["若 2027 年連兩季延交仍季增且外部通路占比加速上升：停止加碼並重估護城河方向","若延交連兩季季減且備件營收成長 ≥20%：維持護城河判斷"],"evidence_refs":["end_markets#3","channel_business_model_shift#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸穩定：A320neo 雙源格局未變、ACP 新進入者規模小；結構軸轉好：IATA 與 Boeing 均稱供給不足延續到 2030 年代初","side_b":"其他結構軸變動中：CPP 反壟斷審查（2027 下半年交割）、Section 232 談判期至 2027-01-05 保留課稅選項、外部維修通路占比上升","ruling":"結構性轉好中（供需結構軸），其他結構軸有法規與通路變動，但現行零關稅協議與 IEEPA 退稅使關稅衝擊有限","evidence_level":"IATA、Boeing 展望與 10-Q","settle_metric":"Section 232 報告與 CPP 監管審查結果","if_then":["若 Section 232 對民用引擎零件課稅且公司未能轉嫁：停止加碼","若 CPP 監管要求剝離關鍵廠：不追，重估 2028 產能假設"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]},{"axis":"前份漂移：價格帶動的估值與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 $345.73、FY1 本益比約 44.6 倍、估值最貴一級、觀望","side_b":"本次：股價 $295.88（−14%）、FY1 37.2 倍、FY2027 32.5 倍，估值降一級；EPS 指引中點再上修 $0.30 也貢獻一部分","ruling":"估值改善主要來自價格；裁決與角色由本輪決策輸入重算，觀望理由由「價格過高」改為「價格接近但 Base 年報酬仍不到 8%」","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：結構判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質好但價格貴、陷阱低、護城河持平、五年後跑道寬、品質複利成長、中循環","side_b":"本次全部維持：第三季訂單 +49%、服務訂單 +23%、LEAP 大修到 2030 年年複合約 25% 再確認；新出現的油價壓力與 CPP 收購放進風險項，不改結構判斷","ruling":"新證據支持原判，不改","evidence_level":"一手法說與新聞稿","settle_metric":null,"if_then":[],"evidence_refs":["supply_demand_durability#2","end_markets#0"]},{"axis":"前份漂移：情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 25%、Bear 25%，最大回撤 −50%（單點），Base 終端 30 倍","side_b":"本次：Bull 25%、Base 45%、Bear 30%，Bear 上調因第三季法說的油價約 $111 與航空公司縮減排班；最大回撤改為 −35% 至 −60% 的範圍，以 250 週均線為錨；Base 終端改 28 倍","ruling":"回撤改用範圍與可驗證的均線錨；終端倍數下修 2 倍是因 2027 年利益率持平、成長在 2028 後降到約 10%","evidence_level":"情境推導","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#4"]},{"axis":"前份漂移：進場重啟門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","side_b":"股價 ≤ $265（FY2027 共識 EPS 9.11 的 29 倍，對應 Base 年報酬約 10%）","ruling":"舊門檻已觸發（現價對 FY2027 共識 32.5 倍 ≤35 倍），依規定是重跑判斷而非直接建倉；重跑發現 2027 年 GE9X 再增虧約 3 億、CES 利益率 2027 持平、CPP 動用約 70 億現金，Base 年報酬僅約 7.7%，分批反買門檻收緊到 29 倍（$265）；FY2028 財測尚未給出，第二條件未觸發","evidence_level":"第三季法說 CFO 2027 框架","settle_metric":"股價對 FY2027 共識倍數","if_then":["若股價 ≤$265：分批反買首筆","若 2027-01 財測 EPS 中點 ≥$9.40：門檻上調到約 $280 並重跑"],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"（前份無唯一致命點）","side_b":"2027 年 1 月第四季財報給出的 2027 財測把商用服務成長下修到個位數","ruling":"新設 Single Thing：商用服務成長是 EPS 最大單一敏感項（低雙位數對應約 35–40 億美元營收增量），選它而非較戲劇化的適航事件；發生時不追、停止加碼，已持有者減碼一半","evidence_level":"第三季法說 CFO","settle_metric":"2027-01 財測","if_then":["若發生：減碼一半、Bear 機率提到 35% 並重跑"],"evidence_refs":[]},{"axis":"kill 指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"（前份無 kill 指標）","side_b":"商用服務營收年增連 2 季 <8%；服務訂單連 2 季年減；CFM56 年退役率 ≥3%；CES 利益率連 4 季年減 ≥50bp；2027 EPS 指引中點 <$8.80","ruling":"新設可量化的減碼與清倉條件：前兩條任一觸發即減碼，三條以上同時觸發即清倉","evidence_level":"公司季報與法說","settle_metric":null,"if_then":["若任一 kill 指標觸發：減碼一半","若三條以上同時觸發：清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 FY2027 共識 29 倍以下才開始分批反買","type":"估值rearm","maps_to":"H1","metric":"股價對 FY2027 共識 EPS 9.11 的倍數","threshold":"股價 ≤ $265","action":"分批反買，首筆三分之一目標倉","source_freq":"每日股價","date":null,"evidence_refs":["capital_markets_pricing#1"]},{"n":2,"text":"2027 財測把商用服務成長下修到個位數","type":"Single Thing","maps_to":"H1","metric":"2027 商用服務營收成長指引","threshold":"<10%","action":"不追、停止加碼；已持有者減碼一半並重跑","source_freq":"年度財測","date":"2027-01","evidence_refs":["end_markets#4"]},{"n":3,"text":"油價壓力進入訂單：服務訂單轉負","type":"風險","maps_to":"R1","metric":"商用服務訂單年增率","threshold":"連 2 季年減","action":"減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#4"]},{"n":4,"text":"新適航指令或合規事件佔用維修產能","type":"風險","maps_to":"R3","metric":"FAA 適航指令範圍與 GE9X 認證時程","threshold":"涉及 LEAP 或 CFM56 全機隊且要求提前拆換，或 GE9X 認證晚於 2027-06-30","action":"停止加碼並重跑","source_freq":"FAA／EASA 公告、每季法說","date":null,"evidence_refs":["product_recall_warning#0","major_events#2","reg_tariff_export#2"]},{"n":5,"text":"CPP 收購監管或整合失敗","type":"風險","maps_to":"R2","metric":"CPP 交割時程與交割後外部客戶營收","threshold":"交割延至 2028 或被要求剝離；交割後外部客戶營收年減逾 10%","action":"停止加碼","source_freq":"8-K、10-Q","date":"2027-09","evidence_refs":["geo_supply_chain#0","major_events#0"]},{"n":6,"text":"2028 利益率拐點驗證","type":"假設驗證","maps_to":"H2","metric":"CES 營業利益率","threshold":"2028 全年 ≥28.5%；連 4 季年減 ≥50bp 視為削弱","action":"削弱則停止加碼，反轉則減碼一半","source_freq":"每季分部數字","date":null,"evidence_refs":[]},{"n":7,"text":"下一代窄體推進失守","type":"清倉","maps_to":"R4","metric":"空巴或波音下一代窄體引擎選型","threshold":"宣布非 CFM 為唯一或主力引擎","action":"清倉","source_freq":"機身廠公告","date":null,"evidence_refs":["substitute_technology#0"]},{"n":8,"text":"第四季財報與 2027 財測後重跑","type":"複審日期","maps_to":"H1","metric":"2027 財測","threshold":"財報公布","action":"重跑判斷","source_freq":"年度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"商用服務營收年增率（季）","bear_threshold":"連 2 季 <8%","window":"2027 年各季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"商用服務訂單年增率（季）","bear_threshold":"連 2 季年減","window":"2027 年各季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"CFM56 年退役率","bear_threshold":"≥3%（2026 年約 1.5–2%）","window":"2027 全年","source":"公司法說會","last_status":"ok"},{"metric":"CES 營業利益率（季）","bear_threshold":"連 4 季年減 ≥50bp","window":"2027–2028","source":"公司季報分部數字","last_status":"ok"},{"metric":"2027 年調整後 EPS 指引中點","bear_threshold":"<$8.80","window":"2027-01 財報","source":"公司財測","last_status":"unknown"}],"evidence_dismissed":[{"ref":"major_events#1","reason":"衍生訴訟是股東代公司向董事與高管求償，勝訴利益歸公司，不是公司對外賠償；10-K 原文說與 2025 年 4 月已和解的 Sjunde AP-Fonden 案事實相同，且未揭露請求金額，構不成對未來現金流的負向證據"},{"ref":"lawsuit_class_action#0","reason":"與同一份 10-K 法律附註的兩件衍生訴訟重複收錄；同一來源另載搜尋未見 2026 年新提起的證券集體訴訟"}],"action_conditions":{"rearm_trigger":"股價 ≤ $265（FY2027 共識 EPS 9.11 的 29 倍，對應 Base 年報酬約 10%）","exec_line":"股價 ≤$265 先建三分之一目標倉；2027-01 財測商用服務成長 ≥10% 再加三分之一；基本面無損而跌到 $230 以下加最後三分之一；回撤可能達 −35% 至 −60%，基本面完整時不因波動砍倉","holding_cap":"6%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 $265 以下（FY2027 共識 EPS 9.11 的 29 倍）","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"qc48_result":"pass","qc48_note":"GE 的 Bull 情境有 LEAP 大修與裝機基數的量價骨架，成長跑道也有公司公開來源支持；但 EPS 逐步推導和歷史類比都不完整，Bull 依據大致站得住，只是細節未經驗證。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=7.39, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='GE 的 Bull 情境有 LEAP 大修與裝機基數的量價骨架，成長跑道也有公司公開來源支持；但 EPS 逐步推導和歷史類比都不完整，Bull 依據大致站得住，只是細節未經驗證。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 $265 以下（FY2027 共識 EPS 9.11 的 29 倍）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"2027 年商用服務低雙位數成長由在手訂單與已飛週期兌現，油價只延後不改變大修需求","2y":"2027 商用服務營收年增 ≥10%、備件延交開始下降","5y":null,"10y":null,"threshold":"2027 全年商用服務營收年增 ≥10%；服務訂單年增率不低於服務營收年增率","source":"公司季報新聞稿與法說會（每季）","drift_rule":"商用服務營收年增連 2 季低於 9.5%（偏離 ≥5%）為削弱；連 3 季低於 9%（偏離 ≥10%）為反轉"},{"id":"H2","text":"LEAP 由新機虧損期進入售後收割期：裝機 2025→2030 翻倍、大修年複合約 25%，LEAP 服務利益率 2028 年對齊整體服務，GE9X 虧損 2027 年後回落，CES 利益率 2028 起擴張","2y":null,"5y":"CES 營業利益率 2028 年起逐年擴張","10y":null,"threshold":"CES 營業利益率 2028 全年 ≥28.5%（2026 年第三季 27.9%）；GE9X 2028 年虧損低於 2027","source":"年報、季報分部數字、法說會","drift_rule":"CES 利益率 TTM 連 4 季低於路徑 ≥5% 為削弱；連 6 季 ≥10% 為反轉"},{"id":"H3","text":"機隊供給不足延續到 2030 年代初，加上 737MAX 與 777X 單一引擎地位，裝機年金持續十年以上；外部維修通路擴大是用 GE 零件放大產能，不是分走零件利潤","2y":null,"5y":null,"10y":"2035 年 LEAP 與 GE9X 裝機年金仍是利潤主體","threshold":"裝機基數年增維持低到中個位數；2030 年 LEAP 外部通路占比 ≤30% 且備件營收成長不低於大修量成長","source":"10-K、投資人日、IATA 與 Boeing 年度市場展望","drift_rule":"跨 2 個年度裝機或備件成長低於門檻為削弱；跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"油價（布蘭特約 $111）與航空公司獲利受壓，出勤停滯，航空公司延後大修、拆舊機取零件，CFM56 退役率由 1.5–2% 回升，二手可用料壓低備件","h_ref":"H1","clock":"⚡","threshold":"商用服務訂單連 2 季年減，或 CFM56 年退役率 ≥3%","evidence_refs":["end_markets#4"]},{"id":"R2","text":"CPP 收購（117.5 億美元，約 70 億現金加新債，2027 下半年交割）壓縮回購、增量報酬未證；鑄件仍是全產業瓶頸，交割前產能改善只能靠合約","h_ref":"H2","clock":"🔥","threshold":"交割延至 2028 或被要求剝離；交割後外部客戶營收年減逾 10%","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"適航與合規事件佔用維修產能：GEnx 燃油熱交換器軟管適航指令（2026-08-21 生效）、Ryanair 1879 航班 CFM56 調查（2026-07-16 CEO）、GE9X 中段密封認證延後、ITAR 和解 3,600 萬美元","h_ref":"H2","clock":"🔥","threshold":"出現涉及 LEAP 或 CFM56 全機隊、要求提前拆換的適航指令；或 GE9X 認證晚於 2027-06-30","evidence_refs":["major_events#2","product_recall_warning#0","reg_tariff_export#2"]},{"id":"R4","text":"下一代窄體推進路線改變：RISE 開放式風扇面臨工程挑戰，電動與氫能長期替代；若 2030 年代中新窄體招標失守，裝機年金在 2040 年後斷層","h_ref":"H3","clock":"🐢","threshold":"空巴或波音下一代窄體宣布非 CFM 為唯一或主力引擎","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"2027 年 1 月第四季財報給出的 2027 財測把商用服務成長下修到個位數","why_fatal":"商用服務是利潤成長主體：低雙位數成長對應約 35–40 億美元營收增量且利益率持平，是 FY2027 共識 EPS 9.11 的主要來源；降到個位數代表訂單轉換或航空公司需求出問題，EPS 與倍數會同時下修","if_happens":"不追、停止加碼；已持有者減碼一半；Bear 機率由 30% 提到 35% 並重跑","how_monitor":"每季服務訂單年增率、備件延交、CFM56 退役率、航空公司出勤；2027-01 財報","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":32.48,"peg_fy2":2.28,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":7.96,"FY2027E":9.11,"FY2028E":10.41},"fy_end_month":12,"eps_basis":"調整後（non-GAAP）EPS，Koyfin 共識快照 2026-10-21；FY2025 調整後實際值事實表未涵蓋（年度財報只有 GAAP 稀釋 EPS 8.14，含非經常項，口徑不同不填）"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"GE9X 升級版中段密封 FAA 認證（公司目標 2026 年底）","impact":"中","watch":"若延到 2027 下半年，GE9X 虧損與 777X 交付延後"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年財測","impact":"高","watch":"商用服務成長是否 ≥10%、CES 利益率是否持平、GE9X 增虧約 3 億是否維持"},{"date":"2027-01","date_precision":"month","type":"regulatory","event":"Section 232 航太談判期進度報告（2027-01-05 前）","impact":"中","watch":"是否對民用引擎與零件課稅、零關稅協議是否延續"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"CPP 收購監管審查與 2027 下半年交割","impact":"中","watch":"是否被要求剝離、交割後外部客戶是否流失"}]}
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
