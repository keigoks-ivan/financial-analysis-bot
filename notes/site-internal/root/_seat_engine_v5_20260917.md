# 席位引擎 v5（2026-09-17）

## 為什麼要改

owner thesis：「品質派 ∩ 獲利上修 ∩ 突破還原權息歷史新高」。品質是資格門檻，獲利
上修是排序的唯一依據，價格動能整個退出排序；買點收斂成一個變數——距還原權息全
歷史最高收盤價（不是 52 週高）。v4 的五百分位排序把上修、動能、成長、品質、殖利率
五個異質變數硬拗成一個分數，稀釋了驗屍證明最強的單一訊號（上修）。耐久若只看五年
均值會被一次性獲利誤判，需要三年均值與現值同時達標的一致性檢驗。

## 改了什麼

1. **資格＝品質派**：品質閘×三年成長×站上 52 週線×耐久一致性（`grp.durable_5y_v5()`：
   QGM 五年穩定度 ≥75%，OR Koyfin 五年∧三年∧現值三者皆 ≥15%）。財報後上修 ≤−5%／
   體質拒絕／衰退 ⛔／DD 迴避／融券占流通股比 >10% 皆整體排除——v5 沒有衛星軌可以
   收留，融券高與耐久都從「只排除核心候選」升級為「整體資格排除」。
2. **排序＝上修單一變數**：池＝資格全過名字中財報後上修 ≥+5%（`grp.in_pool()`）者，
   池內依上修降冪排序，同值 tie-break `implied_growth_pct`、再 tie-break 盈餘殖利率
   （`grp.pool_sort_key()`）。own_score_v4 五百分位保留一輪只做「v4 對照」tooltip。
3. **板機＝距歷史新高**：`timing_lamp()` 全面改讀 `ma.dist_ath_pct`（還原權息全歷史，
   `build_dd_screener.compute_ath_highs()`，`data/ath_cache.json` 7 天 TTL＋每日高
   水位刷新）與 200 日線。綠＝距新高 ≥−3% 且站上 200 日線；黃＝−10%~−3%；紅＝距新高
   <−10% 或跌破 200 日線；橘（過熱）需同時滿足綠燈級距離才降級半倉。RS／階段降為
   tooltip。
4. **席位**：核心＝池前 5，月頻輪動不變（七項硬否決，原六項＋融券高）。衛星軌取消，
   等待池＝池扣掉核心，分「②可買（綠/橘燈）」「③等待池（其餘）」；④收合區列資格
   過閘但上修未達 5% 的名字。`arena.json` 的 `sat_seats` 保留 key，內容改成整個等待池
   （帶 `track:"pool"`）。
5. **`--daily`**：取代 v4 窄流程 `--lamp-only`——全量重跑資格/池/排序/時機燈，不寫
   `arena-ledger.json`，核心席名單仍從帳本 `roster.core` 讀，命中硬否決立即顯示替換
   （下次 `--ledger` 排程才落帳）。`--lamp-only` 保留為別名。

## 陣容對照（2026-09-17 實跑，未帶 `--ledger`）

| | 舊（arena-ledger.json 最近一筆 v3 snapshot，2026-09-12） | 新（v5，本次） |
|---|---|---|
| 核心 5 | NVDA・ASML・TSM・FIX・TXN | STX・LRCX・CLS・KLAC・DELL |
| 衛星/可買 | VRT・PLTR・LLY・ANET・LRCX | 可買：FTNT（綠燈） |
| 等待池 | — | ASML・MSFT・TER・NVDA・JBL・CAH・ANET・TSM・TXN・FIX・NTAP・AMAT・CAT・GRMN（14 檔） |

池大小 20（核心 5＋可買 1＋等待池 14）；④收合區 19 檔。核心全數 RED／HOT 燈（距新高
−28%~−44%，DELL −0.7% 但動能過熱轉 HOT）——耐久＋上修最強不等於現在能買，時機燈才
回答這個問題，同 v4 CLS 案例精神。STX／LRCX 通過新耐久判準（前者 Koyfin 三點皆
≥15%，後者退回 QGM 路徑）；ASML（上修 29.8%，第 6 名）差一名沒進核心。

ATH sanity（5 檔）：FTNT −0.58%／DELL −0.71%（皆 <3%）、NVDA −9.06%、LRCX −37.87%、
JBL −22.90%——與 5 年高代理逐位吻合（5 檔的 5 年高本身就是全歷史新高）。

## 證偽條件

見 `knowledge/rule_ledger.md`「v5 席位引擎：品質派資格 × 上修排序 × 歷史新高板機」列。

## 沒做/未驗證

`arena-ledger.json` 尚未跑過任何 v4/v5 `--ledger`（`roster` 仍是 `None`），本次核心
輪動走的是 bootstrap 整批重選路徑，「月中沿用＋硬否決立即下席」的路徑只在
`test_arena_rotation_v4.py`/`test_arena_lamp_only.py` 的合成 fixture 裡驗證過，
真實資料下的月中沿用行為要等下一次 `weekly-engine.yml --ledger` 跑次才會發生。
QGM／快審卡供給列缺 `ma.dist_ath_pct`/`mom_12_1_pct`（僅有 `above_w52`/`price`），
`timing_lamp()` 對這些列會落「資料缺」黃燈 fallback，非 DD 池名字的時機燈精確度
較低。
