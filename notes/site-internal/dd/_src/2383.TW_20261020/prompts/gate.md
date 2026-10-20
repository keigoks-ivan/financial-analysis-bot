你是 DD 管線 v20 的判斷層閘（gate），標的 2383.TW（20261020）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定，與來源 gate_contract §⑤／critic-gates 的「缺軸即 🔴」不同；重新濃縮時以本卡 ⑤ 為準 -->

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

### 判斷檔 `fact_refs` 引到的事實（38 條）
- `f_kpi0_ifrs`（q1_business）｜營收（合併，IFRS）＝47275.19 百萬TWD｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（2383.TW，TWD）；與 uanalyze 2026-07-29 報導（營收472.7億、毛利率33.9%、淨利98.7億、EPS 27.55）相符；財報日取自 dd_numbers_extra earnings_recency（MOPS 重大訊息），未取得公司 IR 新聞稿 URL（numbers.latest_quarter_kpis.items[0]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
  - 註記：凱基 2026-07-29 報告：季營收473億元優於共識 9.8%
- `f_kpi1_gaap`（q1_business）｜GAAP 毛利率＝33.85 %｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（2383.TW，TWD）；與 uanalyze 2026-07-29 報導（營收472.7億、毛利率33.9%、淨利98.7億、EPS 27.55）相符；財報日取自 dd_numbers_extra earnings_recency（MOPS 重大訊息），未取得公司 IR 新聞稿 URL（numbers.latest_quarter_kpis.items[1]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
  - 註記：凱基：33.9% 優於共識 32.5%
- `f_kpi2_gaap_ifrs_non_gaap_gaap`（q1_business）｜GAAP 營業利益率（台灣 IFRS 無 non-GAAP 口徑，營業利益即 GAAP）＝26.94 %｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（2383.TW，TWD）；與 uanalyze 2026-07-29 報導（營收472.7億、毛利率33.9%、淨利98.7億、EPS 27.55）相符；財報日取自 dd_numbers_extra earnings_recency（MOPS 重大訊息），未取得公司 IR 新聞稿 URL（numbers.latest_quarter_kpis.items[2]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
  - 註記：凱基：26.9% 優於共識 25.1%
- `f_kpi3_gaap`（q1_business）｜營業利益（GAAP）＝12739.82 百萬TWD｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（2383.TW，TWD）；與 uanalyze 2026-07-29 報導（營收472.7億、毛利率33.9%、淨利98.7億、EPS 27.55）相符；財報日取自 dd_numbers_extra earnings_recency（MOPS 重大訊息），未取得公司 IR 新聞稿 URL（numbers.latest_quarter_kpis.items[3]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
- `f_kpi4_eps`（q1_business）｜稅後淨利／EPS＝27.55 TWD/股（淨利 9,873.40 百萬TWD，淨利率20.88%）｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（2383.TW，TWD）；與 uanalyze 2026-07-29 報導（營收472.7億、毛利率33.9%、淨利98.7億、EPS 27.55）相符；財報日取自 dd_numbers_extra earnings_recency（MOPS 重大訊息），未取得公司 IR 新聞稿 URL；uanalyze.com.tw/articles/9219952430（numbers.latest_quarter_kpis.items[4]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
- `f_kpi6_2026`（q1_business）｜資本支出（2026 全年，券商轉述）＝32000 百萬TWD｜期間與口徑：2026-07-29 凱基報告（券商轉述，非公司新聞稿）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：WebSearch 摘要凱基 emc-2383-tt20260729en.pdf（PDF 無法解析，數字未經原文核對）（numbers.latest_quarter_kpis.items[6]，as_of 2026-07-29 凱基報告（券商轉述，非公司新聞稿））
- `f_kpi7`（q1_business）｜管理層指引／展望＝公司無正式數字區間（查無）；公司稱未來一年維持「全產全銷」、產能滿載 文字｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：uanalyze.com.tw/articles/9219952430（媒體轉述）（numbers.latest_quarter_kpis.items[7]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
  - 註記：3Q26 季增≥15%、毛利率再升≥1pp 為凱基推估，非公司指引
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-07-29 date｜期間與口徑：2026-07-29／距今 59 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-07-29）
- `f_peer_2383_tw_gross_margin_pct`（q2_moat）｜2383.TW 毛利率＝31.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2383.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2383_tw_operating_margin_pct`（q2_moat）｜2383.TW 營業利益率＝23.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2383.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_600183_ss_gross_margin_pct`（q2_moat）｜600183.SS 毛利率＝29.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600183.SS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_600183_ss_operating_margin_pct`（q2_moat）｜600183.SS 營業利益率＝19.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600183.SS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6213_tw_gross_margin_pct`（q2_moat）｜6213.TW 毛利率＝15.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6213.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6213_tw_operating_margin_pct`（q2_moat）｜6213.TW 營業利益率＝8.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6213.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝118.64 TWD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.3269 @ 2026-10-17)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-17）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝235.66 TWD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.3269 @ 2026-10-17)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-17）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝379.84 TWD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.3269 @ 2026-10-17)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-17）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝23.19 %｜期間與口徑：2026-07-16 → 2026-10-17／FY1 共識 EPS 96.31 → 118.64（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-17）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝198457.42 TWD m｜期間與口徑：2026-10-20／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝336706.76 TWD m｜期間與口徑：2026-10-20／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流−資本支出）＝-2838.75 百萬TWD｜期間與口徑：2026Q2（季末 2026-06-30，董事會公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 2,341.78；capex −5,180.53）（numbers.latest_quarter_kpis.items[5]，as_of 2026Q2（季末 2026-06-30，董事會公告 2026-07-29））
- `f_peer_2383_tw_fcf_margin_pct`（q2_moat）｜2383.TW FCF 利潤率＝-2.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2383.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.495 %｜期間與口徑：2026-10-20／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-20）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝5924.89 TWD m｜期間與口徑：2026-10-20／yfinance 最新一季：總債務 28492.65、現金 22567.76（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝358.32 m shares｜期間與口徑：2026-10-20／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝5055.0 TWD｜期間與口徑：2026-10-20（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-20（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝79.38 x｜期間與口徑：2026-10-20（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-20（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.94 x｜期間與口徑：2026-10-20（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-20（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝42.78 x｜期間與口徑：2026-10-17／分母＝FY1 EPS 118.64，分子＝快照價 5075.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-17）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝9.19 x｜期間與口徑：2026-10-20／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.52｜期間與口徑：2026-10-20（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-20（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝29.45 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-10-20／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）
  - 原文：「price 5135.0 / W52 3647.82 / W104 2212.03 / W250 1089.25 / W250 13週斜率 8.14%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝3647.82 TWD｜期間與口徑：2026-10-20／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）
- `f_ma_w104`（q5_valuation）｜104 週均線＝2212.03 TWD｜期間與口徑：2026-10-20／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）
- `f_ma_w250`（q5_valuation）｜250 週均線＝1089.25 TWD｜期間與口徑：2026-10-20／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）

### findings_digest 中方向為負或來源衝突的條目（1 條）
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：市場擔心 CPO「光進銅退」趨勢可能削弱 M8、M9 等高階 CCL 需求
  - 來源：中時 wantrich 台光電報導（as_of 2026-03-13）｜affects：moat_trend、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":12960,"bear_5y_price":2025,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":32.5,"ev5y_pct":24.9,"irr_base_pct":5.8,"asym_ratio":1.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":118.64,"pe":42.61,"basis":"FY2026E 共識每股盈餘（Koyfin 快照換算新台幣）；終端倍數同樣用當年度每股盈餘"},"eps":{"bull":[250,380,450,500,540],"base":[215,290,310,320,335],"bear":[195,160,120,125,135]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.495,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 5 | 5 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | none | 0 | 4 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 3 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 3 | 4 |
| major_events | found | 1 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：台光電 大客戶 第二供應商 OR 轉單 2026；台光電 客戶 自製 OR 分散供應商；2383.TW Elite Material largest customer second source OR in-house 2026
- **reg_tariff_export**（none）：台光電 關稅 OR 232 影響 2026；台光電 出口管制 OR 實體清單 OR 國貿署；台光電 美國 關稅 轉嫁 OR 客戶 分攤；2383.TW Elite Material tariff OR export control exposure 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260601","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 基建高階 CCL 結構性需求 + 漲價，推升營收與毛利","columns":{"2Y 驗證點":"2026–2027 月營收 YoY ≥20%、Q2 漲價達 ≥10%、TTM GM ≥29%","5Y 驗證點":"透析期 GM 中樞 ≥28%","10Y 驗證點":"高速 CCL 長期結構需求","數字門檻":"YoY ≥20%；GM ≥29%","來源":"公司法說 / GS、Prismark","漂移觸發":"YoY"}},{"id":"H2","text":"台光電維持高階 CCL 份額 / 收復最先進節點（Rubin）","columns":{"2Y 驗證點":"2026 6–7 月 Rubin 供應商清單守住 ≥40% / 收復部分","5Y 驗證點":"M9+ 持續全球領先、份額 ≥35%","10Y 驗證點":"下世代材料轉換中保住地位","數字門檻":"Rubin 份額 ≥40%；無鹵高速 ≥35%","來源":"Digitimes / GS 供應鏈","漂移觸發":"確認完全出局 Rubin → 推翻（5.F）"}},{"id":"H3","text":"市場維持高成長股估值（Fwd PE 30x+）使股價反映 EPS 成長","columns":{"2Y 驗證點":"EPS 兌現使 Fwd PE 降至 ≤25x 或股價回檔","5Y 驗證點":"競爭未瓦解高階溢價","10Y 驗證點":"結構溢價而非循環折價","數字門檻":"FY+2 Fwd PE ≤25x 且分位","來源":"本 DD §13","漂移觸發":"分位持續 >85% → H3 反轉風險"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI CCL 漲價/需求循環反轉（capex 正常化）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4–6 季）","監測指標":"月營收 YoY、毛利率、漲價持續性","警戒閾值":"YoY"}},{"id":"R2","text":"最先進節點份額流失（Rubin → Doosan，GB300 已失）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1–2 季可觸發，6–7 月窗口）","監測指標":"Rubin 供應商清單、GS/Digitimes 供應鏈","警戒閾值":"確認完全出局 Rubin（5.F）"}},{"id":"R3","text":"材料路線/客戶分散稀釋高階溢價","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"玻璃基板系統板、二供扶植進度","警戒閾值":"主要 AI 主板採新基材或台光電份額跌破 35%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":5070.0,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2383.TW","date":"2026-10-20","schema":"v15.2","contract":"v19","company_name":"台光電"},"oneliner":"AI 高階銅箔基板龍頭，2025 年營收躍居全球第一、產能賣到 2027 年；但 2027–28 共識獲利建立在漲價延續上，現價約 2027 年共識每股盈餘 21 倍，基本情境五年年化約 6%，等回到 4,300 元附近再談","facts_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/facts.json","scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 伺服器與交換器板廠的錢，賣高速、低損耗銅箔基板；錢卡在新平台材料認證這一節點。今年成長主要靠漲價加滿載，產業處擴張期後段","reasoning":"2026 年第二季營收 472.8 億元、毛利率 33.85%、營業利益率 26.94%、每股盈餘 27.55 元。九月營收 215.3 億元，年增 168.9%；前九月 1,412.3 億元，年增 103.7%。以第一季 330.7 億元推算，第三季約 608.9 億元，季增約 29%。營收結構依 2026-03 法說：基礎建設 65–70%、行動裝置 20–25%、車用工業 5–10%，公司預估今年基礎建設升到 70–80%。前兩大客戶 2025 年各占 14% 與 12%，2026 第一季最大客戶占 15%，未達單一客戶 40% 的集中警戒；出貨節奏仍由兩大 AI 平台客戶的新平台決定。錢卡在認證：材料要先通過晶片商與雲端業者的新平台認證才能出貨，通過後同一代平台內不易更換。上游 HVLP 銅箔、E 布與低介電玻纖布吃緊，部分利潤正往上游流。產業時鐘判為擴張期（II），依據是公司稱全產全銷、高階材料短缺，業界看中高階 CCL 至 2028 年供不應求，而全產業同時大舉擴產，這是擴張後段的特徵。供需持久度判為週期性，2028 年後有反轉風險：公司 2027 年底總產能 945 萬張，同業同步擴產，供給可逆性高。產業態勢三軸：競爭面，斗山與台燿在新平台搶份額；結構面，公司 2025 年躍居全球 CCL 營收第一，高速材料份額自述 38.6%；其他結構變數是替代技術（光進銅退）。裁決為雙向拉鋸，結構轉好與替代技術風險同時存在。管理層沒有正式數字財測；第三季季增 15% 以上、毛利率再升 1 個百分點是券商推估。","fact_refs":["f_kpi0_ifrs","f_kpi1_gaap","f_kpi2_gaap_ifrs_non_gaap_gaap","f_kpi3_gaap","f_kpi4_eps","f_kpi6_2026","f_kpi7","f_earnings_recency"],"verdict_values":{"revenue_quality":"以基礎建設（AI 伺服器、交換器、衛星）為主，公司預估 2026 年占 70–80%；成長來自第二季起漲價 10% 以上加產能滿載。品質高但對報價週期敏感","unit_econ_note":"單價與出貨量的結構化數字事實表未涵蓋；第二季毛利率 33.85%，季增 4.3 個百分點，法人歸因漲價。年底 M7 以上材料營收占比預估升到 70%（法人）","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"高階 CCL 份額龍頭，靠 AI 平台認證綁定；但價格與需求跟著 AI 資本支出與上游缺料循環。2023 年電子業低迷時每股盈餘仍由 14.86 元升到 15.75 元，顯示有一定韌性"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉（時點約 2028 年後）：股東會稱高階材料仍短缺，業界稱中高階 CCL 至 2028 年供不應求；但公司 2027 年底產能要到 945 萬張，同業也在擴產，供給可逆性高","bargaining":{"up":"上游 HVLP3／HVLP4 銅箔、E 布與低介電玻纖布吃緊，供應商議價力上升，法人不排除 CCL 再漲價轉嫁","down":"前兩大客戶 2025 年各占 14%、12%，未達集中警戒；新平台認證通過後客戶在一代平台內難以更換","geo":"產能以兩岸為主，另有馬來西亞檳城與美國加州 Arlon EMD（預計 2026 年底營運）分散；關稅與出口管制影響事實表未涵蓋"},"profit_pool_dir":"利潤池往 M7 以上高階材料集中；法人預估年底 M7 以上營收占比升到 70%，同時部分利潤被上游缺料環節分走","tam_table":{"expanded":false,"reason":"事實表未涵蓋 CCL 或高速材料市場規模、滲透率與利潤池占比的數字；份額只有公司自述高速材料 38.6% 與 Prismark 排名，無法填表"}}}},"q2_moat":{"verdict":"護城河擴大中，等級 B：靠 AI 平台材料認證加上全球最大的高階產能，份額升到全球第一；但定價力有一部分來自缺貨景氣，不全是結構","reasoning":"機制是 AI 平台材料認證加上全球最大高階產能。認證要跟著晶片商與雲端業者的新平台逐代通過，通過後一代平台內很難更換；產能規模又讓客戶在缺料時優先找它。可證方向：TTM 營業利益率 23.05%，高於生益的 19.3%（差 3.75 個百分點）與聯茂的 8.94%；TTM 毛利率 31.06%，生益為 29.26%。Prismark 稱 2025 年全球 CCL 營收排名由第三升到第一；法人稱 Google 需求下同業產能不足，公司可拿到更多份額。執行力評 8 分：擴產節奏與份額都在擴大。定價力評 7 分：漲價 10% 以上能轉嫁，毛利率由 2025 年 29.83% 升到第二季 33.85%，但這段有全產業缺料的成分。趨勢判擴大，等級 B。最大客戶占營收由 2024 年 13% 升到 2026 第一季 15%，沒有最大客戶份額下滑的證據；不過公司在客戶端的份額沒有直接數字。報酬持續期：當期營業利益率高，投入資本與周轉率事實表未涵蓋，象限依資本支出強度推斷為高利益率、周轉偏低。增量報酬以年度淨利與自由現金流推算約 44%，再投資率約 86%，內生成長上限約 38%（推算過程見公式欄）。四檢查點：需求基礎值與決策層級為黃，因為需求可延後、每代平台要重新認證；價值鏈分配為黃，上游缺料分走利潤；社會容忍度為綠。","fact_refs":["f_peer_2383_tw_gross_margin_pct","f_peer_2383_tw_operating_margin_pct","f_peer_600183_ss_gross_margin_pct","f_peer_600183_ss_operating_margin_pct","f_peer_6213_tw_gross_margin_pct","f_peer_6213_tw_operating_margin_pct","f_kpi1_gaap","f_kpi6_2026"],"verdict_values":{"moat":{"mechanism":"AI 平台材料逐代認證綁定，加上全球最大高階 CCL 產能，缺料期客戶優先下單","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行力擴大：Prismark 稱 2025 年全球營收排名由第三升到第一，法人預期 Google 份額增加。定價力擴大但帶週期成分：第二季漲價 10% 以上後毛利率 33.85%，TTM 營業利益率 23.05%，高於生益的 19.3%；其中一部分來自上游缺料造成的全產業漲價","competitor_notes":[{"name":"斗山（Doosan）","strategy_note":"輝達最先進平台的主要對手，與公司點對點競爭；事實表沒有其財務數字"},{"name":"台燿（6274.TW）","strategy_note":"下半年大客戶大量導入 1.6T 交換器 M8 材料，交換器材料份額擴大；財報數字事實表無資料"},{"name":"生益科技（600183.SS）","strategy_note":"TTM 營業利益率 19.3%、自由現金流率 9.39%，利潤率略低但現金流較好；2025 年營收排名被公司超越"},{"name":"聯茂（6213.TW）","strategy_note":"TTM 毛利率 15.82%、營業利益率 8.94%，遠低於公司，以中低階為主，在高階不構成直接威脅"}],"spread_notes":{"note":"TTM 營業利益率差：對生益多 3.75 個百分點，對聯茂多 14.11 個百分點；只有一期數字，無法判斷差距擴大或收窄，ROIC 差事實表未涵蓋"},"peer_na_reason":"台燿財報事實表無資料；斗山未列入同業表；同業 ROIC 缺投入資本資料","threats":[{"level":"🔴","text":"光進銅退（光學共封裝）可能削弱 M8、M9 高階材料需求，屬生態層替代；替代程度與時點事實表未涵蓋","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"斗山在輝達最先進平台與公司點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"台燿等同業擴產，並在 1.6T 交換器 M8 材料擴大份額","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"上游 HVLP 銅箔與低介電玻纖布吃緊，價值鏈利潤往上游移動","p":"40%","evidence_refs":["capital_markets_pricing#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（周轉率事實表未涵蓋，依資本支出約占營收一成半推斷）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 AI 伺服器與交換器板廠，決策者是晶片商與雲端業者的平台設計，付款者是雲端資本支出。高速訊號需要低損耗材料，屬於需要而非想要；但付款端可延後，急迫性不等於持久性。業界稱供不應求至 2028 年，屬產業自述"},{"item":"決策層級","level":"🟡","text":"替代性要看平台這個最小決策單位：每代新平台重新認證，認證後一代內難換；但每次換代都是重新開標的機會，斗山與台燿都在搶下一代"},{"item":"價值鏈分配","level":"🟡","text":"下游客戶集中且量大，上游 HVLP 銅箔與玻纖布吃緊；公司今年能把漲價轉嫁出去，毛利率升到 33.85%，但缺料環節也在多拿；產能開出後議價重心可能往客戶端移"},{"item":"社會容忍度","level":"🟢","text":"B2B 工業材料，沒有民生價格敏感問題；公平會處分書搜尋 0 筆，2025 年度反競爭訴訟損失為 0，不依賴監管授權"}],"roiic":"約 44%（推算）","reinvest_rate":"2025 年約 86%；2026 年 TTM 自由現金流為負，再投資率超過 100%","endo_ceiling":38,"formula_note":"資料取自事實表年度財報（yfinance 2022–2025）。2023→2025 年淨利增加 91.6 億元（54.9→146.5 億）。同期再投資以淨利減自由現金流估算：2024 年 82.3 億加 2025 年 125.6 億，合計 207.9 億元。增量報酬約 91.6÷207.9≈44%。2025 年再投資率 125.6÷146.5≈86%。內生成長上限≈44%×86%≈38%。限制：以淨利代替稅後營業利益；投入資本事實表未涵蓋；增量淨利多半來自漲價而非新資本，增量報酬偏高估"}}}},"q3_growth":{"verdict":"成長跑道中等：份額已高，五年後要靠 AI 高速材料總需求擴大與 M9 接棒。共識三年每股盈餘年複合約 110%，遠高於內生上限約 38%，差額靠漲價與利潤率擴張支撐","reasoning":"成長組成：2026 年以價為主（第二季起漲價 10% 以上），法人看 2027 年價量齊揚；無併購、無回購。共識每股盈餘 FY2026 118.64 元、FY2027 235.66 元、FY2028 379.84 元，以 2025 年 40.81 元為基期，三年年複合約 110%。內生上限約 38%（見護城河段的增量報酬乘再投資率），缺口約 72 個百分點，可歸因於利潤率擴張與漲價：淨利率由 2025 年約 15.5% 升到第二季 20.9%，共識 FY2027 隱含約 25%，不靠收購或回購。跑道判中等：份額已過三成，五年後要靠 AI 高速材料總需求擴大與 M9 接棒，第二條曲線（衛星、光學共封裝時代材料）沒有具體證據。衰退訊號亮兩項：獲利成長遠快於營收、自由現金流轉換率低，所以價值陷阱風險與長期成長性都判黃。另外，共識 FY2026 營收 1,984.6 億元隱含第四季僅約 572 億元，低於第三季推算的約 609 億元，該營收共識疑似未更新，不作承重。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi4_eps"],"verdict_values":{"growth":{"driver_mix":"2026 年價為主、產能滿載為輔；2027 年價量齊揚（法人看法）；無併購、無回購","runway_years":"事實表未涵蓋高速材料市場規模；公司自述份額 38.6% 已過 30%，滲透率法不適用，成長要靠市場本身擴張","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 44% × 2025 年再投資率約 86% ≈ 38%（年度淨利減自由現金流推算，偏高估）","segments":[{"item":"基礎建設（AI 伺服器、交換器、低軌衛星）","value":"2025 年第四季法說 65–70%，公司預估 2026 年 70–80%"},{"item":"行動裝置","value":"20–25%"},{"item":"車用、工業及其他","value":"5–10%"}],"decay_signals":[{"signal":"每股盈餘成長顯著快於營收（差距超過 5 個百分點）","lit":true,"evidence":"共識 FY2025→FY2027 每股盈餘年複合約 140%，營收約 89%"},{"signal":"自由現金流對淨利低於 0.75 連兩年","lit":true,"evidence":"2024、2025 年皆約 0.14"},{"signal":"替代技術壓縮市場","lit":false,"evidence":"光進銅退仍屬市場擔憂，未見採用證據，列為觀察"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"第二季 33.85%，連續上升"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"Prismark 排名上升，無份額下滑的資料"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：錢幾乎全數投入擴產，自由現金流薄且近期轉負；股息高於自由現金流，股數每年增加約 1.7%","reasoning":"現金去向：2026 年資本支出約 320 億元（券商轉述，未核對原文）；第二季營業現金流 23.4 億元、資本支出 51.8 億元，自由現金流 −28.4 億元，TTM 自由現金流率 −2.9%。2022–2025 年自由現金流合計約 30.4 億元，對淨利 349 億元的轉換率約 9%。股息以殖利率 0.495% 推算每股約 25 元，總額約 90 億元，高於 2025 年自由現金流 20.9 億元，差額靠現金與借款；淨負債 59.2 億元，槓桿仍低。沒有併購：加州 Arlon EMD 是對既有子公司增資 4,900 萬美元。回購紀錄事實表未涵蓋。股數以淨利除以稀釋每股盈餘推算，2022 年約 3.41 億股，2025 年約 3.59 億股，年增約 1.7%，略高於 1.5% 標準。三項計分：併購不適用、回購不適用、稀釋未過。研發密度 2.15%，低於生益的 5.03%。","fact_refs":["f_kpi5","f_kpi6_2026","f_peer_2383_tw_fcf_margin_pct","f_dividend_yield_ttm","f_net_debt_m","f_shares_diluted_m","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月重大訊息無併購；加州子公司增資屬自建產能"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"回購紀錄事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"淨利除以稀釋每股盈餘推算股數，2022 年 3.414 億股、2025 年 3.590 億股，年增約 1.7%，高於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能不靠併購，回購資料事實表未涵蓋，沒有可展開的資本回報明細"}}}},"q5_valuation":{"verdict":"現價約 FY2027 共識每股盈餘的 21 倍，等於要求 2027 年價量齊揚完全兌現，且 2028 年後不出現報價反轉。我們只信前半段，基本情境五年年化約 6%，偏貴","reasoning":"現價 5,055 元。Trailing 本益比 79.4 倍、市銷率 13.9 倍，都在四個年度端點的最高處；五年分位口徑事實表未涵蓋，不外推。FY2026 共識本益比 42.8 倍，FY2027 約 21.5 倍（5,055÷235.66）。PEG 以 FY2026 本益比 42.6 倍除以三年共識年複合約 110%，約 0.39；但分母是週期高點的漲價獲利，不能當便宜的證據。現價要求兩件事：2027 年每股盈餘翻倍到約 236 元，且 2028 年後市場仍給 20 倍以上。我們信 2027 年的大半（基本情境 215 元），不信 2028 年 380 元會延續。短期目標：一年後市場看 2028 年，基本情境 290 元乘 18 倍（週期高點折價）約 5,220 元，上漲約 3%。中期目標：2029 年基本情境 310 元乘 20 倍約 6,200 元，上漲約 23%。前瞻企業價值營收比 9.2 倍。動能面：FY2026 共識三個月上修 23%，RSI 43.5，26 週漲 29.5%，週線多頭排列。同業本益比事實表未涵蓋，終端倍數無法附同業對照。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_s_fwd","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026、FY2027 共識每股盈餘）","tier":"高階 CCL 龍頭","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有台燿、聯茂、生益、斗山的本益比，無法做倍數對照；終端倍數改以自身 FY2027 共識倍數 21.5 倍為錨"},"fwd_pe":42.78,"peg":0.39,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"Trailing 本益比 79.4 倍，在四個年度端點中最高；FY2026 共識 42.8 倍，FY2027 約 21.5 倍。基本情境五年年化約 6%，低於 8% 但不虧損，判偏貴。前份判最貴一級，這次下修一級，原因是三個月內 FY2026 共識每股盈餘上修 23%，而股價持平","upside_short_pct":3,"upside_mid_pct":23,"denominator_disputed":true,"denominator_note":"FY2027–2028 共識每股盈餘隱含兩件事同時成立：漲價延續，以及產能一年擴充約五成全數消化。分母本身就是爭點，便宜論證不成立"}}},"q6_how_wrong":{"verdict":"最可能看錯在報價：2028 年前後全產業新產能開出時若報價反轉，獲利會回到 120–135 元，倍數壓到 15 倍","reasoning":"第一個錯點是報價。今年成長以漲價為主，若 2028 年前後報價反轉，每股盈餘回到 120–135 元，倍數壓到 15 倍，五年後約 2,000 元。第二個錯點是光進銅退削弱 M8、M9 需求。第三個是擴產吃掉現金，營收達標但每股自由現金流沒有跟上。最大回撤估 −45% 至 −70%：現價是 104 週均線的 2.3 倍、250 週均線的 4.6 倍，回到 104 週均線約跌 56%。陷阱風險判黃，因為亮了兩項衰退訊號。重大事件面乾淨：公平會處分 0 筆，近 12 個月重大訊息沒有併購、訴訟、裁罰或重編。","fact_refs":["f_ma_w52","f_ma_w104","f_ma_w250","f_kpi5","f_peer_2383_tw_fcf_margin_pct","f_kpi1_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"把週期高點獲利當常態的風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":118.64,"pe":42.61,"basis":"FY2026E 共識每股盈餘（Koyfin 快照換算新台幣）；終端倍數同樣用當年度每股盈餘"},"eps":{"bull":[250,380,450,500,540],"base":[215,290,310,320,335],"bear":[195,160,120,125,135]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.5,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"max_dd":{"lo":-70,"hi":-45,"basis":"現價 5,055 元是 104 週均線（2,212 元）的 2.3 倍、250 週均線（1,089 元）的 4.6 倍。上緣 −45%：報價停漲，倍數由 FY2027 的 21 倍壓到約 12 倍。下緣 −70%：報價反轉，每股盈餘回落到 120–135 元並只給 11–12 倍，深於 Bear 終值跌幅約 −60%。歷史最大回撤事實表未涵蓋，以均線距離與 Bear 推算代替","trigger_time":null},"basis":{"bull":"M9 在 2027 年放量，拿下輝達與 Google 新平台主供；2027 年底 945 萬張產能全數消化，2028 年追上共識 380 元，之後年增約 10%。終端 24 倍，參照現價 FY2027 共識約 21.5 倍再給成長溢價","base":"2027 年價量齊揚但略低於共識（215 元）；2028 年新產能開出、報價持平，290 元；之後隨 AI 需求個位數成長。終端 20 倍，低於現價 FY2027 共識倍數，反映週期高點折價；同業本益比事實表未涵蓋，無同業對照","bear":"2027 年仍有訂單支撐（195 元）；2028 年全產業新產能開出加上光進銅退，報價反轉，毛利率回到 2023–2025 年 27–30% 區間，每股盈餘回落到 120–135 元。終端 15 倍，取成長率降到 10% 的熄火情境。機率 35%：共識成長超出內生上限，產業處擴張後段且全產業擴產；業界供不應求至 2028 年的說法只採信到 2027 年，因為它是產業自述，且同時有大量擴產"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"業界稱供不應求至 2028 年，但公司 2027 年底產能要到 945 萬張，同業也在擴產；今年成長以漲價為主","assumption":"高階 CCL 報價與 33% 以上的毛利率能撐到 2028 年","consequence":"報價反轉時每股盈餘回落到 120–135 元、倍數壓到 15 倍，五年後股價約 2,000 元，虧損約六成","ruling":"採納：Bear 機率給 35%，並把高階報價設為唯一致命點","watch":"單季毛利率、月營收年增率、上游銅箔與玻纖布交期","evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","supply_demand_durability#4","end_markets#2"],"fact_refs":["f_kpi1_gaap","f_consensus_eps_fy3"]},{"view":"論點失敗","evidence":"市場擔心光進銅退削弱 M8、M9 需求；法說稱客戶產品轉換初期，舊產品掉得比新產品長得快","assumption":"M9 在 2027 年放量能接上 M8，且光學共封裝五年內不會大量取代板上高速銅傳輸","consequence":"高階材料需求被壓縮時，份額再高也是在縮小的市場","ruling":"部分採納：替代程度與時點事實表未涵蓋，不硬套進基本情境，列為 Bear 成因之一並設減碼條件","watch":"主要 AI 平台是否公開採用光學共封裝；基礎建設營收占比","evidence_refs":["substitute_technology#0","substitute_technology#1","supply_demand_durability#2"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年資本支出約 320 億元（券商轉述）；第二季自由現金流 −28.4 億元，TTM 自由現金流率 −2.9%；2024、2025 年自由現金流只有淨利的 14%；股息約 90 億元，高於 2025 年自由現金流 20.9 億元；股數每年增約 1.7%","assumption":"營收照共識成長時，股東每股自由現金流也會同步成長","consequence":"成長被擴產吃掉；若產能開出時報價已反轉，新資本的報酬會遠低於推算的約 44%","ruling":"採納：資本配置評為偏弱，長期信心上限為中；以 2027 全年自由現金流轉正作驗證","watch":"全年自由現金流、存貨天數、股數","evidence_refs":["capital_markets_pricing#2","geo_supply_chain#2"],"fact_refs":["f_kpi5","f_kpi6_2026","f_peer_2383_tw_fcf_margin_pct","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"Trailing 本益比 79.4 倍，是四個年度端點最高；FY2026 共識 42.8 倍，FY2027 約 21.5 倍；股價是 250 週均線的 4.6 倍","assumption":"市場會在 2027 年獲利翻倍時仍給 20 倍以上","consequence":"基本情境五年年化約 6%，獲利達標也只拿到普通報酬","ruling":"採納：不追，等股價回到 4,300 元以下。反方是共識三個月上修 23%，若續上修，等待可能錯過；接受這個代價","watch":"共識修正方向、FY2027 本益比","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_ma_w250"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 5070.0 → 本次 5055.0（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=5070.0","side_b":"本次 price_at_dd=5055.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 5,070 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 5,070 元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 5,070 元：Bull 價 12,960、Bear 價 2,025，五年期望值 +24.6%，基準年化 5.7%，不對稱比 1.48","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.48。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 5,070 元：五年期望值 +24.6%，基準年化 5.7%，不對稱比 1.48","side_b":"本次情境、股價 5,055 元：五年期望值 +24.9%，基準年化 5.8%，不對稱比 1.49","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.4 個百分點，基準年化多 0.1 個百分點，不對稱比由 1.48 升到 1.49。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與綜合結論","cause":"新證據","prior_field":["val","signal","trap"],"side_a":"前份（2026-06-01，股價 5,070 元）估值判最貴一級，綜合 B，陷阱風險黃","side_b":"本次股價 5,055 元幾乎沒動，但 FY2026 共識每股盈餘三個月內由 96.31 元上修到 118.64 元（+23.2%），第二季毛利率 33.85% 優於預期。估值改判偏貴（下修一級），綜合維持 B，陷阱風險維持黃（獲利成長遠快於營收、自由現金流對淨利連兩年低於 0.75，兩項亮燈）","ruling":"估值下修一級屬新證據：同樣價格買到更高的近年獲利。綜合結論不變，因為基本情境五年年化約 6% 仍弱","evidence_level":"公司財報加共識快照","settle_metric":"2026 第三、四季每股盈餘合計是否達 76 元（FY2026 共識 118.64 元減上半年 42.45 元）","if_then":["若第三、四季每股盈餘合計 ≥76 元且第四季毛利率 ≥34%，則維持本次估值判斷，等待價位上調到 4,600 元","若合計 <68 元（低於共識一成），則估值回判最貴一級，維持不追"],"evidence_refs":["capital_markets_pricing#2","end_markets#0"]},{"axis":"新增判斷欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份沒有產出護城河趨勢、成長跑道、公司類型、循環位置、情境機率與最大回撤（欄位為空）","side_b":"本次首度給出：護城河擴大、跑道中等、以循環／商品為主、中循環、機率 20／45／35、最大回撤 −45% 至 −70%；定期定額欄位本次不產出","ruling":"屬方法變動，沒有前值可比，不代表基本面改變","evidence_level":"方法說明","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics"],"side_a":"前份未設重啟條件，也未設減碼與清倉門檻","side_b":"重啟：股價 ≤4,300 元且單季毛利率 ≥32%。減碼：單季毛利率連兩季 <28%，或公告調降高階報價。清倉：毛利率 <28% 且確認落選下一代平台","ruling":"新流程要求明列門檻，故新增。毛利率 28% 取自 2023–2025 年 27.4–29.8% 區間的中段，代表報價回到漲價前的水準","evidence_level":"公司年報毛利率歷史","settle_metric":"單季毛利率","if_then":["若單季毛利率連兩季 <28%，則減碼至半倉","若毛利率 <28% 且確認落選下一代輝達平台，則清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"Single Thing：公司或主要同業公告調降 M7 以上高階 CCL 報價","ruling":"高階報價是 2026–2028 年獲利最大的單一敏感項（今年成長以價為主），所以設為唯一致命點","evidence_level":"法說與財報","settle_metric":"每季法說報價說法與單季毛利率","if_then":["若公告調降，則減碼至原倉位一半","若報價續漲且毛利率 ≥34%，則維持唯一致命點設定，機率下修到 15%"],"evidence_refs":["end_markets#2"]},{"axis":"前份假設與風險改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份 H3 是估值假設（前瞻本益比 30 倍以上能維持）；風險列漲價循環反轉、最先進節點份額流失、材料路線分散","side_b":"本次估值改放在情境樹，不再當假設；H3 改為擴產能否轉成每股自由現金流；風險新增光進銅退與擴產燒現金，最先進節點份額流失保留為短期風險","ruling":"估值不是公司要證明的事，移到情境樹；擴產燒現金是本次新增的財報證據（第二季自由現金流為負）","evidence_level":"方法變動加公司財報","settle_metric":"2027 全年自由現金流","if_then":["若 2027 全年自由現金流 <0 且存貨天數 >75 天，則停止加碼"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"最先進平台份額","cause":"新證據","prior_field":["R2"],"side_a":"前份風險：最先進節點份額流失給斗山，前一代已失、下一代待定","side_b":"第二季後法人稱下半年兩家客戶新平台放量，M8／M8+／M9 出貨攀升，並看好公司超越斗山成為輝達最大 CCL 供應商；Prismark 稱 2025 年全球營收排名升到第一","ruling":"部分緩解但未證實：來源是法人看法與搜尋摘要，不是供應商名單；保留為一到兩季的短期風險","evidence_level":"媒體轉述加法人看法（未讀原頁）","settle_metric":"下一代輝達平台材料供應商名單與 2027 上半年月營收","if_then":["若確認為下一代平台主要供應商且 2027 第一季營收季增，則護城河趨勢維持擴大","若確認落選，則減碼至半倉，護城河趨勢改判持平"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#0","competitive_share_entrants#1","capital_markets_pricing#2"]},{"axis":"2028 年供需與共識獲利","cause":null,"prior_field":null,"side_a":"業界稱中高階 CCL 至 2028 年仍供不應求，訂單能見度到 2027 年；共識 FY2028 每股盈餘 379.84 元，隱含價量續揚","side_b":"全產業同步擴產（公司 2027 年底 945 萬張，台燿擴大交換器份額），加上光進銅退可能削弱 M8／M9 需求；今年成長以漲價為主，而報價最容易反轉","ruling":"可調和，屬程度差異：供給到 2028 年仍緊與漲價幅度收斂可以同時成立。基本情境 FY2028 每股盈餘 290 元，低於共識約 24%；依據是共識三年年複合約 110%，遠超內生上限約 38%，差額全靠漲價與利潤率擴張，這類成長最容易逆轉","evidence_level":"產業自述與媒體轉述，對上財報推算","settle_metric":"2027 下半年高階 CCL 報價與單季毛利率","if_then":["若 2027 第二季單季毛利率 ≥34% 且公司再漲價，則基本情境上修到共識，等待價位上調到 5,000 元","若 2027 任一季毛利率季減 ≥2 個百分點且月營收年增跌破 20%，則減碼至半倉並停止加碼"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","substitute_technology#0","competitive_share_entrants#2","end_markets#2","channel_business_model_shift#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 共識本益比約 21.5 倍，對應每股盈餘翻倍、產能賣到 2027 年、份額全球第一；共識三個月上修 23%，RSI 43.5 不過熱，週線多頭排列","side_b":"21.5 倍的分母是週期高點獲利；若 2028 年報價反轉，Bear 終值約 2,025 元；基本情境五年年化約 6%","ruling":"不追，等價格。價差不夠大，現在買進要靠 2028 年後高峰獲利延續，而這正是我們不信的部分","evidence_level":"財報、共識與價格資料","settle_metric":"股價與單季毛利率","if_then":["若股價先跌到 4,300 元以下而毛利率仍 ≥32%，則分批反買首倉","若股價續漲但 2027 上半年毛利率與報價沒有再上升，則不追"],"evidence_refs":["end_markets#1","supply_demand_durability#3"]}],"triggers":[{"n":1,"text":"月營收年增率是否延續價量齊揚","type":"假設驗證","maps_to":"H1","metric":"月營收年增率","threshold":"2027 上半年每月年增 ≥30%","action":"符合即續抱；連兩個月 <15% 則停止加碼","source_freq":"每月（公開資訊觀測站，次月 10 日前）","date":null,"evidence_refs":["end_markets#0"]},{"n":2,"text":"高階 CCL 報價下調","type":"Single Thing","maps_to":"H1","metric":"M7 以上 CCL 報價","threshold":"公司或主要同業公告調降","action":"減碼至原倉位一半","source_freq":"每季法說加產業報導","date":null,"evidence_refs":["end_markets#2"]},{"n":3,"text":"光進銅退侵蝕高階材料需求","type":"風險","maps_to":"R2","metric":"基礎建設營收占比","threshold":"主要 AI 平台公開採用光學共封裝取代板上銅傳輸，且基礎建設占比跌破 60%","action":"減碼至半倉","source_freq":"每季法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":4,"text":"股價回到可接受區間","type":"估值rearm","maps_to":null,"metric":"股價與單季毛利率","threshold":"股價 ≤4,300 元且單季毛利率 ≥32%","action":"分批建首倉","source_freq":"每日股價加每季財報","date":null},{"n":5,"text":"報價反轉加上平台落選","type":"清倉","maps_to":"R1","metric":"單季毛利率加下一代平台供應商名單","threshold":"單季毛利率 <28%，且確認未列入下一代輝達平台主要供應商","action":"清倉","source_freq":"每季","date":null,"evidence_refs":["competitive_share_entrants#2"]},{"n":6,"text":"擴產燒掉的現金沒有轉回","type":"風險","maps_to":"R4","metric":"全年自由現金流與存貨天數","threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天","action":"停止加碼","source_freq":"每季現金流量表","date":"2028-03-31","evidence_refs":["capital_markets_pricing#2"]},{"n":7,"text":"全年財報與 2027 擴產進度複審","type":"複審日期","maps_to":null,"metric":"FY2026 每股盈餘與 2027 資本支出","threshold":"FY2026 每股盈餘偏離共識 118.64 元超過 ±10%","action":"偏離超過門檻即重跑研究","source_freq":"年度","date":"2027-03-31"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連兩季 <28%","window":"2027Q1–2027Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月 <0%","window":"2026-11 至 2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"M7 以上高階 CCL 報價","bear_threshold":"公司或主要同業公告調降","window":"未來 24 個月","source":"法說會與產業報導","last_status":"ok"},{"metric":"全年自由現金流與存貨天數","bear_threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天","window":"FY2027","source":"年報現金流量表","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤4,300 元（約 2027 年基本情境每股盈餘 215 元的 20 倍）且單季毛利率 ≥32%","exec_line":"觸發後先建首倉，2027 第一季毛利率與產能爬坡確認後再加到標準倉位；Single Thing 發生即減碼一半，報價反轉加上平台落選即清倉"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 4,300 元以下（約 2027 年基本情境每股盈餘 215 元的 20 倍），或 2027 上半年單季毛利率守住 33% 且月營收年增 ≥30%","qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=29.45, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 高速材料需求加上漲價，2027 年營收與毛利率續創新高","2y":"2027 年營收 ≥2,860 億元（共識 3,367 億元的 85%），且單季毛利率 ≥32%","5y":"2026–2030 年平均毛利率 ≥30%，高於 2023–2025 年 27–30% 區間","10y":null,"threshold":"單季毛利率 ≥32%；2027 上半年月營收年增 ≥30%","source":"公司季報、公開資訊觀測站月營收","drift_rule":"毛利率連兩季低於門檻 5% 以上（<30.4%）為削弱，連三季低於門檻 10% 以上（<28.8%）為反轉"},{"id":"H2","text":"守住並擴大 AI 平台高速材料份額，M9 在 2027 年放量接棒","2y":"列名下一代輝達與 Google 平台的主要材料供應商","5y":"高速材料份額 ≥35%（公司自述現為 38.6%）","10y":"下一世代材料（含光學共封裝時代的基板材料）仍居前二","threshold":"高速材料份額 ≥35%；M9 在 2027 年放量","source":"公司法說、Prismark 排名、供應鏈報導","drift_rule":"確認落選任一主力客戶下一代平台即為削弱；兩家都落選或份額跌破 35% 即為反轉"},{"id":"H3","text":"擴產能轉成每股自由現金流，新增資本維持高報酬","2y":"2027 年底產能達 945 萬張，2027 全年自由現金流 ≥0","5y":"2026–2030 年累計自由現金流 ≥累計淨利的 40%，營業利益率 ≥22%","10y":null,"threshold":"2027 全年自由現金流 ≥0；營業利益率 ≥22%","source":"年報現金流量表、股東會產能說明","drift_rule":"TTM 自由現金流連四季為負為削弱；連六季為負且營業利益率 <22% 為反轉"}],"R":[{"id":"R1","text":"AI 資本支出降速加上全產業擴產，高階 CCL 報價反轉","h_ref":"H1","clock":"🔥","threshold":"單季毛利率較高點下滑 ≥3 個百分點連兩季，或月營收年增連三個月轉負","evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","end_markets#2"]},{"id":"R2","text":"光進銅退削弱 M8、M9 高階材料需求","h_ref":"H2","clock":"🐢","threshold":"主要 AI 平台公開採用光學共封裝取代板上銅傳輸，且基礎建設營收占比跌破 60%","evidence_refs":["substitute_technology#0","substitute_technology#1","supply_demand_durability#2"]},{"id":"R3","text":"下一代平台份額流失給斗山或台燿","h_ref":"H2","clock":"⚡","threshold":"下一代輝達或 Google 平台確認未列主要材料供應商","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"id":"R4","text":"擴產高峰撞上報價反轉，資本支出吃掉現金流","h_ref":"H3","clock":"🔥","threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天（第二季為 64.3 天）","evidence_refs":["capital_markets_pricing#2","geo_supply_chain#2"]}],"single_thing":{"description":"公司或主要同業公告調降 M7 以上高階 CCL 報價","why_fatal":"今年成長以漲價為主，毛利率由 2025 年 29.8% 升到第二季 33.9%。報價下調會同時壓低價格與毛利率，2027–2028 年每股盈餘路徑會從共識的翻倍變成持平，而現價已經含了 2027 年獲利翻倍","if_happens":"減碼至原倉位一半；毛利率跌破 28% 且下一代平台落選即清倉","how_monitor":"每季法說的報價說法、月營收相對產能的比值、單季毛利率、上游 HVLP 銅箔與低介電玻纖布交期","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.45,"peg_fy2":0.35,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":40.81,"FY2026E":118.64,"FY2027E":235.66,"FY2028E":379.84},"fy_end_month":12,"eps_basis":"IFRS 稀釋每股盈餘；共識取 Koyfin 快照美元值，按 32.3269 換算新台幣"},"catalysts":[{"date":"2026Q4","date_precision":"quarter","type":"guidance","event":"第三季財報與法說（確切日期事實表未涵蓋）","impact":"高","watch":"第三季毛利率是否再升，以及 2027 年報價與擴產說法"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"美國加州 Arlon EMD 擴建預計年底營運；第四季產能升到 610 萬張（法人）","impact":"中","watch":"第四季月營收是否跟上產能"},{"date":"2027","date_precision":null,"type":"product","event":"M9 材料放量（法說稱 2027 年，季別未定）","impact":"高","watch":"M9 出貨與高階材料占比"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"總產能達 945 萬張目標","impact":"高","watch":"新產能開出時報價能否守住"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）、reg_tariff_export（關稅／出口管制）（尾部風險或事件型，不擋）。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
