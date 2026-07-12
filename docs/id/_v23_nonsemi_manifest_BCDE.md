# 非半導體 ID v2.3 regen — 視窗 B 工作簿（Waves B / C / D / E）

> 這是**視窗 B**（並行 session）的自足 playbook + 進度表。視窗 A 跑 Wave A 剩餘 + F + G，並擁有 catalog。兩視窗**只寫各自的 report body 檔，零碰撞**。本檔由視窗 A 於 2026-06-21 建立交接。

## 你的範圍：Waves B / C / D / E = 27 篇 + 1 stub

把每篇 legacy v1.x ID 用 industry-analyst v2.3 重生（就地覆蓋 canonical 保留原檔名/原 publish_date + 新增 `_full`）。

### Wave B — finance（5）+ bio（2）
| 批 | 檔（保留原檔名/date） | sub_group | 狀態 |
|---|---|---|---|
| B1 | ID_CardNetworkDuopoly_20260428 | payment_network | ✅ |
| B1 | ID_CobrandCardEcosystem_20260429 | payment_network | ✅ |
| B1 | ID_GlobalBankROE_20260428 | banks | ✅ |
| B2 | ID_StablecoinPayments_20260430 | stablecoin | ✅ |
| B2 | ID_WealthTransfer25Year_20260429 | wealth_mgmt | ✅ |
| B3 | ID_GLP1Master_20260429 | glp1（bio mega） | ✅ |
| B3 | ID_GLP1Treatment_20260428 | glp1（bio mega） | ✅ |

### Wave C — transport（6）
| 批 | 檔 | sub_group | 狀態 |
|---|---|---|---|
| C1 | ID_BoomerTravelSupercycle_20260429 | travel_master | ✅ |
| C1 | ID_HotelChains_20260429 | hotel_lodging | ✅ |
| C1 | ID_LuxuryTravelCruise_20260427 | cruise_luxury_travel | ✅ |
| C2 | ID_OTAandAITravel_20260429 | ota_distribution | ✅ |
| C2 | ID_AirlineLoyaltyRepricing_20260429 | airline | ✅ |
| C2 | ID_CasinoGamingIR_20260429 | casino_gaming | ✅ |

### Wave D — industrial（7→6）+ materials（2）
| 批 | 檔 | sub_group | 狀態 |
|---|---|---|---|
| D1 | ID_DefenseModernization_20260430 **（M1 master ← 吸 DefenseAerospaceUpgrade）** | defense | ✅ |
| D1 | ID_CommercialAerospace_20260427 | commercial_aero | ✅ |
| D1 | ID_RobotaxiAutonomous_20260429 | autonomous_driving | ✅ |
| D2 | ID_HumanoidIndustrialRobotics_20260427 | robotics | ✅ |
| D2 | ID_IndustrialAutomation_20260427 | robotics | ✅ |
| D2 | ID_HeavyMachineryMining_20260427 | heavy_machinery | ✅ |
| D3 | ID_CopperSupercycle_20260428 | industrial_metals | ✅ |
| D3 | ID_AerospaceMetals_20260427 | aerospace_defense_metals | ✅ |
| stub | ID_DefenseAerospaceUpgrade_20260427 → **noindex stub（M1）** | defense | ✅ |

### Wave E — energy（3）+ staples（3）
| 批 | 檔 | sub_group | 狀態 |
|---|---|---|---|
| E1 | ID_NuclearRenaissance_20260430 | nuclear | ✅ |
| E1 | ID_FusionCommercialization_20260505 | nuclear | ✅ |
| E1 | ID_HydrogenFuelCell_20260505 | hydrogen | ✅ |
| E2 | ID_BeverageEnergyDrink_20260428 | beverage（staples） | ✅ |
| E2 | ID_GLP1PackagedFood_20260428 | packaged_food（staples） | ✅ |
| E2 | ID_GLP1RestaurantImpact_20260427 | restaurant_glp1（staples） | ✅ |

## 每篇 pipeline（已驗證，視窗 A 跑了 4 篇）

1. **四軸 WebSearch refresh**：歷史 / 供給 / 需求 / 驗證；承重數字（最新季 ARR/營收/估值、份額、時程、M&A）+ event-type 必當下再驗（<14d）。
2. **先讀模板（每 session 第一輪做一次即可，會 cache）**：
   - golden ref canonical（複製其 `<head>` + 編輯風 CSS + body 7-PART 骨架）：`docs/id/ID_AIComputeCapexCycle_20260611.html`
   - 已完成的非半導體實例（直接照抄結構換內容）：`docs/id/ID_CybersecurityPlatformConsolidation_20260423.html`（canonical）+ `..._full.html`
   - canonical 規格：`.claude/skills/industry-analyst/templates/lean_template.md`
   - _full 規格 + CSS：`.claude/skills/industry-analyst/templates/html_template.md`
3. **rm 舊 v1.5 檔 → Write 新 canonical**（避免 Read 90KB；rm 前確認是目標檔）：
   - 就地覆蓋 `docs/id/ID_{Theme}_{原date}.html`（**保留原檔名 + 原 publish_date**，零斷鏈）。
   - id-meta：保留 theme/mega/sub_group/related_tickers（可更新 role 數字）；`skill_version`→`"v2.3"`、`id_version`→`"v2.0"`；新增 `now_state`/`future_state`/`action`（各 ≤240 字元）；`oneliner` ≤200；`sections_refreshed` 三鍵填 `"2026-06-21"`。head 三 meta：`id-skill-version=v2.3`、`id-publish-date=原date`。
   - masthead 右上日期：`2026年6月21日 · v2.3 改版<br>台北`；colophon：`精煉版 v2.3 · 2026-06-21 改版`。
4. **新增 `_full`**：`docs/id/ID_{Theme}_{原date}_full.html`（9 章 §0–§9，照 html_template.md / 上述實例）；**不放 id-meta、不放 `<meta name="id-*">`**（companion，validator 自動 skip）；可見字 **≥14,000，目標 16k+**（strip tags 後 `len()` 自測）；頂部「⚡ 趕時間？→ 精煉版」連回 canonical。
5. **驗證**：`python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{date}.html`（須 exit 0）+ char caps 自測（oneliner ≤200 / now·next·action ≤240）。
6. **每批跑一次 Sonnet id-review critic**（背景 Agent，model sonnet，operating as id-review，讀 `/Users/ivanchang/.claude/skills/id-review/SKILL.md`，存報告到 `/tmp/`）→ 修 🔴/🟡 → re-validate。
7. **更新本檔狀態**（只改本檔，不碰視窗 A 的 `_v23_nonsemi_manifest.md`）。

### M1 merge（Wave D）：DefenseAerospaceUpgrade → DefenseModernization
- DefenseModernization 寫成 master（把「航太升級週期」當一段吸收進去）。
- DefenseAerospaceUpgrade 轉 **noindex stub**：極簡 HTML、`<meta robots noindex>`、一句話 + 連到 master。**關鍵：stub 不可留 `<meta name="id-skill-version">`，否則 `validate_id_meta.py` 報 missing_block exit 1**（移掉就歸 non_id skip）。stub 範例可參考既有 semi stub：`docs/id/ID_HBM4CustomBaseDie_20260430.html`。

## 寫稿 7 條 lessons（第一版就套，省 critic 來回）
1. **無機成長必揭露**：headline 成長率若被併購灌大，標「報告值 +X%（有機 ~+Y%，含 {標的} $Z 併入）」。
2. **§7 priced-in 必附量化分位 + 來源**：給「EV/S ~Nx 約在 {年}–{年} band 的 ~XX 百分位（來源/自算+資料窗口）」+ 每條分歧現價隱含成長假設（reverse 推導）。
3. **§5 框架逃逸要架橋**：非商品型產業若不用「過剩/平衡/短缺」，加一句對應（如「需求 > 合格供給 = 結構性短缺型，稀缺來自準入門檻非產能」）。
4. **歷史類比必帶量化錨**（年份 + 主角 + 當年數字）。
5. **禁「A 成長快過 B」未對齊口徑**（先確認有機/可比基礎）。
6. **跨期統計釘年份 + 對照當期**：IBM Cost of a Data Breach 等年度數字會更新；breach 均損 / NRR 閾值用「當期實際」校準。
7. **§8 證偽表閾值用 current actual 校準**：bear 閾值若已被當期數字觸發，標「已觸發」+ 釐清「個股 conviction 下調」vs「主題翻空」，falsification 下修到「進一步惡化」。

## 並行協調鐵律（兩視窗共用 working tree）
1. **catalog 一律凍結**：**不要**動 `index.html` / `INDEX.md` / `cat-*.html`、**不要**跑 `build_id_category_pages.py`、**不要 push**。視窗 A 在 semi 視窗 flush+push 後統一做全部 catalog 整合。
2. **只碰自己的檔**：你只 rm/寫 Waves B/C/D/E 的 `ID_*.html` + `_full` + 本檔。**絕不 `git add -A` / `-u`**；要 commit 只 `git add` 你明列的本批檔（push 仍延後）。commit 前 `git status` 確認沒掃到視窗 A / semi 的檔。
3. **manifest 分離**：你只更新本檔（`_v23_nonsemi_manifest_BCDE.md`），視窗 A 用 `_v23_nonsemi_manifest.md`，互不寫對方。
4. 每個 wave 結束時回報進度給用戶。

## Log
- 2026-06-21：視窗 A 建立本工作簿並交接 Waves B/C/D/E。視窗 A 進度：A1 cyber 3/3（body+critic）、A2 DataSecurityBackupConvergence canonical done。semi 視窗 B2 仍 in-flight、catalog 凍結中。
- 2026-06-21（視窗 B）：**Wave B1 完成 3/3** — CardNetworkDuopoly / CobrandCardEcosystem / GlobalBankROE 全部 canonical（lean 7-PART, v2.3, validate exit 0）+ _full（§0–§9, non_id skip, 可見字 14.5k–20.7k）。Sonnet critic 跑完：3 篇皆 THESIS_INTACT、0 🔴、5 🟡 全修（Cobrand §5 框架逃逸架橋 + §4 US GDP 換算 + §7 priced-in 分位收窄；GlobalBank §6 歐日中 P/TBV 估值來源腳注；CardNetwork id-meta tam_note 口徑註）。CJK 全形標點 0 違規。6 檔留 working tree、未 commit/push（catalog 凍結、留視窗 A 統一 flush）。下一步 B2：StablecoinPayments / WealthTransfer25Year。
- 2026-06-21（視窗 B）：**Wave B2 完成 2/2** — StablecoinPayments / WealthTransfer25Year，canonical（v2.3 validate ok）+ _full（可見字 22.5k / 21.2k）。Sonnet critic：2 篇 THESIS_INTACT、0 🔴、6 🟡 全修（Stablecoin id-meta PYUSD 市值釐清 + §7 sell-side consensus 標源 + §5 bull trigger 加 ≤40% 閾值；WealthTransfer $X.XXB(T)→$X.XXT 全表統一含註腳 + §7 basket priced-in 說明 + §2 SCHW 5x 類比加 [T3] 源）。承重 fact 重驗：GENIUS Act = PL 119-27 2025-07-18 簽署（OCC NPR 2026-02-25、2027-01 全面生效）；Cerulli $124T/2048；NTRS-BNY 併購破局。CJK 全形 0 違規、6 檔留 working tree 未 commit。下一步 B3（bio mega）：GLP1Master / GLP1Treatment。
- 2026-06-21（視窗 B）：**Wave B3 完成 2/2（Wave B 全批 7/7 收官）** — GLP1Master / GLP1Treatment，canonical（v2.3 validate ok）+ _full（可見字 17.8k / 23.8k）。承重臨床 fact 大更新：orforglipron 已核准（Foundayo, FDA 2026-04-01）；retatrutide TRIUMPH-1 已讀出 −28.3%（2026-05-21）；LLY Q1 26 M+Z ~$12.8B、FY26 guide $82–85B、已成製藥營收第一；NVO +32% 含 340B 沖回（可比 CER −4%）；CagriSema NDA filed、FDA ~2026-10。Sonnet critic：2 篇 THESIS_INTACT、**2 🔴（Master TRIUMPH-1 在 id-meta/PART VI/bull scenario 殘留「未來 catalyst」標籤，與本文「已讀出」矛盾，共 10 處跨兩檔）全部 reconcile（未讀出→改 TRIUMPH-2/3、已讀出→標 −28.3%）**；5 🟡 修要項（Master stat-grid NVO 口徑、Master _full 補資本週期證據模組、Treatment §0 加 NVO 340B 可比警語、+56%→+55.5% 對齊）；M-4/T-2 priced-in 百分位留作 directional（reverse-implied 邏輯已在）。CJK 全形 0 違規、4 檔留 working tree。下一步 Wave C1（transport）：BoomerTravelSupercycle / HotelChains / LuxuryTravelCruise。
- 2026-06-21（視窗 B）：**Wave C1 完成 3/3** — BoomerTravelSupercycle / HotelChains / LuxuryTravelCruise，canonical（v2.3 validate ok）+ _full（可見字 23.1k / 23.2k / 18.8k）。跨 ID 一致性處理：Boomer 財富移轉更新為 Cerulli $124T/2048（對齊 WealthTransfer25Year）；Hotel MAR royalty +35% / Bonvoy 271M 共品牌基數（vs 283M 總會員）對齊 CobrandCardEcosystem；Cruise berth 瓶頸確認排到 2031–2036（Fincantieri 37/Meyer 9/Chantiers 8）走結構性短缺型框架。Sonnet critic：3 篇 THESIS_INTACT、1 🔴（Boomer RCL FY26 guide $17.10–17.50 過時、與 Cruise SSOT ~$17.30 不一致 → 全部對齊 ~$17.30）、4 🟡 修要項（Hotel 271/283M 區分、Hotel _full §4 bottom-up 補 ~$8–9B 加總 + §7 MAR 27x 百分位、Boomer _full §7 高端旅館 30x+ 百分位）。CJK 全形 0、6 檔留 working tree。下一步 Wave C2（transport）：OTAandAITravel / AirlineLoyaltyRepricing / CasinoGamingIR。
- 2026-06-21（視窗 B）：**Wave C2 完成 3/3（Wave C 全批 6/6 收官）** — OTAandAITravel / AirlineLoyaltyRepricing / CasinoGamingIR，canonical（v2.3 validate ok）+ _full（可見字 21.3k / 17.6k / 17.4k）。大 thesis 更新：OTA「AI 雙重衝擊」翻轉（OpenAI 2026-03 撤 ChatGPT 結帳→下游退潮、上游 Google AI Overview 才是真威脅；TRIP/Viator 併回 thesis 逆轉）；Spirit/SAVE 2026-05-02 全面停飛＝ULCC 終局；MBS 單季 EBITDA 校正為 $788M、Wynn UAE 改口 modest 延遲、新增 Kalshi/Polymarket 預測市場威脅。Sonnet critic：3 篇 THESIS_INTACT、2 🔴（OTA EXPE beneficiary:false 與本文 deep-value long 矛盾 → 改 true+註記；Airline「$8.4B 與兄弟 $8.2B 口徑一致」錯述 → 改為「$8.4B Q4 8-K vs $8.2B 定稿前讀數、差 $0.2B 同合約不同披露時點」）全修；8 🟡 修 3 要項（OTA 代付共識 <5%、Casino TAM $600B 口徑收斂至 ~$80–100B 子集、Kalshi handle ~$2–3B 精確化），其餘 5 條（OTA Google 數據 staleness、Airline DAL fwd PE 標源 / co-brand bottom-up tier、Casino 現倍數 / MGM role）為 sourcing 精度標註、已在文標 [T3]/估，接受為 directional。CJK 全形 0、6 檔留 working tree。下一步 Wave D1（industrial，含 M1 merge）：DefenseModernization（吸 DefenseAerospaceUpgrade→stub）/ CommercialAerospace / RobotaxiAutonomous。
- 2026-06-21（視窗 B）：**Wave D1 完成 3/3 + M1 merge + stub** — DefenseModernization / CommercialAerospace / RobotaxiAutonomous，canonical（v2.3 validate ok）+ _full（可見字 23.0k / 16.2k / 19.7k）。**M1 merge 完成**：DefenseModernization 寫成 master（吸收歐洲主承包結構 alpha strand）、id-meta 加 `absorbed_ids` + sister_ids 移除 DefenseAerospaceUpgrade；DefenseAerospaceUpgrade 轉 noindex stub（無 id-meta/id-skill-version、validator skip non_id、meta-refresh 轉址 master、7.5KB）。承重 fact 大更新：Rheinmetall backlog €135B→€73B（舊值過時校正）、Anduril ~$61B 私募、RTX $271B/NOC $96B record；Airbus 被 Pratt GTF 引擎短缺拖累（thesis 由「Boeing 統治」改「產能爬坡受限、瓶頸在引擎」）、SPR 收購已 2025-12-08 closed；GM Cruise 已退出（~$10B）、Tesla robotaxi 僅 ~20 台、Waymo ~50 萬週訂、Hesai LiDAR $1K→$200 校正。Sonnet critic：3 篇 THESIS_INTACT、0 🔴、5 🟡 全修（Defense absorbed_ids 欄 + _full §5 資本週期替代指標 + §7 估值 band 標源；Aerospace _full §5 資本週期 + §7 售後 band 標源）。CJK 全形 0、7 檔（3 canon + 3 full + stub）留 working tree。下一步 Wave D2（industrial）：HumanoidIndustrialRobotics / IndustrialAutomation / HeavyMachineryMining。
- 2026-06-21（視窗 B）：**Wave D2 完成 3/3** — HumanoidIndustrialRobotics / IndustrialAutomation / HeavyMachineryMining，canonical（v2.3 validate ok）+ _full（可見字 21.4k / 20.5k / 21.7k）。承重 fact 大更新：Nabtesco RV share 校正 60%→~35%、Tesla Optimus ~1,000 自用台、Hyundai Mobis 自製 actuator 垂直整合威脅；HON Aerospace 分拆 2026-06-29 完成（HONA），ROK thesis 反轉（被低估→~36x priced for perfection）、reshoring 降溫（電子 fab capex -44%）、需求雙速；CAT backlog 口徑校正 $51B→$63B 企業總額（backlog≠營收 已標）。Sonnet critic：3 篇 THESIS_INTACT、cornerstone facts 全 CLEAN（critic 逐項驗證）；8「🔴」皆 checklist-depth（V2-5 lean canonical 缺逐 catalyst dual-path / V2-10 資本週期 proxy 缺硬數字 / V2-11 priced-in 缺顯式分位），非事實或 thesis 缺陷。已修高值 4 項：HeavyMach _full §5 資本週期 proxy ③ 由估值倍數改為 capex／折舊 ~1.2–1.4x + ROIC>WACC（方法學修正）；CAT/ROK/6324.T 三處 priced-in 補自身 band 分位（估）。V2-5 dual-path 判定為 lean 格式已由 .monitor fail-path 覆蓋、不重構 PART V；V2-3/V2-4 細節記為 directional。CJK 全形 0、6 檔留 working tree。下一步 Wave D3（materials）：CopperSupercycle / AerospaceMetals。
- 2026-06-21（視窗 B）：**Wave D3 完成 2/2（Wave D 全批 8/8 + stub 收官）** — CopperSupercycle / AerospaceMetals，canonical（v2.3 validate ok）+ _full（可見字 17.9k / 14.9k）。**thesis 大重校**：Copper deficit 框架翻轉——舊「MS 600kt deficit 20 年最嚴」已過時，ICSG 2026 改為 +96kt 全球小幅過剩（關稅囤貨把短缺擠到 ex-US −640kt + 結構性 2030+），銅價 ~$13,530/t LME 史高、Grasberg 復產延到 2027 底、Cobre Panama 待裁；裁決改「結構 INTACT 但即期過剩、進場價敏感」。AerospaceMetals：鈦俄管制校正（美管制 only 2025-09、EU 因 Airbus 依賴拒跟進、客戶自願去風險化非斷崖）、CSTM gigastamping thesis 砍、HWM ~55x priced-in、sister 由 stub 改指 DefenseModernization。Sonnet critic：2 篇 THESIS_INTACT、AerospaceMetals 0 🔴；Copper 2 🔴（footnote 藏空方 2027 數據、選擇性呈現）已修：stat-grid 補 JPM 空 $11.6K + ICSG 2027 +377kt 過剩擴大；另補 SCCO/HWM priced-in 分位。CJK 全形 0、4 檔留 working tree。下一步 Wave E1（energy）：NuclearRenaissance / FusionCommercialization / HydrogenFuelCell。
- 2026-06-21（視窗 B）：**Wave E1 完成 3/3** — NuclearRenaissance / FusionCommercialization / HydrogenFuelCell，canonical（v2.3 validate ok）+ _full（可見字 17.1k / 16.0k / 15.3k）。承重 fact 大更新：Nuclear hyperscaler 13 案 >9.8GW、CCEC（三哩島）重啟提前 2027、鈾長約 $90、SMR/OKLO/NuScale 近零營收確認；Fusion 累積 funding $7.1B→~$10B / ≥53 startup、CFS SPARC Q>1 attempt 2027、ITER $65B+、**tam/cagr 正確 OMIT（pre-revenue）**、funding≠營收≠發電 口徑全程嚴分；Hydrogen 45V 已 Jan-2025 終版（修正「第二批 guidance 將清三家」誤述）、PLUG 累虧 $4B→$8.47B 校正、BE-AWS 100MW 無法證實已移除、Bloom AEP 1GW/$2.65B + Oracle 2.8GW、APD $2.3B 減記。Sonnet critic：Nuclear/Hydrogen THESIS_INTACT、Fusion AT_RISK（1 🔴 AMSC 數字疑誤）→ 查 SEC 確認 AMSC FY26 營收 $299M +34%/淨利 $134M **數字正確但 $134M 主係遞延稅備抵一次性沖回**，已補非營運利潤警語 + FY 標記校正 5 處（Fusion 轉 INTACT）；3 🟡 修（Nuclear MSFT $16B=20yr PPA / Calpine $21.8B 申報口徑 vs $16.4B 股權 caliber 註；Hydrogen _full §8 catalyst 補達成→/落空→雙路徑）。CJK 全形 0、6 檔留 working tree。下一步 Wave E2（staples，最後一批）：BeverageEnergyDrink / GLP1PackagedFood / GLP1RestaurantImpact。
- 2026-06-21（視窗 B）：**Wave E2 完成 3/3（Wave E 全批 6/6 收官 → Waves B/C/D/E 全數完成）** — BeverageEnergyDrink / GLP1PackagedFood / GLP1RestaurantImpact，canonical（v2.3 validate ok）+ _full（可見字 17.9k / 15.9k / 21.1k）。承重 fact 大更新：Beverage CELH 名目 +138% vs 有機 ~+6%（口徑拆分坐實「名目掩蓋有機」）、能量品類過 cycle peak（Monster US −18.7%）、KDP-JDE Peet's $18B + 2026 拆分、**KO 未收 Olipop（舊 thesis 移除）**、PEP-CELH 持股 19%→11% 校正；PackagedFood Cornell 150K（grocery −5.3%/snack −10%/甜點 −6.7~−11%）、value-trap 框架、user 13M→25M；Restaurant SSS 分化（CAVA +9.7% vs WING −8.7%）、operator response 42%、「分散非末日」。三檔跨 ID 對齊 GLP1Master（user 11–13M→25M、Foundayo 2026-04-01）。Sonnet critic：3 篇 THESIS_INTACT、1 🔴（Restaurant Medicare Part D 內文 2027/01 與自身腳注 + 兄弟 ID 的 2026-07 矛盾）已修；跨 ID 一致性 🟡 修（Beverage 2030 user >30M→~25M 對齊、KO organic +5% 補 FY25/Q1 限定、Cornell 甜點 −8.8→−6.7 校正、Restaurant user 口徑 caliber 註）。CJK 全形 0、6 檔留 working tree。
- **2026-06-21 — 🎉 非半導體 ID v2.3 regen Waves B/C/D/E 全數完成：27 篇 canonical + 27 _full + 1 noindex stub（DefenseAerospaceUpgrade）+ 1 M1 merge（DefenseModernization）。全部 validate exit 0、_full 全 non_id skip、char caps 全過、CJK 全形 0 違規、每批 Sonnet critic 過（全 THESIS_INTACT，🔴 全修）。catalog 全程凍結未動、未 push——留視窗 A 統一 flush + catalog 整合。**
