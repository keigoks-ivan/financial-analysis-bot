你是 DD 管線 v20 的判斷層閘（gate），標的 MGA（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（42 條）
- `f_kpi0_sales`（q1_business）｜Sales（營收）＝10059 US$百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi1_adjusted_ebit`（q1_business）｜Adjusted EBIT＝683 US$百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi2_adjusted_ebit_margin`（q1_business）｜Adjusted EBIT margin＝6.8 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi3_income_from_operations_b`（q1_business）｜Income from operations before income taxes（稅前營業利益，GAAP 口徑；公司未單列 GAAP 營業利益率）＝552 US$百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi4_free_cash_flow`（q1_business）｜Free Cash Flow＝584 US$百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi5_adjusted_eps`（q1_business）｜Adjusted EPS＝1.83 US$｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi6_diluted_eps_gaap`（q1_business）｜Diluted EPS（GAAP）＝1.44 US$｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi7_fy2026`（q1_business）｜FY2026 指引（本次更新）＝Sales 41.2–42.0B；Adj EBIT margin 6.3–6.5%；Adj EPS 6.85–7.15（中點 7.00 不變）；FCF 1.85–1.90B —｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000749098/000110465926120352/tm2628312d1_ex99-1.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
  - 註記：共識 FY1 EPS 7.04（dd_numbers_extra.py consensus_revision，2026-10-31 快照）
- `f_peer_mga_gross_margin_pct`（q2_moat）｜MGA 毛利率＝14.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_operating_margin_pct`（q2_moat）｜MGA 營業利益率＝5.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_fcf_margin_pct`（q2_moat）｜MGA FCF 利潤率＝7.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_operating_margin_pct`（q2_moat）｜LEA 營業利益率＝3.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_fcf_margin_pct`（q2_moat）｜LEA FCF 利潤率＝3.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_operating_margin_pct`（q2_moat）｜APTV 營業利益率＝9.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_fcf_margin_pct`（q2_moat）｜APTV FCF 利潤率＝3.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6902_t_operating_margin_pct`（q2_moat）｜6902.T 營業利益率＝6.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6902.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6902_t_fcf_margin_pct`（q2_moat）｜6902.T FCF 利潤率＝1.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6902.T.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bwa_operating_margin_pct`（q2_moat）｜BWA 營業利益率＝10.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bwa_fcf_margin_pct`（q2_moat）｜BWA FCF 利潤率＝9.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.04 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.78 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.36 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝41735.76 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝42283.86 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.38 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 6.81 → 7.04（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝5039.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 6469.0、現金 1430.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝259.66 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.256 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝65.81 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝9.35 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 7.04，分子＝快照價 65.81｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.44 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝67.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝67.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝96.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.52 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝22127.01 USD m｜期間與口徑：2026-11-03／市值 17088.01 ＋ 淨負債 5039.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.14 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（7.05 → 7.04）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝12.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.43｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 65.96 / W52 60.29 / W104 49.69 / W250 48.96 / W250 13週斜率 -0.19%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝60.29 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.19 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Magna FY2025 annual filing says established electronics and semiconductor companies have entered or expanded presence in automotive, and disruptive innovators may offer solutions traditional suppliers cannot match
  - 來源：SEC Form 40-F FY2025 (Magna)（as_of 2026-03-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Competitor Lear acquired Kongsberg Interior Comfort Systems, IGB and Grupo Antolin seating business to strengthen seating vertical integration (Magna seating peer)
  - 來源：Nasdaq/Zacks, Will Magna's Seating Segment Remain a Core Strength in 2026?（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Magna 以 40-F 申報（非 10-K）。FY2025 六大客戶占合併銷售約 76%：GM 15%、Mercedes-Benz 15%、Ford 12%、BMW 12%、Volkswagen 11%、Stellantis 11%（2024 年六大約 73%）。
  - 來源：Magna Form 40-F FY2025 (SEC)（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 年 AIF 載明 Magna 供貨所有主要 OEM，但絕大多數銷售集中於六家客戶（GM、Mercedes-Benz、Ford、BMW、Volkswagen、Stellantis），並提示特定電動車型的內容集中風險。
  - 來源：Magna 2026 Annual Information Form (SEC 40-F exhibit)（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Magna Q3 2026 更新：因中國預期產量下降與車型組合不利而下修銷售區間；調整後 EBIT margin 指引收窄至 6.3%–6.5%，EPS 中位數不變（搜尋摘要轉述）
  - 來源：Magna Form 6-K (SEC)（as_of 2026-10-30）｜affects：thesis.R、valuation
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Magna 揭露巴西 CADE 針對汽車門鎖供應商的反壟斷正式行政程序（2019 年 5 月啟動），為舊案、狀態待確認
  - 來源：Magna Form 6-K FY2022 (SEC EDGAR)（as_of 2022-05-06）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Q1 2026 電話會議：Magna 毛關稅曝險約 $160M（前為 $200M），約一半為 IEEPA；Q1 未認列 IEEPA 退款；客戶去年吸收約 80% 關稅成本（來自搜尋摘要轉述，原文未逐字取得）
  - 來源：Magna Form 6-K Q1 2026 (SEC)（as_of 2026-05-04）｜affects：thesis.R、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：Q2 2026 電話會議：管理層稱美國提議的 50% 美國含量規則將對整個汽車產業有影響，未說明是否預期生效
  - 來源：Magna Form 6-K Q2 2026 (SEC)（as_of 2026-08-07）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2026-08 加美貿易談判中 Section 232 汽車關稅為主要爭點；美方據報提議降至 15%，加方認為過高
  - 來源：Stockwatch 2026-08-17（as_of 2026-08-17）｜affects：thesis.R、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Magna 揭露其為 Nexperia 受影響零件的直接買方（中國出口限制阻擋成品出貨），並提及美國鋁板供應商火災（約占車用鋁板產能 40%）可能造成延長停產
  - 來源：Magna 6-K（2025 Q3 相關檔）（as_of 2025-11-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Magna 管理層估計年化關稅曝險約 2.5 億美元，主要為加拿大、墨西哥輸入美國工廠的零件，另有少量來自中國與歐洲
  - 來源：Magna 6-K Q1 2025 財測電話會議（as_of 2025-05-02）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 銷售約 $10.06B，年減 4%（前年 $10.46B），主因 Lighting 與 Rooftop 出售、客戶價格讓步（net customer price concessions）、外幣走弱，新車型投產部分抵銷；前九個月銷售 $31.4B（+1%）；Adj. EBIT +11% 至 $683M。分部明細未取得。
  - 來源：Magna Q3 2026 results 6-K (SEC)（as_of 2026-10-30）｜affects：valuation、moat_trend
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Magna 自述部分產品組合預期長期衰退，包括手排變速箱、機械式全輪驅動系統
  - 來源：Magna 40-F FY2025 exhibit 99.1 (annual information form)（as_of 2026-03-31）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Magna 風險因子提及部分產品技術過時風險升高
  - 來源：Magna Form 6-K risk factors (SEC)（as_of 2026-02-15）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Magna Electronics 於 2025-09-03 向 NHTSA 申報召回 25E054（後視鏡頭可能顯示空白或倒置，涉 Ford、Chrysler 車款，聚合站稱約 250,292 輛）。
  - 來源：NHTSA Campaign 25E054（as_of 2025-09-03）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Magna 2022 Adjusted EBIT Margin expected ~4.3% per Jan 2023 update, below the 4.8%-5.0% range in Nov 2022 outlook (lower sales contribution, higher warranty, receivable provisions, higher engineering expense).
  - 來源：TipRanks: Magna updates 2022 outlook to reflect preliminary full year 2022 results（as_of 2023-01-19）｜affects：moat_trend、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Magna Q4 2008 loss of $148M and grim 2009 forecast
  - 來源：Manufacturing.net: Magna's 2009 Forecast Grim After $148M Q4 Loss（as_of 2009-02-27）｜affects：moat_trend、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Magna Q4 and full-year 2009 results (trough-cycle financials)
  - 來源：Newswire.ca: Magna announces fourth quarter and 2009 results（as_of 2010-03-01）｜affects：moat_trend、valuation
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：Magna Electronics 於 2025-09-03 向 NHTSA 申報召回 25E054（後視鏡頭畫面空白或倒置，聚合站稱約 250,292 輛）。
  - 來源：NHTSA Campaign 25E054（as_of 2025-09-03）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":133.4,"bear_5y_price":43.5,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":32.8,"ev5y_pct":26.8,"irr_base_pct":5.8,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":7.04,"pe":9.35,"basis":"FY2026共識調整後EPS 7.04美元（FY1）對現價65.81美元；終端倍數套在FY2031E，同為當年度前瞻口徑"},"eps":{"bull":[8.0,8.9,9.8,10.7,11.6],"base":[7.7,8.25,8.55,8.75,9.2],"bear":[6.4,5.0,4.6,5.2,5.8]},"pe":{"bull":11.5,"base":9.5,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.256,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MGA_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明 2026 全年調整後 EBIT margin 展望縮窄上調至 6.3%–6.6%，中點較前次高 15bp（原話："margin of between 6.3% and 6.6%, up 15 basis points at the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年調整後 EPS 展望為 $6.70–$7.30，中點較前次增加 $0.25（原話："adjusted EPS to between $6.70 and $7.30 per share. At the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年自由現金流展望中點上調至 $1.8B，較 5 月多 $100M（原話："cash flow outlook to $1.8 billion at the midpoint, up $100"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 給下半年 EPS 隱含值與 Q3／Q4 的 40-60 切分（原話："adjusted EPS of $3.76. We expect roughly a 40-60 split of"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說 Q3、Q4 的 margin 都預期年增（原話："margins to be up year-over-year in both the third and the"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：管理層給全年加權 growth over market（不含 Complete Vehicles）為 +1% 至 +3%（原話："expect positive growth over market for 2026 in the range of"）
- 2026-07-31｜CEO Swamy Kotagiri｜guidance：CEO 說合併口徑全年 growth over market 為 0% 至 2%（原話："0% to 2% positive growth over market for the full year."）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明全年調整後稅率維持 23%，下半年稅率將高於 23%（原話："expect an adjusted tax rate of 23%, which implies that our"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明 Q2 稅率較 23% 指引帶來 $0.09 EPS 好處，下半年會反轉（原話："tax line, we did have a $0.09 benefit in the quarter"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明下半年有機營收約小幅下滑，主要落在 Q3（原話："guidance at the midpoint would imply we're down kind of"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：CFO 說明下半年 P&V 因出售案減少的營收增為略逾 $400M（5 月為 $350M）（原話："about just over $400 million of revenue coming out of P&V"）
- 2026-07-31｜CFO Philip Fracassa｜guidance：管理層下調中國、上調北美與歐洲產量假設（原話："units, respectively, while we reduced our China production"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 拆解 Q2 margin 橋：營運表現、量與其他為最大正貢獻（約 75bp）（原話："The largest benefit came from operational performance"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 Q2 淨關稅成本年減貢獻約 25bp margin（原話："Lower net tariff costs year-over-year added around 25 basis"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 2026 全年淨關稅逆風與 2025 相近（原話："we currently expect that our net tariff headwind for full"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 IEEPA 關稅已付逾 $100M、約半數已退回（原話："we probably paid just over $100 million in IEEPA tariffs."）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 IEEPA 退款預期有 80%–90% 回饋客戶（原話："pass backs to our customers and would expect customers to"）
- 2026-07-31｜CEO Swamy Kotagiri｜margin：CEO 說明營運卓越帶來的年度 margin 擴張節奏（35–40bp／年，’23 至 ’26 累計約 200bp）（原話："expansion. As we finished this year, we would add about 200"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明 Q2 的 75bp 中營運卓越占大半，與 35–40bp 區間一致（原話："operational excellence is -- I would say a majority of that"）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 說明新合約經濟條件改善，ʼ27 起新專案預期有較佳經濟性（原話："We do expect better economics on those programs."）
- 2026-07-31｜CEO Swamy Kotagiri｜margin：CEO 說明首半年到下半年回收偏重下半年的節奏仍在，但斜率較去年趨緩（原話："continues, but the slope has softened this year."）
- 2026-07-31｜CFO Philip Fracassa｜margin：CFO 表示不預期明年有 margin 拖累（回收項目）（原話："operational excellence momentum and the other things we're"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CFO 說明下半年有小幅未回收成本逆風（DRAM／記憶體等）已納入展望（原話："unrecovered cost headwind in the second half, but we've"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CEO 指出宏觀與地緣政治（中東、貿易政策）仍不確定（原話："macroeconomic and geopolitical conditions remain somewhat"）
- 2026-07-31｜CEO Swamy Kotagiri｜risk：CEO 對美國 50% 本地含量提案表示不評論貿易政策（原話："I think, Ty, I usually refrain from making comments on"）
- 2026-07-31｜CFO Philip Fracassa｜risk：CFO 說明 Complete Vehicles 銷售下滑，因全成本認列客戶量降低（原話："Sales in complete vehicles declined $96 million organically"）
- 2026-07-31｜CEO Swamy Kotagiri｜competition：CEO 說明中國營收約 65% 來自中國 OEM，西方 OEM 在中國失去份額短期會影響銷售（原話："China is about 65% with the Chinese OEMs."）
- 2026-07-31｜CEO Swamy Kotagiri｜competition：CEO 說明對中國 OEM 與供應商進歐洲的防禦論述：平台策略與製造整合能力為護城河（原話："And the technology and the manufacturing DNA and the"）
- 2026-07-31｜CEO Swamy Kotagiri｜product：CEO 公布與歐洲 OEM 的駕駛／乘員監控系統專案得標（原話："We were recently awarded a driver and occupant monitoring"）
- 2026-07-31｜CEO Swamy Kotagiri｜product：CEO 公布奇瑞 800V 二速 eDrive 專案得標（原話："Our recently awarded 800V 2-speed eDrive program with Chery"）
- 2026-07-31｜CEO Swamy Kotagiri｜customer：CEO 提及獲 GM 五項供應商獎（原話："Most recently, Magna earned 5 General Motors Supplier of"）
- 2026-07-31｜CEO Swamy Kotagiri｜customer：CEO 說 2028 年業務已訂單逾 90%（原話："Our business pipeline continues to grow with over 90% of"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明剩餘約 9M 股 NCIB 計畫於 11 月初到期前買完（原話："We are planning to repurchase the remaining shares"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明年度資本配置：提高股息、買完整個 NCIB（逾 $1.5B）（原話："$1.8 billion of free cash flow, we raised the dividend and"）
- 2026-07-31｜CFO Philip Fracassa｜capital_allocation：CFO 說明資本支出預期維持歷史區間（低 4% 水準）（原話："And then managing CapEx within that historical range of 4%"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 說明 Q2 末評等機構口徑槓桿為 1.4x（原話："we ended the quarter with a 1.4x rating agency leverage"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 說明非汽車領域擴張需符合報酬準則，並非為多角化而多角化（原話："The key point is that we are not pursuing diversification"）
- 2026-07-31｜CEO Swamy Kotagiri｜capital_allocation：CEO 回答產能時提及 40 餘座工廠已重組、關閉或縮編（原話："And you've heard me talk about 40-plus plants either"）
- 2026-07-31｜CFO Philip Fracassa｜commitment：CFO 預期未來自由現金流轉換率維持相近水準（原話："we do expect to convert a similar amount of earnings to"）
- 2026-07-31｜CEO Swamy Kotagiri｜commitment：CEO 承諾非汽車機會會在 11 月投資人日提供標準、專案與路徑細節（原話："incremental growth and high return value creation over"）
- 2026-07-31｜CEO Swamy Kotagiri｜commitment：CEO 表示非汽車領域將非常挑剔（原話："So all in all, I think we are going to be very selective."）
- 2026-07-31｜CFO Philip Fracassa｜commitment：CFO 說明 2027 年 growth over market 將重新加速（原話："sets us up well for growth over market to reaccelerate in"）

### 問答異常語氣（迴避／改口／保留）
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Mark Delaney (Goldman)：已贏得的非汽車業務，能否給出已訂單規模｜答法：CEO 拒絕給任何數字，說不想逐案談，只說是 meaningful wins，留待投資人日
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Dan Levy (Barclays)：非汽車業務能否對 $40B+ 營收基期形成實質成長｜答法：CEO 未給規模，說「decide what material means」，改約 11 月再談
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Tom Narayan (RBC)：2028 年已訂單的 margin 輪廓與中國 OEM 占比｜答法：CEO 明說不談各客戶或未來的 margin 輪廓，也未答中國 OEM 占比，留待投資人日
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Jack Joyce (BofA)：2027 年 growth over market 隱含值｜答法：CEO 說 too early，不給 2027 數字，改談 2026 全年
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：Ty Collin (CIBC)：美國 50% 本地含量規則的影響｜答法：CEO 表示不評論貿易政策，只說需敏捷因應，未量化影響
- MGA_Q2_2026_Earnings_Call_20260731.md｜問：James Picariello (BNP)：Q2 關稅回收是否提前、有無一次性項目｜答法：CEO 稱淨關稅與商務回收較去年為負，CFO 則稱 Q2 關稅有 25bp 正貢獻、全年中性；兩人口徑不同，CFO 另補「Maybe we'll do a little better than that. I mean who knows.」

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 3 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 2 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 3 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B 觀望偏進場（衛星候選）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Adj EBIT margin 結構性擴張至 6.0-6.5%（vs FY24 5.2%）","columns":{"2Y 驗證點":"FY26 全年 Adj EBIT margin ≥ 6.0%（guidance 中緣）","5Y 驗證點":"FY29 Adj EBIT margin ≥ 7.0%（操作槓桿全兌現）","10Y 驗證點":"FY35 EBIT margin 維持 7%+（不再回落至 5%）","具體數字門檻":"FY26 全年 Adj EBIT margin ≥ 6.0%；FY27 ≥ 6.5%","信息來源":"Q1 2026 法說會（已 reaffirm guidance）+ 公司 2026 outlook","漂移觸發條件":"連 2 季 TTM &lt; 5.5% → 削弱；連 4 季 &lt; 5.0% → 反轉"}},{"id":"H2","text":"FCF 持續 .6-2.0B/年，capex 從 .55B 峰值穩定下行","columns":{"2Y 驗證點":"FY26 FCF 達 .7B 中緣","5Y 驗證點":"FY29 累積 FCF .0-9.5B","10Y 驗證點":"FY35 capex/Revenue &lt; 4.5%（vs 高峰 6.0%）","具體數字門檻":"FY26 FCF ≥ .6B；capex/Rev &lt; 4.5%","信息來源":"公司 FY26 guidance + Q1 26 法說會 capex 路徑","漂移觸發條件":"連 2 季 FCF/EBITDA &lt; 50% → 削弱"}},{"id":"H3","text":"市場估值倍數均值回歸至 5Y 均（PE 11-14x）","columns":{"2Y 驗證點":"Fwd PE 12 月內回升至 10-11x","5Y 驗證點":"5Y 內 PE 至少觸及 14x（5Y 均 -25%）","10Y 驗證點":"10Y 區間 8-18x（不超過 5Y 高 25x）","具體數字門檻":"Fwd PE 24 月內 ≥ 11x（5Y 均下緣）","信息來源":"Macrotrends / GuruFocus 5Y PE 數據","漂移觸發條件":"連 2 季維持 &lt; 9x → 結構性 de-rating 持續"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"GM / Ford / Stellantis 工會罷工或新模型延後 → 北美營收 -10%、EBIT margin -150bps","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"UAW / Unifor 談判進度、OEM Q-on-Q production 量","警戒閾值":"單季 Adj EBIT margin &lt; 5.0%（連 2 季減倉）"}},{"id":"R2","text":"第 2 個 Fisker 級別 EV 客戶（如 Lucid / Rivian / VinFast / 中國新勢力）破產 → 認列 0M-0M 沖銷","columns":{"對應假設":"H1 + H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"EV 客戶 cash burn 月數、訂單 cancel 公告","警戒閾值":"單客戶沖銷 &gt; 5% 季度 EBIT → 連 4 季影響 → 大動作"}},{"id":"R3","text":"OEM 大規模 in-source 趨勢 + 中國新勢力擠壓 → MGA 全球市佔結構性流失","columns":{"對應假設":"H1 + H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"MGA 全球 organic growth vs 全球 LVP 差距；中國市場 design wins","警戒閾值":"連 8 季 organic growth underperform LVP &gt; 200bps → 結構性失去份額"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":64.58,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MGA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Magna International Inc."},"oneliner":"營收持平、定價權在車廠，EPS成長靠自救式利益率擴張與每年約一成股數回購；前瞻9.4倍的便宜建立在高檔利益率與排除重組費用的調整後盈餘上，等2027年2月財測驗證6.4%利益率是不是起跳點。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MGA_20261103/scenario.json","answers":{"q1_business":{"verdict":"Magna 賺的是全球車廠按車型專案採購車身結構、座椅、電驅與ADAS零件及整車代工的錢，六大客戶占銷售76%；錢卡在車廠議價這一節：每年例行價格讓步、原物料回收慢一到兩季，近兩年獲利改善來自自身營運效率與出售低利益率業務，不是定價。","reasoning":"Q3 2026營收100.6億美元、年減4%：出售車頂與照明減1.65億美元，另有客戶價格讓步與匯率；有機年減2.1%，對比Magna加權產量年減2.6%，不含整車的growth over market約+1%。調整後EBIT 6.83億美元、利益率6.8%（年增90bp），其中營運量與其他項目貢獻約120bp（商務回收含Q4提前、營運卓越），原物料（DRAM、樹脂、鋁）拖累約50bp。GAAP稅前營業利益5.52億美元、GAAP稀釋EPS 1.44美元，對調整後EPS 1.83美元，差距主要是重組與出售相關費用。TTM毛利率14.7%、營業利益率5.5%。分部：Q3 Power & Vision利益率6.6%，Seating全年利益率展望3.1–3.3%（換線拖累），Complete Vehicles改附加價值認列後營收降、利益率升；分部營收占比事實表未涵蓋。單點依賴：六大客戶占2025年銷售76%（2024年73%），GM與Mercedes-Benz各約15%，前兩大合計約30%，未過40%警戒但集中度上升；中國營收約65%來自中國車廠。FY2026指引：營收412–420億美元、利益率6.3–6.5%、調整後EPS 6.85–7.15美元（中點7.00不變）、FCF 18.5–19億美元。產業時鐘判IV（溫和收縮）：產量持平偏降、價格讓步持續、供應商收緊資本支出；但產量水位低於前高、零件庫存偏低，屬溫和下行，不是高檔反轉。","fact_refs":["f_kpi0_sales","f_kpi1_adjusted_ebit","f_kpi2_adjusted_ebit_margin","f_kpi3_income_from_operations_b","f_kpi4_free_cash_flow","f_kpi5_adjusted_eps","f_kpi6_diluted_eps_gaap","f_kpi7_fy2026","f_peer_mga_gross_margin_pct","f_peer_mga_operating_margin_pct"],"verdict_values":{"revenue_quality":"中：營收由車廠產量與專案量產節奏決定，沒有經常性收入；Q3有機年減2.1%略優於加權產量−2.6%。2026年FCF含約5億美元一次性EV專案回收（Q3法說CFO），Q3利益率含部分Q4提前的商務回收，看盈餘品質要扣掉這兩項。","unit_econ_note":"每車零件含量×車廠產量；新專案經濟條件比舊專案好（Q2法說CFO），但每年有價格讓步；原物料中鋼鋁多有轉售或指數化、樹脂約40%指數化，DRAM與電子零件須逐案向車廠議價回收。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"營收隨車廠產量擺動、利益率對產量與原物料敏感：2008年第四季虧損1.48億美元、2022年利益率掉到約4.3%；資本支出約營收3.6–4%"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性、溫和下行後回升：北美輕型車產量2026年−0.2%、2027年−2.1%、2028年+4.6%（ITR），全球2027年約9,264萬輛持平、中國下修（GlobalData與MarkLines），沒有結構性緊缺或過剩；供給可逆性高（Magna四年重組或關閉41個以上事業單位，供應商收緊資本支出核准）","bargaining":{"up":"中：鋼鋁多有轉售或指數化；樹脂僅約40%指數化；DRAM與電子零件漲價要向車廠議價回收，Q3淨拖累約50bp","down":"弱：六大車廠占76%，每年例行價格讓步；原物料與關稅回收靠商務談判，去年客戶吸收約八成關稅成本","geo":"加拿大與墨西哥廠供應美國，美國50%本地含量提案與第232條汽車關稅談判未定；中國業務約65%來自中國車廠"},"profit_pool_dir":"利潤池往車廠與電子、半導體端移；機械傳動件長期萎縮，電驅、ADAS感測與整車代工（中國車廠歐洲在地化、Waymo改裝）是Magna想接住的部分","tam_table":{"expanded":false,"reason":"成熟車用零件市場，論點承重在利益率與回購，不在滲透率或份額擴張；全球產量約9,200萬輛持平已寫在供需判讀"}}}},"q2_moat":{"verdict":"護城河方向→（穩定）：執行力在變強，定價權沒有。機制是規模與全產品線帶來的專案得標與製造整合能力，得標後鎖定車型生命週期，但每代車型重新招標、定價在車廠手上；同業比較營業利益率居中、FCF利益率僅次BorgWarner。","reasoning":"執行面擴大：調整後EBIT利益率由2025年約5.6%到2026年指引中點6.4%，營運卓越今年貢獻約50bp、明年預估再35–40bp（Q3法說CEO），Q3在全球產量年減約3%下仍擴張90bp。定價面縮減：例行價格讓步持續、原物料回收慢一到兩季、六大客戶占比由73%升到76%。兩者相抵判穩定。同業TTM營業利益率：MGA 5.5%、Lear 3.7%、Denso 6.9%、Aptiv 9.8%、BorgWarner 10.2%；FCF利益率：MGA 7.5%（含一次性EV回收）、BorgWarner 9.2%、Aptiv 3.7%、Lear 3.6%、Denso 2.0%。同業ROIC與投入資本事實表未涵蓋，算不出ROIC spread，以營業與FCF利益率代理。評分：執行7（重組與營運卓越已兌現、評等A-），定價4（價格讓步、原物料回收要談判）。","fact_refs":["f_peer_mga_operating_margin_pct","f_peer_mga_fcf_margin_pct","f_peer_mga_gross_margin_pct","f_peer_lea_operating_margin_pct","f_peer_lea_fcf_margin_pct","f_peer_aptv_operating_margin_pct","f_peer_aptv_fcf_margin_pct","f_peer_6902_t_operating_margin_pct","f_peer_6902_t_fcf_margin_pct","f_peer_bwa_operating_margin_pct","f_peer_bwa_fcf_margin_pct","f_kpi2_adjusted_ebit_margin"],"verdict_values":{"moat":{"mechanism":"規模與全產品線（車身結構、座椅、電驅與四驅、ADAS、整車代工）帶來的專案得標與製造整合能力；得標後鎖定車型生命週期，每代車型重新招標，定價權在車廠","execution":7,"pricing":4,"grade":"C","trend":"→","trend_evidence":"執行面擴大（利益率2025年約5.6%→2026年指引中點6.4%，營運卓越每年35–50bp）、定價面縮減（例行價格讓步、原物料回收時差、六大客戶占比73%→76%），兩者相抵判穩定","competitor_notes":[{"name":"LEA","strategy_note":"座椅與電子系統直接對手，營業利益率3.7%低於Magna，正以收購Kongsberg、IGB與Antolin座椅業務垂直整合，壓的是Magna利益率最低的座椅分部"},{"name":"APTV","strategy_note":"電子架構與ADAS領先者，營業利益率9.8%但FCF利益率只有3.7%；區域式架構由它與Bosch、Continental主導，Magna電子在這塊是跟隨者"},{"name":"6902.T","strategy_note":"Denso營業利益率6.9%略高於Magna、FCF利益率2.0%偏低；以日系車廠為主，與Magna客戶重疊有限"},{"name":"BWA","strategy_note":"BorgWarner營業利益率10.2%、FCF利益率9.2%為同組最高，是Magna電驅與四驅的直接對手，說明傳動領域能賺到比Magna整體更高的利益率"}],"peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，只能比營業與FCF利益率；Magna TTM FCF利益率含2026年約5億美元一次性EV回收","threats":[{"level":"🟡","text":"電子與半導體廠擴大車用布局、區域式架構整合控制器，壓縮傳統電子含量；Magna ADAS仍在得標（歐洲車廠駕駛監控），目前屬點對點競爭","p":30,"evidence_refs":["competitive_share_entrants#0","substitute_technology#1"]},{"level":"🟡","text":"Lear收購Kongsberg、IGB與Antolin座椅業務做垂直整合，壓迫Magna座椅（全年利益率3.1–3.3%）","p":25,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"手排變速箱、機械式四驅長期衰退與部分產品技術過時；但Q3仍拿到2028年量產的分動箱與後驅、前驅模組，替代速度慢","p":35,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"車廠自製一體壓鑄與沖壓（Q3法說分析師提問）；管理層稱未見負面影響，未證，列監測","p":20,"evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×高周轉（推定）：稅後營業利益率約5%（6.4%×78%），投入資本周轉率事實表未涵蓋，依接單生產、資本支出約營收3.6%的製造模式判讀，待補資料驗證","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是駕駛、決策者是車廠工程與採購、付款者是車廠；零件需求由車輛產量衍生，屬可延後的需求：全球產量2026–27年約9,200萬輛持平、北美2027年預測−2.1%，景氣衰退時車廠減產會直接傳到Magna"},{"item":"決策層級","level":"🟡","text":"替代決策在車型專案層級：得標後鎖定5–7年車型生命週期（2028年業務已訂逾90%，Q2法說），但每代車型重新招標、六大客戶占76%、供應商眾多；車廠也在評估自製壓鑄與沖壓，管理層稱未見影響（未證）"},{"item":"價值鏈分配","level":"🔴","text":"價值多被車廠與電子、半導體上游拿走：每年例行價格讓步、DRAM與樹脂漲價要逐案談判回收、Q3原物料淨拖累約50bp；同業營業利益率3.7–10.2%，零件環節整體只拿薄利"},{"item":"社會容忍度","level":"🟢","text":"零件價格不受社會或監管定價限制，優勢也不靠授權；政策風險在貿易面（美國50%本地含量提案、第232條關稅），已列入風險，不構成定價上限"}],"roiic":"事實表未涵蓋（投入資本與增量資本口徑缺）；內生上界用假設值約8–10%代入，未證","reinvest_rate":"約24%（代理）：FY2026 FCF指引中點18.75億美元約等於調整後淨利，扣除約5億美元一次性EV回收後約13.75億美元，差額約5億美元視為淨再投資；稅後營業利益約20.8億美元（416億營收×6.4%×78%）；D&A與營運資金拆分事實表未涵蓋","endo_ceiling":2.0,"formula_note":"內生成長上界＝增量ROIC×再投資率≈8–10%（假設）×24%≈2%／年；業務口徑交叉驗證：市場產量持平＋不含整車growth over market約+1–3%（公司口徑）→營收內生成長約1–3%。共識EPS成長超出部分來自利益率擴張與回購，不是再投資。"}}}},"q3_growth":{"verdict":"五年後跑道🟡：終端市場成熟、產量持平，營收內生成長約1–3%；EPS成長主要靠利益率擴張與回購，第二曲線（整車代工中國車廠、Waymo改裝、非車用）管理層未量化。","reasoning":"成長拆解：量持平、價為負（例行價格讓步）、併購為負（出售照明與車頂），EPS成長來自利益率擴張與淨回購（近12個月稀釋股數減約6%）。共識調整後EPS：FY2026 7.04、FY2027 7.78、FY2028 8.36美元；以FY2025調整後約5.74美元為基期，三年年複合約13%，FY2026→2028兩年年複合約9%。共識營收FY2026約417億、FY2027約423億美元，年增約1%。內生上界約2%／年（見護城河段），缺口約11個百分點可歸因：2026年利益率+80bp貢獻了FY2026 EPS年增22%的大部分，之後每年營運卓越35–40bp與淨回購4–6%；不是倍數重估。跑道：利益率由6.4%每年加35–40bp，到7%以上約2年，之後成長回到市場加growth over market加回購。衰退信號亮2個（EPS成長遠高於營收、部分產品被替代技術壓縮）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_fy2026","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量持平、價為負（例行價格讓步）、併購為負（出售照明與車頂）；EPS成長來自利益率擴張與淨回購（近12個月稀釋股數減約6%）","runway_years":"不適用滲透率口徑；利益率由6.4%每年加35–40bp，到7%以上約2年，之後成長回到市場加growth over market加回購","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段內生上界約2%／年（增量報酬假設8–10%×再投資率約24%，與市場持平加growth over market +1–3%交叉驗證）；共識FY2025→2028調整後EPS年複合約13%，缺口約11個百分點可歸因：2026年利益率+80bp、之後每年營運卓越35–40bp與淨回購4–6%，不是倍數重估","segments":[{"item":"Power & Vision","value":"Q3利益率6.6%（年增150bp，管理層歸因營運執行而非商務回收），扣出售與匯率有機營收約+2%"},{"item":"Seating","value":"2026全年利益率展望3.1–3.3%；Ford Louisville換線2027年中回升、BMW Spartanburg影響延續到2027"},{"item":"Body Exteriors & Structures","value":"Q3 EBIT金額與利益率年增；大型壓鑄有客戶興趣，車廠自製趨勢管理層稱未見影響；營收占比事實表未涵蓋"},{"item":"Complete Vehicles","value":"Q3營收年減8%，改附加價值認列後營收降、利益率升；歐洲產能約15萬輛、中國約18萬輛，Waymo改裝在Mesa量產"}],"decay_signals":[{"signal":"EPS成長顯著高於營收成長（差>5pp）","lit":true,"evidence":"FY2026 EPS中點+22%對營收約−1%；共識三年EPS年複合約13%對營收約持平"},{"signal":"TAM萎縮或被替代技術壓縮","lit":true,"evidence":"公司自述手排變速箱、機械式四驅長期衰退；區域式架構壓縮傳統控制單元含量"},{"signal":"毛利率連2季年減","lit":false,"evidence":"TTM毛利率14.7%高於2025年14.3%，利益率連季擴張"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"Q3不含整車growth over market約+1%，全年約+1%（較前次指引下修但仍為正）"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"不適用：價格由車廠合約決定"},{"signal":"FCF對淨利連2年<0.75","lit":false,"evidence":"2025、2026年FCF約等於調整後淨利（含一次性回收；扣除後約73%，列觀察）"},{"signal":"SBC對營收>5%且逐年上升","lit":false,"evidence":"SBC金額事實表未涵蓋，但稀釋股數淨減少"},{"signal":"TAM之外的產業估值倍數近3年系統性下移","lit":null,"evidence":"事實表未涵蓋產業倍數序列"},{"signal":"維護性資本支出占FCF>60%","lit":null,"evidence":"事實表未涵蓋維護性資本支出拆分"},{"signal":"停止投資新產能且營收3年內下滑","lit":false,"evidence":"營收2023–2026約持平略降，但資本支出仍約營收3.6%、2027–28年有新專案量產；列觀察"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律好：近一年買回逾2,500萬股、稀釋股數減約6%，Q3股息加回購回饋6.58億美元，淨負債對調整後EBITDA低於1倍、評等A-與A3；沒有大型併購，管理層只考慮小型補強。隱憂是2026年回購力道有約5億美元一次性EV回收與出售案資金撐腰，2027年經常性FCF約14億美元能否撐住新的約2,580萬股授權（約流通股一成），要看利益率。","reasoning":"FCF轉換：FY2026 FCF指引18.5–19億美元，約等於調整後淨利（CFO），扣除約5億美元一次性EV回收後約73%。現金去向（2026年）：Q3資本支出3.07億美元、全年約15億美元（營收約3.6%）；Q3股息1.29億、回購5.29億美元（790萬股，均價約67美元）；沒有收購，出售照明與車頂回收資金。負債：淨負債約50.4億美元（含租賃）、評等機構口徑槓桿1.4倍，CFO表示不需再降槓桿，會把資產負債表容量用在回購。回購以約67美元買入，對FY2026共識EPS 7.04美元的盈餘殖利率約10.5%；SBC金額事實表未涵蓋，但稀釋股數淨減少。債務到期結構與加權利率事實表未涵蓋。","fact_refs":["f_kpi4_free_cash_flow","f_kpi7_fy2026","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年沒有收購，2026年是出售照明與車頂，沒有已實現的併購報酬可評"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"Q3以5.29億美元買回790萬股、均價約67美元，對FY2026共識EPS 7.04美元的盈餘殖利率約10.5%；10年期公債殖利率事實表未涵蓋，須高於8.5%本項才不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"近12個月稀釋股數減約6%（Q3法說CFO），淨稀釋為負；SBC金額事實表未涵蓋"}]},"governance":{"capital_returns":[{"item":"2026年資本回饋","value":"Q3股息1.29億加回購5.29億美元；近12個月買回逾2,500萬股，舊授權已在10月買完"},{"item":"新回購授權","value":"約2,580萬股（約流通股一成），11月生效"},{"item":"資金來源","value":"FY2026 FCF指引18.5–19億美元，含約5億美元一次性EV回收；另有照明與車頂出售款"},{"item":"槓桿與評等","value":"淨負債對調整後EBITDA低於1倍、評等口徑1.4倍；S&P A-、Moody's A3，展望穩定"}]}}},"q5_valuation":{"verdict":"現價65.81美元隱含調整後EPS照共識由7.04走到8.36美元、前瞻本益比維持約9倍。我部分相信：利益率與回購大致可兌現，但便宜建立在排除重組費用的調整後盈餘與四年最高的利益率上，經常性FCF口徑約12倍；合理偏便宜，不是低估。","reasoning":"前瞻本益比9.35倍（FY2026共識7.04美元）、FY2027約8.46倍；trailing GAAP本益比21.4倍受Q1出售相關待售資產損失4.85億美元扭曲，不採用。EV約221億美元（市值171億加淨負債50.4億），EV/S 0.52。股息殖利率2.26%，加回購的股東殖利率約一成以上（2026年部分資金來自一次性回收與出售案）。FY1共識近3個月上修3.4%、最近一次快照微降0.14%。26週漲12.2%、股價在52週均線60.3美元之上，週線均線已多頭排列但250週均線斜率約−0.2%走平。同業倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_net_debt_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_slope_w250_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026共識調整後EPS）為主，經常性FCF殖利率與EV/S為輔","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，未涵蓋同業本益比或EV倍數，無法做倍數對照；以自身前瞻本益比與經常性FCF殖利率判讀"},"fwd_pe":9.35,"peg":0.7,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比9.35倍、FY2027共識約8.5倍；PEG以FY2025調整後約5.74美元為基期約0.7，以FY2026→2028兩年年複合9%算約1.0。表面便宜，但有三點拉回：一、調整後EPS排除每年都有的重組費用，扣除約5億美元一次性EV回收的經常性FCF約13.75億美元，FCF殖利率約8%、相當約12倍；二、EV/S 0.52處自身四個年度端點最高、股價營收比處96分位，利益率也在四年最高，景氣循環股在利益率高檔時的低本益比不是安全邊際；三、現價與賣方目標價均值約67–70美元相近。判合理偏便宜。五年分位不填：事實表只有四個年度端點，不是五年連續序列。短期上行＝FY2027共識7.78美元×現行9.35倍≈72.7美元（+10.5%）；中期＝FY2028共識8.36美元×9.35倍≈78.2美元（+18.8%）。","upside_short_pct":10.5,"upside_mid_pct":18.8,"denominator_disputed":true,"denominator_note":"調整後與GAAP差距持續且大：Q3 GAAP稀釋EPS 1.44美元對調整後1.83美元，2025年GAAP稀釋EPS 2.93美元對調整後約5.74美元；排除項含每季都有的重組費用（分析師提問指Q3 Power & Vision歐洲重組約7,600萬美元）。2026年FCF又含約5億美元一次性EV回收。以9.35倍前瞻本益比論便宜不成立，改看經常性FCF約12倍。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把自救式利益率當成景氣中性水準：6.4%建立在產量偏平、商務回收順利、原物料可轉嫁的前提上，一次北美與歐洲減產10–15%就可能回到2022年的4%出頭；其次是調整後盈餘排除每年都有的重組費用，便宜程度被高估。陷阱判🟡：衰退信號亮兩個，資產負債表與FCF讓它不是價值陷阱，但也不是複利股。","reasoning":"依據見反證紀錄三個視角：論點失敗（景氣衰退加關稅加原物料回收失敗、或含量被新進者與替代技術侵蝕）、論點成功但股東經濟變差（效率收益被車廠價格讓步拿走、回購資金部分一次性）、價格已反映太多（EV/S與股價營收比處四年最高、經常性FCF口徑約12倍）。26週漲12.2%、RSI 54，動能沒有過熱。","fact_refs":["f_week26_return_pct","f_rsi14","f_ev_s_percentile","f_ps_percentile","f_kpi6_diluted_eps_gaap","f_kpi5_adjusted_eps"],"verdict_values":{"trap":{"verdict":"🟡","label":"高檔利益率的景氣循環股"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":7.04,"pe":9.35,"basis":"FY2026共識調整後EPS 7.04美元（FY1）對現價65.81美元；終端倍數套在FY2031E，同為當年度前瞻口徑"},"eps":{"bull":[8.0,8.9,9.8,10.7,11.6],"base":[7.7,8.25,8.55,8.75,9.2],"bear":[6.4,5.0,4.6,5.2,5.8]},"pe":{"bull":11.5,"base":9.5,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.26,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"max_dd":{"lo":-55,"hi":-35,"basis":"以過去下行週期推估：2008年第四季虧損、2022年利益率掉到約4.3%、美國輕型車銷售歷次峰谷跌20–35%。溫和衰退（北美加歐洲產量−10%）時EPS約5.5美元×本益比7.5–8倍≈41–44美元，跌約35%；深度衰退時EPS約4.5美元×7–8倍≈32–36美元，跌約45–52%，加上恐慌超跌到約−55%。範圍−35%～−55%","trigger_time":null},"basis":{"bull":"營運卓越每年+40bp且產量溫和成長，2030年利益率約7.5%；整車代工與中國車廠業務放大、growth over market到中個位數；每年淨減股約5%；本益比回到前份記載的5年均值區間11–14倍下緣11.5倍（同業本益比事實表未涵蓋，無同業對照）","base":"FY2027–28略低於共識（原物料回收延後、產量偏軟），之後一次溫和產量下行讓利益率持平一年；2027年後利益率每年只加10–20bp，低於管理層的35–40bp；淨減股每年約4%已含在每股EPS路徑內，淨回購殖利率填0避免重複；終端9.5倍約等於現行前瞻9.35倍，不靠倍數重估","bear":"2027–28年北美與歐洲產量衰退10–15%，加上關稅轉嫁失敗，利益率回落到2022年的4%出頭，EPS谷底約4.6美元，第五年只回到5.8美元；本益比7.5倍（成長熄火、景氣谷底）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2008年第四季虧損1.48億美元、2009年谷底；2022年利益率因銷量、保固與應收準備掉到約4.3%（低於當時4.8–5.0%指引）；美國輕型車銷售歷次峰谷跌20–35%；Q3已因中國減產與組合不利下修全年營收","assumption":"營運卓越帶來的利益率可以抵銷產量下行，6.4%是地板","consequence":"北美與歐洲產量年減10–15%時利益率回到4%出頭，EPS約4.5美元，景氣谷底本益比7倍→股價約30–35美元，五年後虧近50%","ruling":"部分採納：放進Bear情境（30%）與最大回撤−35%～−55%；不當基本情境，因Q3在全球產量年減約3%下利益率仍擴張90bp，且評等A-、淨負債對EBITDA低於1倍，衰退時不會被迫增資。與Single Thing部分重疊：財測中點低於6.4%是這個故事的第一個訊號","watch":"北美加歐洲輕型車產量季度年減幅；單季調整後EBIT利益率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#1"],"fact_refs":["f_kpi2_adjusted_ebit_margin","f_kpi7_fy2026"]},{"view":"論點失敗","evidence":"FY2025年報：電子與半導體廠擴大車用布局、新進者可提供傳統供應商做不到的方案；公司自述手排變速箱與機械式四驅長期衰退、部分產品技術過時風險升高；Lear以收購強化座椅垂直整合","assumption":"Magna在新架構（電驅、ADAS、大型壓鑄）拿到的含量足以補上傳統產品萎縮","consequence":"growth over market轉負，營收每年縮1–2%，利益率擴張被固定成本吃掉","ruling":"暫不採納為主情境：Q3仍拿到2028年量產的分動箱與後驅、前驅模組及SmartLatch加量，Q2拿到歐洲車廠駕駛監控與奇瑞800V電驅；但替代是慢變數，列為長期風險與門檻監測","watch":"不含整車growth over market；投資人日揭露的新得標專案中電驅與ADAS占比","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"六大客戶占銷售由73%升到76%；Q3營收年減部分來自客戶價格讓步；原物料（DRAM）回收延到2027年再議","assumption":"營運卓越省下的成本留在Magna，不會在下一輪報價被車廠要走","consequence":"利益率擴張停在6.5%附近，EPS成長只剩回購，五年EPS年複合降到3–4%，股價表現跟股息加回購差不多","ruling":"採納為基本情境的保守處理：基本情境2027年後利益率每年只加約10–20bp，低於管理層的35–40bp","watch":"FY2027利益率指引中點；法說揭露的價格讓步拖累","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","end_markets#0"],"fact_refs":["f_kpi0_sales"]},{"view":"論點成功但股東經濟變差","evidence":"2026年FCF含約5億美元一次性EV專案回收，回購也用到出售照明與車頂的資金；Q2法說管理層拒絕量化非車用（機器人、資料中心）業務規模，留待投資人日","assumption":"經常性FCF足以每年買回約一成股數，多餘現金不會流向報酬未證的非車用多角化","consequence":"2027年回購降到約4–5%，或資金轉往非車用、稀釋報酬","ruling":"部分採納：基本情境淨減股每年約4%而非10%；投資人日若揭露大額非車用投資計畫，重跑資本配置判斷","watch":"投資人日資本配置框架；2027年各季回購金額","evidence_refs":[],"fact_refs":["f_kpi4_free_cash_flow","f_kpi7_fy2026"]},{"view":"價格已反映太多","evidence":"26週漲12.2%、站上52週均線；EV/S 0.52處自身四個年度端點最高、股價營收比處96分位；賣方目標價均值約67–70美元，與現價65.81美元相近；調整後EPS排除每年都有的重組費用（Q3 GAAP稀釋EPS 1.44美元對調整後1.83美元）","assumption":"前瞻9.35倍本益比代表便宜","consequence":"以經常性FCF約13.75億美元計，FCF殖利率約8%、相當約12倍，在利益率高檔時並不便宜；若2027年利益率不再擴張，股價沒有重估空間","ruling":"採納：估值判合理偏便宜而非低估，不追價，等財測驗證後且股價不高於72美元才建倉","watch":"股價對FY2027共識本益比是否超過9.5倍；FY2027經常性FCF","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_week26_return_pct","f_ev_s_percentile","f_ps_percentile","f_fwd_pe_latest","f_kpi6_diluted_eps_gaap","f_kpi5_adjusted_eps"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 64.58 → 本次 65.81（+1.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=64.58","side_b":"本次 price_at_dd=65.81","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 64.58 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 64.58 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 64.58 美元：Bull 價 133.4、Bear 價 43.5，五年期望值 +29.2%，基準年化 6.2%，不對稱比 2.18","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.18。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 64.58 美元：五年期望值 +29.2%，基準年化 6.2%，不對稱比 2.18","side_b":"本次情境、股價 65.81 美元：五年期望值 +26.8%，基準年化 5.8%，不對稱比 2.02","ruling":"再換股價、情境不動：起點價上漲 1.9%，五年期望值少 2.4 個百分點，基準年化少 0.4 個百分點，不對稱比由 2.18 降到 2.02。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利益率是否結構性","cause":null,"prior_field":null,"side_a":"管理層（Q3 2026法說，2026-10-30，CFO Fracassa與CEO Kotagiri）：6.4%是進入2027年的結構性起跳點，Q4利益率將升到約7.3%，2027年營運卓越再加35–40bp","side_b":"同場CFO承認Q3含Q4提前的商務回收、Q4商務項目可能轉負、原物料逆風持平或更大；Q2法說（2026-07-31）CFO稱不預期明年有回收項目拖累，Q3改說未回收部分要到2027年再談；Q2法說CEO與CFO對關稅回收是正是負口徑不一","ruling":"可調和（程度差異）：方向採管理層、幅度打折。一致的部分是營運卓越確實在產量下滑時撐住利益率（Power & Vision利益率+150bp，管理層歸因執行而非回收）；不一致的是2026年數字含一次性項目。這是本次觀望的唯一約束：6.4%能不能當起跳點，要等Q4實績與FY2027財測","evidence_level":"管理層口述加公司6-K","settle_metric":"Q4 2026調整後EBIT利益率（隱含約7.3%）與FY2027利益率指引中點（2027年2月）","if_then":["若Q4 2026利益率≥7.0%且FY2027指引中點≥6.7%，且股價≤72美元→建首倉","若FY2027指引中點<6.4%→不建倉；持有者減碼至一半","若股價在財測前先漲過75美元而證據未到→不追","若股價跌到58美元以下而Q4實績與財測沒有變差→分批反買"],"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"axis":"growth over market下修","cause":null,"prior_field":null,"side_a":"Q2法說（2026-07-31）：2026年不含整車growth over market +1–3%、合併0–2%，CFO稱2027年將重新加速","side_b":"Q3法說（2026-10-30）CFO：全年合併約持平、不含整車約+1%，原因是中國德系車廠Q3減產約28%與北美、歐洲客戶Q4停產","ruling":"可調和（程度差異）：下修來自客戶組合與暫時停產，不是丟專案；但一季內下修讓2027年重新加速的說法未證，第三條論點門檻設在不含整車+1%，不採管理層說的低到中個位數","evidence_level":"管理層口述","settle_metric":"FY2027 growth over market（2027年2月財測與各季法說）","if_then":["若2027年前兩季不含整車growth over market皆為負→停止加碼","若2027年全年≥+2%→第三條論點升為主要成長來源"],"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"A競爭面惡化：電子與半導體廠擴大車用布局、Lear座椅垂直整合、區域式架構壓縮傳統控制器含量；C其他結構變數惡化：美國50%本地含量提案、第232條汽車關稅談判、手排與機械四驅長期衰退","side_b":"B結構轉好：中國車廠在歐洲在地化（小鵬、廣汽在Graz）與Waymo改裝帶來整車代工需求；2028年業務已訂逾90%；供應商收緊資本支出核准，產能紀律改善","ruling":"雙向拉鋸，偏競爭與關稅壓力：轉好的證據沒有金額（管理層拒絕量化非車用與整車代工規模），惡化的證據有來源與機制；論點只押利益率與回購，不押結構轉好","evidence_level":"公司年報風險因子、法說、產業報導","settle_metric":"投資人日揭露的整車代工與非車用規模；不含整車growth over market","if_then":["若投資人日量化整車代工與非車用營收目標且2028年達營收5%以上→第三條論點上調","若美國實施50%本地含量規則→停止加碼並重跑情境"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","reg_tariff_export#1","reg_tariff_export#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"前瞻9.35倍、FY2027約8.5倍；股息殖利率2.3%加每年約一成股數回購；評等A-、淨負債對EBITDA低於1倍；FCF指引年內兩度上調、Q3利益率超預期；投資人日可能給出7%以上的中期利益率目標，股價可能在財測前先走","side_b":"便宜建立在排除重組費用的調整後盈餘與四年最高的利益率上，經常性FCF口徑約12倍；2027年產量偏軟、原物料回收延到2027年；現價已接近賣方目標價均值","ruling":"不採：等待成本約3個月、錯過的上行約10%（FY2027共識維持現行倍數），驗證失敗的下行約12–17%（FY2027 EPS約7.26美元×7.5–8倍）；不對稱不支持現在搶先","evidence_level":"公司6-K與法說、事實表估值欄","settle_metric":"FY2027財測利益率中點","if_then":["若投資人日後股價漲過75美元而財測未出→不追","若財測達標且股價≤72美元→建首倉"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"前份漂移：整體評級、陷阱、護城河方向","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-24）：整體評級B、陷阱🟡、護城河方向→","side_b":"本次：整體評級B、陷阱🟡、護城河方向→","ruling":"三欄不變。Q2、Q3新證據兩面相抵：利益率連兩季超預期、FCF指引年內兩度上調；但六大客戶占比升到76%、全年growth over market由0–2%下修到約持平、原物料逆風擴大。執行變強、定價沒變強，方向仍判穩定；衰退信號仍亮兩個","evidence_level":"公司6-K與法說","settle_metric":"FY2027利益率指引與growth over market","if_then":["若FY2027不含整車growth over market轉負→護城河方向改判↓並重跑"],"evidence_refs":["customer_concentration_credit#0","supply_demand_durability#1"]},{"axis":"前份漂移：估值結論、類型、循環位置、成長跑道、情境機率與最大回撤、裁決與角色","cause":"方法變動","prior_field":["val","archetype","cycle_position","runway_post_y5","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：估值結論🟢；類型、循環位置、五年後成長跑道未判；沒有情境機率與最大回撤；裁決與角色依當時矩陣","side_b":"本次：估值結論🟡；類型景氣循環；中循環；五年後跑道🟡；情境機率20／50／30；最大回撤−35%～−55%；裁決與角色由程式依本次輸入決定","ruling":"本次改用景氣循環視角並檢查盈餘分母：EV/S與股價營收比處自身四年最高、利益率也在四年最高；調整後EPS排除每年都有的重組費用，扣除一次性EV回收後的經常性FCF約12倍。股價只漲1.9%、FY2026共識近3個月上修3.4%，前瞻倍數其實略降，所以估值結論下修來自方法，不是價格或新證據","evidence_level":"事實表估值欄、公司法說","settle_metric":"FY2027經常性FCF與利益率","if_then":["若FY2027經常性FCF≥15億美元且利益率≥6.7%→估值結論可回到🟢"],"evidence_refs":[]},{"axis":"重啟條件（進場與加碼）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"（前份未設重啟條件）","side_b":"Q4 2026利益率≥7.0%且FY2027利益率指引中點≥6.7%，同時股價≤72美元","ruling":"前份只有觀望偏進場的結論，沒有可執行的進場或加碼條件；本次把觀望的唯一約束（6.4%利益率能否當起跳點）寫成事件錨，並加股價上限，避免證據未到時加碼或追價","evidence_level":"公司財測時程","settle_metric":"FY2027財測","if_then":["條件全數成立→建首倉；任一不成立→維持觀望"],"evidence_refs":[]},{"axis":"停損與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"單季 Adj EBIT margin < 5.0%（連 2 季減倉）","side_b":"單季調整後EBIT利益率<5.0%連2季→減碼至一半；FY2027利益率指引中點<6.4%→不建倉、持有者減碼；年度利益率<5.0%且經常性FCF<10億美元→清倉","ruling":"沿用前份5.0%減碼線，新增財測與FCF兩條；2026年利益率已在6.3–6.5%，5.0%離現況太遠，只當減碼線不當預警，預警交給財測中點","evidence_level":"公司季報與財測","settle_metric":"單季利益率、FY2027財測、經常性FCF","if_then":["任一減碼條件觸發→減碼至一半","清倉條件觸發→清倉"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":["single_thing"],"side_a":"（前份未設 Single Thing）","side_b":"2027年2月公布的FY2027財測，調整後EBIT利益率中點低於6.4%","ruling":"前份沒有唯一致命點；本次選利益率指引，因為它是EPS最大的單一敏感度（產量、原物料回收、商務項目都匯總在這個數字），而且是一次揭曉的事件","evidence_level":"公司財測時程","settle_metric":"FY2027利益率指引中點","if_then":["中點<6.4%→不建倉、持有者減碼至一半"],"evidence_refs":[]},{"axis":"論點門檻調整（第一、二條）","cause":"新證據","prior_field":["thesis.H1","thesis.H2"],"side_a":"FY26 全年 Adj EBIT margin ≥ 6.0%；FY27 ≥ 6.5%｜FY26 FCF ≥ .6B；capex/Rev < 4.5%（前份原文金額缺字，應為16億美元）","side_b":"第一條：FY2026≥6.3%、FY2027≥6.7%｜第二條：FY2027經常性FCF≥15億美元、FCF對調整後淨利≥80%","ruling":"FY2026指引6.3–6.5%與FCF 18.5–19億美元已高於前份門檻，舊門檻失去區辨力；FCF改用扣除約5億美元一次性回收的經常性口徑","evidence_level":"公司6-K財測","settle_metric":"FY2027利益率與經常性FCF","if_then":["新門檻未達→對應論點削弱並停止加碼"],"evidence_refs":[]},{"axis":"前份第三條論點（倍數均值回歸）退休","cause":"方法變動","prior_field":["thesis.H3"],"side_a":"Fwd PE 24 月內 ≥ 11x（5Y 均下緣）","side_b":"退休：不以倍數重估當論點；倍數只在情境樹終端倍數表達（基本情境9.5倍）","ruling":"倍數回升不是公司能控制的經營假設；本次基本情境的重估貢獻接近零，避免報酬依賴估值重估；第三條論點改為growth over market","evidence_level":"方法調整","settle_metric":"不適用","if_then":["若日後要以倍數回升為進場理由→須另給市場錯在哪的具體證據"],"evidence_refs":[]},{"axis":"前份風險門檻沿用與調整","cause":"新證據","prior_field":["thesis.R1","thesis.R2","thesis.R3"],"side_a":"R1：單季 Adj EBIT margin < 5.0%（連 2 季減倉）｜R2：單客戶沖銷 > 5% 季度 EBIT｜R3：連 8 季 organic growth underperform LVP > 200bps","side_b":"前份R1沿用為景氣衰退減碼線；前份R2降為監測條件（新興EV客戶占銷售低於5%，2026年反而收到約5億美元EV專案回收）；前份R3沿用為份額流失門檻","ruling":"三條門檻都保留、沒有退休；EV客戶沖銷降為監測，因新證據顯示曝險小","evidence_level":"FY2025年報、Q3法說","settle_metric":"單季利益率、單一客戶沖銷、不含整車growth over market","if_then":["單一客戶沖銷超過當季調整後EBIT的5%→減碼一級"],"evidence_refs":["customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"Single Thing：FY2027財測調整後EBIT利益率中點低於6.4%","type":"Single Thing","maps_to":"H1","metric":"FY2027調整後EBIT利益率指引中點","threshold":"<6.4%","action":"不建倉；持有者減碼至一半，Bear機率調到35%重跑情境","source_freq":"公司年度財測（6-K），每年2月","date":"2027-02","evidence_refs":["supply_demand_durability#1"]},{"n":2,"text":"第一條論點驗證：Q4 2026利益率是否站上7%","type":"假設驗證","maps_to":"H1","metric":"Q4 2026調整後EBIT利益率","threshold":"≥7.0%（管理層隱含約7.3%）","action":"與FY2027財測合併判斷是否解除觀望","source_freq":"季報（6-K）","date":"2027-02"},{"n":3,"text":"重啟進場：利益率起跳點確認且價格未追高","type":"估值rearm","maps_to":"H1","metric":"Q4 2026利益率、FY2027利益率指引中點、股價","threshold":"Q4≥7.0%且FY2027中點≥6.7%，股價≤72美元（約FY2027共識9.3倍）","action":"建首倉，第二批待2027年Q1利益率年增確認","source_freq":"季報與財測","date":"2027-02"},{"n":4,"text":"第二條論點驗證：扣除一次性回收後的FCF","type":"假設驗證","maps_to":"H2","metric":"FY2027 FCF（不含EV專案回收）","threshold":"≥15億美元","action":"未達→停止加碼，回購假設改為每年淨減股3%重跑情境","source_freq":"年報與季報現金流量表","date":"2028-02"},{"n":5,"text":"關稅與貿易規則吸收失敗","type":"風險","maps_to":"R2","metric":"季度淨關稅對利益率的拖累；美國本地含量規則","threshold":"拖累≥30bp連2季，或美國實施50%本地含量規則且公司未給出吸收方案","action":"停止加碼；Bear機率調到35%重跑情境","source_freq":"季度法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"n":6,"text":"景氣衰退減碼線（沿用前份）","type":"減碼","maps_to":"R3","metric":"單季調整後EBIT利益率","threshold":"<5.0%連2季","action":"減碼至一半","source_freq":"季報（6-K）","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"利益率與現金同時失守","type":"清倉","maps_to":"H2","metric":"年度調整後EBIT利益率與經常性FCF","threshold":"年度利益率<5.0%且經常性FCF<10億美元","action":"清倉","source_freq":"年報","date":null},{"n":8,"text":"份額流失（沿用前份門檻）","type":"風險","maps_to":"R4","metric":"不含整車growth over market","threshold":"連4季為負，或連8季累計落後產量200bp以上","action":"停止加碼；連8季成立則減碼至一半","source_freq":"季度法說","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0","customer_concentration_credit#1"]},{"n":9,"text":"供應鏈中斷（晶片出口限制、鋁板供應）","type":"風險","maps_to":"R5","metric":"供應中斷造成的營收損失或財測下修","threshold":"單季因供應中斷損失營收≥3%，或公司因此下修全年財測","action":"停止加碼","source_freq":"季度法說與6-K","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":10,"text":"保固與召回費用","type":"風險","maps_to":"H1","metric":"單季保固與召回費用對利益率的拖累","threshold":"≥20bp","action":"停止加碼並追查是否為系統性品質問題","source_freq":"季報與NHTSA召回公告","date":null,"evidence_refs":["major_events#2","product_recall_warning#0"]},{"n":11,"text":"新興EV客戶沖銷（前份第二條風險降為監測）","type":"風險","maps_to":"H2","metric":"單一客戶應收或資產沖銷","threshold":"超過當季調整後EBIT的5%","action":"減碼一級","source_freq":"季報","date":null},{"n":12,"text":"投資人日複審","type":"複審日期","maps_to":"H1","metric":"中期利益率目標、FCF轉換率、資本配置與非車用投資規模","threshold":"中期利益率目標低於7%，或揭露大額非車用投資計畫","action":"依中期框架複審本判斷","source_freq":"一次性活動","date":"2026-11"}],"kill_metrics":[{"metric":"單季調整後EBIT利益率","bear_threshold":"<5.0%連2季","window":"2026Q4–2028Q4","source":"公司季報（6-K）","last_status":"ok"},{"metric":"FY2027調整後EBIT利益率指引中點","bear_threshold":"<6.4%","window":"2027年2月財測","source":"公司財測（6-K）","last_status":"unknown"},{"metric":"經常性FCF（扣除EV專案回收）","bear_threshold":"FY2027低於12億美元","window":"FY2027","source":"公司年報與季報現金流量表","last_status":"unknown"},{"metric":"不含整車growth over market","bear_threshold":"連4季為負","window":"2027–2028","source":"公司季度法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"來源是2022年5月的6-K，案件2019年啟動，事實表沒有之後的進度、罰款金額或受影響營收，證據過舊、無法判斷是否仍未決；沒有金額可入情境，日後年報再揭露才重新評估"}],"action_conditions":{"rearm_trigger":"Q4 2026利益率≥7.0%且FY2027利益率指引中點≥6.7%，同時股價≤72美元","exec_line":"條件成立後分兩批：財測公布後一週內建首批，2027年Q1財報確認利益率年增後建第二批；任何減碼或清倉條件觸發即停止","holding_cap":"≤3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等2027年2月Q4財報與FY2027財測：Q4利益率≥7.0%且FY2027利益率指引中點≥6.7%；屆時股價≤72美元才建首倉。投資人日（2026年11月）只當提前訊號，不單獨構成進場理由"},"thesis":{"H":[{"id":"H1","text":"調整後EBIT利益率由2025年約5.6%結構性墊高到6.4%以上，之後靠營運卓越每年再加30–40bp","2y":"FY2027調整後EBIT利益率≥6.7%","5y":"FY2030≥7.0%","10y":null,"threshold":"FY2026≥6.3%（指引下緣）；FY2027≥6.7%","source":"公司季報與年度財測（6-K）；Q3 2026法說CEO Kotagiri與CFO Fracassa的起跳點說法","drift_rule":"TTM利益率對6.4%基準：連2季低於6.1%（偏離≥5%）→削弱；連3季低於5.8%（偏離≥10%）→反轉"},{"id":"H2","text":"扣除一次性EV專案回收後，經常性FCF每年≥15億美元，撐住股息與每年淨減股4%以上","2y":"FY2027經常性FCF≥15億美元、稀釋股數年減≥4%","5y":"FY2027–2031累計FCF≥80億美元","10y":null,"threshold":"FY2027 FCF≥15億美元（不含EV回收）；FCF對調整後淨利≥80%","source":"公司年度FCF指引與季報現金流量表（6-K）；Q3 2026法說CFO稱回收不再發生下仍維持高轉換率","drift_rule":"TTM經常性FCF對15億美元基準：連2季偏離≥5%（低於14.25億）→削弱；連3季偏離≥10%（低於13.5億）→反轉"},{"id":"H3","text":"市場產量持平下，靠中國車廠業務、整車組裝附加價值模式與新得標專案維持正的growth over market，抵銷傳統產品萎縮","2y":"FY2027不含整車growth over market≥+1%","5y":"2027–2031年不含整車growth over market平均≥+2%","10y":null,"threshold":"FY2027不含整車≥+1%","source":"公司每季法說揭露的growth over market；Q2 2026法說（2028年業務訂單逾90%）","drift_rule":"不含整車growth over market連4季為負→削弱；連6季低於−2%→反轉"}],"R":[{"id":"R1","text":"原物料（DRAM、樹脂）回收失敗加上Q4商務項目轉負，Q4利益率達不到7%，坐實Q3有提前認列","h_ref":"H1","clock":"⚡","threshold":"Q4 2026調整後EBIT利益率<7.0%；或2027年任一季利益率年減≥50bp連2季","evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"id":"R2","text":"北美貿易規則變動（第232條汽車關稅、美國50%本地含量提案）讓加拿大與墨西哥供美零件的關稅成本轉嫁不出去；目前毛關稅曝險約1.6億美元，客戶去年吸收約八成","h_ref":"H1","clock":"🔥","threshold":"季度淨關稅對利益率拖累≥30bp連2季，或50%本地含量規則實施","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"id":"R3","text":"景氣下行：北美與歐洲產量年減10%以上，利益率回到2022年的4%出頭、FCF腰斬，回購暫停","h_ref":"H2","clock":"🔥","threshold":"北美加歐洲輕型車產量年減≥5%連2季；或單季利益率<5.0%連2季（減碼）","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#1"]},{"id":"R4","text":"份額與含量流失：電子與半導體新進者、車廠自製壓鑄與沖壓、Lear座椅垂直整合、傳統傳動件衰退，加上六大客戶占76%讓議價更弱","h_ref":"H3","clock":"🐢","threshold":"不含整車growth over market連8季累計落後產量200bp以上（沿用前份）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"供應鏈中斷：Magna是Nexperia受影響晶片的直接買方，美國鋁板供應商火災曾威脅車廠停產","h_ref":"H1","clock":"⚡","threshold":"單季因供應中斷損失營收≥3%，或因此下修財測","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"2027年2月公布的FY2027財測，調整後EBIT利益率中點低於6.4%","why_fatal":"利益率是EPS最大的敏感度：每50bp約對應2億美元EBIT、約0.65美元EPS（約FY2027共識的8%）；產量、原物料回收、商務項目轉負都匯總在這個數字。中點低於6.4%等於管理層自己否定6.4%是起跳點，基本情境2027年EPS會落到約7.2美元而非7.7美元，FCF與回購同步縮","if_happens":"不建倉；持有者減碼至一半；Bear機率由30%調到35%重跑情境","how_monitor":"Q4 2026財報與FY2027財測新聞稿（6-K）；投資人日中期利益率框架當提前訊號","probability":"約30%（2027年2月揭曉）"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.46,"peg_fy2":0.64,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":5.74,"FY2026E":7.04,"FY2027E":7.78,"FY2028E":8.36},"fy_end_month":12,"eps_basis":"調整後稀釋EPS（Non-GAAP，美元，12月年度）；FY2025A約5.74美元由Q3 2026法說「FY2026中點7.00美元較去年增22%」回推，非事實表直接值；同年GAAP稀釋EPS為2.93美元"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"紐約投資人日：中期財務框架、營運卓越進度與非車用機會細節","impact":"高","watch":"中期利益率目標是否≥7%、FCF轉換率與回購承諾、非車用投資規模"},{"date":"2026-11","date_precision":"month","type":"other","event":"新一輪約2,580萬股回購授權生效","impact":"中","watch":"Q4實際回購金額"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"其餘照明業務出售案交割","impact":"低","watch":"Power & Vision營收基期與利益率"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"加美貿易談判（第232條汽車關稅）與美國本地含量規則進展","impact":"中","watch":"淨關稅對利益率的拖累"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026財報與FY2027財測","impact":"高","watch":"FY2027利益率指引中點是否≥6.7%、經常性FCF指引"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"Ford Louisville座椅新專案年中量產爬坡","impact":"中","watch":"Seating分部利益率回升"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=12.2, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
