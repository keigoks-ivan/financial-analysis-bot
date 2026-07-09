# knowledge/ — 決策帳本 + 實體圖譜（Phase 0）

> 任何 agent／LLM 工具的入口協議見 repo 根目錄 `AGENTS.md`（本 README 是 knowledge/ 細節）。

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
| `settle_outcomes.py` | 機械結算：decisions × weekly_cache → forward return | ✅ commit |
| `settlement.json` | **衍生**：每筆裁決的 +30/91/182/365 天與 to-date 報酬 | 🚫 gitignore |

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
python knowledge/q.py --calibration # 機械結算記分板（依裁決/評級）+ 錯過成本警報 + 人工 outcome
python knowledge/q.py --rebuild     # 重建衍生物
```

## 機械結算（自動對答案，2026-07-04 起）

`settle_outcomes.py` 把每筆裁決用 `data/weekly_cache` 週線結算 forward return
（+30/91/182/365 天固定視窗 + to-date），寫入 `settlement.json`。**不需手動跑**：
`q.py` 發現 settlement 比 `decisions.jsonl` 或任一週線 cache 檔舊就自動重算——
weekly cache 由 GitHub Actions 每週更新、`git pull` 進來後首次查詢即重新結算，
等效於掛在 weekly workflow 上但零 CI 改動、零衍生物 commit。

`--calibration` 呈現三層：
1. **依裁決**（進場/觀望/迴避，v13+ 才有）——觀望/迴避的正報酬＝**錯過成本**，與套牢同權重。
2. **依基本面評級**（A+/A/B/C/X，涵蓋全部 388+ 筆）。
3. **⚠ 錯過成本警報**：觀望/迴避後漲逾 +30% 的名字＝觀望複審觸發清單。

讀數紀律：聚合只取結算齡 ≥ 28 天樣本；各筆視窗不等長，**方向可信、量級慎讀**；
`px_mismatch` flag＝dd-meta 價與 cache 序列落差 >25%（split/ADR 幣別），報酬仍以 cache 同序列計算、內部一致。

## 回填 outcome（人工複盤，機械結算不取代）

在 `ledger.manual.jsonl` 加一行（`decision_id` = `q.py` 顯示的 `ticker-YYYYMMDD`）：

```json
{"kind":"outcome","decision_id":"NVDA-20260623","reviewed_date":"2026-12-23","price_then":168.0,"realized_return_pct":18.1,"verdict_held":true,"lesson":"對結構性順風又給太少 credit"}
```

`--rebuild` 後 `q.py --calibration` 就會算命中率與各裁決別偏誤，餵回 stock-analyst QC 規則。

## 回填 event_outcome（T-minus 鏈事件複盤，2026-07-05 新增）

財報／催化劑事件過後的複盤記錄。錨是 pre-earnings preview 的凍結快照
（`docs/catalyst/snapshots/preview_*.json`），**不走價格結算、不進裁決校準統計**，
只在 `q.py <TICKER>` 的「事件複盤」段顯示。preview 報告尾段會預填草稿，
`actual`／`verdict` 由人在事後補（**只允許人工寫入，cron 永不碰此檔**）：

```json
{"kind":"event_outcome","id":"evt_NVDA_20260827_earnings","ticker":"NVDA","event_date":"2026-08-27","event_type":"earnings","expected":"共識 EPS 1.62／preview base 情境","actual":"EPS 1.71, DC rev +9% QoQ","verdict":"beat","snapshot":"docs/catalyst/snapshots/preview_NVDA_20260827.json","noted_at":"2026-08-29"}
```

`verdict` 建議值：`beat`／`miss`／`inline`／`mixed`。同時記得把 `docs/catalyst/archive.json`
對應事件的 `outcome` 欄回填（monitor Check 3 讀那裡）。

## 給 Claude 的約定（服務 b）

動部位（加倉/減倉/新進/退出）前，除了既有 `industry-thesis-critic` 冷讀，
**先 `python knowledge/q.py <TICKER>` 看歷次判斷與 outcome**，拿「我實際說過的話」當錨，不要重推。
（是否把這條寫進 repo 頂層 CLAUDE.md 的「Decision-time critic」段 → 待 diff 確認後再動。）

---

# 第二大腦（2026-07-07 起）— 全 repo 全文層

在決策帳本之上疊一層**全文知識層**，一條 pipeline 三形態輸出，**全部本地、不上站**：

| 檔案 | 角色 | git |
|---|---|---|
| `brain_extract.py` | 抽取層：各家族 HTML/md/JSON → 統一 note dict（h2 → section-title → 整篇 fallback 鏈） | ✅ commit |
| `brain_build.py` | orchestrator：增量抽取（mtime cache）→ vault 筆記 + entity/theme hub → FTS → wiki | ✅ commit |
| `brain_wiki.py` | vault → 本機 wiki 靜態頁（[[link]] 可點；由 brain_build 自動呼叫） | ✅ commit |
| `vault/auto/**` | **衍生**：~1,500 則 Obsidian 筆記（DD/DCA/ID/earnings/comparisons/synthesis/monitors/supply-chain/briefing/weekly/qgm/策略規則/internal notes/外部 repo） | 🚫 gitignore |
| `vault/notes/**` | **真相**：用戶手寫筆記（可 [[link]] 進 auto/） | ✅ commit |
| `brain.db` | **衍生**：FTS5 trigram 全文索引（中文可搜；<3 字走 LIKE） | 🚫 gitignore |
| `brain_cache.json` | **衍生**：per-machine mtime 增量快取（絕不 commit） | 🚫 gitignore |
| `wiki/**` | **衍生**：本機 wiki（`open knowledge/wiki/index.html`） | 🚫 gitignore |

**用法**：

```bash
python knowledge/q.py --search "先進封裝" [--type dd] [--limit 10]  # 全文搜尋（自帶 stale gate）
python knowledge/q.py --note NVDA        # 列出 entity 對應 vault 筆記路徑（含用戶手寫思考筆記）
python knowledge/q.py --inbox           # 收 ~/Downloads 訓練匯出 → vault/notes → 自動入腦
python knowledge/q.py --falsifiers      # 個人殺手假設/獵場認領帳本（>90 天未對帳標 ⚠）
python knowledge/q.py --rebrain          # 手動全鏈重建
python knowledge/brain_build.py --stats  # 各家族計數 + 解析降級統計
open knowledge/wiki/index.html           # 本機 wiki（dashboard + 互連筆記頁 + 蒙格清單/道場/訓練場）
```

**思考層閉環**：wiki 訓練頁（munger/dojo/gym）匯出 .md → `q.py --inbox` 收檔入腦 →
`brain_build` 抽「殺手假設/獵場認領」進 `falsifiers.json`（衍生）→ position-thesis-monitor
Check 8 每週機械對帳 → 觸發回 wiki 判定或回填 ledger lesson。工具本身的使用 kill condition
登記於 `rule_ledger.md`（2026-08-07 首審）。

**新內容自動入腦（三道防線）**：① `post-commit` hook（本機新報告）② `post-merge` hook
（`git pull` 拉進 cron 產物）③ `q.py --search` 前自動跑增量 build（no-op ~0.1s，
hook 沒裝或外部 repo 變動也接得住）。

**外部 repo**：`brain_extract.py` 的 `SIBLING_REPOS` registry（v7-backtest / minervini /
morning-briefing / tools / malaysia-property / dotfiles），加新 repo = 加一行 glob；
目錄不在本機（另一台 Mac）= warn 跳過，不是 error。

**Obsidian**：直接開 `knowledge/vault/` 當 vault；auto/ 會被 rebuild 覆寫，
自己的筆記寫 `vault/notes/`（committed）。
