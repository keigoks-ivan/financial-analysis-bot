# 選股主控台整併：4 頁 → 1 console（2026-07-10）

狀態：**已執行**。持有人 2026-07-10 裁決「這四頁重複太多，整合成一個」。
前身：`_proposal_stock_pages_cleanup_20260707.md`（定義四頁職能：cockpit 入口／picks 對外榜／pipeline 流程板機／engine 排序席位）。
本次把該提案的「並存＋分工聲明」升級為「單一 console 四分頁」——**收斂職能表面（surface），不砍任何職能（function）**。

---

## 1. 每頁職能 × 數據源 × builder 盤點

| 頁面 | 職能（獨有內容） | 數據源 | 產生器 | cron |
|---|---|---|---|---|
| `/cockpit/index.html` | 入口：環境／今日待辦裁決／漏斗五層活數字／精選榜摘要／組合記分板 | risk_gauge・risk_history・momentum-5・latest・sop-funnel・arena・cyclical・candidates・tenbagger・picks（10+ JSON，client fetch） | **無**（純前端手寫） | 無（隨各 JSON 排程） |
| `/picks/index.html` | 對外正式榜：長熬／爆發／十倍 official＋候選，每檔「四件事」 | candidates.json・tenbagger.json・picks.json（client fetch，相對路徑 `./`） | **無**（純前端手寫；資料由 build_picks.py＋build_tenbagger.py 產 JSON） | weekly-market-update（僅 JSON） |
| `/dd-screener/pipeline.html` | 流程板機：宇宙／資格閘明細／三軌射擊名單／板機現況＋否決對照組／**回看鏡（發現力稽核）**／**全宇宙潛力榜**／發現層明細（discovery pool＋形狀掃描） | latest・cyclical・sop-funnel latest＋ledger・pre_id_scan・**weekly_cache/*.json**（server 端逐檔算週線報酬） | `build_pipeline_page.py`（server-baked HTML，102KB，重運算） | weekly-fundamental-refresh |
| `/engine/index.html` | 排序席位（GRP）：五步漏斗／權力分工／組合快照／三鐵律／L0-L4 架構／路線圖 | radar・arena・cards・scoreboard JSON | `engine/build_index.py`（page_shell） | weekly-engine |
| `/engine/{radar,arena,cards,scoreboard}.html` | engine 深層明細（雷達／擂台／決策卡／記分板） | 各自 JSON | `engine/build_{radar,arena,cards,scoreboard}.py` | weekly-engine |

## 2. 重複內容矩陣（結論）

| 職能 | cockpit | picks | pipeline | engine |
|---|---|---|---|---|
| 市場環境儀表 | ● 唯一 | | | |
| 今日待辦裁決 | ● 唯一（arena duels＋mom flags＋sop signals 聚合） | | | ○ alert 計數 |
| 漏斗五層 | ○ 摘要 | | ● 深（EV5y 鏡頭·三軌·板機·回看·潛力榜） | ○ 五步摘要（GRP 鏡頭） |
| 精選榜（長熬／爆發／十倍） | ○ 摘要 chips | ● 深（四件事＋候選） | | |
| GRP 排序席位 | ○ 記分板摘要 | | | ● 深（radar／arena／cards／scoreboard） |
| 回看鏡·潛力榜·發現層明細 | | | ● 唯一 | ○ radar 另一鏡頭 |
| Momentum-5 對照 | ● 唯一 | | | |

**結論**：`cockpit` 本來就是全體的 summary superset（設計為入口）；`picks／pipeline／engine` 各自持有「某一切片的深版」。真正的重複是「cockpit 摘要 vs 三頁深版」的一頁兩讀，以及提案已指出的「漏斗雙鏡（pipeline EV5y vs engine GRP）」「名單雙軌（picks 對外 vs arena 機器）」。這兩套是**方法論不同的並存**（提案 D1／D4 已裁決保留），不是可刪的重複——所以整併＝**把三個深版收進 cockpit 的分頁**，cockpit 原摘要成為「總覽」分頁，一個職能都不丟。

## 3. 最終架構

`/cockpit/` 升級為**選股主控台**，四分頁（deep-link hash 錨點）：

| 分頁 | 錨點 | 內容 | 實作 |
|---|---|---|---|
| 總覽 | `#overview` | 現 cockpit 五區（環境／待辦／漏斗／精選摘要／記分板） | 原 client JS **原封不動** |
| 精選榜 | `#picks` | picks 全內容 | iframe → `/picks/_embed.html` |
| 流程板機 | `#pipeline` | pipeline 全內容 | iframe → `/dd-screener/_pipeline_body.html` |
| 席位排序 | `#seats` | engine 總覽（含連往 radar／arena／cards／scoreboard 深頁） | iframe → `/engine/_index_body.html` |

**為何 iframe 而非 client re-render**：pipeline 是 server-baked（逐檔讀 `weekly_cache` 算回看鏡、潛力榜異常抽出），engine cards.html 達 239KB——把這些 Python 渲染邏輯搬成 JS 會製造**資料漂移＋大量 bug 風險**，且違反「不重做分析邏輯」。同源 iframe 做到**零重寫、零漂移、樣式完全隔離**，builder 只改輸出目標（產 nav-less 片段），保留全部運算。片段頁 `<base target="_parent">` 讓內部跨頁連結（DD／engine 深頁）在頂層開啟。

**Surface 帳**：對外入口 4 → **1**（`/cockpit/`）。`/picks/`、`/dd-screener/pipeline.html`、`/engine/` 三個舊 URL → 輕量 redirect stub（meta refresh＋canonical＋noindex → 對應 tab 錨點），比照 `/six-state/` stub 模式。engine 深層 4 頁（radar/arena/cards/scoreboard）維持獨立明細頁（非重複面，從席位排序分頁連入），不動。

## 4. 每個 builder 的處置

| builder | 舊輸出 | 新處置 |
|---|---|---|
| `build_pipeline_page.py` | `pipeline.html`（含 nav） | 改輸出 `dd-screener/_pipeline_body.html`（nav-less 片段，`<base target=_parent>`，noindex）。**所有運算、資料源、console summary 不變**。 |
| `engine/build_index.py` | `engine/index.html`（page_shell 含 nav） | 改用 `page_embed_shell`（common.py 新增）輸出 `engine/_index_body.html`（nav-less 片段）。內容不變。 |
| `build_picks.py` | `candidates.json`（資料，無 HTML） | **不動**（cockpit／picks embed 都 client 讀它）。 |
| `build_tenbagger.py` | `tenbagger.json`（資料） | **不動**。 |
| `engine/build_{radar,arena,cards,scoreboard}.py` | 各自 JSON＋HTML 明細頁 | **不動**（明細頁保留；JSON 供 cockpit／engine embed 讀）。 |
| `docs/picks/index.html` | 手寫頁（無 builder） | 內容搬 `picks/_embed.html`（nav-less），index.html 換 redirect stub。 |

**資料 JSON 一律照舊產出**，下游（cockpit／embed）繼續 client fetch，無斷更。

## 5. nav 與站內引用

- **nav：零改動**（遵循 task「prefer ZERO nav-label changes」）。選股下拉維持列 駕駛艙／精選清單／Pipeline／決策引擎；後三者點擊 → 舊 URL → redirect → 主控台對應分頁。全站無 re-inject，避免與並行 DR session 撞車。
- **site_nav.py SKIP_FILES**：新增 6 檔——3 個 redirect stub（picks/index、dd-screener/pipeline、engine/index）＋ 3 個 embed 片段（picks/_embed、dd-screener/_pipeline_body、engine/_index_body），防 self-heal 把站 nav 灌進 iframe 片段 / 覆寫 stub。
- cockpit 內部指向被折疊頁的 top-level 連結改指 tab 錨點（`#picks`／`#pipeline`／`#seats`），點擊切分頁不整頁 reload；指向 engine 深頁（arena.html/radar.html）的連結保留（明細頁仍在）。

## 6. 治理凍結（原樣搬移，一字不改）

- picks 爆發榜 v1.1 雙窗口＋自動上榜＋veto 規則：只搬 HTML/JS，`build_picks.py` 規則邏輯**未觸碰**。
- M5 對照組 PREREG：未觸碰（cockpit 記分板 JS 原封）。
- GRP 席位「寧缺勿濫＋人工治理」語言：engine embed 內容不變。
- 各頁描述器／非部位指令紀律：片段內文一字未改。

## 7. 需人工確認

1. **nav 是否要瘦身成單一「選股主控台」入口**（移除下拉的 精選清單／Pipeline／決策引擎 三項，只留主控台）。本次為零 nav 改動（redirect 已保通）；若要瘦身需改 `site_nav.py` 全站 re-inject，建議待並行 DR session 結束後單獨一輪做。
2. iframe 內 pipeline 的 `#lookback`／`#leaderboard` 站內錨點在 `base target=_parent` 下會跳頂層（無對應錨點，等同 no-op）——屬可接受的輕微降級。
3. engine `radar/arena/cards/scoreboard` 深頁是否日後也折進 席位排序分頁的子分頁（提案 P3「engine 併頁」）——本次不做。
