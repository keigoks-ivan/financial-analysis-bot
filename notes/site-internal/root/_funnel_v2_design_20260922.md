# FunnelRank v2 逐層法設計稿（2026-09-22）

持有人拍板：不做影子並行、不等 10 月校準，直接換掉 dd-screener 主排序鍵。v1（加權合成分）退場，欄位保留一版供對照。

## 1. 動機——v1 加權合成分丟掉了三件事

v1 的三層（財務品質分 × 護城河分 × 上修動能分）用固定權重 0.40/0.30/0.30 合成單一 0–1 分數，實際跑起來有三個具體毛病，抓自現行 `latest.json`（2026-09-19 快照，339 檔）：

1. **上修動能分只看方向，不看幅度**。FY1/FY2/FY3 每欄只映射成 +1／0／−1 三個值，一家上修 0.6% 跟上修 16% 拿一樣的分。結果 213/339（62.8%）的上修動能分卡在中性值 0.50——92 檔是真的沒有對照基準，另外 121 檔是三欄訊號互相抵消或幅度太小過門檻，兩種情況合起來讓超過六成的名字在這一層完全沒有鑑別力。
2. **護城河資料 87/339（25.7%）缺值**，一律退回 0.50 中性分，等於「不知道」跟「普通」拿一樣的分數，而且缺值比例本身沒有分層——一檔連 DD 都沒有的名字，跟一檔有 DD 但護城河分數剛好沒填的名字，待遇相同。
3. **沒用到 2026-09-16 之後新接的機械層**：ROIC 分解（`incremental_roic_pct`／`implied_growth_pct`）、財報後上修（`eps_rev_since_earnings_pct`）、估值反向欄（`pe_vs_5y_x`／`target_upside_pct`）——這些欄位在 dd-screener 裡都算好了，但 v1 的三層合成公式完全沒有引用，排序鍵跟主表其他機械欄位脫節。

v2 改用四層側寫＋逐層排序法：每層是一個獨立的百分位分數，缺層就是缺層（null），不拿 0.50 打馬虎眼；排序時先比最弱的品質層再比最弱的引擎層，而不是把三個異質分數加權平均成一個數字互相稀釋。護城河不進這四層，見第 5 節。

## 2. 四層定義

四層（事業品質／再投資引擎／期望落差／價格）＝該股票在**全部 stocks**（本次建置的完整母體，目前 339 檔）裡的名次百分位，0–100，越高越好。層內有多個欄位時，先把每個欄位在母體裡做百分位排名（缺值的股票不參與該欄位的排名），再取該股票「有值的那些欄位百分位」的平均——不是拿原始值加總。

### 2.1 護城河——不是一層（2026-09-22 最終定案）

護城河不在這四層之內。護城河是判斷不是可排序的分數，`compute_funnel_v2()` 不讀、不算、也不輸出任何 `moat_*` 欄位。同日曾經歷三版設計（三來源鏈換算百分位、單一來源絕對分層＋過渡開關、純顯示連結），沿革與最終定案見第 5 節。

### 2.2 事業品質 `quality`

四個欄位各自百分位後取平均：`roic_5y_avg_pct`、`fcf`（FCF 利潤率）、`fcf_ni_ratio`、`fund.ni_margin_ltm_pct`。

**2026-09-23 修正——`fcf_ni_ratio` 進這一層前先封頂 `FUNNEL_V2_FCF_NI_CAP=0.8`（懲罰過低，不獎勵過高）**：原始實作沒封頂，讓 GAAP 淨利被 SBC／一次性費用壓得很小的名字（CRWD 35.9、PANW 13.4、MDB 11.2）單靠這一項就幾乎穩拿滿分，但那反映的是淨利分母失真，不是品質真的更好。封頂後 `min(fcf_ni_ratio, 0.8)`：≥0.8 一律打平（「現金轉換沒問題」，不用再比誰換得更誇張），低於 0.8 才繼續按原始值排序、越低分越差。只影響這一層的百分位輸入，不動原始 `fcf_ni_ratio` 欄位輸出，也不動既有 veto 判準（<0.7 fail、decline signal <0.75 兩處仍讀未封頂的原始值）。

### 2.3 再投資引擎 `engine`

三個欄位：`implied_growth_pct`、`incremental_roic_pct`、`eps_fy1_fy3_cagr_pct`。`incremental_roic_pct` 若 `incremental_roic_clamped=true`（增量 ROIC 被 [-200%, 500%] 極端值夾住，數字是防呆哨兵不是真實速率）或 `incremental_roic_note=="資本縮減"`（分母萎縮，比率沒有意義），該欄位視為缺值，不進這一層的平均。

### 2.4 期望落差 `gap`

三個欄位：`eps_rev_3m_pct`、`eps_rev_since_earnings_pct`、`implied_growth_pct − fund.est_eps_cagr_3y_pct`（機械算出的內生成長天花板減共識三年 CAGR；兩者任一缺值則這個衍生欄位本身視為缺值）。

### 2.5 價格 `price`（反向層——越便宜排名越高）

三個欄位，`pe_vs_5y_x`、`live_peg` 兩個反向（原始值越低，百分位越高），`target_upside_pct` 正向（原始值越高，百分位越高）。

**2026-09-23 修正——拿掉 `pct_5y`**：原設計把 `pct_5y` 也放進這一層（反向計分），但這個欄位是寫 DD 那份報告當時從報告裡抄過來的數字，寫完就凍結不再更新（stale），而且全部 87 檔非 DD 個股完全沒有這個欄位可抄。價格層改成上述三個欄位。`pct_5y` 本身仍照算輸出（供其他頁面如 quality-entry screener 用），只是不再進 FunnelRank v2 這一層的百分位平均。

**2026-09-23 新增——`target_upside_pct` 的 yfinance 備援**：Koyfin 匯出對一部分名字是分裂的——例如 TSM（ADR）有 `fund.last_price_local` 卻沒有 `fund.target_avg`，2330.TW 剛好相反，兩邊湊不出同一支股票的分子分母，`target_upside_pct` 只能是 null（連帶這 20 檔：TSM、2330.TW、ASML、RACE、BHP、VALE、RIO、CLS、2327.TW、2383.TW、2345.TW、2368.TW、2308.TW、2317.TW、ESLT、MGA、TD、STM、BMO、ABB）。Koyfin 算不出來時改讀 yfinance `Ticker.info` 的 `targetMeanPrice` 與 `currentPrice`（缺則退 `regularMarketPrice`）——同一次 API 呼叫、同一個報價來源、同一種貨幣，比例才有效。新欄位 `target_upside_source`（`"koyfin"` / `"yfinance"` / `null`）記錄實際來源；只在 Koyfin 那條路徑失敗時才會多打一次 yfinance，不是每檔都打。實作：`scripts/build_dd_screener.py` 的 `_target_upside_yfinance_fallback()`，在 `enrich_ticker()` 裡呼叫，`compute_fundamental_gates()` 本身維持零網路的 pure 函式不變。

## 3. 排序法——逐層比較，不加權合成，最弱層先比（leximin）

品質／引擎／落差／價格四層各自百分位切五分位 tier：`[80,100]→4`、`[60,80)→3`、`[40,60)→2`、`[20,40)→1`、`[0,20)→0`；缺值 → tier `-1`。

**2026-09-23 修正——排序法改成「最弱層先比」，本節取代舊文字**：舊版文字寫「排序鍵＝`(quality_tier, engine_tier, gap_tier, price_tier)` 由大到小逐層比——先比品質 tier，品質 tier 相同再比引擎 tier」，這其實是固定順序比較，跟本節開頭與站上文案一貫講的「先比最弱的那個面向」自相矛盾——程式當時就是照這段文字直接實作成固定順序，於是品質一層獨力決定了大半的名次（品質 tier 一旦分出高下，後面三層根本比不到）。正確做法（leximin）：

1. 取四個 tier，缺值（`-1`）視為中性值 `FUNNEL_V2_MISSING_TIER_AS=2`（不獎不罰——不是最差的 0，也不是最好的 4，避免「剛好缺一層資料」的股票被系統性推到最前或最後）。
2. 把這四個數字由小到大排序，得到「最弱層 → 次弱層 → 次強層 → 最強層」的一個序列。
3. 兩檔股票比較時，先比各自的最弱層——數字大的贏；打平再比次弱層；以此類推比到最強層。
4. 四層（用上述排序後的序列比較）完全打平，才比 `funnel_v2_median`（四層百分位、忽略缺值層的中位數，數字大的贏）；再打平比 ticker 字母序。

這樣做的理由：加權合成分／固定順序比較都會讓「某一層頂尖但另一層墊底」在某些情況下贏過「四層都普通」，但一檔股票的下檔風險通常就卡在它最弱的那一層——leximin 讓最弱層先決定排序，真正頂尖的名字不會被另一項墊底的指標拖累到看起來比「四層都普通」的名字還差，也不會反過來讓一層墊底被另一層頂尖蓋過去。護城河不在這四層之內——原因與沿革見第 5 節。實作：`scripts/build_dd_screener.py` 的 `_sort_tuple()`（`compute_funnel_v2()` 內部）。

輸出欄位：`funnel_v2_rank`（1..N 名次，整數）、`funnel_v2_tiers`（四個 tier 的陣列，品質→引擎→落差→價格順序）、`funnel_v2_profile`（四個值，同順序，皆 0–100 百分位，可為 null）、`funnel_v2_median`（四層百分位的中位數，忽略 null）、`funnel_v2_top_tier_count`（四層裡 tier=4 的層數）。

### 3.1 資料不足門檻

四層裡至少要有 3 層 tier 非 `-1` 才排名。少於 3 層 → `funnel_v2_rank=null`、`funnel_v2_note="資料不足（N/4 層）"`（N＝實際有效的層數），該列跟被否決的列一樣沉底，但 `funnel_v2_veto` 留空——資料不足和否決是兩件不同的事，前端與下游應分開判讀。

## 4. 硬否決——沿用 v1 既有旗標，不新增判準

命中任一即 `funnel_v2_rank=null`、`funnel_v2_veto` 記錄命中的旗標（陣列，可能不只一個）、整列沉底：

- `quality_veto_level == "拒絕"`（體質五項機械閘 4-5 項不合格）
- `decline_signal_light == "⛔"`（衰退訊號六項機械指標命中 ≥5 項）
- `veto_all_downgrade == true`（FY1/FY2/FY3 三欄全部下修，v1 既有欄位）

這三個判準在 v1 就已經是「歸零沉底」的處置（見 `compute_funnel_rank()` 文件字串），v2 原樣沿用判準本身，只是換了一個載體（v1 是分數歸零，v2 是名次設 null）。

**v1 的另外兩個處置本版停用**：`funnel_cap_moat_down`（護城河 ↓ 且非四條件全過 → 分數封頂 0.50）與 `funnel_cap_quality` 的「降一級 → 封頂 0.60」這一格（「拒絕 → 封頂 0.30」併入上面的硬否決，因為它已經跟 `quality_veto_level=="拒絕"` 是同一個判準）。這兩個封頂在 v1 是「拿護城河/品質的弱點去壓總分」的做法，v2 底下護城河與品質已經是各自獨立的層，一旦真的轉弱，會直接反映在對應那一層的 tier 上被排到後面，不需要再用封頂去人工模擬同樣的效果——重複做同一件事的兩種機制沒有必要並存。降一級的封頂在 v1 分數體系裡本來就比拒絕輕微，這裡也一併退場而非只降一半。這兩條列入下方 rule_ledger 候刪名單，本次直接停用（不再是提名審查、是實際不用）。

`quality_cap_overridden_by_revision`（上修覆蓋封頂）這個 v1 判準本身依附在「封頂」這個機制上，封頂機制既然停用，這個覆蓋規則在 v2 的執行路徑上沒有對象可覆蓋，同樣不搬進 v2；v1 legacy 欄位不動，仍照算保留。

## 5. 護城河——最終不進 FunnelRank v2（2026-09-22 同日三度定案，本節取代此前所有草案）

**一句話沿革**：護城河當天先後寫過三版設計——三條來源鏈換算百分位、單一來源絕對分層＋過渡開關、後來的純顯示連結（`moat_questions_url`/`moat_review_due`）——持有人最終拍板護城河是判斷不是可排序的分數，三版全部刪除，FunnelRank v2 只剩四層，不再有任何護城河顯示欄位。

`compute_funnel_v2()` 不讀、不算、也不輸出任何 `moat_*` 欄位（`_load_moat_v2_judgment()`／`_moat_v2_absolute_tier()`／`_load_moat_v2_display()`／`FUNNEL_V2_MOAT_JUDGMENT_ENABLED`／`FUNNEL_V2_MOAT_DIR` 皆已從 `scripts/build_dd_screener.py` 刪除），`FUNNEL_V2_LAYER_ORDER` 固定四個成員 `("quality", "engine", "gap", "price")`。想看一檔的護城河判斷，讀者自己到個股儀表板（`/stock-dash/?t={T}`，`scripts/build_stock_dash.py` 另一條獨立產線，已上線）——dd-screener 每列名次格改提供一個「儀表板」小連結，純粹是站內導覽，不經 `latest.json` 傳遞任何護城河資料、也不影響排序或中位數 tie-break。

v1 legacy 的 `moat_score`／`moat_grade`／`moat_trend`／`moat_score_adj`（`funnel_rank` 舊制的一部分，見 §4 與上方 §1）不受本節影響，仍照算保留一版供對照，下一版才移除。

## 6. 與席位引擎／sop-funnel 的邊界

FunnelRank（v1 與 v2 皆然）只回答「先看誰」，不回答「買不買」與「何時買」——這是 2026-07-11 持有人拍板的聚合層使用邊界（CLAUDE.md「聚合層名單的使用邊界」條）：站上各聚合層對同一個名字的態度可以不一致，這是職能分工，最終「值不值得投資」一律走 DD 統一裁決（`#decision`）→ 決策三錨（critic × 帳本 × usernote）→ sop-funnel 板機，不歸任何排序頁。

v2 換掉的是 dd-screener 主表「先看誰」這一個排序鍵本身，不動：

- **席位引擎**（`scripts/engine/grp.py` 的 v5 品質派 × 上修排序）——它有自己的資格閘與排序鍵（上修動能單一變數），完全不讀 `funnel_rank`／`funnel_v2_rank`，這次不碰。
- **sop-funnel 板機**——時機層獨立於本分數，護城河 veto（grade∉{C,X} 且 trend≠↓）在 `sop_funnel.engine.quality_check` 另外把守，這次不碰。
- **DD 統一裁決**——`dca_verdict`／`#decision` 才是「買不買」的權威來源，FunnelRank 任何版本都不覆蓋它。

## 7. 驗證方式

本次上線前的驗證：

- `python3 scripts/build_dd_screener.py`（既有 xlsx／快取跑一次全量建置）+ `pytest scripts/tests/`，確認 v1 既有測試（`test_funnel_caps.py`）不受影響、v2 新測試通過。
- 前 20 名對照 NVDA／TSM／AMD 三檔名次，與主 session 先前用另一套護城河只取 DD 分數的方法（下稱 C 法）算出的排名做比較（C 法前 10：MA、HLT、NVDA、6857.T、ASML、LRCX、ADI、KLAC、2330.TW、TSM；NVDA 第 3、TSM 第 10、AMD 第 115）——若落差大，在下方交付紀錄逐檔說明原因（多半是 moat 來源鏈或資料完整度差異，非方法論本身有誤）。

**下一輪校準要做、本次不做（TODO）**：v2 前 20 名凍結進 `knowledge/` 帳本、追蹤 91 天後的超額報酬勝率，跟 v1 legacy 前 20 名做同尺對照——這是下方 rule_ledger kill condition 的資料來源，需要接 `knowledge/ledger_from_editorial.py` 或類似機制產生快照，本次只把 kill condition 寫清楚，接線留到 2026-10 校準輪。

## 8. Rule ledger 新增列（見 `knowledge/rule_ledger.md`）

登記「FunnelRank v2 逐層法」一列，kill condition：2026-10 校準輪起，v2 前 20 名 91 天內超額報酬勝率若連兩輪低於 v1 legacy 前 20 名 ≥5pp → 回退 v1 或改層序。同批候刪提名（本次已實際停用，非僅提名審查）：v1 的 moat-down cap（`FUNNEL_MOAT_DOWN_CAP`／`funnel_cap_moat_down`）與 quality 降一級 cap（`FUNNEL_QUALITY_DOWNGRADE_CAP`／`funnel_cap_quality` 的降一級分支）。
