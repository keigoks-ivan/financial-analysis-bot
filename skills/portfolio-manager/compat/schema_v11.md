# DD v11.x → 中性訊號層映射

## 來源欄位（INDEX.md v11 格式，8 欄）

```
| 日期 | Ticker | 版本 | 裁決 | 陷阱 | 品質/短R/中R | 檔名 | 備註 |
```

範例行：
```
| 2026-04-17 | FN | v11.0 | 迴避 | 🟢 非陷阱 | A / −0.65x / −0.55x | DD_FN_20260417.html | ... |
```

## 映射規則

### `quality_tier`
取第 6 欄「品質/短R/中R」的第一個 token：
- `A` → `A`
- `B` → `B`
- 其他（如 C / 拒絕）→ 原值

v11 無 `S` 級；若 quality_tier = A 且 HTML §9 護城河 = 10 分 → 升級為 `S`（需 fetch HTML 確認，可選）。

### `gate`
取第 4 欄「裁決」：

| v11 裁決 | gate |
|:---|:---|
| 進場 | 🟢 |
| 觀望偏進場 | 🟡 |
| 觀望 | 🟠 |
| 迴避 | 🔴 |

### `trap`
直接取第 5 欄「陷阱」：
- `🟢 非陷阱` → `🟢`
- `🟡 觀察期` → `🟡`
- `🔴 高風險陷阱` → `🔴`

### `ma_status`（v11 無此欄，由 Bollinger 推導）
v11 的 §2 F 使用 Bollinger Band 2σ 判定（偏貴 / 合理 / 偏宜）。映射：
- Bollinger「偏宜（下軌之下）」→ `🟢 最佳`
- Bollinger「合理（軌道之間）」→ `✅ 強勢`
- Bollinger「偏貴（上軌之上）」→ `🟡 減半`

若需更精準的 W52/W104/W250 狀態，由 PM skill 執行管線第 4 步的 yfinance 重算一次（保守作法）。

### `entry_price` / `short_target` / `mid_target` / `bear_price`
從 HTML §2 E「雙時距目標價與 R:R」表格取：
- `entry_price`：若 §2 F 有標「建議進場價」，取之；否則用 W52 Low 或 Bear 股價（保守）
- `short_target`：§2 E 短期目標價
- `mid_target`：§2 E 中期目標價
- `bear_price`：§2 E Bear 股價（短期）

若 HTML 取不到（例如 INDEX.md 只有備註欄），由 PM skill 直接用當日現價判斷是否在合理區間，entry_price 可留 `null`。

### `final_signal`（v11 → 綜合訊號燈）

| v11 組合 | final_signal |
|:---|:---|
| 進場 + A 級 + 🟢 非陷阱 | **A+** |
| 進場 + A 級 + 🟡 觀察期 | **A** |
| 觀望偏進場 + A 級 | **A**（降一級） |
| 觀望偏進場 + B 級 | **B** |
| 觀望 | **C** |
| 迴避 或 🔴 高風險陷阱 | **X** |

## 推導限制

v11 無獨立 MA 狀態機與大盤豁免層（皆已內建於裁決中），因此：
- `benchmark_regime` 需由 PM skill 自己用 yfinance 查詢
- 若 benchmark < W104，PM skill 的決策引擎**不做二次 degrade**（避免雙重懲罰），但在 HTML §7 資訊性敘述中標註

## 範例：FN（2026-04-17）

```yaml
ticker: FN
dd_version: v11.0
dd_date: 2026-04-17
quality_tier: A
gate: 🔴                     # 「迴避」
trap: 🟢                     # 「非陷阱」
ma_status: 🟡                # Bollinger 上軌之上
final_signal: X              # 迴避 → X
entry_price: ~353            # 短期目標價（§2 E）
short_target: 353
mid_target: 425
bear_price: 183
```

PM 裁決：現持倉清倉；未持倉不納入候選。
