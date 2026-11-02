你是 DD 管線 v20 的判斷層閘（gate），標的 SOFI（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap_total_net_revenue`（q1_business）｜GAAP total net revenue＝1385.1 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（SEC 8-K）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：adjusted net revenue 1,371.1m vs 共識約 1,260m（來源：tikr.com 報導，媒體轉述，未經 IR 稿佐證）
- `f_kpi1_adjusted_net_revenue`（q1_business）｜Adjusted net revenue＝1371.1 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：共識約 1,260m（tikr.com，媒體轉述）
- `f_kpi2_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA／利益率（Non-GAAP 獲利口徑；SoFi 為銀行控股公司，不揭露營業利益）＝469.8 USD m（利益率 34%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：新聞稿稱優於 FactSet 共識但未列數字
- `f_kpi3_gaap_net_income_sofi_gaa`（q1_business）｜GAAP net income（SoFi 無 GAAP 營業利益，以稅前／淨利替代）＝241.0 USD m（淨利率 17%；稅前 317.8m）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：GAAP／調整後 diluted EPS 0.18 vs 共識 0.17（tikr.com）
- `f_kpi5_fy2026_guidance`（q1_business）｜FY2026 guidance（上修）＝5040 USD m adjusted net revenue（約 +40% YoY）；adjusted EBITDA 約 1,660m（33%）；淨利約 840m（17%）；adjusted EPS 約 0.61；會員成長至少 30%｜期間與口徑：Q3 FY2026（公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-27））
  - 註記：新聞稿稱高於共識；先前指引營收 4.75–4.85B（tikr.com）
- `f_kpi6_fy2027_outlook`（q1_business）｜FY2027 outlook（首度提供）＝6400 USD m adjusted net revenue（約 +27%）；adjusted EBITDA 約 2,240m（35%）；淨利約 1,280m（20%）；adjusted EPS 約 0.90｜期間與口徑：Q3 FY2026（公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（公告於 2026-10-27））
  - 註記：consensus_revision 快照 FY2 EPS 0.89（dd_numbers_extra.py）
- `f_kpi7_members`（q1_business）｜Members＝17.07 百萬｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：n/a
- `f_kpi8_total_products`（q1_business）｜Total products＝26.67 百萬｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：n/a
- `f_kpi9_tangible_book_value_rotc`（q1_business）｜Tangible book value／ROTCE＝9705 USD m（每股 7.48；ROTCE 約 10%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：n/a
- `f_peer_sofi_fcf_margin_pct`（q2_moat）｜SOFI FCF 利潤率＝-222.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SOFI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cof_fcf_margin_pct`（q2_moat）｜COF FCF 利潤率＝45.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COF.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ally_fcf_margin_pct`（q2_moat）｜ALLY FCF 利潤率＝14.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALLY.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hood_operating_margin_pct`（q2_moat）｜HOOD 營業利益率＝45.65 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝0.61 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝0.89 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.14 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5054.63 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6393.89 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_share_based_expense_sbc`（q4_capital）｜Share-based expense（SBC）＝70.9 USD m（占調整後淨收入約 5.2%，占 adjusted EBITDA 約 15.1%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 EX-99.1；占比為本表自算（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：n/a
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1296.62 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝23691.94 USD m｜期間與口徑：2026-11-03／市值 22522.11 ＋ 淨負債 1169.83｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝17.38 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝28.48 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 0.61，分子＝快照價 17.37｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.58 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／2 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝31.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝7.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.67 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 0.6 → 0.61（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（0.89 → 0.89）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 16.9 / W52 19.46 / W104 18.81 / W250 12.09 / W250 13週斜率 0.21%」
- `f_ma_w104`（q5_valuation）｜104 週均線＝18.81 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_rsi14`（q5_valuation）｜RSI(14)＝60.75｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝7.16 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述各業務面對多元競爭者：優質貸款市場高度分散、有銀行／信用合作社／科技型放款人；存款端有更大的銀行與擁有大量客群的科技／零售公司；科技平台端有大型機構可能壓價。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：新進入者與現有業者可能壓低定價，進而影響市占；公司未揭露具體市占數字。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-17）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：SoFi 10-K（FY2025）揭露其受 2019 年 FTC Consent Order 約束，禁止在無可靠證據下向消費者誤述節省金額；並稱可能受政府機關審查、調查與裁罰。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美中、歐盟等貿易與國際投資政策變動近年已對金融市場造成負面影響；貿易戰升級可能引發關稅等報復措施，屬間接（市場／總經）暴露，非產品或供應鏈直接暴露。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：貿易限制、制裁可能限制特定市場的全球匯款服務。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年 4 月 Morgan Stanley 分析師認為關稅影響對 SoFi 難以忽視（總經／消費者信貸管道），並下調目標價；為分析師意見，非公司量化。
  - 來源：TipRanks／Globe and Mail：Morgan Stanley analyst says tariffs impact difficult to ignore for SoFi（as_of 2025-04-08）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因子提及依賴第三方雲端供應商（如 AWS）與 co-location 設施，及供應商可能再外包，未指名單一資料中心供應商
  - 來源：SoFi Technologies Form 10-K FY2024（as_of 2025-02-28）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q3 2026 Technology Platform 營收年減 24% 至 $87.4M（大客戶 2025 年完成遷出）；排除該影響年增 18%
  - 來源：SoFi 8-K Q3 2026 earnings release (SEC)（as_of 2026-10-27）｜affects：thesis.R、moat_trend
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：Lending 佔調整後淨營收 59%（去年同期 51%），收入結構向貸款集中；TD Cowen 分析師質疑個人貸款高速成長可持續性
  - 來源：SoFi Q3 2026 earnings call (Zacks)（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Galileo 一個重要客戶近期轉向競爭對手，且客戶集中。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-17）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子承認若未維持或改善技術與流程，解決方案競爭力會下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-17）｜affects：thesis.R
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：Technology Platform 分部 Q1 2026 營收年減 27%，公司歸因於大型客戶於 2025 年底前完全移出平台；Q2 營收 $84.5M 年減 23%。
  - 來源：SoFi Form 10-Q Q1 2026 / Q2 2026 earnings release（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Q1 後目標價下修：Truist $17（原 $20，Hold）、Morgan Stanley $16（原 $18，Sell）、Citi $30（原 $37，Buy）、Mizuho $29（原 $38）、Stephens $25（原 $26）
  - 來源：搜尋摘要（Truist/Morgan Stanley/Citi/Mizuho/Stephens 動態）（as_of 2026-05-12）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-03-17 Muddy Waters 發布放空報告質疑 SoFi 貸款會計與公允價值評價；SoFi 同日回應稱報告不實並考慮法律行動；CEO Noto 買進 28,900 股。
  - 來源：SoFi 新聞稿 SoFi Responds to Inaccurate Short Seller Report（as_of 2026-03-17）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-05-04 律所 Block & Leviton 公告調查 SoFi 是否違反證券法（律所徵求，非法院起訴）；搜尋未見已提起證券集體訴訟。
  - 來源：Block & Leviton 新聞稿（Newsfile）（as_of 2026-05-04）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#0`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：TransUnion Q2 2026：無擔保個人貸款借款人層級 60+ DPD 為 3.81%，高於去年同期 3.37%（產業層面信用略轉弱）
  - 來源：TransUnion Q2 2026 data via search summary (consumer credit trends)（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `financial_capital_credit_cycle#1`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：TransUnion Q2 2026：消費者層級 90+ DPD 升至 2.26%，主因次級人口增加
  - 來源：TransUnion Q2 2026 consumer credit data via search summary（as_of 2026-08-01）｜affects：thesis.R
- `financial_regulatory_capital_rules#0`（financial_regulatory_capital_rules｜方向 -｜狀態 ok）：SoFi 合併 CET1 比率 2026-09-30 為 16.9%（要求下限 7.0%，含 2.5% 資本保全緩衝），自 2025 年底 22.8%、2026-06-30 18.7% 持續下降；搜尋未見最低要求本身在 2026 有變動
  - 來源：SoFi Q3 2026 earnings release 8-K (SEC)（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-05-04 律所 Block & Leviton 公告調查潛在證券法違反（連結 3/17 Muddy Waters 報告與 4/29 財報後跌逾 13%）；未見已提起證券集體訴訟。
  - 來源：Block & Leviton 新聞稿（Newsfile）（as_of 2026-05-04）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":46.0,"bear_5y_price":8.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":71.2,"ev5y_pct":57.0,"irr_base_pct":11.3,"asym_ratio":2.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":0.61,"pe":28.49,"basis":"起點用 FY2026E 共識 EPS 0.61（Koyfin，與公司 2026 調整後 EPS 財測相同）；終端倍數同樣套在終端年當年度 EPS 上，口徑一致"},"eps":{"bull":[0.93,1.22,1.55,1.92,2.3],"base":[0.89,1.12,1.36,1.56,1.75],"bear":[0.62,0.35,0.5,0.65,0.8]},"pe":{"bull":20,"base":17,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SOFI_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY2026 調整後淨營收財測上調（原話："$4.75 billion to $4.85 billion, which equates to"）
- 2026-07-29｜CFO｜guidance：FY2026 調整後 EBITDA 財測維持約 $1.6B（原話："to deliver adjusted EBITDA of approximately $1.6 billion"）
- 2026-07-29｜CFO｜guidance：EPS 財測內含 22% 稅率（原話："Our EPS guidance now includes a tax rate of 22%"）
- 2026-07-29｜CFO｜margin：以原先中位十幾% 稅率計算 EPS 為 $0.65 而非 $0.60（原話："would have actually been $0.65 in EPS"）
- 2026-07-29｜CFO｜guidance：利率假設改為與 Fed funds futures 一致，2026 升息 1–2 次（原為降息 2 次）（原話："consistent with the Fed funds futures and 1 to 2"）
- 2026-07-29｜CFO｜guidance：NIM 預期維持 5% 以上（原話："a healthy net interest margin above 5%"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EPS 受稅率高於預期的影響（原話："due to higher-than-expected tax rate"）
- 2026-07-29｜CFO｜margin：管理層定義：現金營收的口徑（原話："Cash is defined and accounted for the same universally"）
- 2026-07-29｜CEO｜margin：Q2 增量 EBITDA 利潤率 31%（原話："Our incremental EBITDA margin was 31%"）
- 2026-07-29｜CFO｜margin：Tech Platform 分部貢獻利潤 $12M（原話："Contribution profit was $12 million"）
- 2026-07-29｜CFO｜margin：核心個人貸款風險調整後利差約 6.1%（原話："our core personal loan product generated a roughly 6.1%"）
- 2026-07-29｜CFO｜margin：ROTCE 的拆解口徑：淨利率 ×營收/權益（原話："ROTCE is the product of net income margin"）
- 2026-07-29｜CFO｜margin：增量淨利率已約 30%（營收成長逾 35%）（原話："has already been approximately 30% while growing revenue"）
- 2026-07-29｜CFO｜margin：管理層稱達 25–30% 淨利率路徑「highly probable」（原話："we believe the path to a 25% to 30% net income margin"）
- 2026-07-29｜CFO｜margin：個人貸款淨沖銷率（不含逾期貸款出售）（原話："estimated all-in annualized net charge-off rate was 3.7%"）
- 2026-07-29｜CFO｜risk：個人貸款公允價值 mark 較上季下降 71bp（原話："our personal loans were marked at 104.7%"）
- 2026-07-29｜CEO｜risk：房貸買房與再融資市場仍疲弱（原話："as purchase and refinance remain muted in"）
- 2026-07-29｜CEO｜commitment：Noto 設定 SoFi Plus 一年後 100 萬付費會員目標（原話："I'd be disappointed if we are not at 1 million SoFi Plus"）
- 2026-07-29｜CFO｜commitment：長期 ROTCE 目標 20–30%（原話："we are on a path to generating returns on"）
- 2026-07-29｜CEO｜commitment：Financial Services 與 Tech Platform 營收占比未來超過 50%（原話："to be more than 50% of our revenue"）
- 2026-07-29｜CFO｜capital_allocation：過剩資本中期內將讓風險資本比率回落至低到中十幾%（原話："normalize toward the low to mid-teens"）
- 2026-07-29｜CFO｜capital_allocation：現行營運計畫下不需增資（原話："comfortably within our target capital range"）
- 2026-07-29｜CFO｜capital_allocation：LPB 與資本消耗：財測期自行供資（原話："we're self-funded through our guidance period"）
- 2026-07-29｜CEO｜capital_allocation：資產負債表與 LPB 並行以取得未來數季 NII 能見度（原話："next 6 to 8 quarters"）
- 2026-07-29｜CEO｜capital_allocation：資產負債表放貸使 2027 營收能見度高（原話："we have very strong visibility into our revenue for 2027"）
- 2026-07-29｜CEO｜capital_allocation：累計現金 NII 對非現金溢價的倍數（原話："is 2.7x the cumulative noncash premium on our balance sheet"）
- 2026-07-29｜CFO｜guidance：EBITDA 未上調的理由：多餘營收用於投資（原話："just too many large attractive growth areas"）
- 2026-07-29｜CEO｜guidance：不想為 EPS/EBITDA 過度最佳化（原話："we don't want to over-optimize for the actual EPS"）
- 2026-07-29｜CEO｜guidance：若利率不升，底線有上行空間（原話："we probably have upside to the bottom line"）
- 2026-07-29｜CEO｜commitment：今年推出多項原 2026 計畫外的新業務（原話："things that were never in our 2026 plan"）
- 2026-07-29｜CEO｜competition：非貸款業務競爭環境（原話："Outside the loan business, the competition is very benign"）
- 2026-07-29｜CEO｜competition：貸款產品競爭較強（原話："The lending products are definitely more competitive"）
- 2026-07-29｜CEO｜competition：SMB 放貸對手利率偏高，SoFi 稱可低約 10 點（原話："most SMB lenders are charging exorbitant rates of over 30%"）
- 2026-07-29｜CEO｜customer：會員新增 110 萬（原話："We added a record 1.1 million new members in"）
- 2026-07-29｜CEO｜customer：新產品中既有會員交叉購買比例升至 51%（原話："accelerate with 51% of new products opened by"）
- 2026-07-29｜CEO｜customer：CAC 大致維持不變（原話："over 40% growth in products and really keeping CAC constant"）
- 2026-07-29｜CEO｜customer：SoFi Plus 付費訂閱戶逾 20 萬（原話："we surpassed 200,000 paid subscribers"）
- 2026-07-29｜CEO｜product：SoFi Coach 於 6 月推出（原話："SoFi Coach, which launched in June"）
- 2026-07-29｜CEO｜product：信用卡：稱已摸索出有效獲客方式（原話："We think we've cracked the code on efficiently"）
- 2026-07-29｜CEO｜product：SoFi Money 開始遷移到 STS 自建核心（原話："begun onboarding SoFi Money to our new"）
- 2026-07-29｜CEO｜product：併購 Peach Finance（原話："During the quarter, we acquired Peach"）
- 2026-07-29｜CEO｜product：Mastercard 卡將以 SoFi USD 結算（原話："will begin settling in SoFi USD with Mastercard"）
- 2026-07-29｜CFO｜product：LPB 新增 Basepoint 3 年 $3B SMB 協議（原話："a 3-year $3 billion agreement with Basepoint Capital"）
- 2026-07-29｜CFO｜product：LPB 需求逾 SoFi 願意滿足的量，合約承諾皆已履行（原話："we did fill all demand from our contractual commitments"）
- 2026-07-29｜CEO｜capital_allocation：結語：管理層自述買進股票（原話："when, not if the market can connect the dots"）

### 問答異常語氣（迴避／改口／保留）
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Dolev（Mizuho）：為何不上調 EBITDA？｜答法：未給 EBITDA 上調數字，改談營收上調 $100–200M 與投資新成長領域；Noto 補充稱財測內有緩衝
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Peterson（Needham）：LPB 連兩季未滿足上調需求，個人貸款面是否持續？｜答法：未回答未來個人貸款 LPB 量是否持續受限，改談其他資產類別成長與資本自給
- SOFI_Q2_2026_Earnings_Call_20260729.md｜問：Coad（Truist）：超額資本消耗的節奏｜答法：Noto 轉交 CFO；CFO 重申 18.8% 與低到中十幾%目標，未給時程或消耗速度

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 7 | 3 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 4 | 5 |
| financial_capital_credit_cycle | found | 6 | 3 |
| financial_regulatory_capital_rules | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資本輕費收引擎撐起報酬率目標的分子與分母：Financial Services ＋ Technology Platform 由調整後淨營收的 45.7% 破 50%，且該增量不消耗權益，使營收／有形權益比由 0.503 轉向 1.00"},{"id":"H2","text":"消費飛輪續轉且獲客成本不惡化：交叉購買佔新開產品比續升、每會員產品數續升、獲客成本持平，使追加產品的邊際獲客成本維持趨近零"},{"id":"H3","text":"信用穿越一次完整循環而不破承保容忍上限：無擔保消費簿在家庭債務創紀錄、聯準會轉為升息的環境下，年化淨壞帳率不突破使風險調整後利差歸零的水位"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資本輕費收引擎失效：平台段持續萎縮、Financial Services 段 contribution margin 由 52% 降至 46% 的趨勢延續，費收佔比卡在 46% 上不去 → 報酬率目標的分母腿永遠修不好，估值框架被迫切換到消費放款銀行"},{"id":"R2","text":"口徑與查核風險：公允價值計量的認列時點爭議在年度查核程序中具體化（關鍵查核事項、重述、或監理問詢），或放空方持續施壓使折價常態化"},{"id":"R3","text":"消費信貸循環在晚期轉向：家庭債務 $18.19 兆創紀錄 ＋ 聯準會由降息轉升息 1-2 次 ＋ K 型分化下次級族群持續受壓 → 無擔保簿損失率上行，同時擠壓利差與資本"},{"id":"R4","text":"競爭結構下移：Chime 往上市場（Chime Prime）＋ 大型銀行奪回客戶成長 ＋ 存款端須維持 4.5% 年化利率才能留住存款"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","irr_base_pct":10.4,"ev5y_pct":58.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.4,"ev5y_pct":58.3,"irr_base_pct":10.4,"max_dd_pct":-55.0,"bull_5y_price":36.0,"bear_5y_price":10.3,"p_bull_pct":28.0,"p_bear_pct":27.0,"rearm_trigger":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","price_at_dd":15.25,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SOFI","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"SoFi Technologies, Inc."},"oneliner":"升息環境下營收仍年增 44%，2027 財測明言不增資。ROTCE 能否由 10% 爬到 15%，決定了估值；現價已先付了這段爬坡的錢。唯一致命數字是個貸全口徑淨壞帳率能否守在 5% 以下。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/scenario.json","answers":{"q1_business":{"verdict":"SoFi 賺的是會員的放款利差與手續費。放款段占調整後淨營收 59%，錢卡在資金成本與信用損失這一節：個貸票息 12.8% 扣掉資金成本 3.1%、損失 3.4% 之後，才是真正留下的。費收型營收占 42%，是降低這個依賴的第二條腿。","reasoning":"營收結構（2026Q3）：放款段調整後淨營收約 8.07 億美元，年增 68%，由個貸需求與手續費帶動。金融服務段 5.25 億，年增 25%，其中淨利息收入 +38%、非利息收入 +13%。技術平台段 8,740 萬，年減 24%，因大客戶 2025 年遷出；排除該客戶後 +18%。三段相加超過總額的部分是企業層調整。全公司調整後淨營收 13.71 億，GAAP 13.85 億。銀行不揭露毛利率與營業利益率，改看調整後 EBITDA 4.70 億（34%）、GAAP 淨利 2.41 億（17%）、淨利差 6.14%（季增 16bp）。單點依賴：個貸是唯一承重產品，Q3 個貸放款 126 億，占全部放款 169 億的四分之三，這是集中度風險，不是護城河證據。資金端以存款為主（513 億，目標 80–90% 由存款支應）。產業週期判在過熱段：全產業與公司的個貸放款量都在高檔；聯準會今年已由降息轉為升息；產業無擔保個貸逾期率年增 44bp。信用指標開始轉弱，但還沒出現損失潮。財測：2026 營收 50.4 億（+40%），2027 展望 64 億（+27%），淨利率由 17% 升到 20%。","fact_refs":["f_kpi0_gaap_total_net_revenue","f_kpi1_adjusted_net_revenue","f_kpi2_adjusted_ebitda_non_gaap","f_kpi3_gaap_net_income_sofi_gaa","f_kpi5_fy2026_guidance","f_kpi6_fy2027_outlook","f_kpi7_members","f_kpi8_total_products","f_kpi9_tangible_book_value_rotc"],"verdict_values":{"revenue_quality":"Q3 現金營收約 14 億美元（其中淨利息收入 9.27 億），與調整後淨營收 13.71 億相當，已連四季破 10 億。費收型營收 5.71 億，占 42%（Q2 為 39%）。放款手續費 2.71 億、年增 2.6 倍，多在放款當期認列，比票息更依賴放款量，是收入品質中較不穩定的一塊。","unit_econ_note":"核心個貸風險調整後利差約 7.6%＝票息 12.8%＋手續費 1.4%－資金成本 3.1%－年化損失 3.4%。放款段每產品年化收入 942 美元（去年同期 782），金融服務段 90 美元（上季 88）。每會員產品數 1.56（去年 1.47），新產品有 51% 來自既有會員。","archetype":{"primary":"金融","secondary":null,"confidence":"高","fingerprint":"全國性特許銀行的控股公司：淨利息收入是最大收入來源，放款段占營收 59%，成長受監理資本比約束。估值主錨用 P/TBV 對照 ROTCE。"},"industry":{"clock_phase":"III","sd_verdict_source":"供需耐久性分兩段看。會員與存款需求屬結構性持久，數位銀行滲透持續，會員年增 35%。個貸需求屬週期性、可能反轉：產業逾期率上升，聯準會轉為升息。週期判在過熱段，因為放款量創高的同時信用指標開始轉弱。來源：SoFi 2026Q3 新聞稿、TransUnion 2026Q2。","bargaining":{"up":"資金端有兩類。存款人議價力強，要給高利率才留得住（App 廣告 4.4% 年利率）。LPB 外部資金方議價力弱，Q2 法說稱其需求大於 SoFi 願意供給的量。","down":"借款人以優質客群為主，定價靠票息加手續費；手續費已覆蓋逾半數新個貸，但票息連幾季下滑。","geo":"營收全在美國本土，無海外集中。"},"profit_pool_dir":"事實表未涵蓋產業利潤池分布。可觀察到的是，個貸利潤正以兩種方式並行分配：留在 SoFi 資產負債表，或經 LPB 轉給外部資金方、SoFi 收手續費。","tam_table":[{"item":"SoFi 個貸市占（Dolphin Research 估計）","value":"2023 年約 6.8%，2025 年底約 12%；Truist 另有 >25% 的估計，口徑不同、日期不明"},{"item":"會員數","value":"1,710 萬，年增 35%；管理層規劃 2030 年約 5,000 萬會員支撐 1 億產品"},{"item":"產品數","value":"2,670 萬；管理層 2030 年目標 1 億（4 倍）"},{"item":"每會員產品數","value":"1.47（2025Q3）→ 1.56（2026Q3），管理層目標至少 2.0"},{"item":"費收型營收占比","value":"39%（2026Q2）→ 42%（2026Q3），目標 50% 以上"},{"item":"產業營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河持平，等級 B。多產品交叉購買讓每位會員的終身價值最高，SoFi 因此能把利潤讓回利率與費用去獲客。執行面在擴大；但放款端點對點競爭加劇、平台段又流失客戶，定價面只算穩定。","reasoning":"機制是「產品廣度×每產品單位經濟」推高會員終身價值，再用存款利率與貸款利率讓利獲客，取代分行成本。事實表沒有同業 ROIC 或 ROTCE；FCF 利潤率對銀行不可比（SoFi 為負，因放款計入營運現金流）。所以方向改用份額與留存來判斷：個貸份額估計由 2023 年約 6.8% 升到 2025 年底約 12%；每會員產品數一年由 1.47 升到 1.56；新產品 51% 來自既有會員；使用兩項以上產品的會員占 37%（去年 33%）。執行力給 8 分：營收成長加 EBITDA 利潤率連 20 季超過 40；2026 營收比原始財測多 3.85 億；升息環境下營收仍年增 44%。定價力給 6 分：手續費已覆蓋逾半數新個貸，公司稱個貸風險調整後利差年增逾 100bp，但兩季口徑沒對齊（見矛盾裁定）；個貸票息連幾季下滑；存款仍需高利率；平台段重要客戶轉投對手。當期 ROTCE 約 10%，增量報酬約 16.5%，報酬能維持多久見四檢查點。","fact_refs":["f_peer_sofi_fcf_margin_pct","f_peer_cof_fcf_margin_pct","f_peer_ally_fcf_margin_pct","f_peer_hood_operating_margin_pct","f_kpi7_members","f_kpi8_total_products","f_kpi9_tangible_book_value_rotc"],"verdict_values":{"moat":{"mechanism":"全產品線集中在單一 App，交叉購買推高每會員終身價值，再以較好的存放款利率讓利獲客；全國性銀行執照提供存款資金。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大、定價面穩定，合判持平。正面證據：每會員產品數 1.47→1.56，交叉購買占新產品 51%，個貸份額估計 6.8%→12%。負面證據：平台段重要客戶轉投對手，營收年減 24%；放款端競爭加劇。有已證實的最大客戶流失，不得判為擴大。","competitor_notes":[{"name":"COF","strategy_note":"信用卡與全國性存款的規模龍頭，資金成本與信用卡承保經驗都領先。SoFi 信用卡約 65.6 萬張，仍在虧損換規模，這條戰線 SoFi 是挑戰者。"},{"name":"ALLY","strategy_note":"純數位存款加汽車放款，是存款端的直接競品。SoFi 宣稱靠產品廣度而非利率勝出，需要交叉購買率持續上升來證明。"},{"name":"LC","strategy_note":"同樣持有銀行執照的個貸業者，是個貸定價戰的直接對手；事實表沒有其財務數據，無法比較利潤率。"},{"name":"HOOD","strategy_note":"投資與加密業務的主要對手，資本輕、利潤率遠高於 SoFi。管理層自承 SoFi Invest 的資產收入率低於基準，這一塊 SoFi 是追趕者。"},{"name":"Upstart","strategy_note":"科技型個貸直接對手。2026Q2 放款 42 億、年增 50%，約為 SoFi 同季個貸放款的四成，成長快於 SoFi 個貸，是壓價風險的主要來源。"}],"spread_notes":null,"peer_na_reason":"事實表沒有同業 ROIC 或 ROTCE。同業對照只有 FCF 利潤率，而銀行把放款計入營運現金流，FCF 不能拿來比較報酬率；改用份額、每會員產品數與交叉購買率判斷方向。","threats":[{"level":"🟡","text":"放款端點對點競爭：10-K 稱銀行、信用合作社與科技型放款人會壓價搶份額，Upstart 放款年增 50%。SoFi 以手續費替代票息來維持利差，屬點對點攻擊，不扣分。","p":30,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"平台段客戶集中：Galileo 重要客戶轉投對手，平台段營收年減 24%；排除該客戶則年增 18%。平台段占營收約 6%，不動搖主體護城河。","p":"已發生","evidence_refs":["substitute_technology#1","end_markets#2"]},{"level":"🟡","text":"AI 代理比價：代理工具若讓存放款利率與隱藏費用完全透明，單一產品的轉換摩擦會再降，存款可能變成追最高利率的熱錢。執行長認為終身價值最高者每次都贏，但這只是主張，還沒有證據。","p":20,"evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"低周轉、利益率爬升中：淨利率約 18% × 營收／權益約 0.57 ≈ ROTCE 10%，與股權成本相當","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者是同一位會員，三個角色不脫節。存款與支付屬於需要，不是想要；個貸多用來以 12% 利率替換 25% 的卡債，延後的代價是繼續付高息。讀數：會員年增 35% 至 1,710 萬，單季新增 120 萬創高；管理層稱未見借貸、消費、儲蓄、投資放緩。要注意的是，持久的是低成本數位銀行這個需求，不是個貸量，個貸會隨信用週期起伏。"},{"item":"決策層級","level":"🟡","text":"替代發生在單一產品層。存款跟著利率走，公司自承以高利率代替分行獲客；個貸由比價平台逐筆比較，轉換成本低。能拉高轉換成本的是多產品綁定：37% 會員使用兩項以上產品（去年 33%），新產品 51% 來自既有會員，Q2 稱獲客成本持平。AI 代理比價若普及，單一產品的轉換摩擦還會再降。"},{"item":"價值鏈分配","level":"🟡","text":"SoFi 自己掌握獲客、放款、服務與核心系統，信用風險可以留在表內，也可經 LPB 轉給外部資金方賺手續費。Q2 稱 LPB 需求大於願意供給的量，對資金方有議價力。但存款端要付高利率，個貸票息連幾季下滑、改靠手續費補，對借款人的定價空間有限；管理層也說 LPB 變現率只會在區間內波動。"},{"item":"社會容忍度","level":"🟡","text":"定價上限同時受監理與社會約束。全國性銀行執照本身就是監理授權，資本比受監理約束；2019 年 FTC 同意令限制行銷時誤述節省金額。手續費已覆蓋逾半數新個貸，若消費金融監理轉嚴，手續費是最容易被盯上的項目。Basel III 最終版已重新提出較輕的版本，2026-06 意見期截止、尚未定案，方向中性。"}],"roiic":16.5,"reinvest_rate":100,"endo_ceiling":16.5,"formula_note":"單位為 %。增量 ROTCE：Q3 調整後淨利 2.43 億、年增 74%，年增量約 1.03 億，年化約 4.1 億；同期有形權益增加 25 億（其中約 15.9 億來自增發），4.1÷25≈16.5%。再投資率：不配息、不回購，盈餘 100% 留存放款；外部增資不算內生。內生上限＝16.5%×100%＝16.5%。增發的資本還沒用完（總資本比 17%，規劃水位 13.5%），完全投入後增量報酬可能更高，所以這個數字偏保守。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬。個貸份額約 12%，會員 1,710 萬，離管理層 2030 年約 5,000 萬的規劃還遠；第二條成長曲線有來源可查：金融服務段 2027 財測 +35%，另有信用卡、SMB 放款與 LPB 新資產類別。但近三年 EPS 高成長有一大段來自一次性的利潤率擴張，不能直接外推。","reasoning":"成長以量為主：會員年增 35%，產品年增 44%。價的部分是放款段每產品年化收入由 782 升到 942 美元，金融服務段由 88 升到 90 美元。沒有回購，併購規模小。共識三年 EPS：FY2025 實際 0.39（GAAP）、FY2026E 0.61、FY2027E 0.89、FY2028E 1.14（Koyfin 快照，分析師家數事實表未涵蓋），年複合約 43%。內生上限是 16.5%（增量 ROTCE 約 16.5% × 盈餘全數留存），缺口約 26 個百分點。缺口可以歸因：一是淨利率由 13%（FY2025）升到 20%（FY2027 財測）；二是超額資本投入（CET1 由 22.8% 降到 16.9%），把營收／權益比由 0.50 推到 0.57。兩者都是一次性墊高；等資本比回到中低十幾%、淨利率接近 25–30%，成長會回落到內生上限附近。跑道年數：個貸份額近兩年每年約推進 2.6 個百分點，照這個速度約 7 年到 30%，屬中等。管理層也預告 2026–2030 加權每產品收入會下降，因為產品組合偏向單價低的金融服務；產品成長 4 倍不等於營收成長 4 倍。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi5_fy2026_guidance","f_kpi6_fy2027_outlook","f_kpi7_members","f_kpi8_total_products","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"以量為主（會員 +35%、產品 +44%），價為輔（放款段每產品收入 +20%）；無回購，併購小，2026 年有約 15.9 億外部增資","runway_years":"約 7 年：個貸份額 12%，以每年約 2.6 個百分點推進到 30%；金融服務段另有第二曲線","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的推算：增量 ROTCE 約 16.5% × 盈餘全數留存 100% ＝ 16.5%","segments":[{"item":"放款段","value":"Q3 調整後淨營收約 8.07 億美元，年增 68%，占 59%；2027 財測年增 25%，成長來源改由房貸與學貸再融資帶動，個貸增速放慢"},{"item":"金融服務段","value":"Q3 淨營收 5.25 億，年增 25%（淨利息收入 +38%、非利息收入 +13%）；2027 財測年增 35%"},{"item":"技術平台段","value":"Q3 營收 8,740 萬，年減 24%（排除流失的大客戶則年增 18%）；段貢獻利潤只有 Q2 的 1,200 萬，Q3 段利潤事實表未涵蓋；2027 財測年增 25%"},{"item":"LPB（含在放款段內）","value":"Q3 代外部資金方放款 38 億、收入 1.53 億（Q2 為 31 億、1.43 億）；管理層稱變現率只在區間內波動"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"銀行沒有毛利率；淨利差 6.14%，季增 16bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"個貸份額估計上升；平台段客戶流失發生在非核心段"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"手續費覆蓋率上升的同時，個貸放款量創高"},{"signal":"EPS 成長顯著高於營收成長（差距 >5pp）","lit":true,"note":"FY2025→FY2027：EPS 由 0.39 到 0.90，年複合約 52%；營收由 36.1 億到 64 億，年複合約 33%，差 19pp。來源是淨利率擴張，屬一次性"},{"signal":"FCF／淨利 <0.75 連兩年","lit":false,"note":"不適用：銀行放款計入營運現金流，改看有形淨值年增 25%"},{"signal":"SBC 占營收 >5% 且逐年上升","lit":null,"note":"Q3 為 5.2%，已過線；事實表沒有歷年 SBC，無法判斷是否逐年上升，屬資料缺口"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"未見"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋產業倍數"},{"signal":"維持性資本支出占 FCF >60%","lit":false,"note":"不適用"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"未見"}],"trap_rating":"🟡（亮 1 個，另有 2 個資料缺口）"}}},"q4_capital":{"verdict":"資本配置中等。盈餘全數留下來做放款，不配息、不回購。2025-12 以 27.50 美元增發約 15.9 億美元，回頭看是以高 P/TBV 發股，對每股有形淨值有利。SBC 占營收 5.2%，年化稀釋約 1.3%，勉強達標。歷史收購形成的平台段正在萎縮，報酬無法驗證。","reasoning":"FCF／淨利對銀行不適用：放款計入營運現金流，FY2025 自由現金流 −39.9 億，拿來對淨利 4.8 億沒有意義。改看有形淨值：一年增加 25 億到 97.05 億，每股 7.48（+25%）。其中約 15.9 億來自 2025-12 的增發（57,754,660 股×27.50 美元）；以 2025 年 9 月底每股有形淨值 5.97 計，約 4.6 倍 P/TBV 發股（實際發股時淨值略高，倍數略低），對既有股東是增值。近三年現金去向的四分拆解，事實表未涵蓋。看得到的是：盈餘全數留存放款，Q3 貸款增加 58 億，CET1 由 2025 年底 22.8% 降到 16.9%，管理層計畫降到中低十幾%。SBC 單季 7,090 萬，占調整後淨營收 5.2%、占調整後 EBITDA 15.1%。收購：2026Q2 買下 Peach Finance 與 Composer，另有報導收購 PrimaryBid 資產，條款都未揭露；過去收購形成的技術平台段營收年減 24%，Q2 貢獻利潤只有 1,200 萬。2027 計畫明言不增資：以 13.5% 資本比計，現有資本可支撐 710 億風險資產（現在 560 億），加上盈餘再生約 140 億的容量。","fact_refs":["f_kpi4_share_based_expense_sbc","f_peer_sofi_fcf_margin_pct","f_kpi9_tangible_book_value_rotc","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"過去收購形成的技術平台段（Galileo、Technisys），Q3 營收年減 24%，Q2 貢獻利潤 1,200 萬美元（年化約 4,800 萬）。收購對價事實表未涵蓋，無法算出已實現 ROIIC；2026 年三筆收購條款也未揭露。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"沒有回購計畫；反而在 2025-12 以 27.50 美元增發 5,775 萬股。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 單季 7,090 萬美元×4≈2.84 億，以現價 17.38 計約 1,630 萬股，占 12.97 億股約 1.3%／年，沒有回購抵銷，勉強達標。但若用財測淨利÷EPS 推算稀釋股數，2026→2027 年增約 3%（含可轉債等），改用這個口徑就不過。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠盈餘留存與放款再投資，不靠併購；2026 年三筆收購條款未揭露、規模小，展開也沒有可算的報酬數字"}}}},"q5_valuation":{"verdict":"現價要求 ROTCE 由 10% 升到約 15% 並長期維持，P/TBV 2.32 倍才算合理；換句話說，2027 財測要兌現，2028 還要再往上一段。資本算式與升息下的成長只給了一半證據，信用循環還沒過考驗。估值合理，但不便宜。","reasoning":"銀行尺：P/TBV＝17.38÷7.48＝2.32 倍。合理 P/TBV＝(ROTCE−g)÷(股權成本−g)；以股權成本 10%、長期成長 6% 計，ROTCE 10% 只值 1.0 倍，12%（2027 推算值）值 1.5 倍，15% 值 2.25 倍。現價大致已預付 15% 的 ROTCE。成長尺：前瞻本益比 FY2026 為 28.5 倍，FY2027（共識 0.89）19.5 倍，FY2028 15.2 倍；PEG 約 0.66（28.48 ÷ 三年 EPS 年複合 43%）。歷史位置：P/S 在四個年度端點中位於 31%，EV/S 位於 7%，本益比只有兩個年度端點；三者都不是五年連續分位。短期上檔：2027 共識 EPS 0.89 × 23 倍≈20.5 美元，約 +18%。中期上檔：基本情境 FY2029 EPS 1.36 × 18 倍≈24.5 美元，約 +41%。分母是否有爭議：放空方質疑公允價值計量，但本季公允價值淨效果是拖累（負向逾 8 億、避險利得約 7.34 億抵銷），現金營收也與調整後淨營收相當，EPS 分母沒有被墊高的跡象，不視為爭點。共識近三個月 FY1 上修 1.7%，FY2 持平。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi9_tangible_book_value_rotc","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_ma_state","f_ma_w104","f_rsi14","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"主錨用 P/TBV 對照 ROTCE（合理倍數＝(ROTCE−g)÷(股權成本−g)），輔以前瞻本益比","tier":"數位銀行／消費放款（金融類）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業 P/TBV 或前瞻本益比，無法做倍數對照；終端倍數只能用自身現值校準"},"fwd_pe":28.48,"peg":0.66,"percentile_5y":31.4,"val_light":"🟡","val_light_derivation":"兩把尺結論相反。銀行尺偏貴：P/TBV 2.32 倍，以 ROTCE 約 10%、股權成本約 10% 推算，合理倍數只有約 1.0 倍，現價已預付 ROTCE 升到約 15% 的路徑（(15%−6%)÷(10%−6%)＝2.25 倍）。成長尺偏便宜：FY2027 共識 EPS 對應 19.5 倍，PEG 約 0.66。兩尺一貴一便宜，取中間，判為合理。歷史分位用的是 P/S 四個年度端點中的 31%，不是五年連續序列。","upside_short_pct":18,"upside_mid_pct":41,"denominator_disputed":false,"denominator_note":"放空方質疑公允價值計量，但 Q3 公允價值淨效果為負（負向逾 8 億、避險利得約 7.34 億抵銷），現金營收約 14 億與調整後淨營收 13.71 億相當，EPS 分母沒有被墊高的跡象；年報查核意見（約 2027-02）出來前保留判斷。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是升息中的個貸信用。全口徑淨壞帳率一旦突破 5%，淨利息收入、公允價值標記、LPB 需求與資本比會同時受傷。其次是年報查核對公允價值的結論（約 2027-02）。陷阱風險中度。","reasoning":"三個視角的反證與裁定見反證紀錄。論點失敗路徑（信用循環加上標記回吐）採納為空頭主線，機率 30%。股東經濟變差（每年稀釋約 2–3%、ROTCE 卡在 12–13%）部分採納。價格已反映太多（P/TBV 已預付 15% ROTCE）部分採納，估值因此降為合理。歷史回撤參考：2025-12 增發價 27.50 到 2026-07 低點 14.88，約 −46%。","fact_refs":["f_kpi9_tangible_book_value_rotc","f_price_at_dd","f_kpi6_fy2027_outlook"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長正在兌現，但信用循環與公允價值查核兩關還沒過"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":0.61,"pe":28.49,"basis":"起點用 FY2026E 共識 EPS 0.61（Koyfin，與公司 2026 調整後 EPS 財測相同）；終端倍數同樣套在終端年當年度 EPS 上，口徑一致"},"eps":{"bull":[0.93,1.22,1.55,1.92,2.3],"base":[0.89,1.12,1.36,1.56,1.75],"bear":[0.62,0.35,0.5,0.65,0.8]},"pe":{"bull":20,"base":17,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-65,"hi":-45,"basis":"錨點：2025-12 增發價 27.50 美元跌到 2026-07-29 的 52 週低點 14.88 美元，約 −46%；這段期間沒有信用事件，只有利率轉向與放空報告。若信用循環與公允價值下修同時發生，回撤會比這次更深；空頭情境終點本身就是 −54%。因此取 −45% 到 −65%。","trigger_time":null},"basis":{"bull":"管理層路徑大致兌現：2027 小幅超越財測（0.93），ROTCE 在 2030 年前到 20%，費收占比過半。2031 年 EPS 2.30，約為 2026 的 3.8 倍，仍低於管理層口頭說的 4 倍。終端 20 倍。事實表沒有同業前瞻本益比，只能用自身對照：現價對 2027 共識是 19.5 倍。","base":"2027 照共識 0.89，2028 為 1.12，之後年成長由 21% 遞減到 12%，2031 年 1.75，ROTCE 約 15%；每年 2–3% 的股數增加已內含在 EPS 裡。終端 17 倍，是成長降到十位數中段時的銀行加金融科技混合倍數，低於現價對 2027 的 19.5 倍。","bear":"升息週期把個貸全口徑壞帳推到 6–7%，標記跌破面值，LPB 資金方縮手。2027 為 0.62，2028 谷底 0.35，2031 只回到 0.80。終端 10 倍取成長熄火、降到 10% 情境下的消費放款倍數，約當 P/TBV 0.8 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"聯準會今年已升息一次，管理層預期年內再升兩次，2027 財測再假設兩次。TransUnion 2026Q2 無擔保個貸借款人 60 天以上逾期率 3.81%（去年 3.37%）。放款段占營收 59%，以個貸為主；個貸帳面標記 103.3%；總資本比單季降 180bp。","assumption":"SoFi 客群偏高收入，這輪升息不會把個貸全口徑淨壞帳率推過 5%。","consequence":"壞帳升到 6–7%、標記跌破面值，EPS 在 2028 年掉到 0.35 左右；LPB 資金方縮手，資本比逼近下限，被迫以低 P/TBV 增資。五年後股價約 8 美元（−54%）。","ruling":"採納為空頭主線，機率 30%。這條與唯一致命數字同源，門檻沿用個貸淨壞帳率 5.0%。","watch":"每季的個貸全口徑淨壞帳率、表內 90 天逾期率、個貸標記、總資本比","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#5","financial_regulatory_capital_rules#0"],"fact_refs":["f_kpi9_tangible_book_value_rotc","f_kpi1_adjusted_net_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 單季 7,090 萬美元，占調整後淨營收 5.2%。2025-12 以 27.50 美元增發 5,775 萬股。以財測淨利÷EPS 推算，稀釋股數 FY2026 約 13.8 億、FY2027 約 14.2 億，年增約 3%。存款靠高利率獲客（App 廣告 4.4% 年利率）。技術平台段連三季年減兩成以上，費收占比靠它推升的那條路受阻。","assumption":"營收與會員成長會轉成每股盈餘與每股有形淨值的成長。","consequence":"營收五年翻倍，但每年 3% 稀釋加上存款成本降不下來，ROTCE 卡在 12–13%，每股價值的成長只剩營收成長的一半左右。","ruling":"部分採納。每股有形淨值年增 25%（7.48 對 5.97），目前跑贏稀釋，但其中一部分來自 27.50 美元的高價增發，這種效果不會重複。基本情境 EPS 已內含每年約 2–3% 的股數增加；若稀釋超過每年 4%，就下修基本情境。","watch":"每季稀釋股數年增率、SBC 占營收比、費收型營收占比","evidence_refs":["channel_business_model_shift#2"],"fact_refs":["f_kpi4_share_based_expense_sbc","f_kpi9_tangible_book_value_rotc","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"P/TBV 2.32 倍對 ROTCE 約 10%；用合理倍數公式算，10% ROTCE 只值約 1.0 倍，ROTCE 要長期維持約 15% 才撐得起現價。2027 展望與共識幾乎相同：營收 64 億對 63.9 億，EPS 0.90 對 0.89。Q1 後 Morgan Stanley、Truist 把目標價降到 16、17 美元。","assumption":"市場會繼續用成長股倍數，而不是銀行倍數來評價 SoFi。","consequence":"若市場改用銀行尺，而 ROTCE 到 2028 只有 13%，合理 P/TBV 約 1.75 倍；乘上 2028 年底推算的每股有形淨值約 9.7 美元，約 17 美元，等於兩年零報酬。","ruling":"部分採納，估值因此降為合理。但對 2027 EPS 19.5 倍、EPS 年增近五成，不是泡沫價，不構成迴避的理由。","watch":"季度 ROTCE 與 15% 路徑的差距、P/TBV","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_kpi9_tangible_book_value_rotc","f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 15.25 → 本次 17.38（+14.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=15.25","side_b":"本次 price_at_dd=17.38","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 15.25 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 15.25 美元：Bull 價 36、Bear 價 10.3，五年期望值 +58.3%，基準年化 10.4%，不對稱比 4.4","side_b":"本次情境、股價仍用 15.25 美元：Bull 價 46、Bear 價 8，五年期望值 +78.9%，基準年化 14.3%，不對稱比 3.53","ruling":"先換情境、股價不動：五年期望值多 20.6 個百分點，基準年化多 3.9 個百分點。不對稱比由 4.4 變為 3.53。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 15.25 美元：五年期望值 +78.9%，基準年化 14.3%，不對稱比 3.53","side_b":"本次情境、股價 17.38 美元：五年期望值 +57.0%，基準年化 11.3%，不對稱比 2.54","ruling":"再換股價、情境不動：起點價上漲 14.0%，五年期望值少 21.9 個百分點，基準年化少 2.9 個百分點，不對稱比由 3.53 降到 2.54。合計五年期望值比前份少 1.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值結論與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-30，股價 15.25）：估值偏便宜；裁決觀望","side_b":"本次（股價 17.38，+14%）：估值合理；裁決與角色由本次輸入重新決定","ruling":"FY2026 共識 EPS 只從 0.60 升到 0.61（+1.7%），股價卻漲了 14%，前瞻本益比跟著上升。以每股有形淨值 7.48 計，P/TBV 2.32 倍、ROTCE 約 10%，銀行尺偏貴、成長尺便宜，所以降一級到合理。變動主因是價格，不是基本面轉差。","evidence_level":"事實表價格與共識","settle_metric":"P/TBV 與季度 ROTCE","if_then":["若股價回到 15 美元以下而基本面無損，則估值回到偏便宜，可分批反買"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤區間","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 28%、空頭 27%、最大回撤 −55%","side_b":"本次：多頭 25%、空頭 30%、最大回撤 −45% 到 −65%","ruling":"前份預期聯準會降息，結果是已升息一次、年內預期再升兩次，2027 財測再假設兩次；產業無擔保個貸 60 天以上逾期率年增 44bp。基本情境 EPS 年複合 23.5%，高於內生上限 16.5%，空頭機率至少要 30%。最大回撤改給區間，依據見情境樹。","evidence_level":"公司法說與產業信用數據","settle_metric":"2026Q4 與 2027Q1 個貸全口徑淨壞帳率","if_then":["若連兩季淨壞帳率 ≤3.5% 且已再升息兩次，則空頭機率降回 25%"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"axis":"前份漂移：基本面欄位複核後維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質訊號 B、陷阱風險中度、護城河持平、五年後跑道寬、金融類、未判循環位置","side_b":"本次：與前份相同，以 Q3 新數據複核後維持","ruling":"支持飛輪的數據：會員年增 35%，每會員產品數 1.47→1.56，交叉購買占新產品 51%。但平台段大客戶流失、放款競爭加劇，護城河不升級。衰退訊號只亮一個（EPS 成長遠高於營收成長，來自利潤率擴張），陷阱風險維持中度。個貸份額約 12%（Dolphin 估計），金融服務段 2027 財測年增 35%，跑道維持寬。循環位置不適用，本檔以金融類評估，不是循環股。","evidence_level":"公司一手揭露","settle_metric":"每會員產品數、費收型營收占比","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","side_b":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","ruling":"舊條件的後半段已達成：CFO 揭露營收／權益比 Q3 約 0.57（前份記 0.503，CFO 稱 Q2 已 0.55，兩者口徑可能不同）。前半段會在 2027Q1 因大客戶 2025 年遷出的基期效應自動轉正，那是機械觸發，不是證據。因此改綁本次唯一致命數字（個貸壞帳）加技術面確認，滿足後才建首倉。104 週均線已由 17.70 升到 18.81。","evidence_level":"公司法說與週線均線","settle_metric":"週收盤相對 104 週均線、個貸全口徑淨壞帳率","if_then":["若站回 104 週均線但個貸淨壞帳率 >4.0%，則不追"],"evidence_refs":[]},{"axis":"前份漂移：清倉與減碼門檻（新設）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（null）","side_b":"清倉：個貸全口徑淨壞帳率任一季 >5.0%，或年報查核出現重述或重大內控缺失。減碼：總資本比 <12.5% 或增發普通股，減碼一半；2027 年任兩季 ROTCE <11%，減碼三分之一","ruling":"前份只有論點與風險，沒有可執行的清倉線。本次替信用、資本、會計三個最大敏感項各設門檻，數字都取自公司每季揭露。","evidence_level":"公司一手揭露","settle_metric":"各門檻的季度讀數","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing（新設）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"個人貸款全口徑年化淨壞帳率（排除逾期貸款出售）任一季升破 5.0%（2026Q3 為 3.4%）","ruling":"前份把信用風險列為多條風險之一。本次判定它是數學上最大的單一敏感項，因為它同時打到淨利息收入、公允價值標記、LPB 需求與資本比，所以升格為 Single Thing。","evidence_level":"公司法說的利差拆解","settle_metric":"個貸全口徑年化淨壞帳率","if_then":[],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"信用：公司壞帳改善，產業逾期上升","cause":null,"prior_field":null,"side_a":"公司：個貸全口徑淨壞帳率由 Q2 3.7% 降到 Q3 3.4%，年降 80bp；表內 90 天逾期 42bp，持平。執行長稱未見會員借貸放緩。","side_b":"產業：TransUnion 2026Q2 無擔保個貸借款人 60 天以上逾期 3.81%（去年 3.37%），消費者 90 天以上逾期升到 2.26%；聯準會轉為升息。","ruling":"可調和，屬程度差異。產業惡化主要來自次級族群，SoFi 客群偏高收入。但公司壞帳改善有一部分是平均貸款餘額成長稀釋了分母，新放款也還沒走完一個升息週期。當下讀數採公司側，空頭機率 30% 反映這點尚未驗證。","evidence_level":"公司一手揭露對照產業數據（搜尋摘要）","settle_metric":"2026Q4、2027Q1 個貸全口徑淨壞帳率與表內 90 天逾期率","if_then":["若 2027Q1 個貸淨壞帳率 >4.5% 且 90 天逾期 >60bp，則減碼一半","反向條件：若連兩季 ≤3.5% 且已再升息兩次以上，則加碼到目標倉位"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"axis":"會計：公允價值計量","cause":null,"prior_field":null,"side_a":"放空方（Muddy Waters，2026-03-17）稱 SoFi 的貸款會計與公允價值評價高估；律所 2026-05-04 公告展開證券法調查。","side_b":"公司：Q3 公允價值負向影響逾 8 億美元，約 7.34 億由避險利得抵銷；個貸標記 103.3%，季降 140bp。現金營收 14 億美元（淨利息收入 9.27 億），連四季破 10 億。執行長買進 28,900 股。","ruling":"不可調和，兩邊方向相反；現有證據偏向公司側：本季公允價值是淨拖累而不是墊高盈餘，現金營收也與調整後淨營收（13.71 億）相當。但標記仍高於面值 3.3 個百分點，信用轉弱時會一次回吐。在 FY2026 年報查核意見（約 2027-02）出來之前無法裁決。","evidence_level":"公司一手揭露加放空報告（未見原文）","settle_metric":"FY2026 10-K 查核意見與公允價值相關查核事項；個貸標記","if_then":["若出現重述或重大內控缺失，則清倉","反向條件：若查核意見無保留且個貸標記 ≥101%，則取消為此預留的減碼，維持原倉位"],"evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"axis":"口徑：個貸風險調整後利差前後不一","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說，CFO：核心個貸風險調整後利差約 6.1%。","side_b":"2026-10-27 Q3 法說，CFO：約 7.6%（票息 12.8%＋手續費 1.4%－資金 3.1%－損失 3.4%），並稱票息加手續費收益率季持平、年增逾 100bp。","ruling":"不可調和，屬數字層矛盾。票息加手續費季持平、損失只降 30bp，推不出單季升 150bp；最可能是兩季口徑不同（例如 Q2 未含手續費）。在 10-Q 對帳之前，不把 7.6% 當成定價力提升的證據，護城河的定價分不因此加分。","evidence_level":"管理層口頭數字","settle_metric":"Q3 10-Q 的個貸收益拆解；Q4 法說是否沿用同一口徑","if_then":["若 Q4 以同口徑仍 ≥7.0%，則把定價力由 6 分調到 7 分","反向條件：若口徑回到 6% 區間，則維持原分數，並把手續費依賴列為放款定價風險"],"evidence_refs":[]},{"axis":"市場：券商下修目標價，公司上修財測","cause":null,"prior_field":null,"side_a":"Q1 後券商下修目標價：Morgan Stanley 16（賣出）、Truist 17（持有）、Citi 30、Mizuho 29。共識為持有，平均目標價約 21.4（2026-08）。","side_b":"Q3 公司上修 2026 營收到 50.4 億，首次給出 2027 營收 64 億、EPS 0.90，並明言不需增資。","ruling":"可調和。下修發生在 Q3 上修之前，屬事實層的時間差。但 2027 展望與共識幾乎相同（營收 64 億對 63.9 億，EPS 0.90 對 0.89），上修沒有帶來新的盈餘驚喜。目標價全距 16 到 30，約 1.9 倍，未超過 2.5 倍，不因此下調信心。現價接近看空券商的目標價，代表市場的風險折價還在。","evidence_level":"賣方動態（搜尋摘要）對照公司一手財測","settle_metric":"Q4 財報後 FY2027 共識 EPS 的修正方向","if_then":["若 Q4 財報後 FY2027 共識上修 ≥5%，則可加碼","反向條件：若下修 ≥5%，則停止加碼"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"管理層前後說法：SoFi Plus 目標與盈餘 4 倍","cause":null,"prior_field":null,"side_a":"2026-07-29，執行長 Noto：一年後若沒有 100 萬 SoFi Plus 付費會員會失望。","side_b":"2026-10-27，執行長 Noto：Q3 SoFi Plus 增長低於預期（約 27.5 萬），並說到期沒達到也沒關係，總會到。同場稱產品成長 4 倍可推動盈餘 4 倍，卻又說 2026–2030 加權每產品收入會下降。","ruling":"可調和，但扣管理層信用分。SoFi Plus 年化收入約 3,300 萬美元（27.5 萬×120 美元），不承重。盈餘 4 倍與每產品收入下降要同時成立，淨利率得由 20% 升到 30%。基本情境 2031 年 EPS 1.75，約為 2026 的 2.9 倍，不採用 4 倍。","evidence_level":"兩季法說逐字稿","settle_metric":"SoFi Plus 付費會員數、淨利率","if_then":["若 2027 年底前 SoFi Plus 達 100 萬，則多頭機率可加回 28%"],"evidence_refs":[]},{"axis":"前季迴避的三個問題，本季回答程度","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說沒有正面回答三題：EBITDA 為何不上修、LPB 個貸量是否繼續受限、超額資本消耗的速度。","side_b":"2026-10-27 Q3 法說：EBITDA 由 16 億上修到 16.6 億；LPB 單季 38 億創高，Q4 進度超前；CFO 給出資本容量算式（13.5% 資本比下可支撐 710 億風險資產，現在 560 億，加上盈餘再生約 140 億），但仍未給消耗時程。","ruling":"前兩題已補答。資本消耗速度只給了容量、沒給節奏，列入資本風險追蹤；總資本比單季降 180bp 的速度若持續，2027 年中就會接近規劃水位。","evidence_level":"兩季法說逐字稿","settle_metric":"每季總資本比降幅","if_then":["若連兩季單季降幅 >200bp，則停止加碼"],"evidence_refs":["financial_regulatory_capital_rules#0"]},{"axis":"產業態勢：競爭、結構與其他變數","cause":null,"prior_field":null,"side_a":"競爭惡化：10-K 稱新進者與既有業者會壓價搶份額；Upstart 放款年增 50%；平台段重要客戶轉投對手。","side_b":"結構轉好：SoFi 個貸份額由 2023 年約 6.8% 升到 2025 年底約 12%（Dolphin 估計）；LPB 需求大於供給；會員年增 35%。","ruling":"雙向拉鋸。SoFi 仍在拿份額，但放款定價壓力與平台客戶集中同時存在。其他結構變數中性：Basel III 重新提出較輕的版本，2019 年 FTC 同意令沒有新動作。","evidence_level":"10-K 加第三方估計","settle_metric":"個貸份額、核心個貸風險調整後利差","if_then":["若風險調整後利差（以 Q3 口徑）連兩季 <6.0%，則判為競爭惡化中，停止加碼"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#1"]},{"axis":"反方論證：現在就買的最強理由","cause":null,"prior_field":null,"side_a":"現在就買：股價是 2027 共識 EPS 的 19.5 倍，2027 EPS 年增約 46%；不需增資；升息下營收仍年增 44%；每股有形淨值年增 25%；股價比 2025-12 增發價 27.50 低 37%。","side_b":"再等一下：股價仍在 52 週與 104 週均線之下，信用在升息中還沒被考驗，年報查核意見也還沒出。","ruling":"買進理由在基本面上成立，但時點證據不足。首倉條件設為技術面站回 104 週均線，並搭配壞帳讀數；若價格先漲、證據還沒到，就不追。","evidence_level":"公司一手揭露加週線均線","settle_metric":"週收盤相對 104 週均線、個貸全口徑淨壞帳率","if_then":["若股價站回 104 週均線但個貸淨壞帳率 >4.0%，則不追","反向條件：若股價跌破 15 美元而個貸淨壞帳率 ≤3.5%、總資本比 ≥13.5%，則分批反買，首倉 2%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"個貸全口徑年化淨壞帳率任一季突破 5.0%","type":"Single Thing","maps_to":"R3","metric":"個貸全口徑年化淨壞帳率（排除逾期貸款出售）","threshold":">5.0%（2026Q3 為 3.4%）","action":"清倉","source_freq":"季度財報新聞稿與法說","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":2,"text":"個貸淨壞帳率連兩季 >4.5%，或表內 90 天逾期率 >60bp","type":"風險","maps_to":"R3","metric":"個貸全口徑淨壞帳率、表內 90 天逾期率","threshold":">4.5% 連兩季；或 >60bp（2026Q3 為 42bp）","action":"減碼一半並停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["financial_capital_credit_cycle#1","end_markets#5"]},{"n":3,"text":"FY2026 年報查核意見對公允價值的結論","type":"風險","maps_to":"R2","metric":"查核意見、公允價值相關查核事項、重述或內控缺失","threshold":"出現重述或重大內控缺失","action":"清倉；只列為查核事項而沒有調整則不動","source_freq":"年度 10-K","date":"2027-02","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"n":4,"text":"總資本比跌破 12.5%，或宣布增發普通股","type":"減碼","maps_to":"H2","metric":"總資本比、普通股增發","threshold":"<12.5%（2026Q3 為 17%）或任何普通股增發","action":"減碼一半，並以新股數重算情境","source_freq":"季度 8-K 與 10-Q","date":null,"evidence_refs":["financial_regulatory_capital_rules#0"]},{"n":5,"text":"2027 年季度 ROTCE 達到 12%","type":"假設驗證","maps_to":"H1","metric":"季度 ROTCE","threshold":"2027 年任兩季 ≥12%","action":"論點獲得驗證，可由首倉加到目標倉位 4%","source_freq":"季度財報新聞稿","date":"2027-07","evidence_refs":[]},{"n":6,"text":"大客戶基期效應消失後，平台段能否回到財測成長","type":"假設驗證","maps_to":"R1","metric":"技術平台段營收年增率","threshold":"2027Q1 ≥+18%；<10% 視為未通過","action":"未通過則停止加碼","source_freq":"季度財報新聞稿","date":"2027-04","evidence_refs":["end_markets#2","channel_business_model_shift#2","substitute_technology#1"]},{"n":7,"text":"產業無擔保個貸逾期率續升","type":"風險","maps_to":"R3","metric":"TransUnion 無擔保個貸借款人 60 天以上逾期率","threshold":">4.2%（2026Q2 為 3.81%）","action":"停止加碼","source_freq":"TransUnion 季報","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":8,"text":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","type":"估值rearm","maps_to":"H2","metric":"週收盤相對 104 週均線、個貸淨壞帳率、普通股增發","threshold":"站回滿 4 週，且壞帳 ≤4.0%，且未增資","action":"建首倉 2%","source_freq":"每週價格加季度財報","date":null,"evidence_refs":[]},{"n":9,"text":"股價漲到盈餘撐不住的區間","type":"減碼","maps_to":"H1","metric":"股價、季度 ROTCE","threshold":"股價 >27 美元（約 2027 共識 EPS 30 倍、P/TBV 3.6 倍），而 ROTCE 未達 13%","action":"減碼三分之一","source_freq":"每日價格加季度財報","date":null,"evidence_refs":[]},{"n":10,"text":"放款段占營收持續上升，收入結構更集中","type":"風險","maps_to":"R1","metric":"放款段占調整後淨營收比","threshold":"連兩季 ≥62%（2026Q3 為 59%）","action":"停止加碼","source_freq":"季度財報新聞稿","date":null,"evidence_refs":["end_markets#5"]},{"n":11,"text":"個貸定價被侵蝕","type":"風險","maps_to":"R5","metric":"核心個貸風險調整後利差（以 Q3 口徑）","threshold":"連兩季 <6.0%（2026Q3 約 7.6%）","action":"停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":12,"text":"2026Q4 財報與 2027 財測更新後重新研究","type":"複審日期","maps_to":"H1","metric":"2027 EPS 財測、個貸淨壞帳率、總資本比","threshold":"財報公布","action":"重新跑完整研究","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"個貸全口徑年化淨壞帳率（排除逾期貸款出售）","bear_threshold":"任一季 >5.0% 即清倉（2026Q3 為 3.4%）","window":"每季，至 2028Q4","source":"公司季度財報新聞稿與法說","last_status":"ok"},{"metric":"年報查核意見與公允價值相關查核事項","bear_threshold":"出現重述或重大內控缺失即清倉","window":"FY2026 年報（約 2027-02）","source":"SEC 10-K","last_status":"unknown"},{"metric":"總資本比與普通股增發","bear_threshold":"總資本比 <12.5% 或宣布增發普通股，即減碼一半（2026Q3 為 17%）","window":"每季，2027 全年","source":"公司 8-K、10-Q 監理資本揭露","last_status":"ok"},{"metric":"個貸公允價值標記","bear_threshold":"<101% 即停止加碼（2026Q3 為 103.3%，季降 140bp）","window":"每季","source":"季度法說與 10-Q","last_status":"warning"},{"metric":"季度 ROTCE","bear_threshold":"2027 年任兩季 <11%，減碼三分之一","window":"2027Q1 到 Q4","source":"公司季度財報新聞稿","last_status":"unknown"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"這是 2019 年同意令既有義務的揭露，只限制行銷時誤述節省金額；10-K 沒有揭露任何違反、新調查或罰款金額。證據描述的是一個存在七年的行為約束，不是新事件，也沒有可量化的營收暴露。"},{"ref":"reg_tariff_export#0","reason":"10-K 的制式風險條款，原文只說貿易政策過去曾影響金融市場，沒有給出公司損益的傳導路徑或金額。總經對消費信用的實際影響，已改由個貸逾期率與壞帳門檻直接追蹤，不重複計入。"},{"ref":"reg_tariff_export#1","reason":"條款只說全球匯款服務可能受制裁限制，但事實表與 Q3 逐字稿都沒有把匯款列為營收來源或給出占比，證據本身沒有暴露金額。"},{"ref":"reg_tariff_export#2","reason":"這是 2025-04 單一分析師（Morgan Stanley）的方向性意見，沒有量化。之後 18 個月，公司個貸全口徑淨壞帳率反而由 2026Q2 的 3.7% 降到 Q3 的 3.4%，預期的關稅傳導沒有出現在損益上，證據已過時。"},{"ref":"geo_supply_chain#0","reason":"引用的是 FY2024 年報的制式條款，已被 FY2025 年報取代；沒有指名單一供應商，也沒有服務中斷紀錄或金額，無法從這條證據量化營運中斷風險。"},{"ref":"$.scenario_inputs.p","reason":"閘把兩個機率放在同一期間比較。唯一致命數字的 15% 是未來 12 到 24 個月內任一季破 5.0% 的近端機率；空頭情境的 30% 是五年情境權重，除了這段近端機率，還包含兩年後才破線的路徑，以及基本情境 EPS 年複合 23.5% 高於內生上限 16.5% 所加上的權重（見情境機率與回撤區間的漂移裁定）。空頭 EPS 路徑把谷底放在 2028 年只是代表性時點，不代表 30% 全落在兩年內。兩個數字口徑不同、方向一致，機率不改。"}],"action_conditions":{"rearm_trigger":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","exec_line":"首倉 2%，分兩批：第一批在重啟條件達成時，第二批等 2027Q1 個貸淨壞帳率 ≤4.0%。2027 年兩季 ROTCE ≥12% 後，上限加到 4%。任一清倉條件觸發即全數出清。","holding_cap":"4%。路徑風險高但論點完整，不因股價波動砍倉，要有深回撤的心理準備"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場仍把 SoFi 當成要靠增資撐成長、利率一升就失速的消費放款商：2026 年股價跌約四成，Morgan Stanley、Truist 在 Q1 後把目標價降到 16、17 美元，現價就在這一帶。Q3 已經反證這兩個前提：升息中營收仍年增 44%、個貸壞帳年降 80bp，CFO 也給出不需增資的資本算式。不過 2027 展望與共識幾乎一樣，市場錯的是風險折價，不是盈餘預期；要反轉，得靠接下來的信用數據。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"現價不建倉。首倉 2% 要等以下任一條件成立：一、週收盤站回 104 週均線（現 18.81 美元）滿 4 週，且最近一季個貸全口徑淨壞帳率 ≤4.0%、2027 年未增發普通股；二、股價跌破 15 美元，同時個貸全口徑淨壞帳率 ≤3.5%、總資本比 ≥13.5%。價格先到、壞帳證據沒到，就不追。"},"decision_out":{"role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場仍把 SoFi 當成要靠增資撐成長、利率一升就失速的消費放款商：2026 年股價跌約四成，Morgan Stanley、Truist 在 Q1 後把目標價降到 16、17 美元，現價就在這一帶。Q3 已經反證這兩個前提：升息中營收仍年增 44%、個貸壞帳年降 80bp，CFO 也給出不需增資的資本算式。不過 2027 展望與共識幾乎一樣，市場錯的是風險折價，不是盈餘預期；要反轉，得靠接下來的信用數據。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=7.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='現價不建倉。首倉 2% 要等以下任一條件成立：一、週收盤站回 104 週均線（現 18.81 美元）滿 4 週，且最近一季個貸全口徑淨壞帳率 ≤4.0%、2027 年未增發普通股；二、股價跌破 15 美元，同時個貸全口徑淨壞帳率 ≤3.5%、總資本比 ≥13.5%。價格先到、壞帳證據沒到，就不追。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"報酬率爬坡：淨利率與營收／權益比同時上升，ROTCE 由 2026Q3 的約 10% 升到 FY2028 的 15% 以上；管理層長期目標是 20–30%。","2y":null,"5y":"FY2028 ROTCE ≥15%，FY2030 ≥18%","10y":null,"threshold":"FY2027 全年 ROTCE ≥12%（財測淨利 12.8 億 ÷ 推算的平均有形權益約 108 億）；FY2028 ≥15%","source":"公司季度新聞稿的 ROTCE；CFO 在法說揭露的營收／權益比（Q3 為 0.57）","drift_rule":"TTM ROTCE 低於路徑 5% 以上（相對值）連續 4 季，論點削弱；低於 10% 以上連續 6 季，論點反轉"},{"id":"H2","text":"2027 成長完全靠內部資本：不增發普通股；總資本比由 17% 往中低十幾%回落，但不破 12.5%；個貸全口徑年化淨壞帳率守在 4.5% 以下。","2y":"2027 年底前零增資、總資本比 ≥12.5%、個貸淨壞帳率 ≤4.5%","5y":null,"10y":null,"threshold":"任何普通股增發即失效；總資本比 <12.5%；個貸淨壞帳率連兩季 >4.5%","source":"8-K 與 10-Q 的監理資本比；季度法說的信用數據","drift_rule":"總資本比單季降幅連 2 季超過 200bp（比 Q3 的 180bp 快 10% 以上），論點削弱；連 3 季、或跌破 12.5%，論點反轉；任何普通股增發直接反轉"},{"id":"H3","text":"交叉購買飛輪：每會員產品數由 1.56 升到 2.0，費收型營收占比由 42% 升到 50% 以上，讓報酬率不再綁在個貸資產負債表上。","2y":null,"5y":null,"10y":"2030 年產品 1 億（現 2,670 萬）、費收占比 ≥50%；2035 年每會員產品數 ≥2.0","threshold":"每會員產品數每年增加 ≥0.05（Q3 年增 0.09）；FY2028 費收占比 ≥46%","source":"季度法說的會員、產品與費收型營收","drift_rule":"連續 2 個年度低於門檻，論點削弱；連續 3 個年度，論點反轉"}],"R":[{"id":"R1","text":"費收引擎卡住：大客戶流失的基期效應在 2027Q1 消失後，平台段仍回不到 2027 財測的 25% 成長；放款段占比繼續上升，費收占比停在 40% 上下。","h_ref":"H3","clock":"🔥","threshold":"平台段 2027Q1 到 Q2 年增 <10%，或放款段占調整後淨營收連兩季 ≥62%（Q3 為 59%）","evidence_refs":["end_markets#2","channel_business_model_shift#2","end_markets#5","substitute_technology#1"]},{"id":"R2","text":"會計與法律風險：放空報告質疑的公允價值計量，在 FY2026 年度查核中落地為重述、重大內控缺失或監理要求下修；或律所調查升級為已立案的證券集體訴訟。","h_ref":"H1","clock":"⚡","threshold":"10-K 出現重述或重大內控缺失，或公允價值查核事項附帶調整；集體訴訟立案","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"id":"R3","text":"升息下的消費信用轉弱：聯準會由降息轉為升息（今年已一次，年內預期再兩次，2027 再兩次），產業無擔保個貸逾期率走高，而個貸是放款段的主體。","h_ref":"H2","clock":"🔥","threshold":"個貸全口徑年化淨壞帳率連兩季 >4.5%；表內 90 天逾期率 >60bp（Q3 為 42bp）","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#5"]},{"id":"R4","text":"資本消耗比管理層說的快：CET1 由 2025 年底 22.8%、2026-06 的 18.7%，降到 2026-09 的 16.9%，總資本比單季降 180bp。若 2027 年中已貼近 13%，不增資的承諾就會被考驗。","h_ref":"H2","clock":"🔥","threshold":"總資本比 <12.5%，或宣布增發普通股","evidence_refs":["financial_regulatory_capital_rules#0"]},{"id":"R5","text":"放款定價被侵蝕：新進者與既有業者壓價搶份額（Upstart 放款年增 50%），個貸票息連幾季下滑，靠手續費補；存款端仍以高利率當獲客工具。","h_ref":"H1","clock":"🐢","threshold":"核心個貸風險調整後利差連兩季 <6.0%（以 Q3 口徑，Q3 約 7.6%）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]}],"single_thing":{"description":"個人貸款全口徑年化淨壞帳率（排除逾期貸款出售）任一季升破 5.0%；2026Q3 為 3.4%，去年同期約 4.2%。","why_fatal":"個貸是放款段的主體，放款段占調整後淨營收 59%。核心個貸風險調整後利差 7.6%＝票息 12.8%＋手續費 1.4%－資金成本 3.1%－損失 3.4%，損失每多 1.6 個百分點，利差就少兩成。更大的衝擊在公允價值：個貸帳面按 103.3% 標記，一旦上調損失假設，整本貸款會一次減值，直接打進當季損益與有形淨值。同時 LPB 資金方會縮手，資本比也會加速下滑。這四條傳導會同時發生，所以它是估值上最大的單一敏感項。","if_happens":"FY2027 EPS 往 0.6 以下修正，走空頭情境路徑，清倉。重新進場的條件改為壞帳連兩季回落到 4.0% 以下，並重跑完整研究。","how_monitor":"每季財報新聞稿與法說：個貸全口徑淨壞帳率、表內 90 天逾期率（Q3 為 42bp）、個貸公允價值標記。季與季之間看 TransUnion 無擔保個貸 60 天以上逾期率。","probability":"未來 12 到 24 個月約 15%。不利的一面：聯準會今年已升息一次、預期再升兩次，產業逾期率年增 44bp。有利的一面：SoFi 客群偏高收入，Q3 壞帳年降 80bp。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":19.53,"peg_fy2":0.7,"stress":{"pass":4,"total":8}},"eps_meta":{"base_eps_path":{"FY2025A":0.39,"FY2026E":0.61,"FY2027E":0.89,"FY2028E":1.14},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報）；FY2026E 起為 Koyfin 共識，與公司調整後 EPS 財測口徑一致（2026 為 0.61，2027 為 0.90），兩者口徑不完全相同"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"macro","event":"聯準會年內剩餘會議，管理層假設今年再升息","impact":"中","watch":"升息幅度與 2027 利率路徑；個貸資金成本"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026Q4 財報與 2027 財測更新","impact":"高","watch":"個貸全口徑淨壞帳率、總資本比、2027 EPS 0.90 是否維持"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"FY2026 年報查核意見","impact":"高","watch":"公允價值相關查核事項，以及有無重述或內控缺失"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"2027Q1 財報，平台段大客戶基期效應消失","impact":"中","watch":"平台段年增是否 ≥18%、ROTCE 是否 ≥11%"},{"date":"2027-12","date_precision":"month","type":"product","event":"SoFi Plus 100 萬付費會員目標期限","impact":"低","watch":"Q3 約 27.5 萬，管理層稱 Q4 成長已重新加速"}]}
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
