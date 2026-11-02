你是 DD 管線 v20 的判斷層閘（gate），標的 CLS（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝5829.7 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi1_non_gaap_adjusted_operat`（q1_business）｜Non-GAAP 營業利益率（adjusted operating margin）＝8.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝460.0 百萬美元（利益率 7.9%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi5_q4_2026`（q1_business）｜Q4 2026 指引＝營收 6,275–6,575 百萬美元；adjusted EPS $3.37–3.57；adjusted 營業利益率中位數 8.7% 區間｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi6_2026`（q1_business）｜全年 2026 指引（上調）＝營收 21.0B（前 20.5B）；adjusted EPS 11.55（前 11.30）；adjusted 營業利益率 8.4%（不變）；FCF 460 百萬美元（前 600，下調） 全年｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi7_2027`（q1_business）｜全年 2027 首次指引＝營收 40.0B；adjusted EPS 21.50；adjusted 營業利益率 9.0%；capex 1.5–2.0B 全年｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：consensus FY2 EPS 22.31（來源：numbers_extra.json consensus_revision，2026-10-31 快照）
- `f_peer_cls_gross_margin_pct`（q2_moat）｜CLS 毛利率＝11.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cls_operating_margin_pct`（q2_moat）｜CLS 營業利益率＝8.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cls_fcf_margin_pct`（q2_moat）｜CLS FCF 利潤率＝2.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_flex_operating_margin_pct`（q2_moat）｜FLEX 營業利益率＝5.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FLEX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_flex_fcf_margin_pct`（q2_moat）｜FLEX FCF 利潤率＝3.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FLEX.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jbl_operating_margin_pct`（q2_moat）｜JBL 營業利益率＝5.11 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_jbl_fcf_margin_pct`（q2_moat）｜JBL FCF 利潤率＝3.82 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_sanm_operating_margin_pct`（q2_moat）｜SANM 營業利益率＝5.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sanm_fcf_margin_pct`（q2_moat）｜SANM FCF 利潤率＝4.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2317_tw_gross_margin_pct`（q2_moat）｜2317.TW 毛利率＝6.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2317.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2317_tw_operating_margin_pct`（q2_moat）｜2317.TW 營業利益率＝3.51 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2317.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2317_tw_fcf_margin_pct`（q2_moat）｜2317.TW FCF 利潤率＝-0.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2317.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝11.59 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝22.31 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝31.99 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝1.94 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（31.38 → 31.99）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝21039.53 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝40193.48 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_non_gaap_fcf`（q4_capital）｜自由現金流（non-GAAP FCF）＝127.5 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）；營業現金流 389.7、資本支出淨額 262.2（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝4.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K 附件 https://www.sec.gov/Archives/edgar/data/0001030894/000103089426000049/cls-20260930prcondensedfs.htm（Q3 2026 Financial Results，2026-10-26）；員工 SBC 21.3 百萬美元／GAAP 營業利益 460.0 百萬美元（本 agent 換算；占營收約 0.4%）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-26））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2932.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 1031.1、現金 3963.1（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝126.11 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝259.12 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝22.36 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 11.59，分子＝快照價 259.12｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝24.45 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝45.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝45.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.63 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝53.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝53.1 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.41 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-38.41 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.85 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 11.38 → 11.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟢｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 254.56 / W52 322.92 / W104 236.11 / W250 113.03 / W250 13週斜率 3.82%」
- `f_rsi14`（q5_valuation）｜RSI(14)＝36.66｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝322.92 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝236.11 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（17 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 指出 CCS 競爭仍非常激烈，資料中心支出集中於大型雲端/AI 客戶，導致 EMS 積極競標、ODM 加強搶份額。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素：客戶過去與未來可能把業務轉給競爭者、實施 in-source 與 second-source 計畫，或調整供應商集中度。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K：關稅下客戶可能以 insourcing 或轉移給其他供應商來規避成本，影響可能重大。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：Q2 2026 10-Q：三位客戶（皆屬 CCS）各占營收 10% 以上，為 32%、17%、14%。
  - 來源：SEC EDGAR 10-Q Q2 2026（經搜尋摘要）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：Q4 2025 財報電話會議：管理層稱 Google TPU 專案 Celestica 並非唯一來源，超大型客戶通常保留第二供應商，Celestica 仍為主要來源（搜尋摘要轉述，未逐字）。
  - 來源：MarketBeat Celestica Q4 earnings call highlights（as_of 2026-01-29）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前十大客戶占營收79%（2024 73%、2023 64%）；三家客戶各占10%以上（32%、14%、12%），均在CCS部門。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K風險因素：失去任一重要客戶可能對營運結果造成重大不利影響；無法保證降低客戶集中度的努力成功；CCS占2025合併營收74%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年Enterprise終端市場營收年減19%，原因為一家超大規模客戶AI/ML運算專案的技術轉換，顯示單一客戶專案轉換已造成實際營收波動。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-27）｜affects：thesis.R、moat_trend
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：Q2 2026前三大客戶合計占營收63%，最大客戶占32%；集中度與存貨風險上升。
  - 來源：Panabee Celestica Q2 2026 earnings summary（as_of 2026-07-28）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Celestica 稱零組件供應是主要限制，但認為 2026 承諾與 2027 展望已適當避險。
  - 來源：MarketBeat: Celestica Q2 earnings call highlights（as_of 2026-07-28）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美中貿易爭端已造成關稅上升；Capital Equipment 業務與 CCS 部門過去且可能持續受美國對中國等國的技術/資料出口管制負面影響
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：美國對特定先進運算半導體晶片的出口管制已對並持續對 Capital Equipment 與 CCS 造成不利影響；未來衝擊可能重大
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：關稅影響無法量化但可能重大，取決於客戶是否持續吸收關稅或轉單
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Celestica 10-Q 風險因素點名美中緊張、中台緊張、俄烏與中東衝突及關稅政策為地緣曝險；據來源摘要，營運據點分布北美、亞洲、歐洲，未見分國產能占比。
  - 來源：SEC Form 10-Q (period ended 2026-09-30)（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2026 展望已計入客製矽、記憶體、高層數 PCB 的交期拉長；10-Q 警告短缺可能導致無法及時交貨或須以較差條件向第三方採購。未查到單一來源料件明細。
  - 來源：Celestica 2026 outlook / 10-Q 風險因素（經 itiger、Motley Fool Canada 轉述）（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子列出客戶面臨技術快速變化（含 AI 演進）、替代品出現、低成本與開源 AI 模型競爭，可能限制客戶 AI 相關產品定價；屬一般性風險揭露，未點名特定替代技術取代 CLS 產品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `ems_utilization_capex_cycle#0`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：Celestica 2026 capex 預期約 $1 億美元級的 $10 億（約營收 6%），2025 為 $2.01 億；新產能 2026–2027 陸續開出，含德州 Richardson 擴建與 Fort Worth 新廠（2027 上線）、泰國擴建
  - 來源：Celestica Q4 2025 earnings call highlights / 8-K (search summary)（as_of 2026-01-29）｜affects：valuation、decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":867.0,"bear_5y_price":144.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":75.6,"ev5y_pct":79.3,"irr_base_pct":11.9,"asym_ratio":4.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":11.59,"pe":22.36,"basis":"FY1（FY2026E）調整後 EPS 共識 11.59，現價 259.12；終端倍數同為前瞻一年口徑"},"eps":{"bull":[23.5,35.0,42.0,47.0,51.0],"base":[22.0,28.5,31.0,33.0,35.0],"bear":[19.0,13.0,10.5,11.0,12.0]},"pe":{"bull":17,"base":13,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":-0.3},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CLS_Q1_2026_Earnings_Call_20260428.md
- 2026-04-28｜CFO｜guidance：CFO 給 Q2 營收區間 41.5～44.5 億美元（原話："be between $4.15 billion and $4.45 billion"）
- 2026-04-28｜CFO｜margin：Q2 non-GAAP 營業利益率以中點計預期 8.0%（原話："8.0%, which would represent an increase of 60 basis points"）
- 2026-04-28｜CEO｜guidance：CEO 將 2026 全年營收展望由 170 億上調至 190 億美元（原話："raising our revenue outlook from $17 billion to $19 billion"）
- 2026-04-28｜CEO｜guidance：全年調整後 EPS 展望上調至 10.15 美元（原 8.75）（原話："our outlook for adjusted EPS and from $8.75 to $10.15"）
- 2026-04-28｜CEO｜margin：全年調整後營業利益率展望 8.1%，高於先前 7.8%（原話："an adjusted operating margin outlook of 8.1%"）
- 2026-04-28｜CEO｜guidance：自由現金流展望維持 5 億美元，已含 10 億資本支出（原話："we are reaffirming our free cash flow outlook of $500"）
- 2026-04-28｜CEO｜commitment：CEO 稱 2026 展望為高信心觀點（原話："This outlook represents our high confidence view for 2026"）
- 2026-04-28｜CEO｜guidance：2027 營收成長預期顯著高於 2026 的 65 億美元增量，未給具體數字（原話："grow revenue significantly more than this in 2027"）
- 2026-04-28｜CFO｜guidance：CFO 說明 2027 營收下限約 255 億美元，且實際看到更高（原話："would be somewhere around $25.5 billion"）
- 2026-04-28｜CEO｜guidance：CCS 全年營收成長預期約 70%（原話："we now anticipate approximately 70% revenue growth"）
- 2026-04-28｜CEO｜guidance：ATS 全年營收展望上調為中至高個位數成長（原話："mid- to high single-digit percentage growth"）
- 2026-04-28｜CFO｜margin：Q1 CCS 分部利益率 8.6%，歸因於產品組合與營運槓桿（原話："CCS segment margin in the first quarter was 8.6%"）
- 2026-04-28｜CFO｜margin：Q1 ATS 分部利益率 6.0%，歸因於組合優化（原話："ATS segment margin was 6.0%, up 100 basis points"）
- 2026-04-28｜CFO｜margin：Q1 調整後毛利率 11.3%（原話："Adjusted gross margin was 11.3%, up 30 basis points"）
- 2026-04-28｜CFO｜margin：CFO 表示毛利率目標為維持或提升，並承認長期有輸入成本逆風（原話："we definitely are looking to maintain, if not grow"）
- 2026-04-28｜CFO｜margin：CFO 指出記憶體與矽等輸入成本大幅上升，構成毛利率逆風（原話："some input costs that are going up materially"）
- 2026-04-28｜CEO｜risk：CEO 稱元件短缺較 90 天前更嚴重（原話："more component shortages now than 90 days ago."）
- 2026-04-28｜CEO｜risk：CEO 點名受配給的物料為客製矽與記憶體（原話："on allocation are custom silicon and memory."）
- 2026-04-28｜CFO｜risk：Q1 企業端營收略低於展望，原因為部分元件限制（原話："gated by select component constraints"）
- 2026-04-28｜CEO｜risk：CEO 表示 Q1 AI/ML 運算專案問題屬物料供應而非需求（原話："It was actually a material supply issue."）
- 2026-04-28｜CEO｜risk：供應端緊俏被描述為正在「節制」成長速度（原話："environment, effectively pacing our growth"）
- 2026-04-28｜CEO｜commitment：CEO 稱已與供應商取得支撐展望的供貨承諾（原話："we have commitments from all our suppliers"）
- 2026-04-28｜CEO｜commitment：CEO 稱與客戶的訂單多為 NCNR，提供合約保護（原話："supported by our customers are NCNR"）
- 2026-04-28｜CEO｜customer：CEO 稱已在接 2028 年出貨的訂單（原話："actually booking awards right now"）
- 2026-04-28｜CFO｜customer：Q1 有三家客戶各占營收至少 10%（35%、15%、15%）（原話："three customers that each accounted for at least 10%"）
- 2026-04-28｜CEO｜customer：CPO 交換器訂單來自既有客戶（原話："it's an existing customer"）
- 2026-04-28｜CEO｜commitment：CPO 交換器量產時間為 2027 下半年（原話："this will be second half of 2027"）
- 2026-04-28｜CEO｜product：CEO 稱此為首個使用 Broadcom 方案的大規模 CPO 量產部署（原話："production scale deployment of co-packaged optics"）
- 2026-04-28｜CEO｜margin：CEO 稱 CPO 專案利益率落在公司一般水準的高端（原話："on the higher end of what we typically do"）
- 2026-04-28｜CEO｜product：CEO 自述已上移價值鏈成為共同設計夥伴（原話："a sophisticated codesign partner"）
- 2026-04-28｜CEO｜product：1.6T 有 10 個進行中專案，2027 大量放量（原話："in terms of 1.6T we have 10 active programs"）
- 2026-04-28｜CEO｜product：與 AMD 合作的 Helios 交換器預計年底有初期樣品（原話："we expect initial units to be"）
- 2026-04-28｜CEO｜product：Helios 2027 年營收可能受矽供應而非需求所限（原話："silicon availability than by end market demand"）
- 2026-04-28｜CEO｜commitment：數位原生機櫃專案樣品今年出貨，2027 Q1 末量產（原話："We're shipping sample systems this year"）
- 2026-04-28｜CFO｜product：ATS 資本設備被描述為進入新循環（原話："now is entering into a very nice cycle"）
- 2026-04-28｜CEO｜competition：CEO 回答市占：未見重大變化（原話："We haven't seen a significant change in market share shifts"）
- 2026-04-28｜CEO｜competition：CEO 稱供應緊俏環境下的搶市占機會目前尚未出現（原話："We haven't necessarily seen that as of yet"）
- 2026-04-28｜CFO｜product：設計工程師約 1,350 人，年底將更多，R&D 支撐 HPS（原話："We have about 1,350 design engineers right now."）
- 2026-04-28｜CFO｜capital_allocation：2026 資本支出指引約 10 億美元不變（原話："guidance remains unchanged at approximately $1 billion"）
- 2026-04-28｜CFO｜capital_allocation：2027 資本支出以約 15 億美元作暫定佔位數字（原話："number of $1.5 billion as a placeholder for now"）
- 2026-04-28｜CFO｜capital_allocation：若成長需要額外資金，管理層不會猶豫（原話："we have no hesitation to do that."）
- 2026-04-28｜CFO｜capital_allocation：Q1 回購約 7.3 萬股、2,000 萬美元，態度為機會性（原話："We continue to be opportunistic with respect to share"）
- 2026-04-28｜CFO｜capital_allocation：財報後修訂信貸，循環額度增加 10 億美元至 17.5 億（原話："we amended our credit facility, increasing our revolver"）

### CLS_Shareholder_Analyst_Call_Celestica_Inc_20260519.md
- 2026-05-19｜CEO｜guidance：CEO 提到 Q1 業績後表示年初表現很強。本場無具體財測數字。（原話："we've had a very strong start to the year and"）
- 2026-05-19｜CEO｜commitment：CEO 表示對公司前景維持信心（無量化目標）。（原話："remain confident in our trajectory."）
- 2026-05-19｜CEO｜customer：CEO 稱 CCS 部門因支援超大型雲端客戶而取得顯著成長。（原話："we are capturing significant growth as we"）
- 2026-05-19｜CEO｜customer：CCS 成長來源描述為支援 hyperscaler 建置下一代資料中心基礎設施。（原話："support hyperscalers building next generation of data center"）
- 2026-05-19｜CEO｜competition：CEO 自稱為 400G／800G 乙太網路交換器的公認市場領導者。（原話："recognized market leader in 400G and 800G Ethernet switches"）
- 2026-05-19｜CEO｜product：CEO 表示正交付下一代 1.6T 交換方案。（原話："generation of 1.6T switching solutions"）
- 2026-05-19｜CEO｜customer：CEO 提及先前季度已公告的重大新專案獲標。（原話："significant new program wins we've announced"）
- 2026-05-19｜CEO｜capital_allocation：ATS 策略為工程導向，投資於專業化市場團隊與全球設計中心。（原話："investing in specialized market-focused teams and global"）
- 2026-05-19｜CEO｜commitment：CEO 結語稱成長機會仍在前方。（原話："we are just getting started"）

### CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：CFO 給 2027 全年營收展望 400 億美元。（原話："We anticipate revenue of $40 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 全年 non-GAAP 營業利益率展望 9.0%。（原話："non-GAAP operating margin is expected to be 9.0%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 調整後 EPS 展望 21.50 美元。（原話："We anticipate non-GAAP adjusted EPS of $21.50, up 86%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 營收財測區間。（原話："between $6.275 billion and $6.575 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 調整後 EPS 財測區間。（原話："between $3.37 and $3.57"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2026 全年營收展望由 205 億上調至 210 億美元。（原話："increases from $20.5 billion to $21 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2026 自由現金流展望為 4.6 億美元（原 6 億）。（原話："free cash flow outlook for 2026 is $460 million"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 營收下半年顯著高於上半年。（原話："meaningfully higher revenue in the second half"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 資本支出區間。（原話："in the range of $1.5 billion to $2.0 billion"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：Q4 Compute & Storage 終端市場成長預期約 160%。（原話："we expect growth of approximately 160%"）
- 2026-10-27｜Todd Ankenmann (CFO)｜guidance：2027 營收財測的口徑：已把斜坡、零組件供應與執行風險納入。（原話："took into consideration the risk around the ramps"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：Q3 調整後營業利益率與年增幅度。（原話："Our non-GAAP operating margin was 8.5%, up 90 basis points"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：Q3 調整後毛利率下降，管理層歸因於 CCS 產品組合。（原話："Adjusted gross margin was 11.2%, down 50 basis points"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：2027 毛利率預期維持 11% 出頭，取決於網通與運算的組合。（原話："our margins will continue in '27 in the low 11s"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：CFO 稱網通仍對毛利率有增益。（原話："networking being accretive from a margin perspective"）
- 2026-10-27｜Todd Ankenmann (CFO)｜margin：回答 H1/H2 毛利率是否不同：CFO 稱兩半年無不同動態，取決於各季組合。（原話："different gross margin dynamics in '27 between the 2 halves"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜margin：Mandeep 說明產能與電力投資使其拿下競爭對手拿不到的專案，並帶來較好的定價與毛利。（原話："allowing us to capture program wins that many of our competitors"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：CFO 表示以現有看法，目標 2028 年自由現金流轉正。（原話："target to return to positive cash flow in '28"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：CFO 稱 2027 會出現淨現金使用（自由現金流為負）。（原話："will result in a net use of cash in 2027"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：管理層稱僅依已獲專案推算的 2028 客戶需求預測高於 2027 營收展望。（原話："customer demand forecasts based solely on awarded programs"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜commitment：Mandeep 預期 2027 維持高稼動率。（原話："we do expect high utilization in 2027"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜commitment：CCS 預計 2027 研發投入超過 3 億美元。（原話："expect to invest over $300 million in 2027"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜commitment：HPS 工程師預計明年增至 2,000 人以上。（原話："grow to over 2,000 engineers by next year"）
- 2026-10-27｜Todd Ankenmann (CFO)｜commitment：管理層稱 2027 資本支出對應已獲專案，並承諾持續重新評估產能需求。（原話："we feel we've got the capacity needed with the investments"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：資本配置優先順序：有機成長優先，勝過回購。（原話："the priority and focus of our capital is on the organic growth"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：CFO 解釋更新 NCIB 的原因為加拿大每年需更新之規定。（原話："requirement to renew the program on an annual basis"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：對股東回報的態度：看時機的機會主義。（原話："opportunistic in our approach towards returning capital"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：8 月完成股權增資，CFO 稱足以應付需求。（原話："we did raise $3.5 billion of equity in August"）
- 2026-10-27｜Todd Ankenmann (CFO)｜capital_allocation：2027 約 200 億美元增量營收下，管理層投入營運資金。（原話："we are investing meaningfully in working capital"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜capital_allocation：M&A 有主動漏斗，以能力為導向。（原話："we do have an active funnel"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜competition：Mandeep 稱 1.6T/800G 專案面對的競爭者較前幾代減少。（原話："there are fewer competitors today that we are going up against"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜competition：Dorwart 承認成功會招來競爭、已有新增競爭者。（原話："it's going to invite competition"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜competition：Mandeep 對整櫃整合市場的競爭者去留說法。（原話："not all competitors will stay for the journey"）
- 2026-10-27｜Robert Mionis (CEO) / Steven Dorwart｜competition：引用第三方研究：客製乙太網路交換器營收市占率。（原話："58% share of total custom Ethernet switch revenue"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜competition：Dorwart 稱公司不必像商品化市場那樣定期爭奪份額，但份額會與客戶定期協商，客戶可能把舊產品移出。（原話："we're not in a situation of having to compete for share"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：預期 1.6T 營收明年超過 800G。（原話："1.6T revenue will surpass 800G revenue next year"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜product：已宣布的 10 個 1.6T 專案中，scale-up 與 scale-out 的拆分。（原話："4 of them are scale up and 6 of them are scale out"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：與超大規模客戶共同設計的 CPO 機櫃交換器專案，預定 2027 年底量產。（原話："production scheduled to ramp in late 2027"）
- 2026-10-27｜Gavin Cato (SVP, CCS Engineering)｜product：Gavin 稱 1.6T 世代可插拔光模組仍佔多數，CPO 要到 3.2T/400G SerDes 才更普遍。（原話："you're going to see pluggables remain in the 1.6 time frame"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：DS6010（AMD Helios scale-up 交換器）預計年底開始量產爬坡。（原話："We expect to begin ramping by the end of the year."）
- 2026-10-27｜Steven Dorwart (President, CCS)｜product：OpenAI 客製 ASIC 系統預計 2027 開始量產爬坡。（原話："It is expected to begin ramping production in 2027."）
- 2026-10-27｜Todd Ankenmann (CFO)｜customer：Q3 三家 10% 以上客戶占營收 35%、17%、14%。（原話："accounting for 35%, 17% and 14%, respectively"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：2027 運算成長的兩個主要動力為 Google TPU 與 OpenAI。（原話："relationship with Google in support of their TPU platform"）
- 2026-10-27｜Todd Ankenmann (CFO)｜customer：CFO 稱客戶資金充裕、無財務困難跡象。（原話："We see no financial distress across our portfolio."）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：Dorwart 描述漏斗主要來自既有核心客戶，並以籃子比喻客戶集中。（原話："it's not always good to have all your eggs in one basket"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜customer：Dorwart 稱商機漏斗處於歷史高位，且主要來自既有客戶。（原話："I would say it's at a historic high level"）
- 2026-10-27｜Mandeep Chawla (Group President, Global Markets)｜customer：2023–2026 超大規模客戶營收預計成長約 5 倍。（原話："grow by approximately 5x, expanding at a 71% CAGR"）
- 2026-10-27｜Steven Dorwart (President, CCS)｜risk：Dorwart 指出可能壓低數字的限制多在土地、電力與地緣政治。（原話："more in the areas of land and power"）
- 2026-10-27｜Todd Ankenmann (CFO)｜risk：Q3 存貨較上季增加 11 億美元、年增 25 億美元。（原話："a sequential increase of $1.1 billion"）

### 問答異常語氣（迴避／改口／保留）
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Goldman Sachs Michael Ng 問 2027 CCS 營收成長相對上次指引的預期，並請拆分各專案貢獻｜答法：回答「顯著更多」與 2026 年增量下限推算，未給 CCS 2027 成長率與各專案貢獻，稱之後再提供更具體數字
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：BNP Paribas Karl Ackerman 請拆分新交換器專案與 AI 伺服器的成長驅動，及對利潤率走勢的影響｜答法：列舉各專案名稱與時程，明說暫不提供細節（「more to come」），未回答利潤率軌跡
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Susquehanna Mehdi Hosseini 請量化 Helios 未來 18 個月機會及已含入 2026 目標的部分｜答法：僅稱整體市場為數十億美元級，未回答 Celestica 自身金額，也未說明是否已含入 2026 目標
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：BofA Ruplu Bhattacharya 問 2027 自由現金流與營運資金，以及 scale-up 與 scale-out 對 65 億以上增量的拆分｜答法：CFO 重申 2026 FCF 與資本紀律，未給 2027 FCF 或營運資金數字；CEO 僅確認兩類專案屬性，未拆分金額
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：Wolfe George Notter 問 CPO 訂單規模，以及是否蠶食既有營收｜答法：回答既有客戶、不蠶食及量產在 2027 下半年，未回答訂單規模
- CLS_Q1_2026_Earnings_Call_20260428.md｜問：JPMorgan Samik Chatterjee 問 CPO 交換器的內容價值與利潤率｜答法：未給單機內容價值數字，利潤率只稱位於一般水準高端
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：JPMorgan（Cardoso）要求給 2027 淨現金使用的範圍與現金週期天數｜答法：CFO 未給範圍或週期天數，改談 2026 FCF 下修、8 月增資足夠、2028 年目標轉正。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BNP（Ackerman）問交換器複雜度提升對毛利率的貢獻，以及伺服器/L11 毛利率能否改善｜答法：Dorwart 只答公司能選擇專案、毛利為考量因素，話說到一半被 CFO 接手；CFO 改談毛利率 11% 出頭與營業槓桿，未直接回答伺服器或 L11 毛利。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BofA（Bhattacharya）問現有廠區能支撐多少營收｜答法：CFO 明確表示不給與產能掛鉤的營收數字，只說 2027 投資足以支撐 2027 與 2028 需求。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：BofA（Bhattacharya）問回購是否主要用來抵銷股權激勵，或可能成為有意義的資本回報｜答法：CFO 未直接回答抵銷股權激勵與否，只說時機看機會、優先有機成長、更新 NCIB 是加拿大年度規定。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：Canaccord（Young）問稼動率相關歷史量化數字與維持高稼動率對達成 9% 營益率的重要性｜答法：Mandeep 未給任何量化稼動率數字，只說高稼動率是刻意經營，並說 2027 預期高稼動率。
- CLS_Analyst_Investor_Day_Celestica_Inc_20261027.md｜問：RBC（Treiber）問供應可得性是否比設計能力更重要，以及完整機櫃方案的競爭者是否變少｜答法：Dorwart 未直接回答兩者何者較重，承認有新增競爭者；Mandeep 補充稱 1.6T/800G 競爭者較少，但舉例仍以性質描述為主。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 4 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |
| ems_utilization_capex_cycle | found | 4 | 3 |
| ems_roic_asset_turnover_benchmark | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 機架級「設計+製造」是結構性能力，非純週期需求；hyperscaler 不會在 36 個月內大規模自建或全面切換 ODM","columns":{"2Y 驗證點":"1.6T 兩家 hyperscaler 2H2026 量產如期；custom switch 份額守住 ~55%","5Y 驗證點":"CCS 段仍為多數 hyperscaler 網路/運算平台的量產夥伴","10Y 驗證點":"設計含量 mix 不逆轉，HPS 毛利率不被商品化","數字門檻 + 來源":"custom Ethernet switch 市佔 ≥50%（Dell'Oro 2025）；1.6T 已中標 ≥2 家 hyperscaler（公司法說）；Top 3 客戶 ≥10% 揭露（10-K）","漂移觸發":"某 &gt;10% 客戶單季占比掉 &gt;5pp，或 CCS 毛利率連 2 季 −100bps → 削弱（TTM 季節性過濾）"}},{"id":"H2","text":"2026 capex ramp（約 $1B、5% 營收）為「擴產換訂單」的合理投入，2027 起 FCF/NI 回升","columns":{"2Y 驗證點":"2027 H1/H2 FCF/NI 回到 ≥0.6","5Y 驗證點":"capex/rev 回落 &lt;4%，owner earnings 轉正常化","10Y 驗證點":"資本輕結構不因基建投資變重","數字門檻 + 來源":"FY25 FCF/NI 0.55（GAAP）；2026 capex/rev guide ~5%；AllianceTexas $876M（Bisnow 2025-04）","漂移觸發":"2027 H2 FCF/NI 連 2 季 &lt;0.5 且 capex/rev &gt;6% → 隱性資本密集確認"}},{"id":"H3","text":"35.5x Fwd PE 不會崩至 15x（估值體系不崩壞）；前提是 EPS 維持 +30%+ 且 ROIC &gt;25%","columns":{"2Y 驗證點":"Fwd PE FY1 維持 25-40x 區間，EPS 上修延續","5Y 驗證點":"倍數隨成長放緩溫和壓縮至 ~20x（非崩塌）","10Y 驗證點":"不落入 EMS 均值回歸至 15-18x 的地板","數字門檻 + 來源":"Fwd PE FY1 現 35.5x（5Y 分位 ~78%）；同業 JBL 22x／SANM 17x；EPS 3Y CAGR 45.6%（Excel snapshot 2026-06-23）","漂移觸發":"Fwd PE FY1 分位連 4 季 &gt;90% + 同業溢價連 4 季 &gt;80% → mean reversion 機率升；或 EPS YoY 連 2 季下修 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"hyperscaler 2026 H2 / 2027 capex 大幅修正（2007/2015 式），AI 資本週期拐頭","columns":{"對應假設":"H1+H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Meta/GOOGL/AMZN/MSFT 合計 capex guidance YoY","警戒閾值":"合計 capex YoY 從 +77% 降至 &lt;+15%（連 1 季）"}},{"id":"R2","text":"大客戶 AI 伺服器/交換機組裝二供或 in-house 擴散（Google TPU 已現，蔓延至網路交換機/其他客戶）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Inventec/Foxconn AI 伺服器出貨份額；季度個別客戶占比；CCS 毛利率","警戒閾值":"某 &gt;10% 客戶占比單季 −5pp；或 CCS 毛利率連 2 季 −100bps"}},{"id":"R3","text":"倍數均值回歸——35.5x 峰值 Fwd PE 隨成長放緩壓縮至 EMS 地板 15-18x，即使 EPS 兌現股價仍跌（SMCI/JBL 式 re-rate 頂）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Fwd PE FY1 分位、同業（JBL/SANM）相對倍數","警戒閾值":"Fwd PE FY1 分位連 4 季 &gt;90%；同業本益比連 2 季同步壓縮 &gt;20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"集中度回落<58% 或 Google 二供對 CCS 營收衝擊量化明朗、且證券詐欺調查結案；估值面 Fwd PE FY1≤28x（約 $285）補安全邊際","irr_base_pct":8.4,"ev5y_pct":35.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.8,"ev5y_pct":35.0,"irr_base_pct":8.4,"max_dd_pct":-58.0,"bull_5y_price":768.0,"bear_5y_price":143.0,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":"集中度回落<58% 或 Google 二供對 CCS 營收衝擊量化明朗、且證券詐欺調查結案；估值面 Fwd PE FY1≤28x（約 $285）補安全邊際","price_at_dd":359.85,"archetype":"EMS/ODM（資本輕·低毛利·需求週期·代工服務）","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CLS","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Celestica Inc."},"oneliner":"CLS：AI 網通交換器與運算機櫃的設計加製造廠，2027 年 EPS 指引翻倍、股價半年跌 38%，FY2 本益比約 11.6 倍；便宜與否取決於 2027 年墊進去的營運資金能否在 2028 年收回，先等 Q4 財報的現金與存貨數字。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CLS_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺超大規模雲端客戶 AI 資料中心建置的錢：設計並量產網通交換器、代工運算機櫃；錢卡在受配給的客製矽與記憶體，Celestica 拿的是設計加組裝那一段約 8.5% 的營益率，前三大客戶占 66%。","reasoning":"營收：Q3 2026 營收 58.3 億美元、年增 83%；CCS 約 49 億、年增約 102%、占約 84%，ATS 約 9.6 億、年增約 23%（分部數字為二手轉述）。利潤：Q3 調整後營益率 8.5%（年增 90 個基點），GAAP 營業利益 4.6 億、利益率 7.9%，調整後毛利率 11.2%（年減 50 個基點，管理層歸因 CCS 組合）。收錢方式：網通交換器多為自有設計（HPS，Q2 占營收 41%），矽料計入營收，設計含量反映在價格；運算機櫃與 OpenAI 專案為代料，晶片不進營收。單點依賴：Q3 前兩大客戶 35% 與 17%、合計 52%，前三大 66%，全在 CCS；2025 年曾因單一客戶 AI 運算專案換代，企業終端營收年減 19%。產業時鐘判擴張期：2027 年營收指引 400 億、約為 2026 年的 1.9 倍，需求仍在加速、各家擴產，未見產能過剩；但交期超過 52 週、客戶下 NCNR 長料訂單、公司存貨季增 11 億，是擴張後段的特徵。供需持久度：至 2027 年屬結構性持久（電子業協會 2026 年 8 月調查 64% 製造商限量供貨，記憶體新產能 2028 年起才開出）；2028 年後供給可逆性中等，屆時客戶是否重複下單會被檢驗，這是 Bear 機率的主要來源。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap_adjusted_operat","f_kpi2_gaap","f_kpi5_q4_2026","f_kpi6_2026","f_kpi7_2027"],"verdict_values":{"revenue_quality":"成長以量為主、集中度高：前十大客戶 2025 年占 79%（2023 年 64%），Q3 前三大 66%；網通含矽料墊高營收、壓低毛利率，運算代料使營收低估實際出貨量。2026 年營收指引三度上調到 210 億，2027 年首次指引 400 億，管理層稱已把爬坡、零組件與執行風險納入。","unit_econ_note":"Q3 毛利率 11.2%、調整後營益率 8.5%：營益率擴張來自營運槓桿與 HPS 組合，毛利率本身在下滑（Q2 CFO 稱 2026 年可維持 11.5% 上下，Q3 已低於此）；2027 年指引毛利率 11% 出頭、營益率 9.0%，增量利潤靠費用攤薄。","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"低毛利（11% 出頭）、高周轉、需求跟著超大規模客戶資本支出走；自有交換器設計讓營益率比同業高約 3 個百分點；2026–2027 年資本支出與營運資金大增，已不是資本輕結構"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2027 年，2028 年後供給可逆性中等：零組件緊缺多數來源稱延續到 2027 年底以上，管理層稱需求超過可出貨營收、客戶下 NCNR 長料訂單並簽 12～18 個月具約束力預測；反面是交期拉長本身會誘發重複下單，2028 年記憶體與被動元件新產能開出時才會被檢驗。","bargaining":{"up":"對上游弱：客製矽與記憶體受配給、部分料件交期超過 52 週；以客戶 NCNR 長料訂單與記憶體、PCB 供貨協議把成本與存貨風險轉回客戶。","down":"對客戶中等偏弱：最大客戶 35%、前三大 66%，客戶慣例雙供應商、成熟產品常移給第二供應商；但新世代爬坡階段 CLS 多為首選，投資人日稱份額與客戶定期協商、不必像商品化市場那樣搶。","geo":"產能分布泰國、美國德州（Richardson 擴建、Fort Worth 新園區）、墨西哥、日本；美中出口管制已對 CCS 與資本設備造成不利影響，關稅影響 10-K 稱無法量化但可能重大。"},"profit_pool_dir":"利潤池往晶片與記憶體端集中，代工端總體分配未見擴大；CLS 靠設計含量在代工段內部多拿，營益率高於同業約 3 個百分點。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM／SAM 數字；只有客製乙太網路交換器營收市占 58%（投資人日引第三方研究）與超大規模客戶營收 2023–2026 年約 5 倍兩個點，排不出五年利潤池遷移表；跑道判斷改用市占與第二條曲線"}}}},"q2_moat":{"verdict":"護城河趨勢持平（→）、等級 B：設計加量產爬坡的執行力在擴大，定價力持平偏弱；高 ROIC 是真的，但下一筆投入的報酬較低且要靠外部資金。","reasoning":"機制：自有交換器設計加高複雜度量產爬坡，綁在客戶每一代換代時程；客戶換手成本是重新設計與爬坡風險，不在合約。執行力 8 分：Q2 CEO 稱客戶把轉給別家的份額拿回來，投資人日稱 1.6T／800G 對手比前幾代少、客製乙太網路交換器營收市占 58%，10 個 1.6T 專案、工程師將超過 2,000 人。定價力 6 分：毛利率 Q3 年減 50 個基點、2027 年指引 11% 出頭，營益率擴張靠營運槓桿而非定價；投資人日另稱產能與電力投資帶來較好定價，但未量化。同業對照：TTM 營益率 CLS 8.29%，FLEX 5.44%、JBL 5.11%、SANM 5.49%、鴻海 3.51%，對最強同業差約 2.8 個百分點；但 FCF 利潤率 CLS 2.99% 反而低於 SANM 4.66%、JBL 3.82%、FLEX 3.32%，利潤優勢沒有轉成現金優勢。同業歷史差距事實表未涵蓋，無法判斷差距擴大或收窄。當期報酬落在低利益率×高周轉：調整後 ROIC 近四季 46.5%（增資說明書，平均淨投入資本 26.6 億；公司口徑是否稅前本包未載明，若為稅前以 20% 稅率換算約 37%），Q2 單季約 55%，EMS 大中型平均約 20%（單一摘要來源）；拆開是稅後營益率約 6.8% 乘上投入資本周轉約 5～7 倍。再投資：2027 年增量報酬粗估 33～37%、再投資率約 135～155%，超過 100% 的部分由增資支應，內生成長上界約 35%。三件事分開看：當期報酬高；持續期四項檢查三黃一綠，取決於下一代份額；新增資本報酬低於過去，漂亮的 ROIC 有一部分來自 2025–2026 年剛好有利的爬坡時點。","fact_refs":["f_peer_cls_gross_margin_pct","f_peer_cls_operating_margin_pct","f_peer_cls_fcf_margin_pct","f_peer_flex_operating_margin_pct","f_peer_flex_fcf_margin_pct","f_peer_jbl_operating_margin_pct","f_peer_jbl_fcf_margin_pct","f_peer_sanm_operating_margin_pct","f_peer_sanm_fcf_margin_pct","f_peer_2317_tw_gross_margin_pct","f_peer_2317_tw_operating_margin_pct","f_peer_2317_tw_fcf_margin_pct","f_kpi1_non_gaap_adjusted_operat","f_kpi7_2027"],"verdict_values":{"moat":{"mechanism":"設計加製造一條龍：自有交換器設計加高複雜度量產爬坡能力，綁定客戶每一代換代時程；換供應商的代價是重新設計與爬坡風險，而非合約條款。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大（份額回流、1.6T／800G 對手變少、客製交換器營收市占 58%），定價力持平（毛利率年減 50 個基點、2027 年指引 11% 出頭）；最大客戶占 CLS 營收由 32% 升到 35%，但 CLS 在各客戶內部的份額方向本包無數字（Google TPU 已確認非唯一來源），故不標↑。","competitor_notes":[{"name":"FLEX","strategy_note":"TTM 營益率 5.44%、FCF 率 3.32%；10-K 列為 EMS 對手，本包無其 AI 交換器份額資料，利潤率比 CLS 低約 2.9 個百分點。"},{"name":"JBL","strategy_note":"營益率 5.11% 最低，但 FCF 率 3.82% 高於 CLS，同業在不大舉擴產時現金轉換較好；CLS 的利潤優勢要到 2028 年後才可能轉成現金。"},{"name":"SANM","strategy_note":"營益率 5.49%、FCF 率 4.66% 為同業最佳，是 EMS 現金轉換的對照基準。"},{"name":"2317.TW","strategy_note":"毛利率 6.12%、營益率 3.51%、FCF 為負，規模最大、利潤最薄；10-K 列為 EMS 對手，客戶保留第二供應商時是可能的承接者。"},{"name":"Quanta／Wiwynn／Accton","strategy_note":"10-K 點名的 ODM 對手，提供設計加製造、正加強搶資料中心份額；本包無其財務數字。"}],"threats":[{"level":"🟡","text":"最大客戶二供或自製：客戶慣例雙供應商、成熟產品常移給第二供應商，Google TPU 已確認非唯一來源；屬雙邊份額協商，對 CLS 的衝擊因 35% 集中度放大，離散事件見唯一致命點。","p":"25%","evidence_refs":["customer_second_source#0","customer_second_source#2","customer_second_source#3","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#3"]},{"level":"🟡","text":"EMS 積極競標與 ODM 搶份額：10-K 稱資料中心支出集中導致 EMS 積極競標、ODM 加強搶市占；投資人日 CCS 總裁承認成功會招來競爭、已有新增對手。","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"技術路線變化：客戶面臨 AI 技術快速變化與替代品；CPO 由 CLS 承接首個大規模量產專案，1.6T 世代仍以可插拔光模組為主，架構轉換目前是機會而非替代。","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是超大規模雲端的 AI 叢集，決策者與付款者是同一批雲端業者的資本支出預算；網路頻寬換代（400G→800G→1.6T）屬需要而非想要，但延後購買的代價取決於 AI 投資回報。急迫性高、持久性未證：投資人日稱僅計已得標專案的 2028 年需求高於 2027 年，這是客戶預測，不是合約。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一世代交換器或機櫃專案這一層衡量：每代重新分配，成熟後常移給第二供應商（Q2 CEO）。代理變數：客戶把份額拿回給 CLS、10 個 1.6T 專案、客製交換器營收市占 58%；反面是最大客戶占 35%、Google TPU 非唯一來源，客戶可在下一代切換。"},{"item":"價值鏈分配","level":"🟡","text":"AI 資料中心價值鏈的錢主要落在晶片與記憶體：客製矽與記憶體受配給，代工端毛利率 11% 出頭且在下滑；交換晶片集中在少數供應商，代工段議價空間有限。CLS 靠設計含量在代工段內部多拿，營益率高於同業約 3 個百分點，但總分配份額未見擴大。"},{"item":"社會容忍度","level":"🟢","text":"代工營益率 8～9%，終端與社會無定價反彈壓力，也不依賴監管授權；政策面風險是美中出口管制與關稅，屬地緣而非社會容忍度問題，另列在風險。"}],"roiic":"約 33～37%（2027E 前瞻粗估，未扣折舊、偏保守）","reinvest_rate":"2026E 約 65～70%；2027E 約 135～155%","endo_ceiling":35,"formula_note":"增量稅後營業利益＝400 億×9.0%−210 億×8.4%≈18.4 億，×(1−20% 稅率)≈14.7 億；新增投入資本＝營運資金（增量營收 190 億×現金循環 47 天÷365≈24.5 億）＋資本支出 15～20 億（折舊事實表未涵蓋，未扣）≈40～45 億；增量報酬≈14.7÷40～45≈33～37%。再投資率：2026E 稅後營業利益約 14.1 億、自由現金流指引 4.6 億，約 67%；2027E 約 40～45÷28.8≈135～155%。內生上界＝增量報酬約 35%×再投資率上限 100%≈35%，超過 100% 的部分靠 8 月增資，不算內生；長期若增量報酬回落到 30%、再投資率 70%，上界約 21%。"}}}},"q3_growth":{"verdict":"五年後跑道 🟡：2027 年的翻倍有得標專案與 NCNR 長料訂單撐著，2028 年後要靠下一代 AI 資本支出；第二條曲線（整櫃 scale-up、CPO）已點名，但客戶池相同。","reasoning":"三年共識：FY2026E 11.59→FY2027E 22.31→FY2028E 31.99（Koyfin 2026-10-31）；以 FY2025 調整後 EPS 約 6.04 為基期，年複合約 74%，只看 FY1→FY3 也有約 66%。內生上界約 35%，缺口約 39 個百分點，歸因：一是 8 月增資約 34 億撐起超過 100% 的再投資（外部資金，非內生）；二是營益率 8.4%→9.0%，約占 2027 年營業利益增量 13%；三是 2026 年已建產能的利用率爬升。三項之外仍有一塊說不清：共識 2028 年 +43% 在營益率不變下需要約 550 億營收，管理層只說已得標需求高於 2027 年、沒給數字，屬無法歸因，長期信心上限為中。跑道：客製乙太網路交換器營收市占已 58%，本業滲透率高；第二條曲線（AMD Helios 與 OpenAI 整櫃 2027 年量產、CPO 交換器 2027 年底量產）已有具名專案，但都在同一批超大規模客戶裡，故給 🟡，跑道約 3～5 年。衰退信號亮 2 個：毛利率連 2 季年減、FCF／淨利連 2 年低於 0.75，長期成長性 🟡。AI 取代風險低：公司是 AI 建置的直接受益者。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_kpi6_2026","f_kpi7_2027","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主：800G 續增、1.6T 營收 2027 年超過 800G、OpenAI 與 AMD Helios 整櫃 2027 年量產；價只來自設計含量的組合效果，毛利率反而下滑；無併購；回購象徵性，8 月增資使股數增約 8～10%。","runway_years":"約 3～5 年","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段的增量報酬約 33～37% × 再投資率上限 100% ≈ 35%；共識 FY2025→FY2028 EPS 年複合約 74%（基期 6.04 由逐字稿回推），超出約 39 個百分點：外部增資撐起的再投資、營益率 8.4%→9.0%（約占 2027 年營業利益增量 13%）、2026 年已建產能利用率爬升可解釋一部分；2028 年 +43% 所需約 550 億營收管理層未給數字，屬無法歸因，依賴量能延續而非倍數。","segments":[{"item":"CCS（Q3 2026）","value":"約 49 億美元，年增約 102%，占營收約 84%（二手轉述）"},{"item":"ATS（Q3 2026）","value":"約 9.57 億美元，年增約 23%（二手轉述）"},{"item":"HPS（Q2 2026，屬 CCS）","value":"19 億美元，年增 58%，占營收 41%；交換器多為 HPS，利潤率高於非 HPS"},{"item":"分部利益率（Q2 2026）","value":"CCS 8.7%（年增 40 個基點）、ATS 6.3%（年增 100 個基點）"},{"item":"Q4 2026 指引","value":"運算與儲存終端約 +160%；CCS 約 +110%、ATS 約 +10%（後兩者為二手轉述）"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"note":"Q2 11.5%（年減 20 個基點）、Q3 11.2%（年減 50 個基點）"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"客製乙太網路交換器營收市占 58%，管理層稱份額回流"},{"item":"提價後銷量下滑","lit":false,"note":"無提價證據"},{"item":"EPS 成長高於營收成長超過 5 個百分點","lit":false,"note":"2027 年指引 EPS +86%、營收 +90%"},{"item":"FCF／淨利連 2 年低於 0.75","lit":true,"note":"2025 年 0.55（4.58 億／8.33 億）；2026 年自由現金流指引 4.6 億，遠低於 EPS 指引 11.55 隱含的淨利（約 1.2 億股計約 14 億）"},{"item":"SBC／營收超過 5% 且上升","lit":false,"note":"約 0.4%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"CPO 由 CLS 承接，1.6T 世代仍以可插拔為主"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業歷史倍數事實表未涵蓋，資料缺口"},{"item":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出以擴產為主，維護性部分未揭露"},{"item":"停止投資新產能且收入下滑","lit":false,"note":"正大舉擴產"}]}}},"q4_capital":{"verdict":"資本配置以有機成長優先：2026–2027 年把現金全數投入產能與營運資金，不夠的部分以每股 310 美元增資補足，股東先承受約 8～10% 稀釋；SBC 只占營收約 0.4%，回購是象徵性。這套做法要在 2028 年自由現金流轉正才算數。","reasoning":"現金轉換：2025 年 FCF 4.58 億／淨利 8.33 億＝0.55；TTM FCF 利潤率 2.99% 對營益率 8.29%；Q3 FCF 1.275 億（營業現金流 3.897 億−資本支出淨額 2.622 億）。2026 年 FCF 指引由 6 億下修到 4.6 億，同時營收上調到 210 億；2027 年 CFO 明說淨現金使用、拒絕給範圍，目標 2028 年轉正。現金去向：資本支出 2026 年約 10 億、2027 年 15～20 億；營運資金（存貨年增 25 億）；回購僅 Q1 約 2,000 萬美元後暫停；無股息；無併購（投資人日稱有主動漏斗）。資金來源：8 月增資淨額約 33.9 億（基本發行 968 萬股，CFO 稱約 35 億），循環額度擴至 17.5 億、到期 2031 年；目前淨現金約 29.3 億。SBC：Q3 2,130 萬美元，約 GAAP 營業利益 4.6%、營收 0.4%，年化約市值 0.26%。回購是否只為抵銷股權激勵，CFO 未正面回答。","fact_refs":["f_kpi3_non_gaap_fcf","f_kpi4_sbc_gaap","f_kpi6_2026","f_kpi7_2027","f_net_debt_m","f_shares_diluted_m","f_peer_cls_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"本包無已完成併購（併購事件軸查無），投資人日僅稱有主動漏斗"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q1 2026 回購約 7.3 萬股、2,000 萬美元（均價約 274 美元，對 FY1 EPS 盈餘殖利率約 4.2%）；8 月以 310 美元增發，淨股數增約 8～10%，回購遠不足以抵銷；十年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 員工 SBC 2,130 萬美元，年化約 8,500 萬，約市值 326.8 億的 0.26%／年，低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，股東回報近乎為零（無股息、回購象徵性），重點是再投資與增資，現金去向已寫在理由段"}}}},"q5_valuation":{"verdict":"現價 259 美元要求 2027 年 EPS 約 21～22 美元兌現、且 2028 年後不跌回 15 美元以下；以 FY2 共識約 11.6 倍計，只要 2028 年獲利不比 2027 年低就划算。我信 2027 年，對 2028 年只信一半，估值結論是合理偏低，不是深度便宜。","reasoning":"倍數：FY1 本益比 22.4 倍、FY2 約 11.6 倍、FY3 約 8.1 倍；trailing 本益比 24.5 倍、EV/S 1.63 倍（前瞻 1.41 倍）。四個年度端點內 trailing 本益比 45 分位、EV/S 53 分位，五年分位事實表未涵蓋。26 週跌 38%，FY1 共識近 3 個月上修 1.85%，最近兩份快照間 FY3 再上修 1.94%：股價下跌全是倍數壓縮，不是獲利下修。賣方均價目標 466 美元（22 位、區間 375～550，另一彙整低標 300），全距比約 1.5 倍；現價低於所有賣方目標，代表市場比賣方悲觀，賣方一致看多也說明情緒未投降。我比賣方保守的理由：10 月下修的自由現金流與 2027 年淨現金使用不到一季，還沒進賣方模型，先凍結首倉到 Q4 財報。終端倍數對照：同業現值本益比事實表未涵蓋，只能引前份 2026 年 6 月快照 JBL 約 22 倍、SANM 約 17 倍。上檔與情境樹用同一口徑（第 N 年價格＝Base 終端 13 倍×第 N 年 EPS，起點為 FY2026E）：一年約 13×22.0≈286 美元（+10%）、三年約 13×31.0≈403 美元（+56%）、五年約 13×35.0≈455 美元（+76%）；報酬全部來自 EPS 成長，倍數由 22.4 倍降到 13 倍，是拖累而非貢獻。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy3_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY1／FY2 共識，Koyfin 2026-10-31）為主，EV/S 對照","tier":"EMS／ODM（設計含量較高的一端）","peers":[{"item":"CLS Fwd P/E（FY1／FY2／FY3）","value":"22.4x／11.6x／8.1x（股價 259.12，共識 2026-10-31）"},{"item":"JBL Fwd P/E","value":"約 22x（前份 2026-06-23 快照，本包事實表未更新）"},{"item":"SANM Fwd P/E","value":"約 17x（前份 2026-06-23 快照，本包事實表未更新）"}],"fwd_pe":22.36,"peg":0.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 22.4 倍落在前份引用的 EMS 同業 17～22 倍上緣附近，FY2 11.6 倍則明顯偏低，兩者差距就是 2027 年獲利翻倍能否持續；五年分位事實表未涵蓋，只有四個年度端點（trailing 本益比 45 分位、EV/S 53 分位，居中）。PEG 0.30 被 2025→2028 年爆發成長壓低，不當便宜證據。合起來是合理偏低、非深度便宜。上檔與情境樹同一口徑（Base 終端 13 倍×當年 EPS，起點為 FY2026E）：一年＝2027 年 EPS 22.0×13 倍≈286 美元（+10%）；三年＝2029 年 EPS 31.0×13 倍≈403 美元（+56%）。","upside_short_pct":10,"upside_mid_pct":56,"denominator_disputed":false,"denominator_note":"FY1 調整後 EPS 不含一次性項目，SBC 只占營收 0.4%，分母口徑無爭議；FY2 依賴 2027 年指引，爭點在持續性而非會計，已放進 Bear 路徑而非改分母。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 2027 年的建置高峰當成新常態：最大客戶占 35%、存貨增速快過營收、2027 年自由現金流轉負，三件事都指向帳面 EPS 跑在現金前面。","reasoning":"價值陷阱信號亮 2 個（毛利率連 2 季年減；FCF／淨利連 2 年低於 0.75），判 🟡。壓力測試 4 項過 2 項：一、2027 年 EPS 低於指引 15%、之後照 Base，五年終點約 387 美元，過；二、最大客戶下一代份額減半（營收少約 17%、EPS 少約 25%），約 26×13≈341 美元，過；三、2028 年 AI 建置消化（Bear 路徑），約 144 美元，不過；四、最大客戶換主力供應商（唯一致命點），EPS 約 14×11 倍≈154 美元，不過。管理層迴避：2027 年淨現金使用範圍、與產能掛鉤的營收、稼動率數字、回購是否只抵銷股權激勵，四題都未正面回答，前兩題直接關係現金轉換。回撤：26 週已跌 38%、RSI 36.7；週線收盤 254.56 已跌破 52 週均線 322.92、仍在 104 週均線 236.11 之上；若 Bear 成形，從現價再跌 40%～60% 是此類股在客戶資本支出轉向時的常見幅度。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_kpi3_non_gaap_fcf","f_kpi6_2026"],"verdict_values":{"trap":{"verdict":"🟡","label":"建置高峰被當成新常態"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":11.59,"pe":22.36,"basis":"FY1（FY2026E）調整後 EPS 共識 11.59，現價 259.12；終端倍數同為前瞻一年口徑"},"eps":{"bull":[23.5,35.0,42.0,47.0,51.0],"base":[22.0,28.5,31.0,33.0,35.0],"bear":[19.0,13.0,10.5,11.0,12.0]},"pe":{"bull":17,"base":13,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":-0.3},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"max_dd":{"lo":-60,"hi":-40,"basis":"以 Bear 終點 −44%（12×12≈144 美元）為中樞，加上客戶資本支出轉向時常見的 10～15 個百分點超跌，下緣取 −60%；上緣 −40%（約 155 美元）對應 2028 年 EPS 回到約 14、倍數 11 倍。本檔 26 週已跌 38%，波動量級足以在半年內走完此類跌幅。","trigger_time":null},"basis":{"bull":"2027 年再超指引（2026 年已三度上調），1.6T、CPO、OpenAI 與 AMD 整櫃在 2028–2029 年接續放量、營益率升到約 10%；終端 17 倍＝前份引用同業 17～22 倍下緣","base":"2027 年約達共識 22，2028 年成長放慢到約 30%（共識 +43%），之後 AI 建置成熟、年增 5～8%；終端 13 倍低於同業，反映客戶集中與現金轉換弱","bear":"2027 年因零組件或爬坡延誤低於指引約 12%，2028 年超大規模客戶消化產能、最大客戶下一代改由他家主力，EPS 跌到 13 以下、2031 年回到 12；終端 12 倍＝成長熄火到 10% 時的 EMS 低谷倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"最大客戶占 35%、前三大 66%（Q3）；2025 年單一客戶 AI 運算專案換代讓企業終端營收年減 19%；客戶下 NCNR 長料訂單、部分料件交期超過 52 週，是容易重複下單的環境；管理層把零組件供應列為主要限制。","assumption":"2027 年需求不含重複下單，2028 年已得標需求真的高於 2027 年，最大客戶下一代仍以 CLS 為主力。","consequence":"2028 年營收回落、營益率回到 6% 上下，EPS 跌回 12～15 美元，市場給 EMS 低谷 10～12 倍，五年後股價約 144 美元，較現價 −44%；路徑中可能先跌到 −60%。","ruling":"採納，作為 Bear 機率 30% 的主要依據；不再往上加，因客戶 NCNR 訂單把長料風險留在客戶端、投資人日稱僅計已得標專案的 2028 年需求已高於 2027 年。與唯一致命點部分重疊：致命點是其中「最大客戶換主力」這個離散事件，消化期本身是連續風險，另列風險一。","watch":"每季 ≥10% 客戶占比、FY3 共識 EPS 修正方向、2027 年 10 月前後的 2028 年展望。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#3","supply_demand_durability#1"]},{"view":"論點成功但股東經濟變差","evidence":"2025 年 FCF／淨利 0.55；2026 年 FCF 指引由 6 億下修到 4.6 億而營收上調；2027 年 CFO 明說淨現金使用、資本支出 15～20 億；8 月以 310 美元增資淨額約 33.9 億，股數增約 8～10%；同業 SANM、JBL 的 FCF 利潤率都高於 CLS。","assumption":"2027 年的營運資金與資本支出是爬坡期一次性墊款，2028 年轉正後回收。","consequence":"若 2028 年後再投資率仍高於 100%，每股自由現金流長期落後每股 EPS，股東拿到的是被稀釋的成長；終端倍數應貼 EMS 低端 10～12 倍而非 13 倍，Base 終點少約 15%。","ruling":"部分採納：Base 終端倍數因此用 13 倍、不用同業 17～22 倍；尚不構成否決，因增資後淨現金約 29 億、Q2 毛負債對 EBITDA 約 0.5 倍，流動性無虞，增量投入的報酬粗估仍有 33～37%。","watch":"2028 年全年自由現金流、每季存貨增幅對營收增幅、資本支出指引是否再上調。","evidence_refs":["ems_utilization_capex_cycle#0","geo_supply_chain#1"]},{"view":"價格已反映太多","evidence":"FY1 本益比 22.4 倍仍高於前份引用的 SANM 約 17 倍；22 位賣方一致看多、均價目標 466 美元，FY3 共識近期仍上修 1.94%，情緒沒有投降；循環股在獲利高點本益比最低，FY2 的 11.6 倍可能是高點倍數。","assumption":"FY2 本益比低就代表便宜。","consequence":"若 2027 年是獲利高點，11.6 倍不是安全邊際，股價還要往 Bear 路徑走。","ruling":"部分反駁：股價已低於 8 月增資價 310 美元 16%、26 週跌 38%，FY1 倍數由 35.5 倍壓到 22.4 倍，高點疑慮已部分反映；賣方最低目標 300 美元仍高於現價。但賣方一致看多、10 月下修的自由現金流還沒進模型，正是不立即建倉、改等現金面證據的理由；已跌多少不等於安全邊際。","watch":"賣方評級分布與目標價下限、FY2／FY3 共識修正方向。","evidence_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 359.85 → 本次 259.12（-28.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=359.85","side_b":"本次 price_at_dd=259.12","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 迴避","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=迴避","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 追蹤 → 本次 不持有","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=追蹤","side_b":"本次 dca_role=不持有","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 359.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 359.85 美元：Bull 價 768、Bear 價 143，五年期望值 +35.0%，基準年化 8.4%，不對稱比 1.8","side_b":"本次情境、股價仍用 359.85 美元：Bull 價 867、Bear 價 144，五年期望值 +29.1%，基準年化 4.8%，不對稱比 1.96","ruling":"先換情境、股價不動：五年期望值少 5.9 個百分點，基準年化少 3.6 個百分點。不對稱比由 1.8 變為 1.96。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 359.85 美元：五年期望值 +29.1%，基準年化 4.8%，不對稱比 1.96","side_b":"本次情境、股價 259.12 美元：五年期望值 +79.3%，基準年化 11.9%，不對稱比 4.4","ruling":"再換股價、情境不動：起點價下跌 28.0%，五年期望值多 50.2 個百分點，基準年化多 7.1 個百分點，不對稱比由 1.96 升到 4.4。合計五年期望值比前份多 44.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"獲利與現金方向相反","cause":null,"prior_field":null,"side_a":"獲利面：2026 年 EPS 指引上調到 11.55，2027 年首次指引 21.50（+86%）、營益率 9.0%，FY1 共識近 3 個月上修。","side_b":"現金面：同一份財報把 2026 年自由現金流指引由 6 億下修到 4.6 億，2027 年淨現金使用且不給範圍；Q3 存貨季增 11 億（+32%）快過營收季增 24%；8 月增資約 34 億。","ruling":"方向相反，屬不可調和；裁決採獲利面為主、現金面為期限閘。2027 年增量營收約 190 億按 47 天現金循環要墊約 24.5 億營運資金，加資本支出 15～20 億，量級與自由現金流轉負對得上，判為爬坡期投入而非獲利灌水；但管理層拒給範圍，屬未證。2028 年自由現金流轉正前，不以 FY2 本益比當便宜證據。","evidence_level":"中","settle_metric":"2028 年全年自由現金流 > 0；先行指標為每季存貨增幅對營收增幅","if_then":["若 Q4 2026 財報（預期 2027 年 1 月下旬）揭露 2027 年自由現金流不低於 −15 億美元，且 Q4 存貨季增幅不高於營收季增幅 → 分批建立首倉，第一批組合 1%","若 2027 年任兩季存貨增幅高於營收增幅 5 個百分點以上，或 2027 年自由現金流指引低於 −20 億美元 → 停止加碼，已有部位減碼一半","反向：股價先漲回 310 美元以上而現金面證據未到 → 不追；股價跌到 210 美元以下而上述現金條件已成立 → 分批反買至組合 2%"],"evidence_refs":["ems_utilization_capex_cycle#0","supply_demand_durability#1"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"Q2 2026 法說（2026-07-28）：CFO 稱 2026 年毛利率可維持 11.5% 上下、2027 年資本支出 15 億是佔位數字；CEO 把 2026 年自由現金流指引由 5 億上調到 6 億，並稱 CPO 2027 年下半年量產。Q1 法說（2026-04-28）CEO 稱市占未見重大變化。","side_b":"投資人日（2026-10-27）：CFO 報 Q3 毛利率 11.2%（年減 50 個基點）、2026 年自由現金流下修到 4.6 億、2027 年資本支出 15～20 億；CCS 總裁稱 CPO 2027 年底量產。Q2 起 CEO 改稱各方面都在拿份額。","ruling":"程度差異、可調和：營收與 EPS 承諾全數超標，落差集中在毛利率與現金。毛利率下滑管理層歸因 CCS 組合，不採信也不否定，標未證、監測；預先登記：若 2027 年連 2 季毛利率低於 11.0%，組合歸因證偽，定價力評分下調 1 分。份額改口沒有量化，只當方向性證據。","evidence_level":"中","settle_metric":"季度調整後毛利率、2027 年各季自由現金流","if_then":["若 2027 年連 2 季毛利率低於 11.0% → 定價力降一級並停止加碼","若毛利率回到 11.5% 以上且營益率達 9.0% → 維持現判"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：10-K 稱資料中心支出集中使 EMS 積極競標、ODM 加強搶份額；投資人日 CCS 總裁承認已有新增對手；客戶慣例雙供應商。","side_b":"結構轉好：投資人日稱 1.6T／800G 對手比前幾代少、客製乙太網路交換器營收市占 58%；零組件緊缺延續到 2027 年底以上，讓料件已排好的 CLS 接回對手做不出來的份額。其他結構變數：美中出口管制已造成不利影響、墨西哥對非 FTA 商品課最高 50% 關稅（第三方未核實）、客戶結構越來越集中。","ruling":"雙向拉鋸：當代產品（800G／1.6T）結構轉好，下一代競爭惡化與客戶集中同時升高；結構轉好的依據是供給緊缺，2028 年供給放開後可能反轉，持久度只到 2027 年。","evidence_level":"中","settle_metric":"每季 ≥10% 客戶占比、毛利率","if_then":["若 2027 年內出現對手取得 CLS 主力客戶交換器下一代主力的公告 → 執行力評分降 1 分、減碼一半"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#0"]},{"axis":"循環位置訊號","cause":null,"prior_field":null,"side_a":"偏早、可買的訊號：已得標專案的 2028 年需求高於 2027 年（需求量拐點向上）；26 週跌 38%、RSI 36.7，股價低於所有賣方目標；trailing 本益比在四個年度端點中位附近。","side_b":"偏晚、該賣的訊號：公司存貨季增 32% 快過營收、客戶下 NCNR 長料訂單；交期超過 52 週、資本支出由營收 1.1% 升到 5.6%，屬建設循環後段特徵；賣方一致看多、情緒未投降。","ruling":"訊號矛盾，循環位置判中循環、交易姿態為持有不加，不觸發循環進場；股價淨值比事實表未涵蓋，相關檢查無法完成。投資面（等現金證據）與交易面（持有不加）方向一致，無背離。","evidence_level":"中","settle_metric":"存貨／季營收比、2028 年展望","if_then":["若存貨增幅回落到營收增幅以下且 2028 年展望高於 2027 年 → 位置改判早期，交易姿態可分批建立","若 2028 年展望低於 2027 年實際 → 位置改判晚循環，不得新建部位"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：三季連續上調指引，FY2 本益比 11.6 倍、FY3 約 8.1 倍；股價低於 8 月增資價 16%、低於所有賣方目標；週線仍在 104 週均線之上且三條均線斜率向上；淨現金約 29 億，客戶 NCNR 訂單保護長料成本。","side_b":"再等一季：10 月下修的自由現金流與 2027 年淨現金使用不到一季、尚未進賣方模型；存貨增速已有一季快過營收；管理層拒給 2027 年現金使用範圍。","ruling":"採等待：等的代價是一季的可能漲幅，換到的是唯一說不清那塊（現金轉換）的第一個數據點；期間股價先漲則不追。這不是看壞，是凍結首倉到首個確認點。","evidence_level":"中","settle_metric":"Q4 2026 財報的 2027 年自由現金流指引與 Q4 存貨","if_then":["若 Q4 財報條件成立 → 分批建立首倉","若股價先漲過 310 美元而條件未到 → 不追"],"evidence_refs":[]},{"axis":"前份漂移：估值與回撤","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份（2026-07-11，股價 359.85）：估值偏貴，FY1 本益比 35.5 倍；最大回撤 −58%。","side_b":"本次（股價 259.12）：FY1 本益比 22.4 倍、FY2 約 11.6 倍，估值轉為合理偏低；最大回撤改為 −40%～−60% 區間。","ruling":"估值改善主因是股價下跌 28%（359.85→259.12），同期 FY1 共識 EPS 約由 10.1 上修到 11.59（+14%），分母變化次要。回撤下緣仍在 −60%，因為 Bear 終點與循環超跌幅度不因起點變低而消失。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：情境機率","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"Bull 28%／Bear 30%","side_b":"Bull 25%／Base 45%／Bear 30%","ruling":"共識三年 EPS 年複合約 74% 超過內生上界約 35%，Bear 機率不得低於 30%，維持 30%；Bull 由 28% 降到 25%，因本次 Bull 要求 2028–2029 年再接一波放量，證據只到 2027 年得標專案。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：基本面結論","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","cycle_position"],"side_a":"前份：綜合評級 B、價值陷阱 🟡、護城河趨勢 →、五年後跑道 🟡、循環位置中循環。","side_b":"本次：五欄的值都沒變。列在這裡是因為五欄都有新證據進來重審過；原因欄的「新證據」指重審時用到的證據，不代表值有變動。","ruling":"逐欄寫。綜合評級、價值陷阱、護城河趨勢：正面新證據是 2027 年首次指引 400 億營收、9.0% 營益率，客製乙太網路交換器營收市占 58%，1.6T／800G 對手變少；負面是 Q3 毛利率年減 50 個基點、最大客戶占比由 32% 回升到 35%、2026 年自由現金流指引下修、2027 年轉為淨現金使用，正負相抵，維持原判。五年後跑道：新證據是第二條曲線有了具名專案（AMD Helios 與 OpenAI 整櫃 2027 年量產、CPO 交換器 2027 年底量產），能見度拉長；但客戶池仍是同一批超大規模業者，2028 年後需求只有管理層說法，維持 🟡。循環位置：偏早的新證據是已得標專案的 2028 年需求高於 2027 年，偏晚的是存貨季增 32% 快過營收、交期超過 52 週、資本支出占營收由 1.1% 升到 5.6%，兩邊互相抵銷，維持中循環，細節見循環位置訊號一條。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":["customer_concentration_credit#3"]},{"axis":"前份漂移：公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"EMS/ODM（資本輕·低毛利·需求週期·代工服務）","side_b":"EMS/ODM（低毛利·高周轉·需求週期·設計加製造；資本密集度上升中）","ruling":"類型不變，拿掉「資本輕」：資本支出占營收由一年前 1.1% 升到 5.6%（Q2 2026），2027 年資本支出 15～20 億、自由現金流轉負，這兩年已不是資本輕結構。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件與裁決","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"集中度回落<58% 或 Google 二供對 CCS 營收衝擊量化明朗、且證券詐欺調查結案；估值面 Fwd PE FY1≤28x（約 $285）補安全邊際","side_b":"Q4 2026 財報揭露 2027 年自由現金流 ≥ −15 億美元，且 Q4 存貨季增幅不高於營收季增幅（成立後分批建立首倉）","ruling":"前份估值條件已成立（FY1 本益比 22.4 倍、股價低於 285 美元）；集中度條件未成立且方向相反（Q3 前三大 66%）；證券詐欺一項，本包 10-K 稱過往證券集體訴訟已和解或駁回、查無新調查，退休不再追蹤。集中度改由唯一致命點與出場門檻追蹤，不再當進場條件；本次觀望的唯一約束換成現金轉換，重啟條件改寫為該約束的否定，成立後分批建立首倉。裁決與角色由程式依新輸入重算。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（null）","side_b":"最大客戶（Q3 占營收 35%，身分本包未揭露）在下一代 AI 運算或交換器專案改由他家擔任主力供應商","ruling":"前份未設唯一致命點；本次依最大單一敏感度選定這個離散事件，發生即清倉。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：出場門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"最大客戶占比單季降 ≥5 個百分點且無替補→減碼一半、跌破 20%→清倉；FY3 共識 EPS 累計下修 ≥10% 或跌破 28→減碼一半；2028 年自由現金流 <0→減碼一半、2029 年仍 <0→清倉；毛利率連 2 季 <10.8%→停止加碼；存貨增幅連 2 季高於營收增幅 ≥5 個百分點→減碼一半","ruling":"前份只有風險監測、沒有出場門檻；本次補上減碼與清倉門檻，全部改用公司損益與現金層指標。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：風險門檻","cause":"方法變動","prior_field":["thesis.R"],"side_a":"R1 四大雲端合計資本支出年增由 +77% 降到 <+15%；R2 任一 >10% 客戶單季 −5pp 或 CCS 毛利率連 2 季 −100bps；R3 Fwd PE FY1 分位連 4 季 >90%、同業本益比連 2 季同步壓縮 >20%","side_b":"R1 2028 年營收展望低於 2027 年實際或 FY3 共識單季下修 ≥10%；R2 任一 ≥10% 客戶單季占比降 ≥5 個百分點且無替補專案；R3 存貨增幅連 2 季高於營收增幅 ≥5 個百分點；另增 R4 關稅與出口管制、R5 客戶端技術與商業風險","ruling":"R1 改用公司層指標：事實表不再收錄雲端業者資本支出，改以公司損益層的吸收失敗判斷。R2 客戶占比門檻保留；CCS 毛利率門檻改為全公司毛利率，因分部毛利率本包未揭露。前份 R3 倍數均值回歸已大半發生（35.5→22.4 倍），前瞻本益比分位只有 2026 年 5 月起的短窗，指標失去意義，退休；風險改列存貨與現金轉換，觸發即減碼一半。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"現金面證據到位才建首倉","type":"估值rearm","maps_to":"H2","metric":"2027 年自由現金流指引；Q4 2026 存貨季增幅對營收季增幅","threshold":"2027 年自由現金流 ≥ −15 億美元，且 Q4 存貨季增幅 ≤ 營收季增幅","action":"分批建立首倉，第一批組合 1%，Q1 2027 營益率 ≥ 8.7% 再加到 2%","source_freq":"季度財報新聞稿與法說","date":"2027-01"},{"n":2,"text":"2027 年營收與營益率對指引","type":"假設驗證","maps_to":"H1","metric":"季度營收與調整後營益率對指引中點","threshold":"連 2 季落後 ≥ 5%","action":"停止加碼，第一項假設降為削弱","source_freq":"季度","date":null},{"n":3,"text":"2028 年獲利不比 2027 年低","type":"假設驗證","maps_to":"H3","metric":"FY3（2028）共識 EPS","threshold":"連 2 季累計下修 ≥ 5% 或跌破 28 美元","action":"停止加碼；累計下修 ≥ 10% 則減碼一半","source_freq":"Koyfin 共識快照，月度","date":null},{"n":4,"text":"大客戶占比驟降","type":"減碼","maps_to":"R2","metric":"每季 ≥10% 客戶營收占比","threshold":"任一客戶單季下降 ≥ 5 個百分點，且公司未給替補專案","action":"減碼一半","source_freq":"10-Q／季度新聞稿","date":null},{"n":5,"text":"最大客戶換主力供應商","type":"Single Thing","maps_to":"Single Thing","metric":"最大客戶下一代運算或交換器專案的主力供應商","threshold":"公司或客戶確認下一代主力改由他家，或最大客戶占比跌破 20%","action":"清倉","source_freq":"季度法說、客戶與同業公告","date":null},{"n":6,"text":"存貨堆積快過營收","type":"減碼","maps_to":"R3","metric":"季度存貨增幅減營收增幅","threshold":"連 2 季 ≥ +5 個百分點（Q3 2026 約 +8 個百分點，已滿第 1 季）","action":"減碼一半；未持有則取消首倉計畫","source_freq":"10-Q 資產負債表","date":null},{"n":7,"text":"AI 建置轉入消化期","type":"風險","maps_to":"R1","metric":"公司 2028 年營收展望；FY3 共識 EPS 單季修正","threshold":"2028 年營收展望低於 2027 年實際，或 FY3 共識單季下修 ≥ 10%","action":"減碼一半並重跑研究","source_freq":"年度展望、共識月度","date":"2027-10"},{"n":8,"text":"跌但基本面無損","type":"加碼","maps_to":"H1","metric":"股價對 FY2 共識 EPS 倍數；第一、二項假設狀態","threshold":"股價 ≤ 210 美元（約 FY2 共識 9.4 倍），且第一、二項假設未削弱、首倉條件已成立","action":"分批反買至組合 2%","source_freq":"每日股價、季度財報","date":null},{"n":9,"text":"倍數回到同業區間","type":"減碼","maps_to":"H3","metric":"股價對 FY2 共識 EPS 倍數","threshold":"股價 ≥ 400 美元（FY2 共識約 18 倍，前份引用同業 17～22 倍）","action":"減碼三分之一","source_freq":"每日股價","date":null},{"n":10,"text":"關稅與出口管制吸收失敗","type":"風險","maps_to":"R4","metric":"調整後營益率對指引中點","threshold":"連 2 季低於指引中點 ≥ 30 個基點且公司歸因關稅或出口管制","action":"停止加碼","source_freq":"季度","date":null},{"n":11,"text":"Q4 2026 財報複審","type":"複審日期","maps_to":null,"metric":"2027 年自由現金流指引、Q4 存貨、毛利率","threshold":null,"action":"重跑判斷","source_freq":"季度","date":"2027-01"}],"kill_metrics":[{"metric":"最大客戶營收占比（季度揭露）","bear_threshold":"單季下降 ≥5 個百分點且無替補專案→減碼一半；跌破 20%→清倉","window":"每季","source":"10-Q／季度新聞稿","last_status":"ok"},{"metric":"FY3（2028）共識 EPS","bear_threshold":"累計下修 ≥10% 或跌破 28 美元→減碼一半","window":"連 2 季","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"2028 年全年自由現金流","bear_threshold":"<0→減碼一半；2029 年仍 <0→清倉","window":"2028–2029 年度","source":"10-K／年度新聞稿","last_status":"unknown"},{"metric":"季度調整後毛利率","bear_threshold":"連 2 季 <10.8%→停止加碼","window":"連 2 季","source":"季度新聞稿","last_status":"warning"},{"metric":"存貨季增幅減營收季增幅","bear_threshold":"連 2 季 ≥+5 個百分點→減碼一半","window":"連 2 季","source":"10-Q 資產負債表","last_status":"warning"}],"evidence_dismissed":[{"ref":"$.counter_evidence.contradictions[8]","reason":"產業態勢三軸那一條本來只處理競爭與結構。閘點名的四軸裡，有三軸的實質寫在別段，並非沒接：商業模式（網通交換器自有設計、矽料計入營收；運算機櫃與 OpenAI 專案代料、晶片不進營收）寫在業務段的收錢方式與營收品質，也用來解釋毛利率下滑；資本市場定價（8 月以每股 310 美元增資淨額約 33.9 億、股數增約 8～10%，循環額度擴至 17.5 億）寫在資本配置段，並進了「股東經濟變差」盲點與獲利對現金那條矛盾；終端市場（CCS／ATS 分部、Q4 運算與儲存終端約 +160%、超大規模客戶集中）寫在業務段與成長段分部表。反壟斷一軸：閘與本輪修補都看不到該軸內容，判斷中也沒有引用它的事實，看不到內容就補進去等於編造，列為下次重跑必須補接的一軸。"},{"ref":"$.scenario_inputs","reason":"閘點出的口徑混用已改：估值段的一年與三年上檔改用情境樹同一口徑（Base 13 倍×當年 EPS），見估值段理由與上檔欄。其餘幾點不改情境樹，理由如下。一、Bear 2027 年 EPS 19.0 貼近 Base 22.0 是刻意設計：Bear 依據寫明 2027 年只因零組件或爬坡延誤低於指引 21.50 約 12%（約 18.9），因為 2027 年有得標專案與客戶 NCNR 長料訂單撐著；兩條路徑從 2028 年才分岔（Bear 13.0 對 Base 28.5），Bear 五年價 144 美元只取 2031 年 EPS 12×12 倍，2027 年數字不進終點。二、情境樹起點是 FY2026E 的 11.59，不是 FY2025 的 6.04；Bear 2028–2031 年 EPS 10.5～13.0 等於把 2027 年的翻倍全部吐回、回到起點上下，6.04 只用來算共識年複合率。三、Bear 30% 不是只靠下限規則：論點失敗那條盲點給了證據面依據（最大客戶 35%、交期拉長與 NCNR 長料下的重複下單、2025 年單一客戶換代使企業終端營收年減 19%），也寫了不再往上加的理由；下限規則只限制不得往下調。四、迴避裁決不依賴情境樹：裁決表命中的是「論點不可調和」，它來自獲利與現金方向相反那條矛盾（EPS 指引上調、自由現金流指引同時下修、2027 年淨現金使用），與 Bear 機率、期望值、不對稱比無關；這三個情境產出在判斷裡留空、由程式回填。五、Bear 下的淨負債與股數事實表未涵蓋，不補數字；情境 EPS 已是每股口徑，所用共識快照（2026-10-31）晚於 8 月增資。"}],"action_conditions":{"rearm_trigger":"Q4 2026 財報揭露 2027 年自由現金流 ≥ −15 億美元，且 Q4 存貨季增幅不高於營收季增幅","exec_line":"條件成立後分批建立首倉：第一批組合 1%，Q1 2027 財報營益率 ≥ 8.7% 再加到 2%；股價先漲過 310 美元而證據未到則不追；跌到 210 美元以下且條件成立則分批反買。","holding_cap":"組合 3%"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2 約 11.6 倍把 2027 年當獲利高點定價；但投資人日稱僅計已得標專案的 2028 年客戶需求已高於 2027 年營收展望，1.6T 營收 2027 年才超過 800G，CPO 與 OpenAI 機櫃 2027 年下半年後才放量，獲利高點最早落在 2028 年之後。此理由的證據只到管理層說法，只支撐等待而非立即建倉。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 Q4 2026 財報（預期 2027 年 1 月下旬）：2027 年自由現金流指引不低於 −15 億美元，且 Q4 存貨季增幅不高於營收季增幅；股價先漲過 310 美元而證據未到則不追。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"迴避"},"thesis":{"H":[{"id":"H1","text":"設計加製造讓 CLS 在交換器與機櫃每一代換代時保住主力供應商位置，2027 年營收 400 億、營益率 9.0% 兌現","2y":"2027 年營收 ≥ 380 億美元、調整後營益率 ≥ 8.7%；1.6T 營收 2027 年超過 800G","5y":"客製乙太網路交換器營收市占維持 ≥ 50%，CPO 與整櫃 scale-up 量產客戶 ≥ 2 家","10y":null,"threshold":"2027 年營收 ≥ 380 億美元且調整後營益率 ≥ 8.7%（指引 400 億、9.0% 下緣容忍 5%）","source":"季度新聞稿與法說；市占數字為投資人日引用的第三方研究","drift_rule":"季度營收或營益率對指引中點連 2 季落後 ≥ 5% → 削弱；連 3 季落後 ≥ 10% → 反轉"},{"id":"H2","text":"2026–2027 年的營運資金與資本支出高峰是爬坡期墊款，不是結構性變重；2028 年自由現金流轉正","2y":"2027 年自由現金流不低於 −15 億美元；2028 年全年自由現金流 > 0（管理層目標）","5y":"自由現金流／調整後淨利回到 ≥ 0.6，資本支出／營收回落到 ≤ 4%","10y":null,"threshold":"2028 年全年自由現金流 > 0，且存貨增幅不連 2 季高於營收增幅 5 個百分點以上","source":"季度現金流量表與資產負債表（10-Q／10-K）、年度指引","drift_rule":"存貨增幅連 2 季高於營收增幅 ≥ 5 個百分點 → 削弱；2028 年上半年自由現金流仍為負 → 反轉"},{"id":"H3","text":"AI 資料中心建置在 2028 年仍高於 2027 年，CLS 的獲利高點不在 2027 年","2y":"2028 年營收展望高於 2027 年實際；FY3 共識 EPS ≥ 28 美元","5y":"2031 年 EPS ≥ 30 美元（Base 35 的下緣容忍）","10y":null,"threshold":"FY3（2028）共識 EPS ≥ 28 美元（現 31.99）","source":"Koyfin 共識快照；公司年度展望（預期 2027 年 10 月）","drift_rule":"FY3 共識 EPS 連 2 季累計下修 ≥ 5% → 削弱；連 3 季累計下修 ≥ 10% → 反轉"}],"R":[{"id":"R1","text":"超大規模客戶資本支出轉入消化期，2028 年營收不再成長；客戶 NCNR 長料訂單與交期拉長意味部分需求可能是重複下單","h_ref":"H3","clock":"🔥","threshold":"2028 年營收展望低於 2027 年實際，或 FY3 共識 EPS 單季下修 ≥ 10%","evidence_refs":["supply_demand_durability#1","ems_utilization_capex_cycle#0"]},{"id":"R2","text":"大客戶二供、自製或轉單：最大客戶 35%、前三大 66%，客戶慣例雙供應商；2025 年單一客戶專案換代已讓企業終端營收年減 19%；關稅下客戶也可能自製或轉給其他供應商","h_ref":"H1","clock":"⚡","threshold":"任一 ≥10% 客戶單季占比下降 ≥ 5 個百分點且無替補專案","evidence_refs":["customer_second_source#0","customer_second_source#2","customer_second_source#3","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3","competitive_share_entrants#0"]},{"id":"R3","text":"營運資金與存貨堆積：Q3 存貨季增 11 億、年增 25 億，增幅快過營收；客製矽、記憶體、高層數 PCB 交期拉長，短缺可能迫使以較差條件向第三方採購；需求轉弱時長料存貨會卡住現金","h_ref":"H2","clock":"🔥","threshold":"存貨增幅連 2 季高於營收增幅 ≥ 5 個百分點，或 2027 年自由現金流指引低於 −20 億美元","evidence_refs":["ems_utilization_capex_cycle#0","geo_supply_chain#1","supply_demand_durability#1"]},{"id":"R4","text":"關稅與出口管制：美中出口管制已對 CCS 與資本設備造成不利影響，10-K 稱未來影響與關稅衝擊可能重大；客戶可能以自製或轉單規避關稅；營運橫跨北美、亞洲、歐洲，暴露美中、中台等地緣緊張","h_ref":"H1","clock":"🐢","threshold":"調整後營益率連 2 季低於指引中點 ≥ 30 個基點且公司歸因關稅或出口管制","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","customer_second_source#1"]},{"id":"R5","text":"客戶端技術與商業風險：AI 技術快速變化、替代品出現、低成本與開源模型壓低客戶 AI 產品定價，回頭壓縮客戶資本支出","h_ref":"H3","clock":"🐢","threshold":"公司下一年度營收展望成長率低於 20%，且歸因客戶資本支出下修","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"最大客戶（Q3 占營收 35%，身分本包未揭露）在下一代 AI 運算或交換器專案改由他家擔任主力供應商","why_fatal":"這是單一最大敏感度：35% 營收集中在一家；失去主力位置，2028 年 EPS 少三分之一以上，營益率同時失去規模槓桿，Bear 路徑直接成形","if_happens":"2028 年 EPS 回到約 13～15 美元、倍數壓到 10～12 倍，股價約 130～180 美元；持有則清倉，未持有則取消建倉計畫","how_monitor":"每季 10-Q 與新聞稿揭露的 ≥10% 客戶占比；法說對下一代運算與交換器專案的說法；同業取得同一客戶主力專案的公告","probability":"12～24 個月約 15%：客戶慣例雙供應商、成熟產品常移給第二供應商，Google TPU 已確認非唯一來源；但 CLS 多為新世代首選爬坡夥伴，Q3 最大客戶占比由 32% 回升到 35%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":11.61,"peg_fy2":0.27,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":6.04,"FY2026E":11.59,"FY2027E":22.31,"FY2028E":31.99},"fy_end_month":12,"eps_basis":"調整後（non-GAAP）稀釋 EPS，財年 12 月底；FY2026E–FY2028E 為 Koyfin 2026-10-31 共識快照（FY2026 另見 Chartmill 19 位分析師）；FY2025A 事實表未直接收錄，由 Q2 2026 逐字稿「2026 年調整後 EPS 11.30、年增 87%」回推約 6.04，與 GAAP 稀釋 EPS 7.16 口徑不同，不混用。三年共識年複合約 74%。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"AMD Helios scale-up 交換器開始量產爬坡","impact":"中","watch":"Q4 法說是否確認出貨與 2027 年金額"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年現金使用","impact":"高","watch":"2027 年自由現金流指引、Q4 存貨季增幅對營收季增幅、毛利率"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"OpenAI 客製加速器機櫃量產爬坡","impact":"中","watch":"運算終端營收成長率、代料對營收認列的影響"},{"date":"2027-10","date_precision":"month","type":"guidance","event":"2028 年展望（依今年 10 月投資人日時點推估）","impact":"高","watch":"2028 年營收是否高於 2027 年實際、資本支出指引"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"CPO 交換器量產","impact":"中","watch":"是否如期、是否有第二家 CPO 客戶"}]}
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
