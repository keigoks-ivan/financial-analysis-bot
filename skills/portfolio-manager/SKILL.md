---
name: portfolio-manager
version: v1.0
released: 2026-04-18
description: "基金經理人（PM）技能：以中長期成長股為 mandate，對現有組合做複盤裁決（賣出 / 減碼 / 加碼 / 新進 / 續抱 / 現金部位）。採 core(≤5) + satellite(≤3) 結構，現金殘差式（5% 硬性下限，無上限）。所有個股判斷引用 docs/dd/ 已存在的 DD 報告（分析師角色），PM 不做單股研究，只做組合決策。內建 v11/v12 相容層與 4 級 override 協議（L1 Sizing / L2 Horizon / L3 Information / L4 Thesis，direction override 預設禁止）。觸發：用戶提供持倉表、要求組合複盤、調整配置、rebalance、現金部位建議時。"
---

# 基金經理人（PM）技能 v1.0

## 【哲學三原則】

1. **分工純粹**：DD（stock-analyst）負責個股 direction（買 / 賣 / 迴避），PM 負責 sizing + 組合決策。PM 不做單股研究。
2. **跨版本穩定**：DD schema 從 v11 升 v12 升 v13，PM 決策引擎不動。依靠中性訊號層（Layer 2）吸收版本差異。
3. **有摩擦的 override**：direction override 預設禁止；sizing override 允許且留痕。4 級協議用來放大紀律，不是削弱紀律。

---

## 【PM Mandate】

| 項目 | 規則 |
|:---|:---|
| 投資風格 | 中長期持有成長股（3-5 年） |
| 核心持股 | 最多 **5 檔**，單檔目標上限 **20%**，類別總上限 **95%** |
| 衛星持股 | 最多 **3 檔**，單檔目標上限 **7%**，類別總上限 **21%** |
| 現金 | 硬性下限 **5%**，無上限（可 100% 現金） |
| 最低持股 | **無**（狀況不好可全現金） |
| 現金決定機制 | 殘差式：cash = 100% − Σ(合格股票倉位) |

### 現金政策（bottom-up，非 benchmark 驅動）

- **benchmark 狀態不直接決定現金水位**。benchmark 只透過 DD 的大盤豁免層影響個股 gate 評分。
- 若大盤差但找到強股票（DD gate degrade 後仍 🟢/🟡）→ 可以買到 95%。
- 若大盤好但候選池空（無股票通過 core/satellite 門檻）→ 現金自然上升。
- 若現金 > 30%，HTML §6 以一句話敘述**成因**（pool 空 / 降級 / 主動減碼），不視為警訊。

---

## 【三層架構】

```
Layer 3：PM 決策引擎
          └─ 個股矩陣 + 組合檢核 + override 協議 + Rebalance 建議
                  ↑（只依賴中性欄位）
Layer 2：中性訊號層
          └─ final_signal / quality_tier / gate / trap / entry_price / targets
                  ↑（相容層 compat/schema_vXX.md）
Layer 1：DD 原始輸出
          └─ v11.x / v12.x / ...（docs/dd/*.html + INDEX.md）
```

升級 DD schema 時只改 Layer 2 映射表，Layer 3 不動。

---

## 【輸入格式｜config.yaml】

```yaml
portfolio:
  base_currency: USD            # USD / TWD
  total_nav: 1000000
  as_of_date: 2026-04-18
  holdings:
    - ticker: NVDA
      cost_basis: 120.50
      current_pct: 8.5          # 當前佔組合 %
      entry_date: 2025-11-15
      tier: core                # core / satellite（使用者或 PM 指定）
      notes: "建倉於 GTC 前"
    - ticker: MSFT
      cost_basis: 380.00
      current_pct: 6.2
      entry_date: 2025-09-01
      tier: core

benchmark: SPX                  # SPX / QQQ / TAIEX
risk_appetite: moderate         # conservative / moderate / aggressive

watchlist:                      # 強制納入候選池（即使 INDEX.md 沒有）
  - COHR
  - LLY

override_policy:
  allow_l1_sizing: true         # 預設 true
  allow_l2_horizon: true
  allow_l3_information: true    # 自動觸發 DD 重跑
  allow_l4_thesis: false        # 預設 false（僅 DD invalid 時解鎖）

sector_caps:                    # 可選
  semiconductor: 50             # core+satellite 合計該 sector 不超過
  software: 30

theme_caps:                     # 可選
  ai_infrastructure: 60
```

若使用者未提供 YAML，PM skill 以互動式問答收集（ticker + 成本 + 目前 %），不中斷執行。

---

## 【Layer 2｜中性訊號層】

每檔 ticker 從 DD 映射到下列中性欄位，PM 決策引擎只讀此層。

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `ticker` | str | 代號 |
| `dd_version` | str | "v11.0" / "v12.0" 等（取自 INDEX.md 第 3 欄） |
| `dd_date` | date | DD 報告日期 |
| `dd_age_days` | int | 與今日差距 |
| `current_price` | float | yfinance 當日收盤 |
| `final_signal` | enum | A+ / A / B / C / X（綜合訊號等級，見下表）|
| `quality_tier` | enum | S / A / B / C / 拒絕 |
| `gate` | enum | 🟢 / 🟡 / 🟠 / 🔴 |
| `trap` | enum | 🟢 / 🟡 / 🔴 |
| `entry_price` | float | DD 建議進場價（§2 E / §2 H） |
| `short_target` | float | DD 短期目標價 |
| `mid_target` | float | DD 中期目標價 |
| `bear_price` | float | DD Bear Case 股價 |
| `ma_status` | enum | 🟢最佳 / ✅強勢 / 🟡減半 / 🟡觀察 / 🟠暫不 / ❌失效（v12；v11 用 Bollinger 推導） |
| `benchmark_regime` | enum | 正常 / 破W104 / 破W250（取自當日 yfinance）|
| `stale` | bool | dd_age > 14 |
| `invalid` | bool | dd_age > 30，或 DD 後發生財報/重大事件 |

### final_signal 綜合燈號

Layer 2 把 DD 多軸訊號合成單一字母燈號，給 Layer 3 使用：

| 燈號 | 條件（DD 訊號組合） | 語意 |
|:---|:---|:---|
| **A+** | quality S/A + gate 🟢 + MA 🟢/✅ + trap 🟢 + benchmark 正常 | 滿格進場訊號 |
| **A** | quality S/A + gate 🟡 + MA ✅ + trap 🟢 | 進場訊號 |
| **B** | quality B + gate 🟢/🟡 + trap 🟢/🟡，或 A 級有一項訊號減半 | 衛星級別 |
| **C** | 多項訊號減半 / 觀察池狀態 | watchlist 追蹤 |
| **X** | trap 🔴 / gate 🔴 / MA ❌ / quality 拒絕 | 追蹤或立即處置 |

---

## 【Layer 3｜個股決策矩陣】

對每檔 **holding** 套用：

| final_signal | 持倉裁決 | Override 允許級別 |
|:---|:---|:---|
| trap 🔴 或 X（任一） | **清倉** | L1 only（sizing 降為 0 是 direction，不在 L1 範圍 → 不可 override）|
| invalid（dd_age > 30 或財報後） | **暫停裁決 + 強制重跑 DD** | — |
| A+ + 現價 ≤ entry × 1.05 | **加碼候選** | L1/L2/L3 |
| A+ + 現價 > entry × 1.05 但 < short_target | **續抱** | L1/L2 |
| A + 現價 ≤ entry × 1.05 | **加碼候選**（但低於 A+）| L1/L2/L3 |
| A | **續抱** | L1/L2 |
| B + stale | **觀察 + 刷新 DD 建議** | L1/L2 |
| B | **續抱** | L1/L2 |
| C | **減碼觀察** | L1/L2/L3 |
| 現價 > mid_target × 1.2 | **減碼 30%**（超漲止盈） | L1（只能更保守） |

### 新進候選篩選（對 **watchlist + INDEX.md 未持有**）

| 類別 | 門檻 |
|:---|:---|
| **核心候選** | final_signal A+ 或 A ＋ quality S/A ＋ trap 🟢 ＋ sector 未超 cap ＋ 核心位置 < 5 檔 |
| **衛星候選** | final_signal B ＋ trap 🟢/🟡 ＋ sector 未超 cap ＋ 衛星位置 < 3 檔 |
| **不納入** | final_signal C / X，或現價已 > short_target × 1.1（追高） |

### 目標倉位分配（核心 / 衛星）

| 類別 | 單檔目標 % | 觸發加碼至目標的條件 |
|:---|:---|:---|
| Core | 15-20% | A+ 訊號 + 現價 ≤ entry × 1.05 + MA 🟢/✅ |
| Core 初建倉 | 5-10% | A+ 訊號但現價偏高，先建 1/3 位置 |
| Satellite | 3-7% | B 訊號 + trap 🟢/🟡 |

---

## 【組合級檢核】（可覆寫個股裁決）

| 檢核項 | 觸發條件 | 效果 |
|:---|:---|:---|
| 類別檔數上限 | core ≥ 5 / satellite ≥ 3 | 新進凍結該類 |
| 單檔上限 | core > 20% / satellite > 7% | 自動 trim 建議 |
| 單檔下限 | 任一倉位 < 2% | 建議清倉（位置太小，佔 slot）|
| Sector cap | 某 sector 合計超過 cap | 該 sector 新進凍結 |
| Theme cap | 某主題合計超過 cap | 該主題新進凍結 |
| 現金下限 | cash < 5% | 強制 trim 最低 conviction 倉位 |
| Top 3 集中度 | > 60% 組合 | 警示，但不強制 trim（growth PM 允許集中）|
| 大盤豁免 | benchmark < W104 | **不影響 PM 層現金**；已透過 DD gate degrade 影響個股 |

---

## 【Override 4 級協議】

### 核心原則
**Direction 不可 override，Sizing 可 override。** 所有 override 必須寫入 HTML §8，附 reversal condition。

### 四級定義

| 級 | 類型 | 合法範圍 | 強制欄位 | 預設 |
|:---|:---|:---|:---|:---|
| 🟢 **L1 Sizing** | 方向不變，調整大小 | 例：DD 給 A+ 訊號，PM 因集中度只給 10% | reason | 允許 |
| 🟡 **L2 Horizon** | 持有期變更 | 例：DD 3-5 年持有，PM 因現金流需求縮為 6 月 | reason + **退出條件** | 允許 |
| 🟠 **L3 Information** | 新資訊 DD 未納入 | 例：DD 2 週前寫，期間發生併購 / 法規變動 | **具體資訊來源** + reversal condition + **自動觸發 DD 重跑** | 允許 |
| 🔴 **L4 Thesis** | 不同意 DD 方向 | 例：DD 說迴避，PM 仍想買 | 僅 dd_invalid = true 可解鎖；**強制重跑 DD 而非 override** | **禁止** |

### L3 自動觸發機制
執行 L3 override 時，PM HTML 必須在 §8 標註：「下次應重跑 stock-analyst [TICKER]」。此為提示，不自動執行（避免誤觸發深研究）。

### Reversal Condition 強制性
每個 override 必須寫「什麼條件觸發此 override 失效」。例：
- L1 sizing：「待集中度紓解至 < 30%，回到 DD 建議倉位」
- L2 horizon：「若 6 個月後現金流無需求，回到 DD 3-5 年持有期」
- L3 information：「下次 DD 重跑後若新資訊確認正面則加碼，若負面則清倉」

### 偏誤統計
HTML §8 末尾列「本 PM 歷史 override 統計」：
- 累積 L1-L4 次數
- 事後 DD 重跑確認率（L3）
- 若 L3 確認率 < 50% → 警示「PM 信息層判斷偏差」

---

## 【PM-QC 強制規則（8 條）】

每份 PM 報告必須符合下列規則，不得跳過：

### PM-QC-1｜L4 Thesis Override 預設禁止
L4 override 只有在 dd_invalid = true 時可解鎖，且必須先重跑 DD。禁止以「我覺得 DD 錯」為理由繞過。

### PM-QC-2｜時效性分級
- dd_age > 14 天 → 標註 `stale`，gate/trap 降信心度
- dd_age > 30 天 → 標註 `invalid`，強制暫停該標的裁決並建議重跑

### PM-QC-3｜Reversal Condition 強制
所有 L1-L3 override 必須寫 reversal condition；未寫的 override 直接被拒絕（不納入最終建議）。

### PM-QC-4｜紀律突破顯示警示色
下列情況必須在 HTML 以紅 / 黃標示：
- 單檔 > 目標上限
- 單檔 < 2%
- sector / theme / core / satellite 超 cap
- 現金 < 5%

### PM-QC-5｜現金 bottom-up 禁止 benchmark 硬性上下限
禁止以「benchmark < W104」為由要求組合現金 ≥ X%。benchmark 狀態只透過 DD 個股 gate degrade 影響候選池，不直接影響 PM 層現金水位。

### PM-QC-6｜現價當日 refresh
holdings + watchlist 的現價必須用 yfinance 當日收盤，禁止使用 DD 報告內的過期價。

### PM-QC-7｜Override 累積偏誤統計
HTML §8 必須列本 PM 歷史 override 次數與確認率，供自省。若 `docs/pm/` 下無歷史 PM 報告，標註「首次執行，無歷史統計」。

### PM-QC-8｜執行不中斷
所有資料缺口標註「資料限制」後繼續執行。不中斷詢問使用者。例外：使用者完全未提供 portfolio state，此時互動式問答（僅一次）收集後進入靜默執行。

---

## 【執行管線】

1. **讀 config** → portfolio state（若無 YAML，互動式收集一次）
2. **讀 `docs/dd/INDEX.md`** → 建 ticker → 最新 DD 索引
3. **Layer 2 相容層解析**：
   - 解析 INDEX.md 第 3 欄（版本字串）
   - v11.x → `compat/schema_v11.md` 映射
   - v12.x → `compat/schema_v12.md` 映射
   - 產出每檔 holding / watchlist 的中性訊號層物件
4. **yfinance 批次 refresh**：
   - 所有 holdings + watchlist + benchmark 當日收盤
   - benchmark 的 W104 / W250 週均值（判斷 benchmark_regime）
5. **時效性檢查**：標註 stale / invalid
6. **個股決策矩陣**：對 holdings 套持倉裁決；對 watchlist + INDEX A/S 級未持有 套新進篩選
7. **組合級檢核**：sector / theme / core / satellite / 單檔上下限
7.5. **ID 曝險聚合（v1.1 新增，2026-04-19）**：
   - 讀 `docs/id/INDEX.md`（若不存在 → 跳過此步）
   - 對每份 ID，讀取其 §11 關聯個股清單的 ticker list
   - 計算「組合曝險」：Σ（持倉 % × tier 權重）
     - 🔴 核心 = 1.0、🟡 次要 = 0.6、🟢 邊緣 = 0.3
   - 輸出：`{"ID_AdvancedPackaging": {"raw_pct": 58, "weighted_pct": 52, "holdings": ["NVDA 18", "2330 12", "ASML 10", "AVGO 8", "MRVL 6", "CRDO 4"]}}`
   - **警示規則**：
     - 單一 ID raw 曝險 > 40% → HTML §7 加 ⚠️ 警示
     - 單一 ID 若 §13 Falsification 任 1 條觸發 → 加 🔴 紅字警示「相關持倉須 review」
     - ID stale：若命中 ID 的 judgment 段已過 60 天 → 加「引用 ID 判斷層過期」提示
8. **Override 協議**：收集所有 PM 與 DD 之間的 deviation，分類 L1-L4
9. **Rebalance 建議**：產出 after-rebalance 目標配置（含現金）
10. **HTML 輸出**：`docs/pm/PM_YYYYMMDD.html`
11. **INDEX.md 更新**：append 到 `docs/pm/INDEX.md`
12. **首頁同步**：執行 `python scripts/update_pm_index.py`（若腳本不存在，則提示使用者手動建立）
13. **Git commit + push**（依 MEMORY feedback）

---

## 【HTML 輸出章節】

### 章節順序

| § | 標題 | 內容 |
|:---|:---|:---|
| §1 | 組合快照 | NAV / 現金 / core + satellite 分布 / top 5 持倉 / Beta 加權（可選） |
| §2 | 個股複盤表 | 每檔 holding × 中性訊號層 × PM 裁決 × override 旗標 |
| §3 | 🔴 賣出 / 減碼清單 | 每檔一段：理由 + 引用 DD 章節 + 現價距目標 |
| §4 | 🟢 加碼清單 | 觸發價 + 目標加至 % + 條件 |
| §5 | 🟡 新進候選池 | 核心候選 / 衛星候選 分開列，含門檻通過情形 |
| §6 | ⚪ 維持名單 | gate / trap 未變化的持倉 |
| §7 | 組合風險敘述 | 集中度 / 主題 / sector / benchmark 狀態（資訊性） / 現金成因 |
| **§7.5** | **ID 曝險矩陣（v1.1 新增）** | **每份 ID × raw% × weighted% × 涵蓋持倉清單；單 ID > 40% 警示；§13 觸發紅字** |
| §8 | Override 清單 | 本次 L1-L4 明細 + reversal condition + 歷史累積統計 |
| §9 | Rebalance 建議 | after-rebalance 目標配置表 + pie chart（文字版）+ 執行順序 |

### §7.5 ID 曝險矩陣範例

```
┌─────────────────────────────────────────────────────────────────────┐
│ ID 主題                  │ raw%  │ weighted% │ 涵蓋持倉（% × tier）      │
├─────────────────────────────────────────────────────────────────────┤
│ ID_AdvancedPackaging ⚠️  │ 58%   │ 52%       │ NVDA 18🔴 / 2330 12🔴 / │
│ (judgment 🟢)            │       │           │ ASML 10🔴 / AVGO 8🟡 /   │
│                          │       │           │ MRVL 6🟡 / CRDO 4🟢      │
├─────────────────────────────────────────────────────────────────────┤
│ ID_AIAcceleratorDemand   │ —     │ —         │ ID 未建                 │
│ ID_HBM_Supercycle        │ —     │ —         │ ID 未建                 │
└─────────────────────────────────────────────────────────────────────┘

⚠️ 單一 ID 曝險 > 40%：需評估是否主題過度集中
💡 若 §13 Falsification 條件觸發 → 相關持倉建議同步 review
```

### PM-QC-9｜ID 曝險警示強制（v1.1 新增）

若任何 ID raw 曝險 > 40%，HTML §7 必須**文字敘述該集中度成因**，並在 §9 Rebalance 建議列「若要降低主題集中度，優先 trim 哪幾檔」。若曝險 > 60%，直接在頁首紅字警示。

### 視覺規格（沿用 DD v12 style）
- 主背景 #F8FAFC，卡片白底
- 章節標題深藍 #1E3A5F + accent 線 #3B82F6
- 字型：Noto Sans TC + IBM Plex Mono
- 裁決標記：🔴 賣出 / 🟢 加碼 / 🟡 觀察 / ⚪ 維持
- Override 標記：L1 綠 / L2 黃 / L3 橘 / L4 紅
- 頁首固定：組合日期 ｜ NAV ｜ 現金% ｜ PM Skill v1.0
- 頁尾按鈕：列印為 PDF

---

## 【檔案結構】

```
~/.claude/skills/portfolio-manager/
  SKILL.md                          # 主 skill（本檔）
  compat/
    schema_v11.md                   # v11 → 中性層映射
    schema_v12.md                   # v12 → 中性層映射
  policies/
    decision_matrix.md              # 個股 + 組合矩陣詳版
    override_protocol.md            # 4 級協議詳版
  templates/
    config_example.yaml             # 輸入範例
    html_template.md                # HTML 視覺規格
```

輸出：
```
financial-analysis-bot/
  docs/pm/
    INDEX.md                        # PM 報告索引
    PM_20260418.html                # 當日 PM 報告
  scripts/
    update_pm_index.py              # 首頁同步腳本（沿用 DD 模式）
```

---

## 【INDEX.md 格式】

每份 PM 報告 append 一行到 `docs/pm/INDEX.md`，格式（9 欄）：

```
| YYYY-MM-DD | NAV | 現金% | 核心檔數 | 衛星檔數 | 主要動作 | Override | 檔名 | 備註 |
```

範例：
```
| 2026-04-18 | $1.0M | 12% | 4/5 | 2/3 | 賣 FN / 加 COHR | L1×1, L3×1 | PM_20260418.html | - NVDA 維持 20% 滿倉<br>- FN Trap 🟢 但估值燈🔴 → 清倉<br>- COHR A+ 訊號觸發新進 15% |
```

---

## 【Terminal 摘要格式】

HTML 生成後，terminal 輸出：

```
✅ PM 複盤完成：YYYY-MM-DD
📄 檔案：docs/pm/PM_YYYYMMDD.html
💼 組合現況：NAV $__ ｜ 現金 __% ｜ 核心 _/5 ｜ 衛星 _/3
📊 主要動作：
  - 🔴 賣出：[ticker list]
  - 🟢 加碼：[ticker list]
  - 🟡 新進：[ticker list]
  - ⚪ 維持：[ticker count] 檔
🏛 Override：L1×_ / L2×_ / L3×_ / L4×_
🔗 首頁同步：[✅ 成功 / ❌ 失敗]
```

---

## 【啟動觸發】

使用者提及下列任一情境時自動觸發本 skill：
- 「幫我複盤組合」/「portfolio 複盤」/「rebalance」
- 提供持倉 ticker + % 並詢問「要怎麼調整」
- 「哪些該賣」/「哪些該買」
- 現金部位建議
- 單一 ticker 問「要不要加碼 / 減碼」時，若使用者已有組合上下文，優先走 PM skill（引用 DD）而非重跑 stock-analyst

觸發後直接進入執行管線，不問模式選擇。若 config.yaml 缺，一次性互動收集後靜默執行。
