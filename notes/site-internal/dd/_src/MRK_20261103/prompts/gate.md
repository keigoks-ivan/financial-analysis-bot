你是 DD 管線 v20 的判斷層閘（gate），標的 MRK（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（42 條）
- `f_kpi0_gaap_total_worldwide_sal`（q1_business）｜營收（GAAP，Total Worldwide Sales）＝16607 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/；細項損益表引自 SEC 8-K exhibit 99.1（sec.gov/Archives/edgar/data/0000310158/000110465926090045/tm2621496d1_ex99-1.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：consensus 約 $16.41B，實際 $16.607B 為 beat（來源：web_search 彙整分析師預估，非官方一手數字）
- `f_kpi1_non_gaap_non_gaap_operat`（q1_business）｜Non-GAAP 稅前利益率（無法拆出獨立 non-GAAP operating income，新聞稿只揭露 non-GAAP pretax income）＝3.3 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K exhibit 99.1 reconciliation 表：non-GAAP pretax income $550M / 營收 $16,607M（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：查無官方逐項 consensus 對照
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝-2.6 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（Operating Income -$433M / Revenue $16,607M）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：查無官方逐項 consensus 對照
- `f_kpi5_2026_guidance`（q1_business）｜管理層全年 2026 guidance＝— range｜期間與口徑：公告於 2026-08-04（隨 Q2 FY2026 財報同步更新）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/（numbers.latest_quarter_kpis.items[5]，as_of 公告於 2026-08-04（隨 Q2 FY2026 財報同步更新））
  - 註記：營收 guidance 上調：$66.3B–$67.3B（前次 $65.8B–$67B）；Non-GAAP EPS guidance 大幅下修：$2.66–$2.76（前次 $5.04–$5.16），下修原因為 Terns（$2.43/股）與 Cidara 收購一次性費用認列，非營運惡化
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_mrk_gross_margin_pct`（q2_moat）｜MRK 毛利率＝71.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mrk_operating_margin_pct`（q2_moat）｜MRK 營業利益率＝0.87 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mrk_fcf_margin_pct`（q2_moat）｜MRK FCF 利潤率＝18.72 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pfe_gross_margin_pct`（q2_moat）｜PFE 毛利率＝73.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PFE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pfe_operating_margin_pct`（q2_moat）｜PFE 營業利益率＝26.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PFE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pfe_fcf_margin_pct`（q2_moat）｜PFE FCF 利潤率＝17.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PFE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bmy_gross_margin_pct`（q2_moat）｜BMY 毛利率＝69.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMY.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bmy_operating_margin_pct`（q2_moat）｜BMY 營業利益率＝29.19 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bmy_fcf_margin_pct`（q2_moat）｜BMY FCF 利潤率＝18.56 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMY.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abbv_gross_margin_pct`（q2_moat）｜ABBV 毛利率＝71.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBV.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abbv_operating_margin_pct`（q2_moat）｜ABBV 營業利益率＝33.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abbv_fcf_margin_pct`（q2_moat）｜ABBV FCF 利潤率＝28.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.72 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.14 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝10.12 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.98 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（9.23 → 9.14）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.78 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（10.2 → 10.12）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝67186.2 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝69584.64 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝4477 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（Operating Cash Flow $5,370M − CapEx $893M）；FCF margin = 4477/16607 = 27.0%（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：查無官方逐項 consensus 對照
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收 %＝1.79 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（Stock Based Compensation $298M / Revenue $16,607M）；因 GAAP 營業利益為負，改以占營收表示（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：查無官方逐項 consensus 對照
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝46770.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 53911.0、現金 7141.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.289 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2467.17 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝148.56 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝33.08 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝55.33｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝150.06 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝18.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝18.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.44 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.13 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝54.62 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 2.72，分子＝快照價 148.57｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝413280.67 USD m｜期間與口徑：2026-11-03／市值 366510.67 ＋ 淨負債 46770.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 148.66 / W52 121.86 / W104 102.52 / W250 98.98 / W250 13週斜率 1.28%」
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.73 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 2.74 → 2.72（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Gardasil 2026Q1 銷售暴跌 22% 至 10.7 億美元，中國市場（佔美國以外銷量 60-70%）需求因經濟放緩疲弱，且面臨中國本土 HPV 疫苗以十分之一價格搶市；Merck 已暫停對中國經銷夥伴智飛生物的出貨以消化通路庫存
  - 來源：BioPharma Dive / Fierce Pharma / Yahoo Finance 綜合搜尋摘要（as_of 2026-05-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Merck 的三大藥品批發商客戶（McKesson、AmerisourceBergen、Cardinal Health）合計占應收帳款相當高比重，屬產業結構性集中，非新增惡化
  - 來源：Merck & Co., Inc. Form 10-K FY2022（as_of 2022-12-31）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Gardasil 在中國因通路庫存偏高＋需求疲軟，Merck 自2025年2月暫停出貨，管理層預期2026年銷售不會回升；文章判斷中國經濟放緩屬暫時性因素，但同時提到日本需求下滑趨勢會持續，顯示週期性與結構性因素並存
  - 來源：Yahoo Finance - Will Weak Gardasil Sales Continue to Weigh on MRK's Top Line in 2026?（as_of 2026-03-09）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Merck 2025年2月起暫停對中國出貨；2026年4月與中國經銷夥伴（智飛）簽署修訂後供貨合約；2026年第2季開始恢復有限出貨，但該合約相關營收預期2026年內仍不重大——顯示去化庫存＋需求回補為多季期的結構性過程，非單一季度週期性波動
  - 來源：Merck & Co., Inc. Form 10-Q FY2026 Q2 (SEC)（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Keytruda（占公司腫瘤營收核心）美國組成物專利2028年到期、用法專利至2029年11月，這是結構性、時程明確的懸崖，非週期性問題；公司揭露此為重大風險因子
  - 來源：Merck & Co., Inc. Form 10-K FY2025 (SEC)（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、valuation、moat_trend
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：參議員 Hassan（參院財政委員會健保小組資深議員）對 Merck 的 Keytruda 專利策略與 product hopping（劑型轉換）發起國會質詢，指控其藉此延遲低價競爭產品上市
  - 來源：Senator Hassan press release / ICIJ 'Cancer Calculus' investigation（as_of 2026-09-13）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Merck 於 2024年6月收到 DOJ 依 False Claims Act 發出的民事調查要求(CID)，就 Steglatro、Januvia 在 Medicaid 藥物回扣計畫下的價格申報，以及病患協助計畫的反回扣法遵規範進行調查
  - 來源：Merck & Co. Form 10-Q (FY2026)（as_of 2024-06）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：巴爾的摩市於2023年3月對 Merck 子公司提起反壟斷集體訴訟，指控其利用小兒疫苗市場的壟斷力進行搭售，維持 RotaTeq（輪狀病毒疫苗）市場的壟斷地位並收取超額定價
  - 來源：Merck & Co. Form 10-Q / SEC filings (litigation disclosure)（as_of 2023-03）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：Merck 對 HHS 提起訴訟，主張 IRA（降低通膨法案）的 Medicare 藥價強制議價機制違憲；Januvia／Janumet 已分別於2023年、2025年被選入該議價名單
  - 來源：The Philadelphia Inquirer（as_of 2023-11-30）｜affects：thesis.R、valuation、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：川普政府於 2026-04-02 發布 Section 232 公告，對專利藥品及其原料進口課高達 100% 關稅；默克（Merck Sharp & Dohme）被列在 Annex III 的 17 家指名大廠名單中，適用公告發布後 120 天生效（即 2026-07-31），其餘廠商則自 2026-09-29 生效。
  - 來源：白宮 Section 232 藥品關稅公告 Annex 分析（法律事務所/貿易媒體報導彙整，如 McDermott Will & Emery、Mallory Group）（as_of 2026-04-02）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：美國眾議院中國問題特別委員會主席 Moolenaar 於 2026-06-30 去函 Merck 與 AbbVie，要求說明在中國（含新疆與解放軍附屬醫院）進行臨床試驗的場址審查、資料保護與安全標準，7/17 前需回覆。
  - 來源：Investing.com (Reuters) — US House committee opens investigation into Merck, AbbVie China drug trials（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Merck 自 2005 年起在中國贊助或參與 224 項臨床研究，其中至少 31 項位於新疆、40 項在解放軍附屬醫院或醫療機構進行，成為本次國會調查的具體規模依據。
  - 來源：GuruFocus — Merck (MRK) Faces National Security Scrutiny Over China Trials（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Gardasil(HPV疫苗)段H1 2026合併銷售年減9%，主因中國、日本需求疲弱
  - 來源：SEC 10-Q FY2026 Q2 (Merck & Co.)（as_of 2026-06-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：管理層不預期Gardasil在2026年好轉，2026全年財測未計入任何中國出貨（因中國合作夥伴智飛通路庫存過高，先前已暫停出貨至2025年底）
  - 來源：Fierce Pharma - Merck halts Gardasil shipments to China（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear、valuation
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：Keytruda 2028年專利懸崖：美國核心化合物專利2028到期，涉及逾$25B年化腫瘤營收；2026年生物相似藥侵蝕預期輕微（僅阿根廷等小型市場上市），但Medicare藥價協商新折扣價將於2028年1月生效，市場預期Keytruda美國銷售2027-28見頂後轉降
  - 來源：Patsnap - Keytruda patent cliff 2028: Merck's strategy（as_of 2026-01-01）｜affects：thesis.R、valuation、triggers、moat_trend
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：中國 Akeso 與 Summit Therapeutics 合作開發的 PD-1xVEGF 雙特異性抗體 ivonescimab，在晚期肺癌頭對頭試驗中擊敗 Keytruda，是 Keytruda 上市十年來首次在此類試驗中落敗。
  - 來源：BioPharma Dive - "Merck, facing threat to Keytruda, buys into new kind of cancer immunotherapy"（as_of 2024-11-14）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Cipla 美國子公司已取得 Qilu Pharmaceutical pembrolizumab 生物相似藥 QL2107 的美國獨家銷售權，搶在 Keytruda 核心專利於 2028 年 12 月到期前卡位；報導指出 Keytruda 的生物相似藥倒數計時聲量正在變大。
  - 來源：GuruFocus - "Merck's $8.4 Billion Keytruda Fortress Gets a 2028 Warning"（as_of 2026-09-03）｜affects：moat_trend、thesis.R、decision_inputs.bear、valuation
- `substitute_technology#5`（substitute_technology｜方向 -｜狀態 ok）：新創公司 Crescent Biopharma 正開發 PD-1xVEGF 雙特異性抗體 CR-001，其定位明確是要取代 pembrolizumab 作為免疫腫瘤療法的新骨幹用藥，相關臨床試驗於 2026 年啟動。
  - 來源：DIMA Biotechnology - "2026 ASCO Target Review (Part II): Bispecific and Multispecific Antibodies and Immunotherapy Combinations"（as_of 2026）｜affects：moat_trend、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露 Cronin v. Merck 證券集體訴訟（Gardasil 中國需求陳述），期間 2023-10-26 至 2025-02-03；修正訴狀 2026-02-20 提出，駁回動議 2026-05-01 到期。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-24）｜affects：decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：Emend（aprepitant）口服懸液 125mg 單劑套組 Class II 召回 D-0241-2026，原因為可能含金屬微粒，2025-12-12 起、仍進行中。
  - 來源：recallcheck.net 召回清單（搜尋摘要）（as_of 2025-12-12）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Cronin v. Merck 證券集體訴訟（Gardasil 中國需求），另有 Daniel 與 Kistenmacher 兩件衍生訴訟；駁回動議 2026-05-01 到期。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-24）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：Emend 口服懸液套組 Class II 召回 D-0241-2026（可能含金屬微粒），2025-12-12。未見 2026 警告信。
  - 來源：recallcheck.net 召回清單（搜尋摘要）（as_of 2025-12-12）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":214.2,"bear_5y_price":81.4,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":-5.8,"ev5y_pct":-7.6,"irr_base_pct":-1.2,"asym_ratio":0.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":9.14,"pe":16.25,"basis":"FY2027 共識 EPS 9.14 美元（前瞻約一年）；FY2026 共識 2.72 含收購研發一次性費用不可用；終端倍數同樣套在全年 EPS 上，與起點同口徑"},"eps":{"bull":[9.2,10.2,10.4,11.5,12.6],"base":[8.95,9.5,8.9,9.3,10.0],"bear":[8.6,8.7,7.6,7.1,7.4]},"pe":{"bull":17,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.289,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MRK_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Caroline Litchfield｜guidance：CFO 說全年營收財測上修並收窄至 663–673 億美元（成長 2%–4%）（原話："to be between $66.3 billion and $67.3 billion"）
- 2026-08-04｜Caroline Litchfield｜guidance：全年 non-GAAP EPS 財測 2.66–2.76 美元，中點 2.71（原話："we expect EPS of $2.66 to $2.76 with a midpoint of $2.71"）
- 2026-08-04｜Caroline Litchfield｜margin：全年毛利率假設約 81%，反映較高的存貨提列（原話："Gross margin is now assumed to be approximately 81%"）
- 2026-08-04｜Caroline Litchfield｜margin：Q2 non-GAAP 毛利率 81.1%，年減 1.1 個百分點，管理層歸因於存貨提列（原話："Gross margin was 81.1%, a decrease of 1.1 percentage"）
- 2026-08-04｜Caroline Litchfield｜margin：數字口徑：剔除 Terns 收購費用後，營業費用成長 7%（原話："Excluding these charges, operating expenses grew 7%"）
- 2026-08-04｜Caroline Litchfield｜guidance：全年稅率預期上調至 35%–36%，因 Terns 一次性費用不可抵稅（原話："We now expect a full year tax rate between 35% and 36%"）
- 2026-08-04｜Caroline Litchfield｜guidance：EPS 財測含 Terns 一次性每股 2.31 美元費用（原話："an upfront charge of $2.31 per share related to the"）
- 2026-08-04｜Caroline Litchfield｜guidance：營業費用財測不含其他重大潛在 BD 交易（原話："This guidance does not assume"）
- 2026-08-04｜Caroline Litchfield｜guidance：OHTUVAYRE 第三季銷售將受第二季專業藥局進貨回沖影響（原話："unwind of specialty pharmacy purchases in the second"）
- 2026-08-04｜Caroline Litchfield｜commitment：管理層預期 OHTUVAYRE 相關投入將帶動 2027 年加速成長（原話："expect these actions to lead to accelerated growth in 2027"）
- 2026-08-04｜Caroline Litchfield｜guidance：下半年美國 KEYTRUDA 年增率預期趨緩（原話："total U.S. KEYTRUDA year-over-year growth will moderate"）
- 2026-08-04｜Caroline Litchfield｜guidance：數字口徑：2025 年第三季約 2.5 億美元批發商進貨時點效益今年不會重複（原話："approximately $250 million due to the timing of wholesaler"）
- 2026-08-04｜Caroline Litchfield｜competition：BRIDION 美國銷售預期下滑速度較先前預期慢，因學名藥競爭低於預期（原話："decline at a slower pace than previously expected"）
- 2026-08-04｜Caroline Litchfield｜guidance：下半年其他營收預期明顯高於去年同期，來源為營收避險計畫與第四季授權里程碑（原話："expected to be significantly higher than the second half"）
- 2026-08-04｜Caroline Litchfield｜capital_allocation：今年約 30 億美元庫藏股如先前所述（原話："approximately $3 billion in share repurchases this year"）
- 2026-08-04｜Caroline Litchfield｜commitment：管理層承諾維持股利並以逐步提高為目標（原話："We remain committed to the dividend with the goal of"）
- 2026-08-04｜Caroline Litchfield｜capital_allocation：BD 仍為高優先，維持強投資等級信評下可再做交易（原話："development remains a high priority, and we maintain"）
- 2026-08-04｜Caroline Litchfield｜product：KEYTRUDA QLEX 本季 4.63 億美元，管理層對採用軌跡有信心（原話："confident in the trajectory of KEYTRUDA QLEX adoption"）
- 2026-08-04｜Caroline Litchfield｜product：WINREVAIR 美國已有逾 1,800 名新病人開立處方（原話："1,800 new patients having received a prescription"）
- 2026-08-04｜Caroline Litchfield｜customer：GARDASIL 美國持平，需求較低與 CDC 採購時點被價格大致抵銷（原話："the U.S. was roughly flat as lower demand and timing of CDC"）
- 2026-08-04｜Robert Davis｜risk：CEO 描述 KEYTRUDA 專利到期期間為淺坑而非懸崖（原話："the LOE period is more of a hill than a cliff"）
- 2026-08-04｜Robert Davis｜commitment：CEO 稱預期淺幅下滑後快速回到成長，並以未風險調整基礎仍期望成長穿越（原話："a shallow dip with a fast return back to growth"）
- 2026-08-04｜Robert Davis｜risk：CEO 就 700 億美元機會的最大風險被問及，稱難以指出擔心之處（原話："It's hard to frankly point to anything I'm worried about"）
- 2026-08-04｜Robert Davis｜product：敘事變化：CEO 稱信心高於 1 月，因讀數提前（原話："my confidence is higher than it was in January"）
- 2026-08-04｜Robert Davis｜product：CEO 說 1 月時 sac-TMT 與 I-DXd 預計 2027 才有讀數，現已都有正面讀數（原話："we had highlighted sac-TMT as well as I-DXd as not having"）
- 2026-08-04｜Robert Davis｜product：LIPFENDRA 上市初期節奏預期不會一開始就很快，但長期仍預期為重磅（原話："expecting to see the pace not be as fast out of the gate"）
- 2026-08-04｜Robert Davis｜commitment：依 MFN 協議，公司承諾將 LIPFENDRA 上架 TrumpRx（原話："in our MFN agreement, we did commit to"）
- 2026-08-04｜Robert Davis｜competition：LIPFENDRA 定位為市場擴張而非搶注射型 PCSK9 份額（原話："we are not focusing this market on how do we"）
- 2026-08-04｜Caroline Litchfield｜customer：CFO 稱需把學術領袖的正面回饋轉化到基層醫療端（原話："What we need to do is to translate that to the primary care"）
- 2026-08-04｜Dean Li｜risk：LIPFENDRA 目前沒有 CVOT，進行中的試驗 2029 年讀數（原話："we have an ongoing trial that will read out in 2029"）
- 2026-08-04｜Dean Li｜product：LIPFENDRA 與 rosuvastatin 固定複方，管理層希望 LDL 降幅可達 80%（原話："we think that we could get up to 80%"）
- 2026-08-04｜Dean Li｜risk：流感藥 MK-1406 第三期延長至第二個北半球流感季，仍稱 2029 年可能核准（原話："potential approval in 2029"）
- 2026-08-04｜Robert Davis｜risk：CEO 被問延長試驗是否因數據，回答信心沒有改變，純為申報強度（原話："there's no change in our confidence"）
- 2026-08-04｜Dean Li｜product：tulisokibart 在 SSc-ILD 第二期未達主要終點（原話："the study did not meet its primary end point"）
- 2026-08-04｜Dean Li｜product：tulisokibart 在化膿性汗腺炎第二期達主要與關鍵次要終點（原話："the study met its primary and key secondary endpoints"）
- 2026-08-04｜Dean Li｜product：Dean Li 稱不會因 SSc-ILD 結果放棄免疫纖維化假說（原話："I would not throw out the immunofibrosis"）
- 2026-08-04｜Dean Li｜product：sac-TMT 子宮內膜癌第三期 TroFuse-005 在 OS 與 PFS 皆顯著改善（原話："statistically significant and clinically meaningful"）
- 2026-08-04｜Dean Li｜competition：敘事變化：sac-TMT 肺癌一線將重新思考 KEYNOTE-189 設計，不限 PD-L1 表現（原話："So yes, we are going to rethink KEYNOTE-189"）
- 2026-08-04｜Dean Li｜competition：AVANZAR 讀數後再決定 sac-TMT 是否需要生物標記（原話："You can always have a biomarker, but that doesn't mean"）
- 2026-08-04｜Dean Li｜competition：PD-1/VEGF 策略：關注 Summit/Akeso 數據（原話："We are very interested in following the Summit Akeso data"）
- 2026-08-04｜Dean Li｜commitment：alimatravir 兩項第三期預計明年讀數（原話："Phase III studies anticipated to read out next year"）
- 2026-08-04｜Dean Li｜commitment：WINREVAIR 標示更新 PDUFA 日為 9 月 21 日（原話："September 21 PDUFA date for WINREVAIR"）
- 2026-08-04｜Dean Li｜commitment：10 月 26 日 ESMO 投資人活動預告（原話："Monday, October 26, where we will host an investor event"）

### MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜commitment：MK-2010 第一線非小細胞肺癌（含與 sac-TMT 合用）Phase III 預計 2027 上半年啟動（原話："we anticipate initiating Phase III development for MK-2010"）
- 2026-10-26｜Eliav Barr (CMO)｜guidance：sac-TMT 子宮內膜癌 FDA PDUFA 日期為 6/15（原話："The FDA has granted a PDUFA date of June 15."）
- 2026-10-26｜Eliav Barr (CMO)｜guidance：管理層指明明年有兩個重要腫瘤藥核准潛力（sac-TMT、intismeran）（原話："we see the potential of 2 important oncology approvals"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse 計畫有 18 項進行中全球 Phase III（原話："Our TroFuse program currently includes 18 ongoing global"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse-005 降低進展或死亡風險 41%（原話："reduced the risk of disease progression or death by 41%"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INTerpath-001 降低復發或死亡風險 42%（原話："significantly reduced the risk of recurrence or death by 42%"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INT 前 6 個月曲線重疊（非比例風險）（原話："During the first 6 months, the curves are largely"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：管理層強調該敏感度分析不取代 ITT 分析（原話："does not replace the ITT analysis"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：輔助黑色素瘤檢查點抑制劑尚未改善整體存活（原話："have not yet improved overall survival"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：MK-2010 為 Phase III-ready 資產（原話："MK-2010 is a Phase III-ready asset"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：新輔助 NADINA 研究約 30% 發生 3 級以上毒性（原話："about 30% of people get very significant grade 3 or higher"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：管理層稱 INTerpath-001 與 NADINA/SWOG 無法直接比較（原話："they are very apples and oranges in their approach"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INT 製程週轉時間約 6 週（原話："the turnaround time is around 6 weeks"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜commitment：管理層稱 INT 已備妥商業化（原話："So we're ready for commercialization."）
- 2026-10-26｜Eliav Barr (CMO)｜product：已與監管機關接觸討論 intismeran（原話："we are already engaging with regulatory authorities"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：sac-TMT+MK-2010 vs 與 pembro 組合的設計未揭露，目標取代 KEYNOTE-189（原話："if your goal is really to displace KEYNOTE-189"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：sac-TMT 全球研究劑量 4 mg/kg，無誘導加維持的前瞻計畫（原話："There isn't a current prospective plan"）
- 2026-10-26｜Eliav Barr (CMO)｜customer：新輔助黑色素瘤不會成為主流，輔助為多數病人的路徑（原話："I don't see neoadjuvant becoming the rage."）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜capital_allocation：與 Moderna 的 INT 製造合作（原話："Moderna has been amazing partners to work with"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：生物標記策略未揭露主要假設（原話："where we might have a primary hypothesis about a biomarker"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：與 FDA 就非比例風險的討論內容未揭露（原話："we have not talked about our discussions with the FDA"）
- 2026-10-26｜Eliav Barr (CMO)｜product：INT 單藥與 KEYTRUDA 外組合的探索（AE 考量）（原話："still has an AE profile that requires careful attention"）
- 2026-10-26｜Eliav Barr (CMO)｜commitment：預期 2027 年有 INT 相關研究讀數（原話："I anticipate that 2027 will have some really interesting"）
- 2026-10-26｜Eliav Barr (CMO)｜risk：RCC 為 Phase II，不預設監管結果（原話："we don't want to get ahead of the regulatory authorities"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse-010 為第一線研究（原話："It is a frontline study, yes."）

### 問答異常語氣（迴避／改口／保留）
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Geoff Meacham（Citi）問 LIPFENDRA 初期可及性節奏、報銷預期與是否需要 CVOT 作為商業轉折｜答法：Dean Li 先轉給 CEO；Rob 談標示乾淨、需時間建立可及性、初期速度較慢，未給報銷預期或數字，也未直接回答 CVOT 問題
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Chris Schott（JPMorgan）問 2028 至 2030 年代初 KEYTRUDA LOE 過渡期的獲利輪廓｜答法：CEO 以「hill than a cliff」「shallow dip」作答，未給 EPS 或營收數字，並說「still potential more to do」
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Courtney Breen（Bernstein）問 LIPFENDRA 何時上架 TrumpRx｜答法：Rob 說待初始上市後上架，只說 more to come on timing，未給時點
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Luisa Hector（Berenberg）問標示文字對支付方的影響，以及 GLP-1 使用下降是否影響 LIPFENDRA CVOT｜答法：Dean Li 先說須小心談 FDA 意圖，只答標示與 CVOT 2029 時點，未回應 incretin 使用下降對試驗的影響
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Michael Yee（UBS）問 tulisokibart UC 第三期輪廓（稱公告內容不多）及纖維化論點｜答法：Dean Li 未談 UC 第一項試驗的療效數字，轉述等待第二項試驗讀數；SSc-ILD 部分以「沒有抗細胞激素藥有效」及安慰劑組為由解釋
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：TroFuse-010 規模與讀數時間是否不變｜答法：未直接回答，改請看 ct.gov
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：sac-TMT 是否使用 CNPV、PDUFA 能否提前｜答法：未回答是否使用 CNPV，只說提交後都會拿到 PDUFA 日期
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：是否以 MK-2010+sac-TMT 對戰 KEYNOTE-189、適用組織型｜答法：稱問題為 leading question，只說 stay tuned
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：Phase III 非比例風險分析與 FDA 討論｜答法：拒絕透露與 FDA 討論，答 stay tuned

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 1 | 4 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 2 | 4 |
| end_markets | found | 7 | 6 |
| substitute_technology | found | 6 | 4 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 2 | 2 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Merck largest customer wholesalers McKesson Cardinal AmerisourceBergen percent of sales 10-K；Merck Keytruda subcutaneous in-house OR second source supplier manufacturing 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260929","verdict":"迴避","role":"不持有","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","irr_base_pct":-1.0,"ev5y_pct":-8.9,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有","signal":"C","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":0.5,"ev5y_pct":-8.9,"irr_base_pct":-1.0,"max_dd_pct":-48,"bull_5y_price":198.4,"bear_5y_price":83.6,"p_bull_pct":20,"p_bear_pct":30,"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","price_at_dd":148.69,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MRK","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Merck & Co., Inc."},"oneliner":"Keytruda 專利到期前的換軌期：三期讀數與新藥放量都好，但現價約 FY2027 共識 16 倍、Base 五年年化不到 2%；等 Qlex 與新品放量、且股價落到 FY2027 共識 13 倍以下再重新研究","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺癌症病人與付款方的錢：Keytruda 家族約占營收一半，錢卡在美國專利與 Medicare 議價這一節點，2028–2029 年開始鬆動","reasoning":"收錢方式：專利期內的處方藥與疫苗，經美國三大批發商出貨，最後由 Medicare、商業保險與各國政府付款。營收分部（2026Q3 總營收 181 億美元、年增 5%，Q3 法說）：Keytruda 家族 86 億美元（約 48%、年增 6%，含 Qlex 8.3 億）、Gardasil 20 億美元（約 11%、年增 14%，含 CDC 採購與時點效益）、Winrevair 6.94 億、Welireg 3.07 億、動物保健年增 3%。單點依賴：Keytruda 一項約占營收一半，這是集中度風險，不是護城河證據。利潤率：2026Q2 營收 166.07 億美元，GAAP 營業利益率 −2.6%、調整後稅前利益率 3.3%，都被 Terns 收購研發費用壓低；Q3 調整後毛利率 81.4%、營業費用年增 12%。產業時鐘 III：核心 PD-1 單抗在多個已核准適應症接近滲透高峰（CFO 2026-10-29），2028 年起進入 Medicare 議價與專利到期。產業態勢雙向拉鋸：競爭端惡化（雙特異抗體頭對頭勝過 Keytruda、Imfinzi 年增 30%、生物相似藥卡位），其他結構變數同時在動（Medicare 議價、MFN 直售平價方案、Section 232 關稅以美國投資換三年延後），需求端仍在擴張（PD-1 市場預估年複合 18.7%）。","fact_refs":["f_kpi0_gaap_total_worldwide_sal","f_kpi1_non_gaap_non_gaap_operat","f_kpi2_gaap","f_kpi5_2026_guidance","f_earnings_recency","f_peer_mrk_gross_margin_pct","f_peer_mrk_operating_margin_pct"],"verdict_values":{"revenue_quality":"專利處方藥與疫苗，重複性高；但 2026Q3 含約 5.5 億美元美國進貨時點效益（Keytruda 2 億、Winrevair 0.5 億於 Q4 回吐，疫苗 3 億中 2.5 億在 2027 年回吐），單季成長被墊高","unit_econ_note":"2026Q3 調整後毛利率 81.4%、營業費用年增 12% 至 74 億美元、調整後 EPS 2.49 美元（含 SciBrunch 每股 0.12 美元費用）；TTM GAAP 營業利益率 0.87% 被收購研發費用壓低，FY2025 的 34.01% 才是常態參考","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"高毛利專利藥＋單一大藥專利到期前的換軌期"},"industry":{"clock_phase":"III","sd_verdict_source":"需求面結構性持久（PD-1/PD-L1 市場 2026 年約 738.7 億美元、預估年複合 18.7%），但 Merck 能分到多少由專利時程決定，屬時程明確的結構性下行，不是週期","bargaining":{"up":"上游原料與代工不是瓶頸；供應商集中度事實表未涵蓋","down":"美國三大批發商占應收約 54%（2022 年資料）只是物流通路，真正的定價方是 Medicare、商業保險與 PBM；2026-02 與政府的 MFN 協議與直售病人平價方案進一步壓縮定價","geo":"中國：Gardasil 需求崩落、本土 HPV 疫苗以十分之一價格競爭，眾議院調查 Merck 在中國的臨床試驗；美國：Section 232 專利藥關稅以美國投資換三年延後"},"profit_pool_dir":"PD-1 利潤池仍在擴大，但 2028 年後從原廠單抗流向生物相似藥、付款方與 PD-1×VEGF 雙特異抗體新進者","tam_table":[{"item":"PD-1/PD-L1 全球市場","value":"2026E 約 738.7 億美元，預估 2033 年 2,452.5 億美元、年複合 18.7%（Future Market Insights）"},{"item":"Keytruda 家族份額","value":"2026 年上半年 164.0 億＋Q3 86 億美元，年化約 333 億，約占 2026E 市場 45%"},{"item":"主要對手","value":"Opdivo 2026Q1 21.5 億美元（年減 5%）；Imfinzi 2026Q1 16.9 億美元（年增 30%）"},{"item":"利潤池遷移","value":"2028-01 Medicare 議價價格生效、2028-12 美國核心專利到期；雙特異抗體爭奪下一代骨幹"},{"item":"營業利益池 5 年前→現占比","value":"事實表未涵蓋，無法判定是否淨流出 5 個百分點以上"}]}}},"q2_moat":{"verdict":"護城河縮減中：執行力穩定，但定價權在收縮","reasoning":"機制：專利保護的生物藥＋腫瘤科商業規模＋以 Keytruda 為骨幹的組合開發能力。可證方向：投入資本事實表未涵蓋，取不到 ROIC 差，改看利潤率與份額。FY2025 營業利益率 34.01%，與 ABBV TTM 33.94% 相當、高於 BMY 29.19% 與 PFE 26.72%；但 TTM FCF 利潤率 18.72% 低於 ABBV 28.28%，研發密度 53.19%（含收購研發）是同業的 2.5–3.5 倍。份額：Keytruda 家族仍年增 5–6%、Opdivo 年減 5%，領先地位未失，但 Imfinzi 年增 30%、Opdivo 皮下劑型早 9 個月上市。執行力評 7：新藥上市順利、三期接連正向，但 I-DXd 撤回加速核准申請、tulisokibart 在 SSc-ILD 失敗、Capvaxive 美國年減 13%。定價權評 5：Keytruda 2028 年 Medicare 議價、MFN 協議與直售平價方案、德國政策與美國以外價格逆風、Gardasil 中國十分之一價格競爭。方向：執行力穩定、定價權縮減，整體縮減。","fact_refs":["f_peer_mrk_gross_margin_pct","f_peer_mrk_operating_margin_pct","f_peer_mrk_fcf_margin_pct","f_peer_pfe_gross_margin_pct","f_peer_pfe_operating_margin_pct","f_peer_pfe_fcf_margin_pct","f_peer_bmy_gross_margin_pct","f_peer_bmy_operating_margin_pct","f_peer_bmy_fcf_margin_pct","f_peer_abbv_gross_margin_pct","f_peer_abbv_operating_margin_pct","f_peer_abbv_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"專利保護的生物藥＋腫瘤科商業規模＋以 Keytruda 為骨幹的組合開發能力（sac-TMT、intismeran、calderasib 都設計成與 Keytruda 併用或取代化療組合）","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價權縮減：Keytruda 2028-01 Medicare 議價價格生效、2028-12 美國核心專利到期；Qlex 遭荷蘭法院禁制令，歐洲 6 國停供；德國政策與美國以外價格逆風（Q3 法說）；Gardasil 中國面對十分之一價格的本土疫苗。執行力穩定：Winrevair 年增 94%、Qlex 單季 8.3 億美元、sac-TMT 與 intismeran 三期正向，但也有撤件與失敗","competitor_notes":[{"name":"PFE","strategy_note":"營業利益率 26.72%、FCF 利潤率 17.25%、研發密度 17.35%；同樣處於專利到期期，不是 PD-1 直接對手"},{"name":"BMY","strategy_note":"Opdivo 2026Q1 年減 5%，皮下劑型雖早 9 個月上市仍追不上 Keytruda；營業利益率 29.19%"},{"name":"ABBV","strategy_note":"營業利益率 33.94%、FCF 利潤率 28.28% 皆為同業最高，現金創造力優於 Merck；不在 PD-1 戰場"},{"name":"AZN（Imfinzi）","strategy_note":"Imfinzi 2026Q1 16.9 億美元、年增 30%，成長快於 Keytruda，是份額端最明確的追趕者（利潤率事實表未涵蓋）"},{"name":"Summit／Akeso（ivonescimab）","strategy_note":"PD-1×VEGF 雙特異抗體在肺癌頭對頭試驗勝過 Keytruda，威脅的是骨幹地位，不是單一適應症"}],"peer_na_reason":"事實表未涵蓋投入資本，無法算同業 ROIC 差；改用營業利益率與 FCF 利潤率對照，且 MRK TTM 營業利益率 0.87% 被收購研發費用扭曲，以 FY2025 的 34.01% 代替","threats":[{"level":"🔴","text":"PD-1×VEGF 雙特異抗體攻擊 pembrolizumab 的骨幹地位（ivonescimab 頭對頭勝出、Crescent CR-001 進臨床）；Merck 以自有 MK-2010 對沖，所以列為生態攻擊而非架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"level":"🟡","text":"生物相似藥卡位（Cipla 取得 Qilu QL2107 美國權利）與 2028 年 12 月美國核心專利到期：時程已知的點對點替代，已放進各情境","p":"時程確定","evidence_refs":["substitute_technology#3","supply_demand_durability#2"]},{"level":"🟡","text":"Gardasil 在中國面對十分之一價格的本土 HPV 疫苗","p":"已發生","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"Opdivo 皮下劑型早 9 個月上市、Imfinzi 年增 30%：份額端的點對點競爭","p":40,"evidence_refs":["competitive_share_entrants#3"]}],"roic_durability":{"quadrant":"高利益率×低周轉（投入資本事實表未涵蓋，依 FY2025 營業利益率 34.01% 與大量收購無形資產定性判斷）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是病人、決策者是腫瘤科醫師、付款者是 Medicare 與保險，三角色都成立；癌症治療是需要不是想要，延後的代價是存活。PD-1 市場 2026 年約 738.7 億美元、預估年複合 18.7%。但要解決的問題（免疫治療）會持續，公司目前的解法（pembrolizumab 單抗）不一定"},{"item":"決策層級","level":"🟡","text":"決策最小單位是治療指引與醫院處方集，生物相似藥上市後處方集可整批切換；Qlex 自 2026-04-01 取得永久給付代碼，改變給藥流程形成轉換成本，管理層目標 2027 年底美國轉換 30–40%，但 IV 版本在 2028 年後替代性很高"},{"item":"價值鏈分配","level":"🟡","text":"專利期內價值集中在原廠（調整後毛利率約 81%）；2028 年起 Medicare 議價生效、核心專利到期，價值移向付款方與生物相似藥廠；MFN 協議與直售平價方案再讓一段給付款端。新藥（Winrevair、sac-TMT）各自重建定價空間"},{"item":"社會容忍度","level":"🔴","text":"高必要×高敏感：參議員 Hassan 質詢 Keytruda 專利策略與劑型轉換延遲低價競爭；IRA 議價（Januvia／Janumet 已入選，Merck 提告違憲）；與政府的 MFN 協議與直售平價方案；德國政策逆風。實際定價上限已由政治上限決定"}],"roiic":"無法以實現值計算：投入資本與 2023–2025 收購總額事實表未涵蓋；可見增量為 2022→2025 營業利益增加約 38 億美元。判斷假設取約 10%","reinvest_rate":"約 40%（2026 年單年下限）","endo_ceiling":4.0,"formula_note":"內生成長上界＝增量報酬 × 再投資率＝約 10% × 約 40% ≈ 4%。增量報酬取約 10%：收購資產多數尚未上市、報酬未實現，不給高於資金成本太多的假設；再投資率約 40%：2026 年可見收購與授權至少約 78 億美元（Terns 約 67、TARGAN 約 6.5、SciBrunch 預付 4 億）÷ FY2025 淨利 182.5 億美元，Cidara 金額未涵蓋，實際更高。兩者都是判斷假設，不是已實現數字"}}}},"q3_growth":{"verdict":"五年後跑道中等：新藥是有三期數據的第二條曲線，但規模只夠把 Keytruda 的坑填平","reasoning":"成長來源以量為主：新藥放量（Winrevair 年增 94%、Qlex 單季 8.3 億）與併購帶入的管線（Terns、Cidara、TARGAN）；價格面受壓；回購每年約 30 億美元、約占市值 0.8%。三年共識 EPS：FY2026E 2.72（收購研發費用壓低）、FY2027E 9.14、FY2028E 10.12（Koyfin 快照，家數事實表未涵蓋；營收共識 23 位分析師）。以事實表唯一可得的 FY2025 GAAP 稀釋 EPS 7.28 當基期，三年年複合約 11.6%，但基期與共識口徑不同，高估真實成長。內生成長上界約 4%（見護城河段），缺口歸因見下欄，無法歸因的部分依賴重新評價，長期信心上限為中。五年後跑道：Keytruda 已在多個適應症接近滲透高峰（CFO 2026-10-29），新藥是有三期數據支持的第二條曲線，但管理層 2030 年代中期 700 億美元目標相對 2026 年財測中點 670.5 億只是持平，所以是中等跑道。FY2027／FY2028 共識近期各下修 0.98%／0.78%，CFO 又說多數分析師尚未納入 2027 投資年訊息。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_2026_guidance"],"verdict_values":{"growth":{"driver_mix":"量為主：新藥放量與併購帶入的管線；價格面受 Medicare 議價、MFN 與美國以外降價壓制；回購每年約 30 億美元、約占市值 0.8%","runway_years":"不適用：Keytruda 已在多個適應症接近滲透高峰；新藥各適應症滲透率事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：內生成長上界約 4%（增量報酬約 10% × 再投資率約 40%）。三年共識 EPS 以 FY2025 GAAP 7.28 美元為基期、到 FY2028E 10.12 美元，年複合約 11.6%，缺口約 7.6 個百分點：①基期是 GAAP、共識是調整後口徑，部分是口徑差而非真成長；②2027 年 Keytruda 權利金到期帶動毛利率上升（利潤率擴張）；③舉債收購帶入的新藥（收購）。剩餘部分無法歸因、依賴重新評價","segments":[{"item":"Keytruda 家族（2026Q3）","value":"86 億美元、年增 6%，約占營收 48%；含 Qlex 8.3 億"},{"item":"Gardasil（2026Q3）","value":"20 億美元、年增 14%（美國 +18% 含 CDC 採購，國際 +6%）；上半年年減 9%"},{"item":"Winrevair（2026Q3）","value":"6.94 億美元、年增 94%（含約 0.5 億進貨時點效益）"},{"item":"Welireg（2026Q3）","value":"3.07 億美元、年增 58%"},{"item":"Capvaxive／Enflonsia／Ohtuvayre（2026Q3）","value":"2.63 億（美國 −13%）／1.87 億／1.84 億美元"},{"item":"動物保健","value":"2026Q3 年增 3%；上半年 35.66 億美元、年增 10%"},{"item":"2027 年專利到期逆風","value":"Bridion、Januvia 家族、Adempas 合計超過 20 億美元（Q3 法說 CFO）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"Q2 調整後毛利率 81.1%、年減 1.1 個百分點；Q3 81.4%、小幅下降"},{"signal":"核心市占近 12 個月縮減","lit":null,"note":"事實表未涵蓋份額數據；Keytruda 仍成長但 Imfinzi 成長更快"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"未見證據"},{"signal":"EPS 年複合高於營收年複合 5 個百分點以上","lit":null,"note":"FY2025 基期口徑不一、FY2028 共識營收未涵蓋，無法判定"},{"signal":"FCF/NI 連 2 年低於 0.75","lit":false,"note":"FY2024 1.06、FY2025 0.68，只有 1 年"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"1.79%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"PD-1×VEGF 雙特異抗體頭對頭勝過 Keytruda；Gardasil 中國市場萎縮"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"Q2 資本支出 8.93 億美元、FCF 44.77 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"在美國增加製造投資；營收 2022–2025 年持續成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：股息與每年約 30 億美元回購穩定，但新藥接棒靠舉債併購，收購報酬尚未實現","reasoning":"FCF/NI：FY2022 1.01、FY2024 1.06、FY2025 0.68（FY2023 淨利僅 3.65 億美元，比值失真）。SBC 占營收 1.79%（2026Q2），年化約 12 億美元、約占市值 0.33%。現金去向：股息（殖利率 2.29%，換算約 84 億美元／年）、回購約 30 億美元（2026 年）、收購與授權（Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億，Cidara 金額未涵蓋）、資本支出（Q2 單季 8.93 億美元）。FY2025 FCF 123.6 億美元大致只夠付股息與回購，收購靠舉債，淨負債 467.7 億美元。收購報酬：多數為上市前資產、研發費用一次認列，報酬尚未實現。回購買入收益率以 FY2027 共識計約 6.2%，十年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_peer_mrk_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"2026 年收購 Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元，資產多未上市；2022→2025 營業利益只增加約 38 億美元，收購報酬尚未實現"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"買入收益率約 6.2%（FY2027 共識 9.14 ÷ 148.56）；十年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 單季 2.98 億美元、年化約 12 億，約占市值 0.33%／年，回購抵銷後為淨減少"}]},"governance":{"capital_returns":[{"item":"股息","value":"殖利率 2.29%，以市值 3,665 億美元換算約 84 億美元／年；管理層承諾逐步調升"},{"item":"回購","value":"2026 年約 30 億美元（Q2、Q3 法說），約占市值 0.8%"},{"item":"收購與授權（2026）","value":"Terns 約 67 億（申報總額 68 億，認列 57 億研發費用）、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元；Cidara 金額事實表未涵蓋"},{"item":"自由現金流","value":"FY2025 123.6 億美元、FY2024 181.0 億；2026Q2 單季 44.77 億"},{"item":"淨負債","value":"467.7 億美元（總債務 539.1 億、現金 71.4 億）"}],"sbc":{"pct_rev":1.79,"note":"2026Q2 單季 2.98 億美元"}}}},"q5_valuation":{"verdict":"現價要求 Keytruda 專利到期只是淺坑、新藥五年內接上逾 250 億美元的缺口，且市場續給 15 倍以上；我們只部分相信，價格偏貴","reasoning":"現價 148.56 美元＝FY2027 共識 9.14 美元的 16.25 倍、FY2028 共識 10.12 美元的 14.7 倍；EV 4,132.8 億美元，trailing EV/S 6.13 倍、P/S 5.44 倍，兩者都在可得四個年度端點的最高位。trailing 本益比 150 倍與 FY2026 前瞻 54.6 倍被收購研發費用扭曲，不可用。現價要求：專利到期只是淺坑、FY2028 起 EPS 維持兩位數美元並在 2030 年代回到成長，且市場願意繼續給 15 倍以上。我們只部分相信：Base 情境 FY2031 EPS 10.0 美元 × 14 倍約 140 美元，價格面五年 −5.8%，加股息後年化不到 2%。賣方 8 月初平均目標價約 134.56 美元，比現價低約 9%（ESMO 讀數前的舊數字），方向上支持不追。同業前瞻倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_dividend_yield_ttm","f_net_debt_m","f_ev_m","f_ma_state","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻一年本益比（FY2027 共識 9.14 美元）；FY2026 共識被收購研發費用壓低，trailing 150 倍與 FY2026 前瞻 54.6 倍皆不可用","tier":"大型專利藥廠","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，未涵蓋同業前瞻本益比，無法做倍數對照；終端倍數改以自身前瞻倍數與重新進場價位校準"},"fwd_pe":16.25,"peg":1.52,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 16.25 倍（FY2027）、14.7 倍（FY2028）；P/S 5.44 倍與 EV/S 6.13 倍在可得四個年度端點中最高，真五年分位事實表未涵蓋。PEG 1.52 以 FY2027→FY2028 共識成長 10.7% 計，若改用 Base 路徑約 2% 年成長則遠高於 2。短期（12 個月）以 FY2028E Base 9.5 美元 × 15 倍約 142.5 美元、−4.1%；中期（5 年）Base 140 美元、−5.8%，結論偏貴","upside_short_pct":-4.1,"upside_mid_pct":-5.8,"denominator_disputed":true,"denominator_note":"FY2026 共識 2.72 美元含收購研發一次性費用（Q2 法說 CFO 說 Terns 預付每股 2.31 美元，事實表註記為 2.43，口徑不一；另有 Cidara 與 SciBrunch 費用）。改用 FY2027 共識 9.14 美元當分母，但 CFO 2026-10-29 表示多數分析師尚未納入 2027 投資年訊息，FY2027 分母本身也有下修風險"}}},"q6_how_wrong":{"verdict":"最可能看錯在低估新藥接棒速度；反方向的錯則是低估 Keytruda 美國流失速度","reasoning":"偏空看錯：三期接連成功（TroFuse-005、INTerpath-001）、Winrevair 與 Lipfendra 放量快過預期、2027 年 Keytruda 權利金到期帶動毛利率上升，CFO 明言接近專利到期時盈餘會成長；若 FY2031 EPS 走到 12.6 美元、17 倍，價格約 214 美元。偏多看錯：Keytruda 美國留存率低於預期、Qlex 智財受挫、雙特異抗體取代骨幹，FY2031 EPS 7.4 美元、11 倍約 81 美元。最大回撤範圍 −35%～−55%：Base 路徑 FY2029 低點 8.9 美元 × 約 10.8 倍、Bear 路徑 FY2030 低點 7.1 美元 × 9.5 倍；事實表未涵蓋公司歷史最大回撤，無法用歷史校準。法說迴避：管理層在 Q2 法說與投資人日多次不給專利到期期間的 EPS 數字，也不透露與 FDA 的非比例風險討論。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_consensus_eps_fy2","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"Keytruda 專利到期前的換軌風險；衰退訊號亮 2 個（毛利率連 2 季年減、替代技術壓縮）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":9.14,"pe":16.25,"basis":"FY2027 共識 EPS 9.14 美元（前瞻約一年）；FY2026 共識 2.72 含收購研發一次性費用不可用；終端倍數同樣套在全年 EPS 上，與起點同口徑"},"eps":{"bull":[9.2,10.2,10.4,11.5,12.6],"base":[8.95,9.5,8.9,9.3,10.0],"bear":[8.6,8.7,7.6,7.1,7.4]},"pe":{"bull":17,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.29,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"max_dd":{"lo":-55,"hi":-35,"basis":"上緣 −35%：Base 路徑 FY2029E 低點 8.9 美元 × 約 10.8 倍約 96 美元（專利到期當年倍數壓縮）；下緣 −55%：Bear 路徑 FY2030E 低點 7.1 美元 × 9.5 倍約 67 美元；Bear 終點 7.4 × 11 約 81 美元（−45%）落在範圍內。事實表未涵蓋公司歷史最大回撤，無法用歷史校準","trigger_time":null},"basis":{"bull":"Qlex 美國轉換達 40%、Winrevair 與 Lipfendra 放量、sac-TMT 與 intismeran 2027–2028 年上市，專利到期只是淺坑；FY2031 EPS 12.6 美元、17 倍（回到中個位數以上成長的大藥廠）","base":"2027 年 EPS 略低於共識（8.95 對 9.14），2028 年 Medicare 議價、2029 年美國生物相似藥上市造成低點 8.9 美元，2031 年回到 10.0 美元；終端 14 倍（低成長、專利到期後的大藥廠）","bear":"Qlex 受挫或轉換不足、雙特異抗體壓縮 Keytruda、疫苗與政策逆風延續，FY2030 低點 7.1、FY2031 7.4 美元；終端 11 倍（無成長的老藥廠）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Keytruda 逾 250 億美元年營收的美國核心專利 2028 年到期、Medicare 議價價格 2028-01 生效；ivonescimab 已在肺癌頭對頭試驗勝過 Keytruda","assumption":"多頭假設 Qlex 轉換加上新藥，能讓營收只出現淺坑","consequence":"若美國 Keytruda 在 2029–2030 年流失過半、Qlex 又被擋，FY2031 EPS 約 7.4 美元、11 倍約 81 美元（−45%）；低谷年倍數壓到 9.5 倍時可見 67 美元","ruling":"採納，列為 Bear 30%。與 Single Thing 部分重疊：美國 Qlex 裁決只是其中一條失敗路徑，雙特異抗體取代與 Medicare 議價不需要任何裁決也會發生，所以保留為獨立反證","watch":"Keytruda 家族單季年增率、Qlex 營收與美國訴訟、全球 PD-1×VEGF 三期讀數","evidence_refs":["supply_demand_durability#2","end_markets#5","substitute_technology#0"],"fact_refs":["f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"接棒靠舉債併購與授權：2026 年 Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元，淨負債 467.7 億美元；CFO 預告 2027 年營業費用中高個位數成長、利息與稅率上升。社會容忍度偏低：參議員質詢 Keytruda 專利策略，IRA 議價與 MFN 直售平價方案壓定價","assumption":"營收補回來，利潤率與每股盈餘就會跟著回來","consequence":"營收守住但營業利益率從 FY2025 的 34% 往下走、每股盈餘成長落後營收；收購研發費用年年出現，調整後 EPS 高估真實盈餘","ruling":"採納：Base 情境 EPS 比共識低 2–6%（FY2027 8.95 對 9.14、FY2028 9.5 對 10.12）","watch":"調整後營業費用年增率對營收年增率；每年收購研發費用；淨負債變化","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#3"],"fact_refs":["f_net_debt_m","f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"26 週上漲 33.08%；P/S 5.44 倍、EV/S 6.13 倍在可得四個年度端點中都是最高；FY2027 前瞻本益比 16.25 倍；8 月初賣方平均目標價約 134.56 美元，低於現價約 9%；FY2027／FY2028 共識近期各下修 0.98%／0.78%","assumption":"三期成功等於商業成功，且 2027 共識不再下修","consequence":"即使論點成立，Base 五年年化報酬不到 2%。共識小幅下修時 Bear 錨不依賴共識、暫時平穩；但若 FY2027 共識持續下修，正向不對稱的數字不能當進場依據","ruling":"採納：不追，等股價落到 FY2027 共識 13 倍以下並看到放量","watch":"FY2027 共識 EPS 月度變化；股價 ÷ FY2027 共識","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_ps_current","f_ev_s_current","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 148.69 → 本次 148.56（-0.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=148.69","side_b":"本次 price_at_dd=148.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 148.69 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 148.69 美元：Bull 價 198.4、Bear 價 83.6，五年期望值 −8.9%，基準年化 −1.0%，不對稱比 0.5","side_b":"本次情境、股價仍用 148.69 美元：Bull 價 214.2、Bear 價 81.4，五年期望值 −7.7%，基準年化 −1.2%，不對稱比 0.65","ruling":"先換情境、股價不動：五年期望值多 1.2 個百分點，基準年化少 0.2 個百分點。不對稱比由 0.5 變為 0.65。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 148.69 美元：五年期望值 −7.7%，基準年化 −1.2%，不對稱比 0.65","side_b":"本次情境、股價 148.56 美元：五年期望值 −7.6%，基準年化 −1.2%，不對稱比 0.65","ruling":"再換股價、情境不動：起點價下跌 0.1%，五年期望值多 0.1 個百分點，基準年化多 0.0 個百分點，不對稱比由 0.65 升到 0.65。合計五年期望值比前份多 1.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層淺坑說對上 2027 投資年與專利到期規模","cause":null,"side_a":"CEO（2026-08-04）稱專利到期期間是「小山不是懸崖」、淺幅下滑後快速回到成長；CFO（2026-10-29）稱接近專利到期時盈餘會成長、營收淺坑後很快回升","side_b":"同一場 CFO 也說 2027 年營收只溫和成長、超過 20 億美元學名藥逆風、營業費用中高個位數成長，多數分析師尚未納入；Keytruda 逾 250 億美元年營收 2028 年起受專利與 Medicare 議價夾擊；FY2027／FY2028 共識近期已小幅下修","ruling":"可調和（程度差異）：方向上同意會回到成長，但幅度與時點採較保守的 Base：FY2027 EPS 8.95 美元（共識 9.14）、FY2029 低點 8.9 美元","evidence_level":"管理層陳述＋共識快照（中）","settle_metric":"2027-02 財報給的 2027 年 EPS 財測中點對 9.14 美元","if_then":["若 2027 年 EPS 財測中點 ≥9.1 美元且營業費用成長 ≤5% → Base FY2027 上修到 9.1，重跑情境樹","若財測中點 < 8.8 美元 → 維持不追，Bear 機率上調到 35%","反向條件：若財測高於共識但股價同步漲到 FY2027 的 17 倍以上 → 仍不追"],"evidence_refs":["end_markets#5"]},{"axis":"Q3 上修財測的品質","cause":null,"side_a":"2026 年 EPS 財測由 2.66–2.76 上修到 2.77–2.82 美元，高於當時共識 2.65","side_b":"Q3 營收含約 5.5 億美元美國進貨時點效益：Keytruda 2 億、Winrevair 0.5 億於 Q4 回吐，疫苗 3 億中 2.5 億在 2027 年回吐；全年稅率由 35–36% 降到 32–33% 也有貢獻","ruling":"可調和：上修屬實，但部分來自時點與稅率，不改變 2027 年判斷","evidence_level":"法說與新聞稿（高）","settle_metric":"2026Q4 Keytruda 家族營收扣除 2 億回吐後的年增率","if_then":["若扣除回吐後年增 ≥4% → H2 路徑不變","若 < 2% → R1 升級，Base FY2027 EPS 下修到 8.8 美元"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"ESMO 兩個三期正向（TroFuse-005 降低進展或死亡風險 41%、INTerpath-001 降低復發或死亡風險 42%），sac-TMT PDUFA 2027-06-15；Winrevair 單季 6.94 億美元、年增 94%；CEO 說 700 億美元中期目標將上修；FY2028 共識本益比約 14.7 倍、股息殖利率 2.29%","side_b":"這些成功多數 2028 年後才貢獻，且部分已在 26 週 33% 漲幅中；Base 五年年化不到 2%；Qlex 歐洲禁制令與美國訴訟、Lipfendra 醫保覆蓋要到 2027–2028 年","ruling":"不採納買進。約束條件有兩個：價格（Base 年化不到 2%）與接棒證據（新品組合尚未到 25 億美元），三項重新進場條件需同時成立","evidence_level":"公司發布＋法說（高）","settle_metric":"股價 ÷ FY2027 共識 EPS；新品組合單季營收","if_then":["若股價 ≤119 美元但新品組合未達 25 億 → 不建倉，等放量；分批反買只在重跑研究通過後","若新品組合 ≥25 億且 Qlex ≥12 億但股價仍 ≥140 美元 → 不追（價格先走）"],"evidence_refs":["major_events#2","clinical_fda#0"]},{"axis":"Qlex 智財：管理層說無影響，對上禁制令與國會質詢","cause":null,"side_a":"CEO：有自由實施的智財，荷蘭禁制令只是聽證前的暫時措施；歐洲 6 國停供屬小量市場（Q3 法說）","side_b":"禁制令已生效；分析師直接追問美國是否有風險；參議員 Hassan 質詢 Keytruda 以劑型轉換延遲低價競爭","ruling":"不可裁決至荷蘭聽證結果出爐（日期事實表未涵蓋）；維持把美國 Qlex 裁決設為唯一致命點","evidence_level":"法說陳述（中）","settle_metric":"荷蘭聽證判決；美國是否出現同類禁制令","if_then":["若荷蘭聽證推翻禁制令 → 唯一致命點機率由約 10% 下修到 5%","若美國出現禁制令申請或不利裁決 → Bear 機率上調到 40%，取消重跑研究條件 12 個月"],"evidence_refs":["regulatory_antitrust#0","substitute_technology#3"]},{"axis":"前份至今股價幾乎不動，估值結論、裁決與機率不因價格改變","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-09-29：估值偏貴、迴避、不持有；Bull 20%、Bear 30%","side_b":"本次：股價 148.69→148.56 美元（−0.1%）；估值仍偏貴（FY2027 前瞻 16.25 倍）；機率維持 20／50／30","ruling":"價格沒有帶來新的安全邊際；三期正向讀數（加分）與 2027 投資年訊息（減分）相互抵銷，機率不動","evidence_level":"價格與共識快照（高）","settle_metric":"股價 ÷ FY2027 共識 EPS","if_then":["若股價 ÷ FY2027 共識 ≤13 倍且放量條件成立 → 重跑研究","若股價續漲到 17 倍以上而放量未到 → 不追"]},{"axis":"Q3 財報與 ESMO 讀數檢視後，護城河方向、陷阱風險、五年後跑道與訊號維持","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","signal"],"side_a":"前份：護城河縮減、陷阱風險中、五年後跑道中、訊號 C","side_b":"本次維持同樣四個結論。加分：TroFuse-005 降低進展或死亡風險 41%、INTerpath-001 降低復發或死亡風險 42%、CEO 稱 700 億美元目標將上修、Winrevair 年增 94%。減分：Qlex 在歐洲 6 國遭禁制令停供、2027 年超過 20 億美元學名藥逆風、德國政策與美國以外價格逆風、I-DXd 撤回加速核准申請","ruling":"正負相抵。700 億美元的 2030 年代中期目標相對 2026 年財測中點 670.5 億只是持平，第二曲線不足以把跑道升為寬；定價權仍在收縮，護城河方向不變","evidence_level":"公司法說與投資人日（高）","settle_metric":"新品組合單季營收、Keytruda 家族年增率","evidence_refs":["clinical_fda#0","major_events#2"]},{"axis":"最大回撤改用範圍推導；型態與循環位置維持","cause":"方法變動","prior_field":["max_dd_pct","archetype","cycle_position"],"side_a":"前份最大回撤 −48%（單點）；型態品質複利成長；循環位置未設","side_b":"本次最大回撤 −35%～−55%，由 Base 與 Bear 路徑低谷年 EPS × 低谷倍數推出；型態維持品質複利成長（副型態轉機／特殊情境）；非循環股，循環位置不適用","ruling":"範圍比單點更能反映專利到期當年的倍數壓縮；型態不變，因為毛利率、現金創造與股息紀錄仍是品質股的樣子，換軌風險放在副型態與反證處理"},{"axis":"重新進場研究門檻：價格條件改為倍數錨，並明列新品組合","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","side_b":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","ruling":"固定 120 美元改為 FY2027 共識 13 倍：CFO 2026-10-29 說多數分析師尚未納入 2027 投資年訊息，共識下修時固定價位等於放寬門檻；前份 120 美元換算 12.6 倍與目前共識 9.14 美元換算的 13.1 倍不一致，改以倍數明定。新品組合明列為 Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra，2026Q3 約 21.6 億美元（不含未揭露的 Lipfendra）。前份三項皆未成立","settle_metric":"股價 ÷ FY2027 共識 EPS；新品組合單季營收"},{"axis":"Single Thing 首次設定","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"本次 Single Thing：美國法院或主管機關對 Keytruda Qlex 的透明質酸酶智財作出不利 Merck 的裁決或禁制令，Qlex 無法在美國續售","ruling":"Q3 法說揭露荷蘭禁制令已讓歐洲 6 國停供，分析師追問美國風險；Qlex 是 2028–2029 年美國防線的主要工具，屬可監測的單一二元事件","evidence_refs":["substitute_technology#3"]},{"axis":"清倉／減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設門檻（null）","side_b":"本次四條：Keytruda 家族連 2 季負成長、Qlex 2027Q4 < 10 億美元或美國禁制令、FY2027 共識 EPS < 8.5 美元、新品組合 2027Q4 < 22 億美元","ruling":"任一觸發即停止重跑研究；若屆時已持有則減碼一半，兩條同時觸發則清倉。前份只有重新進場條件，沒有論點失效的出場線，本次補上"}],"triggers":[{"n":1,"text":"三項重新進場條件同時成立","type":"估值rearm","maps_to":"H1/H2","metric":"Qlex 單季營收；新品組合單季營收；股價 ÷ FY2027 共識 EPS","threshold":"≥12 億美元；≥25 億美元；≤13 倍（約 119 美元），三項同時","action":"重跑研究，通過後才考慮首筆建倉","source_freq":"季度新聞稿＋每日收盤＋月度共識快照","date":"2027-02 起逐季"},{"n":2,"text":"美國 Qlex 智財不利裁決或禁制令","type":"Single Thing","maps_to":"Single Thing","metric":"美國 Qlex 透明質酸酶專利訴訟與禁制令","threshold":"任何不利裁決或禁制令","action":"Bear 機率上調到 40%，取消重跑研究條件 12 個月","source_freq":"8-K、10-Q 訴訟附註、法說；不定期","date":"審理時程事實表未涵蓋","evidence_refs":["substitute_technology#3"]},{"n":3,"text":"2027 年 EPS 財測低於共識","type":"假設驗證","maps_to":"R1","metric":"2027 年調整後 EPS 財測中點","threshold":"< 8.8 美元","action":"Base 路徑下修、Bear 機率上調到 35%，維持不追","source_freq":"Q4 FY2026 財報；一次","date":"2027-02"},{"n":4,"text":"Keytruda 家族轉為負成長","type":"風險","maps_to":"R2","metric":"Keytruda 家族單季營收年增率（扣除進貨時點）","threshold":"連 2 季 < 0%","action":"停止重跑研究；若屆時已持有則減碼一半","source_freq":"季報；每季","date":"2027Q1–2028Q4","evidence_refs":["supply_demand_durability#2","end_markets#5"]},{"n":5,"text":"雙特異抗體在全球三期勝過 Keytruda","type":"風險","maps_to":"R3","metric":"PD-1×VEGF 對 Keytruda 的全球三期頭對頭整體存活","threshold":"統計顯著勝出","action":"威脅升為架構替代，Bear 機率上調到 40%，重跑研究","source_freq":"公司與 Summit／Akeso 公告、ASCO／ESMO；不定期","date":"讀數時程事實表未涵蓋","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"n":6,"text":"Gardasil 國際需求續弱","type":"風險","maps_to":"R4","metric":"Gardasil 美國以外單季營收年增率","threshold":"連 2 季 < −10%","action":"Base 疫苗營收再下修 10%，Bear 機率加 5 個百分點","source_freq":"季報；每季","date":"逐季","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1","end_markets#1"]},{"n":7,"text":"政策壓縮毛利率","type":"風險","maps_to":"R5","metric":"全年調整後毛利率","threshold":"< 80%（2026 財測約 81%，2027 預期上升）","action":"Base 終端倍數由 14 降到 13 倍","source_freq":"年度財測與季報","date":"2027-02 起","evidence_refs":["regulatory_antitrust#3","reg_tariff_export#1"]},{"n":8,"text":"中國來源管線受政策限制","type":"風險","maps_to":"R6","metric":"美國對中國臨床數據或授權交易的限制","threshold":"立法或行政命令通過","action":"sac-TMT 與 MK-2010 的上行貢獻歸零，Bull 機率降到 15%","source_freq":"國會與行政部門公告；不定期","date":"不定期","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":9,"text":"訴訟與調查出現重大金額","type":"風險","maps_to":"R7","metric":"DOJ 民事調查、RotaTeq 反壟斷、Cronin 證券訴訟的和解或裁決金額","threshold":"任一 > 10 億美元，或證券訴訟進入證據開示","action":"Bear 情境扣除一次性金額，Bear 機率加 5 個百分點","source_freq":"10-Q／10-K 訴訟附註；每季","date":"逐季","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"n":10,"text":"sac-TMT 子宮內膜癌 PDUFA","type":"複審日期","maps_to":"H3","metric":"FDA 核准與否","threshold":"核准","action":"核准不改變不追；未核准則 Bull 機率降到 15%","source_freq":"FDA／公司公告；一次","date":"2027-06-15"},{"n":11,"text":"Q4 FY2026 財報與 2027 年財測","type":"複審日期","maps_to":"H1/H2/R1","metric":"重新進場三項條件與 2027 年財測","threshold":"見第 1、3 條","action":"逐項對帳後重寫判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"Keytruda 家族單季營收年增率（扣除進貨時點效益）","bear_threshold":"連 2 季 < 0%（2028 年 Medicare 議價生效前）","window":"2027Q1–2027Q4","source":"公司季度新聞稿與法說","last_status":"ok"},{"metric":"Qlex 單季營收","bear_threshold":"2027Q4 < 10 億美元，或美國出現禁制令","window":"至 2027Q4","source":"公司季度新聞稿；8-K 訴訟公告","last_status":"ok"},{"metric":"FY2027 共識調整後 EPS","bear_threshold":"< 8.5 美元","window":"2026-11 至 2027-08","source":"Koyfin 月度共識快照","last_status":"ok"},{"metric":"新品組合單季營收（Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra）","bear_threshold":"2027Q4 < 22 億美元（較 2026Q3 約 21.6 億無成長）","window":"至 2027Q4","source":"公司季度新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#0","reason":"證據是 2022 年底的 10-K 數據、距今近四年，且原文自己註明屬產業結構性集中、非新增惡化；沒有附任何呆帳或信用事件，無法連到本次論點"},{"ref":"major_events#3","reason":"來源是第三方召回清單的搜尋摘要，Class II、單一劑型套組（Emend 口服懸液），未附任何營收金額或後續處分"},{"ref":"product_recall_warning#0","reason":"與 Emend 召回為同一事件的重複收錄，同樣來自第三方召回清單摘要，原文寫明未見 2026 年警告信，未附營收衝擊數字"}],"action_conditions":{"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","exec_line":"不持有、不追；三項條件同時成立前不建倉，成立後先重跑研究，通過才考慮首筆建倉","holding_cap":"0%（重跑研究通過前）"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"FY2027 共識尚未完全反映 CFO 2026-10-29 說的 2027 投資年（營業費用中高個位數成長、超過 20 億美元學名藥逆風），且 26 週上漲 33% 已把 sac-TMT 與 intismeran 的三期成功當成商業成功定價","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"迴避","prior_role":"不持有"},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='迴避', 矩陣機械輸出='迴避'"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"新藥組合在 Keytruda 美國專利到期前放量到足以接棒：Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra 合計單季營收由 2026Q3 約 21.6 億美元（不含未揭露的 Lipfendra）升到 2027Q4 ≥25 億美元","2y":"2027Q4 新品組合單季 ≥25 億美元（扣除進貨時點效益）","5y":null,"10y":null,"threshold":"2027Q4 單季 ≥25 億美元","source":"公司季度新聞稿與法說的產品營收","drift_rule":"以四季合計對比路徑：連 2 季落後 ≥5% 視為削弱，連 3 季落後 ≥10% 視為反轉"},{"id":"H2","text":"Qlex 皮下劑型守住美國轉換：管理層目標 2027 年底美國採用 30–40%（Q3 法說 Jannie Oosthuizen），以 Qlex 單季 ≥12 億美元為代理門檻（美國占比事實表未涵蓋），且美國無禁制令","2y":"2027Q4 Qlex 單季 ≥12 億美元；美國無不利裁決","5y":null,"10y":null,"threshold":"2027Q4 Qlex 單季 ≥12 億美元","source":"季度新聞稿、法說、8-K 與 10-Q 訴訟附註","drift_rule":"連 2 季低於直線路徑（8.3 億→12 億）≥5% 視為削弱，連 3 季 ≥10% 視為反轉；美國出現禁制令即反轉"},{"id":"H3","text":"專利到期只是淺坑：FY2029 全年營收不低於 2026 年財測中點 670.5 億美元的 95%（約 637 億），FY2031 調整後 EPS 回到 ≥10 美元","2y":null,"5y":"FY2029 營收 ≥637 億美元；FY2031 EPS ≥10 美元","10y":"2030 年代中期營收 ≥700 億美元（CEO 2026-10-29 稱將上修此目標）","threshold":"FY2029 營收 ≥637 億美元","source":"年報 10-K 與年度財測；Koyfin 月度共識","drift_rule":"TTM 營收連 4 季落後路徑 ≥5% 視為削弱、連 6 季 ≥10% 視為反轉；10 年目標跨 2 個年度落後削弱、跨 3 個年度反轉"}],"R":[{"id":"R1","text":"2027 投資年讓 EPS 低於共識：營業費用中高個位數成長、超過 20 億美元學名藥逆風、利息與稅率上升（Q3 法說 CFO），且 CFO 說多數分析師尚未納入","h_ref":"H3","clock":"⚡","threshold":"FY2027 共識 EPS 在 2027-02 財報後降到 8.7 美元以下（較 9.14 低約 5%）","evidence_refs":[]},{"id":"R2","text":"Keytruda 防線被突破：美國核心專利 2028 年 12 月到期、Medicare 議價價格 2028-01 生效，生物相似藥（Cipla／Qilu QL2107）卡位，Qlex 在歐洲 6 國遭禁制令，參議員質詢劑型轉換策略","h_ref":"H2","clock":"🔥","threshold":"Keytruda 家族單季年增率連 2 季 < 0%（2028 年前），或美國出現 Qlex 不利裁決","evidence_refs":["supply_demand_durability#2","end_markets#5","substitute_technology#3","regulatory_antitrust#0"]},{"id":"R3","text":"PD-1×VEGF 雙特異抗體取代 pembrolizumab 成為免疫治療骨幹：ivonescimab 在肺癌頭對頭試驗擊敗 Keytruda，Crescent CR-001 2026 年進臨床；Merck 自有 MK-2010 的三期 2027 上半年才啟動","h_ref":"H3","clock":"🐢","threshold":"任一 PD-1×VEGF 在全球（非僅中國）三期頭對頭勝過 Keytruda 的整體存活","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"id":"R4","text":"疫苗需求結構性走弱：Gardasil 中國停貨、本土競品十分之一價格、日本需求下滑，美國疫苗猶豫（Capvaxive 美國 −13%）；Q3 Gardasil +14% 含 CDC 採購與 3 億美元時點效益，其中 2.5 億在 2027 年回吐","h_ref":"H3","clock":"🔥","threshold":"Gardasil 美國以外單季營收年增率連 2 季 < −10%","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","end_markets#1","end_markets#2"]},{"id":"R5","text":"美國藥價與貿易政策壓縮定價：IRA 議價（Januvia／Janumet 已入選，Merck 提告違憲）、MFN 協議與直售病人平價方案、Section 232 專利藥最高 100% 關稅（Merck 以美國投資換三年延後）、德國政策","h_ref":"H3","clock":"🔥","threshold":"全年調整後毛利率 < 80%（2026 財測約 81%），或公司揭露政策造成的年度營收衝擊 > 20 億美元","evidence_refs":["regulatory_antitrust#3","reg_tariff_export#1"]},{"id":"R6","text":"中國來源管線的地緣風險：sac-TMT（Kelun）與 MK-2010（LaNova）皆授權自中國，眾議院中國特別委員會調查 Merck 在中國的 224 項臨床研究（至少 31 項在新疆、40 項在解放軍附屬醫院），CEO 公開警告限制美中交易的後果","h_ref":"H3","clock":"🐢","threshold":"美國立法或行政命令限制使用中國臨床數據申報，或限制中國授權資產","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R7","text":"訴訟與調查：DOJ 依《虛假申報法》調查 Steglatro／Januvia 的 Medicaid 回扣價格申報（2024-06 起）、巴爾的摩市 RotaTeq 反壟斷集體訴訟、Cronin 證券集體訴訟（Gardasil 中國需求陳述）及兩件衍生訴訟","h_ref":null,"clock":"🐢","threshold":"任一案揭露和解或罰款 > 10 億美元，或證券訴訟駁回動議被否決、進入證據開示","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"美國法院或主管機關對 Keytruda Qlex 的透明質酸酶智財作出不利 Merck 的裁決或禁制令，Qlex 無法在美國續售","why_fatal":"Keytruda 美國專利到期後的留存率是情境樹最大的敏感項，Qlex 是其中唯一可二元判定的節點：它是 2028 年 12 月核心專利到期後不受 IV 生物相似藥直接替代的劑型，管理層目標 2027 年底美國轉換 30–40%。Qlex 若被擋，這部分營收在 2029 年也暴露在生物相似藥下，淺坑假設的主要支柱消失","if_happens":"Base 改走 Bear：FY2031 EPS 由 10.0 降向 7.4 美元，Bear 機率上調到 40%，取消重跑研究條件 12 個月","how_monitor":"荷蘭聽證判決（歐洲 6 國停供，日期事實表未涵蓋）作為先行指標；公司 8-K 與 10-Q 訴訟附註；Qlex 單季營收","probability":"12–24 個月約 10%：管理層稱有自由實施的智財、美國目前無禁制令；但荷蘭已核發暫時禁制令，故不低於 5%"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.25,"peg_fy2":1.52,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":7.28,"FY2026E":2.72,"FY2027E":9.14,"FY2028E":10.12},"fy_end_month":12,"eps_basis":"共識為 Koyfin 調整後 EPS（FY2026E 2.72 含收購研發一次性費用）；FY2025A 用事實表唯一可得的 GAAP 稀釋 EPS 7.28，與調整後口徑不同，三年年複合約 11.6% 因此高估真實成長"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 年財測（首次量化投資年）","impact":"高","watch":"EPS 財測中點對共識 9.14 美元、營業費用成長率"},{"date":"2027-06-15","date_precision":null,"type":"regulatory","event":"sac-TMT 子宮內膜癌 PDUFA","impact":"中","watch":"核准與標示範圍"},{"date":"2028-01","date_precision":"month","type":"regulatory","event":"Keytruda Medicare 議價價格生效","impact":"高","watch":"議價折扣幅度與 2028 年財測"},{"date":"2028-12","date_precision":"month","type":"other","event":"Keytruda 美國核心專利到期","impact":"高","watch":"生物相似藥上市時程與 Qlex 轉換率"}]}
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
