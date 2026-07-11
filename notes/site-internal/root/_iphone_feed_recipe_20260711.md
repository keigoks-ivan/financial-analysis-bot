# 免終端機餵養第二大腦 — iPhone 配方 + 重建手冊（2026-07-11）

主場景是 **iPhone**：不開終端機也能把想法／剪報丟進第二大腦。三個入口，背後都收斂到 `knowledge/vault/notes/inbox/` 週檔並自動入腦（增量 `brain_build --no-wiki`）。

- **wiki 餵腦框**：wiki 首頁搜尋框上方「📥 餵大腦」輸入列 → `POST http://127.0.0.1:8873/jot`（body 純文字）→ append 週檔 → 背景入腦。
- **投遞資料夾**：丟 `*.md`／`*.txt` 進 `~/BrainInbox` 或 iCloud `~/Library/Mobile Documents/com~apple~CloudDocs/BrainInbox` → WatchPaths 觸發 `q.py --inbox --quiet`（`.txt` 自動補 frontmatter，收進 `vault/notes/inbox/`，原檔刪除）。
- **`bj`／`bi`**：終端機一秒捕捉（既有 zsh 指令）。

server（`knowledge/brain_server.py`）只綁 127.0.0.1，寫入面僅 append 純文字到固定 inbox 資料夾——無路徑參數、無刪改能力；CORS 全開讓 `file://` 開的 wiki 也打得進來。

---

## 三條路（按「立即可用」排序）

### 1. 現在就能用（零設定）— Files app／分享表單 → iCloud Drive BrainInbox

任何 app 的分享表單 → 「儲存到檔案」→ iCloud Drive → `BrainInbox` 資料夾。回 Mac，iCloud 本機鏡像一落地，`com.ivanchang.brain-inbox` 的 WatchPaths 觸發收檔入腦。純文字 `.txt`／`.md` 皆可（`.txt` 自動補 frontmatter）。Safari 好文章 → 分享 → 儲存到檔案 → BrainInbox 即可。

> WatchPaths 監看的是 Mac 上的 iCloud **本機鏡像**路徑；手機端存檔後需 iCloud 同步落地到 Mac 才觸發（數秒到數十秒；Mac 要連網、該資料夾未被「最佳化儲存」移出本機）。

### 2. iOS 捷徑配方（自己在「捷徑」app 建）

**捷徑 A「丟進大腦（分享表單）」**
1. 捷徑 app → 右上「+」→「i」資訊 → 開「在分享表單中顯示」，接受類型勾「文字」「URL」「Safari 網頁」。
2. 動作「文字」→ 內容填變數：`捷徑輸入`。
3. 動作「儲存檔案」（Save File）→ 服務 iCloud Drive → 路徑 `BrainInbox/` → 關「詢問儲存位置」→ 檔名自訂：`剪報-〔目前日期〕.txt`（「目前日期」變數格式設 `yyyy-MM-dd-HHmmss` 避免同名覆蓋）。
4. 命名「丟進大腦」。用法：任何 app 分享 → 捲到捷徑 → 「丟進大腦」。

**捷徑 B「快速筆記（手動輸入）」**
1. 新增捷徑，**不**開分享表單。
2. 動作「要求輸入」（Ask for Input）→ 類型「文字」→ 提示「丟什麼進大腦？」。
3. 動作「儲存檔案」→ iCloud Drive `BrainInbox/`，檔名 `筆記-〔目前日期〕.txt`，內容用「提供的輸入」變數。
4. 命名「快速筆記」，加到主畫面／鎖定畫面小工具，一點跳輸入框。

兩者都靠路徑 1 的 iCloud→WatchPaths 自動入腦；Mac 要開機連網才會收。

### 3. Tailscale 通了之後 — Safari 直接用餵腦框（即時，最順）

Mac 與 iPhone 上同一 tailnet 後，server 只綁 127.0.0.1，要讓手機打到需在 Mac 跑一次：

```bash
tailscale serve --bg 8873          # 把本機 8873 經 tailnet 對外（HTTPS，僅你的 tailnet 可見）
tailscale serve status             # 看對外 URL（形如 https://<mac-name>.<tailnet>.ts.net/）
```

iPhone Safari 開 `https://<mac-name>.<tailnet>.ts.net/knowledge/wiki/` → 直接用「📥 餵大腦」輸入列，即時入腦、免等 iCloud 同步。收工：`tailscale serve --bg 8873 off`。

（餵腦框的 fetch 目標**依開啟方式自動切換**：`file://` 開的頁 origin=null，打絕對本機位址 `http://127.0.0.1:8873/jot`；經 server 開的頁（`bw` 的 http 同源／Tailscale 的 https 同源）則打相對路徑 `/jot`——所以 Tailscale 情境框可直接用，不會踩 mixed-content。邏輯在 `brain_wiki.py` INDEX 模板 `API=(location.protocol==='file:')?…:'/jot'`。）

---

## macOS 捷徑版（全域快捷鍵跳輸入框）

1. 捷徑 app（Mac）→ 新增捷徑。
2. 「要求輸入」→ 文字 → 提示「丟什麼進大腦？」。
3. 「執行 Shell 指令」→ Shell `zsh` → 勾「輸入以 stdin 傳入」，指令：
   ```
   source ~/dotfiles/scripts/brain.sh && bj "$(cat)"
   ```
4. 捷徑「i」→「加入為快速動作」+ 指定鍵盤快捷鍵（如 ⌃⌥Space）。按一下跳框 → Enter 入腦。

---

## 📔 Apple 日誌 app（Journal）調查 — 誠實優先

**結論：不建議接。Journal 沒有可靠的程式化讀取路徑；最佳替代是好內容改走 BrainInbox／分享捷徑，Journal 留給私人日記。**

2026 現況（WebSearch 查證）：

- **程式化讀取**：無公開 API、無文件化的機器可讀檔案格式。資料存在 app 私有容器內、on-device 處理；當 iPhone 以密碼鎖定時 entries 加密，開啟預設雙因素＋密碼時 Journaling Suggestions 為**端對端加密**（Apple 自己也讀不到）。Journal entries **不含在 iCloud 備份**內（另走 iCloud 同步）。實務上受系統保護、非第三方程式可直讀。無文件記載的 `~/Library` 明碼 SQLite 可直接解析。
- **官方匯出**：macOS Journal（macOS 15 起有桌面版）`File > Export` 產出的是一個**迷你網站（HTML）**，定位是備份／人眼瀏覽，不是乾淨的結構化資料（非 JSON／非逐筆 md）。iOS 端匯出類似。
- **Shortcuts 動作**：iOS 18.1 起有 `Create Entry`、`Create Audio Entry`、`Search Entries`——全是**寫入向或搜尋向**；**沒有**「取出全部 entry 內文」回傳給後續動作的 read/get 動作。`Search Entries` 是給 app 內導航用，不是批次匯出內文的管道。

**為什麼不硬接**：即便走 `File > Export`，產物是 HTML 迷你站，而我們的投遞資料夾目前只收 `*.md`／`*.txt`（`DROP_DIRS` glob）；要接得先把 HTML 逐篇轉純文字再落 BrainInbox，是脆弱的半手動流程，且每次都要手動重匯出——不值得，也違反「不為交差硬掰脆弱 hack」。

**建議的分工**：
- 想留進大腦的好文章／想法 → 用上面路徑 1／2／3（BrainInbox 或分享捷徑），一步到位可搜尋、掛 entity hub。
- Journal → 純私人日記，保留其端對端加密與隱私，不進第二大腦。
- 若哪天真的想把某幾則 Journal entry 進腦：在 Journal 內複製該則文字 → iOS 捷徑 B「快速筆記」貼上存檔，即走正規入腦管道（人工、按需，不做自動同步）。

來源：Apple Support（Journal 隱私與保護、Shortcuts iOS 18 新動作）、Apple Legal（Journaling Suggestions & Privacy 端對端加密）、Matthew Cassinelli（iOS 18.1 Journal shortcuts：Create/Create Audio/Search Entries）、MacMost（macOS Journal `File > Export` 產迷你網站）。

---

## launchd plist 完整內容（`~/Library`，不進 git；另一台 Mac 重建用）

放 `~/Library/LaunchAgents/`，`launchctl load` 之。

### `com.ivanchang.brain-wiki.plist`（server 常駐）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.ivanchang.brain-wiki</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/python3</string>
    <string>/Users/ivanchang/financial-analysis-bot/knowledge/brain_server.py</string>
    <string>8873</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardErrorPath</key><string>/tmp/brain-wiki.err</string>
</dict></plist>
```

### `com.ivanchang.brain-inbox.plist`（投遞資料夾 WatchPaths 觸發）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.ivanchang.brain-inbox</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/python3</string>
    <string>/Users/ivanchang/financial-analysis-bot/knowledge/q.py</string>
    <string>--inbox</string>
    <string>--quiet</string>
  </array>
  <key>WatchPaths</key><array>
    <string>/Users/ivanchang/BrainInbox</string>
    <string>/Users/ivanchang/Library/Mobile Documents/com~apple~CloudDocs/BrainInbox</string>
  </array>
  <key>ThrottleInterval</key><integer>60</integer>
  <key>RunAtLoad</key><false/>
  <key>StandardErrorPath</key><string>/tmp/brain-inbox.err</string>
  <key>StandardOutPath</key><string>/tmp/brain-inbox.out</string>
</dict></plist>
```

### 另一台 Mac 重建步驟

```bash
mkdir -p ~/BrainInbox "$HOME/Library/Mobile Documents/com~apple~CloudDocs/BrainInbox"
# 貼上兩個 plist 到 ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.ivanchang.brain-wiki.plist
launchctl load ~/Library/LaunchAgents/com.ivanchang.brain-inbox.plist
# 驗證：
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8873/knowledge/wiki/index.html   # 期望 200
curl -s -X POST http://127.0.0.1:8873/jot --data-binary '測試'                              # 期望 {"ok": true, ...}
```
