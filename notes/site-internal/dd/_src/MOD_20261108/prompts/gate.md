你是 DD 管線 v20 的判斷層閘（gate），標的 MOD（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝994.4 USD M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 2026-11-03 轉載）；YoY 由新聞稿 $738.9M 計算（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝20.7 %｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿；法說會 CFO：三個部門毛利率皆下降，主因材料成本通膨（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝97.8 USD M（利益率約 9.8%，由 97.8÷994.4 計算）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（SEC 8-K 轉載）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi3_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA／利益率（公司不揭露 Non-GAAP 營業利益，以 Adjusted EBITDA 為準）＝136.2 USD M（利益率 13.7%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿；利益率 13.7% 見法說會 CFO 說明（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得；管理層自承實際利益率低於自身預期
- `f_kpi7_fy2027_performance_techn`（q1_business）｜管理層全年指引（FY2027，已剔除 Performance Technologies）＝營收 $3.1–3.2B（+50–55%）；Adjusted EBITDA $470–500M（成長逾 50%） USD｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿與法說會 CFO 準備稿；資料中心營收 +80–90%、商用空調 +10–15%（兩者皆較上季上調）；FY27 資本支出指引 $150–200M；全年 FCF 預期為正（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：yfinance 共識營收 FY1 $3,283M（8 位分析師，見 capital_structure；與指引口徑可能不同，未剔除 PT 與否待確認）
- `f_kpi8_backlog_book_to_bill`（q1_business）｜訂單／積壓訂單（backlog）與 book-to-bill＝>1000 訂單；book-to-bill >2 USD M（資料中心季度新訂單，史上首次逾 $10 億）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03；法說會 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：法說會 CEO（連四季創紀錄訂單）與分析師問答中 book-to-bill 大於 2 的確認；backlog 金額公司未揭露，僅稱歷史新高；另獲超大型雲端客戶新案，2027 日曆年前供應逾 $400M 客製化空氣處理機組（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03；法說會 2026-11-04））
  - 註記：不適用
- `f_kpi9`（q1_business）｜產能利用／擴產進度（冰水機產線）＝13 條運轉中，目標 FY 年底 20 條｜期間與口徑：Q2 FY2027（法說會 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：法說會 CEO；公司未揭露利用率百分比（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2027（法說會 2026-11-04））
  - 註記：不適用
- `f_peer_mod_gross_margin_pct`（q2_moat）｜MOD 毛利率＝21.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MOD.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mod_operating_margin_pct`（q2_moat）｜MOD 營業利益率＝10.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MOD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mod_fcf_margin_pct`（q2_moat）｜MOD FCF 利潤率＝-0.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MOD.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_gross_margin_pct`（q2_moat）｜VRT 毛利率＝38.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝20.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_fcf_margin_pct`（q2_moat）｜VRT FCF 利潤率＝23.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aaon_gross_margin_pct`（q2_moat）｜AAON 毛利率＝25.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aaon_fcf_margin_pct`（q2_moat）｜AAON FCF 利潤率＝-6.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAON.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_gross_margin_pct`（q2_moat）｜TT 毛利率＝34.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_operating_margin_pct`（q2_moat）｜TT 營業利益率＝17.92 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_fcf_margin_pct`（q2_moat）｜TT FCF 利潤率＝16.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_gross_margin_pct`（q2_moat）｜JCI 毛利率＝36.71 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_operating_margin_pct`（q2_moat）｜JCI 營業利益率＝14.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.1 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.61 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝11.96 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3283.29 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（8 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝4292.14 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_fcf`（q4_capital）｜自由現金流（FCF）＝-140.6 USD M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營運現金流 −98.5、資本支出 −42.1；同表 Q1 FCF −5.0 與公司 Q1 新聞稿一致）；定性說明見法說會：營運資金、資料中心投資、分拆費用 $27.7M 現金支付、較高現金稅。Q2 新聞稿原文的現金流表本次未能取得，數字待對 10-Q 複核（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：不適用
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝4.8 %（SBC $4.7M ÷ GAAP 營業利益 $97.8M；占營收約 0.5%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow Stock Based Compensation 4.7M；營業利益見新聞稿。數字偏低，待對 10-Q 複核（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-03））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝716.4 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 867.0、現金 150.6（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝53.2 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝96.61 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝18.94 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 5.1，分子＝快照價 96.61｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-33.25 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 7.64 → 5.1（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝40.42 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝37.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝37.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.42 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝29.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝29.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.61 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝31.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝31.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝5855.75 USD m｜期間與口徑：2026-11-08／市值 5139.35 ＋ 淨負債 716.4｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.78 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-64.61 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝24.78｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 96.61 / W52 199.98 / W104 157.24 / W250 93.25 / W250 13週斜率 2.05%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝93.25 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱公司與眾多熱傳／HVAC&R 製造商競爭，供應鏈整併與垂直整合可能帶來新的或重組後的競爭者；並面對位於低勞動成本、低稅率地區的公司競爭。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-05-27）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：若新產品／專案未能及時推出，可能流失市占或損害客戶關係；技術落後會導致價格侵蝕。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-27）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 前十大客戶占淨銷售 49%（FY2025 43%、FY2024 40%）；Climate Solutions 一家全球科技客戶約占 11%，FY2025、FY2024 無單一客戶超過 10%。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-05-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因素揭露：資料中心、Gensets 等領域大部分銷售來自少數客戶，失去主要客戶或訂單量顯著下滑會對業績與現金流造成不利影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 稱預期 2027–2029 年對單一資料中心客戶銷售逾 40 億美元但無購買保證（搜尋摘要轉述）。
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-05-27）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Motley Fool：部分分析師警告 2026 下半年至 2027 資料中心電力與冷卻產能可能過剩；論點繫於超大規模業者 capex 放緩，文中亦反駁（機櫃密度上升）
  - 來源：Motley Fool: AI data center stock buy oversupply VRT（as_of 2026-05-22）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K 風險因子：公司明列貿易政策／關稅變動可能衝擊供應鏈、成本與需求；2026年2月最高法院裁定2025年IEEPA關稅無效，但其他關稅仍有效，退款時程與新關稅不確定。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：製造據點或原料來源涉及墨西哥、中國、加拿大，進口限制或關稅可能重大衝擊；墨西哥廠在IMMEX計畫下享減稅，該計畫變動為風險。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 Performance Technologies 銷貨成本中原料成本增加$10百萬，含關稅影響，銷貨成本率升170bp至81.9%。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-05-27）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K：資料中心產品所需部分零組件需求超過供應商產能，短缺自FY2026第四季開始，抑制資料中心產品擴產；公司正在認證新供應商。
  - 來源：Modine 10-K FY2026 (SEC EDGAR)（as_of 2026-05-20）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：最新10-Q（截至2026-09-30）列出美伊衝突、中東軍事衝突擴大、俄烏衝突、制裁與運費中斷為風險，可能推升能源燃料價格、延誤運輸、提高運費與製造成本。
  - 來源：Modine 10-Q period ended 2026-09-30 (SEC EDGAR)（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Chartmill：FY2027 EPS共識$7.34（12位分析師，10/17記錄），次季EPS共識一個月降約5%、三個月降約7%；Q2 FY27預期EPS $1.47、營收$946.95M。
  - 來源：Chartmill MOD estimates（as_of 2026-10-17）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：CPSC 於 2026-08-20 公告 Modine 旗下 Airedale ClassMate／SchoolMate 熱泵通風風扇因火災風險自願召回，美國約 6,061 台、加拿大約 735 台，11 起起火、財損至少 270 萬美元，無傷亡。
  - 來源：CPSC 召回公告（as_of 2026-08-20）｜affects：decision_inputs.bear、moat_trend
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：CPSC 於 2026-08-20 公告 Airedale ClassMate／SchoolMate 熱泵風扇火災風險自願召回，美國約 6,061 台，11 起起火、財損至少 270 萬美元。
  - 來源：CPSC 召回公告（as_of 2026-08-20）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":357.0,"bear_5y_price":60.5,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":88.4,"ev5y_pct":80.6,"irr_base_pct":13.5,"asym_ratio":4.1,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":5.1,"pe":18.94,"basis":"FY1 口徑：FY2027E 共識調整後 EPS 5.10，已不含分拆事業，股價 96.61 美元；終端倍數同用屆時 FY1 EPS。"},"eps":{"bull":[10.2,13.8,16.5,18.8,21.0],"base":[8.2,10.4,11.4,12.2,13.0],"bear":[6.0,5.5,4.2,4.8,5.5]},"pe":{"bull":17,"base":14,"bear":11},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MOD_Q1_2027_Earnings_Call_20260730.md
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 總營收成長指引 20%–35%，與前次相同（outlook unchanged）（原話："total company sales to grow in the range of 20% to 35%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 FY27 營收成長指引 60%–80%（原話："segment, we expect sales to grow 60% to 80%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 調整後 EBITDA 指引 6.5–6.8 億美元（原話："EBITDA to be in the range of $650 million to $680 million"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：FY27 全年自由現金流占營收 4%–6%（原話："full year free cash flow will be between 4% and 6%"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 FY27 盈餘成長預期超過 85%（原話："will generate earnings growth in excess of 85% this year."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：Q1 至 Q2 毛利/EBITDA 率預期階梯上升（原話："we expect a step-up in margins from Q1 to Q2"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：Q2 全公司利潤率預期上升約 200–250 bps（原話："probably a 200, 250 basis point lift."）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 Q2 EBITDA 率預期回到 19%–20%（原話："a lift to be back between 19% and 20%"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：資料中心 Q3、Q4 利潤率逐季再上升（原話："a step-up in Q3 from Q2 in margin"）
- 2026-07-30｜Mick Lucarelli (CFO)｜guidance：商用 HVAC 預期年底 EBITDA 率 18%–20%（原話："end the year somewhere between 18% and 20%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：資料中心 Q1 調整後 EBITDA 率 14.8%（原話："resulting in an adjusted EBITDA margin of 14.8%."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：管理層拆解：多餘人工與較低產量下的固定費用吸收影響利潤率 450–550 bps（原話："had a 450 to 550 basis point impact on margins"）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：管理層拆解：去年同期大額保固和解造成 150 bps 差異（原話："a 150 basis point warranty variance year-over-year"）
- 2026-07-30｜Neil Brinker (CEO)｜margin：管理層將利潤率壓力定性為暫時性時間差而非結構性（原話："are a transitional timing issue, not a structural one."）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：分拆 PT 後，HVAC 與資料中心毛利率預估較現在高 7–10 個百分點（原話："somewhere between 7% to 10% type gross"）
- 2026-07-30｜Mick Lucarelli (CFO)｜margin：PT 利潤率下滑歸因於量低與金屬、關稅成本回收落後（原話："this situation will become more favorable in future"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層稱供應鏈短缺不影響長期產能協議與年度財務目標（原話："capacity agreements or our financial targets for this year."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層對未來 2–3 年營收與盈餘成長能見度表達信心（原話："visibility and confidence in revenue and earnings growth"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層重申對 FY28 資料中心 50–70% 架構信心（原話："We're confident in the numbers that we put out, Matt."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：預計關鍵供應商 FY28、FY29 長約即將到位（原話："would expect to have that for FY '28 as well as FY '29 in"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：管理層稱本年度供應已確保（以供應商履約為前提）（原話："we've secured supply chain for -- going forward for this yea"）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：大型超大規模客戶長約 2027 年出貨比重 20–25%（原話："it's 20% to 25% in '27."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：大型客戶長約 2028、2029 年出貨比重 35–40%（原話："35% to 40% in '28 and '29."）
- 2026-07-30｜Mick Lucarelli (CFO)｜commitment：HVAC 目標今年再增 200 bps 利潤率（原話："the goal here is to add a 200 basis points this year."）
- 2026-07-30｜Neil Brinker (CEO)｜commitment：預期交易於日曆年底前完成（需核准與條件到位）（原話："we are still expecting to close the transaction before the"）
- 2026-07-30｜Neil Brinker (CEO)｜risk：供應鏈短缺比預期更早發生（原話："The shortages hit faster than we anticipated."）
- 2026-07-30｜Neil Brinker (CEO)｜risk：正考慮垂直整合以因應供應風險（原話："we're even considering vertical integration."）
- 2026-07-30｜Neil Brinker (CEO)｜risk：資料中心事業負責人離職，CEO 暫代（原話："In the interim, I will step in to lead this organization."）
- 2026-07-30｜Mick Lucarelli (CFO)｜risk：Q1 資料中心營收季減，含客戶專案延遲（原話："we also had a customer program delay"）
- 2026-07-30｜Neil Brinker (CEO)｜risk：延遲根源為特定超大規模客戶新產品設計變更，非供應鏈（原話："That is based on new product launch."）
- 2026-07-30｜Mick Lucarelli (CFO)｜risk：管理層指稱非冷水機組訂單取消或遞延（原話："chiller orders getting canceled or pushed out."）
- 2026-07-30｜Neil Brinker (CEO)｜customer：新增訂單主要來自兩家超大規模客戶與一家 Neocloud（原話："So it's basically the 3 largest customers that we"）
- 2026-07-30｜Neil Brinker (CEO)｜customer：缺料時優先供應最大客戶，與小客戶有較困難對話（原話："So our largest customers get priority."）
- 2026-07-30｜Neil Brinker (CEO)｜customer：訂單與積壓：連續第三季創新高（原話："consecutive quarter of record order intake"）
- 2026-07-30｜Mick Lucarelli (CFO)｜customer：年初約 70–80% 為確定訂單（原話："we have probably 70%, 80% of it in firm orders"）
- 2026-07-30｜Neil Brinker (CEO)｜competition：回應是否可能轉單給其他供應商：稱自家非商品化產品（原話："concerned if we were a commodity, but we're not."）
- 2026-07-30｜Neil Brinker (CEO)｜product：約一半冷水機組產能屬於長約，之後比例將下降（3MW 冷水機組上線）（原話："I'd say about half of it was part of the LTA"）
- 2026-07-30｜Neil Brinker (CEO)｜product：現有 CapEx 與廠房可支撐的產能約 40 億美元（原話："the range is right around $4 billion"）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：淨負債 4.33 億美元，較上年度底增加 7,000 萬（原話："Net debt of $433 million was $70 million higher"）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：股價走低，將與董事會討論買回股票（原話："we'll always have that discussion with the Board as well."）
- 2026-07-30｜Mick Lucarelli (CFO)｜capital_allocation：分拆後需為併購展望做準備（原話："gear up with an M&A outlook post that."）
- 2026-07-30｜Neil Brinker (CEO)｜capital_allocation：商用 HVAC 以定價抵銷材料與關稅通膨（原話："inflationary cost increases, including materials and tariffs"）

### 問答異常語氣（迴避／改口／保留）
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：Neal Burk 問 7 月以來資料中心量能與供應可得性的趨勢｜答法：Neil 只答本年度供應已確保（以供應商履約為前提），未給 7 月數字；Mick 後來表示不評論 7 月，只說 6 月利潤率明顯回升
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：Matt Summerville 問剩餘冷水機組產線（Grenada、Jefferson City、達拉斯）啟用時點，及 FY28 50–70% 架構是否調整｜答法：Neil 答「對數字有信心」及年底前產線將在某種效率水準上建立，未給各廠具體啟用日期，也未重述 FY28 數字
- MOD_Q1_2027_Earnings_Call_20260730.md｜問：David Tarantino 問供應問題如何隨 6、7 月演變｜答法：Neil 描述供應商硬性停供與重新談判，未給 7 月狀況；Mick 稱不逐月細說，僅講 6 月回到正常利潤率水準

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：MOD Modine Manufacturing antitrust OR DOJ OR FTC OR investigation 2026；Modine Manufacturing regulatory scrutiny OR competition authority OR lawsuit data center cooling 2026；Modine 10-K legal proceedings environmental regulation refrigerant HFC AIM Act 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"DC 業務維持 50-70% 年增至 FY2028、FY2028 DC 營收 $2B+","columns":{"2Y 驗證點":"FY2027 DC 年增落在 guide +60-80% 內","5Y 驗證點":"DC 營收 $2B+（FY28）並延續成長至 $3B+","10Y 驗證點":"MOD 成為 DC 冷卻長期結構受益者","具體數字門檻":"FY26 DC 已 +73% 至 $1.1B、Q4 DC +158%、$4B Airedale LTA（CY27-29）","來源":"MOD Q4 FY26 法說 / PR 2026-05-26","漂移觸發":"連 2 季 DC seq &lt; +10%（2Y 警戒）；DC 年增 &lt; +30%（5Y 反轉）"}},{"id":"H2","text":"Climate Solutions 毛利率在 DC 產能擴張暫時性壓縮後正常化回升","columns":{"2Y 驗證點":"FY2027 Climate GM 回升向 26%+","5Y 驗證點":"Climate GM 站穩 26-28%（規模經濟＋高階液冷 mix）","10Y 驗證點":"DC 溢價 mix 使結構毛利率高於歷史 auto thermal 時代","具體數字門檻":"Q4 FY26 Climate GM 24.6%（−510bps 因產能 ramp 暫時成本＋關稅）","來源":"MOD Q4 FY26 PR [官方歸因]","漂移觸發":"Climate GM 連 2 季再退 &gt; 1pp（2Y 警戒）；GM &lt; 22%（5Y 反轉→證偽「暫時」）"}},{"id":"H3","text":"Performance Technologies 分拆（RMT 併入 Gentherm）2026Q4 完成，純化 Climate Solutions 觸發估值 re-rate","columns":{"2Y 驗證點":"2026Q4-2027Q1 完成交割","5Y 驗證點":"純 Climate Solutions 以更高倍數獨立估值","10Y 驗證點":"—（一次性結構事件）","具體數字門檻":"2026-01-29 宣布 RMT；~$1B EV；Modine 收 $210M 現金＋股東持合併後 ~40%；outside date 2027-03-31（可延至 2027-06-30）","來源":"Modine / Gentherm IR 2026-01","漂移觸發":"2026Q4 未完成 + 推遲至 2027Q2+，或交易終止（2Y 警戒；直接削弱 H3）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"RMT 分拆延宕/失敗（融資、Gentherm 股東同意、IRS 稅務裁定、監管），分拆費用先吃近中期獲利、re-rate 敘事落空","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"交割進度公告；分拆相關費用","警戒閾值":"2026Q4 未完成且無明確新時程 → 直接削弱 H3、頁首 re-rate 假設下修"}},{"id":"R2","text":"AI DC capex 增速放緩，或電力/變壓器瓶頸（交期 36-48 個月、~11GW 專案卡公告）拖延冷卻設備實際交付 → DC 營收時程風險；疊加 hyperscaler 垂直整合冷卻","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"DC sequential 成長；hyperscaler 訂單能見度；四大 capex guide","警戒閾值":"DC seq 連 2 季 &lt; +10%；某 hyperscaler 宣布自建/獨家整廠冷卻協議"}},{"id":"R3","text":"單一客戶集中：$4B LTA 客戶未揭露身分，若其冷卻架構、時程或供應策略（second-source）生變，直接衝擊產能利用；技術路線上乾式冷卻/浸沒侵蝕冰水機","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"客戶集中度揭露；immersion/乾冷市佔；產能利用率","警戒閾值":"最大客戶佔 DC 營收 &gt; 40% 且出現 second-source 動作；immersion/乾冷架構市佔 &gt; 20%（2030 前）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"分批 starter 已建；加碼待 RMT 分拆完成（2026Q4-2027Q1）確認純 Climate Solutions re-rate，或回檔至 $200-215（Fwd PE FY27 ~26-28x）","irr_base_pct":7.1,"ev5y_pct":41.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.9,"ev5y_pct":41.0,"irr_base_pct":7.1,"max_dd_pct":-60.0,"bull_5y_price":528.0,"bear_5y_price":126.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"分批 starter 已建；加碼待 RMT 分拆完成（2026Q4-2027Q1）確認純 Climate Solutions re-rate，或回檔至 $200-215（Fwd PE FY27 ~26-28x）","price_at_dd":243.5,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MOD","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Modine Manufacturing Company"},"oneliner":"資料中心需求仍超過產能，但 7 月承諾的第二季 19–20% 利潤率只做到 15.4%；股價 96.61 美元已反映多數疑慮，第三季利潤率驗證前不加碼。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MOD_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺雲端與 AI 資料中心散熱設備的錢，現階段的錢卡在產能爬坡與零組件成本回收。","reasoning":"分拆 Performance Technologies 後只剩資料中心與商用 HVAC 兩部門。FY27 指引營收 31–32 億美元、調整後 EBITDA 4.7–5.0 億美元，資料中心年增 80–90%、商用 HVAC 年增 10–15%，以 FY26 資料中心 11 億美元推算，資料中心約占三分之二。第二季全公司營收 9.944 億美元、毛利率 20.7%、GAAP 營業利益率約 9.8%，這些數字仍含已分拆事業。資料中心營收年增 95%，新訂單首次超過 10 億美元，訂單對出貨比大於 2，在手訂單金額未揭露。單點依賴屬集中度風險，不是護城河證據：FY26 前十大客戶占銷售 49%，一家全球科技客戶約 11%，2027–2029 年逾 40 億美元協議據搜尋摘要轉述並無購買保證。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_adjusted_ebitda_non_gaap","f_kpi7_fy2027_performance_techn","f_kpi8_backlog_book_to_bill","f_kpi9"],"verdict_values":{"revenue_quality":"資料中心營收多屬專案與長約，成長主要靠量，CFO 稱指引上修多數來自量。第二季營收仍含分拆事業，第三季起改列停業單位。","unit_econ_note":"資料中心第二季調整後 EBITDA 率 15.4%，材料逆風約 375 基點；產品約 70–80% 可共用、20–30% 客製，庫存多為原料。單位毛利事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"單一資本支出循環約占營收三分之二，毛利率低於大型同業 13–16 個百分點，訂單對出貨比大於 2，自由現金流暫時轉負。"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期：訂單連四季創高、需求超過產能，但短缺漲價與客戶提前拉貨已帶偏後段徵兆。供需判斷：未來 24 個月偏結構性持久；2028 年以後偏週期性，供給可逆性高。來源：2026-11-04 法說 CEO、Dell'Oro 2026-08-19、Motley Fool 2026-05-22。","bargaining":{"up":"風扇、壓縮機、蒸發器等關鍵零件供不應求，公司付高價鎖量；風扇與蒸發器已簽長約或一年期採購單，壓縮機仍在談判，盤管自製。","down":"前十大客戶占銷售 49%、應收帳款 53%；合約可重開價，但回收有時間差，客戶也開始直接指定二級供應商。","geo":"墨西哥 IMMEX 廠區與關稅是主要曝險；續營業務受關稅影響的金額事實表未涵蓋。"},"profit_pool_dir":"近兩季短缺帶來的好處流向上游零件商與下游雲端客戶，公司尚未留住；五年利潤池占比事實表未涵蓋。","tam_table":[{"item":"資料中心實體基礎設施市場 2030 年","value":"1,200 億美元（Dell'Oro，2026-08-19）；熱管理是成長最快區塊"},{"item":"公司資料中心營收 FY27 指引推算","value":"約 20 億美元（FY26 11 億美元×1.85）"},{"item":"SAM、滲透率、份額、段 CAGR、營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"競爭優勢持平：需求與認證地位還在，定價權尚未證明。","reasoning":"機制是高能效的應用熱工程，加上自製盤管與客製產線認證。同業 ROIC 差距取不到，改用利潤率與最大客戶訂單判方向。TTM 毛利率 21.73%，VRT 38.12%、JCI 36.71%、TT 34.99%、AAON 25.57%；公司數字含低毛利的已分拆事業，續營口徑事實表未涵蓋。訂單方向有利：連四季創高，近期再獲逾 4 億美元空氣處理機專案。定價方向尚未改善：短缺環境下公司先替供應商的漲價付錢，再向客戶追回。兩者相抵，執行力與定價權都判穩定。","fact_refs":["f_peer_mod_gross_margin_pct","f_peer_mod_operating_margin_pct","f_peer_mod_fcf_margin_pct","f_peer_vrt_gross_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_vrt_fcf_margin_pct","f_peer_aaon_gross_margin_pct","f_peer_aaon_fcf_margin_pct","f_peer_tt_gross_margin_pct","f_peer_tt_operating_margin_pct","f_peer_tt_fcf_margin_pct","f_peer_jci_gross_margin_pct","f_peer_jci_operating_margin_pct","f_kpi8_backlog_book_to_bill","f_kpi9"],"verdict_values":{"moat":{"mechanism":"以低 PUE、低 WUE 的應用熱工程切入資料中心，配合自製盤管（CEO 稱全球最大獨立盤管廠）與客製產線認證，形成短中期卡位。","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力穩定：9、10 月冰水機廠準時交付率 100%，產線 13 條、目標 20 條；但第二季利潤率低於自身預期，資料中心事業負責人 7 月離職。定價權穩定：已談定至少 250 基點回收、新案前置定價，但第二季材料逆風約 375 基點尚未收回。","competitor_notes":[{"name":"VRT","strategy_note":"TTM 毛利率 38.12%、FCF 率 23.74%，同一波需求下定價與現金轉換明顯較佳。"},{"name":"AAON","strategy_note":"TTM 毛利率 25.57%、FCF 率 −6.8%，同樣處於擴產期，是現金結構最接近的對照。"},{"name":"TT","strategy_note":"TTM 營業利益率 17.92%、FCF 率 16.43%，大型 HVAC 平台的獲利水準高於公司。"},{"name":"JCI","strategy_note":"TTM 毛利率 36.71%、營業利益率 14.99%，毛利高但費用重；報導將其列為 AI 冷卻的較大對手。"}],"peer_na_reason":"同業 ROIC 差距事實表未涵蓋，改用毛利率、營業利益率與 FCF 率對照。","threats":[{"level":"🟡","text":"大型同業與整併後競爭者：10-K 提示供應鏈整併與垂直整合可能帶來新對手，新產品延遲會失去份額；目前未見份額流失證據，份額數字事實表未涵蓋。","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"客戶集中與議價：前十大客戶占 49%，資料中心銷售集中於少數客戶；雲端客戶開始直接指定二級供應商，短期帶來盤管機會，長期可能壓縮中間環節。","p":"30%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"level":"🟡","text":"Airedale 校用熱泵通風機火災召回：美國約 6,061 台、加拿大約 735 台，11 起起火、財損至少 270 萬美元，無傷亡。Airedale 也用於資料中心產品，品牌與負債影響的金額事實表未涵蓋。","p":"15%","evidence_refs":["major_events#2","product_recall_warning#0"]},{"level":"🟡","text":"架構替代：浸沒或乾冷路線可能侵蝕冰水機；公司已收購 TMGcore 技術因應，架構市佔事實表未涵蓋。","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×周轉未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運商，決策與付款者是雲端客戶，三角色都成立，散熱不能延後。第二季訂單對出貨比大於 2、需求高於產能。但 CEO 稱 2028 年以後的站點與規模仍有不確定，急迫不等於持久。"},{"item":"決策層級","level":"🟡","text":"替代要看單一站點或產品世代。產品 70–80% 可共用、20–30% 客製，新一代設計時客戶可重新選供應商；CEO 稱非商品化，但漲價後流失率與合約違約條款事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"目前兩頭受壓：上游零件短缺，公司付高價鎖量；下游前十大客戶占 49%，並開始直接指定二級供應商。TTM 毛利率低於 VRT 約 16 個百分點，第二季材料逆風約 375 基點、已談定回收約 250 基點。"},{"item":"社會容忍度","level":"🟡","text":"資料中心的用電與用水受地方社區關注，CEO 認為高能效產品因此受益；站點審批若收緊，總量會受影響。未見針對公司售價的監管或社會壓力。"}],"roiic":25.6,"reinvest_rate":62,"endo_ceiling":16,"formula_note":"以 FY25→FY26 年度資料粗估，稅率 25% 為假設：營業利益由 311.8 增至 370.9 百萬美元，增量稅後營業利益 44.3；FY26 稅後營業利益 278.2 減自由現金流 105.4，淨再投資 172.8。增量報酬＝44.3÷172.8＝25.6%，再投資率＝172.8÷278.2＝62%，內生上界約 16%。未計收購支出，含已分拆事業；投入資本事實表未涵蓋，當期 ROIC 無法計算。"}}}},"q3_growth":{"verdict":"第五年後的成長空間中等：到 FY29 有訂單支撐，更遠的第二曲線還沒落地。","reasoning":"成長以量為主，價格多為成本轉嫁，併購不是主要來源（FY26 氣候解決方案總成長 43%、有機 32%）。共識 EPS 由 FY27E 5.10 到 FY29E 11.96，兩年 CAGR 53%；FY26 實際 EPS 為含分拆事業的 GAAP 數字，不能當同口徑基期。內生上界約 16%，缺口約 37 個百分點，歸因於利潤率擴張與已投產能的營運槓桿：資料中心 EBITDA 率由 15.4% 往 20% 以上、分拆成本消失，不是淨回購或收購，也不依賴倍數重估。基礎情境 FY27E→FY32E EPS CAGR 約 20.6%，仍超過上界，因此 Bear 機率不低於 30%。盤管供應雲端客戶液冷供應鏈是增量，但仍在談判，與資料中心同屬一個循環，不算獨立第二曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_fy2027_performance_techn","f_kpi8_backlog_book_to_bill"],"verdict_values":{"growth":{"driver_mix":"量為主、成本轉嫁型漲價為輔；併購與回購目前都不是主要驅動。","runway_years":"事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"引用競爭優勢題的增量報酬估計，以 FY26 年度資料粗估約 16%，含已分拆事業、未含收購。","segments":[{"item":"資料中心","value":"FY26 約 11 億美元；FY27 指引年增 80–90%；第二季年增 95%，調整後 EBITDA 率 15.4%。"},{"item":"商用 HVAC","value":"FY27 指引年增 10–15%；第二季年增 23%，調整後 EBITDA 率 15.1%；盤管對資料中心銷售是增量來源。"}],"decay_signals":["毛利率同比下滑：FY26 第四季 −320 基點至 22.5%、FY27 第二季 −160 基點至 20.7%；第一季單季值事實表未涵蓋，以 TTM 21.73% 低於 FY26 的 22.98% 佐證。","EPS 成長高於營收成長逾 5 個百分點：FY1→FY2 EPS 增 88%、營收增 31%，依賴利潤率擴張。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換轉弱，但分拆現金入帳後資產負債表不構成壓力。","reasoning":"自由現金流占淨利 FY25 0.70、FY26 0.87，TTM 自由現金流率 −0.27%，第二季 −140.6 百萬美元（待對 10-Q 複核）。全年自由現金流由 7 月的營收 4–6% 改為只說為正。CFO 稱今年約 1 億美元屬非常態現金項目。公司口徑淨負債第二季末約 5.74 億美元（上年度底 3.63 億加 2.11 億），10 月 1 日收到 1.99 億美元後約 3.75 億，約為 FY27 EBITDA 指引中點的 0.8 倍。SBC 單季 4.7 百萬美元，占營收約 0.5%（待複核）。回購尚未決定，CFO 只說會提交董事會。現金去向四分事實表未涵蓋。","fact_refs":["f_kpi5_fcf","f_kpi6_sbc","f_net_debt_m","f_peer_mod_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Scott Springfield、LB White 等併購的投入金額與已實現報酬事實表未涵蓋，無法判定。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"目前無回購；CFO 於 2026-11-04 稱將提交董事會討論。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第二季 SBC 4.7 百萬美元，年化 18.8 百萬美元，除以市值 5,139 百萬美元約 0.37%，低於 1.5% 門檻；數字待對 10-Q 複核。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"FY26 氣候解決方案總成長 43%、有機 32%，成長主要不靠併購；近三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價大約只要求 FY29 共識盈餘實現後不再成長；我信一半，因為利潤率還沒驗證。","reasoning":"以 12% 年報酬、14 倍終端倍數反推，96.61 美元對應 FY2032 EPS 約 12.2，約等於 FY2029 共識 11.96 之後三年幾乎不成長。FY2 EPS 9.61 粗估需要全公司調整後 EBITDA 率約 19%（股數 53.2 百萬、稅率 25%、年折舊與利息合計約 1.25 億美元，後兩項為假設），FY27 指引中點約 15.4%，目前沒有一季實績支持。若利潤率過關，現價沒有計入 FY29 以後的續增。FY1 近 3 個月下修 33.25% 大部分是分拆移出的口徑差，以分拆事業年化 EBITDA 約 1.67 億美元、稅率 25% 推算約每股 2.35 美元上限，同口徑至少下修約 4%；折舊未揭露，實際更多。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_ev_s_fwd","f_rev_consensus_fy1_m","f_net_debt_m"],"verdict_values":{"valuation":{"basis":"FY1 前瞻 P/E，分母為已不含分拆事業的共識調整後 EPS。公司循環來自資本支出而非商品價格，P/B 也未收，因此不用 P/B。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未收同業 Fwd P/E；估值結論以自身前瞻倍數與隱含盈餘為準，不做跨公司倍數對照。"},"fwd_pe":18.94,"peg":0.36,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 P/E 18.94 倍、FY2 10.05 倍、PEG 0.36 看起來便宜，但分母未經驗證，因此判合理，不判便宜。Trailing P/E 40.42 倍、P/S 1.42 倍、EV/S 1.61 倍都含已分拆事業，分位只有 4 個年度端點（37、29.2、31.5），不是五年分位；五年分位事實表未涵蓋，故留空。EV 使用的淨負債 716.4 百萬美元含租賃，且是 10 月 1 日收到 1.99 億美元之前的數字，EV 約高估 2 億美元。","upside_short_pct":27.3,"upside_mid_pct":56.1,"denominator_disputed":true,"denominator_note":"FY1 EPS 5.10 已不含分拆事業，但 FY1 營收共識 32.83 億美元高於公司指引上限 32 億美元，口徑可能混雜。FY2 EPS 9.61 需要利潤率大幅回升，正是爭點；便宜的論證只在 FY2 兌現時成立。"}}},"q6_how_wrong":{"verdict":"不算價值陷阱，但證據還不足以排除；利潤率回不到 20% 是最可能看錯的地方。","reasoning":"衰退信號亮兩個：毛利率同比下滑、EPS 成長遠高於營收成長，屬中度風險。自由現金流占淨利 FY25 0.70、FY26 0.87，尚未連兩年低於 0.75，但 TTM 已為負，FY27 若只略為轉正就會亮燈。壓力測試四項過三項：FY30 之後成長降到 15%、10%、5%，搭配 15、12、9 倍，估值約 226、166、113 美元，都高於現價；Bear 倍數打八折、EPS 打八五折時約 41 美元，不過關。資料限制：第二季自由現金流與 SBC 待 10-Q 複核。7 月法說對 7 月量能、各廠啟用日與 FY28 架構未正面回答，本次 FY28 訂單覆蓋也推到投資人日，屬未回答事項。","fact_refs":["f_kpi5_fcf","f_kpi6_sbc","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_peer_mod_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率承諾尚待驗證的低價"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":5.1,"pe":18.94,"basis":"FY1 口徑：FY2027E 共識調整後 EPS 5.10，已不含分拆事業，股價 96.61 美元；終端倍數同用屆時 FY1 EPS。"},"eps":{"bull":[10.2,13.8,16.5,18.8,21.0],"base":[8.2,10.4,11.4,12.2,13.0],"bear":[6.0,5.5,4.2,4.8,5.5]},"pe":{"bull":17,"base":14,"bear":11},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-40,"basis":"下緣：Bear 路徑谷底 FY2030 EPS 4.2 乘 10 倍約 42 美元，較現價跌約 57%，取整為 −60%。上緣：Bear 終端價約 60.5 美元，跌約 37%，取整為 −40%。過去 26 週已跌 64.61%，實際路徑可能比基本面更劇烈。","trigger_time":null},"basis":{"bull":"FY28 營收約 45 億美元、EBITDA 率約 19.5%；FY32 營收約 82 億美元、EBITDA 率約 21%，盤管與液冷擴大；終端 17 倍低於現值 18.94 倍。同業現值倍數事實表未涵蓋，以自身現值對照。","base":"FY28 營收約 41 億美元、EBITDA 率約 17.5%，低於共識；FY29 後資本支出循環放緩，FY32 EPS 13.0；終端 14 倍低於現值 18.94 倍。同業現值倍數事實表未涵蓋。","bear":"AI 資本支出於 2028 年進入消化期，協議提貨縮減，FY30 EPS 谷底 4.2，FY32 回到 5.5；終端 11 倍。機率 35% 的依據：基礎情境超過內生上界、第二季利潤率失準、協議據轉述無購買保證。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"分析師警告 2026 下半年至 2027 年電力與冷卻產能可能過剩；逾 40 億美元協議據搜尋摘要轉述無購買保證，預付款 1.65 億美元約為協議金額 4%。","assumption":"雲端客戶在 2028 年仍依原定 35–40% 比重提貨，20 條產線持續滿載。","consequence":"若資本支出進入消化期，FY30 EPS 可能跌到 4.2 上下，以 10 倍計約 42 美元，較現價再跌約 57%。","ruling":"採納為 Bear 主路徑，機率 35%，不列基礎情境：站點已取得許可，訂單對出貨比大於 2，Dell'Oro 也預期到 2030 年維持兩位數成長。此路徑與唯一致命點部分重疊，需求退潮會讓利潤率守不住，因此需求面另立環比與訂單門檻。","watch":"訂單對出貨比、資料中心季營收環比、2028 年協議提貨比重。","evidence_refs":["supply_demand_durability#2","customer_concentration_credit#3"],"fact_refs":["f_kpi8_backlog_book_to_bill"]},{"view":"論點成功但股東經濟變差","evidence":"FY27 指引營收上修約 2.1 億美元，同口徑 EBITDA 反而少約 1,300 萬美元；第二季自由現金流 −140.6 百萬美元；公司付高價向供應商鎖量；7 月 CFO 提到分拆後要準備併購，CEO 也考慮垂直整合。","assumption":"量的成長能轉成每股現金。","consequence":"營收達標但 EBITDA 率停在 17% 上下、自由現金流率低於 5%，EPS 低於共識約兩成，倍數不會回升。","ruling":"部分採納，基礎情境 FY28 EBITDA 率只給 17.5%。不全採納的理由：CFO 指出約 1 億美元非常態現金項目不會延續，資本支出也會回落，但仍高於每年 1 億美元。","watch":"FY28 自由現金流率是否達 5%、大型併購金額。","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi5_fcf","f_kpi7_fy2027_performance_techn"]},{"view":"價格已反映太多","evidence":"股價 26 週跌 64.61%，但 FY2 10.05 倍的前提是 EPS 由 5.10 增至 9.61；10 月 17 日的 EPS 共識仍在下修。","assumption":"跌幅等於安全邊際，且共識不再下修。","consequence":"若 FY2 EPS 下修到 6 左右，現價等於約 16 倍，便宜的結論消失。","ruling":"反駁跌多就安全的說法，已跌幅度不當作安全邊際；共識若續降，Bear 地板會跟著下移，上下檔比只當參考，不作進場依據。但現價已不要求 FY29 之後的成長，估值不再是主要反對理由。","watch":"FY28 EPS 共識、第三季實績。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 243.5 → 本次 96.61（-60.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=243.5","side_b":"本次 price_at_dd=96.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟠、五年後跑道 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟠、五年後跑道 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 243.5 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 243.5 美元：Bull 價 528、Bear 價 126，五年期望值 +41.0%，基準年化 7.1%，不對稱比 2.9","side_b":"本次情境、股價仍用 243.5 美元：Bull 價 357、Bear 價 60.5，五年期望值 −28.3%，基準年化 −5.7%，不對稱比 0.35","ruling":"先換情境、股價不動：五年期望值少 69.3 個百分點，基準年化少 12.8 個百分點。不對稱比由 2.9 變為 0.35。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 243.5 美元：五年期望值 −28.3%，基準年化 −5.7%，不對稱比 0.35","side_b":"本次情境、股價 96.61 美元：五年期望值 +80.6%，基準年化 13.5%，不對稱比 4.12","ruling":"再換股價、情境不動：起點價下跌 60.3%，五年期望值多 108.9 個百分點，基準年化多 19.2 個百分點，不對稱比由 0.35 升到 4.12。合計五年期望值比前份多 39.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"資料中心利潤率：時間差還是結構問題","cause":"新證據","prior_field":["signal","trap"],"side_a":"2026-07-30 CFO 預期第二季資料中心 EBITDA 率回到 19–20%，CEO 稱壓力是時間差、非結構性；2026-11-04 CFO 稱已談定至少 250 基點的價格回收，第三季 16.5–17.5%、第四季 20% 以上。","side_b":"第二季實際 15.4%，差 360–460 基點；材料逆風約 375 基點且持續更久；利潤率改善速度下修，全年自由現金流由營收 4–6% 改成只說為正；資料中心事業負責人 7 月離職，由 CEO 暫代。","ruling":"性質為程度差異，可調和。採 A 側方向、B 側幅度：成本回收有合約與已談定金額支持，但管理層上季預測失準，第四季 20% 不作基礎情境，基礎情境 FY28 全公司 EBITDA 率只給約 17.5%。管理層的時間差歸因未證，若第三、四季連兩季低於各自下限，視為證偽。證據出來前維持不加碼。","evidence_level":"一手法說與公司指引，尚無下一季實績。","settle_metric":"資料中心調整後 EBITDA 率：第三季 16.5–17.5%（預估 2027-02 公布）、第四季 20%（預估 2027-05 公布）。","if_then":["若第三季資料中心 EBITDA 率不低於 16.5% 且全年自由現金流維持為正，則分批反買至原定上限。","若第三季低於 16.5%，則停止加碼，等第四季結果。","若第四季低於 18%，則清倉。","若股價先反彈而第三季尚未公布，則不追。","若股價再跌但第三季達標且訂單對出貨比仍大於 1，則分批反買，不作停損。"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"估值與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 243.5 美元，判定偏貴，牛熊機率 30／25，最大回撤假設 −60%。","side_b":"現價 96.61 美元，FY1 P/E 18.94 倍、FY2 10.05 倍。跌幅含 10 月 1 日分拆配發的價值，依前份約 10 億美元企業價值與 2.1 億美元現金推算約每股 15 美元，其餘多數是盈餘預期與倍數重估。","ruling":"估值由偏貴轉為合理，但不判便宜，因為便宜只在 FY28 盈餘兌現時成立。熊機率由 25 升至 35、牛機率由 30 降至 20，最大回撤改為 −40% 至 −60% 區間；機率變動同時反映第二季新證據。","evidence_level":"市場價格與共識快照。","settle_metric":"FY28 共識 EPS 9.61 在投資人日與第三季後是否維持。","if_then":["若 FY28 共識 EPS 降到 8 以下且股價未跌，則不追。","若 FY28 共識維持且第三季達標，則分批反買。"],"evidence_refs":[]},{"axis":"第五年後成長空間","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判定第五年後成長空間寬，依據是資料中心冷卻的長期結構受益。","side_b":"分拆後資料中心約占營收三分之二；CEO 稱 2028 年以後站點與規模仍有不確定；Dell'Oro 指容量新增的年增速 2026 見頂後放緩；事實表沒有滲透率或份額數字。","ruling":"下修為中等。需求沒有轉弱，但無法證明滲透率低，第二曲線也還在談判。","evidence_level":"法說與產業研究，滲透率缺口。","settle_metric":"盤管供應雲端客戶液冷的實際訂單、投資人日揭露的長期目標。","if_then":["若盤管新案取得具體訂單且揭露金額足以改變商用 HVAC 營收結構，則上調為寬，並延長持有年限。","若 FY29 指引已見資料中心成長低於 30%，則下修為窄並減碼。"],"evidence_refs":[]},{"axis":"公司歸類與循環位置","cause":"新證據","prior_field":["archetype","cycle_position"],"side_a":"前份歸為品質複利成長，未標循環位置。","side_b":"10 月 1 日分拆後只剩資料中心與商用 HVAC，資料中心約占三分之二；TTM 自由現金流率 −0.27%，毛利率低於大型同業 13–16 個百分點，獲利與單一資本支出循環綁定。","ruling":"改歸循環型資本設備，信心中等。循環位置判中段：未來 24 個月有訂單與站點支撐，但短缺漲價與客戶提前拉貨已是偏後段徵兆。","evidence_level":"公司指引、法說與同業財務。","settle_metric":"訂單對出貨比、資料中心環比、循環下行時的利潤率。","if_then":["若訂單對出貨比連 2 季低於 1，則改判晚循環並減碼。"],"evidence_refs":[]},{"axis":"競爭優勢方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"訂單連四季創高、新增大型專案、準時交付率回到 100%，支持地位未受損。","side_b":"利潤率遠低於同業，短缺環境下公司未能先行漲價，雲端客戶開始介入下游採購。","ruling":"維持持平。訂單證據與定價證據方向相反，互相抵銷；沒有客戶份額下滑的證據，也沒有定價權擴大的證據。","evidence_level":"法說與同業財務，份額缺口。","settle_metric":"第四季資料中心 EBITDA 率、最大客戶第二來源動作。","if_then":["若最大客戶出現第二來源且公司份額下滑，則改判下行並減碼。","若第四季資料中心 EBITDA 率達 20% 且 FY28 維持，則上調定價權評分。"],"evidence_refs":[]},{"axis":"加碼條件變更","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"分批 starter 已建；加碼待 RMT 分拆完成（2026Q4-2027Q1）確認純 Climate Solutions re-rate，或回檔至 $200-215（Fwd PE FY27 ~26-28x）","side_b":"第三季資料中心調整後 EBITDA 率不低於 16.5%，且全年自由現金流維持為正；觸發後重新做完整分析再建倉。","ruling":"舊條件已失效：分拆如期完成卻沒有帶來重估，200–215 美元也已跌破。加碼改用事件條件，不設進場價，因為目前約束是利潤率未驗證，不是價格。","evidence_level":"公司公告與股價。","settle_metric":"第三季資料中心 EBITDA 率與全年自由現金流指引。","if_then":["若第三季達標，則分批反買。","若第三季未達標，則停止加碼。"],"evidence_refs":[]},{"axis":"Single Thing 新增","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 欄位為空。","side_b":"FY27 第四季（2027 年 1–3 月，預估 2027-05 公布）資料中心調整後 EBITDA 率低於 18%。","ruling":"本次新增 Single Thing。利潤率是未來 24 個月最大且無法靠其他客戶抵銷的敏感項；協議客戶縮量在短缺期可轉給其他客戶，因此列為風險，不列唯一致命點。","evidence_level":"法說與敏感度推算。","settle_metric":"第四季資料中心調整後 EBITDA 率。","if_then":["若低於 18%，則清倉。","若介於 18% 與 20%，則停止加碼。"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未列獨立的清倉或減碼門檻，只在假設與風險表標示：資料中心連 2 季環比低於 +10%、年增低於 +30%、毛利率低於 22%、最大客戶占比高於 40% 且出現第二來源。","side_b":"清倉：第四季資料中心 EBITDA 率低於 18%，或 FY28 資料中心年增低於 +30%。減碼：連 2 季環比低於 +10%、訂單對出貨比連 2 季低於 1、FY27 全年自由現金流為負、最大客戶占比高於 40% 且出現第二來源。","ruling":"保留舊的環比、年增與客戶門檻，新增利潤率、訂單與現金門檻。毛利率 22% 改用分部 EBITDA 率，理由見舊假設處置條目。","evidence_level":"前份門檻與新法說。","settle_metric":"各門檻對應的季度揭露。","if_then":["任一清倉門檻觸發則清倉。","任一減碼門檻觸發則減碼。"],"evidence_refs":[]},{"axis":"舊假設與風險的處置","cause":"方法變動","prior_field":["H2","H3","R1"],"side_a":"舊 H3 與 R1 是分拆完成與延宕風險；舊 H2 是氣候解決方案毛利率回升至 26%，低於 22% 反轉。","side_b":"分拆已於 2026-10-01 完成；FY27 起分部改為資料中心與商用 HVAC，舊氣候解決方案毛利率取不到。","ruling":"分拆風險退休，因事件已完成，新 H3 改看現金轉換。舊毛利率門檻改為分部 EBITDA 率，第二季全公司毛利率 20.7% 含分拆事業，不能直接對舊門檻；舊 22% 門檻標資料缺口，待 10-Q 分部資料補上。","evidence_level":"8-K 與法說。","settle_metric":"10-Q 分部毛利、分部 EBITDA 率。","if_then":["若 10-Q 揭露兩個續營部門合計毛利率低於 22% 且連 2 季下滑，則減碼。"],"evidence_refs":[]},{"axis":"賣方目標價與共識","cause":"新證據","prior_field":null,"side_a":"賣方平均目標價落在 263–358 美元，FY2027 EPS 共識 7.34 美元（10 月 17 日）。","side_b":"現價 96.61 美元；可得目標價都在第二季財報之前，最低 73 美元、最高 355 美元，相差 4.9 倍；FY1 共識已是 5.10。","ruling":"目標價已過時，不支持也不反對本判斷，不採用。全距超過 2.5 倍，代表分歧很大，下調自身報酬估計的信心。新利空只有 4 天，FY2、FY3 是否完整入模無法確認，因此凍結加碼到第一個實績出現。","evidence_level":"第三方聚合資料，時點早於財報。","settle_metric":"投資人日後一個月內的共識與目標價。","if_then":["若 FY2 共識降幅超過 15% 且股價上漲，則不追。"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"指引上修的品質","cause":"新證據","prior_field":null,"side_a":"資料中心成長指引由 60–80% 上修至 80–90%，商用 HVAC 由 5–10% 上修至 10–15%，換算營收中點約增 2.1 億美元。","side_b":"舊 EBITDA 指引 6.5–6.8 億美元扣分拆事業年化約 1.67 億美元後為 4.83–5.13 億美元，新指引 4.7–5.0 億美元，同口徑約少 1,300 萬美元，其中含 1,000–1,500 萬美元過渡成本。","ruling":"營收確實上修，但新增營收沒有帶來利潤；扣除過渡成本後，增量 EBITDA 約為零。指引品質低於標題數字。","evidence_level":"公司指引，分拆事業年化值為推算。","settle_metric":"第三、四季資料中心 EBITDA 率。","if_then":["若第三季營收超指引但利潤率低於 16.5%，則停止加碼。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"訂單對出貨比大於 2、連四季訂單創高，資料中心指引上修到 80–90%，9、10 月準時交付率 100%，至少 250 基點價格回收已談定；現價只要 FY2032 EPS 約 12.2 就有 12% 年報酬。RSI 24.78，26 週已跌 64.61%。","side_b":"利潤率承諾上季剛失準，下一個實績約三個月後就有，等待的代價只是可能買貴一些；投資人日也在 10 天後。","ruling":"選擇等待。綁定條件是利潤率回收尚無實績，不是估值。","evidence_level":"法說與市場資料。","settle_metric":"第三季資料中心 EBITDA 率。","if_then":["若等待期間股價先漲而實績未到，則不追。","若第三季達標，則分批反買。"],"evidence_refs":[]},{"axis":"產業態勢","cause":"新證據","prior_field":null,"side_a":"競爭面：10-K 提示整併與垂直整合，報導列 Vertiv、Johnson Controls 為較大對手，雲端客戶開始直接指定二級供應商。","side_b":"結構面：需求高於供給，熱管理是資料中心基礎設施成長最快區塊，自製盤管在短缺中成為優勢。","ruling":"雙向拉鋸。競爭尚未反映在訂單上，結構順風也沒反映在利潤率上；其他結構變數以關稅與材料成本為主。","evidence_level":"10-K、法說、Dell'Oro。","settle_metric":"資料中心 EBITDA 率與客戶份額揭露。","if_then":["若訂單續強但利潤率連 2 季低於下限，則判競爭或議價惡化並減碼。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第三季資料中心利潤率是否進入管理層給的區間","type":"假設驗證","maps_to":"H2","metric":"FY27 第三季資料中心調整後 EBITDA 率","threshold":"不低於 16.5%","action":"達標且全年自由現金流維持為正，才解除加碼凍結","source_freq":"公司財報與法說；每季","date":"2027-02"},{"n":2,"text":"第四季資料中心利潤率是唯一致命點","type":"Single Thing","maps_to":"H2","metric":"FY27 第四季資料中心調整後 EBITDA 率","threshold":"低於 18%","action":"清倉","source_freq":"公司財報與法說；每季","date":"2027-05"},{"n":3,"text":"利潤率與現金同時過關後重新進場","type":"估值rearm","maps_to":"H2","metric":"第三季資料中心 EBITDA 率與全年自由現金流指引","threshold":"不低於 16.5%，且全年自由現金流維持為正","action":"重新做完整分析後分批反買","source_freq":"公司財報與法說；每季","date":"2027-02"},{"n":4,"text":"投資人日公布 FY28、FY29 展望與長期目標","type":"複審日期","maps_to":"H1","metric":"資料中心 FY28 成長與中期 EBITDA 率目標","threshold":"FY28 成長不低於 50%、中期 EBITDA 率目標不低於 20%","action":"低於門檻則停止加碼；達標也不單獨構成加碼","source_freq":"公司投資人日；一次性","date":"2026-11-18"},{"n":5,"text":"需求轉弱的領先訊號","type":"風險","maps_to":"R2","metric":"訂單對出貨比、資料中心季營收環比","threshold":"訂單對出貨比連 2 季低於 1，或環比連 2 季低於 +10%","action":"減碼","source_freq":"公司財報與法說；每季","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":6,"text":"大客戶提貨或第二來源變化","type":"風險","maps_to":"R3","metric":"最大客戶占資料中心營收、2028 年協議出貨比重","threshold":"占比高於 40% 且出現第二來源，或 2028 年出貨低於協議 35% 比重","action":"減碼","source_freq":"10-K、法說；每年與每季","date":null,"evidence_refs":["customer_concentration_credit#3"]},{"n":7,"text":"關稅與材料成本吸收失敗","type":"風險","maps_to":"R4","metric":"材料與關稅淨逆風占資料中心營收","threshold":"連 2 季超過 375 基點","action":"停止加碼","source_freq":"公司法說；每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#3"]},{"n":8,"text":"全年現金未轉正","type":"減碼","maps_to":"H3","metric":"FY27 全年自由現金流","threshold":"低於 0","action":"減碼","source_freq":"公司財報與 10-K；每年","date":"2027-05"},{"n":9,"text":"資料中心成長中斷","type":"清倉","maps_to":"H1","metric":"FY28 資料中心營收年增率","threshold":"低於 +30%","action":"清倉","source_freq":"公司財報；每季","date":"2028-05"}],"kill_metrics":[{"metric":"資料中心調整後 EBITDA 率（FY27 第四季）","bear_threshold":"低於 18%","window":"FY27 第四季，預估 2027-05 公布","source":"公司新聞稿與法說","last_status":"warning"},{"metric":"資料中心季營收環比","bear_threshold":"連 2 季低於 +10%","window":"連續 2 季","source":"公司財報與法說；分部季額待補","last_status":"unknown"},{"metric":"資料中心營收年增率","bear_threshold":"低於 +30%","window":"FY28","source":"公司財報與法說","last_status":"ok"},{"metric":"訂單對出貨比","bear_threshold":"連 2 季低於 1","window":"連續 2 季","source":"公司法說","last_status":"ok"},{"metric":"全年自由現金流","bear_threshold":"低於 0","window":"FY27","source":"公司財報與 10-K","last_status":"warning"},{"metric":"最大客戶占資料中心營收","bear_threshold":"高於 40% 且出現第二來源","window":"每年 10-K","source":"10-K；占比資料缺口","last_status":"unknown"},{"metric":"浸沒與乾冷架構市佔","bear_threshold":"2030 年前高於 20%","window":"至 2030 年","source":"產業研究；資料缺口","last_status":"unknown"}],"evidence_dismissed":[{"ref":"reg_tariff_export#2","reason":"這筆 1,000 萬美元原料與關稅影響只量測 Performance Technologies，該事業已於 2026-10-01 分拆，不在續營成本結構內；續營業務改用 2026-11-04 法說的資料中心材料逆風約 375 基點。"}],"action_conditions":{"rearm_trigger":"第三季資料中心調整後 EBITDA 率不低於 16.5%，且全年自由現金流維持為正；觸發後重新做完整分析再建倉。","exec_line":"未持有者不建倉；已持有者續抱不加碼。第三季達標才分批反買，第四季資料中心利潤率低於 18% 清倉。","holding_cap":"驗證前不高於現有部位"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第二季 15.4% 當成新常態；但至少 250 基點的價格回收已談定，新案改為出貨前定價，第三季 16.5–17.5% 可驗證。此理由尚未經實績確認。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27 第三季財報（預估 2027 年 2 月）：資料中心調整後 EBITDA 率不低於 16.5%，且全年自由現金流維持為正；11 月 18 日投資人日只作輔證。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"資料中心需求兌現：FY27 年增 80–90% 後，FY28 仍維持 50% 以上。","2y":"FY28 資料中心營收達 30 億美元以上","5y":"FY32 資料中心營收達 50 億美元以上","10y":null,"threshold":"FY27 年增 80–90%；FY28 年增不低於 50%，低於 30% 視為反轉；季營收環比不得連 2 季低於 +10%；訂單對出貨比不得連 2 季低於 1。","source":"公司財報與法說，每季；FY28 架構見 2026-07-30 法說 CEO，2026-11-18 投資人日更新。","drift_rule":"兩年期：TTM 偏離連 2 季達 5% 削弱、連 3 季達 10% 反轉；環比資料缺口待分部揭露補上。"},{"id":"H2","text":"利潤率壓縮是爬坡與成本回收的時間差，第四季起資料中心回到 20% 上下。","2y":"FY27 第四季資料中心調整後 EBITDA 率不低於 18%，管理層目標 20%；FY28 全公司調整後 EBITDA 率約 17.5% 以上","5y":"FY32 全公司調整後 EBITDA 率 18% 以上","10y":null,"threshold":"第三季 16.5–17.5%；第四季低於 18% 視為反轉；商用 HVAC 全年約增 100 基點。","source":"公司財報與法說，每季；指引見 2026-11-04 法說 CFO。","drift_rule":"兩年期：連 2 季低於當季下限削弱，第四季低於 18% 直接反轉。"},{"id":"H3","text":"成長可以自籌，FY27 自由現金流轉正，FY28 起現金轉換恢復。","2y":"FY28 自由現金流率 5% 以上，資本支出低於 FY27 指引 1.5–2 億美元","5y":"FY32 自由現金流占淨利 0.9 以上","10y":null,"threshold":"FY27 全年自由現金流為正；FY28 自由現金流率不低於 5%。","source":"公司財報與 10-Q，每季；指引見 2026-11-04 法說 CFO。","drift_rule":"兩年期：TTM 自由現金流率連 2 季低於目標 5 個百分點以上削弱；FY27 全年為負直接反轉。"}],"R":[{"id":"R1","text":"成本回收落後或再遇新漲價，資料中心利潤率第二次失準；7 月資料中心事業負責人離職、CEO 暫代，加重執行風險。","h_ref":"H2","clock":"⚡","threshold":"第三季資料中心 EBITDA 率低於 16.5%，或第四季低於 18%。","evidence_refs":["geo_supply_chain#0"]},{"id":"R2","text":"AI 資本支出放緩或電力瓶頸延後交付；冷卻設備是站點最後進場的產品，需求退潮會比開工放緩晚 12–18 個月反映。","h_ref":"H1","clock":"🔥","threshold":"資料中心環比連 2 季低於 +10%；訂單對出貨比連 2 季低於 1；雲端客戶宣布自建或獨家整廠冷卻協議。","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"大客戶集中：前十大占 49%，最大客戶約 11%，逾 40 億美元協議據搜尋摘要轉述無購買保證，預付款只有 1.65 億美元。","h_ref":"H1","clock":"🔥","threshold":"最大客戶占資料中心營收高於 40% 且出現第二來源（占比資料缺口）；2028 年協議出貨低於原定 35% 比重。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_concentration_credit#3"]},{"id":"R4","text":"關稅、貿易政策與地緣衝突推高材料與運費，轉嫁有時間差；不預測政策，只看損益是否吸收失敗。","h_ref":"H2","clock":"⚡","threshold":"材料與關稅淨逆風占資料中心營收超過 375 基點，連 2 季。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#3"]},{"id":"R5","text":"營運資金與資本支出繼續吃現金，全年自由現金流只能略為轉正或轉負。","h_ref":"H3","clock":"⚡","threshold":"FY27 全年自由現金流為負，或為擴產增資。","evidence_refs":[]},{"id":"R6","text":"架構替代：浸沒或乾冷路線侵蝕冰水機需求。","h_ref":"H1","clock":"🐢","threshold":"浸沒與乾冷架構市佔於 2030 年前高於 20%（資料缺口）。","evidence_refs":[]}],"single_thing":{"description":"FY27 第四季（2027 年 1–3 月，預估 2027-05 公布）資料中心調整後 EBITDA 率低於 18%。","why_fatal":"以 FY28 資料中心營收約 32 億美元計，每 100 基點約等於 3,200 萬美元 EBITDA、每股 0.45 美元，且沒有其他項目可抵銷；短缺期客戶縮量還能把產能轉給別人，利潤率沒有這個緩衝。第四季低於 18% 等於連續失準，代表短缺下的定價權不存在，FY28 EPS 會落到 6 上下。","if_happens":"清倉，FY28 EPS 改用 Bear 路徑 6.0。","how_monitor":"第三季 16.5–17.5% 是前哨；每季看分部 EBITDA 率、材料逆風基點與已談定的價格回收。","probability":"12–24 個月約 30%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":10.05,"peg_fy2":0.41,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2026A":2.26,"FY2027E":5.1,"FY2028E":9.61,"FY2029E":11.96},"fy_end_month":3,"eps_basis":"FY2027E–FY2029E 為 Koyfin 共識調整後 EPS（2026-11-07 快照，家數事實表未涵蓋），FY2027E 已不含分拆事業。FY2026A 為含分拆事業的 GAAP 稀釋 EPS，與共識不同口徑，成長率改用 FY27E→FY29E 兩年 CAGR 53%。"},"catalysts":[{"date":"2026-11-18","type":"guidance","event":"分析師與投資人日，公布 FY28、FY29 展望與新長期財務目標","impact":"高","watch":"資料中心 FY28 成長是否維持 50–70%、中期 EBITDA 率目標、資本支出與回購"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第三季財報（日期為預估，公司未公告）","impact":"高","watch":"資料中心調整後 EBITDA 率是否達 16.5–17.5%、全年自由現金流指引"},{"date":"2027-03","date_precision":"month","type":"capacity","event":"財年底 20 條冰水機產線目標期限","impact":"中","watch":"運轉線數、準時交付率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第四季與全年財報（日期為預估，公司未公告）","impact":"高","watch":"資料中心調整後 EBITDA 率是否達 20%、全年自由現金流"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第二季 15.4% 當成新常態；但至少 250 基點的價格回收已談定，新案改為出貨前定價，第三季 16.5–17.5% 可驗證。此理由尚未經實績確認。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-64.61, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：regulatory_antitrust（法規／反壟斷）（尾部風險或事件型，不擋）。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
