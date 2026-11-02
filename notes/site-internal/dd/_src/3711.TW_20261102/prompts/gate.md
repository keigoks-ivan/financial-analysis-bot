你是 DD 管線 v20 的判斷層閘（gate），標的 3711.TW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝191064 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[0]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi1`（q1_business）｜毛利率＝21.0 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[1]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝21134 NT$百萬（利益率 11.1%）｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[2]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi3`（q1_business）｜歸屬母公司淨利＝21068 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[3]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi5`（q1_business）｜設備資本支出＝1695 US$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi6_3q26`（q1_business）｜管理層指引：3Q26＝合併營收 QoQ +21%～22%；毛利率 20.5%～21.5%；營業利益率 11.5%～12.5%；ATM 營收 QoQ +11%～13%、毛利率 28%～29%；EMS 營收 QoQ 約 +40%、營業利益率 3.2%～3.4%｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm（匯率假設 US$1=NT$31.9）（numbers.latest_quarter_kpis.items[6]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi7_2026`（q1_business）｜管理層指引：2026 全年＝ATM 營收年增約 35%（美元）；一般業務年增 20%（原 13%）；LEAP 服務營收「高於先前 US$35 億指引」｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm（numbers.latest_quarter_kpis.items[7]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_3711_tw_gross_margin_pct`（q2_moat）｜3711.TW 毛利率＝20.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3711_tw_operating_margin_pct`（q2_moat）｜3711.TW 營業利益率＝11.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3711_tw_fcf_margin_pct`（q2_moat）｜3711.TW FCF 利潤率＝-11.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amkr_gross_margin_pct`（q2_moat）｜AMKR 毛利率＝16.56 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amkr_operating_margin_pct`（q2_moat）｜AMKR 營業利益率＝9.51 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amkr_fcf_margin_pct`（q2_moat）｜AMKR FCF 利潤率＝-2.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_6239_tw_gross_margin_pct`（q2_moat）｜6239.TW 毛利率＝19.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6239.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6239_tw_operating_margin_pct`（q2_moat）｜6239.TW 營業利益率＝12.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6239.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_gross_margin_pct`（q2_moat）｜2449.TW 毛利率＝38.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_operating_margin_pct`（q2_moat）｜2449.TW 營業利益率＝26.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.75 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝21.21 TWD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-02）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝33.78 TWD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-02）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝869241.07 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1118078.5 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4`（q4_capital）｜自由現金流（推算）＝-32835 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm；營業現金流 47,014 減 PP&E 淨支出 79,849，由查證者推算，公司未自報 FCF（numbers.latest_quarter_kpis.items[4]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝305981.99 TWD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 394402.99、現金 88421.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.986 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝4415.15 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝668.0 TWD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝40.68 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.14 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.74 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝3255300.43 TWD m｜期間與口徑：2026-11-02／市值 2949318.44 ＋ 淨負債 305981.99｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 668.0 / W52 467.26 / W104 310.42 / W250 190.54 / W250 13週斜率 5.31%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝467.26 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝310.42 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝190.54 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝5.31 %｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝41.03 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝47.73｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（7 條）
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：對手Amkor 2026年Q2營收創高約19億美元、年增26%，7月宣布與NVIDIA多年期15億美元美國封測合作；Intel EMIB-T在高階封裝積壓訂單增加（Zacks/Nasdaq 轉述）
  - 來源：Nasdaq/Zacks: Can ASE Technology Sustain Its Recent Margin Expansion?（as_of 2026-08-01）｜affects：decision_inputs.bear、moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：玉山投顧 2025 年 4 月分析：台廠中日月光美國比重最高、製造據點分布最廣；預期先進封測客戶可能以代購設備換取封測價格持穩，傳統封測則可能被要求降價以分擔客戶關稅成本（分析師預期，非公司公告）
  - 來源：玉山證券 esunsec.com.tw 研究文章（as_of 2025-04-30）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026年股東會：集團採「台灣優先」原則，先在台灣把封測整合與自動化做成熟再複製海外；2024年股東會曾稱不排除在美國、日本、墨西哥增加先進封裝產能；未找到越南、泰國的2026年產能資訊
  - 來源：自由時報 日月光「卯足全力」擴產 今年啟動15座擴廠計畫（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：日月光高層（黃義從）於SEMICON談話稱部分材料由少數廠商主導、甚至握有全球8、9成市占，替代供應商產能有限；部分特殊氣體與原物料集中於特定國家或地區；任一供應商出問題封裝端可能無法出貨
  - 來源：鉅亨/UAnalyze 〈SEMICON〉日月光：材料聯盟要「築高牆」（as_of 2025-09-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：搜尋摘要提及：客戶自建或英特爾晶圓代工加封測一條龍可能壓低封測價格、分流AI測試訂單，但短期英特爾基板良率偏低、實質影響有限（來源網址未能對應到單一篇，僅作線索）
  - 來源：搜尋結果彙整（未對應單一網址）（as_of 2026-08-04）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：搜尋摘要稱 2023 年第一季日月光投控毛利率降至 14.8%，為四年來低點，因客戶庫存調整、稼動率降溫；2022Q4 封裝、測試稼動率降至 75-80%（僅搜尋摘要，未讀原文頁面）
  - 來源：鉅亨網／中央社日月光法說報導（搜尋結果）（as_of 2023-04-27）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：搜尋摘要稱 2023 年全年營收 5,819.14 億元、年減 13%，全年毛利率 15.8%，較 2022 年減少 4.4 個百分點；2022 全年毛利率 20.1%；2023Q4 毛利率 16%（摘要轉述，未讀原文）
  - 來源：TechNews 日月光投控 2023 EPS 7.39 元報導（搜尋結果）（as_of 2024-02-01）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1452.0,"bear_5y_price":276.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":14.5,"ev5y_pct":18.3,"irr_base_pct":2.7,"asym_ratio":1.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":21.21,"pe":31.49,"basis":"FY2026 共識 EPS（年度已過十個月），與終端以當年度 EPS 計的本益比同口徑"},"eps":{"bull":[35.0,44.0,52.0,59.0,66.0],"base":[32.5,37.0,38.0,41.5,45.0],"bear":[28.0,21.0,16.0,19.0,23.0]},"pe":{"bull":22,"base":17,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.986,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 3711.TW_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joseph Tung｜guidance：Q3 合併營收預期季增 21%～22%（以 USD1=TWD31.9 假設）（原話："our consolidated third quarter revenue should grow by 21%"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 ATM 營收季增 11%～13%（原話："our ATM third quarter revenue should grow by 11% to 13%"）
- 2026-07-30｜Joseph Tung｜margin：Q3 ATM 毛利率指引 28%～29%（Q2 實際 27.3%）（原話："Our ATM third quarter gross margin should be between 28% to"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 合併毛利率與營益率指引（逐字稿原文毛利區間寫為 12.5% to 21.5%）（原話："Our consolidated third quarter gross margin should be"）
- 2026-07-30｜Joseph Tung｜guidance：Q3 EMS 營收預期季增約 40%、營益率 3.2%～3.4%（原話："our EMS third quarter revenue should grow by around 40%"）
- 2026-07-30｜Joseph Tung｜margin：管理層拆解 EMS 季增 40% 為記憶體等零組件漲價所致，剔除後為一般季節性（原話："this is largely because of the component price hikes"）
- 2026-07-30｜Joseph Tung｜margin：Q3 EMS 若剔除零組件漲價，營益率約回到 3.7%～3.8%；記憶體為轉嫁成本（原話："the operating margin will be very similar to typical"）
- 2026-07-30｜Joseph Tung｜guidance：EMS 全年成長低於 20%，ATM 全年成長 35% 以上；Q4 EMS 營收與 Q3 相近（原話："EMS at this point, I think the full year is a sub-20% kind"）
- 2026-07-30｜Tien Wu｜guidance：全年 ATM 營收預期成長 35%（美元口徑）（原話："So for the full year, we expect the ATM business revenue to"）
- 2026-07-30｜Tien Wu｜guidance：一般（非 LEAP）業務全年成長指引由 13% 上修；逐字稿該句數字有勘誤標註（30% 更正為 20%）（原話："general segment is expected to grow by 30% (sic) [ 20% ]"）
- 2026-07-30｜Joseph Tung｜guidance：今年 LEAP 營收追蹤優於先前 35 億美元指引，並以 2027 年 LEAP 營收翻倍為目標（原話："we are aiming to double our LEAP revenue in 2027"）
- 2026-07-30｜Joseph Tung｜guidance：CFO 量化今年 LEAP 超標幅度為再增數億美元（原話："we will be adding another couple of hundred million dollars"）
- 2026-07-30｜Joseph Tung｜capital_allocation：今年資本支出再加 20 億美元（廠房與設備各 10 億）（原話："So the total is adding another USD 2 billion for CapEx."）
- 2026-07-30｜Joseph Tung｜capital_allocation：全年 CapEx 總額約 105 億美元，其中廠房設施 40 億、設備 65 億（原話："$4 billion will be for new factory buildings and facilities"）
- 2026-07-30｜Joseph Tung｜capital_allocation：設備 CapEx 拆解：封裝 56%、測試 40%，且約 70% 用於先進製程（原話："it's about 56% is for assembly, 40% for test and the"）
- 2026-07-30｜Joseph Tung｜capital_allocation：目前 13 個新建案與 8 個購入舊廠改建案，足以支撐到 2028 年並可能到 2029 年部分期間（原話："I think the current projects will be sufficient for us to"）
- 2026-07-30｜Joseph Tung｜capital_allocation：CFO 承認負自由現金流將持續，並稱有多種低成本資金來源（原話："the negative cash flow situation will remain for some time"）
- 2026-07-30｜Joseph Tung｜commitment：CFO 表示不會在必要投資上卻步（原話："we are not going to be shy in making the necessary"）
- 2026-07-30｜Joseph Tung｜margin：Q4 ATM 毛利率可能超過 30% 結構性上限，屆時將檢討調整結構性區間（Q2 ATM 毛利率 27.3%）（原話："fourth quarter ATM gross margin likely to exceed our"）
- 2026-07-30｜Joseph Tung｜commitment：管理層明言若調整結構性毛利率區間，方向為向上（原話："when I say adjust, I mean upward adjustment"）
- 2026-07-30｜Joseph Tung｜margin：管理層對定價環境與成本轉嫁的說法（原話："we can definitely pass on these cost increases to our"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 ATM 毛利率 27.3%，季增 1.3 個百分點，歸因於稼動率槓桿與 LEAP 比重提高（原話："driven by higher operating leverage and a more favorable"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 合併毛利率 21.0%，年增拆解為結構性效率與有利匯率（原話："The annual improvement reflects both structural efficiency"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 營業外收益 46 億元含潛在非經常性項目（評價利得 42 億、避險利得 15 億）（原話："the increase primarily reflects some potentially"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 有效稅率 16.4%，全年仍預期 18%（原話："We continue to expect an effective tax rate of 18% for the"）
- 2026-07-30｜Kenneth Hsiang｜margin：預期下半年 ATM 營業費用率持續改善（原話："We expect our ATM operating expense ratio should continue"）
- 2026-07-30｜Kenneth Hsiang｜margin：Q2 EMS 毛利率降 0.6 個百分點至 8.9%，原因為產品組合與零組件成本（原話："The sequential margin decline is the result of product mix"）
- 2026-07-30｜Kenneth Hsiang｜risk：短期成長受限於設備安裝與廠房建置；Q2 綜合稼動率 80%～85%（原話："Our blended utilization rate for the quarter was between"）
- 2026-07-30｜Tien Wu｜risk：COO 稱需求不是疑慮，不確定性在自身執行能力（原話："So the business demand is not a concern. It's our own"）
- 2026-07-30｜Joseph Tung｜risk：同時推進約 20 個建案，管理層點出對營建夥伴的執行壓力（原話："we really need to have a very, very efficient and very"）
- 2026-07-30｜Kenneth Hsiang｜product：Q2 測試與組裝增速敘事變化：組裝（特別是傳統打線）強於年初預期，現預期兩者全年增速相近（原話："We now believe that both our assembly and test businesses"）
- 2026-07-30｜Joseph Tung｜product：自有整廠製程（full process）今年營收約 3 億（逐字稿原文為 TWD 300 million），進度符合預期並積極擴產（原話："this year, we said that we're going to have about TWD 300"）
- 2026-07-30｜Joseph Tung｜product：full process 毛利尚未完全反映，預期未來為毛利accretive業務（原話："full process will also be another margin accretive business"）
- 2026-07-30｜Tien Wu｜product：自家面板製程全自動產線 2027 Q1 開始量產，規格 310x310；玻璃基板未來 12 個月不會量產（原話："our fully automated line will start production by Q1 of"）
- 2026-07-30｜Tien Wu｜product：CPO 年底前可能小量啟動，管理層表示兩季後再提供細節（原話："somewhere along the line towards the end of the year, the"）
- 2026-07-30｜Tien Wu｜commitment：管理層承諾約兩季後提供 2027 LEAP 營收組成（OS、full process 等）細項（原話："Probably 2 quarters from now, we'll give you a better color."）
- 2026-07-30｜Joseph Tung｜guidance：2027 年 CapEx 預期仍大，但具體金額要再等約一季（原話："I know it's going to be big, but how big?"）
- 2026-07-30｜Tien Wu｜competition：對 Intel EMIB 的說法：不視為威脅，純代工定位下可相容（原話："I don't think there's a potential threat. Again, we are a"）
- 2026-07-30｜Tien Wu｜customer：與主要客戶約定先在台灣建全自動產線，之後再遷往美國或其他地區（原話："we will develop and build fully automated efficient line in"）
- 2026-07-30｜Tien Wu｜customer：Q3/Q4 客戶皆要求更多產能，COO 稱公司處於產能受限的位置（原話："all of our customers are asking for more devices for Q3 and"）
- 2026-07-30｜Tien Wu｜customer：一般元件強勁需求來自工業、電源、連接與儲存，並稱將優於整體半導體市場（原話："I believe we will outperform the general market"）
- 2026-07-30｜Tien Wu｜competition：管理層對競爭優勢的定位：純封測無利益衝突（原話："no conflict with foundry, with no conflict with substrate"）

### 問答異常語氣（迴避／改口／保留）
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Sunny Lin 追問 2027 LEAP 翻倍的拆解（full process／OS／測試）與客戶別組成｜答法：COO 與 CFO 未給拆解數字，兩度表示約兩季後再提供更多細節；CFO 僅稱組合與今年相似
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Charlie Chan 質疑 2027 LEAP 翻倍與 2.5D／測試增速、NVIDIA 與 CoWoS 擴產預期是否吻合｜答法：CFO 未回應數字對帳，改談組裝涵蓋 full process 與其他製程步驟及新封裝
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Haas Liu 追問 Q4 毛利率超過上限，成熟製程與 LEAP 各貢獻多少｜答法：CFO 未拆解貢獻比重，改列多項因素（高毛利業務、效率、自動化、營運槓桿）
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Charlie Chan 詢問客戶說下半年大幅漲價是否屬實，及是漲傳統或先進封裝｜答法：CFO 未直接確認或否認漲價幅度，僅稱定價環境友善、成本可轉嫁
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Haas Liu 要求今年 CapEx 分項及明年哪塊成長較快｜答法：CFO 先以客戶需求籠統回答，未給明年分項；總額與分項在後續追問才補出
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Gokul Hariharan 詢問 2027 CapEx 是否續升｜答法：CFO 僅稱會很大，但拒絕給幅度，請等約一季
- 3711.TW_Q2_2026_Earnings_Call_20260730.md｜問：Sunny Lin 詢問 CPO 服務內容與營收何時有意義｜答法：COO 表示要等兩季再談 CPO 服務、營收與 2027 展望，未給時程或數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 3 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 4 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 3 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261019","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","irr_base_pct":0.1,"ev5y_pct":4.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":4.5,"irr_base_pct":0.1,"max_dd_pct":-60,"bull_5y_price":1210.0,"bear_5y_price":312.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","price_at_dd":670.0,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3711.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"日月光投資控股"},"oneliner":"AI 先進封裝把封測毛利率推過 30%，3Q26 全面超標，但現價已是 2027 共識 EPS 近 20 倍，擴產靠舉債、現金流續負；基準情境年化不到 5%，等股價回到 540 元以下","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺晶片設計公司委外的封裝測試加工費，錢卡在先進封裝（LEAP）產能：3Q26 封測占合併營收 62%、營業利益 91%，EMS 是低利潤的零組件轉嫁生意","reasoning":"2Q26 合併營收 1,910.64 億元、毛利率 21.0%、營益率 11.1%、歸屬母公司淨利 210.68 億元。3Q26（2026-10-29 法說）合併營收 2,442 億元（季增 28%、年增 45%）、毛利率 22.1%、營益率 13.6%、稀釋 EPS 5.84 元；封測 1,515 億元（毛利率 30.6%、營益率 20%），EMS 935 億元（毛利率 8.3%、營益率 3.3%，營收含 AI 帶動的零組件漲價轉嫁）。封測內運算應用季增 39%，是 LEAP 主要所在；車用、工業、消費約 14%，通訊 8%。4Q26 指引合併營收季增 6%～8%、毛利率 23%～24%、營益率 14.5%～15.5%，封測營收季增 11%～13%、毛利率再升 1～2pp。單點依賴：前五大客戶占 44%、前十大 60%，一家客戶逾 10%（未具名）；上游關鍵材料少數廠商握八、九成，替代產能有限。兩者都是集中度與供應風險，不是護城河證據。產業時鐘在擴張期：稼動率滿載、需求超過可供給量、定價友善，產業分析師估供過於求最早 2028 年。供需屬週期性、將反轉，時點未定；新廠蓋好後產能不退場，供給可逆性低。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_gaap","f_kpi3","f_kpi5","f_kpi6_3q26","f_kpi7_2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"加工費按量計價，量與價都隨稼動率擺動；LEAP 比重上升讓季節性變弱（法說稱消費季節性對稼動影響變小），但新增量集中在 AI 相關運算；EMS 營收含記憶體等零組件漲價轉嫁，墊高營收卻壓低利潤率","unit_econ_note":"3Q26 封測毛利率 30.6%、營益率 20%、費用率 10.7%；EMS 毛利率 8.3%、營益率 3.3%；4Q26 指引封測毛利率再升 1～2pp、EMS 營益率約 2%","archetype":{"primary":"循環/商品","secondary":"EMS/ODM","confidence":"中","fingerprint":"資本支出約營收四成（2026 年 115 億美元×31.9≈3,670 億元，對共識營收 8,692 億元）；2023 年稀釋 EPS 由 13.81 元降到 7.18 元，合併毛利率在 15.8%～22.1% 擺動；先進封裝是疊在循環上的結構性成長段"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：公司稱 2027 需求遠高於可供給量、瓶頸是廠房空間（3Q26 法說），產業分析師估供過於求最早 2028 年；但公司與同業同步大幅上修資本支出（ASE 2026 年 115 億美元、2027 更大），新產能在 2027～2028 年集中開出","bargaining":{"up":"關鍵材料與特殊氣體由少數廠商主導、市占八、九成，替代產能有限；基板、貴金屬、電費成本上漲目前可轉嫁","down":"前五大客戶 44%、前十大 60%、一家逾 10%；供不應求下管理層稱定價環境非常友善；財務長稱資金來源包含與客戶安排的貿易融資","geo":"產能以台灣為主、採台灣優先；台廠中美國客戶比重最高；列於美國商務部核可封測名單"},"profit_pool_dir":"利潤池往先進封裝與測試移動；CoWoS 鏈中前段價值大半在代工夥伴，ASE 主要拿後段 on-substrate、整段製程與測試","tam_table":[{"item":"ASE LEAP 營收","value":"2025 約 16 億美元→2026 逾 40 億美元→2027 目標倍增（公司指引）"},{"item":"OSAT 端 CoWoS 類月產能（法人估，非公司公告）","value":"ASE 2026 年底約 2 萬片→2027 年底 5 萬～7 萬片；代工夥伴 18 萬片、Amkor 2 萬片"},{"item":"先進封裝占封裝營收","value":"3Q25 約 48%（打線 26%、測試 18%）"},{"item":"產業 TAM／SAM、段年複合成長、營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河 B 級、趨勢向上：規模、製程認證與純封測中立地位撐住，3Q26 封測毛利率 30.6% 突破歷史上限；但 CoWoS 鏈的價值大半在代工夥伴，2028 年後供給追上需求時，垂直整合是主要威脅","reasoning":"執行力 8 分：整段製程良率已達量產、CPO 於 4Q26 量產、2026 LEAP 一年內由 32 億、35 億、37 億上修到逾 40 億美元，3Q26 營收與毛利率皆超過自家指引。定價力 6 分：法說稱定價環境非常友善、成本可轉嫁，但 2Q26、3Q26 兩季都拒絕拆解價格與組合的貢獻，且 2023 年下行時毛利率掉到 15.8%，定價力有一部分是供不應求帶來的週期性。對同業：TTM 毛利率 20.8% 對 AMKR 16.6%（+4.2pp）、營益率 11.5% 對 9.5%（+2.0pp）；合併口徑含低利潤 EMS，封測單獨營益率 20% 的差距更大；利差是否擴大缺 AMKR 時序，事實表未涵蓋。產業態勢雙向拉鋸：結構轉好（先進封裝供不應求、產業分析師估供過於求最早 2028）對上競爭加劇（Amkor 與 NVIDIA 美國合作、代工夥伴子公司投入 on-substrate、Intel EMIB-T）與關稅在地化壓力。ROIC 推導：投入資本約 7,510 億元＝計息負債 4,065 億元－現金 1,079 億元＋由淨負債比 66% 回推的權益約 4,520 億元（3Q26 法說）；TTM 營收約 7,865 億元＝市值÷股價營收比 3.75；TTM 稅後營益率約 9.5%×周轉約 1.05 倍≈10%，3Q26 年化約 15%。","fact_refs":["f_peer_3711_tw_gross_margin_pct","f_peer_3711_tw_operating_margin_pct","f_peer_3711_tw_fcf_margin_pct","f_peer_amkr_gross_margin_pct","f_peer_amkr_operating_margin_pct","f_peer_amkr_fcf_margin_pct","f_peer_6239_tw_gross_margin_pct","f_peer_6239_tw_operating_margin_pct","f_peer_2449_tw_gross_margin_pct","f_peer_2449_tw_operating_margin_pct","f_ps_current","f_kpi1"],"verdict_values":{"moat":{"mechanism":"規模與產能（OSAT 端最大的先進封裝產能、台灣 22 個在建廠案）＋客戶認證與製程共同開發形成的轉換成本＋不與代工、基板業務衝突的純封測定位","execution":8,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：整段製程良率達量產、CPO 4Q26 量產、2026 LEAP 由 32 億一路上修到逾 40 億美元；定價面擴大：封測毛利率 30.6% 突破歷史結構上限，管理層稱定價環境非常友善；對 AMKR 毛利率差 +4.2pp、營益率差 +2.0pp（TTM 合併口徑）。最大客戶份額方向事實表未涵蓋（客戶未具名，前五大占比 43%→44%）","competitor_notes":[{"name":"AMKR","strategy_note":"TTM 毛利率 16.6%、營益率 9.5%，皆低於 ASE；2Q26 營收年增 26%，靠美國在地化與 NVIDIA 多年期 15 億美元合作爭取政策型訂單，是美國產能的主要對手"},{"name":"6239.TW","strategy_note":"毛利率 19.1%、營益率 12.9%（TTM 截至 2026-06），營益率略高於 ASE 合併口徑，因 ASE 合併含低利潤 EMS；先進封裝布局事實表未涵蓋"},{"name":"2449.TW","strategy_note":"毛利率 38.3%、營益率 26.9%，高於 ASE 封測（30.6%／20%）；FCF 利潤率 −32% 顯示同樣在重押擴產"},{"name":"代工夥伴子公司","strategy_note":"3Q26 法說分析師指其大量訂購設備投入 on-substrate；管理層稱規模差距大、不會引發價格戰，屬需求外溢"}],"threats":[{"level":"🟡","text":"Amkor 與 NVIDIA 的 15 億美元美國封測合作、Intel EMIB-T 積壓訂單增加：點對點分流美國與部分高階封裝訂單","p":0.3,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"代工夥伴子公司投入 on-substrate 並大量訂購設備：2028 年供給追上需求後可能把後段收回自做","p":0.3,"evidence_refs":[]},{"level":"🟡","text":"客戶自建或晶圓代工加封測一條龍方案壓低價格、分流 AI 測試（來源未對應單一報導，僅作線索）","p":0.2,"evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"關鍵材料少數廠商握八、九成市占，斷料即無法出貨，並分走價值鏈利潤","p":0.15,"evidence_refs":["geo_supply_chain#3"]}],"roic_durability":{"quadrant":"中利益率×低周轉：TTM 稅後營益率約 9.5%×投入資本周轉約 1.05 倍≈ROIC 10%，3Q26 年化約 15%；資本密集，先蓋廠後出貨使周轉率下降","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是晶片設計公司，決策者是設計公司與代工夥伴，付款者是設計公司，三角色都成立；封裝測試是每顆晶片出貨的必經步驟，屬需要而非想要。多晶片互連已是先進晶片常態，管理層稱 LEAP 產能不只服務 AI。代理讀數：2027 需求遠高於可供給量（3Q26 法說）。急迫性不等於持久性，需求水位仍綁在 AI 資本支出"},{"item":"決策層級","level":"🟡","text":"替代性要看單一產品、單一封裝型態：換封測廠需重新認證，切換成本存在；但大客戶在 ASE、Amkor、代工夥伴之間分配產能，供給緊時由誰有空間決定份額（3Q26 法說分析師語）。漲價後流失率、合約年限事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"CoWoS 鏈前段價值大半在代工夥伴，ASE 拿後段與測試；上游材料少數廠商握八、九成，下游前五大客戶 44%。目前供不應求讓 ASE 多拿，2028 年後供給追上時，代工夥伴子公司自做是價值重新分配的風險。長期需求存在不等於這個環節能一直賺"},{"item":"社會容忍度","level":"🟡","text":"B2B 加工服務，沒有民生必需品的漲價政治壓力；公平會處分 0 筆、反競爭訴訟損失 0 元。主要限制是地緣政策：台廠中美國客戶比重最高，關稅與在地化要求可能壓傳統封測價格（2025-04 分析師預期）；列於美國商務部核可封測名單"}],"roiic":"約 18%（推估，區間 15%～20%）：3Q25→3Q26 季營業利益 132 億→331 億元，年化增量約 800 億元，扣封測毛利率中約 3.3pp 匯率貢獻（年化約 200 億元）後，稅後約 500 億元；分母只計 2026 前三季資本支出 80 億美元×31.9≈2,550 億元減折舊約 700 億元，得約 1,850 億元時增量報酬約 27%，這是上限（漏計 4Q25 資本支出與營運資金，且含舊產能稼動率回升），實際取 15%～20%","reinvest_rate":"約 290%：2026 資本支出 115 億美元×31.9≈3,670 億元，減折舊約 1,000 億元（3Q26 EBITDA 580 億減營業利益 331 億≈249 億／季），除以稅後營業利益約 900 億元（以 2Q26、3Q26 實績與 4Q26 指引推估全年營業利益約 1,100 億元，1Q26 不在本包，按略低於 2Q26 估計）；超過 100% 的部分靠舉債","endo_ceiling":18,"formula_note":"內生成長＝增量 ROIC×再投資率；自籌口徑再投資率上限 100%，故內生上限約 18%（單位 %）。目前舉債口徑 290% 使短期成長可達 50% 以上，與 2027 共識 EPS 年增約 59% 相當，但不可持續"}}}},"q3_growth":{"verdict":"五年後成長空間中等（🟡）：LEAP 2027 約占封測營收三成，下一條曲線（CPO、整段製程、面板級封裝）已量產或排定量產但規模尚小；2027 年前成長受廠房空間限制，不受需求限制","reasoning":"成長以量為主（LEAP 產能開出、稼動率滿載），價為輔（定價友善、組合升級），無併購、無回購。共識：FY2025 實績稀釋 EPS 8.89 元→FY2026E 21.21 元→FY2027E 33.78 元，兩年年複合約 95%（第三年共識事實表未涵蓋）；營收 FY2026E 8,692 億元→FY2027E 1 兆 1,181 億元（+28.6%，17／18 位分析師）。內生上限約 18%（增量 ROIC 約 18%×自籌再投資率 100%）。缺口約 77pp 可歸因：一是利潤率由 2025 年谷底回升（營益率 7.99%→3Q26 13.6%→4Q26 指引 14.5%～15.5%），二是舉債支應的再投資率約 290%，遠超自籌能力；不依賴本益比擴張，但第二項不可持續，2028 年後成長要回到內生上限以內。以 3Q26 封測單季 1,515 億元年化約 190 億美元估，2026 LEAP 約占兩成，2027 倍增後約三成；先進封裝（Bump、FC、WLP、SiP）3Q25 已占封裝營收 48%，落在 35%～70% 區間。下一條曲線有來源：CPO 4Q26 量產、2027 逾 5 億美元；整段製程 2027 逾 10 億美元；面板級封裝 2027 上半年量產；但合計 2027 僅約 15 億美元，不足以單獨支撐 2031 年後成長。營運槓桿為正：3Q26 營收年增 45%、營業利益年增 151%。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_2026","f_kpi6_3q26"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔；無併購與回購","runway_years":"約 5～7","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 約 18%×自籌再投資率上限 100%≈18%（引護城河段推導，不另算）","segments":[{"item":"封測（ATM）","value":"3Q26 營收 1,515 億元、占合併 62%、營業利益占 91%、毛利率 30.6%；4Q26 指引季增 11%～13%"},{"item":"EMS","value":"3Q26 營收 935 億元、毛利率 8.3%、營益率 3.3%；4Q26 營收持平、營益率約 2%；高效能運算約占 EMS 營收 15% 上下"},{"item":"LEAP","value":"2026 逾 40 億美元（原 37 億）；2027 倍增；其中整段製程 2026 約 3 億、2027 逾 10 億美元，CPO 2027 逾 5 億美元"},{"item":"非 LEAP 一般業務","value":"2026 年增逾 20%（原指引 13%），管理層預期 2027 再現；手機與 PC 偏弱，由車用、工業與 AI 周邊晶片補上"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差>5pp）","lit":true,"reading":"FY2025→FY2027 共識 EPS 年複合約 95%、營收約 32%，差距來自利潤率由谷底回升"},{"signal":"自由現金流／淨利 <0.75 連兩年","lit":true,"reading":"FY2024 0.28、FY2025 −0.59，2026 前三季仍為負"},{"signal":"股份基礎給付／營收 >5% 且逐年上升","lit":null,"reading":"事實表未涵蓋"},{"signal":"毛利率連兩季年減","lit":false,"reading":"3Q26 合併毛利率年增 5pp"},{"signal":"核心市占近 12 個月縮減","lit":false,"reading":"無來源證據顯示份額下滑；客戶未具名"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置全押自建產能：2026 資本支出 115 億美元（約營收四成）、2027 更大，自由現金流為負並以舉債支應；併購不適用、回購與股份基礎給付資料缺口","reasoning":"自由現金流／淨利：FY2023 1.69、FY2024 0.28、FY2025 −0.59；TTM 自由現金流利潤率 −11.3%，2Q26 單季自由現金流約 −328 億元（營業現金流 470 億減資本支出 798 億，查證者推算）。現金去向四分：資本支出壓倒性（2026 前三季 80 億美元，其中廠房 32 億、設備 48 億）；股息（殖利率約 1.0%）；併購（近 12 個月僅子公司間簡易合併與購入既有廠房）；回購（事實表未涵蓋）。資金：3Q26 計息負債 4,065 億元（單季增 1,002 億）、現金 1,079 億元、淨負債比 66%、未動用額度 4,573 億元、季淨利息費用 26 億元；管理層稱另有客戶貿易融資。股份基礎給付占營收事實表未涵蓋；3Q26 稀釋 EPS 5.84 元較基本 6.13 元少約 4.7%。營運槓桿為正，未見利潤壓縮。","fact_refs":["f_kpi4","f_kpi5","f_peer_3711_tw_fcf_margin_pct","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無重大併購，只有子公司間簡易合併；購入既有廠房屬資本支出"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購紀錄事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"股份基礎給付金額事實表未涵蓋；3Q26 稀釋 EPS 5.84 元較基本 6.13 元少約 4.7%，來源未拆分"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購；近 12 個月唯一併購類重訊為子公司間簡易合併，購入群創廠房屬資本支出"}}}},"q5_valuation":{"verdict":"現價要求 2027 共識 EPS 33.78 元兌現，且 2028 年後封測毛利率不回落、終端仍給 17 倍，才有年化約 3%～4% 的報酬；2027 我信，2028 年後不信，偏貴，等 540 元以下","reasoning":"現價 668 元＝2026 共識 EPS 31.5 倍、2027 共識 19.8 倍、TTM 本益比 40.7 倍；股價營收比 3.75 倍、企業價值營收比 4.14 倍（前瞻 3.74 倍），四個年度端點內三者都在最高。由法說淨負債比回推帳面約每股 102 元，股價淨值比約 6.5 倍（自身歷史中位事實表未涵蓋）。分母爭議：2027 EPS 建立在封測毛利率 30% 以上與滿載稼動，正是新底部或循環高點的爭點，故不以 19.8 倍論便宜。情境：基準 2031 EPS 45 元×17 倍＝765 元（+14.5%）；樂觀 66 元×22 倍＝1,452 元；悲觀 23 元×12 倍＝276 元；機率 25／45／30，五年期望值約 +18%，上下行比約 1.7。短期（12 個月）：2027 基準 EPS 32.5 元×20 倍＝650 元（−2.7%）；中期（24 個月）：2028 基準 37 元×18 倍＝666 元（−0.3%）。終端倍數對照：事實表無同業本益比，以自身 2027 共識 19.8 倍為現值對照，基準 17 倍低於此。循環位置中循環偏後：資本支出對折舊遠高於 1、稼動率滿載偏賣方，在手需求超前資本支出、量增領先偏買方；本益比在自身年度端點最高，不新建立部位，等回檔。動能：股價 668＞52 週均線 467＞104 週 310＞250 週 191，250 週均線 13 週斜率 +5.3%；26 週漲 41%，RSI 47.7 不過熱。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_dividend_yield_ttm","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2026、2027 共識 EPS）為主，循環股另看股價淨值比；同業本益比事實表未涵蓋","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，沒有同業本益比；終端倍數改以自身 2027 共識本益比 19.8 倍為現值對照"},"fwd_pe":31.49,"peg":1.46,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 668 元＝2026 共識 EPS 31.5 倍、2027 共識 19.8 倍。本益成長比：以 2026 共識本益比除以基準路徑 2026→2029 年 EPS 年複合 21.5% 約 1.5；以 2027 本益比除以 2027→2030 年複合 8.5% 約 2.3。TTM 本益比、股價營收比、企業價值營收比在四個年度端點內都在最高，五年分位事實表未涵蓋。基準情境五年年化約 3%～4%，低於 8%；樂觀情境仍有一倍以上空間，故判偏貴而非極貴","upside_short_pct":-2.7,"upside_mid_pct":-0.3,"denominator_disputed":true,"denominator_note":"2027 共識 EPS 33.78 元建立在封測毛利率 ≥30%（含約 3.3pp 匯率貢獻）與滿載稼動，這正是循環高點或新底部的爭點；以 19.8 倍論便宜無效"}}},"q6_how_wrong":{"verdict":"最可能看錯在把擴產期的毛利率當成新常態：公司正以舉債把產能推向 2029～2030 年需求，若 2028 年前後 AI 擴產消化疊上主流下行，產能、折舊、利息會同時壓在損益上；反方向的錯是共識仍低估 2027","reasoning":"悲觀路徑參照 2023 年：營收年減 13%、毛利率 20.1%→15.8%、稀釋 EPS 13.81→7.18 元（約 −48%），2022 年第四季稼動率降到 75%～80%。這次多兩個放大器：淨負債比 66%（季淨利息 26 億元）與大量新廠折舊。最大回撤取 −45%～−65%：回到 104 週均線 310 元約 −54%；2027 共識 EPS 打六到七折再給 12 倍約 243～284 元（−57%～−64%）。價值陷阱訊號亮兩個（EPS 成長遠高於營收成長、自由現金流／淨利連兩年 <0.75），屬中度。反向風險：3Q26 合併營收季增 28%，超過自家指引上緣 6pp；若毛利率真的逐季升，2027 EPS 可能高於共識，觀望會錯過一段。","fact_refs":["f_kpi4","f_peer_3711_tw_fcf_margin_pct","f_net_debt_m","f_ma_w104","f_ma_w250","f_week26_return_pct","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高位＋擴產期現金流為負"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":21.21,"pe":31.49,"basis":"FY2026 共識 EPS（年度已過十個月），與終端以當年度 EPS 計的本益比同口徑"},"eps":{"bull":[35.0,44.0,52.0,59.0,66.0],"base":[32.5,37.0,38.0,41.5,45.0],"bear":[28.0,21.0,16.0,19.0,23.0]},"pe":{"bull":22,"base":17,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.99,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"max_dd":{"lo":-65,"hi":-45,"basis":"參照 2023 年下行：營收年減 13%、毛利率 20.1%→15.8%、稀釋 EPS 13.81→7.18 元（約 −48%）。現價 668 元是 104 週均線 310 元的 2.15 倍、250 週均線 191 元的 3.5 倍，26 週漲 41%；回到 104 週均線約 −54%。若 2028 年前後 AI 擴產消化疊上主流下行，2027 共識 EPS 打六到七折並給 12 倍，約 243～284 元（−57%～−64%）；較輕的情況 EPS 打八折、14 倍約 −43%。取 −45%～−65%，淨負債比 66% 使下行時股權波動放大","trigger_time":null},"basis":{"bull":"LEAP 2027 倍增後 2028～2031 年仍年增 25% 以上（整段製程、CPO、面板級封裝接棒），封測毛利率升到 35% 上下，下行溫和；終端 22 倍，接近現在 2027 共識 19.8 倍再加成長溢價","base":"2027 略低於共識（扣利息、折舊與潛在股數稀釋），2028 年續成長，2029 年 AI 擴產消化、EPS 小增，之後年增約 9%；終端 17 倍，低於現在 2027 共識 19.8 倍，因 2031 年成長已降到一成以下","bear":"2027 年仍有供不應求撐住，2028～2029 年 AI 擴產消化疊上主流下行，重演 2023 年 EPS 腰斬幅度，加上新廠折舊與利息，2029 年低到 16 元、2031 年回到 23 元；終端 12 倍參照成長降到一成時的本益比。機率 30%：共識成長超過內生上限，且公司只對 2027 給指引，需求大於供給的來源證據不涵蓋 2028 年後，故不因管理層說法壓低悲觀機率"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年下行時營收年減 13%、毛利率由 20.1% 降至 15.8%、單季低至 14.8%，稀釋 EPS 約腰斬；本輪資本支出 2026 年四度上修到 115 億美元、2027 更大，約 15 座新廠瞄準 2029～2030 年需求","assumption":"需求大於供給延續到 2028 年後；公司只對 2027 給了指引","consequence":"2028～2029 年 AI 擴產消化疊上主流封測下行，稼動率掉到 75%～80%，封測毛利率回到 22%～24%，加上折舊與利息，EPS 回到 16～20 元、本益比 12 倍，股價 250～300 元，五年虧五成到六成","ruling":"採納為悲觀主路徑（30%）。與唯一致命點部分重疊：LEAP 倍增下修是這個故事最早的訊號，已列為觸發器；其餘以月營收與淨負債比監測","watch":"月合併營收年增率、封測稼動率與毛利率、2027 資本支出金額","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_kpi5","f_net_debt_m"]},{"view":"論點失敗","evidence":"Amkor 2Q26 營收年增 26% 並與 NVIDIA 簽 15 億美元美國封測合作；Intel EMIB-T 積壓訂單增加；3Q26 法說分析師指代工夥伴子公司大量訂購設備投入 on-substrate","assumption":"ASE 在後段先進封裝的份額與定價不受代工夥伴垂直整合影響","consequence":"2028 年供給追上需求後，份額改由客戶與代工夥伴指定，LEAP 增速與毛利率同時下修","ruling":"部分採納：2027 年前需求遠大於供給，反駁；2028 年起採納為中期風險，不在現在扣護城河分數","watch":"封測毛利率季變動、公司是否揭露份額或價格壓力","evidence_refs":["competitive_share_entrants#3","substitute_technology#2"],"fact_refs":["f_peer_amkr_gross_margin_pct","f_peer_amkr_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"再投資率約 290%（2026 資本支出約 3,670 億元對稅後營業利益約 900 億元），2027 資本支出更大、現金流續負；3Q26 計息負債單季增 1,002 億元，季淨利息 26 億元；關鍵材料少數廠商握八、九成；稀釋 EPS 比基本 EPS 少約 4.7%","assumption":"LEAP 倍增與毛利率上升會轉成股東每股自由現金流","consequence":"營收、EPS 都達標，但增量報酬只有 15% 左右、多年自由現金流為負、靠舉債與客戶貿易融資撐擴產，材料商與大客戶分走價值，每股價值成長遠低於 EPS 成長","ruling":"採納：H3 以 2028 年自由現金流轉正、淨負債比 ≤50% 驗證；淨負債比 >80% 即減碼一半","watch":"淨負債比、TTM 自由現金流、淨利息費用","evidence_refs":["geo_supply_chain#3"],"fact_refs":["f_kpi4","f_peer_3711_tw_fcf_margin_pct","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"台廠中日月光美國比重最高，分析師預期傳統封測可能被要求降價分攤客戶關稅；集團採台灣優先，先在台灣做成熟再複製海外","assumption":"成本可轉嫁（2Q26 法說董宏思語）能延伸到關稅與在地化成本","consequence":"客戶要求美國產能時，海外新廠成本高、稼動慢，傳統封測降價，封測毛利率被吃掉 1～2pp","ruling":"部分採納：分析師說法是 2025 年 4 月的預期，至 3Q26 毛利率未見侵蝕；設吸收失敗門檻：非 LEAP 降價或封測毛利率季減 ≥1.5pp 且公司歸因關稅","watch":"法說對關稅與美國產能的說法、封測毛利率","evidence_refs":["reg_tariff_export#0","geo_supply_chain#2"],"fact_refs":["f_kpi1"]},{"view":"價格已反映太多","evidence":"現價 668 元＝2027 共識 EPS 19.8 倍、2026 共識 31.5 倍；TTM 本益比、股價營收比、企業價值營收比在四個年度端點內都最高；股價淨值比約 6.5 倍；26 週漲 41%，股價是 250 週均線 3.5 倍","assumption":"市場已把 30% 毛利率是新底部延伸到 2028 年後","consequence":"即使 2027 全數兌現，基準情境五年年化約 3%～4%；只要 2028 年展望轉平，本益比會先修正","ruling":"採納：不追，等 540 元以下","watch":"股價對 2027 共識 EPS 倍數、共識修正方向","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_ma_w250"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 670.0 → 本次 668.0（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=670.0","side_b":"本次 price_at_dd=668.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 670 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 670 元：Bull 價 1,210、Bear 價 312，五年期望值 +4.5%，基準年化 0.1%，不對稱比 1.3","side_b":"本次情境、股價仍用 670 元：Bull 價 1,452、Bear 價 276，五年期望值 +17.9%，基準年化 2.7%，不對稱比 1.65","ruling":"先換情境、股價不動：五年期望值多 13.4 個百分點，基準年化多 2.6 個百分點。不對稱比由 1.3 變為 1.65。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 670 元：五年期望值 +17.9%，基準年化 2.7%，不對稱比 1.65","side_b":"本次情境、股價 668 元：五年期望值 +18.3%，基準年化 2.7%，不對稱比 1.67","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.4 個百分點，基準年化多 0.1 個百分點，不對稱比由 1.65 升到 1.67。合計五年期望值比前份多 13.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"封測毛利率：新底部還是循環高點","cause":null,"prior_field":null,"side_a":"3Q26 法說（2026-10-29，財務長董宏思）：結構性毛利率上限已變成底部，2027 以 30% 為基礎逐季改善；LEAP 組合與全面稼動率提升推動，定價環境非常友善","side_b":"2023 年下行時合併毛利率由 20.1% 降至 15.8%、單季低至 14.8%，稼動率降到 75%～80%；3Q26 封測毛利率年增 8pp 中約 3.3pp 來自新台幣匯率；價格與組合各貢獻多少，2Q26、3Q26 兩季都拒絕拆解","ruling":"程度差異、可調和：LEAP 組合升級是真的，2027 產能已被預訂，採信 2027 毛利率 ≥30%；但 30% 底部建立在滿載與友善定價上，匯率部分不屬結構，2028 年後不外推。悲觀機率維持 30%，基準情境 2029 年放入消化年","evidence_level":"公司法說逐字稿（直接）＋2023 年財報（搜尋摘要轉述）","settle_metric":"2027 各季封測毛利率與管理層對稼動率的說法","if_then":["若 2027 任一季封測毛利率 <30% 且公司歸因稼動率或價格 → 不追，進場條件凍結到連兩季回到 30% 以上","若股價先跌到 540 元以下而封測毛利率仍 ≥30%（價格先走、基本面無損）→ 分批反買首筆 2%","反向：若 2Q27 法說給出 2028 LEAP 成長 ≥30% 且封測毛利率 ≥33% → 進場價位上調至 620 元（約 2028 基準 EPS 17 倍）"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"axis":"淨負債比是否已見頂","cause":null,"prior_field":null,"side_a":"3Q26 法說：第三季是淨負債比近期高點（66%），第四季會略降；有多種低成本資金來源，含與客戶安排的貿易融資","side_b":"同一場財務長說 2027 資本支出會比 2026 的 115 億美元更大、2027 現金流仍為負；3Q26 計息負債單季增 1,002 億元至 4,065 億元，淨利息費用季增 8 億元至 26 億元","ruling":"方向相反、不可調和，選 B 側：資本支出更大且現金流為負下，淨負債比最多第四季短暫下降，2027 年預期回升到 70%～80%；依據是公司自己的資本支出與現金流說法。風險落在 H3 與 R3，不改變 2027 EPS 判斷","evidence_level":"同一場法說逐字稿","settle_metric":"4Q26 與 2027 各季淨負債比","if_then":["若持有且 2027 任一季淨負債比 >80% → 減碼一半","反向：若 4Q27 淨負債比 ≤55% 且 2027 自由現金流轉正 → H3 提前成立，進場價位上調 40 元"],"evidence_refs":[]},{"axis":"競爭：規模優勢對上垂直整合與美國在地化","cause":null,"prior_field":null,"side_a":"3Q26 法說：ASE 是此領域的主導者，代工夥伴與客戶的其他競爭出於必要，規模差距大不會引發價格戰；2Q26 法說（2026-07-30，營運長吳田玉）稱 Intel EMIB 不構成威脅，純封測與代工、基板無利益衝突","side_b":"分析師指代工夥伴子公司大量訂購設備投入 on-substrate；Amkor 2Q26 營收年增 26%，並與 NVIDIA 簽 15 億美元美國封測合作；Intel EMIB-T 積壓訂單增加；客戶自建或一條龍方案可能壓價","ruling":"時間差、可調和：2027 年前需求遠大於供給，份額由誰有空間決定、不傷價格，採 A 側；2028 年起供給追上需求時，B 側是主要結構風險，列中期風險，不在現在扣護城河分數","evidence_level":"法說逐字稿＋媒體轉述（Zacks／Nasdaq）","settle_metric":"封測毛利率季變動、2027 LEAP 實績對指引","if_then":["若公司揭露 LEAP 份額下滑，或封測毛利率季減 ≥2pp 且歸因價格 → 不追，護城河趨勢改為持平","反向：若 2027 整段製程營收 >15 億美元（高於指引 10 億）→ 定價力判斷上調一級，進場價位上調 30 元"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#2"]},{"axis":"前一季承諾對本季兌現","cause":null,"prior_field":null,"side_a":"2Q26 法說（2026-07-30，董宏思）：3Q26 合併營收季增 21%～22%、封測營收季增 11%～13%、封測毛利率 28%～29%；2026 LEAP 高於 35 億美元；吳田玉承諾約兩季後給 2027 LEAP 組成；2027 資本支出金額再等約一季","side_b":"3Q26 實績：合併營收季增 28%、封測季增 20%、封測毛利率 30.6%；2026 LEAP 由 37 億上修到逾 40 億美元；提前一季給出整段製程逾 10 億、CPO 逾 5 億美元；但 2027 資本支出仍只說「比今年大」，沒有數字","ruling":"一致為主：短期財測連續超標、組成揭露提前；唯一未兌現的是 2027 資本支出金額，與現金流為負屬同一風險，列入 4Q26 法說檢查","evidence_level":"前後兩季法說逐字稿","settle_metric":"4Q26 法說是否揭露 2027 資本支出金額","if_then":["若 4Q26 法說仍不給 2027 資本支出金額，或金額 >150 億美元而 LEAP 指引未上修 → 不追，悲觀機率上調至 35%"],"evidence_refs":[]},{"axis":"非 AI 需求：手機與 PC 砍單對上一般業務年增兩成","cause":null,"prior_field":null,"side_a":"3Q26 法說：一般業務 2026 年增逾 20%，2027 預期再現，由車用、工業與 AI 周邊晶片補上手機與 PC 的疲弱","side_b":"同場分析師指晶圓前段已出現 PC 與手機砍單；手機與 PC 因零組件漲價處於疲軟期（管理層也承認）","ruling":"未證、監測：一般業務約占封測營收八成，2027 再增兩成的說法目前只有管理層一方，不採信也不否定","evidence_level":"法說逐字稿","settle_metric":"1H27 一般業務年增率","if_then":["若 1H27 一般業務年增 <10% → 悲觀機率上調至 35%、不追","反向：若 1H27 一般業務年增 ≥20% → 基準 2028 EPS 上調 5%"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：以 2027 共識 EPS 19.8 倍買一家 2027 EPS 年增約 59%、封測毛利率剛突破歷史上限且管理層說還會逐季升、2026 LEAP 一年內上修三次的公司；3Q26 營收超過自家指引上緣 6pp，共識可能仍偏低；若 2028 EPS 再成長 20% 並給 18 倍，約 730 元","side_b":"觀望：基準情境五年年化約 3%～4%，上下行比約 1.7、低於 2；現價隱含 30% 毛利率底部延續到 2028 年後，而公司正以舉債把產能推向 2029～2030 年需求","ruling":"採觀望。買進論證成立的前提是 2028 年後毛利率與成長不回落，這正是本次不採信的部分；唯一約束是價格，540 元以下時下行風險才被價格補償","evidence_level":"法說逐字稿＋情境推算","settle_metric":"股價對 2027 共識 EPS 倍數","if_then":["若股價 ≤540 元且封測毛利率 ≥30% → 分批建立首筆 2%","若股價續漲但 2028 展望未出 → 不追"],"evidence_refs":[]},{"axis":"前份結論欄位對帳（3Q26 法說新證據）","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-10-19）：訊號 B、陷阱風險中（🟡）、護城河趨勢向上、五年後成長空間中等（🟡）、循環／商品型、中循環；裁決觀望、角色追蹤","side_b":"本次：六項判斷維持；3Q26 超標、2026 LEAP 上修到逾 40 億美元、30% 封測毛利率成為 2027 底部，抬高三條 EPS 路徑；但資本支出第四度上修到 115 億美元、2027 更大且現金流續負，兩相抵銷，裁決預期維持觀望、角色追蹤","ruling":"新證據強化 2027 年，未改變 2028 年後的判斷；循環位置在中循環偏後（資本支出對折舊遠高於 1、稼動率滿載），不前移到晚循環是因為在手需求仍超前資本支出","evidence_level":"3Q26 法說逐字稿","settle_metric":"4Q26 法說 2027 LEAP 與資本支出","if_then":[],"evidence_refs":[]},{"axis":"估值結論與情境機率（價格變動）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份股價 670 元：估值偏貴（🟠），機率樂觀 25%／悲觀 30%","side_b":"本次 668 元（−0.3%）：估值仍偏貴（🟠），機率維持 25／45／30","ruling":"價格幾乎沒動，估值結論與機率結構不變；新證據只移動三條路徑的高度，不改變各情境的相對可能性","evidence_level":"收盤價","settle_metric":"股價","if_then":[],"evidence_refs":[]},{"axis":"最大回撤由單點改為區間（方法變動）","cause":"方法變動","prior_field":["max_dd_pct"],"side_a":"前份最大回撤 −60%（單點）","side_b":"本次 −45%～−65%（依 2023 年下行 EPS 約腰斬、回到 104 週均線約 −54%、悲觀情境終點約 −59% 推得）","ruling":"改填範圍以符合寬度至少 10pp 的要求；中心值 −55% 與前份 −60% 相近，下緣 −65% 涵蓋悲觀情境終點","evidence_level":"情境推算","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場（分批建立首筆）門檻變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","side_b":"股價≤540 元（約 2027 共識 EPS 16 倍）且封測毛利率≥30%、2027 LEAP 倍增指引未下修","ruling":"舊→新：價位 500→540，因 2026 LEAP 上修到逾 40 億美元、30% 封測毛利率成為 2027 底部，抬高基準 2031 EPS 到 45 元；以基準終值 765 元回推年化 8%（含股息約 1%）約 545 元。毛利率門檻 27%→30%，因管理層已把 30% 定為 2027 底部，跌破即代表論點走樣","evidence_level":"3Q26 法說逐字稿＋情境推算","settle_metric":"股價、封測季毛利率","if_then":["若股價 ≤540 元且條件成立 → 分批建立首筆 2%"],"evidence_refs":[]},{"axis":"淘汰指標新設（減碼與清倉門檻）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定淘汰指標（null）","side_b":"封測毛利率連兩季 <27%→清倉；2027 LEAP 指引 <60 億美元→清倉；淨負債比 >80%→減碼一半；月營收年增連三個月 <10%→減碼三分之一","ruling":"前份判斷未產出淘汰指標；本次依論點 H1～H3 各設可觀測門檻，門檻取自 3Q26 實績與管理層指引","evidence_level":"3Q26 法說逐字稿","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定（null）","side_b":"公司在任一季法說把 2027 年 LEAP 營收倍增指引下修","ruling":"前份判斷未產出唯一致命點；本次依 EPS 敏感度選定：2027 共識 EPS 比 2026 多約 12.6 元，主要來自 LEAP 增加約 40 億美元營收，是單一最大變數","evidence_level":"3Q26 法說逐字稿","settle_metric":"每季法說 2027 LEAP 指引","if_then":["若下修 → 未持有取消進場條件，已持有減碼一半"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 540 元以下（約 2027 共識 EPS 16 倍）且封測毛利率仍 ≥30%、2027 LEAP 倍增指引未下修","type":"估值rearm","maps_to":"H1","metric":"收盤價＋封測季毛利率＋2027 LEAP 指引","threshold":"≤540 元且 ≥30% 且未下修","action":"分批建立首筆 2%，第二筆待下一季封測毛利率 ≥31%","source_freq":"每日股價／每季法說","date":null,"evidence_refs":[]},{"n":2,"text":"公司在任一季法說把 2027 年 LEAP 營收倍增指引下修","type":"Single Thing","maps_to":"H1","metric":"2027 LEAP 營收指引","threshold":"低於 75 億美元或不再說倍增","action":"未持有：取消進場條件；已持有：減碼一半","source_freq":"每季法說","date":"2027-02","evidence_refs":[]},{"n":3,"text":"封測毛利率以 30% 為底、2027 逐季上升","type":"假設驗證","maps_to":"H2","metric":"封測季毛利率","threshold":"4Q26 ≥31.6%（指引下緣）；2027 每季 ≥30%","action":"單季 <30% 停止加碼；連兩季 <27% 清倉","source_freq":"每季","date":"2027-02","evidence_refs":[]},{"n":4,"text":"擴產撞上下行：淨負債比續升或稼動率下滑","type":"風險","maps_to":"R3","metric":"淨負債比／封測稼動率","threshold":"淨負債比 >80% 或稼動率 <75%","action":"減碼一半","source_freq":"每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":5,"text":"代工夥伴子公司、Amkor、Intel 分食後段先進封裝","type":"風險","maps_to":"R2","metric":"封測毛利率季變動與公司對價格的說法","threshold":"季減 ≥2pp 且歸因價格","action":"不追；已持有則停止加碼","source_freq":"每季","date":null,"evidence_refs":["competitive_share_entrants#3","substitute_technology#2"]},{"n":6,"text":"關稅與在地化成本吸收失敗","type":"風險","maps_to":"R4","metric":"非 LEAP 封測價格／封測毛利率","threshold":"季減 ≥1.5pp 且公司歸因關稅或在地化成本","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#2"]},{"n":7,"text":"需求降溫：月營收年增率放緩","type":"減碼","maps_to":"R1","metric":"月合併營收年增率","threshold":"連 3 個月 <10%","action":"已持有則減碼三分之一；未持有則不追","source_freq":"每月","date":null,"evidence_refs":[]},{"n":8,"text":"關鍵材料供應中斷","type":"風險","maps_to":"R5","metric":"季營收對指引","threshold":"低於指引下緣且公司歸因材料短缺","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#3"]},{"n":9,"text":"4Q26 法說：檢查 2027 LEAP 組成與 2027 資本支出金額（2Q26 法說承諾約兩季後揭露）","type":"複審日期","maps_to":null,"metric":"2027 資本支出金額與 LEAP 指引","threshold":"≥150 億美元且 LEAP 指引未上修則悲觀機率上調至 35%","action":"重跑研究","source_freq":"每季","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"封測（ATM）季毛利率","bear_threshold":"連兩季 <27%","window":"4Q26～4Q27 各季","source":"公司季報與法說簡報封測損益","last_status":"ok"},{"metric":"2027 年 LEAP 營收指引","bear_threshold":"下修至 <60 億美元（3Q26 法說為倍增至逾 80 億）","window":"2027 年內各季法說","source":"公司法說逐字稿","last_status":"ok"},{"metric":"淨負債比（淨負債÷權益）","bear_threshold":">80%（3Q26 為 66%）","window":"4Q26～4Q27","source":"公司季報資產負債表","last_status":"ok"},{"metric":"月合併營收年增率","bear_threshold":"連 3 個月 <10%","window":"2027 年各月","source":"公開資訊觀測站月營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤540 元（約 2027 共識 EPS 16 倍）且封測毛利率≥30%、2027 LEAP 倍增指引未下修","exec_line":"未持有：不追；股價≤540 元且封測毛利率≥30%、2027 LEAP 倍增未下修→分批建立首筆 2%，下一季封測毛利率≥31% 再加第二筆 2%；已持有：不加碼，淨負債比 >80% 或 LEAP 倍增下修→減碼一半，封測毛利率連兩季 <27%→清倉"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價≤540 元（約 2027 共識 EPS 16 倍）且封測毛利率≥30%、2027 LEAP 倍增指引未下修","prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=41.03, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"LEAP 營收 2026 逾 40 億美元、2027 倍增至 80 億美元以上；整段製程 2027 逾 10 億美元、CPO 逾 5 億美元","2y":"2027 全年 LEAP ≥80 億美元","5y":null,"10y":null,"threshold":"2027 全年 LEAP ≥75 億美元；任一季法說不再說倍增即視為偏離","source":"公司季度法說逐字稿與簡報（下次約 2027-02 的 4Q26 法說）","drift_rule":"兩年期：指引或實績偏離連 2 季 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"封測毛利率以 30% 為新底部，2027 逐季上升（3Q26 30.6%，4Q26 指引再升 1～2pp）","2y":"2027 每季封測毛利率 ≥30%","5y":null,"10y":null,"threshold":"單季 <30% 為警示；連兩季 <27% 為反轉","source":"公司季報封測損益表","drift_rule":"兩年期：連 2 季低於門檻 ≥5%（即 <28.5%）為削弱，連 3 季低於 ≥10%（即 <27%）為反轉"},{"id":"H3","text":"擴產的增量報酬至少 15%，2028 年起自由現金流轉正、淨負債比回到 50% 以下","2y":null,"5y":"2028 全年自由現金流 >0 且 4Q28 淨負債比 ≤50%，ROIC 維持 12% 以上","10y":null,"threshold":"2028 年自由現金流 >0；4Q28 淨負債比 ≤50%","source":"公司季報資產負債表與現金流量表","drift_rule":"五年期：淨負債比或 TTM 自由現金流利潤率連 4 季偏離路徑 ≥5% 為削弱，連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"AI 擴產消化或客戶拉貨放緩，2027 LEAP 倍增下修（與唯一致命點同源）","h_ref":"H1","clock":"⚡","threshold":"月合併營收年增率連 2 個月 <15%，或任一季法說下修 2027 LEAP","evidence_refs":[]},{"id":"R2","text":"競爭與垂直整合：代工夥伴子公司投入 on-substrate、Amkor 與 NVIDIA 美國合作、Intel EMIB-T 與一條龍方案，在 2028 年供給追上需求後壓縮份額與價格","h_ref":"H2","clock":"🔥","threshold":"封測毛利率季減 ≥2pp 且公司歸因價格，或 LEAP 增速低於自身產能增速","evidence_refs":["competitive_share_entrants#3","substitute_technology#2"]},{"id":"R3","text":"擴產撞上下行：2026 資本支出四度上修到 115 億美元、2027 更大，約 15 座新廠瞄準 2029～2030 年需求；上次下行（2023 年）營收年減 13%、毛利率 15.8%、單季低至 14.8%","h_ref":"H3","clock":"🐢","threshold":"封測稼動率 <75% 或淨負債比 >80%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R4","text":"關稅與在地化：台廠中美國客戶比重最高，傳統封測可能被要求降價分攤客戶關稅；集團採台灣優先，產能集中台灣","h_ref":"H2","clock":"🔥","threshold":"非 LEAP 封測降價，或封測毛利率季減 ≥1.5pp 且公司歸因關稅或在地化成本","evidence_refs":["reg_tariff_export#0","geo_supply_chain#2"]},{"id":"R5","text":"關鍵材料與特殊氣體由少數廠商握八、九成市占，任一供應商出事即無法出貨","h_ref":"H1","clock":"⚡","threshold":"單季營收低於指引下緣且公司歸因材料短缺","evidence_refs":["geo_supply_chain#3"]}],"single_thing":{"description":"公司在任一季法說把 2027 年 LEAP 營收倍增指引下修（例如降到 60～70 億美元，或不再說倍增）","why_fatal":"2027 共識 EPS 33.78 元比 2026 的 21.21 元多約 12.6 元，主體來自 LEAP 增加約 40 億美元營收及其帶動的封測毛利率，是 EPS 對單一變數最大的敏感度；少做 20 億美元約少 3～5 元 EPS，並同時否定 30% 毛利率是新底部的說法，本益比會一起下修","if_happens":"未持有：取消進場條件，重跑研究；已持有：減碼一半，剩餘部位看下一季封測毛利率是否 ≥30%","how_monitor":"每季法說的 2027 LEAP 指引（下次約 2027-02 的 4Q26 法說）；每月 10 日前後的月營收年增率","probability":"約 20%（12～24 個月）：公司 3Q26 剛重申倍增，自稱需求遠大於可供給量；下修較可能來自建廠與裝機延誤，而非需求"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.78,"peg_fy2":2.33,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":8.89,"FY2026E":21.21,"FY2027E":33.78,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為年報稀釋 EPS；FY2026E、FY2027E 為 yfinance 分析師共識平均（EPS 家數事實表未涵蓋，同年度營收共識 17／18 家）；FY2028E 共識事實表未涵蓋"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"11 月合併營收公布","impact":"低","watch":"年增率是否維持 30% 以上（7 月為 43%）"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"4Q26 法說：2027 LEAP 組成與 2027 資本支出金額（2Q26 法說承諾約兩季後揭露）","impact":"高","watch":"LEAP 倍增是否維持；資本支出是否超過 150 億美元"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"面板級封裝全自動產線量產（管理層稱 2027 第一季、310×310 規格）","impact":"中","watch":"是否如期量產、有無客戶具名"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"1Q27 法說：封測毛利率是否守住 30% 以上並逐季上升","impact":"高","watch":"封測毛利率、淨負債比"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"CPO 放量（2027 逾 5 億美元）與整段製程放量（逾 10 億美元）","impact":"中","watch":"2Q27 法說是否維持兩項指引"}]}
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
