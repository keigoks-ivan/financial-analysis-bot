# Override 4 級協議詳版

## 核心原則

**Direction 不可 override，Sizing 可 override。**

| 允許 | 不允許 |
|:---|:---|
| 改變倉位大小（在 DD 方向同側） | 把「迴避」改成「買」 |
| 縮短持有期（保留方向） | 把「進場」改成「賣」 |
| 基於新資訊調整（觸發重跑）| 基於直覺否決 DD |

所有 override 必須寫入 HTML §8，附 **reason** + **reversal condition** + **開啟日期**。

---

## L1｜Sizing Override

**定義**：DD 方向不變，PM 因組合紀律調整大小。

**典型情境**：
- DD 給 NVDA A+ 訊號，目標 20% 核心倉位。PM 因半導體 sector 已 40% → L1 override 至 10%。
- DD 給 CRDO B 衛星 5%，PM 認為主題過熱，L1 override 至 3%。

**強制欄位**：
- `reason`: 文字（為什麼調整 sizing）
- `from`: DD 建議
- `to`: PM 決定
- `reversal_condition`: 什麼條件下回到 DD 建議（例：「半導體 sector 降至 < 30%」）

**自動化**：無

---

## L2｜Horizon Override

**定義**：DD 持有期變更，PM 因現金流或組合需求縮短持有。

**典型情境**：
- DD 建議 LLY 3-5 年持有。PM 6 個月後需提領 30% 現金買房 → L2 override 至 6 個月內減碼。
- DD 建議 GOOGL 中長期持有。PM 想把一半換成 satellite 倉位做主題押注 → L2 override。

**強制欄位**：
- `reason`: 文字
- `new_horizon`: 新持有期（月/年）
- `original_horizon`: DD 建議持有期
- `reversal_condition`: 何時回到原持有期（例：「現金流需求解除後」）
- `exit_plan`: 具體出場路徑

**自動化**：無

---

## L3｜Information Override

**定義**：PM 掌握 DD 未納入的新資訊。

**典型情境**：
- DD 2 週前出稿，期間標的發布負面 guidance → PM 需比 DD 更保守 → L3 override 減碼。
- DD 建議迴避，但之後出現催化劑（併購 / 法規鬆綁 / 重大客戶）→ L3 override 先小額試倉。
- 同產業對手財報爆雷，DD 未及時更新 → L3 override 減碼該產業所有持倉。

**強制欄位**：
- `reason`: 文字
- `info_source`: 具體資訊來源（URL / 日期 / 媒體名稱）
- `info_date`: 資訊公開日
- `reversal_condition`: 下次 DD 重跑後若資訊被確認為正/負 → 對應行動
- **`trigger_dd_rerun`: true**（自動標記，提示下次執行 stock-analyst）

**自動化**：PM HTML §8 末尾自動列出「待重跑 DD 標的清單」。

**確認機制**：下次 DD 重跑後，PM 報告比對「L3 判斷」與「新 DD 結論」：
- 方向一致 → `confirmed`
- 方向相反 → `rejected`
- 歷史統計用於偵測 PM 資訊層偏誤

---

## L4｜Thesis Override

**定義**：PM 不同意 DD 方向。

**預設：禁止。**

**唯一解鎖條件**：`dd_invalid = true`（dd_age > 30 天 或 DD 後發生財報 / 重大事件）

解鎖後流程：
1. 使用者或 PM 確認要 L4 override
2. **強制先重跑 stock-analyst**（不跳過）
3. 若新 DD 方向與原 DD 一致（即使 dd_invalid）→ L4 再次被擋住
4. 若新 DD 方向與原 DD 相反 → L4 自動升級為「新 DD 下的 L1 sizing」（不再是 override）

**本質**：L4 不是被執行的 override，而是觸發重跑的信號。

---

## Reversal Condition 標準格式

| Override 類型 | Reversal Condition 寫法範例 |
|:---|:---|
| L1 sizing | 「半導體 sector 降至 < 30% 後，回到 DD 建議 20% 核心倉位」 |
| L2 horizon | 「2026-10 後若無現金流需求，回到 3-5 年持有期」 |
| L3 information | 「下次 DD 重跑後：若確認利空 → 清倉；若被推翻 → 加碼至 DD 建議」 |
| L4 | N/A（預設禁止） |

禁止模糊寫法：
- ❌「之後再說」
- ❌「看情況」
- ❌「若市場變好」（不可驗證）

必須可驗證、可落地、有日期或數字閾值。

---

## 偏誤統計（HTML §8 末尾）

每份 PM 報告自動列出：

### 本次 Override 明細
```
L1 × 2（NVDA sizing, CRDO sizing）
L2 × 0
L3 × 1（AMZN: AWS capex 上修，DD 2026-04-14 未納入）
L4 × 0
```

### 歷史累積統計（從 docs/pm/ 下所有歷史報告推算）
```
累積 L1：__ 次（平均 sizing delta __%）
累積 L2：__ 次（平均 horizon 縮短 __ 個月）
累積 L3：__ 次，確認率 __/__（若 < 50% → 警示「PM 資訊層判斷偏差」）
累積 L4：0 次（若 > 0 → 重大警示，檢討紀律）
```

### 開啟中 Override（未 reversal 的）
列出 condition 未達成、尚在作用中的 override，供下次複盤檢視。

---

## Override 拒絕條件

下列情況 PM skill **自動拒絕** override，不納入最終建議：

1. Reversal condition 未寫 / 寫模糊
2. L4 override 但 dd_invalid = false
3. L3 override 但 info_source 缺失
4. L1 sizing override 但 PM decision 與 DD direction 不同側（例：DD 迴避，PM sizing 5%）→ 這是 L4 偽裝成 L1
5. 單次 L1 sizing delta > 50%（例：DD 20%，PM 3%）→ 可能為偽裝 L4，要求改填 L2 或 L3

被拒絕的 override 列於 HTML §8 末尾「被拒絕的 override」，附拒絕理由。
