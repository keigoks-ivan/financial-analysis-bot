你是 DD 管線 v20 的判斷層閘（gate），標的 HON（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝4994 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝740 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝14.8 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi3_segment_margin`（q1_business）｜Segment margin（公司口徑調整後營業利益率）＝21.3 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi4_adjusted_eps`（q1_business）｜Adjusted EPS＝2.27 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi8_backlog`（q1_business）｜Backlog＝19000 USD m（近 19B）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_peer_hon_gross_margin_pct`（q2_moat）｜HON 毛利率＝36.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hon_operating_margin_pct`（q2_moat）｜HON 營業利益率＝16.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hon_fcf_margin_pct`（q2_moat）｜HON FCF 利潤率＝11.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_rok_gross_margin_pct`（q2_moat）｜ROK 毛利率＝54.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_rok_operating_margin_pct`（q2_moat）｜ROK 營業利益率＝19.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_rok_fcf_margin_pct`（q2_moat）｜ROK FCF 利潤率＝16.76 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sie_de_gross_margin_pct`（q2_moat）｜SIE.DE 毛利率＝39.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIE.DE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sie_de_operating_margin_pct`（q2_moat）｜SIE.DE 營業利益率＝12.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIE.DE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abbn_sw_operating_margin_pct`（q2_moat）｜ABBN.SW 營業利益率＝16.93 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abbn_sw_fcf_margin_pct`（q2_moat）｜ABBN.SW FCF 利潤率＝11.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝8.44 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.84 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝11.03 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝20158.86 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝20524.26 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.51 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（9.79 → 9.84）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.64 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（10.96 → 11.03）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi5_fcf`（q4_capital）｜自由現金流（FCF）＝688 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝14.1 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-22））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝10407.0 USD m｜期間與口徑：2026-10-24／yfinance 最新一季：總債務 16593.0、現金 6186.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.01 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝316.94 m shares｜期間與口徑：2026-10-24／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝80498.28 USD m｜期間與口徑：2026-10-24／市值 70091.28 ＋ 淨負債 10407.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝221.15 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.2 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 8.44，分子＝快照價 221.15｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝10.96 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.13 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.99 x｜期間與口徑：2026-10-24／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝66.35｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-0.24 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.81 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 8.29 → 8.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）

### findings_digest 中方向為負或來源衝突的條目（17 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：HON 10-K 列出各事業主要對手（航太：Garmin、L3Harris、Rolls Royce、RTX、Safran、Thales；樓宇：Johnson Controls、Schneider、Siemens；工業自動化：Emerson、Rockwell 等），並把新進入者與產品商品化列為可能造成市占下降、價格與毛利下滑的風險。
  - 來源：SEC EDGAR 10-K FY2025（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱公司須在對手數量不斷增加（含許多新進與非傳統對手）的情況下守住市占。
  - 來源：SEC EDGAR 10-K FY2025（as_of 2026-02-17）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：CSIMarket 顯示 Honeywell Aerospace 在其追蹤同業營收合計中的份額由 4.62% 降至 4.31%（商業資料庫，分母口徑未驗證）。
  - 來源：CSIMarket HON Competitors（as_of 2026-07-31）｜affects：moat_trend
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Honeywell Aerospace Q2 2026: orders +8% with book-to-bill 1.1 but output only +4%; supply chain constraints persist, 2026 organic growth guidance cut to 4-5%.
  - 來源：GuruFocus/MarketBeat, Honeywell Aerospace Q2 2026 earnings call highlights（as_of 2026-08-05）｜affects：thesis.R、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 披露國際營運（含美國出口）占銷售逾半，關稅與其他貿易限制若升高，可能衝擊競爭地位與財務表現；美國對中國等國關稅已引發報復性關稅，公司稱可能有重大不利影響，且無法保證完全抵銷
  - 來源：SEC EDGAR Honeywell 10-K FY2025（as_of 2026-02-17）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 稱美方持續對中國及其他國家商品加徵關稅並引發報復，公司已部署緩解策略，但不保證能完全抵銷
  - 來源：SEC EDGAR Honeywell 10-K FY2025（as_of 2026-02-17）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明航太事業多項主要零組件與原料為單一或唯一來源採購，關稅與貿易障礙可能影響關鍵供應商
  - 來源：SEC EDGAR Honeywell 10-K FY2025（as_of 2026-02-17）｜affects：moat_trend、thesis.R
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明俄烏衝突下美國與他國對俄、白俄實施制裁與出口管制，公司對俄方合約剩餘義務無法估計超出已提列準備的合理可能損失
  - 來源：SEC EDGAR Honeywell 10-K FY2025（as_of 2026-02-17）｜affects：decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年 Q1 10-Q 列出 2025 與 2026 年關稅、新貿易調查與談判造成市場波動，並提及關稅傳導增加供應鏈與成本壓力；摘錄未給中國專屬金額
  - 來源：SEC EDGAR Honeywell 10-Q (2026-03-31)（as_of 2026-04-30）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Honeywell 10-Q 揭露：營運處於中東衝突環境，影響能源市場、貿易流與航運；管理層稱正轉向在地/區域供應來源並對受限物料雙重採購，並警告地緣衝突、貿易政策變動與通膨可能對業績造成重大不利影響。
  - 來源：Honeywell Form 10-Q FY2026 (SEC)（as_of 2026-10-23）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Honeywell 10-Q 稱，對其製造或採購所在國家的關稅或貿易限制可能損害競爭地位與財務結果；Q1 2026 10-Q 並提及中東衝突、美國關稅授權法院裁決後的政策不確定性。
  - 來源：Honeywell Form 10-Q Q1 FY2026 (SEC)（as_of 2026-04-30）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 10-K 風險因子：供應商財務困難或交貨問題可能使公司無法滿足供應需求，導致銷售與利潤下降、合約罰則或終止；未找到指名單一供應商/零件為關鍵單點。
  - 來源：Honeywell Form 10-K FY2024 (SEC)（as_of 2025-02-13）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Aerospace 負責人 Jim Currier（2025年3月）稱機械類供應基礎「still very fragmented」「still very non-robust」，為持續性問題。
  - 來源：IndustryWeek: Honeywell aerospace CEO says supply chain problems persist（as_of 2025-03-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子列出成長取決於監控顛覆性技術與商業模式、防止產品商品化，並提及競爭者可能開發售後服務與零件；未點名具體替代技術。
  - 來源：SEC EDGAR 10-K FY2025（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：MarketBeat 稱 FY2026 EPS 指引 $8.05–$8.35 低於 $10.78 的分析師預估、營收指引 $19.8–20.0B 低於 $24.1B 共識，平均評級 Hold、共識目標價 $257.79；共識似為分拆前舊基準，尚未更新。
  - 來源：MarketBeat: Honeywell releases FY 2026 earnings guidance（as_of 2026-08-01）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Q1 2026 後 Barclays 將 12 個月目標價由 $255 降至 $243（4/24），維持 Overweight，理由為航太部門表現；來源為轉載站，品質偏弱。
  - 來源：轉載頁 Honeywell HON Sell-Side Analysts Trim Price Targets Post Q1 2026 Results（as_of 2026-05-01）｜affects：valuation
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：英國產品安全通報（2026-06-25）：Honeywell Lighting Controls UltraLite CDW4U1UL／CDW6U1UL 特定批次因黏著不良有觸電風險，召回換新。
  - 來源：GOV.UK Product safety alert（2606-0168）（as_of 2026-06-25）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":405.6,"bear_5y_price":155.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":31.0,"ev5y_pct":25.9,"irr_base_pct":5.6,"asym_ratio":2.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.44,"pe":26.2,"basis":"2026 共識調整後 EPS（Koyfin 快照），屬前瞻一年口徑，與終端倍數同口徑"},"eps":{"bull":[10.0,11.4,12.8,14.2,15.6],"base":[9.7,10.8,11.8,12.8,13.8],"bear":[8.9,9.1,9.3,9.5,9.7]},"pe":{"bull":26,"base":21,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.01,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HON_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年有機營收成長財測上修（原話："up from previous guidance of 2% to 3%"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年調整後 EPS 中點 8.20 美元（原話："We now expect full year adjusted earnings per share of $8.20"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年 segment margin 擴張幅度（原話："segment margin expansion of 250 to 290 basis points"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：年底 segment margin 水準（原話："exit the year above 22% segment margin"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年自由現金流（原話："expect free cash flow of roughly $2 billion in 2026"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：PA&T 自第三季起成長急遽轉折（原話："we expect a sharp inflection in growth"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：2027 展望較上月投資人日更強（原話："looking stronger versus when we talked even last month"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：中東營收與訂單全年預期（原話："orders should be about 40%"）
- 2026-07-23｜Vimal Kapur (CEO)｜guidance：第二季訂單成長與涵蓋範圍（原話："Orders grew 16% organically with broad-based demand"）
- 2026-07-23｜Vimal Kapur (CEO)｜guidance：中東假設情境（原話："we are assuming the situation remains as it is today"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：管理層認為仍有超越上修財測空間（原話："I also think there is more room"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：IA 第四季 segment margin 目標（原話："Pete will deliver a 22% margin rate in the fourth quarter"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：PA&T 第二季 margin 下滑口徑（原話："margin contracted 180 basis points to 22.1%"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：第二季稅率造成 EPS 逆風（原話："tax rate drove a $0.16 headwind"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：呆滯成本（stranded cost）較投資人日預期少約 2000 萬（原話："This is about $20 million better right now."）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：價格第二季漲幅（原話："Price was about 3.5%, 3.7% for the second quarter."）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：通膨黏性、價格僅涵蓋通膨（原話："but inflation is stubborn"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：整併重組費用全年估計（原話："around that $100 million, $110 million"）
- 2026-07-23｜Vimal Kapur (CEO)｜margin：60bp/年營運面利潤率擴張的組成（原話："we expect to drive 60 basis points a year of operational"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：三年承諾信心（原話："highly confident in our ability to deliver on our 3-year"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：三年 EPS 目標（原話："Collectively, this will drive approximately $12 of adjusted"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：現金轉換率目標（原話："we expect to improve our conversion to over 90%"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：2026 年先償債（原話："we are very focused to retire our debt"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：12 美元 EPS 不含併購（原話："There's not even single M&A assumed"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：軟體 ARR 2026 成長目標（原話："about 15% for 2026"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：JM Catalyst 收購倍數與綜效假設（原話："13x EBITDA with cost synergies, no sales synergies"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：Quantinuum 持股後續說明時程（原話："more color on our plans of our 47% ownership stake"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：M&A 第一優先為 IA 感測與量測（原話："strengthening our industrial automation, sensing"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：資料中心於 Building Automation 的占比（原話："that's 5% of the Building Automation business"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：資料中心現場發電商機尚未進訂單（原話："None of that is into our orders even yet"）
- 2026-07-23｜Mike Stepniak (CFO)｜customer：LNG 設備產能已被預訂（原話："we're sold out LNG for the next 3 years"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：中東以外專案增加（原話："We absolutely are seeing projects coming in."）
- 2026-07-23｜Vimal Kapur (CEO)｜product：IA 交貨準時率改善（原話："we were in mid-40s"）
- 2026-07-23｜Vimal Kapur (CEO)｜product：Forge 軟體 ARR 規模（原話："We are going to inch from about $900 million"）
- 2026-07-23｜Vimal Kapur (CEO)｜competition：對 BA 高個位數成長持續性的謹慎理由（原話："we are always cautious given competition can respond to"）
- 2026-07-23｜Vimal Kapur (CEO)｜risk：中東收款問題（原話："we observed some collection issues in pockets"）
- 2026-07-23｜Vimal Kapur (CEO)｜risk：BA 財測內含審慎成分（原話："there is a level of prudence"）

### HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md
- 2026-06-11｜Vimal Kapur｜guidance：三年有機成長承諾 4%–6%，並內建緩衝（原話："4% to 6% organic growth. We do have a contingency"）
- 2026-06-11｜Vimal Kapur｜guidance：IA 與 PA&T 中個位數、建築中到高個位數成長（原話："high single-digit growth is absolutely going to happen"）
- 2026-06-11｜Vimal Kapur｜guidance：市場約 3.5% 成長，公司目標高於市場 4%–6%（原話："Now we want to grow 4% to 6%"）
- 2026-06-11｜Mike Stepniak｜guidance：承諾 2029 年前 EPS 年增 10% 以上（原話："committing to delivering 10% plus EPS growth through 2029"）
- 2026-06-11｜Mike Stepniak｜guidance：2029 年 EPS 約 $6，稱為基本門檻（原話："the $6 EPS in 2029 of 10% drop, this is table stakes"）
- 2026-06-11｜Mike Stepniak｜guidance：2026 年 EPS $4.05 仍有超越空間（原話："the $4.05 for this year, there's still a lot of opportunity"）
- 2026-06-11｜Mike Stepniak｜guidance：明年 EPS 成長目標 12% 以上（原話："super disappointed in next year if we don't grow EPS by 12%"）
- 2026-06-11｜Mike Stepniak｜guidance：成長框架：量每年 4%（原話："we should grow 4% a year"）
- 2026-06-11｜Mike Stepniak｜guidance：定價三年內 3% 以上（原話："confident we'll deliver 3% plus pricing"）
- 2026-06-11｜Mike Stepniak｜guidance：併購貢獻約 1% 增量成長（原話："M&A will drive 1% incremental growth"）
- 2026-06-11｜Mike Stepniak｜guidance：保留大額緩衝因地緣風險頻繁（原話："we have a 100-year flood about every 6 months"）
- 2026-06-11｜Mike Stepniak｜guidance：確認隱含量成長約 2%、定價約 3%，並稱為超越空間（原話："that's really where the opportunity is for us to overdrive"）
- 2026-06-11｜Vimal Kapur｜guidance：定價 2026–27 年預期在 3%–4% 區間，並設 2% 緩衝（原話："why we show the hedge of 2%, right?"）
- 2026-06-11｜Mark Macaluso｜guidance：IR 描述 PA&T 下半年成長轉折至高個位數（原話："inflection in the back half to sort of high single-digit"）
- 2026-06-11｜Kenneth West｜guidance：PA&T 近幾季訂單出貨比高於 1.2（原話："higher than 1.2 book to bills over the past few quarters"）
- 2026-06-11｜Mike Stepniak｜guidance：催化劑短期需求下半年較上半年增逾 20%（原話："catalyst short-term demand is going to be up more than 20%"）
- 2026-06-11｜Mike Stepniak｜guidance：LNG 業務未來三年已售罄（原話："Our LNG business is sold out for the next 3 years"）
- 2026-06-11｜Billal Hammoud｜guidance：建築自動化 2025 年成長 8%、營收 74 億美元（原話："grow our top line by 8% to $7.4 billion"）
- 2026-06-11｜Billal Hammoud｜guidance：建築自動化展望為高個位數成長（原話："this business to grow at high single digits"）
- 2026-06-11｜Peter Lau｜guidance：IA 稱下半年與 2027 年看法樂觀、成長非後段集中（原話："I feel very bullish about the second half of 2026 and 2027"）
- 2026-06-11｜Peter Lau｜guidance：IA 三年營收中個位數成長（原話："this business is going to grow mid-single digits"）
- 2026-06-11｜Vimal Kapur｜guidance：服務與軟體 ARR 以約 15% 成長，基期約 10 億美元（原話："the ARR growth of 15% from a base of about $1 billion"）
- 2026-06-11｜Billal Hammoud｜margin：建築自動化 2025 年利潤率與三年目標 29%（原話："We see that going to 29% over the next 3 years"）
- 2026-06-11｜Billal Hammoud｜margin：建築自動化稱不需新建廠房即可支應成長（原話："without having to build a single factory"）
- 2026-06-11｜Billal Hammoud｜margin：定價與生產力持續高於通膨與投資（原話："productivity always exceeding inflation and investment"）
- 2026-06-11｜Peter Lau｜margin：IA 三年 segment margin 擴張 500 bps（原話："500 basis points of segment margin expansion"）
- 2026-06-11｜Peter Lau｜margin：對 500 bps 擴張的把握程度（原話："the margin expansion of 500 basis points, I go as far as a"）
- 2026-06-11｜Peter Lau｜margin：IA 利潤擴張僅靠低個位數成長即可（原話："feel like we could do that at low single-digit growth"）
- 2026-06-11｜Mike Stepniak｜margin：IA 重整使公司未來 12 個月貢獻 100 bps 利潤率（原話："going to deliver 100 bps of margin expansion for Honeywell"）
- 2026-06-11｜Mike Stepniak｜margin：2026 年 segment margin 約 20%（原話："we'll deliver about 20% segment margin this year"）
- 2026-06-11｜Mike Stepniak｜margin：結構性行動未來 12 個月擴張約 200 bps（原話："expand about 200 bps over the next 12 months"）
- 2026-06-11｜Mike Stepniak｜margin：有機每年再擴張 60 bps（原話："we'll expand another 60 bps a year"）
- 2026-06-11｜Mike Stepniak｜margin：24% 目標被稱為可超越（原話："24% is not only achievable, it's actually beatable"）
- 2026-06-11｜Mike Stepniak｜margin：滯留成本剩 2.9 億美元（原話："our stranded cost is only $290 million"）
- 2026-06-11｜Mike Stepniak｜margin：約 2 億美元滯留成本已啟動措施，待反映於 run rate（原話："actioned about $200 million of that through repositioning"）
- 2026-06-11｜Mike Stepniak｜margin：法人實體由約 700 個減至 300 個（原話："Over the next 2 years, we'll eliminate 400 legal entities"）
- 2026-06-11｜Mike Stepniak｜margin：ERP 由約 10 套整併為 2 套（原話："Today, we still have about 10 ERPs"）
- 2026-06-11｜Mike Stepniak｜margin：共享服務滲透率由約 40% 升至逾 70%（原話："our shared services penetration is about 40%"）
- 2026-06-11｜Mike Stepniak｜margin：固定成本占比 2025 至 2027 下降 500–600 bps（原話："is going down by about 500 to 600 bps from '25 to '27"）
- 2026-06-11｜Vimal Kapur｜margin：固定成本已降近 600 bps，目標維持 31%（原話："Now our job is to keep it at 31%"）
- 2026-06-11｜Mike Stepniak｜margin：利潤擴張不依賴強勁營收成長（原話："expansion is not dependent on the strong top line growth"）
- 2026-06-11｜Mike Stepniak｜margin：稱利潤擴張大致已去風險（原話："the margin expansion is largely derisked"）
- 2026-06-11｜Mike Stepniak｜margin：軟體增量利潤高，Forge 投入已減少（原話："We invested $1 billion in Forge"）
- 2026-06-11｜Vimal Kapur｜margin：PA&T 納入 Johnson Matthey 使基期利潤率偏低（原話："the Johnson Matthey acquisition. It pulls our margins down"）
- 2026-06-11｜Mike Stepniak｜margin：口徑：服務與軟體約 70 億美元占 40%，軟體 ARR 約 9 億美元（原話："software ARR is about $900 million"）
- 2026-06-11｜Vimal Kapur｜margin：口徑：軟體 ARR 以開立發票金額定義（原話："just report ARR, which is what we invoice"）
- 2026-06-11｜Jim Masso｜margin：口徑：PA 單一事業服務與軟體約 10 億美元 ARR（與 Vimal 全公司 10 億美元說法並陳）（原話："got around $1 billion of ARR"）
- 2026-06-11｜Vimal Kapur｜margin：口徑：vitality 定義為近三年新產品占比（原話："defined as products you created over the last 3 years"）
- 2026-06-11｜Peter Lau｜margin：口徑：IA 同時以淨新品 NPI 衡量，vitality 較大（原話："we measure it not just in vitality, but in net new"）
- 2026-06-11｜Vimal Kapur｜product：vitality 升至 40% 中段（原話："our vitality has been progressively growing to mid-40s"）
- 2026-06-11｜Vimal Kapur｜product：R&D 已提高約 50 bps，不再需要更多調整（原話："We are at the point we like it to be"）
- 2026-06-11｜Billal Hammoud｜product：2025 年 8% 成長中 4.5 個百分點來自新品（原話："4.5% came from new product introduction"）
- 2026-06-11｜Vimal Kapur｜product：連網資產 520 萬，預計 2028 年達 900 萬（原話："it will be 9 million conservatively by 2028"）
- 2026-06-11｜Kenneth West｜product：PA 系統連網比例僅 14%（原話："Only 14% of our systems are connecting"）
- 2026-06-11｜Vimal Kapur｜product：服務與軟體占營收由 40% 提高到 45%（原話："we want our services and software revenue to grow to 45%"）
- 2026-06-11｜Mike Stepniak｜product：軟體成長速度約為其餘業務 3 倍（原話："software is going to grow at about 3x the rest of the"）
- 2026-06-11｜Peter Lau｜product：IA 三年 R&D 再增 15%–20%（原話："we're going to do another 15% to 20%"）
- 2026-06-11｜Suresh Venkatarayalu｜product：CLSS 軟體組合 1.3 億美元，ARR 4,000 萬美元（原話："$130 million software portfolio with $40 million ARR"）
- 2026-06-11｜Billal Hammoud｜competition：建築產品組合以消防與安防為主，與 HVAC 設備商重疊較少（原話："Fire and Security being over 2/3 of what we sell"）
- 2026-06-11｜Peter Lau｜competition：IA 同業比較對象為 AMETEK、Teledyne、IDEXX 類（原話："AMETEK, Teledyne and IDEXX"）
- 2026-06-11｜Peter Lau｜competition：IA 無單一公司在所有領域競爭（原話："company that we compete with in every place that we play"）
- 2026-06-11｜Peter Lau｜competition：IA 過去四年份額流失（原話："As a result, we lost share."）
- 2026-06-11｜Vimal Kapur｜competition：工業與流程自動化自認前三、目標第一（原話："honest admission, we are top 3"）
- 2026-06-11｜Kenneth West｜competition：稱不陷入價格戰、較早切入專案（原話："We're not getting into a price war"）
- 2026-06-11｜Jim Masso｜competition：AI 與新軟體正在顛覆許多企業，公司稱其強化自身（原話："a lot of businesses are being disrupted by a lot"）
- 2026-06-11｜Vimal Kapur｜competition：離散自動化控制層目前未參與，保持彈性（原話："today, our position is open at this point"）
- 2026-06-11｜Billal Hammoud｜customer：建築自動化資料中心占比由 4% 升至 5% 以上（原話："And as we sit here it's operating well above 5%"）
- 2026-06-11｜Jim Masso｜customer：生命科學營收約 6 億美元（原話："around $600 million of revenue"）
- 2026-06-11｜Kenneth West｜customer：Dangote 將自動化合約由他人轉給公司（原話："he took contracts away from others for the automation side"）
- 2026-06-11｜Suresh Venkatarayalu｜customer：NVIDIA 園區試點客戶再給六週評估（原話："they've given us 6 more weeks"）
- 2026-06-11｜Billal Hammoud｜customer：通路占建築銷售逾 60%（原話："Our channels represent over 60% of our sales"）
- 2026-06-11｜Vimal Kapur｜customer：Forge 開放給通路夥伴，收取授權費（原話："When they sell it, they have to pay me a license fee"）
- 2026-06-11｜Vimal Kapur｜customer：跨事業交叉銷售未計入現有數字（原話："cross-sell built in because we haven't proven anything"）
- 2026-06-11｜Vimal Kapur｜customer：交叉銷售可能再貢獻 200 bps 成長（原話："200 basis point of growth in there is possible? Absolutely"）
- 2026-06-11｜Peter Lau｜customer：為提升客戶交付願多備庫存 2,000 萬美元（原話："putting in $20 million of extra inventory"）
- 2026-06-11｜Kenneth West｜risk：中東設施受衝擊，公司預期參與重建（原話："facilities across the Middle East that are our technology"）
- 2026-06-11｜Mike Stepniak｜risk：上半年自由現金流受中東衝突影響（原話："also the conflict in Middle East"）
- 2026-06-11｜Peter Lau｜risk：承認對 IA 轉型存在懷疑（原話："I wouldn't disagree with any skepticism"）
- 2026-06-11｜Vimal Kapur｜risk：客戶導入需組織調整，影響擴張速度（原話："our scaling is more dependent upon customer adoption"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：目標槓桿率年底前低於 3（原話："leverage ratio to below 3, hopefully by year-end"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：CapEx 約占營收 3%（原話："Our CapEx should be about 3% of sales"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：股利支付率約 35%（原話："Our dividend payout ratio should be about 35%"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：股數每年減少約 1%（原話："we'll focus on about 1% share count reduction"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：補強型併購規模 20–40 億美元（原話："bolt-on is about $2 billion to $4 billion"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：維持補強併購策略，2027 年前以降債為先（原話："stay on the bolt-on strategy in the optimal size"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：不改變以補強併購為主的策略，不排除任何選項（原話："you never say no to everything"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：下半年自由現金流轉換率逾 95%（原話："We will be 95-plus percent converter in"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：往後自由現金流轉換率約 95%（原話："convinced we are 95% free cash flow converter going forward"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：稅率降至約 19%（原話："tax rate going forward is about 19%"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：Quantinuum 持股帳面價值約 70 億美元（原話："is going to sit on our books at $7"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：適當時機再出售 Quantinuum 持股（原話："it will be the right time for us to monetize our stake"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：未來每年重整費用約 7,000–8,000 萬美元（原話："about $70 million to $80 million of repositioning"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：約 80 座工廠整併，25 座產出 80% 營收（原話："25 facilities will produce 80% of our revenue"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：Process 兩事業今年商業協同效益預計逾 1 億美元（原話："will deliver over $100 million of commercial synergies"）
- 2026-06-11｜Vimal Kapur｜commitment：CEO 稱立場一致、不改變主意（原話："I stay on course. I don't change my mind"）
- 2026-06-11｜Vimal Kapur｜commitment：高階主管薪酬將與承諾連動（原話："compensation should link to what we committed to you"）
- 2026-06-11｜Mike Stepniak｜commitment：對前兩年成果最有信心，最後一年打折（原話："I always discount the last year"）
- 2026-06-11｜Mike Stepniak｜commitment：聚焦未來 18 個月（原話："So it's really about next 18 months"）
- 2026-06-11｜Kenneth West｜commitment：服務由零起算可達數億美元（原話："several hundred million dollars of services business"）
- 2026-06-11｜Vimal Kapur｜commitment：不打算讓流程事業走通路（原話："We are not moving our process"）
- 2026-06-11｜Vimal Kapur｜product：敘事：業務團隊原集中於 Connected Enterprise，後改回四個事業部（原話："It turns out that thesis was wrong"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：不新增工廠，LNG 為唯一例外（原話："with one exception, LNG"）

### 問答異常語氣（迴避／改口／保留）
- HON_Q2_2026_Earnings_Call_20260723.md｜問：Deane Dray 問 JM Catalyst 重新議價降價的情境｜答法：未說明降價原因，稱屬正常談判並表示不想多談，轉而講策略與倍數
- HON_Q2_2026_Earnings_Call_20260723.md｜問：Alexander Virgo 問催化劑量下滑對 margin 的影響幅度及下半年反彈幅度｜答法：未給數字，只說明下半年量較正常及單季 mix 不可預測
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Sprague：已連網並有 ARR 的裝機基礎對有機成長貢獻幾個百分點｜答法：Ken West 以觸媒數位影像、PDH 客戶為例回答，未給成長點數
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Mitchell：IA 準時交貨等營運 KPI 改善速度｜答法：Pete Lau 談客戶滿意與庫存投入，稱以自由現金流利潤率、營業利潤與成長自評，未給 KPI 改善速率
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Coe：ARR 與經常性服務的增量利潤率、PA&T 2029 利潤率為何只到 25%｜答法：Mike 稱軟體增量利潤『really high』未給數字；PA&T 25% 由 Vimal 以 Johnson Matthey 基期作答
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Sprague：離散自動化與野戰儀器空白的策略優先順序｜答法：Vimal 談 IA 補強、垂直型併購與前沿技術，未回應離散自動化
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Linzey：AI 在自家工廠與營運的效益大小｜答法：Vimal 稱『hard for us to put a number on the table』，只說大於預期且高於 0

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 3 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Honeywell largest customer second source OR in-house 2026；Honeywell largest customer concentration Boeing Airbus supplier dual source insourcing 2026；Honeywell Aerospace customer second source supplier in-house avionics 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"PA&T「sharp inflection」是真實結構拐點，非一次性 backlog 錯位","columns":{"2Y 驗證點":"H2 2026 有機營收加速至高個位數","5Y 驗證點":"PA&T 5Y 有機 CAGR ≥ 中個位數，LNG/催化劑 backlog 持續轉換","10Y 驗證點":"能源轉型（renewable fuels/氫）成第二成長腿","具體數字門檻":"PA&T 訂單 +24-25%、BtB &gt;1.2x、LNG 專有設備「賣光 3 年」","來源":"2Y 假設：連 2 季 TTM 偏離 ≥5% → 削弱"}},{"id":"H2","text":"Building Automation 高個位數成長可持續（7 季連續）","columns":{"2Y 驗證點":"資料中心/醫療/hospitality 高成長 vertical 驅動 BA ≥ 中高個位數有機","5Y 驗證點":"BA 佔比提升 + 服務/軟體 ARR 拉高整體 margin","10Y 驗證點":"Niagara/BMS 平台成資料中心/樓宇標準","具體數字門檻":"Q2 BA +9% 有機、訂單 +13%、高成長 vertical 訂單 +50%、margin 27.1%","來源":"連 2 季 BA 有機 &lt; 中個位數 → 削弱"}},{"id":"H3","text":"純自動化重估：市場給 pure-play 自動化倍數（vs 舊 conglomerate 折價）","columns":{"2Y 驗證點":"Fwd PE 站穩 ~25x（peer 中段）而非回落至 conglomerate 18-20x","5Y 驗證點":"3 年 EPS target（~$12 by 2029）兌現支撐倍數","10Y 驗證點":"ROIC/margin 結構性上台階（exit &gt;22% → 24% target）","具體數字門檻":"賣方目標價中位 ≈ $247、Buy 評級;段 margin +90-100bps","來源":"連 4 季 EPS 共識下修 或 PE 回落 conglomerate 檔 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PA&T H2 拐點跳票（catalyst 出貨/backlog 轉換慢於承諾）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"PA&T 有機營收 QoQ/YoY","警戒閾值":"Q3 未轉正、連 2 季 &lt; 低個位數 → 減觀望信心"}},{"id":"R2","text":"Industrial Automation turnaround 失敗、EMR/ROK 續侵蝕份額","columns":{"對應假設":"H1/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"IA 有機成長 + 交付績效 %","警戒閾值":"交付績效自 ~80% 回落、有機成長轉負 → moat_trend 降 ↓"}},{"id":"R3","text":"能源 capex 見頂 + 中東地緣升級 + renewable fuels 政策逆風（45Z）","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"油氣資本開支週期 + 中東 collection + 45Z CI 計分規則落地","警戒閾值":"油氣 capex 下行 + 中東惡化 或 45Z 持續不確定使 renewable fuels 催化劑延後 → 需 ≥50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","irr_base_pct":8.0,"ev5y_pct":29.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.8,"ev5y_pct":29.0,"irr_base_pct":8.0,"max_dd_pct":-42.0,"bull_5y_price":416.0,"bear_5y_price":185.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","price_at_dd":246.27,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"HON","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Honeywell International Inc."},"oneliner":"分拆後的純自動化公司，Q3 有機成長 7%、全年指引三項全上修，但現價 26 倍今年獲利只換到約一成的年化獲利成長；等股價回到 216 美元以下，或 2027 年 2 月指引確認獲利路徑。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/scenario.json","answers":{"q1_business":{"verdict":"Honeywell 賺的是全球建築、能源與工廠業主的錢。利潤主要落在裝機之後的售後環節，包括消防與安防面板、控制系統、催化劑和服務的續購。","reasoning":"Q3 營收 49.9 億美元。三個分部如下：樓宇自動化 20.2 億美元，有機成長 8%；流程自動化與技術 18.6 億美元，有機成長 8%；工業自動化約 11.2 億美元（由總營收減去另兩個分部推算），有機成長 4%，帳面因出售業務年減 23%。GAAP 營業利益率 14.8%，公司口徑 segment margin 21.3%，年增 370bp。調整後 EPS 2.27 美元，年增 34%。backlog 近 190 億美元。單點依賴：10-K 稱銷售不實質依賴單一客戶，風險不在集中度。護城河證據是裝機基礎：Niagara 中介軟體超過百萬套，約 2 萬座流程工廠用 Honeywell 技術。產業時鐘判在擴張期，依據是能源專案在北美、中東、非洲與亞洲同時下單，資料中心訂單倍增，backlog 年增 7%。供需持久性屬週期性偏結構：LNG 與煉油專案跟著能源資本支出週期走；消防安防法規需求和資料中心偏結構性；供給端可逆性中等。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_segment_margin","f_kpi4_adjusted_eps","f_kpi8_backlog","f_earnings_recency"],"verdict_values":{"revenue_quality":"樓宇分部約占 40%，產品成長 11%、解決方案 4%；流程分部約占 37%，專案成長 14%、煉油催化劑 +80%，專案占比上升會拉低毛利結構；工業自動化約占 22%。軟體 ARR 今年接近 10 億美元，成長 12–13%。","unit_econ_note":"GAAP 營業利益率 14.8% 與 segment margin 21.3% 相差 6.5pp，差額是分拆成本、重整與攤銷等調整項。全年漲價約 4%，通膨約 350bp，價格與成本相抵後淨正約 30bp。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"分拆後的純自動化公司，靠裝機基礎帶動售後與軟體收入；流程分部受能源資本支出週期影響"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏結構：LNG 設備三年產能已被訂滿（2026-06-11 投資人日，Mike Stepniak），流程分部 backlog 年增超過 10%，但 Q3 法說也提到 Brent 高於 110 美元。消防安防與資料中心需求偏結構性。","bargaining":{"up":"上游是半導體、電子零件、銅與黃銅等通膨項目，公司以 3.5–4.5% 漲價抵銷，價格與成本相抵後淨正約 30bp。","down":"樓宇銷售六成以上經通路夥伴；流程端的大型專案業主（如 Dangote）議價力強，但裝機後的催化劑與服務會持續續購。","geo":"國際營運（含美國出口）占銷售一半以上，關稅和中東衝突是主要的地緣變數。"},"profit_pool_dir":"利潤池往軟體、服務與售後催化劑移動；服務加軟體目標由營收的 40% 提高到 45%。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM 與滲透率的分段資料；成長主軸是既有裝機的漲價、售後與專案轉換，不是新品類滲透，展開也沒有可引用的數字。"}}}},"q2_moat":{"verdict":"護城河方向持平","reasoning":"護城河機制是裝機基礎鎖定：換掉控制系統或消防平台要停機並重新驗證，所以售後、催化劑與軟體會跟著已裝設備續購。執行力在改善：工業自動化準時交貨率由不到 40% 升到 60%，樓宇連續 8 季高個位數有機成長，Q3 法說稱這是在拿份額。定價力穩定：價格成長 3.5–4.5%，抵銷通膨後仍淨正。扣分項有兩個：投資人日上 Peter Lau 承認工業自動化過去四年失去份額；10-K 稱對手數量持續增加、產品有商品化風險。同業 ROIC 不在事實表內，只能用利潤率比較。HON 近四季營業利益率 16.6%，Rockwell 19.8%、ABB 16.9%、西門子 13.0%；Rockwell 毛利率 54.5%，HON 36.6%。另外 HON 這四季數字含分拆前的航太，可比性有限。兩項評分都給 7 分，合併等級 B。產業態勢判為雙向拉鋸：競爭面，對手增加，且四大樓宇業者都在押注水平平台；結構面，能源專案多區域上行、資料中心訂單倍增；其他變數是關稅與中東衝突。","fact_refs":["f_peer_hon_gross_margin_pct","f_peer_hon_operating_margin_pct","f_peer_hon_fcf_margin_pct","f_peer_rok_gross_margin_pct","f_peer_rok_operating_margin_pct","f_peer_rok_fcf_margin_pct","f_peer_sie_de_gross_margin_pct","f_peer_sie_de_operating_margin_pct","f_peer_abbn_sw_operating_margin_pct","f_peer_abbn_sw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"裝機基礎鎖定：樓宇的消防安防面板與 Niagara 中介軟體、約 2 萬座流程工廠的控制系統與製程授權，帶出催化劑、服務與軟體續購。換系統需要停機、重新驗證並重新訓練人員。","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：工業自動化準時交貨率由不到 40% 升到 60%，逾期訂單減少 18%，樓宇連續 8 季高個位數成長。定價力穩定：漲價 3.5–4.5%，價格與成本相抵後淨正約 30bp。不過工業自動化過去四年失去份額、近期才止血，同業 ROIC 差距無資料可比，合判持平。","competitor_notes":[{"name":"ROK","strategy_note":"毛利率 54.5%，比 HON 高約 18pp，強項在離散自動化；Honeywell 在這一塊目前沒有參與，正面重疊集中在工業自動化。"},{"name":"SIE.DE","strategy_note":"以 Building X 爭奪樓宇平台層，營業利益率 13.0% 低於 HON，但研發密度 8.3% 高出約 3pp，是平台戰的主要對手。"},{"name":"ABBN.SW","strategy_note":"營業利益率 16.9%、FCF 利潤率 11.7%，與 HON 幾乎同一水準，在流程控制系統上正面競爭。"},{"name":"SU.PA","strategy_note":"以 EcoStruxure 押注同一個水平平台；事實表沒有它的財務數據，無法比較利潤率。"}],"peer_na_reason":"事實表沒有同業 ROIC，以利潤率代替。HON 近四季數字含分拆前的航太，和分拆後的結構不能直接比。","threats":[{"level":"🟡","text":"對手數量增加，包括新進者與非傳統對手，可能帶來產品商品化、壓低價格與毛利（10-K 自述）","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"樓宇軟體平台層之爭：JCI、西門子、施耐德都押注水平平台加生成式 AI，Honeywell 靠 Niagara 的裝機量防守；10-K 也列出要防範顛覆性技術與產品商品化","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"工業自動化對 Emerson、Rockwell 失去份額；2026-06-11 投資人日上 Peter Lau 承認過去四年失份額，轉機才剛開始","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"事實表沒有投入資本數據，推定為高利益率×低周轉（segment margin 21%，歷年併購帶來大量商譽）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"消防與安防有法規強制需求；流程控制是工廠安全運轉必需品，客戶要解決的問題長期存在。backlog 近 190 億美元、年增 7%。"},{"item":"決策層級","level":"🟢","text":"替代決策的最小單位是整座工廠或整棟建築的控制系統，換系統要停機、重新驗證並重新訓練人員。Q3 法說說明，升級與資安強化可以在線上完成，不必停機，裝機客戶受到保護。新建專案則是競標，屬另一回事。"},{"item":"價值鏈分配","level":"🟡","text":"樓宇有六成以上銷售經通路夥伴，通路分走部分價值；上游的半導體與金屬通膨約 350bp，漲價只比成本多出約 30bp，在價值鏈裡能守住分配，但擴張空間有限。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與工業業主，沒有消費者層面的政治價格上限；主要政策風險是關稅與出口管制，那是成本面的問題，不是定價上限。"}],"roiic":"事實表沒有增量投入資本。唯一能算的是 Johnson Matthey 催化劑技術的收購：買價約 13 倍 EBITDA（2026-07-23 Q2 法說），換算稅前 EBITDA 收益率約 7.7%，扣稅與折舊後報酬偏低，要靠成本綜效才能提高。","reinvest_rate":"事實表未涵蓋。資本支出約占營收 3%（投資人日），收購金額沒有收錄。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，兩個輸入都不在事實表內。成長題改用公司承諾的有機營收 4–6% 當替代上界。"}}}},"q3_growth":{"verdict":"五年後的成長跑道屬中等。成長來自漲價 3–4%、銷量約 2–4% 與 margin 擴張；資料中心與低碳燃料這兩條可能的第二曲線，規模還不足以撐起成長。","reasoning":"共識調整後 EPS：2026 年 8.44 美元、2027 年 9.84 美元、2028 年 11.03 美元，兩年年化約 14.3%。從分拆後的 2025 年基期約 6.48 美元起算，三年年化約 19%。基期是用 Q3 法說「全年獲利成長約 30%」，從 2026 指引中點 8.425 美元回推。共識營收 2027 年只比 2026 年多 1.8%（205.2 億對 201.6 億美元），獲利成長遠快於營收。內生上界：增量投入資本沒有資料，以有機營收 4–6% 當替代，約 5%。共識成長高出的部分歸因於 margin 擴張：呆滯成本 2026 年底清完，營運面每年擴張 60bp，公司費用降到約 4 億美元，利息費用也在下降。這不是再投資帶來的成長。第二曲線方面，資料中心訂單成長超過 100%，但只占樓宇分部約 5%；永續航空燃料已授權 100 個專案，只有約 20% 建成。兩者都還沒到能撐規模的程度，事實表也沒有滲透率資料，所以判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_backlog","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"價格約 4%（2026 年平均）＋銷量約 2–4%＋margin 擴張（呆滯成本清除、每年營運面 60bp）＋利息下降；2029 年 12 美元的目標不含併購。","runway_years":"事實表沒有滲透率資料，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"增量投入資本不在事實表內，內生上界以公司承諾的有機營收 4–6% 替代，約 5%。共識 EPS 年化 14–19% 和這個上界的差額歸因於 margin 擴張與利息下降，可以歸因，不屬於依賴重新評價。","segments":[{"item":"樓宇自動化","value":"Q3 營收 20.2 億美元，有機成長 8%，連續 8 季高個位數；segment margin 27%；高成長產業（資料中心、醫療、旅館）占 20%，其餘本業成長中個位數。"},{"item":"流程自動化與技術","value":"Q3 營收 18.6 億美元，有機成長 8%；專案 +14%，煉油催化劑 +80%；margin 由 22.2% 降到 Q4 預估 21.5%，原因是專案占比提高與 CT 併購稀釋；backlog 年增超過 10%。"},{"item":"工業自動化","value":"Q3 營收約 11.2 億美元（推算），有機成長 4%，帳面年減 23%（出售業務）；margin 18.4%，Q4 目標 22%，其中約 150bp 來自營運改善；核心訂單成長 15%。"}],"decay_signals":[{"signal":"EPS 成長顯著快於營收成長（差距超過 5pp）","lit":true,"evidence":"2027 共識 EPS 年增 16.6%，共識營收只增 1.8%；獲利成長靠成本結構。"},{"signal":"FCF 對淨利低於 0.75 連 2 年","lit":false,"evidence":"2026 FCF 指引 21 億美元，除以調整後淨利約 26.7 億美元（8.425 美元×3.17 億股），約 79%；前一年分拆後口徑不在事實表內。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"evidence":"Q3 約 2.1%（14.1%×7.4 億÷49.9 億）"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"樓宇連續 8 季拿份額；工業自動化失份額發生在過去四年，近期已止血。"}]}}},"q4_capital":{"verdict":"資本配置中等：2026 年先還債，之後以補強型併購為主，回購要等槓桿降下來。","reasoning":"Q3 FCF 6.88 億美元，現金轉換率 95%。全年 FCF 指引 21 億美元，約為調整後淨利的 79%，上半年受中東衝突與分拆影響。淨負債 104 億美元，目標年底總債務降到 130 億美元以下、毛槓桿低於 3 倍。股息殖利率 2.0%，投資人日設定配發率約 35%。股票酬勞約占 GAAP 營業利益的 14.1%，年化約 4.2 億美元，約占市值 0.6%。Johnson Matthey 催化劑技術以約 13 倍 EBITDA 買入，Q3 法說稱成本綜效高於原估，但收購 2026-07-17 才完成，報酬還無法驗證。管理層稱 2027 年起再看 20–40 億美元的補強併購，第一優先是工業自動化的感測與量測。Quantinuum 47% 持股帳面約 70 億美元，管理層說會擇時出售。","fact_refs":["f_kpi5_fcf","f_kpi6_sbc","f_kpi1_gaap","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Johnson Matthey 催化劑技術 2026-07-17 完成收購，買價約 13 倍 EBITDA（Q2 法說），還沒有實現報酬可以驗證；13 倍的倒數約 7.7%，是稅前現金收益率的起點，扣稅後不一定高於資金成本。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"2026 年資金優先還債（總債務年底降到 130 億美元以下），今年沒有回購可評；投資人日的目標是每年減少約 1% 股數。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 股票酬勞約占 GAAP 營業利益 7.4 億美元的 14.1%，約 1.04 億美元一季，年化約 4.2 億美元，占市值 701 億美元約 0.6%，低於每年 1.5%。淨稀釋要看股數年變化，事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主體是有機成長（2029 年 12 美元目標不含併購）；近三年現金去向四分與回購均價都不在事實表內。"}}}},"q5_valuation":{"verdict":"以現價 221 美元買進，需要 2026–2028 年 EPS 年化成長約 14%、2029 年接近 12 美元；就算倍數之後由 26 倍降到 21 倍，基本情境年報酬仍有約 8%。前兩年我相信，2029 年的目標我打折看。","reasoning":"前瞻本益比是今年 26.2 倍、明年 22.5 倍。兩年共識 EPS 年化 14.3%，PEG 約 1.8，在合理區間的偏上緣。近四季本益比只有 11 倍、EV/S 2.1 倍，看起來便宜，但分母含已經分拆出去的航太和分拆前的營收，不能當便宜的證據。前瞻 EV/S 是 4.0 倍。分拆前的歷史倍數和現在不可比，五年分位也無法使用。賣方平均目標價約 250 美元（2026-07 至 08 月，27 至 28 位分析師），較現價高約 13%。股價自上份研究以來下跌 10%，同期今年 EPS 上修 3%，倍數由約 30 倍降到 26 倍，估值由偏貴轉為中性。26 週股價報酬 −0.2%，RSI 66，動能沒有過熱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rsi14","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2026 共識調整後 EPS）＋ PEG（2026→2028 共識 EPS 年化）","tier":"大型多角化工業自動化","peers":{"expanded":false,"reason":"事實表沒有同業的前瞻本益比，只有利潤率對照，無法做倍數錨定。"},"fwd_pe":26.2,"peg":1.8,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"今年 26.2 倍、明年 22.5 倍；兩年共識 EPS 年化 14.3%，PEG 約 1.8，落在 1–2 的合理區間；分拆後只有一季可比的歷史倍數，五年分位不可用；賣方目標價約 250 美元，較現價高 13%。綜合判為中性。","upside_short_pct":12.9,"upside_mid_pct":14.7,"denominator_disputed":true,"denominator_note":"近四季本益比 11 倍與 EV/S 2.1 倍的分母，含已分拆的航太和分拆前營收（2025 年 374 億美元，分拆後今年約 200 億美元），而且 2026-06-29 還做了 1 比 2 反向分割，不能當便宜的證據。本研究一律用前瞻口徑。短期上檔以賣方平均目標 249.64 美元計算；中期上檔以 2028 共識 EPS 11.03 美元 × 23 倍 ≈ 254 美元計算。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方有三個。一是能源專案潮比管理層說的短；二是工業自動化的轉機停在低個位數成長；三是獲利成長主要靠成本、營收增速太慢，一旦 margin 擴張用完，倍數會下修。","reasoning":"價值陷阱的訊號亮了一個：2027 共識 EPS 年增 16.6%，營收只增 1.8%，獲利靠成本結構撐，所以判 🟡。其餘訊號沒有亮：FCF 轉換約 79%，股票酬勞約占營收 2.1%，樓宇仍在拿份額。下行路徑：今年 EPS 約 8.4 美元，倍數如果由 26 倍壓到 14–16 倍，股價約落在 125–157 美元。管理層改口的地方有兩處：軟體 ARR 成長由 15% 降為 12–13%，Q4 margin 由「高於 22%」改為「約 22%」。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"獲利增速遠超營收增速，靠成本結構撐"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.44,"pe":26.2,"basis":"2026 共識調整後 EPS（Koyfin 快照），屬前瞻一年口徑，與終端倍數同口徑"},"eps":{"bull":[10.0,11.4,12.8,14.2,15.6],"base":[9.7,10.8,11.8,12.8,13.8],"bear":[8.9,9.1,9.3,9.5,9.7]},"pe":{"bull":26,"base":21,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.01,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-45,"hi":-28,"basis":"熊市情境下，EPS 停在 8.9–9.84 美元，倍數由 26.2 倍壓到 14–16 倍。淺端：9.84 美元×16 倍÷221.15−1 ≈ −29%；中段：8.9 美元×16 倍 ≈ −36%；深端：8.9 美元×14 倍 ≈ −44%。範圍取 −28% 至 −45%，前份為 −42%。","trigger_time":null},"basis":{"bull":"能源專案上行延續到 2028 年，工業自動化回到中個位數成長，margin 每年擴張 80bp 以上，2029 年 EPS 超過 12 美元並繼續雙位數成長；倍數維持在今年水準。","base":"有機成長 4–6%，margin 每年擴張約 60bp，2029 年 EPS 約 11.8 美元，略低於公司 12 美元的目標；倍數降到 21 倍。","bear":"能源資本支出 2027 年見頂，工業自動化轉機失敗，關稅與通膨吃掉漲價空間，EPS 停在 9–10 美元；成長降到 5% 左右，倍數壓到 16 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 剔除去年同期大單後，訂單只成長 3%，book-to-bill 1.0；法說提到 Brent 高於 110 美元。10-Q 揭露中東衝突影響能源市場與航運。","assumption":"流程分部的多年成長期是結構性的，不是高油價帶來的一波專案潮。","consequence":"如果 2027–2028 年能源專案退潮，同時工業自動化轉機停住，EPS 會停在 9–10 美元，倍數壓到 16 倍，五年後股價約 155 美元，較現價下跌約 30%。","ruling":"部分採納。管理層提到非洲 Dangote 擴建、永續航空燃料授權專案只建成 20%、LNG 設備三年產能已訂滿，這些支撐需求的力量不只來自油價，所以不採全盤失敗；但熊市機率因此維持 30%。這條與唯一致命點部分重疊：唯一致命點監測的是 2027 指引，這條監測的是訂單。","watch":"流程分部訂單（剔除大型 LNG 案）年增率；book-to-bill 是否連兩季低於 1.0","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi8_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"GAAP 營業利益率 14.8%，segment margin 21.3%，差 6.5pp；股票酬勞約占營業利益 14%；每年重整費用約 7,000–8,000 萬美元。管理層稱 2027 年起做 20–40 億美元補強併購，CT 以 13 倍 EBITDA 買入。10-K 另稱對俄合約剩餘義務超出已提列準備的可能損失無法估計。","assumption":"調整後獲利能轉成股東拿得到的現金，降槓桿後省下的現金會用在高報酬的地方。","consequence":"營運目標全部達成，但調整項持續存在、併購以高倍數買入，每股自由現金流成長會比調整後 EPS 慢，股東實得報酬低於帳面成長。","ruling":"採納為監測項，不改結論。今年 FCF 轉換約 79%，Q4 管理層預期超過 100%；但 GAAP 與調整後的差距需要逐年縮小。","watch":"GAAP 營業利益率與 segment margin 的差距；新併購的 EBITDA 倍數是否超過 15 倍；全年 FCF 對調整後淨利是否低於 85%","evidence_refs":["reg_tariff_export#3"],"fact_refs":["f_kpi2_gaap","f_kpi3_segment_margin","f_kpi6_sbc","f_kpi5_fcf"]},{"view":"價格已反映太多","evidence":"今年 26.2 倍、明年 22.5 倍獲利；PEG 約 1.8；2027 共識營收只增 1.8%。","assumption":"市場會一直給純自動化公司的高倍數，不會回到多角化集團的折價。","consequence":"基本情境 EPS 到 13.8 美元，但倍數由 26 倍降到 21 倍，股價年化約 5–6%，加上股息約 8%，在中段偏弱。","ruling":"採納。這是等價格而不追價的主要理由；但現價只比進場價高約 2%，這個風險在價格上的差距不大。","watch":"股價對 2027 共識 EPS 的倍數；賣方目標價的方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_rev_consensus_fy2_m"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 246.27 → 本次 221.15（-10.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=246.27","side_b":"本次 price_at_dd=221.15","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 246.27 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 246.27 美元：Bull 價 416、Bear 價 185，五年期望值 +29.0%，基準年化 8.0%，不對稱比 2.8","side_b":"本次情境、股價仍用 246.27 美元：Bull 價 405.6、Bear 價 155.2，五年期望值 +13.0%，基準年化 3.3%，不對稱比 1.46","ruling":"先換情境、股價不動：五年期望值少 16.0 個百分點，基準年化少 4.7 個百分點。不對稱比由 2.8 變為 1.46。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 246.27 美元：五年期望值 +13.0%，基準年化 3.3%，不對稱比 1.46","side_b":"本次情境、股價 221.15 美元：五年期望值 +25.9%，基準年化 5.6%，不對稱比 2.33","ruling":"再換股價、情境不動：起點價下跌 10.2%，五年期望值多 12.8 個百分點，基準年化多 2.2 個百分點，不對稱比由 1.46 升到 2.33。合計五年期望值比前份少 3.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單動能：backlog 創高，但本季 book-to-bill 只有 1.0","cause":null,"side_a":"Q2 法說訂單有機成長 16%；投資人日稱流程分部 book-to-bill 高於 1.2；本季 backlog 年增 7%，接近 190 億美元。","side_b":"Q3 剔除去年同期一筆 7 億美元大單後，訂單只成長 3%，book-to-bill 1.0。","ruling":"可調和，屬程度差異。去年 Q3、Q4 各有一筆 7 億美元的低碳與 LNG 大單，本季比較基期偏高；流程分部 backlog 仍年增超過 10%。採 A 側，但把 Q4 訂單當作驗證點。","evidence_level":"公司新聞稿與法說（2026-10-22 Q3、2026-07-23 Q2、2026-06-11 投資人日）","settle_metric":"Q4 訂單剔除大型 LNG 案後的年增率","if_then":["若 Q4 剔除大單後的訂單年增達高個位數，維持流程分部的成長論點，進場價不變","若 Q4 剔除大單後的訂單年減，進場價下修到 2027 共識 EPS 的 20 倍（約 197 美元）"],"evidence_refs":[]},{"axis":"管理層承諾與改口：軟體 ARR 與年底 margin","cause":null,"side_a":"2026-07-23 Q2 法說：Vimal Kapur 稱 2026 年 ARR 成長約 15%；Mike Stepniak 稱年底 segment margin 高於 22%。","side_b":"2026-10-22 Q3 法說：Vimal Kapur 改稱今年 ARR 約 12–13%；Mike Stepniak 稱 Q4 margin 約 22%，流程分部降到 21.5%。","ruling":"可調和，屬程度差異的小幅改口。EPS、FCF、有機成長三項都上修，改口集中在軟體成長與流程分部的 margin。記為管理層可信度的扣分項，不改結論。","evidence_level":"兩場法說逐字稿","settle_metric":"2027 年指引中的 ARR 目標與 Q4 實際 margin","if_then":["若 2027 年指引把 ARR 成長目標降到 12% 以下，護城河中軟體這一項降為弱項","若 Q4 margin 達 22% 以上，視為承諾兌現"],"evidence_refs":[]},{"axis":"現在就買的最強論證，對照等價格","cause":null,"side_a":"全年指引三項全部上修，新指引低端已高於原本的高端；股價較上份研究下跌 10%，明年獲利倍數 22.5 倍；上份研究等待的流程分部拐點本季已經出現（有機成長 8%）。","side_b":"26 倍今年獲利只換到約一成的年化獲利成長，基本情境年報酬約 8%；成長多來自 margin 而不是營收（2027 共識營收只增 1.8%）；2 月的指引是二元事件。","ruling":"選擇等價格。基本情境報酬在 8% 上下，現價離進場價只差約 2%，不值得為這 2% 去承擔 2 月指引的二元風險。現在就買的論證有分量，所以進場價設在接近現價的位置。","evidence_level":"事實表估值與共識數字＋Q3 法說","settle_metric":"股價對 2027 共識 EPS 的倍數；2027-02 的指引","if_then":["若股價跌到 216 美元以下，先建 2% 試單","若股價沒有回落，但 2 月指引 EPS 中點達 9.6 美元以上、且 Q4 流程分部有機成長達 5%，以當時價格建 2% 試單","若指引中點低於 9.4 美元，取消進場價，等兩季數據後重做研究"],"evidence_refs":[]},{"axis":"前份漂移：估值、評等、裁決與角色","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份股價 246.27 美元，今年指引中點 8.20 美元，前瞻倍數約 30 倍，估值偏貴，評等 B，裁決為觀望。","side_b":"現價 221.15 美元，今年共識 8.44 美元，前瞻 26.2 倍、明年 22.5 倍，估值轉為中性；品質判斷不變。","ruling":"估值結論由偏貴改為中性，原因是股價下跌 10% 加上獲利上修 3%。綜合評等維持 B；裁決與角色由矩陣決定，預期仍是等價格觀察。","evidence_level":"事實表股價與共識快照","settle_metric":"前瞻本益比","if_then":["若股價回升到 245 美元以上而獲利沒有再上修，估值回到偏貴"],"evidence_refs":[]},{"axis":"前份漂移：陷阱、護城河方向、跑道、公司類型、循環位置","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱 🟢，護城河方向持平，五年後跑道 🟡，品質複利型，未判循環位置。","side_b":"本次：陷阱轉 🟡，因 2027 共識 EPS 年增 16.6%、營收只增 1.8%，差距超過 5pp；護城河方向維持持平（樓宇連 8 季拿份額，工業自動化過去四年失份額、剛止血）；跑道維持 🟡；類型維持品質複利型；循環位置仍不判。","ruling":"只有陷阱一欄改變，來源是事實表新收錄的分拆後共識營收。其他四欄有新證據，但不足以改判。","evidence_level":"事實表共識營收與 EPS；Q3 法說","settle_metric":"2027 實際營收與 EPS 成長差距","if_then":["若 2027 年有機營收成長達 5% 以上、獲利與營收的成長差距收窄到 10pp 以內，陷阱回到 🟢"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份牛市、熊市機率各 25%，最大回撤 −42%。","side_b":"本次牛市 25%、基本 45%、熊市 30%；最大回撤範圍 −28% 至 −45%。","ruling":"基本情境的獲利成長超過再投資能支撐的內生上界，差額靠 margin 擴張，因此熊市機率提高到 30%。回撤改用區間，並以熊市倍數壓縮推導。","evidence_level":"本次情境假設","settle_metric":"2027 margin 擴張幅度","if_then":["若 2027 年 margin 擴張達 60bp 以上且有機成長在 4–6%，下份可把熊市機率降回 25%"],"evidence_refs":[]},{"axis":"進場條件更動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","side_b":"股價 ≤216 美元（FY2027 共識 EPS 9.84 的 22 倍），觸及後進場試單 2%，2 月指引確認後再加碼到 4%。","ruling":"上份進場條件的後半「流程分部 Q3 確認高個位數拐點」已經發生（Q3 有機成長 8%、催化劑雙位數成長），約束只剩價格。2027 共識 EPS 由約 9.9 美元變為 9.84 美元，22 倍對應的價格由 218 改為 216 美元。","evidence_level":"Q3 新聞稿與法說；事實表共識","settle_metric":"股價對 2027 共識 EPS 的倍數","if_then":["若股價跌到 216 美元以下，進場試單 2%","若 2 月指引中點達 9.6 美元以上，加碼到 4%"],"evidence_refs":[]},{"axis":"出場指標新設","cause":"方法變動","prior_field":[],"side_a":"前份沒有設定獲利或營運的出場指標（空白）。","side_b":"本次設定四條：2027 指引 EPS 中點低於 9.4 美元，減碼一半；流程分部有機成長連兩季低於 3%；全公司 margin 連兩季年減；工業自動化有機成長連兩季低於 2%，減碼到 2% 以下。","ruling":"前份是觀察、不持有，所以沒有設出場指標。本次股價接近進場價，補上減碼的量化條件；四條都觸發時清倉。","evidence_level":"本次判斷","settle_metric":"各條指標的季報數據","if_then":["若四條中任兩條同季觸發，減碼一半","若四條全部觸發，清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":[],"side_a":"前份沒有設定唯一致命點（空白）。","side_b":"2027 年 2 月公布的 2027 全年調整後 EPS 指引中點低於 9.4 美元（較 2026 指引中點成長不到 12%）。","ruling":"Single Thing 設定為 2027 年指引。分拆完成後的第一份完整年度指引，是獲利路徑上最大的單一敏感項；CFO 在投資人日說過，明年 EPS 成長不到 12% 會非常失望。觸發時減碼一半。","evidence_level":"2026-06-11 投資人日 Mike Stepniak；Q3 法說","settle_metric":"2027-02 指引 EPS 中點","if_then":["若中點低於 9.4 美元，減碼一半，未持有則取消進場價","若中點達 9.6 美元以上，視為通過"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年指引的 EPS 中點低於 9.4 美元","type":"Single Thing","maps_to":"H3","metric":"2027 全年調整後 EPS 指引中點","threshold":"<9.4 美元","action":"減碼一半；未持有則取消進場價","source_freq":"公司財報，每年 2 月","date":"2027-02","evidence_refs":[]},{"n":2,"text":"股價回到 216 美元以下（2027 共識 EPS 的 22 倍）","type":"估值rearm","maps_to":"H3","metric":"股價÷FY2027 共識 EPS","threshold":"≤22 倍（約 216 美元）","action":"先建 2% 試單","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":3,"text":"Q4 流程分部有機成長達 5% 以上，訂單剔除大型 LNG 案後達高個位數成長","type":"假設驗證","maps_to":"H1","metric":"流程分部有機成長；剔除大單後的訂單年增","threshold":"有機成長 ≥5%；訂單 ≥7%","action":"確認後試單可加到 4%","source_freq":"季報","date":"2027-02","evidence_refs":[]},{"n":4,"text":"關稅與通膨讓價格成本淨效果轉負","type":"風險","maps_to":"R3","metric":"法說揭露的價格成本淨效果（bp）","threshold":"連 2 季為負","action":"停止加碼","source_freq":"季報法說","date":null,"evidence_refs":["reg_tariff_export#4","geo_supply_chain#1"]},{"n":5,"text":"工業自動化有機成長連兩季低於 2%","type":"減碼","maps_to":"R2","metric":"工業自動化有機成長","threshold":"連 2 季 <2%","action":"減碼到 2% 以下","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"Q4 財報與 2027 年指引公布後，重做研究","type":"複審日期","maps_to":"H3","metric":"2027 指引全項","threshold":"公布即複審","action":"重跑研究","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"2027 全年調整後 EPS 指引中點","bear_threshold":"<9.4 美元（成長不到 12%）","window":"2027-02 財報","source":"公司 Q4 2026 新聞稿","last_status":"unknown"},{"metric":"流程自動化與技術分部有機成長","bear_threshold":"連兩季 <3%","window":"2026Q4–2027Q2","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全公司 segment margin 年增幅","bear_threshold":"連兩季年減","window":"2027 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"工業自動化有機成長","bear_threshold":"連兩季 <2%","window":"2027 每季","source":"公司季報新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#2","reason":"這條講的是航太事業的份額，航太已在 2026-06-29 分拆，不再屬於本公司；而且來源是商業資料庫，分母口徑沒有驗證。"},{"ref":"supply_demand_durability#0","reason":"來源是 Honeywell Aerospace 的 Q2 2026 法說，這家公司分拆後已獨立上市，數據不屬於本公司的營運。"},{"ref":"reg_tariff_export#2","reason":"原文指出單一來源採購「particularly in Aerospace Technologies」，主要範圍是已分拆的事業；剩下三個分部的單一來源比重，原文沒有揭露。"},{"ref":"geo_supply_chain#3","reason":"這是 2025 年 3 月航太事業負責人談機械類供應商的說法，該事業已分拆，證據對象不是本公司。"},{"ref":"capital_markets_pricing#2","reason":"這條拿分拆後的指引去比分拆前的共識（EPS 10.78 美元、營收 241 億美元），基準不同，原文也自己註明共識還沒更新；而且引用的指引之後已上修到 8.40–8.45 美元。"},{"ref":"capital_markets_pricing#3","reason":"來源是轉載站，品質偏弱；降目標價的理由是航太部門表現，而航太已分拆，和現在的公司結構不同。"},{"ref":"product_recall_warning#0","reason":"通報只涵蓋英國兩款照明控制器的特定批次，沒有揭露數量和成本，無法連結到任何分部營收或 margin。"}],"action_conditions":{"rearm_trigger":"股價 ≤216 美元（FY2027 共識 EPS 9.84 的 22 倍）","exec_line":"觸及後先建 2% 試單；2027 年 2 月指引 EPS 中點 ≥9.6 美元且 Q4 流程分部有機 ≥5% 再加到 4%；指引 <9.4 美元則取消進場價並減碼一半"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤216 美元（2027 共識 EPS 22 倍），或 2027-02 指引 EPS 中點 ≥9.6 美元且 Q4 流程分部有機 ≥5%"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-0.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"流程自動化與技術進入多年成長期：能源專案（LNG、非洲與中東煉油、石化）會轉成營收，並帶動之後的催化劑與服務續購。","2y":"2026Q4 至 2027Q2 有機成長維持 5% 以上；2027 年催化劑中個位數成長","5y":"分部有機成長年化達中個位數以上，margin 從 2027 下半年起恢復擴張","10y":null,"threshold":"分部有機成長連兩季 ≥5%；分部 backlog 年增 ≥10%；2027 下半年 margin 年增轉正","source":"公司季報新聞稿與法說（分部有機成長、backlog、margin）","drift_rule":"連 2 季偏離門檻 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"},{"id":"H2","text":"樓宇自動化靠新品與資料中心維持高於市場的成長，消防與安防持續拿份額。","2y":"有機成長維持中個位數以上（目前已連 8 季高個位數）","5y":"margin 由 27% 走向 29%（投資人日目標），資料中心占比持續上升","10y":null,"threshold":"有機成長 ≥5%；margin 年增 ≥50bp","source":"季報分部數據；2026-06-11 投資人日 Billal Hammoud 的目標","drift_rule":"5 年期論點：連 4 季偏離 5% 以上視為削弱，連 6 季偏離 10% 以上視為反轉"},{"id":"H3","text":"分拆後成本結構上了一個台階，2029 年調整後 EPS 約 12 美元可以達成。","2y":"2027 年 EPS 指引中點 ≥9.6 美元；公司費用約 4 億美元；margin 每年擴張 60bp 以上","5y":"2029 年 EPS ≥11.5 美元（公司目標 12 美元打折計）","10y":null,"threshold":"2027 指引中點 ≥9.6 美元；全公司 segment margin 年增 ≥60bp","source":"2027-02 的 Q4 2026 財報；Q3 2026 法說 Mike Stepniak；2026-06-11 投資人日","drift_rule":"2 年期論點：連 2 季偏離 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"}],"R":[{"id":"R1","text":"流程分部的專案占比與 CT 併購稀釋，拖累 margin 的時間比管理層說的長。","h_ref":"H1","clock":"⚡","threshold":"Q4 分部 margin 低於 21.5%，或 2027 上半年 margin 年減超過 100bp","evidence_refs":[]},{"id":"R2","text":"工業自動化轉機失敗：對手持續增加、產品商品化，份額繼續流失。","h_ref":"H3","clock":"🔥","threshold":"工業自動化有機成長連 4 季低於 2%，或 Q4 margin 未達 22%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R3","text":"關稅、通膨與中東衝突讓價格成本轉負；國際營運占銷售一半以上，供應商也可能出問題。","h_ref":"H3","clock":"🔥","threshold":"價格成本淨效果連 2 季為負，或全公司 margin 年增轉負","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R4","text":"能源資本支出見頂：高油價帶來的專案潮在 2028 年前退去，訂單轉弱。","h_ref":"H1","clock":"🐢","threshold":"分部訂單（剔除大型 LNG 案）連 4 季年減且 book-to-bill 低於 1.0；機率達 50% 以上才砍倉","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月公布的 2027 全年調整後 EPS 指引中點低於 9.4 美元（較 2026 指引中點 8.425 美元成長不到 12%）。","why_fatal":"現價是今年 26 倍、明年 22.5 倍獲利，撐住這個價格的是 2027–2029 年每年雙位數的獲利成長、一路走到 12 美元。指引一旦低於 12% 成長，就跌破 CFO 在投資人日自己設的底線，倍數和獲利路徑會同時下修。這是情境樹裡敏感度最大的一項。","if_happens":"持股減碼一半；未持有則取消進場價，等 2027 上半年兩季的分部數據再重做研究。","how_monitor":"看 2027-02 的 Q4 財報與指引。在那之前看兩件事：Q4 訂單剔除大型 LNG 案後是否達高個位數成長，工業自動化 Q4 margin 是否達到 22%。","probability":"約 20%。呆滯成本已提前清完，Q3 上修後的指引低端已高於原本的高端，達標的可能性較高；風險在流程分部上半年的 margin 與通膨。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.5,"peg_fy2":1.6,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":6.48,"FY2026E":8.44,"FY2027E":9.84,"FY2028E":11.03},"fy_end_month":12,"eps_basis":"公司口徑調整後 EPS，採 2026-06-29 的 1 比 2 反向分割後股數與分拆後基準。FY2025A 是用 Q3 法說「全年獲利成長約 30%」，從 2026 指引中點 8.425 美元回推（8.425÷1.30）；2026–2028 為 Koyfin 共識。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年指引","impact":"高","watch":"EPS 中點達 9.6 美元以上為通過，低於 9.4 美元為唯一致命點"},{"date":"2027-02","date_precision":"month","type":"other","event":"Q4 訂單：剔除大型 LNG 案後的成長","impact":"中","watch":"管理層預期高個位數成長；book-to-bill 是否回到 1.0 以上"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新型燃氣表在多家公用事業的測試完成（測試期 6–9 個月）","impact":"低","watch":"2027 年起是否轉成大規模換裝訂單"},{"date":null,"date_precision":null,"type":"other","event":"Quantinuum 47% 持股變現","impact":"中","watch":"帳面約 70 億美元，管理層稱擇時出售；所得用於還債或回購"}]}
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
