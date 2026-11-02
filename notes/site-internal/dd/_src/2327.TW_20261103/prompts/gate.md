你是 DD 管線 v20 的判斷層閘（gate），標的 2327.TW（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝495.32 億元 TWD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：國巨法說報導 https://uanalyze.com.tw/articles/1516757975（IR 新聞稿未取得）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無 Q3 共識
- `f_kpi1`（q1_business）｜毛利率＝41.0 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/1516757975（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝146.03 億元 TWD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/1516757975（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益率＝29.5 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/1516757975（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無
- `f_kpi4_eps`（q1_business）｜稅後純益（歸屬母公司）／EPS＝5.83 元 TWD／股（純益 119.81 億元）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/1516757975（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無
- `f_kpi5_q4_2026`（q1_business）｜管理層下一季指引（Q4 2026）＝營收、毛利率、營業利益率皆較 Q3「微幅成長」（無數字區間） qualitative｜期間與口徑：Q3 2026 法說（2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：https://uanalyze.com.tw/articles/8967257977（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026 法說（2026-10-29））
  - 註記：查無
- `f_kpi6_book_to_bill`（q1_business）｜訂單出貨比（book-to-bill）＝接近 2（鉭質電容、MLCC 等 AI 相關產品更高，無精確數字） 倍｜期間與口徑：Q3 2026（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/8967257977（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（公告於 2026-10-29））
  - 註記：不適用
- `f_kpi7`（q1_business）｜產能利用率＝特殊品與標準品皆接近 95% %｜期間與口徑：Q3 2026（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：https://uanalyze.com.tw/articles/8967257977（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（公告於 2026-10-29））
  - 註記：不適用
- `f_peer_2327_tw_gross_margin_pct`（q2_moat）｜2327.TW 毛利率＝37.61 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2327.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2327_tw_operating_margin_pct`（q2_moat）｜2327.TW 營業利益率＝24.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2327.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2327_tw_fcf_margin_pct`（q2_moat）｜2327.TW FCF 利潤率＝18.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2327.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6981_t_gross_margin_pct`（q2_moat）｜6981.T 毛利率＝42.32 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6981.T.gross_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_6981_t_operating_margin_pct`（q2_moat）｜6981.T 營業利益率＝15.39 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6981.T.operating_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_6981_t_fcf_margin_pct`（q2_moat）｜6981.T FCF 利潤率＝9.45 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6981.T.fcf_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_6762_t_operating_margin_pct`（q2_moat）｜6762.T 營業利益率＝11.15 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6762.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_009150_ks_operating_margin_pct`（q2_moat）｜009150.KS 營業利益率＝9.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.009150.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2492_tw_operating_margin_pct`（q2_moat）｜2492.TW 營業利益率＝7.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2492.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝46858.83 TWD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 247410.95、現金 200552.12（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.19 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝31.92 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝46.9 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝184179.38 TWD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝248773.08 TWD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝5.76 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 19.09 → 20.19（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2058.46 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.203 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝498.5 TWD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝33.57 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.77 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.07 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.86 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 20.19，分子＝快照價 502.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.83 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 502.0 / W52 457.62 / W104 296.09 / W250 184.16 / W250 13週斜率 3.98%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝457.62 TWD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝296.09 TWD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_rsi14`（q5_valuation）｜RSI(14)＝39.07｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝59.5 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：摩根士丹利法說前報告：日韓 MLCC 供應商可能將產能轉向高階產品，並列同業競爭為風險；下修國巨 EPS 預估、目標價 1515 元調為 1465 元
  - 來源：工商時報 wantrich（as_of 2026-07-23）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：大摩悲觀情境（目標價685元）假設非AI需求自2026下半年大幅下滑且併購效益不如預期；法說前關注非AI需求能見度（搜尋摘要轉述，未取得逐字原文）
  - 來源：技術新報/經濟日報等外資報導彙整（as_of 2026-07-28）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：高盛、花旗於國巨7月法說後同步調降目標價：高盛1490→1280元、花旗1500→1450元，皆維持買進；報導稱主因產業本益比壓縮而非國巨獲利轉弱。
  - 來源：聯合新聞網〈國巨目標價 兩外資調降〉（as_of 2026-07-30）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：摩根士丹利於法說前將國巨目標價由1515元降至1465元，評等維持買進；以2028年EPS與31倍本益比推算，樂觀情境2075元、悲觀情境685元。
  - 來源：自由財經〈外資第1槍!國巨高點腰斬 大摩目標價降至1465元〉（as_of 2026-07-27）｜affects：valuation
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：村田2026-10-30宣布2026至2030財年約1兆日圓MLCC投資，FY2027–2028產能年增約20%，岡山新廠2027年4月動工、2028年底完工
  - 來源：EE Times Japan 村田製、MLCCに1兆円投資（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：傳京瓷計劃將日本MLCC產能擴增至3倍（報導，未證實）
  - 來源：TechNews 京瓷傳計劃將日本MLCC工廠產能擴增至3倍（as_of 2026-07-13）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2019 Q1 國巨毛利率 44.8%，年減 6.6 個百分點、季減 14.3 個百分點，大中華區需求疲弱
  - 來源：technews 國巨 Q1 獲利寫近 6 季新低（as_of 2019-04-25）｜affects：moat_trend、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2019 Q3 稅後淨利季增44%、年減85.9%，前三季 EPS 14.26 元，庫存回復正常
  - 來源：technews 國巨 Q3 獲利季增 44%（as_of 2019-11-08）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023 Q3 法說：Q4 2023 與 Q1 2024 為此波景氣循環谷底；2023 全年毛利率 33.5%
  - 來源：富果研究 國巨 2023-10-26 法說會（as_of 2023-10-26）｜affects：decision_inputs.bear、triggers
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023 全年毛利率 33.5%，年減 4.5 個百分點
  - 來源：富果研究 國巨 2024-02-29 法說會（as_of 2024-02-29）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1144.0,"bear_5y_price":204.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":5.7,"ev5y_pct":17.2,"irr_base_pct":1.1,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.19,"pe":24.69,"basis":"FY2026E 共識 EPS 20.19 元（Koyfin，新台幣）÷判斷日股價 498.5 元；終端倍數同樣套在當年度 EPS 上"},"eps":{"bull":[32.0,40.0,43.0,47.0,52.0],"base":[28.5,29.5,24.0,27.5,31.0],"bear":[23.0,19.0,13.0,15.0,17.0]},"pe":{"bull":22,"base":17,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.203,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2327.TW_Q2_2024_Earnings_Call_20240730.md
- 2024-07-30｜CEO Deng-Rue Wang｜guidance：CEO 給 Q3 營收低個位數成長，理由為 AI/運算/通訊/消費動能與通路庫存健康。（原話："we will guide the low single-digit growth."）
- 2024-07-30｜CEO Deng-Rue Wang｜guidance：CEO 表示不預期 V 型反彈，需求為溫和回補。（原話："we don't see that there will be a V"）
- 2024-07-30｜CFO Eddie Chen｜margin：Q2 毛利率 35.1%，較上季高 1.3 個百分點，為兩年來首度回到 35%。（原話："The gross margin also improved to 35.1% or TWD 11 billion."）
- 2024-07-30｜CFO Eddie Chen｜margin：Q2 營收 314 億台幣，季增 10.2%，優於前次財測，主因 AI 相關動能與部分消費性產品。（原話："the company has reported TWD 31.4 billion sales"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：Q3 毛利率財測：價格穩定、稼動率微升、持續成本改善（原文為 below single-digit，實為低個位數改善之意）。（原話："we see the utilization in quarter 3 was slightly improved."）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：CEO 給出稼動率：Q3 premium 產品由 70% 升至 75%。（原話："from quarter 2, 70% to next"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：分析師確認稼動率提高降低單位成本，CEO 回答正確；並說明提高 commodity 稼動率是為補自家庫存。（原話："So that's why we want to increase the utilization"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：OpEx 口徑：僅配銷成本隨營收變動，約占 2%~3%，其餘為相對固定成本，故不給 OpEx 比率目標。（原話："Around 2% to 3%. This is the distribution cost."）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 稱 OpEx 預期隨收購相關交易成本消退而逐步改善，但無長期目標。（原話："But I don't have a long-term targets per se for that matter."）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 拆解 Q2 OpEx：金額 45 億，占營收 14.5%（Q1 為 16.4%）。（原話："So TWD 4.5 billion spending OpEx dollars"）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 拆解非本業：Q1 含日本投資處分的資本利得，剔除後季對季相近。（原話："divestitures of our investments in Japan"）
- 2024-07-30｜CFO Eddie Chen｜product：產品別：MLCC、感測器季對季動能放緩，鉭質電容升溫。（原話："So we've seen tantalum is picking up the momentum."）
- 2024-07-30｜CEO Deng-Rue Wang｜product：鉭質電容訂單：book-to-bill 為正、接單穩定、積壓訂單小幅增加，與去年多數時間不同。（原話："Booking is stable and backlog is slightly building."）
- 2024-07-30｜CEO Deng-Rue Wang｜product：鉭質電容最大宗為筆電，另含 SSD、伺服器與 EV。（原話："Largest portion was notebook."）
- 2024-07-30｜CFO Eddie Chen｜customer：區域別：歐洲占比季減 3%，美中升溫。（原話："Europe is probably suffering more than the rest"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：終端排序：消費、筆電、手機、SSD、伺服器強；工業（尤其歐洲）偏弱，Q3 趨勢相同。（原話："We probably rank Q3 in a similar way as year-to-date."）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：工業需求：下半年大致與上半年相同，期待明年需求轉強。（原話："we'll probably look at next year for the stock to digest"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：管理層不追蹤 AI 營收，不提供 AI 占比。（原話："We do not track revenue linked to AI"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：Q2 優於預期來自整體需求，非未預期的單一新專案。（原話："nothing unexpected in terms of a particular design that we"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：通路庫存下降趨勢已穩定逾一年，Q3 預期延續；EMS/直接客戶庫存能見度較低。（原話："where we have less visibility."）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：Q2 book-to-bill 約 1 或略高，部分來自通路補庫，Q3 預期同趨勢。（原話："The ratio was positive in Q2, around one or slightly better"）
- 2024-07-30｜Deng-Rue Wang（逐字稿標註）｜competition：車用相對同業跌幅較小，歸因於 KEMET 帶來的車廠關係與設計導入，稱在特定技術上取得份額。（原話："we were gaining share for sure in certain technologies"）
- 2024-07-30｜CEO Deng-Rue Wang｜competition：MLCC 與各終端未偵測到顯著價格變動；電感未跟隨日系同業漲價。（原話："We haven't really detected any significant price change"）
- 2024-07-30｜CEO Deng-Rue Wang｜competition：電感成本：該領域未遭受大幅成本衝擊。（原話："We haven't really suffered a large cost impact"）
- 2024-07-30｜CFO Eddie Chen｜competition：電源 IC 佈局仍在早期，自稱未與大廠並列。（原話："I would say this is still very initial stage, right?"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：CapEx 約占 EBITDA 15%~20%，以維持性為主，不積極擴產。（原話："still spending about a 15%, 20% of our EBITDA"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：廣州新廠第一期持續爬坡，為市場回溫預先備產能。（原話："So that Phase 1 expansion is still on that."）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：持有 UPI 約 20%，視為投資策略延伸，以權益法認列於非本業。（原話："So right now, we're having about 20% in UPI."）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：資產負債表：現金 920 億，淨負債/權益 16.7%，仍高於收購 Telemecanique 前的 11.2%。（原話："The net debt to equity"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：庫存週轉天數降至約 120 天，為過去 5~6 季最低；預期庫存動態無大變化。（原話："So right now, we're saying about 120 days."）
- 2024-07-30｜CFO Eddie Chen｜risk：關稅影響難預測，需保持彈性。（原話："it's hard to predict, honestly."）
- 2024-07-30｜CEO Deng-Rue Wang｜risk：地緣政治：客戶討論供應韌性，部分客戶要求特定原產地，電信/5G 客戶最在意。（原話："Some customers are being more forward in requesting specific"）
- 2024-07-30｜CEO Deng-Rue Wang｜risk：成本轉嫁政策：過去曾在無法吸收成本時向客戶反映，目前不在該情況。（原話："But we are not in that"）
- 2024-07-30｜CEO Deng-Rue Wang｜commitment：CEO 表示稼動率是否達 90% 取決於終端需求與庫存，不給前瞻預測，僅承諾需求改善時逐步拉升。（原話："I cannot give you an outlook"）
- 2024-07-30｜CEO Deng-Rue Wang｜commitment：CEO 結語：認為景氣已落底、逐步復甦，正向動能延伸至下一季。（原話："still see this positive momentum extended into next quarter"）

### 問答異常語氣（迴避／改口／保留）
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：AI 占營收是否約個位數中段百分比？｜答法：未回答占比，改稱不追蹤 AI 營收並指出消費/個人電腦亦貢獻。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：OpEx 比率是否有可追蹤的新目標（如 13%~13.5%）？｜答法：拒絕給數字目標，改談逐步改善與變動成本結構。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：稼動率何時可達 90% 以上？｜答法：不給前瞻預測，僅稱取決於終端需求與庫存。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：是否有庫存跌價回沖的機會？｜答法：CFO 先稱不知如何重述問題，未直接回答是否有沖銷回沖，改談投資組合與庫存週轉。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：高稼動率 vs 低個位數營收財測，混合 ASP 是否下降？｜答法：未回答 ASP，改談自身庫存重建與可供應量。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 1 | 4 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 4 | 4 |
| substitute_technology | found | 2 | 3 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 5 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：國巨* 大客戶 第二供應商 OR 轉單 2026；國巨* 客戶 自製 OR 分散供應商；2327.TW 國巨 Yageo largest customer second source OR in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260526","verdict":"B 觀望（thesis 完整：產業 🟢 + A 級護城河 8.5 + AI 🟢；但 4W +110.7% 動能極端過熱、短中期 R:R 失效（雙負）、Pure MA ✅ 但 BB 上軌 +18.6% stretched；等回測 BB 中軌 NT$328 或 W52 NT$235 + Q3 26 AI 占比 ≥ 16% 三條件後試倉 3-5% 衛星）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI server MLCC 滲透率上升 → AI 占營收比結構性擴大","columns":{"2Y 驗證點":"2026 Q4 AI 占比達 18%+；2027 達 22%+","5Y 驗證點":"2030 AI 占比達 30%+，AI 業務 GM ≥ 45%","10Y 驗證點":"2035 後 AI MLCC 成為主流業務","具體數字門檻":"Q2 2026 法說 AI 占 ≥ 16%；FY26 末 ≥ 20%","信息來源":"Yageo Q1 26 法說、TrendForce","漂移觸發":"連 2 季 AI 占比未達門檻 → 削弱"}},{"id":"H2","text":"MLCC pricing 漲價週期持續 + Yageo 無新擴產 → margin 擴張","columns":{"2Y 驗證點":"2026 全年 GM ≥ 38%（vs FY25 36.2%）；OM ≥ 26%","5Y 驗證點":"2027-28 cycle 平穩期 GM 維持 35-38%；OM 24-27%","10Y 驗證點":"2030+ cycle peak 後 normalize GM 32-35%","具體數字門檻":"2026 H2 spot pricing 環比 +5%+；GM YoY 持續擴張","信息來源":"TrendForce、Digitimes、Yageo 法說","漂移觸發":"連 2 季 GM YoY 下滑 &gt; 1.5pp → 反轉"}},{"id":"H3","text":"Shibaura 整合 + 多元化降低 cycle 波動","columns":{"2Y 驗證點":"2026 H2 Shibaura full integration；2027 感測器業務貢獻 EPS ≥ 5%","5Y 驗證點":"2028-30 多元化業務（感測器 + EMC + 工業）占比達 30%+","10Y 驗證點":"2031+ 國巨成為 「multi-component diversified passives leader」","具體數字門檻":"FY26 感測器業務 Revenue ≥ NT$8B；2027 occupy ≥ 8% Rev","信息來源":"Yageo FY25 年報、Schaffner / Shibaura 整合進度","漂移觸發":"2027 H1 仍未產生 synergy → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"4 週 +111% 動能 mean reversion + 股價短期 -30 至 -50%","columns":{"對應假設":"H2 / 估值","時間尺度":"⚡ 短期（1-2 月）","監測指標":"股價 vs BB 中軌 / 漲跌幅","警戒閾值":"5/27 起 5-10 日內回檔 &gt; -15% → 動能消化開始；&gt; -30% → 短期支撐測試"}},{"id":"R2","text":"Murata Izumo 全速量產 → 供給轉鬆 → 漲價週期反轉","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Murata 月度產能利用率 / spot pricing","警戒閾值":"2026 Q4 spot price 環比 &gt; -10% → 削弱；2027 H1 連 2 季 -10%+ → 反轉"}},{"id":"R3","text":"AI hyperscaler capex 結構性下修 + AI server 出貨放緩","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年）","監測指標":"Microsoft / Amazon / Google capex guidance / NVDA DC Rev","警戒閾值":"2027-28 top 4 hyperscaler capex YoY 連 3 季 &lt; +10% → 警戒；&lt; 0% → 結構反轉（≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"加深","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":668,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2327.TW","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"國巨"},"oneliner":"國巨 AI 占比升到 2 成、毛利率 41% 創近年新高，但盈餘高點來自漲價與稼動率近 95%；2028 年日系擴產放量前，現價在基準路徑下 5 年價格報酬接近零，等 380 元以下且 2027 年中訂單仍強再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/scenario.json","answers":{"q1_business":{"verdict":"國巨賺的是全球電子廠與通路的被動元件錢，錢卡在高階電容（MLCC、鉭質）與缺貨期的定價：2026Q3 營收 495.32 億元、毛利率 41%、營益率 29.5%，這個獲利水準有相當部分來自漲價與稼動率近 95%。","reasoning":"獲利：2026Q3 營收 495.32 億元、營業利益 146.03 億元、歸母純益 119.81 億元、EPS 5.83 元。Q4 指引營收、毛利率、營益率較 Q3「微幅成長」，沒有數字區間。結構：2026Q1 約 75% 營收來自 AI、車用、工規、醫療與國防航太，高階電容占比由 17% 升至 45%，大中華區客戶降到 25% 以下（董事長 2026-04-30）。2026Q3 AI 占比約 2 成。年報未列占營收 10% 以上的單一客戶，通路約占四成（2024-10-29 逐字稿）。產品別營收拆分事實表未涵蓋。產業時鐘判第 III 階段：特殊品與標準品稼動率都近 95%、訂單出貨比接近 2、2026-07 起 MLCC 與鉭質、鋁質電容全面漲價 15–25%、村田等同業宣布大規模擴產，屬於供給緊、價格漲、資本支出開始追的階段。供需持久度判週期性將反轉：TrendForce 預期高階短缺延續到 2027 上半年，之後村田 FY2027–28 產能年增約 20%、國巨自身擴產 10–15% 陸續開出。單點依賴：沒有集中客戶；鉭質電容在中國、泰國、墨西哥三地生產（2024-10-29 逐字稿），也沒有單一廠區依賴。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_gaap","f_kpi3_gaap","f_kpi4_eps","f_kpi5_q4_2026","f_kpi6_book_to_bill","f_kpi7"],"verdict_values":{"revenue_quality":"高：沒有單一客戶占營收 10% 以上，約 75% 營收在高門檻應用；但 2026 年的毛利率含漲價週期成分，不能全當常態","unit_econ_note":"稼動率已近 95%（2024Q3 標準品 65%、特殊品 75%），量的增量只能靠 2027 年擴產 10–15%；毛利率每 1pp 約每股 0.9 元（以 2027 年營收約 2,300 億元、稅率約 21% 估）","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"全產品線被動元件平台，靠併購轉向高階；盈餘隨漲價與稼動率擺動，轉型降低但沒有消除循環性"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：高階短缺預期延續到 2027 上半年（TrendForce 2026-06-17），村田 2026-10-30 宣布 FY2027–28 產能年增約 20%，國巨 2026-10-29 宣布 2027 年擴產 10–15%","bargaining":{"up":"貴金屬（銀、釕、鈀）上漲可以轉嫁：2026-01 磁珠漲約一成、2026-02 晶片電阻漲 15–20%","down":"客戶分散、約四成走通路；缺貨期 AI 與記憶體客戶以長約溢價鎖料，供過於求時話語權回到客戶","geo":"墨西哥、亞洲、歐洲多地生產，美國有普思、基美據點，董事長預期關稅影響輕微"},"profit_pool_dir":"短期往元件廠移動（漲價、長約溢價），2028 年前後新產能開出後可能回流客戶","tam_table":{"expanded":false,"reason":"被動元件是成熟品類，AI 帶動的是單機用量而非新品類；事實表未涵蓋 TAM、滲透率與利潤池占比數字，無法展開"}}}},"q2_moat":{"verdict":"護城河穩定（→）、B 級：產品線最廣，加上多地產能與通路，營益率領先所有同業；但定價力只在缺貨期明顯，村田與日韓廠擴產正打進國巨轉型的同一塊高階市場。","reasoning":"機制：產品線最廣（電阻、鉭質電容全球第一，MLCC、電感前三，見 2024-10-29 逐字稿主持分析師介紹），加上墨西哥、亞洲、歐洲多地產能與約四成通路銷售，車用、工規、國防醫療料號有認證黏著。可證方向：TTM 營益率 24.8%，高於村田 15.39%、TDK 11.15%、三星電機 9.8%、華新科 7.64%；自由現金流利潤率 18.86%，約為村田 9.45% 的兩倍（村田期間至 2026-03，各家期間不同）。不過毛利率 37.61% 低於村田 42.32%，研發密度 2.32% 對村田 8.68%：高階技術領先在村田，國巨贏在成本結構、產品組合與通路。ROIC 同業價差事實表未涵蓋，只有單期營益率價差，看不出擴大或收窄。執行力穩定：轉型已完成，約 75% 營收在高門檻應用、大中華區客戶 <25%。定價力擴大但屬缺貨期現象：2024-07-30 CEO 說 MLCC 沒有價格變動、電感沒跟日系漲價，2026 年才改為主動調漲 15–25%。兩者合併判穩定。評分：執行 8、定價力 7，B 級；定價力沒有跨循環證據（2023 年毛利率只有 33.5%），不給 8 分以上。","fact_refs":["f_peer_2327_tw_gross_margin_pct","f_peer_2327_tw_operating_margin_pct","f_peer_2327_tw_fcf_margin_pct","f_peer_6981_t_gross_margin_pct","f_peer_6981_t_operating_margin_pct","f_peer_6981_t_fcf_margin_pct","f_peer_6762_t_operating_margin_pct","f_peer_009150_ks_operating_margin_pct","f_peer_2492_tw_operating_margin_pct","f_kpi1","f_kpi7","f_net_debt_m"],"verdict_values":{"moat":{"mechanism":"規模與產品線廣度（電阻、鉭質電容全球第一，MLCC、電感前三）＋墨西哥／亞洲／歐洲多地產能＋約四成通路銷售，車用、工規、國防醫療料號有認證黏著","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力穩定：轉型已完成（約 75% 營收在高門檻應用、高階電容占比 45%）；定價力擴大但屬缺貨期現象（2024 年 MLCC 沒有價格變動，2026 年主動漲價 15–25%）；村田一兆日圓擴產與日韓廠轉高階正進入同一市場。合併判穩定，不給擴大","competitor_notes":[{"name":"6981.T 村田","strategy_note":"高階 MLCC 技術領先、研發投入最重；2026-10-30 宣布五年約 1 兆日圓投資，並退出低毛利消費與車規品項，往上集中，與國巨高階化路線正面交會。"},{"name":"009150.KS 三星電機","strategy_note":"高階 MLCC 主要對手，自由現金流利潤率偏薄；大摩點名日韓廠產能轉向高階，屬擴產競爭者。"},{"name":"6762.T TDK","strategy_note":"被動與磁性元件分散經營，電感與感測器和國巨重疊，營益率約國巨一半，價格競爭壓力有限。"},{"name":"2492.TW 華新科","strategy_note":"台系標準品為主，營益率不到國巨三分之一，說明標準品定價力弱，也是國巨若退回標準品組合時的利潤下限參考。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以 TTM 營益率與自由現金流利潤率代替；各家期間不同（村田至 2026-03）","threats":[{"level":"🟡","text":"村田五年約 1 兆日圓 MLCC 投資、FY2027–28 產能年增約 20%，岡山新廠 2028 年底完工；高階 MLCC 供給放大，國巨的漲價空間在 2028 年前後受壓","p":"35%","evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"日韓廠把產能轉向高階產品（大摩 2026-07），京瓷傳日本 MLCC 產能擴 3 倍（未證實）；與國巨高階化路線重疊","p":"30%","evidence_refs":["competitive_share_entrants#0","cyclical_supply_discipline_capacity#3"]},{"level":"🟡","text":"設計端在關鍵電源軌同時驗證 MLCC 與聚合物電容，降低單一技術黏著；國巨自有鉭質聚合物產品線，替代多半發生在自家組合內","p":"15%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"被動元件是每塊電路板的必需料，工程師、採購、付款的品牌或 EMS 都跳不過；AI 伺服器單機用量上升，AI 占比由 2024 年約 5%（2024-10-29 逐字稿分析師引述）升到 2026Q3 約 2 成。風險在時點而非存在：消費級需求可延後，2026-09 消費級 MLCC 報價已轉軟（TrendForce）"},{"item":"決策層級","level":"🟡","text":"以單一料號衡量：車用、工規、國防與醫療料號要重新認證，轉換成本高（約 75% 營收在這些應用）；標準品料號工程師多保留兩家以上供應商或兩種技術（設計端建議關鍵電源軌同時驗證 MLCC 與聚合物電容），替代容易"},{"item":"價值鏈分配","level":"🟡","text":"元件占整機成本低，缺貨時話語權在元件廠（2026-07 起電容漲 15–25%、AI 與記憶體客戶以長約溢價鎖料），供過於求時回到客戶與通路（通路約占四成）；村田、京瓷、日韓廠同步擴產，供給紀律能撐多久是分配的關鍵"},{"item":"社會容忍度","level":"🟢","text":"B2B 料件，終端消費者看不到，沒有政策性價格上限；反壟斷紀錄只有 2008 年台灣與 2019 年中國的結合未申報處分，2021 年鉭質電容卡特爾案國巨不是被處分對象。缺貨期大幅漲價若引來調查屬尾端風險，目前沒有報導"}],"roiic":"增量報酬極高但屬週期、不可外推：FY2024 營業利益約 235 億元→2026Q3 年化約 584 億元（+349 億），同期淨負債約 230 億→468.6 億元（+239 億，主要是芝浦、茂達收購），2026 前九月資本支出只有約 57 億元；增量主要來自漲價與稼動率（65–75%→近 95%），不是新資本","reinvest_rate":"有機再投資率低：自由現金流÷淨利 FY2024 1.25、FY2025 1.04；2024-07-30 CFO 說資本支出約 EBITDA 的 15–20%、以維持為主；2027 年擴產 10–15% 會推高，但規模未定","endo_ceiling":12,"formula_note":"內生成長＝增量 ROIC×再投資率。當期 ROIC 只算得到 2024 年：投入資本≈權益 1,550 億（總資產 3,580 億－負債 2,030 億）＋淨金融負債約 230 億＝約 1,780 億（2024-10-29 逐字稿），FY2024 稅後營業利益≈235 億×(1−21%)≈186 億，ROIC 約 10%；2026 年投入資本事實表未涵蓋。增量 ROIC 被週期價格扭曲，天花板改用實體上界：量≈產能成長 10–15%，取 12%"}}}},"q3_growth":{"verdict":"後五年跑道中等（🟡）：2027 年靠漲價全年化與擴產 10–15% 仍是高成長，2028 年後回到電子用量加 AI 單機用量；共識三年 EPS 年複合約 60%，遠超約 12% 的內生上界，缺口幾乎全靠毛利率擴張，屬週期性。","reasoning":"三年共識 EPS：FY2025A 11.48 元→FY2026E 20.19→FY2027E 31.92→FY2028E 46.9 元（Koyfin；EPS 家數事實表未涵蓋，營收共識 FY1 12 家、FY2 14 家），年複合約 59.8%（(46.9÷11.48)^(1/3)−1）。內生上界約 12%：稼動率已近 95%，量只能跟產能走，2027 年擴產 10–15%；有機再投資率也低。缺口約 48pp，歸因以毛利率擴張為主（2026-07 起電容漲 15–25%、AI 組合），沒有回購，併購只占小部分。但 FY2028E 46.9 元換算淨利約 965 億元（×20.58 億股），約為 2026Q3 年化淨利 479 億元的兩倍，已知產能與已公布的漲價都解釋不了，這段無法歸因、依賴 re-rate，長期信心上限中。跑道：被動元件是成熟品類，成長跟電子用量走，AI 伺服器單機用量是加速器而不是新品類；主動元件 2024-07-30 CFO 自稱仍在很早期，嵌入式基板電感 2028 年才推出，第二條曲線未證實，判中等。衰退信號亮 1 項：共識 2027 年 EPS +58%、營收 +35%，EPS 成長遠高於營收成長。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct","f_kpi6_book_to_bill","f_kpi7"],"verdict_values":{"growth":{"driver_mix":"量（產能 +10–15%，稼動率近 95% 已無再拉空間）＋價（2026-07 起電容漲 15–25%，約占營收一半）＋組合（AI 約 2 成）；芝浦 2025-11 起併表墊高 2026 年增率；沒有回購","runway_years":"5–9","runway_post_y5":"🟡","endo_ceiling_basis":"實體上界：稼動率已近 95%、長期目標 85–90%，量只能跟產能走，2027 年擴產 10–15%；有機再投資率低（自由現金流÷淨利 FY2024 1.25、FY2025 1.04），內生天花板取每年約 12%","segments":{"expanded":false,"reason":"事實表未涵蓋產品別或應用別營收拆分；可得的只有 2026Q1 高門檻應用約 75%、2026Q3 AI 約 2 成兩個總量，已寫入成長判斷"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"2026Q3 毛利率 41%，仍在年增"},{"signal":"核心市占近 12 個月縮減","lit":null,"note":"事實表未涵蓋市占"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"漲價後稼動率仍近 95%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"共識 2027 年 EPS +58%、營收 +35%"},{"signal":"自由現金流÷淨利連 2 年 <0.75","lit":false,"note":"FY2024 1.25、FY2025 1.04"},{"signal":"SBC÷營收 >5% 且上升","lit":false,"note":"稀釋股數三年幾乎不變"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"聚合物電容替代多半在自家組合內"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"2026-07 外資以族群本益比壓縮調降目標價，只有一年"},{"signal":"維持性資本支出占自由現金流 >60%","lit":false,"note":"2026 前九月資本支出約 57 億元"},{"signal":"停止新產能投資且營收 3 年內下滑","lit":false,"note":"2027 年擴產 10–15%"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上：自由現金流約等於淨利、股數三年幾乎不變、股東回報只有現金股利；但成長長期靠併購，2025 年芝浦（競價取得）與茂達（非合意收購）兩筆的報酬尚未實現。","reasoning":"自由現金流÷淨利：FY2022 0.84、FY2023 0.82、FY2024 1.25、FY2025 1.04（年度財報），TTM 自由現金流利潤率 18.86%。稀釋股數 FY2023 約 2,055 百萬股→FY2025 約 2,059 百萬股，目前 2,058.46 百萬股，年稀釋約 0.1%。淨負債 468.6 億元（含租賃），約 FY2025 自由現金流的 1.9 倍。股東回報：TTM 殖利率 1.2%，事實表未見庫藏股。資本支出 2026 前九月約 57 億元，全年高於去年，2027 年未定（2024-07-30 CFO：約 EBITDA 的 15–20%）。現金去向四分（資本支出／併購／股利／償債）的完整數字事實表未涵蓋。併購：KEMET 等舊案帶來毛利率增益（2024-10-29 CFO）；芝浦 87.3%、茂達約 28.5% 是 2025 年交易，報酬還看不到。","fact_refs":["f_peer_2327_tw_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"事實表未涵蓋併購對價與併購後增量獲利。間接證據：2024-10-29 CFO 說收購帶來毛利率增益，淨負債÷權益由 2024Q2 的 16.7% 降到 Q3 的 14.7%，仍高於收購前的 11.2%；2025 年芝浦（競價取得 87.3%）與茂達（非合意取得約 28.5%）報酬未實現，無法判定是否高於資金成本"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見近年庫藏股；FY2023–FY2025 稀釋股數約 2,055→2,059 百萬股，沒有淨回購"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數 FY2023 約 2,055 百萬股（淨利 174.27 億÷EPS 8.48）→FY2025 約 2,059 百萬股（236.34 億÷11.48）→目前 2,058.46 百萬股，年稀釋約 0.1%，低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"2026 年成長主要來自漲價、稼動率與芝浦併表，不是靠持續併購撐；股東回報只有現金股利（殖利率約 1.2%），事實表未見庫藏股"}}}},"q5_valuation":{"verdict":"現價要求 2027–28 年盈餘接近共識、而且倍數不再壓縮才划算；我不信 2028 年共識，基準路徑下 5 年價格報酬接近零，估值偏貴。","reasoning":"現價 498.5 元要的是：2027–28 年 EPS 接近共識 31.92／46.9 元，而且倍數不再壓縮。我大致相信 2027 年（基準 28.5 元，略低於共識），不相信 2028 年（需要淨利約 965 億元）。終端倍數：同業本益比事實表未涵蓋，改以自身為錨。下緣是景氣前約 11.7 倍（前一年平均股價 134.6 元÷FY2025 EPS 11.48 元），上緣是賣方目標價隱含的 31 倍（大摩，2028 年 EPS）至 40 倍；Bull 22、Base 17、Bear 12 倍。短期：2027 年基準 28.5 元×17 倍＝484.5 元（−2.8%）。中期：2028 年 29.5 元×17 倍＝501.5 元（+0.6%）。動能面：週線均線多頭排列、RSI 39、26 週仍 +59.5%，近 3 個月 FY1 共識上修 5.76%，股價比前份低約 25%。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ma_state","f_ma_w52","f_ma_w104","f_rsi14","f_week26_return_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"當年度（FY2026E）本益比為主，循環股另以景氣前倍數與正常化 EPS 檢核；同業本益比事實表未涵蓋","peers":{"expanded":false,"reason":"事實表的同業資料只有毛利率、營益率與自由現金流利潤率，沒有同業本益比或 EV/S，無法做倍數對照"},"fwd_pe":24.86,"peg":0.42,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"①追溯本益比 33.57 倍，在 4 個年度端點中最高（不是連續五年分位，百分位以此近似為 100）；P/S 6.77 倍、EV/S 7.07 倍同樣最高。②景氣前倍數：前一年平均股價約 134.6 元（104 週均線 296.09×2－52 週均線 457.62），對 FY2025 EPS 11.48 元約 11.7 倍；現價對 FY2026E 20.19 元是 24.7 倍，倍數與盈餘同時在高點。③PEG：Fwd 本益比 24.86÷共識三年 EPS 年複合 59.8%≈0.42，但分母是高峰盈餘；改用基準五年 EPS 年複合約 8.9%，PEG 約 2.8。④基準路徑（FY2031E EPS 31 元×17 倍＝527 元）5 年價格報酬約 +6%，加股利年化約 2–3%。綜合判偏貴（🟠）：股價已比前份低 25%，但用正常化盈餘看沒有安全邊際","upside_short_pct":-2.8,"upside_mid_pct":0.6,"denominator_disputed":true,"denominator_note":"分母有爭議：2026–28 年 EPS 含漲價與稼動率近 95% 的週期成分。2026Q3 毛利率 41%，2023 年谷底 33.5%；以 2027 年共識算出的 15.6 倍、PEG 0.42 都建立在高峰盈餘上，不能當便宜的證據"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把漲價週期的盈餘當新常態：陷阱風險中度（🟡），亮 1 項衰退信號；若 2028 年供給潮遇上非 AI 需求轉弱，股價可能再跌四到六成。","reasoning":"衰退信號十項只亮 1 項（EPS 成長遠高於營收成長，屬漲價驅動）；毛利率仍年增、自由現金流÷淨利約 1、維持性資本支出低（2026 前九月約 57 億元）。三項壓力測試過 2 項：①2023 年型谷底（毛利率 33.5%）仍獲利，FY2023 自由現金流 142 億元（過）；②淨負債 468.6 億元，約 FY2025 自由現金流 245.6 億元的 1.9 倍（過）；③谷底 EPS 約 13 元×景氣前 12 倍＝156 元，遠低於現價（不過）。回撤：股價已自前份 668 元跌約 25%，但 26 週仍 +59.5%，路徑風險高。法說問答：2024 年管理層曾拒答 AI 占比、OpEx 目標、稼動率何時到 90% 與混合 ASP；定性指引落空過一次（2024Q3 指引毛利率季增，實際持平），本次 Q4 指引同樣只有定性描述。","fact_refs":["f_kpi1","f_kpi6_book_to_bill","f_kpi7","f_net_debt_m","f_price_at_dd","f_week26_return_pct","f_peer_2327_tw_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰盈餘當分母的陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.19,"pe":24.69,"basis":"FY2026E 共識 EPS 20.19 元（Koyfin，新台幣）÷判斷日股價 498.5 元；終端倍數同樣套在當年度 EPS 上"},"eps":{"bull":[32.0,40.0,43.0,47.0,52.0],"base":[28.5,29.5,24.0,27.5,31.0],"bear":[23.0,19.0,13.0,15.0,17.0]},"pe":{"bull":22,"base":17,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.2,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-65,"hi":-40,"basis":"①Bear 終點 17 元×12 倍＝204 元，較現價約 −59%；②景氣前倍數：前一年平均股價約 134.6 元（104 週均線×2－52 週均線），約 FY2025 EPS 的 11.7 倍；③前兩次下行：2019Q1 毛利率季減 14.3pp、2019Q3 淨利年減 85.9%，2023 年毛利率 33.5%；④股價已自前份判斷日 668 元跌約 25%，26 週仍 +59.5%，漲幅還沒吐完。hi＝−40%（毛利率回到 36% 左右、EPS 約 20 元×15 倍＝300 元），lo＝−65%（谷底 EPS 約 13 元×13 倍≈170 元）。路徑風險高，但論點未破，屬深回撤心理準備","trigger_time":null},"basis":{"bull":"AI 占比升到 3 成以上、高階短缺延續到 2028 年，2027 年貼近共識 31.9 元，之後年增約 10%；市場以高階平台給 22 倍（低於賣方 31–40 倍，高於景氣前約 12 倍）","base":"2027 年漲價全年化＋擴產 10–15% 帶動 EPS 約 28.5 元（低於共識 31.9 元），2028 年供給放量後大致持穩，2029 年循環回落約兩成，2030–31 年回升；終端 17 倍介於景氣前約 12 倍與現價 24.7 倍之間","bear":"短缺在 2027 年中結束，村田等擴產遇上非 AI 需求轉弱，毛利率 2029 年回到 33–34%，EPS 13 元左右；終端倍數回到景氣前約 12 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"村田 2026-10-30 宣布五年約 1 兆日圓 MLCC 投資、FY2027–28 產能年增約 20%；京瓷傳擴產 3 倍；大摩點名日韓廠轉向高階，悲觀情境假設非 AI 需求自 2026 下半年大幅下滑；TrendForce 2026-09 消費級報價已轉軟；國巨 2019Q3 淨利年減 85.9%、2023 年毛利率 33.5%","assumption":"AI 需求的增量能吸收 2027–28 年新增供給，國巨的高階組合讓谷底高於前兩次","consequence":"若不成立，2029 年 EPS 回到 13 元左右、倍數回到景氣前約 12 倍，股價約 160–200 元，較現價 −60% 上下","ruling":"採納為 Bear 情境，機率 30%；與唯一致命點撞上（毛利率指引下滑＋訂單出貨比 <1 是第一個訊號），不另設","watch":"季度毛利率指引、訂單出貨比、TrendForce 高階報價、村田擴產進度","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#0","supply_demand_durability#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"],"fact_refs":["f_kpi1","f_kpi6_book_to_bill","f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"國巨規劃 2027 年擴產 10–15%，2026 年資本支出高於去年、2027 年規模未定；2024-07-30 CFO 說資本支出約 EBITDA 的 15–20%、以維持為主；2025 年以競價取得芝浦 87.3%、以非合意公開收購取得茂達約 28.5%（自稱財務性投資）","assumption":"AI 成長不需要大幅提高再投資率，併購能維持過去 KEMET 式的增益","consequence":"若同業擴產逼國巨跟進，資本支出占 EBITDA 升到 30% 以上、自由現金流÷淨利跌破 0.75，營收成長但每股自由現金流不增；高價收購稀釋報酬","ruling":"部分採納：自由現金流÷淨利目前仍約 1（FY2025 1.04），還沒發生；列為觀察，不調機率","watch":"年度資本支出÷EBITDA、自由現金流÷淨利、新併購的對價與資金來源","evidence_refs":["ma_merger#0","ma_merger#1","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_peer_2327_tw_fcf_margin_pct","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"追溯本益比 33.57 倍，在 4 個年度端點中最高，P/S 6.77 倍、EV/S 7.07 倍同樣最高；前一年平均股價約 134.6 元，只有 FY2025 EPS 的 11.7 倍；高盛、花旗以族群本益比壓縮為由調降目標價，大摩目標價降到 1,465 元","assumption":"市場會把 2026 年漲價週期的盈餘當新常態，並給高階平台溢價","consequence":"若市場改用正常化盈餘（約 16–20 元）與景氣前 12–14 倍，合理價約 190–280 元","ruling":"部分採納：現價只有 2027 年共識的 15.6 倍、低於大摩悲觀情境 685 元，市場已經不信遠期共識；但在本研究的基準路徑下 5 年價格報酬仍只有個位數，沒有安全邊際，所以觀望","watch":"Fwd 本益比與 2027 年 EPS 修正方向；外資目標價調整","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_ma_w52","f_ma_w104","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 668 → 本次 498.5（-25.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=668","side_b":"本次 price_at_dd=498.5","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 668 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 668 元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 668 元：Bull 價 1,144、Bear 價 204，五年期望值 −12.5%，基準年化 −4.6%，不對稱比 0.85","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.85。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 668 元：五年期望值 −12.5%，基準年化 −4.6%，不對稱比 0.85","side_b":"本次情境、股價 498.5 元：五年期望值 +17.2%，基準年化 1.1%，不對稱比 1.83","ruling":"再換股價、情境不動：起點價下跌 25.4%，五年期望值多 29.7 個百分點，基準年化多 5.7 個百分點，不對稱比由 0.85 升到 1.83。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價格與動能","cause":"價格變動","prior_field":["signal","trap"],"side_a":"前份（2026-05-26，股價 668 元）：訊號 B 級、陷阱風險中度，四週漲 110.7%，動能極端過熱","side_b":"本次（股價 498.5 元，約 −25%，RSI 39）：動能疑慮已消化，但循環位置轉為後段、正常化盈餘下估值不便宜，訊號與陷阱風險維持不變；定期定額結論與角色前後都未設","ruling":"價格回落抵銷了動能疑慮，但被週期後段與估值分母爭議取代，結論不變","evidence_level":"高（價格與技術指標為實測）","settle_metric":"股價相對 380 元重跑價位","if_then":["若股價跌破 380 元而毛利率與訂單出貨比未惡化，依條件重跑研究","若股價先漲回 650 元以上而 2027Q2 數據未到，不追"],"evidence_refs":[]},{"axis":"前份漂移：護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：護城河加深","side_b":"本次：穩定（→）","ruling":"新證據：村田 2026-10-30 宣布五年約 1 兆日圓 MLCC 投資、FY2027–28 產能年增約 20%，大摩指日韓廠轉向高階；國巨的轉型成果（高門檻應用約 75%）已實現，但定價力的擴大是缺貨期現象，合併判穩定","evidence_level":"中（擴產計畫為報導，效果尚未發生）","settle_metric":"國巨與村田營益率價差、TrendForce 高階報價","if_then":["若 2028 年高階報價季減而國巨營益率仍領先村田 8pp 以上，改判擴大","若營益率價差連 4 季收窄，改判縮減"],"evidence_refs":["cyclical_supply_discipline_capacity#2","competitive_share_entrants#0"]},{"axis":"前份漂移：分類與估值口徑","cause":"方法變動","prior_field":["val","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：估值中性（🟡）、未判類型、未設後五年跑道與循環位置，也沒有情境機率與回撤範圍","side_b":"本次：歸為循環股（次類為高品質成長），循環位置晚循環，後五年跑道中等（🟡），估值偏貴（🟠）；機率 25／45／30，回撤範圍 −40% 至 −65%","ruling":"股價自 668 元跌到 498.5 元本應讓估值改善；轉為偏貴完全來自改用正常化分母（前一年平均股價只有 FY2025 EPS 的 11.7 倍，現價是當年度 EPS 的 24.7 倍），屬方法變動而不是基本面轉壞；其餘欄位是本次新判","evidence_level":"高（倍數由事實表均線與財報直接推得）","settle_metric":"2027 年實際 EPS 與毛利率","if_then":["若 2027 年毛利率全年 ≥40% 且 2028 年指引不降，正常化 EPS 上調、估值改判中性"],"evidence_refs":[]},{"axis":"行動門檻：進場重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等回測 BB 中軌 NT$328 或 W52 NT$235 + Q3 26 AI 占比 ≥ 16% 三條件後試倉 3-5% 衛星","side_b":"股價 ≤380 元且 2027Q2 法說訂單出貨比 ≥1.3、毛利率 ≥39%（兩者同時成立）→重跑研究，進場首倉 ≤3%","ruling":"舊→新：AI 占比 ≥16% 已達成（2026Q3 約 2 成），52 週均線已升到 457.62 元，舊技術價位失去意義；改為價格錨＋事件錨同時成立，試倉上限由 3–5% 降到 ≤3%，因為循環位置轉為後段","evidence_level":"高","settle_metric":"股價與 2027Q2 法說數據","if_then":["兩條件同時成立才重跑研究，不直接進場"],"evidence_refs":[]},{"axis":"唯一致命點 Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"某一季法說指引下季毛利率下滑，同時訂單出貨比降到 1 以下（非季節性）","ruling":"新設 Single Thing：毛利率是盈餘最大的單一敏感項，發生即持有者減碼一半、未持有者不進場","evidence_level":"中","settle_metric":"每季毛利率指引與訂單出貨比","if_then":["發生：減碼一半；訂單出貨比連 2 季 <1.0：清倉"],"evidence_refs":[]},{"axis":"行動門檻：清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）；前份風險門檻為股價回檔 −15%／−30%、村田現貨價季減 10%、四大雲端資本支出年增 <10%","side_b":"單季毛利率連 2 季 <36%、非淡季訂單出貨比 <1.0、月營收年增連 3 個月 <+10%、AI 占比連 2 季 <20%；毛利率 <35% 且訂單出貨比連 2 季 <1.0 時清倉，月營收門檻觸發時減碼三分之一","ruling":"舊→新：股價回檔門檻已在價格面發生（668→498.5 元），不再有資訊量；現貨價與雲端資本支出事實表未涵蓋、無法追蹤，改用公司自己揭露的毛利率、訂單出貨比與月營收","evidence_level":"高","settle_metric":"季報與月營收","if_then":["任一指標觸發即依對應動作執行"],"evidence_refs":[]},{"axis":"論點門檻：假設與風險門檻改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：Q2 2026 AI 占 ≥16%、FY26 末 ≥20%；H2 前提：國巨無新擴產、2026 毛利率 ≥38%；R2：村田量產使 2026Q4 現貨價季減 >10%","side_b":"本次 H1：2027Q2 AI 占比 ≥22%；H2：2027 年各季毛利率 ≥39%、訂單出貨比 ≥1.2；R1：高階報價季減或訂單出貨比連 2 季 <1.2","ruling":"舊 H1 已達成（2026Q3 約 2 成），門檻上調；舊 H2 的前提「無新擴產」被 2027 年擴產 10–15% 推翻；村田風險的觀察點由現貨價改為擴產計畫（1 兆日圓）","evidence_level":"中","settle_metric":"2027 年各季法說","if_then":["新門檻連 2 季未達即論點削弱"],"evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"axis":"賣方共識與股價方向相反","cause":null,"prior_field":null,"side_a":"賣方：目標價 1,280–1,500 元（高盛、花旗、大摩），2028 年共識 EPS 46.9 元，現價只有 10.6 倍","side_b":"市場：股價 498.5 元，低於大摩悲觀情境 685 元，自前份判斷日跌約 25%；追溯本益比 33.57 倍仍在年度端點最高","ruling":"方向相反的不可調和矛盾，屬估值框架層，不涉及論點本身。裁 B 側：2028 年共識要淨利約 965 億元（46.9 元×20.58 億股），約為 2026Q3 年化淨利 479 億元的兩倍，已知產能（+10–15%）與已公布的漲價解釋不了，而且 2028 年正是村田等新產能放量年；基準 EPS 採 2027 年 28.5 元、2028 年 29.5 元。現在就買的最強論證：2027 年共識本益比 15.6 倍、股價低於大摩悲觀價、AI 占比 2 成且訂單出貨比近 2、短缺延續到 2027 上半年；但即使 2027 年 EPS 達 30 元，17 倍也只有 510 元，回到現價附近，不足以進場","evidence_level":"中（賣方目標價為 2026-07 報導轉述）","settle_metric":"2027Q2 法說訂單出貨比與毛利率","if_then":["若 2027Q2 訂單出貨比 ≥1.3 且毛利率 ≥39%，且股價 ≤380 元，重跑研究，通過後首倉 ≤3%","若 2027 年任一季指引毛利率下滑且訂單出貨比 <1.0，不進場；持有者減碼一半","反向：若股價先漲回 650 元以上而上述數據未到，不追","若股價先跌破 380 元但毛利率與訂單出貨比未惡化，依重跑結果分批反買，不是停損"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"近端短缺與遠端供給潮","cause":null,"prior_field":null,"side_a":"訂單出貨比近 2、稼動率近 95%、TrendForce 預期高階短缺延續到 2027 上半年、新產線建置需 1–2 年","side_b":"村田 FY2027–28 產能年增約 20%、京瓷傳擴產 3 倍、國巨自身 2027 年擴產 10–15%、消費級報價 2026-09 已轉軟","ruling":"可調和（時間差）：2027 年偏多、2028 年起風險上升；情境路徑把 2027 年放在高位、2029 年回落","evidence_level":"中（多為搜尋摘要轉述）","settle_metric":"TrendForce 高階 MLCC 季報價","if_then":["若 2027 下半年高階報價仍季增，Bull 機率上調到 35%","若高階報價季減，Bear 機率上調到 40%"],"evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2024-10-29 CFO Eddie Chen：Q3 2024 原指引毛利率、營益率季增低個位數，實際持平，歸因產品組合；2024-07-30 CEO Deng-Rue Wang：不追蹤 AI 營收、不預期 V 型反彈、資本支出以維持為主","side_b":"2026-10-29 法說：Q4 指引只給「微幅成長」，沒有數字區間；AI 占比改為主動揭露約 2 成；2027 年轉為擴產 10–15%","ruling":"可調和：由維持轉擴產與需求一致，但定性指引曾經落空；Q4 2026 實際毛利率若低於 Q3 的 41%，視為指引未兌現","evidence_level":"高（逐字稿原文）","settle_metric":"Q4 2026 毛利率相對 41%","if_then":["若 Q4 2026 毛利率 <41%，短缺延續的假設削弱一級"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：村田一兆日圓擴產、日韓廠轉向高階（大摩）、京瓷傳擴產","side_b":"結構轉好：AI 占比 2 成、75% 營收在高門檻應用、大中華區客戶 <25%；其他結構變數：關稅影響輕微（美國有普思、基美據點），近年沒有反壟斷案，替代技術多在國巨自家組合內","ruling":"雙向拉鋸：競爭惡化是未來 1–2 年的供給面，結構轉好是已實現的組合面，兩者時間錯開","evidence_level":"中","settle_metric":"營益率價差與高階報價","if_then":["若 2028 年營益率仍 ≥25%，改判結構性轉好中","若營益率跌破 20%，改判競爭惡化中"],"evidence_refs":["competitive_share_entrants#0","cyclical_supply_discipline_capacity#2"]}],"triggers":[{"n":1,"text":"AI 占比續升驗證","type":"假設驗證","maps_to":"H1","metric":"AI 相關營收占比","threshold":"2027Q2 法說 ≥22%","action":"達標維持論點；連 2 季 <20% 論點削弱，長期信心降為低","source_freq":"每季法說","date":"2027-07-31"},{"n":2,"text":"短缺延續驗證","type":"假設驗證","maps_to":"H2","metric":"單季毛利率、訂單出貨比","threshold":"毛利率 ≥39% 且訂單出貨比 ≥1.2","action":"連 2 季未達：Base 機率移 10 個百分點到 Bear","source_freq":"每季法說","date":"2027-02-28"},{"n":3,"text":"日系擴產進度與高階報價","type":"風險","maps_to":"R1","metric":"TrendForce 高階 MLCC 季報價；村田岡山新廠時程","threshold":"高階報價季減，或岡山新廠提前完工","action":"未持有者延後重跑研究；持有者停止加碼","source_freq":"每月","date":"2027-04-30","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#0"]},{"n":4,"text":"非 AI 需求轉弱","type":"減碼","maps_to":"R2","metric":"月營收年增率","threshold":"連 3 個月 <+10%","action":"持有者減碼三分之一；未持有者不進場","source_freq":"每月 10 日前","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":5,"text":"漲價週期第一次反轉","type":"Single Thing","maps_to":"Single Thing","metric":"下季毛利率指引＋訂單出貨比","threshold":"指引下滑且訂單出貨比 <1.0（非淡季）","action":"不進場；持有者減碼一半","source_freq":"每季法說","date":"2027-02-28"},{"n":6,"text":"價格與數據同時到位才重跑","type":"估值rearm","maps_to":"觀望約束","metric":"股價；2027Q2 訂單出貨比與毛利率","threshold":"≤380 元且訂單出貨比 ≥1.3、毛利率 ≥39%","action":"重跑研究，通過後首倉 ≤3%","source_freq":"每日股價＋每季法說","date":"2027-07-31"},{"n":7,"text":"景氣下行確認","type":"清倉","maps_to":"R3","metric":"單季毛利率、訂單出貨比","threshold":"毛利率 <35% 且訂單出貨比連 2 季 <1.0","action":"清倉，改用循環谷底框架重新研究","source_freq":"每季法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"n":8,"text":"全年財報複審","type":"複審日期","maps_to":null,"metric":"2026Q4 財報與 2027 年展望","threshold":"2027-02 底法說","action":"重跑本研究","source_freq":"一次","date":"2027-02-28"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連 2 季 <36%（2026Q3 為 41%）","window":"2027Q1–2028Q4","source":"國巨季報與法說會","last_status":"ok"},{"metric":"訂單出貨比","bear_threshold":"非淡季單季 <1.0","window":"每季法說，2027–2028","source":"國巨法說會","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 <+10%（2026-09 為 +46.1%）","window":"2026-11 起逐月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"AI 相關營收占比","bear_threshold":"連 2 季 <20%","window":"2027 年各季","source":"國巨法說會","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價 ≤380 元且 2027Q2 法說訂單出貨比 ≥1.3、毛利率 ≥39%（兩者同時成立）→重跑研究，首倉 ≤3%","exec_line":"現在不進場、不追價；兩條件同時成立後重跑研究，首倉 ≤3%，循環位置回到早中段前不加碼；若已持有，Single Thing 發生即減碼一半，毛利率 <35% 且訂單出貨比連 2 季 <1.0 清倉","holding_cap":"3%（循環後段、路徑風險高）"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤380 元（約 2027 年基準 EPS 的 13 倍），且 2027Q2 法說訂單出貨比 ≥1.3、毛利率 ≥39%，兩者同時成立才重跑研究","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=59.5, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 相關營收占比結構性擴大，帶動高階電容與電感的組合升級","2y":"2027Q4 AI 占比 ≥25%","5y":"2031 年 AI 占比 ≥30%，且 AI 營收在下一個景氣下行年仍年增","10y":null,"threshold":"2027Q2 法說 AI 占比 ≥22%（2026Q3 約 2 成）","source":"國巨每季法說會；月營收","drift_rule":"2 年期：AI 占比連 2 季低於門檻 5% 以上（<20.9%）削弱，連 3 季低於門檻 10% 以上（<19.8%）反轉"},{"id":"H2","text":"高階 MLCC 與鉭質電容短缺延續到 2027 年，漲價與高稼動率撐住毛利率","2y":"2027 年全年毛利率 ≥40%、各季訂單出貨比 ≥1.2","5y":null,"10y":null,"threshold":"2027 年各季毛利率 ≥39%（2026Q3 為 41%）","source":"季報；法說會訂單出貨比與稼動率；TrendForce 月度 MLCC 報價","drift_rule":"TTM 毛利率連 2 季低於 37%（門檻 −5%）削弱、連 3 季低於 35%（−10%）反轉；非淡季訂單出貨比 <1.0 直接視為反轉"},{"id":"H3","text":"高階化與地域分散讓下一個景氣谷底高於前兩次","2y":null,"5y":"下一個谷底年毛利率 ≥34%、營益率 ≥20%、EPS 不低於 FY2025 的 11.48 元","10y":"跨一個完整循環的平均營益率 ≥22%","threshold":"谷底年毛利率 ≥34%（2023 年谷底 33.5%）","source":"年報與季報","drift_rule":"5 年期：TTM 毛利率連 4 季低於 32.3%（門檻 −5%）削弱、連 6 季低於 30.6%（−10%）反轉；10 年期：跨 2 個年度營益率 <22% 削弱、跨 3 個年度反轉"}],"R":[{"id":"R1","text":"村田、京瓷與日韓廠擴產在 2027 下半年到 2028 年放量，高階 MLCC 由短缺轉寬鬆，漲價逆轉","h_ref":"H2","clock":"🔥","threshold":"TrendForce 高階 MLCC 報價季減，或國巨訂單出貨比連 2 季 <1.2","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#0"]},{"id":"R2","text":"非 AI 需求轉弱：消費級報價 2026-09 已轉軟，若車用、工規、消費同步下滑，AI 的增量蓋不住","h_ref":"H2","clock":"⚡","threshold":"月營收年增率連 3 個月 <+10%（2026-09 為 +46.1%）","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"重演 2019 或 2023 年型下行：毛利率回到 33–35%，盈餘回吐大半","h_ref":"H3","clock":"🐢","threshold":"單季毛利率 <35%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R4","text":"族群倍數壓縮延續：外資已以族群本益比壓縮為由調降目標價，獲利達標股價仍可能不漲","h_ref":"估值","clock":"🔥","threshold":"Fwd 本益比跌破 15 倍（現 24.86 倍）而 2027 年共識 EPS 未下修","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"single_thing":{"description":"某一季法說管理層指引下季毛利率下滑，同時訂單出貨比降到 1 以下（非季節性），也就是本輪漲價週期第一次反轉的訊號","why_fatal":"毛利率是盈餘最大的單一敏感項：以 2027 年營收約 2,300 億元估，毛利率每 1pp 約稅後 18 億元、每股約 0.9 元；由 41% 回到 2023 年的 33.5%，每股少約 6.6 元，2027 年 EPS 由 28 元左右掉到 21 元附近，共識 2028 年 46.9 元的路徑同時失效","if_happens":"不進場；若已持有，減碼一半，訂單出貨比連 2 季 <1.0 清倉；研究改以谷底 EPS 13 元左右與 12–14 倍重算","how_monitor":"每季法說（2 月、4 月、7 月、10 月底）的毛利率指引與訂單出貨比；每月 10 日前的月營收；TrendForce 月度 MLCC 報價","probability":"約 35%（12–24 個月內）：TrendForce 預期短缺延續到 2027 上半年，村田 FY2027–28 產能年增約 20%，2028 年前後是供給放量窗口"}},"appendix_a":{"growth_durability":6,"quality_score":7.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.6,"peg_fy2":0.27,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":11.48,"FY2026E":20.19,"FY2027E":31.92,"FY2028E":46.9},"fy_end_month":12,"eps_basis":"稀釋 EPS（新台幣；FY2025A 取年度財報，FY2026E–FY2028E 取 Koyfin 共識，美元依 2026-10-31 匯率換算）"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026Q4 財報與 2027Q1 指引","impact":"高","watch":"毛利率是否高於 41%、訂單出貨比"},{"date":"2027-04","date_precision":"month","type":"capacity","event":"村田岡山新廠動工","impact":"中","watch":"擴產時程是否提前"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"國巨 2027 年新增產能部分開出","impact":"中","watch":"稼動率是否仍 ≥90%"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"2027Q2 法說","impact":"高","watch":"訂單出貨比 ≥1.3、毛利率 ≥39%、AI 占比 ≥22%"}]}
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
