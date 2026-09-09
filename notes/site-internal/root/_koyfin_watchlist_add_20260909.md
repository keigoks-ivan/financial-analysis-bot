# Koyfin watchlist 待補名單（2026-09-09，v3 席位資格）

**用途**：v3 席位資格要求成長預估必須是三年期（Koyfin FY1→FY3 CAGR），不是 yfinance
單年 fallback。以下名字目前在研究母體（`docs/engine/universe_board.json`）裡，但**不在
最新一份 Koyfin EPS Excel 覆蓋範圍內**——把它們加進 Koyfin `dd_screener` watchlist（連同
FY1/FY2/FY3E EPS、ROIC、FCF Margin、ROIC 5Y Avg 五欄），下次 `refresh-eps-screener` /
`refresh-eps-screener-web` 跑完，這些名字就會拿到三年成長率，脫離「可選但先不入席」隊列、
正式參與席位競爭。

比對基準：
- 研究母體 = `docs/engine/universe_board.json`（as_of 2026-09-08，276 檔唯一 ticker）
- Koyfin 覆蓋 = `data/eps-estimates/DD_universe_EPS_estimates_20260904.xlsx`（snapshot 2026-09-04）

未覆蓋合計 **46 檔**：DD 池 19 檔 + QGM 品質池 27 檔。

## DD 池（19 檔，已有 DD 報告，但 Koyfin 沒這個 ticker 或代碼對不上）

```
5246.KL  5326.KL  5398.KL  6139.KL  AAON  AEIS  AVT  DOCN  DY  INCY
KNX  LFUS  LSCC  LYC.AX  MSM  NXT  ROKU  SMTC  VACN.SW
```

備註：`5246.KL`／`5326.KL`／`5398.KL`／`6139.KL`（大馬掛牌）與 `LYC.AX`（澳股）／
`VACN.SW`（瑞士）為海外掛牌，Koyfin 若無對應代碼可能要用主掛牌別名（比照現有
`LVMH→MC`、`SU→SU.FR` 模式，見 `scripts/load_eps_estimates_xlsx.py` 的
`_EXPLICIT_ALIASES`）；`INCY` 在 universe_board 裡同時有 dd-pool 與 qgm 兩筆列（既有資料
重複，非本清單造成），歸在 DD 池即可。

## QGM 品質池（27 檔，目前只有 yfinance 單年 FY1→FY2 成長，卡在隊列）

```
ADP  ADSK  ALNY  AMP  BMY  CBOE  CL  CTSH  DXCM  EOG
EXPE  FANG  FFIV  GDDY  GEN  INTU  IT  MCO  MO  MSCI
NEM  ODFL  PODD  PTC  RMD  VRSK  VRTX
```

這一批一旦補上 Koyfin 三年成長率，就會脫離 `build_arena.py` 的「可選但先不入席：缺三年
成長預估」隊列，用真實三年 CAGR 重新跟現任席位比擁有層分。

## 下一步

1. 把上面 46 個代碼加進 Koyfin `dd_screener` watchlist（USD 幣別）。
2. 跑 `refresh-eps-screener-web`（或等新 Excel 用 `refresh-eps-screener`），順帶把
   ROIC／FCF Margin／ROIC 5Y Avg 三個選填欄位一起抓（見兩份 skill 2026-09-09 更新）。
3. 下次 `daily-taipei-morning.yml` 排程（已加 `--include-non-dd`）跑完，`docs/dd-screener/
   latest.json` 會帶著這些名字的 Koyfin 三年成長率；`build_arena.py` 週跑後這批就有機會
   進入「可選但先不入席」隊列的三年成長率競爭，甚至坐上席位。
