你是 DD 管線 v20 的判斷層閘（gate），標的 EHC（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap_net_operating_reven`（q1_business）｜營收（GAAP net operating revenue）＝1609.5 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi1_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代替）＝346.6 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益（營收減總營業費用，自算；新聞稿未直接列示）＝288.0 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi5_adjusted_eps`（q1_business）｜Adjusted EPS＝1.52 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi6_2026`（q1_business）｜2026 全年指引（上調）＝營收 6,450–6,500M；Adj EBITDA 1,395–1,415M；Adj EPS 6.23–6.37 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi7_discharges`（q1_business）｜出院人次（discharges）＝69605 人次｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_peer_ehc_operating_margin_pct`（q2_moat）｜EHC 營業利益率＝18.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EHC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ehc_gross_margin_pct`（q2_moat）｜EHC 毛利率＝95.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EHC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_ehc_fcf_margin_pct`（q2_moat）｜EHC FCF 利潤率＝6.97 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EHC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hca_operating_margin_pct`（q2_moat）｜HCA 營業利益率＝15.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HCA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hca_fcf_margin_pct`（q2_moat）｜HCA FCF 利潤率＝7.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HCA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_uhs_operating_margin_pct`（q2_moat）｜UHS 營業利益率＝11.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UHS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_uhs_fcf_margin_pct`（q2_moat）｜UHS FCF 利潤率＝4.98 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UHS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_thc_operating_margin_pct`（q2_moat）｜THC 營業利益率＝22.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.THC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_thc_fcf_margin_pct`（q2_moat）｜THC FCF 利潤率＝14.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.THC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝6.27 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.81 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝7.42 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.5 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 6.0 → 6.27（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝2.62 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（6.11 → 6.27）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6475.16 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7017.86 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝98.3 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_adjusted_fcf`（q4_capital）｜自由現金流（Adjusted FCF）＝263.4 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝5.2 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝2727.2 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 2803.4、現金 76.2（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.571 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝16163.83 USD m｜期間與口徑：2026-11-03／市值 13436.63 ＋ 淨負債 2727.2｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝136.69 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.8 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 6.27，分子＝快照價 136.69｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.87 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝92.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝92.1 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.12 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.55 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝28.64 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 137.08 / W52 110.36 / W104 109.65 / W250 83.37 / W250 13週斜率 1.6%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝110.36 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝109.65 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝1.6 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：急性醫院系統可能擴張復健服務；2023 年南卡羅來納廢除 IRF 的 CON，CON 弱化可能提高競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：decision_inputs.bear、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：北卡羅來納州廢除 IRF certificate-of-need，據稱自 2029 年起可支撐每年 6–10 家新設施（潛在新進者供給）
  - 來源：Q2 2026 earnings coverage (MarketBeat / Simply Wall St)（as_of 2026-08-08）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：有分析敘事指出價值導向照護與門診／居家復健轉移可能長期壓抑住院量
  - 來源：Simply Wall St EHC narrative（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：FTC 與 DOJ 近年積極挑戰併購，持續積極執法會增加收購的時間與費用並可能降低成交可能性（對併購／新設醫院的一般性風險，非針對 EHC 的調查）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：文獻指出居家復健（HBR）是傳統住院復健的替代方案（2020 髖骨骨折比較研究，非 Medicare Advantage 情境）。
  - 來源：Frontiers in Medicine 2020 (frontiersin.org) 居家 vs 住院復健（as_of 2020-01-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：醫院協會致 CMS 信函：2022 年 Medicare Advantage 的 IRF 使用率僅 0.4%，傳統 Medicare 為 1.16%。
  - 來源：California Hospital Association letter to CMS re rehabilitation hospitals and MA network standards（as_of 2024-10-01）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：AJMC：高強度居家復健模式（Medicare ACO）在低至中度複雜度病患中功能結果較佳、成本較低；現行支付以地點而非強度計價，偏向住院復健。
  - 來源：AJMC, High-Intensity Home-Based Rehabilitation in a Medicare ACO（as_of 2025-01-08）｜affects：moat_trend、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2025-07 起多家原告律所公告調查 EHC 可能違反證券法；Rosen 網頁載有證券集體訴訟起訴書，涵蓋 2022-02-26 至 2025-07-15 購入證券者，被告含 CEO Tarr 與 CFO。搜尋摘要稱 2025-07-15 股價跌 10.4% 收 107.28 美元。法院、案號、現況未查到。
  - 來源：Rosen Law Firm｜Encompass Health complaint PDF；Business Wire 律所公告 2025-07-17（as_of 2025-08-01）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Rosen 載有證券集體訴訟起訴書（Exchange Act 10(b)/20(a)），被告含 EHC、CEO Tarr 與 CFO，類別期間 2022-02-26 至 2025-07-15；多家律所於 2025-07 至 09 公告調查。法院、案號與現況未查到。
  - 來源：Rosen Law Firm｜Encompass Health complaint PDF（as_of 2025-08-01）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：FY2025 10-K 稱公司在日常業務中涉及各類訴訟，部分求准許為集體或集體訴訟，並可能有未公開的 qui tam 案。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-26）｜affects：thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":236.5,"bear_5y_price":87.1,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":23.5,"ev5y_pct":15.5,"irr_base_pct":4.3,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":6.27,"pe":21.8,"basis":"FY2026E共識調整後EPS（Koyfin 2026-10-31）；終端倍數同樣以前瞻一年EPS為分母"},"eps":{"bull":[7.05,7.85,8.75,9.7,10.75],"base":[6.81,7.42,8.05,8.7,9.38],"bear":[6.4,6.3,6.4,6.55,6.7]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.571,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EHC_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Douglas Coltharp｜guidance：CFO 公布 2026 全年調升後的 EBITDA 與 EPS 財測區間（原話："adjusted earnings per share of $6.02 to $6.25."）
- 2026-08-06｜Douglas Coltharp｜guidance：Q4 Medicare 定價假設反映 7/30 公布的 IRF final rule（原話："reflects the IRF final rule released on July 30."）
- 2026-08-06｜Douglas Coltharp｜guidance：全年每 FTE SWB 成長預期上修為 3.5% 至 4%（原話："year 2026 SWB per FTE growth is 3.5% to 4%"）
- 2026-08-06｜Douglas Coltharp｜guidance：淨 provider tax 對 2026 EBITDA 的貢獻預期由約 2,100 萬美元下修為約 1,000 萬（原話："we now expect the net benefit to adjusted EBITDA in 2026"）
- 2026-08-06｜Douglas Coltharp｜guidance：全年開辦前與爬坡成本預期維持 1,800 萬至 2,200 萬美元（原話："ramp-up costs of $18 million to $22 million"）
- 2026-08-06｜Douglas Coltharp｜guidance：回應下半年上修財測的來源：定價（敏銳度）上行不確定（原話："There's no certainty that, that continues"）
- 2026-08-06｜Douglas Coltharp｜guidance：EPS 財測僅反映年初至今已執行的庫藏股（原話："The EPS guidance change reflects only the share repurchases"）
- 2026-08-06｜Douglas Coltharp｜guidance：SWB 上調假設僅限今年下半年趨勢（原話："it is an assumption for this year only"）
- 2026-08-06｜Mark Tarr｜guidance：CMS 2027 IRF final rule 對 Medicare 每次出院淨收入的估計影響（原話："approximately 2.3% increase in net revenue per discharge"）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 營收成長 9.6% 的拆解：出院量成長 5.6%（原話："The increase was comprised of 5.6% discharge growth"）
- 2026-08-06｜Douglas Coltharp｜margin：每次出院淨收入成長歸因於病患敏銳度提高（原話："growth was driven by higher patient acuity."）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 調整後 EBITDA 數字，並說明吸收了 provider tax 年減（原話："Our Q2 adjusted EBITDA increased 9.2% to $348 million"）
- 2026-08-06｜Douglas Coltharp｜margin：壞帳費用 Q2 為 2.3%，管理層稱符合預期（原話："in Q2 was 2.3%, in line with our expectations"）
- 2026-08-06｜Douglas Coltharp｜margin：合約勞工 FTE 占比 1.1%，較去年同期改善 20 bp（原話："was 1.1%, an improvement of 20 basis points from Q2 '25."）
- 2026-08-06｜Douglas Coltharp｜margin：EPOB 改善來源：較高入住率與 career ladder 的附帶效益（原話："we did see some further benefits in EPOB"）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 系統入住率及年增幅（原話："Q2 occupancy of 77.4% was up 290 basis points over Q2 '25."）
- 2026-08-06｜Douglas Coltharp｜margin：持有 CRRN 認證護理師的薪資溢價（原話："It's about 9% over their peers who do not have"）
- 2026-08-06｜Douglas Coltharp｜margin：CFO 稱溢價勞工降幅已進入邊際遞減（原話："Q2 marked our 11th consecutive quarter where we had a"）
- 2026-08-06｜Patrick Tuer｜margin：COO 表示溢價勞工還有空間但幅度較小（原話："There's some diminishing returns on this"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：Q2 庫藏股回購股數（原話："repurchased approximately 704,000 shares of our common stock"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：發行 5.875% 2034 到期票據並贖回 2028 到期舊票據（原話："we issued $500 million of 5.875% Senior Notes due 2034"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：季末淨槓桿比率（原話："Our net leverage at quarter end was 1.9x."）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：季度股利調升至每股 0.21 美元（原話："quarterly dividend next payable in October to $0.21"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：管理層稱資本配置框架不變，是「and」而非「or」（原話："we're an and story, not an or story"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：CapEx 約占營收 15%，管理層稱可能是高點（原話："probably represents close to a high watermark."）
- 2026-08-06｜Patrick Tuer｜capital_allocation：開始評估加床的入住率門檻由 80-85% 降到 70-75%（原話："lowered that threshold to 70% to 75%"）
- 2026-08-06｜Douglas Coltharp｜commitment：維持每年 6 至 10 家新院目標，期望北卡將其推向高端（原話："we're going to stay with the 6 to 10 range"）
- 2026-08-06｜Douglas Coltharp｜commitment：北卡將自 2029 年起把新院數推向 6-10 區間高端（原話："it would drive us probably beginning in 2029"）
- 2026-08-06｜Mark Tarr｜commitment：北卡下一家新院預計開業時間（原話："our next hospital opening in North Carolina to occur"）
- 2026-08-06｜Mark Tarr｜commitment：下半年計畫開 5 家新院、250 床（原話："we intend to open 5 more hospitals with a total of 250 beds"）
- 2026-08-06｜Mark Tarr｜commitment：2026 年後已宣布的新院管線規模（原話："currently consists of 13 hospitals with 606 beds"）
- 2026-08-06｜Douglas Coltharp｜commitment：小型院計畫明年至少開一家，2028 年起每年近五家（原話："the intent to get at least one open next year"）
- 2026-08-06｜Patrick Tuer｜commitment：admit-and-appeal 預計年底前評估是否全面推廣（原話："we'll be in a position to evaluate for a full"）
- 2026-08-06｜Patrick Tuer｜commitment：管理層表示不願承諾敏銳度會持續（原話："it'd be prudent for us to back us into a corner"）
- 2026-08-06｜Douglas Coltharp｜commitment：對 2027 年 SWB 每 FTE 增幅尚不給水準（原話："we're not ready to call a level on it"）
- 2026-08-06｜Douglas Coltharp｜competition：管理層稱高敏銳度病患形成競爭護城河（原話："there's a bit of a competitive moat around that"）
- 2026-08-06｜Douglas Coltharp｜competition：北卡進入策略強調先行者優勢（原話："we felt that first-mover advantage was"）
- 2026-08-06｜Mark Tarr｜competition：北卡將以自有與合資混合方式進入（原話："you could count on a mixture of some wholly owned and some"）
- 2026-08-06｜Douglas Coltharp｜competition：管理層說明同店與總出院量的區分重要性下降（原話："distinction between same-store and total discharge growth"）
- 2026-08-06｜Mark Tarr｜competition：北卡廢除 CON 的生效資訊（原話："North Carolina repealed its Certificate of Need law"）
- 2026-08-06｜Mark Tarr｜competition：北卡初步優先鎖定的市場數（原話："This has led to an initial prioritization of 15 markets"）
- 2026-08-06｜Patrick Tuer｜product：中風出院量成長（同店口徑另列）（原話："Those were up 7.9% and 8%, respectively, on a same-store"）
- 2026-08-06｜Douglas Coltharp｜product：髖膝關節置換類別成長（原話："was up only modestly, about 1% in the quarter."）
- 2026-08-06｜Patrick Tuer｜product：VA 業務 Q2 成長率（原話："we hit VA growth of around 33%"）
- 2026-08-06｜Douglas Coltharp｜product：新院平均損益轉正與入住率爬坡節奏（原話："4-wall positive EBITDA by the time they hit month 6"）
- 2026-08-06｜Douglas Coltharp｜product：AI／Palantir 效益多半仍在未來（原話："I think a lot of it is still in front of us"）
- 2026-08-06｜Mark Tarr｜product：Q2 開幕的新院（原話："we opened a new 50-bed hospital in Concordville"）
- 2026-08-06｜Douglas Coltharp｜risk：Medicare Advantage 事前授權拒付仍是挑戰（原話："denials through pre-authorization from Medicare Advantage"）
- 2026-08-06｜Douglas Coltharp｜risk：admit-and-appeal 試行勝訴率數字（原話："of that 144, we have prevailed on 128, which is"）
- 2026-08-06｜Douglas Coltharp｜risk：加州 RCD 的 MAC 準備不足（原話："the MAC was less well prepared than we would have hoped for"）
- 2026-08-06｜Patrick Tuer｜customer：護理離職率降至 12 年以上低點（原話："our nursing turnover sits around 19%"）
- 2026-08-06｜Patrick Tuer｜customer：career ladder 參與度（原話："we are up to 43% of eligible RNs"）
- 2026-08-06｜Douglas Coltharp｜customer：Q2 超過 90% 入住率的醫院數（原話："In Q2, we had 60 hospitals at greater than 90%"）
- 2026-08-06｜Patrick Tuer｜customer：COO 稱此為近年最佳招募季度（原話："this was our best hiring"）

### 問答異常語氣（迴避／改口／保留）
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：Andrew Mok：同店出院量成長是否優於內部預期；若高敏銳度類別會持續，為何不願說敏銳度增益可持續｜答法：拒絕回答是否優於內部預期（只對照財測）；對敏銳度可持續性改談同店口徑不重要與波動，COO 稱不願被「逼到牆角」
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：Pito Chickering：下半年同店出院量是否應模型化為 4% 以上｜答法：未給數字，改談同店與總出院量區分漸不重要、較易比較基期與新增產能
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：A.J. Rice：SWB 上調是否僅今年，或長期以更高工資換較低離職｜答法：稱僅是今年假設，明年增幅預期放緩，但拒絕給出水準

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 4 | 4 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 衛星候選（護城河 8/10 B 級頂端 + 估值 🟢 便宜 Fwd PE 16x 5Y 分位 22%；但 Pure MA 🟡 觀察池修復中 + Rosen class action 未結案 🟡 兩項時機訊號疊加 → 等 W52 斜率轉正 + 訴訟 motion to dismiss 解除任一觸發後可升 A）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"2026-2028 新院 ramp 順利且新建總 capex IRR > 15%","columns":{"2Y 驗證點":"2026 開 8 新院 + 175 擴床如期完工；新院首年 occupancy ≥ 65%","5Y 驗證點":"2028 ROIC 維持 14-15%（capex peak 過後）；2030 IRF 床數較 2025 +25%（即 +1900 床）","10Y 驗證點":"2030 維持 30%+ IRF 市佔；新院第 4 年 occupancy ≥ 78%（與成熟院相當）","具體數字門檻":"2026 capex $675-725M / 新院 8 家全完工；首年新院 occupancy ≥ 65%；ROIC ≥ 14%","信息來源":"5/1 Q1 26 法說 + 2026 guidance；2025 10-K p.42","漂移觸發條件":"連 2 季 TTM occupancy"}},{"id":"H2","text":"IRF-PPS Medicare rate update 持續正向（2026 +2.6%，未來年化 +2% ~ +3%）","columns":{"2Y 驗證點":"2027 IRF-PPS proposed rule（4 月）顯示 rate update ≥ 1.5%","5Y 驗證點":"2028-2030 累積 rate update ≥ 8%（年化 ≥ 2.5%）","10Y 驗證點":"2030+ Medicare-for-All 或 MA bundled payment 未顛覆 fee-for-service IRF-PPS 架構","具體數字門檻":"年度 rate update ≥ 1.5% 為門檻；","信息來源":"CMS-1829-F（FY2026 final rule, Aug 2025）；前 5Y 平均 rate update +2.3%","漂移觸發條件":"連 2 年 rate update"}},{"id":"H3","text":"估值倍數從當前 16x 修復至 19-20x（capex 期過 + 監管疑雲消化）","columns":{"2Y 驗證點":"2027 末 Fwd PE 修復至 18x 以上","5Y 驗證點":"2028+ Fwd PE 19-20x（5Y 中位）","10Y 驗證點":"不適用（10Y 倍數本就 mean-revert）","具體數字門檻":"Fwd PE 修復至 18x 以上、PEG 修復至 1.5 以下","信息來源":"§13.1 歷史分位；StockAnalysis 5Y forward PE 區間","漂移觸發條件":"連 4 季 Fwd PE"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"新院 ramp 慢 + capex 浪費","columns":{"對應假設":"H1","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"新院首年 occupancy；ROIC 趨勢；growth capex 占營收比","警戒閾值":"新院首年 occupancy 15% 連 2 年 → 警戒；ROIC 跌破 13% → 反轉"}},{"id":"R2","text":"IRF-PPS rate update 結構性下降","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"每年 4 月 proposed rule；MA 占 Medicare 比例變化；CMS 對 IRF 60% Rule 政策動態","警戒閾值":"連 2 年 rate update"}},{"id":"R3","text":"Class action 訴訟惡化 + 監管罰款","columns":{"對應假設":"H3、品質保證","時間尺度標記":"⚡ 短期（1-2 季可觸發）","監測指標":"Rosen / Levi 案 motion to dismiss 結果；SEC 公開調查公告；CMS 對個別醫院的監管動作","警戒閾值":"motion to dismiss 被駁回 → ⚡ 立即修正 trap 至 🔴；SEC 啟動正式調查 → ⛔ 重評至 X；多家醫院被 CMS 暫停 Medicare 認證 → ⛔"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":104.96,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"EHC","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Encompass Health Corporation"},"oneliner":"美國住院復健醫院龍頭：高齡化需求加自建床位撐起約9%營收成長，Medicare與MA合占營收約82%是最大風險；前瞻本益比21.8倍已反映品質，等115美元以下再分批","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是傳統Medicare與Medicare Advantage的錢（合計約占營收82%），錢卡在CMS年度費率與MA事前授權兩道關；量靠自建床位承接高齡化需求","reasoning":"收錢方式：病患從急性醫院轉入（10-K稱約92%病患來自急性醫院），按每次出院向付款方請款。Q3營收1,609.5百萬美元（+8.9%）＝出院69,605人次（+5.7%，同店+3.0%）×每次出院淨收入22,543美元（+4.0%）；調整後EBITDA 346.6百萬美元，利潤率約21.5%；自算GAAP營業利益288.0百萬美元，利潤率約17.9%；TTM營業利益率18.47%。全年指引年內第三度上修到營收64.5～65億美元、調整後EPS 6.23～6.37美元。分部資料事實表未涵蓋，以付款方結構代替：FY2025傳統Medicare 65.4%、Medicare加MA約82%。事實表毛利率自2025年起由約41%跳到約96%，是資料商科目歸類改變，不是經營變化，本文改用營業利益率判讀。單點依賴：付款方集中於聯邦醫療保險，這是集中度風險，不是護城河證據。產業時鐘在擴張期：需求隨75歲以上人口每年約+4%成長，公司全年開8家新院，北卡10-01廢除CON打開新市場；依據是床位與需求，不是股價。供需持久度：結構性持久，需求端由人口結構決定，但供給可逆性正在升高（南卡、北卡相繼廢除CON），付款方審核（MA事前授權、RCD事前審查）決定需求能轉成多少收入。","fact_refs":["f_kpi0_gaap_net_operating_reven","f_kpi1_adjusted_ebitda_non_gaap","f_kpi2_gaap","f_kpi5_adjusted_eps","f_kpi6_2026","f_kpi7_discharges","f_peer_ehc_operating_margin_pct","f_peer_ehc_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"高重複性、低自主定價：約82%營收來自Medicare與MA，傳統Medicare費率由CMS每年規則決定（FY2027淨更新+2.3%），公司能主導的是病患敏銳度組合與床位量","unit_econ_note":"每次出院淨收入22,543美元（Q3，+4.0%）；新院第6個月四牆EBITDA轉正、第10個月入住率逾70%、第3～4年成熟；新院每床約125萬美元、IRR中段十幾%，擴床每床約85萬美元、IRR 25%以上（2026-10-29 Q3法說 Coltharp）","archetype":{"primary":"受監管公用/穩定內需","secondary":"品質複利成長","confidence":"中","fingerprint":"政府定價為主、靠自建產能擴張吃人口老化需求、再投資報酬中段十幾%"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：公司所在郡一年新增近50萬名Medicare受益人、75歲以上人口年增約4%（法說），多市場IRF需求超過供給（Becker's評論）；風險在付款方審核與CON廢除帶來的供給可逆性","bargaining":{"up":"上游是護理與治療人力：Q3薪資每FTE+3.8%，溢價人力連16季下降、約聘占FTE 0.9%，離職率20.7%低於十年均值24.2%，上游議價力目前偏弱","down":"下游付款方強勢：傳統Medicare費率由CMS訂，MA以事前授權拒付壓用量；公司以入院後申訴反制（294件、87%翻案），VA轉介按傳統Medicare費率付款且連6季成長逾20%","geo":"39州加波多黎各，集中佛州與德州，無海外營運；州級CON法規與州Medicaid補充給付（佛州）是地域變數"},"profit_pool_dir":"IRF利潤池往規模化、高敏銳病患集中：公司關閉4個低效單位，低敏銳關節置換同店−5.3%，以中風、腦傷、神經等高敏銳類別補量；主要對手是急性醫院附設復健單位","tam_table":{"expanded":false,"reason":"事實表未涵蓋IRF全國床數、公司份額與滲透率；公司成長主要靠自建產能而非滲透率提升，改以出院量、床位管線與受益人增量判讀"}}}},"q2_moat":{"verdict":"護城河方向持平：執行力仍在擴大，定價權握在CMS與MA手上，CON廢除是兩面刃，合併判為B級","reasoning":"機制：規模化的臨床能力加開院機器。臨床面，公司持有150張Joint Commission中風認證、約占全部中風認證65%，AHA/ASA 2026指引建議符合條件的中風病患優先IRF而非SNF；人力面，溢價人力連16季下降、約聘占比0.9%為2020年Q4以來最低；開院面，每年6～10家新院、新院第6個月四牆EBITDA轉正。可證方向：年度營業利益率由2022年14.49%、2023年15.24%、2024年16.09%、2025年17.74%升到TTM 18.47%，執行力擴大。同業TTM營業利益率HCA 15.31%、UHS 11.28%、THC 22.52%；FCF利潤率EHC 6.97%低於HCA 7.59%與THC 14.09%，因為成長型資本支出全數計入；同業投入資本與ROIC事實表未涵蓋，無法算報酬差距。定價權：傳統Medicare費率由CMS決定，MA以事前授權壓量，公司靠敏銳度組合把每次出院收入推高約4%，但管理層已說Q4起年增會放緩；MA壓力只計入定價權分數一次，威脅不重複扣分。評分：執行9、定價權6。產業態勢：雙向拉鋸——競爭面南卡、北卡廢除CON降低進入障礙；結構面高齡化與AHA指引支持IRF；其他結構變數在付款方（MA事前授權、2027-01起RCD擴大到75家醫院）。報酬持續期：當期ROIC因投入資本事實表未涵蓋無法計算，推定為高利益率×低周轉；增量報酬取管理層自述專案IRR約15%；淨再投資率下限以FY2025（淨利566.2－自由現金流439.2）÷淨利≈22%代理，上限依Q2法說資本支出約占營收15%估約六成（折舊攤銷事實表未涵蓋）；內生成長上界約9%，下限約3%。","fact_refs":["f_peer_ehc_operating_margin_pct","f_peer_ehc_fcf_margin_pct","f_peer_hca_operating_margin_pct","f_peer_hca_fcf_margin_pct","f_peer_uhs_operating_margin_pct","f_peer_uhs_fcf_margin_pct","f_peer_thc_operating_margin_pct","f_peer_thc_fcf_margin_pct","f_peer_ehc_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模化臨床能力（中風認證約占全國65%、高敏銳病患收治）＋人力體系（職涯階梯、低溢價人力）＋可複製的開院機器，在付款方審核下仍能收到並留住高敏銳病患","execution":9,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：營業利益率2022年14.49%→TTM 18.47%，溢價人力連16季下降；定價權穩定偏弱：費率由CMS訂、MA事前授權收緊、2027年RCD擴大；兩者合併為持平。份額數據事實表未涵蓋","competitor_notes":[{"name":"HCA","strategy_note":"急性醫院龍頭，附設復健單位是IRF主要競爭形式；營業利益率15.31%低於EHC，在CON廢除州有能力自建復健產能，也是潛在合資夥伴"},{"name":"UHS","strategy_note":"以急性與行為健康醫院為主，營業利益率11.28%、FCF利潤率4.98%，與EHC住院復健的直接重疊有限"},{"name":"THC","strategy_note":"營業利益率22.52%、FCF利潤率14.09%高於EHC，但事實表未拆其業務組合，不宜直接當IRF對照"},{"name":"SEM","strategy_note":"同業表無財務資料；10-K提到另有一家上市公司經營38家IRF，事實表未指名是否即此公司"}],"peer_na_reason":"同業投入資本與ROIC事實表未涵蓋，改以營業利益率與FCF利潤率比較；SEM財務資料缺","threats":[{"level":"🟡","text":"CON廢除：南卡2023年、北卡2026-10-01相繼廢除IRF的CON，急性醫院系統可自建或擴張復健服務；短期公司是北卡先行者（15個優先市場、6塊土地簽約），長期進入障礙下降","p":"20%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#3"]},{"level":"🟡","text":"Medicare Advantage用量偏低：MA體系IRF使用率0.4%對傳統Medicare 1.16%，Q3全公司MA出院年減1.1%；入院後申訴試點翻案率87%，此項已計入定價權分數，不重複扣分","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"居家與價值導向照護替代：高強度居家復健在低中複雜度病患成本較低、功能結果較佳，支付若改按強度計價將削弱IRF溢價；公司病患組合正往指引推薦IRF的高敏銳類別移動","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#2","supply_demand_durability#5"]}],"roic_durability":{"quadrant":"高利益率×低周轉（推定；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是中風、腦傷等病患，決策者是急性醫院醫師與個管師，付款者是Medicare與MA；需求屬需要而非想要（延後復健會損失功能），75歲以上人口年增約4%。弱環在付款者：MA事前授權讓需求轉不成收入，Q3全公司MA出院年減1.1%。代理讀數：同店出院+3.0%、總出院+5.7%"},{"item":"決策層級","level":"🟡","text":"替代發生在每一次出院去向的選擇（IRF、SNF或居家），轉換成本低，靠轉介關係與臨床成果維繫。高敏銳類別替代性低（神經+9.3%、中風+5.1%，AHA指引優先IRF），低敏銳關節置換同店−5.3%已在流失；出院返家率84.7%是留住轉介的代理指標"},{"item":"價值鏈分配","level":"🟡","text":"付款方拿走價值鏈最大份額：傳統Medicare單方定價，MA透過拒付分走節省；上游人力議價力目前偏弱（溢價人力連降16季）。急性醫院既是轉介來源也是對手，北卡採自有與合資混合進入，合資會分走部分利潤"},{"item":"社會容忍度","level":"🟡","text":"IRF費率高於SNF，屬聯邦預算壓力下的可砍項目；授權法源是IRF前瞻支付制度與CMS年度規則，可經年度規則或國會預算法案修改。2027年RCD事前審查擴大到75家醫院、證券集體訴訟未結，顯示監管審視在升高；替代支付方案是否已進入政策討論，事實表未涵蓋"}],"roiic":"約15%（管理層自述專案IRR：新院中段十幾%、擴床≥25%、小型院目標約20%；屬專案IRR，非會計增量ROIC）","reinvest_rate":"約22%～60%（下限＝FY2025（淨利566.2－自由現金流439.2）÷淨利，未加回少數股東現金盈餘與非現金費用而偏低；上限依Q2法說資本支出約占營收15%推估，折舊攤銷事實表未涵蓋）","endo_ceiling":9.0,"formula_note":"內生成長上界＝增量報酬約15%×再投資率上限約60%≈9%；以下限22%計約3%。取上界9%作情境檢查用，屬估計值、信心低"}}}},"q3_growth":{"verdict":"成長跑道寬：需求由人口結構決定，小型院（約200個潛在地點）與北卡是有來源的下一段產能曲線，但五年後仍受付款方政策約束","reasoning":"成長組成：量為主、價為輔、回購加成、無併購。Q3營收+8.9%＝出院+5.7%與每次出院收入+4.0%；前九月回購191萬股，約占流通股98.3百萬股的1.9%。三年共識EPS（Koyfin：FY2026E 6.27、FY2027E 6.81、FY2028E 7.42美元，近三個月FY1上修4.5%）以FY2025A GAAP稀釋EPS 5.54美元為基期，年複合約10.2%；只看FY2026E到FY2028E為8.8%。內生成長上界約9%（見護城河段），共識超出約1個百分點，缺口歸因淨回購（每年約1.5～2%），不依賴倍數重估。FY2027共識營收70.18億美元，較FY2026E 64.75億美元成長8.4%。跑道：公司目標每年6～10家新院、2027年擴床150～200床，首家小型院2027年底開業，管理層稱2028～2029年每年至少6家、已辨識約200個地點，北卡已鎖定15個市場；需求端公司所在郡一年新增近50萬名Medicare受益人。IRF滲透率與公司份額事實表未涵蓋，跑道年數以產能管線與人口成長判斷約10年以上。衰退信號亮一項：2022～2025年EPS年複合約27%遠高於營收約11%，主要是疫情後人力成本正常化帶來的利潤率回升，管理層已說溢價人力降幅進入邊際遞減；自由現金流對淨利2024年0.79、2025年0.78，未連兩年低於0.75。價值陷阱風險🟡、長期成長性🟡。AI取代風險低：實體住院照護，AI目前用於營運效率（Q2法說稱效益多在未來）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_discharges","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"量約六成、價約四成，加上回購每年約1.5～2%；無併購（Q3：出院+5.7%、每次出院收入+4.0%）","runway_years":10,"runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段：增量報酬約15%×再投資率上限約60%≈9%；三年共識EPS年複合10.2%超出約1個百分點，缺口歸因淨回購","segments":{"expanded":false,"reason":"事實表未收分部資料；成長由出院量、每次出院收入與床位擴充三項驅動，已在成長組成交代"},"decay_signals":[{"signal":"毛利率連2季YoY下滑","lit":false,"note":"毛利率資料受科目歸類改變扭曲，改看營業利益率，連續上升"},{"signal":"核心市占近12個月縮減","lit":false,"note":"份額事實表未涵蓋；總出院+5.7%"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"每次出院收入+4.0%同時出院+5.7%"},{"signal":"EPS CAGR顯著高於Rev CAGR","lit":true,"note":"2022～2025年EPS年複合約27%對營收約11%，來自人力成本正常化的利潤率回升"},{"signal":"FCF/NI<0.75連2年","lit":false,"note":"2024年0.79、2025年0.78"},{"signal":"SBC/Rev>5%且逐年上升","lit":false,"note":"SBC約占營業利益5.2%，占營收更低"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"note":"需求隨高齡化成長；MA與居家替代列為監測"},{"signal":"產業估值倍數近3年系統性下移","lit":false,"note":"事實表未涵蓋產業倍數序列"},{"signal":"maintenance capex占FCF>60%","lit":false,"note":"維護性資本支出事實表未涵蓋"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"note":"持續擴產，營收年增約10%"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健：以自建新院與擴床為主、近12個月無併購，回購與小額股息並行，淨槓桿1.8倍","reasoning":"現金轉換：自由現金流對淨利2023年0.76、2024年0.79、2025年0.78（年度財報），TTM FCF利潤率6.97%，成長型資本支出全數計入；公司口徑調整後自由現金流Q3為263.4百萬美元、前九月634.2百萬美元（+8.9%）。資本去向：前九月回購約191萬股、203.7百萬美元（均價約106.7美元），Q3回購約49.5萬股、57.9百萬美元（均價約117美元）；季股息0.21美元，TTM殖利率0.57%；Q3加發1億美元2034年到期5.875%票據。資產負債：總債務2,803.4百萬美元、現金76.2百萬美元，淨負債2,727.2百萬美元，季末淨槓桿1.8倍，10億美元循環額度可用約8.7億美元，信貸協議債務2031年前不到期。管理層稱框架不變：股息溫和調升，北卡與小型院會推高資本支出，槓桿低於2倍下仍有空間加大回購。近三年現金去向四分、債務加權利率與到期結構事實表未涵蓋。營運槓桿：Q3營收+8.9%、調整後EBITDA+15.5%，沒有利潤率壓縮。SBC約占營業利益5.2%，以年化營業利益計約當市值0.45%，稀釋輕。回購收益率：以FY2026E EPS 6.27美元對前九月均價約106.7美元計約5.9%，十年期公債殖利率事實表未涵蓋，無法判定是否高出2個百分點。","fact_refs":["f_kpi3_adjusted_fcf","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_ehc_fcf_margin_pct","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近12個月8-K未見併購項目，成長來自自建新院與擴床，併購報酬不適用"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"前九月回購均價約106.7美元，以FY2026E共識EPS 6.27美元計盈餘收益率約5.9%；十年期公債殖利率事實表未涵蓋，無法判定"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC約占營業利益5.2%，以Q3營業利益288.0百萬美元年化計約6千萬美元，約當市值0.45%/年，低於1.5%；前九月淨回購約1.9%股數"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，近12個月無併購；股東回饋以回購為主、股息殖利率約0.6%"}}}},"q5_valuation":{"verdict":"現價要求未來五年EPS年增約10%且本益比守在20倍以上，才有年化8%以上報酬；我信成長約8～9%，不信倍數守得住，估值偏貴、不追","reasoning":"現價136.69美元對FY2026E共識EPS 6.27美元為前瞻21.8倍、對FY2027E 6.81美元為20.1倍；trailing本益比21.87倍，在近四個年度端點中位於92分位，P/S 2.12倍與EV/S 2.55倍都在最高點；五年分位事實表未涵蓋（只有四個年度端點）。PEG＝21.8÷三年EPS年複合10.2%≈2.1，偏貴。反推：要年化約8.7%（含0.6%股息），需EPS五年年增10%且終端倍數維持20倍；Base假設EPS年增約8.4%、終端18倍，五年價格報酬約+24%，年化中個位數。漲幅來源：26週上漲28.6%，同期FY1共識只上修4.5%，大部分來自倍數擴張；前份（2026-05-25，股價104.96美元）的估值修復論點已兌現。分母檢查：FY2026調整後EPS含佛州補充給付沖回與系統轉換壞帳等一次性負向項目，估計約占EBITDA 1%以內，分母不構成爭點。賣方：8月平均目標價約148.7美元、區間140～160美元（Q3後更新未查到），現價距平均約低8%，不足以支持追價。同業前瞻本益比事實表未涵蓋，終端倍數以自身區間定錨。週線均線狀態為觀察：價格137.08美元高於52週110.36與104週109.65，250週斜率1.6%仍在±3%區間；RSI資料標示不可用，不引用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_slope_w250_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026E共識調整後EPS）搭配PEG；受監管、穩定成長型公司以盈餘倍數為主尺","peers":{"expanded":false,"reason":"事實表同業對照只收毛利率、營業利益率與FCF利潤率，未收同業前瞻本益比，無法做倍數對照；終端倍數改以自身倍數區間定錨"},"fwd_pe":21.8,"peg":2.14,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"PEG約2.1（前瞻21.8倍÷三年EPS年複合10.2%）高於2；trailing本益比在近四個年度端點的92分位、P/S與EV/S在最高點；Base五年年化報酬中個位數，低於8%；五年分位事實表未涵蓋","upside_short_pct":-0.4,"upside_mid_pct":23.5,"denominator_disputed":false,"denominator_note":"FY2026調整後EPS含佛州補充給付沖回（淨約550萬美元）與系統轉換帶來的壞帳偏高，合計約占全年EBITDA 1%以內，分母不構成爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在付款方：傳統Medicare費率或MA用量轉向，加上未結的證券集體訴訟；價值陷阱風險🟡","reasoning":"反證與裁定集中寫在反證紀錄，此處只交結論。三個最強反駁：①付款方把病患導向SNF與居家（MA體系IRF使用率只有傳統Medicare約三分之一）；②成長靠資本支出，新院與小型院報酬若下滑，營收成長不等於每股價值成長；③前瞻21.8倍已把2026年三度上修外推。管理層前後說法對照：2026-08-06 Q2法說，COO Tuer不願承諾敏銳度可持續、CFO Coltharp拒給2027年薪資增幅水準；2026-10-29 Q3法說改稱部分趨勢可持續，但承認Q4起定價年增放緩、職涯階梯效益滿年，沒有改口，承諾仍保守。最大回撤推估：Bear終點約−36%，監管與訴訟消息曾造成單日−10.4%（2025-07-15），倍數由21.8倍壓到13～15倍的過程可再放大，區間取−30%～−45%；歷史最大回撤事實表未涵蓋。訴訟的法院、案號與進度事實表未涵蓋。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_fwd_pe_latest","f_ma_w52","f_ma_w104"],"verdict_values":{"trap":{"verdict":"🟡","label":"訴訟未結＋付款方政策風險，衰退信號亮一項（歷史EPS增速遠高於營收）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":6.27,"pe":21.8,"basis":"FY2026E共識調整後EPS（Koyfin 2026-10-31）；終端倍數同樣以前瞻一年EPS為分母"},"eps":{"bull":[7.05,7.85,8.75,9.7,10.75],"base":[6.81,7.42,8.05,8.7,9.38],"bear":[6.4,6.3,6.4,6.55,6.7]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.57,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-45,"hi":-30,"basis":"Bear終點約−36%（6.70美元×13倍）為下限參考；監管與訴訟消息曾造成單日−10.4%（2025-07-15），倍數由21.8倍壓到13～15倍的過程會先於盈餘下修發生，回撤區間取−30%～−45%；歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"小型院2028年起每年≥6家、北卡新院放量，總出院年增約8%；MA申訴擴大收復用量；每次出院收入年增約3%、回購每年約2%；EPS年複合約11%；終端22倍與現價相近","base":"總出院年增約6%、每次出院收入年增約3%、利潤率持平、回購約1.5%；2027～2028年貼共識，之後EPS年增約8%；終端18倍，低於前份引述的五年中位約19～20倍，反映成長放緩與付款方風險；同業前瞻本益比事實表未涵蓋","bear":"Medicare淨費率更新趨近零、RCD與MA壓低用量和收款，總出院年增降到2～3%，FY2031 EPS僅6.70美元；終端13倍，對應成長熄火到低個位數後的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"MA體系IRF使用率0.4%對傳統Medicare 1.16%；高強度居家復健在低中複雜度病患功能較佳、成本較低，現行支付按地點而非強度計價才偏向住院復健；另有分析認為價值導向照護與門診、居家轉移會長期壓抑住院量","assumption":"付款方持續把IRF病患導向SNF與居家，支付改按強度計價，傳統Medicare占比隨MA滲透下降","consequence":"總出院年增由約6%降到2%、每次出院收入被拉向SNF水準，EPS停滯，倍數壓到13倍，五年後股價腰斬","ruling":"部分採納：MA轉移是真的（Q3全公司MA出院−1.1%），但公司組合已往AHA指引推薦IRF的高敏銳類別移動（神經+9.3%、中風+5.1%），低敏銳關節置換本就在流失；居家研究多針對低中複雜度與非MA情境。放進Bear情境與30%機率，不作為不投資的理由。與唯一致命點部分重疊：同屬付款方定價，致命點看傳統Medicare費率，此處補足用量面","watch":"全公司MA出院年增；高敏銳類別占比；CMS支付改革提案","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","supply_demand_durability#5"],"fact_refs":["f_kpi7_discharges"]},{"view":"論點失敗","evidence":"證券集體訴訟起訴書（Exchange Act 10(b)與20(a)），類別期間2022-02-26至2025-07-15，被告含CEO Tarr與CFO；多家律所2025年7～9月公告調查；2025-07-15單日跌10.4%；10-K稱可能有未公開的qui tam案；法院、案號與現況事實表未涵蓋","assumption":"訴訟揭露的事實若涉及收治或申報作法，會引來監管或聯邦虛假申報追訴","consequence":"RCD與稽核更嚴，量與費率雙殺，管理層信任折價","ruling":"不可裁決至駁回動議裁定出爐；事件軸未見SEC調查或財報重編，目前列風險，價值陷阱維持🟡","watch":"法院對駁回動議的裁定；10-Q法律程序段；SEC公告","evidence_refs":["major_events#0","lawsuit_class_action#0","lawsuit_class_action#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"成長靠資本支出：Q2法說稱資本支出約占營收15%（可能為高點）；新院每床約125萬美元、IRR中段十幾%；TTM FCF利潤率6.97%；北卡將採自有與合資混合進入；CON廢除後在更多市場要靠搶建取勝，10-K自承競爭可能升高","assumption":"建造、土地與人力成本上升，加上合資分潤，新院增量報酬滑到10%以下","consequence":"營收照樣成長約9%，但再投資不再創造價值，每股價值成長落後營收","ruling":"部分採納：目前新院第6個月四牆EBITDA轉正、與歷史一致，擴床IRR≥25%拉高組合報酬；但小型院與北卡都未驗證。增量報酬以約15%為上限，Base不給加速","watch":"新院第10個月入住率>70%；每床成本；少數股東分配占EBITDA比例","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_peer_ehc_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價26週漲28.6%；前瞻本益比21.8倍；trailing本益比在近四個年度端點的92分位、P/S與EV/S在最高點；8月賣方平均目標價約148.7美元、區間140～160美元，Q3後更新未查到","assumption":"市場把2026年三度上修與約4%的每次出院收入年增外推為常態","consequence":"2027年定價年增如管理層所說放緩、上半年RCD壞帳波動，倍數回到18倍就抵銷近兩年盈餘成長","ruling":"採納：這是本次不追的主因。Base五年年化中個位數，低於8%","watch":"前瞻本益比；FY2027共識EPS修正方向","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_fwd_pe_latest","f_week26_return_pct","f_pe_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 104.96 → 本次 136.69（+30.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=104.96","side_b":"本次 price_at_dd=136.69","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 104.96 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 104.96 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 104.96 美元：Bull 價 236.5、Bear 價 87.1，五年期望值 +50.4%，基準年化 10.0%，不對稱比 4.91","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 4.91。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 104.96 美元：五年期望值 +50.4%，基準年化 10.0%，不對稱比 4.91","side_b":"本次情境、股價 136.69 美元：五年期望值 +15.5%，基準年化 4.3%，不對稱比 1.34","ruling":"再換股價、情境不動：起點價上漲 30.2%，五年期望值少 34.9 個百分點，基準年化少 5.7 個百分點，不對稱比由 4.91 降到 1.34。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層一次性歸因：壞帳","cause":null,"prior_field":null,"side_a":"公司：Q3壞帳2.7%約三分之二來自Q2帳務系統轉換，Q4回到2～2.5%，新系統處理的帳款沒有問題（2026-10-29 Q3法說 Coltharp）","side_b":"RCD於2027-01-01擴大到75家醫院，審查方處理量增逾10倍、第一循環100%事前審查，公司自己最擔心審查方的行政能力","ruling":"可調和：系統轉換與RCD是兩件事，前者已有具體機制說明，後者尚未發生。不採信也不否定，列為未證、監測；Q4壞帳>2.5%或2027上半年任一季>3.0%，一次性說法即證偽","evidence_level":"管理層說法加法規時程","settle_metric":"季度壞帳占營收","if_then":["若2026年Q4壞帳≤2.5%且2027年Q1≤2.8%，則一次性說法成立，等待價格條件不變","若2027年Q1與Q2壞帳皆>3.0%，則停止加碼並把Bear機率提高到35%"],"evidence_refs":[]},{"axis":"MA用量：入院後申訴能否扭轉","cause":null,"prior_field":null,"side_a":"公司：9家試點醫院294件申訴、87%翻案，試點市場MA出院成長36%、總出院+9.3%；2027年推到所有醫院的中風病患，試點醫院由9家增到13家（Tuer、Coltharp）","side_b":"MA體系IRF使用率0.4%對傳統Medicare 1.16%；Q3全公司MA出院年減1.1%（排除單位關閉約+1%）；公司所在郡新增受益人約一半走MA","ruling":"可調和、程度差異：試點證明申訴有效，但規模小，全公司MA仍接近零成長。選公司一側但打折：Base不計入申訴擴大的量能貢獻，Bull才計入","evidence_level":"公司試點數據對外部使用率統計","settle_metric":"全公司MA出院人次年增（2027上半年）","if_then":["若2027年Q2全公司MA出院年增≥+3%，則MA侵蝕論點證偽，股價≤125美元即可分批建倉","若連兩季全公司MA出院年增≤−3%，則Base機率降到40%並把首倉上限減半"],"evidence_refs":["substitute_technology#1"]},{"axis":"CON廢除對護城河的方向","cause":null,"prior_field":null,"side_a":"北卡2026-10-01廢除CON，公司已鎖定15個市場、6塊土地簽約，管理層強調先行者優勢（2026-08-06 Q2法說 Coltharp；2026-10-29 Q3法說 Tarr）","side_b":"10-K自承CON弱化可能提高競爭，南卡2023年已廢除；急性醫院系統可能擴張復健服務","ruling":"可調和、按時間分層：三年內對公司是淨增量（資本、開院速度、臨床認證領先）；更多州廢除後，原受CON保護市場的進入障礙下降。威脅只在護城河段記一次，不重複扣分","evidence_level":"10-K風險因素與逐字稿","settle_metric":"北卡、南卡非公司IRF新設數","if_then":["若2028年前北卡、南卡出現3家以上非公司新設IRF，則護城河方向改判向下並把Base終端倍數下修1倍"],"evidence_refs":["competitive_share_entrants#1","supply_demand_durability#3"]},{"axis":"管理層前後說法：敏銳度與定價","cause":null,"prior_field":null,"side_a":"2026-08-06 Q2法說：Tuer不願承諾敏銳度可持續（不想被逼到牆角），Coltharp稱下半年定價上行沒有確定性","side_b":"2026-10-29 Q3法說：Tuer稱部分趨勢可持續；Coltharp稱Q4起對上去年MA事前授權收緊後的高基期，定價年增會較不明顯","ruling":"一致，沒有改口：管理層一直保守，Q3更明確承認2027年定價年增放緩。Base把2027年每次出院收入年增放在約3%，低於近四季約4%","evidence_level":"逐字稿對照","settle_metric":"每次出院淨收入年增","if_then":["若2027年Q1每次出院收入年增<2.5%，則H2進入削弱觀察並下修Base EPS約2%"],"evidence_refs":[]},{"axis":"現在就買的最強論證（對本次不追的反面）","cause":null,"prior_field":null,"side_a":"全年指引年內三度上修；調整後EPS前九月+17%；FY1共識三個月上修4.5%；2027年佛州給付沖回不再重演、單位關閉滿年、擴床150～200床、北卡開市；高齡化需求每年約+4%","side_b":"股價26週漲28.6%，前瞻本益比21.8倍；上修只解釋漲幅一小部分；Base五年年化中個位數，Bear可回到87美元附近","ruling":"維持不追：生意好已被定價，約束是價格。若基本面續強而股價不回，接受錯過","evidence_level":"事實表與逐字稿","settle_metric":"2027年指引與股價","if_then":["若2027年指引中點隱含調整後EPS≥7.0美元且股價≤125美元，則提前分批建倉","若股價續漲而共識沒有上修，則不追","若股價下跌但H1至H3都沒有受損，則分批反買"],"evidence_refs":[]},{"axis":"估值結論與綜合評級（前份→本次）","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-05-25，股價104.96美元）：前瞻本益比約16倍、估值便宜，綜合評級B，等週線斜率轉正或訴訟駁回動議兩者任一再升級","side_b":"本次（股價136.69美元，+30.2%）：前瞻本益比21.8倍、PEG約2.1，估值改判偏貴；綜合評級仍為B，理由由「便宜但時機未到」改為「品質好但價格已滿」","ruling":"前份兩個等待條件都沒有被證實：股價已站上52週與104週均線，但250週均線斜率1.6%仍在±3%區間，駁回動議結果事實表未涵蓋；價格卻先漲了30%。同期FY1共識只上修4.5%，漲幅大部分是倍數擴張（前份16倍的分母口徑未載，跨期比較只作方向參考）。本次不翻面追價，改等價格","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比與FY2027共識EPS","if_then":["若股價回到115美元以下而FY2027共識維持6.81美元以上，則分三批建立首倉","若股價續漲而共識沒有上修，則不追"],"evidence_refs":[]},{"axis":"前份估值修復假設退休","cause":"價格變動","prior_field":["thesis.H3"],"side_a":"前份H3：前瞻本益比由16倍修復到18倍以上、2028年後19～20倍","side_b":"本次：前瞻本益比已到21.8倍，假設提前兌現；本次H3改為成本紀律與壞帳","ruling":"門檻已達成而退休，不是因為不成立；新H3改看會直接決定2027年盈餘的壞帳與利潤率","evidence_level":"事實表","settle_metric":"前瞻本益比","if_then":["若前瞻本益比回落到17倍以下而H1至H3仍成立，則重新視為估值修復機會並分批建倉"],"evidence_refs":[]},{"axis":"價值陷阱、護城河方向與成長跑道（前份→本次）","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：價值陷阱🟡（集體訴訟未結）；護城河方向與五年後跑道未填","side_b":"本次：價值陷阱仍為🟡（訴訟未結，衰退信號亮一項）；護城河方向持平；五年後跑道寬","ruling":"新證據：Q3法說揭露小型院約200個潛在地點、2028～2029年每年至少6家，北卡10-01廢除CON且已簽6塊土地，構成有來源的下一段產能曲線；同時MA出院年減1.1%、RCD擴大，定價權沒有變強，護城河方向判持平而非向上。訴訟仍無進度資料，價值陷阱評級不變","evidence_level":"逐字稿與10-K","settle_metric":"小型院開業數、MA出院年增","if_then":["若2028年小型院開業少於3家，則五年後跑道降為中等並下修Bull機率5個百分點"],"evidence_refs":["lawsuit_class_action#0"]},{"axis":"新增欄位（前份未填）","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未填公司類型、循環位置、情境機率、最大回撤與分批裁決","side_b":"本次：公司類型以受監管公用/穩定內需為主、品質複利成長為輔；非循環股，循環位置不適用；情境機率Bull 20、Base 50、Bear 30；最大回撤−30%～−45%；分批裁決與角色由程式依決策矩陣產出","ruling":"框架改版後新增的必填欄，不代表基本面變化；Bear機率30%是因為三年共識EPS年複合超出內生成長上界","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟（加碼）條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：未設定（null）；文字條件為週線斜率轉正或駁回動議解除任一觸發後升級","side_b":"本次：股價≤115美元（約FY2027共識EPS 17倍）時分三批加碼建立首倉","ruling":"本次不追的唯一約束是估值，重啟條件就是估值約束的否定；週線與訴訟條件改列為風險監測，不再當進場條件","evidence_level":"方法","settle_metric":"股價對FY2027共識EPS倍數","if_then":["若股價≤115美元，則分三批加碼建立首倉","若FY2027共識下修超過5%，則115美元門檻按17倍同步下移"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"CMS在FY2028 IRF最終規則或國會立法中，對IRF給出≤0%淨費率更新或改採跨機構同病同酬","ruling":"依數學敏感度選定：傳統Medicare約占營收65.4%，費率每少1個百分點約影響EBITDA 3%，大於任何單一訴訟或競爭事件；發生即清倉","evidence_level":"事實表付款方結構與指引","settle_metric":"年度淨費率更新","if_then":["若FY2028最終規則淨更新≤0%或納入同病同酬，則清倉"],"evidence_refs":[]},{"axis":"停損指標與風險門檻（前份→本次）","cause":"新證據","prior_field":["kill_metrics","thesis.R"],"side_a":"前份：無停損指標陣列；風險門檻為新院首年入住率≥65%、ROIC跌破13%反轉、費率更新<1.5%連2年、駁回動議遭否決則價值陷阱轉🔴、SEC正式調查重評","side_b":"本次：保留費率<1.5%連2年、ROIC<13%（投入資本資料缺口）、駁回動議遭否決減碼一半、SEC正式調查清倉；新院門檻改為第6個月四牆EBITDA轉正與第10個月入住率>70%；新增壞帳連兩季>3.0%減碼一半、單季總出院連6季<4.5%減碼一半、MA出院連兩季≤−3%停止加碼","ruling":"新證據：Q3法說揭露RCD 2027-01起擴大到75家醫院、MA出院年減1.1%、新院爬坡節奏，前份未涵蓋；新院門檻改用公司揭露的節點，比首年入住率65%更早可驗證。前份門檻沒有刪除，取不到值的ROIC標為資料缺口","evidence_level":"逐字稿","settle_metric":"各停損指標","if_then":["若任一停損指標觸發，則依該條動作減碼或清倉，不等下一次完整分析"],"evidence_refs":["substitute_technology#1"]}],"triggers":[{"n":1,"text":"股價回到115美元以下（約FY2027共識EPS的17倍）才分批建立首倉","type":"估值rearm","maps_to":"H1","metric":"股價對FY2027共識EPS倍數","threshold":"股價≤115美元（約16.9倍）","action":"分三批建立首倉，每批間隔至少一次季報","source_freq":"每日收盤","date":null},{"n":2,"text":"RCD事前審查擴大到75家醫院後，壞帳占營收超過3%","type":"風險","maps_to":"R1","metric":"季度壞帳占營收","threshold":">3.0%（2027年Q1或Q2）；連兩季","action":"單季超標停止加碼；連兩季減碼一半","source_freq":"季報","date":"2027-07"},{"n":3,"text":"FY2028 IRF最終規則淨費率更新≤0%或納入跨機構同病同酬","type":"Single Thing","maps_to":"Single Thing","metric":"Medicare IRF PPS年度淨費率更新","threshold":"≤0%或同病同酬","action":"清倉","source_freq":"每年4月提案、7～8月最終規則","date":"2027-07"},{"n":4,"text":"總出院成長跌破論點門檻","type":"假設驗證","maps_to":"H1","metric":"單季總出院人次年增","threshold":"連4季<4.75%削弱；連6季<4.5%反轉","action":"削弱時停止加碼；反轉時減碼一半","source_freq":"季報","date":null},{"n":5,"text":"證券集體訴訟駁回動議遭法院否決，或SEC啟動正式調查","type":"風險","maps_to":"R3","metric":"法院裁定與SEC公告","threshold":"駁回動議遭否決；SEC正式調查","action":"駁回動議遭否決減碼一半；SEC正式調查清倉","source_freq":"10-Q法律程序段與法院文件","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"股價升到165美元以上而FY2027共識沒有同步上修","type":"減碼","maps_to":"H2","metric":"股價對FY2027共識EPS倍數","threshold":"≥165美元（約24倍）且FY2027共識未上修","action":"減碼三分之一","source_freq":"每日收盤與月度共識","date":null},{"n":7,"text":"Q4財報與2027年全年指引","type":"複審日期","maps_to":null,"metric":"2027年調整後EPS指引","threshold":"指引中點對FY2027共識6.81美元的差距","action":"重跑完整分析","source_freq":"一次性","date":"2027-02"},{"n":8,"text":"全公司MA出院連兩季明顯負成長","type":"風險","maps_to":"R2","metric":"全公司MA出院人次年增","threshold":"連兩季≤−3%","action":"停止加碼，首倉上限減半","source_freq":"季報法說","date":null,"evidence_refs":["substitute_technology#1"]},{"n":9,"text":"每次出院淨收入年增跌破2.5%","type":"假設驗證","maps_to":"H2","metric":"每次出院淨病患收入年增","threshold":"連2季<2.4%削弱；連3季<2.25%反轉","action":"削弱時停止加碼；反轉時減碼一半","source_freq":"季報","date":null}],"kill_metrics":[{"metric":"Medicare IRF PPS年度淨費率更新","bear_threshold":"<1.5%連2年（沿用前份）；單年≤0%即清倉","window":"每年7～8月最終規則","source":"CMS IRF PPS最終規則","last_status":"ok"},{"metric":"單季總出院人次年增","bear_threshold":"連6季<4.5%","window":"季報","source":"公司季報新聞稿","last_status":"ok"},{"metric":"季度壞帳占營收","bear_threshold":"連兩季>3.0%","window":"2027上半年RCD第一循環","source":"公司季報與法說","last_status":"warning"},{"metric":"全公司MA出院人次年增","bear_threshold":"連兩季≤−3%","window":"季報","source":"公司法說","last_status":"warning"},{"metric":"ROIC（稅後營業利益÷投入資本）","bear_threshold":"<13%（沿用前份）","window":"年報","source":"10-K；投入資本事實表未涵蓋，資料缺口","last_status":"unknown"},{"metric":"證券集體訴訟駁回動議","bear_threshold":"遭法院否決","window":"裁定時點事實表未涵蓋","source":"法院文件、公司10-Q","last_status":"unknown"},{"metric":"新院爬坡","bear_threshold":"第10個月入住率<70%或第6個月四牆EBITDA未轉正","window":"每批新院開業後一年","source":"公司法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"這段是10-K風險因素的一般性樣板文字，原文本身說明是針對併購審查的產業通則、非針對公司的調查；公司成長路徑是自建新院與擴床，近12個月8-K未見併購項目，證據指向的暴露在本公司不存在"}],"action_conditions":{"rearm_trigger":"股價≤115美元（約FY2027共識EPS 17倍）時分三批建立首倉","exec_line":"現價不追；≤115美元分三批建倉，每批間隔一次季報；FY2028費率最終規則淨更新≤0%或同病同酬則不進場、持有即清倉；股價≥165美元且共識未上修則減碼三分之一"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把2026年約4%的每次出院收入年增與三度上修外推為常態；管理層已說Q4起對上高基期定價年增放緩，2027上半年RCD擴大到75家醫院會讓壞帳波動","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到115美元以下（約FY2027共識EPS的17倍）再分三批建立首倉","qc48_result":"pass","qc48_note":"Bull 情境有出院量乘每次出院收入的算術骨架，但小型院開業節奏和 MA 用量收復兩個關鍵假設只有管理層說法；同業五年報酬的可比案例查不到，所以還不能說有歷史實績背書，成長跑道的證據也建立在尚未開業的新院上。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把2026年約4%的每次出院收入年增與三度上修外推為常態；管理層已說Q4起對上高基期定價年增放緩，2027上半年RCD擴大到75家醫院會讓壞帳波動"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=28.64, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 情境有出院量乘每次出院收入的算術骨架，但小型院開業節奏和 MA 用量收復兩個關鍵假設只有管理層說法；同業五年報酬的可比案例查不到，所以還不能說有歷史實績背書，成長跑道的證據也建立在尚未開業的新院上。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到115美元以下（約FY2027共識EPS的17倍）再分三批建立首倉'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"自建產能驅動量成長：每年開6～10家新院（含小型院）加擴床，總出院人次維持中高個位數成長","2y":"2027年單季總出院年增≥5%；首家小型院2027年底開業；2026年8家新院第6個月四牆EBITDA轉正","5y":"2029年起小型院每年≥6家、北卡開出多家新院；2027～2031年總出院年複合≥6%","10y":null,"threshold":"單季總出院人次年增≥5%（公司2023～2027年總出院目標6～8%；2026年前三季4.3%、5.6%、5.7%，含單位關閉拖累，2027年Q1滿年）","source":"公司季報新聞稿；2026-10-29 Q3法說（Coltharp、Tuer）","drift_rule":"連4季<4.75%（偏離5%）為削弱；連6季<4.5%（偏離10%）為反轉"},{"id":"H2","text":"Medicare費率更新與病患敏銳度支撐每次出院淨收入年增≥2.5%","2y":"FY2028 IRF最終規則淨更新≥1.5%；2027年每次出院淨收入年增≥2.5%（2026年約4%，管理層預告放緩）","5y":"2027～2031年Medicare年度淨更新平均≥2%，未出現跨機構同病同酬","10y":"傳統Medicare仍以IRF前瞻支付制度按地點付費","threshold":"每次出院淨病患收入年增≥2.5%；年度淨費率更新≥1.5%","source":"CMS IRF PPS年度最終規則（FY2027為+2.3%）；公司季報","drift_rule":"連2季<2.4%（偏離5%）為削弱；連3季<2.25%（偏離10%）為反轉"},{"id":"H3","text":"成本紀律守住利潤率：RCD擴大後壞帳回到2～2.5%，調整後EBITDA利潤率≥21%","2y":"2027全年壞帳≤2.5%；2027年調整後EBITDA利潤率≥21%（2026指引中點約21.7%）","5y":"溢價人力降幅進入邊際遞減後，薪資每FTE增幅不高於每次出院收入增幅","10y":null,"threshold":"單季調整後EBITDA÷營收≥21%（Q3為21.5%）；壞帳≤2.5%","source":"公司季報與補充資料；2026-10-29 Q3法說（Coltharp）","drift_rule":"連2季利潤率<19.95%（偏離5%）為削弱；連3季<18.9%（偏離10%）為反轉"},{"id":"H4","text":"IRF仍是中風、腦傷等高敏銳病患的首選照護地點，未被SNF或居家取代","2y":"高敏銳類別（中風、腦傷、神經）出院年增≥4%","5y":"AHA/ASA指引維持IRF優先；出院返家率維持≥84%","10y":"75歲以上人口成長轉成IRF用量成長，傳統Medicare的IRF使用率不下降","threshold":"高敏銳類別出院年增≥4%（Q3：神經+9.3%、中風+5.1%、腦傷+5.7%）","source":"公司法說病患類別揭露；AHA/ASA 2026中風復健指引","drift_rule":"跨2個年度低於3.8%（偏離5%）為削弱；跨3個年度低於3.6%（偏離10%）為反轉"}],"R":[{"id":"R1","text":"RCD事前審查2027-01-01擴大到75家醫院、審查方處理量增逾10倍，壞帳與收款延遲上升","h_ref":"H3","clock":"⚡","threshold":"2027年Q1或Q2壞帳>3.0%，或任一州第一循環核可率<80%","evidence_refs":[]},{"id":"R2","text":"MA事前授權持續壓低用量，MA體系IRF使用率只有傳統Medicare約三分之一，受益人往MA移動","h_ref":"H1","clock":"🔥","threshold":"全公司MA出院年增連4季≤−3%，或入院後申訴翻案率<70%","evidence_refs":["substitute_technology#1"]},{"id":"R3","text":"證券集體訴訟（類別期間2022-02-26至2025-07-15，被告含CEO與CFO）與可能的聯邦虛假申報追訴","h_ref":null,"clock":"⚡","threshold":"駁回動議遭法院否決→價值陷阱評級升為🔴並減碼一半；SEC正式調查→清倉（沿用前份門檻並明定動作）","evidence_refs":["major_events#0","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R4","text":"居家與價值導向照護替代、各州廢除CON引來新進者，長期壓低住院復健用量與進入障礙","h_ref":"H4","clock":"🐢","threshold":"同店出院連4季<1%（排除單位關閉影響），或北卡、南卡出現3家以上非公司新設IRF","evidence_refs":["substitute_technology#0","substitute_technology#2","supply_demand_durability#5","competitive_share_entrants#1","supply_demand_durability#3"]},{"id":"R5","text":"Medicare支付政策收緊：年度費率更新偏低或改採跨機構同病同酬","h_ref":"H2","clock":"🔥","threshold":"年度淨費率更新<1.5%連2年（沿用前份門檻）","evidence_refs":[]}],"single_thing":{"description":"CMS在FY2028 IRF前瞻支付制度最終規則（約2027年7～8月）或國會立法中，對IRF給出≤0%淨費率更新，或改採跨機構同病同酬","why_fatal":"傳統Medicare約占營收65.4%，成本不隨費率調整；以2026指引中點營收約64.75億美元計，費率每少1個百分點約少4,200萬美元營收、幾乎全數落到EBITDA，約占指引中點14.05億美元的3%；同病同酬若把部分診斷拉向SNF費率，降幅以兩位數計，整條EPS路徑下移","if_happens":"清倉；Bear機率上調到50%以上並重跑完整分析","how_monitor":"每年4月提案規則、7～8月最終規則；國會預算法案中的後急性照護條款；公司法說對費率影響的估計","probability":"約5%（12～24個月；FY2027最終規則剛給+2.3%，事實表未見跨機構支付改革提案）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.1,"peg_fy2":1.97,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":5.54,"FY2026E":6.27,"FY2027E":6.81,"FY2028E":7.42},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（事實表未收調整後EPS，口徑不一致）；FY2026E～FY2028E為Koyfin共識調整後EPS（2026-10-31快照）"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"CMS對佛州FY2026 Medicaid州指定給付方案的決定（含公司醫院豁免）","impact":"低","watch":"若核准，Q4可回補約800萬美元EBITDA"},{"date":"2027-01","date_precision":"month","type":"regulatory","event":"RCD事前審查擴大到Jurisdiction JJ的75家醫院，第一循環100%事前審查至6月底","impact":"高","watch":"壞帳占營收與核可率是否≥80%"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4財報與2027年全年指引","impact":"高","watch":"2027年調整後EPS指引中點對共識6.81美元"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"FY2028 IRF PPS提案規則","impact":"高","watch":"淨費率更新與是否出現跨機構支付改革"},{"date":"2027-07","date_precision":"month","type":"regulatory","event":"FY2028 IRF PPS最終規則","impact":"高","watch":"淨費率更新≥1.5%"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"首家小型院（休士頓周邊）開業","impact":"中","watch":"每床成本約100萬美元、IRR目標約20%能否兌現"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「受監管公用/穩定內需」，受監管公用/穩定內需 的專屬核心軸未採證（不計燈號）：regulated_rate_case_roe。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
