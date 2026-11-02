你是 DD 管線 v20 的判斷層閘（gate），標的 RCL（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（44 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝5591 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：Benzinga 報導營收低於共識（未取得精確數字）
- `f_kpi1_operating_income_gaap`（q1_business）｜Operating income (GAAP)＝1871 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi2_operating_margin_gaap`（q1_business）｜Operating margin (GAAP, 計算值)＝33.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi3_adjusted_ebitda`（q1_business）｜Adjusted EBITDA＝2539 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi7_load_factor`（q1_business）｜Load factor＝112 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi8_guidance_fy2026_adjusted`（q1_business）｜Guidance: FY2026 Adjusted EPS＝17.85～17.95 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：上調；yfinance/快照 FY1 共識 17.90
- `f_kpi10_guidance_fy2026_net_yiel`（q1_business）｜Guidance: FY2026 Net Yields (as-reported)＝2.7 %（約）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi11_guidance_fy2026_ncc_ex_f`（q1_business）｜Guidance: FY2026 NCC ex fuel per APCD (as-reported)＝0.4 %（約）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_peer_rcl_operating_margin_pct`（q2_moat）｜RCL 營業利益率＝27.56 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RCL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rcl_gross_margin_pct`（q2_moat）｜RCL 毛利率＝49.06 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RCL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rcl_fcf_margin_pct`（q2_moat）｜RCL FCF 利潤率＝7.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RCL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vik_gross_margin_pct`（q2_moat）｜VIK 毛利率＝43.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VIK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vik_operating_margin_pct`（q2_moat）｜VIK 營業利益率＝23.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VIK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vik_fcf_margin_pct`（q2_moat）｜VIK FCF 利潤率＝16.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VIK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nclh_gross_margin_pct`（q2_moat）｜NCLH 毛利率＝40.57 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NCLH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nclh_operating_margin_pct`（q2_moat）｜NCLH 營業利益率＝10.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NCLH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ccl_gross_margin_pct`（q2_moat）｜CCL 毛利率＝39.47 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCL.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ccl_operating_margin_pct`（q2_moat）｜CCL 營業利益率＝15.99 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ccl_fcf_margin_pct`（q2_moat）｜CCL FCF 利潤率＝11.51 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCL.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝17.9 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝20.43 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝23.38 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝19558.01 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝20991.68 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_free_cash_flow_ytd_5_274`（q4_capital）｜Free cash flow YTD (計算值： 營運現金流 5,274 − 資本支出 3,880)＝1394 USD M｜期間與口徑：9M FY2026（至 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（公司未報 FCF，為自行計算）（numbers.latest_quarter_kpis.items[5]，as_of 9M FY2026（至 2026-09-30，公告於 2026-10-27））
- `f_kpi6_share_based_compensation`（q1_business）｜Share-based compensation YTD＝94 USD M｜期間與口徑：9M FY2026（至 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 earnings release（8-K 附件）https://www.sec.gov/Archives/edgar/data/0000884887/000088488726000042/a2026q3earningsrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of 9M FY2026（至 2026-09-30，公告於 2026-10-27））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝22319.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 23170.0、現金 851.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.706 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝267.47 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝322.3 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝18.01 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 17.9，分子＝快照價 322.32｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝19.07 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝51.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝51.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.51 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.67 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝72.74｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝25.65 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.02 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 17.72 → 17.9（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝108530.23 USD m｜期間與口徑：2026-11-03／市值 86211.23 ＋ 淨負債 22319.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_w250`（q5_valuation）｜250 週均線＝167.87 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w52`（q5_valuation）｜52 週均線＝282.4 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝272.37 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司依賴旅行顧問訂位，若佣金不具競爭力，顧問可能轉賣對手郵輪
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：業界新船訂單簿：2026-03 約 78 艘、逾 206,600 床位；2027 年交付 15 艘、2028 年 13 艘（約 30,770 床位）；2026-04 更新為 93 艘、約 229,500 床位
  - 來源：Cruise Industry News orderbook updates (2026-03, 2026-04, 2026-07)（as_of 2026-03-31）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K FY2025 Item 3 僅列 Helms-Burton Act 的 Havana Docks 訴訟（美國最高法院 2025-10-03 准予調卷），其餘為產業常見索賠、多數有保險；未列反壟斷調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings（as_of 2026-02-11）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：RCL 10-K 風險因素稱供應鏈可能受關稅與貿易制裁等新法規影響；美國對特定國家進口品加徵關稅帶來不確定性，重大貿易關係變動可能對業務、財務與經營成績產生重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：RCL 2026年營收成長指引由10%下調至約9%，理由是長期地緣緊張對部分航程造成小幅訂位衝擊；歐洲航程最受影響
  - 來源：Hotel-Online/Reuters: Royal Caribbean Trims Revenue Forecast on Booking Hit from Geopolitical Tensions（as_of 2026-07-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：RCL新船集中於Meyer Turku（芬蘭）與Chantiers de l'Atlantique（法國）兩家船廠，在建船約165億美元，約49.9%成本暴露於歐元匯率
  - 來源：RCL 10-Q (2026-09-30)（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中東衝突壓抑RCL歐洲航程需求
  - 來源：Cruise Industry News（as_of 2026-07-28）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：部分歐洲航線訂位因地緣政治活動受輕微影響，已反映於指引；2026全年淨收益率指引曾兩度收窄至1.75%–2.25%；有分析師質疑船上消費強勢能否轉為2027年船票價格。
  - 來源：Cruise Industry News／Zacks 報導，RCL 2027 pricing（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：若公司跟不上技術發展，營運或競爭地位可能受損；使用 AI 等新興技術帶來業務、合規與聲譽風險。未點名具體取代性技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 指出具備建造/維修能力的船廠數量有限，供應鏈中斷因替代選項少而衝擊業務（替代供應商面向，非替代產品）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：2026-07-31 Freedom Capital 將 RCL 由 strong buy 降至 hold；Stifel 目標價 $415、BMO $370；Susquehanna $355、Wells Fargo $358、Jefferies $330（10 月）
  - 來源：MarketBeat 2026-07-31 Freedom Capital downgrade；FN2（as_of 2026-07-31）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Havana Docks 訴訟（Helms-Burton）：11th Circuit 於 2024-10-22 推翻約 1.12 億美元判決；原告 cert 申請於 2025-10-03 獲最高法院受理，結果未定。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-11）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Havana Docks 訴訟：最高法院 2025-10-03 受理 cert，原判決約 1.12 億美元已被 11th Circuit 推翻，結果未定；搜尋未見近 12 個月證券集體訴訟（僅 2011、2020 舊案）。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-11）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":605.2,"bear_5y_price":194.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":41.9,"ev5y_pct":28.9,"irr_base_pct":7.3,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":17.9,"pe":18.01,"basis":"FY2026E 共識調整後 EPS 17.90（財年只剩約兩個月，接近實績）；終端倍數同樣套在終端當年 FY2031E，口徑一致"},"eps":{"bull":[21.0,24.4,28.0,31.8,35.6],"base":[20.4,23.0,25.5,28.0,30.5],"bear":[19.2,15.8,15.0,16.8,18.5]},"pe":{"bull":17,"base":15,"bear":10.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.706,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RCL_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：全年淨收益率成長財測（原話："We expect net yield growth of 1.75% to 2.25% for the"）
- 2026-07-28｜CEO｜guidance：全年調整後EPS財測（原話："grow 14% and be in the range of $17.73 to $17.87"）
- 2026-07-28｜CFO｜guidance：第三季淨收益率財測（原話："net yields are expected to be roughly flat"）
- 2026-07-28｜CFO｜guidance：第三季運力成長（原話："capacity is expected to be up 8.5%"）
- 2026-07-28｜CFO｜guidance：第四季收益率預期重新加速（原話："we anticipate yield growth during the fourth quarter"）
- 2026-07-28｜CFO｜guidance：第四季約2點有利、第三季同等不利（原話："this provides a 2-point benefit to fourth quarter yields"）
- 2026-07-28｜CFO｜guidance：全年不含燃油淨郵輪成本大致持平（原話："expected to be approximately flat, consistent with"）
- 2026-07-28｜CFO｜guidance：第三季不含燃油淨郵輪成本財測（原話："expected to decrease in the range of 1.1% to 1.6%"）
- 2026-07-28｜CFO｜guidance：第三季EPS財測（原話："between $6.26 and $6.36, a double-digit year-over-year"）
- 2026-07-28｜CFO｜guidance：燃油避險比例（原話："58% hedged at significantly below market rates"）
- 2026-07-28｜CFO｜guidance：為2027年加碼避險（原話："we opportunistically hedged more for 2027"）
- 2026-07-28｜CFO｜guidance：EPS財測受合資事業與財務費用面支撐（原話："benefited from an improved outlook from our joint ventures"）
- 2026-07-28｜CFO｜guidance：佈署組合對收益率的輕微逆風（原話："mix this year creates slight headwinds to yields"）
- 2026-07-28｜CFO｜guidance：CFO說第三季約200基點逆風、第四季類似順風（原話："around 200 basis points headwind to the third quarter"）
- 2026-07-28｜CEO｜guidance：2027年收益率幅度現在談為時過早（原話："exactly what the yield handle will be for next year"）
- 2026-07-28｜CEO｜guidance：載客率目標區間（原話："we're happy with being a couple of"）
- 2026-07-28｜CEO｜guidance：2027年預訂進度與價格（原話："book position is in line with prior years at record pricing"）
- 2026-07-28｜CFO｜margin：Q2 EBITDA 利潤率（原話："EBITDA margin was 38%"）
- 2026-07-28｜CFO｜margin：Q2成本較預期低因時點（原話："timing of our costs shifting to the second half of the year"）
- 2026-07-28｜CEO｜margin：致力擴張利潤率（原話："We also remain committed to expanding margins by"）
- 2026-07-28｜CFO｜margin：Q2收益率較財測高100基點（原話："were 100 basis points above our guidance"）
- 2026-07-28｜CFO｜margin：Q2 EPS超財測中點（原話："$0.33 higher than the midpoint of our guidance"）
- 2026-07-28｜CEO｜risk：中東衝突持續比預期長（原話："the conflict has persisted longer than anticipated"）
- 2026-07-28｜CEO｜risk：歐洲收益率低於預期；管理層稱否則會上調下半年（原話："to the point, we would have raised the"）
- 2026-07-28｜CEO｜risk：歐洲收益率未下降但低於預期（原話："Now that's not to say that European yields are down."）
- 2026-07-28｜CEO｜risk：Mahahual時程受影響（原話："is expected to affect our previously planned time line"）
- 2026-07-28｜CEO｜risk：消費者更審慎支出（原話："Consumers are becoming more deliberate about their spending"）
- 2026-07-28｜CEO｜risk：消費者偏好較近目的地（原話："preferring closer destinations over international trips"）
- 2026-07-28｜CFO｜competition：加勒比海競爭定位（原話："competitive position in the region is strong"）
- 2026-07-28｜CFO｜competition：業界運力偏高下仍成長收益率（原話："with elevated industry capacity in the region"）
- 2026-07-28｜CEO｜competition：對同業促銷的回應（原話："less insulated from what our competitors are doing"）
- 2026-07-28｜CEO｜competition：Celebrity River定價高於同業（原話："higher than what we see in the competitive set for River"）
- 2026-07-28｜CEO｜capital_allocation：Q2回饋股東（原話："we returned over $600 million of capital to investors"）
- 2026-07-28｜CFO｜capital_allocation：股利與回購（原話："we paid $404 million of dividends and repurchased"）
- 2026-07-28｜CFO｜capital_allocation：剩餘回購額度（原話："$805 million remaining under our current share repurchase"）
- 2026-07-28｜CFO｜capital_allocation：流動性與槓桿（原話："$6.9 billion in liquidity and leverage below 3x"）
- 2026-07-28｜CEO｜customer：Royal ONE持卡人重複出航（原話："they are twice as likely to sail"）
- 2026-07-28｜CEO｜customer：年輕客群偏好較短假期（原話："they like to take shorter vacations, like to do"）
- 2026-07-28｜CEO｜customer：重複客消費多20-25%（原話："those repeat guests spend 20% to 25% more"）
- 2026-07-28｜CEO｜customer：近期預訂定價能力（原話："we would typically have to discount for close-in demand"）
- 2026-07-28｜CEO｜commitment：2027年達成Perfecta（原話："reaching Perfecta by the end of next year"）
- 2026-07-28｜CEO｜commitment：App個人化功能明年初推出（原話："you'll start to see in early next year"）
- 2026-07-28｜CEO｜commitment：不為完美做規劃（原話："we don't plan for perfection"）
- 2026-07-28｜CEO｜commitment：以溫和收益率成長加成本控制創造價值（原話："tremendous shareholder value with moderate yield growth"）
- 2026-07-28｜CEO｜product：西加勒比佈署可能邊際調整（原話："That's not our expectation today, but there might be."）
- 2026-07-28｜CEO｜product：Mahahual狀態不評論（原話："we're not really in a place to comment on the status of that"）

### 問答異常語氣（迴避／改口／保留）
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Farley：2027在手訂單的載客率與價格是否較去年同期高｜答法：CFO只答「booked very well and at higher prices」；CEO說載客率「more or less in line」，未給具體數字
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Dove：2027是否可能是高於長期算法的一年｜答法：CEO反駁「comps are easy」，說明年收益率幅度太早，未給方向或數字
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Montour：Mahahual延後是否影響2028-29年東西加勒比50-50目標｜答法：CEO答「we'll see」，表示不評論開發狀態，僅稱部署可能邊際調整
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Rollo：第三季載客率是否降、預訂載客率是否因晚訂單轉弱｜答法：CEO談價格紀律與管理最適載客率，未直接回答第三季或未來載客率是否下降
- RCL_Q2_2026_Earnings_Call_20260728.md｜問：Cunningham：第四季隱含收益率走升的驅動｜答法：CFO稱「not guiding to it」，只給約200基點時點性順逆風，未談需求面

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 6 | 3 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 4 | 1 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"供給端結構性受限使郵輪業具備長期定價地板——全球船廠年交付上限 14-16 艘、RCL 已鎖定 Meyer Turku 檔期至 2036，供給無法對需求上升快速反應"},{"id":"H2","text":"Perfecta 兌現且其後仍有 10%+ 的內生成長——2027 年調整後 EPS 達到相對 2024 的 20% CAGR（$20.4）、ROIC 17%+，且 2028-2031 靠運力 +5%／收益率 +2%／利息下降／回購維持雙位數 EPS 成長"},{"id":"H3","text":"市場對這門生意的估值框架不再下移——退出倍數維持在 Fwd P/E 14-16x 的成熟複利區間，而非回到 pre-COVID 郵輪業的 11-13x 週期股區間"}],"extra_text":"# | 具體數字門檻（floor） | 信息來源 | 漂移觸發條件\nH1 | FY2027 RCL 運力成長 ≤ +5%；FY2027 淨收益率 CC ≥ +2.5%；全球船廠年交付 ≤ 16 艘 | 船廠產能上限與六家主要船廠集中度：Hope Research Group《Cruise Capacity Growth 2026-2028》（2026）；Meyer Turku 長約鎖至 2036、Icon 6/7 訂單：Royal Caribbean Group 新聞稿（2026-05）；RCL 自身 2027-2029 運力 +4%／+6%／+7%：產業運力預測（2026） | 連 4 季淨收益率 CC 低於 +1.5%（5Y 假設，季節性過濾後）→ 削弱；連 6 季低於 0% → 反轉。單季地緣造成的波動不觸發。\nH2 | FY2026 調整後 EPS ≥ $17.73（指引下緣）；FY2027 ≥ $20.0；FY2031 ≥ $32；單船增量 ROIC ≥ 13% | FY2026 指引 $17.73-17.87：RCL Q2 2026 財報新聞稿（2026-07-28）；FY2027 共識 $20.01（n=28）、FY2028 $22.76：Koyfin/Excel 共識快照 2026-07-16 ＋ yfinance earnings_estimate（2026-07-29）；Perfecta 目標定義：RCL 新聞稿（2025-03） | FY2027 共識連 4 季累計下修 &gt; 5%（5Y 假設）→ 削弱；共識跌破 $18.5 → 反轉（Perfecta 結構性失敗）。\nH3 | Fwd P/E（FY+2）≥ 13x；EV/EBITDA ≥ 11x | 本報告自算之後疫情期（2023-01 起）Fwd P/E（FY+2 口徑）分布：低 4.72x／中位 11.05x／p75 14.47x／高 20.06x，現值 16.12x（§11.1）；EV/EBITDA 5 年均 13.36x、2025-12 峰 15.4x：GuruFocus／valueinvesting.io（2026） | 連 4 季 Fwd P/E（FY+2）低於 11x → 削弱（市場重新以週期股框架定價）；連 6 季低於 9x → 反轉。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"地緣事件持續壓抑地中海與近端國際航線。中東衝突已持續超出管理層預期，改變了消費者的目的地偏好（因機票成本轉向近程）。歐洲占 Q3 運力 28%，單季曝險遠高於全年 14%。"},{"id":"R2","text":"加勒比海運力集中投放引發系統性降價。加勒比海占全球郵輪運力 42%、占 RCL FY26 運力 57%；2026 年加勒比海部署較 2025 年增加 12%，2027-2029 產業運力續增 +4%／+6%／+7%。同業已在加速促銷。"},{"id":"R3","text":"目的地資產的政治與監管風險系統化。Mahahual 時程已受影響；墨西哥 DNR 稅三年 4.2 倍；EU ETS 自 2026-01 起 100% 涵蓋且擴及甲烷與氧化亞氮；美國 Section 883 免稅地位（RCL 有效稅率僅 1.9%）長期存在政策檢討風險。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","irr_base_pct":9.4,"ev5y_pct":30.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.8,"ev5y_pct":30.6,"irr_base_pct":9.4,"max_dd_pct":-60.0,"bull_5y_price":646.0,"bear_5y_price":170.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","price_at_dd":322.5,"archetype":"品質複利成長","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"RCL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Royal Caribbean Cruises Ltd."},"oneliner":"郵輪業利潤率最高的一家，2027 年 20 美元 EPS 大概率達標；但現價已用 15.8 倍 FY2027 盈餘在利潤率高點定價，自由現金流又只有淨利三成上下，等回到約 296 美元再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺北美為主度假客的船票與船上消費，錢卡在「自有新船＋私人目的地」這一節：Q3 營收 55.9 億美元、營業利益率 33.5%，TTM 營益率 27.6% 為上市同業最高","reasoning":"收錢方式：先收訂金後出航，營收＝船票＋船上消費；Q3 營收年增 9%＝運力 +8%＋淨收益率 +0.6%（固定匯率）。部署：2026 年加勒比占運力 57%、歐洲 15%、阿拉斯加 5%；2027 年加勒比 56%、歐洲 16%、亞太 11%（2026-10-27 法說 CFO）。船票與船上消費的拆分、品牌別營收事實表未涵蓋。單點依賴：加勒比占運力過半；新船集中在 Meyer Turku 與 Chantiers de l'Atlantique 兩家船廠，屬供應商集中風險；客戶為分散個人，無大客戶。供需持久性：供給端結構性受限（大型船廠訂單排到 2036、2027 年全業界約 15 艘交付），需求端屬可延後的週期性消費；加勒比區域運力 2026 年 NCLH +55%、MSC +23%，區域供給可逆性高。產業時鐘判 III：利潤率在歷史高點（營益率 FY2023 20.7%→FY2025 27.4%→TTM 27.6%），淨收益率成長已放緩到全年約 2.1%，對手運力集中投放加勒比，屬擴張後段。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_operating_income_gaap","f_kpi2_operating_margin_gaap","f_kpi3_adjusted_ebitda","f_kpi7_load_factor","f_kpi8_guidance_fy2026_adjusted","f_kpi10_guidance_fy2026_net_yiel","f_kpi11_guidance_fy2026_ncc_ex_f","f_peer_rcl_operating_margin_pct"],"verdict_values":{"revenue_quality":"預收型、可見度高：2026 與 2027 訂位進度都領先往年且費率創紀錄，近一半旅客為回頭客；弱點是對消費景氣、燃油與地緣事件敏感（2026-04 曾因燃油把全年 EPS 指引中點由 17.90 下修到 17.30）","unit_econ_note":"Q3 載客率 112%、調整後 EBITDA 25.39 億美元（利潤率約 45%）；全年不含燃油單位成本約持平（報表口徑約 +0.4%），淨收益率約 +2.1% 即可擴張利潤率；FY2026 燃油費用約 13.5 億美元，Q4 避險 58%","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"重資產、預收現金、運力受船廠排程限制；三年共識 EPS 年複合約 14%，但自由現金流只有淨利三成上下，景氣下行時盈餘彈性大"},"industry":{"clock_phase":"III","sd_verdict_source":"供給結構性受限、需求週期性：CLIA 稱大型船訂單排到 2036、2027 年約 15 艘約 2.8 萬床位交付；需求面 CLIA 預測 2026–2029 全球乘客個位數成長，NCLH 預期 2027 上半年需求仍弱","bargaining":{"up":"船廠議價權強：可建大型船的船廠少，RCL 在建船約 165 億美元、約 49.9% 成本以歐元計（2026-09-30 10-Q）","down":"客戶為分散個人消費者，無單一大客戶；旅行顧問仍是重要通路，佣金需維持競爭力","geo":"客源以美國為主（FY2020 10-K 美國占船票營收 67%，資料偏舊）；運力過半在加勒比"},"profit_pool_dir":"利潤池向頭部集中：TTM 營益率 RCL 27.6%、VIK 23.3%、CCL 16.0%、NCLH 10.9%","tam_table":{"expanded":false,"reason":"核心郵輪屬成熟市場，事實表未涵蓋郵輪滲透率與利潤池分段歷史；Sandals 全包式度假村是新品類，但公司稱 2027 年貢獻不重大，不承重本次估值"}}}},"q2_moat":{"verdict":"護城河 B 級、方向穩定（→）：利潤率仍是同業最高，但收益率成長放緩、加勒比對手運力大增，前幾年的擴大趨勢暫停","reasoning":"機制：規模＋硬體差異化＋自有私人目的地＋跨品牌會員，轉成定價溢價與單位成本優勢。證據：TTM 毛利率 49.1%、營益率 27.6%，分別高於 CCL 9.6 與 11.6 個百分點、高於 NCLH 8.5 與 16.7 個百分點、高於 VIK 5.9 與 4.3 個百分點；Icon 級新船載客率 133%、NPS 80 以上（2026-10-27 法說，品牌總裁 Bayley）；約一半旅客為回頭客、40% 為會員。同業 ROIC 差距無法計算（事實表無投入資本），改用營益率差距，且只有一個 TTM 時點，差距方向無法驗證。方向：執行面仍擴大（營益率續升、不含燃油單位成本約持平），定價面由擴大轉穩定（淨收益率放緩到全年約 2.1%，Q3 報表口徑毛利收益率 −0.8%），合判穩定。反例：VIK 自由現金流利潤率 16.6% 遠高於 RCL 7.9%，代表 RCL 的利潤率優勢有一部分是靠更重的資本投入換來。評分：執行 8、定價 7。","fact_refs":["f_peer_rcl_gross_margin_pct","f_peer_rcl_operating_margin_pct","f_peer_rcl_fcf_margin_pct","f_peer_vik_gross_margin_pct","f_peer_vik_operating_margin_pct","f_peer_vik_fcf_margin_pct","f_peer_nclh_gross_margin_pct","f_peer_nclh_operating_margin_pct","f_peer_ccl_gross_margin_pct","f_peer_ccl_operating_margin_pct","f_peer_ccl_fcf_margin_pct","f_kpi7_load_factor"],"verdict_values":{"moat":{"mechanism":"規模＋硬體差異化（Icon 級新船載客率 133%、NPS 80 以上）＋自有私人目的地＋跨品牌會員（約一半回頭客、40% 為會員），轉成定價溢價與單位成本優勢","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營益率 FY2023 20.7%→FY2024 24.9%→FY2025 27.4%→TTM 27.6%，每年擴張幅度由 2～4 個百分點降到 0.2；FY2026 淨收益率約 +2.1%（固定匯率），低於年初指引區間 1.5–3.5% 的中點；2026 加勒比運力 RCL +9%，NCLH +55%、MSC +23%","competitor_notes":[{"name":"CCL","strategy_note":"最大運力、偏大眾價位，TTM 營益率 16.0%，比 RCL 低約 11.6 個百分點；稱 2027 約半數已訂、價格創紀錄，需求面與 RCL 同向"},{"name":"NCLH","strategy_note":"2026 年加勒比運力 +55% 最激進，TTM 營益率 10.9%、自由現金流利潤率 −6.4%，並預期 2027 上半年需求仍弱，最可能在加勒比以價格搶客"},{"name":"VIK","strategy_note":"河輪與小型遠洋、高價位熟齡客群，TTM 營益率 23.3%、自由現金流利潤率 16.6% 高於 RCL，資本負擔較輕；RCL 2027 年進入河輪後正面相遇"},{"name":"MSC","strategy_note":"未上市，2026 年加勒比運力 +23%、份額約 10%，事實表無財務數字"}],"peer_na_reason":"事實表同業對照只有利潤率、沒有投入資本，無法算同業 ROIC 差距；改用營益率差距，且只有單一 TTM 時點","threats":[{"level":"🟡","text":"加勒比對手運力集中投放（NCLH +55%、MSC +23%）與業界新船訂單約 93 艘，區域價格競爭；目前 RCL 加勒比收益率仍為正","p":"35%","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2"]},{"level":"🟡","text":"陸上全包式度假村與主題樂園爭奪同一筆度假預算；管理層自承郵輪價格漲幅落後陸上，並以 Sandals 50% 股權因應","p":"25%","evidence_refs":["substitute_technology#3","substitute_technology#2"]},{"level":"🟡","text":"旅行顧問通路：佣金若不具競爭力，顧問會轉賣對手產品；公司同步投資自有網站與 App","p":"15%","evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#0"]},{"level":"🟡","text":"技術落後或 AI 應用失誤的通用風險，10-K 未點名具體取代技術；郵輪是實體體驗，AI 較可能是工具而非替代","p":"10%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一家庭，三角色一致；但度假屬可延後的「想要」。Q2 法說（2026-07-28）CEO 稱消費者花錢更審慎、偏好近程，Q3 法說改稱訂位加速、2027 費率創紀錄：目前需求強，本質仍是景氣轉差時最先延後的支出"},{"item":"決策層級","level":"🟡","text":"客戶在「這次去哪度假」的層級選擇，CEO 稱客戶不是拿 RCL 換別家郵輪，而是換陸上度假；代理變數：回頭客約一半、會員占 40%、跨品牌旅客單日消費較高。但沒有合約或轉換成本，留存靠產品力而非鎖定"},{"item":"價值鏈分配","level":"🟡","text":"上游船廠集中（兩家承建、約 49.9% 成本為歐元）分走部分價值；旅行顧問收佣；目的地港口與政府收稅費。RCL 以自有私人目的地（2028 年前由 3 個增至 8 個）把岸上消費留在體系內，是少數能從其他環節搶回價值的做法"},{"item":"社會容忍度","level":"🟡","text":"目的地社區與政府的容忍度是上限：Mahahual 開發時程已受影響，兩季法說都不評論進度；環保法規與目的地稅費會抬高成本。航運所得稅務地位與碳排成本數字事實表未涵蓋，列資料缺口"}],"roiic":20,"reinvest_rate":57,"endo_ceiling":11.4,"formula_note":"當期 ROIC：事實表未涵蓋投入資本，管理層稱已達 Perfecta ROIC 目標，數字未核實。再投資率＝FY2023–FY2025 累計（淨利−自由現金流）÷累計淨利＝（88.42−38.13）÷88.42 億美元≈57%（以淨利代稅後營業利益、以自由現金流缺口代淨再投資，含預收款變動，屬粗估）。增量報酬＝FY2024→FY2025 營業利益增加約 8.0 億美元（164.85 億×24.92%→179.34 億×27.38%）÷FY2025 淨再投資約 30.3 億美元≈26%；疫後收益率回升殘差會高估、新船當年未滿載會低估，取 20% 為中值（區間 15–26%）。內生成長上界＝20%×57%≈11.4%"}}}},"q3_growth":{"verdict":"中長期跑道寬：郵輪在兆美元度假市場占比小，Sandals、河輪與私人目的地是有來源的第二條曲線；但未來三年約 14% 的 EPS 成長有約 3 個百分點不是內生","reasoning":"成長拆解：量（運力 2026 +6.6%、2027 +4.5%，Q1 2026 財報稿稱 2028 +6%、2029 +7%）＋價（淨收益率 2026 約 +2.1%，2027 公司未給，且 Q1 有約 200 個基點結構性逆風）＋成本（不含燃油單位成本約持平帶來營業槓桿）＋淨回購。三年共識 EPS 年複合約 14.4%（FY2025A 15.61→FY2028E 23.38），但 FY2027 共識營收只成長 7.3%，差額靠利潤率與每股化。再投資報酬推導的內生成長上界約 11.4%，缺口約 3 個百分點主要歸因利潤率擴張（營業槓桿），其次淨回購；財務費用變化方向事實表未涵蓋。跑道：10-K 稱公司在逾兆美元度假市場占比小，CEO 稱目前只拿到客人年度度假支出的 20～25%，加入全包式度假村後可觸及約 50%；限制主要在船廠交付而非需求。反例：CLIA 預測 2028–2029 全球乘客只成長約 2%，若第二曲線遲遲不貢獻，跑道會比判斷窄。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_guidance_fy2026_adjusted","f_kpi10_guidance_fy2026_net_yiel"],"verdict_values":{"growth":{"driver_mix":"量＋價為主：運力每年 +4.5～7%、淨收益率約 +2%，加上成本約持平的營業槓桿與淨回購；Sandals 2027 年貢獻公司稱不重大","runway_years":"≥10（推估；郵輪滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"內生成長上界約 11.4%（增量報酬約 20%×再投資率約 57%）；三年共識 EPS 年複合約 14.4%，缺口約 3 個百分點歸因利潤率擴張與淨回購，可歸因","segments":{"expanded":false,"reason":"公司只報單一郵輪分部，品牌別營收事實表未涵蓋；部署區域占比已寫進怎麼賺錢一題，利潤 mix 的承重點在加勒比收益率，已設為風險與觸發條件"},"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 49.06% 對 FY2025 49.35% 小幅回落，列觀察"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"加勒比運力份額被稀釋（RCL +9% 低於 NCLH +55%、MSC +23%），但 RCL 加勒比收益率仍為正，營收份額未見縮減，列觀察"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"Q3 載客率 112%，2027 訂位量年增高十幾%且費率創紀錄"},{"item":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY2027 共識 EPS +14.1% 對共識營收 +7.3%，差 6.8 個百分點"},{"item":"自由現金流÷淨利連 2 年 < 0.75","lit":true,"evidence":"FY2024 0.69、FY2025 0.29，主因新船資本支出"},{"item":"SBC 占營收 > 5% 且逐年上升","lit":false,"evidence":"前 9 個月 SBC 9,400 萬美元，不到營收 1%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"CLIA 預測乘客 2026 年 3,830 萬→2027 年 4,030 萬"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"P/S、EV/S 都在近 4 個年度端點最高位"},{"item":"維持性資本支出占自由現金流 > 60%","lit":false,"evidence":"維持性資本支出事實表未涵蓋，無法判斷"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2027 仍有 Hero of the Seas 與河輪加入，營收持續成長"}],"trap_rating":"🟡（亮 2 項）"}}},"q4_capital":{"verdict":"資本配置中等：SBC 稀釋輕、資產負債表升到投資級，但自由現金流只有淨利三成上下，股利已吃掉大半，回購與 Sandals 靠舉債支應，回購報酬是否跑贏資金成本無法驗證","reasoning":"自由現金流轉換率偏低：FY2023／2024／2025 自由現金流÷淨利＝0.34／0.69／0.29（年度財報，事實表 financial_history，yfinance）；FY2026 前 9 個月自由現金流 13.94 億美元（營運現金流 52.74 億−資本支出 38.80 億），TTM 自由現金流利潤率 7.9%，低於 CCL 11.5%、VIK 16.6%。主因新船資本支出；2027 運力成長降到 4.5%，資本支出有機會放緩，但金額事實表未涵蓋。現金去向：資本支出為大宗；Q2 回饋股東逾 6 億美元（股利 4.04 億美元＋回購），剩餘回購額度 8.05 億美元（2026-07-28 法說 CFO）；股利殖利率 1.7%，年化股利約 14～15 億美元，與自由現金流相當，回購與 Sandals 實質靠舉債與再融資（2026-08 發行 12.5 億美元 5.55% 2034 年票據償還浮動利率貸款；Sandals 由 Morgan Stanley 承諾融資）。三年現金去向四分事實表未涵蓋。資產負債表：淨負債 223 億美元、流動性 74 億美元、槓桿低於 3 倍、S&P 2026-02 升到 BBB。","fact_refs":["f_kpi5_free_cash_flow_ytd_5_274","f_kpi6_share_based_compensation","f_net_debt_m","f_dividend_yield_ttm","f_peer_rcl_fcf_margin_pct","f_peer_ccl_fcf_margin_pct","f_peer_vik_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"尚無已實現併購：Sandals 50% 股權約 30 億美元（10 倍前瞻 EBITDA）預計 2027 年初交割，報酬待驗"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"以約 18 倍本益比回購，盈餘殖利率約 5.6%，僅與 2026-08 新發 2034 年票據利率 5.55% 相當；10 年期公債殖利率與回購均價事實表未涵蓋，無法判過或不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前 9 個月 SBC 9,400 萬美元，年化約 1.25 億，約為市值 0.15%，遠低於 1.5%；股數變化事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠新船運力與收益率，不靠併購；Sandals 交割後才有併購報酬可驗，股利與回購數字已寫在判讀句"}}}},"q5_valuation":{"verdict":"現價 322.3 美元要求 FY2027 調整後 EPS 達 20 美元以上、之後每年再成長約 10%，且退場時市場仍給 15 倍左右；前者我信，後者只信一半，估值偏貴","reasoning":"現價＝FY2026E 共識 17.90 的 18.0 倍、FY2027E 20.43 的 15.8 倍、FY2028E 23.38 的 13.8 倍；三年共識 EPS 年複合約 14.4%，PEG 約 1.25（FY2027 口徑約 1.1）。現價要求三件事：2027 年 20 美元以上兌現、之後每年約 10% 成長、退場倍數不跌回週期股區間。第一項有訂位與指引支撐，第三項依賴市場繼續把 RCL 當複利股。短期上檔：FY2027E 20.43×16.5 倍≈337 美元（+4.6%）；約兩年：FY2028E 23.38×15 倍≈351 美元（+8.8%）。賣方目標價平均約 345～349 美元，Q3 後 Barclays、BofA 下修目標價到 342、325。動能：26 週漲 25.7%、RSI 72.7 偏熱，同期盈餘預估上修遠小於股價漲幅（FY1 近 3 個月僅 +1.0%），漲幅主要來自倍數回升。同業倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_rsi14","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ev_m"],"verdict_values":{"valuation":{"basis":"Fwd P/E：FY2026E 共識調整後 EPS 17.90，現值 18.0 倍；FY2027E 20.43 對應 15.8 倍","tier":"大型上市郵輪（與 CCL、NCLH、VIK 同層）","peers":{"expanded":false,"reason":"事實表同業對照只含毛利率、營益率、自由現金流利潤率，未含同業倍數，無法建立倍數對照"},"fwd_pe":18.01,"peg":1.25,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"PEG 約 1.25（Fwd P/E 18.0÷三年共識 EPS 年複合約 14.4%）落在合理區；但分母是利潤率歷史高點的盈餘（TTM 營益率 27.6%，FY2023 為 20.7%），P/S 4.51 倍、EV/S 5.67 倍都在近 4 個年度端點最高位；5 年本益比分位事實表未涵蓋（只有 3 個年度端點，51.8 分位不能當 5 年分位）。週期性重資產公司在利潤率高點給 18 倍當年本益比，定為偏貴","upside_short_pct":4.6,"upside_mid_pct":8.8,"denominator_disputed":false,"denominator_note":"調整後與 GAAP 口徑差距小（FY2025 GAAP 稀釋 EPS 15.61，公司稱 FY2026 指引年增 14%，隱含調整後基期約 15.7）；分母的真正爭點是利潤率是否在週期高點，已反映在偏貴結論與 Bear 情境，不另標爭議"}}},"q6_how_wrong":{"verdict":"最可能看錯兩處：一是 2027–2028 年收益率被加勒比運力與消費降溫壓到 1% 以下；二是 EPS 達標但自由現金流長期只剩淨利三成、靠舉債回饋股東","reasoning":"三視角反證寫在反證紀錄。最大回撤推估 −40%～−60%：250 週均線 167.87 美元距現價約 −48%；Bear 五年終點約 194 美元（−40%）；淨負債約為市值 26%，衰退時槓桿放大跌幅。路徑風險偏高，但論點未破，屬深回撤心理準備，不是砍倉理由。衰退信號亮 2 項（FY2027 共識 EPS +14.1% 對營收 +7.3%；自由現金流÷淨利連 2 年低於 0.75），陷阱風險中等。反例：若 2027 年運力成長降到 4.5% 後資本支出明顯下降，自由現金流這一項會自然熄燈。","fact_refs":["f_ma_w250","f_ma_w52","f_ma_w104","f_net_debt_m","f_rsi14","f_peer_rcl_fcf_margin_pct","f_consensus_eps_fy2","f_rev_consensus_fy2_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"亮 2 項：EPS 成長快於營收、自由現金流轉換率偏低"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":17.9,"pe":18.01,"basis":"FY2026E 共識調整後 EPS 17.90（財年只剩約兩個月，接近實績）；終端倍數同樣套在終端當年 FY2031E，口徑一致"},"eps":{"bull":[21.0,24.4,28.0,31.8,35.6],"base":[20.4,23.0,25.5,28.0,30.5],"bear":[19.2,15.8,15.0,16.8,18.5]},"pe":{"bull":17,"base":15,"bear":10.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.71,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-40,"basis":"三個錨：250 週均線 167.87 美元距現價約 −48%；Bear 五年終點約 194 美元（−40%），路徑中途通常低於終點；淨負債約 223 億美元、約為市值 26%，衰退時盈餘下滑經槓桿放大到股價。觸發情境為消費衰退疊加加勒比降價或燃油急漲","trigger_time":null},"basis":{"bull":"2027 收益率 +3～4%、Sandals 綜效與回購加持，FY2027 21.0、之後年增 12～16%；市場持續以複利股看待，退場 17 倍","base":"FY2027 約 20.4（公司 20 美元以上說法加小幅上修），FY2028 23.0 略低於共識 23.38，之後隨運力與收益率成長放緩到年增約 9%；每股路徑已含回購效果，故淨回購殖利率填 0；退場 15 倍","bear":"2027 訂位撐住第一年，2028 年消費衰退疊加加勒比降價與燃油上漲，收益率轉負，EPS 由 19.2 跌到 15.0 再緩步回升到 18.5；倍數回到週期股低端 10.5 倍（成長熄火到 5% 的情境）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"業界新船訂單約 93 艘、對手加勒比運力大增；NCLH 預期 2027 上半年需求仍弱；有分析師質疑船上消費能否轉成 2027 票價；Q2 法說 CEO 稱消費者花錢更審慎","assumption":"2027 訂位年增高十幾%與創紀錄費率能延續到 2028","consequence":"2028 消費衰退疊加加勒比降價，淨收益率轉負、EPS 回到 15～16 美元，市場改用週期股 10～11 倍定價，五年後股價約 190 美元（−40%）","ruling":"部分採納：列為 Bear 30% 機率；不再往上調，因為 2026、2027 訂位都領先往年、費率創紀錄，12 個月內需求斷崖的證據不足。與唯一致命點部分重疊：FY2027 指引跌破 20 美元是這個故事最早能看到的訊號","watch":"FY2027 首次指引、Q1 2027 淨收益率、加勒比收益率是否轉負","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#2","end_markets#2","supply_demand_durability#4"]},{"view":"論點成功但股東經濟變差","evidence":"FY2025 自由現金流只有淨利 29%，股利已約等於自由現金流；在建新船約 165 億美元、近半以歐元計價，可建船廠少、議價權在船廠，關稅與貿易制裁可能干擾供應鏈；Sandals 30 億美元舉債收購","assumption":"2027 年後運力成長放緩、資本支出下降，自由現金流自然追上淨利","consequence":"EPS 照樣達標，但新船成本因歐元與關稅上升、Sandals 綜效延後，自由現金流長期停在淨利三到五成，回購靠舉債，股東實拿報酬低於 EPS 成長","ruling":"採納：列入資本週期假設與資本負擔風險監測；這是本次最被市場忽略的一點，也是不給更高 Base 倍數的原因之一","watch":"TTM 自由現金流÷淨利、淨負債÷調整後 EBITDA、新船訂單金額與歐元匯率","not_applicable_reason":null,"evidence_refs":["geo_supply_chain#1","reg_tariff_export#0","substitute_technology#1"]},{"view":"價格已反映太多","evidence":"現價為 FY2026E 18.0 倍、FY2027E 15.8 倍；P/S 與 EV/S 都在近 4 個年度端點最高位；26 週漲 25.7%、RSI 72.7；Freedom Capital 2026-07 降評至持有，Q3 後 Barclays、BofA 下修目標價","assumption":"市場會繼續以複利股而非週期股替 RCL 定價","consequence":"即使盈餘照共識走，倍數由 18 倍回到 15 倍就吃掉約一年半的盈餘成長，五年 Base 年化報酬只剩約 9%","ruling":"採納：這是觀望的主因，價格回到 FY2027 共識 14.5 倍（約 296 美元）以下才重啟","watch":"股價÷FY2027 共識 EPS、賣方目標價變化","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 322.5 → 本次 322.3（-0.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=322.5","side_b":"本次 price_at_dd=322.3","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 322.5 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 322.5 美元：Bull 價 646、Bear 價 170，五年期望值 +30.6%，基準年化 9.4%，不對稱比 1.8","side_b":"本次情境、股價仍用 322.5 美元：Bull 價 605.2、Bear 價 194.25，五年期望值 +28.8%，基準年化 7.2%，不對稱比 1.84","ruling":"先換情境、股價不動：五年期望值少 1.8 個百分點，基準年化少 2.2 個百分點。不對稱比由 1.8 變為 1.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 322.5 美元：五年期望值 +28.8%，基準年化 7.2%，不對稱比 1.84","side_b":"本次情境、股價 322.3 美元：五年期望值 +28.9%，基準年化 7.3%，不對稱比 1.84","ruling":"再換股價、情境不動：起點價下跌 0.1%，五年期望值多 0.1 個百分點，基準年化多 0.0 個百分點，不對稱比由 1.84 升到 1.84。合計五年期望值比前份少 1.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現在就買 vs 等價格","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Perfecta 三年 EPS 年複合約 20% 已近兌現，FY2027 本益比 15.8 倍換約 14% 的三年 EPS 成長（PEG 約 1.1），2026、2027 訂位都領先往年且費率創紀錄，利潤率同業最高、仍在擴張","side_b":"等價格的理由：現價用利潤率歷史高點的盈餘給 18 倍當年本益比，Base 五年年化約 9%、上下檔比約 1.8 屬平庸；自由現金流只有淨利約三成；RSI 72.7 偏熱；加勒比對手運力大增、收益率成長已放緩到約 2%","ruling":"不可調和（買或等，方向相反），選等價格。依據：上檔不足以補償 30% 機率的 Bear（五年 −40%）；硬數據點是 FY2027 本益比 15.8 倍對比重啟門檻 14.5 倍。執行上用價格解：價格到位就買，證據先轉壞就延後","evidence_level":"事實表數字＋公司財報指引（一手）","settle_metric":"股價÷FY2027 共識 EPS；2027-01 底 FY2027 首次指引","if_then":["若股價跌到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）且基本面無損，則重跑判斷、分批反買，首筆不超過目標倉位三分之一","若股價續漲但 FY2027 指引尚未公布，則不追","若 FY2027 首次指引中值低於 20 美元，則不追，重啟價位改為新指引中值的 12 倍","反向條件（等待證實為錯）：若 2027-04 Q1 財報淨收益率（固定匯率）扣除約 200 個基點逆風後仍 ≥ +2%，且全年指引中值 ≥ 20.5 美元，則把重啟倍數上調到 15.5 倍（約 317 美元）重跑判斷"],"evidence_refs":["capital_markets_pricing#3","end_markets#0"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2026-07-28 Q2 法說：CEO 稱 2027 訂位與往年相當、價格創紀錄，消費者花錢更審慎、偏好近程；CFO 預告 Q3 淨收益率約持平、全年 EPS 17.73～17.87","side_b":"2026-10-27 Q3 法說：Q3 淨收益率 +0.6%，高於指引約 60 個基點，EPS 6.57 高於指引中點 0.26；CEO 改稱 2027 訂位領先往年、2027 航次訂位年增高十幾%；但分析師追問「高十幾%」是年增還是季增時，CEO 未正面回答","ruling":"可調和：財測兌現紀錄良好（全年 EPS 指引上調到 17.85～17.95，回到年初中點 17.90），採信方向；但「高十幾%」口徑不明，標為未證、以 Q1 2027 淨收益率驗證","evidence_level":"公司法說逐字稿（一手）","settle_metric":"Q1 2027 淨收益率（固定匯率）扣除約 200 個基點結構性逆風後是否為正","if_then":["若 Q1 2027 淨收益率（固定匯率）< 0%，則視 2027 訂位說法落空，Bear 機率上調到 35%"],"evidence_refs":["end_markets#1","supply_demand_durability#0"]},{"axis":"訂位量與收益率","cause":null,"prior_field":null,"side_a":"訂位：自上次法說以來訂位量年增中段十幾%、2027 航次訂位年增高十幾%，費率創紀錄","side_b":"收益率：Q3 淨收益率僅 +0.6%（固定匯率），報表口徑毛利收益率 −0.8%；全年約 +2.1%，低於年初區間 1.5–3.5% 的中點；NCLH 預期 2027 上半年需求仍弱","ruling":"可調和（程度差異）：量的成長大部分來自運力與短航程產品，單價成長溫和；Base 只給 2027 收益率 +2～3%","evidence_level":"公司財報＋同業說法","settle_metric":"FY2027 淨收益率指引","if_then":["若 FY2027 淨收益率指引 < +1%，則重啟價位下修到 FY2027 EPS 13 倍"],"evidence_refs":["supply_demand_durability#0","end_markets#4","supply_demand_durability#4","end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：NCLH 2026 加勒比運力 +55%、MSC +23%，業界訂單約 93 艘、22.95 萬床位，區域競爭惡化中","side_b":"結構：大型船廠排到 2036、2027 年約 15 艘交付，全球供給受限；其他結構變數：Sandals 擴到全包式度假村、私人目的地 2028 年前增至 8 個，通路仍倚重旅行顧問，未見反壟斷行動","ruling":"雙向拉鋸：加勒比區域競爭惡化與全球供給受限同時成立，前者壓 2026–2027 收益率，後者撐長期定價地板","evidence_level":"產業媒體＋CLIA＋公司 10-K","settle_metric":"加勒比收益率方向、年度新船交付艘數","if_then":["若全業界年交付超過 16 艘，則供給受限論點削弱、Base 退場倍數降到 13.5 倍"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","competitive_share_entrants#2","channel_business_model_shift#1"]},{"axis":"估值、評級與機率（股價幾乎未動）","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-29，股價 322.5）：估值偏貴、整體評級 B、Bull／Bear 機率 25%／30%、最大回撤 −60%、觀望","side_b":"本次（股價 322.3）：估值偏貴、整體評級 B、機率 25%／45%／30%、最大回撤範圍 −40%～−60%","ruling":"股價幾乎不變；FY2027 共識上修約 2% 讓 FY2027 本益比由 16.1 倍降到 15.8 倍，幅度不足以改變估值結論。機率維持，因 Q3 的利多（指引上調、訂位領先）與利空（收益率放緩、對手運力大增）互相抵銷。裁決與角色由程式依本輪輸入重算","evidence_level":"事實表價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：護城河方向擴大（↑）","side_b":"本次：穩定（→）","ruling":"新證據：營益率擴張幅度由每年 2～4 個百分點降到 0.2（FY2025 27.4%→TTM 27.6%）；FY2026 淨收益率約 +2.1%，低於年初區間中點，Q3 報表口徑毛利收益率 −0.8%；2026 加勒比對手運力 NCLH +55%、MSC +23%。執行面仍擴大，定價面轉穩定，合判穩定","evidence_level":"公司財報＋產業媒體","settle_metric":"TTM 營業利益率、FY2027 淨收益率","if_then":["若 FY2027 淨收益率 ≥ +3% 且營益率再擴張 1 個百分點以上，則方向回調為擴大"],"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2","end_markets#4"]},{"axis":"價值陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份：價值陷阱風險低（🟢）","side_b":"本次：中等（🟡），十項衰退信號逐條檢查亮 2 項","ruling":"前份未逐條套用衰退信號清單；本次逐條檢查：EPS 成長快於營收（FY2027 共識 EPS +14.1% 對營收 +7.3%，差 6.8 個百分點）與自由現金流÷淨利連 2 年低於 0.75（FY2024 0.69、FY2025 0.29）兩項亮燈。後者主因新船資本支出、屬成長投資，但仍真實壓低股東可拿的現金，故由低調到中等","evidence_level":"年度財報＋共識快照","settle_metric":"FY2027 自由現金流÷淨利","if_then":["若 FY2027 自由現金流÷淨利 ≥ 0.6，則該項熄燈、陷阱風險回到低"],"evidence_refs":[]},{"axis":"跑道、類型與循環位置","cause":"新證據","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份：中長期跑道寬（🟢）、品質複利成長型、晚循環","side_b":"本次：三項判斷維持，次要類型另標循環型","ruling":"Q3 新證據支持維持：Sandals 全包式度假村（CEO 稱可觸及度假支出由 20～25% 擴到約 50%）、河輪 2027 開航、私人目的地 2028 年前增至 8 個，是有來源的第二條曲線；利潤率在高點、收益率成長放緩，仍屬晚循環。次要類型標循環型，反映自由現金流與景氣敏感度","evidence_level":"公司法說（一手）","settle_metric":"Sandals 交割後權益法收益、會員占比","if_then":["若 Sandals 交割延後超過 2027 年底或認列減損，則跑道下修一檔"],"evidence_refs":["substitute_technology#2","channel_business_model_shift#1"]},{"axis":"重啟進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","side_b":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）才重啟進場；倍數沿用前份，價位隨共識上修由 290 上移","ruling":"倍數門檻 14.5 倍不變；FY2027 共識由前份的 20.01 上修到 20.43，對應重啟進場價位由約 290 美元上移到約 296 美元","evidence_level":"共識快照","settle_metric":"股價÷FY2027 共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"假設門檻","cause":"新證據","prior_field":null,"side_a":"前份：FY2026 調整後 EPS ≥ 17.73 美元（當時指引下緣）；FY2027 ≥ 20.0","side_b":"本次：FY2026 ≥ 17.85 美元（2026-10-27 上調後指引下緣）；FY2027 ≥ 20.0 不變","ruling":"公司兩度上調指引，門檻隨新指引下緣上移","evidence_level":"公司財報新聞稿","settle_metric":"FY2026 實績","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 補設","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（null）","side_b":"2027 年 1 月底 Q4 財報給出的 FY2027 首次調整後 EPS 指引中值低於 20 美元","ruling":"本次補設：FY2027 指引跌破 20 美元會同時打到盈餘與退場倍數，是數學上最大的單一敏感項","evidence_level":"公司法說（一手）","settle_metric":"FY2027 首次指引中值","if_then":["若指引中值 < 20 美元，則撤出進場名單、重啟價位改為新指引中值的 12 倍"],"evidence_refs":[]},{"axis":"清倉／減碼門檻（kill 指標）","cause":"方法變動","prior_field":null,"side_a":"前份未設 kill 指標（null）；前份 H2 反轉條件為 FY2027 共識跌破 18.5 美元","side_b":"本次四條：FY2027 首次指引中值 < 19 美元；FY2027 淨收益率 < +1%；FY2027 共識跌破 18.5 美元；Sandals 交割後淨負債÷調整後 EBITDA > 3.5 倍。持有中觸發任一即減碼一半、兩條以上清倉；未持有則撤出進場名單","ruling":"補上可監測的出場門檻；18.5 美元共識底線沿用前份，其餘三條為本次新增","evidence_level":"公司財報＋共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 本益比回到 14.5 倍以下才重啟進場","type":"估值rearm","maps_to":"H1","metric":"股價÷FY2027 共識調整後 EPS","threshold":"≤ 14.5 倍（現約 296 美元）","action":"重跑判斷；通過後分批反買，首筆不超過目標倉位三分之一","source_freq":"每日股價、每月共識快照","date":null,"evidence_refs":["capital_markets_pricing#4"]},{"n":2,"text":"FY2027 首次指引中值跌破 20 美元","type":"Single Thing","maps_to":"H1","metric":"公司 FY2027 調整後 EPS 指引中值","threshold":"< 20.0 美元","action":"撤出進場名單；重啟價位改為新指引中值的 12 倍；H1 判反轉","source_freq":"Q4 2026 財報一次","date":"2027-01"},{"n":3,"text":"營業利益率領先失守","type":"假設驗證","maps_to":"H2","metric":"TTM 營業利益率","threshold":"連 4 季 < 26.2% 削弱；連 6 季 < 24.8% 反轉","action":"削弱時 Base 退場倍數由 15 倍降到 13.5 倍重算；反轉時改以週期股框架重做判斷","source_freq":"每季財報","date":null},{"n":4,"text":"自由現金流追不上淨利","type":"假設驗證","maps_to":"H3","metric":"自由現金流÷淨利","threshold":"FY2027 < 0.5","action":"Bear 機率上調到 35%，重啟價位改為 FY2027 EPS 13.5 倍","source_freq":"年度財報、每季現金流量","date":"2028-02"},{"n":5,"text":"加勒比降價擴散到全年收益率","type":"風險","maps_to":"R1","metric":"全年淨收益率（固定匯率）","threshold":"FY2027 指引 < +1%，或公司稱加勒比收益率轉負","action":"Bear 機率上調到 35%；重啟價位下修到 FY2027 EPS 13 倍","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":6,"text":"地緣或燃油再度迫使下修指引","type":"風險","maps_to":"R2","metric":"全年 EPS 指引因地緣或燃油下修幅度","threshold":"單季下修 ≥ 3%，連 2 季","action":"不追；若已持有則減碼三分之一","source_freq":"每季財報、燃油遠期曲線","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","end_markets#2"]},{"n":7,"text":"資本負擔超出投資級框架","type":"風險","maps_to":"R3","metric":"淨負債÷調整後 EBITDA","threshold":"Sandals 交割後 > 3.5 倍","action":"Bear 機率上調到 35%；若已持有則減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#1","substitute_technology#1","reg_tariff_export#0"]},{"n":8,"text":"目的地或訴訟出現不利定案","type":"風險","maps_to":"R4","metric":"Mahahual 開發狀態；Havana Docks 案最高法院判決","threshold":"Mahahual 正式停建，或最高法院恢復原判且衍生其他古巴航線索賠","action":"重估西加勒比部署與法律負債；涉及集體索賠時暫停進場計畫","source_freq":"法說、8-K、法院判決","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#1","lawsuit_class_action#0"]},{"n":9,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"FY2027 首次指引與 2027 訂位進度","threshold":"財報公布後一週內","action":"重跑完整判斷","source_freq":"一次","date":"2027-02-05"}],"kill_metrics":[{"metric":"公司 FY2027 調整後 EPS 首次指引中值","bear_threshold":"< 19.0 美元（比共識 20.43 低約 7%）","window":"2027-01 底 Q4 2026 財報","source":"公司財報新聞稿（8-K）","last_status":"unknown"},{"metric":"全年淨收益率成長（固定匯率）","bear_threshold":"FY2027 指引或實績 < +1.0%","window":"2027 全年，按季追蹤","source":"公司季報與法說","last_status":"ok"},{"metric":"FY2027 共識調整後 EPS","bear_threshold":"跌破 18.5 美元","window":"滾動 2 季","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"淨負債÷調整後 EBITDA","bear_threshold":"> 3.5 倍","window":"Sandals 交割後每季","source":"公司季報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）才重啟進場；倍數沿用前份，價位隨共識上修由 290 上移","exec_line":"未持有，不追；到價先重跑判斷，再分批進場，首筆不超過目標倉位三分之一；FY2027 首次指引跌破 20 美元則撤出進場名單"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）","qc48_result":"pass","qc48_note":"RCL 的爆發情境缺少「運力 × 收益率 → 營收 → EPS」的逐步算術，第二條成長曲線（Sandals）真實存在，但還沒有可驗證的營收或盈餘數字。這些依據大多只能算作未證實，本次沒有發現足以否定的反證。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=25.65, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='RCL 的爆發情境缺少「運力 × 收益率 → 營收 → EPS」的逐步算術，第二條成長曲線（Sandals）真實存在，但還沒有可驗證的營收或盈餘數字。這些依據大多只能算作未證實，本次沒有發現足以否定的反證。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Perfecta 收尾兌現：FY2027 調整後 EPS 達 20 美元以上，靠運力 +4.5%、淨收益率溫和成長與成本紀律，不靠 Sandals 與回購","2y":"FY2027 調整後 EPS ≥ 20 美元、淨收益率（固定匯率）≥ +2%","5y":null,"10y":null,"threshold":"FY2026 調整後 EPS ≥ 17.85 美元（新指引下緣）；FY2027 ≥ 20.0 美元；FY2027 淨收益率（固定匯率）≥ +2%","source":"公司 Q3 2026 財報新聞稿與 2026-10-27 法說（CEO 稱依目前燃油遠期曲線 2027 年可達 20 美元以上，且不含 Sandals、回購、再融資）；FY2027 共識 20.43（Koyfin 快照 2026-10-31）","drift_rule":"FY2027 共識或公司指引連 2 季比 20.43 低 5% 以上→削弱；連 3 季低 10% 以上（約 18.4）→反轉"},{"id":"H2","text":"利潤率領先能守住：全球船廠產能受限壓住新增供給，加上硬體與私人目的地差異化，RCL 營業利益率維持同業最高","2y":null,"5y":"2031 年前 TTM 營業利益率不低於 24.8%，且對 CCL 差距 ≥ 8 個百分點","10y":null,"threshold":"TTM 營業利益率 ≥ 26.2%（現值 27.6% 的 95%）為健康，< 24.8% 為反轉線；對 CCL 營益率差距 ≥ 8 個百分點（現 11.6）；全業界年交付 ≤ 16 艘","source":"事實表同業對照（yfinance TTM）；CLIA 稱大型船訂單排到 2036；Cruise Industry News 2026 年訂單簿更新","drift_rule":"TTM 營益率連 4 季低於 26.2%（偏離現值 5%）→削弱；連 6 季低於 24.8%（偏離 10%）→反轉"},{"id":"H3","text":"資本週期轉正：新船交付放緩後，自由現金流追上淨利，股東回饋不再靠舉債","2y":null,"5y":"FY2028 自由現金流÷淨利 ≥ 0.6，Sandals 交割後淨負債÷調整後 EBITDA ≤ 3 倍","10y":null,"threshold":"FY2027 自由現金流÷淨利 ≥ 0.5、FY2028 ≥ 0.6（FY2025 為 0.29）；淨負債÷調整後 EBITDA ≤ 3.0 倍","source":"年度財報（事實表 financial_history，yfinance FY2023–FY2025）；FY2026 前 9 個月現金流量（Q3 財報）；2026-10-27 法說 CFO 稱槓桿低於 3 倍、2027 運力 +4.5%","drift_rule":"TTM 自由現金流÷淨利連 4 季低於 0.45→削弱；連 6 季低於 0.4→反轉"},{"id":"H4","text":"度假錢包份額擴大：跨品牌會員、河輪與 Sandals 把客戶留在體系內，郵輪之外長出第二條曲線","2y":null,"5y":null,"10y":"會員占旅客比例由 40% 升到 50% 以上；Sandals 權益法收益與管理層所稱數億美元綜效逐年兌現","threshold":"會員占比 ≥ 40% 且逐年上升；Sandals 交割後兩年內權益法收益進入指引且未認列減損","source":"2026-10-27 法說（CEO：40% 旅客為會員、約一半為回頭客、目前只拿到客人年度度假支出 20～25%，加入全包式度假村後可觸及約 50%）","drift_rule":"會員占比連 2 個年度未上升→削弱；連 3 個年度下降或 Sandals 認列減損→反轉"}],"R":[{"id":"R1","text":"加勒比運力集中投放引發降價：NCLH 2026 加勒比運力 +55%、MSC +23%，業界新船訂單約 93 艘、22.95 萬床位，RCL 運力 57% 在加勒比","h_ref":"H2","clock":"🔥","threshold":"FY2027 淨收益率（固定匯率）指引 < +1%，或公司稱加勒比收益率轉負","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2"]},{"id":"R2","text":"地緣事件與燃油：中東衝突壓抑歐洲航程，2026-07 營收成長指引由 10% 降到約 9%；2026-04 曾因燃油把全年 EPS 指引中點由 17.90 下修到 17.30；歐洲占 2027 運力 16%","h_ref":"H1","clock":"⚡","threshold":"單季因地緣或燃油下修全年 EPS 指引 ≥ 3%，連 2 季發生","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","end_markets#2"]},{"id":"R3","text":"資本負擔吃掉股東經濟：在建新船約 165 億美元、約 49.9% 成本為歐元，可建船廠只有少數幾家，關稅與貿易制裁可能干擾供應鏈；再加上 Sandals 約 30 億美元舉債收購","h_ref":"H3","clock":"🔥","threshold":"淨負債÷調整後 EBITDA > 3.5 倍，或 FY2027 自由現金流÷淨利 < 0.4","evidence_refs":["geo_supply_chain#1","substitute_technology#1","reg_tariff_export#0"]},{"id":"R4","text":"目的地與法律風險：Mahahual 開發時程受影響且管理層兩季不評論；Havana Docks 案（原判約 1.12 億美元已被上訴法院推翻）最高法院 2025-10 受理，結果事實表未涵蓋","h_ref":"H2","clock":"🐢","threshold":"Mahahual 正式停建，或最高法院恢復原判且衍生其他古巴航線索賠","evidence_refs":["regulatory_antitrust#0","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"2027 年 1 月底 Q4 財報給出的 FY2027 首次調整後 EPS 指引中值低於 20 美元","why_fatal":"20 美元是市場把 RCL 從週期股改看成複利股的錨；共識 20.43 已在其上，跌破代表 FY2027 下修 5% 以上、FY2028 共識 23.38 跟著下修，同時退場倍數往週期股區間回落，兩者疊加估值約下修 25～30%（推估：盈餘 −5%、倍數 18 倍→14 倍）","if_happens":"撤出進場名單，重啟價位改為新指引中值的 12 倍；Perfecta 假設判反轉，利潤率領先假設重估","how_monitor":"Q4 2026 財報（預計 2027-01 底至 02 初）的 FY2027 指引；期間看每月共識快照、燃油遠期曲線與避險比例（Q4 2026 避險 58%）","probability":"約 15%（12–24 個月）：2026 與 2027 訂位進度領先往年且費率創紀錄，CEO 稱依目前燃油遠期曲線可達 20 美元以上；主要變數是燃油與匯率"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.78,"peg_fy2":1.1,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":15.61,"FY2026E":17.9,"FY2027E":20.43,"FY2028E":23.38},"fy_end_month":12,"eps_basis":"共識為調整後 EPS（Koyfin 快照 2026-10-31；共識營收為 yfinance 25 位分析師）；FY2025A 用 GAAP 稀釋 EPS 15.61（年度財報），公司稱 FY2026 指引年增 14%，隱含調整後基期約 15.7，差距約 0.6%"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 首次指引","impact":"高","watch":"調整後 EPS 指引中值是否 ≥ 20 美元、淨收益率指引是否 ≥ +2%"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"Sandals 與 Beaches 50% 股權交割（約 30 億美元、舉債支應）","impact":"中","watch":"交割後淨負債÷調整後 EBITDA、權益法收益何時納入指引"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"Q1 2027 財報（公司預告 Q1 約 200 個基點結構性逆風）","impact":"中","watch":"Q1 淨收益率扣除逆風後是否仍為正"}]}
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
