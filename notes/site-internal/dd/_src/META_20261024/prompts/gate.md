你是 DD 管線 v20 的判斷層閘（gate），標的 META（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝64601 USD M（YoY +26%；QoQ +6.2%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：共識約 $63.4B（LSEG，Reuters 2026-10-20）；公司原指引 $61–64B
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income（Meta 不報 Non-GAAP；此為剔除 $9.89B 訴訟和解費用後的調整數）＝22880 USD M（利益率約 35.4%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝12988 USD M（利益率 20%；YoY -37%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi7_guidance_q4_2026_revenue`（q1_business）｜Guidance: Q4 2026 revenue＝73000～76000 USD M（含約 1% 匯率逆風）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：Benzinga 彙整 Q4 營收共識約 $73.65B
- `f_kpi10_guidance_fy2026_reality_`（q1_business）｜Guidance: FY2026 Reality Labs 虧損與其他＝18000～19000 USD M（RL 虧損區間；Q4 稅率 15–17%；2027 RL 虧損約 $15B；剔除訴訟費用後 2026 營業利益仍預期高於 2025）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi11_family_daily_active_peop`（q1_business）｜Family daily active people (DAP)＝3.64 billion（YoY +3%，2026 年 9 月平均）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi12_ad_impressions_growth`（q1_business）｜Ad impressions growth＝10 % YoY｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[12]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi13_average_price_per_ad_gro`（q1_business）｜Average price per ad growth＝14 % YoY｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[13]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_peer_meta_gross_margin_pct`（q2_moat）｜META 毛利率＝81.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_meta_operating_margin_pct`（q2_moat）｜META 營業利益率＝38.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_googl_operating_margin_pct`（q2_moat）｜GOOGL 營業利益率＝33.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amzn_operating_margin_pct`（q2_moat）｜AMZN 營業利益率＝11.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_snap_operating_margin_pct`（q2_moat）｜SNAP 營業利益率＝-5.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNAP.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pins_operating_margin_pct`（q2_moat）｜PINS 營業利益率＝6.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PINS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_meta_fcf_margin_pct`（q2_moat）｜META FCF 利潤率＝17.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_googl_fcf_margin_pct`（q2_moat）｜GOOGL FCF 利潤率＝11.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pins_fcf_margin_pct`（q2_moat）｜PINS FCF 利潤率＝28.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PINS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi9_guidance_fy2026_capex`（q1_business）｜Guidance: FY2026 capex（含融資租賃本金）＝135000～145000 USD M（前次 130,000–145,000）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝30.29 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝34.8 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝40.42 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝256558.0 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate 0y 平均（50 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝311385.98 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate +1y 平均（60 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_share_based_compensation`（q1_business）｜Share-based compensation＝7363 USD M（占營收 11.4%；占 GAAP 營業利益 56.7%；占剔除費用後營業利益 32.2%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi6_gaap_diluted_eps`（q1_business）｜GAAP diluted EPS＝3.83 USD（剔除和解費用後 7.40；Q3 2025: 1.05）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：共識 EPS 分歧大（含費用口徑約 3.56–5.70、不含約 6.53，來源：web_search 彙整，未能單一驗證）
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝-2120 USD M（營運現金流 32,786 減 capex 33,942 減融資租賃本金；Q3 2025: +10,625）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_kpi4_capital_expenditures`（q1_business）｜Capital expenditures（含融資租賃本金）＝34910 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝32393.0 USD m｜期間與口徑：2026-10-24／yfinance 最新一季：總債務 114842.0、現金 82449.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2547.51 m shares｜期間與口徑：2026-10-24／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝1669471.4 USD m｜期間與口徑：2026-10-24／市值 1637078.4 ＋ 淨負債 32393.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.327 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝642.62 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.22 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 30.29，分子＝快照價 642.62｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.92 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝54.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝54.9 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.78 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝57.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.51 x｜期間與口徑：2026-10-24／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-2.85 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 31.18 → 30.29（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.03 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（30.3 → 30.29）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（34.8 → 34.8）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.47 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（40.23 → 40.42）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi8_guidance_fy2026_total_ex`（q1_business）｜Guidance: FY2026 total expenses＝175000～179000 USD M（已納入 9.9B 訴訟費用）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-21））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-4.64 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.76｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：META 10-K FY2025 風險因子自述：部分用戶（尤其年輕用戶）已轉用替代產品並減少使用 Meta 產品，且 Apple、Google 皆把競品整合進 iOS／Android。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：META 10-K FY2025 自述除社群與廣告對手外，另在前沿 AI 模型與消費硬體／AR／VR 與其他公司競爭，且硬體經驗有限，可能讓他人更有效競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：moat_trend、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：CFO Li 表示公司持續低估算力需求，並拒絕給 2027 年資本支出指引，稱規劃為動態
  - 來源：Munich Startup feed（Meta CFO refuses 2027 capex guidance）（as_of 2026-10-23）｜affects：thesis.R、valuation、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 披露：FTC 自 2020 年起訴 Meta 反壟斷，訴求含剝離或重組 Instagram 與 WhatsApp；2024 年 11 月歐盟執委會就 Marketplace 搭售與資料使用開罰。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-29）｜affects：moat_trend、decision_inputs.bear、triggers
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 披露：美國、歐洲及其他轄區競爭主管機關對 Meta 的社交、廣告、行動應用及併購行為有多項訴訟與調查，且數量與重要性近年增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：Meta 有意義的營收來自服務中國廣告主的少數經銷商，美中貿易爭端（含關稅）可能使政府行動減少或消除中國廣告營收。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：消費硬體製造依賴少數第三方、營運集中亞洲，關稅、制裁、出口管制可能造成供應短缺與成本上升。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：資料中心與光纖基建擴張涉及多地，貿易爭端可能推高專案成本或延誤。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：消費性硬體製造依賴少數第三方，且常集中於亞洲單一區域；關稅、制裁、出口管制可能衝擊製造與銷售。
  - 來源：Meta Platforms Form 10-K FY2025 (SEC)（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FT 報導 Goertek 代工 Meta AI 眼鏡，Meta 稱供應鏈多元、不單靠一家製造商。
  - 來源：PYMNTS: Meta Seeks New Supply Chain Opportunities for AI Smart Glasses（as_of 2025-09-16）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Meta 10-K 自述：部分用戶（尤其年輕用戶）已使用類似或可替代其產品的其他產品，並減少使用 Meta 產品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-29）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026（2026-07-29 公布）營收約 $60.8B 小幅優於預期約 $60.2B，GAAP EPS $6.18 低於預期約 $7.18–7.22；Q3 營收 guidance $61–64B，中點低於共識約 1%（Barchart 數字：中點 $62.5B vs 預期約 $63.1B）；FY2026 capex guidance 收窄至 $130–145B、費用 $165–169B。
  - 來源：Barchart / Rivkin / Benzinga（搜尋摘要）（as_of 2026-07-29）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q1 2026（4/29）公司上調 FY2026 capex guidance 至 $125–145B（原 $115–135B），Q2 營收 guidance $58–61B 涵蓋共識 $59.5B；公布後股價隔日跌近 10%。Benzinga 統計 2022-10 至 2026-07 共 17 次 guidance 更新，上調 11 次、下調 4 次。
  - 來源：Investing.com (Reuters)；SiliconANGLE；Benzinga（搜尋摘要）（as_of 2026-04-29）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露公司涉及多起集體訴訟與股東衍生訴訟，涵蓋廣告、反壟斷、隱私、青少年等主題，另有 AI 訓練版權訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `major_events#5`（major_events｜方向 -｜狀態 ok）：投資人於聯邦法院聲請認證 Cambridge Analytica 相關證券集體訴訟（購買期間2017-02至2018-07）。
  - 來源：MLex 報導（as_of 2026-08-21）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：FY2025 10-K 揭露公司涉及多起集體訴訟與股東衍生訴訟，涵蓋廣告、反壟斷、隱私、青少年等主題，另有 AI 訓練版權訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1716.0,"bear_5y_price":462.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":81.4,"ev5y_pct":69.9,"irr_base_pct":12.6,"asym_ratio":5.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":30.29,"pe":21.22,"basis":"FY2026E 共識 EPS（GAAP 稀釋口徑，是否含第三季和解費用各家不一）；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[35.8,42.5,49.5,57.5,66.0],"base":[34.2,39.5,44.8,50.2,55.5],"bear":[28.5,27.0,28.5,30.5,33.0]},"pe":{"bull":26,"base":21,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.327,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### META_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Susan Li (CFO)｜guidance：Q3 2026 總營收財測 $61–64 十億美元（原話："$61 billion to $64 billion."）
- 2026-07-29｜Susan Li (CFO)｜guidance：Q3 財測假設匯率約 1% 逆風（原話："Our guidance assumes foreign currency is an approximately 1%"）
- 2026-07-29｜Susan Li (CFO)｜guidance：2026 全年總費用指引 $165–169 十億美元（下限上調以納入 Q2 法律費用）（原話："in the range of $165 billion to $169 billion."）
- 2026-07-29｜Susan Li (CFO)｜guidance：仍預期 2026 營業利益高於 2025（原話："We continue to expect to deliver operating income this year"）
- 2026-07-29｜Susan Li (CFO)｜guidance：2026 資本支出指引 $130–145 十億，自原 $125–145 十億收窄（原話："to be in the range of $130 billion to $145 billion"）
- 2026-07-29｜Susan Li (CFO)｜guidance：其餘季度稅率預期 15%–17%，原為 13%–16%（原話："an increase from our prior outlook of 13% to 16%."）
- 2026-07-29｜Susan Li (CFO)｜risk：管理層點出青少年議題訴訟風險（原話："scrutiny on youth-related issues in several markets"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 營業利益排除法律費用與資遣費後的口徑（原話："Excluding the Q2 legal charges and severance expenses"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 總費用年增 55%，含 24 億美元法律費用（原話："up 55% compared to last year and included $2.4 billion"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 含 12 億美元資遣費（5 月裁員）（原話："$1.2 billion in severance expenses"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 年底員工數超過 7.5 萬人，較 Q1 減 3%（原話："We ended Q2 with over 75,000 employees, down 3% from Q1."）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 自由現金流僅 7.84 億美元（原話："Free cash flow was $784 million."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：Q2 資本支出金額（原話："were $31.1 billion"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：期末現金與有價證券（原話："$90.3 billion in cash and marketable securities"）
- 2026-07-29｜Susan Li (CFO)｜customer：Q2 廣告營收與年增（原話："Q2 Family of Apps ad revenue was $59.4 billion, up 27%"）
- 2026-07-29｜Susan Li (CFO)｜customer：廣告曝光量年增 14%（原話："the total number of ad impressions served across our"）
- 2026-07-29｜Susan Li (CFO)｜customer：每則廣告均價年增 12%（原話："The global average price per ad increased 12% year-over-year"）
- 2026-07-29｜Susan Li (CFO)｜product：FoA 其他營收首度達 10 億美元，主要來自 WhatsApp 付費訊息與訂閱（原話："other revenue reached $1 billion and grew 73%"）
- 2026-07-29｜Susan Li (CFO)｜product：Reality Labs Q2 營收 4.31 億美元，AI 眼鏡成長（原話："Q2 revenue was $431 million, up 16% year-over-year"）
- 2026-07-29｜Susan Li (CFO)｜product：Advantage+ 年化營收規模（原話："continue to grow, reaching over $75 billion in"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：CEO 稱其廣告業務美元成長速度為同業最快（原話："reporting faster year-over-year revenue growth than any"）
- 2026-07-29｜Susan Li (CFO)｜product：Reels 排名改善帶來 Instagram sessions 提升（原話："drove a 15 basis point increase in sessions on Instagram"）
- 2026-07-29｜Susan Li (CFO)｜product：Facebook 廣告模型改善數據（原話："8.3% increase in ad clicks and a 15.7% uplift"）
- 2026-07-29｜Susan Li (CFO)｜product：推出 Meta Generative Recommender 廣告系統（原話："a paradigm shift in how our ad system works"）
- 2026-07-29｜Susan Li (CFO)｜product：Instagram 時長雙位數成長（原話："global time spent this quarter grew double digits"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：推出 Meta One 訂閱服務（原話："We also just launched Meta One, a new subscription offering"）
- 2026-07-29｜Susan Li (CFO)｜product：已推出模型 API（原話："We also recently launched a high intelligence model API"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：Meta AI 每日互動人數成長（原話："a 60% increase in the number of people interacting"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：商業代理已有逾百萬企業使用（原話："already more than 1 million businesses using"）
- 2026-07-29｜Susan Li (CFO)｜customer：Movida 案例：WhatsApp 每日訂位成長（原話："44% increase in daily bookings through WhatsApp"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：眼鏡早期銷售優於預期（原話："Early sales have been strong, exceeding our expectations"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：CEO 預告個人代理產品將很快推出（原話："we're going to ship this at some point soon"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：對個人代理的長期預測（原話："extremely unlikely if you look out 5 years from now"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：管理層對算力的定位：可直接出售，現有算力獲高於成本的報價（原話："We're getting a lot of offers for compute at a"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：問答中再提算力報價溢價（原話："quite a number of offers at a meaningful"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜margin：CEO 稱賣智能比賣算力毛利更高（原話："margin on selling intelligence rather than selling compute"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：不會把算力全數出售換短期利潤（原話："foolish to basically just sell all of the compute"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：與 BlackRock 合資興建 1GW 資料中心（原話："BlackRock to develop a new 1 gigawatt data center"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：資本結構納入更高比重債務（原話："to include a greater mix of debt as we"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：2026–2027 容量規劃以最大化為目標（原話："geared towards maximizing 2026 and 2027 capacity."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：產業長期建置不足，現有容量極具價值（原話："making existing capacity, including our own,"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：自研晶片投資（原話："our internal custom silicon effort, which will provide"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：2028 規劃重視彈性（原話："we're really focusing on flexibility."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：核心業務仍有未滿足的算力需求（原話："ROI-positive places that we would put compute toward"）
- 2026-07-29｜Susan Li (CFO)｜competition：稱模型不在前沿也能服務用戶（原話："regardless of whether our models are on the frontier"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：開源模型目前不如前沿模型，故不依賴（原話："source models are not as strong as the frontier models."）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：預期近期回頭釋出開源模型（原話："we will get back to releasing some open source models at"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：自稱最擅長將產品規模化至數十億人（原話："we're probably the best company in the world at scaling"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：AI 定位：把超級智能交到個人手中（原話："AI with the primary goal of putting superintelligence"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：企業商機被描述為需新建的能力（原話："somewhat of a new muscle that we"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：企業產品採按結果付費模式（原話："businesses only pay us when we achieve results for them"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：對 MSL 實驗室進展的評價（原話："I'm quite happy with the trajectory that we're on."）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：持續擴大更大模型訓練（原話："we're in the process of scaling"）

### 問答異常語氣（迴避／改口／保留）
- META_Q2_2026_Earnings_Call_20260729.md｜問：Brian Nowak 問 2026–27 哪個新業務最先能展現可量化的 ROIC｜答法：Mark 未點名單一業務，改稱對所有領域都有意義的成長，細節『稍後分享』
- META_Q2_2026_Earnings_Call_20260729.md｜問：Brian Nowak 問 2027 年資本支出的哲學與上下行因素｜答法：Susan 表示不提供 2027 資本支出指引，僅說規劃高度動態

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 1 | 0 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 6 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"廣告核心維持 ≥18% 營收成長，且 AI 能持續讓「曝光」與「每廣告價」同時上升（＝變現效率真的在提高，而非用廣告版位換量）"},{"id":"H2","text":"2026–2028 的巨額 AI capex 最終轉為可衡量的損益貢獻——經由（a）廣告變現效率續升，或（b）一條具名、帶金額的外部收入線（企業 agent／模型 API／直接賣算力／訂閱）。這是 make-or-break。"},{"id":"H3","text":"市場對資本強度的折價，隨 ROI 能見度回升而部分修復（不需要回到 25 倍，只需要不再往 12 倍走）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"廣告景氣下行——廣告是需求端週期敏感支出，中小企業預算對總經最敏感。Q2 的每廣告價 +12% 中，管理層明說有一部分來自「相對去年 Q2 的總經改善」與「匯率順風」，這兩項都會反向。Q3 指引已隱含匯率約 1% 的逆風。"},{"id":"R2","text":"AI capex 與折舊爬坡吞噬營運槓桿，ROI 遲遲不兌現（本檔最高機率風險）——Q2 折舊攤銷 $63.56 億（+46% YoY），H1 累計 $123.55 億（去年同期 $82.42 億）。2026 全年 D&amp;A 約 $275 億，2027 依當前資本投入節奏將跳到 $440 億上下。同期營收增速由 +28% 降到 +19–20%。費用的二階導數為正、營收的二階導數為負，這是利潤率壓縮的定義。"},{"id":"R3","text":"注意力介面遷移 ＋ 自家前沿模型落後——Meta Superintelligence Labs 的 Muse Spark 在 Artificial Analysis Intelligence Index v4.0 得 52 分、排名第 4，落後 Gemini 3.1 Pro（57）、GPT-5.4（57）、Claude Opus 4.6（53）。Zuckerberg 自己在法說上把「即使我們的模型不在前沿也沒關係，我們有分發」寫進論述——這是一個誠實但不令人安心的護欄。若消費者的預設 AI 互動介面長在別人的模型上，Meta 的分發優勢會被逐步中介化。"},{"id":"R4","text":"訴訟與監理已進入兌現階段（非「即將發生」）——這是本次相對前次報告最需要改寫的一條。截至報告日的已實現事實：① 2026-03 新墨西哥州陪審團認定 Meta 違反州法、危害兒童身心安全，判民事罰款 $3.75 億；② 同月另一新墨西哥州陪審團認定違反消費者保護法，再判 $3.72 億；③ 同月洛杉磯 K.G.M. v. Meta et al. 陪審團認定 Meta（與 YouTube）對用戶心理健康損害負有責任；④ 本季財報認列 $24 億法律相關費用，管理層並在展望中明文警告「數起美國兒少相關審判排定於今年，最終可能造成重大損失」。已兌現的民事罰款合計約 $7.47 億，與「$1.4 兆」的州檢察長理論求償上限相差三個數量級——但重點不是金額，是 Meta 至今在這一波審判中尚未勝訴過。加上 EU DMA 已於 2025-04 開罰 €2 億（consent-or-pay 違規），且 DMA 對重複違規的理論上限為全球營收 10%，這是一條持續性、非一次性的成本曲線。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","irr_base_pct":10.3,"ev5y_pct":55.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.9,"ev5y_pct":55.8,"irr_base_pct":10.3,"max_dd_pct":-60.0,"bull_5y_price":1500.0,"bear_5y_price":271.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","price_at_dd":542.49,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"META","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Meta Platforms, Inc."},"oneliner":"廣告本業年增 26%，每則廣告均價加速到 +14%；但 2026 年資本支出 1,350–1,450 億美元，第三季自由現金流已轉負。21 倍前瞻本益比對約 15% 的獲利成長算合理，成敗看 2027 年 1 月的資本支出與營業利益指引。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球廣告主的轉換預算。Q3 營收 646 億美元，約 99% 來自 Family of Apps，其中廣告 631 億美元，年增 26%。錢卡在「注意力分配加廣告排序」這一個節點；上游的算力成本正在快速墊高。","reasoning":"最小交付：Q3 營收 64,601 百萬美元，年增 26%。Family of Apps 64,158 百萬美元；其中廣告 63,060 百萬美元，其他營收（WhatsApp 付費訊息、訂閱）約 1,100 百萬美元，年增 59%。Reality Labs 營收 443 百萬美元，年減 6%，2026 年虧損指引 18,000–19,000 百萬美元，2027 年約 15,000 百萬美元。TTM 毛利率 81.75%。GAAP 營業利益率 20%，含 99 億美元多州檢察長和解費用；剔除後約 35.4%，營業利益年增 11%。量價結構：家族日活 36.4 億人，年增 3%，用戶面已近飽和；曝光年增 10%（Q1 19%、Q2 14%），每則廣告均價年增 14%（Q1、Q2 皆 12%）。成長正從量轉向價。景氣位置判第 II 段（擴張）：Q4 營收指引 730–760 億美元，中點年增仍逾兩成，均價還在加速。依據是營收與單價，不是股價。產業態勢判雙向拉鋸：競爭面，10-K 自述年輕用戶轉向替代產品，前沿 AI 與硬體也有對手；結構面，eMarketer 預估 2026 年 Meta 數位廣告份額 26.8%，首度超越 Google 的 26.4%；其他面，FTC 上訴、青少年訴訟與歐盟處分持續。單點依賴：無單一客戶占營收或應收帳款達 10%（10-K FY2025），客戶面沒有集中度風險。外部依賴有兩處：Apple、Google 掌握作業系統入口，以及服務中國廣告主的少數經銷商。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi7_guidance_q4_2026_revenue","f_kpi10_guidance_fy2026_reality_","f_kpi11_family_daily_active_peop","f_kpi12_ad_impressions_growth","f_kpi13_average_price_per_ad_gro","f_peer_meta_gross_margin_pct"],"verdict_values":{"revenue_quality":"高。收入按曝光與轉換計價、屬經常性，沒有單一客戶達營收 10%。但管理層明說均價上漲有一部分來自相對去年的總經改善，這部分會反轉。","unit_econ_note":"Q3 曝光 +10%、均價 +14%，量價同升。Muse 推理成本高，管理層稱一年內算力成本效率可提升十倍以上，但未揭露單位成本數字。","archetype":{"primary":"品質複利成長","secondary":"資本密集轉型期","confidence":"中","fingerprint":"TTM 毛利率約 82%、營業利益率約 38%，但第三季資本支出已高於營運現金流"},"industry":{"clock_phase":"II","sd_verdict_source":"供需判結構性持久，問題在成長斜率放緩，不是需求反轉。WARC 預估全球廣告支出 2026 年 +9.1%、2027 年 +7.9%；Oberlo 預估數位廣告 2027–2028 年仍成長，只是略降速。","bargaining":{"up":"上游議價權偏強。第三方雲端、AI token、折舊與資料中心營運成本是 Q3 費用年增 68% 的主因之一（Q3 法說 CFO）。","down":"下游分散。無單一客戶達營收或應收 10%，廣告主仍接受每則廣告均價年增 14%。","geo":"10-K 風險因素自述：服務中國廣告主的少數經銷商貢獻有意義的營收，實際金額事實表未涵蓋。"},"profit_pool_dir":"數位廣告利潤池往頭部集中：2026 年預估 Meta、Google、Amazon 合計約 62.3% 份額（eMarketer）。五年營業利益池占比的變化，事實表未涵蓋。","tam_table":[{"item":"全球廣告支出","value":"2026 年約 1.30 兆美元（+9.1%），2027 年約 1.40 兆美元（+7.9%）；WARC 2025-12 預測"},{"item":"全球數位廣告支出","value":"2027 年約 9,103 億美元，2028 年約 9,656 億美元，成長略放緩；Oberlo"},{"item":"Meta 數位廣告份額","value":"2026 年預估 26.8%，Google 26.4%，Amazon 9.0%；eMarketer 預測值"},{"item":"Meta 廣告成長外部預測","value":"WARC 預估 2026 年 +22.3%，2027 年放緩至 +12.1%；對照 FY2027 共識營收年增約 21%"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平（→）。網路效應加上排序系統的資料回饋，讓廣告均價連三季上升；但重資本化與年輕用戶分流兩股力量互相抵銷，評 B 級。","reasoning":"機制：36.4 億日活產生的行為資料餵給推薦與廣告排序模型，模型提高轉換，廣告主再加碼預算。可證方向一是定價：每則廣告均價年增率由 12% 升到 14%，而曝光同期由 19% 降到 10%，代表廣告主為同一次曝光付更多錢。可證方向二是利潤率：TTM 營業利益率 38.1%，高於 GOOGL 33.1%、PINS 6.3%、SNAP −5.1%。同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率代替，無法判斷 spread 是否擴大，所以不給 8 分以上的合併分。執行力 9：Instagram 時長雙位數成長，Reels 相關性改版讓時長再增 4% 以上，GEM 擴展讓 App 廣告轉換增 9.6%。定價權 8：均價加速；但法說也承認其中一部分來自總經，一部分被低變現地區的曝光稀釋。威脅：AI 介面遷移屬生態攻擊；年輕用戶分流與反壟斷屬點對點。","fact_refs":["f_kpi12_ad_impressions_growth","f_kpi13_average_price_per_ad_gro","f_peer_meta_operating_margin_pct","f_peer_googl_operating_margin_pct","f_peer_amzn_operating_margin_pct","f_peer_snap_operating_margin_pct","f_peer_pins_operating_margin_pct","f_peer_meta_fcf_margin_pct","f_peer_googl_fcf_margin_pct","f_peer_pins_fcf_margin_pct","f_kpi9_guidance_fy2026_capex"],"verdict_values":{"moat":{"mechanism":"使用者規模產生行為資料，資料改善推薦與廣告排序，排序再提高廣告主轉換與預算的自我強化迴圈","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"擴大的一面：均價年增率 12%→12%→14% 連三季走高，Advantage+ 年化營收逾 750 億美元（Q2 法說），合作廣告年化逾 150 億美元、年增 97%。縮減的一面：資本支出超過營運現金流，10-K 自述年輕用戶轉向替代產品，前沿模型仍在追趕。兩邊抵銷，判持平。","competitor_notes":[{"name":"GOOGL","strategy_note":"搜尋加 YouTube 雙引擎，TTM 營業利益率 33.1%，低於 Meta；2026 年數位廣告份額預估被 Meta 小幅超越，是最直接的預算競爭者。"},{"name":"AMZN","strategy_note":"零售媒體掌握購買端資料，份額約 9%；TTM 自由現金流率 −0.5%，同樣處在重資本支出期，在電商轉換廣告上與 Advantage+ 正面競爭。"},{"name":"SNAP","strategy_note":"TTM 營業利益率 −5.1%，規模與排序能力差距大，對 Meta 只構成年輕用戶時間上的點狀競爭。"},{"name":"PINS","strategy_note":"毛利率 79.5% 接近 Meta，但營業利益率只有 6.3%，屬購物意圖利基平台，不足以撼動 Meta 定價。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營業利益率與自由現金流率代替","threats":[{"level":"🔴","text":"消費者的預設 AI 互動介面若長在別家前沿模型或作業系統上，Meta 的分發優勢會被中介化。10-K 自述在前沿模型與消費硬體上都有對手，且硬體經驗有限。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"年輕用戶轉向替代產品並減少使用 Meta 產品（10-K 自述），Apple、Google 也把競品整合進作業系統。","p":25,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"FTC 對 Instagram、WhatsApp 收購案上訴，訴求含拆分或重組；歐盟就 Marketplace 搭售與資料使用開罰。","p":10,"evidence_refs":["regulatory_antitrust#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（資本支出由輕轉重，周轉率下滑中）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者免費、廣告主付費，三角色分得清。廣告主買的是轉換：採用 Meta AI 商業助理建議的廣告主，在同樣單次轉換成本下多拿近 5% 轉換，並多投 9% 預算（Q3 法說）。這是需要，不只是想要。"},{"item":"決策層級","level":"🟢","text":"決策單位是單一廣告活動的投報率，不是平台品牌。均價年增 14%，曝光仍年增 10%，漲價後用量沒有流失；近 1,000 萬廣告主用過生成式素材工具，轉換成本在工作流程層加深。"},{"item":"價值鏈分配","level":"🟡","text":"Meta 在廣告價值鏈拿走大部分經濟利益，但上游算力供應（第三方雲端、AI token、伺服器）正分走更多。2026 年資本支出指引 1,350–1,450 億美元，Q3 自由現金流 −21 億美元；作業系統入口也掌握在 Apple、Google 手上。"},{"item":"社會容忍度","level":"🔴","text":"Q3 認列 99 億美元多州檢察長和解費用，Q2 另有 24 億美元法律費用。管理層警告未來數月有多場美國青少年相關審判，FTC 對拆分案上訴。社會對其變現方式的容忍度，已轉成實際成本曲線。"}],"roiic":9,"reinvest_rate":"約 180%：2026 年資本支出指引中值 1,400 億美元，除以 FY2026 共識淨利約 772 億美元，毛額口徑","endo_ceiling":16,"formula_note":"當期 ROIC：投入資本與折舊攤銷事實表未涵蓋，無法用稅後營業利益率×投入資本周轉率計算。增量報酬：FY2026→FY2028 共識 EPS 增量 10.13 美元 × 25.48 億股，約 258 億美元淨利增量；對應 2026–2027 兩年資本支出毛額約 2,800 億美元（2027 年假設不低於 2026 年），得約 9%。再投資率約 180%，內生成長上界約 9% × 1.8 ≈ 16%。這個上界要靠再投資持續高於淨利；若再投資率壓回 100%，上界只剩約 9%。"}}}},"q3_growth":{"verdict":"成長跑道寬（🟢）。數位廣告份額約 27%，仍未見頂；WhatsApp 付費訊息、Muse、Meta One 與企業 API 都有可追蹤的早期數字，但第二曲線的變現金額尚未揭露。","reasoning":"成長組成：價大於量。均價 +14%、曝光 +10%；無併購貢獻；回購淨效果事實表未涵蓋，SBC 占營收 11.4%，淨回購大概率被稀釋抵銷。共識三年 EPS：FY2025A 23.49 到 FY2028E 40.42，年化約 19.8%。但 FY2025 基期偏低（Q3 2025 單季 EPS 僅 1.05），改用 FY2026E 30.29 到 FY2028E 40.42，年化約 15.5%。內生上界約 16%，三年口徑的 3.8pp 缺口可歸因於基期一次性壓低後的利潤率回復，不是無法歸因。EPS 分析師家數事實表未涵蓋；營收共識分別為 50 與 60 位分析師。跑道：份額已 26.8%，靠搶份額大約幾年內就會碰到 30%，所以跑道年數取中段；第二曲線有具名早期數據：Muse 上線六週逾 1,000 萬人設定、設定者約 25% 每日使用，Meta One 訂閱加試用逾 1,500 萬，合作廣告年化逾 150 億美元。外部預測的落差要盯：WARC 預估 Meta 廣告 2027 年只成長 12.1%，FY2027 共識營收卻要年增約 21%。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi12_ad_impressions_growth","f_kpi13_average_price_per_ad_gro","f_kpi5_share_based_compensation","f_kpi6_gaap_diluted_eps"],"verdict_values":{"growth":{"driver_mix":"價為主、量為輔：每則廣告均價 +14%，曝光 +10%；無併購；淨回購受 SBC 抵銷，事實表未涵蓋","runway_years":"5–9","runway_post_y5":"🟢","endo_ceiling_basis":"增量報酬約 9% × 再投資率約 180% ≈ 16%（推導見護城河題）；共識 FY2026E→FY2028E 年化 15.5%，落在上界內","segments":[{"item":"Family of Apps 廣告","value":"Q3 2026 63,060 百萬美元，年增 26%"},{"item":"Family of Apps 其他（WhatsApp 付費訊息、訂閱）","value":"約 1,100 百萬美元，年增 59%"},{"item":"Reality Labs 營收","value":"443 百萬美元，年減 6%；AI 眼鏡成長，Quest 衰退"},{"item":"Reality Labs 虧損","value":"2026 年指引 18,000–19,000 百萬美元，2027 年約 15,000 百萬美元，收斂約 3,000–4,000 百萬美元"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 81.75% 對 FY2025 82.0%，大致持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"2026 年數位廣告份額預估上升至 26.8%"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"均價 +14%，曝光仍 +10%"},{"signal":"EPS CAGR 高於營收 CAGR 逾 5pp","lit":false,"evidence":"FY2025→FY2027 共識營收年化約 24%，高於 EPS 成長"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FY2023 1.13、FY2024 0.87、FY2025 0.76；2026 年 Q3 自由現金流轉負，明年可能亮燈"},{"signal":"SBC／營收逾 5% 且上升","lit":true,"evidence":"Q3 SBC 占營收 11.4%；歷年趨勢事實表未涵蓋，從嚴計為亮燈"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"全球廣告支出 2026–2027 年仍成長，只是略降速"},{"signal":"產業估值倍數三年系統性下移","lit":false,"evidence":"事實表未涵蓋同業倍數史"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"自由現金流為負，維持性資本支出事實表未涵蓋，無法判讀"},{"signal":"停止投資新產能且收入三年內下滑","lit":false,"evidence":"資本支出仍在擴張"}]}}},"q4_capital":{"verdict":"資本配置偏弱。營運現金流幾乎全數投入資本支出，第三季自由現金流 −21 億美元；SBC 占營收 11.4%，回購抵銷能力下降；新設無投票權股讓籌資與發股工具都變多。","reasoning":"FCF／淨利轉換率（年度財報 2022–2025）：0.83、1.13、0.87、0.76，逐年下滑。Q3 營運現金流 32,786 百萬美元，資本支出 33,942 百萬美元，再投資約 104%。資產負債：季末現金與有價證券 824 億美元，債務 837 億美元，淨負債約 324 億美元（含租賃）。Q2 法說 CFO 已說資本結構要提高債務比重，並與 BlackRock 合建 1GW 資料中心。10-19 董事會核准新設無投票權 C 股，CFO 說用途含籌資、員工薪酬與收購。現金去向四分（回購、股息、併購、償債）的金額事實表未涵蓋。SBC 年化約 295 億美元，約為市值的 1.8%，在沒有回購抵銷時已超過 1.5% 的稀釋線。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_capital_expenditures","f_kpi5_share_based_compensation","f_kpi9_guidance_fy2026_capex","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無重大併購完成；CRED 收購僅見聚合站且未經一手來源證實"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購金額、回購均價與 10 年期公債殖利率事實表未涵蓋；Q3 自由現金流為負，回購能量受限"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"Q3 SBC 7,363 百萬美元 × 4 ÷ 市值 1,637,078 百萬美元 ≈ 1.8%／年毛稀釋；回購抵銷金額事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建算力與廣告本業，不靠併購；回購與股息金額、回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 2026–2028 年 EPS 年增約 15%，而且 2027 年折舊爬坡不能吃掉營業利益成長。本業動能支持這個前提，我們大致相信，但不給溢價。","reasoning":"前瞻本益比 21.2 倍（FY2026 共識 30.29）；以 FY2027 共識 34.8 計約 18.5 倍。Trailing 本益比 21.9 倍，在四個年度端點中位於 54.9 分位；這不是真正的五年分位，樣本只有四點。PEG 以 FY2026→FY2028 共識年化 15.5% 計約 1.37，落在合理區間。FY1 共識近三個月下修 2.85%（31.18→30.29），方向偏空。賣方平均目標價 785 美元（MarketBeat 2026-09-09，47 位，區間 595–1,000），高於現價約 22%；高低倍差 1.7 倍，分歧不大。短期上檔：FY2027 EPS 34.8 × 21 倍 ≈ 731 美元，約 +13.7%。中期上檔：FY2028 EPS 40.42 × 20 倍 ≈ 808 美元，約 +25.8%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比，以 FY2027 共識為主錨；FY2026 含一次性和解費用","tier":"大型廣告平台","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋；同業利潤率對照已在護城河題處理"},"fwd_pe":21.22,"peg":1.37,"percentile_5y":54.9,"val_light":"🟡","val_light_derivation":"前瞻 21.2 倍對共識年化 15.5% 的 EPS 成長，PEG 約 1.37；trailing 本益比在四個年度端點中位於 54.9 分位，屬中段。近三個月共識下修 2.85%，不支撐便宜論證，所以估值判為合理、不便宜。","upside_short_pct":13.7,"upside_mid_pct":25.8,"denominator_disputed":false,"denominator_note":"FY2026 GAAP EPS 含第三季 99 億美元和解費用，各家共識是否計入口徑不一，Q3 單季共識就分歧在 3.56–6.53。因此改以 FY2027 前瞻為主錨，分母本身不是多空爭點；爭點在 2027 年折舊爬坡，已放進情境樹。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把 AI 資本支出當成必然有回報。若 2027 年資本支出再大幅上修、營業利益同時停止成長，獲利與倍數會一起下修。","reasoning":"衰退信號十類亮一類（SBC 占營收 11.4%），FCF／淨利 0.76 逼近亮燈線，判黃燈。看錯的主路徑有三條。其一，資本支出：CFO 自承持續低估算力需求，並拒給 2027 年資本支出指引；Q1 上調資本支出後股價隔日跌近 10%。其二，法律成本：2026 年已認列 24 億加 99 億美元，未來數月還有多場青少年審判。其三，Q2 法說原本承諾 2026 營業利益高於 2025，本季改口成「剔除第三季法律費用後」才成立，承諾口徑被放寬。詳細裁定見反證紀錄。","fact_refs":["f_kpi3_free_cash_flow","f_kpi8_guidance_fy2026_total_ex","f_kpi6_gaap_diluted_eps","f_consensus_rev_3m_fy1_pct","f_kpi5_share_based_compensation"],"verdict_values":{"trap":{"verdict":"🟡","label":"資本密集化與法律成本雙壓，廣告本業尚未失速"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":30.29,"pe":21.22,"basis":"FY2026E 共識 EPS（GAAP 稀釋口徑，是否含第三季和解費用各家不一）；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[35.8,42.5,49.5,57.5,66.0],"base":[34.2,39.5,44.8,50.2,55.5],"bear":[28.5,27.0,28.5,30.5,33.0]},"pe":{"bull":26,"base":21,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.33,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-55,"hi":-35,"basis":"Bear 情境終點約 −28%（33.0 × 14 倍 ≈ 462 美元）。路徑低點取 FY2027 Bear EPS 27.0 × 14 倍 ≈ 378 美元，約 −41%；再加上資本支出指引或訴訟裁決的事件性超跌，取 −35% 至 −55%。事件衝擊參考：2026-04-29 上調資本支出指引後，股價隔日跌近 10%。","trigger_time":null},"basis":{"bull":"AI 讓廣告均價續升，Muse 與企業 API 在 2028 年後貢獻具名營收，Reality Labs 虧損依指引收斂，營業利益率回到 40% 以上","base":"廣告年增由 2026 年的二成多放緩至 2028 年後約一成，折舊爬坡吃掉部分營運槓桿，EPS 大致跟著 FY2027–FY2028 共識走","bear":"2027 年資本支出再大幅上修、折舊暴增，加上新一輪法律費用與廣告景氣轉弱（WARC 預估 Meta 2027 年廣告只成長 12.1%），EPS 兩年停滯後緩步回升"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CFO 自承持續低估算力需求，並拒給 2027 年資本支出指引；Q3 自由現金流 −21 億美元，費用年增 68%；10-K 自述在前沿模型上有強勁對手。","assumption":"AI 資本支出會透過廣告效率與新營收線在 2028 年前轉成可衡量的利潤。","consequence":"五年後虧 50% 最可能的故事：2027–2028 年資本支出逼近 2,000 億美元，折舊吃掉營業利益成長；Muse 變現慢於成本，廣告成長在 2027 年放緩到一成左右；EPS 卡在 30 上下，倍數壓到 14 倍，股價約 420 美元，再加上一場不利判決。","ruling":"部分採納。已用 30% 空頭機率與 −55% 回撤下緣定價；與唯一致命點重疊，以 2027 年 1 月指引作為對帳時點。","watch":"2027 年 1 月第四季法說的資本支出與營業利益指引；10-Q 折舊攤銷年增率","evidence_refs":["supply_demand_durability#1","competitive_share_entrants#1","capital_markets_pricing#2"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi9_guidance_fy2026_capex","f_kpi8_guidance_fy2026_total_ex"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 11.4%、年化約為市值 1.8%；新設無投票權 C 股，用途含籌資、員工薪酬與收購，且維持創辦人控制；Q2 法說已說要提高債務比重。","assumption":"AI 成功後每股盈餘會跟著總利潤成長。","consequence":"Muse 與企業業務成功，但靠發 C 股與舉債支應算力，每股經濟被稀釋，小股東沒有投票權可以制衡。","ruling":"採納為中度風險。C 股尚未發行籌資，先不下修 EPS 路徑；淨回購殖利率設為 0。","watch":"C 股掛牌後（預計 2027 年 1 月下旬）的發行公告；稀釋後股數年增率是否超過 1.5%","evidence_refs":["major_events#1"],"fact_refs":["f_kpi5_share_based_compensation","f_shares_diluted_m","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"10-K 揭露競爭主管機關訴訟與調查的數量和重要性近年增加；多起集體訴訟與股東衍生訴訟；Cambridge Analytica 證券集體訴訟正聲請認證；2026 年已認列 24 億加 99 億美元法律費用。","assumption":"法律成本是一次性的。","consequence":"變現越成功，社會容忍度越低；法律與合規成本變成每年都有的費用，壓住營業利益率。","ruling":"採納。不把和解費用當一次性加回；法律成本設為持續性成本，列入停損門檻。","watch":"每季新認列法律費用；青少年審判裁決；集體訴訟認證結果","evidence_refs":["regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"],"fact_refs":["f_kpi8_guidance_fy2026_total_ex"]},{"view":"價格已反映太多","evidence":"股價較前份上漲約 18%；FY1 共識近三個月下修 2.85%；Q2 財報 GAAP EPS 低於預期，Q3 營收指引中點低於共識；UBS、Baird 下修目標價。","assumption":"21 倍前瞻本益比已反映 AI 投資的不確定性。","consequence":"若市場仍用 2024 年輕資產時期的倍數錨定，資本強度上升後合理倍數應下移，現價就偏貴。","ruling":"反駁。FY2027 前瞻約 18.5 倍，對 15% 左右的 EPS 成長並不擁擠；26 週報酬 −4.6%、RSI 35.8，沒有動能過熱。但共識下修方向偏空，所以不給溢價。","watch":"FY1 與 FY2 共識三個月修正率；若轉為連續下修，將倍數錨往 18 倍調","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_fwd_pe_latest","f_week26_return_pct","f_rsi14"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 542.49 → 本次 642.62（+18.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=542.49","side_b":"本次 price_at_dd=642.62","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 542.49 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 542.49 美元：Bull 價 1,500、Bear 價 271，五年期望值 +55.8%，基準年化 10.3%，不對稱比 2.9","side_b":"本次情境、股價仍用 542.49 美元：Bull 價 1,716、Bear 價 462，五年期望值 +101.3%，基準年化 16.5%，不對稱比 12.15","ruling":"先換情境、股價不動：五年期望值多 45.5 個百分點，基準年化多 6.2 個百分點。不對稱比由 2.9 變為 12.15。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 542.49 美元：五年期望值 +101.3%，基準年化 16.5%，不對稱比 12.15","side_b":"本次情境、股價 642.62 美元：五年期望值 +69.9%，基準年化 12.6%，不對稱比 4.95","ruling":"再換股價、情境不動：起點價上漲 18.5%，五年期望值少 31.4 個百分點，基準年化少 3.9 個百分點，不對稱比由 12.15 降到 4.95。合計五年期望值比前份多 14.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AI 投資回報","cause":null,"prior_field":null,"side_a":"管理層：AI 投資已透過更強的參與度、推薦與變現效率，為廣告帶來大量增量營收（Q3 法說 2026-10-21，Susan Li）。剔除費用後營業利益年增 11%。","side_b":"第三季自由現金流 −21 億美元，費用年增 68%。CFO 自承持續低估算力需求，2027 年資本支出指引在 Q2、Q3 兩次法說都不給。","ruling":"可調和，屬程度差異。本業 AI 回報有證據（均價加速、轉換率提升），Muse 與 MSL 的回報則明說要更久。裁定採信本業回報、不採信新業務回報，新業務在情境樹只放進多頭。","evidence_level":"公司揭露加管理層陳述","settle_metric":"2027 年營業利益指引是否高於 2026 年（剔除法律費用）","if_then":["若 2027 年 1 月指引資本支出 ≥2,000 億美元，且不再承諾營業利益成長，則減碼至半倉","若資本支出 ≤2,000 億美元且營業利益指引續增，則加碼第二批 1/3"],"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2"]},{"axis":"管理層承諾兌現","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-07-29，Susan Li）：Q3 營收指引 610–640 億美元；2026 年仍預期營業利益高於 2025 年；資本支出 1,300–1,450 億美元。","side_b":"Q3 實績：營收 646 億美元，超過指引上緣；資本支出收窄至 1,350–1,450 億美元，下緣上調；營業利益承諾改成「剔除第三季法律費用後」才成立。","ruling":"營收承諾超額兌現；營業利益承諾口徑被放寬，屬改口。裁定以剔除法律費用口徑追蹤，但法律費用不視為一次性。","evidence_level":"新聞稿加逐字稿","settle_metric":"FY2026 剔除法律費用營業利益是否高於 FY2025 約 833 億美元","if_then":["若 FY2026 剔除法律費用營業利益仍低於 FY2025，則停止加碼，並把空頭機率上調至 35%","若高於且 2027 年續增，則維持原分批節奏"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"年輕用戶與參與度","cause":null,"prior_field":null,"side_a":"10-K 自述部分年輕用戶已轉向替代產品並減少使用 Meta 產品。","side_b":"Q3 法說：Instagram 人均時長創新高、年增雙位數；Facebook Reels 時長創新高；家族日活 36.4 億，年增 3%。","ruling":"可調和。總量參與度仍升，但年輕族群的分齡數據事實表未涵蓋，所以無法排除結構性流失被總量掩蓋。","evidence_level":"公司自述","settle_metric":"家族日活年增率與 Instagram 時長","if_then":["若家族日活連兩季年增 ≤0%，則減碼 1/3","若日活與時長續增，則維持"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方論證：GAAP 每股盈餘被法律費用壓低、自由現金流轉負、新設無投票權股預告稀釋，且青少年審判接連開庭，四件事都在 12 個月內。","side_b":"持有論證：剔除費用後營業利益年增 11%，均價加速，Q4 營收指引中點年增仍逾兩成，FY2027 前瞻約 18.5 倍。","ruling":"不賣。四件賣方論證中只有資本支出一件可能改變五年 EPS 路徑，它已設為唯一致命點並綁定日期；其餘屬成本與稀釋程度問題，已放進空頭情境與停損門檻。","evidence_level":"事實與推論混合","settle_metric":"2027 年 1 月指引","if_then":["若唯一致命點發生，則減碼至半倉","若青少年審判出現單案 ≥50 億美元不利判決，則減碼 1/3"],"evidence_refs":["regulatory_antitrust#1","major_events#2"]},{"axis":"前份漂移：裁決與部位","cause":"價格變動","prior_field":[],"side_a":"前份（2026-07-30，股價 542.49）：進場，首批 1/3","side_b":"本次股價 642.62，較前份高約 18%；裁決與部位交由本次情境與週線位置重新決定","ruling":"基本面輸入不主動改變方向。若結果改列，主因是股價上漲約 18% 壓縮報酬空間，不是論點轉弱。","evidence_level":"事實","settle_metric":"本次情境基準年化報酬","if_then":["若基準年化報酬低於 8%，則只維持首批、不加碼"],"evidence_refs":[]},{"axis":"前份漂移：機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤 −60%（單點）","side_b":"本次：多頭 25%、空頭 30%、最大回撤區間 −35% 至 −55%","ruling":"機率不變；共識三年口徑超過內生上界，空頭維持 30%。回撤改成區間：由 Bear 路徑低點乘以 14 倍再加事件超跌推出，不再用單點。Reality Labs 2027 年虧損指引約 150 億美元，加上剔除費用後營業利益仍成長，墊高了路徑低點。","evidence_level":"推論","settle_metric":"2027 年 Bear 路徑 EPS 27.0 是否被實績跌破","if_then":["若 FY2027 EPS 實績低於 28，則把回撤下緣下修至 −60%"],"evidence_refs":[]},{"axis":"前份漂移：基本面結論延續","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、估值合理（黃）、陷阱風險黃、護城河持平、跑道寬、品質複利成長、非循環股","side_b":"本次維持同一組結論","ruling":"Q3 新證據兩面都有。強化的是：均價加速到 +14%，營收超過指引上緣，Muse 六週逾 1,000 萬人設定。削弱的是：99 億美元和解費用、自由現金流轉負、CFO 不給 2027 年資本支出指引。兩邊抵銷，結論不變。","evidence_level":"新聞稿加逐字稿","settle_metric":"均價年增率與自由現金流","if_then":["若均價年增率連兩季低於 5%，則護城河方向改判下滑並減碼"],"evidence_refs":[]},{"axis":"前份漂移：加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","side_b":"首階現價可建；加碼待 2027 年 1 月法說：2027 資本支出指引 ≤2,000 億美元且營業利益指引續增，或回檔至 $557（FY2027 共識 16 倍）","ruling":"加碼條件改寫，理由有三。一，舊條件綁定的 10 月法說沒有給 2027 年資本支出，條件未觸發、也未否證，順延到慣例給年度指引的 1 月。二，2026 年資本支出已達 1,350–1,450 億美元，1,800 億美元門檻幾乎注定被超過，真正決定 EPS 的是營業利益能否續增，所以改綁營業利益指引。三，外部營收線已具名（Muse、Meta One 逾 1,500 萬、模型 API），不再列為條件。價位錨改用 FY2027 共識乘 16 倍。","evidence_level":"逐字稿","settle_metric":"2027 年 1 月指引","if_then":["若條件成立，則加碼第二批 1/3","若資本支出 ≥2,000 億美元且營業利益不再成長，則減碼至半倉"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Single Thing：2027 年 1 月第四季法說的 2027 年資本支出 ≥2,000 億美元，且不再承諾 2027 年營業利益高於 2026 年","ruling":"本次補設。情境樹裡對終端價值敏感度最大的單一變數，是 2027 年折舊對 EPS 的衝擊；它有明確日期、結果二元，適合作為唯一致命點。","evidence_level":"推論","settle_metric":"2027 年資本支出與營業利益指引","if_then":["若發生，則減碼至半倉並凍結加碼"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份漂移：停損門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼／清倉門檻（null）","side_b":"新增四條：廣告營收年增連兩季 <15% 減碼；2027 年資本支出 ≥2,000 億美元且無營業利益成長減碼至半倉；2027 年累計新法律費用 >100 億美元或 FTC 上訴取得拆分裁定則清倉；家族日活連兩季年增 ≤0% 減碼","ruling":"本次補設，讓論點的每一條主要假設都有對應的數字門檻與動作。","evidence_level":"方法","settle_metric":"各門檻按季檢查","if_then":["任一門檻觸發，即執行對應的減碼或清倉"],"evidence_refs":["regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"廣告本業增速驗證","type":"假設驗證","maps_to":"H1","metric":"Family of Apps 廣告營收年增率","threshold":"連兩季 <15%","action":"減碼 1/3","source_freq":"季度新聞稿","date":null,"evidence_refs":[]},{"n":2,"text":"2027 年資本支出與營業利益指引","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年資本支出指引、2027 年營業利益方向","threshold":"資本支出 ≥2,000 億美元且不再承諾營業利益成長","action":"減碼至半倉並凍結加碼","source_freq":"第四季法說","date":"2027-01","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2"]},{"n":3,"text":"青少年審判與多州訴訟成本","type":"風險","maps_to":"R2","metric":"單季新認列法律費用與判決金額","threshold":"2027 年累計 >100 億美元，或單案判決 ≥50 億美元","action":"減碼 1/3","source_freq":"10-Q／8-K","date":null,"evidence_refs":["regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"]},{"n":4,"text":"FTC 上訴取得拆分 Instagram 或 WhatsApp 的裁定","type":"清倉","maps_to":"R2","metric":"FTC 上訴裁決","threshold":"上訴法院發回並命令拆分或重組","action":"清倉","source_freq":"法院公告／8-K","date":null,"evidence_refs":["regulatory_antitrust#0"]},{"n":5,"text":"回檔加碼","type":"估值rearm","maps_to":"H1","metric":"股價對 FY2027 共識本益比","threshold":"股價 ≤557 美元（C 股配發後約減半對照）且基本面門檻未觸發","action":"加碼第二批 1/3","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":6,"text":"中國廣告主營收與硬體供應鏈受貿易行動影響","type":"風險","maps_to":"R4","metric":"管理層對中國經銷商營收與硬體關稅的揭露","threshold":"揭露政府行動已實質減少中國廣告營收","action":"減碼 1/3","source_freq":"10-Q 風險因素與法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":7,"text":"年度指引複審","type":"複審日期","maps_to":"H3","metric":"全年自由現金流與 Reality Labs 虧損","threshold":"複審","action":"重跑完整研究","source_freq":"第四季財報","date":"2027-01"}],"kill_metrics":[{"metric":"Family of Apps 廣告營收年增率","bear_threshold":"連兩季 <15% 則減碼","window":"2026Q4–2027Q4","source":"Meta 季度新聞稿","last_status":"ok"},{"metric":"2027 年資本支出指引（含融資租賃本金）","bear_threshold":"≥2,000 億美元且不再承諾營業利益成長，則減碼至半倉","window":"2027 年 1 月第四季法說","source":"Meta 第四季新聞稿與法說","last_status":"unknown"},{"metric":"新認列法律與和解費用","bear_threshold":"2027 年累計 >100 億美元則減碼；FTC 取得拆分裁定則清倉","window":"2026Q4–2027Q4","source":"10-Q、8-K、法院公告","last_status":"warning"},{"metric":"家族日活人數年增率","bear_threshold":"連兩季 ≤0% 則減碼","window":"2026Q4–2027Q4","source":"Meta 季度新聞稿","last_status":"ok"}],"action_conditions":{"rearm_trigger":"首階現價可建；加碼待 2027 年 1 月法說：2027 資本支出指引 ≤2,000 億美元且營業利益指引續增，或回檔至 $557（FY2027 共識 16 倍）","exec_line":"現價分三批建立，首批 1/3。第二批等 2027 年 1 月法說確認資本支出與營業利益指引，或股價回到 557 美元以下。第三批等 2027 年上半年自由現金流回正。2027 年 1 月下旬配發無投票權股後（效果等同一拆二），所有價位與每股數字約減半對照。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用含 99 億美元和解費用的 GAAP 數字與負自由現金流定價，低估了剔除費用後營業利益仍年增 11%、均價加速的本業動能。但 2027 年資本支出未知，這個理由只支撐合理價，不支撐溢價。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":null,"wait_for_price_condition":null,"prior_verdict":"進場","prior_role":"核心"},"thesis":{"H":[{"id":"H1","text":"廣告本業在用戶近飽和下，仍靠 AI 排序推升單價，維持高成長","2y":"FY2027 廣告營收年增 ≥18%，且曝光與每則廣告均價年增皆為正","5y":null,"10y":null,"threshold":"廣告營收年增 ≥18%；均價年增 ≥5%","source":"Meta 季度新聞稿","drift_rule":"TTM 偏離門檻連兩季 ≥5% 視為削弱，連三季 ≥10% 視為反轉"},{"id":"H2","text":"AI 投資在 2030 年前轉成可衡量的新營收線，不只是護住廣告","2y":null,"5y":"到 FY2030 年，Muse 訂閱、交易抽成、企業 API 與 WhatsApp 付費訊息合計揭露年營收 ≥200 億美元","10y":null,"threshold":"FY2028 起管理層揭露具名 AI 營收金額；FY2030 合計 ≥200 億美元","source":"年報分部揭露、法說","drift_rule":"TTM 偏離門檻連四季 ≥5% 視為削弱，連六季 ≥10% 視為反轉"},{"id":"H3","text":"資本強度在 2027 年見頂，自由現金流回正，Reality Labs 虧損依指引收斂","2y":"FY2027 全年自由現金流 >0，Reality Labs 虧損 ≤160 億美元","5y":null,"10y":null,"threshold":"全年自由現金流 >0；Reality Labs 虧損 ≤160 億美元","source":"10-K 現金流量表與分部損益","drift_rule":"TTM 偏離門檻連兩季 ≥5% 視為削弱，連三季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本支出與折舊爬坡吃掉營運槓桿。CFO 自承持續低估算力需求、拒給 2027 年指引；Q1 上調資本支出後股價隔日跌近 10%；資料中心擴張也可能因貿易爭端增加成本。","h_ref":"H3","clock":"🔥","threshold":"2027 年資本支出 ≥2,000 億美元且營業利益不再成長","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2","capital_markets_pricing#0","reg_tariff_export#2"]},{"id":"R2","text":"訴訟與監理成本已在兌現。2026 年認列 24 億加 99 億美元；未來數月有多場青少年審判；FTC 上訴拆分案；訴訟數量與重要性逐年增加；Cambridge Analytica 證券集體訴訟正聲請認證。","h_ref":"H1","clock":"⚡","threshold":"2027 年累計新法律費用 >100 億美元，或 FTC 取得拆分裁定","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"]},{"id":"R3","text":"注意力介面遷移。年輕用戶轉向替代產品，作業系統業者整合競品，前沿模型與硬體都有強勁對手。","h_ref":"H2","clock":"🐢","threshold":"家族日活連兩季年增 ≤0%，或 Instagram 人均時長轉為年減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R4","text":"地緣與貿易。服務中國廣告主的經銷商貢獻有意義營收，可能被政府行動削減；硬體製造集中亞洲少數代工廠（如 Goertek），受關稅與出口管制影響。","h_ref":"H1","clock":"🔥","threshold":"管理層揭露中國廣告營收已因政府行動實質減少","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"廣告景氣反轉。Q3 均價上漲有一部分來自相對去年的總經改善（法說原話），Q4 指引也含約 1% 匯率逆風。","h_ref":"H1","clock":"🔥","threshold":"每則廣告均價年增率連兩季 <5%","evidence_refs":[]}],"single_thing":{"description":"2027 年 1 月第四季法說的 2027 年指引：資本支出（含融資租賃本金）≥2,000 億美元，且管理層不再承諾 2027 年營業利益高於 2026 年。","why_fatal":"資本支出每多 400 億美元，按五年平均攤提的假設，每年多約 80 億美元費用（實際折舊年限事實表未涵蓋），約占 FY2026 共識淨利一成。若同時失去營業利益成長承諾，FY2027 共識 EPS 34.8 與 21 倍倍數會一起下修，是情境樹中對終端價值敏感度最高的單一變數。","if_happens":"減碼至半倉，凍結加碼，直到自由現金流連兩季回正。","how_monitor":"2027 年 1 月下旬的第四季新聞稿與法說；10-Q 的折舊攤銷與資本支出明細。","probability":"30%"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":18.47,"peg_fy2":1.19,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":23.49,"FY2026E":30.29,"FY2027E":34.8,"FY2028E":40.42},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS。FY2025A 基期偏低（Q3 2025 單季 1.05）；FY2026E 各家是否計入第三季 99 億美元和解費用口徑不一。2027 年 1 月下旬配發無投票權股後（效果等同一拆二），每股數字約減半。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Muse 登上 Meta 眼鏡","impact":"中","watch":"眼鏡付費訂閱數與 Reality Labs 營收"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年資本支出、費用指引","impact":"高","watch":"資本支出是否 ≥2,000 億美元、營業利益是否續增"},{"date":"2027-01","date_precision":"month","type":"other","event":"無投票權 C 股配發並開始交易","impact":"中","watch":"後續是否用 C 股籌資或作員工薪酬"},{"date":"2027-01","date_precision":"quarter","type":"regulatory","event":"美國多場青少年相關審判","impact":"高","watch":"判決金額與是否追加法律費用"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用含 99 億美元和解費用的 GAAP 數字與負自由現金流定價，低估了剔除費用後營業利益仍年增 11%、均價加速的本業動能。但 2027 年資本支出未知，這個理由只支撐合理價，不支撐溢價。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-4.64, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"requires_critic":[]}}
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
