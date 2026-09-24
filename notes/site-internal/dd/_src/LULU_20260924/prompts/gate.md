你是 DD 管線 v20 的判斷層閘（gate），標的 LULU（20260924）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。[gate_contract §④]

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_net_revenue_gaap`（q1_business）｜Net revenue（GAAP）＝2415.6 $M｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 Condensed Consolidated Statements of Operations（$2,415,631K vs 去年同期 $2,525,219K）；QoQ 為自算（vs Q1 $2,471,603K）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：共識約 $2.46B、實際低約 1.6%（web_search 聚合站報導，未經第二來源核對）；公司自家 Q2 指引 $2.450–2.475B，實際低於指引下緣
- `f_kpi1_comparable_sales_total`（q1_business）｜Comparable sales（total）＝-9 %｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（constant dollar −10%；Americas −12%；International −3%，constant dollar −6%；China Mainland −2%，constant dollar −8%）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a（未取得可靠的 comp 共識）
- `f_kpi2_gross_margin_gaap`（q1_business）｜Gross margin（GAAP）＝60.5 %｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（gross profit $1,461,878K；含 IEEPA 關稅退款 $134.5M＝+560bp）；扣除退款的 54.9% 為自算（60.5%−5.6pp；管理層電話會議亦說 ex-refund 較指引的 −410bp 好 50bp，即 −360bp，兩者相符）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi3_gaap_operating_income_op`（q1_business）｜GAAP operating income／operating margin＝18.8 % margin（營業利益 $453.7M）｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（income from operations $453,653K vs $523,814K，YoY −13%；margin 18.8% vs 20.7%）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi4_operating_margin_ieepa_n`（q1_business）｜Operating margin 扣除 IEEPA 關稅退款（自算，非公司 non-GAAP）＝13.2 % margin（營業利益約 $319.2M）｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：GAAP 營業利益 $453.653M − 公司揭露的退款 $134.5M（新聞稿註明退款使 operating margin +560bp）。公司本季不發布 non-GAAP 營業利益（新聞稿的 non-GAAP 只有 constant dollar），此數字僅供還原一次性項目（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi8_guidance_q3_fy2026`（q1_business）｜Guidance：Q3 FY2026＝營收 $2.290–2.320B（YoY −10% 至 −11%）；EPS $0.93–0.98；營業利益率約 6.5%（去年 Q3 為 17%） range｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（營收與 EPS、稅率約 30%）；營業利益率、毛利率 −250bp、SG&A 去槓桿 800bp、降價 +60bp、北美中段兩位數衰退（美國同）、中國大陸與其他市場 +3–5% 來自 CFO 於 2026-09-03 電話會議的準備稿（逐字稿 LULU_Q2_2027_Earnings_Call_20260903.md）（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a（未取得 Q3 單季共識）
- `f_kpi9_guidance_fy2026`（q1_business）｜Guidance：FY2026 全年＝營收 $10.350–10.500B（YoY −5% 至 −7%）；EPS $9.48–9.73（含 Q2 退款 +$0.86）；營業利益率較 FY2025 −530bp（含退款 +130bp） range｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（營收、EPS、稅率約 30%、不含任何後續退款與回購）；毛利率 −80bp、SG&A +450bp、降價 +40bp、營業利益率 −530bp、淨新店約 35 家來自電話會議準備稿（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：FY1 EPS 共識 $9.39（dd_numbers_extra.py consensus_revision，2026-09-19 快照），低於新指引下緣 $9.48；90 天前（2026-06-23）為 $11.03
- `f_peer_lulu_gross_margin_pct`（q2_moat）｜LULU 毛利率＝56.11 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LULU.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lulu_operating_margin_pct`（q2_moat）｜LULU 營業利益率＝17.84 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LULU.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lulu_fcf_margin_pct`（q2_moat）｜LULU FCF 利潤率＝12.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LULU.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nke_gross_margin_pct`（q2_moat）｜NKE 毛利率＝42.91 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NKE.gross_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nke_operating_margin_pct`（q2_moat）｜NKE 營業利益率＝8.18 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NKE.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_onon_gross_margin_pct`（q2_moat）｜ONON 毛利率＝64.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_onon_operating_margin_pct`（q2_moat）｜ONON 營業利益率＝13.79 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_deck_operating_margin_pct`（q2_moat）｜DECK 營業利益率＝22.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DECK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_deck_fcf_margin_pct`（q2_moat）｜DECK FCF 利潤率＝20.22 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DECK.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rl_gross_margin_pct`（q2_moat）｜RL 毛利率＝70.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rl_operating_margin_pct`（q2_moat）｜RL 營業利益率＝16.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝9.39 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.78 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-19）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝9.78 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-19）
- `f_kpi6_free_cash_flow`（q1_business）｜Free cash flow（單季）＝225.2 $M（占營收 9.3%）｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：Q2 營運現金流 $374.8M（上半年 $589,278K − Q1 $214,440K）− Q2 資本支出 $149.7M（上半年 $277,056K − Q1 $127,380K，10-Q https://www.sec.gov/Archives/edgar/data/1397187/000139718726000127/lulu-20260802.htm 與 Q1 10-Q；管理層電話會議說 capex 約 $150M）。公司新聞稿只揭露上半年累計，不揭露單季 FCF。營運現金流含已收到的關稅退款 $134.5M（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi7_stock_based_compensation`（q1_business）｜Stock-based compensation（單季）＝21.1 $M（占營收 0.9%；占 GAAP 營業利益 4.6%；占扣退款營業利益 6.6%）｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q 股東權益變動表：上半年 $50,275K − Q1 $29,186K（Q1 10-Q）＝Q2 $21,089K；占比為自算（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi11_share_repurchases`（q1_business）｜Share repurchases（單季）與 門市數＝330.0 $M（2.7M 股）；期末 825 家門市（淨增 9）｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1；剩餘授權約 $713M（電話會議）。期末現金 $1,389.7M、循環信用可用額度 $593.7M。回購 $330.0M 高於同季自算 FCF $225.2M，差額由現金池補（現金較 FY2025 年底 $1,807.2M 少 $417.5M）（numbers.latest_quarter_kpis.items[11]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：n/a
- `f_kpi5_diluted_eps_gaap`（q1_business）｜Diluted EPS（GAAP）＝2.92 $｜期間與口徑：Q2 FY2026（季末 2026-08-02，公告於 2026-09-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（vs $3.10；含關稅退款與相關利息稅後 +$0.86）；扣除退款的 $2.06 為自算（2.92−0.86）（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-08-02，公告於 2026-09-03））
  - 註記：共識約 $1.82（web_search 聚合站報導，未經第二來源核對）；公司自家 Q2 指引 $1.76–1.81。GAAP 數字勝出全靠退款，扣除後 $2.06 仍高於指引，主因為較指引低的獎金提列與費用管控（管理層說明）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝102.28 USD｜期間與口徑：2026-09-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝10.89 x｜期間與口徑：2026-09-19／分母＝FY1 EPS 9.39，分子＝快照價 102.28｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-19）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝8.54 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.02 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.09 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-23（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-14.87 %｜期間與口徑：2026-06-23 → 2026-09-19／FY1 共識 EPS 11.03 → 9.39（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-19）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-35.56 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.04｜期間與口徑：2026-09-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-09-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）
  - 原文：「price 102.28 / W52 152.2 / W104 221.54 / W250 296.45 / W250 13週斜率 -1.82%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝296.45 USD｜期間與口徑：2026-09-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）

### findings_digest 中方向為負或來源衝突的條目（32 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Earnest Analytics (交易資料)：2023-04 至 2024-04，Vuori 與 Alo Yoga 各自約取得 1% 的市占；Nike 與 Lululemon 仍主導 Active／Athleisure 市場；除 Under Armour 掉份額外，其餘品牌市占持平或略升。文中未給 Lululemon 單獨的市占百分比。資料期間為 2024 年，非 2026。
  - 來源：Earnest Analytics, 'Athleisure shoppers lean into Vuori, Alo Yoga' — https://www.earnestanalytics.com/insights/athleisure-shoppers-lean-into-vuori-alo-yoga（as_of 2024-04-22）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Forbes 2026-01-21 文章標題為「Lululemon Hits The Wall While Fabletics Takes Flight」，標題把 Fabletics 描述為上升中的競爭者、Lululemon 為遇到瓶頸的一方。僅見標題與搜尋摘要，內文未抓取，無法引用具體數字。
  - 來源：Forbes (Pamela Danziger), 'Lululemon Hits The Wall While Fabletics Takes Flight' — https://www.forbes.com/sites/pamdanziger/2026/01/21/lululemon-hits-the-wall-while-fabletics-takes-flight/（as_of 2026-01-21）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：搜尋摘要顯示：2025 年 9 月 Nike 與 Kim Kardashian 的 SKIMS 推出獨立女性運動服品牌 NikeSKIMS，目標是搶回被 Lululemon、Vuori、Alo 拿走的女性消費者。as_of 為月份層級（2025-09），日期以當月 1 日代填；具體出自哪一篇搜尋結果未逐篇核對（同批結果含 Retail TouchPoints 'Athleisure Faceoff' 一文）。
  - 來源：WebSearch 結果摘要（query: 'Lululemon new entrant OR displace threat athleisure 2026 Alo Vuori'），相關文章：Retail TouchPoints, 'Athleisure Faceoff: How Lululemon, Vuori, Alo and Fabletics are Making Their Case to Consumers' — https://www.retailtouchpoints.com/topics/market-news/athleisure-faceoff-how-lululemon-vuori-alo-and-fabletics-are-making-their-case-to-consumers（as_of 2025-09-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：10-K 原文："Many of the specialty fabrics used in our products are technically advanced textile products developed and manufactured by third parties and may be available, in the short term, from only one or a limited number of sources."
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：公司 2026-03-18 公布的 FY2026 指引為營收 $11.35–11.50B（分析師預期 $11.52B）、EPS $12.10–12.30（預期 $12.58）。報導引述的需求面描述為「設計新鮮度不足、客戶支出轉軟、大型對手競爭」；管理層優先事項為北美重回全價銷售成長，手段為產品新鮮度、SKU 縮減與庫存再平衡。
  - 來源：FashionNetwork USA, 'Lululemon forecasts softer 2026 amid demand strains, taps ex-CEO of Levi for board' https://us.fashionnetwork.com/news/Lululemon-forecasts-softer-2026-amid-demand-strains-taps-ex-ceo-of-levi-for-board,1816672.html（as_of 2026-03-18）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：同一報導：FY2026 預估關稅衝擊約 $380M（2025 年為 $275M）；Q4 毛利率年減 550bps，其中 520bps 來自美國進口關稅；公司預期以減少降價與提高全價銷售抵銷「幾乎全部」關稅影響。
  - 來源：FashionNetwork USA, 'Lululemon forecasts softer 2026 amid demand strains, taps ex-CEO of Levi for board' https://us.fashionnetwork.com/news/Lululemon-forecasts-softer-2026-amid-demand-strains-taps-ex-ceo-of-levi-for-board,1816672.html（as_of 2026-03-18）｜affects：decision_inputs.bear、valuation
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Q2 FY2026 財報公布前的預覽（尚非實際結果）：共識 Q2 營收 $2.45–2.475B、年減 2.7%（去年同期年增 6.5%）；共識 EPS $1.79 vs 去年 $3.10（-42.3%）；全年 EPS 指引由 $12.10–12.30 下修至 $10.95–11.15；預估毛利率年減 410bps，其中關稅約 150bps、降價再增 40–50bps；中國大陸預期 +19.5%、其他地區 +14.6%，北美走勢「疲弱」、客流「不均」。此為聚合站預覽文，實際 Q2 結果須待財報。
  - 來源：Pomegra News, 'Lululemon Q2 2026: Athleisure Under Pressure' https://pomegra.io/news/lululemon-q2-2026-athleisure-under-pressure（as_of 2026-09-24）｜affects：moat_trend、thesis.R、decision_inputs.bear、triggers
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Texas Attorney General Ken Paxton announced on 2026-04-13 that his office opened an investigation (civil investigative demand) into Lululemon over whether its athletic apparel contains PFAS ('forever chemicals') that health-conscious customers would not expect given the brand's marketing. Scope: review of the company's Restricted Substances List, testing protocols and supply chain practices against its stated safety standards. Framed as a consumer-protection matter.
  - 來源：National Law Review, 'Texas AG Announces CID to Lululemon into PFAS in Athletic Apparel' https://natlawreview.com/article/texas-ag-investigates-lululemon-potential-presence-pfas-activewear ; Freeman Mathis & Gary, 'PFAS regulatory scrutiny expands to consumer apparel: What the Texas AG's Lululemon inquiry signals' https://www.fmglaw.com/environmental-law/pfas-regulatory-scrutiny-expands-to-consumer-apparel-what-the-texas-ags-lululemon-inquiry-signals/（as_of 2026-04-13）｜affects：moat_trend、decision_inputs.bear、triggers
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：公司 2026 年預期關稅成本毛額約 $380M，另有較高的行銷與人力支出（2026 年指引偏弱）。此為 2026-03 財測時的數字，之後是否更新未查證。
  - 來源：Jing Daily, 'Lululemon warns of weaker 2026 as tariffs bite', https://jingdaily.com/intels/2026-03/18/lululemon-warns-of-weaker-2026-as-tariffs-bite（數字取自搜尋摘要，未抓全文）（as_of 2026-03-18）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025（截至 2026-02-01）10-K：未緩解的關稅上升加 de minimis 豁免取消，使 2025 年毛利減少約 $275M；de minimis 取消與 IEEPA 等法源下的較高關稅對 2025、2026 年營運結果有重大不利影響。
  - 來源：SEC EDGAR, lululemon athletica inc. Form 10-K (FY ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（取自搜尋摘要；as_of 用會計年度結束日，未核到實際提交日）（as_of 2026-02-01）｜affects：moat_trend、decision_inputs.bear
- `reg_tariff_export#6`（reg_tariff_export｜方向 -｜狀態 ok）：2026-06-30 Hagens Berman 於美國華盛頓西區聯邦地方法院提起消費者集體訴訟，指控 LULU 自 2025-02 起以 IEEPA 關稅為由調高直營進口商品售價，向消費者多收數億美元，而該關稅其後被宣告無效；Law360 另報導有新一起消費者關稅退款訴訟。
  - 來源：Business Wire / Hagens Berman press release, 'Hagens Berman Files Consumer Class Action Accusing Lululemon of Unlawfully Passing Tariff Costs to Consumers', https://www.businesswire.com/news/home/20260630748486/en/Hagens-Berman-Files-Consumer-Class-Action-Accusing-Lululemon-of-Unlawfully-Passing-Tariff-Costs-to-Consumers；Law360, 'Lululemon Targeted In New Shopper Tariff Refund Lawsuit', https://www.law360.com/articles/2496328/lululemon-targeted-in-new-shopper-tariff-refund-lawsuit（as_of 2026-06-30）｜affects：decision_inputs.bear、triggers
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 面料產地：台灣 34%、中國大陸 29%、南韓 10%、越南 10%。
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險段寫明：相當比例的技術面料來自台灣，台灣海峽軍事衝突、貿易禁運或該區中斷，可能對公司取得原料與履行客戶訂單的能力造成重大影響。
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 約 51 家成衣代工廠、約 65 家面料供應商；前五大代工廠占產量 47%（最大一家約 15%）；前五大面料供應商占面料 48%（最大一家約 20%）。
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 寫明：許多特殊面料是第三方開發製造的技術型紡織品，短期內可能只有一家或少數幾家來源。
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：moat_trend、thesis.R
- `geo_supply_chain#5`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險段稱公司與任何供應商或代工廠均無長期合約，且與其他公司競爭面料、原料與產能。
  - 來源：lululemon athletica inc. Form 10-K (fiscal year ended 2026-02-01), https://www.sec.gov/Archives/edgar/data/1397187/000139718726000020/lulu-20260201.htm（as_of 2026-02-01）｜affects：decision_inputs.bear
- `geo_supply_chain#6`（geo_supply_chain｜方向 -｜狀態 ok）：lululemon 在長城辦的瑜珈活動出現日本太鼓道具，引發中國消費者反彈，公司公開道歉。
  - 來源：CNN, 'Lululemon yoga event on Great Wall of China causes Japanese drum furor', https://www.cnn.com/2026/06/17/china/lululemon-wall-of-china-drum-japan-intl-hnk（as_of 2026-06-17）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：FY2026 Q2（截至 2026-08-02）Americas 淨營收 $1,616.8M，年減 8%（去年同期 $1,758.2M）；Americas 可比銷售年減 12%，為各區最弱。Americas 占總營收 67%。
  - 來源：lululemon athletica inc. Announces Second Quarter Fiscal 2026 Results (BusinessWire) https://www.businesswire.com/news/home/20260903500312/en/lululemon-athletica-inc.-Announces-Second-Quarter-Fiscal-2026-Results ；佐證 Sporting Goods Intelligence https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article（as_of 2026-09-03）｜affects：moat_trend、thesis.R、decision_inputs.bear、valuation
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：FY2026 Q2 China Mainland 淨營收 $407.1M，報告幣別 +4%、固定匯率 -2%；可比銷售固定匯率 -8%；占總營收 17%。SGI 稱管理層承認結果「well below」預期。
  - 來源：Sporting Goods Intelligence, Lululemon Q2 2026 results: revenue down 4% as key markets weaken https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article（as_of 2026-09-03）｜affects：moat_trend、thesis.H、thesis.R、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：FY2026 Q2 全公司淨營收約 $2.4B，年減 4%（固定匯率 -5%）；全球可比銷售 -9%（固定匯率 -10%）；FY2026 營收指引下修至 $10.35–10.5B，SGI 標示為年減 5–7%。
  - 來源：Sporting Goods Intelligence https://www.sgieurope.com/financial-results/lululemons-tough-quarter-deepens-across-key-markets/122957.article ；Yahoo Finance 轉載 Q2 新聞稿 https://finance.yahoo.com/markets/stocks/articles/lululemon-athletica-inc-announces-second-200500621.html（as_of 2026-09-03）｜affects：moat_trend、decision_inputs.bear、valuation、triggers
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Rest of World 全年營收指引：Q1 時為「mid-teens」成長，Q2 財報後下修為「mid-single digits」成長。
  - 來源：TradingKey, Lululemon (LULU) Fiscal Q2 2026 Earnings Call: Guidance Cut as Revenue Falls https://www.tradingkey.com/news/transcripts/262150881-tradingkey ；Investing.com Q1 2026 逐字稿 https://www.investing.com/news/transcripts/earnings-call-transcript-lululemon-q1-2026-sees-revenue-rise-stock-gains-93CH-4727636（as_of 2026-09-03）｜affects：thesis.H、valuation、triggers
- `end_markets#6`（end_markets｜方向 -｜狀態 ok）：Kungfudata 對 Q1 FY26 的標題稱 China 成長 30%，「home market」（本土市場）萎縮 3%。搜尋摘要未載明該 3% 是 Americas 還是美國，引用時以標題字面為準。
  - 來源：Kungfudata, Lululemon's China just grew 30%. Its home market shrank 3%. https://kungfudata.com/resources/lululemon-q1-fy26-china-growth（as_of 2026-06-04）｜affects：moat_trend、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：lululemon 在委託書中揭露，創辦人 Chip Wilson 曾對競爭對手 Alo 與 Vuori 提供諮詢（advised）。Bloomberg 報導標題：Lululemon Says Its Founder Has Advised Rivals Alo and Vuori。
  - 來源：Bloomberg, 'Lululemon (LULU) Discloses Founder Chip Wilson Has Advised Rivals Alo, Vuori', https://www.bloomberg.com/news/articles/2026-04-28/lululemon-says-its-founder-has-advised-rivals-alo-and-vuori（as_of 2026-04-28）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：lululemon 的 10-K 風險因素寫明：公司的織物與製造技術通常未取得專利，可被競爭對手模仿；織物、技術與製程的智慧財產多由供應商擁有或控制，並非 lululemon 獨有；公司持有的專利與專屬智慧財產有限。若競爭對手以較低價格賣類似產品，淨營收與獲利可能受影響。
  - 來源：lululemon athletica inc. Form 10-K（搜尋結果列出的最新一份為 FY2023 財年報，期末 2024-01-28）https://www.sec.gov/Archives/edgar/data/1397187/000139718724000010/lulu-20240128.htm；搜尋摘要未指明此句出自哪一份 10-K，as_of 取該份年報期末日（as_of 2024-01-28）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：2026-09-03 公司第二度下修全年財測：FY2026 營收 $10.35–10.50B（前次 $11.0–11.15B，同比 -5% 至 -7%）、EPS $9.48–9.73（前次 $10.95–11.15）。報導同時列出事前市場共識：營收 $11.03B、EPS $10.84，新財測中點明顯低於共識。
  - 來源：Yahoo Finance, 'Lululemon tumbles 17% after another guidance cut; Q2 tops estimates' https://finance.yahoo.com/markets/stocks/articles/lululemon-tumbles-15-weak-guidance-204337889.html ；MarketBeat 'lululemon athletica Updates FY 2026 Earnings Guidance' https://www.marketbeat.com/instant-alerts/guidance-lululemon-athletica-nasdaq-lulu-updates-fy-2026-earnings-guidance-2026-09-03/（as_of 2026-09-03）｜affects：valuation、thesis.R、decision_inputs.bear、triggers
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 FY2026 財測：營收中點 $2.305B 對共識 $2.53B；EPS $0.93–0.98 對共識 $2.41。JPMorgan 稱 Q3 展望較共識低約 60%。
  - 來源：Yahoo Finance 'Lululemon tumbles 17% after another guidance cut' https://finance.yahoo.com/markets/stocks/articles/lululemon-tumbles-15-weak-guidance-204337889.html（Q3 共識數字，經搜尋摘要取得）；Yahoo Finance 'Lululemon (LULU): Wall Street Keeps Cutting Targets, But Nobody's Calling It Cheap Enough to Buy' https://finance.yahoo.com/markets/stocks/articles/lululemon-lulu-wall-street-keeps-215239806.html（JPMorgan 60% 說法，2026-09-21 刊出）（as_of 2026-09-03）｜affects：valuation、thesis.R、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 FY2026 營收年減 4% 至 $2.42B，低於分析師預期的 $2.46B；Americas 營收 -8%、同店銷售 -9%。Yahoo 標題稱 Q2 EPS 優於預期，營收未達。報導稱此次為今年第二度下修全年財測。
  - 來源：Yahoo Finance 'Lululemon Athletica (LULU) Cut Full Year Guidance After Q2 Revenue Decline' https://finance.yahoo.com/markets/stocks/articles/lululemon-athletica-lulu-cut-full-030922053.html ；'Lululemon Shares Fall 17% After FY2026 Guidance Cut Despite Q2 Earnings Beat' https://finance.yahoo.com/markets/stocks/articles/lululemon-shares-fall-17-fy2026-094142265.html（as_of 2026-09-03）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：財測下修後個別目標價調整（Yahoo 2026-09-21 彙整）：Citi $130→$117（Neutral，稱股價重挫後風險報酬『略為有利』）；Wells Fargo $105→$95（Equal Weight，稱下滑幅度『jarring』，並把下半年獲利預估下調約 30%）；JPMorgan $154→$95；Morgan Stanley $83（Underweight，分析師 Alex Straton 預期仍有進一步負向修正）；Truist $82（Sell）；BMO 新評等 Underperform、目標價 $70。stockanalysis 同期另記 Goldman Sachs $111→$95、Morgan Stanley $93→$83。
  - 來源：Yahoo Finance 'Lululemon (LULU): Wall Street Keeps Cutting Targets, But Nobody's Calling It Cheap Enough to Buy' https://finance.yahoo.com/markets/stocks/articles/lululemon-lulu-wall-street-keeps-215239806.html ；stockanalysis.com https://stockanalysis.com/stocks/lulu/forecast/（as_of 2026-09-21）｜affects：valuation、decision_inputs.bear、triggers
- `major_events#0`（major_events｜方向 -｜狀態 ok）：美國證券集體訴訟（SDNY，案號 24-cv-06033）進入證據開示階段：集體期間 2023-12-08 至 2024-07-24；2026-03-31 法院對被告駁回動議部分准許、部分駁回；2026-05-08 被告提出答辯狀。訴狀指稱公司對庫存配置、產品表現的說法有誤導，2024-07-24 Bloomberg 報導配置不一致當日股價跌 3.3%。
  - 來源：Kessler Topaz Meltzer & Check — lululemon athletica inc. (NASDAQ: LULU) Securities Fraud Class Action, https://www.ktmc.com/new-cases/lululemon-athletica-inc/（as_of 2026-05-08）｜affects：decision_inputs.bear、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-09-03 公布 FY2026 第二季財報（公司新聞稿網址日期為 2026-09-03），2026-09-04 股價單日跌 17.4%；之後 BFA Law、Levi & Korsinsky 等律所公告展開證券詐欺調查（調查公告，非已提起的新訴訟），主題為成長動能與整體業務健康度的陳述。
  - 來源：BFA Law 新聞稿 via GlobeNewswire 2026-09-23, https://www.globenewswire.com/news-release/2026/09/23/3367258/0/en/lulu-stock-notification-lululemon-is-being-investigated-for-securities-fraud-after-growth-issues-disclosed-investors-are-alerted-to-contact-bfa-law.html ; Levi & Korsinsky 新聞稿 via PRNewswire 2026-09-16, https://www.prnewswire.com/news-releases/lululemon-athletica-inc-lulu-securities-investigation-notice---levi--korsinsky-302880124.html（as_of 2026-09-23）｜affects：decision_inputs.bear、thesis.R、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：美國證券集體訴訟（SDNY，案號 24-cv-06033）：集體期間 2023-12-08 至 2024-07-24；2026-03-31 法院對被告駁回動議部分准許、部分駁回；2026-05-08 被告提出答辯狀；目前為證據開示階段。
  - 來源：Kessler Topaz Meltzer & Check — lululemon athletica inc. (NASDAQ: LULU) Securities Fraud Class Action, https://www.ktmc.com/new-cases/lululemon-athletica-inc/（as_of 2026-05-08）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-09-04 股價單日跌 17.4% 後，BFA Law、Levi & Korsinsky 等律所公告證券詐欺調查（調查公告，所查來源未見新提起的訴狀）。
  - 來源：BFA Law 新聞稿 via GlobeNewswire 2026-09-23, https://www.globenewswire.com/news-release/2026/09/23/3367258/0/en/lulu-stock-notification-lululemon-is-being-investigated-for-securities-fraud-after-growth-issues-disclosed-investors-are-alerted-to-contact-bfa-law.html（as_of 2026-09-23）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":238.0,"bear_5y_price":64.8,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":26.7,"ev5y_pct":25.7,"irr_base_pct":4.8,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":9.39,"pe":10.89,"basis":"FY1（FY2026E，財年至 2027 年 1 月底）共識 EPS 的前瞻本益比；終端倍數同樣套在當年度 EPS 上。共識是否含一次性關稅退款 $0.86 事實表未涵蓋"},"eps":{"bull":[9.8,9.6,11.2,12.6,14.0],"base":[9.4,8.4,9.2,10.0,10.8],"bear":[9.0,6.8,6.5,6.8,7.2]},"pe":{"bull":17,"base":12,"bear":9},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":4},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"valuation_dependent":true}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LULU_Q1_2027_Earnings_Call_20260604.md
- 2026-06-04｜Meghan Frank｜guidance：CFO 給第二季營收財測 $2.45B–$2.475B，年減 2%–3%（減幅在同一句後半）。（原話："revenue in the range of $2.45 billion to $2.475 billion"）
- 2026-06-04｜Meghan Frank｜guidance：第二季 EPS 財測 $1.76–$1.81，去年同期 $3.10。（原話："in the range of $1.76 to $1.81 versus EPS of $3.10"）
- 2026-06-04｜Meghan Frank｜guidance：第二季北美預期低雙位數下滑，美國同區間。（原話："North America to decline in the low double digits"）
- 2026-06-04｜Andre Maestrini｜guidance：Andre 說第二季中國大陸銷售預期中到高十幾% 成長，全年仍約 20%。（原話："we expect sales to increase in the mid- to high teens"）
- 2026-06-04｜Meghan Frank｜guidance：全年營收財測改為 $11.00B–$11.15B（$11B 下緣在前一行），持平至年減 1%。（原話："to $11.15 billion, flat to down 1% relative to 2025"）
- 2026-06-04｜Meghan Frank｜guidance：全年北美改為高個位數下滑；後文說美國略差、加拿大較好。（原話："to be down in the high single digits"）
- 2026-06-04｜Meghan Frank｜guidance：全年中國大陸維持約 20% 成長；Rest of World 維持中十幾% 成長（在後一行）。（原話："revenue in China Mainland to be up approximately 20%"）
- 2026-06-04｜Meghan Frank｜guidance：全年新開自營店改為靠近原 40–45 家區間的低端，最佳化改裝仍約 35 間。（原話："we now expect to be closer to the low end of the"）
- 2026-06-04｜Meghan Frank｜guidance：全年毛利率財測改為年減約 90 bps。（原話："gross margin to decrease approximately 90 basis points"）
- 2026-06-04｜Meghan Frank｜guidance：答分析師時 Meghan 說全年毛利率減幅先前預期是 130 bps（現為 90）。（原話："expectation was 130"）
- 2026-06-04｜Meghan Frank｜guidance：全年 SG&A 費用率財測為年增約 290 bps 的去槓桿。（原話："we now expect deleverage of approximately 290 basis"）
- 2026-06-04｜Meghan Frank｜guidance：全年營業利益率財測改為年減約 380 bps（句首在前一行）。（原話："380 basis points versus last year"）
- 2026-06-04｜Meghan Frank｜guidance：全年 EPS 財測 $10.95–$11.15，2025 年為 $13.26。（原話："in the range of $10.95 to $11.15 versus EPS of $13.26"）
- 2026-06-04｜Meghan Frank｜guidance：口徑說明：EPS 財測不含未來任何股票買回的影響。（原話："excludes the impact of any future share repurchases"）
- 2026-06-04｜Meghan Frank｜guidance：全年存貨金額預期低至中個位數成長，件數略減。（原話："dollar growth to be in the low to mid-single-digit range"）
- 2026-06-04｜Meghan Frank｜guidance：全年關稅對毛利率的毛衝擊約 30 bps，管理層預期幾乎全數可抵銷。（原話："tariffs to have a gross impact of 30 basis points"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：財測假設第二季追加關稅率為 10%，較先前假設的約 20% 下修。（原話："This is down from our prior assumption of approximately 20%"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：下半年財測仍假設追加關稅率 20%。（原話："we continue to assume a 20% incremental rate"）
- 2026-06-04｜Meghan Frank｜guidance：口徑：公司參與退稅流程，但財測不計入 IEEPA 關稅的任何回收。（原話："guidance assumes no recovery of tariffs paid under IEEPA"）
- 2026-06-04｜Meghan Frank｜guidance：答北美問題時 Meghan 說財測沒有計入現行各項措施的任何實質貢獻，措施奏效則區間有上檔空間。（原話："not assuming any meaningful impact from those initiatives"）
- 2026-06-04｜Meghan Frank｜guidance：被問下半年與 90 天前相比：Meghan 說下半年趨勢相對第二季財測是小幅改善。（原話："it's a slight improvement relative to Q2 guide"）
- 2026-06-04｜Meghan Frank｜guidance：Meghan 說北美第二季低雙位數下滑，下半年大致同水準。（原話："and then generally in line in the second half of the"）
- 2026-06-04｜Meghan Frank｜guidance：第二季全價銷售預期整體中個位數下滑。（原話："overall to decrease in the mid-single digits"）
- 2026-06-04｜Meghan Frank｜guidance：全年全價銷售預期持平至略好，並預期逐季推進。（原話："flat to slightly better in terms of full price"）
- 2026-06-04｜Meghan Frank｜margin：第一季毛利率 54.2%，年減 410 bps，其中產品毛利率下降 330 bps。（原話："a 330 basis point decline in overall product margin"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季關稅毛衝擊 280 bps，被企業效率專案約 100 bps 抵銷。（原話："Tariffs had a gross negative impact of 280 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第一季固定成本去槓桿 140 bps，管理層歸因於門市投資與區域組合。（原話："Deleverage on fixed costs was 140 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第一季 SG&A 費用率 42.9%（去年 39.8%），增加 310 bps。（原話："The increase of 310 basis points relates to expenses"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季 SG&A 增加的成分包含去年砍掉、今年加回的費用（門市工時、獎金）。（原話："expenses that we've reduced last year"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第一季 SG&A 增加成分另含委託書之爭（proxy contest）相關成本。（原話："activations and costs related to the proxy contest"）
- 2026-06-04｜Meghan Frank｜margin：第一季營業利益 $277M，營業利益率 11.2%（去年同期 18.5%）。（原話："Operating income for the quarter was $277 million or 11.2%"）
- 2026-06-04｜Meghan Frank｜margin：第二季毛利率財測年減約 410 bps。（原話："margin in Q2 to decrease approximately 410 basis points"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第二季關稅毛衝擊約 150 bps，抵銷項約 100 bps。（原話："negative impact of approximately 150 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第二季折扣（markdowns）預期年增約 50 bps。（原話："markdowns to be up approximately 50 basis points"）
- 2026-06-04｜Meghan Frank｜margin：第二季 SG&A 費用率預期去槓桿 500 bps。（原話："we expect our SG&A rate to deleverage by 500 basis points"）
- 2026-06-04｜Meghan Frank｜margin：口徑：第二季 SG&A 去槓桿部分來自銷售低於原先預期。（原話："associated with lower sales than initially expected"）
- 2026-06-04｜Meghan Frank｜margin：第二季營業利益率財測約 11.6%，去年同期 20.7%。（原話："approximately 11.6% versus 20.7% in Q2 2025"）
- 2026-06-04｜Andre Maestrini｜margin：Andre 說第二季財測納入較高的季節性清倉。（原話："our guidance assumes higher levels of seasonal clearance"）
- 2026-06-04｜Meghan Frank｜margin：被問下半年折扣假設：Meghan 說第二季是全年折扣高點。（原話："So Q2 will be our high-water mark this year"）
- 2026-06-04｜Meghan Frank｜margin：第四季折扣預期低於去年（去年為折扣高水位）；第三季較第二季逐季改善。（原話："expect markdowns in Q4 to be under last year"）
- 2026-06-04｜Meghan Frank｜margin：口徑：Meghan 說她講的 reg price 等同全價（full price）。（原話："reg price, which is the same in my mind as full price"）
- 2026-06-04｜Meghan Frank｜margin：Meghan 說第一季全球 reg price 增加高個位數。（原話："we saw a high single-digit increase in reg price"）
- 2026-06-04｜Andre Maestrini｜margin：Andre 說北美門市已大幅降低折扣活動。（原話："a significant reduction in markdowns"）
- 2026-06-04｜Meghan Frank｜margin：口徑：存貨金額增 2% 但件數減約 4%，差異主要來自較高關稅與匯率。（原話："predominantly to higher tariff rates relative to last year"）
- 2026-06-04｜Meghan Frank｜margin：被問開發週期縮短的成本取捨：Meghan 說不會把更高產品成本和上市時程掛勾，只提空運取捨。（原話："I wouldn't equate any higher product costs"）
- 2026-06-04｜Meghan Frank｜margin：被問中國毛利／營業利益率：Meghan 說中國營業利益率仍有健康擴張，公司繼續加碼投資。（原話："continue to invest behind that business"）
- 2026-06-04｜Meghan Frank｜margin：企業賦能（enterprise enablement）專案的效益預期要一段時間才會浮現。（原話："we expect to see benefits over time"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說第一季收尾與進入第二季時出現若干逆風與銷售趨勢放緩。（原話："headwinds and a moderating sales trend"）
- 2026-06-04｜Meghan Frank｜risk：管理層點出的第一個因素：媒體與社群上的負面評論暴增，影響客流與營收。（原話："spikes of negative commentary in the media and on social"）
- 2026-06-04｜Meghan Frank｜product：管理層點出的第二個因素：並非所有新品上市都達預期。（原話："not all of our product launches have met our expectations"）
- 2026-06-04｜Meghan Frank｜risk：被問社群風波成因：Meghan 列出委託書之爭。（原話："had the proxy contest during that period"）
- 2026-06-04｜Meghan Frank｜risk：被問社群風波成因：Meghan 另列四月中對部分產品成分（composition）的質疑。（原話："we had some questions around the composition of"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說負面報導已退，但趨勢尚未回到風波前水準。（原話："have not yet seen a return to our pre-disruption"）
- 2026-06-04｜Andre Maestrini｜risk：Andre 在中國段說負面評論的暴增現已消退。（原話："spikes of negative commentary, which has now subsided"）
- 2026-06-04｜Meghan Frank｜risk：Meghan 說近期表現正衝擊產品面各個區塊。（原話："recent performance is impacting all areas of our business"）
- 2026-06-04｜Andre Maestrini｜risk：Andre 說中東特許經營受衝突擾動、歐洲與日本觀光疲軟，管理層視為暫時。（原話："We view these as temporary"）
- 2026-06-04｜Meghan Frank｜competition：被問表現相對市場：Meghan 說運動品類趨勢相對穩定，公司自身掉下來。（原話："relative stability in the trend of the athletic space"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說近 6–7 週的落差主要在客流，其次是轉換率。（原話："primarily in traffic and, to a lesser degree, conversion"）
- 2026-06-04｜Meghan Frank｜customer：被問客流下滑是否集中於特定客群：Meghan 說是全客群的廣泛性減少。（原話："We really did see a broad-based traffic reduction"）
- 2026-06-04｜Meghan Frank｜customer：被問受影響區域：Meghan 說跨區域，以中國與美國受影響較大。（原話："predominantly, I would say China was impacted"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說美洲第一季下滑 4%，優於原先低到中個位數下滑的預期。（原話："we did see a negative 4% trend in Q1 overall"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說第一季二、三月最強，趨勢在四月底至五月轉軟。（原話："February and March were our strongest months"）
- 2026-06-04｜Meghan Frank｜customer：第一季北美營收 -3%（固定匯率 -4%），同店銷售下滑 6%。（原話："Comparable sales were down 6%"）
- 2026-06-04｜Andre Maestrini｜customer：Andre 說第一季北美全價銷售相對第四季有序列改善。（原話："sequential improvement in our full price sales"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說第一季美國全價銷售略為負成長，但相對第四季有實質序列改善。（原話："The U.S. was slightly negative"）
- 2026-06-04｜Meghan Frank｜customer：第一季中國大陸營收 +30%（固定匯率 +23%），同店銷售 +13%。（原話："with comparable sales increasing 13%"）
- 2026-06-04｜Meghan Frank｜customer：口徑：農曆新年移入第一季，替中國成長率加了 8 個百分點。（原話："added 8 percentage points to the growth rate"）
- 2026-06-04｜Meghan Frank｜customer：Meghan 說中國業務在負面評論後已有一定程度改善。（原話："We have seen that business improve to a degree"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 對中國全年約 20% 的財測表態維持不變。（原話："We are still holding our guide for the year at 20%"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 說中國全年同店銷售未另行拆分披露。（原話："broken out the full year comp"）
- 2026-06-04｜Meghan Frank｜product：Meghan 說「新瑜珈造型」活動未達預期的營收效果。（原話："new look of yoga campaign didn't drive top line results"）
- 2026-06-04｜Meghan Frank｜product：Meghan 說 Align、Groove 的 away-from-body 款式反應不錯，但未帶動其他品類的光環效應。（原話："the campaign hasn't had the expected halo"）
- 2026-06-04｜Meghan Frank｜product：被問設計檢討：Meghan 說顏色是光環效應不足的一個因素。（原話："think color is an aspect of that"）
- 2026-06-04｜Meghan Frank｜product：追單量今年比去年多 20%。（原話："20% more volume this year relative to last year"）
- 2026-06-04｜Meghan Frank｜product：主線產品開發週期已從 18–24 個月縮短（現為 15–16 個月，見下一行）。（原話："mainline product development process from 18 to 24 months"）
- 2026-06-04｜Meghan Frank｜commitment：管理層正進一步把開發週期縮到 12–14 個月。（原話："working to further reduce it down to 12 to 14 months"）
- 2026-06-04｜Meghan Frank｜product：新品占比目標：全年由去年 23% 拉到 35%（23% 在前一行）。（原話："year to 35% over the course of this year"）
- 2026-06-04｜Meghan Frank｜product：目前新品占比約 30%，會隨季節波動。（原話："Right now, we sit at about 30%"）
- 2026-06-04｜Andre Maestrini｜product：Andre 說北美門市改為較不密集的陳列，SKU 少 15%。（原話："presentation of products featuring 15% fewer SKUs"）
- 2026-06-04｜Andre Maestrini｜product：被問國際市場對新品的接受度：Andre 說核心系列的新色與新版本在國際市場是成長動能。（原話："bringing the core franchise to life with different colors"）
- 2026-06-04｜Meghan Frank｜capital_allocation：第一季買回約 220 萬股，均價 $165。（原話："2.2 million shares at an average price of $165"）
- 2026-06-04｜Meghan Frank｜capital_allocation：買回計畫尚餘約 $10 億額度，管理層說會持續使用。（原話："$1 billion remaining on our share repurchase program"）
- 2026-06-04｜Meghan Frank｜capital_allocation：管理層稱買回是偏好的股東回饋方式。（原話："Share repurchases remain our preferred method"）
- 2026-06-04｜Meghan Frank｜capital_allocation：2026 年買回規模預期與 2025 年相當。（原話："repurchase levels in 2026 to be in line with 2025"）
- 2026-06-04｜Meghan Frank｜capital_allocation：全年資本支出財測 $7.0 億–$7.2 億。（原話："approximately $700 million to $720 million"）
- 2026-06-04｜Meghan Frank｜capital_allocation：被問新店報酬：Meghan 說新店資本回收期 1 年（改裝 2–3 年，在下一行）。（原話："return on capital of 1 year for our new stores"）
- 2026-06-04｜Meghan Frank｜capital_allocation：Meghan 說有幾間新店延到 2027 年開。（原話："We did have a few stores push into '27"）
- 2026-06-04｜Meghan Frank｜capital_allocation：行銷投入提高到占銷售 6%–6.5%（去年 5.6%）；上一行說比去年高約 10%–15%。（原話："in the range of 6% to 6.5% of sales versus last year at"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 承諾下半年品牌活動會更大膽。（原話："You will see us be bolder in the second half of the year"）
- 2026-06-04｜Meghan Frank｜commitment：新任 CEO Heidi O'Neill 預計 9 月加入公司。（原話："welcome incoming CEO, Heidi O'Neill"）
- 2026-06-04｜Meghan Frank｜commitment：被問新 CEO 是否改變現行做法：Meghan 說目標仍是恢復全價健康度。（原話："restoring the full price health of the business"）
- 2026-06-04｜Meghan Frank｜commitment：Meghan 說公司正依現況趨勢調整（pivoting）。（原話："we're pivoting based on current trends"）

### 問答異常語氣（迴避／改口／保留）
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Dana Telsey：營收疲弱有多少來自轉向時尚款？新品占比多少？弱的是核心款還是新款？｜答法：Meghan 改談客流下降、負面評論與部分新品不如預期；核心款與新款沒有拆分，只說近期表現「影響產品面所有區塊」。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Matthew Boss：美洲下滑幅度能否拆成產品設計、品類需求、總經幾塊？五月需求趨勢？｜答法：Meghan 說是「early analysis」，定性歸因客流與負面評論、新品表現；沒有給各因素的量化拆分，五月只說趨勢在四月底至五月轉軟、無五月數字。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Michael Binetti：SKU 精簡的測試門市轉換率或銷售效率有無改善？哪些品類最過多？｜答法：Andre 重述少 15% SKU 與門市陳列邏輯、稱「over time」會累積成效；Meghan 補第一季 reg price 與美國序列改善；未給測試門市的轉換率／效率數字，也未指出哪類 SKU 最過多。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Mark Altschwager：中國全年約 20% 成長中，同店與新店各占多少？｜答法：Meghan 說「haven't broken out the full year comp」，只重述第一季同店 13% 與全年 20% 財測，沒有拆分。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Mark Altschwager：縮到 12–14 個月的卡關點？何時反映在同店？｜答法：Meghan 答技術解鎖需時間，速度效益「will build over time」，未給時程或量化。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Aneesha Sherman：全價銷售何時轉正？第一季 reg price 高個位數增長是不是不含折扣的平均售價？｜答法：Meghan 給第二季全價銷售中個位數下滑、全年持平至略好、「progress throughout the year」，未指明哪一季轉正；ASP 之問只答「reg price 等同 full price」，未確認是 ASP 還是銷售額。
- LULU_Q1_2027_Earnings_Call_20260604.md｜問：Jay Sole：社群風波何時開始、為何結束、有無殘留影響？｜答法：Meghan 說報導「died down and subsided」，但強調尚未回到風波前趨勢、所以下修財測區間；未說明結束原因。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 4 | 4 |
| customer_concentration_credit | found | 2 | 4 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 7 | 4 |
| geo_supply_chain | found | 7 | 4 |
| end_markets | found | 7 | 6 |
| substitute_technology | found | 2 | 4 |
| channel_business_model_shift | found | 2 | 4 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 4 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260516","verdict":"B 觀望（thesis 完整但時機極壞 + CEO 真空）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Americas comp 從衰退恢復至持平至小幅正成長","columns":{"2Y 驗證":"FY26-27 Americas comp 從 -3% → 0% → +2%","5Y 驗證":"FY28-FY30 Americas comp 持平 +1-3%","10Y 驗證":"Americas 占 revenue 從 70% → 55%（國際分子放大）","具體門檻":"FY26 guide Americas -1% 至 -3%；FY27 共識 0%","來源":"FY25 Q4 法說 + sell-side","漂移條件":"連 4 季 comp &lt; -3% → 反轉"}},{"id":"H2","text":"International + China 維持 +20% 增速並成為第二成長曲線","columns":{"2Y 驗證":"FY26-27 international +20-25%","5Y 驗證":"FY28-FY30 international 達 revenue 35-40%","10Y 驗證":"10Y 國際 50%+ revenue","具體門檻":"FY25 +22% / China +29%","來源":"Q4 FY25 法說","漂移條件":"連 2 季 international &lt; +15% → 削弱"}},{"id":"H3","text":"毛利率 / Op margin 在 56% / 19-21% 穩定","columns":{"2Y 驗證":"FY26-27 GM 56%、Op margin 18-20%","5Y 驗證":"FY28-30 規模 leverage 後 op margin 21-23%","10Y 驗證":"10Y 維持高 margin profile","具體門檻":"FY25 GM 56.6%、Op margin 19.9%","來源":"Q4 FY25 法說 + sell-side","漂移條件":"連 4 季 op margin &lt; 17% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Americas brand power 永久喪失（Alo / Vuori 持續搶份）","columns":{"對應":"H1, H3","時間尺度":"🐢 長期 2+ 年","監測指標":"Americas comp 連 4 季、competitor SOM 數據","警戒":"連 8 季 Americas comp &lt; -3% → 砍倉"}},{"id":"R2","text":"新 CEO 上任後 strategy reset 不力或 brand IP 流失","columns":{"對應":"H1, H2","時間尺度":"🔥 中期 4-6 季","監測指標":"CEO 上任時程、首份 strategy update、product 創新 cycle","警戒":"2026 Q4 仍空缺 → 砍倉"}},{"id":"R3","text":"China 增速減速 + 國際擴張遇挫","columns":{"對應":"H2","時間尺度":"🔥 中期","監測指標":"China + international 各國 Rev growth","警戒":"連 2 季 international &lt; +15% → 削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":119.14,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LULU","date":"2026-09-24","schema":"v15.2","contract":"v19","company_name":"lululemon athletica inc."},"oneliner":"北美客流流失、中國第二曲線失速，全年財測年內二度下修，營益率從約兩成往個位數掉（Q3 指引 6.5%）；前瞻 11 倍看似便宜但分母還在下修，等新 CEO 2027 年 3 月首份財測證明營益率守得住 12% 再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/scenario.json","answers":{"q1_business":{"verdict":"賺高收入、以女性為主的消費者買全價運動休閒服的錢，錢卡在品牌熱度這一節：北美占營收 67%、同店 −12%，熱度一退，自營門市與官網的固定成本就反過來吃掉利潤","reasoning":"收錢方式：以自營門市加官網直營為主，全價賣高價運動休閒服；Q2 數位營收約 $0.9B、占 39%，批發與授權併在其他通路，10-K 未見單一客戶占營收 10% 以上。分區：北美 $1,616.8M、占 67%（年減 8%、同店 −12%）；中國大陸 $407.1M、占 17%（報告幣 +4%、固定匯率 −2%、同店 −8%）；其他地區 $391.8M、占 16%（+5%）。品類：女性 −4%、男性約 −1%、配件 −13%，主力 leggings 約 −20%。獲利：Q2 GAAP 毛利率 60.5%、營益率 18.8%，其中一次性 IEEPA 關稅退款 $134.5M 貢獻 560bp；扣掉後毛利率約 54.9%、營益率約 13.2%（去年同期 20.7%）。Q3 指引營益率約 6.5%（去年 17%）。錢卡在品牌熱度：管理層自述主因是客流，而門市面積年增 11%、營收年減 4%，固定成本去槓桿同時壓毛利率（230bp）與費用率（+400bp）。供需持久性：這是公司自身的份額問題，不是景氣——2026-06-04 Q1 法說 CFO 說運動品類趨勢相對穩定、是公司自己掉下來，所以不會隨景氣自然反轉。產業態勢：競爭惡化中，Alo、Vuori 在 2023–24 年各取約 1% 份額，NikeSKIMS 自 2025 年起瞄準同一女性客群；關稅與訴訟是旁邊的結構變數。單點依賴：面料 34% 來自台灣、29% 來自中國大陸，特殊面料短期可能只有單一來源，屬集中度風險，不是護城河。","fact_refs":["f_kpi0_net_revenue_gaap","f_kpi1_comparable_sales_total","f_kpi2_gross_margin_gaap","f_kpi3_gaap_operating_income_op","f_kpi4_operating_margin_ieepa_n","f_kpi8_guidance_q3_fy2026","f_kpi9_guidance_fy2026"],"verdict_values":{"revenue_quality":"中：直營全價為主、無客戶集中，但全價比重在降、季節性清倉加大；Q2 GAAP 獲利有每股 $0.86 來自一次性關稅退款，本業品質比帳面差","unit_econ_note":"門市面積年增 11%、營收年減 4%，單位面積產出在下滑；管理層稱新店一年回本（2026-06-04 Q1 法說），但全公司層的扣退款營業利益年減約 39%，門店層說法得不到公司層數字支持","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"前身是高利潤率品牌成長股，現在是營收衰退、利潤率下台階、激進投資人 Elliott 持股逾 $10 億、新 CEO 剛上任的轉機狀態"},"industry":{"clock_phase":"III","sd_verdict_source":"2026-06-04 Q1 法說 CFO：運動品類趨勢相對穩定、公司自身下滑；2026-09-03 Q2 法說 CFO：各區市場都競爭激烈，澳洲轉向促銷。品類需求沒縮，新品牌大量湧入、促銷增加，屬擴張末段的擁擠期","bargaining":{"up":"成衣約 51 家代工、前五大 47%、最大一家 15%，成衣端議價力尚可；但特殊面料短期只有單一或少數來源、前五大面料商 48%，且與所有供應商都沒有長期合約","down":"直營為主、無單一大客戶，對消費者的議價力完全取決於品牌熱度；目前客流與轉換率雙降、折扣加深，議價力在流失","geo":"成衣 87% 集中在越南、柬埔寨、斯里蘭卡、印尼、孟加拉；面料 34% 台灣、29% 中國大陸。2026 年關稅毛額約 $380M（3 月財測時數字）；IEEPA 已付約 $230M、Q2 收回 $134.5M，餘約 $105M 未計入財測"},"profit_pool_dir":"利潤池從 LULU 流向 Alo、Vuori、Fabletics 與 NikeSKIMS 等新品牌；方向有 2023–24 年交易資料支持，金額事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池金額；唯一的份額證據是 2023–24 年交易資料（Alo、Vuori 各取約 1%），沒有總盤，無法建表；利潤池外流方向已寫在利潤池欄"}}}},"q2_moat":{"verdict":"護城河在縮：執行力與定價力同時往下，趨勢判向下；實質護城河是品牌熱度而不是面料技術，而熱度正在流失","reasoning":"機制：品牌溢價＋技術面料形象＋直營全價通路＋社群活動（SeaWheeze 近 1 萬名跑者、Strava 線上 8.5 萬人）。10-K 自承面料多由供應商開發、未取得專利、可被模仿，所以撐住溢價的是品牌熱度，不是技術。方向：執行力縮減——年內兩度下修全年財測、新品反應被管理層形容為不一致、Q2 折扣年增 70bp 高於原指引的 50bp；定價力縮減——扣退款毛利率年減約 360bp、Q3 毛利率再年減約 250bp，還要靠季節性清倉消化庫存。兩軸同降，判向下。同業對照（TTM）：毛利率 56.1% 高於 NKE 42.9%、低於 ONON 64.8% 與 RL 70.3%；營益率 17.8% 低於 DECK 22.7%，高於 RL 16.4%、ONON 13.8%、NKE 8.2%。但 LULU 的 TTM 含退款與上半年較好的季度，Q2 扣退款單季 13.2% 已低於 ONON。同業 ROIC 事實表未涵蓋，只能用利潤率差代理，差距在收窄。評分：執行 4、定價 6，等級 C。四個持續期檢查點中，決策層級最弱：每一件衣服都是重新選擇，沒有轉換成本。","fact_refs":["f_peer_lulu_gross_margin_pct","f_peer_lulu_operating_margin_pct","f_peer_lulu_fcf_margin_pct","f_peer_nke_gross_margin_pct","f_peer_nke_operating_margin_pct","f_peer_onon_gross_margin_pct","f_peer_onon_operating_margin_pct","f_peer_deck_operating_margin_pct","f_peer_deck_fcf_margin_pct","f_peer_rl_gross_margin_pct","f_peer_rl_operating_margin_pct","f_kpi2_gross_margin_gaap","f_kpi4_operating_margin_ieepa_n"],"verdict_values":{"moat":{"mechanism":"品牌溢價＋技術面料形象＋直營全價通路（數位 39% 加自營門市）＋社群大使與活動；面料無專利、IP 多在供應商手上，實質靠品牌熱度","execution":4,"pricing":6,"grade":"C","trend":"↓","trend_evidence":"執行力縮減：全年財測年內二度下修、Q3 營收中點 $2.305B 對事前共識 $2.53B、主力 leggings 單季約 −20%；定價力縮減：扣退款毛利率年減約 360bp、Q2 折扣年增 70bp、Q3 再年增 60bp 並需季節性清倉","competitor_notes":[{"name":"NKE","strategy_note":"大眾量販打法，TTM 毛利率 42.9%、營益率 8.2%，LULU 扣退款毛利率仍高約 12 個百分點；但 NikeSKIMS 直接切入 LULU 的女性客群，是份額攻擊不是價格攻擊"},{"name":"ONON","strategy_note":"跑鞋起家往服飾延伸，毛利率 64.8% 高於 LULU；營益率 13.8% 已與 LULU Q2 扣退款單季 13.2% 相當，高端運動品牌的溢價正被新進者分走"},{"name":"DECK","strategy_note":"營益率 22.7%、FCF 利潤率 20.2%，是同組獲利最好的高端品牌，顯示高端運動消費仍有品牌賺得到錢，問題在 LULU 自身"},{"name":"RL","strategy_note":"毛利率 70.3% 最高、營益率 16.4%，靠全價銷售撐利潤，是 LULU 想走的保全價路線的參照；差別在 RL 的全價路線有穩定客流支撐，LULU 目前沒有"},{"name":"Alo／Vuori","strategy_note":"未上市、事實表無財務數字；交易資料顯示 2023–24 年各取約 1% 份額，創辦人曾對兩家提供諮詢"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只有毛利率、營益率、FCF 利潤率；以營益率差代理 ROIC 差，LULU 對 ONON、RL 的領先已在扣退款後消失","threats":[{"level":"🟡","text":"Alo、Vuori、Fabletics 以點對點方式分走北美女性客群：交易資料 2023–24 年 Alo、Vuori 各取約 1% 份額；Forbes 2026 年 1 月標題稱 LULU 撞牆、Fabletics 起飛。屬破壞性競爭，機率下限 30%","p":60,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🔴","text":"NikeSKIMS 自 2025 年起挾大廠通路與行銷資源，瞄準被 LULU、Vuori、Alo 拿走的女性消費者，屬生態級攻擊","p":40,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"面料與製程未取得專利、IP 多在供應商手上，特殊面料短期只有單一或少數來源：模仿門檻低，技術差異撐不住溢價","p":50,"evidence_refs":["substitute_technology#1","geo_supply_chain#4","customer_second_source#3"]},{"level":"🟡","text":"創辦人曾對 Alo、Vuori 提供諮詢（公司委託書揭露）；Bloomberg 2026 年 8 月報導把創辦人與 Alo、Vuori 並列為新 CEO 要面對的對手，品牌敘事與人脈外流","p":30,"evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（依過往定性判讀；投入資本事實表未涵蓋）。利益率正在下台階，能維持多久取決於品牌熱度","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多半是同一個消費者，沒有斷點；但這是想要不是需要，延後購買沒有代價。客戶要解決的問題（好穿、好看、能運動）還在，管理層稱瑜珈、皮拉提斯與健康趨勢仍強；變的是解法——需求從緊身 leggings 轉向寬鬆版型，leggings 單季約 −20%、下身整體中個位數衰退"},{"item":"決策層級","level":"🔴","text":"替代性要看每一次購買：沒有合約、沒有資料遷移、沒有轉換成本，每件衣服都是重新選擇。代理變數：門市與官網客流同時下滑、轉換率年減；面料未取得專利；Alo、Vuori、NikeSKIMS、Fabletics 都能在同一次購物決策裡取代"},{"item":"價值鏈分配","level":"🟡","text":"品牌加直營零售這一節拿走大部分價值，下游無單一客戶超過 10%；上游成衣代工分散，但特殊面料集中、無長期合約；關稅這一節在 2026 年拿走約 $380M 毛額。品牌端能留下多少，取決於熱度"},{"item":"社會容忍度","level":"🟡","text":"不是必需品，價格上限由競爭者決定而非政治；但品牌靠健康、安心的形象，社會面已在三處被測試：德州檢察長 2026 年 4 月就 PFAS 發出調查令、消費者集體訴訟指控以關稅為由多收錢、2026 年 6 月長城活動在中國引發反彈並公開道歉。尚未形成法規上限，列中等"}],"roiic":"公司層為負（定性）：面積年增 11%、全年資本支出 $680–700M，但 Q2 扣退款營業利益約 $319M、去年同期 $524M；投入資本口徑事實表未涵蓋，無法給數字","reinvest_rate":"事實表未涵蓋 D&A 與營運資金變動，無法計算；資本支出 $680–700M 對應全年營收 $10.35–10.50B，約 6.5%","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；投入資本、D&A、營運資金變動事實表未涵蓋，只能定性判斷。增量面以面積 +11%、營收 −4%、扣退款營業利益約 −39% 判讀為負"}}}},"q3_growth":{"verdict":"成長跑道中等：北美已進入衰退，第二曲線（中國與其他地區）在 Q2 同時失速，但仍在開新市場、未證實見頂","reasoning":"成長組成：量與價都在負（客流、轉換率雙降；折扣加深），剩下的是開店（全年淨增約 35 家、面積約 +10%）、國際低個位數與回購減股。三年共識 EPS：FY2025 實際 $13.26、FY2026E $9.39、FY2027E $8.78、FY2028E $9.78，年複合約 −9.7%（GAAP，FY2026 含一次性退款）。內生天花板：投入資本與 D&A 事實表未涵蓋，算不出數字；公司層增量報酬為負，內生成長上界暫視為零以下。缺口：共識年複合為負，沒有超出天花板；但 FY2027 到 FY2028 共識 +11% 的回升全靠利潤率回升，歸因為利潤率擴張，不是營收。營運槓桿：Q2 營收年減約 4%、扣退款營業利益年減約 39%，差距遠大於 3 個百分點，列為成長熄火。跑道：滲透率與 TAM 事實表未涵蓋；北美占 67% 已在衰退；中國固定匯率 −2%、全年指引由約 20% 下修為高個位數，其他地區由中雙位數下修為中個位數；但仍在進新市場（2026 年六個新市場、墨西哥年底門市逾 30 家），第二曲線失速但未證實見頂，給中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi8_guidance_q3_fy2026","f_kpi9_guidance_fy2026"],"verdict_values":{"growth":{"driver_mix":"量價皆負：北美客流與轉換率雙降（量）、折扣加深（價）；正貢獻只剩開店（面積約 +10%）、國際低個位數成長與回購減股（Q1 220 萬股、Q2 270 萬股）","runway_years":"事實表未涵蓋滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"共識三年 EPS 年複合約 −9.7%，不存在超出內生天花板的缺口；天花板本身因投入資本與 D&A 事實表未涵蓋而無法計算，公司層增量報酬定性為負","segments":[{"item":"北美","value":"Q2 營收 $1,616.8M、占 67%、年減 8%、同店 −12%；Q3 指引中雙位數衰退，全年低雙位數衰退"},{"item":"中國大陸","value":"Q2 營收 $407.1M、占 17%、報告幣 +4%、固定匯率 −2%、同店 −8%；全年指引由約 20% 下修為高個位數"},{"item":"其他地區","value":"Q2 營收 $391.8M、占 16%、+5%（固定匯率 +6%）；全年指引由中雙位數下修為中個位數"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"text":"Q1 年減 410bp；Q2 扣退款年減約 360bp；Q3 指引再年減約 250bp"},{"item":"核心市占近 12 個月縮減","lit":true,"text":"Q1 法說 CFO 說品類穩定、是公司自己掉；leggings 約 −20%；Alo、Vuori 取得份額"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"消費者訴訟指控以關稅為由漲價，屬原告主張；公司提價幅度事實表未涵蓋，不計"},{"item":"EPS 成長顯著高於營收成長","lit":false,"text":"方向相反，EPS 跌得比營收快"},{"item":"FCF／淨利連 2 年低於 0.75","lit":null,"text":"年度數字事實表未涵蓋；Q2 單季約 0.68（兩邊皆含退款）"},{"item":"SBC／營收高於 5% 且上升","lit":false,"text":"Q2 為 0.9%"},{"item":"TAM 萎縮或被替代","lit":false,"text":"品類內版型轉移，不是需求消失"},{"item":"產業倍數近 3 年系統性下移","lit":null,"text":"同業倍數事實表未涵蓋；公司自身倍數在四個年度端點中最低"},{"item":"維持性資本支出占 FCF 高於 60%","lit":null,"text":"事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"text":"仍在開店，全年淨增約 35 家"}]}}},"q4_capital":{"verdict":"資本配置中偏弱：SBC 很低、股數在減，但回購買在 $120–165，Q2 回購超過當季自由現金流，是在下跌途中動用現金池","reasoning":"現金流：Q2 自算 FCF $225.2M（占營收 9.3%），其中含已收關稅退款 $134.5M，扣掉後約 $91M；Q2 淨利 $329M，單季 FCF／淨利約 0.68（兩邊都含退款）；TTM FCF 利潤率 12.2%。SBC 單季 $21.1M、占營收 0.9%，稀釋很低。現金去向：Q2 回購 $330M（270 萬股、均價 $120），高於當季 FCF，期末現金 $1,389.7M、比年初 $1,807.2M 少 $417.5M；Q1 回購 220 萬股、均價 $165。兩次均價都高於現價 $102，事後看是在下跌途中燒現金。全年資本支出 $680–700M（開店、DC、IT），營收在縮時仍維持面積約 +10%。剩餘回購額度約 $713M，管理層說 2026 年回購與 2025 年相當、回購是偏好的回饋方式；循環信用可用額度 $593.7M。治理：激進投資人 Elliott 持股逾 $10 億；委託書之爭費用進了 SG&A；創辦人曾替對手提供諮詢。近三年現金去向四分、債務到期與回購歷史均價事實表未涵蓋。","fact_refs":["f_kpi6_free_cash_flow","f_kpi7_stock_based_compensation","f_kpi11_share_repurchases","f_kpi5_diluted_eps_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表查無併購事件，不適用"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q1 均價 $165、Q2 均價 $120；以 FY2 共識 EPS $8.78 計，買入盈餘殖利率約 5.3%／7.3%；10 年期公債殖利率事實表未涵蓋，無法判過或不過。兩次均價都高於現價"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 單季 $21.1M、占營收 0.9%；同期回購 270 萬股，淨股數下降，稀釋率低於每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；近三年現金去向四分事實表未涵蓋，只有本季回購 $330M 高於同季 FCF $225.2M、現金較年初少 $417.5M，已寫進理由"}}}},"q5_valuation":{"verdict":"現價要求 FY2027 營益率守住 12–13%、之後每年回升一點；我只信一半，11 倍的便宜建立在還在往下修的分母上，估值只算合理","reasoning":"現價 $102.28 要成立，需要 FY2027 營益率守在 12–13%、之後每年回升一點，FY2030 EPS 回到約 $10.8，再給 12 倍。我只信一半：止跌時點要看新 CEO 2027 年 3 月的首份財測。倍數：FY1 前瞻 10.9 倍、FY2 11.6 倍、trailing 8.5 倍、P/S 1.0、EV/S 1.1，在四個年度端點裡都是最低，但分母有問題：trailing 用 FY2025 高點 $13.26，FY1 可能含一次性退款 $0.86，FY2 比 FY1 還低。利空是否已進賣方模型：9 月 19 日 FY1 共識 $9.39 已低於新指引下緣 $9.48，已進；FY2 $8.78 以 Q2 淨利 $329M ÷ EPS $2.92 回推約 1.13 億股、稅率 30%、營收約 $104 億粗算，約對應 13% 營益率，大致假設持平；我的基本情境 $8.40 更低，因為新 CEO 首份財測傾向一次重設。賣方平均目標 $105.65、中位數 $100，與現價差不到 4%，方向中性；全距 $44–$255、高低約 5.8 倍，市場對終局沒有共識，我把自身報酬估計的信心往下調。情境對稱度看起來偏正，但共識仍在下修、空頭錨每次都往下移，不作進場依據。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"FY2 前瞻本益比（FY2027E，扣掉一次性退款後的第一個乾淨年度）＋五年情境期望值","tier":"美國上市高端運動服飾與鞋類品牌","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數；不跨 tier 找錨，也不從記憶補同業本益比"},"fwd_pe":10.89,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2 前瞻 11.6 倍、FY1 10.9 倍；分母有爭議，不用 trailing。情境加權：多頭 17 倍 × $14.0＝$238（20%）、基本 12 倍 × $10.8≈$130（45%）、空頭 9 倍 × $7.2≈$65（35%），期望值約 $129，五年約 +26%、年化約 4.7%，加上約 4% 回購約 9%，落在中等報酬區，判合理、不判便宜。12 個月：FY2027E 基本 $8.40 × 12 倍≈$101，約 −1%。PEG 不適用：三年共識 EPS 年複合為負。五年分位事實表只有四個年度端點（分位 0），非五年序列，不填","upside_short_pct":-1,"upside_mid_pct":27,"denominator_disputed":true,"denominator_note":"trailing 8.5 倍用的是 FY2025 高點 EPS $13.26，短期回不去；FY1 $9.39 可能含一次性退款 $0.86；FY2 $8.78 低於 FY1 且仍在下修。分母正是市場的爭點，低倍數不能當便宜證據，改以 FY2 前瞻與五年情境期望值定錨"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是太早認定品牌熱度可修；分母還在下修，陷阱風險中度","reasoning":"太悲觀的可能：若北美只是品牌聲量與產品週期的短期失誤，行銷加碼、寬鬆版型新款、追單量 +20%，加上新 CEO 與激進投資人 Elliott 一起推，FY2027 營益率回到 14% 以上，現價只有約 10 倍，賣方低點 $44 不會出現；另有約 $105M 關稅退款未入財測。太樂觀的可能：分母還在往下修——FY1 共識 3 個月下修約 15%、FY2 比 FY1 還低、摩根士丹利分析師預期還有負向修正；管理層在 Q1 法說說過第二季是全年折扣高點、中國全年約 20%，兩件都沒兌現。股價近 26 週跌 35.6%、RSI 43 不在超賣區，週線價格遠在 250 週均線 $296 之下，沒有反轉訊號。衰退十項確認亮兩項（毛利率連季年減、核心份額縮減），FCF／淨利、維持性資本支出、產業倍數三項事實表未涵蓋，陷阱判中度；依據見反證紀錄。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：看起來 11 倍便宜，但分母還在下修"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":9.39,"pe":10.89,"basis":"FY1（FY2026E，財年至 2027 年 1 月底）共識 EPS 的前瞻本益比；終端倍數同樣套在當年度 EPS 上。共識是否含一次性關稅退款 $0.86 事實表未涵蓋"},"eps":{"bull":[9.8,9.6,11.2,12.6,14.0],"base":[9.4,8.4,9.2,10.0,10.8],"bear":[9.0,6.8,6.5,6.8,7.2]},"pe":{"bull":17,"base":12,"bear":9},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":4},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":4},"max_dd":{"lo":-55,"hi":-35,"basis":"起點 $102.28。三個錨：賣方最低目標 $44（約 −57%）；空頭路徑 FY2027 EPS $6.8 × 9 倍約 $61（約 −40%）；若 2027 年 3 月財測再砍、倍數壓到 7–8 倍，約 $48–54（約 −47%～−53%）。取 −35% 到 −55%。近 26 週已跌 35.6%、週線價格遠在 250 週均線 $296 之下，跌深不代表跌完","trigger_time":null},"basis":{"bull":"新 CEO 在 FY2027 內讓北美止跌、寬鬆版型新款接棒、中國聲量恢復；FY2026 另入帳部分剩餘關稅退款；FY2030 營益率回到約 17%、營收年成長約 6%；倍數 17 倍，仍遠低於過去的成長溢價。同業現值倍數事實表未涵蓋，無法做同業對照","base":"FY2026 落在指引下緣附近；FY2027 是新 CEO 重設年，行銷加碼、營益率約 12–13%，EPS 低於共識 $8.78；FY2028 起營收低個位數成長、營益率每年回升 0.5–1 個百分點，FY2030 約 14–15%。EPS 路徑不含未來回購減股，回購另計約 4%／年（自由現金流撐得住的水準，低於 2026 年實際速度）。倍數 12 倍＝成熟、低成長的高端品牌","bear":"品牌熱度持續流失、北美續跌、中國不回升；FY2027 營益率約 10–11% 並停在那裡，EPS $6.5–7.2；倍數 9 倍，接近現在的 trailing 8.5 倍。空頭機率 35%：共識三個月下修約 15%、FY2 低於 FY1、管理層兩次指引失準，不採信品類需求仍強就能保護利潤率"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"北美 Q2 同店 −12%、營收 −8%，Q3 指引中雙位數衰退；主力 leggings 單季約 −20%；Alo、Vuori 在 2023–24 年各取約 1% 份額，NikeSKIMS 2025 年起瞄準同一女性客群；10-K 自承面料未取得專利、可被模仿；2026 年 3 月財測時的報導已點名設計新鮮度不足","assumption":"北美下滑是品牌聲量與產品週期的短期失誤，行銷加碼與新款可以找回客流","consequence":"若是結構性份額流失，營收每年縮、門市固定成本把營益率壓到 10% 以下，EPS 落到 $5–6，市場只給 8 倍，股價約 $45，五年虧五成以上","ruling":"採納為主要風險：以 35% 空頭機率定價，現在不持有。與唯一致命點部分重疊：2027 年 3 月的 FY2027 財測是這個故事第一個可觀察的斷點","watch":"北美季營收年增率、FY2027 財測營益率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","supply_demand_durability#0","end_markets#0","substitute_technology#1"],"fact_refs":["f_kpi1_comparable_sales_total","f_kpi8_guidance_q3_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"要穩住營收，公司同時加碼行銷（2026 年占營收 6–6.5%，去年 5.6%）、面積約 +10%、DC 與 IT 投資，全年資本支出 $680–700M；2026 年關稅毛額約 $380M，2025 年關稅與小額豁免取消已吃掉約 $275M 毛利；回購買在 $120–165；消費者集體訴訟指控公司以關稅為由多收數億美元（原告說法）","assumption":"營收止跌後利潤率會自然回到兩成","consequence":"營收穩了，但營益率停在 13–15%、ROIC 永久下一個台階；行銷與關稅成本變成常態，每股盈餘回不到 FY2025 的 $13.26","ruling":"採納：基本情境只給 FY2030 營益率回到 14–15%、EPS $10.8，不回前高","watch":"SG&A 費用率、扣一次性毛利率、每股自由現金流","evidence_refs":["supply_demand_durability#1","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#6"],"fact_refs":["f_kpi6_free_cash_flow","f_kpi11_share_repurchases"]},{"view":"價格已反映太多","evidence":"現價對應 FY2 共識 11.6 倍，但共識還在下修：FY1 三個月下修約 15%，FY2 $8.78 比 FY1 還低；Wells Fargo 把下半年獲利預估砍約 30%、摩根士丹利分析師預期還有負向修正、BMO 首評表現落後、目標 $70；Q3 EPS 指引對事前共識低約 60%","assumption":"11 倍已經把壞消息價格化","consequence":"若 FY2 再下修到 $7.50，同樣 11–12 倍對應 $83–90，現價還有 12–19% 下檔，便宜只是分母還沒修完","ruling":"採納：分母穩定前，不把低倍數當安全邊際","watch":"FY2 共識 EPS 每月快照","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#5"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"面料 34% 來自台灣、29% 中國大陸；前五大面料商占 48%、最大一家約 20%；特殊面料短期可能只有單一來源；與所有供應商都沒有長期合約","assumption":"供應鏈中斷不會發生，或可快速轉單","consequence":"台海衝突或禁運時技術面料斷供，新品與補貨同時停擺","ruling":"反駁為尾部風險，不放進主情境機率：屬低機率離散事件，但列入觸發清單，發生即清倉","watch":"台海情勢、公司供應商揭露","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","geo_supply_chain#5","customer_second_source#3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 119.14 → 本次 102.28（-14.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=119.14","side_b":"本次 price_at_dd=102.28","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"北美下滑：可修的品牌聲量問題，還是結構性份額流失","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：管理層說主因是客流與品牌聲量，SeaWheeze 等活動互動強、寬鬆版型新款賣得好、追單量 +20%；激進投資人 Elliott 持股逾 $10 億、新 CEO 9 月上任；扣退款毛利率仍約 55%，比 NKE 高十個百分點以上；只要 FY2028 營益率回到 15%，EPS 就回 $10 以上，12 倍是 $120 以上，還有約 $105M 關稅退款未入財測、每年約 4% 回購","side_b":"Q2 行銷加碼後北美趨勢反而更差（Q2 營收 −8%，Q3 指引中雙位數衰退），管理層自承行銷還沒帶動營收、8 月開局偏慢；Q1 法說 CFO 說品類趨勢相對穩定、是公司自己掉下來；主力 leggings −20%；Alo、Vuori 份額上升；年內二度下修全年財測","ruling":"不可調和，採 B 側。依據：若只是聲量問題，行銷加碼後應先看到客流止跌，但北美趨勢在加碼後惡化，方向相反；A 側的回升路徑目前沒有一個數據點支持。現在不持有。綁住結論的約束是北美趨勢與 FY2027 利潤率底部，重啟條件即其否定","evidence_level":"高：公司新聞稿、2026-06-04 與 2026-09-03 兩場法說逐字稿、交易資料","settle_metric":"北美季營收年增率；2027 年 3 月 FY2027 全年營益率指引","if_then":["若 FY2027 營益率指引中點 ≥12% 且 Q4 FY2026 北美營收年減收斂到 8% 以內：重跑研究，結論轉正才建首倉，上限 2%","若 2027 年 3 月 FY2027 EPS 指引中點低於 $7.50：維持不持有，空頭機率上調到 45%，研究改為每半年一次","若股價先跌到 $80 以下但北美數據沒改善：不追、不接，價格先走、證據未到","反向條件：若 Q4 FY2026 北美營收年增轉正且扣一次性毛利率年增，不等三月財測，直接重跑研究"],"evidence_refs":["end_markets#0","capital_markets_pricing#2","competitive_share_entrants#0","supply_demand_durability#0"]},{"axis":"管理層指引可信度","cause":null,"prior_field":null,"side_a":"2026-06-04 Q1 法說：CFO Meghan Frank 說第二季是全年折扣高點、下半年相對第二季小幅改善、北美下半年大致與第二季同水準；Andre Maestrini 說中國第二季中到高十幾成長、全年約 20%","side_b":"2026-09-03 Q2 法說：Q2 折扣年增 70bp（原指引 50bp）、Q3 再 +60bp；北美下半年比 Q2 更慢；中國 Q2 +4%（固定匯率 −2%），全年改為高個位數；其他地區由中雙位數降為中個位數；Q3 營收中點 $2.305B 對事前共識 $2.53B","ruling":"管理層的前瞻說法打折使用：情境不採信回升敘述，只認實際數字；新 CEO 首份財測前，不以指引當進場依據","evidence_level":"高：兩場法說逐字稿、公司新聞稿","settle_metric":"Q3 FY2026 實際對指引（營收 $2.290–2.320B、EPS $0.93–0.98）","if_then":["若 Q3 實際營收低於指引下緣 $2.290B：空頭機率上調 5 個百分點，維持不持有","若 Q3 實際高於指引上緣且 Q4 指引不再下修：指引可信度回升，北美門檻照舊驗證"],"evidence_refs":["end_markets#4","capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"前份國際第二曲線假設與中國風險觸發（減碼條件）","cause":"新證據","prior_field":["H2","R3"],"side_a":"連 2 季 international < +15% → 削弱","side_b":"中國大陸固定匯率營收連 2 季 <0% → 空頭機率上調，若持有則減碼；國際合計 FY2030 占營收 ≥40%","ruling":"前份觸發器已發火，本份不沿用前份判斷：Q2 中國 +4%、其他地區 +5%，Q3 指引兩區 +3–5%，連 2 季低於 +15% 已成定局，前份國際 +20% 的假設判削弱。新門檻改看中國固定匯率是否轉正，因 +15% 在現況已沒有鑑別力","evidence_refs":["end_markets#1","end_markets#4"]},{"axis":"前份北美品牌力門檻（砍倉）改為本份清倉門檻","cause":"新證據","prior_field":["R1","H1"],"side_a":"連 8 季 Americas comp < -3% → 砍倉","side_b":"北美季營收連 3 季年減 ≥10% → 清倉（若持有），未持有則不追","ruling":"舊門檻太鬆：8 季才動作，而 Q1 北美同店 −6%、Q2 −12%、Q3 指引中雙位數營收衰退，惡化速度遠超前份假設；改用新聞稿直接揭露的營收並縮短為 3 季。前份北美同店回到持平的假設判反轉","evidence_refs":["end_markets#0","capital_markets_pricing#2"]},{"axis":"前份 CEO 空缺門檻（砍倉即清倉）退休","cause":"新證據","prior_field":["R2"],"side_a":"2026 Q4 仍空缺 → 砍倉","side_b":"退休；改由唯一致命點追蹤新 CEO 首份 FY2027 財測（EPS 指引中點 <$7.50 則維持不持有、若持有減碼一半）","ruling":"門檻條件不再成立：新 CEO Heidi O'Neill 已於 2026 年 9 月上任，依規定退休並寫明理由。CEO 風險轉成重設幅度風險，併入新的 R2 門檻"},{"axis":"前份利潤率門檻改為本份清倉門檻","cause":"新證據","prior_field":["H3"],"side_a":"連 4 季 op margin < 17% → 反轉","side_b":"FY2027 全年營益率（扣一次性）<10% → 清倉（若持有）；指引中點 ≥12% 才算利潤率假設成立","ruling":"前份利潤率假設實質已反轉：Q1 11.2%、Q2 扣退款 13.2%、Q3 指引 6.5%，已三季低於 17%，Q4 指引再年減約 250bp。17% 在新 CEO 重設期內沒有可達路徑，保留只會讓門檻失去行動意義，降到 12%／10%","evidence_refs":["capital_markets_pricing#1","end_markets#3"]},{"axis":"唯一致命點（Single Thing）首次設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"2027 年 3 月 FY2027 EPS 指引中點 <$7.50：維持不持有，若持有則減碼一半","ruling":"前份格式未要求此欄；本份依數學上最大單一敏感項選 FY2027 EPS（每 $1 EPS 在 12 倍下約等於股價 $12），屬方法變動，不是判斷翻轉"},{"axis":"停損指標與重啟條件首次設定（清倉與重跑研究）","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份停損指標與重啟條件皆未設（空值）","side_b":"停損：北美連 3 季年減 ≥10%、FY2027 營益率 <10%、中國連 2 季負成長、FY2 共識跌破 $7.50 → 清倉或不進場；重啟：北美年減收斂到 5% 以內且 FY2027 營益率指引中點 ≥12%，兩者同時成立","ruling":"前份用風險欄的警戒代替；本份改成獨立清單，各門檻的新舊差異已在上面逐條歸因"},{"axis":"結論等級、護城河趨勢、成長跑道與陷阱風險","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","trap"],"side_a":"前份：結論等級 B、陷阱風險 🟡，護城河趨勢與成長跑道未記","side_b":"本份：結論等級 C、陷阱風險 🟡、護城河趨勢向下、成長跑道中等（🟡）","ruling":"Q2 新證據：北美同店 −12%、中國固定匯率轉負、全年二度下修、主力 leggings −20%；執行與定價兩軸同降，護城河判向下；國際第二曲線失速但未證實見頂，跑道給中等；衰退訊號確認亮兩項，陷阱維持中度","evidence_refs":["end_markets#0","end_markets#1","capital_markets_pricing#0","competitive_share_entrants#0"]},{"axis":"估值結論由 🟠 改為 🟡","cause":"方法變動","prior_field":["val"],"side_a":"前份估值結論 🟠，股價 $119.14","side_b":"本份估值結論 🟡，股價 $102.28","ruling":"前份摘要未留估值推導；本份改以 FY2 前瞻倍數加五年情境期望值定錨，屬方法變動。股價下跌約 14% 與 FY1 共識下修約 15% 大致抵銷，前瞻倍數本身沒有變便宜；改判合理，是因為情境期望值加回購約 9%／年落在中等區，不是因為價格更低"},{"axis":"情境輸出與其他未記欄位","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","archetype","cycle_position"],"side_a":"前份皆為空值","side_b":"本份：情境機率多頭 20／基本 45／空頭 35，最大回撤區間 −35%～−55%，五年價格與報酬由程式從情境輸入算出；公司類型歸為轉機／特殊情境；非循環股，循環位置不適用；定期定額欄不填","ruling":"屬格式與方法補齊，不是判斷翻轉"}],"triggers":[{"n":1,"text":"新 CEO 首份全年財測：FY2027 EPS 指引中點低於 $7.50","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 全年 EPS 指引中點","threshold":"<$7.50","action":"維持不持有，空頭機率上調到 45% 重算；若持有則減碼一半","source_freq":"年度財測（每年 3 月）","date":"2027-03","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#5"]},{"n":2,"text":"北美營收降幅是否收斂","type":"假設驗證","maps_to":"H1","metric":"北美季營收年增率","threshold":"Q4 FY2026 優於 −8%；FY2027 Q2 優於 −5%","action":"兩點都達成且利潤率條件同時成立才重跑研究；未達成則不追","source_freq":"每季財報","date":"2026-12","evidence_refs":["end_markets#0","end_markets#3"]},{"n":3,"text":"FY2027 營益率是否見底","type":"假設驗證","maps_to":"H2","metric":"FY2027 全年營業利益率指引中點（扣一次性）","threshold":"≥12% 為成立；<10% 為反轉","action":"<10% 則清倉（若持有），研究改為每半年一次","source_freq":"年度財測","date":"2027-03","evidence_refs":["capital_markets_pricing#0"]},{"n":4,"text":"北美份額持續流失","type":"風險","maps_to":"R1","metric":"北美季營收年增率","threshold":"連 3 季年減 ≥10%","action":"清倉（若持有）；未持有則不追","source_freq":"每季財報","date":"2027-03","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","capital_markets_pricing#2"]},{"n":5,"text":"中國品牌聲量未恢復","type":"風險","maps_to":"R3","metric":"中國大陸固定匯率營收年增率","threshold":"連 2 季 <0%（Q2 FY2026 為 −2%）","action":"空頭機率上調 5 個百分點；若持有則減碼","source_freq":"每季財報","date":"2026-12","evidence_refs":["end_markets#1","geo_supply_chain#6","end_markets#6"]},{"n":6,"text":"關稅吸收失敗","type":"風險","maps_to":"R4","metric":"毛利率年增減（扣一次性退款）","threshold":"Q4 FY2026 未達管理層所說略高於去年，且 FY2027 Q1 年減 ≥200bp","action":"空頭機率上調 5 個百分點；若持有則減碼","source_freq":"每季財報","date":"2027-03","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","supply_demand_durability#1"]},{"n":7,"text":"PFAS 調查與訴訟升級。受影響營收與審理時程事實表未涵蓋；證券集體訴訟（SDNY 24-cv-06033）在證據開示階段，屬民事集體訴訟；消費者關稅訴訟原告主張多收數億美元","type":"風險","maps_to":"R5","metric":"德州檢察長調查進度、證券集體訴訟集體認證、消費者關稅訴訟","threshold":"調查轉正式提告或他州跟進；集體認證後出現不利和解；任何刑事程序","action":"集體認證加不利和解：若持有減碼一半；出現刑事程序：清倉","source_freq":"事件驅動","date":"2027-03","evidence_refs":["regulatory_antitrust#0","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","reg_tariff_export#6"]},{"n":8,"text":"台海或面料來源中斷","type":"風險","maps_to":"R4","metric":"台海軍事衝突、禁運或公司面料供應中斷公告","threshold":"發生即觸發","action":"清倉（若持有）；未持有則不進場","source_freq":"事件驅動","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":9,"text":"重啟研究條件","type":"估值rearm","maps_to":"H1","metric":"北美季營收年增率＋FY2027 營益率指引中點","threshold":"北美年減 ≤5% 且營益率指引 ≥12%，兩者同時成立","action":"重跑研究，不直接建倉；結論轉正才建首倉，上限 2%","source_freq":"每季財報＋年度財測","date":"2027-03"},{"n":10,"text":"Q3 FY2026 財報後複審","type":"複審日期","maps_to":null,"metric":"Q3 實際對指引（營收 $2.290–2.320B、EPS $0.93–0.98）","threshold":"營收低於 $2.290B 或 Q4 指引再下修","action":"空頭機率上調 5 個百分點，維持不持有、不追","source_freq":"每季財報","date":"2026-12"}],"kill_metrics":[{"metric":"北美季營收年增率","bear_threshold":"連 3 季年減 ≥10%（Q3 FY2026 指引為中雙位數衰退）","window":"FY2026 Q3 至 FY2027 Q1","source":"公司季報新聞稿北美分部營收","last_status":"warning"},{"metric":"FY2027 全年營業利益率（扣一次性）","bear_threshold":"指引中點或實際 <10%","window":"2027-03 財測至 FY2027 年報","source":"公司年度財測與年報","last_status":"unknown"},{"metric":"中國大陸固定匯率營收年增率","bear_threshold":"連 2 季 <0%","window":"FY2026 Q2 至 Q3","source":"公司季報新聞稿","last_status":"warning"},{"metric":"FY2（FY2027）共識 EPS","bear_threshold":"跌破 $7.50","window":"至 2027-03","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"期末現金與回購","bear_threshold":"期末現金 <$1.0B 且單季回購仍高於當季自由現金流","window":"每季","source":"公司季報資產負債表與現金流量表","last_status":"ok"}],"evidence_dismissed":[{"ref":"supply_demand_durability#2","reason":"這是財報公布前的聚合站預覽文，所載第二季共識與全年 EPS 區間 $10.95–11.15 已被 2026-09-03 實際財報與新指引取代；文中中國 +19.5% 的預估與實際 +4% 相差甚遠，屬過時預估，不作判斷依據"}],"action_conditions":{"rearm_trigger":"北美季營收年減收斂到 5% 以內，且 FY2027 全年營益率指引中點 ≥12%；兩者同時成立才重跑研究","exec_line":"現在不持有、不追；價格先跌但北美數據沒改善也不接。重啟條件成立後先重跑研究，結論轉正才建首倉，上限 2%","holding_cap":"若日後建倉，上限 3%（護城河趨勢向下、深回撤風險）"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"北美營收降幅在 FY2027 內收斂：從 Q3 FY2026 指引的中雙位數衰退，回到年減 5% 以內","2y":"FY2027 Q2 北美營收年減 ≤5%、FY2027 Q4 年減 ≤3%","5y":null,"10y":null,"threshold":"北美季營收年增率：Q4 FY2026 優於 −8%、FY2027 Q2 優於 −5%、FY2027 Q4 優於 −3%","source":"公司季報新聞稿北美分部營收；法說 CFO 分區指引","drift_rule":"連 2 季落後門檻路徑 ≥5 個百分點 → 削弱；連 3 季落後 ≥10 個百分點 → 反轉，空頭機率上調"},{"id":"H2","text":"營業利益率在 FY2027 見底、不低於 12%，FY2030 回到 14–15%","2y":"FY2027 全年營益率（扣一次性）≥12%","5y":"FY2030 營益率 14–15%","10y":null,"threshold":"FY2027 指引中點 ≥12%；FY2028 實際 ≥13%","source":"公司年度財測（每年 3 月）與年報","drift_rule":"2 年段：連 2 季單季營益率年減幅擴大 → 削弱；5 年段：TTM 營益率連 4 季低於路徑 ≥5% → 削弱、連 6 季 ≥10% → 反轉"},{"id":"H3","text":"國際（中國大陸＋其他地區）恢復正成長，FY2030 占營收提高到四成以上","2y":"FY2027 中國固定匯率營收回到正成長","5y":"FY2030 國際占營收 ≥40%（Q2 FY2026 為 33%）","10y":null,"threshold":"中國固定匯率營收年增 ≥0%（Q2 FY2026 為 −2%）；其他地區 ≥+5%","source":"公司季報分部營收","drift_rule":"連 4 季國際合計成長低於 +5% → 削弱；連 6 季低於 0% → 反轉"}],"R":[{"id":"R1","text":"北美份額被 Alo、Vuori、NikeSKIMS、Fabletics 永久分走，客流下滑是結構性的","h_ref":"H1","clock":"🔥","threshold":"北美季營收連 3 季年減 ≥10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","end_markets#0","end_markets#6","substitute_technology#0","substitute_technology#1","capital_markets_pricing#2"]},{"id":"R2","text":"新 CEO 上任後一次重設：2027 年 3 月 FY2027 財測大砍","h_ref":"H2","clock":"⚡","threshold":"FY2027 EPS 指引中點 <$7.50","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#5","end_markets#3","end_markets#4"]},{"id":"R3","text":"中國品牌聲量受損延續，第二曲線失速","h_ref":"H3","clock":"🔥","threshold":"中國固定匯率營收連 2 季 <0%","evidence_refs":["end_markets#1","geo_supply_chain#6"]},{"id":"R4","text":"關稅成本吸收失敗，加上台灣與中國大陸面料集中、無長期合約","h_ref":"H2","clock":"🐢","threshold":"扣一次性毛利率自 Q4 FY2026 起連 2 季年減 ≥200bp；或面料供應中斷事件","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","supply_demand_durability#1","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","geo_supply_chain#5","customer_second_source#3"]},{"id":"R5","text":"PFAS 調查與證券、消費者集體訴訟傷到健康安心的品牌形象與現金","h_ref":"H1","clock":"🐢","threshold":"德州調查轉正式提告或他州跟進；證券集體訴訟獲集體認證並出現不利和解","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#6","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]}],"single_thing":{"description":"2027 年 3 月新 CEO Heidi O'Neill 任內第一份全年財測：FY2027 EPS 指引中點是否低於 $7.50","why_fatal":"FY2027 EPS 是估值的最大單一敏感項：共識 $8.78、基本情境 $8.40、空頭 $6.80，每 $1 EPS 在 12 倍下約等於股價 $12。指引中點落到 $7.50 以下，代表營益率要在約 11% 以下待一年以上，止跌時點往後推，股價錨向空頭 9 倍 × $7 靠攏，約 $63","if_happens":"空頭機率由 35% 上調到 45% 以上重算情境；維持不持有，下次複審延到 FY2027 Q2 財報","how_monitor":"2026 年 12 月 Q3 財報看 Q4 指引與北美趨勢；2027 年 3 月年度財報看 FY2027 全年 EPS、營益率與開店指引；FY2 共識若在 3 月前先跌破 $8 是前兆","probability":"35%（12–24 個月）：新任 CEO 首份財測傾向保守，FY1 共識三個月已下修約 15%、摩根士丹利分析師預期還有負向修正；但要跌破 $7.50，營益率得比 Q4 FY2026 指引再低一段，不是基本情境"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":11.65,"peg_fy2":null,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":13.26,"FY2026E":9.39,"FY2027E":8.78,"FY2028E":9.78},"fy_end_month":1,"eps_basis":"GAAP 稀釋 EPS；財年結束於 1 月底或 2 月初（FY2025 止於 2026-02-01）。FY2025A $13.26 取自 2026-09-03 Q2 法說 CFO 原話；FY2026E–FY2028E 為 Koyfin 2026-09-19 快照共識，家數事實表未涵蓋。三年年複合約 −9.7%；FY2026 公司指引含一次性退款每股 $0.86，共識是否含退款事實表未涵蓋"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q3 FY2026 財報與 Q4 指引，新 CEO 上任後第一次財報","impact":"高","watch":"北美營收年減是否在中雙位數以內、Q4 營益率年減約 250bp 是否守住"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與 FY2027 全年財測","impact":"高","watch":"FY2027 EPS 指引中點是否低於 $7.50、營益率是否 ≥12%、開店與面積計畫"},{"date":"2026-11","date_precision":"month","type":"other","event":"天貓雙 11","impact":"中","watch":"中國在不跟促銷的條件下能否守住去年水準"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"剩餘 IEEPA 關稅退款約 $105M 的處理進度","impact":"中","watch":"是否在 Q3 或 Q4 入帳，財測未計入"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"德州檢察長 PFAS 調查與證券集體訴訟進度","impact":"低","watch":"是否轉正式提告、是否獲集體認證"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
