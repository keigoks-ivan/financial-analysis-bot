# 建議書：整站資訊架構重整（2026-07-07）

狀態：**提案，未執行**。承接同日「選股頁面整理」（_proposal_stock_pages_cleanup_20260707.md），這次處理的是**站層**：nav 分群、首頁、與跨群散落問題。

---

## 0. 問題定性

nav 現況＝3 個 catch-all 下拉（研究 12 項＋市場 9 項＋工具 11 項）＋2 個頂層連結，共 34 個目的地。三群是「內容形態」分群，不是「使用意圖」分群，造成：

1. **選股系統散在兩個選單**：cockpit／picks／Momentum-5 在「研究」，dd-screener／engine／QGM×2／RS+VCP×4 在「工具」——用戶要選股得跨兩個下拉找 10 個目的地。這是「散落各處」的最大來源。
2. **「研究」群 12 項混了四種東西**：選股輸出（cockpit/picks/M5）＋個股研究（DD/synthesis/comparisons）＋產業研究（ID/supply-chain/Tier Matrix）＋跨資產描述器（crowding/rotation/regime）。
3. **「市場」群混內容與部位**：daily/weekly 內容（briefing 已暫停仍掛第一位/weekly/earnings/catalyst）＋參考儀表（Markets/Sectors）＋部位狀態頁（long-track×2/turtle-sleeve）。
4. **首頁文案過期**：hero 副標第一句仍是「量化系統回測 · 每日市場簡報」（briefing 已暫停）；精選清單 CTA 寫「兩組收斂輸出」（現為三組，十倍軌 07-05 上線）；stats 數字（34+ 深度研究/245+ DD）待校。

## 1. 新分群設計（依使用意圖：今天我來做什麼）

> 原則：**選股一個選單全包**（直接治「散落」）；研究＝深度報告庫；市場＝市場狀態與行事曆；系統＝部位軌與量化底層。

### nav v2：首頁 ｜ 選股▾ ｜ 研究▾ ｜ 市場▾ ｜ 系統▾ ｜ 🧠 心智模型 ｜ 📘 使用說明

**選股▾（10 項，全站選股唯一入口群）**
| 項 | 現在住哪 |
|---|---|
| 選股駕駛艙（總入口） | 研究▾ |
| 精選清單 | 研究▾ |
| 🧭 Pipeline 漏斗 | （nav 無，只在 dd-screener subnav） |
| DD Screener 主表 | 工具▾ |
| ⚙ 決策引擎 | 工具▾ |
| Momentum-5 | 研究▾ |
| QGM 美股 / QGM 台股 | 工具▾ |
| RS+VCP 美/台/日/馬 | 工具▾（4 項；依 D4 可收成 1 項小 hub） |

**研究▾（6 項，深度報告庫）**：個股 DD ／ 期望落差綜合研判 ／ 多股對比 ／ 產業深度 ID ／ 🎯 Tier Matrix ／ 供應鏈地圖

**市場▾（8-9 項，市場狀態與行事曆）**：財報分析 ／ 催化劑日曆 ／ Markets ／ Sectors ／ 擁擠交易監測 ／ 產業輪動 ／ 大類資產 regime ／ 週報 ／（每日簡報——已暫停，依 D3 移除或標註）
— 跨資產三頁從「研究」移來：它們是市場狀態描述器（與首頁風險儀表同家族），意圖上屬「看市場」不屬「讀報告」。

**系統▾（6 項，部位軌與量化底層）**：長線訊號 SMH ／ 台股長線 ／ 商品 Sleeve ／ 量化回測 ／ 期貨部位計算機 ／ 🗄 Data Cache

計數：10＋6＋9＋6＝31 目的地、四群意圖分明，選股從跨兩選單 10 目的地收斂為一個選單。

## 2. 首頁改版（同步 nav 分群）

1. **hero 副標改寫**：拿掉「每日市場簡報」（已暫停），改為現行主軸——例：「選股系統 × 個股/產業深度研究 × 市場狀態儀表 ｜ AI 驅動 · 每日更新」；stats 四格重校（DD 數 245+→實數、加「選股三軌」）。
2. **CTA 區改雙卡**：精選清單（THE LIST）＋選股駕駛艙（今天開站看什麼）並列；精選卡文案「兩組」→「三組（長熬×爆發×十倍）」。
3. **風險儀表區不動**（實證裁決已定案，描述器定位）。
4. **features 四欄重排**成新四群（選股/研究/市場/系統），卡片連結與新 nav 一一對應；心智模型欄併入頁尾或保留第五欄（傾向保留——它是獨立心智資產）。

## 3. 執行面與影響半徑

| 動作 | 檔案 | 風險 |
|---|---|---|
| nav 分群改 4 群 | `scripts/site_nav.py`（MENU/GROUP_LABELS/PREFIX_ACTIVE） | 低——單一真相來源 |
| 全站 re-inject | 本 repo 擁有的樹（排除 weekly/briefing/qgm×2/backtest 外部樹） | 低——冪等 |
| **外部 3 repo nav snippet 同步** | v7-backtest `site_nav_snippet.py`；morning-briefing `briefing/site_nav_snippet.py`；minervini-quality-backtest `live/site_nav_block.py` | **中——動外部 repo 是新的 commit/push 範圍（D2）**；不同步則外部樹頁面（backtest/briefing/weekly/qgm）nav 停在舊 3 群，直到各自下次重生 |
| 首頁改版 | `docs/index.html` | 低 |
| 使用說明重排 | `docs/how-to.html`（07-05 剛重寫，內容新；只需依新分群改組標籤與順序） | 低 |
| （D4）RS+VCP 小 hub | 新 `docs/screeners.html`（4 張卡的落地頁）＋4 個 daily cron 不動 | 低 |

不動區：/private/、/pm/（封存）、/report/、feed.xml、robots、各內容頁本體。

## 4. 裁決分岔

| # | 分岔 | 我的建議 |
|---|---|---|
| **D1** | 採用四群 nav（選股/研究/市場/系統）？ | 採用——「選股一個選單全包」直接治本次主訴 |
| **D2** | 外部 3 repo nav snippet 同步（新的 commit/push 範圍）？ | 同步——不同步則四個外部樹的頁面停留舊 nav，整站分群名不符實；三個 repo 各一個小 commit |
| **D3** | 每日簡報（已暫停）nav 去留？ | 自 nav 移除（/briefing/ 歸檔頁仍可達，從週報頁或 sitemap 進）；若日後復刊再加回 |
| **D4** | RS+VCP 四項收成一個 /screeners.html 小 hub？ | 收——選股▾ 從 13 項瘦到 10 項；hub 是 4 張卡的靜態落地頁，零管線 |

## 5. 執行順序（裁決後）

1. site_nav.py 四群改版＋PREFIX_ACTIVE 重映射＋（D4）screeners hub 頁
2. 本 repo 樹 re-inject（排除外部樹）
3. 首頁 hero/CTA/features 改版＋how-to 分群標籤同步
4. （D2 通過）外部 3 repo snippet 各一 commit——**動手前逐一向持有人回報**
5. memory 更新；全程比照 parallel-session git hygiene 四步
