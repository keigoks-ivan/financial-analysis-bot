你是 DD 管線 v20 的判斷層閘（gate），標的 BKNG（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜GAAP 營收＝8893 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi1_adjusted_non_gaap_ftc`（q1_business）｜Adjusted 營收（non-GAAP，加回 FTC 沖減）＝9793 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi2_adjusted_ebitda`（q1_business）｜Adjusted EBITDA＝4607 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝38.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi8_room_nights`（q1_business）｜間夜數（room nights）＝345 百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi9_gross_bookings`（q1_business）｜總預訂額（gross bookings）＝54.5 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi10_q4_2026`（q1_business）｜管理層指引：Q4 2026＝room nights +1%~+3%；gross bookings +2%~+4%（固定匯率 +4%~+6%）；adjusted 營收 0%~+2%（固定匯率 +2%~+4%）；adjusted EBITDA 約持平 YoY YoY｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未查
- `f_peer_bkng_operating_margin_pct`（q2_moat）｜BKNG 營業利益率＝32.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bkng_fcf_margin_pct`（q2_moat）｜BKNG FCF 利潤率＝32.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_expe_operating_margin_pct`（q2_moat）｜EXPE 營業利益率＝18.39 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_expe_fcf_margin_pct`（q2_moat）｜EXPE FCF 利潤率＝23.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_tcom_operating_margin_pct`（q2_moat）｜TCOM 營業利益率＝18.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TCOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_trip_operating_margin_pct`（q2_moat）｜TRIP 營業利益率＝3.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRIP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_trip_fcf_margin_pct`（q2_moat）｜TRIP FCF 利潤率＝-1.18 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRIP.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_abnb_operating_margin_pct`（q2_moat）｜ABNB 營業利益率＝20.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abnb_fcf_margin_pct`（q2_moat）｜ABNB FCF 利潤率＝36.93 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.41 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.29 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝14.35 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝28620.09 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（26 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝31547.68 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（35 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_fcf_non_gaap`（q4_capital）｜自由現金流（FCF，non-GAAP）＝1069 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi6_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝4.2 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Exhibit 99.1，2026-11-03）https://www.sec.gov/Archives/edgar/data/0001075531/000107553126000044/q3-26bkngearningsrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝5505.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 21319.0、現金 15814.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝743.7 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.023 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝160.66 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.43 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 10.41，分子＝快照價 160.66｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝17.43 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.38 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 10.45 → 10.41（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.25 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.49 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（12.35 → 12.29）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：Google 將旅遊搜尋整合進 Maps 與 Gemini，其他大型科技平台與 AI 原生業者正開發可直接搜尋、比價、訂位的 Gen AI 助理，可能減少直接流量並使 OTC 被繞過；Gen AI 亦降低進入門檻。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K：部分對手願意零利潤或虧損以搶份額，亞洲尤其盛行折扣與優惠券，折扣會壓低 ADR 與營收占訂單比。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：2026-09 下旬 Meta 個人 AI 代理 Muse 被報導可直接與航空公司或飯店完成訂位，Booking 股價當日跌約 5%，Expedia 跌 7%、Airbnb 跌 6%。
  - 來源：24/7 Wall St. 報導 Muse（as_of 2026-09-23）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：BKNG 全年展望假設高機票價、部分航線運力受限與長程國際需求偏弱會持續（Q2 2026 報導）
  - 來源：Booking Holdings Q2 2026 coverage (finviz)（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：BKNG 10-Q：中東衝突直接影響已大致正常化，但機票價格偏高的間接影響仍壓抑長程國際需求
  - 來源：Booking Holdings 10-Q FY2026 (Q3)（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K FY2025 揭露 Booking.com 受各國競爭主管機關調查（合約平價、定價工具、排名標準），已以承諾改變平價、排名資訊與價格顯示做法了結部分案件；並因 DMA gatekeeper／DSA VLOP 指定而受額外規範，已依 DMA 取消歐洲經濟區平價條款
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：2026 年 7 月 FTC 幕僚告知 Priceline 擬建議提起訴訟（揭露、費用、帳單等不公平或欺騙性做法，屬消費者保護而非反壟斷）；公司於 Q3 2026 認列營收減項 9 億美元及應計損失 1 億美元，尚未和解
  - 來源：Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述（as_of 2026-09-30）｜affects：thesis.R、valuation、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：西班牙 CNMC 2024 年裁罰並限制平價條款與排名標準；公司已入帳負債 4.76 億美元，西班牙國家法院裁定上訴期間暫停執行
  - 來源：Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述（as_of 2026-09-30）｜affects：thesis.R、valuation
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：義大利 AGCM 2026 年 4 月對 Booking.com 啟動調查（付費能見度／偏好夥伴排名）；瑞士 2025 年命令降低佣金、上訴中；希臘 2025 年 6 月啟動正式調查
  - 來源：Booking Holdings 10-Q（2026-09-30）經搜尋摘要引述（as_of 2026-09-30）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#5`（regulatory_antitrust｜方向 -｜狀態 ok）：希臘競爭委員會就 Booking 濫用優勢地位案，異議聲明與救濟措施聽證（12/28）
  - 來源：MLex（as_of 2026-10-29）｜affects：thesis.R、triggers
- `regulatory_antitrust#6`（regulatory_antitrust｜方向 -｜狀態 ok）：歐盟執委會調查 Booking.com 詐欺防制（德文報導，未核實）
  - 來源：goldesel.de（as_of 2026-10-21）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Q1 2026 10-Q：中東衝突造成全球地緣與總經擾動，直接衝擊中東及歐亞等旅遊走廊，取消增加、新訂單成長放緩。
  - 來源：Booking Holdings 10-Q Q1 FY2026 (SEC)（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026 10-Q：區域直接影響於 6 月大致正常化，但仍有間接影響（機票價格高、國際航線運能減少、長程需求下降）；Q3 10-Q 指長程需求疲弱仍壓低間夜成長。
  - 來源：Booking Holdings 10-Q Q2 FY2026 (SEC)（as_of 2026-07-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因素：硬體放在全球託管設施，災難復原計畫未必涵蓋所有區域；第三方服務商合約通常不提供服務中斷追索權。搜尋未見「單點失效」字樣或具名雲端供應商。
  - 來源：Booking Holdings 10-K FY2023 (SEC)（as_of 2024-02-23）｜affects：thesis.R
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Q4 2026 guidance: room nights +1% to +3%, gross bookings +2% to +4% (4%-6% constant currency); management cited Middle East disruption, higher airfares, localized European unrest and softer international travel late in Q3, assumed to persist through year-end
  - 來源：Booking Holdings Q3 2026 earnings release (8-K)（as_of 2026-11-03）｜affects：thesis.R、decision_inputs.bear、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：2026-09-23 Meta 推出可不經 OTA 直接訂機票/飯店的個人 AI agent，BKNG 當日跌約 5%，Goldman 警告此類 agent 可能衝擊仲介型業務。
  - 來源：247WallSt｜Travel booking stocks tumble as Muse threatens to bypass them（as_of 2026-09-23）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：FY2025 10-K：2025年平均績效行銷ROI小幅下滑，原因為付費流量組合變化與社群媒體支出增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026（2026-11-03 公布）：room nights +7%、gross bookings +10%，報告營收 -1%（FTC 相關約 $9 億營收減項）；Q4 指引 room nights +1%~3%、調整後 EBITDA 約持平，管理層稱季末旅遊需求略降溫；全年指引大致不變。（搜尋摘要轉述，未核原文）
  - 來源：Finviz/247wallst/Booking Q3-26 earnings release 搜尋摘要（as_of 2026-11-03）｜affects：thesis.R、valuation、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Booking.com 於 2026-04 確認訂房資料遭未授權第三方存取（姓名、聯絡方式、訂房細節），稱未涉及付款資料、已重設訂位 PIN。
  - 來源：BleepingComputer：New Booking.com data breach forces reservation PIN resets（as_of 2026-04-13）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Q3 2026 10-Q 揭露：2026-10 歐盟執委會對 Booking.com 啟動 DSA 調查；2026-07 FTC 員工告知 Priceline 擬建議提起訴訟；2026-04 義大利競爭暨消費者局啟動調查；西班牙 CNMC 罰款上訴中、已認列約 4.72 億美元負債。
  - 來源：SEC EDGAR 10-Q（2026-09-30）及 10-Q（2026-06-30）（as_of 2026-10-31）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2026 Q1 10-Q：兩個荷蘭基金會代表歐洲飯店與消費者提出競爭法／消費者索賠；Booking 表示將抗辯。
  - 來源：SEC EDGAR 10-Q（2026-03-31）（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：無實體產品召回；2026-04 Booking.com 資料外洩事件，公司重設訂位 PIN。
  - 來源：BleepingComputer：New Booking.com data breach forces reservation PIN resets（as_of 2026-04-13）｜affects：moat_trend

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":432.0,"bear_5y_price":119.7,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":83.9,"ev5y_pct":72.3,"irr_base_pct":13.0,"asym_ratio":5.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.41,"pe":15.43,"basis":"FY1（FY2026E）共識調整後 EPS，終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[12.6,15.0,17.6,20.6,24.0],"base":[11.9,13.7,15.6,17.6,19.7],"bear":[10.3,10.6,10.9,11.1,11.4]},"pe":{"bull":18,"base":15,"bear":10.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.023,"net_buyback":6.5},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BKNG_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Ewout Steenbergen｜guidance：Q3 guidance: room nights +3% to 5%; gross bookings, revenue, adj. EBITDA each +4% to 6%.（原話："expect third quarter room nights to increase between 3% and"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Full-year reported guidance: GB, revenue, adj. EBITDA each up high single digits.（原話："to each be up high single digits and for adjusted EPS"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Adj. EPS full-year guidance is low to mid-teens growth; GB expectation lowered vs prior.（原話："Our expectation for gross bookings is lower than our prior"）
- 2026-08-04｜Ewout Steenbergen｜guidance：GB cut is attributed to flight ticket growth; accommodation outlook unchanged.（原話："primarily due to lower flight ticket growth"）
- 2026-08-04｜Ewout Steenbergen｜guidance：FX assumed to add to full-year reported growth.（原話："we estimate changes in FX will positively impact full year"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Guidance assumes stable travel environment.（原話："Our guidance assumes stability in the broader travel"）
- 2026-08-04｜Ewout Steenbergen｜guidance：Full-year guidance in line with long-term algorithm, assuming 7 of 12 months Middle East impact.（原話："that is still in line with our long-term algorithm"）
- 2026-08-04｜Ewout Steenbergen｜risk：Guidance assumes 7 of 12 months of Middle East impact.（原話："we have 7 out of 12 months impact of the Middle East"）
- 2026-08-04｜Ewout Steenbergen｜risk：Q2 Middle East impact was said to be a bit higher than Q1's ~2 point impact.（原話："the impact was actually a bit higher"）
- 2026-08-04｜Ewout Steenbergen｜risk：Q3 Middle East impact expected a bit smaller than Q2 on normalization.（原話："we expect that there will be a little bit less of an impact"）
- 2026-08-04｜Glenn Fogel｜risk：Long-haul international travel pressured by airline prices and capacity.（原話："international travel remained pressured by elevated airline"）
- 2026-08-04｜Ewout Steenbergen｜risk：Booking window and length of stay contracted globally in Q2.（原話："we saw a modest contraction in booking window and length"）
- 2026-08-04｜Ewout Steenbergen｜margin：Adj. EBITDA margin expansion in Q2.（原話："Adjusted EBITDA margin expanded nearly 40 basis points"）
- 2026-08-04｜Ewout Steenbergen｜margin：Marketing expense grew faster than gross bookings.（原話："Marketing expense increased 11% year-over-year, modestly"）
- 2026-08-04｜Ewout Steenbergen｜margin：Revenue growth below GB growth, explained by March cancellations.（原話："Revenue growth was lower than gross bookings growth"）
- 2026-08-04｜Ewout Steenbergen｜margin：Adj. EPS growth outpaced EBITDA growth with lower share count.（原話："Adjusted EPS of $2.54 per share increased 15%"）
- 2026-08-04｜Ewout Steenbergen｜margin：Transformation savings target raised from $550M to $650M.（原話："increasing our expected annual run rate savings from"）
- 2026-08-04｜Ewout Steenbergen｜margin：Additional $100M savings mostly from procurement, existing categories.（原話："mostly came from the procurement work stream"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：Q2 debt raised and repaid.（原話："raised $3 billion of debt, paid down $1 billion of debt"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：H1 2026 buybacks of $7.4B.（原話："repurchased $7.4 billion of our common stock"）
- 2026-08-04｜Ewout Steenbergen｜capital_allocation：Capital allocation framework stated.（原話："We remain committed to a disciplined capital allocation"）
- 2026-08-04｜Glenn Fogel｜commitment：Management says it does not want surprise AI spending; return or stop.（原話："What we do not want is any surprise"）
- 2026-08-04｜Ewout Steenbergen｜commitment：Management states AI ROI already positive.（原話："already seeing an ROI that is positive on our AI investments"）
- 2026-08-04｜Glenn Fogel｜customer：Genius level 2/3 share of room nights.（原話："accounted for a high 50% share of room nights"）
- 2026-08-04｜Glenn Fogel｜customer：U.S. room nights growth in Q2.（原話："U.S. room nights grew in the high single digits"）
- 2026-08-04｜Ewout Steenbergen｜customer：Connected Trip transactions growth.（原話："Connected Trip transactions grew low double digits"）
- 2026-08-04｜Ewout Steenbergen｜customer：Merchant share of gross bookings.（原話："approximately 73% of total gross bookings"）
- 2026-08-04｜Ewout Steenbergen｜customer：Flight tickets growth in Q2.（原話："flight tickets increased 4% year-over-year"）
- 2026-08-04｜Glenn Fogel｜customer：Alt accommodation growth; wants higher especially in U.S.（原話："4% growth in alternative accommodations, well, I'd like that"）
- 2026-08-04｜Ewout Steenbergen｜competition：SEO described as small component under pressure.（原話："SEO remains a small component of our overall room"）
- 2026-08-04｜Glenn Fogel｜competition：Google AI overview pressured SEO.（原話："Putting in that AI overview probably has done it."）
- 2026-08-04｜Ewout Steenbergen｜competition：LLM traffic share of room nights.（原話："of our room nights. And that hasn't moved so much recently."）
- 2026-08-04｜Ewout Steenbergen｜competition：Booking is in OpenAI CPC test group.（原話："part of the test group of OpenAI for CPC."）
- 2026-08-04｜Glenn Fogel｜competition：Google agentic booking launch with Booking among first.（原話："of our room nights. And that hasn't moved so much recently."）
- 2026-08-04｜Glenn Fogel｜competition：Google moved toward performance marketing ad platform.（原話："performance marketing advertising platform"）
- 2026-08-04｜Glenn Fogel｜competition：Asia described as dynamic competitive environment.（原話："Despite a dynamic competitive"）
- 2026-08-04｜Glenn Fogel｜product：AI referrals described as small contributor.（原話："performance marketing advertising platform"）
- 2026-08-04｜Glenn Fogel｜product：Penny usage still very small; no metrics.（原話："it's still very small, and we're not at a stage"）
- 2026-08-04｜Glenn Fogel｜product：Customer service cost per booking decreasing at double-digit rate.（原話："per booking continues to decrease at a double-digit rate"）
- 2026-08-04｜Ewout Steenbergen｜product：AI costs a low single-digit share of tech spend.（原話："low single-digit level of our overall technology spend."）
- 2026-08-04｜Glenn Fogel｜product：B2B units being merged into one.（原話："let's put it together as one unit."）
- 2026-08-04｜Ewout Steenbergen｜product：B2B incrementality discipline vs B2C cannibalization.（原話："cannibalizing your existing B2C business"）

### 問答異常語氣（迴避／改口／保留）
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Mahaney: quantitative evidence AI/Penny improved conversion or bookings per customer?｜答法：Declined to give percentages or CSAT numbers; said still very small.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Kopelman: where did the assumed 300bp Middle East headwind for Q2 end up, and Q3 assumption?｜答法：No bp figure; said Q2 'a bit higher' than Q1 and Q3 'a little bit less'.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Post: why air decelerated and rental cars were down, what it means for Connected Trip｜答法：Answered air only, framed as exogenous; rental cars not addressed.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Walmsley: SEO pressure not called out before; AI search shift or SEM favoring? Traffic going direct to hotels?｜答法：Fogel said 'I don't know, they don't tell me' on hotels; Ewout corrected that SEO was discussed last quarter.
- BKNG_Q2_2026_Earnings_Call_20260804.md｜問：Kopelman: extent of AI discovery testing on Booking.com and learnings｜答法：Said no data yet, gave only impressions.

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 7 | 3 |
| reg_tariff_export | found | 1 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：Booking Holdings 10-K customer concentration no single customer significant percentage of revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260805","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Connected Trip 由敘事變成經濟：跨垂直交易的附著率持續推進，機票／租車／景點由「留客工具」變成自身有利潤的垂直，讓 BKNG 由住宿 OTA 進化為全旅程平台"},{"id":"H2","text":"Agentic commerce 穿過 OTA 而非繞過 OTA：AI 平台把發現層拿走，但結帳與 merchant of record 留在 BKNG，因此 take rate 不被結構性抽稅"},{"id":"H3","text":"低至中雙位數 EPS 複利可維持 5 年：約 7–8% 固定匯率營收成長 × 每年約 40 個基點 EBITDA 利潤率擴張 × 每年約 4% 淨股數縮減"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"發現層通路稅結構化：AI 平台與搜尋引擎把「被看見」變成永久性收費項目。已在動的三條線——Google AI 概覽壓縮自然搜尋（管理層本季正面承認）、OpenAI CPC 廣告位（BKNG 已在測試群）、以及旅館連鎖自有 AI 訂房工具（Hilton「AI Planner」2026-03 上線、Marriott「Ask Bonvoy」2026-06 上線涵蓋約 10,000 家物業／146 國、IHG 2026-07 起可在自家 AI 對話內以點數／現金／混合方式搜尋並訂房）。最後這條是 BKNG 結構上無法對稱回應的——它沒有忠誠度貨幣。"},{"id":"R2","text":"歐洲法律與監理堆疊的追溯性賠償階段：比價條款之爭已由「禁止未來使用」進入「追溯賠償」。柏林第二地方法院於 2025-12-16 判定 1,099 家德國旅館可就 2013–2024 年的窄式最惠條款求償（金額待後續程序認定）；HOTREC 主導的集體訴訟在阿姆斯特丹審理，參與旅館由 2026-01 的 3,087 家增至 2026-07 底的 10,783 家，預計 2026 秋季達約 18,000 家，求償框架約 €8B、涵蓋 2004–2024 年；西班牙 CNMC 的 €413M 罰款雖獲暫緩執行，BKNG 已提存全額財務擔保；瑞士 COMCO 於 2026-04-30 對旅遊業「品牌關鍵字競價互不出價」開啟調查（歐盟執委會有平行調查）。這不是近期盈餘風險，而是把多年法務成本與和解風險制度化，並永久拿掉 BKNG 用契約手段守住 take rate 的工具。"},{"id":"R3","text":"中東衝突再升溫或蔓延：現行指引假設「情況穩定、間接影響持續至第三季末」。若衝突延長至 2027 或蔓延至紅海航運／台海，全球入境流量可再降 10–15%，全年營收成長可能跌至 +3–5%，營運槓桿反轉。聯合國世界旅遊組織已將 2026 年國際入境成長由原估 3–4% 下修 1–2 個百分點；中東入境 2026 年預估下滑 11–27%。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","irr_base_pct":13.5,"ev5y_pct":66.1,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.9,"ev5y_pct":66.1,"irr_base_pct":13.5,"max_dd_pct":-52.0,"bull_5y_price":463.0,"bear_5y_price":126.5,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","price_at_dd":194.27,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BKNG","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Booking Holdings"},"oneliner":"Q3 全面高於指引上緣，LLM 轉介仍遠低於間夜 1%，但 Q4 指引轉弱，FTC 案一次認列 10 億美元。現價約 15.4 倍當年 EPS，只要代理型 AI 沒把獲客成本墊高，EPS 複利就夠回報；真正的賭注是發現層會不會開始抽稅。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺旅宿業者按成交支付的佣金與結帳收入，錢卡在全球需求聚合加付款這一節點，這個位置到本季還沒被繞過。","reasoning":"Q3 總預訂額 545 億美元、間夜 3.45 億、調整後營收 9,793 百萬美元、GAAP 營收 8,893 百萬美元，差額主要是 FTC 相關 9 億美元減項。GAAP 營益率 38.4%，調整後 EBITDA 4,607 百萬美元，毛利率公司未揭露。商家模式占總預訂額 75%，較去年多 3 個百分點。收入分部占比事實表未涵蓋，只能用品類增速代替。單點依賴在流量入口：B2C 直接占比 60% 中段，其餘靠第三方流量，最大來源占比事實表未涵蓋；供應端反而分散，十大連鎖只占 Booking.com 間夜低雙位數。產業位置判擴張期，依據是全球旅遊訂房額預估年增 5.2%、本季間夜 +7%；Q4 間夜指引 +1%～+3% 來自長程航線受阻和全年最難基期，還不算景氣翻轉。反例是 10 月的擾動若延續到 2027 年，這個判斷就要改成收縮。","fact_refs":["f_kpi0_gaap","f_kpi1_adjusted_non_gaap_ftc","f_kpi2_adjusted_ebitda","f_kpi4_gaap","f_kpi8_room_nights","f_kpi9_gross_bookings","f_kpi10_q4_2026"],"verdict_values":{"revenue_quality":"佣金與商家模式收入為主。GAAP 營收含 FTC 相關 9 億美元減項，調整後營收才是營運口徑；法務支出反覆出現，調整後數字要打折看。","unit_econ_note":"成交才收費，旅宿沒有前期成本。Q3 調整後營收占總預訂額約 18.0%，年減約 15 個基點，主因機票占比上升與訂房入住時間差，付款收入部分抵銷。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"輕資產、預收款帶來負營運資金、FCF 利潤率約 33%、EPS 靠大額回購放大"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構性持久，短期壓力屬週期性：Phocuswright 預估全球旅遊訂房額年增 5.2% 至 2027 年；美國飯店供給成長僅 0.4%～0.6%，但全球在建管線創高，供給端長期有回補空間。","bargaining":{"up":"對獨立旅宿議價力強，十大連鎖只占 Booking.com 間夜低雙位數；對流量入口議價力弱，Google、Meta、OpenAI 掌握發現層。","down":"旅客切換成本低，靠 Genius、App 與跨品類留人；二三級會員占間夜 50% 後段。","geo":"歐洲監管最重，DMA 已取消歐洲經濟區平價條款；亞洲折扣競爭盛行。"},"profit_pool_dir":"同業對照只有一期：本公司營益率 32.78%，Expedia 18.39%、Airbnb 20.81%、Trip.com 18.19%、Tripadvisor 3.1%。五年利潤池變化事實表未涵蓋，無法判斷是否流出。","tam_table":[{"item":"全球旅遊訂房額","value":"2027 年約 1.8 兆美元，年增 5.2%（Phocuswright，2025-10）"},{"item":"本公司粗估滲透率","value":"Q3 總預訂額 545 億美元年化約 2,180 億，約 12%；單季年化，未經季節調整"},{"item":"利潤池五年占比變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向判穩定：執行力仍在擴大，定價權被監管和代理通路壓著，兩邊相抵。","reasoning":"機制是雙邊網路加付款與服務能力：獨立旅宿自己做不到全球行銷和一百多種付款方式，旅客靠 Genius 和 App 回流。同業 ROIC 事實表未涵蓋，改用營益率差：本公司 32.78%，高 Expedia 14.4 個百分點、高 Airbnb 12.0 個百分點，但只有一期，看不出擴大或收窄。份額面只有管理層自述美國連三年勝大盤；美國間夜增速由 Q2 高個位數降到 Q3 中個位數，不足以標擴大。執行力判擴大：Q3 四項指標都高於指引上緣，轉型節省目標由 5.5 億美元升到 6.5 億美元，客服成本在量增下減少。定價權判縮減：歐洲平價條款已取消，瑞士命令降佣（上訴中），調整後營收占總預訂額年減約 15 個基點，不過主因是機票占比。AI 的附著點分兩段看：長在自有供給、即時房價和結帳的部分是強化，發現層被拿走的部分是替代。分界年訂在 2028 年底，屆時代理占間夜超過 5% 而 B2C 行銷仍有槓桿就算強化，失去槓桿就算替代。","fact_refs":["f_peer_bkng_operating_margin_pct","f_peer_bkng_fcf_margin_pct","f_peer_expe_operating_margin_pct","f_peer_expe_fcf_margin_pct","f_peer_tcom_operating_margin_pct","f_peer_trip_operating_margin_pct","f_peer_trip_fcf_margin_pct","f_peer_abnb_operating_margin_pct","f_peer_abnb_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"需求聚合加結帳的雙邊網路：旅宿只在成交時付費，旅客靠直接訪問、App 與 Genius 回流。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"B2C 直接占比四季穩定在 60% 中段，Genius 二三級占間夜 50% 後段且年增，App 占比由 50% 中段升到 50% 後段，LLM 轉介遠低於 1%。反向是 2025 年行銷 ROI 小降、調整後營收占比年減 15 個基點、多國監管。沒有份額流失的一手證據，也沒有擴大的量化證據。","competitor_notes":[{"name":"EXPE","strategy_note":"營益率 18.39%、FCF 利潤率 23.09%，都明顯較低；美國份額流向本公司的說法來自二手摘要，未核原文。"},{"name":"TCOM","strategy_note":"營益率 18.19%。亞洲是主要競爭地帶，10-K 指當地折扣盛行，但未點名此公司。"},{"name":"TRIP","strategy_note":"營益率 3.1%、FCF 為負，已不構成定價壓力，只剩流量入口角色。"},{"name":"ABNB","strategy_note":"營益率 20.81%、FCF 利潤率 36.93%，現金轉換高於本公司，是替代住宿的直接對手；本公司替代住宿占 Booking.com 間夜約 37%，Q3 間夜 +7%。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用同期營益率差，且只有一期。","threats":[{"level":"🔴","text":"水平代理與 Gen AI 助理把發現層拿走：Google 整合 Maps 與 Gemini，Meta Muse 可直接訂位。目前代理偏好串接聚合平台，Agoda 也是 Muse 亞洲上線夥伴，但變現模式未定。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"監管壓定價工具：DMA 已取消歐洲經濟區平價條款，義大利、希臘、瑞士對排名和佣金持續調查。賠償金額放在風險段，這裡只計對定價權的影響。","p":"40%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#3"]},{"level":"🟡","text":"部分對手願意零利潤甚至虧損搶份額，亞洲折扣與優惠券盛行，壓低房價和營收占訂單比。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"2025 年績效行銷 ROI 小幅下滑，原因是付費流量組合變化和社群媒體支出增加；B2B 分潤也讓整體行銷連續幾季快於總預訂額。","p":"30%","evidence_refs":["channel_business_model_shift#1"]},{"level":"🟡","text":"2026 年 4 月訂房資料遭未授權存取，公司稱未涉付款資料並重設訂位 PIN，傷害集中在信任，尚未見流量或金額影響。","p":"20%","evidence_refs":["major_events#1","product_recall_warning#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"旅客是使用者和付款者，佣金由旅宿支付。旅遊可延後但長期需求穩定，訂房額預估年增 5.2%。需要留意的是決策者可能由旅客移到代理。"},{"item":"決策層級","level":"🟡","text":"替代性要看單次訂房，旅客隨時能切換。代理變數是 B2C 直接占比 60% 中段、App 占比 50% 後段、Genius 二三級占間夜 50% 後段；水平代理若接手比價，這些黏性會被削弱。"},{"item":"價值鏈分配","level":"🟡","text":"獨立旅宿沒有自建替代方案，對本公司議價力弱；但上游發現層集中在少數科技平台，收費權在擴大。管理層稱代理多家競爭有利條件，變現模式仍未定。"},{"item":"社會容忍度","level":"🔴","text":"佣金與排名已是多國監管標的：瑞士命令降佣，西班牙裁罰並限制平價與排名，DMA 取消平價條款，FTC 案認列 10 億美元。實際定價上限已由監管決定。"}],"roiic":"無法計算：投入資本事實表未涵蓋，商家模式的預收款讓投入資本接近零或為負。","reinvest_rate":"約為零或負：TTM FCF 利潤率 32.84% 不低於營業利益率 32.78%，稅後營業利益更低，代表帳面上沒有淨再投資。","endo_ceiling":8.0,"formula_note":"增量報酬乘再投資率在再投資率為零或負時沒有意義，改用代理上界：管理層固定匯率營收成長目標至少 8%，當作不靠回購與利潤率擴張的有機成長。這是代理值，不是公式結果。反例是 2024、2025 年營收年增 11%、13%，上界可能偏低；但 Q4 固定匯率營收指引僅 +2%～+4%，短期也可能低於 8%。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：粗估滲透率約 12%，跨品類是有數據的第二條曲線；但 EPS 增速有一半以上靠回購與利潤率，不是營收。","reasoning":"滲透率用 Q3 總預訂額年化約 2,180 億美元，對 2027 年約 1.8 兆美元，粗估 12%，未經季節調整。以長期目標 8% 對大盤 5.2%，相對每年多約 2.8 個百分點，到 30% 要超過 20 年。第二條曲線已有數據：跨品類交易年增近 20%，機票 +19%，景點 +24%，不過機票會拉低營收占比。共識 FY2026E→FY2028E EPS 年化 17.4%，高於管理層 15% 目標，也高於我的 Base 13.6%。EPS 共識家數事實表未涵蓋。反例：代理通路若改變份額分配，滲透率推算就失效。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_room_nights","f_kpi9_gross_bookings"],"verdict_values":{"growth":{"driver_mix":"Q3 量 +7%、固定匯率房價約 +3%，機票與其他品類再加一點；EPS 再疊平均股數年減 7.5%。併購可忽略。","runway_years":">20","runway_post_y5":"🟢","endo_ceiling_basis":"代理上界 8%，共識 EPS 年化 17.4%，缺口 9.4 個百分點。約 7 點來自淨回購，約 2.4 點來自利潤率（6.5 億美元轉型節省與營運槓桿），無併購貢獻，缺口可歸因。FY2025 調整後 EPS 事實表未涵蓋，所以只算 FY2026E 到 FY2028E 兩年。","segments":[{"item":"Booking.com 替代住宿","value":"約占間夜 37%，Q3 間夜 +7%，Q2 為 +4%"},{"item":"機票票數","value":"Q3 +19%，Q2 為 +4%"},{"item":"景點票數","value":"Q3 +24%"},{"item":"跨品類交易","value":"年增近 20%，占 Booking.com 交易低雙位數，Q2 為低雙位數成長"},{"item":"分部營收與利潤","value":"事實表未涵蓋；B2B 預計 2027 年起分開揭露"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"公司未揭露毛利率，資料缺口；替代看調整後營收占比，Q3 年減約 15 個基點"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"未見流失的一手證據"},{"signal":"提價後銷量下滑","lit":false,"evidence":"Q3 房價約 +3%，間夜 +7%"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"evidence":"共識 EPS 年化 17.4%，FY2027E 營收年增約 10.2%，差約 7 個百分點"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 1.34 倍，2025 年 1.68 倍"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"evidence":"Q3 換算約 1.6%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"AI 代理仍是潛在威脅，LLM 轉介遠低於 1%"},{"signal":"產業倍數近 3 年系統性下移","lit":true,"evidence":"本公司本益比、P/S、EV/S 都在四個年度端點最低位；同業倍數歷史資料缺口"},{"signal":"維持性資本支出占 FCF 高於 60%","lit":false,"evidence":"資本支出事實表未涵蓋，但 FCF 約等於營業利益，不像高資本負擔"},{"signal":"停止投資且收入 3 年內下滑","lit":false,"evidence":"營收持續成長，投資增加"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置幾乎全押回購，還給股東的現金已超過當期自由現金流，目前有效，但速度不能永遠維持。","reasoning":"FCF／淨利 2023 至 2025 年為 1.63、1.34、1.68 倍，高於 1 的部分有一部分是預收款流入；Q3 FCF 10.69 億美元就因 36 億美元商家預收款季節性回吐而偏低。SBC 占 Q3 GAAP 營業利益 4.2%，換算約占營收 1.6%。現金去向：前九個月回饋 105 億美元，其中回購 95 億美元；併購只有 OpenTable 收購 Libro；資本支出事實表未涵蓋。Q2 舉債 30 億美元、還債 10 億美元；現金及投資由 Q2 的 177 億美元降到 Q3 的 162 億美元。回購均價與 10 年期殖利率事實表未涵蓋，回購是否過關無法驗證。","fact_refs":["f_kpi5_fcf_non_gaap","f_kpi6_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無大型併購，僅 OpenTable 收購 Libro，金額與報酬事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"現價 TTM FCF 殖利率約 7.7%，但回購均價與 10 年期殖利率事實表未涵蓋，無法驗證是否高於門檻。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 約占 Q3 營收 1.6%，Q3 平均股數年減 7.5%，淨稀釋為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；回購金額已寫在判讀，事實表沒有逐年現金去向與回購均價，展開也只能重複同一組數字。"}}}},"q5_valuation":{"verdict":"現價只要求 FY2031 EPS 約 16.5 美元，就能在倍數不變下賺到年化約 10%；這個要求低於管理層目標，我判斷達成機率高於五成，估值偏便宜。","reasoning":"推算：終端 15 倍，股價年化 9% 加股息 1%，五年後價格約 247 美元，對應 EPS 16.5 美元、年化 9.6%。扣掉每年約 6.5% 淨回購，淨利只要年增約 2%～3%。這代表市場已經為 AI 繞過風險定價。賣方平均目標價 232～234 美元是 8 月資料，沒反映 Q3，不用來支持結論。同業倍數事實表未涵蓋，終端倍數只能對照本公司現值 15.43 倍。反例：若 Bear 成真，FY2027 EPS 只有 10.3 美元，現價對應 15.6 倍，並不便宜。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_peer_bkng_fcf_margin_pct","f_ps_current"],"verdict_values":{"valuation":{"basis":"FY1 共識調整後 EPS 的前瞻本益比，輔以 FCF 殖利率","tier":"品質複利","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數或目標價，無法做同級比較；這是資料缺口，不是因為不重要。"},"fwd_pe":15.43,"peg":0.89,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 15.43 倍。PEG 用共識兩年年化 17.4% 為 0.89，用我的 Base 13.6% 為 1.13。TTM FCF 殖利率約 7.7%（FCF 利潤率 32.84% 除以 P/S 4.25），含預收款流入。本益比、P/S、EV/S 都在四個年度端點最低位，但四個點不是五年分位，五年分位資料缺口留空。綜合判便宜；若共識下修到 Base，PEG 回到合理區間，便宜程度會降低。","upside_short_pct":14.3,"upside_mid_pct":31.6,"denominator_disputed":false,"denominator_note":"FY1 調整後 EPS 排除 FTC 9 億美元營收減項與 1 億美元應計，所以用前瞻口徑。監管支出反覆出現，Base 已比共識低 3%～5%。爭點在未來行銷費用率，不在今年的分母。"}}},"q6_how_wrong":{"verdict":"最可能看錯三處：把代理通路的早期順風當長期結果，把法務支出當一次性，把回購撐起的 EPS 當內生成長。","reasoning":"對 Base 終端價約 296 美元的影響：營收年增少 2 點，EPS 少約 9%，股價約 268 美元；淨回購由 6.5% 降到 3%，EPS 少約 17%，股價約 246 美元；營益率少 5 點且倍數降到 12 倍，股價約 200 美元。第三項最大，所以唯一致命點放在代理通路。成長熄火測試以 FY2028 EPS 13.7 美元起算：之後年增 15% 配 16 倍約 333 美元，10% 配 13 倍約 237 美元，5% 配 10 倍約 159 美元，三種情況兩種高於現價。歷史最大回撤事實表未涵蓋。上季法說有五項問答未正面回答，包含 AI 量化成效、中東影響基點與租車，本季只補了 AI 使用者比較數字。","fact_refs":["f_kpi10_q4_2026","f_consensus_rev_fy2_pct","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：獲利品質好，但 EPS 高度依賴回購，估值已連續下移。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.41,"pe":15.43,"basis":"FY1（FY2026E）共識調整後 EPS，終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[12.6,15.0,17.6,20.6,24.0],"base":[11.9,13.7,15.6,17.6,19.7],"bear":[10.3,10.6,10.9,11.1,11.4]},"pe":{"bull":18,"base":15,"bear":10.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.02,"net_buyback":6.5},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"max_dd":{"lo":-50,"hi":-30,"basis":"上緣：Bear 前兩年 EPS 10.3～10.6 美元乘 10.5 倍，約 108～111 美元，約 −31%～−33%，取 −30% 作較輕情況。下緣：極端 Bear 倍數 8.4 倍乘 EPS 9.69 美元，約 81 美元，約 −49%。歷史最大回撤事實表未涵蓋，區間未用實際回撤校準。","trigger_time":null},"basis":{"bull":"代理通路帶來增量並分散流量入口，營收年增約 9%～10%，利潤率每年擴張約 50 個基點，淨回購約 6%；18 倍需要市場相信 AI 風險解除。同業倍數事實表未涵蓋，只能對照本公司現值 15.43 倍。","base":"營收年增約 6.5%～7%，利潤率小幅擴張，股價上升後淨回購降到約 5.5%～6%，EPS 年化 13.6%，比共識 FY2027E、FY2028E 低 3%～5%；15 倍略低於現值，不靠重新評價。","bear":"代理通路開始收費加上監管壓抑，營收年增約 2%，營益率累計下滑約 5 個百分點，回購降到每年約 3%，EPS 年化約 1.8%。成長降到 10% 對應約 13 倍，此路徑成長更低，所以用 10.5 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"10-K 已把 Gen AI 助理列為可能繞過本公司的風險；2026-09-23 Meta Muse 報導後股價當日跌約 5%，Goldman 示警仲介型業務。","assumption":"水平代理會繼續串接聚合平台，不會和旅宿直連，也不會收取高於現行績效行銷的費用。","consequence":"五年虧 50% 最可能的路徑：代理握有決策權，行銷與分潤墊高，營益率少 5 個百分點以上，市場給 8～9 倍，股價約 80 美元。","ruling":"採納為 30% Bear 的主路徑，和唯一致命點是同一件事。本季證據站在多方：LLM 轉介遠低於 1%，管理層引第三方資料稱大部分流量導向本公司，但未獨立驗證。這份證據蓋不到 2028 年後，不能說風險已解。","watch":"LLM 與代理占間夜、B2C 行銷是否有槓桿、B2C 直接占比。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 FTC 相關減項 9 億美元加應計 1 億美元，西班牙已入帳 4.76 億美元，瑞士命令降佣上訴中，荷蘭兩基金會索賠，歐盟啟動 DSA 調查。","assumption":"這些支出屬一次性，不會變成佣金上限。","consequence":"間夜和預訂額照長，但累計賠款和佣金管制把部分成長價值移給旅宿和消費者。前份記錄的約 80 億歐元求償框架本次事實表未再驗證。","ruling":"部分採納。社會容忍度判紅，Base 比共識低 3%～5%，Bear 納入營益率下滑。反駁點是目前已知金額合計約 15 億美元，僅占市值約 1.2%，真正的傷害要看佣金管制會不會擴散。","watch":"歐盟主要市場是否出現佣金上限、累計一次性支出是否超過 30 億美元、FTC 是否正式起訴。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","regulatory_antitrust#5","lawsuit_class_action#1","major_events#2"]},{"view":"論點成功但股東經濟變差","evidence":"前九個月回饋股東 105 億美元，高於 TTM FCF 約 92 億美元；Q2 淨舉債 20 億美元；Q3 平均股數年減 7.5%，約占調整後 EPS 增幅 17% 的四成多。","assumption":"回購速度可以靠 FCF 與適度舉債維持。","consequence":"若預收款回吐或成長放緩壓低 FCF，回購減半，EPS 年增少 3～4 個百分點，共識 17% 的路徑不成立。","ruling":"採納。Base 的回購隨股價上升下修到每年約 5.5%～6%，Bear 降到約 3%。","watch":"平均股數年減幅度、淨負債、商家預收款變化。"},{"view":"價格已反映太多","evidence":"Q4 調整後 EBITDA 約持平且投資增加，但 FY2027E 共識 EPS 仍年增 18%，高於管理層 15% 長期目標，最新快照只下修 0.49%。","assumption":"便宜的結論建立在共識成立。","consequence":"FY2027 EPS 若落在 Base 11.9 美元，現價約 13.5 倍；若落在 Bear 10.3 美元，約 15.6 倍，便宜論證就消失。","ruling":"反駁已反映太多：現價連 Base 都沒完全反映。採納其中一點：共識偏高，2 月前仍有下修風險。已跌幅度本身不算安全邊際。","watch":"2027 年 2 月的年度展望，以及財報後 FY2027E 共識修正。","evidence_refs":["capital_markets_pricing#0","end_markets#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 194.27 → 本次 160.66（-17.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=194.27","side_b":"本次 price_at_dd=160.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 194.27 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 194.27 美元：Bull 價 463、Bear 價 126.5，五年期望值 +66.1%，基準年化 13.5%，不對稱比 3.9","side_b":"本次情境、股價仍用 194.27 美元：Bull 價 432、Bear 價 119.7，五年期望值 +42.5%，基準年化 8.8%，不對稱比 2.66","ruling":"先換情境、股價不動：五年期望值少 23.6 個百分點，基準年化少 4.7 個百分點。不對稱比由 3.9 變為 2.66。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 194.27 美元：五年期望值 +42.5%，基準年化 8.8%，不對稱比 2.66","side_b":"本次情境、股價 160.66 美元：五年期望值 +72.3%，基準年化 13.0%，不對稱比 5.52","ruling":"再換股價、情境不動：起點價下跌 17.3%，五年期望值多 29.8 個百分點，基準年化多 4.2 個百分點，不對稱比由 2.66 升到 5.52。合計五年期望值比前份多 6.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢：代理型 AI 是增量還是繞過","cause":null,"prior_field":null,"side_a":"管理層稱代理偏好串接聚合平台，流量大多導向本公司，通路分散有利經濟條件（2026-11-03，Ewout Steenbergen）；2026-02 財務長也稱去中介不算風險。","side_b":"10-K 自己列為風險，Meta Muse 可直接訂位，Goldman 示警；Marriott、Wyndham 也在推自家代理計畫。","ruling":"裁決為雙向拉鋸。競爭面在惡化，新入口出現，LLM 轉介加速。結構面有利，聚合平台省去代理逐家串接 470 萬家物業，Bernstein 也認為 OpenAI 縮減直接結帳降低去中介風險。其他結構變數是監管，DMA、DSA 可能拖慢水平代理。兩邊方向相反，今天選多方，因為實際數據是 LLM 遠低於 1%、B2C 有行銷槓桿。決勝數據要到 2028 年才足夠，在那之前不稱風險已解。","evidence_level":"一手法說與 10-K 為主，流量分布僅管理層引述第三方資料","settle_metric":"代理占 Booking.com 間夜比重與 B2C 行銷槓桿","if_then":["若代理占間夜達 5% 且 B2C 行銷連 4 季失去槓桿，減碼至半倉，後續兩季未改善就清倉。","若代理占間夜達 5% 而 B2C 行銷仍有槓桿，加碼至滿額。","若股價先漲回 104 週線 192 美元之上而數據未到，不追。","若股價跌破 145 美元而基本面無損，分批反買。"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"Q4 EBITDA 持平、共識偏高、股價在 52 週與 104 週均線之下，監管與 AI 兩條線都未決，沒有必要提前承擔。","side_b":"現價 15.43 倍，Q3 實績高於指引上緣，管理層稱 2027 年上半年訂單健康，淨利只要年增 2%～3% 就有約 10% 年報酬。","ruling":"不賣，但只用首筆部位，加碼凍結到 2 月財報。週線偏空若證實為對，表現會出現在 2027 年指引。","evidence_level":"財報與法說一手資料，2027 訂單為管理層定性說法","settle_metric":"2027 年 2 月的 Q4 間夜與 2027 年調整後 EBITDA 指引","if_then":["若 2 月財報的 2027 年調整後 EBITDA 指引低於中個位數，停止加碼並減碼三分之一。","若 Q4 間夜不低於 +3% 且 2027 年指引不低於高個位數，加碼第二筆。"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層前後說法：中東影響","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Ewout Steenbergen：指引假設旅遊環境穩定，10-Q 稱區域直接影響 6 月大致正常化。","side_b":"2026-11-03 Ewout Steenbergen：10 月再受往返中東的擾動與歐洲局部動亂影響，指引假設直接與間接影響持續到年底。","ruling":"外部因素的歸因不採信也不否定，標為未證、持續監測。預先約定：Q1 2027 若管理層仍以中東解釋，且間夜年增低於 4%，外部因素說法視為不成立，改按需求放緩處理。","evidence_level":"法說與 10-Q 一手資料","settle_metric":"2027 年第一季間夜年增與長程占比","if_then":["若 Q1 2027 間夜年增低於 4% 且仍歸因中東，減碼三分之一。","若 Q1 2027 間夜年增回到 6% 以上，維持持有並恢復加碼資格。"],"evidence_refs":["geo_supply_chain#1","supply_demand_durability#1"]},{"axis":"Q4 指引與 2027 上半年訂單","cause":"新證據","prior_field":null,"side_a":"Q4 間夜 +1%～+3%，調整後 EBITDA 約持平，投資增加。","side_b":"2027 上半年已訂房量管理層稱健康；上季 Q3 間夜指引上緣 5%，實際 7%，總預訂額上緣 6%，實際 10%。","ruling":"屬程度差異，可以調和。不把 Q4 外推成全年趨勢，也不假設一定再超標 2 點。上季超標有基期與中東正常化因素，且 10 月環境確實變差。","evidence_level":"一手財報與法說，訂單狀況未量化","settle_metric":"Q4 實際間夜與 2027 年展望","if_then":["若 Q4 間夜低於 +1%，減碼三分之一。","若 Q4 間夜高於 +3%，依計畫加碼第二筆。"],"evidence_refs":["end_markets#1"]},{"axis":"AI 成效數據品質","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Glenn Fogel：Penny 使用量很小，尚未到可給數字的階段。","side_b":"2026-11-03 Ewout Steenbergen：Penny 與 Agoda AI 助理用戶轉換率約為非用戶兩倍，Agoda 用戶訂單金額高約 20%。","ruling":"這是使用者對非使用者的比較，有自選樣本問題，不能說 AI 造成轉換上升。標為未證、持續監測，收入面暫不計入。AI 對成本的效益較可信，客服成本在量增下確實減少。","evidence_level":"管理層口頭揭露，無實驗對照","settle_metric":"公司是否揭露實驗增量或全平台轉換率變化","if_then":["若 2027 年中前仍沒有實驗增量數據，Base 不計入 AI 營收加成，也不加碼。","若揭露的增量可讓全平台轉換率提高 1% 以上，Bull 機率上調 5 個百分點並加碼第二筆。"]},{"axis":"直接占比口徑","cause":null,"prior_field":null,"side_a":"FY2025 10-K：直接訂房占總間夜 50% 中段且年增。","side_b":"Q3 法說：B2C 直接占比四季穩定在 60% 中段，直接通路與其他業務同速成長。","ruling":"分母不同，兩者不矛盾。但穩定代表 B2C 直接占比已不再上升，這是不把護城河方向標成擴大的原因之一。","evidence_level":"一手資料，口徑不同","settle_metric":"2027 年 B2B 分開揭露後的 B2C 直接占比","if_then":["若 B2C 直接占比連 4 季低於 60%，減碼至半倉。","若回升到 70% 附近，加碼至滿額。"]},{"axis":"估值結論與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份估值中性，股價 194.27 美元，裁決進場。","side_b":"本次估值偏便宜，股價 160.66 美元，前瞻 15.43 倍。","ruling":"股價跌 17.3%，FY1 共識近 3 個月只降 0.38%，估值改善幾乎全部來自價格。裁決與角色由本次輸入算出。","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比與 FY2027E 共識修正","if_then":["若股價漲回 192 美元而共識未上修，不追。"]},{"axis":"基本面判讀","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份綜合評等 B、價值陷阱風險中等、護城河穩定、五年後跑道寬、品質複利成長、無景氣位置。","side_b":"本次全部維持。","ruling":"Q3 新證據兩面都有：實績高於指引、AI 轉介仍小；但 Q4 指引轉弱，FTC 認列與 DSA 調查是新的。正反相抵，沒有足以改級的證據。","evidence_level":"一手財報、法說與 10-Q","settle_metric":"B2C 行銷槓桿與 2027 年指引","if_then":["若 B2C 行銷連 4 季失去槓桿，護城河改判縮減並減碼至半倉。"],"evidence_refs":["major_events#2","regulatory_antitrust#1"]},{"axis":"機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 30%、最大回撤 −52%。","side_b":"本次 Bull 25%、Bear 30%，最大回撤改用區間 −30%～−50%。","ruling":"機率不變，Q3 的正面和 Muse 的負面相抵。回撤由單點改為區間，並從較低股價起算；絕對底部約 81 美元，前份約 93 美元。","evidence_level":"情境推算，歷史回撤資料缺口","settle_metric":"情境與實際回撤對照"},{"axis":"加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","side_b":"2027 年 2 月財報：Q4 間夜不低於 +3%，且 2027 年調整後 EBITDA 指引不低於高個位數才加碼第二筆；跌破 145 美元而基本面無損也可加碼。","ruling":"舊加碼條件的回落 180 美元以下已觸發，Q2、Q3 間夜 +5%、+7% 也已達標，但 Q4 指引 +1%～+3% 會破線。TTM 總預訂額事實表未涵蓋，舊的 take rate 門檻無法驗證，所以改用下一個可驗證的數據點。","evidence_level":"財報與價格","settle_metric":"Q4 間夜、2027 年指引、週線收盤","if_then":["若兩項條件都達到，加碼第二筆。","若條件未達且股價未跌破 145 美元，停止加碼。"]},{"axis":"減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標。","side_b":"本次設六項：代理占間夜與 B2C 行銷、調整後營收占比、間夜年增、EBITDA 利潤率、平均股數、監管累計支出。","ruling":"舊判斷沒有落在這一欄，本次依現行格式補齊減碼與清倉的具體門檻，並以 Q3 數字為起點。","evidence_level":"方法調整","settle_metric":"六項指標每季追蹤"},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"公司首度揭露 AI 代理與 LLM 通路占 Booking.com 間夜達 5% 以上，且同一年度 B2C 行銷費用失去槓桿，等於發現層開始向平台抽稅。","ruling":"前份把這件事放在風險段，本次依情境敏感度抽出為 Single Thing。它同時影響營益率和終端倍數，敏感度高於監管賠款和短期需求。","evidence_level":"情境敏感度推算","settle_metric":"代理占間夜比重與 B2C 行銷槓桿"}],"triggers":[{"n":1,"text":"跨品類交易能否維持雙位數成長","type":"假設驗證","maps_to":"H1","metric":"跨品類交易年增","threshold":"不低於 15%","action":"連 2 季未達就停止加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"代理通路成長時 B2C 行銷能否維持槓桿","type":"假設驗證","maps_to":"H2","metric":"B2C 行銷增速減總預訂額增速","threshold":"不高於零","action":"連 4 季未達，減碼至半倉","source_freq":"每季法說；2027 年起 B2B 分開揭露","date":"2027-02"},{"n":3,"text":"發現層開始抽稅","type":"Single Thing","maps_to":"Single Thing","metric":"代理占間夜與 B2C 行銷槓桿","threshold":"代理占間夜達 5% 且同一年度 B2C 行銷失去槓桿","action":"減碼至半倉","source_freq":"每季法說","date":"2027-02"},{"n":4,"text":"短期需求惡化超過指引","type":"風險","maps_to":"R3","metric":"間夜年增","threshold":"Q4 低於 +1%，或 2027 上半年連 2 季低於 +3%","action":"減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["end_markets#1","supply_demand_durability#0"]},{"n":5,"text":"監管支出或佣金管制擴大；希臘 12 月 28 日聽證是最近的里程碑","type":"風險","maps_to":"R2","metric":"累計一次性支出與佣金管制","threshold":"累計超過 30 億美元，或歐盟主要市場出現佣金上限","action":"減碼至半倉；若有刑事介入則清倉","source_freq":"10-Q 與 10-K 法律附註","date":"2026-12-28","evidence_refs":["regulatory_antitrust#5","major_events#2"]},{"n":6,"text":"回購速度放慢","type":"風險","maps_to":"R4","metric":"平均股數年減","threshold":"連 4 季低於 4%","action":"停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":7,"text":"第二筆進場條件","type":"估值rearm","maps_to":"H3","metric":"Q4 間夜與 2027 年調整後 EBITDA 指引","threshold":"間夜不低於 +3%，且指引不低於高個位數","action":"加碼第二筆","source_freq":"Q4 財報","date":"2027-02"},{"n":8,"text":"價格先跌、基本面無損","type":"加碼","maps_to":"H3","metric":"週收盤價","threshold":"跌破 145 美元且前述風險條件都未觸發","action":"分批反買","source_freq":"每週","date":null},{"n":9,"text":"論點破裂","type":"清倉","maps_to":"Single Thing","metric":"唯一致命點與調整後 EPS 路徑","threshold":"唯一致命點成立後兩季未改善，或 TTM 調整後 EPS 連 6 季低於 Base 路徑 10%","action":"清倉","source_freq":"每季財報","date":null},{"n":10,"text":"下一次完整複審","type":"複審日期","maps_to":"H1、H2、H3","metric":"Q4 財報與 2027 年展望","threshold":"財報公布後","action":"重跑完整判斷","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"AI 代理與 LLM 占 Booking.com 間夜，搭配 B2C 行銷槓桿","bear_threshold":"占比達 5% 且 B2C 行銷失去槓桿","window":"連 4 季","source":"每季法說","last_status":"ok"},{"metric":"調整後營收占總預訂額年變動","bear_threshold":"年減超過 30 個基點","window":"連 4 季","source":"每季財報新聞稿","last_status":"ok"},{"metric":"間夜年增","bear_threshold":"低於 +3%","window":"連 2 季","source":"每季財報新聞稿","last_status":"warning"},{"metric":"全年調整後 EBITDA 利潤率（含 SBC）","bear_threshold":"年減超過 100 個基點","window":"一個會計年度","source":"年度財報與法說","last_status":"ok"},{"metric":"平均股數年減","bear_threshold":"低於 4%","window":"連 4 季","source":"每季財報新聞稿","last_status":"ok"},{"metric":"監管累計一次性支出","bear_threshold":"超過 30 億美元，或歐盟主要市場出現佣金上限","window":"自 2026 年 Q3 起累計","source":"10-Q 與 10-K 法律附註","last_status":"warning"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"來源是 FY2023 年 10-K 的一般性風險條文，距今近三年；摘要也註明查無單點失效字樣或具名雲端業者，沒有事件、金額或受影響營收可以對應。"}],"action_conditions":{"rearm_trigger":"2027 年 2 月財報：Q4 間夜不低於 +3%，且 2027 年調整後 EBITDA 指引不低於高個位數才加碼第二筆；跌破 145 美元而基本面無損也可加碼。","exec_line":"現價一帶先建目標部位三分之一；加碼凍結到 2027 年 2 月財報；股價漲回 192 美元之上而數據未到，不追。","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把代理型 AI 的繞過風險提前定價到淨利只剩約 2%～3% 年增；但 Q3 的 LLM 轉介遠低於間夜 1%，B2C 行銷仍有槓桿，代理業者目前也偏好串接聚合平台。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"跨品類與高等級會員把住宿客變成高頻直客。","2y":"跨品類交易維持雙位數成長，Genius 二三級占間夜續升。","5y":null,"10y":null,"threshold":"跨品類交易年增不低於 15%；Genius 二三級占 Booking.com 間夜維持 50% 後段以上","source":"每季法說的跨品類與 Genius 揭露","drift_rule":"連 2 季年增低於 14.25% 算削弱，連 3 季低於 13.5% 算反轉"},{"id":"H2","text":"代理型 AI 會穿過平台，而不是繞過平台；代理帶來的量不會把獲客成本整體墊高。","2y":null,"5y":"代理占比上升時，B2C 行銷仍有槓桿，結帳和供給留在本公司。","10y":null,"threshold":"B2C 行銷增速不高於總預訂額增速；調整後營收占總預訂額年減不超過 30 個基點","source":"每季法說；2027 年起 B2B 分開揭露後可直接計算","drift_rule":"B2C 行銷失去槓桿連 4 季算削弱，連 6 季算反轉"},{"id":"H3","text":"EPS 複利靠營收、利潤率和回購三者合作，五年維持低雙位數以上。","2y":null,"5y":"調整後 EPS 年化約 13.6%，到 FY2031E 約 19.7 美元。","10y":null,"threshold":"調整後 EPS 年增不低於 12%，平均股數年減不低於 5%","source":"每季財報新聞稿","drift_rule":"TTM 調整後 EPS 連 4 季低於 Base 路徑 5% 算削弱，連 6 季低於 10% 算反轉"}],"R":[{"id":"R1","text":"發現層開始抽稅：AI 代理和搜尋引擎把被看見變成新的收費項目，連鎖飯店自家 AI 訂房也在搶直客。不過十大連鎖只占間夜低雙位數，連鎖這條路徑的影響有限。","h_ref":"H2","clock":"🔥","threshold":"B2C 行銷連 4 季失去槓桿，或調整後營收占總預訂額連 4 季年減超過 30 個基點","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#3"]},{"id":"R2","text":"監管由禁止未來做法走向追溯賠償：FTC 案認列 10 億美元且未和解，西班牙已入帳 4.76 億美元，荷蘭基金會代表旅宿與消費者索賠，歐盟啟動 DSA 調查，希臘 12 月 28 日聽證救濟方案。","h_ref":"H3","clock":"🐢","threshold":"累計一次性支出超過 30 億美元，或歐盟主要市場出現佣金上限","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#5","regulatory_antitrust#6","major_events#2","lawsuit_class_action#1"]},{"id":"R3","text":"長程需求持續受壓：機票偏貴、部分航線運力受限，10 月又有往返中東的直接擾動和歐洲局部動亂，Q4 間夜指引只有 +1%～+3%。","h_ref":"H3","clock":"⚡","threshold":"Q4 間夜低於 +1%，或 2027 上半年連 2 季低於 +3%","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#0","geo_supply_chain#1","end_markets#1","capital_markets_pricing#0"]},{"id":"R4","text":"EPS 過度依賴回購：前九個月回饋 105 億美元，高於 TTM FCF，速度不能無限維持。FCF 還含預收款流入，成長放緩時會反轉。","h_ref":"H3","clock":"🔥","threshold":"平均股數年減連 4 季低於 4%"}],"single_thing":{"description":"公司首度揭露 AI 代理與 LLM 通路占 Booking.com 間夜達 5% 以上，且同一年度 B2C 行銷費用失去槓桿，等於發現層開始向平台抽稅。","why_fatal":"這是情境中敏感度最大的一項：營益率少 5 個百分點，Y5 EPS 由 19.7 美元降到約 16.7 美元；倍數若同時降到 12 倍，終端價由約 296 美元降到約 200 美元。FTC 加西班牙約 15 億美元只占市值約 1.2%。","if_happens":"Bear 機率升到 50% 以上，部位減半並停止加碼；後續兩季未改善就清倉。","how_monitor":"每季法說的 LLM 轉介占比（本季遠低於 1%）、B2C 行銷是否有槓桿、B2C 直接占比（本季 60% 中段）；2027 年起 B2B 分開揭露後可直接計算 B2C 行銷費用率。","probability":"12～24 個月約 10%～15%，五年內約 30%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":13.07,"peg_fy2":0.75,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":6.62,"FY2026E":10.41,"FY2027E":12.29,"FY2028E":14.35},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識調整後 EPS（分割後）。FY2025A 只有 GAAP 稀釋 EPS 6.62 美元，調整後基期事實表未涵蓋，兩者口徑不同，不可用來算成長率；共識年化 17.4% 只用 FY2026E 到 FY2028E 兩年。"},"catalysts":[{"date":"2026-12-28","date_precision":null,"type":"regulatory","event":"希臘競爭委員會就 Booking 承諾方案與異議聲明舉行聽證","impact":"中","watch":"救濟方案是否涉及佣金或排名限制，以及是否被其他歐洲機關援用"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 2027 年展望，B2B 業務合併後預計開始分開揭露","impact":"高","watch":"Q4 間夜、2027 年調整後 EBITDA 指引、投資金額、B2C 行銷費用率"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"中東直接與間接影響是否在第一季消退","impact":"中","watch":"Q1 2027 間夜年增是否回到 4% 以上，長程需求說法有無改變"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把代理型 AI 的繞過風險提前定價到淨利只剩約 2%～3% 年增；但 Q3 的 LLM 轉介遠低於間夜 1%，B2C 行銷仍有槓桿，代理業者目前也偏好串接聚合平台。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-2.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
