你是 DD 管線 v20 的判斷層閘（gate），標的 EAT（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_total_revenues_gaap`（q1_business）｜Total revenues (GAAP)＝1475.6 US$M｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi1_operating_income_gaap`（q1_business）｜Operating income (GAAP)＝151.0 US$M｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi2_operating_margin_excl_ot`（q1_business）｜Operating margin excl. other gains & charges（衍生值：GAAP OI 151.0＋other gains and charges 2.4＝153.4，/1,475.6）＝10.4 %｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi3_restaurant_operating_mar`（q1_business）｜Restaurant operating margin (non-GAAP)＝17.7 %｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi7_comparable_restaurant_sa`（q1_business）｜Comparable restaurant sales — Brinker／Chili's＝9.1 %｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[7]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi8_guidance_fy2027_total_re`（q1_business）｜Guidance FY2027 total revenues＝6230～6330 US$M｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[8]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi9_guidance_fy2027_adjusted`（q1_business）｜Guidance FY2027 adjusted EPS (non-GAAP)＝13.3～13.9 US$｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[9]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：dd_numbers_extra consensus_revision：FY1 13.68（2026-10-31 快照，已含財報後修正）；指引中點 13.60
- `f_peer_eat_gross_margin_pct`（q2_moat）｜EAT 毛利率＝19.14 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EAT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eat_operating_margin_pct`（q2_moat）｜EAT 營業利益率＝11.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EAT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eat_fcf_margin_pct`（q2_moat）｜EAT FCF 利潤率＝11.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EAT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_dri_operating_margin_pct`（q2_moat）｜DRI 營業利益率＝12.18 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DRI.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_dri_fcf_margin_pct`（q2_moat）｜DRI FCF 利潤率＝7.64 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DRI.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_txrh_operating_margin_pct`（q2_moat）｜TXRH 營業利益率＝7.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXRH.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_txrh_fcf_margin_pct`（q2_moat）｜TXRH FCF 利潤率＝6.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXRH.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cmg_operating_margin_pct`（q2_moat）｜CMG 營業利益率＝14.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mcd_operating_margin_pct`（q2_moat）｜MCD 營業利益率＝45.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1768.4 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 1799.1、現金 30.7（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝10582.93 USD m｜期間與口徑：2026-11-02／市值 8814.53 ＋ 淨負債 1768.4｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.78 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝90.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.68 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝14.8 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝16.45 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6308.76 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6494.11 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_stock_based_compensation`（q1_business）｜Stock-based compensation（占 GAAP 營業利益 5.5%、占營收 0.56%）＝8.3 US$M｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_kpi5_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝105.7 US$M｜期間與口徑：Q1 FY2027（季末 2026-09-23，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/703351/000070335126000036/fy27q1ex991-earningsrelease.htm（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（季末 2026-09-23，公告於 2026-10-28））
  - 註記：未查得共識，省略比較
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝41.54 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.51 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 13.68，分子＝快照價 212.18｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝212.18 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝18.71 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝45.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝45.9 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.49 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝93.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝93.6 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝90.1 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.68 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.22 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（13.65 → 13.68）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝27.14 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 10.76 → 13.68（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝43.23 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝157.58 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝90.31 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Maggiano's FY26可比銷售 -3.9%、客流 -9.3%（集團內弱項）
  - 來源：Brinker earnings coverage (Zacks/Nasdaq)（as_of 2026-08-12）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：NRA中期更新：2026經通膨調整餐飲銷售成長預測由1.3%下調至0.8%（油價>$4拖累）；未見官方2027/2028銷售預測；2027僅有總經GDP +2.5%
  - 來源：National Restaurant Association midyear update（as_of 2026-07-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：EAT 10-K FY2026 風險因子：美國或全球貿易政策變動（如新增或加徵食品／進口品關稅）可能持續推高成本、擾亂供應，並限制以定價保護利潤率的能力。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-19）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：EAT 10-K FY2026 MD&A：地緣緊張與總體壓力導致產品成本通膨（含關稅）與供應鏈中斷。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-08-19）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K 風險因子：貿易政策變動（如對某些食品或進口商品新增或加徵關稅）可能推高成本、干擾供應；未能有效管理供應鏈風險會增加成本或減少營收。未見單一地緣區域或單點供應商集中度的量化揭露。
  - 來源：Brinker International Form 10-K FY2026 (SEC)（as_of 2026-06-24）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Maggiano's FY2026 可比店銷售 -3.9%、客流 -9.3%；Q2 FY26 Maggiano's 可比 -2.4% 對 Chili's +8.6%，公司稱因客流下降
  - 來源：Brinker FY2026 results / Q2 FY26 release (franchising.com) 及 Q1 FY27 摘要（as_of 2026-01-28）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":399.6,"bear_5y_price":129.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":41.0,"ev5y_pct":28.9,"irr_base_pct":7.1,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.68,"pe":15.51,"basis":"FY2027（2027年6月止）共識每股盈餘13.68美元，含第53週約0.70美元；與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[13.95,15.6,17.7,19.9,22.2],"base":[13.6,14.7,16.3,17.8,19.3],"bear":[12.9,11.6,10.8,11.2,11.8]},"pe":{"bull":18,"base":15.5,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":3.5},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EAT_Q4_2026_Earnings_Call_20260812.md
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 營收財測區間 $6.15B–$6.27B（原話："we expect F '27 annual revenues in the range of $6.15 billion to $6.27 billion,"）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 調整後稀釋 EPS 財測 $12.60–$13.40（原話："adjusted diluted EPS in the range of $12.60 to $13.40,"）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 資本支出財測 $265M–$285M（原話："and capital expenditures in the range of $265 million to $285 million."）
- 2026-08-12｜CFO Mika Ware｜guidance：FY27 第四季含第 53 週，估計增加約 2% 營收與 $0.70 EPS（原話："approximately 2% in total revenues and $0.70 in incremental earnings per share."）
- 2026-08-12｜CFO Mika Ware｜guidance：財測假設：7 月加一點上檔後，其餘時間 Chili's 同店中個位數、客流為正（原話："for the remainder of the year, we have assumed mid-single digit same-store sales and"）
- 2026-08-12｜CFO Mika Ware｜guidance：財測含收購阿拉巴馬與密西西比 12 家 Chili's 加盟店（原話："Guidance also contemplates the planned acquisition of 12 Chili's franchise restaurants located in"）
- 2026-08-12｜CFO Mika Ware｜guidance：12 家收購店對 EPS 影響約持平，增量營收約 $30M（原話："it's going to have a flat impact to EPS basically because it's a very small acquisition."）
- 2026-08-12｜CFO Mika Ware｜guidance：財測假設 Maggiano's 營收與獲利與去年持平（原話："Maggiano's is going to have flat revenues and flat profits"）
- 2026-08-12｜CFO Mika Ware｜guidance：全年定價約略高於 3%，組合（mix）假設持平，其餘成長來自客流（原話："flattish mix for the year. You got the price just over 3%"）
- 2026-08-12｜CFO Mika Ware｜margin：FY27 以 52 週計，餐廳層級利潤率預期改善 20–40bp（原話："I'm going to expect 20 to 40 basis points of margin improvement."）
- 2026-08-12｜CFO Mika Ware｜margin：第 53 週可讓利潤率改善最高到 50bp（原話："Depending on where it falls in that range, the 53rd week could get you"）
- 2026-08-12｜CFO Mika Ware｜margin：各季商品通膨建模路徑：Q1 4%、Q2 3%、Q3 2%、Q4 1%（原話："Q1, 3% inflation in Q2, 2% inflation in Q3 and 1% in Q4."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層說利潤率成長在轉型後會趨緩（對比轉型期累積逾 600bp 改善）（原話："you're going to see the margin growth moderate a little bit."）
- 2026-08-12｜CFO Mika Ware｜margin：回答利潤率有無天花板：仍可擴張，但幅度不會像轉型期那麼大（原話："It's just not going to be as material as it has been during this turnaround."）
- 2026-08-12｜CEO Kevin Hochman｜margin：CEO 表示每年起始的利潤率財測偏合理，歷來都被超越（原話："then we've blown through it"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 Brinker 餐廳營業利潤率 18%，年增 20bp（原話："restaurant operating margins were 18%, a 20 basis points improvement"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 食材與飲料成本增加 80bp，商品通膨 4.4%（原話："Food and beverage costs for the quarter increased by 80 basis points, driven by 4.4% commodity"）
- 2026-08-12｜CFO Mika Ware｜margin：番茄價格飆升比預期久，已正常化且不影響 Q1 成本（原話："Tomato costs remained elevated longer than expected, but have since normalized and will"）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 人力成本占比年減 90bp（原話："Labor for the quarter was favorable 90 basis points year-over-year."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層要求營運端依想要的銷量排班，人力效率未達預期（原話："We have been telling our operators to staff for the sales they want."）
- 2026-08-12｜CFO Mika Ware｜margin：Q4 Chili's 同店 +5.6%：價格 4.3%、客流 +1.5%、組合 -0.2%（原話："driven by price of 4.3% and positive traffic of 1.5%, partially offset by negative mix of 0.2%."）
- 2026-08-12｜CFO Mika Ware｜margin：定價策略原為 3–5%，FY27 落在低端（原話："3% to 5%. We're on the lower end of that."）
- 2026-08-12｜CFO Mika Ware｜margin：管理層提到餐廳仍有客流容量（為歷史客數的 80%）（原話："Our restaurants are only at 80% capacity of"）
- 2026-08-12｜CEO Kevin Hochman｜competition：CEO 稱 Chili's 每人均消費比競爭對手低 $3–4（原話："average spend that is $3 to $4 below competition"）
- 2026-08-12｜CFO Mika Ware｜competition：CFO 稱同業也有不想現在過度提價的心態，因此自身保守看待定價（原話："You've heard a lot of our competitors have that same mindset"）
- 2026-08-12｜CEO Kevin Hochman｜product：Big Crispy 每店每日雞肉三明治銷量由 20 個升到 55 個（原話："By the end of Q4, we were selling 55 sandwiches per restaurant per day"）
- 2026-08-12｜CEO Kevin Hochman｜product：CEO 稱 Big Crispy 規模大於前兩次 Big Smasher 與 Big QP 的上市（原話："the Big Crispy is bigger than the '24 Big Smasher launch"）
- 2026-08-12｜CEO Kevin Hochman｜product：FY27 菜單優先順序調整，沙拉延到 FY28 上半年（原話："We have shuffled a little bit of our priorities in '27"）
- 2026-08-12｜CEO Kevin Hochman｜product：沙拉改在 FY28 上半年推出（原話："front half, we're going to launch salads."）
- 2026-08-12｜CEO Kevin Hochman｜product：外帶占營收 25%，被稱為尚未開發的下一個前沿（原話："which we haven't even scratched the surface on is to-go."）
- 2026-08-12｜CEO Kevin Hochman｜product：用餐室循環時間改善至少還有 3 年跑道（原話："we've got at least 3 years of runway on that"）
- 2026-08-12｜CFO Mika Ware｜product：3 For Me 參與率穩定，Q4 略高於 21%（原話："So in Q3, it was just under 21%. And in Q4, it's just over 21%"）
- 2026-08-12｜CEO Kevin Hochman｜customer：每月近一半以上的 token（會員代碼）為新客（原話："a little bit more than half of the tokens that we see each month"）
- 2026-08-12｜CFO Mika Ware｜customer：客流成長涵蓋各收入層級（原話："We're growing all income levels, low,"）
- 2026-08-12｜CFO Mika Ware｜risk：酒類品類整體承受壓力（原話："look at the whole alcohol category, we're feeling a little pressure"）
- 2026-08-12｜CEO Kevin Hochman｜risk：CEO 提到產業面臨的總體逆風仍在（原話："The macro headwinds the industry is experiencing are still there"）
- 2026-08-12｜CEO Kevin Hochman｜risk：Maggiano's 轉型進度比計畫慢（原話："the turnaround is happening slower than we had planned."）
- 2026-08-12｜CFO Mika Ware｜risk：Q4 Maggiano's 同店 -2.5%、客流 -5.3%（原話："comp sales for the quarter of negative 2.5% with negative"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：Q4 回購 $100M 普通股（原話："repurchasing $100 million of common stock"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：董事會 8 月增加回購授權，可用總額達 $750M（原話："program in August, bringing the total amount available to"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：年度結束後以循環信貸額度贖回 $350M 8.25% 債券（原話："we redeemed our outstanding $350 million, 8.25% bonds"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：資本支出上調的大宗來自店面改裝（reimage）（原話："The majority of that increase year-over-year is due to the reimages"）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：FY27 計畫再完成 60–80 家改裝（FY26 為 11 家）（原話："we plan to complete another 60 to 80 during fiscal '27."）
- 2026-08-12｜CFO Mika Ware｜capital_allocation：管理層偏好持有不動產，不傾向賣回租回（原話："We prefer probably just to hold the real estate."）
- 2026-08-12｜CFO Mika Ware｜commitment：FY28 起改裝步調為每年 10% 店數（原話："we will start a planned cadence of 10% of the fleet annually."）
- 2026-08-12｜CFO Mika Ware｜commitment：新店成長 FY27 溫和，FY28 顯著加速，細節留待 9/17 投資人日（原話："the pipeline to ramp up significantly in fiscal '28"）
- 2026-08-12｜CFO Mika Ware｜commitment：CFO 稱有信心達成先前承諾的雙位數 EPS 成長（原話："So we feel good about delivering the results in the double-digit EPS"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：管理層承諾維持價值領先與改善客人體驗（原話："we will work hard for our guests to maintain both our value leadership"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：廣告與 $10.99 輪替的做法不打算改變（原話："So we don't plan on changing that formula."）
- 2026-08-12｜CEO Kevin Hochman｜commitment：營運副總的 FY27 執著指標：客流第三年，新增獲利改善（原話："have chosen traffic for a third year in a row"）
- 2026-08-12｜CEO Kevin Hochman｜commitment：店經理獎金改為完全聚焦銷售與獲利，GWOP 移出獎金（原話："We removed that from the bonus."）
- 2026-08-12｜CFO Mika Ware｜guidance：CFO 稱 7、8 月顯著加速，Q1 同店高於 Q4 的 6%，未給具體數字（原話："if Chili's was 6% in Q4, that means it's higher than that in Q1."）
- 2026-08-12｜CFO Mika Ware｜guidance：CFO 說 7 月營收與客流較 Q4 顯著加速（原話："significantly accelerated versus the fourth quarter,"）

### EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md
- 2026-09-17｜Mika Ware｜guidance：CFO 給出 3 年新目標：年營收成長 4%–6%（原話："deliver 4% to 6% annual revenue growth"）
- 2026-09-17｜Mika Ware｜guidance：3 年目標含雙位數 EPS 成長（原話："deliver double-digit EPS growth"）
- 2026-09-17｜Mika Ware｜guidance：新目標隱含假設：新店 2–3%、買回 3–5%（原話："Underlying these assumptions are the 2% to 3% new unit"）
- 2026-09-17｜Mika Ware｜guidance：CFO 對同店銷售的基本情境假設為 2%–3%，並稱有機會超標（原話："2% to 3% same-store sales, that seems highly achievable"）
- 2026-09-17｜Mika Ware｜guidance：價格／組合：mix 預期持平到略正（原話："flat to slightly positive moving forward"）
- 2026-09-17｜Mika Ware｜margin：餐廳利潤率每年 20–40 bps 的常態化擴張，維持舊說法（原話："still going to stick with my 20 to 40 basis points per year"）
- 2026-09-17｜Mika Ware｜margin：被問 North of 6 的 400 bps 差距能實現多少，CFO 稱不一定走到 400（原話："are we going to get all the way to 400? Maybe not."）
- 2026-09-17｜Kevin Hochman｜margin：North of 6 餐廳的餐廳營業利潤率比系統高 400 bps（原話："400 basis points better than the system"）
- 2026-09-17｜Kevin Hochman｜margin：North of 6 占比僅 20%，管理層以此論述利潤率上升空間（原話："only 20% of our estate are north of 6"）
- 2026-09-17｜Kevin Hochman｜margin：管理層稱利潤率擴張的主因是 AUV 而非砍成本（原話："the main driver of our margin expansion has been AUVs"）
- 2026-09-17｜Mika Ware｜margin：Chili's 品牌營業利潤率超過 18%（原話："the Chili's operating margins are over 18%"）
- 2026-09-17｜Mika Ware｜margin：G&A 約占營收 4%，無具體下調指引（原話："you guys see us stay around that 4% of revenues"）
- 2026-09-17｜Kevin Hochman｜margin：10.99 美元價位僅占 9% 的帳單（原話："it's only like 9% of checks"）
- 2026-09-17｜Kevin Hochman｜margin：EDLP 使人均客單低於 CDR 同業 3–4 美元（原話："$3 to $4 less on a per person average than our competitors"）
- 2026-09-17｜Mika Ware｜commitment：資本支出路徑：今年中位 2.75 億，後續 3.5 億再 4 億（原話："I would ramp that up to $350 million and then $400 million"）
- 2026-09-17｜Mika Ware｜capital_allocation：年度股數減少目標 3%–5%，由超額自由現金流支應（原話："our goal will be to reduce our shares by 3% to 5% annually"）
- 2026-09-17｜Mika Ware｜capital_allocation：槓桿目標：租賃調整後槓桿維持 2 倍以下（原話："our target is to keep it at less than 2x"）
- 2026-09-17｜Mika Ware｜capital_allocation：股利：現在不做，未來會再討論（原話："I'm not saying never. I'm just saying not right now."）
- 2026-09-17｜Mika Ware｜capital_allocation：租賃調整後槓桿由 3.7 倍降至 1.4 倍（原話："we took our lease adjusted leverage from 3.7x to 1.4x"）
- 2026-09-17｜Mika Ware｜capital_allocation：去年自由現金流 5.58 億美元（原話："last year, we delivered $558 million"）
- 2026-09-17｜Kevin Hochman｜capital_allocation：資本配置重心由還債轉為投資與買回（原話："our capital allocation will shift from paying down debt"）
- 2026-09-17｜Kevin Hochman｜capital_allocation：每年 reimage 資本支出超過 6,000 萬美元（原話："spending over $60 million a year in capital on reimages"）
- 2026-09-17｜Mika Ware｜commitment：新店節奏：2029 財年達每年 30 家（原話："ramp up to 30 units per year by F '29"）
- 2026-09-17｜Mika Ware｜commitment：新店成長率目標 2%–3%／年（原話："the pace that we want to go is 2% to 3% new units per year"）
- 2026-09-17｜Mika Ware｜commitment：新店單位投資額 500–600 萬美元（原話："going to be between $5 million and $6 million"）
- 2026-09-17｜Mika Ware｜commitment：F28 已核准 15 家新店（原話："we already have 15 units approved and ready to go for F '28"）
- 2026-09-17｜Mika Ware｜commitment：Reimage 目標 F28 達系統 10%（原話："our plan is to ramp up to 10% of the system in F '28"）
- 2026-09-17｜Mika Ware｜commitment：轉 reimage 到 F28 預計每年約 110 家，歷史最高 125 家（原話："125 is the most we've been able to get done in a year"）
- 2026-09-17｜Mika Ware｜commitment：管理層表示不縮小新店面積，新原型反而更大（原話："no plans for smaller ones. Not this time."）
- 2026-09-17｜Aaron White｜commitment：擬在 12–24 個月內推出股票薪酬計畫（原話："we are looking and evaluating a stock comp program"）
- 2026-09-17｜Mika Ware｜commitment：新店審慎擴張，不為追量核准次級地點（原話："not feel pressured to approve any subpar sites"）
- 2026-09-17｜Mika Ware｜product：早期 16 家 reimage 店銷售提升 3%–5%（原話："we are getting a 3% to 5% sales lift"）
- 2026-09-17｜Mika Ware｜product：Reimage 平均每家花費約 60 萬美元（原話："the average spend is $600,000 per unit"）
- 2026-09-17｜George Felix｜product：Triple Dipper 占 Chili's 總銷售 16%（原話："that one item alone now makes up 16% of Chili's total sales"）
- 2026-09-17｜George Felix｜product：管理層稱 Triple Dipper 未見退燒（原話："We have seen no signs of the triple dipper fading"）
- 2026-09-17｜George Felix｜product：Big Crispy 年化後預期成為 2.2 億美元以上品類（原話："going to be over $220 million category"）
- 2026-09-17｜George Felix｜product：Mexican QSR 為下一個目標品類，預計約 2 年後（原話："We're probably not even doing this in the next 12 months."）
- 2026-09-17｜Kevin Hochman｜product：菜單約 40% 尚待翻新（原話："We have 40% left."）
- 2026-09-17｜Kevin Hochman｜product：Maggiano's 義大利麵份量增加 20%（原話："20% more portions to all of our pasta dishes"）
- 2026-09-17｜Kevin Hochman｜product：Maggiano's 份量調整已納入現行財測（原話："That's all baked into the current guidance that you have."）
- 2026-09-17｜Kevin Hochman｜customer：新 token 約占 60%，管理層以此說明可持續 comp（原話："That represents about 60% of the tokens that we see are new."）
- 2026-09-17｜Kevin Hochman｜customer：新客在 9–12 個月內行為近似既有客（原話："they look a lot like existing guests"）
- 2026-09-17｜George Felix｜customer：Gen Z 占客群約 25%（原話："Gen Z is now making up about 25% of our total guest mix"）
- 2026-09-17｜Aaron White｜customer：每店每週客數目標 4,300（原話："Our goal is at 4,300."）
- 2026-09-17｜Aaron White｜customer：客數由 4,300 的目標對應約 2% 同店銷售（原話："and that's an additional 2% in same-store sales"）
- 2026-09-17｜Aaron White｜customer：2000 年代初同棟建築歷史高峰每週 5,200 人（原話："Our largest guests per week was an average of 5,200."）
- 2026-09-17｜Aaron White｜customer：出餐時間達標店僅 40%，目標 65%（原話："Only 40% of our system today are actually at our goals"）
- 2026-09-17｜Aaron White｜customer：小時工離職率降至 84%，首次回到業界平均（原話："declined to 84%"）
- 2026-09-17｜George Felix｜competition：管理層稱價格下殺未拖慢 Chili's（原話："It hasn't slowed Chili's down."）
- 2026-09-17｜Kevin Hochman｜competition：競爭對手開店只造成短期分流（原話："it's going to all snap back and it does."）
- 2026-09-17｜Kevin Hochman｜competition：管理層稱休閒餐飲價值感首度追平 QSR（原話："people think casual dining is as good a value as QSR"）
- 2026-09-17｜Kevin Hochman｜competition：管理層稱獨立餐廳目前在搶市占（原話："right now, I think independents are winning"）
- 2026-09-17｜George Felix｜competition：酒類份額為產業第一（原話："we are now the #1 alcohol share brand in the entire industry"）
- 2026-09-17｜Kevin Hochman｜competition：Maggiano's 約占獲利 3%（原話："It's about 3% of profitability."）
- 2026-09-17｜Kevin Hochman｜competition：Maggiano's 營運指標改善，財務與客流尚未反映（原話："not seeing it necessarily in the financials"）
- 2026-09-17｜Kevin Hochman｜competition：近 2–3 年聚焦 Chili's，之後可能重新看組合／併購（原話："that can change 2 to 3 years from now."）
- 2026-09-17｜Kevin Hochman｜risk：管理層稱體驗改善仍在中段（原話："we're still middle innings on improving this experience"）
- 2026-09-17｜George Felix｜risk：管理層承認消費者承壓、油價偏高（原話："We know the gas prices are high."）
- 2026-09-17｜Mika Ware｜risk：FY27 營收成長與 3 年目標的關係，CFO 稱因同店基準尚在摸索（原話："we're just trying to figure out, does this thing ever settle"）
- 2026-09-17｜Aaron White｜risk：只有 50% 餐廳（原文寫 15%）達歷史客流高峰，管理層仍視為成長空間（原話："only 50% of our restaurants, so 15% that are actually"）

### 問答異常語氣（迴避／改口／保留）
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Brian Vaccaro（Raymond James）：請提供 Q1 迄今 Chili's 同店或給個護欄｜答法：未給數字，僅說比 Q4 的 6% 高，並稱待季末再談 Q1 結果
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：John Ivankoe（JPMorgan）：FY27 每間改裝的單店成本落在哪｜答法：稱數字仍在定案，只重申整體 $60–80M 與資本支出上調，細節延到投資人日
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Andrew Charles（TD Cowen）：12 家加盟店收購價格是多少｜答法：未給收購價，只說拿到很好的價格，細節之後再說
- EAT_Q4_2026_Earnings_Call_20260812.md｜問：Andrew Strelzik（BMO）：若薪酬改制能帶來更多流通，為何利潤率起點仍是 20–40bp｜答法：回答以通膨、低端定價與保守假設為由，並說明年中若銷售超預期可能優於財測，未接受流通提升的說法
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Fadem：是否估算過獨立餐廳市場規模／從獨立餐廳取得份額｜答法：答「We have not. We don't look at it that way.」，未給數字
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Binshtok：家庭客群目前占比與成長速度｜答法：CEO 稱不追蹤該區塊、沒有數據，改談社群與 Gen Z
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Chris O'Cull：Chili's 是否出現更多用餐情境｜答法：CMO 稱沒有硬數據，僅以質化的社群例子回答
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：未具名分析師：快 5–10 分鐘出餐對同店／AUV 的貢獻｜答法：CEO 稱難以量化，改以經理刷卡等例子說明
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Vaccaro：用餐時長過長的訪客占比｜答法：COO 稱沒有占比數字，只給平均約 50 分鐘
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Carril：FY27 營收成長 6–8% 對比 3 年目標 4–6% 是否保守｜答法：CFO 未直接確認保守與否，改說仍在摸索新的同店常態值、2–3% 為基本情境
- EAT_Analyst_Investor_Day_Brinker_International_Inc_20260917.md｜問：Andrew Charles：North of 6 的 400 bps 差距會實現多少｜答法：CFO 未給比例，稱不一定走到 400、不知天花板

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 4 |
| turnaround_catalyst_timeline | found | 2 | 3 |
| turnaround_liquidation_floor | found | 2 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：Brinker International 10-K customer concentration risk no single customer
- **substitute_technology**（none）：Brinker International Chili's technology disruption risk 2026；restaurants alternative technology disruption AI ordering robots delivery 2026 casual dining

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260711","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Chili's 份額增益是結構性（營運＋價值架構搶市），非純 lapping 的數學回歸","columns":{"2Y 驗證點":"同店續守 ≥ MSD 且跑贏產業","5Y 驗證點":"穿越一次消費放緩仍守正同店","10Y 驗證點":"Chili's 維持休閒正餐份額領先地位","具體數字門檻":"FY26-28 每季同店 ≥ +2%、vs 產業價差 ≥ +200bps","來源":"公司 Q3 FY26 8-K／法說（跑贏產業 420bps）","漂移觸發":"連 2 季同店 &lt; +2% → 削弱"}},{"id":"H2","text":"margin 恢復可守——OM ~10%＋餐廳層利潤率不因價值促銷回吐","columns":{"2Y 驗證點":"合併 OM 守 ≥ 9.5%","5Y 驗證點":"through-cycle OM ≥ 8%","10Y 驗證點":"規模＋供應鏈使 margin 結構性高於轉機前","具體數字門檻":"餐廳層 flow-through ≥ 10%；合併 OM FY26 ~10%","來源":"公司財報（FY25 OM 10.3%；Q3 flow-through ~14%）","漂移觸發":"flow-through 連 2 季 &lt; 10% → 削弱"}},{"id":"H3","text":"去債＋回購把 EPS 往上頂，估值對 DRI/TXRH 折價溫和收斂","columns":{"2Y 驗證點":"FY27 EPS ≥ $12、股數續縮","5Y 驗證點":"forward PE 站穩 14-16x","10Y 驗證點":"股東總回報（回購＋潛在復股息）持續","具體數字門檻":"年淨回購 ≥ 2%、FY27 共識 ≥ $12；折價由 ~40% 收至 ~30%","來源":"公司回購揭露（FY26 前三季 $343M）＋同業倍數","漂移觸發":"FY27 共識連 3 月 &lt; $11.50 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"同店大幅減速／轉負（消費放緩＋lapping tough comp）","columns":{"對應假設":"H1+H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Chili's 季度同店、量/價拆分","警戒閾值":"任一季轉負 ＝ 撤退；連 2 季 &lt; +2% ＝ 減碼／重評"}},{"id":"R2","text":"TXRH/DRI/Fast-casual 持續搶流量，Chili's vs 產業價差縮窄；價值促銷侵蝕餐廳層 margin","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Black Box 月度流量、TXRH/DRI 季度同店、Chili's flow-through","警戒閾值":"價差連 3 月 &lt; +200bps ＝ 護城河侵蝕；flow-through 連 2 季 &lt; 10%"}},{"id":"R3","text":"牛肉超級週期／勞動通膨壓制餐廳層 margin；單一品牌集中風險（Chili's ~88%）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"牛肉現貨/期貨、最低工資立法、餐廳層 OM 趨勢","警戒閾值":"餐廳層 OM 自高位回落 &gt; 200bps 且無定價對沖"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","irr_base_pct":7.0,"ev5y_pct":22.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":22.8,"irr_base_pct":7.0,"max_dd_pct":-46.0,"bull_5y_price":319.0,"bear_5y_price":104.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","price_at_dd":185.26,"archetype":"轉機/特殊情境","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"EAT","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Brinker International, Inc."},"oneliner":"Chili's 靠天天低價套餐加營運改善，連三年雙位數同店、客流連12季贏產業，轉機已到後段；現價約FY2027共識15.5倍，基本情境五年年化約7%，生意變好但價格已反映大半，續抱等回檔再加。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺美國中價位用餐客的錢：Chili's 以10.99美元套餐等天天低價把速食客拉進門，再靠出餐與服務改善留住。錢卡在「客流」這一節點：客流占同店三分之二，撐起營業槓桿，客流一斷利潤率就回吐。","reasoning":"Q1 FY27 營收14.756億美元、GAAP營業利益1.51億美元、排除其他損益後營業利益率10.4%、餐廳營業利潤率17.7%（年增150bp）。Brinker合併同店+9.1%，其中Chili's +10.1%＝客流6.4%＋價格3.7%＋組合持平；Maggiano's −3.4%（客流−5.1%）。TTM毛利率19.14%、營業利益率11.43%。分部營收占比事實表未涵蓋；投資人日（2026-09-17，CEO Kevin Hochman）稱Maggiano's約占獲利3%，所以Chili's是唯一承重分部，全集團約97%獲利繫於單一品牌。收錢方式以自營門店內用為主，外帶約四分之一（外送、自取各約12.5%，Q1 FY27法說CEO）；Triple Dipper一項占Chili's銷售16%（投資人日CMO George Felix）。單點依賴屬集中度風險，不是護城河證據。產業時鐘判IV收縮：休閒餐飲自2022年淨店數−3.3%，約9%全服務餐廳2026年有倒閉風險，NRA把2026實質餐飲成長由1.3%下修至0.8%。產業正在出清供給，存活的規模業者受惠。供需持久性方面，供給收縮是結構性的，需求則是週期性走弱，兩者相抵：份額可以延續，但總量不長。產業態勢三軸：A競爭面，同業開始複製社群行銷與價值套餐（CEO稱已有競爭者成功）；B結構面，供給出清，速食漲價使休閒餐飲的價值感追平速食，屬轉好；C其他面，關稅、運費與時薪成本上升。裁決為雙向拉鋸。類型仍判轉機/特殊情境（後段），次要類型為品質複利成長。利潤率修復、去槓桿、高息債贖回三件轉機工作已完成，但目前盈餘水準是否已正常化，還沒經過一次消費下行的檢驗。","fact_refs":["f_kpi0_total_revenues_gaap","f_kpi1_operating_income_gaap","f_kpi2_operating_margin_excl_ot","f_kpi3_restaurant_operating_mar","f_kpi7_comparable_restaurant_sa","f_kpi8_guidance_fy2027_total_re","f_kpi9_guidance_fy2027_adjusted","f_peer_eat_gross_margin_pct","f_peer_eat_operating_margin_pct"],"verdict_values":{"revenue_quality":"營收幾乎全來自自營門店（內用約75%、外帶約25%），Chili's為主體，Maggiano's約占獲利3%。同店由客流帶動（約三分之二），價格只取3–5%區間低端，品質高於靠漲價撐同店的同業。分部營收占比與加盟收入事實表未涵蓋。","unit_econ_note":"餐廳營業利潤率17.7%（Q1 FY27，年增150bp）。新店每家投資500–600萬美元，目標每年30家；改裝每家50–60萬美元，帶來3–5%營收提升，CFO稱目前只打平資金成本。North of 6門店利潤率比全系統高400bp，但只占約20%。","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"營業利益率由FY23的4.28%回升到FY26的10.82%，租賃調整後槓桿由3.7倍降到1.4倍，8.25%高息債已贖回，資本配置由還債轉向回購與開店；盈餘是否正常化，還要等一次消費下行來檢驗。"},"industry":{"clock_phase":"IV","sd_verdict_source":"休閒餐飲淨店數自2022年−3.3%，同期速食+5.8%、快休閒+15.5%（Black Box，2026-02）；NRA 2026-07中期更新下修2026實質餐飲成長至0.8%；Black Box預估2027銷售小幅成長、客流大致持平。判讀：供給結構性收縮，需求週期性偏弱。","bargaining":{"up":"上游是商品型食材（雞、牛、乳製品、蔬果）、運費與時薪。公司有採購規模，但仍是價格接受者：Q1 FY27商品通膨3.3%、時薪通膨約2.6%，10-K也點名關稅可能推高成本。","down":"下游是分散的個人消費者，轉換成本為零，議價權在消費者手上；公司選擇用低價換客流，而不是靠漲價取利。","geo":"營運集中在美國本土，國際以加盟為主，金額事實表未涵蓋；地緣風險主要經由進口食材關稅傳導。"},"profit_pool_dir":"利潤池由弱勢休閒餐飲業者往執行力強的規模品牌集中；管理層也承認獨立餐廳目前在搶份額。5年前與現在的利潤池占比數字事實表未涵蓋。","tam_table":{"expanded":false,"reason":"成長來自成熟且店數萎縮的品類內搶份額，加上每年2–3%開店，不屬低滲透、新品類或利潤池遷移情境；休閒餐飲市場規模與利潤池占比數字事實表未涵蓋。"}}}},"q2_moat":{"verdict":"護城河方向穩定、等級B。執行面在擴大：領先產業幅度由420bp拉到720bp，客流連12季贏產業。定價面只算穩定：人均消費價差被第三方更正為比原說法窄，10月客單組合轉負。合併判穩定。","reasoning":"機制是全國廣告規模＋天天低價菜單架構（3 for Me約占21%、10.99美元套餐約占帳單9%）＋營運簡化與人力配置，形成相對價值優勢。這種優勢靠執行維持，不是轉換成本或網路效應。\n\n可證方向用份額軸：Chili's同店領先休閒餐飲產業，Q3 FY26為420bp，Q1 FY27擴大到720bp，客流已連12季贏產業（法說CEO）。\n\n同業ROIC事實表未涵蓋，改用利潤率當代理。EAT TTM營業利益率11.43%，DRI 12.18%、TXRH 7.86%、CMG 14.95%；FCF利潤率EAT 11.11%，高於DRI 7.64%、TXRH 6.43%；MCD以加盟權利金為主（營業利益率45.71%），不可直接比。EAT自身營業利益率由FY23 4.28%升到FY26 10.82%（財務歷史欄，年度財報），與DRI的差距在縮小，但DRI歷年數字未涵蓋，只能看單點。\n\n評分：執行8分，依據是客流領先、Google評分創新高4.3、時薪員工離職率降到84%回到產業平均。定價6分：價格+3.7%同時客流+6.4%，代表漲價沒傷到量；但公司刻意把漲價壓在3–5%低端，人均消費優勢經Black Box更正後變窄，10月起酒類與甜點的客單組合也轉負。合併約7分，等級B；未達8分，不需做同業ROIC價差檢驗。三項威脅都屬點對點，不扣分。\n\n當期ROIC粗估約25%（推導見持續期欄），屬高周轉×中高利益率。四檢查點中三項黃燈，報酬持續期取決於執行，不取決於結構。","fact_refs":["f_peer_eat_operating_margin_pct","f_peer_eat_fcf_margin_pct","f_peer_dri_operating_margin_pct","f_peer_dri_fcf_margin_pct","f_peer_txrh_operating_margin_pct","f_peer_txrh_fcf_margin_pct","f_peer_cmg_operating_margin_pct","f_peer_mcd_operating_margin_pct","f_kpi3_restaurant_operating_mar","f_net_debt_m","f_ev_m","f_ev_s_current"],"verdict_values":{"moat":{"mechanism":"全國廣告規模＋天天低價菜單架構＋營運簡化與人力配置帶來的相對價值優勢，靠執行維持，沒有轉換成本","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：領先休閒餐飲產業由420bp（Q3 FY26）擴大到720bp（Q1 FY27），客流連12季贏產業。定價面穩定：價格+3.7%未傷客流，但Black Box更正後人均消費價差比原說法窄，10月客單組合轉負。兩者合併判穩定；要升為擴大，須見產業客流轉負期間Chili's仍維持正成長。","competitor_notes":[{"name":"DRI","strategy_note":"多品牌規模採購與管理效率最強的同業，營業利益率12.18%仍略高於EAT，但FCF利潤率7.64%低於EAT的11.11%；EAT在利潤率上正在追近。"},{"name":"TXRH","strategy_note":"牛排館型高客流、重視經理留任的營運標竿；本資料源TTM營業利益率7.86%低於EAT，牛肉成本曝險較高。"},{"name":"CMG","strategy_note":"快休閒，營業利益率14.95%，與Chili's爭奪年輕客群與外帶；快休閒自2022年淨店數+15.5%，是休閒餐飲流失份額的去處之一。"},{"name":"MCD","strategy_note":"加盟權利金模式使利潤率（45.71%）不可直接比；它是Chili's廣告直接對比的價值標靶。速食漲價縮小價差讓Chili's受惠，速食若重啟價格戰，則是主要外部威脅。"}],"peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，以營業利益率與FCF利潤率代理","threats":[{"level":"🟡","text":"同業複製社群爆紅＋價值套餐打法，CEO已點名有競爭者做得成功；若對手營運也到位，Chili's領先產業的幅度會收窄","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"level":"🟡","text":"速食重啟價格戰，使休閒餐飲剛追平速食的價值感再度落後","p":"30%","evidence_refs":["supply_demand_durability#4"]},{"level":"🟡","text":"商品（含關稅）、運費與時薪通膨推升成本，而公司刻意把漲價壓在區間低端，價值架構的利潤緩衝變薄","p":"35%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]}],"roic_durability":{"quadrant":"高周轉×中高利益率","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一位用餐客，三個角色一致；但外食屬想要而非需要，延後的代價低。消費承壓下客流仍+6.4%，顯示價值定位在消費降級時受惠；不過10月起酒類與甜點的客單組合轉負，需求韌性只在客流端成立。"},{"item":"決策層級","level":"🟡","text":"替代性要在「今晚吃哪裡」這一層衡量：速食、快休閒、超市熟食、外送都可替代，轉換成本為零。代理讀數方面，價格+3.7%後客流仍+6.4%，沒有漲價流失；新客約占60%，並在9–12個月內行為接近舊客（投資人日）。優勢靠持續執行，不是靠鎖定客戶。"},{"item":"價值鏈分配","level":"🟡","text":"食材、運費與時薪是主要的外部分配者，公司是價格接受者；外送平台分走外送那段約12.5%營收的部分利潤；部分門店自有不動產，降低房東分得的份額。10-K點名關稅可能推高成本，並限制以定價保護利潤率。目前靠銷售槓桿吸收，Q1 FY27餐廳利潤率仍年增150bp。"},{"item":"社會容忍度","level":"🟢","text":"平價外食不依賴任何授權，公司主動把價格壓在低端，沒有逼近社會容忍上限。需留意的是最低工資與小費抵稅（FICA tip credit）等政策變動對人力成本的影響；具體立法進度事實表未涵蓋。"}],"roiic":11,"reinvest_rate":15,"endo_ceiling":1.7,"formula_note":"單位皆為%。當期ROIC粗估約25%：稅後營業利益率＝TTM營業利益率11.43%×（1−19%調整後稅率）≈9.3%；投入資本周轉率＝TTM營收約59.5億美元（企業價值105.8億美元÷企業價值營收比1.78倒推）÷投入資本約22.1億美元（權益4.437億＋淨負債17.68億，後者含租賃負債）≈2.7倍。偏差方向：淨負債含租賃、但營業利益已扣租金，會低估ROIC；權益因多年回購偏低，會高估。增量ROIC約11%：新店每家500–600萬美元、餐廳營業利潤率約17.7%，換算稅前現金報酬約15%上下，扣稅與分攤後約11–12%；改裝CFO稱目前只打平資金成本。再投資率約15%：FY27資本支出中值2.75億美元−折舊攤提約2.39億（3.8%×營收指引中值62.8億）＋加盟店收購約0.275億≈0.64億，除以稅後營業利益約5.8億≈11%；FY28至FY29資本支出升到3.5億、4億後約20%，取中值約15%。營運資金變動事實表未涵蓋，假設為0。內生成長上界≈11%×15%≈1.7%/年。"}}}},"q3_growth":{"verdict":"五年後跑道中等：在成熟且店數萎縮的品類裡靠搶份額，加上FY29起每年2–3%開店，目前沒有已證實的第二條成長曲線。","reasoning":"成長組成：Q1 FY27 Chili's同店10.1%中，客流6.4%、價格3.7%、組合持平。FY27後三季指引回到中個位數同店、客流為正。投資人日的三年框架為營收年增4–6%（同店2–3%、新店2–3%）、每年減股3–5%、每股盈餘雙位數成長。\n\n三年共識：FY2026A GAAP稀釋每股盈餘10.87美元（財務歷史欄）→FY2029E 16.45美元，CAGR約14.8%。但基期是GAAP、共識是調整後，且FY2027含第53週約0.70美元；去除後FY2027約12.98美元→FY2029E 16.45美元，CAGR約12.6%，以後者為準。\n\n內生成長上界約1.7%/年（增量ROIC約11%×再投資率約15%，推導見持續期欄）。共識與上界的缺口約11pp，歸因如下：利潤率擴張與既有門店同店帶來的營業槓桿約5–6pp、淨回購約4pp、收購0、無法歸因約1–2pp。成長主要靠不需新增資本的同店與回購，屬高ROIC、低再投資空間的形狀，信心上限為中。\n\n跑道：管理層稱門店只用到歷史客流容量約80%，每店每週客數目標4,300人約可再帶來2%同店，份額跑道約5年；新店有300個以上商圈、每年約30家，約可走10年。五年後的跑道無法用滲透率衡量，以無第二曲線、品類不成長判為中等。\n\n衰退訊號亮兩項：每股盈餘成長遠高於營收（FY23→FY26每股盈餘2.28→10.87美元，營收41.3→58.1億美元）、品類店數萎縮。其餘未亮：毛利率連升，FCF/淨利FY25 1.08倍、FY26 1.14倍，SBC占營收0.56%。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_comparable_restaurant_sa","f_kpi9_guidance_fy2027_adjusted","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_stock_based_compensation"],"verdict_values":{"growth":{"driver_mix":"量為主：客流約占同店三分之二、價格約三分之一；每股盈餘另加淨回購3–5%與利潤率每年20–40bp；新店FY29起每年貢獻2–3%","runway_years":"份額約5年、新店約10年","runway_post_y5":"🟡","endo_ceiling_basis":"增量ROIC約11%（新店每家500–600萬美元、餐廳營業利潤率約17.7%換算；改裝目前只打平資金成本）×再投資率約15%（FY27至FY29資本支出由2.75億升到4億美元，扣折舊攤提與加盟店收購後，除以稅後營業利益）≈1.7%/年","segments":{"expanded":false,"reason":"分部營收占比事實表未涵蓋；Maggiano's約占獲利3%（投資人日），論點全由Chili's承擔，分部組合不決定利潤走向。"},"decay_signals":[{"item":"毛利率連2季年減","lit":false,"note":"Q1 FY27餐廳利潤率年增150bp"},{"item":"核心市占近12個月縮減","lit":false,"note":"領先產業720bp"},{"item":"提價後銷量下滑","lit":false,"note":"Chili's價格+3.7%、客流+6.4%；Maggiano's價格+2%、客流−5.1%，但只占獲利約3%"},{"item":"每股盈餘成長顯著高於營收成長","lit":true,"note":"FY23→FY26每股盈餘年化約68%、營收約12%；往後共識每股盈餘約12%，對營收4–6%"},{"item":"FCF/淨利連2年低於0.75","lit":false,"note":"FY25 1.08倍、FY26 1.14倍"},{"item":"SBC/營收高於5%且上升","lit":false,"note":"0.56%"},{"item":"TAM萎縮或被替代","lit":true,"note":"休閒餐飲淨店數自2022年−3.3%，客流多年未成長"},{"item":"產業估值倍數近3年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維持性資本支出占FCF高於60%","lit":false,"note":"FY27資本支出2.65–2.85億美元，對FCF約5.5億，維持性部分低於一半"},{"item":"停止新產能且收入3年內下滑","lit":false,"note":"新店FY28加速"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金流強，用途已轉向回購：FY26自由現金流約5.58億美元、為淨利1.14倍，SBC只占營收0.56%。回購是否買得划算，因回購均價與10年期公債殖利率事實表未涵蓋，無法下定論。","reasoning":"FCF/淨利：FY25 1.08倍（4.137億÷3.831億）、FY26 1.14倍（5.575億÷4.87億）。SBC：Q1 FY27為830萬美元，占營收0.56%、占GAAP營業利益5.5%。\n\n現金去向：FY26全年分項事實表未涵蓋。已知的有：Q4 FY26回購1億美元；Q1 FY27回購1.25億美元，高於當季FCF 1.057億，差額由循環信貸支應（Q1末循環信貸餘額3.75億）；8月董事會加碼授權至7.5億美元；以循環信貸贖回3.5億美元8.25%票據，換成較低利率，屬再融資而非還債；12家加盟店收購約0.275億美元；不發股利（投資人日CFO：現在不做）。\n\n槓桿：租賃調整後由3.7倍降到1.4倍，目標低於2倍；目前淨負債17.68億美元（含租賃）。營運槓桿：FY26營收+7.86%、營業利益約+13%（5.54億→6.28億，以年度營業利益率換算），屬擴張而非壓縮。\n\n計分卡：\n- 併購報酬：不適用，金額約市值0.3%，也沒有實現報酬揭露。\n- 回購收益率：以判斷日前瞻本益比15.5倍換算約6.4%，若10年期殖利率低於約4.4%即通過；殖利率事實表未涵蓋，故不判。\n- SBC淨稀釋：約為市值0.4%/年，且股數淨減，通過。","fact_refs":["f_kpi5_free_cash_flow_non_gaap","f_kpi6_stock_based_compensation","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"唯一收購為12家加盟店，約2,750萬美元（約市值0.3%）；CFO稱對每股盈餘影響約持平，無實現報酬揭露"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"前瞻本益比15.5倍換算回購收益率約6.4%；回購均價與10年期公債殖利率事實表未涵蓋，無法對照門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC年化約3,300萬美元、約市值0.38%，且加權股數指引42–43百萬股持續下降，淨稀釋低於1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；資本回饋以回購為主（授權7.5億美元、每季1–1.25億美元），不發股利，金額已列在計分卡與理由中"}}}},"q5_valuation":{"verdict":"現價要求FY2029每股盈餘約16.5美元、倍數守在15倍上下才划算。盈餘路徑我大致相信，但26週漲43%後，基本情境五年年化只剩約7%，價格合理偏滿，不追。","reasoning":"判斷日股價212.18美元。\n\n倍數：前瞻本益比15.51倍（FY2027共識13.68美元）；FY2027含第53週約0.70美元，去除後約16.3倍；FY2028共識14.80美元對應約14.3倍。Trailing本益比18.71倍，位於近4個年度端點的45.9百分位。股價營收比1.49倍、企業價值營收比1.78倍，分居93.6、90.1百分位；營收倍數偏高是因為利潤率由4%修復到11%，不代表貴，盈餘倍數才是主尺。五年分位事實表未涵蓋（只有4個年度端點），不外推。\n\nPEG：去除第53週後，FY2027→FY2029共識CAGR約12.6%，16.3÷12.6≈1.3，落在合理區。同業本益比事實表未涵蓋，無法做同層錨定。\n\n賣方：Jefferies目標價255美元，過去一年更新的平均目標價243.38美元（24家中19家買進），距現價約15%。\n\n共識修正：財報後FY2027共識由13.65上修到13.68美元，Chartmill顯示財報前三個月上修約6%。事實表的近三月+27%，是7月底快照仍以FY2026為FY1造成的財年換檔，不是真實上修。\n\n上檔：12個月以FY2028基本情境每股盈餘14.70美元×15.5倍＝約228美元（+7.4%）；約3年以FY2029的16.30美元×15.5倍＝約253美元（+19.1%）。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027共識，經第53週校正）為主、PEG為輔；轉機後段看正常化盈餘能力，營收倍數只作參考","peers":{"expanded":false,"reason":"事實表的同業對照只有毛利率、營業利益率、FCF利潤率，未涵蓋同業本益比與目標價，無法同層錨定；改以自身前瞻與歷史倍數為錨"},"fwd_pe":15.51,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比15.5倍（去第53週約16.3倍）、PEG約1.3、trailing本益比在4個年度端點的45.9百分位；基本情境五年年化約7%，機率加權後報酬與風險比約1.9。價格合理，但沒有便宜到能補償空方30%的機率。五年分位屬資料缺口，改用年度端點分位代替。","upside_short_pct":7.4,"upside_mid_pct":19.1,"denominator_disputed":false,"denominator_note":"FY2027共識含第53週約0.70美元（約5%），已改用去除後約12.98美元校正倍數；一次性效應沒有大到成為爭點。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是客流飛輪的持續性：若Chili's在高基期與消費承壓下出現一季客流年減，營業槓桿會反轉，每股盈餘與倍數同時下修。","reasoning":"唯一致命點與空方主線重合（客流轉負），見反證紀錄。\n\n價值陷阱判中度：衰退訊號亮兩項（每股盈餘成長遠高於營收、品類店數萎縮），屬轉機後段的正常形狀，不是盈餘品質惡化。\n\n最大回撤推導：空方情境終點約130美元（−39%）；路徑谷底以FY2029空方每股盈餘10.8美元×10倍≈108美元（−49%）；技術面回到104週均線157.58美元為−26%，回到250週均線90.31美元為−57%；26週漲43%後，回吐空間大。取範圍−55%至−30%。\n\n壓力測試三項（以FY2029兩年期、跌幅不超過5%算通過），通過1/3：\n- 四季同店持平：每股盈餘約14美元×14倍≈196美元（−8%），不過。\n- 餐廳利潤率回吐200bp：16.3−2.75＝13.55美元×15.5倍≈210美元（−1%），通過。\n- 倍數降到11倍、盈餘照基本情境：16.30×11≈179美元（−16%），不過。\n\n訴訟與監管：只有轉租違約訴訟（FY25費用170萬美元、FY26無），無集體訴訟、無SEC調查。法說迴避的問題中，最相關的是改裝報酬，以及North of 6利潤率差距能實現多少，管理層都沒給數字。","fact_refs":["f_price_at_dd","f_ma_w104","f_ma_w250","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩項衰退訊號亮燈（每股盈餘成長遠高於營收、品類店數萎縮），屬轉機後段形狀，不是價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.68,"pe":15.51,"basis":"FY2027（2027年6月止）共識每股盈餘13.68美元，含第53週約0.70美元；與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[13.95,15.6,17.7,19.9,22.2],"base":[13.6,14.7,16.3,17.8,19.3],"bear":[12.9,11.6,10.8,11.2,11.8]},"pe":{"bull":18,"base":15.5,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":3.5},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-55,"hi":-30,"basis":"空方終點11.8美元×11倍≈130美元（−39%）；路徑谷底以FY2029空方10.8美元×10倍≈108美元（−49%）；回到250週均線90.31美元為−57%。下緣−55%涵蓋谷底後再超跌；上緣−30%約等於吐回26週全部漲幅（212÷1.43≈148美元）。","trigger_time":null},"basis":{"bull":"Chili's中個位數同店延續到FY29，新店與外帶加速，餐廳利潤率每年擴張40bp以上，每年減股4–5%；倍數18倍，接近目前trailing 18.7倍","base":"FY27達指引中值13.60美元；FY28起同店2–4%、營收年增約5%、利潤率每年擴張20–40bp、每年減股約3.5%（每股盈餘路徑已含回購）；FY29約16.3美元，略低於共識16.45；倍數維持目前前瞻15.5倍","bear":"FY27下半年同店轉為持平，FY28客流轉負，營業槓桿反轉使利潤率回吐約200bp，回購放慢；每股盈餘谷底約10.8美元後緩升到11.8美元；倍數收斂到11倍（成長降到5%以下的成熟休閒餐飲）。同業倍數事實表未涵蓋，以自身現值15.5倍與trailing 18.7倍對照"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"10-K指出休閒餐飲多年客流沒有明顯成長，成長只能從同業手上搶；NRA把2026實質餐飲銷售成長由1.3%下修到0.8%；10月起客單組合轉負；Q2要對上去年11月的高基期；Chili's三年累計同店已+52%","assumption":"份額增益是可持續的營運優勢，而不是社群爆紅加價值戰造成的一段高峰","consequence":"若客流轉負，營業槓桿反轉，FY28至FY29每股盈餘可能回到11美元上下，倍數收斂到11倍，股價約120–130美元（約−40%）","ruling":"採納為空方主線，機率30%；與唯一致命點撞上，兩者一致不改動。Q2開局仍高個位數、客流占同店三分之二，一季內發生的機率不高","watch":"Chili's季度客流、領先產業幅度、法說季中同店口徑","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#0"],"fact_refs":["f_kpi7_comparable_restaurant_sa"]},{"view":"論點成功但股東經濟變差","evidence":"FY27資本支出2.65–2.85億美元，投資人日稱之後升到3.5億、4億；CFO說改裝目前只打平資金成本；新店每家500–600萬美元，報酬未揭露；10-K稱關稅與供應鏈可能推高成本，並限制以定價保護利潤率；公司刻意把漲價壓在3–5%區間低端，同時加碼人力","assumption":"客流成長能同時換到利潤率擴張與高增量報酬","consequence":"營收照長、份額照拿，但增量資本報酬掉到接近資金成本，每股盈餘成長主要靠回購；若在高倍數回購，股東實得報酬會低於帳面每股盈餘成長","ruling":"部分採納：再投資規模相對自由現金流（約5.5億美元）仍小，稀釋有限；但這是基本情境年化只有約7%的原因之一","watch":"改裝與新店報酬揭露、餐廳營業利潤率、回購均價","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"],"fact_refs":["f_kpi5_free_cash_flow_non_gaap"]},{"view":"價格已反映太多","evidence":"26週漲43%；股價營收比與企業價值營收比位於近4個年度端點的93.6、90.1百分位；前瞻本益比15.5倍含第53週約0.70美元，去除後約16.3倍；近三月共識+27%是財年換檔造成，實際上修約6%；賣方平均目標價243美元，距現價僅約15%","assumption":"市場仍低估份額增益的持續性","consequence":"就算論點成立，基本情境五年年化約7%，略低於8%的及格線；機率加權後報酬與風險比約1.9","ruling":"採納：續抱不追，等回落到185美元附近（約13.5倍）再加","watch":"股價對FY2027共識的倍數、FY2028共識是否再上修","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"2026-10-28 Q1法說CEO揭露：Black Box告知產業人均消費基準有誤，Chili's仍較低，但差距比過去引用的3–4美元窄，新數字11月更新","assumption":"天天低價的價值領先幅度夠大，足以在同業複製時守住客流","consequence":"若價差縮到1美元以內，客流領先主要靠營運與行銷，定價面優勢接近消失；同業一旦跟進價值套餐，領先產業的幅度會快速收窄","ruling":"部分採納：定價分維持6不升，護城河方向不升為擴大，等11月資料再定","watch":"Black Box 11月更新、Chili's領先產業幅度","evidence_refs":["competitive_share_entrants#2"],"fact_refs":["f_kpi7_comparable_restaurant_sa"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 185.26 → 本次 212.18（+14.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=185.26","side_b":"本次 price_at_dd=212.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 185.26 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 185.26 美元：Bull 價 319、Bear 價 104，五年期望值 +22.8%，基準年化 7.0%，不對稱比 1.4","side_b":"本次情境、股價仍用 185.26 美元：Bull 價 399.6、Bear 價 129.8，五年期望值 +47.6%，基準年化 10.1%，不對稱比 3.22","ruling":"先換情境、股價不動：五年期望值多 24.8 個百分點，基準年化多 3.1 個百分點。不對稱比由 1.4 變為 3.22。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 185.26 美元：五年期望值 +47.6%，基準年化 10.1%，不對稱比 3.22","side_b":"本次情境、股價 212.18 美元：五年期望值 +28.9%，基準年化 7.1%，不對稱比 1.9","ruling":"再換股價、情境不動：起點價上漲 14.5%，五年期望值少 18.7 個百分點，基準年化少 2.9 個百分點，不對稱比由 3.22 降到 1.9。合計五年期望值比前份多 6.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"份額增益是結構性還是高峰","cause":null,"side_a":"管理層（2026-10-28 Q1 FY27法說，CEO Kevin Hochman）：客流連12季贏產業，三年累計同店+52%，新客約60%並轉為常客，Q2開局高個位數，飛輪可持續","side_b":"10-K：休閒餐飲多年客流不長，成長只能靠搶份額；NRA下修2026實質餐飲成長至0.8%；10月客單組合轉負，11月要對上去年高基期；Big Crispy Parm每店每日約2份，低於預期","ruling":"可調和，屬程度差異：份額增益真實，但速度會回到指引的中個位數；基本情境略低於共識，空方30%即為此風險定價","evidence_level":"中（公司自報＋第三方產業資料）","settle_metric":"Chili's Q2 FY27同店與客流（2027年1月公布）","if_then":["若Q2 FY27 Chili's同店不低於+4%且客流為正：維持基本情境，股價不高於185美元時分批加碼","若任一季Chili's客流年減：減碼一半；下一季同店也轉負且餐廳利潤率年減則清倉","若股價先漲、證據未到（Q2財報前漲破240美元）：不追"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","supply_demand_durability#3","end_markets#2"]},{"axis":"近三月共識上修的口徑","cause":null,"side_a":"事實表顯示近三月FY1共識由10.76上修到13.68美元（+27%）","side_b":"7月30日快照時FY2026尚未公告，仍被當成FY1（10.76美元與FY2026實際GAAP每股盈餘10.87美元相近），屬財年換檔；Chartmill 10月17日顯示FY2027共識三個月上修約6%，財報後再由13.65上修至13.68美元","ruling":"採B側：真實上修約6%，盈餘動能不以27%計；這也是不把盈餘動能當加碼理由的原因之一","evidence_level":"高（兩個獨立來源口徑可對上）","settle_metric":"下一份共識快照的FY2027與FY2028數字","if_then":[],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#1"]},{"axis":"管理層利潤率說法前後對照","cause":null,"side_a":"2026-08-12 Q4 FY26法說CFO Mika Ware：FY27餐廳利潤率以52週計改善20–40bp，轉型後利潤率成長會趨緩；2026-09-17投資人日重申長期每年20–40bp","side_b":"2026-10-28 Q1 FY27法說CFO：FY27改善70–90bp（含第53週約30bp），Q2約持平，Q3回到20–40bp，Q4因番茄、生菜基期有上檔","ruling":"可調和：上修來自Q1超預期與商品基期，長期說法沒變；情境樹基本情境採每年20–40bp，不外推FY27的幅度","evidence_level":"高（逐字稿）","settle_metric":"FY27第2季餐廳營業利潤率年變化（指引約持平）","if_then":[],"evidence_refs":[]},{"axis":"價值領先的量化幅度","cause":null,"side_a":"2026-08-12 Q4法說與2026-09-17投資人日，CEO稱Chili's人均消費比競爭者低3–4美元","side_b":"2026-10-28 Q1法說CEO：Black Box告知產業人均消費基準有誤，Chili's仍較低，但差距比原先說法窄，新數字11月更新","ruling":"採B側：定價分維持6不升；若11月更新後差距不到1美元，定價分降到5，合併分降到約6.5，護城河等級可能降為C","evidence_level":"中（尚待更新資料）","settle_metric":"Black Box 2026年11月更新的休閒餐飲人均消費基準","if_then":["若更新後價差不低於2美元：定價面維持穩定","若更新後價差低於1美元：重估護城河等級，暫停加碼，直到下一季客流確認"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"客流連12季領先、指引上修、Q2開局高個位數；管理層財測歷來偏保守（2026-08-12 CEO：每年起始財測都被超越）；前瞻本益比15.5倍低於自身trailing 18.7倍；每年減股3–5%；若同店守住中個位數，FY2029每股盈餘可能高於共識16.45美元，股價可能不再回到185美元","side_b":"26週已漲43%，財報當日漲約13%；基本情境五年年化約7%，低於8%；空方機率30%，報酬與風險比約1.9；共識實際上修只有約6%","ruling":"不採A側為立即加碼理由，但保留證據先到的分支","evidence_level":"中","settle_metric":"Q2、Q3 FY27同店與FY2028共識","if_then":["若股價未回落，而Q2、Q3 FY27同店均不低於+4%且FY2028共識再上修5%以上：以目標倉位1/3小量加回","若股價回落到185美元以下而客流仍為正：分批加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"評等、估值與陷阱判讀的前後對照","cause":"新證據","prior_field":["signal","val","trap"],"side_a":"前份（2026-07-11，股價185.26美元）：綜合評等B級、估值合理、價值陷阱風險中等","side_b":"本次三欄維持同值：Q1 FY27同店+10.1%、指引上修、FY2027共識13.68美元（前份門檻為12美元），盈餘基礎上移；但股價同步上漲約14.5%，前瞻倍數仍約15.5倍；陷阱訊號仍是兩項","ruling":"三欄不變；盈餘上修與股價上漲大致抵銷","evidence_level":"高","settle_metric":"FY2027實際每股盈餘對指引中值13.60美元","if_then":[],"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0"]},{"axis":"護城河方向、跑道與類型","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河方向穩定、五年後跑道中等、類型為轉機/特殊情境、未標循環位置","side_b":"本次維持四欄。執行面因領先產業由420bp擴大到720bp而轉強，但Black Box人均消費價差被更正變窄，合併仍判穩定；投資人日公布每年2–3%新店與300個商圈，仍不是第二條成長曲線；轉機三件工作已完成，但盈餘正常化未經消費下行檢驗，類型維持；非商品循環股，不標循環位置","ruling":"四欄不變；若產業客流轉負期間Chili's仍維持正成長，護城河方向升為擴大，類型改為品質複利成長","evidence_level":"中","settle_metric":"下一次產業客流轉負季度的Chili's客流","if_then":[],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"機率與最大回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭25%、空頭30%、最大回撤−46%","side_b":"本次多頭25%、空頭30%不變；最大回撤改為−55%至−30%的範圍。下緣加深，是因為股價由185.26美元漲到212.18美元，與250週均線90.31美元的距離拉大到−57%","ruling":"機率不變，因基本面上修已被價格吸收；回撤下緣隨價格上移而加深","evidence_level":"高","settle_metric":"股價與250週均線距離","if_then":[],"evidence_refs":[]},{"axis":"裁決與角色","cause":"價格變動","prior_field":[],"side_a":"前份：進場、衛星角色","side_b":"本次結論改為續抱不追、等回落到185美元附近再加：股價漲14.5%，基本情境年化仍只有約7%。最終裁決與角色由決策矩陣依本次輸入重算","ruling":"約束來自價格，不是論點；論點比前份更扎實","evidence_level":"高","settle_metric":"股價對FY2027共識倍數","if_then":[],"evidence_refs":[]},{"axis":"加碼條件改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","side_b":"股價不高於185美元（FY2027共識約13.5倍）且最近一季Chili's客流為正，才恢復分批加碼；客流轉負先減碼一半，同店轉負且利潤率年減才清倉","ruling":"前份加碼條件已兌現（Q4 FY26 Chili's同店+5.6%，FY27指引10月上修），但股價已先漲。現在的約束是價格，所以新加碼條件改為價格錨加客流確認；撤退條件拆成兩段：減碼看客流、清倉看同店與利潤率","evidence_level":"高","settle_metric":"股價、Chili's單季客流","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"Single Thing（唯一致命點）由未設定改為客流轉負","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"Chili's出現第一季客流年減，客流帶動同店的飛輪斷裂","ruling":"依敏感度設定：客流占同店三分之二，同店每少5個百分點，每股盈餘約少2美元，是數學上最大的單一敏感項；觸發時減碼一半，確認後清倉","evidence_level":"中","settle_metric":"Chili's單季客流","if_then":[],"evidence_refs":["supply_demand_durability#3"]},{"axis":"清倉與減碼門檻更新","cause":"新證據","prior_field":["kill_metrics","thesis.R","thesis.H"],"side_a":"前份：未設kill metrics；R1任一季同店轉負＝撤退、連2季低於+2%＝減碼；R2價差連3月低於+200bps；R3餐廳層利潤率自高位回落超過200bps；H3以FY27共識連3月低於11.50美元為反轉","side_b":"本次：客流任一季低於0%＝減碼一半；同店低於0%且餐廳利潤率年減＝清倉；領先產業連2季低於200bp＝停止加碼；餐廳利潤率連2季年減超過50bp＝減碼1/3；租賃調整後槓桿超過2倍＝重評回購；H3改為年淨減股不低於3%且槓桿低於2倍","ruling":"門檻改動理由有四：①客流已占同店三分之二，比同店更早反映飛輪斷裂，所以減碼提前到看客流；②月度Black Box資料不在證據包，價差改用季度；③利潤率門檻由200bp收緊到連2季50bp，因公司刻意壓低漲價，緩衝變薄；④FY27共識已是13.68美元，遠高於舊門檻11.50，舊H3門檻退休","evidence_level":"高","settle_metric":"各門檻對應的季度數字","if_then":[],"evidence_refs":["reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"以Chili's季度同店、客流與領先產業幅度驗證份額增益","type":"假設驗證","maps_to":"H1","metric":"Chili's單季同店、客流、領先休閒餐飲產業幅度","threshold":"同店不低於+3%、客流不低於0%、領先不低於300bp","action":"達標則維持；連2季未達則停止加碼","source_freq":"公司季報與法說，每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1"]},{"n":2,"text":"Chili's任一季客流年減","type":"Single Thing","maps_to":"R1","metric":"Chili's單季客流年變化","threshold":"低於0%","action":"減碼一半；下一季同店也低於0%且餐廳利潤率年減則清倉","source_freq":"公司季報，每季","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"成本通膨（含關稅、運費、時薪）壓縮餐廳利潤率","type":"風險","maps_to":"R3","metric":"Brinker餐廳營業利潤率年變化","threshold":"連2季年減超過50bp（FY27第2季指引約持平，不計）","action":"減碼1/3","source_freq":"公司季報，每季","date":"2027-04","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":4,"text":"價格回到合理偏便宜區，且飛輪未斷","type":"估值rearm","maps_to":"H1","metric":"股價、FY2027共識倍數、最近一季Chili's客流","threshold":"股價不高於185美元（約13.5倍）且客流高於0%","action":"分批加碼，每次目標倉位1/3","source_freq":"每日股價＋每季財報","date":null},{"n":5,"text":"倍數超過自身合理上緣，而盈餘未跟上","type":"減碼","maps_to":"H3","metric":"股價÷次一財年共識每股盈餘","threshold":"不低於19倍，且近3個月共識未上修","action":"減碼1/3","source_freq":"每週","date":null},{"n":6,"text":"同店轉負同時利潤率下滑，確認飛輪斷裂","type":"清倉","maps_to":"R1","metric":"Chili's單季同店與餐廳營業利潤率年變化","threshold":"同店低於0%且餐廳利潤率年減","action":"清倉","source_freq":"公司季報，每季","date":null},{"n":7,"text":"Maggiano's客流持續流失","type":"風險","maps_to":"R4","metric":"Maggiano's單季客流","threshold":"連4季不高於−5%","action":"不加碼，並留意減損或出售；不單獨觸發減碼（約占獲利3%）","source_freq":"公司季報，每季","date":"2027-08","evidence_refs":["supply_demand_durability#2","end_markets#1"]},{"n":8,"text":"Black Box人均消費基準更新，以及Q2 FY27財報後複審","type":"複審日期","maps_to":"R2","metric":"更新後Chili's人均消費低於同業的差距、Q2同店","threshold":"差距低於1美元則重估護城河等級","action":"複審","source_freq":"一次性","date":"2027-01"},{"n":9,"text":"回購與開店節奏","type":"假設驗證","maps_to":"H3","metric":"年淨股數縮減、租賃調整後槓桿、FY28開店數","threshold":"減股不低於3%、槓桿低於2倍、FY28開店不少於15家","action":"未達則下調基本情境每股盈餘","source_freq":"年報與投資人日，每年","date":"2027-08"},{"n":10,"text":"利潤率修復能否守住","type":"假設驗證","maps_to":"H2","metric":"營業利益率（排除其他損益）","threshold":"不低於10%","action":"連4季未達則下調基本情境倍數至14倍","source_freq":"公司季報，每季","date":"2027-04"}],"kill_metrics":[{"metric":"Chili's單季客流（年變化）","bear_threshold":"低於0%","window":"任一季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"Chili's單季同店銷售","bear_threshold":"低於0%且同季餐廳營業利潤率年減","window":"任一季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"Chili's同店領先休閒餐飲產業幅度","bear_threshold":"低於200bp","window":"連2季","source":"公司法說引用的Black Box產業資料","last_status":"ok"},{"metric":"Brinker餐廳營業利潤率年變化","bear_threshold":"年減超過50bp","window":"連2季（FY27第2季指引約持平，不計）","source":"公司季報新聞稿","last_status":"ok"},{"metric":"租賃調整後槓桿","bear_threshold":"超過2倍","window":"任一季","source":"公司法說與投資人日","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價不高於185美元（FY2027共識約13.5倍）且最近一季Chili's客流為正，才恢復分批加碼","exec_line":"續抱現有部位、不追價；股價不高於185美元且最近一季Chili's客流為正時分批加碼（每次目標倉位1/3）；客流任一季轉負減碼一半；同店轉負且餐廳利潤率年減清倉；股價達次一財年共識19倍以上且共識未上修，減碼1/3","holding_cap":"單一持股上限3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回落到185美元以下（FY2027共識約13.5倍，基本情境五年年化約10%），且最近一季Chili's客流仍為正","qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=43.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件=\"股價回落到185美元以下（FY2027共識約13.5倍，基本情境五年年化約10%），且最近一季Chili's客流仍為正\""},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Chili's由客流帶動的份額增益，在高基期後仍能延續；新客轉為常客，不是一次性爆紅","2y":"FY27至FY28每季同店不低於+3%、客流不低於0%、領先休閒餐飲產業不低於300bp","5y":null,"10y":null,"threshold":"單季Chili's同店不低於+3%、客流不低於0%、領先產業不低於300bp","source":"公司季報新聞稿與法說（Q1 FY27同店+10.1%、客流+6.4%、領先720bp）；Black Box產業基準","drift_rule":"以近四季同店平均對門檻的偏離計：連2季偏離5%以上為削弱，連3季偏離10%以上為反轉；任一季客流轉負直接觸發唯一致命點"},{"id":"H2","text":"利潤率修復可守並緩步擴張，不因價值策略與加碼人力而回吐","2y":null,"5y":"FY2031餐廳營業利潤率較FY2026累計擴張不少於100bp；穿越一次消費放緩，營業利益率（排除其他損益）仍守在9%以上","10y":null,"threshold":"營業利益率（排除其他損益）不低於10%；餐廳營業利潤率年增不低於20bp（FY27第2季指引約持平，除外）","source":"公司季報（Q1 FY27分別為10.4%、17.7%）；2026-09-17投資人日CFO Mika Ware的長期每年20–40bp說法","drift_rule":"連4季偏離門檻5%以上為削弱，連6季偏離10%以上為反轉"},{"id":"H3","text":"自由現金流轉成每年3–5%減股與2–3%開店，且不拉高槓桿","2y":null,"5y":"FY2031稀釋股數較FY27指引中值42.5百萬股減少不少於15%；FY29起每年開約30家新店","10y":null,"threshold":"年淨減股不低於3%；租賃調整後槓桿低於2倍；FY28開店不少於15家","source":"2026-09-17投資人日（CFO：每年減股3–5%、槓桿目標低於2倍、FY28已核准15家）；Q1 FY27回購1.25億美元","drift_rule":"連4季年化減股低於2.85%為削弱；連6季低於2.7%或槓桿超過2倍為反轉"}],"R":[{"id":"R1","text":"消費放緩加上高基期，使Chili's客流轉負","h_ref":"H1","clock":"⚡","threshold":"任一季客流低於0%＝減碼一半；同店同步低於0%且餐廳利潤率年減＝清倉","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#0"]},{"id":"R2","text":"同業複製社群行銷與價值套餐，價值領先縮小（Black Box已更正人均消費價差，比原先說法窄）","h_ref":"H1","clock":"🔥","threshold":"領先產業幅度連2季低於200bp，或客單組合連2季不高於−1%","evidence_refs":["competitive_share_entrants#2"]},{"id":"R3","text":"商品（含關稅）、運費與時薪通膨吃掉餐廳利潤率，而公司刻意把漲價壓在3%附近","h_ref":"H2","clock":"🔥","threshold":"餐廳營業利潤率連2季年減超過50bp（FY27第2季指引約持平，除外）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"id":"R4","text":"Maggiano's客流持續流失，轉機慢於計畫（2026-08-12 CEO已承認比計畫慢）","h_ref":"H2","clock":"🐢","threshold":"Maggiano's客流連4季不高於−5%（Q1 FY27為−5.1%）","evidence_refs":["supply_demand_durability#2","end_markets#1"]},{"id":"R5","text":"資本支出由約2.75億升至4億美元，改裝目前只打平資金成本，新店報酬未證實，回購在高倍數執行，增量報酬被稀釋","h_ref":"H3","clock":"🐢","threshold":"FY28改裝店營收提升低於3%，或管理層仍未揭露改裝與新店報酬；回購期間前瞻本益比均值超過18倍","evidence_refs":[]}],"single_thing":{"description":"Chili's出現第一季客流年減，客流帶動同店的飛輪斷裂","why_fatal":"這是每股盈餘最大的單一敏感項：客流約占同店三分之二，營業槓桿雙向作用。以約35%遞減利潤率假設估算，同店每少5個百分點，營業利益約少1億美元、每股盈餘約少2美元（約15%），倍數也會同時由15倍往11倍收斂","if_happens":"減碼一半；下一季同店也轉負且餐廳利潤率年減，則清倉","how_monitor":"每季財報的Chili's客流拆分、法說的季中同店口徑、Black Box產業客流","probability":"約30%（12–24個月）：Q2 FY27要對上去年11月的高基期，10月客單組合已轉負，NRA也下修2026實質餐飲成長；但Q2開局仍高個位數，客流仍是同店主力"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.3,"peg_fy2":1.3,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.87,"FY2027E":13.68,"FY2028E":14.8,"FY2029E":16.45},"fy_end_month":6,"eps_basis":"FY2026A為GAAP稀釋每股盈餘（財務歷史欄，調整後數字未涵蓋）；FY2027E至FY2029E為Koyfin調整後共識，FY2027含第53週約0.70美元"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"Black Box更正休閒餐飲人均消費基準","impact":"中","watch":"Chili's低於同業的價差還剩多少"},{"date":"2026-11","date_precision":"month","type":"product","event":"Big Crispy Chicken Parm店內桌卡上架","impact":"低","watch":"每店每日銷量是否由約2份回升"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q2 FY27財報與長期成長更新","impact":"高","watch":"同店是否守住中個位數、客流為正，以及對上去年11月高基期的表現"},{"date":"2027-05","date_precision":"month","type":"product","event":"評估是否更換Big Crispy主打訊息","impact":"中","watch":"廣告帶動的客流增量是否衰退"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27年報（含第53週）與FY28財測","impact":"高","watch":"FY28財測扣除第53週後是否仍雙位數成長，開店是否達15家以上"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：substitute_technology（替代技術）（尾部風險或事件型，不擋）。核心軸由採證 agent 自報不適用（燈號不變，請看 note 理由）：customer_concentration_credit。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
