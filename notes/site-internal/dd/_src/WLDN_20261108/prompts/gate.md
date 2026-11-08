你是 DD 管線 v20 的判斷層閘（gate），標的 WLDN（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（40 條）
- `f_kpi0_contract_revenue_gaap`（q1_business）｜Contract revenue（GAAP 營收）＝214.5 USD m｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：查無單季共識，省略
- `f_kpi1_net_revenue_non_gaap`（q1_business）｜Net revenue（non-GAAP，扣分包）＝112.2 USD m｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：查無
- `f_kpi2_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代之）＝28.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：查無
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝16.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿損益表；利益率為本表計算：占 contract revenue 7.6%、占 net revenue 14.5%（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：查無
- `f_kpi7_fy2026`（q1_business）｜FY2026 指引（上修）＝net revenue 435–445；Adj. EBITDA 109–111；Adj. EPS 5.15–5.25 USD m／USD per share｜期間與口徑：Q3 FY2026 公告（2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1；假設 15.9m 稀釋股、稅率 0%、不含未來併購（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026 公告（2026-11-05））
  - 註記：consensus_revision 快照 FY1 EPS 5.07（財報前快照）；指引中點 5.20
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-05 date｜期間與口徑：2026-11-05／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-05）
- `f_peer_wldn_gross_margin_pct`（q2_moat）｜WLDN 毛利率＝37.79 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WLDN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wldn_operating_margin_pct`（q2_moat）｜WLDN 營業利益率＝7.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WLDN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wldn_fcf_margin_pct`（q2_moat）｜WLDN FCF 利潤率＝8.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WLDN.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ttek_gross_margin_pct`（q2_moat）｜TTEK 毛利率＝18.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTEK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ttek_operating_margin_pct`（q2_moat）｜TTEK 營業利益率＝11.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTEK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ttek_fcf_margin_pct`（q2_moat）｜TTEK FCF 利潤率＝10.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTEK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_acm_gross_margin_pct`（q2_moat）｜ACM 毛利率＝5.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ACM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_acm_operating_margin_pct`（q2_moat）｜ACM 營業利益率＝4.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ACM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_acm_fcf_margin_pct`（q2_moat）｜ACM FCF 利潤率＝1.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ACM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_j_gross_margin_pct`（q2_moat）｜J 毛利率＝22.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.J.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_j_operating_margin_pct`（q2_moat）｜J 營業利益率＝4.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.J.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_j_fcf_margin_pct`（q2_moat）｜J FCF 利潤率＝4.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.J.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.07 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.42 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝826.8 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（1 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝960.0 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（1 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_gaap_eps`（q4_capital）｜GAAP 淨利／稀釋 EPS＝11.9 USD m（EPS 0.76）｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：查無
- `f_kpi5_ytd_9_32_9_5_2`（q4_capital）｜自由現金流（YTD 9 個月：營業現金流 32.9 − 資本支出 5.2）＝27.8 USD m｜期間與口徑：YTD 至 Q3 FY2026（2026-10-02，公告於 2026-11-05）；新聞稿未揭露單季現金流／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿現金流量表，FCF 為本表計算（numbers.latest_quarter_kpis.items[5]，as_of YTD 至 Q3 FY2026（2026-10-02，公告於 2026-11-05）；新聞稿未揭露單季現金流）
  - 註記：查無
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝30.5 %｜期間與口徑：Q3 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SBC 4.972 ÷ GAAP 營業利益 16.304，本表計算；占 contract revenue 2.3%（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝43.14 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 82.3、現金 39.16（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝66.22 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝13.06 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 5.07，分子＝快照價 66.22｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝16.07 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝43.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝40.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝1058.29 USD m｜期間與口徑：2026-11-08／市值 1015.15 ＋ 淨負債 43.14｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝15.33 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 5.07 → 5.07（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.28 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-25.08 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝32.2｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 66.22 / W52 90.04 / W104 75.79 / W250 45.8 / W250 13週斜率 1.37%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝45.8 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（5 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K風險因子：大量營收來自競標，輸標可能多年失去該市場機會，得標也可能因壓價而侵蝕利潤。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025：兩大客戶 Clark County School District 與 Southern California Edison 合計占合併合約營收 23.2%；前10大客戶占 50.7%（FY2024 51.3%、FY2023 52.7%）；FY2024、FY2023 無單一客戶超過10%。
  - 來源：SEC EDGAR 10-K FY2025（申報 2026-02-27）Item 8 客戶集中度（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：S&P 於2025-09 將 Edison International 與 SCE 下調一級至 BBB-（野火基金縮減）；SCE 為 WLDN 前兩大客戶之一。
  - 來源：SCE Form 424B5 / 搜尋結果（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因子提及供應鏈限制與勞力短缺推高材料與勞力成本、使交付與專案時程延長；並依賴分包商
  - 來源：Willdan Group Form 10-K (FY ended 2026-01-02)（as_of 2026-03-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St community narrative argues automation/technology-driven alternatives needing fewer staff could undermine Willdan's consulting model (opinion, not company forecast)
  - 來源：Simply Wall St community narrative: Automation Disruption And Public Sector Cuts Will Undermine Performance（as_of 2025-07-13）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":200.3,"bear_5y_price":48.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":82.9,"ev5y_pct":73.7,"irr_base_pct":12.8,"asym_ratio":4.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.07,"pe":13.06,"basis":"FY2026E 共識調整後 EPS（快照未反映 11-05 指引中點 5.20 美元）；終端倍數同用當年度調整後 EPS 口徑"},"eps":{"bull":[5.87,7.23,8.83,10.28,11.78],"base":[5.4,6.25,7.15,7.96,8.65],"bear":[4.4,4.2,4.35,4.55,4.8]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WLDN_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：CFO 上調 2026 全年財測：淨收入、調整後 EBITDA、調整後 EPS 區間（原話："range of $415 million to $430 million"）
- 2026-08-06｜CFO｜guidance：財測假設：全年有效稅率 0%、年底稀釋股數約 15.9 百萬股（原話："a 0% effective tax rate for the year"）
- 2026-08-06｜CFO｜guidance：CFO 稱下半年稅率約 15%–20%，因 179D 效益於 6 月底到期（原話："it's going to be a tax rate somewhere between 15% and 20%"）
- 2026-08-06｜CFO｜guidance：CFO 說 Q3、Q4 大致類似 Q2，Q2 有部分業務自下半年提前認列（原話："Q3 and Q4 are probably going to look something similar"）
- 2026-08-06｜CEO｜guidance：CEO 解釋財測偏保守：LADWP 放量速度為最大變數，可能延至 2027 初（原話："we don't know how quickly LADWP will ramp up"）
- 2026-08-06｜CFO｜margin：Q2 毛利率下滑 150 bp，管理層歸因於收入組合轉向績效工程與商業專案（原話："The gross margin declined 150 basis points"）
- 2026-08-06｜CFO｜margin：管理層說明商業專案毛利較低但間接費用率較低，調整後 EBITDA 利潤率較高（原話："they also carry a lower overhead rate, and resulting higher"）
- 2026-08-06｜CFO｜margin：Q2 調整後 EBITDA 利潤率 28.2%，稱為公司史上單季最高（原話："the highest quarterly margin in the company's history"）
- 2026-08-06｜CFO｜margin：Q2 利潤率不預期全年維持；全年預估約 25%（2025 年 21.8%）（原話："we do not expect that margin to hold throughout the year"）
- 2026-08-06｜CFO｜margin：G&A 占合約收入比由 32.6% 降至 29.3%；股權激勵費用年增 51%（原話："declined to 29.3% of contract revenue"）
- 2026-08-06｜CFO｜margin：Q2 淨收入年增 23%，扣除 Burton 併購的有機成長為 18%（原話："the organic growth rate"）
- 2026-08-06｜CFO｜margin：Q2 帳面含 $5.3 百萬稅務利益，GAAP 淨利 $24.3 百萬（原話："We recognized a $5.3 million tax benefit for the quarter."）
- 2026-08-06｜CFO｜commitment：CFO 重申長期調整後 EBITDA 利潤率目標在高 20% 區間（上季提出）（原話："a clear path to achieving margins in the high 20% range"）
- 2026-08-06｜CFO｜commitment：CFO 稱可將調整後 EBITDA 超過 70% 轉為自由現金流（年度）（原話："convert more than 70% of adjusted EBITDA into free cash flow"）
- 2026-08-06｜CFO｜commitment：CFO 預期（若無新併購）循環信貸於年底前還清（原話："we would expect the revolver to be fully repaid by year-end"）
- 2026-08-06｜CFO｜capital_allocation：季末淨負債 $33 百萬、淨負債/EBITDA 0.3x，總流動性 $165 百萬；Burton 動用 $30 百萬循環信貸，已還 $10 百萬（原話："$165 million in total available liquidity at quarter end"）
- 2026-08-06｜CFO｜capital_allocation：管理層持續尋找併購以擴大服務並加速成長（原話："accelerate growth through acquisition"）
- 2026-08-06｜CFO｜capital_allocation：179D 條款 6 月底到期，但遞延稅資產 $34 百萬仍帶來現金流效益（原話："$34 million in deferred tax assets on our balance sheet"）
- 2026-08-06｜CEO｜customer：CEO 稱商業客戶約占營收四分之一，為第三條支柱（原話："It is currently about a quarter of"）
- 2026-08-06｜CEO｜customer：CEO 稱商業營收中最大部分為資料中心電力，成長最快（原話："is the fastest growing part of Willdan"）
- 2026-08-06｜CEO｜customer：APG 收購貢獻預計今年約 $75 百萬，近乎三倍（原話："is projected to nearly triple this year over"）
- 2026-08-06｜CEO｜customer：LADWP 新增 $110 百萬太陽能路燈合約擴充；CEO 稱 2027 可能成為最大客戶（原話："could be our largest customer in 2027"）
- 2026-08-06｜CEO｜customer：LADWP 擴充案已有一半取得開工授權（原話："authorization to proceed on half of that $110"）
- 2026-08-06｜CEO｜customer：Burton 5/4 完成後自 5 月起新增 Walgreens、Carter's、Five Below 等客戶（原話："relationships with Walgreens, Carter's, and Five Below"）
- 2026-08-06｜CEO｜customer：其他新合約：SoCal REN 5 年 $49 百萬、紐約市立學院 $53 百萬中央電廠升級（原話："a new 5-year, $49 million energy efficiency contract"）
- 2026-08-06｜CEO｜product：Burton 帶來建築 HVAC 與能源控制技術及商業能源採購新業務線（原話："a new line of business in commercial energy procurement"）
- 2026-08-06｜CEO｜product：管理層稱電池儲能機會管線成長，常與規劃、工程、微電網合併（原話："a growing pipeline of battery storage opportunities"）
- 2026-08-06｜CFO｜product：CFO 稱 AI 採用有助效率，是獲利成長快於營收的原因之一（原話："AI adoption"）
- 2026-08-06｜CEO｜competition：CEO 稱加州 REN 正承接傳統投資者擁有公用事業在能效領域的更大角色，後續有更大機會（原話："The California RENs are assuming a larger role"）
- 2026-08-06｜CEO｜risk：CEO 承認 LADWP 放量時程不確定，Q3 貢獻難估（原話："It's too early to tell exactly what the Q3 contribution"）
- 2026-08-06｜CEO｜risk：CEO 稱人才市場偏緊、資深人員薪資上升，但未見人力短缺（原話："but labor is tight."）
- 2026-08-06｜CEO｜risk：CEO 稱資料中心專案遍及全美，並新設佛州、喬治亞、北卡、肯塔基、德州據點（原話："projects in New Mexico and Montana, and some in Utah"）

### 問答異常語氣（迴避／改口／保留）
- WLDN_Q2_2026_Earnings_Call_20260806.md｜問：Wedbush 分析師：本季大幅超預期但財測上調幅度不大，是否缺乏能見度？｜答法：CEO 承認刻意偏保守，歸因於 LADWP 放量速度不確定，未給出下半年具體區間拆解；CFO 僅說 Q3/Q4 類似但略低於 Q2
- WLDN_Q2_2026_Earnings_Call_20260806.md｜問：Roth 分析師：LADWP 專案 Q2 放量情形及下半年走勢｜答法：CEO 自述「we were appropriately conservative, but in fact, we were not」語句前後矛盾，且未給 Q3 數字，稱太早無法判斷

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 1 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 1 | 2 |
| geo_supply_chain | found | 1 | 1 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 1 | 3 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Willdan Group largest customer concentration in-house insourcing 2026；Willdan Group 10-K customer concentration risk largest client percent of contract revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260703","verdict":"進場","role":"衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"APG 段 2026-2028 至少 3 倍成長，from ~$37M FY24 → $100-130M FY27","columns":{"2Y 驗證點":"Q2-Q4 FY2026 APG cumulative ≥ $75M；FY27 APG ≥ $110M","5Y 驗證點":"FY30 APG ≥ $200M + 數據中心客戶 ≥ 5 家（去集中）","10Y 驗證點":"FY35 APG ≥ $500M（成 WLDN 最大段）","具體數字門檻":"FY26 APG +100% YoY / FY30 $200M / FY35 $500M","信息來源":"CEO Bieber Q1 FY26 法說「APG more than double 2026」+ backlog 延伸 2027-2028","漂移觸發":"連 2 季 APG YoY &lt; +60% → 削弱；連 4 季 → 反轉"}},{"id":"H2","text":"Adj EBITDA margin 2026-2028 維持 24-26%（FY25 21.8% → FY27 25-26%）","columns":{"2Y 驗證點":"FY26 全年 ≥ 24%（guide $102.5M / $417.5M = 24.6%）；Q2-Q3 連 2 季 ≥ 24%","5Y 驗證點":"FY28 sustainable 25%+ 且 FCF/NI ≥ 1.0","10Y 驗證點":"FY30 達 industry leader 27%+","具體數字門檻":"Q2 FY26 ≥ 24% / FY28 25% / FY30 27%","信息來源":"公司 FY26 guide adj EBITDA $100-105M / net rev $410-425M；FY25 actual $79.5M/$364.8M = 21.8%","漂移觸發":"連 2 季 &lt; 22% → 削弱；連 4 季 → 反轉"}},{"id":"H3","text":"現金轉換 OCF/NI 全年維持 ≥ 1.2、FCF ≥ $70M（證偽 screener「賺不到錢」）","columns":{"2Y 驗證點":"FY26 全年 OCF/NI ≥ 1.2、FCF ≥ $65M（吸收 Q1 營運資金季節後回補）","5Y 驗證點":"FY28 FCF ≥ $110M、FCF/NI ≥ 1.0（roll-up 攤銷後仍現金為王）","10Y 驗證點":"FY32 FCF ≥ $180M、cumulative FCF &gt; 併購支出","具體數字門檻":"FY26 OCF/NI ≥ 1.2 / FY28 FCF $110M","信息來源":"FY25 OCF $80.1M / NI $52.6M = 1.52；FCF $71M（gurufocus / 公司）","漂移觸發":"連 2 季 TTM OCF/NI &lt; 1.0 → 削弱；FY 全年 &lt; 1.0 → 反轉（陷阱重評）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"APG doubling 跳票——1-2 個大型數據中心客戶專案遞延","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度 APG revenue YoY、法說中 APG 描述 tone","警戒閾值":"Q2 FY26 APG YoY &lt; +80% → 削弱；連 2 季 &lt; +50% → 反轉"}},{"id":"R2","text":"IRA 能效條款 / federal 能效資金被削（QC-39 C 軸法規）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"federal budget、DOE/EPA 預算、utility program funding","警戒閾值":"utility 能效 funding 連 2 季 YoY &lt; +5% → 削弱"}},{"id":"R3","text":"roll-up 整合失敗 / 現金轉換惡化（one-too-many acquisition）","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Burton retention / margin 貢獻；APG × Energy Solutions cross-sell；全年 FCF/OCF","警戒閾值":"FY27 全年 OCF/NI &lt; 1.0 或 Burton net rev &lt; $30M → 削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.5,"ev5y_pct":80.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星持倉","signal":"A","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":6.0,"ev5y_pct":80.0,"irr_base_pct":13.5,"max_dd_pct":-45.0,"bull_5y_price":198.0,"bear_5y_price":52.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":76.3,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"WLDN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Willdan Group, Inc."},"oneliner":"能源顧問需求與併購把 EBITDA 推向 1.4 億美元，但稅率回正與舉債併購讓每股盈餘幾乎不動；現價約 12 倍 FY27 調整後盈餘，勝負在 2 月公布的現金流與有機成長。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺公用事業、州與地方政府、商業客戶的能效與電網規劃服務費，錢卡在電網受限地區的規劃與方案設計這一節；併購已把三類客戶拉成各約三分之一。","reasoning":"Q3 合約營收 2.145 億美元，扣掉分包與材料轉手後的淨營收 1.122 億才是自己賺的；毛利率 38.4%，GAAP 營業利益占合約營收 7.6%，Adj EBITDA 占淨營收 25.2%。分部上 Energy 約 85%、Engineering 約 15%，FY27 Energy 會超過 90%。超過 80% 的工作來自重複客戶，NYPA 10 年多家得標合約（總額約 33 億美元）續標成功，Con Ed 合作進入第 17 年。單點依賴在付款來源：公用事業的能效預算最終由電費支付，FY25 兩大客戶占合約營收 23.2%；管理層稱納入 Mantis 後沒有客戶超過 10%。供需判斷為結構性持久：負載成長與老舊電網不是單一年度現象，但資料中心這一段的政治風險正在升高。","fact_refs":["f_kpi0_contract_revenue_gaap","f_kpi1_net_revenue_non_gaap","f_kpi2_adjusted_ebitda_non_gaap","f_kpi3_gaap","f_kpi7_fy2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"重複客戶超過 80%，但多數合約靠競標與多家得標，得標不保證工作量；合約營收約一半是轉手，判斷規模要看淨營收。","unit_econ_note":"Q3 Adj EBITDA 占淨營收 25.2%；Mantis 約 7,500 萬美元淨營收、35% 利潤率，會拉高組合利潤率。Q3 毛利率上升部分來自激勵收入與 LADWP，持續性未證。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"輕資產能源服務，靠重複客戶與併購擴張，EBITDA 成長快，但每股盈餘受稅率、利息與稀釋拖累"},"industry":{"clock_phase":"II","sd_verdict_source":"雙向拉鋸：競爭未見惡化（10-K 稱市場分散，Q3 NYPA 續標成功）；結構性轉好（負載成長，美國投資者所有公用事業 2026 年資本支出估 2,278 億美元，2024 年約 1,730 億，來源為招募業者部落格，品質偏低）；其他結構變數是電費負擔與資料中心許可的政治反彈。擴張期的依據是公用事業資本支出與新約，不是股價。","bargaining":{"up":"上游主要是工程人才與分包商；CEO 在 2026-08-06 稱人才市場偏緊、資深人員薪資上升。","down":"下游是受監管公用事業與政府，靠競標與預算決定；FY25 前十大客戶占 50.7%，兩大客戶占 23.2%。","geo":"過去集中在加州與紐約，納入併購後工作涵蓋 50 州，地域集中度下降。"},"profit_pool_dir":"利潤往電網規劃、能源採購與商業工業客戶移動，事實表未涵蓋量化的利潤池資料。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與分段利潤池，只有同業群營收份額約 0.2% 這個代理值，展開等於自行編造數字。"}}}},"q2_moat":{"verdict":"護城河穩定、等級 B：優勢來自長年公用事業專案經驗與重複客戶，執行力在擴大，定價權沒有擴大的證據。","reasoning":"可證的方向是最大客戶關係：NYPA 續標成功，年工作量 5,000 萬到 6,000 萬美元；Con Ed 與 National Grid 合併成每年 2,500 萬美元的方案。反面是客群擴張主要靠併購，事實表沒有同業 ROIC，只有利潤率：WLDN 營益率 7.05%，低於 TTEK 的 11.73%，高於 ACM 與 J；毛利率 37.79% 與同業口徑不同，不能當優勢。Q2 毛利率下滑與 Q3 上升都歸因組合，定價權無法由此證明。Mantis 單筆稅後報酬約 7.1%，再投資品質低於整體增量報酬。投入資本事實表未涵蓋，當期 ROIC 只能判方向。","fact_refs":["f_peer_wldn_gross_margin_pct","f_peer_wldn_operating_margin_pct","f_peer_wldn_fcf_margin_pct","f_peer_ttek_gross_margin_pct","f_peer_ttek_operating_margin_pct","f_peer_ttek_fcf_margin_pct","f_peer_acm_gross_margin_pct","f_peer_acm_operating_margin_pct","f_peer_acm_fcf_margin_pct","f_peer_j_gross_margin_pct","f_peer_j_operating_margin_pct","f_peer_j_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"監管型能效專案與電網規劃的長年經驗，加上跨公用事業、政府、商業三類客戶的重複委託，換手要付出專案知識與重新採購的成本。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大（NYPA 續標、Con Ed 擴約、Adj EBITDA 利潤率上升）；定價權穩定（競標為主，毛利率變動主要來自組合）。兩者合併為穩定，同業 ROIC 差距事實表未涵蓋。","competitor_notes":[{"name":"TTEK","strategy_note":"營益率 11.73%、FCF 利潤率 10.81%，都高於 WLDN 的 7.05% 與 8.4%，是目前利潤結構的上限對照；事實表沒有業務重疊度。"},{"name":"ACM","strategy_note":"營益率 4.65%、FCF 利潤率 1.32%，低於 WLDN；毛利率 5.68% 的成本口徑與 WLDN 不同，不能直接比。"},{"name":"J","strategy_note":"營益率 4.57%、FCF 利潤率 4.53%，低於 WLDN；屬於 10-K 提示可能跨入的大型工程公司類型。"}],"spread_notes":null,"peer_na_reason":"事實表只有同業三項利潤率，未涵蓋同業 ROIC 與份額變化，無法計算報酬差距。","threats":[{"level":"🟡","text":"競標為主，輸標可能失去該市場多年，得標也可能壓價；NYPA 續標成功顯示目前守得住，但多家得標合約不保證工作量。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"自動化工具可能壓縮工程與顧問工時；目前只有社群文章的觀點，沒有數據，公司則把 AI 列為效率來源，先監測不扣分。","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"大型全國工程公司可能切入能源專案與電網規劃；10-K 已提示，本包未見實際案例。","p":"20%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（方向判斷；事實表未涵蓋投入資本，Mantis 入帳後周轉率會下降）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是電力用戶與建物業主，決策者是公用事業與政府，付款來自費率與預算；電網受限是必須解決的問題，超過 80% 工作來自重複客戶。資料中心那一段的急迫性高，持久性較難判斷。"},{"item":"決策層級","level":"🟡","text":"單一專案的替代性由競標決定，10-K 明示輸標會失去多年機會；NYPA 續標與 Con Ed 第 17 年說明現有客戶黏著，但事實表沒有續約率與漲價後流失率。"},{"item":"價值鏈分配","level":"🟡","text":"合約營收約一半轉手給分包與材料，公司留下淨營收；營益率 7.05% 低於 TTEK 的 11.73%，買方是受監管大型機構，議價力不弱。"},{"item":"社會容忍度","level":"🟡","text":"CEO 稱電費負擔已成客戶最重要的考量，部分地區電價年增超過 30%；這有利能效方案的論述，也會壓縮由費率支付的預算，資料中心許可的政治反彈已經出現。"}],"roiic":13.7,"reinvest_rate":50,"endo_ceiling":5.5,"formula_note":"FY25 到 FY27 指引 Adj EBITDA 增 6,050 萬美元，以 23% 稅率計稅後約 4,660 萬，除以 FY26 併購投入 3.41 億美元得 13.7%，其中含幾乎不用資本的有機成長；單看 Mantis 約 7.1%。再投資率 50% 是本次判斷，假設現金先還債再做小型併購。13.7%×50% 得 6.9%，資本配置未過關打八折後為 5.5%。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬，但 FY27 帳面成長大半是併購，有機成長的下限要到 2027 年 2 月才看得清楚。","reasoning":"FY27 合約營收約 19% 的成長中，Mantis 增量約 12 個百分點，指引下限隱含的有機成長僅約 6%，低於管理層口頭的低雙位數。共識只有兩年：FY25 實績 4.91 美元（由逐字稿推算）到 FY27E 5.42 美元，年化 5.1%，且快照早於本次財報，第三年共識事實表未涵蓋。內生上界 5.5%；Base 路徑 FY26 到 FY31 年化 11.3%，超出 5.8 個百分點，主要來自債務還清省下利息（約 2.5 個百分點）、利潤率擴張與輕資本的有機成長，不靠回購與倍數。份額代理值僅約 0.2%，低於 35% 的寬跑道標準，但 TAM 未涵蓋。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_kpi7_fy2026","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"FY26 Q3 淨營收成長 18%，有機 12%、併購 6%；FY27 合約營收成長約 19%，併購約 12 個百分點以上，指引下限隱含有機約 6%。成長來自量與併購，回購沒有貢獻。","runway_years":"超過 10 年（份額代理值約 0.2%，TAM 事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界 5.5%（推導見護城河報酬持續期）。共識兩年年化 5.1% 未超過，Base 路徑 11.3% 超過，缺口可歸因於利息下降與利潤率擴張；情境已按超出處理，空頭機率 30%。","segments":[{"item":"Energy","value":"約占營收 85%，FY27 將超過 90%；Q3 有機淨營收成長 17%"},{"item":"Engineering","value":"約占營收 15%，FY27 降到 10% 左右"},{"item":"客群","value":"含併購全年化後，公用事業、州與地方政府、商業各約三分之一"},{"item":"資料中心（APG）","value":"FY26 約 7,500 萬美元，約占隱含合約營收 8.4 億的 9%；Q3 未更新數字"}],"decay_signals":["EPS 成長顯著高於營收成長：FY23 到 FY25 GAAP EPS 由 0.80 升到 3.49 美元，營收年增 11% 到 20%，已亮燈，且部分來自低稅率","毛利率連兩季年減：未亮燈，Q2 減 150 個基點、Q3 增 150 個基點","FCF／淨利低於 0.75 連兩年：未亮燈，FY25 為 1.34；FY26 前九個月 0.62 需看 Q4","SBC 占營收超過 5% 且上升：未亮燈，Q3 占合約營收 2.3%，但年增 58%","產業估值倍數系統性下移：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置目前不及格：舉債併購的報酬尚未證明，股數每年增約 5%；還債是接下來一年的正確優先序。","reasoning":"FY25 FCF／淨利 1.34，FY26 前九個月 FCF 2,780 萬美元、對淨利 4,470 萬只有 0.62，對 Adj EBITDA 只有 35%，靠 Q4 回補。FY26 併購投入約 3.41 億美元，淨槓桿由 Q3 的 0.2 倍升到 2.3 倍。公司目標 Q3 FY27 淨槓桿低於 2.0 倍，以 1.4 億 EBITDA 計只需少約 1,300 萬美元淨負債，門檻很鬆，本次用 1.8 倍檢驗。SBC 單季 497 萬美元，占 GAAP 營業利益 30.5%。債務到期結構、新貸款利率與近三年現金去向事實表未涵蓋；以 Q3 利息推估利率約 6% 到 7%，FY27 利息約 2,000 萬美元。","fact_refs":["f_kpi4_gaap_eps","f_kpi5_ytd_9_32_9_5_2","f_kpi6_sbc","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Mantis 以 2.85 億美元換約 2,625 萬 Adj EBITDA（7,500 萬×35%），約 10.9 倍；稅後約 2,020 萬，報酬約 7.1%，低於 9% 到 10% 的資金成本假設，且尚未實現。Burton 與 Compass 未揭露單獨獲利。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"法說未提回購，現金優先還債；事實表未涵蓋回購紀錄。"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"稀釋股數由 FY23 約 1,366 萬（淨利÷稀釋 EPS）增到 FY26 指引 1,590 萬，年增約 5.2%，高於每年 1.5% 上限；部分來自股價上升造成的計算效果。"}]},"governance":{"capital_returns":[{"item":"FY26 併購現金支出","value":"約 3.41 億美元（前九個月 5,600 萬＋Mantis 2.85 億）"},{"item":"債務","value":"Mantis 完成後總債務 3.32 億美元、淨負債 2.93 億美元，淨槓桿約 2.3 倍，可動用流動性 1.54 億美元"},{"item":"回購與股利","value":"事實表未涵蓋，法說未提"},{"item":"優先序","value":"多數自由現金流還債，同時尋找小型併購"}],"sbc":{"note":"Q3 SBC 497 萬美元，年增 58%，占 GAAP 營業利益 30.5%、占淨營收 4.4%。"}}}},"q5_valuation":{"verdict":"現價要求 FY27 調整後 EPS 約 5.4 美元、之後獲利年增約 10%，不需要倍數上修；我相信 EBITDA 兌現，對每股現金只信一半，所以估值算合理，不算便宜。","reasoning":"表面 Forward P/E 13.06 倍，但 FY26 指引假設 0% 稅率，用 22% 還原後約 16.3 倍。事實表的 EV 10.58 億美元仍用舊淨負債，納入 Mantis 後 EV 約 13.1 億到 13.5 億，對 FY27 Adj EBITDA 下限約 9.3 到 9.6 倍。FY27 Base EPS 5.40 美元對應 12.3 倍；若扣回 SBC 與攤銷，GAAP EPS 估約 3.1 到 3.4 美元，約 20 到 22 倍。管理層 FCF 約 9,800 萬美元的目標等於市值 9.3%，扣 SBC 後約 7.4%。12 個月目標 75.6 美元（5.40×14），三年約 100 美元。賣方 7 月底共識目標 112.67 美元早於本次財報，隱含倍數未計稅率回正；共識 EPS 三個月零修正也是快照未更新，不代表市場沒有反應。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_ev_m","f_net_debt_m","f_shares_diluted_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct","f_ev_s_fwd","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"valuation":{"basis":"FY27E 調整後 EPS，以約 22% 稅率計，輔以納入 Mantis 淨負債後的 EV／EBITDA 與 FCF 殖利率","tier":"小型能源服務與工程顧問","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業現值本益比或 EV／EBITDA；同業倍數承重但無資料，標為缺口，改用公司自身現值與情境推導。"},"fwd_pe":13.06,"peg":1.56,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 調整後本益比 12.3 倍與 FCF 殖利率 7.4% 到 9.3% 偏低，但分母受稅率影響，GAAP 本益比約 20 到 22 倍，且槓桿剛升到 2.3 倍，結論為合理。PEG 以 FY25 實績 4.91 到 FY28 Base 6.25 美元年化 8.4% 計算，第三年並非共識。五年分位留空，因事實表只有 3 到 4 個年度端點（本益比 0、P/S 43、EV/S 40.2），不是五年序列。","upside_short_pct":14.2,"upside_mid_pct":51.2,"denominator_disputed":true,"denominator_note":"FY26 調整後 EPS 5.20 美元建立在全年 0% 稅率上；179D 已於 2026 年 6 月底到期，Q3 稅率 23%。以 22% 粗估還原約 4.06 美元，對應 16.3 倍而非 13 倍，FY27 的稅率公司尚未揭露。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把 EBITDA 成長當成每股價值成長；真正致命的是 FY27 Adj EBITDA 跌破 1.4 億美元。","reasoning":"敏感度：FY27 Adj EBITDA 少 10%（1,400 萬美元）約少 0.67 美元 Adj EPS，是最大單一項；稅率高 3 個百分點少 0.21 美元；利率高 1 個百分點少約 0.14 美元。對 FY31 目標價（Base 121 美元）的衝擊：稅率高 3 個百分點約少 4.8 美元，FY28 起有機成長每年少 2 個百分點約少 9.4 美元，利潤率低 200 個基點約少 9.4 美元，終端倍數少 1 倍少 8.65 美元。價值陷阱風險中等，反證寫在反證紀錄。歷史最大回撤、債務條款與訴訟金額事實表未涵蓋；10-K 只列一般專業疏失索賠。","fact_refs":["f_kpi7_fy2026","f_week26_return_pct","f_ma_w250","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"EBITDA 高成長掩蓋每股盈餘停滯，便宜感部分來自 0% 稅率"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.07,"pe":13.06,"basis":"FY2026E 共識調整後 EPS（快照未反映 11-05 指引中點 5.20 美元）；終端倍數同用當年度調整後 EPS 口徑"},"eps":{"bull":[5.87,7.23,8.83,10.28,11.78],"base":[5.4,6.25,7.15,7.96,8.65],"bear":[4.4,4.2,4.35,4.55,4.8]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-40,"basis":"Bear 谷底 FY28 EPS 4.20 美元×9 倍得 38 美元，較現價約 −43%；若 FY27 指引落空，EPS 3.7 美元×8 倍得 30 美元，約 −55%。區間上緣 −40% 比 250 週均線 45.8 美元對應的 −31% 更深，因為 2.3 倍槓桿下技術支撐不可靠。事實表未涵蓋歷史最大回撤。","trigger_time":null},"basis":{"bull":"FY27 Adj EBITDA 約 1.50 億美元，FY31 約 2.9 億（淨營收年增約 15%，含小型併購，利潤率約 29%）；17 倍反映成長延續。事實表未涵蓋同業現值倍數，無法附對照。","base":"FY27 Adj EBITDA 約 1.46 億美元，有機淨營收約 10%，利潤率到 28%，稅率 22% 到 24%，FCF 還債到 FY31 利息歸零，股數年增約 1.8%。IRR 約 12.8%，EPS 複利 11.3 點、倍數 1.4 點。14 倍低於稅率還原後約 16 倍；事實表未涵蓋同業現值倍數，對照用公司自身 13.06 倍與 trailing 16.07 倍。","bear":"資料中心延案加上費率預算緊縮，FY27 Adj EBITDA 約 1.25 億美元低於指引，之後低個位數成長；10 倍來自成長降到 5% 以下的倍數壓縮。機率 30%：Base 成長超過內生上界，槓桿剛升到 2.3 倍。採信長約韌性，所以 Bear 是成長熄火，不是崩盤。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"公用事業與政府客戶靠費率和預算付款，CEO 自己說電費負擔已是最重要的考量；FY25 兩大客戶占合約營收 23.2%，其中 SCE 所屬集團已被 S&P 降到 BBB-；資料中心許可出現政治反彈。","assumption":"能效與電網規劃預算不會因電費壓力被砍，資料中心案照進度走。","consequence":"五年虧 50%（約 33 美元）最可能的路徑是 FY27 跌破 1.4 億美元指引，有機成長轉負，FY31 EPS 約 4.1 美元、8 倍。","ruling":"部分採納。Bear 機率定 30%，FY27 EBITDA 列為唯一致命數字；反駁一次崩潰的說法，NYPA 10 年合約續標與 Con Ed 第 17 年顯示核心客戶仍穩。","watch":"2 月有機成長揭露、公用事業客群年增率、SCE 評等","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"],"fact_refs":["f_kpi7_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 Adj EBITDA 年增 22%，Adj EPS 1.20 美元對 1.21 美元；GAAP EPS 0.76 對 0.90。指引隱含 Q4 Adj EPS 約 1.02 美元，去年同季 1.57 美元。FY26 全年 Adj EBITDA 增 38%，Adj EPS 僅增約 6%。稀釋股數 FY23 到 FY26 年增約 5.2%。","assumption":"EBITDA 成長會轉成每股成長。","consequence":"FY27 EBITDA 增逾 27%，Base Adj EPS 只增約 4%；若繼續以約 7% 報酬舉債併購，營收漂亮但每股價值不動。","ruling":"採納。Base 路徑按 22% 以上稅率、約 2,000 萬美元利息與持續稀釋建立，資本配置判定未過關。","watch":"FY27 Adj EPS 低於 5.0 美元，或年度稀釋股數增幅高於 3%","fact_refs":["f_kpi4_gaap_eps","f_kpi6_sbc","f_kpi7_fy2026"]},{"view":"價格已反映太多","evidence":"股價 26 週跌 25%，表面 13 倍，但分母用 0% 稅率；納入 Mantis 後 EV 約 13.1 億到 13.5 億美元，不是 10.58 億；FY27 GAAP 本益比估約 20 到 22 倍。","assumption":"市場會繼續用加回 SBC 與攤銷的調整後 EPS 定價。","consequence":"若市場改看 GAAP 或扣 SBC 後的 FCF，便宜感消失，倍數上修空間有限。","ruling":"採納一半。估值結論由偏便宜降為合理，Base 倍數 14 倍低於稅率還原後的 16 倍；但 FCF 若達標，扣 SBC 後殖利率仍約 7.4%。","watch":"FY27 扣 SBC 後 FCF 殖利率低於 6%","fact_refs":["f_fwd_pe_latest","f_pe_current","f_ev_m","f_net_debt_m"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 76.3 → 本次 66.22（-13.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=76.3","side_b":"本次 price_at_dd=66.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟡、均線 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟡、均線 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 76.3 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 76.3 美元：Bull 價 198、Bear 價 52，五年期望值 +80.0%，基準年化 13.5%，不對稱比 6.0","side_b":"本次情境、股價仍用 76.3 美元：Bull 價 200.26、Bear 價 48，五年期望值 +50.7%，基準年化 9.7%，不對稱比 2.92","ruling":"先換情境、股價不動：五年期望值少 29.3 個百分點，基準年化少 3.8 個百分點。不對稱比由 6.0 變為 2.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 76.3 美元：五年期望值 +50.7%，基準年化 9.7%，不對稱比 2.92","side_b":"本次情境、股價 66.22 美元：五年期望值 +73.7%，基準年化 12.8%，不對稱比 4.9","ruling":"再換股價、情境不動：起點價下跌 13.2%，五年期望值多 22.9 個百分點，基準年化多 3.2 個百分點，不對稱比由 2.92 升到 4.9。合計五年期望值比前份少 6.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"FY27 成長是自己長的還是買來的","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：FY27 合約營收 10 億美元、年增約 19%，EBITDA 超過 1.4 億、增逾 25%，有機成長維持低雙位數。","side_b":"Mantis 全年化後，FY26 備考合約營收約 9.4 億、淨營收約 5.03 億、Adj EBITDA 約 1.32 億；指引對備考僅增 6%、接近零、增 6%，Burton 1 到 4 月尚未計入。","ruling":"可調和：指引應視為下限，不是低雙位數有機成長的預測。Base 取 FY27 Adj EBITDA 約 1.46 億，高於下限但低於備考加 11% 有機。","evidence_level":"法說原話與本次換算；Burton 備考未揭露","settle_metric":"2027 年 2 月法說的有機與併購拆分","if_then":["若正式指引 Adj EBITDA ≥1.45 億美元且有機成長 ≥10%，加碼第二筆","若正式指引仍停在 1.40 億且有機成長低於 7%，停止加碼並下修 Base FY27 EPS 約 0.3 美元"],"evidence_refs":[]},{"axis":"EBITDA 與每股盈餘背離","cause":null,"prior_field":null,"side_a":"2026-11-05 CFO：獲利成長快於營收，TTM Adj EBITDA 增 29%、Adj EPS 5.75 美元增 41%。","side_b":"Q3 Adj EPS 持平，GAAP EPS 減 16%；FY26 指引隱含 Q4 Adj EPS 年減約 35%。TTM 41% 含低稅率效果。","ruling":"可調和：差異來自稅率回正、利息與稀釋。估值以稅率還原後的每股盈餘為準，FY26 的 13 倍不作便宜依據。","evidence_level":"法說與新聞稿","settle_metric":"FY27 有效稅率與 Adj EPS 指引","if_then":["若 FY27 稅率指引 ≥25%，Base FY27 EPS 下修約 0.2 美元並停止加碼","若 FY27 稅率指引 ≤20%，Base FY27 EPS 上修約 0.15 美元"],"evidence_refs":[]},{"axis":"Mantis 淨營收由 1.2 億改為 7,500 萬美元","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：會計師重新檢視淨營收組成，Mantis 利潤率因此是 35%，對公司有增益。","side_b":"收購公告後兩個月內，同一項目的淨營收少了 37.5%；2.85 億美元買價約 10.9 倍 EBITDA，高於 WLDN 目前約 9.3 到 9.6 倍。","ruling":"未證、監測。淨營收改變不一定改變 EBITDA，但本包沒有獨立驗證。預登記：FY27 Mantis Adj EBITDA 低於 2,400 萬美元，即視為管理層說法證偽。","evidence_level":"管理層單方說明","settle_metric":"FY27 Mantis Adj EBITDA 與淨營收","if_then":["若 Mantis FY27 Adj EBITDA 低於 2,400 萬美元，減碼一半","若 Mantis 達 2,800 萬美元以上且交叉銷售有具體案例，併購報酬項目重新評估"],"evidence_refs":[]},{"axis":"現金轉換","cause":null,"prior_field":null,"side_a":"2026-11-05 CFO：9 月營運資金是暫時落差，Q4 回補；長期 FCF 超過 Adj EBITDA 七成，FY27 約 9,800 萬美元。","side_b":"前九個月營業現金流 3,290 萬，低於去年 4,010 萬；FCF／Adj EBITDA 前九個月 35%、TTM 65%，都低於七成承諾。","ruling":"未證、監測。FY26 達 7,000 萬美元需要 Q4 FCF 約 4,220 萬，去年同季約 3,670 萬；預登記 FY26 低於 6,500 萬即視為暫時落差的說法證偽。","evidence_level":"新聞稿現金流量表與法說","settle_metric":"FY26 全年 FCF","if_then":["若 FY26 FCF 低於 6,500 萬美元，減碼一半","若 FY26 FCF ≥7,000 萬美元且 FY27 指引過關，加碼第二筆"],"evidence_refs":[]},{"axis":"毛利率與稅率的說法前後對照","cause":null,"prior_field":null,"side_a":"2026-08-06 CFO：Q2 毛利率減 150 個基點，歸因組合轉向績效工程與商業專案；下半年稅率約 15% 到 20%。","side_b":"2026-11-05 CFO：Q3 毛利率增 150 個基點至 38.4%，歸因有利組合、激勵收入與 LADWP；Q3 稅率實際 23%。","ruling":"同一個組合說法解釋相反方向，毛利率不能當結構性改善，改看 Adj EBITDA 占淨營收。稅率已高於上季說法，Base 不採 FY26 的低稅率。","evidence_level":"兩季法說原話","settle_metric":"連續四季 Adj EBITDA 占淨營收與 FY27 稅率","if_then":["若 FY27 單季 Adj EBITDA 占淨營收連 2 季低於 24%，停止加碼","若連 4 季高於 27%，利潤率假設上修"],"evidence_refs":[]},{"axis":"資料中心曝險能否裁決","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：資料中心需求沒有動搖，管線看到 2029 年以後，併網通常在流程末端，不會擋住前期工作。","side_b":"分析師直接問 FY27 含多少資料中心、APG 是否再翻倍，CEO 沒有給數字；電池儲能占比也只是估計 5% 以下。","ruling":"不可裁決至 2027 年 2 月。APG 約 7,500 萬美元僅占合約營收約 9%，所以這不是最大敏感項，但 Mantis 的資料中心占比未揭露，曝險上限未知。","evidence_level":"法說問答，未量化","settle_metric":"FY27 APG 與 Mantis 的資料中心收入揭露","if_then":["若 FY27 APG 指引低於 1.1 億美元，停止加碼","若管理層撤回管線看到 2029 年以後的說法，減碼一半"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣：槓桿剛升到 2.3 倍，併購報酬約 7%，現金轉換落後承諾，每股盈餘不成長，股價仍在 52 與 104 週均線下方，2 月前沒有明確的向上催化。","side_b":"持有：淨營收有機成長 12%，核心續約成功，指引下限保守，FCF 若達標扣 SBC 後殖利率約 7.4%，Base IRR 約 12.8%。","ruling":"不賣但不追：首筆限半倉，因本週的新負面資訊尚未進入賣方模型，2 月前凍結加碼。","evidence_level":"綜合判斷","settle_metric":"2027 年 2 月 FY26 現金流與 FY27 正式指引","if_then":["若股價先漲到 85 美元以上而 2 月數據未到，不追","若股價跌破 52 美元且有機成長仍 ≥10%，分批反買","若 FY27 Adj EBITDA 指引低於 1.40 億美元，清倉"],"evidence_refs":[]},{"axis":"基本面結論相對前份下修","cause":"新證據","prior_field":["signal","val","trap","moat_trend"],"side_a":"前份（2026-07-03，股價 76.3 美元）：進場、評級 A、估值偏便宜、價值陷阱風險低、護城河擴大。","side_b":"本次：評級 B、估值合理、價值陷阱風險中等、護城河穩定；裁決與角色依本次輸入重算。","ruling":"股價跌了但結論下修，原因是 7 月後三項新事實：Mantis 把淨負債由 2,300 萬拉到 2.93 億美元；179D 到期後 Q3 稅率 23%；Adj EBITDA 成長沒有轉成每股成長。護城河由擴大改穩定，因為客群擴張主要靠併購，定價權與同業報酬差距沒有擴大的證據。","evidence_level":"公司法說與新聞稿","settle_metric":"FY26 現金流、FY27 稅率與有機成長","if_then":["若 FY26 FCF ≥7,000 萬美元且有機成長 ≥10%，估值結論可回到偏便宜並加碼第二筆","若 FY27 有機成長低於 7%，停止加碼並重評護城河方向"],"evidence_refs":[]},{"axis":"情境機率、跑道與公司分類","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率 30%、空頭 25%、最大回撤 −45%、五年後跑道寬，未標公司類型與循環位置。","side_b":"本次：多頭 20%、基準 50%、空頭 30%，最大回撤 −40% 到 −55%；跑道仍寬，類型為品質複利成長，不按循環股處理。","ruling":"Base 路徑高於內生成長上界，空頭機率拉到 30%；回撤改成區間，下緣反映 2.3 倍槓桿。跑道結論未變。","evidence_level":"本次情境推導","settle_metric":"FY27 有機成長與淨槓桿","if_then":["若 Q3 FY27 淨槓桿 ≤1.8 倍且有機成長 ≥10%，下次複審把空頭機率降回 25%","若淨槓桿 ≥2.0 倍，減碼一半"],"evidence_refs":[]},{"axis":"加碼條件新設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（null）","side_b":"FY26 FCF≥7,000 萬美元且 2 月指引 Adj EBITDA≥1.45 億美元；或股價<52 美元且有機成長≥10%","ruling":"前份沒有明確的加碼條件；本次把加碼綁在現金流與正式指引，股價下跌時也要有機成長過關才分批反買，避免機械式攤平。","evidence_level":"方法補強","settle_metric":"FY26 FCF 與 FY27 正式指引","if_then":["條件成立才加碼第二筆","條件未成立則停止加碼"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）；前份風險門檻為 APG 連 2 季年增低於 50%、公用事業能效資金連 2 季年增低於 5%、FY27 OCF／淨利低於 1.0 或 Burton 淨營收低於 3,000 萬美元。","side_b":"FY27 Adj EBITDA 低於 1.40 億美元清倉；FY26 FCF 低於 6,500 萬美元減碼；Q3 FY27 淨槓桿 ≥2.0 倍減碼；有機成長連 2 季低於 9.5% 停止加碼。","ruling":"Mantis 舉債後最敏感的數字改為 EBITDA 與現金，因此新設清倉與減碼門檻。前份後兩條保留在風險欄，能效資金與 Burton 目前標資料缺口。APG 年增率門檻退休，因 FY26 基期已接近三倍，年增率失去鑑別力，改用 FY27 絕對金額 1.1 億美元。","evidence_level":"法說與前份紀錄","settle_metric":"各門檻對應的季度揭露","if_then":["任一清倉條件成立即清倉","減碼條件成立即減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（null）","side_b":"2027 年 2 月正式指引或 FY27 實績把 Adj EBITDA 壓到 1.40 億美元以下。","ruling":"Single Thing 選 EBITDA，因為它是數學上最大的敏感項：少 10% 約少 0.67 美元 Adj EPS，遠大於稅率與利率的影響。達標只需備考基礎上成長約 6%，若連這都做不到，代表核心業務沒有成長，應清倉。","evidence_level":"本次敏感度推導","settle_metric":"FY27 Adj EBITDA","if_then":["若低於 1.40 億美元，清倉","若高於 1.45 億美元，加碼第二筆"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY26 現金流與 FY27 正式指引同時過關，才加第二筆。","type":"加碼","maps_to":"H3","metric":"FY26 FCF 與 FY27 Adj EBITDA 指引","threshold":"FCF≥7,000 萬美元且 Adj EBITDA 指引≥1.45 億美元","action":"加碼第二筆","source_freq":"新聞稿與法說，每季","date":"2027-02"},{"n":2,"text":"FY27 Adj EBITDA 跌破指引下限。","type":"Single Thing","maps_to":"H2","metric":"FY27 Adj EBITDA","threshold":"低於 1.40 億美元","action":"清倉","source_freq":"新聞稿，每季","date":"2027-02"},{"n":3,"text":"Q4 營運資金沒有回補。","type":"減碼","maps_to":"R1","metric":"FY26 全年 FCF","threshold":"低於 6,500 萬美元","action":"減碼一半","source_freq":"新聞稿現金流量表，每季","date":"2027-02"},{"n":4,"text":"去槓桿沒有達標；公司目標門檻很鬆，未達代表現金流或併購紀律出問題。","type":"減碼","maps_to":"H3","metric":"季末淨槓桿","threshold":"Q3 FY27 季末 ≥2.0 倍","action":"減碼一半","source_freq":"法說資本結構頁，每季","date":"2027-11"},{"n":5,"text":"有機成長低於假設。","type":"假設驗證","maps_to":"H1","metric":"有機淨營收成長","threshold":"連 2 季低於 9.5%","action":"停止加碼","source_freq":"法說，每季","date":null},{"n":6,"text":"資料中心延案或管理層改口。","type":"風險","maps_to":"R2","metric":"FY27 APG 收入與資料中心管線說法","threshold":"FY27 APG 低於 1.1 億美元，或撤回管線看到 2029 年以後的說法","action":"減碼一半","source_freq":"法說，每季；單季 APG 目前未揭露","date":null},{"n":7,"text":"主要公用事業客戶信用轉弱或流失。","type":"風險","maps_to":"R3","metric":"SCE 信評與兩大客戶合約","threshold":"SCE 降至投機級，或兩大客戶任一流失","action":"停止加碼","source_freq":"信評公告與 10-K，事件驅動","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":8,"text":"競標壓價或人才分包成本侵蝕利潤。","type":"風險","maps_to":"R4、R6","metric":"Adj EBITDA 占淨營收；薪資福利年增減淨營收年增","threshold":"利潤率連 2 季低於 24%，或成本差距 ≥5 個百分點且利潤率年減連 2 季","action":"停止加碼","source_freq":"新聞稿與法說，每季","date":null,"evidence_refs":["competitive_share_entrants#1","geo_supply_chain#0"]},{"n":9,"text":"股價先跌而基本面未破時分批反買；股價先漲而數據未到時不追。","type":"估值rearm","maps_to":"H1","metric":"股價與有機成長","threshold":"低於 52 美元且有機成長 ≥10%；高於 85 美元且 2 月數據未到","action":"分批反買；不追","source_freq":"每日股價與每季法說","date":null},{"n":10,"text":"FY26 全年財報與 FY27 正式指引公布後重新研究。","type":"複審日期","maps_to":"H1、H2、H3","metric":"有機成長、稅率、FCF、Adj EBITDA 指引","threshold":"公布即複審","action":"重跑完整研究","source_freq":"2027 年 2 月下旬法說","date":"2027-02"}],"kill_metrics":[{"metric":"FY27 Adj EBITDA","bear_threshold":"低於 1.40 億美元即清倉","window":"2027-02 指引起至 FY27 實績","source":"公司新聞稿 8-K","last_status":"ok"},{"metric":"FY26 全年 FCF","bear_threshold":"低於 6,500 萬美元即減碼一半","window":"2027-02 公告","source":"新聞稿現金流量表","last_status":"warning"},{"metric":"季末淨槓桿","bear_threshold":"Q3 FY27 季末 ≥2.0 倍即減碼一半","window":"至 2027-11 公告","source":"法說資本結構頁","last_status":"ok"},{"metric":"有機淨營收成長","bear_threshold":"連 2 季低於 9.5% 即停止加碼","window":"FY27 逐季","source":"每季法說","last_status":"ok"},{"metric":"Adj EBITDA 占淨營收","bear_threshold":"單季連 2 季低於 24% 即停止加碼","window":"FY27 逐季","source":"新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"FY26 FCF≥7,000 萬美元且 2 月指引 Adj EBITDA≥1.45 億美元；或股價<52 美元且有機成長≥10%","exec_line":"現價先建計畫部位一半，2 月法說前不加碼；FY26 現金流與 FY27 正式指引過關才加第二筆。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把資料中心政治風向當成全公司風險，但 APG 約 7,500 萬美元只占 FY26 隱含合約營收約 9%，主體是 NYPA、Con Ed 等公用事業與政府工作；FY27 指引下限也只要求備考基礎上成長約 6%。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"成長不是只靠併購撐出來：FY27 有機淨營收維持低雙位數。","2y":"FY27 有機淨營收成長 ≥10%（Q3 FY26 為 12%，Energy 為 17%）","5y":"FY31 淨營收 ≥7.7 億美元（不含 FY27 後新併購）","10y":null,"threshold":"FY27 有機淨營收 ≥10%；FY31 淨營收 ≥7.7 億美元","source":"新聞稿與每季法說的有機成長揭露；2027 年 2 月法說首度拆分 FY27 有機與併購","drift_rule":"TTM 有機成長連 2 季低於 9.5% 為削弱，連 3 季低於 9% 為反轉"},{"id":"H2","text":"併購後 Adj EBITDA 利潤率站上 27% 以上，Mantis 的 35% 利潤率成立。","2y":"FY27 Adj EBITDA ≥1.40 億美元，占淨營收 ≥27%","5y":"FY31 Adj EBITDA 占淨營收 ≥28%","10y":null,"threshold":"FY27 Adj EBITDA ≥1.40 億美元且利潤率 ≥27%；FY31 利潤率 ≥28%","source":"2026-11-05 CFO 長期目標為高 20% 區間；FY26 指引中點 1.10 億／4.40 億美元為 25%","drift_rule":"自 Q2 FY27 起，TTM 利潤率連 2 季低於 25.6% 為削弱，連 3 季低於 24.3% 為反轉"},{"id":"H3","text":"現金跟得上 EBITDA：FCF 達 Adj EBITDA 七成，淨槓桿實際下降。","2y":"FY26 FCF ≥7,000 萬美元；FY27 FCF ≥9,800 萬美元；Q3 FY27 淨槓桿 ≤1.8 倍","5y":"FY31 FCF ≥1.5 億美元，累計 FCF 高於同期併購支出","10y":null,"threshold":"FCF／Adj EBITDA ≥70%；Q3 FY27 淨槓桿 ≤1.8 倍（公司目標低於 2.0 倍太鬆，以 1.4 億 EBITDA 計只需再少約 1,300 萬美元淨負債）","source":"新聞稿現金流量表與法說資本結構頁","drift_rule":"TTM FCF／Adj EBITDA 連 2 季低於 66.5% 為削弱，連 3 季低於 63% 為反轉（目前 65%）；前份門檻保留：TTM OCF／淨利連 2 季低於 1.0 為削弱"}],"R":[{"id":"R1","text":"9 月營運資金落差沒有在 Q4 回補，現金轉換承諾落空。","h_ref":"H3","clock":"⚡","threshold":"FY26 全年 FCF 低於 6,500 萬美元，即 Q4 低於約 3,720 萬美元","evidence_refs":[]},{"id":"R2","text":"資料中心許可與併網遭政治反彈，APG 與 Mantis 的資料中心客戶延案。","h_ref":"H1","clock":"🔥","threshold":"FY27 APG 低於 1.1 億美元（前份門檻保留，單季未揭露，標資料缺口），或管理層撤回管線看到 2029 年以後的說法","evidence_refs":[]},{"id":"R3","text":"電費負擔壓力讓能效與電網規劃預算被砍，主要公用事業客戶信用轉弱或流失。","h_ref":"H1","clock":"🔥","threshold":"公用事業能效資金連 2 季年增低於 5%（前份門檻保留，標資料缺口）；SCE 降至投機級；兩大客戶任一流失","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R4","text":"競標壓價，且多家得標合約不保證工作量。","h_ref":"H2","clock":"🔥","threshold":"單季 Adj EBITDA 占淨營收連 2 季低於 24%，或 NYPA 年工作量低於 5,000 萬美元","evidence_refs":["competitive_share_entrants#1"]},{"id":"R5","text":"併購過多或 Mantis 整合失敗，舉債收購的報酬低於資金成本。","h_ref":"H2、H3","clock":"🔥","threshold":"Mantis FY27 Adj EBITDA 低於 2,400 萬美元；FY27 全年 OCF／淨利低於 1.0，或 Burton 淨營收低於 3,000 萬美元（後兩項前份保留）","evidence_refs":[]},{"id":"R6","text":"人才與分包成本侵蝕利潤；Q3 薪資福利年增 24%，高於淨營收年增 18%。","h_ref":"H2","clock":"⚡","threshold":"薪資福利年增高於淨營收年增 ≥5 個百分點，且 Adj EBITDA 利潤率年減，連 2 季","evidence_refs":["geo_supply_chain#0"]},{"id":"R7","text":"FY27 稅率高於 22%，每股盈餘再被壓低。","h_ref":"H2","clock":"⚡","threshold":"2 月指引 FY27 有效稅率 ≥25%，每高 3 個百分點約少 0.21 美元 Adj EPS","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月正式指引或 FY27 實績把 Adj EBITDA 壓到 1.40 億美元以下。","why_fatal":"達標只需在備考約 1.32 億美元上成長約 6%；做不到代表核心業務沒有成長。槓桿 2.3 倍下，EBITDA 每少 10% 約少 0.67 美元 Adj EPS，是最大單一敏感項。","if_happens":"清倉，股價可能落到 Bear 路徑的 38 到 48 美元。","how_monitor":"2 月正式指引、每季 Adj EBITDA、有機成長與併購拆分、Mantis 貢獻。","probability":"約 15% 到 20%（12 到 24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":12.22,"peg_fy2":1.46,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":4.91,"FY2026E":5.07,"FY2027E":5.42,"FY2028E":null},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS。FY2025A 4.91 美元由逐字稿推算（前九個月 4.18 美元年增 25%，TTM 5.75 美元）；FY2026E 與 FY2027E 為 Koyfin 共識快照，未反映本次財報與 Mantis；FY2028E 共識事實表未涵蓋，留空。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY26 財報與 FY27 正式指引，首度拆分有機與併購","impact":"高","watch":"FY26 FCF、FY27 Adj EBITDA、有機成長、稅率"},{"date":"2027-Q2","date_precision":"quarter","type":"guidance","event":"Q1 FY27 財報，現金流季節性偏弱的第一次檢驗","impact":"中","watch":"淨槓桿與 Mantis 整合進度"},{"date":"2027-Q4","date_precision":"quarter","type":"guidance","event":"Q3 FY27 財報，檢驗淨槓桿承諾","impact":"高","watch":"淨槓桿是否 ≤1.8 倍"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"LADWP 太陽能路燈專案放量，CEO 稱 2027 年可能成為最大客戶","impact":"中","watch":"放量速度與客戶集中度"},{"date":null,"type":"regulatory","event":"各州資料中心許可與併網限制的政策進展","impact":"中","watch":"德州、俄亥俄州的政策與 APG 管線說法"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把資料中心政治風向當成全公司風險，但 APG 約 7,500 萬美元只占 FY26 隱含合約營收約 9%，主體是 NYPA、Con Ed 等公用事業與政府工作；FY27 指引下限也只要求備考基礎上成長約 6%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-25.08, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
