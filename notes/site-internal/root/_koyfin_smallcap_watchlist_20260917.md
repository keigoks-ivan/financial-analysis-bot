# Koyfin smallcap watchlist 建置紀錄（2026-09-17）

給 `refresh-eps-screener-web` skill 未來收編用的操作紀錄——本次是新母體
（`dd_smallcap`），不是既有 `dd_screener` 的例行刷新。

## 篩選器（My Screens → 新建，名稱 `dd_smallcap_v5`）

Stocks 分頁「Get started from scratch」。Universe：Trading Region = United
States and Canada（預設）＋加一條 Universe Criteria「Trading Country」=
United States (US)。Filter：Market Cap（USD）1000M–20000M（$1B–$20B）；
ROIC (LTM) ≥15（搜尋「ROIC」→ Return on Invested Capital → 子選單 LTM）；
FCF Margin % (LTM) ≥10（搜尋「FCF Margin」→ 選 Free Cash Flow Margin %，
不是 excl. SBC 那個 → 子選單 LTM）。結果 **209 檔**（brief 預期 80–250）。

## 存成 watchlist

篩選結果頂端「Save as watchlist」，預設名 `dd_smallcap_v5 (Screen
Results)`，改名存成 `dd_smallcap`——209 檔一次存入，未觸發人工上限。

## 欄位模板（複製 dd_screener 的 80 欄）

Column Selection 對話框沒有「套用其他 watchlist 欄位」按鈕；改用
**Duplicate Watchlist**（工具列，在 `dd_screener` 分頁按）：整份複製（含
80 欄＋原 ~56 檔 DD 名字）。複製後：全選（表頭 checkbox）→ Bulk Actions →
Delete 清空舊名字；回 `dd_smallcap_v5` 篩選結果全選 → Bulk Actions → Add To
Watchlist → 選複製出來的 list，灌入 209 檔。刪掉最早那份 8 欄的
`dd_smallcap` 草稿，複製版改名成 `dd_smallcap`。驗證：橫向捲動收表頭文字，
`headerCount===80`。

## 抓取（沿用 skill v2.0 Step 1–4，改讀新 watchlist）＋下游

```bash
python3 scripts/koyfin_xlsx_from_raw.py \
  --raw /path/to/koyfin_smallcap_raw_20260917.txt \
  --out data/eps-estimates/DD_smallcap_EPS_estimates_20260917.xlsx \
  --snapshot-date 2026-09-17 \
  --universe-note "dd_smallcap watchlist (screen dd_smallcap_v5: US, \$1-20B, ROIC>=15, FCF>=10)"
python3 scripts/build_dd_screener.py --universe smallcap
python3.12 scripts/build_tenbagger.py
```
