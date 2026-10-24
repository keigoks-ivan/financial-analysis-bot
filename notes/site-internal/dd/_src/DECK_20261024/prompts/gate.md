你是 DD 管線 v20 的判斷層閘（gate），標的 DECK（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1481 百萬美元｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載，見 quarter 欄 URL）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：共識約 $1,510M，未達（來源：Zacks/Yahoo Finance 轉述）
- `f_kpi1_non_gaap_ieepa`（q1_business）｜Non-GAAP（剔除 IEEPA 關稅退款）營業利益率＝23.2 %｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：法說逐字稿（管理層口述 excluding refund benefit）；公司不另報 non-GAAP 營業利益（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：營業利益率共識未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝389.5 百萬美元（利益率 26.3%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載）；利益率 26.3% 見法說稿（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi3_gaap`（q1_business）｜毛利率（GAAP）＝60.5 %｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi7`（q1_business）｜品牌／通路＝HOKA $677.2M；UGG $786.4M 百萬美元｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載）（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi6_fy2027`（q1_business）｜管理層指引：全年 FY2027＝營收 $5.700–5.725B；EPS $7.80–7.95；毛利率約 58.5%；營業利益率約 23%；SG&A 約 35.5%；稅率約 23%；假設回購 $1.0B｜期間與口徑：Q2 FY2027 公告（2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（Business Wire 轉載）（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2027 公告（2026-10-22））
  - 註記：營收指引下修（HOKA 高個位數、UGG 低個位數成長，均較前次調降）；FY1 EPS 共識 7.73（見 consensus_revision，財報前快照）
- `f_peer_deck_gross_margin_pct`（q2_moat）｜DECK 毛利率＝57.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DECK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_deck_operating_margin_pct`（q2_moat）｜DECK 營業利益率＝22.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DECK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_deck_fcf_margin_pct`（q2_moat）｜DECK FCF 利潤率＝20.22 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DECK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_onon_gross_margin_pct`（q2_moat）｜ONON 毛利率＝64.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_onon_operating_margin_pct`（q2_moat）｜ONON 營業利益率＝13.79 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nke_gross_margin_pct`（q2_moat）｜NKE 毛利率＝43.16 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NKE.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nke_operating_margin_pct`（q2_moat）｜NKE 營業利益率＝8.28 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NKE.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_birk_operating_margin_pct`（q2_moat）｜BIRK 營業利益率＝24.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BIRK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_crox_operating_margin_pct`（q2_moat）｜CROX 營業利益率＝20.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CROX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi5_q3_fy2027`（q1_business）｜管理層指引：Q3 FY2027＝EPS $3.52–3.60；營收年增低個位數｜期間與口徑：Q2 FY2027 公告（2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：法說逐字稿（Motley Fool）（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027 公告（2026-10-22））
  - 註記：未取得
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.73 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.21 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝9.34 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_kpi8`（q4_capital）｜期末現金／存貨／回購＝現金 $1.210B；存貨 $860.8M；Q2 回購 $299.3M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載）（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi4_eps`（q4_capital）｜稀釋 EPS＝2.31 美元（剔除退款 $2.03，年增 11.5%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire 轉載）（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：Zacks 稱共識 $1.82 → 調整後 EPS 超預期；但 $1.82 同為去年同期 GAAP EPS，疑似轉述混淆，使用前須另行核對
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝81.09 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝10.49 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 7.73，分子＝快照價 81.09｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝2.93 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（7.51 → 7.73）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-1.44 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（8.33 → 8.21）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-1.27 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（9.46 → 9.34）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.66 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 7.53 → 7.73（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-25.28 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 81.09 / W52 98.68 / W104 117.13 / W250 102.88 / W250 13週斜率 0.36%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝102.88 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_w52`（q5_valuation）｜52 週均線＝98.68 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.37｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：公司 10-K 風險因子自述：面臨既有與新進入者競爭，HOKA 與 UGG 的能見度吸引了專攻這些品類的競爭者，離岸製造降低進入門檻，市占可能下滑。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-22）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：公司 10-K 自述已經歷並預期持續面臨定價與促銷壓力，競爭者加大折扣可能迫使其降價或加促銷。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-22）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Bernstein 給予 Deckers Underperform、目標價 $100，認為休閒鞋品類趨於萎縮。
  - 來源：Tiger Brokers 轉載 Bernstein（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：關稅假設由 10% 上調至 12.5%，管理層預期 Q2 毛利率受關稅與運費壓力；風險列有消費支出轉變、貿易政策、供應鏈中斷
  - 來源：Deckers Q1 FY27 earnings call highlights (MarketBeat)（as_of 2026-07-23）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Quince 於 2026-02 對 Deckers 提起反壟斷訴訟，指稱以 trade dress 訴訟企圖壟斷羊皮／羊毛內裡休閒鞋市場；2026-08 下旬聯邦法院駁回起訴書但准許修正。
  - 來源：The Fashion Law: Quince's Antitrust Case Against UGG Owner Deckers Hits an Early Hurdle（as_of 2026-08-31）｜affects：moat_trend、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 成品生產主要在越南與印尼，中國或任何其他單一國家不到 5%；關稅可能在有限通知下調整，公司揭露地理集中與關稅風險。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-22）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：毛利率下滑主因關稅，HOKA、UGG、Teva 皆受影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-05-22）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K：成品由外部製造商生產，主要在東南亞，以越南與印尼為主，中國或其他單一國家低於 5%；公司揭露集中度帶來貿易關係、關稅、政治不穩等風險
  - 來源：Deckers FY2026 Form 10-K (SEC)（as_of 2026-05-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K：UGG 羊皮主要自澳洲採購，並倚賴中國兩家製革廠供應多數羊皮，替代材料可能無法及時取得
  - 來源：Deckers FY2026 Form 10-K (SEC)（as_of 2026-05-30）｜affects：moat_trend、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：部分競爭者在財務、技術、製造、行銷與通路資源上遠大於 Deckers，能更快加速產品開發、運用數據分析或 AI、適應技術變化；Deckers 亦稱無法保證能成功適應技術變化。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-22）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Bernstein 給 Deckers Underperform、目標價 $100：稱 Hoka 緩衝技術已被競品複製、On 持續取得市占、Nike 跑鞋回歸構成威脅，UGG 休閒品類緩慢萎縮。
  - 來源：Tiger Brokers 轉載 Bernstein 報告（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：公司長期策略仍是提高 DTC 占比，但為擴大品牌認知與市占也擴張批發，批發占比在特定期間可能上升並壓低毛利率。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-05-22）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年 7 月財報後目標價下修：Telsey 由 $113 降至 $105，Needham 由 $138 降至 $125，Truist 降至 $105。
  - 來源：MarketBeat instant alerts（as_of 2026-07-24）｜affects：valuation、triggers
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Seeking Alpha 2026-03-20 顯示下一季估計過去 90 天修正偏空：2 上修、16 下修。
  - 來源：Seeking Alpha DECK earnings（as_of 2026-03-20）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":219.2,"bear_5y_price":67.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":73.4,"ev5y_pct":70.6,"irr_base_pct":11.6,"asym_ratio":8.5,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":7.73,"pe":10.49,"basis":"FY2027E（截至 2027 年 3 月）共識 EPS 7.73，快照可能早於 10-22 財報，含部分關稅退款。Y1–Y5 是 FY2028E 到 FY2032E；終端倍數套在 FY2032E，等於五年後的前瞻一年口徑，和現價倍數同源。每股 EPS 已含回購效果"},"eps":{"bull":[8.6,9.8,11.0,12.3,13.7],"base":[8.05,8.85,9.65,10.45,11.25],"bear":[6.9,6.7,6.9,7.2,7.5]},"pe":{"bull":16,"base":12.5,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":8.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DECK_Q1_2027_Earnings_Call_20260723.md
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 營收財測區間維持不變。（原話："range of $5.86 billion to $5.91 billion"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 毛利率預期上調至略高於 56.5%。（原話："now be slightly better than 56.5%"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 稀釋 EPS 財測上調 $0.05 至 $7.35–7.50。（原話："range of $7.35 to $7.50, which represents a $0.05 increase"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季合併營收預期年增約 5%。（原話："consolidated revenue up approximately 5% in Q2"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季 EPS 財測區間。（原話："earnings per share in the range of $1.73 to $1.78"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季毛利率預期下滑，原因為關稅與運費上升。（原話："gross margin is expected to be down due to tariffs and"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：下半年成長率預期加速。（原話："expect growth rates to accelerate in the second half"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：下半年加速主要來自 HOKA 與國際批發及經銷商業務。（原話："driven primarily by the HOKA brand and our international"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季其他品牌預期年減約 50%，歸因於精簡品牌組合。（原話："other brands are expected to be down approximately 50%"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：財測的前瞻關稅稅率假設由 10% 調高至 12.5%。（原話："go-forward tariff rate assumption to 12.5% from the"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：財測未納入任何關稅退款假設。（原話："not included any assumptions regarding refunds"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季毛利率 56.4%，年增 60 bps。（原話："Gross margin for the quarter was 56.4%, which is up 60"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：毛利率橋接：全價銷售加通路與品牌組合貢獻約 110 bps、匯率約 40 bps。（原話："about 110 basis points. And then FX, we benefited a little"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：毛利率橋接：第一季關稅造成約 150 bps 年增負面影響。（原話："impact of about 150 basis points."）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季折扣出清（closeout）管理較佳，約貢獻 60 bps。（原話："60 basis points."）
- 2026-07-23｜Steve Fasching (CFO)｜margin：管理層稱出清帶來的順風屬第一季獨有，其餘季度促銷節奏假設無重大變化。（原話："assumed any significant change in the promotional cadence"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：管理層預期其餘季度毛利率相較去年同期會有壓力。（原話："we will see some pressure on the gross margin"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季是全年四季中關稅年增逆風最大的一季。（原話："headwind in terms of the 4 quarters that we will experience"）
- 2026-07-23｜Stefano Caroti (CEO)｜margin：UGG 產品組合轉向帶動該品牌毛利率提升。（原話："favorable product mix shifts that supported higher gross"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季 SG&A 為 $420M，年增 13%。（原話："quarter was $420 million, which is up 13% from last year's"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：關稅稅率上調對毛利率的影響集中在第三季尾與第四季，未拆出金額。（原話："some impact to it in Q3 and more impact on a full Q4 basis"）
- 2026-07-23｜Steve Fasching (CFO)｜commitment：FY28 起開始釋放營業費用槓桿。（原話："begin delivering operating expense leverage in fiscal year"）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：維持拉式需求模式為核心承諾。（原話："preserving a pull model of demand and investing with purpose"）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：承諾維持高端全價的全球通路。（原話："maintaining a premium full-price global marketplace."）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：UGG 男裝目標佔營收 20% 以上（逐字稿記為 15% 的更正）。（原話："the goal is to get it to 20% or higher"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：第一季回購約 $338M，均價 $103.79。（原話："we repurchased approximately $338 million worth of shares"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：回購授權剩餘約 $4.7B。（原話："approximately $4.7 billion remaining"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：EPS 財測假設回購金額約為 FY27 自由現金流的 80%。（原話："equal to approximately 80% of our projected fiscal year"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：若收到關稅退款，將部分返還分攤成本的夥伴。（原話："return some of those funds to our partners"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：關稅退款預期非一次性入帳。（原話："We don't see it necessarily as a lump sum."）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：季末存貨 $808M，年減 5%。（原話："Inventory was $808 million, down 5% versus the same point"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 全球營收 +8% 至 $704M。（原話："first quarter increased 8% versus last year to $704 million."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 全球批發營收僅 +3%，管理層稱符合國際出貨時點差異預期。（原話："global revenue increased 3% versus last year, aligned with"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：Clifton PRO 上市約兩週已有帳戶補單。（原話："some accounts already placing reorders."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：Clifton PRO 採選擇性策略性批發分級，Clifton 11 走較廣批發配銷。（原話："PRO launched with selective strategic wholesale segmentation"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：EMEA 批發出貨實績與補單創季度紀錄。（原話："robust wholesale sell-through and another quarterly record"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：下半年 HOKA 依通路分級推出不同款式，含運動用品通路新款 Fly Pace。（原話："a new shoe for sporting goods called the Fly Pace."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 預期生活風格品類在下半年帶來更大貢獻。（原話："you'd like to see a bit more of an impact in the second"）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：管理層表示 UGG 訂單簿沒有取消。（原話："No, no cancellations to the order book, Laurent."）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：HOKA 下半年將新增運動用品等通路的優質夥伴，不給家數。（原話："to provide specific numbers, but you'll see an expanded"）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：管理層稱今年消費者買氣更偏事件驅動。（原話："I think we're seeing a bit more event-driven buying this"）
- 2026-07-23｜Stefano Caroti (CEO)｜competition：稱 HOKA 在效能跑鞋與越野跑鞋維持或取得市占。（原話："we continue to maintain or gain share in performance run"）
- 2026-07-23｜Stefano Caroti (CEO)｜competition：引用 Circana 資料稱 $120 以上價帶取得市占。（原話："we've gained share above $120, which is fantastic."）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：承認歐洲消費者壓力高於美國，起因為能源價格上升。（原話："consumer in Europe is probably a bit more pressured"）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：開場稱消費環境仍承壓。（原話："continue to see people showing up for the brands they love"）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：被問暖冬風險，稱即使暖冬仍預期持續表現。（原話："even if we had a warmer winter, we believe we will continue"）
- 2026-07-23｜Steve Fasching (CFO)｜risk：國際批發與經銷商出貨時點移至今年下半年，管理層稱是物流變動而非需求變動。（原話："It's not any change in assumption in demand, right?"）
- 2026-07-23｜Steve Fasching (CFO)｜risk：第二季受去年 Koolaburra 品牌收尾的基期影響。（原話："impact from lapping last year's wind-down of the Koolaburra"）

### 問答異常語氣（迴避／改口／保留）
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Peter McGoldrick 請 CFO 估算關稅假設由 10% 升至 12.5% 的影響（bps 或 EPS）｜答法：CFO 說「We haven't called it out」，未給金額，只說影響在第三季尾與第四季，建議分析師自行在模型中計算
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Sam Poser 問 HOKA 官網促銷與出清對第一季營收與毛利率的貢獻幅度｜答法：CFO 說「I'm not going to give you kind of specifics」，只說包含在毛利率超預期內、Clifton 為其中一部分
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Sam Poser 問 UGG 美國通路是否在收縮小客戶、調整配銷｜答法：CEO 先承認「you've seen some changes」，隨後稱策略不變、「no major changes」，未回應去年取消訂單的零售商是否被調整
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Rick Patel 問 HOKA 新增批發夥伴的據點數與對下半年加速的貢獻｜答法：CEO 表示不提供具體數字，只說下半年會有新夥伴與擴大配銷
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Laurent Vasilescu 追問第二季 HOKA 全球 DTC 成長如何看｜答法：CFO 兩次回答都停在「not a significant change」與「significant growth」，未給 DTC 成長數字
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Blake Anderson 問下半年 HOKA 的 DTC 與批發相對規模｜答法：CFO 只說加速來自物流時點，未回答批發是否會高於 DTC，也未給兩通路的幅度

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 4 | 1 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260706","verdict":"進場","role":"衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HOKA 維持低雙位 cc growth（從 $2.59B 走向 $3.5-4B），Q1 高單位為 wholesale timing 一次性","columns":{"2Y 驗證":"FY27 HOKA +低雙位（管理層 guide）；Q1 高單位後 Q2-Q4 回站 ≥ +10%","5Y 驗證":"HOKA 達 $3.8-4B（FY29-30）","10Y 驗證":"HOKA 全球 premium running share ~10-12%（vs 當前 ~23% run-specialty 並列 Brooks）","數字門檻":"HOKA quarterly cc growth ≥ 10%；全價銷售 ≥ 80%","來源":"Q4 FY26 法說 2026-05-21 / FY27 guide","漂移觸發":"連 2 季 ＜ 10% 削弱；連 3 季 ＜ 8% 反轉"}},{"id":"H2","text":"UGG 維持 mid-single mature 穩定（不從 +8% 滑入負成長）","columns":{"2Y 驗證":"FY27 UGG +mid-single；冬季 Q3 sell-through 穩","5Y 驗證":"UGG 維持 $2.8-3B 穩定","10Y 驗證":"UGG cozy boot 全球 share 維持 ~25-30%","數字門檻":"UGG cc growth ≥ +3%；Q3（冬季）＞全年 50%","來源":"FY26 +8% / FY27 guide mid-single","漂移觸發":"連 2 季 ＜ 0% 削弱；單季 ＜ −10% 反轉"}},{"id":"H3","text":"Tariff 可吸收，GM 維持 ≥ 55%（越南 75% 採購、20% 關稅、$185M 毛衝擊、~$75M 靠提價 offset）","columns":{"2Y 驗證":"FY27 GM ≥ 56%（guide 56.5%）","5Y 驗證":"5Y avg GM ≥ 55%","10Y 驗證":"結構性 GM ≥ 53%（即使 tariff 持續）＋ 越南採購降至 ＜ 70%","數字門檻":"季度 GM ≥ 55%","來源":"FY27 公司 guide 56.5% / 5/21 法說","漂移觸發":"連 2 季 ＜ 55% 削弱；連 2 季 ＜ 53% 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"HOKA 減速從一次性變結構性 — Q1 FY27 已掉到高單位，若非 wholesale timing 而是 On/Nike 搶走 race-day credibility → 掉低單位","columns":{"對應":"H1","時間尺度":"🔥 中期（2-4 季）","監測指標":"HOKA cc growth；run-specialty sell-through；international growth","警戒閾值":"連 2 季 cc ＜ 10% 削弱；連 3 季 ＜ 8% 反轉（trap 升 🔴）"}},{"id":"R2","text":"UGG 高 base 冬季反轉 — Q3+Q4 佔 UGG 75%+，若時尚輪替轉向 retro non-cozy → 佔 50% Rev 的品牌 YoY 轉 −5% ~ −15%","columns":{"對應":"H2","時間尺度":"🔥 中期（4-6 季，季節性）","監測指標":"UGG quarterly cc；冬季旺季趨勢；Gen Z sentiment","警戒閾值":"連 2 季 cc ＜ 0% 削弱；單季 ＜ −10% 反轉"}},{"id":"R3","text":"Tariff 升級至 25-30% — 越南 75% 集中，Trump 政府進一步上調風險，GM 結構性壓 100-150bp","columns":{"對應":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"US Trade Rep 通報；提價接受度；越南採購佔比","警戒閾值":"連 2 季 GM ＜ 55% / 越南採購未降 ＜ 70% 24 個月"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","irr_base_pct":9.6,"ev5y_pct":51.5,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星持倉","signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.0,"ev5y_pct":51.5,"irr_base_pct":9.6,"max_dd_pct":-40.0,"bull_5y_price":218.5,"bear_5y_price":86.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","price_at_dd":104.69,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"DECK","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Deckers Outdoor Corporation"},"oneliner":"HOKA 成長從雙位數掉到 7%，全年營收指引再下修；但全價紀律讓剔除退款營業利益率仍有 23%。10.5 倍前瞻本益比加上一年約一成市值的回購，價格已計入停滯，還缺 HOKA 重新加速的證據","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是消費者為 HOKA 與 UGG 兩個品牌付的溢價；錢卡在全價銷售的定價權。產業時鐘在收縮段：美國通路去庫存、促銷加劇，國際需求仍強","reasoning":"賺的是消費者為品牌付的溢價：HOKA 賣高價緩衝跑鞋，UGG 從羊皮靴延伸到休閒鞋、木屐和服飾。Q2 FY27 營收 $1,481M，其中 HOKA $677.2M（年增 7%）、UGG $786.4M（年增 4%），兩個品牌合計約占 99%。GAAP 毛利率 60.5%、營業利益率 26.3%；剔除關稅退款後營業利益率 23.2%，去年同期 22.8%。製造外包給越南、印尼的代工廠，品牌端拿走大部分價值，錢卡在全價銷售的定價權這一個節點。本季美國運動鞋促銷加劇，公司選擇不跟價，結果美國電商轉弱，營收靠批發與國際撐住。供需持久性屬週期性壓力，預期會反轉：美國通路庫存與促銷是一輪去化（2026-10-22 法說 CFO），國際需求仍強，APAC 增速最高；目前沒有證據顯示品類在結構性衰退。單點依賴：沒有單一客戶占營收 10% 以上，但有一家客戶占應收帳款 18.5%（前一年 13.6%）；UGG 羊皮依賴中國兩家製革廠加工。產業態勢是雙向拉鋸：競爭面在惡化（美國促銷、新進者、資源更大的對手）；結構面在國際市場與 $120 以上高價段轉好；另有關稅這個結構變數，IEEPA 退款屬一次性","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap_ieepa","f_kpi2_gaap","f_kpi3_gaap","f_kpi7","f_kpi6_fy2027"],"verdict_values":{"revenue_quality":"Q2 營收中 HOKA 約 46%、UGG 約 53%；批發占比上升、美國直營電商轉弱；全價銷售比重高，毛利率不靠折扣撐","unit_econ_note":"外包製造、資本輕；Q2 剔除退款後毛利率年增 120bp，全價銷售與產品組合各貢獻一半（2026-10-22 法說 CFO）","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利品牌鞋業，外包製造，自由現金流約八成用於回購，放大每股盈餘"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性壓力、預期反轉：美國運動鞋通路庫存偏高、促銷加劇，消費者集中在促銷檔期購買（2026-10-22 法說 CFO 與 CEO）；國際需求仍強","bargaining":{"up":"代工集中在越南、印尼，代工廠分攤關稅成本（退款按分攤比例扣除後才入帳），品牌對代工有議價權","down":"沒有單一客戶占營收 10% 以上，但單一客戶占應收 18.5% 且無擔保；批發占比上升，零售夥伴的促銷會外溢到品牌自營電商","geo":"成品主要在越南、印尼生產，中國或其他單一國家低於 5%；UGG 羊皮由中國兩家製革廠加工"},"profit_pool_dir":"高價段（$120 以上）利潤池往有創新的品牌集中，HOKA 在這段持續拿份額；$120 以下價帶競爭加劇，HOKA 可能流失（2026-10-22 法說 CEO）","tam_table":{"expanded":false,"reason":"證據包沒有 TAM、滲透率與利潤池占比；HOKA 份額只有管理層引 Circana 的質性說法（$120 以上價帶居首），沒有可展開的數字"}}}},"q2_moat":{"verdict":"護城河方向 →：定價力穩定，但 HOKA 執行力在縮減，兩者互抵；等級 B","reasoning":"機制是品牌溢價加全價紀律：拉式需求、控制配銷。證據包沒有同業 ROIC，可證方向改用營業利益率差距：DECK TTM 營業利益率 22.67%，高於 On 的 13.79%、Nike 的 8.28%、Crocs 的 20.73%，略低於 Birkenstock 的 24.94%；毛利率 57.8%，僅次於 On 的 64.82%。資料只有一期，無法判斷差距在擴大還是收窄。執行力評 7，方向縮減：HOKA 成長從 FY26 Q3 的 +18% 降到 Q2 FY27 的 +7%；CEO 承認 Transport、Kawana、Solimar 等新款沒打中；歐洲物流也出了問題。定價力評 8，方向穩定：在促銷環境下，剔除退款後毛利率仍年增 120bp；$120 以上價帶份額持續增加；Bondi 9 仍以全價持續售出。一縮一穩，方向判 →，等級 B。報酬持續期：稅後營業利益率約 17.5%（22.67% × 稅後 77%，用 23% 的稅率指引）。投入資本周轉率證據包沒有；以外包製造、存貨 $861M 對年營收約 $5.7B 推斷，屬高利益率×高周轉。再投資率接近零：TTM FCF 利潤率 20.22% 高於稅後營業利益率，表示淨再投資接近零或為負，公式算出的內生成長上限也接近零。實際成長來自費用化的行銷與產品開發，多出來的現金透過回購還給股東","fact_refs":["f_peer_deck_gross_margin_pct","f_peer_deck_operating_margin_pct","f_peer_deck_fcf_margin_pct","f_peer_onon_gross_margin_pct","f_peer_onon_operating_margin_pct","f_peer_nke_gross_margin_pct","f_peer_nke_operating_margin_pct","f_peer_birk_operating_margin_pct","f_peer_crox_operating_margin_pct","f_kpi1_non_gaap_ieepa","f_kpi7"],"verdict_values":{"moat":{"mechanism":"品牌溢價加全價紀律：控制配銷與上市節奏（如 Bondi 換代前先清乾淨舊款），不參與促銷；外包製造讓資本報酬維持高檔","execution":7,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力縮減：2026 年部分新款反應不佳，HOKA 成長從雙位數降到 7%，Q3 預告只剩低至中個位數。定價力穩定：促銷環境下剔除退款毛利率仍年增 120bp，$120 以上價帶份額持續增加（2026-10-22 法說）。兩者互抵","competitor_notes":[{"name":"ONON","strategy_note":"毛利率 64.8% 高於 DECK，但營業利益率只有 13.8%；Bernstein 稱它持續拿份額，是 HOKA 高價跑鞋最直接的對手"},{"name":"NKE","strategy_note":"毛利率 43.2%、營業利益率 8.3%，遠低於 DECK；Bernstein 認為它在跑鞋的回歸是 HOKA 的威脅"},{"name":"BIRK","strategy_note":"營業利益率 24.9%，略高於 DECK；同樣靠品牌稀缺與全價策略，適合當 UGG 的利潤率對照"},{"name":"CROX","strategy_note":"營業利益率 20.7%，略低於 DECK；同樣從單一招牌鞋款擴到多品類，可對照 UGG 的延伸路徑"}],"peer_na_reason":"證據包沒有同業 ROIC 與投入資本，只有利潤率；改以營業利益率差距當可比軸","threats":[{"level":"🟡","text":"HOKA 被複製：緩衝技術已被同業跟進，On 持續拿份額，Nike 跑鞋回歸；資源更大的對手能更快開發產品，也更能運用資料分析與 AI。這是點對點的品牌競爭，不是生態替代","p":"35%","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"促銷壓力：公司在 10-K 自述已經歷、也預期持續面臨定價與促銷壓力；美國運動鞋通路庫存偏高","p":"50%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"UGG 原料集中：羊皮主要來自澳洲，由中國兩家製革廠加工；替代材料不帶相同商標","p":"10%","evidence_refs":["geo_supply_chain#1"]},{"level":"🟡","text":"Quince 提起反壟斷訴訟，挑戰 UGG 的外觀設計權。2026 年 8 月下旬遭法院駁回，但准許修正後再提；若最終勝訴，UGG 經典款防堵仿品的能力會變弱","p":"10%","evidence_refs":["regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是消費者本人，三個角色一致。但這是可以延後的非必需品：2026-10-22 法說指出消費者改成需要時才買，並集中在促銷檔期，購買急迫性下降。跑鞋與冬靴的需求本身是持久的"},{"item":"決策層級","level":"🟡","text":"替代發生在每一雙鞋的購買決策上，轉換成本接近零，品牌偏好是唯一的黏著力。HOKA 在 $120 以上價帶持續拿份額，但 $120 以下可能流失（2026-10-22 法說 CEO）"},{"item":"價值鏈分配","level":"🟢","text":"品牌端拿走大部分價值：TTM 毛利率 57.8%，Nike 是 43.2%；代工廠還分攤了關稅成本。議價缺口有兩個：批發占比上升，以及 UGG 羊皮集中在兩家製革廠"},{"item":"社會容忍度","level":"🟢","text":"屬非必需品，也不依賴監管授權，漲價沒有社會面的上限；政策風險在關稅（越南、印尼生產），不在價格管制"}],"roiic":"無法計算：投入資本與歷年增量投入，證據包都沒有","reinvest_rate":"約 0% 或為負：TTM FCF 利潤率 20.22% 高於稅後營業利益率約 17.5%","endo_ceiling":null,"formula_note":"內生成長＝增量 ROIC × 再投資率。再投資率接近零，公式算出的上限也接近零。品牌鞋業的成長投入（行銷、產品開發、門市）多半費用化，公式會低估實際成長能力；本檔改用實際營收成長加回購來拆解每股成長"}}}},"q3_growth":{"verdict":"五年後成長空間中等：HOKA 在運動用品通路鋪貨仍少、國際市場還早，但美國核心跑鞋已不再是雙位數；UGG 已成熟。每股成長主要靠回購","reasoning":"成長動力以量為主（HOKA 擴大鋪貨、國際市場），價格為輔（全價銷售、選擇性漲價），每股層面靠回購，沒有併購。FY27 全年營收指引 $5.700–5.725B，比 FY26 的 $5.472B 多約 4%；HOKA 高個位數、UGG 低個位數，兩者都比前次下修。Q3 預告 HOKA 只有低至中個位數，全年數字因此隱含 HOKA 在第四財季加速，加速全部押在 Bondi 10、Fly Pace 等新品。三年共識 EPS 從 FY2026A 的 7.02 到 FY2029E 的 9.34，年複合約 10.0%；共識家數證據包沒有。公式算出的內生成長上限接近零，共識與上限之間約 10pp 的缺口可以歸因：回購每年約 8–10% 市值（$1B 對約 $10B 市值），加上小幅營業利益率改善與費用化的品牌投入；不是無法歸因。過去三年每股盈餘年複合約 29.6%，遠高於營收約 14.7%，來自毛利率從 50.3% 升到 57.7% 加上回購，未來難以重演","fact_refs":["f_kpi6_fy2027","f_kpi5_q3_fy2027","f_kpi7","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_peer_deck_fcf_margin_pct","f_peer_deck_operating_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量（HOKA 擴大鋪貨、國際市場）為主，價格（全價銷售、選擇性漲價）為輔；每股層面靠回購；沒有併購","runway_years":"證據包沒有滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"再投資率接近零（TTM FCF 利潤率 20.22% 高於稅後營業利益率約 17.5%），公式上限接近零；共識約 10% 的每股成長主要靠淨回購（年約 8–10% 市值）補足","segments":[{"item":"HOKA Q2 FY27","value":"$677.2M，年增 7%；批發 +9%（$444M），直營 +4%（$234M）；美國直營受促銷拖累"},{"item":"UGG Q2 FY27","value":"$786.4M，年增 4%；批發 +7%（$641M），直營 −8%（$146M）；Q2 以進貨為主，旺季在 Q3"},{"item":"其他品牌","value":"Q2 年減 54%，主因 Koolaburra 收尾的基期效應"},{"item":"FY27 全年指引","value":"HOKA 高個位數、UGG 低個位數；Q3 HOKA 低至中個位數、UGG 低個位數"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q1 年增 60bp；Q2 剔除退款年增 120bp"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"CEO 稱 $120 以下價帶可能流失份額（2026-10-22）"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"2025 年 7 月起選擇性漲價，管理層稱沒看到明顯的銷量下滑"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY2023–FY2026 EPS 年複合約 29.6%，營收約 14.7%"},{"signal":"FCF 對淨利低於 0.75","lit":false,"evidence":"約 1.08 倍"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":null,"evidence":"證據包沒有 SBC 資料"},{"signal":"TAM 萎縮或被替代","lit":false,"evidence":"只有 Bernstein 單一賣方稱休閒品類萎縮，沒有量化證據"},{"signal":"產業估值倍數下移","lit":null,"evidence":"證據包沒有同業倍數歷史"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律佳：無負債，自由現金流高於淨利，大部分現金拿去回購；缺點是回購均價高於現價","reasoning":"FCF 對淨利的轉換約 1.08 倍：TTM FCF 利潤率 20.22%，FY26 淨利率約 18.7%。兩者期間差一季，只看量級。期末現金 $1.210B，沒有借款；存貨 $860.8M，年增 3%，和營收成長 3.5% 相當，沒有堆積。現金去向以回購為主：FY27 上半年回購 $637M，約占流通股 5%；Q1 $338M 均價 $103.79，Q2 $299.3M 均價 $93.65；剩餘授權約 $4.4B，全年假設回購 $1.0B。沒有股息、沒有併購、沒有債要還；資本支出與 SBC 證據包沒有。用上半年 $637M 約占 5% 回推，流通股約 1.2–1.3 億股，現價市值約 $10B，$1B 回購約等於一成市值。營運槓桿：Q2 營收 +3.5%，剔除退款營業利益率升 40bp，沒有壓縮。缺點：回購均價比現價高 15–28%，已經買進的股票目前帳面上是虧的","fact_refs":["f_kpi8","f_kpi4_eps","f_peer_deck_fcf_margin_pct","f_kpi1_non_gaap_ieepa","f_kpi0_gaap","f_kpi6_fy2027"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 唯一的重大項目是信貸協議修訂，沒有併購"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"Q1 均價 $103.79、Q2 均價 $93.65，用 FY1 共識 EPS 7.73 換算，買入收益率約 7.4%–8.3%。十年期公債殖利率證據包沒有：只要殖利率低於約 5.4% 就算通過，本判定以此為前提"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"證據包沒有 SBC 金額。回購讓流通股半年減少約 5%，淨股數在下降，但算不出毛稀釋率"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購（近 12 個月沒有併購公告）；資本回饋以回購為主，金額與均價已寫在現金配置的判讀裡"}}}},"q5_valuation":{"verdict":"現價只要求 EPS 不衰退：就算淨利零成長，回購也能讓每股盈餘年增高個位數。回購這一半我信；FY3 共識的加速，我不完全信","reasoning":"現價 $81.09，對 FY1 共識 EPS 7.73 是 10.5 倍。FY1 含約 $0.52 的一次性關稅退款（Q2 $0.28、Q3 預估約 $0.24）；剔除後用指引中點約 $7.36 算，約 11 倍。用 FY2 共識 8.21 算是 9.9 倍。三年共識 EPS 從 FY2026A 的 7.02 到 FY2029E 的 9.34，年複合約 10.0%，PEG 約 1.05。這個價格只要求 EPS 不衰退：淨利零成長、每年回購約 8% 市值，每股盈餘仍能年增高個位數。回購這一半我信；共識 FY3 的加速我不完全信，FY2、FY3 共識本週各下修 1.4% 和 1.3%。短期上檔：FY2 EPS × 12 倍＝$98.5（+21.5%）。中期上檔取 Base 情境第五年的 $140.6（+73.4%）。五年估值分位與同業本益比證據包沒有；改用自身倍數對照：前份 7 月股價 $104.69，以 7 月底共識 7.53 算約 14 倍，倍數已壓縮約四分之一","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_kpi6_fy2027","f_kpi4_eps","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 與 FY2）；PEG 用 FY2026A 到 FY2029E 的三年共識 EPS 年複合成長","tier":"高利潤品牌鞋業","peers":{"expanded":false,"reason":"證據包的同業只有利潤率、沒有本益比，做不了倍數對照；終端倍數改用公司自身 2026 年 7 月約 14 倍當對照，同業倍數的缺口已在情境假設中註明"},"fwd_pe":10.49,"peg":1.05,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"FY1 前瞻本益比 10.5 倍，剔除一次性退款約 11 倍，FY2 口徑 9.9 倍；三年共識 EPS 年複合約 10%，PEG 約 1.0。比 7 月時約 14 倍再壓縮約四分之一，判便宜。五年估值分位證據包沒有，未納入","upside_short_pct":21.5,"upside_mid_pct":73.4,"denominator_disputed":false,"denominator_note":"FY1 共識含約 $0.52 的一次性關稅退款，快照也可能早於 10-22 財報；剔除後本益比約 11 倍，前瞻錨改用 FY2 的 8.21（9.9 倍）。分母本身不是爭點，爭點在 FY2 之後 HOKA 能不能加速"}}},"q6_how_wrong":{"verdict":"最可能看錯的是 HOKA：新品週期若救不回成長，10 倍本益比就是價值陷阱的起點。目前衰退訊號亮兩個，陷阱風險中等","reasoning":"可能看錯的路徑有三條：①HOKA 新品週期失靈（即唯一致命點）；②UGG 冬季旺季賣不動、補單不如去年；③促銷與批發占比上升，侵蝕全價紀律。股價已在 250 週均線 $102.88 與 52 週均線 $98.68 之下，26 週跌 25%；RSI 43，不過熱。最大回撤區間 −30% 至 −45%，推導見情境假設，路徑風險中等偏高。十類衰退訊號亮兩類：過去三年 EPS 年複合約 29.6%，遠高於營收約 14.7%；$120 以下價帶份額可能流失。毛利率與 FCF 轉換都沒亮。空方最強論證來自 Bernstein（休閒品類萎縮、HOKA 被複製）與 BMO 9 月以 Underperform 開始追蹤，賣方最低目標價 $70","fact_refs":["f_week26_return_pct","f_ma_state","f_ma_w250","f_ma_w52","f_rsi14","f_kpi7"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長減速型：利潤率與現金流沒壞，衰退訊號亮兩個"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":7.73,"pe":10.49,"basis":"FY2027E（截至 2027 年 3 月）共識 EPS 7.73，快照可能早於 10-22 財報，含部分關稅退款。Y1–Y5 是 FY2028E 到 FY2032E；終端倍數套在 FY2032E，等於五年後的前瞻一年口徑，和現價倍數同源。每股 EPS 已含回購效果"},"eps":{"bull":[8.6,9.8,11.0,12.3,13.7],"base":[8.05,8.85,9.65,10.45,11.25],"bear":[6.9,6.7,6.9,7.2,7.5]},"pe":{"bull":16,"base":12.5,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":8.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-45,"hi":-30,"basis":"現價已比前份 $104.69 跌 23%，26 週跌 25%。Bear 終點 9 倍 × 7.50＝$67.5（−17%）。下緣：Bear 倍數打八折為 7.2 倍，乘 Bear 最低年 EPS 6.70，約 $48（−41%），再留一點緩衝。上緣：Bear 最低年 EPS 6.70 × 8.5 倍，約 $57（−30%）。區間取 −30% 至 −45%","trigger_time":null},"basis":{"bull":"HOKA 新品週期成功，FY2028 回到低雙位數；UGG 靠品類延伸維持中個位數；剔除退款營業利益率回到 23–24%，每年回購約 7%。終端 16 倍：同業倍數證據包沒有，以公司 7 月約 14 倍為對照","base":"HOKA 高個位數、UGG 低個位數。FY2028 扣掉一次性退款後 EPS 約 8.05，之後靠回購與小幅營益率改善，每年約 9% 成長。終端 12.5 倍，低於 7 月的約 14 倍","bear":"HOKA 份額流失、成長降到中低個位數，UGG 年減，促銷把營業利益率壓到約 18%，回購只能抵銷淨利下滑。終端 9 倍，接近現價剔除退款後的倍數再折價"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Bernstein 稱 HOKA 緩衝技術已被複製、零售商對這波趨勢疲乏、On 持續拿份額、Nike 跑鞋回歸；2026-10-22 CEO 也承認 Transport、Kawana、Solimar 等新款沒打中","assumption":"HOKA 的高價跑鞋地位是可以持續的品牌優勢，不是一輪潮流","consequence":"五年後 HOKA 停滯、UGG 隨流行退燒，促銷把營業利益率壓到 15–17%；EPS 回到約 $5.5，給 9 倍，股價約 $50（−40%）","ruling":"部分採納：已反映在 Bear 30% 的機率與唯一致命點（兩者部分重疊）。不全採的理由：Bernstein 的觀點早於 FY26 Q3 HOKA +18% 的那一季；管理層引 Circana 稱 $120 以上份額仍在增加；Q2 全價銷售還讓毛利率上升","watch":"HOKA 季度成長、$120 以上份額說法、新品全價售出率","evidence_refs":["competitive_share_entrants#3","substitute_technology#2"],"fact_refs":["f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"公司長期目標是提高直營占比，但為了擴大份額持續擴張批發（FY26 批發 +12.3%，快於直營 +6.3%）；HOKA 推出 $115 的入門款並擴大運動用品通路。上半年回購均價 $93.65–103.79，高於現價","assumption":"HOKA 回到成長的同時，不稀釋品牌、不犧牲毛利率","consequence":"營收成長回來，但靠的是批發與低價帶，毛利率回落 100–200bp，每股盈餘成長低於營收成長；高價買進的回購，實際創造的每股價值也低於回購金額","ruling":"列為監測項：Q2 批發成長、毛利率仍上升，暫不扣分；剔除退款毛利率連 2 季年減就觸發","watch":"剔除退款毛利率的年變化、批發占比、Fly Pace 銷售占比","evidence_refs":["channel_business_model_shift#1"],"fact_refs":["f_kpi1_non_gaap_ieepa","f_kpi8"]},{"view":"價格已反映太多","evidence":"7 月財報後賣方下修目標價：Telsey $113→$105、Needham $138→$125、Truist 降到 $105。FY1 共識 7.73 含約 $0.5 的一次性關稅退款；FY2、FY3 共識各下修約 1.4% 和 1.3%","assumption":"現價 10.5 倍是真便宜，而不是盈餘基期被一次性項目墊高造成的假象","consequence":"若 FY2 共識再下修 10% 到約 7.4，本益比約 11 倍，和今年剔除退款後的 EPS 幾乎一樣，等於兩年零成長","ruling":"反駁：剔除退款後仍約 11 倍，FY2 口徑 9.9 倍；即使走 Bear 路徑，EPS 6.9 × 9 倍也只到 $62（−23%）。價格已經反映的是停滯，不是成長","watch":"FY2 共識修正方向、賣方目標價中位數","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 104.69 → 本次 81.09（-22.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=104.69","side_b":"本次 price_at_dd=81.09","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟡→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星持倉 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟡→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 104.69 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 104.69 美元：Bull 價 218.5、Bear 價 86，五年期望值 +51.5%，基準年化 9.6%，不對稱比 6.0","side_b":"本次情境、股價仍用 104.69 美元：Bull 價 219.2、Bear 價 67.5，五年期望值 +32.1%，基準年化 6.1%，不對稱比 2.57","ruling":"先換情境、股價不動：五年期望值少 19.4 個百分點，基準年化少 3.5 個百分點。不對稱比由 6.0 變為 2.57。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 104.69 美元：五年期望值 +32.1%，基準年化 6.1%，不對稱比 2.57","side_b":"本次情境、股價 81.09 美元：五年期望值 +70.6%，基準年化 11.6%，不對稱比 8.47","ruling":"再換股價、情境不動：起點價下跌 22.5%，五年期望值多 38.5 個百分點，基準年化多 5.6 個百分點，不對稱比由 2.57 升到 8.47。合計五年期望值比前份多 19.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"HOKA 成長論點與門檻","cause":"新證據","prior_field":["signal","moat_trend"],"side_a":"前份：HOKA 維持低雙位數成長，Q1 的高個位數只是批發出貨時點造成的一次性；門檻是季度成長 ≥10%","side_b":"本次：Q1 +7.7%、Q2 +7%；全年指引從低雙位數降到高個位數，Q3 預告低至中個位數；CEO 承認 2026 年部分新款反應不佳。門檻下修為 ≥8%","ruling":"採本次證據：前份 H1 已經削弱，出貨時點一次性的說法不成立。門檻從 10% 改為 8%，是依管理層新指引重新定錨，不是放寬標準。定價力沒有受損（剔除退款毛利率年增 120bp），護城河方向維持 →，品質訊號維持 B；進出場結論與倉位角色交給估值與均線重新判定","evidence_level":"公司新聞稿加上法說中管理層口述","settle_metric":"HOKA FY27 第四財季營收年增率（2027 年 5 月公布）","if_then":["若 HOKA 第四財季年增 ≥5%，且 FY2028 指引 ≥ 高個位數 → 維持論點，可分批加碼到 3%","若 HOKA 第四財季 <5%，且 FY2028 指引 ≤ 中個位數 → 減碼一半，H1 改判為反轉"],"evidence_refs":["substitute_technology#2"]},{"axis":"管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-07-23 法說：CFO 說 FY27 營收 $5.86–5.91B 維持不變，下半年加速主要來自 HOKA 與國際批發，國際出貨移後不是需求假設改變；CEO 說 UGG 訂單沒有被取消","side_b":"2026-10-22：營收下修到 $5.700–5.725B，HOKA 高個位數、UGG 低個位數；歐洲第三方物流延遲約 $22M，其中部分可能被取消；UGG 不再假設有去年那樣的補單","ruling":"不可調和（方向相反），採 10-22 的新說法。三個月前歸因為物流時點，現在變成全年下修，管理層對短期能見度的判斷要打折。歐洲物流延遲維持為未證實的一次性因素，並先寫下證偽條件","evidence_level":"兩場法說的管理層原話","settle_metric":"下一季是否再揭露履約延遲；HOKA 第四財季是否如指引加速","if_then":["若 Q3 FY27 法說再揭露歐洲或其他物流延遲 → 一次性歸因視為證偽，下修 EMEA 成長假設並停止加碼","若 Q3、Q4 都達到指引且沒有新的延遲 → 恢復對管理層指引的正常信任，不再額外打折"],"evidence_refs":[]},{"axis":"價值陷阱、成長空間與公司類型","cause":"新證據","prior_field":["trap","runway_post_y5","archetype","cycle_position"],"side_a":"前份：價值陷阱 🟡、五年後成長空間 🟡、品質複利成長、非循環股（沒有循環定位）","side_b":"本次維持同樣的判讀。衰退訊號亮兩個：過去三年 EPS 年複合約 29.6%，遠高於營收約 14.7%；$120 以下價帶份額可能流失。HOKA 在批發與國際仍有擴張空間，UGG 在延伸品類；利潤率高、沒有負債，仍屬品質複利型，但信心降為中","ruling":"四欄都不變：成長減速還沒讓衰退訊號累積到三個以上。但若 HOKA 連 3 季低於 5%，陷阱判讀升為 🔴、成長空間降為 🔴","evidence_level":"年度財報與法說","settle_metric":"HOKA 與 UGG 季度營收年增率","if_then":["若 HOKA 連 3 季 <5% 或 UGG 連 2 季年減 → 陷阱改判 🔴、成長空間改判 🔴","若 HOKA FY2028 回到 ≥8% → 維持 🟡"],"evidence_refs":[]},{"axis":"估值結論與回撤範圍","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份：股價 $104.69（約 14 倍 FY1）判便宜，最大回撤預估 −40%","side_b":"本次：股價 $81.09，26 週跌 25%，前瞻本益比 10.5 倍（剔除退款約 11 倍），判便宜，而且比前份更便宜；最大回撤改成區間 −30% 至 −45%","ruling":"估值結論不變，股價下跌讓倍數壓縮約四分之一。回撤改用區間表示，下緣用極端 Bear（7.2 倍 × 6.70，約 $48）推出","evidence_level":"收盤價與共識快照","settle_metric":"FY2 共識 EPS 與股價","if_then":["若 FY2 共識下修超過 10% → 重算 Bear 下緣","若股價先漲過 $100 而 HOKA 證據還沒出現 → 不追"],"evidence_refs":[]},{"axis":"情境機率","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份 Bull 25%、Bear 25%","side_b":"本次 Bull 25%、Base 45%、Bear 30%","ruling":"Bear 機率上調 5pp：HOKA 成長門檻已破、管理層改口，而且共識的每股成長要靠回購才補得上，超出資本再投資能支撐的內生成長，所以 Bear 不低於 30%","evidence_level":"法說加財報推算","settle_metric":"FY2028 財測","if_then":["若 FY2028 HOKA 指引 ≥ 高個位數 → Bear 機率降回 25%","若 FY2028 HOKA 指引 ≤ 中個位數 → Bear 機率升到 40% 並減碼一半"],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","side_b":"HOKA 單季營收年增回到 ≥5%（先看 FY27 第四財季），且週收盤站回 250 週均線 $102.88","ruling":"重新進場的條件改寫。舊條件的價格那一半已被跌破（現價 $81.09），而 HOKA 並沒有回到低雙位數，舊條件失效。新條件依新指引把 HOKA 門檻下修到 ≥5%，並加上 250 週均線確認；兩者同時成立才重跑判斷、首倉進場。另設：跌破 $70 且門檻未破時，可先試單加碼","evidence_level":"法說指引與週線價格","settle_metric":"HOKA 第四財季營收年增率、週收盤價","if_then":["若兩條件同時成立 → 重跑判斷後首倉 2%","若只有價格站回、HOKA 沒達標 → 不追"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份沒有設 Single Thing（null）","side_b":"Single Thing：2027 年 5 月的 FY2028 財測給出 HOKA 全年成長 ≤ 中個位數","ruling":"新設 Single Thing：HOKA 是唯一的成長引擎，它的成長指引是對 EPS 路徑與終端倍數影響最大的單一變數；一旦發生就減碼一半，若 UGG 冬季同時年減則清倉","evidence_level":"法說指引","settle_metric":"FY2028 HOKA 成長指引","if_then":["若發生 → 減碼一半","若同時 UGG 冬季年減 → 清倉"],"evidence_refs":[]},{"axis":"停損指標","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份沒有設停損門檻（null）","side_b":"HOKA 季度年增連 3 季 <5%；剔除退款的年度營業利益率 <20%；UGG 連 2 季年減","ruling":"新設三條：任一條觸發就減碼一半，兩條同時觸發就清倉。門檻來自本次 HOKA 指引下修與全價紀律能不能守住","evidence_level":"季報與法說","settle_metric":"三條指標每季更新","if_then":["任一條觸發 → 減碼一半","兩條同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"現在就買或等待","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：剔除退款仍只有 11 倍本益比，沒有負債，FCF 約為市值 11%；公司一年回購約一成股本，還有 $4.4B 授權。同業在促銷時毛利率反升 120bp，證明定價力沒壞；只要 EPS 不衰退，倍數回到 12–13 倍就有 15–20% 空間","side_b":"現在不買的最強論證：管理層三個月內從只是物流時點，改口成下修全年；HOKA 已連兩季低於 8%，下一季預告更低，第四財季的加速全押在新品。股價在 250 週均線之下，賣方目標價持續下修，價格趨勢和基本面一起轉弱","ruling":"兩邊都成立，結論是等證據：估值給了安全邊際，但成長引擎還在驗證期。不追，等 HOKA 第四財季回到 ≥5% 再進；跌破 $70 且門檻未破，可先試單","evidence_level":"財報、法說與價格","settle_metric":"HOKA 第四財季營收年增率","if_then":["若 2027 年 5 月 HOKA 第四財季 ≥5%，且週收盤站回 $102.88 → 重跑判斷，首倉 2%","若股價先漲過 $100 而 HOKA 證據還沒到 → 不追","若股價跌破 $70 而 HOKA、UGG 門檻都沒破 → 分批試單 1%（不是停損邏輯）"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"HOKA 第四財季（2027 年 1–3 月）營收年增是否回到 ≥5%","type":"假設驗證","maps_to":"H1","metric":"HOKA 季度營收年增率","threshold":"≥5%","action":"達標就維持論點，可分批加碼到 3%；沒達標就停止加碼","source_freq":"季報新聞稿／每季","date":"2027-05","evidence_refs":["substitute_technology#2"]},{"n":2,"text":"UGG 冬季旺季（Q3 FY27）營收能否守住正成長","type":"假設驗證","maps_to":"H2","metric":"UGG 季度營收年增率","threshold":"≥0%","action":"若年減，減碼三分之一","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":3,"text":"FY2028 財測中 HOKA 全年成長 ≤ 中個位數","type":"Single Thing","maps_to":"single_thing","metric":"HOKA FY2028 成長指引","threshold":"≤ 中個位數（約 ≤5%）","action":"減碼一半；若 UGG 冬季同時年減則清倉","source_freq":"年度財測","date":"2027-05","evidence_refs":[]},{"n":4,"text":"剔除關稅退款的毛利率連 2 季年減（促銷與批發占比擴大侵蝕定價力）","type":"風險","maps_to":"R2","metric":"剔除退款毛利率的年變化","threshold":"連 2 季 <0bp","action":"停止加碼，護城河方向改判 ↓","source_freq":"法說／每季","date":null,"evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#1"]},{"n":5,"text":"公司關稅稅率假設從 12.5% 再上調，或剔除退款毛利率跌破 55%","type":"風險","maps_to":"R3","metric":"關稅稅率假設／剔除退款毛利率","threshold":">12.5%／<55%","action":"減碼三分之一","source_freq":"法說／每季","date":null,"evidence_refs":["reg_tariff_export#0","supply_demand_durability#3"]},{"n":6,"text":"股價跌破 $70（約 FY2 EPS 8.5 倍），且 HOKA、UGG 門檻都沒破","type":"加碼","maps_to":"H3","metric":"股價","threshold":"≤ $70","action":"分批試單 1%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":7,"text":"股價到 $115（約 FY2 EPS 14 倍），但 HOKA 加速還沒證實","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥ $115","action":"減碼三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":8,"text":"HOKA 單季營收年增回到 ≥5%，且週收盤站回 250 週均線 $102.88","type":"估值rearm","maps_to":null,"metric":"HOKA 季度營收年增率、週收盤價","threshold":"≥5% 且 ≥ $102.88","action":"重跑判斷後首倉 2%","source_freq":"每季／每週","date":null,"evidence_refs":[]},{"n":9,"text":"歐洲第三方物流再次出現履約問題","type":"風險","maps_to":"R5","metric":"管理層揭露的出貨延遲金額","threshold":"任一季再次出現","action":"一次性歸因視為證偽，下修 EMEA 成長假設並停止加碼","source_freq":"法說／每季","date":"2027-01","evidence_refs":[]},{"n":10,"text":"FY2027 第四季財報與 FY2028 全年財測","type":"複審日期","maps_to":null,"metric":"全面複審","threshold":null,"action":"重跑完整判斷","source_freq":"年度","date":"2027-05","evidence_refs":[]}],"kill_metrics":[{"metric":"HOKA 季度營收年增率","bear_threshold":"連 3 季 <5%","window":"FY27 Q3 至 FY28 Q2","source":"公司季報新聞稿","last_status":"warning"},{"metric":"剔除關稅退款的營業利益率（年度）","bear_threshold":"<20%","window":"FY2028 全年","source":"公司新聞稿與法說","last_status":"ok"},{"metric":"UGG 季度營收年增率","bear_threshold":"連 2 季年減","window":"FY27 Q3 至 FY28 Q1","source":"公司季報新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#4","reason":"資料日是 2026-03-20，針對的是 FY26 第四季的單季估計，之後又過了兩次財報；本包較新的共識快照顯示 FY1 近三個月上修 2.66%，舊的上下修家數已被較新資料取代"}],"action_conditions":{"rearm_trigger":"HOKA 單季營收年增回到 ≥5%（先看 FY27 第四財季），且週收盤站回 250 週均線 $102.88","exec_line":"現在不追。兩個條件同時成立才重跑判斷、首倉 2%；跌破 $70 且 HOKA、UGG 門檻都沒破，可先試單 1%","holding_cap":"4%"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 HOKA 兩季減速和指引下修直接外推成盈餘停滯，給 10.5 倍；但就算淨利零成長，每年約 8–10% 市值的回購也能撐住高個位數的每股成長。全價紀律在促銷環境下還讓毛利率上升，定價力沒壞","momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 HOKA 第四財季（2027 年 1–3 月，5 月公布）營收年增回到 ≥5%，且週收盤站回 $102.88；或股價跌破 $70 且 HOKA、UGG 門檻都沒破時先試單","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 HOKA 兩季減速和指引下修直接外推成盈餘停滯，給 10.5 倍；但就算淨利零成長，每年約 8–10% 市值的回購也能撐住高個位數的每股成長。全價紀律在促銷環境下還讓毛利率上升，定價力沒壞"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-25.28, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 HOKA 第四財季（2027 年 1–3 月，5 月公布）營收年增回到 ≥5%，且週收盤站回 $102.88；或股價跌破 $70 且 HOKA、UGG 門檻都沒破時先試單'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"HOKA 在 2027 年新品週期（Bondi 10、Mach Pro、Fly Pace、Bondi Ultra X）之後回到高個位數成長，並守住 $120 以上價帶的份額","2y":"FY2028 HOKA 年增 ≥8%","5y":"FY2028–FY2032 HOKA 年複合成長 ≥7%","10y":null,"threshold":"HOKA 季度營收年增 ≥8%；Q3 FY27 管理層已預告低至中個位數，該季門檻放寬為 ≥3%","source":"公司季報新聞稿的品牌營收；法說中管理層引用的 Circana 份額說法","drift_rule":"連 2 季 <8% 為削弱；連 3 季 <5% 為反轉"},{"id":"H2","text":"UGG 品牌熱度維持，休閒鞋、木屐、服飾等延伸品類抵銷經典靴的成熟化，營收維持正成長","2y":"FY2028 UGG 年增 ≥0%","5y":"UGG 五年營收不低於 FY2026 水準","10y":null,"threshold":"UGG 季度營收年增 ≥0%；冬季季度（Q3）不年減","source":"公司季報新聞稿","drift_rule":"單季年減為削弱；連 2 季年減 ≥5% 為反轉"},{"id":"H3","text":"全價紀律守住利潤率，自由現金流約八成用於回購；即使營收只成長中個位數，每股盈餘仍能維持高個位數成長","2y":"FY2028 剔除退款營業利益率 ≥21%","5y":"五年流通股淨減 ≥25%，剔除退款營業利益率 ≥20%","10y":null,"threshold":"剔除退款毛利率 ≥56%、營業利益率 ≥21%；年度回購 ≥ 自由現金流 70%","source":"法說中 CFO 的毛利率拆解；新聞稿中的回購金額","drift_rule":"剔除退款毛利率連 2 季 <56% 為削弱；年度營業利益率 <20% 為反轉"}],"R":[{"id":"R1","text":"HOKA 品牌熱度退潮：緩衝技術被複製、On 持續拿份額、Nike 跑鞋回歸，份額流失從 $120 以下延伸到高價段","h_ref":"H1","clock":"🔥","threshold":"HOKA 連 2 季年增 <5%，或管理層不再宣稱 $120 以上份額成長","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0"]},{"id":"R2","text":"美國促銷環境拉長，加上成長改靠批發與 $115 的低價款，全價銷售與毛利率被侵蝕","h_ref":"H3","clock":"🔥","threshold":"剔除退款毛利率連 2 季年減","evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#1"]},{"id":"R3","text":"關稅再升級：成品主要在越南、印尼生產，關稅假設已從 10% 升到 12.5%，毛利率下滑主因就是關稅；IEEPA 退款是一次性的，明年同期基期被墊高","h_ref":"H3","clock":"🐢","threshold":"關稅假設 >12.5%，或剔除退款毛利率 <55%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","supply_demand_durability#3","geo_supply_chain#0"]},{"id":"R4","text":"UGG 冬季旺季不如預期：消費者延後到需要時才買，去年天氣帶動的補單今年不會再有","h_ref":"H2","clock":"⚡","threshold":"Q3 FY27 UGG 年減","evidence_refs":[]},{"id":"R5","text":"歐洲第三方物流問題不是一次性：約 $22M 的出貨延遲，部分可能被取消","h_ref":"H1","clock":"⚡","threshold":"下一季再揭露履約延遲","evidence_refs":[]}],"single_thing":{"description":"2027 年 5 月的 FY2028 財測給出 HOKA 全年成長 ≤ 中個位數，也就是 2027 年 1 月 Bondi 10、Fly Pace 上市後，HOKA 仍沒回到高個位數","why_fatal":"HOKA 是唯一的成長引擎，UGG 已經降到低個位數。HOKA 若只剩中個位數，合併營收成長約 3%，EPS 只能靠回購撐，合理倍數從 12–13 倍降到 9–10 倍，情境終點會從 Base 走向 Bear","if_happens":"減碼一半，H1 改判反轉；若 UGG 冬季同時年減，清倉","how_monitor":"Q3 FY27 法說（2027 年 1 月底）的 HOKA 成長與第四財季指引；Bondi 10 上市後的批發補單；2027 年 5 月的 FY2028 財測","probability":"35%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.88,"peg_fy2":0.99,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":7.02,"FY2027E":7.73,"FY2028E":8.21,"FY2029E":9.34},"fy_end_month":3,"eps_basis":"GAAP 稀釋 EPS，財年截至 3 月；FY2027E 共識含部分 IEEPA 關稅退款一次性，FY2028E 要對比被退款墊高的基期"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"product","event":"HOKA Bondi 10 與入門款 Fly Pace（$115）上市","impact":"高","watch":"上市後的批發補單與全價售出率；Bondi 9 是否乾淨出清"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q3 FY27 財報（UGG 冬季旺季、HOKA 第四財季指引）","impact":"高","watch":"UGG 是否年增；HOKA 第四財季的加速指引是否維持"},{"date":"2027-04","date_precision":"month","type":"product","event":"HOKA Mach Pro 上市","impact":"中","watch":"管理層稱訂單很強，看上市後的售出率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第四季財報與 FY2028 全年財測","impact":"高","watch":"HOKA 全年成長指引是否 ≥ 高個位數；剔除退款後的營業利益率指引"},{"date":"2027-06","date_precision":"month","type":"product","event":"Bondi Ultra X（$325）上市","impact":"低","watch":"高價段份額能否延伸"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"剩餘約一成、尚未收到的 IEEPA 關稅退款","impact":"低","watch":"未納入財測，到帳屬一次性，不改變經常性盈餘"}]}
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
