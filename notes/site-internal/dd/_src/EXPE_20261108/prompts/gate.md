你是 DD 管線 v20 的判斷層閘（gate），標的 EXPE（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（43 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝4938 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi1_ebitda_non_gaap_non_gaap`（q1_business）｜調整後 EBITDA（公司主要 non-GAAP 獲利指標；新聞稿未報 non-GAAP 營業利益）＝1689 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝1326 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi5_gross_bookings`（q1_business）｜總預訂額 Gross Bookings＝34008 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi6_booked_room_nights`（q1_business）｜預訂間夜數 Booked Room Nights＝115.7 m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi7_q4_2026`（q1_business）｜Q4 2026 指引（營收）＝3,690–3,750 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi8_2026`（q1_business）｜全年 2026 指引（營收）＝16,370–16,430 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_peer_expe_operating_margin_pct`（q2_moat）｜EXPE 營業利益率＝18.39 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_expe_fcf_margin_pct`（q2_moat）｜EXPE FCF 利潤率＝23.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bkng_operating_margin_pct`（q2_moat）｜BKNG 營業利益率＝32.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bkng_fcf_margin_pct`（q2_moat）｜BKNG FCF 利潤率＝32.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_abnb_operating_margin_pct`（q2_moat）｜ABNB 營業利益率＝20.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abnb_fcf_margin_pct`（q2_moat）｜ABNB FCF 利潤率＝36.93 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tcom_operating_margin_pct`（q2_moat）｜TCOM 營業利益率＝18.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TCOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_trip_operating_margin_pct`（q2_moat）｜TRIP 營業利益率＝3.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRIP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_trip_fcf_margin_pct`（q2_moat）｜TRIP FCF 利潤率＝-1.18 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRIP.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.89 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝24.55 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝27.92 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝16382.5 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（35 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝17452.63 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（36 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝-1399 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收＝2.43 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（Form 8-K 附件，IR 入口 ir.expediagroup.com）https://www.sec.gov/Archives/edgar/data/0001324424/000132442426000059/earningsrelease-q32026.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識未取得（未於新聞稿揭露，未另查）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝122.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 5689.0、現金 5567.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.71 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝118.57 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝259.24 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝12.41 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 20.89，分子＝快照價 259.24｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝15.2 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.89 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝49.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝49.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.9 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝36.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝36.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.05 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（20.9 → 20.89）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.12 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（24.58 → 24.55）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.36 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（28.02 → 27.92）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝30861.2 USD m｜期間與口徑：2026-11-08／市值 30739.2 ＋ 淨負債 122.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_w52`（q5_valuation）｜52 週均線＝260.8 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝223.04 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝164.01 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝13.13 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝42.01｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 新增風險：生成式／代理式 AI 帶來新進入者，可能使 Expedia 流失份額、直接訂房率下降、行銷費用上升。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出供應商直營通路（航空、飯店）積極搶直接分銷，並提及 Google 持續強化自家旅遊產品與搜尋位置。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-13）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱競爭強且增加，部分對手提供供應商與旅客更優惠條款與更佳介面技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-13）｜affects：moat_trend
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Skift 解析 Expedia 10-K：代理式 AI 旅遊競爭新風險揭露。
  - 來源：Skift What Expedia Says About the Coming Agentic Travel Fight（as_of 2026-02-20）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K FY2025 Item 3 未列出反壟斷或政府調查為重大訴訟，主要訴訟為各司法管轄區的住宿稅／占用稅訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings（as_of 2026-02-13）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：公司過去曾涉及多國競爭主管機關對價格平價條款的調查，並以自願承諾處理；無法預測未來監管行動。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：2026-10 提起全國性反壟斷集體訴訟 Andrews v. Expedia Group（W.D. Wash.），指控平價條款與搜尋排名懲罰使飯店價格偏高；Expedia 稱指控無理由。
  - 來源：Honolulu Star-Advertiser（as_of 2026-10-17）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：平台關鍵功能遷移至 AWS 後，公司依賴 AWS 服務可用性，任何影響 AWS 基礎設施與可用性的事件都會波及公司。
  - 來源：Expedia Group Form 10-K FY2025（as_of 2026-02-15）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2025-10 AWS US-East-1 中斷事件，Expedia 列為受影響的旅遊公司之一（次級來源）。
  - 來源：Skift / travelupdate.com 彙整（as_of 2025-10-20）｜affects：decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 將烏克蘭戰爭、以哈戰爭等地緣衝突列為會突然改變旅遊行為的風險因子；無製造產地，未見單一供應商集中揭露。
  - 來源：Expedia Group Form 10-K FY2025（as_of 2026-02-15）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q1 2026 10-Q：美國內需疲弱與入境國際旅遊偏弱壓抑機票價格
  - 來源：Expedia Group 10-Q Q1 2026（as_of 2026-05-07）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Expedia 10-K FY2025 風險因子指出 AI、雲端、替代平台與行動裝置的成長及擅用新技術的利基競爭者，已經且將持續需要新的昂貴投資，轉型可能干擾資源與服務並提高對第三方服務商的依賴。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Expedia 在 ChatGPT 與 Claude 有訂房整合，並將 emerging AI-powered platforms 列為競爭威脅；OpenAI 縮減 ChatGPT 直接結帳；Expedia 自家調查僅 8% 旅客願意透過 AI 平台訂購。
  - 來源：GeekWire：Expedia Group sees reward and risk in the rise of AI-powered travel（as_of 2026-04-01）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#0`（channel_business_model_shift｜方向 -｜狀態 ok）：10-K 述及競爭加劇，含供應商直營網站、Gen AI 與 AI agent 業者；B2B 以 Rapid API、白標、TAAP 等通路供貨
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 列示：Helms-Burton 訴訟八件中四件仍在進行；以色列推定集體訴訟（Ze'ev）集體認證聲請仍待決；Jasper County 稅務訴訟已和解並於 2026-01-05 駁回。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-13）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 列示以色列推定集體訴訟（Ze'ev，2018 年起）集體認證聲請仍待決；Helms-Burton 四件仍進行；未見 2024–2026 證券集體訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-13）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":720.0,"bear_5y_price":180.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":77.5,"ev5y_pct":65.1,"irr_base_pct":12.2,"asym_ratio":3.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.89,"pe":12.41,"basis":"FY2026 共識 EPS，財年只剩一季，視為當年度口徑；終端倍數同樣乘當年度 EPS"},"eps":{"bull":[25.6,30.2,35.0,40.0,45.0],"base":[23.8,26.7,29.6,32.5,35.4],"bear":[21.5,20.0,19.0,19.5,20.0]},"pe":{"bull":16,"base":13,"bear":9},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.71,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EXPE_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Derek Andersen｜guidance：Q3 gross bookings 財測區間與年增幅（原話："we expect gross bookings of $32.2 billion to $32.8 billion"）
- 2026-08-05｜CFO Derek Andersen｜guidance：Q3 調整後 EBITDA 財測與隱含 margin（原話："implying a margin of 32.5% to 32.8%"）
- 2026-08-05｜CFO Derek Andersen｜guidance：上調全年 gross bookings 財測（原話："gross bookings of $129.5 billion to $130.8 billion"）
- 2026-08-05｜CFO Derek Andersen｜guidance：上調全年 EBITDA margin 擴張幅度（原話："adjusted EBITDA margin expansion of 150 to 175 basis points"）
- 2026-08-05｜CFO Derek Andersen｜guidance：Q3 成長減速的原因：比較基期較高與匯率（原話："reflecting tougher comparisons as we lap faster growth"）
- 2026-08-05｜CFO Derek Andersen｜guidance：下半年 bookings 與間夜成長都將減速，bookings 減速較多（原話："although probably more so on the bookings side"）
- 2026-08-05｜CFO Derek Andersen｜guidance：財測假設 Q2 至 Q3 初的健康需求延續（原話："healthy demand trends that we have seen through Q2"）
- 2026-08-05｜CFO Derek Andersen｜margin：Q2 調整後 EBITDA 與 margin 數字（原話："representing a margin of 25.9%"）
- 2026-08-05｜CFO Derek Andersen｜margin：Q2 margin 擴張的三項來源拆解（原話："cost efficiencies, consumer marketing leverage and the flow"）
- 2026-08-05｜CFO Derek Andersen｜margin：Q3 margin 擴張放緩的原因：基期、B2B 投資、淨匯率（原話："lapping of prior year cost actions, ongoing investment"）
- 2026-08-05｜CFO Derek Andersen｜margin：全年指引隱含 Q4 中點約擴張 50 bp，並說明擴張不會線性（原話："we'd be expanding by about 50 basis points there"）
- 2026-08-05｜CFO Derek Andersen｜margin：管理費用持平而營收成長 14%（原話："overheads were flat year-over-year in the most recent"）
- 2026-08-05｜CFO Derek Andersen｜margin：管理層說行銷結構性改善會延續，但下半年開始遇到高基期（原話："the structural improvements that we've made on the marketing"）
- 2026-08-05｜CEO Ariane Gorin｜margin：B2C 行銷支出僅增 1%，bookings 增 8%（原話："We grew our bookings 8% while leveraging marketing spend"）
- 2026-08-05｜CFO Derek Andersen｜margin：B2B 利潤率短期驅動因素：夥伴組合與自身投資步調（原話："partner mix and the pace of our own investments"）
- 2026-08-05｜CFO Derek Andersen｜margin：B2B 開支增加歸因於 Tiqets 併入與匯率避險損益表位置（原話："we had the digestion of Tiqets and that acquisition in Q2"）
- 2026-08-05｜CFO Derek Andersen｜commitment：CFO 承諾持續推動營運效率與提高利潤率（原話："we're committed to continuing to drive our strategic pillar"）
- 2026-08-05｜CFO Derek Andersen｜commitment：CFO 表示一邊投資 B2B 一邊能持續改善利潤率（原話："we can invest and continue to make progress on margins"）
- 2026-08-05｜CEO Ariane Gorin｜commitment：已連續第五季優於財測高標（原話："We exceeded the high end of both our top- and bottom-line"）
- 2026-08-05｜CFO Derek Andersen｜capital_allocation：Q2 買回股數、金額與均價（原話："we repurchased roughly 880,000 shares for $200 million"）
- 2026-08-05｜CFO Derek Andersen｜capital_allocation：資本配置優先順序不變，買回為機會性（原話："Our capital allocation priorities remain unchanged"）
- 2026-08-05｜CFO Derek Andersen｜capital_allocation：近 12 個月自由現金流金額（原話："which reached $4.5 billion on a trailing 12-month basis"）
- 2026-08-05｜CEO Ariane Gorin｜capital_allocation：宣布收購 CarTrawler 與 Layla，並提及已收購 Tiqets（原話："we announced the acquisition of Layla"）
- 2026-08-05｜CEO Ariane Gorin｜capital_allocation：B2B 一站式旅遊商店的收購佈局（原話："announced our intent to acquire CarTrawler"）
- 2026-08-05｜CEO Ariane Gorin｜competition：CEO 回應 B2B 競爭加劇的提問（原話："it's always been a competitive space"）
- 2026-08-05｜CEO Ariane Gorin｜competition：B2B 合約部分獨家、部分非獨家（原話："some relationships are exclusive, some are not exclusive"）
- 2026-08-05｜CEO Ariane Gorin｜competition：自然搜尋流量與 SEO／AEO 現況（原話："organic search traffic is stable to slightly up"）
- 2026-08-05｜CEO Ariane Gorin｜competition：SEO 偏軟但近幾季趨穩，並稱至少拿到合理份額（原話："SEO has remained a bit soft, but it's stabilized"）
- 2026-08-05｜CEO Ariane Gorin｜competition：搜尋演算法與頁面變動更頻繁，公司保持警戒（原話："algorithms and search page changes more prevalent"）
- 2026-08-05｜CEO Ariane Gorin｜product：AEO 仍是小管道但為成長最快管道之一；agentic 流量仍小（原話："AEO, it's still a small channel"）
- 2026-08-05｜CEO Ariane Gorin｜product：對話式 AI 功能目前未帶動轉換，但帶來更多旅客意圖資訊（原話："you get over 60% more information about traveler intent"）
- 2026-08-05｜CEO Ariane Gorin｜product：Expedia 品牌連續創下 attach rate 新高（原話："another quarter of record attach rates"）
- 2026-08-05｜CEO Ariane Gorin｜product：Uber 合作不評論，指引中不重大（原話："it's not going to be material to our guidance"）
- 2026-08-05｜CFO Derek Andersen｜product：廣告業務成長與 Q1 持平，並計畫擴及 B2B 與 Vrbo（原話："growth was stable relative to Q1 and Q2"）
- 2026-08-05｜CEO Ariane Gorin｜product：成為首家配銷 Allegiant 的 OTA，涵蓋全部美國商業航空（原話："we became the first OTA to distribute Allegiant flights"）
- 2026-08-05｜CEO Ariane Gorin｜customer：Q2 間夜成長及分區拆解（原話："Total booked room nights were up 6%"）
- 2026-08-05｜CEO Ariane Gorin｜customer：B2C bookings 增 8%，美國成長為 15 季最快（原話："driven by our fastest U.S. growth in 15 quarters"）
- 2026-08-05｜CEO Ariane Gorin｜customer：B2B 連續第 20 季雙位數成長（原話："20th consecutive quarter of double-digit growth"）
- 2026-08-05｜CEO Ariane Gorin｜customer：忠誠會員數低個位數成長，高階會員較快（原話："Active loyalty members increased low single digits"）
- 2026-08-05｜CFO Derek Andersen｜customer：World Cup 對 Q2 影響有限，反映在 ADR 多於間夜（原話："driven by our fastest U.S. growth in 15 quarters"）
- 2026-08-05｜CFO Derek Andersen｜customer：B2B 合作夥伴超過 7 萬家（原話："We have over 70,000 partners today"）
- 2026-08-05｜CEO Ariane Gorin｜risk：歐洲，特別是出境旅遊，仍承壓（原話："Europe remained pressured, particularly outbound travel"）
- 2026-08-05｜CFO Derek Andersen｜risk：中東衝突透過油價產生次級影響（原話："secondary impacts impacting jet fuel prices"）
- 2026-08-05｜CEO Ariane Gorin｜risk：美國與墨西哥旅遊在前季安全事件後恢復正常（原話："we've seen a normalization"）
- 2026-08-05｜CFO Derek Andersen｜risk：下半年面對更高的比較基期（原話："we do have much tougher comps in the second half of the year"）
- 2026-08-05｜CEO Ariane Gorin｜risk：AI 使用的 token 成本，管理層稱審慎管理（原話："we're managing token costs thoughtfully"）

### 問答異常語氣（迴避／改口／保留）
- EXPE_Q2_2026_Earnings_Call_20260805.md｜問：Naved Khan 詢問 Uber 合作的早期情況與財測納入多少貢獻｜答法：拒絕評論個別夥伴，僅說對財測不重大，未給數字
- EXPE_Q2_2026_Earnings_Call_20260805.md｜問：Lloyd Walmsley 詢問 AEO 是否比同業更有意義、是否短期會變重要｜答法：未回答相對同業表現，說太早判斷誰拿得多，也未給占比或時程
- EXPE_Q2_2026_Earnings_Call_20260805.md｜問：Kevin Kopelman 詢問美墨旅遊在安全事件後的進展｜答法：僅簡短回答「normalization」，重複一次，未給數字
- EXPE_Q2_2026_Earnings_Call_20260805.md｜問：Cameron Lynch 詢問 B2C margin 擴張在 2027 的跑道｜答法：只解釋本季驅動因素，未回應 2027 年展望
- EXPE_Q2_2026_Earnings_Call_20260805.md｜問：Kevin Kopelman 詢問 B2B 銷售與行銷費用年減及下半年看法｜答法：改談夥伴組合與投資，未直接回答該費用項目下滑原因或下半年數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 1 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Expedia Group largest customer second-source OR in-house 2026；Expedia Group single-source risk customer diversify supplier

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"EXPE","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Expedia Group, Inc."},"oneliner":"全球兩大線上旅遊平台之一，B2B 帶成長、B2C 行銷效率帶利潤。12.4 倍預估本益比定價的是 AI 代理搶走訂房入口的疑慮，B2C 利潤率守不守得住，決定這個折價該不該收斂。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EXPE_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是住宿佣金與商家差價，另有機票、廣告與 B2B 供貨收入。錢卡在「誰掌握訂房入口」這一節：入口在自己手上利潤率就高，入口在 Google 或 AI 代理手上就得付過路費。","reasoning":"第三季營收 49.38 億美元、總預訂額 340.08 億美元、間夜 1.157 億，變現率 14.5%（旺季，全年指引約 12.5%）。依 2026-11-04 財報新聞稿，B2C 營收 30.65 億美元，占 62%，調整後 EBITDA 13.31 億美元，利潤率 43.4%；B2B 營收年增 23%，利潤率 27.5%，年減 134bp。GAAP 營業利益 13.26 億美元，單季利益率 26.9%，TTM 18.39%。第四季營收指引 36.9～37.5 億美元，全年 163.7～164.3 億美元。單點依賴有兩個：流量依賴 Google 等上層入口，基礎設施依賴 AWS，2025 年 10 月 US-East-1 中斷時公司在受影響名單內。B2B 夥伴 7.5 萬家，管理層稱沒有過度集中，前幾大占比事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi1_ebitda_non_gaap_non_gaap","f_kpi2_gaap","f_kpi5_gross_bookings","f_kpi6_booked_room_nights","f_kpi7_q4_2026","f_kpi8_2026","f_peer_expe_operating_margin_pct"],"verdict_values":{"revenue_quality":"以交易抽成為主，沒有合約鎖定的經常性收入，品質靠回頭客與直接訂房支撐，三分之二訂單來自自有入口。廣告是高毛利補充，但第三季成長由 13% 放緩到 7%。","unit_econ_note":"單位經濟看 B2C 行銷效率：第二季 B2C 預訂增 8%、行銷支出只增 1%；第三季營收增 12%、管理費用只增 1%。固定成本槓桿向上時很快，向下時也一樣快，第四季利潤率指引 22.5%～23.5% 已反映營收放緩後槓桿縮小。","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"資產輕、靠旅客預付款周轉，2024 到 2026 年指引累積擴張逾 4 個百分點利潤率，需求仍有循環。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期在擴張段後半，需求放緩屬週期性，線上化屬結構性。第三季間夜 +7%，ADR 由第二季 +5 放緩到 +2，第四季預訂指引 +3.3%～+5.2%。美國飯店供給 2026 年 +0.4%、2027 年 +0.6%，在建客房 12 年低點（CoStar／STR）；Phocuswright 估全球旅遊預訂由 2024 年約 1.6 兆美元增至 2027 年逾 1.8 兆美元，約三分之二線上。","bargaining":{"up":"上游是飯店與航空。頭部供應商積極導直營，長尾獨立飯店較依賴平台帶客。美國新增供給低，飯店不缺定價空間。","down":"旅客每次訂房都能換平台，轉換成本接近零，靠會員與價格維持。B2B 夥伴做大會升級分潤等級，是該分部利潤率下滑的第一原因。","geo":"美國、EMEA 與其他地區都有曝險，第四季指引點名中東與歐洲的長程航線受擾；沒有單一製造或供應產地風險。"},"profit_pool_dir":"利潤正往上層入口與頭部供應商兩端被擠，平台中間層靠規模與售後守住；5 年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"全球旅遊總預訂","value":"2024 年約 1.6 兆美元，2027 年估逾 1.8 兆美元，約三分之二線上（Phocuswright，2025）"},{"item":"公司總預訂額占比","value":"2026 年指引 1,314～1,319 億美元，約當全球 7%～8%"},{"item":"B2B 可觸及市場","value":"CEO 定義為逾 3 兆美元旅遊市場扣掉供應商直營與最大幾家線上旅遊平台後的其餘部分，未量化，口徑與 Phocuswright 不同，公司份額未揭露"},{"item":"營業利益池 5 年占比變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定，等級 B。執行面在擴大，定價權穩定，但營業利益率仍比 Booking 低 14.4 個百分點，AI 代理會不會拿走入口要到 2028 年前後才看得清。","reasoning":"機制是雙邊規模加 B2B 供貨基礎設施：全球庫存、即時價格、付款與售後一次接好，三分之二訂單直接進自有入口，夥伴用同一套供貨。可證方向改用利潤率軸：TTM 營業利益率 18.39% 對 Booking 32.78%，FCF 利潤率 23.09% 對 32.84%；同業 ROIC 與歷史序列事實表未涵蓋，差距是否收斂無法驗證。公司自身利益率由 FY2022 的 10.19% 升到 FY2025 的 14.68%。評分：執行 8，已連六季超過財測高標，第三季管理費用只增 1%；定價權原 7，AI 上層入口屬生態攻擊扣一分，為 6。可能看錯的地方是第三季廣告成長由 13% 掉到 7%、活躍會員只有低個位數成長，定價權若再轉弱，方向要下修。","fact_refs":["f_peer_expe_operating_margin_pct","f_peer_expe_fcf_margin_pct","f_peer_bkng_operating_margin_pct","f_peer_bkng_fcf_margin_pct","f_peer_abnb_operating_margin_pct","f_peer_abnb_fcf_margin_pct","f_peer_tcom_operating_margin_pct","f_peer_trip_operating_margin_pct","f_peer_trip_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"雙邊市場規模加 B2B 供貨基礎設施，連接全球庫存、價格、付款與售後，並以會員與直接入口留住旅客。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：2024 到 2026 年指引利潤率累積擴張逾 4 個百分點，第三季總預訂額 +11%，公司稱優於產業。定價權穩定：Vrbo 費用調整預期不影響整體變現率，但 B2B 夥伴升級壓低利潤率、廣告放緩。兩者合併判為穩定。","competitor_notes":[{"name":"BKNG","strategy_note":"規模與利益率最強對手，TTM 營業利益率 32.78%，是行銷效率與直接訂房的標竿。2026 年 4 月也下修成長預期，但稱需求完好。"},{"name":"ABNB","strategy_note":"住宿替代品，與 Vrbo 直接競爭，FCF 利潤率 36.93%（TTM 至 6 月）。Vrbo 調整房東費用，管理層稱產業結構正在靠攏。"},{"name":"TCOM","strategy_note":"亞洲主要平台，營業利益率 18.19%（TTM 至 6 月）與 Expedia 接近，研發密度 24.33% 高於 Expedia 的 8.04%。雙方重疊程度事實表未涵蓋。"},{"name":"TRIP","strategy_note":"內容與導流型平台，營業利益率 3.1%、FCF 為負，說明沒有交易與供給閉環的旅遊入口很難變現，是「只做發現」的負面對照。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用營業利益率與 FCF 利潤率比較，只有單一 TTM 時點，無法判斷差距方向。","threats":[{"level":"🔴","text":"AI 代理與 Google 的上層入口：代理擅長發現，若訂房也留在代理內，Expedia 會變成付通路費的供貨商。目前流量很小、經濟條款未定，公司自家調查只有 8% 旅客願意透過 AI 平台訂購。若代理直連供應商、繞過平台，才升級為架構替代。分界年看 2028 年。","p":35,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"飯店與航空直營：10-K 點名供應商積極搶直接分銷，會員權益與價格有時優於平台。頭部連鎖壓力大，長尾獨立飯店仍需平台帶客。","p":40,"evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#0"]},{"level":"🟡","text":"同業條款競爭：部分對手給供應商與旅客更好的條款與介面，Booking 的規模差距使行銷戰不對等。","p":30,"evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（定性判斷）：營業利益率 18.39%，資產輕；投入資本事實表未涵蓋，數值無法計算。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者與付款者多半是同一位旅客，需求成立。旅遊是想要大於需要，短期可延後，第四季地緣事件就是例子；長期全球預訂仍在成長。問題不會消失，受挑戰的是「用線上旅遊平台解決」這個方案。"},{"item":"決策層級","level":"🟡","text":"替代要看每一次訂房。旅客換平台幾乎沒有成本，靠會員與直接入口留人，三分之二訂單來自直接入口，活躍會員只有低個位數成長。B2B 合約部分獨家、部分非獨家，整合成本較高，但夥伴升級會分走更多利潤。"},{"item":"價值鏈分配","level":"🟡","text":"上游有供應商直營，下游有流量入口收費。Booking 與 Expedia 占線上旅遊平台逾 200 億美元行銷支出的四分之三以上，利潤有一大塊付給上層流量。入口由單家分散成多家 AI，議價力可能改善；若收斂成少數代理，會更差。"},{"item":"社會容忍度","level":"🟡","text":"2026 年 10 月的全美反壟斷集體訴訟指控平價條款抬高房價，公司過去也曾在多國因平價條款被調查並作出自願承諾。目前沒有判決或罰款，但這是平台抽成的實際上限。"}],"roiic":"事實表未涵蓋：投入資本、資本支出、折舊攤銷與營運資金變動均未收錄，無法計算增量報酬。","reinvest_rate":"事實表未涵蓋：只知 2026 年前九個月收購支出 6.76 億美元，其餘再投資項目未收錄。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，本輪輸入不足未計算。成長題改用 FY2027 共識營收成長 6.5% 當代理上界，並以保守方式視為共識 EPS 成長超過內生天花板。"}}}},"q3_growth":{"verdict":"五年後的成長跑道屬中等：線上化已到約三分之二，沒有已驗證的第二條曲線可以算進來。B2B 是最接近的候選，但公司不給份額數字。","reasoning":"共識 EPS 為 FY2026 20.89、FY2027 24.55、FY2028 27.92 美元，兩年 CAGR 15.6%；FY2027 共識營收成長只有 6.5%。缺口約 9 個百分點，約 5 點靠利潤率擴張、約 4 點靠淨回購，併購不重大，可以歸因，但都不是內生成長。三年口徑缺 FY2025 非 GAAP 基期，事實表未涵蓋，改用兩年。CFO 2026-11-04 把行銷槓桿的說法改成速度略減，未來利潤率只說逐步進展，這是共識最脆弱的部分。B2B 第三季預訂 +19%，但 2026-11-04 被問到夥伴數與單一夥伴成長的拆分時，管理層沒有提供。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_2026"],"verdict_values":{"growth":{"driver_mix":"第三季總預訂額 +11%，由間夜 +7%、ADR +3%（匯率中性）貢獻，機票票價偏高也有幫助。EPS 端再加淨回購約 4% 與利潤率擴張，併購目前不重大。","runway_years":"不適用：線上滲透約三分之二，公司約占全球 7%～8%，用 30% 滲透率換算年限沒有意義。","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與再投資明細事實表未涵蓋，無法算增量報酬。以 FY2027 共識營收成長 6.5% 當內生成長代理上界，共識 EPS 兩年 CAGR 15.6% 超過此上界，超出部分靠利潤率與回購。","segments":[{"item":"B2C","value":"第三季營收 30.65 億美元（+6%），總預訂額 +7%，調整後 EBITDA 13.31 億美元，利潤率 43.4%，美國加速"},{"item":"B2B","value":"第三季營收 +23%，總預訂額 +19%，利潤率 27.5%（年減 134bp），所有區域雙位數成長，夥伴 7.5 萬家，CarTrawler 9 月併入"},{"item":"廣告","value":"第三季成長由 13% 放緩至 7%，公司稱產品改版中，金額事實表未涵蓋"}],"decay_signals":["未亮｜毛利率連兩季年減：年度毛利率由 FY2022 的 85.8% 升到 FY2025 的 90.12%，季度年減資料事實表未涵蓋","未亮｜核心市占縮減：第三季公司稱優於產業，同業份額事實表未涵蓋","未亮｜提價後銷量下滑：Vrbo 費用調整才開始，尚無資料","亮燈｜EPS 成長顯著高於營收成長：共識兩年 EPS CAGR 15.6%，FY2027 營收成長 6.5%，差 9 個百分點","未亮｜FCF 對淨利低於 0.75：FY2025 為 2.4 倍","未亮｜SBC 占營收超過 5%：第三季 2.43%","未亮｜TAM 被替代技術壓縮：10-K 列為風險，尚無量化證據","未亮｜產業倍數系統性下移：同業歷史倍數事實表未涵蓋","未亮｜維護性資本支出占 FCF 超過 60%：資本支出事實表未涵蓋","未亮｜停止投資且收入下滑：營收自 FY2022 起每年成長"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置屬中等：股數真的在減、帳面槓桿低，但回購買得不算便宜，併購還沒有報酬可驗。","reasoning":"FY2025 FCF 31.1 億美元、淨利 12.94 億美元，FCF 對淨利 2.4 倍，FY2024 為 1.9 倍、FY2023 為 2.3 倍，現金流明顯高於盈餘，不能全當盈餘看。第三季 FCF −13.99 億美元，TTM FCF 由 2026-08-05 CFO 說的 45 億美元降到 2026-11-04 的 37 億美元，一季少約 8 億美元，公司只講年增 25%，營運資金明細事實表未涵蓋。SBC 占第三季營收 2.43%。現金去向：今年前九個月回購約 15 億美元、併購 6.76 億美元，股息按 0.71% 殖利率換算約 2.2 億美元，資本支出事實表未涵蓋。總債務 56.89 億美元、現金 55.67 億美元，淨負債 1.22 億美元；依線上旅遊收款模式推定現金含旅客預付款，帳面淨負債可能低估真實槓桿，遞延商家預訂款事實表未涵蓋。25 億美元循環信貸簽約時未動用，Moody's Baa2 展望正向，S&P 與 Fitch 為 BBB。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"2026 年前九個月收購三家合計 6.76 億美元，約市值 2.2%，交易剛併入，管理層稱單一交易對業績不重大，已實現增量報酬尚無資料。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"第三季約 200 萬股、5.76 億美元，均價約 288 美元；第二季 88 萬股、2 億美元，均價約 227 美元。以 FY2026 共識 EPS 計，第三季買入盈餘殖利率約 7.25%，以 GAAP TTM 計約 5.9%。10 年期公債殖利率事實表未涵蓋，無法判斷是否達標。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季調整後加權股數年減 4%，SBC 占營收 2.43%，淨稀釋為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐：併購金額約市值 2.2%，管理層稱不重大，回購與併購的判斷已寫在三個計分項。"}}}},"q5_valuation":{"verdict":"12.4 倍等於假設 FY2026 之後永續成長約 2%，現價只要求 EPS 不要倒退。我相信未來三年成長高於這個數，但低於共識。","reasoning":"12.41 倍 FY2026 共識 EPS，以 10% 要求報酬、盈餘全數可分配換算，隱含永續成長約 2%；用 GAAP TTM 15.2 倍換算約 3.4%。PEG 用兩年 CAGR 15.6% 約 0.8。便宜要打折：P/S 與 EV/S 的年度端點分位是 49 和 37，營收倍數並未被壓到底，本益比低主要來自利潤率上升，利潤率一回吐就沒那麼便宜。賣方平均目標價 271～278 美元，只比現價高 4%～7%，但多數早於八月上調與第三季財報，全距資料缺，只當背景，不當依據。共識三年 EPS 兩份快照間下修 0.05%～0.36%，幅度很小。基準情境 FY2027 EPS 23.8 美元乘 12.41 倍約 295 美元，上檔 13.8%；FY2028 EPS 26.7 美元乘 13 倍約 347 美元，上檔 33.9%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_ev_m"],"verdict_values":{"valuation":{"basis":"FY2026 共識 EPS 的預估本益比，輔以 FCF 殖利率與營收倍數","tier":"成熟線上旅遊平台","peers":{"expanded":false,"reason":"同業預估本益比事實表未涵蓋，只有利潤率對照，無法做倍數比較。"},"fwd_pe":12.41,"peg":0.8,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"預估本益比 12.41 倍、PEG 約 0.8、TTM FCF 約 37 億美元對市值 307 億美元約 12%，都落在便宜區。真五年分位事實表未涵蓋，只有 4 個年度端點，不能當五年分位使用。","upside_short_pct":13.8,"upside_mid_pct":33.9,"denominator_disputed":false,"denominator_note":"FY2026 只剩一季未實現，分母未見一次性項目，不算爭點。要留意兩件事：共識推定為非 GAAP，GAAP TTM 本益比 15.2 倍；FCF 含 SBC 加回，以第三季占比粗算每年約 4.8 億美元，扣除後 FCF 殖利率約 10.5%。"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：把高點利潤率當常態，以及低估 AI 入口收過路費的速度。價值陷阱風險中等。","reasoning":"衰退十項亮一項，就是共識 EPS 成長比營收成長多 9 個百分點。壓力測試以基準 FY2031 EPS 35.4 美元、13 倍、460 美元為起點，假設稅率 21%、FY2031 股數約 9,670 萬股：營收成長每年少 2 個百分點，EPS 約 32.0，價格約 416 美元；B2C 利潤率少 500bp，EPS 約 29.9，價格約 389 美元；倍數壓到 9 倍，價格約 319 美元；三者同時，EPS 約 26.5，價格約 239 美元，低於現價 8%。四項過三項。2026-08-05 法說有五題沒有正面回答，其中 2027 年 B2C 利潤率跑道與 B2B 銷售費用兩題正好落在本論點的關鍵處。歷史最大回撤、訴訟金額事實表未涵蓋。","fact_refs":["f_kpi7_q4_2026","f_kpi3_fcf","f_ma_w52","f_ma_w104","f_ma_w250","f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率高點下的低本益比，要靠 B2C 行銷效率證明不是陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.89,"pe":12.41,"basis":"FY2026 共識 EPS，財年只剩一季，視為當年度口徑；終端倍數同樣乘當年度 EPS"},"eps":{"bull":[25.6,30.2,35.0,40.0,45.0],"base":[23.8,26.7,29.6,32.5,35.4],"bear":[21.5,20.0,19.0,19.5,20.0]},"pe":{"bull":16,"base":13,"bear":9},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.71,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-35,"basis":"歷史最大回撤事實表未涵蓋，改用三個錨：250 週均線 164 美元約 −37%；Bear 終值 180 美元約 −31%；極端 Bear 為 FY2026 EPS×0.9×0.85，乘 9 倍×0.8，約 115 美元，約 −56%。範圍取 −35% 至 −55%。","trigger_time":null},"basis":{"bull":"AI 入口成為便宜的新通路，B2B 維持高雙位數成長，B2C 預訂回到 8% 以上，利潤率每年擴張 100bp 以上，股數每年少 4%～5%。16 倍接近目前 GAAP TTM 15.2 倍再加少量溢價，同業現值倍數事實表未涵蓋。","base":"FY2027、FY2028 低於共識約 3%～4%，反映第四季減速與利潤率槓桿放緩；之後營收年增約 6%、股數每年少約 3.5%、利潤率小幅擴張。13 倍以自身 12.41 倍為錨，同業現值倍數事實表未涵蓋。EPS 已含回購效果，淨回購殖利率填 0，避免重複計入。","bear":"AI 入口與直營擠壓 B2C 利潤率 500bp 以上，FY2028 前遇一次需求下行，營收年增 2%～3%，回購減股抵銷部分衰退。機率 30% 的依據是內生成長撐不起共識，且 AI 經濟條款未定。9 倍取成長熄火的低檔：3 年後成長降到 15%／10%／5% 時，預估本益比約 14／11／9 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"AI 代理經濟條款未定，FY2025 10-K 首度點名代理式 AI，第三季法說承認流量在分散，公司也願意接受較低報酬去測試新通路。","assumption":"訂房最後仍回到可信任的品牌，新通路費率不會高於現有搜尋廣告。","consequence":"若代理掌握訂房並收費，B2C 利潤率掉 500bp 以上，EPS 停在 20 美元附近，倍數 9 倍，五年後約 180 美元，虧 31%；再遇需求下行可虧到 50% 以上。","ruling":"部分採納，以 30% 機率進 Bear。這與唯一致命點是同一件事，不重複計算。反駁在於目前沒有直接流量受損的證據，但證據時間窗蓋不到 2028 年後的風險，不能說風險已解。","watch":"B2C 利潤率年增減、直接訂房占比、代理流量首次量化揭露。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_fwd_pe_latest"]},{"view":"論點成功但股東經濟變差","evidence":"B2B 營收 +23%，利潤率卻年減 134bp 至 27.5%，低於 B2C 的 43.4%；TTM FCF 一季少約 8 億美元；Reserve Now, Pay Later 已在所有品牌上線。","assumption":"組合轉向 B2B 後整體利潤率仍能擴張，旅客預付款仍隨預訂成長。","consequence":"預訂達標，但 EPS 增速少 2～3 個百分點，FCF 對淨利倍數下降，回購能力縮小。","ruling":"採納，基準情境 FY2028 EPS 已低於共識約 4%。先訂後付對現金流的影響是推論，公司沒有揭露數字。","watch":"B2B 利潤率、TTM FCF、第四季現金流說明。","evidence_refs":["end_markets#1","channel_business_model_shift#1"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"P/S 1.89 倍、EV/S 1.9 倍在年度端點分位 49 與 37，並非低檔；2024 到 2026 年指引利潤率擴張逾 4 點，CFO 對未來只說逐步進展。","assumption":"12.4 倍是便宜，不是對高點利潤率的合理定價。","consequence":"若利潤率回吐、FY2027 EPS 只有 21.5 美元，同倍數約 267 美元，上檔幾乎沒有。","ruling":"部分反駁：扣除 SBC 後 FCF 殖利率仍約 10.5%，現價沒有要求成長溢價。但同意便宜程度被本益比誇大，所以加碼要等第四季財報與 FY2027 指引。","watch":"FY2027 利潤率指引、營收倍數。","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 259.24","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=259.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"第四季減速的性質","cause":null,"prior_field":null,"side_a":"CFO 2026-11-04：第四季放緩來自美國選舉周期、中東與歐洲地緣事件、B2B 促銷基期、秋季特賣提前。","side_b":"第四季總預訂額指引 +3.3%～+5.2%，第三季為 +11%，ADR 由第二季 +5 放緩到 +2，間夜也一起減速。","ruling":"可調和，屬程度差異。第四季指引中點 281.5 億美元和八月指引隱含的約 281.6 億美元幾乎一樣，第三季多出的約 15 億美元全留在第三季，沒有下修也沒有上修。合併下半年成長約 7.8%，這才是底層速度。一次性歸因標記為未證、監測。","evidence_level":"中：數字來自公司財報，歸因沒有量化","settle_metric":"2027 年第一、二季匯率中性總預訂額年增率","if_then":["若 2027 年第一、二季匯率中性總預訂額成長都低於 6%，則一次性歸因證偽，減碼一半","若 2027 年第一季回到 8% 以上，則解除加碼凍結，加碼至目標倉位","若股價先漲但第一季數據未到，則不追；若股價下跌但基本面未破，則分批反買"],"evidence_refs":["end_markets#2","geo_supply_chain#2","supply_demand_durability#0"]},{"axis":"AI 代理是通路還是替代","cause":null,"prior_field":null,"side_a":"CEO 2026-11-04：代理流量很小、意向高，沒有影響直接流量，入口分散對公司有利，過去都能談到不錯的通路條件。","side_b":"FY2025 10-K 首次點名代理式 AI 可能帶來新進入者與競爭加劇；CEO 同場承認經濟條款還在談，公司願意接受較低報酬去測試。","ruling":"方向相反，屬不可調和，2028 年前不可裁決。現階段採公司側作工作假設，依據是第二、三季法說都說流量很小，第三季明確說未影響直接流量；Bear 機率 30% 反映另一側。不得宣稱風險已解。","evidence_level":"低：雙方都沒有量化資料","settle_metric":"直接訂房占比、B2C 利潤率年增減、代理流量占比首次揭露","if_then":["若直接訂房占比跌破 60%，或代理流量揭露超過 10% 而 B2C 利潤率年減，則減碼至一半","若 2028 年前代理流量超過 10% 且 B2C 利潤率仍年增，則 Bear 機率下調至 20%，加碼至目標倉位"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","substitute_technology#1"]},{"axis":"對話式 AI 的轉換效果說法","cause":null,"prior_field":null,"side_a":"CEO 2026-08-05：對話式功能目前沒有帶動轉換，主要收穫是多 60% 以上的旅客意圖資訊。","side_b":"CEO 2026-11-04：同類體驗帶來更高轉換與更大訂單，活動代理使用者七日內訂購機率為兩倍。","ruling":"可調和，但要打折。一季之內說法由未帶動轉為有帶動，公司沒給轉換率數字，也承認流量小，不算進基準情境的利潤率。","evidence_level":"低：管理層口述，無數字","settle_metric":"公司揭露的轉換率或訂單金額變化","if_then":["若連兩季仍不提供轉換率數字，則繼續不計入基準情境，也不因此加碼"],"evidence_refs":[]},{"axis":"B2B 的量與質","cause":null,"prior_field":null,"side_a":"第三季 B2B 預訂 +19%、營收 +23%，所有區域雙位數成長，第二季時已連續 20 季雙位數。","side_b":"利潤率年減 134bp 至 27.5%，CFO 在 2026-08-05 與 2026-11-04 都歸因夥伴組合與投資。2026-11-04 被問成長拆分時管理層未提供，2026-08-05 被問銷售費用也沒有正面回答。","ruling":"可調和。成長是真的，利潤率壓力也不是暫時的，因為夥伴做大升級就會分走更多。基準情境假設 B2B 利潤率 26%～27%。","evidence_level":"中：分部數字可靠，拆分未揭露","settle_metric":"B2B 調整後 EBITDA 利潤率與預訂成長","if_then":["若 B2B 利潤率連兩季低於 25% 且預訂成長低於 12%，則減碼三分之一"],"evidence_refs":["end_markets#1","channel_business_model_shift#1","channel_business_model_shift#2"]},{"axis":"回購是否機會性","cause":null,"prior_field":null,"side_a":"CFO 2026-08-05 與 2026-11-04 都說回購是機會性。","side_b":"第二季均價約 227 美元只買 2 億美元，第三季均價約 288 美元買 5.76 億美元，價格高 27%，金額反而是 2.9 倍。","ruling":"採後者。回購確實減股，但時點不算機會性，現價已低於第三季均價 10%。","evidence_level":"高：公司揭露金額與股數","settle_metric":"第四季回購金額與均價","if_then":["若第四季股價低於第三季均價而回購金額縮小，則確認為順勢回購，下調 FY2028 之後的減股假設"],"evidence_refs":[]},{"axis":"現金流品質","cause":null,"prior_field":null,"side_a":"CFO 2026-11-04：TTM FCF 37 億美元，年增 25%。","side_b":"CFO 2026-08-05：同一指標為 45 億美元，一季少約 8 億美元，公司沒有說明。","ruling":"兩個數字都對，後者更重要。未獲解釋前，不把 TTM FCF 當作回購能力的穩定基礎。","evidence_level":"中：數字來自法說，原因缺","settle_metric":"FY2026 全年 FCF 與營運資金說明","if_then":["若 TTM FCF 低於 30 億美元，則減碼三分之一並下修回購假設","若全年 FCF 回到 40 億美元以上，則撤銷此項疑慮"],"evidence_refs":[]},{"axis":"利潤率還能擴張多少","cause":null,"prior_field":null,"side_a":"CFO 2026-11-04：衡量與調校能力更持久，還有機會逐步進展。","side_b":"2026-08-05 被問 2027 年 B2C 利潤率跑道時沒有回答；2026-11-04 改說行銷槓桿速度略減，共識 FY2027 EPS 仍要 +17.5%，其中約 6 點靠利潤率。","ruling":"採後者。基準情境 FY2027 EPS 23.8 美元，比共識低約 3%。","evidence_level":"中：管理層用語變化加共識拆解","settle_metric":"FY2027 全年利潤率指引","if_then":["若 FY2027 利潤率指引擴張低於 50bp，則 FY2027 EPS 下修至 23 美元以下，停止加碼"],"evidence_refs":[]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭惡化：10-K 指出對手條款更好、供應商搶直營，AI 帶來新進入者。","side_b":"結構轉好：線上占比約三分之二且仍在成長，美國飯店新增供給低，Expedia 第三季稱優於產業。","ruling":"雙向拉鋸。其他結構變數中，AI 入口與平價條款訴訟最重要，方向都還沒定。","evidence_level":"中：多為公司揭露與產業機構預測","settle_metric":"B2C 利潤率與直接訂房占比","if_then":["若 B2C 利潤率連兩季年減且直接訂房占比下降，則改判競爭惡化中，減碼一半"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#2","supply_demand_durability#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"利潤率剛到高點，下一季預訂增速減半以上，AI 條款未定，反壟斷集體訴訟剛開始，股價略低於 52 週均線。","side_b":"現價隱含永續成長約 2%，公司連六季超過財測高標，TTM FCF 殖利率約 12%。","ruling":"賣出論證成立的部分已反映在 Bear 30% 與低於共識的基準情境，不足以推翻買進，但足以限制首筆規模。","evidence_level":"中","settle_metric":"FY2027 指引與 2027 年第一季數據","if_then":["若 FY2027 指引同時低於共識營收與 50bp 利潤率擴張，則不加碼，並重算基準情境"],"evidence_refs":["regulatory_antitrust#2"]}],"triggers":[{"n":1,"text":"管理層把第四季放緩歸因於一次性因素，要用 2027 年上半年驗證。","type":"假設驗證","maps_to":"H1","metric":"匯率中性總預訂額年增率","threshold":"2027 年第一、二季都低於 6%","action":"減碼一半","source_freq":"季報新聞稿與法說，每季","date":"2027-08","evidence_refs":["end_markets#2","geo_supply_chain#2"]},{"n":2,"text":"B2C 花更多行銷費，預訂卻長得更慢。","type":"Single Thing","maps_to":"Single Thing","metric":"B2C 調整後 EBITDA 利潤率年增減與 B2C 總預訂額成長","threshold":"連兩季年減 ≥150bp，且 B2C 總預訂額成長低於 5%","action":"清倉","source_freq":"季報新聞稿，每季","date":"每季","evidence_refs":["competitive_share_entrants#0"]},{"n":3,"text":"B2B 成長放緩的同時利潤率繼續走低。","type":"風險","maps_to":"R3","metric":"B2B 調整後 EBITDA 利潤率與預訂成長","threshold":"利潤率連兩季低於 25%，且預訂成長低於 12%","action":"減碼三分之一","source_freq":"季報新聞稿，每季","date":"每季","evidence_refs":[]},{"n":4,"text":"反壟斷集體訴訟進入不利階段。","type":"風險","maps_to":"R4","metric":"Andrews 訴 Expedia 案程序進度","threshold":"集體認證通過或不利和解；刑事或政府調查介入則另列","action":"集體認證通過或不利和解時減碼一半，刑事介入時清倉","source_freq":"法院文件與 10-Q，事件驅動","date":"時程事實表未涵蓋","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2"]},{"n":5,"text":"直接訂房占比下降，代表入口開始流失。","type":"風險","maps_to":"R1","metric":"直接訂房占總訂單比","threshold":"低於 60%","action":"減碼至一半","source_freq":"法說管理層揭露，每季","date":"每季","evidence_refs":["substitute_technology#1"]},{"n":6,"text":"第四季財報與第一季數據都確認需求回升，解除加碼凍結。","type":"加碼","maps_to":"H1","metric":"FY2027 利潤率指引與第一季匯率中性預訂成長","threshold":"利潤率擴張 ≥50bp，且第一季預訂成長 ≥8%","action":"加碼至目標倉位","source_freq":"季報與法說，每季","date":"2027-05","evidence_refs":[]},{"n":7,"text":"股價下跌但基本面未破時分批買回。","type":"估值rearm","maps_to":"H2","metric":"股價與 B2C 利潤率","threshold":"股價 ≤223 美元（104 週均線），且 B2C 利潤率未年減","action":"分批反買","source_freq":"週線收盤與最新季報","date":"持續","evidence_refs":[]},{"n":8,"text":"股價先走到倍數上限時先收一部分。","type":"減碼","maps_to":"H2","metric":"股價對 FY2027 基準 EPS 的倍數","threshold":"股價 ≥381 美元（基準 EPS 的 16 倍），且 EPS 未上修","action":"減碼三分之一","source_freq":"日線收盤與共識快照","date":"持續","evidence_refs":[]},{"n":9,"text":"第四季財報後重新檢查全部假設。","type":"複審日期","maps_to":"H1","metric":"FY2027 指引、TTM FCF、B2C 與 B2B 利潤率","threshold":"財報公布後重看，不設數字門檻","action":"重看情境與倉位","source_freq":"季報與法說","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"B2C 調整後 EBITDA 利潤率年增減","bear_threshold":"連兩季年減 ≥150bp，且 B2C 總預訂額成長低於 5%","window":"連兩季","source":"季報新聞稿分部資料","last_status":"ok"},{"metric":"匯率中性總預訂額年增率","bear_threshold":"2027 年第一、二季都低於 6%","window":"2027 年上半年","source":"季報新聞稿與法說","last_status":"warning"},{"metric":"直接訂房占總訂單比","bear_threshold":"低於 60%（目前約三分之二）","window":"每季法說","source":"法說管理層揭露","last_status":"ok"},{"metric":"B2B 調整後 EBITDA 利潤率","bear_threshold":"連兩季低於 25%，且 B2B 總預訂額成長低於 12%","window":"連兩季","source":"季報新聞稿分部資料","last_status":"warning"},{"metric":"TTM 自由現金流","bear_threshold":"低於 30 億美元","window":"最近四季","source":"季報現金流量表","last_status":"ok"}],"action_conditions":{"rearm_trigger":"FY2027 指引利潤率擴張至少 50bp 且第一季匯率中性預訂成長達 8%，或股價回到 223 美元而基本面未破。","exec_line":"首筆不超過目標倉位一半，理由是 2026 年 10 月的反壟斷新案與第四季減速都未滿一季，尚未被確認。第二筆等 2027 年 2 月第四季財報與 FY2027 指引，第三筆綁第一季數據。股價先漲而數據未到不追；下跌但 B2C 利潤率未破則分批反買。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 AI 入口的未來風險提前打進今天的倍數：12.41 倍只隱含約 2% 永續成長，但三分之二訂單仍來自直接入口，兩次法說都說代理流量很小。第四季指引也沒有低於八月隱含值，市場把既有的放緩讀成新壞消息。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"第四季放緩主要是一次性與基期因素，2027 年總預訂額回到中高個位數成長。","2y":"FY2027 匯率中性總預訂額成長至少 6%，營收接近共識 174.5 億美元。","5y":null,"10y":null,"threshold":"FY2027 匯率中性總預訂額成長 ≥6%","source":"季報新聞稿與法說的總預訂額及匯率影響","drift_rule":"兩年期口徑：TTM 較門檻偏離連兩季達 5% 為削弱，連三季達 10% 為反轉"},{"id":"H2","text":"B2C 行銷效率與固定成本紀律是結構性改善，利潤率還能逐步擴張。","2y":null,"5y":"到 FY2031，調整後 EBITDA 利潤率較 FY2026 再高 200～300bp，第三季 B2C 利潤率不低於 43%。","10y":null,"threshold":"FY2027 調整後 EBITDA 利潤率擴張 ≥50bp；第三季 B2C 利潤率 ≥43%","source":"季報新聞稿分部資料與全年指引","drift_rule":"五年期口徑：TTM 較門檻偏離連四季達 5% 為削弱，連六季達 10% 為反轉"},{"id":"H3","text":"B2B 是第二成長來源，規模放大後利潤率守得住。","2y":null,"5y":"B2B 總預訂額五年 CAGR 至少 12%，調整後 EBITDA 利潤率維持 26% 以上，營收占比由約 35% 升到 40% 以上。","10y":null,"threshold":"B2B 預訂成長 ≥12%，利潤率 ≥26%","source":"季報新聞稿分部資料與法說夥伴數","drift_rule":"五年期口徑：TTM 較門檻偏離連四季達 5% 為削弱，連六季達 10% 為反轉"}],"R":[{"id":"R1","text":"AI 代理與 Google 等上層入口收過路費，B2C 利潤率反轉。","h_ref":"H2","clock":"🔥","threshold":"B2C 利潤率連兩季年減 ≥150bp，且 B2C 預訂成長低於 5%；或直接訂房占比低於 60%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"id":"R2","text":"第四季減速延伸成趨勢，地緣事件與美國內需偏弱持續壓抑旅遊。","h_ref":"H1","clock":"⚡","threshold":"2027 年第一、二季匯率中性預訂成長都低於 6%","evidence_refs":["end_markets#2","geo_supply_chain#2"]},{"id":"R3","text":"B2B 夥伴升級與投資持續壓低利潤率，成長品質下降。","h_ref":"H3","clock":"🔥","threshold":"B2B 利潤率連兩季低於 25%，且預訂成長低於 12%","evidence_refs":["end_markets#1","channel_business_model_shift#1"]},{"id":"R4","text":"Andrews 訴 Expedia 全美反壟斷集體訴訟（2026 年 10 月，華盛頓西區聯邦法院，民事）指控平價條款與排名懲罰抬高房價，公司稱無理由。受影響營收與求償金額事實表未涵蓋。另有 Helms-Burton 四件、以色列集體認證待決與各地住宿稅訴訟。","h_ref":"H2","clock":"🐢","threshold":"集體認證通過、不利和解，或政府調查介入","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"id":"R5","text":"平台關鍵功能遷移到 AWS 後形成單點依賴，2025 年 10 月的中斷事件已波及公司。","h_ref":"H1","clock":"🐢","threshold":"管理層將單次中斷列為當季預訂成長減少至少 1 個百分點的原因","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"現金流高於盈餘的部分可能縮小，回購能力下降。","h_ref":"H2","clock":"🔥","threshold":"TTM FCF 低於 30 億美元","evidence_refs":[]}],"single_thing":{"description":"B2C 行銷效率反轉：B2C 調整後 EBITDA 利潤率連兩季年減至少 150bp，同時 B2C 總預訂額成長低於 5%。","why_fatal":"共識 EPS 兩年成長中約 5 個百分點靠利潤率，B2C 又是第三季 EBITDA 的主要來源。B2C 利潤率每少 100bp，FY2031 EPS 約少 1.1 美元；少 500bp 約少 5.5 美元，再加倍數由 13 倍降到 9 倍，目標價由 460 美元掉到約 269 美元，是模型裡最大的單一敏感項。","if_happens":"代表花錢買不到成長，入口議價權已轉移。清倉，等新的全年指引與通路條款明朗後重做研究。","how_monitor":"每季財報新聞稿的 B2C 營收、調整後 EBITDA 與總預訂額；第三季基準為利潤率 43.4%、預訂 +7%。","probability":"12～24 個月內約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":10.56,"peg_fy2":0.68,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":9.81,"FY2026E":20.89,"FY2027E":24.55,"FY2028E":27.92},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識，對照 GAAP TTM 約 17 美元推定為非 GAAP 口徑。FY2025A 的 9.81 美元是 GAAP 稀釋 EPS，非 GAAP 基期事實表未涵蓋，兩者不可直接算成長率；成長率改用 FY2026E 至 FY2028E 兩年 CAGR 15.6%。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY2027 指引","impact":"高","watch":"總預訂額指引、利潤率擴張幅度、TTM FCF 說明"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 年第一季財報","impact":"高","watch":"匯率中性預訂成長是否回到 8%，B2C 與 B2B 利潤率"},{"date":null,"date_precision":null,"type":"regulatory","event":"Andrews 反壟斷集體訴訟的駁回聲請或集體認證裁定","impact":"中","watch":"程序進度與求償金額，時程事實表未涵蓋"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 AI 入口的未來風險提前打進今天的倍數：12.41 倍只隱含約 2% 永續成長，但三分之二訂單仍來自直接入口，兩次法說都說代理流量很小。第四季指引也沒有低於八月隱含值，市場把既有的放緩讀成新壞消息。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=13.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
