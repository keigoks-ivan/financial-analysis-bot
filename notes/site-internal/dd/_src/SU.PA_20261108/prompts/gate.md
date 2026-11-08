你是 DD 管線 v20 的判斷層閘（gate），標的 SU.PA（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_revenue_q3`（q1_business）｜Revenue（Q3，營收）＝11460 € million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 營收新聞稿（Rueil-Malmaison, 2026-10-16），https://www.webdisclosure.com/press-release/third-quarter-revenues-2026-odiihfxJLgs（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-16））
  - 註記：有機成長 +16.9% 對分析師預期 13.8%（來源：Quartr Q3 2026 summary 經 web_search，未核對原始共識）
- `f_kpi1_revenue_h1`（q1_business）｜Revenue（H1，營收）＝21.2 € billion｜期間與口徑：H1 2026（半年報，2026-07-30 公告）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 H1 2026 新聞稿（2026-07-30），經 web_search 摘要（emr-online／optionfinance），非直接讀原稿（numbers.latest_quarter_kpis.items[1]，as_of H1 2026（半年報，2026-07-30 公告））
  - 註記：查無
- `f_kpi2_adjusted_ebita_non_gaap`（q1_business）｜Adjusted EBITA（Non-GAAP 營業利益）與利益率＝19.3 % margin（Adj. EBITA €4.1bn，有機 +22%，利益率有機 +120bps）｜期間與口徑：H1 2026（半年報，2026-07-30 公告）；Q3 無單季數字／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 H1 2026 新聞稿（2026-07-30），經 web_search 摘要，非直接讀原稿（numbers.latest_quarter_kpis.items[2]，as_of H1 2026（半年報，2026-07-30 公告）；Q3 無單季數字）
  - 註記：查無
- `f_kpi4_net_income`（q1_business）｜Net income（淨利）＝2.5 € billion｜期間與口徑：H1 2026（半年報，2026-07-30 公告）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 H1 2026 新聞稿，經 web_search 摘要（numbers.latest_quarter_kpis.items[4]，as_of H1 2026（半年報，2026-07-30 公告））
  - 註記：查無
- `f_kpi5_2026_q3`（q1_business）｜2026 全年指引（Q3 後上修）＝營收有機 +12%～+14%；Adj. EBITA 有機 +18%～+21%；利益率有機 +100～+120bps，隱含約 19.7%～19.9% organic｜期間與口徑：Q3 2026（公告於 2026-10-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 營收新聞稿，https://www.webdisclosure.com/press-release/third-quarter-revenues-2026-odiihfxJLgs（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-10-16））
  - 註記：查無
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_fcf_margin_pct`（q2_moat）｜ETN FCF 利潤率＝11.87 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abbn_sw_gross_margin_pct`（q2_moat）｜ABBN.SW 毛利率＝40.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abbn_sw_operating_margin_pct`（q2_moat）｜ABBN.SW 營業利益率＝17.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abbn_sw_fcf_margin_pct`（q2_moat）｜ABBN.SW FCF 利潤率＝13.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lr_pa_gross_margin_pct`（q2_moat）｜LR.PA 毛利率＝49.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LR.PA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lr_pa_operating_margin_pct`（q2_moat）｜LR.PA 營業利益率＝19.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LR.PA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lr_pa_fcf_margin_pct`（q2_moat）｜LR.PA FCF 利潤率＝13.51 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LR.PA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sie_de_gross_margin_pct`（q2_moat）｜SIE.DE 毛利率＝39.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIE.DE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sie_de_operating_margin_pct`（q2_moat）｜SIE.DE 營業利益率＝12.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIE.DE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sie_de_fcf_margin_pct`（q2_moat）｜SIE.DE FCF 利潤率＝14.61 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIE.DE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.37 USD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.59 USD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝45342.69 EUR m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝50495.77 EUR m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q4_capital）｜Free cash flow（自由現金流）＝1.6 € billion｜期間與口徑：H1 2026（半年報，2026-07-30 公告）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 H1 2026 新聞稿，經 web_search 摘要（connaissancedesenergies／AFP）：較去年同期增逾三倍，部分因去年有法國法律罰款（numbers.latest_quarter_kpis.items[3]，as_of H1 2026（半年報，2026-07-30 公告））
  - 註記：查無
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝16291.0 EUR m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 20809.0、現金 4518.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝150671.89 EUR m｜期間與口徑：2026-11-08／市值 134380.89 ＋ 淨負債 16291.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝587.71 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝228.65 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝27.48 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝57.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝57.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝81.8 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.58 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝97.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝97.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.32 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.837 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-14.81 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝32.85｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w250`（q5_valuation）｜250 週均線＝193.61 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：法國競爭管理局2024-10-29裁定 Schneider 與經銷商 Rexel、Sonepar 間2012-12至2018-09的轉售價格安排違規，Schneider 被罰2.07億歐元（四家合計4.7億歐元）；Schneider 表示不同意並保留上訴權；搜尋未見2026年上訴結果
  - 來源：Bloomberg Law: Schneider Among Firms Fined €470 Million in French Cartel Case（as_of 2024-10-30）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Schneider FY2025 results (Feb 2026): CFO Maxson guided 2026 import-tariff impact (incl. US) relative to the EUR160m incremental 2025 impact; reports conflict on the multiple
  - 來源：Reuters via itiger: Schneider Electric Exceeds Profit Expectations as Data Center Demand Counters Weak Dollar Impact（as_of 2026-02-26）｜affects：decision_inputs.bear、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Uptime Institute 分析指固態變壓器（SST）可把中壓交流直接轉為 400/480V AC 或 800V DC，部分設計可能不再需要 sidecar（Schneider 現行 800VDC 方案採 sidecar）；SST 仍在開發與產業化階段
  - 來源：Uptime Institute intelligence report（as_of 2026-01-15）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Navitas 與 EPFL 於 APEC 2026 展示 250kW SST，用於 800V DC 資料中心架構
  - 來源：Electronic Design（as_of 2026-04-20）｜affects：moat_trend
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Chile SERNAC 公告 Schneider SYBTU 電池模組安全警示（2024-12 至 2026-09 銷售），內部電池模組可能故障
  - 來源：SERNAC（as_of 2026-09-30）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：Chile SERNAC 公告 SYBTU 電池模組安全警示（2024-12 至 2026-09 銷售）
  - 來源：SERNAC（as_of 2026-09-30）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 33 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":540.0,"bear_5y_price":183.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":60.9,"ev5y_pct":51.7,"irr_base_pct":10.0,"asym_ratio":4.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.37,"pe":22.05,"basis":"FY2026E（FY1）共識 EPS，與終端倍數同為當年度預估 EPS 口徑"},"eps":{"bull":[12.9,15.3,17.8,20.2,22.5],"base":[12.2,13.7,15.3,16.9,18.4],"bear":[11.2,10.3,10.6,11.4,12.2]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.837,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SU.PA_2024_Earnings_Call_20250220.md
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 調整後 EBITA 有機成長目標 10%–15%（原話："we have set up a target with an improvement of our adjusted EBITA from 10% to 15% organically."）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 有機營收成長目標 7%–10%（原話："strong growth organically between 7% and 10% for the year 2025"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 調整後 EBITA 利潤率目標約 19.2%–19.5%（原話："an adjusted EBITA margin around 19.2% to 19.5%"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：跨循環成長率維持 7%–10%（原話："we confirm really this 7% to 10% growth across the cycle"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 匯率預期轉為正貢獻，營收約 +6–7 億歐元（原話："plus EUR 600 million to EUR 700 million to our top line"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 有效稅率預期 23%–25%（原話："our ETR will be in the range of 23% to 25% for 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 現金轉換率預期再度接近 100%，含資本支出增加（原話："the cash conversion ratio to again be approaching 100%"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：Discrete 自動化需求回升，預期下半年加速（原話："accelerating a bit more in the second part of the year 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2025 毛利率仍有進步但幅度較小（原話："some gross margin progression, but at a more muted level"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：Systems 定價在 2025 預期趨於正常化（原話："We would expect some normalization of that in 2025."）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2025 毛利率放緩原因：Systems 定價正常化，加上正常範圍的產業生產力（原話："more normal pricing in Systems"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2024 工業自動化調整後 EBITA 利潤率下滑 150bp，管理層稱符合預期（原話："was down, as expected, 150 basis points"）
- 2025-02-20｜Olivier Blum (CEO)｜margin：管理層稱 AI 訓練／推論資料中心對利潤率無特別影響（原話："From a margin standpoint, it does not have any particular impact."）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：數字口徑：資料中心占訂單 24% 的拆解（原話："Around 20% of that is pure Data Center, around 4% is Distributed IT now."）
- 2025-02-20｜Hilary Maxson (CFO)｜customer：純資料中心中，超大規模雲端客戶占比不到一半（原話："Of that 20%, a bit less than half of that will be with hyperscalers."）
- 2025-02-20｜Olivier Blum (CEO)｜customer：資料中心占 2024 終端訂單 24%（原話："that represents 24% of our end orders in 2024"）
- 2025-02-20｜Hilary Maxson (CFO)｜customer：資料中心成長描述為健康而非指數式（原話："As we've said before, not exponential, but healthy growth"）
- 2025-02-20｜Olivier Blum (CEO)｜customer：針對 DeepSeek 提問，稱客戶端訂單趨勢沒有變化（原話："there is no change in the trend"）
- 2025-02-20｜Olivier Blum (CEO)｜customer：北美占比：在地製造在地銷售比例（原話："we have already 83% of what we sell in North America"）
- 2025-02-20｜Olivier Blum (CEO)｜competition：DeepSeek 被詮釋為 AI 消耗量增加的佐證（原話："the consumption for AI will get bigger and bigger"）
- 2025-02-20｜Hilary Maxson (CFO)｜product：數位與數位賦能營收占比及軟體循環收入占比（原話："we're now at 77% recurring revenues in agnostic software"）
- 2025-02-20｜Hilary Maxson (CFO)｜product：Systems 業務 Q4 銷售成長 27%（原話："translating into sales of plus 27%"）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：北美住宅市場疲弱，管理層歸因於高利率（原話："We did see some weakness in residential, particularly in the U.S."）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：法國競爭主管機關罰款已提列 1.04 億歐元準備（原話："a provision of EUR 104 million tied to the fine"）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：關稅：若現行貿易協定特殊區維持，墨西哥對美進口曝險規模（原話："only in a few hundred millions"）
- 2025-02-20｜Olivier Blum (CEO)｜risk：中國 2025 預期無重大轉變（原話："we don't expect any major shift in 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：不排除特別配息（原話："not averse to some sort of special distribution"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：庫藏股僅用於抵銷員工持股計畫（原話："share buybacks to neutralize our employee share plans"）
- 2025-02-20｜Olivier Blum (CEO)｜capital_allocation：2027 計畫不含併購（原話："the plan that we have presented by '27 is without M&A"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：第 15 年累進股息提案（原話："dividend for the 15th year of EUR 3.90 per share"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：下一循環增量產能投資 20 億歐元（原話："EUR 2 billion of incremental capacity in the next cycle"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：稱商業應變措施可使 2025 獲利指引仍能達成（原話："we will be able still to deliver our profitability guidance in 2025"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：數位飛輪目標：2027 年占集團營收 60%–65%（原話："60% to 65% of our group revenue by 2027"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：Motivair 收購將於數日內完成（原話："we are closing, in the coming days, the acquisition of Motivair"）

### SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20230504.md
- 2023-05-04｜Hilary Maxson｜guidance：CFO 宣布調升 2023 年調整後 EBITDA 同口徑成長目標區間（原話："adjusted EBITDA to between plus 16% and plus 21%"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 稱 2023 年需求持續強勁（原話："persistence of strong demand, supported by underlying trends"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 預期供應鏈情況改善（原話："expect an improvement in the supply chain situation"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 提到消費相關區塊出現放緩（原話："a slowdown observed in consumer-related segments"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 揭露年底在手訂單金額（原話："record backlog of EUR 16.50 billion"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 報告能源管理事業第一季營收與同口徑成長（原話："ended the quarter at EUR 6.5 billion, up by more than 18%"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 揭露 2022 調整後 EBITDA 利潤率水準（原話："ended the year at a record level of 17.6%"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 說明 2022 調整後 EBITDA 利潤率同口徑改善幅度（原話："improve our adjusted EBITDA margin by 40 basis points"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 說明毛利率韌性的來源（原話："thanks to actions on prices to counter inflation"）
- 2023-05-04｜Jean-Pascal Tricoire｜margin：執行長說明營運現金流與自由現金流差距的原因（原話："we built up stock to be able to supply our customers"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露數位飛輪占集團營收比重（原話："digital flywheel represent 53% of group revenues"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露軟體與服務中經常性收入占比及目標（原話："36% of the revenues associated is classified as recurring"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露 AVEVA 年化經常性收入成長（原話："ended the year with 23% growth annualized recurring revenue"）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長說明集團軟體營收規模（原話："software company with revenues of EUR 2.6 billion"）
- 2023-05-04｜Jean-Pascal Tricoire｜competition：董事長說明集團在工業軟體的排名（原話："top 3 of industrial software businesses"）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長談 AI 對產品的影響（原話："A huge impact."）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長說明 AI 工程師招募（原話："several hundreds of recruitment of AI engineers"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 說明槓桿比率偏高及預期（原話："we expect it to normalize over time"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 宣布股利提案（原話："EUR 3.15 per share, up 9% on last year"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 回答庫藏股暫停（原話："we've been on a pause for quite some time"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 指出現行庫藏股計畫規模（原話："EUR 1.5 billion to EUR 2 billion worth of plan"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 說明近年未宣布新的庫藏股計畫（原話："we haven't announced any new share buyback plans"）
- 2023-05-04｜Jean-Pascal Tricoire｜capital_allocation：董事長列出現金配置第一優先（原話："The #1 priority is to preserve a high-quality rating."）
- 2023-05-04｜Peter Herweck｜commitment：新任執行長承諾 2023 年交付（原話："focused on sticking to our commitments and driving growth"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長重申影響力營收承諾（原話："we have committed to generate 80% impact revenue by 2027"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長說明 SBTi 認證的 2030 減碳承諾（原話："by 2030 to reduce our carbon footprint by 25%"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長說明 2050 減碳承諾（原話："by 2050, we are determined to reduce our emissions by 90%"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談美中兩大市場夾在地緣緊張中（原話："we're in the crossfire"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談電子零組件供應壓力（原話："a great deal of pressure on the number of components"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談俄羅斯營運撤出（原話："We managed to extract from Russia."）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明財星 500 大客戶覆蓋（原話："partners of around 40% of Fortune 500 businesses"）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明沃爾瑪要求協助其供應商減碳（原話："Walmart has asked us to work with its suppliers"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長回應 EACOP 專案爭議決定續做（原話："We, therefore, decided to continue with this project."）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長談核能業務定位（原話："we did not work so much in nuclear"）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明節能效益（住宅）（原話："You can save up to 25% of energy."）
- 2023-05-04｜Jean-Pascal Tricoire｜capital_allocation：董事長說明併購與庫藏股之間的取捨（原話："the creation of the future through acquisitions"）

### SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md
- 2023-11-09｜Hilary Maxson｜guidance：2024–2027 有機成長 CAGR 目標 7%–10%（原話："organic growth CAGR of plus 7% to 10%"）
- 2023-11-09｜Hilary Maxson｜guidance：Hilary 說明 7–10% 不是逐年指引，而是整個週期（原話："that's not a guideline for any of the given years"）
- 2023-11-09｜Peter Herweck｜guidance：可觸及市場未來 4 年 CAGR 6%–7%（原話："a 6% to 7% CAGR over the next 4 years"）
- 2023-11-09｜Hilary Maxson｜guidance：調整後 EBITA 率有機 CAGR 約 50 bp（原話："adjusted EBITA margin at a CAGR of around 50 basis points"）
- 2023-11-09｜Hilary Maxson｜margin：分析師問 50bp CAGR 是否=20% 利潤率，Hilary 說明 CAGR 口徑（原話："then it would be 50-50, 50-50"）
- 2023-11-09｜Peter Herweck｜guidance：長期營收與獲利願景：500 億歐元營收（原話："EUR 50 billion revenue, we think,"）
- 2023-11-09｜Peter Herweck｜guidance：長期調整後 EBITA 目標 100 億歐元（2x5）（原話："We need profitability, EUR 10 billion, 2x5 adjusted EBITA."）
- 2023-11-09｜Peter Herweck｜guidance：自由現金流轉換率目標約淨利 100%（原話："100% of net income over the and across the cycle"）
- 2023-11-09｜Hilary Maxson｜guidance：現金流 2024 年 40 億歐元目標維持（原話："the EUR 4 billion ambition by 2024"）
- 2023-11-09｜Hilary Maxson｜guidance：產品商業模式 2024–2027 年成長中高個位數（原話："growth of mid- to high single digit from 2024 to 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：系統業務 2027 前預期雙位數成長（原話："we'll see double-digit growth in this business model"）
- 2023-11-09｜Hilary Maxson｜guidance：系統業務積壓訂單延伸到 2025（原話："backlog in the systems business model now extends into 2025"）
- 2023-11-09｜Hilary Maxson｜guidance：軟體與服務預期雙位數成長（原話："expect double-digit growth in both of those business models"）
- 2023-11-09｜Hilary Maxson｜guidance：數位飛輪占營收 2027 年達 60%–65%（原話："stepping up to 60% to 65% of our total revenues by 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：agnostic 軟體經常性收入 2027 年約 80%（原話："agnostic software to around 80% by 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：法國與歐洲成長預期低於集團其餘部分（原話："grow at a relatively lower pace than the rest"）
- 2023-11-09｜Hilary Maxson｜margin：淨價格（net price）口徑：產品價格加總減原料指數（原話："the sum of all the price that we put on our products"）
- 2023-11-09｜Hilary Maxson｜margin：過去多年淨價格貢獻毛利率約 30bp（原話："around 30 basis points average improvements"）
- 2023-11-09｜Hilary Maxson｜margin：工業生產力 2024–2027 預期為強勁貢獻（原話："a strong contributor for us between '24 and '27"）
- 2023-11-09｜Hilary Maxson｜margin：系統成長快於產品，預期對毛利結構負面但幅度較小（原話："growth in systems to negatively impact our mix"）
- 2023-11-09｜Hilary Maxson｜margin：系統與集團毛利率差距自 2016 年已縮小逾 1/3（原話："this difference has decreased by more than 1/3 since 2016"）
- 2023-11-09｜Hilary Maxson｜margin：系統業務 OpEx 密度較低，EBITA 層級緩衝更強（原話："the systems business is less OpEx-intensive"）
- 2023-11-09｜Hilary Maxson｜margin：SFC／銷售比預期下降（原話："a reduction in our SFC to sales ratio between '24 to '27"）
- 2023-11-09｜Hilary Maxson｜margin：研發占銷售由約 5.7% 提高到 2027 年約 7%（原話："we expect that to step up to around 7% by 2027"）
- 2023-11-09｜Hilary Maxson｜margin：自身永續投資約 4 億歐元至 2030（原話："around EUR 400 million in our own sustainability journey"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：增量資本支出約 20 億歐元（2024–2027）（原話："CapEx around EUR 2 billion to support growth"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：有形資本支出維持占銷售 2%–2.5%（原話："remain in a range of around 2% to 2.5%"）
- 2023-11-09｜Hilary Maxson｜guidance：ROCE 目標 15% 以上（原話："our ROCE towards 15% plus in the next few years"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：庫藏股改為只對沖員工股權計畫（原話："buy back shares to neutralize employee share plans"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：近期無轉型性併購或處分（原話："don't see any transformative transactions in the near term"）
- 2023-11-09｜Peter Herweck｜capital_allocation：CEO：議程上無轉型性併購（原話："no transformational M&A on my current agenda"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：連續 13 年累進股利，列為優先順位（原話："maintained a progressive dividend for the past 13 years"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：槓桿預期從 OSI／AVEVA 少數股權後的高點下降，不給具體數字（原話："decrease versus the level of leverage that we have today"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：若有多餘現金，不排除以特別股息或買回形式返還（原話："not averse to giving that back in some form"）
- 2023-11-09｜Hilary Maxson｜commitment：「Company of 25」為跨週期目標（成長＋EBITA 率）（原話："a sum of our organic growth and adjusted EBITA margin"）
- 2023-11-09｜Peter Herweck｜commitment：CEO 承諾延續性與嚴格執行（原話："what I will promise you a stringent execution"）
- 2023-11-09｜Hilary Maxson｜commitment：2021 資本市場日承諾達標進度：在軌（原話："we're well on track to meet these commitments"）
- 2023-11-09｜Peter Herweck｜guidance：CEO 表示今天不談 2024 財測，之後公布（原話："not the day to talk about the '24 guidance"）
- 2023-11-09｜Peter Herweck｜guidance：CEO：部分市場未來數季偏慢甚至轉負，其他雙位數（原話："certain areas will be a little bit slower"）
- 2023-11-09｜Hilary Maxson｜guidance：7–10% 成長不假設價格是主要驅動（原話："haven't assumed that price would be an enormous driver"）
- 2023-11-09｜Peter Herweck｜risk：OEM 市場疲弱，始於中國，後延及歐洲部分市場（原話："OEM market shows some weaknesses predominantly started"）
- 2023-11-09｜Peter Herweck｜risk：CEO 預期此輪 OEM 週期歷時數季（原話："cycles have traditionally had a certain period"）
- 2023-11-09｜Peter Herweck｜risk：CEO 承認市場有波動（原話："there are some volatilities in the market"）
- 2023-11-09｜Peter Herweck｜risk：AI 熱潮能持續多久無法預測（原話："I don't have the glass ball"）
- 2023-11-09｜Aamir Paul｜risk：美國 IRA 資金流經聯邦到州再到市，大案進度較慢（原話："Now those tend to move a little bit slower."）
- 2023-11-09｜Peter Herweck｜customer：資料中心占集團 19%，稱不爭議第一（原話："19% of the group, undisputed #1 position"）
- 2023-11-09｜Peter Herweck｜customer：資料中心過去數年成長高於市場（原話："it will continue to be a double-digit growth market"）
- 2023-11-09｜Christopher Crosby｜customer：Compass 簽 30 億美元多年期電力中心單元供貨協議（原話："$3 billion multiyear agreement for supply"）
- 2023-11-09｜Christopher Crosby｜customer：Compass 預期含預測維護服務合約毛利高（原話："which we expect to be very high margin for them"）
- 2023-11-09｜Aamir Paul｜customer：Compass 合約為 5 年期，資料中心可見度為史上最高（原話："highest visibility we've ever had on data centers"）
- 2023-11-09｜Peter Herweck｜customer：Compass 為既有客戶，合約是成長（原話："It's not a new customer. We've had them before."）
- 2023-11-09｜Aamir Paul｜customer：美國管線大案增加，案件規模變大（原話："the deal sizes are getting larger"）
- 2023-11-09｜Kathleen Mazzarella｜customer：Graybar 稱 Schneider 為其最大供應商（原話："Graybar's largest supplier"）
- 2023-11-09｜Peter Herweck｜customer：通路夥伴約貢獻 60% 營收（原話："It creates and it turns roughly 60% of our revenue."）
- 2023-11-09｜Nicole Dezen｜customer：Microsoft 與 Schneider 簽訂供應鏈確定性協議（原話："agreement ensuring supply chain certainty"）
- 2023-11-09｜Amit Bhalla｜customer：電網業務占比高個位數（原話："high single-digit exposure for Schneider"）
- 2023-11-09｜Caspar Herzberg｜competition：AVEVA 高層對比整合型廠商：agnostic 擴張更快（原話："we scale better. We scale faster"）
- 2023-11-09｜Peter Herweck｜competition：分析師質疑 PLC 規模偏小，CEO 稱差距不大（原話："Yes, but not substantially."）
- 2023-11-09｜Peter Herweck｜competition：CEO 稱大型同業不太會加入開放自動化（原話："the very large ones, I wouldn't expect them to sign up"）
- 2023-11-09｜Olivier Pascal Blum｜competition：低壓業務規模為第二名 2 倍（原話："2x bigger than the second player in the market"）
- 2023-11-09｜Peter Herweck｜product：軟體定義自動化可能減少 PLC 硬體銷售、增加軟體（原話："we're going to be selling more software"）
- 2023-11-09｜Unknown Executive (Caspar Herzberg)｜product：Connect 平台已有 3 家外部公司承諾上線（原話："have committed to move on to this platform"）
- 2023-11-09｜Peter Herweck｜product：ETAP 為核能領域唯一獲認證軟體（原話："Every nuclear player we are talking to"）
- 2023-11-09｜Olivier Pascal Blum｜product：EcoCare 數位服務定位為下一個大型業務（原話："we love recurring revenues at Schneider"）
- 2023-11-09｜Caspar Herzberg｜product：AVEVA 稱按進度達管理層目標（原話："on track to meet the targets"）
- 2023-11-09｜Caspar Herzberg｜product：訂閱／SaaS 轉型對營收表現有影響，屬計畫內（原話："has an impact on the revenue performance"）
- 2023-11-09｜Caspar Herzberg｜product：AVEVA ARR 成長高於 15%（原話："annualized recurring revenue growth of above 15%"）
- 2023-11-09｜Caspar Herzberg｜product：agnostic 軟體營收約 19 億歐元（原話："just under EUR 2 billion, EUR 1.9 billion"）
- 2023-11-09｜Hilary Maxson｜guidance：AVEVA 訂閱轉型的大額衝擊預期 2026–2027 結束（原話："through the big impacts in terms of revenue"）
- 2023-11-09｜Barbara Frei｜product：馬達管理業務 15 年內成長 3 倍（原話："this business has tripled over the last 15 years"）

### SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO重申2025年調整後EBITDA有機成長區間（原話："organic growth of adjusted EBITDA between 10% and 15%"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO拆解EBITDA成長的營收成長區間（原話："organic revenue growth between 7% and 10%"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO拆解2025年調整後EBITDA margin有機增幅區間（原話："adjusted EBITDA margin between 50 and 80 basis points"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO說離散自動化需求復甦、銷售成長偏重下半年（原話："sales growth weighted towards the second half of the year"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO說軟體與服務預期不變，AVEVA年化經常性收入雙位數成長（原話："annualized recurring revenues at AVEVA"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO談離散自動化市場預期復甦（原話："a recovery in demand in the Discrete automation market"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO報告2024年調整後EBITDA margin創高（原話："record adjusted EBITDA margin of 18.6%"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO報告ROCE 2024年水準與目標（原話："Now at 14.8%, well on track towards our goal of 15%-plus."）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告能源管理2024年營收規模（原話："Energy management achieved EUR 31 billion revenues"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告工業自動化2024年有機衰退（原話："an organic decline of 4%"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告系統業務占比與成長（原話："which represent 31% of sales in 2024 and grew 19% organic"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO說產品業務尚未回到成長（原話："not yet returning to growth overall"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO報告2025Q1能源管理成長（原話："up 10% organic in the first quarter"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告2025Q1工業自動化持平（原話："Industrial Automation was around flat during the quarter"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO談關稅，稱已在採取因應措施（原話："already taking measures to counter the impacts of tariffs"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO談關稅對營業利益率的因應是調價（原話："we would work on the pricing in the regions concerned"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO說明在地化供應鏈目標（原話："90% of our supply chain needs to come from the region"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO說明股價下跌原因之一為美元貶值（原話："a big degradation of the U.S. dollar"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO說資料中心成長預期分歧影響股價（原話："low double digit and super high double digits"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO在Q&A表示對2025財測有信心（原話："We feel very confident in the 2025 guidance, 7% to 10%."）
- 2025-05-07｜CEO Olivier Blum｜commitment：數位化營收占比現況（原話："We reached 57% of digital offering, 57% of our revenue."）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO談數位化中期目標（同篇另有60%–65%的說法）（原話："medium-term target, which is around 70% of digitalization"）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO談2027年數位化營收占比目標（原話："60% to 65% of group revenues by 2027"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜commitment：董事長重申投資人日的自由現金流轉換目標（原話："conversion of free cash flow of 100% on average year-on-year"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜capital_allocation：董事長報告股利與連續增加年數（原話："a dividend of EUR 3.90 per share, an increase of 11%"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜capital_allocation：董事長指出連續第15年增加股利（原話："15th year in a row of an increase of dividend"）
- 2025-05-07｜CFO Hilary Maxson｜capital_allocation：CFO列出資本配置第一優先為信用評等（原話："strong credit grade ratings as the first priority"）
- 2025-05-07｜CFO Hilary Maxson｜capital_allocation：CFO談併購態度（原話："cautiously opportunistic and agile regarding acquisitions"）
- 2025-05-07｜CEO Olivier Blum｜capital_allocation：CEO談遇到合適標的可加速執行併購（原話："if we find the right company at the right price"）
- 2025-05-07｜CEO Olivier Blum｜capital_allocation：CEO說明買Motivair的原因（原話："that's why we bought Motivair"）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO確認7%–10%成長為有機成長（原話："that growth would be organic"）
- 2025-05-07｜CEO Olivier Blum｜competition：CEO說明客戶向NVIDIA推薦施耐德的理由（原話："most advanced portfolio of technologies"）
- 2025-05-07｜CEO Olivier Blum｜customer：CEO以Capgemini為案例，節能成果（原話："They saved 30% in energy consumption"）
- 2025-05-07｜CEO Olivier Blum｜customer：CEO說明Capgemini服務合約帶來經常性收入（原話："Capgemini will be paying us every year"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜product：董事長說明StarCharge合資在歐洲的獨家權（原話："exclusivity in developing these technologies in Europe"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明資料中心占全球用電比重（原話："only 0.4% of the world's electricity consumption"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO回應美國ESG壓力：大型美企仍重視淨零（原話："continue to have a powerful focus on their net 0 targets"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明美國CSR招標規則僅政府合約有變（原話："The only change has been for government contracts"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明美國業務約80%不受影響（原話："About 80% of what we do in the States, nothing has changed"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO談印度–巴基斯坦衝突的可能影響（原話："our ambitions remain untouched"）
- 2025-05-07｜Vice-Chairman Manfred Kindle｜risk：董事會主席說明前CEO的非競業與資遣補償（原話："a non-compete indemnity and also to a severance indemnity"）
- 2025-05-07｜Vice-Chairman Manfred Kindle｜commitment：董事會提議調高CEO總薪酬（原話："an increase in total compensation for the CEO"）
- 2025-05-07｜CEO Olivier Blum｜product：CEO稱工業自動化已見低點（原話："I think we've reached the low point"）
- 2025-05-07｜CEO Olivier Blum｜competition：CEO稱未流失市占（原話："We did not lose any market share"）
- 2025-05-07｜CEO Olivier Blum｜guidance：CEO報告2024營收成長與規模（原話："we attained 8.4% revenue growth, EUR 38 billion"）

### SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md
- 2025-12-11｜CEO Olivier Blum｜guidance：CEO 說下一個週期可達 7%～10% 的持續成長。（原話："a sustained growth of 7% to 10%"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 將 7%～10% CAGR 的差異化成長目標延伸到 2030 年。（原話："differentiated growth target of 7% to 10% CAGR"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 估計可觸及市場到 2030 年年增 6%～7%。（原話："will grow between 6% and 7% between now and 2030"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：純資料中心這塊 2025～2030 年預期年複合成長 12%～14%。（原話："to grow 12% to 14% CAGR between 2025 and 2030"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：資料中心與網路整體預期成長超過 10%。（原話："still greater than 10% growth expected there"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：其他終端市場成長預期：建築與工業 4%～5%，基礎設施 5%～7%。（原話："industry at 4% to 5% and infrastructure at 5% to 7%"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：揭露每百萬瓦資料中心對公司的商機區間，並說明最複雜的 AI 資料中心不預期落在區間高端。（原話："$1.2 million to $3.3 million per megawatt"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：同一段中，CFO 表示 AI 資料中心每百萬瓦金額不預期走到區間頂端。（原話："we wouldn't expect to trend to the top of that range"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：預期中國在這個週期朝中個位數成長。（原話："China to be trending towards mid-single-digit growth"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：依商業模式拆解：產品中高個位數成長（系統與軟體服務另述）。（原話："products to grow mid-single digit to high single digit"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 說明終端市場拆分是用年底訂單簿預測，並說明為何公布訂單而非營收。（原話："best indicator of what the upcoming sales are looking like"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：電網在基礎設施終端市場中占大宗，對集團的曝險約為高個位數百分比。（原話："probably high single digit in terms of exposure with the group"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：建築市場因住宅拖累而延後，現在預期 4%～5% 的終端市場成長。（原話："we now expect that 4% to 5% end market growth"）
- 2025-12-11｜CEO Olivier Blum｜guidance：CEO 描述工業自動化市場 2025 年是逐步復甦的一年。（原話："was a year of step-by-step recovery in the IA market"）
- 2025-12-11｜Aamir Paul (North America)｜guidance：北美銷售團隊稱電力鏈公司目前對資料中心的確定可見度為 12～18 個月。（原話："So we have visibility for 12 to 18 months"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 承諾調整後 EBITA 利潤率在 2026～2030 年有機擴張 250 個基點。（原話："another plus 250 basis points organic expansion"）
- 2025-12-11｜CFO Hilary Maxson｜margin：被問到 250 個基點是否前低後高，CFO 回答不要多解讀、也不是後段集中。（原話："Nothing back-end loaded."）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 說明 250 個基點的時間分布大致可假設為線性。（原話："you could assume somewhat linear over that time frame"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 解釋改用「加 250 基點」而非「每年 50 基點 CAGR」的表述原因。（原話："plus 250 a bit little better than the 50 CAGR"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜margin：工業自動化事業負責人給出利潤率目標：2028 年回到 18%。（原話："the margin ambition is to get back to 18% by 2028"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 主管說隨訂閱轉型拖累淡出，利潤率將朝 30% EBITDA 邁進。（原話："moving towards 30% EBITDA over the coming years"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 給出 AVEVA 調整後 EBITA 利潤率 2028 年約 30% 的口徑。（原話："strong adjusted EBITA margins of around 30% by 2028"）
- 2025-12-11｜CFO Hilary Maxson｜margin：管理層點出毛利率路徑不如 EBITA 利潤率平順，內部要加強毛利率管理。（原話："driving an obsession with gross margin"）
- 2025-12-11｜CFO Hilary Maxson｜margin：工業生產力節省目標：2026 年起這個週期 20～25 億歐元。（原話："industrial productivity of EUR 2 billion to EUR 2.5 billion"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 承認今年的定價相對通膨偏慢。（原話："We've been a bit slow this year in terms of pricing"）
- 2025-12-11｜CFO Hilary Maxson｜margin：未來五年的定價目標：淨定價持平到正向，以完全抵銷關稅與通膨影響。（原話："an ambition of flat to positive net pricing"）
- 2025-12-11｜CFO Hilary Maxson｜risk：CFO 表示未來五年很可能面臨通膨，且關稅更難預測。（原話："some more unpredictability in terms of tariffs"）
- 2025-12-11｜CFO Hilary Maxson｜margin：毛利率層面預期持續受到負面組合影響，主要在調整後 EBITA 層面抵銷。（原話："we expect to continue to have negative gross margin impacts"）
- 2025-12-11｜CFO Hilary Maxson｜margin：系統業務稀釋毛利率，但在調整後 EBITA 利潤率層面已接近中性。（原話："systems are already around neutral to our adjusted EBITA margin"）
- 2025-12-11｜CFO Hilary Maxson｜margin：軟體在調整後 EBITA 層面預期在這個週期轉為加分。（原話："software to become accretive at the adjusted EBITA level"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 經常性收入占比與毛利率口徑。（原話："has reached 85% of this business"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 預期營收與 ARR 成長將趨於收斂。（原話："revenue and ARR growth will start to converge"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜product：AVEVA 揭露客戶流失與留存指標。（原話："low churn of less than 2% and 110% retention rate"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：研發費用占營收比重逐步提高到約 7%。（原話："move our R&D as a percentage of sales to around 7%"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：資本支出約占營收 2.5%，前幾年達到高峰。（原話："invest around 2.5% of our group revenues in CapEx"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：CFO 說明資本支出領先需求 18～24 個月投入。（原話："we're investing now 18 to 24 months in advance of the demand cycle"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：銷售與行政等費用占營收比（不含研發）目標下降 1.5～2 個百分點。（原話："SFC to sales ratio down by 1.5 to 2 points"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：2025 年重組費用約 3 億歐元，並預期到 2027 年有額外重組費用。（原話："restructuring of around EUR 300 million in 2025"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：自由現金流轉換率目標約 100%（占淨利）。（原話："around 100% free cash conversion ratio"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：ROCE 目標上調為 15%～20%。（原話："upgraded our ambition for ROCE growth to between 15% and 20%"）
- 2025-12-11｜CEO Olivier Blum｜commitment：2030 年數位飛輪占營收超過 70%。（原話："More than 70% of our revenue should come from the flywheel"）
- 2025-12-11｜CEO Olivier Blum｜commitment：軟體與服務占集團營收目標 25%。（原話："25% of our group revenue being made of software and services"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：經常性收入占比到 2030 年加倍。（原話："contractual recurring revenues by 2030"）
- 2025-12-11｜CEO Olivier Blum｜commitment：供應鏈在地化目標：每個區域 90% 銷售商品為當地製造或採購。（原話："in every region, 90% of what we sell is made sourced locally"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：自 2026 年第一季起改用新區域口徑報告。（原話："intend to start reporting on in Q1 of 2026"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：未來五年股票回購計畫 25～35 億歐元，並稱會比近年更有系統。（原話："EUR 2.5 billion to EUR 3.5 billion in share buyback"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：信用評等目標明確化為維持 A 級類別。（原話："retain category A credit ratings over this next 5 years"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：股利政策維持累進，已連續 15 年。（原話："paid a progressive dividend now for 15 years in a row"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：首次設定處分目標：到 2030 年處分 10～15 億歐元營收的資產。（原話："EUR 1 billion to EUR 1.5 billion revenue disposal"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 說明處分屬例行修剪，不預期有大案。（原話："Don't expect any big things"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 說所有中期目標均為有機成長，不含併購。（原話："all the ambition that we are giving to you today are organic"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 表示目前不計畫大型收購。（原話："We don't plan any major acquisition at that point of time."）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：CFO 回應若做大型併購 ROCE 目標是否成立：稱 15%～20% 在五年內仍有把握。（原話："we feel comfortable with over the 5-year time frame"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：印度 Lauritz Knudsen 收購已獲印度競爭委員會核准，預計年底前完成。（原話："close the acquisition before the end of this year"）
- 2025-12-11｜Aamir Paul (North America)｜customer：與 Switch 的資料中心整合模組方案，單筆金額 19 億美元。（原話："that particular deal was $1.9 billion"）
- 2025-12-11｜David Howson (Vantage Data Centers)｜customer：Vantage 表示已與公司簽訂長期供應產能協議。（原話："long-term supply capacity agreements with Schneider"）
- 2025-12-11｜Aamir Paul (North America)｜customer：與 Vantage 的業務規模約為過去的十倍。（原話："almost 10x larger than it used to be"）
- 2025-12-11｜CEO Olivier Blum｜customer：CEO 描述與大型客戶的新型承諾式合約：客戶承諾採購量，公司承諾產能。（原話："commit on a certain number of capacity we'll give to them"）
- 2025-12-11｜Noelle Walsh (Microsoft)｜customer：微軟代表稱公司為關鍵且具策略性的供應商。（原話："We view Schneider as a critical and strategic supplier."）
- 2025-12-11｜Unknown Executive｜risk：高管提到大型客戶的建置節奏會調整，去年微軟曾放慢。（原話："as you saw with Microsoft last year, they'll slow things down"）
- 2025-12-11｜Aamir Paul (North America)｜customer：Compass 案例：資料中心連網監控帶來現場事件與資本支出下降。（原話："a 40% reduction in on-site events"）
- 2025-12-11｜Guillaume Texier (Rexel)｜customer：通路夥伴 Rexel 預期定價環境支持價格上漲（為分銷商觀點）。（原話："price appreciation over the next few years"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 承認 2025 年是定價的過渡年。（原話："25 years has been a bit of a year of transition"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 說中國市場通縮，限制了正向定價的能力。（原話："the capacity to deliver positive pricing is very limited"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 說明關稅反覆期間，公司花了數週到數月才決定定價。（原話："a couple of weeks, months to really take stock"）
- 2025-12-11｜Laurent Bataille (Europe)｜risk：歐洲區主管承認歐洲在 AI 與資料中心相關成長上落後。（原話："Europe has probably missed in terms of growth potential"）
- 2025-12-11｜Aamir Paul (North America)｜risk：北美住宅在疫後強勁後目前承壓。（原話："that is more challenged right now"）
- 2025-12-11｜Aamir Paul (North America)｜risk：墨西哥因 USMCA 談判目前偏軟。（原話："Mexico is softer a little bit for us right now"）
- 2025-12-11｜Aamir Paul (North America)｜risk：美國電工人力缺口被點名為資料中心擴張的限制之一。（原話："There are roughly about 600,000 electricians in the U.S."）
- 2025-12-11｜Frederic Godemel｜competition：被問到固態變壓器（SST），資料中心技術長說 2027 年前不預期大規模新技術。（原話："Up to 2027, we don't see at large new technology like SST"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜competition：工業自動化負責人承認 PLC 不是領先位置，策略上刻意轉向虛擬 PLC 與軟體定義自動化。（原話："the areas where we are not the leaders, PLC."）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜competition：工業自動化策略強調選擇性，與競爭者合作推動開放標準。（原話："even with competition to impose standards"）
- 2025-12-11｜CFO Hilary Maxson｜competition：CFO 稱公司是資料中心與網路的市場領導者並打算維持。（原話："we are clearly the market leader, and we intend to remain so"）
- 2025-12-11｜Frederic Godemel｜product：預告明年推出的馬達控制中心新方案，可節省最多 80% 空間。（原話："up to 80% of space saving"）
- 2025-12-11｜Frederic Godemel｜product：軟體定義中壓架構可大幅縮短訂購與設計時間。（原話："accelerate 3x the time to order and design"）
- 2025-12-11｜David Howson (Vantage Data Centers)｜product：Vantage 表示 800 伏特直流技術預計 2028～2030 年才會部署。（原話："until 2028, 2029, 2030"）
- 2025-12-11｜Frederic Godemel｜product：服務業務：公司估計目前服務的裝置基數比例，並預期服務持續雙位數成長。（原話："we serve around 16% of our asset"）
- 2025-12-11｜Frederic Godemel｜product：服務業務下個週期預期維持雙位數成長。（原話："to keep growing double digit this business"）
- 2025-12-11｜Rich Whitmore (Motivair)｜product：Motivair 於今年 3 月被收購，目前正推動全球產能工業化。（原話："we were acquired in March this year"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜product：EcoStruxure Automation Expert 已部署站點數。（原話："Today, we have 550 sites deployed with EAE"）
- 2025-12-11｜CEO Olivier Blum｜commitment：組織效率：CEO 說明不會有大規模重組，但會逐步減少領導層人數。（原話："we are not going through massive restructuring"）
- 2025-12-11｜CEO Olivier Blum｜commitment：CEO 說將逐步精簡領導層。（原話："we are going to reduce step-by-step the number of leaders that we have"）
- 2025-12-11｜CEO Olivier Blum｜commitment：被問到薪酬與 KPI 是否調整，CEO 說薪酬制度不變。（原話："nothing that we are changing on compensation"）

### SU.PA_2026_20260730.md
- 2026-07-30｜Olivier Blum (CEO)｜guidance：全年營收有機成長財測上調（原話："from 7% to 10% to 10% to 13% organic"）
- 2026-07-30｜Olivier Blum (CEO)｜guidance：全年調整後 EBITA 利潤率改善幅度財測上調（原話："from 50 to 80 bps to 70 to 100 bps by the end of the year"）
- 2026-07-30｜Olivier Blum (CEO)｜guidance：調整後 EBITA 有機改善的區間說法（原話："between 14% and 19% of organic improvement of adjusted EBITA"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：CFO 預期全年匯率對營收的影響（原話："minus EUR 450 million to minus EUR 500 million on revenues"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：CFO 預期全年現金轉換率（原話："cash conversion ratio to be around 100% for full year"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：重組費用預期今年見頂（原話："restructuring charges of around EUR 450 million this year"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：上半年毛利率數字（原話："gross margin of 42.5%, up 10 bps"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：Q2 價格對產品業務成長的貢獻口徑（原話："represent approximately 4 points of product growth in Q2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：毛利率橋中含關稅退款一次性項目（原話："around EUR 100 million coming from tariff refunds in Q2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：CFO 提醒生產力下半年基期較高（原話："more than 70% of our full year 2025 productivity in H2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：系統業務成長使毛利率結構轉差（原話："Mix was negative in gross margin as expected"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：支援職能費用占銷售比改善幅度（原話："SFC to sales ratio improving by 1.1 points"）
- 2026-07-30｜Olivier Blum (CEO)｜margin：管理層說明下半年若價格貢獻重現可抵銷原料與關稅衝擊（原話："if we are able to repeat that in H2"）
- 2026-07-30｜Nathan Fast (CFO)｜commitment：工業自動化利潤率回復目標重申（原話："on track to our 18% by 2028"）
- 2026-07-30｜Nathan Fast (CFO)｜commitment：對長期生產力節奏的回答：不會線性延續（原話："the same linear over a 5-year period? Probably not"）
- 2026-07-30｜Olivier Blum (CEO)｜commitment：今年不增加人力、嚴控 SG&A（原話："not increasing our headcount this year"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：股利政策連續年數（原話："progressive since 16 years"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：上半年已執行的庫藏股金額（原話："already EUR 250 million that have been repurchase"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：回答 M&A 問題：成長主要來自內生（原話："most of it will come organically"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：CEO 描述 Cognite 收購的定位（原話："it's the brain of the next cycle of Schneider"）
- 2026-07-30｜Olivier Blum (CEO)｜product：資料中心新架構（固態變壓器電力中心）研發進度（原話："power center with new SST solution that we have developed"）
- 2026-07-30｜Nathan Fast (CFO)｜product：系統業務 Q2 成長數字與驅動（原話："sales of 28% growth driven by data center"）
- 2026-07-30｜Olivier Blum (CEO)｜product：與 Foxconn 合作擴充北美預製化產能，並提及產業放緩情境（原話："mitigate potential not, I would say, decline, but slowdown"）
- 2026-07-30｜Olivier Blum (CEO)｜competition：CEO 回應競爭與資料中心整合方案執行風險：已增加安全庫存（原話："we increased our safety stock in all those components"）
- 2026-07-30｜Olivier Blum (CEO)｜risk：資料中心市場可能受零組件與記憶體限制（原話："constrained sometimes by component, by memory"）
- 2026-07-30｜Nathan Fast (CFO)｜risk：中東情勢被列為下半年挑戰（原話："we see this as a challenge in H2 2026"）
- 2026-07-30｜Olivier Blum (CEO)｜risk：CEO 對資料中心執行的保留語氣（原話："the world is so unpredictable that you can have always issue"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：資料中心客戶基礎與預測方式（原話："work with 200 customers in the world"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：客戶選擇標準：重視長期合作與經濟條件（原話："customers that wants to build a long-term partnership"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：中國需求結構：建築與住宅仍慢，並已降低曝險（原話："we reduced drastically our exposure"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：CEO 描述需求來源的敘事：由資料中心擴及所有終端市場（原話："we see all segments contributing"）

### SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md
- 2026-10-05｜Nathan Fast (CFO)｜guidance：CFO 給出成本綜效 2.5 億歐元、3 年內實現（原話："EUR 250 million of cost synergies to be generated"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：一次性整合成本約 2.5 億歐元（原話："EUR 250 million of onetime implementation costs"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：營收綜效 8 億歐元，由三個槓桿構成（原話："EUR 800 million of revenue synergies clearly defined"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：營收綜效時程：交割後不久開始、中期線性實現（原話："delivered linear over the midterm"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：交易價值：PTC 100% 現金收購、企業價值約 210 億歐元（原話："implying approximately EUR 21 billion of enterprise value"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：估值倍數口徑：含完整綜效約 13 倍調整後 EBITDA（原話："valued at approximately 13x adjusted EBITDA"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：2027 調整後 EBITA 倍數隨綜效下降的分段口徑（原話："21x before synergies to 17x with cost synergies"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：PTC 綜效前毛利率與調整後 EBITA 利潤率（原話："85% gross margin and 40% adjusted EBITA margin"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：PTC 中期有機 ARR 與營收 CAGR 約 10%（原話："10% organic ARR and revenue CAGR in the medium term"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：PTC 現金轉換率高於 100%（原話："PTC cash conversion is above 100%"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：調整後 EPS（PPA 前）第一年增厚：未計完整綜效為低個位數（原話："immediately accretive to adjusted EPS before PPA in year 1"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：交易 ROCE 第 5 年超過 WACC（原話："the transaction ROCE is expected to exceed the WACC"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：集團 ROCE 於交割後 1 年內回到 15%–20%（原話："ROCE to be back in the 15% to 20% at a Schneider level"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：預計交割時點（CFO 口徑）（原話："We are expecting closing by Q3 2027."）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：股權融資規模 50–60 億歐元（原話："EUR 5 billion to EUR 6 billion of equity"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：新增優先債規模 160–170 億歐元（原話："EUR 16 billion to EUR 17 billion of senior debt"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：承諾維持 A 級信用評等（原話："a commitment to our category A credit rating"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：2030 庫藏股總額維持，但 2027、2028 暫停（原話："with some pause over 2027 and 2028"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：CFO 重申利潤率改善承諾（原話："We remain committed on the margin improvement"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：CFO 稱相對 CMD 承諾無改變，並自述併購紀律（原話："nothing changes versus those commitments from CMD"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：CFO 列舉併購篩選條件（原話："nothing changes versus those commitments"）
- 2026-10-05｜Olivier Blum (CEO)｜product：CEO 稱收購使可觸及的工業軟體市場放大 3 倍（原話："we multiply by 3, the accessible market"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：合併後軟體與服務占集團營收口徑（以 2025 為基準）（原話："representing 24% of our group revenues"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：合併軟體組合經常性收入占比（原話："89% of that portfolio being recurring"）
- 2026-10-05｜Olivier Blum (CEO)｜product：CEO 稱 Cognite 將成為集團能源管理的 AI 基礎（原話："Cognite will be definitely the AI foundation"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：CEO 以開放、互通為差異化主軸（原話："we are open by design"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：CEO 回應整合式硬軟體廠商 vs 純軟體廠商之爭，指客戶看待 Schneider 的方式已改變（原話："they don't perceive Schneider Electric today like it was"）
- 2026-10-05｜Olivier Blum (CEO)｜customer：CEO 描述客戶採購趨向整合、AI 化方案（原話："buying integrated, connected and AI-enabled solutions"）
- 2026-10-05｜Nathan Fast (CFO)｜product：CFO 談軟體定價：席位制與 flex credit 並存、保留兩種模式（原話："the seat and flex credit models are probably complementary"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：CFO 回應收購時點／估值：看長期內在價值而非當下股價（原話："their trading value at an arbitrary point in time"）
- 2026-10-05｜Olivier Blum (CEO)｜risk：整合風險：CEO 稱人才留任是首要事項（原話："retention of people is an absolute priority"）
- 2026-10-05｜Olivier Blum (CEO)｜risk：CFIUS 等監管審批：CEO 稱不預期重大問題（原話："we don't expect any major issue"）
- 2026-10-05｜Nathan Fast (CFO)｜risk：被問及競標／第三方介入，CFO 表示不就假設性情境表態（原話："not going to speculate on what type of interlopers"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：股權與債務置換時點尚未決定（原話："we haven't decided exact timing of those yet"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：敘事變化：CEO 稱工業自動化不是獨立事業，須與其他產品組合一起看（原話："Industrial Automation is not a stand-alone business"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：CEO 提到工業自動化單獨報告時仍須展現獲利反轉（原話："has also to demonstrate a turnaround in profitability"）
- 2026-10-05｜Olivier Blum (CEO)｜commitment：CEO 說明交割前兩家公司獨立營運、交割後單一軟體載體單一領導（原話："continue to operate in post-closing with one software"）

### SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md
- 2026-10-16｜Olivier Blum｜guidance：CEO 宣布 2026 全年目標第二次上調（營收與調整後 EBITA margin）（原話："we are upgrading for the second time in 2026"）
- 2026-10-16｜Olivier Blum｜guidance：全年有機營收成長目標 12%–14%（原話："between 12% and 14% organically"）
- 2026-10-16｜Olivier Blum｜margin：全年調整後 EBITA margin 隱含約 19.7%–19.9%（有機 +100 至 +120bps）（原話："adjusted EBITA margin of around 19.7% to 19.9%"）
- 2026-10-16｜Nathan Fast｜margin：匯率對全年 margin 影響預期可忽略（原話："negligible impact in adjusted EBITA margin for the full year"）
- 2026-10-16｜Nathan Fast｜margin：管理層預期 2026 年以價格行動以價值計抵銷原物料與關稅逆風（原話："expect to offset in value for 2026 the headwinds"）
- 2026-10-16｜Nathan Fast｜margin：Q3 產品價格貢獻金額與整個上半年相當（原話："product pricing in Q3 around the same level in value"）
- 2026-10-16｜Nathan Fast｜guidance：全年區間上調同時收窄，說明為信心與能見度提高（原話："we have also narrowed the range"）
- 2026-10-16｜Nathan Fast｜guidance：CFO 回應 Q4 隱含放緩：基期為 2025 年最強季度之一（原話："the baseline was the strongest quarter in 2025"）
- 2026-10-16｜Nathan Fast｜product：資料中心需求再一季三位數成長（原話："another quarter of triple digit demand growth in Q3"）
- 2026-10-16｜Nathan Fast｜product：預製化（prefab）占比不揭露，僅稱成長極強（原話："we don't give the exact split of the prefab business"）
- 2026-10-16｜Nathan Fast｜product：AVEVA ARR 與 Q3 有機成長均約 10%（原話："AVEVA's ARR and Q3 organic sales growth both at around 10%"）
- 2026-10-16｜Nathan Fast｜customer：Q4 預期趨勢中，成長國家新增中國（原為美國、印度）（原話："we add China alongside U.S. and India"）
- 2026-10-16｜Olivier Blum｜customer：CEO 稱與客戶討論後，中國成長水準至少可延續至 2027（原話："this level of growth could continue at least across '27"）
- 2026-10-16｜Olivier Blum｜customer：年初對中國需求是否短期現象較為保守（敘事與當時不同）（原話："we were a bit more cautious in our answer"）
- 2026-10-16｜Olivier Blum｜customer：CEO 說明客戶選擇上高度挑剔（技術共同設計、財務能力）（原話："we are extremely careful to select those company"）
- 2026-10-16｜Nathan Fast｜customer：去年底資料中心與網路占營收 30%，今年預期集中度上升（原話："was 30% on data center and networks"）
- 2026-10-16｜Olivier Blum｜competition：中國通路優勢：最大夥伴網絡（原話："we are the largest network of partner in the country"）
- 2026-10-16｜Nathan Fast｜competition：800V 等技術轉向目前客戶端尚未提出疑問（原話："we have not had a question on 800 volt"）
- 2026-10-16｜Nathan Fast｜capital_allocation：持續於區域據點擴充產能（含液冷，與 Foxconn 合作）（原話："capacity investments across our regional hubs"）
- 2026-10-16｜Nathan Fast｜risk：住宅端貢獻不及其他板塊（原話："residential has not matched the level of the other segments"）
- 2026-10-16｜Nathan Fast｜risk：工業自動化 Process 與 Hybrid 成長仍疲弱（原話："Sales growth in Process and Hybrid remains subdued overall"）
- 2026-10-16｜Nathan Fast｜risk：CFO 指出下一波投入成本（半導體、記憶體、銅）上漲（原話："Now we see the next wave coming"）
- 2026-10-16｜Nathan Fast｜risk：建築市場：高利率目前未見對需求的影響（原話："We have not seen any impact from higher interest rates."）
- 2026-10-16｜Nathan Fast｜commitment：若 2027 有通膨壓力，將再執行定價（原話："we'll be flexing those muscles from an execution perspective"）

### 問答異常語氣（迴避／改口／保留）
- SU.PA_2024_Earnings_Call_20250220.md｜問：James Moore (Redburn)：資料中心各細分（含超大規模雲端）訂單成長幅度與未來 3–5 年展望｜答法：CEO 表示不提供具體數字（'We don't communicate any specific number moving forward'），CFO 給占比拆解但稱難以回推訂單成長率，未確認分析師推算的 70–75% 成長
- SU.PA_2024_Earnings_Call_20250220.md｜問：Andre Kukhnin (UBS)：中壓業務占比、急單定價是否已享受、SF6-free 帶來的增量｜答法：CEO 稱不公布占比，轉談 AirSeT 產品更新；未回答急單定價問題與 2025 SF6-free 貢獻；CFO 稱 'you said it all'
- SU.PA_2024_Earnings_Call_20250220.md｜問：Alexander Virgo (BofA)：Systems 定價約 15% 以上、2025 毛利率緩和幅度是否如此｜答法：CEO 先談產品組合與在地定價能力，CFO 稱無特別事項，只說 Systems 定價預期正常化，未給幅度數字
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：UBS：未來 12 個月成長與利潤率如何取捨？｜答法：CEO 未直接回答取捨，表示今天不談 2024 財測，改談各市場分化、部分領域可能轉負
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Berenberg：激勵薪酬是否會對齊新成長與利潤率目標？｜答法：CEO 稱尚未想過，長期激勵已定，只說各年 KPI 權重會視情況調整
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：BNP Paribas Exane：多餘資本將返還多少、理想槓桿？｜答法：CEO 先轉給 CFO；CFO 明說不給具體槓桿數字，只說預期自高點下降，返還形式為特別股息或買回
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Morgan Stanley：PLC 規模偏小是投資組合弱點，如何強化？｜答法：CEO 未提補強計畫，改談製程／混合市場強勢，並說 PLC 只占業務約幾個百分點、刻意避開汽車
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Citi：成長是否需要更多政府方案？｜答法：CEO 不直接回答是否需要，改談現有法規、能源成本與高端市場聚焦
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Citi（Daniela Costa）：AVEVA 轉型順風使利潤率路徑是否前高後低？｜答法：CFO 未確認前高後低，表示時間點無法精確預知，說軟體貢獻偏後段、系統業務同時回升
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：SocGen：SFC 比率是否可再降 100–150bp？｜答法：CFO 回答系統毛利差距，但未回應 SFC 具體降幅
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Bernstein：2027 年軟體與服務占比會到多少？｜答法：CFO 表示這次未提供數位飛輪各部分細項，只給成長方向，不給 2027 占比數字
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問Peter Herweck離職補償，以及下任CEO若自願離職是否也有同樣補償政策｜答法：董事長答該合約已經股東大會表決、依合約執行，未直接回答下任CEO自願離職是否適用
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問Notre-Dame專案花費多少百萬歐元｜答法：CEO答數字大概未公開，改談捐贈內容包含設備與工時，未給金額
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問風力發電機與住家的最小距離政策｜答法：董事長答公司不製造風機、無法回答，改談荷蘭風車
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：UBS 分析師：工業終端市場目標被調低、大盤成長目標卻維持，是什麼讓你們對更長期可見度有信心？｜答法：CEO 以電氣化／自動化／數位化趨同、全生命週期與地理擴張作答，未回答工業目標為何調低；CFO 補稱是用內部經濟模型估算，並說資料中心才有跟客戶談較長週期，工業『may happen in this cycle or a bit beyond』難預測。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：Schneider 很少見不當價格領先者，這是單一區域、事業部還是系統性問題？｜答法：CEO 未指認區域或事業部，改談中國通縮、關稅反覆造成決策延遲、服務過去以成長優先；未給定價落差的數字，並承諾回到定價紀律。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：Gael：若 AVEVA 回到 30% 利潤率，其餘工業自動化 18% 目標是否保守（隱含不到 15%）？｜答法：CFO 未回應推算，也未給任何額外數字，只重申 2028 年 18% 並說『Let us get started』『不是旅程終點』。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：同業都在布局固態變壓器（SST），你們是自建、合作還是收購？｜答法：CEO 轉交資料中心技術長；技術長未回答自建／合作／收購，只說 800V 直流下功能區塊仍在、2027 年前不預期大規模新技術，並把細節推給下午的展示攤位。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：重組費用上升、過去人員增幅高於同業，是否人招太多？｜答法：CEO 以『疫後週期檢討效率』作答，未回答是否多聘人，也未給人數或節省金額，只說不會有重大新聞級的重組、領導層逐步精簡。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：Citi 分析師：若做大型併購，ROCE 目標是否仍成立？｜答法：CEO 重申有機優先、目前不計畫大型收購；CFO 自己承認『pretty much all acquisitions cause a small … negative impact on ROCE』，但仍稱 15%～20% 有把握，未說明大型併購時的影響幅度。
- SU.PA_2026_20260730.md｜問：Phil Buller (JPMorgan)：毛利率與 EBITA 利潤率優於預期，但財測隱含下半年利潤率進展較低，如何調和？｜答法：CEO 說上半年「a bit in advance versus what was the initial plan」；CFO 接著說上半年「primarily in line with what we had guided」，兩人說法略有差異，且未直接回應下半年隱含利潤率進展為何較低，只提到關稅退款與多種情境
- SU.PA_2026_20260730.md｜問：James Moore (Redburn)：今年高訂單水準明年能否再成長，還是會正常化？｜答法：CEO 未給訂單或成長數字，改談公司自身使用 AI、token 成本與 Schneider 預測方式，結論為「so far, we believe it's manageable」
- SU.PA_2026_20260730.md｜問：Daniela Costa (Goldman)：Cognite 的成長與利潤率輪廓，以及是否加速 M&A｜答法：CEO 自述「I'm afraid I'm going to be a bit boring and repeating」，未給 Cognite 的成長或利潤率數字，只講策略定位
- SU.PA_2026_20260730.md｜問：Jonathan Mounsey (BNP)：IA 營收成長強但利潤率僅 +30bps，何時改善？｜答法：CEO 與 CFO 重申計畫在軌，說明需要「a couple of months, maybe 2 years」，CFO 稱「we don't give you the details」，未提供拆解數字
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Mackie：對 PTC 客戶基礎的反向綜效（dis-synergies）與競爭反應如何評估？｜答法：CEO 談開放互通與客戶採購趨勢，未直接量化或回答 dis-synergies；交割風險部分 CFO 稱不就第三方介入作假設性推測。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Buller：自上次 CMD 後策略改變了什麼？AI 顛覆風險是否升高？何時再開 CMD？｜答法：CEO 改談以終端市場而非事業群看組合，未直接回答 AI 顛覆風險是否升高，也未回答新 CMD 時點；CFO 補充承諾不變。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Moore：8 億歐元營收綜效按四個領域的拆分、各年度節奏、PTC 自身 vs Schneider 自動化各占多少？｜答法：CFO 明說不給拆分（I'm not going to dimension exactly），只稱雙向、交割後不久開始、中期線性。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Moore：ROCE 計算所用 WACC 是多少？｜答法：CFO 回答 ROCE 15–20% 與 5 年內超過 WACC，但未給出 WACC 數字。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Yates：股權募集時點？是否等監管核准後才募？｜答法：CFO 稱時點尚未決定，僅說會相當快降低融資風險。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Kukhnin：兩宗大型併購（Cognite、PTC）同時進行，內部如何管理？｜答法：CEO 稱交割時點「probably Q2 next year」，與 CFO 簡報中「closing by Q3 2027」口徑不同，未在 Q&A 中說明差異。
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Ben Heelan (BofA)：2027 是否還會有漲價以抵銷成本？｜答法：明說不給 2027 指引，改談年內三輪漲價與定價紀律，未回答 2027 漲價幅度
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Max Yates (Morgan Stanley)：資料中心訂單在超大型雲端、neocloud、其他的拆分｜答法：兩度表明不揭露分類拆分，僅稱曝險「應與大盤相當」並稱選擇性高
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Delphine Brault (Oddo)：新指引隱含 Q4 放緩，原因為何？｜答法：提及多重情境與高基期，未給 Q4 具體數字或確認是否保守

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 1 | 3 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 2 | 2 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SU.PA","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Schneider Electric S.E."},"oneliner":"資料中心與電氣化訂單創高、全年指引兩度上修，但約 210 億歐元的 PTC 併購把資本報酬與融資風險放進論點；現價約 22 倍本年度獲利，合理但不算便宜。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是資料中心、建築、工業與基礎設施業主的電力配電與自動化支出，錢卡在低壓規格、系統整合和經銷通路這幾個節點。","reasoning":"2026 年第三季營收 114.6 億歐元，有機成長 16.9％；其中能源管理 96.2 億歐元，有機 +18.8％，推算工業自動化約 18.4 億歐元。第三季只公布營收，沒有單季毛利率與利益率，最新可用是 2026 上半年：毛利率 42.5％、調整後 EBITA 利潤率 19.3％。2025 年能源管理利潤率 21.8％，工業自動化 14.2％，獲利重心在能源管理。經銷商約占總銷售 50％、型錄產品 70％，這是低壓業務的收費節點；資料中心則靠系統與預製方案，和客戶共同設計後凍結規格。單點依賴：資料中心與網路 2025 年底占營收 30％，CFO 說今年集中度上升，而超大型雲端與新興雲端的訂單拆分公司兩度拒絕揭露，前 1 至 2 大客戶是否超過 40％ 事實表未涵蓋。","fact_refs":["f_kpi0_revenue_q3","f_kpi1_revenue_h1","f_kpi2_adjusted_ebita_non_gaap","f_kpi4_net_income","f_kpi5_2026_q3"],"verdict_values":{"revenue_quality":"中上。2025 年數位飛輪占營收 62％，軟體與服務接近 20％，獨立軟體經常性收入占 79％；但成長最快的系統業務毛利率低於集團，拉低組合。","unit_econ_note":"每百萬瓦資料中心對公司的商機為 120 萬至 330 萬美元，CFO 說最複雜的 AI 資料中心不會走到區間高端；單一客戶毛利與訂單拆分公司不揭露。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"利潤率穩定上升、自由現金流約等於淨利，但資料中心占比上升使循環性增加。"},"industry":{"clock_phase":"II","sd_verdict_source":"供需判斷：電氣化與電網屬結構性持久，資料中心三位數需求成長屬週期高點讀數；公司每季滾動檢視三年產能並與 Foxconn 合作，供給在 18 至 24 個月內可擴張，供給可逆性中等。集團仍在擴張期，住宅與 Process、Hybrid 尚未同步，未到全面過熱。","bargaining":{"up":"銅、銀、半導體與記憶體成本上行，CFO 2026-10-16 說下一波投入成本正在來；公司以多區域採購與提高安全庫存因應。","down":"經銷通路分散，對公司議價力有限；超大型客戶維持多供應商，議價力較強，但以共同設計與產能承諾換取供貨確定性。","geo":"目標每個區域 90％ 銷售在當地製造或採購；中國是第二大市場，北美約占營收 40％。"},"profit_pool_dir":"利潤池往資料中心與系統移動，系統在毛利層稀釋、在 EBITA 層約中性；軟體要到這個週期才轉為加分。各環節營業利益池五年占比事實表未涵蓋。","tam_table":[{"item":"可觸及市場 2025～2030 年增","value":"6％～7％（CFO，2025-12-11）"},{"item":"純資料中心 2025～2030 年複合成長","value":"12％～14％（CFO，2025-12-11）"},{"item":"資料中心與網路整體","value":"超過 10％（CFO，2025-12-11）"},{"item":"建築與工業","value":"4％～5％（CFO，2025-12-11）"},{"item":"基礎設施","value":"5％～7％（CFO，2025-12-11）"},{"item":"800V 直流影響的需求比重","value":"到 2030 年 15％～25％（CEO，2026-02-26）"},{"item":"滲透率與營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平（→）：規模與通路仍穩，資料中心份額與市場同步，定價權剛從 2025 年的落後開始修復。","reasoning":"機制是裝機基礎與規格權、全球經銷通路，再加上和超大型客戶共同設計後凍結規格的轉換成本。執行力給 8 分：2026 年兩度上修指引，第三季有機成長高於共識 3.1 個百分點，在手訂單創高。定價權給 7 分：2025 年毛利率有機年減 40 個基點，CFO 承認定價偏慢；2026 上半年毛利率年增 10 個基點，但含約 1 億歐元關稅退款，約當 47 個基點，扣掉後約年減 37 個基點；第三季產品定價金額約等於整個上半年，是修復的第一個乾淨訊號。對最強同業的 ROIC spread 取不到，改看份額：Dell'Oro 1Q 2025 顯示與 Vertiv 差距約 0.1 個百分點，Bernstein 認為銷售與訂單與市場同步。同業利潤率的期間與 Schneider 不同（同業為 2026 TTM，Schneider 只有 2025 年度），只能看方向。產業態勢裁定雙向拉鋸：資料中心與電氣化讓結構轉好，固態變壓器與專業廠商在同一塊市場施壓。","fact_refs":["f_peer_etn_gross_margin_pct","f_peer_etn_operating_margin_pct","f_peer_etn_fcf_margin_pct","f_peer_abbn_sw_gross_margin_pct","f_peer_abbn_sw_operating_margin_pct","f_peer_abbn_sw_fcf_margin_pct","f_peer_lr_pa_gross_margin_pct","f_peer_lr_pa_operating_margin_pct","f_peer_lr_pa_fcf_margin_pct","f_peer_sie_de_gross_margin_pct","f_peer_sie_de_operating_margin_pct","f_peer_sie_de_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"裝機基礎與規格權（低壓規模在 2023 年為第二名 2 倍）、全球經銷通路、與超大型客戶共同設計後凍結規格的轉換成本；AVEVA 流失率低於 2％、留存 110％，加深軟體黏著。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"份額與市場同步，看不到擴大也看不到流失；毛利率扣除關稅退款後尚未轉正，第三季定價轉強但還沒有反映在可驗證的毛利率上。","competitor_notes":[{"name":"ETN","strategy_note":"毛利率 35.05％ 低於 Schneider 2025 年的 42.08％，營業利益率 17.32％ 卻接近，費用效率較好；期間不同，只看方向。"},{"name":"ABBN.SW","strategy_note":"毛利率 40.12％、營業利益率 17.6％，自由現金流利潤率 13.29％ 高於 Schneider 2025 年的 11.43％，現金轉換較佳。"},{"name":"LR.PA","strategy_note":"毛利率 49.66％、營業利益率 19.11％，是低壓通路定價權的上限參考；Schneider 的系統與自動化拉低整體利潤。"},{"name":"SIE.DE","strategy_note":"營業利益率 12.98％、研發密度 8.31％，自動化與軟體投入最重；Schneider 買 PTC 後，兩家在工業軟體的正面競爭會增加，此為判斷。"},{"name":"Vertiv","strategy_note":"Dell'Oro 1Q 2025 與 Schneider 的資料中心實體基礎設施份額只差約 0.1 個百分點，Bernstein 估三年銷售成長相當；財務數字事實表未涵蓋。"}],"spread_notes":null,"peer_na_reason":"Schneider 同期間 TTM 利潤率在事實表為空，同業 ROIC 也未涵蓋，無法計算 ROIC spread，改用份額方向判斷。","threats":[{"level":"🔴","text":"800V 直流與固態變壓器可能跳過 Schneider 現行 sidecar 過渡方案；公司預計 2028 年才備妥完整架構，CEO 估 2030 年影響 15％～25％ 需求。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"專業廠商在資料中心份額幾乎並列，大客戶維持多供應商，Schneider 的份額只與市場同步。","p":35,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#0"]},{"level":"🟡","text":"AI 代理可能繞過軟體介面層，併入 PTC 後軟體與服務約占營收 24％，曝險上升；產品附著在工業資料與關鍵基礎設施上，判斷強化多於替代，分界年暫看 2028 年，淨增量公司未揭露。","p":25,"evidence_refs":[]},{"level":"🟡","text":"法國轉售價格案罰款 2.07 億歐元，涉及 Rexel、Sonepar 兩大經銷商，顯示通路定價受監管檢視；上訴結果未見。","p":20,"evidence_refs":["regulatory_antitrust#0"]},{"level":"🟡","text":"客戶集中度上升但看不到全貌：資料中心與網路 2025 年底占營收 30％，CFO 說今年再上升，超大型與新興雲端的訂單拆分公司兩度拒絕揭露，前 1 至 2 大客戶是否超過 40％ 事實表未涵蓋。大客戶一旦調節奏，會發生在併購後負債最高、公司又承諾維持 A 類信評的時候；機率沿用在手訂單年減的判斷，沒有客戶資料可校準。","p":20,"evidence_refs":["end_markets#0","customer_second_source#0","customer_concentration_credit#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"配電與冷卻是資料中心和電氣化的必要投入，延後的代價高；但急迫性不等於持久性，資料中心三位數需求成長屬高點讀數，大客戶也曾放慢節奏。"},{"item":"決策層級","level":"🟡","text":"型錄產品由電工與經銷商指定，換品牌要重新認證與訓練，黏著高；資料中心在設計凍結後 18 至 24 個月鎖定，但下一代專案可換供應商，Digital Realty 維持多供應商。"},{"item":"價值鏈分配","level":"🟡","text":"系統占比上升拉低毛利，超大型客戶集中議價；電力架構由 NVIDIA 的產品節奏決定，關鍵互補品集中在單一廠商，公司能分到多少尚待驗證。"},{"item":"社會容忍度","level":"🟡","text":"企業對企業的設備沒有消費者漲價爭議，但法國轉售價格案顯示通路定價有監管上限，上訴結果未見。"}],"roiic":"本業層代理值 17.5％（公司 ROCE 目標 15％～20％ 中點），是平均報酬而非實測增量報酬，增量投入資本事實表未涵蓋；公司只揭露目前 ROCE 超過 15％，17.5％ 可能已含部分利潤率改善，和利潤率缺口有重疊，只能當粗估。併購層另算：PTC 以 2027 年調整後 EBITA 計，未計綜效稅後報酬約 3.6％，計成本綜效約 4.5％，稅率取 24％；Cognite、Shelly 的報酬事實表未涵蓋，暫用同一報酬。約 250 億歐元乘 3.6％～4.5％，得稅後利益約 9.0 億至 11.3 億歐元；年 NOPAT 約 73.5 億歐元（250 億除以 1.7 再除以 2），所以獲利一次墊高 12.2％～15.3％，攤到五年每年約 2.3～2.9 個百分點，扣掉增資稀釋約 4％（每年約 0.8）後約 1.5～2.1。融資利率事實表未涵蓋，這是扣利息前的數字。本業層 8.75％ 加併購層得 10.3％～10.9％，ROCE 取 20％ 時最高約 12.1％，都低於 Base 的 12.15％，所以維持超過上界的判定。反向風險：3.6％～4.5％ 是 2027 年的報酬，CFO 說第五年 ROCE 才超過 WACC，WACC 未揭露，終端年報酬若明顯升高，併購層會高於上述數字，這部分無法複算。","reinvest_rate":"本業層代理值 50％：2025 年每股股息 4.20 歐元對調整後 EPS 約 8.45 歐元的留存比率。定義式所需的折舊、營運資金與收購淨額事實表未涵蓋，算不出實際值。這個代理值的偏誤是雙向的：併購面，2026 至 2027 年收購合計約 250 億歐元，約為兩年 NOPAT 的 1.7 倍，實際再投資率遠高於 50％，但報酬只有 3.6％～4.5％，已改在增量報酬欄單獨計算；本業面，2025 年自由現金流約為淨利 1.10 倍，暗示本業淨再投資可能遠低於 50％。因此 8.75％ 只是本業層的粗略讀數，不是含併購的上界。","endo_ceiling":8.75,"formula_note":"內生上界＝17.5％×50％＝8.75％，ROCE 用 15％～20％ 時區間為 7.5％～10％。ROIC 約等於稅後利潤率 14.2％（2025 年調整後 EBITA 約 18.7％ 乘 76％）乘周轉率約 1.05 倍，周轉率由公司揭露 ROCE 超過 15％ 反推，投入資本口徑事實表未涵蓋。"}}}},"q3_growth":{"verdict":"五年後仍有跑道（🟢），靠電氣化與裝機服務延伸，但資料中心這段高速成長不能外推。","reasoning":"成長以量為主，第三季有機 16.9％ 主要來自資料中心系統，價格在第二季約貢獻產品成長 4 個百分點，併購是附加，回購不是來源。共識只有兩年：FY2026E 10.37 到 FY2027E 12.59，年增 21.4％，同期共識營收年增約 11.4％。基期口徑不同：財報 2025 年稀釋 EPS 7.33，換算到 FY2027E 年化 31.1％；用調整後約 8.45 起算則為 22.1％，第三年共識與 EPS 預估家數事實表未涵蓋。Base 情境 EPS 五年年增 12.15％，高於內生上界 8.75％（只算本業層），缺口 3.4 個百分點。其中利潤率擴張約 2.4～3.1 個百分點可複算，算式是 2031 年約 22.5％ 除以起點後開五次方減 1：起點用 Base 每年擴約 50 個基點回推的 2026 年約 20.0％ 得 2.4，用最新可用的 2026 上半年 19.3％ 得 3.1。其餘約 0.3～1.0 個百分點是殘差，融資利率事實表未涵蓋，不能確認來自併購。缺口不靠倍數上升。跑道判斷的依據是公司目前服務的裝機基礎只有約 16％，目標 2030 年軟體與服務占營收 25％；集團層滲透率事實表未涵蓋。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_revenue_q3","f_kpi5_2026_q3"],"verdict_values":{"growth":{"driver_mix":"量為主，價格次之，併購附加；回購不是成長來源，2027、2028 年暫停。","runway_years":"集團層滲透率事實表未涵蓋，無法換算年數；服務業務目前服務裝機約 16％。","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段再投資推算的 8.75％，區間 7.5％～10％，只算本業層；共識與 Base 都超過，Base 缺口中利潤率擴張約 2.4～3.1 個百分點可複算，其餘約 0.3～1.0 個百分點是殘差，不能確認來自併購。","segments":[{"item":"能源管理","value":"2026 Q3 有機 +18.8％，2025 年 +10％，利潤率 21.8％"},{"item":"工業自動化","value":"2025 年 +3％，下半年 +7％，利潤率 14.2％，目標 2028 年 18％；Process 與 Hybrid 仍弱"},{"item":"系統","value":"2026 Q2 成長 28％，毛利率低於集團，EBITA 層約中性"},{"item":"軟體與服務","value":"AVEVA ARR 約 +10％；併入 PTC 後以 2025 年為基準約占營收 24％"},{"item":"產品","value":"2025 Q4 +4％，約一半來自價格"},{"item":"區域","value":"北美約占 40％，2026 Q3 +19.9％；中國及東亞 +26.1％"}],"decay_signals":[{"item":"毛利率連 2 季年減","status":"亮燈","note":"2025 年有機年減 40 個基點，2026 上半年扣除關稅退款約年減 37 個基點；公司只半年揭露"},{"item":"EPS 成長顯著高於營收成長","status":"亮燈","note":"共識 FY2 EPS 年增 21.4％，營收年增約 11.4％，差約 10 個百分點"},{"item":"核心市占縮減","status":"未亮","note":"第三方資料顯示與市場同步"},{"item":"提價後銷量下滑","status":"未亮","note":"事實表未見銷量下滑"},{"item":"自由現金流對淨利低於 0.75","status":"未亮","note":"2025 年約 1.10 倍"},{"item":"替代技術壓縮市場","status":"觀察","note":"固態變壓器仍在產業化，2028 年前後才有營收影響"},{"item":"SBC、產業倍數、維護性資本支出","status":"資料缺口","note":"事實表未涵蓋"},{"item":"停止投資新產能","status":"未亮","note":"持續擴充區域產能"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金創造強，但資本配置正從保守轉向重押，PTC 改變了原本以有機成長為主的承諾。","reasoning":"自由現金流對淨利：2022 年 0.94 倍、2023 年 1.13 倍、2024 年 0.97 倍、2025 年 1.10 倍，2026 上半年自由現金流 16 億歐元，部分因去年基期含法國罰款。現金去向以股息為主，2025 年每股 4.20 歐元，連續 16 年累進；回購 2026 上半年 2.5 億歐元，2027、2028 年暫停。PTC 企業價值約 210 億歐元，約市值 15.6％，以 50～60 億歐元股權加 160～170 億歐元優先債融資。目前淨負債約 162.9 億歐元，加上 PTC 債務與 Cognite、Shelly，粗估備考淨負債約 368 億歐元，尚未扣除期間自由現金流，約為 2027 年合併 EBITA 的 3 倍多。CFO 說會維持 A 類信評，WACC 拒絕揭露；CEO 說交割大概在明年第二季，CFO 簡報寫第三季前，兩者沒有對齊。SBC 金額與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi3_free_cash_flow","f_net_debt_m","f_ev_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"已實現併購報酬事實表未涵蓋。CFO 自述 PTC 第五年 ROCE 才超過 WACC，WACC 未揭露；2027 年未計綜效稅後報酬約 3.6％。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"2026 上半年回購 2.5 億歐元，買入均價與 10 年期殖利率事實表未涵蓋；2027、2028 年暫停。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"由淨利除以稀釋 EPS 推算股數：2022 年約 565.4 百萬股，2025 年約 567.9 百萬股，年增約 0.15％，低於 1.5％。SBC 金額事實表未涵蓋；PTC 增資約稀釋 4％，屬融資，不計入此項。"}]},"governance":{"capital_returns":[{"item":"股息","value":"2025 年每股 4.20 歐元，連續 16 年累進"},{"item":"回購","value":"2026～2030 年計畫 25～35 億歐元，2026 上半年 2.5 億歐元，2027、2028 年暫停"},{"item":"併購","value":"Cognite 31 億美元、PTC 約 226 億美元現金、Shelly 約 12 億歐元"},{"item":"融資","value":"股權 50～60 億歐元，優先債 160～170 億歐元，時點未定"},{"item":"信評","value":"Moody's A2，公司承諾維持 A 類"}]}}},"q5_valuation":{"verdict":"現價要求 EPS 五年年增約 10％ 且倍數守住 20 倍，才有年化 8％ 的股價報酬；獲利路徑我相信，併購回報還要驗證，估值只算合理。","reasoning":"事實表把股價與 EPS 標為美元，但 228.65 乘 587.71 百萬股正好等於市值 1,343.8 億歐元，所以實際幣別是歐元，本文一律以歐元讀。現價對 FY2026E 共識 EPS 10.37 為 22.05 倍，對 FY2027E 12.59 為 18.16 倍。要有年化 8％ 的股價報酬，2031 年股價要到約 336 歐元，以 20 倍計需要 EPS 約 16.8 歐元。公司 2030 年目標是有機成長 7％～10％ 加上利潤率再擴 250 個基點，這個要求可信。併購報酬不會很快兌現，所以 Base 倍數從 22 倍降到 20 倍，2027 年 EPS 也低於共識約 3％。賣方目標價均值 300.78 歐元（區間 250～340）是 2026-06-19 的資料，早於 PTC 案，現價低於當時最低目標，但資料過期，不拿來支持進場。PTC 融資是否已進共識無法確認，消息距今不到一季，所以首筆之後先凍結加碼。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_shares_diluted_m","f_ev_m","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"FY1 共識 EPS 本益比，輔以 FY2 本益比與 EV/S","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業估值倍數，無法做跨公司倍數對照。"},"fwd_pe":22.05,"peg":1.59,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 22.05 倍，PEG 約 1.59（第三年共識缺，改用自己 Base 的 FY2026E 到 FY2029E EPS 年增 13.84％），落在 1 到 2 的合理帶；Base 含股息年化約 11.8％。EV/S 在四個年度端點的 97.1 分位，P/S 在 81.8 分位，Trailing P/E 只在 57.6 分位；真正的五年分位與同業倍數事實表未涵蓋，所以只判合理，不判便宜。","upside_short_pct":12.0,"upside_mid_pct":40.5,"denominator_disputed":true,"denominator_note":"共識 EPS 未標明口徑，數值接近調整後 EPS；2025 年財報 EPS 7.33 對調整後約 8.45，差約 15％，PTC 交割後購買價格分攤會再拉開差距。PTC 融資是否已計入共識也未揭露，因此本文不主張便宜。短期上行用 FY2027E Base EPS 12.2 乘 21 倍，中期用 FY2029E 15.3 乘 21 倍。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把資料中心需求高峰當成新常態，同時低估併購把資本報酬拉低多久。","reasoning":"三個主要錯誤來源。第一，資料中心訂單基期在 2027 年變得極難比，公司不揭露客戶拆分，能見度說法也沒有取消條款佐證。第二，PTC 的回報要到第五年才超過 WACC，而 WACC 不揭露、8 億歐元營收綜效不拆分、股權融資時點未定。第三，毛利率修復目前混有關稅退款。法說迴避紀錄中，最影響判斷的是這三項，加上 2027 年漲價幅度與第四季放緩原因沒有正面回答。資料限制：本包的全文逐字稿是 2026-02-26 的全年法說，2026-07-30 與 2026-10-16 只有摘錄；歷史最大回撤、空方數字事實表未涵蓋；26 週跌 14.81％、RSI 32.85 只代表股價已修正，不代表安全邊際。價值陷阱風險中等，兩項衰退信號亮燈。","fact_refs":["f_week26_return_pct","f_rsi14","f_net_debt_m","f_ma_w250","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱風險中等：毛利率與獲利品質兩項信號亮燈，需求與現金尚未受損。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.37,"pe":22.05,"basis":"FY2026E（FY1）共識 EPS，與終端倍數同為當年度預估 EPS 口徑"},"eps":{"bull":[12.9,15.3,17.8,20.2,22.5],"base":[12.2,13.7,15.3,16.9,18.4],"bear":[11.2,10.3,10.6,11.4,12.2]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.84,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"max_dd":{"lo":-40,"hi":-23,"basis":"Bear 谷底 EPS 10.3 歐元（FY2028E）乘 13.5 至 17 倍，得 139 至 175 歐元，相對現價約 −39％ 至 −23％，取 −40％ 至 −23％。歷史最大回撤事實表未涵蓋，無法用過往回撤校準；第一個技術參考是 250 週線 193.61 歐元，約 −15.3％。","trigger_time":null},"basis":{"bull":"資料中心需求延續到 2029 年，系統定價守住，PTC 營收綜效 8 億歐元如期，利潤率約 23％；終端 24 倍高於現值 22.05 倍，事實表未涵蓋同業倍數，只能對照自身。","base":"2027 年略低於共識約 3％，反映增資稀釋約 4％ 與融資利息；之後有機成長 7％～9％，利潤率每年擴約 50 個基點，2031 年約 22.5％；終端 20 倍低於現值 22.05 倍，事實表未涵蓋同業倍數，只能對照自身。增資稀釋已在 EPS 內，淨回購殖利率填 0 避免重複計算。","bear":"資料中心訂單反轉，2028 年 EPS 跌到 10.3 歐元，併購後負債高、利潤率回落至約 18.5％；終端 15 倍為成長降至 5％～10％ 的判斷值，事實表沒有多年前瞻倍數可校準。機率 30％：Base EPS 年增高於內生上界，下限就是 30％，且資料中心占比仍在上升。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"資料中心與網路 2025 年底占營收 30％ 且上升，第三季需求三位數成長；2026 至 2027 年併購約 250 億歐元，粗估備考淨負債約 368 億歐元。","assumption":"超大型雲端資本支出持續到 2028 年以後，客戶不調節奏。","consequence":"以 2027 年資料中心約占營收 35％、需求回落 25％、遞減利潤率 30％ 粗估，EPS 約減 14％；疊加倍數壓到 13.5 至 17 倍，股價約 139 至 175 歐元。","ruling":"採納，列為 Bear 主路徑與唯一致命事件，機率 30％。","watch":"在手訂單年增率、超大型客戶資本支出指引。","evidence_refs":["end_markets#2","supply_demand_durability#0"],"fact_refs":["f_rev_consensus_fy2_m","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"系統業務 2026 年第二季成長 28％，毛利率低於集團；PTC 2027 年未計綜效稅後報酬約 3.6％，回購 2027、2028 年暫停，增資稀釋約 4％。","assumption":"營收成長能同時轉成每股價值與更高的資本報酬。","consequence":"營收達標但 ROCE 低於 15％ 的時間拉長；調整後 EPS 看起來增厚，財報 EPS 被購買價格分攤拉開。","ruling":"部分採納：Base EPS 低於共識約 3％，且不計入營收綜效上緣。","watch":"交割滿一年後的 ROCE、調整後與財報 EPS 的差距。","evidence_refs":["major_events#0","ma_merger#0"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"價格已反映太多","evidence":"EV/S 3.58 倍在四個年度端點的 97.1 分位，P/S 在 81.8 分位；Trailing P/E 在 57.6 分位，FY1 約 22 倍。","assumption":"資料中心高成長已反映在營收倍數上。","consequence":"倍數回到 15 倍時，Bear 五年約 −20％。","ruling":"部分反駁：分位只有四個端點，不足以代表五年區間；FY2 約 18.2 倍。但已跌不是安全邊際，所以結論只到合理。","watch":"FY2 共識 EPS 是否因 PTC 融資下修、增資定價。","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ev_s_percentile","f_ps_percentile","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 228.65","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=228.65","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"併購承諾對照實際行動","cause":null,"prior_field":null,"side_a":"2025-12-11 投資人日，CEO Blum：目前不計畫大型收購，中期目標都是有機。","side_b":"2026-06-30 宣布 Cognite 31 億美元，2026-10-05 宣布 PTC 約 226 億美元現金收購，約市值 15.6％，同時暫停 2027、2028 年回購。","ruling":"方向相反，不可調和。採後者的事實：管理層十個月內改變資本配置框架。CFO 2026-10-05 說相對投資人日承諾不變，只能視為財務目標不變。併購報酬列為未證假設，Base 不計入營收綜效上緣。","evidence_level":"管理層原話與併購公告","settle_metric":"交割滿一年後集團 ROCE 是否回到 15％～20％，PTC ARR 是否維持約 10％ 成長","if_then":["若 2028 年全年 ROCE 低於 15％，減碼至原倉位一半","若交割前再宣布超過市值 5％ 的併購，停止加碼至 2028 年 ROCE 公布","反向：若 2028 年 ROCE 達 15％ 以上且維持 A 類信評，加碼至目標倉位"],"evidence_refs":["major_events#0","major_events#1","ma_merger#0","ma_merger#1"]},{"axis":"毛利率修復的品質","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO：上半年毛利率 42.5％，年增 10 個基點；2026-10-16 CFO：第三季產品定價金額約等於整個上半年。","side_b":"同一場 CFO 說毛利率橋含約 1 億歐元第二季關稅退款，以上半年營收 212 億歐元算約 47 個基點，扣掉後約年減 37 個基點；關稅影響倍數的報導也有出入。","ruling":"程度差異，可調和。定價轉強是真的，但毛利率轉正尚未被乾淨數字證明。關稅退款按一次性處理，歸因標為未證，以下兩個半年度驗證。","evidence_level":"管理層原話與自行換算","settle_metric":"2026 下半年與 2027 上半年扣除一次性項目後的毛利率年變化","if_then":["若兩期都年減，減碼三分之一","若兩期都年增，加碼至目標倉位"],"evidence_refs":["reg_tariff_export#0"]},{"axis":"訂單能見度對照需求見頂","cause":null,"prior_field":null,"side_a":"2026-10-16 CEO：第三季資料中心需求再度三位數成長，能見度延伸到 2027、2028 年。","side_b":"2025-12-11 投資人日高管：大型客戶會調節奏，微軟去年曾放慢；2026-07-30 CEO 提到以 Foxconn 合作緩和放緩；公司兩度拒絕揭露客戶拆分。","ruling":"可調和。能見度是需求規劃的能見度，不等於不可取消的訂單；取消條款事實表未涵蓋，訂單持久性不可裁決至 2027 年 7 月半年報。","evidence_level":"管理層原話，缺合約條款","settle_metric":"2026 年底與 2027 年中在手訂單年增率","if_then":["若 2026 年底在手訂單年增低於 15％，停止加碼","若任一半年度在手訂單年減，減碼一半"],"evidence_refs":["end_markets#2","supply_demand_durability#0","supply_demand_durability#2"]},{"axis":"800V 與固態變壓器時程","cause":null,"prior_field":null,"side_a":"2025-12-11 技術長：2027 年前不預期固態變壓器大規模應用；2026-10-16 CFO：沒有人問 800V。","side_b":"2026-02-26 CEO：2030 年可能影響 15％～25％ 需求，完整架構 2028 年才備妥；Uptime 指部分設計可能不需 sidecar，Navitas 與 EPFL 已展示 250kW 樣機。","ruling":"可調和。2027 年前沒有營收衝擊，但 sidecar 過渡方案有被跳過的風險，投資人日被問到自建、合作或收購時也沒有回答。2026-07-30 CEO 已提到自研方案，先不下修護城河。","evidence_level":"管理層原話與第三方技術報告","settle_metric":"2028 年底前公司固態變壓器方案的超大型客戶設計採用","if_then":["若 2028 年底前無量產案而對手已有，減碼至倉位上限一半","若 2028 年底前取得至少一家超大型客戶量產案，解除此項加碼限制"],"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"axis":"基本面對照股價走勢","cause":null,"prior_field":null,"side_a":"第三季有機成長 16.9％，高於共識 13.8％，全年指引第二次上修。","side_b":"26 週股價跌 14.81％，RSI 32.85，股價低於 52 週線 259.25 歐元與 104 週線 242.47 歐元。","ruling":"可調和。下跌主因是併購融資與軟體疑慮，需求面沒有同步惡化；已跌不等於安全邊際。","evidence_level":"公司公告與價格資料","settle_metric":"增資定價、2026 全年毛利率","if_then":["若股價先站上 52 週線 259.25 歐元而毛利率證據未到，不追","若股價跌到 250 週線 193.61 歐元且在手訂單仍年增，分批反買"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"平衡曝險的說法","cause":null,"prior_field":null,"side_a":"2026-02-26 CEO：三大終端市場各約三分之一，曝險非常平衡。","side_b":"2026-10-16 CFO：去年底資料中心與網路占營收 30％，今年集中度上升。","ruling":"程度差異，可調和，但平衡的敘事正在減弱，資料中心已是最大單一敏感度來源。","evidence_level":"管理層原話","settle_metric":"2026 年終端市場訂單占比","if_then":["若資料中心與網路占 2026 年訂單超過 40％，停止加碼至在手訂單客戶結構揭露"],"evidence_refs":["end_markets#0"]},{"axis":"中國需求的說法轉向","cause":null,"prior_field":null,"side_a":"2025-12-11 CEO：中國通縮，正向定價能力非常有限；2026-02-26 CFO：中國僅低個位數成長。","side_b":"2026-10-16 CEO：中國這個成長水準至少可延續到 2027 年，自承年初較保守；第三季中國及東亞成長 26.1％。","ruling":"可調和。成長回升主要跟資料中心有關，建築與住宅仍慢，定價是否改善尚未證實，不把中國列入 Base 的利潤率上修。","evidence_level":"管理層原話","settle_metric":"2027 上半年中國成長與定價說明","if_then":["若 2027 上半年中國成長回落到個位數，停止加碼"],"evidence_refs":["end_markets#1","geo_supply_chain#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：電氣化與資料中心需求創高，在手訂單創紀錄，CEO 稱四大終端市場需求健康。","side_b":"競爭與替代：專業廠商份額並列，固態變壓器進入產業化，關稅與第二波投入成本持續。","ruling":"雙向拉鋸。需求面結構轉好，競爭與替代技術同時施壓，價值分配尚未定案。","evidence_level":"第三方份額資料、公司公告","settle_metric":"份額資料與扣除一次性項目的毛利率","if_then":["若第三方資料顯示連續兩年份額下降，減碼三分之一"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"axis":"最強反方論證","cause":null,"prior_field":null,"side_a":"現在就買：第三季高於共識 3.1 個百分點，指引兩度上修，股價反而下跌；FY2 只有 18.16 倍，Bear 五年約 −20％，Base 約 +61％。","side_b":"現在就賣：資料中心需求是高峰讀數，下一步是基期變難；公司在需求最好時舉債買軟體，還有 50～60 億歐元增資沒有定價。","ruling":"兩邊都成立。裁定基本面可以持有，但不在增資定價前一次買足。","evidence_level":"公司公告、情境估算","settle_metric":"增資定價折價與 2026 全年在手訂單","if_then":["若增資折價超過 8％ 但在手訂單仍年增，分批反買","若 2026 年底在手訂單年增低於 15％，停止加碼"],"evidence_refs":["capital_markets_pricing#0","regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"2026 年全年財報確認在手訂單延續成長","type":"假設驗證","maps_to":"H1","metric":"年底在手訂單年增率","threshold":"2026 年底年增 15％ 以上","action":"達標維持假設；未達標列為削弱並停止加碼","source_freq":"公司全年財報，每半年揭露","date":"2027-02"},{"n":2,"text":"集團在手訂單總額首次年減","type":"Single Thing","maps_to":"H1","metric":"在手訂單年增率","threshold":"任一半年度低於 0％","action":"減碼一半","source_freq":"公司半年報與全年財報","date":"2027-02 起逐期"},{"n":3,"text":"定價無法吸收關稅與原料成本","type":"風險","maps_to":"R2","metric":"扣除一次性項目後毛利率年變化，及損益橋淨價格","threshold":"連兩個半年度毛利率年減，或淨價格轉負","action":"減碼三分之一","source_freq":"公司半年報毛利率橋","date":"2027-07","evidence_refs":["reg_tariff_export#0"]},{"n":4,"text":"併購融資使信評跌出 A 類","type":"風險","maps_to":"R3","metric":"信用評等類別","threshold":"任一主要評等機構評等低於 A 類","action":"減碼三分之一並停止加碼","source_freq":"評等機構公告，事件驅動","date":"2027-12 前","evidence_refs":["customer_concentration_credit#0","major_events#0"]},{"n":5,"text":"增資定價完成且毛利率過關","type":"加碼","maps_to":"H2","metric":"增資折價與 2026 下半年毛利率","threshold":"折價不超過 8％，且扣除一次性項目後毛利率年增","action":"補足至目標倉位","source_freq":"公司公告與全年財報","date":"2027-02"},{"n":6,"text":"股價先跌到長期均線而基本面無損","type":"估值rearm","maps_to":"H1","metric":"股價與在手訂單年增率","threshold":"股價不高於 193.61 歐元，約 FY2026E 的 18.7 倍，且在手訂單仍年增","action":"分批反買","source_freq":"每日股價，半年度訂單","date":null},{"n":7,"text":"股價超過合理上緣","type":"減碼","maps_to":"H1","metric":"股價對 FY2027E 共識 EPS 倍數","threshold":"股價不低於 315 歐元，約 25 倍","action":"減碼三分之一","source_freq":"每日股價","date":null},{"n":8,"text":"需求與資產負債表同時失守","type":"清倉","maps_to":"H1","metric":"在手訂單年增率與信評類別","threshold":"在手訂單年減，且信評跌出 A 類，同時成立","action":"清倉","source_freq":"公司財報、評等機構公告","date":null},{"n":9,"text":"固態變壓器競爭落後","type":"風險","maps_to":"R4","metric":"超大型客戶設計採用與量產案","threshold":"2028 年底前公司無量產案，而對手已有","action":"減碼至倉位上限一半","source_freq":"法說與產業報告，每季","date":"2028-12","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":10,"text":"電池模組安全警示擴大","type":"風險","maps_to":"R5","metric":"召回範圍與提列金額","threshold":"歐美主管機關發布同型號召回，或提列超過 1 億歐元","action":"停止加碼至召回範圍與費用揭露","source_freq":"監管機關與公司公告，事件驅動","date":null,"evidence_refs":["major_events#2","product_recall_warning#0"]},{"n":11,"text":"通路定價監管升級","type":"風險","maps_to":"R5","metric":"法國案上訴結果與新調查","threshold":"上訴敗訴且新增提列超過 1 億歐元，或歐盟層級啟動同類調查","action":"停止加碼至影響營收揭露","source_freq":"公司與監管機關公告，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0"]},{"n":12,"text":"2026 年全年財報後完整複審","type":"複審日期","maps_to":"H1","metric":"日期","threshold":"全年財報公布後","action":"重跑完整研究","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"集團在手訂單年增率","bear_threshold":"低於 0％","window":"每半年，2027-02 起","source":"公司全年財報與半年報","last_status":"ok"},{"metric":"扣除一次性項目後毛利率年變化","bear_threshold":"連兩個半年度年減","window":"2026 下半年、2027 上半年","source":"公司半年報毛利率橋","last_status":"warning"},{"metric":"集團 ROCE","bear_threshold":"PTC 交割滿一年後低於 15％","window":"2028 年度財報","source":"公司年報","last_status":"unknown"},{"metric":"信用評等類別","bear_threshold":"跌出 A 類，目前 Moody's A2","window":"融資起至交割後 24 個月","source":"評等機構公告","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.decision_inputs.wait_for_price","reason":"閘把增資定價讀成等待股價的條件。原判斷寫的是事件條件：增資完成定價、折價不超過 8％，加上 2026 下半年毛利率扣除一次性項目後年增，兩項都成立才補足倉位，這個條件已完整寫在補足倉位條件與第 5 條觸發，沒有對應的股價水準可填。第 6 條 193.61 歐元是基本面無損時的反買價，第 7 條 315 歐元是減碼價，都不是增資前的等待價，硬填會造出原判斷沒有的進場價。"}],"action_conditions":{"rearm_trigger":"增資定價完成且折價不超過 8％，加上 2026 下半年毛利率扣除一次性項目後年增，兩項都成立才補足倉位。","exec_line":"不追高，分兩段：確認前只放首筆，上限為目標倉位三分之一；PTC 增資定價與 2026 全年毛利率都過關才補足；在手訂單轉為年減就停止加碼並減碼一半。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把併購融資與 AI 軟體疑慮放大到本業：股價 26 週跌 14.81％，但第三季有機成長高於共識 3.1 個百分點，全年指引兩度上修，在手訂單創高。市場對資本報酬的擔心有道理，對需求的折價目前沒有數據支持。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"資料中心與其他終端市場的需求，足以支撐 2027 年有機營收成長至少 10％。","2y":"2027 年有機營收成長 10％ 以上，2026 年底在手訂單年增 15％ 以上","5y":null,"10y":null,"threshold":"2027 年有機營收成長 10％ 以上","source":"公司季度營收稿、全年財報；FY2 共識營收 504.96 億歐元","drift_rule":"TTM 有機成長低於門檻的幅度連 2 季達 5％ 為削弱，連 3 季達 10％ 為反轉"},{"id":"H2","text":"定價與生產力能把調整後 EBITA 利潤率推到 2030 年至少 21％，毛利率不靠一次性項目。","2y":null,"5y":"2030 年調整後 EBITA 利潤率 21％ 以上，毛利率不低於 42％","10y":null,"threshold":"2030 年調整後 EBITA 利潤率 21％ 以上","source":"公司半年報毛利率與利潤率橋","drift_rule":"TTM 利潤率低於路徑的幅度連 4 季達 5％ 為削弱，連 6 季達 10％ 為反轉"},{"id":"H3","text":"PTC 與 Cognite 併購後，集團 ROCE 在交割滿一年後回到 15％～20％，並維持 A 類信評。","2y":null,"5y":"2028 年 ROCE 15％ 以上，PTC 案第五年 ROCE 高於 WACC","10y":null,"threshold":"交割滿一年後 ROCE 15％ 以上","source":"公司年報 ROCE、評等機構公告","drift_rule":"ROCE 低於門檻的幅度連 4 季達 5％ 為削弱，連 6 季達 10％ 為反轉"}],"R":[{"id":"R1","text":"資料中心訂單見頂，大客戶調整建置節奏，高基期使 2027 年下半年成長明顯放慢。","h_ref":"H1","clock":"🔥","threshold":"在手訂單年增低於 0％","evidence_refs":["end_markets#2","supply_demand_durability#0"]},{"id":"R2","text":"定價追不上關稅與半導體、記憶體、銅的第二波成本，毛利率修復只是關稅退款造成。","h_ref":"H2","clock":"🔥","threshold":"扣除一次性項目後毛利率連兩個半年度年減","evidence_refs":["reg_tariff_export#0"]},{"id":"R3","text":"PTC 約 210 億歐元併購回報低於預期，負債升高；新任 CFO 上任不到一年就要執行融資，營收綜效與 WACC 都不揭露細節。","h_ref":"H3","clock":"🐢","threshold":"交割滿一年後 ROCE 低於 15％，或信評跌出 A 類","evidence_refs":["major_events#0","major_events#1","ma_merger#0","ma_merger#1","regulatory_antitrust#1"]},{"id":"R4","text":"800V 直流與固態變壓器讓新進者切入配電架構，sidecar 過渡方案被跳過。","h_ref":"H2","clock":"🐢","threshold":"2028 年底前無超大型客戶量產案，而對手已有","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R5","text":"監管與產品安全事件衝擊通路定價與品牌：法國案罰款 2.07 億歐元、智利電池模組警示；受影響營收事實表未涵蓋。","h_ref":"H2","clock":"🐢","threshold":"上訴敗訴且新增提列超過 1 億歐元，或歐美主管機關發布召回","evidence_refs":["regulatory_antitrust#0","major_events#2","product_recall_warning#0"]},{"id":"R6","text":"零組件與記憶體短缺、中東情勢影響短期交付，第四季放緩超過指引隱含幅度。","h_ref":"H1","clock":"⚡","threshold":"2026 年全年有機成長低於 12％","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"集團在手訂單總額在任一半年度揭露時出現年減（2025 年底為逾 250 億歐元）。","why_fatal":"資料中心與網路占營收 30％ 以上，是最大單一敏感度來源：需求回落 25％ 約使 EPS 減 14％，高於 PTC 成本綜效完全落空的約 3％，而且會發生在併購後負債最高的時候。","if_happens":"Base 的 2028 年以後路徑失效，轉向 Bear，倍數同時被壓縮，股價區間看 139 至 175 歐元，減碼一半。","how_monitor":"每半年查在手訂單金額與年增率；第三季營收稿看資料中心需求描述；追蹤超大型雲端客戶資本支出指引。","probability":"12 至 24 個月約 20％；本包沒有訂單時間序列可校準，屬判斷。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":18.16,"peg_fy2":1.31,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":7.33,"FY2026E":10.37,"FY2027E":12.59,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為財報稀釋 EPS；FY2026E、FY2027E 為 yfinance 共識，未標口徑，數值接近調整後 EPS（2025 年調整後淨利約 48 億歐元，推算每股約 8.45），兩者不同源。FY2028E 共識事實表未涵蓋，留空；EPS 預估家數也未涵蓋。事實表幣別標美元，實際為歐元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 年全年財報與 2027 年指引","impact":"高","watch":"在手訂單年增率、扣除一次性項目後毛利率、2027 年有機成長指引"},{"date":null,"date_precision":null,"type":"other","event":"PTC 增資 50～60 億歐元定價，時點未定","impact":"高","watch":"折價幅度、股權與債務的先後順序"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"Shelly Group 約 12 億歐元收購預計完成","impact":"低","watch":"要約結果與監管核准"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"2027 年上半年財報","impact":"高","watch":"毛利率橋、在手訂單、資料中心基期效應"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"PTC 交割期限，CFO 口徑第三季前，CEO 口徑大概第二季","impact":"高","watch":"CFIUS 等審批、競標者介入、人才留任"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把併購融資與 AI 軟體疑慮放大到本業：股價 26 週跌 14.81％，但第三季有機成長高於共識 3.1 個百分點，全年指引兩度上修，在手訂單創高。市場對資本報酬的擔心有道理，對需求的折價目前沒有數據支持。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-14.81, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
