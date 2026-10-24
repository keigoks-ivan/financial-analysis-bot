你是 DD 管線 v20 的判斷層閘（gate），標的 IBM（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝17103 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：IBM Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi1_operating_non_gaap`（q1_business）｜Operating（non-GAAP）稅前利益＝3295 百萬美元｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：IBM Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（公告於 2026-10-21））
- `f_kpi2_gaap`（q1_business）｜GAAP 稅前利益＝2497 百萬美元｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：IBM Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（公告於 2026-10-21））
- `f_peer_ibm_gross_margin_pct`（q2_moat）｜IBM 毛利率＝58.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ibm_operating_margin_pct`（q2_moat）｜IBM 營業利益率＝18.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi6_fy2026`（q1_business）｜管理層全年指引（FY2026）＝固定匯率營收成長 4%–5%（維持）；FCF 年增逾 $10 億（上調） text｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：IBM Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（公告於 2026-10-21））
- `f_peer_ibm_fcf_margin_pct`（q2_moat）｜IBM FCF 利潤率＝19.02 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_acn_gross_margin_pct`（q2_moat）｜ACN 毛利率＝32.01 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ACN.gross_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_acn_operating_margin_pct`（q2_moat）｜ACN 營業利益率＝15.75 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ACN.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_orcl_gross_margin_pct`（q2_moat）｜ORCL 毛利率＝63.96 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ORCL.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_orcl_operating_margin_pct`（q2_moat）｜ORCL 營業利益率＝34.23 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ORCL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_orcl_fcf_margin_pct`（q2_moat）｜ORCL FCF 利潤率＝-40.01 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ORCL.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_msft_gross_margin_pct`（q2_moat）｜MSFT 毛利率＝67.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msft_operating_margin_pct`（q2_moat）｜MSFT 營業利益率＝46.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hpe_gross_margin_pct`（q2_moat）｜HPE 毛利率＝36.73 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HPE.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_hpe_operating_margin_pct`（q2_moat）｜HPE 營業利益率＝7.84 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HPE.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝12.42 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.24 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝14.48 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_kpi5_sbc_operating`（q4_capital）｜SBC 占 operating 稅前利益＝16.2 %｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：SBC 535 ÷ operating 稅前利益 3,295（SBC 取自新聞稿）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-21））
- `f_kpi4_fcf`（q4_capital）｜自由現金流（FCF）＝3027 百萬美元｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：IBM Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（公告於 2026-10-21））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.658 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝253.56 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.42 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 12.42，分子＝快照價 253.56｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.73 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 12.33 → 12.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（12.42 → 12.42）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.08 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（13.23 → 13.24）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_rsi14`（q5_valuation）｜RSI(14)＝71.22｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝10.9 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 253.56 / W52 258.54 / W104 250.24 / W250 184.07 / W250 13週斜率 1.09%」

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：第三方分析（依 SEC 申報）：2026 年第二季基礎設施營收下滑 7.4%，IBM Z 大型主機營收年減 42.0%；全年軟體成長預期下修至 6%–8%（原 10% 以上）。頁面未提供份額數據。
  - 來源：sec-api.io insights：IBM stock after the Q2 2026 guidance cut（as_of 2026-10-12）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：IBM 2026 Q2 後下調全年財測（二手分析文章）
  - 來源：sec-api insights: IBM stock after the Q2 2026 guidance cut（as_of 2026-10-12）｜affects：thesis.R、triggers
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：IBM 10-Q（截至 2026-06-30）：z17 於 2025-06 推出、為史上最強的大型主機開局，但 Q2 2026 低於預期，主因 IBM Z 及相關軟體（主要為交易處理）短缺；Network World 報 z 主機營收該季年減 42%。
  - 來源：IBM Form 10-Q FY2026 Q2 / Network World（as_of 2026-07-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：2026-04-10 美國司法部與 IBM 就 False Claims Act 達成 1,710 萬美元和解，指控涉及不實證明遵守反歧視要求（非反壟斷案）。
  - 來源：Digital Policy Alert｜DOJ investigation into IBM over alleged false certification of compliance with anti-discrimination requirements（as_of 2026-04-10）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：IBM CEO Krishna 表示伊朗戰爭與地緣不確定性開始影響展望，影響主要經由客戶端
  - 來源：idnfinancials: IBM CEO Arvind Krishna: Iran war starts to weigh on outlook（as_of 2026-04-20）｜affects：decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：IBM Q2 2026 Z 大型主機營收年減 42%，IBM 稱為 z17 週期尾段及客戶把六月底資本支出轉向供給吃緊的伺服器／儲存／記憶體；全年營收成長指引由 >5% 下修至 4–5%；管理層稱 z17 為史上最佳換機週期、無客戶離開大型主機的證據
  - 來源：AI Weekly, IBM Cuts 2026 Outlook as Q2 Mainframe Revenue Falls 42%（as_of 2026-07-23）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：IBM 10-K FY2025 風險因素：若未能及時因應顛覆性技術與新商業模式，客戶對其產品或服務的需求可能下降、成本可能上升
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：報導稱 Anthropic 宣布 Claude Code 可用於含 COBOL 的程式現代化後，IBM 股價單日重挫（約 13%，單一來源）
  - 來源：BusinessDay, Anthropic AI tool sparks plunge in IBM stock（as_of 2026-02-24）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：7月中下旬多家券商下調IBM目標價：Citigroup 255（原375）、JPMorgan 250（原291）、Stifel 235（原290）、Barclays 288（原350）、Jefferies 260（原320）；MarketScreener顯示平均目標價約244、25位分析師覆蓋，多數維持評級。
  - 來源：MarketScreener, Evolution of the Average Target: IBM（as_of 2026-07-21）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：HSBC於7月16日給IBM目標價175、評級reduce；MarketBeat七月底平均目標價265.40、共識Moderate Buy（各聚合站數字不一致）。
  - 來源：MarketBeat, FY2026 earnings estimate for IBM issued by Erste Group Bank（as_of 2026-07-29）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026營收17.2B（年增1%）、調整後EPS 2.93，低於共識（Benzinga：EPS預期3.02、營收預期17.86B）；全年指引原為固定匯率營收成長5%以上、FCF較去年增加約10億美元，7月14日初步數字顯示該指引仍有效，7月22日8-K標題為更新全年預期但摘要未含數字。
  - 來源：MarketBeat, IBM updates Q2 2026 earnings guidance (2026-07-14); Benzinga IBM earnings forecasts; SEC 8-K 2026-07-22（as_of 2026-07-22）｜affects：thesis.R、valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Erste Group於7月27日將IBM FY2026 EPS估計由12.39微降至12.36（共識12.34），FY2027為13.14；Bank of America先前因Confluent併購稀釋與諮詢趨勢轉弱，將2026 EPS由12.20降至11.98。
  - 來源：MarketBeat, FY2026 earnings estimate for IBM issued by Erste Group Bank（as_of 2026-07-29）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：律所 Bleichmar Fonti & Auld 因 2026-07-14 Q2 財報後股價下跌，調查 IBM 是否就大型交易簽約速度誤導投資人；屬調查，未見已提起集體訴訟。
  - 來源：Bleichmar Fonti & Auld｜IBM class action lawsuit investigation page（as_of 2026-07-15）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Bleichmar Fonti & Auld 於 2026-07-14 Q2 財報後股價下跌，調查 IBM 是否誤導投資人大型交易成交速度；僅為調查。另有 2023 年起訴於 SDNY 的主機營收重分類集體訴訟，搜尋結果未載結案狀態。
  - 來源：Bleichmar Fonti & Auld｜IBM class action lawsuit page（as_of 2026-07-15）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":433.4,"bear_5y_price":179.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":24.9,"ev5y_pct":20.2,"irr_base_pct":4.6,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":12.42,"pe":20.42,"basis":"FY1（FY2026E）共識 non-GAAP 營業 EPS；終端倍數同為終端年當年 FY1 口徑"},"eps":{"bull":[13.4,14.9,16.4,18.0,19.7],"base":[13.24,14.48,15.5,16.55,17.6],"bear":[12.6,12.3,12.1,12.4,12.8]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.658,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### IBM_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Arvind Krishna｜guidance：全年營收成長預期下修為 4% 至 5%，自由現金流仍預期增加約 10 億美元（原話："revenue growth for the full year in a range of 4% to 5%"）
- 2026-07-22｜James Kavanaugh｜guidance：CFO 稱營收區間低端為基本情境（原話："We believe the low end of the revenue range appropriately"）
- 2026-07-22｜James Kavanaugh｜guidance：軟體全年成長預期下修為 6% 至 8%，低端假設近期支出型態在下半年持續（原話："the low end of the software range assumes that recent"）
- 2026-07-22｜James Kavanaugh｜guidance：基礎設施全年預期上調為低個位數成長（90 天前為下降低至中個位數）（原話："we now expect Infrastructure to grow"）
- 2026-07-22｜James Kavanaugh｜guidance：第三季固定匯率營收成長與全年一致，匯率為 1.5 個百分點逆風，營業稅前利潤率與第二季相近（原話："we now expect currency to be a 1.5 point headwind to revenue"）
- 2026-07-22｜James Kavanaugh｜guidance：下半年交易處理軟體（TP）預期下降低至中個位數，管理層把它放在 2027 年才作為成長動能（原話："we've got TP down low single digits"）
- 2026-07-22｜James Kavanaugh｜margin：全年營業稅前利潤率預期擴張 100 個基點，生產力行動抵銷營收相關逆風（原話："we now expect to deliver 100 basis points of operating"）
- 2026-07-22｜James Kavanaugh｜margin：第二季營業毛利率下降 70 個基點，原因為營收落差與組合；營業稅前利潤率仍擴張 30 個基點（原話："Operating gross profit margins were down 70 basis points"）
- 2026-07-22｜James Kavanaugh｜margin：分部利潤率：顧問 +160bp、軟體 +110bp、基礎設施 −150bp（IBM Z 組合逆風）（原話："segment profit margin declined 150 basis points"）
- 2026-07-22｜James Kavanaugh｜margin：數字口徑：軟體約 80% 為經常性收入，ARR 246 億美元、年增 8%；其餘 20% 為交易型，與大型主機授權協議（ELA）綁定（原話："other 20% of software revenue is transactional in nature"）
- 2026-07-22｜James Kavanaugh｜risk：數字口徑：第二季軟體落差來自大客戶資本支出型交易延後；TP 下降 9%、資料 +18%、自動化 +3%（原話："processing revenue declining 9%, while data grew 18%"）
- 2026-07-22｜James Kavanaugh｜risk：六月最後幾週客戶把預算轉向伺服器、儲存與記憶體採購，數十件大單未如期成交（原話："tens of large deals failed to close on the time lines"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 表示約三分之一遞延交易已在三週內成交，並判斷為遞延而非流失，但自稱尚非完整證據（原話："not yet full evidence, but a good indication"）
- 2026-07-22｜James Kavanaugh｜risk：CFO 對遞延交易成交比例的說法（約 40%）與 CEO（約 1/3）略有不同；高端假設全數成交（原話："Our high-end range says we close all of them"）
- 2026-07-22｜Arvind Krishna｜customer：CEO 解釋客戶因替代採購價格季增約 30% 而挪移預算，IBM 七月未漲價（原話："held our price so far in the month of July"）
- 2026-07-22｜Arvind Krishna｜product：z17 週期至今約為 z16 的 130%（program-to-program），管理層稱沒有客戶離開主機證據；第二季主機營收年減 42%，因去年同期上市基期高（原話："z17 remains at nearly 130% program-to-program"）
- 2026-07-22｜James Kavanaugh｜product：主機年減 42%，管理層歸因於去年上市季成長 70% 的基期（原話："Mainframe overall, yes, down 42%. It's off a 70% growth"）
- 2026-07-22｜Arvind Krishna｜product：分散式基礎設施單季成長 37%，創紀錄（原話："best quarter of revenue growth on record, growing 37%"）
- 2026-07-22｜James Kavanaugh｜product：Red Hat 成長較上季加速 1 點至 11%，RHEL 仍受硬體供應受限影響（原話："Red Hat growth accelerated 1 point sequentially to 11%"）
- 2026-07-22｜James Kavanaugh｜product：顧問簽約成長 6%，生成式 AI 約占簽約 50%、占在手訂單超過 30%（原話："Generative AI represented about 50% of our signings"）
- 2026-07-22｜Arvind Krishna｜product：Lightwell 開源安全修補訂閱，每年 100 萬美元；管理層稱 TAM 為數十億美元，目標數百家客戶（原話："Clients can subscribe to Lightwell for $1 million per year"）
- 2026-07-22｜Arvind Krishna｜capital_allocation：量子運算：宣布五年內投資逾 100 億美元（原話："invest more than $10 billion in Quantum"）
- 2026-07-22｜James Kavanaugh｜capital_allocation：上半年自由現金流 48 億美元，與去年持平；為因應供應吃緊提前備貨，庫存年增約 6 億美元，下半年預期轉為順風（原話："Our inventory exiting the first half is up $600 million"）
- 2026-07-22｜James Kavanaugh｜capital_allocation：季末現金 82 億美元，債務 620 億美元（含融資業務 130 億美元），上半年股利支出 32 億美元（原話："We returned $3.2 billion to shareholders"）
- 2026-07-22｜Arvind Krishna｜commitment：維持全年自由現金流增加約 10 億美元的承諾（原話："expect to grow free cash flow by about $1 billion"）
- 2026-07-22｜Arvind Krishna｜commitment：CEO 重申軟體長期雙位數成長承諾不變（原話："we are not going to back off from our commitment of long-"）
- 2026-07-22｜James Kavanaugh｜commitment：CFO 稱下半年自由現金流將不低於 10 億美元增幅，且自由現金流利潤率創新高（原話："maintain growing free cash flow, at least $1 billion"）
- 2026-07-22｜Arvind Krishna｜competition：敘事：價值將轉向編排與資料層，IBM 強調中立與企業級控制（原話："shift towards the orchestration and data layers"）
- 2026-07-22｜Arvind Krishna｜customer：調整市場進入模式，擴大涵蓋數千家額外客戶，並增加前線部署工程師（原話："expand coverage across thousands of additional clients"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 承認本季在執行面未達標（原話："That is where we fell short in the second quarter"）
- 2026-07-22｜Arvind Krishna｜risk：CEO 說軟體落差約 4–5 億美元，TP 約占大額資本支出型交易的 50–60%，資料軟體也受波及（原話："$500 million of the miss was in software overall"）

### 問答異常語氣（迴避／改口／保留）
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Ben Reitzes 問 TP（−9%）與主機（−42%）如何改善，以及 4–5% 指引是否可信｜答法：CFO 未給 TP 恢復的時間點，改談主機基礎與 MIPS 容量，並稱 TP 下半年仍下降低至中個位數、改列為 2027 年成長動能
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Fatima Boolani 追問 85% 穩定或成長的 MIPS 容量之外，另外 15% 發生什麼事｜答法：CEO 只回答遞延交易成交原因，沒有回答另外 15% 的去向
- IBM_Q2_2026_Earnings_Call_20260722.md｜問：Erik Woodring 問為何 IBM 自家有機資料軟體（約年減中個位數）表現落後非 TP 軟體｜答法：CEO 未確認或否認有機資料的下滑數字，以大額資本支出交易受影響和預期未來 12 個月表現良好回應

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | not_applicable | 1 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 1 | 3 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：IBM largest customer concentration second source OR in-house 2026；IBM 10-K no single customer 10% of revenue 2025

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260723","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"軟體段（Red Hat+HashiCorp+Confluent+watsonx）恢復並維持 ~雙位數成長，交易型滑單為遞延非破壞","columns":{"2Y 驗證點":"FY27 軟體 ARR ≥ $28B；交易型軟體回正","5Y 驗證點":"FY30 軟體占公司營收 >50%；80/20 經常性占比升至 >85%","10Y 驗證點":"FY35 軟體 ARR >$45B、經常性 >90%","具體數字門檻 / Sourced Floor":"Sourced：管理層 FY26 軟體 guide 下修至 6–8%（原 10%，Q2'26 逐字稿）；ARR $24.6B +8%（Q1 為 +10%，已放緩）；80% 經常性 +8% 「approaching 10%」狀態：削弱中（guide 破 10% 底、有機 flat）","漂移觸發":"連兩季 ARR YoY"}},{"id":"H2","text":"Consulting 不因 AI 結構性崩塌（Claude Code 衝擊是逆風非 thesis-killer）","columns":{"2Y 驗證點":"Consulting signings YoY ≥ +1%；GenAI signings 比例 ≥ 40%","5Y 驗證點":"FY30 Consulting 段營收 ≥ $22B；backlog GenAI >40%","10Y 驗證點":"Consulting 段轉型為 AI 部署主導","具體數字門檻 / Sourced Floor":"Sourced：Q2'26 signings +6%（第二個連續成長季）、GenAI ~50% 之 signings、>30% backlog、段利潤率 +160bps（逐字稿）狀態：holding／略強化（signings 正、margin 擴張）","漂移觸發":"連兩季 signings YoY ≤ 0% → 削弱；單一 top-100 client 公開 migrate 案例 → 立即降級 trap 🔴"}},{"id":"H3","text":"估值自崩盤位置修復（FCF 續增 + 軟體回升驅動 re-rate）","columns":{"2Y 驗證點":"FY27 Fwd PE 回 ~17–18x；股價 $240+","5Y 驗證點":"FY30 Fwd PE 穩定 16–19x；股價 $280+（5Y target）","10Y 驗證點":"與 ACN/成熟軟體中位收斂","具體數字門檻 / Sourced Floor":"Sourced：現 Fwd PE 16.9x（FY26 non-GAAP $12.16 基）；EV/EBITDA 15.1x vs 5Y 中位 17.1x（近 5Y 低）；但非同業折價——HSBC 指 IBM 仍在 CY27e 22x（同業中位 16.9x）之溢價（GuruFocus/HSBC）狀態：反轉（市場 de-rate 而非 re-rate）","漂移觸發":"連四季 Fwd PE 停在"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI capex 對企業軟體錢包的排擠從 20% 交易型軟體外溢至更廣（記憶體/HBM 超級循環延續至 2027–28，逼單機制不退）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（2–3 年結構背景）","監測指標":"交易型軟體 TPP YoY；80% 經常性軟體 YoY 是否也開始鬆動","警戒閾值":"經常性軟體連兩季跌破 +6% → 排擠外溢確認、H1 反轉"}},{"id":"R2","text":"Claude Code／Cursor 等 AI coding 工具侵蝕 Consulting COBOL 現代化與 IBM Z 綁定","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"Consulting signings YoY；單一 top-100 client 公開 migrate off mainframe","警戒閾值":"signings 連兩季 ≤0% → 觸發；公開 migrate 案例 → 立即 trap 🔴（並見 §3.F）"}},{"id":"R3","text":"有機軟體長期 flat，成長依賴越來越貴的併購（出價紀律惡化 + 整合失利）","columns":{"對應假設":"H1／H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"剔除併購後有機軟體成長率；HashiCorp/Confluent 整合 churn 與 ARR","警戒閾值":"剔併購有機成長連四季 ≤ +3% → 品質降級、re-rate thesis 破"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","irr_base_pct":6.7,"ev5y_pct":30.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.0,"ev5y_pct":30.5,"irr_base_pct":6.7,"max_dd_pct":-35.0,"bull_5y_price":370.0,"bear_5y_price":161.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","price_at_dd":205.77,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"IBM","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"International Business Machines"},"oneliner":"第三季軟體回到 9%、交易處理反彈 10%，延遲大單是遞延不是流失；但股價三個月漲兩成三、FY1 本益比 20 倍已反映復原，基本情境年化約 7%，等回檔或 2027 財測再動手","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/scenario.json","answers":{"q1_business":{"verdict":"IBM 賺的是大企業關鍵系統的錢：大型主機與其上的交易處理軟體（多年期企業授權綁定）、Red Hat 混合雲訂閱、加上顧問；錢卡在大型主機裝機容量這一節點，每 1 美元主機硬體帶動 3–5 美元軟體","reasoning":"最新一季（Q3 FY2026）營收 $171.03 億，年增 5%（固定匯率 6%）；分部：軟體 $78 億（固定匯率 +9%，其中 Red Hat 與混合雲 +11%、資料 +19%、交易處理 +9%～10%）、顧問 $53 億（固定匯率 +2%）、基礎設施 $37 億（固定匯率 +5%，其中 IBM Z −20%、分散式基礎設施 +32%）。三段皆超過營收 10%。營業（non-GAAP）稅前利益 $32.95 億、GAAP 稅前利益 $24.97 億；TTM 毛利率 58.1%、營業利益率 18.39%。軟體約 80% 為經常性收入（高價值 ARR $249 億、年增 8%），其餘 20% 為交易型、與主機企業授權綁定，第二季失速、第三季反彈的波動就出在這 20%。客戶不集中：2023–2025 年無客戶占營收 10% 以上，約六成營收來自美國以外。全年指引：固定匯率營收成長 4%–5% 維持、FCF 年增上調至逾 $10 億。產業態勢屬雙向拉鋸：競爭面，AI 編碼工具壓低主機程式移轉成本（惡化）；結構面，主權 AI 與本地部署需求、記憶體與伺服器漲價讓主機總持有成本優勢擴大（轉好）。產業時鐘在擴張期：企業 AI 支出擴大，第三季三個分部同時加速。供需持久性：軟體經常性需求屬結構性持久；主機硬體與交易處理屬週期性，z17 週期已過高峰，2027 年將回到正常化。單點依賴：主機是利潤核心，這是護城河證據也是集中風險。","fact_refs":["f_kpi0_gaap","f_kpi1_operating_non_gaap","f_kpi2_gaap","f_peer_ibm_gross_margin_pct","f_peer_ibm_operating_margin_pct","f_kpi6_fy2026"],"verdict_values":{"revenue_quality":"軟體約八成為經常性（ARR $249 億、年增 8%），另兩成交易型綁主機企業授權、季度波動大；顧問與基礎設施成長低、週期性高","unit_econ_note":"每 1 美元主機帶 3–5 美元軟體（CFO，Q3 FY2026 法說）；z17 出貨 MIPS 增逾 100%、裝機 MIPS 增約 18%，是交易處理未來的變現基數","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"成熟現金流公司，營收 4–5% 成長，靠生產力擴利潤率與併購推軟體成長，股東回饋以股息為主"},"industry":{"clock_phase":"II","sd_verdict_source":"軟體經常性需求結構性持久；主機與交易處理屬週期性將反轉（z17 週期尾段），依據為 Q2 FY2026 Z 營收年減 42%、Q3 仍 −20%，以及管理層自述 z16 週期上市年持平、之後兩年才加速","bargaining":{"up":"對上游：記憶體、伺服器與儲存元件漲價時，客戶預算被硬體吸走（Q2 FY2026 實例），IBM 七月選擇不漲價","down":"對客戶：多年期企業授權綁定、轉換成本高、無單一客戶占營收 10% 以上；定價權存在但保守使用","geo":"業務遍及 175 國以上、約六成營收來自美國以外，貿易關係惡化列為風險因素但無量化揭露"},"profit_pool_dir":"管理層稱價值往 AI 編排與資料層移動；短期內硬體與記憶體端分走企業預算","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池占比；IBM 的成長來自既有客戶內擴容與併購，不是滲透率故事，改以分部成長與裝機容量判斷"}}}},"q2_moat":{"verdict":"護城河持平：主機加企業授權的轉換成本仍在、軟體利潤率在擴張，但 AI 編碼工具壓低移轉成本、主機硬體仍在下滑，兩邊相抵","reasoning":"機制：主機承載多數大型金融與零售核心交易，客戶以多年期企業授權把交易處理、資料與自動化軟體綁在主機上，搬家要重寫核心系統與重新驗證，轉換成本高；Red Hat OpenShift 以混合雲中立標準延伸到主機以外。方向證據：執行面，Q3 FY2026 軟體分部利潤率 +210bp、基礎設施 +120bp，約 85% 裝機容量的客戶維持或增加容量，z17 週期至今比前代多逾 $10 億營收（擴大）；定價面，七月未漲價、AI 編碼工具讓 COBOL 現代化變便宜、Q3 Z 營收仍 −20%（縮減）。同業對照（事實表只有利潤率、無 ROIC）：IBM TTM 毛利率 58.1%、營業利益率 18.39%，高於 ACN（32.01%／15.75%）與 HPE（36.73%／7.84%），低於 MSFT（67.94%／46.78%）與 ORCL（63.96%／34.23%）；位置在服務商與純軟體之間，與其混合結構一致。執行力 7、定價權 7，合併 7 分。","fact_refs":["f_peer_ibm_gross_margin_pct","f_peer_ibm_operating_margin_pct","f_peer_ibm_fcf_margin_pct","f_peer_acn_gross_margin_pct","f_peer_acn_operating_margin_pct","f_peer_orcl_gross_margin_pct","f_peer_orcl_operating_margin_pct","f_peer_orcl_fcf_margin_pct","f_peer_msft_gross_margin_pct","f_peer_msft_operating_margin_pct","f_peer_hpe_gross_margin_pct","f_peer_hpe_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"主機核心交易系統的轉換成本＋多年期企業授權綁定交易處理與資料軟體；Red Hat 混合雲中立標準","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 FY2026 軟體分部利潤率 +210bp、85% 裝機容量客戶維持或成長、z17 週期比前代多逾 $10 億；定價面縮減：七月未漲價、AI 編碼工具降低移轉成本、Z 營收 Q3 仍 −20%；兩者相抵為穩定","competitor_notes":[{"name":"ACN","strategy_note":"純服務商、毛利結構遠低於 IBM，是顧問段 AI 部署的正面對手；IBM 顧問 Q3 僅 +2%，未拉開差距"},{"name":"ORCL","strategy_note":"資料庫加雲端重資本擴張，近一年自由現金流轉負，路線與 IBM 輕資本混合雲相反，競爭點在大型企業資料庫與核心系統"},{"name":"MSFT","strategy_note":"利潤率遠高於 IBM，是 AI 平台與雲的主要對手；IBM 以混合雲中立、本地部署與主權 AI 區隔"},{"name":"HPE","strategy_note":"混合基礎設施對手、利潤率明顯較低；IBM 稱儲存與 Power 本季取得份額，但事實表未涵蓋份額數字"}],"peer_na_reason":"事實表只有同業利潤率、無投入資本與 ROIC，改以毛利率與營業利益率對照","threats":[{"level":"🔴","text":"AI 編碼工具（如 Claude Code）降低 COBOL 現代化成本，讓主機客戶有能力把核心系統移出，侵蝕交易處理與相關顧問","p":30,"evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"level":"🔴","text":"記憶體、伺服器漲價把企業預算從軟體挪到硬體，交易型軟體大單延遲（Q2 FY2026 實例）","p":25,"evidence_refs":["supply_demand_durability#0","end_markets#1"]},{"level":"🟡","text":"超大型雲端與服務商（MSFT、ACN 等）在 AI 平台與 AI 轉型顧問點對點競爭","p":20,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉（定性判斷：併購商譽與融資業務資產厚；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"主機承載核心交易，使用者（營運）、決策者（CIO）、付款者（銀行與零售）三角色都成立，屬需要而非想要；Q3 FY2026 約 85% 裝機容量客戶維持或增加容量，五年裝機 MIPS 翻倍"},{"item":"決策層級","level":"🟡","text":"替代決策發生在單一核心應用的遷移專案，代價是重寫、重新驗證與停機風險，多年期企業授權拉長決策週期；但 AI 編碼工具正壓低重寫成本，2026-02 相關發布當天股價重挫約 13%，替代門檻在下降"},{"item":"價值鏈分配","level":"🟡","text":"Q2 FY2026 客戶把預算轉去搶購漲價約 30% 的伺服器、儲存與記憶體，硬體供應端在當下分走較多價值；IBM 以每 1 美元主機帶 3–5 美元軟體維持自己的份額，但互補品漲價時沒有轉嫁"},{"item":"社會容忍度","level":"🟢","text":"未見針對 IBM 的新反壟斷案或拆分調查，管理層稱監管對併購更友善；唯一監管事件為 2026-04 以 $1,710 萬和解的反歧視證明案，已結案；依賴的不是監管授權"}],"roiic":"事實表未涵蓋投入資本與歷次收購金額，無法算增量報酬；可追溯的部分：營業利益由 FY2023 約 $94 億（$618.6 億 × 15.17%）增至 FY2025 約 $125 億（$675.4 億 × 18.5%），兩年增約 $31 億，對應的新增投入未揭露","reinvest_rate":"2026 年 Confluent 約 $110 億全現金收購，接近一整年稅後營業利益（約 $106 億＝$125 億 × (1 − 約 15% 稅率)），屬一次性高峰；常態再投資率事實表未涵蓋","endo_ceiling":5.0,"formula_note":"無法以增量 ROIC × 再投資率正式推導；以管理層長期營收成長目標逾 5%（2025 投資人日）與 Q3 軟體有機成長約 4 點作為內生上界代理，利潤率擴張與併購另列為缺口來源"}}}},"q3_growth":{"verdict":"五年後跑道中等：既有主機與軟體客戶內持續擴容，但五年後沒有已證實的第二條成長曲線","reasoning":"成長來源：量為主（裝機 MIPS 擴大、OpenShift ARR $24 億年增逾 30%），價格次之（容量擴大後的交易處理變現），併購約占軟體成長一半（Q3 軟體 9% 中有機逾 4 點，其餘多為 Confluent）；前九月回饋全為股息，沒有回購助攻。三年共識 EPS：FY2026 $12.42 → FY2027 $13.24 → FY2028 $14.48，FY2026 起兩年年增約 8.0%；若以 FY2025 GAAP 稀釋 EPS $11.17 為基期約 9.0%，但口徑不同會高估。內生上界約 5%（代理值，見護城河段），缺口約 3pp 歸因於利潤率擴張：全年營業稅前利潤率指引 +100bp、累計生產力逾 $55 億，Q3 營業稅前利潤率 +70bp；此缺口可歸因，不屬於依賴重估。成長是否持久看三件事：交易處理能否複製 z16 週期（上市年持平、次年中個位數、第三年高個位數）、Red Hat 訂單高十幾能否轉成營收、顧問能否從低個位數加速。衰退訊號：亮 1 個（替代技術壓縮可用市場）。Runway 5–9 年：成熟市場不以滲透率衡量；量子（Quantum Day 2026-12-10）仍屬早期，不算已證實的下一條曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_fy2026","f_kpi5_sbc_operating","f_kpi0_gaap"],"verdict_values":{"growth":{"driver_mix":"量（裝機容量、OpenShift 採用）為主、價格（容量變現）次之、併購約占軟體成長一半、無回購；EPS 另加利潤率擴張約 3pp","runway_years":"5~9","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 5%：以管理層長期營收成長目標逾 5% 與軟體有機約 4 點代理；共識 EPS 年增約 8% 超出約 3pp，歸因利潤率擴張（每年營業稅前利潤率約 +100bp）","segments":[{"item":"軟體（Q3 FY2026）","value":"$78 億，固定匯率 +9%；Red Hat +11%、資料 +20%、交易處理 +10%，全年指引約 7%–8%"},{"item":"顧問（Q3 FY2026）","value":"$53 億，固定匯率 +2%；AI 占顧問營收約 30%、在手訂單 35%，全年指引低至中個位數"},{"item":"基礎設施（Q3 FY2026）","value":"$37 億，固定匯率 +5%；分散式基礎設施 +32%、IBM Z −20%，全年指引低個位數"},{"item":"利潤結構","value":"軟體分部利潤率 +210bp、基礎設施 +120bp、顧問小幅下滑（把生產力收益再投資於數位資產）"}],"decay_signals":["替代技術壓縮可用市場：亮（AI 編碼工具降低主機移轉成本，2026-02 單日重挫約 13%）","毛利率連 2 季年減：未亮（毛利率 FY2022 54.0% 起逐年升至 FY2025 58.19%，TTM 58.1%）","EPS 成長高於營收成長逾 5pp：未亮（約 8% 對 4–5%，差 3–4pp）","SBC 占營收逾 5% 且上升：未亮（Q3 SBC $5.35 億 ÷ 營收 $171.03 億約 3.1%）","核心市占縮減：資料不足（事實表未涵蓋份額）","產業估值倍數近 3 年下移：資料不足（事實表未涵蓋同業倍數歷史）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中段：現金流穩、股息可靠，但沒有回購、成長靠併購加債，增量報酬無法驗證","reasoning":"現金產出：Q3 FCF $30.27 億，前九月約 $80 億、年增約 8%，FCF 利潤率為歷史最高；全年 FCF 年增指引上調至逾 $10 億。TTM FCF 利潤率 19.02%，對照 FY2025 淨利率約 15.7%（$105.93 億 ÷ $675.36 億），FCF 對淨利轉換約 1.2 倍。SBC 占營業稅前利益 16.2%（約占營收 3.1%）。現金去向：股息前九月 $48 億；併購 Confluent 約 $110 億全現金；回購法說未提、事實表未涵蓋；資本支出上升（CFO 說法，金額未揭露）。負債：Q3 末債務 $638 億（含融資業務 $127 億）、現金 $111 億；6 月底淨負債 $538 億，較 2025 年底 $468 億增加，主因 Confluent；評等 S&P A-、Moody's A3、Fitch A- 維持。三項評分：併購增量報酬無法驗證、回購不適用、SBC 淨稀釋率因股數變動未涵蓋而無法計算。","fact_refs":["f_kpi4_fcf","f_kpi5_sbc_operating","f_peer_ibm_fcf_margin_pct","f_kpi6_fy2026","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"HashiCorp、Confluent 等收購的已實現增量報酬事實表未涵蓋；Confluent 2026 年才併入，資料段 +20% 有貢獻但無利潤數字"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"前九月股東回饋 $48 億全為股息，法說未提回購"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 占營業稅前利益 16.2%（Q3 FY2026）；股數變動事實表未涵蓋，淨稀釋率無法計算"}]},"governance":{"capital_returns":[{"item":"股息","value":"前九月 $48 億；TTM 殖利率約 2.66%"},{"item":"併購","value":"Confluent 約 $110 億全現金（2026 年完成）；HRL Laboratories 條件未揭露"},{"item":"回購","value":"法說未提，事實表未涵蓋"},{"item":"負債","value":"Q3 末債務 $638 億（含融資業務 $127 億）、現金 $111 億；6 月底淨負債 $538 億（2025 年底 $468 億）"}]}}},"q5_valuation":{"verdict":"現價要求 IBM 在 20 倍以上的本益比下維持約 8% 的 EPS 成長五年；我信成長，不信倍數能守住，估值偏貴","reasoning":"現價 $253.56，FY1（FY2026E）共識 EPS $12.42，本益比 20.42 倍；FY2 $13.24 對應 19.15 倍。PEG＝20.42 ÷ 8.0%（FY2026→FY2028 共識年增）約 2.6，高於 2。共識近三個月只上修 0.73%，但股價自前份判斷（$205.77）上漲約 23%，等於倍數由約 16.9 倍重估到 20.4 倍，漲幅幾乎全來自倍數。股息殖利率約 2.66%。基本情境：FY2031 EPS $17.60 × 18 倍＝$316.8，較現價 +24.9%，加股息年化約 7%，落在弱區。短期參考：七月（Q3 財報前）賣方平均目標價約 $244，較現價約 −3.8%，但該數字未反映 Q3，參考性有限。五年本益比百分位：事實表未涵蓋估值歷史高低點，無法計算。同業倍數：事實表未涵蓋。分母採 non-GAAP 營業 EPS，與 GAAP 稅前差約每季 $8 億（$32.95 億對 $24.97 億，多為併購攤銷），屬一貫口徑，不視為爭點。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_dividend_yield_ttm","f_kpi1_operating_non_gaap","f_kpi2_gaap"],"verdict_values":{"valuation":{"basis":"FY1 non-GAAP 營業 EPS 本益比＋PEG","tier":"成熟軟體與 IT 服務混合","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比，無法做同層級倍數對照"},"fwd_pe":20.42,"peg":2.56,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 本益比 20.42 倍、PEG 約 2.6（20.42 ÷ 共識 EPS 兩年年增 8.0%）；基本情境五年年化約 7% 低於 8%；三個月股價 +23% 對共識 EPS +0.7%，重估已發生；五年百分位事實表未涵蓋 → 偏貴","upside_short_pct":-3.8,"upside_mid_pct":24.9,"denominator_disputed":false,"denominator_note":"non-GAAP 與 GAAP 稅前差約每季 $8 億，主要為併購攤銷等，口徑一貫，不構成爭點"}}},"q6_how_wrong":{"verdict":"價值陷阱風險中等：最可能看錯的是 AI 編碼工具讓主機客戶真的搬走，其次是倍數回落吃掉 EPS 成長","reasoning":"三個方向的反證見反證紀錄：論點失敗（AI 工具降低移轉成本、客戶預算被硬體擠壓）、股東經濟變差（高價併購與負債上升、無回購）、價格已反映太多（20.4 倍、RSI 71.22、26 週 +10.9%）。衰退訊號亮 1 個，週線均線排列過但長均線走平。","fact_refs":["f_rsi14","f_week26_return_pct","f_ma_state","f_fwd_pe_latest"],"verdict_values":{"trap":{"verdict":"🟡","label":"成熟現金流公司復原中，主機替代風險未解、估值已回到溢價"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":12.42,"pe":20.42,"basis":"FY1（FY2026E）共識 non-GAAP 營業 EPS；終端倍數同為終端年當年 FY1 口徑"},"eps":{"bull":[13.4,14.9,16.4,18.0,19.7],"base":[13.24,14.48,15.5,16.55,17.6],"bear":[12.6,12.3,12.1,12.4,12.8]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.66,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-40,"hi":-25,"basis":"三個依據：①三個月前股價 $205.77，回到該處即約 −19%；②2026-02 AI 編碼工具發布當天單日重挫約 13%，顯示主機替代題材可快速重定價；③Bear 倍數 14 倍 × FY1 EPS 12.42 約 $174（約 −31%），極端情況 12 倍 × 12.4 約 $149（約 −41%）。取 −25% 至 −40%","trigger_time":null},"basis":{"bull":"交易處理複製 z16 週期（2027 中個位數、2028 高個位數）、Red Hat 高十幾訂單轉為雙位數營收、Confluent 綜效兌現，軟體達雙位數，利潤率每年 +100bp 以上；市場給 22 倍","base":"照共識到 FY2028，之後營收 4–5%、利潤率擴張放緩，EPS 年增約 7%；倍數回到 18 倍","bear":"AI 編碼工具讓部分大客戶開始移出主機、顧問被 AI 通縮、硬體漲價反覆擠壓軟體預算，加上利息與併購稀釋，EPS 五年停在 $12–13；倍數降到成長熄火的 14 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2026-02 AI 編碼工具宣布可做 COBOL 現代化當天股價重挫約 13%；10-K 風險因素自列顛覆性技術；Q3 FY2026 Z 營收仍 −20%","assumption":"主機客戶的移轉成本長期高到不值得搬","consequence":"若前幾大銀行陸續搬離，交易處理、Z 與主機現代化顧問這組高毛利來源轉為遞減，EPS 停在 $12–13、倍數降到 14 倍以下，五年虧三到四成","ruling":"部分採納，已放入 30% 的 Bear 機率；目前反證較強：裝機 MIPS 五年翻倍、約 85% 裝機容量客戶維持或增加、z17 比前代多逾 $10 億，IBM 也把 AI 工具用在主機上的現代化","watch":"每季法說的「維持或增加容量客戶占比」、大型銀行核心系統遷移公告","evidence_refs":["substitute_technology#2","substitute_technology#0"],"fact_refs":[]},{"view":"論點失敗","evidence":"CEO 四月稱伊朗戰爭與地緣不確定性開始經由客戶影響展望；第二季客戶把預算轉去搶購漲價中的伺服器、儲存與記憶體，數十件大單延遲","assumption":"客戶 IT 預算分給 IBM 軟體的比例穩定","consequence":"交易型軟體（約占軟體 20%）再度延後，全年指引第二次下修，市場把第三季反彈視為一次性","ruling":"部分採納：第三季已收回約三分之二延遲單，但硬體漲價擠預算的機制沒有消失","watch":"記憶體與伺服器價格、管理層對預算挪移的說明、交易型軟體季增","evidence_refs":["geo_supply_chain#0","end_markets#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Confluent 約 $110 億全現金收購後淨負債由 $468 億升至 $538 億；賣方因併購稀釋與顧問轉弱下修 2026 EPS；SBC 占營業稅前利益 16.2%；前九月回饋全為股息、未見回購","assumption":"軟體成長能靠有機與既有併購延續，不需要再付高價收購","consequence":"營收與 EPS 達標，但每股價值被高價併購、利息與 SBC 吃掉，股息之外沒有回購撐每股","ruling":"採納為中度風險：管理層稱 2027 為併購綜效年，CFO 同時提到有機與無機並行；若再有逾 $100 億併購，資本配置風險升級","watch":"下一筆收購金額、淨負債與信用評等","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#3"],"fact_refs":["f_kpi5_sbc_operating"]},{"view":"價格已反映太多","evidence":"FY1 本益比 20.42 倍（三個月前約 16.9 倍）、RSI 71.22、26 週 +10.9%；七月賣方平均目標價約 $244、HSBC $175，均低於現價（皆為 Q3 前資料）","assumption":"市場會持續給復原中的 IBM 20 倍以上","consequence":"即使 EPS 照共識走，倍數回到 17–18 倍就吃掉兩年的 EPS 成長","ruling":"採納：這是本次不追價的主要原因","watch":"FY1 本益比與共識 EPS 上修幅度之間的差距","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_rsi14","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 205.77 → 本次 253.56（+23.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=205.77","side_b":"本次 price_at_dd=253.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 205.77 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 205.77 美元：Bull 價 370、Bear 價 161，五年期望值 +30.5%，基準年化 6.7%，不對稱比 3.0","side_b":"本次情境、股價仍用 205.77 美元：Bull 價 433.4、Bear 價 179.2，五年期望值 +48.1%，基準年化 9.0%，不對稱比 7.14","ruling":"先換情境、股價不動：五年期望值多 17.6 個百分點，基準年化多 2.3 個百分點。不對稱比由 3.0 變為 7.14。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 205.77 美元：五年期望值 +48.1%，基準年化 9.0%，不對稱比 7.14","side_b":"本次情境、股價 253.56 美元：五年期望值 +20.2%，基準年化 4.6%，不對稱比 2.02","ruling":"再換股價、情境不動：起點價上漲 23.2%，五年期望值少 27.9 個百分點，基準年化少 4.5 個百分點，不對稱比由 7.14 降到 2.02。合計五年期望值比前份少 10.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"第二季主機與交易處理失速是遞延還是流失","cause":"新證據","prior_field":null,"side_a":"第二季：交易處理 −9%、Z −42%，全年營收指引由逾 5% 下修至 4–5%，CFO 預期下半年交易處理下降低至中個位數","side_b":"第三季：交易處理 +10%、軟體 +9%，約三分之二延遲大單成交，z17 週期比前代多逾 $10 億，約 85% 裝機容量客戶維持或成長","ruling":"可調和：採第三季證據，遞延說法成立；但第三季同時吃到遞延單與正常購買週期，CEO 自承交易處理雙位數不會延續、全年交易處理指引為持平，因此只確認沒有流失，不確認加速","evidence_level":"公司財報與法說（一手）","settle_metric":"FY2027 交易處理全年成長率（管理層自述 z16 週期：上市年持平、次年中個位數、第三年高個位數）","if_then":["若 FY2027 前兩季交易處理年增 ≥3%，則確認 z16 式週期，Base 機率維持 45%","若 FY2027 任兩季交易處理年減 ≥5%，則 Bear 機率升至 40%、放棄建倉"],"evidence_refs":["end_markets#1","supply_demand_durability#0","capital_markets_pricing#2","competitive_share_entrants#1"]},{"axis":"管理層前後說法對帳","cause":"新證據","prior_field":null,"side_a":"2026-07-22 CEO（Krishna）：三週內約三分之一延遲交易成交，「尚非完整證據」；CFO（Kavanaugh）說約 40%，並把交易處理改列為 2027 年成長動能","side_b":"2026-10-21 CFO（Kavanaugh）：約 $4 億延遲軟體單收回三分之二、約 $2.5 億，占軟體加速的四分之一，其餘四分之三為新業務；全年軟體基本情境上調至約 7%","ruling":"可調和：數字前後一致且有進展，第二季給的保守基準被第三季超越，管理層可信度回升；但剩餘三分之一未收回，第二季被問到另外 15% 主機容量去向時沒有回答，仍是未解問題","evidence_level":"法說逐字稿（一手）","settle_metric":"Q4 FY2026 資料與自動化段是否收回剩餘延遲單；下一次法說是否揭露其餘 15% 容量客戶的狀態","if_then":["若 Q4 FY2026 軟體達全年 7% 以上，則管理層指引視為可信，不再對指引打折","若 Q4 FY2026 軟體全年低於 7%，則把 2027 財測打九折估算"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買：遞延已證、出貨 MIPS 增逾 100% 為 2027 交易處理變現鋪路、Red Hat 訂單回到高十幾、前九月 FCF 利潤率創新高、FCF 指引上調","side_b":"不追：FY1 本益比 20.42 倍已較三個月前約 16.9 倍重估，PEG 約 2.6，基本情境年化約 7% 低於 8%，RSI 71.22 過熱","ruling":"方向相反的估值分歧，不是論點矛盾：選不追。依據：Base EPS 年增約 7% 加股息約 2.7% 已等於基本情境全部報酬，股價再漲只能靠倍數再擴張；硬數據為 FY1 本益比 20.42 倍","evidence_level":"事實表價格與共識（一手）","settle_metric":"FY1 本益比；FY2027 共識 EPS","if_then":["若股價回到約 $215（FY1 本益比約 17 倍）且軟體成長未低於 7%，則分批建首倉至 2%","反向：若 2027 財測軟體 ≥8% 且 FY2027 共識上修至 ≥$13.8，而股價未超過 $265，則直接建首倉 2%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"前份估值與機率欄位漂移","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-23，股價 $205.77）：估值中性、FY1 本益比約 16.9 倍、Bull／Bear 機率 25%／30%、最大回撤 −35%","side_b":"本次（股價 $253.56）：估值偏貴、FY1 本益比 20.42 倍；機率維持 25／45／30，最大回撤改為範圍 −25% 至 −40%","ruling":"估值結論由中性降為偏貴，完全來自股價上漲約 23%，而共識 FY1 EPS 三個月只上修 0.73%；機率不動，因 Q3 的好消息已反映在 Base 終端 EPS，且共識成長超出內生上界，Bear 仍需至少 30%；最大回撤改成範圍、中點與前份相近","evidence_level":"事實表價格與共識","settle_metric":"FY1 本益比","if_then":["若 FY1 本益比回到 17 倍以下，估值結論回到中性"],"evidence_refs":[]},{"axis":"前份基本面欄位對帳","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質中上、價值陷阱風險中等、護城河持平、五年後成長跑道中等、品質複利成長型、非循環股、結論觀望","side_b":"本次：各欄不變。Q3 證據（軟體 +9%、交易處理 +10%、利潤率擴張、FCF 上調）強化軟體論點，但 Z 營收 −20% 與 AI 編碼工具威脅未解，相抵後各欄不動；軟體 ARR 兩年門檻由 $280 億改為 $270 億，因 ARR 年增穩在 8%、未見回到 10%","ruling":"維持：新證據讓延遲屬遞延得到確認，但沒有改變護城河方向或成長跑道；結論維持觀望的原因從「基本面未確認」換成「價格已反映」","evidence_level":"公司財報與法說（一手）","settle_metric":"2027 財測軟體成長","if_then":["若 2027 財測軟體 ≥8% 且交易處理轉正，則重評護城河方向是否轉為擴大"],"evidence_refs":[]},{"axis":"重啟條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","side_b":"FY1 本益比回到 17 倍以下（約 $215）且軟體固定匯率成長未低於 7%；或 2027 財測軟體 ≥8% 且股價未超過 $265","ruling":"前份三項條件兌現兩項（軟體固定匯率 +9%、未再砍指引並上調 FCF），延遲單收回約三分之二、未達 75%；同時股價已大漲，約束從基本面轉為價格，重啟條件改為價格錨，觸發後分批建倉、不追","evidence_level":"公司財報與法說（一手）","settle_metric":"FY1 本益比","if_then":["觸發價格條件後分三批建倉，每批間隔一季財報"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（空值）","side_b":"軟體固定匯率成長連兩季 <5%；交易處理連兩季 ≤−5%；顧問連兩季 <0%；FY2027 FCF 年增 <0","ruling":"新增：任一觸發即減碼，兩項同時觸發即清倉；門檻取自前份 R1、R2 的監測方向並改為可直接讀季報的數字","evidence_level":"方法調整","settle_metric":"各季報","if_then":["任一指標觸發則減碼一半","兩項同時觸發則清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空值）","side_b":"前 50 大銀行中有一家公開宣布以 AI 工具完成核心交易系統移出 IBM 大型主機","ruling":"新設：主機加交易處理是利潤與倍數的最大單一敏感項，公開先例會同時壓 EPS 與倍數；觸發即清倉","evidence_level":"方法調整","settle_metric":"公開遷移公告；維持或增加容量客戶占比","if_then":["若出現一例公開遷移，則清倉","若占比由約 85% 降至 80% 以下，則減碼一半"],"evidence_refs":["substitute_technology#2"]}],"triggers":[{"n":1,"text":"Q4 FY2026 軟體全年成長確認","type":"假設驗證","maps_to":"H1","metric":"軟體全年固定匯率成長","threshold":"≥7%","action":"未達則 Base 機率降至 40%、Bear 升至 35%，不建倉","source_freq":"季報（每季）","date":"2027-01"},{"n":2,"text":"交易處理再度失速","type":"風險","maps_to":"R2","metric":"交易處理軟體季度年增率","threshold":"連 2 季 ≤−5%","action":"減碼至零、放棄建倉","source_freq":"季報（每季）","date":null,"evidence_refs":["end_markets#1","supply_demand_durability#0","competitive_share_entrants#1"]},{"n":3,"text":"前 50 大銀行公開移出大型主機","type":"Single Thing","maps_to":"R1","metric":"公開遷移公告；維持或增加容量客戶占比","threshold":"出現一例，或占比低於 80%","action":"清倉","source_freq":"新聞與每季法說","date":null,"evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"n":4,"text":"價格回到合理區","type":"估值rearm","maps_to":"H3","metric":"FY1 本益比","threshold":"≤17 倍（約 $215）且軟體成長 ≥7% 未破","action":"分批建首倉至 2%","source_freq":"每日","date":null,"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"n":5,"text":"大單延遲揭露的證券集體訴訟正式提起並獲集體認證","type":"風險","maps_to":"R2","metric":"集體訴訟程序進度","threshold":"正式起訴且獲集體認證","action":"持倉減半、凍結加碼","source_freq":"SEC 申報與法院公告","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":6,"text":"顧問段轉負","type":"風險","maps_to":"H2","metric":"顧問固定匯率營收年增","threshold":"連 2 季 <0%","action":"Bear 機率升至 35%、停止加碼","source_freq":"季報（每季）","date":null,"evidence_refs":["substitute_technology#0"]},{"n":7,"text":"FY2026 自由現金流兌現","type":"假設驗證","maps_to":"H3","metric":"FY2026 FCF 年增額","threshold":"逾 $10 億","action":"未達則 H3 削弱、Base 終端倍數降至 17 倍","source_freq":"年報","date":"2027-01"},{"n":8,"text":"客戶預算再被硬體漲價或地緣衝突擠壓","type":"風險","maps_to":"R2","metric":"全年營收指引","threshold":"再次下修","action":"Bear 機率升至 40%、放棄建倉","source_freq":"季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","customer_concentration_credit#2","capital_markets_pricing#2"]},{"n":9,"text":"2027 財測與軟體長期目標量化","type":"複審日期","maps_to":null,"metric":"2027 軟體成長指引","threshold":"≥8% 視為加速、<6% 視為減速","action":"重跑完整判斷","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"軟體段固定匯率年增率","bear_threshold":"連兩季 <5%","window":"2027 年各季","source":"IBM 季報新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"交易處理軟體年增率","bear_threshold":"連兩季 ≤−5%","window":"2027 年各季","source":"IBM 季報法說","last_status":"ok"},{"metric":"顧問段固定匯率營收年增率","bear_threshold":"連兩季 <0%","window":"2027 年各季","source":"IBM 季報新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"全年自由現金流年增額","bear_threshold":"FY2027 年增 <0","window":"FY2027 全年","source":"IBM 10-K","last_status":"ok"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"事件已於 2026-04-10 以 $1,710 萬和解結案，指控屬反歧視證明不實而非反壟斷，證據本身沒有後續程序、也沒有對應的營收或業務限制可延伸到未來現金流"}],"action_conditions":{"rearm_trigger":"FY1 本益比回到 17 倍以下（約 $215）且軟體固定匯率成長未低於 7%；或 2027 財測軟體 ≥8% 且股價未超過 $265","exec_line":"不追高；觸及重啟條件後分三批建首倉至 2%，每批間隔一季財報；2027 財測軟體 <6% 則取消","holding_cap":"首倉上限 2%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY1 本益比回到 17 倍以下（約 $215），或 2027 年 1 月財測確認軟體 ≥8% 且股價未超過 $265","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=10.9, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"軟體段（Red Hat、Confluent、HashiCorp、交易處理）維持高個位數到雙位數成長，第二季交易型軟體失速屬遞延而非需求流失","2y":"FY2027 軟體固定匯率成長 ≥7%；高價值 ARR 於 FY2027 年底 ≥ $270 億","5y":"FY2030 軟體占公司營收過半，經常性占軟體比重 ≥85%","10y":null,"threshold":"高價值 ARR 年增 ≥7%（Q3 FY2026 為 $249 億、年增 8%）；軟體全年固定匯率成長 ≥7%","source":"IBM 季報新聞稿與法說（Q3 FY2026 軟體固定匯率 +9%、ARR $249 億 +8%）","drift_rule":"ARR 年增連 2 季低於 6.5% 為削弱、連 3 季低於 6% 為反轉"},{"id":"H2","text":"顧問段不因 AI 結構性萎縮，AI 轉型專案抵銷傳統專案通縮","2y":"FY2027 顧問固定匯率成長 ≥1%、簽約年增 ≥0","5y":null,"10y":null,"threshold":"顧問季度固定匯率成長 ≥0%；AI 占顧問營收 ≥30%、占在手訂單 ≥35%（Q3 FY2026 值）","source":"Q3 FY2026 法說：顧問 +2%、AI 約占顧問營收 30%、在手訂單 35%；Q2 FY2026 簽約 +6%","drift_rule":"連 2 季固定匯率成長 <0% 為削弱、連 3 季 <−2% 為反轉"},{"id":"H3","text":"生產力計畫每年推升營業稅前利潤率約 100bp，讓 EPS 在營收 4–5% 下仍有約 8% 成長、自由現金流每年增逾 $10 億","2y":null,"5y":"FY2030 營業利益率較 FY2025（18.5%）高 ≥300bp；FCF 每年正成長","10y":null,"threshold":"全年營業稅前利潤率擴張 ≥70bp；FY2026 FCF 年增逾 $10 億","source":"Q3 FY2026 法說（全年擴張 100bp 指引、FCF 上調）；年度營業利益率 FY2022 13.5% → FY2025 18.5%","drift_rule":"連 4 季利潤率年擴張 <50bp 為削弱、連 6 季 ≤0 為反轉"}],"R":[{"id":"R1","text":"AI 編碼工具（如 Claude Code）降低 COBOL 現代化成本，讓主機客戶移出核心系統，侵蝕交易處理與相關顧問","h_ref":"H1","clock":"🔥","threshold":"維持或增加容量客戶占比由約 85% 降至 80% 以下，或前 50 大銀行出現公開遷移案例","evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"id":"R2","text":"交易型軟體與主機硬體的季度波動：z17 週期進入尾段（Q3 FY2026 Z 仍 −20%），第二季式的大單延遲重演","h_ref":"H1","clock":"⚡","threshold":"交易處理連 2 季年減 ≥5%，或軟體季度固定匯率成長 <6%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0","end_markets#1","capital_markets_pricing#2"]},{"id":"R3","text":"成長愈來愈靠併購與舉債：Confluent 全現金收購後淨負債由 $468 億升至 $538 億，軟體有機成長只有約 4 點","h_ref":"H3","clock":"🐢","threshold":"剔除併購的有機軟體成長連 4 季 ≤3%，或信用評等降至 BBB+ 以下","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#3"]},{"id":"R4","text":"估值已回到溢價：FY1 本益比 20.42 倍、RSI 71，七月賣方平均目標價約 $244 低於現價","h_ref":"H3","clock":"⚡","threshold":"FY1 本益比超過 22 倍而共識 EPS 未同步上修","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"single_thing":{"description":"前 50 大銀行中有一家公開宣布以 AI 工具完成核心交易系統移出 IBM 大型主機","why_fatal":"主機是 IBM 利潤與倍數的核心：每 1 美元主機帶 3–5 美元軟體，交易處理多以企業授權綁定；公開先例會讓市場把交易處理、Z 與相關顧問從永續收入重估為遞減資產，EPS 與倍數同時下修","if_happens":"清倉；終端倍數改用 14 倍以下重估","how_monitor":"每季法說的維持或增加容量客戶占比（Q3 FY2026 約 85%）、大型銀行與監管單位的核心系統遷移公告","probability":"約 10%（12–24 個月）：管理層稱沒有客戶離開主機的證據、裝機 MIPS 五年翻倍；但 2026-02 AI 工具發布當天股價重挫約 13%，市場認真看待此風險"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":19.15,"peg_fy2":2.4,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":11.17,"FY2026E":12.42,"FY2027E":13.24,"FY2028E":14.48},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識 non-GAAP 營業 EPS；FY2025A 用 GAAP 稀釋 EPS $11.17（事實表未涵蓋 FY2025 營業 EPS），基期口徑不同會高估三年年增率，FY2026→FY2028 同口徑年增約 8.0%"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Confluent Streamhouse 發布","impact":"低","watch":"資料段交叉銷售是否讓 Q4 資料段維持 15% 以上"},{"date":"2026-12-10","date_precision":null,"type":"product","event":"IBM Quantum Day（量子路線圖與商業化進度）","impact":"低","watch":"有沒有量子營收或簽約金額的具體數字"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 全年財測、軟體長期目標量化","impact":"高","watch":"2027 軟體成長指引是否 ≥8%、交易處理是否轉為成長、FCF 年增是否兌現逾 $10 億"}]}
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
