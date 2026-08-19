# scripts/intel/ — 情報監視器 Phase 1（市場層）

對應設計文件：`notes/site-internal/intel/DESIGN.md`。本目錄目前只做 **06:00
抓取 job**（§10），不含 haiku／sonnet 分類摘要與 render（那兩步在同一條 GHA
workflow 的後續 job，Phase 1 尚未實作）。

## 這裡跑什麼

`fetch.py` 是唯一入口，全程零 LLM：

1. 讀 `sources.yml`，逐一抓取（RSS／FRED CSV／Polymarket JSON／少數純健康
   檢查用的 JSON），每個來源記一筆健康狀態。
2. 讀站內既有的 `docs/monitor|regime|rotation|crowding|detective/data/*.json`
   （已存在的日更數字骨幹），只在「今日新穿越門檻」或「狀態與昨天不同」時
   產生數字卡——不是每個序列每天都發卡。
3. 正規化成卡片（schema 見 DESIGN.md §11 的子集）、去重（URL 精確比對＋
   標題 token Jaccard ≥0.85 近重複合併）、丟棄 36 小時前的新聞（`data` 卡
   不受此限）、關鍵字 deny-list 過濾、依 tier／交叉印證數／新鮮度排序後
   截斷至 ≤200 條、對排名前 60 條做連結存活檢查。
4. 寫出兩個檔案。

## 輸入 / 輸出

| 檔案 | 角色 |
|---|---|
| `sources.yml` | 輸入：來源白名單（誰／怎麼抓／哪個維度／T1-T4） |
| `docs/monitor\|regime\|rotation\|crowding\|detective/data/*.json` | 輸入：站內既有數字骨幹（唯讀，本目錄不寫這些檔） |
| `docs/intel/pending/YYYY-MM-DD.json` | 輸出：候選卡片＋當日統計，餵給下一步 haiku/sonnet |
| `docs/intel/data/sources_health.json` | 輸出：每個來源本次抓取的 ok/latency/item_count/error |
| `docs/intel/data/state.json` | 輸出：跨日狀態（regime 標籤／輪動領先象限／擁擠極端集合／kill-watch near-set／Polymarket 前日機率），用來判斷「有沒有變」 |

## 怎麼加一個來源

1. 用真實 HTTP fetch 核實 URL（10 秒 timeout），確認回傳的是可解析的
   RSS/Atom 或 JSON，不是轉址回首頁的 HTML。
2. 在 `sources.yml` 加一筆，欄位說明見該檔開頭註解；`category` 必須是
   DESIGN.md §3 十三維度 key 之一。
3. `kind: rss` 直接吃 `fetch_rss_source`；`kind: csv` 只給 FRED 系列用
   （fetch.py 靠 `fred_` id 前綴＋URL 裡的 `id=` 參數辨識）；新的結構化
   JSON 來源（非 FRED、非 Polymarket）預設走 `fetch_json_healthcheck_source`
   （只健康檢查、不產卡）——要讓它產卡，得照 FRED／Polymarket 的模式在
   `dispatch_source()` 加專屬分支。
4. 抓不到的來源設 `enabled: false` 並在 `note` 寫清楚失敗原因（不要用猜的）。

## 本機怎麼跑

```bash
# 全量抓取（正式寫檔）
python3 scripts/intel/fetch.py --date 2026-08-19

# 只跑其中一個來源（除錯用）
python3 scripts/intel/fetch.py --date 2026-08-19 --only fed_press_all

# 只跑站內數字卡（不打任何外部 HTTP）
python3 scripts/intel/fetch.py --date 2026-08-19 --only onsite

# 乾跑，不寫檔（印統計即可，state.json 也不會被更新）
python3 scripts/intel/fetch.py --date 2026-08-19 --dry-run
```

依賴：`requests`／`feedparser`／`pyyaml`（皆為純 Python、無編譯依賴，GHA
安裝一行 `pip install requests feedparser pyyaml` 即可，不需要金鑰）。

## 2026-08-19 補充（orchestrator 驗收後修正）

- FRED 規則 1 改為「20 日變化 vs 近一年 20 日變化的 2σ」（原本對日變化 σ 比，10 條裡 6 條天天觸發）；新增規則 2「一年水位進出前／後 5% 分位」，只在換帶那天發卡（`state.json.fred_bands`）。
- 沒有時間戳的新聞（Nikkei Asia RSS）改用 `state.json.seen_news` 判新舊：首跑全收，之後只留第一次出現的，7 天後遺忘。
- `udn_money` 的 RSS 回 200 但零條，換成鉅亨網頭條 `cnyes_headline`（有日期、40 條）。
