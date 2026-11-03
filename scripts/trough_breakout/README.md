# scripts/trough_breakout — 翻身突破（雲端副本）

這個資料夾是 v7-backtest `src/trough_breakout/` 的同步副本，給 GitHub Actions 用，Mac 關機也能更新
/trough-picks/（`scripts/build_trough_picks.py` 產生）。規則、登記、結果都在 v7-backtest；這裡不改邏輯。

| 檔案 | 來源 |
|---|---|
| `__init__.py` `common.py` `engine.py` `prep.py` `signals.py` `tw_data.py` `risk.py` `run_tw_risk.py` `verify.py` `upgrade.py` `report_stats.py` | v7 `src/trough_breakout/` 原樣複製（內容必須一字不差） |
| `QueueOrder_IndustryMap_tw.csv` | v7 `docs/QueueOrder_IndustryMap_tw.csv` 原樣複製（同產業上限用的產業對照表） |
| 本 README | 只在網站 repo |

名單頁只跑一組：組合版（四條手段全加）、跌破 200 日線出場、設計 (i) 全部持有等權。登記
`docs/TroughBreakout_Risk_Prereg.md`（v7 commit 4e63690），結果 `docs/TroughBreakout_Risk_Results.md`（d1eb6e1）。

## 雲端跟本機的差別

程式本身不分雲端或本機，差別只在資料從哪裡讀（`common.ROOT` 與三個退路）：

- 資料根目錄 `common.ROOT`：預設是這個資料夾往上兩層（網站 repo 根目錄）；環境變數 `TB_ROOT` 可以改。
- 面板 `data/revmom/{prices,revenue,names,index_tr}.parquet`：雲端由 RevMom Daily 從 Release `revmom-data` 解開，
  跟 /revmom-picks/ 共用同一份，不另外抓。
- 隔夜拆款利率：v7 讀 `data/tw_cash_rate/call_rate_on_d.csv`；網站 repo 沒有這個檔，`tw_data.cash_csv()` 改讀
  `data/macro_db/series/tw.call_rate_on_d.csv`（同一條序列、同欄位）。也可用 `TB_CASH_CSV` 指定。
- 產業對照表：v7 讀 `docs/QueueOrder_IndustryMap_tw.csv`；網站 repo 的 docs/ 是公開網站，不放這個檔，
  `risk.industry_csv()` 改讀本資料夾的副本。也可用 `TB_INDUSTRY_CSV` 指定。
- Koyfin NTM EPS（`data/koyfin_estimates_tw/eps_ntm.csv`）：雲端沒有，`tw_data.load_eps()` 回傳空表，L3 全部不成立。
  組合版只用 L1、L2，不受影響。

`scripts/build_trough_picks.py` 在本 repo 沒有 `data/revmom/prices.parquet` 時，自動把 `TB_ROOT` 指到 `~/v7-backtest`
（可用 `TB_V7_ROOT` 改），所以在 Mac 上直接跑也行：

```bash
~/.venvs/v7bt/bin/python scripts/build_trough_picks.py --out /tmp/trough-check    # 本機用 v7 的資料，頁面寫到別處
```

## 同步方式

v7 改了 `src/trough_breakout/` 或產業對照表之後，在 Mac 上：

```bash
cd ~/v7-backtest
for f in __init__ common engine prep signals tw_data risk run_tw_risk verify upgrade report_stats; do
  cp src/trough_breakout/$f.py ~/financial-analysis-bot/scripts/trough_breakout/; done
cp docs/QueueOrder_IndustryMap_tw.csv ~/financial-analysis-bot/scripts/trough_breakout/
for f in __init__ common engine prep signals tw_data risk run_tw_risk verify upgrade report_stats; do
  cmp src/trough_breakout/$f.py ~/financial-analysis-bot/scripts/trough_breakout/$f.py; done
```

再逐檔 commit 網站 repo。反方向：這裡的同名檔若被改過，先 `diff` 回 v7、在 v7 改好再照上面複製，兩邊不要各改各的。
改了產業對照表會讓已存檔的名單跟重算結果不同，頁面會標「修正」，這是預期的。

## 排程

`.github/workflows/revmom-daily.yml`（RevMom Daily，平日 18:50 台北）在 revmom 產頁之後跑
`python scripts/build_trough_picks.py`，產出 `docs/trough-picks/{index.html,data.json,history/*.json}` 跟 revmom 的頁面一起
commit。這一步失敗時 job 標紅，但 revmom 的頁面照常 commit、push，資料照常回傳 Release。
