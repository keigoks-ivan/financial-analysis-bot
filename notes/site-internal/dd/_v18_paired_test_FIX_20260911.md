# v18 受控成對驗證：FIX（爭議檔，同證據包、同逐字稿、只換規則）

2026-09-11，獨立審查者（未參與寫 v18 規則、未跑任何模型、未 commit／push）。

- **A＝舊規則**：`.dd_build/runs/FIX_20260911_A/`，worktree HEAD `77aec95a8`（**WP-D／WP-E 已在內、v18 六問骨架尚未進**）。harness 為 WP-G 之前：J2 因 `scenario_ref` 相對路徑被解析成重複目錄而略過、無 J6、無 `val_denominator_note` 檢查。
- **B＝新規則**：`.dd_build/runs/FIX_20260911/`，HEAD `0e2a6c973`（v18 基準版＋WP-F 陣列形狀＋WP-G）。harness 含 J2 真跑、J6、`val_denominator_note` FAIL 檢查。
- 控制：`evidence.json`／`digest.json` 兩邊 SHA-256 完全相同（`7a598aa5…`／`fef7f195…`），兩份 judge bundle 都含 `FIX_Q2_2026_Earnings_Call_20260724` 全文（各 1 處命中）。judge bundle 203,429 vs 201,129 bytes（−1.1%）。`--no-delta`，只跑 judge＋gate，不發布。
- 基準參照：`.dd_build/runs/FIX_20260906/`（前一份實跑，舊規則、當時同一份證據包）。

---

## 結論先行

| 問題 | 判定 |
|---|---|
| kill (a)：漏掉關鍵反證 | **不觸發**。13 條 `direction=-` finding 兩邊 100% 有處置；A 12 引用＋1 不採納，B 13 全引用。B 引用的 finding id 反而更多（23 vs 15） |
| kill (a)：漏掉承重數字／行動條件 | **觸發，1 例（形式上成立）**。`kill_metrics[]` 裡對應唯一致命點的那條指標（「模組化客戶多年承諾｜任一家取消或延後」）在 B 被換成「共識 EPS 修正 90 天下修 ≥10%」，**且沒有任何 `contradictions[]` 條目歸因**。這正是 WP-G 第 2 件措辭想擋的形狀——措辭寫的是 `rearm_trigger`／`triggers[]`／`decision_inputs`，B 在這三處都合規了，卻從 `kill_metrics[]` 溜掉。另有一例白話層損失見下 |
| kill (b)：裁決分歧 | **不觸發**。觀望／追蹤／row 8／signal B／val 🔴／ma ✅／runway 🟡 全同 |
| 成本與耗時改善 | **幾乎沒有**。乾淨輪對乾淨輪 $11.17→$10.37（−7.2%），含修補口徑 $12.19→$10.37（−15%），牆鐘 1,762s→1,643s（−6.8%）。**TXN 那次省下的 51% 幾乎全部來自 WP-D 規則精簡，而 WP-D 已經在 A 裡面**——v18 六問骨架本身沒省 |
| 六問是否都有實質回答 | 6/6 有證據到結論，`reasoning` 六個承重模組都有算式或機制推導。**這是 B 最紮實的一面** |
| 閘 | A 🔴1／🟡2（修補後 PASS）→ B 🔴0／🟡3。精簡未新增判斷級 🔴 |
| EV5y −1.6 → +13.3 | **不是規則直接造成，但也不是純跑次噪音**：約三分之二（+9.6pp）來自情境樹終端年由 FY2030 移到 FY2031（口徑選擇），約三分之一（+5.3pp）來自同年 EPS 路徑上修淨掉終端倍數下修 |

**一次比較只是訊號。** 這是第二檔（n=2，一乾淨 TXN、一爭議 FIX），仍不能證明普遍不降品質。

---

## 一、EV5y −1.6% → +13.3% 是哪裡來的

### 1.1 情境樹三支並排

| 欄位 | 0906（舊規則基準） | A（舊規則） | B（新規則） |
|---|---|---|---|
| `start.eps` ／ `start.pe` | TTM 40.58 ／ 39.68x | TTM 40.58 ／ 39.68x | **FY2026E 共識 49.01 ／ 32.86x** |
| `start.basis` | trailing 口徑 | trailing 口徑 | **FY2026E 共識 GAAP（三季近乎已實現）** |
| `terminal_label` | FY2030E | FY2030E | **FY2031E** |
| Bull EPS 路徑 | 50→63→80→92→105 | 50.5→64→78→86→95 | 63→78→92→105→**118** |
| Base EPS 路徑 | 49→59→68→72→75 | 49.5→59→68→70→74 | 59→72→77→82→**88** |
| Bear EPS 路徑 | 47→54→42→36→38 | 47→50→42→38→42 | 52→46→40→42→**45** |
| 終端倍數 Bull／Base／Bear | 26 ／ 22 ／ 15 | 26 ／ 23 ／ 16 | 25 ／ 22 ／ 16 |
| 機率 Bull／Base／Bear | 25／45／30 | 25／45／30 | 25／45／30 |
| Bull 五年價 | 2,730 | 2,470 | 2,950 |
| Base 五年價 | 1,650 | 1,702 | 1,936 |
| Bear 五年價 | 570 | 672 | 720 |
| `second_stage` | null | 8% ／ 4% | 10% ／ 6% |
| `peer_max_fpe` | — | — | 24（新填，`dd_scenario.py` 會用它警戒 Bull 倍數） |
| **`ev5y_pct`／`irr_base_pct`／`asym_ratio`** | −0.9／0.5／0.9 | −1.6／1.1／0.8 | **+13.3／3.8／1.3** |

### 1.2 逐項歸因（機率權重下的貢獻，總差 14.87pp）

| 來源 | 貢獻 | 是規則還是跑次 |
|---|---|---|
| **終端年由 FY2030 移到 FY2031**（多一年複利） | **+9.62pp** | 口徑選擇。把 B 的樹截在 FY2030（Bull 105×25、Base 82×22、Bear 42×16）重算，EV＝**+3.7%** 而非 +13.3% |
| 同年（FY2030）EPS 路徑上修：Bull 95→105、Base 74→82、Bear 42→42 | +8.79pp | 跑次／判斷差。Bear 完全同值，差異全在 Bull／Base |
| 終端倍數下修：Bull 26→25、Base 23→22、Bear 16→16 | −3.55pp | 判斷差（往保守方向） |
| 合計 | +14.87pp | |

Base 年化同理：A 1,702／1,610.34 五年＝**1.11%／年**；B 1,936／1,610.34＝**3.75%／年**。兩邊都是「Base 幾乎不賺」，只是 B 的「幾乎不賺」是 4%、A 的是 1%。

### 1.3 這是不是規則造成的？

**不是規則明文要求的。** 情境樹年期硬規則三條（①表頭終端年＝主時距終端年 ②終端倍數 EPS 分母年期與現價倍數同源 ③終端倍數必附 ≥1 同業現值 comp）在 A、B 兩版**逐字相同**，v18 一字未改。

**但也不是純噪音。** 兩件事把 B 推向 forward 口徑：

1. **WP-G 新增的 `val_denominator_note`（2026-09-11）是 FAIL 級檢查**，強制判斷者交代「所選分母（FY2026E／FY2027E／forward）為何可用」。B 交出的原文是：「分母用 FY2026E 共識 $49.01（三季近乎已實現）；trailing 窗因 FY25→FY26 一次性跳升 70% 受污染，PEG 分母改用 FY26→FY28 前瞻 CAGR 22.75%。分母本身無爭議，爭議在 FY28 之後的成長率，已由情境樹處理」。一旦把估值分母正式定在 FY2026E，情境樹起點跟著搬到 FY2026E，硬規則②（終端分母與現價倍數同源）就把終端推到 FY2031。
2. **A／0906 兩次獨立的舊規則跑次都落在 FY2030 起點 TTM**，B 是唯一一次落在 FY2031。兩比一，很難只用跑次變異解釋。

**哪一邊比較對？** 今天是 2026-09-11、FY 年底 12 月。從現在起算五年落在 2031 年秋，**B 的 FY2031 終端在年期上比較誠實**；A 的 FY2030 只距今 4.3 年卻叫「五年期望報酬」。反過來，A 的 trailing 起點在「現價倍數同源」這條上比較乾淨（現價÷trailing PE 是可觀測的，FY2026E 是估計值）。**兩邊各對一半，但這個選擇值 15pp 的 EV，不能繼續留給判斷者自由心證。**

### 1.4 這件事為什麼對持有人重要

裁決沒變（兩邊都是 row 8 觀望／追蹤），但 `ev5y_pct` 是 dd-meta 直讀欄，會流進 `/research/` DD 組合快照、`dd-screener/latest.json`、picks／engine 的聚合視圖。**同一份證據、同一天、同一個裁決，聚合層看到的是「五年期望 −1.6%」還是「+13.3%」，差別是這檔在名單上長什麼樣。**

另外附帶差異（同樣是 dd-meta 直讀）：

| dd-meta 欄 | A | B | 差異來源 |
|---|---|---|---|
| `peg` | **0.90** | **1.44** | A 用 FY2025A→FY2028E CAGR 36.7% 當分母，B 用 FY2026E→FY2028E 前瞻 22.75%。**B 的分母才合規**（分母窗口硬規則：基期含一次性效應→改前瞻錨定；FY26 EPS 跳升 70% 正是一次性）。A 自己也算了 1.45 那一版，只是把 0.90 寫進機器欄 |
| `peg_fy2`（附錄 A） | 0.73 | 1.18 | 同上 |
| `upside_short_pct`／`upside_mid_pct` | −20.9／−2.8 | −14.8／+4.6 | 合理本益比 26x vs 28x |
| `moat_trend` | ↑ | **→** | B 明寫理由：執行面仍擴大、定價面 2–3 年後被第二供應商稀釋，取對論點更關鍵的定價面 |
| `trap` | 🟡 | **🟢** | B 判非陷阱（「陷阱定義的便宜假象不適用」），把那盞衰退燈丟給反證第二視角處理 |
| `max_dd.lo`／`hi`／`path_risk` | −55／−35／🔴 | −56／−30／🟡 | 見 §6 |

`peg` 0.90→1.44 是**「便宜」變「合理」**的跨檔位變動，且是 B 對；`trap` 🟡→🟢 與 `path_risk` 🔴→🟡 是**兩盞警示燈被熄掉**，理由寫得出來但方向一致偏樂觀。這三欄一起看，B 在機器欄上比 A 更樂觀，儘管 B 在散文裡對護城河更保守（↑→→）。**這個不一致本身值得持有人看一眼。**

---

## 二、關鍵反證逐條對帳

### 2.1 J1 機械層：13 條 `direction=-` finding 的處置（Codex 要求的清單）

| # | finding | 摘要 | A 落在哪 | B 落在哪 | 判 |
|---|---|---|---|---|---|
| 1 | `customer_second_source#1` | 資料中心占 Q1 營收 56%，客戶高度集中 | threats[1]／blind_spots[1]／R2／trig 4 | blind_spots[0]／R1／trig 4 | 保留 |
| 2 | `customer_second_source#2` | 業主自採長交期設備（OFE）繞過承包商設備毛利 | threats[0]／blind_spots[1]／R2／trig 4 | contradictions[2]／threats[0]／blind_spots[1]／R4／trig 6 | 保留（B 多一處歸因） |
| 3 | `customer_concentration_credit#0` | 科技客戶由約 31% 升至 58.7% | blind_spots[0]／R1／R2／trig 3 | blind_spots[0]／R1／trig 4 | 保留 |
| 4 | `customer_concentration_credit#1` | 10-K 明列客戶集中為重大風險 | threats[1]／blind_spots[1]／R2 | blind_spots[0]／R1／trig 4 | 保留 |
| 5 | `customer_concentration_credit#3` | Amazon 2026 年 FCF 轉負 | blind_spots[0]／R1／trig 3 | blind_spots[0]／R1／trig 4 | 保留 |
| 6 | `supply_demand_durability#4` | 技術工短缺限制訂單轉營收 | threats[2]／blind_spots[2]／R4／trig 2 | threats[3]／blind_spots[1]／R2／trig 5 | 保留（B 升格為獨立 R2） |
| 7 | `reg_tariff_export#0` | 10-K：材料占專案成本 40–45%、貿易政策風險 | threats[3]／blind_spots[2]／R4／trig 2 | blind_spots[1]／R3／trig 5 | 保留 |
| 8 | `geo_supply_chain#0` | 長交期機電設備依賴進口 | threats[3]／blind_spots[2]／R4／trig 7 | blind_spots[4]／R3／trig 5 | 保留 |
| 9 | `geo_supply_chain#1` | 變壓器交期最長五年、近半 2026 年案延後 | threats[3]／blind_spots[2]／R4／trig 7 | blind_spots[4]／R3／trig 5 | 保留 |
| 10 | `geo_supply_chain#2` | 銅 50% 232 關稅 | threats[3]／blind_spots[2]／blind_spots[3]／R4 | blind_spots[1]／R3／trig 5 | 保留（B 未提「銅」二字，見 §3） |
| 11 | `capital_markets_pricing#4` | 管理層預告 H2／Q4 因基期減速 | contradictions[0][2][3][5]／blind_spots | blind_spots[0]／R1／trig 4 | 保留 |
| 12 | `major_events#2` | ERISA 401(k) 集體訴訟 | **`evidence_dismissed`（附理由）** | trig 12（治理監測列） | 保留（處置方式不同，兩者都合法） |
| 13 | `major_events#3` | 近半 2026 年美國資料中心面臨延後或取消 | blind_spots[0]／R1／trig 3 | blind_spots[0]／blind_spots[4]／R1／trig 4 | 保留 |

**J1 兩邊 0 FAIL、0 漏接。** B 額外引用了 8 個 A 沒引的 id（`competitive_share_entrants#0/1/2`、`end_markets#1`、`supply_demand_durability#0/1/3`、`capital_markets_pricing#0/3`），多半用在 B 新增的「觀望論點可能錯」那條 steelman 反證上——**B 的證據引用面比 A 寬，不是窄**。

### 2.2 語意層：A 的實質反證 → B 的位置（分開評分）

| # | A 的實質反證 | B 的位置 | 判 |
|---|---|---|---|
| 1 | 資本支出消化（12GW 中 7GW 取消延後、Amazon FCF 轉負、Q4 基期） | `blind_spots[0]` 視角一＋R1＋Single Thing | 保留（B 用「近半 2026 年案延後」代替 7GW／12GW 的精確讀數） |
| 2 | 客戶扶植第二模組化供應商＋OFE 自採 | `blind_spots[1]` 視角二＋`threats[0]`＋R4＋`contradictions[2]` | 保留（A 放視角一、B 放視角二；B 明說「已反映在 Base 終端 22x 與 Bull 25x」） |
| 3 | 技術工短缺（含學徒比例受州法限制） | R2 獨立一條＋`threats[3]`＋`blind_spots[1]` | 保留並升格（A 只是 R4 的一個子句） |
| 4 | 變壓器交期 4–5 年、設備延誤 | `blind_spots[4]` 獨立一條＋R3 | 保留並升格 |
| 5 | 銅 50% 關稅、材料占成本 40–45% | `blind_spots[1]`「材料占專案成本 40–45% 受關稅影響」＋R3「232 關稅」 | **弱化**：全份 0 次提「銅」「50%」；關稅由具名稅率降為泛稱 |
| 6 | 資本支出 2%→5%、自購 $100M 級廠房、預收占 FCF 三分之一 | `blind_spots[1]`（預收）＋`governance.capital_returns`（capex 5%） | **弱化**：「資本支出占營收由 2% 升到 5%」這個變化率、「$100M 級單棟」的具體讀數在 B 只剩片段 |
| 7 | trailing 39.68x 為五年最貴、P/S 5.05 vs 2022 年 0.98、財報超預期 20.7% 股價反跌 | `blind_spots[2]` 視角三（trailing 39.7x 最高、Fwd 32.9x 建立在峰值利潤率上） | **弱化**：P/S 對照只剩 1 次且不在反證裡；「超預期 20.7% 股價反跌」整條消失 |
| 8 | 賣方均價 $2,197 隱含 FY2028 $73.85 不正常化且 30x | `contradictions[7]` 專條，含區間 $1,910–2,500、max/min 1.3x | 保留並強化 |
| 9 | PFAS 冷媒／密封膠淘汰改設備規格與時程 | **無** | **消失**（見下） |
| 10 | 2026-06-08 232 修訂與 301 暫停一年的關稅緩解面 | **無** | **消失**（見下） |
| 11 | 成長熄火壓測：成長率降到 10% → 本益比 18x → 股價 −51% | `valuation.targets.bear_anchor` 794（−50.7%）＋`reasoning.valuation`「熄火至 10% 的 18x」 | 保留（換位置，數字同源） |
| 12 | OEM 保固綁服務、卡住服務第二曲線 | `threats[2]` | 保留 |
| 13 | 紐約州暫停令／NIMBY／電網排隊 4–5 年 | `roic_durability.checkpoints[3]` 社會容忍度 🟡「州級暫停令與鄰避反對」 | 保留（「紐約州」「NIMBY」「許可」三個具名詞消失） |

**第 9、10 條要說清楚**：這兩條在 A 裡是**閘的修補加進去的**，不是 A 的判斷者自己寫的（見 §6）。A 的判斷者原稿與 B 一樣，兩邊都沒接 PFAS 與關稅緩解面。**若比 judge 對 judge（同一階段對同一階段），第 9、10 條不算 v18 的損失；若比最終產物對最終產物，A 有 B 沒有。** 我採前者計 kill condition，因為 gate 是獨立階段、A 那次剛好判紅而 B 沒判紅，這是閘的判斷差不是規則差。

### 2.3 真正屬於「消失」的兩件

| 項目 | A | B | 歸因 |
|---|---|---|---|
| **`kill_metrics[]` 的唯一致命點指標** | 4 條，第 4 條＝「模組化客戶多年承諾｜任一家取消或延後｜事件｜法說會／8-K」 | 4 條，第 4 條換成「FY26／FY27 共識 EPS 修正｜90 天下修 ≥10%｜每月快照｜Koyfin」 | **無任何 `contradictions[]` 歸因。** Single Thing 本身還在 `triggers[6]`，但 `kill_metrics[]` 才是 `position-thesis-monitor` 週更掃描讀的欄——監測器從此不會替 FIX 盯「客戶撤承諾」這件事 |
| **`plain.change_my_mind` 的清倉級觸發器** | 4 列，含兩條清倉（訂單連兩季季減→清倉；模組化客戶撤承諾→清倉，不等確認） | 2 列，**都是進場條件**（Fwd PE ≤28x → 買；FY27 指引 ≥15% → 門檻放寬 30x） | **規則直接造成。** 舊 `judge.md.tmpl` 的「plain 寫作規則五條」第 5 條寫「有寫 `change_my_mind` 就必含那條清倉級觸發器，每條寫出日期（無明確日期填「—」）」；v18 把五條壓成四條時**把第 5 條一起刪了**。結果快速版頁面「什麼會讓我改變主意」整段只剩買點，沒有出場點 |

同一形狀的第三件（較輕）：`decision_out.exec_line`。A 寫「新資金：現價不進…**已持有：不因估值單獨清倉，最多 trim；在手訂單連兩季季減或模組化客戶撤承諾才清倉**」；B 只寫「追蹤不進場；股價回約 $1,372 且訂單未轉負再買首筆 1/3 衛星倉」。B 的已持有者處置寫在 `contradictions[3].ruling` 裡（「三選一取調整：不清倉、不加碼，減至衛星上限 3%」），**規則層合規，但頁面首屏那一行看不到**。

### 2.4 承重數字：問四（現金與資本配置）整組變薄

| 數字 | A | B |
|---|---|---|
| 毛利率／營益率／FCF 利潤率／SBC／ROIC−WACC 五列 × FY2024／FY2025／TTM × **同業中位** | 有（`quality.three_year` 5 列帶 `peer_median`） | 只剩 4 列 Q2 對 Q2，**無同業中位、無 FCF 利潤率列、無 ROIC−WACC 列** |
| 回購占 FCF 比（`buyback_to_fcf`） | 有（>$200M vs 遠低於 80% 警戒） | 無 |
| 剔除回購的 EPS CAGR（`ex_buyback_eps_cagr`） | 有（回購貢獻 <2pp／年，EPS +92% 幾乎全為淨利成長） | 無 |
| 維護性資本支出推法（`maint_capex_method`） | 有（模組化占 1.5–2pp ⇒ 維護性約 2–3% 營收 ≈$0.3B） | 無 |
| 債務到期與加權利率 | 無（A 也沒有） | 「淨現金 $1.8B；信貸額度 $1.1B；**到期結構與加權利率證據包未涵蓋**」——明示缺口 |
| `valuation.targets` 形狀 | 巢狀物件，每個期限帶 `eps`／`pe`／`price`／`upside_pct`，`bear_anchor` 帶推導 note，`sell_side` 帶 mean／median／range／n／vs_price | 扁平五個數字（1372／1685／794／28／2197）。sell-side 的區間與分歧描述搬到 `contradictions[7]`，沒丟；但 EPS×PE 的拆解只剩 `reasoning.valuation` 散文 |

v18 把 `quality` 降 5 欄選填、`valuation.targets` 降選填，B 就真的少寫了。**這幾個不是反證，是承重數字**：回購對 EPS 的貢獻、維護性 capex、同業中位對照，都是「盈餘品質是不是真的」的直接檢查點。B 的 `reasoning.quality`（303 字）與 `reasoning.governance`（386 字）有覆蓋 FCF／NI、SBC、capex 5%、指引可信度，**但同業對照與回購拆解確實沒了**。

---

## 三、Codex 點名的 FIX 風險

### 3.1 PFAS（`regulatory_antitrust#1`，direction=**0**）

| | A | B |
|---|---|---|
| judge 原稿 | 未接 | 未接 |
| gate 判定 | **🔴**（連同 `reg_tariff_export#1/#2` 一起點名，要求補記或列 `evidence_dismissed`） | **🟡**（點名 `regulatory_antitrust#0/#1` 未進任一欄且 `evidence_dismissed` 為空陣列） |
| 修補後 | `moat.threats[3]` 補上「另 PFAS 冷媒／密封膠淘汰會改設備規格與時程，對 FIX 成本的量化證據包未涵蓋」，`evidence_refs` 加 `regulatory_antitrust#1` | 未修補（🟡 不觸發 patch） |
| 全份提及次數 | PFAS 2 次、冷媒 1 次 | **0 次、0 次** |

**判定**：J1 不適用（dir=0，機械閘本來就不管）。語意層 B 確實沒討論；A 也是靠閘才補上的。**這一軸兩版的判斷者表現相同，差別在閘給紅還給黃。**

### 3.2 關稅到期（`reg_tariff_export#1` dir=0、`#2` dir=+）

| | A | B |
|---|---|---|
| judge 原稿 | 只用 `reg_tariff_export#0`（10-K 泛稱）與 `geo_supply_chain#2`（4 月銅 50%），未提 6 月修訂與 301 暫停 | 同樣只用 `#0`＋`geo_supply_chain#2`（且未寫「銅」「50%」） |
| gate | 🔴（明指「判斷反而沿用較舊的 2026-04-01 銅 50% 作為 R4 與 threats 的關稅承重」） | 未點名這兩筆 |
| 修補後 | `moat.threats[3]` 補「2026-06-08 232 修訂後標準稅率 25%、15% 減稅率擴及 HVAC 系統與零件，且 301 關稅暫停一年」，`p` 由 35% 下修到 30% | 無 |
| 提及 | 232 五次、301 三次、銅 六次 | 232 兩次、301 **0 次**、銅 **0 次** |

**判定**：同上——兩邊判斷者一樣沒查到緩解面，A 的優勢完全來自閘。**但值得記一筆**：這條緩解面若被採納，方向是**降低**風險（關稅承重下修），所以 B 漏掉它反而讓 B 更悲觀一點，不是樂觀偏誤。

### 3.3 引用與主張是否對應

| 檢查 | A | B |
|---|---|---|
| 引用不存在的 finding | `evidence_dismissed[1]` 引 `lawsuit_class_action#0` | `triggers[11].evidence_refs` 引 `lawsuit_class_action#0` |
| 該 id 是否存在 | **存在**——在 `evidence.events.lawsuit_class_action.findings[0]`，不在 `coverage` | 同左 |
| 閘怎麼判 | 未點名 | **⑤ 🟡「該軸不存在於 coverage 任一列」** |
| 我的判定 | 兩邊都合法；**B 的閘 ⑤ 是誤報**——閘只掃了 `coverage`，沒掃 `events`。這是閘的職責書問題，不是 B 的錯 |
| `evidence_dismissed` 被拿來裝非證據 | **A 有**：第 3 條寫 `decision_inputs.irr_base_pct（同 ev5y_pct、asym_ratio）`——那不是 finding ref，是回應閘的建議。Codex 第三輪已明說「該陣列是對證據的處置，不是程式回填說明」 | **B 無**（陣列為空）。但空陣列又被閘 ③ 拿來當 🟡 依據 |

### 3.4 成長天花板來源與毛利期間口徑

| | A | B |
|---|---|---|
| `endo_ceiling` | **15%** | **15%** |
| 推導 | ROIIC 約 50%（CFO 稱模組化 1–2 年回本 ⇒ 增量 ROIC 50–100%，取下緣）× 再投資率約 30%（淨 capex $0.35B＋併購 $0.2B ÷ NOPAT $1.4B） | 「公式退化」：ΔNOPAT 年化約 $795M ÷ 新增投入資本 ≤$230M ⇒ ROIIC >300% 無判讀意義 → **改以永續工班成長高個位數 × 模組化生產力與定價 +5–6pp ≈ 15%** |
| 合規性 | 規則寫「再投資率口徑 `(Capex−D&A+ΔWC+收購淨額)÷NOPAT`；**負 CCC 業務公式失效，改以 ROIIC 為上界**」。A 沒有走「改以 ROIIC 為上界」這條，而是把 ΔWC 硬設為 0 硬算出 30% | B 正確辨識負營運資金使公式失效，**但沒有照規則改用 ROIIC 當上界**（因為 ROIIC >300% 當上界毫無意義），自創了一把勞動供給的尺 |
| 判定 | **兩邊都沒有真正照條文走，兩邊都湊出同一個 15%。** A 的問題是假精準（ROIIC 從一句法說會回本評論反推、再投資率把負營運資金算成 0）；B 的問題是換了一把規則沒授權的尺，但至少誠實說了為什麼舊尺不能用。**規則本身在負 CCC 業務上有洞，這是本輪最該補的條文，不是 v18 造成的** |
| 毛利期間口徑混用 | `quality.three_year` 用 FY2024／FY2025／TTM 三欄，內容大量「證據包未涵蓋」，`ttm_2026` 毛利率 25.66（TTM）與正文常引的 25.9%（Q2 單季）並存 | `quality.three_year` **標題叫 three_year 但裝的是 Q2_2025 對 Q2_2026 的兩點，外加一列 FY2022／FY2025 的年度 trailing P/E**——三種期間裝在同一張表。25.9% 全份 13 次一致用單季口徑 |
| 判定 | **A 的欄名與內容較一致但半數空白；B 的內容較實但期間口徑混在一張表裡。** Codex 點的這條在 B 成立，且是 v18 把 `quality` 降選填後判斷者自由發揮的直接後果 |

---

## 四、門檻與行動條件並排

| 項目 | 0906（前份） | A（舊規則） | B（新規則） |
|---|---|---|---|
| **唯一致命點** | 「兩家雲端同季下修 ≥10%」 | 「兩家模組化超大規模客戶之一公開取消或延後多年產能承諾（含 FIX 因此宣布暫停 500 萬平方英尺擴產）」 | 「兩家模組化承諾客戶之一公開暫停或縮減多年產能承諾」 |
| 致命點機率 | — | 12–24 個月約 15% | 12–24 個月約 15–20% |
| **清倉門檻** | 在手訂單 QoQ 連 2 季下滑 → 清倉 | ①在手訂單連 2 季季減 → 清倉；②模組化客戶撤承諾 → 清倉不等確認；③毛利率連 3 季 <22.5% → 清倉 | ①訂單連 2 季季減**且** FY1 共識 90 天下修 ≥15% → 清倉（`triggers[10]`）；②承諾客戶撤回 → 清倉／撤出追蹤（`triggers[6]`）。**22.5% 那條消失** |
| **重啟（rearm）** | ≤$1,050（FY27 共識 17.5x）；或訂單 ≥$16B 且 2028 口徑不降 | **≤$1,440（FY2027 共識 24x）且最近一季毛利率 ≥24% 且在手訂單季增未轉負** | **Fwd PE ≤28x（約 $1,372）且同店訂單季增 ≥0；或 FY27 同店指引 ≥+15% 且 ≤30x**（毛利率條件消失） |
| **kill_metrics[]** | 訂單 QoQ／四大 capex 指引／TTM 營益率 <15%／毛利 YoY vs EME | 同店訂單季增／單季毛利率 <22.5% 連 3 季／四大 capex 指引／**模組化客戶多年承諾** | 同店訂單季增率／毛利率連 2 季 <24%／四大 FY27 capex 指引／**FY26 ／FY27 共識 EPS 90 天下修 ≥10%** |
| triggers 條數／型別 | 11（含清倉列） | 9（無獨立清倉型別，清倉寫在 action 裡） | 14（型別齊：假設 3／風險 4／Single Thing／rearm／加碼／減碼／清倉／複審 2） |
| 有 `date` 的 triggers | 多數 | 5／9 | **3／14**（其餘 `date: null`） |
| **exec_line 是否含已持有者處置** | 有 | 有 | 無（移到 `contradictions[3].ruling`） |
| **`plain.change_my_mind` 是否含清倉列** | — | **有 2 條** | **0 條** |

### J6（門檻漂移機械比對）在 B 有沒有抓到？

**沒有，因為它跑不起來。** B 的 validator 回：

```
⚠ J6｜門檻漂移比對（Single Thing）：前份 0 列／本次 1 列，非 1:1 無法機械比對，略過
⚠ J6｜門檻漂移比對（清倉）：前份 0 列／本次 1 列，非 1:1 無法機械比對，略過
```

原因 B 自己在 `contradictions[5]` 誠實寫了：「前份觸發器清單證據包不可得（`prior_dd.triggers` unavailable）；前份 Single Thing 未於證據包呈現」。**`dd_prior.extract_triggers` 對 FIX 的前份（v12.3 舊格式 DD）抽不出任何列，J6 因此在本檔完全空轉。** J6 不是壞了，是它依賴的上游資料在舊格式 DD 上抽不到——**這是 J6 上線後第一次在真檔上被驗，結論是「對 v12.3 前份無效」。**

順帶：J6 設計上是拿**本次對前份 DD**，本來就無法做 A/B 比對；A、B 的門檻差異（見上表）只能人工比，也就是本節。

### WP-G 的措辭補丁效果評估

WP-G 在 `judgment-rules.md` §4 加了：「**行動門檻同受此律（2026-09-11 新增）**：`kill_metrics[]`／`triggers[]`／`decision_inputs` 裡任何門檻數字或唯一致命點與前份不同，必須在 `contradictions[]` 有一條 `cause`＝新證據或方法變動的條目寫『舊門檻→新門檻＋理由』；`rearm_trigger` 不得對已變動的門檻寫『相同』。」

**部分有效**：

- ✅ `rearm_trigger` 的變動，B 在 `contradictions[3]` 寫了完整理由（「前份技術錨布林中軌 $1,421 已被跌破而失效；前份 28–32x 區間現價 32.9x 已在邊緣，沿用等於現在就該買」）。閘 ⑧ 給 🟢。A 同一件事被閘 ⑧ 判 🟡（把毛利率條件歸在「價格變動」下）。**這一項 B 比 A 好，是 WP-G 的功勞。**
- ✅ Single Thing 與新設門檻，B 在 `contradictions[5]` 專條說明「無舊門檻可對照，全部視為新設並註明來源；下輪複審以本份為基準」。
- ❌ **`kill_metrics[]` 第 4 條被整條換掉（客戶承諾 → 共識 EPS 修正），沒有出現在任何 `contradictions[]` 條目**。措辭寫了 `kill_metrics[]` 三個字，但機械檢查（J6）在本檔空轉，閘也沒查這一欄，所以沒有任何一層攔到。

---

## 五、六問是否都有實質回答（B）

| 題 | 權威欄（字數） | 有無證據到結論 | 判 |
|---|---|---|---|
| 一 怎麼賺錢 | `reasoning.industry`（768） | 分部 58／17／17／8％＋建造 90%／服務 10%／模組化 17%＋Q2 毛利 25.9%、營益 17.1%（親讀）；判斷句「錢卡在能執行的產能——技術工與模組廠」；時鐘 Phase II 偏後段，依據非股價（同店訂單季增 13%、2027 capex $934.5B vs 管理層提示 H2 減速、Amazon FCF 轉負） | ✅ |
| 二 競爭優勢 | `moat.trend` → ＋`trend_evidence` | 機制一條（把機電工程搬進自己工廠＋全國移動工班，客戶用預付與多年承諾換交期）；可證方向（營益率 spread 對 EME 6.9pp、YoY 由 13.8%→17.1% 擴大）；**趨勢由 ↑ 改 →，理由是親讀原句（客戶正誘導其他公司生產共同設計的模組）**。同業 ROIC 取不到，明說換營益率軸 | ✅ |
| 三 成長 | `growth.runway_post_y5` 🟡 | 三年共識 CAGR 兩種口徑都算（36.7% 基期含一次性 → 改用前瞻 22.75%）＋內生上界 15%＋缺口 7.75pp 三段歸因（營益率再擴約 5pp／併購約 2pp／餘 <1pp 無法歸因，不標「依賴 re-rate」）；FY+3 不機械外推，理由綁訂單覆蓋 1.15 倍 | ✅ |
| 四 現金與資本配置 | `governance.capalloc_grade` B | FCF／NI 2.26 且 CFO 拆三分之一為預收；SBC 0.47%／2.74%；capex 5% 營收含模組化 1.5–2pp、回收 1–2 年；**債務到期與利率明示「證據包未涵蓋」**；可信度段有指引三次上修的時間序列 | ⚠️ 有結論有依據，但**同業中位對照、回購占 FCF、剔除回購的 EPS CAGR、維護性 capex 推法四項 A 有 B 無**（見 §2.4） |
| 五 估值 | `valuation.val_light` 🔴＋`val_light_derivation` | 分位算式、PEG 兩口徑、合理 PE 28x 的來源（護城河 B＋成長 🟡，隱含 PEG 1.23）、三分量拆解（EPS +12.4%／倍數 −7.7%／股息＋回購 0.5%）、現價隱含條件（「要 32.9x 合理，需 FY29 後仍 15% 以上成長且毛利率不回落；我不信」） | ✅ |
| 六 可能看錯在哪 | `premortem.blind_spots[]` 5 條 | 三視角齊（論點失敗 3／股東經濟變差 1／價格已反映 1），每條 evidence→assumption→consequence→ruling→watch 五欄全填；**第 4 條是 steelman（觀望論點可能錯），A 沒有這一條** | ✅ |

`plain.six` 六段每段都帶數字、都是白話，沒有空話。**A 的 `plain.five` 缺「競爭優勢」與「資本配置」兩題**——六問骨架在頁面上確實補了兩個舊版沒問的問題，這一點與 TXN 那次結論一致。

---

## 六、閘

### A：🔴 1 條

| 軸 | 內容 |
|---|---|
| ③ 其他結構變數 | `reg_tariff_export#1`（2026-06-08 232 修訂）、`#2`（301 暫停一年）、`regulatory_antitrust#1`（PFAS）三筆皆未進任何欄；判斷反而沿用較舊的 `geo_supply_chain#2`（2026-04-01 銅 50%）作為 R4 與 threats 的關稅承重 |

另 🟡 2：⑥ `decision_inputs` 三欄 null 且「腳本回填」聲明放錯位置；⑧ `rearm_trigger` 新增的「毛利率 ≥24%」被歸在 `cause="價格變動"` 條目下。

**修補結果（`agents/gate_patch_1.json`，5 筆）**：

| 補丁路徑 | 是否落地 |
|---|---|
| `$.moat.threats[3]` | ✅ 落地（PFAS＋232 修訂＋301 暫停進來，`p` 由 35% 下修到 30%） |
| **`$.R[3]`** | ❌ **沒落到 `thesis.R[3]`**——patcher 照字面在 judgment **頂層新建了一個 `R` 物件 `{"3": {...}}`**。`thesis.R[3]` 的文字至今仍是修補前的舊版（無關稅緩解面）。log 卻印「patch map 套用 5 筆，錯誤 0」 |
| `$.triggers[6].evidence_refs` | ✅ 落地 |
| `$.contradictions[0].ruling` | ✅ 落地 |
| `$.evidence_dismissed` | ✅ 落地（3 筆，其中第 3 筆是**對閘建議的拒絕**，把非證據塞進證據處置陣列——Codex 第三輪已判此為契約誤解） |

**這是本輪最該修的機械缺陷**：閘寫錯 JSONPath（應為 `$.thesis.R[3]`），patcher 不但沒報錯，還憑空造了一個頂層 `R` 欄；schema（`additionalProperties` 未鎖）與新舊兩版 validator 都沒抓到。**閘判紅 → 修補 → 重驗 PASS，中間有一筆是假的。**

### B：🟡 3 條、🔴 0

| # | 軸 | 內容 | 我的複核 |
|---|---|---|---|
| ③ | 其他結構變數 | `regulatory_antitrust#0`（licensing）與 `#1`（PFAS）未進任一欄，且 `evidence_dismissed` 為空陣列 | **成立**。這正是 Codex 點名的 PFAS 軸（dir=0，J1 管不到），要靠閘或規則接 |
| ⑤ | 覆蓋面掃描 | `triggers[11]` 引 `lawsuit_class_action#0`，該軸不在 coverage 任一列 | **誤報**。該 finding 真實存在於 `evidence.events.lawsuit_class_action.findings[0]`；閘只掃 `coverage`。閘的職責書要補「events 也是合法 ref 命名空間」 |
| ⑥ | 量化模組完整性 | `decision_inputs` 三欄 null＋回填聲明位置；**`max_dd.lo` −56 與 `reasoning.premortem` 的「−30～−50%」差 6pp** | **前半是契約誤解**（衍生欄由 `dd_metric_resolver` 從 `scenario_meta` 取，Codex 已判閘該改）；**後半成立且是真弱點**——J2 把 `max_dd.lo` 從 −55 修成 −56，但 `reasoning.premortem` 的推導散文沒跟著改，數字與敘述脫勾 |

### 是否揭露弱點

- A 的 🔴 揭露了真實的證據覆蓋缺口（關稅時效＋PFAS），但修補本身出了一筆假補丁。
- B 的 🟡③ 揭露了同一類缺口（PFAS），只是沒升級到紅；🟡⑥ 後半揭露了「機械修數字但沒修散文」這個新 harness 的副作用。
- **兩邊的閘都有一條在浪費篇幅**：A 的 ⑥、B 的 ⑥ 前半都在要求把腳本回填欄手填，這是 Codex 已經裁定的契約誤解，閘每次都會再提一次。建議照 Codex 建議改閘的職責書，不要靠判斷者作文擋。

---

## 七、成本與時間

### 7.1 本輪逐筆（`manifest.agents` 加總，非估算）

| 項 | A（舊規則） | B（新規則） | Δ |
|---|---:|---:|---:|
| 判斷 `judge_1`：turns／output／cache_read／cache_creation／$ | 4／93,470／613,937／188,829／**$8.687** | 4／88,538／615,338／172,379／**$8.109** | −6.7% |
| 判斷 `judge_fix_1`：turns／output／$ | 1／2,851／**$1.089** | 1／2,639／**$0.925** | −15.1% |
| **判斷段小計** | 2 spawn／5 turns／96,321 out／**$9.776** | 2 spawn／5 turns／91,177 out／**$9.034** | **−7.6%** |
| 閘 `gate_1`：turns／output／$ | 2／17,603／**$1.397** | 2／18,795／**$1.340** | −4.1% |
| 閘 `gate_patch_1` | 1／3,751／**$1.016** | **無** | — |
| **閘小計** | 2 spawn／**$2.413** | 1 spawn／**$1.340** | **−44.5%** |
| **含修補口徑合計** | **$12.19** | **$10.37** | **−14.9%** |
| **乾淨輪合計**（扣掉 A 的閘修補） | **$11.17** | **$10.37** | **−7.2%** |
| 牆鐘：judged／gated／合計（stage 時戳） | 1,445s／317s／**1,762s** | 1,376s／267s／**1,643s** | **−6.8%** |
| judgment.json（`json.dumps` 預設分隔符） | 38,910 | 33,870 | −13.0% |
| judge bundle 輸入 | 203,429 bytes | 201,129 bytes | −1.1% |
| gate bundle 輸入 | 122,597 bytes | 112,778 bytes | −8.0% |
| validate | 0 FAIL／**6** WARN | 0 FAIL／**17** WARN | 見 §8 |

**交辦單表格的「A validate PASS 8 WARN」與 manifest 對不上**：manifest `validate_summary` 與 log 都是 `{'fail': 0, 'warn': 6}`。本報告一律以 manifest 為準。

### 7.2 為什麼 TXN 省一半、FIX 幾乎沒省

**因為 TXN 的節省來自 WP-D，而 WP-D 已經在本次的 A 裡面。**

- TXN 那組：舊＝`TXN_20260907`（v17 規則，2026-09-07，8 spawn 含配額失敗）；新＝`TXN_20260910`（WP-D／WP-E 精簡規則）。省下的 51% 是「A1 反證單一居所＋A3 `plain`／`reasoning` 撤地板＋A4 漂移按原因分組＋撤配額六項＋B1–B9 條件式」的效果。
- 本次的 A 在 `77aec95a8`，`a7f8b24d8`（WP-D，2026-09-10）與 `3c739b0fe` 都已合併。**A 已經是 TXN 的「新版」。** 本次 A/B 唯一的差是 `2e594765a`（六問骨架）＋`750dc1312`（陣列形狀）＋`0e2a6c973`（WP-G）。
- 六問骨架做的是**重排規則檔與 schema 放寬**，不是刪掉重複作文——重複作文在 WP-D 就刪完了。`judgment-rules.md` 45,359 → 41,289 bytes（−9.0%），但 judge bundle 只降 1.1%（九成是證據包與逐字稿），輸出降 5.3%。**這個量級與跑次變異同階，不能宣稱是規則效果。**

三件次要因素也要如實說：

1. **FIX 是爭議檔**（估值尺互斥、錯過成本反向命中、前份翻面），反證與矛盾本來就多。B 寫了 10 條 `contradictions`（A 6 條）、14 條 `triggers`（A 9 條）、5 條 `blind_spots`（A 5 條）——**B 沒有寫得比較少，只是把字挪了位置**。
2. **閘那 44% 的節省不是規則帶來的**：`gate_1` 冷讀本身只省 4.1%（$1.397→$1.340，gate bundle −8%），整個節省來自「B 沒判紅所以不用 patch spawn」。下一份若判紅，這 44% 立刻消失。
3. **B 的 judge 沒有變快**：turns 兩邊都是 4＋1，牆鐘 1,445s→1,376s（−4.8%）。

### 7.3 TXN／FIX 兩組總表

| 指標 | TXN 舊（v17，20260907） | TXN 新（WP-D／E，20260910） | FIX A（WP-D／E，20260911） | FIX B（v18＋WP-G，20260911） |
|---|---:|---:|---:|---:|
| 檔別 | 乾淨 | 乾淨 | 爭議 | 爭議 |
| 前份逐字稿控制 | ❌ 未讀最新季 | ✅ 親讀 Q2'26 | ✅ 親讀 Q2'26 | ✅ 親讀 Q2'26 |
| 判斷段 spawn／output（最近完成輪含該輪修補） | 2／93,195 | 4／58,489 | 2／96,321 | 2／91,177 |
| 判斷段 $（最近完成輪含該輪修補） | $9.88 | $6.67 | $9.78 | $9.03 |
| 閘 spawn／$（含閘的修補） | 2／$3.16 | 1／$1.32 | 2／$2.41 | 1／$1.34 |
| **實付合計（最近完成輪含修補）** | **$13.03** | **$7.99** | **$12.19** | **$10.37** |
| 剔除事故修補後的乾淨輪 | — | $6.37 | $11.17 | $10.37 |
| 另計歷史用量（配額失敗等） | ＋$6.23（manifest 全部 $19.26） | — | — | — |
| 牆鐘（判斷＋閘） | 1,756s | 1,321s | 1,762s | 1,643s |
| judgment 大小（`json.dumps` 預設分隔符） | 36,935 | 32,848 | 38,910 | 33,870 |
| 裁決 | 進場／核心 | 進場／核心 | 觀望／追蹤 | 觀望／追蹤 |
| 閘 | 🔴1／🟡4 | 🔴0／🟡3 | 🔴1／🟡2 | 🔴0／🟡3 |
| 規則世代差 | v17 → WP-D／E | — | WP-D／E → v18＋WP-G | — |
| 該世代改善（實付口徑） | **−39%** | | **−14.9%** | |
| 該世代改善（剔除事故口徑） | **−51%** | | **−7.2%** | |

TXN 欄位採 Codex 第三輪複審 `_codex_v18_round3_review_20260911.md` 的重新核帳（該輪已更正 TXN 報告原表的 $16.11／$13.04）。FIX 欄位為本次 `manifest.agents` 逐筆加總。**兩組口徑一致才可比**：FIX 這組 A 的「事故」是閘判紅後的 patch spawn（$1.02），B 無事故，所以 B 的兩個口徑同值。

**一句話**：規則精簡的錢在 WP-D 就賺完了；v18 六問骨架的價值不在成本，在「六問齊備＋三視角反證＋一次判斷」的結構，這是要用品質論證的，不是用帳單。**n=2，且兩組的規則世代不同（TXN 測 v17→WP-D／E，FIX 測 WP-D／E→v18），不能相加成「v18 省了 51%＋7%」。**

---

## 八、B 的 17 個 WARN 是什麼

用**同一把新 validator**跑 A 與 B（A 用其 run 內的 evidence，repo cwd）得到可比基準：

| 類別 | A（新 validator） | B | Δ | 性質 |
|---|---:|---:|---:|---|
| `triggers[].action` 不含 E12 動作詞幹（soft） | 4 | **12** | +8 | **B 寫了 14 條 trigger（A 9 條），且用詞更口語（「反轉則撤出追蹤池」「Bear 機率上調至 35%」）。純數量×寬鬆檢查，非品質退步；但這條檢查在真檔上噪音很大，12／14 都中，等於沒有鑑別力** |
| `scenario_ref` 交叉檢查略過（dd-meta 缺 `scenario_tree`） | 1 | 1 | 0 | 既有 |
| **J2 情境樹年期提示** | —（A 在自己的 harness 下是「J2 略過」） | **1** | +1 | **新檢查揭露的既有問題**：`terminal_label` FY2031 vs `eps_meta.base_eps_path` 終端 FY2028 不一致。訊息自己註明「base_eps_path 年期契約未明文（三年錨或完整路徑皆有既有先例），僅供人工複核」——這正是 Codex A 節指出、尚未定義的契約 |
| **J2 Max DD 恆等式** | **1 FAIL**（新 validator 下） | 0 | — | **A 的 `max_dd.lo=-55` 對 Bear 終點 −58.3% 違反恆等式**，舊 harness 因 `scenario_ref` 路徑重複目錄整條略過，紅字沒響。B 被抓到後由 `judge_fix_1` 改成 −56（Bear −55.3%），過關 |
| J4 `plain` 出現 judgment 查無的數字 `['1610','1992']` | 0 | **1** | +1 | B 的 `plain` 寫「$1,992」「$1,610」，judgment 其他欄是 `1992.74`／`1610.34`。**格式面**，非新增數字 |
| **J6 門檻漂移比對（Single Thing／清倉）** | 2（新 validator 下） | **2** | 0（相對舊 harness 是 +2） | **新檢查，兩條都是「前份 0 列，無法比對，略過」**——揭露 `dd_prior.extract_triggers` 對 v12.3 格式前份抽不出列 |
| 合計 | 7 WARN＋1 FAIL | 17 WARN | | |

**歸類**：

- **8／11 的增量是同一條寬鬆檢查（E12 動作詞幹）乘上 trigger 條數**，不是新問題。
- **2 條是新檢查（J6）誠實回報「查不了」**——這是有價值的訊息，不是雜訊：它告訴我們 WP-G 加的門檻漂移閘在舊格式前份上完全空轉。
- **1 條是新檢查（J2 年期）揭露的既有契約缺口**——`base_eps_path` 到底是三年共識錨還是完整五年路徑，至今沒有明文。A 的 `base_eps_path` 是五年路徑（FY2026E–FY2030E），B 的是共識錨（FY2025A–FY2028E＋`source`）。**兩份同一天、同一個 ticker、兩種形狀，validator 只能 WARN。這一條要先定義才有辦法查 §1.3 的口徑問題。**
- **v18 新形狀造成的實質新問題：0 條。** 但 A 那邊有 1 個 FAIL 是新 validator 才抓得到的——**新規則這一輪最大的實質貢獻是 J2，不是六問骨架。**

---

## 九、頁面（brief A／B 並排）

| 項 | A | B |
|---|---|---|
| 檔案大小 | 54,402 bytes | 52,422 bytes（−3.6%，沒有縮水） |
| 首屏標題 | 「五句話」 | **「六個問題」六段全渲染**（怎麼賺錢／競爭優勢／成長／現金與資本配置／估值／可能看錯在哪） |
| 三視角反證 | 5 條，依 view 分組渲染（論點失敗 3／股東經濟變差 1／價格已反映 1） | 5 條，同樣分組；**多一條 steelman（「觀望論點可能錯」）**；另有 `failure_story`＋`second_failure` 兩段（A 兩欄皆 null，v18 降選填後 B 反而寫了） |
| **未展開標記** | ✅ 有一列：「未展開區塊——分部三年模型……；同業倍數對照……」（`growth.segments`、`valuation.peers` 皆 `expanded:false` 附理由與重啟觸發） | **無**——B 把四個條件式區塊全部展開了 |
| 情境樹表 | Bull 95×26＝$2,470／Base 74×23＝$1,702／Bear 42×16＝$672；EPS 列 FY26–FY30 | Bull 118×25＝$2,950／Base 88×22＝$1,936／Bear 45×16＝$720；EPS 列 **FY27–FY31** |
| Tile | EV −1.6%／IRR 1.1／AR 0.8／Max DD −55%（−55～−35）／護城河 B ↑／估值 🔴 分位 100% · PEG 0.9／陷阱 🟡 | EV +13.3%／IRR 3.8／AR 1.3／Max DD −56%（−56～−30）／護城河 B →／估值 🔴 分位 100% · PEG 1.44／陷阱 🟢。**`decision_inputs` 三欄皆 null 仍正確渲染，`scenario_meta` fallback 生效** |
| **「市場隱含成長（CAGR）」欄** | 36.7% | **「—」空白** |
| 「什麼會讓我改變主意」 | 4 列，含 2 條清倉 | **2 列，全是買點，沒有出場點** |
| 觸發器表 | 9 列，5 列有日期 | 14 列，**只有 3 列有日期**；有 `type_display`（「唯一致命點」「估值rearm」等）比 A 好讀 |
| 跨模型冷讀摘要 | 「判斷級 🔴 1、🟡 2」 | 「判斷級 🔴 0、🟡 3」——**TXN 那次的中文數字 regex bug 沒有復現**（B 的 `gate_audit.md` 附註寫「🟡 3 條」是阿拉伯數字） |
| 怎麼行動 | 執行摘要含新資金＋已持有者兩段 | **只有新資金一段** |

### 渲染缺漏（三處，兩處新）

1. **「市場隱含成長（CAGR）」在 B 是空的。** `dd_brief.py:457 _implied_cagr()` 用 regex 掃 `valuation` 這個 dict 的 JSON 找「CAGR…x%」。A 的 `val_light_derivation` 裡有「共識 EPS CAGR 36.7%」所以抓得到；B 的推導文字精簡後沒出現「CAGR」這個詞（22.75% 寫在 `reasoning.growth` 與 `val_denominator_note`），regex 落空。**v18 的文字精簡直接把頁面上一格數字打空。** 修法：改從 `growth`／`eps_meta` 取權威值，不要 regex 撈散文。
2. **`render_e7_html`（§5.R ROIC 持續期四檢查點）在 B 渲染出 4 列全空。** 它讀 `n`／`question`／`status`／`evidence`；A 的 checkpoints 用 `name`／`light`／`evidence`／`proxy`（`evidence` 對得上，其餘 3 欄空）；**B 的 `judge_fix_1` 把 checkpoints 改成 `item`／`level`／`text`，4 欄全對不上。** schema 對 checkpoints 只寫 `{"type":"object"}`（新舊版皆同），沒有形狀約束，validator 過、閘也沒看表格。這是 Codex「陣列形狀修補仍未與表格渲染契約對齊」的第二個實例（第一個是 E10）。
3. **「負向證據處置表」在 A 與 B 都是 13 列全部「—（judgment 未列 evidence_refs／evidence_dismissed）」。** `dd_brief.py:813` 用 **claim 全文**當 key 去比對 `evidence_refs` 裡的 **id 字串**（`customer_second_source#1` 之類），永遠比不中。**這張表從來沒有正確運作過**，而它正是頁面上唯一一個「我有沒有處理負面證據」的面板。**既有 bug、與 v18 無關，但要修，否則讀者看到的永遠是「全部沒處理」。**

**反向要記一筆的改善**：`render_e10_html`（十年資本配置）在 A 只有 5／35 格有內容（A 的 `capital_returns` 用 `year`／`deal`／`price`／`roiic`，渲染器要 `year`／`buyback`／`dividend`／`capex`／`rd`），**B 的 `[{item,value}]` 形狀 10／10 格全滿**——WP-G 的 `gen_dd_tables.py` 改動修好了 Codex 點名的 E10 空表問題。`render_e3_html`（TAM）同理：A 9／21，B 14／14。

---

## 十、結論

### 10.1 kill condition 按帳本原文判

`knowledge/rule_ledger.md` v18 列原文：「**成對驗證（同一份證據包、同模型設定，一乾淨一爭議）出現任一即回退規則檔到 WP-E 版**：(a) 新版漏掉舊版有的關鍵反證或承重數字 ≥1 例；(b) 新舊裁決分歧且經審為新版的證據或推理不成立。」

| 條款 | 判定 |
|---|---|
| (b) 裁決分歧 | **不觸發** |
| (a) 關鍵反證 | **不觸發**（13 條負向 finding 兩邊全處置，語意層無整條消失；PFAS／關稅緩解面兩邊判斷者表現相同，A 的優勢來自閘不是規則） |
| (a) **承重數字／行動條件** | **觸發，1 例**：`kill_metrics[]` 第 4 條由「模組化客戶多年承諾｜任一家取消或延後」換成「共識 EPS 90 天下修 ≥10%」，**無任何歸因**。唯一致命點從週更監測器（`position-thesis-monitor` 讀 `kill_metrics[]`）的視野裡消失。另一例（`plain.change_my_mind` 失去清倉列）是 `judge.md.tmpl` 刪掉「寫作規則五條」第 5 條的直接後果 |

**按原文，(a) ≥1 例成立 → 應回退。**

我的處置建議（明說這是建議，裁定權在持有人）：**不回退，但這是同一形狀的第二次，第三次沒有理由再補。**理由三點：

1. 兩個 kill 例都**指得出單一成因、一行可修**：一個是 WP-G 措辭涵蓋 `kill_metrics[]` 但沒有任何一層真的去查（J6 在 v12.3 前份上空轉、閘不查這欄）；一個是壓縮 prompt 時漏帶一句。
2. 同一輪裡 v18／WP-G 也**接住了 A 接不住的東西**：J2 抓到 A 的 Max DD 恆等式違反（−55 vs −58.3，舊 harness 整條略過）；`val_denominator_note` 讓 B 補上 A 留成 null 的 `val_denominator_disputed`（A 的決策矩陣因此多一個輸入缺口）；漂移歸因由 A 的 🟡 變成 B 的 🟢；E10／E3 表由半空變全滿。**回退等於把這些一起退掉。**
3. 但要防 Codex 警告的「看過結果才自行改門檻」：**本輪不動門檻文字**，只補實作（見下）；第三次同形狀出現時直接執行帳本原文，不再討論。

### 10.2 「保留 v18 精簡方向」的建議成不成立

**成立，但要換一個理由。**

- 用**成本**論證：**不成立**。乾淨輪只省 7.2%、牆鐘省 6.8%、bundle 只省 1.1%，與跑次變異同階。TXN 的 51% 屬於 WP-D，不屬於 v18。
- 用**品質結構**論證：**成立**。六問在 B 是 6／6 有證據到結論；三視角反證齊備且多一條 steelman；`plain.six` 補了 A 沒問的「競爭優勢」與「資本配置」；`contradictions` 反而更多更實（10 條 vs 6 條）；`triggers` 型別齊全（B 有獨立清倉列，A 沒有）；引用的 finding id 更廣（23 vs 15）；漂移歸因通過閘。**B 的判斷物是比 A 更完整的東西，只是沒有更便宜。**
- 兩件必須同時承認的退步：**`quality` 模組整組變薄**（同業中位、回購占 FCF、剔除回購 EPS CAGR、維護性 capex 四項全失）與**白話層行動條件缺出場**。前者是 schema 降選填的代價，後者是 prompt 壓縮的疏漏。

### 10.3 給持有人的三個下一步

1. **把 WP-G 的門檻措辭做成機械檢查，不要再靠作文。** 具體：(a) `validate_judgment.py` 加一條 **本份自檢**——`thesis.single_thing.description` 所指的那個指標必須出現在 `kill_metrics[]` 或型別為「Single Thing／清倉」的 `triggers[]` 列裡，缺了 FAIL（這不需要前份資料，J6 在 v12.3 前份上空轉的問題繞得過去）；(b) `judge.md.tmpl` 把刪掉的那句話加回去：「`plain.change_my_mind` 必含至少一條清倉級觸發器」；(c) `decision_out.exec_line` 要求新資金與已持有者分兩段（規則 §5 裁決品質四問④本來就這樣寫，只是沒接到這個欄）。**三件都是一行，不動規則檔的精簡方向。**
2. **定義 `eps_meta.base_eps_path` 與情境樹終端年的契約，把 §1 那 15pp 的自由度關掉。** 現在同一天同一檔可以合法地產出 FY2030 或 FY2031 兩種終端，EV 差 15pp，而 `ev5y_pct` 是 dd-meta 直讀欄、會進聚合層。建議：**終端年一律取「判斷日起滿五個完整會計年度」**（FIX 2026-09 → FY2031），`start` 一律用與該終端同源的年度 GAAP 口徑，並把 `base_eps_path` 明文定為「共識三年錨＋來源」（B 的形狀）而非模型路徑（A 的形狀）——然後把 J2 的年期檢查由 WARN 升成 FAIL。**這是本輪唯一影響持有人看到的數字的事，優先於任何規則精簡議題。**
3. **修三個機械缺陷，然後停。** (a) 閘寫 `$.R[3]` 卻被 patcher 在頂層造出 `R` 欄：patcher 對未知頂層 key 要報錯，schema 加 `additionalProperties: false` 或 validator 加一條「未知頂層欄＝FAIL」；(b) `dd_brief.render_negative_evidence` 用 claim 全文比對 id，13 列永遠顯示「未處理」——改成比對 `{axis}#{i}`；(c) `_implied_cagr` 從散文 regex 撈 CAGR，改讀權威欄；順帶把 `render_e7_html` 的 checkpoints 欄名與 schema 對齊（或讓渲染器接受 `item`／`level`／`text`）。

### 10.4 **不需要再做的事**（持有人要收斂，這幾件請直接劃掉）

- **不需要跑第三檔成對驗證。** 兩檔（乾淨 TXN／爭議 FIX）已經回答了設計問題：規則精簡的錢在 WP-D 賺完、v18 的價值在結構不在成本、失效形狀集中在「門檻與行動條件在搬家時掉了」。第三檔只會再花 $10 得到同一句話。**第三次同形狀失效直接執行帳本回退，不需要再開一組對照。**
- **不需要為 PFAS／關稅到期加新的 LLM 閘或新的證據軸。** 兩版判斷者表現相同，差別只在閘給紅給黃。這是**閘的職責書**問題（要不要把 dir=0 的法規 finding 列為必答），改一句話即可，不要加模型、不要加軸。
- **不需要再爭 `decision_inputs` 三欄（`ev5y_pct`／`irr_base_pct`／`asym_ratio`）該不該手填。** Codex 已裁定：腳本回填是現行契約。**請直接改閘的 checklist 把這條刪掉**——它在 A 與 B 的 gate_audit 各占一條 🟡，兩次都是假警報，還誘使 A 的判斷者把非證據塞進 `evidence_dismissed[]`。
- **不需要為 `endo_ceiling` 再蓋一套公式。** A 與 B 用兩條完全不同的路徑都湊到 15%——問題不在判斷者，在規則對「負營運資金業務」只寫了「改以 ROIIC 為上界」而 ROIIC 在這種業務上會爆到 300%。**在 `roic-durability.md` 補一句「ROIIC 無界時改用實體產能或人力供給約束，並明寫所用約束」**，一句話收掉，不要另立模組。
- **不需要回頭重跑或修補 A、B 這兩份 run。** 兩份都不發布，本報告的作用是規格輸入。

---

## 附：本次檢查的邊界

- 未跑任何模型、未 commit、未 push、未改任何正式檔（本檔為唯一新增）。
- 唯讀探針：兩份 `judgment.json`／`scenario.json`／`scenario_meta.json`／`gate_audit.md`／`manifest.json`／`agents/*.json` 逐欄比對；`validate_judgment.py --report` 對 A 與 B 各跑一次（新版 validator，`--evidence`）；`gen_dd_tables` 七張表對 A／B 各渲染一次數非空格數；兩份 brief HTML 全文抽取比對；`evidence.json` 13 條 `direction=-` finding 的引用可達性程式比對；`git diff 77aec95a8 0e2a6c973` 對 `judgment-rules.md`／`judge.md.tmpl`／`judgment.schema.json`／`validate_judgment.py`／`gen_dd_tables.py`。
- **未做**：13 條反證的金融真偽查證、任何投資建議、FIX 的估值獨立複算（EV 分解為算術重算，非重估）、`--full` 散文段（本輪未產）。
- 標的僅為測試案例，本檔不構成對 FIX 的投資意見。
