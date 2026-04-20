# Thesis Classification Tag（事件型 vs 結構型）

**用途**：每條 §12 Non-Consensus thesis 必須自標分類，決定 refresh 節奏（QC-I22）。

---

## 分類定義

### 🟠 Event-Triggered Thesis（14 天 refresh）

**特徵**：引用具體、可變動的 data point 作為 thesis 基石。

**典型 pattern**：
- 具體 yield 數字："Samsung SF2P 達 70% yield"
- 具體訂單 / 簽約："Intel 18A 2026-2027 基本 in-house only"
- backlog 絕對值："GEV 83 GW backlog 已售至 2030"
- 併購 / 股權："AMAT/LRCX 對 BESI 併購傳聞"
- 產能 sold out 時序："Samsung HBM4 Feb 2026 量產"

**風險**：data 過期 14 天就可能讓 thesis 基石動搖。

**發布前檢查**：必須在發布日前 14 天內用 WebSearch 重新檢索所有引用的具體事件。

---

### 🟢 Structural Thesis（60 天 refresh 足夠）

**特徵**：基於物理定律、經濟學原理、歷史類比、產業結構 — 不依賴某個具體數字的當下狀態。

**典型 pattern**：
- 物理 / 材料定律："HBM 消耗 3x DRAM wafer per GB"
- 經濟學原理："Jevons 效應 — 推論成本下降反而擴大 TAM"
- 歷史類比："COUPE 重演 CoWoS 獨家路徑（2017→2024 = 7 年）"
- 產業結構論："Scale-up 與 Scale-out 是兩個獨立市場"
- 生態位論述："TSMC HBM base die 是新收入切片"

**風險**：較低，基礎邏輯不易在 14 天內崩潰。

**發布前檢查**：60 天內 refresh 即可。

---

### 🟡 Hybrid Thesis（兩種節奏都跑）

**特徵**：結構論 + 引用具體數字支撐。

**典型 pattern**：
- "BSPDN 是 2027-2028 真護城河（TSMC A16 H2 2026 首發）" — 結構論 + 具體時程
- "Gas turbine 2030+ 主力（GEV backlog $150B）" — 結構論 + 具體數字

**發布前檢查**：
1. 對「結構論」部分 → 60 天 refresh
2. 對「引用具體數字」部分 → 14 天 refresh
3. 以較嚴格者為準

---

## 八份 ID v1.0.1 thesis 分類對照表

| ID | Thesis | 分類 |
|:---|:---|:---|
| AI Accelerator | ① Jevons 推論需求是 run-rate | 🟢 Structural |
| AI Accelerator | ② 2027 非峰值是轉折 | 🟢 Structural |
| AI Accelerator | ③ 電力永久瓶頸 + FLOPS/W | 🟢 Structural |
| AP | ① BESI 應類比 ASML | 🟡 Hybrid |
| AP | ② Rubin Ultra 4→2 揭物理極限 | 🟠 Event |
| AP | ③ ASE 成長是量非質 | 🟡 Hybrid |
| HBM | ① Samsung HBM4 份額 35% | 🟠 Event |
| HBM | ② HBM 脫離 DRAM 週期 | 🟢 Structural |
| HBM | ③ TSMC base die 隱性贏家 | 🟡 Hybrid |
| LEN | ① Samsung 2nm 2028 市佔 15%+ | 🟠 Event |
| LEN | ② Intel 18A 無外部客戶 | 🟠 Event（**已被反證**） |
| LEN | ③ TSMC A16 backside power | 🟡 Hybrid |
| Networking | ① Scale-up/out 二分法 | 🟢 Structural |
| Networking | ② UALink 商用 2027+ | 🟠 Event |
| Networking | ③ Credo + Astera 稀缺 | 🟡 Hybrid |
| AI DC | ① VRT 比 NVDA 更安全 | 🟡 Hybrid |
| AI DC | ② GEV gas turbine 2030+ 主力 | 🟢 Structural |
| AI DC | ③ ETN Boyd 結構轉型 | 🟡 Hybrid |
| SiPho | ① CPO 2026 H2 商用 | 🟠 Event |
| SiPho | ② pluggable + CPO 並存 | 🟡 Hybrid |
| SiPho | ③ TSMC COUPE 重演 CoWoS | 🟢 Structural |
| LC | ① CDU 是瓶頸 | 🟡 Hybrid |
| LC | ② Immersion 2028+ 超 DTC | 🟠 Event |
| LC | ③ Asetek 被低估 | 🟠 Event |

---

## 觀察：C / D 級 ID 基本是 Event-heavy

HBM ID（6.0）和 LEN ID（5.5）分數最低的原因是**三條 thesis 裡 2-3 條為 Event-triggered**，一旦 data 過期就 thesis 動搖。相對地，SiPho ID（8.2）雖也有 Event thesis，但 data refresh 貼近發布日故傷害小。

**啟示**：若 ID 的三條 thesis 全是 Event-triggered → 風險高，應至少加一條 Structural；若全 Structural → 可能偏學術，需至少一條 Event 連結當下。

---

## 版本歷史
- 2026-04-19 v1.0：初版
