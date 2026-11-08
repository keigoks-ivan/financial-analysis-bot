你是 DD 管線 v20 的判斷層閘（gate），標的 SN（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝1976.4 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未驗證（僅第三方稱 adj EPS $2.34 vs consensus $1.87，新聞稿無此數）
- `f_kpi1_adjusted_non_gaap_operat`（q1_business）｜Adjusted (Non-GAAP) operating income / margin＝21.5 % margin（$425.5m，YoY +47.2%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝22.4 % margin（$442.9m，YoY +68.5%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results；含 $109.6m IEEPA 關稅退款（不計入 adjusted）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi3_gross_margin_gaap_adjust`（q1_business）｜Gross margin GAAP / Adjusted＝59.2 % GAAP（Adjusted 55.9%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi7_guidance_fy2026`（q1_business）｜Guidance FY2026（上修）＝net sales +18.0%~19.0%（前次 16~17%）；adj EPS $6.65~6.75（前次 $6.45~6.55）；adj EBITDA $1,380~1,391m（前次 $1,357~1,369m） range｜期間與口徑：Q3 FY2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 Q3 2026 Results；稅率約 22~23%、稀釋股數約 142.0m、capex $190~210m；新聞稿無單獨 Q4 指引（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（公告於 2026-11-04））
  - 註記：FY1 共識 EPS $6.59（dd_numbers_extra.py consensus_revision，財報前快照）；指引中位 $6.70 高於該值
- `f_kpi8_net_sales_by_category_cl`（q1_business）｜Net sales by category（Cleaning / Cooking&Beverage / Food Prep / Beauty&Home Env）＝617.2 (+4.1%) / 597.7 (+36.6%) / 485.5 (+18.3%) / 276.1 (+45.8%) USD m｜期間與口徑：Q3 FY2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results；Domestic $1,313.7m +19.4%、International $662.7m +25.2%（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（公告於 2026-11-04））
- `f_peer_sn_gross_margin_pct`（q2_moat）｜SN 毛利率＝51.45 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sn_operating_margin_pct`（q2_moat）｜SN 營業利益率＝15.58 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sn_fcf_margin_pct`（q2_moat）｜SN FCF 利潤率＝6.8 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hele_gross_margin_pct`（q2_moat）｜HELE 毛利率＝47.37 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HELE.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hele_operating_margin_pct`（q2_moat）｜HELE 營業利益率＝9.4 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HELE.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hele_fcf_margin_pct`（q2_moat）｜HELE FCF 利潤率＝8.06 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HELE.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nwl_operating_margin_pct`（q2_moat）｜NWL 營業利益率＝8.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NWL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_whr_operating_margin_pct`（q2_moat）｜WHR 營業利益率＝2.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WHR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝6.59 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.67 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.76 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝7641.24 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝8720.29 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_free_cash_flow_fcf`（q4_capital）｜Free cash flow（僅有前九個月，新聞稿未列單季與 FCF 定義）＝-17.2 USD m（九個月：營業現金流 $107.4m − 資本支出 $124.6m，本欄為自行換算）｜期間與口徑：YTD 9M FY2026（至 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results 現金流量表（numbers.latest_quarter_kpis.items[4]，as_of YTD 9M FY2026（至 2026-09-30，公告於 2026-11-04））
- `f_kpi5_share_based_compensation`（q1_business）｜Share-based compensation＝42.0 USD m（占 GAAP 營業利益 9.5%、占營收 2.1%，由兩數換算）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 Results（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝424.84 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 912.66、現金 487.82（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝140.91 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝222.95 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝33.83 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 6.59，分子＝快照價 222.95｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝37.41 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝86.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝86.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 6.59 → 6.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝99.65 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝137.88 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝-｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 222.95 / W52 137.88 / W104 118.7 / W250 None / W250 13週斜率 None%」
- `f_ma_w104`（q5_valuation）｜104 週均線＝118.7 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K風險因子：部分對手可能降價並接受較低利潤，公司可能流失市佔。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 最大客戶占淨銷售 23.8%；Amazon、Costco、Walmart 各逾 10%，合計 45.7%
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：客戶 A 占營收 23.8%（2024 23.1%、2023 19.9%）、B 11.4%、C 10.5%；客戶 A 占應收帳款 22.0%（2024 為 29.1%）
  - 來源：SEC EDGAR 10-K FY2025 財報附註（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Allianz Trade 預期無房屋換手回升則 2026–2027 家電銷量無復甦；中國補貼提前拉貨留下餘波；高端區塊比量販區塊撐得住；美國僅約四分之一家電為本土生產；記憶體晶片短缺推高 BOM。
  - 來源：Allianz Trade, household equipment sector report（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 稱美國貿易政策變動（進口關稅）已對公司造成並預期持續造成重大不利影響；大部分產品在中國、越南等美國以外地區製造；2026-02-20 最高法院裁定推翻部分 IEEPA 關稅，政府宣布以其他法律徵收新關稅
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：大部分產品在中國、越南等美國以外地區製造，美國政策使取得海外製品更困難或更昂貴，已影響並可能持續影響銷售與獲利
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：CFO 稱關稅為 2026 Q1 的 sizable headwind；展望假設中國、越南等數個東南亞國家基準關稅 10%
  - 來源：Supply Chain Dive, SharkNinja leverages production flexibility to mitigate tariffs（as_of 2026-05-07）｜affects：thesis.R、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露重要比例產品在中國、越南及其他非美地區製造，美國政策變動影響淨銷售與獲利，他國報復性關稅可能影響出口
  - 來源：SharkNinja FY2025 Form 10-K (SEC)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：SharkNinja 10-K 風險因子自陳技術變化加速（AI、機器人、感測器等），未能適應可能不利營運
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：瑞士零售商資料顯示中國品牌 Dreame、Roborock 已幾乎接管機器人吸塵器品類，Dyson 傳統吸塵器份額下滑
  - 來源：Digitec/Galaxus, Chinese vacuum cleaner brands are blowing away their global competition（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：董事會2026-07-10批准董事長CJ Xuning Wang一次性限制期豁免，其出售部分持股予既有機構投資者
  - 來源：SEC EDGAR 8-K Item 8.01（as_of 2026-07-13）｜affects：decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：Foodi OP300壓力鍋召回（CPSC #25-247，180萬台、106起燙傷）；後續消費者集體訴訟，N.D. Cal. Biscovich案獲早期駁回（2026-03）
  - 來源：Shook Hardy & Bacon news 2026 / CBS News（as_of 2026-03-01）｜affects：decision_inputs.bear
- `major_events#4`（major_events｜方向 -｜狀態 ok）：FY2025 10-K（2026-03-02）：二手報導稱公司揭露財報內控重大缺陷、審計師對ICFR出具否定意見；未見重編報導（二手來源，未核10-K原文）
  - 來源：rallies.ai: SharkNinja slides as internal-control weaknesses resurface（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：CPSC召回Foodi OP300壓力鍋180萬台（#25-247，2025-05-01，約在12個月窗口之前）；搜尋未見2026新召回
  - 來源：CBS News / CPSC recall #25-247（as_of 2025-05-01）｜affects：decision_inputs.bear
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：未見SEC調查或重編報導；近12個月8-K無Item 4.02。但二手報導稱FY2025內控有重大缺陷、ICFR否定意見
  - 來源：rallies.ai / SEC EDGAR 8-K 清單（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":447.2,"bear_5y_price":103.6,"p_bull_pct":25,"p_bear_pct":25,"upside_5y_pct":24.3,"ev5y_pct":23.9,"irr_base_pct":4.5,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":6.7,"pe":33.28,"basis":"FY2026 全年調整後 EPS，用 2026-11-04 上修後指引中值 6.70；共識 6.59 是財報前快照。起點與終端都用當年度 EPS 口徑。"},"eps":{"bull":[8.3,10.0,12.0,14.4,17.2],"base":[7.8,9.0,10.2,11.4,12.6],"bear":[6.9,6.8,6.9,7.1,7.4]},"pe":{"bull":26,"base":22,"bear":14},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.0,"net_buyback":0.2},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SN_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：FY2026 淨銷售成長財測上調（原話："we now expect net sales to increase between 16% and 17%"）
- 2026-08-05｜CFO｜guidance：FY2026 調整後 EPS 財測區間與前次比較（原話："$6.45 to $6.55 compared to $6 to $6.10 previously."）
- 2026-08-05｜CFO｜guidance：FY2026 調整後 EBITDA 財測區間（原話："in the range of $1.36 billion to $1.37 billion"）
- 2026-08-05｜CFO｜guidance：EPS 上調 $0.45 中關稅退款貢獻口徑（原話："is associated with the expected net tariff refund benefit."）
- 2026-08-05｜CFO｜guidance：關稅退款認列金額與時點（原話："recognize a benefit of approximately $247.1 million as a"）
- 2026-08-05｜CFO｜margin：2026 年度關稅退款納入調整後指標的口徑（原話："will be reflected in these same adjusted metrics as part"）
- 2026-08-05｜CFO｜guidance：財測假設關稅維持現況（原話："assumes current tariff levels persist for the remainder"）
- 2026-08-05｜CFO｜guidance：仍預期全年調整後 EBITDA 成長高於淨銷售成長（原話："anticipate adjusted EBITDA growing ahead of net sales"）
- 2026-08-05｜CFO｜margin：毛利率壓力主因（原話："primary headwind due mostly to the annualization"）
- 2026-08-05｜CFO｜margin：調整後營業費用率連續第五季槓桿（原話："driven leverage on adjusted operating expense as a"）
- 2026-08-05｜CFO｜margin：獲利目標定義（原話："full year adjusted EBITDA growth that outpaces"）
- 2026-08-05｜CFO｜margin：Q2 調整後 EBITDA 利潤率下滑幅度（原話："adjusted EBITDA margin, down approximately 50 basis points"）
- 2026-08-05｜CFO｜margin：DTC／社群電商結構性毛利較高（原話："commerce does come at a higher structural gross margin."）
- 2026-08-05｜CFO｜capital_allocation：管理層選擇將部分退款再投資（原話："We are opportunistically choosing to reinvest a portion of"）
- 2026-08-05｜CFO｜capital_allocation：Q2 買回金額（原話："repurchased roughly $100 million worth of stock"）
- 2026-08-05｜CFO｜capital_allocation：買回採機動執行（原話："continue to utilize the program opportunistically."）
- 2026-08-05｜CFO｜capital_allocation：資本支出預期偏高端（原話："tracking toward the high end"）
- 2026-08-05｜CEO｜commitment：美國＋加拿大下半年雙位數成長（原話："double-digit second half number for the domestic business."）
- 2026-08-05｜CEO｜commitment：DTC 與聯盟行銷成長快於其他業務至 2027 年底（原話："to grow at a faster rate than the rest of the business"）
- 2026-08-05｜CEO｜commitment：2027 年大致持平人力下維持成長（原話："on roughly flat headcount as we get into '27."）
- 2026-08-05｜CEO｜commitment：每年至少推出 2 個新子類別（原話："we would launch in a minimum of 2 subcategories a year."）
- 2026-08-05｜CEO｜commitment：TikTok Shop 國家數目標（原話："goal of more than double that number by this holiday season."）
- 2026-08-05｜CEO｜commitment：經銷商轉直營告一段落（原話："now done for the foreseeable future with these distributor"）
- 2026-08-05｜CEO｜commitment：將推動零售商庫存於 Q4 增加（原話："push for inventory levels to grow as we head into"）
- 2026-08-05｜CEO｜risk：分析師懷疑雙位數成長可持續性（管理層轉述）（原話："hard to believe that double-digit growth in a business"）
- 2026-08-05｜CEO｜risk：加拿大 Q2 衰退（原話："The Canada business was down 17% as we flow"）
- 2026-08-05｜CEO｜risk：歐洲 DTC 轉換對 Q2 的影響（原話："they may even have a little bit of hurt"）
- 2026-08-05｜CFO｜risk：Q2 POS 高於出貨主因為 Prime Day 時點（原話："largely driven by the timing of Prime Day."）
- 2026-08-05｜CEO｜customer：TikTok Shop 國家數（原話："TikTok Shop in 7 countries compared to 0 in the year ago"）
- 2026-08-05｜CFO｜customer：零售商庫存（原話："Overall, the retailer inventory is extremely healthy."）
- 2026-08-05｜CEO｜customer：歐洲零售商是否調整年度陳列（原話："Some are simply not."）
- 2026-08-05｜CEO｜product：既有品類成長範圍（原話："typically grow mid- to high single digits."）
- 2026-08-05｜CEO｜product：新品多數落在既有品類（原話："products we launch each year go into existing categories."）
- 2026-08-05｜CFO｜product：清潔類 Q2 成長（原話："Cleaning category increased 4.1% year-over-year"）
- 2026-08-05｜CFO｜product：美容與居家環境類 Q2 成長（原話："Beauty and Home Environment category increased 65.3%"）
- 2026-08-05｜CEO｜product：電扇缺貨（原話："we sold out and couldn't capture all"）
- 2026-08-05｜CEO｜product：第 41 個子類別 Q3 末進入（原話："we'll be entering into our 41st subcategory"）
- 2026-08-05｜CEO｜product：AI 提升社群內容擷取率（原話："AI has lifted our capture rate to 60% plus accuracy"）
- 2026-08-05｜CEO｜product：AI 專案數量（原話："bet projects and 20 quick win projects."）
- 2026-08-05｜CEO｜product：AI 專案兩週檢視機制（原話："tangible progress on an initiative every 2 weeks"）
- 2026-08-05｜CEO｜product：Palantir 二期專案（原話："moved ahead with a Phase 2 initiative with Palantir"）
- 2026-08-05｜CEO｜product：AWS 媒體優化系統上線時程（原話："going live at the end of September on a system"）
- 2026-08-05｜CEO｜product：AWS 系統效益多在 2027 年（原話："really for the most part, that won't scale until '27."）
- 2026-08-05｜CEO｜competition：歐洲品類滲透率估計（原話："less than 10% penetrated on an overall category basis"）
- 2026-08-05｜CEO｜competition：年底可觸及 TAM 估計（原話："$125 billion to $130 billion available TAM"）
- 2026-08-05｜CEO｜competition：管理層對市場與自身創造需求的說法（原話："getting consumers excited about our products"）

### 問答異常語氣（迴避／改口／保留）
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Randy Konik 問 DTC 與批發毛利差距，及行銷費用是否有槓桿空間｜答法：CFO 只說 DTC／社群電商結構性毛利較高，未給差距數字，也未回應行銷槓桿問題
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Brooke Roach 問美國 DTC 業務目前規模｜答法：CEO 答不拆分 D2C 占比，改談成長快於其他業務與 Salesforce 上線
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Steven Forbes 問相較去年錯過陳列日期，今年美國零售商陳列有何實質變化｜答法：CEO 先談歐洲與新通路，美國部分講 Walmart／Target 等促銷，未直接回答去年錯過陳列日的比較

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260619","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"創新引擎可持續命中爆品（hit 接棒）","columns":{"2Y 驗證點":"每年 ~25 款新品中 ≥2-3 款成為千萬美元級爆品","5Y 驗證點":"新品類（戶外/家居環境/Beauty）合計營收佔比升至 ≥ 25%","10Y 驗證點":"研發命中率不衰減，品類數持續擴張","具體數字門檻":"整體營收 CAGR ≥ 10%；Beauty &amp; Home Env 維持 &gt; 20% 成長","信息來源":"公司法說（Q 報品類拆分）","漂移觸發":"連 2 季整體營收 &lt; +8% → 削弱（2Y 假設）"}},{"id":"H2","text":"供應鏈出中國 + 關稅可控（margin 不被吃）","columns":{"2Y 驗證點":"東南亞產能滿載、adj GM 維持 ~48%","5Y 驗證點":"SE Asia 多地分散降低單一國地緣風險","10Y 驗證點":"長期 GM 結構穩定 &gt; 47%","具體數字門檻":"adj GM（扣關稅一次性）≥ 47%；FY26 adj EPS ≥ $6.00（guide 下緣）","信息來源":"Q1'26 法說 + 8-K（5/6）","漂移觸發":"連 4 季 adj GM &lt; 47% → 削弱（5Y margin 假設）"}},{"id":"H3","text":"估值維持 high-teens~low-20s fwd PE（不 de-rate 至成熟期倍數）","columns":{"2Y 驗證點":"fwd PE FY27 維持 18-24x","5Y 驗證點":"成長放緩前不被重設至 De'Longhi 13.5x 級","10Y 驗證點":"市場持續給予「成長性溢價」","具體數字門檻":"fwd PE FY27 ≥ 16x（否則向消費電器成熟期收斂）","信息來源":"市場估值（Koyfin/yfinance）","漂移觸發":"fwd PE &lt; 16x 持續 → 反轉（市場 de-rate）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"消費降溫 + 爆品退潮 → 營收增速失速","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季營收 YoY、Beauty/Food Prep 增速","警戒閾值":"整體連 2 季 &lt; +8%"}},{"id":"R2","text":"關稅上修 / 促銷加劇 → adj GM 壓縮","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"adj GM（扣一次性）、東南亞稅率","警戒閾值":"連 4 季 adj GM &lt; 47%；SE Asia 稅率 ≥ 20%"}},{"id":"R3","text":"私牌/競品侵蝕 + 創新引擎衰減 → pricing power 結構下滑","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"新品命中率、ASP 趨勢、市佔","警戒閾值":"連續 ≥ 2 年新爆品數下滑 + ASP 下行（需 ≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":140.84,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"SharkNinja, Inc."},"oneliner":"SharkNinja 連 14 季雙位數成長，生意沒問題，問題在價格：26 週翻倍後約 29 倍 FY2027 EPS，Q3 獲利跳升有很大一塊是關稅退款。要賺 12% 年化，五年 EPS 得年增約 18% 且 2031 年還值 26 倍，現價不追，170 美元以下再看。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/scenario.json","answers":{"q1_business":{"verdict":"SharkNinja 賺的是美國與歐洲家庭添購和更換小家電的錢，靠新品和內容創造購買理由，錢最後要過三家大零售商這一關。","reasoning":"Q3 淨銷售 19.764 億美元，年增 21.2%。四個品類都超過營收一成：清潔 31%、烹飪飲品 30%、食物料理 25%、美容居家環境 14%；美加占 66.5%，國際占 33.5%。調整後毛利率 55.9%、調整後營業利益率 21.5%，但兩者都含 1.34 億美元屬於 FY2026 的關稅退款。CFO 在 2026-11-04 法說表示，扣掉退款毛利率約年減 100 個基點，換算約 49.1%。單點依賴在通路：FY2025 Amazon、Costco、Walmart 合計 45.7%，最大客戶由 2023 年的 19.9% 升到 23.8%。製造外包，主力 SKU 有多家工廠，這點是公司自述。成長的集中度比表面高：Q3 增加的 3.46 億美元裡，烹飪飲品和美容居家環境占 71%，清潔只占 7%。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_non_gaap_operat","f_kpi2_gaap_operating_income_ma","f_kpi3_gross_margin_gaap_adjust","f_kpi7_guidance_fy2026","f_kpi8_net_sales_by_category_cl"],"verdict_values":{"revenue_quality":"中上。增長以銷量和品類擴張為主，公司今年延後漲價；但 Q3 調整後利潤含退款，美國出貨也含假期檔進貨，兩者要到 2027 上半年才看得清。","unit_econ_note":"媒體和促銷每年合計超過 15 億美元，約占 FY2026 營收兩成，單位經濟要看行銷效率。事實表沒有客單價、分通路毛利或回購率；DTC 毛利較高，但公司不揭露占比（2026-08-05 法說）。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"多品類消費硬體、外包製造、高行銷投入，成長靠新品命中，沒有訂閱或合約收入墊底。"},"industry":{"clock_phase":"IV","sd_verdict_source":"需求端週期偏弱，供給可逆性高。Allianz Trade 預期房屋換手不回升則 2026–2027 家電銷量不復甦，GfU 估歐洲大家電以換機為主；這些來源偏大家電，只能間接代表小家電。外包產能容易擴張，SN 的超額成長靠份額與新品，不靠產業回升。","bargaining":{"up":"代工廠分散，主力 SKU 有多於一家工廠（公司自述）；Q3 另提列約 4,500 萬美元給工廠夥伴，顯示關稅損失有一部分要分回供應端。","down":"三大零售商合計 45.7%，最大客戶 23.8% 且三年上升；公司靠 DTC、社群電商和區域平台降低依賴。","geo":"大部分產品在中國、越南及其他非美地區製造；Q3 指引假設中國、越南、泰國 12.5%，印尼、馬來西亞、柬埔寨 10%。"},"profit_pool_dir":"五年利潤池占比事實表未涵蓋。只能從同業利潤率間接看，SN 的 TTM 營業利益率高於 HELE、NWL、WHR，但 TTM 含退款。","tam_table":[{"item":"總市場（公司自估）","value":"三年前 1,120 億美元，現約 1,300 億美元（CEO，2026-11-04）"},{"item":"可服務市場（公司舊數）","value":"全球 390 億、美國 160 億美元，是分析師 2026-11-04 引用的三年前數字；CEO 當場只更新總市場"},{"item":"全球滲透率","value":"FY2026 營收約 75.8 億美元，占總市場約 5.8%，占三年前全球可服務市場約 19%"},{"item":"美國滲透率","value":"以 Q3 美國占比 61.7% 粗算約 47 億美元，約為三年前美國可服務市場的 29%、總市場 380 億的 12%"},{"item":"歐洲","value":"CEO 估品類滲透率不到 10%（2026-08-05）"},{"item":"新增品類","value":"淨水和微波爐合計增加近 100 億美元總市場；淨水公司估 60 億美元以上"},{"item":"分段年化成長與利潤池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"→ 競爭優勢穩定：執行力還在變強，定價力沒有新證據，不標擴大。","reasoning":"機制是把消費者痛點快速做成新品，再用社群內容和多品類陳列放大。可驗證的方向有兩個：Q3 營收年增 21.2%，可得的產業預估只有低到中個位數，等於在拿份額；TTM 營業利益率 15.58%，高於 HELE 9.40%、NWL 8.38%、WHR 2.05%。折扣也有三個。第一，TTM 含約 1.99 億美元淨退款，約 2.7 個百分點，扣掉後對 HELE 的領先由 6.2 點縮到約 3.4 點，這是下限，因為再投資費用沒有加回。第二，份額都是公司自述或公司引用 Circana，事實表找不到具體市佔數字。第三，最大品類清潔連兩季只長 4.1%。事實表沒有投入資本，同業 ROIC 差距算不出來。AI 目前是成本工具，附著在公司自有的媒體與促銷支出上，屬於強化；代理式購物若繞過品牌搜尋才算替代，2027 假期季是第一個可觀察點。","fact_refs":["f_peer_sn_gross_margin_pct","f_peer_sn_operating_margin_pct","f_peer_sn_fcf_margin_pct","f_peer_hele_gross_margin_pct","f_peer_hele_operating_margin_pct","f_peer_hele_fcf_margin_pct","f_peer_nwl_operating_margin_pct","f_peer_whr_operating_margin_pct","f_kpi8_net_sales_by_category_cl"],"verdict_values":{"moat":{"mechanism":"新品速度加內容驅動的需求生成，再加上 41 個子品類帶來的零售陳列優先權；不是轉換成本，也不是合約。","execution":9,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：連 14 季雙位數成長，美國 Q3 年增 20.8%，18–24 歲家庭滲透率兩年升五成。定價面穩定：公司今年選擇延後漲價，扣退款毛利率年減約 100 個基點，事實表沒有平均售價。沒有獨立市佔數字，SN 在最大客戶內的份額也查不到，所以不標擴大。","competitor_notes":[{"name":"WHR","strategy_note":"大家電為主，和 SN 產品重疊少，只能說明家電製造的基本利潤很薄，不能當定價力對照。"},{"name":"HELE","strategy_note":"最接近的上市多品牌小家電同業，毛利率接近 SN，營業利益率落後，差在費用效率；事實表沒有其成長數字。"},{"name":"NWL","strategy_note":"多品牌消費品，毛利率和現金流都弱於 SN，不是搶份額的主要對手。"},{"name":"Dyson","strategy_note":"10-K 點名的高價對手，吸塵器和美容都重疊；未上市，事實表沒有財務數字。"},{"name":"Dreame／Roborock","strategy_note":"機器人吸塵器的進攻者，資本量級事實表未涵蓋；目前證據來自瑞士單一零售商，不能直接外推到美國。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本，無法算 ROIC 差距；10-K 點名的直接對手多數未上市或不在同業表內。","threats":[{"level":"🟡","text":"對手降價搶份額，10-K 自陳可能被迫跟降。這是點對點競爭，目前沒有 SN 流失份額的證據。","p":"20%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"中國品牌已接管機器人吸塵器。若機器人替代直立和手持吸塵器，占 Q3 營收 31% 的清潔品類首當其衝。受損方式是客群範圍失守，尚未見到 SN 數字受傷。","p":"35%","evidence_refs":["substitute_technology#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，象限待補；外包製造、資本支出約營收 2.6%，傾向高周轉。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者通常是同一個家庭，轉換順暢，但小家電多屬可延後的想要。管理層 2026-08-05 說既有品類通常只長中高個位數，北美 Q1 也只有高個位數。"},{"item":"決策層級","level":"🟡","text":"每次購買都重新決定，沒有合約，也沒有換機成本；留客靠品牌信任和新品。淨水濾芯的定期訂購只是早期訊號，事實表沒有漲價後流失或回購率。"},{"item":"價值鏈分配","level":"🟡","text":"下游三家零售商占 45.7% 且集中度上升，上游代工分散。DTC 與社群電商在分回部分價值，但占比不揭露；Q3 給工廠約 4,500 萬美元也說明利潤不完全留在品牌端。"},{"item":"社會容忍度","level":"🟢","text":"非必需品，沒有社會對漲價的天花板，也不靠監管授權。180 萬台壓力鍋召回屬產品安全事件，未形成對定價的限制。"}],"roiic":75.6,"reinvest_rate":32.4,"endo_ceiling":24.5,"formula_note":"單位為百分比，皆為代理值。事實表沒有投入資本和折舊，用淨利減自由現金流當淨再投資。FY2023 至 FY2025 合計 3.886 億美元，對應營收增加 26.82 億，每 1 美元新營收投入 0.145 美元。FY2025 淨利率 10.96%，固定利潤率下增量報酬約 75.6%。FY2025 再投資率＝(7.014−4.744)÷7.014＝32.4%。內生上界＝75.6%×32.4%＝24.5%。股權薪酬沒有扣除，真實再投資率會更高，上界偏寬。"}}}},"q3_growth":{"verdict":"🟢 五年後仍有跑道，但寬度依賴公司自估的市場規模，可服務市場沒有更新。","reasoning":"成長主要靠銷量、新品類和新地區。價格不是驅動力，公司今年延後漲價；沒有併購，回購很小。共識 FY2026 到 FY2028 EPS 年化 15.3%。若用 FY2025 GAAP 4.94 起算是 21.0%，但起點和終點口徑不同，會高估。兩者都低於內生上界 24.5%，缺口為負。共識 FY2027 EPS 成長 16.4%、營收 14.1%，多出來的部分要靠費用率槓桿，CFO 2026-11-04 也說毛利率的逆風還在。以總市場 1,300 億和 18.5% 成長計，到 30% 滲透率約 9.6 年；若用三年前可服務市場 390 億，只剩約 2.5 年。分析師 2026-11-04 同時問了兩個數字，CEO 只更新總市場，這是跑道判斷最弱的一環。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_guidance_fy2026","f_kpi8_net_sales_by_category_cl"],"verdict_values":{"growth":{"driver_mix":"銷量、新品類、新地區為主；價格貢獻低，併購為零，回購只抵銷股權稀釋。","runway_years":"約 9.6 年（總市場 1,300 億美元、18.5% 成長）；用三年前可服務市場計只有約 2.5 年","runway_post_y5":"🟢","endo_ceiling_basis":"引用競爭優勢題的代理推導：增量報酬約 75.6%×再投資率 32.4%＝24.5%。Base 的 EPS 年化 13.5% 在上界內。","segments":[{"item":"清潔","value":"Q3 6.172 億美元，年增 4.1%，占 31%"},{"item":"烹飪飲品","value":"5.977 億美元，年增 36.6%，占 30%"},{"item":"食物料理","value":"4.855 億美元，年增 18.3%，占 25%"},{"item":"美容居家環境","value":"2.761 億美元，年增 45.8%，占 14%；Q2 年增 65.3%，增速放緩"},{"item":"美加","value":"13.137 億美元，年增 19.4%"},{"item":"國際","value":"6.627 億美元，年增 25.2%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"扣退款口徑：Q3 約年減 100 個基點，Q4 指引再年減約 100 個基點；報表口徑 Q3 反而升 560 個基點。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"沒有獨立份額數字，只能說未見縮減。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"今年延後漲價，尚未測試。"},{"signal":"EPS 年化高於營收年化超過 5 點","lit":false,"note":"前瞻約差 2.3 點，未亮；FY2022 到 FY2025 差 23.6 點，那段靠毛利率由 37.9% 升到 49.0%，不可重複。"},{"signal":"自由現金流對淨利低於 0.75 連 2 年","lit":true,"note":"FY2024 為 0.67，FY2025 為 0.68。"},{"signal":"股權薪酬占營收超過 5% 且上升","lit":false,"note":"Q3 為 2.1%。"},{"signal":"總市場萎縮或被替代","lit":false,"note":"公司自估總市場上升；機器人吸塵器的替代風險另列威脅。"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋。"},{"signal":"維持性資本支出占自由現金流超過 60%","lit":false,"note":"維持性支出未拆；總資本支出約 2 億美元，約為 TTM 自由現金流的四成。"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"不適用，營收仍在成長。"}],"trap_rating":"價值陷阱風險🟡（亮 2 個）；長期成長性🟡"}}},"q4_capital":{"verdict":"資本配置不差但樣本淺：沒有併購，股權稀釋低，回購報酬無法驗證，現金轉換率是弱項。","reasoning":"自由現金流對淨利 FY2024 為 0.67、FY2025 為 0.68，連兩年低於 0.75。今年前九個月營業現金流 1.074 億、資本支出 1.246 億，自由現金流 −0.172 億美元；現金流集中在第四季，但退款已收回多少現金，事實表沒有。Q3 股權薪酬 4,200 萬美元，占營收 2.1%。今年前三季現金用在回購 1.7 億和資本支出 1.246 億，沒有併購和配息；三年現金去向四分、債務到期結構、回購均價事實表未涵蓋。季末現金 4.88 億、公司口徑總債務 7.09 億；事實表 9.1266 億的總債務含租賃，淨負債 4.2484 億也是含租賃口徑。稀釋股數 FY2024 約 141.1、FY2025 約 142.0、FY2026 指引約 142.0 百萬股，回購大致抵掉稀釋。","fact_refs":["f_kpi4_free_cash_flow_fcf","f_kpi5_share_based_compensation","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 沒有併購項目，沒有可驗證的併購報酬。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"今年前三季回購 1.7 億美元；回購均價和 10 年期殖利率都不在事實表，無法判斷。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 股權薪酬 4,200 萬美元，年化約 1.68 億，約占市值 0.5%；稀釋股數 FY2025 較 FY2024 增 0.7%，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有新品與市場擴張，近 12 個月 8-K 沒有併購項目，成長不靠併購支撐。"}}}},"q5_valuation":{"verdict":"🔴 現價要求的成長和倍數同時接近我的樂觀情境，不信到那個程度。","reasoning":"想賺 12% 年化，五年後股價要 393 美元。若 2031 年值 22 倍，EPS 要 17.9，年化 21.7%；值 26 倍也要 15.1，年化 17.7%。我的 Base 是 13.5%，五年年化報酬約 4.5%。股價從前份 140.84 漲到 222.95，FY2026 指引中值只上修 10.7%，其餘是倍數由約 23.3 倍升到 33.3 倍。共識修正 0.0 不代表沒有上修，而是快照沒更新：FY1 的 6.59 低於上修後指引下緣 6.65，營收共識 76.41 億卻高於指引上緣約 76.15 億，兩組資料不同步。賣方均價 215.81（10 月底、單一聚合站、財報前）低於現價約 3%，最高最低只差 1.23 倍，不支持追價，但財報後大概會上調。短期目標用 FY2027 EPS 7.80×28 倍＝218，較現價 −2.0%；中期用 FY2028 EPS 9.00×25 倍＝225，較現價 +0.9%。動能方面，RSI 標記不可用，事實表也沒有四週漂移，過熱判斷留空；26 週漲 99.65%、股價高出 52 週均線 62% 是事實。250 週均線無值，週線六態無法判定。五年分位事實表未涵蓋，86.5 只是 4 個年度端點的分位。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_ma_w52","f_ma_state"],"verdict_values":{"valuation":{"basis":"FY2026 與 FY2027 前瞻本益比；trailing 本益比含退款，不採用。","tier":"消費品牌成長股；可得同業多為成熟公司，不能當直接錨點。","peers":[{"item":"De'Longhi","value":"約 13.5 倍（前份 2026-06-19 所記，不是本次現值），作成熟期下緣參考"},{"item":"HELE／NWL／WHR","value":"事實表只有利潤率，沒有倍數，資料缺口"}],"fwd_pe":33.83,"peg":2.21,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY2026 本益比 33.83 倍，PEG 2.21（33.83÷FY2026 到 FY2028 共識年化 15.3%）；P/S 和 EV/S 在可得年度端點最高，P/E 分位 86.5。Base 五年年化約 4.5%，低於 8%。若改用混合口徑 21.0%，PEG 為 1.61，但 Base 報酬和分位仍指向貴。","upside_short_pct":-2.0,"upside_mid_pct":0.9,"denominator_disputed":false,"denominator_note":"過去 12 個月 EPS 含約 1.99 億美元淨退款，稅後約每股 1.08 美元，37.41 倍的 trailing 本益比不可用。FY2026 指引只含約 0.17 美元淨效果，FY2027 共識應不含退款。結論用前瞻分母，一次性效應不影響貴的判斷。"}}},"q6_how_wrong":{"verdict":"🟡 最可能看錯的地方是把退款季當常態，以及把進貨當需求；陷阱風險中等。","reasoning":"敏感度：毛利率每差 100 個基點，FY2031 EPS 約差 0.70 美元、目標價約差 15 美元；終端倍數每差 1 倍，目標價差 12.6 美元；五年營收年化少 1 個百分點，EPS 約少 0.6 美元、目標價約少 13 美元。單項看差距不大，但雙位數成長一斷，倍數會一次掉好幾倍，所以唯一致命點選它。成長熄火的倍數錨：三年後成長率降到 15%／10%／5%，我給約 24／18／14 倍。管理層沒正面回答的題目有四個：DTC 與批發毛利差距、美國 DTC 規模、美國陳列相對去年的變化（2026-08-05），以及可服務市場的更新（2026-11-04）。事實表沒有歷史最大回撤、訴訟金額，內控缺陷只有二手來源，未核對 10-K 原文。","fact_refs":["f_week26_return_pct","f_ma_w52","f_ma_w104","f_kpi4_free_cash_flow_fcf"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：生意真實，現金轉換和扣退款毛利率待驗證。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":6.7,"pe":33.28,"basis":"FY2026 全年調整後 EPS，用 2026-11-04 上修後指引中值 6.70；共識 6.59 是財報前快照。起點與終端都用當年度 EPS 口徑。"},"valuation_basis":"eps_pe","eps":{"bull":[8.3,10.0,12.0,14.4,17.2],"base":[7.8,9.0,10.2,11.4,12.6],"bear":[6.9,6.8,6.9,7.1,7.4]},"pe":{"bull":26,"base":22,"bear":14},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.0,"net_buyback":0.2},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-40,"basis":"事實表沒有歷史最大回撤，用現價推：回到 52 週均線 137.88 是 −38%，回到 104 週均線 118.70 是 −47%，Bear 終值約 103.6 是 −54%。26 週翻倍後一次雙位數斷線會同時打到盈餘和倍數，下緣再留約 6 個百分點給超跌。","trigger_time":null},"basis":{"bull":"營收五年年化約 15%，國際占比過四成，淨利率升到約 15.5%，股數約 1.38 億；2031 年市場仍給 26 倍。","base":"營收五年年化約 10.5%，FY2027 略高於財報前共識，淨利率由 12.5% 升到約 14%；倍數收斂到 22 倍，落在前份假設區間的上緣。","bear":"爆品退潮加關稅回升，營收年化 3%–5%，扣退款毛利率掉到 46%–47%，EPS 五年只到 7.40；14 倍接近 De'Longhi 約 13.5 倍（前份 2026-06-19 所記，不是本次現值）。機率 25% 取五年常態區間下緣：連 14 季雙位數和 41 個子品類分散壓低失敗機率，但硬體爆品公司沒有合約收入，不壓到 20%。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 增量 3.46 億美元有 71% 來自烹飪飲品和美容居家環境，清潔連兩季只長 4.1%；美容居家環境增速由 Q2 的 65.3% 降到 45.8%。管理層說基礎業務貢獻最大，但沒有給定義和數字。","assumption":"新品接棒的速度能長期快過舊爆品退潮，而且 41 個子品類足以分散單一爆品風險。","consequence":"五年虧 50% 最可能的故事：烹飪和美容的爆品週期結束，清潔被機器人吸塵器侵蝕，營收掉回低個位數，倍數由 33 倍回到 14 倍。此故事與唯一致命點同一條路徑。","ruling":"部分採納。分散度是真的，但基礎業務的說法未經驗證，Bear 機率保留 25%。","watch":"每季品類拆分，清潔是否轉負；烹飪飲品增速是否跌破 15%。","evidence_refs":["supply_demand_durability#0","substitute_technology#0"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 銷售行銷年增 25.3%、研發 24.4%、管理費用 43.3%，都快過營收 21.2%，調整後營業費用率升 180 個基點，打斷先前連五季的槓桿。FCF 對淨利兩年約 0.67。媒體和促銷已超過 15 億美元。","assumption":"成長能維持，但取得成長的成本不再下降，再投資變成常態。","consequence":"若約 1 億美元再投資在 FY2027 延續而退款消失，EPS 約少 0.57 美元，占 FY2027 共識 7.4%。營收達標但每股現金沒有跟上。","ruling":"未證，監測。CFO 說再投資都在 Q4 結束，但媒體投放和 AI 人力本質上容易延續；FY2027 上半年費用率不降，一次性的說法就不成立。","watch":"FY2027 Q1、Q2 調整後營業費用率年變化；全年自由現金流對淨利。","evidence_refs":["reg_tariff_export#3"]},{"view":"價格已反映太多","evidence":"26 週漲 99.65%；股價高出 52 週均線 62%；FY2026 本益比 33.83 倍；P/S、EV/S 在可得端點最高；倍數由約 23.3 倍升到 33.3 倍。","assumption":"市場願意持續為雙位數成長付接近 30 倍的 FY2027 盈餘。","consequence":"Base 五年年化約 4.5%，Bull 14.9%，Bear −14.2%，正負不對稱僅約 1.9。","ruling":"採納。這是不追的唯一卡點，生意本身沒有破。","watch":"股價對 FY2027 共識的倍數；170 美元和 268 美元兩條線。","evidence_refs":[]},{"view":"論點失敗","evidence":"二手報導稱 FY2025 財報內控有重大缺陷、審計師出具否定意見；未見重編報導，也未核對 10-K 原文。董事長 2026-07-10 獲一次性豁免出售部分持股。","assumption":"報表可靠，控股股東與小股東利益一致。","consequence":"若內控缺陷未改善或延伸到退款認列，33 倍的盈餘品質會被重新質疑；Q3 退款金額大、口徑複雜，正是內控要過關的項目。","ruling":"不採信也不否定。證據等級低，但影響大，列為必查項，並先按主動賣出看待，留存比例事實表未涵蓋。","watch":"下一份 10-K 的內控段落；是否再有豁免或由 CEO、CFO 在更低價賣出。","evidence_refs":["major_events#4","sec_investigation_restatement#0","major_events#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 140.84 → 本次 222.95（+58.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=140.84","side_b":"本次 price_at_dd=222.95","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 140.84 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 140.84 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 140.84 美元：Bull 價 447.2、Bear 價 103.6，五年期望值 +96.2%，基準年化 14.5%，不對稱比 8.23","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 8.23。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 140.84 美元：五年期望值 +96.2%，基準年化 14.5%，不對稱比 8.23","side_b":"本次情境、股價 222.95 美元：五年期望值 +23.9%，基準年化 4.5%，不對稱比 1.88","ruling":"再換股價、情境不動：起點價上漲 58.3%，五年期望值少 72.3 個百分點，基準年化少 10.1 個百分點，不對稱比由 8.23 降到 1.88。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與評級（價格）","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-06-19 股價 140.84 美元，評級 B，估值中性；未記錄裁決角色、機率與最大回撤。","side_b":"現價 222.95 美元，漲 58%，評級仍 B，估值轉貴；機率 25／50／25，最大回撤 −40% 到 −60%。","ruling":"股價漲 58%，FY2026 EPS 指引中值只上修 10.7%，其餘來自倍數。生意比前份好，估值轉貴的原因是價格。可調和。","evidence_level":"高","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價回到 170 美元以下且合併單季年增仍在 10% 以上，則分批買進。","若股價續漲而 2027 上半年費用率還沒驗證，則不追。"],"evidence_refs":[]},{"axis":"陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份為中度，摘要未保存依據。","side_b":"本次仍為中度，亮的是自由現金流對淨利連兩年低於 0.75，以及扣退款毛利率年減。","ruling":"結論不變，依據換成本次財報數字。若亮燈增加到 3 個，改為高風險。","evidence_level":"中","settle_metric":"FY2026 全年自由現金流對淨利","if_then":["若 FY2026 比率仍低於 0.75，則連三年成立，停止加碼。","若回到 0.85 以上，則移除此亮燈。"],"evidence_refs":[]},{"axis":"舊格式空白欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份這四欄都空白。","side_b":"本次：競爭優勢穩定，五年後跑道寬，公司類型為品質複利成長，循環位置不適用。","ruling":"這些是首次填寫，不是判斷改變。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設進場重啟條件（空白）。","side_b":"股價回到 170 美元以下，約 22 倍 FY2027 共識 EPS，且合併單季年增仍在 10% 以上才進場。","ruling":"估值是唯一卡點，所以用價格錨，成長條件只是檢查論點仍有效。觸發後重跑研究再分批進場。","evidence_level":"中","settle_metric":"股價與單季年增","if_then":["若價格到位但成長跌破 10%，則不進場，改按論點受損處理。"],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（空白）。","side_b":"合併單季年增低於 10% 減碼一半；連 2 季低於 10% 且 FY2027 共識下修超過 10% 清倉。","ruling":"改用可每季驗證的數字，動作寫死，避免事後解釋。","evidence_level":"中","settle_metric":"合併單季年增與 FY2027 共識","if_then":["若第一次跌破 10%，則減碼一半。","若連 2 季跌破且共識下修超過 10%，則清倉。"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）。","side_b":"合併淨銷售單季年增首度跌破 10%，結束連 14 季雙位數。","ruling":"現價倍數最敏感，而倍數取決於雙位數成長是否斷線，所以選這個數字。","evidence_level":"中","settle_metric":"合併單季年增","if_then":["若發生，則減碼一半。"],"evidence_refs":[]},{"axis":"營收減碼線","cause":"新證據","prior_field":["H1","R1"],"side_a":"整體連 2 季低於 +8%。","side_b":"整體連 2 季低於 +10% 為削弱並減碼；連 3 季低於 +8% 為反轉，舊線保留。","ruling":"現價倍數由約 23 倍升到 33 倍，容錯變小，所以提高減碼線，舊 8% 不刪。","evidence_level":"中","settle_metric":"合併單季年增","if_then":["若連 3 季低於 8%，則清倉。"],"evidence_refs":[]},{"axis":"毛利率與關稅減碼線","cause":"新證據","prior_field":["H2","R2"],"side_a":"連 4 季調整後毛利率低於 47%；東南亞稅率 ≥20%。","side_b":"連 4 季扣退款毛利率低於 48%；東南亞基準關稅 ≥20% 不變。","ruling":"Q3 扣退款約 49.1%，舊線離現況 2 點，等於太晚才減碼，所以提高 1 點。Q4 指引還會年減約 100 個基點，48% 不會輕易被碰到。","evidence_level":"中","settle_metric":"扣退款毛利率","if_then":["若連 4 季低於 48%，則減碼。"],"evidence_refs":[]},{"axis":"倍數假設降位","cause":"方法變動","prior_field":["H3"],"side_a":"FY2027 前瞻本益比 ≥16 倍，低於 16 倍為反轉；區間 18–24 倍。","side_b":"倍數不再當投資論點，16 倍保留在清倉指標；現值 29.07 倍，已高於舊區間上緣。","ruling":"倍數是結果，不是企業論點。H3 改為國際與直營投入能否回收，舊門檻保留。","evidence_level":"中","settle_metric":"FY2027 前瞻本益比","if_then":["若倍數低於 16 倍且成長未破，則重跑研究並考慮分批買進。"],"evidence_refs":[]},{"axis":"Q3 亮眼數字與扣退款數字","cause":"新證據","prior_field":null,"side_a":"管理層 2026-11-04：Q3 調整後 EBITDA 年增約 46%，調整後 EPS 2.34，年增 56%。","side_b":"全額扣掉 1.34 億退款，調整後營業利益 2.915 億，較去年 2.89 億增不到 1%；這是下限，因同季有再投資。下半年合計 EBITDA +25%，扣約 3,000 萬淨退款約 +21%，快過營收 +19%。","ruling":"可調和。Q3 單季不能用，要看下半年合計；基本盤仍跑贏營收，幅度約 2 個百分點，不是 25 個百分點。","evidence_level":"高","settle_metric":"FY2027 調整後 EBITDA 增速減營收增速","if_then":["若 FY2027 上半年 EBITDA 增速低於營收，則停止加碼。"],"evidence_refs":["reg_tariff_export#3"]},{"axis":"再投資是否一次性","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：再投資全部在 Q4 結束；2027 靠營業費用槓桿跑贏營收。CEO 2026-08-05：2027 人力大致持平。","side_b":"CEO 同場說還有更多地方要播種；Q3 管理費用年增 43.3%，原因含人員與 AI 投資；連五季費用槓桿在 Q3 中斷；毛利率逆風 CFO 也說還在。","ruling":"未證、監測，不採信也不否定。預先寫好證偽條件：FY2027 Q1、Q2 調整後營業費用率連 2 季沒有年減，一次性的說法就不成立。","evidence_level":"中","settle_metric":"FY2027 Q1、Q2 調整後營業費用率年變化","if_then":["若連 2 季沒有年減，則停止加碼並把 FY2027 EPS 下調約 0.57 美元重算。","若兩季都年減且毛利率不低於 48%，則解除此疑慮。"],"evidence_refs":[]},{"axis":"美國成長是需求還是進貨","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：美加很穩固地是雙位數成長者，趨勢延續到 2027。美國主要零售商網站今年累計 POS 增逾 30%。","side_b":"CEO 2026-08-05 說要推動零售商庫存在 Q4 前增加；CFO 2026-11-04 說假期進貨發生在 Q3。全年指引暗示 Q4 合併約 +17%，若國際加速，美加粗估降到約 12%。POS 只講網站，Q3 沒有更新零售商庫存。","ruling":"不可裁決至 2027 年 2 月 Q4 財報。Q1 FY2026 北美只有高個位數，證明雙位數不是保證。","evidence_level":"中","settle_metric":"Q4 美加年增與零售商庫存說法","if_then":["若 Q4 美加年增低於 10%，則視為進貨提前，停止加碼。","若 Q4 美加年增高於 14% 且庫存健康，則解除疑慮。"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"基礎業務說法與品類數字","cause":"新證據","prior_field":null,"side_a":"CEO 2026-11-04：基礎業務對淨銷售貢獻最大。","side_b":"品類拆分顯示清潔只貢獻 7% 增量，烹飪飲品加美容居家環境占 71%；基礎業務沒有定義，Luxe Café、Crispi 這類近年產品算哪邊也沒說。","ruling":"可調和但未驗證。公司可能把上市滿一定時間的產品算基礎，定義不公開就不當作爆品風險下降的證據。","evidence_level":"中","settle_metric":"公司是否揭露基礎業務定義與金額；清潔年增","if_then":["若清潔連 2 季年減，則停止加碼。"],"evidence_refs":[]},{"axis":"共識資料是否可用","cause":"新證據","prior_field":null,"side_a":"事實表顯示 FY1、FY2、FY3 共識修正都是 0.0。","side_b":"公司兩度上修指引，EPS 由 6.00–6.10 升到 6.65–6.75；FY1 共識 6.59 低於指引下緣。","ruling":"資料未更新，不當作市場沒有上修。上修動能這項本次沒有可用讀數，Base 的 FY2027 略高於共識也因此。","evidence_level":"高","settle_metric":"財報後第一份共識快照","if_then":["若更新後 FY2027 共識高於 8.2，則重算 Base。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"18 年營收年化 21%、連 14 季雙位數、總市場滲透不到 6%、美國和英國這兩個最成熟市場還在加速；共識偏舊。好公司的倍數常常比想像中撐得久。","side_b":"要 12% 年化得五年 EPS 年增約 18% 且 2031 年仍有 26 倍；Base 只有 4.5%，股價已高於財報前賣方均價。","ruling":"不追。論證講的是公司好，沒有回答價格。若倍數能長期撐住，代價是少賺一段，比買在 33 倍後遇到斷線便宜。","evidence_level":"中","settle_metric":"Base 五年年化報酬","if_then":["若 FY2027 上半年成長和費用率都超預期，把 Base EPS 上調後重算，年化高於 10% 就可分批買進。","若股價續漲但數字沒有更新，則不追。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：中國品牌接管機器人吸塵器，10-K 自陳對手可能降價。其他結構：關稅 10%–12.5%，大部分產品在中國、越南等地製造，他國也可能報復。","side_b":"結構轉好：IEEPA 部分關稅遭最高法院推翻並退款；社群電商與直營打開新通路；供應鏈已多元。","ruling":"雙向拉鋸。依據是 10-K、Q3 新聞稿和 Digitec 零售資料；通路改善較確定，競爭惡化目前集中在機器人品類。","evidence_level":"中","settle_metric":"清潔品類年增與扣退款毛利率","if_then":["若清潔轉負且毛利率低於 48%，則改判競爭惡化中並減碼。"],"evidence_refs":["competitive_share_entrants#2","substitute_technology#1","reg_tariff_export#0","geo_supply_chain#2"]}],"triggers":[{"n":1,"text":"合併淨銷售單季年增首度跌破 10%。","type":"Single Thing","maps_to":"H1","metric":"合併淨銷售年增","threshold":"<10%","action":"減碼一半","source_freq":"季度新聞稿","date":null,"evidence_refs":["supply_demand_durability#0"]},{"n":2,"text":"成長連 2 季失守且共識明顯下修。","type":"清倉","maps_to":"H1／R1","metric":"合併年增與 FY2027 共識 EPS","threshold":"連 2 季 <10% 且共識下修 >10%；或連 3 季 <8%","action":"清倉","source_freq":"季度新聞稿、共識快照","date":null,"evidence_refs":[]},{"n":3,"text":"再投資是否真的一次性。","type":"假設驗證","maps_to":"H2／R3","metric":"調整後營業費用率年變化","threshold":"FY2027 Q1、Q2 連 2 季沒有年減","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-08","evidence_refs":[]},{"n":4,"text":"關稅或成本吸收失敗。","type":"風險","maps_to":"R2","metric":"扣退款毛利率；東南亞基準關稅","threshold":"連 4 季 <48%；或基準關稅 ≥20%","action":"減碼","source_freq":"季度法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"n":5,"text":"Q4 美加成長驗證 Q3 是需求還是進貨。","type":"假設驗證","maps_to":"R1","metric":"Q4 美加淨銷售年增","threshold":"<10%","action":"停止加碼","source_freq":"Q4 財報","date":"2027-02","evidence_refs":[]},{"n":6,"text":"存貨成長跑贏營收。","type":"風險","maps_to":"R1","metric":"存貨年增減營收年增","threshold":"連 2 季 >5 個百分點（Q3 為 2.1 點）","action":"停止加碼","source_freq":"季度新聞稿","date":null,"evidence_refs":[]},{"n":7,"text":"零售商集中度繼續上升。","type":"風險","maps_to":"R4","metric":"最大客戶占比；三大客戶合計","threshold":"最大客戶 ≥27%；或三大合計 ≥50%","action":"停止加碼","source_freq":"年度 10-K","date":"2027-03","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":8,"text":"核對內控缺陷的原文與改善進度。","type":"假設驗證","maps_to":"R5","metric":"10-K 內控段落","threshold":"重大缺陷未改善，或審計師仍出具否定意見","action":"停止加碼","source_freq":"年度 10-K","date":"2027-03","evidence_refs":["major_events#4","sec_investigation_restatement#0"]},{"n":9,"text":"內部人賣股升級。","type":"風險","maps_to":"R5","metric":"董事長再獲豁免；CEO、CFO 賣股","threshold":"12 個月內再次豁免；或 CEO、CFO 在低於 2026-07 的價格主動賣出","action":"減碼","source_freq":"8-K、Form 4","date":null,"evidence_refs":["major_events#1"]},{"n":10,"text":"再出現大規模產品召回。","type":"風險","maps_to":"R6","metric":"CPSC 召回台數","threshold":"單次 ≥100 萬台","action":"停止加碼","source_freq":"CPSC 公告","date":null,"evidence_refs":["major_events#3","product_recall_warning#0"]},{"n":11,"text":"清潔品類轉負。","type":"風險","maps_to":"R7","metric":"清潔品類年增","threshold":"連 2 季 <0%","action":"停止加碼","source_freq":"季度新聞稿","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#2"]},{"n":12,"text":"估值回到可重新評估的位置。","type":"估值rearm","maps_to":"H1","metric":"股價；合併單季年增","threshold":"股價 ≤170 美元且年增 ≥10%","action":"重跑研究後分批買進","source_freq":"每日股價、季度新聞稿","date":null,"evidence_refs":[]},{"n":13,"text":"下跌但基本面沒壞。","type":"加碼","maps_to":"H1／H2","metric":"股價；H1、H2 門檻","threshold":"股價 ≤150 美元（Base 年化約 13%）且 H1、H2 未破","action":"分批反買","source_freq":"每日股價、季度新聞稿","date":null,"evidence_refs":[]},{"n":14,"text":"股價再漲但盈餘沒跟上。","type":"減碼","maps_to":"H1","metric":"股價對 FY2027 共識","threshold":"股價 ≥268 美元（約 35 倍）且共識未同步上修","action":"減碼","source_freq":"每日股價、共識快照","date":null,"evidence_refs":[]},{"n":15,"text":"Q4 財報與 FY2027 指引後複審。","type":"複審日期","maps_to":"H1／H2／H3","metric":"全部門檻","threshold":"財報公布後一週內","action":"重跑研究","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"合併淨銷售單季年增","bear_threshold":"<10% 減碼一半；連 2 季 <10% 且共識下修 >10% 清倉","window":"單季／連 2 季","source":"季度新聞稿","last_status":"ok"},{"metric":"扣退款毛利率","bear_threshold":"連 4 季 <48%","window":"連 4 季","source":"季度法說與新聞稿","last_status":"ok"},{"metric":"調整後營業費用率年變化","bear_threshold":"FY2027 Q1、Q2 連 2 季沒有年減","window":"2027 上半年","source":"季度新聞稿","last_status":"warning"},{"metric":"自由現金流對淨利","bear_threshold":"連 3 年 <0.75","window":"FY2024 至 FY2026","source":"年度財報","last_status":"warning"},{"metric":"FY2027 前瞻本益比","bear_threshold":"<16 倍（前份保留）","window":"持續","source":"Koyfin 共識與收盤價","last_status":"ok"},{"metric":"東南亞基準關稅","bear_threshold":"≥20%（前份保留）","window":"持續","source":"公司指引假設","last_status":"ok"},{"metric":"新爆品數與平均售價","bear_threshold":"連續 ≥2 年爆品數下滑且平均售價下行（前份保留，資料缺口）","window":"2 年以上","source":"法說；事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[{"ref":"customer_second_source#0","reason":"閘沒有讀錯，這條確實沒被引用。本輪修補包只有閘的清單和判斷全文，沒有這條證據的內文，硬引用等於替沒讀到的內容背書，所以不寫進競爭威脅。客戶端議價風險已由通路集中風險項和零售商集中度觸發條件追蹤，門檻是最大客戶 ≥27% 或三大客戶合計 ≥50%。這條留待下次重跑研究時讀原文再歸類。"},{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"閘的複核已認定沒有矛盾，並建議降為 🟢，此欄維持否。本判斷確實沒有主張市場看錯，估值結論是現價要求的成長和倍數接近樂觀情境。閘提到 Base 五年年化 4.5%、1.9 的不對稱要靠 Bull 25% 支撐，這正是宣告等價格的原因：現價不進場，要等股價回到 170 美元以下且合併單季年增仍在 10% 以上，最終裁決是觀望。"},{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"閘列的兩點都不需要改欄位。股權薪酬未扣、上界偏寬，原算式說明已寫明；24.5% 只用來檢查共識和 Base 的 EPS 年化有沒有超過上界，沒有當精確估計。本判斷引用的股權薪酬只有 Q3 一季，沒有三年合計，補不出更準的數字。Bear 的五年後淨負債和股數此包未見，是因為情境採 EPS 乘本益比估值，Bear 終值是 7.40×14 倍，這兩項不是這個估值法的輸入。"},{"ref":"$.counter_evidence.contradictions","reason":"閘已確認這段站得住，不改。估值由 🟡 轉 🔴 歸為價格變動，依據已寫在裁定裡：股價漲 58%，FY2026 EPS 指引中值只上修 10.7%，倍數由約 23.3 倍升到 33.3 倍。指引上修會讓同一股價下的估值變便宜，不能解釋估值轉貴，所以歸因維持價格變動。前份其餘欄位空白，沒有可歸因的變動。"}],"action_conditions":{"rearm_trigger":"股價回到 170 美元以下（約 22 倍 FY2027 共識 EPS，Base 年化約 10%），且合併單季年增仍在 10% 以上。","exec_line":"現價不追。未持有者等 170 美元以下再分批；已持有者續抱不加碼，波動不是賣出理由，超過 268 美元且共識沒跟上才減碼。續漲但 2027 上半年費用率未驗證，一律不追；下跌但合併成長仍在 10% 以上，分批反買。","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 170 美元以下，約 22 倍 FY2027 共識 EPS，且合併單季年增仍在 10% 以上。","qc48_result":"pass","qc48_note":"Bull 的 EPS 路徑算得出來，但關鍵假設和成長跑道的來源都還沒有被證實，歷史上硬體爆品高估值之後的報酬也明顯低於 Bull 隱含的 14.9% 年化，這條 Bull 依據只能算勉強站得住。"},"thesis":{"H":[{"id":"H1","text":"新品和既有品類一起撐住合併雙位數成長。","2y":"FY2027 淨銷售年增 ≥14%，FY2028 ≥10%。","5y":"FY2031 營收約 125 億美元以上，非清潔品類占比高於 Q3 的 69%。","10y":null,"threshold":"合併淨銷售單季年增 ≥10%。","source":"季度新聞稿品類拆分與法說。","drift_rule":"連 2 季低於 10% 削弱，連 3 季低於 8% 反轉。"},{"id":"H2","text":"關稅退款用完之後，FY2027 調整後 EBITDA 仍跑贏營收，而且靠的是營業費用率下降。","2y":"FY2027 調整後 EBITDA 增速高於淨銷售增速，上半年費用率逐季年減。","5y":"FY2031 調整後 EBITDA 利潤率 ≥20%（FY2026 指引約 18.3%）。","10y":null,"threshold":"扣退款毛利率 ≥48%；FY2027 調整後 EBITDA 增速高於淨銷售增速。","source":"季度新聞稿與 CFO 法說口徑。","drift_rule":"FY2027 連 2 季費用率沒有年減為削弱；連 4 季扣退款毛利率低於 48% 為反轉。"},{"id":"H3","text":"歐洲和拉美轉直營、社群電商的投入能回收，國際成為第二條成長曲線。","2y":"FY2027 國際年增 ≥20%；Q4 FY2026 國際增速高於 Q3 的 25.2%（CEO 2026-11-04 的說法）。","5y":"國際占營收 ≥42%（Q3 為 33.5%）。","10y":null,"threshold":"國際單季年增 ≥15%。","source":"季度新聞稿地區拆分與法說。","drift_rule":"連 4 季低於 15% 削弱，連 6 季低於 10% 反轉。"}],"R":[{"id":"R1","text":"爆品退潮或假期進貨提前，合併增速跌破雙位數；家電需求本身也沒有回升的順風。","h_ref":"H1","clock":"⚡","threshold":"合併連 2 季低於 10%；連 3 季低於 8%（舊線保留）。","evidence_refs":["supply_demand_durability#0"]},{"id":"R2","text":"關稅回升或成本壓力吸收不掉。公司已提示關稅造成重大不利影響，且製造集中在中國、越南等地。","h_ref":"H2","clock":"🔥","threshold":"扣退款毛利率連 4 季低於 48%，或東南亞基準關稅 ≥20%。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R3","text":"再投資不是一次性，退款消失後費用還在。若約 1 億美元延續，FY2027 EPS 約少 0.57 美元。","h_ref":"H2","clock":"⚡","threshold":"FY2027 Q1、Q2 調整後營業費用率連 2 季沒有年減。","evidence_refs":[]},{"id":"R4","text":"通路集中度上升，大零售商壓縮條件或調整陳列。","h_ref":"H1","clock":"🔥","threshold":"最大客戶 ≥27%，或三大客戶合計 ≥50%。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"報表可靠性與控股股東賣股。內控缺陷目前只有二手來源，未核對 10-K。","h_ref":"H2","clock":"🔥","threshold":"下一份 10-K 重大缺陷未改善；或 12 個月內再次豁免賣股。","evidence_refs":["major_events#4","sec_investigation_restatement#0","major_events#1"]},{"id":"R6","text":"產品安全。壓力鍋召回 180 萬台、106 起燙傷，N.D. Cal. 案已獲早期駁回，其他消費者案金額事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"單次新召回 ≥100 萬台，或集體訴訟獲認證且和解金額重大。","evidence_refs":["major_events#3","product_recall_warning#0"]},{"id":"R7","text":"對手降價、機器人吸塵器替代、新品命中率下滑，定價力結構性走弱。","h_ref":"H1","clock":"🐢","threshold":"連續 ≥2 年爆品數下滑且平均售價下行（前份保留，資料缺口）；清潔品類連 2 季年減。","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"]}],"single_thing":{"description":"合併淨銷售單季年增首度跌破 10%，結束連 14 季雙位數。","why_fatal":"現價約 29 倍 FY2027 EPS，買的是雙位數成長不會斷。終端倍數每差 1 倍影響 12.6 美元，毛利率 100 個基點影響約 15 美元，但斷線會讓倍數一次掉好幾倍，是最大的單一敏感項。","if_happens":"EPS 下修約 10%，倍數掉到約 20 倍，股價約 138 美元，較現價跌 38%。先減碼一半，連 2 季且共識下修超過 10% 才清倉。","how_monitor":"每季新聞稿的淨銷售年增，同時看美加年增和零售商庫存說法。FY2027 Q2、Q3 要面對超過 20% 的基期。","probability":"35%（未來 8 季，判斷值：FY2027 共識年增 14.1%，但基期變高，Q4 FY2026 指引已降到約 17%）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":29.07,"peg_fy2":1.9,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":4.94,"FY2026E":6.59,"FY2027E":7.67,"FY2028E":8.76},"fy_end_month":12,"eps_basis":"FY2025A 用 GAAP 稀釋 EPS 4.94，事實表沒有 FY2025 調整後數字；FY2026E 至 FY2028E 是 Koyfin 共識調整後口徑，且為財報前快照。起點與預估口徑不同，三年年化 21.0% 偏高，判斷時改用 FY2026 到 FY2028 的 15.3%。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"2026 假期檔：首次有單一官網、14 國 TikTok Shop、西班牙和義大利直營。","impact":"高","watch":"美加成長、社群電商基期、零售商庫存。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 FY2027 指引，日期公司尚未公告。","impact":"高","watch":"FY2027 EBITDA 增速指引、費用率、毛利率逆風。"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"FY2026 10-K。","impact":"中","watch":"內控段落、最大客戶占比。"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY2027 Q1 財報，第一次驗證再投資是否結束。","impact":"高","watch":"調整後營業費用率年變化、扣退款毛利率。"}],"decision_out":{"role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=99.65, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 的 EPS 路徑算得出來，但關鍵假設和成長跑道的來源都還沒有被證實，歷史上硬體爆品高估值之後的報酬也明顯低於 Bull 隱含的 14.9% 年化，這條 Bull 依據只能算勉強站得住。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 170 美元以下，約 22 倍 FY2027 共識 EPS，且合併單季年增仍在 10% 以上。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
