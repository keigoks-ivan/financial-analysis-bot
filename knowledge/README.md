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

# 免終端機餵腦（2026-07-11 起）— server + 投遞資料夾 + 手機

不開終端機也能把想法丟進第二大腦。三個入口，背後都收斂到 `vault/notes/inbox/` 週檔並自動入腦：

| 入口 | 機制 | launchd |
|---|---|---|
| **wiki 餵腦框** | wiki 首頁搜尋框上方「📥 餵大腦」輸入列 → `POST /jot` → append 週檔 → 背景 `brain_build --no-wiki` | `com.ivanchang.brain-wiki`（跑 `brain_server.py 8873`，只綁 127.0.0.1） |
| **投遞資料夾** | 丟 `*.md`／`*.txt` 進 `~/BrainInbox` 或 iCloud 的 `~/Library/Mobile Documents/com~apple~CloudDocs/BrainInbox` → WatchPaths 觸發 `q.py --inbox --quiet`（`.txt` 自動補 frontmatter） | `com.ivanchang.brain-inbox`（WatchPaths 監看兩資料夾，ThrottleInterval 60） |
| **`bj` / `bi`** | 終端機一秒捕捉（既有） | — |

`brain_server.py` 寫入面只有 append 純文字到固定 inbox 資料夾——無路徑參數、無刪改能力；CORS 全開讓 `file://` 開的 wiki 也打得進來。`bw` 指令會先偵測 server 活著就開 `http://127.0.0.1:8873/knowledge/wiki/`（同源，餵腦框可用），否則 fallback `file://`。

## 📱 iPhone 餵腦

主場景是 iPhone。三條路，按「立即可用」排序：

**1. 現在就能用（零設定）— Files app／分享表單存進 iCloud Drive**

任何 app 的分享表單 → 「儲存到檔案」→ iCloud Drive → `BrainInbox` 資料夾。回到 Mac，iCloud 本機鏡像一落地，`com.ivanchang.brain-inbox` 的 WatchPaths 就觸發收檔入腦。純文字選 `.txt`／`.md` 皆可（`.txt` 自動補 frontmatter）。Safari 讀到好文章 → 分享 → 儲存到檔案 → BrainInbox，即可。

> 注意：WatchPaths 監看的是 Mac 上的 iCloud **本機鏡像**路徑；手機端存檔後需 iCloud 同步落地到 Mac 才觸發（通常數秒到數十秒；Mac 需連網且該資料夾未被「最佳化儲存」移出本機）。

**2. iOS 捷徑配方（自己在「捷徑」app 建，截圖級步驟）**

捷徑 A「丟進大腦（分享表單）」：
1. 捷徑 app → 右上「+」新增捷徑 → 「i」資訊 → 開「在分享表單中顯示」，接受類型勾「文字」「URL」「Safari 網頁」。
2. 加動作「文字」→ 內容填變數：`捷徑輸入`（把分享進來的東西當文字）。
3. 加動作「儲存檔案」（Save File）→ 服務選 iCloud Drive → 目的地路徑 `BrainInbox/` → 關閉「詢問儲存位置」→ 檔名開「自訂」填：`剪報-〔目前日期〕.txt`（用「目前日期」變數，格式設 `yyyy-MM-dd-HHmmss` 避免同名覆蓋）。
4. 命名捷徑「丟進大腦」。用法：任何 app 分享 → 捲到捷徑 → 「丟進大腦」。

捷徑 B「快速筆記（手動輸入）」：
1. 新增捷徑，**不**開分享表單。
2. 加動作「要求輸入」（Ask for Input）→ 類型「文字」→ 提示「丟什麼進大腦？」。
3. 加動作「儲存檔案」→ 同上，iCloud Drive `BrainInbox/`，檔名 `筆記-〔目前日期〕.txt`，內容用「提供的輸入」變數。
4. 命名「快速筆記」，可加到主畫面／鎖定畫面小工具，一點就跳輸入框。

兩者都靠路徑 1 的 iCloud→WatchPaths 自動入腦，不需 Mac 開著終端機（但 Mac 要開機連網才會收）。

**3. Tailscale 通了之後 — Safari 直接用餵腦框（即時，最順）**

Mac 與 iPhone 都裝 Tailscale 上同一 tailnet 後，server 只綁 127.0.0.1，要讓手機打得到需在 Mac 跑一次：

```bash
tailscale serve --bg 8873          # 把本機 8873 經 tailnet 對外（HTTPS，僅你的 tailnet 可見）
tailscale serve status             # 看對外 URL（形如 https://<mac-name>.<tailnet>.ts.net/）
```

之後 iPhone Safari 開 `https://<mac-name>.<tailnet>.ts.net/knowledge/wiki/` → 直接用「📥 餵大腦」輸入列，即時入腦、免 iCloud 等同步。收工關閉：`tailscale serve --bg 8873 off`。

## 🖥 macOS 捷徑版（全域快捷鍵跳輸入框）

Mac 上想一個快捷鍵就跳出輸入框餵腦：
1. 捷徑 app（Mac）→ 新增捷徑。
2. 加「要求輸入」→ 文字 → 提示「丟什麼進大腦？」。
3. 加「執行 Shell 指令」（Run Shell Script）→ Shell 選 `zsh` → 勾「輸入以 stdin 傳入」，指令：
   ```
   source ~/dotfiles/scripts/brain.sh && bj "$(cat)"
   ```
   （或不透過 stdin，直接把「提供的輸入」變數插進 `bj "…"`。）
4. 捷徑「i」資訊 → 設「加入為快速動作」+ 指定鍵盤快捷鍵（如 ⌃⌥Space）。按一下跳輸入框 → Enter 直接入腦。

## 📔 Apple 日誌 app（Journal）能不能接？— 結論：不建議接（見下）

完整調查與判斷見 `notes/site-internal/root/_iphone_feed_recipe_20260711.md`。一句話：Journal 的資料**沒有可靠的程式化讀取路徑**（無公開 API、無結構化匯出格式、鎖屏後端對端加密、entries 不進 iCloud 備份），Shortcuts 只有寫入向（Create Entry / Search Entries，無「取出全部 entry 內文」動作）。最佳做法＝**好文章／想留的內容改走 BrainInbox 或分享捷徑**，Journal 留給私人日記。
