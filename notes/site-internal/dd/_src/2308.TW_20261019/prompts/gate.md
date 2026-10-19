你是 DD 管線 v20 的判斷層閘（gate），標的 2308.TW（20261019）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_ifrs`（q1_business）｜營收（IFRS 合併）＝183.256 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf（numbers.latest_quarter_kpis.items[0]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
  - 註記：市場共識 182.833（Bloomberg，經 KGI 報告），+0.2%
- `f_kpi1`（q1_business）｜毛利率＝35.6 %｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf（numbers.latest_quarter_kpis.items[1]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
  - 註記：共識 36.4%（經 KGI），低 0.8ppt
- `f_kpi2_ifrs_non_gaap`（q1_business）｜營業利益（IFRS，台達電無 non-GAAP 口徑）＝30.57 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf（numbers.latest_quarter_kpis.items[2]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
  - 註記：共識 33.77（經 KGI），低 9.5%
- `f_kpi3_ifrs`（q1_business）｜營業利益率（IFRS）＝16.7 %｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf（numbers.latest_quarter_kpis.items[3]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
  - 註記：共識 18.5%（經 KGI），低 1.8ppt
- `f_kpi4_eps`（q1_business）｜稅後淨利（歸屬母公司）／EPS＝9.68 NT$/股（淨利 25.14 十億）｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf；業外收益 4.43 十億（占營收 2.4%）墊高 EPS（numbers.latest_quarter_kpis.items[4]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
  - 註記：共識 EPS 9.47（經 KGI），+2.2%
- `f_kpi6_2026`（q1_business）｜2026 年資本支出（管理層上調）＝65–70 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30），法說會表述／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KGI 2026-07-30 報告 https://www.kgi.com.hk/zh-hk/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_20260730_en.pdf（轉述管理層：上調逾 100 億，原則上 2027–28 仍可能成長）（numbers.latest_quarter_kpis.items[6]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30），法說會表述）
- `f_kpi7_infrastructure`（q1_business）｜部門營收：Infrastructure（資料中心等）＝62.938 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf（numbers.latest_quarter_kpis.items[7]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-07-29 date｜期間與口徑：2026-07-29／距今 58 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-07-29）
- `f_peer_2308_tw_gross_margin_pct`（q2_moat）｜2308.TW 毛利率＝35.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2308_tw_operating_margin_pct`（q2_moat）｜2308.TW 營業利益率＝16.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2308_tw_fcf_margin_pct`（q2_moat）｜2308.TW FCF 利潤率＝11.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vrt_gross_margin_pct`（q2_moat）｜VRT 毛利率＝38.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝19.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_fcf_margin_pct`（q2_moat）｜VRT FCF 利潤率＝25.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_etn_fcf_margin_pct`（q2_moat）｜ETN FCF 利潤率＝13.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_gross_margin_pct`（q2_moat）｜2301.TW 毛利率＝23.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_operating_margin_pct`（q2_moat）｜2301.TW 營業利益率＝11.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_fcf_margin_pct`（q2_moat）｜2301.TW FCF 利潤率＝-6.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝40.45 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝64.33 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝97.14 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.5 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（40.25 → 40.45）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝776572.09 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1098817.94 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q4_capital）｜自由現金流（營運現金流－資本支出）＝26.9 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營運現金流 43.17、資本支出 16.27，單位十億 NT$）（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-111877.84 TWD m｜期間與口徑：2026-10-19／yfinance 最新一季：總債務 74292.72、現金 186170.56（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.707 %｜期間與口徑：2026-10-19／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-19）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2597.54 m shares｜期間與口徑：2026-10-19／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1640.0 TWD｜期間與口徑：2026-10-19（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝52.28 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.51 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝48.58 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 40.45，分子＝快照價 1965.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-1.12 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 40.91 → 40.45（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.34 x｜期間與口徑：2026-10-19／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-13.23 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-19（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝37.27｜期間與口徑：2026-10-19（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-10-19／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-19）
  - 原文：「price 1635.0 / W52 1557.9 / W104 1021.4 / W250 593.89 / W250 13週斜率 4.51%」

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：凱基證券 2026-04 研報預期台達電液冷市占率因競爭加劇而下降，但仍是散熱方案關鍵供應商；並指台達電有望成為 NVIDIA VR200 首家通過認證的 12kW PSU 供應商
  - 來源：KGI Securities, Delta Electronics (2308 TT) 研究報告 20260420（as_of 2026-04-20）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：中國時報報導投顧報告：水冷標案出現競爭對手，台達電最大水冷專案可能流失小部分市占，但下半年新產品仍有較高機率維持獨家供應
  - 來源：中國時報 wantrich（as_of 2026-04-05）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：經濟日報報導：台達電與光寶科在 AI 伺服器電源領跑，法人估台達電大型 AI 運算中心客戶電源供貨比由去年約5成升至今年約7成；客戶可能找第二、第三供應商，董事長表示未來市占率不會維持這麼高
  - 來源：經濟日報 money.udn.com《台達電、光寶 AI 電源供貨比7成！2026年競爭因2原因加劇》（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：執行長鄭平表示台達在液冷與電源供應器早期市占率很高，部分細分元件高到客戶感到不安，客戶已開始找第二、甚至第三供應商（未點名客戶）
  - 來源：經濟日報（money.udn.com）（as_of 2025-10-31）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2025-02 因美墨關稅，市場擔憂台達電 AI 伺服器電源客戶（廣達、鴻海、緯創等輝達夥伴）出貨受阻，股價盤中跌約 9%；未發現客戶信用惡化的具體證據
  - 來源：自由時報 焦點股》台達電：客戶墨國產線慘了 股價重挫9%（as_of 2025-02-01）｜affects：decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 年 7 月報導提到市場流傳「掉單」與競爭格局生變傳聞，公司尚未證實；來源僅見搜尋摘要
  - 來源：工商時報 wantrich.chinatimes.com（as_of 2026-07-04）｜affects：decision_inputs.bear、triggers
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：2Q26 伺服器電源受缺料影響，功率半導體部分料號交期逾六個月，毛利率低於預期（凱基）；外資另指 IGBT/MOSFET 交期拉長、資料中心專案延期
  - 來源：KGI 研究報告 delta-electronics_20260730（as_of 2026-07-30）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：美國ITC於2026年10月依337條款對特定垂直供電系統啟動調查，申訴方Vicor主張專利侵權；台達電及兩家美國子公司（Delta Electronics (Americas) Ltd.、DET Logistics (USA) Corporation）列為被調查對象。性質為專利／進口爭議，非反壟斷。台達電表示將積極因應、相關產品目前未受影響；經濟部貿易署稱審理通常12至16個月。
  - 來源：中央社 美國啟動337調查鴻海台達電等台廠入列 經濟部：必要時提供協助（as_of 2026-10-11）｜affects：decision_inputs.bear、triggers、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：券商報告稱USITC於2026-10-09依Vicor申訴對台達電等20家公司啟動調查，預估16–18個月，和解或改設計較可能；引述Vicor與台達電先前爭議於2025年5月和解（二手來源，未對照USITC案卷）。
  - 來源：Kaohoon International: Kiatnakin Maintains 'Buy' on Delta Thailand, Expecting Limited Impact From US Probe Into Taiwan Parent（as_of 2026-10-09）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：法人分析文章估計：電動車、工業／醫療用電源與風扇短期可能由客戶負擔關稅，液冷系統部分零組件需台達電自行負擔，液冷毛利率可能下降約5%；此為法人估計非公司公告，發布日未確認（2025年）。
  - 來源：搜尋結果分析文章（台達電 美國 關稅 轉嫁），來源頁面未逐字讀取（as_of 2025-04-30）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：另有文章指出美國占台達電營收比重達30%以上，生產基地無法完全避開美方貿易壓力（搜尋摘要轉述，文章日期未確認）。
  - 來源：搜尋結果（台達電 美國 關稅 轉嫁 客戶 分攤）（as_of 2025-04-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：台達電生產基地分布大陸、台灣、泰國、印度、斯洛伐克；較早報導（約2018年）稱大陸產能約佔七成，後續持續提高中國以外配置；搜尋未找到最新各地區產能百分比
  - 來源：搜尋結果摘要（天下雜誌 cw.com.tw／科技新報等，年份不一）（as_of 2018-09-09）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q3成長降速主因電源IC、PMIC、MOSFET等關鍵零組件供給吃緊，部分AI伺服器訂單出貨遞延，可能於Q4回補
  - 來源：優分析 台達電(2308) Q3成長為何降速?何時回升?（as_of 2026-10-12）｜affects：thesis.R、decision_inputs.bear
- `channel_business_model_shift#3`（channel_business_model_shift｜方向 -｜狀態 ok）：電動車業務處於修正期，公司將視需求在AI與EV業務間調整產能與投資（來源日期不明，可能早於2026）
  - 來源：Taiwan News 報導（as_of 2026-01-01）｜affects：thesis.R、moat_trend
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：2026年9月中旬，民營金控旗下投顧將目標價由2300元下修至2200元，維持買進；主因8月營收低於預期與電源IC等供應瓶頸，2027年EPS預估下修至62.50元、改用35倍本益比。
  - 來源：中國時報 旺得富 2026-09-17 報導（搜尋摘要）（as_of 2026-09-17）｜affects：valuation
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：2026年7月底第2季財報後，國泰、富邦、凱基投顧同步下修目標價（國泰2680→1930、富邦2500→2300、凱基2910→2505），評等仍為買進或增加持股；目標價分布約1930至2505元。
  - 來源：搜尋摘要整理（中文財經媒體，7月底）（as_of 2026-07-31）｜affects：valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：2026年第二季自結營收1,832.56億元、EPS 9.68元創單季新高，毛利率降至35.64%，受零組件成本與產品組合影響。
  - 來源：工商時報 2026-07 報導（搜尋摘要）（as_of 2026-07-30）｜affects：thesis.R、valuation
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：法說會前有外資調降目標價，理由為零組件成本上升持續壓抑毛利率，並提到800V高壓直流供電架構導入速度較預期慢。
  - 來源：UDN 搜尋摘要（as_of 2026-07-28）｜affects：thesis.R、valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：美國 USITC 於 2026-10 對 AI 伺服器供電系統啟動 337 專利侵權調查，台達電及兩家美國子公司列為調查對象；台達表示生產出貨未受影響，審理通常 12–16 個月，尚無侵權認定或排除令
  - 來源：中央社 美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對（as_of 2026-10-11）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：USITC 於 2026-10 啟動 337 調查，台達電及兩家美國子公司列為調查對象（Vicor 專利案延伸），尚無認定
  - 來源：中央社 美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對（as_of 2026-10-11）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":4424,"bear_5y_price":880,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":44.9,"ev5y_pct":48.7,"irr_base_pct":7.7,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":40.45,"pe":40.54,"basis":"2026 年共識 EPS（當年度口徑，上半年已實現 17.59 元）；終端倍數同樣套在 2031 年當年度 EPS"},"eps":{"bull":[66,97,120,140,158],"base":[60,78,90,100,108],"bear":[55,52,45,50,55]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.707,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2308.TW_Q3_2025_Earnings_Call_20251030.md
- 2025-10-30｜Rodney Liu｜margin：財務長報告 Q3 毛利率 34.9%，較 Q2 略降（原話："GP margin for Q3 was 34.9%, slightly"）
- 2025-10-30｜Rodney Liu｜margin：Q3 營收創單季新高（原話："billion, marking a record high quarterly result."）
- 2025-10-30｜Executive｜margin：管理層把 Q2 到 Q3 毛利率下滑歸因於存貨回沖與跌價損失的差異（原話："was still related to the inventory reversal and inventory"）
- 2025-10-30｜Executive｜margin：管理層說明資料中心系統型業務毛利不一定高於零組件業務，是毛利率下滑的主因（原話："is not necessarily higher or is not going to"）
- 2025-10-30｜Executive｜margin：營收加速成長時，費用率有機會因營運槓桿續降（原話："we will continue to enjoy some operating leverage."）
- 2025-10-30｜Executive｜guidance：對第四季與明年第一季展望表示相當樂觀（原話："I think we are quite optimistic."）
- 2025-10-30｜Executive｜guidance：同一段話中附帶提醒環境變化快、需保持謹慎（原話："So we still need to be cautious and be prepared."）
- 2025-10-30｜Rodney Liu｜guidance：管理層認為明年動能應該不差，理由是資料中心業者仍高度投入 AI 資本支出（原話："for the whole next years I think the momentum should be"）
- 2025-10-30｜Executive｜guidance：被問明年 AI 相關營收貢獻時，管理層表示難以預測比重（原話："So it's really difficult to forecast the percentage."）
- 2025-10-30｜Executive｜margin：管理層揭露 Q3 伺服器電源占營收 23%（原話："sorry, 23% of our total"）
- 2025-10-30｜Executive｜margin：管理層揭露 Q3 散熱方案占營收約 11%（原話："the cooling solutions was around 11% of our total revenues."）
- 2025-10-30｜Executive｜capital_allocation：前三季資本支出約 297 億台幣（原話："quarters, it was around TWD 29.7 billion."）
- 2025-10-30｜Executive｜capital_allocation：全年資本支出預估約 400 億台幣（原話："for the whole year, I think it's going to be somewhere"）
- 2025-10-30｜Executive｜capital_allocation：明年資本支出金額與今年相近，內容偏向工廠自動化與設備（原話："for the next year, I think, in terms of the dollar amount"）
- 2025-10-30｜Executive｜capital_allocation：解釋收購日本公司動機：整合半導體電源關鍵技術，取得 RF 電源能力（原話："this Japanese company brings leading RF power expertise"）
- 2025-10-30｜Rodney Liu｜capital_allocation：管理層把併購視為加速成長的主要工具之一（原話："we do view this M&A as one of our main tools"）
- 2025-10-30｜Executive｜product：產能很緊，持續擴產（原話："the capacity is actually pretty tight."）
- 2025-10-30｜Executive｜commitment：泰國三座新廠預計年底前完成建造（原話："we may have 3 new factories in Thailand are likely to be"）
- 2025-10-30｜Executive｜product：800 HVDC 要一段時間才會對營收有意義貢獻（原話："it's still going to take some time before it become more"）
- 2025-10-30｜Po-Wen Yu｜risk：美國產能約兩年後才會有較有意義的規模，且占整體比重不會太大（原話："the U.S. capacity is going to account for a really big"）
- 2025-10-30｜Executive｜risk：被問美國製造成本時，管理層補充勞力是美國製造的關鍵瓶頸（原話："labors are actually one of the key bottlenecks"）
- 2025-10-30｜Executive｜risk：超過 95% 業務為 FOB，關稅由客戶負擔，有時公司先墊再向客戶請款（原話："more than 95% of our businesses on this FOB basis, which"）
- 2025-10-30｜Executive｜customer：大客戶新一代產品今年仍未使用 DC/DC 模組（原話："they are still not using the DC/DC"）
- 2025-10-30｜Executive｜competition：管理層承認客戶會想找第二供應商以增加供應商間競爭（原話："increase the competition among the suppliers."）
- 2025-10-30｜Executive｜competition：管理層認為客戶尋找第二來源必然會發生（原話："something that is definitely going to happen."）
- 2025-10-30｜Executive｜guidance：氫能未來一兩年內不預期對財務有實質貢獻（原話："we do not expand hydrogen to make a meaningful contribution"）
- 2025-10-30｜Executive｜risk：交通與自動化兩個事業今年都很吃力（原話："these 2 businesses have been very challenged"）
- 2025-10-30｜Executive｜risk：中國以外主要車廠電動車銷售明顯下滑（原話："nearly all major OEMs are seeing clear declines in EV sales"）

### 問答異常語氣（迴避／改口／保留）
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師問明年 AI 相關業務的預估營收貢獻｜答法：未給數字，表示變數多、難以預測比重
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師追問 AI 占比提高為何 Q3 毛利率仍低於 Q2，以及費用率走向｜答法：重複前一題的產品組合說法，未提供毛利率或費用率數字，費用率僅以有條件語氣回應
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師問先前說美國製造成本遠高於泰國，現在對美國製造是否改變想法｜答法：未直接回答是否改變想法，改談勞力瓶頸與美國產能擴張時程

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 4 | 6 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 5 | 3 |
| end_markets | found | 7 | 4 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 4 | 3 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260514","verdict":"B 觀望偏進場（thesis 完整 + Q1 26 GM 37% 超預期、估值透過 EPS 修正自然壓縮至 FY+2 PE 33.4x，但短中期 R:R 仍雙負，等 BB 中軌 1,500 或 Q2 法說連 2 季驗證）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心 Capex 結構性持續，±400V 2026 量產、800V 2027 主貢獻，Infrastructure 維持 +40%+ 連 6 季","columns":{"具體數字門檻（sourced floor）":"Infrastructure YoY ≥ +30% 連 6 季（Q4 25 基準 +53%）；800V 出貨量 2027 成為 &gt;50% Infrastructure Rev 來源（管理層法說 2026-04-30）","信息來源":"管理層 2026-04-30 法說確認「800V 2027 年進入主要貢獻期」；GOOGL FY26 Capex 上修至 $185-190B（2026-04 Reuters）","漂移觸發條件（對齊 QC-34）":"連 2 季偏離（Infrastructure YoY &lt;+30%）→ H1 警戒；連 4 季偏離 → H1 反轉（QC-35：2Y 假設連 2 季即可警戒）","2Y 驗證點":"Q2-Q3 2027：Infrastructure YoY +40%+ × 6 季；800V 出貨 ramp 確認","5Y/10Y 驗證點":"5Y（2031）：Infrastructure 占總 Rev 35%+；10Y（2036）：AI DC 電源系統整合市佔 25%+"}},{"id":"H2","text":"合併 GM 升級至 36-37%（Q1 26 已達 37%），液冷 + 800V 高附加價值產品組合持續","columns":{"具體數字門檻（sourced floor）":"合併 GM ≥ 35%（每季，Q1 26 actual 37%）；Infrastructure OI margin ≥ 16.3%（Q4 25 基準）","信息來源":"Q1 2026 法說 GM 37% 實際數字（sinotrade.com 2026-05 引用）；管理層指引「全年 GM ≥ 35%」","漂移觸發條件（對齊 QC-34）":"連 2 季 GM &lt;35% → H2 警戒（QC-35：2Y 連 2 季警戒）；連 4 季 &lt;34% → H2 反轉","2Y 驗證點":"FY26 GM 全年 ≥ 36%（Q1 26 已 37%，需 Q2-Q4 維持）","5Y/10Y 驗證點":"5Y（2031）：GM 穩定 36-38%；10Y（2036）：Delta 從「電源 OEM」升級為「DC 電力系統 IP 商」，GM 趨近 IDC 廠水位 38-42%"}},{"id":"H3","text":"市場給予合理 Forward P/E 32-38x；當前 FY+2 33.40x 已落入合理區間，需 EPS 持續上修才能維持","columns":{"具體數字門檻（sourced floor）":"FY+2 PE ≤ 38x（32-38x 合理帶）；FY26 EPS 共識 ≥ 41.67（當前）；FY27 共識 ≥ 64.52（當前）","信息來源":"yfinance 共識 EPS（17-19 位分析師）；5Y PE 歷史分位 56%（§13.1）","漂移觸發條件（對齊 QC-34）":"FY+2 PE 突破 42x 連 4 週 → 估值體系透支警告；EPS 共識下修連 2 個月 → H3 警戒","2Y 驗證點":"FY26 共識 EPS 再上修至 ≥50（再 +20%）；FY27 上修至 ≥75","5Y/10Y 驗證點":"5Y：估值體系穩定在「系統廠」35-40x；10Y：EPS 複利成長為長期驅動主軸"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI Capex 2027 拐點，Top 4 Hyperscaler 削減資本支出","columns":{"對應":"H1","時間尺度":"🔥 中期（4-6 季可觸發）","監測指標":"Top 4 Hyperscaler Capex 指引（季法說）、Infrastructure YoY","警戒閾值":"連續 2 季 Infrastructure &lt;+30% YoY，或任 1 Hyperscaler 2027 Capex YoY &lt;+10%"}},{"id":"R2","text":"Vertiv 在 800V HVDC 標準戰中拿下 NVIDIA Rubin Ultra 主供地位（Vertiv backlog $9.5B Q1 26，800V H2 2026 release 確認）","columns":{"對應":"H1, H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"2026 Q3 OCP Summit、Vertiv / Schneider 新訂單公告、Yole/TrendForce 季報 Delta 市佔","警戒閾值":"Vertiv 取得 NVIDIA Rubin 主供 reference design 公告 → H1 立即削弱 50%；Delta 市佔 &lt;50% → §5.F 觸發"}},{"id":"R3","text":"地緣政治升級，中國產能（估 ~25% 營收）遷移成本超預期","columns":{"對應":"整體","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"美中關稅政策、Delta 中國產能占比、東南亞 / 墨西哥稼動率","警戒閾值":"遷移期間 GM 回落 &gt;200bp 連 4 季，或東南亞 / 墨西哥稼動率 &lt;70% 連 6 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":2155.0,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2308.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"台達電子"},"oneliner":"台達電是 AI 伺服器電源與液冷龍頭，股價較前份跌 24%，2027 年共識本益比降到 25.5 倍；但缺料壓毛利、大客戶多源化與 337 專利調查同時出現，等第三季法說確認毛利率與第四季出貨回補再進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 資料中心建置的錢：超大型雲端業者經由輝達平台與組裝廠向台達買電源與散熱，錢卡在電源轉換效率與平台認證這一節點，當下瓶頸是上游功率半導體供給","reasoning":"2Q26 營收 1,832.6 億元、毛利率 35.6%、營業利益率 16.7%，但毛利率比共識低 0.8 個百分點、營業利益比共識低 9.5%，稅後 EPS 9.68 元靠業外收益 44.3 億撐住才高於共識。部門結構（2026 年 6 月單月）：電源及零組件約 50%、基礎設施約 37%、自動化約 8%、交通約 5%；伺服器電源占合併營收約 30%（凱基，2Q26），液冷 2025 年約占 9%。超過一成的分部只有電源及零組件與基礎設施兩塊，兩塊都吃 AI 資料中心。客戶集中度公司不揭露，報導點名輝達、Google、Meta 與廣達、鴻海、緯創等組裝廠；單點依賴是輝達平台的電源認證，這既是護城河證據（凱基指台達可望為 VR200 首家通過 12kW 電源認證），也是集中度風險。產業時鐘在擴張期：2026 年資本支出由 466 億元拉到約 700 億元，泰國三座新廠去年底上線後管理層仍說產能吃緊，依據是訂單與擴產，不是股價。供需耐久度判為週期性為主：需求方向是結構性的，但當下限制是功率半導體交期逾六個月，這類供給瓶頸可逆性高，一旦解除，客戶多源化與價格競爭會接手。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_non_gaap","f_kpi3_ifrs","f_kpi4_eps","f_kpi6_2026","f_kpi7_infrastructure","f_earnings_recency"],"verdict_values":{"revenue_quality":"硬體出貨型營收，按客戶平台世代認證取得訂單，沒有長約或訂閱；AI 相關比重高，季度隨客戶建置節奏波動，月營收年增由 6 月 55% 降到 9 月約 15%","unit_econ_note":"單位經濟靠轉換效率與系統整合：電源機櫃把繼電器、斷路器、配電、備援電池甚至液冷整合進同一出貨單位，單機價值上升；但管理層在 2025-10-30 法說承認資料中心系統型業務毛利不一定高於零組件，組合轉向系統時毛利率會被稀釋","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利電源轉換龍頭，獲利被 AI 資本支出週期放大"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性為主：需求來自超大型雲端業者 AI 資本支出（方向結構性），當下瓶頸是電源 IC、PMIC、MOSFET 缺料，供給可逆性高；依據為 2026-07 凱基報告與 2026-10 第三季降速歸因報導","bargaining":{"up":"上游功率半導體部分料號交期逾六個月、零組件漲價壓毛利，上游議價力上升","down":"客戶極度集中且主動找第二、第三供應商，董事長自承份額不會維持這麼高，下游議價力上升","geo":"產能分布中國、台灣、泰國、印度、斯洛伐克，擴產重心轉往泰國；管理層稱超過 95% 業務以 FOB 交貨、關稅多由客戶負擔，但法人估液冷部分零組件關稅需自行吸收"},"profit_pool_dir":"利潤池往系統層移動（電源機櫃、高壓直流、液冷整合），台達往上整合；但到了系統層，對手換成 Vertiv、Eaton 這類國際基礎設施廠","tam_table":{"expanded":false,"reason":"事實表未涵蓋 AI 電源、液冷、高壓直流的市場規模與滲透率數字；高壓直流屬新品類，但證據包只有管理層定性時程，沒有規模可填"}}}},"q2_moat":{"verdict":"護城河 B 級、方向穩定：規模與產品廣度的領先還在擴大，但大客戶主動多源化讓定價力縮減，兩向相抵","reasoning":"機制是電源轉換效率加上平台認證：每一代輝達平台的電源都要重新認證，台達憑產品廣度（交流電源、直流轉換、液冷、電源機櫃）與量產規模拿到首發。事實表未涵蓋同業投入資本，可證方向改用利潤率對照：TTM 毛利率 35.7%，對直接對手光寶 23.4% 領先 12 個百分點，對 Eaton 35.9% 相當，對 Vertiv 38.0% 落後 2.3 個百分點；營業利益率 16.8%，對 Vertiv 19.4%、Eaton 17.7%、光寶 11.4%。自身毛利率 2022 年 28.8%、2025 年 34.3%、TTM 35.7%，持續擴大。執行面判擴大：2025 年營收年增 32%、2026 年前 8 月年增 41%，資本支出擴約五成。定價面判縮減：法人估大客戶電源供貨比由約 5 成升到約 7 成，但執行長說客戶已感不安、開始找第二第三家，董事長說份額不會維持這麼高；液冷最大專案傳出流失小部分份額；第二季毛利率低於共識。領先者在最大客戶的份額已有下滑證據，不能標上升。執行 8 分、定價力 6 分。","fact_refs":["f_peer_2308_tw_gross_margin_pct","f_peer_2308_tw_operating_margin_pct","f_peer_2308_tw_fcf_margin_pct","f_peer_vrt_gross_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_vrt_fcf_margin_pct","f_peer_etn_gross_margin_pct","f_peer_etn_operating_margin_pct","f_peer_etn_fcf_margin_pct","f_peer_2301_tw_gross_margin_pct","f_peer_2301_tw_operating_margin_pct","f_peer_2301_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"電源轉換效率＋平台世代認證＋量產規模；產品廣度讓台達能從單顆電源一路整合到整座電源機櫃","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率 2022 年 28.8% 到 TTM 35.7%，2026 年資本支出約 700 億元擴產；定價面縮減：客戶找第二、第三供應商，董事長表示份額不會維持這麼高，第二季毛利率低於共識 0.8 個百分點。兩向相抵判穩定","competitor_notes":[{"name":"VRT","strategy_note":"毛利率 38.0%、自由現金流利潤率 25.5% 都高於台達，強項是熱管理加電力系統整合；高壓直流電源機櫃世代是它與台達正面交鋒的戰場"},{"name":"ETN","strategy_note":"毛利率 35.9%、營業利益率 17.7% 與台達相當，強在電網端與配電，固態變壓器與機房供電整合是潛在交集"},{"name":"2301.TW","strategy_note":"光寶毛利率 23.4%、自由現金流利潤率 −6.2%，用價格與擴產搶第二供應商位置，是客戶多源化最直接的受益者，但利潤率差距顯示它在成本與產品組合上仍追不上台達"}],"threats":[{"level":"🟡","text":"客戶主動多源化：大型 AI 客戶的電源與液冷開始找第二、第三供應商，台達份額由高點回落，液冷最大專案傳出流失小部分份額，另有公司未證實的掉單傳聞","p":"70%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"level":"🔴","text":"高壓直流世代由國際基礎設施廠（Vertiv、Eaton 等）以機房到機櫃整套供電方案切入，台達從整合者退為零組件供應商；本輪事實表未涵蓋對手新訂單證據，沿用為結構性威脅","p":"35%","evidence_refs":[]},{"level":"🟡","text":"Vicor 專利引發美國 337 調查，涉及垂直供電系統，最壞情況是相關產品被排除進口美國；審理約 12–18 個月，二手來源指雙方前次爭議在 2025 年 5 月和解","p":"20%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（稅後營業利益率約 13%，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 AI 伺服器、決策者是輝達平台與雲端業者、付款者多為組裝廠，三角色都成立；電源是必需品不是想要，但出貨量綁 AI 資本支出節奏，急迫性不等於持久性。代理讀數：2026 年 9 月營收年增降到 14.6%，報導歸因缺料遞延而非砍單，尚待第四季驗證"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代平台的電源認證層看：約每年一次重新認證，等於每年給客戶一次換供應商的窗口；執行長證實客戶已在找第二、第三家。轉換成本存在但不長，靠的是每一代都先過認證"},{"item":"價值鏈分配","level":"🟡","text":"整座 AI 機櫃的經濟利益主要被運算晶片端拿走，電源占採購金額小；台達毛利率五年由 28.8% 升到 35.7%，代表多分到一些，但上游功率半導體交期逾六個月、零組件漲價，下游客戶高度集中又主動多源化，兩頭都在擠"},{"item":"社會容忍度","level":"🟢","text":"產品功能是提升能源轉換效率、降低資料中心耗電，社會敏感度低，不靠監管授權；政策風險在關稅與出口管制（報導稱美國營收占比逾三成），屬地緣風險而非定價上限"}],"roiic":"約 65%（2024→2025 實績，含利潤率擴張）；剔除週期成分保守取 40%","reinvest_rate":"約 80%（2026 年推估）","endo_ceiling":32,"formula_note":"增量報酬：營業利益 2024 年約 478 億（4,211 億×11.35%）到 2025 年約 843 億（5,549 億×15.2%），增 365 億，稅率 22.7% 後增約 283 億；增量資本＝2025 年資本支出約 466 億減折舊約 300 億（以 2025 年 EBITDA 1,179 億減稅前利益 879 億推估）＝166 億，加營運資金增量（事實表未涵蓋，假設為新增營收 1,337 億的 20%＝267 億），合計約 433 億，得約 65%，再扣除利潤率擴張的週期成分保守取 40%。再投資率：2026 年資本支出 650–700 億減折舊約 300 億，加營運資金增量（同一假設，新增營收約 2,217 億×20%＝443 億），合計約 820 億，除以稅後營業利益約 990 億（共識營收 7,766 億×16.5%×77.3%），約 80%。內生上界＝40%×80%＝32%。折舊與營運資金皆為推估，只能當量級參考"}}}},"q3_growth":{"verdict":"成長跑道中等：AI 電源與液冷還在放量，高壓直流電源機櫃 2027 年才進入主要貢獻，固態變壓器與燃料電池只有管理層時程；共識三年 EPS 年化約 61%，遠高於內生上界約 32%","reasoning":"成長以量為主（伺服器電源 1Q26 年增逾 90%、占營收 31%），價靠系統整合提高單機價值，併購與回購貢獻小。共識 EPS：2025 年實際 23.08 元、2026 年 40.45 元、2027 年 64.33 元、2028 年 97.14 元，三年年化約 61%（Koyfin 快照，家數未揭露；營收共識 21 位分析師）。內生上界約 32%，缺口約 29 個百分點：一部分可歸因營業利益率由 15.2% 往 17% 以上擴張，以及 2025 年第四季資產打銷壓低基期；其餘無法歸因，依賴 AI 需求週期延續與估值不下修，因此長期信心上限為中。2026 年共識營收 7,766 億隱含第四季營收約 2,369 億、季增約 20%，需要第三季遞延訂單在第四季回補才做得到。滲透率事實表未涵蓋，跑道年數以管理層時程推：高壓直流 2027 年主貢獻、固態變壓器最慢 2027 年爆發、燃料電池客戶仍是電力公司，第二曲線有時程但沒有營收證據，判中等。衰退信號亮兩個：核心份額近 12 個月縮減，以及共識 EPS 年化（約 61%）高於營收年化（2025→2027 年約 41%）逾 5 個百分點。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_2026","f_kpi7_infrastructure"],"verdict_values":{"growth":{"driver_mix":"量為主（AI 伺服器電源、液冷出貨量），價靠電源機櫃與高壓直流整合提高單機價值；併購與回購貢獻可忽略","runway_years":7,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 32%＝增量報酬保守 40%×2026 年再投資率約 80%，推導見護城河段的報酬持續期說明","segments":[{"item":"電源及零組件","value":"約 50%（2026 年 6 月單月營收比重）；其中伺服器電源占合併營收約 30%（2Q26，凱基），2025 年部門營收年增 25%、利潤年增 37%"},{"item":"基礎設施（資料中心電源系統、液冷）","value":"約 37%（2026 年 6 月）；2Q26 營收 629.4 億元；2025 年營收年增 82%、利潤年增 413%，是利潤成長主引擎"},{"item":"自動化","value":"約 8%；2025 年利潤年減 39%，管理層稱中國市場觸底但未見強勁回升"},{"item":"交通（電動車）","value":"約 5%；2025 年營收年減 16% 且轉虧，公司視需求在 AI 與電動車間調度產能"}],"decay_signals":["核心份額近 12 個月縮減：大客戶多源化、液冷最大專案流失小部分份額","共識 EPS 年化（約 61%）高於營收年化（約 41%）逾 5 個百分點"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健、不靠回購：淨現金約 1,119 億元、配息率約五成，但 2026 年資本支出跳增約五成到 650–700 億元，自由現金流轉換會下降","reasoning":"自由現金流÷淨利：2022 年 0.74、2023 年 1.28、2024 年 1.07、2025 年 0.85（年度財報推算），2Q26 單季自由現金流 269 億對淨利 251 億約 1.07。2025 年每股配息 11.6 元對 EPS 23.14 元，配息率約 50%，TTM 殖利率 0.71%。現金去向：資本支出（2025 年 466 億、2026 年約 700 億）、配息、併購（日本射頻電源公司、晶睿股份轉換每股現金 100 元，金額事實表未涵蓋），沒有回購。流通股約 25.98 億股，2025 年淨利 601 億÷23.08 元約 26.04 億股，未見稀釋；員工股票酬勞事實表未涵蓋。管理層對 2026 年資本支出改口三次：2025-10-30 法說說與 2025 年相近，2026-02-26 法說說略高，7 月再上調到 650–700 億，反映需求超預期，也代表 2026 年自由現金流÷淨利可能跌破 0.75。營運槓桿：2025 年營收年增 32%、營業利益年增 76%，為正向。","fact_refs":["f_kpi5","f_kpi6_2026","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"近年併購（日本射頻電源公司、晶睿股份轉換）的併購後報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"台達電不做庫藏股回購，股東回饋以現金股利為主"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"流通股約 25.98 億股，與 2025 年淨利÷EPS 推得的約 26.04 億股相當，年稀釋率低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購撐起，現金去向以資本支出與配息為主；四分拆解所需的三年現金流量表細項事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價 1,640 元隱含 2031 年 EPS 約 110 元、終端 22 倍才有年化約 8%，與我的基準情境相當；不算貴也不便宜，便宜論證要靠 2027 年共識 EPS 64 元站得住","reasoning":"前瞻本益比：2026 年 40.5 倍、2027 年 25.5 倍、2028 年 16.9 倍；Trailing 52.3 倍、P/S 6.5 倍，都在近四個年度端點的最高位置（這不是五年分位，五年分位事實表未涵蓋）。前瞻 EV/S 5.34 倍。PEG 以共識三年 EPS 年化約 61% 計約 0.66，看似便宜，但 2028 年共識 97 元偏樂觀；改用我的基準（2026→2029 年化約 30%）PEG 約 1.33，屬合理。股價在 10-08 快照時 1,965 元，11 天內跌到 1,640 元（−16.5%），期間有 337 調查立案與第三季營收降速；26 週報酬 −13.2%、RSI 37，不過熱。共識 2026 年 EPS 近三個月下修 1.1%；賣方 7 月底目標價 1,930–2,505 元，9 月一家降到 2,200 元（35 倍 2027 年 EPS 62.5 元），全距約 1.3 倍。12 個月上行以 2028 年基準 EPS 78 元×23 倍＝1,794 元計約 +9%；三年以 2030 年基準 EPS 100 元×22 倍＝2,200 元計約 +34%。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ev_s_fwd","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2027 年共識 EPS 64.33 元）","tier":"AI 資料中心電源與散熱系統供應商","peers":{"expanded":false,"reason":"事實表未涵蓋同業前瞻本益比，同業只有毛利率、營業利益率與自由現金流利潤率可比"},"fwd_pe":40.54,"peg":0.66,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"2027 年本益比 25.5 倍低於一家賣方 9 月採用的 35 倍，但現價已大致反映基準情境（年化約 8%）；Trailing 倍數在近四年最高位置、2028 年共識過度樂觀、337 與份額風險尚未落地，三者抵銷便宜感，結論為合理區","upside_short_pct":9,"upside_mid_pct":34,"denominator_disputed":false,"denominator_note":"分母採 2027 年共識 EPS 64.33 元；賣方 9 月已下修到 62.5 元，差距約 3%，不構成分母爭點。第二季業外收益 44.3 億屬單季墊高，不進年度錨"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：把缺料遞延當成需求轉弱而過度保守，或低估客戶多源化與 AI 資本支出降溫同時發生時的毛利與份額下滑","reasoning":"價值陷阱風險亮兩個信號（份額縮減、EPS 成長遠超營收成長），判中度。看錯方向一（太保守）：若第四季遞延訂單如期回補、2028 年共識 97 元成真，現價只有約 17 倍 2028 年本益比，偏多情境年化逾 20%。看錯方向二（太樂觀）：2028 年雲端業者資本支出消化，同時客戶把電源份額分給第二供應商，EPS 在 2027 年見頂約 55 元、倍數壓到 16 倍，五年跌約 46%；最大回撤範圍 −40% 到 −60%。法說問答迴避紀錄：2025-10-30 法說被問明年 AI 營收占比、毛利率走向、美國製造成本是否改觀，都沒給數字或直接回答；2026-02-26 法說拒絕拆分 AI 與傳統伺服器電源、GPU 與 ASIC 平台，份額變化只能從法人報告間接追蹤。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy3","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長延續但份額與毛利受壓"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":40.45,"pe":40.54,"basis":"2026 年共識 EPS（當年度口徑，上半年已實現 17.59 元）；終端倍數同樣套在 2031 年當年度 EPS"},"eps":{"bull":[66,97,120,140,158],"base":[60,78,90,100,108],"bear":[55,52,45,50,55]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.7,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-40,"basis":"從現價 1,640 元起算：2027 年 EPS 由共識 64 元下修到 52 元（份額與毛利雙壓），2027 年本益比由 25.5 倍壓到 18–20 倍，股價約 940–1,040 元，跌 37–43%；再碰上 AI 資本支出降溫，倍數殺到 15 倍約 780 元，跌 52%；AI 硬體股在需求轉折時回撤常超過一半，下緣取 −60%、上緣 −40%。前份到本次已跌 24%，範圍從現價重新起算","trigger_time":null},"basis":{"bull":"第四季遞延訂單回補、高壓直流 2027 年如期放量且台達保住主供，2028 年 EPS 追上共識 97 元，之後每年 13–17% 成長；終端 28 倍，低於賣方採用的 35 倍","base":"2027 年 EPS 60 元（比共識低 7%，反映份額回落與零組件成本），2028 年後 AI 資本支出成長放緩，EPS 五年年化約 22%；終端 22 倍","bear":"客戶多源化把伺服器電源份額由約 7 成壓到 4 成以下，2028–29 年 AI 資本支出消化，EPS 2027 年 55 元見頂、2029 年回落到 45 元；終端 16 倍取成長熄火到 10% 的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"法人估大客戶電源供貨比已到約 7 成，執行長證實客戶在找第二、第三供應商；9 月營收年增降到 14.6%，市場流傳掉單傳聞","assumption":"第三季降速只是缺料遞延，第四季會回補","consequence":"若其實是份額開始流失，2027 年 EPS 會落在 52–55 元而非 64 元，倍數同時壓到 16–18 倍，五年後虧近五成","ruling":"部分採納：缺料有凱基與優分析兩方佐證，掉單只有傳聞；但份額回落方向已確定，因此 Bear 機率給 30%，基準情境 2027 年 EPS 用 60 元而非共識","watch":"10–11 月營收年增率、第三季毛利率、法人對大客戶供貨比的更新","evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3","end_markets#2"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年資本支出由 466 億元拉到約 700 億元；第二季毛利率 35.6% 比共識低 0.8 個百分點，外資指零組件成本持續壓毛利；法人估液冷部分零組件關稅需自行吸收","assumption":"營收成長會轉成同比例的自由現金流","consequence":"營收照成長，但毛利率卡在 34–35%、自由現金流÷淨利跌破 0.75，股東拿到的現金報酬遜於 EPS 成長","ruling":"採納：列為第二條假設的檢驗，毛利率連 2 季低於 35% 就減碼","watch":"每季毛利率、年度自由現金流÷淨利","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4","supply_demand_durability#4","reg_tariff_export#1"],"fact_refs":["f_kpi1","f_kpi5","f_kpi6_2026"]},{"view":"價格已反映太多","evidence":"Trailing 本益比 52.3 倍、P/S 6.5 倍都在近四個年度端點最高位置；2028 年共識 EPS 97 元隱含三年年化約 61%；賣方 7 月與 9 月連續下修目標價","assumption":"2027 年本益比 25.5 倍已經便宜","consequence":"若 2028 年共識下修到我的基準 78 元，現價對應 2028 年本益比 21 倍，並不便宜","ruling":"部分反駁：股價已較前份跌 24%，2027 年倍數從 33.4 倍降到 25.5 倍，再跌的空間主要來自 EPS 下修而非倍數；但現價大致只反映基準情境，不構成安全邊際","watch":"共識 2027、2028 年 EPS 修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_pe_percentile","f_consensus_eps_fy3"]},{"view":"論點失敗","evidence":"美國 ITC 337 調查涉及垂直供電系統，台達與兩家美國子公司列名；另有報導稱美國營收占比逾三成，產能過去約七成在中國；2025 年 2 月美墨關稅曾讓股價盤中跌約 9%","assumption":"337 會像前次一樣和解或改設計，關稅可轉嫁客戶","consequence":"若裁定侵權並發排除令，相關直流轉換產品無法進口美國，伺服器電源份額直接受損","ruling":"暫不採納為主情境：審理約 12–18 個月，二手來源指前次已和解，公司稱產品目前未受影響；列入風險與觸發器追蹤","watch":"USITC 初步裁定、和解公告、公司歸因關稅的毛利率變化","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0","reg_tariff_export#2","geo_supply_chain#1","customer_concentration_credit#2"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 2155.0 → 本次 1640.0（-23.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=2155.0","side_b":"本次 price_at_dd=1640.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 2,155 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 2,155 元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 2,155 元：Bull 價 4,424、Bear 價 880，五年期望值 +13.2%，基準年化 2.0%，不對稱比 1.48","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.48。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 2,155 元：五年期望值 +13.2%，基準年化 2.0%，不對稱比 1.48","side_b":"本次情境、股價 1,640 元：五年期望值 +48.7%，基準年化 7.7%，不對稱比 3.05","ruling":"再換股價、情境不動：起點價下跌 23.9%，五年期望值多 35.5 個百分點，基準年化多 5.7 個百分點，不對稱比由 1.48 升到 3.05。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-05-14 股價 2,155 元、2027 年本益比 33.4 倍，估值判為中性；情境機率與最大回撤未填","side_b":"本次 1,640 元、2027 年本益比 25.5 倍，估值仍判中性；Bull 25%、Base 45%、Bear 30%，最大回撤 −40% 到 −60%","ruling":"股價跌 24% 讓倍數變便宜，但同期新增 337 調查、份額回落與毛利未達共識，下檔情境加寬，抵銷後估值結論不變","evidence_level":"事實表價格與共識","settle_metric":"2027 年共識 EPS 與本益比","if_then":["若 2027 年共識 EPS 守住 62 元以上且股價跌到 1,350 元以下（約 21 倍），則估值轉入便宜區、分批反買","若 2027 年共識 EPS 跌破 55 元，則即使股價不動，倍數也回到約 30 倍，估值轉貴、不建倉"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"品質評級、陷阱與護城河方向","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份品質評級 B、陷阱風險中度、護城河方向未填","side_b":"本次品質評級 B、陷阱風險中度、護城河方向穩定","ruling":"評級與陷阱結論不變但理由更新：前份靠第一季毛利率 37% 超預期，本次第二季毛利率回到 35.6%，客戶多源化與液冷份額流失有多方報導；執行力擴大與定價力縮減相抵，方向判穩定而非上升","evidence_level":"公司法說＋法人報告＋媒體報導","settle_metric":"每季毛利率、大客戶電源供貨比","if_then":["若連 2 季毛利率 <35% 且法人估大客戶供貨比降到 5 成以下，則護城河方向改判下降、減碼至半倉","若第三、第四季毛利率回到 36% 以上，則維持穩定判斷"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","capital_markets_pricing#3"]},{"axis":"新增判斷欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份這些欄位為空白","side_b":"本次：成長跑道中等、類型為品質複利成長（次類循環）、循環位置中循環；裁決與角色由決策矩陣推出","ruling":"屬判斷框架新增欄位，不是基本面改變","evidence_level":"方法","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件欄（裁決文字寫等布林通道中軌 1,500 元或第二季法說連 2 季驗證）","side_b":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","ruling":"改用事件錨、不設價格：前份的技術錨 1,500 元未觸及，真正卡住的是毛利與出貨回補兩件事，該等的是證據不是價位","evidence_level":"方法＋公司法說","settle_metric":"第三季毛利率、10 月營收年增率","if_then":["若兩條件同時成立，則重跑判斷並建首倉 2%","若股價先漲但證據未到，則不追"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"輝達 800V 高壓直流世代的電源主供落到他家，台達降為第二供應商","ruling":"前份沒有這一欄；本次依敏感度選定：2027 年共識 EPS 年增約 59% 的最大來源是伺服器電源與高壓直流，主供地位是數學上最大的單一變數，影響範圍比 337 排除令大；發生即清倉","evidence_level":"法人報告＋管理層時程","settle_metric":"輝達平台電源認證與主供公告","if_then":["若確認台達失去主供，則清倉並重跑判斷","若台達取得 VR200 首家 12kW 認證並量產，則此風險降級"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"清倉與減碼門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（空白）","side_b":"毛利率連 2 季 <35% 減碼至半倉、連 2 季 <34% 列失效；月營收年增連 3 個月 <10%；大客戶電源供貨比 <5 成減碼；337 初步裁定侵權減碼一半；2027 年共識 EPS <55 元減碼至 1/3 以下；主供易手清倉","ruling":"新增門檻是回應本輪新證據：第二季毛利率未達共識、9 月營收年增降到 14.6%、337 立案","evidence_level":"公司法說＋月營收＋ITC 立案報導","settle_metric":"同上門檻","if_then":["若任一門檻觸發，則依該門檻的減碼或清倉動作執行並重跑判斷"],"evidence_refs":["end_markets#2","regulatory_antitrust#0"]},{"axis":"假設與風險門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：基礎設施年增 ≥30% 連 6 季、合併毛利率 ≥35%、2027 年本益比 ≤38 倍；Vertiv 取得輝達 Rubin 主供則論點削弱","side_b":"本次：月營收年增自 11 月回到 ≥25%、第四季季增 ≥10%，基礎設施年增 ≥30% 保留為輔助門檻；毛利率 ≥35%、2027 年營業利益率 ≥17%；高壓直流世代主要平台供貨比 ≥5 成；新增 337 與缺料兩條風險","ruling":"毛利率 35% 門檻保留；基礎設施年增門檻保留但本期部門年增數字事實表未涵蓋，標資料缺口，主檢驗改用合併月營收；本益比 38 倍門檻退休，因股價已跌到 25.5 倍、不再是約束；Vertiv 風險移到護城河威脅，本輪無新證據","evidence_level":"公司法說＋月營收＋法人報告","settle_metric":"月營收、每季毛利率","if_then":["若門檻連 2 季未達，則依觸發器減碼"],"evidence_refs":["end_markets#2","supply_demand_durability#4"]},{"axis":"管理層說法與實績","cause":"新證據","prior_field":null,"side_a":"2026 年 7 月法說董事長：產能與物料掌握尚稱穩定，下半年營運優於上半年","side_b":"第三季營收季增 7.5%，但 9 月年增降到 14.6%，降速歸因電源 IC、PMIC、MOSFET 缺料；第二季毛利率與營業利益率低於共識；賣方 7 月與 9 月兩度下修目標價","ruling":"可調和（程度差異）：下半年營收仍高於上半年，管理層說法字面成立，但缺料影響比描述大；採信缺料遞延，但用第四季回補驗證，不靠管理層措辭","evidence_level":"月營收＋法人報告","settle_metric":"第四季營收季增率、10–11 月營收年增率","if_then":["若第四季營收季增 ≥10%，則採信遞延說法","若第四季營收季增 <5%，則判定不只缺料，2027 年 EPS 錨下修至 55 元並減碼"],"evidence_refs":["end_markets#2","supply_demand_durability#4","capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較前份跌 24%、11 天內跌 16.5%，但 2027 年共識 EPS 幾乎沒動（64.52 到 64.33）；2027 年本益比 25.5 倍低於賣方 35 倍；淨現金約 1,119 億；Vicor 前次爭議已和解","side_b":"第三季法說預計 10 月底（日期事實表未涵蓋，依前兩季 4 月底、7 月底推估），毛利率與第四季展望是當前唯一約束；等這段時間的成本，小於在份額與缺料未明時買進的風險","ruling":"選 B 側：不是不看好，而是決勝數據即將出現；觀望的約束只有一個，就是第三季毛利率與出貨回補","evidence_level":"事實表價格與共識","settle_metric":"第三季毛利率、10 月營收年增率","if_then":["若第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，則重跑判斷後建首倉 2%","若股價先反彈到 1,965 元以上而證據未到，則不追","若跌到 1,350 元以下而基本面門檻未破，則分批反買"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：AI 資料中心需求讓產能吃緊，2026 年資本支出由 466 億拉到約 700 億，6 月營收年增 55% 創高","side_b":"競爭惡化：客戶多源化、液冷份額流失；其他結構變數：337 專利調查、關稅與產地分散、電動車業務處於修正期","ruling":"雙向拉鋸：結構順風仍在，但競爭與法規兩軸同時轉負，份額高點已過","evidence_level":"公司法說＋媒體＋ITC 立案報導","settle_metric":"大客戶供貨比、337 初步裁定","if_then":["若供貨比守在 5 成以上且 337 和解，則改判結構性轉好中","若供貨比跌破 5 成，則改判競爭惡化中並減碼"],"evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#0","channel_business_model_shift#3"]}],"triggers":[{"n":1,"text":"第三季法說毛利率確認","type":"假設驗證","maps_to":"H2","metric":"2026 年第三季合併毛利率","threshold":"≥35%","action":"達標且 10 月營收年增 ≥20% 則重跑判斷建首倉；未達則續觀望","source_freq":"季度法說","date":"2026-10","evidence_refs":["capital_markets_pricing#3"]},{"n":2,"text":"第四季遞延訂單回補","type":"假設驗證","maps_to":"H1","metric":"10–12 月合併營收年增率與第四季季增率","threshold":"月營收年增自 11 月起 ≥25%；第四季季增 ≥10%","action":"未達則 2027 年 EPS 錨下修至 55 元重算","source_freq":"每月 10 日前後月營收","date":"2026-11","evidence_refs":["end_markets#2"]},{"n":3,"text":"缺料與零組件成本壓毛利","type":"減碼","maps_to":"R1","metric":"合併毛利率","threshold":"連 2 季 <35%","action":"減碼至半倉並停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["supply_demand_durability#4","capital_markets_pricing#4"]},{"n":4,"text":"客戶多源化侵蝕份額","type":"風險","maps_to":"R2","metric":"法人估大型 AI 客戶電源供貨比","threshold":"<50%","action":"減碼至半倉，護城河方向改判下降並重跑判斷","source_freq":"法人報告與媒體（不定期）","date":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"n":5,"text":"337 專利調查裁定","type":"風險","maps_to":"R3","metric":"USITC 初步裁定","threshold":"裁定侵權並建議排除令","action":"減碼一半；和解或改設計則解除","source_freq":"USITC 案卷（不定期）","date":"2027-10","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"輝達高壓直流世代主供易手","type":"Single Thing","maps_to":"Single Thing","metric":"輝達 800V 平台電源主供名單","threshold":"台達不是主供","action":"清倉並重跑判斷","source_freq":"法人報告、平台發表（不定期）","date":"2027","evidence_refs":["competitive_share_entrants#0"]},{"n":7,"text":"證據到位後進場","type":"估值rearm","maps_to":"H1,H2","metric":"第三季毛利率與 10 月營收年增率","threshold":"毛利率 ≥35% 且 10 月營收年增 ≥20%","action":"重跑判斷後建首倉 2%；股價先漲證據未到則不追","source_freq":"季度法說＋月營收","date":"2026-11","evidence_refs":[]},{"n":8,"text":"基本面未破的深跌","type":"加碼","maps_to":"H3","metric":"股價與 2027 年共識 EPS","threshold":"股價 ≤1,350 元且 2027 年共識 EPS ≥62 元","action":"分批反買，每次 1%，上限 4%","source_freq":"每日股價＋每月共識快照","date":null,"evidence_refs":[]},{"n":9,"text":"AI 資本支出降溫與共識下修","type":"減碼","maps_to":"R5","metric":"2027 年共識 EPS","threshold":"<55 元","action":"減碼至 1/3 以下並重跑判斷","source_freq":"每月共識快照","date":null,"evidence_refs":["channel_business_model_shift#3"]},{"n":10,"text":"年度複審","type":"複審日期","maps_to":null,"metric":"2026 年全年財報與 2027 年資本支出指引","threshold":"到期即複審","action":"重跑完整判斷","source_freq":"年度法說","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"合併毛利率（季）","bear_threshold":"連 2 季 <34%","window":"2026Q3–2027Q2","source":"公司季度法說簡報","last_status":"ok"},{"metric":"合併月營收年增率","bear_threshold":"連 3 個月 <10%","window":"2026-10～2027-06","source":"公司月營收公告","last_status":"warning"},{"metric":"大型 AI 客戶電源供貨比（法人估）","bear_threshold":"<50%","window":"2027 年底前","source":"法人報告／經濟日報","last_status":"unknown"},{"metric":"USITC 337 調查初步裁定","bear_threshold":"裁定侵權並建議排除令","window":"2027-10～2028-04","source":"USITC 案卷","last_status":"warning"},{"metric":"2027 年共識 EPS","bear_threshold":"<55 元","window":"2027-06 前","source":"Koyfin 共識快照","last_status":"ok"}],"action_conditions":{"rearm_trigger":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","exec_line":"兩條件成立：重跑判斷、首倉 2%；第三季毛利率 <35% 或第四季季增 <5%：2027 年 EPS 錨下修至 55 元重算、不建倉；股價先漲證據未到：不追；跌到 1,350 元以下且 2027 年共識 EPS 守住 62 元：分批反買","holding_cap":"首倉 2%，證據確認後上限 4%（最大回撤可能超過五成，需有深回撤心理準備）"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺料造成的出貨遞延與 337 立案，當成需求轉弱與出口禁令來定價，11 天跌 16.5%；但 2027 年共識 EPS 幾乎未動，337 也還沒有任何裁定","momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等第三季法說毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺料造成的出貨遞延與 337 立案，當成需求轉弱與出口禁令來定價，11 天跌 16.5%；但 2027 年共識 EPS 幾乎未動，337 也還沒有任何裁定"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-13.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等第三季法說毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 資料中心需求帶動 2027 年營收再成長三成以上，第三季降速是缺料遞延，不是需求轉弱","2y":"2027 年合併營收 ≥1 兆元（共識約 1.10 兆），第四季單季營收季增 ≥10% 驗證遞延回補","5y":null,"10y":null,"threshold":"月營收年增率自 2026 年 11 月起回到 ≥25%；2027 年全年營收年增 ≥30%；輔助門檻：基礎設施部門季營收年增 ≥30%（前份門檻保留，本期數字事實表未涵蓋，標資料缺口）","source":"公司月營收公告、季度法說簡報；2026-10 優分析把第三季降速歸因於電源 IC、PMIC、MOSFET 缺料","drift_rule":"2 年期規則：實績偏離門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"零組件漲價與缺料只是過渡，合併毛利率守住 35% 以上，營業利益率回到 17% 以上","2y":"2027 年四季毛利率皆 ≥35%，全年營業利益率 ≥17%","5y":null,"10y":null,"threshold":"每季合併毛利率 ≥35%；2027 年營業利益率 ≥17%","source":"季度法說簡報；2Q26 毛利率 35.6%、營業利益率 16.7%（共識 36.4%、18.5%）","drift_rule":"連 2 季毛利率 <35% 視為削弱；連 3 季 <34% 視為反轉"},{"id":"H3","text":"台達在 800V 高壓直流電源機櫃世代維持主要供應商地位，客戶多源化之後伺服器電源份額仍在 5 成以上","2y":null,"5y":"2031 年基礎設施部門營收占合併 ≥40%，電源機櫃與高壓直流成為最大單一產品線","10y":null,"threshold":"2027 年起高壓直流與電源機櫃開始大量貢獻（管理層時程）；主要 AI 平台電源供貨比 ≥50%（目前法人估約 7 成）","source":"2025 年第四季、2026 年第一季法說管理層時程；凱基 2026-04 指台達可望為 VR200 首家通過認證的 12kW 電源供應商；經濟日報供貨比報導","drift_rule":"5 年期規則：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"功率半導體缺料與零組件漲價持續，出貨遞延並壓毛利","h_ref":"H1,H2","clock":"⚡","threshold":"毛利率連 2 季 <35%，或 10–11 月營收年增 <15%","evidence_refs":["supply_demand_durability#4","end_markets#2","capital_markets_pricing#3","capital_markets_pricing#4","capital_markets_pricing#0","capital_markets_pricing#1"]},{"id":"R2","text":"大客戶主動多源化，電源與液冷份額由高點回落並帶動降價","h_ref":"H3","clock":"🔥","threshold":"法人估大型 AI 客戶電源供貨比 <50%，或連 4 季毛利率低於 35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"id":"R3","text":"Vicor 專利引發的美國 337 調查，最壞情況是垂直供電相關產品被排除進口美國","h_ref":"H3","clock":"🔥","threshold":"USITC 初步裁定侵權並建議排除令（預計 2027 年第四季前後）","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"id":"R4","text":"關稅與地緣：報導稱美國營收占比逾三成，液冷部分零組件關稅可能自行吸收，產能過去集中中國","h_ref":"H2","clock":"🐢","threshold":"公司歸因關稅的毛利率下滑 >200 個基點，連 4 季","evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1","customer_concentration_credit#2"]},{"id":"R5","text":"AI 資本支出 2028 年進入消化期，同時非 AI 業務（電動車、自動化）仍弱，接不了棒","h_ref":"H1","clock":"🐢","threshold":"2027 年共識 EPS 跌破 55 元，或主要雲端業者 2028 年資本支出指引年減","evidence_refs":["channel_business_model_shift#3"]}],"single_thing":{"description":"輝達 800V 高壓直流世代（2027 年量產）的電源主供落到他家，台達降為第二供應商","why_fatal":"2027 年共識 EPS 年增約 59% 的最大來源是伺服器電源與高壓直流電源機櫃；主供易手後份額可能由約 7 成降到 3–4 成，推估 2027 年 EPS 下修 20–25%，倍數同時從成長股降到電源代工水位","if_happens":"清倉並重跑判斷；Bear 情境機率上調至 50% 以上","how_monitor":"輝達平台電源認證公告、法人供貨比估計、2026 下半年高壓直流小量出貨進度、2027 年月營收","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.5,"peg_fy2":0.42,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":23.08,"FY2026E":40.45,"FY2027E":64.33,"FY2028E":97.14},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（台達電無 non-GAAP 口徑）；共識為 Koyfin 美元值依 2026-10-08 匯率換算新台幣"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"2026 年第三季法說：毛利率與第四季展望","impact":"高","watch":"毛利率是否 ≥35%、管理層對缺料回補的說法"},{"date":"2026-11","date_precision":"month","type":"other","event":"10 月合併營收公布","impact":"中","watch":"年增是否回到 ≥20%"},{"date":"2026Q4","date_precision":"quarter","type":"product","event":"800V 高壓直流電源機櫃小量出貨","impact":"中","watch":"是否如期出貨、客戶是誰"},{"date":"2027-02","date_precision":"month","type":"macro","event":"主要雲端業者公布 2027 年資本支出","impact":"高","watch":"年增幅度是否仍為正"},{"date":"2027Q4","date_precision":"quarter","type":"regulatory","event":"USITC 337 調查初步裁定","impact":"高","watch":"侵權認定、排除令或和解"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
