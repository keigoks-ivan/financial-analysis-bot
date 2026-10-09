# Koyfin 台股 watchlist 建置紀錄（2026-10-09，已建）

給 `refresh-eps-screener-web` skill 與 `koyfin_refresh_all.py` 未來維護用的操作紀錄。
這是第四個 Koyfin 母體，跟 `dd_smallcap` 一樣是獨立的 `UNIVERSE_MODE`（`tw`），
輸出 `docs/dd-screener/tw/latest.json`，不進主檔、tenbagger、arena 或美股 cockpit。

持有人 2026-10-09 的決定：台股 DD Screener 要用 Koyfin，因為 yfinance 沒有 FY3 預估；
台股範圍不必像美股那麼大。

## 篩選器 `dd_tw_v1`

- 網址：https://app.koyfin.com/mys/01M4G7CV48TS27YV3408JZPGYK
- Universe：Trading Country = Taiwan。
- 條件：市值（USD）≥ 1,000M、ROIC (LTM) ≥ 15、FCF Margin % (LTM) > 0。
  FCF 用 > 0 而非 ≥ 10，理由同大市值池（見 `_koyfin_largecap_watchlist_20260918.md`）：
  重投資期、現金流薄但不為負的高 ROIC 名字要先進得了清單。
- 2026-10-09 結果 69 檔，其中上櫃 14 檔。

## Watchlist `dd_tw_80col`

- 網址：https://app.koyfin.com/myw/b56fc646-d1b8-41f7-b4d1-438744598421
- 為什麼叫 80col：第一份 `dd_tw` 用 Koyfin 預設的 8 欄版面建立，既有 watchlist
  套不上 dd_screener 的 80 欄版面，只好另存一份完整版面。抓取的是 `dd_tw_80col`。
- **殘留草稿**：第一份 8 欄的 `dd_tw`（https://app.koyfin.com/myw/7766e3a2-8bcf-4508-825c-e9fb39aadfaa）
  沒有用途，持有人可自行刪除。程式不讀它。

## 抓取與指紋

- 2026-10-09 原始檔 `data/eps-estimates/raw/koyfin_tw_raw_20261009.txt`：69 列、80 欄、
  27,399 bytes、djb2 1944496195。瀏覽器端與 Python 端指紋一致。
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
4. **15 檔沒有分析師預估**：Koyfin 的 FY1～FY3 全空（例如創見、光聖）。它們仍會排名，
   只是名次只看品質和股價。
5. **7856 漢測 EPS 跳升**：FY1 0.91 → FY3 8.97 美元，三年年化 214%。四條件只過兩條，
   但 FunnelRank v2 排第 1。這是 Koyfin 預估本身，build 沒有改它。

## DD 疊加

主 latest.json 的台股 DD 名字一律是 `.TW`（5274、8299 由 `TICKER_YF_OVERRIDE` 對應），
台股池用代號比對。2026-10-09 池內 9 檔有 DD（2330、3017、2454、5274、3653、2345、2368、
3443、2308），DD 欄位從主檔複製過來，`dd_overlay_from` 記來源列。另有 7 檔台股 DD
不符合本池篩選（2327、2383、3661、3037、3231、2317、8299），只列在美股主頁。

## 下游

- 每日：`daily-taipei-morning.yml` Step 2a-tw（build）→ Step 2a-tw-page（`build_dd_screener_tw_page.py`
  從主頁衍生 `docs/dd-screener/tw/index.html`）。
- 每月：`monthly-eps-snapshot.yml` 存 `docs/dd-screener/tw/eps-estimates-snapshots/`。第一份是 2026-10，
  上修欄要到 2026-11 快照之後才有數字。
- Koyfin 重抓：`koyfin_refresh_all.py` 的下游鏈最後兩步是台股 build 與台股頁，排在 tenbagger／arena
  之後，台股出錯不會擋到美股。
- 台股選股主控台 `/cockpit-tw/` 讀 `tw/latest.json`，與美股 `/cockpit/` 互相有切換連結。
