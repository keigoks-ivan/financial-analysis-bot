# Koyfin 台股 watchlist 建置紀錄（2026-10-09，已建）

給 `refresh-eps-screener-web` skill 與 `koyfin_refresh_all.py` 未來維護用的操作紀錄。
這是第四個 Koyfin 母體，跟 `dd_smallcap` 一樣是獨立的 `UNIVERSE_MODE`（`tw`），
輸出 `docs/dd-screener/tw/latest.json`，不進主檔、tenbagger、arena 或美股 cockpit。

持有人 2026-10-09 的決定：台股 DD Screener 要用 Koyfin，因為 yfinance 沒有 FY3 預估；
台股範圍不必像美股那麼大。

## 篩選器 `dd_tw_v1`

- 網址：https://app.koyfin.com/mys/01M4G7CV48TS27YV3408JZPGYK
- Universe：Trading Country = Taiwan。
- 條件：市值（USD）≥ 1,000M、ROIC (LTM) ≥ 15。
- 原本還有 FCF Margin % (LTM) > 0，2026-10-09 晚間依持有人決定拿掉（見下方「現金流」一節）。
  拿掉前 69 檔（上櫃 14 檔），拿掉後 86 檔（上櫃 21 檔），原 69 檔全部留著，多出 17 檔。

## Watchlist `dd_tw_80col`

- 網址：https://app.koyfin.com/myw/b56fc646-d1b8-41f7-b4d1-438744598421
- 為什麼叫 80col：第一份 `dd_tw` 用 Koyfin 預設的 8 欄版面建立，既有 watchlist
  套不上 dd_screener 的 80 欄版面，只好另存一份完整版面。抓取的是 `dd_tw_80col`。
- **殘留草稿**：第一份 8 欄的 `dd_tw`（https://app.koyfin.com/myw/7766e3a2-8bcf-4508-825c-e9fb39aadfaa）
  沒有用途，持有人可自行刪除。程式不讀它。

## 抓取與指紋

- 2026-10-09 原始檔 `data/eps-estimates/raw/koyfin_tw_raw_20261009.txt`：86 列、80 欄、
  33,983 bytes、djb2 1350491970。瀏覽器端與 Python 端指紋一致。
- 同日稍早的 69 列版本改名為 `koyfin_tw_raw_20261009_69rows.txt`（27,399 bytes、djb2 1944496195）。
  兩次抓取共同的 69 檔裡有 6 檔數字不同，全是 0.01 美元等級的 EPS 或本益比 0.1 倍的小幅變動。
- 原始 txt 與 sidecar 照慣例不進 git，xlsx 進 git。

## 地雷

1. **子選單跑出畫面外**：在篩選器加條件時，ROIC／FCF 的 LTM 子選單會開在視窗外，
   點不到。解法是用 PointerEvent 直接派送點擊，或把頁面 CSS zoom 縮小再點。
2. **幣別混用**：台股 xlsx 的 EPS 與金額欄是美元，股價與目標價是新台幣。
   - 上修計算一律用美元對美元（快照存的是 Excel 原始美元值）。
   - 上修算完後，非 DD 列按 xlsx 日期的即期匯率換成新台幣，原值留在 `*_usd_orig`。
   - DD 列走主 build 既有的逐檔換算（用 yfinance 新台幣預估反推匯率），數字跟美股主頁一致。
3. **上市／上櫃後綴**：Koyfin 只給代號（"2330"、"5274"），yfinance 需要正確後綴，
   "5274.TW" 抓不到，"5274.TWO" 才行。`scripts/tw_listing_suffix.py` 依序查證交所名冊、
   櫃買中心名冊，最後用 yfinance 試抓。2026-10-09 有三檔（3595、6826、7861）剛從興櫃轉上櫃、
   還不在櫃買名冊上，靠試抓解出 `.TWO`；它們沒有中文名，頁面顯示代號。
4. **沒有分析師預估**（69 檔時 15 檔，86 檔時 19 檔）：Koyfin 的 FY1～FY3 全空（例如創見、光聖）。它們仍會排名，
   只是名次只看品質和股價。
5. **7856 漢測 EPS 跳升**：FY1 0.91 → FY3 8.97 美元，三年年化 214%。四條件只過兩條，
   但 FunnelRank v2 排第 1。這是 Koyfin 預估本身，build 沒有改它。

## 現金流條件改看營業現金流（2026-10-09 起）

持有人當天回饋：台股不少公司資本支出重，FCF 利潤率會誤殺。台股池四條件的
「FCF≥10%」因此換成「OCF≥10%」：營業現金流利潤率＝FCF 利潤率＋資本支出占營收
（xlsx 的 Capex LTM ÷ Sales LTM）。FunnelRank v2 品質層同步換。門檻數字不變，
美股各池不動。登記在 `knowledge/rule_ledger.md`，含 kill condition。

- 當日 21 檔 FCF 利潤率 <10%，其中 17 檔營業現金流 ≥10%。
- 沒被救到的 4 檔不是資本支出問題。智邦的營業現金流只有淨利的 37%，是營運資金吃掉現金。
  創意（9.3%）、旭隼（9.9%）差一點到 10%。富邦媒淨利率 2.5%，利潤率本來就薄。
- 持有人同日第二次決定：
  - 母體篩選的「FCF >0」拿掉。台光電（FCF −1.1%、資本支出占營收 11.6%、ROIC 28.8%）因此進池。
  - 體質 veto 裡跟淨利比的那一項（標籤「OCF/淨利」，門檻 0.7）和衰退訊號「營業現金流遜於淨利」
    （0.75）也改看營業現金流。「資本支出侵蝕 FCF」照舊，它描述的就是資本支出本身。
- 拿掉 FCF >0 後多出 17 檔：台光電、潤弘、新產、中信金、健鼎、威剛、雙鴻、宜鼎、旺矽、
  台燿、緯穎、聯友金屬、永擎、7892、7924、群聯、金居。2026-10 快照已用 86 檔重存。
  - 四條件全過的只有台光電、健鼎、旺矽 3 檔，台股池全過 41 → 44。其餘 14 檔營業現金流利潤率也不到 10%，
    負的 FCF 不全是資本支出造成的。
  - 體質 veto 的現金對淨利一項，原 69 檔亮燈從 31 檔降到 11 檔。仍亮的智邦、致茂、金像電等，
    是營運資金吃掉現金。
- 新進名字的資料問題：
  - 中信金、新產是金融股（池內原本就有中再保）。銀行與保險的營業現金流、ROIC 跟一般公司算法不同，
    四條件與 veto 對它們沒有意義，目前沒有排除。
  - 7924 在 Koyfin 幾乎沒有資料：FY1～FY3 全空，FCF 利潤率 −1,227%。四條件 0 條過。
  - 7892、7924 還不在櫃買中文名冊上，頁面顯示代號。

## 成長條件改看今年到明年（2026-10-09 起）

- **地雷**：Koyfin 從 2026-06-23 的匯出起，三個預先算好的成長欄（FY1→FY2、
  FY2→FY3、FY1→FY3 CAGR）整欄空白，台股 xlsx 也一樣。`build_dd_screener.py` 現在用
  FY1／FY2／FY3 自己算（`_koyfin_eps_growth()`），不靠這三欄。
- 持有人決定：台股池的成長條件看 Koyfin 的 FY+1→FY+2（今年到明年）單年成長 ≥15%，
  只用 Koyfin，缺值算不過。理由：69 檔有明年預估的 53 檔，有後年預估的只有 45 檔。
- 台股頁的成長欄改顯示這個數字，月修正 chip 拿掉，因為月快照比的是 FY+1→FY+3 年化。
- FunnelRank v2 的成長面向（engine 層）仍用 FY+1→FY+3 年化，沒有改。

## DD 疊加

主 latest.json 的台股 DD 名字一律是 `.TW`（5274、8299 由 `TICKER_YF_OVERRIDE` 對應），
台股池用代號比對。2026-10-09 池內 9 檔有 DD（2330、3017、2454、5274、3653、2345、2368、
3443、2308），DD 欄位從主檔複製過來，`dd_overlay_from` 記來源列。另有 7 檔台股 DD
不符合本池篩選（2327、2383、3661、3037、3231、2317、8299），只列在美股主頁。
拿掉 FCF >0 後，台光電（2383）與群聯（8299）進池，池內有 DD 的變 11 檔，池外剩 5 檔
（2327、3661、3037、3231、2317）。

## 下游

- 每日：`daily-taipei-morning.yml` Step 2a-tw（build）→ Step 2a-tw-page（`build_dd_screener_tw_page.py`
  從主頁衍生 `docs/dd-screener/tw/index.html`）。
- 每月：`monthly-eps-snapshot.yml` 存 `docs/dd-screener/tw/eps-estimates-snapshots/`。第一份是 2026-10，
  上修欄要到 2026-11 快照之後才有數字。
- Koyfin 重抓：`koyfin_refresh_all.py` 的下游鏈最後兩步是台股 build 與台股頁，排在 tenbagger／arena
  之後，台股出錯不會擋到美股。
- 台股選股主控台 `/cockpit-tw/` 讀 `tw/latest.json`，與美股 `/cockpit/` 互相有切換連結。
