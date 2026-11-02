你是 DD 管線 v20 的判斷層閘（gate），標的 2308.TW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
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
- `f_peer_2308_tw_gross_margin_pct`（q2_moat）｜2308.TW 毛利率＝35.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2308_tw_operating_margin_pct`（q2_moat）｜2308.TW 營業利益率＝16.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2308_tw_fcf_margin_pct`（q2_moat）｜2308.TW FCF 利潤率＝11.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝20.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_fcf_margin_pct`（q2_moat）｜VRT FCF 利潤率＝23.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_gross_margin_pct`（q2_moat）｜2301.TW 毛利率＝23.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_operating_margin_pct`（q2_moat）｜2301.TW 營業利益率＝11.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2301_tw_fcf_margin_pct`（q2_moat）｜2301.TW FCF 利潤率＝-6.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2301.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝37.78 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝60.9 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝94.77 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝757808.77 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1065093.91 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q4_capital）｜自由現金流（營運現金流－資本支出）＝26.9 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營運現金流 43.17、資本支出 16.27，單位十億 NT$）（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-98132.15 TWD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 115079.74、現金 213211.89（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2597.54 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.869 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1335.0 TWD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝35.34 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 37.78，分子＝快照價 1335.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝42.56 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝98.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝98.5 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.94 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.45 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-4.59 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（63.83 → 60.9）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-38.01 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝25.61｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-6.58 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 40.44 → 37.78（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-6.44 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（40.38 → 37.78）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）

### findings_digest 中方向為負或來源衝突的條目（22 條）
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
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-10-09 美國ITC 對 Vicor 申訴之垂直供電系統專利案立案 337-TA-1526，台達電與鴻海、廣達等同列被調查方；申訴方要求有限排除令及停止侵權命令；台達電稱將依程序積極因應、相關產品目前未受影響；立案不等於認定侵權。
  - 來源：中央社｜美國啟動337調查鴻海台達電廣達入列（as_of 2026-10-11）｜affects：thesis.R、decision_inputs.bear、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：公開資訊觀測站 2026-10-12 有重大訊息「美國國際貿易委員會337調查說明」。
  - 來源：公開資訊觀測站｜歷史重大訊息清單（未命中關鍵字者）（as_of 2026-10-12）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-10-09 美國ITC 對 Vicor 申訴之垂直供電系統專利案立案 337-TA-1526，台達電列被調查方；台達電稱將積極因應、產品目前未受影響。未見投保中心團體訴訟。
  - 來源：中央社｜美國啟動337調查鴻海台達電廣達入列（as_of 2026-10-11）｜affects：thesis.R、decision_inputs.bear、triggers
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：公開資訊觀測站 2026-10-12 重大訊息「美國國際貿易委員會337調查說明」。
  - 來源：公開資訊觀測站｜歷史重大訊息清單（as_of 2026-10-12）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3810,"bear_5y_price":768,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":40.2,"ev5y_pct":51.7,"irr_base_pct":7.0,"asym_ratio":3.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":37.78,"pe":35.34,"basis":"FY1（2026E）共識 EPS 37.78 元，年度已過十個月，視同當年口徑；終端倍數同樣乘以終端年度 EPS"},"eps":{"bull":[61,90,105,117,127],"base":[51,60,67,73,78],"bear":[40,36,40,44,48]},"pe":{"bull":30,"base":24,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.869,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
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
| major_events | found | 5 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261019","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","irr_base_pct":7.7,"ev5y_pct":48.7,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.1,"ev5y_pct":48.7,"irr_base_pct":7.7,"max_dd_pct":-60,"bull_5y_price":4424,"bear_5y_price":880,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","price_at_dd":1640.0,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2308.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"台達電子"},"oneliner":"AI 資料中心電源龍頭，營收仍創新高，但零組件成本壓縮毛利率，客戶也開始分散供應，共識 2027–28 年 EPS 偏高；股價半年跌 38% 後接近合理，等 10 月營收與第三季毛利率證實再動","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺的是美系雲端業者擴建 AI 資料中心的電源與散熱錢，利潤卡在電源轉換效率與機櫃級整合這一節點；產業仍在擴張期，但上游缺料、下游分散供應，兩頭都在擠壓","reasoning":"最新一季（2Q26）營收 1,832.6 億元，毛利率 35.6%（共識 36.4%），營益率 16.7%（共識 18.5%）。營業利益 305.7 億元，比共識少 9.5%；EPS 9.68 元高於共識，靠的是業外收益 44.3 億元。分部比重（2026 年 6 月營收）：電源及零組件約 50%、基礎設施約 37%、自動化約 8%、交通約 5%；第二季基礎設施營收 629.4 億元，占 34.3%。伺服器電源約占第二季營收 30%，液冷約占 2025 年營收 9%。2025 年基礎設施營收增 82%、利益增 413%，交通轉為虧損。產業時鐘判在擴張期，依據是第三季營收約 1,971 億元、年增 31.1%，產能仍緊，2026 年資本支出也上調到 650–700 億元。供需屬週期性，現階段偏緊，但供給可逆性高：客戶已在導入第二、第三供應商，同業也能擴產。議價權方面，上游功率半導體交期逾六個月、成本上升；下游雲端業者與代工廠集中。管理層不揭露客戶別營收，前一、兩大客戶占比屬資料缺口，集中度風險先標記。產業態勢是雙向拉鋸：一邊是競爭惡化（客戶分散供應、液冷份額回落），一邊是結構轉好（高壓直流、電源機櫃整合、資本支出上調）；另有 337 專利調查與美國關稅兩項結構變數。管理層在 2025-10-30 法說承諾泰國三座新廠年底前完工，2026-02-26 法說確認已上線，執行有紀錄","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_non_gaap","f_kpi3_ifrs","f_kpi4_eps","f_kpi6_2026","f_kpi7_infrastructure"],"verdict_values":{"revenue_quality":"交易型硬體銷售，沒有訂閱收入；需求綁雲端業者資本支出，能見度約一到兩季。管理層不給 AI 營收占比，也不拆 GPU／ASIC 與客戶別","unit_econ_note":"近四季毛利率 35.69%、營益率 16.78%、FCF 利潤率 11.7%。年度毛利率由 2022 年 28.81% 一路升到 2025 年 34.27%，主因是資料中心產品組合與規模經濟：4Q25 費用率 18.3%，一年前為 21.4%","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"電源轉換與散熱系統供應商，成長綁雲端資本支出循環，毛利率四年升 5.5 個百分點"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性，現階段供給偏緊：2025-10-30 與 2026-02-26 兩場法說都說產能吃緊，功率半導體部分料號交期逾六個月；需求來自美系雲端業者資本支出，2026-02-26 法說稱今年金額不低於前一年。供給可逆性高，客戶可導入第二來源，同業也能擴產","bargaining":{"up":"上游功率半導體（IGBT、MOSFET、電源 IC）缺料又漲價，議價權偏向供應商","down":"下游雲端業者與代工廠（廣達、鴻海、緯創）集中，且主動導入第二、第三供應商，議價權偏向客戶；客戶別占比未揭露","geo":"美國占營收 30% 以上；產能分布在大陸、台灣、泰國、印度、斯洛伐克，擴產重心移往泰國；超過 95% 為 FOB 交易，關稅原則上由客戶負擔"},"profit_pool_dir":"利潤池正往機櫃級整合與高壓直流移動，台達電站在這個方向上；但 2025-10-30 法說提到系統型業務毛利不一定高於零組件，份額擴張不必然帶來利潤率擴張","tam_table":{"expanded":false,"reason":"事實表未涵蓋 AI 資料中心電源與液冷的 TAM、滲透率與利潤池數據，暫以月營收與分部營收代理；此項承重但沒有資料，列為資料缺口"}}}},"q2_moat":{"verdict":"護城河方向穩定（→），評等 B：執行力仍領先，但零組件成本與客戶分散供應正在侵蝕定價力","reasoning":"護城河機制有兩層：一是電源轉換效率，以及跟著 GPU 平台換代的共同設計能力；二是把繼電器、斷路器、BBU、液冷整合成電源機櫃的系統能力。對同業（近四季）：營益率 16.78%，比 VRT 的 20.35% 低 3.6 個百分點，略低於 ETN 的 17.71%，比光寶的 11.41% 高 5.4 個百分點；FCF 利潤率 11.7%，遠低於 VRT 的 23.74%。事實表沒有同業 ROIC 與投入資本，報酬差距只能用利潤率代替；同業也只有單期資料，看不出差距在擴大還是收窄。執行力給 8 分：凱基認為台達電有望成為 NVIDIA VR200 首家通過認證的 12kW 電源供應商，±400V 與 800V 兩種高壓直流架構也都能供貨。定價力給 6 分：第二季毛利率低於共識，零組件成本吃掉部分組合改善；董事長也預告份額不會一直維持在約七成的高檔。當期報酬落在高利益率、高周轉象限：2023–25 年淨利減自由現金流合計約 −32 億元，稅後營業利益卻由約 318 億元翻倍到約 652 億元，成長幾乎沒有動用新增資本。2026 年起資本支出跳到約 700 億元，新增資本能賺多少，才是接下來的考題。四項檢查點：需求基礎值、決策層級、價值鏈分配皆為中，社會容忍度為高","fact_refs":["f_peer_2308_tw_gross_margin_pct","f_peer_2308_tw_operating_margin_pct","f_peer_2308_tw_fcf_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_vrt_fcf_margin_pct","f_peer_etn_operating_margin_pct","f_peer_2301_tw_gross_margin_pct","f_peer_2301_tw_operating_margin_pct","f_peer_2301_tw_fcf_margin_pct","f_kpi1","f_kpi6_2026"],"verdict_values":{"moat":{"mechanism":"電源轉換效率加上 GPU 平台換代時的共同設計，再加電源機櫃的系統整合；轉換成本來自每代平台都要重新認證","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：新平台 12kW 電源有望首家通過認證，兩種高壓直流架構都能供貨。定價力縮減：第二季毛利率 35.6%，低於共識 0.8 個百分點；客戶在導入第二、第三供應商；液冷份額預期回落。一升一降，合計穩定。毛利率仍高於 2025 年全年的 34.27%，份額回落目前只是預期、尚未實現，還不足以判為縮減","competitor_notes":[{"name":"VRT","strategy_note":"資料中心電源與散熱的系統整合對手，近四季營益率 20.35%、FCF 利潤率 23.74%，都高於台達電；它是電源機櫃策略正面交鋒的標竿，台達電的利潤率還沒追上"},{"name":"ETN","strategy_note":"上游配電與電氣設備大廠，營益率 17.71%，與台達電相近；在高壓直流與固態變壓器上會有重疊"},{"name":"2301.TW","strategy_note":"光寶是 AI 伺服器電源最可能的第二供應商；毛利率 23.4%，比台達電低約 12 個百分點，FCF 利潤率 −6.21%，顯示它正在用資本支出與營運資金換份額"}],"peer_na_reason":"事實表未涵蓋同業 ROIC 與投入資本，以營益率與 FCF 利潤率代替報酬差距；同業只有單期資料，無法判斷差距在擴大還是收窄","threats":[{"level":"🟡","text":"雲端客戶導入第二、第三家電源與液冷供應商（點對點競爭，光寶等），份額由高檔回落","p":"70%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"Vicor 對垂直供電提出 337 專利調查，最壞情況是輸美排除令；和解或改設計的可能性較高","p":"30%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","lawsuit_class_action#0"]},{"level":"🟡","text":"上游功率半導體缺料又漲價，價值鏈的利潤往供應商移","p":"50%","evidence_refs":["supply_demand_durability#4"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 AI 伺服器與機櫃，決策者是雲端業者與 GPU 平台設計方，付款經代工廠轉手。電源與散熱是「需要」不是「想要」，延後的代價是 GPU 無法上線。但需求水位綁在雲端業者資本支出上，管理層也承認缺工缺料會影響建置節奏（2026-02-26 法說）；急迫不等於持久"},{"item":"決策層級","level":"🟡","text":"替代發生在每一代平台認證的時點，而不是在商品層；換供應商的代價是重跑認證週期。客戶正主動在每一代導入第二、第三供應商，執行長也說部分元件市占高到客戶不安。代理變數：伺服器電源占營收比重 1Q26 為 31%、2Q26 約 30%"},{"item":"價值鏈分配","level":"🟡","text":"電源與散熱在機櫃成本裡占比小，價值大多落在 GPU。上游功率半導體交期逾六個月、成本上升，下游客戶集中又分散供應，台達電夾在中間。毛利率仍比去年高，但第二季低於共識；系統型業務毛利也不一定高於零組件（2025-10-30 法說）"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的電力設備，沒有民生價格敏感的問題，優勢也不靠監管授權；能源效率產品反而受政策支持。政策風險在貿易面（美國占營收 30% 以上、337 調查），已列入風險，不在本項"}],"roiic":40,"reinvest_rate":40,"endo_ceiling":16,"formula_note":"單位皆為 %。當期 ROIC：稅後營業利益率約 13%，但事實表沒有營運資產明細，投入資本周轉率無法算出點值。增量報酬約 40%：新產能稅後營益率約 13%（近四季營益率 16.78%×（1−2025 年有效稅率 22.7%）），乘以增量資本周轉約 3 倍。周轉的推法是：共識隱含 2025→2027 年營收增約 5,100 億元，兩年資本支出約 1,400 億元，毛周轉 3.6 倍，扣掉營運資金打折。再投資率約 40%：2026 年資本支出 650–700 億元減折舊約 300 億元（2025 年 EBITDA 1,179 億元減稅前淨利 879 億元，含少量利息），淨額約 380 億元，除以稅後營業利益約 950 億元；營運資金變動事實表未涵蓋。內生上界＝40%×40%≈16%。2023–25 年稅後營業利益由約 318 億元升到約 652 億元，同期淨利減自由現金流合計約 −32 億元，歷史增量報酬失真，不採用"}}}},"q3_growth":{"verdict":"第五年後跑道中等：AI 電源仍在擴張，第二曲線（高壓直流機櫃、固態變壓器、燃料電池）有時程，但還沒量化","reasoning":"成長以量為主，來自伺服器電源、液冷與高壓直流機櫃出貨；其次是產品組合帶動營益率。沒有回購，併購只是技術補強。共識 EPS 由 2025 年 23.08 元，到 2026–28 年 37.78、60.9、94.77 元，三年年複合約 60%（EPS 預估家數事實表未涵蓋；營收共識 FY1 17 家、FY2 21 家）。內生上界約 16%，缺口約 44 個百分點。其中一部分可歸因於營益率擴張（2024 年 11.35%→近四季 16.78%）與既有產能利用率提升。但 2028 年 94.77 元對應淨利約 2,460 億元，推算需要營收比 2025 年放大 2.5–2.8 倍、淨利率 16–18%；超過最佳同業稅後營益率（約 15.7%）的那一段無法歸因，只能靠 re-rate 與共識不下修，所以長期信心上限為中。事實表未涵蓋滲透率，跑道依據是管理層時程：高壓直流 2026 下半年小量出貨、2027 年主要貢獻；固態變壓器最慢 2027 年爆發；燃料電池客戶是電力公司，一兩年內沒有實質貢獻。衰退信號亮兩項（核心份額預期回落、EPS 成長遠快於營收），長期成長性中等","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_infrastructure","f_kpi6_2026"],"verdict_values":{"growth":{"driver_mix":"量為主（AI 伺服器電源、液冷、高壓直流機櫃），產品組合帶動營益率為輔；無回購，併購為技術補強","runway_years":"5–9（事實表未涵蓋滲透率，依高壓直流 2027 年起量、固態變壓器最慢 2027 年爆發推估）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬 40%×再投資率 40%≈16%（推導見護城河報酬持續期）。共識三年 EPS 年複合約 60%，缺口約 44 個百分點：一部分歸因於營益率擴張與產能利用率，其餘無法歸因","segments":[{"item":"電源及零組件（含伺服器電源）","value":"2026 年 6 月營收比重約 50%；2025 年營收增 25%、利益增 37%；伺服器電源約占 2Q26 營收 30%"},{"item":"基礎設施（資料中心電源機櫃、液冷等）","value":"2Q26 營收 629.4 億元、占 34.3%（6 月約 37%）；2025 年營收增 82%、利益增 413%"},{"item":"自動化","value":"6 月比重約 8%；2025 年營收小增、利益減 39%；大陸市場止跌，但還沒強勁回升"},{"item":"交通（電動車）","value":"6 月比重約 5%；2025 年營收減 16%，轉為虧損"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"2Q26 毛利率 35.6%，仍高於 2025 年全年 34.27%；第三季數字本包未收"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"凱基假設液冷份額下降，最大水冷專案可能流失小部分份額；董事長也預告份額不會維持高檔"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"無證據"},{"signal":"EPS 年複合比營收高 5 個百分點以上","lit":true,"note":"2022–25 年 EPS 年複合約 22.6%、營收約 13.0%；共識 2025–28 年 EPS 年複合約 60%"},{"signal":"FCF／淨利連 2 年 <0.75","lit":false,"note":"2024 年 1.07、2025 年 0.85；2026 年資本支出跳升後要追"},{"signal":"SBC／營收 >5% 且逐年上升","lit":false,"note":"股數 2025 年約 26.04 億股、目前 25.98 億股，沒有稀釋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"高壓直流、固態變壓器是公司自身的世代轉換"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋產業倍數序列"},{"signal":"維持性資本支出占 FCF >60%","lit":false,"note":"以折舊約 300 億元代替維持性支出，約占 2025 年 FCF 513 億元的 58%，接近門檻"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"資本支出上調到 650–700 億元"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置以自建產能為主，不回購，股數穩定，約一半盈餘配息；併購的事後報酬事實表未涵蓋","reasoning":"自由現金流對淨利：2022 年 0.74、2023 年 1.28、2024 年 1.07、2025 年 0.85。2Q26 單季自由現金流 269 億元（營運現金流 431.7 億元減資本支出 162.7 億元）。2026 年資本支出 650–700 億元，比 2025 年約 466 億元多約五成，轉換率會下滑，這是接下來最該盯的股東經濟指標。淨現金約 981 億元（現金 2,132 億元，債務 1,151 億元）。2025 年度配息每股 11.6 元，約為 EPS 的一半，近四季殖利率 0.87%。併購方面，2025 年收購日本 RF 電源公司做技術補強，2026-01 處分泰達電部分股權約 87.55 億泰銖，兩者都沒有事後報酬資料。事實表未涵蓋現金去向四分","fact_refs":["f_kpi5","f_kpi6_2026","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"2025 年收購日本 RF 電源公司；2026-01 處分泰達電部分股權約 87.55 億泰銖；收購後的增量報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"未見庫藏股紀錄，事實表未涵蓋回購"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"2025 年淨利 601.1 億元÷稀釋 EPS 23.08 元≈26.04 億股，目前 25.98 億股，淨稀釋 ≤0"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購，回購為零；事實表未涵蓋現金去向四分"}}}},"q5_valuation":{"verdict":"現價要求 2027 年 EPS 至少接近 51 元，且倍數維持 24 倍以上；我們相信這個基準，但不信共識的 60.9 元，所以判合理而非便宜","reasoning":"現價 1,335 元，對 FY1（2026E）共識 37.78 元是 35.3 倍，近四季本益比 42.6 倍。本益比與股價營收比都在近四個年度端點的最高處（98.5 與 100 分位，不是五年分位）；前瞻企業價值營收比 4.45 倍。對 FY2 共識 60.9 元只有 21.9 倍，但這個分母近期仍在下修，而且遠超內生上界，便宜的論證不成立；改用本文基準 2027 年 51 元，約 26 倍。PEG 用共識三年年複合 60% 算出 0.59，同樣受分母爭議影響，只供對照。7 月底券商目標價落在 1,930–2,505 元；9 月中又有投顧由 2,300 元下修到 2,200 元，用的是 2027 年 EPS 62.5 元×35 倍，正是本文不採用的分母。基準情境五年後約 1,872 元，年化約 7%，加股息約 8%，落在中等區","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_fy2_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 共識 EPS）為主、PEG 為輔；FY2 分母有爭議","tier":"AI 資料中心電源硬體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比；改以券商採用的 2027 年 35 倍作對照"},"fwd_pe":35.34,"peg":0.59,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"事實表未涵蓋五年分位，只有四個年度端點的分位 98.5，不外推。判合理的依據：本文基準 2027 年 EPS 51 元對應約 26 倍，基準情境五年年化約 8%（含股息），屬中等。短期上檔＝2027 年 51 元×27 倍，約 1,377 元（+3.1%）；中期上檔＝2029 年 67 元×25 倍，約 1,675 元（三年 +25.5%）。不判便宜，因為便宜的說法全靠 FY2 共識分母；不判昂貴，因為股價半年已跌 38%，基準情境仍有正報酬","upside_short_pct":3.1,"upside_mid_pct":25.5,"denominator_disputed":true,"denominator_note":"FY2 共識 EPS 60.9 元最近一次快照下修 4.6%，FY1 近三月下修 6.6%；隱含的三年 EPS 年複合約 60%，遠高於內生上界 16%，所以用 FY2 算出的 21.9 倍不能當便宜的證據。FY1 分母另含第二季業外收益 44.3 億元"}}},"q6_how_wrong":{"verdict":"價值陷阱風險中等：最可能看錯的是 2027 年 EPS 分母與新平台份額，不是需求方向","reasoning":"衰退信號亮兩項（份額預期回落、EPS 成長遠快於營收），價值陷阱風險中等。空方最強的數字：FY1 共識近三月下修 6.6%，九月營收年增降到 14.6%，第二季營業利益比共識少 9.5%，股價 26 週跌 38%（RSI 25.6）。可能看錯的路有三條：一是共識 2027–28 年分母過高，連本文基準都還偏樂觀；二是新平台主供應商地位流失；三是 337 調查裁定侵權（受影響營收比重事實表未涵蓋）。2025-10-30 法說上，管理層三度避開具體數字（AI 營收占比、毛利率與費用率走向、美國製造成本），能見度有限。成長熄火壓力測試：基準路徑在 2029 年後成長分別降到 15%、10%、5%，配 22、18、14 倍，五年後約 1,950、1,460、1,030 元，三項中有兩項高於現價。歷史最大回撤只有 26 週 −38% 這一筆資料","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_kpi2_ifrs_non_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長延續，但份額與毛利率在正常化"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":37.78,"pe":35.34,"basis":"FY1（2026E）共識 EPS 37.78 元，年度已過十個月，視同當年口徑；終端倍數同樣乘以終端年度 EPS"},"eps":{"bull":[61,90,105,117,127],"base":[51,60,67,73,78],"bear":[40,36,40,44,48]},"pe":{"bull":30,"base":24,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.87,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-55,"hi":-40,"basis":"近 26 週已跌 38%。高端 −40%：基準路徑 2027 年 EPS 51 元，若遇資本支出消化期、倍數一度壓到 16 倍，約 816 元。低端 −55%：空方路徑 2028 年 EPS 36 元×16.5 倍，約 594 元。論點目前完整，這是深回撤的心理準備，不因波動砍倉","trigger_time":null},"basis":{"bull":"共識路徑大致兌現：2027 年 EPS 61 元、2028 年 90 元，高壓直流與電源機櫃放量，營益率升到 19% 上下；終端 30 倍，低於券商採用的 35 倍","base":"營收 2027 年增約 25%，之後逐年降到個位數；營益率守在 16–17%，份額正常化；2027 年 EPS 51 元，五年年複合約 15.6%，在內生上界 16% 以內。終端 24 倍；同業前瞻本益比事實表未涵蓋，對照錨是券商的 2027 年 35 倍與本身目前對 FY1 的 35.3 倍","bear":"雲端資本支出消化，加上份額流失：2027 年 EPS 40 元，2028 年降到 36 元，之後緩慢回升；終端 16 倍，介於成長熄火到 10%（18 倍）與 5%（14 倍）之間"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY1 共識近三月下修 6.6%，FY2 再降 4.6%；九月營收年增降到 14.6%；券商 7 月底與 9 月連續下修目標價；董事長預告份額不會維持高檔","assumption":"本文基準假設 2027 年 EPS 51 元，且雲端資本支出 2027 年仍成長","consequence":"若雲端業者 2027 年進入資本支出消化期，新平台份額又被第二供應商分走，2027–28 年 EPS 會停在 36–40 元，倍數壓到 16 倍，五年後約 770 元，較現價 −42%","ruling":"採納為空方路徑，機率 30%。與 Single Thing 部分重疊：Single Thing 只看新平台份額，本條再加上資本支出消化，兩者並存","watch":"月營收年增率、FY2 共識 EPS、伺服器電源占營收比重","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","competitive_share_entrants#2","customer_second_source#0"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年資本支出 650–700 億元，比 2025 年多約五成，2027–28 年可能再增；第二季毛利率與營益率低於共識，主因是零組件成本；2025-10-30 法說稱系統型業務毛利不一定高於零組件；337 若和解可能附帶權利金","assumption":"本文假設新產能增量報酬 40%，自由現金流對淨利不低於 0.75","consequence":"營收照樣翻倍，但若增量報酬掉到 20% 以下、轉換率跌破 0.75，EPS 成長會落後營收，倍數也會往一般硬體靠攏","ruling":"採納：把自由現金流對淨利列為減碼指標；增量報酬假設一旦證偽，下修到 25%","watch":"年度自由現金流÷淨利、季營益率","evidence_refs":["supply_demand_durability#4","capital_markets_pricing#3","regulatory_antitrust#1"],"fact_refs":["f_kpi6_2026","f_kpi3_ifrs","f_kpi5"]},{"view":"價格已反映太多","evidence":"跌了 38% 之後，近四季本益比 42.6 倍、股價營收比 4.94 倍，仍在近四個年度端點的最高處；對 FY1 仍有 35.3 倍","assumption":"本文基準 2027 年 51 元對應約 26 倍，並假設倍數五年內降到 24 倍","consequence":"若市場改用一般電源硬體的十幾倍來看，即使 EPS 照基準走，股價也只能原地踏步","ruling":"部分採納：價格不便宜，所以不追；但股價已從高點跌 38%，基準情境仍有約 8% 年化報酬，不構成迴避的理由","watch":"FY1 與 FY2 前瞻本益比","fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1640.0 → 本次 1335.0（-18.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1640.0","side_b":"本次 price_at_dd=1335.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,640 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,640 元：Bull 價 4,424、Bear 價 880，五年期望值 +48.7%，基準年化 7.7%，不對稱比 3.1","side_b":"本次情境、股價仍用 1,640 元：Bull 價 3,810、Bear 價 768，五年期望值 +23.5%，基準年化 2.7%，不對稱比 2.07","ruling":"先換情境、股價不動：五年期望值少 25.2 個百分點，基準年化少 5.0 個百分點。不對稱比由 3.1 變為 2.07。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,640 元：五年期望值 +23.5%，基準年化 2.7%，不對稱比 2.07","side_b":"本次情境、股價 1,335 元：五年期望值 +51.7%，基準年化 7.0%，不對稱比 3.64","ruling":"再換股價、情境不動：起點價下跌 18.6%，五年期望值多 28.2 個百分點，基準年化多 4.3 個百分點，不對稱比由 2.07 升到 3.64。合計五年期望值比前份多 3.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：需求方向","cause":null,"side_a":"管理層：看不到 AI 停下來，泰國、大陸、美國持續建廠（2026-07 董事長）","side_b":"數據：7 月營收 670.7 億元、第三季約 1,971 億元，都創新高，第三季年增 31.1%","ruling":"兩邊一致：需求方向沒有反轉的證據，九月降速來自缺料造成的出貨遞延","evidence_level":"一致","settle_metric":"第四季營收","if_then":["若第四季營收 ≥2,180 億元，需求判斷維持","若第四季營收 <2,050 億元，且管理層不再歸因於缺料，需求判斷改為降溫，空頭機率升到 35%"],"evidence_refs":["end_markets#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"買方：26 週跌 38%，RSI 25.6；對 FY2 共識只有 21.9 倍；淨現金約 981 億元；第三季營收約 1,971 億元仍創新高；資本支出上調代表客戶訂單能見度；券商目標價 1,930–2,505 元全在現價之上","side_b":"觀望方：FY2 分母仍在下修，且超出內生上界；本包沒有第三季毛利率；第二季毛利率與營益率已低於共識；份額正常化與 337 調查都還沒落地","ruling":"選觀望。買方的論證幾乎全建立在 FY2 共識分母上，而分母正是爭點；股價下跌本身不是安全邊際。現價已接近本文基準的合理值，下一批證據（10 月營收、第三季毛利率）兩週內可得，等待成本低","evidence_level":"程度差異：分歧在時點與分母，不在方向","settle_metric":"10 月營收年增率、第三季毛利率","if_then":["若兩項同時達標，重跑判斷，通過後以小倉起步","若股價續跌而兩項達標，分批反買，不等更低價","若股價反彈而兩項未達標，不追"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"共識 2027–28 年 EPS 是否過高","cause":null,"side_a":"共識：2026–28 年 EPS 37.78、60.9、94.77 元，三年年複合約 60%","side_b":"本文：基準 2027 年 51 元、2028 年 60 元。2028 年 94.77 元對應淨利約 2,460 億元，推算要營收比 2025 年放大 2.5–2.8 倍、淨利率 16–18%；這高於台達電近四季營益率的稅後水準約 13%，也高於利潤率最高的同業 VRT（營益率 20.35%，稅後約 15.7%）","ruling":"採本文。共識近三月持續下修，又超過內生上界 16%，董事長也已預告份額不會維持高檔。賣方錯在把 2025–26 年缺貨期的份額與利潤率外推到 2028 年；股價已跌 38%，不等於有安全邊際","evidence_level":"程度差異","settle_metric":"2027 上半年單季 EPS","if_then":["若 2027 上半年單季 EPS ≥14 元，基準 2027 年 EPS 上修到 58 元，並重跑判斷決定是否建首倉","若 2027 上半年單季 EPS <11 元，空頭機率升到 40%，不建倉"],"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","capital_markets_pricing#0"]},{"axis":"關稅由誰負擔","cause":null,"side_a":"管理層（2025-10-30 法說）：超過 95% 業務為 FOB，關稅由客戶負擔，有時公司先墊付再向客戶請款","side_b":"法人估計：液冷部分零組件的關稅要自行負擔，液冷毛利率可能降約 5 個百分點；另有文章稱美國占營收 30% 以上","ruling":"主體採信管理層，因為是一手資料、時間也較新；法人估計的來源頁未逐字讀取、日期未確認，只當作監測液冷毛利率的理由","evidence_level":"可調和（程度差異）","settle_metric":"季毛利率與管理層對關稅的說明","if_then":["若毛利率連 2 季低於 34%，且管理層把原因歸到關稅，關稅風險升為中期主要風險，空頭機率加 5 個百分點","若毛利率維持 ≥35%，關稅風險維持觀察"],"evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","customer_concentration_credit#2"]},{"axis":"資本支出改口","cause":null,"side_a":"2025-10-30 法說：明年資本支出金額與今年相近，內容偏工廠自動化與設備","side_b":"2026-07-30 法說：全年約 700 億元，比 2025 年 466 億元增約 50%，且 2027–28 年原則上仍可能成長","ruling":"說法前後方向相反，但可以調和：需求比管理層九個月前預期得更強，再投資負擔也明顯加重。兩者都採納：需求面加分，但股東經濟要看新產能的報酬，所以把自由現金流對淨利列為減碼指標","evidence_level":"可調和","settle_metric":"自由現金流÷淨利","if_then":["若 2026–27 年自由現金流對淨利連兩年低於 0.75，增量報酬下修到 25%，基準 EPS 路徑下修 10%；已持有則減碼一半","若維持 ≥0.85，維持 40% 的假設"],"evidence_refs":["supply_demand_durability#0","geo_supply_chain#2"]},{"axis":"337 調查的影響","cause":null,"side_a":"公司：將積極因應，相關產品目前未受影響（2026-10-12 重大訊息）","side_b":"申訴方 Vicor 要求有限排除令與停止侵權命令；立案日 2026-10-09，被調查方含鴻海、廣達等 20 家","ruling":"程序性質是民事專利與進口爭議，不是刑事，也不是集體訴訟；受影響營收比重事實表未涵蓋。二手來源稱雙方先前爭議已於 2025 年 5 月和解，這次和解或改設計的可能性較高。初裁（約 2027 年第四季到 2028 年上半年）之前不可裁決","evidence_level":"不可裁決至初裁","settle_metric":"337-TA-1526 初裁結果","if_then":["若初裁認定侵權：未持有則不建倉，已持有則減碼一半；終裁發布排除令且無法改設計則清倉","若宣布和解，且權利金沒有壓低毛利率，此項風險解除"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","lawsuit_class_action#1"]},{"axis":"股價兩週跌 18.6% 後的估值、機率與回撤","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（10-19，股價 1,640 元）：估值合理，多頭機率 25%、空頭 30%，最大回撤約 −60%，觀望","side_b":"本次（股價 1,335 元）：估值仍判合理，機率 25／45／30 不變；最大回撤區間 −40%～−55%，以較低的起點計","ruling":"股價下跌讓 FY1 本益比由約 41 倍降到 35 倍，但分母同時下修（FY1 −6.4%）；以本文基準 2027 年 51 元計約 26 倍，還沒到便宜，估值結論不變。基本面證據方向沒變，所以機率不動。回撤區間縮小只是因為起點較低，不代表風險降低。若裁決或角色改列，原因只會是價格與均線，基本面輸入沒有變","evidence_level":"前後份對帳","settle_metric":"FY2 共識 EPS、月營收年增率","if_then":["若股價續跌，而 10 月營收年增 ≥20%、第三季毛利率 ≥35%，重跑判斷後分批反買","若股價反彈而兩項未成立，不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"十月以來的新證據是否改變基本面結論","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：訊號 B、陷阱風險中等、護城河方向穩定（→）、第五年後跑道中等、品質複利成長、中循環","side_b":"本次新增：FY1 共識再降 6.4%、FY2 降 4.6%；九月營收年增降到 14.6%；337 調查已立案（10-09）。判讀後六欄全部維持","ruling":"九月降速的主因是功率半導體缺料造成出貨遞延，屬供給面。需求面（雲端業者資本支出、產能吃緊、資本支出上調到約 700 億元）沒有反轉，所以循環位置仍在中段。份額下滑還是預期、尚未實現，護城河方向維持。衰退信號仍只亮兩項，陷阱風險維持中等","evidence_level":"前後份對帳","settle_metric":"第四季營收能否回補到約 2,180 億元（達成全年共識所需）","if_then":["若第四季營收低於 2,050 億元，且十二月年增 <10%，循環位置改判晚段，空頭機率升到 40%，不建倉","若第四季營收 ≥2,180 億元，維持中段判讀"],"evidence_refs":["end_markets#2","competitive_share_entrants#0","regulatory_antitrust#0"]},{"axis":"重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","side_b":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","ruling":"門檻維持原文，因為約束還是同一個：第三季毛利率與第四季出貨回補都沒證實。第三季財報 10-28 已公布，但本包沒有收毛利率；10 月營收要到 11 月上旬才公布，兩項都還沒發火。FY1 共識在財報前後再降 6.4%，暗示第三季可能不如預期，但不據此推定。前份觸發器沒有任何一條發火","evidence_level":"前後份對帳","settle_metric":"第三季毛利率、10 月營收年增率","if_then":["若兩項同時成立，重跑判斷，通過後建首倉","若第三季毛利率 <34%，重啟順延到第四季財報（2027-02），期間不追"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"下一代 NVIDIA 平台（VR200）的 12kW 伺服器電源與高壓直流機櫃，台達電在 2027 年量產時失去首家主供應商地位","ruling":"前份是舊格式，沒有產出 Single Thing。本次選平台份額而不選 337 調查，因為伺服器電源約占營收 30%，又是 2027 年成長主力，敏感度最大；337 的受影響營收不明，和解機率也較高。一旦發生就移出名單，已持有則清倉","evidence_level":"前後份對帳","settle_metric":"新平台首批量產的供應商分配","if_then":["若確認新平台首批量產由台達電主供，Single Thing 機率降到 15%","若法說或供應鏈確認失去主供應商，清倉並移出名單"],"evidence_refs":["customer_second_source#0","competitive_share_entrants#0"]},{"axis":"減碼與清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼或清倉指標","side_b":"毛利率連 2 季 <34%；月營收年增連 3 個月 <10%；FY2 共識 EPS <51.8 元；自由現金流對淨利連 2 年 <0.75；337 初裁認定侵權。任一觸發，已持有者減碼一半；Single Thing 發生則清倉","ruling":"前份是舊格式，沒有產出指標。本次按三條主要風險（缺料與毛利率、份額與共識、擴產報酬）加上 337 調查，各設一項可量測的門檻","evidence_level":"前後份對帳","settle_metric":"上述五項指標","if_then":["若任一指標觸發且已持有，減碼一半","若兩項以上同時觸發，清倉"]}],"triggers":[{"n":1,"text":"10 月營收年增率是否回到 20% 以上，確認第四季出貨回補","type":"假設驗證","maps_to":"H1","metric":"月營收年增率","threshold":"≥20%","action":"達標即滿足重啟條件之一","source_freq":"公開資訊觀測站月營收，每月 10 日前","date":"2026-11-10","evidence_refs":["end_markets#2"]},{"n":2,"text":"第三季毛利率是否守住 35%（10-28 已公布，本包未收）","type":"假設驗證","maps_to":"H2","metric":"季毛利率（IFRS）","threshold":"≥35%","action":"達標即滿足重啟條件之一；低於 34% 則重啟順延到第四季財報","source_freq":"公司 IR 季度簡報，每季","date":"2026-10-28","evidence_refs":["capital_markets_pricing#3"]},{"n":3,"text":"兩項重啟條件同時成立","type":"估值rearm","maps_to":"重啟條件","metric":"第三季毛利率與 10 月營收年增率","threshold":"毛利率 ≥35% 且營收年增 ≥20%","action":"重跑判斷，通過後以小倉試單","source_freq":"每月與每季","date":"2026-11-10"},{"n":4,"text":"缺料延長，第四季出貨沒有回補","type":"風險","maps_to":"R1","metric":"第四季營收、季毛利率","threshold":"第四季營收 <2,050 億元，或毛利率 <34%","action":"重啟延後一季，空頭機率升到 35%","source_freq":"月營收與季報","date":"2027-02","evidence_refs":["supply_demand_durability#4","end_markets#2"]},{"n":5,"text":"伺服器電源份額回落","type":"風險","maps_to":"R2","metric":"伺服器電源占營收比重","threshold":"連 2 季 <25%（2Q26 約 30%）","action":"不建倉，護城河方向改判縮減，並重跑判斷","source_freq":"法說與券商報告，每季","date":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"n":6,"text":"337 調查（Vicor，垂直供電）初裁","type":"風險","maps_to":"R3","metric":"USITC 337-TA-1526 初裁結果","threshold":"認定侵權或發布排除令","action":"不建倉；已持有則減碼一半","source_freq":"USITC 案卷與公開資訊觀測站重大訊息，事件型","date":"2027-12","evidence_refs":["major_events#0","regulatory_antitrust#1"]},{"n":7,"text":"下一代平台的主供應商地位","type":"Single Thing","maps_to":"Single Thing","metric":"VR200 12kW 電源與高壓直流機櫃首批量產供應商","threshold":"失去首家主供應商","action":"移出名單；已持有則清倉","source_freq":"法說、供應鏈與券商報告，每季","date":"2027-06","evidence_refs":["competitive_share_entrants#0"]},{"n":8,"text":"共識 2027 年 EPS 持續下修","type":"減碼","maps_to":"R4","metric":"FY2 共識 EPS","threshold":"<51.8 元（較 60.9 元累計下修 >15%）","action":"已持有則減碼一半；未持有則在重啟條件加上共識止跌","source_freq":"共識快照，每月","date":null,"evidence_refs":["capital_markets_pricing#0"]},{"n":9,"text":"擴產後現金轉換惡化","type":"減碼","maps_to":"H3","metric":"自由現金流÷淨利","threshold":"連 2 年 <0.75","action":"已持有則減碼一半，增量報酬假設下修到 25%","source_freq":"年報，每年","date":"2028-03"},{"n":10,"text":"10 月營收與第三季損益入表後複審","type":"複審日期","maps_to":"重啟條件","metric":null,"threshold":null,"action":"重跑判斷","source_freq":"事件型","date":"2026-11-16"},{"n":11,"text":"第四季財報與 2027 年資本支出指引公布後複審","type":"複審日期","maps_to":"H2","metric":null,"threshold":null,"action":"重跑判斷","source_freq":"每季","date":"2027-03-02"}],"kill_metrics":[{"metric":"季毛利率（IFRS）","bear_threshold":"連 2 季 <34%","window":"2026Q3–2027Q2","source":"公司 IR 季度簡報","last_status":"unknown"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 <10%","window":"2026-10 至 2027-06","source":"公開資訊觀測站月營收","last_status":"warning"},{"metric":"FY2（2027）共識 EPS","bear_threshold":"<51.8 元（較 60.9 元累計下修 >15%）","window":"2026-11 至 2027-06","source":"Koyfin 共識快照","last_status":"warning"},{"metric":"自由現金流÷淨利","bear_threshold":"連 2 年 <0.75","window":"FY2026–FY2027","source":"年度現金流量表","last_status":"ok"},{"metric":"337 調查（337-TA-1526）初裁","bear_threshold":"認定侵權或發布排除令","window":"2027-10 至 2028-04","source":"USITC 案卷、公開資訊觀測站重大訊息","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","exec_line":"現在不建倉，也不設進場價。兩項條件同時成立後重跑判斷，通過才以小倉試單起步；條件成立前，股價漲跌都不追、不攤平"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等 10 月營收年增 ≥20% 與第三季毛利率 ≥35% 同時證實；不設進場價","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-38.01, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 資料中心電源與散熱需求在 2027 年仍高成長，台達電營收跟得上","2y":"2027 年營收 ≥9,500 億元（較 FY1 共識 7,578 億元增約 25%）","5y":null,"10y":null,"threshold":"2027 年營收 ≥9,500 億元；月營收年增率季平均 ≥20%","source":"公開資訊觀測站月營收、公司季報","drift_rule":"近四季營收較本論點路徑偏離 ≥5% 連 2 季＝削弱；偏離 ≥10% 連 3 季＝反轉"},{"id":"H2","text":"即使零組件成本上升、客戶分散供應，毛利率仍守在 34% 以上、營益率 15% 以上","2y":"2026Q3–2027Q4 季毛利率 ≥34%、營益率 ≥15%","5y":null,"10y":null,"threshold":"季毛利率 ≥34% 且營益率 ≥15%","source":"公司 IR 季度法說簡報","drift_rule":"近四季毛利率低於 34% 門檻 5%（<32.3%）連 2 季＝削弱；低於門檻 10%（<30.6%）連 3 季＝反轉"},{"id":"H3","text":"高壓直流電源機櫃自 2027 年放量，成為第二條成長腿，擴產的資本賺得回來","2y":null,"5y":"2028 年基礎設施部門營收占比 ≥40%，且自由現金流÷淨利維持 ≥0.75","10y":null,"threshold":"基礎設施部門營收占比 ≥40%（2Q26 為 34.3%）","source":"公司 IR 分部營收與利益、年度現金流量表","drift_rule":"近四季分部營收較路徑偏離 ≥5% 連 4 季＝削弱；偏離 ≥10% 連 6 季＝反轉"}],"R":[{"id":"R1","text":"功率半導體（IGBT、MOSFET、PMIC）缺料拖到第四季以後，出貨遞延並壓縮毛利率","h_ref":"H2","clock":"⚡","threshold":"第四季營收 <2,050 億元，或季毛利率 <34%","evidence_refs":["supply_demand_durability#4","end_markets#2","capital_markets_pricing#3","capital_markets_pricing#4"]},{"id":"R2","text":"雲端客戶導入第二、第三供應商，台達電在伺服器電源與液冷的份額從高檔回落","h_ref":"H1","clock":"🔥","threshold":"伺服器電源占營收比重連 2 季低於 25%（2Q26 約 30%），或下一代平台失去首家供應商地位","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"id":"R3","text":"Vicor 的 337 調查若裁定侵權，垂直供電產品可能被禁止輸美","h_ref":"H1","clock":"🔥","threshold":"行政法官初裁認定侵權或發布排除令；受影響營收比重事實表未涵蓋","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R4","text":"雲端業者 AI 資本支出進入消化期，2027–28 年營收成長大幅降速","h_ref":"H1","clock":"🐢","threshold":"FY2 共識 EPS 累計下修 >15%（低於 51.8 元），或月營收年增率連 3 個月 <10%","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"id":"R5","text":"美國關稅與產地限制：美國占營收 30% 以上，液冷部分關稅可能要自行吸收","h_ref":"H2","clock":"🔥","threshold":"季毛利率連 2 季 <34% 且管理層歸因於關稅，或 FOB 比重低於 95%","evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","customer_concentration_credit#2","geo_supply_chain#1"]},{"id":"R6","text":"交通（電動車）部門 2025 年轉虧，處於需求修正期，公司會視需求在 AI 與電動車之間調配產能","h_ref":"H2","clock":"🐢","threshold":"交通部門 2026、2027 年連續虧損，且營收續降","evidence_refs":["channel_business_model_shift#3"]}],"single_thing":{"description":"下一代 NVIDIA 平台（VR200）的 12kW 伺服器電源與高壓直流機櫃，台達電在 2027 年量產時失去首家主供應商地位","why_fatal":"伺服器電源約占第二季營收 30%，也是 2027 年成長的主要來源。失去主供應商位置，2027 年 EPS 會從本文基準 51 元落到約 40 元，倍數同時壓到 16 倍，股價約 640 元；這是情境樹裡單一影響最大的項目","if_happens":"不建倉，移出名單；屆時若已持有則清倉","how_monitor":"每季伺服器電源占營收比重、法說對新平台認證與出貨的說法、券商供應鏈報告、月營收年增率","probability":"約 25%（12–24 個月）：客戶已在找第二、第三供應商，董事長也預告份額不會維持；但凱基認為台達電有望首家通過認證"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.9,"peg_fy2":0.36,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":23.08,"FY2026E":37.78,"FY2027E":60.9,"FY2028E":94.77},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（台達電沒有 non-GAAP 口徑）；共識為 Koyfin 美元值，依 32.5669 匯率換算新台幣"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"10 月營收公布","impact":"高","watch":"年增率是否 ≥20%，第四季出貨是否回補"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報，以及 2027 年資本支出與產品展望","impact":"高","watch":"毛利率、2027 年資本支出、高壓直流出貨時程"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"NVIDIA 下一代平台（VR200）量產與電源供應商分配","impact":"高","watch":"台達電是否為首家主供應商"},{"date":"2027-12","date_precision":"quarter","type":"regulatory","event":"Vicor 337 調查初裁時點（立案後 12–18 個月）","impact":"中","watch":"初裁是否認定侵權、是否和解"}]}
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
