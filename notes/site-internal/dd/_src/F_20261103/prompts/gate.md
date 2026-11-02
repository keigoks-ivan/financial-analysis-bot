你是 DD 管線 v20 的判斷層閘（gate），標的 F（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（55 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝49.5 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi1_adjusted_ebit`（q1_business）｜Adjusted EBIT＝2.658 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi2_adjusted_ebit_margin`（q1_business）｜Adjusted EBIT margin＝5.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝1.454 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率（自算）＝2.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi10_adjusted_ebit`（q1_business）｜全年指引 Adjusted EBIT＝10.5～11.0 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_kpi12_wholesales`（q1_business）｜批發量 Wholesales＝1049 千輛｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[12]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi13_ford_pro_ebit`（q1_business）｜Ford Pro EBIT＝1.665 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[13]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi14_ford_blue_ebit`（q1_business）｜Ford Blue EBIT＝1.392 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[14]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi15_ford_model_e_ebit`（q1_business）｜Ford Model e EBIT＝-1.058 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[15]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_f_gross_margin_pct`（q2_moat）｜F 毛利率＝2.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.F.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_f_operating_margin_pct`（q2_moat）｜F 營業利益率＝-3.82 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.F.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_f_fcf_margin_pct`（q2_moat）｜F FCF 利潤率＝2.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.F.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gm_gross_margin_pct`（q2_moat）｜GM 毛利率＝7.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gm_operating_margin_pct`（q2_moat）｜GM 營業利益率＝2.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gm_fcf_margin_pct`（q2_moat）｜GM FCF 利潤率＝-0.19 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_stla_gross_margin_pct`（q2_moat）｜STLA 毛利率＝7.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STLA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stla_operating_margin_pct`（q2_moat）｜STLA 營業利益率＝0.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STLA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stla_fcf_margin_pct`（q2_moat）｜STLA FCF 利潤率＝-7.18 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STLA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_tm_gross_margin_pct`（q2_moat）｜TM 毛利率＝16.76 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tm_operating_margin_pct`（q2_moat）｜TM 營業利益率＝7.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tm_fcf_margin_pct`（q2_moat）｜TM FCF 利潤率＝-2.35 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.91 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.91 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝2.09 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝175943.28 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝179702.64 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.52 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（1.92 → 1.91）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.95 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.11 → 2.09）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_kpi5_eps_gaap`（q4_capital）｜淨利／稀釋 EPS（GAAP）＝2.049 USD bn（EPS 0.50）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi7`（q4_capital）｜營業現金流＝5.4 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi8_adjusted`（q4_capital）｜Adjusted 自由現金流＝4.7 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無（新聞稿未載）
- `f_kpi9_sbc_9`（q4_capital）｜SBC（前9個月累計，無單季）＝324 USD m｜期間與口徑：2026 年前九個月（公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[9]，as_of 2026 年前九個月（公告於 2026-10-28））
  - 註記：不適用
- `f_kpi11_adjusted_fcf_capex`（q4_capital）｜全年指引 Adjusted FCF／Capex＝fcf_low 6；fcf_high 7；capex_low 9.5；capex_high 10.5 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，2026-10-28）https://www.sec.gov/Archives/edgar/data/0000037996/000003799626000190/exhibit99tooctober282026.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝4.781 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝3993.22 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝140345.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 165433.0、現金 25088.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝12.55 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝6.57 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 1.91，分子＝快照價 12.54｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝3.8 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（1.84 → 1.91）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝5.52 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 1.81 → 1.91（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.27 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝97.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝97.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.02 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝87.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝87.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.08 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝190422.34 USD m｜期間與口徑：2026-11-03／市值 50077.34 ＋ 淨負債 140345.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝11.61 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.68｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 12.61 / W52 13.16 / W104 11.61 / W250 10.86 / W250 13週斜率 -0.67%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝13.16 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝11.61 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝10.86 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.67 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（32 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Ford 10-K 稱產業歷來競爭激烈、產能過剩，業者以折扣與促銷維持市占；EV 政策支持減弱導致該區隔供給過剩，近季已見此類行動重現。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Ford 10-K 風險因子指出其產品面臨汽車及數位軟體服務產業既有業者與新進入者的重大競爭，且新進入者可能加速其重組行動。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Cox Automotive 預估 GM 與 Ford 為 2026 年美國市占流失最大的主要車廠；Ford 前九月市占約 12.5%，降近一個百分點。
  - 來源：OCBJ / Cox Automotive：Ford US share decline slowing（as_of 2006-04-11）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Ford 2026年7月美國銷量（Ford 品牌）年減 9.1%，年初至今減 9.5%。
  - 來源：Ford U.S. July 2026 Sales Release（as_of 2026-08-04）｜affects：moat_trend
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：Farley 於 2026-07-30 員工會議表示中國車廠可能在 5–10 年內進入美國市場。
  - 來源：GM Authority：Ford CEO tells employees Chinese automakers could arrive in the U.S. within 10 years（as_of 2026-07-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：GlobalData/MarkLines 預測 2026 全球輕型車產量約 91.97M（-1.2%）、2027 約 92.64M；2026/2027 預測分別下修 1.7M 與 2.5M，主因中國需求疲弱
  - 來源：MarkLines GEN-AI forecast production 202607（as_of 2026-07-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：BCG 研究（經 Milano Finanza 引述）估歐洲約 5.4M 輛過剩產能、35 座工廠有風險、平均稼動率 59%；Mercedes 計畫 2028 年將全球產能降至 2.2M
  - 來源：Milano Finanza (BCG study)（as_of 2026-07-01）｜affects：thesis.R、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：S&P 中國評級 2026 年 4 月：產能整併是緩解中國車市競爭的主要途徑，預期 2026 年競爭激烈、短期利潤率承壓
  - 來源：S&P Global Ratings China 2026 Auto Outlook（as_of 2026-04-08）｜affects：thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：福特 10-K 揭露：已實施的美國及他國關稅對福特、其他車廠、供應商與經銷商造成顯著干擾與成本增加
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年關稅毛成本約 30 億美元，扣除抵減後對 EBIT 淨影響約 20 億美元
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-11）｜affects：valuation、thesis.R
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：中國稀土及零組件出口限制已造成福特供應鏈生產中斷與成本上升，並列為出口管制風險
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Novelis Oswego NY 鋁廠 2025年9月火災，該廠供應美國車用鋁板約40%，Ford 為最大客戶（F-150）；Ford 暫停至少五款車型生產，預估Q4 EBIT 逆風$1.5-2B、自由現金流衝擊$2-3B；Ford 改向 Novelis 其他廠採購
  - 來源：Deseret News: Ford stops production of multiple vehicles（as_of 2025-10-14）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：第三方風險彙整站轉述 Ford SEC 申報：中國稀土與零組件出口限制已造成 Ford 生產中斷與成本上升，未來中斷風險升高；鋁供應中斷拉低 F-150 批售（原文未核，需對照 10-K/10-Q）
  - 來源：policyrisk.com Ford (F) company page（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中荷 Nexperia 晶片爭端引發 GM、Ford 股價下滑與供應鏈疑慮，車廠警告可能干擾美歐生產
  - 來源：Stocktwits: GM, Ford Stocks Slip As China-Dutch Chip Dispute Over Nexperia（as_of 2025-10-30）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：2026Q3 Ford Model e 批發 34k（-31%）、營收 $1.2B（-31%），EBIT 虧損約 $1.06B
  - 來源：Ford Q3 2026 Earnings Press Release（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：2026Q3 Ford Blue 營收 $27.1B（-3%），因批發下降，部分被產品組合與匯率抵銷；EBIT $1,392M
  - 來源：Ford Q3 2026 Earnings Press Release（as_of 2026-10-28）｜affects：thesis.H、valuation
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Ford 美國銷量 2026Q3 年減 7% 至 509,764 輛；1–9 月累計 -8.6% 至 1,516,279 輛
  - 來源：Ford Authority（as_of 2026-10-01）｜affects：moat_trend、decision_inputs.bear
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Experian 2026Q2：Ford 在美國新車市佔排第四、11.8%
  - 來源：Ford Authority（as_of 2026-09-01）｜affects：moat_trend
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：報導稱Ford CEO Farley承認中國汽車技術在全球已領先／中國品牌為北美市場存亡威脅
  - 來源：Katadata: Ford Boss Admits Chinese Car Technology Starting to Surpass US（as_of 2025-11-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：2026北京車展：軟體定義車輛與AI成為競爭焦點，中國品牌出口擴張並往高端移動
  - 來源：WhichEV: Auto China 2026 show report（as_of 2026-05-05）｜affects：moat_trend
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2025-12-09 Ford 與 SK On 簽 BOSK 合資處分協議：Ford 持分被贖回、Ford 子公司取得肯塔基兩座電池廠，並認列 BOSK 資產減損及剩餘投資減損（8-K Item 2.06），預計 2026 上半年交割
  - 來源：SEC EDGAR 8-K Item 2.06 (2025-12-15)（as_of 2025-12-15）｜affects：valuation、thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：10-K FY2025 列示 Hetsler v. Ford 產品責任案：2024 年陪審團判 Ford 賠 1.03 億美元，Ford 已上訴
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：GM 於 2025 年 6 月宣布 $40 億美國投資，Orion 汽油全尺寸 SUV/皮卡 2027 年初開產；GM 預計至 2027 年每年資本支出 $100–120 億
  - 來源：GreentechLead: EV Factory Investment in 2026（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Hyundai 美國 2025–2028 投資由 $210 億增至 $260 億，Metaplant America 目標 2028 年年產 50 萬輛（規劃產能）
  - 來源：GreentechLead: EV Factory Investment in 2026（as_of 2026-01-01）｜affects：thesis.R
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：美國新車整體庫存 2026-09 升 4.5% 至 280 萬輛，庫存天數 82 天（8 月 75 天）；J.D. Power 預估 10 月獎勵金占 MSRP 6.3%，較去年同期高 0.7pp
  - 來源：Cox Automotive / J.D. Power via search summaries (cbtnews, beinsure)（as_of 2026-10-28）｜affects：valuation、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Ford 2008 全年虧損 146 億美元（上一輪金融危機下行）
  - 來源：GoAuto: Ford books record $US14.6b. loss（as_of 2009-01-30）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Trefis 稱 Ford 股價在 2008–2009 危機中跌幅 82%（同期 S&P 500 為 53%）
  - 來源：Trefis: How Low Can F Really Go In A Market Crash?（as_of 2026-05-16）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2020 疫情期間 Company adj. EBIT margin 全年 2.2%（2019 為 4.1%），Q2 2020 為 -10.0%，Q3 反彈至 9.7%
  - 來源：Ford Form 10-K FY2020 / Q3 2020 8-K（as_of 2021-02-01）｜affects：decision_inputs.bear、valuation
- `ma_merger#0`（ma_merger｜方向 -｜狀態 ok）：2025-12-09 BOSK 合資處分協議：Ford 子公司取得肯塔基兩座電池廠，Ford 退出 BOSK 持分
  - 來源：SEC EDGAR 8-K Item 2.06 (2025-12-15)（as_of 2025-12-15）｜affects：valuation、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K FY2025 列示 Hetsler v. Ford 產品責任案，判賠1.03億美元，上訴中
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2024 年起 E.D. Michigan 有證券集體訴訟（Guzman v. Ford，指保固準備金低估，期間至 2024-07-24）；為 2024 年案，非近12個月新案，現況未查證
  - 來源：BFA Law／Frank R. Cruz 律所新聞稿（搜尋摘要）（as_of 2024-09-24）｜affects：thesis.R、decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA 2024-11 對 Ford 課 1.65 億美元民事罰款（後視鏡頭召回延遲），同意令為期三年起、季度會議與獨立第三方監督，仍在監督期內；2026-08 Ford 聘 NHTSA 資深官員任首席汽車安全官。搜尋未見 2026 新罰款
  - 來源：NHTSA 新聞稿 Ford consent order 165 million civil penalty（搜尋摘要）／Ford Authority 2026-08（as_of 2024-11-14）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":25.2,"bear_5y_price":7.2,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":8.8,"ev5y_pct":11.8,"irr_base_pct":1.7,"asym_ratio":1.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.91,"pe":6.57,"basis":"FY2026E 共識調整後 EPS 1.91 美元（Koyfin 2026-10-31）、現價 12.55 美元；終端倍數同樣用調整後 EPS 口徑"},"eps":{"bull":[1.98,2.25,2.5,2.65,2.8],"base":[1.85,1.8,1.7,1.85,1.95],"bear":[1.65,1.35,0.7,0.95,1.2]},"pe":{"bull":9,"base":7,"bear":6},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":4.781,"net_buyback":0},"second_stage":{"bull_cagr_pct":3,"base_cagr_pct":1},"valuation_dependent":true}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### F_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 稱全年調整後 EBIT 指引收窄至 100–110 億美元，中點上調 10 億美元，原因為定價與組合（原話："increasing the midpoint by $1 billion, driven by strong"）
- 2026-07-28｜CFO｜guidance：全年調整後自由現金流指引上調至 60–70 億美元（原話："adjusted free cash flow to $6 billion to $7 billion"）
- 2026-07-28｜CFO｜guidance：資本支出指引不變，為 95–105 億美元（原話："capital expenditures remain unchanged at $9.5"）
- 2026-07-28｜CFO｜risk：CFO 說明指引未納入的情境：中東重大升級與美國經濟顯著下滑（原話："a significant escalation in the Middle East"）
- 2026-07-28｜CFO｜guidance：Ford Blue 全年 EBIT 指引上調為 50–55 億美元（原話："Ford Blue's EBIT range to $5 billion to"）
- 2026-07-28｜CFO｜guidance：Ford Pro 全年 EBIT 指引收窄為 70–75 億美元（原話："Ford Pro's EBIT range to $7 billion to $7.5 billion"）
- 2026-07-28｜CFO｜guidance：Model e 全年虧損預期改善至約 40 億美元，含約 10 億美元 UEV 與 Ford Energy 增量投資（原話："Model e losses to about $4 billion."）
- 2026-07-28｜CFO｜guidance：Ford Credit 全年 EBT 預期高於 25 億美元（原話："expected to be above $2.5 billion."）
- 2026-07-28｜CFO｜guidance：指引假設的美國 SAAR 區間為 1,600–1,650 萬輛（原話："a U.S. SAAR of 16 million to 16.5 million units"）
- 2026-07-28｜CFO｜guidance：美國產業定價全年預期上調約 0.5 個百分點至 +50bp（原話："about 0.5 point higher at plus 50 basis points"）
- 2026-07-28｜CFO｜guidance：Novelis 鋁供應中斷全年成本影響更新為約 15 億美元（原話："expect a full year cost impact of about $1.5 billion."）
- 2026-07-28｜CFO｜commitment：CFO 重申對 Novelis 復原計畫下全年淨 10 億美元 EBIT 改善有信心（原話："confident in our net $1 billion EBIT improvement"）
- 2026-07-28｜Ford Pro 總裁｜guidance：Ford Pro 下半年 EBIT 指引區間，對照上半年 34 億美元（原話："it's $3.6 billion to $4.1 billion."）
- 2026-07-28｜Ford Pro 總裁｜guidance：Ford Pro 預期年底恢復至 2025 年營收水準（原話："full recovery to Ford Pro's 2025 revenue run rate"）
- 2026-07-28｜CFO｜margin：CFO 拆解大宗商品逆風：全年略高於 20 億美元，下半年占約 15 億美元（原話："about $1.5 billion of that to be in the second half"）
- 2026-07-28｜CFO｜margin：CFO 說明下半年大宗商品額外衝擊約 9 億美元（原話："about $900 million additional to what we've already had"）
- 2026-07-28｜CFO｜margin：管理層稱第二季 EBIT 增長主要來自組合與淨定價（原話："this quarter's EBIT strength was largely a result of strong"）
- 2026-07-28｜CFO｜margin：Ford Blue 營收與 EBIT 成長歸因於美國法規調整與較高淨定價（原話："enabled by U.S. regulatory changes and higher net pricing"）
- 2026-07-28｜CFO｜margin：CFO 稱全年有 10 億美元材料與保固成本降幅，用於再投資 UEV 與 Ford Energy（原話："on track to deliver $1 billion in material and"）
- 2026-07-28｜CEO｜margin：Farley 稱縮小成本差距是達成 8% 利潤率的重要路線（原話："is continuing to close the cost gap"）
- 2026-07-28｜CEO｜margin：Farley 稱整合服務有可能為公司貢獻 0.5 個百分點利潤率（原話："integrated services being 0.5 point of margin"）
- 2026-07-28｜CEO｜margin：Farley 說明 Ford 只強調付費訂閱，不同公司口徑不同（原話："we are focused on paid subscription."）
- 2026-07-28｜CFO｜margin：CFO 澄清 160 萬付費訂閱含零售與 Pro，其中 Pro Intelligence 為 90 萬（原話："that does include retail plus Pro."）
- 2026-07-28｜CFO｜commitment：CFO 結語重申 2029 年 8% EBIT 利潤率目標（原話："firmly on the path to our 8% EBIT margin target by 2029"）
- 2026-07-28｜CFO｜commitment：CFO 重申維持投資等級與股東回報（原話："to our investment-grade rating and returning capital"）
- 2026-07-28｜CFO｜capital_allocation：宣布第三季定期股息每股 0.15 美元（原話："a third quarter regular dividend of $0.15 per share."）
- 2026-07-28｜CFO｜capital_allocation：BlueOval SK 處分認列 36 億美元一次性特殊項目費用（原話："special item charge of $3.6 billion"）
- 2026-07-28｜CFO｜capital_allocation：12 月公告相關剩餘現金費用最多 20 億美元，預計年底前完成大部分（原話："to be completed by the end of the year."）
- 2026-07-28｜CEO｜capital_allocation：Farley 表述資本紀律原則（原話："Every dollar must earn durable returns"）
- 2026-07-28｜CEO｜capital_allocation：Farley 稱國防業務須是強勁且資本回報良好的事業（原話："It has to be a strong business with really good returns"）
- 2026-07-28｜CEO｜product：Farley 稱 Ford Energy 預計 2027 年底前達年產能 20GWh（原話："By late next year, we expect to reach 20 gigawatt"）
- 2026-07-28｜CEO｜customer：Farley 自評 2028 年 20GWh 產能的銷售進度（原話："third inning of selling out the 2028 capacity"）
- 2026-07-28｜CEO｜capital_allocation：Farley 列出 Ford Energy 是否擴產的考量之一為稅務處理（原話："Obviously, the tax treatment is very"）
- 2026-07-28｜CEO｜product：Farley 描述 Ford Energy 回收期短（原話："but one with a very short payback."）
- 2026-07-28｜CEO｜customer：Farley 稱已與美國聯邦政府簽約生產 3 台基於 Super Duty 的軍用原型車（原話："with the U.S. federal government to produce 3 prototypes"）
- 2026-07-28｜CEO｜product：Oakville 擴產預計第四季啟動，新增最多 10 萬輛 Super Duty 產能（原話："on track to launch in the fourth quarter of this year"）
- 2026-07-28｜CEO｜product：UEV 平台首款車預計明年開始交車（原話："Customer deliveries will begin next year."）
- 2026-07-28｜CEO｜product：UEV 首款車起價約 3 萬美元（原話："It starts around $30,000."）
- 2026-07-28｜CEO｜product：Apple 將為每款 UEV 平台車提供內建地圖（原話："will be the embedded map provider for every UEV platform"）
- 2026-07-28｜CEO｜product：歐洲與 Geely 的協議，管理層稱可帶來速度與資本效率（原話："our agreement with Geely, which will bring speed and"）
- 2026-07-28｜CFO｜guidance：CFO 預期 2026 年 Gen 1 EBIT 較去年改善約 40%（原話："we expect to improve Gen 1 EBIT by approximately 40%"）
- 2026-07-28｜CFO｜product：總付費訂閱成長約 50%（原話："Total paid subscriptions grew about 50% to"）
- 2026-07-28｜CEO｜product：越野車款占美國第二季銷售 25%（原話："25% of our U.S. sales in the second quarter."）
- 2026-07-28｜Ford Blue 與 Model e 總裁｜guidance：Frick 稱預期目前的產品與系列組合水準將持續至年底（原話："that level of product mix and series mix to continue"）
- 2026-07-28｜CFO｜customer：2027 車型年北美客戶合約簽訂進度較去年提前（原話："contracting in North America is off to a fast start"）
- 2026-07-28｜Ford Blue 與 Model e 總裁｜competition：Frick 對比 F-Series 與競爭對手的租賃（rental）銷量（原話："we've had really low rental volume"）
- 2026-07-28｜CEO｜product：Farley 稱 F-Series 庫存約 45 天，對批發量有上行空間（原話："F-Series is around 45-day supply, which"）
- 2026-07-28｜CEO｜competition：Farley 表述 USMCA 立場：要讓美國車廠更易與日韓競爭（原話："to compete with Japan and South Korea"）
- 2026-07-28｜CEO｜commitment：Farley 稱支持修訂 USMCA 的條件（原話："prepared to support revising the USMCA so long as it"）
- 2026-07-28｜CEO｜risk：Farley 評價 Ford 對關稅的處理（原話："has done a good job with our exposure to tariffs"）
- 2026-07-28｜COO｜risk：Galhotra 稱今年召回約 1,200 萬輛，召回件數較去年下降（原話："we've recalled about 12 million vehicles"）
- 2026-07-28｜CFO｜guidance：Sherry 被問 2027 年時稱明年的 EBIT 方向現在說太早（原話："It's too early to say at this point."）
- 2026-07-28｜CFO｜guidance：CFO 稱 2027 年大宗商品衝擊規劃為四個季度，對照 2026 年三個季度（原話："we are planning for 4 quarters of impact versus 3"）
- 2026-07-28｜CFO｜margin：Ford Credit 第二季 EBT 數字（原話："EBT of $757 million, up $112 million"）

### 問答異常語氣（迴避／改口／保留）
- F_Q2_2026_Earnings_Call_20260728.md｜問：Spak 問為何下半年 F-Series 指引的量回升在低端、是否為審慎或競爭考量｜答法：先談庫存與需求強勁，被再問後 CFO 回答「就是組合」，未直接說明量回升偏低端的原因
- F_Q2_2026_Earnings_Call_20260728.md｜問：Percoco 問是否與超大規模雲端業者洽談直接購買 Ford Energy 產能｜答法：未直接回答超大規模雲端業者，改談廣泛客戶與專案報價流程，並稱內部預測不展開
- F_Q2_2026_Earnings_Call_20260728.md｜問：Delaney 問關稅進一步緩解空間與 USMCA 美國含量要求對 Ford 的影響｜答法：談立場與原則，關稅部分稱不談細節，未回應含量要求的具體影響
- F_Q2_2026_Earnings_Call_20260728.md｜問：Levy 請管理層重述與同業的成本差距｜答法：未給數字，只稱縮小成本差距是 8% 路線的重點並談下一代產品
- F_Q2_2026_Earnings_Call_20260728.md｜問：Rosner 問 2027 年 EBIT 淨效果是否較高｜答法：列出多項正反因素後，拒絕給方向，稱現在說太早
- F_Q2_2026_Earnings_Call_20260728.md｜問：Langan 問為何下半年 EBIT 年化後呈現放緩｜答法：逐項回答大宗商品與 Novelis 金額，對年化放緩以列舉下半年成本與投資回應，IR 最後提議會後另談模型細節
- F_Q2_2026_Earnings_Call_20260728.md｜問：Yu 問 Ford Defense 未來幾年可能規模｜答法：未給規模，只談 3 台原型車合約，並稱沒有其他可補充

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 4 | 0 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 7 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 6 | 3 |
| cyclical_inventory_price_position | found | 2 | 2 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：Ford Motor 10-K customer concentration no single customer 10% revenue dealers

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Ford Pro 商用車段持續 best-in-class margin（10%+）並擴大 SaaS recurring revenue","columns":{"2Y 驗證點":"2026 Ford Pro EBIT $6.5-7.5B（已 guide）；軟體訂閱破 100 萬","5Y 驗證點":"Ford Pro 占公司 EBIT > 60%；SaaS ARR > $1B","10Y 驗證點":"商用車 EV 化滲透 > 40% 時 Ford Pro 仍維持 8%+ margin（電動商用車段贏家）","具體數字門檻":"Pro EBIT margin ≥ 10%（連 2 季）；SaaS ARR 同比 +20%","信息來源":"Ford Q1 26 法說會 + 2025 10-K + Q4 25 投資者日","漂移觸發":"連 2 季 Pro margin"}},{"id":"H2","text":"Model e 段虧損漸縮 + Universal Platform $30K truck 證明可賺錢","columns":{"2Y 驗證點":"2026 Model e 虧損 $4-4.5B（已 guide）；Q4 26 季虧縮至","5Y 驗證點":"Universal Platform 首款車（2027/8）量產順利；2029 Model e 損平","10Y 驗證點":"EV 段占公司 EBIT > 0%（從虧轉盈）","具體數字門檻":"Model e 季虧 50K","信息來源":"Ford 2025/12 戰略簡報 + Kentucky $2B 投資案","漂移觸發":"季虧 > $1.3B 連 2 季 → 削弱；連 3 季 > $1.5B → 反轉"}},{"id":"H3","text":"OEM 圈估值倍數從目前 6-10x 區間 mean revert 至 10-12x（multiple re-rating）","columns":{"2Y 驗證點":"Fwd PE 從 9.2x 修復至 10x+ → 股價 +9%","5Y 驗證點":"OEM 圈整體估值結構性復甦（接近 SPX P/E）","10Y 驗證點":"—（不適用，10Y 看則 OEM 已被新 mobility 範式取代）","具體數字門檻":"同業中位 Fwd PE > 10x（Toyota 已 10.57x）","信息來源":"StockAnalysis.com / Macrotrends 5Y Fwd PE 歷史","漂移觸發":"同業中位"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Ford Pro margin 結構性壓縮（競爭 + 工資成本）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Ford Pro 季度 EBIT margin、SaaS 訂閱數","警戒閾值":"margin 連 2 季"}},{"id":"R2","text":"Model e Universal Platform 再次失敗（impairment 第二輪）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Kentucky 廠進度、$30K EV truck 預售訂單、Model e 季虧","警戒閾值":"Q4 26 季虧 > $1.3B / Q2 27 Universal Platform 預售"}},{"id":"R3","text":"Ford Credit 槓桿放大車市下行（信用收縮 + 壞帳率）","columns":{"對應假設":"H3（間接）","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Ford Credit 60+ delinquency rate、Net charge-off、ABS spread","警戒閾值":"delinquency > 4%（vs 目前 ~2.5%）/ ABS spread + 100bp"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"侵蝕","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":14.93,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"F","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Ford Motor Company"},"oneliner":"福特靠北美皮卡與商用車賺錢，前瞻本益比 6.6 倍加 4.8% 股息看似便宜，但盈餘處在循環晚段，調整後口徑又排除了幾乎年年出現的減損；基準情境年報酬約 6% 上下，不追，等股價 10 美元以下且車市未破底再研究。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/F_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺北美卡車、商用車與車隊客戶的錢。獲利集中在 Ford Pro 與 F-Series 皮卡，再加上 Ford Credit 的車貸利差；電動車部門每年吃掉約 40 億美元。產業處於高檔、開始鬆動的第三階段。","reasoning":"2026 年第三季營收 495 億美元，調整後 EBIT 26.58 億（利潤率 5.4%），GAAP 營業利益 14.54 億（2.9%），批發 104.9 萬輛。分部：Ford Pro 營收 178 億、EBIT 16.65 億；Ford Blue 營收 271 億、EBIT 13.92 億；Model e 營收 12 億、EBIT −10.58 億；Ford Credit EBT 8.03 億。全年指引調整後 EBIT 105–110 億，其中 Pro 約 70 億、Blue 約 55 億、Model e 約 −40 億、Credit 約 28 億（2026-10-28 CFO）。單點依賴：獲利高度集中在美國全尺寸皮卡與商用車（F-Series、Super Duty、Transit）；上游集中度也高，Novelis 一座廠供應美國車用鋁板約四成，2025 年這座廠失火，曾讓多款車停產。供需持久性屬週期性、將反轉：美國 9 月新車庫存升到 82 天，10 月獎勵金占 MSRP 6.3%、年增 0.7pp，全球 2026–27 年產量預測下修；供給可逆性高（GM 與 Hyundai 在美國擴產、中國出口）。產業態勢是雙向拉鋸：一邊是競爭惡化（中國出口、歐洲產能過剩、美國同業擴產），另一邊是部分結構轉好（Stellantis 削減歐洲產能約 80 萬輛、VW 再減約 100 萬輛）。其他結構變數裡，關稅與稀土管制影響最大。","fact_refs":["f_kpi0_gaap","f_kpi1_adjusted_ebit","f_kpi2_adjusted_ebit_margin","f_kpi3_gaap","f_kpi4_gaap","f_kpi10_adjusted_ebit","f_kpi12_wholesales","f_kpi13_ford_pro_ebit","f_kpi14_ford_blue_ebit","f_kpi15_ford_model_e_ebit","f_earnings_recency"],"verdict_values":{"revenue_quality":"以整車批發為主，收入隨景氣起落；軟體服務與零件約占第三季營收一成，毛利較高且有經常性；Ford Credit 賺車貸利差，衰退時信用損失會放大","unit_econ_note":"第三季每批發一輛車約對應 4.7 萬美元營收（495 億÷104.9 萬輛，含零件與 Credit），調整後 EBIT 約 2,500 美元（26.58 億÷104.9 萬輛）","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"高","fingerprint":"美國皮卡與商用車的需求量循環，加上電動車部門虧損收斂的轉機選擇權，以及自營車貸"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性、將反轉。美國新車庫存 9 月升到 82 天（8 月 75 天），10 月獎勵金占 MSRP 6.3%、年增 0.7pp（Cox、J.D. Power 2026-10）；全球輕型車 2026、2027 年產量預測各下修 170 萬與 250 萬輛（MarkLines 2026-07）。美國定價仍年增約 1%（2026-10-28 法說），尚未轉跌","bargaining":{"up":"上游強勢：2026 年大宗商品逆風接近 25 億美元，鋁板（Novelis）、稀土與車用晶片的供應都很集中","down":"下游中等：經銷商通路加上車隊年度議約；第三季 F-Series 獎勵金最低，車隊定價年增逾 1%","geo":"2025 年關稅對 EBIT 的淨影響約 20 億美元；中國稀土與零組件出口管制已造成停產"},"profit_pool_dir":"北美卡車與商用車利潤池持穩，歐洲乘用車與電動車利潤池在流出","tam_table":{"expanded":false,"reason":"成熟市場，Ford 沒有份額擴張的故事；美國量預測從 2026 年 1,610 萬輛到 2020 年代末 1,640 萬輛，大致持平。影響最大的變數是景氣與利潤率，不是 TAM"}}}},"q2_moat":{"verdict":"→：卡車與商用車的定價紀律守住，執行力也在改善，但美國市占下滑，趨勢無法往上。等級 C（執行 6 分、定價 6 分，中國車廠的生態攻擊扣 1 分）。","reasoning":"機制是規模加上品牌與服務網。F-Series 有望連續第 50 年拿下美國最暢銷皮卡，Transit 是美國最暢銷廂型車；Ford Pro 把車隊管理軟體、維修與融資綁在一起。可比軸方面，同業 ROIC 事實表未涵蓋，改看 TTM 利潤率：Ford 的毛利率與營業利益率都低於 GM、Stellantis、Toyota，但 Ford 的 TTM 含電動車減損與合資處分的特殊費用，同業的調整後數字又未涵蓋，所以利差方向只能確認對 Toyota 是大幅負值。趨勢不往上，是因為美國第二季市占 11.8%、排第四，第三季美國銷量年減 7%。趨勢也不往下，是因為第三季 F-Series 營收份額最高、獎勵金最低，車隊定價年增逾 1%；市占流失主要來自停產 Escape 與 Corsair。報酬持續期：當期 ROIC 無法從事實表算出；以 GAAP 計的增量報酬近零或為負，內生成長上界約 1%。","fact_refs":["f_peer_f_gross_margin_pct","f_peer_f_operating_margin_pct","f_peer_f_fcf_margin_pct","f_peer_gm_gross_margin_pct","f_peer_gm_operating_margin_pct","f_peer_gm_fcf_margin_pct","f_peer_stla_gross_margin_pct","f_peer_stla_operating_margin_pct","f_peer_stla_fcf_margin_pct","f_peer_tm_gross_margin_pct","f_peer_tm_operating_margin_pct","f_peer_tm_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模加上品牌與服務網：F-Series、Super Duty、Transit 在美國全尺寸皮卡與商用車領先，Ford Pro 再用車隊管理軟體、維修與融資綁住客戶","execution":6,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力在改善：J.D. Power 2026 年新車品質調查居首；保固與材料成本 2025 年降 15 億美元、2026 年再降 10 億；Oakville Super Duty 爬坡進度超前。定價力持穩：第三季 F-Series 營收份額最高、獎勵金最低，車隊定價年增逾 1%，2027 車型年車隊訂單符合預期（2026-10-28 CFO、Frick、Davis）。美國市占下滑讓趨勢不能往上；這項與中國威脅都記在威脅欄，不再重複扣在趨勢上","competitor_notes":[{"name":"GM","strategy_note":"同樣靠北美全尺寸皮卡與 SUV 賺錢，2027 年初在 Orion 加產汽油車款，是 F-Series 利潤池最直接的對手；TTM 利潤率高於 Ford，但 Ford 的 TTM 含大額特殊費用，口徑不完全可比"},{"name":"STLA","strategy_note":"Ram 皮卡在美國與 Ford 正面競爭，但公司正在重整、削減歐洲產能約 80 萬輛，TTM 自由現金流為負，短期內價格侵略性有限"},{"name":"TM","strategy_note":"利潤率明顯領先所有同業，是成本與品質的標竿；在美國全尺寸皮卡份額小，對 Ford 的威脅主要在混合動力與乘用車"}],"spread_notes":{"axis":"TTM 營業利益率（GAAP）","reading":"Ford 對最強同業 Toyota 的利差為大幅負值，對 GM 也是負值；Ford 數字含特殊費用，同業的調整後數字事實表未涵蓋，無法確認利差是否在收窄"},"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用營業利益率當可比軸","threats":[{"level":"🔴","text":"中國車廠以軟體定義與低成本電動車擴張，歐洲、東南亞、拉美已受壓，CEO 稱 5–10 年內可能進美國；屬生態攻擊","p":"30%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"GM 2027 年初在 Orion 加產汽油全尺寸皮卡與 SUV，產業的折扣與促銷已經重現，F-Series 的價格紀律會受考驗","p":"40%","evidence_refs":["cyclical_supply_discipline_capacity#2","competitive_share_entrants#0"]},{"level":"🟡","text":"美國市占下滑：第二季 11.8% 排第四，第三季美國銷量年減 7%，7 月 Ford 品牌年減 9.1%；部分來自主動停產 Escape 與 Corsair","p":"50%","evidence_refs":["end_markets#3","end_markets#4","competitive_share_entrants#3"]},{"level":"🟡","text":"Hyundai 美國投資加碼到 260 億美元，Metaplant 目標 2028 年年產 50 萬輛，美國產能增加","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#3"]}],"roic_durability":{"quadrant":"低利益率、周轉率未證：調整後 EBIT 利潤率約 5–6%；合併報表含 Ford Credit 大額融資資產，投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"卡車與商用車對車隊客戶是生產工具，屬於需要而非想要，2027 車型年車隊訂單與定價符合預期；但延後換車的代價低。美國量預測到 2020 年代末約 1,640 萬輛，低於疫情前約 1,700 萬，負擔能力是主要障礙（Mobility Global 2026-07）"},{"item":"決策層級","level":"🟡","text":"車隊採購的最小決策單位是年度議約，GM 與 Ram 都能替代。綁定來自 Ford Pro 的車隊管理軟體、維修與融資：同時有軟體訂閱與定期保養的客戶，零件留存率高約 9 個百分點（2026-10-28 CEO），數位車隊管理年底將超過 10 萬台、多數不是 Ford 車。但漲價後的流失率與分客群續約率未揭露"},{"item":"價值鏈分配","level":"🔴","text":"Ford 在上游是價格接受者：2026 年大宗商品逆風接近 25 億美元，2027 年再約 20 億；2025 年關稅對 EBIT 淨影響約 20 億；一座 Novelis 廠供應美國車用鋁板約四成，失火就讓多款車停產；中國稀土與晶片管制造成停產與成本上升。整條價值鏈裡，Ford 只拿到約 5–6% 的調整後 EBIT 利潤率"},{"item":"社會容忍度","level":"🟡","text":"新車負擔能力已是政治議題，美國近半新車成交價低於 4 萬美元，產業定價年增約 1% 已接近上限；NHTSA 1.65 億美元同意令仍在監督期，關稅與 USMCA 修訂直接影響成本；不依賴單一監管授權"}],"roiic":"為負，絕對值算不出。分子：GAAP 營業利益 2023→2024 年減少 2.4 億美元（52.2−54.6），2023→2025 年減少 146.4 億（−91.8−54.6，含特殊費用）。分母取期間累計資本支出（現金口徑），2024、2025 年的金額事實表未涵蓋，但資本支出一定為正，所以可以確定是負值。不含 2025 年大額費用的 2023→2024 年也是負值：營收多 88.1 億（1,850−1,761.9），營業利益反而少 2.4 億，增量營收的營業利益率約 −2.7%","reinvest_rate":"毛額約 86%–100%：2026 年資本支出指引 95–105 億美元 ÷ 調整後 EBIT 指引 105–110 億（下緣 95÷110≈86%，上緣 105÷105＝100%）。這是毛額、稅前的近似值。折舊攤銷與稅後營業利益事實表未涵蓋，所以淨再投資率算不出。用毛額會高估，用稅前分母會低估，兩者合起來偏哪一邊無法確定。維持性與成長性資本支出的拆分未揭露","endo_ceiling":1,"formula_note":"內生成長上界＝增量資本報酬×再投資率。代入後，增量資本報酬為負（見上欄：分子 −2.4 億與 −146.4 億美元，分母為正），再投資率毛額約 86%–100%，兩者相乘為負，公式值低於 0%。數字來源：營收 2023 年 1,761.9 億、2024 年 1,850 億、2025 年 1,872.7 億、2026E 共識 1,759.4 億；GAAP 營業利益 2023 年約 54.6 億（3.1%×1,761.9 億）、2024 年約 52.2 億（2.82%×1,850 億）、2025 年約 −91.8 億（−4.9%×1,872.7 億）。欄位填的 1% 不是公式算出來的，是取整後的下限。公式值為負，表示新增資本沒有換到新增獲利，但不表示盈餘一定萎縮：美國定價仍年增約 1%（2026-10-28 法說），漲價這部分不需要新增資本。1% 比公式值寬鬆，並不保守。改填 0% 時，與共識 EPS 年化約 4.6% 的缺口由 3.6pp 擴大到 4.6pp，但超出內生上界的判定不變，缺口一樣只能用 Model e 減虧與降本帶來的利潤率擴張解釋。可能算錯的地方：分母若改用帳面投入資本，2025 年的電動車減損會把帳面資本一起打掉，分子分母同時為負，算出來反而是正值。這裡用現金口徑，因為錢已經花出去，減損只是在承認這筆投資的報酬為負"}}}},"q3_growth":{"verdict":"🟡：北美核心車市已經飽和；第二條曲線（儲能、軟體服務）有公司提出的證據，但相對 1,760 億美元營收量體太小。成長來自虧損收斂與降成本，不是營收擴張。","reasoning":"成長拆解：量持平偏降，價格與組合撐住營收，沒有併購，也沒有淨回購。共識 EPS：FY2026E 1.91、FY2027E 1.91、FY2028E 2.09 美元（Koyfin 2026-10-31，家數未揭露）。FY2025A 的調整後 EPS 事實表未涵蓋，只能算 FY2026E 到 FY2028E 兩年年化約 4.6%。共識營收 FY2026E 1,759 億、FY2027E 1,797 億（+2.1%）。內生上界約 1%（見護城河段），缺口約 3.6pp，歸因於利潤率擴張：Model e 年虧從約 40 億往 2029 年損平收斂、每年約 10 億美元的材料與保固降本、軟體服務與零件組合提升。缺口可以歸因，不靠倍數回升。跑道：核心市場滲透已到頂，以年數計算不適用；第二條曲線存在，所以不落最差一檔，但量體不足以給寬跑道。衰退訊號亮兩項（GAAP 毛利率連年下滑、核心市占縮減），另有兩項資料缺口（產業倍數三年走勢、維持性資本支出占比）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi15_ford_model_e_ebit","f_kpi12_wholesales"],"verdict_values":{"growth":{"driver_mix":"量持平偏降，價格與組合撐住營收；沒有併購、沒有淨回購；EPS 成長主要靠 Model e 虧損收斂與降成本","runway_years":"不適用（成熟市場，美國市占約 12%）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬近零：2023 年到 2026E 營收持平，同期 GAAP 營業利益下滑，內生成長上界取 1%（推導見護城河段的報酬持續期）","segments":[{"item":"Ford Pro（商用車與車隊服務）","value":"2026 年第三季營收 178 億美元（+2%）、EBIT 16.65 億（前年同期 19.85 億）；全年 EBIT 約 70 億"},{"item":"Ford Blue（燃油與混動）","value":"第三季營收 271 億美元（−3%）、EBIT 13.92 億；全年 EBIT 約 55 億"},{"item":"Ford Model e（電動車）","value":"第三季營收 12 億美元（−31%）、EBIT −10.58 億；全年虧損約 40 億，目標 2029 年損平"},{"item":"Ford Credit","value":"第三季 EBT 8.03 億美元（年增 1.72 億）；全年約 28 億"},{"item":"軟體服務與零件（跨分部）","value":"約占第三季營收一成，毛利率高於整車"},{"item":"Ford Energy（儲能）","value":"2027 年底達 20 GWh 年產能，投資約 20 億美元（2026 年花三分之一、2027 年花三分之二）；目前尚無營收"}],"decay_signals":[{"signal":"毛利率連兩季年減","status":"亮","evidence":"季度毛利率事實表未涵蓋；年度 GAAP 毛利率 2022 年 10.86%、2023 年 9.17%、2024 年 8.38%、2025 年 0.9%，連年下滑（2025 年含特殊費用）"},{"signal":"核心市占近 12 個月縮減","status":"亮","evidence":"美國第二季市占 11.8%、排第四；1–9 月美國銷量年減 8.6%，同期產業 SAAR 大致持平"},{"signal":"主力產品提價後銷量下滑","status":"未亮","evidence":"第三季 F-Series 營收份額最高、獎勵金最低；銷量下降主因是停產 Escape、Corsair"},{"signal":"EPS 成長高於營收成長逾 5pp","status":"未亮","evidence":"共識 EPS 兩年年化約 4.6%，營收約 2%，差距約 2.6pp"},{"signal":"FCF 對淨利低於 0.75 倍連兩年","status":"未亮","evidence":"2023 年約 1.5 倍、2024 年約 1.1 倍"},{"signal":"SBC 占營收逾 5% 且逐年上升","status":"未亮","evidence":"年化約 0.25%"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","evidence":"美國量持平在 1,610–1,640 萬輛；中國軟體定義電動車的威脅記在護城河威脅欄"},{"signal":"產業估值倍數近三年系統性下移","status":"資料缺口","evidence":"同業本益比歷史事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 逾六成","status":"資料缺口","evidence":"資本支出 95–105 億美元高於自由現金流 60–70 億，但維持性與成長性的拆分未揭露"},{"signal":"停止投資新產能且營收三年內下滑","status":"未亮","evidence":"仍在投資 Oakville、UEV 與肯塔基儲能"}],"trap_rating":"🟡（亮兩項）"}}},"q4_capital":{"verdict":"現金流付得起股息，但過去投入電動車的資本大量減損，增量資本報酬差；資本回饋只有股息，沒有回購。","reasoning":"第三季營業現金流 54 億美元、調整後自由現金流 47 億，GAAP 淨利 20.49 億（EPS 0.50）。全年調整後自由現金流指引 60–70 億，資本支出 95–105 億。定期股息每季每股 0.15 美元，以約 39.93 億股計，一年約 24 億美元，自由現金流覆蓋約 2.5–2.9 倍。年度 FCF 對淨利：2023 年約 1.5 倍、2024 年約 1.1 倍（年度 FCF 含 Ford Credit 現金流，與公司的調整後口徑不同）；2025 年淨利為負，不適用。前九個月 SBC 3.24 億美元，年化約占營收 0.25%。股數 2023 年約 40.25 億（淨利 43.47 億÷稀釋 EPS 1.08），目前 39.93 億，淨稀釋近零。季末現金 253 億、總流動性 464 億（2026-10-28 CFO）。現金去向四分、汽車部門債務的到期結構與加權利率、回購金額，事實表皆未涵蓋。","fact_refs":["f_kpi5_eps_gaap","f_kpi7","f_kpi8_adjusted","f_kpi9_sbc_9","f_kpi11_adjusted_fcf_capex","f_dividend_yield_ttm","f_shares_diluted_m","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"BlueOval SK 電池合資投入後又處分，2026 年第二季認列 36 億美元特殊費用，剩餘現金費用最多 20 億（2026-07-28 CFO）；已實現報酬為負"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"回購金額事實表未涵蓋，兩場法說都只提定期股息；股數 2023 年至今大致持平"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九個月 SBC 3.24 億美元；股數從 2023 年約 40.25 億降到目前 39.93 億，淨稀釋近零，低於每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；資本回饋只有每季每股 0.15 美元的定期股息，回購與特別股息金額事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價只要求調整後 EPS 在下一次溫和衰退中守住 1.7 美元以上、股息不砍，就有約 6% 上下的年報酬。要賺得更多，得靠 2029 年 8% 利潤率兌現，這點我只部分相信。估值合理，不算便宜。","reasoning":"前瞻本益比 6.57 倍（12.54÷FY2026E 的 1.91），FY2027E 也是 1.91，等於市場只給持平盈餘。股息殖利率 4.8%，調整後自由現金流指引相當於市值的 12–14%。但分母有爭議：2022–2025 年 GAAP 稀釋 EPS 合計約 −0.01 美元，調整後口徑排除了 2022 年、2025 年與 2026 年第二季的大額特殊費用。P/S 0.27 倍位在自身 4 個年度端點的 97 分位，EV/S 1.02 倍在 87 分位（都不是五年分位；EV 含 Ford Credit 融資債務，EV/S 失真，不拿來當錨）。五年本益比區間事實表未涵蓋，分位留空。PEG 約 1.4（6.57÷FY2026E 到 FY2028E 年化 4.6%）。短期目標 12.95 美元（FY2027E 基準 EPS 1.85×7 倍，+3%）；五年目標 13.65 美元（1.95×7 倍，+9%，不含股息）。賣方均價 14.88 美元（25 家、評等為持有、資料停在 2026-08），比現價高約 19%，但還沒反映 10 月的 2027 年持平指引，以及 FY2027、FY2028 共識的微幅下修。FY2026E 近三個月上修 5.5%，主要反映今年已實現的部分。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_net_debt_m","f_ev_m","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"以前瞻本益比（FY2026E 調整後 EPS）為主，自由現金流殖利率與股息覆蓋為輔；EV 倍數因淨負債含 Ford Credit 融資債務而失真，不拿來當錨","tier":"美國傳統車廠","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比，無法做倍數對照；終端倍數只能以自身現值 6.6 倍校準，這是本次估值已知的缺口"},"fwd_pe":6.57,"peg":1.43,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"便宜的一面：本益比 6.6 倍、股息殖利率 4.8%、自由現金流殖利率 12–14%。不便宜的一面：調整後 EPS 排除了經常性特殊費用，四年 GAAP EPS 合計近零；P/S 在自身年度端點的高檔，盈餘處在循環晚段；基準情境含一次溫和衰退，年報酬約 6% 上下，低於 8% 的及格線。分母有爭議時，便宜的論證不成立，綜合判斷為合理","targets":{"short_usd":12.95,"mid_usd":13.65,"basis":"短期＝FY2027E 基準 EPS 1.85×7 倍；中期＝FY2031E 基準 EPS 1.95×7 倍"},"upside_short_pct":3.2,"upside_mid_pct":8.8,"denominator_disputed":true,"denominator_note":"調整後 EPS 排除了幾乎每年都有的特殊項目：2022 年與 2025 年 GAAP 虧損，以及 2026 年第二季 BlueOval SK 處分費用 36 億美元；2022–2025 年 GAAP EPS 合計約 −0.01 美元。6.6 倍本益比用的是排除電動車減損後的分母，所以改用自由現金流對股息的覆蓋，以及含衰退的基準情境報酬來判斷"}}},"q6_how_wrong":{"verdict":"🟡：最可能看錯的方向是太保守。若 2029 年 8% 利潤率兌現，EPS 約 2.6 美元，給 8 倍就是 21 美元。最痛的錯則是太樂觀：衰退若與 UEV、儲能的投資高峰重疊，股價可能回到 5–7 美元。","reasoning":"反證寫在反證紀錄，三個視角各一條。歷史回撤：2008–09 年股價跌 82%（同期標普 −53%），2020 年第二季調整後 EBIT 利潤率 −10%。訴訟與監管：Hetsler 產品責任案判賠 1.03 億美元，上訴中；NHTSA 2024-11 同意令罰款 1.65 億美元，監督期三年；2024 年的證券集體訴訟現況未查證。管理層迴避：前一季（2026-07-28）沒給與同業的成本差距數字，沒回答儲能是否與超大型雲端業者洽談，對 2027 年方向說「現在說太早」；本季（2026-10-28）改口說 2027 年與 2026 年大致持平，儲能的 backlog 仍不揭露。技術面：股價 12.61 美元，在 52 週均線 13.16 之下，在 104 週均線 11.61 與 250 週均線 10.86 之上；250 週均線 13 週斜率 −0.67%；RSI 54.7，不過熱。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"低本益比的循環股：便宜可能只是晚段盈餘，加上被排除的經常性減損"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.91,"pe":6.57,"basis":"FY2026E 共識調整後 EPS 1.91 美元（Koyfin 2026-10-31）、現價 12.55 美元；終端倍數同樣用調整後 EPS 口徑"},"eps":{"bull":[1.98,2.25,2.5,2.65,2.8],"base":[1.85,1.8,1.7,1.85,1.95],"bear":[1.65,1.35,0.7,0.95,1.2]},"pe":{"bull":9,"base":7,"bear":6},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":4.78,"net_buyback":0},"second_stage":{"bull_cagr_pct":3,"base_cagr_pct":1},"max_dd":{"lo":-65,"hi":-40,"basis":"衰退情境下 EPS 落到約 0.7 美元（調整後 EBIT 約 40 億、利潤率約 2%，對照 2020 年全年 2.2%）。市場在谷底通常用 8–10 倍往後看，對應股價約 5.6–7.0 美元，即 −44%～−55%；溫和放緩則只到 −40%。下緣取 −65%，參考 2008–09 年的 −82%，但不假設金融危機式的信用崩潰。起點本益比已低，4.8% 股息也提供部分支撐","trigger_time":null},"basis":{"bull":"2029 年調整後 EBIT 利潤率接近 8%（約 148 億美元；以目前每 10 億 EBIT 約對應 0.18 美元 EPS 換算，EPS 約 2.6 美元），Model e 損平、儲能開始貢獻，衰退輕微；終端 9 倍","base":"2027 年獲利與 2026 年持平，2028–2029 年遇一次溫和衰退（EPS 低點 1.70），2031 年回到約 1.95；給 7 倍，略高於自身現值 6.6 倍，因為終端年落在復甦段；同業前瞻本益比事實表未涵蓋","bear":"2028–2029 年衰退與 UEV、儲能投資高峰重疊，EPS 谷底 0.70（調整後 EBIT 約 40 億、利潤率約 2%，對照 2020 年 2.2%），中國競爭壓低復甦高度，2031 年只到 1.20；給 6 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2008 年全年虧損 146 億美元，股價在 2008–09 年跌 82%；2020 年第二季調整後 EBIT 利潤率 −10%、全年 2.2%。目前產業庫存 82 天且還在升，獎勵金 6.3%、年增 0.7pp，全球輕型車產量預測下修","assumption":"論點假設北美卡車利潤池在下一次衰退中只會縮水，不會崩","consequence":"若 2028 年的衰退與 UEV、儲能的投資高峰重疊，調整後 EPS 可能跌到 0.7 美元、股息被砍，股價落到 5–6 美元（跌幅超過 50%）","ruling":"採納。空頭機率取 30%，最大回撤下緣取 −65%；這條與 Single Thing 指向同一件事（北美衰退），不另設","watch":"每月 SAAR、產業庫存天數、獎勵金占 MSRP、Ford Credit 逾期率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_inventory_price_position#1","supply_demand_durability#0"]},{"view":"論點成功但股東經濟變差","evidence":"BlueOval SK 處分認列 36 億美元特殊費用，剩餘現金費用最多 20 億（2026-07-28 CFO）。2022–2025 年 GAAP 淨利合計約 0.6 億美元（−19.8＋43.5＋58.8－81.8 億）。2026 年資本支出 95–105 億，高於調整後自由現金流 60–70 億；2027 年儲能、UEV、歐洲合作的投資還會再增加","assumption":"假設調整後盈餘改善，就等於股東拿得到的錢","consequence":"就算 2029 年 8% 利潤率達標，只要每隔兩三年就有數十億美元的減損與重組現金支出，每股價值的累積會遠低於調整後 EPS 呈現的樣子，而且股息之外沒有回購","ruling":"採納。估值分母列為有爭議，便宜的論證打折，終端倍數不給回升","watch":"每年特殊項目費用金額、GAAP EPS 占調整後 EPS 的比例","evidence_refs":["major_events#0","ma_merger#0"]},{"view":"價格已反映太多","evidence":"P/S 0.27 倍在自身 4 個年度端點的 97 分位，EV/S 在 87 分位（都不是五年分位）；26 週上漲 11.6%；共識 FY2027E EPS 1.91 與 2026 年持平","assumption":"假設 6.6 倍本益比代表市場已經很悲觀","consequence":"如果現價對應的是晚段盈餘，低本益比就不是安全邊際；衰退一來 EPS 下修，倍數也不會擴張","ruling":"部分採納。現價沒有反映 8% 利潤率，但也沒有反映衰退；循環晚段不追","watch":"FY2027E 共識 EPS 的修正方向；股價相對 52 週均線 13.16 美元的位置","fact_refs":["f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_consensus_eps_fy2","f_ma_w52"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 14.93 → 本次 12.55（-15.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=14.93","side_b":"本次 price_at_dd=12.55","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 14.93 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 14.93 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 14.93 美元：Bull 價 25.2、Bear 價 7.2，五年期望值 −6.1%，基準年化 −1.8%，不對稱比 0.89","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.89。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 14.93 美元：五年期望值 −6.1%，基準年化 −1.8%，不對稱比 0.89","side_b":"本次情境、股價 12.55 美元：五年期望值 +11.8%，基準年化 1.7%，不對稱比 1.58","ruling":"再換股價、情境不動：起點價下跌 15.9%，五年期望值多 17.8 個百分點，基準年化多 3.5 個百分點，不對稱比由 0.89 升到 1.58。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：整體評等、護城河方向、價值陷阱","cause":"新證據","prior_field":["signal","moat_trend","trap"],"side_a":"前份（2026-05-24，股價 14.93 美元）：整體評等 B；護城河方向為侵蝕；價值陷阱 🟡","side_b":"本次：整體評等 C；護城河方向 →；價值陷阱 🟡，不變","ruling":"評等下調是因為新證據，不是因為股價。前份第一條假設要求 Ford Pro 利潤率連兩季 ≥ 10%，2026 年第三季只有 9.4%；Pro 全年指引落到前一季區間的下緣，約 70 億；管理層對 2027 年只給與 2026 年大致持平，且 Model e 2027 年費用更高；FY2027、FY2028 共識 EPS 近期各下修約 0.5% 與 1%。護城河方向由侵蝕改為持平：第三季 F-Series 營收份額最高、獎勵金最低，車隊定價年增逾 1%；美國市占下滑主要來自停產車款，改記在威脅欄，不重複扣在趨勢上。價值陷阱同為 🟡，亮的兩項是 GAAP 毛利率連年下滑與核心市占縮減","evidence_level":"公司季報與法說（2026-10-28），以及 Experian 與 Ford Authority 的銷量統計","settle_metric":"2027 年全年調整後 EBIT 指引與 Ford Pro 季利潤率","if_then":["若 2027 年指引 ≥ 105 億美元，且 Ford Pro 季利潤率回到 10% 以上 → 整體評等回到 B","若 F-Series 獎勵金占售價比的年增幅超過產業平均，或車隊定價轉為年減 → 護城河方向改判 ↓，改為迴避"],"evidence_refs":["end_markets#3","end_markets#4"]},{"axis":"前份漂移：估值結論、成長跑道、公司類型、循環位置、回撤與情境機率","cause":"方法變動","prior_field":["val","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：估值結論 🟢，第三條假設靠同業前瞻本益比回到 10 倍以上；成長跑道、公司類型、循環位置、最大回撤、多空機率、裁決與角色都沒有輸出","side_b":"本次：估值結論 🟡，不假設倍數回升，改以調整後 EPS 分母有爭議與循環晚段來處理；成長跑道 🟡；類型為循環股（次要為轉機）；循環位置在晚段；最大回撤 −40%～−65%；多頭 20%、空頭 30%；裁決與角色由程式依新輸入產生","ruling":"股價從 14.93 跌到 12.55 美元，本益比更低，估值結論反而由便宜改為合理，主因在方法：前份把倍數回升當基準，本次改用自身盈餘分母校準。2022–2025 年 GAAP EPS 合計約 −0.01 美元，6.6 倍本益比的分母排除了電動車減損，便宜的論證要打折。其餘欄位前份為空，本次依新框架補齊","evidence_level":"公司 2022–2025 年度財報，以及 2026-07-28 法說 CFO 揭露的特殊費用","settle_metric":"2027 年特殊項目費用總額、GAAP EPS 占調整後 EPS 的比例","if_then":["若 2027 年 GAAP EPS ≥ 調整後 EPS 的 80% → 接受調整後分母，估值結論可回到便宜","若 2027 年再認列 ≥ 20 億美元的電動車或重組特殊費用 → 終端倍數下修到 6 倍"],"evidence_refs":["major_events#0"]},{"axis":"前份假設與風險門檻改動","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：Ford Pro EBIT 利潤率 ≥ 10%（連 2 季）；Model e 2026 年第四季季虧 > 13 億美元為警戒；同業中位前瞻本益比 > 10 倍（倍數回升）；Ford Credit 60 天以上逾期率 > 4%","side_b":"本次：Ford Pro 單季利潤率連兩季 < 8% 才減碼；Model e 第四季季虧 > 13 億美元沿用；倍數回升假設退休；Ford Credit 逾期率 > 4% 沿用（現值為資料缺口）","ruling":"Pro 門檻由 10% 降到 8%，不是重新定義什麼叫成功：前份門檻已在 2026 年第三季跌破（9.4%），這筆記為前份第一條假設削弱。降門檻的依據是第三季壓力來自大宗商品與 Oakville 爬坡的暫時成本（2026-10-28 CFO），車隊定價仍年增逾 1%。若 2027 年 Oakville 爬坡完成後 Pro 季利潤率仍 < 9%，直接視同反轉。倍數回升假設退休，因為 FY2027、FY2028 共識微幅下修，2027 年又只給持平獲利，看不到倍數回升的催化","evidence_level":"公司季報分部表與法說","settle_metric":"2027 年 Ford Pro 季利潤率","if_then":["若 2027 年下半年 Pro 季利潤率 < 9% → 減碼三分之一，Pro 假設判反轉","若連兩季 ≥ 10% → 門檻回到 10%"]},{"axis":"Single Thing 唯一致命點首次設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing：未設定（null）","side_b":"本次 Single Thing：美國車市進入衰退，輕型車 SAAR 季均連兩季低於 1,450 萬輛；一旦發生，減碼至半倉","ruling":"前份框架沒有要求唯一致命點。本次依數學上最大的單一敏感度，選北美量價：北美卡車與商用車是獲利主體，2020 年全年調整後 EBIT 利潤率只有 2.2%，公司指引也明說不含美國經濟顯著下滑","evidence_level":"公司指引假設與 2020 年歷史數據","settle_metric":"美國 SAAR 季均","if_then":["若 SAAR 連兩季 < 1,450 萬輛 → 減碼至半倉","若同時 Ford Credit 逾期率 > 4% → 清倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"axis":"減碼與清倉門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份減碼／清倉指標：未設定（null）","side_b":"本次：SAAR 連兩季 < 1,450 萬輛 → 減碼至半倉；Ford Pro 單季利潤率連兩季 < 8% → 減碼三分之一；全年調整後自由現金流 < 30 億美元或削減股息 → 清倉；Ford Credit 逾期率 > 4% 且 SAAR 門檻同時成立 → 清倉","ruling":"前份只有風險警戒值，沒有對應動作。本次每條門檻都綁定具體動作，避免看到訊號卻沒有執行","evidence_level":"方法調整","settle_metric":"各指標的季度讀數","if_then":["任一減碼門檻觸發 → 依該條減碼","清倉門檻觸發 → 一次清倉，不分批"]},{"axis":"重新研究條件首次設定","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重新進場條件：未設定（null）","side_b":"本次：股價 ≤ 10 美元，且美國 SAAR 季均仍 ≥ 1,550 萬輛；觸發後重做完整研究，通過才分批建立首筆","ruling":"本次不追的約束是兩件事同時成立：盈餘處在循環晚段，以及調整後分母有爭議。重啟條件就是把這個約束反過來：價格先補償下行風險（10 美元約為 FY2027E 共識的 5.2 倍、股息殖利率 6%），同時景氣尚未破底","evidence_level":"本次的估值與循環位置判斷","settle_metric":"股價與 SAAR","if_then":["兩個條件同時成立 → 重做研究，通過後分批建立首筆","只有股價到位，但 SAAR < 1,550 萬輛 → 不買，等 SAAR 連兩月回升"]},{"axis":"管理層前後說法：Ford Pro 指引與成本逆風","cause":"新證據","prior_field":null,"side_a":"2026-07-28 法說 CFO：Ford Pro 全年 EBIT 70–75 億美元、下半年 36–41 億；大宗商品逆風略高於 20 億；2027 年方向「現在說太早」","side_b":"2026-10-28 法說 CFO：Ford Pro 全年約 70 億（區間下緣）；大宗商品逆風接近 25 億，增加約 5 億；全公司調整後 EBIT 下緣上調到 105 億，Ford Blue 約 55 億，落在區間上緣；CEO 稱 2027 年獲利與 2026 年大致持平","ruling":"可調和，屬程度差異：Pro 下修來自成本而不是定價，全公司靠組合與定價補回。但 Ford Pro 是本檔最強的一塊，指引往下緣走，要算削弱。第四季 Pro EBIT 隱含約 19.4 億美元（70 億 − 上半年 34 億 − 第三季 16.65 億）","evidence_level":"兩場法說逐字稿","settle_metric":"2026 年第四季 Ford Pro EBIT","if_then":["若第四季 Pro EBIT < 17 億美元 → 停止加碼，並把 2027 年 Pro EBIT 預估降到 65 億以下","若 ≥ 20 億美元 → 維持 Pro 假設"]},{"axis":"儲能訂單的證據品質","cause":"新證據","prior_field":null,"side_a":"2026-10-28 CEO：已簽約加上後期議約，合計超過 2028 年產能的八成，預期 2027 年第一季全數承諾","side_b":"同場儲能總裁 Carroll：今天不談 backlog，明年才開始揭露；前一季（2026-07-28）CEO 自稱 2028 年產能的銷售進度在「第三局」，也沒回答是否與超大型雲端業者洽談","ruling":"不採信，也不否定：八成裡含後期議約，不是確定訂單，列為未證、持續監測。若 2027 年首次揭露的已簽約量低於 2028 年產能的 60%（約 12 GWh），判定說法證偽，儲能不計入任何情境；目前只放在多頭情境","evidence_level":"管理層口述，尚無揭露數字","settle_metric":"2027 年首次揭露的儲能已簽約 GWh","if_then":["已簽約 < 12 GWh → 多頭機率由 20% 降到 15%","已簽約 ≥ 20 GWh，且 2029–2030 年也有簽約 → 維持多頭情境，並把儲能列入基準情境"]},{"axis":"便宜與否：低本益比對上循環晚段盈餘","cause":null,"prior_field":null,"side_a":"便宜：前瞻本益比 6.6 倍、股息殖利率 4.8%，調整後自由現金流指引相當於市值的 12–14%，足以支付約 2.5 倍股息","side_b":"不便宜：調整後 EPS 排除了經常性特殊費用（2022–2025 年 GAAP EPS 合計約 −0.01 美元）；P/S 在自身 4 個年度端點的 97 分位；產業庫存與獎勵金上升，盈餘處在循環晚段","ruling":"⚖ 不可調和（方向相反），裁定站在不便宜這一側。依據：基準情境含一次溫和衰退，5 年年報酬約 6% 上下，補償不了 −40%～−65% 的回撤風險；四年 GAAP 盈餘合計近零是硬數據。現在就買的最強論證：自由現金流殖利率 12–14%，F-Series 的定價紀律與 Ford Pro 軟體服務成長都是真的，市場卻只給持平盈餘 6.6 倍；若 2029 年 8% 利潤率兌現，EPS 約 2.6 美元，給 8 倍就是約 21 美元，比現價高約 66%。不採納，因為這個論證完全依賴管理層的調整口徑，以及尚未發生的利潤率目標","evidence_level":"公司年度財報、季報與產業庫存統計","settle_metric":"2027 年 GAAP EPS 占調整後 EPS 的比例、美國 SAAR","if_then":["若股價 ≤ 10 美元且 SAAR 季均 ≥ 1,550 萬輛 → 重做研究，通過後分批建立首筆","反向：若 2027 年 GAAP EPS ≥ 調整後 EPS 的 80%，且調整後 EBIT ≥ 105 億美元 → 接受調整後分母，股價 ≤ 12 美元即分批建立首筆","價格先走、證據未到：股價漲過 14 美元，但 2027 年指引未確認 → 不追；已持有者分批了結三分之一"],"evidence_refs":["cyclical_inventory_price_position#1"]}],"triggers":[{"n":1,"text":"美國車市進入衰退（唯一致命點）","type":"Single Thing","maps_to":"H1","metric":"美國輕型車 SAAR 季均","threshold":"連兩季 < 1,450 萬輛","action":"減碼至半倉；若同時 Ford Credit 60 天以上逾期率 > 4% → 清倉","source_freq":"每月（美國車市銷售統計）","date":null,"evidence_refs":["supply_demand_durability#0","cyclical_inventory_price_position#1"]},{"n":2,"text":"重新研究的價格與景氣條件","type":"估值rearm","maps_to":"H3","metric":"股價與美國 SAAR","threshold":"股價 ≤ 10 美元，且 SAAR 季均 ≥ 1,550 萬輛","action":"重做完整研究，通過後才分批建立首筆","source_freq":"股價每日、SAAR 每月","date":null},{"n":3,"text":"Ford Pro 第四季能否守住全年約 70 億美元的指引","type":"假設驗證","maps_to":"H1","metric":"2026 年第四季 Ford Pro EBIT","threshold":"≥ 19 億美元（70 億 − 上半年 34 億 − 第三季 16.65 億）","action":"< 17 億美元 → 停止加碼","source_freq":"每季財報","date":"2027-Q1"},{"n":4,"text":"2027 年全年指引","type":"假設驗證","maps_to":"H1","metric":"2027 年調整後 EBIT 指引","threshold":"≥ 100 億美元","action":"< 100 億美元 → 已持有者減碼三分之一","source_freq":"年度指引","date":"2027-Q1"},{"n":5,"text":"Model e 第四季虧損（沿用前份門檻）","type":"風險","maps_to":"R3","metric":"2026 年第四季 Model e 單季 EBIT","threshold":"虧損 > 13 億美元","action":"停止加碼","source_freq":"每季財報","date":"2027-Q1","evidence_refs":["end_markets#1"]},{"n":6,"text":"Fathom 上市時程","type":"假設驗證","maps_to":"H2","metric":"Fathom 交車時點","threshold":"延後到 2028 年第一季之後","action":"減碼三分之一，並把 Model e 2029 年損平從基準情境移除","source_freq":"法說與產品公告","date":"2027-Q4","evidence_refs":["major_events#0"]},{"n":7,"text":"產業庫存與獎勵金","type":"風險","maps_to":"R1","metric":"美國新車庫存天數與獎勵金占 MSRP","threshold":"庫存 > 90 天，且獎勵金 > 7.5%","action":"停止加碼；已持有者在 14 美元以上分批了結","source_freq":"每月（Cox、J.D. Power）","date":null,"evidence_refs":["cyclical_inventory_price_position#1"]},{"n":8,"text":"成本逆風吸收失敗","type":"減碼","maps_to":"R2","metric":"單季調整後 EBIT 利潤率","threshold":"連兩季 < 4%（2026 年第三季為 5.4%）","action":"減碼三分之一","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#0"]},{"n":9,"text":"股息覆蓋破功","type":"清倉","maps_to":"H3","metric":"定期股息與全年調整後自由現金流","threshold":"削減每季 0.15 美元股息，或全年調整後自由現金流 < 30 億美元","action":"清倉","source_freq":"每季股息公告、年報","date":null},{"n":10,"text":"Ford Credit 信用惡化（沿用前份門檻）","type":"風險","maps_to":"R6","metric":"Ford Credit 60 天以上逾期率","threshold":"> 4%（現值事實表未涵蓋）","action":"與第 1 條同時成立 → 清倉；單獨成立 → 減碼三分之一","source_freq":"每季 Ford Credit 財報","date":null},{"n":11,"text":"中國車廠進入美國","type":"風險","maps_to":"R4","metric":"中國品牌在美國的生產或銷售管道","threshold":"宣布在美國設廠、併購或取得銷售許可","action":"減碼三分之一","source_freq":"新聞與政策公告","date":null,"evidence_refs":["competitive_share_entrants#4"]},{"n":12,"text":"下一次完整複審","type":"複審日期","maps_to":null,"metric":"2026 年第四季財報與 2027 年指引","threshold":"財報公布後兩週內","action":"重跑完整研究","source_freq":"一次","date":"2027-Q1"}],"kill_metrics":[{"metric":"美國輕型車 SAAR 季均","bear_threshold":"連兩季 < 1,450 萬輛 → 減碼至半倉","window":"每季","source":"美國車市月度銷售統計；公司指引假設 1,650 萬","last_status":"ok"},{"metric":"Ford Pro 單季 EBIT 利潤率","bear_threshold":"連兩季 < 8% → 減碼三分之一（2026 年第三季 9.4%，已跌破前份 10% 門檻）","window":"每季","source":"公司季報新聞稿分部表","last_status":"warning"},{"metric":"全年調整後自由現金流與定期股息","bear_threshold":"自由現金流 < 30 億美元，或削減每季 0.15 美元股息 → 清倉","window":"每年","source":"公司年報與股息公告","last_status":"ok"},{"metric":"Ford Credit 60 天以上逾期率","bear_threshold":"> 4% → 減碼三分之一；與 SAAR 門檻同時成立 → 清倉","window":"每季","source":"Ford Credit 季報（現值事實表未涵蓋）","last_status":"unknown"},{"metric":"美國新車獎勵金占 MSRP","bear_threshold":"> 7.5%，且產業庫存 > 90 天 → 停止加碼","window":"每月","source":"J.D. Power、Cox Automotive","last_status":"warning"},{"metric":"Model e 單季 EBIT 虧損","bear_threshold":"> 13 億美元（沿用前份）→ 停止加碼","window":"每季","source":"公司季報新聞稿分部表","last_status":"ok"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#2","reason":"來源頁面日期是 2006-04-11，摘錄內容是 2006 年市占下滑放緩的舊報導，對不上「Cox 預估 2026 年 GM 與 Ford 市占流失最大、前九月約 12.5%」的說法，數字無法從這個來源核實。美國市占下滑改用日期吻合的兩條來源處理：Experian 第二季 11.8%，以及第三季美國銷量年減 7%"},{"ref":"$.thesis.R","reason":"資本市場定價這一項，如果指的是融資利差與信用評等，第六條風險的門檻已寫明資產證券化利差擴大超過 100bp，第三條假設也要求維持投資等級。閘只看到這兩處沒有掛證據編號，沒有讀到門檻內容。反壟斷監管、通路與商業模式轉變這兩條證據，本輪沒有工具可用，修補包也沒附原文。沒讀過內容就掛到某條風險上，等於只是貼標籤，所以這次不補。留到 2027 年第一季完整複審時讀過原文，再決定掛在第五條風險，或另立一條"},{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"閘把賣方目標價 14.88 美元（比現價高約 19%）讀成股價被低估的對照。但估值段引用這個數字，是要說明它已經過時：資料停在 2026-08，還沒反映 10 月給出的 2027 年持平指引，也沒反映 FY2027、FY2028 共識的微幅下修，所以沒拿來當上檔依據。本判斷沒有主張市場看錯。反證紀錄第三條的結論是：現價既沒反映 2029 年 8% 利潤率，也沒反映衰退。因此「沒給出市場錯在哪」維持否，觀望靠的是等待價格條件。閘也確認了輸入與裁決一致"}],"action_conditions":{"rearm_trigger":"股價 ≤ 10 美元，且美國 SAAR 季均仍 ≥ 1,550 萬輛；觸發後重做完整研究，通過才分批建立首筆","exec_line":"未持有：不追，等重新研究的條件。已持有：不加碼；循環位置在晚段，股價 14 美元以上（約 FY2027E 共識 7.3 倍）分批了結三分之一；Single Thing 觸發就減碼至半倉，削減股息就清倉。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤ 10 美元（約 FY2027E 共識 5.2 倍、股息殖利率 6%），且美國 SAAR 季均仍 ≥ 1,550 萬輛","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"6,7a","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=11.61, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6', '7a']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"北美卡車與商用車利潤池守得住：Ford Pro 加上 F-Series 撐起全公司獲利，2027 年調整後 EBIT 不低於 100 億美元","2y":"2027 年調整後 EBIT ≥ 100 億美元（管理層 2026-10-28 稱與 2026 年大致持平，2026 年指引 105–110 億）；Ford Pro 2027 年 EBIT ≥ 65 億美元","5y":null,"10y":null,"threshold":"Ford Pro 單季 EBIT 利潤率 ≥ 8%（2026 年第三季 9.4%）；公司年度調整後 EBIT ≥ 100 億美元","source":"公司季報新聞稿分部表與法說（2026-10-28 CFO 的分部指引、Davis 的車隊訂單與定價）","drift_rule":"以 TTM 調整後 EBIT 對照 105 億美元：連兩季偏離 ≥ 5% 判削弱，連三季偏離 ≥ 10% 判反轉"},{"id":"H2","text":"Model e 虧損照路徑收斂：Fathom（UEV 首款，起價 28,350 美元）2027 年第四季如期上市，2029 年電動車部門損益兩平","2y":null,"5y":"2028 年 Model e 虧損收窄到 25 億美元以內，2029 年接近損益兩平","10y":null,"threshold":"Model e 年度 EBIT：2026 年約 −40 億；2027 年虧損不超過 50 億（CFO 已說 2027 年費用更高）；2028 年虧損 ≤ 25 億","source":"公司分部揭露；2026-10-28 法說 CFO（2029 年損平、2028 年上半年階躍式改善）與 COO（驗證測試完成九成，主要風險在供應鏈）","drift_rule":"以 TTM Model e 虧損對照上述路徑：連四季差距 ≥ 5% 判削弱，連六季差距 ≥ 10% 判反轉"},{"id":"H3","text":"自由現金流在一次衰退中仍覆蓋定期股息，並維持投資等級","2y":"2026–2027 年調整後自由現金流每年 ≥ 50 億美元（2026 年指引 60–70 億），每季每股 0.15 美元股息不變","5y":"下一次衰退年的調整後自由現金流 ≥ 25 億美元，股息不削減","10y":null,"threshold":"全年調整後自由現金流 ≥ 股息總額的 1.5 倍（約 36 億美元；股息約 0.60 美元 × 39.93 億股 ≈ 24 億）","source":"公司季報、年度指引與股息公告","drift_rule":"TTM 調整後自由現金流低於 36 億美元：連兩季差距 ≥ 5% 判削弱，連三季 ≥ 10% 判反轉；股息一旦削減，直接判反轉"}],"R":[{"id":"R1","text":"美國車市轉弱：產業庫存與獎勵金上升，量價同時回落；Ford Blue 第三季營收已因批發下降而年減 3%","h_ref":"H1","clock":"⚡","threshold":"產業庫存 > 90 天且獎勵金占 MSRP > 7.5%，或 Ford 單季批發量年減 > 10%","evidence_refs":["supply_demand_durability#0","cyclical_inventory_price_position#1","end_markets#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R2","text":"成本逆風吃掉改善：大宗商品、記憶體與物流在 2027 年約 20 億美元，再加上關稅、鋁板與稀土的供應中斷；第三季末又遇到短期供應商中斷（2026-10-28 CFO）","h_ref":"H1","clock":"🔥","threshold":"2027 年成本逆風 > 25 億美元，或單季調整後 EBIT 利潤率連兩季 < 4%（2026 年第三季 5.4%）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R3","text":"電動車再次失敗：Fathom 延期或成本不達標，出現第二輪減損；Model e 第三季批發與營收都年減 31%，BlueOval SK 處分已認列 36 億美元","h_ref":"H2","clock":"🔥","threshold":"Fathom 交車延後到 2028 年第一季之後，或 2026 年第四季 Model e 單季虧損 > 13 億美元，或新的電動車減損 > 20 億美元","evidence_refs":["end_markets#1","major_events#0","ma_merger#0"]},{"id":"R4","text":"中國車廠與新進入者：歐洲產能過剩與中國出口先壓到歐洲業務，CEO 稱中國車廠 5–10 年內可能進入美國","h_ref":"H1","clock":"🐢","threshold":"中國品牌取得在美國生產或銷售的實質管道（設廠、併購或取得許可），或 Ford 歐洲業務連兩年虧損擴大","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","substitute_technology#1","substitute_technology#2","supply_demand_durability#2","supply_demand_durability#3"]},{"id":"R5","text":"訴訟與安全監管：Hetsler 案判賠 1.03 億美元，上訴中（判決時點未知）；NHTSA 2024-11 同意令罰款 1.65 億，監督期至少三年、約至 2027-11；2024 年保固準備金的證券集體訴訟現況未查證","h_ref":"H3","clock":"🐢","threshold":"單案判賠或罰款 > 10 億美元，或 NHTSA 同意令延長並加罰，或證券集體訴訟通過集體認證","evidence_refs":["major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","product_recall_warning#0"]},{"id":"R6","text":"Ford Credit 在衰退中放大損失（沿用前份風險）；管理層已預告 2027 年 Credit 會遇到總經逆風","h_ref":"H3","clock":"🐢","threshold":"60 天以上逾期率 > 4%，或資產證券化利差擴大 > 100bp（現值事實表未涵蓋，屬資料缺口）"}],"single_thing":{"description":"美國車市進入衰退：輕型車 SAAR 季均連兩季低於 1,450 萬輛（2026 年指引假設 1,650 萬）","why_fatal":"北美卡車與商用車是獲利主體，量價同時回落時營業槓桿最大；2020 年全年調整後 EBIT 利潤率只有 2.2%、第二季 −10%，管理層指引也明說不含美國經濟顯著下滑。EPS 可能從 1.9 美元跌到 0.7 美元左右，股息覆蓋會受威脅","if_happens":"減碼至半倉；若 Ford Credit 逾期率同時 > 4%，清倉。不在衰退初期攤平，等 SAAR 連兩月回升再重做研究","how_monitor":"每月 SAAR、Cox 庫存天數、J.D. Power 獎勵金占 MSRP、Ford Credit 季度逾期率","probability":"12–24 個月內約 25%：產業庫存升到 82 天、獎勵金年增 0.7pp、全球產量預測下修；但美國定價仍年增 1%，Ford 自身庫存偏低"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":6.57,"peg_fy2":1.43,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":1.91,"FY2027E":1.91,"FY2028E":2.09},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（公司 non-GAAP，與 Koyfin 共識同口徑）；FY2025A 的調整後實際值事實表未涵蓋（只有 GAAP −2.06），因此留空，三年共識成長改以 FY2026E 到 FY2028E 兩年年化計算"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"CFO 在 Barclays 全球汽車與移動科技研討會發言（11 月 18 日）","impact":"低","watch":"2027 年約 20 億美元成本逆風的抵銷進度"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"2026 年第四季財報與 2027 年全年指引","impact":"高","watch":"調整後 EBIT 指引是否 ≥ 100 億、Model e 2027 年虧損指引、Ford Pro 第四季 EBIT 是否 ≥ 19 億"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"Fathom 開放預購；儲能 2028 年產能全數承諾的目標期限","impact":"中","watch":"預購量，以及儲能已簽約量是否首次揭露"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"Fathom（UEV 首款）在 Louisville 上市","impact":"高","watch":"是否如期上市、起價 28,350 美元是否維持"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"肯塔基儲能電池 20 GWh 年產能上線","impact":"中","watch":"是否如期上線，以及 2029–2030 年產能的議約進度"}]}
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
