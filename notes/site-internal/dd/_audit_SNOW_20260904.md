## AUDIT: 判斷級🔴 = 2｜資料級🔴 = 2｜🟡 = 11

流程外事後抽查（跨模型冷讀，writer＝Fable／auditor＝Opus）。標的 SNOW，報告日 2026-09-04（v16 dry-run，未上站）。輸入僅三檔：`.dd_build/SNOW_20260904.judgment.json`、`.dd_build/SNOW_20260904.evidence.json`、`.dd_build/SNOW_20260904.text.txt`（另讀同目錄 `SNOW_20260904.scenario.json` 之內嵌值係由 judgment `scenario_ref` 指向，僅作對帳）。未上網、未跑腳本、未動任何既有檔。

---

### ① 競爭惡化——🔴（判斷級 1 之 1）

**接進判斷的部分是完整的。** `coverage.competitive_share_entrants.findings[0..3]`（Databricks 年化 $6.9B／+80% 以上、2025-10 季度超車；ClickHouse $15B；52% 雙平台；SNOW Q2 絕對加速）四條全部落地：judgment `thesis.R[0]`（R1）、`moat.threats[0]`（⛔ 架構替代）、`moat.spread_table[4]`（相對成長列）、`contradictions[1]`（競爭：↓ 還是 →）。`coverage.customer_second_source.findings[1]`（查無任何具名大客戶整組遷移／自建案例）也被正確用作 B 側證據（`contradictions[1].side_b`、正文 §5 護城河趨勢段）。`coverage.customer_concentration_credit` 三條（無單一客戶逾 10%、G2K 790 家占 FY26 營收 43%、無客戶信用風險揭露）進 §3 對下游議價與 §6.H 客戶結構。就「有沒有整軸沒查／查了沒接」而言，本軸 🟢。

**但 R1 的門檻計數是判斷級錯誤。** judgment `triggers[3]`（＝E12 表 #4）與 `moat.threats[0].p` 都寫「連 4 季相對速度差大於 2 倍→升級為趨勢 ↓」，並把現況記為「現約 2.2 倍，**計 1 季**」；`contradictions[6].ruling` 用「前份口徑不同、資料來源不同」把計數重置為 1。可是本輪證據包自己說的是：Databricks「first passed Snowflake in the **October 2025 quarter** and the gap has **widened every quarter since**」（`coverage.competitive_share_entrants.findings[0]`，as_of 2026-06-16），而報告自己在正文 §3／§5 反覆印出 SNOW 產品營收 26%→30%→34%→37% 的四季序列。把證據包的 80%＋對上這四個數字，比值分別約 3.1／2.7／2.4／2.2 倍——**四季皆大於 2 倍**。也就是說「計 1 季」不是保守，是與同一份證據包的敘述相反，且報告從未把這個計數拿去對自己印出的序列驗一次。此事有裁決重量：計數若照證據包落到 4 季，`triggers[3]` 命中→`moat.trend` 由 → 降為 ↓；而 `moat.grade`＝B，`decision_out.audit_rows` row 3（`moat_trend ↓ 且 moat ≤ B → 迴避`）即成立，裁決由「觀望」翻成「迴避」。這是 觀望↔迴避 的分界，不是量的差異。

削弱本項的唯一合理反論（報告未寫出）是：Databricks 的 80%＋是單一時點的媒體引述私人公司數字，不構成可計數的季度序列，故拿它當硬否決閘的分子本身不穩。這個反論成立，但那應該寫在裁決裡，而不是以「計 1 季」的方式默默把閘推遲三季。

### ② 供需 durability——🟢（附 1 條 🟡）

`coverage.supply_demand_durability` 三條 findings 全部進判斷，且**結構 vs 週期兩面都被寫成可裁決的物件**，不是各表一次。A 側（CEO 三動態、Cortex Code 9,100／CoWork 5,800 帳戶）→ `thesis.H[0]`、`contradictions[0].side_a`；B 側（10-K 自承客戶會縮短保留期／縮短合約／auto-suspend，FY2024 成長 70%→38% 前例）→ `thesis.R[2]`（R3）、`contradictions[0].side_b`。

關鍵在於「供給可逆性是否寫進 bear 機率」——**有，而且是明寫的因果**：`contradictions[0].ruling` 寫「Bear 機率 30% 依 searched durability（10-K 自承＋FY24 前例）設定而非 pattern 外推」，`scenario.json` 的 bear.basis 也具體化成 FY2024 型優化週期的營收路徑（20%→8%→4%→3%→3%）與利潤率回落（13%→10%），而非只把機率調高。另加一條 writer 自己找到的機制點：CoCo 的成本管理 skill 已是前十大 skill——「加速工具同時是節流工具」（正文 §11 矛盾一、`thesis.R[2]`），這是把可逆性接回本檔特有機制，不是套模板。`moat.roic_durability.endo_ceiling`＝30% 略低於共識 CAGR，也被拿來當 Bear 30% 的第二個支撐（`moat.roic_durability.formula_note` 末句）。

🟡：`coverage.supply_demand_durability.findings[2]`（Morningstar／第三方指 AI 支出 2025 見頂、2026 放緩）只在正文 §3 得到一句轉述，未進 Bear 的**時點**設定——Bear 路徑第一年仍給 20% 成長、減速從 FY28 才開始，與該 finding 指的 2026 放緩不對帳。不影響裁決（Bear 機率已由 10-K 自承撐住），列可改善。

### ③ 其他結構變數——🟡

逐軸點名 coverage 有料的結構變數落在哪：`substitute_technology`（Iceberg 成事實標準、Polaris 開源、Databend／MotherDuck／Dremio／Trino）四條全進 `thesis.R[1]`（R2，含門檻「產品毛利連 2 年低於 72%」）＋`moat.threats[2]`＋`triggers[1]`，且第二敗局（`premortem.second_failure`：低毛利 AI 推論轉售致估值框架由 DDOG 79x 切到 CFLT 2.8x EV/S）就是這一軸的量化出口——這一項處理得比一般 DD 好。`channel_business_model_shift`（OpenAI／Anthropic 各 $200M、Natoma／Cortex AI Gateway）三條進 `moat.threats[1]`（模型商由下往上）與 `governance.scorecard`。`reg_tariff_export.findings[0]`（Section 232 不涉 SaaS）在正文 §3 有結論句。

**沒有進判斷物的是資料主權這一軸的下游。** `coverage.regulatory_antitrust.findings[2]`（CLOUD Act × Schrems II 結構性衝突，direction −）與 `coverage.geo_supply_chain.findings[1]`（控制平面元資料仍在美國區域，風險分數 21/25，兩份獨立來源）都是 direction「−」的 sourced 發現，卻只到達三個位置：正文 §3 地緣段的敘述、`moat.roic_durability.checkpoints[3]`（社會容忍度仍給 🟢，理由「影響歐盟採購而非定價」）、`premortem.blind_spots[2]`（承認地區營收占比未涵蓋故無法量化）。**`contradictions[]` 15 條無一涉及、`thesis.R[]` 三條無一涉及、`triggers[]` 10 條無一涉及。** 同樣地 `reg_tariff_export.findings[1]`（DOJ EO 14117 大量敏感個資出口規則，direction −）只有 §3 一句。判為 🟡 而非 🔴 的理由：報告有明說為什麼不能量化（缺地區營收拆分），而且社會容忍度 🟢 的推理（合規需求而非價格管制）站得住；但一個帶兩份獨立來源的負向結構變數最終沒有任何一條可監測的觸發器，是覆蓋面上的實質缺口。

### ④ priced-in——🟢

**裁決不是重述市場已知，是與賣方正面對立且說得出分歧在哪一層。** 證據包給的是一面倒的多方定價：`numbers.analyst_price_target_consensus`（財報後 as_of 2026-09-03，51 位均值 $403.27、區間 $110–525、Strong Buy）＋`coverage.capital_markets_pricing.findings[1]`（BTIG／Needham／Raymond James／DA Davidson／Oppenheimer／BofA 全數上修至 $424–475，無一下修）。報告的 1Y 目標價是 `valuation.targets.short_1y`＝$153.5（−56.9%），與賣方中樞差 2.6 倍——這是可被證偽的反向立場，不是共識覆述。

更關鍵的是它把分歧定位到層級而非方向：正文 §11 矛盾三第③點算出「賣方隱含 FY28E 118x 維持 12 個月」（$403.27÷`eps_meta.base_eps_path.FY2028E` $3.41＝118.3x，我覆算相符），結論「分歧在倍數 regime 非成長」。同段第④點把 26 週 +100.88% 拆成「FY27 EPS 上修 1.79→2.35（+31%）vs 價格 $177→$356」，得出約 55% 來自倍數擴張——這是本份報告最有資訊量的一句，且與 `decision_inputs.consensus_rev_3m_pct`＝11.98 的共識上修事實並存不迴避。`contradictions[3]`（錯過成本反向覆核）也如實記錄「2026-07-05 觀望後 +37%」與 FY2 共識 90 天 +11.98% 兩個條件皆命中，依規則只升級為條件式而不翻面。買方最強論證被逐點列出五條再逐點反駁（§11 矛盾三），其中第②點「用未揭露的 AI 收入為溢價辯護＝分母爭議，此便宜論證無效」是正確的方法論拒斥，且沒有反過來拿它去覆寫估值燈（`decision_inputs.val_denominator_disputed`＝false，`audit_rows` row 11.4b-denom 未命中）——處理乾淨。

### ⑤ 覆蓋面——🟡

16 軸 `coverage.*.status` 全數 found；`events.*` 五軸中 clinical_fda／product_recall_warning／sec_investigation_restatement 三軸 status＝none，note 均為「由 major_events 軸查證：無此類事件證據」。**這三軸的 none 理由站得住**：SNOW 是純軟體公司，臨床／FDA 與產品召回在本業無對應路徑；SEC 一項則由 `coverage.major_events.note` 明寫「treated as absence-of-evidence, not confirmed absence」，且 judgment `governance.litigation_note` 忠實轉述為「未查得 SEC 調查或財報重編」而非斷言無事——查無與確無的分界守住了。

findings 未被使用的殘留兩處，皆 🟡：
（a）`coverage.unprofitable_nrr_rule40_band.findings[2]`（同業 NRR 帶：SNOW ~125／DDOG ~120／MDB ~118／CFLT ~114）全篇未用。方向為「＋」（有利本標的），略去屬保守，但這正是 §5 spread_table「NRR 126%」缺的同業對照，判斷上可惜。
（b）`coverage.major_events.findings[4]`（Datavolo、Select Star 兩筆 tuck-in）未進 `governance.scorecard`——金額不重大，可接受。

另有一處是「judgment 有、散文丟失」：`governance.litigation_note` 完整寫了 Patel v. Snowflake（撤案動議截止 2026-06-03、裁定未見）與 2024 撞庫 MDL 3126（160 家以上客戶、5 億人資料、2025-02 達成和解條款），但正文 §9 治理與資本配置整段**沒有任何訴訟段落**（全文 grep：「MDL」0 次、「撞庫」0 次、「外洩」0 次，「集體訴訟」僅 1 次且出現在 §13 末 E12 表 `triggers[8]`）。判斷做了、呈現層掉了，🟡。

### ⑥ 量化模組——🟢（三項皆真算；附 1 條 🟡）

**(i) roic_durability 是真的換尺不是繞過。** `moat.roic_durability.roiic` 誠實宣告標準式失效（FY25→FY26 投入資本 $5.27B→$4.20B，ΔIC 為負，`five_year_financials.balance_sheet.invested_capital` 覆核相符），改用費用化口徑：增量非 GAAP 營業利益率 25%（Δ非 GAAP OI $262M ÷ Δ營收 $1.05B）與 27.7%（Q2 YoY：ΔOI $111M ÷ ΔRev $401M）。我獨立覆算：Q2 FY27 總營收 1,546.8×15.3%＝$236.7M，Q2 FY26＝1,546.8÷1.35×11%＝$126.0M，ΔOI＝$110.7M，ΔRev＝$401M，比值 27.6%——相符。`reinvest_rate` 同樣宣告 (Capex−D&A＋ΔWC＋併購)÷NOPAT 為負，改記研發占營收 40.4%＋S&M 走損益表，FCF 23.9% 為扣除後剩餘。**`endo_ceiling`＝30% 有推導亦有交叉檢查**：NRR 隱含既有客戶擴張 26pp（126−100）＋新客首年約 4pp；`formula_note` 明寫與共識交叉——FY1→FY3 非 GAAP EPS 共識 CAGR 38%（1.94→3.71）與 Base 五年 EPS CAGR 31.2% 皆高於 30% 營收天花板，缺口 8pp 與 1.2pp 歸因營業槓桿（14.5%→26%，增量 27.7% 已實證），並註明 Base 案 re-rate 貢獻為 −21.6%/yr 故非依賴 re-rate，最後把「天花板略超」轉成 Bear 30%。這是 sanity check 做完且處理了結果，不是算完放著。

**(ii) 情境樹價差是實質的 EPS 價差，非只有倍數差。** Bull FY32E EPS $14.93 vs Base $9.12＝**+64%**，Bear $2.10＝−77%。我用 `scenario.json` 的營收路徑與利潤率逐年重建：Base 6.29×1.26×1.21×1.18×1.15×1.13＝$14.70B×26%×0.97÷(378M×1.015^5＝407M)＝$9.11；Bull 6.29 循 34/30/27/24/21% ＝$20.88B×30%×0.97÷407M＝$14.94；Bear 循 20/8/4/3/3%＝$8.99B×10%×0.97÷(378M×1.02^5＝417M)＝$2.09——三條全部對得上，且終端倍數 60／45／18x 各有外部錨（DDOG 現值 79x、MDB trailing 60x、CFLT 併購前 GAAP fwd PE 28.5x 的下緣）。Bear 終端 EPS $2.10 被刻意壓到低於財報前 FY28 共識 $2.71（`contradictions[12].ruling` 明標為方法論趨嚴），是往嚴的方向動。無退化。

**(iii) IRR／EV5y／AR 內部對帳全通。** Base 410.4÷356.47＝+15.13%，五年化＝+2.86%→`decision_inputs.irr_base_pct` 2.9 ✓；Bull 895.8÷356.47＝+151.3%→+20.2%/yr ✓；Bear 37.8÷356.47＝−89.4%→−36.2%/yr ✓。機率加權 0.25×151.3＋0.45×15.1＋0.30×(−89.4)＝+17.80%→`decision_inputs.ev5y_pct` 17.8 ✓，年化 +3.3% ✓。`decision_inputs.asym_ratio` 1.4＝機率加權口徑 (0.25×151.3)÷(0.30×89.4)＝1.41 ✓，且與前份 1.0 的算法一致（覆核 `prior_dd.prior_meta`：0.25×107.5÷0.30×86.3＝1.04）。Base 三分量 1.312×0.7842＝1.0289 亦回到 +2.9% ✓（re-rate 151.69x→45x 五年化＝−21.6% ✓）。

🟡：§10 情境表「股息回購 −1.5%/yr」與「含息合計」欄有重複計——EPS 路徑的股數已內含 1.5%／年淨稀釋（我上面重建時用 407M 即是），再從不含息 IRR 減 1.5% 得 Base +1.4%/yr 屬雙計；且 Bear 案 `scenario.json` basis 自述「淨稀釋 2%/yr」（EPS 路徑確實用 417M）卻在表上同樣顯示 −1.5%/yr。裁決引用的是不含息口徑（2.9%／17.8%／1.4），未受污染，故不升級。

### ⑦ 數字新鮮度——🟡（另含資料級 🔴 兩條，見文末）

**營運指標端乾淨。** `numbers.latest_quarter_kpis.items` 17 項（Q2 FY2027，季末 2026-07-31、公告 2026-09-02）逐項對正文 §8：總營收 1,546.8／產品 1,491.9／非 GAAP OM 15.3%／GAAP OM −17%／FCF 83.8M／SBC 29.5%／NRR 126%／$1M 客戶 828／RPO $9.0B／cRPO +42%／產品毛利 74.7%／G2K 829／Q3 指引 1,588–1,593M 與 15.5%／FY27 指引 6,070M 與 14.5%／adj FCF 23%——全部使用最新值，無一項被更舊的季度替代。財報前共識 EPS 1.94／2.71 每次出現都標「財報前快照」（§4 EPS CAGR 口徑段、§8 共識時效段），並改以指引推導的 FY27E $2.35 為基期，處理正確；`numbers.earnings_recency_note` 要求的「財報後 ≤3 日用 RTH 收盤而非盤後報價」也照做（$356.47 而非盤後 355.50，且 `contradictions[7]` 專門歸因前份的 $369.89→$356.47）。

未標 as-of 的第三方／同業數字集中在以下，皆 🟡：（a）`peer_valuation_multiples.DDOG` as_of 2026-08-12 在 §5.F 未標（同段 MDB 的 2026-07-03 有標）；（b）`coverage.customer_concentration_credit.findings[0]` 的「無單一客戶逾 10%」as_of 2025-10-31（10-Q），正文 §3／§6.H 寫成「10-Q 揭露」不帶日期，而證據包另有更新的 FY2026 10-K（`geo_supply_chain.findings[0]`，2026-03-20 申報）可用；（c）`numbers.roic_gross_margin_history_web.roic_as_of`＝「2026-01（FY2026 年報口徑）」，正文 §6.D／§5.R 卻把 −19.06% 稱作「現值」，且 WACC 17.5% 全篇未標來源；（d）ClickHouse $15B 的 as_of 2026-01 在 judgment `thesis.R[0]` 有、正文 §5 威脅段落掉；（e）`decision_out.audit_rows` row 5 命中所依的「4 週漂移 > +10%」在證據包無對應欄位（`numbers.momentum_26w` 只有 13w/26w，且 `rsi14`＝66.17 並不過 70、`rsi14_usable`＝false），該輸入不可覆核——所幸反動能閘另有兩條可覆核依據（距 52 週高點 0.00%、`qc24_intraday_flags.shooting_star` 7.3%），閘不因此鬆動。

### ⑧ 散文一致性——🟡

**裁決層前後一致，無矛盾。** `decision_out.verdict`／`role`／`row_hit`（觀望／追蹤／row 8）與 §1 開頭、§13、§14、`exec_line`、`oneliner` 全部同向同數：$356.47、151.7x、104.5x、IRR +2.9%、EV +17.8%、AR 1.4、Max DD −65%～−90%、rearm $239。散文沒有出現判斷物以外的關鍵數字：$10M 客戶 65 家（`moat.roic_durability.checkpoints[1]`）、G2K 平均年支出 $2.3M（`industry.tam_table`）、330 項 GA（`moat.trend_evidence`）、遞延收入單季認列 $988.7M 與 DSO 93→101 天（`quality.ccc`）、2021 高點 $405（`premortem.max_dd.trigger_time`）、Q4 FY26 裁員約 200 人（`governance.scorecard`）——逐一回得去。區間也沒有被講成單點：Q3 指引 $1,588–1,593M、Max DD −65%～−90%、AI 收入 $300–500M（且明標為買方論證的假設而非事實）、目標價全距 $110–525 均保留區間。

殘留三處 🟡：（a）`decision_inputs.market_wrong_reason_given`＝false，但 §11 矛盾三實際給出了具體的「市場錯在倍數 regime（賣方隱含 FY28E 118x 維持 12 個月）」——機器欄與散文不符；因 `valuation_dependent`＝false，`audit_rows` row 7a 不命中，無裁決後果，但下游若讀機器欄會讀反。（b）附錄 A 表頭「品質分（護城河/成長/財務）｜7.3/8.0/7.7」中的 7.7＝`appendix_a.quality_score`，而同段正文自述「品質分＝(護城河 7.3＋成長持久性 8.0)÷2＝7.7」——它是綜合分不是財務分，表頭標籤與值不對應。（c）§3 TAM 表的「G2K 平均年支出 $2.3M」用產品營收 $4,446M×43%÷829 家推得，但 43% 這個口徑在 `coverage.customer_concentration_credit.findings[1]` 對應的是 **790 家**與**總營收**（FY26 $4.68B）——分子分母各換了一次，正確值約 $2.5M。數量級無誤，不影響「錢包滲透低於 20%」的結論。

---

### 資料級 🔴（不計入判斷級）

**1. 「52% 的 SNOW 客戶同時使用 Databricks」——來源與時效都撐不住它的承重。** 出處 `coverage.competitive_share_entrants.findings[2]` 與 `coverage.customer_second_source.findings[0]`，來源為 PitchGrade Research（內容農場級二手來源，非 filing、非一手券商、非公司揭露），`as_of` 僅「2025」——最舊可達 20 個月。這個數字在正文出現 14 次，且是承重件：`thesis.R[0]`（R1）主文、`moat.threats[0]`（⛔ 架構替代）、`thesis.H[2]`（H3）的 2Y 驗證點「雙平台滲透率（2025 年 52%）不再上升」、`contradictions[1]` 兩側、§3 對下游議價、§6.H 客戶結構。散文全數以現在式呈現（「52% 客戶同時用 Databricks」），**未標 as-of、未標信心度、未標來源層級**——同一份報告對 `unprofitable_nrr_rule40_band.findings[2]` 的同業 NRR 帶就因「secondary aggregator」而降級不用，兩把尺不一致。

**2. EV 與 EPS 的股數口徑不一致，`growth-adjusted EV/S` 這把尺的分子被系統性低估。** `valuation.val_light_derivation` 的 EV $122.0B＝市值 $123.55B −現金投資 $4.3B ＋可轉債 $2.74B；市值取自 `numbers.valuation_multiples.market_cap_usd`＝123,552,505,856，對現價 $356.47 隱含股數約 346.6M（與 `book_value_per_share` 5.596 × ~343M 相符，屬基本股數口徑）。但同一份報告所有 EPS 都用 378M 非 GAAP 稀釋股數（`scenario.json` 起始 EPS 推導、`eps_meta.base_eps_path`、§4 EPS CAGR 口徑段）。同口徑重算：378M×$356.47＝市值 $134.7B、EV $133.1B、÷FY27E 總營收 $6.29B＝**21.2x**（非 19.4x），÷成長 36%＝**0.59**（非 0.54）。方向對 writer 自己的結論是保守的（讓估值看起來更便宜），且該尺本來就判 🟡、最終燈由 EV/S 自身分位 95.9%（來自 `valuation_history.trailing.ev_s` 的一致 yfinance 序列，未受影響）決定，故不改裁決；但這是量化模組輸入的內部不一致，且 §10 把「市值 $123.55B」與 FY28E EPS $3.41 並列使用時沒有任何口徑註記。

---

### 裁決方向

**同意「觀望・追蹤」，且同意 row 8（估值主因）是正確的命中路徑。** 生意面本季確實是三年最好的一季且方向一致（產品營收 +37% 連三季加速、NRR 126% 止跌、非 GAAP OM +4.3pp、cRPO +42% 連四季加速、$1M 客戶 +27%），沒有 thesis 級失敗證據可以支撐「迴避」；而 Base 案在**沿用公司自己的 Investor Day $10B 路線圖、利潤率一路推到 26%** 的前提下，五年不含息 IRR 只有 +2.9%/yr、AR 1.4，這個結果我獨立覆算成立（見 ⑥(iii)），意味著即使公司照自己的劇本演完，現價買進的報酬仍劣於現金以外的任何合理替代——這正是「唯一約束是價格、不是生意」的定義，也正是 觀望 而非 迴避 的位置。條件式升級被擋下也是對的，且是被兩個獨立條件擋下而非一個：26 週 +100.88% 落 100–150% 邊界帶（`audit_rows` row 8a 的 input_gap 誠實記錄腳本不放行），以及反動能閘中兩條可覆核事實（距 52 週高點 0.00%、9/3 上影線 7.3%）——不是靠那條無法覆核的「4 週漂移 >10%」單腳站立。rearm 條件（FY28E ≤70x 約 $239 **且** 產品營收 YoY ≥30%、NRR ≥122%）帶 AND 條件防接刀，方向正確。

**唯一保留**：這個「觀望」與「迴避」的距離比報告呈現的近。差別只在 `moat.trend` 給 → 還是 ↓，而 → 之所以成立，靠的是把 R1 的相對速度差計數重置為「1 季」（見 ①）；若照本輪證據包自己的敘述（2025-10 起每季拉大）與報告自己印出的四季序列計，該閘已在門上。我不會因此改判——把媒體引述的私人公司單點成長率當作硬否決閘的分子，證據等級不足以支撐 迴避 這種等級的裁決——但這一點應該寫成裁決的一部分（「閘為何不啟用」），而不是以計數口徑的方式默默推遲三季。
