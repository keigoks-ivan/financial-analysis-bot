你是 DD 管線 v20 的判斷層閘（gate），標的 ROP（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_gaap_revenue`（q1_business）｜GAAP revenue＝2171.8 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release（8-K Ex.99）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未查得
- `f_kpi1_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝28.7 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release；營業利益 623.2M，利益率為 623.2/2171.8 自算（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未查得
- `f_kpi2_adjusted_ebitda_margin`（q1_business）｜Adjusted EBITDA / margin＝39.8 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release；adj. EBITDA 864M，+7% YoY（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未查得
- `f_kpi3_adjusted_diluted_eps`（q1_business）｜Adjusted diluted EPS＝5.89 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release（經 web search 摘要；GAAP DEPS 4.88）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未查得（管理層稱優於其預期）
- `f_kpi4_free_cash_flow_ocf_capex`（q1_business）｜Free cash flow（前九個月，OCF − capex − 資本化軟體，自算）＝1800.0 USD M｜期間與口徑：9M FY2026（截至 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release 現金流量表：OCF 1,882.2M、capex 35.4M、資本化軟體 46.8M；新聞稿未直接列 FCF（numbers.latest_quarter_kpis.items[4]，as_of 9M FY2026（截至 2026-09-30，公告於 2026-10-22））
  - 註記：未查得
- `f_kpi6_guidance_fy2026_adjusted`（q1_business）｜Guidance：FY2026 adjusted DEPS＝22.35–22.40 USD｜期間與口徑：Q3 FY2026 公告（2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Roper Q3 2026 earnings release（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026 公告（2026-10-22））
  - 註記：上調自 22.15–22.30；最新快照共識 FY1 22.34（consensus_revision）
- `f_peer_rop_gross_margin_pct`（q2_moat）｜ROP 毛利率＝69.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROP.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rop_operating_margin_pct`（q2_moat）｜ROP 營業利益率＝27.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROP.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rop_fcf_margin_pct`（q2_moat）｜ROP FCF 利潤率＝30.93 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_csu_to_gross_margin_pct`（q2_moat）｜CSU.TO 毛利率＝37.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSU.TO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_csu_to_operating_margin_pct`（q2_moat）｜CSU.TO 營業利益率＝17.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSU.TO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_csu_to_fcf_margin_pct`（q2_moat）｜CSU.TO FCF 利潤率＝21.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSU.TO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tyl_gross_margin_pct`（q2_moat）｜TYL 毛利率＝47.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TYL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tyl_operating_margin_pct`（q2_moat）｜TYL 營業利益率＝15.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TYL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tyl_fcf_margin_pct`（q2_moat）｜TYL FCF 利潤率＝29.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TYL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jkhy_gross_margin_pct`（q2_moat）｜JKHY 毛利率＝43.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JKHY.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jkhy_operating_margin_pct`（q2_moat）｜JKHY 營業利益率＝24.96 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JKHY.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jkhy_fcf_margin_pct`（q2_moat）｜JKHY FCF 利潤率＝19.91 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JKHY.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ame_gross_margin_pct`（q2_moat）｜AME 毛利率＝36.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AME.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ame_operating_margin_pct`（q2_moat）｜AME 營業利益率＝25.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AME.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ame_fcf_margin_pct`（q2_moat）｜AME FCF 利潤率＝23.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AME.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝22.34 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝24.57 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝26.39 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_kpi5_stock_based_compensation`（q1_business）｜Stock-based compensation（前九個月）＝163.9 USD M｜期間與口徑：9M FY2026（截至 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Roper Q3 2026 earnings release 現金流量表 non-cash stock compensation（numbers.latest_quarter_kpis.items[5]，as_of 9M FY2026（截至 2026-09-30，公告於 2026-10-22））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.831 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝438.14 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.61 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 22.34，分子＝快照價 438.14｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_rsi14`（q5_valuation）｜RSI(14)＝80.65｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝24.6 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.45 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（22.24 → 22.34）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.74 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（24.39 → 24.57）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 438.14 / W52 379.55 / W104 459.77 / W250 464.0 / W250 13週斜率 -0.26%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝379.55 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子指出可能出現新競爭者，產品線可能受包含 AI 在內的新技術威脅；AI 能力可能快速商品化。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：AI／agentic 產品2026年尚非重大營收，變現預期為2027年議題；分析師7月將合理價自694降至550，理由為 AI 衝擊財務模型耐久性的疑慮
  - 來源：Simply Wall St narrative update for Roper Technologies（as_of 2026-01-07）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明銷售須遵守 EAR、ITAR、OFAC 制裁，並可能受新增、擴大或報復性關稅影響
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：第三方彙整稱 Roper 近期申報提示美國對中國、加拿大、墨西哥、英國等的新增或報復性關稅風險，並有單一來源供應商與少數雲端平台依賴
  - 來源：policyrisk.com ROP（as_of 2026-01-01）｜affects：decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Deltek 政府承包企業業務 Q1 仍疲弱（聯邦採購中斷、機關重組、預算不確定）；管理層 2026 指引未預設 Neptune 復甦
  - 來源：Roper Q1/Q2 2026 call 摘要（Quartr／vectorshift）（as_of 2026-07-23）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FY2025 10-K 風險因子明列：若出現競爭或替代技術，商譽（$21,341.2，約占總資產 62%）可能減損；收購風險評估亦提及「來自 AI 的市場顛覆」易感性。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-24）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 揭露其 AI 產品依賴第三方 LLM 供應商（OpenAI、Anthropic、Google、Microsoft），供應商可能漲價且 Roper 未必能轉嫁給客戶。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-24）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Seeking Alpha 2026-01 文章稱股價自高點下跌近 40%，歸因於 AI 引發的軟體股拋售。
  - 來源：Seeking Alpha 'Roper Technologies: At A Crossroad'（as_of 2026-01-15）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":892.8,"bear_5y_price":317.2,"p_bull_pct":25,"p_bear_pct":25,"upside_5y_pct":36.4,"ev5y_pct":37.2,"irr_base_pct":6.4,"asym_ratio":3.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":22.34,"pe":19.61,"basis":"FY1（FY2026）共識調整後EPS，與終端倍數同為前瞻一年口徑"},"eps":{"bull":[25.0,27.6,30.5,33.7,37.2],"base":[24.57,26.39,28.5,30.8,33.2],"bear":[23.2,23.5,23.8,24.1,24.4]},"pe":{"bull":24,"base":18,"bear":13},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.831,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ROP_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Neil Hunn｜guidance：全年調整後 DEPS 指引第二度上調，區間 22.15–22.30 美元（原話："second time this year to a range of $22.15 to $22.30."）
- 2026-07-23｜Neil Hunn｜guidance：全年營收成長指引上調：總營收 8% 以上、有機約 6%（有機數字在同句後段）（原話："guidance to north of 8%, with organic revenue growth"）
- 2026-07-23｜Neil Hunn｜guidance：Q3 調整後 DEPS 指引 5.75–5.80 美元（原話："we're establishing adjusted DEPS guidance of $5.75 to $5.80."）
- 2026-07-23｜Neil Hunn｜guidance：指引不含 Indicor 出售儀器業務的收益（原話："excludes any proceeds from Indicor's divestiture of its"）
- 2026-07-23｜Neil Hunn｜guidance：應用軟體下半年有機成長預期為中個位數偏上（原話："to be in the mid-single-digit plus range."）
- 2026-07-23｜Neil Hunn｜guidance：TEP 下半年有機成長預期為高個位數，Q3 較強（原話："high singles range and be a bit stronger in Q3."）
- 2026-07-23｜Jason Conley｜guidance：有機經常性營收成長預期於下半年走高（原話："organic recurring revenue growth to inflect higher"）
- 2026-07-23｜Neil Hunn｜guidance：管理層說明上調主要來自上半年已實現的表現與下半年機械性因素，仍保留審慎區間（原話："it was a lot of the increase is sort of in the bank."）
- 2026-07-23｜Jason Conley｜guidance：指引未計入 AI 帶來的實質貢獻，AI 變現屬 2027 規劃（原話："we haven't really baked in anything meaningful for AI"）
- 2026-07-23｜Jason Conley｜margin：核心 EBITDA 利潤率下滑 70bp，主因 TEP；軟體部門僅降 10bp 且含 AI 團隊投資（原話："Core EBITDA margin was down 70 basis points."）
- 2026-07-23｜Neil Hunn｜margin：TEP 利潤率下滑來自 Neptune 青銅錠投入成本通膨，以及 NDI/Verathon 耗材組合偏移（原話："Input cost pressure at Neptune, principally bronze ingot"）
- 2026-07-23｜Jason Conley｜margin：管理層預期下半年 Neptune 利潤率改善且比較基期較易（原話："we expect margin improvement at"）
- 2026-07-23｜Neil Hunn｜margin：網路軟體 EBITDA 利潤率年減 370bp 與核心利潤率微增 30bp 的落差，歸因於 Subsplash 收購與 DAT/Convoy 投資（原話："The gap reflects 2 dynamics: the acquisition of Subsplash"）
- 2026-07-23｜Jason Conley｜margin：AI 團隊人力投資約完成一半，支出占比因先聘資深人員而更高，多數已在 Q2 基期內（原話："a lot of that is already in our second quarter base"）
- 2026-07-23｜Jason Conley｜margin：公司 AI 工具/token 支出年化已為 1 月的約 3 倍，預期年底前再上升（原話："annualized basis, about 3x since January."）
- 2026-07-23｜Neil Hunn｜customer：企業軟體毛留存率維持在 90 中段，核心訂單 TTM 成長中個位數以上（原話："retention remained strong consistently in the mid-90s."）
- 2026-07-23｜Neil Hunn｜customer：Deltek 政府承包市場：有鼓舞跡象但尚不上調展望，要看管線連續數季轉換（原話："we'd like to see the sales pipeline convert consistently"）
- 2026-07-23｜Jason Conley｜customer：Deltek Q2 受惠於一筆未納入指引的大型授權案（原話："We had mentioned a large license deal that we had not put"）
- 2026-07-23｜Neil Hunn｜customer：DAT 貨運市場出現多項改善指標，但貨量尚未回升（原話："We still need to see load volumes improve before becoming"）
- 2026-07-23｜Jason Conley｜customer：DAT 2026 年僅預期小幅受益，重點放在 2027（原話："not baking in a massive inflection up"）
- 2026-07-23｜Neil Hunn｜customer：Neptune 營收小幅年減但優於預期；表計業務預計下半年回到成長（原話："remains on track to return to growth in the second half."）
- 2026-07-23｜Jason Conley｜customer：網路軟體中 MHA 與 iPipeline 的重複性/非經常性營收偏弱，MHA 因大客戶單位經濟較低（原話："more large customers with lower unit economics, and"）
- 2026-07-23｜Neil Hunn｜customer：Procare 被形容為仍需調整的業務，正補強核心產品、市場執行與導入能力（原話："Procare remains a work in progress."）
- 2026-07-23｜Neil Hunn｜product：AI/agentic 產品發布節奏加速，管理層稱商業化曲線仍早期（原話："we're still early in the commercialization curve"）
- 2026-07-23｜Neil Hunn｜product：Vertafore 發布 Velocity 平台，首批 6 個 agentic SKU（原話："released its AI velocity platform with 6 agentic SKUs"）
- 2026-07-23｜Neil Hunn｜product：Vertafore agentic 在 5 個領域的 TAM 擴張估計約為現有市場的兩倍，6 個 SKU 僅占一小部分（原話："It's a doubling-ish of the"）
- 2026-07-23｜Neil Hunn｜product：管理層自承 TAM 數字為推測（原話："And by the way, these are informed"）
- 2026-07-23｜Neil Hunn｜product：SoftWriters AI 訂單輸入把處理時間由約 90 秒降到約 18 秒，採交易計價（原話："SoftWriters prices the solution transactionally,"）
- 2026-07-23｜Neil Hunn｜product：Procare 首個 agentic 功能（未變現）上線 4 小時內約 20% 客戶使用（原話："within 4 hours of release, I think 20% of the customer base"）
- 2026-07-23｜Neil Hunn｜product：AI 變現主要採訂閱制 agent 層加階梯式用量層級，非純用量計費；Deltek 靠上雲加價、DAT/SoftWriters 交易計價（原話："Imagine it's going to be stair step consumption."）
- 2026-07-23｜Jason Conley｜product：地面轉雲端遷移持續推進；Deltek Costpoint 宣告停止支援舊版（原話："they actually just end of life on"）
- 2026-07-23｜Neil Hunn｜risk：客戶採用速度是最大未知數，近期變現規模無法具體說明（原話："pace of adoption at the customer level? That's the unknown."）
- 2026-07-23｜Neil Hunn｜risk：AI 產品 2026 年下半年不會形成實質營收（原話："So will it be material revenue in the"）
- 2026-07-23｜Neil Hunn｜risk：開發策略由方法化低風險轉向高速、容許部分失敗（原話："if we miss on a few, that's okay"）
- 2026-07-23｜Neil Hunn｜competition：管理層主張垂直軟體護城河：領域專長、嵌入式工作流、獨有資料、信任與配銷（原話："deep domain expertise, embedded customer workflows, unique"）
- 2026-07-23｜Neil Hunn｜competition：Aderant 定位為法律「事務所營運」(ERP/計費)，而非 Harvey 等「執業」AI；市占由 35% 升至 65%（原話："Aderant is all about the business of law."）
- 2026-07-23｜Neil Hunn｜competition：法律計費模式轉向固定費用的採用度目前仍偏低（原話："relatively low uptake across the industry."）
- 2026-07-23｜Neil Hunn｜competition：管理層稱自家 AI 產品進度領先私募買家持有的標的，但對方在追趕（原話："we're ahead on the product side versus the sponsors"）
- 2026-07-23｜Jason Conley｜capital_allocation：Q2 以約 12 億美元、均價約 341 美元回購 360 萬股，8 個月累計 32 億美元（原話："3.6 million of shares for $1.2 billion"）
- 2026-07-23｜Jason Conley｜capital_allocation：淨負債/EBITDA 由 3.1x 升至 3.4x，循環信貸已動用 29 億美元（原話："We exited the second quarter at 3.4x net debt to EBITDA"）
- 2026-07-23｜Jason Conley｜capital_allocation：Indicor 儀器業務出售予 AMETEK，預估稅前約 14 億、稅後約 12 億美元，下半年close（原話："approximately $1.4 billion or an estimated $1.2 billion"）
- 2026-07-23｜Jason Conley｜capital_allocation：年化資本部署能力超過 50 億美元（原話："more than $5 billion of annualized capacity for capital"）
- 2026-07-23｜Neil Hunn｜capital_allocation：管理層稱過去 8 個月因股價水準回購轉為顯著較有吸引力，此前數學一向偏向 M&A（原話："the capital allocation mathematically always favored"）
- 2026-07-23｜Neil Hunn｜capital_allocation：上半年除回購外僅兩筆小型併購，合計約 5,000 萬美元（原話："Well, outside the buyback, there are 2 small bolt-ons."）
- 2026-07-23｜Neil Hunn｜capital_allocation：併購策略：買贏家，不做買進後修復（原話："We're going to buy the winners and make them better."）
- 2026-07-23｜Neil Hunn｜capital_allocation：賣方（私募）估值預期鬆動，管理層看到自營機會增加，但預期不會短期內大爆發（原話："the new 15 is yesterday's 25"）
- 2026-07-23｜Neil Hunn｜commitment：未來 12–18 個月審慎樂觀部署 50 億美元以上於併購（原話："cautiously optimistic about deploying $5 billion"）
- 2026-07-23｜Neil Hunn｜commitment：近期資本部署偏向去槓桿而非機會性回購（敘事由前兩季大量回購轉向）（原話："near-term capital deployment will favor deleveraging over"）
- 2026-07-23｜Jason Conley｜commitment：預期 M&A 活動於今年稍後及 2027 年啟動，並先整備資產負債表（原話："We expect M&A activity to break loose later this year"）
- 2026-07-23｜Neil Hunn｜commitment：資本配置框架不變，以每股現金流長期複利為目標（原話："our capital allocation framework remains unchanged."）

### 問答異常語氣（迴避／改口／保留）
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Tillman：這些 agentic 產品何時能進入大規模生產工作負載（下半年？）｜答法：未給時點，改談學習曲線與組織動能；僅明確表示今年不會有實質營收，採用速度為「大未知數」
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Jester：2027 年 AI 變現上行空間有多大｜答法：明言不給 2027 變現金額，稱在客戶採用訊號更清楚前「unfortunately vague」
- ROP_Q2_2026_Earnings_Call_20260723.md｜問：Tilton：指引中還剩多少保守成分｜答法：未量化，僅稱仍有結果區間，要保持審慎以便全年強勢收尾

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 1 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 2 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Roper Technologies largest customer concentration 10-K 2026；Roper Technologies customers in-house OR insourcing OR second source 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"VMS 護城河（工作流鎖定+合規+專有資料）抵禦 AI 通用化，組織不被侵蝕","columns":{"2Y 驗證點":"合併有機成長維持 5-6%、旗艦淨留存 ≥93%","5Y 驗證點":"留存 ≥90%、無旗艦垂直被 AI-native 對手系統性搶客","10Y 驗證點":"核心垂直仍為該行標準系統，AI 為加值層非替代","數字門檻":"旗艦淨留存 ≥90%;合併有機 ≥5%","來源":"公司法說（Q1 2026）+ 產業（Gartner 垂直 AI）","漂移觸發":"連 2 季 TTM 有機 &lt;4% → 削弱"}},{"id":"H2","text":"M&A 飛輪持續：大型 Tier-1 交易 cash-on-cash 維持約雙位數，不向 WACC 崩塌","columns":{"2Y 驗證點":"年度部署 ~$2-4B，揭露交易 ROIIC ≥ WACC","5Y 驗證點":"累積 M&A 增量 NOPAT/投入 ≥ 10-12%","10Y 驗證點":"飛輪未被「越來越貴的下一筆」吃掉；槓桿 ≤3x","數字門檻":"大型交易 ROIIC ≥ ~10%;ND/EBITDA ≤3x","來源":"公司揭露 + 賣方（PE 出價競爭）","漂移觸發":"年度 ≥2 筆大型交易出價落敗，或揭露 ROIIC &lt; WACC → 削弱"}},{"id":"H3","text":"市場對「高品質軟體 vs 中速槓桿 rollup」的重定性部分修復（15x → ~17-18x fwd）","columns":{"2Y 驗證點":"Fwd P/E 回升至 ≥16x","5Y 驗證點":"倍數穩定於 17-19x（peer/自身歷史下緣）","10Y 驗證點":"不再被永久打「conglomerate 折價」","數字門檻":"Fwd P/E ≥16x 且 EPS 兌現","來源":"賣方目標價（median $456）+ 同業（CSU 17.5x）","漂移觸發":"Fwd P/E 至 2027 仍困 &lt;13x → 反轉（永久重定性）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI-native 垂直軟體挑戰者（Onit/Applied Systems/新創潮）在旗艦垂直搶客 → 留存/定價侵蝕","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"旗艦淨留存、法律/保險垂直份額","警戒閾值":"任一旗艦淨留存 &lt;90% 或公開丟標竿客戶"}},{"id":"R2","text":"Deltek/GovCon 結構性永久降速（DOGE、聯邦採購凍結）+ DAT 貨運長弱","columns":{"對應假設":"H1","時間尺度":"🔥 中期（已跨 2025-26）","監測指標":"Deltek/DAT 有機成長、聯邦撥款能見度","警戒閾值":"Deltek 有機至 FY2026 底仍為負且無回穩"}},{"id":"R3","text":"大型 Tier-1 M&A 被 PE dry powder 抬價 → cash-on-cash 向 WACC 收斂；槓桿見頂限制飛輪","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"交易 ROIIC、ND/EBITDA、出價落敗次數","警戒閾值":"年度 ≥2 筆大交易落敗，或揭露 ROIIC &lt; WACC，或 ND/EBITDA &gt;3.5x"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","irr_base_pct":11.5,"ev5y_pct":70.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.4,"ev5y_pct":70.0,"irr_base_pct":11.5,"max_dd_pct":-42.0,"bull_5y_price":886.0,"bear_5y_price":270.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","price_at_dd":355.94,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ROP","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Roper Technologies"},"oneliner":"美國利基垂直軟體收購平台，Q3有機成長7%、全年EPS指引年內三度上調，AI代理產品已大範圍上市但變現未證；股價半年漲24.6%、前瞻本益比19.6倍，基本面無損但價格先走，等回落再買。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是美國利基產業（律所、保險代理、政府承包商、醫院財務、貨運仲介、藥局、水公用事業）每年續約的軟體訂閱與維護費，錢卡在客戶帳務、計費與合規工作流這一節點；Q3營收21.718億美元、營益率28.7%、調整後EBITDA利潤率39.8%，調整後EPS 5.89美元年增15%。","reasoning":"分部（Q3法說）：應用軟體營收年增7%、有機6%、EBITDA利潤率43.7%；網路軟體年增8%、有機5%、利潤率52.4%；TEP（Neptune水表、NDI量測、Verathon醫材）年增10%、有機10%、利潤率34.3%。Q2三分部營收分別為11.8億、4.309億、4.972億美元，應用軟體約占56%。集中度：2025年無單一客戶占任一分部或公司營收10%以上，美國以外營收13%，沒有單點客戶依賴；上游單點依賴在第三方大型語言模型供應商。產業時鐘判在擴張期（II）：依據是兩軟體部門有機經常性營收由Q2的7%升到Q3的8%、企業核心訂單近12個月中個位數成長，加上私募賣方估值預期鬆動使收購環境轉好，不是看股價。供需耐久性：軟體端屬結構性持久（企業軟體毛留存連續多季在90%中段）；週期性將反轉的部分集中在Neptune表計（新冠後換表高峰的消化期）與DAT貨運（供給面回升、貨量未回）。資本輕：前九月資本支出3,540萬加資本化軟體4,680萬美元，對營業現金流18.822億美元約4%，管理層預估全年自由現金流約營收30%。","fact_refs":["f_kpi0_gaap_revenue","f_kpi1_gaap_operating_income_ma","f_kpi2_adjusted_ebitda_margin","f_kpi3_adjusted_diluted_eps","f_kpi4_free_cash_flow_ocf_capex","f_kpi6_guidance_fy2026_adjusted"],"verdict_values":{"revenue_quality":"經常性收入為主：兩軟體部門有機經常性營收Q3年增約8%，企業軟體毛留存90%中段（Q3法說）；TEP硬體（Neptune表計、NDI、Verathon）屬專案與耗材型，季度波動較大，本季機械式表計組合偏高拖累營收與利潤率。","unit_econ_note":"資本支出加資本化軟體約營業現金流4%，FCF利潤率TTM約31%；新增營收幾乎不需資本，股東報酬的變數在收購價格而非營運投資。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利經常性軟體收入＋以自由現金流持續收購的資本配置平台，股東報酬取決於下一筆收購的增量報酬"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：企業軟體毛留存連續多季90%中段、有機經常性營收8%（Q3法說）；週期性部分集中在Neptune表計換表週期與DAT貨運需求，兩者合計不是營收主體。","bargaining":{"up":"對上游：AI功能依賴OpenAI、Anthropic、Google、Microsoft等模型供應商，10-K明言漲價未必能轉嫁；Neptune有青銅錠成本通膨（Q2法說）。","down":"對客戶：無單一客戶占營收10%以上，毛留存90%中段，議價力在公司這邊。","geo":"美國以外營收13%，地緣與關稅曝險集中在TEP硬體。"},"profit_pool_dir":"垂直軟體利潤池可能有一部分流向模型供應商，但目前毛利率未見移轉（TTM 69.53%）；方向待2027年AI收費規模揭露後才能判斷。","tam_table":{"expanded":false,"reason":"29家事業分散在數十個利基垂直，事實表未涵蓋任何垂直的TAM、滲透率或利潤池占比；唯一的TAM數字（Vertafore代理AI讓可服務市場約翻倍）是管理層自承的推測，不能承重；成長判斷改以有機經常性營收與毛留存承重。"}}}},"q2_moat":{"verdict":"護城河方向穩定（→），等級B：機制是工作流嵌入加專有資料造成的轉換成本，可證方向是毛利率69.53%與營益率27.97%對四家同業（毛利率36%–47%、營益率15%–26%）的持續領先，以及企業軟體毛留存連續多季維持90%中段；AI是目前最大的未決威脅。","reasoning":"執行力給8分：Q3有機成長7%、全年EPS指引年內三次上調（累計較原始指引高0.95美元）、21家軟體事業中17到18家已有代理式AI產品上市，管理層稱尚無明顯失敗的上市案。定價力給7分：毛利率FY2022 69.86%到FY2025 69.24%小幅下移，TTM 69.53%，沒有擴張證據；Vertafore改用價值點數計價、Strata以加購訂閱賣AI功能，屬試探提價但尚未反映在數字。同業ROIC事實表未涵蓋，只能比利潤率，因此等級壓在B不往上。報酬持續期：高利益率×低周轉，資產負債表約六成是商譽，帳面ROIC偏低，股東報酬主要取決於下一筆收購的增量報酬，而這個數字公司未揭露。四檢查點中需求基礎值與社會容忍度為綠，決策層級與價值鏈分配為黃，黃燈都與AI有關：替代可能先在單一工作流任務出現，模型成本可能被上游拿走。","fact_refs":["f_peer_rop_gross_margin_pct","f_peer_rop_operating_margin_pct","f_peer_rop_fcf_margin_pct","f_peer_csu_to_gross_margin_pct","f_peer_csu_to_operating_margin_pct","f_peer_csu_to_fcf_margin_pct","f_peer_tyl_gross_margin_pct","f_peer_tyl_operating_margin_pct","f_peer_tyl_fcf_margin_pct","f_peer_jkhy_gross_margin_pct","f_peer_jkhy_operating_margin_pct","f_peer_jkhy_fcf_margin_pct","f_peer_ame_gross_margin_pct","f_peer_ame_operating_margin_pct","f_peer_ame_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"工作流嵌入＋專有資料（例如Strata數十年累積的醫院總帳對照與病患層級成本會計）＋產業合規需求，形成高轉換成本；可證方向用毛留存與對同業的利潤率差距。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力穩定：毛留存連續多季90%中段（Q2、Q3法說）、Q3有機成長7%、有機經常性營收由7%升到8%；定價力穩定：年度毛利率FY2022 69.86%→FY2025 69.24%小幅下移、TTM 69.53%，未見擴大也未破位；兩維皆穩定，方向判為不變。","competitor_notes":[{"name":"CSU.TO","strategy_note":"同為垂直軟體收購平台，毛利率37.26%、FCF利潤率21.92%低於ROP，但兩家成本列報口徑可能不同，利潤率差距不宜全歸因於護城河；它是收購市場上最直接的出價對手。"},{"name":"TYL","strategy_note":"政府垂直軟體，營益率15.14%遠低於ROP、FCF利潤率29.05%接近，帳面利潤與現金之間的落差比ROP大；客群與Deltek的政府承包業務相近，是政府端上雲與AI節奏的對照。"},{"name":"JKHY","strategy_note":"銀行核心系統供應商，營益率24.96%、FCF利潤率19.91%，是單一垂直深耕的對照組；ROP本季新收購的c. myers也面向銀行與信用合作社。"},{"name":"AME","strategy_note":"工業儀器收購平台，營益率25.9%接近ROP的TEP分部，也是Indicor儀器業務的買家；只用來對照ROP硬體分部，不是軟體護城河的對照。"}],"peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，只能以毛利率、營益率、FCF利潤率比較；同業前瞻本益比也未涵蓋。","threats":[{"level":"🟡","text":"AI原生垂直方案或通用代理在任務層繞過既有工作流，先壓定價再侵蝕留存；目前留存未見受損，若旗艦垂直公開失去大型客戶即升級為生態攻擊。","p":30,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"第三方模型供應商漲價而公司無法轉嫁，AI加值功能的毛利被上游拿走；緩解是每個產品都有模型路由可切換較小或開源模型。","p":25,"evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"私募買方回到收購市場抬高倍數，收購增量報酬向資金成本收斂。","p":25,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是律所會計、保險代理、醫院財務人員，決策者與付款者是同一機構的管理層，三角色都在；工作屬計費、合規、結帳等不能延後的需要而非想要。2025年無客戶占營收10%以上。例外是Neptune水表的換表時點可延後（新冠後換表高峰正在消化）。"},{"item":"決策層級","level":"🟡","text":"以整套系統衡量替代性仍低：企業軟體毛留存連續多季90%中段，Deltek Costpoint地端停止支援反而推動客戶升級上雲。但AI代理把替代的最小單位從整套系統縮到單一任務（例如計費描述、保單處理），對手可在任務層切入，現有留存數字還反映不到這一層。"},{"item":"價值鏈分配","level":"🟡","text":"AI功能依賴少數模型供應商，10-K明言漲價未必能轉嫁；關鍵互補品集中在少數供應商，是價值被上游拿走的典型風險。緩解是每個產品都有模型路由，管理層稱代理工具毛利與軟體毛利相當（Q3法說）。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與機構，不是消費者必需品，大幅漲價的政治敏感度低；子公司PowerPlan的反壟斷訴訟已於2025年1月以2,400萬美元和解結案，未見現行反壟斷調查。Neptune售予受費率審議的水公用事業，屬間接約束，占比有限。"}],"roiic":"事實表未涵蓋：近年收購金額與被收購事業的獲利貢獻未揭露。可得線索僅有管理層稱Q3三筆小型收購成長快於母體、合併綜效後報酬很有吸引力，屬未量化說法。本次以收購稅後現金報酬約7%–8%作為工作假設（未驗證）。","reinvest_rate":"推估約80%–100%的自由現金流再投入收購或回購：全年自由現金流約營收30%（Q3法說），管理層稱未來12個月可部署資本逾60億美元；比例是推論，非揭露值。","endo_ceiling":10,"formula_note":"內生成長上界約10%＝有機成長約6%（全年指引，幾乎不耗資本：資本支出加資本化軟體約營業現金流4%）＋收購再部署約4點（再投資率約九成×假設增量報酬約7%–8%，換算到每股盈餘再扣利息成本與整合期稀釋，保守取4點）。帳面ROIC下限：FY2025營業利益約22.36億美元（79.025億×28.29%）×（1−21%稅率）≈17.7億；投入資本以總資產上限約344億（商譽213.412億÷62%）計，ROIC約5%，未加回攤銷，屬保守下限。"}}}},"q3_growth":{"verdict":"五年後成長跑道中等（🟡）：有機成長約6%加收購撐得住8%左右的每股盈餘成長，AI可能是第二條曲線但尚未在營收出現。","reasoning":"成長組成：量與價的有機成長約6%（全年指引，Q3單季7%），併購今年約貢獻1點，回購前八個月約32億美元但Q3暫停、轉向收購。共識調整後EPS：FY2026 22.34、FY2027 24.57、FY2028 26.39美元，FY1到FY3年化約8.7%；FY2025調整後基期事實表未涵蓋，三年CAGR無法依公式算，改用兩年年化。內生上界約10%（見護城河段），共識低於上界，缺口為負，不需依賴倍數擴張。跑道：各垂直滲透率未揭露，年數事實表未涵蓋；Aderant在法律事務所營運軟體的份額由35%升到65%（Q2法說），說明部分旗艦已高滲透，新的成長要靠AI加值與上雲加價，而Vertafore代理AI讓可服務市場約翻倍是管理層自承的推測。衰退信號亮一個、接近亮一個：軟體類股估值倍數在2026年初AI拋售中系統性下移；年度毛利率連三年小幅下移。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_guidance_fy2026_adjusted","f_peer_rop_gross_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量（有機約6%：經常性營收與模組加購）＋價（AI點數與加購訂閱、Deltek上雲加價）＋併購（今年約1點）＋回購（前八個月約32億美元，Q3暫停）","runway_years":"事實表未涵蓋（各垂直滲透率未揭露）","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段內生上界約10%：有機約6%＋收購再部署約4點；共識FY1到FY3年化約8.7%落在上界內。","segments":[{"item":"應用軟體（Q3）","value":"營收年增7%、有機6%、EBITDA利潤率43.7%（年增30bp）；Q4預期有機中個位數偏上"},{"item":"網路軟體（Q3）","value":"營收年增8%、有機5%、EBITDA利潤率52.4%（年減130bp，核心大致不變）；DAT加速，Q4有機略高於Q3"},{"item":"TEP（Q3）","value":"營收與有機皆年增10%、EBITDA利潤率34.3%（年減90bp）；Neptune機械式表計組合偏高，Q4有機中個位數"},{"item":"Q2營收規模","value":"應用軟體11.8億、網路軟體4.309億、TEP 4.972億美元"}],"decay_signals":["產業估值倍數下移：軟體類股2026年初因AI拋售倍數下移，第三方報導股價一度自高點跌近40%，亮燈","毛利率：年度數字FY2022 69.86%→FY2025 69.24%連三年小幅下移（季度年比資料事實表未涵蓋），接近亮燈","EPS成長高於營收成長：Q3調整後EPS年增15%、營收8%，差距來自回購與利息，屬單季未連續，暫不亮燈","其餘類別（市占縮減、提價後量減、FCF對淨利過低、SBC過高、TAM被壓縮、維護性資本支出過高、停止投資）證據包內未見亮燈"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律可信、收購報酬未經外部驗證：今年先大舉回購（前八個月約32億美元、Q2均價約341美元），股價回升後轉向去槓桿與小型收購，淨負債/EBITDA由3.4倍降到2.9倍。","reasoning":"現金：前九月營業現金流18.822億美元，扣資本支出與資本化軟體後自由現金流約18億，管理層預期全年自由現金流約營收30%、每股自由現金流與調整後EPS同步或略好。Q3自由現金流8.05億美元年減4%，原因是2025年發行債券的票息時點與Illumia導入ERP造成收款延遲，部分可能延到2027年第一季（Q3法說），列為未證的一次性歸因，若2027年第一季自由現金流仍年減即證偽。去向：回購（Q3暫停，授權仍有餘額）、收購（Q3三筆共4.36億美元）、股息（殖利率0.831%）、還債（槓桿降0.5倍）。SBC前九月1.639億美元，以現價換算約37萬股，遠小於Q2單季回購的360萬股，淨股數下降。三項計分：收購增量報酬未揭露、無法判定；回購買入收益率以341美元對FY1共識EPS約6.5%，十年期公債殖利率事實表未涵蓋、無法判定；SBC淨稀釋為負，通過。","fact_refs":["f_kpi4_free_cash_flow_ocf_capex","f_kpi5_stock_based_compensation","f_dividend_yield_ttm","f_consensus_eps_fy1","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"收購金額與被收購事業獲利未揭露；Q3三筆小型收購管理層稱報酬很有吸引力，未量化"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q2回購均價約341美元，對FY1共識EPS 22.34美元的盈餘收益率約6.5%；十年期公債殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九月SBC 1.639億美元，以現價換算約37萬股；Q2單季回購360萬股，淨稀釋為負"}]},"governance":{"capital_returns":[{"item":"回購","value":"八個月累計約32億美元；Q2約12億美元、360萬股、均價約341美元；Q3暫停"},{"item":"收購","value":"上半年兩筆小型約5,000萬美元；Q3三筆（iPipeline、Procare、Strata的補強）共4.36億美元"},{"item":"處分收入","value":"Indicor儀器業務售予AMETEK稅後約12億美元；流量控制業務售予Xylem稅前約6億美元，預計Q4入帳"},{"item":"槓桿","value":"淨負債/EBITDA：Q2末3.4倍→Q3末2.9倍；35億美元循環額度動用13億美元"},{"item":"股息","value":"近12個月殖利率0.831%"},{"item":"可部署資本","value":"未來12個月逾60億美元"}]}}},"q5_valuation":{"verdict":"現價438.14美元要求未來五年調整後EPS年增約8%，且前瞻本益比守在18倍以上，才有約7%的年化報酬；EPS路徑可信，但倍數已超過前份的重定性目標，再擴張的空間不支撐追價，偏貴。","reasoning":"前瞻本益比19.61倍（FY1共識22.34美元），以FY2共識24.57美元計約17.8倍。PEG以FY1到FY3共識年化8.69%計約2.26。26週漲24.6%、RSI 80.65，動能過熱。五年歷史分位所需的估值歷史高低點事實表未涵蓋，分位留空。賣方：16位分析師平均目標約445.92美元（區間約350–550），評等9買9持有2賣（家數與16位不一致，來源本身有誤差），BMO於10月以持有、目標393美元；現價已在賣方均值附近，賣方均值不支持進一步上漲；全距550÷350約1.6倍，未達分歧過大。短期上檔8.4%＝一年後以FY2028共識26.39美元×18倍；中期上檔36.4%＝基準情境五年終端33.2美元×18倍。調整後與GAAP口徑落差大（Q3 GAAP EPS 4.88美元對調整後5.89美元），差額主要是收購無形資產攤銷，本檔與共識、指引皆用調整口徑，不構成爭點。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rsi14","f_week26_return_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_kpi3_adjusted_diluted_eps"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1調整後EPS）＋PEG","tier":"高品質垂直軟體收購平台","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比或目標價；終端倍數改以本檔現值19.6倍與前份引用的CSU約17.5倍對照，後者未於本包更新。"},"fwd_pe":19.61,"peg":2.26,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比19.61倍÷共識EPS年化成長8.69%＝PEG 2.26，高於2屬偏貴；倍數已高於前份重定性目標16倍；未判最貴一級，因共識EPS仍在上修（FY1+0.45%、FY2+0.74%）且FCF利潤率約31%，盈餘品質支撐目前倍數。","upside_short_pct":8.4,"upside_mid_pct":36.4,"denominator_disputed":false,"denominator_note":"分母為公司調整後EPS，排除收購無形資產攤銷；對連續收購者攤銷是真實成本，GAAP本益比遠高於調整口徑，但本檔的歷史對照、共識與指引全用同一調整口徑，比較一致，不把分母當爭點。"}}},"q6_how_wrong":{"verdict":"最可能看錯在三處：AI在任務層繞過工作流、收購報酬向資金成本收斂、價格已經提前反映重定性；價值陷阱風險中等。","reasoning":"三視角的反證與裁定寫在反證紀錄：AI替代與商譽減損屬論點失敗路徑，目前證據（毛留存90%中段、有機經常性營收8%）反駁但未排除；模型成本與收購倍數屬論點成功但股東經濟變差的路徑，部分採納；股價半年漲24.6%、前瞻本益比19.6倍屬價格已反映太多，採納並據此不追。管理層在Q2法說迴避了AI在2027年的變現金額與指引保守程度，Q3法說也只說2027年規劃下週才開始，AI已進入商業化階段，但訂單、採用、用量都還要證明。Neptune下半年展望由回到成長改為略低於先前展望，是本季唯一的展望改口。","fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_rsi14","f_ma_state","f_ma_w52"],"verdict_values":{"trap":{"verdict":"🟡","label":"AI替代與收購報酬未證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":22.34,"pe":19.61,"basis":"FY1（FY2026）共識調整後EPS，與終端倍數同為前瞻一年口徑"},"eps":{"bull":[25.0,27.6,30.5,33.7,37.2],"base":[24.57,26.39,28.5,30.8,33.2],"bear":[23.2,23.5,23.8,24.1,24.4]},"pe":{"bull":24,"base":18,"bear":13},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.83,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":7},"max_dd":{"lo":-42,"hi":-28,"basis":"三個依據：2026年初軟體股AI拋售時股價自高點跌近40%（第三方報導），顯示同類疑慮重燃時倍數壓縮的速度；空頭情境終點約317美元（24.4×13倍）較現價約−28%；現價高於52週均線379.55約15%、RSI 80.65，動能回吐會先跌掉這一段。取−28%到−42%。","trigger_time":null},"basis":{"bull":"AI加值方案在2027–2028年轉成可計量訂閱收入，有機成長升到7%–8%，60億美元收購以合理報酬部署，EPS年增約11%；倍數24倍＝市場重新給予高品質複利溢價。","base":"2027–2028年照共識（24.57、26.39美元），之後有機約6%加收購與回購，EPS年增約8%；倍數小降到18倍，介於CSU約17.5倍（前份資料）與本檔現值19.6倍之間。","bear":"AI在任務層壓縮定價、模型成本侵蝕毛利，Neptune與Deltek疲弱延續，收購報酬下滑，EPS五年僅年增約2%；倍數降到13倍，對應成長熄火到個位數低段的估值。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"10-K風險因子明列可能出現新競爭者、產品線可能受包括AI在內的新技術威脅；若替代技術出現，約213億美元、占總資產約62%的商譽可能減損。","assumption":"工作流嵌入與專有資料讓AI成為公司自己的加值層，而不是繞過它的替代品。","consequence":"五年後虧50%最可能的故事：通用代理在計費、保單處理等任務層以低價切入，留存先跌破90%，市場把ROP重新定為衰退中的收購平台，倍數跌到12–13倍、EPS停滯，同時認列商譽減損。","ruling":"反駁但不排除：企業軟體毛留存連續多季90%中段、Q3有機經常性營收8%、21家軟體事業中17到18家已上市代理產品且管理層稱無明顯失敗，現有數字與替代故事方向相反；但留存是落後指標，任務層替代要一到兩年才會反映。","watch":"企業軟體毛留存跌破90%；兩軟體部門有機經常性營收連2季低於5%（季度法說）。","evidence_refs":["substitute_technology#0","competitive_share_entrants#1"]},{"view":"論點成功但股東經濟變差","evidence":"10-K揭露AI產品依賴OpenAI、Anthropic、Google、Microsoft，供應商漲價未必能轉嫁；AI代理產品2026年不構成重大營收，變現是2027年議題，曾有第三方因AI耐久性疑慮將合理價由694下調至550美元（該頁面日期與股價欄位不一致，只採其敘述部分，與Q2法說稱AI今年不會形成實質營收一致）。","assumption":"AI功能能以加購或點數方式收費，毛利維持在軟體水準；收購能在合理倍數成交。","consequence":"AI產品成功上市、留存守住，但收入只是把原有授權費換成點數，模型成本吃掉增量毛利；加上60億美元收購在私募回流後以高倍數成交，每股自由現金流成長掉到5%以下。","ruling":"部分採納：管理層稱代理工具毛利與軟體毛利相當、所有產品都有模型路由可切換，但Q2法說也說AI工具支出年化約為1月的3倍；毛利率是可結算的數字，TTM 69.53%尚未受損，先以門檻監測。","watch":"TTM毛利率跌破68%；2027年指引是否揭露AI收入或訂單占比；大型收購的成交倍數。","evidence_refs":["substitute_technology#1","supply_demand_durability#1"]},{"view":"價格已反映太多","evidence":"26週漲24.6%、RSI 80.65；前瞻本益比19.61倍已高於前份重定性目標16倍；賣方平均目標約445.92美元，與現價相當；2026年初股價曾因AI拋售自高點跌近40%。","assumption":"重定性已大致完成，後續報酬主要靠EPS成長。","consequence":"即使論點全部成立，五年基準報酬約年化7%，低於持有高品質複利股的期望；若AI疑慮再起，倍數回到前份的15–16倍即跌20%以上。","ruling":"採納：現價不追，等價格回到約17倍前瞻本益比附近再分批。","watch":"前瞻本益比回到17倍以下（約380美元），或FY2027共識上修使現價對應倍數下降。","evidence_refs":["substitute_technology#2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 355.94 → 本次 438.14（+23.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=355.94","side_b":"本次 price_at_dd=438.14","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 355.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 355.94 美元：Bull 價 886、Bear 價 270，五年期望值 +70.0%，基準年化 11.5%，不對稱比 6.4","side_b":"本次情境、股價仍用 355.94 美元：Bull 價 892.8、Bear 價 317.2，五年期望值 +68.9%，基準年化 10.9%，不對稱比 13.86","ruling":"先換情境、股價不動：五年期望值少 1.1 個百分點，基準年化少 0.6 個百分點。不對稱比由 6.4 變為 13.86。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 355.94 美元：五年期望值 +68.9%，基準年化 10.9%，不對稱比 13.86","side_b":"本次情境、股價 438.14 美元：五年期望值 +37.2%，基準年化 6.4%，不對稱比 3.76","ruling":"再換股價、情境不動：起點價上漲 23.1%，五年期望值少 31.7 個百分點，基準年化少 4.5 個百分點，不對稱比由 13.86 降到 3.76。合計五年期望值比前份少 32.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AI是擴大市場還是替代威脅","cause":null,"prior_field":null,"side_a":"管理層（2026-10-22 Q3法說，Neil Hunn）：AI建立在領域專長、嵌入工作流、專有資料與客戶信任上，能擴大可服務市場並拿到更多創造的價值；CentralReach約75%、Aderant約25%的訂單與AI相關。","side_b":"10-K風險因子：新競爭者與AI可能削弱產品線價值、AI能力可能快速商品化；第三方因AI耐久性疑慮下調合理價。","ruling":"方向相反，暫採管理層側：依據是可結算的數字（毛留存90%中段、有機經常性營收由7%升到8%、TTM毛利率69.53%）目前都與替代故事相反；但這些是落後指標，裁定有效到2027年第二季，屆時要看到AI訂單擴散到兩家以上旗艦。現在就買的最強論證：全年EPS指引三度上調、每股自由現金流兩位數成長、私募賣方估值鬆動讓60億美元可部署資本有機會以較好價格成交，等回落可能錯過；本檔仍選等，因為這些利多已反映在19.6倍。","evidence_level":"公司法說與10-K（一手）對第三方評論","settle_metric":"企業軟體毛留存；旗艦AI訂單占比","if_then":["若2027年上半年毛留存維持90%以上且兩家以上旗艦揭露AI訂單占比≥25%→即使價格未回落也以三分之一部位分批買進","若毛留存跌破90%或有機經常性營收連2季低於5%→已持有者減碼至半倉並凍結加碼"],"evidence_refs":["competitive_share_entrants#1","supply_demand_durability#1"]},{"axis":"Neptune下半年展望改口","cause":null,"prior_field":null,"side_a":"2026-07-23 Q2法說，Neil Hunn：表計業務預計下半年回到成長。","side_b":"2026-10-22 Q3法說，Neil Hunn：下半年營收改為略低於先前溫和成長的展望，機械式表計組合偏高、可能延續到Q4，稱屬暫時性；Jason Conley稱靜態表計管線仍強，是專案遞延。","ruling":"可調和（程度差異）：出貨數量接近預期，落差在組合與大型專案遞延；暫時性歸因不採信也不否定，標未證、監測；若2027年上半年TEP有機成長仍≤0，歸因證偽，下修TEP成長假設。","evidence_level":"公司法說（一手）","settle_metric":"TEP分部有機成長與EBITDA利潤率","if_then":["若2027年Q1、Q2 TEP有機成長皆≤0→空頭情境機率由25%調到30%並停止加碼"],"evidence_refs":["end_markets#3"]},{"axis":"關稅與供應鏈","cause":null,"prior_field":null,"side_a":"10-K：銷售受出口管制、制裁與新增或報復性關稅影響；第三方彙整另提單一來源供應商與少數雲端平台依賴。","side_b":"10-K：美國以外營收13%；TD Cowen稱關稅風險可忽略（美國曝險約85%）。","ruling":"可調和：風險條款為制式揭露、未附金額，第三方彙整未附申報原文；實際曝險集中在TEP硬體（Q2法說提到Neptune青銅錠投入成本通膨），軟體幾乎不受影響。不預測關稅，改用吸收失敗門檻：TEP EBITDA利潤率跌破33%（Q3 34.3%）視為成本轉嫁失敗。","evidence_level":"10-K（一手）對賣方與第三方彙整","settle_metric":"TEP EBITDA利潤率","if_then":["若TEP EBITDA利潤率連2季低於33%→下調TEP成長與利潤率假設、空頭情境機率加5點"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","reg_tariff_export#1","reg_tariff_export#2"]},{"axis":"產業態勢：競爭／結構／其他","cause":null,"prior_field":null,"side_a":"競爭面：AI原生方案與通用代理可能在任務層切入（10-K風險因子）。","side_b":"結構面：毛留存90%中段、Deltek地端停止支援推動上雲加價、私募賣方估值鬆動改善收購環境（Q2、Q3法說）。","ruling":"雙向拉鋸：競爭惡化尚未出現在數字，結構性轉好有一手證據；其他結構變數中，反壟斷（PowerPlan訴訟已和解）與通路（直銷為主未見轉變）都屬靜態。","evidence_level":"公司法說與10-K（一手）","settle_metric":"毛留存；有機經常性營收","if_then":["若出現旗艦垂直公開失去大型客戶給AI原生對手→改判競爭惡化中，護城河方向下修並停止買進"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"前份漂移：股價帶動的欄位","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份（2026-07-10）：股價355.94美元、估值中性、進場；最大回撤−42%、多空機率各25%。","side_b":"本次：股價438.14美元（約+23%）、前瞻本益比19.61倍、估值偏貴、改為等價格回落；最大回撤範圍−28%到−42%、多空機率維持各25%。","ruling":"基本面在這三個多月轉好（全年EPS指引再上調、有機成長7%），估值結論變貴完全來自股價上漲；機率不動是因為新證據兩面都有（留存與經常性營收轉好、Neptune改口），互相抵銷；回撤下緣不變，上緣改以空頭情境終點推得。","evidence_level":"價格與共識資料","settle_metric":"前瞻本益比","if_then":["若股價回落至約380美元且毛留存未破90%→恢復分批買進"],"evidence_refs":[]},{"axis":"前份漂移：基本面欄位維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質評級B、價值陷阱中等、護城河方向不變、五年後跑道中等、品質複利成長、未列循環位置。","side_b":"本次：六欄皆維持。","ruling":"Q3新證據（有機經常性營收8%、毛留存90%中段、17到18家軟體事業已上市AI代理產品、Neptune改口）正負互抵，不足以改變任何一欄；循環位置仍不適用，主體是經常性軟體收入。","evidence_level":"公司法說（一手）","settle_metric":"毛留存；有機經常性營收","if_then":["若2027年上半年兩家以上旗艦AI訂單占比≥25%→跑道判斷上修一級"],"evidence_refs":[]},{"axis":"加碼觸發條件改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","side_b":"回落至約380美元（約17倍FY1共識）且毛留存維持90%以上→分批買進；或2027年指引≥24.57美元且兩家以上旗艦AI訂單占比≥25%→分批加碼。","ruling":"前份加碼條件中連2季有機成長≥5%已達成（Q2 5%、Q3 7%），但Deltek、DAT回穩管理層仍在觀察；同時股價已漲約23%、本益比超過前份目標，原條件會在偏貴價位觸發加碼，因此改為價格錨加證據錨。站回104週均線一條刪除，現價438.14低於104週均線459.77，在估值偏貴時用均線觸發加碼不合理。","evidence_level":"公司法說與價格資料","settle_metric":"股價；毛留存；2027年指引","if_then":["若2027年指引中點低於24.57美元→加碼條件只保留價格錨並把價位下移至約340美元"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼或清倉的數字門檻。","side_b":"本次設定：企業軟體毛留存跌破90%、兩軟體部門有機經常性營收連2季<5%、淨負債/EBITDA>3.5倍、TTM毛利率<68%；任一發生即減碼至半倉，毛留存跌破90%且有機經常性營收連2季<4%即清倉。","ruling":"前份只有假設與風險的漂移條件，沒有落成可執行的減碼、清倉數字，本次補上。","evidence_level":"方法調整","settle_metric":"四項門檻指標","if_then":["若四項中任一項觸發→減碼至半倉並凍結加碼"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）。","side_b":"本次Single Thing：未來12–24個月以高倍數完成單筆逾50億美元、目標有機成長低於ROP母體的大型收購。","ruling":"前份未指定；本次以數學上最大的單一離散事件指定：收購是每股盈餘複利的主要引擎，單筆約相當兩年自由現金流，錯一筆會同時拉低增量報酬並推高槓桿，且無法逆轉。","evidence_level":"方法調整","settle_metric":"8-K重大收購公告的金額與倍數","if_then":["若宣布此類收購→當季減碼至半倉，首年每股自由現金流成長仍≥8%才回補"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"企業軟體毛留存與有機經常性營收是工作流鎖定的結算數字","type":"假設驗證","maps_to":"H1","metric":"企業軟體毛留存；兩軟體部門有機經常性營收年增","threshold":"毛留存≥90%且有機經常性營收≥6%","action":"兩項守住→論點維持；有機經常性營收連2季<5%→減碼至半倉","source_freq":"季度法說","date":null},{"n":2,"text":"AI變現從訂單走進營收","type":"假設驗證","maps_to":"H2","metric":"旗艦AI相關訂單占比；AI收入揭露","threshold":"2027年中前至少兩家旗艦AI訂單占比≥25%","action":"達成→即使價格未回落也以三分之一部位分批買進；2027年底仍無量化揭露→不加碼","source_freq":"季度法說","date":"2027-07"},{"n":3,"text":"模型成本是否被上游拿走","type":"風險","maps_to":"R2","metric":"TTM毛利率","threshold":"<68%（TTM 69.53%）","action":"減碼至半倉並凍結加碼","source_freq":"季報","date":null,"evidence_refs":["substitute_technology#1"]},{"n":4,"text":"Neptune與Deltek等循環性業務拖累","type":"風險","maps_to":"R3","metric":"TEP分部有機成長；TEP EBITDA利潤率","threshold":"有機成長連2季≤0或利潤率<33%","action":"停止加碼，空頭情境機率調至30%","source_freq":"季度法說","date":null,"evidence_refs":["end_markets#3"]},{"n":5,"text":"大型收購的倍數與目標成長","type":"Single Thing","maps_to":"Single Thing","metric":"單筆收購金額、成交倍數、目標有機成長","threshold":"單筆>50億美元且目標有機成長低於母體約6%","action":"宣布當季減碼至半倉；首年每股自由現金流成長仍≥8%才回補","source_freq":"8-K與季度法說","date":null},{"n":6,"text":"價格回落到合理區","type":"估值rearm","maps_to":"H3","metric":"股價；前瞻本益比","threshold":"≤380美元（約17倍FY1共識）且毛留存≥90%","action":"首批三分之一部位","source_freq":"每日股價＋季度法說","date":null},{"n":7,"text":"倍數過度擴張時收割","type":"減碼","maps_to":"H3","metric":"前瞻本益比","threshold":"≥24倍且共識EPS未同步上修","action":"減碼三分之一","source_freq":"每日","date":null},{"n":8,"text":"工作流鎖定失守","type":"清倉","maps_to":"H1","metric":"企業軟體毛留存＋有機經常性營收","threshold":"毛留存<90%且有機經常性營收連2季<4%","action":"清倉","source_freq":"季度法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":9,"text":"Q4財報與2027年指引","type":"複審日期","maps_to":"H1","metric":"2027年調整後EPS指引","threshold":"指引中點≥24.57美元","action":"重跑完整研究","source_freq":"年度","date":"2027-01"}],"kill_metrics":[{"metric":"企業軟體毛留存率","bear_threshold":"跌破90%（目前90%中段）","window":"任一季","source":"季度法說","last_status":"ok"},{"metric":"兩軟體部門有機經常性營收年增","bear_threshold":"連2季<5%（Q3約8%）","window":"連續2季","source":"季度法說","last_status":"ok"},{"metric":"淨負債/EBITDA","bear_threshold":">3.5倍（Q3末2.9倍）","window":"任一季末","source":"季度法說／10-Q","last_status":"ok"},{"metric":"TTM毛利率","bear_threshold":"<68%（TTM 69.53%）","window":"TTM滾動","source":"10-Q／季報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"回落至約380美元（約17倍FY1共識）且毛留存維持90%以上→分批買進；或2027年指引≥24.57美元且兩家以上旗艦AI訂單占比≥25%","exec_line":"現價不追；回落約380美元首批三分之一，340美元以下且毛留存未損再加三分之一，2027年指引不低於24.57美元後補足；毛留存跌破90%即停止買進。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回落至約380美元（接近52週均線379.55、約17倍FY1共識）且企業軟體毛留存未破90%；或2027年指引不低於共識24.57美元且兩家以上旗艦AI訂單占比≥25%時以較高價分批。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=24.6, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」","row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"垂直軟體工作流鎖定在AI代理普及後仍成立，AI成為公司自己的加值層而非替代品","2y":"企業軟體毛留存維持90%中段、兩軟體部門有機經常性營收≥6%","5y":"毛留存≥90%、核心旗艦未被AI原生對手系統性搶客","10y":null,"threshold":"毛留存≥90%；有機經常性營收≥6%","source":"季度法說（毛留存、有機經常性營收）","drift_rule":"有機經常性營收連2季<5%→削弱；毛留存跌破90%→反轉"},{"id":"H2","text":"AI代理產品在2027–2028年轉成可計量的增量訂閱收入，毛利維持在軟體水準","2y":"至少兩家旗艦AI訂單占比≥25%，TTM毛利率≥68%","5y":null,"10y":null,"threshold":"旗艦AI訂單占比≥25%；TTM毛利率≥68%","source":"季度法說（AI訂單占比）＋季報毛利率","drift_rule":"2027年底仍無AI收入或訂單量化揭露→削弱；TTM毛利率連2季<68%→反轉"},{"id":"H3","text":"自由現金流再部署（收購為主、回購為輔）維持每股自由現金流約兩位數成長，槓桿不失控","2y":null,"5y":"每股自由現金流年增≥8%、淨負債/EBITDA≤3.5倍、無重大商譽減損","10y":null,"threshold":"每股自由現金流年增≥8%；淨負債/EBITDA≤3.5倍","source":"公司法說與年報","drift_rule":"連續兩個年度每股自由現金流增速<6%→削弱；認列重大商譽減損→反轉"}],"R":[{"id":"R1","text":"AI原生垂直方案或通用代理在任務層繞過工作流，旗艦垂直留存或定價受壓，商譽面臨減損","h_ref":"H1","clock":"🔥","threshold":"企業軟體毛留存跌破90%或有機經常性營收連2季<5%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"id":"R2","text":"AI變現延後到2027年後、第三方模型成本吃掉增量毛利","h_ref":"H2","clock":"🔥","threshold":"TTM毛利率<68%或2027年中前仍無AI收入量化","evidence_refs":["supply_demand_durability#1","substitute_technology#1"]},{"id":"R3","text":"循環性業務拖累：Neptune表計組合偏機械式、Deltek政府承包市場不確定、DAT貨量未回","h_ref":"H1","clock":"⚡","threshold":"TEP分部有機成長連2季≤0或EBITDA利潤率<33%","evidence_refs":["end_markets#3"]},{"id":"R4","text":"私募買方回流抬高收購倍數，收購增量報酬向資金成本收斂、槓桿回升","h_ref":"H3","clock":"🐢","threshold":"淨負債/EBITDA>3.5倍，或單年收購逾40億美元且未揭露報酬","evidence_refs":[]}],"single_thing":{"description":"未來12–24個月以高倍數完成單筆逾50億美元、目標有機成長低於ROP母體（約6%）的大型收購","why_fatal":"收購是每股盈餘複利的主要引擎，單筆約相當兩年自由現金流（以營收年增8%、自由現金流約營收30%推算）；高價買進低成長資產會同時壓低增量報酬、推高槓桿並鎖住之後兩三年的部署能力，而且無法逆轉。","if_happens":"宣布當季減碼至半倉；首年每股自由現金流成長仍≥8%且淨負債/EBITDA回到3.5倍以下才回補。","how_monitor":"8-K重大收購公告（成交金額、倍數）；法說揭露的目標成長與綜效；淨負債/EBITDA。","probability":"約15%：管理層稱未來12個月可部署逾60億美元、對2027年收購審慎樂觀，大型交易宣布機率不低；但要同時出現高倍數與低成長目標才算，且管理層重申只買贏家。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.83,"peg_fy2":2.05,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":22.34,"FY2027E":24.57,"FY2028E":26.39},"fy_end_month":12,"eps_basis":"公司調整後稀釋EPS（排除收購無形資產攤銷等）；FY2026E–FY2028E為Koyfin共識，家數事實表未涵蓋；FY2025A調整後實際值事實表未涵蓋（年度表只有GAAP 14.20美元，口徑不同不可代入）"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026財報與2027年全年指引","impact":"高","watch":"2027年調整後EPS指引中點對共識24.57美元；是否量化AI訂單或收入"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Indicor流量控制業務售予Xylem，稅前約6億美元入帳（待監管許可）","impact":"低","watch":"入帳時點與用途（收購或回購）"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"未來12個月逾60億美元可部署資本的收購動向","impact":"高","watch":"單筆金額、成交倍數、目標有機成長"},{"date":"2028-03","date_precision":"quarter","type":"product","event":"Deltek Costpoint地端版停止支援（2028年第一季）","impact":"中","watch":"上雲轉換率與授權收入轉為經常性收入的過渡缺口"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
