# 精選榜改版：爆發組退役、十倍組改 v5 小市值池（2026-09-17）

## 為什麼要改

爆發（循環拐點型）追循環股價格動能，跟 v5 席位引擎 thesis「品質派資格 ∩ 獲利上修
排序 ∩ 突破還原歷史新高、價格動能整個退出排序」正面矛盾；記分板顯示循環轉折形狀
（n=20）中位報酬 −2.8%、虧損率 55%，是輸家形狀。十倍組原 gate-set（逐檔 yfinance
掃六條件，全數標「未調參」、從未回溯驗證）是與 GRP 席位獨立的一把尺，兩尺並存徒
增認知成本，統一為同一套已校準的規則、只換市值帶，風險更低。

## 改了什麼

1. **爆發退役**：比照長熬（2026-07-29）先例。`build_picks.py` 移除 `build_baofa()`
   及整條 cyclical-track/sop-funnel/radar/arena/ID 產業趨勢 pipeline，`candidates.json`
   的 `official_baofa[]`／`baofa[]` 寫死空陣列＋`retired_groups.baofa`。`picks.json`
   changelog 新增一筆、`rules.retired_baofa` 留痕。
2. **十倍組全面重寫**：`build_tenbagger.py` 不再自建 gate-set，改逐字重用 GRP 席位
   v5 資格閘（`grp.quality_gate`／`durable_5y_v5`／成長閘含基期效應／`grp_score`／
   `pool_sort_key`／`in_pool`／`timing_lamp`，經 `build_arena.row_dict`／`_flat_view`）
   跑在 $10億–$200億市值帶。母體＝`data/engine/universe.json`（972 檔）∪
   `docs/dd-screener/latest.json` ticker，查不到 v5 欄位或市值未知者計入「資料
   不足」，不用 QGM 原始池回推湊數（缺 revision/timing 欄位會讓資格閘失真）。市值
   來源：`qgm_seed.market_cap_b` → `mktcap.json` 快取 → QGM 原始池 → 網路補。
3. **無核心席、無月頻輪動**：`official`＝池（依上修排序，無上限）、`buyable`＝綠/
   橘燈、`waiting.{yellow,red}`＝其餘依燈號分組、`not_in_pool`＝資格過但上修未達
   5% 收合複審；無 `seat_cap`（舊 schema 遺留鍵，v5 不消費）。
4. **排程改每日**：`daily-taipei-morning.yml` Step 2b（Arena `--daily` 之後），鏡射
   進 `daily-non-fundamental-refresh.yml`；`weekly-market-update.yml` 移除舊兩步。
5. **頁面**：`_embed.html` 改「①可買②等待池③收合」單表，欄位對齊 GRP 席位表
   （代號／上修%／距歷史新高%／下次財報／耐久／時機／倉位／DD／備註）；cockpit
   picks 分頁摘要句同步改寫。
6. `generate_list_forecasts.py` 的 `picks`／`late` producer 降 dormant（讀空陣列
   時印明「來源已退役」），PREREG claim_template 不刪。

## 實跑結果（2026-09-17，`python3.12 scripts/build_tenbagger.py`）

universe 980 檔（扣 .TW）→ 池覆蓋 263 → 市值可判定 250 → 落在 $10億–$200億帶 56 →
資格閘全過 **0**（47/56 卡耐久、30/56 卡站上 52 週線、29/56 卡三年成長多數缺
Koyfin 三年期預估、13/56 卡融券 >10%，卡點重疊、分散在多閘，非單一閘全滅——誠實
掛零非 bug）。資料不足：未在池覆蓋 717、市值未知 13；帶外 194。

## 證偽條件

見 `knowledge/rule_ledger.md`「精選榜改版：爆發組退役、十倍組改 v5 小市值池」列。

## 沒做/未驗證

小市值池目前掛零，無「可買」實例可供 UI 視覺驗算（表格渲染以合成 fixture 在
`scripts/tests/test_picks_v5.py` 驗證）。市值網路補抓對 .KL/.T/.AX/.SW 等非 .TW
外國掛牌會打 404（`grp.fetch_caps()` 既有行為，非本次新增，僅警告不影響輸出）。

## 追記（2026-09-17b）：母體太窄是主因，補第二個 Koyfin 母體

上面「資格閘全過 0」的漏斗顯示卡點分散在耐久／52 週線／三年成長／融券四道閘，
但更根本的問題是母體只有 56 檔——`data/engine/universe.json` ∪ 主 dd-screener
池落在 $10–200 億市值帶的名字就這麼多，56 檔要同時扛四道閘，統計上池長期掛零
是必然，不是規則系統性太嚴。

**新母體＝獨立 Koyfin 篩選器**，不沿用 DD 池／QGM 池：

- 篩選器 `dd_smallcap_v5`：Trading Country=US（含 ADR）、Market Cap $1,000M–
  $20,000M、ROIC (LTM) ≥15%、FCF Margin % (LTM) ≥10%——209 檔命中。
- 存成 watchlist `dd_smallcap`（與既有 `dd_screener` 各自獨立，互不覆蓋），
  欄位比照 `dd_screener` 複製同一套 80 欄（同一份 Koyfin 帳號 duplicate
  watchlist 再換 ticker 成員，見 `_koyfin_smallcap_watchlist_20260917.md`）。
- `scripts/build_dd_screener.py --universe smallcap`：母體只認這 209 檔（無
  DD 池／QGM 池假設），寫 `docs/dd-screener/smallcap/latest.json`，主
  latest.json 位元組不變（同檔改動前後對 AAPL/NVDA/TSM 關鍵欄位做過 diff）。
- `scripts/build_tenbagger.py`：母體改讀 smallcap latest.json ∪ 主
  latest.json 帶內名字，同 ticker 兩邊都有時主池列優先——56 檔不會被小市值
  池的資料蓋掉，只是多 209 檔候選可以判定資格。

**首次快照無基準**：`docs/dd-screener/smallcap/eps-estimates-snapshots/
2026-09.json` 是這批母體第一份月度快照，本輪上修（`rev_used_pct`）沒有前月
可比，資格閘全過的 smallcap 名字這輪一律顯示上修缺值，`grp.in_pool()` 對缺值
不收（既有規則，非本次新增），所以池今天仍可能是 0——是基準未建，不是規則
又失靈一次。頁面（`docs/picks/_embed.html`）用 `smallcap_rev_baseline_note`
欄位顯示「上修基準將於下次快照建立（YYYY-MM）」，避免使用者誤讀。下次重跑
（10 月）才有第一個真實上修數字可判。

**驗證過程中發現並修的兩個既有 bug（非本次新增規則，純機械修正）**：
1. `_fetch_live_fy_eps()` 的「無 DD 錨點」分支（`build_dd_screener.py` 約
   3077 行）只把 xlsx 的 `growth_fy1_fy2_pct`／`cagr_fy1_fy3_pct` 原樣抄出，
   沒有像有 DD 錨點的分支那樣做 FY1/FY2/FY3 回推 fallback——這條分支是**所有**
   `dd_status="none"` 名字（既有 QGM 27 檔＋新 smallcap 208 檔）的唯一路徑，
   結果 27 檔既有 QGM 名字與全部 smallcap 名字的 `eps_fy1_fy3_cagr_pct` 一律
   是 None（即使 fy1/fy3 EPS 都在），三年成長閘因此系統性餓死。修完後 QGM
   27/27、smallcap 183/208 拿到真實 CAGR。
2. `_load_eps_rev_3m_baseline()` 挑「離目標 90 天最近」的月度快照時沒檢查
   候選快照是否真的早於今天——smallcap 池第一次建母體時，唯一存在的快照就是
   今天剛寫的 `2026-09.json`，於是被當成「最近」基準選中，把每個 ticker 的
   今天資料拿去跟自己比，得出假的 `0.0%`（不是預期中的 `None`）。加了
   `sd_date >= current_date` 就跳過的守門後，smallcap 池首輪正確顯示
   `None`；主池母體因為一直有真實歷史快照，這個守門是 no-op（同一份基準
   選擇結果不變，已跑 `--include-non-dd` 前後對照驗證）。
