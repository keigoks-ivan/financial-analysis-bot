# earnings-synthesis — review-gates.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-16 v1.3 結構拆分，內容自 v1.2 原文搬移、語意零變更）。收錄三道 review gate 的逐條 checklist 細則：Step 4.5 寫稿前 self-review、Step 5.5 寫稿後 sanity check、Step 8.5 發布後反思。必讀時點見 SKILL.md 條件載入路由表。

## Step 4.5 — Self-Review Gate（反思 / write-time critic）

**v1.1 新增、強制執行**。Step 4 完成 web augmentation 之後、Step 5 開寫 HTML 之前，必須對手上的 in-memory 數據做 5 軸 sanity check。**這個 step 沒過就不准開寫**。

### 4.5.A. Ticker Completeness Sweep（重點）

對本期 window 內 US top-20 mkt cap 公司逐一 confirm 是否覆蓋：

```
top_20_mkt_cap = [NVDA, MSFT, AAPL, AMZN, GOOGL, META, TSLA, BRK.B, 
                  JPM, V, MA, LLY, ORCL, UNH, XOM, JNJ, WMT, PG, HD, BAC]
```

對每一檔：
1. 確認該公司 earnings date 是否落在 window 內
2. 如是，確認是否在 `local_reports[]` 任一份的 tickers 名單中
3. 如不在，且不在 `web_filled_companies[]`，則**必須補回**（走 Step 0.5.2.5 day-內盲點流程，light webfetch）

**這條最容易漏的是 day-內盲點**：本地某日報告涵蓋了 N 家，但**該日另有 mega-cap 報 earnings 沒被收進去**（典型例：NVDA AMC 在當日本地報告主場已存其他 retail 公司時被遺漏）。Top-20 級別的 ticker 必須補回。

### 4.5.B. 未來日期 Fact-Check（防 hallucinate）

掃過 `web_filled_companies[]` 與你在 Step 4 抓到的 catalyst / event dates，並準備寫進 §7 Watchlist 的「earnings ahead」名單前：

- **任何「earnings ahead」日期都必須有對應的 source URL**（earnings whisper / company IR / WallStreetHorizon / TipRanks earning calendar 等）。
- 不可由模型自由生成 date（例如「~5/30 NVDA Q2」這種就是 hallucinate — NVDA Q2 FY27 真實日期是 8/26，模型不應自由填空）。
- **NVDA 行事曆**：Feb / May / Aug / Nov（fiscal quarter ends April/Jul/Oct/Jan）。若不確定，WebSearch `"NVDA next earnings date"` 確認。
- 其他常被誤判的：AAPL（Jan/Apr/Jul/Oct）、AMZN（Jan/Apr/Jul/Oct/月底）、MSFT（Jan/Apr/Jul/Oct/月底）。
- 如連 WebSearch 都查不到精確日期，就**用含糊但安全的表述**（如「Q2 FY27 預期 ~8 月底」）而非具體編日期。

### 4.5.C. Source Provenance Check

對每條 §3 trend 主訊號裡會出現的數字（%, $, +XX% YoY），確認該數字能在：
1. 本地 `local_reports[].sections.sec2-sec5` 找到原始引用，或
2. `web_filled_companies[]` 的 `thesis_one_liner` / 對應 source URL 找到，或
3. Step 4 web augmentation 抓回的 source quote 裡找到

如有任何數字「印象記憶」但找不到 source，**移除或改成定性敘述**（如「+8x 訂單」→「訂單顯著加速」），不可保留精確數字。

### 4.5.D. 本地 vs Web 標籤完整性

確認 in-memory 結構裡每個 ticker 都有正確 provenance flag：
- 本地深度料 → `<span class="source-local">` 將在 HTML 出現
- Web 補料（缺失日 + day-內盲點）→ `<span class="source-webfill">` 將在 HTML 出現

§6 ADD/CUT 名單原則上**只用本地深度料**。Web 補料公司原則上在 §6 confidence-note 提及為 confirm-only — 但**唯一例外是 top-5 mkt cap 的 day-內盲點 webfill**（例：NVDA / MSFT / AAPL 等級），可破例入主 ADD/CUT 但必須在 confidence 欄標「業務 High / 短期 entry Medium」並附 caveat 段。

### 4.5.E. 跨章節一致性 Plan

寫 HTML 之前，先草擬：
- §0 TL;DR 5 條 → 每條必須在 §3 對應 trend block 展開
- §6 ADD/CUT/HOLD 每個 ticker → 必須在 §4 對應產業段有業務敘述背景
- §7 Watchlist catalysts → 必須與 §3 trends 有 logical link（不可空降不相關的 event）

如發現任一條 violate，回 Step 3-4 補資料，不要硬寫。

---

## Step 5.5 — Post-Write Sanity Check（v1.1 新增）

HTML 寫完、commit 前，跑下列 grep 自我驗證。任一條 fail 就回頭修。

### 5.5.A. 結構基本盤

```bash
python3 -c "
import re
with open('docs/earnings/synthesis_{YYYY-MM-DD}.html') as f: s = f.read()
print('size:', len(s), 'chars')
print('sections H2:', len(re.findall(r'<h2 id=\"sec', s)))   # 應為 8
print('trend blocks:', len(re.findall(r'class=\"trend-block\"', s)))   # 應 5-7
print('source-local refs:', len(re.findall(r'class=\"source-local\"', s)))   # 應 ≥ 50
print('source-webfill refs:', len(re.findall(r'class=\"source-webfill\"', s)))   # 應 ≥ web-fill ticker 數 × 2
print('add/cut/hold tags:', len(re.findall(r'class=\"tag-(add|cut|hold)\"', s)))
print('external URLs:', len(re.findall(r'href=\"https?://', s)))   # 應 ≥ 12 (2 per trend × 6 trends)
"
```

Gate：size ≥ 60KB；H2 = 8；trends 5-7；external URLs ≥ 12。

### 5.5.B. 未來日期反查

對 §7 watchlist 表格的每個 `<td>` 含日期，grep 確認該日期出自 Step 4.5.B 通過過的 source URL。**任何 `YYYY-MM-DD` 或 `M/DD` 格式的具體日期，如不能對應到一個 source URL，必須改為含糊表述**。

特別檢查：
- `~5/30` / `5月底` 這類「month-end」guess → 必須 source confirm
- 「NVDA Q2 / AAPL Q3」這類 fiscal quarter → 必須對應到真實財報日（NVDA fiscal Q2 = 8/26、Q3 = 11月底 等）

### 5.5.C. Top-20 mkt cap 覆蓋反查

```bash
for t in NVDA MSFT AAPL AMZN GOOGL META TSLA JPM V MA LLY ORCL UNH XOM JNJ WMT PG HD BAC; do
  if grep -q "$t" docs/earnings/synthesis_{YYYY-MM-DD}.html; then
    echo "$t ✓"
  else
    echo "$t ✗ MISSING"
  fi
done
```

如該公司有在 window 內 report earnings 但 grep 不到 → 回 Step 4.5.A 補回。
如該公司沒在 window 內 report（如 LLY 4 月已報過、AAPL 4/30 已在 4/30 local） → 確認本身 ticker 至少在 §2 行業地圖或 §6 holdwatch 中出現一次。

### 5.5.D. 本地 / Web 分色標籤一致

確認每個 web-filled ticker 的所有出現都帶 `<span class="source-webfill">`。

```bash
# webfill ticker 應該出現在以下 3 個地方都有 webfill tag：
# §1 fill-gap table, §2 industry map, §3 trend block (confirm webfill list), §6 confidence-note
```

### 5.5.E. 跨章節一致 final check

讀 §0 TL;DR 5 條，對每條找 §3 對應 trend block 確認 narrative 一致。讀 §6 ADD 名單，對每個 ticker 找 §4 對應產業段確認業務敘述背景。讀 §7 watchlist，對每個 catalyst 找 §3 對應 trend 確認 logical link。

---

## Step 8.5 — Reflective Review（反思 / post-publish critic, v1.1 新增）

commit & push 之後、Step 8 回報用戶之前，跑 **inline 自我反思**。讀自己剛寫的 HTML 全文，對下列五題用 contrarian 角度回答：

### 8.5.A. 「如果這次 synthesis 有大錯，最可能錯在哪？」

從用戶角度想：「我點開這份 HTML，第一個會挑剔的是什麼？」常見錯誤類型：
- **遺漏關鍵 ticker**：top-20 mkt cap 公司在 window 內報了 earnings 但沒被覆蓋（NVDA day-內盲點是 v1.0 翻車的真實案例）
- **虛構未來日期**：§7 catalyst calendar 寫了「~5/30 NVDA Q2」這類 hallucinate
- **Trend 主訊號數字找不到 source**：印象記憶寫的 +XX% 但 grep 不到原始引用
- **§6 add 名單沒有業務背景**：§4 對應產業段找不到敘述支撐
- **§0 TL;DR 與 §3 trends 編號不一致**

### 8.5.B. 「我的 ADD 名單反向想：如果其中 3 檔是錯的，可能的理由是什麼？」

對 §6 ADD 名單每檔，問自己：
- 業務動能是否真的可持續 4-8 季？還是只是 cyclical bounce？
- 估值（NTM P/E vs 5Y avg）已經 priced in 多少 thesis？
- 同產業同主題的其他名稱有沒有可能反而是更乾淨的 add？

如有任一檔通不過這個反向 test，移到 HOLD/WATCH。

### 8.5.C. 「Web 補料公司的 confidence flag 是否誠實？」

對每個 web-filled ticker，確認：
- §1 fill-gap 表 source URL 真的能驗證關鍵數字（不是泛泛 calendar 頁）
- §3 trend confirm list 有明確區分本地 vs webfill
- §6 confidence-note 真的有點明「web 補料不入主 add/cut」

### 8.5.D. 「§7 Watchlist 的每個 catalyst 都有真實 source 嗎？」

特別檢查日期 — 用 contrarian 心態假設「這個日期是我亂編的」，去找 source 反證。如找不到精確 source，立即改為含糊表述。

### 8.5.E. 「最重要：我有沒有過度自信？」

讀 §0 TL;DR — 5 條 conviction shift 是否有任何一條是「我覺得這樣比較簡潔好讀」而非「實際 trend 浮現」？如有，改寫成更謙遜的措辭（如「初步觀察」「需 H2 驗證」）。

**如 8.5.A-E 任一條發現問題**：
- 小錯（cosmetic / 措辭）→ 直接 patch HTML，commit 一次 `fix(synthesis): self-review 反思 patch`
- 大錯（漏 ticker / 虛構日期 / trend 無證據）→ 必須通知用戶承認失誤 + 給修補 plan，**不可悄悄改**
