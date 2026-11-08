你是 DD 管線 v20 的判斷層閘（gate），標的 GFS（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1786 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
  - 註記：高於公司自家指引區間上緣（CEO 說法）；Earnings Whispers 共識約 $1.76B（二手來源，未經 IR 驗證）
- `f_kpi1_non_ifrs`（q1_business）｜Non-IFRS 營業利益率＝16.7 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝9.7 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi6_q3_2026`（q1_business）｜下一季（Q3 2026）指引：營收＝1885 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-04 date｜期間與口徑：2026-11-04／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-04）
- `f_peer_gfs_gross_margin_pct`（q2_moat）｜GFS 毛利率＝28.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_gfs_operating_margin_pct`（q2_moat）｜GFS 營業利益率＝11.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_gfs_fcf_margin_pct`（q2_moat）｜GFS FCF 利潤率＝6.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2303_tw_gross_margin_pct`（q2_moat）｜2303.TW 毛利率＝31.71 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2303_tw_operating_margin_pct`（q2_moat）｜2303.TW 營業利益率＝21.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2303_tw_fcf_margin_pct`（q2_moat）｜2303.TW FCF 利潤率＝25.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2330_tw_gross_margin_pct`（q2_moat）｜2330.TW 毛利率＝65.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2330_tw_operating_margin_pct`（q2_moat）｜2330.TW 營業利益率＝57.98 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.96 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.63 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.61 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝7323.06 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝8294.54 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3`（q4_capital）｜營業現金流＝405 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi4_non_ifrs`（q4_capital）｜調整後自由現金流（Non-IFRS）＝-3 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝49.4 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-539.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 1716.0、現金 2255.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝557.45 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.621 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝38.62 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.7 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.96，分子＝快照價 38.62｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝110.34 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.01 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.94 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝20989.67 USD m｜期間與口徑：2026-11-08／市值 21528.67 ＋ 淨負債 -539.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.87 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-47.69 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.66｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 38.62 / W52 51.45 / W104 44.58 / W250 50.57 / W250 13週斜率 -0.5%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝50.57 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.96 → 1.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（2.63 → 2.63）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（3.61 → 3.61）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（28 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Counterpoint 純晶圓代工季度份額：GFS 由 2024Q4 約 5% 降至 2025 年 4%，2026Q1 為 3%；TSMC 2026Q1 佔 73%，產業年增 30%（AI GPU/ASIC 驅動）。
  - 來源：Counterpoint Research, Global Pure Foundry Market Share: Quarterly（as_of 2026-03-31）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：Simply Wall St 社群敘事（非公司/機構資料）主張 GFS 先進製程落後 TSMC/Samsung，且在地化要求與客戶垂直整合為風險；未找到 2026 針對 GFS 的具名新進入者報導。
  - 來源：Simply Wall St community narrative（as_of 2026-01-01）｜affects：decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：GF 20-F 風險因素：部分 OEM 可能自行開發 in-house ASIC、繞過 fabless 的 GF 客戶並改採其他晶圓代工策略；幾乎所有客戶都有自家設計能力。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：2025 年 Smart Mobile Devices 營收年減 12.1%，部分原因是客戶雙供應來源（dual sourced）處的價格調整；單一來源產品約占晶圓出貨量 63%。
  - 來源：SEC EDGAR 20-F FY2025 Item 5（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2024 20-F：兩個匿名客戶各超過營收 10%，Customer A 2024 年占 16%（$1,061M）、Customer B 占 11%（$722M）；客戶名稱未揭露。
  - 來源：GLOBALFOUNDRIES Form 20-F FY2024 (SEC EDGAR)（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2021 20-F：前十大客戶占晶圓出貨量 2019/2020/2021 年約 73%/73%/67%；公司預期營收仍將集中在少數客戶。
  - 來源：GLOBALFOUNDRIES Form 20-F FY2021 (SEC EDGAR)（as_of 2021-12-31）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：12 吋擴產近 70% 來自中國晶圓廠，其餘地區擴產溫和；TSMC 縮減 12 吋成熟產能預期將轉單給其他代工廠
  - 來源：TrendForce／iconnect007（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce 2023 年預測中國成熟製程產能占比 2027 年達 39%，並警告 CIS、DDI、PMIC、功率離散元件可能價格競爭（舊預測，早於 2026 年緊俏）
  - 來源：TrendForce press 2023-12-14（as_of 2023-12-14）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：GF 2026 Q2 財報電話會議：車用與智慧行動營收轉弱，家用與工業 IoT 改善
  - 來源：GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#7`（supply_demand_durability｜方向 -｜狀態 ok）：消費性電子受記憶體漲價與零組件成本拖累，2026 下半年出貨承壓，部分客戶希望延後漲價
  - 來源：TrendForce DRAMeXchange weekly research（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：2024-11 美國商務部 BIS 就 GFS 2021-02 至 2022-10 間向實體清單中國公司出口晶圓的違規予以處罰（GFS 承認違反 EAR）；屬過往出口管制執法。
  - 來源：Linklaters: Due Diligence in China's Semiconductor Value Chain - Lessons from the GlobalFoundries Enforcement Case（as_of 2024-11-07）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2024-11-01 BIS 對 GFS 處以50萬美元和解罰款：2021–2022年向實體清單公司 SJ Semiconductor 出貨約1,710萬美元晶圓未取得許可；GFS自行揭露並合作，歸因於交易篩查系統資料輸入錯誤。
  - 來源：Manufacturing Dive / BIS 執法案（as_of 2024-11-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：據 policyrisk.com 對 SEC 申報的摘要，GF 對單一 SOI 晶圓供應商（摘要指為 Soitec）的採購占比為 2025 年 71.4%、2024 年 60.9%、2023 年 63.0%；替換該供應商需時甚長。部分原料（稀土、天然氣）亦有單一來源，價格與供應受美中貿易緊張及烏克蘭、中東衝突影響。（二手摘要，未核對申報原文）
  - 來源：policyrisk.com GFS company page（SEC 申報摘要）（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：GF 申報文件的風險語言提及其業務可能受地緣政治狀況影響，例如與中國的政治與貿易緊張（2024 年 6-K 與投資人文件；非 2026 專屬揭露）。
  - 來源：GLOBALFOUNDRIES Form 6-K 3Q2024 earnings（as_of 2024-11-12）｜affects：decision_inputs.bear、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q2 2026 智慧行動裝置段營收年減 5.7%（上半年 -5.3%），歸因記憶體價格導致智慧手機疲弱；居家與工業 IoT 段 Q2 +10.3%、上半年 -6.7%，管理層上調 IoT 展望。
  - 來源：GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear
- `end_markets#6`（end_markets｜方向 -｜狀態 ok）：Counterpoint 純代工市佔表：GF 2026 Q1 約 3%，2024 Q4 為 5%；TSMC 73%。
  - 來源：Counterpoint Research Global Pure Foundry Market Share: Quarterly（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `end_markets#7`（end_markets｜方向 -｜狀態 ok）：IDC 2026 年 2 月預測 2026 智慧手機出貨年減 12.9% 至約 11.2 億支、2027 年 +2%；後續（約 2026 年 6 月，二手報導）修正為 2026 年 -13.9% 至約 10.9 億支、2027 年 -1.1%、2028 年 +5.5%。IDC 預期記憶體晶片價格 2027 年中趨穩。
  - 來源：eeNews Europe / Gigazine (IDC Feb 2026); IT Brief (IDC revision, secondary)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：FY2023 20-F 載明技術與服務價格隨時間下滑，未推出新技術可能迫使既有技術降價。
  - 來源：SEC GLOBALFOUNDRIES Form 20-F FY2023（as_of 2024-03-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：中國成熟製程晶圓廠持續擴張：Nexchip 28nm 邏輯平台於 2026-03-11 完成開發，Silan、Hua Hong 亦擴產與製程升級（競爭壓力，非替代技術）。
  - 來源：TrendForce News 2026-03-26 Nexchip, Silan and Hua Hong mature node（as_of 2026-03-26）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 營收指引發布後 Chartmill 報導盤前約下跌 5.5%，稱 Q3 營收預測略低於市場預期；Benzinga 則稱營收預測較前次區間 17.4–17.8 億上調，兩來源對「上調或略低」解讀不一
  - 來源：Chartmill: GlobalFoundries Dips After Q3 Revenue Forecast Trails Estimates; Benzinga earnings forecasts（as_of 2026-08-05）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#6`（capital_markets_pricing｜方向 -｜狀態 ok）：Axelrod Research 2026-10-07 筆記評級 HOLD，稱 2026-10-06 收盤 48.63 美元，對比 2026-05-09 的 74.12 美元（該筆記依 5 月營運快照，非新財報修正）
  - 來源：Axelrod Research: GFS the foundry thesis survives（as_of 2026-10-07）｜affects：valuation、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：TrendForce 報導：12 吋成熟製程擴產約 70% 由中國晶圓廠驅動；SMIC、華虹、晶合（Nexchip）新廠陸續投產，Nexchip 合肥四期 51 億美元擴 28nm。
  - 來源：TrendForce News / Tom's Hardware（搜尋摘要轉述）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：TrendForce 2026年4月：成熟製程價格或在2026回升，但庫存過剩與中國同業競爭仍構成壓力。
  - 來源：TrendForce News, Mature node prices may rebound in 2026 but inventory overhang and China competition weigh（as_of 2026-04-03）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2024 營收 67.5 億美元，較 FY2023 的 73.92 億下降 9%（-6.42 億）
  - 來源：GlobalFoundries Reports Fourth Quarter 2024 and Fiscal Year 2024 Financial Results（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2024 GAAP 毛利率 24.5%，較 FY2023 的 28.4% 下滑 390bp；非 IFRS 毛利率 25.3% vs 29.1%（搜尋摘要之轉述，未取得逐字原文）
  - 來源：GlobalFoundries Q4/FY2024 earnings release (6-K)（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024 年季度調整後毛利率：Q2 25.2%（年減 440bp）、Q3 24.7%、Q4 25.4%；去庫存壓力來自客戶庫存偏高，Q2 營收年減 12%
  - 來源：Benzinga: GlobalFoundries Exceeds Q2 Projections, Navigates High Inventory Levels In Chip Market（as_of 2024-08-06）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024 年 9 月 GFS 股價單月下跌 13.8%，年初至 9 月累計約 -36%，同期 TSMC +73%
  - 來源：Motley Fool: Why GlobalFoundries Stock Fell 14% Last Month（as_of 2024-10-04）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#4`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Q4 2024 另認列 9.35 億美元與 Malta, NY 產能相關減損，毛利率收縮、展望低於市場預期
  - 來源：Benzinga: GlobalFoundries Q4 Earnings: Revenue And EPS Beat, Margins Shrink, Revenue Outlook Disappoints Street（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":123.5,"bear_5y_price":26.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":70.9,"ev5y_pct":77.4,"irr_base_pct":11.3,"asym_ratio":5.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.96,"pe":19.7,"basis":"FY2026E 共識 Non-IFRS EPS（Koyfin，2026-11-07），現價 38.62 美元；終端倍數同樣以當年度 Non-IFRS EPS 為分母。"},"eps":{"bull":[2.8,3.95,4.9,5.7,6.5],"base":[2.55,3.25,3.7,4.05,4.4],"bear":[2.2,2.3,1.8,1.95,2.2]},"pe":{"bull":19,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.621,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GFS_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：Q3 營收財測 18.85 億美元±2,500 萬（原話："We expect total GF revenue to be $1.885 billion, plus or"）
- 2026-08-05｜CFO｜guidance：Q3 毛利率財測約 30.5%±100bp（原話："We expect gross margin to be approximately 30.5%, plus or"）
- 2026-08-05｜CFO｜guidance：Q3 EPS 財測 0.51±0.05（原話："we expect diluted earnings per share for the third quarter"）
- 2026-08-05｜CFO｜guidance：CID 全年成長預期由高 30% 上調至 50–60%（原話："we now expect to achieve full year 2026 revenue growth in"）
- 2026-08-05｜CEO｜guidance：矽光子 2026 營收預期至少翻倍（原話："we now expect our silicon photonics revenue as reported"）
- 2026-08-05｜CFO｜guidance：智慧行動裝置全年預期衰退低十位數百分比，原因為記憶體價格與短缺（原話："we currently expect smart mobile devices to decline by a"）
- 2026-08-05｜CFO｜guidance：IoT 全年成長預期由中個位數上調至 10–15%（原話："we expect our revenue for the home and industrial IoT end"）
- 2026-08-05｜CFO｜guidance：車用全年仍預期低雙位數成長，下半年（Q4）權重較高（原話："we continue to expect low double-digit percentage revenue"）
- 2026-08-05｜CFO｜guidance：技術服務營收全年貢獻上調至 1–1.2 億美元（原 6000 萬–1 億）（原話："we expect revenue contribution of approximately $100"）
- 2026-08-05｜CFO｜guidance：全年自由現金流率維持約 10%（原話："we continue to expect an adjusted free cash flow margin of"）
- 2026-08-05｜CFO｜guidance：下半年每季營運費用與 Q3 財測一致（原話："we now expect quarterly operating expenses in the second"）
- 2026-08-05｜CFO｜guidance：全年有效稅率中段十幾%（原話："we expect an effective tax rate in the mid-teens percentage"）
- 2026-08-05｜CFO｜margin：Q2 毛利率 29.9%，年增 470bp（原話："approximately 29.9% gross margin, above the high end of the"）
- 2026-08-05｜CFO｜margin：毛利率全年預期由年底 30% 目標改為全年約 30%（原話："we should be at about 30 points of gross margin for the"）
- 2026-08-05｜CFO｜margin：營收年增約 1 億美元對應毛利約增 1 億美元（落差口徑）（原話："about $100 million of revenue growth. Look at that adjusted"）
- 2026-08-05｜CFO｜margin：技術服務營收年增不到 4,000 萬，貢獻約 1 個百分點毛利率（原話："You take our technology services revenue up a little under"）
- 2026-08-05｜CFO｜margin：Q2 稼動率高 80%，仍有約 10 個百分點可成長空間（原話："we've still got about 10 points of utilization to be able"）
- 2026-08-05｜CFO｜margin：產品組合為毛利率單一最大驅動，仍處早期（原話："mix point, CJ, because it remains the single biggest driver."）
- 2026-08-05｜CFO｜margin：去年同期含 liquidated damages 一次性效益（原話："We had things like liquidated damages in early 2025, which"）
- 2026-08-05｜CFO｜margin：Q2 營業利益率 16.7%、營運費用 2.36 億（季增 16%）（原話："Total operating expenses of $236 million were up 16%"）
- 2026-08-05｜CFO｜commitment：2028 年毛利率退出率目標 40%（原話："get towards that 40% exit run rate that we indicated in the"）
- 2026-08-05｜CFO｜commitment：長期模型 CID 成長 30%+ 維持不變（原話："I would still stand by our long-term model that"）
- 2026-08-05｜CFO｜commitment：股東回饋目標：追蹤 12 個月調整後自由現金流之最多 50%（原話："our objective is to return up to 50% of trailing 12-month"）
- 2026-08-05｜CFO｜capital_allocation：首次季度現金股利 0.12 美元已發放，並宣布下一季同額股利（原話："we paid GF's first-ever quarterly cash dividend of $0.12"）
- 2026-08-05｜CFO｜capital_allocation：買回授權剩約 1 億美元，部署彈性（原話："approximately $100 million remains under the share"）
- 2026-08-05｜CFO｜capital_allocation：Q2 淨資本支出 4.08 億（約 23% 營收），自由現金流 −300 萬（原話："Adjusted free cash flow for the quarter was negative $3"）
- 2026-08-05｜CFO｜capital_allocation：全年 CapEx 預期落在 15–20% 區間的高端（原話："my expectation is that we'll be up to the higher end of"）
- 2026-08-05｜CFO｜capital_allocation：現金及有價證券約 33 億、負債 11 億、10 億循環額度未動用（原話："approximately $3.3 billion. Our total debt was $1.1 billion"）
- 2026-08-05｜CEO｜capital_allocation：7 月完成 Photon Technologies IVR 團隊 acquihire；6 月完成 Synopsys ARC 收購（原話："we completed our previously announced acquisition of"）
- 2026-08-05｜CFO｜product：Q2 CID 營收年增 62%、季增 20%（原話："Revenue increased 20% sequentially and 62% year-over-year."）
- 2026-08-05｜CEO｜product：SiGe 2027 年全年超額認購，擴充佛蒙特產能（原話："Demand for SiGe remains strong, and we are oversubscribed"）
- 2026-08-05｜CEO｜product：SiGe 業務目前大於矽光子業務（原話："our SiGe business is actually larger than our silicon"）
- 2026-08-05｜CEO｜product：矽光子 SCALE 平台 7 個進行中合作；Q2 tape-out 一個、Q3 預計再一個（原話："We currently have 7 active engagements with leading"）
- 2026-08-05｜CEO｜product：NPO 2027 起量、CPO 2028 起量，說法與前幾季一致（原話："We still maintain the view that '27 we will see the"）
- 2026-08-05｜CEO｜product：現有廠區內矽光子產能可擴 10 倍（原話："we could 10x our photonics capacity within our current 4"）
- 2026-08-05｜CEO｜product：矽光子成長目標（2028–2030）進度符合並可能超前（原話："very much on track and potentially ahead of those targets"）
- 2026-08-05｜CEO｜product：量子：預期 3.75 億美元商務部補助；1–3 年營收主要來自工程服務，製造服務營收年底前後才放量（原話："we expect to generate quantum-related revenue largely"）
- 2026-08-05｜CEO｜product：量子視為長期『買權』，放量時點太早無法判斷（原話："Think of it more medium term as a kind of call option on"）
- 2026-08-05｜CEO｜product：矽光子取得美國商務部 3 億美元意向書補助（原話："entered into a letter of intent with the U.S. Department of"）
- 2026-08-05｜CFO｜product：MIPS 與 ARC 收購貢獻營收首日起、營運費用上升預期大致被增量營收覆蓋（原話："largely be covered by that incremental revenue we see"）
- 2026-08-05｜CEO｜customer：矽光子客戶逾 40 家，管理層稱無客戶集中疑慮（原話："we have more than 40 customers today in SiPho"）
- 2026-08-05｜CEO｜customer：與前五大光收發模組廠中 4 家有接洽（原話："we are actively engaged with 4 of the top 5 optical"）
- 2026-08-05｜CFO｜customer：IoT 上調部分來自行動客戶將需求轉入 IoT（原話："some of those customers within mobile have actually"）
- 2026-08-05｜CFO｜customer：首次取得 MediaTek PMIC 設計案（原話："This marked GF's first-ever power management integrated"）
- 2026-08-05｜CEO｜customer：Q2 新增 7 個光網路設計案（原話："we secured 7 new"）
- 2026-08-05｜CFO｜customer：Bosch ADAS 雷達於 FDX 平台 tape-out（原話："we also taped out an ADAS radar built on our FDX"）
- 2026-08-05｜CEO｜competition：面對矽光子競爭者變積極，管理層視競爭為需求佐證（原話："the fact that there's competition is a sign that there's"）
- 2026-08-05｜CEO｜competition：客戶多源採購風險與地緣政治考量，客戶表示要確保更多供給（原話："customers are also coming to us and saying, I don't have"）
- 2026-08-05｜CEO｜competition：管理層稱無需新建晶圓廠即可擴產，對比同業新建廠（原話："We don't need to build other fabs and some of our other"）
- 2026-08-05｜CFO｜risk：手機預測因記憶體價格與短缺而下修（原話："principally due to the continued impact from memory"）
- 2026-08-05｜CFO｜risk：車用 Q2 衰退 13% 季減、10% 年減，歸因客戶出貨時點（原話："principally driven by customer-led"）
- 2026-08-05｜CFO｜risk：定價調整預期自 2027 年起反映於營收（原話："we expect the pricing adjustments to be reflected in"）
- 2026-08-05｜CFO｜risk：R&D 占營收比重預期上升（原話："we believe that R&D will rise as a percentage of revenue"）
- 2026-08-05｜CEO｜risk：管理層稱產能有限：CID 成長受限於製造生產力與擴產速度（原話："the question is more about the rate and pace of"）

### GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md
- 2026-03-10｜Michael Hogan｜guidance：矽光子營收 2025 年翻倍、2026 年再近乎翻倍（原話："revenue doubled in 2025 is set to nearly double again in"）
- 2026-03-10｜Michael Hogan｜guidance：矽光子 2028 年底年化營收達 10 億美元以上（原話："a clear line of sight to a $1 billion-plus run rate"）
- 2026-03-10｜Michael Hogan｜commitment：10 億美元年化目標有實際營收客戶支撐、稱產能超額認購（原話："is actually supported by real revenue customers"）
- 2026-03-10｜Michael Hogan｜margin：目標營收口徑：2028 年約 1/3 來自 CPO，其餘為可插拔（原話："we model about maybe 1/3 of that"）
- 2026-03-10｜Michael Hogan｜guidance：CPO 若較慢，目標不變、改出更多可插拔（原話："We'll just ship more pluggables as CPO catches up."）
- 2026-03-10｜Michael Hogan｜risk：管理層承認 CPO 放量時程可能較晚（原話："if CPO takes a little longer, we still stick by that"）
- 2026-03-10｜Michael Hogan｜guidance：2030 年 GF 通訊基建與資料中心可服務市場約 110 億美元（原話："than doubles to approximately $11 billion."）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 同期放大逾五倍（原話："the optical networking SAM more than quintuples"）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 至 2030 年約 40% CAGR（原話："optical networking SAM will grow something like 40% CAGR"）
- 2026-03-10｜Michael Hogan｜competition：自稱矽光子代工最大業者（原話："we think we're the largest player in silicon photonics"）
- 2026-03-10｜Michael Hogan｜competition：併入 AMF 後自稱市佔第一，現今 SAM 約 10 億美元（原話："we're the #1 guy in the market"）
- 2026-03-10｜Michael Hogan｜commitment：預期市佔將持續提高（原話："our share will actually continue to grow"）
- 2026-03-10｜Kevin Soukup｜customer：前五大可插拔收發器廠中四家與 GF 合作（原話："4 out of 5 of the top pluggable transceiver players are"）
- 2026-03-10｜Gregg Bartlett｜competition：對 TSMC COUPE 的回應：主張開放生態、雙向相容（原話："We are very much in support of an open ecosystem."）
- 2026-03-10｜Michael Hogan｜capital_allocation：在既有無塵室空間內擴產，由美國與新加坡政府夥伴支持（原話："GlobalFoundries is scaling within existing clean room space"）
- 2026-03-10｜Michael Hogan｜capital_allocation：矽光子每增加一美元資本支出的營收效率提高（原話："revenue per dollar of incremental CapEx is meaningfully"）
- 2026-03-10｜Gregg Bartlett｜capital_allocation：Malta 矽光子與先進封裝廠預期提供整合流程至良品光模組（原話："expected to deliver a fully integrated silicon"）
- 2026-03-10｜Kevin Soukup｜capital_allocation：AMF 併購預期帶來營收與成本綜效（原話："we expect to unlock further revenue and cost"）
- 2026-03-10｜Michael Hogan｜product：銅線於每通道 200G 以上面臨根本挑戰（原話："Using copper becomes fundamentally challenged"）
- 2026-03-10｜Michael Hogan｜product：光互連使 XPU 使用率由十幾趴升至 80% 以上（原話："from as low as mid-teens to north of 80%"）
- 2026-03-10｜Gregg Bartlett｜product：晶圓對晶圓鍵合可縮小 RF 開關晶粒面積（原話："reduce the effective die size by as much as 45%."）
- 2026-03-10｜Michael Hogan｜guidance：前述 10 億美元目標由 2030 年提前至 2028 年底前年化（原話："we pulled in the expectation of sort of $1 billion-plus"）
- 2026-03-10｜Michael Hogan｜customer：稱 10 億美元年化目標已有客戶爭搶產能（原話："this is an oversubscribed corridor, right?"）
- 2026-03-10｜Gregg Bartlett｜product：非光學先進封裝各線暫無個別 TAM（原話："here's what the TAM is going to be for each of these."）
- 2026-03-10｜Gregg Bartlett｜product：各非光學封裝應用成長不及 CPO 光模組（原話："None of these are likely to grow at the rate that"）
- 2026-03-10｜Michael Hogan｜risk：管理層明說暫不提供先進封裝 TAM（原話："we're not ready to put a particular TAM on that"）
- 2026-03-10｜Eric Chow｜commitment：將於 2026 年 5 月 7 日在紐約舉辦投資人日（原話："we will be hosting an Investor Day on Thursday, May 7"）
- 2026-03-10｜Eric Chow｜guidance：近期營運問題延後到 Q1 財報後再答（原話："We will be happy to address near-term questions"）

### GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md
- 2026-05-07｜Sam Franklin (CFO)｜guidance：CI&D 市場長期成長目標 30% 以上（原話："we feel very comfortable with the target of 30-plus percent"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2025 CI&D 營收年增 29%（原話："We delivered 29% year-over-year revenue growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：車用目標：低雙位數成長（原話："our target to deliver low double-digit percentage growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：IoT 目標：中段十幾%成長（原話："we believe that a target growth rate of mid-teens"）
- 2026-05-07｜Michael Hogan｜guidance：智慧手機（SMD）預期大致持平（原話："we'll probably look to stay relatively flat in SMD"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：矽光子營收目標：2028 年底年化 10 億美元（原話："$1 billion run rate by the exit of 2028"）
- 2026-05-07｜Gregg Bartlett｜guidance：矽光子 2030 營收可達 20 億美元（原話："we can actually achieve $2 billion in revenue by 2030"）
- 2026-05-07｜Gregg Bartlett｜guidance：電源業務 2030 前增量營收 10 億美元（原話："targeting an incremental $1 billion of revenue in our power"）
- 2026-05-07｜Gregg Bartlett｜guidance：MIPS／客製矽業務 2030 年化營收 10 億美元（原話："we see an opportunity to achieve a $1 billion run rate"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年底毛利率目標約 30%（原話："with a 30% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底毛利率目標 40%（原話："we expect to achieve a 40% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期毛利率目標 45%（原話："a line of sight to a 45% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底營業利益率約 25%（原話："delivering approximately 25% operating margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期營業利益率約 35%（原話："support an operating margin of approximately 35% longer term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底 EPS 約 4 美元、長期 6 美元（原話："approximately $4 of EPS exiting 2028, and $6 of longer-term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：自由現金流率目標約 10%（原話："to target approximately 10% free cash margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年資本支出占營收 15% 至 20%（原話："We're targeting about 15% to 20%"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期資本支出強度約 20%，且為淨額目標（原話："we think of that as a net target"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：技術服務占比 2026 全年預期靠近 12%（原話："we're going to be closer to that 12% end of the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率 40% 橋接：組合貢獻 5 至 6 點（原話："6 points of margin opportunity over the next 3 years"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：製造成本與每層光罩現金成本改善貢獻 1 至 2 點（原話："can deliver 1 to 2 points of margin growth as well"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：折舊上升在未來幾年約構成一點左右的逆風（原話："probably is a point or so of headwind"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：模型未預設大幅漲價，毛利改善來自組合（原話："price increases just associated with supply and demand"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率與營業利益率差距維持約 15 點，2028 後才縮至 10 點（原話："that sort of 15-point delta to the gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：OpEx 成長速度約為營收 CAGR 的一半（原話："we expect our OpEx to grow at roughly half the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：2026 Q1 毛利率年增 510 bps（原話："gross margin, up 510 basis points year-over-year"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：不按終端市場拆毛利，因產線設備可互換（原話："we don't break out the gross margin by end market"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：上市以來毛利率擴張超過 1,000 bps（原話："over 1,000 basis points of margin expansion"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：宣布首次季度現金股息（原話："initiation of a quarterly cash dividend of $0.12 per share"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：資本配置框架：回饋最多 50% 投資後自由現金流（原話："returning up to 50% of free cash flow after investments"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：預期可回收 30% 至 50% 的合格支出（原話："recover anywhere between 30% and 50% of eligible spending"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：第四筆併購預計未來幾個月內完成（原話："We have a fourth, which we expect to close in the next"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：10 億美元軟體與服務目標已含 ARC（原話："That's included."）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：最近五年資本支出強度約 22%，略高於前一版模型（原話："marginally higher than the prior model we shared"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：未來自由現金流預期維持 10% 以上區間（原話："over the next 5 years in the 10-plus percent range"）
- 2026-05-07｜Timothy Breen (CEO)｜capital_allocation：美國將占成長投資的大宗（原話："that will be the lion's share of our growth investments"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：正式併購 ARC IP 業務（原話："we're seeking to acquire the ARC IP business"）
- 2026-05-07｜Gregg Bartlett｜product：SCALE 為業界首個支援 OCI 的方案（原話："solution is the industry's first OCI capable solution"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 材料級放量預期 2028 開始（原話："material volume in co-packaged optics will start"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 顯著放量時點預估 2028 下半年（原話："probably the second half of '28"）
- 2026-05-07｜Sam Franklin (CFO)｜product：2028 前矽光子成長主要來自可插拔（原話："principally pluggables revenue growth focused"）
- 2026-05-07｜Michael Hogan｜product：車用毫米波雷達：FDX 靈敏度較 bulk CMOS 高 75%（原話："FDX is 75% more sensitive than the same solution"）
- 2026-05-07｜Gregg Bartlett｜product：量子運算目前為 NRE 型業務（原話："This is an NRE business for the foreseeable future"）
- 2026-05-07｜Sam Franklin (CFO)｜product：新增營收分類：製造服務與技術服務（原話："manufacturing services and revenue from technology services"）
- 2026-05-07｜Gregg Bartlett｜competition：可插拔光學方案低插入損耗光纖貼合（原話："We have a very elegant solution that has the lowest loss"）
- 2026-05-07｜Timothy Breen (CEO)｜competition：CEO 對 CPO 地位：預期為前二（原話："GF will be one of the top 2."）
- 2026-05-07｜Timothy Breen (CEO)｜competition：管理層預期車用小幅取得市占（原話："net-net, probably will gain a little bit of share"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 設計案 500 件，95% 為單一來源（原話："95% of those wins were awarded to GF on a sole-source"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 年再在岸化帶來 30 億美元設計案（原話："We had $3 billion of design wins in 2025 alone"）
- 2026-05-07｜Michael Hogan｜customer：車用營收由期初 1 億美元增至期中 14 億美元（原話："$100 million at the beginning of the decade, $1.4"）
- 2026-05-07｜Michael Hogan｜customer：IoT 優於市場主要來自市占提升（原話："I think it's mostly share gain."）
- 2026-05-07｜Timothy Breen (CEO)｜customer：與現代汽車集團簽署合作（原話："we announced a partnership with Hyundai Motor Group"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：CSP 預計計畫後段轉向更直接參與（原話："the latter part of the plan into more direct work"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：高效能 SiGe 產能超額認購至 2027 上半年（原話："seeing oversubscription in high-performance SiGe"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：手機市場成長受限，管理層不倚賴其成長（原話："no longer reliant on the growth of smart mobile devices"）
- 2026-05-07｜Timothy Breen (CEO)｜risk：全球一半關鍵半導體產能在中國與台灣（原話："50% of essential semiconductor capacity"）

### GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20261014.md
- 2026-10-14｜CEO｜customer：GF 被選為日本出資至多 210 億美元、Malta 兩座 300mm 新廠的技術提供者與營運者（原話："GF has been selected as the technology provider and operator"）
- 2026-10-14｜CFO｜capital_allocation：由 SPV 出資並擁有廠房與設備，GF 不直接承擔資本支出（原話："without directly incurring the associated capital investment"）
- 2026-10-14｜CFO｜margin：數字口徑：費用組成為建廠與營運管理費、技術費及 SPV 的 EBITDA 分成（原話："GF will earn construction and operations management fees"）
- 2026-10-14｜CFO｜guidance：待最終協議簽署後，預期 2027 年營收貢獻約 5,000 萬美元（原話："expect revenue contribution of approximately $50 million"）
- 2026-10-14｜CFO｜guidance：毛利率增益 2027 年 30–50bp，長期 100–200bp（原話："annual accretion of 30 to 50 basis points in 2027"）
- 2026-10-14｜CFO｜guidance：營益率增益 2027 年 100–200bp，長期 200–300bp（原話："annual accretion of 100 to 200 basis points in 2027"）
- 2026-10-14｜CFO｜margin：營益率增幅高於毛利率增幅，管理層說明主因是建廠管理費的損益表認列（初步看法）（原話："our preliminary views on the income statement recognition"）
- 2026-10-14｜CFO｜guidance：EPS 增益 2027 年 0.10–0.15 美元，長期 0.50–0.75 美元（原話："annual accretion of $0.10 to $0.15 in 2027"）
- 2026-10-14｜CFO｜guidance：技術與廠務管理服務模式預期 10 年累計自由現金流約 30 億美元（原話："approximately $3 billion of cumulative free cash flow"）
- 2026-10-14｜CFO｜margin：數字口徑：10 年內每片晶圓利潤設計為與自建產能相當，但無對應固定成本（原話："target profit per wafer without incurring the associated"）
- 2026-10-14｜CEO｜commitment：時程：本季動工、2028 年可進機台、2029 年首批晶圓（原話："We expect to break ground during this quarter"）
- 2026-10-14｜CEO｜commitment：第二座廠須在 2028 年底前由利害關係人做 go/no-go 決定（原話："go/no-go decision between the stakeholders before the end"）
- 2026-10-14｜CFO｜risk：財務數字以簽署最終協議為前提，且僅反映第一座廠（原話："subject to the signing of definitive agreements"）
- 2026-10-14｜CEO｜product：新廠技術範圍為 FDX、BCD、UX 平台（原話："highly differentiated and sought-after FDX, BCD and UX"）
- 2026-10-14｜CEO｜capital_allocation：管理層稱此計畫與 GF 自有成長計畫並行、完全是額外增量（原話："does not displace or replace what GF is doing on its own"）
- 2026-10-14｜CEO｜customer：點名日美既有客戶與供應商，並稱與更多客戶處於進階洽談（原話："We are in advanced discussion with many more customers"）
- 2026-10-14｜Unknown Executive｜capital_allocation：CHIPS 辦公室同意將先前核定的 9.55 億美元資金改用於 2027 年起的研發與資本支出（原話："repurpose $955 million of our previously awarded CHIPS"）
- 2026-10-14｜Unknown Executive｜capital_allocation：美國商務部將取得 GF 約 4% 股權（原話："will receive an equity stake in GF of approximately 4%"）
- 2026-10-14｜Unknown Executive｜commitment：預期今日公告後美國政府不再有進一步股權參與（原話："we do not expect any further equity participation"）
- 2026-10-14｜CEO｜competition：管理層稱 GF 是少數在美國本土有規模產能與擴產能力的晶圓代工廠（原話："one of the only at-scale foundries with meaningful capacity"）
- 2026-10-14｜CEO｜product：每期滿載約新增 90 萬片年產能（300mm 約當）（原話："add approximately 900,000 wafers of annual capacity"）

### 問答異常語氣（迴避／改口／保留）
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Arcuri：SiPho 競爭者積極、客戶集中，客戶能否多源採購？｜答法：未直接說明多源採購可行性，改談競爭代表需求強、客戶超過40家、客戶要確保更多供給
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Muse：CID 2026 退出率約 3.5 億，2027 成長是大幅成長或消化期？｜答法：不給 2027 具體數字，重申長期模型 30%+ 成長，CEO 改談產能與生產力步調
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Caso：矽光子補助如何沖抵淨 CapEx？｜答法：CEO 回答補助的技術內容與戰略意義，未回答對淨 CapEx 的沖抵幅度
- GFS_Q2_2026_Earnings_Call_20260805.md｜問：Karl Ackerman：ARC 與 IVR 對 9 月財測的營收與費用貢獻｜答法：CFO 給全年營收區間與 Q3/Q4 1/3、2/3 分佈，未給 Q3 單季營收與費用絕對數字
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Bryson：競爭對手稱握有逾 80% 矽光子市佔、營收與 GF 相近，如何解釋落差｜答法：Hogan 回「You can talk to the Tower about what they think」，未回應落差，改談自身十年投資與三大支柱
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Garrigan：目前與 3 至 5 年後的市佔為何｜答法：未給市佔百分比，只講自身為第一、SAM 約 10 億美元、預期市佔續升
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Hosseini：光學以外先進封裝機會與 TAM 數字｜答法：Bartlett 與 Hogan 皆明說暫不給 TAM，改談產品組合與「stay tuned」
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Ted Kang（Craig Group）請按事業別拆分 2030 毛利率，並問何以營業利益率槓桿不如毛利率｜答法：管理層明確不拆毛利率（理由為產線設備可互換），改以組合與成本層次回覆；營業利益率差距以技術服務 R&D 密集解釋。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Charles Shi（Needham）請拆分毛利率改善中組合與效率占比，以及基礎晶圓代工毛利目標與補貼貢獻｜答法：CFO 給組合 5 至 6 點、成本 1 至 2 點等區間，但未提供基礎晶圓代工的毛利目標，也未量化補貼對毛利的貢獻。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Matt Bryson（Wedbush）問 1 百萬量子位元系統的含量或 TAM，及 IonQ 收購 SkyWater 的影響｜答法：Gregg 未給含量或 TAM 數字，改說之後有網路研討會，對 IonQ 事件僅說不評論；Tim 補充當日市場在找數字。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 8 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 3 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 9 | 6 |
| substitute_technology | found | 5 | 4 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 6 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","irr_base_pct":6.9,"ev5y_pct":41.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":41.5,"irr_base_pct":6.9,"max_dd_pct":-60,"bull_5y_price":117.6,"bear_5y_price":28.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","price_at_dd":48.24,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GFS","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"GLOBALFOUNDRIES Inc."},"oneliner":"Q3 毛利率與矽光子進度都超前，股價卻半年跌 48%；2027 年 40 億美元資本支出的現金帳還沒交代清楚，等 Q4 法說看自由現金流與客戶預付再決定。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261108/scenario.json","answers":{"q1_business":{"verdict":"GF 賺的是非先進製程晶圓代工的錢，錢卡在單一來源的特殊製程節點；利潤正從手機移向光通訊，2026 Q3 非手機營收首度超過三分之二。","reasoning":"最新一季為 2026 Q3（2026-11-04 法說，CFO；事實表 KPI 只到 Q2，Q3 數字取自逐字稿）：營收 18.99 億美元，季增 6%、年增 13%；Non-IFRS 毛利率 31.4%，營業利益率 17.9%；出貨 64.7 萬片 300mm 約當，年增 7%，混合 ASP 年增近 5%，量和價一起走。製造服務占 88%，技術服務占 12%。四個終端市場合計 88%：手機 32%（年減 19%）、IoT 20%（年增 49%）、車用 19%（年增 20%）、通訊基建與資料中心 17%（年增 81%）。單點依賴：上游單一 SOI 晶圓供應商 2025 年占該類採購 71.4%（二手摘要，未核對申報原文）；下游前兩大客戶 2024 年合計 27%。這兩項是集中度風險，不是護城河證據。產業時鐘判擴張期：8 吋前十大平均稼動率 2026 年近 90%，2026 Q1 到 Q2 漲價 5%～15%，第三輪可能延續到 2027（TrendForce）。產業態勢判雙向拉鋸：競爭面，中國晶圓廠貢獻 12 吋擴產近 70%，矽光子新進者增加；結構面，台積電與三星縮減 8 吋，客戶以預付鎖產能；其他結構面，美國政府將持股約 7%，CHIPS 資金改配 9.55 億美元。","fact_refs":["f_kpi0_gaap","f_kpi1_non_ifrs","f_kpi2_gaap","f_kpi6_q3_2026","f_earnings_recency","f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct"],"verdict_values":{"revenue_quality":"中等偏好：製造服務 88%，技術服務 12% 且毛利率高於長期目標；但 2025 年毛利含一次性補償項目，2026 Q3 自由現金流含約 1.5 億美元預付與補助。","unit_econ_note":"2026 Q3 每片 300mm 約當的製造服務營收約 2,583 美元（18.99 億×88%÷64.7 萬片），全公司約 2,935 美元；混合 ASP 季增約 2.5%、年增近 5%。CFO 指引 2027 年 ASP 與組合合計約 +10%。","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"資本密集晶圓代工；FY2024 IFRS 虧損，FY2023 與 FY2024 營收各年減約 9%，年度毛利率 24%～28%，2026 Q3 才到 31.4%；光通訊段已形成獨立成長線。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉為主，只有光通訊段可望結構性持久。成熟製程緊俏來自台積電與三星縮減 8 吋及 AI 排擠產能（TrendForce、IDC），但中國 12 吋持續擴產，供給可逆；光通訊段有 2027 訂滿、2028 漸滿的公司口徑，尚無第三方驗證。","bargaining":{"up":"單一 SOI 晶圓供應商 2025 年占採購 71.4%（二手摘要指為 Soitec，未核對原文），上游議價權偏高；雷射供應同樣吃緊。","down":"前兩大客戶 2024 年占 16% 與 11%；單一來源產品約占晶圓出貨 63%，對設計導入後的客戶有議價力，雙來源手機料號則已被迫降價。","geo":"美國、德國、新加坡產地是客戶分散地緣風險的理由，美國政府將持股約 7%。"},"profit_pool_dir":"利潤池由手機往光通訊、車用與技術服務移動；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"通訊基建與資料中心可服務市場（2030，管理層口徑）","value":"約 110 億美元（2026-03-10，Michael Hogan）"},{"item":"光網路可服務市場成長","value":"至 2030 年約 40% 年複合（2026-03-10，Michael Hogan）"},{"item":"矽光子可服務市場（當時）","value":"約 10 億美元（2026-03-10，Michael Hogan）"},{"item":"GF 矽光子營收","value":"2026 年約 5 億美元，2027 年底年化約 10 億美元（2026-11-04，CEO）；2030 年目標 20 億美元（2026-05-07，Gregg Bartlett）"},{"item":"滲透率粗估","value":"通訊基建與資料中心 2026 營收約 12.5 億美元（Q3 占比 17%×FY1 共識營收）÷2030 年 110 億美元＝約 11%"},{"item":"營業利益池五年占比","value":"事實表未涵蓋，無法判斷利潤池是否淨流出"}]}}},"q2_moat":{"verdict":"護城河方向判穩定：執行力擴大，定價權只是隨產業回升，整體代工份額仍在下滑。","reasoning":"機制是差異化特殊製程（SiGe、矽光子、RF、FDX、BCD 與 GaN）設計導入後難替換，2025 年 500 件設計案 95% 為單一來源（2026-05-07，CEO），單一來源產品約占晶圓出貨 63%（20-F），再加上美、德、新加坡的非中台產地。同業 ROIC 差距事實表未涵蓋，改用份額、ASP 與利潤率。份額向下：Counterpoint 純代工份額由 2024 Q4 約 5% 降到 2026 Q1 約 3%，主因台積電 AI 放量，這是全市場營收份額，不是特殊製程份額，但也沒有數據能反駁。ASP 向上：2026 Q3 年增近 5%，為 2023 年以來首次，同期成熟製程普遍漲 5%～15%，不能算成 GF 獨有的定價權。TTM 毛利率與營業利益率仍低於聯電。執行面確實變好：連續三季達指引高端，矽光子目標提前一年，台積電把美國矽中介層交給 GF（5 年 20 億美元）。份額下滑沒被反駁前，不標擴大。","fact_refs":["f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct","f_peer_gfs_fcf_margin_pct","f_peer_2303_tw_gross_margin_pct","f_peer_2303_tw_operating_margin_pct","f_peer_2303_tw_fcf_margin_pct","f_peer_2330_tw_gross_margin_pct","f_peer_2330_tw_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"特殊製程設計導入後的單一來源鎖定，加上非中台產地與美國政府支持的產能。","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：2026 Q3 毛利率 31.4% 創新高，矽光子年化 10 億美元提前一年。定價權穩定：ASP 年增近 5% 與全產業漲價同步。份額由約 5% 降到約 3%（Counterpoint），兩者合併不標上升。","competitor_notes":[{"name":"2330.TW","strategy_note":"既是最大競爭者，也成為 GF 矽中介層客戶；若把矽光子與自家先進封裝綁售，威脅會升級。"},{"name":"INTC","strategy_note":"代工與自家產品並行，對 GF 的直接重疊有限，爭的是美國在地產能與政府資源。"},{"name":"005930.KS","strategy_note":"重心在記憶體與先進製程，正縮減 8 吋，短期反而讓出成熟製程需求。"},{"name":"2303.TW","strategy_note":"最接近的成熟製程對手，利潤率與自由現金流都高於 GF，並已進入矽光子。"},{"name":"Tower","strategy_note":"矽光子與 RF 的直接對手，曾被引述持有逾八成矽光子份額，GF 已向 ITC 提出專利申訴。"}],"peer_na_reason":"事實表未涵蓋同業 ROIC 與投入資本，改以份額、ASP 與利潤率對照。","threats":[{"level":"🟡","text":"矽光子新進者增加（Tower、台積電、STMicro、聯電），目前是點對點競爭；若台積電把矽光子與 CoWoS 綁售，升級為生態攻擊。","p":"35%","evidence_refs":["competitive_share_entrants#0","end_markets#6"]},{"level":"🟡","text":"中國成熟製程持續擴產，12 吋擴產近七成來自中國，壓力落在差異化較低的料號。","p":"40%","evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","substitute_technology#3","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#1"]},{"level":"🟡","text":"客戶自建設計能力與雙來源：2025 年手機營收年減 12.1%，部分來自雙來源料號降價；技術價格長期傾向下滑。","p":"30%","evidence_refs":["customer_second_source#0","customer_second_source#1","substitute_technology#1"]}],"roic_durability":{"quadrant":"低利益率×低周轉（周轉率為定性判斷，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端與 AI 資料中心，決策者是收發器廠與晶片商，三層目前都成立：每通道 200G 以上銅線受限，產能訂滿到 2027、2028 漸滿（2026-11-04，CEO）。但大部分預付協議要到 2026 Q4 至 2027 年初才簽，急迫不等於持久。"},{"item":"決策層級","level":"🟢","text":"在設計導入這個最小決策單位，替代性低：2025 年設計案 95% 單一來源，單一來源產品約占晶圓出貨 63%。例外是雙來源手機料號已被降價，矽光子能否多源採購管理層沒有正面回答。"},{"item":"價值鏈分配","level":"🟡","text":"光通訊鏈目前缺 GF 的產能，客戶願意預付；但雷射更緊，離散雷射不在 GF 路線圖上，利潤可能往雷射端集中。TTM 營業利益率約為聯電一半。"},{"item":"社會容忍度","level":"🟡","text":"沒有社會對漲價的天花板問題，美國政府站在同一邊。但部分優勢來自政策：CHIPS 改配 9.55 億美元、35% 投資抵減，都可能隨政策改變。"}],"roiic":"已實現為負：營業利益由 FY2022 約 12.6 億降到 FY2025 約 8.0 億美元（營收×營業利益率），同期仍有資本支出。前瞻值未證，CFO 稱多數投資 2 年內回收（2026-11-04）。","reinvest_rate":"事實表未涵蓋折舊、營運資金與投入資本，正式再投資率算不出。規模參考：2027 年淨資本支出 40 億美元，約為 FY1 共識 EPS×5.58 億股（約 10.9 億美元）的 3.7 倍。","endo_ceiling":null,"formula_note":"稅後營業利益率以 TTM 11.74%×（1−約 15% 稅率）≈10.0%；投入資本周轉率事實表未涵蓋，當期 ROIC 與內生成長上限無法計算。"}}}},"q3_growth":{"verdict":"跑道中等：光通訊五年內會吃掉可見空間的三成以上，其他新線都還太小，接不住。","reasoning":"成長來源是量價加組合：2026 Q3 營收年增 13%，晶圓量年增 7%，混合 ASP 年增近 5%。三年共識 EPS 年複合 31.4%（FY2025A IFRS 1.59 到 FY2028E 3.61，基期與共識口徑不同，EPS 家數事實表未涵蓋）；FY2025A 到 FY2027E 營收年複合 10.5%（FY1、FY2 營收共識各 21、22 位分析師）。缺口約 21 個百分點，幾乎全部來自利潤率擴張，不是再投資複利。跑道：通訊基建與資料中心 2026 營收粗估 12.5 億美元，2030 年可服務市場 110 億美元的 30% 是 33 億美元，以管理層長期下限 30% 成長計約 3.7 年到達，不足 5 年，倍數要保守。第二曲線有但都小：台積電矽中介層約每年 4 億美元、客製矽與電源各為 2030 年 10 億美元目標、量子是買權，美日 Malta 第一座廠 2029 年才出首批晶圓，最終協議未簽。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量（Q3 晶圓年增 7%）、價與組合（Q3 ASP 年增近 5%，2027 指引約 +10%），EPS 成長主要靠利潤率擴張。","runway_years":3.7,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上限算不出：投入資本與折舊事實表未涵蓋，已實現增量報酬為負，CFO 的 2 年回收未證。缺口歸因於利潤率擴張，情境樹按超出上限處理。","segments":[{"item":"通訊基建與資料中心","value":"Q3 占 17%；年增 81%；2026 全年 +60%～70%；長期模型 30% 以上"},{"item":"車用","value":"Q3 占 19%；年增 20%；2026 低雙位數成長"},{"item":"居家與工業 IoT","value":"Q3 占 20%；年增 49%；2026 +10%～15%"},{"item":"智慧行動裝置","value":"Q3 占 32%；年減 19%；2026 年減低十幾個百分點"},{"item":"技術服務","value":"Q3 占 12%；毛利率高於長期目標"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"Q3 年增 540bp"},{"name":"核心市占近 12 個月縮減","lit":true,"note":"Counterpoint 純代工份額約 5% 降到約 3%"},{"name":"主力產品提價後銷量下滑","lit":false,"note":"事實表未見此現象"},{"name":"EPS 年複合高於營收年複合逾 5 個百分點","lit":true,"note":"31.4% 對 10.5%"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY2025 為 1.14；FY2024 淨損不適用"},{"name":"股權酬勞占營收逾 5% 且上升","lit":false,"note":"Q4 指引約 3.4%"},{"name":"TAM 萎縮或被替代","lit":false,"note":"手機下滑主因記憶體短缺，不是技術替代"},{"name":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋，未計入"},{"name":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"事實表未涵蓋，未計入"},{"name":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"2027 年大幅擴產"}]}}},"q4_capital":{"verdict":"資本配置中等：股權酬勞節制，但 2027 年要花 40 億美元，現金帳沒交代清楚，政府股權又帶來 7.5% 股數增加。","reasoning":"FY2025 自由現金流 10.09 億美元，淨利 8.85 億美元，轉換率 1.14；TTM 自由現金流率只剩 6.01%。Q2 調整後自由現金流 −300 萬美元；Q3 為 1.36 億美元，其中約 1.5 億美元是客戶預付與政府補助，扣掉約 −1,400 萬美元。股權酬勞 Q4 指引 6,800 萬美元，占營收 3.4%。現金去向：資本支出為主（2026 淨額占營收 15%～20%），併購 ARC 4.55 億美元，股利每季 0.12 美元，Q3 回購 1 億美元，政策上限為自由現金流的 50%。資產負債表健康：現金與有價證券約 32 億美元，負債 11 億美元，循環額度由 10 億增到 15 億美元，未動用。問題在 2027：要維持約 10% 自由現金流率，以 FY2 共識營收 82.9 億美元算，含預付的營業現金流要 48.3 億美元（40 億＋8.3 億），扣掉三分之一預付 13.3 億美元，基礎營業現金流要約 35 億美元；2026 Q2、Q3 年化只有 14.9 億美元，差約 20 億美元。Chris Caso 在法說上問現金實際流出多少，CFO 沒給數字。股數由 5.58 億增到 2027 年約 6 億。","fact_refs":["f_kpi3","f_kpi4_non_ifrs","f_kpi5_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_gfs_fcf_margin_pct","f_rev_consensus_fy2_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"ARC（4.55 億美元，2026-06）、MIPS、AMF 的已實現增量報酬事實表未涵蓋；CFO 只說費用大致被新增營收覆蓋，未能證明，不計通過。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 回購 1 億美元，均價事實表未涵蓋。即便以 2026-10-06 收盤 48.63 美元估，FY1 盈餘殖利率約 4.0%；十年期公債殖利率事實表未涵蓋，未能證明超過門檻，不計通過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q4 指引股權酬勞 6,800 萬美元，年化 2.72 億，約占市值 215 億美元的 1.26%，低於 1.5%；政府股權造成的 7.5% 股數增加不算在這項，另列風險。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，併購金額相對 2027 年資本支出小，現金去向已寫在本題理由。"}}}},"q5_valuation":{"verdict":"現價只要 2031 年 EPS 做到約 4.15 美元就有 10% 年化，我基本相信，但要先看到 2027 的現金帳與新股數下的共識。","reasoning":"現價 38.62 美元，FY1 本益比 19.7 倍，FY2 14.7 倍（38.62÷2.63），FY3 10.7 倍（38.62÷3.61）。現價隱含：用 15 倍終端本益比、要年化 10%，2031 年股價要到 62.2 美元（38.62×1.1^5），EPS 要約 4.15 美元，只略高於 FY3 共識 3.61，等於假設 2028 年之後幾乎不再成長。這個要求不高，條件是毛利率至少到 35%。PEG 0.63（19.7÷31.4），但成長率的基期是週期低點的 FY2025 IFRS 1.59，會放大成長率，不當便宜證據。Trailing 本益比 110.34 倍與同一份事實表的 FY2025 稀釋 EPS 1.59（約 24 倍）不相容，視為分母失真，不使用。EV 方面，事實表淨現金 5.39 億美元，CFO 口徑現金與有價證券約 32 億、負債 11 億，淨現金約 21 億；但股數要升到 6 億，6 億×38.62＝231.7 億，扣淨現金約 211 億美元，與事實表 EV 209.9 億相近，前瞻 EV/S 2.87 倍可用。五年歷史分位事實表未涵蓋，年度端點只有 3～4 點，P/S 與 EV/S 都在端點最低。同業 Fwd P/E 事實表未涵蓋。賣方均價 80.24 美元（高 125、低 60，全距 2.08 倍）是 10 月前快照，股價已跌 20%，不支持也不反對本次結論。短期目標：Base FY2027E 2.55×18 倍＝45.9 美元；中期：Base FY2028E 3.25×16 倍＝52.0 美元。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_ev_s_fwd","f_net_debt_m","f_shares_diluted_m","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"valuation":{"basis":"Non-IFRS Fwd P/E 為主（FY1 19.7 倍、FY2 14.7 倍），前瞻 EV/S 2.87 倍為輔；Trailing 本益比分母失真，不使用。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業 Fwd P/E，無法做倍數對照，終端倍數改以自身現值對照。"},"fwd_pe":19.7,"peg":0.63,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2 14.7 倍、PEG 0.63、P/S 在年度端點最低，表面便宜；但分母有爭議，三年共識 90 天沒動，6 億股與新增折舊是否入模無法確認，因此結論維持中性偏便宜，不升為便宜。五年分位事實表未涵蓋。","upside_short_pct":18.9,"upside_mid_pct":34.6,"denominator_disputed":true,"denominator_note":"FY1 到 FY3 EPS 為 Non-IFRS，排除每季約 6,800 萬美元股權酬勞。三年共識在相隔約 90 天的兩份快照間完全相同，這段期間公司發布 Q3 財報、2027 年約 6 億股與 40 億美元資本支出，零修正不可信。便宜的說法要等 Q4 法說後共識更新才算數。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把週期高點的毛利率當成結構，其次是低估 40 億美元資本支出的折舊與股本成本。","reasoning":"三種看錯的完整論證在反證紀錄。壓力測試 4 項過 3 項：以 Base FY2029 EPS 3.70 美元為起點，後續成長率降到 15%、10%、5%，FY2031 分別為 4.89、4.48、4.08 美元，配 15、12、10 倍，股價 73、54、41 美元，皆不低於現價；若 2028 年毛利率卡在 33%，EPS 約 2.96 美元（營收 98 億、費用 11.2 億、稅率 16%、6 億股），配 12 倍為 35.5 美元，低於現價 8%。資料缺口：外部證據多數抓取於 2026-10-12，股價自 48.24 跌到 38.62 美元（−19.9%）期間，包內只有兩次公司公告，沒有第三方解讀，市場真正擔心什麼只能推論。管理層迴避紀錄：矽光子能否多源採購（2026-08-05）、競爭者稱逾八成市占的落差（2026-03-10）、補助沖抵淨資本支出的幅度（2026-08-05）、2027 現金實際流出（2026-11-04）。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度風險：份額縮減與 EPS 成長遠高於營收成長兩項訊號亮起"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.96,"pe":19.7,"basis":"FY2026E 共識 Non-IFRS EPS（Koyfin，2026-11-07），現價 38.62 美元；終端倍數同樣以當年度 Non-IFRS EPS 為分母。"},"eps":{"bull":[2.8,3.95,4.9,5.7,6.5],"base":[2.55,3.25,3.7,4.05,4.4],"bear":[2.2,2.3,1.8,1.95,2.2]},"pe":{"bull":19,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.2,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-35,"basis":"近 26 週已跌 47.7%，顯示此股兩季內可以腰斬；2024 年至 9 月累計跌約 36%。Bear 谷底 EPS 1.80 美元配 10～13 倍為 18.0～23.4 美元，較現價 −53%～−39%，上下各留緩衝。","trigger_time":null},"basis":{"bull":"2028 年底毛利率達 40%，矽光子 2030 年 20 億美元以上，美日計畫順利，長期 EPS 目標 6 美元在 2030 年前後達成；終端 19 倍略低於今日 FY1 的 19.7 倍。","base":"2027 年 2.55 美元略低於共識 2.63，因股數升到 6 億、折舊上升；2028 年以營收約 98 億美元、平均毛利率約 35%、費用約 11.2 億美元、稅率 16% 算出約 3.25 美元，低於共識 3.61；2029 年起成長放緩。終端 15 倍對照自身 FY2 14.7 倍，事實表未涵蓋同業 Fwd P/E。","bear":"2028 年光通訊消化，毛利率卡在 31%～33%，資本支出變成折舊，手機不回升，FY2029 谷底 1.80 美元。機率 30% 依據：2023、2024 年營收各年減約 9%，產業約 4.4 年一輪，內生成長上限算不出來。終端 12 倍取自成長率降到 10% 的本益比壓縮情境。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023、2024 年營收各年減約 9%，2024 年毛利率掉 390bp，再認列 9.35 億美元 Malta 減損。本輪資本支出規模更大：2027 年 40 億美元，約為 2026 年的 2.7～3.6 倍。","assumption":"光通訊需求在 2028 年不消化，成熟製程 ASP 不回落。","consequence":"毛利率卡在 31%～33%，FY2029 EPS 跌到 1.80 美元，股價落在 18～23 美元。","ruling":"採納，列入 Bear 30% 與唯一致命數字；但不足以否定主線，因為 2027 已訂滿，部分產能有客戶預付。","watch":"2027 Q4 毛利率、2028 訂單能見度、稼動率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#4"]},{"view":"論點成功但股東經濟變差","evidence":"美國政府持股約 7%，股數由 5.58 億升到約 6 億（+7.5%）；美日 Malta 廠由 SPV 持有，GF 收費並分 EBITDA；客戶預付換來的是未來產能承諾。","assumption":"2028 年底 EPS 約 4 美元與長期 6 美元的目標，在新股數下仍然成立。","consequence":"同樣淨利在 6 億股下，4 美元變 3.72 美元；若預付合約鎖價，漲價的好處會少一截。","ruling":"採納。Base 已用 6 億股，EPS 低於共識。","watch":"Q4 法說是否以新股數重述 EPS 目標，預付合約是否含價格條款。","fact_refs":["f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比仍 19.7 倍；賣方均價 80.24 美元是 10 月前快照，Axelrod 2026-10-07 評持有；Q3 指引公布後盤前跌約 5.5%，兩個來源對指引解讀不一；2024 年 9 月單月跌 13.8%。","assumption":"共識分母可信，2027 年 EPS 能到 2.63 美元。","consequence":"若 2027 年 EPS 只有 2.2 美元，現價對應 17.6 倍，便宜的說法不成立。","ruling":"部分反駁：現價已跌 47.7%，但跌幅不是安全邊際，FY2 14.7 倍要等共識更新才算數。","watch":"Q4 法說後 FY2 共識與股數假設。","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#6","cyclical_prior_downcycle_behavior#3"],"fact_refs":["f_fwd_pe_latest","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 48.24 → 本次 38.62（-19.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=48.24","side_b":"本次 price_at_dd=38.62","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 48.24 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 48.24 美元：Bull 價 117.6、Bear 價 28.8，五年期望值 +41.5%，基準年化 6.9%，不對稱比 3.0","side_b":"本次情境、股價仍用 48.24 美元：Bull 價 123.5、Bear 價 26.4，五年期望值 +42.0%，基準年化 6.5%，不對稱比 2.87","ruling":"先換情境、股價不動：五年期望值多 0.5 個百分點，基準年化少 0.4 個百分點。不對稱比由 3.0 變為 2.87。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 48.24 美元：五年期望值 +42.0%，基準年化 6.5%，不對稱比 2.87","side_b":"本次情境、股價 38.62 美元：五年期望值 +77.4%，基準年化 11.3%，不對稱比 5.79","ruling":"再換股價、情境不動：起點價下跌 19.9%，五年期望值多 35.4 個百分點，基準年化多 4.8 個百分點，不對稱比由 2.87 升到 5.79。合計五年期望值比前份多 35.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"進場首倉條件：前份門檻已達成，本次改用現金帳門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","side_b":"2026 Q4 法說（約 2027 年 2 月）：2027 自由現金流率指引 ≥8% 且已簽客戶預付 ≥10 億美元 → 重跑判斷後進場首倉","ruling":"前份三項條件全數達成（Q3 毛利率 31.4%、Q4 指引 31.5%、通訊基建與資料中心全年 60%～70%），這條觸發器已發火，所以重跑判斷。重跑後不直接建倉，因為 2026-11-04 才出現 2027 年 40 億美元淨資本支出與 6 億股，約束由毛利率驗證改為現金驗證，只等這一件事。","evidence_level":"高（公司法說）","settle_metric":"2026 Q4 法說的 2027 自由現金流率指引與已簽預付金額","if_then":["若 2027 自由現金流率指引 ≥8% 且已簽預付 ≥10 億美元，則重跑判斷後進場首倉，上限 3%。","若股價先漲但上述數字未出，則不追。","若股價先跌、但 Q4 法說數字達標，則分批反買。","若 2027 自由現金流率指引低於 5%，則不追，Base 的 2028 年 EPS 下修到 2.96 美元重算。"]},{"axis":"Single Thing 由未列改為 2027 年第四季毛利率","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未列唯一致命點（null）","side_b":"2027 年第四季 Non-IFRS 毛利率低於 33%（管理層目標 35%）。","ruling":"毛利率是最大的單一敏感度，每 1 個百分點約影響 2028 年 EPS 0.14 美元，故設為唯一致命點。","evidence_level":"中（敏感度為本文估算）","settle_metric":"2027 Q4 Non-IFRS 毛利率","if_then":["若 2027 Q4 毛利率低於 33%，持有則清倉，未持有則不追。","若 2027 Q4 毛利率達 35% 以上，解除此項疑慮。"]},{"axis":"停損指標由未列改為五項，觸發時減碼或清倉","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未列指標門檻（null）","side_b":"毛利率 2027 Q4 低於 33%；通訊基建與資料中心年增低於 30% 連 2 季；2027 自由現金流率低於 5% 或預付低於 10 億美元；稼動率低於 80%；2027 ASP 與組合合計低於 5%。","ruling":"前份摘要沒有可對帳的指標，本次全部新設。毛利率觸發則清倉，其餘觸發則減碼。","evidence_level":"中","settle_metric":"各季財報與法說"},{"axis":"護城河、跑道、陷阱、總評四欄維持前份，但兩邊證據都變強","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","trap"],"side_a":"Q3 毛利率新高、矽光子年化 10 億美元提前一年、台積電矽中介層 5 年 20 億美元、Marvell 與 Monolithic Power 合作、2027 產能訂滿。","side_b":"純代工份額約 5% 降到約 3%、中國擴產、矽光子新進者增加、雙來源料號降價。","ruling":"可調和，兩邊都成立，四欄維持：方向未翻、跑道中等、陷阱中度、總評 B。","evidence_level":"中","settle_metric":"特殊製程份額、ASP 年增率、矽光子營收","if_then":["若 2027 ASP 與組合合計達 +10% 且矽光子如期，總評可上調。","若矽光子營收連 2 季低於路徑，方向改判縮減，並減碼。"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#1"]},{"axis":"股價由 48.24 跌到 38.62 美元，估值結論仍為中性偏便宜","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"FY1 本益比由約 24.6 倍降到 19.7 倍；機率維持 25／45／30；最大回撤範圍因股價已跌而略收。","side_b":"三年共識 90 天完全未動，6 億股與新增折舊是否入模未知。","ruling":"價格確實更好，但分母有爭議，不升為便宜；機率不動，因利多與資本支出、稀釋的利空互相抵銷。","evidence_level":"中","settle_metric":"Q4 法說後 FY2 共識與股數假設","if_then":["若新股數下 FY2 共識仍 ≥2.5 美元，估值結論改為便宜。","若 FY2 共識低於 2.2 美元，便宜論點作廢，不追。"]},{"axis":"循環位置維持中循環，類別維持循環股","cause":"新證據","prior_field":["archetype","cycle_position"],"side_a":"偏早：晶圓量年增 7% 與 ASP 同步上升，P/S 在年度端點最低，股價跌 47.7%、賣方目標價遠高於現價，過去 3 年資本支出僅約營收一成，P/B 事實表未涵蓋。","side_b":"偏晚：毛利率 31.4% 歷史新高，8 吋稼動率近 90%，第三輪漲價，40 億美元擴產即將投入，2H26 電視與筆電備貨有庫存疑慮。","ruling":"六項訊號取中位，判中循環。循環判讀只套手機、車用、IoT 等成熟製程，光通訊段另計，不隨循環賣。","evidence_level":"中","settle_metric":"稼動率、ASP、資本支出占營收比","if_then":["若 2027 稼動率升至 95% 且資本支出持續超前訂單，改判晚循環，減碼。","若 ASP 轉為年減且稼動率跌破 80%，改判下行，不追。"]},{"axis":"2027 年 40 億美元淨資本支出與自由現金流目標","cause":"新證據","side_a":"CFO（2026-11-04）：約三分之一由客戶預付支持，補助與投資抵減也會挹注，仍維持自由現金流目標。","side_b":"本包算術：10% 自由現金流率需基礎營業現金流約 35 億美元，2026 Q2、Q3 年化僅 14.9 億美元，差約 20 億美元；就算補助另計約 7.6 億美元也補不滿。","ruling":"可調和，程度差異，等公司給數字。在公司給出前，採 B 側，不把 10% 計入 Base。償債不是問題，淨現金約 21 億美元、循環額度 15 億美元未動用。","evidence_level":"中（公司口徑與本包算術，未含 2027 折舊與營運資金）","settle_metric":"2026 Q4 法說的 2027 自由現金流率指引","if_then":["若指引 ≥8% 且已簽預付 ≥10 億美元，則重跑判斷。","若指引低於 5%，則不追。"]},{"axis":"每股目標與新股數","cause":"新證據","side_a":"2026-05-07 CFO：2028 年底 EPS 約 4 美元，長期 6 美元。","side_b":"2026-11-04 CFO：Q4 股數約 5.75 億，2027 年起約 6 億；Atif Malik 問新合作是否改變長期模型，CEO 答現在更新數字太早。","ruling":"目標未按新股數重述。同樣淨利下 4 美元約變 3.72 美元，美日計畫的長期增益 0.50～0.75 美元只部分抵銷，且只含第一座廠、最終協議未簽。","evidence_level":"高","settle_metric":"公司是否重述每股目標","if_then":["若公司以 6 億股重述仍維持 4 美元，Base 的 2028 年 EPS 上調至共識水準。","若公司下修每股目標，則不追。"]},{"axis":"毛利率橋接的折舊與稼動率假設","cause":"新證據","side_a":"2026-05-07 CFO：折舊逆風約一點；2026-08-05 CFO：稼動率還有約 10 點可成長。","side_b":"2026-11-04：2027 淨資本支出 40 億美元，Q3 稼動率仍在高 80%，CFO 說擴產持續放大分母。以 7 年直線折舊作假設（事實表未涵蓋年限），每年新增約 5.7 億美元折舊，約占 Base 2028 年營收 5.8 個百分點。","ruling":"投資人日的橋接是在較小資本支出下做的，公司只說目標不變，沒有更新折舊假設。Base 把 2028 年底毛利率放在約 38%，低於目標 40%。此假設未含舊資產折舊到期的抵銷。","evidence_level":"中（折舊年限為假設）","settle_metric":"每季折舊金額與 Non-IFRS 毛利率","if_then":["若 2027 Q2 毛利率達 33% 以上，折舊疑慮減半。","若 2027 Q2 毛利率低於 31.5%，則不追。"]},{"axis":"手機展望前後不一","cause":"新證據","side_a":"2026-05-07 Michael Hogan：手機預期大致持平，長期不倚賴其成長。","side_b":"2026-08-05 起下修為全年年減低十幾個百分點；2026-11-04 C.J. Muse 推算 Q4 年減約 22%、較前波峰約 −40%，CFO 認可此推算。","ruling":"手機不再是穩定基盤。Base 不假設 2027 年回升，高階占比是公司說法，未經第三方驗證。","evidence_level":"中","settle_metric":"手機段每季年增率","if_then":["若手機段年減超過 25% 連 2 季，則減碼。"],"evidence_refs":["end_markets#2","end_markets#7","supply_demand_durability#5","supply_demand_durability#7"]},{"axis":"矽光子客戶與市占口徑","cause":"新證據","side_a":"2026-03-10 管理層自稱矽光子代工第一；2026-08-05 稱前五大收發器廠有 4 家接洽。","side_b":"2026-03-10 分析師引述競爭者稱逾八成市占，管理層未正面回答；2026-11-04 口徑改為前十大中 7 家，分母換了，無法與前次比較。","ruling":"份額兩邊都不採信，只看矽光子實際營收。","evidence_level":"低","settle_metric":"矽光子營收與 2027 年底年化 10 億美元","if_then":["若 2027 Q4 矽光子季營收低於 2 億美元，則減碼。"]},{"axis":"現在就買的最強論證","cause":"新證據","side_a":"Q3 全面超前、前份進場條件全數達成、FY2 14.7 倍、股價半年跌 47.7%、2027 訂滿、客戶願意預付；等到 Q4 法說，股價可能已先反彈。","side_b":"現金帳差約 20 億美元沒有說明，共識分母未更新，股價跌破 250 週線約 24%，下跌原因包內無第三方解讀。","ruling":"採 B 側。等待成本只有約三個月，而 Q4 法說會直接回答最大的未知數。","evidence_level":"中","settle_metric":"2026 Q4 法說","if_then":["若法說前股價大漲但數字未出，則不追。"]}],"triggers":[{"n":1,"text":"Q4 法說現金帳過關才進場首倉","type":"估值rearm","maps_to":"H3","metric":"2027 自由現金流率指引與已簽客戶預付","threshold":"≥8% 且 ≥10 億美元","action":"重跑判斷後進場首倉，上限 3%","source_freq":"公司法說，每季","date":"2027-02"},{"n":2,"text":"毛利率未達路徑的唯一致命點","type":"Single Thing","maps_to":"H1","metric":"2027 Q4 Non-IFRS 毛利率","threshold":"低於 33%","action":"持有則清倉，未持有則不追","source_freq":"公司季報，每季","date":"2028-02"},{"n":3,"text":"矽光子年化 10 億美元是否如期","type":"假設驗證","maps_to":"H2","metric":"2027 Q4 矽光子季營收","threshold":"≥2.5 億美元","action":"達標維持 Base，低於 2 億美元則減碼","source_freq":"公司法說，每季","date":"2028-02"},{"n":4,"text":"毛利率中途檢查","type":"假設驗證","maps_to":"H1","metric":"2027 Q2 Non-IFRS 毛利率","threshold":"≥33%","action":"低於 31.5% 則不追，持有則減碼","source_freq":"公司季報，每季","date":"2027-08"},{"n":5,"text":"光通訊需求消化","type":"風險","maps_to":"R3","metric":"通訊基建與資料中心年增率","threshold":"低於 30% 連 2 季","action":"減碼","source_freq":"公司季報，每季","date":null},{"n":6,"text":"手機繼續惡化","type":"風險","maps_to":"R4","metric":"手機段年增率","threshold":"年減超過 25% 連 2 季","action":"減碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["end_markets#2"]},{"n":7,"text":"成熟製程漲價失敗","type":"減碼","maps_to":"R2","metric":"2027 ASP 與組合合計漲幅","threshold":"低於 5%（公司指引約 10%）","action":"減碼","source_freq":"公司法說，每季","date":"2027-12"},{"n":8,"text":"下次完整複審","type":"複審日期","maps_to":"H3","metric":"2026 Q4 財報與 2027 全年框架","threshold":"法說後一週內完成","action":"重跑判斷","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"Non-IFRS 毛利率","bear_threshold":"2027 Q4 低於 33%（目標 35%）","window":"2027 Q4 財報","source":"公司季報與法說","last_status":"ok"},{"metric":"通訊基建與資料中心年增率","bear_threshold":"低於 30% 連 2 季","window":"2027 全年","source":"公司季報","last_status":"ok"},{"metric":"2027 自由現金流率與已簽客戶預付","bear_threshold":"低於 5%，或預付低於 10 億美元","window":"2026 Q4 法說至 2027 全年","source":"公司法說與現金流量表","last_status":"unknown"},{"metric":"稼動率","bear_threshold":"跌破 80%","window":"每季","source":"公司法說","last_status":"ok"},{"metric":"2027 ASP 與組合合計漲幅","bear_threshold":"低於 5%（公司指引約 10%）","window":"2027 全年","source":"公司法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#5","reason":"來源是 Simply Wall St 社群敘事，非公司或機構資料，也沒有具名進入者或數字；先進製程落後對 GF 不是新資訊，公司本來就不做先進製程。"}],"action_conditions":{"rearm_trigger":"2026 Q4 法說（約 2027 年 2 月）：2027 自由現金流率指引 ≥8% 且已簽客戶預付 ≥10 億美元 → 重跑判斷後進場首倉","exec_line":"目前不建倉。條件達成且重跑通過後，首倉不超過 3%，分兩批；股價先漲不追，股價先跌而數字達標則分批反買。","holding_cap":"重跑通過後首倉不超過 3%"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2 14.7 倍定價，等於假設 2028 年 EPS 就是週期頂點；但 2027 年產能已訂滿、客戶願意預付、ASP 與組合合計約 +10% 都有公司口徑支持。這條理由要等現金帳過關才成立。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 2026 Q4 法說（約 2027 年 2 月）：2027 自由現金流率指引 ≥8% 且已簽客戶預付 ≥10 億美元；等的是事件，不是價位。"},"thesis":{"H":[{"id":"H1","text":"產品組合把 Non-IFRS 毛利率從 2026 Q3 的 31.4% 推到 2027 年底 35%、2028 年底接近 40%。","2y":"2028 Q4 毛利率 ≥38%（管理層目標 40%）","5y":"FY2031 毛利率 ≥38%，且跨過一次下行仍守住","10y":null,"threshold":"2027 Q4 ≥35%；2028 Q4 ≥38%","source":"公司季報與法說，每季","drift_rule":"實際值低於路徑 5% 以上連 2 季為削弱，低於 10% 以上連 3 季為反轉。"},{"id":"H2","text":"光通訊帶動通訊基建與資料中心 2027 年維持 30% 以上成長，矽光子 2027 年底年化約 10 億美元。","2y":"2027 Q4 矽光子季營收 ≥2.5 億美元","5y":"2030 年矽光子營收 ≥20 億美元","10y":null,"threshold":"通訊基建與資料中心年增 ≥30%；矽光子 2027 年底年化 ≥10 億美元","source":"公司季報與法說；矽光子營收只在法說揭露","drift_rule":"實際值低於路徑 5% 以上連 2 季為削弱，低於 10% 以上連 3 季為反轉。"},{"id":"H3","text":"2027 年 40 億美元淨資本支出在客戶預付與補助支持下，自由現金流率不低於 8%，且投資在兩年內開始回收。","2y":"2027 調整後自由現金流率 ≥8%","5y":"2027～2031 平均自由現金流率 ≥10%","10y":null,"threshold":"2027 自由現金流率 ≥8%；已簽預付 ≥10 億美元","source":"6-K 現金流量表與法說，每季","drift_rule":"實際值低於路徑 5% 以上連 2 季為削弱，低於 10% 以上連 3 季為反轉。"}],"R":[{"id":"R1","text":"現金帳對不上：2027 年資本支出大於營業現金流與預付的合計，自由現金流目標落空。","h_ref":"H3","clock":"⚡","threshold":"2027 自由現金流率指引低於 5%，或已簽預付低於 10 億美元"},{"id":"R2","text":"成熟製程週期回落：重演 2023、2024 年營收各年減約 9%、毛利率掉約 4 個百分點，並再有減損。","h_ref":"H1","clock":"🔥","threshold":"毛利率轉為年減，或稼動率跌破 80%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#4"]},{"id":"R3","text":"光收發器 2028 年過度建置，新進者增加，預付產能用不完。","h_ref":"H2","clock":"🔥","threshold":"通訊基建與資料中心年增低於 30% 連 2 季，或管理層不再說 2028 訂滿"},{"id":"R4","text":"手機仍占 Q3 營收 32%，記憶體短缺與高階機需求轉弱，拖累稼動率與組合。","h_ref":"H1","clock":"🔥","threshold":"手機段年減超過 25% 連 2 季","evidence_refs":["supply_demand_durability#5","supply_demand_durability#7","end_markets#2","end_markets#7"]},{"id":"R5","text":"客戶集中：前兩大客戶 2024 年占 27%，前十大 2021 年占晶圓出貨 67%，最新比重待新資料。","h_ref":"H2","clock":"🐢","threshold":"單一客戶占營收超過 20%，或失去前兩大客戶任一主力平台","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R6","text":"供應鏈與出口管制：單一 SOI 供應商占比升到 71.4%，美中緊張持續，2024 年曾因出口管制違規被罰。","h_ref":"H1","clock":"🐢","threshold":"SOI 供應中斷造成單季出貨缺口，或出口管制案件罰金與限制擴大到影響單一客戶出貨","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","regulatory_antitrust#2","reg_tariff_export#2"]}],"single_thing":{"description":"2027 年第四季 Non-IFRS 毛利率低於 33%（管理層目標 35%）。","why_fatal":"這是最大的單一敏感度。2028 年營收約 98 億美元時，毛利率每差 1 個百分點，EPS 差約 0.14 美元（9,800 萬×84%÷6 億股），占 Base 3.25 美元的 4.2%；差 5 點就少 0.69 美元，約兩成，比營收少一成的影響（約 0.55 美元）更大。","if_happens":"毛利率路徑失效，Base 往 Bear 靠。持有則清倉，未持有則不進場，要等毛利率連 2 季回到 34% 以上才重跑。","how_monitor":"每季財報的 Non-IFRS 毛利率與下一季指引；2027 Q1 起季度值低於 31.5% 就提前警示。","probability":"約 30%（2027 年底前）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.7,"peg_fy2":0.47,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":1.59,"FY2026E":1.96,"FY2027E":2.63,"FY2028E":3.61},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識 Non-IFRS EPS（2026-11-07，12 月年度）；FY2025A 1.59 為 IFRS 稀釋 EPS，Non-IFRS 基期事實表未涵蓋，兩者口徑不同。"},"catalysts":[{"date":"2026-12-01","type":"guidance","event":"UBS Global Technology and AI Conference 爐邊談話","impact":"低","watch":"是否補充 2027 現金帳與預付簽約進度"},{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"美日 Malta 計畫最終協議、政府股權簽署與動工","impact":"中","watch":"最終條款；2027 年 EPS 增益 0.10～0.15 美元是否維持"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 全年框架（月份依往年推估）","impact":"高","watch":"2027 自由現金流率指引、以新股數重述的 EPS 目標"},{"date":"2027-Q1","date_precision":"quarter","type":"capacity","event":"客戶產能預付協議簽約（CFO 稱大致在 2026 Q4 至 2027 年初完成）","impact":"高","watch":"已簽金額是否達 10 億美元以上，是否含價格條款"},{"date":"2028-Q2","date_precision":"quarter","type":"capacity","event":"台積電矽中介層在 Malta 開始量產（公司稱 2028 上半年）","impact":"中","watch":"毛利率是否高於長期目標，是否有第二家客戶"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2 14.7 倍定價，等於假設 2028 年 EPS 就是週期頂點；但 2027 年產能已訂滿、客戶願意預付、ASP 與組合合計約 +10% 都有公司口徑支持。這條理由要等現金帳過關才成立。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-47.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
