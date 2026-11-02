你是 DD 管線 v20 的判斷層閘（gate），標的 H（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（44 條）
- `f_kpi0_gaap_total_revenues`（q1_business）｜營收（GAAP total revenues）＝1743 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_adjusted_ebitda_recast`（q1_business）｜Adjusted EBITDA（recast 口徑）＝295 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gross_fees`（q1_business）｜總費用收入 Gross fees＝327 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_gaap_hyatt`（q1_business）｜GAAP 淨利（歸屬 Hyatt）＝58 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_comparable_system_wide_r`（q1_business）｜Comparable system-wide RevPAR 成長＝7.2 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi6_pipeline`（q1_business）｜淨客房成長與 pipeline＝158000 間（pipeline）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_h_gross_margin_pct`（q2_moat）｜H 毛利率＝20.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.H.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_h_operating_margin_pct`（q2_moat）｜H 營業利益率＝7.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.H.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝7143.17 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_h_fcf_margin_pct`（q2_moat）｜H FCF 利潤率＝6.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.H.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mar_operating_margin_pct`（q2_moat）｜MAR 營業利益率＝15.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MAR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mar_fcf_margin_pct`（q2_moat）｜MAR FCF 利潤率＝11.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MAR.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hlt_operating_margin_pct`（q2_moat）｜HLT 營業利益率＝24.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HLT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hlt_fcf_margin_pct`（q2_moat）｜HLT FCF 利潤率＝14.49 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HLT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_chh_operating_margin_pct`（q2_moat）｜CHH 營業利益率＝25.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CHH.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_chh_fcf_margin_pct`（q2_moat）｜CHH FCF 利潤率＝7.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CHH.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wh_operating_margin_pct`（q2_moat）｜WH 營業利益率＝36.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wh_fcf_margin_pct`（q2_moat）｜WH FCF 利潤率＝30.57 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.81 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.9 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝6.09 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7722.09 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc`（q4_capital）｜SBC（占營收）＝0.63 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi8`（q1_business）｜資本回饋＝147 US$M（Q3 買回）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.hyatt.com/news/investor-news/news-details/2026/Hyatt-Reports-Third-Quarter-2026-Results/default.aspx（EX-99.1: https://www.sec.gov/Archives/edgar/data/0001468174/000146817426000029/q32026earningsrelease.htm）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝4153.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 4648.0、現金 495.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝93.39 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.319 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝49.31 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.81，分子＝快照價 187.89｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝187.89 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝97.86 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.4 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.67 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.04 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝21700.06 USD m｜期間與口徑：2026-11-03／市值 17547.06 ＋ 淨負債 4153.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.82 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（4.86 → 4.9）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.67 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 3.64 → 3.81（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝70.01｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝18.28 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 186.55 / W52 168.63 / W104 154.53 / W250 130.94 / W250 13週斜率 1.06%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝168.63 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝154.53 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出的競爭來源包含新分銷管道（潛在 AI 平台）、Alibaba、Google、信用卡發行商及 Airbnb/Vrbo 等短租，並指出部分對手規模與會員數大於 Hyatt。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素提及產業整併，若競爭對手整併可能使 Hyatt 失去份額或難以吸引業主與加盟商。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Colliers 2026 展望引 Green Street：2026 美國前 50 市場住宿需求成長 1.3%，低於 2006-2019 年均 2%。
  - 來源：Colliers 2026 U.S. Hospitality Outlook via Hotel Management（as_of 2026-01-15）｜affects：moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Hyatt 10-K 風險因素列出國際營運風險包括進出口許可要求與未預期的法規變動，含關稅、禁運、出口管制與其他貿易限制（一般性風險揭露，未量化）
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Skift 報導 2026 年 2 月全球關稅政策急變讓部分飯店營運商及其供應商感到混亂（產業層級，非 Hyatt 專屬）
  - 來源：Skift, Hoteliers Scramble to Price U.S. Tariff Risk（as_of 2026-02-23）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026：中東衝突使系統整體 RevPAR 成長少 1.1 個百分點（原為 +5.9%）；CFO 預期中東酒店收入明顯低於去年，全年費用收入約減 $10 百萬
  - 來源：eGlobalTravelMedia / panabee 轉述 Hyatt Q2 2026 業績（as_of 2026-08-03）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Hyatt 2026 前瞻聲明列出中東軍事衝突與墨西哥安全問題為影響旅遊的因素，風險因素亦提及貿易政策與關稅
  - 來源：Hyatt Form S-3ASR 2026（as_of 2026-06-30）｜affects：decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：核心營運依賴第三方或雲端供應商的 IT 服務，並可能受軟體供應鏈事件影響
  - 來源：Hyatt FY2025 Form 10-K（as_of 2026-02-20）｜affects：decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：全包式度假村（Distribution 段）Net Package RevPAR -2.5%，主因墨西哥需求下滑；颶風 Melissa 關閉牙買加飯店，Distribution 段 Adjusted EBITDA 下滑；預期 Q4 Net Package RevPAR 回正
  - 來源：Hyatt Q3 2026 earnings release (SEC 8-K)（as_of 2026-10-29）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Hyatt 10-K 風險因子：生成式 AI 工具與 LLM（ChatGPT、Claude、Gemini 等）決定提供何種資訊的方式，可能使 Hyatt 物業獲得的關注減少；資訊不準確也可能損及品牌聲譽。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Hyatt 10-K：自家 AI 部分依賴第三方授權 AI 技術，無法控制其可得性與定價；若不相容或不可用，其方案吸引力下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：10-K 明列新分銷通路（含潛在 AI 平台）可能對業務造成負面影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：Distribution 分部 2025 年營收 $946M，較 2024 年 $1,023M 下降 7.5%。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-13）｜affects：valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 後多家券商下調目標價（Morgan Stanley、Barclays、Baird、Deutsche Bank，據 StockAnalysis）。
  - 來源：StockAnalysis（搜尋摘要）（as_of 2026-08-01）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":332.8,"bear_5y_price":95.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":23.6,"ev5y_pct":12.4,"irr_base_pct":4.3,"asym_ratio":1.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.81,"pe":49.31,"basis":"FY2026 共識 EPS 3.81 美元（財年 12 月，判斷日距年底約兩個月，視同當年口徑）；終端倍數同樣套在 FY2031 當年 EPS，分母同口徑。同業前瞻本益比事實表未涵蓋，終端倍數以 Hyatt 自身 FY2028 隱含 30.9 倍與 EV/EBITDA 約 18 倍對照"},"eps":{"bull":[5.0,6.3,7.55,8.9,10.4],"base":[4.8,5.75,6.65,7.6,8.6],"bear":[4.25,3.9,4.05,4.4,4.75]},"pe":{"bull":32,"base":27,"bear":20},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.319,"net_buyback":1.8},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### H_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joan Bottarini｜guidance：全年系統 RevPAR 成長財測上調至 3.5%–4.5%（原話："increasing our full year system-wide RevPAR growth outlook"）
- 2026-07-30｜Joan Bottarini｜guidance：全年美國 RevPAR 成長預期 3%–4%（原話："RevPAR growth in the United States of between 3% and 4%."）
- 2026-07-30｜Joan Bottarini｜guidance：全年 gross fees 財測維持，成長 9%–11%、1.305–1.335 十億美元（原話："grow between 9% to 11% in the range of $1.305 billion"）
- 2026-07-30｜Joan Bottarini｜guidance：全年調整後 EBITDA 財測維持，成長 13%–18%、1.155–1.205 十億美元（原話："13% to 18% in the range of $1.155 billion to $1.205 billion"）
- 2026-07-30｜Joan Bottarini｜guidance：調整後自由現金流財測維持，EBITDA 轉換至少 50%（原話："adjusted free cash flow of at least 50% for the full year"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：全年股東回報（回購加股息）預期 3.25–3.75 億美元（原話："$325 million and $375 million of capital to shareholders"）
- 2026-07-30｜Joan Bottarini｜guidance：第三季全球 RevPAR 預期落在全年區間低端（原話："global RevPAR growth towards the low end of our full year"）
- 2026-07-30｜Joan Bottarini｜guidance：第三季 net package RevPAR 預期略低於去年（原話："net package RevPAR to be moderately below last year."）
- 2026-07-30｜Joan Bottarini｜guidance：全年淨增房數約 6%，轉換案帶動（原話："approximately 6% for the full year, with momentum in"）
- 2026-07-30｜Mark Hoplamazian｜guidance：全年淨增房數區間下調，Q4 開幕部分可能延到 2027（原話："quarter openings, some of which could slip into 2027."）
- 2026-07-30｜Mark Hoplamazian｜commitment：管理層表示對 Investor Day 所述有機成長的信心很高（原話："I want to be clear, our confidence in delivering on"）
- 2026-07-30｜Mark Hoplamazian｜capital_allocation：Hyatt Grand Central New York 出售預期不會在 2026 年完成（原話："we no longer expect the transaction to"）
- 2026-07-30｜Mark Hoplamazian｜capital_allocation：持續洽談出售部分自有資產（原話："assets to unlock additional value from our owned portfolio."）
- 2026-07-30｜Joan Bottarini｜risk：中東飯店營收明顯低於去年，估計全年費用減少約 1,000 萬美元（原話："will reduce full year fees by approximately $10 million."）
- 2026-07-30｜Joan Bottarini｜risk：墨西哥 all-inclusive 訂房復甦不如預期，對費用影響約 1,500 萬美元（原話："resulting in an approximately $15 million impact to fees"）
- 2026-07-30｜Joan Bottarini｜risk：中東 RevPAR 年減 36%（原話："RevPAR in the Middle East declined by 36%"）
- 2026-07-30｜Joan Bottarini｜margin：世界盃對美國 RevPAR 成長的貢獻約 70 個基點（原話："contributed approximately 70 basis points of RevPAR growth"）
- 2026-07-30｜Joan Bottarini｜margin：第二季 gross fees 年增 8% 至 3.24 億美元（原話："Gross fees increased 8% to $324 million"）
- 2026-07-30｜Joan Bottarini｜margin：自有及租賃部門調整後 EBITDA 還原資產出售後成長 16%（原話："owned and leased segment adjusted EBITDA increased by 16%"）
- 2026-07-30｜Joan Bottarini｜margin：第二季調整後 EBITDA 還原資產出售後年增約 9%（原話："approximately 9% year-over-year after adjusting for"）
- 2026-07-30｜Joan Bottarini｜risk：分銷部門受 4 星級客群需求偏弱影響（原話："lower demand for 4-star properties"）
- 2026-07-30｜Joan Bottarini｜margin：分銷部門全年 EBITDA 預期較 2025 年減少約 2,500 萬美元（原話："$25 million year-over-year decline in our Distribution"）
- 2026-07-30｜Joan Bottarini｜margin：成長數字已調整 JV 按比例 EBITDA 的新定義，口徑為扣除 1,300 萬美元（原話："$13 million of pro rata JV EBITDA removed under our updated"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：年初至今以回購與股息回報約 1.75 億美元（原話："we've returned approximately $175 million to"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：回購授權餘額約 15 億美元（原話："approximately $1.5 billion remaining under our"）
- 2026-07-30｜Joan Bottarini｜commitment：重申維持投資等級信用（原話："We remain committed to our investment-grade profile"）
- 2026-07-30｜Joan Bottarini｜capital_allocation：Q2 回購金額偏低，原因為 Investor Day 期間的禁止交易期（原話："we were locked out for Investor Day for a period of time"）
- 2026-07-30｜Mark Hoplamazian｜risk：部分轉換案因 PIP 比原先模型更重而延後（原話："turned out to be heavier than we initially had modeled"）
- 2026-07-30｜Mark Hoplamazian｜risk：已見到開幕從 Q2 延到 Q3、Q3 延到 Q4（原話："we've seen slippage from Q2 to Q3 and Q3 to Q4 already."）
- 2026-07-30｜Mark Hoplamazian｜risk：約半數管線開幕集中在第四季（原話："our pipeline openings are in the fourth quarter."）
- 2026-07-30｜Mark Hoplamazian｜commitment：管理層稱淨增房數不是價值驅動，淨費用成長才是（原話："You can't take net rooms growth to the bank."）
- 2026-07-30｜Mark Hoplamazian｜product：與 Hall Financial 設立 5 億美元融資工具，Hyatt 提供部分信用支持（原話："We provided some credit support in that facility."）
- 2026-07-30｜Mark Hoplamazian｜commitment：對 Investor Day 提出的 6%–8% 淨增房數區間表示有信心（原話："the 6% to 8% range that we gave during Investor Day"）
- 2026-07-30｜Joan Bottarini｜commitment：管理層預期 9%–11% 的費用複合成長率（原話："the 9% to 11% compounded rate over the next couple of years"）
- 2026-07-30｜Joan Bottarini｜margin：新品牌每房費用較低，對費用有稀釋作用（原話："will be dilutive because of the fees per room"）
- 2026-07-30｜Mark Hoplamazian｜customer：團體訂房窗口沒有明顯改變（原話："booking window with respect to group hasn't really changed."）
- 2026-07-30｜Joan Bottarini｜guidance：美國全服務飯店下半年團體預訂 pace 為中個位數成長（原話："U.S. full-service hotels up in the mid-single"）
- 2026-07-30｜Joan Bottarini｜guidance：2027 年第一季該區域 pace 為高個位數成長（原話："the Q1 pace is up in the high"）
- 2026-07-30｜Joan Bottarini｜customer：2027 Q1 多明尼加 pace 成長逾 20%（原話："The Dominican in particular, is up over 20%."）
- 2026-07-30｜Joan Bottarini｜customer：Cancun 復甦程度不如預期（原話："improving, but not as much as we had anticipated."）
- 2026-07-30｜Joan Bottarini｜risk：全包式飯店 net package RevPAR 第二季年減 1.2%（原話："RevPAR in our all-inclusive portfolio declined 1.2%"）
- 2026-07-30｜Joan Bottarini｜guidance：下半年 EBITDA 預期有強勁假設，Q4 加速（原話："But there is a strong back half EBITDA assumption there."）
- 2026-07-30｜Joan Bottarini｜guidance：下半年美國財測對休閒與商務能見度較低，可能有保守成分（原話："probably some conservatism there"）
- 2026-07-30｜Mark Hoplamazian｜customer：奢華與休閒在各區域持續領先（原話："Luxury was the highest RevPAR growth with the highest ADR"）
- 2026-07-30｜Mark Hoplamazian｜customer：中國奢華飯店 RevPAR 本季成長 11%（原話："China luxury properties were up 11% this past quarter"）
- 2026-07-30｜Mark Hoplamazian｜competition：奢華與生活風格飯店上半年 RevPAR 指數提升近 3 點（原話："lifestyle portfolios increased RevPAR index by nearly 3"）
- 2026-07-30｜Mark Hoplamazian｜customer：World of Hyatt 會員約 6,900 萬、年增 17%（原話："approximately 69 million members, an increase of 17%"）
- 2026-07-30｜Mark Hoplamazian｜product：開發管線創紀錄，約 15.4 萬間、年增 10%（原話："development pipeline of approximately 154,000 rooms, up 10%"）
- 2026-07-30｜Mark Hoplamazian｜customer：休閒 transient RevPAR 年增約 7%（原話："transient RevPAR increasing approximately 7%"）
- 2026-07-30｜Mark Hoplamazian｜customer：商務 transient RevPAR 年增約 2%（原話："business transient RevPAR increasing approximately 2%"）
- 2026-07-30｜Mark Hoplamazian｜competition：管理層稱系統成本與最大對手相比具競爭力（原話："highly competitive, if not at a cost advantage to our"）
- 2026-07-30｜Mark Hoplamazian｜product：PMS 每房成本對業主下降 40%（原話："our PMS cost to owners has been reduced by 40%"）
- 2026-07-30｜Mark Hoplamazian｜commitment：已取消所有新開幕飯店的 IT 實施費（原話："we've removed IT implementation fees for all new"）
- 2026-07-30｜Mark Hoplamazian｜product：開發大型 AI 平台為團體業務評分（原話："a large-scale AI platform to actually score and"）
- 2026-07-30｜Mark Hoplamazian｜product：與 Dossen 簽署 Hyatt Select 中國大陸 master franchise 協議（原話："a master franchise agreement with Dossen Group"）
- 2026-07-30｜Mark Hoplamazian｜risk：UrCove 組合有部分飯店租約到期造成流失，租約約 10 年（原話："These lease deals tend to be 10 years in length."）
- 2026-07-30｜Mark Hoplamazian｜competition：交易市場焦點在高進入門檻市場的優質物業（原話："to-entry markets is what is garnering the most attention"）
- 2026-07-30｜Mark Hoplamazian｜guidance：特許加盟占比預期未來兩年不會顯著上升，五年後才明顯（原話："we will see franchise increase as a percentage of the total"）
- 2026-07-30｜Mark Hoplamazian｜customer：美國下半年比較基期受去年 Liberation Day 影響（原話："Liberation Day hit at the very beginning of the second"）

### H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md
- 2026-05-28｜CFO｜guidance：CFO 給 2025–2028 全球系統 RevPAR 複合成長區間 2%–4%（原話："RevPAR could grow at a compounded rate of between 2% and 4%"）
- 2026-05-28｜CFO｜guidance：淨房數成長 2028 前年複合 6%–8%（原話："rooms to grow at a compounded rate of 6% to 8%"）
- 2026-05-28｜CFO｜guidance：2025–2028 總費用（gross fees）三年複合成長 9%–13%（原話："a very strong 3-year compounded growth rate of between 9%"）
- 2026-05-28｜CFO｜guidance：調整後 EBITDA 2028 前三年複合成長 11%–16%（原話："3-year compounded rate of 11% to 16% through 2028"）
- 2026-05-28｜CFO｜guidance：調整後自由現金流複合成長 14%–18%（原話："compounded rate of between 14% to 18%"）
- 2026-05-28｜CFO｜margin：調整後 EBITDA 轉自由現金流轉換率約 55%，與 2022–2025 平均一致（原話："conversion of 55%, consistent with what we have delivered"）
- 2026-05-28｜CFO｜guidance：調整後 G&A 三年複合成長 2%–3%（原話："adjusted G&A to grow at a 3-year rate of between 2% to 3%"）
- 2026-05-28｜CFO｜guidance：Distribution 分部調整後 EBITDA 較 2025 年複合成長 2%–4%（原話："we expect adjusted EBITDA to grow between 2% and 4%"）
- 2026-05-28｜CFO｜guidance：key money 年均 1.5–1.7 億美元（原話："key money to average around $150 million to $170 million"）
- 2026-05-28｜CFO｜guidance：CapEx 年均 1.35–1.4 億美元，並預期之後下降（原話："CapEx to be between $135 million and $140 million per year"）
- 2026-05-28｜CFO｜guidance：有效稅率 27%–30%（原話："effective tax rate to be between 27% and 30%"）
- 2026-05-28｜CFO｜guidance：2026–2028 累計自由現金流 20–22 億美元（原話："between $2 billion and $2.2 billion of free cash flow"）
- 2026-05-28｜CFO｜capital_allocation：2028 年底前可增加 2–5 億美元負債並維持投資級（原話："capacity to increase our debt in the range of $200"）
- 2026-05-28｜CFO｜commitment：承諾維持投資級信用輪廓（原話："We remain committed to an investment-grade profile."）
- 2026-05-28｜CFO｜commitment：資產輕型盈餘占比 2028 年底可達 95%（原話："with the potential to increase to 95% by the end of 2028"）
- 2026-05-28｜CFO｜capital_allocation：董事會當天宣布庫藏股授權增加 10 億美元（原話："Board has authorized a $1 billion increase in our share"）
- 2026-05-28｜CFO｜capital_allocation：2022 年以來現金運用，回饋股東占比逾九成（原話："we've returned $2.1 billion or over 90% of"）
- 2026-05-28｜CFO｜capital_allocation：多餘現金優先走庫藏股（原話："we're going to return it through share repurchases"）
- 2026-05-28｜CFO｜capital_allocation：自有／租賃資產組合估值 22–25 億美元（原話："portfolio is valued between $2.2 billion and $2.5 billion"）
- 2026-05-28｜CFO｜capital_allocation：估值倍數 18–20 倍 2025 調整後 EBITDA（原話："multiple of 18x to 20x 2025 adjusted EBITDA"）
- 2026-05-28｜CFO｜commitment：持續評估減持自有飯店，無必持有之店（原話："there are no hotels we must own"）
- 2026-05-28｜CFO｜capital_allocation：三項特殊投資約 7 億美元，不含在 2028 展望內（原話："valued at about $700 million"）
- 2026-05-28｜CFO｜guidance：展望前提：總經成長穩定（原話："growth remains stable and consistent between now and 2028"）
- 2026-05-28｜CFO｜guidance：費用結構假設：九成獎勵費來自美國以外（原話："Today, 90% of our incentive fees are"）
- 2026-05-28｜CFO｜risk：CFO 稱 2026 年 Distribution 的干擾（颶風、墨西哥）屬暫時（原話："The disruptions in 2026, we believe are temporary."）
- 2026-05-28｜CEO｜commitment：CEO 稱展望 100% 以有機成長為基礎，併購為額外加成（原話："is all based on organic growth, period, end of story"）
- 2026-05-28｜CEO｜capital_allocation：併購不是第一優先（原話："nor is it our #1 priority"）
- 2026-05-28｜CEO｜guidance：展望內含的有機成長中，轉換型占約 35%–40%（原話："35% and 40% per year of conversions"）
- 2026-05-28｜CEO｜risk：新建案開幕過去較為遲緩（原話："new-build openings have been relatively more sluggish"）
- 2026-05-28｜CEO｜capital_allocation：正尋找銀行以外的非銀行融資管道（原話："we're looking for non-bank financial institutions"）
- 2026-05-28｜CEO｜risk：資本形成仍是問題，故轉換案是 6–8% 區間的關鍵（原話："capital formation remains an issue"）
- 2026-05-28｜CEO｜guidance：CEO 對 8% 高標不給保證，路徑取決於轉換加速（原話："we know for sure we're going to hit 8%"）
- 2026-05-28｜Laurie Blair｜commitment：擴大信用卡：未來 12–24 個月推出多張國際聯名卡（原話："several co-branded cards internationally"）
- 2026-05-28｜Laurie Blair｜guidance：信用卡與第三方費用 EBITDA 貢獻明年增逾一倍（原話："than double the EBITDA contribution from our credit card"）
- 2026-05-28｜CFO｜guidance：CFO：新卡擴張不在展望內，屬上行空間（原話："that will be upside to our outlook"）
- 2026-05-28｜CEO｜margin：CEO：資產輕型模式使利潤率擴張（原話："our asset-light model will enable margin expansion"）
- 2026-05-28｜CEO｜margin：CEO 對忠誠度滲透率口徑：滲透率高但利潤差「是愚蠢」（原話："with worse margins is idiotic"）
- 2026-05-28｜CEO｜margin：管理層改以淨房價實現率與利潤率為重點指標（原話："we are increasingly focused on net room realization"）
- 2026-05-28｜CEO｜margin：強調費用（美元）而非淨房數成長（原話："Net rooms growth doesn't create dollars."）
- 2026-05-28｜CEO｜competition：暗指同業部分淨房數成長是空熱量（原話："net rooms growth that's being reported is empty calories"）
- 2026-05-28｜Chief Commercial Officer｜competition：滲透率計算口徑與同業不同，不願同口徑比較（原話："we think about penetration through the owner lens"）
- 2026-05-28｜Chief Commercial Officer｜competition：Vondrasek 稱同口徑下差距遠小於近 50%（原話："we're a heck of a lot closer than"）
- 2026-05-28｜CEO｜competition：不進入輕經濟型與經濟型級距（原話："We're not in the lower mid-scale economy"）
- 2026-05-28｜CEO｜customer：約 70% 房晚經由 Hyatt 直銷管道（原話："70% of our room nights are booked through Hyatt's direct"）
- 2026-05-28｜Laurie Blair｜customer：自上次投資人日以來會員基數成長 78%（原話："our membership base has grown by 78%"）
- 2026-05-28｜CEO｜customer：Hyatt 客人每住一次花費高於同業 25%（原話："Hyatt guests spend over 25% more per stay"）
- 2026-05-28｜CEO｜risk：美國旅遊需求在不同收入層近期變異加大（原話："U.S. travel demand has recently shown more variability"）
- 2026-05-28｜CEO｜customer：科技業客戶迄今未見下滑（原話："We haven't seen a decline from that area to date."）
- 2026-05-28｜CEO｜product：Hyatt Select 首批物業在宣布後 8 個月開業（原話："first properties opened only 8 months after announcing"）
- 2026-05-28｜CEO｜product：Essentials 簽約量近期年增約 80%（原話："for essentials rooms were up approximately 80%"）
- 2026-05-28｜CEO｜customer：Essentials 簽約中 85% 為新業主（原話："85% of those signings are with new owners"）
- 2026-05-28｜CEO｜guidance：自 2017 年以來有機淨房數年均成長 7%（原話："Our organic net rooms growth was 7%"）
- 2026-05-28｜Chief Commercial Officer｜product：自 IDeaS 營收管理系統的營收提升（原話："has already delivered a 1.4%"）
- 2026-05-28｜Chief Commercial Officer｜product：意圖式搜尋轉換率提升 23%（原話："a 23% lift in conversion of intent-based search"）
- 2026-05-28｜Chief Commercial Officer｜product：ChatGPT 整合目前量體不大（原話："there is not a ton of volume here yet"）
- 2026-05-28｜Chief Commercial Officer｜competition：預期未來分銷轉向代理式 AI，直連意圖與訂房（原話："there won't be funnel, it will be a direct connect"）
- 2026-05-28｜CEO｜margin：AI 客服中心已省下數百萬美元並讓利給業主（原話："We took millions of dollars out of the"）
- 2026-05-28｜CEO｜commitment：AI 投資不會加到系統基金（原話："investments that we've been making in AI are not additive"）
- 2026-05-28｜Amar Lalvani｜product：Lifestyle 模式不需要增加人力或資本（原話："does not require additional headcount or additional capital"）
- 2026-05-28｜Javier Aguila｜customer：全包式渠道自有管道占 60% 銷售（原話："60% of our sales come from our internal channels"）
- 2026-05-28｜Javier Aguila｜competition：Inclusive 為該區隔最大營運商（原話："we are the largest in the segment"）
- 2026-05-28｜Javier Aguila｜risk：中東拓展須待地緣政治穩定（原話："we need to wait until the geopolitical situation stabilizes"）
- 2026-05-28｜CEO｜product：2.3 百萬間的全球可拓展房數（原話："We've identified approximately 2.3 million"）

### 問答異常語氣（迴避／改口／保留）
- H_Q2_2026_Earnings_Call_20260730.md｜問：Chaiken：Q4 開幕集中，是否已預先把部分房數移到 2027｜答法：先談兩年累計與 8 年有機成長、改強調費用成長而非房數，之後才說部分開幕可能延到 Q1
- H_Q2_2026_Earnings_Call_20260730.md｜問：Politzer：2027 淨增房數是否至少落在 6%–8% 區間中點或以上｜答法：回答 yes 後轉向歷史數據與管線，未給 2027 具體數字
- H_Q2_2026_Earnings_Call_20260730.md｜問：Montour：美國全年 3%–4% 隱含下半年明顯放緩，多少為保守｜答法：承認有保守成分，但未量化
- H_Q2_2026_Earnings_Call_20260730.md｜問：Duane：Q4 EBITDA 加速的驅動因素｜答法：列舉質化因素（颶風基期、G&A、Playa 季節性），未給金額
- H_Q2_2026_Earnings_Call_20260730.md｜問：Grambling：Dossen 與 Home Inns 協議的版稅率比較、UrCove 流失是否一次性｜答法：說明模式與租約年限，未回答版稅率，亦未明確回答是否為一次性，被時間打斷
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Barclays：6–8% 再加速中，Essentials、轉換、新建各占多少｜答法：回答只給轉換案占 35–40%，未拆 Essentials 比重數字，改談區域差異與新建融資管道
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：JPMorgan：忠誠度滲透率約 49–50% 對比同業 65–70%，如何追上｜答法：質疑同業計算口徑，稱同口徑下「遠較接近」但不給調整後數字，並改談淨房價與利潤率
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Baird：key money 1.5–1.7 億如何得出，新建與轉換、新增與防守各占多少｜答法：只答以現有合約加緩衝與小幅成長，未拆分新建／轉換或防守占比
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Morgan Stanley：代理式 AI 對分銷、忠誠度成本及系統基金（同業降低提撥）影響｜答法：談分銷趨勢與免收啟動費用，未回答系統基金提撥率是否調降，僅稱 AI 投資不另加系統基金
- H_Analyst_Investor_Day_Hyatt_Hotels_Corporation_20260528.md｜問：Deutsche：Distribution 2–4% 為何不能回到 2024 水準｜答法：回答回到 2025 水準並略高，未直接回應 2024 水準，稱可能有上行

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 5 | 2 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 4 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_concentration_credit**（not_applicable）：Hyatt Hotels 10-K customer concentration no single customer significant portion of revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260520","verdict":"B（觀望偏進場；品質 A + asset-light 90% + 66M loyalty +18% + Pipeline 151K 新高，但 Fwd PE 34.8x 已 priced in 完整復甦，5Y PEG 2.05 接近警示；建議等 Fwd PE&lt;28x 或股價回測 W52 $151）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Lodging cycle 不在 2026-27 反轉，RevPAR 維持 +2-5% YoY","columns":{"2Y 驗證點":"2026 全年 RevPAR YoY +2-4% 達標 + 2027 H1 RevPAR YoY 仍 &gt; 0","5Y 驗證點":"2028-2030 跨完整 cycle 平均 RevPAR YoY +2-3%","10Y 驗證點":"2030+ 跨多次 cycle 全週期 RevPAR CAGR &gt; +2%","具體數字門檻":"FY26 guide 2-4%；下方 floor 連 2 季 YoY &lt; -2% → 反轉","信息來源":"Q1 26 8-K + FY26 mgmt guidance + STR Lodging report","漂移觸發":"連 2 季 RevPAR YoY &lt; 0 → 削弱；連 3 季 &lt; -2% → 反轉"}},{"id":"H2","text":"Loyalty + Pipeline 飛輪持續加速，Active Members &gt; 100M by FY28","columns":{"2Y 驗證點":"2026-27 World of Hyatt 會員 YoY +15%+；US Pipeline signings 連 4 季 +20%+","5Y 驗證點":"FY30 會員達 110M+；Pipeline 200K+ rooms","10Y 驗證點":"FY35 會員 150M+；luxury portfolio 全球 dominant","具體數字門檻":"Q1 26 66M 會員 +18%；下方 floor 連 2 季 YoY +10%","信息來源":"Q1 26 earnings release + Investor Day 2024-25","漂移觸發":"會員 QoQ 增量首次轉負 → 削弱；連 2 季 &lt; +10% → 反轉"}},{"id":"H3","text":"Asset-light 達 90%+ by 2026 完成；FY28 fee revenue 占 EBITDA 90%","columns":{"2Y 驗證點":"FY26 Q4 asset-light 80%+ → 90% transition；Playa 持續管理合約 $60-65M 增量 EBITDA","5Y 驗證點":"FY28 fee revenue 占 EBITDA 90%+","10Y 驗證點":"FY30 Hyatt 完全轉型為「hospitality brand manager」","具體數字門檻":"FY26 guide 90% asset-light；下方 floor 88%","信息來源":"Skift 2026/02 報導 + Q1 26 supplementary","漂移觸發":"asset-light 占比連 2 季 &lt; 85% → 削弱；&lt; 80% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"消費衰退觸發 — RevPAR YoY 轉負，corporate travel demand 下降","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"STR US Lodging RevPAR YoY、Conference Board CCI、ISM Services PMI","警戒閾值":"連 2 季 RevPAR YoY 轉負；CCI &lt; 90；ISM Services &lt; 50"}},{"id":"R2","text":"Margin gap 擴大 — Marriott / Hilton 規模 + technology spending 拉大領先","columns":{"對應假設":"H2 + H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"MAR/HLT vs H Adj EBITDA margin gap; H technology spending / Rev","警戒閾值":"Adj EBITDA margin gap 從當前 5pp 擴大至 &gt; 8pp 連 2 年"}},{"id":"R3","text":"估值倍數結構性壓縮 — 市場對 asset-light premium 重設預期","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Forward PE multiple vs MAR/HLT；EV/EBITDA multiple convergence","警戒閾值":"Fwd PE 跌至 25x（-28% 倍數壓縮）or EV/EBITDA &lt; 18x"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":164.4,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"H","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Hyatt Hotels Corporation"},"oneliner":"Hyatt 的費用引擎與開發 pipeline 都在加速，但股價半年漲 18%，FY2027 共識 38 倍已先反映 25% 以上的盈餘成長。論點完整，價格沒有留安全邊際，等 155 美元以下再談建倉。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/scenario.json","answers":{"q1_business":{"verdict":"Hyatt 賺的是業主付的費用：把高端品牌、會員與訂房系統授權給業主，按飯店營收與利潤抽管理費與加盟費。錢卡在「誰握有訂房入口」這一節點，目前約七成房晚走 Hyatt 直銷；這一節守得住，費用就能維持雙位數成長。","reasoning":"營收結構：Q3 2026 報表營收 17.43 億美元，其中 gross fees 3.27 億（年增 15.2%），調整後 EBITDA 2.95 億，GAAP 淨利 0.58 億。全年 gross fees 指引 13.2～13.35 億（2026-10-29 CFO），約占 FY2026 共識營收 71.4 億的 19%，其餘為自有與租賃飯店、Distribution 及其他非費用營收；分部營收事實表未拆。TTM 毛利率 20.1%、營業利益率 7.2%，報表利益率被非費用營收稀釋，看獲利能力要看費用與調整後 EBITDA。成長來源：Q3 系統可比 RevPAR +7.2%，約八成來自房價；pipeline 約 15.8 萬間，年增 12%。單點依賴：10-K 載明沒有單一重要客戶。集中點在兩處，一是通路（直銷約七成，2026-05-28 投資人日 CEO），二是全包式事業的墨西哥 Riviera Maya（約占全包式三分之一強，2026-10-29 CEO）。景氣位置屬擴張期（II）：美國供給成長約 0.6%～1.3%、在建量 12 年低；需求成長 1.3% 低於歷史均值，RevPAR 靠房價推動。供需持久性：供給面屬結構性、偏持久；需求面屬週期性。景氣反轉時，壓力會先出現在房價，而不是供給過剩。","fact_refs":["f_kpi0_gaap_total_revenues","f_kpi1_adjusted_ebitda_recast","f_kpi2_gross_fees","f_kpi3_gaap_hyatt","f_kpi5_comparable_system_wide_r","f_kpi6_pipeline","f_peer_h_gross_margin_pct","f_peer_h_operating_margin_pct","f_rev_consensus_fy1_m"],"verdict_values":{"revenue_quality":"以費用收入為主，合約約 20 年，經常性高，且隨 RevPAR 放大。GAAP 淨利受資產出售與一次性項目干擾大（稀釋 EPS 2024 年 12.65 美元、2025 年 −0.55 美元），判讀以費用與調整後 EBITDA 為準。","unit_econ_note":"新增一間管理或加盟房，主要投入是 key money（管理層預估每年 1.5～1.7 億美元，2026-10-29 CEO）。管理層稱 pipeline 的每房費用高於在營飯店。中高價位新品牌單房費用較低，但多數落在 Hyatt 原本沒有據點的市場。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"輕資產費用模式疊加 RevPAR 週期槓桿"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性：供給面屬結構性、偏持久。美國供給成長 2026 年約 1.2%、2027 年約 0.6%～1.3%，在建量為 12 年低點，在建專案年減 4.9%（CoStar、Lodging Econometrics）。需求面屬週期性：前 50 大市場 2026 年需求成長 1.3%，低於 2006–2019 年均 2%（Green Street）。RevPAR 靠房價推動，景氣反轉時會先反映在房價。","bargaining":{"up":"上游是業主與開發商。key money 需求升高，新建案融資仍緊（2026-05-28 CEO：資本形成仍是問題），議價力偏向業主。","down":"下游是住客與企業客戶，沒有單一重要客戶（10-K）。高端客群對房價容忍度高；OTA 與 AI 平台可能分走通路利潤。","geo":"2026 年兩個壓力區：墨西哥坎昆（坎昆需求年減逾 10%）與中東（國際入境年減 40%）。兩地合計使全年費用減約 3,000 萬美元（2026-10-29 CFO）。"},"profit_pool_dir":"高端與休閒市場的利潤池往品牌與會員規模大的業者集中；分銷段的利潤可能流向 AI 平台，方向未定。","tam_table":[{"item":"可拓展房數（管理層辨識）","value":"約 230 萬間（2026-05-28 投資人日 CEO）"},{"item":"開發 pipeline","value":"約 15.8 萬間，年增 12%（Q3 2026）"},{"item":"淨增房數目標","value":"2026–2028 年複合 6%～8%；Q3 2026 為 3.9%（不含 Playa）"},{"item":"美國產業供給成長","value":"2026 年約 1.2%，2027 年約 0.6%～1.3%（CoStar、Lodging Econometrics）"},{"item":"滲透率與利潤池占比","value":"事實表未涵蓋現有系統房數與產業營業利益池，無法計算滲透率，也無法對比五年前"}]}}},"q2_moat":{"verdict":"護城河方向判穩定（→）。高端品牌組合與 World of Hyatt 會員讓 Hyatt 在競爭組中持續拿到市占與房價指數；但報表利益率只有同業一半左右，代理式 AI 分銷入口也還沒定局，所以不標擴大。","reasoning":"機制：高端品牌與會員讓業主拿到較高的 RevPAR，Hyatt 以此換取長約與費用。執行力判擴大：年初至今市占 +100bp、房價指數上升（2026-10-29 CEO），坎昆全包式市占 +400bp（CFO），簽約量 +70%、動工 +40%，會員 7,200 萬、年增 19%。定價力判穩定：房價貢獻約八成 RevPAR 成長，管理層稱 pipeline 每房費用高於在營飯店；但業主端 key money 競爭激烈（CEO：key money flying around）。同業只能比利益率：營業利益率 Hyatt 7.21%，MAR 15.73%、HLT 24.01%、CHH 25.52%、WH 36.38%；FCF 利益率 Hyatt 6.35%，MAR 11.64%、HLT 14.49%。差距有一部分來自 Hyatt 仍有自有飯店與 Distribution，一部分是規模。同業投入資本與 ROIC 事實表未涵蓋，無法驗證報酬差距方向，所以合併分不給到 8 分以上：執行力 8、定價力 7，等級 B。市占數據是公司自報，第三方報導也說沒有直接數據，因此不標擴大。AI 曝險：Hyatt 已在 ChatGPT 等平台建自有入口，這是接在自有資產上的強化；若代理式 AI 改經 OTA 或平台自家預訂完成訂房，就是繞過 Hyatt。管理層預期未來兩年代理式訂房成長很快，分界年抓 2028。再投資：增量報酬約 20%～35%，再投資率約 33%，內生成長上界約 10%。","fact_refs":["f_peer_h_operating_margin_pct","f_peer_h_fcf_margin_pct","f_peer_mar_operating_margin_pct","f_peer_mar_fcf_margin_pct","f_peer_hlt_operating_margin_pct","f_peer_hlt_fcf_margin_pct","f_peer_chh_operating_margin_pct","f_peer_chh_fcf_margin_pct","f_peer_wh_operating_margin_pct","f_peer_wh_fcf_margin_pct","f_kpi2_gross_fees","f_kpi6_pipeline"],"verdict_values":{"moat":{"mechanism":"高端、生活風格與全包式品牌組合，加上 World of Hyatt 會員與直銷管道，讓業主拿到較高的 RevPAR 與房價指數；Hyatt 以此換取約 20 年期的管理與加盟合約及費用。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：年初至今市占 +100bp、房價指數上升（2026-10-29 CEO），坎昆全包式市占 +400bp（CFO），簽約量 +70%、動工 +40%，會員 7,200 萬、年增 19%。定價力穩定：房價貢獻約八成 RevPAR 成長，pipeline 每房費用高於在營飯店，但業主端 key money 競爭激烈。兩者合併為穩定。市占數據為公司自報，第三方報導稱沒有直接的市占與定價數據，故不標擴大。","competitor_notes":[{"name":"MAR","strategy_note":"規模最大，營業利益率 15.7%、FCF 利益率 11.6%，都約是 Hyatt 的兩倍。Hyatt 靠高端組合與房價指數取勝，不靠規模。"},{"name":"HLT","strategy_note":"營業利益率 24.0%、FCF 利益率 14.5%，是輕資產模式的標竿。Hyatt 在 2028 年達成 95% 輕資產目標之前，利益率差距難以收斂。"},{"name":"CHH","strategy_note":"以中低價位加盟為主，營業利益率 25.5%，但 FCF 利益率只有 7.1%。Hyatt 的中高價位 Essentials 品牌進入新市場時，會與它正面競爭。"},{"name":"WH","strategy_note":"純加盟、以經濟型為主，營業利益率 36.4%、FCF 利益率 30.6%。Hyatt 不做中低階與經濟型（2026-05-28 CEO），兩者直接重疊有限。"}],"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，只能用報表營業利益率與 FCF 利益率比較。MAR 與 CHH 的 TTM 截至 2026-06-30，比 Hyatt 晚一季。","threats":[{"level":"🟡","text":"代理式 AI 與 LLM 平台成為新的分銷入口，可能降低 Hyatt 物業的曝光並抬高通路成本。目前經 LLM 完成的訂房「非常少」（2026-10-29 CEO），先列點對點威脅；直銷占比跌破 65% 時升級為生態攻擊。","p":30,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","channel_business_model_shift#1"]},{"level":"🟡","text":"自家 AI 部分依賴第三方授權技術，可得性與定價不受 Hyatt 控制，談判條件可能不利。","p":20,"evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"同業整併加上部分對手規模與會員數較大（10-K 自承），在爭取業主與 key money 上施壓，也可能使 Hyatt 失去份額。","p":25,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"level":"🟡","text":"Airbnb、Vrbo 等短租替代住宿，以及 Alibaba、Google、信用卡發行商這類新分銷參與者。","p":15,"evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"報表口徑為低利益率（營業利益率 7.2%），周轉率未知。費用收入約占營收 19%，以費用口徑推論屬高利益率×高周轉，但事實表沒有投入資本可以驗證。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"三種角色分開看：住客是使用者，企業差旅與會議主辦是決策者，付費者是住客與企業。Hyatt 的直接客戶是業主，業主要的是更高的 RevPAR 與融資可得性。業主需求強：2026 年初至今簽約 +70%、動工 +40%，pipeline 15.8 萬間創新高（Q3 2026 CEO）。終端住客需求屬可延後的消費，週期風險放在景氣假設處理。"},{"item":"決策層級","level":"🟡","text":"業主端的替換成本高：合約約 20 年，系統轉換「painful and arduous」（Q3 2026 CEO）。但新約與續約靠 key money 激烈競爭。住客端每趟都能換品牌，留存靠會員：會員 7,200 萬，年住 100 晚以上的會員自 2022 年增加近 40%。分析師引述會員滲透率約 49%～50%、同業 65%～70%；管理層質疑計算口徑，但沒有給同口徑數字（2026-05-28 投資人日）。"},{"item":"價值鏈分配","level":"🟡","text":"Hyatt 收費用，業主承擔不動產與營運風險，約七成房晚走 Hyatt 直銷（2026-05-28 CEO）。壓力來自兩端：業主要求更多 key money（每年 1.5～1.7 億美元），通路端的 AI 平台可能成為新的收費關卡（10-K 風險因子）。目前守住分配的證據是：高端組合每房費用較高，pipeline 每房費用高於在營飯店。"},{"item":"社會容忍度","level":"🟢","text":"飯店房價不受價格管制，旅客對高端房價上漲的容忍度高（房價貢獻約八成 RevPAR 成長）。加盟業務受 FTC 與各州加盟法規範，屬既有框架。Hyatt 被控透過 IDeaS 收益管理軟體交換價格資訊的私人反托拉斯集體訴訟，法院已先行駁回；但若演算法定價的監管收緊，收益管理工具會受影響。"}],"roiic":"代理值約 20%～35%（稅後）。2026 調整後 EBITDA 增量約 1.6 億美元（指引 11.7～12.0 億、年增 14%～17%，反推 2025 約 10.3 億），除以每年再投資約 3 億（key money 1.5～1.7 億＋資本支出 1.35～1.4 億），稅前約 53%；以稅率 27%～30% 換算，稅後約 38%。這個增量含 RevPAR 順風與 Playa 管理合約的貢獻，扣除後取 20%～35%。","reinvest_rate":"約 33%：每年再投資約 3 億 ÷（調整後 FCF 指引中值 6.05 億＋3 億）","endo_ceiling":10,"formula_note":"事實表沒有投入資本、折舊與營運資金，無法照（Capex−D&A＋ΔWC＋收購淨額）÷NOPAT 計算。改用 key money 加資本支出作為再投資，以調整後 FCF 加回再投資作為現金 NOPAT 的代理值。上界包含景氣順風，偏高。"}}}},"q3_growth":{"verdict":"5 年後的成長空間仍寬（🟢）。中高價位 Essentials 品牌進入 Hyatt 原本沒有據點的市場（美國簽約過半在新市場，pipeline 逾 150 家），是第二條成長曲線。但共識 EPS 年增約 26%，大半來自固定成本攤薄與回購，不是內生成長。","reasoning":"共識三年 EPS：FY2026 3.81、FY2027 4.90、FY2028 6.09 美元（Koyfin 快照；分析師家數事實表未載，營收共識為 20 位分析師），FY2026→FY2028 兩年年複合 26.4%。FY2025 GAAP 每股 −0.55 美元口徑不同，不作基期。共識營收 FY2026 71.4 億→FY2027 77.2 億，年增 8.1%。內生上界約 10%（增量報酬 20%～35% × 再投資率約 33%，推導見護城河段）。缺口約 16pp，可以歸因：①利益率擴張：EBITDA 下方的折舊與利息等成本相對固定，EBITDA 年增 11%～16%（投資人日 2025–2028 指引）就能撐出 20% 以上的 EPS 成長；這是推論，折舊與利息事實表未涵蓋。②淨回購約 2pp：2026 回饋指引 3.75～4.25 億，扣除股息後約占市值 2%。③2026～2027 的 RevPAR 景氣順風。缺口既然可歸因，就不屬於靠倍數重估撐起的成長。成長空間：管理層辨識約 230 萬間可拓展房數，Essentials 新品牌與國際 pipeline 構成第二條曲線，判 🟢。中高價位的單房費用較低，但管理層稱 pipeline 整體每房費用仍高於在營飯店。十項衰退信號亮 1 項（EPS 成長遠高於營收），長期成長性 🟡。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_pipeline","f_kpi2_gross_fees"],"verdict_values":{"growth":{"driver_mix":"量（淨增房數 2026–2028 年複合 6%～8% 目標）加價（RevPAR，投資人日指引 2025–2028 年複合 2%～4%），帶動費用年增 9%～13%；回購每年約 2%；併購不在展望內（2026-05-28 CEO：展望百分之百是有機成長）。","runway_years":"≥10 年（管理層辨識約 230 萬間可拓展房數、pipeline 15.8 萬間；現有系統房數事實表未涵蓋，滲透率無法計算）","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的再投資推導：增量報酬約 20%～35% × 再投資率約 33%，約 10%。事實表沒有投入資本，屬代理值。","segments":[{"item":"管理與加盟費用（gross fees）","value":"Q3 2026 為 3.27 億美元、年增 15.2%；FY2026 指引 13.2～13.35 億、年增 10%～11%"},{"item":"Distribution（全包式分銷與旅行社平台）","value":"2025 營收 9.46 億、年減 7.5%；2026 調整後 EBITDA 預期比 2025 少約 3,000 萬（Q3 法說 CFO）"},{"item":"自有與租賃","value":"Q3 調整後 EBITDA 還原資產出售後年減 1%；Grand Central 與數家物業仍在出售中"},{"item":"輕資產盈餘占比","value":"2026 年約 90%，2028 年底目標 95%（2026-05-28 投資人日 CFO）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率 19.6%→19.5%→19.7%，TTM 20.1%；季度數據事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱年初至今市占 +100bp（公司自報）"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q3 房價貢獻約八成 RevPAR 成長，未見入住率下滑的證據"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2027 共識 EPS +28.6%，共識營收 +8.1%，差 20pp；成因是 EBITDA 下方固定成本攤薄與回購"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2024 年為 0.36，但淨利含出售利得；2025 年淨利為負，比率失真，不構成連 2 年。改用調整後 FCF／EBITDA ≥50% 追蹤"},{"signal":"SBC／營收超過 5% 且逐年上升","lit":false,"note":"Q3 2026 為 0.63%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"尚未見到；代理式 AI 屬通路變動，列入風險監測"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋，屬資料缺口；Hyatt 自身倍數在年度端點最高位"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出 1.35～1.4 億，對調整後 FCF 5.8～6.3 億，約 23%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"pipeline 創新高；營收 2022–2025 由 58.9 億增至 71.0 億"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等。現金九成以上回饋股東，SBC 很低；但在 40～50 倍盈餘下回購，買入收益率偏低，收購報酬也無法驗證。報表與調整後自由現金流的口徑落差大，是要盯的地方。","reasoning":"現金轉換：年度報表 FCF／淨利，2022 年 1.04、2023 年 2.74、2024 年 0.36（淨利含資產出售利得），2025 年淨利為負、不具意義。2025 報表 FCF 1.59 億（利益率 2.2%）；公司 2026 調整後 FCF 指引 5.8～6.3 億、年增 20%～30%，反推 2025 調整後約 4.85 億。兩種口徑差約 3.3 億，原因事實表未涵蓋。SBC 占營收 0.63%，稀釋可以忽略。現金去向：每年再投資約 3 億（key money 1.5～1.7 億、資本支出 1.35～1.4 億）。2026 股東回饋指引 3.75～4.25 億（Q2 時為 3.25～3.75 億）；2022 年以來回饋 21 億，占現金運用逾九成。收購：2025 年收購 Playa，同年 12 月以約 20 億美元出售不動產，保留管理合約，並投資 2 億美元優先股給買方。Two Roads 收購價只有單一法文來源，由 4.8 億降至 4.05 億，未核原文、不計入。兩案的收購後報酬事實表都無法驗證。負債：總債務 46.48 億、現金 4.95 億，淨負債 41.53 億（含租賃口徑），約為 2026 調整後 EBITDA 指引中值的 3.5 倍；流動性約 18 億，公司承諾維持投資等級。三項評分：收購報酬無法驗證、回購買入收益率不通過、SBC 稀釋通過。","fact_refs":["f_kpi4_sbc","f_kpi8","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Playa（2025 年收購，同年 12 月出售不動產、保留管理合約）與 Two Roads 的收購總價、收購後 EBITDA 拆分，事實表未涵蓋，無法驗證已實現報酬"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋。以 26 週前約 159 美元到現價 188 美元、FY1 EPS 3.81 計算，買入盈餘殖利率約 2.0%～2.4%，自由現金流殖利率約 3.4%～4.1%。門檻是 10 年期殖利率加 2%；10 年期殖利率事實表未涵蓋，但以盈餘殖利率計，任何正常利率環境都不會通過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 0.63%（Q3 2026）。以 FY2026 共識營收 71.4 億計約 4,500 萬美元，約當股本每年稀釋 0.3% 以下，回購抵銷有餘"}]},"governance":{"capital_returns":[{"item":"2022 年以來回饋股東","value":"21 億美元，占現金運用逾九成（2026-05-28 投資人日 CFO）"},{"item":"2026 年初至 Q3 回饋","value":"約 3.36 億美元（回購加股息）；Q3 回購 1.47 億"},{"item":"2026 全年回饋指引","value":"3.75～4.25 億美元（Q2 時為 3.25～3.75 億）"},{"item":"剩餘回購授權","value":"約 14 億美元"},{"item":"淨負債與流動性","value":"淨負債約 41.5 億美元（含租賃口徑）；流動性約 18 億；承諾維持投資等級，2028 年底前可再增加 2～5 億負債"}]}}},"q5_valuation":{"verdict":"現價要求 2026–2028 年每股盈餘照共識年增約 26%，而且五年後市場仍給 27 倍以上，才換得每年約 6% 的報酬。成長方向我信，但價格沒有留安全邊際，估值偏貴。","reasoning":"現價 187.89 美元。FY2026（FY1）共識 EPS 3.81 對應 49.3 倍，FY2027 的 4.90 對應 38.3 倍，FY2028 的 6.09 對應 30.9 倍；trailing GAAP 97.9 倍受 2025 年一次性損益干擾，不採用。EV 217 億美元除以 2026 調整後 EBITDA 指引中值 11.85 億，約 18.3 倍；前瞻 EV/S 3.04 倍。P/E、P/S、EV/S 都在自身 3～4 個年度端點的最高位（分位 100），但這不是五年分位。PEG＝49.3 ÷ FY2026–2028 EPS 年複合 26.4%＝1.87，落在合理區間上緣。自由現金流殖利率約 3.4%（調整後 FCF 指引中值 6.05 億 ÷ 市值 175 億），股息殖利率 0.32%。賣方目標價均值約 195～198 美元（2026 年 8～9 月，都在 Q3 上修指引之前），最高 221，現價的上行空間約 5%。Base 情境為 2031 年 EPS 8.6 × 27 倍＝232 美元，五年價格報酬只有每年約 4%，加股息與回購約 6%，不足以補償 30% 機率的衰退情境。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_rsi14","f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1、FY2 共識 EPS），以 EV/EBITDA 輔助","tier":"輕資產旅宿品牌（高端組合）","peers":{"expanded":false,"reason":"事實表的同業對照只有利益率，沒有收同業的前瞻本益比或 EV/EBITDA，無法做同層級倍數比較；終端倍數改以 Hyatt 自身 FY2028 隱含倍數與 EV/EBITDA 對照"},"fwd_pe":49.31,"peg":1.87,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 49 倍、FY2027 38 倍，自身年度端點分位 100，EV/EBITDA 約 18 倍；PEG 1.87 在合理區間上緣；賣方均價只有約 5% 上行；base 五年價格報酬每年約 4%。結論是偏貴但未到極端，因為 FY2028 的 31 倍對應約 25% 的盈餘成長，判 🟠。五年分位：事實表只有 3～4 個年度端點，不外推。","upside_short_pct":4.8,"upside_mid_pct":23.6,"denominator_disputed":false,"denominator_note":"trailing GAAP 本益比 98 倍的分母受 2025 年 GAAP 每股虧損 0.55 美元與資產出售損益干擾，改用 FY1、FY2 共識；前瞻分母本身不是爭點。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是景氣。2026 年的 RevPAR 有一次性助力；若 2027～2028 年轉入衰退，固定成本會把費用下滑放大成 EPS 下滑，49 倍的倍數也會失去支撐。","reasoning":"三個視角與 AI 通路情境已寫在反證紀錄，這裡不重寫。壓力測試 5 項過 3 項。①2026 年墨西哥、中東、牙買加合計 EBITDA 衝擊約 6,000 萬美元，費用仍維持 +10%～11%：通過。②流動性約 18 億、承諾投資等級：通過。③SBC 0.63%：通過。④RevPAR 轉為年減 3%，EPS 成長轉負：不通過。⑤倍數回到 27 倍，base 五年報酬每年低於 8%：不通過。管理層迴避的問題集中在幾處：key money 的新建與轉換拆分、會員滲透率的同口徑數字、系統基金提撥率（2026-05-28 投資人日），以及 2027 淨增房數的具體數字（2026-07-30）。這幾處是資訊最軟的地方。歷史最大回撤事實表未涵蓋。","fact_refs":["f_rsi14","f_week26_return_pct","f_pe_percentile","f_kpi5_comparable_system_wide_r","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退信號亮燈（EPS 成長遠高於營收），成因是固定成本攤薄；陷阱風險低到中"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.81,"pe":49.31,"basis":"FY2026 共識 EPS 3.81 美元（財年 12 月，判斷日距年底約兩個月，視同當年口徑）；終端倍數同樣套在 FY2031 當年 EPS，分母同口徑。同業前瞻本益比事實表未涵蓋，終端倍數以 Hyatt 自身 FY2028 隱含 30.9 倍與 EV/EBITDA 約 18 倍對照"},"eps":{"bull":[5.0,6.3,7.55,8.9,10.4],"base":[4.8,5.75,6.65,7.6,8.6],"bear":[4.25,3.9,4.05,4.4,4.75]},"pe":{"bull":32,"base":27,"bear":20},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.32,"net_buyback":1.8},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-45,"basis":"事實表未涵蓋歷史最大回撤。以 bear 終點約 −49%（EPS 4.75 × 20 倍）為中樞；旅宿衰退時 RevPAR 下滑會經固定成本放大到 EPS，加上現價 FY1 49 倍、自身年度端點分位 100 的倍數壓縮空間，路徑中途低點可能比終點再深 5～10pp，推得 −45%～−60%。","trigger_time":null},"basis":{"bull":"2027 指引 RevPAR ≥4%、淨增房數 7%～8%，Essentials 與國際 pipeline 放量，Delta 合作與國際聯名卡拉高費用；費用年增 12%～13%，倍數維持 32 倍（EV/EBITDA 約 18 倍不變）","base":"2027 RevPAR +2%～3%（世足與節日時點的基期退場），淨增房數 6%～7%，費用年增約 10%；EBITDA 下方固定成本攤薄，使 EPS 在 2027～2028 年增 20%～26%，之後回落到 11%～16%；終端 27 倍（推論約當 EV/EBITDA 15 倍）","bear":"2028 年美國旅宿衰退、RevPAR 年減，墨西哥與中東未恢復，代理式 AI 抬高分銷成本，key money 加碼；EPS 2028 年回落至 3.9 美元，2031 年才回到 4.75；終端 20 倍（成長熄火至約 10% 的倍數）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"前 50 大市場需求成長 1.3%，低於歷史 2%。2026 年 RevPAR 有世足、猶太節日時點與中東基期助力，管理層自己說不會重複。CoStar 預測美國 2027 RevPAR 只有 +2.1%。","assumption":"base 假設 RevPAR 全週期 +2%～4%、淨增房數 6%～7%","consequence":"2028 年衰退使 RevPAR 轉負，EPS 下方的固定成本反向放大，EPS 回到 3.9 美元；倍數由 49 倍收斂到 20 倍，五年後股價約 95 美元，跌約一半。","ruling":"部分採納，給 30% 機率。供給成長 0.6%～1.3%、在建量 12 年低，限制了下行深度，所以不把衰退情境放到 base 之上。這條與唯一致命點同源（RevPAR 轉負），不另立。","watch":"每季系統可比 RevPAR；2027 指引","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi5_comparable_system_wide_r","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"key money 競爭激烈，管理層預估每年 1.5～1.7 億美元（2026-10-29 CEO）。Hall Financial 的 5 億美元融資工具由 Hyatt 提供部分信用支持（2026-07-30 CEO）。出售 Playa 時另投 2 億美元優先股給買方。2025 報表自由現金流 1.59 億（利益率 2.2%），公司調整後口徑約 4.85 億。以 FY1 EPS 計，現價回購的盈餘殖利率約 2%。","assumption":"費用與房數達標，就能轉成每股價值","consequence":"房數與費用都達標，但業主支援（key money、信用支持、優先股）吃掉自由現金流，報表與調整後現金流持續有大落差；回購又在 40～50 倍盈餘下進行，每股價值累積得比費用成長慢。","ruling":"採納為監測項。以管理層自訂的調整後 EBITDA 轉自由現金流 ≥50% 為門檻，並追蹤報表與調整後自由現金流的差距；回購買入收益率偏低這點，已直接計入資本配置評分。","watch":"年度調整後 FCF／EBITDA；報表 FCF；key money 是否超過 1.7 億","evidence_refs":[],"fact_refs":["f_kpi8","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"FY1 前瞻本益比 49 倍、FY2027 38 倍、trailing 98 倍；P/E、P/S、EV/S 都在自身年度端點分位 100。RSI 70，26 週漲 18%。Q2 後多家券商下調目標價，均價約 195～198 美元。","assumption":"市場會持續給輕資產轉型完成的溢價倍數","consequence":"即使 EPS 照 base 走到 8.6 美元，倍數回到 27 倍時，五年價格報酬每年只有約 4%。","ruling":"採納。這是本次不追價的主因，進場改等 155 美元以下。","watch":"股價對 FY2027 共識的倍數；共識修正方向","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_rsi14","f_week26_return_pct","f_consensus_rev_fy2_pct"]},{"view":"論點失敗","evidence":"10-K 承認：AI 工具決定給使用者什麼資訊時，Hyatt 物業可能得到較少關注；新分銷通路（含潛在 AI 平台）可能對業務造成負面影響。管理層也說代理式訂房會成長很快。","assumption":"直銷約七成與會員入口可以延續","consequence":"2028 年後代理式 AI 成為主要預訂入口，Hyatt 只能付佣換曝光，費用率與會員價值下降，倍數向中價位連鎖靠攏。","ruling":"暫不採納為 base。LLM 完成的訂房目前非常少；Hyatt 已在 ChatGPT 等平台建立自有入口，接在自有資產上屬強化。設直銷占比低於 65% 為轉向條件。","watch":"直銷房晚占比；管理層揭露的 AI 來源訂房占比","evidence_refs":["substitute_technology#0","channel_business_model_shift#1","competitive_share_entrants#0"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 164.4 → 本次 187.89（+14.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=164.4","side_b":"本次 price_at_dd=187.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 164.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 164.4 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 164.4 美元：Bull 價 332.8、Bear 價 95，五年期望值 +28.4%，基準年化 7.1%，不對稱比 1.62","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.62。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 164.4 美元：五年期望值 +28.4%，基準年化 7.1%，不對稱比 1.62","side_b":"本次情境、股價 187.89 美元：五年期望值 +12.4%，基準年化 4.3%，不對稱比 1.04","ruling":"再換股價、情境不動：起點價上漲 14.3%，五年期望值少 16.1 個百分點，基準年化少 2.8 個百分點，不對稱比由 1.62 降到 1.04。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"淨增房數：承諾對實績","cause":null,"prior_field":null,"side_a":"管理層：2026 全年淨增房數約 6%，2026–2028 年複合 6%～8%，2027 Q1 可達 6%～7%（2026-10-29 CEO）","side_b":"Q3 2026 淨增房數只有 3.9%（不含 Playa），全年過半開幕擠在 Q4；2026-07-30 CEO 已說部分 Q4 開幕可能延到 2027，轉換案的 PIP 也比原先模型重","ruling":"程度差異，可以調和。採信方向、不採信時點：base 假設 2026 全年約 5%～5.5%，2027 回到 6%～7%。若 2026 全年低於 5%，開發飛輪假設降為削弱。","evidence_level":"公司季報與法說（自報）","settle_metric":"FY2026 全年淨增房數（2027-02 第四季財報）","if_then":["若 FY2026 淨增房數 <5% 且 2027 指引 <6%：開發飛輪假設降為削弱，停止加碼","若 FY2026 ≥6% 且 2027 Q1 單季 ≥6%：維持假設，動作不變"],"evidence_refs":[]},{"axis":"2027 RevPAR：公司口徑對產業預測","cause":null,"prior_field":null,"side_a":"公司兩度上修 2026 全年 RevPAR 指引至 5%～5.5%，稱 2027 的布局很好：企業團體 pace 近 +10%，扣除世足的團體 pace 為中個位數（2026-10-29 CFO、CEO）","side_b":"CoStar 預測美國 2027 RevPAR 只有 +2.1%；同業給 2027 年 3%～4%；管理層自己也說世足與節日時點不會重複；Green Street 估 2026 年前 50 大市場需求成長 1.3%，低於歷史 2%","ruling":"程度差異，可以調和。Hyatt 的高端與休閒組合有贏過產業的紀錄（年初至今市占 +100bp），但 base 只給 2027 系統 RevPAR +2%～3%，不跟管理層的語氣走；衰退情境給 30%。","evidence_level":"第三方產業預測加公司前瞻 pace","settle_metric":"2027 RevPAR 指引（2027-02）與 2027 Q1 實績（2027-05）","if_then":["若 2027 指引 RevPAR ≥4%：上調 base 路徑並重算進場價","若 2027 指引 ≤1% 或 Q1 實績轉負：衰退機率上調至 40%，未持有者不建倉"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"Distribution 與全包式：暫時性歸因","cause":null,"prior_field":null,"side_a":"2026-05-28 投資人日 CFO：2026 年的颶風與墨西哥干擾屬暫時，Distribution EBITDA 年複合成長 2%～4%。Q3 法說稱 2027 Q1 全包式訂房 pace 為高個位數，坎昆航班運能回升，牙買加 2027 Q1 末至 Q2 初復開","side_b":"Distribution 全年 EBITDA 預期年減幅度由 Q2 的 2,500 萬擴大到 3,000 萬，Q3 也低於公司預期；net package RevPAR Q2 −1.2%、Q3 −2.5%；2025 Distribution 營收已年減 7.5%；這塊業務的去留，管理層沒有給答案","ruling":"管理層的一次性歸因，不採信也不否定，標為未證、監測。預先登記：若 2027 上半年 Distribution 調整後 EBITDA 仍低於 2025 同期，或 2027 Q1 net package RevPAR 仍為負，暫時性歸因視為證偽。","evidence_level":"公司季報加法說","settle_metric":"2027 Q1、Q2 的 net package RevPAR 與 Distribution 調整後 EBITDA","if_then":["若證偽：衰退機率上調 5pp，Distribution 改以永久性減損看待","若 2027 Q1 net package RevPAR 轉正且 Distribution EBITDA 年增：維持暫時性歸因"],"evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"axis":"觀望對現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：全年指引兩度上修，FY1 共識三個月上修 4.7%，pipeline 與會員都創新高；2027 有牙買加復開與墨西哥回升這兩個已知順風；回購授權還有 14 億美元，可以在回檔時承接","side_b":"股價 26 週漲 18%、RSI 70，但 FY2027 共識只上修 0.82%、FY2028 只上修 0.5%，漲幅主要來自倍數擴張；Q2 後多家券商下調目標價，均價約 195～198 美元，只比現價高約 5%；FY2027 共識 38 倍","ruling":"採觀望，約束條件是估值。漲幅來自倍數而不是遠期盈餘；base 情境五年價格報酬每年約 4%（不含股息與回購），撐不起 30% 機率的衰退情境。","evidence_level":"共識快照加價格資料","settle_metric":"FY2027 共識 EPS 與股價的相對變化","if_then":["若股價續漲而 FY2027 共識未上修 ≥3%：不追","若股價回落至 155 美元以下且共識未下修：重跑估值後分批建倉"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：美國供給成長 2026～2027 年約 0.6%～1.3%，在建量 12 年低，品牌方在高端市場的房價指數上升","side_b":"其他結構變數：10-K 把含 AI 平台的新分銷通路列為負面因素；競爭面則有同業整併與 key money 加碼","ruling":"雙向拉鋸。供給軸轉好，通路軸（代理式 AI）變動中，競爭軸大致靜態；淨效果不足以改變護城河方向。","evidence_level":"第三方產業資料加 10-K","settle_metric":"美國年度供給成長率；直銷房晚占比","if_then":["若美國年度供給成長升破 2%：衰退機率上調","若直銷房晚占比 <65%：護城河方向改判縮減"],"evidence_refs":["channel_business_model_shift#1","competitive_share_entrants#1"]},{"axis":"前份漂移：價格","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-20，股價 164.4）：綜合評級 B，估值偏貴（🟠）","side_b":"本次（股價 187.89，漲 14%）：綜合評級 B，估值偏貴（🟠）；FY1 49 倍、FY2027 38 倍","ruling":"股價上漲，但 FY2027 共識同期只微調，估值更貴；沒有到極端，是因為 FY2028 的 31 倍對應約 25% 的盈餘成長。兩欄的值都沒變，變的是價格。前次觀望以來報酬 +14%，未達需要說明翻面理由的 30%。","evidence_level":"價格與共識快照","settle_metric":"股價對 FY2027 共識的倍數","if_then":["若倍數升破 45 倍：已持有者減碼","若倍數回到 32 倍以下：重跑研究"],"evidence_refs":[]},{"axis":"前份漂移：方法補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這幾欄都是空值，沒有產出護城河方向、五年後成長空間、公司類型、循環位置、情境機率與最大回撤","side_b":"本次：護城河方向穩定（→），五年後成長空間寬（🟢），類型為品質複利成長（次類循環），循環位置中循環，情境機率 20／50／30，最大回撤 −45%～−60%；裁決與角色由矩陣依新欄位產生","ruling":"屬方法補齊，不是基本面變化。","evidence_level":"方法變更","settle_metric":"無","if_then":["若下份研究上述欄位改變：依新證據或價格分別歸因"],"evidence_refs":[]},{"axis":"前份漂移：陷阱判讀","cause":"方法變動","prior_field":["trap"],"side_a":"前份陷阱判讀 🟢","side_b":"本次 🟡：十項衰退信號中，「EPS 成長顯著高於營收成長」亮燈（FY2027 共識 EPS +28.6%，共識營收 +8.1%）","ruling":"本次事實表首度有共識營收可以比對，逐項計數得到 1 項。成因是 EBITDA 下方固定成本攤薄，不是品質惡化，所以只到 🟡。","evidence_level":"共識快照","settle_metric":"FY2027 實際 EPS 與營收成長差","if_then":["若再亮第 2 項以上：陷阱判讀維持 🟡 並重估倉位上限","若 EPS 與營收成長差縮到 5pp 內：回到 🟢"],"evidence_refs":[]},{"axis":"建倉門檻變更","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"建議等 Fwd PE<28x 或股價回測 W52 $151","side_b":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 指引的 RevPAR 與淨增房數未下修","ruling":"前份以單一倍數與 52 週均線作為建倉錨；本次改由情境樹反推。股價 155 美元時，base 五年價格報酬每年約 8%，加股息與回購約 10%。52 週均線已上移到 168.6，不再適合當錨點；新門檻約略等於 104 週均線 154.5。","evidence_level":"情境樹推導","settle_metric":"股價","if_then":["若股價 ≤155 且 2027 指引未下修：重跑研究後分批建倉","若股價 ≤155 但指引下修：不建倉，先重估 base 路徑"],"evidence_refs":[]},{"axis":"唯一致命點變更","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"Single Thing：2027～2028 年旅宿景氣轉入衰退，系統可比 RevPAR 出現單季年減 3% 以上","ruling":"前份沒有指定唯一致命點；本次依敏感度選 RevPAR。每 1 個百分點的 RevPAR 變動同時影響費用、獎勵費與倍數，敏感度大於淨增房數落後。發生時減碼至半倉，連 2 季為負則清倉。","evidence_level":"情境樹敏感度","settle_metric":"每季系統可比 RevPAR","if_then":["若單季 ≤−3%：減碼至半倉","若連 2 季為負：清倉並重跑研究"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"風險門檻與退場指標變更","cause":"新證據","prior_field":["kill_metrics","thesis.R"],"side_a":"前份 R1：連 2 季 RevPAR 年增轉負；R2：調整後 EBITDA 利益率差距由 5pp 擴大到 >8pp 連 2 年；R3：Fwd PE 跌至 25 倍或 EV/EBITDA <18 倍；前份未設退場指標","side_b":"本次：RevPAR 連 2 季年減，或單季 ≤−3% 即減碼、連 2 季清倉；利益率差距 >8pp 門檻保留，標資料缺口；倍數壓縮改列為建倉條件，不再列為風險；新增五項退場指標：gross fees <9%、淨增房數 <5%、FCF 轉換 <50%、Distribution EBITDA 再年減、直銷占比 <65%","ruling":"RevPAR 門檻加上單季 −3%，是因為 Q3 法說顯示 2026 年有一次性助力，而產業預測 2027 年只剩 +2.1%。倍數門檻退休：現價 EV/EBITDA 約 18.3 倍，已貼近前份的 18 倍門檻，但那是估值問題、不是論點風險，改由建倉價處理。利益率差距門檻保留，但事實表只有報表營業利益率（H 7.2%、MAR 15.7%、HLT 24.0%），沒有調整後 EBITDA 利益率，標資料缺口。","evidence_level":"Q3 2026 季報、法說與產業預測","settle_metric":"各退場指標","if_then":["若任一退場指標觸發：依該指標動作減碼或清倉","若利益率差距資料補齊且 >8pp 連 2 年：護城河改判縮減"],"evidence_refs":["supply_demand_durability#3","competitive_share_entrants#1"]},{"axis":"假設門檻變更","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份 H1：RevPAR 年增 +2%～5%（連 2 季 <−2% 為反轉）；H2：會員 FY28 突破 1 億；H3：輕資產 2026 年達 90%（下限 88%）","side_b":"本次 H1：gross fees 年增 ≥9%；H2：淨增房數 ≥5%、三年複合 ≥6%；H3：會員年增 ≥10%、直銷占比 ≥65%；RevPAR 改由唯一致命點與 R1 監測","ruling":"會員 1 億的門檻退休：目前 7,200 萬、年增 19%，到 2028 年底要再年增約 16% 才達標，門檻過度依賴單一增速，而且會員數不等於費用，改用年增率。輕資產 90% 已兌現（2026 年約 90%），退休。RevPAR 從假設移到風險端，是因為 Q3 法說顯示 2026 年有一次性助力。","evidence_level":"Q3 2026 季報與 2026-05-28 投資人日","settle_metric":"gross fees、淨增房數、會員年增率","if_then":["若 H1 至 H3 任兩項削弱：停止加碼並重跑研究","若三項皆維持：動作不變"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 全年 gross fees 指引年增低於 9%，視為費用引擎假設削弱","type":"假設驗證","maps_to":"H1","metric":"FY2027 gross fees 成長指引","threshold":"<9%","action":"停止加碼；未持有者維持觀望","source_freq":"第四季財報（一年一次）","date":"2027-02"},{"n":2,"text":"FY2026 全年淨增房數低於 5%，視為開發飛輪假設削弱","type":"假設驗證","maps_to":"H2","metric":"FY2026 淨增房數","threshold":"<5%","action":"停止加碼，重估 base 的房數路徑","source_freq":"季報","date":"2027-02"},{"n":3,"text":"系統可比 RevPAR 單季年減 3% 以上，唯一致命點成立","type":"Single Thing","maps_to":"Single Thing","metric":"系統可比 RevPAR 年增率（每季）","threshold":"單季 ≤−3%；連 2 季為負","action":"單季 ≤−3% 減碼至半倉；連 2 季為負清倉並重跑研究","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"全包式復甦落空：2027 Q1 net package RevPAR 仍為負","type":"風險","maps_to":"R2","metric":"net package RevPAR 年增率","threshold":"2027 Q1 <0","action":"Distribution 改以永久性減損看待，衰退機率上調 5pp，停止加碼","source_freq":"季報","date":"2027-05","evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"n":5,"text":"直銷房晚占比跌破 65%，或 AI 平台來源訂房超過 5% 且需付佣","type":"風險","maps_to":"R3","metric":"直銷房晚占比、AI 來源訂房占比","threshold":"<65% 或 >5%","action":"護城河方向改判縮減，減碼三分之一","source_freq":"年度（投資人日、10-K、法說）","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","channel_business_model_shift#1","competitive_share_entrants#0"]},{"n":6,"text":"中東與墨西哥合計的年度費用衝擊擴大","type":"風險","maps_to":"R4","metric":"區域費用衝擊（管理層揭露）","threshold":">4,000 萬美元／年","action":"衰退機率上調 5pp，停止加碼","source_freq":"季報法說","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"股價回落到 155 美元以下，且 2027 指引未下修：重跑研究後分批建倉","type":"估值rearm","maps_to":null,"metric":"股價（約為 FY2027 共識 EPS 的 32 倍）","threshold":"≤155 美元","action":"重跑研究確認論點未破，首批建倉不超過目標倉位的三分之一","source_freq":"每日價格","date":null},{"n":8,"text":"已持有者在 FY2027 共識 45 倍以上分批減碼","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥221 美元（FY2027 共識 4.90 × 45，約等於賣方最高目標價）","action":"減碼三分之一","source_freq":"每日價格","date":null},{"n":9,"text":"第四季財報與 2027 全年指引","type":"複審日期","maps_to":null,"metric":"2027 年 RevPAR、淨增房數、gross fees 與 EBITDA 指引","threshold":null,"action":"重跑情境樹與進場價","source_freq":"一年一次","date":"2027-02"},{"n":10,"text":"World of Hyatt 會員年增連 2 季低於 10%","type":"假設驗證","maps_to":"H3","metric":"會員數年增率","threshold":"<10%，連 2 季","action":"會員入口假設降為削弱，停止加碼","source_freq":"季報","date":null}],"kill_metrics":[{"metric":"系統可比 RevPAR 年增率（每季）","bear_threshold":"單季 ≤−3% 減碼至半倉；連 2 季為負清倉","window":"每季財報","source":"公司季報新聞稿（Q3 2026 為 +7.2%）","last_status":"ok"},{"metric":"年度 gross fees 成長率","bear_threshold":"<9%（投資人日三年複合 9%～13% 的下緣）","window":"年度（2027-02 起）","source":"季報新聞稿與第四季法說指引（2026 指引 +10%～11%）","last_status":"ok"},{"metric":"年度淨增房數","bear_threshold":"<5%","window":"年度","source":"季報新聞稿（Q3 2026 為 3.9%，全年目標約 6%）","last_status":"warning"},{"metric":"調整後 EBITDA 轉調整後自由現金流比率","bear_threshold":"<50%（管理層自訂下限）","window":"年度","source":"季報新聞稿與法說（2026 指引 ≥50%）","last_status":"ok"},{"metric":"Distribution 分部調整後 EBITDA","bear_threshold":"2027 上半年仍低於 2025 同期","window":"2027 上半年","source":"季報分部資料（2026 全年預期年減約 3,000 萬美元）","last_status":"warning"},{"metric":"Hyatt 對 MAR、HLT 的調整後 EBITDA 利益率差距","bear_threshold":">8pp 連 2 年（沿用前份門檻）","window":"年度","source":"資料缺口：事實表只有報表營業利益率（H 7.2%、MAR 15.7%、HLT 24.0%）","last_status":"unknown"},{"metric":"直銷房晚占比","bear_threshold":"<65%","window":"年度","source":"投資人日、10-K 與法說揭露（2026-05-28 約 70%）","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這是 10-K 對 IT 與雲端供應商依賴的一般性風險揭露，沒有指出任何已發生的事件、受影響營收或金額，無法對應到可監測的門檻；日後若出現具體的系統中斷事件，再列入風險。"}],"action_conditions":{"rearm_trigger":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 指引的 RevPAR 與淨增房數未下修","exec_line":"觀望、不追價。未持有者等股價 ≤155 美元且 2027 指引未下修，重跑研究後分批建倉；已持有者續抱，≥221 美元減碼三分之一；RevPAR 單季 ≤−3% 減碼至半倉，連 2 季為負則清倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 年指引的 RevPAR 與淨增房數未下修","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"qc48_result":"pass","qc48_note":"Hyatt 的 Bull 情境有量加價的骨架，Essentials 新市場擴張也有公開來源，但從費用收入到 EPS 的槓桿、230 萬間可拓展房數這個數字，以及同業 5 年實際報酬的對照都沒有可驗證的來源，目前只能算部分成立，沒有哪一項被證偽。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=18.28, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Hyatt 的 Bull 情境有量加價的骨架，Essentials 新市場擴張也有公開來源，但從費用收入到 EPS 的槓桿、230 萬間可拓展房數這個數字，以及同業 5 年實際報酬的對照都沒有可驗證的來源，目前只能算部分成立，沒有哪一項被證偽。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 年指引的 RevPAR 與淨增房數未下修'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"費用引擎維持雙位數成長：2026 年 gross fees 年增 10%～11% 落地，2027 年再年增至少 9%（投資人日 2025–2028 年複合 9%～13% 的下緣）。","2y":"FY2026 gross fees 達 13.2～13.35 億美元；FY2027 年增 ≥9%","5y":null,"10y":null,"threshold":"FY2027 gross fees 年增 <9%，或單季年增連 2 季 <5%","source":"季報新聞稿的 gross fees；2027-02 第四季法說的 2027 指引；2026-05-28 投資人日 CFO 的三年複合指引","drift_rule":"TTM gross fees 對指引路徑連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H2","text":"開發飛輪延續：2026–2028 年淨增房數年複合 6%～8%，pipeline 持續創新高；中高價位新品牌開進新市場，但不稀釋整體每房費用。","2y":null,"5y":"2028 年底淨增房數三年複合 ≥6%；pipeline ≥17 萬間；管理層仍揭露 pipeline 每房費用高於在營飯店","10y":null,"threshold":"年度淨增房數 <5%，或 pipeline 年增轉負","source":"季報的淨增房數與 pipeline；2026-10-29 第三季法說 CEO 對 2027 Q1 淨增房數 6%～7% 的展望","drift_rule":"TTM 淨增房數對 6% 目標連 4 季偏離 ≥5% 為削弱，連 6 季偏離 ≥10% 為反轉"},{"id":"H3","text":"會員與直銷守住訂房入口：World of Hyatt 會員年增 ≥10%，直銷房晚占比維持約七成；代理式 AI 成為接在 Hyatt 自有預訂上的新入口，而不是抽成的中介。","2y":null,"5y":null,"10y":"2030 年後會員年增仍 ≥10%；直銷房晚占比 ≥65%；AI 平台來源的訂房主要在 Hyatt 自有通路完成","threshold":"會員年增 <10%，或直銷房晚占比 <65%","source":"季報會員數（Q3 2026 約 7,200 萬、年增 19%）；投資人日與 10-K 的直銷占比（2026-05-28 CEO：約 70%）；法說對 AI 訂房占比的揭露","drift_rule":"跨 2 個年度低於門檻為削弱，跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"旅宿景氣反轉：2026 年的世足、猶太節日時點與中東基期等一次性助力退場後，需求成長本來就低於歷史（前 50 大市場 1.3%，2006–2019 年均 2%），RevPAR 轉負。","h_ref":"H1","clock":"🔥","threshold":"系統可比 RevPAR 連 2 季年減，或任一季 ≤−3%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"全包式與 Distribution 復甦落空：墨西哥坎昆的需求與航班運能、牙買加復開都延後，Distribution 營收與 EBITDA 連年下滑；出售 Playa 時投給買方的 2 億美元優先股，信用風險也連帶升高。","h_ref":"H1","clock":"⚡","threshold":"2027 Q1 net package RevPAR 年增 <0，或 2027 上半年 Distribution 調整後 EBITDA 仍低於 2025 同期","evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"id":"R3","text":"代理式 AI 與新分銷通路截走訂房入口：由 LLM 決定推薦哪家飯店，第三方 AI 技術的定價又不受 Hyatt 控制；結果是直銷占比下滑、分銷成本上升。","h_ref":"H3","clock":"🐢","threshold":"直銷房晚占比 <65%，或管理層揭露 AI 平台來源訂房 >5% 且需支付佣金","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","substitute_technology#1","channel_business_model_shift#1"]},{"id":"R4","text":"地緣政治與貿易政策：中東衝突、墨西哥治安與關稅急變，壓抑國際旅遊並推高供應商成本。","h_ref":"H1","clock":"🔥","threshold":"中東加墨西哥的年度費用衝擊 >4,000 萬美元（2026 年約 3,000 萬）","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"id":"R5","text":"開幕延遲、轉換案卡關：2026 年過半開幕擠在第四季，2026-07-30 法說已坦承部分開幕會延到 2027，轉換案的 PIP 也比原先模型重。","h_ref":"H2","clock":"⚡","threshold":"FY2026 淨增房數 <5%，或 2027 上半年仍出現跨季延遲","evidence_refs":[]},{"id":"R6","text":"與 MAR、HLT 的規模差距擴大：同業整併、會員規模更大，報表營業利益率只有對方的一半左右（7.2% 對 15.7%、24.0%），在爭取業主與 key money 上處於劣勢。","h_ref":"H2","clock":"🐢","threshold":"調整後 EBITDA 利益率差距 >8pp 連 2 年（事實表只有報表營業利益率，標資料缺口）","evidence_refs":["competitive_share_entrants#1"]}],"single_thing":{"description":"2027～2028 年旅宿景氣轉入衰退，系統可比 RevPAR 出現單季年減 3% 以上","why_fatal":"費用直接按飯店營收與利潤抽成，而 EPS 下方的折舊與利息大致固定；RevPAR 由 +5% 轉為 −3%，會讓共識預期的 2027～2028 年約 25% EPS 成長轉為下滑。現價 49 倍的倍數同時失去成長支撐，盈餘與倍數雙殺，落到衰退情境（五年後約 95 美元）。","if_happens":"單季 ≤−3% 減碼至半倉；連 2 季為負則清倉並重跑研究；未持有者暫停建倉，直到 RevPAR 回正","how_monitor":"每季財報的系統與美國可比 RevPAR；第四季美國全服務飯店的團體 pace（目前中個位數成長）；企業協議價業務成長（Q3 約 +4.8%）","probability":"12～24 個月約 20%"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":38.35,"peg_fy2":1.45,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.55,"FY2026E":3.81,"FY2027E":4.9,"FY2028E":6.09},"fy_end_month":12,"eps_basis":"FY2026–2028 為 Koyfin 共識 EPS。TTM GAAP EPS 約 1.9 美元，與共識差距大，推定共識為調整後口徑，但事實表未載明。FY2025A 為 GAAP 稀釋 EPS −0.55 美元，受資產出售與一次性項目影響，口徑與共識不同，不作成長率基期；三年成長率以 FY2026→FY2028 計。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉（管理層稱會壓抑 Q4 美國 RevPAR）","impact":"低","watch":"Q4 美國 RevPAR 是否低於指引隱含值"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年指引（RevPAR、淨增房數、gross fees、EBITDA）","impact":"高","watch":"2027 RevPAR 指引是否 ≥2%，淨增房數是否 ≥6%"},{"date":"2027-02","date_precision":"month","type":"product","event":"Delta 雙向累積合作的細節揭露","impact":"中","watch":"會員交叉使用與聯名卡的經濟效益是否量化"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"轉換案端到端 AI 平台完成","impact":"低","watch":"轉換案開幕週期是否縮短，2027 Q1 淨增房數是否達 6%～7%"},{"date":"2027-04","date_precision":"quarter","type":"capacity","event":"牙買加飯店復開（管理層預估 2027 Q1 末至 Q2 初）","impact":"中","watch":"Distribution 分部 EBITDA 是否轉為年增"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。核心軸由採證 agent 自報不適用（燈號不變，請看 note 理由）：customer_concentration_credit。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
