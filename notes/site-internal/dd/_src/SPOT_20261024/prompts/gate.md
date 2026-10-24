你是 DD 管線 v20 的判斷層閘（gate），標的 SPOT（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_total_revenue_ifrs`（q1_business）｜Total revenue (IFRS)＝4969 €M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi1_operating_income_ifrs_no`（q1_business）｜Operating income (IFRS，公司無 non-GAAP 營業利益)＝672 €M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi2_operating_margin_ifrs`（q1_business）｜Operating margin (IFRS)＝13.5 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi3_gross_margin`（q1_business）｜Gross margin＝33.0 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi4_free_cash_flow`（q1_business）｜Free cash flow＝735 €M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi6_mau`（q1_business）｜MAU＝788 M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi7_premium_subscribers`（q1_business）｜Premium subscribers＝306 M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi8_premium_arpu`（q1_business）｜Premium ARPU＝4.95 €｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_kpi9_guidance_q4_2026`（q1_business）｜Guidance Q4 2026＝MAU 818M；Premium subs 316M；營收 €5.2B（含約 230bps 匯率順風）；毛利率 33.8%；營業利益 €820M（含約 €6M Social Charges，以 Q3 收盤價 $487.38 計） 點估計（公司僅給單點，無區間；無全年指引）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_peer_spot_gross_margin_pct`（q2_moat）｜SPOT 毛利率＝32.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPOT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_spot_operating_margin_pct`（q2_moat）｜SPOT 營業利益率＝14.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPOT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_peer_spot_fcf_margin_pct`（q2_moat）｜SPOT FCF 利潤率＝18.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPOT.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tme_gross_margin_pct`（q2_moat）｜TME 毛利率＝44.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TME.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tme_operating_margin_pct`（q2_moat）｜TME 營業利益率＝29.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TME.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tme_fcf_margin_pct`（q2_moat）｜TME FCF 利潤率＝28.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TME.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nflx_gross_margin_pct`（q2_moat）｜NFLX 毛利率＝49.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nflx_operating_margin_pct`（q2_moat）｜NFLX 營業利益率＝29.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nflx_fcf_margin_pct`（q2_moat）｜NFLX FCF 利潤率＝23.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wmg_gross_margin_pct`（q2_moat）｜WMG 毛利率＝45.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WMG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wmg_operating_margin_pct`（q2_moat）｜WMG 營業利益率＝16.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WMG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wmg_fcf_margin_pct`（q2_moat）｜WMG FCF 利潤率＝3.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WMG.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.45 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝17.24 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝21.98 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_kpi5_share_based_compensation`（q1_business）｜Share-based compensation expense＝87 €M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝584.22 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝43.44 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 13.45，分子＝快照價 584.22｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝2.05 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（13.18 → 13.45）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.41 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（17.17 → 17.24）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.05 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（21.99 → 21.98）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-7.05 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 14.47 → 13.45（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝12.78 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_rsi14`（q5_valuation）｜RSI(14)＝70.61｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 584.22 / W52 517.7 / W104 561.97 / W250 338.95 / W250 13週斜率 1.42%」

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因素：Apple、Alphabet、Amazon 的裝置預載或預設其自家音訊串流服務，Spotify 自述處於重大競爭劣勢；並提及 AI 帶來新進入者與新消費方式
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-02-10）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F：新興技術（含 AI）使競爭者推出新的內容消費方式，可能使年輕用戶轉向其他產品，影響留存
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-02-10）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Digital Music News：美國 YouTube Music 訂閱用戶一年增 45%
  - 來源：Digital Music News Pro（as_of 2026-08-04）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：土耳其競爭委員會對 Spotify 展開調查（2025 年啟動，涉及對權利人的演算法歧視與掠奪性訂閱定價），官方稱不代表已認定違規；Spotify 否認指控。2026-04-21 GCR 另有一則相關條目，日期未核實。
  - 來源：Digital Policy Alert / Turkish Competition Authority（搜尋摘要）（as_of 2025-08-28）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：GCR 列出 Spotify 土耳其反壟斷調查（2026-04-21 條目）
  - 來源：Global Competition Review（as_of 2026-04-21）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：美國貿易代表署 2025-12-16 威脅對含 Spotify 在內的九家歐洲公司採取報復措施（費用或限制），與歐盟數位規則相關；僅為威脅，未見已實施。
  - 來源：WebSearch 摘要（引述 USTR 聲明）（as_of 2025-12-16）｜affects：decision_inputs.bear、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Spotify 在 FY2025 20-F 風險因素揭露：新興技術（含 AI）帶來新的內容消費方式，可能使用戶（尤其年輕族群）轉向其他產品；Apple、Alphabet、Amazon 可能藉由在裝置或作業系統整合 AI 取得競爭優勢。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-02-10）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026 營業利益 guidance €630M 低於分析師共識 €684M（約 8%）；管理層稱高 OpEx 持續至 Q3 後於 Q4 趨緩
  - 來源：TIKR blog（as_of 2026-06-22）｜affects：valuation、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 20-F：MLC 於 2024 年 5 月對 Spotify USA 提起訴訟（授權費／強制授權相關），列為風險因素；法律程序另見財報附註 21、24
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-02-10）｜affects：decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Pomerantz 律所於 2026 年 5 月宣布調查 Spotify 是否有證券詐欺，起因為 Q1 財報後股價於 2026-04-28 下跌 12.43%；僅為律所調查通知，搜尋未見已提起的集體訴訟
  - 來源：Barchart／Pomerantz 投資人警示（as_of 2026-05-15）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Pomerantz 律所 2026-05 宣布調查證券詐欺（股價 2026-04-28 跌 12.43%），尚非法院案件
  - 來源：Barchart／Pomerantz 投資人警示（as_of 2026-05-15）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1303.5,"bear_5y_price":344.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":50.2,"ev5y_pct":41.0,"irr_base_pct":8.5,"asym_ratio":2.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.45,"pe":43.44,"basis":"FY2026 共識 EPS（10 月時點的當年度 EPS）；終端同以 FY2031 當年度 EPS 為分母"},"eps":{"bull":[18.0,23.5,28.5,34.0,39.5],"base":[17.24,21.98,25.5,29.0,32.5],"bear":[15.0,15.8,16.3,16.8,17.2]},"pe":{"bull":33,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.7},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SPOT_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 MAU 預測 7.88 億（原話："we are forecasting MAU of 788 million"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 訂閱數預測 3.05 億（淨增 500 萬）（原話："we are forecasting 305 million for quarter 3"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 營收預測約 50 億歐元、成長 14%（原話："total revenue of approximately EUR 5 billion in quarter 3"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 毛利率預測 32.9%（原話："We anticipate a quarter 3 gross margin of 32.9%"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 營業利益預測 6.7 億歐元（原話："We're guiding to EUR 670 million in quarter 3."）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 重申全年行銷與 AI 投入帶來約 2 億歐元增量營業費用（原話："approximately EUR 200 million in incremental"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 指 Q4 營業費用年增率將趨緩（原話："Quarter 4 is well positioned to see a moderation"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 重申廣告業務下半年轉為雙位數成長（原話："We continue to expect our ads business to inflect"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 表示不給全年毛利率與營業利益率數字，但預期全年皆改善（原話："improve in 2026 on a full year basis"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 預期 2026 年自由現金流有意義成長（原話："meaningful year-over-year growth in free cash flow in 2026"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 重申 2030 年目標：毛利率 35% 至 40%、營業利益率高於 20%（原話："of 35% to 40%, operating margin above 20%"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告 Q2 毛利率 33.4%，高於財測（原話："Gross margin came in at 33.4%, surpassing"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明毛利率優於財測含加拿大數位服務稅一次性迴轉（原話："small onetime benefit from cancellation of the Digital"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告 Q2 營業利益 6.55 億歐元（原話："Operating income of EUR 655 million"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 拆解營業利益優於財測中社會費用的貢獻（原話："Social charges contributed to EUR 9 million"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明 Q3 營業費用成長（扣除匯率與社會費用）與 Q2 大致相同（原話："roughly consistent with quarter 2"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明廣告自動化銷售轉為規模型業務，廣告利潤率目標由 20% 區間往 40%（原話："move from the 20% range we have today towards 40%"）
- 2026-08-04｜Co-CEO Gustav Söderström｜margin：共同 CEO 稱利潤率是管理出來的結果（原話："Our margin is a managed outcome"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告廣告營收年增 3%，與 Q1 相同（原話："Our Ad-supported revenue grew 3% year-over-year"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告自動化通路占廣告營收近 4 成（原話："represented nearly 40% of our ad-supported revenue in"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明直營通路價格優化工作已完成（原話："our price optimization work is now complete"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 拆解 Premium 營收成長中的 ARPU 貢獻（原話："ARPU expansion of 7.4% year-over-year"）
- 2026-08-04｜CFO Christian Luiga｜customer：CFO 報告 Q2 MAU 淨增低於預測 100 萬（原話："Our net additions of 16 million were 1 million below"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：共同 CEO 稱超過 1 億訂閱者每月活躍超過 20 天（原話："over 100 million of our subscribers spending more than 20"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：廣告主數量成長（原話："We are now at 33,000 active"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：Reserved 售票數（原話："nearly 100,000 tickets reserved through Spotify"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 報告年初至今庫藏股買回金額（原話："we have repurchased $662 million in shares year-to-date"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 表示即使有併購仍預期回饋股東現金（原話："even with M&A, we expect that we will also return cash"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 報告現金部位（原話："EUR 9.4 billion in cash and cash equivalents"）
- 2026-08-04｜CFO Christian Luiga｜commitment：CFO 表示 2026 年員工人數持平（原話："In 2026, we continue to be flat on the number of employees."）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 稱 Q4 成本趨緩（原話："we are sticking to our cost moderating in Q4"）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 稱過去三年人數未增加（原話："we have not increased head count"）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 表示 AI 成本面也要贏（原話："beneficiary means winning on the cost side, too"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 承認新興市場調整將反映在 Q3 MAU（原話："Yes, this will show itself in our Q3 MAU"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 稱新興市場在免費版增加摩擦以推動轉換（原話："carefully increases friction in our free service"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 稱開始拉動變現槓桿（原話："Now here, we're starting to pull the monetization lever"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 稱新興市場調整不影響近期訂閱成長（原話："this will not affect subs"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 稱新興市場調整不以訂閱成長為代價（原話："expect it to come at the expense of our subscriber growth"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Prompted Playlists 使用規模（原話："Around 14 million of the"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Audiobooks+ 年化經常性收入（原話："has passed $100 million in annual recurring revenue"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Audiobooks+ 規模自上次揭露翻倍（原話："that has now doubled, which is great"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Reserved 的變現方式目前是提高 Premium 性價比（原話："currently about increasing the value to price ratio"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Taste Model 驅動的 Autoplay 讓活躍天數上升（原話："active days have increased which is very hard to do"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Chirp 將對外提供給其他公司（原話："that we will also offer to"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Large Taste Model 以開源模型為基礎（原話："the Large Taste model is based on open source."）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Merlin 授權協議納入翻唱與混音（原話："30,000 labels in Merlin's network"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：混音產品需要時間才能成為重大營收來源（原話："it will take time to scale into a material revenue"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：混音產品將先以研究預覽推出（原話："you should expect to see a research preview"）
- 2026-08-04｜Co-CEO Gustav Söderström｜competition：共同 CEO 稱不需與所有大廠達成協議才推出 AI 音樂服務（原話："we do not need a deal with all the majors"）
- 2026-08-04｜Co-CEO Gustav Söderström｜competition：共同 CEO 談 AI 生成音樂與自家混音產品的差異（原話："Normal generative music will happen with or without us."）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 稱不評論 Apple Music 漲價（原話："We don't comment on other companies' price increases."）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 稱目前樂於當品類價格領導者（原話："we're happy to be the price leader in our category"）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 談長期滲透率（原話："it's not impossible that we'll get to 15% penetration"）
- 2026-08-04｜Co-CEO Alex Norström｜guidance：共同 CEO 稱不評論上線時程（原話："We don't comment on timing for launches"）

### SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md
- 2026-05-21｜Alex Norström｜guidance：2030 目標：營收中段兩位數 CAGR、毛利率 35–40%、營業利益率 20% 以上（原話："a mid-teens revenue CAGR, a gross margin of 35% to 40%"）
- 2026-05-21｜Alex Norström｜commitment：重申長期北極星目標（10 億訂閱、1000 億美元營收、毛利率 40% 以上）（原話："we also remain committed to our North Stars, 1 billion"）
- 2026-05-21｜Katie English｜guidance：廣告業務預期 2026 下半年成長加速，之後維持兩位數成長（原話："we expect higher growth in the second half of 2026."）
- 2026-05-21｜Christian Luiga｜guidance：CFO：廣告回到兩位數成長，2026 下半年開始爬升（原話："reaccelerate growth into the double-digit range."）
- 2026-05-21｜Christian Luiga｜margin：CFO：高端以音樂在行銷平台與加購支撐下仍有毛利空間（原話："music has further room to run, supported by marketplace"）
- 2026-05-21｜Christian Luiga｜guidance：2026 Q2、Q3 費用成長墊高，Q4 與 2027 趨緩（原話："quarter 3 before moderating into quarter 4 and 2027."）
- 2026-05-21｜Christian Luiga｜guidance：費用暫時增加約 2 億歐元，用於行銷與研發（原話："EUR 200 million on marketing and R&D."）
- 2026-05-21｜Christian Luiga｜margin：Podcast 毛利率 2026 預期超過 20%，長期路徑 40%（原話："to what we believe will be more than 20% in 2026."）
- 2026-05-21｜Roman Wasenmüller｜margin：Podcast 長期毛利率路徑 40%（原話："we see a path to 40% margins in the long term."）
- 2026-05-21｜Christian Luiga｜guidance：2030 營業利益率至少 20%（原話："All of this points to an operating margin of at least 20%,"）
- 2026-05-21｜Christian Luiga｜margin：廣告業務在重建廣告技術期間仍有 10% CAGR（原話："Our advertising business grew at a 10% CAGR"）
- 2026-05-21｜Christian Luiga｜margin：營運費用 2022 年以來大致持平，因通膨上升被人力縮減抵銷（原話："Operating expense growth has remained essentially flat"）
- 2026-05-21｜Christian Luiga｜margin：全職人力減少 23%（原話："reduction in full-time headcount."）
- 2026-05-21｜Christian Luiga｜guidance：正常化帳面稅率約 22%，2027 年成為完整納稅人（原話："foresee that we will become a full taxpayer by 2027"）
- 2026-05-21｜Christian Luiga｜commitment：每股自由現金流納入未來記分板（原話："will be part of our scorecard going forward."）
- 2026-05-21｜Christian Luiga｜capital_allocation：現金與短期投資 88 億歐元（原話："balance of EUR 8.8 billion today."）
- 2026-05-21｜Christian Luiga｜capital_allocation：CFO：資本不是限制（原話："Simply put, capital is not a constraint."）
- 2026-05-21｜Christian Luiga｜capital_allocation：資本配置偏好自建優先（原話："Our bias remains towards build"）
- 2026-05-21｜Christian Luiga｜capital_allocation：除了抵銷稀釋的回購外，另將返還超額現金（原話："This will be over and above the anti-dilution baseline."）
- 2026-05-21｜Christian Luiga｜capital_allocation：AI 研發支出分為兩塊（大型品味模型前期集中、開發者 AI 工具持續性）（原話："Our AI R&D spend has 2 pieces."）
- 2026-05-21｜Owen Smith｜guidance：Audiobooks+ 預計今年 7 月達年化經常性營收 1 億美元（原話："recurring revenue from Audiobooks Plus only this July."）
- 2026-05-21｜Owen Smith｜commitment：今夏擴充 Audiobooks+ 加購層級（原話："we're expanding Audiobooks+ with new add-on tiers"）
- 2026-05-21｜Roman Wasenmüller｜commitment：今夏推出 podcast 創作者會員制（原話："we're taking the next step by introducing memberships."）
- 2026-05-21｜Maya Prohovnik｜product：所有 Premium 用戶每月有生成個人 podcast 的額度，重度用戶可加購（原話："a monthly allocation of credits to generate podcast"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：巴西 2026 營收成長預期超過 30%（原話："revenue is going to grow with more than"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：印度新高階方案 Premium Platinum 定價約標準版 2 倍（原話："Premium Platinum, priced at just over 2x the cost of our"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：印度訂閱戶已有逾 7% 選高階層（原話："more than 7% of our subscribers are already on this higher"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：美國 Premium 市佔六年增加 8–10 個百分點（原話："grown our U.S. premium market share by 8 to 10"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：全球付費轉換率多年維持約 40%（原話："has actually stayed around 40% for many years"）
- 2026-05-21｜Christian Luiga｜customer：美國客戶終身價值 2022 年以來增加逾 70%（原話："LTV has increased by more than 70% since 2022."）
- 2026-05-21｜Gustav Gyllenhammar｜customer：管理層稱免費用戶成長加速，朝 2030 前 10 億用戶（原話："we are on the right path to reach 1 billion users before"）
- 2026-05-21｜Gustav Söderström｜margin：UMG 授權的加購：預期毛利至少持平到增加（原話："this to be at least margin neutral to accretive for us."）
- 2026-05-21｜Charlie Hellman｜product：與 UMG 簽署授權，讓粉絲合法製作翻唱與混音，作為付費加購（原話："landmark licensing agreements with Universal Music Group"）
- 2026-05-21｜Charlie Hellman｜risk：AI 生成內容湧入，權利人失控風險（管理層稱像狂野西部）（原話："things are starting to feel like the Wild West."）
- 2026-05-21｜Rene（未標示姓氏）｜product：Reserved：Live Nation 為首發夥伴，多年合約（原話："Reserved arrives with Live Nation as our launch"）
- 2026-05-21｜Gustav Söderström｜product：管理層稱 AI 是順風而非逆風（原話："Guess what? It's a tailwind."）
- 2026-05-21｜Gustav Söderström｜competition：Spotify 選擇向公開市場購買通用 LLM，自訓大型品味模型（原話："buying this capability on the open market"）
- 2026-05-21｜Gustav Söderström｜competition：面對 LLM 平台：視為更多通路（ubiquity）（原話："So for us, this is just more ubiquity."）
- 2026-05-21｜Gustav Söderström｜competition：管理層對自身差異化優勢感到安心（個人化資料）（原話："we feel quite comfortable about the unique advantages"）
- 2026-05-21｜Gustav Söderström｜product：AI 不只是成本層，也是產品與變現層（原話："It's a product and monetization layer."）
- 2026-05-21｜Niklas Gustavsson｜product：程式碼貢獻逾 73% 由 AI 輔助（原話："73% of our code contributions are AI-assisted"）
- 2026-05-21｜Gustav Gyllenhammar｜guidance：定價仍是工具箱中的工具，預期持續調價（原話："pricing will continue to be a tool in our toolbox."）
- 2026-05-21｜Alex Norström｜customer：調價後流失率極低，管理層自己也意外（原話："Even us, we were surprised that the churn was so minimal."）
- 2026-05-21｜Katie English｜competition：廣告主動廣告商 Q1 年增 68%（原話："active advertisers grew 68% year-over-year in Q1"）
- 2026-05-21｜Katie English｜product：競價式廣告渠道已占廣告業務逾三分之一（原話："biddable channels have grown to more than 1/3 of our Ads"）
- 2026-05-21｜Katie English｜risk：承認廣告轉型太慢（原話："took us too long to make the shift."）
- 2026-05-21｜Katie English｜risk：過去廣告過度集中於音訊預算（原話："too centered on audio-only budgets"）
- 2026-05-21｜Katie English｜commitment：廣告平台重建工作已結束（原話："The heavy platform rebuild is now behind us."）

### 問答異常語氣（迴避／改口／保留）
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Doug Anmuth 追問新產品加價方案上線時程與對 Premium ARPU 下半年與 2027 年的影響｜答法：共同 CEO 說不評論時程、不給 ARPU 指引，改談 Audiobooks+ 翻倍與加價結構
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Jason Bazinet 追問唱片公司稱產業 Q2 付費成長放緩，對長期訂閱成長有多大信心｜答法：共同 CEO 答非常有信心，但表示不給長期指引，未回應產業放緩的數據
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Jason Helfstein 追問 Apple Music 漲價的啟示與 Spotify 未來漲價想法｜答法：共同 CEO 稱不評論其他公司漲價，未說明自家漲價計畫
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：Wells Fargo Steve Cahall 問 UMG 加購的定價、對毛利率的影響、是否全球推出、其他大廠跟進｜答法：Alex 明說不談具體細節；Gustav 只給「至少毛利持平到增加」，未回答定價與推出範圍
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：Guggenheim Michael Morris 問去年免費層改版後轉換到 Premium 的進展｜答法：Alex 以 MAU 超預期與互動天數回答，未給轉換率數字；Gustav 談互動與付費相關性
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：BofA Jessica Reif Cohen 問各加購層定價、是否有多層超級 Premium，以及日均使用時數｜答法：未給任何定價，講價值對價格比與「多個加購、依意願定價」；日均使用時數完全未回答

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 4 | 2 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"成熟市場（NA/歐洲）Premium 飽和為「成熟非結構崩壞」，新興市場量 + ARPU 二曲線接棒總訂戶淨增","columns":{"2Y 驗證點":"Q2 26 NA Premium 回穩、Q2 總訂戶 299M guide 兌現","5Y 驗證點":"總 Premium 訂戶維持 +8-10%/yr CAGR，新興市場佔淨增 &gt;60%","10Y 驗證點":"Premium 訂戶向 5-6 億邁進（全球逼近 10 億付費）","數字門檻":"總 Premium ≥ +8%/yr；NA 訂戶不連 2 季負","來源":"Q1 26 newsroom；MBW；Music Ally","漂移觸發":"NA（或歐洲）Premium 連 2 季 YoY 負 → 削弱"}},{"id":"H2","text":"毛利率守 33% 且 OM 全年擴張，ARPU 二曲線（podcast/audiobook/super-premium/AI，較音樂高毛利）改善 mix","columns":{"2Y 驗證點":"FY26 GM &gt;33%、OM YoY 擴張（Q2 guide OM 33.1%*）","5Y 驗證點":"GM 向 35% 靠、OM 向高十幾%（規模槓桿）","10Y 驗證點":"OM 進入 20%+ 區間（成熟平台）","數字門檻":"季 GM ≥ 32.8%；FY26 OM YoY 正","來源":"Q1 26 shareholder letter；investing.com","漂移觸發":"連 2 季 GM &lt; 32.8% 或 labels royalty 再 +1pp → 削弱"}},{"id":"H3","text":"估值從 26x Fwd PE（5Y ~30 分位）向合理 26-30x 修復/守穩，報酬由 EPS 複利驅動（非 re-rate 依賴）","columns":{"2Y 驗證點":"FY27 EPS 共識 ≥ $18 守穩、Fwd PE 不破 20x","5Y 驗證點":"EPS 由 FY26 $14.7 → FY28 $22.4（~23% CAGR）兌現","10Y 驗證點":"成熟期 PE 收斂 22-26x、EPS 持續複利","數字門檻":"Fwd PE ≥ 20x；FY27 EPS 共識不連 2 季下修","來源":"Excel snapshot 2026-06-23；stockanalysis","漂移觸發":"FY1/FY2 EPS 共識連 2 季下修 &gt;5% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成熟市場（NA→歐洲）Premium 結構性飽和蔓延（vs Apple/YouTube Music + subscription fatigue）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"NA/歐洲 Premium 訂戶 YoY","警戒閾值":"NA 連 2 季 YoY 負 → H1 失敗"}},{"id":"R2","text":"labels（UMG/Sony/Warner）供給端議價權持續回收，mechanical royalty 再上調封頂毛利","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM、labels 合約重議公告","警戒閾值":"連 2 季 GM &lt; 32.8% 或任一 label royalty +1pp"}},{"id":"R3","text":"EU DMA / Apple App Store 佣金與導流規則（雙向，偏正面）","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"DMA 執行進展、Apple 佣金/CTF 調整","警戒閾值":"7/8 EU 法院已裁 Apple 敗訴、確認 gatekeeper → 對 SPOT 通路成本正面緩衝；若反轉則 −ve"}},{"id":"R4","text":"AI 生成音樂（Suno/Udio）破壞內容經濟與訂閱必要性（critic 補入；賣方砍價明示理由）","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期結構（2+ 年，但近月有判決催化）","監測指標":"Sony v. Suno 判決、AI 音樂佔串流量、Viral 榜 AI 曲目","警戒閾值":"7 月判 AI 訓練屬合理使用 或 AI 音樂 &gt;10% 串流量 → 結構 reframe"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","irr_base_pct":11.5,"ev5y_pct":62.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.8,"ev5y_pct":62.0,"irr_base_pct":11.5,"max_dd_pct":-58.0,"bull_5y_price":1224.0,"bear_5y_price":360.0,"p_bull_pct":25.0,"p_bear_pct":32.0,"rearm_trigger":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","price_at_dd":479.77,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SPOT","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Spotify Technology S.A."},"oneliner":"逐季兌現、毛利率擴張、帳上近百億歐元現金無負債，生意品質好；但股價 584 美元已貼近分析師均值，FY2027 本益比約 34 倍，FY2026 共識三個月內下修 7%，報酬得靠 2030 年利潤率目標全數達成，等回到約 480 美元再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球個人與家庭的月訂閱費（約九成），廣告約一成；錢卡在上游唱片公司的授權分成，毛利率 33% 就是 Spotify 從每一歐元裡實際留下的部分。","reasoning":"Q3 2026 營收 49.69 億歐元，固定匯率年增 14%；毛利率 33.0%、營業利益 6.72 億歐元、營業利益率 13.5%、單季自由現金流 7.35 億歐元。Premium 營收年增 15%，拆成訂戶 +9% 與 ARPU +7.5%；廣告年增 9%，CFO 說廣告只占營收約 10%。季末 MAU 7.88 億、付費訂戶 3.06 億，比指引多 100 萬。Q4 指引：訂戶 3.16 億、營收 52 億歐元、毛利率 33.8%、營業利益 8.2 億歐元。產業處在擴張期：Q3 各區域訂戶都季增，全球人口付費滲透率不到 4%，Futuresource 預估產業訂閱 2027 年底超過 10 億。供需屬結構性持久：美國 2026 年 2 月漲價，Q1 北美淨增偏軟，但 Q2、Q3 恢復，公司說 150 多個市場漲價後留存穩定。單點依賴在供給端：三大唱片公司集中，UMG 與 WMG 合約在 2027 年 Q1 到兩年期節點。對消費者有定價領導權（2026 年 8 月法說：樂於當品類價格領導者），對供應商沒有。毛利率從 2022 年 24.95% 升到 2025 年 31.98%，表示播客、有聲書與行銷平台正把利潤池往 Spotify 這一節移。分部金額、客戶與供應商占比事實表未涵蓋。","fact_refs":["f_kpi0_total_revenue_ifrs","f_kpi1_operating_income_ifrs_no","f_kpi2_operating_margin_ifrs","f_kpi3_gross_margin","f_kpi4_free_cash_flow","f_kpi6_mau","f_kpi7_premium_subscribers","f_kpi8_premium_arpu","f_kpi9_guidance_q4_2026","f_peer_spot_gross_margin_pct","f_peer_spot_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"約九成是月訂閱經常性收入；管理層說 2018 年上市以來每年淨增訂戶都在 2,500 萬以上，2026 年預計 3.16 億。","unit_econ_note":"Q3 Premium ARPU 4.95 歐元，年增 7.5%；投資人日說全球免費轉付費比例多年維持約 40%，美國客戶終身價值 2022 年以來增加逾 70%；Q3 SBC 8,700 萬歐元，約占營收 1.75%。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"訂閱收入約九成、資本支出低、營運資本為負，利潤率由虧轉盈後仍在擴張，最大成本是上游授權分成"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：漲價後留存穩定（公司說法、RSM 報導），Q3 各區域訂戶季增，全球付費滲透率不到 4%（Q3 法說）","bargaining":{"up":"弱：三大唱片公司集中，UMG 與 WMG 合約 2027 年 Q1 到兩年期節點；WMG 毛利率 45.8%，高於 Spotify 的 32.8%","down":"強：美國個人方案 2026 年 2 月由 11.99 漲到 12.99 美元，Q3 ARPU 仍年增 7.5%","geo":"成長來自拉美與新興市場；土耳其競爭局調查中，USTR 2025-12 威脅對含 Spotify 在內的歐洲公司報復"},"profit_pool_dir":"往 Spotify 移：毛利率 2022 年 24.95% → 2025 年 31.98% → Q3 2026 33.0%，全年指引擴張約 130bp","tam_table":[{"item":"全球人口付費滲透率","value":"不到 4%（Q3 2026 法說）"},{"item":"瑞典","value":"近 50%"},{"item":"英國、德國","value":"20%–25%"},{"item":"拉丁美洲","value":"約 11%"},{"item":"新興市場","value":"不到 3%"},{"item":"全球音樂串流訂閱（產業）","value":"2027 年底超過 10 億、2029 年約 12 億（Futuresource 預測）；拉美、亞太至 2029 年 CAGR 14%、10%"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"→","reasoning":"機制：使用頻率加個人化資料加裝置普及。逾 1 億用戶每月用 28 天（Q3 法說），漲價後流失低到管理層自己都意外（投資人日），美國 Premium 市占六年增加 8–10 個百分點。執行面給 8 分：Q3 毛利率年增約 140bp，廣告由 3% 回升到 9%，人數持平下產品出貨加速。定價權給 8 分：對消費者是價格領導者，但上游授權拿走大部分營收。同業比較是負的：營業利益率 14.65%，TME 29.73%、NFLX 29.68%，差距約 15 個百分點，所以兩項平均不能落到 8 分以上；生態系對手扣 1 分後約 7 分，等級 B。方向持平的理由：執行面在擴大，但 YouTube Music 美國訂戶一年增 45%，Apple、Alphabet、Amazon 在裝置上預載自家服務，2027 年 Q1 又要和兩家唱片公司續約，兩邊抵銷。同業 ROIC 與投入資本口徑事實表未涵蓋，以利潤率代替。","fact_refs":["f_peer_spot_gross_margin_pct","f_peer_spot_operating_margin_pct","f_peer_spot_fcf_margin_pct","f_peer_tme_gross_margin_pct","f_peer_tme_operating_margin_pct","f_peer_tme_fcf_margin_pct","f_peer_nflx_gross_margin_pct","f_peer_nflx_operating_margin_pct","f_peer_nflx_fcf_margin_pct","f_peer_wmg_gross_margin_pct","f_peer_wmg_operating_margin_pct","f_peer_wmg_fcf_margin_pct","f_kpi3_gross_margin"],"verdict_values":{"moat":{"mechanism":"高頻使用累積的個人化品味資料，加上嵌進車用、音箱、AI 代理等第三方介面的普及度，讓用戶很少主動退訂；漲價後留存穩定是可觀察的證據","execution":8,"pricing":8,"combined":null,"score":null,"grade":"B","trend":"→","trend_evidence":"擴大面：Q3 毛利率年增約 140bp、廣告成長 3%→9%、美國市占六年 +8–10pp（投資人日）、Midia 稱 2025 年各平台中淨增最多。縮減面：YouTube Music 美國訂戶一年 +45%、大廠裝置預載、UMG／WMG 2027 年 Q1 續約。兩邊抵銷，判持平。","competitor_notes":[{"name":"TME","strategy_note":"中國市場結構不同，營業利益率 29.73%，不能直接當 Spotify 的利潤率天花板"},{"name":"NFLX","strategy_note":"自製內容攤提可以靠規模稀釋，毛利率 49.12%；Spotify 音樂成本按營收比例分成，規模槓桿較小"},{"name":"WMG","strategy_note":"是供應商，毛利率 45.77% 但 FCF 利潤率只有 3.94%；續約時是議價對手"},{"name":"UMG.AS","strategy_note":"最大供應商，事實表只有一季且缺營收，無法比較；2027 年 Q1 續約是近期最大變數"},{"name":"YouTube Music","strategy_note":"綁在 YouTube 生態裡，美國訂戶一年增 45%，在中東北非已居第一，是增量訂戶的主要對手"},{"name":"Apple Music／Amazon Music","strategy_note":"靠裝置預載與預設，Spotify 在 20-F 自述居重大競爭劣勢"}],"spread_notes":{"note":"營業利益率比 TME、NFLX 低約 15 個百分點，FCF 利潤率 18.04% 也低於兩者；ROIC 同業差距事實表未涵蓋，以利潤率代理，差距為負"},"peer_na_reason":null,"threats":[{"level":"🔴","text":"生態系攻擊：Apple、Alphabet、Amazon 在裝置預載或預設自家音訊服務，YouTube Music 美國訂戶一年增 45%，搶的是成熟市場的增量訂戶","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"level":"🟡","text":"AI 帶來新的內容消費方式，年輕族群可能轉向其他產品；公司策略是把自己做成可被其他代理呼叫的服務，目前代理內收聽仍在 Spotify 內發生（Q3 法說）","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（營業利益率中段、投入資本極輕）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"個人方案的使用者就是付款者，家庭方案由一人付款；逾 1 億用戶每月用 28 天，CEO 說問卷裡幾乎沒有人是忘了退訂；聽音樂屬於想要，但日常頻率高，延後購買代價就是每天少了習慣的服務"},{"item":"決策層級","level":"🟡","text":"替代決策發生在個人或家庭層級；漲價後流失極低是最好的代理變數。但大廠把音樂綁進手機與會員組合，換服務的摩擦主要是播放清單與聽歌紀錄，搬遷成本中等"},{"item":"價值鏈分配","level":"🟡","text":"上游三大唱片公司集中，Spotify 毛利率 33% 代表授權分成仍拿走大部分；毛利率 2022–2026 年擴張約 8 個百分點，靠播客、有聲書與行銷平台。2027 年 Q1 兩家續約是檢驗點"},{"item":"社會容忍度","level":"🟡","text":"土耳其競爭局以演算法歧視與掠奪性定價為由調查；USTR 威脅對歐洲數位公司報復；MLC 授權費訴訟未結。目前沒有處分金額，但漲價與分成都受監管與輿論檢視"}],"roiic":"事實表未涵蓋（投入資本口徑缺）","reinvest_rate":"事實表未涵蓋；營運資本為負、資本支出低，帳面再投資率趨近零或為負，再投資主要以研發與行銷費用化","endo_ceiling":14,"formula_note":"增量 ROIC 乘再投資率的公式在這家公司不適用：成長靠費用化的產品與行銷投入，而不是資本支出。改用不靠利潤率擴張的成長上界代理：Q3 2026 固定匯率營收成長 14%，與 2030 年中段兩位數營收 CAGR 目標一致。超出 14% 的 EPS 成長都要靠利潤率擴張。"}}}},"q3_growth":{"verdict":"🟢","reasoning":"成長靠量加價：Q3 訂戶 +9%、ARPU +7.5%；回購只中和稀釋，近年收購都小。共識 EPS：FY2026 13.45、FY2027 17.24、FY2028 21.98，FY2026→FY2028 年化約 27.8%（家數事實表未涵蓋）。FY2025 實際稀釋 EPS 10.51 來自年報，公司以歐元報表，共識標美元，三年 CAGR 可能有幣別落差，所以用同源的兩年 27.8% 判斷。不靠利潤率的成長上界約 14%，缺口約 14 個百分點，歸因利潤率擴張：2026 年毛利率擴張約 130bp，2030 年目標毛利率 35%–40%、營業利益率 20% 以上，這部分可歸因，不是倍數擴張。跑道：全球付費滲透不到 4%，英德 20%–25%，瑞典近 50%，就算以每年 9% 訂戶成長，十年內也到不了 30%；有聲書擴到 180 多個市場、加購方案與廣告回升是第二條曲線。衰退信號只亮一個：EPS 成長明顯高於營收成長，原因是利潤率擴張。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_premium_subscribers","f_kpi8_premium_arpu","f_kpi5_share_based_compensation","f_kpi4_free_cash_flow"],"verdict_values":{"growth":{"driver_mix":"量（訂戶 +9%）加價（ARPU +7.5%）為主；回購只中和稀釋；收購規模小且條件未揭露","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"Q3 2026 固定匯率營收成長 14% 與 2030 年中段兩位數營收 CAGR 目標；共識 EPS 年化 27.8% 超出部分歸因利潤率擴張","segments":{"expanded":false,"reason":"Premium 約九成、廣告約一成；Q3 廣告分部金額與播客、有聲書各自毛利率事實表未取得，無法拆分，利潤率變化只能看合併毛利率"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q3 年增約 140bp，Q4 指引再增約 70bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"YouTube Music 美國訂戶 +45%，但沒有 Spotify 市占下降的直接數據；投資人日稱美國市占六年 +8–10pp"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q1 2026 美國漲價後北美淨增偏軟，Q2、Q3 恢復，訂戶仍年增"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"共識 EPS 年化約 27.8%，營收約中段兩位數，差額來自利潤率擴張"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"過去 12 個月 FCF 約 32 億歐元，高於 FY2025 淨利 22.1 億歐元"},{"signal":"SBC／營收超過 5% 且上升","lit":false,"note":"Q3 約 1.75%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"產業訂閱預估 2029 年 12 億；AI 替代是風險因素，尚未見量化萎縮"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出低"},{"signal":"停止投資且收入 3 年內下滑","lit":false,"note":"仍在投資，營收成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"B：回購已中和稀釋並開始退還多餘現金，但買在高本益比；收購小且無法驗證報酬。","reasoning":"過去 12 個月 FCF 約 32 億歐元（Q3 法說），對 FY2025 淨利 22.1 億歐元，轉換率約 1.4（期間不完全對齊）。Q3 SBC 8,700 萬歐元，約占營收 1.75%。季末現金 99 億歐元，除租賃外無負債。年初至 10 月 21 日回購 220 萬股、11 億美元，均價約 500 美元；2025 年 8 月恢復回購以來約 300 萬股，約占流通股 1.5%。以 FY2026 共識 EPS 13.45 計，買入時的盈餘收益率約 2.7%，低於十年期公債殖利率加 2%（殖利率事實表未涵蓋，但 2.7% 很難過關）。員工持股稀釋約 100 萬股已被抵銷，淨稀釋過關。收購（WhoSampled、Findaway、Sonantic）條件未揭露，無法算已實現報酬。現金去向四分、回購均價明細事實表未涵蓋。","fact_refs":["f_kpi4_free_cash_flow","f_kpi5_share_based_compensation","f_kpi0_total_revenue_ifrs","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年收購規模小、條件未揭露（WhoSampled 2025-11），無法計算已實現增量報酬"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"年初至 10-21 回購 220 萬股、11 億美元，均價約 500 美元；以 FY2026 共識 EPS 13.45 計盈餘收益率約 2.7%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"員工持股年稀釋約 100 萬股（約 0.5%）已被回購抵銷；Q3 SBC 約占營收 1.75%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，回購只中和稀釋並小幅退還現金；現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求公司在 2030 年前把營業利益率拉到 20% 以上、EPS 維持約兩成年增，而且市場到時仍給 27 倍左右；我信生意，但不信現在這個價格還留有足夠補償。","reasoning":"以 FY2026 共識 EPS 13.45 計本益比 43.4 倍，以 FY2027 的 17.24 計約 33.9 倍。FY2026→FY2028 共識年化約 27.8%，PEG 約 1.56。FY2026 已只剩一季，等同近乎實現值，所以主要看 FY2027。近三個月 FY2026 共識由 14.47 下修到 13.45（−7.05%），同期股價 26 週漲 12.78%，倍數上升不是盈餘推動。股價與 37 位分析師均值目標 594.92 美元只差 1.8%。兩年看，FY2028 共識 21.98 乘 28 倍約 615 美元，只有約 5%。五年 Base 若 FY2031 EPS 32.5、27 倍，約 878 美元、+50%，年化約 8.5% 加上約 0.7% 淨回購，落在中段偏弱；這段報酬全部來自 EPS，倍數是往下壓的。五年估值分位事實表未涵蓋（估值歷史只有最近一點）。同業倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"本益比（FY2026 43.4 倍、FY2027 33.9 倍）加 PEG","tier":null,"peers":{"expanded":false,"reason":"事實表同業只有利潤率，沒有同業本益比，無法做倍數對照"},"fwd_pe":43.44,"peg":1.56,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2027 本益比 33.9 倍、PEG 約 1.56，屬合理區間上緣；FY2026 共識三個月下修 7.05% 而股價上漲，倍數擴張；現價與分析師均值目標只差 1.8%；五年分位資料缺口。綜合判偏貴，比前份往貴一級。","upside_short_pct":1.8,"upside_mid_pct":5.3,"denominator_disputed":false,"denominator_note":"FY2026 EPS 含年內約 2 億歐元一次性費用墊高與隨股價波動的社會費用，已近乎實現值；改以 FY2027 為主要錨，結論不依賴分母爭議"}}},"q6_how_wrong":{"verdict":"最可能看錯在三處：唱片公司續約抽走毛利擴張、生態系對手吃掉成熟市場增量、以及好生意被我低估而股價續漲。","reasoning":"價值陷阱風險只亮一個信號（EPS 成長高於營收成長，原因是利潤率擴張），判中度。致命點是 2027 年 Q1 UMG 與 WMG 續約：以 TTM 營業利益率 14.65% 計，毛利率每少 1 個百分點，營業費用不變下營業利益少約 7%。第二是 YouTube Music 與大廠預載搶增量訂戶。第三個是反方向的錯：Q3 全部兌現、Q4 指引營業利益 8.2 億歐元，若 2027 年費用如承諾放緩，EPS 可能高於共識，等 480 美元可能等不到。監管與訴訟（土耳其調查、USTR 威脅、MLC 訴訟、律所調查）都沒有金額，列監測。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_rsi14","f_ma_state","f_kpi9_guidance_q4_2026","f_peer_spot_operating_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"生意不是陷阱，風險在上游分成與價格"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.45,"pe":43.44,"basis":"FY2026 共識 EPS（10 月時點的當年度 EPS）；終端同以 FY2031 當年度 EPS 為分母"},"eps":{"bull":[18.0,23.5,28.5,34.0,39.5],"base":[17.24,21.98,25.5,29.0,32.5],"bear":[15.0,15.8,16.3,16.8,17.2]},"pe":{"bull":33,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.7},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-60,"hi":-35,"basis":"現價 43.4 倍若壓回 FY2027 的 20–25 倍、EPS 停在 15–17 美元，價位約 300–425 美元，跌 27%–49%；再疊加 RSI 70.6 的過熱與 2026-04-28 財報後單日 −12.43% 的波動，下緣放到 −60%；前份為 −58%","trigger_time":null},"basis":{"bull":"續約條件持平，有聲書與加購推高 ARPU，2030 年營業利益率超過 20%，市場給 33 倍","base":"FY2027–FY2028 照共識，之後 EPS 年增降到 13%–18%，利潤率接近但未完全達 2030 目標，倍數收斂到 27 倍","bear":"2027 年 Q1 續約分成惡化加上生態系對手搶走增量，毛利率回到 32% 以下，EPS 五年停在 17 美元以下，倍數 20 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"20-F 自述大廠裝置預載使其居重大競爭劣勢；YouTube Music 美國訂戶一年 +45%；AI 帶來新的消費方式可能使年輕用戶轉移；UMG／WMG 2027 年 Q1 續約","assumption":"成熟市場增量訂戶被生態系對手吃掉，同時續約抬高授權分成，毛利率擴張停止","consequence":"Base 的利潤率路徑失效，EPS 停在 15–17 美元，倍數壓到 20 倍，股價約 340 美元","ruling":"部分採納：Bear 機率給 30%。反駁點是公司數據：逾 1 億用戶每月用 28 天、美國市占六年 +8–10pp、2025 年淨增各平台最多，Q3 訂戶還超出指引","watch":"年度訂戶淨增低於 2,000 萬；續約後兩季毛利率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"],"fact_refs":["f_kpi7_premium_subscribers","f_kpi3_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"現金 99 億歐元閒置；回購在 FY2026 約 43 倍本益比、均價約 500 美元買入；管理層保留併購彈性；投資人日說 2027 年成為完整納稅人、正常稅率約 22%；Gustav 說 AI 投資會維持在目前水準","assumption":"營運如期擴張，但稅率上升、高價回購與可能的大型收購稀釋每股報酬","consequence":"營業利益達標但每股 EPS 成長比營業利益慢，報酬再少 1–2 個百分點","ruling":"採納：資本配置判 B，回購收益率不過關；稅率正常化影響共識是否已計入事實表未涵蓋","watch":"2027 年有效稅率；單筆收購超過市值 5%；回購均價對應的本益比","evidence_refs":[],"fact_refs":["f_kpi4_free_cash_flow","f_consensus_eps_fy1"]},{"view":"價格已反映太多","evidence":"股價 584 美元與分析師均值 594.92 美元只差 1.8%；FY2026 共識三個月下修 7.05% 而股價 26 週漲 12.78%；RSI 70.6；Q2 營業利益指引曾低於共識約 8%","assumption":"市場已經把 2030 年利潤率目標當成會達成","consequence":"Base 五年年化只有約 9%，兩年上檔約 5%，任何一次指引落空都會讓倍數先壓","ruling":"採納：這是本次觀望的唯一約束","watch":"股價對 FY2027 共識的倍數；共識修正方向","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"MLC 2024 年 5 月就授權費提告；土耳其競爭局調查演算法歧視與掠奪性定價；USTR 2025-12 威脅報復；Pomerantz 律所 2026 年 5 月宣布調查，起因是 Q1 財報後單日跌 12.43%","assumption":"其中一案演變成費用或處分，直接吃掉利潤率擴張","consequence":"若處分或新增費用超過年營業利益 5%，Base 路徑要下修","ruling":"反駁：目前都沒有金額，律所只是調查通知、未見已提起的集體訴訟，USTR 只是威脅；Drake 灌水案已獲駁回。列監測不進情境","watch":"任一案出現金額或判決；USTR 是否實施","evidence_refs":["major_events#0","major_events#1","lawsuit_class_action#0","regulatory_antitrust#1","regulatory_antitrust#3","reg_tariff_export#0"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 479.77 → 本次 584.22（+21.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=479.77","side_b":"本次 price_at_dd=584.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 479.77 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 479.77 美元：Bull 價 1,224、Bear 價 360，五年期望值 +62.0%，基準年化 11.5%，不對稱比 4.8","side_b":"本次情境、股價仍用 479.77 美元：Bull 價 1,303.5、Bear 價 344，五年期望值 +71.7%，基準年化 12.8%，不對稱比 5.06","ruling":"先換情境、股價不動：五年期望值多 9.7 個百分點，基準年化多 1.3 個百分點。不對稱比由 4.8 變為 5.06。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 479.77 美元：五年期望值 +71.7%，基準年化 12.8%，不對稱比 5.06","side_b":"本次情境、股價 584.22 美元：五年期望值 +41.0%，基準年化 8.5%，不對稱比 2.5","ruling":"再換股價、情境不動：起點價上漲 21.8%，五年期望值少 30.7 個百分點，基準年化少 4.4 個百分點，不對稱比由 5.06 降到 2.5。合計五年期望值比前份少 21.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價上漲帶動的估值與情境機率變動","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 479.77 美元，估值中性偏貴，Bull 25%／Bear 32%，最大回撤 −58%，裁決觀望","side_b":"股價 584.22 美元（+21.8%），FY2026 共識同期下修，FY2026 本益比 43.4 倍、FY2027 約 33.9 倍，估值改偏貴；Bull 25／Base 45／Bear 30；回撤區間 −35%～−60%","ruling":"估值結論往貴一級。Bear 機率由 32% 降到 30%，因 Q3 營收、訂戶、毛利率全數達標或超標，但價格上漲讓報酬變薄，裁決仍是觀望","evidence_level":"公司財報、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["股價回到 480 美元以下且 FY2027 共識未下修超過 5% → 重跑後分批進場","股價續漲但 Q4 營業利益未達 7.8 億歐元 → 不追"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"跑道判讀","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判中等跑道","side_b":"判寬：Q3 法說首次量化全球付費滲透不到 4%、英德 20%–25%、拉美約 11%、新興市場不到 3%；有聲書年底擴到 180 多個市場","ruling":"改判寬。滲透率遠低於 35%，且有聲書已是有營收的第二條曲線（Audiobooks+ 年化經常性收入逾 1 億美元）","evidence_level":"公司法說","settle_metric":"新興市場訂戶占淨增比重；有聲書擴張後 ARPU","if_then":["新興市場淨增放緩且有聲書擴張後兩季 ARPU 沒有改善 → 改回中等跑道"],"evidence_refs":[]},{"axis":"維持不變的判斷","cause":"新證據","prior_field":["signal","trap","moat_trend","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱中度、護城河持平、品質複利成長型、非循環股","side_b":"本次相同","ruling":"新證據兩邊都有：Q3 毛利率年增約 140bp、廣告回升到 +9% 支持執行面；YouTube Music 美國 +45% 與 2027 年 Q1 續約壓住方向。結論不動","evidence_level":"公司財報、第三方產業資料","settle_metric":"續約後毛利率；年度訂戶淨增","if_then":["續約後兩季毛利率都不低於 32.8% 且年淨增超過 2,500 萬 → 護城河改判擴大"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","side_b":"股價回落至 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識同期下修不超過 5%","ruling":"北美回穩已由 Q3 各區域訂戶季增兌現，不再是約束；Suno 判決結果證據包未涵蓋，不作條件。現在唯一約束是價格，進場改成價格錨；480 美元由 FY2027 共識 17.24 乘 28 倍得出","evidence_level":"公司法說、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["條件達成 → 重跑後分批進場，首筆小倉位","共識下修超過 5% → 進場價同步下移"],"evidence_refs":[]},{"axis":"賣出門檻新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設賣出門檻（null）","side_b":"季毛利率連 2 季低於 32.8%；年度訂戶淨增低於 2,000 萬；FY+1 共識三個月下修超過 10%；營業利益連 2 季低於自家指引超過 5%","ruling":"Q3 法說點名 2027 年 Q1 續約節點，前份的毛利率門檻要落成可執行的賣出條件","evidence_level":"公司法說","settle_metric":"續約後季毛利率","if_then":["持有時毛利率連 2 季低於 32.8% → 減碼一半","毛利率門檻觸發後年淨增也低於 2,000 萬 → 清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"2027 年 Q1 UMG／WMG 兩年期合約續約時，核心串流授權分成條件惡化","ruling":"毛利率是 EPS 路徑數學上最大的單一敏感項：毛利率每少 1 個百分點，營業利益少約 7%。Q3 法說最後一題首次點名續約時點，因此設為唯一致命點","evidence_level":"公司法說","settle_metric":"續約後兩季毛利率與 2030 毛利目標是否改口","if_then":["續約後毛利率指引下修或 2030 目標改口 → Bear 機率上調到 40%，不進場；持有則減碼一半"],"evidence_refs":[]},{"axis":"廣告承諾措辭","cause":"新證據","prior_field":null,"side_a":"投資人日與 Q2 法說：廣告下半年回到兩位數成長","side_b":"Q3 廣告 +9%，CFO 改說 Q4「繼續往兩位數前進」","ruling":"可調和的程度差異：方向兌現（3%→9%），時點往後挪。廣告只占營收約一成，影響有限；但連續措辭軟化要記。Q2 營業利益指引也曾低於共識約 8%","evidence_level":"法說逐字稿","settle_metric":"Q4 2026 廣告成長率","if_then":["Q4 廣告仍低於 10% 且 2027 年 Q1 仍無兩位數 → 管理層承諾可信度下調，進場價再下移 5%"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：Q3 全部達標、Q4 指引營業利益 8.2 億歐元、費用增速 2027 年續降、無負債現金 99 億歐元、過去 12 個月 FCF 32 億歐元、付費滲透不到 4%，好生意少有便宜價","side_b":"觀望：價格已貼近分析師均值，FY2027 本益比約 34 倍，五年 Base 年化約 9%，續約結果未知","ruling":"觀望。生意好不等於現在這個價位有補償；唯一約束是價格","evidence_level":"公司財報、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["股價 480 美元以下且共識未下修 → 分批進場","Q4 達標且 2027 年費用增速低於營收增速、共識上修超過 5% → 進場價上調到 FY2027 共識 30 倍"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q4 2026 營業利益是否達指引","type":"假設驗證","maps_to":"H3","metric":"Q4 2026 營業利益","threshold":"≥ 7.8 億歐元（指引 8.2 億的 95%）","action":"未達 → 不追，Bear 機率上調 5 個百分點","source_freq":"季報（每季）","date":"2027-02","evidence_refs":[]},{"n":2,"text":"UMG／WMG 兩年期續約後的毛利率","type":"Single Thing","maps_to":"R1","metric":"季毛利率","threshold":"續約後連 2 季低於 32.8% 或年減","action":"觸發 → 不進場；持有則減碼一半","source_freq":"季報（每季）","date":"2027-05","evidence_refs":[]},{"n":3,"text":"價格回到有補償的區間","type":"估值rearm","maps_to":null,"metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤ 480 美元且 FY2027 共識下修不超過 5%","action":"重跑後分批進場，首筆小倉位","source_freq":"每日股價、共識快照","date":null,"evidence_refs":[]},{"n":4,"text":"生態系對手搶走增量訂戶","type":"風險","maps_to":"R2","metric":"年度 Premium 訂戶淨增","threshold":"低於 2,000 萬","action":"護城河改判縮減，不進場","source_freq":"季報（每季）","date":"2027-02","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"n":5,"text":"共識持續下修","type":"風險","maps_to":"R5","metric":"FY+1 共識 EPS 三個月修正","threshold":"下修超過 10%（目前 −7.05%）","action":"進場價同步下移，停止加碼","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#0"]},{"n":6,"text":"Q4 財報與 2027 年展望後複審","type":"複審日期","maps_to":null,"metric":"Q4 結果與 2027 年費用、毛利指引","threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季毛利率（IFRS）","bear_threshold":"連 2 季低於 32.8% 或年減","window":"2027 年 Q1 續約後連續 2 季","source":"公司季報 6-K","last_status":"ok"},{"metric":"年度 Premium 訂戶淨增","bear_threshold":"低於 2,000 萬","window":"會計年度","source":"公司季報 6-K","last_status":"ok"},{"metric":"FY+1 共識 EPS 三個月修正","bear_threshold":"下修超過 10%","window":"滾動 90 天","source":"Koyfin 共識快照","last_status":"warning"},{"metric":"營業利益相對公司自家指引","bear_threshold":"連 2 季低於指引超過 5%","window":"滾動 2 季","source":"公司季報與法說","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識同期下修不超過 5%","exec_line":"條件達成後先重跑判斷，再分兩批進場，首筆小倉位；Q4 營業利益未達 7.8 億歐元時不追","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識下修不超過 5%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"qc48_result":"pass","qc48_note":"Bull 路徑是用量加價與利潤率目標撐起來的，但 EPS 沒有被推導到數字，歷史上高倍數成長股的 5 年報酬多半低於本案隱含的 17.4%，runway 的滲透率證據也還沒能回到原文，三項都不到站穩的程度，也沒有哪一項能直接判為不成立。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=12.78, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑是用量加價與利潤率目標撐起來的，但 EPS 沒有被推導到數字，歷史上高倍數成長股的 5 年報酬多半低於本案隱含的 17.4%，runway 的滲透率證據也還沒能回到原文，三項都不到站穩的程度，也沒有哪一項能直接判為不成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識下修不超過 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"訂戶與 ARPU 雙引擎持續：總 Premium 訂戶年增至少 8%，ARPU 固定匯率年增至少 3%","2y":"2028 年 Q4 訂戶約 3.7 億","5y":"2031 年訂戶約 4.5 億，ARPU 每年仍正成長","10y":null,"threshold":"Premium 訂戶年增 ≥ 8%；Premium ARPU（固定匯率）年增 ≥ 3%","source":"公司季報 6-K 與法說","drift_rule":"訂戶年增連 4 季低於 7.6% → 削弱；連 6 季低於 7.2% → 反轉"},{"id":"H2","text":"利潤率朝 2030 年目標擴張：毛利率 35%–40%、營業利益率 20% 以上","2y":"FY2027 毛利率至少 33.8%（FY2026 約 33.3% 加 50bp）","5y":"FY2030 毛利率 ≥ 35%、營業利益率 ≥ 20%","10y":null,"threshold":"全年毛利率年增 ≥ 50bp；季毛利率不低於 32.8%","source":"公司季報 6-K、投資人日 2030 目標","drift_rule":"季毛利率連 4 季年減 → 削弱；續約後連 2 季低於 32.8% → 反轉"},{"id":"H3","text":"投資年過後營業利益增速回到高於營收：Q4 2026 營業利益兌現，2027 年營業費用增速低於營收增速","2y":"Q4 2026 營業利益 ≥ 7.8 億歐元；FY2027 共識 EPS 不低於 16.4","5y":null,"10y":null,"threshold":"Q4 2026 營業利益 ≥ 7.8 億歐元（指引 95%）；FY2027 共識 EPS ≥ 16.4（現值 95%）","source":"公司季報與法說、Koyfin 共識快照","drift_rule":"連 2 季偏離門檻 5% 以上 → 削弱；連 3 季偏離 10% 以上 → 反轉"}],"R":[{"id":"R1","text":"UMG／WMG 2027 年 Q1 續約提高核心串流授權分成，壓住毛利率擴張","h_ref":"H2","clock":"🔥","threshold":"續約後連 2 季毛利率低於 32.8% 或年減","evidence_refs":[]},{"id":"R2","text":"生態系對手（YouTube Music、Apple、Amazon 預載）與 AI 新消費方式搶走增量訂戶，尤其年輕族群","h_ref":"H1","clock":"🔥","threshold":"年度 Premium 淨增低於 2,000 萬（管理層自述 2018 年起每年 ≥ 2,500 萬）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]},{"id":"R3","text":"漲價邊際失效：漲價後流失上升，Q1 2026 北美淨增曾偏軟","h_ref":"H1","clock":"⚡","threshold":"任一主要區域漲價後該區訂戶連 2 季季減","evidence_refs":["supply_demand_durability#1"]},{"id":"R4","text":"監管與訴訟成本：土耳其反壟斷調查、USTR 報復威脅、MLC 授權費訴訟","h_ref":"H2","clock":"🐢","threshold":"任一案出現處分或新增費用超過年營業利益 5%","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#3","reg_tariff_export#0","major_events#0"]},{"id":"R5","text":"指引落空與共識下修：Q2 營業利益指引曾低於共識約 8%，Q1 財報後單日跌 12.43% 並引來律所調查","h_ref":"H3","clock":"⚡","threshold":"營業利益連 2 季低於自家指引超過 5%，或 FY+1 共識三個月下修超過 10%","evidence_refs":["capital_markets_pricing#0","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"2027 年 Q1 UMG 與 WMG 兩年期合約續約時，核心串流授權分成條件惡化","why_fatal":"Base 的 EPS 路徑靠毛利率往 35%–40% 擴張；以 TTM 營業利益率 14.65% 計，毛利率每少 1 個百分點，營業費用不變下營業利益少約 7%，五年 EPS 路徑直接下移","if_happens":"Base 毛利率路徑下修、Bear 機率上調到 40%，不進場；若已持有則減碼一半，毛利率再低於 32.8% 兩季則清倉","how_monitor":"續約公告、續約後兩季毛利率、管理層是否改口 2030 年毛利目標","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":33.89,"peg_fy2":1.22,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.51,"FY2026E":13.45,"FY2027E":17.24,"FY2028E":21.98},"fy_end_month":12,"eps_basis":"FY2026–FY2028 為 Koyfin 共識（事實表標美元）；FY2025A 取年報稀釋 EPS 10.51，公司以歐元報表，基期與共識可能幣別不同"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"有聲書擴展到 180 多個市場完成","impact":"中","watch":"Q4 毛利率是否守住 33.8% 指引"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年展望","impact":"高","watch":"營業利益是否達 7.8 億歐元以上、2027 年費用增速"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"UMG／WMG 兩年期合約續約節點","impact":"高","watch":"續約後兩季毛利率與 2030 毛利目標措辭"}]}
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
