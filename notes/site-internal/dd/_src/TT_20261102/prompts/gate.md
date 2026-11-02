你是 DD 管線 v20 的判斷層閘（gate），標的 TT（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（46 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，持續營運）＝6759.7 USD m（YoY +18%，有機 +16%；去年同期 5742.5）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP（調整後）營業利益＝1363.8 USD m；利益率 20.2%（去年同期 20.6%，-40bps）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝1343.1 USD m；利益率 19.9%（去年同期 20.3%，-40bps；YoY +15%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi4_eps`（q1_business）｜調整後持續營運 EPS＝4.86 USD（YoY +25%；GAAP 4.79，去年同期 3.88／3.82）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無單季共識；FY 對照見 consensus_revision（FY1 15.28，財報前快照）
- `f_kpi5_bookings`（q1_business）｜訂單 Bookings＝7248 USD m（YoY +21%，有機 +20%；去年同期 5979）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi6_book_to_bill`（q1_business）｜Book-to-bill＝107 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi7_backlog`（q1_business）｜Backlog 在手訂單＝12.5 USD bn（YoY +73%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_kpi8_2026`（q1_business）｜管理層全年 2026 指引＝reported_rev_growth 約 13.5%（上調）；organic_rev_growth 約 11%（上調）；adj_EPS 15.20–15.30（維持）；GAAP_EPS 15.00–15.10 FY2026｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：FY1 共識 EPS 15.28（consensus_revision，落在指引區間內）
- `f_peer_tt_gross_margin_pct`（q2_moat）｜TT 毛利率＝34.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_operating_margin_pct`（q2_moat）｜TT 營業利益率＝17.92 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_fcf_margin_pct`（q2_moat）｜TT FCF 利潤率＝16.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_carr_gross_margin_pct`（q2_moat）｜CARR 毛利率＝24.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_carr_operating_margin_pct`（q2_moat）｜CARR 營業利益率＝8.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_carr_fcf_margin_pct`（q2_moat）｜CARR FCF 利潤率＝10.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_jci_gross_margin_pct`（q2_moat）｜JCI 毛利率＝36.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_operating_margin_pct`（q2_moat）｜JCI 營業利益率＝14.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_fcf_margin_pct`（q2_moat）｜JCI FCF 利潤率＝6.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_gross_margin_pct`（q2_moat）｜LII 毛利率＝33.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_operating_margin_pct`（q2_moat）｜LII 營業利益率＝19.94 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_fcf_margin_pct`（q2_moat）｜LII FCF 利潤率＝15.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi3_fcf_9_q3`（q4_capital）｜自由現金流（FCF，年初至今 9 個月；Q3 單季新聞稿未載）＝2827.5 USD m（YTD，去年同期 1786.0，約 +60%；營業現金流 YTD 3060.1，淨資本支出 264.2）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：查無（新聞稿未載共識，未自行填造）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝15.28 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝17.7 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝20.33 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝24139.46 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝26525.58 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝2990.2 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 4217.6、現金 1227.4（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝218.9 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.768 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝92737.29 USD m｜期間與口徑：2026-11-02／市值 89747.09 ＋ 淨負債 2990.2｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝410.0 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.83 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 15.28，分子＝快照價 410.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝28.49 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝53.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝53.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.86 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝74.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝74.2 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.99 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝71.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝71.4 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.84 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.48 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 14.91 → 15.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.07 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（15.29 → 15.28）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-15.33 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝31.37｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 410.0 / W52 441.74 / W104 418.19 / W250 298.0 / W250 13週斜率 1.45%」
- `f_ma_w104`（q5_valuation）｜104 週均線＝418.19 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝298.0 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子載明產業已有整併與新進入者（含非傳統競爭者），可能加劇競爭與價格壓力，並有來自非傳統製造商的顛覆性技術風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：HVAC Equipment Antitrust Litigation：2026-03-20 於 E.D. Michigan 提起，被告含 Trane Technologies plc，主張 Sherman Act 第 1 條價格壟斷；2026-05-15 合併案件。
  - 來源：Justia Dockets HVAC Equipment Antitrust Litigation（as_of 2026-05-15）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 風險因素：美國已對多國商品加徵關稅並引發報復性關稅，另可能有進出口管制，公司稱無法預測關稅範圍，且限制可能無預警實施
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：Q4 2025 財報電話會議：2025年關稅成本略高於1.4億美元，預期2026年有更多通膨影響
  - 來源：Yahoo Finance: Trane Technologies Q4 earnings call（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年關稅成本略高於 1.4 億美元，2026 年因多一季關稅預期再增約 5,000 萬美元通膨影響；管理層先以緩解措施、必要時才訂價因應。
  - 來源：Trane Technologies Bank of America Conference Transcript 2026（as_of 2026-05-13）｜affects：valuation、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年約 25% 營收來自美國以外；管理層點出中東區域逆風（Q2 約 5,000 萬美元營收）與中國市場艱困。
  - 來源：Trane Technologies Q1 2026 Earnings Call Transcript (MarketBeat)（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露部分品項向單一或有限來源供應商採購（成本效益、法規要求、設計獨特性或產品品質），並稱許多客戶、製造營運與供應商位於美國以外。
  - 來源：Trane Technologies plc Form 10-K FY2025（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FY2025 10-K 風險因子承認有來自非傳統製造商/服務商的顛覆性技術風險，且技術變遷加速會縮短產品生命週期；未點名具體替代品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：ACHR News：Nvidia CEO 稱最新 AI 系統可用熱水冷卻、無需冷水機，多家 HVAC 廠商股價下跌；Rubin 系統預計 2026 下半年上市。
  - 來源：ACHR News - Cooling without water chillers（as_of 2026-02-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：10-K FY2025：最重大訴訟為 Aldrich 與 Murray 石棉破產案，管理層認為待決法律事項預期不會有重大不利影響
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：搜尋未見證券集體訴訟；10-K 稱最重大訴訟為 Aldrich／Murray 石棉破產案，其餘待決事項預期無重大影響
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":912.0,"bear_5y_price":291.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":48.1,"ev5y_pct":43.6,"irr_base_pct":8.2,"asym_ratio":3.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":15.28,"pe":26.83,"basis":"FY2026E 共識調整後持續營運 EPS 15.28（公司指引 15.20–15.30），起點本益比 26.83 倍；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[18.3,21.4,24.4,27.4,30.4],"base":[17.4,19.7,21.8,23.6,25.3],"bear":[15.6,14.4,14.0,15.0,16.2]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.768,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TT_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO Chris Kuehn｜guidance：全年調升：調整後 EPS 區間 $15.20–$15.30（有機營收約 9% 於同段）（原話："our adjusted EPS guidance to a range of $15.20 to $15.30."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q3 指引：有機營收約 +10%、調整後 EPS 約 $4.70（原話："with adjusted EPS of approximately $4.70."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q3 利潤率預期擴張約 50 bp 等級（原話："We would expect margin expansion in the third quarter."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q4 目標利潤率擴張超過 1 個百分點（原話："we'd be targeting over 1 point"）
- 2026-07-30｜CFO Chris Kuehn｜margin：報告槓桿與有機槓桿之間約 700 bp 差距，來自併購與第一年投資（原話："about a 700 basis point delta between reported leverage"）
- 2026-07-30｜CFO Chris Kuehn｜margin：價格對比通膨在 Q2 為逆風，下半年仍略為逆風（原話："a bit of a headwind in the second half of the year as well."）
- 2026-07-30｜CEO Dave Regnery｜margin：CEO 稱不介意單季或單半年的槓桿（原話："concerned about leverage in any quarter or really in any"）
- 2026-07-30｜CEO Dave Regnery｜commitment：長期槓桿目標 25% 以上，Q2 低於該水準（原話："our target is 25% plus. We may have a quarter like the"）
- 2026-07-30｜CFO Chris Kuehn｜margin：EMEA 因中東衝突採取成本行動，預期下半年減損落在毛利率之內（原話："we do expect deleverage to be within gross margins"）
- 2026-07-30｜CFO Chris Kuehn｜risk：EMEA 中東營收 Q2 下滑約 30%，下半年指引同樣假設下滑約 30%（原話："we're anticipating to be down about 30%."）
- 2026-07-30｜CFO Chris Kuehn｜risk：6 月底採取成本行動（調整人員與基礎設施）（原話："we did take some cost actions at the end of June."）
- 2026-07-30｜CEO Dave Regnery｜customer：Q2 企業有機訂單 +37%，積壓訂單創高 $12.1 billion、年增 70%（原話："record backlog of $12.1 billion, up 70% year-over-year."）
- 2026-07-30｜CEO Dave Regnery｜customer：約 $6 billion 積壓訂單排在 2027 年及之後（原話："approximately $6 billion slated for 2027 and beyond."）
- 2026-07-30｜CEO Dave Regnery｜customer：Applied 訂單 +130%（原話："Applied bookings were up 130%"）
- 2026-07-30｜CEO Dave Regnery｜customer：14 個垂直領域中，年初至今 11 個訂單成長（原話："growth in 11 of 14 verticals from an order standpoint."）
- 2026-07-30｜COO Donny Simmons｜customer：Q2 有 4 筆超過 1 億美元訂單，其一來自 Stellar（原話："we had 4 orders that were over $100 million"）
- 2026-07-30｜CEO Dave Regnery｜customer：超大規模客戶多有主採購協議或長期產能承諾（原話："master purchase agreement or a long-term capacity commitment"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：預期長期部署 100% 的超額現金（原話："we expect to deploy 100% of excess cash over time."）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：2026 資本部署目標 $2.8–$3.3 billion（原話："deployment of $2.8 billion to $3.3 billion"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：年初至今買回約 $840 million 股票（原話："repurchased approximately $840 million of shares"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：現行買回授權剩餘 $3.8 billion（原話："$3.8 billion remaining on our current share repurchase"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：2026 CapEx 預期為營收的 2%–3%（原話："expected CapEx of 2% to 3% of revenue in 2026."）
- 2026-07-30｜CFO Chris Kuehn｜commitment：管理層表示不拒單、產能不落後（原話："we're not turning away any orders"）
- 2026-07-30｜CEO Dave Regnery｜commitment：Applied 產能過去三年擴充 4 倍，仍在擴充（原話："applied capacity 4x over the last 3 years."）
- 2026-07-30｜CEO Dave Regnery｜risk：供應鏈限制比平常多一些但可管理（原話："we are asking more from our supply partners."）
- 2026-07-30｜CFO Chris Kuehn｜risk：指引已假設部分專案延遲（leakage/breakage）（原話："assume some level of leakage, breakage in the guide, right?"）
- 2026-07-30｜CFO Chris Kuehn｜risk：資料中心專案可能位移（原話："So could there be some things that shift?"）
- 2026-07-30｜CEO Dave Regnery｜product：資料中心冷卻創新快，稱冰水機組變得更聰明（原話："think of chillers as getting smarter."）
- 2026-07-30｜COO Donny Simmons｜competition：市場整體朝風冷傾向（原話："the overall market has trended more towards air"）
- 2026-07-30｜CEO Dave Regnery｜product：LiquidStack 併購優於預期（原話："The LiquidStack acquisition is exceeding our expectations"）
- 2026-07-30｜CEO Dave Regnery｜product：不做冷板（cold plates）（原話："we don't have cold plates."）
- 2026-07-30｜CEO Dave Regnery｜product：電池儲能租賃等仍屬早期（原話："So we're still early days."）
- 2026-07-30｜CEO Dave Regnery｜guidance：Stellar 納入指引的 EPS 為持平，前一季說法為略有加分（原話："being flat for the year from an EPS standpoint."）
- 2026-07-30｜COO Donny Simmons｜guidance：Stellar 2026 營收仍預期 $500 million（原話："we expect the Stellar business to be $500 million in"）
- 2026-07-30｜CEO Dave Regnery｜customer：住宅今年預期中個位數成長，年初預期可能下滑、Q1 末修正為持平（原話："a mid-single-digit growth number for us in 2026"）
- 2026-07-30｜CEO Dave Regnery｜customer：住宅聚焦替換市場而非新建（原話："heavily focused on the replacement, not on new construction"）
- 2026-07-30｜CFO Chris Kuehn｜customer：年初至今住宅 sell-in 約等於 sell-through（原話："sell-in is really approximately equal to sell-through."）
- 2026-07-30｜CEO Dave Regnery｜customer：Americas 運輸市場預期 2026 下半年改善，內部假設復甦斜率較 ACT 平緩（原話："assumes a more gradual slope of recovery."）
- 2026-07-30｜CEO Dave Regnery｜customer：Thermo King 預期下半年轉為成長引擎（原話："Thermo King is going to be transitioning into more of a"）
- 2026-07-30｜CEO Dave Regnery｜customer：亞洲除中國外成長，加碼通路投資（原話："we're also doubling down on some of our investments"）
- 2026-07-30｜CFO Chris Kuehn｜customer：中東占企業營收不到 3%（原話："the Middle East is less than 3% of our total enterprise"）
- 2026-07-30｜CFO Chris Kuehn｜commitment：2027 出口率：管理層說再多幾季才會校準 2027（原話："let's get a few more quarters in before we dial in 2027"）

### 問答異常語氣（迴避／改口／保留）
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Mehrotra：下半年成長出口率是否為 2027 起點、供應鏈能否跟上｜答法：CFO 未給 2027 數字，表示再多幾季才校準 2027
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Mehrotra：是否已到訂單高峰｜答法：CEO 改談過去訂單規模與管線強勁，未直接回答是否高峰
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Ritchie：CDU 業務占積壓比重與趨勢｜答法：CEO 表示不會講到那個細節，僅稱業績與管線良好
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Hammond：Stellar 營收節奏｜答法：管理層重申營收 $500M 未變，EPS 假設由前一季的略有加分改為持平

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 1 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 6 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 5 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260731","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"核心商用 HVAC 的訂單洪流是廣泛的、不是單一垂直市場的——因此其可持續性高於「資料中心敘事」所隱含者"},{"id":"H2","text":"定價權與資本效率同時維持：產品組合升級（applied／高效／控制／液冷）持續推升毛利率與 ROIC，且投資前置只是階段性壓抑增量槓桿"},{"id":"H3","text":"紀錄 backlog 提供的是「一年半」能見度，不是「多年」——但足以讓 FY26-27 營收預測的變異數低於同業"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler 資本支出於 2027 進入消化期，同時商用建築與貨運週期下行。"},{"id":"R2","text":"HVAC 價格操縱民事集體訴訟（Carrier／Trane／Rheem 等，2026 年 3-5 月 5 案合併於密西根聯邦法院；控以疫情／法規變動為掩護協調漲價；TT 否認，未經法院認定，無 DOJ 刑事立案證據）。"},{"id":"R3","text":"資料中心 bolt-on 整合失敗與出價紀律惡化。"},{"id":"R4","text":"資料中心熱管理的美元往晶片端位移：TT 明言不做冷板、依賴夥伴；浸沒式「還有一段距離、有些挑戰」。"},{"id":"R5","text":"宏觀成本／法規外生變數（關稅、A2L 冷媒轉換、Pillar Two 全球最低稅負）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已持有續抱＋首階加碼 1/3；再加碼＝$415 以下，或 FY26 有機增量槓桿回到 25%＋","irr_base_pct":9.0,"ev5y_pct":49.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.2,"ev5y_pct":49.0,"irr_base_pct":9.0,"max_dd_pct":-48.0,"bull_5y_price":910.0,"bear_5y_price":285.0,"p_bull_pct":27.0,"p_bear_pct":25.0,"rearm_trigger":"已持有續抱＋首階加碼 1/3；再加碼＝$415 以下，或 FY26 有機增量槓桿回到 25%＋","price_at_dd":440.28,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TT","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Trane Technologies plc"},"oneliner":"需求面強：第三季訂單 +21%、在手訂單 125 億美元其中逾 80 億排在 2027 年後，自由現金流高於淨利；成本面弱：全年價格只剩約 1 個百分點、追不上通膨，增量槓桿降到兩成出頭。410 美元約當年度 26.8 倍，合理不便宜，勝負看第四季槓桿能否回到 25%，以及資料中心訂單會不會斷層。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺建物業主與資料中心營運者的錢：大型冰水機與空調系統在設計階段就被指定，之後由自家技師的服務綁住已安裝基礎，錢卡在系統設計與服務這兩個節點。第三季營收 67.6 億美元（年增 18%，有機 16%），調整後營益率 20.2%（年減 40bp）。","reasoning":"收錢方式：設備（Applied 冰水機與空調箱、單元機、住宅空調、Thermo King 運輸冷凍）加服務。服務約占營收三分之一，2020 年以來低雙位數複合成長，技師全是自家員工（第三季法說 CEO）。分部：美洲占第三季營收約 84%，歐中非與亞太合計約 16%；美國約占營收 75%（10-K FY2025）。單點依賴：沒有單一客戶占合併營收 10% 以上（10-K FY2025），所以集中度風險不在客戶，而在成長來源：追蹤中的 1,700 個大型專案逾九成是資料中心，Stellar 幾乎全為資料中心；上游部分零件為單一或有限來源。產業時鐘判為擴張期：第三季訂單 72.5 億美元（+21%）、訂單/營收比 107%、在手訂單 125 億美元（+73%），運輸冷凍在多年下行後轉入上行，14 個垂直市場有 11 個成長。不過供應鏈吃緊與全面通膨已是擴張後段的跡象。供需判讀：以結構性持久為主，資料中心段落有週期性反轉風險。單價與量拆分、分部利潤事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi4_eps","f_kpi5_bookings","f_kpi6_book_to_bill","f_kpi7_backlog","f_kpi8_2026"],"verdict_values":{"revenue_quality":"設備為主、服務約三分之一；在手訂單只含設備不含服務，逾 80 億美元排在 2027 年及以後（第三季法說 CFO）；第三季有機成長 16%，價格只貢獻約 0.5 個百分點，成長幾乎全來自量","unit_econ_note":"單價與量的結構化數字事實表未涵蓋；第三季企業價格約 +0.5 個百分點、美洲約 +0.6、歐中非約 +0.5、亞太約 −1（中國），運輸因大車隊組合為負（第三季法說 CFO）","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"高","fingerprint":"資本支出約營收 2%、自由現金流約等於淨利、服務占三分之一、在手訂單提供一到兩年能見度；住宅與運輸冷凍帶短週期"},"industry":{"clock_phase":"II","sd_verdict_source":"以結構性持久為主、資料中心段落有週期性反轉風險：第三季訂單 +21%、在手訂單逾 80 億美元排在 2027 年及以後、14 個垂直市場有 11 個成長（第三季新聞稿與法說）；資料中心專案時程可能因場址與電力併網而位移（第二季法說）","bargaining":{"up":"上游風扇、線圈、熱交換器產能吃緊，部分零件為單一或有限來源；TT 占 Cancoil 約 40% 的量，議價力在 TT，但短期缺的是產能不是價格，今年價格對通膨為逆風","down":"沒有客戶占營收 10% 以上；超大規模客戶以主採購協議或長期產能承諾鎖量，大單議價力偏向客戶；住宅經銷通路量增時獎勵增加，壓縮實現價格","geo":"約 75% 營收在美國，北美 21 座廠有 20 座在美國、在美銷售逾 95% 為美國製造或組裝；中東衝突與中國價格競爭是區域逆風"},"profit_pool_dir":"核心建築 HVAC 與服務的利潤池穩定擴大；資料中心熱管理的利潤池有往晶片端與液冷段位移的風險，TT 以 LiquidStack（CDU）與 Stellar（模組化冰水站）補位，但不做冷板","tam_table":[{"item":"資料中心 HVAC 市場（ABI Research，2026-01）","value":"液冷 9.7 億美元、占 15%，回推整體約 65 億美元；口徑可能偏窄，與 TT 的大型專案管線不易對齊"},{"item":"液冷 2030 年預估","value":"35 億美元，年複合約 20%；營運商採液冷加氣冷的兩段式冷卻"},{"item":"TT 資料中心營收占比與份額","value":"事實表未涵蓋；Stellar 2026 營收約 5 億美元、幾乎全為資料中心"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋，無法判斷是否淨流出 5 個百分點以上"}]}}},"q2_moat":{"verdict":"護城河方向穩定（→），等級 B：執行面擴大，定價面今年轉弱，兩者相抵。","reasoning":"機制：大型冰水機與 Applied 系統在設計與規格階段被指定，自家員工技師的服務綁住已安裝基礎，並以系統層級的熱管理工程被邀入超大規模資料中心的參考設計。評分：執行 9（第三季有機訂單 +20%、全球 Applied 訂單逾 +40%、年初至今自由現金流 28.3 億美元）；定價 7（全年價格由 1.5 降到約 1 個百分點、價格對通膨為逆風、有機增量槓桿下修到 20% 出頭，但商用 HVAC 仍是正價格，第四季價格預計回到 1.5 個百分點）。資料中心散熱往晶片端位移列為生態攻擊、扣 1 分，綜合落在 B。同業對照（近 12 個月）：營益率 TT 17.9%、LII 19.9%、JCI 14.5%、CARR 8.1%；FCF 利潤率 TT 16.4%，四家最高；毛利率 TT 35.0%，低於 JCI 36.7%、高於 LII 33.1% 與 CARR 24.6%。同業 ROIC 與份額事實表未涵蓋，無法驗證報酬差距是否擴大，所以不給 A。當期 ROIC：次要來源稱約 28%（TIKR，2026-08），投入資本口徑事實表未涵蓋。再投資：FY2023–FY2025 累計自由現金流 76.8 億美元，高於累計淨利 75.1 億美元，有機淨再投資接近零，增量報酬算不出；內生上界改以 FY2022–FY2025 營收年複合 10.1% 代理。","fact_refs":["f_peer_tt_gross_margin_pct","f_peer_tt_operating_margin_pct","f_peer_tt_fcf_margin_pct","f_peer_carr_gross_margin_pct","f_peer_carr_operating_margin_pct","f_peer_carr_fcf_margin_pct","f_peer_jci_gross_margin_pct","f_peer_jci_operating_margin_pct","f_peer_jci_fcf_margin_pct","f_peer_lii_gross_margin_pct","f_peer_lii_operating_margin_pct","f_peer_lii_fcf_margin_pct","f_kpi5_bookings","f_kpi7_backlog","f_kpi3_fcf_9_q3"],"verdict_values":{"moat":{"mechanism":"大型冰水與 Applied 系統在設計階段被指定，加上自家員工技師維護已安裝基礎（服務約占營收三分之一、2020 年以來低雙位數複合成長），以及系統層級的熱管理工程能力（被邀入超大規模資料中心參考設計）","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：第三季有機訂單 +20%、全球 Applied 訂單逾 +40%、在手訂單 125 億美元（+73%）。定價面這一年轉弱：全年價格貢獻由 1.5 降到約 1 個百分點、價格對通膨為逆風、有機增量槓桿由 25% 以上降到 20% 出頭；但商用 HVAC 仍是正價格（第三季法說 CFO）。兩者相抵判為穩定；同業份額數字事實表未涵蓋","competitor_notes":[{"name":"CARR","strategy_note":"近 12 個月毛利率 24.6%、營益率 8.1%、FCF 利潤率 10.4%，三項都明顯低於 TT；從數字看，對 TT 的定價不構成壓力"},{"name":"JCI","strategy_note":"毛利率 36.7% 略高於 TT，但營益率 14.5%、FCF 利潤率 6.6% 低很多（期間至 2026-06），獲利轉成現金的能力弱於 TT"},{"name":"LII","strategy_note":"營益率 19.9% 高於 TT 的 17.9%，FCF 利潤率 15.3% 略低；業務組合差異事實表未涵蓋，營益率落後不足以判定 TT 護城河較弱"}],"spread_notes":{"basis":"近 12 個月營益率代理（同業 ROIC 事實表未涵蓋）","vs_peers":"對 LII 約 −2.0 個百分點、對 JCI +3.5、對 CARR +9.9","fcf":"FCF 利潤率四家最高"},"peer_na_reason":"同業 ROIC 與份額事實表未涵蓋，報酬差距方向無法驗證","threats":[{"level":"🔴","text":"資料中心散熱價值往晶片端位移：晶片商稱新一代系統可用熱水冷卻、不需冷水機，多家 HVAC 股價應聲下跌；10-K 承認非傳統業者的顛覆性技術；TT 不做冷板（第二季法說 CEO）","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"產業整併與非傳統新進入者可能帶來價格壓力；資料中心有純冷卻廠商造成價格壓力（次要來源），TT 以收購 Stellar、LiquidStack 回應","p":20,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"level":"🟡","text":"短週期業務的實現價格偏弱：住宅經銷通路量增時獎勵增加、運輸大車隊組合為負價格、亞太約 −1 個百分點（中國）","p":40,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×高周轉（推估：資本支出約營收 2%、自由現金流約等於淨利；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（建物住戶、資料中心營運者）、決策者（業主、設計顧問、超大規模客戶）、付款者（業主）三個角色都成立；建物約 30% 能源被浪費（第三季法說 CEO），效率是需要不是想要；服務約占營收三分之一、低雙位數複合成長；14 個垂直市場有 11 個成長。資料中心的急迫性不等於持久性，核心垂直與服務才是基礎值"},{"item":"決策層級","level":"🟡","text":"替代性在專案設計與系統規格層決定：TT 被邀入超大規模客戶的參考設計，Applied 已安裝基礎帶出服務；但超大規模客戶多簽主採購協議或長期產能承諾（第二季法說 CEO），大單議價力在客戶端；續約率與漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"上游風扇、線圈、熱交換器產能吃緊，且有單一或有限來源採購，TT 以收購 Cancoil（TT 占其量約 40%）收回一段價值；下游由晶片商主導散熱架構，若改用熱水冷卻，冷水機的價值份額會被壓縮；今年價格對通膨為逆風，代表價值鏈分配短期往供應商傾斜"},{"item":"社會容忍度","level":"🟡","text":"HVAC 屬必需品，住宅端持續漲價（2026-09 產業報導）；2026 年 3 月起的 HVAC 設備價格壟斷民事集體訴訟（密西根東區聯邦法院，5 月合併）主張業者借疫情與法規變動協調漲價，TT 為被告之一，未經法院認定。社會對漲價的容忍度已出現法律面挑戰，實際訂價上限可能低於經濟上限"}],"roiic":"事實表未涵蓋投入資本、折舊攤提、營運資金變動與收購淨額，增量報酬無法用公式算；以淨利與自由現金流代估，FY2023–FY2025 有機淨再投資接近零（累計 FCF 76.8 億高於累計淨利 75.1 億），增量營業利益主要來自低資本密度下的量增與利潤率擴張（營益率 15.1%→18.6%）","reinvest_rate":"有機約 0%（代估）；2026 年收購 Stellar 約 5.5 億美元（不含取得現金）加上其他未揭露金額，含收購的再投資率事實表未涵蓋","endo_ceiling":10.1,"formula_note":"當期 ROIC 的投入資本口徑事實表未涵蓋，次要來源（TIKR，2026-08）稱 ROIC 28%，屬分析師說法。增量 ROIC×再投資率的公式因有機淨再投資接近零而失效，改以 FY2022–FY2025 營收年複合（159.9 億→213.2 億美元，(213.2÷159.9)^(1/3)−1＝10.1%）為內生上界代理"}}}},"q3_growth":{"verdict":"五年後跑道仍寬（🟢）：核心建築汰換與服務是底，資料中心熱管理與歐洲供熱電氣化是有來源的第二曲線；但其中一條第二曲線正被晶片端架構挑戰。","reasoning":"成長來源：以量為主（第三季價格約 +0.5 個百分點，有機 16% 幾乎全靠量），併購約 2 個百分點，淨回購讓稀釋股數 3 年年減約 1.4%。三年共識 EPS 年複合：FY2025 GAAP 12.98 → FY2028E 20.33，(20.33÷12.98)^(1/3)−1＝16.1%（Koyfin 快照，家數事實表未涵蓋；基期為 GAAP、共識為調整後，口徑小有落差）。內生上界 10.1%（見護城河段的再投資推導）。缺口 6.0 個百分點可以歸因：利潤率擴張約 3–4 個百分點（25% 增量槓桿對 18% 基期營益率，營收每成長 10%，營業利益約成長 14%）、淨回購約 1.4 個百分點、併購約 1 個百分點，不屬無法歸因。營收共識 FY2026E 241.4 億（+13.2%）、FY2027E 265.3 億（+9.9%），成長在 2027 年放緩。營運槓桿：第三季營收 +18%、GAAP 營業利益 +15%，差 3 個百分點，在邊界上、未超過。跑道：HVAC 屬汰換型需求，滲透率概念不適用，事實表也未涵蓋；第二曲線有來源：ABI 預估資料中心液冷 2030 年達 35 億美元（年複合 20%），COO 說歐洲供熱電氣化在成長，Stellar 規劃兩年內做到營收 10 億美元。衰退訊號亮 2 項（毛利率年減屬推估、EPS 與營收增速差 5.3 個百分點在邊界），長期成長性判為中。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_bookings","f_kpi7_backlog","f_kpi2_gaap","f_kpi0_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（第三季價格約 +0.5 個百分點）＋併購約 2 個百分點＋淨回購（稀釋股數 3 年年減約 1.4%）","runway_years":"≥10（汰換需求與服務；滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC×再投資率在 TT 失效：有機淨再投資接近零（FY2023–FY2025 累計 FCF 高於累計淨利），公式會得到接近零的上界，不合理；改以 FY2022–FY2025 營收年複合 10.1%（159.9 億→213.2 億美元）作為不靠外部資本的成長代理，利潤率擴張、回購、併購另列缺口歸因","segments":[{"item":"美洲（Q3 2026）","value":"營收 5,647.9 百萬（+21%），占全公司約 84%；訂單 5,681.4 百萬（+18%），訂單/營收比 101%；商用 HVAC 在手訂單約 +80%"},{"item":"歐中非（Q3 2026）","value":"營收 755.8 百萬（+1%）；訂單 1,109.4 百萬（+40%），訂單/營收比 147%；GAAP 營業利益率 17.2%（−240bp，八成以上來自中東）"},{"item":"亞太（Q3 2026）","value":"營收 356.0 百萬（+8%）；訂單 457.1 百萬（+22%）；中國約占亞太三分之一，價格約 −1 個百分點"},{"item":"服務（全公司）","value":"約占營收三分之一，2020 年以來低雙位數複合成長；在手訂單只含設備、不含服務"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"近 12 個月毛利率 34.99% 低於 FY2025 的 36.16%，等於 2026 前三季合計年減；單季毛利率事實表未涵蓋，屬推估亮燈"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"份額數字事實表未涵蓋；訂單 +21%，未見流失跡象"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"住宅今年兩次漲價後，第三季營收仍 +20%"},{"signal":"EPS 年複合高於營收年複合逾 5 個百分點","lit":true,"note":"FY2025–FY2027 共識 EPS 年複合 16.8%、營收 11.5%，差 5.3 個百分點，邊界亮燈；基期用 GAAP EPS，口徑略有落差"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"note":"FY2024 1.08、FY2025 0.96"},{"signal":"SBC÷營收高於 5% 且上升","lit":false,"note":"SBC 事實表未涵蓋；稀釋股數 3 年年減約 1.4%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"晶片商熱水冷卻說法是警訊，但 ABI 預估兩段式冷卻持續，尚無數據"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"資本支出約營收 2%，FCF 利潤率 16.4%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"Applied 產能 3 年擴 4 倍（第二季法說 CEO），德州新廠正在試產"}],"trap_rating":"🟡（亮燈 2 項，其一在邊界）"}}},"q4_capital":{"verdict":"現金轉換強，回購與股息持續，併購報酬尚未證實。","reasoning":"現金轉換：FY2024 FCF÷淨利 1.08、FY2025 0.96；2026 年初至今自由現金流 28.3 億美元（年增約 60%），管理層預期全年高於淨利（第三季法說 CEO）。現金去向（2026）：資本支出約營收 2%（由先前 2–3% 下修）；股息上調 12%，以殖利率 0.768% 乘市值約 897 億推算，一年約 6.9 億；回購年初至今約 14 億（第二季時為 8.4 億）；併購包括 Stellar（約 5.5 億，不含取得現金 1.85 億）、LiquidStack 剩餘股權、Kieback&Peter 49%、CSTK 與 Cancoil（金額未揭露）；全年部署逾 34 億，高於原先 28–33 億的區間。資產負債：淨負債約 29.9 億美元，不到 FY2025 營業利益約 39.7 億的 1 倍。SBC 占營收事實表未涵蓋；以淨利÷稀釋 EPS 推算，稀釋股數 FY2022 約 2.348 億、FY2025 約 2.249 億，判斷日 2.189 億，淨稀釋為負。計分：併購已實現的增量報酬未證（Stellar 今年 EPS 持平）；回購以盈餘殖利率約 3.7%（15.28÷410）計，門檻所需的 10 年期殖利率事實表未涵蓋；淨稀釋通過。","fact_refs":["f_kpi3_fcf_9_q3","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Stellar 對價約 5.534 億美元（不含取得現金 1.854 億），2026 營收約 5 億、EPS 持平，兩年後目標營收 10 億、EBITDA 利潤率十幾%；已實現增量報酬與資金成本事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"年初至今回購約 14 億美元，回購均價事實表未涵蓋；以判斷日股價計，盈餘殖利率約 3.7%，門檻＝10 年期殖利率＋2 個百分點，10 年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數 FY2022 約 2.348 億→FY2025 約 2.249 億（淨利÷稀釋 EPS 推算），年減約 1.4%；判斷日 2.189 億"}],"grade":null},"governance":{"capital_returns":{"expanded":false,"reason":"第三季營收成長 18% 中有機 16%、併購約 2 個百分點，成長不靠併購撐；近三年現金去向四分的完整數字事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價 410 美元要求 2027–2028 年 EPS 年增約 15% 兌現、倍數守在 23–27 倍。需求面我相信，利潤率立刻回到 25% 增量槓桿我只信一半，估值判為合理、不便宜。","reasoning":"倍數：當年度（FY2026E 15.28）26.83 倍、FY2027E（17.7）23.2 倍、trailing 28.49 倍；PEG＝26.83÷16.1＝1.67，落在合理區。歷史位置：trailing 本益比在近 4 個年度端點的分位是 53，P/S 3.86 倍分位 74、EV/S 3.99 倍分位 71；五年高低區間事實表未涵蓋，五年分位留空。與前份相比：股價由 440.28 跌到 410（−6.9%），同期 FY2026 共識由 14.91 上修到 15.28（+2.5%），前瞻本益比由約 29.5 倍降到 26.8 倍。短期上檔：FY2027E 基準 EPS 17.4×25 倍＝435 美元（+6.1%）；中期（三年）：FY2029E 21.8×24 倍＝523 美元（+27.6%）。賣方目標價（約 2026-08）均值約 520–530 美元、區間 444–614，各站不一致，且早於第三季財報，不拿來當錨。同業本益比事實表未涵蓋，不做跨公司倍數對照。分母：FY2026 EPS 含第三季約 0.10 美元的稅率時點效益，第四季抵銷、全年稅率 19% 不變，分母沒有爭議。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2026E 共識 15.28）＋PEG，trailing P/E 28.49 倍為對照","tier":"品質工業複利","peers":{"expanded":false,"reason":"同業本益比（CARR、JCI、LII）事實表未涵蓋，只有利潤率對照，不跨口徑硬比"},"fwd_pe":26.83,"peg":1.67,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Fwd P/E 26.83 倍、PEG 約 1.67（26.83÷三年 EPS 年複合 16.1%），落在合理區間；trailing 本益比在近 4 個年度端點的中位附近（分位 53）；P/S、EV/S 分位 74／71 偏高；五年分位事實表未涵蓋","upside_short_pct":6.1,"upside_mid_pct":27.6,"denominator_disputed":false,"denominator_note":"FY2026 EPS 含第三季約 0.10 美元稅率時點效益，第四季抵銷，全年稅率維持 19%，分母不受影響"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：資料中心大單在 2027 年斷層，以及價格對通膨的逆風不是時點問題，而是定價權鬆動；價值陷阱風險中（🟡）。","reasoning":"三個視角的反證見反證紀錄：論點失敗（資料中心散熱架構轉向，加上超大規模客戶進入消化期，五年後可能腰斬）、論點成功但股東經濟變差（營收長但利潤率停滯）、價格已反映太多（大部分反駁）。價格面：26 週跌 15.33%，RSI 31.4，股價 410 跌破 104 週均線 418.19，但仍在 250 週均線 298.0 之上。衰退訊號亮 2 項，判為中。歷史最大回撤與空方最強數字事實表未涵蓋，回撤範圍以情境推導（−30% 到 −45%）。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w104","f_ma_w250","f_kpi1_non_gaap","f_peer_tt_gross_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"需求仍強、利潤率先轉弱的早期警訊"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":15.28,"pe":26.83,"basis":"FY2026E 共識調整後持續營運 EPS 15.28（公司指引 15.20–15.30），起點本益比 26.83 倍；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[18.3,21.4,24.4,27.4,30.4],"base":[17.4,19.7,21.8,23.6,25.3],"bear":[15.6,14.4,14.0,15.0,16.2]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.77,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-45,"hi":-30,"basis":"起點 410 美元。淺端 −30%：2027 年超大規模客戶放慢的消息先出，EPS 仍在 15.6 美元附近，倍數由 26.8 倍壓到 18–19 倍（約 287–296 美元）。深端 −45%：Bear 谷底 FY2029E EPS 14.0 美元×16 倍＝224 美元，對應訂單斷層與反壟斷不利和解同時發生。Bear 終點 −29% 落在範圍內；歷史回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"資料中心與核心垂直訂單延續，2027 年起價格高於通膨、增量槓桿 25% 以上，FY2027–FY2028 略高於共識，之後年增 12–14%；終端 30 倍，約為現值 trailing 28.5 倍、略高於近 4 個年度端點中位；同業本益比事實表未涵蓋","base":"FY2027–FY2028 略低於共識（17.7／20.33），反映價格與供應鏈逆風，之後年增 8–10%；終端 24 倍，較現值 26.8 倍壓縮；EPS 為每股口徑、已含回購，淨回購殖利率不另計","bear":"2027 年超大規模客戶資本支出進入消化、資料中心大單延後，住宅隨利率轉弱、運輸復甦落空，FY2028–FY2029 EPS 跌到 14.0–14.4，FY2031 只回到 16.2；終端 18 倍，對應成長降到 5–10% 時的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"晶片商執行長說新一代 AI 系統可用熱水冷卻、不需冷水機，多家 HVAC 股價應聲下跌；10-K 承認非傳統業者的顛覆性技術；TT 追蹤的 1,700 個大型專案逾九成是資料中心，Stellar 幾乎全為資料中心；資料中心專案可能因場址與電力併網而位移","assumption":"資料中心維持液冷加氣冷的兩段式架構（ABI：液冷占資料中心 HVAC 15%），冷水機仍在架構內；2027 年超大規模客戶資本支出不出現消化","consequence":"Applied 訂單斷層、在手訂單連兩季淨減，FY2028–FY2029 EPS 跌到 14.0–14.4 美元、倍數降到 16–18 倍，股價約 224–260 美元（−37% 到 −45%）；若再疊上反壟斷不利和解，五年後腰斬","ruling":"部分採納：Bear 機率提高到 30%，並把在手訂單淨減設為唯一致命點（與唯一致命點部分重疊，已回補）。不全採納，因為第二季法說稱市場朝風冷冰水機傾斜，第三季又追加參考設計與 CDU 訂單，替代目前仍停在說法","watch":"季末在手訂單、全球 Applied 訂單年增率、法說對冷水機在新架構中用量的描述","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#4","competitive_share_entrants#0"],"fact_refs":["f_kpi7_backlog","f_kpi5_bookings"]},{"view":"論點成功但股東經濟變差","evidence":"需求成功但成本吃掉利潤：全年價格約 1 個百分點、價格對通膨為逆風，所有成本類別的通膨都比 3、6、9 個月前高（第三季法說 CFO）；風扇、線圈、熱交換器吃緊到 2027 上半年；UFLPA 名單造成產線缺料與重工；2025 關稅成本逾 1.4 億美元、2026 再多約 5,000 萬；部分零件單一或有限來源；收購 Stellar 今年 EPS 持平，併購使報告與有機增量槓桿相差約 500bp","assumption":"這些都是一到兩季的時點問題，2027 年回到價格高於通膨 0.2–0.3 個百分點與 25% 增量槓桿","consequence":"營收照長但利潤率停滯，EPS 年增只剩營收增速，終端倍數向 20 倍靠，基準年報酬由約 9% 降到 5% 上下","ruling":"部分採納：毛利率年減已出現，價值陷阱判讀升為中；以第四季槓桿與 2027 價格指引作為驗證期限，沒過就停止加碼","watch":"第四季 2026 有機增量槓桿、2027 指引價格對通膨、單季調整後營益率年變化","evidence_refs":["geo_supply_chain#1","geo_supply_chain#3","reg_tariff_export#0","reg_tariff_export#3"],"fact_refs":["f_kpi1_non_gaap","f_peer_tt_gross_margin_pct","f_kpi8_2026"]},{"view":"價格已反映太多","evidence":"判斷日為當年度 EPS 26.83 倍、trailing 28.49 倍；P/S 3.86 倍、EV/S 3.99 倍在近 4 個年度端點的分位為 74／71；FY2027–FY2028 共識隱含 EPS 年增約 15%","assumption":"2027–2028 年 EPS 成長照共識兌現","consequence":"若 2027 指引只給 8–10% 成長，FY2027 EPS 約 16.5–16.8，倍數向 21–22 倍靠，股價約 350–370 美元（−10% 到 −15%）","ruling":"大部分反駁：股價 26 週跌 15%，前瞻本益比由前份約 29.5 倍降到 26.8 倍，近 3 個月 FY2026 共識上修 2.5%；基準情境已假設倍數壓縮到 24 倍，年報酬仍約 9%。但安全邊際不大，不支持一次加滿","watch":"2027 年全年指引、前瞻本益比、FY2027 共識修正方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 440.28 → 本次 410.0（-6.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=440.28","side_b":"本次 price_at_dd=410.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份角色：均線 ✅→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 440.28 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 440.28 美元：Bull 價 910、Bear 價 285，五年期望值 +49.0%，基準年化 9.0%，不對稱比 4.2","side_b":"本次情境、股價仍用 440.28 美元：Bull 價 912、Bear 價 291.6，五年期望值 +33.7%，基準年化 6.6%，不對稱比 2.64","ruling":"先換情境、股價不動：五年期望值少 15.3 個百分點，基準年化少 2.4 個百分點。不對稱比由 4.2 變為 2.64。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 440.28 美元：五年期望值 +33.7%，基準年化 6.6%，不對稱比 2.64","side_b":"本次情境、股價 410 美元：五年期望值 +43.6%，基準年化 8.2%，不對稱比 3.53","ruling":"再換股價、情境不動：起點價下跌 6.9%，五年期望值多 9.9 個百分點，基準年化多 1.5 個百分點，不對稱比由 2.64 升到 3.53。合計五年期望值比前份少 5.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"prior_field":null,"side_a":"需求面：新聞稿、法說、外部次要來源都指向訂單與在手訂單創高，自由現金流強","side_b":"成本面：法說與 10-K 都承認供應鏈、關稅、通膨壓力","ruling":"兩者同時成立、不互相否定：需求是長期變數，成本是一到兩季的變數","evidence_level":"高（公司新聞稿、法說、10-K）","settle_metric":"在手訂單與調整後營益率","if_then":[],"evidence_refs":["end_markets#0","reg_tariff_export#1"]},{"axis":"前份漂移：股價下跌，結論未翻面","cause":"價格變動","prior_field":["signal","val","moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct"],"side_a":"前份（2026-07-31，股價 440.28）：進場；品質與估值綜合訊號高、估值中性、護城河方向穩定、五年後跑道寬、品質複利成長、未設循環位置；最大回撤 −48%","side_b":"本次（股價 410，−6.9%）：綜合訊號、估值結論、護城河方向、跑道、公司類型都不變，循環位置仍不適用；前瞻本益比由約 29.5 倍降到 26.8 倍，是股價下跌加上共識上修 2.5% 的結果，尚未跌到便宜區；回撤範圍改為 −30% 到 −45%，起點較低，深端收窄；裁決與角色由決策輸入重算，均線轉弱是主因之一","ruling":"價格變動造成的漂移，不改基本面結論","evidence_level":"高（股價與共識快照）","settle_metric":"前瞻本益比、FY2027 共識 EPS","if_then":["若股價跌到 370 美元以下而在手訂單未淨減 → 分批反買，加碼一階","若股價反彈到 470 美元以上但第四季槓桿未回到 25% → 不追"],"evidence_refs":[]},{"axis":"價值陷阱判讀由低升為中","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低（🟢）","side_b":"本次：中（🟡）。近 12 個月毛利率 34.99%，低於 FY2025 的 36.16%，2026 前三季合計年減；全年價格由 1.5 降到約 1 個百分點、價格對通膨轉為逆風、有機增量槓桿由 25% 以上降到 20% 出頭（第三季法說 CFO）；三年共識 EPS 增速比營收快 5.3 個百分點（邊界）","ruling":"採納：衰退訊號由 0 項亮到 2 項；第四季槓桿若回到 25% 且 2027 價格高於通膨，回降為低","evidence_level":"中（毛利率年減屬推估，單季數字事實表未涵蓋）","settle_metric":"第四季 2026 有機增量槓桿、2027 指引價格對通膨、單季毛利率年變化","if_then":["若第四季有機增量槓桿 ≥25% → 價值陷阱判讀回降為低","若 2027 上半年調整後營益率仍年減 → 停止加碼"],"evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"]},{"axis":"加碼條件變動（前份條件已觸發）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已持有續抱＋首階加碼 1/3；再加碼＝$415 以下，或 FY26 有機增量槓桿回到 25%＋","side_b":"第四季2026有機增量槓桿≥25%且2027指引價格高於通膨→補足加碼；或股價≤370美元且在手訂單未淨減→加碼一階","ruling":"前份 415 美元以下的加碼條件已在判斷日（410 美元）觸發；另一條件「全年有機增量槓桿 25%」已被第三季下修到 20% 出頭所否定。本次加碼一階分兩半：先執行一半，另一半綁第四季槓桿；價格錨下移到 370 美元（約 FY2026E 24 倍、FY2027E 共識 21 倍）","evidence_level":"高（股價與第三季法說 CFO 原話）","settle_metric":"第四季 2026 有機增量槓桿","if_then":["若第四季有機增量槓桿 ≥25% 且 2027 價格高於通膨 → 補足剩餘一半加碼","若第四季有機增量槓桿 <20% → 停止加碼，剩餘一半取消"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"情境機率變動","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份 Bull 27%／Bear 25%","side_b":"本次 Bull 25%／Base 45%／Bear 30%","ruling":"三年共識 EPS 年複合 16.1% 高於內生上界 10.1%，依規則 Bear 機率不低於 30%；第三季美洲訂單減速與資料中心架構的說法是方向一致的新證據，但這次調整的主因是方法","evidence_level":"中","settle_metric":"滾動四季訂單/營收比、在手訂單","if_then":["若 2027 上半年滾動四季訂單/營收比 ≥105% 且在手訂單續創高 → 下次判斷 Bear 機率可回到 25%","若在手訂單單季淨減 → Bear 機率提高到 35% 以上並停止加碼"],"evidence_refs":[]},{"axis":"唯一致命點新設（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing：未設（空白）","side_b":"本次 Single Thing：資料中心大單在 2027 年取消或大規模延後，使企業在手訂單連續兩季較前季淨減少","ruling":"前份未設屬缺漏；資料中心訂單同時決定 EPS 路徑與倍數，是最大的單一敏感度項，觸發時減碼至原部位一半","evidence_level":"中","settle_metric":"季末在手訂單","if_then":["若在手訂單連續兩季淨減 → 減碼至原部位一半","若 2027 年各季在手訂單持續創高 → 維持部位"],"evidence_refs":["substitute_technology#1","end_markets#4"]},{"axis":"停損指標新設（減碼與清倉條件）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份停損指標：未設（空白）","side_b":"在手訂單連兩季淨減 → 減碼至一半；FY2027 有機增量槓桿 <20% 且價格低於通膨 → 減碼一階；反壟斷集體認證加不利和解 → 減碼至半倉，司法部刑事介入 → 清倉；次年及以後在手訂單跌破 60 億美元 → 停止加碼","ruling":"補上可觀察的減碼與清倉條件，每條附資料來源","evidence_level":"中","settle_metric":"見各條指標","if_then":["若任一條減碼條件成立 → 依該條動作執行，不等下次判斷"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"訂單減速與管理層「不擔心」","cause":"新證據","prior_field":null,"side_a":"第三季美洲訂單 5,681 百萬、訂單/營收比 101%，較第二季兩位數減少（UBS 分析師提問）；企業有機訂單成長由第二季 +37% 降到 +20%","side_b":"CEO：大單本來就不規則，追蹤的大型專案由 1,400 增至 1,700 個（逾九成資料中心），在手訂單 125 億美元，其中逾 80 億排在 2027 年及以後；歐中非排除中東訂單 +50%、亞洲排除中國 +70%","ruling":"可調和（程度差異）：採信在手訂單的結構，但一季訂單不足以否定減速；以滾動四季訂單/營收比與在手訂單作為裁決指標","evidence_level":"中","settle_metric":"滾動四季企業訂單/營收比、季末在手訂單","if_then":["若 2027 上半年滾動四季訂單/營收比 <100% → 停止加碼","若第四季訂單/營收比 ≥105% 且在手訂單再創高 → 補足剩餘一半加碼"],"evidence_refs":["supply_demand_durability#0","end_markets#1","end_markets#4"]},{"axis":"第二季的利潤率說法與第三季結果","cause":"新證據","prior_field":null,"side_a":"2026-07-30 第二季法說 CFO Chris Kuehn：預期第三季利潤率擴張、第四季目標擴張逾 1 個百分點，長期增量槓桿 25% 以上","side_b":"第三季調整後營業利益率 20.2%，年減 40bp；全年價格由 1.5 降到約 1 個百分點，有機增量槓桿下修到 20% 出頭；營收指引上調但 EPS 指引不動；第三季調整後 EPS 4.86 美元，扣掉約 0.10 美元稅率時點效益約 4.76，略高於第二季給的約 4.70","ruling":"管理層把落差歸因於短週期業務的時點與組合，不採信也不否定，標為未證、監測。驗證期限：第四季 2026 有機增量槓桿 <25%，且 2027 指引價格仍低於通膨，即視為歸因不成立，信心降一級並停止加碼","evidence_level":"高（公司新聞稿與法說原話）","settle_metric":"第四季 2026 有機增量槓桿；2027 指引價格對通膨","if_then":["若第四季有機增量槓桿 ≥25% → 歸因成立，補足加碼","若第四季 <20% 且 2027 價格低於通膨 → 停止加碼，長期信心維持中"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"Stellar 獲利貢獻改口","cause":"新證據","prior_field":null,"side_a":"第一季時的說法為 EPS 略有加分","side_b":"第二季（2026-07-30）改為全年持平；第三季（2026-10-29）CFO 維持營收約 5 億、EPS 持平，兩年後營收 10 億、EBITDA 利潤率十幾%","ruling":"可調和：屬投資前置（佛州與德州新廠），但收購報酬尚未實現，資本配置的併購項目不判通過","evidence_level":"中","settle_metric":"2027 年 Stellar EPS 貢獻","if_then":["若 2027 指引 Stellar 仍為 EPS 持平或負 → 不再接受新的資料中心大型收購作為加分理由"],"evidence_refs":["major_events#3","ma_merger#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面：10-K 列出新進入者與非傳統競爭者；資料中心有純冷卻廠商帶來價格壓力；晶片商說新系統可用熱水冷卻、不需冷水機","side_b":"結構面：在手訂單 125 億美元（+73%）、14 個垂直市場有 11 個成長、運輸景氣轉入上行。其他結構變數：部分 HVAC 設備 232 關稅自 25% 降到 15%（至 2027 年底）、反壟斷集體訴訟待決、北美 21 座廠有 20 座在美國","ruling":"雙向拉鋸：需求結構轉好有公司數字支撐，競爭與替代技術的威脅仍停在說法與早期跡象，未見份額流失數據","evidence_level":"中","settle_metric":"全球 Applied 訂單年增率、同業利潤率差距","if_then":["若 Applied 訂單連 2 季年減且同業營益率差距收窄 → 改判競爭惡化中，減碼一階"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#1","reg_tariff_export#2","regulatory_antitrust#2","geo_supply_chain#0"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣出論證：今年價格追不上通膨，增量槓桿兩度下修，供應鏈壓力延續到 2027 上半年；在手訂單的成長集中在資料中心，若 2027 年超大規模客戶放慢，FY2027 共識 17.7 有下修空間；股價已跌破 104 週均線，26 週跌 15%","side_b":"續抱論證：當年度 26.83 倍、FY2027E 23.2 倍，對應兩年約 15% 的共識 EPS 成長，且有逾 80 億美元排在 2027 年後的在手訂單支撐；年初至今自由現金流 28.3 億美元、全年高於淨利；基準情境倍數壓縮到 24 倍，年報酬仍約 9%","ruling":"續抱並分批加碼，但一半加碼綁第四季槓桿驗證；賣出論證的關鍵在 2027 指引，現在無法證實","evidence_level":"中","settle_metric":"2027 全年指引（EPS 成長與價格對通膨）","if_then":["若第四季有機增量槓桿 <20% 且 2027 EPS 指引成長 <8% → 減碼一階至原部位四分之三","若 2027 指引 EPS 成長 ≥12% 且價格高於通膨 → 補足加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第四季 2026 有機增量槓桿是否回到 25% 以上（管理層說會超過目標區間）","type":"假設驗證","maps_to":"H2","metric":"有機增量槓桿（單季）","threshold":"≥25% 達標；<20% 證偽","action":"達標 → 執行剩餘一半加碼；<20% → 停止加碼、長期信心維持中","source_freq":"季度法說","date":"2027-01","evidence_refs":["capital_markets_pricing#0"]},{"n":2,"text":"2027 年指引中的價格對通膨","type":"假設驗證","maps_to":"H2","metric":"2027 指引價格減通膨","threshold":"<0，即「今年只是時點與組合」的說法不成立","action":"停止加碼","source_freq":"年度指引","date":"2027-01","evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"]},{"n":3,"text":"在手訂單連續兩季較前季淨減少","type":"Single Thing","maps_to":"Single Thing","metric":"季末在手訂單","threshold":"連續兩季較前季減少","action":"減碼至原部位一半，倉位上限降到 3%","source_freq":"季度新聞稿","date":null,"evidence_refs":["substitute_technology#1","end_markets#4"]},{"n":4,"text":"企業訂單/營收比轉弱","type":"風險","maps_to":"R1","metric":"滾動四季企業訂單/營收比","threshold":"<100%，或單季 <95%","action":"停止加碼","source_freq":"季度新聞稿","date":null,"evidence_refs":["end_markets#4"]},{"n":5,"text":"HVAC 設備反壟斷集體訴訟進度","type":"風險","maps_to":"R4","metric":"集體認證、和解、司法部動向","threshold":"集體認證通過且不利和解；或司法部刑事介入","action":"前者減碼至半倉；後者清倉","source_freq":"法院案卷、10-Q","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":6,"text":"關稅與通膨吸收失敗","type":"風險","maps_to":"R2","metric":"調整後營業利益率年變化","threshold":"連 2 季年減 ≥50bp","action":"停止加碼","source_freq":"季度新聞稿","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#1","geo_supply_chain#3"]},{"n":7,"text":"資料中心冷卻架構轉向不用冷水機","type":"風險","maps_to":"R3","metric":"全球 Applied 訂單年增率","threshold":"連 2 季年減，且法說承認冷水機在新架構中的用量下降","action":"減碼一階","source_freq":"季度法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#0"]},{"n":8,"text":"價格回落到合理偏低區","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤370 美元（約 FY2026E 24 倍、FY2027E 共識 21 倍）且在手訂單未淨減","action":"分批反買，加碼一階","source_freq":"每日","date":null,"evidence_refs":[]},{"n":9,"text":"區域逆風在比較基期轉易後仍未改善","type":"風險","maps_to":"R5","metric":"歐中非 GAAP 營業利益率","threshold":"2027 上半年仍年減","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-07","evidence_refs":["geo_supply_chain#2"]},{"n":10,"text":"第四季財報與 2027 指引公布後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-02-01","evidence_refs":[]}],"kill_metrics":[{"metric":"季末在手訂單","bear_threshold":"連續兩季較前季淨減少 → 減碼至原部位一半","window":"2027 年各季財報","source":"公司季度新聞稿","last_status":"ok"},{"metric":"有機增量槓桿（全年）","bear_threshold":"FY2027 低於 20% 且價格低於通膨 → 減碼一階","window":"FY2027，2028 年 1 月公布","source":"公司財報與法說","last_status":"warning"},{"metric":"HVAC 反壟斷集體訴訟進度","bear_threshold":"集體認證＋不利和解 → 減碼至半倉；司法部刑事介入 → 清倉","window":"2026–2028","source":"密西根東區聯邦法院案卷、10-K／10-Q","last_status":"warning"},{"metric":"排在次年及以後的在手訂單","bear_threshold":"由逾 80 億美元降到 60 億美元以下 → 停止加碼","window":"2027 年各季","source":"季度法說 CFO 揭露","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"第四季2026有機增量槓桿≥25%且2027指引價格高於通膨→補足加碼；或股價≤370美元且在手訂單未淨減→加碼一階","exec_line":"已持有續抱；前份 415 美元的加碼條件已觸發，本次加碼一階分兩半：先執行一半，另一半等第四季有機增量槓桿 ≥25%；在手訂單連兩季淨減則減碼至原部位一半"}},"decision_inputs":{"signal":"A","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第三季美洲訂單減速與資料中心不用冷水機的說法當成需求見頂；但在手訂單 125 億美元中逾 80 億排在 2027 年及以後，歐中非排除中東訂單 +50%、亞洲排除中國 +70%，需求分布比資料中心單一主題廣。市場錯在把一季的專案時點當成趨勢","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第三季美洲訂單減速與資料中心不用冷水機的說法當成需求見頂；但在手訂單 125 億美元中逾 80 億排在 2027 年及以後，歐中非排除中東訂單 +50%、亞洲排除中國 +70%，需求分布比資料中心單一主題廣。市場錯在把一季的專案時點當成趨勢"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='→', week26=-15.33, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"商用 HVAC 需求廣泛、不只資料中心：在手訂單轉成 2027 年營收，帶動 FY2027 有機營收成長至少高個位數","2y":"FY2027 有機營收成長 ≥8%，在手訂單維持 100 億美元以上","5y":null,"10y":null,"threshold":"滾動四季企業訂單/營收比 ≥100%；季末排在次年及以後的在手訂單 ≥80 億美元","source":"公司季度新聞稿（訂單、在手訂單）與法說（垂直市場成長家數，目前 14 個中 11 個）","drift_rule":"滾動四季訂單相對門檻連 2 季偏低 ≥5% 為削弱，連 3 季偏低 ≥10% 或在手訂單較前季淨減為反轉"},{"id":"H2","text":"定價權與增量槓桿回到長期框架：2027 年價格高於通膨 0.2–0.3 個百分點、有機增量槓桿 ≥25%，今年的落差只是短週期業務的時點與組合","2y":"FY2027 有機增量槓桿 ≥25%，價格高於通膨 0.2–0.3 個百分點","5y":null,"10y":null,"threshold":"第四季 2026 單季有機增量槓桿 ≥25%；FY2027 全年 ≥25%","source":"第四季法說（2027 年 1 月）與 2027 全年指引；季度新聞稿利潤率","drift_rule":"連 2 季有機增量槓桿低於 20% 為削弱；FY2027 全年低於 20% 且價格仍低於通膨為反轉"},{"id":"H3","text":"服務與已安裝基礎複利：服務約占營收三分之一，維持年增 ≥8%，自由現金流長期不低於淨利","2y":null,"5y":"服務年增 ≥8%；滾動兩年 FCF÷淨利 ≥0.9","10y":null,"threshold":"服務有機成長 ≥8%／年；滾動兩年 FCF÷淨利 ≥0.9","source":"法說的服務成長描述、年度財報現金流量表","drift_rule":"連 4 季服務成長低於 8% 為削弱、連 6 季低於 5% 為反轉；FCF÷淨利跨 2 個年度低於 0.9 為削弱"}],"R":[{"id":"R1","text":"超大規模客戶資本支出在 2027 年進入消化期、資料中心大單因場址與電力併網延後，同時商用建築與住宅隨利率轉弱","h_ref":"H1","clock":"🔥","threshold":"滾動四季企業訂單/營收比 <100%，或排在次年及以後的在手訂單由逾 80 億美元降到 60 億以下","evidence_refs":["end_markets#4","supply_demand_durability#0"]},{"id":"R2","text":"價格對通膨持續逆風與供應鏈瓶頸：全年價格由 1.5 降到約 1 個百分點、有機增量槓桿 20% 出頭；風扇、線圈、熱交換器吃緊到 2027 上半年；UFLPA 名單造成缺料重工；2025 關稅成本逾 1.4 億美元、2026 再增約 5,000 萬；部分零件為單一或有限來源","h_ref":"H2","clock":"⚡","threshold":"第四季 2026 有機增量槓桿 <25% 且 2027 指引價格仍低於通膨；或調整後營業利益率連 2 季年減 ≥50bp","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#1","geo_supply_chain#3"]},{"id":"R3","text":"資料中心散熱價值往晶片端位移：晶片商稱新系統可用熱水冷卻、不需冷水機；10-K 承認非傳統業者的顛覆性技術；TT 不做冷板（第二季法說 CEO）","h_ref":"H1","clock":"🐢","threshold":"全球 Applied 訂單連 2 季年減，且法說承認冷水機在新資料中心架構中的用量下降","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#0","competitive_share_entrants#2"]},{"id":"R4","text":"HVAC 設備價格壟斷民事集體訴訟：2026-03-20 於密西根東區聯邦法院提起，被告含 TT，主張違反休曼法第 1 條，2026-05-15 合併；未經法院認定，事實表未見司法部刑事立案；受影響營收與和解金額事實表未涵蓋","h_ref":"H2","clock":"🐢","threshold":"集體認證通過且出現不利和解 → 減碼至半倉；司法部刑事介入 → 清倉","evidence_refs":["regulatory_antitrust#2"]},{"id":"R5","text":"美國以外約 25% 營收的區域逆風：中東衝突（第二季營收影響約 5,000 萬美元；第三季歐中非營業利益少約 1,800 萬，八成以上來自中東；中東占全公司營收不到 3%）與中國價格約 −1 個百分點","h_ref":"H2","clock":"🔥","threshold":"2027 上半年比較基期轉易後，歐中非 GAAP 營業利益率仍年減","evidence_refs":["geo_supply_chain#2"]},{"id":"R6","text":"石棉相關破產案（Aldrich、Murray）是 10-K 自列的最重大訴訟；管理層稱待決法律事項不致造成重大不利，但準備金與現金流出規模事實表未涵蓋","h_ref":"H3","clock":"🐢","threshold":"破產法院裁定或和解，使公司須提列超出既有準備的費用，或單年現金流出超過自由現金流 5%","evidence_refs":["major_events#2","lawsuit_class_action#0"]}],"single_thing":{"description":"資料中心大單在 2027 年取消或大規模延後，使企業在手訂單連續兩季較前季淨減少","why_fatal":"在手訂單 125 億美元（+73%）的增量主要來自 Applied 與資料中心：追蹤中的 1,700 個大型專案逾九成是資料中心，Stellar 幾乎全為資料中心。訂單斷層會同時拉低 FY2027–FY2028 EPS（第三季 Applied 營收成長逾 60%）與倍數，是對終端股價影響最大的單一敏感度項","if_happens":"減碼至原部位一半，停止所有加碼，倉位上限降到 3%","how_monitor":"每季新聞稿的在手訂單總額、法說揭露的次年及以後在手訂單（目前逾 80 億美元）、全球 Applied 訂單年增率","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.2,"peg_fy2":1.44,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":12.98,"FY2026E":15.28,"FY2027E":17.7,"FY2028E":20.33},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報，調整後數字事實表未涵蓋；第三季 GAAP 與調整後差距約 0.06–0.07 美元）；FY2026E–FY2028E 為 Koyfin 共識調整後持續營運 EPS"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季 2026 財報與 2027 全年指引（價格對通膨、增量槓桿、在手訂單）","impact":"高","watch":"有機增量槓桿是否 ≥25%、2027 價格是否高於通膨、在手訂單是否再創高"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Cancoil 收購交割（預計 2026 年底或 2027 年初）","impact":"低","watch":"線圈供應瓶頸是否在 2027 上半年緩解"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"風扇、線圈、熱交換器的供應壓力預計在 2027 上半年改善（第三季法說 CEO）","impact":"中","watch":"調整後營益率年變化轉正"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"晶片商新一代 AI 系統出貨後，資料中心冷卻架構是否減少冷水機用量","impact":"中","watch":"全球 Applied 訂單、法說對架構的描述"},{"date":"2027-06","date_precision":"quarter","type":"macro","event":"運輸冷凍（Thermo King 美洲）進入多年上行週期的驗證","impact":"低","watch":"運輸訂單與營收年增"},{"date":"2027-12","date_precision":"month","type":"regulatory","event":"部分 HVAC 設備 232 關稅 15% 優惠期到期（2027-12-31）","impact":"中","watch":"是否延長；2028 年關稅成本指引"},{"date":null,"date_precision":null,"type":"regulatory","event":"HVAC 設備反壟斷集體訴訟的集體認證或和解進度","impact":"中","watch":"集體認證裁定、和解金額、司法部是否介入"}]}
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
