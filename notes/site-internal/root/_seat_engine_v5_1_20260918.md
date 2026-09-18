# 席位引擎 v5.1 設計稿（2026-09-18）

持有人 2026-09-18 拍板三件事，都在 v5 之上加，不改 v5 的排序與板機。

## 1. 資格加估值閘（機械，取代 DD 裁決的估值判斷）

- 紅燈＝PEG >2.0，或 PE NTM 相對五年均倍數 >1.5，任一個紅就紅。紅燈不進池。
- PEG 取 `live_peg`（現價重算）優先，缺則 `peg`（Koyfin）。倍數＝`pe_vs_5y_x`（Koyfin PE NTM ÷ PE NTM 5Y Avg）。
- 五年本益比分位只有 DD 報告有，沒 DD 的名字沒有；持有人拍板用倍數代替分位，不加 Koyfin 欄。
- 缺值：兩個都缺 → 不否決，標 ⚪ 缺值；缺一個 → 用另一個判。
- 它是入池／月頻換席時的資格閘，不是月中硬否決。核心席月中不因估值轉紅下席。
- 市場隱含成長率（反推 DCF）只顯示、不當閘，跟既有 `implied_growth_pct`（增量 ROIC × 再投資率）分開命名。
- DD skill 不動（待決 A／B 未選，本次只補閘）。下檔閘（離 200 日線 >15%）本次不做。

## 2. 主母體加 Koyfin 大市值來源（DD 選配落實）

- 現況 279 檔＝252 有 DD ＋ 27 QGM 無 DD；Koyfin 表只補資料不決定母體。
- 新增第三來源：Koyfin 篩選 `dd_largecap_v5`＝美股、市值 ≥ 200 億美元、ROIC LTM ≥15、FCF Margin LTM >0。
  FCF 用 >0 不用 ≥10：品質閘本來就有「ROIC ≥25 ∧ FCF ≥0」豁免路，清單要接得住重投資期的名字；FCF 0–10 且 ROIC <25 的會被閘刷掉。
- xlsx family `DD_largecap_EPS_estimates_`，`universe_source="largecap-koyfin"`，照小市值池 `_smallcap_universe_entries()` 的寫法。
- 新名字第一個月沒有上修基準，進不了池（同小市值池），10 月第二份快照才有。
- 沒 DD 的欄位（分位、護城河、裁決）一律空，引擎已能處理（QGM 列先例）。

## 3. VCP 深度 1（只當標籤和排序，燈號倉位不變）

- 用 `scripts/screener.py::calc_vcp()` 在 dd-screener 端算，原料是既有的日線（需補最高、最低、成交量）。
- 🟡 等待池多一欄「底部緊度」；🟡 組內排序改成先 VCP 過不過、再上修。🟢 標「緊縮後突破」或「鬆散突破」。
- 只在距歷史新高 10% 以內的名字算 VCP，避免 VCP 的底部高點（260 日內最高）與板機的全歷史新高量的不是同一個點。
- 沒記分板前不進燈號。
- 實作記錄（C，2026-09-18 完成）：`calc_vcp()` 因 `screener.py` import 時會寫檔（`HISTORY_DIR.mkdir`），改搬到新模組 `scripts/vcp_core.py`，`screener.py`／`screener_tw.py`／`screener_jp.py`／`screener_my.py` 改從那裡 re-import，行為不變。原料不是另開下載，是重用 `compute_daily_5y_highs()` 已經抓的 5 年日線（該函式原本只留 Close，這次順手把 High/Low/Volume 也一起留下，供 `compute_vcp_tag()` 用）。新增欄位：`vcp_scope`（computed／far_from_ath／insufficient_bars／None）、`vcp_gate`（pass／contraction／trend）、`vcp_score`、`vcp_pullback_count`、`vcp_last_pullback_pct`、`vcp_vol_dryup_ratio`、`vcp_base_age_days`、`vcp_tight`（bool，`vcp_gate=="pass"`）。

## 實作分工

A＝估值閘（sonnet）；B＝母體來源（sonnet）；C＝VCP（sonnet，A、B 之後）。各自不 commit，主 session 統一驗收、跑 `python3.12 -m pytest scripts/tests/`、commit、push。
