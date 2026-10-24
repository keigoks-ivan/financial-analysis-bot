你是 DD 管線 v20 的判斷層閘（gate），標的 TSLA（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝28046 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝718 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝2.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi6_gaap`（q1_business）｜汽車毛利率（GAAP）＝18.5 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi7`（q1_business）｜交車量＝486532 輛｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi8`（q1_business）｜儲能部署量＝13.7 GWh｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi9`（q1_business）｜管理層指引＝無量化指引｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_peer_gm_operating_margin_pct`（q2_moat）｜GM 營業利益率＝0.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_f_operating_margin_pct`（q2_moat）｜F 營業利益率＝-3.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.F.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rivn_operating_margin_pct`（q2_moat）｜RIVN 營業利益率＝-60.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RIVN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_1211_hk_operating_margin_pct`（q2_moat）｜1211.HK 營業利益率＝5.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.1211.HK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsla_gross_margin_pct`（q2_moat）｜TSLA 毛利率＝18.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSLA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsla_operating_margin_pct`（q2_moat）｜TSLA 營業利益率＝4.61 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSLA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsla_fcf_margin_pct`（q2_moat）｜TSLA FCF 利潤率＝5.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSLA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_1211_hk_gross_margin_pct`（q2_moat）｜1211.HK 毛利率＝17.76 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.1211.HK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_1211_hk_fcf_margin_pct`（q2_moat）｜1211.HK FCF 利潤率＝-6.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.1211.HK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gm_gross_margin_pct`（q2_moat）｜GM 毛利率＝5.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_f_gross_margin_pct`（q2_moat）｜F 毛利率＝2.22 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.F.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rivn_gross_margin_pct`（q2_moat）｜RIVN 毛利率＝7.51 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RIVN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.77 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.16 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.22 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.56 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 1.78 → 1.77（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-1.37 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（2.19 → 2.16）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-2.42 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（3.3 → 3.22）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi4_gaap`（q4_capital）｜自由現金流（非GAAP）＝1531 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi5_sbc`（q4_capital）｜SBC＝1165 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Tesla Q3 2026 Update（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝372.22 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝210.29 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 1.77，分子＝快照價 372.22｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_rsi14`（q5_valuation）｜RSI(14)＝51.52｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-1.08 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 372.22 / W52 396.82 / W104 369.85 / W250 286.55 / W250 13週斜率 0.17%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝396.82 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_w104`（q5_valuation）｜104 週均線＝369.85 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_w250`（q5_valuation）｜250 週均線＝286.55 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.17 %｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述：進入電動車與自駕市場的既有與新進車廠數量顯著且持續增加，競爭加劇可能導致銷量下降、降價與市占流失；另稱許多對手資源更多。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：西歐18國 Tesla 2026Q2 份額 2.6%（去年同期1.7%），中國品牌合計創 10.7% 新高
  - 來源：SCMP：Europe's new EV power struggle（as_of 2026-07-15）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：Waymo 為 robotaxi 領先者，Zoox、Uber/Lucid/Nuro 為新進入者
  - 來源：SF Standard：Waymo has robotaxi lead（as_of 2026-01-07）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K FY2025 揭露：公司配合多項政府調查；就公司所知，沒有任何機關在進行中的調查裡認定有不當行為，但無法預測結果，若 SEC、司法部或其他機關日後採取法律行動，可能面臨責任、罰款與限制性制裁。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：中國有一件反壟斷訴訟指控 Tesla 濫用市場支配地位、限制獨立維修商取得維修軟體（民間訴訟，非主管機關行動）
  - 來源：MLex（as_of 2026-09-29）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：NHTSA 對 Tesla FSD 的調查延長，回覆期限延至 2026-02-23
  - 來源：HeyGoTrade: Tesla FSD Probe: NHTSA Grants 5-Week Breathing Room（as_of 2026-01-19）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 稱 2025 年美國關稅調升及報復措施已影響供應鏈成本，並可能影響部分技術或零組件的取得（視關稅範圍與報復性出口管制而定）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K MD&A 稱現行關稅制度對儲能業務的衝擊相對大於汽車業務；進口關稅可能顯著推高電池電芯成本。
  - 來源：SEC EDGAR 10-K FY2025 Item 7（as_of 2026-01-29）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年汽車銷售成本下降，部分被關稅增加抵銷。
  - 來源：SEC EDGAR 10-K FY2025 Item 7（as_of 2026-01-29）｜affects：valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Musk 稱中國稀土磁鐵供應中斷延誤 Optimus 關鍵零件，北京要求出口許可
  - 來源：The Register: Tesla's Optimus can't roll without rare earth magnets（as_of 2025-04-23）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 總營收約 $28.05B，與去年同期 $28.095B 大致持平；汽車營收約 -3% 至約 $20.6B，法規積分收入降至 $113M（去年 $417M）；服務及其他營收 +33% 至約 $4.6B。
  - 來源：Electrek, Tesla Q3 2026 financial results（as_of 2026-10-21）｜affects：thesis.R、valuation
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Q3 2026 能源發電與儲能營收 -16% 至約 $2.9B，儘管部署量 +10% 至 13.7 GWh（低於分析師預期約 15.9 GWh）；公司部分歸因於關稅相關客戶退款。
  - 來源：Electrek, Tesla Q3 2026 financial results（as_of 2026-10-21）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Waymo 以光達＋雷達＋相機路線領先 Tesla 純視覺 robotaxi 部署規模
  - 來源：The Great Robotaxi Race: A Look at Tesla's Competition (notateslaapp)（as_of 2026-03-18）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Tesla 於 2026 Q1 財報後把 2026 年資本支出指引上調至至少 250 億美元（1 月為 200 億），並預期本年其餘時間自由現金流為負；Morningstar 維持 400 美元公允價值。
  - 來源：Morningstar, Tesla Earnings: Shares Fall Slightly as Management Raises Capital Expenditure Guidance（as_of 2026-04-23）｜affects：decision_inputs.bear、valuation
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Tesla 公司彙編的分析師共識：2026 全年交付約 165 萬輛（3 月時約 169 萬，再早為 175 萬），共識被下修；Tesla 未提供正式交付量指引。
  - 來源：Electrek, Tesla Q1 2026 delivery consensus; Automotive World（as_of 2026-03-26）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：美國證券集體訴訟（W.D. Texas，Autopilot／FSD／Robotaxi 陳述）：修正訴狀 2026-02-17，Tesla 於 04-20 聲請駁回，最新 10-Q 稱已完成briefing，未見裁決。
  - 來源：Tesla 10-Q（截至 2026-09-30）（as_of 2026-10-22）｜affects：decision_inputs.bear、thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：NHTSA 正評估是否就 robotaxi 學區超速請願開正式調查（期限約 2027-01-21），並另就 Cybercab 無踏板／方向盤的自我認證發出查詢。
  - 來源：The Star｜Tesla faces US probe over claim of robotaxis speeding in school zones（as_of 2026-10-13）｜affects：decision_inputs.bear、triggers
- `major_events#5`（major_events｜方向 -｜狀態 ok）：2026 年多起 NHTSA 召回（26V445、26V315、26V255、26V558 等）。
  - 來源：NHTSA recall report 26V445（as_of 2026-04-01）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：W.D. Texas 證券集體訴訟（Autopilot／FSD／Robotaxi）駁回聲請已briefing完畢，未見裁決；另有 2026-06-04 N.D. Cal. 集體訴訟。
  - 來源：Tesla 10-Q（截至 2026-09-30）（as_of 2026-10-22）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2018 CEO 績效獎勵訴訟：法院判決應撤銷，原告律師費判 $345 million。
  - 來源：Tesla 10-K FY2025 Note 13（as_of 2026-01-29）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA 評估 robotaxi 學區超速請願是否開調查，並對 Cybercab 認證發出查詢。
  - 來源：The Star（as_of 2026-10-13）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":840.0,"bear_5y_price":73.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-18.7,"ev5y_pct":-1.1,"irr_base_pct":-4.1,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.77,"pe":210.29,"basis":"FY2026E 共識 EPS 1.77 美元（Koyfin），與終端倍數同為前瞻口徑"},"eps":{"bull":[2.3,3.6,5.5,8.3,12.0],"base":[2.1,2.9,3.7,4.6,5.5],"bear":[1.6,1.5,1.7,1.9,2.1]},"pe":{"bull":70,"base":55,"bear":35},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TSLA_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明自由現金流本季為負，原因是資本支出季增超過一倍，且下半年預期再增加（原話："CapEx more than doubled sequentially"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 表示資本支出未來兩三年持續成長（全年指引為超過 250 億美元，見同段上一句）（原話："CapEx will grow for the next 2 or 3 years as we expand our"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 表示研發為主的營運費用 2026 年及之後會持續成長（原話："we are in a big investment cycle"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明量產成長受供應鏈限制，不只電池也包括電子零件（原話："Production growth will be limited by our supply chain."）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 說明已取得最高可借 300 億美元的債務額度（原話："the capacity to borrow up to $30 billion"）
- 2026-07-22｜Vaibhav Taneja｜guidance：CFO 預期機器人計程車車隊成長在年內加速，並擴展到新的美國市場（原話："have expanded to a total of 7 markets in"）
- 2026-07-22｜Ashok Elluswamy｜guidance：Ashok 表示預期無人監督里程的高複利成長在今年剩餘時間持續（原話："we expect to continue growing at such a large rate"）
- 2026-07-22｜Elon Musk｜guidance：Musk 說明 Semi 自駕預計年底或明年初可運作，但未來約六個月排在次要（原話："taking a bit of a backseat for the next 6"）
- 2026-07-22｜Elon Musk｜guidance：Musk 說明 AI5 預計明年中進入量產，且最先用在 Optimus（原話："AI5, which hopefully is in volume production"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告汽車毛利率（不含碳權）由 19.2% 降至 16.3%（原話："declined sequentially from 19.2% to 16.3%"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 說明上季有 2.3 億美元保固回沖與關稅減免，本季未重複（原話："we had a $230 million benefit from warranty true-downs and"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 的數字口徑：扣除上季一次性效益後，汽車毛利率大致持平（原話："excluding credits, would have been approximately flat"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 指出利率上升使利息補貼成本增加，對汽車毛利率有負面影響（原話："the cost of subvention has risen along with them"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告儲能毛利率由 39.5% 降至 20.4%（原話："energy gross margins declined from 39.5% to 20.4%."）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 拆解儲能毛利下滑原因之一為約 2.4 億美元保固補提（供應商電芯問題）（原話："First, there was a warranty true-up in the quarter"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 給出儲能長期毛利率區間（原話："gross margin rate in the mid- to low 20% range"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 報告服務及其他毛利率創高（原話："improved sequentially from 9.2% to 14.1%, an all-time high"）
- 2026-07-22｜Vaibhav Taneja｜margin：CFO 說明淨利含 SpaceX 持股約 10 億美元的市價評價利得（原話："a mark-to-market gain of $1 billion on our SpaceX holdings,"）
- 2026-07-22｜Vaibhav Taneja｜competition：CFO 提到工業儲能均價在競爭加劇下下降（先前已預告）（原話："industrial storage is coming down amidst growing competition"）
- 2026-07-22｜Ashok Elluswamy｜competition：Ashok 主張純鏡頭方案的安全紀錄可驗證其技術路線，反駁需要光達的說法（原話："and affordable autonomy with just cameras"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 說明期末訂單積壓為 2023 年以來最大（原話："We exited Q2 with our largest order backlog since 2023."）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 揭露北美約 55% 交車在交付時已啟用 FSD 訂閱（原話："about 55% of our deliveries had FSD subscription"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 揭露 FSD 全球付費客戶數（原話："reaching nearly 1.5 million paid customers"）
- 2026-07-22｜Vaibhav Taneja｜customer：CFO 說明 FSD 變現成長主要來自訂閱，因多數市場已移除買斷選項（原話："the growth in FSD monetization will come from subscriptions"）
- 2026-07-22｜Elon Musk｜customer：Musk 說明儲能需求預期很高，並稱電池可使美國發電量近乎翻倍（原話："demand for Megapack being very, very high in the future"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 表示今年是大規模資本支出年（原話："this is a massive CapEx year"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 說明資本支出寧可資本效率略低也要更快完成（原話："it's okay to be a little less capital efficient"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 提到已下單採購 Austin 開發用晶圓廠設備（原話："We've placed equipment orders for our development fab"）
- 2026-07-22｜Brandon Ehrhart｜capital_allocation：法務長說明今年稍早與 SpaceX 透過投資與框架協議深化關係（原話："we deepened our relationship through an investment"）
- 2026-07-22｜Elon Musk｜capital_allocation：Musk 提到可在超充站部署 Megapod 分散式 AI 運算，超充站電力約 7 GW（原話："something like 7 gigawatts of power at our Superchargers"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Cybercab 已開始量產（原話："The Cybercab has started production"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Optimus 即將開始量產（原話："we will soon start production with Optimus"）
- 2026-07-22｜Elon Musk｜product：Musk 校準預期：Optimus 量產曲線前段會又平又長（原話："curve will be quite flat and long"）
- 2026-07-22｜Elon Musk｜product：Musk 稱 Optimus 是 Tesla 迄今最難量產的產品（原話："product to scale manufacturing that we've ever made at Tesla"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Optimus 4 將在 Austin 生產，垂直整合程度更高（原話："For Optimus 4, which will be built in Austin"）
- 2026-07-22｜Elon Musk｜product：Musk 給出 Optimus 4 對 Optimus 3 的產能願景（加上多項但書）（原話："aspirationally 10 million units a"）
- 2026-07-22｜Ashok Elluswamy｜product：Ashok 說明早期 v15 版本已在機器人計程車車隊上運行，七條改進主軸已併入四成（原話："40% of those tracks merged"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Cybercab 因底盤全新，需先累積專屬行駛資料才能大量上路（原話："to accumulate driving data that is specific to the Cybercab"）
- 2026-07-22｜Elon Musk｜product：Musk 說明舊款（低於 Hardware 4）車輛未來將升級，計畫以下一代 AI 板為目標（原話："upgrade all cars with that are -- have less than Hardware 4"）
- 2026-07-22｜Elon Musk｜product：Musk 說明 Semi 的自駕工作排在 Model 3/Y 與 Cybercab 之後（原話："get self-driving working on the Tesla Semi"）
- 2026-07-22｜Elon Musk｜risk：Musk 說明機器人計程車的限制是安全可靠度，並稱任何傷人事件都會招致監管收緊（原話："the march of nines of reliability is, I think, the only"）
- 2026-07-22｜Lars Moravy｜risk：Lars 對紐澤西州的州級規定表示失望（原話："the stuff in New Jersey is a little bit"）
- 2026-07-22｜Elon Musk｜risk：Musk 表示若無 Terafab，Optimus 量產會受 AI 晶片供給限制（原話："constrained in our ability to scale Optimus production"）
- 2026-07-22｜Ashok Elluswamy｜risk：Ashok 稱至今 38 萬英里無人監督行駛無重大事故（原話："0 notable incidents over 380,000 miles."）
- 2026-07-22｜Elon Musk｜risk：Musk 感謝 Micron 在記憶體價格極高下給予 Tesla 大量配額（原話："a very significant allocation on reasonable terms"）
- 2026-07-22｜Elon Musk｜commitment：Musk 承諾機器人計程車維持垂直整合、不引入第三方叫車平台（原話："We expect to be vertically integrated with robotaxi"）
- 2026-07-22｜Ashok Elluswamy｜commitment：Ashok 表示新城市上線時間預期趨近於零，目標以整州為單位營運（原話："time to launch to a new city will continue to trend"）
- 2026-07-22｜Ashok Elluswamy｜commitment：Ashok 表示 Cybercab 製造目標與無人監督里程成長率大致對齊（原話："We have aligned our manufacturing targets to roughly"）
- 2026-07-22｜Elon Musk｜commitment：Musk 表示 Terafab 地點將於日後單獨發表，不在法說會上說明（原話："we expect to announce a location soon"）

### 問答異常語氣（迴避／改口／保留）
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Colin Langan（Wells Fargo）問 Musk 是否看到 Tesla 與 SpaceX 合併的綜效、是否合理｜答法：Musk 未正面回答合併問題，表示不能在法說會討論，轉交法務長；法務長只談現有合作與框架協議
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：William Stein（Truist）追問 Optimus 4 何時開始量產｜答法：Musk 接著只回答硬體升級與 AI5/AI6 晶片，未給 Optimus 4 的開始量產時程
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Dan Levy（Barclays）問儲能是否長期供給受限，以及資料中心與電網調峰的需求占比｜答法：Musk 談電網平衡、資料中心電力平滑與美國發電量論述，未回答供給是否受限，也未給資料中心與調峰的占比數字
- TSLA_Q2_2026_Earnings_Call_20260722.md｜問：Colin Langan 追問為何不先在一兩個城市把車隊規模做大（媒體報導車數僅數十輛）｜答法：管理層以里程成長、跨城市驗證通用性、各城市監管不同回應，未給車隊車輛數

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 3 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 6 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260705","verdict":"迴避","role":"不持有/迴避","H":{"status":"ok","format":"table","rows":[{"id":"H1｜robotaxi 規模化","text":"FSD v15（~10B 參數）在 2026 末/2027 上線後，unsupervised 車隊由現 ~20 台放大至數千台、擴至 5+ 城市，形成可營運的自駕網絡。Floor：2027 底 unsupervised 車隊 >1,000 台且營運 ≥5 城；來源：Tesla 指引 FSD v15 late-2026/early-2027（techtimes 2026-06-10）","columns":{"時間軸":"2Y：v15 上線＋Dallas/Houston 規模化5Y：多城數萬台10Y：自駕網絡貢獻 EPS 主體","驗證指標 / 漂移觸發":"車隊台數（Robotaxi Tracker）、營運城市數。漂移：v15 延至 2027H2 或上線後 6 個月車隊"}},{"id":"H2｜汽車毛利觸底回升","text":"Auto GM（ex-credit）自 2025 的 17.9% 谷底回穩，Q1'26 已回到 19.2%；新平台（低價車、Cybertruck 效率）＋規模＋軟體吸附（FSD 訂閱）讓每車毛利止跌。Floor：FY2026 Auto GM ex-credit 全年 ≥18%；來源：Q1 2026 財報 electrek 2026-04-22","columns":{"時間軸":"2Y：GM 站穩 18-20%5Y：軟體佔比拉高毛利結構10Y：混合毛利 >25%","驗證指標 / 漂移觸發":"季度 Auto GM ex-credit、FSD 訂閱轉化率。漂移：連 2 季 Auto GM ex-credit"}},{"id":"H3｜能源第二曲線","text":"能源儲存（Megapack/Powerwall）維持高速成長，成為毛利與成長的穩定貢獻者，抵銷汽車週期性。Floor：能源部署年化 ≥40 GWh、營收 YoY >25%；來源：Q2 2026 部署 13.5 GWh（IR 2026-07-02）","columns":{"時間軸":"2Y：年化 50+ GWh5Y：能源毛利佔比 >20%10Y：獨立成長引擎","驗證指標 / 漂移觸發":"季度 GWh 部署、能源毛利率。漂移：能源部署 YoY 轉負連 2 季 → H3 削弱"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","irr_base_pct":-2.7,"ev5y_pct":-12.0,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有/迴避","signal":"B","val":"🔴","ma":"🟡","trap":"🟡","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":0.7,"ev5y_pct":-12.0,"irr_base_pct":-2.7,"max_dd_pct":-65.0,"bull_5y_price":660.0,"bear_5y_price":91.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","price_at_dd":393.45,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TSLA","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Tesla, Inc."},"oneliner":"車業利潤薄、估值押在無人車：Fwd P/E 約 210 倍，基本情境五年後約 303 美元仍低於現價，等股價回到 250 美元或無人車營收證據到位再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是買車的人和電網、資料中心客戶的錢，錢卡在汽車硬體毛利：Q3 營收 280.5 億美元年持平，GAAP 營業利益率只有 2.6%，研發與折舊把汽車毛利幾乎吃光","reasoning":"分部（Electrek 2026-10-21 引 Q3 財報）：汽車約 206 億美元（約 73%，年減約 3%，法規積分由 4.17 億降到 1.13 億美元）、能源約 29 億美元（約 10%，年減 16%）、服務及其他約 46 億美元（約 16%，年增 33%，含超充、保險與 Robotaxi）。汽車 GAAP 毛利率 18.5%，不含積分由上季 16.3% 升到 18.1%，CFO 歸因亞太交車占比提高；能源毛利率 33.1% 含關稅退款與供應商保固分攤。交付 486,532 輛、儲能部署 13.7 GWh，公司不給量化指引。單點依賴：電池電芯產能是整車量產限制，記憶體靠 Micron 配額，稀土磁鐵受中國出口許可影響；客戶端為個人與電網客戶，10-K 集中度附註待核，未見單一客戶達 10% 的揭露。產業時鐘判收縮期：GM、Ford、Rivian 的營業利益率分別為 0.98%、−3.74%、−60%，BYD 5.25%，美國稅收抵免結束後 EV 零售占比降到 6.2%，產業利潤在收縮。供需持久性：週期性將反轉為主，Q3 交付超預期多篇歸因高油價與庫存去化，屬可逆的順風。產業態勢為雙向拉鋸：競爭惡化（中國品牌西歐份額創 10.7% 新高、Waymo 無人車規模領先）對結構轉好（FSD 改為純訂閱、儲能資料中心需求），其他結構變數為關稅與無人車監管。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi6_gaap","f_kpi7","f_kpi8","f_kpi9","f_peer_gm_operating_margin_pct","f_peer_f_operating_margin_pct","f_peer_rivn_operating_margin_pct","f_peer_1211_hk_operating_margin_pct"],"verdict_values":{"revenue_quality":"汽車硬體一次性銷售約占 73%；經常性收入（FSD 訂閱年化約 10 億美元、超充、保險、Robotaxi）在服務及其他項下年增 33%；法規積分由 4.17 億降到 1.13 億美元，低品質收入在退場","unit_econ_note":"New Street 估每車售出當下毛利約 7,000 美元、FSD 每年逾 1,000 美元，CFO 認可方向；Robotaxi 每英里成本尚未達 0.30 美元目標，管理層未給現值","archetype":{"primary":"轉機/特殊情境","secondary":"循環/商品","confidence":"中","fingerprint":"EPS 由 2023 年 4.31 美元降到 2025 年 1.08 美元、營業利益率由 17% 降到最新一季 2.6%，價值押在無人車、Optimus、儲能能否商業化"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉為主：Q3 交付超預期多篇歸因高油價與庫存去化，交付高於產量約 2.2 萬輛；美國稅收抵免結束後 EV 零售占比降 3.6 點至 6.2%；同業營業利益率 GM 0.98%、Ford −3.74%、BYD 5.25%，產業利潤收縮","bargaining":{"up":"上游偏強：管理層稱電池產能是全球量產限制，記憶體在高價下靠 Micron 配額，中國稀土磁鐵需出口許可","down":"直營無經銷商、終端定價自主，但需以融資補貼抵銷利率上升，汽車硬體議價力有限；FSD 訂閱是定價力最強的一段","geo":"中國與德國設廠緩衝汽車關稅；要求供應商把顯示器、ECU、PCB 移出中國與台灣；關稅對儲能電芯成本衝擊大於汽車"},"profit_pool_dir":"汽車利潤池由硬體移向軟體與服務（FSD 訂閱、Robotaxi），硬體端被中國品牌與價格戰擠壓；儲能利潤受關稅與工業儲能均價下滑影響","tam_table":[{"item":"美國 EV 市場 Q3 2026 銷量","value":"262,649 輛，Tesla 約 144,094 輛、份額約 54%（Cox 估計）"},{"item":"全球 BEV 份額 2026Q2","value":"Tesla 13%（Q1 11%），BYD 約 12%（Counterpoint）"},{"item":"西歐 18 國份額 2026Q2","value":"Tesla 2.6%（去年同期 1.7%），中國品牌合計 10.7% 創新高"},{"item":"美國 EV 零售占比","value":"稅收抵免結束後降 3.6 點至 6.2%（J.D. Power 引 Reuters）"},{"item":"儲能部署","value":"2025 年 46.7 GWh；2026 年前三季 8.8＋13.5＋13.7 GWh；管理層稱 2027 年 Megapack 幾乎售罄"},{"item":"Robotaxi 與 Optimus 的市場規模及利潤池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：汽車硬體定價權仍在流失，但 FSD 訂閱附加率與車隊資料規模擴大，兩者抵銷；綜合等級 C","reasoning":"機制是車隊資料規模加垂直整合：FSD 以全車隊資料訓練端到端模型，Cybercab 零件比過去任何車款少 50%，直營通路與自有超充網。可證方向：對最強同業 BYD，TTM 毛利率 18.85% 對 17.76% 小幅領先，但營業利益率 4.61% 對 5.25% 落後，報酬差距為負；對 GM、Ford、Rivian 則大幅領先。份額面 Q2 全球 BEV 13% 高於 BYD 12%、美國 EV 約 54%。執行力 7 分：北美 FSD 交車附加率由約 55% 升到逾 75%，全球付費客戶逾 170 萬，Cybercab 已量產。定價權 5 分：汽車毛利率由 2022 年 25.6% 降到 18% 上下後持平，需以融資補貼抵銷利率，法規積分萎縮；FSD 訂閱是唯一在變強的定價點，但其他車廠可能用 Nvidia、Qualcomm 方案追上並壓低價格（2026-10-21 法說 RBC 提問，管理層只說問題很難，未給數字反駁）。綜合 6 分。當期 ROIC 偏低：稅後營業利益率不到 4%，投入資本周轉率事實表未涵蓋。","fact_refs":["f_peer_tsla_gross_margin_pct","f_peer_tsla_operating_margin_pct","f_peer_tsla_fcf_margin_pct","f_peer_1211_hk_gross_margin_pct","f_peer_1211_hk_operating_margin_pct","f_peer_1211_hk_fcf_margin_pct","f_peer_gm_gross_margin_pct","f_peer_gm_operating_margin_pct","f_peer_f_gross_margin_pct","f_peer_f_operating_margin_pct","f_peer_rivn_gross_margin_pct","f_peer_rivn_operating_margin_pct","f_kpi6_gaap"],"verdict_values":{"moat":{"mechanism":"車隊資料規模加垂直整合：全車隊資料訓練 FSD、自產 LFP 電芯與自研晶片、Cybercab 零件數少 50%、直營與自有超充網","execution":7,"pricing":5,"combined":6,"score":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大（FSD 附加率約 55%→逾 75%、付費客戶近 150 萬→逾 170 萬、Cybercab 量產），定價權縮減（汽車毛利率 2022 年 25.6%→2025 年 18.03%、法規積分萎縮、融資補貼增加），合計持平；營業利益率仍低於 BYD，不足以標擴大","competitor_notes":[{"name":"1211.HK（BYD）","strategy_note":"毛利率 17.76% 接近 Tesla、營業利益率 5.25% 反而較高，FCF 利潤率 −6.5% 顯示擴產激進，是份額與成本上最強的對手"},{"name":"GM","strategy_note":"毛利率 5.74%、營業利益率 0.98%，電動化拖累利潤，成本上不構成威脅，但可外購 L2+ 方案在輔助駕駛上追趕"},{"name":"F","strategy_note":"營業利益率 −3.74%，價格戰承受力最弱，對 Tesla 定價的壓力有限"},{"name":"RIVN","strategy_note":"營業利益率 −60%、FCF 利潤率 −59%，規模未成，短期無威脅"},{"name":"Waymo","strategy_note":"無人車規模領先，多感測器路線成本較高但安全冗餘較強；財務數字事實表未涵蓋"}],"threats":[{"level":"🔴","text":"中國品牌在西歐份額創 10.7% 新高、BYD 全球 BEV 份額 12% 逼近；10-K 自承競爭加劇可能導致降價與份額流失","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"level":"🔴","text":"Waymo 以光達＋雷達＋相機路線領先無人車部署規模，Zoox、Uber 與 Lucid、Nuro 陸續進入；若多感測器路線先取得監管信任，純視覺路線的成本優勢換不到市場","p":"40%","evidence_refs":["competitive_share_entrants#5","substitute_technology#0"]},{"level":"🟡","text":"其他車廠借 Nvidia 或 Qualcomm 方案推出 L2+ 產品，壓低 FSD 訂閱價格（2026-10-21 法說 RBC 提問）","p":"30%","evidence_refs":[]},{"level":"🟡","text":"中國反壟斷民事訴訟指控限制獨立維修商取得維修軟體，若成立將削弱售後服務的封閉性","p":"15%","evidence_refs":["regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"低利益率×低周轉（周轉率事實表未涵蓋，以重資本擴張判讀）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"個人購車時使用者、決策者、付款者重合，需求成立；但有週期成分：Q3 超預期部分歸因高油價，美國稅收抵免結束後 EV 零售占比降到 6.2%。訂單積壓四年最高、交付高於產量約 2.2 萬輛是正面讀數"},{"item":"決策層級","level":"🟡","text":"FSD 為月訂閱，客戶隨時可退，轉換成本低；流失率管理層承諾日後揭露但目前未給。北美逾 75% 交車簽付費訂閱（每車已含一個月免費仍簽），是黏著度的初步代理"},{"item":"價值鏈分配","level":"🟡","text":"電池電芯與記憶體是瓶頸：管理層稱電池產能限制量產，記憶體在高價下靠 Micron 配額；儲能已開始用自產 LFP 電芯出貨，收回部分價值，但上游議價力仍偏強"},{"item":"社會容忍度","level":"🔴","text":"Robotaxi 能否營運取決於監管授權：NHTSA 正評估學區超速請願並查詢 Cybercab 無踏板的自我認證，Musk 自承任何傷人事件都會招致監管收緊，也說除非被政府擋下才能拿下多數客運里程。授權可被收回，是定價上限的政策風險，已列入反證紀錄"}],"roiic":"負值（推估）：2022→2025 年營收增約 134 億美元，營業利益由約 138 億降到約 48 億美元，減約 90 億；投入資本與 D&A 事實表未涵蓋，無法算精確值","reinvest_rate":"遠高於 100%：2026 年資本支出約 200 億美元（2026-10-21 CFO），對照 TTM 營業利益率 4.61%、Q3 營業利益 7.18 億美元；D&A 與營運資金變動事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；增量報酬為負時內生上界沒有意義，留空白，共識成長全部要靠新事業的利潤率擴張"}}}},"q3_growth":{"verdict":"五年後跑道中：汽車本業在美國 EV 份額已逾五成，無人車與 Optimus 還沒有營收證據，儲能營收本季年減 16%","reasoning":"成長來源以量為主：交付年減 2%、儲能部署年增 10%、服務及其他年增 33%；價格面法規積分萎縮、融資補貼增加；無併購、無回購。共識 EPS FY2026E 1.77、FY2027E 2.16、FY2028E 3.22 美元（Koyfin 快照，家數事實表未涵蓋），兩年年化約 35%；近 3 個月 FY1 下修 0.56%，本期 FY2、FY3 各下修 1.37%、2.42%。內生上界：增量報酬為負，既有資本報酬撐不起任何成長，缺口全部歸因於利潤率擴張（研發投入回收、無人車與 FSD 高毛利），信心上限中。跑道：Tesla 在美國 EV 份額約 54%，介於 35%～70%；無人車管理層稱 2027 年 Q2 起才明顯、Optimus 對外交貨約 2027 年底、Terafab 量產晶片約 2028 年，都還不是已證實的第二曲線，所以不給寬跑道。衰退信號亮兩個：EPS 成長遠高於營收成長、美國 EV 零售占比下滑。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi7","f_kpi8"],"verdict_values":{"growth":{"driver_mix":"量為主：汽車交付年減 2%、儲能部署年增 10%、服務及其他年增 33%；價格面法規積分萎縮、融資補貼增加；無併購、無回購","runway_years":"事實表未涵蓋（全球滲透率資料缺）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬為負（2022→2025 營收增約 134 億美元、營業利益減約 90 億），內生上界無法支撐共識 FY2026E→FY2028E 年化約 35% 的 EPS 成長；缺口歸因利潤率擴張，無法用既有資本報酬驗證，依賴新事業與重新評價","segments":[{"item":"汽車","value":"Q3 約 206 億美元，年減約 3%；GAAP 毛利率 18.5%，不含積分 18.1%"},{"item":"能源發電與儲能","value":"Q3 約 29 億美元，年減 16%；部署 13.7 GWh 年增 10%；毛利率 33.1%（含關稅退款與保固分攤）"},{"item":"服務及其他（含 Robotaxi）","value":"Q3 約 46 億美元，年增 33%；毛利率 15.9% 創新高"}],"decay_signals":["EPS 成長遠高於營收成長：共識 FY2026E→FY2028E EPS 年化約 35%，營收本季年持平","市場規模壓縮：美國稅收抵免結束後 EV 零售占比降 3.6 點至 6.2%"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：進入大投資期，本季自由現金流 15.31 億美元扣掉 SBC 後只剩約 3.7 億美元，無回購無股息，還有 SpaceX 合併與 Terafab 分攤的關係人問題","reasoning":"現金去向：本年資本支出約 200 億美元（2026-04 曾指引至少 250 億），未來幾年持續擴大到 Robotaxi 車隊、Optimus 產能、太陽能、AI 算力與晶圓廠；Terafab 至 2028 年初投入數百億、長期逾千億美元，與 SpaceX 的分攤未定。期末現金與投資逾 450 億美元，2026-09-29 簽 200 億美元延遲提款定期貸款與合計 100 億美元循環額度，今年不動用。SBC 單季 11.65 億美元，占營收約 4.15%。併購：無重大併購，不適用；回購：公司不回購，不適用；淨稀釋率：股數序列事實表未涵蓋，無法判定。治理：2018 年 CEO 績效獎勵遭判撤銷、原告律師費 3.45 億美元；SpaceX 合併只成立特別委員會，條款未定。FCF 對淨利轉換率的年度序列事實表未涵蓋。","fact_refs":["f_kpi4_gaap","f_kpi5_sbc","f_kpi0_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無重大併購"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"公司不回購、不配息"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 單季 11.65 億美元、占營收約 4.15%；稀釋股數序列事實表未涵蓋，淨稀釋率無法計算"}]},"governance":{"capital_returns":{"expanded":false,"reason":"公司未配息、未回購，成長靠自有資本支出而非併購，沒有股東回饋紀錄可展開"}}}},"q5_valuation":{"verdict":"現價要市場相信無人車與 Optimus 照管理層時程兌現：以 55 倍終端倍數倒推，2031 年 EPS 須達約 6.8 美元，是基本情境的 1.2 倍。我不信這是基本情境","reasoning":"Fwd P/E 210 倍（FY2026E 共識 1.77 美元），以 FY2027E 計 172 倍；PEG 約 6（FY2026E→FY2028E 共識年化約 35%）。五年估值分位：事實表只有近期一點，不外推，留空白。分母受研發與折舊壓低，但即使把營業利益率還原到 2023 年的 9.19%，獲利約翻倍，倍數仍逾百倍，分母不是爭點。賣方平均目標價約 408 美元（2026-09 初，非最新），較現價高 9.6%；目標價全距 25～600 美元，最高對最低逾 20 倍，分歧極大，下調對自身情境的信心。基本情境五年終點約 303 美元，較現價低 18.7%。同業前瞻倍數事實表未涵蓋，不跨類比較。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2026E 共識 EPS）","peers":{"expanded":false,"reason":"事實表未收同業前瞻倍數；GM、Ford、BYD、Rivian 只有利潤率，不能當倍數錨"},"fwd_pe":210.29,"peg":6.03,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"Fwd P/E 210 倍、FY2027E 172 倍，PEG 約 6（共識兩年年化約 35%），遠高於 2 的偏貴線；基本情境五年終點低於現價","upside_short_pct":9.6,"upside_mid_pct":-18.7,"denominator_disputed":false,"denominator_note":"分母受投資期研發與折舊壓低，但把營業利益率還原到 2023 年 9.19% 後倍數仍逾百倍，結論不因分母改變"}}},"q6_how_wrong":{"verdict":"最可能看錯在無人車速度：若 Robotaxi 在 2027 年真的成為主要利潤，現在的 EPS 是谷底，210 倍會被快速消化","reasoning":"反方最強數字：FSD 年化經常性營收約 10 億美元、北美附加率季增約 20%、無人里程每週雙位數成長、Cybercab 產線額定年產逾 12.5 萬輛且可再提高、Megapack 2027 年幾乎售罄。我方會看錯的條件見反證紀錄。動能中性：26 週報酬 −1.08%、RSI 51.5、週線均線排列過但長均線走平；近三個月共識小幅下修。上一季法說有四處未正面回答（車隊規模、儲能資料中心占比、Optimus 4 量產時程、SpaceX 合併），都是估值關鍵資訊。歷史最大回撤事實表未涵蓋；空方最低目標價 25 美元屬賣方個例。","fact_refs":["f_rsi14","f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"新事業故事撐估值、本業利潤收縮，陷阱風險中"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.77,"pe":210.29,"basis":"FY2026E 共識 EPS 1.77 美元（Koyfin），與終端倍數同為前瞻口徑"},"eps":{"bull":[2.3,3.6,5.5,8.3,12.0],"base":[2.1,2.9,3.7,4.6,5.5],"bear":[1.6,1.5,1.7,1.9,2.1]},"pe":{"bull":70,"base":55,"bear":35},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-82,"hi":-50,"basis":"下緣 −82%：Bear 終點約 74 美元（EPS 2.1 美元×35 倍），較現價跌約 80%，再留過衝空間；上緣 −50%：即使走基本情境，倍數由 210 倍壓到約 100 倍、乘 FY2027E 共識 2.16 美元約 216 美元，跌約 42%，加情緒過衝。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"無人車照管理層時程：2027 下半年 Robotaxi 成為主要利潤、客戶車輛加入車隊、Optimus 2028 年起對外放量、儲能毛利維持高檔；2031 年 EPS 12 美元，倍數 70 倍","base":"汽車持平微增、儲能穩定成長、FSD 訂閱與 Robotaxi 2028 年後逐步貢獻，研發與折舊仍高；2027–2028 略低於共識，2031 年 EPS 5.5 美元，倍數收斂至 55 倍（同業前瞻倍數事實表未涵蓋，以 2031 年後 EPS 年增約 10% 校準）；淨稀釋事實表未涵蓋，殖利率以 0 計","bear":"交付停在 160～170 萬輛、融資補貼與關稅壓毛利、無人車因監管或事故停在小規模；2031 年 EPS 2.1 美元，倍數向高成長車廠收斂至 35 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"無人車被監管或事故卡住：NHTSA 評估學區超速請願（期限約 2027-01-21）並查詢 Cybercab 自我認證、FSD 調查延長、2026 年多起召回；10-K 稱若主管機關日後採取行動，可能面臨責任、罰款與限制性制裁","assumption":"多頭假設監管會跟著安全數據放行，2027 年 Q2 起開放客戶車輛加入車隊","consequence":"無人車營收延後兩年以上，估值回到車廠加儲能，倍數向 35 倍收斂，五年後股價約 70～80 美元","ruling":"採納：這是五年後虧五成最可能的故事，與唯一致命事件部分重疊（致命事件是其中最尖銳的一種），Bear 機率 30% 反映此路徑；社會容忍度判紅記在這裡","watch":"NHTSA 立案與召回公告、無人營運城市數與營運時段是否收縮","evidence_refs":["regulatory_antitrust#0","major_events#3","major_events#5","product_recall_warning#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Cybercab 主要由 Tesla 自有、以運輸服務營運，車隊要用資產負債表買；Terafab 長期逾千億美元、與 SpaceX 的分攤未定；SpaceX 合併只成立委員會；2018 年 CEO 獎勵訴訟判撤銷並付律師費 3.45 億美元，治理爭議未了","assumption":"無人車成功後利潤直接流到股東，不被資本支出與關係人交易吃掉","consequence":"營收與里程成長，但自由現金流長期為負、需借款或換股，每股價值成長遠低於業務成長","ruling":"採納：Bull 情境 EPS 不給到業務成長的幅度，並把合併條款列入複審事件","watch":"年度自由現金流、信貸額度動用、合併換股比例","evidence_refs":["capital_markets_pricing#0","lawsuit_class_action#1","major_events#1","major_events#0"],"fact_refs":["f_kpi4_gaap","f_kpi5_sbc"]},{"view":"價格已反映太多","evidence":"Fwd P/E 210 倍、FY2027E 172 倍；Q3 營收年持平、汽車營收年減約 3%；基本情境五年終點約 303 美元","assumption":"市場把管理層時程當成基本情境","consequence":"即使業務照基本情境走，五年報酬仍為負","ruling":"採納：這是本次不建倉的主因","watch":"股價對 FY2027E 共識的倍數，回到約 115 倍（約 250 美元）重新評估","evidence_refs":["end_markets#0"],"fact_refs":["f_fwd_pe_latest","f_price_at_dd","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"10-K：2025 年關稅調升與報復措施已推高供應鏈成本，汽車銷售成本下降被關稅部分抵銷；中國稀土磁鐵出口許可曾延誤 Optimus 關鍵零件","assumption":"量產擴大時零組件成本可控","consequence":"交付成長但毛利率被成本吃掉，Optimus 量產時程再延","ruling":"部分採納：中國與德國設廠能緩衝汽車關稅，但儲能與 Optimus 的零組件曝險較大；不預測關稅走向，以毛利率單季下滑≥2 個百分點作吸收失敗判定","watch":"汽車與能源毛利率、稀土出口許可消息","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 393.45 → 本次 372.22（-5.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=393.45","side_b":"本次 price_at_dd=372.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 迴避 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=迴避","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份裁決：護城河趨勢 ↓→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 不持有/迴避 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=不持有/迴避","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、護城河趨勢 ↓→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 393.45 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 393.45 美元：Bull 價 660、Bear 價 91，五年期望值 −12.0%，基準年化 −2.7%，不對稱比 0.7","side_b":"本次情境、股價仍用 393.45 美元：Bull 價 840、Bear 價 73.5，五年期望值 −6.4%，基準年化 −5.1%，不對稱比 1.16","ruling":"先換情境、股價不動：五年期望值多 5.6 個百分點，基準年化少 2.4 個百分點。不對稱比由 0.7 變為 1.16。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 393.45 美元：五年期望值 −6.4%，基準年化 −5.1%，不對稱比 1.16","side_b":"本次情境、股價 372.22 美元：五年期望值 −1.1%，基準年化 −4.1%，不對稱比 1.3","ruling":"再換股價、情境不動：起點價下跌 5.4%，五年期望值多 5.3 個百分點，基準年化多 1.1 個百分點，不對稱比由 1.16 升到 1.3。合計五年期望值比前份多 10.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"價格與估值","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份：股價 393.45 美元，估值偏貴，不持有並迴避；Bull 機率 25%、Bear 30%","side_b":"本次：股價 372.22 美元（−5.4%），Fwd P/E 仍約 210 倍，估值結論不變；Bull 25%、Bear 30% 不變","ruling":"跌幅不足以改變估值結論，機率不動；裁決與角色由本次輸入重新路由，價格變動本身不構成改判理由","evidence_level":"事實表股價與共識","settle_metric":"股價對 FY2027E 共識的倍數","if_then":["若股價跌到 250 美元以下而 H1～H3 無損：重跑研究後分批反買小額","反向：若股價續漲而無人車營收仍未揭露：不追"],"evidence_refs":[]},{"axis":"公司類型、綜合評級與回撤區間","cause":"方法變動","prior_field":["archetype","signal","cycle_position","max_dd_pct"],"side_a":"前份歸為品質複利成長，綜合評級 B，最大回撤 −65%（單點），循環位置空白","side_b":"本次改歸轉機／特殊情境（次類循環），綜合評級 C，回撤區間 −50%～−82%，循環位置仍空白","ruling":"EPS 由 2023 年 4.31 美元降到 2025 年 1.08 美元、營業利益率由 17% 降到最新一季 2.6%，增量報酬為負，不符合品質複利的定義；價值押在新事業能否商業化，屬轉機型，品質項連帶降一級。回撤改為區間，下緣加深是因 Bear 終點約 74 美元，區間必須涵蓋該跌幅。循環位置對轉機型不適用，維持空白","evidence_level":"事實表年度財報","settle_metric":"年度營業利益率與 EPS","if_then":["若 2027 年營業利益率回到 9% 以上且 EPS 超過 2023 年水準：改回品質複利評估","反向：若 2027 年營業利益率仍低於 5%：維持轉機型與 C 級"],"evidence_refs":[]},{"axis":"護城河方向、陷阱與跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河方向向下，陷阱風險中，五年後跑道中","side_b":"本次：護城河方向改為持平，陷阱風險與跑道維持中","ruling":"改持平的依據：北美 FSD 交車附加率由約 55% 升到逾 75%、全球付費客戶由近 150 萬升到逾 170 萬、FSD 年化經常性營收約 10 億美元（CFO 確認）、美國 EV 份額約 54%、全球 BEV 份額 13% 高於 BYD；毛利率自 2023 年起穩在 18% 上下，略高於 BYD 的 17.76%。但營業利益率仍低於 BYD（4.61% 對 5.25%），硬體定價權沒有恢復，所以只升到持平、不升到擴大。陷阱與跑道的證據方向未變","evidence_level":"公司法說與第三方份額統計","settle_metric":"北美 FSD 附加率與對 BYD 營業利益率差距","if_then":["若 FSD 附加率回落到 55% 以下或全球 BEV 份額連兩季低於 11%：護城河方向改回向下","反向：若營業利益率連兩季超過 BYD：考慮改為擴大"],"evidence_refs":["channel_business_model_shift#1","end_markets#3","competitive_share_entrants#2","competitive_share_entrants#4"]},{"axis":"重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","side_b":"股價≤250 美元（約 FY2027E 共識 115 倍）且汽車毛利率不含積分連兩季≥17%；或 Robotaxi 營收單獨揭露且年化≥50 億美元","ruling":"舊條件中「中國重回前 10」在本包沒有可驗證的資料來源，改用真正決定估值的無人車營收取代；毛利門檻由 19% 改 17%，因 Q2 落到 16.3%、Q3 回到 18.1% 靠亞太組合，17% 才是扣除一次性後的中樞；價位改用 FY2027E 共識 2.16 美元的 115 倍約 250 美元。觸發後只重啟完整研究，不直接加碼","evidence_level":"法說會與事實表共識","settle_metric":"股價、汽車毛利率、Robotaxi 營收揭露","if_then":["若任一條件成立：重跑完整研究，首筆僅小額","反向：若條件成立前出現監管暫停無人營運：重啟條件作廢"],"evidence_refs":[]},{"axis":"kill 指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標（空白）","side_b":"汽車毛利率不含積分連兩季<16%；能源毛利率扣除一次性<20%；自由現金流連兩季為負且動用新信貸；2027 年底無人營運<10 城或遭暫停","ruling":"新設：對持有者是減碼與清倉的依據，對本檔（不持有）是重啟評估的否決條件，任一觸發即取消重啟評估","evidence_level":"季度財報口徑","settle_metric":"各 kill 指標季度讀數","if_then":["若兩項以上同時觸發：持有者清倉","若僅一項觸發：持有者減碼一半並凍結加碼"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設定 Single Thing（空白）","side_b":"Single Thing：無人監督 Robotaxi 或 Cybercab 車隊發生致死或重傷事故，監管機關因此暫停或限制無人營運","ruling":"新設 Single Thing：Cybercab 已無人營運並快速擴車，NHTSA 學區超速請願與 Cybercab 認證查詢都是 2026-10 的新證據；這是估值最大的單一敏感項，發生時持有者清倉","evidence_level":"監管公告與法說會","settle_metric":"NHTSA 調查與召回公告","if_then":["若發生：持有者清倉，重啟條件作廢","反向：若 2027 年底前擴到 24 小時與高速路段仍無重大事故：Bear 機率下調 5 個百分點"],"evidence_refs":["major_events#3","product_recall_warning#0"]},{"axis":"論點門檻","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份：H1 2027 底無人監督車隊>1,000 台且營運≥5 城；H2 FY2026 汽車毛利率不含積分全年≥18%；H3 能源部署年化≥40 GWh、營收年增>25%","side_b":"本次：H1 2027 年底 FSD 付費客戶≥250 萬且無人營運≥10 城；H2 汽車毛利率不含積分每季≥17%、FY2027 交付≥185 萬輛；H3 2027 年部署≥60 GWh 且扣除一次性毛利率≥22%","ruling":"H1 改用付費客戶與城市數，因管理層不揭露車隊台數（2026-07-22 被問時迴避），舊門檻無法驗證。按舊門檻 H3 本季已不成立（能源營收年減 16%），H2 前三季約 17.9% 也在邊緣，兩者記為削弱，不因改門檻而抹掉；新門檻改看部署量與扣除一次性的毛利率，是因營收增速被關稅退款扭曲","evidence_level":"季度財報與法說會","settle_metric":"各假設門檻的季度讀數","if_then":["若新門檻連兩季未達：該假設改判反轉，減碼條件成立","反向：若 2027 年三項同時達標：重啟研究"],"evidence_refs":["end_markets#1"]},{"axis":"需求：管理層說法與數字","cause":null,"prior_field":null,"side_a":"管理層：需求快速成長、明顯超過產量，訂單積壓四年最高（Musk、CFO，2026-10-21 法說）","side_b":"數字：Q3 交付 486,532 輛年減 2%、營收年持平、汽車營收約 −3%；交付比產量多約 2.2 萬輛，靠庫存去化；超預期部分歸因高油價；共識交付在 2026 年 3 月曾被下修","ruling":"不可調和（方向相反），採數字側：積壓與交付超產量只說明短期供不應求，年比仍在下滑，且部分需求來自油價這種週期因素；交付恢復年增前不採信需求快速成長","evidence_level":"公司公告交付與第三方報導","settle_metric":"Q4 2026 與 2027 上半年交付年增率","if_then":["若 2027 上半年交付年增≥10% 且汽車毛利率不含積分≥17%：承認需求轉強，進入重啟評估","反向：若 Q4 2026 交付年減且交付低於產量：H2 削弱，維持不建倉"],"evidence_refs":["end_markets#0","capital_markets_pricing#2","supply_demand_durability#0"]},{"axis":"能源毛利率：前後說法","cause":null,"prior_field":null,"side_a":"CFO 2026-07-22：儲能長期毛利率在 20% 出頭到中段；Musk 2026-10-21：毛利率會明顯上升","side_b":"Q3 能源毛利率 33.1%，CFO 自承主要來自關稅退款與供應商保固分攤；能源營收年減 16%，部署 13.7 GWh 低於分析師約 15.9 GWh","ruling":"管理層一次性歸因不採信也不否定，標「未證、監測」：以 CFO 先前給的 20% 出頭為基準，扣除一次性後連兩季≥25% 才承認改口成立","evidence_level":"法說會原話與第三方財報整理","settle_metric":"扣除一次性後的能源毛利率","if_then":["若 Q4 2026 與 Q1 2027 扣除一次性後≥25%：H3 加強","反向：若任一季<20%：H3 削弱並觸發 kill 指標"],"evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"axis":"資本支出與現金流","cause":null,"prior_field":null,"side_a":"2026-04 財報後資本支出指引上調至至少 250 億美元並預期年內其餘時間自由現金流為負；2026-07-22 CFO 稱未來兩三年持續成長","side_b":"2026-10-21 下修本年資本支出至約 200 億美元、Q3 自由現金流逾 15 億美元；同時 Terafab 至 2028 年初投入數百億、長期逾千億美元，並簽 300 億美元信貸額度","ruling":"可調和（程度差異）：今年下修是時點遞延不是規模縮小，2027～2028 年支出仍上升；本季自由現金流扣掉 SBC 後只剩約 3.7 億美元，現金創造不足以自行支應","evidence_level":"法說會與 8-K","settle_metric":"2027 年資本支出指引與季度自由現金流","if_then":["若 2027 年自由現金流連兩季為負並動用新信貸：kill 指標觸發，取消重啟評估","反向：若 2027 年資本支出逾 300 億美元而自由現金流仍為正：上調 Base 情境現金流假設"],"evidence_refs":["capital_markets_pricing#0","major_events#1"]},{"axis":"無人車規模：說法與揭露","cause":null,"prior_field":null,"side_a":"管理層：無人里程每週雙位數成長、未來數月可擴到數百萬輛、2027 年無人車成為營收與獲利的重要部分","side_b":"未揭露車隊車輛數（2026-07-22 被問車隊規模時迴避）；營運市場由 Q2 稱的 7 個變成 Q3 的 6 個城市；每英里成本未達 0.30 美元目標；Musk 自稱本季不影響數字、2027 下半年才明顯","ruling":"不可裁決至 2027 年 Q2 財報：目前沒有車隊數、付費里程或營收，證據時間窗蓋不到估值所需的風險窗，不得把指數成長當成已證實","evidence_level":"法說會原話","settle_metric":"Robotaxi 營收或付費里程揭露","if_then":["若 2027 年 Q2 前揭露 Robotaxi 營收且年化≥50 億美元：重啟研究","反向：若 2027 年 Q2 仍未揭露任何營收或車隊數：H1 削弱，Bull 機率下調"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"多方：FSD 年化經常性營收約 10 億美元且附加率快速攀升、Cybercab 零件少 50%、Megapack 2027 年幾乎售罄、現金與投資逾 450 億美元；若無人車照時程在 2027 年成為主要利潤，現在的 EPS 是谷底","side_b":"本方：即使採基本情境 2031 年 EPS 5.5 美元，55 倍終端倍數只值約 303 美元，低於現價；要回到現價須假設 EPS 約 6.8 美元以上，等於把多頭情境當基本情境","ruling":"可調和（程度差異），採本方：分歧在時程與量級，不在方向。現在不追","evidence_level":"事實表共識與情境推算","settle_metric":"Robotaxi 營收揭露與股價對 FY2027E 倍數","if_then":["若股價≤250 美元而 H1～H3 無損：重跑研究後分批反買小額","反向：若 2027 年 Q2 前 Robotaxi 營收年化≥50 億美元而股價未同步上漲：放棄等價位，直接重啟研究"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FSD 付費客戶與無人營運城市是否達標","type":"假設驗證","maps_to":"H1","metric":"FSD 全球付費客戶數；無人監督營運城市數","threshold":"2027 年底≥250 萬且≥10 城","action":"達標且價位條件成立→重跑完整研究；落後→維持不建倉","source_freq":"季度更新簡報與法說會","date":"2027-12","evidence_refs":["channel_business_model_shift#1"]},{"n":2,"text":"汽車毛利率守住 17%","type":"假設驗證","maps_to":"H2","metric":"汽車毛利率（不含法規積分）","threshold":"每季≥17%；連兩季<16.2% 為削弱","action":"連兩季<16.2%→取消重啟評估","source_freq":"季度更新簡報","date":"2027-01","evidence_refs":["end_markets#0"]},{"n":3,"text":"能源毛利率扣除一次性後的真實水準","type":"假設驗證","maps_to":"H3","metric":"能源毛利率（扣除關稅退款與保固回沖）；年度部署量","threshold":"單季≥22%；2027 年部署≥60 GWh","action":"單季<20%→H3 削弱並列入 kill 指標","source_freq":"季度更新簡報與法說會","date":"2027-01","evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"n":4,"text":"NHTSA 是否就學區超速請願正式立案","type":"風險","maps_to":"R2","metric":"NHTSA 立案決定與範圍","threshold":"正式立案或要求暫停無人營運","action":"立案→凍結重啟評估至調查範圍明朗；持有者減碼一半","source_freq":"NHTSA 公告，事件型","date":"2027-01-21","evidence_refs":["major_events#3","product_recall_warning#0"]},{"n":5,"text":"無人車隊致死或重傷事故導致監管暫停","type":"Single Thing","maps_to":"Single Thing","metric":"監管暫停或限制無人營運","threshold":"任一州或聯邦層級暫停","action":"持有者清倉；重啟條件作廢","source_freq":"監管公告與公司聲明，事件型","date":null,"evidence_refs":["major_events#3"]},{"n":6,"text":"價位或無人車營收到位才重啟研究","type":"估值rearm","maps_to":"rearm","metric":"股價；汽車毛利率；Robotaxi 營收","threshold":"股價≤250 美元且汽車毛利率連兩季≥17%；或 Robotaxi 營收年化≥50 億美元","action":"重跑完整研究，首筆僅小額","source_freq":"每日股價、季度財報","date":null,"evidence_refs":[]},{"n":7,"text":"SpaceX 合併條款公布","type":"風險","maps_to":"R4","metric":"換股比例、稀釋幅度、Terafab 成本分攤","threshold":"條款公布，或換股稀釋逾 10%","action":"公布→重跑估值與稀釋試算；稀釋逾 10% 且無對價說明→持有者減碼","source_freq":"8-K 與公司公告，事件型","date":null,"evidence_refs":["major_events#0","ma_merger#0"]},{"n":8,"text":"Q4 2026 財報後複審","type":"複審日期","maps_to":"全部假設","metric":"交付、汽車與能源毛利率、2027 資本支出指引","threshold":"財報公布","action":"逐項對照 H1～H3 與 kill 指標","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"汽車毛利率（不含法規積分）","bear_threshold":"連兩季<16%","window":"2027 年內","source":"季度更新簡報與法說會","last_status":"ok"},{"metric":"能源毛利率（扣除關稅退款與保固回沖）","bear_threshold":"任一季<20%","window":"2026Q4～2027Q4","source":"季度更新簡報與法說會","last_status":"unknown"},{"metric":"季度自由現金流（公司口徑）","bear_threshold":"連兩季為負且動用新信貸額度","window":"2027～2028","source":"季度更新簡報、8-K","last_status":"ok"},{"metric":"無人監督營運城市數","bear_threshold":"2027 年底<10 城或遭監管暫停","window":"至 2027-12","source":"法說會與公司公告","last_status":"warning"}],"action_conditions":{"rearm_trigger":"股價≤250 美元（約 FY2027E 共識 115 倍）且汽車毛利率不含積分連兩季≥17%；或 Robotaxi 營收單獨揭露且年化≥50 億美元","exec_line":"現價不建倉；任一重啟條件成立後先重跑完整研究，首筆僅小額試單，不追價","holding_cap":"0%（重啟前）"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把管理層的無人車與 Optimus 時程當成基本情境：FY2027E 共識 2.16 美元仍約 172 倍，以 55 倍終端倍數倒推須 2031 年 EPS 約 6.8 美元，而管理層自承無人車營收要到 2027 下半年才明顯、目前未揭露車隊數","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤250 美元且汽車毛利率連兩季≥17%，或 Robotaxi 營收單獨揭露且年化≥50 億美元"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把管理層的無人車與 Optimus 時程當成基本情境：FY2027E 共識 2.16 美元仍約 172 倍，以 55 倍終端倍數倒推須 2031 年 EPS 約 6.8 美元，而管理層自承無人車營收要到 2027 下半年才明顯、目前未揭露車隊數"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=-1.08, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"FSD 訂閱與無人車服務成為經常性利潤來源：付費客戶持續擴大，Robotaxi 2027 年起貢獻可見營收","2y":"2027 年底 FSD 付費客戶≥250 萬、無人監督營運≥10 城","5y":"FSD 與 Robotaxi 占公司毛利三成以上","10y":null,"threshold":"2027 年底 FSD 付費客戶≥250 萬（現約 170 萬）且無人監督營運城市≥10 個","source":"季度更新簡報與法說會（CFO 承諾隨規模揭露 FSD 營收與流失率）","drift_rule":"付費客戶季增連兩季<5% 為削弱、連三季持平或下滑為反轉；2027 年中無人營運仍≤6 城為削弱"},{"id":"H2","text":"汽車本業毛利守住：不含法規積分的汽車毛利率站穩 17% 以上，交付恢復成長","2y":"FY2027 交付≥185 萬輛、汽車毛利率不含積分全年≥17%","5y":null,"10y":null,"threshold":"汽車毛利率（不含法規積分）每季≥17%；FY2027 交付≥185 萬輛（市場共識約 192 萬）","source":"季度交付公告與更新簡報","drift_rule":"連兩季低於門檻≥5%（<16.2%）為削弱，連三季低於≥10%（<15.3%）為反轉"},{"id":"H3","text":"儲能成為第二條利潤線：Megapack 資料中心需求與自產 LFP 電芯撐住部署成長與毛利","2y":"2027 年部署≥60 GWh","5y":"能源毛利占全公司毛利≥25%","10y":null,"threshold":"2027 年部署≥60 GWh，且扣除關稅退款與保固回沖後毛利率≥22%","source":"季度更新簡報與法說會","drift_rule":"部署年增連兩季轉負為削弱；扣除一次性後毛利率連兩季<20% 為反轉"}],"R":[{"id":"R1","text":"本季利潤靠一次性項目撐：能源毛利 33.1% 含關稅退款與供應商保固分攤，汽車毛利改善來自亞太組合；Q4 回落即暴露真實獲利","h_ref":"H3","clock":"⚡","threshold":"Q4 2026 能源毛利率<22% 或汽車毛利率（不含積分）<17%","evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"id":"R2","text":"無人車監管與訴訟：NHTSA 學區超速請願評估、Cybercab 無踏板自我認證查詢、FSD 調查、多起召回、Autopilot／FSD 證券集體訴訟（德州駁回聲請待裁、另有加州案）","h_ref":"H1","clock":"🔥","threshold":"NHTSA 正式立案或要求暫停無人營運；或集體訴訟駁回聲請遭拒","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#2","major_events#3","major_events#5","lawsuit_class_action#0","product_recall_warning#0"]},{"id":"R3","text":"競爭：中國品牌西歐份額創 10.7% 新高、BYD 全球 BEV 份額 12% 逼近；Waymo 無人車規模領先，新進者陸續上路；其他車廠可能借外部方案追上 L2+ 並壓低 FSD 價格","h_ref":"H2","clock":"🔥","threshold":"全球 BEV 份額連兩季<11%，或北美 FSD 交車附加率回落至 55% 以下","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","competitive_share_entrants#5","substitute_technology#0"]},{"id":"R4","text":"資本支出週期與關係人交易：Terafab 至 2028 年初投入數百億美元、長期逾千億，與 SpaceX 分攤未定；合併探索條款未定，可能以換股稀釋股東","h_ref":"H1","clock":"🐢","threshold":"年度自由現金流轉負並動用新信貸額度，或合併換股稀釋逾 10%","evidence_refs":["capital_markets_pricing#0","major_events#0","ma_merger#0"]},{"id":"R5","text":"關稅與供應鏈地緣：關稅推高電芯與零組件成本、對儲能衝擊大於汽車；中國稀土磁鐵出口許可曾延誤 Optimus","h_ref":"H3","clock":"🐢","threshold":"汽車或能源毛利率因關稅單季下滑≥2 個百分點","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"]}],"single_thing":{"description":"無人監督 Robotaxi 或 Cybercab 車隊發生致死或重傷事故，監管機關因此暫停或限制無人營運","why_fatal":"現價約 FY2026E 共識 210 倍，倍數幾乎全靠無人車與 FSD 的未來利潤；暫停營運會同時打到 H1 時程、FSD 訂閱需求與 Optimus 的 AI 敘事，Bull 情境幾乎歸零","if_happens":"持有者清倉；重啟條件作廢，待監管恢復且一年內無重大事故再重跑研究","how_monitor":"NHTSA 調查與召回公告、公司無人營運安全報告、營運城市數與營運時段是否收縮","probability":"15%～25%（12～24 個月）：無人里程每週雙位數成長、正擴到 24 小時與高速路段，曝險快速放大；Musk 自承任何傷人事件都會招致監管收緊"}},"appendix_a":{"growth_durability":5,"quality_score":4,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":172.3,"peg_fy2":4.94,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":1.08,"FY2026E":1.77,"FY2027E":2.16,"FY2028E":3.22},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS 1.08 美元（事實表只有此口徑）；FY2026E～FY2028E 為 Koyfin 共識，是否為調整後口徑事實表未涵蓋，兩者可能不同口徑，三年成長率以 FY2026E→FY2028E 兩年年化約 35% 為準"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Cybercab 在 Dallas 上線","impact":"中","watch":"上線後車隊規模與營運時段"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年資本支出指引","impact":"高","watch":"能源毛利率扣除一次性後是否≥22%、2027 年資本支出規模"},{"date":"2027-01-21","date_precision":null,"type":"regulatory","event":"NHTSA 決定是否就學區超速請願正式立案","impact":"高","watch":"立案範圍是否涵蓋暫停無人營運"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"FSD 歐盟全境核准（管理層稱不晚於 Q1）","impact":"中","watch":"核准與否及歐洲訂閱附加率"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"客戶車輛加入 Robotaxi 車隊（管理層稱約 Q2）","impact":"高","watch":"是否如期開放及首批城市"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「轉機/特殊情境」，轉機/特殊情境 的專屬核心軸未採證（不計燈號）：turnaround_catalyst_timeline、turnaround_liquidation_floor。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
