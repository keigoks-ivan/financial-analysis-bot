你是 DD 管線 v20 的判斷層閘（gate），標的 ISRG（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝3048.7 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 財報新聞稿（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝41.6 %（營業利益 1,269.7M）｜期間與口徑：Q3 2026（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（公告於 2026-10-20））
  - 註記：未查到
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝19.4 %（營業利益 592.6M）｜期間與口徑：Q3 2026（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1；含 4.5 億美元反托拉斯集體訴訟和解費（SG&A，待法院核准；Q3 訴訟費用合計 454.9M）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（公告於 2026-10-20））
  - 註記：未查到
- `f_kpi3_diluted_eps_gaap_non_gaa`（q1_business）｜Diluted EPS GAAP / Non-GAAP＝3.0 USD（Non-GAAP；GAAP 1.49）｜期間與口徑：Q3 2026（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（公告於 2026-10-20））
  - 註記：未查到
- `f_kpi6_guidance_fy2026`（q1_business）｜Guidance FY2026（全年）＝da Vinci 手術量成長 ~14–15%（偏中點）；Non-GAAP 毛利率 68.7–69.3%（含關稅約 0.9% 營收）；Non-GAAP 營業費用成長 11–13% 區間｜期間與口徑：Q3 2026 公告（2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 8-K Ex.99.1；稅率未提供（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026 公告（2026-10-20））
  - 註記：未查到
- `f_kpi7_da_vinci_installed_base_`（q1_business）｜da Vinci installed base / procedures＝12094 systems（YoY +12%；Q3 手術量約 906,000，+14%；裝機 546 台，其中 da Vinci 5 為 315 台；Ion 裝機 1,152，+21%）｜期間與口徑：2026-09-30（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1（numbers.latest_quarter_kpis.items[7]，as_of 2026-09-30（公告於 2026-10-20））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-20 date｜期間與口徑：2026-10-20／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-20）
- `f_peer_isrg_gross_margin_pct`（q2_moat）｜ISRG 毛利率＝66.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ISRG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_isrg_operating_margin_pct`（q2_moat）｜ISRG 營業利益率＝31.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ISRG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_isrg_fcf_margin_pct`（q2_moat）｜ISRG FCF 利潤率＝29.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ISRG.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mdt_operating_margin_pct`（q2_moat）｜MDT 營業利益率＝19.04 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MDT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mdt_fcf_margin_pct`（q2_moat）｜MDT FCF 利潤率＝16.33 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MDT.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_syk_operating_margin_pct`（q2_moat）｜SYK 營業利益率＝21.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SYK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_syk_fcf_margin_pct`（q2_moat）｜SYK FCF 利潤率＝18.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SYK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bsx_operating_margin_pct`（q2_moat）｜BSX 營業利益率＝21.0 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BSX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bsx_fcf_margin_pct`（q2_moat）｜BSX FCF 利潤率＝8.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BSX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.8 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.12 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝13.67 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.65 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 10.42 → 10.8（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_kpi4_free_cash_flow`（q1_business）｜Free cash flow（前三季累計，非單季）＝2868.0 USD M｜期間與口徑：2026 前九個月（季末 2026-09-30，10-Q）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q isrg-20260930：營運現金流 3,197.0 − 資本支出 329.0；新聞稿與 10-Q 均無單季數（numbers.latest_quarter_kpis.items[4]，as_of 2026 前九個月（季末 2026-09-30，10-Q））
  - 註記：不適用
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC（占營收／占 GAAP 營業利益）＝212.6 USD M（占營收 7.0%；占 GAAP 營業利益 35.9%，被和解費壓低分母；占 Non-GAAP 營業利益 16.7%）｜期間與口徑：Q3 2026（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 調節表；新聞稿文字段落寫 216M，與調節表 212.6M 不一致，本表採調節表（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-10-20））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-6800.4 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 0.0、現金 6800.4（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝353.28 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝428.12 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝39.64 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 10.8，分子＝快照價 428.12｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝51.77 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝144444.99 USD m｜期間與口徑：2026-10-22／市值 151245.39 ＋ 淨負債 -6800.4｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-2.94 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝488.41 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）

### findings_digest 中方向為負或來源衝突的條目（25 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出 Surgerii、CMR、Distalmotion、Medicaroid、Medtronic、J&J、Noah、微創醫療機器人、SS Innovations 等為已推出或明確進入機器人手術的對手，並預期中國競爭加劇；2025 年中國競爭與反貪腐使裝機少於預期
  - 來源：SEC EDGAR 10-K FY2025 Item 1/1A（as_of 2026-02-03）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Q2 2026 財報電話會議：管理層稱中國招標減少、本土機器人競爭增加、政策導向降價壓力
  - 來源：Webull：Intuitive Surgical Q2 2026 Earnings Call Transcript（as_of 2026-07-22）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素揭露：第三方（欲競爭器械或維修市場者）與部分客戶已對公司提出反壟斷訴訟；公司業務受美國與歐盟反壟斷法規範。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：第九巡迴法庭 2026-08 撤銷 SIS 反壟斷案原判（陪審團指示錯誤）並發回地方法院；Intuitive 2026-09-28 聲請全院重審
  - 來源：Bloomberg Tax：Surgical Robot Monopoly Suit Revived Over Jury Instructions（as_of 2026-08-13）｜affects：moat_trend、decision_inputs.bear、triggers
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：Intuitive 向上訴法院聲請全院重審，要求推翻復活 SIS 主張的合議庭判決
  - 來源：MLex：Intuitive Surgical asks US appeals court for rehearing after loss in antitrust case（as_of 2026-09-28）｜affects：moat_trend、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：多數器械與配件在墨西哥 Mexicali 製造，多數符合 USMCA 原產地而至今未被課美國進口關稅；內視鏡多在德國製造且受關稅；自中國進口原料與組件、並將美製 da Vinci Xi 賣入中國，皆受關稅，預期持續不利中國 Xi 系統產品成本。2025 年關稅與其他貿易措施使銷貨成本增加約 6,300 萬美元，預期 2026 年續增。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（Trade and Tariffs Update）（as_of 2026-02-03）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年關稅與其他貿易措施使銷貨成本增加約 6,300 萬美元，並預期 2026 年關稅帶來的銷貨成本續增。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-03）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年中國政府宣布對含中國產稀土的部分產品實施出口管制與許可要求；稀土為公司產品部分零組件的關鍵材料，若實施可能需為部分產品申請出口許可，並可能造成供應中斷。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-03）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：Q2 2026 10-Q 提及臨時 Section 122 附加稅到期後，美國依 Section 301 對 60 個貿易夥伴加徵一般 10% 或 12.5% 關稅。
  - 來源：SEC EDGAR 10-Q Q2 2026（as_of 2026-07-30）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：器械與配件的絕大多數在墨西哥 Mexicali 生產，多數符合 USMCA 原產地而至今未被課美國進口關稅；內視鏡為進口、課關稅，多數在德國製造。
  - 來源：ISRG Form 10-Q (period ended 2026-09-30), SEC EDGAR（as_of 2026-09-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2026 年前九個月計入銷貨成本的關稅與貿易措施為 $72.4M；另認列 IEEPA 關稅退款 $63.7M，後續退款金額仍不確定。
  - 來源：ISRG Form 10-Q (period ended 2026-09-30), SEC EDGAR（as_of 2026-09-30）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因子警告中國對稀土（含磁鐵）與關鍵礦物的出口限制，可能限制多項產品所用零件的取得；2025 年關稅與貿易措施使銷貨成本增加約 $63.0M，預期 2026 年續增。
  - 來源：ISRG Form 10-K FY2025, SEC EDGAR（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：部分組裝零件來自單一或唯一來源供應商，以採購單而非長期供應合約購料，且通常存貨很少（FY2018 10-K 原文，後續年度重複為風險因子）。
  - 來源：ISRG Form 10-K FY2018, SEC EDGAR（as_of 2018-12-31）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Medtronic 的 Hugo 手術機器人於 2025 年 12 月取得 FDA 泌尿科適應症許可，可在美國醫院廣泛行銷。
  - 來源：eWeek｜Medtronic's 'Hugo' Surgical Robot Receives FDA Clearance for Urological Procedures（as_of 2025-12-31）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：J&J Ottava 據稱於 2026 年中獲 FDA 許可十項一般外科術式；Intuitive 2026 年股價大幅回檔（來源為股票分析文章）。
  - 來源：TIKR｜Intuitive Surgical fell 30% in 2026 as a rival arrived（as_of 2026-08-17）｜affects：moat_trend、decision_inputs.bear、valuation
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Intuitive 因競爭與中國標案偏好本土廠商，成長放緩。
  - 來源：Bloomberg｜Intuitive Surgical Falls as Rivalry, Funding Slows Growth（as_of 2026-01-14）｜affects：moat_trend、thesis.R
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Medtronic 已提交 Hugo 一般外科與婦科 510(k)；2026-02-17 Cleveland Clinic 完成美國首例商業 Hugo 手術。
  - 來源：MedTech Dive｜Medtronic completes first Hugo case in the US（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#4`（substitute_technology｜方向 -｜狀態 ok）：第三方再製 Intuitive 器械與 Restore Robotics 反壟斷訴訟威脅高毛利器械與配件業務；Deutsche Bank 2025 年 6 月因此降評。
  - 來源：Motley Fool｜Why Intuitive Surgical stock plunged today（as_of 2025-06-09）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：目標價自上半年下移：Fintel 2026-02-25 平均 $624.51；Barchart（Q1 前）平均 $619.85；Evercore 7 月由 $480 降至 $430；BofA 5 月由 $650 降至 $520；HSBC 7/30 降評 Hold 目標 $931
  - 來源：Barchart；Sell-side 報導彙整（Sahm Capital／SimplyWall.St 搜尋摘要）（as_of 2026-07-30）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：10-K 披露多起產品責任訴訟（da Vinci 設計瑕疵、訓練不足等指控）及 In Re: da Vinci Surgical Robot Antitrust Litigation 集體訴訟（器械維修服務反壟斷），均仍在辯護中。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-03）｜affects：decision_inputs.bear、moat_trend
- `major_events#3`（major_events｜方向 -｜狀態 ok）：FDA 執行報告列 2026 年 da Vinci X/Xi 機械臂螺絲可能斷裂之 Class II 召回（Z-2046-2026，2026-05-01 分類）及病人側推車煞車固定銷 Class II 召回（Z-2521-2026，2026-06-22 公布）；未見 FDA 警告信。
  - 來源：FDA 召回資料庫／MarketScreener 搜尋摘要（as_of 2026-06-22）｜affects：decision_inputs.bear、thesis.R
- `major_events#4`（major_events｜方向 -｜狀態 ok）：2026-02-04 有團體向 FDA 提出公民請願，要求對 da Vinci 5 全系統 Class I 召回、發緊急安全通訊並對 Intuitive 發警告信；此為請求，未見 FDA 回應。
  - 來源：Northeastern Univ. AJRC citizen petition (PDF)（as_of 2026-02-04）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 披露產品責任訴訟與 da Vinci 維修反壟斷集體訴訟（2021 年起），仍在辯護；搜尋未見 2026 年新的證券集體訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-03）｜affects：decision_inputs.bear、moat_trend
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：FDA 列 2026 年 da Vinci X/Xi 機械臂螺絲 Class II 召回（Z-2046-2026）及病人側推車煞車銷 Class II 召回（Z-2521-2026）；未見 FDA 警告信。
  - 來源：FDA 召回資料庫／MarketScreener 搜尋摘要（as_of 2026-06-22）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#1`（product_recall_warning｜方向 -｜狀態 ok）：2026-02-04 公民請願要求 FDA 對 da Vinci 5 Class I 召回並發警告信；為請求，非 FDA 行動。
  - 來源：Northeastern Univ. AJRC citizen petition (PDF)（as_of 2026-02-04）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":792.0,"bear_5y_price":264.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":34.5,"ev5y_pct":25.3,"irr_base_pct":6.1,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.8,"pe":39.64,"basis":"FY2026 共識非 GAAP EPS 10.80 美元，與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[12.6,14.6,16.9,19.4,22.0],"base":[12.0,13.4,14.9,16.4,18.0],"bear":[11.0,11.4,11.7,11.9,12.0]},"pe":{"bull":36,"base":32,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ISRG_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜Daniel Connally (IR)｜guidance：全年 da Vinci 程序量成長財測區間維持 13.5%–15.5%（原話："within a range of 13.5% to 15.5%"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：程序量預期落在區間中點附近（原話："with an expectation to be closer to the midpoint"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：非 GAAP 毛利率財測由 67.5–68.5% 上調至 68–69%（原話："to be within a range of 68% to 69% of revenue"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：前次毛利率財測含關稅約 100 bps 影響（原話："which reflected 100 basis points of impact from tariff"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：非 GAAP 營業費用成長財測 11%–13%（原話："operating expense growth to be between 11% and 13%"）
- 2026-07-16｜Daniel Connally (IR)｜guidance：下半年 Q3 美國基期較高，國際有假期季節移動（原話："bit of a tougher comp in the U.S. in Q3"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 毛利率含 IEEPA 關稅退款 3600 萬美元（原話："Excluding the $36 million benefit from IEEPA tariff refunds"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：扣除退款後 Q2 非 GAAP 毛利率為 68.7%（原話："gross margin would have been 68.7%"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 非 GAAP 營業利益率 42%、EPS 年增 28%（原話："42%, and non-GAAP earnings per share increased 28%"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：R&D 成長刻意高於 SG&A（原話："We are intentionally growing R&D at a higher rate than SG&A"）
- 2026-07-16｜Jamie Samath (CFO)｜margin：Q2 da Vinci I&A 每程序收入約 1,830 美元，去年 1,800（原話："increased to approximately $1,830 compared to $1,800"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：延長使用壽命器械計畫預計 2027 上半年推出（原話："Beginning in the first half of 2027, we plan to introduce"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：延長使用計畫定價與量化影響留待下次財報（原話："we'll provide additional quantification on our next"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：分析師問延長使用影響，管理層表示尚不量化（原話："not ready to quantify it yet"）
- 2026-07-16｜Jamie Samath (CFO)｜commitment：管理層形容延長使用影響為 2027 年逐步發生（原話："think of it as being a progressive"）
- 2026-07-16｜David Rosa (CEO)｜commitment：da Vinci 5 以固定節奏持續推更新（原話："this cadence that we've committed to"）
- 2026-07-16｜Daniel Connally (IR)｜commitment：2026 年不再對基金會捐款（Q4 2025 曾捐 7000 萬）（原話："made a $70 million multiyear contribution to the"）
- 2026-07-16｜David Rosa (CEO)｜product：Q2 推出 100 項計畫更新的第一階段（原話："100 planned updates to the da Vinci 5 platform"）
- 2026-07-16｜David Rosa (CEO)｜product：SP 程序量成長 61%（原話："SP procedures grew 61%"）
- 2026-07-16｜Jamie Samath (CFO)｜product：SP 吻合器在美國適用病例使用率近 60%（原話："it was used in nearly 60% of eligible cases"）
- 2026-07-16｜David Rosa (CEO)｜product：向 FDA 遞交 GI 軟式機器人內視鏡 510(k)（非商用）（原話："not ready today to describe kind of timing"）
- 2026-07-16｜David Rosa (CEO)｜product：GI 機器人時程與市場規模尚不揭露（原話："not ready today to describe kind of timing or size"）
- 2026-07-16｜David Rosa (CEO)｜product：Ion 程序量成長 36%（原話："Ion procedures increased 36% to 48,000"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：XiR 安裝基數約 130 台（原話："the installed base is something like 130 XiRs in the field"）
- 2026-07-16｜David Rosa (CEO)｜customer：CEO 預期 XiR 將成為未來數季裝機的重要部分（原話："the installed base is something like 130 XiRs"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：首批 My Intuitive+ 續約客戶無人退出（原話："customer chose to opt out of their MI+ arrangement"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：海外良性程序占國際業務略逾 25%（原話："just over 25% of our international business"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：ACA 補貼到期對美國 da Vinci 程序量有輕微不利影響（原話："modest adverse impact to Q2 U.S. da Vinci procedure growth"）
- 2026-07-16｜David Rosa (CEO)｜risk：美國成長較年初預期放緩，集中在可延後程序（原話："Growth in the U.S. moderated from recent trends"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：CFO 稱部分放緩源自基期變大（原話："a little bit of the law of large numbers"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：減重手術受 GLP-1 影響持續下滑（原話："Growth in the U.S. moderated from recent trends"）
- 2026-07-16｜Daniel Connally (IR)｜risk：財測區間納入中國招標量與競爭強度（原話："China tender volumes and competitive intensity"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：管理層對日本新給付態度為平衡（原話："we're balanced about the continuing financial challenges"）
- 2026-07-16｜Jamie Samath (CFO)｜risk：暴露於交易所／Medicaid 的程序占比無精確估計（原話："We don't have a precise estimate"）
- 2026-07-16｜David Rosa (CEO)｜competition：中國環境持續具挑戰性（原話："the environment remains challenging"）
- 2026-07-16｜David Rosa (CEO)｜competition：中國本土機器人競爭與政策性價格壓力（原話："domestic robotic competition and policy-driven pricing"）
- 2026-07-16｜Jamie Samath (CFO)｜competition：Q2 中國僅裝 2 台，含香港首台 da Vinci 5（原話："placing 2 systems, including our first da Vinci 5"）
- 2026-07-16｜Jamie Samath (CFO)｜competition：經銷商市場相對強勢（原話："relative strength in distributor markets"）
- 2026-07-16｜David Rosa (CEO)｜competition：管理層不認為中國集中招標等同 VBP（原話："I wouldn't compare this tender centralization"）
- 2026-07-16｜David Rosa (CEO)｜competition：器械加密技術被問及是否抵擋再製器械，答以網路安全（原話："cybersecurity is front and center"）
- 2026-07-16｜Jamie Samath (CFO)｜capital_allocation：Q2 回購 3.79 億美元，均價 439 美元（原話："stock repurchases of $379 million at an average price"）
- 2026-07-16｜Jamie Samath (CFO)｜capital_allocation：2026 上半年自由現金流 18 億美元，年增 71%（原話："Free cash flow in the first half of 2026 was $1.8 billion"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國資本環境穩定（原話："The U.S. capital environment, at least in our experience"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國約 70% 系統採租賃（原話："70-ish percent of the systems acquired in the U.S."）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國裝機增量幾乎全來自換機（原話："the entirety of that increase is in trades"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：美國約半數裝機為換機（原話："half of the placements in the U.S. in Q2 were trades"）
- 2026-07-16｜Jamie Samath (CFO)｜customer：以 Si→Xi 歷史類比 dV5 換機週期（原話："it took about 7 years before we got to the peak"）

### 問答異常語氣（迴避／改口／保留）
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Travis Steed／Michael Polark：延長使用計畫對 I&A 每程序收入的量化影響（約 5 點？2027 持平或下降？）｜答法：兩次皆不給數字，僅稱下次財測會量化、需先走完內部分析；改談成長與獲利平衡及 mix 抵銷
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Larry Biegelsen：器械加密是否促使醫院不改用再製器械｜答法：未正面回答再製器械問題，改談網路安全與產品品質、可用性
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Vijay Kumar：程序對交易所與 Medicaid 的暴露程度｜答法：先請對方重述問題，後答無精確估計，只說商保占大部分
- ISRG_Q2_2026_Earnings_Call_20260716.md｜問：Rick Wise：GI 機器人的時機與潛在 TAM｜答法：稱仍早期，不給時程與市場規模

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 5 | 1 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 2 | 2 |
| substitute_technology | found | 5 | 3 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 6 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：Intuitive Surgical largest customer concentration hospitals 10-K 2025 no single customer

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260717","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"裝機基數 ＋ ~85% 經常性耗材年金鎖住 83-85% 軟組織份額，且年金的單位經濟不被侵蝕前次僅要求份額；本次因 EUP 與售後市場訴訟同現，加入單位經濟這一半——份額守住但每台收入被砍，H1 一樣不成立"},{"id":"H2","text":"Ion／SP／心臟／NSM／國際 benign／ASC 通路接棒，維持整體雙位數手術量成長"},{"id":"H3","text":"市場願給高成長醫材上緣的倍數溢價。本次重寫：前次「長期 Fwd PE 38-48x」已被市場實付 34.45x(FY26)／30.47x(FY27) 直接否決（§12 矛盾 #1）。重寫後 ＝ 28-34x（Fwd FY2 口徑，相對高成長醫材同業 ~28x 約 0-20% 溢價）——不是回到 38-48x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EUP ＋ XiR／翻新機低價組合 ＋ GLP-1，三者同向侵蝕 I&amp;A 每台手術收入。EUP 於 2027 上半年上線、量級管理層兩次拒答（BofA 估 ~5pt、Wolfe 援引 2020 先例 ~7pt）；XiR（裝機 ~130 台）與翻新 Xi／X（Q2 共 122 台 vs 去年 59 台）把組合往低單價拉；美國 bariatric 因 GLP-1 高個位數下滑、膽囊切除等低單價術式佔比上升"},{"id":"R2","text":"手術量結構性降檔 ＋ 政策給付逆風，倍數向成熟醫材 22-26x 收斂。美國 da Vinci 自 Q1 +14% 降至 Q2 +12%；上半年 ~15% → 全年「靠近中點」14.5% → 下半年隱含 ~14%；管理層自承「大數法則」。疊加政策：ACA 增強版補貼已於 2026-01-01 到期且未見續延，非單季雜訊而是延續至 2026-27 的結構性逆風，且與 GLP-1 對 bariatric 的衝擊同方向疊加"},{"id":"R3","text":"EndoWrist 售後市場的法律可分割性 ＋ 競品在新興市場的價格戰。① 醫院買方反壟斷集體訴訟已於 2025-03-31 獲裁准 class certification，核心指控＝以程式化使用次數限制強迫回購 EndoWrist、禁止第三方維修；SIS v. Intuitive 一案 ISRG 雖於 2025-01-28 獲法官於陪審團審判中途作出有利之 JMOL（援引 Epic v. Apple 第九巡迴 2023 先例，認未能證明售後市場存在），但現上訴於第九巡迴（Open Markets Institute 已提 amicus）；法院曾於較早之即決判決認定 da Vinci 機器與 EndoWrist 為獨立產品市場且 ISRG 於售後市場具獨占力，惟已於 2024-07-30 准重新審議而撤銷——此爭點法院曾兩度改變見解，屬真正未定。② MicroPort Toumai 累計 300+ 全球訂單、覆蓋 60+ 國家（印度 30+ 台、巴西／阿根廷各近 20 台），定價約低 30%，主攻的正是 H2 所倚賴的國際低滲透市場"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","irr_base_pct":10.8,"ev5y_pct":47.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"❌","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.5,"ev5y_pct":47.9,"irr_base_pct":10.8,"max_dd_pct":-45.0,"bull_5y_price":770.0,"bear_5y_price":280.0,"p_bull_pct":22.0,"p_bear_pct":33.0,"rearm_trigger":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","price_at_dd":358.97,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ISRG","date":"2026-10-22","schema":"v15.0","contract":"v19","company_name":"Intuitive Surgical"},"oneliner":"達文西裝機帶動耗材與服務年金，第三季營收增 22%、手術量增 14%；但公司已宣布 2027 年器械降價 3–5%，美國手術量增速降到 10%，競品陸續拿到美國許可。前瞻本益比近 40 倍只對應年增約 12% 的盈餘，等股價回到 350 美元附近再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/scenario.json","answers":{"q1_business":{"verdict":"賣系統、收耗材年金：84% 經常性收入，錢卡在每台手術的器械單價","reasoning":"錢從醫院來：先賣或租出系統，之後每台手術買器械與配件、每年付服務費。第三季營收 30.49 億美元、年增 22%，其中 84% 是經常性收入；器械配件 18 億美元（年增 18%，約占 59%）、系統 7.69 億美元（年增 30%）、服務 4.82 億美元（年增 22%），分部數字取自 2026-10-20 法說 CFO 發言。非 GAAP 營業利益率 41.6%，GAAP 只有 19.4%，差額主要是 4.5 億美元反托拉斯集體訴訟和解費（待法院核准）。錢卡在每台手術的器械單價：達文西器械配件每台手術約 1,860 美元（去年 1,800 美元），公司已宣布延長使用計畫加中國政策降價，組合不變下每台手術收入降 3–5%，2027 年逐季累積。單點依賴：沒有單一大客戶，美國占營收 68%（FY2025 10-K）；真正的單點是器械售後市場的封閉性，也正是反壟斷訴訟攻擊的位置。產業處於擴張期：第三季全球裝機 546 台年增 28%、裝機基數 12,094 台年增 12%。供需耐久性：結構性持久，手術量由微創滲透驅動（海外良性手術年增 41%），不是庫存週期；但美國增速已由第二季 12% 降至 10%。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_diluted_eps_gaap_non_gaa","f_kpi6_guidance_fy2026","f_kpi7_da_vinci_installed_base_","f_earnings_recency"],"verdict_values":{"revenue_quality":"經常性收入占 84%（器械配件、服務、系統租賃），裝機基數 12,094 台年增 12%，收入隨手術量累積","unit_econ_note":"每台達文西手術器械配件收入約 1,860 美元（去年 1,800 美元）；延長使用計畫加中國降價在組合不變下拉低 3–5%，2027 年逐季生效","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"裝機帶耗材年金、毛利率約 69%、零負債、經常性收入 84%"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：手術量由微創滲透與新適應症驅動（海外良性手術年增 41%、SP 年增 55%），不是庫存或資本支出週期；美國增速放緩至 10% 是降溫訊號","bargaining":{"up":"上游議價弱但金額小：部分零件單一來源、以採購單購料，稀土依賴中國","down":"下游醫院裝機後耗材鎖定，議價權在公司；例外是中國集中招標與成本敏感的 ASC 客群","geo":"美國占營收 68%；中國政策壓價；器械在墨西哥生產依賴 USMCA 免稅"},"profit_pool_dir":"利潤池仍集中在公司的器械配件環節，公司主動讓出 3–5% 單價換滲透，中國由政策強制讓利","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；管理層稱 2027 年 1 月更新軟組織長期機會估計，屆時再展開"}}}},"q2_moat":{"verdict":"→ 持平：執行力擴大，定價權主動讓出一部分","reasoning":"機制：裝機基數加醫師訓練（達文西 5 代已有逾 18,000 位醫師使用）加 48,000 篇同儕審查文獻，加上器械只能用在自家系統，醫院換平台要重訓整個團隊。可證方向用同業利潤率差代替 ROIC 差（事實表無投入資本）：近四季營業利益率 31.3%，對 SYK 21.7%、BSX 21.0%、MDT 19.0%，領先最強同業約 9.6 個百分點；FCF 利潤率 29.2% 對 8.6–18.2%。只有一期數據，差距是否擴大事實表未涵蓋。執行力在擴大：第三季裝機年增 28%，美國第一季達文西 5 代占系統裝機 85%，非 GAAP 毛利率扣除關稅退款仍年增 0.9 個百分點。定價權在縮：公司主動對高量良性手術降價、中國 11 月起政策降價，管理層稱是用單價換滲透。兩向相抵判持平。執行 9 分、定價權 8 分；若同業營益率差距下兩期連續收窄就要下調。","fact_refs":["f_peer_isrg_gross_margin_pct","f_peer_isrg_operating_margin_pct","f_peer_isrg_fcf_margin_pct","f_peer_mdt_operating_margin_pct","f_peer_mdt_fcf_margin_pct","f_peer_syk_operating_margin_pct","f_peer_syk_fcf_margin_pct","f_peer_bsx_operating_margin_pct","f_peer_bsx_fcf_margin_pct","f_kpi7_da_vinci_installed_base_"],"verdict_values":{"moat":{"mechanism":"裝機基數＋醫師訓練與臨床證據＋器械配件只能用在自家系統的封閉耗材，醫院換平台要重訓團隊、重建流程","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"執行力擴大：第三季裝機年增 28%、扣退款毛利率年增 0.9 個百分點、達文西 5 代逾 2,000 台；定價權縮減：2027 年器械降價 3–5%、中國 11 月政策降價。兩向相抵為持平","competitor_notes":[{"name":"MDT","strategy_note":"Hugo 以泌尿適應症切入美國，一般外科與婦科已送件；營業利益率 19.0%，規模大但機器人業務仍早期"},{"name":"SYK","strategy_note":"法說問答提及 Stryker 與 CMR 的消息，可能帶模組化系統進 ASC；營業利益率 21.7%"},{"name":"BSX","strategy_note":"非軟組織手術機器人直接對手，毛利率 69.9% 與 ISRG 相近但 FCF 利潤率只有 8.6%，作利潤率對照"},{"name":"J&J（Ottava）","strategy_note":"據股票分析文章，2026 年中獲十項一般外科許可，是軟組織手術二十年來首個可信挑戰者；同業財務事實表未涵蓋"},{"name":"中國本土廠商（微創等）","strategy_note":"靠集中招標與價格優勢在中國拿份額，10-K 列為競爭加劇來源"}],"peer_na_reason":"同業 ROIC 與 Fwd P/E 事實表未涵蓋，只用利潤率對照","threats":[{"level":"🔴","text":"中國：本土機器人競爭、集中招標、政策降價，2025 年裝機少於預期、2026 年第二季只裝 2 台，11 月起器械價格大幅下調","p":"60%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#2"]},{"level":"🟡","text":"美國：Medtronic Hugo（2025-12 泌尿許可、2026-02 美國首例、一般外科與婦科已送件）與 J&J Ottava（據報 2026 年中十項一般外科許可）切入良性手術與 ASC；目前仍屬點對點，尚無份額數據","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#3"]},{"level":"🔴","text":"售後市場：第三方再製器械與維修，SIS 案發回重審、醫院集體訴訟以 4.5 億美元和解待核准；若被迫開放，器械配件封閉性受損","p":"20%","evidence_refs":["substitute_technology#4","regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1","lawsuit_class_action#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（外科醫師，逾 18,000 人用過達文西 5 代）、決策者（醫院與 IDN，已開始用即時儀表板比較機器人與腹腔鏡的成本與結果）、付款者（保險與政府）三環都成立；良性手術大型統合分析顯示轉開腹機率較腹腔鏡低 54%。付款端有 ACA 補貼到期、Medicaid 資格變動的短期壓力"},{"item":"決策層級","level":"🟡","text":"替代要在醫院手術室層級衡量：已建立機器人計畫的醫院換平台要重訓團隊、重建流程，轉換成本高；但美國約 70% 新系統採租賃、約半數裝機是換機，降低了換平台的資本門檻，ASC 客群更看單台成本"},{"item":"價值鏈分配","level":"🟡","text":"公司拿走手術機器人價值鏈大部分利潤（營業利益率比同業高約 10 個百分點），付款端與中國政府已在要回：中國政策降價、公司主動對高量良性手術降價 3–5%"},{"item":"社會容忍度","level":"🟡","text":"社會天花板已在作用：醫院買方反壟斷集體訴訟以 4.5 億美元和解、SIS 案發回重審、中國以政策壓價；公司選擇不把價格推到經濟上限，用延長器械壽命讓利，屬保費性質"}],"roiic":"事實表未涵蓋（投入資本、折舊攤銷、營運資金變動皆缺）","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；本包缺投入資本，改以代理：2022→2025 營收年化 17.4%，期間唯一收購為 2026 年南歐經銷權約 5.28 億美元，成長幾乎全屬內生"}}}},"q3_growth":{"verdict":"🟡 五年後跑道中等：量還在長，但第二曲線相對總量仍小、價格轉為負貢獻","reasoning":"成長以量為主：2026 年手術量指引 14–15%，系統裝機年增 28%；價格轉為負貢獻（2027 年器械降價 3–5%，管理層稱 SP、達文西 5 代與力回饋器械會抵銷，但未量化）；回購是第三項，第三季買回 29 億美元。共識每股盈餘 FY2026 10.80、FY2027 12.12、FY2028 13.67 美元，兩年年化 12.5%；FY2025 非 GAAP 實際值事實表未涵蓋，三年 CAGR 無法依規格計算，改用兩年代理。內生上界：投入資本與再投資率事實表未涵蓋，無法算增量報酬；代理是 2022–2025 營收年化 17.4%，期間唯一收購是南歐經銷權約 5.28 億美元，成長幾乎全屬內生。共識 12.5% 低於此代理，缺口可由量增減降價、營益率持平、約 1% 淨回購解釋，不依賴重新評價。跑道：滲透率事實表未涵蓋；管理層稱 ASC 滲透在第一個四分位、心臟手術可見機會每年 30–40 萬例、海外良性手術占國際量四分之一且缺口最大，Ion 手術量年增 31%，但這些第二曲線相對總量仍小，美國增速由 12% 降到 10%，判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_guidance_fy2026","f_kpi7_da_vinci_installed_base_"],"verdict_values":{"growth":{"driver_mix":"量為主（手術量 14–15%、裝機 28%），價轉負（2027 年組合不變下 −3～−5%），回購為輔（淨回購約 1%）","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本事實表未涵蓋；代理為 2022–2025 營收年化 17.4% 且無大型收購，共識 EPS 兩年年化 12.5% 在代理之內","segments":[{"item":"器械配件","value":"第三季 18 億美元，年增 18%，約占營收 59%；每台手術約 1,860 美元"},{"item":"系統","value":"第三季 7.69 億美元，年增 30%；購買 ASP 約 160 萬美元持平"},{"item":"服務","value":"第三季 4.82 億美元，年增 22%"},{"item":"Ion","value":"裝機 1,152 台年增 21%，手術量年增 31%"}],"decay_signals":["核心市占近 12 個月縮減：中國 2025 年裝機少於預期、2026 年第二季只裝 2 台，本土機器人競爭與招標政策","SBC 占營收逾 5%：第三季 7.0%，全年估 8.6–8.7 億美元；是否逐年上升事實表未涵蓋","未亮：毛利率（扣退款年增 0.9 個百分點）、EPS 與營收成長差距（25% 對 22%）、FCF 對淨利（2025 年 0.87）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"B：回購買得不夠便宜，SBC 稀釋輕","reasoning":"現金轉換：2025 年自由現金流 24.9 億美元、淨利 28.6 億美元，轉換率 0.87；2023–2024 年只有 0.42–0.56，因建廠資本支出；2026 前九個月自由現金流 28.7 億美元。SBC 第三季 2.13 億美元、占營收 7.0%，全年估 8.6–8.7 億美元，約市值 0.6%，被回購完全抵銷。現金去向：第三季回購 29 億美元、均價 377 美元，第二季 3.79 億美元、均價 439 美元；南歐經銷權收購約 5.28 億美元；第三季資本支出 1.13 億美元；季底現金 68 億美元、零負債。以 377 美元計算的盈餘收益率約 2.9%（FY2026 共識 10.80 美元除以 377 美元），十年公債殖利率事實表未涵蓋，但要低於 0.9% 才會通過，此項判不過；收購金額小且已實現報酬事實表未涵蓋，不適用；SBC 淨稀釋低於 1.5%，通過。","fact_refs":["f_kpi4_free_cash_flow","f_kpi5_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"唯一收購為南歐經銷權約 5.28 億美元，約市值 0.35%，已實現報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"第三季均價 377 美元，對 FY2026 共識 EPS 10.80 美元的收益率約 2.9%；十年公債殖利率事實表未涵蓋，但需低於 0.9% 才會通過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"全年 SBC 約 8.65 億美元除以市值約 1,512 億美元約 0.6%，且回購金額遠大於 SBC"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，唯一收購為南歐經銷權約 5.28 億美元，現金主要用於回購"}}}},"q5_valuation":{"verdict":"現價要市場相信五年每股盈餘年增約 11–12% 且 2031 年仍給 32 倍以上；前半我信，後半不信","reasoning":"現價 428.12 美元，是 FY2026 共識 10.80 美元的 39.6 倍、FY2027 共識 12.12 美元的 35.3 倍。要划算，市場得相信五年每股盈餘年增約 11–12%，而且 2031 年仍給 32 倍以上。前半我信：共識兩年年化 12.5%，近三個月 FY2026 共識上修 3.65%，第三季優於預期。後半不信：公司自己把每台手術器械單價降 3–5%，美國增速 10%，J&J 與 Medtronic 已在美國拿到許可，倍數要維持 35 倍以上需要成長回到 15% 左右。PEG 以兩年 CAGR 12.5% 計為 3.2（FY2027 口徑 2.8），屬貴。歷史對照：近四個年度端點的本益比、P/S、EV/S 分位都是 0，現價是自己歷史的低點，但只有四個點、不是五年連續序列。追蹤本益比 51.8 倍被 4.5 億美元和解費壓低分母，不採用，改看前瞻口徑。賣方平均目標價 477–539 美元，上半年曾在 620 美元左右，持續下修。同業前瞻本益比事實表未涵蓋，前份以高成長醫材約 28 倍作錨，本次無法重驗。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ev_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026 非 GAAP 共識）＋PEG","tier":"高成長醫材","peers":{"expanded":false,"reason":"事實表只有同業利潤率，無同業前瞻本益比；前份以高成長醫材約 28 倍作錨，本次無法重驗"},"fwd_pe":39.64,"peg":3.17,"percentile_5y":0.0,"val_light":"🟠","val_light_derivation":"PEG 3.2（FY2026 口徑，CAGR 用 FY2026→FY2028 兩年年化 12.5%）大於 2 屬貴；但本益比在自身四個年度端點的分位為 0（非連續五年序列），不到最貴一檔，判 🟠。短期以 FY2027 Base 12.0 美元乘 34 倍得 408 美元，−4.7%；中期（三年）以 FY2029 Base 14.9 美元乘 32 倍得 477 美元，+11.4%","upside_short_pct":-4.7,"upside_mid_pct":11.4,"denominator_disputed":false,"denominator_note":"追蹤 GAAP 盈餘含 4.5 億美元一次性和解費，分母偏低；改用 FY2026／FY2027 非 GAAP 共識，分母不構成爭點"}}},"q6_how_wrong":{"verdict":"🟡 最可能看錯在：降價沒換到量、競品在美國良性手術切入、售後市場被法院打開","reasoning":"三處：一是降價換滲透沒換到量，2020 年第一次延長使用計畫時管理層稱有彈性，但這次美國增速已降到 10%，若 2027 年美國良性一般外科不加速，單價與量會同時往下；二是競品用低價切入 ASC 與良性手術，Ottava、Hugo 都已可在美國銷售，Stryker 也有模組化系統的消息；三是售後市場被法院打開，SIS 案發回重審，若最終認定售後市場獨占並開放第三方再製，器械配件的封閉性就破了。三個反證視角都已寫進反證紀錄；衰退訊號亮兩項（中國市占、SBC 占營收），判 🟡。股價 26 週跌 2.9%、仍低於 104 週均線，市場已部分反映競爭擔憂。","fact_refs":["f_week26_return_pct","f_ma_w104","f_kpi2_gaap_operating_income_ma","f_kpi5_sbc_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩項衰退訊號：中國市占流失、SBC 占營收逾 5%"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.8,"pe":39.64,"basis":"FY2026 共識非 GAAP EPS 10.80 美元，與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[12.6,14.6,16.9,19.4,22.0],"base":[12.0,13.4,14.9,16.4,18.0],"bear":[11.0,11.4,11.7,11.9,12.0]},"pe":{"bull":36,"base":32,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"max_dd":{"lo":-48,"hi":-30,"basis":"2026 年股價曾自高點回落約 30%（Ottava 獲准後）；現價 428 美元仍低於 104 週均線 488 美元。Bear 終點 12.0 美元乘 22 倍為 264 美元，約 −38%；若路徑中同時遇到售後市場不利判決與美國手術量跌破 8%，倍數可短暫壓到 20 倍左右（FY2027 Bear 11.4 美元乘 20 倍為 228 美元，約 −47%），取 −30% 至 −48%","trigger_time":null},"basis":{"bull":"美國手術量回到 12% 以上、延長使用計畫帶出量的彈性、力回饋與 SP 抵銷降價，營益率維持 40% 以上；終端 36 倍，介於現值 39.6 倍與前份同業錨約 28 倍之間","base":"全球手術量年增 11–13% 逐年放緩、器械單價 2027 年淨降約 2%（降價扣組合抵銷）、營益率 38–40%、淨回購約 1%；2029 年後盈餘年增約 10%；終端 32 倍","bear":"競品在美國良性手術與 ASC 拿下份額、售後市場開放或中國持續流失，手術量增速降至個位數中段，營益率回到 35% 區間下緣；倍數向成熟醫材 22 倍收斂，作為成長熄火至 10% 的錨"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Ottava 2026 年中獲 FDA 十項一般外科許可、Hugo 2025-12 獲泌尿許可並於 2026-02 完成美國首例；中國本土競爭使裝機少於預期；美國達文西增速 10%，為疫情後最低","assumption":"美國醫院在成本敏感的良性手術與 ASC 會選低價第二平台","consequence":"美國手術量增速降到 5–7%，降價又沒換到量，盈餘五年只增約 2%，倍數壓到 22 倍，股價約 264 美元、五年虧近四成；再疊加售後市場開放（獨立於此故事的唯一致命點）才會到虧五成","ruling":"部分採納：競品拿到許可是事實，但第三季美國系統裝機年增 27%、美國淨新增裝機年增 41%，醫院仍在擴產能；Bear 機率取 30% 而非更高","watch":"美國達文西手術量年增率，連兩季低於 8% 即成立","evidence_refs":["substitute_technology#1","substitute_technology#0","competitive_share_entrants#0"],"fact_refs":["f_kpi7_da_vinci_installed_base_"]},{"view":"論點成功但股東經濟變差","evidence":"CFO：營業利益率合理區間 35–40%，現在 41–42%，有投資的空間；2027 年器械降價 3–5%；全年 SBC 8.6–8.7 億美元","assumption":"手術量照計畫成長，但公司把超額利潤再投入研發、海外擴張與降價","consequence":"營收年增十幾 %、營益率回落到 38%，每股盈餘成長落後營收，股東拿到較低的利潤率","ruling":"採納：Base 路徑已把 2027–2028 年盈餘放在共識略下（12.0／13.4 美元對 12.12／13.67 美元）","watch":"2027 年 1 月指引的非 GAAP 營業費用成長是否高於營收成長","evidence_refs":[],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi5_sbc_gaap","f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"前瞻本益比 39.6 倍、PEG 3.2；賣方平均目標價由上半年約 620 美元降到 477–539 美元，Evercore 降到 430 美元、BofA 降到 520 美元","assumption":"市場仍以高成長醫材上緣定價","consequence":"即使盈餘照共識，倍數回到 32 倍，五年 Base 年化只有約 7%","ruling":"採納：這是現在不進場的主因，進場條件綁價格","watch":"股價對 FY2027 共識的倍數是否降到 29 倍以下","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"2026 年兩起 Class II 召回（機械臂螺絲、病人側推車煞車銷）；2 月有團體請願要求對達文西 5 代 Class I 召回並發警告信","assumption":"安全事件升級成全系統召回或警告信","consequence":"新機裝機暫停、醫院延後採購，達文西 5 代換機週期中斷","ruling":"反駁：兩起皆為 Class II，未見 FDA 警告信，請願只是請求、FDA 未回應；第三季達文西 5 代裝機 315 台未見影響","watch":"FDA Class I 召回或警告信","evidence_refs":["major_events#3","major_events#4","product_recall_warning#0","product_recall_warning#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 358.97 → 本次 428.12（+19.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=358.97","side_b":"本次 price_at_dd=428.12","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 358.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 358.97 美元：Bull 價 770、Bear 價 280，五年期望值 +47.9%，基準年化 10.8%，不對稱比 3.5","side_b":"本次情境、股價仍用 358.97 美元：Bull 價 792、Bear 價 264，五年期望值 +49.4%，基準年化 9.9%，不對稱比 3.8","ruling":"先換情境、股價不動：五年期望值多 1.5 個百分點，基準年化少 0.9 個百分點。不對稱比由 3.5 變為 3.8。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 358.97 美元：五年期望值 +49.4%，基準年化 9.9%，不對稱比 3.8","side_b":"本次情境、股價 428.12 美元：五年期望值 +25.3%，基準年化 6.1%，不對稱比 1.85","ruling":"再換股價、情境不動：起點價上漲 19.3%，五年期望值少 24.1 個百分點，基準年化少 3.8 個百分點，不對稱比由 3.8 降到 1.85。合計五年期望值比前份少 22.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決（價格變動）","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 358.97 美元，估值判貴（🟠），裁決觀望","side_b":"本次：股價 428.12 美元，漲約 19%，FY2026 共識只上修 3.65%，前瞻本益比升到 39.6 倍；估值結論仍判貴，未到最貴一檔","ruling":"估值結論維持；價格漲幅大於盈餘上修，離進場價更遠，裁決與角色預期不變，由程式依矩陣確認","evidence_level":"事實表","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若股價續漲到 480 美元以上而盈餘未上修則不追"],"evidence_refs":[]},{"axis":"價值陷阱評級","cause":"新證據","prior_field":["trap"],"side_a":"前份：🟢，無衰退訊號","side_b":"本次：🟡，亮兩項——中國市占流失（2025 年裝機少於預期、第二季只裝 2 台、11 月政策降價）、SBC 占營收 7.0%","ruling":"採 🟡：中國流失有 10-K 與法說原話支持；SBC 比率逐年趨勢事實表未涵蓋，保守計入","evidence_level":"10-K／法說","settle_metric":"中國手術量與裝機","if_then":["若中國手術量轉負則停止加碼","若中國綠色通道核准達文西 5 代且裝機回升則撤回該訊號"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"情境機率","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：Bull 22%、Bear 33%","side_b":"本次：Bull 25%、Bear 30%","ruling":"第三季營收增 22%、全年手術量指引收窄到 14–15%、毛利率指引上調，且延長使用計畫量化為 3–5%，低於市場擔心的 5–7%；但美國增速降到 10%、Ottava 已獲准，Bear 只降 3 個百分點、仍守 30%","evidence_level":"8-K／法說","settle_metric":"2027 年手術量指引","if_then":["若 2027 年手術量指引中點低於 12% 則 Bear 調回 35% 以上","若美國手術量連兩季回到 12% 以上則上調 Bull"],"evidence_refs":["substitute_technology#1"]},{"axis":"護城河方向、跑道、總評","cause":"新證據","prior_field":["moat_trend","runway_post_y5","signal"],"side_a":"前份：護城河持平、五年後跑道中等、總評 B","side_b":"本次：三項不變","ruling":"新證據雙向：裝機年增 28%、達文西 5 代逾 2,000 台支持執行力；降價、中國、競品許可壓定價權，相抵後方向不變；滲透率仍無數據，跑道維持中等","evidence_level":"8-K／法說","settle_metric":"同業營益率差距與美國手術量","if_then":["若同業營益率差距連兩期收窄則護城河方向改為縮減並重跑","若海外良性手術維持 35% 以上成長且 1 月更新的長期機會上調則跑道改寬"],"evidence_refs":[]},{"axis":"最大回撤、類型、循環位置","cause":"方法變動","prior_field":["max_dd_pct","archetype","cycle_position"],"side_a":"前份：最大回撤單點 −45%；品質複利成長；不適用循環位置","side_b":"本次：回撤改給範圍 −30%～−48%；類型與循環位置不變","ruling":"規格改為範圍、寬度至少 10 個百分點；下緣取 Bear 路徑中途倍數壓到 20 倍（FY2027 Bear 11.4 美元乘 20 倍為 228 美元）","evidence_level":"推算","settle_metric":"無","if_then":["若售後市場判決不利則以下緣 −48% 作倉位上限依據"],"evidence_refs":[]},{"axis":"進場條件（首倉）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","side_b":"股價 ≤ $350（約 FY2027 共識 EPS 12.12 的 29 倍）；或 FY2027 共識升至 ≥ $14.7 而股價不變","ruling":"首倉進場條件改錨 FY2027：FY2026 只剩一季，已不是前瞻分母；舊條件的 FY2026 EPS 10.75 美元已達成，但股價同時漲到 428 美元，PEG 仍 3.2，未觸發。新門檻 350 美元對應 Base 五年年化約 11%","evidence_level":"事實表","settle_metric":"股價／FY2027 共識","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若 FY2027 共識下修 5% 以上則門檻價同比例下移"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"美國手術量連兩季低於 8% 減碼；器械每台手術收入低於 1,780 美元減碼；非 GAAP 營益率低於 35% 減碼；SIS 發回重審認定售後市場獨占則清倉","ruling":"本次新增：延長使用計畫已量化，能把前份風險文字轉成可監測門檻","evidence_level":"法說","settle_metric":"各季財報","if_then":["任一減碼門檻觸發則減碼一半","SIS 不利判決則清倉"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"SIS 反壟斷案全院重審被駁回、發回重審認定售後市場獨占並要求開放第三方再製與維修","ruling":"新證據：第九巡迴 2026-08 撤銷原判並發回，公司 2026-09-28 聲請全院重審；器械配件約占營收 59%，是數學上最大的單一敏感項。發生則清倉","evidence_level":"法院判決報導","settle_metric":"全院重審裁定","if_then":["若全院重審准許並恢復原判則風險降級","若發回重審判決不利則清倉"],"evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"axis":"假設與風險改寫","cause":"新證據","prior_field":["H","R"],"side_a":"前份 H3 是倍數維持 28–34 倍；R1 延長使用計畫量級管理層兩次拒答","side_b":"本次 H3 改為營益率 ≥38%；R1 改用已量化的 3–5%；新增關稅供應鏈與產品安全兩條風險","ruling":"倍數不是公司能交付的假設，改放進場條件；延長使用計畫第三季已量化，風險改寫成可監測門檻","evidence_level":"法說","settle_metric":"無","if_then":["若 2027 年 1 月指引營益率低於 38% 則 H3 判削弱"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Ottava、Hugo 在美國可銷售，中國本土競爭與招標政策壓價","side_b":"結構轉好：海外良性手術年增 41%、美國淨新增裝機年增 41%、ASC 兩季裝機超過過去近三年；其他結構變數：售後市場反壟斷、關稅","ruling":"雙向拉鋸：競爭在中國已見份額影響，在美國只有許可、尚無份額數據；需求面擴張仍有手術量支持","evidence_level":"10-K／法說／新聞","settle_metric":"美國手術量與中國裝機","if_then":["若美國手術量連兩季低於 8% 則改判競爭惡化中"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#1"]},{"axis":"降價換滲透（可調和）","cause":null,"prior_field":null,"side_a":"管理層：降價集中在高量良性手術，2020 年第一次延長使用計畫的資料證明有彈性，量會回來","side_b":"2026-07-16 CFO 兩次拒答量級（not ready to quantify it yet）；美國增速 10% 為疫情後最低，降價時機與放緩重疊","ruling":"可調和、程度差異：本次已給 3–5%，小於 2020 年的 7%，管理層並承諾用成本下降抵銷毛利率影響；採信方向，但量的回應要到 2027 下半年才看得到，Base 盈餘放在共識略下","evidence_level":"法說","settle_metric":"2027 年美國良性一般外科手術量增速","if_then":["若 2027 下半年美國手術量回到 12% 以上則上調 Bull","若降價上路後兩季美國手術量仍低於 10% 則減碼一半"],"evidence_refs":[]},{"axis":"管理層承諾兌現（一致）","cause":null,"prior_field":null,"side_a":"2026-07-16 IR：全年手術量 13.5–15.5%、靠近中點；毛利率 68–69%；延長使用計畫下次量化","side_b":"2026-10-20：收窄到 14–15%、靠近中點；毛利率上調到 68.7–69.3%；延長使用計畫已量化 3–5%","ruling":"一致：三項承諾都兌現，管理層信用不扣分","evidence_level":"法說","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"反壟斷：和解與發回重審","cause":null,"prior_field":null,"side_a":"管理層：與美國客戶集體訴訟無過失和解，提供確定性","side_b":"SIS 競爭者案 2026-08 被第九巡迴發回，公司 2026-09-28 聲請全院重審；和解只涵蓋客戶集體訴訟，和解所稱第三方再製與維修的合作框架條款未公開","ruling":"不可調和於確定性這一點，選 B 側：客戶求償金額已封頂在 4.5 億美元，但售後市場能否被開放仍未決，風險保留於唯一致命點","evidence_level":"法說／法院判決報導","settle_metric":"法院核准的和解條款、全院重審裁定","if_then":["若和解條款允許第三方再製器械普遍使用則減碼一半","若全院重審推翻合議庭判決則售後市場風險降級並重跑"],"evidence_refs":["regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"第三季營收增 22%、非 GAAP EPS 增 25%，營益率 41.6%，零負債，第三季以均價 377 美元回購 29 億美元；本益比是自身近四個年度端點最低；賣方 27 人中 23 人給買進","side_b":"同樣的盈餘只值 32 倍時，Base 五年年化約 7%；價格要到 350 美元附近才有 11% 以上","ruling":"不採：好生意，但現價的五年報酬不夠；不追、等價格","evidence_level":"事實表／賣方彙整","settle_metric":"股價","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若股價續漲而 FY2027 共識未上修則不追"],"evidence_refs":["capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"美國達文西手術量年增率連兩季跌破 8%","type":"假設驗證","maps_to":"H2","metric":"美國 da Vinci 手術量 YoY","threshold":"<8% 連兩季","action":"撤銷進場條件；持有者減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":2,"text":"延長使用計畫上路後器械每台手術收入守不住","type":"假設驗證","maps_to":"H1","metric":"da Vinci 器械配件每台手術收入","threshold":"<1,780 美元（2027 下半年任一季）","action":"減碼","source_freq":"法說／每季","date":"2027-07","evidence_refs":[]},{"n":3,"text":"營業利益率跌出管理層區間","type":"假設驗證","maps_to":"H3","metric":"非 GAAP 營業利益率","threshold":"2027 全年 <38%；單季 <35%","action":"低於 38% 停止加碼；低於 35% 減碼","source_freq":"8-K 財報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":4,"text":"SIS 案全院重審裁定與發回重審結果","type":"Single Thing","maps_to":"Single Thing","metric":"第九巡迴全院重審裁定","threshold":"駁回重審並進入發回重審；發回後判決不利","action":"駁回時不追；發回後判決不利則清倉","source_freq":"法院公告／事件","date":"2027-01","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"n":5,"text":"關稅與稀土供應吸收失敗","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率（扣關稅退款）","threshold":"<68% 連兩季，或公告稀土出口許可造成出貨延遲","action":"停止加碼","source_freq":"季報／每季","date":"2027-04","evidence_refs":["reg_tariff_export#1","geo_supply_chain#2"]},{"n":6,"text":"股價回到進場區","type":"估值rearm","maps_to":"進場條件","metric":"股價／FY2027 共識 EPS","threshold":"股價 ≤350 美元（約 29 倍）","action":"重跑判斷後首倉 ≤2%","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":7,"text":"第四季財報、2027 年指引與軟組織長期機會更新","type":"複審日期","maps_to":"H1/H2/H3","metric":"2027 年手術量與營業費用指引","threshold":"手術量指引中點 <12%","action":"重跑判斷","source_freq":"法說／一次","date":"2027-01","evidence_refs":[]},{"n":8,"text":"中國器械降價 11 月生效後的實際影響","type":"風險","maps_to":"R1","metric":"中國手術量與器械收入","threshold":"中國手術量轉負","action":"停止加碼","source_freq":"法說／每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1"]}],"kill_metrics":[{"metric":"美國 da Vinci 手術量年增率","bear_threshold":"<8% 連兩季","window":"2026Q4–2027Q4","source":"公司季報新聞稿","last_status":"warning"},{"metric":"da Vinci 器械配件每台手術收入","bear_threshold":"<1,780 美元","window":"2027 全年","source":"每季法說 CFO 發言","last_status":"ok"},{"metric":"非 GAAP 營業利益率","bear_threshold":"<35%（管理層區間下緣）","window":"任一連續四季","source":"8-K 財報新聞稿","last_status":"ok"},{"metric":"SIS 反壟斷案","bear_threshold":"發回重審認定器械售後市場獨占","window":"2027–2028","source":"第九巡迴與地方法院公告","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤ $350（約 FY2027 共識 EPS 12.12 的 29 倍）；或 FY2027 共識升至 ≥ $14.7 而股價不變","exec_line":"觸發後先重跑判斷；首倉 ≤2%，2027 年 1 月指引確認營益率 ≥38% 且美國手術量 ≥8% 後加到 4%；不追高","holding_cap":"4%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤350 美元（約 FY2027 共識 29 倍），或 FY2027 共識升至 ≥14.7 美元而股價不變","qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-2.94, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"裝機基數與 84% 經常性收入守住，器械配件每台手術收入在延長使用計畫與中國降價全面實施後，加上組合抵銷，年降幅不超過 4%","2y":"2027 年底每台手術器械收入 ≥1,780 美元","5y":"經常性收入占比維持 ≥80%","10y":null,"threshold":"每台手術器械收入 ≥1,780 美元；經常性收入占比 ≥80%","source":"每季法說 CFO 揭露的每台手術器械收入、財報新聞稿經常性收入占比","drift_rule":"5 年期：連 4 季偏離門檻 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H2","text":"海外良性手術、SP、Ion、心臟與 ASC 接棒，全球達文西手術量維持年增 11% 以上到 2028 年","2y":"2027 年全球 ≥12%、美國 ≥8%","5y":"2028–2030 年全球 ≥10%","10y":null,"threshold":"全球達文西手術量年增 ≥11%、美國 ≥8%","source":"每季財報新聞稿與法說手術量數據","drift_rule":"5 年期：連 4 季偏離門檻 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"在降價與關稅下，非 GAAP 營業利益率仍守在管理層 35–40% 區間上緣","2y":"2027 年非 GAAP 營業利益率 ≥38%","5y":null,"10y":null,"threshold":"非 GAAP 營業利益率 ≥38%","source":"8-K 財報新聞稿、每年 1 月全年指引","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱、連 3 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"器械單價侵蝕：延長使用計畫（2027 上半年起逐國上路）、中國 11 月起政策降價、XiR 與 X 低價機組合，加上 GLP-1 壓抑減重手術，同向拉低每台手術收入；管理層說的 SP、達文西 5 代與力回饋抵銷尚未量化（力回饋只用在 8% 的 5 代手術）","h_ref":"H1","clock":"🔥","threshold":"每台手術器械收入年減逾 4% 連兩季","evidence_refs":["competitive_share_entrants#1"]},{"id":"R2","text":"美國手術量降檔加競品入場：美國增速由第二季 12% 降到 10%；Hugo、Ottava 已可在美國銷售，Stryker 有模組化系統的消息；ACA 補貼、Medicaid 資格與 340B 變動是付款端壓力","h_ref":"H2","clock":"🔥","threshold":"美國達文西手術量年增 <8% 連兩季","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3"]},{"id":"R3","text":"器械售後市場被法院打開：SIS 案發回重審並聲請全院重審，醫院集體訴訟 4.5 億美元和解待核准，第三方再製器械持續挑戰","h_ref":"H1","clock":"🐢","threshold":"發回重審判決不利，或和解條款開放第三方再製器械","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1","lawsuit_class_action#0","substitute_technology#4"]},{"id":"R4","text":"關稅與稀土：器械在墨西哥生產靠 USMCA 免稅，內視鏡在德國生產受關稅；2026 前九個月關稅成本 7,240 萬美元，另認列 IEEPA 退款 6,370 萬美元且後續不確定；Section 301 對 60 國加徵 10–12.5%；中國稀土出口管制可能斷料，部分零件單一來源","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率扣退款 <68% 連兩季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#4","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"產品安全：2026 年兩起 Class II 召回，公民請願要求達文西 5 代 Class I 召回","h_ref":"H2","clock":"🐢","threshold":"FDA Class I 召回或警告信","evidence_refs":["major_events#3","major_events#4","product_recall_warning#0","product_recall_warning#1"]}],"single_thing":{"description":"SIS 反壟斷案全院重審被駁回，發回重審後認定公司在器械售後市場具獨占力，法院要求開放第三方再製與維修","why_fatal":"器械配件約占營收 59%、是利潤主來源；封閉售後市場一打開，每台手術器械收入可能被第三方以低價分走，影響遠大於公司自己宣布的 3–5% 降價","if_happens":"Base 機率移入 Bear，持有者清倉；未持有則撤銷進場條件、重跑判斷","how_monitor":"第九巡迴全院重審聲請結果（2026-09-28 提出）、客戶集體訴訟和解的法院核准條款（管理層稱 2027 年裁定）","probability":"約 10%（12–24 個月內出現不利判決；重審聲請未決、發回後仍需重新審理，客戶集體訴訟已和解）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":35.32,"peg_fy2":2.83,"stress":{"pass":3,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":10.8,"FY2027E":12.12,"FY2028E":13.67},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識）；FY2025 非 GAAP 實際值事實表未涵蓋（GAAP 7.87 美元口徑不同不得混用），三年 CAGR 以 FY2026→FY2028 兩年年化 12.5% 代理"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國器械收費代碼政策降價生效","impact":"中","watch":"第四季中國手術量與器械收入"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"SP 血管閉合器美國送件","impact":"低","watch":"SP 手術量成長"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報、2027 年指引與軟組織長期機會更新","impact":"高","watch":"手術量指引中點、營業費用成長"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"美國延長使用器械 510(k) 許可與上路","impact":"高","watch":"每台手術器械收入"},{"date":"2027-Q2","date_precision":"quarter","type":"regulatory","event":"客戶集體訴訟和解法院核准與 SIS 案全院重審裁定（管理層稱 2027 年裁定，季度未定）","impact":"高","watch":"和解條款是否開放第三方再製器械"}]}
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
