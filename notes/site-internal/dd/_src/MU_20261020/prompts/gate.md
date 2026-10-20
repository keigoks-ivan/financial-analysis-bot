你是 DD 管線 v20 的判斷層閘（gate），標的 MU（20261020）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_gaap`（q1_business）｜GAAP 營收＝41456 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.micron.com Reports Record Results for the Third Quarter of Fiscal 2026；交叉核對 SEC 8-K exhibit https://www.sec.gov/Archives/edgar/data/723125/000072312526000013/a2026q3ex991-pressrelease.htm 與 10-Q https://www.sec.gov/Archives/edgar/data/723125/000072312526000015/mu-20260528.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-05-28，公告於 2026-06-24））
  - 註記：analyst consensus 約 $35.69 billion（來源：news aggregator 彙整之市場預期，非公司揭露，beat 約 16.17%）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝81.2 %（Non-GAAP operating income $33,681 百萬 ÷ 營收 $41,456 百萬）｜期間與口徑：Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.micron.com Q3 FY26 press release（同上 SEC 連結）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-05-28，公告於 2026-06-24））
  - 註記：查無公開 Non-GAAP 營業利益率 consensus 數字，未填造
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝80.4 %（GAAP operating income $33,318 百萬 ÷ 營收 $41,456 百萬）｜期間與口徑：Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.micron.com Q3 FY26 press release；同數字見 SEC 10-Q 損益表（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-05-28，公告於 2026-06-24））
  - 註記：查無公開 GAAP 營業利益率 consensus 數字，未填造
- `f_kpi5_q4_fy2026_guidance`（q1_business）｜管理層 Q4 FY2026 財測（guidance）＝營收 $50.0B ± $1.0B；毛利率約 86%；Non-GAAP EPS $31.00 ± $1.00 區間｜期間與口徑：Q4 FY2026 展望（公告於 Q3 FY2026 法說會 2026-06-24，Q4 尚未公告實際結果——本站 earnings_recency 顯示最近一次財報仍是 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investors.micron.com Q3 FY26 press release，Business Outlook 表格（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026 展望（公告於 Q3 FY2026 法說會 2026-06-24，Q4 尚未公告實際結果——本站 earnings_recency 顯示最近一次財報仍是 2026-06-24））
  - 註記：查無公告當時 Q4 consensus 對照數字，未填造
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-09-30 date｜期間與口徑：2026-09-30／距今 14 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-09-30）
- `f_peer_mu_gross_margin_pct`（q2_moat）｜MU 毛利率＝72.57 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.gross_margin_pct，as_of TTM ending 2026-05-31（4季加總））
- `f_peer_mu_operating_margin_pct`（q2_moat）｜MU 營業利益率＝65.67 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
- `f_peer_mu_fcf_margin_pct`（q2_moat）｜MU FCF 利潤率＝28.99 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.fcf_margin_pct，as_of TTM ending 2026-05-31（4季加總））
- `f_peer_nvda_gross_margin_pct`（q2_moat）｜NVDA 毛利率＝74.67 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_tsm_gross_margin_pct`（q2_moat）｜TSM 毛利率＝64.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_avgo_gross_margin_pct`（q2_moat）｜AVGO 毛利率＝68.77 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amd_gross_margin_pct`（q2_moat）｜AMD 毛利率＝53.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝176.55 USD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-17）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝204.47 USD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-17）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝203.33 USD/share｜期間與口徑：2026-10-17／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-17）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.23 %｜期間與口徑：2026-10-17／兩份 Koyfin 快照之間的 EPS 修正幅度（176.15 → 176.55）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-17）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.9 %｜期間與口徑：2026-10-17／兩份 Koyfin 快照之間的 EPS 修正幅度（206.33 → 204.47）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-17）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝140.63 %｜期間與口徑：2026-07-16 → 2026-10-17／FY1 共識 EPS 73.37 → 176.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261017.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-17）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝275504.76 USD m｜期間與口徑：2026-10-20／yfinance revenue_estimate 0y 平均（41 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝318881.82 USD m｜期間與口徑：2026-10-20／yfinance revenue_estimate +1y 平均（43 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝12.17 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／3 個年度端點內的分位＝4.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-19（RTH 收盤，UTC））
- `f_kpi3_adjusted_fcf`（q4_capital）｜調整後自由現金流（Adjusted FCF）＝18304 百萬美元（Operating cash flow $25,388 - net capex $7,084）｜期間與口徑：Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.micron.com Q3 FY26 press release（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-05-28，公告於 2026-06-24））
  - 註記：查無公開 FCF consensus 數字，未填造
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC（股票薪酬）占 GAAP 營業利益／占營收 %＝341 百萬美元（占 GAAP 營業利益 1.02%；占營收 0.82%）｜期間與口徑：Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.micron.com Q3 FY26 press release，Non-GAAP 調節表 Stock-based compensation 341（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-05-28，公告於 2026-06-24））
  - 註記：不適用（SBC 無 consensus 概念）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-38255.0 USD m｜期間與口徑：2026-10-20／yfinance 最新一季：總債務 5179.0、現金 43434.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.062 %｜期間與口徑：2026-10-20／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-20）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1131.42 m shares｜期間與口徑：2026-10-20／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝904.9 USD｜期間與口徑：2026-10-19（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-19（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝4.98 x｜期間與口徑：2026-10-17／分母＝FY1 EPS 176.55，分子＝快照價 878.84｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-17）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝4.4 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.69 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.4 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.58 x｜期間與口徑：2026-10-20／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝985569.89 USD m｜期間與口徑：2026-10-20／市值 1023824.89 ＋ 淨負債 -38255.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝93.18 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-19（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.04｜期間與口徑：2026-10-19（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-10-20／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）
  - 原文：「price 878.84 / W52 623.18 / W104 366.15 / W250 197.27 / W250 13週斜率 8.15%」

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：China's CXMT is projected to reach ~350,000 wafer starts per month of DRAM capacity by end-2026 — only ~25,000 WSPM behind Micron — putting CXMT in 4th place globally in DRAM (behind Samsung, SK Hynix, Micron) and on track to make China the world's second-largest DRAM production base.
  - 來源：Tom's Hardware, "CXMT close to matching Micron's memory capacity in 2026"（as_of 2026-07-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：Some Chinese PC/memory-module brands (cited: Corsair, HP, Dell) have begun sourcing homegrown DDR5 chips from CXMT and YMTC instead of Samsung, Micron and SK Hynix.
  - 來源：Tom's Hardware, "Chinese memory brands ditch Samsung and Micron for homegrown CXMT and YMTC silicon"（as_of 2026-07-01）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#6`（competitive_share_entrants｜方向 -｜狀態 ok）：Micron CEO Sanjay Mehrotra pushed the US Congress to restrict chip-equipment access for CXMT, YMTC and SMIC, warning that Chinese state-backed investment poses a competitive threat comparable to China's dominance of the solar industry.
  - 來源：Taipei Times, "Micron pushes US Congress to curb Chinese competitors"（as_of 2026-04-23）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：Nvidia CEO Jensen Huang confirmed on 2026-06-05 that Samsung, SK Hynix, and Micron have all passed certification to supply HBM4 for Nvidia's Vera Rubin platform; supply-chain analysts estimate SK Hynix holds roughly 60-70% of Vera Rubin HBM4 volume, Samsung ~25-30%, and Micron the remainder — i.e. Micron's largest AI customer already multi-sources HBM across three qualified suppliers, with Micron as the smallest share.
  - 來源：Yahoo Finance, "Nvidia certifies Samsung, SK Hynix and Micron for Vera Rubin HBM4 supply"; TweakTown, "SK hynix, Samsung, and Micron fighting for NVIDIA supply contracts for new 16-Hi HBM4 orders", https://finance.yahoo.com/sectors/technology/articles/nvidia-certifies-samsung-sk-hynix-133001560.html（as_of 2026-06-05）｜affects：moat_trend、thesis.R、decision_inputs.bear、valuation
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Samsung、SK Hynix、Micron 三家於 2026年6月25日在美國加州北區聯邦法院被 17 名消費者/小型企業提起集體訴訟，指控三家共謀限制commodity DRAM供給、藉擴產HBM為由人為推升價格，四年來漲幅約700%；三家合計約佔全球DRAM營收九成。Micron 否認指控並表示將抗辯。
  - 來源：TrendForce, "Samsung, SK hynix, Micron Face U.S. Class-Action Lawsuit Over Alleged DRAM Supply Manipulation", https://www.trendforce.com/news/2026/06/29/news-samsung-sk-hynix-micron-face-u-s-class-action-lawsuit-over-alleged-dram-supply-manipulation/（as_of 2026-06-25）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：美國於2026年1月14日依Section 232發布公告，對符合特定效能門檻的半導體品項課徵25%進口關稅，2026年1月15日生效；範圍涵蓋先進運算晶片（如Nvidia H200、AMD MI325X）等HTS 8471.50/8471.80/8473.30項下產品。
  - 來源：The White House, Presidential Actions - Adjusting Imports of Semiconductors (whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors...)（as_of 2026-01-14）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：美光在FY2026 10-Q中揭露：美國商務部BIS已於2025年4月14日對半導體、半導體製造設備及其衍生品發起Section 232國安調查，調查結果未定，公司表示此調查可能導致全產業性額外關稅與貿易限制，並可能對美光業務造成不利影響。
  - 來源：Micron Technology Inc, Form 10-Q FY2026 (SEC EDGAR, sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm)（as_of 2026-05-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Micron's FY2026 10-Q risk factors disclose that a substantial portion of its manufacturing operations are located in Taiwan (along with Singapore, Japan, Malaysia, China, India), and that trade restrictions, tariffs, export controls, and sanctions involving the U.S., China, Taiwan, and Korea can directly affect what Micron can sell, where, and how it sources materials/equipment.
  - 來源：Micron Technology Inc. Form 10-Q FY2026, SEC EDGAR (mu-20260226.htm)（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Investor risk-factor analysis describes Micron as having 'extreme Taiwan dependency,' with Taiwan characterized as the central hub of the global tech supply chain, magnifying the potential for catastrophic disruption to Micron's operations from a regional conflict.
  - 來源：Holdingschannel.com, "Micron Risk Factors: Key Threats To MU Stock Explained For Investors"（as_of 2026-04-07）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：China's Cyberspace Administration determined in May 2023 that Micron products posed a national security risk and banned Micron chips from purchase by operators of China's critical information infrastructure; this remains the realized precedent cited in current (2026) risk analyses for Micron's China-market exposure.
  - 來源：TechCrunch, "China bans Micron" / PhoneArena, "China bans shipments from U.S. memory chipmaker Micron Technology"（as_of 2023-05-21）｜affects：thesis.R、decision_inputs.bear、valuation
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：Micron is acquiring Powerchip Semiconductor Manufacturing Corp's (PSMC) fab site in Tongluo, Taiwan (a 300,000 sq ft cleanroom) for $1.8 billion to expand DRAM and HBM capacity; deal expected to close in 2H2026, with meaningful DRAM wafer output targeted for 2H2027 — this increases, rather than diversifies, Micron's manufacturing footprint concentration in Taiwan.
  - 來源：MarketWise, "Micron's $1.8B Taiwan Fab Deal: What It Means for AI & Investors" (also reported by Tom's Hardware)（as_of 2026-01-23）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `geo_supply_chain#5`（geo_supply_chain｜方向 -｜狀態 ok）：Report on Micron's Taiwan HBM fab workers raising strike-risk concerns and seeking a larger share of pay amid the AI memory supercycle, highlighting labor/operational risk concentrated at Micron's Taiwan production sites.
  - 來源：Tech Times, "Micron Taiwan Strike Risk: HBM Workers Claim Share of AI Memory Supercycle"（as_of 2026-09-02）｜affects：thesis.R、decision_inputs.bear
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：TrendForce將2026年智慧型手機出貨展望下修為年減2%（原預估+0.1%），筆電出貨展望下修為年減2.4%（原預估+1.7%），主因記憶體漲價侵蝕終端需求
  - 來源：TrendForce Press Center, https://www.trendforce.com/presscenter/news/20251117-12784.html（as_of 2025-11-17）｜affects：thesis.R、decision_inputs.bear
- `end_markets#6`（end_markets｜方向 -｜狀態 ok）：2026年全球車用產業因DRAM/NAND嚴重短缺面臨供應鏈危機，因記憶體大廠將產能與資本支出轉向高毛利HBM/DDR5，不願維持成熟製程產能，造成車用/工業用舊製程晶片人為稀缺
  - 來源：EE Times, https://www.eetimes.com/automakers-face-memory-shock-as-ai-uses-up-semiconductor-supply/（as_of 2026）｜affects：thesis.R、decision_inputs.bear
- `end_markets#8`（end_markets｜方向 -｜狀態 ok）：TrendForce（2026-07-30發布）預期2027年DRAM與NAND走勢分化：DRAM因HBM產能持續排擠、伺服器需求強勁維持供給緊張、價格上行；NAND則因新產能開出、消費性需求疲弱，預估2027下半年供給轉為寬鬆，價格承壓
  - 來源：TrendForce Press Center, https://www.trendforce.com/presscenter/news/20260730-13158.html（as_of 2026-07-30）｜affects：thesis.R、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Samsung 與 SK hynix 據報正在探索超越 HBM（高頻寬記憶體，AI 加速卡用來加速資料存取的記憶體規格，美光靠此打入 AI 供應鏈）的次世代 AI 記憶體架構，可能挑戰 Nvidia 現有記憶體使用方式
  - 來源：TrendForce, "Beyond HBM: Samsung, SK hynix Reportedly Explore Next-Gen AI Memory That Could Challenge NVIDIA", https://www.trendforce.com/news/2026/03/10/news-beyond-hbm-samsung-sk-hynix-reportedly-explore-next-gen-ai-memory-that-could-challenge-nvidia/（as_of 2026-03-10）｜affects：moat_trend、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-06-25 於 N.D. Cal. 提起 DRAM 買方集體反托拉斯訴訟，被告含 Micron、Samsung、SK hynix，指控限制供給與操縱價格（期間自 2022-10-26 起）；2026-07-17 夏威夷聯邦地院另有類似個人訴訟
  - 來源：SEC EDGAR 10-K FY2026 Item 8 Antitrust Matters（as_of 2026-10-09）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：在 2023 年那波記憶體下行中，DRAM 與 NAND 價格自 2021 年第 3 季高點起分別下跌 57% 與 55%；2023 年 DRAM 市場營收萎縮至 420 億美元（年減 47%），NAND 萎縮至 370 億美元（年減 37%）
  - 來源：StorageNewsletter, 'WW 2023 Memory Market Declining to $42 Billion for DRAM (-47% Y/Y) and $37 Billion for NAND (-37% Y/Y)'（as_of 2023-07-21）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Micron FY2023（截至 2023 年 8 月）毛利轉負，毛利為 -14.16 億美元（營收 155.4 億美元），全年淨損 58.33 億美元
  - 來源：Micron Technology Inc, SEC Form 8-K FY2023 press release（as_of 2023-09-27）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Micron 單季毛利率在 2023 年 8 月觸及近 5 年低點 2.7%
  - 來源：Macrotrends, 'Micron Technology Gross Margin 2012-2026'（as_of 2023-08-31）｜affects：thesis.R、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-06-25 N.D. Cal. DRAM 買方集體反托拉斯訴訟（Micron、Samsung、SK hynix）
  - 來源：SEC EDGAR 10-K FY2026 Item 8 Antitrust Matters（as_of 2026-10-09）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":2700,"bear_5y_price":450,"p_bull_pct":25,"p_bear_pct":35,"upside_5y_pct":64.1,"ev5y_pct":57.6,"irr_base_pct":10.4,"asym_ratio":2.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":176.55,"pe":5.13,"basis":"FY2027E（2027 年 8 月止）共識 non-GAAP EPS；現價 904.9÷176.55；終端倍數同樣套在年度 EPS 上"},"eps":{"bull":[186,230,240,215,225],"base":[176,200,172,118,135],"bear":[158,125,45,12,30]},"pe":{"bull":12,"base":11,"bear":15},"p":{"bull":25,"base":40,"bear":35},"yield_pct":{"dividend":0.062,"net_buyback":0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"valuation_dependent":true}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MU_Q4_2026_Earnings_Call_20260930.md
- 2026-09-30｜Mark Murphy｜guidance：CFO 補充 FQ1 指引含的位元成長與成本降幅口徑（DRAM、NAND 皆是）（原話："single-digit sequential bit growth and double-digit for cost"）
- 2026-09-30｜Mark Murphy｜guidance：CFO 說明 FY27 研發費用年增幅（排除獎金效應）將超過上季所說的 10 億美元（原話："more than the $1 billion that we said last quarter"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 表示 FY27 出貨已有超過七成五被承諾，因此配置談判延伸到 2028（原話："more than 75% of our shipments committed for the year"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 對 2028 供需的說法：看不到供需平衡的時點（原話："don't have line of sight to when supply and demand balances"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 說明 FY27 中國營收占比預期降到個位數（原話："exposure will be in the single-digit range in fiscal '27"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 表示業界 DRAM 供給明年出貨下降；Idaho 首批晶圓出貨在 2027 年中（原話："first wafer output from our Idaho facility mid-calendar '27"）
- 2026-09-30｜Mark Murphy｜margin：CFO 拆解 FY27 毛利擴張來源：漲價放緩、產品組合改善，起動成本為部分抵銷（原話："the partial offset to price and favorable mix would be"）
- 2026-09-30｜Mark Murphy｜margin：CFO 說明 FY27 全年相對 Q1 仍有毛利擴張，來自持續但較溫和的漲價（原話："we would see margin expansion relative to Q1"）
- 2026-09-30｜Manish Bhatia｜margin：COO 說明 HBM 2027 曆年價格已大幅調升，以縮小與傳統 DRAM 的獲利差距（原話："to narrow the profitability gap with conventional DRAM"）
- 2026-09-30｜Manish Bhatia｜margin：CTO 回應同製程是否降成本：同產線可調組合，但 COO 稱不一定有助成本（原話："But I wouldn't say that it helps necessarily with cost."）
- 2026-09-30｜Scott DeBoer｜competition：CTO 稱技術領先中國競爭者至少兩個節點（原話："our technology leadership is at least 2 nodes ahead"）
- 2026-09-30｜Manish Bhatia｜competition：COO 對 HBM 市占目標的說法：約等於整體 DRAM 市占，不鎖定單一數字（原話："we do expect our HBM share to be around our broader DRAM"）
- 2026-09-30｜Scott DeBoer｜competition：CTO 稱各代 HBM 的差異在功耗、速度與產品良率，認為將持續是美光強項（原話："the first major custom HBM product out in the market"）
- 2026-09-30｜Scott DeBoer｜product：CTO 說明與 NVIDIA 共同設計 HBM4E（NVHBM），為首款主要客製 HBM 產品（原話："On HBM4E, this co-design is on a foundry process"）
- 2026-09-30｜Scott DeBoer｜product：CTO 澄清 HBM4E 共同設計不是自家基底晶粒，而是晶圓代工製程（與 HBM4 不同）（原話："On HBM4E, this co-design is on a foundry process"）
- 2026-09-30｜Scott DeBoer｜product：CTO 說明 1-gamma 已占多數位元，1-delta 預計明年下半年放量（原話："our 1-gamma DRAM technology is already the majority"）
- 2026-09-30｜Manish Bhatia｜product：COO 稱 DRAM 位元成長受 HBM 轉移與 HBM 交換比率上升壓抑（原話："these are increasing trade ratio"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明 SCA 涵蓋 DRAM 與 NAND，DRAM 比例略低於約 35%，NAND 略高（原話："the SCA agreements do cover both DRAM and NAND"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明 SCA 營收約四分之三有明定價格框架，約四分之一隨市場協商（原話："about 3/4 of the SCA have this"）
- 2026-09-30｜Manish Bhatia｜customer：COO 稱新簽 SCA 的談判反映當前市況與漲價方向，不同於先前以 CQ2 市況定價者（原話："the direction of travel has been for higher pricing"）
- 2026-09-30｜Manish Bhatia｜customer：COO 回應手機與 PC：位元出貨連續下滑但營收因價格與組合成長（原話："We did see sequential bit decline in our mobile and client"）
- 2026-09-30｜Manish Bhatia｜customer：COO 稱客戶正在以現有記憶體供給最大化運算晶片出貨，形成潛在需求（原話："customers are choosing to maximize the compute silicon"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明代理式 AI 帶動 CPU 需求與伺服器單位數成長，並稱 DRAM 是主要限制（原話："server units are growing so strongly"）
- 2026-09-30｜Mark Murphy｜capital_allocation：COO 與 CFO 說明 FY27 資本支出增加主要為廠房建設，多數為 2028 後才投產的無塵室（原話："the majority of the increase is for construction CapEx"）
- 2026-09-30｜Mark Murphy｜capital_allocation：CFO 稱建廠支出不等於位元產出，設備依市場需求與 SCA 配置（原話："SCAs are a good way for us to keep a pulse on the market"）
- 2026-09-30｜Manish Bhatia｜risk：COO 提到新增無塵室從啟用到有意義出貨仍需數季（原話："it takes a few quarters for meaningful shipments to come"）
- 2026-09-30｜Manish Bhatia｜risk：COO 說明 FY26 美光 NAND 供給成長低於業界，因 Singapore 無塵室被研發線與 HBM 試產占用（原話："our supply growth grew less than the industry this year"）
- 2026-09-30｜Manish Bhatia｜commitment：COO 表示不更新 HBM TAM 展望（原話："We are not updating that TAM outlook right now."）
- 2026-09-30｜Manish Bhatia｜commitment：COO 承諾依需求趨勢才為無塵室裝機擴產（原話："we will equip the clean rooms and build capacity to the"）
- 2026-09-30｜Manish Bhatia｜commitment：COO 稱 SCA 占比未來可能提高，持續談判中（原話："this number could get up to be higher in the future"）

### 問答異常語氣（迴避／改口／保留）
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Reitzes 問 2028 為何比 2027 更緊、對毛利意味什麼（認為看不出 2028 毛利會不同於 2027）｜答法：COO 與 CFO 談需求與供給結構與漲價放緩、組合與起動成本，未給 2028 毛利數字或與 2027 的差異
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Weathers 問 HBM TAM 更新數字及位元與價格拆分｜答法：明說不更新 TAM，未拆位元與價格，改談 HBM 成長快於傳統 DRAM
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Weathers 問 HBM 市占目標是否仍為低 20% 區間｜答法：未確認舊目標，改稱約等於整體 DRAM 市占、不鎖定單一數字
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Malik 問 SCA 占 2030 年銷售 35% 中 DRAM 與 NAND 的拆分｜答法：拒絕拆分，只給 DRAM 略低於約 35%、NAND 略高的方向，事後再要求澄清該回答
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Schneider 問 SCA 價格上下限是否整體重設及是否含超大規模客戶｜答法：稱有多種框架、不點名客戶，未直接回答上下限是否整體重設或超大規模客戶是否納入
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Hosseini 問 FY27–28 NAND 位元出貨能否與業界約 25% 持平｜答法：稱不評論那麼遠，只談業界成長與產能因素，未給自家數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 8 | 4 |
| customer_second_source | found | 2 | 4 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 6 | 4 |
| end_markets | found | 9 | 5 |
| substitute_technology | found | 1 | 4 |
| channel_business_model_shift | found | 2 | 4 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 5 | 2 |
| cyclical_inventory_price_position | found | 5 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260705","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"本輪記憶體上行因「結構性 AI 需求 + 供給紀律」延長，循環不像過去 ~2 年見頂崩落（最關鍵也最脆弱，依賴循環定價非永續複利）","columns":{"2Y 驗證點":"2026-2027 DRAM/HBM 合約價維持正成長、毛利率守 60%+","5Y 驗證點":"through-cycle normalized 毛利率台階較上輪（~30%）抬升至 40%+","10Y 驗證點":"記憶體不再是純商品，AI 使需求基底結構性黏著","數字門檻":"HBM 2028 達 $100B、CAGR ~40%；2026 產能售罄；AI 吃掉 ~70% 記憶體增量","來源":"Micron 法說、TrendForce、SK 集團主席","漂移觸發":"連 2 季 DRAM 合約價 TTM 偏離 ≥5% 向下 → 削弱"}},{"id":"H2","text":"Micron 在 HBM4／HBM4E 守住 ~20% 份額並改善獲利結構，不被 SK Hynix / Samsung 邊緣化","columns":{"2Y 驗證點":"HBM4 份額 ≥18%、取得 NVIDIA Rubin 平台合格量產（已達成）","5Y 驗證點":"HBM4E（2027 ~40% 市場）份額不低於 HBM4","10Y 驗證點":"在 custom HBM / 先進封裝整合維持三強之一","數字門檻":"HBM4 份額 ~20%（mid-range）；HBM4 11Gbps 送樣、Rubin 合格","來源":"Astute Group、TrendForce 2026/02","漂移觸發":"連 2 季 HBM 份額 TTM 下滑 ≥3pp → 削弱"}},{"id":"H3","text":"估值不在峰值 EPS 上被進一步 re-rate；當前股價已大致反映（甚至超額反映）多頭預期（市場假設）","columns":{"2Y 驗證點":"股價不顯著超越分析師均值目標 ~$1,486、且不再獲得更高倍數","5Y 驗證點":"循環下行時倍數不系統性下移（如 2022-2023 那樣）","10Y 驗證點":"市場願給記憶體龍頭結構性更高倍數","數字門檻":"均值目標 $1,486（42 位，strong_buy）；現價 $976 已在其下 35%，但 P/B 15.2x 峰值","來源":"yfinance targetMeanPrice / TipRanks 共識","漂移觸發":"股價回 $1,255 ATH 上方（再獲更高倍數）→ H3 削弱、R:R 惡化"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"記憶體循環反轉——合約價 QoQ 轉跌、毛利率自峰值回落","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"TrendForce DRAM/HBM 月度合約價","警戒閾值":"連 2 季持平或轉負 → 循環軌了結 / 放棄進場"}},{"id":"R2","text":"HBM 競爭——Samsung HBM4 強勢回歸 + SK Hynix 領先，Micron 份額／獲利結構被壓","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 HBM 份額、HBM4 大客戶合格進度","警戒閾值":"份額連 4 季 TTM 下滑 ≥3pp → moat_trend 降 ↓"}},{"id":"R3","text":"資本密集吞噬報酬——擴產 capex（FY26 &gt;$25B）長期壓低 through-cycle FCF / ROIC；中國供給替代（CXMT/YMTC）加劇","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"capex/營收、through-cycle FCF margin、ROIC−WACC、中國成熟節點份額","警戒閾值":"下一輪低谷 FCF 再度轉負 + ROIC &lt; WACC → 重估產業質地"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","irr_base_pct":0.6,"ev5y_pct":6.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":6.8,"irr_base_pct":0.6,"max_dd_pct":-70.0,"bull_5y_price":1700.0,"bear_5y_price":470.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","price_at_dd":975.56,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MU","date":"2026-10-20","schema":"v15.0","contract":"v19","company_name":"Micron Technology, Inc."},"oneliner":"美光 FY2027 共識每股盈餘 176.55 美元，現價約 5 倍，但這個便宜建立在峰值毛利上；長約延後了下一次合約價下行，沒有取消它。循環位置偏晚，等合約價轉跌、止跌兩季後再談進場","facts_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/facts.json","scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/scenario.json","answers":{"q1_business":{"verdict":"美光賺的是記憶體位元稀缺的錢，雲端、資料中心、手機與 PC、車用客戶都在付漲價；利潤卡在 DRAM 供給這一節點，本季 80% 營益率主要靠價格撐出來，量的貢獻有限","reasoning":"FQ3'26 營收 414.56 億美元，GAAP 營益率 80.4%，non-GAAP 81.2%；FQ4 財測營收 500 億美元（±10 億）、毛利率約 86%、non-GAAP EPS 31 美元。FQ2'26 四個業務單位都超過營收一成：雲端記憶體 77.49 億、核心資料中心 56.87 億、手機與用戶端 77.11 億、車用與嵌入式 27.08 億美元（2026-03-18 第二季新聞稿）。最大單一客戶占比由 FY26 第一季的 17% 降到前九個月的 10%，前十大客戶約占 FY2025 營收一半，集中度在下降。2026-09-30 法說會上，COO 說 DRAM 已是 AI 資料中心的主要瓶頸，CFO 說 FQ1'27 財測的位元季增只有個位數、單位成本降兩位數，所以營收成長幾乎全是價格。產業態勢屬雙向拉鋸：結構轉好的一邊是多年期長約（SCA）、HBM 排擠一般 DRAM 產能、新無塵室要兩年才投產；另一邊是其他結構變動，包括 DRAM 買方反托拉斯集體訴訟，以及中國 CXMT 的 DRAM 月產能已逼近美光。景氣時鐘判第三期過熱：合約價季增幅由第二季的 58–63% 收斂到第三季的 13–18%，手機與 PC 位元連兩季下滑，毛利率財測卻創新高。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_q4_fy2026_guidance","f_earnings_recency"],"verdict_values":{"revenue_quality":"營收主要由合約價驅動。SCA 約四分之三有明定價格框架、多數設有上下限，到 2030 年約覆蓋 35% 的 DRAM 位元（2026-09-30 COO）；其餘部分隨市價波動","unit_econ_note":"FQ1'27 位元季增個位數、單位成本降兩位數；80% 營益率是漲價撐出的峰值，不是規模經濟","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"近五年有虧損年（FY2023 毛利率 -9.11%）；毛利率由負數擺到財測約 86%；營收由合約價主導；屬記憶體產業"},"industry":{"clock_phase":"III","sd_verdict_source":"供需判斷：HBM 排擠與無塵室建置期撐住 2027–2028 的緊張（SK 海力士、TrendForce、美光 COO 三方一致）。但業界建設型資本支出正在加速，2028 下半年起新無塵室陸續投產，供給可逆性高。判為週期性將反轉，只是時點延後","bargaining":{"up":"設備端依賴 EUV，美光已和設備商簽長期供貨協議；供應商集中度事實表未涵蓋","down":"前十大客戶約占營收一半；最大客戶占比由 17% 降到 10%；輝達的 HBM4 同時向三家採購，美光分到的量最少","geo":"台灣產能占比高，力積電銅鑼廠交割後集中度更高；中國營收占比 FY27 預期降到個位數"},"profit_pool_dir":"利潤池目前流向記憶體：美光 TTM 毛利率 72.57%，已逼近輝達的 74.67%。這是稀缺帶來的暫時分配，供給追上後會回流","tam_table":{"expanded":false,"reason":"管理層 2026-09-30 明說不更新 HBM 市場規模，事實表也沒有滲透率序列；本檔的承重點是價格循環，不是滲透率曲線"}}}},"q2_moat":{"verdict":"護城河方向持平。製程與 HBM 認證守住第三名，執行面在擴大；但定價力來自全產業稀缺，不是美光獨有，HBM 議價又被輝達多源採購壓住，兩邊相抵","reasoning":"機制有三：一是製程節點，1-gamma 已占多數位元，CTO 稱領先中國至少兩個節點（2026-09-30）；二是 HBM 認證資格，HBM4 已量產供 Vera Rubin，並與輝達共同設計 HBM4E；三是 SCA 多年期 take-or-pay 長約。執行面在擴大：NAND 份額升到 15%（2026Q2），最大客戶依賴度下降。定價面在縮減：輝達 HBM4 三家都認證，美光分配最少；CXMT 的 DRAM 月產能預計 2026 年底只落後美光約 2.5 萬片；管理層也不再確認 HBM 份額要拿到二成出頭的舊目標。同業表是 AI 價值鏈公司，不是記憶體廠，算不出同業報酬差，只能用份額方向當替代證據。執行力給 8 分、定價力給 6 分。","fact_refs":["f_peer_mu_gross_margin_pct","f_peer_mu_operating_margin_pct","f_peer_mu_fcf_margin_pct","f_peer_nvda_gross_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_tsm_gross_margin_pct","f_peer_avgo_gross_margin_pct","f_peer_amd_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"製程節點領先（1-gamma 為主力、1-delta 2027 下半年放量）＋HBM 認證資格＋SCA 多年期長約綁住客戶配置","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：NAND 份額升到 15%，HBM4 量產供貨。定價面縮減：輝達 HBM4 分配美光最少，CXMT 產能逼近美光。兩相抵銷，判持平","competitor_notes":[{"name":"SK hynix","strategy_note":"HBM 龍頭，份額由 64% 降到約 50%，堅持供給紀律；美光 HBM 份額增加的主要來源"},{"name":"Samsung","strategy_note":"HBM4 已回歸並取得輝達認證，2026 年資本支出約 200 億美元、年增 11%，對美光 HBM 價格壓力最大"},{"name":"CXMT","strategy_note":"有國家資金支持，2026 年底 DRAM 月產能約 35 萬片、只落後美光約 2.5 萬片，主攻商品 DDR5 與中國客戶"},{"name":"YMTC","strategy_note":"中國 NAND 廠，已打進部分模組品牌的採購名單，壓的是商品 NAND 價格"},{"name":"NVDA","strategy_note":"最大的 AI 客戶，也是價值鏈上分利潤的對手；向三家採購 HBM，壓住單一供應商的議價"}],"peer_na_reason":"事實表同業為 NVDA、TSM、AVGO、AMD，都不是記憶體廠；三星與 SK 海力士的報酬率未收錄，算不出同業報酬差","threats":[{"level":"🟡","text":"CXMT 擴產逼近美光，中國品牌改採國產 DDR5。屬於商品 DRAM 的點對點破壞性競爭","p":"40%","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5"]},{"level":"🟡","text":"輝達 HBM4 三家都認證、美光分配最少，HBM 定價受多源採購壓制","p":"50%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"三星與 SK 海力士在探索 HBM 之後的 AI 記憶體架構，目前只有報導，沒有產品時程","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）；依資本密集的產業結構，判為高利益率×低周轉，重點在再投資負擔","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"資料中心的需求是真需要：COO 說客戶在現有記憶體量下盡量多出運算晶片，存在潛在需求。但消費端是可延後的需求，手機與 PC 位元已連兩季下滑，TrendForce 也下修 2026 年手機與筆電出貨"},{"item":"決策層級","level":"🟡","text":"HBM 的重新認證週期與 SCA 的五年期合約提高了轉換成本；但最大的 AI 客戶本來就向三家採購，在產品層的替代性仍高"},{"item":"價值鏈分配","level":"🟡","text":"DRAM 目前是瓶頸，美光毛利率逼近輝達，代表記憶體正在多分利潤。這靠的是稀缺，2028 年後新無塵室開出，分配會回流到運算端"},{"item":"社會容忍度","level":"🔴","text":"DRAM 買方指控四年漲價約 700%，已提起反托拉斯集體訴訟；車用廠商因記憶體短缺出現供應危機；中國 2023 年禁用美光的先例還在。價格上限實際由社會與政治決定，低於經濟上限"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋（資本支出全年數、折舊、營運資金變動都沒收錄；只知 FQ3'26 淨資本支出 70.84 億美元）","endo_ceiling":null,"formula_note":"ROIC＝稅後營益率×投入資本周轉率；TTM 營益率 65.67% 已知，投入資本缺，未計算。管理層的選擇是用 SCA 鎖住配置、建廠支出先行、裝機看需求，以延長稀缺的持續期，代價是建廠支出在出貨前就先燒掉"}}}},"q3_growth":{"verdict":"成長跑道屬中等。成長幾乎全來自漲價，量受無塵室限制到 2028 年；HBM 份額成長了但沒有找到第二條曲線，五年後的成長靠下一輪漲價，不靠滲透率","reasoning":"共識每股盈餘 FY2027E 176.55、FY2028E 204.47、FY2029E 203.33，第三年持平，賣方沒有模擬下行。以 FY2026 實績約 74.35（股價÷trailing 本益比反推）為基期，三年年化約 39.8%；若從 FY2027 起算只有 7.3%。缺口全部歸因於毛利率擴張（毛利率由 FY2025 的 39.79% 到財測約 86%），不是再投資帶來的內生成長。近 3 個月 FY1 共識上修 140.63%，其實是財年換季（FY2026 換成 FY2027），不是真上修；同一財年兩次快照之間 FY1 只上修 0.23%、FY2 反而下修 0.9%。衰退訊號亮三項：提價後手機與 PC 位元連兩季下滑；盈餘成長遠快於營收（FY2025→FY2027E 營收約 7.4 倍、EPS 約 23 倍）；FCF 對淨利 FY2024 為 0.16、FY2025 為 0.20，連兩年低於 0.75。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_pe_current"],"verdict_values":{"growth":{"driver_mix":"以價格為主：合約價年增倍數；FQ1'27 位元季增只有個位數，2028 年前量的成長受無塵室限制；不靠併購與回購","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本缺，內生上限算不出；共識三年年化約四成全部來自漲價與毛利率擴張，判定超出任何以再投資支撐的內生上限","segments":[{"item":"雲端記憶體（CMBU）","value":"77.49 億美元（FQ2'26，占 32.5%）"},{"item":"核心資料中心（CDBU）","value":"56.87 億美元（FQ2'26，占 23.8%）"},{"item":"手機與用戶端（MCBU）","value":"77.11 億美元（FQ2'26，占 32.3%）；位元已連兩季下滑"},{"item":"車用與嵌入式（AEBU）","value":"27.08 億美元（FQ2'26，占 11.3%）"}],"decay_signals":["主力產品提價後銷量下滑：手機與 PC 位元連兩季季減（2026-09-30 法說）","盈餘成長顯著高於營收成長：毛利率由 39.79% 擴張到財測約 86%","FCF 對淨利連兩年低於 0.75：FY2024 約 0.16、FY2025 約 0.20"],"trap_rating":"🔴"}}},"q4_capital":{"verdict":"現金大量流入，但再投資報酬還沒證實。FQ3'26 調整後自由現金流 183.04 億美元，淨現金約 382.55 億；新增資本支出以建廠為主，2028 年後才投產，報酬要到下一輪才看得到","reasoning":"FQ3'26 營業現金流 253.88 億、淨資本支出 70.84 億，調整後 FCF 約為 GAAP 營業利益的 55%。SBC 3.41 億美元、占營收 0.82%，年化約 13.6 億，對約 1.02 兆美元市值約 0.13%，稀釋可忽略。股息殖利率 0.062%；回購金額與均價事實表未涵蓋。CFO 說 FY27 研發年增超過 10 億美元（2026-09-30），建廠支出是先燒錢、後出貨。力積電銅鑼廠 18 億美元屬資產收購，還沒產出，已實現報酬算不出來。","fact_refs":["f_kpi3_adjusted_fcf","f_kpi4_sbc_gaap","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"唯一一筆收購是力積電銅鑼廠 18 億美元（資產收購），目標 2027 下半年出貨，已實現報酬算不出來"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購金額與均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 季 3.41 億美元、占營收 0.82%；年化約占市值 0.13%，遠低於每年 1.5% 的門檻；股數淨變化事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回購與現金去向四分的資料事實表未涵蓋，無法展開"}}}},"q5_valuation":{"verdict":"現價要成立，前提是 2029 年後的下行比過去淺，FY2031 盈餘還能回到約 135 美元並拿到 11 倍。我半信：長約下限是新東西，但它的金額只覆蓋峰值營收的一小塊。估值判合理，不判便宜","reasoning":"現價 904.9 美元，對 FY2027 共識約 5.1 倍、對 FY2028 約 4.4 倍，trailing 12.17 倍；P/S 7.69 倍、EV/S 7.4 倍，都在年度端點的最高分位，前瞻 EV/S 3.58 倍。低本益比是峰值盈餘造成的，分母本身就是爭點。PEG 0.13（4.98÷39.8）因成長全靠漲價而失真，不能當便宜的證據。短期以維持目前前瞻倍數、往後滾一年估算：FY2028E 204.47×5.1≈1,043 美元，約 +15%。中期取基準情境 FY2031 為 135×11≈1,485 美元，約 +64%。賣方均價目標 1,308（Benzinga，26 位）到 1,522（Walnut，42 位）兩個口徑不一致，只當區間參考。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_net_debt_m","f_ev_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027E）搭配自身年度端點 P/S；記憶體慣用的 P/B 事實表未涵蓋","tier":"記憶體三強（同業本益比事實表未涵蓋）","peers":{"expanded":false,"reason":"事實表同業為 NVDA、TSM、AVGO、AMD，屬不同層級；沒有三星、SK 海力士的倍數，不能跨層級當錨"},"fwd_pe":4.98,"peg":0.13,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價÷FY2027 共識約 5.1 倍，隱含市場預期 2029 年後盈餘大幅回落。基準情境（FY2030 盈餘較 FY2027 低約三成、終端 11 倍）五年年化約一成，屬合理區。但 P/S 在年度端點最高、分母是峰值盈餘，便宜的論證不成立，所以判黃不判綠。五年分位事實表未涵蓋，只有 3 到 4 個年度端點：本益比在 4.4 分位、P/S 在 100 分位","upside_short_pct":15.2,"upside_mid_pct":64.1,"denominator_disputed":true,"denominator_note":"分母 FY2027 盈餘建立在約 86% 毛利率與合約價年增倍數上，是循環峰值。P/B 事實表未涵蓋，改以 P/S 位於年度端點最高、以及前次下行毛利率轉負作對照"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把峰值盈餘當成常態。5 倍本益比看起來便宜，但它是商品循環高點的典型讀數","reasoning":"衰退訊號亮三項，價值陷阱判紅：提價後位元下滑、盈餘成長遠快於營收、FCF 轉換率連兩年偏低。26 週漲 93.18%，RSI 已回落到 34.04，股價自前份 975.56 美元降到 904.9 美元，市場已開始計價高點。週線均線排列仍完整。前次下行營收年減 49%、毛利率轉負，最大回撤取 -50% 到 -70%。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ps_percentile"],"verdict_values":{"trap":{"verdict":"🔴","label":"峰值利潤率陷阱：低本益比建立在漲價撐出的毛利上"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":176.55,"pe":5.13,"basis":"FY2027E（2027 年 8 月止）共識 non-GAAP EPS；現價 904.9÷176.55；終端倍數同樣套在年度 EPS 上"},"eps":{"bull":[186,230,240,215,225],"base":[176,200,172,118,135],"bear":[158,125,45,12,30]},"pe":{"bull":12,"base":11,"bear":15},"p":{"bull":25,"base":40,"bear":35},"yield_pct":{"dividend":0.06,"net_buyback":0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"max_dd":{"lo":-70,"hi":-50,"basis":"前次下行時，DRAM 與 NAND 合約價自高點跌 57% 與 55%，FY2023 營收年減 49%、毛利率轉負（-9.11%）。現在毛利率財測約 86%、P/S 位於年度端點最高、26 週漲 93%，倍數與利潤率會一起回落。下緣 -70% 對應合約價腰斬且市場不採信長約下限，上緣 -50% 對應長約下限部分有效","trigger_time":null},"basis":{"bull":"長約與 HBM 排擠讓供給緊張延到 2029 年，下行只是漲幅停滯；FY2031 盈餘 225 美元，市場改給記憶體 12 倍（以自身 trailing 12.17 倍對照）","base":"2028 下半年新無塵室投產，FY2029 到 FY2030 合約價回落、毛利率降到五成上下，由長約下限托住；FY2031 盈餘 135 美元×11 倍（同業本益比事實表未涵蓋，以自身 trailing 12.17 倍對照）","bear":"業界同步擴產加上 CXMT 放量，2029 年合約價腰斬，FY2030 盈餘 12 美元；FY2031 進入復甦初期，30 美元×15 倍（低谷盈餘給較高倍數）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"前次下行合約價自高點跌 57% 與 55%，FY2023 毛利率轉負；TrendForce 預期 NAND 在 2027 下半年轉寬鬆；業界建設型資本支出加速，CXMT 產能逼近美光","assumption":"長約下限加上 HBM 排擠，讓本輪下行比過去淺","consequence":"2029 年合約價腰斬，FY2030 盈餘掉到二十美元以下，五年後股價落在 450 美元附近","ruling":"採納。空頭機率給 35%，情境終點約 -50%；這條與唯一致命點（合約價轉負）是同一件事","watch":"TrendForce 每季合約價、美光每季毛利率財測","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","end_markets#8","competitive_share_entrants#4"],"fact_refs":["f_ps_percentile"]},{"view":"論點成功但股東經濟變差","evidence":"DRAM 買方提起反托拉斯集體訴訟（依 Sherman Act 可求三倍賠償）；台灣 HBM 員工要求分潤、有罷工風險；車用客戶因短缺承壓；FY27 研發年增超過 10 億美元；建廠支出要到 2028 年後才轉成出貨","assumption":"稀缺帶來的利潤會留在股東手上","consequence":"供給緊張雖然延續，但賠償、勞動成本與先行建廠支出吃掉超額利潤，FCF 只有營業利益的五成多","ruling":"部分採納。FCF 轉換率列為持續監測項；賠償金額未知，不放進情境數字","watch":"集體認證裁定、每季 FCF 對營業利益比","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","geo_supply_chain#5","end_markets#6"],"fact_refs":["f_kpi3_adjusted_fcf"]},{"view":"價格已反映太多","evidence":"Goldman 稱美光一家占 S&P 500 盈餘上修的 51%；賣方目標價 1,308 到 1,522；共識 FY2029 盈餘與 FY2028 持平，沒有模擬下行；同一財年快照之間 FY2 共識已下修 0.9%","assumption":"5 倍本益比代表便宜","consequence":"分母是峰值，P/S 7.69 倍位於年度端點最高；共識一旦開始反映下行，倍數不會擴張，盈餘先降","ruling":"採納。便宜論證無效，估值只判合理","watch":"FY2 與 FY3 共識是否連續下修","evidence_refs":["capital_markets_pricing#5","capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_consensus_rev_fy2_pct","f_ps_current","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"台灣產能占比高，銅鑼廠交割後集中度更高；中國 2023 年禁用美光的先例；232 條款半導體調查與關稅","assumption":"地緣風險不會在五年內實現","consequence":"台灣停工或關稅擴及記憶體，會直接打斷出貨或壓縮毛利","ruling":"不放進情境，列為尾端風險。COO 說 FY27 中國營收占比降到個位數（2026-09-30），中國禁令的衝擊已縮小","watch":"台灣廠區運作、232 條款裁定是否涵蓋記憶體","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#4","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 975.56 → 本次 904.9（-7.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=975.56","side_b":"本次 price_at_dd=904.9","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 975.56 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 975.56 美元：Bull 價 1,700、Bear 價 470，五年期望值 +6.8%，基準年化 0.6%，不對稱比 1.4","side_b":"本次情境、股價仍用 975.56 美元：Bull 價 2,700、Bear 價 450，五年期望值 +46.2%，基準年化 8.8%，不對稱比 2.34","ruling":"先換情境、股價不動：五年期望值多 39.4 個百分點，基準年化多 8.2 個百分點。不對稱比由 1.4 變為 2.34。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 975.56 美元：五年期望值 +46.2%，基準年化 8.8%，不對稱比 2.34","side_b":"本次情境、股價 904.9 美元：五年期望值 +57.6%，基準年化 10.4%，不對稱比 2.82","ruling":"再換股價、情境不動：起點價下跌 7.2%，五年期望值多 11.4 個百分點，基準年化多 1.6 個百分點，不對稱比由 2.34 升到 2.82。合計五年期望值比前份多 50.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值、陷阱、訊號、裁決","cause":"新證據","prior_field":["val","trap","signal"],"side_a":"前份：估值紅、陷阱黃、訊號 B，觀望","side_b":"本次：估值黃（FY2027 共識 176.55、現價約 5 倍）、陷阱紅（衰退訊號亮三項）、訊號 B 不變","ruling":"估值由紅轉黃，主因是盈餘分母換到 FY2027 且大幅高於前份的 FY2026，加上新簽十份 SCA；股價由 975.56 降到 904.9 是次因。陷阱轉紅，是因為手機與 PC 位元連兩季下滑屬新證據，加上 FCF 轉換率連兩年偏低。裁決與角色依新輸入重新路由","evidence_level":"高","settle_metric":"FQ1'27 毛利率與手機用戶端位元","if_then":["若 FQ1'27 毛利率低於 75%→已持有者減碼至半倉","若手機與用戶端位元回到季增且毛利率續升→陷阱降回黃，維持不加碼"],"evidence_refs":["channel_business_model_shift#1","capital_markets_pricing#2","end_markets#5"]},{"axis":"前份漂移：護城河方向、跑道、類型、循環位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：持平、跑道中等、循環/商品、晚循環","side_b":"本次：四欄都不變","ruling":"新證據正反都有。NAND 份額升到 15%，但輝達 HBM4 分配美光最少，護城河仍判持平；沒有找到第二條成長曲線，跑道維持中等；合約價季增幅由 58–63% 收斂到 13–18%，循環位置維持晚段","evidence_level":"中","settle_metric":"季度合約價、HBM 份額","if_then":["若合約價季增率轉負→循環位置改為過熱頂部轉下行","若 HBM 份額連兩季升到 22% 以上→護城河方向改為擴大"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#1","cyclical_inventory_price_position#2"]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"多頭 30%、空頭 30%、最大回撤單點 -70%","side_b":"多頭 25%、空頭 35%、最大回撤區間 -70% 到 -50%","ruling":"共識成長超出內生上限，空頭機率至少 30%，再加 5 個百分點反映峰值毛利；回撤改用區間取代單點，下緣不變","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","side_b":"DRAM 合約價季減後連 2 季止跌，且公司財測毛利率止跌（循環回到早段），屆時重跑研究，首倉上限 3%；觸發前不追、已持有不加碼","ruling":"舊門檻的價格錨已被股價觸及（904.9 低於 946），但 FY2026 已成實績，分母換成 FY2027 後，5 倍本益比是峰值盈餘下的假便宜，價格錨失效。真正的約束是循環位置，所以改用事件錨；P/B 事實表未涵蓋，拿掉","evidence_level":"中","settle_metric":"TrendForce 合約價、美光財測毛利率","if_then":["若合約價季減後連兩季止跌→重跑研究，確認後首倉 ≤3%","若合約價持續季增而股價續跌→不追，不加碼"],"evidence_refs":["cyclical_inventory_price_position#2"]},{"axis":"停損指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有設停損指標（null）","side_b":"合約價季增 ≤0 連兩季→減碼至半倉；季毛利率低於 70%→減碼；CXMT 產能追平美光→減碼；合約價連兩季轉負且財測毛利率季減 ≥10pp→清倉","ruling":"前份只有警戒閾值，沒有綁定減碼與清倉動作，本次補上，門檻對應三個最大敏感度項","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 為 null（未設）","side_b":"Single Thing：DRAM 一般型合約價季增率轉負","ruling":"營收由合約價驅動，終端盈餘對合約價的敏感度高於份額、HBM 或成本任何一項，因此設為唯一致命點；發生時減碼至半倉","evidence_level":"高","settle_metric":"TrendForce 季度合約價","if_then":["若轉負→減碼至半倉；連兩季且財測毛利率季減 ≥10pp→清倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"axis":"供需持續期","cause":null,"prior_field":null,"side_a":"管理層：看不到供需平衡的時點，2028 年比 2027 更緊，FY27 出貨已承諾超過七成五（2026-09-30 COO）","side_b":"TrendForce：NAND 在 2027 下半年轉寬鬆、價格承壓；業界建設型資本支出加速，2028 下半年起新無塵室投產","ruling":"兩邊在時點上方向相反，屬不可調和。選第二邊作為 FY2029 以後的基準：DRAM 緊到 2028 年有多方佐證，但 NAND 先鬆；管理層也承認新增建廠支出主要是 2028 年後才投產","evidence_level":"中","settle_metric":"2027 下半年 NAND 合約價季增率","if_then":["若 TrendForce 公布 DRAM 合約價季增轉負→已持有者減碼至半倉，未持有不建倉","若 2027 下半年 NAND 合約價仍季增、且 2028 年配置談判已完成→維持持有、不加碼，首倉條件不變"],"evidence_refs":["end_markets#8","supply_demand_durability#3","cyclical_supply_discipline_capacity#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 約 5 倍本益比、淨現金 382.55 億美元、FY27 七成五出貨已承諾、SCA take-or-pay 到 2030 年、FQ1'27 指引高於共識","side_b":"毛利率財測約 86% 已是峰值，手機位元在下滑；SCA 最低承諾約 1,000 億美元分攤到 2030 年，每年約 200 多億，只占 FY2027 共識營收約 8%","ruling":"不買。真正的約束是循環位置偏晚，長約下限的金額只覆蓋峰值營收的一小塊，托不住價格下行","evidence_level":"中","settle_metric":"合約價季增率","if_then":["若合約價轉跌後連兩季止跌→重跑研究，首倉 ≤3%","若合約價持續季增而股價跌到 FY2028 共識 4 倍以下→仍不追，等合約價訊號"],"evidence_refs":["customer_second_source#0","channel_business_model_shift#1"]},{"axis":"HBM 份額證據","cause":null,"prior_field":null,"side_a":"Counterpoint 與市場彙整：美光 HBM 份額約 20%，輝達 HBM4 分配約兩成","side_b":"供應鏈估計輝達 Vera Rubin 的 HBM4 由 SK 海力士拿六到七成、三星二到三成，美光只拿剩下的；管理層 2026-09-30 也不再確認二成出頭的舊目標","ruling":"不可裁決，要等 2026Q4 的 HBM 份額公布。在那之前不把 HBM 份額當加分項，並列入停損指標","evidence_level":"低","settle_metric":"Counterpoint 2026Q4 HBM 份額","if_then":["若份額連兩季低於 15%→減碼至半倉","若份額 ≥20%→維持護城河判斷，不加碼"],"evidence_refs":["customer_second_source#1","end_markets#3","end_markets#4"]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"近 3 個月 FY1 共識上修 140.63%","side_b":"90 天前的 FY1 是 FY2026（73.37），現在的 FY1 是 FY2027（176.55），屬財年換季，不是真上修；同一財年兩次快照之間，FY1 +0.23%、FY2 -0.9%","ruling":"不把 140% 當成盈餘動能證據；近期共識已停止上修，FY2 開始下修","evidence_level":"高","settle_metric":"FY2 共識月度變化","if_then":["若 FY2 共識連兩個月下修合計超過 3%→停止任何加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FQ1'27 財報毛利率對照財測，以及 FY27 毛利續升的說法","type":"假設驗證","maps_to":"H1","metric":"季 GAAP 毛利率","threshold":"≥75%，且 FQ2 財測不低於 FQ1","action":"低於 75% 或財測季減→已持有者減碼至半倉；達標→維持，不加碼","source_freq":"美光季報／每季","date":"2026-12","evidence_refs":["capital_markets_pricing#2"]},{"n":2,"text":"DRAM 一般型合約價季增率轉負","type":"Single Thing","maps_to":"single_thing","metric":"DRAM 一般型合約價季增率","threshold":"≤0%","action":"減碼至半倉；連兩季轉負且財測毛利率季減 ≥10pp→清倉","source_freq":"TrendForce／每季","date":"2027-01","evidence_refs":["end_markets#8","cyclical_prior_downcycle_behavior#0"]},{"n":3,"text":"CXMT 的 DRAM 產能追平美光","type":"風險","maps_to":"R2","metric":"CXMT DRAM 月產能對美光差距","threshold":"差距 ≤0","action":"減碼至半倉","source_freq":"TrendForce／產業報導／每季","date":"2027-03","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","competitive_share_entrants#6"]},{"n":4,"text":"DRAM 買方反托拉斯集體訴訟獲集體認證","type":"風險","maps_to":"R4","metric":"集體認證裁定","threshold":"認證通過","action":"減碼至半倉","source_freq":"美光 10-Q／10-K 訴訟附註／每季","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"n":5,"text":"循環回到早段：合約價季減後止跌，財測毛利率止跌","type":"估值rearm","maps_to":"rearm","metric":"DRAM 合約價季增率＋公司財測毛利率","threshold":"合約價季減後連兩季止跌，且財測毛利率止跌","action":"重跑研究，確認循環回到早段後首倉 ≤3%","source_freq":"TrendForce＋美光季報／每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#3"]},{"n":6,"text":"合約價連兩季轉負，且財測毛利率大幅季減","type":"清倉","maps_to":"R1","metric":"合約價季增率與財測毛利率","threshold":"合約價連兩季 ≤0，且財測毛利率季減 ≥10pp","action":"清倉","source_freq":"TrendForce＋美光季報／每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"HBM 份額公布，裁定份額證據的衝突","type":"假設驗證","maps_to":"H3","metric":"美光 HBM 份額","threshold":"≥18%","action":"低於 15% 連兩季→減碼至半倉；≥18%→維持","source_freq":"Counterpoint／每季","date":"2027-02","evidence_refs":["customer_second_source#1"]},{"n":8,"text":"FQ1'27 財報後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"DRAM 一般型合約價季增率","bear_threshold":"≤0% 連 2 季","window":"2026Q4–2028Q4","source":"TrendForce 季度合約價報告","last_status":"ok"},{"metric":"美光季 GAAP 毛利率","bear_threshold":"低於 70%，或財測季減 ≥10pp","window":"FY2027–FY2028 各季","source":"美光季報與財測","last_status":"ok"},{"metric":"美光 HBM 份額","bear_threshold":"<15% 連 2 季","window":"2026Q4–2028","source":"Counterpoint 季度份額","last_status":"unknown"},{"metric":"CXMT DRAM 月產能對美光差距","bear_threshold":"差距 ≤0（追平）","window":"2026–2027","source":"TrendForce／Tom's Hardware 產能報導","last_status":"warning"},{"metric":"SCA 覆蓋的 DRAM 位元占比","bear_threshold":"<25%","window":"至 2030","source":"美光法說","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"DRAM 合約價季減後連 2 季止跌，且公司財測毛利率止跌（循環回到早段），屆時重跑研究，首倉上限 3%","exec_line":"未持有：不建倉，等循環回到早段。已持有：維持、不加碼；合約價季增轉負即減碼至半倉，連兩季轉負且財測毛利率季減 10pp 以上就清倉","holding_cap":"≤3%"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追價。等 DRAM 合約價季減後連兩季止跌、公司財測毛利率止跌，確認循環回到早段","qc48_result":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7a","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=93.18, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7a']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":["QC-50"]},"thesis":{"H":[{"id":"H1","text":"DRAM 供給緊張延續到 2028 年，FY2027 每季毛利率守在 75% 以上（FQ4'26 財測約 86%）","2y":"FY2027 四季毛利率都 ≥75%；DRAM 合約價季增率不轉負","5y":null,"10y":null,"threshold":"季毛利率 ≥75%；DRAM 一般型合約價季增率 ≥0","source":"美光季報與財測、TrendForce 季度合約價","drift_rule":"季毛利率比 86% 的財測水準連 2 季低 5pp 以上→削弱；連 3 季低 10pp 以上→反轉"},{"id":"H2","text":"長約讓本輪下行比過去淺：下一次景氣下行時，年度毛利率守在 35% 以上（FY2023 為 -9.11%、FY2024 為 22.35%）","2y":null,"5y":"下一個下行年度毛利率 ≥35%，且年度 FCF 為正","10y":null,"threshold":"下行年度毛利率 ≥35%；SCA 覆蓋 DRAM 位元 ≥35%","source":"美光 10-K、法說（2026-09-30 COO：SCA 約四分之三有價格框架）","drift_rule":"TTM 毛利率連 4 季低於門檻 5% 以上→削弱；連 6 季低於門檻 10% 以上→反轉"},{"id":"H3","text":"技術與 HBM 位置守住：HBM 份額約等於整體 DRAM 份額（約二成），1-delta 在 2027 下半年放量，領先中國至少兩個節點","2y":null,"5y":"HBM 份額 ≥18%、DRAM 份額 ≥18%，HBM4E／NVHBM 量產","10y":null,"threshold":"HBM 份額 ≥18%；DRAM 份額 ≥18%（2026Q1 為 19.9%）","source":"Counterpoint 季度份額、美光法說","drift_rule":"份額連 4 季偏離門檻 5% 以上→削弱；連 6 季偏離 10% 以上→反轉"}],"R":[{"id":"R1","text":"記憶體合約價漲幅收斂後轉跌，毛利率自財測約 86% 的峰值回落","h_ref":"H1","clock":"⚡","threshold":"DRAM 一般型合約價季增率 ≤0 連 2 季，或公司財測毛利率季減 ≥5pp","evidence_refs":["end_markets#8","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2"]},{"id":"R2","text":"中國 CXMT 與 YMTC 擴產，搶走商品 DRAM 與 NAND 的價格和中國客戶","h_ref":"H3","clock":"🔥","threshold":"CXMT DRAM 月產能 ≥ 美光，或美光 DRAM 份額連 2 季 <18%","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","competitive_share_entrants#6"]},{"id":"R3","text":"業界同步擴建無塵室，2028 下半年起新產能開出，下一輪下行跟過去一樣深","h_ref":"H2","clock":"🐢","threshold":"下一個下行年度毛利率 <35%，或年度 FCF 轉負","evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#3"]},{"id":"R4","text":"反托拉斯集體訴訟與 232 條款關稅，壓低價格上限或侵蝕毛利","h_ref":"H2","clock":"🔥","threshold":"DRAM 買方集體訴訟獲集體認證，或 232 條款對記憶體課稅且公司財測毛利率因此下修 ≥3pp","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R5","text":"台灣產能集中與地緣風險：銅鑼廠交割後集中度更高，員工有罷工風險，中國禁令先例還在","h_ref":"H1","clock":"🐢","threshold":"台灣廠區停工 ≥2 週，或中國禁令擴大到一般商用採購","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#4","geo_supply_chain#5"]},{"id":"R6","text":"漲價侵蝕終端需求：手機、PC、車用位元下滑，消費端先鬆動","h_ref":"H1","clock":"⚡","threshold":"手機與用戶端業務單位位元連 3 季季減，且營收轉為季減","evidence_refs":["end_markets#5","end_markets#6"]}],"single_thing":{"description":"DRAM 一般型合約價季增率轉負（以 TrendForce 季度合約價為準）","why_fatal":"營收由合約價驅動，80% 營益率幾乎都是價格。前次下行合約價自高點跌 57%、毛利率轉負，終端盈餘對合約價的敏感度高過份額、HBM 或成本任何一項","if_happens":"已持有者減碼至半倉；連兩季轉負且財測毛利率季減 ≥10pp 就清倉；未持有者不建倉，等止跌兩季","how_monitor":"TrendForce 每季合約價預估與實績；美光每季毛利率財測","probability":"35%（12 到 24 個月內）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":4.43,"peg_fy2":0.28,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":74.35,"FY2027E":176.55,"FY2028E":204.47,"FY2029E":203.33},"fy_end_month":8,"eps_basis":"共識為 Koyfin non-GAAP 稀釋 EPS（FY1＝FY2027，2027 年 8 月止）。FY2026A 由判斷日股價 904.9÷trailing 本益比 12.17 反推約 74.35，屬 GAAP 口徑，與共識口徑不完全一致；事實表沒有直接收錄 FY2026 實際 EPS"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"FQ1'27 財報與 FQ2 財測（毛利率是否續升）","impact":"高","watch":"毛利率 ≥75%，FQ2 財測不低於 FQ1"},{"date":"2027-01","date_precision":"month","type":"other","event":"TrendForce 公布 CQ1'27 DRAM 與 NAND 合約價","impact":"高","watch":"DRAM 季增率是否轉負"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"力積電銅鑼廠 18 億美元收購交割","impact":"低","watch":"交割進度與 2027 下半年 DRAM 出貨時程"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Idaho 新廠首批晶圓產出","impact":"中","watch":"首批產出後還要數季才有量；同期業界新無塵室開出的進度"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"HBM4E／NVHBM 量產與 1-delta 放量","impact":"中","watch":"輝達 HBM4E 分配份額"},{"date":null,"date_precision":null,"type":"regulatory","event":"DRAM 買方反托拉斯集體訴訟的集體認證裁定","impact":"中","watch":"認證通過即減碼至半倉"}]}
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
