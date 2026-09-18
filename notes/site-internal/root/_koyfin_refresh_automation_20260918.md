# Koyfin 三份清單月度重抓自動化（2026-09-18）

這份筆記給 `refresh-eps-screener-web` skill 未來收編用。原本三份 Koyfin watchlist（`dd_screener`、`dd_smallcap`、`dd_largecap`）每個月都要手動開 Chrome、逐步照 skill 的 8 個步驟操作，一次抓完要 15 分鐘到半小時。現在改成三支程式接力：`koyfin_scraper.js`（瀏覽器裡跑的抓取器）、`koyfin_scrape.py`（Playwright 開瀏覽器、跑抓取器、驗指紋、落檔）、`koyfin_refresh_all.py`（串起抓取、建 xlsx、跑下游 build、選擇性 commit）。owner 只需要跑一個指令。

## owner 要做的事

**第一次、只做一次**：

```bash
python3 scripts/koyfin_scrape.py --login
```

這會開一個看得到畫面的瀏覽器視窗，停在 Koyfin 首頁。手動登入 Koyfin（帳密由 owner 自己輸入，程式不會也不能代打密碼）。登入完成程式會自動偵測到並關閉瀏覽器。登入狀態存在 `~/.koyfin-playwright` 這個資料夾，之後每個月都沿用同一份，不用重登入，除非它過期或被登出。

**之後每個月，一個指令**：

```bash
python3.12 scripts/koyfin_refresh_all.py --scrape --commit
```

這行會照順序做完：三份 watchlist 依序抓值 → 驗指紋 → 跑分割／異常檢查（下面「會卡住流程的三種情況」有解釋）→ 建三份 xlsx → 跑四個下游 build 指令 → 印出總結（三個母體各自的檔數、dd-screener 母體大小、席位擂台核心╱等待池/可買名單那一行）→ 把 xlsx 跟 build 出來的 docs 檔案加進 git、commit（不 push）。加 `--push` 才會真的推上 main。不加 `--commit` 就是預設值：跑完停在那裡等複審，不動 git。

**改用 launchd 排程**（選配，不裝也可以繼續手動跑）：

```bash
cp launchd/com.investmquest.koyfin-refresh.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.investmquest.koyfin-refresh.plist
```

解除排程：

```bash
launchctl unload ~/Library/LaunchAgents/com.investmquest.koyfin-refresh.plist
rm ~/Library/LaunchAgents/com.investmquest.koyfin-refresh.plist
```

排程訂在每月第一個週六早上 9:30。launchd 沒有「每月第 N 個週幾」這個原生功能，plist 裡用「週六 且 日期是 1 號到 7 號」七個條件疊起來湊出「第一個週六」，檔頭註解有寫這個湊法。另外 launchd 只認電腦本身設定的時區，不是設定檔裡能指定「台北時間」——這台 Mac 系統時區若不是台北，9:30 就不是台北時間 9:30，要自己核對系統時區或改 Hour 欄位。排程執行的是 `--scrape`（不帶 `--commit`），跑完停下等人看，不會自動推上 main。log 在 `~/Library/Logs/koyfin-refresh.log`。

## 三份 watchlist

| 名稱 | Koyfin 網址 | xlsx 檔名開頭 |
|---|---|---|
| dd_screener | `https://app.koyfin.com/myw/3f1528f1-c3fb-452d-975a-57dbc269e716` | `DD_universe_EPS_estimates_` |
| dd_smallcap | `https://app.koyfin.com/myw/4b480dbd-996d-4c8e-b47f-2d3ebf1b6ae9` | `DD_smallcap_EPS_estimates_` |
| dd_largecap | `https://app.koyfin.com/myw/0270b5a3-a66d-4e38-9b33-78916ca2bc53` | `DD_largecap_EPS_estimates_` |

程式內部用短名字 `screener`／`smallcap`／`largecap` 代表這三份（對應 `scripts/koyfin_families.py`），跟 raw txt 檔名（例如 `koyfin_largecap_raw_20260918.txt`）延續手動時代已經在用的命名，不是 Koyfin 網頁上分頁顯示的 `dd_largecap` 那個全名。

## 會卡住流程的三種情況，以及為什麼要卡

**沒登入（exit 3）**：程式偵測到頁面上有密碼輸入框，代表沒登入或登入過期。訊息會印「請先跑 --login」，直接停，不會用假資料硬跑下去。

**分頁或幣別不對（exit 4）**：Koyfin 的作用分頁名稱不是預期的那份 watchlist，或右上角幣別不是 USD，就停。這條 pipeline 全程假設抓到的是 USD 報價，非美股的匯率換算交給下游 build 處理，抓錯幣別會讓換算整個錯掉，所以在抓取這一關就要擋。

**指紋兜不起來（exit 5）**：瀏覽器裡算一次 djb2 雜湊、Python 收到資料後獨立重算一次，兩個數字要完全一樣才准落檔。這是防止「抓到一半漏行、資料在傳輸中被截斷」的唯一保險——兩邊都是機械計算，沒有轉抄，理論上不該不一樣，一旦不一樣就代表哪個環節出錯，寧可不寫檔也不要寫一份不知道對不對的資料。

**FY1 盈餘估值跳動異常（exit 6）**：這是原本 skill 裡唯一需要人判斷的步驟，這次只自動化了「抓出可疑名單」，沒有自動化「判斷」。任何一檔股票這次抓到的 FY1 每股盈餘估值，跟上一份同系列 xlsx 比，變動 ≥35% 或由正轉負／由負轉正，就會被列進名單，整條 pipeline 在這裡停下、不建 xlsx、不跑任何下游指令。原本 skill 的教訓是 2026-07-16 KLAC／CRWD 那次，數字差了 10 倍與 4 倍，一開始以為是資料壞掉，查了才知道是股票分割——分割要保留新數字、把舊的基準檔案除以分割比例；資料真的壞掉要整檔剔除；真實的分析師大幅調整估值要保留。這三種情況長得很像，但處理方式完全不同，程式沒辦法自動分辨，所以維持人工判斷，程式只負責找出「哪些名字需要人看」。

## 卡住之後怎麼恢復

- **exit 3**：跑 `python3 scripts/koyfin_scrape.py --login`，重新登入一次。
- **exit 4**：打開瀏覽器看一下卡在哪個畫面，通常是 Koyfin 把預設分頁換掉了，或者幣別 toggle 被手動切過；手動切回去再重跑就好，不用改程式。
- **exit 5**：重跑一次 `--scrape`；如果連續好幾次都兜不起來，代表 Koyfin 那次抓取本身有問題（例如網路中斷造成資料截斷），不是程式的邏輯錯，先確認網路穩定再重試。
- **exit 6**：照 `.claude/skills/refresh-eps-screener-web/SKILL.md` 的 Step 5 決策樹逐檔查：三個 FY 一起乾淨縮放（例如都除以 10）→ 大概率是分割，上網查證後保留新數字、把舊 baseline 除以分割比；數字塌到接近零或轉負但公司明明在賺錢→ Koyfin 資料壞了，那一檔從這次的 xlsx 剔除；查不出原因就先停下回報，不要自己猜。確認完，如果有調整 baseline，改完再重跑 `koyfin_refresh_all.py`。

## 還是需要人的地方

**登入會過期**。多久過期不知道，第一次遇到就會撞見 exit 3，重新 `--login` 就好，這不是程式的問題，是 Koyfin 登入態本身的限制。

**Koyfin 改版**。表格的 CSS class 名稱後綴本來就會變（skill 裡記過三次），`koyfin_scraper.js` 已經用前綴比對來擋掉這種變動。但如果 Koyfin 哪天把表格結構整個換掉（不是只換 class 後綴），會出現兩種訊號：抓到的 `headerCount` 大幅偏離 80，或抓到的欄位對不上 `koyfin_scraper.js` 裡寫死的表頭文字（`F` 這個陣列），值全部變空白。這兩種都要有人回去用瀏覽器手動核對新的表頭文字，改 `koyfin_scraper.js` 的 `F` 陣列，這步沒辦法自動化。

**分頁判斷跟幣別 toggle 的抓取邏輯，這次沒有真的在 Koyfin 頁面上驗證過**。因為到目前為止還沒有已登入的 Koyfin session 可以測試，`koyfin_scrape.py` 裡判斷「作用分頁是不是這一份 watchlist」的邏輯用了幾種常見的 DOM 寫法去猜，猜不到就退而求其次，只確認畫面上有出現這個分頁名字（比較弱的驗證）。第一次真的拿去跑，如果卡在 exit 4 但畫面看起來明明是對的，很可能是這段猜測不準，要打開瀏覽器開發者工具核對實際的 DOM 結構，回來改 `scripts/koyfin_scrape.py` 的 `_find_active_tab_label()`。

## 沒有被自動化的部分

Step 0.5（用 Columns 對話框新增新欄位）沒有自動化。這步只在「這次要幫 watchlist 加新欄位」才需要，出現頻率低（2026-09-17 才加過一次），而且牽涉到點擊 Koyfin 彈出層裡巢狀 DOM 的內層節點，skill 裡有記錄踩過的坑（外層 div 的點擊只是預覽高亮、不會真的加入欄位）。這步維持手動，加完欄位、確認 `headerCount` 變化之後，再跑自動化的抓取流程。

## 2026-09-18 補記：選擇器已對照真實頁面

用登入中的 Chrome 看過 /myw 頁：作用中分頁是 `div.kui-tabs-header-item--active`（`aria-selected="true"`），名稱在 `span.kui-tabs-header-item__label-text`；表格容器 class 含 `table__scrollContainer___`；幣別是右上角 `button.kui-button` 裡的 `span.kui-button__text`，文字 USD。腳本的三個檢查都對得上。還沒跑過的只有 Playwright 持久 profile 的完整抓取，第一次 `--login` 之後跑一次就知道。
