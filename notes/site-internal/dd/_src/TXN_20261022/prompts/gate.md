你是 DD 管線 v20 的判斷層閘（gate），標的 TXN（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（33 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝5463 US$M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.ti.com "TI reports second quarter 2026 financial results and shareholder returns" (https://investor.ti.com/news-releases/news-release-details/ti-reports-second-quarter-2026-financial-results-and-shareholder)（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-22））
  - 註記：consensus 約 US$5.24B（來源：Q2 FY26 earnings call 前市場預期彙整，Investing.com transcript 摘要引用，非公司揭露）；實際 $5.463B 超出約 4.3%
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益／利益率＝42.28 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.ti.com Q2 FY26 press release（Operating profit US$2,310M / Revenue US$5,463M）。註：TI 未另外揭露 Non-GAAP 營業利益／利益率，本季亦無 non-GAAP 財報揭露欄位（僅 FCF 為官方 non-GAAP 指標），故通用必填第2、3項合併為此欄（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-22））
  - 註記：查無市場對 GAAP 營業利益率之獨立 consensus 數字
- `f_kpi4_q3_fy2026_guidance_eps`（q1_business）｜管理層 Q3 FY2026 guidance（營收／EPS 區間）＝— 營收 US$5.65B–6.15B（中值 US$5.90B）；GAAP EPS US$2.23–2.57（中值 US$2.40）｜期間與口徑：公告於 2026-07-22（隨 Q2 FY2026 財報同步發布）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investor.ti.com Q2 FY26 press release（numbers.latest_quarter_kpis.items[4]，as_of 公告於 2026-07-22（隨 Q2 FY2026 財報同步發布））
  - 註記：查無公告當下市場對 Q3 guidance 的獨立 consensus 對照
- `f_kpi5_inventory_days`（q1_business）｜存貨天數（inventory days，半導體週期性參考指標）＝196 天｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 FY26 earnings call CFO 評論（媒體 transcript 轉述，非新聞稿正文；Investing.com "Earnings call transcript: Texas Instruments beats Q2 2026 estimates"），信心層級較低，建議 writer 交叉確認（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-22））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-21 date｜期間與口徑：2026-10-21／距今 1 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-21）
- `f_peer_txn_gross_margin_pct`（q2_moat）｜TXN 毛利率＝58.33 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_txn_operating_margin_pct`（q2_moat）｜TXN 營業利益率＝38.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_txn_fcf_margin_pct`（q2_moat）｜TXN FCF 利潤率＝27.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2308_tw_gross_margin_pct`（q2_moat）｜2308.TW 毛利率＝35.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vrt_gross_margin_pct`（q2_moat）｜VRT 毛利率＝38.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝8.44 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝10.65 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝13.52 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝4.0 %｜期間與口徑：2026-10-21／兩份 Koyfin 快照之間的 EPS 修正幅度（13.0 → 13.52）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝21972.06 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（30 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝25183.36 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi2_fcf_chips_act`（q4_capital）｜自由現金流（FCF，公司定義：營運現金流減資本支出＋CHIPS Act 激勵）＝2738 US$M（本季）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.ti.com Q2 FY26 press release（Operating cash flow US$2,703M；本季 FCF US$2,738M；TTM FCF US$6,534M，約當 TTM 營收 33.6%，YoY+271%）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-22））
  - 註記：查無單季 FCF 之市場 consensus 資料
- `f_kpi3_sbc_gaap`（q4_capital）｜SBC（股票薪酬）占營收／占 GAAP 營業利益 %＝2.32 % of revenue（另：占 GAAP 營業利益 5.50%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.ti.com Q2 FY26 press release（Stock compensation US$127M；US$127M/US$5,463M=2.32%；US$127M/US$2,310M=5.50%）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-22））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝7051.0 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 14052.0、現金 7001.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝913.25 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.995 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝284.65 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝33.73 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 8.44，分子＝快照價 284.65｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝43.33 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.36 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-21（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝8.21 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 7.8 → 8.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_rsi14`（q5_valuation）｜RSI(14)＝55.82｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝21.69 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-10-22／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
  - 原文：「price 284.65 / W52 238.21 / W104 209.39 / W250 179.8 / W250 13週斜率 1.1%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝238.21 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w250`（q5_valuation）｜250 週均線＝179.8 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Over the past five years, Chinese domestic analog vendors (e.g., SG Micro, 3Peak) have gradually eroded overseas incumbents' (including TI's) share in telecom and consumer-electronics segments, driven by geopolitical friction and China's domestic-substitution push, though their overlap is concentrated in TI's mid-to-low-end part numbers rather than the full portfolio.
  - 來源：Chinese analog chip vendors brace for impact as Texas Instruments slashes prices (jw.ijiwei.com); Citrini Research "Semis Memo: Supply Chain Inheritance"（as_of 2026-05-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：TI, NXP and Infineon raised analog IC prices effective April 2026 (TI hikes up to 85% on select parts), and TI announced a third sweeping price increase in May 2026 effective July 1, 2026. Analysts flagged that end customers seeking to avoid TI's price hikes may accelerate adoption of Chinese domestic alternatives, especially in long-cycle industrial and automotive sectors.
  - 來源：BigGo Finance: "Texas Instruments' Third Price Hike in Six Months Ignites New Analog Chip Cycle, Opening Triple-Bonanza Window for China's Domestic Substitution"（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：TI management cautioned in Q1 2026 commentary that customer inventory depletion appears complete but 'any renewed economic weakness could trigger another destocking phase' — i.e. end-customer macro-demand risk (not a TI-specific customer credit event) has not been eliminated.
  - 來源：TI Q1 2026 earnings commentary (Yahoo Finance / Globe and Mail republication of TI investor materials)（as_of 2026-04-22）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：截至 2026-06 該併購案在中國市場監管總局（SAMR）的申報尚未被正式受理（filing not yet accepted），中國反壟斷結清仍是交易能否完成的關鍵未決條件；TI 中國營收占比約 20%、Silicon Labs 約 15%，中國政府過去曾用反壟斷審查程序卡關美系半導體併購案。
  - 來源：MLex "Texas Instruments, Silicon Labs merger filing not yet accepted in China" (2026-06)（as_of 2026-06-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：中國半導體行業協會（CSIA）發布通知，明確以晶圓廠（wafer fabrication facility）所在地認定晶片原產地以適用對美關稅；由於 TI 晶片多在美國本土廠生產，被認定為對中國關稅特別敏感的美系晶片廠之一，TXN 股價當日重挫 9% 至 $142.66，為 2020 年 3 月以來單日最大跌幅。
  - 來源：Investing.com "US semiconductor manufacturer stocks fall on China tariff concerns"; barchart.com "why texas instruments txn stock is falling today"（as_of 2026-01）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：中國對美進口商品加徵 34% 全面關稅（貿易戰升級），對高度依賴中國需求的美系晶片廠（含 TI）構成利潤率壓縮與市占流失風險；委外代工（outsource manufacturing）的美系晶片廠則被中國官方協會排除在報復性關稅之外，形成自有晶圓廠（IDM，如 TI）相對代工客戶的競爭劣勢。
  - 來源：stocktwits.com "US Chipmakers Who Outsource Manufacturing To Be Exempt From China Tariffs, Says State-Backed Association"（as_of 2026-01）｜affects：thesis.R、moat_trend、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：TI 終端客戶總部設於中國的營收占比約 20%（依 TI 最新年報揭露），為公司在中國市場政策／需求面的主要地緣曝險來源；公司財報並揭露面臨關稅、進出口管制、貿易禁運與制裁等地緣政治貿易障礙的一般性風險敘述。
  - 來源：Texas Instruments 2024 Annual Report / Notice of Annual Meeting (investor.ti.com)（as_of 2025）｜affects：thesis.R、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：In the broader analog semiconductor market, unit shipment growth (6.98% CAGR 2026-2031) is projected to outpace revenue growth, indicating persistent price pressure in commodity analog categories.
  - 來源：Analog Semiconductor Market Size, Share & Research Report (Coherent Market Insights / GMInsights)（as_of 2026-01-01）｜affects：moat_trend、thesis.R、valuation
- `end_markets#11`（end_markets｜方向 -｜狀態 ok）：In the competing microcontroller/embedded segment, Infineon Technologies led global market share at 21.3% in 2024, ahead of TXN — unlike its #1 analog position, TXN is not the share leader in embedded/MCU.
  - 來源：What is Competitive Landscape of Texas Instruments Company? (MatrixBCG.com)（as_of 2024-12-31）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":518.4,"bear_5y_price":188.1,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":21.2,"ev5y_pct":19.9,"irr_base_pct":3.9,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.44,"pe":33.73,"basis":"2026 年共識 EPS 8.44 美元（Koyfin 2026-10-21）對現價 284.65；終端倍數同為前瞻一年口徑。"},"eps":{"bull":[11.8,14.8,16.2,17.6,19.2],"base":[11.0,13.0,12.2,13.6,15.0],"bear":[9.6,7.6,7.9,8.9,9.9]},"pe":{"bull":27,"base":23,"bear":19},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.995,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TXN_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Rafael Lizardi｜guidance：CFO 給 Q3 營收區間（56.5–61.5 億美元）（原話："We expect TI's revenue in the range of $5.65 billion to"）
- 2026-07-22｜Rafael Lizardi｜guidance：Q3 EPS 區間 2.23–2.57 美元（原話："earnings per share to be in the range of $2.23 to $2.57."）
- 2026-07-22｜Haviv Ilan｜guidance：CEO 稱 Q3 高於季節性的貢獻來自所有市場（原話："I expect strong demand across the board."）
- 2026-07-22｜Rafael Lizardi｜margin：Q2 毛利率 61%，季增 340 bp（原話："or 61% of revenue. Sequentially, gross profit margin"）
- 2026-07-22｜Rafael Lizardi｜margin：Q2 EPS 含 0.05 美元未列入原財測的離散稅務利益（原話："Earnings per share included a $0.05 benefit not in our"）
- 2026-07-22｜Rafael Lizardi｜margin：Q3 OpEx、其他收支、併購費用預期與 Q2 持平（原話："you should expect all of those to be flat second quarter"）
- 2026-07-22｜Julie Knecht｜margin：新任 CFO 稱 Q3 增量毛利率（不含折舊）70%–85% 為建模參考（原話："that 70% to 85% is a good placeholder."）
- 2026-07-22｜Haviv Ilan｜margin：CEO 補充 Q3 毛利率不會持平，應略高（原話："But it shouldn't be flat. It should be a little higher."）
- 2026-07-22｜Mike Beckman｜margin：資料中心毛利率目前與公司平均相近，不預設偏向（原話："it's been pretty similar to the overall corporate average."）
- 2026-07-22｜Haviv Ilan｜customer：資料中心 Q2 年增一倍、季增約 20%（原話："Data center doubled year-on-year and grew around 20%"）
- 2026-07-22｜Haviv Ilan｜customer：工業 Q2 年增約 30%、季增約 10%（原話："increased around 30% year-on-year and was up about 10%"）
- 2026-07-22｜Haviv Ilan｜customer：車用需求於季內逐步堆高，以中國為首（4 月電話會時能見度不同）（原話："It built up as we went through the quarter, led by China."）
- 2026-07-22｜Haviv Ilan｜customer：管理層稱處於範圍很廣的循環起點（原話："we are in the start of a cycle that is very, very broad."）
- 2026-07-22｜Haviv Ilan｜customer：個人電子 Q3 預期季增但幅度低於常態，客戶受缺貨壓力（原話："We are seeing challenges in PE as some shortages are"）
- 2026-07-22｜Haviv Ilan｜customer：工業仍低於 2022 年高峰約 5–6 個百分點（原話："5 or 6 points"）
- 2026-07-22｜Haviv Ilan｜customer：工業復甦歸因於客戶庫存去化結束與新世代系統（原話："New systems that were designed in the last 4 or 5 years."）
- 2026-07-22｜Haviv Ilan｜guidance：Q3 成長絕大部分為出貨量，漲價貢獻幾乎不顯著（原話："the vast majority of it is just unit growth and"）
- 2026-07-22｜Haviv Ilan｜risk：上半年價格持平（符合先前預期）（原話："And as we predicted, pricing was stable"）
- 2026-07-22｜Haviv Ilan｜commitment：管理層稱已開始執行漲價（上季為討論可能性）（原話："we have started executing price increases, yes."）
- 2026-07-22｜Haviv Ilan｜commitment：漲價逐客戶談判，Q3 起部分生效並延續至 Q4 及明年（原話："Some of it will start to play in, in Q3"）
- 2026-07-22｜Haviv Ilan｜risk：交期原低於 13 週（原話："They were below 13 weeks, in Q2"）
- 2026-07-22｜Haviv Ilan｜risk：交期小幅拉長約數週，因需求成長（原話："Maybe a couple of weeks higher"）
- 2026-07-22｜Mike Beckman｜guidance：訂單與遠期 backlog 於季內皆增加（原話："we did see backlog build"）
- 2026-07-22｜Mike Beckman｜guidance：backlog 增加已反映在財測中（原話："And it's reflected in the guide."）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：2026 資本支出維持 20–30 億，不偏向低端（原話："I would not skew it or bias it lower on the lower end"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：未來資本支出偏重美國以外的封測，該部分無 ITC（原話："disproportionately placed in the assembly test operation"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：資本支出經驗法則：以成長率 1.2 倍估算資本密集度（原話："the framework we've given you, 1.2x the"）
- 2026-07-22｜Julie Knecht｜capital_allocation：產能：Q2 稼動率提高並於季內持續上升（原話："So our loadings did increase from first to second quarter."）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：TTM 自由現金流含 16 億 CHIPS Act 獎勵（原話："cash flow in the trailing 12 months includes $1.6 billion"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：庫存 46 億美元（天數 196 天，季減 13 天）（原話："Inventory at the end of the quarter was $4.6 billion"）
- 2026-07-22｜Haviv Ilan｜commitment：自由現金流框架（營收 200 億對 80–90 億、220 億對 90–100 億）仍有效（原話："So that framework is still valid, Jim."）
- 2026-07-22｜Haviv Ilan｜commitment：目標為超越市場而非設定資料中心成長率，2026 預期達成（原話："to outgrow the market. I believe we will do it in 2026,"）
- 2026-07-22｜Haviv Ilan｜commitment：潔淨室與產能足以支應未來約三年；2027 資本支出細節留待二月（原話："we are good for the next 3 years, okay?"）
- 2026-07-22｜Julie Knecht｜commitment：Silicon Labs 交易預計明年上半年完成（原話："We still expect to close in the first half of next year."）
- 2026-07-22｜Haviv Ilan｜competition：稱競爭對手 52 週交期對 TI 是新設計機會（原話："competition talks about lead times that are 52 weeks away"）
- 2026-07-22｜Haviv Ilan｜competition：稱可能在較大內容量機會上拿到市占（需時間驗證）（原話："we grew share on the larger content opportunity"）
- 2026-07-22｜Haviv Ilan｜competition：800V 架構視為 TAM 擴大、轉換級數增加（原話："higher growth of the TAM, more conversion stages"）
- 2026-07-22｜Haviv Ilan｜product：資料中心優勢含供貨能力，強調地緣政治可靠產能（原話："geopolitical dependable capacity like we hold"）
- 2026-07-22｜Haviv Ilan｜risk：Q3 成敗在執行：提高產能稼動並追逐需求（原話："We are ramping our factories. We are going after it."）

### TXN_Shareholder_Analyst_Call_Texas_Instruments_Incorporated_20260416.md
- 2026-04-16｜Unknown Attendee（Chevedden 代表）｜risk：股東提案代表指出 TI 召開股東臨時會需持有 25% 流通股（治理面，非營運面）。（原話："requires the backing of 25% of all shares outstanding"）
- 2026-04-16｜Unknown Attendee（Chevedden 代表）｜commitment：提案人主張以書面同意讓股東在年會之間採取行動（提案 4）。（原話："take action between annual meetings"）
- 2026-04-16｜Haviv Ilan（Chairman）｜commitment：董事長宣布初步投票結果：公司提案全數通過，股東提案未通過。（原話："all company proposals have passed"）

### 問答異常語氣（迴避／改口／保留）
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Stacy Rasgon 追問個人電子 Q3 年增是持平或下滑｜答法：IR 表示不提供各終端市場財測，僅重申 Q2 觀察，未回答方向
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Vivek Arya 詢問 2027、2028 後資料中心合理成長率｜答法：CEO 先說 I don't think I can help there，不給數字，改談超越市場的目標
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Vivek Arya 要求量化漲價對 Q3 約 8% 季增的貢獻及 Q4 能否再漲｜答法：僅答 Q3 漲價貢獻幾乎不顯著，未直接回答 Q4 是否再漲

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 12 | 6 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260907","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"capex 過峰後 FCF/share 由 2025 $3.23 重建至 2026 &gt;$8，並回到約 10% CAGR 趨勢線","columns":{"2Y驗證點":"2026 FCF/share ≥$8、2027 ≥$9；2026 capex $2–3B、折舊 $2.2–2.4B","5Y驗證點":"FCF/share CAGR ≥10%、FCF 利潤率 ≥30%","10Y驗證點":"FCF/share 複利 10% 且股數持續淨減","具體數字門檻":"2026 FCF/share &lt;$8 削弱；&lt;$7 反轉","信息來源":"年報（2027-01）／資本管理會（2027-02）","漂移觸發條件":"連 4 季 TTM FCF/share 偏離軌道 ≥5% 削弱；連 6 季 ≥10% 反轉"}},{"id":"H2","text":"工業／車用復甦為多年上行週期而非單季回補：GM 從 56% 回到 60% 以上、GAAP 營益率守 40%+","columns":{"2Y驗證點":"TTM GM ≥60%；工業營收距 2022 峰值缺口由 25% 收斂至 &lt;10%","5Y驗證點":"GM 穩定 62–65%（稼動率 80–90% 甜蜜區）","10Y驗證點":"類比份額由 17.8–19% 續升","具體數字門檻":"TTM GM 連 4 季 &lt;60% 削弱；&lt;58% 反轉","信息來源":"季報","漂移觸發條件":"連 2 季 TTM GM 偏離 ≥5%（相對）削弱；連 3 季 ≥10% 反轉"}},{"id":"H3","text":"資料中心成為第二曲線：可觸及市場 $7.5B→$12.5B（+65%），TI 約 20% 份額、營收年增 &gt;50%","columns":{"2Y驗證點":"資料中心營收年增 ≥30%（2027）","5Y驗證點":"資料中心占營收 ≥15%","10Y驗證點":"800V 架構下 GaN＋控制 IC 份額守住","具體數字門檻":"連 2 季 &lt;30% 削弱；&lt;15% 反轉","信息來源":"季報（資料中心自 2026 起獨立揭露）","漂移觸發條件":"連 2 季年增 &lt;30% 削弱；連 3 季 &lt;15% 反轉"}},{"id":"H4","text":"中國約 20% 營收守得住：本土替代只吃中低階料號，TI 2025 在中國仍取得份額（來源：摘要）","columns":{"2Y驗證點":"中國營收占比 ≥18%","5Y驗證點":"≥15% 且中國以外成長補足","10Y驗證點":"美中脫鉤基準情境下仍能出貨類比與嵌入式","具體數字門檻":"連 4 季合計 −3pp 或 &lt;17% 削弱；&lt;15% 反轉","信息來源":"年報／季報地區揭露","漂移觸發條件":"連 4 季合計偏離 ≥3pp 削弱；連 6 季 ≥5pp 反轉"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8","irr_base_pct":8.5,"ev5y_pct":44.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":4.8,"ev5y_pct":44.7,"irr_base_pct":8.5,"max_dd_pct":-45,"bull_5y_price":546.0,"bear_5y_price":208.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8","price_at_dd":258.44,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TXN","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Texas Instruments"},"oneliner":"類比龍頭進入全面上行週期，Q3 營收年增 28%、毛利率 64%，生意比前份更強；但現價對 2027 年共識本益比約 27 倍，基準五年年化僅約 6%，持有不追，等回到 245 美元以下或一月漲價指引落地再加碼。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/scenario.json","answers":{"q1_business":{"verdict":"TI 的收入來自十萬家以上工業、車用與資料中心客戶購買的類比和嵌入式晶片。獲利的關鍵在自家 300mm 廠的稼動率與價格：稼動率回升時，增量毛利（不含折舊）有 75–85% 落到損益。","reasoning":"最新一季（2026-10-21 法說，財務長 Julie Knecht）營收 61 億美元，季增 11%、年增 28%。其中類比年增 32%、嵌入式年增 21%、其他年減 6%。毛利率 64%（季增 280bp），營益率 47%，EPS 2.62 美元。前一季營收 54.63 億美元、GAAP 營益率 42.3%；其中類比 43.7 億、嵌入式 7.88 億，兩個主力分部都超過營收一成。終端市場方面，工業略高於營收三分之一，年增逾 40%，首度回到 2022 年 Q3 的水準；資料中心約占營收 13%，年增約 95%；車用年增十幾%；個人電子持平。Q4 指引營收 58–63 億、EPS 2.45–2.79，幾乎持平，遠強於往年 Q4 的季節性下滑。客戶結構分散：無單一客戶超過營收一成，八成以上直接銷售。產業態勢屬雙向拉鋸。結構轉好的一面：過去四年類比幾乎沒有新增潔淨室，代工廠也把產能移出類比，而 TI 九成自製。其他結構變動的一面：中國以晶圓廠所在地認定原產地並加徵報復性關稅，本土廠也在替代中低階料號。沒有單一客戶依賴，集中度風險在中國約兩成營收。存貨天數 194 天，季減 2 天。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi4_q3_fy2026_guidance_eps","f_kpi5_inventory_days","f_earnings_recency"],"verdict_values":{"revenue_quality":"需求分散：十萬家以上客戶、無單一客戶逾一成、八成以上直接通路。本輪成長以出貨量為主，2026 下半年起加上漲價，另有部分客戶趕料，品質中上。","unit_econ_note":"長期增量毛利模型（不含折舊）為 75–85%。Q3 增量毛利率約九成，主要來自營收放大，其次是價格、稼動率與產品組合，不宜外推。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"自建 300mm 成熟製程的成本領先，加上數萬料號的目錄廣度；獲利隨稼動率大幅擺動。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性為主，結構性為輔：四年少擴產加上代工廠撤出類比產能，使供給偏緊，這一點屬結構性；但趕料與交期拉長帶動的需求屬週期性，兩到三年內會反轉。管理層稱各終端與地區全面成長。","bargaining":{"up":"機台與外包封測交期拉長，封測代工拿不到足量，供應商議價力上升；晶圓九成自製，不受代工廠議價。","down":"客戶十萬家以上、無單一客戶逾一成、八成直接銷售，議價力在 TI；2026 下半年類比已開始漲價。","geo":"中國約兩成營收，美國自製的產品在中國原產地規則下吃虧；但在西方客戶眼中屬地緣可靠產能，成為取得訂單的理由。"},"profit_pool_dir":"類比利潤池往擁有自有成熟製程產能者集中；中低階料號的利潤池則往中國本土廠流出。","tam_table":[{"item":"資料中心類比加嵌入式可觸及市場","value":"2025 年約 75 億美元，2026 年約 125 億美元（第三方估計）"},{"item":"TI 資料中心營收與份額","value":"2025 年約 15 億美元、約兩成份額；2026 年 Q3 約占營收 13%、年增約 95%、出貨約一萬個料號"},{"item":"全球類比份額","value":"2025 年 17.8–19%，排名第一"},{"item":"工業營收位置","value":"2026 年 Q3 首度回到 2022 年 Q3 高點；九至十個子領域中，部分仍低於前高"}]}}},"q2_moat":{"verdict":"護城河擴大（↑）。機制是自有 300mm 廠的單位成本，加上目錄廣度與直接通路；在供給偏緊時，以較短交期和地緣可靠產能換到價格與訂單。","reasoning":"可證方向有三。第一，毛利率：2026 年 Q3 為 64%，前一季 61%，TTM 58.3%。2025 年全年 57% 的谷底主要來自擴產折舊與低稼動，不是失去定價權。第二，價格：2026 上半年價格持平，下半年類比開始漲價，客戶接受（2026-10-21 Haviv Ilan）。第三，交期：同業交期長達 52 週（2026-07-22 Haviv Ilan），TI 仍自稱交期最具競爭力。事實表的同業是電源設備廠：TI 的 TTM 毛利率 58.3%、營益率 38.1%、自由現金流利潤率 27.5%，都高於台達電、Vertiv、Eaton；但這些不是直接同業，利差不能當份額證據。反向證據也存在：份額增加管理層自承尚無法量測；中國本土廠持續替代中低階料號；嵌入式並非份額龍頭。評分上，執行 9、定價 8；威脅以點對點為主，不扣分。","fact_refs":["f_peer_txn_gross_margin_pct","f_peer_txn_operating_margin_pct","f_peer_txn_fcf_margin_pct","f_peer_2308_tw_gross_margin_pct","f_peer_vrt_gross_margin_pct","f_peer_etn_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"自有 300mm 成熟製程廠帶來單位成本領先，搭配數萬料號的目錄廣度與八成直接通路。設計導入後，車用與工業的重新認證週期長，形成轉換成本；供給吃緊時，產能本身也成為護城河。","execution":9,"pricing":8,"grade":"A","trend":"↑","trend_evidence":"支持擴大的證據：Q3 毛利率 64%（季增 280bp）；類比下半年開始漲價且客戶接受；工業營收創四年新高；Sherman 第二模組與馬來西亞封測廠持續擴產；代工廠把產能移出類比。反向證據：份額增加管理層自承無法量測；中國中低階料號持續被本土廠替代。","competitor_notes":[{"name":"2308.TW","strategy_note":"電源系統廠，屬 TI 的客戶端環節而非類比晶片對手；毛利率約 36%，只能說明 TI 位於價值鏈利潤較厚的一段。"},{"name":"VRT","strategy_note":"資料中心電力與散熱設備商，是 TI 資料中心需求的下游；自由現金流利潤率 25%，與 TI 不在同一競爭層。"},{"name":"ETN","strategy_note":"電氣設備商，受惠於電網重建，與 TI 工業能源基礎建設的成長同源，不構成直接競爭。"},{"name":"SU.PA","strategy_note":"事實表無財務資料；屬電氣設備廠，角色同 ETN。"},{"name":"英飛凌","strategy_note":"2024 年微控制器份額約 21% 居首，TI 在嵌入式並非龍頭；同時也是 2026 年 4 月一同漲價的對手。"},{"name":"中國本土類比廠（聖邦微、思瑞浦）","strategy_note":"在通訊與消費性的中低階料號替代外資，受國產化政策推動；TI 漲價後替代誘因上升。"}],"peer_na_reason":"事實表同業為電源設備廠，非類比晶片同業；ADI、Microchip 等直接同業的利潤率與報酬率數字事實表未涵蓋。","threats":[{"level":"🟡","text":"中國本土類比廠在中低階料號替代，TI 漲價（部分料號最高 85%）可能加速轉單。","p":"30%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3"]},{"level":"🟡","text":"中國以晶圓廠所在地認定原產地並加徵報復性關稅，美國自製的 TI 相對委外代工的美系同業吃虧。","p":"25%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"level":"🟡","text":"通用類比的出貨量成長預估快於營收，表示價格長期受壓。","p":"30%","evidence_refs":["end_markets#3"]},{"level":"🟡","text":"嵌入式與微控制器份額落後英飛凌，Lehi 廠的產能能否換成份額尚未證實。","p":"30%","evidence_refs":["end_markets#11"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"類比是任何電子系統的必需品。使用者、決策者、付款者都在系統廠，三角色一致。Q3 各終端與地區全面成長，工業設備每代的晶片內容增加（2026-10-21 Haviv Ilan）。"},{"item":"決策層級","level":"🟡","text":"在單一料號設計導入層級，車用與工業的重新認證週期長，替代性低；但中低階通用料號可被本土廠逐顆替代，漲價後轉單誘因上升。"},{"item":"價值鏈分配","level":"🟢","text":"類比占系統物料成本比例小，客戶為供貨保證願付溢價。代工廠把成熟產能移出類比，使擁有自有產能的環節多拿；但封測機台與外包封測供應商的議價力同步上升。"},{"item":"社會容忍度","level":"🟡","text":"部分料號漲價最高 85%，且年內第三次漲價。中國官方以原產地規則與關稅回應美系晶片，政策上限可能低於經濟上限。"}],"roiic":"峰對峰尚未轉正。2022 年營業利益約 104 億美元，2025 年約 61 億，期間投入逾 200 億美元擴產；2026 年 Q3 單季營業利益 29 億（47%），稼動回升後增量報酬才開始兌現。前瞻報酬取決於在既有潔淨室加裝機台，邊際報酬高於過去六年。","reinvest_rate":"毛再投資率約 26%（TTM 資本支出 26 億美元÷營運現金流 99 億美元）。折舊事實表未涵蓋，淨再投資率無法計算。另有矽實驗室收購 75 億美元，屬一次性。","endo_ceiling":6.2,"formula_note":"內生成長率＝增量報酬×再投資率，兩項輸入都不完整，改用峰對峰 EPS 年增率代理：2022 年 9.41 美元到 2028 年共識 13.52 美元，六年年化約 6.2%。投入資本事實表未涵蓋，當期報酬率無法計算。"}}}},"q3_growth":{"verdict":"五年後成長空間寬（🟢）。資料中心與工業內容增加是有來源的第二曲線；但未來三年的 EPS 高成長大多來自週期利潤率回升，不是內生成長。","reasoning":"成長來源以量為主，2026 下半年起價格加入，2027 上半年起加上矽實驗室併購，回購貢獻近零。共識 EPS：2025 年實際 5.45 美元，2026 年 8.44、2027 年 10.65、2028 年 13.52，三年年化約 35%。內生上限約 6.2%（峰對峰），差距約 29 個百分點，可歸因於三項：稼動率與折舊槓桿帶動的利潤率回升（毛利率 57% 到 64%）、2026 下半年起的漲價、2027 年起併購。不屬無法歸因。共識營收 2026 年約 220 億、2027 年約 252 億，年增約 15%；EPS 成長遠快於營收，正是週期槓桿。滲透率資料事實表未涵蓋，無法換算成長年數。五年後空間判寬的依據：資料中心可觸及市場由 75 億升至 125 億美元，TI 出貨料號每季增加；800V 高壓供電 2027 年放量；人形機器人每台 TI 內容 500–1000 美元（2026-10-21 Haviv Ilan，屬管理層說法、未證）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔（2026 下半年起），2027 年起加上併購；淨回購近零。","runway_years":"事實表未涵蓋滲透率資料","runway_post_y5":"🟢","endo_ceiling_basis":"峰對峰 EPS 年增約 6.2%（2022 年 9.41 美元到 2028 年共識 13.52 美元），毛再投資率約 26%。共識三年年化約 35%，超出部分歸因於利潤率回升、漲價與併購。","segments":[{"item":"類比","value":"2026 年 Q2 43.7 億美元、年增 26%；Q3 年增 32%；供需落差大於嵌入式"},{"item":"嵌入式","value":"2026 年 Q2 7.88 億美元、年增 16%；Q3 年增 21%；週期約落後類比一年，毛利率一年約升 10 個百分點"},{"item":"其他","value":"2026 年 Q3 年減 6%"}],"decay_signals":["亮燈：EPS 成長顯著高於營收成長（2025 到 2027 年 EPS 年化約 40%，營收約 19%），屬週期槓桿","亮燈：自由現金流對淨利 2023 年 0.21、2024 年 0.31、2025 年 0.52，連續低於 0.75，屬擴產期資本支出","未亮：毛利率連兩季年減（Q2、Q3 均上升）","未亮：核心市占近 12 個月縮減（中國替代屬五年期、局部料號）","未亮：提價後銷量下滑（Q3 全終端成長）","未亮：股票薪酬占營收逾 5%（2.32%）","未亮：可觸及市場萎縮","事實表未涵蓋：產業估值倍數三年系統性下移","未亮：維持性資本支出占自由現金流逾六成","未亮：停止投資新產能且營收下滑"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上：股息連升 23 年，股票薪酬稀釋輕；但在高價區幾乎沒有回購，75 億美元現金收購的報酬尚待證明。","reasoning":"自由現金流對淨利：2023 年 0.21、2024 年 0.31、2025 年 0.52，擴產期轉換率偏低。TTM 自由現金流 84 億美元（2025 年 Q3 為 24 億），其中含 CHIPS 補助 16 億；不含補助約 68 億，除以 9.13 億股，每股約 7.45 美元。現金去向（TTM）：資本支出 26 億；回饋股東 58 億，以股息為主（Q3 單季股息 13 億，9 月起季配升 7% 至 1.52 美元）；Q3 還債 5 億；收購尚未付款，2027 上半年將付出 75 億。期末現金 81 億、負債 136.5 億，加權票息 4.11%。股票薪酬單季 1.27 億美元，占營收 2.32%、占營業利益 5.5%。逐項計分：已實現併購報酬不適用（矽實驗室未完成）；回購收益率未過（現價自由現金流收益率約 3.2%，含補助）；淨稀釋過（股票薪酬年化約市值 0.2%）。","fact_refs":["f_kpi2_fcf_chips_act","f_kpi3_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"矽實驗室收購預計 2027 上半年完成，尚無已實現報酬；2011 年 National Semiconductor 的報酬事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"現價自由現金流收益率約 3.2%（TTM 84 億÷市值約 2600 億，含補助），盈餘收益率約 2.3%（本益比 43 倍）。10 年期公債殖利率事實表未涵蓋，但除非低於 1.2%，否則不可能通過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"股票薪酬單季 1.27 億美元，年化約 5 億，約市值 0.2%，遠低於每年 1.5% 的上限；歷年股數事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要靠自有產能與終端需求，不靠併購撐；矽實驗室約市值 3%，在情境樹與風險中處理，不另展開。"}}}},"q5_valuation":{"verdict":"現價要求 2027–2028 年的週期高點盈餘（10.65、13.52 美元）兌現，而且之後倍數不能跌破 23 倍；我只信前半段。現價偏貴，持有可以，不追。","reasoning":"現價 284.65 美元，對 2026 年共識 EPS 為 33.7 倍、對 2027 年為 26.7 倍、對 2028 年為 21.1 倍；落後本益比 43.3 倍，P/S 13.4 倍，都在過去四個年度端點的最高。2026 年共識三個月上修 8.2%，最近兩次快照 2027 年持平、2028 年上修 4%。基準情境：五年後 EPS 15 美元、23 倍，對應 345 美元，五年漲 21%，加股息約 2%，年化約 6%，未達 8%。賣方平均目標價約 320 美元（7 月下旬資料，可能過時），最高 400、最低 225，差距 1.8 倍；大摩維持減碼。26 週漲 21.7%，RSI 55.8，不過熱；週線均線排列已過，但 250 週均線斜率僅 1.1%。類比同業的倍數事實表未涵蓋，無法做同層對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2027 年共識），加上五年情境報酬","peers":{"expanded":false,"reason":"事實表同業為電源設備廠，與類比晶片不同層級，不能當倍數錨；類比同業倍數事實表未涵蓋。"},"fwd_pe":33.73,"peg":0.95,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"2027 年共識本益比 26.7 倍，高於基準終端 23 倍與悲觀 19 倍；基準五年年化約 6%（含股息），低於 8%，判為偏貴。五年分位事實表未涵蓋，只有四個年度端點，現值位於最高；但端點盈餘為谷底，參考性低。","upside_short_pct":0.5,"upside_mid_pct":21.2,"denominator_disputed":true,"denominator_note":"2025 年 EPS 5.45 美元是擴產折舊高峰加週期谷底。以它為基期，三年 EPS 年化 35%，讓 PEG 看似 0.95。改看 2027 年前瞻本益比 26.7 倍對 2027 到 2028 年增約 27%，PEG 約 1.0，談不上便宜。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把週期高點當成結構成長。若 2027 年趕料退潮，EPS 回到 7–8 美元、倍數收到 19 倍，股價約跌 35% 到 50%。","reasoning":"悲觀路徑的依據與裁定見反證紀錄。數字錨：52 週均線 238 美元（−16%），250 週均線 179.8 美元（−37%）；悲觀谷底 EPS 7.6×19 倍約 144 美元（−49%）。存貨天數 194 天仍屬高檔。衰退訊號兩項亮燈，都可由擴產與週期槓桿解釋，判中度陷阱風險。","fact_refs":["f_ma_w52","f_ma_w250","f_price_at_dd","f_kpi5_inventory_days"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點被誤當成結構成長"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.44,"pe":33.73,"basis":"2026 年共識 EPS 8.44 美元（Koyfin 2026-10-21）對現價 284.65；終端倍數同為前瞻一年口徑。"},"eps":{"bull":[11.8,14.8,16.2,17.6,19.2],"base":[11.0,13.0,12.2,13.6,15.0],"bear":[9.6,7.6,7.9,8.9,9.9]},"pe":{"bull":27,"base":23,"bear":19},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-50,"hi":-32,"basis":"悲觀谷底年（2028）EPS 7.6 美元×19 倍＝144 美元，約 −49%；250 週均線 179.8 美元，約 −37%。週期回落疊加倍數由前瞻 33.7 倍收斂，取 −32% 到 −50%。","trigger_time":null},"basis":{"bull":"漲價在 2027 年全面落地，資料中心維持倍增，工業續創新高，2028 年超越共識；週期延長到 2029 年才小幅回落；倍數維持 27 倍。","base":"2027 年略高於共識（Q4 指引 EPS 中值已與 Q3 相同，再加漲價），2028 年略低於共識；2029 年溫和下行週期，之後恢復；矽實驗室利息與攤銷壓低 GAAP EPS；倍數收斂到 23 倍。","bear":"趕料與重複下單在 2027 下半年退潮，2028 年 EPS 回落約兩成到 7.6 美元，同時漲價回吐、中國替代加速；倍數收到 19 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026 年 4 月示警：任何景氣轉弱都可能再觸發去庫存。本季交期拉長，車用客戶湊料困難，工業已創新高。","assumption":"本輪需求是終端真實需求，不是趕料重複下單。","consequence":"2027 下半年起訂單退潮，2028 年 EPS 回到約 7.6 美元，倍數收到 19 倍，股價約 144 美元（−49%）。","ruling":"部分採納：客戶端未見庫存堆積（CEO 稱車用客戶庫存反而偏低），存貨天數 194 天，尚非頂部；但重複下單風險真實存在，悲觀機率給 30%。","watch":"Q1 營收指引中值的季變化、存貨天數、交期","evidence_refs":["customer_concentration_credit#3"]},{"view":"論點失敗","evidence":"中國約占營收兩成。本土類比廠五年來在通訊與消費性中低階料號侵蝕外資份額；TI 漲價後，分析師示警替代加速。中國以晶圓廠所在地認定原產地，使美國自製晶片承擔關稅；通用類比出貨量成長快於營收，表示價格受壓。","assumption":"中國客戶的高內容車用與工業設計不會被替代。","consequence":"中國營收占比跌破 15%，高固定成本工廠稼動下滑，增量毛利反向流失。","ruling":"採納為唯一致命點，12–24 個月機率約 15%。第三方資料顯示 TI 在中國仍取得淨份額，管理層也稱中國車用是成長主力，故不再提高悲觀機率。","watch":"年報地區營收、法說會中國評論、中國官方對美系晶片的措施","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","geo_supply_chain#1","reg_tariff_export#0","end_markets#3"]},{"view":"論點成功但股東經濟變差","evidence":"六年逾 200 億美元擴產後，2025 年營業利益約 61 億，仍低於 2022 年約 104 億。CHIPS 補助占 TTM 自由現金流約兩成且將遞減。矽實驗室 75 億美元現金收購將吃掉近一年自由現金流，中國監管總局至 6 月仍未受理。中國關稅規則又讓自製模式相對委外同業吃虧。","assumption":"營收回升自然帶來每股自由現金流複利。","consequence":"營收超越前高，但每股自由現金流只是回到 2022 年水準；增量投資報酬偏低，配息之外無力回購。","ruling":"部分採納：峰對峰 EPS 年增約 6% 定為本次內生上限，基準情境第六年起只給 7%。","watch":"2027 年不含補助的每股自由現金流、2027 年 2 月資本支出指引、併購核准進度","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#1"]},{"view":"價格已反映太多","evidence":"2027 年共識本益比 26.7 倍；落後本益比、P/S、EV/S 都在過去四個年度端點的最高；26 週漲 21.7%；2026 年共識三個月上修 8.2%。","assumption":"市場沒有把 2027–2028 年的週期高點盈餘當成常態。","consequence":"共識一旦停止上修，倍數就會回落，股價可能橫盤兩年。","ruling":"採納：基準五年年化約 6%，持有不追，等 245 美元以下再加碼。","watch":"2027 年 1 月財報後的共識 EPS 變化","evidence_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 258.44 → 本次 284.65（+10.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=258.44","side_b":"本次 price_at_dd=284.65","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 258.44 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 258.44 美元：Bull 價 546、Bear 價 208，五年期望值 +44.7%，基準年化 8.5%，不對稱比 4.8","side_b":"本次情境、股價仍用 258.44 美元：Bull 價 518.4、Bear 價 188.1，五年期望值 +32.1%，基準年化 5.9%，不對稱比 3.08","ruling":"先換情境、股價不動：五年期望值少 12.6 個百分點，基準年化少 2.6 個百分點。不對稱比由 4.8 變為 3.08。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 258.44 美元：五年期望值 +32.1%，基準年化 5.9%，不對稱比 3.08","side_b":"本次情境、股價 284.65 美元：五年期望值 +19.9%，基準年化 3.9%，不對稱比 2.02","ruling":"再換股價、情境不動：起點價上漲 10.1%，五年期望值少 12.2 個百分點，基準年化少 2.0 個百分點，不對稱比由 3.08 降到 2.02。合計五年期望值比前份少 24.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與加碼意願","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-09-07，股價 258.44）：估值中性，加碼帶 230–245 美元，綜合評級偏高。","side_b":"本次股價 284.65（+10%），2027 年共識本益比約 26.7 倍，基準五年年化約 6%（含股息），低於 8%。","ruling":"估值結論由中性轉為偏貴，綜合評級降一級。基本面變強（2026 年共識三個月上修 8.2%）只抵掉部分漲幅。持有不追，不加碼。","evidence_level":"事實表＋最新一季逐字稿","settle_metric":"2027 年 1 月財報後，2027 年共識 EPS 是否上修到使本益比不高於 23 倍","if_then":["若股價不高於 245 美元且 Q1 指引不低於季節性，則加碼回原目標權重","若 2027 年共識本益比超過 32 倍，則減碼三分之一"],"evidence_refs":[]},{"axis":"陷阱風險、回撤區間與機率","cause":"方法變動","prior_field":["trap","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：陷阱風險低，最大回撤單點約 −45%，樂觀 25%、悲觀 30%。","side_b":"本次逐條清點十類衰退訊號，兩項亮燈（EPS 成長高於營收逾 5 個百分點；自由現金流對淨利 2023–2025 年皆低於 0.75），判中度。回撤改用區間 −32% 到 −50%（悲觀谷底 EPS 7.6 美元×19 倍）；機率維持 25、45、30。","ruling":"兩項亮燈都來自擴產折舊與週期槓桿，可以解釋，不升為高風險；但也不再標低風險。","evidence_level":"事實表年度財報","settle_metric":"2026 年全年自由現金流對淨利是否回到 0.75 以上","if_then":["若 2026 年自由現金流對淨利不低於 0.75，則下次撤銷該項亮燈","若 2027 年營收成長低於 5% 而 EPS 仍要求兩位數成長，則陷阱風險升為高"],"evidence_refs":[]},{"axis":"護城河方向、五年後成長空間、公司屬性、週期位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河擴大，五年後成長空間寬，屬品質複利成長，處於中循環。","side_b":"Q3 毛利率 64%，工業首度回到 2022 年高點，資料中心年增約 95%、占營收約 13%，類比下半年開始漲價且客戶接受；但份額增加，管理層自承無法量測。","ruling":"四欄維持不變，新證據支持原判斷。週期仍判中段，理由見週期位置裁決。","evidence_level":"最新一季逐字稿","settle_metric":"2027 年資料中心與工業年增率、毛利率","if_then":["若資料中心年增連兩季低於 30%，則五年後成長空間降為中"],"evidence_refs":[]},{"axis":"行動門檻（加碼、減碼、清倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8","side_b":"加碼＝股價不高於 245 美元（2027 年共識本益比約 23 倍）且 2027 年 1 月 Q1 指引不低於季節性；減碼＝2027 年共識本益比超過 32 倍，或工業營收年增連兩季轉負；清倉＝單季毛利率連兩季低於 58%，且 2027 年不含補助的每股自由現金流低於 7 美元。","ruling":"加碼價位維持 245 美元。條件由 Q3 指引改為一月指引，因為 Q3 已兌現：營收 61 億落在指引上半，EPS 2.62 高於區間。清倉的毛利率條件由連四季縮為連兩季：Q3 為 64%，要跌到 58% 需要大幅反轉，觀察期太長會反應過慢。每股自由現金流門檻由 8 美元改為不含 CHIPS 補助的 7 美元，因為補助將遞減，舊門檻含補助會高估。","evidence_level":"最新一季逐字稿＋事實表","settle_metric":"2027 年 1 月財報","if_then":["若觸發清倉兩條件，則全數出清","若只觸發其中一條，則減碼一半"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點","side_b":"中國以政策手段（原產地認定加懲罰性關稅、禁採或審查）實質排除美系自製類比晶片，使中國營收占比跌破 15%。","ruling":"前份沒有這一欄，本次補設。中國約兩成營收，一旦失去，加上高固定成本工廠的稼動率反向槓桿，是單一事件中對 EPS 敏感度最大的一項。","evidence_level":"事實表發現","settle_metric":"年報中國營收占比、中國官方公告","if_then":["若出現禁採或懲罰性關稅，則減碼一半並暫停加碼"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"axis":"清倉指標（kill 指標）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標","side_b":"單季毛利率連兩季低於 58%；中國營收占比低於 15%；2027 年不含補助的每股自由現金流低於 7 美元；工業營收年增連兩季轉負。","ruling":"前份沒有這一欄，本次補設。任一條觸發即減碼；毛利率與自由現金流同時觸發即清倉。","evidence_level":"判斷設定","settle_metric":"季報與年報","if_then":["若任一條觸發，則減碼三分之一"],"evidence_refs":[]},{"axis":"週期位置：管理層說還早，市場出現晚期跡象","cause":null,"prior_field":null,"side_a":"管理層（2026-10-21 Haviv Ilan）：週期比疫情時期更早，不宜與當時相比；工業部分子領域尚未回到前高；可以每季擴產。","side_b":"晚期跡象：部分料號漲價最高 85%，且年內第三次漲價；交期拉長；車用客戶湊料困難；工業已創新高；Q4 指引幾乎持平，遠強於季節性。","ruling":"⚖ 不可調和，選中段。依據：工業剛回到 2022 年高點；存貨天數 194 天仍高；客戶端未見庫存堆積，所以尚非頂部。但價格與交期訊號已經出現，不再按早期週期給倍數。現在就賣的最強論證：近 27 倍的 2027 年本益比是建立在週期中後段的盈餘上，一旦重複下單退潮，EPS 與倍數會同時下修，回到 250 週均線約 −37%。現在就買的最強論證：Q4 EPS 指引中值 2.62 美元已與 Q3 持平，2027 年漲價還沒進共識，2027 年共識 10.65 美元可能偏低。","evidence_level":"最新一季逐字稿＋事實表","settle_metric":"2027 年 1 月 Q1 營收指引與存貨天數","if_then":["若 Q1 指引中值季減不超過 5% 且 2027 年漲價落地，則維持中段判斷，並在 245 美元以下加碼","若 Q1 指引中值季減超過 8% 或存貨天數升破 210 天，則改判晚期並減碼三分之一"],"evidence_refs":["customer_concentration_credit#3"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-07-22（Haviv Ilan）：潔淨室與產能足以支應未來約三年；Q3 成長絕大部分來自出貨量，漲價貢獻幾乎不顯著。當時由財務長 Rafael Lizardi 主講，Julie Knecht 給出增量毛利 70–85% 的建模參考。","side_b":"2026-10-21：封測機台交期拉長，外包封測拿不到足量，改為加速馬來西亞自有廠；Q3 毛利率提升有一部分來自價格；財務長改由 Julie Knecht 擔任，長期增量毛利模型改為 75–85%。","ruling":"可調和。產能說法指的是潔淨室，並未改口，新增的是機台與封測瓶頸。價格貢獻由「幾乎沒有」變成「有一些」，屬於實際兌現。Q3 營收與 EPS 都落在或超過前季指引。財務長交接是預告式的，未見財測失準，列入觀察，不扣分。","evidence_level":"逐字稿","settle_metric":"2027 年 2 月資本管理會的資本支出與產能計畫","if_then":["若 2027 年資本支出指引高於成長率 1.2 倍的框架，則下調每股自由現金流路徑並重算情境"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 1 月財報：Q4 毛利率、Q1 指引、2027 年漲價結果","type":"假設驗證","maps_to":"H2","metric":"單季毛利率；Q1 營收指引中值的季變化","threshold":"毛利率不低於 62%；指引中值季減不超過 5%","action":"達標續抱；未達標停止加碼","source_freq":"季報","date":"2027-01","evidence_refs":[]},{"n":2,"text":"中國以政策手段排除美系自製類比晶片","type":"Single Thing","maps_to":"Single Thing","metric":"中國客戶營收占比；中國官方對美系晶片的措施","threshold":"占比低於 15%，或出現禁採、懲罰性關稅","action":"減碼一半並暫停加碼","source_freq":"年報、即時公告","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"n":3,"text":"股價回到約 245 美元，且一月指引不低於季節性","type":"估值rearm","maps_to":"估值","metric":"股價、2027 年共識本益比","threshold":"不高於 245 美元（約 23 倍）","action":"加碼回原目標權重","source_freq":"每日","date":null,"evidence_refs":[]},{"n":4,"text":"估值過高或工業轉負","type":"減碼","maps_to":"H2","metric":"2027 年共識本益比；工業營收年增率","threshold":"本益比超過 32 倍（約 340 美元），或工業年增連兩季轉負","action":"減碼三分之一","source_freq":"每日、季報","date":null,"evidence_refs":[]},{"n":5,"text":"毛利率崩落且自由現金流未重建","type":"清倉","maps_to":"H1","metric":"單季毛利率；2027 年不含補助的每股自由現金流","threshold":"毛利率連兩季低於 58%，且每股自由現金流低於 7 美元","action":"清倉","source_freq":"季報、年報","date":"2028-01","evidence_refs":[]},{"n":6,"text":"矽實驗室併購的中國監管進度","type":"風險","maps_to":"R4","metric":"中國監管總局受理與核准","threshold":"2027 年 6 月底前未核准","action":"停止加碼，重估資本配置","source_freq":"公司公告","date":"2027-06","evidence_refs":["regulatory_antitrust#2"]},{"n":7,"text":"重複下單退潮、去庫存再起","type":"風險","maps_to":"R2","metric":"存貨天數；營收季變化","threshold":"存貨天數超過 210 天，且營收季減","action":"減碼三分之一","source_freq":"季報","date":null,"evidence_refs":["customer_concentration_credit#3"]},{"n":8,"text":"中國本土替代加速","type":"風險","maps_to":"R1","metric":"中國客戶營收占比","threshold":"低於 17%，或連四季合計下滑 3 個百分點以上","action":"停止加碼","source_freq":"年報","date":null,"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","end_markets#3"]},{"n":9,"text":"資本管理說明會：2027 年資本支出與產能","type":"複審日期","maps_to":"H1","metric":"2027 年資本支出指引","threshold":"高於成長率 1.2 倍框架即重算","action":"複審情境","source_freq":"年度","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"單季毛利率（GAAP）","bear_threshold":"連兩季低於 58%","window":"2027 Q1 至 2028 Q4","source":"TI 季報","last_status":"ok"},{"metric":"中國客戶營收占比","bear_threshold":"低於 15%","window":"2026 至 2028 年報","source":"TI 年報地區揭露","last_status":"unknown"},{"metric":"不含 CHIPS 補助的每股自由現金流","bear_threshold":"2027 年低於 7 美元","window":"2027 年度","source":"TI 年報、2027 年 2 月資本管理會","last_status":"unknown"},{"metric":"工業終端營收年增率","bear_threshold":"連兩季轉負","window":"滾動四季","source":"法說會終端市場評論","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價不高於 245 美元（2027 年共識本益比約 23 倍），且 2027 年 1 月 Q1 指引不低於季節性","exec_line":"持有不追；回到 245 美元以下且一月指引不弱才加碼；觸發減碼或清倉條件時依觸發器執行。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價回到 245 美元以下（2027 年共識本益比約 23 倍）；或等 2027 年 1 月財報後共識上修，使現價對 2027 年 EPS 的本益比降到 23 倍以下。","prior_verdict":"進場","prior_role":"核心","qc48_result":"pass","qc48_note":"TXN 的 Bull 情境缺少「量 × 價」的營收推導，歷史類比也沒有查到可比案例；資料中心第二曲線有部分公開佐證，但 TAM 與人形機器人內容量缺具名來源，所以依據目前站不穩，還沒到被推翻的程度。"},"thesis":{"H":[{"id":"H1","text":"擴產結束、資本支出降到 20–30 億美元後，自由現金流重建，長期以每股自由現金流年增約一成為主軸。","2y":"2027 年不含補助的每股自由現金流不低於 8 美元","5y":"2030 年不含補助的每股自由現金流不低於 11 美元，自由現金流利潤率不低於 30%","10y":null,"threshold":"2027 年不含補助的每股自由現金流低於 8 美元削弱、低於 7 美元反轉","source":"年報、2027 年 2 月資本管理說明會","drift_rule":"TTM 每股自由現金流連四季偏離軌道 5% 以上削弱，連六季 10% 以上反轉"},{"id":"H2","text":"這一輪是工業、車用、資料中心同時拉動的多年上行週期，不是單季補庫存：毛利率站穩 62% 以上，2027 年營收年增至少一成。","2y":"2027 年單季毛利率維持在 62% 以上；2027 年營收較 2026 年成長不低於 10%（共識約 15%）","5y":null,"10y":null,"threshold":"單季毛利率連兩季低於 60% 削弱、低於 58% 反轉；或工業營收年增連兩季轉負","source":"季報、法說會終端市場評論","drift_rule":"連兩季偏離 5% 以上削弱，連三季 10% 以上反轉"},{"id":"H3","text":"資料中心成為第二曲線：可觸及市場由 75 億升到 125 億美元，TI 以料號廣度與高壓供電新品擴大內容，2026 年 Q3 已占營收約 13%。","2y":"2027 年資料中心營收年增不低於 30%","5y":"2030 年資料中心占營收不低於 18%","10y":"800V 高壓供電世代下，電源轉換與控制晶片份額守在約兩成","threshold":"資料中心營收年增連兩季低於 30% 削弱，連三季低於 15% 反轉","source":"季報、法說會資料中心評論","drift_rule":"連兩季年增低於 30% 削弱，連三季低於 15% 反轉"}],"R":[{"id":"R1","text":"漲價（部分料號最高 85%）加上地緣摩擦，促使中國客戶加速改用本土類比廠，侵蝕中低階料號；中國約占營收兩成，通用類比價格長期受壓。","h_ref":"H2","clock":"🔥","threshold":"年報中國客戶營收占比低於 17%，或連四季合計下滑 3 個百分點以上","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","geo_supply_chain#1","end_markets#3"]},{"id":"R2","text":"客戶趕料與交期拉長造成重複下單，週期在 2027 年提前見頂並再次去化庫存（管理層 2026 年 4 月已示警）。","h_ref":"H2","clock":"⚡","threshold":"下一季營收指引中值季減超過 8%，或存貨天數升破 210 天且營收季減","evidence_refs":["customer_concentration_credit#3"]},{"id":"R3","text":"中國以晶圓廠所在地認定原產地，加上報復性關稅，美國自製的 TI 相對委外代工同業吃虧。該報導的日期標示與股價水位不一致，時間點待查，但規則本身持續有效。","h_ref":"H1","clock":"🐢","threshold":"營收成長下毛利率仍季減超過 200bp，或中國營收占比低於 15%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"矽實驗室併購（約 75 億美元現金）卡在中國監管總局，到 6 月仍未受理；或完成後整合拉低報酬，擠壓配息以外的現金。","h_ref":"H1","clock":"🔥","threshold":"2027 年 6 月底前未完成；或完成後兩年內嵌入式毛利率未改善","evidence_refs":["regulatory_antitrust#2"]},{"id":"R5","text":"嵌入式與微控制器並非份額龍頭（英飛凌 2024 年約 21%），Lehi 廠產能能否換成份額尚未證實。","h_ref":"H2","clock":"🐢","threshold":"嵌入式營收年增連四季落後類比 10 個百分點以上，且毛利率改善停滯","evidence_refs":["end_markets#11"]}],"single_thing":{"description":"中國以政策手段（原產地認定加懲罰性關稅、禁採或審查）實質排除美系自製類比晶片，使 TI 中國營收占比跌破 15%。","why_fatal":"中國約占營收兩成，多為高內容的電動車與工業客戶。失去這塊後，固定成本極高的 300mm 廠稼動率下滑，增量毛利會以 75–85% 的速度反向流失，EPS 敏感度大於任何單一終端市場。","if_happens":"悲觀機率升到約 45%，減碼一半並暫停加碼，直到中國以外營收補足缺口。","how_monitor":"每季法說會中國評論、年報地區營收、中國商務部與半導體行業協會公告、矽實驗室案在監管總局的進度。","probability":"12–24 個月約 15%"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.73,"peg_fy2":0.99,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":5.45,"FY2026E":8.44,"FY2027E":10.65,"FY2028E":13.52},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（TI 不揭露非 GAAP EPS）；共識來自 Koyfin 2026-10-21 快照"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 財報、2027 年 Q1 指引與年度漲價結果","impact":"高","watch":"Q1 營收指引中值的季變化、毛利率、存貨天數"},{"date":"2027-02","date_precision":"month","type":"capacity","event":"資本管理說明會：2027 年資本支出與產能計畫","impact":"中","watch":"資本支出是否超過成長率 1.2 倍的框架"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"矽實驗室併購預定完成期限（需中國監管總局核准）","impact":"中","watch":"監管總局受理與核准進度"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=21.69, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='TXN 的 Bull 情境缺少「量 × 價」的營收推導，歷史類比也沒有查到可比案例；資料中心第二曲線有部分公開佐證，但 TAM 與人形機器人內容量缺具名來源，所以依據目前站不穩，還沒到被推翻的程度。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 245 美元以下（2027 年共識本益比約 23 倍）；或等 2027 年 1 月財報後共識上修，使現價對 2027 年 EPS 的本益比降到 23 倍以下。'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
