你是 DD 管線 v20 的判斷層閘（gate），標的 MSTR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（38 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝125.4 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001050446/000105044626000047/mstr-20261029x8kxex9912.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：共識約 128M（媒體報導，未經公司來源驗證）；營收未達
- `f_kpi1_gaap_operating_income`（q1_business）｜GAAP operating income＝20910 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（同上）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：不適用（數字幾乎全為數位資產公允價值利得 20.91B）
- `f_kpi2_operating_result_excludi`（q1_business）｜Operating result excluding digital asset gains＝-2.6 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：依新聞稿毛利 89.6M 減不含數位資產的營業費用 92.2M 自行計算，公司未揭露（非公司 non-GAAP）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無
- `f_kpi3_gross_profit_margin`（q1_business）｜Gross profit / margin＝71 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（毛利 89.6M）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無
- `f_kpi4_net_income_to_common_dil`（q1_business）｜Net income to common / diluted EPS＝44.75 USD per diluted share｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（淨利 19.53B；歸普通股 19.12B，已扣特別股股利 419.6M）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無（EPS 受 BTC 公允價值波動主導，無可比共識）
- `f_kpi5_btc_holdings`（q1_business）｜BTC holdings＝848517 BTC｜期間與口徑：截至 2026-10-25（Q3 FY2026 新聞稿，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（成本 64.02B；9-30 約 847,666 BTC）（numbers.latest_quarter_kpis.items[5]，as_of 截至 2026-10-25（Q3 FY2026 新聞稿，公告於 2026-10-29））
  - 註記：無
- `f_kpi6_btc_yield_ytd`（q1_business）｜BTC Yield (YTD)＝-3.7 %｜期間與口徑：YTD 2026 至 Q3 FY2026（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（單季值未揭露）（numbers.latest_quarter_kpis.items[6]，as_of YTD 2026 至 Q3 FY2026（公告於 2026-10-29））
  - 註記：無
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝423.57 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝58022.92 USD m｜期間與口徑：2026-11-03／市值 57152.6 ＋ 淨負債 870.32｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_mstr_gross_margin_pct`（q2_moat）｜MSTR 毛利率＝66.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSTR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mstr_operating_margin_pct`（q2_moat）｜MSTR 營業利益率＝-10.96 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSTR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mstr_fcf_margin_pct`（q2_moat）｜MSTR FCF 利潤率＝-4539.71 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSTR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_coin_operating_margin_pct`（q2_moat）｜COIN 營業利益率＝5.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_coin_fcf_margin_pct`（q2_moat）｜COIN FCF 利潤率＝68.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mara_operating_margin_pct`（q2_moat）｜MARA 營業利益率＝-126.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MARA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3350_t_operating_margin_pct`（q2_moat）｜3350.T 營業利益率＝69.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3350.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_glxy_operating_margin_pct`（q2_moat）｜GLXY 營業利益率＝-0.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GLXY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝-17.44 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝23.67 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝23.77 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（-17.44 → -17.44）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（23.67 → 23.67）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（23.77 → 23.77）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝500.56 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝515.49 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝870.32 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 6776.23、現金 5905.91（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝134.93 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝115.44 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝81.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝81.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝117.2 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝73.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝73.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝115.92 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 132.65 / W52 141.15 / W104 244.56 / W250 139.73 / W250 13週斜率 1.03%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝139.73 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w52`（q5_valuation）｜52 週均線＝141.15 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-26.59 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.64｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出企業分析軟體對手為 IBM、Microsoft、Oracle、Salesforce、SAP 等全球 ISV；AI 整合落後可能損害競爭力
  - 來源：SEC EDGAR 10-K FY2025 Item 1 / 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 表示募資時與 ETP、礦商、其他持幣企業、傳統金融機構等競爭資金，競爭加劇可能提高融資成本
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Pepperstone：若 Strategy 無法再融資或展期票據，未來可轉債需求恐大減
  - 來源：Pepperstone — Bitcoin Treasury Risk and Strategy's Balance Sheet（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Rosen Law Firm 於 2026-06-24 對 Strategy 及 Saylor 展開證券調查（原告律所調查，非政府行動，未提起集體訴訟）；三項搜尋均未找到 DOJ/FTC/EU 反壟斷調查。
  - 來源：Bitcoin.com, Law Firm Investigates Strategy as MSTR Drops 7% and STRC Crashes to $73（as_of 2026-06-24）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q 風險因子：比特幣有時可能集中由單一託管人保管，託管人保險為所有客戶共用
  - 來源：Strategy Inc Form 10-Q (period 2026-06-30)（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 總營收 $125.4M，YoY -3%（Q3 2025 為 $128.7M）
  - 來源：AMBCrypto: MSTR stock falls 6.8% in 2026 despite Strategy's $20.9B Q3 income（as_of 2026-10-30）｜affects：valuation、moat_trend
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：AI 驅動攻擊與量子運算可能使傳統密碼技術失效，構成對公司系統的新漏洞(技術面風險，非替代產品)。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Blockworks 指出 2026 年 Strategy 買幣較零星，ETF 資金流為更可靠的價格決定力量;Strategy 與現貨比特幣上市商品爭奪投資人資金。
  - 來源：Blockworks: The Strategy playbook looks different in 2026（as_of 2026-01-15）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年 6–7 月多家調降目標價：TD Cowen 6/30 降至 $260、Citi 7/1 降至 $136、Mizuho 7/7 降至 $213，皆維持 Buy/Outperform；B. Riley 4/29 由 $188 升至 $200
  - 來源：AnaChart / Placera（as_of 2026-07-07）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Ticker Nerd 修正追蹤：次一財年 EPS 90 天修正 -88.1%，0 位上修、1 位下修（單一分析師樣本）
  - 來源：Ticker Nerd MSTR forecast（as_of 2026-09-15）｜affects：valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露一件進行中的 putative class action（Dodge Class Action），涉及 2025-07-07 STRK 特別股指定證書修正，董事會同為被告；公司稱不預期其他訴訟有重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A / Note 9（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#2`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：Q2 2026 歸屬普通股淨損$8.62B（含$400.7M優先股股息）；今年已賣約$218.4M比特幣支付部分優先股股息；STRC低於面值100買回
  - 來源：Strategy Q2 2026 Financial Results (press release)（as_of 2026-07-30）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#3`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：軟體為2026槓桿貸款壓力主要來源：占市場13%卻占31%困境貸款；實際違約率仍低(TTM 0.93%，2026年7月)
  - 來源：PitchBook / 搜尋彙整（Distressed & Defaults）（as_of 2026-09-30）｜affects：decision_inputs.bear
- `financial_capital_credit_cycle#4`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：Morgan Stanley 預期私募信貸違約率因AI衝擊軟體業升至8%
  - 來源：Bloomberg（as_of 2026-03-16）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Dodge Class Action（Delaware Chancery，2025-07-21 提起）主張 STRK 修正案應經普通股股東投票，並訴董事會違反受託義務。
  - 來源：SEC EDGAR 10-K FY2025 Note 9（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":628.2,"bear_5y_price":36.7,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":51.3,"ev5y_pct":92.7,"irr_base_pct":8.6,"asym_ratio":4.2,"scenario_tree":{"terminal_label":"FY2031E","valuation_basis":"sales_multiple","start":{"rev":500.56,"ev_s":115.92,"basis":"起點營收取 FY2026E 共識（7 位分析師平均）；起點 EV/S＝事實表 EV（市值＋總債務−現金）÷ FY2026E 營收，未含約 131 億美元優先股。終端 EV/S＝終端年 EV ÷ 同年營收，同為前瞻年度口徑；但終端淨負債把優先股名目當作股東之前的求償權計入，若起點也計入優先股，起點 EV/S 約 142 倍。同業 EV/S 現值事實表未涵蓋，終端倍數只能對照本身現值。EV/S 在此只是把淨資產模型換成營收倍數格式，數字本身無經濟意義"},"rev":{"bull":[530,560,590,620,650],"base":[510,515,520,525,530],"bear":[480,460,440,420,400]},"ev_s":{"bull":543.7,"base":246.8,"bear":91.16},"net_debt_y5":{"bull":33000,"base":28700,"bear":16300},"shares_y5":{"bull":510,"base":500,"bear":550},"net_debt_now":870.32,"shares_now":423.57,"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":null,"valuation_dependent":true}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSTR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Phong Le｜guidance：美元準備金目標存續期 2–3 年（原話："our target is to be somewhere between 2 and 3 years."）
- 2026-07-30｜Phong Le｜commitment：美元準備金最低維持 1 年股息利息覆蓋（原話："we're going to keep 1 year of minimum"）
- 2026-07-30｜Phong Le｜commitment：Phong 重申美元準備金最低 1 年（原話："our minimum will be 1 year."）
- 2026-07-30｜Phong Le｜guidance：STRC 股息率目前計畫維持 12%（原話："So our current plan is to keep the rate right at 12%."）
- 2026-07-30｜Phong Le｜commitment：不打算降 STRC 利率來拉回面值（原話："We're not planning on decreasing the Stretch rate"）
- 2026-07-30｜Phong Le｜guidance：公司目標讓 STRC 回到 $99–100（原話："It's for Stretch to trade at $99 to $100 over time."）
- 2026-07-30｜Phong Le｜risk：STRC 現價約 $89.50，低於目標區間（原話："Stretch is now trading at about $89.50."）
- 2026-07-30｜Michael Saylor｜guidance：Saylor 以 IPO 後 70 交易日到面值類比，推算時點約 9/8（原話："that would put us around September 8"）
- 2026-07-30｜Michael Saylor｜commitment：Saylor 表示確定會讓 STRC 回到面值（原話："We're certain that we will return STRC to par."）
- 2026-07-30｜Michael Saylor｜guidance：買回規模與速度仍在摸索（原話："We're currently in a discovery process"）
- 2026-07-30｜Michael Saylor｜risk：STRC 市值與面額約 $1.2B 缺口（原話："So there's about a $1.2 billion dislocation."）
- 2026-07-30｜Michael Saylor｜commitment：STRC 低於面值就不發行（原話："we can't sell it at par, we're not going to sell it at all"）
- 2026-07-30｜Michael Saylor｜capital_allocation：目前不發行 STRC（原話："we're not selling Stretch right now"）
- 2026-07-30｜Michael Saylor｜commitment：公司不會暫停股息（原話："The company is not going to suspend its dividends"）
- 2026-07-30｜Phong Le｜capital_allocation：比特幣貨幣化三用途（原話："Bitcoin monetization, selling Bitcoin for 3 purposes"）
- 2026-07-30｜Phong Le｜capital_allocation：首筆賣幣 32 BTC 的理由（原話："We did it to inoculate the market and test our processes."）
- 2026-07-30｜Andrew Kang｜capital_allocation：季後至 7/27 賣出 2,225 BTC（原話："we did sell 2,225 Bitcoin for approximately $135 million"）
- 2026-07-30｜Phong Le｜capital_allocation：年初至今買賣 BTC 數量（原話："We bought 174,895 Bitcoin year-to-date 2026."）
- 2026-07-30｜Phong Le｜capital_allocation：年初至今賣出 BTC 數量（原話："We sold 3,620 Bitcoin during that same period of time."）
- 2026-07-30｜Phong Le｜capital_allocation：STRC 買回授權至多 $1B（原話："ability to repurchase digital credit up to $1 billion"）
- 2026-07-30｜Phong Le｜capital_allocation：MSTR 買回條件：低於每股淨比特幣（原話："when it's trading at a discount to net Bitcoin per share"）
- 2026-07-30｜Andrew Kang｜capital_allocation：Q2 以折價回購可轉債 $1.5B（原話："the $1.5 billion repurchase of convertible debt"）
- 2026-07-30｜Phong Le｜capital_allocation：下次可轉債回售日（原話："next convertible debt put date is September of next year"）
- 2026-07-30｜Andrew Kang｜capital_allocation：可轉債處理無時程（原話："There is no set time line."）
- 2026-07-30｜Andrew Kang｜capital_allocation：可轉債處理有三種選項，優先順位為 STRC 回面值（原話："liability management options remain open"）
- 2026-07-30｜Phong Le｜capital_allocation：不排除調降 STRC 利率與調整 ATM 發行（原話："We could adjust the rate down from 12% to 11% to 10%"）
- 2026-07-30｜Phong Le｜capital_allocation：可管理 ATM 發行節奏（原話："We could manage the ATM issuance, right?"）
- 2026-07-30｜Michael Saylor｜capital_allocation：資產配置不再 100% BTC（原話："I don't think it will be 100% in the future."）
- 2026-07-30｜Phong Le｜capital_allocation：Phong 談左腦比特幣多頭的教訓（原話："we shouldn't let our left brain Bitcoin bull"）
- 2026-07-30｜Phong Le｜capital_allocation：Phong 表示高幣價時可考慮降息（原話："reducing the rate when we see a strong Bitcoin price"）
- 2026-07-30｜Phong Le｜capital_allocation：Q1 說法延伸：由單向發行轉主動資本管理（原話："We went from one-way capital issuance"）
- 2026-07-30｜Michael Saylor｜commitment：不採用比特幣質押借款（原話："it's not on the table right now"）
- 2026-07-30｜Michael Saylor｜commitment：避免保證金式負債（原話："avoid any kind of appearance of a margin debt"）
- 2026-07-30｜Michael Saylor｜commitment：現有債務為上限並逐步縮減（原話："the existing amount of debt to be the maximum we have"）
- 2026-07-30｜Michael Saylor｜commitment：不賣出波動率（選擇權）（原話："right now, that's not part of the plan"）
- 2026-07-30｜Michael Saylor｜commitment：對衍生品交易商承諾不競爭、不改凸性（原話："we won't compete with you, and we won't change the convexity"）
- 2026-07-30｜Michael Saylor｜guidance：每 $1 資本每年可賣 $0.10–0.20 信用（原話："we can sell $0.10 to $0.20 of credit per year"）
- 2026-07-30｜Phong Le｜guidance：目標七年內讓每股比特幣翻倍（原話："double Bitcoin per share in 7 years through digital credit"）
- 2026-07-30｜Phong Le｜guidance：7 月迄今普通股發行約 $1.3B（原話："we've issued about $1.3 billion of common equity"）
- 2026-07-30｜Andrew Kang｜margin：放大倍數口徑（原話："Amplification represents our total Bitcoin as a multiple"）
- 2026-07-30｜Andrew Kang｜margin：淨槓桿口徑（原話："a low net leverage of 5.4%"）
- 2026-07-30｜Andrew Kang｜margin：年初至今 BTC yield（原話："Year-to-date BTC yield is currently 4.5%"）
- 2026-07-30｜Andrew Kang｜margin：Q2 BTC yield 對 Q1（原話："BTC yield of 5% outperformed the Q1 BTC yield of 3.2%"）
- 2026-07-30｜Andrew Kang｜margin：Q2 EPS（原話："an EPS of negative $24.45 per share"）
- 2026-07-30｜Phong Le｜margin：每年股息與利息支出（原話："interest payments of $1.76 billion currently annually"）
- 2026-07-30｜Michael Saylor｜margin：hurdle rate 定義（原話："hurdle rate represents our blended current cost of credit"）
- 2026-07-30｜Michael Saylor｜margin：floor rate 定義（原話："rate the Bitcoin would have to fall on an annualized basis"）
- 2026-07-30｜Michael Saylor｜competition：STRC 對標私募信用、銀行特別股、垃圾債（原話："STRC as competing against private credit and bank"）
- 2026-07-30｜Michael Saylor｜competition：STRC 在三大特別股指數均為第一大持股（原話："STRC is now the #1 holding at all 3"）
- 2026-07-30｜Michael Saylor｜competition：只有兩家公司能賣數位信用（原話："There's only 2 companies in the world right now"）
- 2026-07-30｜Michael Saylor｜product：聚焦整併信用工具（原話："We're laser-focused on consolidation."）
- 2026-07-30｜Michael Saylor｜product：計畫逐步縮減 11 檔信用工具（原話："Our explicit plan is to whittle them down over time."）
- 2026-07-30｜Michael Saylor｜product：重來會只發行 STRC、不發債（原話："I would do no bonds, I would just sell STRC"）
- 2026-07-30｜Michael Saylor｜product：STRC 名目規模成長（原話："to $10.5 billion at the end of Q2"）
- 2026-07-30｜Michael Saylor｜product：官網新增 200 週均線指標（原話："we've also added the 200-week moving average"）
- 2026-07-30｜Michael Saylor｜product：新推銀行採用指數（原話："Bitcoin Banking Adoption Index"）
- 2026-07-30｜Michael Saylor｜risk：Saylor 列五項比特幣逆風（原話："We really think there are 5."）
- 2026-07-30｜Michael Saylor｜risk：Fed 理事投票主張升息（原話："governors actually voted to raise rates"）
- 2026-07-30｜Michael Saylor｜risk：STRC 跌至 70 的成因：二三階信用額度收回（原話："third order reflexive contraction in credit in the system"）
- 2026-07-30｜Michael Saylor｜risk：Saylor 否認為 DeFi 清算（原話："so it wasn't DeFi, by the way."）
- 2026-07-30｜Phong Le｜risk：2026 最大教訓：持有流動美元（原話："the importance of holding liquid U.S. dollars"）
- 2026-07-30｜Phong Le｜risk：2022 教訓：避免有契約與保證金的債（原話："was don't do either of those"）
- 2026-07-30｜Michael Saylor｜customer：STRC 機構持有比重上升（原話："holdings had grown from $1.1 billion to $3.1 billion"）
- 2026-07-30｜Michael Saylor｜customer：STRC 持有人結構（原話："78% of STRC was held by retail and 22% by institutional"）
- 2026-07-30｜Andrew Kang｜customer：新增兩家分析師覆蓋（原話："We added 2 new covering analysts from Barclays and Siebert"）
- 2026-07-30｜Andrew Kang｜customer：分析師平均 MSTR 目標價（原話："The average MSTR price target is approximately $296"）

### 問答異常語氣（迴避／改口／保留）
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Barclays：是否將美元準備金最低門檻由 12 個月提高到 18–24 個月｜答法：Phong 先說會考慮，隨即改口一年是好的位置，轉談實際準備金金額與使用承諾，未給是否調高的結論
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Mark Palmer：是否以比特幣質押借款補美元準備金｜答法：Phong 說曾與多家對手方洽談，又說沒有認真研究過；Saylor 接著說目前不在檯面上但保留未來選項
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：Lance Vitanza：哪些原則是基礎、哪些隨市況調整｜答法：Saylor 只談 STRC 不低於面值，未回答如何區分基礎原則與可變原則
- MSTR_Q2_2026_Earnings_Call_20260730.md｜問：STRC 回面值需要多少資金與時間｜答法：Saylor 表示無法保證需要多少美元或多少天，只給 $1B 授權、9/8 類比時點與「花多少都花」的說法

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 1 | 1 |
| geo_supply_chain | found | 1 | 1 |
| end_markets | found | 2 | 2 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 6 | 3 |
| major_events | found | 3 | 3 |
| financial_capital_credit_cycle | found | 5 | 2 |
| financial_regulatory_capital_rules | none | 0 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）
- **financial_regulatory_capital_rules**（none）：Strategy MSTR regulatory capital requirement bitcoin treasury company 2026；Strategy MSTR bitcoin treasury company regulatory capital rules Basel bitcoin crypto exposure standard 2026；Strategy Inc MSTR MSCI index exclusion digital asset treasury companies decision 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260819","verdict":"迴避","role":"不持有","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"權益mNAV連續8週≥1.15x 且 BTC/股連2季QoQ回正 且 2028 put wall（$67.1億六檔轉債本金，2027-09至2028-06陸續到期）完成再融資且淨稀釋<15% 且 MSCI未將MSTR排除出現有指數 → 由迴避重審至觀望","irr_base_pct":15.9,"ev5y_pct":145.1,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有","signal":"X","val":"🟠","ma":"❌","trap":"🔴","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":4.52,"ev5y_pct":145.1,"irr_base_pct":15.9,"max_dd_pct":-93.0,"bull_5y_price":625.0,"bear_5y_price":9.41,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"權益mNAV連續8週≥1.15x 且 BTC/股連2季QoQ回正 且 2028 put wall（$67.1億六檔轉債本金，2027-09至2028-06陸續到期）完成再融資且淨稀釋<15% 且 MSCI未將MSTR排除出現有指數 → 由迴避重審至觀望","price_at_dd":105.31,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MSTR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Strategy Inc"},"oneliner":"Strategy 是用 12% 優先股換比特幣的槓桿持幣公司，持有 84.85 萬枚 BTC；資產負債表明顯轉強，但每股 BTC 年初至今 −3.7%、股價約為淨資產 1.06 倍、週線仍在 250 週均線下，等每股 BTC 重新成長再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSTR_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是比特幣漲幅減去約 12% 信用成本的利差，不是軟體：Q3 軟體營收 1.254 億美元，剔除數位資產後營業結果約 −260 萬美元，209 億美元營業利益幾乎全是比特幣公允價值利得；錢卡在「能否以高於淨資產的價格持續發行普通股與優先股」這一節點","reasoning":"營收面：軟體營收 2022–2025 年在 4.6–5.0 億美元之間打轉，Q3 年減 3%；毛利率由 2022 年 79.4% 降到 2025 年 68.7%，Q3 為 71%。地端授權 2026-12-31 結束主流支援（延伸支援到 2028 年底），雲端訂閱 Q2 年增 54%，但軟體不決定股價。股東價值＝（84.85 萬枚 BTC＋約 51 億美元美元資產−67 億美元可轉債−133 億美元優先股名目）×市場給的溢價；公司口徑 10-23 淨準備約 539 億美元，對照市值 571.5 億美元約 1.06 倍（比特幣以 10-23 價格計，11-02 比特幣價格本包未涵蓋）。運作方式：發行 STRC（票息 12%）等優先股買幣，比特幣年漲幅超過綜合信用成本 10.6% 的部分歸普通股，低於 2.2% 就要靠賣幣或增資付息（2026-10-29 法說，Phong Le）。產業時鐘判在復甦（I）：依據不是股價，而是 STRC 由 6 月約 $75 回到 $99.99、美元準備由約半年拉到 3.4 年、淨槓桿 8.4%→2.4%，但信用發行尚未重啟。供需持久度：屬週期性、可逆性高，持幣公司今年買進約 22 萬枚、相當新挖量 165%（Saylor），STRC 被單一來源稱為 2026 年邊際買盤主力，這股需求靠溢價與信用發行撐，溢價消失就會反轉。單點依賴：公開市場籌資能力；STRC 持有人 3/17 口徑約 80% 散戶，近 6 個月高資產個人占比 24%→29%、機構 21%→23%。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_gaap_operating_income","f_kpi2_operating_result_excludi","f_kpi3_gross_profit_margin","f_kpi4_net_income_to_common_dil","f_kpi5_btc_holdings","f_kpi6_btc_yield_ytd","f_earnings_recency","f_shares_diluted_m","f_ev_m"],"verdict_values":{"revenue_quality":"低：軟體營收四年零成長、毛利率年度連三年下滑，且對每股價值不承重；EPS 由比特幣公允價值主導，與營收脫鉤","unit_econ_note":"每股淨資產＝公司口徑淨準備 539 億美元 ÷ 4.2357 億股 ≈ $127；若用公司每股 sats（187,700）隱含的約 4.52 億股則約 $119，現價溢價 6%–13%","archetype":{"primary":"金融","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"資產負債表就是產品：比特幣存量加上優先股發行利差，軟體營收不承重"},"industry":{"clock_phase":"I","sd_verdict_source":"週期性、供給可逆性高：持幣公司 2026 年買進量達新挖量 165%（2026-10-29 法說，Saylor）；STRC 被稱為 2026 年比特幣邊際買盤主力且約八成散戶（inter.capital，單一來源，2026-05-18）；需求靠普通股溢價與信用發行撐，溢價一消失即可逆","bargaining":{"up":"資金提供者強勢：STRC 要把票息拉到 12%、加上約 20 億美元買回才回到面值，信用成本由投資人決定","down":"軟體客戶議價力高：對手是 IBM、Microsoft、Oracle、Salesforce、SAP，地端授權即將停止主流支援，客戶可趁轉雲端時換供應商","geo":"不適用實體供應鏈；歐洲上市的 STRE 掛在非監管市場、不能賣給散戶，屬監管通路限制"},"profit_pool_dir":"利潤池由持幣公司的普通股溢價流向優先股持有人與現貨 ETF：多頭期 mNAV 中位數 2.28–2.60 倍，現在 1.15 倍；同期 STRC 票息拉到 12%","tam_table":[{"item":"數位信用市場規模","value":"約 160 億美元；Phong Le 稱 6 家發行人、Saylor 稱 4 家，同場說法不一（2026-10-29 法說）"},{"item":"Strategy 優先股名目","value":"約 131–133 億美元（9-30／10-23，Andrew Kang），約占數位信用市場八成"},{"item":"比特幣占全球資本資產","value":"約 0.1%（Saylor，未附出處）"},{"item":"5 年利潤池占比變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向往下：持幣規模與 STRC 流動性仍是同業最大，但把這項優勢換成股東報酬的管道，也就是普通股溢價與每股 BTC 成長，正在變窄","reasoning":"執行力 6 分：2026 年在比特幣空頭中仍募到 212 億美元，STRC 由約 $75 拉回 $99.99、美元準備 3.4 年、BTC 零質押，屬修復到原位而非擴大。定價力 4 分：STRC 票息拉到 12% 才穩住，綜合信用成本 10.6%；普通股溢價由 2024 年多頭中位數 2.60 倍降到 1.15 倍；法說分析師提問稱 Q3 經 ATM 賣出逾 50 億美元普通股、多數用於補現金與買回 STRC，管理層未反駁，BTC Yield 年初至今由 7 月底的 +4.5% 轉為 −3.7%。同業報酬率差距無法計算（投入資本口徑事實表未涵蓋），改用溢價與每股 BTC 當可比軸，兩者都在縮。報酬持續期：軟體本業屬低利益率×低周轉（TTM 營益率約 −11%）；持幣部分的增量報酬以 BTC Yield 代理，年初至今為負，內生成長上界取 0%。四項持續期檢查中，決策層級與價值鏈分配為紅燈。產業態勢屬雙向拉鋸：競爭面惡化（ETF 與其他持幣公司搶同一批資金，Blockworks 稱 ETF 資金流已比 Strategy 買幣更能決定價格）；結構面轉好（銀行採用度 24%→34%，本季財政部、SEC、CFTC 指引轉友善，Saylor）；其他變數在監管與通路（Nasdaq 被報導勸阻上市公司參與代幣化、STRE 困在歐洲非監管市場）。重大事件：財務長 11-05 離任，列紅色威脅。","fact_refs":["f_peer_mstr_gross_margin_pct","f_peer_mstr_operating_margin_pct","f_peer_mstr_fcf_margin_pct","f_peer_coin_operating_margin_pct","f_peer_coin_fcf_margin_pct","f_peer_mara_operating_margin_pct","f_peer_3350_t_operating_margin_pct","f_peer_glxy_operating_margin_pct","f_kpi6_btc_yield_ytd","f_kpi5_btc_holdings"],"verdict_values":{"moat":{"mechanism":"規模與先行者：84.85 萬枚未質押 BTC 加上 STRC 的流動性（全球交易量最大的優先股、PFF 第一大持股），讓公司能以單一發行人身分大量發行數位信用；這項優勢的經濟表現是普通股溢價，目前已壓縮到約 1.15 倍","execution":6,"pricing":4,"grade":"C","trend":"↓","trend_evidence":"定價力縮減：STRC 票息拉到 12% 才回到面值、綜合信用成本 10.6%，普通股溢價中位數由 2024 年 2.60 倍降到 1.15 倍，Q3 增資款多數拿去補美元準備與買回 STRC，BTC Yield 年初至今由 +4.5% 轉為 −3.7%；執行力只是回到原位：STRC 由 $75 拉回 $99.99、淨槓桿 8.4%→2.4%。軟體端 Q3 營收年減 3%","competitor_notes":[{"name":"COIN","strategy_note":"交易所與託管商，TTM 營益率 5.7%、FCF 利潤率 68%，靠交易與服務費賺錢；與 Strategy 爭的是想要比特幣曝險的資金，同時是比特幣安全聯盟成員"},{"name":"MARA","strategy_note":"礦商兼持幣，TTM 營益率 −126%，同樣靠資本市場籌資買幣，是爭奪同一批持幣股資金的直接對手"},{"name":"3350.T","strategy_note":"日本上市的持幣同業，毛利率 99%、營益率 70%，損益來源事實表未說明，不宜直接比較；與 Strategy 爭的是全球持幣股資金"},{"name":"GLXY","strategy_note":"數位資產金融服務與交易，TTM 毛利率與營益率接近零；同為比特幣安全聯盟成員，偏生態夥伴而非直接對手"}],"spread_notes":null,"peer_na_reason":"同業投入資本口徑事實表未涵蓋；持幣公司的資產主體是比特幣、損益由公允價值主導，本業 ROIC 不具可比性，改用普通股溢價與每股 BTC 成長當可比軸","threats":[{"level":"🔴","text":"現貨 ETF 與其他持幣公司搶同一批想要比特幣曝險的資金，普通股溢價壓縮就是結果；ETF 資金流已比 Strategy 買幣更能決定價格；公司 10-K 也承認募資時與 ETP、礦商、其他持幣公司競爭，競爭加劇會推高融資成本","p":"40%","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"level":"🟡","text":"企業分析軟體面對 IBM、Microsoft、Oracle、Salesforce、SAP 與 AI 整合競爭，Q3 營收年減 3%，地端授權 2026 年底結束主流支援；軟體不承重，不扣分","p":"50%","evidence_refs":["competitive_share_entrants#0","end_markets#0"]},{"level":"🔴","text":"財務長 Andrew Kang 11-05 離任（公司稱個人因素），CEO Phong Le 暫兼，2027-01 起財務長拆成軟體與比特幣兩位；資本結構是本業核心，主導信用框架與準備金政策的人在信用發行尚未重啟時離開","p":"25%","evidence_refs":[]},{"level":"🟡","text":"AI 驅動攻擊與量子運算可能削弱傳統密碼技術；公司以產業安全聯盟協調應對，屬長期技術風險","p":"5%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉（軟體本業，TTM 營益率約 −11%，約 5 億美元營收對上 700 億美元以上資產）；持幣部分不適用 ROIC，改看 BTC Yield 與綜合信用成本","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者是同一批人（想要比特幣曝險或高殖利率的投資人），需求真實但屬想要而非需要：STRC 6 月跌到約 $75 時資金撤出，Phong Le 在 Q3 法說承認是募得太快、吸進不健康的資金"},{"item":"決策層級","level":"🔴","text":"在投資人做選擇的最小單位，替代品多且轉換成本接近零：要曝險可直接買現貨 ETF，要殖利率可買其他發行人的數位信用；溢價一高就流失，代理變數是 mNAV 由 2.60 倍降到 1.15 倍"},{"item":"價值鏈分配","level":"🔴","text":"價值鏈上最難取代的是比特幣本身與提供資金的信用投資人：STRC 票息拉到 12%、綜合信用成本 10.6%，比特幣報酬低於這條線時超額報酬歸信用端；Q3 增資款多數用於美元準備與買回 STRC，普通股每股 BTC 下降"},{"item":"社會容忍度","level":"🟡","text":"本季美國監管轉友善（財政部、SEC、CFTC 指引，Saylor 2026-10-29），但通路仍受政策左右：Nasdaq 被報導勸阻上市公司參與代幣化，歐洲上市的 STRE 在非監管市場不能賣給散戶；優勢依賴監管態度，政策可逆"}],"roiic":"約 −3.7%（以 BTC Yield 年初至今代理：2026 年募資 212 億美元後每股 BTC 不升反降）","reinvest_rate":"不適用：剔除數位資產後 NOPAT 約為零（Q3 營業結果約 −260 萬美元），分母無意義；募資幾乎全數再投入比特幣、美元準備與買回優先股","endo_ceiling":0,"formula_note":"內生成長＝增量報酬×再投資率；增量報酬為負、本業 NOPAT 約零，剔除比特幣價格後的內生每股成長上界取 0%，每股價值成長全靠比特幣價格與溢價"}}}},"q3_growth":{"verdict":"五年後跑道中等：比特幣與數位信用的潛在市場大，但 Strategy 已占數位信用約八成、普通股溢價壓縮，成長要靠市場本身擴大與溢價回升，沒有已證實的第二條曲線","reasoning":"成長是資產價格加上發行利差，不是量、價或併購。共識 EPS 由 FY2025 實際 −15.23 美元到 FY2028 預估 23.77 美元，基期為負，三年 CAGR 無法計算，且全部來自比特幣公允價值假設；兩份快照間修正幅度皆為 0，快照可能未更新。內生上界引報酬持續期推導為 0%，共識與內生上界的缺口無法歸因到利潤率、回購或收購，屬依賴資產重估，長期信心上限為中。跑道：比特幣只占全球資本資產約 0.1%（Saylor），數位信用市場約 160 億美元；Strategy 份額已約八成，擴張空間有限；代幣化對美國投資人尚無自家產品，Saylor 稱未來 12 個月才可能出現標準，不算已證實的第二曲線。軟體營收 FY2026、FY2027 共識 5.01 億、5.15 億美元，近乎零成長。衰退信號亮 3 項，長期成長性紅燈。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_btc_yield_ytd","f_kpi0_revenue_gaap"],"verdict_values":{"growth":{"driver_mix":"比特幣價格（主）＋以優先股與普通股增發換幣的利差（次）＋軟體（可忽略）","runway_years":"不適用：持幣公司沒有滲透率曲線，跑道取決於數位信用市場擴大與普通股溢價","runway_post_y5":"🟡","endo_ceiling_basis":"引用報酬持續期推導：增量報酬（BTC Yield 年初至今 −3.7%）×再投資率（本業 NOPAT 約零，無意義）→ 內生每股成長上界 0%；共識 FY2027–FY2028 EPS 23.67／23.77 美元超出上界，缺口無法歸因","segments":{"expanded":false,"reason":"損益由比特幣公允價值決定，軟體分部合計 Q3 毛利 8,960 萬美元、扣營業費用後約損益兩平，不影響每股價值方向；分部細項事實表未涵蓋"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":null,"evidence":"年度連三年下滑（79.4%→77.9%→72.1%→68.7%），單季年減事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":null,"evidence":"BI 市占數據查無，各來源估計差異大"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"不適用：STRC 調高票息是為了穩價，不是提價"},{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"evidence":"共識 EPS 由負轉為約 +23.7 美元，營收 FY2026→FY2027 只增 3%，差距全由比特幣公允價值造成"},{"signal":"FCF/NI 連 2 年 <0.75","lit":null,"evidence":"不適用：FCF 含買幣支出（2025 年約 −225.8 億美元），淨利亦為負，比值無意義"},{"signal":"SBC/營收 >5% 且逐年上升","lit":null,"evidence":"SBC 事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"現貨 ETF 取代持幣股成為比特幣曝險管道；軟體端地端授權停止主流支援"},{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"mNAV 中位數 2023 年 2.57、2024 年 2.60，現在 1.15"},{"signal":"維護性資本支出占 FCF >60%","lit":false,"evidence":"不適用"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"營收 2025 年 +3%，未連續下滑"}],"trap_rating":"🔴"}}},"q4_capital":{"verdict":"資本配置偏向保信用、犧牲每股 BTC：普通股買回為零、沒有併購，Q3 增資主要拿去補美元準備與買回 STRC，每股 BTC 年初至今 −3.7%；三項計分全數未過","reasoning":"現金去向（2026 年至 10 月）：募資 212 億美元，買幣約 17.6 萬枚；美元資產由約 25 億美元拉到 51–58 億美元；買回 STRC 約 20 億美元（尚餘 9.57 億美元授權）；5 月以約 13.8 億美元現金買回 15 億美元 2029 年可轉債（折價約 8%）；另以約 2.18 億美元賣幣支付部分優先股股息（Q2 新聞稿）。普通股買回授權 10 億美元未動用，Q2 法說訂的條件是股價低於每股淨比特幣，目前未觸發。可轉債維持 67 億美元，與 Saylor 在 Q2 說的現有債務為上限一致。FCF 對淨利轉換率不適用（FCF 含買幣支出、淨利由公允價值主導）。股息與利息約 17.6 億美元／年（Q2 法說口徑），美元資產覆蓋 3.4 年。管理層的選擇很清楚：用股東稀釋換信用安全，代價是今年每股 BTC 下降。","fact_refs":["f_kpi6_btc_yield_ytd","f_kpi5_btc_holdings","f_net_debt_m","f_shares_diluted_m","f_peer_mstr_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購；2026-03-23 的 8-K 為發行協議修訂與 STRC 授權股數增加，非併購"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"普通股買回授權 10 億美元尚未動用，普通股買回收益率為 0；買回的是 STRC 約 20 億美元與 2029 年可轉債 15 億美元"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"SBC 金額事實表未涵蓋；但普通股以 ATM 大量增發（Q3 逾 50 億美元），且增資款未換成比特幣，每股 BTC 年初至今 −3.7%，淨稀釋遠超每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；資本去向集中在買幣、美元準備、買回優先股與可轉債，已寫在判斷理由"}}}},"q5_valuation":{"verdict":"現價約為公司口徑淨資產的 1.06–1.13 倍；要划算，比特幣得長期跑贏 10.6% 的綜合信用成本，而且溢價要回升。前者有歷史支持，後者在 ETF 競爭下我不信，估值只算合理、不便宜","reasoning":"主錨用淨資產倍數。市值 571.5 億美元（11-02 收盤 $134.93 × 4.2357 億股）對公司口徑 10-23 淨準備 539 億美元＝1.06 倍；用公司每股 sats 隱含的 4.52 億股則約 1.13 倍。11-02 的比特幣價格本包未涵蓋，倍數有日期錯位。合理倍數：若比特幣年報酬約 10%（公司自己引用的 JPMorgan 假設），與 10.6% 綜合信用成本相當，普通股沒有超額報酬，合理倍數約 1.0 倍；現價略高於此，落在合理區間。營收倍數分母有爭議，只作程式口徑對照：P/S 115.4 倍、trailing EV/S 117.2 倍，在 4 個年度端點內分位 81.3／73.4，不是五年分位。賣方目標價中位數 $233、平均 $257.5，全距 $125–$550（4.4 倍），分散過大，不作為錨。短期空間取至每股淨資產（約 −5.7%），中期取 Base 情境 5 年終值（約 +51%）。","fact_refs":["f_price_at_dd","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_net_debt_m","f_shares_diluted_m","f_rev_consensus_fy1_m","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2"],"verdict_values":{"valuation":{"basis":"淨資產倍數（比特幣＋美元資產−可轉債−優先股名目）為主錨；營收倍數分母有爭議，只作程式口徑對照","peers":{"expanded":false,"reason":"同業 EV/S 與淨資產倍數事實表未涵蓋；同業表只有利潤率，持幣公司之間的可比尺是淨資產倍數，本包取不到"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"輸入：市值 571.5 億美元、公司口徑淨準備 539 億美元（10-23）→ 1.06 倍；合理倍數＝（權益報酬−g）÷（資金成本−g），比特幣 10% 年報酬對上 10.6% 綜合信用成本時超額報酬約為零，合理倍數約 1.0 倍 → 現價溢價約 6%，屬合理；五年分位不可得（只有 4 個年度端點且分母有爭議），PEG 因基期 EPS 為負不適用","targets":{"sell_side_median":233,"sell_side_mean":257.5,"sell_side_range":"125–550","company_cited_mean":248,"note":"公司稱 17 位分析師全數買進、平均目標價約 $248（Q3 法說），Q2 法說時為約 $296；全距 4.4 倍，超過 2.5 倍"},"upside_short_pct":-5.7,"upside_mid_pct":51.3,"denominator_disputed":true,"denominator_note":"營收倍數的分母是約 5 億美元軟體營收，股價卻由約 690 億美元比特幣決定；事實表 EV 又未計入約 131 億美元優先股名目，計入後前瞻 EV/S 約為（58,023＋13,100）÷500.56＝142 倍。這把尺無法支持便宜或昂貴的論證，本題改以淨資產倍數判斷"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是太保守：若比特幣進入多頭、溢價回到過去多頭中位數 2.3–2.6 倍，普通股會大幅跑贏；但這需要兩件事同時發生，現有證據只支持資產負債表變安全，不支持每股 BTC 重新成長","reasoning":"三視角反證與矛盾裁定寫在反證紀錄。壓力測試五項過三項：①比特幣跌 50%，資產對負債覆蓋由 4.6 倍降到約 2.3 倍（過）②比特幣跌約 78% 到 $17,662 才到 1 倍覆蓋（過）③美元準備 ≥1 年（3.4 年，過）④2028 年回售前的再融資方案（未公布，不過）⑤溢價跌破 1 倍時不稀釋股東（Q3 在 1.1 倍附近增資且每股 BTC 下降，不過）。歷史最大回撤幅度事實表未涵蓋，回撤範圍由比特幣本輪跌幅（約 $124,000→約 $58,700）、1.28 倍放大與溢價壓縮推估。","fact_refs":["f_kpi6_btc_yield_ytd","f_ma_state","f_ma_w250","f_ma_w52","f_week26_return_pct","f_rsi14","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🔴","label":"資產重估依賴：本業沒有內生成長，每股價值全靠比特幣價格與溢價"}}}},"scenario_inputs":{"valuation_basis":"sales_multiple","terminal_label":"FY2031E","start":{"rev":500.56,"ev_s":115.92,"basis":"起點營收取 FY2026E 共識（7 位分析師平均）；起點 EV/S＝事實表 EV（市值＋總債務−現金）÷ FY2026E 營收，未含約 131 億美元優先股。終端 EV/S＝終端年 EV ÷ 同年營收，同為前瞻年度口徑；但終端淨負債把優先股名目當作股東之前的求償權計入，若起點也計入優先股，起點 EV/S 約 142 倍。同業 EV/S 現值事實表未涵蓋，終端倍數只能對照本身現值。EV/S 在此只是把淨資產模型換成營收倍數格式，數字本身無經濟意義"},"rev":{"bull":[530,560,590,620,650],"base":[510,515,520,525,530],"bear":[480,460,440,420,400]},"ev_s":{"bull":543.7,"base":246.8,"bear":91.16},"net_debt_y5":{"bull":33000,"base":28700,"bear":16300},"shares_y5":{"bull":510,"base":500,"bear":550},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"max_dd":{"lo":-90,"hi":-70,"basis":"本輪比特幣由約 $124,000 跌到約 $58,700（−53%，2026-10-29 法說）；普通股對比特幣的放大約 1.28 倍 → 每股淨值約 −68%；溢價由 1.15 倍壓到 0.85 倍再乘 0.74 → 約 −76%；比特幣若跌 65%，同法約 −87%。歷史最大回撤事實表未涵蓋。取 −70% 至 −90%","trigger_time":null},"basis":{"bull":"比特幣年化約 22% 至 2031 年約 $219,500；優先股擴到約 430 億美元，持幣增至約 115 萬枚；可轉債全數轉股、美元準備 100 億美元，求償權淨額 330 億美元；股數 5.1 億；EV 為比特幣淨值 1.4 倍（低於過去多頭中位數 2.3–2.6 倍）","base":"比特幣年化約 10%（公司引用的 JPMorgan 假設）至約 $130,800；優先股增至約 280 億美元、持幣約 100 萬枚；可轉債 67 億美元再融資、美元準備 60 億美元，求償權淨額 287 億美元；增發付股息，股數 5 億（年增約 3.4%）；EV 等於比特幣淨值。比特幣報酬低於 10.6% 綜合信用成本，普通股跑輸比特幣","bear":"比特幣 5 年年化約 −7.5% 至約 $55,000；STRC 無法重啟，賣幣付股息並應付 2028 回售，持幣降到約 78 萬枚；優先股 133 億美元、可轉債剩 40 億美元、美元準備 10 億美元，求償權淨額 163 億美元；以低於淨值增資，股數 5.5 億；EV 為比特幣淨值 0.85 倍。不採信「比特幣每個 4 年窗口都高於 2.2%」作為壓低機率的理由：樣本約 11 年且窗口重疊、獨立觀察很少，過去也沒有 12% 固定求償權結構"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"公司自己的門檻：比特幣年報酬低於 10.6% 時超額報酬歸信用端，低於 2.2% 就要賣幣或增資付息，年跌 17.4% 時覆蓋降到 1 倍（2026-10-29 法說，Phong Le）；6 月 STRC 跌到約 $75，Saylor 歸因於系統內信用額度連鎖收縮；目前信用市場壓力集中在軟體槓桿貸款（占市場 13%、占困境貸款 31%），Morgan Stanley 預估私募信貸違約率升到 8%；Pepperstone 指出若無法再融資，未來可轉債需求恐大減","assumption":"比特幣長期年化 ≥10.6%，且信用市場不再出現足以讓 STRC 跌破面值的收縮","consequence":"5 年虧 50% 以上最可能的路徑：比特幣橫盤或下跌，加上信用收縮讓 STRC 停發、溢價轉折價，公司以低於淨值增資付 12% 股息，每股 BTC 持續下降；最後一步就是唯一致命點（股息暫停），兩者部分重疊，致命點是這條故事的末端","ruling":"採納，為 Bear 情境主路徑，機率 30%。軟體信貸壓力與 Strategy 沒有直接借貸關係（公司負債是可轉債與永續優先股），只透過整體信用情緒間接傳導，證據強度中等","watch":"STRC 週收盤價、mNAV、比特幣 4 年滾動年化報酬對 10.6%","evidence_refs":["financial_capital_credit_cycle#3","financial_capital_credit_cycle#4","supply_demand_durability#2"],"fact_refs":["f_kpi6_btc_yield_ytd"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 比特幣漲 43%、普通股漲 76%，但 BTC Yield 年初至今由 7 月底 +4.5% 轉為 −3.7%；分析師提問稱 Q3 經 ATM 賣出逾 50 億美元普通股、多數用於補現金與買回 STRC，管理層未反駁；今年已賣約 2.18 億美元比特幣支付部分優先股股息；STRC 票息拉到 12%","assumption":"比特幣上漲的好處會留在普通股","consequence":"信用平台救回來了，代價由普通股承擔：每股 BTC 下降、股息與利息約 17.6 億美元／年，比特幣只要表現平平，普通股就跑輸直接持有比特幣","ruling":"採納，這是本次不建倉的主因；Phong Le 說下一輪 STRC 募資部分轉入美元準備、其餘買幣，若做到，每股 BTC 可回升","watch":"每季 BTC Yield、STRC 淨發行額、普通股增資用途","evidence_refs":["financial_capital_credit_cycle#2"],"fact_refs":["f_kpi6_btc_yield_ytd","f_kpi5_btc_holdings"]},{"view":"價格已反映太多","evidence":"賣方 17 位全數買進、平均目標價約 $248（Q3 法說）；但 6–7 月 TD Cowen、Citi、Mizuho 已下調目標價，Citi 降到 $136；次一財年 EPS 90 天修正 −88%（僅 1 位分析師樣本）","assumption":"現價已計入比特幣多頭與溢價回升","consequence":"若賣方預期中的比特幣（平均約 $111,000）與溢價回升沒有發生，目標價會再下修","ruling":"價格面反駁、預期面採納：現價只比淨資產高 6%–13%，沒有反映太多多頭；但賣方目標價反映太多。EPS 修正只有單一分析師樣本，不作承重證據","watch":"賣方平均目標價與比特幣目標價的變動、mNAV","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_price_at_dd","f_consensus_rev_fy2_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 105.31 → 本次 134.93（+28.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=105.31","side_b":"本次 price_at_dd=134.93","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 105.31 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 105.31 美元：Bull 價 625、Bear 價 9.41，五年期望值 +145.1%，基準年化 15.9%，不對稱比 4.52","side_b":"本次情境、股價仍用 105.31 美元：Bull 價 628.25、Bear 價 36.66，五年期望值 +146.8%，基準年化 14.2%，不對稱比 6.35","ruling":"先換情境、股價不動：五年期望值多 1.7 個百分點，基準年化少 1.7 個百分點。不對稱比由 4.52 變為 6.35。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 105.31 美元：五年期望值 +146.8%，基準年化 14.2%，不對稱比 6.35","side_b":"本次情境、股價 134.93 美元：五年期望值 +92.7%，基準年化 8.6%，不對稱比 4.18","ruling":"再換股價、情境不動：起點價上漲 28.1%，五年期望值少 54.2 個百分點，基準年化少 5.5 個百分點，不對稱比由 6.35 降到 4.18。合計五年期望值比前份少 52.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：信用風險下降、上一季承諾兌現","cause":null,"side_a":"Q2 法說（2026-07-30）Phong Le：美元準備最低 1 年、目標 2–3 年；Saylor：現有債務為上限、STRC 一定回到面值、不會暫停股息","side_b":"Q3 法說（2026-10-29）：美元準備 3.4 年、可轉債維持 67 億美元、STRC 收在 $99.99、兩年 40 次股息全數照付；淨負債約 8.7 億美元","ruling":"一致：償債與流動性風險明顯下降，這是品質訊號上調一級的依據","evidence_level":"公司財報與法說原話，兩季對照"},{"axis":"股東價值：管理層稱 Q3 極強，每股 BTC 卻下降","cause":null,"side_a":"管理層：Q3 是各業務都極強的一季，目標 7 年內每股 BTC 翻倍（Andrew Kang、Phong Le，2026-10-29）","side_b":"BTC Yield 年初至今 −3.7%，Q2 法說時為 +4.5%；Q3 增資款多數未換成比特幣","ruling":"性質：不可調和（方向相反）。選資料側：每股 BTC 是普通股唯一的價值累積指標，Q3 的紀錄利得來自比特幣價格，不是公司創造；7 年翻倍需年化約 10.4%，今年為負。裁決已選邊，論點不因此懸而未決","evidence_level":"公司新聞稿口徑","settle_metric":"每季 BTC Yield","if_then":["若 FY2026 Q4 與 FY2027 Q1 BTC Yield 皆為正且 STRC 恢復淨發行：重跑研究，通過才以 ≤1% 試單起步","若股價先漲回 250 週均線之上、BTC Yield 仍為負：不追","反向：若 Q4 BTC Yield 仍為負且普通股繼續增發補準備：維持不持有，重審條件由連 2 季改為連 3 季"],"evidence_refs":["financial_capital_credit_cycle#2"]},{"axis":"STRC 失序原因：外因或自招","cause":null,"side_a":"Q2 法說 Saylor：系統內二、三階信用額度收回，不是 DeFi 清算；並以 IPO 後 70 個交易日類比，推算 9/8 前後回到面值","side_b":"Q3 法說 Phong Le：8 個月由 25 億美元募到 105 億美元，可能募太快、吸進不健康的資金；實際花約 4 個月才回到面值，晚於 9/8","ruling":"可調和（程度差異）。採信 Q3 的自承：STRC 需求有速度上限，重啟發行後要放慢。兩種歸因都未證，標為監測：重啟發行後 6 個月內若再跌破 $95，一次性歸因即證偽","evidence_level":"管理層兩季說法對照","settle_metric":"STRC 重啟發行後 6 個月內週收盤低點","if_then":["若重啟發行後 6 個月內 STRC 週收盤跌破 $95：重審條件全數作廢，維持不持有 4 季","反向：若重啟後連 2 季淨發行 ≥30 億美元且週收盤維持 $99 以上：數位信用需求的持久度改判為中性"]},{"axis":"財務長離任：個人因素或治理訊號","cause":null,"side_a":"公司：Andrew Kang 因個人因素 11-05 離任，交接對股東無縫（Phong Le）","side_b":"資本結構是本業核心，主導信用框架、準備金與可轉債處理的人，在 STRC 剛回面值、信用發行尚未重啟時離開；2027-01 起財務長拆成兩人","ruling":"不可裁決至 2027 年中：公司歸因不採信也不否定，列紅色威脅並監測。消息不到一季，是否已進賣方模型本包未涵蓋；本次未持有，不涉倉位調整","evidence_level":"公司公告，單一事件","settle_metric":"2027 年內財務與資金主管異動、BTC Yield 等自訂指標定義是否改變","if_then":["若 2027 年內再有財務或資金主管離任，或自訂指標定義改變：品質訊號降回 X，重審條件凍結 4 季","反向：若 FY2026 年報與 FY2027 Q1 揭露口徑不變、信用發行順利重啟：此項威脅降為黃色"]},{"axis":"本次比賣方共識悲觀","cause":null,"side_a":"賣方：17 位全數買進，平均目標價約 $248（Q3 法說）、中位數 $233，全距 $125–$550","side_b":"本次：不建倉，Base 5 年終值約 $204、年化約 8.6%","ruling":"分歧在框架層：賣方多以比特幣目標價（平均約 $111,000）乘上溢價推算，本次把約 12% 優先股成本與 10.6% 綜合信用成本放進普通股報酬。市場錯在假設比特幣上漲必然放大到普通股。目標價全距 4.4 倍，超過 2.5 倍，本次情境的年化報酬與正不對稱數字同步下調信心。前份以來股價漲 28%，未達需說明翻面的門檻，本次也不翻面","evidence_level":"賣方彙整網站與公司引述","settle_metric":"賣方平均目標價與 BTC Yield","if_then":["若賣方平均目標價續降至 $200 以下而 BTC Yield 轉正：分歧消失，重跑研究","反向：若比特幣上漲但 BTC Yield 仍為負、賣方仍上調目標價：維持不持有、不追"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"比特幣自 200 週均線反彈、Q3 ETF 淨流入約 63 億美元、銀行採用度 34%；BTC 零質押、資產覆蓋 4.6 倍、1 倍覆蓋的比特幣價格約 $17,662；溢價只有 1.15 倍，等於用接近淨值買 1.28 倍放大，再附送溢價回到多頭中位數 2.3–2.6 倍的選擇權；上一輪多頭（2023–2024）普通股漲 1,897%、比特幣漲 454%","side_b":"放大不是免費：約 133 億美元優先股每年要付約 12%，比特幣報酬低於 10.6% 時普通股跑輸；溢價回升要和現貨 ETF 及其他數位信用發行人搶資金；週線仍在 250 週均線（$139.73）與 52 週均線（$141.15）之下","ruling":"反駁，但承認這是最可能讓本次判斷出錯的地方。正不對稱比率不作進場依據：Bear 錨跟著比特幣價格移動、護城河方向又向下，地板不穩","evidence_level":"公司法說與週線均線","settle_metric":"BTC Yield 連 2 季、週收盤對 250 週均線","if_then":["若 BTC Yield 連 2 季為正且週收盤站上 250 週均線：重跑研究","反向：若比特幣續漲但週收盤仍站不上 250 週均線、BTC Yield 仍為負：不追"]},{"axis":"前份漂移：品質訊號、陷阱、護城河方向、跑道、裁決與角色","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"前份（2026-08-19）：品質訊號 X、價值陷阱紅燈、護城河方向向下、五年後跑道黃燈，裁決迴避、不持有","side_b":"本次：品質訊號 C；陷阱紅燈、方向向下、跑道黃燈不變；裁決與角色由程式依本次輸入重算","ruling":"品質訊號上調一級的新證據：美元準備由約半年拉到 3.4 年、淨槓桿 8.4%→2.4%、STRC 由約 $75 回到 $99.99、6 檔可轉債 4 檔高於面值，現金跑道不足的否決條件已不成立。其餘維持不變的新證據：BTC Yield 年初至今由 +4.5% 轉 −3.7%、溢價仍約 1.15 倍、財務長離任，沒有推翻前份對護城河、陷阱與跑道的判斷","evidence_level":"公司 Q2／Q3 新聞稿與法說"},{"axis":"前份漂移：估值結論、回撤範圍、情境機率、公司類型、循環位置","cause":"方法變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct","archetype","cycle_position"],"side_a":"前份：估值偏貴（橙）、最大回撤 −93%（單點）、Bull 25%／Bear 30%、類型金融、循環位置未設","side_b":"本次：估值合理（黃）、最大回撤 −70% 至 −90%、Bull 25%／Base 45%／Bear 30%、類型金融、循環位置未設","ruling":"估值改以淨資產倍數為主錨（營收倍數分母有爭議）；比特幣由 Q2 季末約 $58,700 漲到 10-23 約 $81,200（+38%），股價自前份 $105.31 到 $134.93（+28%），兩段起點日期不同、前份日比特幣價格本包未涵蓋，只能說溢價方向收斂，故由偏貴轉合理。回撤改用比特幣跌幅×1.28 倍放大×溢價壓縮推導範圍，不再給單點，淨槓桿下降也讓極端值收窄。機率維持前份水準：共識超出內生上界，Bear 不得低於 30%。類型與循環位置不變，持幣公司不套用循環股位置","evidence_level":"本次情境推導"},{"axis":"前份漂移：由迴避重審的條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"權益mNAV連續8週≥1.15x 且 BTC/股連2季QoQ回正 且 2028 put wall（$67.1億六檔轉債本金，2027-09至2028-06陸續到期）完成再融資且淨稀釋<15% 且 MSCI未將MSTR排除出現有指數 → 由迴避重審至觀望","side_b":"BTC Yield 連 2 季為正 且 STRC 週收盤連 8 週 ≥$99 並恢復淨發行 且 週收盤站上 250 週均線 → 由迴避重審","ruling":"舊→新：①mNAV 1.15 倍已在 10-23 觸及（公司口徑），而 Q3 在此倍數附近增資仍稀釋每股 BTC，說明它不是真正的約束，改由 BTC Yield 連 2 季為正直接檢驗；②2028 回售：低於面值的兩檔最早 2028-03 才可回售、美元準備 3.4 年，緊迫性下降，移到清倉與減碼指標並保留淨稀釋 <15% 門檻；③MSCI 納入狀態本包沒有新證據可追蹤，移到指標清單並標資料缺口，門檻不刪；④新增 STRC 恢復淨發行與週線站上 250 週均線，分別對應論點事件與趨勢確認。真正的約束是每股 BTC 不成長，重審條件就是它的否定","evidence_level":"Q2／Q3 法說、週線均線"},{"axis":"前份漂移：清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標（null）","side_b":"本次設 6 條：BTC Yield 全年 <0%；mNAV <1.0 倍連 8 週；STRC 週收盤 <$95 連 2 週；美元準備 <1 年；2028 回售券 2027-12-31 前未公布方案或淨稀釋 ≥15%；MSCI 剔除（資料缺口）","ruling":"前份把門檻全放在重審條件裡，本次拆成重審條件與清倉、減碼指標兩組；舊門檻（淨稀釋 15%、MSCI）保留在指標內，沒有安靜刪除","evidence_level":"方法調整"},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"公司宣布暫停、延後或改以非現金方式支付任一檔優先股股息","ruling":"前份未指定唯一致命點；本次選股息暫停，因為它同時切斷信用發行與普通股溢價兩條價值管道，是對每股價值敏感度最大的單一離散事件；比特幣價格的敏感度更大，但屬連續變數，放在情境樹處理。觸發即清倉","evidence_level":"方法調整"}],"triggers":[{"n":1,"text":"每股 BTC 是否重新成長","type":"假設驗證","maps_to":"H1","metric":"BTC Yield（季，公司口徑）","threshold":"FY2026 Q4 與 FY2027 Q1 連 2 季 >0","action":"兩季皆正且其餘重審條件成立 → 重跑研究；任一季為負 → 維持不持有","source_freq":"公司季報新聞稿，每季","date":"2027-02","evidence_refs":["financial_capital_credit_cycle#2"]},{"n":2,"text":"普通股溢價能否維持在淨值之上","type":"假設驗證","maps_to":"H2","metric":"mNAV（公司口徑）","threshold":"<1.0 倍連 8 週","action":"論點反轉、維持不持有；公司若啟動普通股買回，記錄買回均價對每股淨值","source_freq":"strategy.com，每日","date":null},{"n":3,"text":"優先股市場再度失序","type":"風險","maps_to":"R1","metric":"STRC 週收盤價","threshold":"<$95 連 2 週","action":"若已持有則清倉；未持有則重審條件凍結 2 季","source_freq":"交易所行情，每週","date":null,"evidence_refs":["financial_capital_credit_cycle#2","financial_capital_credit_cycle#3","financial_capital_credit_cycle#4"]},{"n":4,"text":"2028 回售可轉債處理","type":"風險","maps_to":"R2","metric":"回售券處理方案與美元準備年數","threshold":"2027-12-31 前未公布方案且美元準備 <2 年，或方案淨稀釋 ≥15%","action":"若已持有則減碼至 0；未持有則重審條件凍結至方案公布","source_freq":"8-K／10-Q，每季","date":"2027-12-31","evidence_refs":["supply_demand_durability#2"]},{"n":5,"text":"財務長交接後的資本配置與揭露","type":"風險","maps_to":"R3","metric":"財務與資金主管異動、自訂指標定義","threshold":"2027 年內再有財務或資金主管離任，或 BTC Yield 定義改變","action":"品質訊號降回 X、重審條件凍結 4 季","source_freq":"8-K、季報，事件驅動","date":"2027-01"},{"n":6,"text":"訴訟里程碑","type":"風險","maps_to":"R4","metric":"Dodge 集體訴訟與 Rosen 調查進度","threshold":"Dodge 案獲集體認證或不利和解；Rosen 調查轉為正式集體訴訟","action":"若已持有則減碼一半；未持有則在重審時把優先股條款調整受限列入 Bear","source_freq":"10-Q／10-K 訴訟附註，每季","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#2"]},{"n":7,"text":"唯一致命點：優先股股息暫停","type":"Single Thing","maps_to":"single_thing","metric":"每日股息公告、8-K","threshold":"任一檔優先股股息暫停、延後或改非現金支付","action":"清倉；4 季內不重審","source_freq":"STRC 自 11-01 起每日配息，其餘自 2027-01 起每日","date":null},{"n":8,"text":"由迴避重審","type":"估值rearm","maps_to":"rearm_trigger","metric":"BTC Yield、STRC 週收盤與淨發行、週收盤對 250 週均線","threshold":"BTC Yield 連 2 季為正 且 STRC 週收盤連 8 週 ≥$99 並恢復淨發行 且 週收盤站上 250 週均線","action":"三項同時成立 → 重跑研究，通過才以 ≤1% 試單起步","source_freq":"每季／每週","date":null},{"n":9,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"Q4 FY2026 財報","threshold":"財報公布","action":"財報後 2 週內重跑研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"BTC Yield（年度，公司口徑）","bear_threshold":"FY2026 全年 <0%","window":"FY2026（2027-02 財報）","source":"公司季報新聞稿 8-K Ex.99.1","last_status":"warning"},{"metric":"mNAV（公司口徑，EV÷比特幣淨值）","bear_threshold":"<1.0 倍連續 8 週","window":"滾動 8 週","source":"strategy.com 每日 mNAV","last_status":"ok"},{"metric":"STRC 週收盤價","bear_threshold":"<$95 連 2 週","window":"滾動 2 週","source":"交易所行情","last_status":"ok"},{"metric":"美元準備覆蓋年數","bear_threshold":"<1 年（公司自訂下限）","window":"每季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"2028 回售可轉債再融資","bear_threshold":"2027-12-31 前未公布方案，或方案淨稀釋 ≥15%","window":"至 2027-12-31","source":"8-K／10-Q","last_status":"unknown"},{"metric":"MSCI 指數納入狀態","bear_threshold":"被剔除出現有指數","window":"每次指數調整","source":"MSCI 公告（本包未涵蓋，資料缺口）","last_status":"unknown"}],"evidence_dismissed":[{"ref":"$.scenario_inputs.net_debt_y5","reason":"閘自己的複算已經把三條路徑全部對上，內文結論是無實質缺陷，紅燈跟內文矛盾，欄位不改。重算（單位百萬美元）：Bull 543.7×650＝353,405，減求償權淨額 33,000，除 5.1 億股＝$628.25；Base 246.8×530＝130,804，減 28,700，除 5 億股＝$204.2；Bear 91.16×400＝36,464，減 16,300，除 5.5 億股＝$36.66。求償權淨額與敘述逐項相符：Bull 優先股 430 億減美元準備 100 億＝330 億；Base 280＋67−60＝287 億；Bear 133＋40−10＝163 億。終端 EV 與敘述的比特幣淨值也相符：Base 100 萬枚×$130,800＝1,308 億；Bull 115 萬枚×$219,500×1.4≈3,534 億；Bear 78 萬枚×$55,000×0.85≈365 億。三情境加權約 $260，對現價 $134.93 為 +92.7%；Base 終值 204.2÷134.93 開五次方減 1≈8.6%，都和程式輸出一致。起點 EV/S 沒含優先股、終端求償權有含，這個口徑差已寫在起點說明；終值只用終端 EV 減終端求償權，不經過起點倍數，不影響價格"},{"ref":"$.answers.q2_moat.verdict_values.moat.threats","reason":"第三條威脅（財務長離任）的出處是公司公告與 Q3 法說，文字已寫明；本輪可見的證據引用裡沒有記載這次離任的條目，同一事件在 R3 與財務長離任的矛盾條目也都沒有掛引用。硬填一個不相干的編號，讀者會追到錯的證據，所以維持空陣列"},{"ref":"$.counter_evidence.blind_spots","reason":"監管資本規則三條查詢都沒找到證據，沒有內容可以寫成新的反證視角。Strategy 不是銀行，銀行資本規則只透過銀行持有比特幣或放款意願，間接影響比特幣需求；可能直接打到股價的是 MSCI 指數剔除，已經列在清倉與減碼指標並標為資料缺口。再補一個沒有證據的盲點條目，只是把同一個缺口重寫一次"},{"ref":"$.answers.q1_business.reasoning","reason":"日期錯位來自事實表本身：公司口徑淨準備只到 10-23，事實表沒有 11-02 的比特幣價格。商業模式與估值兩段都已註明以 10-23 比特幣價格計、倍數有日期錯位。要對齊日期就得補一個事實表沒有的比特幣價格，這不能做"},{"ref":"$.counter_evidence.contradictions","reason":"歸因欄只用在跟前份比較的漂移條目。一致判斷、管理層說法對照、STRC 失序原因、財務長離任、與賣方分歧、現在就買的論證，這六條是本期正反證據的裁定，不是前份到本次的變動，所以歸因欄留空；填成新證據或方法變動，反而會被當成漂移來源。裁決與角色前後都是迴避、不持有，沒有變動可以歸因；品質訊號那條漂移條目也已寫明裁決與角色由程式依本次輸入重算"}],"action_conditions":{"rearm_trigger":"BTC Yield 連 2 季為正 且 STRC 週收盤連 8 週 ≥$99 並恢復淨發行 且 週收盤站上 250 週均線 → 由迴避重審","exec_line":"不建倉；條件同時成立後重跑研究，通過才以 ≤1% 試單起步，上限 3%（深回撤路徑）","holding_cap":"0%（迴避期間）；重審通過後上限 3%"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":"賣方目標價多以比特幣目標價乘上溢價推算，忽略約 12% 優先股成本：比特幣年報酬低於 10.6% 綜合信用成本時普通股跑輸比特幣，溢價回升又要和現貨 ETF 搶資金","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"迴避","prior_role":"不持有"},"decision_out":{"role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='迴避', 矩陣機械輸出='迴避'"}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[],"verdict":"迴避"},"thesis":{"H":[{"id":"H1","text":"數位信用恢復發行，發行所得換成比特幣，讓每股 BTC 重新成長","2y":"FY2027 全年 BTC Yield ≥ +5%，STRC 恢復淨發行","5y":null,"10y":null,"threshold":"BTC Yield 季度值 >0、年度 ≥ +5%；STRC 淨發行 >0","source":"公司季報新聞稿（8-K Ex.99.1）、STRC 發行 8-K","drift_rule":"連 2 季低於門檻 5 個百分點以上＝削弱；連 3 季低於門檻 10 個百分點以上＝反轉"},{"id":"H2","text":"普通股相對淨資產維持溢價，讓增資換幣不稀釋每股 BTC","2y":null,"5y":"2031 年前 mNAV 多數時間 ≥1.0 倍；跌破時公司以普通股買回處理","10y":null,"threshold":"mNAV ≥1.0 倍（公司口徑）","source":"strategy.com 每日 mNAV、季報","drift_rule":"連 4 季季末低於 1.0 倍＝削弱；連 6 季＝反轉"},{"id":"H3","text":"比特幣長期報酬高於公司綜合信用成本 10.6%，超額報酬才會流到普通股","2y":null,"5y":null,"10y":"2036 年前比特幣 4 年滾動年化報酬多數時間 >10.6%，綜合信用成本不再上調","threshold":"比特幣 4 年滾動年化 >10.6%","source":"公司官網信用頁的 hurdle ARR、比特幣價格","drift_rule":"跨 2 個年度低於門檻＝削弱；跨 3 個年度＝反轉"}],"R":[{"id":"R1","text":"優先股市場再度失序：STRC 6 月曾跌到約 $75；若信用環境再收縮，STRC 跌破面值就停發，增資只能拿去護盤，每股 BTC 繼續下降；今年已賣幣支付部分股息","h_ref":"H1","clock":"⚡","threshold":"STRC 週收盤 <$95 連 2 週","evidence_refs":["financial_capital_credit_cycle#2"]},{"id":"R2","text":"2028 年可轉債回售：67 億美元可轉債中低於面值的兩檔最早 2028-03 可回售（Q3 法說，Andrew Kang），屆時股價不足以轉股又無法再融資，就要動用美元準備或賣幣；Q2 法說 Phong Le 曾稱下一個回售日在 2027 年 9 月，該檔目前高於面值","h_ref":"H2","clock":"🔥","threshold":"2027-12-31 前未公布處理方案且美元準備 <2 年，或方案淨稀釋 ≥15%","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"財務長 Andrew Kang 11-05 離任（公司稱個人因素），CEO Phong Le 暫兼，2027-01 起財務長分成軟體與比特幣兩位；信用框架與準備金政策的主導者離開，執行與揭露口徑可能改變","h_ref":"H1","clock":"🔥","threshold":"2027 年內再有財務或資金主管離任，或 BTC Yield 等自訂指標定義改變","evidence_refs":[]},{"id":"R4","text":"治理與訴訟：Dodge 集體訴訟（Delaware 衡平法院，民事、尚待集體認證）主張 STRK 條款修正應經普通股股東表決並告董事會違反受託義務；Rosen 律所 6 月展開證券調查，尚非訴訟。若敗訴，日後調整優先股條款可能要經普通股表決，資本結構調整變慢；影響金額本包未涵蓋","h_ref":"H2","clock":"🐢","threshold":"Dodge 案獲集體認證或不利和解；Rosen 調查轉為正式集體訴訟","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#2"]},{"id":"R5","text":"託管集中：10-Q 揭露比特幣有時集中由單一託管人保管、託管保險與其他客戶共用；託管事故會直接打到淨資產","h_ref":"H3","clock":"🐢","threshold":"10-Q 揭露單一託管比例或託管事故；目前比例本包未涵蓋（資料缺口）","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"公司宣布暫停、延後或改以非現金方式支付任一檔優先股股息","why_fatal":"股息是數位信用的全部承諾；一旦失信，所有優先股會跌離面值、信用發行停擺，普通股失去增資換幣的管道，溢價轉為折價，每股價值同時被比特幣與溢價兩頭壓","if_happens":"清倉，4 季內不重審；重審時改用清算價值當估值底","how_monitor":"STRC 自 11-01 起每日配息、其餘優先股 2027-01 起每日配息的公告；每季美元準備覆蓋年數；8-K","probability":"12–24 個月約 5%：美元準備覆蓋 3.4 年、Saylor 在 Q2 法說明言不會暫停股息、兩年 40 次股息全數照付；要發生須比特幣長期深跌、美元準備耗到 1 年以下、普通股又低於淨值無法增資，三者同時成立"}},"appendix_a":{"growth_durability":3,"quality_score":4,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":5.7,"peg_fy2":null,"stress":{"pass":3,"total":5},"fy2_valuation_basis":"依 Koyfin 共識（2026-10-31）"},"eps_meta":{"base_eps_path":{"FY2025A":-15.23,"FY2026E":-17.44,"FY2027E":23.67,"FY2028E":23.77},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（含比特幣公允價值變動）；FY2025A 取年度財報，FY2026E–FY2028E 取 Koyfin 2026-10-31 快照共識，家數事實表未涵蓋；基期為負，三年 CAGR 無意義；兩份快照間修正幅度皆為 0，疑似快照未更新"},"catalysts":[{"date":"2026-11-05","type":"other","event":"財務長 Andrew Kang 離任生效，CEO Phong Le 暫兼財務長","impact":"中","watch":"2027-01 起財務長拆成兩人後，BTC Yield 等自訂指標的揭露口徑是否改變"},{"date":"2026-12-31","type":"product","event":"地端授權主流支援結束，延伸支援至 2028-12-31","impact":"低","watch":"軟體營收與雲端訂閱成長"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報（管理層稱約 3 個月後）","impact":"高","watch":"BTC Yield 是否轉正、STRC 是否恢復淨發行"},{"date":"2027-09","date_precision":"month","type":"other","event":"Q2 法說提到的下一個可轉債回售日（該檔目前高於面值）","impact":"中","watch":"屆時股價是否仍高於轉換價"},{"date":"2028-03","date_precision":"month","type":"other","event":"低於面值的兩檔可轉債最早回售日","impact":"高","watch":"再融資方案、淨稀釋幅度與美元準備年數"},{"date":"2028-04","date_precision":"month","type":"macro","event":"比特幣減半（Saylor 預估時點）","impact":"中","watch":"新增供給減半後比特幣價格與持幣公司買盤"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：financial_regulatory_capital_rules（監管資本規則變動）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
