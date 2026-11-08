你是 DD 管線 v20 的判斷層閘（gate），標的 6669.TW（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_ifrs`（q1_business）｜合併營收（IFRS）＝278.153 十億 NT$｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿 wiwynn.com/news/wiwynn-reports-second-quarter-2026-financial-results（YoY +26.0%）；QoQ +0.59% 為上半年 554.660 − Q2 278.153 = Q1 276.507 推算（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無營收共識
- `f_kpi1`（q1_business）｜毛利率＝9.3 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；公司歸因＝記憶體代採購模式移出營收與成本＋新產品導入帶來較高 NRE 收入（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無毛利率共識
- `f_kpi2_ifrs_non_gaap`（q1_business）｜營業利益率（IFRS，緯穎不揭露 Non-GAAP）＝7.3 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；新聞稿未列營業利益金額（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無營益率共識
- `f_kpi3_pat_eps`（q1_business）｜稅後淨利（PAT）／基本 EPS＝14.969 十億 NT$（EPS NT$80.43）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；PAT 年增 23.5%，PAT margin 5.4%；Q2 2025 EPS NT$65.23（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：凱基事前預估 EPS 82.01 元（來源：KGI 報告 2026-07-28，實際略低於該預估）；非全市場共識
- `f_kpi4`（q1_business）｜管理層指引（下一季／全年）＝無量化指引｜期間與口徑：Q2 2026（公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：緯穎 IR 新聞稿（同上）：僅表示對 AI 與資料中心市場長期成長樂觀，未給營收／利益率區間；並提及 AI 產品組合變化與零組件成本上升，正與客戶調整商業模式（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（公告於 2026-08-07））
  - 註記：不適用
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝579.63 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝132.11 TWD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×33.1093 @ 2026-11-07)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_peer_6669_tw_operating_margin_pct`（q2_moat）｜6669.TW 營業利益率＝6.62 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2382_tw_operating_margin_pct`（q2_moat）｜2382.TW 營業利益率＝3.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2382.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3231_tw_operating_margin_pct`（q2_moat）｜3231.TW 營業利益率＝3.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3231.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_smci_operating_margin_pct`（q2_moat）｜SMCI 營業利益率＝7.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SMCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6669_tw_gross_margin_pct`（q2_moat）｜6669.TW 毛利率＝8.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝192.37 TWD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×33.1093 @ 2026-11-07)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝241.37 TWD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×33.1093 @ 2026-11-07)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝1399677.81 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝2488718.28 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝85277.45 TWD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 187896.81、現金 102619.36（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q1_business）｜下半年資本支出預算＝942 百萬 US$｜期間與口徑：董事會 2026-08-07 核准（2026 下半年）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）：主要用於電力基礎設施、設備、土地與廠房；同時核准首次國內無擔保可轉債上限 NT$150 億與 US$15 億聯貸（numbers.latest_quarter_kpis.items[5]，as_of 董事會 2026-08-07 核准（2026 下半年））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.113 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_peer_6669_tw_fcf_margin_pct`（q2_moat）｜6669.TW FCF 利潤率＝-5.84 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝986599.04 TWD m｜期間與口徑：2026-11-08／市值 901321.59 ＋ 淨負債 85277.45｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1555.0 TWD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝11.77 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 132.11，分子＝快照價 1555.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（132.11 → 132.11）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（192.37 → 192.37）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.14 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（241.7 → 241.37）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝15.85 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.7 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.77 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-8.22 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝25.67｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝1622.86 TWD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝1224.93 TWD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟢｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 1555.0 / W52 1622.86 / W104 1224.93 / W250 769.32 / W250 13週斜率 3.12%」

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Q1 2026 營收 NT$276.5B（YoY +62%），毛利率 7.6%；與鴻海、廣達、英業達等 ODM 同樣出現營收增速高於毛利增速
  - 來源：Borecraft：AI server ODMs are running into awkward math（as_of 2026-05-01）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：Quartr Q1 2026 摘要指客戶集中度與訴訟為風險；以美國為主要市場
  - 來源：Quartr Wiwynn (6669) Q2 2026 earnings summary（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：CMoney 研究筆記稱緯穎營收 Meta 占 52%、Microsoft 占 34%、其他 14%（合計兩大客戶 86%）；為 2024 年資料，非 2026 年揭露，as_of 為約略年份
  - 來源：CMoney 研究筆記 note-detail nid=782415（經搜尋摘要轉引）（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：Quartr 2026 Q1 摘要將客戶集中與訴訟列為風險，未給占比
  - 來源：Quartr, Wiwynn (6669) Q2 2026 earnings summary（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：Goldman估計2027年需約4,000億美元投資級債券發行支應建置，且五大hyperscaler每年需約3,000億美元AI相關營收才能打平基礎設施投資（融資風險面）。
  - 來源：roic.ai: Goldman Sachs sees AI capex at 12 trillion by 2027 fueling debt financed buildout（as_of 2026-09-25）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：緯穎產能分布：墨西哥占總產能 70%、馬來西亞 20%、歐洲 10%；德州第二棟廠明年量產後，美國產能預計占 20%。
  - 來源：Taipei Times, 2026-09-18 Wiwynn Texas plant report（as_of 2026-09-18）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年報導：墨西哥產出因 USMCA 待遇避開部分關稅；有客戶要求停止自墨西哥出貨、改由捷克或馬來西亞工廠供應（摘要轉述，未取得原文）。
  - 來源：Taipei Times / Taiwan News 2025 coverage (search summary)（as_of 2025-03-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Q1 2026 毛利率 7.6%（Q4 2025 為 7.2%）；GPU與DRAM價格推升營收但毛利未同步；4月起部分客戶改由雲端客戶直購記憶體、記憶體不計入營收，4月營收月減16%；Q1 78%銷售來自美洲；ODM-direct 約占 Q1 2026 伺服器營收 50.2%（IDC）；緯穎在台灣五大AI伺服器ODM中Q1營收排第四
  - 來源：Borecraft / Digitimes 2026-06-15 (secondary)（as_of 2026-06-15）｜affects：decision_inputs.bear、moat_trend、valuation
- `ems_utilization_capex_cycle#0`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：Amazon 與緯穎於 2026-09-09 表示德州 Socorro 伺服器製造據點投資額已超過 US$1.6 billion（2025-06 首次揭露為 US$152 million）；報導未說明 Amazon 是否共同出資。
  - 來源：CTOL, Wiwynn's $1.6B Texas Expansion: Amazon Gets the Capacity, Wiwynn Takes the Risk（as_of 2026-09-09）｜affects：thesis.R、decision_inputs.bear、valuation
- `ems_roic_asset_turnover_benchmark#0`（ems_roic_asset_turnover_benchmark｜方向 -｜狀態 ok）：Wiwynn 2026Q1末存貨約NT$229.2B（較上季+68%），應收約NT$91.8B；存貨堆高拉長現金循環（僅事實，未見官方CCC數字）
  - 來源：Wiwynn 26Q1 investor conference presentation (2026-05-07)（as_of 2026-05-07）｜affects：decision_inputs.bear、valuation
- `ems_roic_asset_turnover_benchmark#1`（ems_roic_asset_turnover_benchmark｜方向 -｜狀態 ok）：StockAnalysis資產負債表：2026/3/31總資產約NT$432.6B（FY2025末NT$338.2B），存貨約NT$229B（前期NT$136B），應付帳款NT$152.6B
  - 來源：StockAnalysis Wiwynn balance sheet（as_of 2026-03-31）｜affects：decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":5330,"bear_5y_price":960,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":76.8,"ev5y_pct":69.7,"irr_base_pct":12.1,"asym_ratio":3.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":132.11,"pe":11.77,"basis":"FY2026E 共識 EPS，拆股後每股口徑，與終端倍數同為當年度 EPS 本益比"},"eps":{"bull":[210,275,320,365,410],"base":[175,205,215,230,250],"bear":[150,135,95,105,120]},"pe":{"bull":13,"base":11,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":3.113,"net_buyback":-0.3},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 4 | 3 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 2 | 3 |
| channel_business_model_shift | found | 2 | 4 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |
| ems_utilization_capex_cycle | found | 2 | 3 |
| ems_roic_asset_turnover_benchmark | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","irr_base_pct":6.1,"ev5y_pct":35.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.4,"ev5y_pct":35.9,"irr_base_pct":6.1,"max_dd_pct":-60,"bull_5y_price":5520,"bear_5y_price":1125,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","price_at_dd":2275.0,"archetype":"EMS/ODM","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"6669.TW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"緯穎"},"oneliner":"緯穎靠 AWS 的 ASIC 機櫃訂單快速成長，現價約 2027 年共識 EPS 的 8 倍，是否便宜取決於第三季財報與 2027 年獲利預估能否守住；股價四週跌三成的原因尚未查明，先等財報再決定。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/scenario.json","answers":{"q1_business":{"verdict":"緯穎賺的是大型雲端客戶 ASIC 與通用伺服器機櫃的設計導入與全球交付的錢，利潤卡在少數客戶的專案分配上，晶片與記憶體的利潤不在它手上。","reasoning":"2025 年 AI 伺服器與通用伺服器各約占營收一半，AI 之中 ASIC 約九成，管理層預期 2026 年 AI 過半。2026 年第二季營收 2,781.53 億元、年增 26.0%，毛利率 9.3%、營益率 7.3%，稅後淨利 149.69 億元。毛利率從第一季 7.6% 升到 9.3% 有兩個來源：4 月起部分客戶的記憶體改代採購，營收與成本同時移出；另一個是新產品 NRE 收入。前者是列報方式改變，後者公司未量化，都不能當成定價能力提升。單點依賴：凱基 2026-07 指 AWS 將續為最大客戶，高盛估 2026 年緯穎約占 AWS 相關份額七成；2026 年實際客戶占比事實表未涵蓋，2024 年資料是 Meta 52%、Microsoft 34%，已過時。產業週期判為過熱期：報導稱 CoWoS 產能訂滿到 2027 年，高盛估 2027 年需約 4,000 億美元投資級債支應建置。供需持久性判斷為週期性將反轉，高盛看供需最早 2027 下半年平衡、2028 年資本支出增速降到 12%。每股數字要留意：事實表股數 579.63 百萬股，約為第二季推算股數 186 百萬股的三倍，共識 EPS 與現價是拆股後口徑，歷年 EPS 265.54 元與第二季 80.43 元是拆股前口徑，不能直接相比。拆股比例事實表未直接揭露，此處由股數推得。本次沒有逐字稿。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_non_gaap","f_kpi3_pat_eps","f_kpi4","f_shares_diluted_m","f_consensus_eps_fy1"],"verdict_values":{"revenue_quality":"營收年增率自 2026 年 4 月起因記憶體代採購被低估，毛利率被墊高，與前期比較需要調整；公司未揭露調整金額，事實表未涵蓋。","unit_econ_note":"低毛利、高周轉：2025 年毛利率 8.25%、營益率 6.72%。以 2027 年共識營收計，每 1 個百分點淨利率約等於每股 43 元，占共識 EPS 22%。","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"客戶高度集中、低毛利高周轉、需求跟隨雲端資本支出週期"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：高盛與摩根士丹利預估 2027 年五大雲端資本支出約 1.2 兆美元，高盛看 2028 年增速降到 12%，供需最早 2027 下半年平衡。","bargaining":{"up":"對晶片與記憶體供應商議價力弱，部分記憶體已改由客戶直購。","down":"客戶少而大，AWS 為最大客戶；2026 年占比事實表未涵蓋。","geo":"墨西哥占產能 70%、馬來西亞 20%、歐洲 10%，德州第二棟廠量產後美國預計占 20%。"},"profit_pool_dir":"事實表未涵蓋五年利潤池數字；可見的方向是利潤集中在晶片與記憶體端。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與五年利潤池占比，只有 ODM 直供占伺服器營收 50.2% 與雲端資本支出預估，不足以成表。"}}}},"q2_moat":{"verdict":"護城河方向持平：ASIC 機櫃的導入與交付能力仍領先，定價空間沒有變大。","reasoning":"機制是與少數雲端客戶共同開發 ASIC 機櫃，再用分散在墨西哥、馬來西亞、歐洲與德州的產能交付，換代時要重新認證，客戶不容易臨時換人。可驗證的方向有兩個。第一，高盛 2026-09 估緯穎仍維持約七成 AWS 相關份額，沒有份額下滑的來源，但這是單一券商估計。第二，過去 12 個月營益率 6.62%，高於廣達 3.34%、緯創 3.80%，低於 SMCI 7.09%；同業只有單期資料，算不出利差方向，ROIC 對比事實表未涵蓋。執行面評 8 分，定價面評 6 分：營益率領先台灣同業約 3 個百分點，但部分優勢來自產品組合，凱基也預期 GPU 專案會稀釋 2027 年毛利率。產業態勢裁決為雙向拉鋸：競爭面同業同樣出現營收增速高於毛利增速，結構面 AMD Helios 與通用伺服器提供新來源，其他變數是代採購商模改變與關稅。","fact_refs":["f_peer_6669_tw_operating_margin_pct","f_peer_2382_tw_operating_margin_pct","f_peer_3231_tw_operating_margin_pct","f_peer_smci_operating_margin_pct","f_peer_6669_tw_gross_margin_pct","f_kpi1"],"verdict_values":{"moat":{"mechanism":"ASIC 機櫃共同開發與多地交付，靠換代重新認證形成轉換成本","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：高盛估 2026 年 AWS 相關份額仍約七成，AMD Helios 訂單份額據轉述可達三到四成。定價面穩定偏弱：毛利率回升來自列報方式改變與 NRE，沒有提價證據。","competitor_notes":[{"name":"2382.TW","strategy_note":"營益率 3.34%、毛利率 5.54%，利潤率低於緯穎；事實表未涵蓋其 ASIC 份額，無法判斷是否正切入同一客戶。"},{"name":"3231.TW","strategy_note":"營益率 3.80%，FCF 利潤率 −8.93%，擴產吃現金比緯穎更重；過去協助緯穎處理部分組裝，備援關係值得追蹤。"},{"name":"SMCI","strategy_note":"毛利率 10.82%、營益率 7.09% 略高於緯穎，但 FCF 利潤率 −17.85%，較高的利潤率同樣沒有換成現金。"}],"peer_na_reason":"事實表的同業資料只有單期利潤率，沒有 ROIC 與多年序列，無法計算利差趨勢。","threats":[{"level":"🟡","text":"同業在 AI 伺服器同樣擴張，營收增速高於毛利增速，若搶單變成價格競爭，緯穎的利潤率優勢會縮小。","p":"35%","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"level":"🟡","text":"最大客戶引入第二供應商或分散次世代專案，這是最直接的份額風險。","p":"30%","evidence_refs":["customer_second_source#3","customer_concentration_credit#1"]},{"level":"🟡","text":"客戶把更多高價零組件改為自行採購，營收與議價基礎被壓縮，但緯穎的營運資金負擔同時下降。","p":"40%","evidence_refs":["channel_business_model_shift#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"付款者是雲端資本支出，2027 年預估約 1.2 兆美元；高盛估當年需約 4,000 億美元投資級債支應，五大雲端每年需約 3,000 億美元 AI 營收才打平，需求可以延後。"},{"item":"決策層級","level":"🟡","text":"客戶以每一代平台為單位分配專案，高盛估 AWS 相關份額約七成，顯示轉換有成本；合約年限、重新認證週期與失單紀錄事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"緯穎近四年毛利率在 8% 到 10% 區間，價值多被晶片與記憶體拿走，部分記憶體已由客戶直購；共識隱含淨利率由 2026 年 5.5% 降到 2027 年 4.5%。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業，沒有民生價格上限問題；政策風險在關稅與產地規則，已列入風險項。"}],"roiic":34.4,"reinvest_rate":125,"endo_ceiling":34.4,"formula_note":"單位為百分比。FY2022 到 FY2025 淨利增加 369.4 億元，FY2023 到 FY2025 累計再投資 1,075.3 億元（淨利減 FCF 的代理值），增量報酬 34.4%；同期累計淨利 859.4 億元，再投資率 125%。超過 100% 的部分靠外部資金，不算內生，內生上界取 34.4%；不設上限時為 43.0%。以淨利代替稅後營業利益是近似值，期間又涵蓋 AI 放量，下一筆投資未必拿到同樣報酬。當期 ROIC 因事實表未涵蓋投入資本而無法計算。"}}}},"q3_growth":{"verdict":"五年後跑道中等：ODM 直供已占伺服器營收約一半，第二曲線 AMD Helios 尚未驗證，而且可能稀釋毛利率。","reasoning":"成長主要靠量，零組件漲價也墊高過營收，沒有併購或回購貢獻。共識 EPS 由 2025 年 88.19 元（淨利 511.18 億元除以現行股數換算）升到 2028 年 241.37 元，三年複合 39.9%。內生上界 34.4%，缺口 5.5 個百分點。缺口無法歸因到利潤率擴張（共識隱含淨利率由 5.4% 降到 2027 年 4.5%）、回購或併購，實際上靠舉債加速再投資，依賴re-rate，長期信心上限為中。跑道方面，IDC 資料顯示 ODM 直供占 2026 年第一季伺服器營收 50.2%（二手轉述），落在 35% 到 70%。凱基估 2027 年 Helios 機櫃出貨 4,000 到 5,000 櫃，是可能的第二曲線，但仍在寄售，GPU 專案也可能稀釋毛利率，暫不算已成立。衰退訊號亮一項：自由現金流對淨利比連兩年低於 0.75（FY2024 −1.10、FY2025 −0.28）；毛利率單季年比、SBC、維護性資本支出事實表未涵蓋。FY2025 營收年增 163.7%、營業利益年增約 127%，差距超過 3 個百分點，營運槓桿被零組件轉嫁壓縮。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"量為主，零組件轉嫁墊高營收，無併購與回購","runway_years":"ODM 直供占比已過 30%，這項換算不適用","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的增量報酬 34.4% 與再投資率上限 100%，共識複合成長 39.9% 超過上界。","segments":[{"item":"ASIC AI 伺服器","value":"2025 年約占營收 45%（AI 約一半、其中 ASIC 約九成），凱基預期毛利率高於公司平均"},{"item":"GPU AI 伺服器","value":"2025 年約占營收 5%，2026 下半年起供應 AMD MI450，可能稀釋 2027 年毛利率"},{"item":"通用伺服器","value":"2025 年約占營收一半，Nomura 預期 2026 年出貨年增 20% 到 30%"}],"decay_signals":["自由現金流對淨利比連兩年低於 0.75：已亮","毛利率連兩季年比下滑：事實表未涵蓋單季對比","SBC 占營收：事實表未涵蓋","維護性資本支出占 FCF：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置仍在投入期，現金被擴產與存貨吃掉，配息實際靠融資支應。","reasoning":"FCF 連續為負：FY2024 −251.0 億元、FY2025 −145.6 億元，過去 12 個月 FCF 利潤率 −5.84%。淨負債 852.8 億元。董事會 2026-08-07 核准下半年資本支出 9.42 億美元、最多 150 億元可轉債與 15 億美元聯貸；德州投資額由 1.52 億美元增至逾 16 億美元，報導未說明 Amazon 是否共同出資。過去 12 個月股息殖利率 3.11%，約等於每年 280 億元配息，在 FCF 為負時由融資支應，不該視為剩餘現金回饋。並購與回購事實表沒有紀錄，僅有出售 LiquidStack 持股 1,540 萬美元；SBC 事實表未涵蓋。FY2022、FY2023 的 FCF 為正（290.9 億元、180.6 億元），負值與高速擴張同時出現，需求放緩時營運資金可能回流，前提是存貨賣得掉。","fact_refs":["f_net_debt_m","f_kpi5","f_dividend_yield_ttm","f_peer_6669_tw_fcf_margin_pct","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表未見緯穎作為收購方的併購案，僅出售 LiquidStack 持股。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄。"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"事實表未涵蓋 SBC；可轉債上限 150 億元約為市值 1.7%，屬另一類稀釋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，事實表也未涵蓋近三年現金去向四分與回購均價，無法展開。"}}}},"q5_valuation":{"verdict":"現價等於假設可持續 EPS 約 155 元（以 10 倍計），比 2027 年共識低 19%。我傾向認為共識偏高，但不確定偏高多少，所以便宜的結論先不成立。","reasoning":"現價 1,555 元，2026 年共識本益比 11.77 倍，2027 年 8.08 倍。以 10 倍回推，市場認為可持續 EPS 約 155.5 元，比共識 192.37 元低 19%，比我的基準 175 元低 11%。共識有三個爭議。第一，Koyfin 數字由美元換算，2026 年 132.11 元高於其他來源換成拆股後的數字：FactSet 348.72 元約 116 元、凱基 370.69 元約 124 元、Simply Wall St 淨利 667.97 億元約 115 元，不過這些來源日期較舊；2027 年營收共識 2.49 兆元也比 StocksGuide 的 2.1 兆元高 19%。第二，最近兩次共識快照修正為 0.0%，股價四週跌 31.6% 時仍未變動，可能是共識還沒反映跌因，也可能是資料未更新。第三，第二季毛利率含 NRE。賣方目標價換成拆股後約 2,200 到 2,500 元，都是大跌前的數字，不能當支持證據。同業 Fwd P/E 事實表未涵蓋，終端倍數只能對照自身現值，這是缺口。P/S 0.70 倍與 EV/S 0.77 倍換算的營收分母約 1.28 兆元，高於依公司數字推得的過去 12 個月營收約 1.11 兆元，這兩個倍數未用於結論。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current"],"verdict_values":{"valuation":{"basis":"本益比，以 FY2026E 與 FY2027E 共識 EPS 為分母，採拆股後每股口徑","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業 Fwd P/E，無法做倍數比較。"},"fwd_pe":11.77,"peg":0.29,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"以共識計 2027 年 8.08 倍看似便宜，但分母有爭議，便宜的論證不能用；改用我的 2027 年基準 175 元為 8.9 倍，週期高點的本益比通常偏低，結論維持中性。短期上檔以 2027 年基準 175 元乘 10 倍得 1,750 元；中期以 2028 年基準 205 元乘 11 倍得 2,255 元。五年分位無法計算：事實表只有 4 個年度端點，歷史本益比的股價與 EPS 也可能拆股口徑不一致。","upside_short_pct":12.5,"upside_mid_pct":45.0,"denominator_disputed":true,"denominator_note":"2027 年 EPS 是估值爭點：Koyfin 2026 年共識經美元換算後高於其他來源約 7% 到 17%，最近修正為零，第二季利潤又含 NRE。便宜的論證在第三季財報前不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方有兩個：把週期高點的低本益比當便宜，或把市場過度恐慌誤認成基本面惡化。","reasoning":"股價從前份判斷時的 2,275 元跌到 1,555 元，四週跌 31.6%，RSI 25.67，跌破 52 週均線 1,622.86 元，仍高於 104 週均線 1,224.93 元。事實表找不到這段下跌的原因：多數資料抓取於 10-12，第三季財報與 7 到 10 月月營收都未收錄。所以我既不能說市場錯，也不能說基本面壞了。陷阱風險評為中等：低本益比、FCF 為負、客戶集中同時存在，符合週期股假便宜的形狀，但目前沒有份額流失或共識下修的直接證據。歷史最大回撤與訴訟金額事實表未涵蓋，Quartr 摘要提及訴訟風險但未說明案情。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_state","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"低本益比可能是週期高點的假便宜"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":132.11,"pe":11.77,"basis":"FY2026E 共識 EPS，拆股後每股口徑，與終端倍數同為當年度 EPS 本益比"},"eps":{"bull":[210,275,320,365,410],"base":[175,205,215,230,250],"bear":[150,135,95,105,120]},"pe":{"bull":13,"base":11,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":2.5,"net_buyback":-0.3},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-48,"basis":"熊市路徑谷底年 2029 年 EPS 95 元，乘 6.5 到 8.5 倍得 618 到 808 元，相對現價 −60% 到 −48%。倍數下緣低於終端 8 倍，反映週期谷底的情緒折價；事實表未涵蓋歷史最大回撤，此區間由情境推得。","trigger_time":null},"basis":{"bull":"ASIC 與 Helios 同時放量，AWS 份額守住，2028 年 EPS 高於共識約 14%，終端 13 倍。","base":"2027、2028 年 EPS 低於共識 9%、15%，2029 年資本支出放緩後低速成長，終端 11 倍略低於現值 11.77 倍；股利由 3.1% 下修到 2.5%，可轉債每年稀釋約 0.3%。同業 Fwd P/E 事實表未涵蓋。","bear":"雲端資本支出 2028 年後轉跌，AWS 份額流失，2029 年 EPS 跌到 95 元，終端 8 倍作為成長降到 10% 的本益比錨。機率 35%：共識成長超過內生上界，且股價下跌原因未查明。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"高盛估 2027 年需約 4,000 億美元投資級債支應建置，五大雲端每年要約 3,000 億美元 AI 營收才打平；緯穎收入高度依賴少數客戶。","assumption":"AI 資本支出到 2028 年仍維持成長。","consequence":"2029 年 EPS 跌到 95 元、本益比 6.5 倍時股價約 618 元，虧損約 60%。","ruling":"採納，列為熊市路徑，機率 35%。","watch":"五大雲端 2028 年資本支出指引、緯穎月營收年增率。","evidence_refs":["supply_demand_durability#5","customer_concentration_credit#0","customer_second_source#3"]},{"view":"論點失敗","evidence":"四週股價下跌 31.6%，事實表沒有對應的消息或第三季資料，最近共識修正為 0.0%。","assumption":"目前的共識仍有效。","consequence":"若跌因是訂單或毛利率變化，2027 年 EPS 可能低於 173 元，10 倍的進場條件失效。","ruling":"不可裁決至第三季財報公布；在此之前不把下跌當安全邊際。","watch":"第三季財報、財報後兩週內的共識修正。","fact_refs":["f_price_at_dd","f_consensus_rev_fy2_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年第一季末存貨約 2,292 億元、較上季增 68%，第二季存貨事實表未涵蓋；過去 12 個月 FCF 利潤率 −5.84%；德州投資增至逾 16 億美元；同業同樣出現營收增速高於毛利增速。","assumption":"營收放量會轉成每股現金。","consequence":"2027 年營收達共識 2.49 兆元，但淨利率降到 4.5%、現金持續流出，股東要承擔舉債與可轉債稀釋。","ruling":"採納。基準路徑 EPS 低於共識，股利假設由 3.1% 下修到 2.5%。","watch":"存貨年增與營收年增的差距、季度 FCF、淨負債。","evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1","ems_utilization_capex_cycle#0","competitive_share_entrants#2","end_markets#4"]},{"view":"價格已反映太多","evidence":"現價是 2027 年共識 8.08 倍，看來低，但週期股在獲利高點本來就低本益比；賣方目標價多在大跌前發布。","assumption":"8 倍代表市場已過度悲觀。","consequence":"若 2027 年就是獲利高點，8 倍只是正常的高點倍數，後面還有下跌空間。","ruling":"部分採納。現價沒有反映過多樂觀，但便宜的論證要等分母確認。","watch":"2027 年共識 EPS、單季毛利率。","fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 2275.0 → 本次 1555.0（-31.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=2275.0","side_b":"本次 price_at_dd=1555.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 2,275 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 2,275 元：Bull 價 5,520、Bear 價 1,125，五年期望值 +35.9%，基準年化 6.1%，不對稱比 2.4","side_b":"本次情境、股價仍用 2,275 元：Bull 價 5,330、Bear 價 960，五年期望值 +16.0%，基準年化 3.9%，不對稱比 1.33","ruling":"先換情境、股價不動：五年期望值少 19.9 個百分點，基準年化少 2.2 個百分點。不對稱比由 2.4 變為 1.33。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 2,275 元：五年期望值 +16.0%，基準年化 3.9%，不對稱比 1.33","side_b":"本次情境、股價 1,555 元：五年期望值 +69.7%，基準年化 12.1%，不對稱比 3.63","ruling":"再換股價、情境不動：起點價下跌 31.6%，五年期望值多 53.7 個百分點，基準年化多 8.2 個百分點，不對稱比由 1.33 升到 3.63。合計五年期望值比前份多 33.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論、情境機率與最大回撤","cause":"方法變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 2,275 元，估值中性，裁決觀望，牛熊機率 25% 與 30%，最大回撤 −60%。","side_b":"現價 1,555 元，估值結論仍為中性，便宜的論證因分母爭議暫不成立；牛熊機率 20% 與 35%，最大回撤 −60% 到 −48%。","ruling":"牛熊機率與最大回撤的變動來自本次重建情境，股價本身對報酬的影響已在前面的拆解列明。機率往熊市移 5 個百分點，是重建情境時的判斷，原因是共識成長超過內生上界，跌因也查不到。最大回撤區間來自新的熊市路徑：2029 年 EPS 95 元乘 6.5 到 8.5 倍得 618 到 808 元，再對現價換算。估值結論前後都是中性，沒有變動。第三季財報未到，維持等待。","evidence_level":"中","settle_metric":"第三季財報與財報後的 2027 年共識 EPS","if_then":["若 2027 年共識 EPS 低於 173 元：不追","若 2027 年共識 EPS 不低於 173 元且毛利率不低於 8%：重做判斷後分批反買"]},{"axis":"基本面判斷複核","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份綜合評等 B，價值陷阱風險中等，護城河持平，五年後跑道中等，類型為 EMS/ODM，循環位置為晚循環。","side_b":"本次六項判斷都不變。","ruling":"新證據有 AMD Helios 份額、第二季毛利率回升、德州投資擴大與融資案，方向互相抵銷，不足以改變判斷。循環位置仍為晚循環：存貨堆高與資本支出增速將放緩偏賣方，股價急跌偏買方，訂單能見度事實表未涵蓋。","evidence_level":"中","settle_metric":"五大雲端 2028 年資本支出指引、AWS 相關份額","if_then":["若 AWS 相關份額跌破 60%：停止加碼並下修護城河方向","若 2028 年資本支出指引年增低於 5%：減碼"]},{"axis":"重新進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","side_b":"第三季財報後 2027 共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍","ruling":"舊的進場條件已觸發：11-06 收盤 1,555 元，2027 年共識 192.37 元。但共識最近修正為 0.0%，第二個條件可能只是資料尚未更新，所以觸發後重做判斷，不直接進場。新門檻把第三季財報放進條件，EPS 下限由 192.37 元下修 10% 得 173 元，10 倍錨不變。","evidence_level":"中","settle_metric":"第三季財報後的 2027 年共識 EPS 與單季毛利率","if_then":["若三項條件同時成立：重做判斷後分批反買，首筆 2%","若股價漲回 1,800 元以上而財報證據未到：不追"]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未載明唯一致命點（null）。","side_b":"AWS 下一代 Trainium 機櫃專案把主力份額移給其他 ODM，緯穎相關份額由約七成跌破五成。","ruling":"前份無可比原文，本次以敏感度最大的單一事件為準，發生即清倉。","evidence_level":"低","settle_metric":"AWS 相關份額估計、年報客戶占比","if_then":["若 AWS 相關份額跌破 50%：清倉"]},{"axis":"清倉與減碼監測指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未載明監測門檻（null）。","side_b":"2027 年共識 EPS 低於 173 元；單季毛利率連 2 季低於 8%；存貨年增率連 2 季高於營收年增率 20 個百分點；FCF 利潤率低於 −8%；AWS 相關份額跌破 60%。","ruling":"前份無可比原文，本次首次寫明門檻與來源，對應減碼或清倉動作。","evidence_level":"中","settle_metric":"各項監測指標的最新季度值","if_then":["若存貨門檻觸發：減碼一半"]},{"axis":"每股數字口徑","cause":"方法變動","prior_field":null,"side_a":"事實表歷年 EPS 265.54 元與第二季 EPS 80.43 元是拆股前口徑。","side_b":"現價 1,555 元、股數 579.63 百萬股與共識 EPS 132.11 元是拆股後口徑。","ruling":"情境與共識基期一律用拆股後口徑，FY2025 基期以淨利除以現行股數得 88.19 元。若用 265.54 元當基期，三年成長率會被算成負值。拆股比例由股數推得，事實表未直接揭露；高盛 3,777 元目標價也符合拆股後水準。","evidence_level":"中","settle_metric":"公司股本變更公告與調整後歷史 EPS","if_then":["若公告的實際比例與約 3 倍相差超過 5%：重算基期與每股路徑"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：2027 年共識 8.08 倍、RSI 25.67、前份進場條件已成立，股價仍在 104 週均線之上，財報若優於預期可能快速反彈，等待的代價是少賺。","side_b":"等財報：跌因不明，共識沒有更新，2026 年下半年淨利要比上半年高約六成才達共識，第二季毛利率又含 NRE。","ruling":"等財報。依前兩季 5/7、8/7 的節奏，第三季財報應在 11 月上中旬公布，確切日期事實表未涵蓋；等待期短，買錯的代價是 −48% 到 −60%。性質屬可調和，由財報數字裁定。","evidence_level":"中","settle_metric":"第三季毛利率與財報後的 2027 年共識 EPS","if_then":["若財報後 2027 年共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍：重做判斷後分批反買，首筆 2%","若股價先漲回 1,800 元以上而財報證據未到：不追","若 2027 年共識 EPS 低於 173 元或毛利率低於 8%：不追","若股價續跌但共識與毛利率沒有惡化：分批反買"]}],"triggers":[{"n":1,"text":"第三季財報後重新評估進場","type":"估值rearm","maps_to":"H1","metric":"2027 年共識 EPS、單季毛利率、股價對該 EPS 的倍數","threshold":"EPS 不低於 173 元、毛利率不低於 8%、股價不高於 10 倍","action":"重做完整判斷，通過才分批反買，首筆 2%","source_freq":"每季財報與共識快照","date":"2026-11"},{"n":2,"text":"毛利率跌破代採購後的合理水準","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"連 2 季低於 8%","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#4","competitive_share_entrants#2"]},{"n":3,"text":"AWS 次世代專案主力份額轉移","type":"Single Thing","maps_to":"Single Thing","metric":"AWS 相關份額","threshold":"跌破 50%","action":"清倉","source_freq":"賣方報告與年報，不定期","date":null,"evidence_refs":["customer_second_source#3"]},{"n":4,"text":"存貨增速持續超過營收增速","type":"風險","maps_to":"R4","metric":"存貨年增率減營收年增率","threshold":"連 2 季高於 20 個百分點","action":"減碼一半","source_freq":"每季資產負債表","date":null,"evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]},{"n":5,"text":"擴產舉債超過可承受範圍","type":"風險","maps_to":"R4","metric":"淨負債","threshold":"超過 1,500 億元","action":"停止加碼","source_freq":"每季資產負債表","date":null,"evidence_refs":["ems_utilization_capex_cycle#0"]},{"n":6,"text":"雲端資本支出進入放緩","type":"風險","maps_to":"R2","metric":"五大雲端 2028 年資本支出指引年增率","threshold":"低於 5%","action":"減碼","source_freq":"每季雲端業者財報","date":"2027-02","evidence_refs":["supply_demand_durability#5"]},{"n":7,"text":"關稅或產地轉移成本無法轉嫁","type":"風險","maps_to":"R5","metric":"單季毛利率年減幅度","threshold":"管理層歸因關稅或產地轉移，且年減 100 個基點以上","action":"減碼","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"n":8,"text":"單一客戶依賴升高且份額下滑","type":"風險","maps_to":"R1","metric":"年報最大客戶占比、AWS 相關份額","threshold":"最大客戶占比超過 60%，且 AWS 相關份額跌破 60%","action":"停止加碼","source_freq":"每年年報、賣方報告","date":"2027-03","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"n":9,"text":"第三季財報後複審","type":"複審日期","maps_to":"H1","metric":"第三季財報是否公布","threshold":"公布後 5 個交易日內","action":"重做完整判斷","source_freq":"一次性","date":"2026-11-30"}],"kill_metrics":[{"metric":"2027 年共識 EPS","bear_threshold":"低於 173 元（較 192.37 元下修超過 10%）","window":"第三季財報後 30 天內","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連 2 季低於 8%","window":"未來 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"存貨年增率減營收年增率","bear_threshold":"連 2 季高於 20 個百分點","window":"未來 4 季","source":"公司資產負債表與季報","last_status":"unknown"},{"metric":"過去 12 個月 FCF 利潤率","bear_threshold":"低於 −8%","window":"未來 4 季","source":"公司現金流量表","last_status":"warning"},{"metric":"AWS 相關份額","bear_threshold":"跌破 60%，跌破 50% 即清倉","window":"未來 8 季","source":"賣方份額估計、年報客戶占比","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.answers.scenario_inputs.yield_pct.dividend","reason":"閘認為五年期望值 +69.7% 與基準年化 12.1% 依賴股利口徑，這是誤讀，兩個數字都只算股價。機率加權終值（20%×5,330＋45%×2,750＋35%×960）為 2,639.5 元，除以現價 1,555 元得 +69.7%；基準終值 2,750 元對現價五年複利為 12.1%；股價 2,275 元時的 +16.0% 與 3.9% 也能用同一算式重現。股利用 2.5% 或 3.113%，這兩個數字都不變。3.113% 與過去 12 個月殖利率 3.11% 相同，屬已實現數字；2.5% 是未來五年的假設，下修已寫在基準情境與第三個盲點的裁決，原因是自由現金流為負、配息靠融資。兩個數字時點不同，所以保留 2.5%，不改成過去的殖利率。"}],"action_conditions":{"rearm_trigger":"第三季財報後 2027 共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍","exec_line":"條件成立後先重做完整判斷，不直接建倉；通過後分兩批反買，首筆 2%，第二筆等下一季毛利率確認。","holding_cap":"驗證完成前總倉位不超過 3%"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等第三季財報公布，確認 2027 年共識 EPS 不低於 173 元、單季毛利率不低於 8%，且股價不高於該 EPS 的 10 倍。"},"thesis":{"H":[{"id":"H1","text":"緯穎守住 AWS ASIC 主力供應地位，2027 年 EPS 達 175 元以上。","2y":"2027 年 EPS 不低於 175 元","5y":null,"10y":null,"threshold":"2027 年 EPS 不低於 175 元，AWS 相關份額不低於 60%","source":"公司季報、月營收、賣方份額估計","drift_rule":"過去 12 個月 EPS 較路徑偏離連 2 季達 5% 為削弱，連 3 季達 10% 為反轉"},{"id":"H2","text":"代採購模式下毛利率站穩 8% 以上，NRE 消退後仍不跌破。","2y":"2027 年全年毛利率不低於 8%","5y":null,"10y":null,"threshold":"單季毛利率不低於 8%，營益率不低於 6%","source":"公司季報新聞稿","drift_rule":"過去 12 個月毛利率較門檻偏離連 2 季達 5% 為削弱，連 3 季達 10% 為反轉"},{"id":"H3","text":"擴產高峰過後自由現金流轉正，五年累計現金轉換率回到合理水準。","2y":null,"5y":"FY2027 到 FY2031 累計 FCF 對淨利比不低於 0.6","10y":null,"threshold":"FY2028 FCF 轉正，五年累計 FCF 對淨利比不低於 0.6","source":"年度現金流量表","drift_rule":"過去 12 個月 FCF 利潤率較路徑偏離連 4 季達 5% 為削弱，連 6 季達 10% 為反轉"}],"R":[{"id":"R1","text":"客戶高度集中：2026 年實際占比未揭露，2024 年舊資料顯示前兩大客戶合計 86%，目前以 AWS 為最大客戶。","h_ref":"H1","clock":"🔥","threshold":"AWS 相關份額跌破 60%，或年報最大客戶占比超過 60%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"id":"R2","text":"雲端資本支出部分靠舉債支撐，融資轉緊時 ODM 訂單會先受影響。","h_ref":"H1","clock":"🔥","threshold":"五大雲端 2028 年資本支出指引年增低於 5%","evidence_refs":["supply_demand_durability#5"]},{"id":"R3","text":"GPU 產品組合與零組件轉嫁壓低毛利率，NRE 消退後毛利率回落。","h_ref":"H2","clock":"⚡","threshold":"單季毛利率連 2 季低於 8%","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"id":"R4","text":"存貨與資本支出吃掉現金，需求轉弱時負債壓力和存貨跌價會同時發生。","h_ref":"H3","clock":"🔥","threshold":"存貨年增率連 2 季高於營收年增率 20 個百分點，或淨負債超過 1,500 億元","evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1","ems_utilization_capex_cycle#0"]},{"id":"R5","text":"墨西哥占產能 70%，關稅或客戶要求移轉產地會增加成本。","h_ref":"H2","clock":"🔥","threshold":"管理層歸因關稅或產地轉移，且單季毛利率年減 100 個基點以上","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]}],"single_thing":{"description":"AWS 下一代 Trainium 機櫃專案把主力份額移給其他 ODM，緯穎相關份額由約七成跌破五成。","why_fatal":"每 1 個百分點淨利率約等於 2027 年 EPS 43 元，占共識 22%；凱基預期 ASIC 毛利率高於公司平均，失單會同時打擊營收與產品組合。2026 年 AWS 營收占比事實表未涵蓋，敏感度為估算。","if_happens":"未持有就不進場；已持有則清倉，並改用熊市路徑重做判斷。","how_monitor":"每月營收、AWS 次世代平台供應商報導、賣方份額估計、年報客戶占比。","probability":"12 到 24 個月約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.08,"peg_fy2":0.2,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":88.19,"FY2026E":132.11,"FY2027E":192.37,"FY2028E":241.37},"fy_end_month":12,"eps_basis":"新台幣，拆股後每股口徑。FY2025A 88.19 元＝淨利 511.18 億元÷現行股數 579.63 百萬股，事實表歷年 EPS 265.54 元為拆股前；拆股比例由股數推得，事實表未直接揭露。共識為 Koyfin 美元值依快照日匯率換算。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報，依前兩季節奏應在 11 月上中旬公布，確切日期事實表未涵蓋","impact":"高","watch":"毛利率是否守住 8%、代採購與 NRE 的影響、下半年營收跳升幅度"},{"date":"2027-02","date_precision":"month","type":"macro","event":"大型雲端業者公布第四季財報與資本支出指引，時間為預估","impact":"高","watch":"五大雲端資本支出指引與融資方式"},{"date":"2027-03","date_precision":"month","type":"other","event":"2026 年年報揭露客戶集中度，時間為預估","impact":"中","watch":"最大客戶占比與 AWS 相關份額"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-8.22, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
