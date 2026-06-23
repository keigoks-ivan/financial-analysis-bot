# knowledge/ — 決策帳本 + 實體圖譜（Phase 0）

把鎖在 484 份 DD / 174 份 ID HTML 裡的判斷，抽成**一條可查的決策帳本 + 一張跨域實體圖**，
讓「我」（`q.py`）和「Claude」（讀這兩個檔）共用同一份 ground truth。
目標：**a 自我導航決策 + b Claude 協助更準**（不做對外發布，故不進 `docs/`、不上站）。

## 檔案

| 檔案 | 角色 | git |
|---|---|---|
| `ledger.manual.jsonl` | **真相**：人工 outcome 回填 + 非 DD 決策 | ✅ commit |
| `build_knowledge.py` | 掃 dd-meta/id-meta → 生衍生物 | ✅ commit |
| `q.py` | 查詢 CLI | ✅ commit |
| `decisions.jsonl` | **衍生**：每份 DD = 一筆決策事件（+ 合併 manual） | 🚫 gitignore |
| `graph.json` | **衍生**：公司/產業節點 + 關係邊 | 🚫 gitignore |

## 跨機同步規則（兩台 Mac）

1. **真相才 commit，衍生物 gitignore**：`decisions.jsonl` / `graph.json` 由 dd-meta 重算，
   每台機本地 `--rebuild` 即可 → **零 git 衝突**。手寫的 `ledger.manual.jsonl` 才進 git。
2. **工作前 `git pull --rebase`**（沿用你既有習慣），再 `q.py --rebuild`。
3. `ledger.manual.jsonl` 是 append-only；萬一兩台機同時加，衝突就是「兩行都留」，極好解。
4. 對應 financial-analysis-bot CLAUDE.md「Parallel-session git hygiene」：別盲 `git add -A`。

## 用法

```bash
python knowledge/q.py NVDA          # entity 決策史 + 現裁決 + 所屬產業
python knowledge/q.py --theme CoWoS # 主題 + 成員 ticker 現裁決
python knowledge/q.py --stale       # 該重跑 DD 的公司（canonical 過期）
python knowledge/q.py --verdicts    # 全公司最新裁決分布
python knowledge/q.py --calibration # 命中率（需 outcome）/ 覆蓋報告
python knowledge/q.py --rebuild     # 重建衍生物
```

## 回填 outcome（校準閉環的關鍵）

在 `ledger.manual.jsonl` 加一行（`decision_id` = `q.py` 顯示的 `ticker-YYYYMMDD`）：

```json
{"kind":"outcome","decision_id":"NVDA-20260623","reviewed_date":"2026-12-23","price_then":168.0,"realized_return_pct":18.1,"verdict_held":true,"lesson":"對結構性順風又給太少 credit"}
```

`--rebuild` 後 `q.py --calibration` 就會算命中率與各裁決別偏誤，餵回 stock-analyst QC 規則。

## 給 Claude 的約定（服務 b）

動部位（加倉/減倉/新進/退出）前，除了既有 `industry-thesis-critic` 冷讀，
**先 `python knowledge/q.py <TICKER>` 看歷次判斷與 outcome**，拿「我實際說過的話」當錨，不要重推。
（是否把這條寫進 repo 頂層 CLAUDE.md 的「Decision-time critic」段 → 待 diff 確認後再動。）
