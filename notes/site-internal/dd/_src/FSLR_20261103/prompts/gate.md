你是 DD 管線 v20 的判斷層閘（gate），標的 FSLR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_gaap_net_sales`（q1_business）｜營收（GAAP net sales）＝1056.2 US$M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/1274494/000127449426000169/ex991pressreleaseq2-2026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-30））
  - 註記：consensus 約 $1,061M（多家彙整站稱『大致符合／小幅未達』，來源：web_search，非公司原文）
- `f_kpi1_non_gaap_adjusted_ebitda`（q1_business）｜Non-GAAP 獲利指標（Adjusted EBITDA；公司本季未單獨揭露 non-GAAP operating income）＝643.6 US$M；margin 61%｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 SEC 8-K Ex.99.1（同上）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-30））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／營業利益率＝450.4 US$M；margin 42.6%｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 SEC 8-K Ex.99.1（同上）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-30））
- `f_kpi5_fy2026_guidance_q2`（q1_business）｜FY2026 全年 guidance（隨Q2財報重申，區間未變動）＝Net sales $4.9B–$5.2B；Gross profit $2.4B–$2.6B；Opex $610M–$635M；Adjusted EBITDA $2.6B–$2.8B；Capex $0.8B–$1.0B；年底Net cash $1.7B–$2.3B；另單獨給Q3單季 Adjusted EBITDA guide $625M–$775M US$（詳見value欄各分項）｜期間與口徑：公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 SEC 8-K Ex.99.1（同上）（numbers.latest_quarter_kpis.items[5]，as_of 公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致））
  - 註記：營收guidance中值≈$5.05B，市場彙整站稱略低於 street consensus $5.08B（來源：web_search，非公司原文）
- `f_kpi6_contracted_sales_backlog`（q1_business）｜Contracted sales backlog（硬體／設備 archetype 追加項）＝45.1 GW；對應合約總值 $13.6B（不含技術調整項），交貨期至2030年｜期間與口徑：截至 2026-06-30，公告於 2026-07-30／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 SEC 8-K Ex.99.1（同上）（numbers.latest_quarter_kpis.items[6]，as_of 截至 2026-06-30，公告於 2026-07-30）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝17.48 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝107.48 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_fslr_gross_margin_pct`（q2_moat）｜FSLR 毛利率＝49.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FSLR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_fslr_operating_margin_pct`（q2_moat）｜FSLR 營業利益率＝37.69 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FSLR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_csiq_operating_margin_pct`（q2_moat）｜CSIQ 營業利益率＝-0.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSIQ.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jks_operating_margin_pct`（q2_moat）｜JKS 營業利益率＝-6.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JKS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_enph_operating_margin_pct`（q2_moat）｜ENPH 營業利益率＝4.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ENPH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_fslr_fcf_margin_pct`（q2_moat）｜FSLR FCF 利潤率＝4.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FSLR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝23.51 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝29.65 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4822.75 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5945.83 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF＝營運現金流－資本支出）＝-306.2 US$M；margin -29.0%｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表僅列 Six Months Ended 欄位，Q2 單季由 H1（營運現金流 -$359.8M／資本支出 -$279.8M）減去 Q1 press release 對應數字（-$214.9M／-$118.5M）反推，非公司原文直接揭露（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-30））
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益（及占營收）%＝1.56 %（占GAAP營業利益）；另占營收 0.67%｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表 H1 股權薪酬 $13.826M 減 Q1 press release 三個月數字 $6.781M，反推 Q2 單季 SBC ≈$7.045M，非公司原文直接揭露單季數（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-30））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1299.11 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 324.97、現金 1624.08（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝184.21 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝10.54 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 17.48，分子＝快照價 184.21｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝10.65 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.95 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.84 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（17.48 → 17.48）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（23.51 → 23.51）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-12.86 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.47｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 183.14 / W52 222.53 / W104 200.65 / W250 177.33 / W250 13週斜率 0.84%」
- `f_ma_w104`（q5_valuation）｜104 週均線＝200.65 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝177.33 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.29 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 17.43 → 17.48（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）

### findings_digest 中方向為負或來源衝突的條目（23 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：2025年全球模組出貨量排名：LONGi 約87GW、Jinko約86GW 並列龍頭，FSLR出貨17.5GW創自身紀錄但僅佔全球約2%市佔率，量能上落後中國廠
  - 來源：TaiyangNews / SolarQuarter，2025全球模組出貨排名報導（as_of 2026-03-14）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：同業／風險因子提及：來自矽晶（crystalline silicon）模組廠的激烈競爭可能壓低平均售價與淨銷售；FSLR 也在CdTe配方中加入鈣鈦礦(perovskite)以提升效率，屬對新興技術威脅的回應
  - 來源：綜合搜尋摘要（PV Tech / CleanTechnica 相關報導）（as_of 2026-03-13）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K names two customers each at/above 10% of modules business net sales: Silicon Ranch Corporation and NextEra Energy.
  - 來源：First Solar, Inc. Form 10-K FY2025（as_of 2025-12-31）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：全球太陽能供應鏈各環節產能相對近期需求嚴重過剩（pv magazine 用「severely overbuilt」形容）
  - 來源：pv magazine USA（as_of 2026-09-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：第三方估算：多晶矽產能約 2,034 GW 對比 2026 年預估裝機 638 GW，模組產能約 1,908 GW，過剩逾 1.2 TW；此為結構性而非暫時性短缺
  - 來源：ICRA / SurgePV 產業分析（經搜尋摘要彙整）（as_of 2026-08-28）｜affects：moat_trend、thesis.R
- `supply_demand_durability#7`（supply_demand_durability｜方向 -｜狀態 ok）：產業預估 2026 年全球 PV 模組需求將自 2025 年的 653–706 GWdc 降至 529–624 GWdc，為近十年來首次年度負成長
  - 來源：搜尋摘要彙整（產業預估報告）（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Section 201 進口晶矽太陽能電池／模組安全防護關稅於 2026-02-06 到期，結束長達八年的對低價進口品限制
  - 來源：Beveridge & Diamond (bdlaw.com) - Solar's Momentum At Mid-2026 Will Help It Overcome Snags（as_of 2026-02-06）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：中國自2025年2月起收緊含碲（tellurium）等五項關鍵礦物的出口管制，出口商須向中國商務部申請許可；碲是 First Solar CdTe 模組的主要原料之一，中國佔2024年全球精煉碲產量約76.53%。First Solar 10-K/10-Q 揭露已組建跨部門小組監控此風險、申請出口許可並尋求替代供應商。
  - 來源：pv-magazine-india.com — 'China adds export restrictions for minerals used in thin-film solar'; First Solar SEC filings (10-K/10-Q risk factors, 搜尋摘要)（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：First Solar 的關鍵原料碲(tellurium)是煉銅的副產品，供應量跟著銅需求走;公司只跟少數幾家供應商採購，換供應商要走很長的資格審查，萬一斷供不容易及時補上
  - 來源：First Solar 10-K (FY2015) 風險因子章節（as_of 2015-12-31）｜affects：thesis.R、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：印度市場：Q1'26 新簽 0.8 GW、均價僅 $0.20/W，明顯低於美國 utility-scale 的 $0.35/W，反映印度段定價力較弱、屬較低毛利的地區市場。
  - 來源：First Solar Q1'26 earnings coverage aggregation（as_of 2026-04-30）｜affects：thesis.H、decision_inputs.bear、valuation
- `end_markets#7`（end_markets｜方向 -｜狀態 ok）：全球（非 FSLR 所在的關稅保護利基）結晶矽模組市場：2026 年預估為十餘年來全球 PV 需求首次負成長（529–624 GWdc），全球產能逾 1,100 GW 對僅約 650 GW 裝機需求，模組價格崩至約 $0.10/W，遠低於 TOPCon 約 $0.16/W 的生產成本；此為中國結晶矽產能過剩導致，與 FSLR 受美國關稅/本土含量保護的薄膜（CdTe）利基市場性質不同。
  - 來源：InfoLink Consulting / pv magazine aggregation（as_of 2026-01-12）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：矽晶太陽能效率持續提升、成本下降，可能使 CdTe 與矽晶的效率差距擴大到租稅抵減也難以彌補的程度
  - 來源：FinancialContent - The American Solar Champion: An In-Depth Research Feature on First Solar (FSLR)（as_of 2026-04-15）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：2026-10-29 Q3 財報下修全年 2026 guidance：出貨量 16.0–17.0GW（原 17.0–18.2GW）、淨銷售 $4.6–4.9B（原 $4.9–5.2B）、調整後 EBITDA $2.55–2.75B（原 $2.6–2.8B）、資本支出 $0.6–0.8B（原 $0.8–1.0B）；新聞稿未明說下修原因，並稱展望假設現行美國政策環境持續
  - 來源：First Solar 8-K Ex.99.1 Q3 2026 press release (SEC)（as_of 2026-10-29）｜affects：thesis.R、valuation、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 初始 guidance 營收 $4.9–5.2B 遠低於約 $6.16B 共識，多家券商降評/降目標價
  - 來源：Finviz: First Solar 2026 Guidance Disappoints Wall Street Firms, Triggers Downgrades（as_of 2026-03-01）｜affects：valuation、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Morgan Stanley 下修 2026 出貨預估至 17.6GW（原 19.7GW）、ASP 至 $0.287/W（原 $0.315）
  - 來源：Yahoo Finance: Why Morgan Stanley Cut First Solar's Target as Pricing Recovery Slows（as_of 2026-03-10）｜affects：valuation、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2025-09 First Solar 在紐約州最高法院控告 BP Solar Holding 及 Lightsource 違約，要求支付 3.236 億美元及其他已交付模組應收款。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：decision_inputs.bear、thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2026年有針對 FSLR 的證券集體訴訟（Day v. First Solar，EDNY），集體期間 2025-02-26 至 2026-02-24，指控淡化關稅影響；原告律所公告，指控未經證實。
  - 來源：Levi & Korsinsky 公告（natlawreview）（as_of 2026-06-24）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：中國龍頭LONGi與Jinko仍持續擴大電池產能，LONGi的HPBC電池產能預計2026年底達50GW、Jinko的N型TOPCon產能超過60GW，顯示同業並未收縮新產能
  - 來源：TheEnergyBrief - PV Module Manufacturers' New Reality 2026（as_of 2026-07-19）｜affects：moat_trend
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：美國同業Qcells在喬治亞州Cartersville廠已開始生產矽晶太陽能電池，3.5GW電池線預計2026年第三季達全產能，屬美國本土新增產能
  - 來源：Solar Power World Online（as_of 2026-06）｜affects：moat_trend、thesis.bear、decision_inputs.bear
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：美國同業T1 Energy 2026年模組產量預計3.1-4.2GW（2025年為2.79GW），德州Milam County的2.1GW電池廠第一期預計2026年第四季開始投產，屬未來12-24個月內的新增美國本土產能
  - 來源：pv magazine USA（as_of 2026-05-14）｜affects：moat_trend、thesis.bear、decision_inputs.bear
- `cyclical_inventory_price_position#3`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：First Solar 合約在手訂單（backlog）截至 2026/6/30 降至 45.1GW、約 $13.6B，較 2025 年底的 50.1GW 下降；當季出貨 7.6GW、新增訂單僅 2.8GW，取消訂單多於新單
  - 來源：PV Tech / Investing.com（First Solar Q2 2026 財報）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026年有針對 FSLR 的證券集體訴訟（Day v. First Solar，EDNY），集體期間 2025-02-26 至 2026-02-24，指控淡化關稅影響；原告律所公告，指控未經證實。
  - 來源：Levi & Korsinsky 公告（natlawreview）（as_of 2026-06-24）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#2`（lawsuit_class_action｜方向 -｜狀態 ok）：2025-09 對 BP Solar/Lightsource 追討 3.236 億美元。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":494.0,"bear_5y_price":90.0,"p_bull_pct":20,"p_bear_pct":32,"upside_5y_pct":52.3,"ev5y_pct":42.4,"irr_base_pct":8.8,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":17.48,"pe":10.54,"basis":"FY2026E共識EPS（當年度，判斷日距年底約兩個月），與終端FY2031E當年度EPS同口徑"},"eps":{"bull":[25.0,32.0,35.0,37.0,38.0],"base":[22.5,27.0,26.5,26.0,25.5],"bear":[19.0,18.0,14.0,12.0,10.0]},"pe":{"bull":13,"base":11,"bear":9},"p":{"bull":20,"base":48,"bear":32},"yield_pct":{"dividend":0,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":2},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FSLR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：CFO 表示 2026 全年財測維持不變（原話："Our full year 2026 guidance remains unchanged."）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：財測現假設淨關稅影響 6,000 萬至 8,000 萬美元（含 IEEPA 淨回收與下半年 Section 301 假設）（原話："assumes a net tariff impact of $60 million to $80 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：Q3 出貨量指引 3.9–4.5 GW（原話："volumes sold between 3.9 gigawatts and 4.5 gigawatts"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：Q3 調整後 EBITDA 指引 6.25–7.75 億美元（原話："EBITDA between $625 million and $775 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜guidance：印度產能假設主要在國內短週期市場銷售、高稼動率；上半年訂單約 1.1 GW（原話："totaled approximately 1.1 gigawatts"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：Q2 毛利率約 57%（原話："expanded gross margin to approximately 57%"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：CFO 拆解毛利率年增原因之一：約 8,900 萬美元 IEEPA 關稅淨利益（原文金額 $89 在上一行）（原話："million net IEEPA tariff-related benefit"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：毛利率另一拆解項：符合 45X 稅額抵減的模組組合提高（原話："higher mix of modules qualifying for Section 45X tax credits"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：IEEPA 淨關稅利益為目前估計，後續可能調整（原話："remains subject to refinement as"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：Q2 調整後 EBITDA 6.44 億美元，高於先前預覽區間上緣（原話："above the high end of our previously communicated"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：部分美國境內運費已接近國際海運成本（因模組交付地點改變）（原話："domestic freight costs are now approaching"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：東南亞廠低稼動每季約 3,000 萬美元，約一半為現金、一半非現金（原話："somewhere around $30 million quarter of underutilization"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：CEO 描述成本環境：大宗商品成本上升、降本空間有限（原話："a pretty challenging rising commodity cost environment"）
- 2026-07-30｜Mark Widmar (CEO)｜margin：CEO 稱當前是降成本最困難的時期之一（原話："probably one of the most challenging times that we've been in"）
- 2026-07-30｜Alexander Bradley (CFO)｜margin：研發費用含部分不再用於技術路線圖的研發設備減損（原話："impairment of certain R&D equipment"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：CEO 表示優先看價格、合約品質與風險分配，而非短期訂單量（原話："we continue to prioritize pricing, contract quality"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：南卡完工廠第一階段預計 2026 下半年開始生產（原話："first phase of the finishing facility remains on track"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：Series 6 尺寸鈣鈦礦試產線預計 2027 上半年達運作就緒（原話："operational readiness in the first half of 2027"）
- 2026-07-30｜Alexander Bradley (CFO)｜commitment：CFO 稱 232 結果出來後會盡快形成對東南亞產能的看法（原話："We would expect to evaluate that and have a view shortly thereafter."）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：CEO 表示不會放棄降低投入成本（原話："we're never going to give up on the input costs"）
- 2026-07-30｜Mark Widmar (CEO)｜commitment：新訂單優先要求現金流動性擔保（原話："having cash liquid security against new bookings"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：季末淨現金約 17 億美元，在目標區間 15–20 億內（原話："approximately $1.7 billion of net cash"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：上半年營運現金流出 3.6 億美元（原話："Operating cash outflows year-to-date were $360 million"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：上半年資本支出 2.8 億美元（原話："First half capital expenditures were $280 million"）
- 2026-07-30｜Mark Widmar (CEO)｜capital_allocation：CEO 表示持續投入大量資本於鈣鈦礦商業化（原話："continue to invest substantial capital in our efforts"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：CFO 提到可運用資產負債表協助供應商擴產以換取遠期定價（原話："We could try and leverage our position of"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：CFO 對併購表示較過去更願意、更開放，但強調紀律（原話："So we are more willing to do that."）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：東南亞可全流程完工產能約 1.8 GW，待 232 結果再決定（原話："about 1.8 gigawatts of end-to-end fully finished capacity"）
- 2026-07-30｜Alexander Bradley (CFO)｜capital_allocation：東南亞產能決策等待 232 結果（原話："we're really waiting for the outcome of the 232"）
- 2026-07-30｜Mark Widmar (CEO)｜product：南卡第二階段完工時間改為 2027 年中，並稱可更早納入 CuRe（原話："we now expect completion in mid-2027"）
- 2026-07-30｜Mark Widmar (CEO)｜product：CEO 稱 CuRe 量產與田間表現優於預期（原話："We are pleased with the performance of CuRe"）
- 2026-07-30｜Alexander Bradley (CFO)｜product：已開始發出合約 CuRe 價格調整項的首批客戶通知（原話："initiated our first customer notifications"）
- 2026-07-30｜Alexander Bradley (CFO)｜product：2026 年 CuRe 銷售的 ASP 上行有限（原話："expect limited ASP upside from CuRe sales in 2026"）
- 2026-07-30｜Mark Widmar (CEO)｜product：Series 6 尺寸鈣鈦礦試產線進度符合時程（原話："Series 6 form factor pilot line remains on schedule"）
- 2026-07-30｜Mark Widmar (CEO)｜product：CEO 對 FCC 逆變器裁決：認為近期不會構成限制（原話："I don't see it being a constraint near term."）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：在手訂單 45.1 GW（原話："our contracted backlog totaled 45.1 gigawatts"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：自上次財報新增美國毛訂單約 1.9 GW（原話："approximately 1.9 gigawatts of additional U.S. gross bookings"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：新增美國訂單平均售價約每瓦 0.36 美元（含技術調整項）（原話："average selling price of approximately $0.36 per watt"）
- 2026-07-30｜Alexander Bradley (CFO)｜customer：美國完全整合產線產能已大致被承諾至 2028 年（原話："substantially committed through 2028"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：在手訂單約 41 GW 含某種形式的本土含量要求（原話："Approximately 41 gigawatts of our 45-gigawatt"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 描述超大規模資料中心業者需求（原話："somewhat insatiable demand from hyperscalers"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 稱 7 月已簽近 2 GW 美國訂單（原話："we booked almost 2 gigawatts in the"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：另有超過 2 GW 在合約中但附帶先決條件（CP）（原話："There's about 2 more gigawatts, north of 2 gigawatts"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：另有約 2 GW 洽談中，CEO 稱年底前高機率成交（原話："we can close through by the end of the year"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 確認有客戶因等待政策而觀望（原話："customers that are sitting on the sidelines"）
- 2026-07-30｜Mark Widmar (CEO)｜customer：CEO 說明 1.9 GW 訂單多數發生在 7 月（季末之後）（原話："So most of that happened in July"）
- 2026-07-30｜Mark Widmar (CEO)｜risk：Section 232 結果尚未公布，CEO 仍樂觀認為結果將具建設性（原話："we're still optimistic that the outcome will be constructive."）
- 2026-07-30｜Alexander Bradley (CFO)｜risk：CFO 指 Section 301 產能過剩調查仍有風險（原話："There is still risk around 301 relating to excess capacity"）
- 2026-07-30｜Mark Widmar (CEO)｜risk：CEO 反對 232 設豁免或配額（原話："we don't believe that they should be allowed"）
- 2026-07-30｜Alexander Bradley (CFO)｜competition：CFO 描述競爭格局：多數競爭對手為中國企業且規則不同（原話："the vast majority of our competitors are Chinese"）
- 2026-07-30｜Alexander Bradley (CFO)｜competition：CFO 認為國安性質的 232 設carve-out不合理（原話："doesn't make a lot of sense to have a carve-out"）

### FSLR_Shareholder_Analyst_Call_First_Solar_Inc_20260513.md
- 2026-05-13｜Mark Widmar｜commitment：CEO 確認 CuRe 技術已在 Perrysburg 完成導入，首條 Series 6 產線爬坡符合預期（原話："the CuRe launch is complete in Perrysburg"）
- 2026-05-13｜Mark Widmar｜guidance：CuRe 技術調整可望為 backlog 帶來最高 6 億美元額外營收，主要落在 2027-2028 年（原話："$0.6 billion of additional revenue from technology adjusters"）
- 2026-05-13｜Mark Widmar｜customer：CEO 重申技術策略前提：客戶買的是全生命週期發電量，不是單純名牌效率（原話："buy lifetime energy, not just nameplate efficiency"）
- 2026-05-13｜Mark Widmar｜product：Perovskite 技術可靠度已達可比業界最佳 R&D 成果的水準（原話："reliability results that we believe are comparable to"）
- 2026-05-13｜Alexander Bradley｜margin：CFO 確認 2026 年第一季毛利率明顯擴張，帶動單季每股盈餘創紀錄（原話："margin expansion and record Q1 diluted EPS of $3.22"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認南卡羅來納州加工產線進度符合 2026 年第四季排程（原話："Carolina finishing line remains on schedule for Q4 2026"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認路易斯安那州廠已完成試車並啟動商業化生產（原話："initiated commercial production at our Louisiana facility"）

### 問答異常語氣（迴避／改口／保留）
- FSLR_Q2_2026_Earnings_Call_20260730.md｜問：Brian Lee (Goldman)：Section 232 時程與 $0.40/W 以上價格下限的看法｜答法：CEO 未回應價格下限數字，表示不願給內部判斷（'I don't want to give kind of our internal read'），僅稱仍演進中、保持樂觀
- FSLR_Q2_2026_Earnings_Call_20260730.md｜問：Philip Shen (ROTH)：232 是否會在 8 月公布或延到秋季｜答法：CEO 未給時間點，稱無法提供更強的信心（'I can't really give you a strong view on that'），改談希望正確實施

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 9 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 9 | 5 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 1 | 4 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 4 | 5 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260929","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","irr_base_pct":8.8,"ev5y_pct":52.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":52.7,"irr_base_pct":8.8,"max_dd_pct":-55,"bull_5y_price":476.0,"bear_5y_price":88.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","price_at_dd":172.97,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FSLR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"First Solar, Inc."},"oneliner":"獲利幾乎全靠45X抵減與232保護；FY2026E本益比10.5倍看似便宜，但在手訂單九個月降12%、新簽轉慢，232生效後兩季訂單數據出來前不加碼","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺美國公用事業級電廠開發商的錢，獲利卡在美國本土製造換來的45X抵減與本土含量溢價：2026年預估抵減約21億美元，高於共識淨利約18.8億美元","reasoning":"收錢方式：把CdTe薄膜模組賣給美國公用事業級電廠開發商、獨立發電商、公用事業與大型企業購電方，以多年框架合約或單一專案合約鎖量鎖價，交貨時認列；沒有住宅通路。FY2025年報揭露Silicon Ranch與NextEra各占模組事業營收10%以上，前兩大合計約兩成，未構成集中度風險。最新一季（2026-10-29 Q3法說會，CFO Alex Bradley）：營收約12億美元、年減約23%（第三方模組量下滑），毛利率約58%、年增約20個百分點（美國製占比提高、關稅與稼動成本下降），稀釋每股盈餘5.30美元；前一季GAAP營業利益率42.6%、調整後EBITDA率61%。錢卡在兩個節點：一是美國本土製造換來的45X抵減，2025年認列約16億美元、2026年預估產生約21億美元，都高於當年淨利（FY2026E共識淨利約18.8億美元＝17.48美元×1.0748億股）；二是本土含量與FEOC合規換來的單價溢價。單點依賴在政策而非客戶：10-29下修財測時公司明言展望假設現行美國政策延續。產業時鐘III：全球矽晶產業處收縮期，但FSLR所在的美國受保護市場毛利處歷史高點、新進者在美國加產能、客戶延後下單，屬過熱後段。","fact_refs":["f_kpi0_gaap_net_sales","f_kpi1_non_gaap_adjusted_ebitda","f_kpi2_gaap","f_kpi5_fy2026_guidance_q2","f_kpi6_contracted_sales_backlog","f_earnings_recency","f_consensus_eps_fy1","f_shares_diluted_m"],"verdict_values":{"revenue_quality":"合約型為主但彈性大：在手訂單44 GW、約135億美元排到2030年，框架合約允許客戶調整交期，Q3仍有合約終止收入；45X入帳在成本端、現金回收落後（政府補助應收約19億美元），獲利品質低於表面毛利率。","unit_econ_note":"美國新簽約0.35–0.36美元／瓦（含技術加價），在手訂單均價約0.31（135億美元÷44 GW），印度本地約0.20，美國市場中位價2026Q1約0.28，中國TOPCon出口約0.11；同一片模組在不同市場的價差主要由關稅與本土含量規則決定。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"近五年有GAAP虧損年（2022年）、毛利率峰谷由2.67%到約58%、太陽能產業、營收受模組單價與政策驅動"},"industry":{"clock_phase":"III","sd_verdict_source":"供給可逆性高：美國市場的供不應求建立在232最低進口價與本土含量規則上，全球模組產能逾1.1 TW對約650 GW需求，政策一鬆過剩產能即可回流；屬政策型持久，非產業結構型持久。","bargaining":{"up":"上游：碲為煉銅副產品，供應商少、認證期長，中國占2024年全球精煉碲約77%且自2025-02起出口管制；上游議價力中等偏強","down":"下游：大型開發商與公用事業，前兩大客戶各約一成；客戶在232後延後採購做價格發現，短期議價力上升","geo":"製造集中美國（俄亥俄、阿拉巴馬、路易斯安那、南卡），2027年約80%產能在美國；印度、越南、馬來西亞為國際產能，馬來西亞2027上半年決定去留"},"profit_pool_dir":"利潤池由中國矽晶廠移向美國本土製造：FSLR營業利益率37.69%，CSIQ、JKS為負；移轉動力是政策，不是成本優勢","tam_table":[{"item":"全球模組需求2026年","value":"529–624 GWdc，近十年首次負成長（產業預估）"},{"item":"美國公用事業級2026年計劃新增","value":"43.4 GW，較前一年增60%（EIA）"},{"item":"美國本土模組產能","value":"2025年底65.5 GW，2024年底42.5 GW"},{"item":"FSLR 2026年出貨","value":"16.0–17.0 GW（10-29下修後財測，原17.0–18.2 GW）"},{"item":"滲透率與營業利益池占比五年前→現","value":"事實表未涵蓋；同業營業利益率對照顯示利潤集中在美國本土製造"}]}}},"q2_moat":{"verdict":"護城河方向持平（→），等級C：CdTe不碰中國矽晶供應鏈加上美國本土製造，換來45X與本土含量溢價；這道牆是政策砌的，對手正在牆內蓋廠","reasoning":"機制：CdTe薄膜不需多晶矽，是美國唯一完整整合、不依賴中國矽晶供應鏈的公用事業級模組廠，2027年約80%產能在美國，同時拿到45X抵減與客戶的本土含量、FEOC合規溢價。可證方向：TTM營業利益率37.69%，對照CSIQ −0.55%、JKS −6.7%、ENPH 4.53%，差距為正，且隨FSLR毛利率由FY2023年39.19%升到TTM 49.25%而擴大（同業ROIC事實表未涵蓋，以營業利益率代理）。評分：執行7（CuRe在Perrysburg完成導入、路易斯安那商轉、南卡第一期投產；扣分在Series 7早期品質問題與馬來西亞低稼動）；定價7（美國新簽0.35–0.36美元／瓦，高於在手訂單均價約0.31與美國市場中位價0.28；扣分在溢價來自政策）；232遭囤貨與豁免稀釋屬生態攻擊扣1分，合併6，等級C。方向：執行穩定、定價穩定偏強、量能轉弱，判持平。報酬持續期：投入資本與稅率事實表未涵蓋，當期ROIC無法計算；依重資產、45X應收約19億美元與存貨倉儲成本研判屬高利益率×低周轉。增量報酬約44%、前瞻再投資率上限約37%、內生上界約16.5%，推導見公式欄；增量報酬含45X，本質是政策報酬。四檢查點中社會容忍度為紅。","fact_refs":["f_peer_fslr_gross_margin_pct","f_peer_fslr_operating_margin_pct","f_peer_csiq_operating_margin_pct","f_peer_jks_operating_margin_pct","f_peer_enph_operating_margin_pct","f_peer_fslr_fcf_margin_pct","f_kpi2_gaap","f_kpi6_contracted_sales_backlog"],"verdict_values":{"moat":{"mechanism":"CdTe薄膜不需多晶矽，是美國唯一完整整合、不依賴中國矽晶供應鏈的公用事業級模組廠；美國本土產能換到45X抵減與本土含量、FEOC合規溢價","execution":7,"pricing":7,"grade":"C","trend":"→","trend_evidence":"執行面穩定：CuRe在Perrysburg完成導入、首條Series 7轉換2027Q1在印度啟動、南卡第一期Q3投產；定價面穩定偏強：美國新簽0.35–0.36美元／瓦高於在手訂單均價約0.31，232後新談案已提價；量能面轉弱：在手訂單由2025年底50.1 GW降到44.0 GW、自上次法說僅新簽1.4 GW。三者相抵判持平，未見最大客戶份額下滑的證據。","competitor_notes":[{"name":"CSIQ","strategy_note":"矽晶模組＋儲能＋電廠開發多角化，模組端在全球過剩下虧損；在美國受232與FEOC審查限制"},{"name":"JKS","strategy_note":"全球出貨龍頭之一，TOPCon產能逾60 GW仍在擴，毛利率低到個位數；FSLR對其提TOPCon專利訴訟"},{"name":"ENPH","strategy_note":"住宅微型逆變器，非模組同業，只作美國太陽能製造利潤率參照"},{"name":"Qcells","strategy_note":"喬治亞州3.5 GW電池線2026Q3滿產，是FSLR在美國本土含量市場最直接的矽晶對手"},{"name":"T1 Energy","strategy_note":"德州2.1 GW電池廠2026Q4投產、2026年模組3.1–4.2 GW；Q3法說會分析師提到其申請電池進口豁免"}],"peer_na_reason":"同業ROIC與本益比事實表未涵蓋，以營業利益率差距代理","threats":[{"level":"🔴","text":"232最低進口價遭囤貨、第三國繞道與豁免稀釋：進口商由約200家增至約400家、僅約60家被擋，全球過剩產能逾1 TW形成持續壓力","p":"40%","evidence_refs":["regulatory_antitrust#0","end_markets#7","supply_demand_durability#1"]},{"level":"🟡","text":"美國本土矽晶新產能放量（Qcells、T1），FEOC規則明朗後可能取得本土含量資格","p":"40%","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"level":"🟡","text":"TOPCon效率領先CdTe數美分且持續提升，中國龍頭仍在擴產；FSLR全球市占僅約2%","p":"35%","evidence_refs":["substitute_technology#0","competitive_share_entrants#5","cyclical_supply_discipline_capacity#1","competitive_share_entrants#2"]},{"level":"🟡","text":"碲原料受中國出口管制、供應商少且認證期長","p":"15%","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是電廠、決策者是開發商、付款者是購電的公用事業與資料中心；需求是真的（EIA估2026年美國公用事業級計劃新增43.4 GW、年增60%），但可延後：Q3法說會CEO Mark Widmar稱客戶延後2029年後早期專案採購，一筆2 GW案因州政府暫停令中止，且專案須在2028年底前完工才拿得到安全港，需求向2028年前擠。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一電廠設計：模組在專案初期鎖定，決定組串與電壓配置，交貨前18–24個月定案，同一專案內換供應商成本高、跨專案可換。Q2法說會稱45 GW在手訂單中約41 GW含本土含量要求，加上客戶自評對手FEOC風險，決策層級的替代性低於商品層級。"},{"item":"價值鏈分配","level":"🟡","text":"FSLR拿到45X與本土含量溢價，開發商卻同時承受電池漲價、關稅與通膨（Q3法說會CEO），下游利潤被擠壓會回頭壓模組議價；中國矽晶廠虧損，價值已由中國廠轉到美國本土廠，但這次重分配靠政策維持。"},{"item":"社會容忍度","level":"🔴","text":"獲利約等於政策移轉：2026年預估45X抵減約21億美元，高於共識淨利；232屬總統公告可被豁免或調整，公用事業對價格敏感、業者正在遊說豁免（Q3法說會分析師提問）。45X法源與修法程序事實表未涵蓋。實際定價天花板由政策上限決定，不是經濟上限。"}],"roiic":44.2,"reinvest_rate":37.3,"endo_ceiling":16.5,"formula_note":"增量報酬＝淨利增量÷累計再投資：（2025年淨利15.28億−2022年−0.44億）÷（2023–2025年淨利減自由現金流合計16.15＋16.00＋3.41＝35.56億）≈44.2%。前瞻再投資率上限＝2026年資本支出財測中值7億÷FY2026E共識淨利約18.8億≈37.3%，未扣折舊故為上限（折舊事實表未涵蓋）；歷史再投資率約97%（35.56÷三年淨利36.51億）。內生上界＝44.2%×37.3%≈16.5%。以淨利代替稅後營業利益，含45X抵減。"}}}},"q3_growth":{"verdict":"五年後成長空間中等（🟡）：2027–28年有44 GW在手訂單與CuRe技術加價撐，2029年後的量與價沒有合約保護，鈣鈦礦第二曲線仍在試產線階段","reasoning":"成長來源以價與組合為主：共識FY2027E每股盈餘年增約34.5%（17.48→23.51），營收年增約23.3%（48.2億→59.5億美元），差距來自美國製產品占比提高與CuRe技術加價（最多約6億美元，約20%落在2027年交貨，其餘2028年以後）；回購只有新授權5億美元，約市值2.5%，無併購。共識三年每股盈餘年化約27.8%（FY2025A 14.21→FY2028E 29.65，Koyfin快照，EPS家數事實表未涵蓋；FY1營收共識32位分析師），高於內生上界約16.5%，缺口約11個百分點歸因於毛利擴張，不屬無法歸因。Runway：美國整合產能大致已簽到2028年，之後可售產能較多但客戶尚未下單；專案安全港須在2028年底前完工，2029年後需求有斷層風險；鈣鈦礦試產線2027上半年才就緒，沒有量產證據，不算已證實的第二曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_contracted_sales_backlog"],"verdict_values":{"growth":{"driver_mix":"價與產品組合為主、量為輔；回購小、無併購","runway_years":"約2–3年訂單能見度（美國整合產能大致已簽到2028年）；30%滲透率口徑事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約16.5%（增量報酬約44.2%×前瞻再投資率上限約37.3%），共識三年每股盈餘年化27.8%超出約11個百分點，缺口歸因毛利擴張（本土占比、CuRe加價、232後新單漲價）","segments":[{"item":"美國整合產線（Series 6／7）","value":"2027年約占全球產能80%；產能大致已簽到2028年；新簽0.35–0.36美元／瓦"},{"item":"南卡完工廠（越南半成品）","value":"2027年產量2.2–2.5 GW；第二期2027年中商轉"},{"item":"印度廠","value":"2027年成品2.2–2.6 GW；本地單價約0.20美元／瓦；2026年本地出貨下修約0.7 GW"},{"item":"馬來西亞廠","value":"1.8 GW，2027上半年二選一：滿載或停產；管理層稱不影響經常性獲利"},{"item":"分部營收與毛利拆分","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":false,"note":"Q2約57%、Q3約58%，年增約20個百分點"},{"signal":"核心市占近12個月縮減","lit":false,"note":"美國市占事實表未涵蓋；在手訂單連降列入觀察"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"232後新單提價、新簽轉慢，但下修集中在印度與國際Series 6，美國全本土產品出貨區間未變；觀察中"},{"signal":"EPS成長顯著高於營收成長","lit":true,"note":"共識FY2025A→FY2027E每股盈餘年化約28.6%，營收年化約6.7%，差距逾20個百分點"},{"signal":"自由現金流／淨利連2年低於0.75","lit":false,"note":"FY2024約−0.24、FY2025約0.78；TTM自由現金流率僅4.64%，FY2026若低於0.75即亮"},{"signal":"SBC占營收逾5%且上升","lit":false,"note":"Q2約0.67%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"note":"全球需求2026年負成長，但核心的美國公用事業級仍成長"},{"signal":"估值倍數近3年系統性下移","lit":true,"note":"自身本益比在3個年度端點、股價營收比在4個端點皆為最低；產業倍數事實表未涵蓋，以自身倍數代替"},{"signal":"維護性資本支出占自由現金流逾60%","lit":false,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且營收3年內下滑","lit":false,"note":"資本支出下修、2026年營收低於2025年，但南卡第二期與CuRe轉換仍在投入"}],"trap_rating":"價值陷阱風險🟡（亮2項）；長期成長性🟡"}}},"q4_capital":{"verdict":"資本配置中段：淨現金約15億美元守在目標區下緣，新授權5億美元回購，但自由現金流被45X應收與存貨吃掉","reasoning":"自由現金流轉換弱：FY2023自由現金流／淨利約−0.94、FY2024約−0.24、FY2025約0.78，TTM自由現金流率4.64%對營業利益率37.69%；Q2單季自由現金流−3.06億美元（由上半年數字反推）。錢卡在45X應收（政府補助應收約19億美元，其中美國約18億）與存貨：CFO Alex Bradley稱框架合約交期變動迫使公司多囤庫存，倉儲成本與營運資金變差。2026年資本支出財測下修到6–8億美元。配置順序：維持15–20億美元淨現金應對循環，Q3末約15億美元；其次技術、研發與併購（Q2法說會CFO稱對併購更願意）；10-29董事會授權5億美元回購、無到期日，尚未執行。SBC占營收約0.67%，稀釋輕微。近三年現金去向四分、債務到期結構事實表未涵蓋。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_peer_fslr_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近12個月無併購完成；管理層稱更願意做技術相關併購"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"5億美元回購授權於2026-10-29生效，尚未執行，無買入均價可算"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q2單季SBC約占營收0.67%、占營業利益1.56%；淨稀釋率事實表未涵蓋，但SBC規模遠低於每年1.5%門檻"}],"grade":null},"governance":{"capital_returns":{"expanded":false,"reason":"成長沒有靠併購撐；股東回報只有新授權的5億美元回購，尚無執行紀錄可評"}}}},"q5_valuation":{"verdict":"現價只要求2028年後盈餘不崩就划算；但這份盈餘幾乎等於45X抵減、毛利率又在歷史高點，我只信2027–28年那一段，估值合理而非便宜","reasoning":"以FY2026E本益比10.54倍、FY2027E 7.84倍計，市場隱含的是盈餘在2028年後明顯縮水。2027–28年有在手訂單撐，我信；2029年後的量價，不信到管理層說的程度。基準情境五年後約280美元（FY2031E 25.5美元×11倍），一年約214美元（FY2027E 22.5美元×9.5倍）。PEG以共識三年每股盈餘年化27.8%計約0.38；分位只有3個年度端點、當前在最低點，非五年分位。同業CSIQ、JKS營業利益率為負，本益比無意義，終端倍數只能錨自身現值。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_s_fwd","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E），輔以FY2027E","tier":"美國本土受保護模組製造商（同業虧損，無同級可比本益比）","peers":{"expanded":false,"reason":"同業CSIQ、JKS營業利益率為負、本益比無意義，ENPH屬逆變器非同級；同業倍數事實表未涵蓋"},"fwd_pe":10.54,"peg":0.38,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"表面便宜：FY2026E本益比10.54倍、FY2027E 7.84倍、PEG 0.38，本益比與股價營收比都在自身年度端點最低。但分母是爭點：2026年預估45X抵減約21億美元高於共識淨利，Q3毛利率約58%處自身歷史高點，便宜論證不成立。改以情境期望值看：機率加權五年價約262美元，年化約7%，屬合理區。五年分位因只有3個年度端點無法計算，留空。","upside_short_pct":16.0,"upside_mid_pct":52.3,"denominator_disputed":true,"denominator_note":"每股盈餘幾乎全數來自45X抵減（2026年預估約21億美元對共識淨利約18.8億美元），且Q3毛利率約58%處自身歷史高點；這份盈餘能否延續正是多空爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在政策：若45X延續、232執行到位、2029年後美國本土產品簽滿，現價7.84倍FY2027E就是錯殺","reasoning":"看錯的方向有兩個：一是政策比預期穩，基準情境太保守；二是需求斷層與政策縮減同時發生，空頭情境約90美元。推論與處置寫在反證紀錄，本欄不重寫。26週報酬−12.86%、RSI 54.47，動能不過熱；股價在104週均線之下、250週均線之上。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w104","f_ma_w250","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"便宜但獲利靠政策"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":17.48,"pe":10.54,"basis":"FY2026E共識EPS（當年度，判斷日距年底約兩個月），與終端FY2031E當年度EPS同口徑"},"eps":{"bull":[25.0,32.0,35.0,37.0,38.0],"base":[22.5,27.0,26.5,26.0,25.5],"bear":[19.0,18.0,14.0,12.0,10.0]},"pe":{"bull":13,"base":11,"bear":9},"p":{"bull":20,"base":48,"bear":32},"yield_pct":{"dividend":0,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":2},"max_dd":{"lo":-62,"hi":-42,"basis":"空頭情境終點跌幅約51%為下緣錨；上一輪谷底2022年毛利率曾跌到2.67%，獲利對政策與價格高度敏感；現價已低於52週均線約17%；歷史最大回撤事實表未涵蓋，故取−42%到−62%","trigger_time":null},"basis":{"bull":"232價格重設成功、45X延續，2029年後美國新簽以0.38美元／瓦以上簽滿，CuRe加價全數實現、鈣鈦礦開始量產；13倍為現值10.5倍上調、反映政策風險降低","base":"FY2027–28在手訂單撐住，但國際量與技術加價打折，低於共識4–9%；2029年後需求斷層被232定價部分抵銷、政策支撐逐步遞減，每股盈餘高原後微降；終端11倍對照現值10.5倍（同業虧損，事實表無可比本益比）","bear":"2028年底安全港期限後需求斷層，加上45X縮減或232被稀釋，毛利率回落到FY2023年約39%以下，每股盈餘降到10美元；9倍對應成長熄火情境"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"專案須在2028年底前完工才拿得到安全港，客戶目前不下2029年單（Q3法說會CEO Mark Widmar）；在手訂單九個月由50.1降到44.0 GW；2026年全球需求預估近十年首次負成長；10-29下修全年出貨與營收財測","assumption":"基準情境假設2029–2031年每股盈餘維持在25.5–26.5美元","consequence":"若2029年後美國產能只賣出七成、單價回到約0.30美元，每股盈餘降到10美元附近，9倍約90美元，五年虧約51%","ruling":"採納，作為空頭情境主線（機率32%）。與唯一致命點部分重疊：需求斷層是漸進的，45X縮減是離散事件，兩者疊加才是最壞路徑","watch":"在手訂單GW、2029年後交貨占比、單季美國新簽","evidence_refs":["supply_demand_durability#7","cyclical_inventory_price_position#3","capital_markets_pricing#0","supply_demand_durability#0","end_markets#7"],"fact_refs":["f_kpi6_contracted_sales_backlog","f_kpi5_fy2026_guidance_q2"]},{"view":"論點失敗","evidence":"獲利約等於45X抵減；232屬總統公告，可被豁免或調整；201關稅已在2026-02到期，證明保護會到期；Q3法說會分析師提到業者遊說豁免、公用事業對價格敏感","assumption":"45X與232在五年內維持現行力道","consequence":"任一項縮減都直接削去大部分每股盈餘或美國溢價","ruling":"採納：45X列為唯一致命點，232稀釋列為短期風險；社會容忍度判紅","watch":"國會稅改條文、財政部與IRS指引、商務部232豁免公告","evidence_refs":["regulatory_antitrust#0"],"fact_refs":[]},{"view":"論點失敗","evidence":"矽晶效率持續提升，Q3法說會CEO自承Series 7 CuRe對TOPCon仍落後數美分；Qcells與T1在美國加電池產能，中國龍頭仍擴產；FSLR全球市占約2%","assumption":"CdTe在美國保有本土含量與FEOC溢價","consequence":"FEOC規則放寬或對手取得本土含量資格後，FSLR新簽單價被壓回在手訂單均價以下","ruling":"部分反駁：客戶自評對手仍有FEOC風險、CdTe在高溫地區發電表現較佳（CEO），五年內溢價縮小但不消失；反映在多頭機率下調","watch":"FEOC最終指引、對手美國產能稼動與關係人銷售比重","evidence_refs":["substitute_technology#0","competitive_share_entrants#5","competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"],"fact_refs":[]},{"view":"論點失敗","evidence":"中國自2025-02起管制碲出口，占全球精煉碲約77%；公司只向少數供應商採購、換供應商認證期長","assumption":"碲供應不中斷","consequence":"斷供即直接限制CdTe產量","ruling":"反駁為低機率（約15%）：公司已組跨部門小組、申請出口許可並找替代供應；影響大故保留監測","watch":"出口許可狀態、原料庫存天數","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"即使232奏效：TTM自由現金流率僅4.64%、Q2單季自由現金流−3.06億美元；45X應收約19億美元、存貨倉儲成本拖累營運資金（CFO）；鈣鈦礦研發2026年由約1億增至1.2億美元、2027年再增；管理層對併購更願意；Swift Current保固訴訟、對BP／Lightsource追討3.236億美元（2023年才續簽4 GW，如今對簿公堂）、證券集體訴訟；前兩大客戶各約一成","assumption":"盈餘成長能轉成每股自由現金流","consequence":"每股盈餘達標，但現金被研發、併購、訴訟與營運資金吃掉，回購只能小量，股價跟不上盈餘","ruling":"部分採納：淨現金與新授權回購提供下限，但基準情境淨回購殖利率只給0.5%","watch":"年度自由現金流／淨利、45X抵減出售或退稅入帳金額、訴訟進度","evidence_refs":["major_events#1","lawsuit_class_action#2","major_events#3","lawsuit_class_action#0","customer_concentration_credit#0"],"fact_refs":["f_kpi3_fcf","f_peer_fslr_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"共識FY2027E 23.51、FY2028E 29.65美元在10-29下修財測兩天後的快照沒有變動，近三個月FY1只上修0.29%；8月分析師目標價中位260美元在下修前；3月初始財測遠低於共識並引發降評，Morgan Stanley下修出貨與單價","assumption":"現價7.84倍FY2027E的便宜，建立在共識不再下修","consequence":"共識若跟著財測與訂單下修5–10%，便宜幅度跟著縮","ruling":"部分採納：基準情境FY2027E 22.5、FY2028E 27.0美元，低於共識4–9%；利空進入共識前凍結加碼。反駁「已反映太多樂觀」的說法：10.5倍不是追高價位，問題在分母而不在倍數","watch":"共識FY2027E每股盈餘修正幅度","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"],"fact_refs":["f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 172.97 → 本次 184.21（+6.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=172.97","side_b":"本次 price_at_dd=184.21","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 迴避","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=迴避","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、估值 🟢→🟡、均線 ❌→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 不持有","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=不持有","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、估值 🟢→🟡、均線 ❌→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 172.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 172.97 美元：Bull 價 476、Bear 價 88，五年期望值 +52.7%，基準年化 8.8%，不對稱比 3.0","side_b":"本次情境、股價仍用 172.97 美元：Bull 價 494、Bear 價 90，五年期望值 +51.6%，基準年化 10.2%，不對稱比 2.42","ruling":"先換情境、股價不動：五年期望值少 1.1 個百分點，基準年化多 1.4 個百分點。不對稱比由 3.0 變為 2.42。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 172.97 美元：五年期望值 +51.6%，基準年化 10.2%，不對稱比 2.42","side_b":"本次情境、股價 184.21 美元：五年期望值 +42.4%，基準年化 8.8%，不對稱比 2.06","ruling":"再換股價、情境不動：起點價上漲 6.5%，五年期望值少 9.3 個百分點，基準年化少 1.4 個百分點，不對稱比由 2.42 降到 2.06。合計五年期望值比前份少 10.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2029年後需求與定價","cause":null,"side_a":"管理層（2026-10-29 Q3法說會，CEO Mark Widmar、CFO Alex Bradley）：2028年後可售產能較多，預期定價與合約條件優於現有在手訂單，對2029年後本土產品需求有信心","side_b":"訂單數據：在手訂單由2025年底50.1 GW降到44.0 GW（九個月約−12%）；自上次法說只新簽1.4 GW；客戶延後2029年後早期專案採購，一筆2 GW案因州政府暫停令中止","ruling":"不可調和（方向相反：一邊說2029年後更好，一邊是2029年後沒有人下單）。站訂單數據這邊：價格可以談，量要簽了才算；基準情境2029–2031年每股盈餘高原後微降，不給管理層的定價改善全額","evidence_level":"公司揭露＋第三方報導","settle_metric":"232生效後兩季（2026Q4、2027Q1）美國新簽GW與單價、在手訂單GW","if_then":["若2026Q4與2027Q1美國新簽各≥2 GW且單價≥0.38美元／瓦，重跑判斷，通過才加碼至3%","若在手訂單跌破38 GW且單季新簽少於1 GW，減碼一半","反向：若新簽量回升但單價低於0.34美元／瓦，不加碼，代表以價換量、232保護失效"],"evidence_refs":["cyclical_inventory_price_position#3","capital_markets_pricing#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"FY2027E本益比7.84倍、PEG 0.38；淨現金約15億美元加新授權5億美元回購；232推升美國模組價格（Q3法說會分析師估矽晶漲0.10–0.20美元／瓦），FSLR是唯一不依賴中國矽晶供應鏈的整合廠，2027年約80%產能在美國；44 GW在手訂單排到2030年，2027–28年獲利能見度高","side_b":"便宜的分母靠政策；10-29下修財測才兩天，共識未動，利空尚未進模型；毛利率處歷史高點、訂單量轉弱是循環後段特徵","ruling":"不買的理由較強：利空進入共識前不加碼。買進理由要成立，必須看到232生效後新簽量價齊升，條件同上一條","evidence_level":"公司揭露","settle_metric":"共識FY2027E修正幅度、232生效後兩季美國新簽","if_then":["若共識FY2027E下修不到5%且2026Q4美國新簽≥2 GW，買進理由成立，重跑判斷","若共識FY2027E下修逾10%，維持不加碼並檢查空頭機率是否上調"],"evidence_refs":[]},{"axis":"232保護強度","cause":null,"side_a":"232最低進口價0.38美元／瓦、多晶矽衍生品15%關稅，12-04生效；商務部執法積極，已擋約60家進口商","side_b":"201關稅2026-02已到期；232公布後進口商由約200家增至約400家，CEO稱囤貨與繞道從各角度湧入；業者遊說豁免，T1申請電池進口豁免；232前已簽約的約4 GW可選擇量會以舊價成交","ruling":"可調和（程度差異）：方向對FSLR有利，力道要看2027Q1實際進口價與新簽單價；舊價可選擇量讓2027年單價改善有限","evidence_level":"公司揭露＋政府公告","settle_metric":"2027Q1美國新簽單價、232豁免公告","if_then":["若出現涵蓋主要矽晶來源的豁免或最低進口價下調，停止加碼並重估定價假設","若新簽單價≥0.40美元／瓦，定價假設提前驗證"],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"全球過剩與美國漲價並存","cause":null,"side_a":"全球模組產能逾1.1 TW對約650 GW需求，2026年全球需求近十年首次負成長，中國TOPCon出口價約0.11美元／瓦，多晶矽產能約2 TW","side_b":"美國模組中位價2026Q1升到0.28美元／瓦，本土含量合規模組供給短缺至少延續到2027年（EIA）","ruling":"可調和：市場被關稅與本土含量規則切開，切割有效就各走各的；但全球過剩是囤貨與繞道的動力，切割的有效期取決於政策，不是產業結構","evidence_level":"第三方產業資料","settle_metric":"美國模組中位價與中國出口價的價差","if_then":["若美國中位價跌回0.25美元／瓦以下，視為切割失效，空頭機率上調"],"evidence_refs":["end_markets#7","supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#7"]},{"axis":"管理層前後說法：財測與訂單","cause":null,"side_a":"2026-07-30 Q2法說會：CFO Alex Bradley稱全年財測維持不變、印度廠假設高稼動；CEO Mark Widmar稱另有逾2 GW附先決條件、約2 GW年底前高機率成交","side_b":"2026-10-29 Q3：出貨下修到16.0–17.0 GW、營收到46–49億美元、調整後EBITDA中值少5,000萬美元；印度本地出貨下修約0.7 GW，本地單價僅約0.20美元／瓦；自上次法說僅新簽1.4 GW；3月時初始財測已遠低於共識並引發降評","ruling":"可調和但扣分：下修集中在低毛利的印度與國際產品，美國全本土出貨區間不變，獲利影響小；但管理層對訂單管道的樂觀已落空一次，基準情境對其訂單管道陳述打五折","evidence_level":"公司揭露","settle_metric":"2027年財測（預計2027-02）出貨與營收中值","if_then":["若2027年營收財測中值低於共識59.5億美元10%以上，重跑判斷並下修基準情境"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2","end_markets#3"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭惡化：中國龍頭續擴電池產能，Qcells、T1在美國加電池產能，TOPCon效率領先數美分","side_b":"結構轉好：232與FEOC規則讓本土整合供應鏈稀缺；其他結構變數：客戶由框架合約轉向單一專案合約，能見度縮短","ruling":"雙向拉鋸：政策面結構轉好，競爭面與商業模式面同時轉差，淨效果要看232執行","evidence_level":"公司揭露＋第三方報導","settle_metric":"美國新簽單價對市場中位價的溢價","if_then":["若溢價收斂到0.03美元／瓦以內，判競爭惡化勝出，減碼三分之一"],"evidence_refs":["cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"axis":"前份漂移：綜合評級、估值結論、循環位置、裁決與角色","cause":"新證據","prior_field":["signal","val","cycle_position"],"side_a":"前份（2026-09-29，股價172.97美元）：綜合評級B、估值🟢、循環位置中循環、裁決進場、角色衛星","side_b":"本次：綜合評級C、估值🟡、循環位置晚循環；裁決與角色由程式依本次輸入重算","ruling":"主因是新證據：10-29下修全年出貨與營收財測；Q3毛利率約58%創新高但營收年減23%；在手訂單降到44 GW、新簽僅1.4 GW；Q3法說揭露2026年預估45X抵減約21億美元、高於共識淨利，分母能否延續成為爭點，便宜論證失效。毛利在峰、量在降、訂單在縮，循環位置由中段移到後段。股價上漲約6.5%只是次要因素","evidence_level":"公司揭露","settle_metric":"232生效後兩季美國新簽與在手訂單","if_then":["若232生效後兩季新簽量價齊升，循環位置回調為中循環並重評綜合評級"],"evidence_refs":["capital_markets_pricing#0","cyclical_inventory_price_position#3"]},{"axis":"前份漂移：維持不變的欄位","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：陷阱風險🟡、護城河方向→、五年後成長空間🟡、類型循環/商品","side_b":"本次相同","ruling":"新證據雙向抵銷，結論不變：232強化本土定價（正）對上在手訂單連降、對手在美國擴產（負）；衰退信號亮2項，陷阱風險維持；毛利率峰谷擺動逾50個百分點、2022年虧損，循環/商品類型不變","evidence_level":"公司揭露＋第三方報導","settle_metric":"衰退信號亮燈數、在手訂單","if_then":["若FY2026自由現金流／淨利低於0.75，衰退信號增至3項，陷阱風險升為紅"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率25%、空頭30%、最大回撤−55%（單點）","side_b":"本次：多頭20%、基準48%、空頭32%；最大回撤改為區間−42%至−62%","ruling":"情境樹依本次共識重建：共識三年每股盈餘年化27.8%超出內生上界約16.5%，空頭機率不得低於30%；2029年後需求斷層證據轉強，多頭機率下調5個百分點；回撤改用區間，下緣須覆蓋空頭終點跌幅約51%","evidence_level":"本次推導","settle_metric":"在手訂單與新簽","if_then":["若在手訂單跌破38 GW，空頭機率上調至40%"],"evidence_refs":[]},{"axis":"前份漂移：加碼重啟門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","side_b":"232生效後連兩季美國新簽各≥2 GW且單價≥0.38美元／瓦，且週收盤站回104週均線（約201美元）之上，才重跑判斷並考慮加碼","ruling":"前份門檻在Q3受測：美國新簽1.4 GW未達2 GW，單價0.36美元達標、股價站上250週均線達標，條件未成立、未觸發。新的加碼門檻改為232生效後兩季，單價提高到0.38美元以反映矽晶漲價、並濾掉232前已談定的訂單；技術面改看104週均線，因股價已在250週均線之上，舊線不再有篩選力","evidence_level":"公司揭露","settle_metric":"2026Q4與2027Q1美國新簽、週收盤價","if_then":["兩季皆達標且站回104週均線，重跑判斷後加碼","任一季新簽少於1 GW，門檻重設並維持不加碼"],"evidence_refs":["cyclical_inventory_price_position#3"]},{"axis":"Single Thing變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份Single Thing：無（未記錄）","side_b":"本次Single Thing：美國45X先進製造稅額抵減被立法取消、提前退場或可轉讓／可退還機制被收緊","ruling":"前份未設唯一致命點；本次依最大單一敏感度選定：抵減規模約等於全年淨利，232稀釋或需求斷層的影響都在其一半以下；法案通過即清倉","evidence_level":"公司揭露","settle_metric":"國會立法進度、財政部與IRS指引","if_then":["法案通過即清倉","法案進入委員會審議即減碼一半"],"evidence_refs":[]},{"axis":"前份漂移：減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份：無指標門檻（未記錄）","side_b":"本次：在手訂單跌破38 GW減碼、美國新簽單價連兩季低於0.32美元減碼、TTM毛利率低於40%減碼、45X法源生變清倉、FY2027自由現金流為負停止加碼","ruling":"前份未設，本次新設；門檻取自本次三條論點的反轉線，不沿用前份","evidence_level":"本次推導","settle_metric":"各指標季度讀數","if_then":["任兩項同時觸發，減碼至零"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"232生效後美國新簽量價回升，驗證本土定價重設","type":"假設驗證","maps_to":"H1","metric":"美國季度新簽GW與平均單價（含技術加價）","threshold":"連兩季各≥2 GW且≥0.38美元／瓦","action":"達標即重跑判斷，通過才加碼至3%","source_freq":"季報新聞稿與法說會，每季","date":"2027-05","evidence_refs":[]},{"n":2,"text":"在手訂單持續下滑，2029年後需求斷層成形","type":"風險","maps_to":"R2","metric":"在手訂單GW","threshold":"跌破38 GW，或連4季下滑","action":"減碼一半","source_freq":"季報，每季","date":"2027-02","evidence_refs":["cyclical_inventory_price_position#3","supply_demand_durability#7"]},{"n":3,"text":"45X抵減被立法取消、提前退場或轉讓與退稅機制收緊","type":"Single Thing","maps_to":"single_thing","metric":"45X法源與IRS指引","threshold":"相關法案經國會通過或財政部發布收緊指引","action":"法案通過即清倉；進入委員會審議即減碼一半","source_freq":"國會立法進度、財政部公告，事件驅動","date":null,"evidence_refs":[]},{"n":4,"text":"232保護被豁免或最低進口價下調","type":"風險","maps_to":"R1","metric":"232豁免公告、最低進口價","threshold":"出現涵蓋主要矽晶進口來源的豁免，或最低進口價低於0.38美元／瓦","action":"停止加碼，重估定價假設","source_freq":"商務部公告，事件驅動","date":"2026-12","evidence_refs":["regulatory_antitrust#0","end_markets#7"]},{"n":5,"text":"重新考慮加碼的條件","type":"估值rearm","maps_to":"H1","metric":"美國新簽量價＋週收盤價對104週均線","threshold":"232生效後連兩季美國新簽各≥2 GW且≥0.38美元／瓦，且週收盤高於104週均線（約201美元）","action":"重跑判斷，通過才加碼","source_freq":"季報＋週線，每週","date":"2027-05","evidence_refs":[]},{"n":6,"text":"毛利率從歷史高點回落","type":"減碼","maps_to":"H2","metric":"TTM毛利率（含45X）","threshold":"連兩季低於42.75%","action":"減碼三分之一","source_freq":"10-Q，每季","date":"2027-02","evidence_refs":[]},{"n":7,"text":"Swift Current保固訴訟、BP／Lightsource追討與證券集體訴訟","type":"風險","maps_to":"R5","metric":"判賠或和解金額、集體認證","threshold":"單案逾3億美元，或集體訴訟通過集體認證","action":"減碼一半","source_freq":"10-Q法律程序附註，每季","date":null,"evidence_refs":["major_events#1","major_events#3","lawsuit_class_action#0","lawsuit_class_action#2"]},{"n":8,"text":"碲供應受阻","type":"風險","maps_to":"R4","metric":"出口許可狀態、原料庫存天數","threshold":"許可遭拒或庫存低於一季用量","action":"減碼一半","source_freq":"10-K／10-Q風險因子，每季","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"n":9,"text":"2027年財測與馬來西亞廠去留複審","type":"複審日期","maps_to":"H3","metric":"2027年出貨、營收、資本支出財測","threshold":"營收財測中值低於共識FY2027E營收59.5億美元10%以上","action":"重跑判斷","source_freq":"年度財測","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"在手訂單（GW）","bear_threshold":"跌破38 GW","window":"2027年底前任一季","source":"季報新聞稿","last_status":"warning"},{"metric":"美國新簽平均單價（含技術加價）","bear_threshold":"連兩季低於0.32美元／瓦","window":"2027全年","source":"季報法說會","last_status":"ok"},{"metric":"TTM毛利率（含45X）","bear_threshold":"低於40%","window":"滾動4季","source":"10-Q／10-K","last_status":"ok"},{"metric":"45X先進製造稅額抵減法源","bear_threshold":"立法取消、提前退場或轉讓與退稅機制收緊","window":"未來24個月","source":"國會立法、財政部與IRS公告","last_status":"ok"},{"metric":"年度自由現金流","bear_threshold":"FY2027為負","window":"FY2027","source":"10-K現金流量表","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"232生效後連兩季美國新簽各≥2 GW且單價≥0.38美元／瓦，且週收盤站回104週均線（約201美元）之上，才重跑判斷並考慮加碼","exec_line":"現有部位持有不加、不追；等2026Q4與2027Q1兩季新簽數據；在手訂單跌破38 GW或單季新簽少於1 GW減碼一半；45X法源被取消即清倉","holding_cap":"≤3%，深回撤心理準備"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等事件不等價：12-04 Section 232生效後兩季（2026Q4、2027Q1）美國新簽各≥2 GW且單價≥0.38美元／瓦，且週收盤站回104週均線（約201美元）","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"進場","prior_role":"衛星"},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='迴避'"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Section 232生效後，美國本土製模組的新簽單價明顯高於在手訂單均價（約0.31美元／瓦），且量能恢復","2y":"2027年美國新簽單價≥0.38美元／瓦、單季新簽≥2 GW","5y":null,"10y":null,"threshold":"連兩季美國新簽各≥2 GW且單價≥0.38美元／瓦","source":"季報新聞稿與法說會新簽數據；商務部232最低進口價公告","drift_rule":"新簽單價連2季低於0.36美元（約低5%）為削弱，連3季低於0.34美元（約低10%）為反轉"},{"id":"H2","text":"美國產能占比升到約80%加上CuRe技術加價，含45X的毛利率在FY2027維持45%以上","2y":"FY2027全年毛利率≥45%","5y":null,"10y":null,"threshold":"TTM毛利率≥45%（目前49.25%）","source":"10-Q／10-K損益表；法說會毛利拆解","drift_rule":"TTM毛利率連2季低於42.75%（低5%）為削弱，連3季低於40.5%（低10%）為反轉"},{"id":"H3","text":"2029年後美國可售產能能以不低於在手訂單均價的條件簽滿，在手訂單止跌","2y":null,"5y":"2029–2031年美國廠稼動率維持九成以上，在手訂單回到45 GW以上","10y":null,"threshold":"在手訂單≥40 GW，且2027年起年度新簽對出貨比≥1","source":"季報在手訂單GW、合約金額與交貨年度分布","drift_rule":"在手訂單連4季低於門檻5%以上（38 GW）為削弱，連6季低於門檻10%以上（36 GW）為反轉"}],"R":[{"id":"R1","text":"232保護被豁免、囤貨與第三國繞道稀釋，新單價格發現失敗，客戶持續延後採購","h_ref":"H1","clock":"⚡","threshold":"2027Q1前出現大範圍豁免或最低進口價下調，或連2季美國新簽少於1.5 GW","evidence_refs":["regulatory_antitrust#0","supply_demand_durability#0","supply_demand_durability#1","end_markets#7"]},{"id":"R2","text":"2028年底安全港期限後美國公用事業級需求斷層，加上地方暫停令與電池漲價，2029年後產能簽不滿","h_ref":"H3","clock":"🔥","threshold":"在手訂單連4季下滑且跌破38 GW","evidence_refs":["cyclical_inventory_price_position#3","capital_markets_pricing#0","supply_demand_durability#7","capital_markets_pricing#1","capital_markets_pricing#2"]},{"id":"R3","text":"矽晶TOPCon效率持續拉開、美國本土矽晶產能放量，CdTe溢價縮小","h_ref":"H2","clock":"🐢","threshold":"美國新簽對市場中位價的溢價收斂到0.03美元／瓦以內，或FEOC規則放寬使對手取得本土含量資格","evidence_refs":["substitute_technology#0","competitive_share_entrants#5","competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"id":"R4","text":"中國碲出口管制收緊或少數供應商斷供，CdTe產線受限","h_ref":"H2","clock":"🔥","threshold":"公司揭露出口許可遭拒，或原料庫存低於一季用量","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"id":"R5","text":"Series 7早期品質問題引發保固訴訟擴大（Swift Current案），加上對BP／Lightsource 3.236億美元應收款追討失利與證券集體訴訟","h_ref":"H2","clock":"⚡","threshold":"單案判賠或和解逾3億美元，或集體訴訟通過集體認證","evidence_refs":["major_events#1","major_events#3","lawsuit_class_action#0","lawsuit_class_action#2","customer_concentration_credit#0"]}],"single_thing":{"description":"美國45X先進製造稅額抵減被立法取消、提前退場，或可轉讓與可退還機制被收緊","why_fatal":"2025年認列約16億美元，高於全年淨利15.3億美元；2026年預估產生約21億美元，高於共識淨利約18.8億美元，等於獲利幾乎全部來自這項抵減","if_happens":"每股盈餘回到個位數，終端價值落向空頭情境約90美元以下；法案通過即清倉","how_monitor":"國會稅改與預算法案條文、財政部與IRS對45X及FEOC的指引、公司季報抵減產生額與出售價格","probability":"12–24個月約10%（事實表未涵蓋立法動態；依公司財測假設政策延續、商務部長親自為南卡廠剪綵所示的政策方向推估）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":7.84,"peg_fy2":0.28,"stress":{"pass":3,"total":6}},"eps_meta":{"base_eps_path":{"FY2025A":14.21,"FY2026E":17.48,"FY2027E":23.51,"FY2028E":29.65},"fy_end_month":12,"eps_basis":"FY2025A取年報稀釋EPS；FY2026E–FY2028E為Koyfin快照共識，事實表未註明GAAP或調整後口徑"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"Section 232最低進口價與多晶矽衍生品關稅12-04生效","impact":"高","watch":"豁免名單、囤貨執法、232前已進口庫存的消化速度"},{"date":"2027-01","date_precision":"quarter","type":"regulatory","event":"FEOC最終指引公布（管理層預期年底或明年初）","impact":"高","watch":"美國本土矽晶對手能否取得合規資格"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026Q4財報與2027全年財測","impact":"高","watch":"美國新簽GW與單價、在手訂單、2027年出貨與營收中值"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"232前舊價可選擇量約4 GW中約一半在5個月內到期決定","impact":"中","watch":"客戶行使比例與成交單價"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"印度廠首條Series 7 CuRe轉換啟動","impact":"中","watch":"轉換良率與對美國後段的供料"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"馬來西亞1.8 GW廠滿載或停產二選一；俄亥俄鈣鈦礦試產線就緒；南卡第二期商轉","impact":"中","watch":"國際產品需求、停產費用、鈣鈦礦田間數據"}]}
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
