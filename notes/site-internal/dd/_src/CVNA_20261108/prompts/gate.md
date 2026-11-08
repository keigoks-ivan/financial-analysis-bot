你是 DD 管線 v20 的判斷層閘（gate），標的 CVNA（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝8040 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi1`（q1_business）｜零售銷量＝217385 輛｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi2_ebitda_non_gaap`（q1_business）｜調整後 EBITDA（公司不報 non-GAAP 營業利益，以此代之）＝800 百萬美元（利益率 10.0%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝714 百萬美元（利益率 8.9%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi4_gaap`（q1_business）｜GAAP 淨利＝483 百萬美元（淨利率 6.0%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：EPS 約 $0.39 對共識約 $0.47–0.48（Zacks 等第三方，低於預期）
- `f_kpi6`（q1_business）｜管理層指引＝Q4 零售銷量較 Q3 季增；2026 全年調整後 EBITDA 落在先前區間 27–30 億美元的偏高端（假設環境穩定） 文字｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：無數值型 Q4 指引
- `f_peer_cvna_gross_margin_pct`（q2_moat）｜CVNA 毛利率＝19.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CVNA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cvna_operating_margin_pct`（q2_moat）｜CVNA 營業利益率＝8.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CVNA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cvna_fcf_margin_pct`（q2_moat）｜CVNA FCF 利潤率＝4.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CVNA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_kmx_operating_margin_pct`（q2_moat）｜KMX 營業利益率＝-1.4 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KMX.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_an_operating_margin_pct`（q2_moat）｜AN 營業利益率＝4.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lad_operating_margin_pct`（q2_moat）｜LAD 營業利益率＝3.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LAD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.52 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.12 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝2.73 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝29731.63 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝37481.56 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝3.5 %（SBC 25 百萬；占營收 0.3%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Business Wire 2026-10-28，經 finviz.com/news/410551 轉載；IR 站 press.carvana.com 403 未能直接取得）；比例為自算 25/714（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝2091.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 5697.0、現金 3606.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝73.57 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝48.4 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.52，分子＝快照價 73.57｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝35.37 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝90.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝87.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.52 → 1.52）｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝62.82｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-5.61 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w250`（q5_valuation）｜250 週均線＝33.9 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝63.94 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 73.57 / W52 71.08 / W104 63.94 / W250 33.9 / W250 13週斜率 1.4%」

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出的競爭者包括 CarMax、Amazon、Costco Auto Program、車廠（Ford、GM、Toyota、Tesla、Rivian、Lucid 等），並預期新舊競爭者持續進入。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Amazon Autos 擴及二手與認證二手車，被視為對 Carvana 的潛在新進入者威脅，但目前僅限單一城市、單一車廠，短期影響有限（2025-08 分析）。
  - 來源：247WallSt: Carvana Surged 8,200% in 2+ Years. Is Amazon About to Wreck Its Rally?（as_of 2025-08-06）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：批發二手車價創近三年高點，供給偏緊、新車均價逾 $49,000 推動需求轉向二手
  - 來源：ConsumerAffairs: Used-car prices climb as tight supply makes it tougher for buyers（as_of 2026-04-09）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 法律程序章節：2025年6月收到SEC傳票，主要涉及做空機構報告的指控，公司表示全面配合；未提及反壟斷調查或拆分。
  - 來源：SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 風險因子將美國聯邦政府關稅或貿易限制的實施／暫停列為可能影響業務的汽車生態系因素。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：公司自述日益依賴第三方生成式 AI 平台與內部軟體，AI 表現不如預期可能造成轉換率下降、營運中斷與品牌受損（屬自身技術風險，非外部替代品）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：經銷商產業人士預測 agent-to-agent 購車 2029 年成為常態（預測，非事實）。
  - 來源：Car Dealership Guy newsletter（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Hertz 宣布推出直接向消費者線上銷售二手車平台，與 Carvana、CarMax 競爭。
  - 來源：Bloomberg Government（as_of 2025-09-30）｜affects：moat_trend
- `major_events#0`（major_events｜方向 -｜狀態 ok）：SEC 於 2025-06 對 Carvana 發出傳票（主要涉及空頭報告指控）；FY2025 10-K 稱公司全力配合。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2022 年證券集體訴訟 In re Carvana Co. Securities Litigation 仍列於 FY2025 10-K 法律事項（非近12月新案）。
  - 來源：SEC EDGAR 10-K FY2025 Note 16（as_of 2026-02-18）｜affects：thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2026-01-28 Gotham City Research 發空頭報告後股價單日跌約14.2%，多家原告律所宣布調查；搜尋未見 2026 新集體訴訟起訴。
  - 來源：Pomerantz 投資人通知（placera.se 轉載）（as_of 2026-01-30）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2022 年證券集體訴訟仍列於 10-K；2026-01 Gotham 空頭報告後多家律所宣布調查，未見新案起訴。
  - 來源：SEC EDGAR 10-K FY2025 Note 16（as_of 2026-02-18）｜affects：thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":198.4,"bear_5y_price":28.8,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":41.4,"ev5y_pct":36.4,"irr_base_pct":7.2,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.52,"pe":48.4,"basis":"FY2026E 共識 EPS，當年度口徑；終端倍數同樣用終端年當年度 EPS"},"eps":{"bull":[2.3,3.2,4.15,5.2,6.2],"base":[2.05,2.6,3.05,3.55,4.0],"bear":[1.75,1.55,1.35,1.45,1.6]},"pe":{"bull":32,"base":26,"bear":18},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CVNA_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 給 2026 全年調整後 EBITDA 區間（附帶「環境維持穩定」前提）（原話："adjusted EBITDA of $2.7 billion to $3.0 billion"）
- 2026-07-29｜CFO｜guidance：CFO 預期 Q3 零售銷量較 Q2 季增（原話："a sequential increase in retail units sold in Q3"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q3 營收成長將與零售銷量成長較一致（總額法認列的同比影響自 Q3 消失）（原話："revenue growth to be more in line with retail unit growth"）
- 2026-07-29｜CFO｜guidance：CFO 預期 Q3 廣告費用金額增加（原話："We expect an increase in advertising expense dollars in Q3."）
- 2026-07-29｜CFO｜guidance：CFO 解釋今年 EBITDA 區間的給法與前兩年相同，下半年才給具體 EBITDA 護欄（原話："same style of guidance that we've applied the last 3 years"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EBITDA 利潤率 10.4%，年減（CFO 歸因於總額法認列使每台零售營收上升）（原話："Adjusted EBITDA margin was 10.4%, a decrease from 12.4%"）
- 2026-07-29｜CFO｜margin：營收成長高於銷量成長的原因之一：向大型零售市集夥伴取得之部分車輛改採總額認列（原話："traditional gross revenue treatment for certain vehicles"）
- 2026-07-29｜CFO｜margin：非 GAAP 零售 GPU 年減 $105，主因是對比去年約 $100 關稅相關利益（原話："Non-GAAP retail GPU decreased by $105"）
- 2026-07-29｜CFO｜margin：非 GAAP 批發 GPU 年減 $158，CFO 歸因於零售銷量成長快於批發毛利（原話："Non-GAAP wholesale GPU decreased by $158"）
- 2026-07-29｜CFO｜margin：非 GAAP 其他 GPU 年減 $192，CFO 提到讓利給客戶降低利率與基準利率上升（原話："Non-GAAP other GPU decreased by $192"）
- 2026-07-29｜CEO｜margin：CEO 拆解其他 GPU：讓利約 100bp 利率，單純算應降約 $500，實際只降約 $200，差額為基本面增益（原話："give or take, $300 of fundamental gains in there"）
- 2026-07-29｜CFO｜margin：CFO 說 Q2 非 GAAP SG&A 每台零售單位下降 $157（管理費用 −$272、營運費用 +$88）（原話："$157 reduction in non-GAAP SG&A expense per retail unit"）
- 2026-07-29｜CEO｜margin：CEO 拆解每台 EBITDA 年減約 $300 的原因之一：油價上升的成本估計（原話："That probably cost us something on the order of $75"）
- 2026-07-29｜CEO｜margin：CEO 指出去年同期有約 $100 的關稅利益（影響每台 EBITDA 年比）（原話："Last year, we had a tariff benefit that was around $100."）
- 2026-07-29｜CFO｜margin：CFO 稱仍看到顯著的 SG&A 規模槓桿空間（原話："opportunities for significant SG&A expense leverage"）
- 2026-07-29｜CEO｜margin：CEO 說明 FTC 要求經銷商報價含文件費等後，Carvana 定價演算法跟隨市場，造成零售 GPU 出現超額收益（原話："the FTC put out guidance to all dealers"）
- 2026-07-29｜CEO｜commitment：CEO 說基本面增益將隨時間回饋給客戶，作為邁向 3 百萬台／13.5% 的路徑（原話："we've elected to pass those back over time"）
- 2026-07-29｜CEO｜commitment：CEO 重申中期目標：2030–2035 年每年賣 300 萬台、調整後 EBITDA 利潤率 13.5%（原話："3 million cars per year at 13.5% adjusted EBITDA margin"）
- 2026-07-29｜CEO｜commitment：CEO 表示管理層有信心庫存成長會追上銷售並可能超越（原話："we're confident they'll catch up and hopefully surpass it"）
- 2026-07-29｜CEO｜commitment：CEO 說新零件工具（Roll Call、Leader Hub）尚未全面上線，將在未來數季推出（原話："we'll be rolling it out over the coming quarters"）
- 2026-07-29｜CEO｜risk：CEO 承認庫存成長落後銷售，是對業務的逆風（原話："inventory has undergrown sales over the last several months"）
- 2026-07-29｜CEO｜risk：CEO 說庫存偏低影響轉換率，近期用行銷費用填補（原話："Inventory is a little lighter relative to where we wish"）
- 2026-07-29｜CEO｜risk：CEO 承認對客戶讓利利率在庫存吃緊下，可能未在成長上獲得完整回報（原話："we probably didn't get fully paid for it"）
- 2026-07-29｜CFO｜risk：CFO 的展望以環境穩定為前提（原話："as long as the environment remains stable"）
- 2026-07-29｜CEO｜product：CEO 說明庫存計畫三步驟的第三步：回到較傳統的車齡／里程組合（原話："we plan now to shift to cars that are closer to our"）
- 2026-07-29｜CEO｜product：CEO 說明偏向較新較貴車款的庫存組合轉變並非結構性（原話："So I would say definitely not structural."）
- 2026-07-29｜CEO｜product：CEO 以客服成本逐年下降說明 AI／網站自助的效果，今年再降 10%（原話："This year, we went down an additional 10% year-over-year."）
- 2026-07-29｜CEO｜product：CEO 談新車（新經銷據點）業務：目前有獲利，但不願多提細節（原話："New cars are profitable for us today."）
- 2026-07-29｜CEO｜customer：CEO 說年收入逾 10 萬美元客群銷售年增逾 60%（原話："customers with over $100,000 of income"）
- 2026-07-29｜CEO｜customer：CEO 解釋區域數據：庫存增 57% 的兩區銷售成長 54%（庫存與銷售相關）（原話："In those markets, sales grew in the second quarter by 54%."）
- 2026-07-29｜CFO｜customer：CFO 提供 Q2 零售銷量與年增率（原話："Retail units sold totaled 197,325 in Q2, an increase of 38%"）
- 2026-07-29｜CFO｜competition：CFO 對比產業背景：產業年減約 4 個百分點，Carvana 零售銷量成長 38%（原話："the industry is down, call it, on the order of 4 points"）
- 2026-07-29｜CEO｜competition：CEO 談護城河：規模建立後，其他人不願跨越（原話："a big moat behind us that nobody else wants to run across"）
- 2026-07-29｜CFO｜capital_allocation：CFO 稱淨負債對近 12 個月調整後 EBITDA 降至 1.0x（原話："net debt to trailing 12-month adjusted EBITDA ratio to 1.0x"）
- 2026-07-29｜CFO｜capital_allocation：CFO 答資本回報提問：現金首要用途是投資業務、取得回報，未談股東回報（原話："investing in the business and generating returns"）
- 2026-07-29｜CFO｜capital_allocation：CFO 提供營運資產報酬率：近 12 個月營業利益約 $2.2B，淨營運資產約 $7.5B（原話："on the order of 30% operating return on net operating assets"）

### 問答異常語氣（迴避／改口／保留）
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Rajat Gupta（JPMorgan）：下半年 EBITDA 指引暗示較上半年下滑，為何如此保守、是否遺漏什麼｜答法：CEO 說「stick with guidance」，不解釋上下半年動態，改談執行力與機器模型
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Joseph Spak（UBS）：下半年獲利與上半年接近，是基期還是成本因素｜答法：CEO 同樣回「stick with our guidance」，未回答基期或成本拆分，轉向執行
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Sharon Zackfia（William Blair）：Q3 GPU 逐季降幅是否收斂｜答法：CEO 拒絕逐項 GPU 說明，僅稱季節性可能與過去相似
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Jeff Lick（Stephens）：上季提到的 GPU $200–300 逆風是否未如預期發生｜答法：CEO 不確認或否認該 $200–300，重申整體指引，改談庫存不足造成轉換率下降
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：John Babcock（Barclays）：7 月至今 GPU 與成本（油價、整備）概況｜答法：CFO 只指向全年展望，不提供 6 月到 7 月的細節
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Joseph Spak（UBS）：新車經銷據點是否已開始幫助二手車庫存｜答法：CEO 說「早期」、不給可評論的內容，只提及 NPS 高
- CVNA_Q2_2026_Earnings_Call_20260729.md｜問：Rajat Gupta（JPMorgan）：每台 EBITDA 連續三季下滑，何時回到成長（年底或 2027）｜答法：CEO 未給時間點，拆解年比因素（關稅、油價、基準利率）後轉談庫存成長與執行

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 2 | 2 |
| major_events | found | 5 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CVNA","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Carvana Co."},"oneliner":"Carvana 在持平的二手車市場繳出 39% 的台數成長，營益率約為傳統車商兩倍。但現價是 FY2026E 的 48.4 倍，基本情境五年年化只有約 7%，其他收入又相當於 EBITDA 的 74%，等 59 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/scenario.json","answers":{"q1_business":{"verdict":"Carvana 賺買車人的車差和貸款的錢，錢卡在貸款能不能順利賣出去。","reasoning":"Q3 營收 80.4 億美元，零售占 76.4%，批發 16.2%，其他 7.4%。TTM 毛利率 19.04%，GAAP 營益率 8.74%，Q3 單季營益率 8.9%。其他收入只占營收 7.4%，但 5.94 億美元相當於調整後 EBITDA 的 74%，每台 2,733 美元，是全公司最依賴外部資金市場的一段；其他毛利事實表未單列，此數為上限。每台總毛利 7,093 美元，年減 410 美元，每台費用持平，所以每台調整後 EBITDA 約 3,680 美元，年減約 400 美元，CEO 歸因約 200 美元來自油價與利率。單點依賴在貸款買方與 ABS 市場，買方名單與集中度事實表未涵蓋。可能看錯的地方：若其他收入有相當部分來自保固與服務合約，對資金市場的敏感度會低於這裡的估計。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_ebitda_non_gaap","f_kpi3_gaap","f_kpi4_gaap","f_kpi6","f_peer_cvna_gross_margin_pct","f_peer_cvna_operating_margin_pct"],"verdict_values":{"revenue_quality":"零售 6,144 百萬美元，年增 54%；批發 1,302 百萬美元，年增 11%；其他 594 百萬美元，年增 25%。分部數字來自聚合站摘要，三項加總等於 8,040 百萬美元。","unit_econ_note":"Q3 零售 GPU 3,625 美元，年增 85 美元；批發年減 196 美元；其他年減 299 美元。每台 GAAP 營業利益 3,284 美元，年減約 250 美元。去年同期台數由 39% 年增率反推。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"已獲利、高成長、低滲透率的線上零售，獲利對利率與消費信貸敏感"},"industry":{"clock_phase":"IV","sd_verdict_source":"需求結構性持久，量的壓力屬週期性。Cox 預估 2026 年零售二手車 −0.7%，CFO 稱 Q2 產業年減約 4 點，批發價卻在近三年高點，屬供給偏緊造成的量縮，不是需求崩塌。2027 年租賃退場車回升（次級來源轉述 Manheim）會緩解供給。","bargaining":{"up":"車源來自消費者、拍賣與市集夥伴，分散；各來源占比事實表未涵蓋。","down":"購車人極度分散，真正有議價權的下游是貸款買方與 ABS 投資人。","geo":"主要在美國單一市場。"},"profit_pool_dir":"CEO 稱車商淨利率 25 至 30 年大致持平。利潤往規模化線上業者移動的證據是 CVNA 營益率約為 AN、LAD 的兩倍以上，五年利潤池占比事實表未涵蓋。","tam_table":[{"item":"全美二手車總量（Cox 2026）","value":"3,830 萬台"},{"item":"全美零售二手車（Cox 2026）","value":"2,030 萬至 2,040 萬台"},{"item":"CVNA 年化台數（Q3）","value":"87 萬台"},{"item":"滲透率","value":"占總量 2.3%，占零售二手 4.3%。管理層說的兩個百分點出頭，分母是總量"},{"item":"300 萬台目標占比","value":"占總量 7.8%，占零售二手 14.8%"},{"item":"營業利益池五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河在變寬，來自規模帶動的選車、到貨速度與資金成本，定價面大致穩定。","reasoning":"機制是整備、物流與單一庫存池的垂直整合：規模越大，選車越多、到貨越快、資金成本越低。可驗證的方向是份額，從 10-K 的 1.6% 升到 Q3 的兩個百分點出頭，產業同期持平；營益率高於 KMX、AN、LAD。稅後 ROIC 約 23%：2026-07-29 CFO 給的 TTM 營業利益約 22 億美元、淨營運資產約 75 億美元，稅前約 29%，再以 21% 假設稅率換算，隱含周轉約 3.4 倍。這是低利益率、高周轉的零售模式。FY2025 實現的增量報酬約 118%，主因是填滿既有產能，不能外推，前瞻取 50%。反例是 Q3 每台費用沒有槓桿，新場站初期成本也較高，增量報酬可能比 50% 更低。同業 ROIC 事實表未涵蓋。","fact_refs":["f_peer_cvna_gross_margin_pct","f_peer_cvna_operating_margin_pct","f_peer_cvna_fcf_margin_pct","f_peer_kmx_operating_margin_pct","f_peer_an_operating_margin_pct","f_peer_lad_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"垂直整合的整備與物流網路加上單一庫存池，規模帶來更多選車、更快到貨與更低資金成本。","execution":9,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：連續 11 季台數成長與 EBITDA 利潤率業界第一，NPS 兩年升 9 點，到貨快 2 天。定價面穩定：每台總毛利年減 410 美元，主因是讓利給客戶與利率上升，零售 GPU 反而年增 85 美元。可能看錯的地方：讓利結束後每台獲利若仍不回升，定價面要改判縮減。","competitor_notes":[{"name":"KMX","strategy_note":"規模最接近的二手車對手，線上化追趕尚未轉成獲利，CEO 表示看不出對 CVNA 有明顯影響。"},{"name":"AN","strategy_note":"特許經銷模式毛利率接近 CVNA，但費用結構重，營益率約只有一半。"},{"name":"LAD","strategy_note":"靠併購擴張，自由現金流為負，資本路徑與 CVNA 相反。"},{"name":"ACVA","strategy_note":"批發拍賣平台，只在批發端部分重疊，對零售端不構成直接威脅。"},{"name":"Amazon Autos","strategy_note":"10-K 點名的潛在進入者，現有證據是 2025 年 8 月的單一城市與單一車廠，規模資料過舊。"},{"name":"Hertz","strategy_note":"線上通路主要消化自有車隊，車源與品項受限。"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，以份額與營益率差替代。","threats":[{"level":"🟡","text":"新進者持續進場：Amazon、Costco、車廠直售列在 10-K，Hertz 2025 年推線上二手車，目前都還沒有規模證據。","p":"30%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#3"]},{"level":"🟡","text":"AI 代理比價對零售端透明度有利，但會提高貸款提前清償與利率比價。CEO 在 2026-10-28 也承認提前清償可能上升；產業人士預測 2029 年常態化，屬預測。","p":"30%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"公司依賴第三方生成式 AI 平台，表現不如預期時會影響轉換率與客服，屬營運風險，不是替代威脅。","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者與付款者多為同一人，買車需求可延後但不會消失。美國零售二手車約 2,030 萬台，新車均價逾 49,000 美元，推動需求轉向二手。"},{"item":"決策層級","level":"🟡","text":"每次購車都是單筆決策，沒有轉換成本，也沒有回購率資料。替代性靠當地選車量與到貨速度維持，CEO 稱多數大都會庫存已超過當地車商總和，此為公司說法。"},{"item":"價值鏈分配","level":"🟡","text":"其他收入相當於 EBITDA 的 74%，獲利有很大一段要經過貸款買方與 ABS 投資人。公司又主動把利率讓給客戶，這段價值的分配權不完全在公司手上。"},{"item":"社會容忍度","level":"🟡","text":"車貸受 CFPB、FTC 與各州監管，獲利若過度依賴貸款會招致政策與輿論壓力。FTC 費用揭露方向目前對公司有利，SEC 調查已結案且不建議執法。"}],"roiic":50,"reinvest_rate":40,"endo_ceiling":20,"formula_note":"再投資率以 FY2025（稅後營業利益−FCF）÷稅後營業利益代理：營業利益 1,882 百萬美元×0.79＝1,487 百萬美元，減 FCF 889 百萬美元，得 40%；未加回利息，會高估再投資。實現增量報酬＝兩年稅後營業利益差 705 百萬美元÷598 百萬美元＝118%，受既有產能填滿推高。平均資本報酬約 23%。前瞻 50% 為判斷值。內生上界＝50%×40%＝20%，單位為百分比。稅率 21% 為假設；折舊、營運資金與收購淨額事實表未涵蓋，所以無法用標準公式。"}}}},"q3_growth":{"verdict":"成長跑道寬，五年後仍有空間，滲透率遠低於 35%。","reasoning":"成長以量為主：Q3 零售營收年增 54%，台數 39%，其餘約一成是高價車組合，量約占 76%。共識 EPS 從 FY2025A 1.69 到 FY2028E 2.73，年化 17.3%；但 FY2026E 1.52 低於 FY2025A，營收卻增 46%，基期含不會重複的成分，細項事實表未涵蓋。改用 FY2026E 為基期，兩年年化 34.0%，高於內生上界 20%，缺口 14 個百分點歸因於營益率擴張，主要是費用槓桿，不是回購或併購。Koyfin 的 EPS 家數未載明。按 39% 成長率，5.9 年即達零售二手市場的 30%，這不現實；用平均 20% 成長則為 10.7 年。反例：CEO 說成長受限於供應鏈，產能一旦跟不上，跑道再長也兌現不了。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi1"],"verdict_values":{"growth":{"driver_mix":"量約 76%，價格與組合約 24%，併購與回購幾乎沒有貢獻。","runway_years":"5.9（維持 39% 成長）至 10.7（平均 20% 成長）","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段推導：前瞻增量報酬 50%×再投資率 40%＝20%。","segments":[{"item":"零售","value":"Q3 占營收 76.4%，年增 54%"},{"item":"批發","value":"Q3 占營收 16.2%，年增 11%"},{"item":"其他","value":"Q3 占營收 7.4%，年增 25%，相當於調整後 EBITDA 的 74%"},{"item":"新車","value":"收購 Stellantis 經銷店，CEO 稱目前獲利，占比事實表未涵蓋"}],"decay_signals":["毛利率連兩季年減：亮燈。Q2 每台毛利年減 455 美元，Q3 年減 410 美元，TTM 毛利率 19.04% 低於 FY2025 的 20.63%。","EPS 成長高於營收成長超過 5 個百分點：亮燈。FY2026E 到 FY2027E 的 EPS 增 39%，營收增 26%。","FCF／淨利連兩年低於 0.75：未亮，但接近。FY2025 為 63%，FY2024 為 394%，FY2026 尚未結束。","核心市占縮減、提價後銷量下滑、SBC 偏高、停止投資新產能：未亮。","TAM 萎縮或被替代：未亮。Cox 預估 2026 年零售二手車 −0.7%，屬持平。","產業倍數下移、維護性資本支出占比：事實表未涵蓋。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金優先投回業務和降債，沒有回購，股本稀釋很低。","reasoning":"FY2025 FCF 為淨利的 63%，TTM FCF 利潤率 4.05%。SBC 每季 2,500 萬美元，占營收 0.3%。Q3 淨負債對 TTM 調整後 EBITDA 0.8 倍，利息保障 6.9 倍，都是公司紀錄。2026 年 8 月以 16.6 億美元定期貸款再融資，每年省息約 4,500 萬美元，Q3 認列一次性費用 5,300 萬美元。CFO 在 2026-07-29 表示現金首要用途是投資業務。營運槓桿在 Q3 轉弱：營收年增 42%，GAAP 營業利益年增 29%，差 13 個百分點。近三年現金去向四分、債務到期結構與逐年股數事實表未涵蓋。","fact_refs":["f_kpi5_sbc_gaap","f_net_debt_m","f_peer_cvna_fcf_margin_pct","f_kpi3_gaap","f_kpi0_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月只有七家 Stellantis 經銷店的小型收購，金額事實表未涵蓋，無法計算已實現報酬。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"公司沒有回購，CFO 表示現金優先投資業務。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 1 億美元，除以市值 1,097.6 億美元，約 0.09%，低於 1.5%。逐年股數事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能與份額，不靠併購或回購，且近三年現金去向細項事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2031 EPS 接近 5 美元才有 12% 年報酬，我只信到 4 美元，所以偏貴。","reasoning":"現價 73.57 美元，Forward P/E 48.4 倍。要賺 12% 年報酬，五年後股價要 130 美元，以 26 倍計 FY2031 EPS 要約 5.0 美元，等於約 220 萬台、12% 營益率。我的基本情境是 185 萬台、11.5%、EPS 4.00 美元，終點 104 美元，年化約 7%。短期目標：FY2027E 2.05 美元×38 倍＝77.9 美元；中期：FY2028E 2.60 美元×33 倍＝85.8 美元，兩個倍數都是判斷值。賣方目標均值 84.14 美元，區間 48 至 120 美元，是 2026-08-05 的舊資料，早於 Q3，不支持追價。Q3 EPS 約 0.39 美元，低於共識 0.47 至 0.48 美元，但兩份快照的 FY1 共識都是 1.52 美元，可能尚未更新。RSI 62.82 未過熱，4 週漂移事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_fy1_pct","f_rsi14","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E，分母為 FY2026E 共識 EPS 1.52 美元","tier":"高成長線上零售，事實表沒有同層同業倍數","peers":{"expanded":false,"reason":"事實表的同業表只有毛利率、營益率與 FCF 利潤率，沒有同業倍數，無法做跨公司估值對照，這是資料缺口。"},"fwd_pe":48.4,"peg":1.42,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴。Forward P/E 48.4 倍÷FY2026E 到 FY2028E 年化 34.0%，PEG 1.42；改用基本情境五年年化約 21%，PEG 約 2.3，低 PEG 來自近兩年的成長高峰。五年分位事實表未涵蓋，只有年度端點分位：P/S 90.4、EV/S 87.4。基本情境五年年化約 7%，上下行比約 1.9。","upside_short_pct":5.9,"upside_mid_pct":16.6,"denominator_disputed":true,"denominator_note":"Trailing P/E 35.37 倍低於 Forward 48.4 倍，反推 trailing EPS 約 2.08 美元，高於 FY2025A 的 1.69 美元與 FY2026E 的 1.52 美元，而營收預期成長 46%。分母含不會重複或口徑不同的項目，細項事實表未涵蓋，P/E 端點分位 0 不能當便宜的證據。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是融資收益的韌性，其次是現價已先付了未來幾年的成長。","reasoning":"悲觀路徑是利率與信用同時轉差，其他收入下滑，台數停在 130 萬台左右。FY2022 的 FCF −18.36 億美元、營益率 −11.06% 是這家公司真實發生過的下行。我也可能看錯在另一邊：若每台獲利在 2027 年回升，同時台數維持 30% 以上成長，等 59 美元可能永遠等不到。未涵蓋且會影響判斷的資料有：貸款買方集中度、其他收入細項、歷史最大回撤、Gotham 報告的指控內容、集體訴訟金額、同業倍數。2026-07-29 的法說會上，管理層多次避開下半年獲利與每台獲利回升時點的提問。","fact_refs":["f_price_at_dd","f_ma_w250","f_ma_w104","f_ma_state","f_kpi2_ebitda_non_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"貴的好公司：兩項衰退信號亮燈，還不是價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.52,"pe":48.4,"basis":"FY2026E 共識 EPS，當年度口徑；終端倍數同樣用終端年當年度 EPS"},"eps":{"bull":[2.3,3.2,4.15,5.2,6.2],"base":[2.05,2.6,3.05,3.55,4.0],"bear":[1.75,1.55,1.35,1.45,1.6]},"pe":{"bull":32,"base":26,"bear":18},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-70,"hi":-45,"basis":"事實表未涵蓋股價歷史最大回撤，改用三個價位推：回到 250 週均線 33.90 美元為 −54%，悲觀情境終點 28.80 美元為 −61%，融資事件的過度下跌再加約 9 個百分點，取 −70%；較淺端 −45% 對應股價約 40 美元，約為悲觀 FY2027E EPS 1.75 美元的 23 倍。","trigger_time":null},"basis":{"bull":"2031 年賣約 260 萬台，年化約 27%，每台收入 3.75 萬美元，GAAP 營益率 12.5%，稅率 22%，稀釋股數 15.2 億股；終端 32 倍對應其後仍有約 15% 成長。","base":"2031 年賣約 185 萬台，年化約 18%，GAAP 營益率 11.5%，低於管理層 12.5% 目標，稅率 22%。FY2027E 2.05 美元略低於共識 2.12 美元，等於 Q3 加回一次性費用後的年化約 1.70 美元，再加約兩成台數成長，每台獲利大致不變。終端 26 倍是判斷值，同業現值倍數事實表未涵蓋，無法附對照，只能和 CVNA 自身現值 48.4 倍比較。","bear":"機率 30%：共識近兩年成長高於內生上界，每台獲利也還在下滑。2028 至 2029 年融資收益與信用同時走弱，2031 年只賣約 130 萬台，營益率 7.5%。倍數取成長熄火對照（三年後成長降到 15%、10%、5%，約 24、18、12 倍，判斷值）的 10% 那格，18 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 其他收入 5.94 億美元，相當於調整後 EBITDA 的 74%；利率今年持續上升，每台其他毛利年減 299 美元。FY2022 曾出現 FCF −18.36 億美元、營益率 −11.06%。","assumption":"多頭假設信用轉差時融資管道仍然暢通，貸款買方持續接手。","consequence":"管道收緊時貸款留在帳上，現金轉負，成長被迫放慢。五年虧 50% 最可能就是這條路：約 130 萬台，EPS 1.60 美元，18 倍。","ruling":"採納，悲觀機率給 30%。這和唯一致命事件是同一條因果鏈，兩處一致。Gotham 報告的指控內容事實表未涵蓋，無法判斷是否指向同一處。","watch":"每台其他收入低於 2,200 美元連兩季、ABS 發行是否縮量、淨負債比。","evidence_refs":["major_events#3"],"fact_refs":["f_kpi2_ebitda_non_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 在 2026-10-28 表示寧可讓價值表現在台數上；2025 年底起把利率讓給客戶，2026-07-29 也承認庫存吃緊時讓利「probably didn't get fully paid」。CEO 同時承認 AI 代理可能提高提前清償。FY2025 FCF 只有淨利的 63%。","assumption":"多頭假設規模帶來的好處會留給股東。","consequence":"台數照基本情境，但營益率停在 9.5%，FY2031 EPS 約 3.30 美元，26 倍值 86 美元，五年年化約 3%。","ruling":"部分採納。基本情境營益率 11.5%，已低於管理層目標 1 個百分點。","watch":"每台 GAAP 營業利益、每台 SG&A、FCF 與淨利的比率。","evidence_refs":["substitute_technology#2"],"fact_refs":["f_kpi3_gaap","f_kpi1"]},{"view":"價格已反映太多","evidence":"Forward P/E 48.4 倍，EV/S 在四個年度端點的 87.4 分位。賺 12% 年報酬要 FY2031 EPS 約 5.0 美元，等於約 220 萬台、12% 營益率。","assumption":"現價假設成長放慢前倍數撐得住，或 FY2031 結果接近樂觀情境。","consequence":"基本情境終點 104 美元，五年年化約 7%；三情境機率加權五年約 +36%，年化約 6%，上下行比約 1.9。","ruling":"採納，本輪不追價，等 59 美元以下。","watch":"股價、FY2027E 共識 EPS。","fact_refs":["f_fwd_pe_latest","f_ev_s_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 73.57","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=73.57","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"單位獲利走向與管理層的路徑說法","cause":null,"prior_field":null,"side_a":"2026-10-28 CEO 說到 13.5% EBITDA 利潤率的路徑「extremely clear」，單靠費用槓桿就足以到 12.5% 營益率。","side_b":"Q3 每台費用持平，每台總毛利年減 410 美元，營收年增 42% 而營業利益只增 29%。2026-07-29 被問每台 EBITDA 何時回升時 CEO 沒給時間點，2026-10-28 再被問仍只談長期目標。","ruling":"程度差異，可調和。方向採信管理層，時點不採信。要到 12.5%，每台營業利益要從 3,284 美元升到約 4,620 美元，若全靠費用，每台費用要再降約四成，所以基本情境只算到 11.5%。","evidence_level":"高，財報數字與逐字稿","settle_metric":"每台 GAAP 營業利益年增率，看 2027 上半年兩季","if_then":["若 2027 上半年兩季每台 GAAP 營業利益轉為年增，但股價仍高於 59 美元，不追","若每台 GAAP 營業利益連兩季年減超過 300 美元，停止加碼","反向：股價先跌到 59 美元以下且每台 GAAP 營業利益未惡化，分批反買"]},{"axis":"庫存追上銷售的承諾","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO 表示有信心庫存成長會追上並可能超過銷售。","side_b":"2026-10-28 CFO 說上架可立即購買的車輛，成長率仍遠低於銷售；分析師估庫存約增 30%，銷量增 39%。Q3 產量略高於銷量。","ruling":"承諾尚未兌現，方向正確。CEO 稱成長主要受限於供應鏈，這條決定第一個假設能否成立。","evidence_level":"中，庫存年增率為分析師說法","settle_metric":"上架庫存年增率減零售台數年增率","if_then":["若連四季庫存成長仍低於銷量成長，停止加碼","若 2027 上半年庫存成長超過銷量成長，但股價高於 59 美元，不追"]},{"axis":"高價車組合是否為結構性轉變","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO 說偏向較新較貴車款「definitely not structural」，計畫回到較傳統的車齡里程組合。","side_b":"2026-10-28 CEO 說 prime 客群占比明顯上升，Q3 零售營收成長比台數高 15 個百分點，CFO 把 EBITDA 利潤率下滑部分歸因於高價車組合。","ruling":"管理層的一次性歸因未獲證實，也未被否定，列入監測。若到 2027 年 Q2 每台零售收入仍年增超過 5%，視為歸因證偽，利潤率目標要用每台金額重新檢視。","evidence_level":"中","settle_metric":"零售營收÷零售台數的年增率","if_then":["若 2027 年 Q2 每台零售收入仍年增超過 5% 且每台獲利未增，停止加碼"]},{"axis":"SEC 調查","cause":null,"prior_field":null,"side_a":"2025 年 6 月公司收到 SEC 傳票，主要涉及空方報告的指控。","side_b":"2026 年 9 月 SEC 告知已結束調查，不擬建議執法，未見財報重編。","ruling":"此風險退場。結案只代表沒有執法行動，不等於空方的所有指控都不成立。","evidence_level":"高，10-K 與 10-Q 原文","settle_metric":"已結案，不再需要判定","if_then":["若主管機關重啟調查或財報重編，清倉"],"evidence_refs":["regulatory_antitrust#0","major_events#0","major_events#1","sec_investigation_restatement#0"]},{"axis":"空方報告與證券集體訴訟","cause":null,"prior_field":null,"side_a":"2022 年證券集體訴訟仍在進行；2026-01-28 Gotham 報告後股價單日跌約 14.2%，多家律所宣布調查。","side_b":"搜尋未見 2026 年新案起訴，SEC 已結案，公司財報數字持續改善。","ruling":"不可裁決至集體認證或和解出現為止。求償金額、涉及營收與開庭日期事實表未涵蓋，這段證據不足以說風險已解除。","evidence_level":"低，缺金額與時程","settle_metric":"集體認證結果與和解金額","if_then":["若集體認證通過且和解金額超過 5 億美元，減碼一半","若出現刑事介入，清倉"],"evidence_refs":["major_events#2","major_events#3","lawsuit_class_action#0"]},{"axis":"停止給指引與追蹤可見度","cause":null,"prior_field":null,"side_a":"CFO 說轉向 GAAP 是公司成熟的自然演進。","side_b":"公司從 Q4 財報起不再提供展望，調整後 EBITDA 的重要性也會下降，而每台獲利正在下滑。","ruling":"轉向 GAAP 本身是好事，但外部監測變難。本報告的每台獲利關卡一律改用 GAAP 營業利益，避免口徑消失。","evidence_level":"中","settle_metric":"Q4 財報是否仍揭露每台毛利與費用拆解","if_then":["若公司同時取消每台毛利與費用拆解，停止加碼"]},{"axis":"Q3 獲利不如預期與共識未修正","cause":null,"prior_field":null,"side_a":"Q3 EPS 約 0.39 美元，低於共識 0.47 至 0.48 美元，含 5,300 萬美元一次性費用。","side_b":"兩份快照的 FY1、FY2、FY3 共識都沒有變動，FY1 仍是 1.52 美元。","ruling":"利空出現不到一季，共識可能還沒反映。Q4 財報出來之前凍結任何加碼。","evidence_level":"中，快照時點不明","settle_metric":"Q4 財報後 FY2027E 共識 EPS 是否低於 2.00 美元","if_then":["若 Q4 財報後 FY2027E 共識低於 2.00 美元且股價未跌，不追"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"結構轉好：FTC 要求揭露費用，對不收文件費的業者有利；CEO 認為 AI 代理放大實體摩擦的差異，線上化持續。","side_b":"競爭與融資壓力：10-K 預期新舊競爭者持續進入，Hertz 已進場；利率上升壓低每台融資收益，批發價處近三年高點。","ruling":"雙向拉鋸。零售端結構轉好，融資端面臨壓力，靠 Q3 份額續增與每台其他毛利年減 299 美元同時成立來支持這個判斷。","evidence_level":"中","settle_metric":"份額與每台其他收入","if_then":["若份額增速放慢且每台其他收入連兩季下滑，減碼"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"連續 11 季業界最快成長，資產負債表創紀錄，SEC 結案，股價 26 週跌 5.61%。若 FY2027 走樂觀路徑 2.30 美元，且倍數維持 38 倍，一年後約 87 美元，再等可能錯過。","side_b":"同一情境只給 19% 空間，而悲觀路徑五年虧 61%，上下行比約 1.9，基本情境年化約 7%。","ruling":"不採納現在進場。公司好不等於價格好，綁定約束只有價格，到 59 美元以下基本情境年化回到 12%。若訊號證實我錯，即 2027 上半年每台 GAAP 營業利益轉正成長且台數增 30% 以上，就把基本情境上修再重算進場價。","evidence_level":"中","settle_metric":"股價與 2027 上半年每台 GAAP 營業利益","if_then":["若股價先漲但每台獲利未回升，不追","若股價跌到 59 美元以下且基本面未受損，分批反買"]},{"axis":"估值分母","cause":null,"prior_field":null,"side_a":"Trailing P/E 35.37 倍，年度端點分位 0，看起來便宜。","side_b":"Forward P/E 48.4 倍，FY2026E 低於 FY2025A，營收卻預期成長 46%。","ruling":"採 Forward。Trailing 分母含不會重複或口徑不同的成分，不能用來說便宜。Q3 EPS 0.39 美元乘全部股數高於淨利 4.83 億美元，每股口徑也需要在原始財報上核對，本包無法查證。","evidence_level":"中","settle_metric":"10-K 的 FY2026 稀釋股數與稅率揭露","if_then":["若 FY2026 財報顯示正常化 EPS 低於 1.40 美元，不追"]}],"triggers":[{"n":1,"text":"貸款銷售管道中斷，或每台其他收入連兩季低於 2,200 美元。","type":"Single Thing","maps_to":"Single Thing","metric":"其他收入÷零售台數","threshold":"低於 2,200 美元連兩季，Q3 為 2,733 美元；或公告暫停主要貸款銷售管道","action":"清倉；未持有則不建倉","source_freq":"季報；ABS 發行文件每月","date":null},{"n":2,"text":"股價回到基本情境年化 12% 的價位。","type":"估值rearm","maps_to":"估值","metric":"收盤價","threshold":"不高於 59 美元","action":"重跑研究，基本面關卡未觸發才分批建倉","source_freq":"每日","date":null},{"n":3,"text":"台數成長是否維持基本情境路徑。","type":"假設驗證","maps_to":"H1","metric":"零售台數年增率","threshold":"連兩季低於 25% 視為偏離","action":"下修基本情境，價位未到不動作","source_freq":"每季","date":"2027-02"},{"n":4,"text":"每台獲利是否恢復成長。","type":"假設驗證","maps_to":"H2","metric":"GAAP 營業利益÷零售台數","threshold":"2027 上半年連兩季年增","action":"上修基本情境並重算進場價","source_freq":"每季","date":"2027-08"},{"n":5,"text":"每台獲利持續惡化。","type":"減碼","maps_to":"R1","metric":"每台 GAAP 營業利益年變動","threshold":"連兩季年減超過 300 美元，Q3 年減約 250 美元","action":"減碼一半；未持有則延後進場","source_freq":"每季","date":"2027-02"},{"n":6,"text":"整備產能跟不上銷售。","type":"風險","maps_to":"R2","metric":"上架庫存年增率減零售台數年增率","threshold":"連四季為負","action":"停止加碼","source_freq":"每季，法說會","date":"2027-08"},{"n":7,"text":"外部成本吸收失敗，包含油價、關稅與批發車價。","type":"風險","maps_to":"R3","metric":"零售 GPU","threshold":"低於 3,200 美元連兩季，Q3 為 3,625 美元","action":"停止加碼","source_freq":"每季","date":"2027-02","evidence_refs":["reg_tariff_export#0","supply_demand_durability#3"]},{"n":8,"text":"證券訴訟出現不利進展。","type":"風險","maps_to":"R4","metric":"集體認證與和解金額","threshold":"集體認證通過且和解超過 5 億美元；或刑事介入","action":"前者減碼一半，後者清倉","source_freq":"10-K、10-Q 法律事項","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":9,"text":"建倉後基本面連續驗證才加碼。","type":"加碼","maps_to":"H2","metric":"每台 GAAP 營業利益與淨負債比","threshold":"連兩季年增且淨負債比低於 1 倍","action":"分批加碼至目標倉位","source_freq":"每季","date":null},{"n":10,"text":"Q4 財報後複審，含共識是否下修與指引取消後的揭露內容。","type":"複審日期","maps_to":"全部","metric":"Q4 2026 財報","threshold":"財報發布後一週內","action":"重跑研究","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"每台其他收入（其他收入÷零售台數）","bear_threshold":"低於 2,200 美元連兩季","window":"兩季","source":"公司季報","last_status":"ok"},{"metric":"每台 GAAP 營業利益年變動","bear_threshold":"年減超過 300 美元連兩季","window":"兩季","source":"公司季報","last_status":"warning"},{"metric":"零售台數年增率","bear_threshold":"低於 20% 連兩季","window":"兩季","source":"公司季報","last_status":"ok"},{"metric":"淨負債對 TTM EBITDA","bear_threshold":"高於 2.0 倍","window":"單季","source":"公司季報，指標停揭時用 GAAP 數字自算","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價收在 59 美元以下，基本情境五年年化回到 12%；觸發後重跑研究，不直接建倉","exec_line":"現價不追。股價到 59 美元以下且每台 GAAP 營業利益年減未擴大，重跑研究後先建首筆；Q4 財報前凍結任何加碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2026E 到 FY2028E 年化 34% 的 EPS 定價，等於假設每台獲利止跌回升；但 Q3 每台 EBITDA 年減約 400 美元，費用沒有槓桿，營業利益增速低於營收 13 個百分點。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價收在 59 美元以下，此時基本情境五年年化回到 12%；到價後重跑研究。","qc48_result":"pass","qc48_note":"Bull 路徑是用台數、每台收入、營益率和股數推出來的算術，不是題材敘事，管理層 300 萬台目標也查得到;但本次沒有找到可比案例的五年報酬數字，Bull 隱含年化 21.9% 是否合理無法驗證，只能算有條件成立。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"產能擴張撐得住台數成長，FY2027 年增約 26%，FY2028 約 21%。","2y":"FY2028 零售台數約 122 萬台","5y":null,"10y":null,"threshold":"FY2027 年增不低於 25%，FY2028 不低於 20%","source":"公司季報零售台數；法說會的整備產量與上架庫存說明","drift_rule":"TTM 台數偏離路徑 5% 以上連兩季為削弱，10% 以上連三季為反轉"},{"id":"H2","text":"費用槓桿讓每台獲利恢復成長，GAAP 營益率逐年上升。","2y":null,"5y":"FY2031 GAAP 營益率 11.5%","10y":null,"threshold":"FY2028 不低於 10%，FY2031 不低於 11.5%","source":"公司季報 GAAP 營業利益與營收","drift_rule":"TTM 營益率偏離路徑 5% 以上連四季為削弱，10% 以上連六季為反轉"},{"id":"H3","text":"規模優勢延續，公司走到年賣 300 萬台。","2y":null,"5y":null,"10y":"2036 年前年賣 300 萬台，約占全美二手車總量 8%","threshold":"FY2031 年賣不少於 185 萬台","source":"公司年報台數；Cox Automotive 產業總量","drift_rule":"跨兩個年度落後路徑為削弱，跨三個年度為反轉"}],"R":[{"id":"R1","text":"利率、信用或貸款買方需求轉差，壓低融資收益。","h_ref":"H2","clock":"⚡","threshold":"每台其他收入低於 2,200 美元連兩季","evidence_refs":[]},{"id":"R2","text":"整備與人力擴張跟不上，新場站成本偏高，成長放慢或費用上升。","h_ref":"H1","clock":"🔥","threshold":"上架庫存成長低於銷量成長連四季，或台數年增低於 20% 連兩季","evidence_refs":[]},{"id":"R3","text":"批發車價處高點、供給偏緊，加上油價與關稅，車源與運輸成本吸收不了。Cox 與公司都以環境穩定為前提。","h_ref":"H2","clock":"🔥","threshold":"零售 GPU 低於 3,200 美元連兩季","evidence_refs":["supply_demand_durability#3","reg_tariff_export#0"]},{"id":"R4","text":"空方報告衍生的法律風險與 2022 年集體訴訟，金額與時程未知。","h_ref":"H3","clock":"🐢","threshold":"集體認證通過且和解超過 5 億美元，或刑事介入","evidence_refs":["major_events#2","major_events#3","lawsuit_class_action#0"]}],"single_thing":{"description":"貸款銷售管道中斷：ABS 市場或整批貸款買方在一季內拒買，或要求的價差使利得接近歸零。","why_fatal":"Q3 其他收入 5.94 億美元，相當於調整後 EBITDA 的 74%。每台少 1,000 美元，FY2031 基本 EPS 約少 0.95 美元，約 24%；相比之下營益率每 1 個百分點約 9%，倍數每 1 倍約 4%。它是最大的單一敏感度。","if_happens":"貸款留在帳上，營運資金吸走現金，0.8 倍淨負債比快速惡化，成長被迫放慢。FY2022 的 FCF −18.36 億美元、營益率 −11.06% 是前例。此時應清倉，不等下一季確認。","how_monitor":"每季其他收入÷零售台數；每月 ABS 發行規模與是否縮量；法說會揭露的貸款買方變動。","probability":"12 至 24 個月約 10%，判斷值；貸款買方集中度事實表未涵蓋，可能低估。"}},"appendix_a":{"growth_durability":8,"quality_score":7.5,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":34.7,"peg_fy2":1.02,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.69,"FY2026E":1.52,"FY2027E":2.12,"FY2028E":2.73},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS；FY2026E 至 FY2028E 為 Koyfin 共識，GAAP 或調整後未標明，EPS 家數未載明。FY2025A 含不會重複的成分，成長判斷改以 FY2026E 為基期。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報（日期未公告，依往例推估），公司自此不再提供展望，2027 年起以 GAAP 為主","impact":"高","watch":"每台 GAAP 營業利益、零售台數、每台毛利與費用拆解是否續揭露"},{"date":"2027-03","date_precision":"quarter","type":"macro","event":"租賃退場車回升，次級來源轉述 Manheim 預估 2027 年 310 萬台","impact":"中","watch":"批發與零售價差、零售 GPU"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"完整轉換的 ADESA 場站陸續上線，時點為推估，新場站初期成本偏高","impact":"中","watch":"每台營運費用、整備產量相對銷量"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新車經銷據點是否擴展到 Stellantis 以外的車廠，時點未揭露","impact":"低","watch":"新車業務揭露與車廠合作"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2026E 到 FY2028E 年化 34% 的 EPS 定價，等於假設每台獲利止跌回升；但 Q3 每台 EBITDA 年減約 400 美元，費用沒有槓桿，營業利益增速低於營收 13 個百分點。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-5.61, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑是用台數、每台收入、營益率和股數推出來的算術，不是題材敘事，管理層 300 萬台目標也查得到;但本次沒有找到可比案例的五年報酬數字，Bull 隱含年化 21.9% 是否合理無法驗證，只能算有條件成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價收在 59 美元以下，此時基本情境五年年化回到 12%；到價後重跑研究。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
