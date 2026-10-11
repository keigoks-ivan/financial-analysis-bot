你是 DD 管線 v20 的判斷層閘（gate），標的 3044.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑤ 覆蓋面掃描（強制）——facts.json 逐軸點名 status="none"／"not_applicable" 的每一軸：理由站得住嗎？查詢是否切題且足以支撐該軸結論（不以查詢次數計）？**缺軸本身即 🔴，不需先證明結論錯**。[gate_contract §⑤]

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、裁決、角色）。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤，缺軸本身即 🔴。
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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_ifrs`（q1_business）｜營收（IFRS 合併）＝24857 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MOPS 合併財報（經 uanalyze 整理）；yfinance quarterly_income_stmt Total Revenue 24.857B（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：Investing.com 預估 24.21B（約高於預期 2.7%）
- `f_kpi1`（q1_business）｜毛利率＝30.02 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze 引 MOPS；yfinance 毛利 7.479B／營收 24.857B（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：媒體稱優於預期，未取得量化共識
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝5608 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt Operating Income 5.608B；經濟日報報導約 55.8 億（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：媒體稱優於預期，未取得量化共識
- `f_kpi3_gaap_ifrs_non_gaap`（q1_business）｜GAAP 營業利益率（台灣 IFRS，無 Non-GAAP 口徑）＝22.56 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：由營業利益 5,608 ÷ 營收 24,857 計算（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：未取得
- `f_kpi4_eps`（q1_business）｜稅後純益／EPS＝7.41 TWD／股（純益 3,896 百萬，YoY +59.41%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze／cnyes 引 MOPS（yfinance 為 7.40）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：Investing.com 預估 6.97
- `f_kpi6_7`（q1_business）｜7 月營收（最新月）＝9822 百萬 TWD｜期間與口徑：2026 年 7 月（公告於 2026 年 8 月）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze 整理月營收公告：MoM +22.74%、YoY +56.55%（numbers.latest_quarter_kpis.items[6]，as_of 2026 年 7 月（公告於 2026 年 8 月））
  - 註記：不適用
- `f_kpi7`（q1_business）｜產品組合：伺服器／記憶體營收占比＝65.3 %（伺服器 42.2% + 記憶體 23.1%）｜期間與口徑：Q2 2026（公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：投顧報告經媒體引述（uanalyze）；伺服器 YoY +70.4%、記憶體 YoY +99.6%（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026（公告於 2026-08-11））
  - 註記：不適用
- `f_kpi8_2026`（q1_business）｜2026 年資本支出計畫＝10000 百萬 TWD 以上｜期間與口徑：2026（公告於 2026-08-11 前後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze 整理（湖北仙桃、越南新廠），高於前高 8,000（numbers.latest_quarter_kpis.items[8]，as_of 2026（公告於 2026-08-11 前後））
  - 註記：不適用
- `f_peer_3044_tw_gross_margin_pct`（q2_moat）｜3044.TW 毛利率＝27.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3044.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3044_tw_operating_margin_pct`（q2_moat）｜3044.TW 營業利益率＝19.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3044.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3044_tw_fcf_margin_pct`（q2_moat）｜3044.TW FCF 利潤率＝-2.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3044.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2368_tw_gross_margin_pct`（q2_moat）｜2368.TW 毛利率＝34.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2368.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2368_tw_operating_margin_pct`（q2_moat）｜2368.TW 營業利益率＝26.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2368.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_operating_margin_pct`（q2_moat）｜3037.TW 營業利益率＝10.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8046_tw_operating_margin_pct`（q2_moat）｜8046.TW 營業利益率＝12.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_8046_tw_fcf_margin_pct`（q2_moat）｜8046.TW FCF 利潤率＝7.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_4958_tw_operating_margin_pct`（q2_moat）｜4958.TW 營業利益率＝8.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4958.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_4958_tw_fcf_margin_pct`（q2_moat）｜4958.TW FCF 利潤率＝-14.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4958.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝-3533 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow：OCF −606，Capex −2,927（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.182 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.63 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.39 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝582.0 USD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝25.02 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝58.23 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝403.99 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w104`（q5_valuation）｜104 週均線＝309.14 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w250`（q5_valuation）｜250 週均線＝204.96 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）

### findings_digest 中方向為負或來源衝突的條目（4 條）
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：2026 年起中國與海外 PCB 廠大幅擴產（勝宏 2026 年投資計畫最高人民幣 200 億、為 2025 計畫 5–6 倍；滬電子公司擬投 55 億人民幣）；分析師示警 2026 年後新產能集中投產而 AI 終端需求不及預期，產業可能陷入低價競爭。未見協同供給紀律的證據
  - 來源：搜尋結果摘要（itiger/longportapp 轉載中文財經新聞）（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：健鼎主要生產基地在中國（江蘇無錫自2003年起、湖北仙桃自2013年起，仙桃已建三廠）；仙桃三廠產能已到位，越南新廠預計2026下半年開始貢獻產出。
  - 來源：富果研究 健鼎(3044) 2026-06 法說會備忘錄（as_of 2026-06-03）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：PCB上游材料（玻纖布、CCL、銅箔）2026年供給吃緊，缺料已由高階擴散到標準FR-4；中國CCL廠商停供部分厚度。
  - 來源：Evertiq 2026-08-19 PCB material shortage spreads to standard FR-4（as_of 2026-08-19）｜affects：decision_inputs.bear、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：2026年1月法說相關報導：車用板件進入庫存去化、手機板件因去年Q3提前拉貨進入季節性調整；伺服器與記憶體板需求仍強
  - 來源：工商時報 ctee 2026-02-11 / 鉅亨 元月營收報導（as_of 2026-02-11）｜affects：decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3044.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1100.0,"bear_5y_price":252.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-8.5,"ev5y_pct":1.4,"irr_base_pct":-1.8,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":23.26,"pe":25.02,"basis":"TTM（2025Q3–2026Q2）稀釋 EPS 約 23.26 元，由現價 582 元÷trailing 本益比 25.02 倍推回；事實表股價單位標 USD，實為新台幣；終端倍數同為 trailing 口徑"},"eps":{"bull":[31.0,41.0,47.0,51.0,55.0],"base":[29.5,35.0,34.0,32.0,35.5],"bear":[28.0,25.0,19.5,19.0,21.0]},"pe":{"bull":20,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.182,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | none | 0 | 2 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 3 | 4 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | none | 0 | 4 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 1 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：健鼎 3044 最大客戶 第二供應商 OR 自製 2026；Tripod Technology 3044 largest customer second source PCB 2026；健鼎 單一客戶 集中度 美光 海力士 供應商 分散 PCB 記憶體模組板
- **customer_concentration_credit**（none）：健鼎 3044 主要客戶 營收占比 客戶集中度；Tripod Technology 3044 customer concentration top customers revenue 2026
- **regulatory_antitrust**（none）：健鼎 3044 antitrust OR monopoly investigation 2026；Tripod Technology 健鼎 regulation OR regulatory scrutiny PCB 2026；3044.TW Tripod Technology DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）：健鼎 3044 PCB 替代技術 威脅 2026；PCB alternative technology disruption glass substrate Tripod Technology 2026 2027
- **channel_business_model_shift**（none）：健鼎 3044 Tripod Technology business model transition 2026；Tripod Technology PCB distribution channel shift customers 2026；PCB industry channel disintermediation direct sourcing 2026 server PCB；健鼎 go-to-market 轉型 伺服器 車用 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3044.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"健鼎科技 Tripod Technology"},"oneliner":"AI 伺服器與記憶體板的外溢訂單把健鼎毛利率推到 30%，但同業擴產潮 2027 年後落地；582 元已用四年最高的倍數定價高峰利潤，Base 情境五年報酬接近零，等股價回到 410 元以下且毛利率仍守 27% 再進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3044.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3044.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"健鼎賺的是伺服器與記憶體模組客戶的 PCB 加工錢，錢卡在產能：一線大廠把產能讓給 GPU／ASIC 高階板，一般伺服器板外溢到健鼎，再疊上記憶體上行，Q2 2026 毛利率衝到 30.02%；這兩股力量都可逆。","reasoning":"營收結構：Q2 2026 合併營收 248.57 億元，伺服器板占 42.2%（YoY +70.4%）、記憶體模組板占 23.1%（YoY +99.6%），其餘約 34.7% 為筆電、車用、手機等；車用板進入庫存去化、手機板季節性調整，非 AI 業務今年只小幅成長。最新一季毛利率 30.02%、營益率 22.56%、EPS 7.41 元（市場預估 6.97 元），7 月營收 98.22 億元、YoY +56.55%。錢卡在哪：一線 PCB 廠優先供應 GPU／ASIC 高階 AI 伺服器，一般伺服器訂單明顯外溢到健鼎；記憶體 PCB 主要客戶含美光、海力士，法人估記憶體業務占比可升到 25% 以上。健鼎拿到的是產能吃緊期的外溢與組合紅利，不是技術授權或規格主導權（同業對照研發密度僅 0.35%）。產業時鐘判在過熱期：上游缺料已由高階蔓延到標準 FR-4、同業 2026 年擴產規模放大 5–6 倍、二線廠承接一線外溢訂單，屬供給吃緊但新產能尚未落地的階段，依據是供需而非股價。供需持久性：週期性將反轉——上游銅箔與玻纖布短缺有規格驅動的結構成分，但成品板產能可逆性高，2027 年後新產能集中投產。單點依賴：伺服器＋記憶體合計 65.3%，記憶體客戶集中在美光、海力士，個別客戶占比事實表未涵蓋。本次沒有法說逐字稿，管理層對報價與擴產回收期的說法無法對照，屬證據缺口。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_gaap","f_kpi3_gaap_ifrs_non_gaap","f_kpi4_eps","f_kpi6_7","f_kpi7","f_kpi8_2026"],"verdict_values":{"revenue_quality":"B2B 訂單型營收，無長約與經常性收入；伺服器與記憶體兩個終端合計 65.3%，季營收隨客戶拉貨與記憶體循環擺動，FY2023 營收曾衰退 10.5%。","unit_econ_note":"毛利率由 FY2022 的 17.95% 升到 Q2 2026 的 30.02%，營益率由 10.19% 升到 22.56%；利潤率改善來自高層數伺服器與記憶體板的組合與稼動率，研發密度 0.35% 顯示不是技術溢價。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY2023 營收 −10.5%、毛利率四年間由 17.95% 擺到 30.02%、2026 年資本支出逾 100 億元創新高：利潤跟著稼動率、組合與產業擴產週期擺動的製造業。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：上游 HVLP4 銅箔短缺被 Morgan Stanley 視為結構性（2027 年缺 31%、2028 年仍缺 20%），但成品板產能可逆性高——同業 2026 年投資計畫放大 5–6 倍、2027 年後集中投產；來源為券商報告轉述與產業新聞，非公司揭露。","bargaining":{"up":"上游銅箔、玻纖布、CCL 缺料且由高階擴散到標準 FR-4，Panasonic 永久停產標準玻纖布 CCL 產線，供應商議價力上升。","down":"客戶含美光、海力士與伺服器組裝客戶；訂單能從一線廠外溢到健鼎，代表客戶依產能在已認證供應商間分配，議價力在客戶端。","geo":"主力產能在中國江蘇無錫（2003 年起、六個廠）與湖北仙桃（三廠已到位），越南周德新廠規劃每月約 30 萬呎、2026 年下半年開始貢獻。"},"profit_pool_dir":"利潤池往兩端集中：上游高階材料（銅箔、玻纖布）與承接 GPU／ASIC 主板的一線廠；健鼎吃到的是一般伺服器與記憶體板的外溢與組合紅利，營業利益池占比的五年變化事實表未涵蓋。","tam_table":[{"item":"全球 PCB 市場","value":"2025 年 924 億美元 → 2026 年 1,137 億美元（台灣電路板協會估）"},{"item":"AI 伺服器 PCB","value":"2027 年約 375 億美元（GPU 伺服器約 188 億、ASIC 伺服器約 187 億）、2028 年約 840 億美元（高盛 2026-08，單一券商）"},{"item":"中國 AI-PCB","value":"2027 年人民幣 3,070 億、2028 年 5,620 億（花旗 2026-06，單一券商、中國口徑）"},{"item":"健鼎份額與營業利益池占比","value":"事實表未涵蓋：缺匯率與同業營業利益合計，無法換算滲透率與五年前占比"}]}}},"q2_moat":{"verdict":"護城河方向穩定（→），等級 C：優勢是製造效率與成本，TTM 營益率 19.38% 在五家同業排第二、比最強同業低 6.67 個百分點；份額正在流入，但流入來自一線廠產能滿載的外溢，產能一鬆可能流回。","reasoning":"機制：成本與製造效率——大量通用伺服器與記憶體模組板的良率與規模，加上客戶料號認證；研發密度 0.35% 為五家同業最低，不是技術型護城河。可證方向：份額正在流入——一線廠專注 GPU／ASIC 高階板，一般伺服器訂單明顯外溢到健鼎；法人估記憶體業務占比可升到 25% 以上；ASIC 主板切入只是法人預期、非已確認設計案。但流入原因是對手產能滿載而非健鼎贏得規格，產能一鬆可逆。對最強同業 TTM 營益率差 −6.67 個百分點（19.38% 對 26.05%），高於其餘三家（10.24%、12.27%、8.66%）；只有一期 TTM，差距擴大或收窄無法判斷。評分：執行 7（同業第二高利潤率、FY2022–FY2025 自由現金流皆為正、FY2023 衰退期 EPS 只減 2%）；定價權 5（毛利率改善靠產能吃緊與組合，上游缺料與同業擴產兩頭夾）。趨勢：執行擴大、定價權有縮減風險，兩者相抵判穩定。最大威脅是同業擴產潮引發的價格競爭（生態層級，機率 30%）。報酬持續期四檢查點三黃一綠，超額報酬能維持多久取決於成品板供需何時轉鬆。","fact_refs":["f_peer_3044_tw_gross_margin_pct","f_peer_3044_tw_operating_margin_pct","f_peer_3044_tw_fcf_margin_pct","f_peer_2368_tw_gross_margin_pct","f_peer_2368_tw_operating_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_8046_tw_operating_margin_pct","f_peer_8046_tw_fcf_margin_pct","f_peer_4958_tw_operating_margin_pct","f_peer_4958_tw_fcf_margin_pct","f_kpi1"],"verdict_values":{"moat":{"mechanism":"成本與製造效率（通用伺服器、記憶體模組板的良率與規模），輔以客戶料號認證；研發密度 0.35% 顯示不是技術型護城河。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大（一般伺服器訂單外溢流入、仙桃三廠到位、越南新廠動工）；定價權面有縮減風險（上游缺料推高成本、同業 2026 年擴產放大 5–6 倍）；兩者相抵判穩定。對最強同業營益率差 −6.67 個百分點，事實表只有 TTM 一期，無法判斷差距方向。","competitor_notes":[{"name":"2368.TW","strategy_note":"同業利潤率最高（TTM 毛利率 34.69%、營益率 26.05%），是健鼎對照的最強同業；健鼎營益率落後 6.67 個百分點，差距方向因只有一期數據無法判斷。"},{"name":"3037.TW","strategy_note":"研發密度 3.92%、為健鼎十倍以上，走高階技術路線，但 TTM 營益率 10.24% 低於健鼎，技術投入尚未換成利潤率。"},{"name":"8046.TW","strategy_note":"營益率 12.27% 低於健鼎，但 FCF 利潤率 7.71% 是五家中唯一明顯為正，擴產期現金紀律優於健鼎。"},{"name":"4958.TW","strategy_note":"營益率 8.66%、FCF 利潤率 −14.2%，擴產期現金消耗最重，價格競爭時承壓能力弱於健鼎。"}],"peer_na_reason":"同業 ROIC 與多年利潤率序列事實表未涵蓋，以 TTM 營益率差作可比軸。","threats":[{"level":"🔴","text":"中國與海外同業 2026 年起大幅擴產（勝宏投資計畫最高人民幣 200 億、為前一年 5–6 倍），未見供給紀律，新產能 2027 年後集中投產，一般伺服器板外溢訂單可能回流一線廠並引發價格競爭。","p":"30%","evidence_refs":["supply_demand_durability#2"]},{"level":"🟡","text":"上游銅箔、玻纖布、CCL 缺料由高階擴散到標準 FR-4，中國 CCL 廠停供部分厚度；成本轉嫁能力在成品板供需轉鬆時會受考驗。","p":"25%","evidence_refs":["geo_supply_chain#2"]},{"level":"🟡","text":"主力產能集中中國無錫與仙桃，中國製 PCB 輸美有效稅率最高約 45%；越南新廠每月約 30 萬呎、2026 下半年才開始貢獻，客戶若要求非中國產地，健鼎能承接的量有限。","p":"20%","evidence_refs":["geo_supply_chain#0","reg_tariff_export#2"]}],"roic_durability":{"quadrant":"稅後營業利益率約 15%（TTM 營益率 19.38%×FY2025 淨利÷營業利益約 0.79），投入資本周轉率事實表未涵蓋，當期 ROIC 無法計算；資本密集製造業，暫列高利益率×周轉率待查。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"付款者是伺服器組裝廠、品牌與記憶體模組廠，決定者是雲端業者的 AI 資本支出；需求屬需要但時點可延後，AI 資本支出一旦消化，伺服器拉貨會延後。高盛把 AI 伺服器 PCB 市場上調到 2027 年約 375 億美元、2028 年約 840 億美元（單一券商），持久性未經下行期驗證。"},{"item":"決策層級","level":"🟡","text":"替代性要在料號認證層級看：伺服器與記憶體板需通過客戶認證，短期換供應商有成本；但一線廠滿載時訂單能外溢到健鼎，代表客戶在認證過的多家供應商間依產能分配，產能一鬆訂單也能流回。漲價後流失率、續約與認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的稀缺點在上游材料（Morgan Stanley 估 HVLP4 銅箔 2027 年短缺 31%，Panasonic 停產標準玻纖布 CCL）與承接高階 AI 主板的一線廠；健鼎站在中間，下游含美光、海力士等集中買方。目前毛利率創高顯示吃得到組合紅利，但最難取代的環節不在健鼎。"},{"item":"社會容忍度","level":"🟢","text":"B2B 零組件，終端消費者看不到 PCB 價格，不依賴監管授權，沒有社會定價天花板；關稅屬貿易政策風險，另列在風險項。"}],"roiic":"代理約 125%（FY2023→FY2025 營業利益增約 63 億元、稅後約 50 億元，÷同期淨利減自由現金流合計約 40 億元），屬循環回升期讀數，不代表新增產能的報酬，不可外推。","reinvest_rate":"FY2025 約 43%（1−自由現金流 58.3 億元÷淨利 102.2 億元）；TTM FCF 利潤率 −2.65%，再投資已超過盈餘。","endo_ceiling":null,"formula_note":"內生成長＝增量報酬×再投資率；事實表沒有資產負債表、年度資本支出與折舊拆分，投入資本與增量報酬無法正式計算，天花板留空；淨利減自由現金流只作再投資方向的代理。"}}}},"q3_growth":{"verdict":"五年後跑道中等（🟡）：成長來自量與組合，共識 FY2025→FY2027 EPS 年化約 34%，其中 2026 年營收 +32%、EPS +44%，差距 12 個百分點來自利潤率擴張；券商的 AI PCB 預測只看到 2028 年，Y5 之後沒有已證實的第二條成長曲線。","reasoning":"成長是量（伺服器、記憶體板出貨）加組合（高層數板拉高毛利率），無併購、無回購。共識（S&P Global 經 StockAnalysis，2026-08-01、Q2 財報前，家數未揭露）：FY2026E 營收約 969 億元（+32%）、EPS 27.94 元（+44%），FY2027E EPS 34.75 元；以 FY2025 實際 19.36 元為基期，兩年年化約 34%；FY2028E 事實表未涵蓋，因此用兩年。內生天花板無法正式計算（見報酬持續期），缺口歸因利潤率擴張：FY2025 毛利率 25.88% → Q2 2026 30.02%、營益率 17.63% → 22.56%，不是淨回購或收購。產能：2026 年資本支出逾 100 億元（前高 80 億元），仙桃三廠到位、越南新廠每月約 30 萬呎 2026 下半年貢獻，量的成長有產能支撐。跑道：滲透率口徑事實表未涵蓋；AI 伺服器 PCB 市場券商預測到 2028 年仍大幅成長，ASIC 主板切入僅屬法人預期，Y5 之後沒有 sourced 的第二條曲線，判中等。衰退信號亮 1 個（EPS 成長遠快於營收），自由現金流對淨利接近亮燈。","fact_refs":["f_kpi7","f_kpi6_7","f_kpi8_2026","f_kpi0_ifrs","f_kpi1","f_kpi3_gaap_ifrs_non_gaap"],"verdict_values":{"growth":{"driver_mix":"量（伺服器、記憶體板出貨）＋組合（高層數伺服器板拉高毛利率）為主；無併購、無回購。","runway_years":"約 2–3 年可見度（券商 AI PCB 預測止於 2028 年）；滲透率口徑事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"事實表沒有資產負債表、年度資本支出與折舊拆分，增量報酬與投入資本無法正式計算，天花板留空。代理讀數：FY2025 自由現金流÷淨利 0.57、TTM 自由現金流為負，再投資率已超過盈餘；FY2023→FY2025 營業利益增約 63 億元、同期淨再投資代理約 40 億元，增量報酬看似極高但主要來自稼動率與組合回升。共識兩年 EPS 年化約 34% 主要靠利潤率擴張，按超出天花板處理。","segments":[{"item":"伺服器板","value":"Q2 2026 占營收 42.2%，YoY +70.4%；承接一線廠外溢的一般伺服器訂單"},{"item":"記憶體模組板","value":"占 23.1%，YoY +99.6%；客戶含美光、海力士，法人估占比可升到 25% 以上"},{"item":"其他（筆電、車用、手機等）","value":"約 34.7%；車用庫存去化、手機季節性調整，2026 年僅小幅成長"}],"decay_signals":[{"item":"毛利率連 2 季 YoY 下滑","lit":false,"text":"未亮：Q2 2026 毛利率 30.02% 為四年新高"},{"item":"核心市占近 12 個月縮減","lit":false,"text":"未亮：一般伺服器訂單外溢流入"},{"item":"EPS 成長顯著高於營收成長","lit":true,"text":"亮：FY2023→FY2025 EPS 年化 30.0%、營收 11.7%，差 18 個百分點；2026 年共識 EPS +44%、營收 +32%"},{"item":"FCF/淨利 <0.75 連 2 年","lit":false,"text":"接近亮燈：FY2025 為 0.57、TTM 自由現金流為負；FY2026 若仍低於 0.75 即亮"},{"item":"其餘六類（提價後銷量、股份基礎給付、TAM 萎縮、產業倍數下移、維持性資本支出、停止投資新產能）","lit":false,"text":"未見訊號；股份基礎給付與維持性資本支出拆分事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置是擴產優先、配息照發：2026 年資本支出逾 100 億元創新高，TTM 自由現金流轉負，股息靠帳上淨現金支應；無併購、事實表未見回購，股數四年無淨稀釋。","reasoning":"現金轉換：自由現金流÷淨利 FY2022 1.41、FY2023 2.08、FY2024 1.04、FY2025 0.57（yfinance 年度財報），TTM FCF 利潤率 −2.65%；Q2 2026 營業現金流 −6.06 億元、資本支出 29.27 億元、自由現金流 −35.33 億元，獲利創高的一季營業現金流為負，應收或存貨墊高（拆分事實表未涵蓋）。資本支出：2026 年逾 100 億元，高於前高 80 億元。股東回報：TTM 股息殖利率 2.18%，約當每股 12.7 元、FY2025 EPS 的 66%，現金股利約 67 億元已高於 FY2025 自由現金流 58 億元，差額由淨現金支應（由 P/S 3.63 倍與 EV/S 3.39 倍之差推估淨現金約 200 億元）。無併購、事實表未涵蓋回購；淨利÷稀釋 EPS 推算股數 FY2022 約 5.31 億股、FY2025 約 5.28 億股、Q2 2026 約 5.26 億股，無淨稀釋。員工酬勞與股份基礎給付金額事實表未涵蓋。營運槓桿為正：FY2025 營收 +11.54%、營業利益約 +32.9%，沒有壓縮。現金去向四分與債務結構事實表未涵蓋。","fact_refs":["f_kpi5","f_kpi8_2026","f_dividend_yield_ttm","f_peer_3044_tw_fcf_margin_pct","f_kpi4_eps","f_ps_current","f_ev_s_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購紀錄（事件掃描未見併購）"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄；股東回報以現金股利為主，TTM 殖利率 2.18%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"淨利÷稀釋 EPS 推算股數：FY2022 約 5.31 億股、FY2025 約 5.28 億股、Q2 2026 約 5.26 億股，四年無淨稀釋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能（仙桃、越南）而非併購，資本回報以現金股利為主；現金去向四分與回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"582 元要求健鼎在同業擴產潮落地後仍守住 22% 以上營益率、2030 年 EPS 達約 51 元，我不信：那是 Bull 情境；Base 情境終端約 533 元，低於現價。","reasoning":"現價隱含什麼：要五年年化 8% 的報酬，2030 年股價需約 770 元，以 15 倍中循環倍數換算 EPS 要約 51 元，等於營益率在同業新產能落地後仍維持 22% 以上、營收比 2026 年再成長六成以上。Base 情境 2030 年 EPS 35.5 元×15 倍＝約 533 元，比現價低 8.5%，加上股息，五年報酬接近零。倍數：trailing 本益比 25.02 倍、P/S 3.63 倍、EV/S 3.39 倍都高於過去四個年度端點；以共識計 FY2026E 約 20.8 倍、FY2027E 約 16.7 倍。PEG 約 0.6 看似便宜，但分母站在高峰利潤率上，循環股不用它判便宜。賣方：6 位分析師平均目標 610 元、區間 570–666 元，資料最新為 2026-05，現價只差 4.8%；Q2 財報後法人上調目標價但數字未取得。同業本益比事實表未涵蓋，無法做同業倍數對照。市場錯在哪：用四年最高的倍數定價高峰利潤，等於假設擴產潮不會壓回利潤率。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_week26_return_pct","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"valuation":{"basis":"循環股以前瞻本益比對照自身年度端點與共識倍數；同業倍數與股價淨值比事實表未涵蓋","tier":"一般伺服器與記憶體板二線廠（高階 GPU／ASIC 主板由一線廠主導）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比與股價，無法建立倍數對照；改以自身年度端點分位與共識倍數為錨"},"fwd_pe":20.8,"peg":0.61,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"倍數位置：trailing 本益比 25.02 倍、P/S 3.63 倍、EV/S 3.39 倍都在過去四個年度端點之上（分位 100；只有四個年度端點，非連續五年序列）。前瞻：現價÷共識 FY2026E 27.94 元＝約 20.8 倍、÷FY2027E 34.75 元＝約 16.7 倍。PEG＝20.8÷兩年共識年化 34%＝約 0.61，但分母站在高峰毛利率上，不採信為便宜證據。現價距賣方平均目標 610 元僅 4.8%（資料最新 2026-05）。Base 情境終端約 533 元低於現價，判偏貴。","upside_short_pct":4.8,"upside_mid_pct":-8.5,"denominator_disputed":true,"denominator_note":"分母（FY2026–FY2027 共識 EPS）建立在 30% 毛利率與一線廠外溢訂單上，是否為循環高峰利潤正是本案爭點；PEG 0.6 的便宜論證因此不成立，改以中循環 EPS 與 15 倍錨定。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把結構性組合升級當成循環高峰；但即使組合升級成立，582 元也已反映大半，看錯的代價主要是錯過上漲，不是虧損。","reasoning":"最可能看錯的方向有三。（一）組合升級是結構性的：FY2023 營收衰退 10.5% 時毛利率反而由 17.95% 升到 19.34%、EPS 只減 2%，若高層數伺服器與記憶體板已把利潤率中樞墊高到 25% 以上，Base 情境 15 倍×35.5 元太保守，合理值會接近 Bull。（二）ASIC 主板設計案落地：目前只是法人預期，若成真，份額流入就從外溢變成規格贏單，護城河方向應改判擴大。（三）Bear 太輕：記憶體與 AI 拉貨同時反轉、中國產能遇上關稅，EPS 可能跌破 FY2025 的 19 元。價值陷阱判讀黃燈：十類衰退信號亮 1 個（EPS 成長遠快於營收），自由現金流÷淨利 FY2025 0.57、TTM 為負，FY2026 若仍低於 0.75 即亮第二個；三視角反證見反證紀錄。","fact_refs":["f_kpi1","f_kpi5","f_pe_percentile","f_week26_return_pct","f_peer_3044_tw_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰利潤率風險：獲利成長遠快於營收，自由現金流轉負"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":23.26,"pe":25.02,"basis":"TTM（2025Q3–2026Q2）稀釋 EPS 約 23.26 元，由現價 582 元÷trailing 本益比 25.02 倍推回；事實表股價單位標 USD，實為新台幣；終端倍數同為 trailing 口徑"},"eps":{"bull":[31.0,41.0,47.0,51.0,55.0],"base":[29.5,35.0,34.0,32.0,35.5],"bear":[28.0,25.0,19.5,19.0,21.0]},"pe":{"bull":20,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.18,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"max_dd":{"lo":-65,"hi":-45,"basis":"現價 582 元高出 52 週線 44%，26 週漲 58%；跌回 104 週線 309 元為 −47%、跌回 250 週線 205 元為 −65%；循環轉折時股價常回到長週期均線，Bear 情境終點跌幅約 57%；下限取 250 週線、上限取 104 週線附近；歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"健鼎切入 ASIC 主板、越南新廠滿載，AI 伺服器 PCB 市場依高盛預測 2028 年擴到 840 億美元，營益率守在 22–24%、營收 2030 年約 1,700 億元；終端 20 倍約等於現價對 FY2026 共識的前瞻倍數 20.8 倍","base":"FY2027 達共識 34.75 元附近後，同業新產能投產使營益率由 22% 回到 18–19%，2029 年記憶體下行小幅衰退、2030 年回升；終端 15 倍為中循環倍數，低於現價對 FY2027 共識的 16.7 倍；同業本益比事實表未涵蓋","bear":"同業擴產集中投產、外溢訂單回流一線廠、記憶體與 AI 拉貨同時轉弱，營益率退回 FY2024 的 15% 左右，EPS 回到 19–21 元；終端 12 倍取自成長熄火測試（成長降至 15%／10%／5% 時倍數約 18／13／10 倍，只有 15% 一檔股價不跌）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"中國與海外同業 2026 年起大幅擴產（勝宏投資計畫最高人民幣 200 億、為前一年 5–6 倍，滬電子公司擬投 55 億人民幣），分析師示警新產能集中投產而 AI 終端需求不及預期時會陷入低價競爭","assumption":"健鼎的外溢訂單與 30% 毛利率在新產能落地後仍保得住","consequence":"營益率退回 15%、EPS 回到 20 元左右、倍數壓到 12 倍 → 股價約 250 元，五年虧損過半","ruling":"採納：列為 Bear 情境（機率 30%）；與唯一致命點是同一機制，兩者一致，不重複計","watch":"月營收 YoY、季毛利率、一線廠新產能投產時點","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"Q2 2026 營業現金流 −6.06 億元、資本支出 29.27 億元，自由現金流 −35.33 億元；2026 年資本支出逾 100 億元創新高；上游缺料由高階擴散到標準 FR-4，中國 CCL 廠停供部分厚度","assumption":"營收與獲利創高會轉成股東拿得到的現金","consequence":"獲利創高但營運資金與擴產吃光現金，股息靠淨現金支應；若材料備貨成常態，自由現金流÷淨利長期低於 0.5，股東實得報酬落後帳面 EPS","ruling":"部分採納：擴產期自由現金流為負屬正常，但獲利創高的一季營業現金流為負不尋常；應收與存貨拆分事實表未涵蓋，無法判斷是備料還是收款放慢，以 FY2027 上半年自由現金流為驗證點","watch":"FY2027 上半年自由現金流、營業現金流是否轉正","evidence_refs":["geo_supply_chain#2"],"fact_refs":["f_kpi5","f_kpi8_2026","f_peer_3044_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"trailing 本益比 25.02 倍、P/S 3.63 倍、EV/S 3.39 倍皆高於過去四個年度端點；26 週漲 58.2%；現價高出 52 週線 44%，距賣方平均目標 610 元只差 4.8%","assumption":"市場用的 2027 年獲利是可延續的中樞","consequence":"即使 FY2027 EPS 達共識 34.75 元，倍數回到 15 倍股價約 520 元，比現價低 10%","ruling":"採納：這是本次不追的主因","watch":"股價與 52 週線距離、賣方目標價更新","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_ma_w52"]},{"view":"論點失敗","evidence":"主力產能在中國江蘇無錫與湖北仙桃；中國製 PCB 輸美因多重懲罰性關稅有效稅率最高約 45%；越南新廠每月約 30 萬呎、2026 下半年才開始貢獻","assumption":"關稅與去中化要求不會落到健鼎主要客戶的訂單上","consequence":"客戶要求非中國產地而越南產能接不住，訂單轉向台灣或東南亞產能的同業","ruling":"部分採納：來源描述的是產業背景、未直接指涉健鼎，客戶出貨路徑事實表未涵蓋；不預測關稅，以關稅變動後毛利率季減 ≥2 個百分點作吸收失敗判定","watch":"關稅公告後一季毛利率、越南新廠爬坡進度","evidence_refs":["geo_supply_chain#0","reg_tariff_export#2","geo_supply_chain#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 582.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=582.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：近兩季基本面","cause":null,"prior_field":null,"side_a":"Q2 2026 營收、毛利率、EPS 皆優於預期；7、8 月營收續創新高；Q2 後法人上調 2026、2027 年獲利預估","side_b":"空方也不否認近兩季動能，爭點在 2027 年同業新產能落地後的利潤率","ruling":"一致：短期基本面不是爭點，爭點在利潤率持續期","evidence_level":"高：財報與月營收公告","settle_metric":"季毛利率","if_then":["Q3 2026 毛利率低於 28% → 提前把唯一致命點的監測窗口拉到 2026Q4"],"evidence_refs":["capital_markets_pricing#0","end_markets#0"]},{"axis":"上游缺料：保護健鼎還是擠壓健鼎","cause":null,"prior_field":null,"side_a":"缺料是規格驅動的結構性週期：Morgan Stanley 估 HVLP4 銅箔 2027 年短缺 31%、2028 年仍缺 20%，缺料蔓延到標準 FR-4，供給吃緊撐住 PCB 報價","side_b":"缺口在上游材料，成品板產能反而在擴：中國與海外同業 2026 年投資計畫放大 5–6 倍、未見供給紀律；材料短缺推高的是健鼎的成本，不是健鼎的議價力","ruling":"不可調和，選 B 側。依據：缺料保護的是材料商的利潤池；健鼎 Q2 毛利率 30.02% 創高的主因是伺服器與記憶體組合，不是報價權；成品板新產能 2027 年後落地，屆時材料仍緊、成品板轉鬆，健鼎兩頭受壓。硬數據點是季毛利率與月營收 YoY。","evidence_level":"中：券商報告轉述與產業新聞，無公司逐字稿","settle_metric":"2027 年上半年季毛利率與月營收 YoY","if_then":["若 2027 年上半年季毛利率仍 ≥28% 且月營收 YoY 為正 → 改判 A 側成立，進場價上調到 480 元（約 FY2027 共識 13.8 倍），首倉 2%","若季毛利率季減 ≥2 個百分點且公司歸因材料成本 → 不進場；持有者減碼一半"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","geo_supply_chain#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"Q2 EPS 7.41 元高於預估 6.97 元，7 月營收 YoY +56.55%、8 月營收創新高，Q2 後法人上調 2026、2027 年獲利；以 FY2027 共識 34.75 元計只有約 16.7 倍；FY2023 營收衰退 10.5% 時 EPS 只減 2%，下行韌性比一般 PCB 廠好；週線多頭排列完整","side_b":"上修的 EPS 站在 30% 高峰毛利率上；trailing 本益比 25 倍高於過去四個年度端點、26 週漲 58%；Base 情境五年報酬接近零，Bull 機率 25% 漲約 89%、Bear 機率 30% 跌約 57%，上下檔不對稱不明顯","ruling":"可調和（程度差異）：近期基本面動能是真的，但 582 元已先把 2027 年的好結果算進去；不追，等價格或利潤率證據","evidence_level":"中","settle_metric":"股價與季毛利率","if_then":["股價續漲而季毛利率未再創高 → 不追","股價跌回 410 元以下且季毛利率 ≥27% → 分批反買，首倉 2%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3","end_markets#0"]},{"axis":"成長集中在兩個循環終端","cause":null,"prior_field":null,"side_a":"伺服器板 YoY +70.4%、記憶體板 YoY +99.6%，合計占營收 65.3%","side_b":"車用板進入庫存去化、手機板因前一年提前拉貨進入季節調整，其他業務 2026 年只小幅成長，約占營收 35% 的部分沒有提供緩衝","ruling":"可調和：成長引擎單一化不推翻近期獲利，但 AI 伺服器拉貨與記憶體循環同時轉弱時沒有第二支腳，已反映在 Bear 機率 30%","evidence_level":"中：法說報導與投顧拆分","settle_metric":"伺服器＋記憶體占比與月營收 YoY","if_then":["記憶體板占比回落到 18% 以下且月營收 YoY 轉負 → 持有者減碼一半","非 AI 業務 YoY 回到雙位數 → 情境樹 Bull 機率上調 5 個百分點"],"evidence_refs":["end_markets#2","end_markets#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：高盛把 AI 伺服器 PCB 市場上調到 2027 年約 375 億美元、2028 年約 840 億美元，花旗上調中國 AI-PCB 規模，全球 PCB 2026 年 1,137 億美元；上游材料短缺被視為結構性","side_b":"競爭惡化：中國與海外同業 2026 年大幅擴產、未見供給紀律；其他結構變數：中國製 PCB 輸美有效稅率最高約 45%，健鼎主力產能在中國，越南新廠 2026 下半年才開始貢獻","ruling":"雙向拉鋸：需求面結構轉好有多家券商數據，供給面競爭惡化與關稅風險同時成立；勝負要到 2027 年新產能投產後才見分曉，在那之前不給溢價","evidence_level":"中：多家券商估計與產業新聞","settle_metric":"2027 年月營收 YoY 與季毛利率","if_then":["2027 年同業新產能投產後健鼎季毛利率仍 ≥27% → 判結構轉好勝出，進場價上調到 480 元","2027 年任一季毛利率跌破 25% → 判競爭惡化勝出，清倉"],"evidence_refs":["supply_demand_durability#4","supply_demand_durability#5","supply_demand_durability#6","supply_demand_durability#2","reg_tariff_export#2","geo_supply_chain#0"]},{"axis":"配息照發與擴產燒錢","cause":null,"prior_field":null,"side_a":"TTM 股息殖利率 2.18%，約每股 12.7 元、FY2025 EPS 的 66%","side_b":"TTM 自由現金流為負、Q2 2026 自由現金流 −35.33 億元，2026 年資本支出逾 100 億元；現金股利約 67 億元已高於 FY2025 自由現金流 58 億元","ruling":"可調和：淨現金約 200 億元（市值×(1−EV/S÷P/S) 推估）足以支應一到兩年；FY2027 自由現金流若仍為負，配息率下修機率升高，股息不能當下檔支撐","evidence_level":"中：年度財報與最新一季現金流，資產負債表事實表未涵蓋","settle_metric":"FY2027 半年度自由現金流","if_then":["FY2027 上半年自由現金流轉正 → 維持股息假設","FY2027 上半年自由現金流仍為負 → 停止加碼，情境樹股息殖利率下修到 1.5%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 410 元以下且最近一季毛利率仍 ≥27%：重跑研究後建首倉","type":"估值rearm","maps_to":"H1","metric":"股價＋季毛利率","threshold":"股價 ≤410 元且季毛利率 ≥27%","action":"兩條件同時成立後首倉 2%","source_freq":"每日收盤價＋季報","date":null},{"n":2,"text":"任一季毛利率跌破 25%：同業新產能投產後價格戰成真","type":"Single Thing","maps_to":"Single Thing","metric":"季毛利率","threshold":"<25%","action":"清倉；未持有者撤銷進場條件","source_freq":"季報（每季）","date":"2026Q4–2027Q4","evidence_refs":["supply_demand_durability#2"]},{"n":3,"text":"月營收 YoY 連 3 個月轉負：外溢訂單回流或記憶體下行","type":"風險","maps_to":"R1","metric":"月營收 YoY","threshold":"連 3 個月 <0%","action":"減碼一半；未持有者不進場","source_freq":"月營收公告（每月 10 日前）","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"毛利率季減 ≥2 個百分點且公司歸因材料成本：缺料轉嫁失敗","type":"風險","maps_to":"R2","metric":"季毛利率季變化","threshold":"季減 ≥2 個百分點且歸因材料","action":"減碼三分之一","source_freq":"季報＋法說會","date":null,"evidence_refs":["geo_supply_chain#2"]},{"n":5,"text":"FY2027 上半年自由現金流仍為負：擴產回收慢於預期","type":"假設驗證","maps_to":"H2","metric":"半年度自由現金流","threshold":"<0","action":"停止加碼","source_freq":"半年報","date":"2027-08"},{"n":6,"text":"美國對中國製 PCB 關稅變動後一季毛利率季減 ≥2 個百分點：關稅吸收失敗","type":"風險","maps_to":"R3","metric":"季毛利率＋公司關稅歸因","threshold":"季減 ≥2 個百分點且公司歸因關稅或轉單","action":"減碼一半","source_freq":"季報＋法說會","date":null,"evidence_refs":["geo_supply_chain#0","reg_tariff_export#2"]},{"n":7,"text":"2026-09-21 重訊澄清報導的內容不明：若後續揭露涉及主要客戶、訂單或產能","type":"風險","maps_to":"R1","metric":"重大訊息","threshold":"內容涉及客戶、訂單或產能變動","action":"暫停任何進場；持有者減碼三分之一直到內容明朗","source_freq":"公開資訊觀測站重訊（不定期）","date":"2026-09-21 起","evidence_refs":["major_events#0"]},{"n":8,"text":"Q3 2026 財報複審：7、8 月營收已創新高，檢查毛利率與營業現金流","type":"複審日期","maps_to":null,"metric":"Q3 毛利率、營業現金流","threshold":"毛利率 ≥28% 且營業現金流轉正","action":"未達標則維持不進場並下修 Bull 機率 5 個百分點","source_freq":"季報","date":"2026-11"}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"任一季 <25%","window":"2026Q4–2027Q4","source":"公開資訊觀測站季報","last_status":"ok"},{"metric":"月營收 YoY","bear_threshold":"連 3 個月 <0%","window":"2026-11 至 2027-12","source":"公開資訊觀測站月營收公告","last_status":"ok"},{"metric":"年度自由現金流÷淨利","bear_threshold":"FY2027 <0.3 或自由現金流仍為負","window":"FY2027","source":"年報現金流量表","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤410元且最近一季毛利率≥27%，兩條件同時成立後重跑研究並建首倉","exec_line":"綁定約束是價格：Base 情境五年報酬近零。未持有不追；持有者不加碼，月營收 YoY 連 3 個月轉負減碼一半，任一季毛利率跌破 25% 清倉"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用四年最高的倍數定價高峰利潤，等於假設同業 2026 年放大 5–6 倍的擴產在 2027 年後落地時不會壓回健鼎 30% 的毛利率；擴產規模與投產時點已公開，倍數卻停在歷史端點之上。","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 410 元以下（約 52 週線 404 元、FY2027 共識 EPS 的 11.8 倍）且最近一季毛利率仍 ≥27%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用四年最高的倍數定價高峰利潤，等於假設同業 2026 年放大 5–6 倍的擴產在 2027 年後落地時不會壓回健鼎 30% 的毛利率；擴產規模與投產時點已公開，倍數卻停在歷史端點之上。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=58.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"伺服器＋記憶體板撐住高利潤率：兩者合計占營收 ≥60%，季營益率 ≥20%","2y":"到 2028 年中季營益率維持 20% 以上（Q2 2026 為 22.56%），伺服器＋記憶體占比維持 60% 以上（Q2 2026 為 65.3%）","5y":null,"10y":null,"threshold":"季營益率 ≥20% 且伺服器＋記憶體占營收 ≥60%","source":"公開資訊觀測站季報、法說會簡報、投顧產品組合拆分","drift_rule":"季營益率連 2 季低於 19% 視為削弱；連 3 季低於 18% 視為反轉"},{"id":"H2","text":"擴產期現金消耗在 2027 年止血：FY2027 自由現金流轉正，自由現金流÷淨利 ≥0.5","2y":"FY2027 年度自由現金流÷淨利 ≥0.5（FY2025 為 0.57，TTM 為負，Q2 2026 自由現金流 −35.33 億元）","5y":null,"10y":null,"threshold":"FY2027 年度自由現金流÷淨利 ≥0.5","source":"半年報與年報現金流量表","drift_rule":"FY2027 上半年自由現金流仍為負視為削弱；FY2027 全年仍為負視為反轉"},{"id":"H3","text":"擴產潮落地後利潤率中樞已墊高：FY2028 起年度毛利率守在 25% 以上（FY2022 為 17.95%、FY2025 為 25.88%）","2y":null,"5y":"FY2028–FY2030 年度毛利率皆 ≥25%，營益率 ≥18%","10y":null,"threshold":"年度毛利率 ≥25%","source":"年報與季報損益表","drift_rule":"季毛利率連 4 季低於 23.75% 視為削弱；連 6 季低於 22.5% 視為反轉"}],"R":[{"id":"R1","text":"同業擴產集中投產，一般伺服器板外溢訂單回流一線廠並陷入價格競爭","h_ref":"H3","clock":"🔥","threshold":"月營收 YoY 連 3 個月 <0%，或季毛利率 YoY 連 2 季下滑","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#0"]},{"id":"R2","text":"上游銅箔、玻纖布、CCL 缺料推升成本且無法轉嫁","h_ref":"H1","clock":"⚡","threshold":"季毛利率季減 ≥2 個百分點且公司歸因材料成本","evidence_refs":["geo_supply_chain#2","supply_demand_durability#1"]},{"id":"R3","text":"產能集中中國無錫與仙桃，美國關稅或客戶非中國產地要求轉不出去","h_ref":"H3","clock":"🐢","threshold":"關稅變動後一季毛利率季減 ≥2 個百分點，或公司揭露客戶要求轉移產地","evidence_refs":["geo_supply_chain#0","reg_tariff_export#2"]},{"id":"R4","text":"記憶體循環反轉：記憶體板 YoY +99.6% 的高基期回落","h_ref":"H1","clock":"🔥","threshold":"記憶體板占營收回落到 18% 以下，或月營收 YoY 轉負","evidence_refs":["competitive_share_entrants#2"]}],"single_thing":{"description":"2027 年前任一季毛利率跌破 25%（同業新產能投產、外溢訂單回流後的價格戰訊號）","why_fatal":"情境樹裡最大的單一敏感度是營益率：營益率每少 3 個百分點，2030 年 EPS 約少 15%；毛利率跌破 25% 等於營益率回到 FY2024 的 15% 附近，EPS 掉回 20 元、股價落入 Bear 區","if_happens":"清倉；未持有者撤銷進場條件，改等新一輪循環谷底","how_monitor":"季報毛利率（每季）＋月營收 YoY（每月 10 日前）","probability":"約 30%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.7,"peg_fy2":0.49,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":19.36,"FY2026E":27.94,"FY2027E":34.75,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（新台幣）；共識取 S&P Global（經 StockAnalysis，2026-08-01，Q2 財報前），家數未揭露；FY2028E 事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"Q3 2026 財報（7、8 月營收已創新高）","impact":"中","watch":"毛利率能否守在 30% 附近、營業現金流是否轉正"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"越南周德新廠開始貢獻產出（規劃每月約 30 萬呎）","impact":"中","watch":"新廠爬坡期對毛利率的稀釋幅度"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"中國同業擴產產能陸續投產","impact":"高","watch":"一般伺服器板報價與健鼎月營收 YoY"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
