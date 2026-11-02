你是 DD 管線 v20 的判斷層閘（gate），標的 LEA（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（48 條）
- `f_kpi0_gaap_net_sales`（q1_business）｜營收（GAAP net sales）＝5773.0 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi1_core_operating_earnings_`（q1_business）｜Core operating earnings（Non-GAAP 營業利益）＝255.7 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi2_core_operating_margin_no`（q1_business）｜Core operating margin（Non-GAAP）＝4.43 %｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（255.7÷5,773.0）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi3_gaap_net_sales_cogs_sg_a`（q1_business）｜GAAP 營業利益（net sales−COGS−SG&A−無形資產攤銷，自損益表推算）＝197.0 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（損益表推算；公司未單列營業利益）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝3.41 %｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（197.0÷5,773.0，推算）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi6_eps`（q1_business）｜調整後 EPS＝3.71 USD｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi7_2026_net_sales`（q1_business）｜2026 全年財測：Net sales＝23,350–23,750 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi8_2026_core_operating_earn`（q1_business）｜2026 全年財測：Core operating earnings＝1,080–1,200 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi10_adjusted_ebitda`（q1_business）｜Adjusted EBITDA 全年財測＝1,700–1,820 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi11_content_per_vehicle`（q1_business）｜Content per vehicle（北美／歐非）＝682／505 USD｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-30 date｜期間與口徑：2026-10-30／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-30）
- `f_peer_lea_gross_margin_pct`（q2_moat）｜LEA 毛利率＝6.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_operating_margin_pct`（q2_moat）｜LEA 營業利益率＝3.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_fcf_margin_pct`（q2_moat）｜LEA FCF 利潤率＝3.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_adnt_gross_margin_pct`（q2_moat）｜ADNT 毛利率＝6.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADNT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_adnt_operating_margin_pct`（q2_moat）｜ADNT 營業利益率＝2.83 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADNT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_adnt_fcf_margin_pct`（q2_moat）｜ADNT FCF 利潤率＝1.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADNT.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_operating_margin_pct`（q2_moat）｜APTV 營業利益率＝9.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_operating_margin_pct`（q2_moat）｜MGA 營業利益率＝5.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝14.99 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝16.73 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝19.52 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝23661.24 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝23891.57 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.3 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（16.68 → 16.73）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.62 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（19.4 → 19.52）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_kpi5_fcf_329_3_170_9`（q4_capital）｜自由現金流（FCF = 營運現金流 329.3 − 資本支出 170.9）＝158.4 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_kpi9_2026_fcf`（q4_capital）｜2026 全年財測：FCF／營運現金流／重組成本＝FCF 565–665；OCF 1,225–1,325；重組 ≈200 USD M｜期間與口徑：Q3 2026（季末 2026-10-03，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-10-03，公告於 2026-10-30））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝2612.2 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 3507.7、現金 895.5（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.488 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝48.19 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝8578.37 USD m｜期間與口徑：2026-11-03／市值 5966.17 ＋ 淨負債 2612.2｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝10.78 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝7.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝123.8 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝8.26 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 14.99，分子＝快照價 123.8｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝7.6 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.25 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝25.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝25.6 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.36 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝54.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝54.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.47 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 14.92 → 14.99（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-3.55 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝60.51｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 123.36 / W52 124.57 / W104 108.65 / W250 116.29 / W250 13週斜率 -0.59%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝124.57 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝108.65 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝116.29 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.59 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Lear 10-K風險因子：新進入者與中國本土供應商（財務報酬要求較低）正在挑戰傳統供應商份額
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Lear 10-K風險因子：中國本土車廠擴張份額，使傳統車廠（Lear大客戶）營收與份額下滑
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年GM占Lear淨銷售22%，Ford 12%，Mercedes-Benz與Volkswagen各10%，Stellantis 9%（前五大合計約63%）
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K風險因子載明主要客戶產量下滑或財務困境可能損害Lear財務表現；傳統車廠（Lear最大客戶）受中國車廠擴張侵蝕市占
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：S&P Global Mobility 5月更新將北美2027輕型車產量預測下調33.9萬輛，理由是油價情境持續影響至2027年（需求、生產成本、供應鏈承壓）
  - 來源：autoinformed.com - May 2026 Light Vehicle Production Forecast is Down Again (S&P Global Mobility)（as_of 2026-05-15）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：GlobalData 8月下調2027全球輕型車產量預測30萬輛，主因中國
  - 來源：just-auto - China weighs down on global light vehicle production forecast（as_of 2026-08-15）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Lear 10-K FY2025 discloses that US tariffs apply to countries (China, Mexico, Canada) and materials (steel, aluminum, auto parts) it buys or produces, and could raise costs or hurt customers' production; export controls and sanctions also noted.
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Lear 年報稱美國現行關稅適用於其營運或採購所在國（含中國、墨西哥）及鋼鋁等材料，可能推高營運成本或迫使更換供應商
  - 來源：SEC Form ARS FY2025 (Lear)（as_of 2026-02-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：PolicyRisk 摘要稱 2026 年 USMCA 檢討可能衝擊 Lear 高度集中於墨西哥的製造布局
  - 來源：PolicyRisk company page LEA（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Lear 68% 製造設施位於低成本國家
  - 來源：MarketScreener（as_of 2026-01-01）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：S&P Global Mobility 2026年6月更新：全球輕型車銷售 2026 年 89.4M、2027 年 91.6M（2025 年 91.9M），因中國需求疲弱與伊朗戰爭下修
  - 來源：S&P Global Mobility rapid-impact analysis（經搜尋摘要轉述）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：產業正經歷電動化與數位化的重大技術變革，新進者與中國本土供應商（財務報酬要求較低）挑戰既有供應商市佔；若無法差異化或維持低成本，可能失去市佔或被迫降價。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Lear 2009 gross margin 3.7% (gross profit $360M) vs 5.5% ($748M) in 2008; Q1 2009 gross margin was -3.5% (gross loss $76M); 9M2009 sales fell 36.2% YoY to $7.0B.
  - 來源：Lear Corp Form 10-K FY2009 / 10-Q FY2009 (SEC)（as_of 2010-03-01）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":278.2,"bear_5y_price":91.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":58.5,"ev5y_pct":46.2,"irr_base_pct":9.6,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":14.99,"pe":8.26,"basis":"FY1（2026 年）調整後 EPS 共識 14.99、現價 123.8 美元；終端倍數同樣套在當年度調整後 EPS 上"},"eps":{"bull":[17.0,19.8,22.2,24.3,26.5],"base":[16.2,18.0,19.4,20.6,21.8],"bear":[13.5,11.0,11.8,12.5,13.0]},"pe":{"bull":10.5,"base":9.0,"bear":7.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.488,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEA_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：CFO 說全年營收中點上調至約 238 億美元，前次為 236 億。（原話："Revenue is now expected to be approximately $23.8 billion"）
- 2026-07-31｜CFO｜guidance：CFO 說全年核心營業利益中點約 11.4 億美元，前次為 11.15 億。（原話："$1.14 billion or 2% higher than our prior guidance"）
- 2026-07-31｜CFO｜guidance：CFO 說全年營業現金流中點約 13 億美元。（原話："expected to be approximately $1.3 billion"）
- 2026-07-31｜CFO｜guidance：CFO 給下半年營業利益中點 5.29 億美元，營業利益率 4.5%。（原話："second half operating income outlook is $529 million"）
- 2026-07-31｜CFO｜guidance：CFO 說全年展望假設關稅政策不變、無產業性大幅中斷。（原話："current tariff policies or significant industry-wide"）
- 2026-07-31｜CFO｜guidance：CFO 說全年全球產量假設中點為年減不到 2%，前次為減 1%，主因中國下修。（原話："than 2% on a Lear sales weighted basis compared to 2025"）
- 2026-07-31｜CFO｜guidance：CFO 給第三季營收區間 58～59 億美元。（原話："revenues to be $5.8 billion to $5.9 billion in the quarter"）
- 2026-07-31｜CFO｜margin：CFO 給第三季座椅利益率區間。（原話："We expect Seating margins in the low to mid-6s"）
- 2026-07-31｜CFO｜margin：CFO 給第三季 E-Systems 利益率區間。（原話："Systems in the low 4s."）
- 2026-07-31｜CFO｜margin：CFO 說第三季利益率低於第四季，原因含歐洲夏季停工與銅價回收時間差。（原話："Q3 margins will be lower than the"）
- 2026-07-31｜CFO｜margin：CFO 說上半年 E-Systems 受惠於銅庫存重估，第三季出現回收落差。（原話："where we benefited in the first half of the year"）
- 2026-07-31｜CFO｜commitment：CFO 說會在九月投資人會議給第三季中期更新。（原話："provide a mid-quarter update at an investor conference"）
- 2026-07-31｜CFO｜margin：CFO 說座椅第二季營業利益率 6.7%，與去年持平。（原話："with adjusted operating margins of 6.7%"）
- 2026-07-31｜CFO｜margin：CFO 說 E-Systems 第二季調整後利益 9100 萬美元、利益率 5.8%（去年 4.9%）。（原話："Adjusted earnings were $91 million or 5.8%"）
- 2026-07-31｜CEO｜margin：CEO 說 E-Systems 第二季淨績效貢獻 155 bps。（原話："driven by a strong 155 basis points of net performance"）
- 2026-07-31｜CEO｜margin：CEO 說 E-Systems 上半年淨績效約 100 bps，已超過全年目標。（原話："having generated approximately 100 basis points"）
- 2026-07-31｜CFO｜margin：CFO 拆解上半年到下半年：銷貨減少約 6.64 億美元、下行轉換率 25%（1.67 億），並自承偏重。（原話："still a bit heavy at 25% or $167 million"）
- 2026-07-31｜CFO｜margin：CFO 說關稅退款使下半年營收較上半年多 1.9 億美元但無盈餘對應。（原話："you have $190 million higher revenue in the second half"）
- 2026-07-31｜CFO｜margin：CFO 說下半年展望含較上半年 55 bps 的淨營運績效改善。（原話："outlook with 55 basis points of improvement sequentially"）
- 2026-07-31｜CFO｜commitment：CFO 說今年座椅與 E-Systems 淨績效預計達成或超過 40 與 80 bps。（原話："meet or exceed the 40 and 80 basis points"）
- 2026-07-31｜CFO｜guidance：CFO 說明年座椅與 E-Systems 預期再各貢獻 40 與 80 bps 淨績效。（原話："we expect another 40 and 80 basis points in C and E-Systems"）
- 2026-07-31｜CFO｜margin：CFO 表示 E-Systems 利益率明年不太可能明顯改善，2027～2029 逐步改善。（原話："it's not likely in '27, but as you progress through that '27"）
- 2026-07-31｜CFO｜margin：CFO 對 E-Systems 現階段利益率表達不滿意。（原話："We're not happy with where margins are right now"）
- 2026-07-31｜CFO｜commitment：CFO 說公司計畫恢復提供三年 backlog，時點為第四季財報與 2027 初步財測。（原話："historical practice of providing a 3-year backlog"）
- 2026-07-31｜CFO｜customer：CFO 說客戶選商節奏已趨穩定，近似電動車急轉彎之前。（原話："has stabilized. It more closely resembles what we"）
- 2026-07-31｜CFO｜guidance：CFO 說 2029 年 backlog 很穩，可能優於 2027、2028。（原話："a very robust 2029 backlog, very likely better than"）
- 2026-07-31｜CFO｜guidance：CFO 重申 2026～2028 backlog 較年初合約改善 4 億美元，偏重 2028。（原話："our 2026 to '28 backlog had improved by $400 million"）
- 2026-07-31｜CFO｜guidance：CFO 說非核心電子產品退場今年少 9000 萬美元營收，明年少 2.35 億。（原話："$90 million of revenue that goes away this year"）
- 2026-07-31｜CFO｜guidance：CFO 在被問及 2027 時表示預期成長有限，即使 backlog 逾 7 億美元。（原話："we do expect limited growth in ' 27 despite the more than"）
- 2026-07-31｜CFO｜risk：CFO 預期 JLR、Ford Explorer、Jeep Grand Wagoneer 三個平台明年回落。（原話："we expect those 3 platforms to pull back a bit"）
- 2026-07-31｜CFO｜risk：CFO 引述通用說明年全尺寸卡車與 SUV 量大致持平。（原話："full-size truck and SUV volumes being sort of flat next year"）
- 2026-07-31｜CFO｜guidance：CFO 說 2028～2030 有機會回到高於市場 3～4 個百分點的成長。（原話："return to our historical growth above market profile"）
- 2026-07-31｜CFO｜guidance：CFO 說資本支出預期不會有明顯變化，今年約 2.8% 營收。（原話："We don't see a meaningful change in our CapEx footprint."）
- 2026-07-31｜CFO｜capital_allocation：CFO 說併購製造整合商使設備成本下降 20% 以上。（原話："We've reduced the cost of our equipment by 20% or"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說全年買回目標上調至至少 3.5 億美元。（原話："year repurchase target to at least $350 million"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說現有買回授權剩餘約 6 億美元，可買到 2026 年底。（原話："approximately $600 million remaining"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說自 2011 年起以買回與股利返還超過 85% 自由現金流。（原話："returned over 85% of free cash flow to"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說可用流動性 30 億美元。（原話："we have $3 billion of available liquidity"）
- 2026-07-31｜CFO｜risk：CFO 說上半年中國內需銷售下滑 20%，下半年假設弱勢持續。（原話："domestic sales in China, they're down 20%"）
- 2026-07-31｜CFO｜guidance：CFO 說若非中國疲弱，本次財測可能上調更多。（原話："have raised guidance a little bit more today"）
- 2026-07-31｜CFO｜risk：CFO 說財測區間低端是為防範伊朗衝突等引發的需求疲弱。（原話："the low end of the range is in place to protect against"）
- 2026-07-31｜CFO｜risk：CFO 提到伊朗衝突為北美與歐洲購車需求下行風險。（原話："stemming from the continued conflict in Iran"）
- 2026-07-31｜CFO｜guidance：CFO 說 301 與 122 條款關稅影響較先前假設少約 4000 萬美元，僅影響營收。（原話："301 tariffs and 122 tariffs were -- are about $40 million"）
- 2026-07-31｜CFO｜competition：CFO 說財測內已把傳統客戶讓給中國車廠的份額假設由約 1.5% 升至 3%。（原話："went from roughly 1.5% this year to 3%"）
- 2026-07-31｜CFO｜customer：CFO 說中國車廠占其新訂單近 20%，但占營收不到 10%。（原話："less than 10% of our revenue"）
- 2026-07-31｜CFO｜customer：CFO 說公司營收與中國車廠的比例將於 2027 達 50%（此句口徑為「revenue」，同場稍後問答改稱「China revenues」）。（原話："We're well on track to get to 50% of our revenue"）
- 2026-07-31｜CFO｜customer：CFO 說目前中國營收中 44% 來自中國車廠，明年 50% 以上。（原話："we're at 44% of our China revenues"）
- 2026-07-31｜CFO｜commitment：CFO 說對中國車廠成長以保護報酬為優先。（原話："but we're protecting returns"）
- 2026-07-31｜CFO｜competition：CFO 說出口導向的中國車廠專案占比偏低，短期是風險、長期可能是機會。（原話："we're a bit under-indexed on the export front"）
- 2026-07-31｜CEO｜customer：CEO 說今年累計新訂單約 29 億美元（座椅逾 23 億、E-Systems 逾 5 億）。（原話："approximately $2.9 billion of business awards year-to-date"）
- 2026-07-31｜CFO｜customer：CFO 說 Audi 訂單約為去年底最大 conquest 訂單的 75%，投產於 2028 年底。（原話："it's about 75% as large as our largest conquest award"）
- 2026-07-31｜CFO｜customer：CFO 說 Audi 專案 2028 年底起量產，2029～2030 爬坡。（原話："launches towards tail end of '28 and programs ramp up"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說 Leapmotor 南美訂單不需大額投資。（原話："No, there's not major investment required."）
- 2026-07-31｜CEO｜commitment：CEO 說下半年預期還有更多好消息，待鎖定合約。（原話："more good news in the second half"）
- 2026-07-31｜CEO｜commitment：CEO 說今年 IDEA by Lear 節省目標 7500 萬美元。（原話："deliver $75 million in IDEA savings this year"）
- 2026-07-31｜CEO｜commitment：CEO 說重組節省上半年已達 5000 萬美元，全年目標 8000 萬。（原話："we have generated $50 million in savings"）
- 2026-07-31｜CEO｜product：CEO 稱自動化與數位工具使公司領先同業數年。（原話："positioning Lear years ahead of our competition"）

### 問答異常語氣（迴避／改口／保留）
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Dan Levy 問 E-Systems 8% 利益率路徑（先前說與量相關）是否還成立、淨績效能否壓過量價組合。｜答法：CFO 回答未提 8%，改談 2027～2029 backlog、40/80 bps 淨績效，並說 E-Systems 利益率明年不太可能明顯改善。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Joe Spak 問先前財測上下各 4 億美元緩衝，如今低端上調後剩多少緩衝。｜答法：CFO 說明高低端情境（中國政策、北美卡車、伊朗衝突），未給剩餘緩衝金額。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Itay Michaeli 問下半年財測中中國內需與產量假設的量化程度。｜答法：CFO 說沒有具體數字可提供，改給份額轉移假設與新訂單比重。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Colin Langan 問第三季至第四季利益率走勢。｜答法：CFO 先說不提供按季精確財測，隨後仍給第三季營收與兩部門利益率區間，並說商業談判是最大變數。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Emmanuel Rosner 問 2027 營收成長是否被下修，以及 Audi 訂單規模。｜答法：CFO 確認 2027 成長有限（與前文偏重 backlog 的說法相比語氣轉保留）；Audi 規模拒給確切數字，只說約最大 conquest 訂單的 75%。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 3 | 3 |
| cyclical_inventory_price_position | found | 1 | 3 |
| cyclical_prior_downcycle_behavior | found | 2 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B 觀望偏進場（衛星，等回測）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Seating margin 結構性回升至 7.0%+（vs Q2 25 6.4%）","columns":{"2Y":"FY27 Seating margin ≥ 7.0%","5Y":"FY29 Seating margin ≥ 7.5%","10Y":"FY35 維持 7%+","具體門檻":"FY26 全年 ≥ 6.8%；FY27 ≥ 7.0%","來源":"Q1 2026 8-K + 法說會","漂移觸發":"連 2 季 &lt; 6.5% → 削弱"}},{"id":"H2","text":"E-Systems 段占比擴張至 28%+ + 持續 .0B+ 新 awards/年","columns":{"2Y":"FY27 E-Sys 占比 ≥ 27%","5Y":"FY29 ≥ 30%","10Y":"FY35 ≥ 35%","具體門檻":"FY26 E-Sys Rev ≥ .2B；FY26 全年 awards ≥ .0B","來源":"2025 awards 公告 .4B","漂移觸發":"FY27 全年 awards &lt; .8B → 削弱"}},{"id":"H3","text":"市場估值倍數均值回歸至 11-12x（vs 5Y 均 25.95x 折讓 55%）","columns":{"2Y":"Fwd PE 24 月內 ≥ 11x","5Y":"5Y 內 PE 至少觸及 14x","10Y":"10Y 區間 8-22x","具體門檻":"Fwd PE 24 月內 ≥ 11x","來源":"Macrotrends 5Y PE 數據","漂移觸發":"連 2 季維持 &lt; 9x → 結構性 de-rating"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"GM 罷工或 production miss（GM 占 LEA 22%）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"UAW 2027 談判進度、GM Q-on-Q production","警戒閾值":"單季 Seating margin &lt; 5.5% 或 GM production -10% 連 2 季"}},{"id":"R2","text":"Seating 段 commoditization 持續（BWA / Adient / 中國 Yanfeng 壓價）","columns":{"對應假設":"H1 + H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Seating margin 季度走勢；新 awards 流向","警戒閾值":"Seating margin 連 4 季 &lt; 6.0% → 大動作"}},{"id":"R3","text":"OEM in-source + 中國新勢力擠壓 → 全球市佔結構性流失","columns":{"對應假設":"H1 + H2 + H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"LEA organic growth vs LVP；新 awards 量","警戒閾值":"連 8 季 organic growth underperform LVP &gt; 200bps"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":139.8,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LEA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Lear Corporation"},"oneliner":"全球座椅雙強之一，執行力與買回撐起每股盈餘，但車市停在高原、中國車廠吃掉傳統客戶份額；前瞻 8 倍便宜但不是錯價，等循環低點再進。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球車廠座椅與線束的組裝錢：營收跟著客戶車款產量走，毛利率只有 6～7%，錢卡在車廠採購端；座椅約占營收四分之三、E-Systems 約四分之一。","reasoning":"2026 Q3 營收 57.73 億美元、年增 2%，同期 Lear 加權產量年減 2%，成長高於市場約 4 個百分點；核心營業利益 2.557 億美元、核心營益率 4.43%，GAAP 營益率 3.41%，兩者差約 1 個百分點，主要是重組費。分部：座椅營收約 43 億美元、調整後利益率 6.3%；E-Systems 營收 14.47 億美元、調整後利益率 4.8%。2026 全年財測營收 233.5～237.5 億美元、核心營業利益 10.8～12 億美元，中點營益率約 4.8%。收錢方式：得標後按車款產量出貨，每車內容價值北美 682 美元、歐非 505 美元；商品成本以指數與背對背合約轉嫁，2026 年商品毛衝擊逾 3 億美元、淨影響約 1,000 萬美元（2026-10-30 CFO）。單點依賴：GM 占 2025 年淨銷售 22%，前五大車廠合計約 63%（10-K）；Orion 新廠專供 GM 三款主力車，是集中度風險，也是關係深度的證據（Q2 新聞稿稱獲 GM 2025 年供應商獎項）。產業時鐘判在收縮段：全球輕型車銷量 2026 年 8,940 萬輛低於 2025 年 9,190 萬輛，Q3 北美產量年減 5%、中國年減 7%，屬輕度收縮而非崩落。","fact_refs":["f_kpi0_gaap_net_sales","f_kpi1_core_operating_earnings_","f_kpi2_core_operating_margin_no","f_kpi3_gaap_net_sales_cogs_sg_a","f_kpi4_gaap","f_kpi6_eps","f_kpi7_2026_net_sales","f_kpi8_2026_core_operating_earn","f_kpi10_adjusted_ebitda","f_kpi11_content_per_vehicle","f_earnings_recency"],"verdict_values":{"revenue_quality":"合約制、隨車款生命週期出貨，可見度中等；價格每年向車廠讓價，商品成本靠指數轉嫁。2026 營收含約 2 億美元一次性關稅退還，沒有對應盈餘（2026-10-30 CFO），2027 會變成基期逆風。","unit_econ_note":"量的變動以 15～25% 轉成營業利益，新案約 10%，退場業務約 20%（2026-10-30 CFO）；利潤率這麼薄，營收每少 10% 就吃掉三到五成核心營業利益。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"汽車產量驅動的需求量循環：毛利率 6.5%～7.3%、營益率 3.1%～4.0%（2022–2025 年度財報），獲利對產量高度敏感；不是商品價格驅動，資本支出約占營收 2.8%。"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉、非結構性：全球車產在 9,000 萬輛上下高原盤整，ITR 預期北美 2027 約 −2.1%、2028 約 +4.6%，維持在 1,500～1,560 萬輛窄區間；下行來自中國內需與油價。座椅產能可在車款換代時重新招標，供給可逆性高。來源：S&P Global Mobility 2026-05 與 2026-06、GlobalData 2026-08、ITR 2026-07。","bargaining":{"up":"鋼、泡棉化學品、銅等原料以指數與背對背合約轉嫁，上游議價影響有限","down":"車廠強勢：前五大客戶約 63%、每年降價，商業談判決定季度盈虧（2026-10-30 CFO 稱談判是第四季區間的主要變數）","geo":"68% 製造設施在低成本國家、墨西哥比重高，受美國關稅與 USMCA 檢討影響；目前多數關稅由客戶抵減分攤"},"profit_pool_dir":"利潤池往中國車廠與其在地供應鏈移動：公司財測已假設客戶今年讓給中國車廠約 3% 份額（原 1.5%）；Lear 用中國車廠訂單追趕（今年約 39 億美元新訂單中約 9 億），但中國車廠目前只占營收約 8.5%。","tam_table":{"expanded":false,"reason":"成熟市場，論點不靠 TAM 擴張；利潤池往中國車廠移動的分段營業利益池占比事實表未涵蓋，改用客戶讓出份額假設與中國車廠訂單占比追蹤"}}}},"q2_moat":{"verdict":"護城河 C 級、方向持平：座椅雙強的規模、就近組裝與垂直整合守住約 26% 全球份額，但沒有定價權，毛利率四年都在 6.5%～7.3%，價值大多被車廠拿走。","reasoning":"機制是成本與規模，不是定價權。可證方向：對最直接的對手 ADNT，TTM 營益率 3.67% 對 2.83%、FCF 利潤率 3.58% 對 1.95%，Lear 領先但幅度沒有擴大；Lear 營益率 2022–2025 年在 3.1%～4.0% 窄區間。份額方向是雙向的：Q3 成長高於市場 4 個百分點、2026 年整椅新案過半為新增或搶單、E-Systems 約七成；但中國連續數季成長低於市場，主要客戶持續讓份額給中國車廠。執行力評 7（連 4 季核心營業利益年增，兩部門淨績效都達標或超標），定價權評 5（能轉嫁商品與關稅成本，卻擴大不了毛利率），合併落在 C 級下緣。Orion 自動化廠預計把轉換成本降 10～15%，公司自稱難以複製，但屬成本優勢、明年才投產，暫不加分。投入資本未收錄，當期 ROIC 無法計算。","fact_refs":["f_peer_lea_gross_margin_pct","f_peer_lea_operating_margin_pct","f_peer_lea_fcf_margin_pct","f_peer_adnt_gross_margin_pct","f_peer_adnt_operating_margin_pct","f_peer_adnt_fcf_margin_pct","f_peer_aptv_operating_margin_pct","f_peer_mga_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模＋就近 JIT 組裝＋垂直整合（泡棉、面套、骨架、腰靠與熱舒適模組）＋車款生命週期內的轉換成本；自建自動化設備（收購 ASI 等）壓低轉換成本，屬成本優勢而非定價權。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大（Q3 成長高於市場 4 個百分點、兩部門利益率皆年增），定價權縮減（客戶讓份額給中國車廠、E-Systems 售價下調抵銷商業回收），合併判持平。營益率 2022–2025 年 3.1%～4.0% 窄區間，TTM 對 ADNT 領先約 0.8 個百分點、未擴大。最大客戶群份額下滑有來源，不判上升。","competitor_notes":[{"name":"ADNT","strategy_note":"座椅雙強中較弱的一方，三項利潤率都低於 Lear；收購美洲泡棉廠走垂直整合，與 Lear 屬逐案價格競爭，不構成生態威脅。"},{"name":"MGA","strategy_note":"產品線廣的多元零組件商，利潤率與現金流高於 Lear，座椅只是其中一塊；換代招標時是有資本實力的搶單者。"},{"name":"APTV","strategy_note":"線束與電子架構對手，對應 E-Systems；利潤率高一個量級，屬不同族群，不拿來當座椅估值或護城河的錨。"},{"name":"延鋒等中國本土供應商","strategy_note":"報酬要求較低、跟著中國車廠出海，是長期份額最大的威脅；Lear 的對策是搶中國車廠的高端與海外在地化案。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改以營業利益率與 FCF 利潤率差距代理","threats":[{"level":"🔴","text":"中國車廠以在地與自製供應鏈擴張全球份額，Lear 的傳統大客戶（前五大約 63%）持續失血；公司已把客戶今年讓給中國車廠的份額假設由 1.5% 調高到 3%。屬生態層級攻擊，Lear 用中國車廠訂單追趕，但這塊營收占比仍只有約 8.5%。","p":35,"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1"]},{"level":"🟡","text":"中國本土供應商報酬要求較低，在電動化與數位化變革期用價格搶傳統供應商份額；目前是逐案報價競爭，Lear 仍拿下 BYD 泰國與印尼、Leapmotor 南美等中國車廠海外案。","p":40,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"車廠自製座椅（如比亞迪旗下 FinDreams）縮小可外包市場；現階段集中在中國，未見擴散到 Lear 主要客戶。","p":20,"evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（周轉率事實表未涵蓋，依組裝業型態推定，待現金循環資料確認）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"每台車都要座椅與線束，使用者（駕駛）、決策者（車廠採購）、付款者（車廠）三個角色都成立，是『需要』不是『想要』；但基礎量在高原：全球車產 2025 年 9,190 萬輛、2026 年 8,940 萬輛，北美 2027 預測又被下修 33.9 萬輛，需求持久但不成長。"},{"item":"決策層級","level":"🟡","text":"替代發生在單一車款招標層級：車款生命週期內很少換供應商，但每次換代都重新報價。代理讀數：Q3 拿回一個現有車款的續約、同時拿到新車款；整椅新案過半是搶單，表示份額雙向可爭，對手也能在換代時搶走 Lear 的案子。"},{"item":"價值鏈分配","level":"🔴","text":"車廠拿走大部分價值：Lear 毛利率 6.9%、前五大客戶約 63%、每年降價；中國供應商以較低報酬要求報價，車廠自製可繞過外部供應商。長期需求存在，不等於 Lear 這一環能多賺。"},{"item":"社會容忍度","level":"🟡","text":"B2B 零件不受消費者漲價容忍度約束；但墨西哥等低成本國家的成本優勢依賴貿易協定，USMCA 檢討與美國關稅屬政策風險。目前多數關稅由客戶抵減，10-Q 明言無法保證客戶持續同意。"}],"roiic":"事實表未涵蓋（缺投入資本與折舊，無法算增量報酬）","reinvest_rate":"事實表未涵蓋；以自由現金流口徑，公司 2026 年約八成返還股東（2026-10-30 CFO），留存再投資約兩成","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；TTM 營業利益率 3.67%，周轉率與投入資本未收錄。內生成長上界以『留存約兩成、資本支出約占營收 2.8%、共識營收 FY1→FY2 只增約 1%』判為低個位數，不給點值。"}}}},"q3_growth":{"verdict":"跑道窄：車市停在高原、沒有第二條成長曲線，成長只能靠搶單與買回；共識 EPS 兩年年化約 14%，營收只貢獻約 1%，其餘靠利潤率與股數減少。","reasoning":"成長來源是量（新案與搶單，2026 年前三季淨新訂單約 39 億美元，座椅約 31 億、E-Systems 約 8 億）加上淨回購；價格為負（年度降價、E-Systems 售價下調）；併購只做小型補強。共識 EPS 由 FY2026 的 14.99 到 FY2027 的 16.73、FY2028 的 19.52，兩年年化約 14.1%；共識營收由 236.6 億到 238.9 億美元，只增 1.0%。缺口歸因：利潤率擴張（淨績效座椅 40bp、E-Systems 80bp，重組節省 2026 年上調到 9,500 萬美元）加淨回購（每年約 3.5 億美元，約占市值 5.9%），可以歸因，不靠重估。但管理層 Q2 自承 2027 成長有限，非核心電子退場 2027 年少 2.35 億美元營收，Audi 大案 2028 年底才量產，共識 2028 年 +16.7% 偏樂觀。管理層目標 2029 年座椅回到高於市場 3～4 個百分點、E-Systems 4～6 個百分點，三年核心 backlog 約 22.5 億美元。跑道判窄：座椅在車上已全面滲透、全球車產不成長；模組化座椅（47 個案）與 Orion 自動化是成本與內容的改善，還不是有來源的第二條曲線。衰退信號亮 2 個（EPS 成長遠高於營收、自身倍數在四年低檔），價值陷阱風險中度。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量（新案與搶單，管理層目標高於市場 3～4 個百分點）＋淨回購每年約 5～6%＋小幅利潤率改善；價格為負；併購可忽略","runway_years":"不適用：座椅已全面滲透，Lear 全球份額 26%，市場本身不成長","runway_post_y5":"🔴","endo_ceiling_basis":"投入資本與折舊事實表未涵蓋，增量報酬算不出來；留存約兩成自由現金流、資本支出約占營收 2.8%、共識營收年增約 1%，內生成長上界判為低個位數。共識 EPS 年增約 14% 明顯超出，缺口由利潤率與買回填補。","segments":[{"item":"座椅（2026 Q3）","value":"營收約 43 億美元、年增 2%（新業務貢獻 1.72 億美元），調整後利益率 6.3%，成長高於市場約 4 個百分點"},{"item":"E-Systems（2026 Q3）","value":"營收 14.47 億美元、年增 1%，調整後利益率 4.8%（去年 4.2%）；扣除非核心產品退場，成長高於市場 5 個百分點"},{"item":"非核心電子退場","value":"2026 年少約 9,000 萬美元營收、2027 年少約 2.35 億美元（2026-07-31 CFO），退場業務約以 20% 轉換率拖累利潤"},{"item":"中國車廠業務","value":"約占營收 8.5%（含未合併合資）；中國營收中來自中國車廠 44%，目標明年 50% 以上；2026 年座椅中國車廠新案預估年均營收逾 6 億美元"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"季度毛利率事實表未涵蓋；Q3 兩部門調整後利益率皆年增"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"整體成長高於市場 4 個百分點；中國是例外，列風險追蹤"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"不適用：價格每年向車廠讓價"},{"signal":"EPS 成長顯著高於營收成長（差逾 5 個百分點）","lit":true,"note":"共識 EPS 兩年年化約 14%，營收 FY1→FY2 約 1%"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2022–2025 年介於 1.09～1.21"},{"signal":"SBC／營收逾 5% 且上升","lit":false,"note":"SBC 事實表未涵蓋；股數因買回下降"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"車產在高原、未萎縮；車廠自製目前限於中國"},{"signal":"估值倍數近 3 年系統性下移","lit":true,"note":"滾動本益比在近四個年度端點 7.6 百分位；產業倍數事實表未涵蓋，以自身倍數代理"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"維持性資本支出拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收 2023–2025 年微降，但 Orion 新廠持續投資"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律好：自由現金流連四年高於淨利、約八成返還股東、負債便宜且到期長；弱點是新投資（Orion、自動化）的報酬還看不到。","reasoning":"現金轉換：自由現金流／淨利 2022–2025 年分別約 1.17、1.09、1.11、1.21（年度財報），品質佳。2026 財測自由現金流 5.65～6.65 億美元（Q2 時為 5.9～6.9 億，因重組費多 2,500 萬美元下修），營運現金流 12.25～13.25 億、重組約 2 億；Q3 自由現金流 1.584 億美元（營運現金流 3.293 億減資本支出 1.709 億），因模具與工程投資和營運資金時點，低於去年同期。現金去向：資本支出約占營收 2.8%（2026-07-31 CFO）；2026 年 3.5 億美元買回已在 Q3 完成；股利殖利率約 2.5%；併購只做小型補強，近 12 個月沒有併購類申報。自 2011 年累計買回 63 億美元、返還逾 85% 自由現金流；9 月董事會把買回授權提高到 15 億美元並延到 2029 年底，約占市值四分之一。負債：淨負債 26.1 億美元，約為 2026 調整後 EBITDA 財測中點的 1.5 倍；平均利率低於 4%、加權到期約 11 年、可用流動性 29 億美元（2026-10-30 CFO）。三項檢驗：併購規模太小不適用；買回的 GAAP 盈餘殖利率約 9.3%（滾動本益比 10.8 倍），十年期公債殖利率事實表未涵蓋，只要低於 7.3% 就過；SBC 金額未收錄，但 Q3 調整後 EPS 年增 33%、核心營業利益只增 6%，股數淨減少明確。","fact_refs":["f_kpi5_fcf_329_3_170_9","f_kpi9_2026_fcf","f_kpi10_adjusted_ebitda","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m","f_pe_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年只有小型補強收購（ASI 等自動化設備商），金額與已實現報酬事實表未涵蓋；管理層稱設備成本因此降 20% 以上（2026-07-31 CFO），屬間接效益、未證"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"買入時 GAAP 盈餘殖利率約 9.3%（滾動本益比 10.8 倍），調整後約 12.1%（前瞻 8.26 倍）；十年期公債殖利率事實表未涵蓋，低於 7.3% 即過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 金額事實表未涵蓋；2026 年買回 3.5 億美元約占市值 5.9%，Q3 調整後 EPS 年增 33% 遠高於核心營業利益 6%，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，資本返還以買回與股利為主，近 12 個月 8-K 沒有併購項目"}}}},"q5_valuation":{"verdict":"現價只要求每股盈餘守住 15 美元：前瞻本益比 8.3 倍，等於市場假設獲利已近高點、之後會被景氣吃回；我同意景氣風險，但不同意每股盈餘會掉，因為買回每年減股約 6%。便宜，但還不到錯價。","reasoning":"現價 123.8 美元，前瞻本益比 8.26 倍（FY1 EPS 14.99），FY2 約 7.4 倍；滾動本益比 10.78 倍在近四個年度端點 7.6 百分位，P/S 0.25 倍在 25.6 百分位，但 EV/S 0.36 倍在 54.3 百分位：加上 26 億美元淨負債後的企業價值並不便宜，便宜主要出在股權倍數。反推：EPS 持平在 15 美元、倍數不動，股利 2.5% 加買回約 6%，每年約 8%；要虧錢，得 EPS 回落且倍數再被壓。PEG 以共識 FY1→FY3 年化 14.1% 算約 0.59，用本次基準路徑（兩年年化約 9.6%）算約 0.86。賣方目標均價 135.6～150.5 美元（2026-08 前後，各家家數不同），全距 130～179 美元，最高最低比約 1.4，都在現價之上，支持便宜但不支持急進。同業前瞻倍數事實表未涵蓋，不拿 APTV 等不同族群當錨。循環位置判中段：需求拐點未見（2027 預測仍在下修）偏空，倍數近自身下緣偏多，客戶庫存事實表未涵蓋，終端產量在高原，賣方目標價高於現價偏多；訊號互相矛盾、也沒有投降式下跌，循環進場條件未觸發。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ev_m","f_net_debt_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 調整後 EPS）為主，EV/S 對照；循環股優先看的股價淨值比，因淨值事實表未涵蓋而無法使用","tier":"汽車零組件—座椅與線束","peers":{"expanded":false,"reason":"同業前瞻本益比與目標價事實表未涵蓋（只收同業利潤率）；APTV 屬電子架構不同族群，不跨族群當錨"},"fwd_pe":8.26,"peg":0.59,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻 8.26 倍、PEG 約 0.59、滾動本益比在自身四個年度端點最低區（7.6 百分位，不是五年分位；五年高低點事實表未涵蓋，五年分位留空）→ 便宜。EV/S 在 54.3 百分位，提醒負債讓企業價值不便宜，所以只到便宜、不到極便宜。上檔：1 年以基準 FY2027 EPS 16.2×8.5 倍約 137.7 美元（+11.2%）；3 年以 FY2029 EPS 19.4×9 倍約 174.6 美元（+41.0%）。","upside_short_pct":11.2,"upside_mid_pct":41.0,"denominator_disputed":false,"denominator_note":"調整後 EPS 排除重組費，2026 年重組約 2 億美元且年年發生，嚴格說是經常性成本，Q3 GAAP 與核心營益率差約 1 個百分點；改用 GAAP 滾動本益比 10.8 倍，仍在自身四個年度端點最低區，便宜結論不靠分母口徑，但每股盈餘的品質要打折。"}}},"q6_how_wrong":{"verdict":"最可能看錯在景氣：基準路徑把每股盈餘成長押在淨績效與買回，但只要 Lear 加權產量年減一成，15～25% 的下行轉換率就會吃掉三到五成核心營業利益，股價可能腰斬。","reasoning":"下行路徑：2009 年前三季營收年減 36%、Q1 毛利轉負（2009 年報）；事實表收錄的汽車售後通路股 GPC 在 2007–09 與 2020 年各跌約 51%、53%（不是直接同業，只作類比）；本次空頭路徑谷底 EPS 11.0、給 6 倍約 66 美元，較現價約 −47%；淨負債約占 EV 三成，會放大股權回撤。最大回撤範圍取 −35%～−55%。目前動能：26 週報酬 −3.6%、RSI 60.5，不過熱；週收 123.36 美元略低於 52 週均線 124.57，高於 104 週 108.65 與 250 週 116.29，250 週均線 13 週斜率 −0.59%，長線趨勢走平。反方向看錯：若 2027 年 2 月財測核心營業利益年增、買回續行，股價可能不回檔就重估到 9～10 倍（約 135～150 美元），等待的代價是錯過一到兩成。另一個看錯點是調整後 EPS 高估股東盈餘：重組費若常態化，GAAP 口徑的成長會比共識慢。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_net_debt_m","f_ev_m","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"便宜有理由：營收停滯、每股盈餘成長靠利潤率與買回；但現金流品質好，不是陷阱型衰退"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":14.99,"pe":8.26,"basis":"FY1（2026 年）調整後 EPS 共識 14.99、現價 123.8 美元；終端倍數同樣套在當年度調整後 EPS 上"},"eps":{"bull":[17.0,19.8,22.2,24.3,26.5],"base":[16.2,18.0,19.4,20.6,21.8],"bear":[13.5,11.0,11.8,12.5,13.0]},"pe":{"bull":10.5,"base":9.0,"bear":7.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.49,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":4},"max_dd":{"lo":-55,"hi":-35,"basis":"依據四點：一、2009 年前三季營收年減 36%、Q1 毛利為負（年度財報）；二、事實表收錄的汽車售後通路股 GPC 在 2007–09 與 2020 年各跌約 51%、53%（非直接同業，僅作類比）；三、本次空頭路徑谷底 EPS 11.0×6 倍約 66 美元，較現價約 −47%；四、淨負債 26 億美元約占 EV 三成，放大股權回撤。溫和減產（年減 5～10%）落在 −35% 上緣，深度衰退落在 −55% 下緣。","trigger_time":null},"basis":{"bull":"共識兌現並超出：2027 淨績效超標、Orion 模式複製到 Ford Super Duty 等新廠、中國車廠與日系訂單放量，核心營益率升向 6%，每年減股約 5%；終端 10.5 倍（同業前瞻倍數事實表未涵蓋，以自身年度倍數區間上緣為錨）","base":"產量持平，淨績效大多被價格年降與成本吃掉，核心營益率每年只升約 10bp、營收年增約 2%、每年減股約 4～5%；2028 年 EPS 18.0 低於共識 19.52（Audi 案 2028 年底才量產、管理層自承 2027 成長有限）；EPS 路徑已含股數減少，淨回購殖利率填 0 避免重複計算；終端 9 倍略高於現值 8.3 倍","bear":"2027–28 出現產量年減近一成的衰退，下行轉換率 15～25%，核心營益率回到 3% 多；中國車廠持續吃掉傳統客戶份額，復甦後 EPS 回不到 2026 年水準；買回放緩；終端 7 倍（成長熄火）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2009 年前三季營收年減 36%、Q1 毛利為負；S&P 把北美 2027 產量下修 33.9 萬輛、GlobalData 下修全球 2027 產量 30 萬輛，全球銷量 2026 年 8,940 萬輛低於 2025 年；中國內需與排程持續轉弱（2026-10-30 CFO）。","assumption":"產量維持高原，淨績效每年抵銷價格年降與部分量的逆風。","consequence":"五年後虧五成最可能的故事：2027–28 一次產量年減一成的衰退，下行轉換率 15～25% 讓核心營業利益掉三到五成，EPS 回到 10～11 美元、倍數壓到 6 倍，股價約 60～70 美元；中國車廠同時趁機吃掉傳統客戶份額，復甦後 EPS 回不到 2026 年。","ruling":"採納：空頭機率給 30%、最大回撤下緣 −55%，與唯一致命點是同一件事。但不據此迴避：平均到期 11 年、利率低於 4%、流動性 29 億美元，2009 年式財務危機的機率低，衰退是進場時點而不是出場理由。","watch":"每季公司的 Lear 加權產量假設、S&P Global Mobility 月度預測；年減逾 10% 即啟動唯一致命點處置。","evidence_refs":["cyclical_prior_downcycle_behavior#0","supply_demand_durability#0","supply_demand_durability#2","end_markets#2"]},{"view":"論點成功但股東經濟變差","evidence":"Lear 對中國車廠的新訂單快速成長（2026 年約 39 億美元中約 9 億），但中國車廠與本土供應商的報酬要求較低；E-Systems Q3 商業回收被售價下調抵銷；2026 年重組費約 2 億美元並再上調 2,500 萬，年年發生。","assumption":"新案都以超過資金成本的條件承接（2026-10-30 CFO 稱每案都經審查），調整後 EPS 代表股東盈餘。","consequence":"營收如願回到高於市場成長，但新客戶利潤率較低、重組費常態化，核心營益率停在 5% 以下，GAAP 與核心差距維持約 1 個百分點，每股成長只剩買回，股東實得報酬落到個位數。","ruling":"部分採納：基準路徑每年只給約 10bp 利潤率改善，2028 年 EPS 低於共識約 8%，並以 GAAP 與核心營益率差距作監測。","watch":"2027 年重組費是否仍 ≥2 億美元；GAAP 與核心營益率差距是否連 4 季 ≥1 個百分點；中國車廠營收占比上升時座椅利益率的方向。","evidence_refs":["competitive_share_entrants#1"]},{"view":"價格已反映太多","evidence":"共識 FY2028 EPS 19.52，比 FY2027 多 16.7%，但管理層 Q2 自承 2027 成長有限、Audi 大案 2028 年底才量產；EV/S 0.36 倍在自身四個年度端點 54.3 百分位，含債後並不便宜。","assumption":"8.3 倍前瞻本益比已充分折價景氣風險。","consequence":"若共識 2027–28 再下修一成，實際前瞻倍數約 9 倍以上，不再處於低檔；景氣下行時，薄利率公司的倍數常在盈餘下修前就先被壓。","ruling":"部分反駁：即使 EPS 下修一成、或改用 GAAP 口徑，倍數仍在自身區間低檔，價格沒有反映過多樂觀；但承認企業價值口徑不便宜，估值結論維持便宜而非極便宜，也不把低倍數當唯一進場理由。","watch":"2027 年 2 月財測與共識 FY2027 EPS 16.73 的落差；共識三個月修正方向。","evidence_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 139.8 → 本次 123.8（-11.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=139.8","side_b":"本次 price_at_dd=123.8","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 139.8 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 139.8 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 139.8 美元：Bull 價 278.25、Bear 價 91，五年期望值 +29.5%，基準年化 7.0%，不對稱比 1.89","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.89。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 139.8 美元：五年期望值 +29.5%，基準年化 7.0%，不對稱比 1.89","side_b":"本次情境、股價 123.8 美元：五年期望值 +46.2%，基準年化 9.6%，不對稱比 3.14","ruling":"再換股價、情境不動：起點價下跌 11.4%，五年期望值多 16.7 個百分點，基準年化多 2.6 個百分點，不對稱比由 1.89 升到 3.14。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾兌現（一致）","cause":null,"prior_field":null,"side_a":"2026-07-31 Q2 法說（CFO）：今年座椅、E-Systems 淨績效達成或超過 40bp、80bp；IDEA 節省 7,500 萬美元；重組節省 8,000 萬美元；全年買回至少 3.5 億美元","side_b":"2026-10-30 Q3 法說（CEO、CFO）：E-Systems 前三季淨績效 105bp，座椅 30bp、要靠第四季加速到 40bp；IDEA 已達 5,500 萬；重組節省上調到 9,500 萬；3.5 億美元買回已提前完成","ruling":"一致：承諾大致兌現，座椅淨績效是唯一要靠第四季補的項目","evidence_level":"高：兩場法說原文","settle_metric":"2027 年 2 月公布的 2026 座椅全年淨績效是否 ≥40bp","if_then":["若座椅 2026 全年淨績效 <40bp → 假設一降一級，2027 核心營益率門檻列為高風險"],"evidence_refs":[]},{"axis":"營收財測下修但營業利益財測不變","cause":null,"prior_field":null,"side_a":"2026-07-31 CFO：全年營收中點上調到約 238 億美元、核心營業利益中點 11.4 億","side_b":"2026-10-30 CFO：營收中點下修約 2.25 億美元，主要是中國排程與匯率；營業利益區間 10.8～12 億不變，靠重組節省、淨績效與『預期中的商業談判落地』抵銷，第四季區間比平常寬","ruling":"可調和（程度差異）但未證：用成本與談判補量的缺口，談判部分屬管理層歸因，不採信也不否定，列入監測；若 2026 實際核心營業利益低於 11.4 億中點且公司歸因談判未落地，視為歸因證偽","evidence_level":"中：只有財測與法說說法，尚無實際值","settle_metric":"2026 全年核心營業利益 vs 11.4 億美元中點（2027 年 2 月）","if_then":["若 2026 核心營業利益低於 10.8 億美元下緣 → 停止任何建立、下修基準路徑","若落在中點以上且 2027 財測不低於 2026 實際值 → 計入重啟條件"],"evidence_refs":[]},{"axis":"市場定價方向 vs 共識獲利方向","cause":null,"prior_field":null,"side_a":"市場：前瞻本益比 8.3 倍、26 週跌 3.6%、週收略低於 52 週均線，定價為獲利已近高點、之後回落","side_b":"共識與管理層：FY2027 EPS 16.73（+11.6%）、FY2028 19.52（+16.7%）；管理層稱 2029 年回到高於市場 3～4 個百分點成長、三年核心 backlog 約 22.5 億美元","ruling":"⚖ 不可調和（方向相反）。選邊：方向站共識，每年約 6% 減股與兩年淨績效兌現紀錄讓每股盈餘大概率續增；幅度站市場，Audi 案 2028 年底才量產、管理層自承 2027 成長有限，本次基準 FY2028 EPS 取 18.0，低於共識約 8%。硬數據：2027 年 2 月財測的核心營業利益中點。現在就買的最強論證：8 倍本益比、15 億美元買回授權約占市值四分之一、殖利率 2.5%，就算 EPS 持平，股東每年也拿到約 8%。仍不買，是因為景氣位置在中段、跑道窄，三到五成的下檔要在更低價位才划算。","evidence_level":"高：財報、法說與共識快照","settle_metric":"2027 財測核心營業利益中點 vs 2026 實際值","if_then":["若 2027 財測中點 ≥2026 實際值且股價 ≤約 105 美元（前瞻 7 倍）→ 重跑研究，通過後以小倉位分三批建立","若 2027 財測中點低於 2026 實際值 → 基準路徑下修一成，維持觀望不碰","反向：若股價先漲回 140 美元以上而財測未出 → 不追"],"evidence_refs":[]},{"axis":"本次比賣方悲觀","cause":null,"prior_field":null,"side_a":"賣方：目標均價 135.6～150.5 美元、全距 130～179 美元，評等從 Hold 到 Buy 不等（TD Cowen 2026-05 升 Buy、目標 165；BNP Paribas Exane 2026-08 降 Hold）","side_b":"本次：觀望、不追","ruling":"可調和：分歧在框架不在事實。賣方假設 2027–28 共識兌現並給 9～10 倍；本次不否定方向，但認為景氣位置在中段，三到五成的下檔大於目標價一到兩成的上檔，跑道窄使長抱報酬只能靠低點買進。已跌 11% 不等於安全邊際。","evidence_level":"中：目標價時點不一（2026-08 前後）","settle_metric":"股價 vs 前瞻 7 倍（約 105 美元）與 2027 財測","if_then":["若股價先漲回 140 美元以上而 2027 財測未出 → 不追","若股價跌到約 105 美元以下而成長仍高於市場 → 重跑研究後分批建立"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國本土供應商以較低報酬要求搶份額，中國車廠擴張使傳統車廠（Lear 主要客戶）營收與份額下滑（10-K 風險因子）","side_b":"結構轉好與其他變數：歐盟討論在地含量法案、中歐預計 2026-12-01 起限制中國混動車出口每年 35 萬輛、中國 2027-04-01 起新能源車出口退稅由 13% 降到 9%，推動中國車廠海外在地化，Lear 已拿到 BYD 泰國與印尼、Leapmotor 南美案；另有 USMCA 檢討與美國關稅","ruling":"雙向拉鋸：中國帶來的競爭惡化，與在地化法規、關稅帶來的其他結構變動同時發生。在地化法規多屬『可能』或『預期』（2026-10-30 CFO 用語），不計入基準路徑；競爭惡化已反映在客戶讓份額的假設裡，計入空頭機率。","evidence_level":"中：法規尚未定案","settle_metric":"2027 年中國車廠占中國營收是否 ≥50%；中國車廠海外在地化新案數","if_then":["若歐盟在地含量法案定案且 Lear 拿到 ≥2 個中國車廠歐洲在地案 → 多頭機率上修 5 個百分點","若 2027 年中國車廠占中國營收仍 <50% → 假設二削弱"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"重大事件：財務長交接","cause":null,"prior_field":null,"side_a":"財務長 Jason Cardew 服務 34 年後退休","side_b":"2027-03-01 起由在職 23 年的 Jared Fedele 接任，已參與本季法說與財測說明","ruling":"計畫性內部接班，不是突發離職，不列核心風險；但 2027 財測是交接期的第一份年度指引，列入 2 月複審，觀察口徑是否改變","evidence_level":"高：法說原文","settle_metric":"2027 財測口徑與淨績效目標是否沿用","if_then":["若新任財務長上任後下修淨績效目標（座椅 40bp、E-Systems 80bp）→ 假設一削弱，停止任何建立"],"evidence_refs":[]},{"axis":"綜合訊號與估值結論漂移","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-24，股價 139.8 美元）：綜合訊號 B、估值便宜","side_b":"本次（股價 123.8 美元，前瞻 8.26 倍）：綜合訊號 B、估值便宜","ruling":"股價跌約 11%、FY1 共識三個月上修 0.47%，估值更便宜但沒有跨等級，兩欄不變","evidence_level":"高","settle_metric":"前瞻本益比","if_then":["若前瞻本益比 ≤7 倍 → 計入重啟條件"],"evidence_refs":[]},{"axis":"護城河方向與價值陷阱漂移","cause":"新證據","prior_field":["trap","moat_trend"],"side_a":"前份：價值陷阱中度、護城河方向持平","side_b":"本次：價值陷阱中度、護城河方向持平（不變）","ruling":"新證據雙向互抵。正面：Q3 成長高於市場 4 個百分點、整椅新案過半為新增或搶單、中國車廠新訂單占 23%。負面：中國連續數季成長低於市場、客戶讓份額假設由 1.5% 升到 3%。管理層 Q2 一度把中國車廠目標說成占總營收 50%，Q3 明確是中國營收口徑（44%→明年 50% 以上），以後者為準。訂單今天拿、營收 2028 年後才進來，屬時間差而非方向矛盾。","evidence_level":"中","settle_metric":"2027 年中國車廠占中國營收是否 ≥50%；成長高於市場是否維持正值","if_then":["若成長高於市場連 4 季轉負 → 護城河方向改判下降並清倉"],"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1"]},{"axis":"前份未判欄位補判","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄都是空值：舊版沒有要求成長跑道、公司類型與循環位置，也沒有產生情境機率與最大回撤","side_b":"本次：成長跑道窄、歸為景氣循環型、循環位置中段；情境機率多頭 20、基準 50、空頭 30，最大回撤 −35%～−55%；裁決與角色由程式依本次輸入重算","ruling":"屬方法變動，不是基本面翻轉。跑道窄加上循環型的歸類，讓長抱報酬只能靠低點進場，這是本次由『等回測』改為『等循環低點』的主因。","evidence_level":"中","settle_metric":"無（方法補判）","if_then":["若出現有來源的第二條成長曲線（例如模組化座椅營收占比明顯放大）→ 跑道改判中等"],"evidence_refs":[]},{"axis":"估值重啟條件改設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，只寫『觀望偏進場、等回測』","side_b":"三取二：前瞻本益比≤7倍（約105美元）／公司全年產量假設由年減轉年增／週收站回52週均線且250週均線斜率轉正；成立後重跑研究","ruling":"前份要的回測已經發生（139.8→123.8 美元），但本次把觀望的約束改成循環位置而不是價格：跑道窄的循環股只該在景氣低點建倉。重啟條件就是這個約束的否定；觸發後重跑研究，不直接建倉。","evidence_level":"中","settle_metric":"三項條件逐週檢查","if_then":["若三取二成立 → 重跑研究，通過後以小倉位分三批建立"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點改設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空值）","side_b":"Lear 加權全球產量出現年減 10% 以上的年度","ruling":"按數學上最大的單一敏感度挑選：營益率只有 4～5%、量的下行轉換率 15～25%，產量年減一成就吃掉三到五成核心營業利益，遠大於關稅或單一客戶事件。發生時若份額同時流失就清倉，否則分批反買。","evidence_level":"高：CFO 揭露的轉換率與 2009 年紀錄","settle_metric":"公司全年產量假設與實際 Lear 加權產量","if_then":["若年減 ≥10% 且成長低於市場連 2 季 → 清倉","若年減 ≥10% 但成長仍高於市場 → 分批反買"],"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"axis":"減碼與清倉門檻改設","cause":"新證據","prior_field":["kill_metrics","R"],"side_a":"前份未設清倉門檻；風險門檻為：單季座椅利益率 <5.5% 或 GM 產量連 2 季 −10%；座椅利益率連 4 季 <6.0% 才大動作；連 8 季成長落後產量 200bp","side_b":"本次：座椅調整後利益率連 2 季 <6.0% 減碼、連 4 季清倉；成長高於市場連 4 季轉負或年度新訂單 <25 億美元清倉；TTM 核心營益率連 2 季 <4.0% 減碼；未回收關稅年化 ≥5,000 萬美元減碼","ruling":"收緊的理由是新證據：Q3 座椅調整後利益率 6.3%（Q2 為 6.7%，雖含歐洲夏季停工的季節性），離 6.0% 只剩 30bp；CFO 揭露量的下行轉換率 15～25%，損害速度比前份假設快；成長落後產量 8 季才動作太慢，改用公司自己揭露的成長高於市場指標。","evidence_level":"高","settle_metric":"每季分部利益率與成長高於市場幅度","if_then":["若座椅利益率連 2 季 <6.0% → 減碼一半","若成長高於市場連 4 季 <0 → 清倉"],"evidence_refs":[]},{"axis":"論點假設改寫","cause":"新證據","prior_field":["H"],"side_a":"前份：H1 座椅利益率 FY26 ≥6.8%、FY27 ≥7.0%；H2 E-Systems 營收占比 FY27 ≥27%；H3 前瞻本益比 24 個月內回到 ≥11 倍","side_b":"本次：H1 淨績效抵銷逆風、FY2027 核心營益率 ≥5.0%；H2 成長高於市場與中國車廠訂單、2029 年高於市場 ≥3 個百分點；H3 買回每年減股、FY2027 年底股數 ≤46.0 百萬股","ruling":"前份 H1 的 FY26 門檻依 Q2 6.7%、Q3 6.3% 看已難達成，屬削弱的新證據（前份『連 2 季 <6.5%』的削弱條件目前只有 Q3 一季符合，尚未觸發），改用公司承諾的淨績效作可驗證門檻；E-Systems 正退出非核心產品線（2026 年少 9,000 萬、2027 年少 2.35 億營收），占比門檻失去意義；倍數回歸不是生意假設，移到情境樹終端倍數。","evidence_level":"高","settle_metric":"2026 全年座椅調整後利益率（2027 年 2 月）","if_then":["若 2026 座椅全年調整後利益率 <6.5% → 確認前份 H1 失效，本次 H1 門檻不變"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 2 月財測驗證淨績效假設","type":"假設驗證","maps_to":"H1","metric":"2027 核心營業利益財測中點 vs 2026 實際值；座椅 2026 全年淨績效","threshold":"中點 ≥2026 實際值且座椅淨績效 ≥40bp","action":"成立：計入重啟條件；不成立：假設一削弱、維持觀望","source_freq":"年度財測（Q4 法說）","date":"2027-02","evidence_refs":[]},{"n":2,"text":"Lear 加權產量出現年減一成以上的年度","type":"Single Thing","maps_to":"Single Thing","metric":"公司全年產量假設或實際 Lear 加權全球產量年增率","threshold":"年減 ≥10%","action":"若成長仍高於市場：確認流動性無虞後分批反買，不停損；若同時成長低於市場連 2 季：清倉不碰","source_freq":"每季財報、S&P Global Mobility 月度","date":null,"evidence_refs":["supply_demand_durability#0","supply_demand_durability#2","end_markets#2","cyclical_prior_downcycle_behavior#0"]},{"n":3,"text":"關稅吸收失敗","type":"風險","maps_to":"R4","metric":"未回收關稅淨成本（10-Q 揭露）；USMCA 檢討結果","threshold":"年化 ≥5,000 萬美元，或客戶公開拒絕分攤","action":"持有者減碼一半；未持有則延後重啟","source_freq":"每季 10-Q","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#2","geo_supply_chain#3"]},{"n":4,"text":"循環低點重啟","type":"估值rearm","maps_to":"H3","metric":"前瞻本益比；公司全年產量假設；週線均線","threshold":"三取二：前瞻 ≤7 倍（約 105 美元）／產量假設由年減轉年增／週收站回 52 週均線且 250 週均線斜率轉正","action":"觸發後重跑研究，通過後以小倉位分三批建立","source_freq":"每週價格、每季財報","date":null,"evidence_refs":[]},{"n":5,"text":"座椅利益率轉弱","type":"減碼","maps_to":"R2","metric":"座椅調整後營業利益率","threshold":"連 2 季 <6.0%（連 4 季則清倉）","action":"持有者減碼一半；未持有則重啟條件須三項全部成立","source_freq":"每季 8-K 分部資料","date":null,"evidence_refs":["supply_demand_durability#0","customer_concentration_credit#0"]},{"n":6,"text":"份額流失確認","type":"清倉","maps_to":"R3","metric":"整體成長高於市場的幅度；年度淨新訂單","threshold":"成長高於市場連 4 季 <0，或年度淨新訂單 <25 億美元","action":"清倉，撤銷重啟條件","source_freq":"每季法說","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_concentration_credit#1"]},{"n":7,"text":"複審：12 月投資人會議與 2027 年 2 月 Q4 財報","type":"複審日期","maps_to":null,"metric":"第四季進度、2027 財測、三年 backlog","threshold":"事件發生即複審","action":"重跑情境樹與機率","source_freq":"事件","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"Lear 加權全球產量年增率（公司財測假設與實際）","bear_threshold":"年減 ≥10%","window":"每季更新","source":"公司季度財報投影片產量假設","last_status":"ok"},{"metric":"座椅調整後營業利益率","bear_threshold":"連 2 季 <6.0% 減碼；連 4 季清倉","window":"季度","source":"8-K 新聞稿分部資料","last_status":"ok"},{"metric":"TTM 核心營業利益率（Non-GAAP）","bear_threshold":"連 2 季 <4.0%","window":"季度","source":"8-K 新聞稿","last_status":"ok"},{"metric":"整體成長高於市場的幅度","bear_threshold":"連 4 季 <0 個百分點","window":"季度","source":"法說會","last_status":"ok"},{"metric":"年度淨新訂單金額","bear_threshold":"<25 億美元","window":"年度","source":"Q4 法說會","last_status":"ok"},{"metric":"未回收關稅淨成本","bear_threshold":"年化 ≥5,000 萬美元","window":"季度","source":"10-Q 關稅揭露","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"三取二：前瞻本益比≤7倍（約105美元）／公司全年產量假設由年減轉年增／週收站回52週均線且250週均線斜率轉正；成立後重跑研究","exec_line":"觀望不追。重啟三取二成立後重跑研究，通過後以小倉位分三批建立；產量年減一成而成長仍高於市場時分批反買、不停損；座椅利益率連 2 季 <6.0% 減碼，成長高於市場連 4 季轉負清倉。","holding_cap":"≤3%：景氣循環、跑道窄，持有年限以 3 年為上限"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 8 倍前瞻本益比定價獲利見頂，忽略每年約 6% 的股數減少與連 4 季核心營業利益年增；即使產量持平，每股盈餘仍可年增約 6～8%","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等循環低點：前瞻本益比 ≤7 倍（約 105 美元）、公司產量假設由年減轉年增、週收站回 52 週均線且 250 週斜率轉正，三取二後重跑研究","qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":true,"basis":"runway_post_y5='🔴'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 8 倍前瞻本益比定價獲利見頂，忽略每年約 6% 的股數減少與連 4 季核心營業利益年增；即使產量持平，每股盈餘仍可年增約 6～8%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🔴', val='🟢', moat_trend='→', week26=-3.55, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"淨績效持續抵銷量與商品逆風：座椅每年 ≥40bp、E-Systems 每年 ≥80bp，核心營益率逐年上移","2y":"FY2027 核心營益率 ≥5.0%（2026 財測中點約 4.8%）","5y":null,"10y":null,"threshold":"FY2027 核心營益率 ≥5.0%；座椅調整後利益率每季 ≥6.0%","source":"每季 8-K 新聞稿分部資料、法說會淨績效拆解","drift_rule":"TTM 核心營益率較門檻路徑連 2 季落後 ≥5%（相對值）→ 削弱；連 3 季落後 ≥10% → 反轉"},{"id":"H2","text":"新案與搶單讓成長回到高於市場，中國車廠與日系客戶補上傳統客戶的流失","2y":null,"5y":"2029 年整體成長高於市場 ≥3 個百分點；中國車廠占中國營收 ≥55%","10y":null,"threshold":"2026 全年淨新訂單 ≥40 億美元（前三季約 39 億）；2027 年中國車廠占中國營收 ≥50%；三年核心 backlog ≥22.5 億美元","source":"Q4 法說 backlog 更新、季度新訂單與成長高於市場揭露","drift_rule":"成長高於市場連 4 季 <1 個百分點 → 削弱；連 6 季 <0 → 反轉"},{"id":"H3","text":"每股複利靠資本返還：約八成自由現金流用於買回與股利，股數每年減少約 5%","2y":"FY2027 年底流通股數 ≤46.0 百萬股（現約 48.2 百萬）","5y":null,"10y":null,"threshold":"每年買回 ≥3.5 億美元；自由現金流 ≥營收 2.3%","source":"10-Q 股數與現金流量表、法說會資本配置說明","drift_rule":"連 2 季買回年化 <2.5 億美元 → 削弱；暫停買回或連 3 季年化 <1.5 億美元 → 反轉"}],"R":[{"id":"R1","text":"中國內需與排程轉弱、商業談判未落地，拖累第四季與 2027 上半年","h_ref":"H1","clock":"⚡","threshold":"2026 核心營業利益 <10.8 億美元（財測下緣），或 2027 財測中點低於 2026 實際值；連 2 季未達即減碼","evidence_refs":["end_markets#2","supply_demand_durability#2"]},{"id":"R2","text":"北美產量下修，最大客戶 GM（占 22%）全尺寸卡車與 SUV 量能轉弱","h_ref":"H1","clock":"🔥","threshold":"座椅調整後利益率連 4 季 <6.0%（連 2 季先減碼），或 GM 相關平台量年減 ≥10% 連 2 季","evidence_refs":["supply_demand_durability#0","customer_concentration_credit#0"]},{"id":"R3","text":"中國車廠以在地與自製供應鏈擴張、中國本土供應商低報酬搶單，傳統客戶結構性失血","h_ref":"H2","clock":"🐢","threshold":"成長高於市場連 4 季 <0，或年度淨新訂單 <25 億美元，或 2027 年中國車廠占中國營收 <50%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_concentration_credit#1","substitute_technology#0"]},{"id":"R4","text":"美國關稅與 USMCA 檢討讓墨西哥低成本布局失去優勢，客戶不再分攤","h_ref":"H1","clock":"🔥","threshold":"未回收關稅淨成本年化 ≥5,000 萬美元，或客戶公開拒絕分攤關稅","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"重組費常態化，調整後 EPS 高估股東盈餘","h_ref":"H3","clock":"🐢","threshold":"2027 重組費 ≥2 億美元，且 GAAP 與核心營益率差距連 4 季 ≥1 個百分點","evidence_refs":[]}],"single_thing":{"description":"未來 24 個月內出現 Lear 加權全球汽車產量年減 10% 以上的年度（北美衰退或中國需求崩落）","why_fatal":"核心營益率只有 4～5%，CFO 揭露量的下行轉換率 15～25%：營收少 10%（約 23.5 億美元），營業利益就少 3.5～5.9 億美元，約占 2026 核心營業利益財測中點的三到五成，每年 40～80bp 的淨績效補不回來；2009 年營收年減 36% 時毛利一度轉負。","if_happens":"EPS 跌向 10～11 美元、倍數壓到 6 倍左右，股價約 60～70 美元。若成長仍高於市場（份額沒丟），確認流動性（29 億美元、債務平均到期約 11 年）後分批反買，不停損；若同時成長低於市場連 2 季，清倉。","how_monitor":"每季公司全年產量假設與實際 Lear 加權產量、S&P Global Mobility 月度產量預測、GM 與 Ford 排程變動","probability":"20%（12～24 個月）：北美 2027 已被下修 33.9 萬輛、中國內需持續轉弱，但 ITR 預期北美 2027 只約 −2.1%、2028 回升，年減一成需要真正的需求衰退"}},"appendix_a":{"growth_durability":4,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":7.4,"peg_fy2":0.52,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":14.99,"FY2027E":16.73,"FY2028E":19.52},"fy_end_month":12,"eps_basis":"調整後（Non-GAAP）稀釋 EPS，Koyfin 共識快照 2026-10-31；FY2025 調整後實際值事實表未涵蓋，GAAP 稀釋 EPS 8.15 口徑不同，不可當基期"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"投資人會議更新第四季進度","impact":"中","watch":"第四季是否守住核心營業利益中點、中國排程變化"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報、2027 全年財測與三年 backlog","impact":"高","watch":"2027 核心營業利益中點 vs 2026 實際值、淨績效目標是否沿用"},{"date":"2027-01","date_precision":"quarter","type":"capacity","event":"Orion 自動化整椅廠投產（供 GM Escalade、Silverado、Sierra）","impact":"中","watch":"量產爬坡，以及轉換成本是否真降 10～15%"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"中歐預計限制中國混動車出口每年 35 萬輛","impact":"低","watch":"中國車廠歐洲在地化新案"},{"date":"2027-03","date_precision":"month","type":"other","event":"新任財務長 Jared Fedele 上任","impact":"低","watch":"資本配置與財測口徑是否延續"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"中國新能源車出口退稅由 13% 降到 9%","impact":"低","watch":"中國車廠海外在地化速度"}]}
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
