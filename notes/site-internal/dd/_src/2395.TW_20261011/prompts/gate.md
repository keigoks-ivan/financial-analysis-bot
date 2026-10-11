你是 DD 管線 v20 的判斷層閘（gate），標的 2395.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝26126 NT$百萬（YoY +46%、QoQ +28%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi1_non_gaap_gaap`（q1_business）｜Non-GAAP 營業利益／利益率（公司不另報，以 GAAP 為準）＝19.6 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
  - 註記：營收與營益率優於公司財測，毛利率低於財測（來源：wantrich/ctee 報導）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝5127 NT$百萬，營業利益率 19.6%（YoY +64%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi3`（q1_business）｜毛利率＝37.7 %（YoY −2.31pp；毛利 NT$9,845M）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
  - 註記：低於公司財測；管理層歸因短期關鍵原物料價格波動
- `f_kpi4_eps`（q1_business）｜稅後淨利／EPS＝5.2 NT$/股（淨利 NT$4,518M，YoY +127%、QoQ +36%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi7`（q1_business）｜管理層指引＝— 無數字指引｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi8_book_to_bill`（q1_business）｜Book-to-bill＝1.44 倍（北美 1.92、歐洲 1.25、中國 1.21）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：研華公司新聞稿 https://www.advantech.com/zh-tw/resources/news/研華公告2026年第二季每股盈餘520元（numbers.latest_quarter_kpis.items[8]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi9`（q1_business）｜庫存＝20908 NT$百萬；約 116 天（庫存 ÷ 單季營業成本 16,281 × 90，自行換算）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow／balance_sheet（依公司合併報表）（numbers.latest_quarter_kpis.items[9]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_peer_2395_tw_gross_margin_pct`（q2_moat）｜2395.TW 毛利率＝39.0 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2395.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2395_tw_operating_margin_pct`（q2_moat）｜2395.TW 營業利益率＝17.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2395.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2395_tw_fcf_margin_pct`（q2_moat）｜2395.TW FCF 利潤率＝1.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2395.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6166_tw_gross_margin_pct`（q2_moat）｜6166.TW 毛利率＝35.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6166.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6166_tw_operating_margin_pct`（q2_moat）｜6166.TW 營業利益率＝9.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6166.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3088_two_operating_margin_pct`（q2_moat）｜3088.TWO 營業利益率＝11.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3088.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6414_tw_gross_margin_pct`（q2_moat）｜6414.TW 毛利率＝20.33 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6414.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2397_tw_fcf_margin_pct`（q2_moat）｜2397.TW FCF 利潤率＝-1.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2397.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝46.28 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.69 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.535 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝833 NT$百萬（OCF 1,553，CapEx 720）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow／balance_sheet（依公司合併報表）（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝1.1 %（SBC NT$55.7M）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-31）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow／balance_sheet（依公司合併報表）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-31））
- `f_peer_6166_tw_fcf_margin_pct`（q2_moat）｜6166.TW FCF 利潤率＝6.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6166.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6414_tw_fcf_margin_pct`（q2_moat）｜6414.TW FCF 利潤率＝4.29 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6414.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3088_two_fcf_margin_pct`（q2_moat）｜3088.TWO FCF 利潤率＝3.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3088.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝727.0 TWD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.48 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝113.4 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：2025Q3 DDR4供應緊俏使研華毛利率約降1個百分點，DDR4短缺衝擊整個工業電腦供應鏈
  - 來源：Digitimes via Borecraft 2025-11-06（as_of 2025-11-06）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：2026年5月Digitimes報導：研華第一季接單大增，但零組件供應吃緊與材料成本上升可能限制近期成長
  - 來源：Digitimes: Advantech warns supply constraints will temper near-term growth despite strong order momentum（as_of 2026-05-01）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：2025年8月研華表示，多數產品受衝擊程度取決於 Section 232 調查結果；計畫將大部分成本轉嫁客戶，並與少數客戶協商分攤。
  - 來源：Taipei Times 2025-08-07 (Advantech / Section 232)（as_of 2025-08-07）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2025年4月報導：北美占研華2024年營收約31%，研華與美國客戶討論關稅轉嫁與價格調整。
  - 來源：中央社 2025-04-07（as_of 2025-04-07）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：中國廠商 Beilai (BLIIoT) 發布 2026 年新一代工業邊緣產品，規劃 ARM 架構工業 PC 與可跑 OpenPLC/CODESYS 軟 PLC 的 EdgePLC 控制器（低價同類競品）
  - 來源：BLIIoT: Beilai Tech Announces 2026 Next-Generation Industrial Edge Products（as_of 2026-01-01）｜affects：decision_inputs.bear、moat_trend
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：風險面：記憶體成本壓力可能擴大到 CPU 與 PCB；研究機構認為需求強勁、研華可望轉嫁大部分新增成本。
  - 來源：搜尋結果彙整自 2026-08 法說會後報導（as_of 2026-08-06）｜affects：decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1610.0,"bear_5y_price":390.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":21.3,"ev5y_pct":26.1,"irr_base_pct":3.9,"asym_ratio":2.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":15.71,"pe":46.28,"basis":"最近四季（截至 2026-06-30）GAAP 稀釋 EPS，由現價 727 元÷Trailing P/E 46.28 倍推得，與終端倍數同為落後四季口徑；路徑 Y1–Y5 對應 FY2027E–FY2031E"},"eps":{"bull":[26.5,31.0,36.0,41.0,46.0],"base":[23.0,24.0,26.5,29.0,31.5],"bear":[18.5,15.5,16.5,18.0,19.5]},"pe":{"bull":35,"base":28,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.535,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | none | 0 | 4 |
| customer_concentration_credit | none | 0 | 2 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | found | 4 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 2 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | none | 0 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：研華 2395 最大客戶 單一客戶 集中度 第二供應商 自製 2026；Advantech 2395.TW largest customer concentration single-source risk customer diversify supplier；研華 客戶分散 無單一客戶超過 10% 營收 年報 主要銷貨客戶；Advantech NVIDIA edge AI customers in-house design industrial PC insourcing 2026
- **customer_concentration_credit**（none）：研華 2395 前十大客戶 營收比重 客戶集中度 2026；Advantech 2395.TW customer concentration risk top customer revenue share annual report
- **regulatory_antitrust**（none）：研華 Advantech 2395 antitrust OR regulation OR export controls 2026；研華 公平交易委員會 OR 反壟斷 OR 調查 2026
- **major_events**（none）：研華 2395 Advantech acquisition merger 2025 2026；研華 2395 Advantech class action lawsuit securities fraud；研華 Advantech product recall warning investigation restatement 2026；研華 重大訊息 訴訟 裁罰 金管會 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2395.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"研華"},"oneliner":"全球工業電腦份額第一，邊緣 AI 帶動訂單與獲利創高；但現價已是樣本最高倍數，部分訂單是零組件短缺下的提前下單，等價格回落或接單消化的證據再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"研華賺的是工業設備商與系統整合商的邊緣運算硬體錢。錢落在設計導入後長期出貨的板卡與系統，毛利則被上游記憶體與 CPU 卡住","reasoning":"最新一季營收 261.26 億元，年增 46%、季增 28%。毛利率 37.7%，低於公司財測 38%–40%，年減 2.31 個百分點，管理層歸因於原物料波動。營益率 19.6%，營業利益年增 64%。上半年美元營收 14.7 億美元、年增 33%。分事業群：iSystems 年增 34%（半導體設備、雲端網通設備），Embedded 28%（智慧醫療、自動化設備、機器人專案），iAutomation 19%，iService 只有個位數。分地區：中國年增 51%、北美 30%，北美約占 2024 年營收 31%。各事業群營收占比事實表未涵蓋，所以占比超過一成的分部無法逐一列出。邊緣 AI 營收占比由 2023 年 4% 升到上半年 22.5%，公司目標年底 30%，專案毛利約 40%。單點依賴：客戶集中度查無資料；上游記憶體與 CPU 是實質單點，證據是 2025 年第三季 DDR4 吃緊讓毛利率少了約 1 個百分點，本季毛利率又低於財測。產業態勢分三面看。競爭面靜態：全球份額 8.6% 居首，但沒有消長資料；中國低價 ARM 工業電腦與軟 PLC 屬點狀攻擊。結構面轉好：AI 推動買家由 PLC 轉向配備加速器的工業電腦。其他結構變數是關稅，Section 232 衍生品範圍尚未確認。裁決為結構性轉好中，關稅與零組件成本兩面拉鋸。產業時鐘判擴張期：2024 年工業電腦市場明顯衰退，2025 年營收年增 18.6%，本季接單出貨比 1.44、7 月 1.64；不過提前下單、零組件短缺、交期拉長已經是過熱徵兆。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap_gaap","f_kpi2_gaap","f_kpi3","f_kpi4_eps","f_kpi7","f_kpi8_book_to_bill","f_kpi9"],"verdict_values":{"revenue_quality":"營收來自訂單驅動的硬體出貨。接單出貨比 1.44（北美 1.92、歐洲 1.25、中國 1.21），7 月升到 1.64；其中一部分是客戶為了鎖定記憶體等零組件而提前下單，週期性成分高","unit_econ_note":"毛利率 37.7%、營益率 19.6%，營業槓桿為正（營收年增 46%、營業利益年增 64%）。淨利年增 127%，高於營業利益增幅，主因是去年同季淨利只有營業利益的約 64%，基期偏低；本季回到約 88%，與 FY2022–FY2025 的 86%–99% 相符","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"高毛利、長尾客戶的工業電腦品牌。盈餘跟著工業資本支出與零組件庫存週期起伏：FY2023–FY2024 營收連兩年下滑，FY2022–FY2025 EPS 原地踏步。邊緣 AI 是結構性的第二曲線"},"industry":{"clock_phase":"II","sd_verdict_source":"供需分兩層。邊緣 AI 部署屬結構性持久：43% 的邊緣 AI 訂單交期超過六個月，客戶在規劃兩到三年的部署（媒體轉述）。記憶體短缺引發的提前下單屬週期性，將會反轉，2027–2028 年有消化期風險","bargaining":{"up":"上游記憶體、CPU、PCB 供應吃緊，議價權在上游；記憶體的成本壓力可能擴大到 CPU 與 PCB","down":"下游是分散的工業客戶。研華計畫轉嫁大部分關稅與新增成本，研究機構也認為需求強勁、轉嫁可行，但轉嫁有時間差","geo":"製造約台灣 45%、中國 45%，輸美出貨 93% 來自台灣；南加州第二個美國組裝據點預計 2026 年啟用；Section 232 是否涵蓋研華產品尚未確認"},"profit_pool_dir":"利潤池往軟硬整合的邊緣 AI 方案移動，研華邊緣 AI 營收占比從 2023 年 4% 升到上半年 22.5%；整體工業電腦利潤池的五年變化事實表未涵蓋","tam_table":[{"item":"全球工業電腦份額（2025）","value":"研華逾 8.6% 居首，前五大合計 25.9%"},{"item":"中國工業電腦份額","value":"研華逾 36%（無年度消長資料）"},{"item":"邊緣 AI 嵌入式 PC 年複合成長（2024–2030，第三方）","value":"14.6%，第三方口徑差異大"},{"item":"研華邊緣 AI 營收占比","value":"2023 年 4% → 2026 上半年 22.5%，目標年底 30%"},{"item":"AI 邊緣架構滲透","value":"視覺檢測已量產，軟體定義控制在早期量產，閉環製程控制仍在試點；第三方估約 2029 年成為新廠預設規格"},{"item":"TAM 金額、SAM 與營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行面在擴大，定價面被上游成本侵蝕，兩者相抵","reasoning":"機制：長尾工業客戶的設計導入，加上最廣的產品線與全球通路，讓研華以份額第一（全球逾 8.6%、中國逾 36%）換到約同業兩倍的營益率。可證方向：投入資本事實表未涵蓋，算不出對同業的 ROIC 差距，改用利潤率差距代理。近四季營益率 17.97%，比次佳同業 3088.TWO 的 11.46% 高約 6.5 個百分點；毛利率 39.0%，比 6166.TW 的 35.49% 高約 3.5 個百分點。這只是單期截面，差距在擴大還是收窄，事實表未涵蓋。份額也只有靜態值：凌華 1 月營收年增 43%、2 月 16%，研華第二季年增 46%，看不出消長。執行面判擴大，因為接單出貨比與邊緣 AI 占比雙雙走高；定價面判縮減，因為第二季毛利率年減 2.31 個百分點、低於財測。兩者合判穩定；沒有來源化的份額上升證據，所以不給上升。執行力 8 分、定價力 7 分。報酬持續期方面，當期 ROIC 無法計算；四檢查點裡需求基礎值、決策層級、價值鏈分配都只到中等，持續期的關鍵在於上游零組件的議價權會不會鬆動。","fact_refs":["f_peer_2395_tw_gross_margin_pct","f_peer_2395_tw_operating_margin_pct","f_peer_2395_tw_fcf_margin_pct","f_peer_6166_tw_gross_margin_pct","f_peer_6166_tw_operating_margin_pct","f_peer_3088_two_operating_margin_pct","f_peer_6414_tw_gross_margin_pct","f_peer_2397_tw_fcf_margin_pct","f_kpi3","f_kpi8_book_to_bill"],"verdict_values":{"moat":{"mechanism":"長尾工業客戶的設計導入與長生命週期出貨，加上最廣產品線與全球通路帶來的規模，換得約同業兩倍的營益率","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：接單出貨比第二季 1.44、7 月 1.64，邊緣 AI 營收占比從 2023 年 4% 升到上半年 22.5%。定價面縮減：第二季毛利率 37.7%，低於財測 38%–40%，年減 2.31 個百分點。兩者相抵判穩定；份額只有靜態值，沒有來源化的上升證據","competitor_notes":[{"name":"6414.TW","strategy_note":"毛利率 20.33%、營益率 5.78%，約為研華的一半與三分之一，屬走量的成本結構，對研華的定價不構成直接壓力"},{"name":"6166.TW","strategy_note":"毛利率 35.49%，最接近研華；但營益率 9.78% 只有研華一半多，研發密度 11.7% 為同業最高。產品面最接近的對手，規模不足以把毛利轉成營益"},{"name":"3088.TWO","strategy_note":"營益率 11.46% 為同業次高，毛利率 33.62%，自由現金流利潤率 3.3%，屬利基型對手"},{"name":"2397.TW","strategy_note":"毛利率 25.57%、自由現金流利潤率 −1.44%，價格導向；它同樣被營運資金吃掉現金，顯示備料壓力是全產業現象"}],"spread_notes":{"basis":"投入資本事實表未涵蓋，以近四季營益率與毛利率差距代理","op_margin_vs_best_peer_pp":6.51,"gross_margin_vs_best_peer_pp":3.51,"direction":"單期截面，擴大或收窄事實表未涵蓋"},"peer_na_reason":null,"threats":[{"level":"🟡","text":"中國廠商推出低價 ARM 架構工業電腦，以及可跑軟 PLC 的邊緣控制器。這是點對點的價格攻擊，主要威脅中國市場與低階產品線","p":"25%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"上游記憶體短缺與成本上升侵蝕毛利：2025 年第三季毛利率約少 1 個百分點，2026 年第二季又低於財測，壓力可能擴大到 CPU 與 PCB","p":"40%","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"level":"🟡","text":"美國關稅：北美約占營收三成，60% 北美訂單的關稅先由研華吸收再向客戶請款；若 Section 232 衍生品範圍涵蓋主力產品，轉嫁能力會受考驗","p":"20%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]}],"roic_durability":{"quadrant":"高利益率；周轉率事實表未涵蓋（缺投入資本），庫存約 116 天，顯示營運資金負擔偏重","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"客戶要解決的問題是工廠、醫療、半導體設備的邊緣運算，屬於需要而非想要，延後購買會拖慢產線升級。但目前訂單水位含有記憶體短缺下的提前下單，急迫性不等於持久性；2022 年短缺之後，FY2023–FY2024 營收連兩年下滑就是前例"},{"item":"決策層級","level":"🟡","text":"替代發生在設備商選定平台的那一刻，換供應商要重新設計與驗證。但漲價後流失率、重新認證週期、合約年限等代理變數事實表未涵蓋，只能用份額第一與約同業兩倍的營益率間接佐證"},{"item":"價值鏈分配","level":"🟡","text":"上游記憶體與 CPU 供應集中，短缺時先拿走價值：2025 年第三季 DDR4 讓毛利率少了約 1 個百分點，2026 年第二季毛利率 37.7% 低於財測。研華能轉嫁大部分成本，但有時間差；價值鏈中最難取代的環節不是研華"},{"item":"社會容忍度","level":"🟢","text":"研華賣的是 B2B 工業硬體，不依賴監管授權，也沒有民生必需品式的漲價天花板；關稅屬政策成本，已列入風險，不是社會容忍度的問題"}],"roiic":"事實表未涵蓋（缺投入資本，無法計算增量報酬率）","reinvest_rate":"近四季約 93%（自由現金流只剩淨利約 7%）；FY2022–FY2025 約 2%–35%","endo_ceiling":null,"formula_note":"再投資率以 1−自由現金流÷淨利代理（淨利含業外，不是稅後營業利益）：FY2022 23%、FY2023 23%、FY2024 2%、FY2025 35%，近四季約 93%。近四季的淨利率約 16.6%，由 P/S 7.69÷P/E 46.28 推得；自由現金流利潤率 1.21%。近四季的高再投資有一部分靠資產負債表撐：每股配息約 11.2 元（殖利率 1.535%×727 元），約為 FY2025 EPS 12.14 元的 92%，也約為近四季每股自由現金流 1.1 元的十倍。可持續的保留率約 8%，即使增量報酬率達 50%，內生成長上限也只有約 4%/年。當期 ROIC 與增量報酬率都需要投入資本，事實表未涵蓋。"}}}},"q3_growth":{"verdict":"跑道寬：全球份額只有 8.6% 的分散市場，加上邊緣 AI 第二曲線。但近期的高成長主要來自產能利用率、產品組合與週期，不是來自再投資","reasoning":"成長以量為主：各事業群上半年年增 19%–34%，接單出貨比 1.44。產品組合改善為輔：邊緣 AI 專案毛利約 40%，占比 22.5%。另有成本轉嫁帶來的價格成分；併購與回購沒有貢獻。三年共識 EPS 與分析師家數事實表未涵蓋，算不出共識年複合成長；法說後只有「全年營收首度破千億、EPS 大幅上修」的定性描述。高配息讓內生成長上限只有約 4%/年，推導見報酬持續期。Base 路徑由最近四季 15.71 元到 FY2031E 31.5 元，約 14%–15%/年；超出上限的部分，歸因於利潤率擴張（產能利用率與邊緣 AI 組合）和週期上行，其餘無法歸因，所以加註依賴 re-rate 與週期配合，長期信心上限為中。跑道：全球前五大合計只有 25.9%，研華 8.6%。第三方估邊緣 AI 嵌入式 PC 2024–2030 年複合成長 14.6%；軟體定義的 AI 邊緣架構約 2029 年成為新廠預設規格，閉環 AI 製程控制仍在試點，所以第二曲線有來源。衰退信號成立一個半：自由現金流／淨利 FY2025 為 0.65、近四季約 0.07；毛利率第二季年減 2.31 個百分點（第一季事實表未涵蓋）。","fact_refs":["f_kpi0_gaap","f_kpi3","f_kpi8_book_to_bill","f_pe_current","f_ps_current","f_dividend_yield_ttm","f_peer_2395_tw_fcf_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（接單出貨比 1.44、各事業群年增 19%–34%），組合為輔（邊緣 AI 專案毛利約 40%），另有部分成本轉嫁的價格成分；無併購與回購貢獻","runway_years":"≥10（全球份額 8.6%、前五大合計 25.9% 的分散市場）","runway_post_y5":"🟢","endo_ceiling_basis":"引報酬持續期的推導：保留率約 8%，即使增量報酬率達 50%，內生上限也只有約 4%/年。Base 路徑約 14%–15%/年，明顯超出上限，差額來自產能利用率、邊緣 AI 組合與週期","segments":[{"item":"iSystems","value":"上半年年增 34%（半導體設備、雲端網通設備）；營收占比事實表未涵蓋"},{"item":"Embedded","value":"上半年年增 28%（智慧醫療、自動化設備、機器人專案）"},{"item":"iAutomation","value":"上半年年增 19%（自動化設備、交通專案）"},{"item":"iService","value":"上半年僅個位數成長"},{"item":"邊緣 AI（跨事業群）","value":"營收占比 2023 年 4% → 上半年 22.5%，目標年底 30%，專案毛利約 40%"},{"item":"機器人","value":"上半年成長 250%，占比低"}],"decay_signals":[{"signal":"毛利率連兩季年減","status":"部分成立","evidence":"第二季年減 2.31 個百分點已確認，第一季事實表未涵蓋；FY2025 毛利率 39.78% 已低於 FY2024 的 40.77%"},{"signal":"核心市占近 12 個月縮減","status":"資料缺口","evidence":"只有靜態份額（全球逾 8.6%、中國逾 36%），沒有消長資料"},{"signal":"主力產品提價後銷量下滑","status":"不成立","evidence":"轉嫁成本的同時，接單出貨比仍有 1.44"},{"signal":"EPS 成長顯著高於營收成長","status":"不成立","evidence":"FY2022–FY2025 EPS 與營收都接近原地；近一年的差距來自營運槓桿與去年同季業外的低基期，不是多年趨勢"},{"signal":"自由現金流／淨利連兩年低於 0.75","status":"成立","evidence":"FY2025 為 0.65，近四季約 0.07；FY2026 全年待確認"},{"signal":"SBC 占營收逾 5% 且上升","status":"不成立","evidence":"第二季約 0.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"不成立","evidence":"AI 推動買家由 PLC 轉向配備加速器的工業電腦，屬順風"},{"signal":"產業估值倍數近三年系統性下移","status":"不成立","evidence":"自身倍數位在年度端點最高；同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","status":"資料缺口","evidence":"第二季資本支出 7.20 億元、自由現金流 8.33 億元，維護與擴產的拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收三年內下滑","status":"不成立","evidence":"美、日、台持續擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置以高配息為主。近四季營運資金與擴產吃掉了幾乎全部自由現金流，配息靠資產負債表支應","reasoning":"現金轉換：自由現金流／淨利 FY2022 為 0.77、FY2023 0.77、FY2024 0.99、FY2025 0.65，近四季只剩約 0.07。近四季自由現金流利潤率 1.21%，也低於同業 6166.TW 的 6.66%、6414.TW 的 4.29%、3088.TWO 的 3.3%。第二季營業現金流 15.53 億元、資本支出 7.20 億元，自由現金流 8.33 億元，只有淨利 45.18 億元的 18%。庫存 209.08 億元、約 116 天，是現金轉換崩落的主因；管理層的說法是為訂單備料，庫存分項事實表未涵蓋。SBC 第二季 0.557 億元，約占營收 0.2%、營業利益 1.1%，稀釋可以忽略。現金去向：配息是最大宗，約為 FY2025 EPS 的 92%，也約為近四季每股自由現金流的十倍（推導見報酬持續期）；資本支出用於美、日、台擴產；營運資金主要是庫存；併購與回購事實表未涵蓋。差額由帳上現金或借款支應，現金與負債結構事實表未涵蓋。營運槓桿為正：營收年增 46%、營業利益年增 64%，利潤率沒有被壓縮。","fact_refs":["f_kpi5","f_kpi6_sbc","f_kpi9","f_kpi4_eps","f_dividend_yield_ttm","f_peer_2395_tw_fcf_margin_pct","f_peer_6166_tw_fcf_margin_pct","f_peer_6414_tw_fcf_margin_pct","f_peer_3088_two_fcf_margin_pct","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":null,"passed":null,"input":"併購金額與已實現報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購金額與均價事實表未涵蓋；股東回饋以現金股利為主"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第二季 SBC 0.557 億元，年化約 2.2 億元，相對市值的稀釋遠低於每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，股東回饋以現金股利為主；回購與併購金額事實表未涵蓋"}}}},"q5_valuation":{"verdict":"要讓現價划算，未來約五年 EPS 每年得成長約 17%–18%，終端還要維持 28–30 倍。週期股要同時做到這兩件事，我不信","reasoning":"反推：以年化約 8% 價格報酬加約 1.5% 股息為門檻，五年後股價需要約 1,068 元。終端 28 倍時，FY2031E EPS 需約 38 元；30 倍時需約 36 元。對照最近四季 EPS 15.71 元，等於每年成長約 17%–18%，比 Base 路徑高出一截。倍數：Trailing P/E 46.28 倍、P/S 7.69 倍、EV/S 7.48 倍，三者都在四個年度端點中最高；這是年度端點的比較，不是連續五年分位。賣方：5 月時 15 位分析師平均目標約 502 元（高 628、低 400），早於第二季財報，不拿來當錨。法說後外資目標 700–750 元、本土最高 800 元，現價 727 元貼近外資區間中點，短線上檔約為零，與觀望的結論一致。同業倍數事實表未涵蓋，終端倍數只能以自身現值與歷史端點為錨：Bull 35 倍、Base 28 倍、Bear 20 倍，Bear 取成長熄火到約 10% 時的倍數。分母檢查：近四季 EPS 沒有明顯一次性項目，第二季淨利年增 127% 是去年同季業外偏低的基期效應。分母正處於週期上行段，這個問題交給情境樹處理。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_week26_return_pct","f_dividend_yield_ttm","f_kpi4_eps"],"verdict_values":{"valuation":{"basis":"Trailing P/E（GAAP 稀釋 EPS），以情境樹終端倍數檢核","peers":{"expanded":false,"reason":"同業倍數事實表未涵蓋，事實表只收同業利潤率；終端倍數以自身現值與年度端點為錨"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"Trailing P/E 46.28 倍、P/S 7.69 倍、EV/S 7.48 倍都在四個年度端點中最高；連續五年分位事實表未涵蓋，所以五年分位欄留空。現價 727 元貼近法說後外資目標 700–750 元的中點。Base 情境五年終值約 882 元，年化價格報酬約 4%，加上股息仍低於 8% 的持有門檻，結論為偏貴。短期上檔以外資目標中點 725 元計約 −0.3%，中期上檔以 Base 五年終值計約 +21.3%","upside_short_pct":-0.3,"upside_mid_pct":21.3,"denominator_disputed":false,"denominator_note":"近四季 EPS 15.71 元沒有明顯一次性項目。第二季淨利年增 127%，高於營業利益的 64%，原因是去年同季淨利只有營業利益的約 64%，基期偏低；本季約 88%，與 FY2022–FY2025 的 86%–99% 一致。分母處於週期上行段的問題交給情境樹，不視為分母爭議"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把零組件短缺下的提前下單當成結構性需求","reasoning":"依據見反證紀錄。衰退信號成立一個半，價值陷阱屬中度風險：生意本身不會因此變壞，但眼前的盈餘與訂單水位可能被短缺放大了。歷史最大回撤、空方最強數字、訴訟與監管金額事實表未涵蓋；重大事件、訴訟、監管各軸都查無結果。","fact_refs":["f_week26_return_pct","f_pe_current","f_peer_2395_tw_fcf_margin_pct","f_kpi3","f_kpi8_book_to_bill"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點的提前下單與現金轉換惡化"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":15.71,"pe":46.28,"basis":"最近四季（截至 2026-06-30）GAAP 稀釋 EPS，由現價 727 元÷Trailing P/E 46.28 倍推得，與終端倍數同為落後四季口徑；路徑 Y1–Y5 對應 FY2027E–FY2031E"},"eps":{"bull":[26.5,31.0,36.0,41.0,46.0],"base":[23.0,24.0,26.5,29.0,31.5],"bear":[18.5,15.5,16.5,18.0,19.5]},"pe":{"bull":35,"base":28,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.535,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-40,"basis":"由三條路徑交叉推得。①倍數回歸：上半年 EPS 9.05 元年化約 18 元，倍數回到 25 倍約 453 元，跌約 38%。②週期消化：上一輪 FY2022→FY2024 EPS 由 12.46 元降到 10.38 元，約 −17%；本輪提前下單規模更大，取 −20%，再疊加倍數落到 22–24 倍，跌約 52%–56%。③26 週已漲 113%，全部回吐約 −53%。因此取 −40% 到 −60%","trigger_time":null},"basis":{"bull":"邊緣 AI 占比升破三成並持續擴大，美日台擴產在 2027–2028 年貢獻營收，毛利率回到 38%–40%；FY2027E 26.5 元到 FY2031E 46 元，每年約成長 15%，終端 35 倍","base":"2027 年靠在手訂單續成長；2028 年提前下單小幅消化，年增約 4%；之後隨邊緣 AI 回到每年約 9%–10% 的成長，FY2031E 31.5 元，終端 28 倍","bear":"提前下單完整消化，劇本與 FY2022→FY2024 相同但幅度更大：FY2028E 回落到 15.5 元，較 FY2027E 再降約 16%，之後緩慢回升到 19.5 元；終端 20 倍，取成長熄火到約 10% 時的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026 年 3 月自承，當季營收被客戶因記憶體短缺而提前下單推升；2022 年短缺期之後，FY2023、FY2024 營收分別年減 6.08%、7.41%，FY2024 EPS 由 12.46 元降到 10.38 元；第三方指出 2024 年工業電腦市場明顯衰退；5 月報導也提到零組件吃緊與材料成本可能限制近期成長","assumption":"目前接單出貨比 1.44、7 月 1.64 的訂單中，有相當比重是為了鎖料，而不是實際部署","consequence":"2027 下半年起進入消化期，FY2028 EPS 回落到 15 元附近，倍數回到 20 倍，股價約 300–400 元，比現價低四成五到六成","ruling":"採納為 Bear 主路徑，機率 30%。不升為 Base，因為 43% 的邊緣 AI 訂單交期超過六個月，客戶也在規劃兩到三年的部署，不全是囤貨。這條與唯一致命數字（接單出貨比跌破 1.0）是同一件事，兩處結論一致","watch":"每季接單出貨比（含北美）、庫存天數、月營收年增率","evidence_refs":["supply_demand_durability#0","supply_demand_durability#4","supply_demand_durability#6"],"fact_refs":["f_kpi8_book_to_bill","f_kpi9"]},{"view":"論點成功但股東經濟變差","evidence":"近四季自由現金流利潤率 1.21%，FY2024 還有 14.84%；第二季毛利率 37.7%，低於財測；記憶體的成本壓力可能擴大到 CPU 與 PCB；2025 年第三季 DDR4 已讓毛利率少約 1 個百分點；北美 60% 訂單的關稅先由研華吸收","assumption":"營收照邊緣 AI 劇本成長，但上游與關稅分走毛利，成長所需的庫存與擴產長期吸走現金","consequence":"EPS 成長，但自由現金流／淨利長期低於 0.75，現行約九成的配息率撐不住，股息成長停滯，每股價值的成長慢於 EPS","ruling":"部分採納。庫存建置有訂單支撐，屬策略備料，暫不視為盈餘品質問題；但設下期限：FY2026 全年自由現金流／淨利低於 30%，且 2027 上半年沒有回到 50% 以上，就認定這條成立，Bear 機率上調至 40%","watch":"自由現金流／淨利、庫存天數、單季毛利率、配息率","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3","reg_tariff_export#0"],"fact_refs":["f_peer_2395_tw_fcf_margin_pct","f_kpi3","f_kpi5"]},{"view":"價格已反映太多","evidence":"26 週股價上漲 113.4%；Trailing P/E 46.28 倍、P/S 7.69 倍都是四個年度端點中最高；現價 727 元貼近法說後外資目標 700–750 元的中點","assumption":"市場已把邊緣 AI 第二曲線與 2027 年續成長算進價格","consequence":"即使 Base 兌現，五年終值約 882 元，年化價格報酬約 4%，加上股息仍低於 8%；只要任何一季接單轉弱，EPS 與倍數會同時受打擊","ruling":"採納，這是本次不追價的主因。卡住結論的是價格，不是生意","watch":"股價相對最近四季 EPS 的倍數是否回到 30 倍以下","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_price_at_dd"]},{"view":"論點失敗","evidence":"中國廠商發布 2026 年新一代低價 ARM 架構工業電腦，以及可跑軟 PLC 的邊緣控制器；研華約 45% 的製造在中國，中國營收上半年年增 51%，是本輪主要成長引擎之一","assumption":"中國市場出現本土低價替代，研華逾 36% 的中國份額開始流失","consequence":"中國區成長由正轉負，整體毛利率再受壓","ruling":"反駁它作為主要失敗路徑：目前只有產品發布，沒有份額或價格數據，而且上半年中國區年增 51%，方向相反；列為長期觀察","watch":"中國區營收年增率與整體年增率的落差","evidence_refs":["substitute_technology#2"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 727.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=727.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單強度：結構性需求還是提前下單","cause":null,"prior_field":null,"side_a":"43% 的邊緣 AI 訂單交期超過六個月，客戶在規劃兩到三年的部署；第二季接單出貨比 1.44、7 月 1.64；法人預期 2027 年續成長，美日台擴產牽動 2027–2028 年營收","side_b":"管理層自承第一季營收被提前下單推升，客戶去年就因擔憂零組件緊俏而下單；5 月報導指出零組件吃緊可能限制近期成長；2022 年短缺之後，FY2023–FY2024 營收連兩年下滑","ruling":"可調和，屬程度差異，兩者並存。Base 保留 FY2028 小幅放緩（EPS 年增約 4%），Bear 承接完整的消化期；2027 上半年之前分不出兩者的比重","evidence_level":"中：證據是公司說法與媒體轉述，訂單分項事實表未涵蓋","settle_metric":"2027 上半年接單出貨比與庫存天數","if_then":["若 2027 上半年接單出貨比維持 1.1 以上，且庫存天數降到 100 天以下，則上修 Base 的 FY2028 EPS，Bear 機率降至 25%","若任一季接單出貨比低於 1.0 且庫存天數高於 130 天，則不建倉；已持有者減碼至半倉"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#3","supply_demand_durability#4","supply_demand_durability#5"]},{"axis":"盈餘品質：EPS 創高，現金轉換卻崩落","cause":null,"prior_field":null,"side_a":"第二季 EPS 5.20 元，營業利益年增 64%，營運槓桿為正","side_b":"第二季自由現金流 8.33 億元，只有淨利的 18%；近四季自由現金流利潤率 1.21%，低於多數同業；庫存約 116 天；近四季每股配息約為每股自由現金流的十倍","ruling":"可調和，屬時間差。採信庫存是有訂單支撐的備料，但這是尚未證實的管理層歸因，所以設下期限，見反證紀錄的股東經濟視角","evidence_level":"中：庫存分項與管理層說法事實表未涵蓋","settle_metric":"FY2026 全年與 2027 上半年的自由現金流／淨利","if_then":["若 2027 上半年自由現金流／淨利回到 50% 以上，則維持原判","若 FY2026 全年低於 30%，且 2027 上半年沒有改善，則 Bear 機率上調至 40%，並停止任何加碼"],"evidence_refs":[]},{"axis":"現在就買的最強論證，對上等待價格","cause":null,"prior_field":null,"side_a":"現在就買的理由：全球份額第一，營益率約為同業兩倍，邊緣 AI 第二曲線有來源，7 月接單創高、交期拉長，美日台擴產支撐 2027–2028 年；若 Bull 的 FY2027 EPS 26.5 元兌現，現價只約是前瞻 EPS 的 27 倍，對龍頭而言合理","side_b":"等待的理由：現價是樣本最高倍數，26 週已漲 113%；Base 五年價格報酬約兩成、年化約 4%，Bear 下跌約 46%；部分訂單是短缺下的提前下單，自由現金流幾乎歸零","ruling":"不可調和，兩邊方向相反，選擇等待。依據：機率加權後，上檔集中在 Bull 一個情境，Base 報酬低於 8% 的持有門檻；硬數據點是 Trailing P/E 46.28 倍與自由現金流利潤率 1.21%。卡住結論的是價格","evidence_level":"高：價格與倍數都是已實現數據","settle_metric":"股價相對最近四季 EPS 的倍數；季度接單出貨比","if_then":["若股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍在 1.0 以上，則重跑研究，通過後建立 2% 首倉","若股價續漲，但第三季毛利率仍低於 38%，則不追","反向條件：若股價下跌，但接單出貨比維持 1.2 以上、毛利率回到 38%，則提前重跑研究，通過後分批建立首倉，不等更低的價格"],"evidence_refs":["capital_markets_pricing#1","end_markets#1"]}],"triggers":[{"n":1,"text":"季度整體接單出貨比跌破 1.0，代表提前下單開始消化","type":"Single Thing","maps_to":"R1","metric":"季度整體接單出貨比","threshold":"任一季 <1.0","action":"不建倉；已持有者減碼至半倉，不攤平","source_freq":"每季法說","date":null,"evidence_refs":["supply_demand_durability#4"]},{"n":2,"text":"股價回到最近四季 EPS 的 30 倍以下，且接單沒有轉弱","type":"估值rearm","maps_to":null,"metric":"股價÷最近四季 EPS；最近一季接單出貨比","threshold":"≤30 倍，且接單出貨比 ≥1.0","action":"重跑研究，通過後建立 2% 首倉","source_freq":"每日股價＋每季法說","date":null},{"n":3,"text":"邊緣 AI 營收占比年底達 30%","type":"假設驗證","maps_to":"H1","metric":"邊緣 AI 營收占比","threshold":"FY2026 年底 ≥30%；低於 27% 視為未達","action":"未達則 Bull 機率降至 15%","source_freq":"每季法說","date":"2027-03"},{"n":4,"text":"毛利率回到財測區間","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"≥38%","action":"連兩季達標，就解除成本轉嫁的疑慮；連兩季低於 37%，改走減碼條件","source_freq":"每季財報","date":"2026-11"},{"n":5,"text":"上游零組件成本吸收失敗","type":"風險","maps_to":"R2","metric":"單季毛利率","threshold":"連兩季 <37%","action":"不建倉；已持有者減碼至半倉","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"n":6,"text":"關稅成本吸收失敗","type":"風險","maps_to":"R3","metric":"單季營業利益率；Section 232 衍生品清單","threshold":"營益率連兩季 <16%，或主力產品列入衍生品課稅","action":"停止加碼並重跑研究","source_freq":"每季財報＋美國商務部公告","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"現金轉換沒有回復","type":"風險","maps_to":"R5","metric":"自由現金流／淨利","threshold":"FY2026 全年 <30%，且 2027 上半年 <50%","action":"Bear 機率上調至 40%，停止任何加碼","source_freq":"半年報、年報","date":"2027-08"},{"n":8,"text":"消化期的盈餘底部跌破論點前提","type":"清倉","maps_to":"H3","metric":"2027 年起的最近四季 GAAP EPS","threshold":"<16 元","action":"已持有者清倉，等下一輪谷底再重跑研究","source_freq":"每季財報","date":null},{"n":9,"text":"第三季財報複審","type":"複審日期","maps_to":null,"metric":"毛利率、接單出貨比、庫存天數、自由現金流","threshold":"見各條門檻","action":"逐條對帳後更新情境機率","source_freq":"每季","date":"2026-11"}],"kill_metrics":[{"metric":"季度整體接單出貨比","bear_threshold":"任一季 <1.0","window":"每季","source":"研華法說會／公司新聞稿","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連兩季 <37%","window":"每季","source":"研華公司新聞稿","last_status":"warning"},{"metric":"自由現金流／淨利","bear_threshold":"FY2026 全年 <30%，且 2027 上半年 <50%","window":"至 2027-08","source":"研華合併財報","last_status":"warning"},{"metric":"庫存天數（庫存÷單季營業成本×90）","bear_threshold":">130 天","window":"每季","source":"研華合併財報","last_status":"ok"},{"metric":"邊緣 AI 營收占比","bear_threshold":"FY2026 年底 <27%","window":"2027-03","source":"研華法說會","last_status":"unknown"},{"metric":"2027 年起的最近四季 GAAP EPS","bear_threshold":"<16 元","window":"2027–2029","source":"研華合併財報","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍 ≥1.0；觸發後先重跑研究，不直接建倉","exec_line":"觀望，卡住結論的是價格。不追價；等倍數靠回檔或 EPS 成長消化到 30 倍以下、接單也沒有轉弱時，才重新評估 2% 首倉","holding_cap":"首倉 2%，上限 4%；要有深回撤的心理準備（情境推估回撤 40%–60%）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍在 1.0 以上"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=113.4, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"邊緣 AI 成為主要成長引擎：營收占比 FY2026 年底達 30%，2027 年不回落","2y":"FY2026 年底占比 ≥30%，FY2027 全年維持 ≥30%","5y":null,"10y":null,"threshold":"年底占比 ≥30%；低於 27% 視為未達","source":"研華每季法說會與公司新聞稿","drift_rule":"占比連兩季低於目標 5% 以上（<28.5%）為削弱，連三季低於目標 10% 以上（<27%）為反轉"},{"id":"H2","text":"上游成本可以轉嫁，毛利率回到公司財測區間","2y":"2027 年單季毛利率回到 38%–40%","5y":null,"10y":null,"threshold":"單季毛利率 ≥38%","source":"研華每季公司新聞稿與財報","drift_rule":"連兩季低於 38% 達 5% 以上（<36.1%）為削弱，連三季低於 10% 以上（<34.2%）為反轉；第二季 37.7% 低於財測，但還沒到削弱線"},{"id":"H3","text":"下一次消化期的盈餘底部明顯高於上一輪谷底，證明邊緣 AI 抬高了週期中樞","2y":null,"5y":"2027–2031 年任一年度 EPS 不低於 16 元（FY2024 谷底為 10.38 元），FY2031E 接近 Base 路徑的 31.5 元","10y":null,"threshold":"2027 年起最近四季 EPS ≥16 元","source":"研華季報與年報（GAAP 稀釋 EPS）","drift_rule":"最近四季 EPS 連四季低於 Base 路徑 5% 以上為削弱，連六季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"提前下單反轉，2027–2028 年進入庫存消化期","h_ref":"H3","clock":"⚡","threshold":"任一季整體接單出貨比 <1.0，或庫存天數 >130 天","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"上游記憶體、CPU、PCB 成本持續侵蝕毛利，轉嫁跟不上","h_ref":"H2","clock":"🔥","threshold":"單季毛利率連兩季 <37%","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"id":"R3","text":"美國關稅成本吸收失敗：北美約占三成營收，60% 北美訂單的關稅先由研華吸收","h_ref":"H2","clock":"🔥","threshold":"單季營益率連兩季 <16%，或主力產品列入 Section 232 衍生品課稅","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"id":"R4","text":"中國本土低價 ARM 工業電腦與軟 PLC 侵蝕研華的中國份額","h_ref":"H3","clock":"🐢","threshold":"中國區營收連兩季年減，而整體營收仍在年增","evidence_refs":["substitute_technology#2"]},{"id":"R5","text":"庫存與擴產長期吸走現金，配息靠資產負債表支應","h_ref":"H3","clock":"🔥","threshold":"FY2026 全年自由現金流／淨利 <30%，且 2027 上半年 <50%","evidence_refs":[]}],"single_thing":{"description":"未來 12–24 個月內，任一季整體接單出貨比跌破 1.0，代表提前下單開始消化","why_fatal":"現價是最近四季 EPS 的 46 倍，隱含多年高成長。接單一轉弱，EPS 路徑與倍數會同時下修：終端 EPS 從 Base 的 31.5 元掉到 Bear 的 19.5 元，倍數從 28 倍掉到 20 倍，這是情境樹裡最大的單一敏感項","if_happens":"不建倉；已持有者減碼至半倉、不攤平。等接單出貨比連兩季回到 1.0 以上、庫存天數降到 100 天以下，再重跑研究","how_monitor":"每季法說公布的整體與分區接單出貨比、月營收年增率、庫存天數","probability":"約 35%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":30.8,"peg_fy2":1.67,"stress":{"pass":null,"total":null},"fy2_valuation_basis":"依 Koyfin 共識（2026-10-09）；10-11 補正，本文撰寫時未載入共識"},"eps_meta":{"base_eps_path":{"FY2025A":12.14,"FY2026E":null,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（TWD）；三年共識 EPS 與分析師家數事實表未涵蓋，FY2026E–FY2028E 留空，不另補"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與法說：毛利率能否回到 38%，接單出貨比能否維持 1.2 以上","impact":"高","watch":"單季毛利率、接單出貨比、庫存天數"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"南加州第二個美國組裝據點預計 2026 年啟用","impact":"中","watch":"北美毛利率與關稅吸收比例"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與法說：邊緣 AI 營收占比是否達 30%，以及全年自由現金流","impact":"高","watch":"邊緣 AI 占比、自由現金流／淨利、配息率"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
