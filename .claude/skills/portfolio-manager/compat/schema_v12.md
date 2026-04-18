# DD v12.x → 中性訊號層映射

## 來源欄位（INDEX.md v12 格式，8 欄，與 v11 相同結構）

```
| 日期 | Ticker | 版本 | 最終建議 | 陷阱 | 品質/估值燈/MA | 檔名 | 備註 |
```

v12 的第 4 欄改為「最終建議」（進場 X% / 追蹤池 / 拒絕），第 6 欄擴充為「品質 / 估值燈 / MA」。

## 映射規則

### `quality_tier`
直接取 §2 B 護城河等級：`S` / `A` / `B` / `C` / `拒絕`。

體質 veto 若觸發降級，以**調整後等級**為準（INDEX 備註欄通常已寫調整後值）。

### `gate`
v12 將裁決拆為「估值燈 × MA 狀態」兩軸。映射規則：
- 估值燈 🔴 或 MA ❌ → `🔴`
- 估值燈 🟠 或 MA 🟠 → `🟠`
- 估值燈 🟡 或 MA 🟡 → `🟡`
- 估值燈 🟢 且 MA 🟢/✅ → `🟢`

取**較嚴**的一個（例：估值燈 🟢 但 MA 🟠 → `🟠`）。

### `trap`
直接取 §1 陷阱定性：`🟢` / `🟡` / `🔴`。

### `ma_status`
直接取 §2 F Pure MA 狀態：
- `🟢 最佳進場` / `✅ 強勢進場` / `🟡 減半進場` / `🟡 觀察池` / `🟠 暫不進場` / `❌ 系統失效`

### `benchmark_regime`
直接取 §2 G 大盤豁免：
- `正常` → `正常`
- `破 W104` → `破W104`
- v12 無 W250 判定；PM skill 自行補查

### `entry_price` / `short_target` / `mid_target` / `bear_price`
取 §2 E「R:R 與 Bear Case（參考用）」表格：
- `entry_price`：§2 F 若標「DD 建議進場價」取之；否則用 bear_price 作保守錨點
- `short_target`：§2 E 短期目標價
- `mid_target`：§2 E 中期目標價
- `bear_price`：§2 E Bear 股價（短期）

### `final_signal`

v12 的 §2 H 雙軌矩陣已產出訊號強度。映射：

| §2 H 訊號組合 | final_signal |
|:---|:---|
| quality S/A + gate 🟢 + MA 🟢/✅ + trap 🟢 | **A+** |
| quality S/A + gate 🟡 + MA ✅ + trap 🟢 | **A** |
| quality B + gate 🟢/🟡 + trap 🟢 | **B** |
| quality C + gate 🟢 + trap 🟢 | **B**（降一級）|
| 任一 MA 🟡/🟠 + gate 🟡+ | **B**（MA 減半）|
| 任一 MA ❌ 或 gate 🔴 或 trap 🔴 或 quality 拒絕 | **X** |
| 其他訊號混合 | **C**（觀察）|

## v12 特有訊號（PM 層保留引用）

### 體質 veto 調整
若 §2 B 顯示「調整後等級」低於原等級（例：A → B，因體質 veto 2 項不過），PM 層採用**調整後等級**作為 quality_tier。

### 壓力測試通過率（§2 E QC-29）
v12 記錄「壓力測試通過率 X/4」。PM 層若 < 3/4 → final_signal 降一級（即使其他條件滿分）。

### 估值燈升級規則
v12 §2 D「估值燈 🟢」觸發「等級 +1」。此升級效果**只在 DD 層內作用於 §2 H**，PM 層的 quality_tier 仍取原始等級（§2 B 調整後），避免雙重加分。

## 範例：假設未來 CAMT v12（2026-05-01）

```yaml
ticker: CAMT
dd_version: v12.0
dd_date: 2026-05-01
quality_tier: A              # §2 B 調整後 A
gate: 🔴                     # 估值燈 🔴 過熱
trap: 🟢
ma_status: ✅
benchmark_regime: 正常
final_signal: X              # gate 🔴 → X
entry_price: ~220
short_target: 280
mid_target: 340
bear_price: 165
```

PM 裁決：現持倉視 gate 嚴重度決定清倉或減碼；未持倉不納入候選。
