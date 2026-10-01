# scripts/revmom_backtest — 台股月營收動能（雲端副本）

這個資料夾是 v7-backtest `src/revmom_backtest/` 的同步副本，給 GitHub Actions 用，Mac 關機也能更新
/revmom-picks/ 與 /backtest/revmom/。規則、規格、帳本都在 v7-backtest；這裡不改邏輯。

| 檔案 | 來源 |
|---|---|
| `__init__.py` `data.py` `engine.py` `signals.py` `run.py` `verify.py` `picks.py` `update_data.py` `generate_page.py` `generate_picks_page.py` `site_env.py` | v7 `src/revmom_backtest/` 原樣複製（內容必須一字不差） |
| `site_kit.py` | v7 `src/site_kit.py` 原樣複製 |
| `pubdates.py`、本 README | 只在網站 repo |
| `../../data/revmom/ledger_revmom.json` | v7 實驗帳本 REVMOM 的快照（雲端沒有帳本，回測頁的試驗次數與 DSR 從這裡讀） |

`site_env.py` 會判斷自己在哪裡跑：在網站 repo 裡，資料、結果、輸出頁面都在網站 repo 本身；在 v7 裡，頁面寫到旁邊的
`~/financial-analysis-bot`（可用 `REVMOM_SITE_ROOT` 改）。

## 兩個 workflow

- `.github/workflows/revmom-daily.yml`（RevMom Daily）：平日 18:50 台北。資料放在 Release `revmom-data` 的
  `revmom-data.tar.gz`（`data/revmom/*.parquet`、`meta.json`、`data/revmom_raw/`、`results/revmom/`），不進 git。
- `.github/workflows/revmom-pubdates.yml`（RevMom Revenue Pubdates）：每天 08:05、18:35 台北，記錄月營收公布時間，
  寫進 `data/revmom/revenue_pubdates.csv` 與 `revenue_pubdates_runs.csv`（進 git，只追加）。

## 同步方式

v7 改了程式（或帳本新增 REVMOM 試驗）之後，在 Mac 上：

```bash
cd ~/v7-backtest
for f in __init__ data engine signals run verify picks update_data generate_page generate_picks_page site_env; do
  cp src/revmom_backtest/$f.py ~/financial-analysis-bot/scripts/revmom_backtest/; done
cp src/site_kit.py ~/financial-analysis-bot/scripts/revmom_backtest/site_kit.py
~/.venvs/v7bt/bin/python -m src.revmom_backtest.generate_page /tmp/revmom_check.html   # 順便重寫帳本快照
cp data/revmom/ledger_revmom.json ~/financial-analysis-bot/data/revmom/ledger_revmom.json
```

再逐檔 commit 網站 repo。反方向：這裡的同名檔若被改過，先 `diff` 回 v7、在 v7 改好再照上面複製，兩邊不要各改各的。

改了資料格式（例如重新匯出 `data/revmom/`）時，要重新上傳 Release：

```bash
cd ~/v7-backtest
tar czf /tmp/revmom-data.tar.gz --exclude=ledger_revmom.json --exclude=job.log data/revmom data/revmom_raw results/revmom
gh release upload revmom-data /tmp/revmom-data.tar.gz --clobber -R keigoks-ivan/financial-analysis-bot
```

注意：Release 上的資料由雲端每天往前更新，v7 本機的 `data/revmom/` 不會自動跟上；要在本機跑，先
`gh release download revmom-data -p revmom-data.tar.gz -R keigoks-ivan/financial-analysis-bot` 再解開。
