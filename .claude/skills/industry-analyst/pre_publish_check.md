# industry-analyst v2.5 — Pre-Publish Gate Check（13 Gates）

每份 v2.x 產業深度報告（ID）發布前必跑。寫好 HTML 草稿後（Step 8.5），讀取本檔逐條檢查，產出 `pre_publish_report.md`。

Gate 編號與 `SKILL.md`【Pre-Publish Gate（13 道）】表完全一致：

| Gate | 性質 | 檢查 | 來源 |
|:---|:---|:---|:---|
| **Gate 1** | 阻斷 | 核心 ticker financials < 60 天 | ID v1.x Gate 1 原文 |
| **Gate 2** | 阻斷 | Event-triggered thesis < 14 天 refresh | ID v1.x Gate 2 原文 |
| **Gate 2.1** | 阻斷 | Thesis Cornerstone Fact 驗證（獨家/首家/唯一） | ID v1.x Gate 2.1 原文 |
| **Gate 3** | 阻斷 | Cross-ID reconciliation | ID v1.x Gate 3 原文 |
| **Gate 4** | 阻斷 | id-meta JSON validate（原 ID Gate 8） | ID v1.x Gate 8 |
| **Gate 5** | 阻斷 | §0 PM Implication 綠卡（原 ID Gate 9） | ID v1.x Gate 9 |
| **Gate 6** | 阻斷 | 文字比 ≥ 55% + 表格 ≤10 張 / ≤8 行（§9 ≤16） | DS Gate 11 + Gate 10 碼，門檻 80%→55% |
| **Gate 7** | 阻斷 | 推導鏈 regex（掃 §4/§5/§7/§8/§9） | DS Gate 13 碼 |
| **Gate 8** | 阻斷 | aside 來源 + T1 占比 ≥ 60% | DS Gate 12 碼，門檻 50%→60% |
| **Gate 9** | 阻斷 | §1 錨點（日期 + 量化） | DS Gate 14/DS-9 對應碼 |
| **Gate 10** | warning | 供需裁決三選一 + §9 depth 時間限定 + catalyst 雙路徑 + 原 ID warning gates 摘要 | 新（DS Gate 7 + Gate 14 + ID 3.1/5/6/7 摘要） |
| **Gate 11** | 阻斷 | dual-output 完整性（canonical + `_full.html` 皆存在、marker + id-meta 各就位） | v2.5 新 |
| **Gate 12** | 阻斷 | kill_metrics 同步（id-meta `kill_metrics[]` ≥3 對齊 §8；sd_verdict/clock_phase/conviction 一致 §0/§5） | v2.5 新 |
| **Gate 13** | warning | purity 推導（§9 每檔 `purity_pct` 有 segment 營收推導行） | v2.5 新 |

任一阻斷 Gate（1/2/2.1/3/4/5/6/7/8/9/11/12）fail → **阻斷發布** + 列修正項。阻斷全過、warning Gate（10/13）fail → 允許發布但輸出 warning。

> 下方所有出現 `docs/id/ID_{Theme}_{Date}.html` 的 path 在實跑時替換為實際檔案路徑（草稿階段可能在 staging path）。

---

## Gate 1 [必備 / 阻斷]｜Core Ticker Financials Refresh（< 60 天）

**規則**：所有 🔴 核心 ticker 的最新公告季度財報必須在發布日前 60 天內。

**檢查步驟**：
1. 列出 §9 所有 🔴 核心 ticker
2. 對每檔 → 查最近公告的 quarterly earnings release 日期
3. 若 `(發布日 - earnings 日) > 60 天`：
   - **阻斷發布**
   - 列出該 ticker 名稱 + 需查的最新季 + 預期公告日

**典型 fail 情境**：
- 報告發布 4/19，ticker Q 結束 3/18（30 天前已公告）但 skill 仍用 Q1 舊數據
- 報告引用「Q × 4」推估而非最新 actual

---

## Gate 2 [必備 / 阻斷]｜Event-Triggered Thesis Refresh（< 14 天）

**規則**：§7 Non-Consensus thesis 引用的事件性 data point，必須在發布日前 14 天內重新檢索最新狀態。

**事件性 data point 定義**：
- 具體 yield 數字（"Samsung SF2P 70% yield"）
- 具體訂單 / 簽約（"Intel 18A 無外部客戶"）
- backlog 絕對值（"GEV $135B backlog"）
- 併購 / 股權狀態（"AMAT 併 BESI 傳聞"）
- 產能 sold out / 量產時序（"Samsung HBM4 Feb 2026 量產"）

**檢查步驟**：
1. 掃 §7 三條 thesis 的「分歧事實」與「證偽條件」段落
2. 標註每條為 `[event-triggered]` 或 `[structural]`
3. 對 event-triggered → WebSearch 最近 14 天是否有更新
4. 若最新資料矛盾：
   - 降信心級別（高 → 中、中 → 低）
   - 或直接重寫 thesis
   - 若時間不夠重寫 → **阻斷發布**

**典型 fail 情境**：
- LEN ID 引用 Samsung SF2P 70%（1 月舊報導），但 4/14 TrendForce 已更新為 SF2 55%
- AP ID 寫「AMAT/LRCX 併 BESI 傳聞」，但 AMAT 2025-04 已持股 9%

---

## Gate 2.1 [必備 / 阻斷]｜Thesis Cornerstone Fact Verification

**規則**：§7 每條 thesis 的「核心分歧事實」必須獨立 WebSearch 最新狀態，特別針對含有「獨家」「首家」「唯一」「only」等定性的 claim 逐一驗證。

**為何存在**：
ID_Transformers v1.4 發生的「Eaton 800V DC 獨家 co-design」錯誤是典型案例 — Gate 2 確實檢查了 Eaton Beam Rubin DSX 公告 14 天內正確，但未驗證「是否真的獨家」這個 thesis 基石 claim。實際狀況：NVDA MGX 800V DC 官方 14+ 家夥伴（ABB、Delta、Schneider、Vertiv 等），Eaton 是 top 3 而非獨家。此類錯誤不是 data 過期，是 cornerstone 定性從未被獨立驗證。

**檢查步驟**：
1. 掃 §7 每條 thesis，圈出所有含「獨家」「首家」「唯一」「only」「first」「exclusive」「sole」「lock-in」「壟斷」等詞的 claim
2. 對每條 → 獨立 WebSearch：
   - `"{相關技術或事件}" partners list` 或
   - `"{相關技術或事件}" ecosystem OR alliance OR consortium`
   - 確認「除了該公司，還有誰也有類似地位」
3. 若發現 ≥ 2 家其他玩家同樣定位：
   - 改寫為「結構性優勢」「top 3 玩家之一」等非獨家措辭
   - 重新評估信心級別（高→中）
   - 重新評估估值敏感度（+5-8x PE → +2-3x）
   - 重新定義證偽條件（原條件若已被其他玩家進入滿足，需改寫）
4. 若 thesis 作者堅持「獨家」定性：
   - 必須在 thesis block 明確列出「被考慮但排除的競爭玩家」+「為何它們不算同級」
   - 無此防禦 → **阻斷發布**

**典型 fail 情境**：
- Transformers ID「Eaton 獨家 co-design NVIDIA 800V DC」— 實際 14+ 家夥伴
- 若未來 SiPho/CPO ID 寫「TSMC COUPE 獨家」但 Intel / Samsung 也在做
- 若未來 Glass ID 寫「LPKF LIDE 唯一」但 NEC / Disco 也有類似技術

**輸出格式**（在 pre_publish_report 內）：
```
## Gate 2.1: Thesis Cornerstone Fact Verification
Thesis 1 cornerstone: "{關鍵 claim}"
  → WebSearch 查 ecosystem 玩家 → {發現結果}
  → 結論：✅ 獨家驗證 / ⚠ 需改寫 / ❌ 阻斷
```

---

## Gate 3 [必備 / 阻斷]｜Cross-ID Reconciliation

**規則**：同批次發布的所有 ID，共用數字、ticker 評級、關鍵事實必須一致。

**需 reconcile 的項目**：
- 共用 ticker 的核心財務數字（NVDA DC Rev、AVGO AI Rev、Credo Rev 等）
- 共用事實（Rubin Ultra stack、AI capex 總和、CoWoS 分配）
- Ticker 評級（🔴/🟡/🟢 在多份 ID 出現必須一致）
- TAM 數字（避免 AI DC ID 和 Liquid Cooling ID 的「液冷 2026 TAM $4-5B vs $6.4B」類似情境）

**檢查步驟**：
1. 掃所有待發布 ID 的 §4 TAM 表 + §3 玩家清單 + §9 關聯個股
2. 對每檔共用 ticker → 列所有 ID 的核心數字
3. 若 inconsistency：
   - 數字差 > 10% → **阻斷發布**
   - 評級不一致 → **阻斷發布**
4. 輸出 reconciliation report 並修正

**典型 fail 情境**：
- 兩份 ID 對同一檔 ticker 給不同評級（LITE 在 Networking ID 是 🟢、在 SiPho 是 🟡）
- 液冷 TAM 在 AI DC 和 Liquid Cooling 數字差 40%

---

## Gate 4 [必備 / 阻斷]｜id-meta JSON 存在且通過 strict 驗證

**規則**：每份 ID HTML 的 `<head>` 內必含 `<script id="id-meta" type="application/json">{...}</script>`，且該 JSON 通過 `scripts/validate_id_meta.py` strict 驗證（必填欄位齊全、enum 值合法、`oneliner` ≤ 200 chars、`related_tickers` 結構正確）。**v2.2 新增**：`skill_version` 為 `v2.x` 時，§0 三句話 `now_state` / `future_state` / `action` 三欄**必填且各 ≤240 chars**（validator 阻斷；legacy v1.x 不受影響）。

**為何阻斷**：
2026-04-27 連 11 份新 ID 漏了 id-meta 區塊，CI `Validate DD + ID metadata` workflow strict gate 全部 fail，使用者收到連續失敗信件。本 Gate 把 id-meta 從「QC 提醒」升格為「阻斷式 publish gate」。

**檢查步驟**：
```bash
python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{Date}.html
```
1. exit code != 0 → **阻斷發布**，列出缺漏 / 違規欄位
2. 常見 fail：
   - 沒有 `<script id="id-meta">` 區塊（漏寫）
   - `oneliner` 超過 200 chars（沒裁切，把 §0 整段塞進去）
   - enum 值用了複合字串（`structural+event` / `mature_diverging` / `oligopoly+disruption`）— 必須改回單一白名單 enum
   - `related_tickers` 為空陣列且非 cross-cutting 主題

**典型 fail 情境**：
- skill 從 html_template 複製骨架但忘記填 id-meta JSON 內容 → block
- backfill 工具產的 oneliner 是 §0 截斷段 → block（length > 200）

**輸出格式**：
```
## Gate 4: id-meta JSON Validation
$ python3 scripts/validate_id_meta.py docs/id/ID_XXX_YYYYMMDD.html
{exit code, errors}
✅ PASS / ❌ FAIL — {缺漏欄位列表}
```

---

## Gate 5 [必備 / 阻斷]｜§0 PM Implication 綠卡存在 + conviction 一致性

**規則**：每份 ID HTML 的 §0 內（決策摘要層）必須存在 `<h2>` 含「Portfolio Implication」及對應的綠色 `judgment-card`（`background:#F0FDF4;border-left:4px solid #16A34A`），且內容必須通過以下一致性查驗。

**為何阻斷**：
§9 conviction tier / §6 de-rating window / §8 falsification metric 這三個判斷層完成後，PM 的行動結論必須在同一文件明文化 — 否則讀者得自己從三個不同章節拼湊，增加誤讀風險。

**檢查步驟**：

1. **存在性查驗**（阻斷）
   - HTML 中搜尋 `Portfolio Implication`（或 §0 內 `judgment-card` 綠卡）
   - 搜尋 `background:#F0FDF4` + `border-left:4px solid #16A34A`
   - 缺任一 → **阻斷發布**：「§0 PM Implication 綠卡 missing」

2. **五 bullet 完整性**（阻斷）
   - 確認存在以下五個 `<strong>` 標籤的 bullet：
     - `thesis 方向`
     - `個股 conviction tier 變化`
     - `關鍵新監測點`
     - `multiple / 估值 / 週期定位風險`（允許近似詞）
     - `Entry 時機`
   - 任一 bullet 缺失 → 阻斷

3. **j-logic 四行動**（阻斷）
   - 確認 `.j-logic` div 存在，且包含 `①`、`②`、`③`、`④` 四個行動符號
   - 缺少任一符號 → 阻斷

4. **conviction pill 一致性**（warning）
   - 讀取 `<span class="j-conf">` 內的 conviction 值（high/mid/low）
   - 對比 §9 🔴 ticker 數量 + §8 falsification 距離：
     - ≥ 2 個 🔴 且 §8 falsification 距離 > 2 sigma → 預期 `high`；若標 `low` → warning
     - 0 個 🔴 → 預期 `low`；若標 `high` → warning
   - Conviction 不一致 → warning（不阻斷，但必須在 report 說明）

5. **ticker 點名查驗**（warning）
   - `個股 conviction tier 變化` bullet 中必須出現至少一個 ticker symbol（大寫英文字母組合，如 NVDA、AVGO、TSMC）
   - 若只寫「部分核心股」「相關個股」等泛語 → warning

**典型 fail 情境**：
- 整份 ID 缺 §0 PM 綠卡（舊格式或未跑 §0 定稿步驟）→ 阻斷
- 綠卡只有 3 條 bullet，漏寫 Entry 時機 → 阻斷
- j-logic 只列 ①②③，沒有 ④ → 阻斷
- conviction 標 `high` 但 §9 無任何 🔴 ticker → warning

**檢查碼（存在性 + 五 bullet + j-logic）**：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
# 1. 綠卡存在
card = bool(re.search(r'#F0FDF4', html)) and bool(re.search(r'border-left:4px solid #16A34A', html))
title = bool(re.search(r'Portfolio Implication', html))
print(f"綠卡存在: {'✅' if (card and title) else '❌ MISSING'}")
# 2. 五 bullet
bullets = ['thesis 方向', '個股 conviction tier 變化', '關鍵新監測點', '估值', 'Entry 時機']
missing = [b for b in bullets if b not in html]
print(f"五 bullet: {'✅ all present' if not missing else '❌ missing: '+str(missing)}")
# 3. j-logic 四行動
acts = [s for s in '①②③④' if s in html]
print(f"j-logic 四行動: {'✅' if len(acts)==4 else '❌ missing: '+''.join(s for s in '①②③④' if s not in html)}")
PY
```

**輸出格式**：
```
## Gate 5: §0 PM Implication Existence + Conviction Consistency
綠卡 exists: ✅ / ❌ MISSING
Five bullets: ✅ all present / ❌ missing: {bullet names}
j-logic 4 actions: ✅ / ❌ missing: {①②③④ which absent}
Conviction consistency: ✅ / ⚠ {explain mismatch}
Ticker name-check: ✅ / ⚠ {no ticker found}
→ Gate 5: ✅ PASS / ❌ BLOCKED / ⚠ WARNED
```

---

## Gate 6 [必備 / 阻斷]｜文字比 ≥ 55% + 表格 ≤ 10 張 / ≤ 8 行（§9 ≤ 16）

**規則**（搬自 DS Gate 11 + Gate 10，門檻 80%→55%、表格上限 4→10）：
- 純文字字元（含 bullet 內容）/ 整篇可見字元 ≥ **55%**（DS 為 80%；v2.0 是 ID 70-80% 表 ↔ DS 80% 文字的中間值）。
- 表格數量 ≤ **10** 張；每張 ≤ **8** 行（不含表頭），**§9 ticker 表例外可至 16 行**；成本曲線 / 庫存指標表視產業屬性可省。

**為何阻斷**：低於 55% 文字 → 退化回舊 ID 表格 dashboard；表格爆量同理。

**Part A — 文字比例 ≥ 55%**（搬自 DS Gate 11 碼，門檻改 0.80 → 0.55）：
```bash
python3 << 'PY'
import re
path = "docs/id/ID_{Theme}_{Date}.html"
html = open(path).read()

# 1. 移除 <script>...</script>、<style>...</style>、<!-- comments -->
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)

# 2. 抓所有 <table>...</table> 區塊
tables = re.findall(r'<table[^>]*>.*?</table>', clean, flags=re.DOTALL)

# 3. 計算純文字總字元（去 HTML tags 後）
text_only = re.sub(r'<[^>]+>', '', clean)
total_chars = len(re.sub(r'\s+', '', text_only))
table_chars_clean = sum(len(re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', t))) for t in tables)

narrative_chars = total_chars - table_chars_clean
ratio = narrative_chars / total_chars if total_chars else 0

print(f"總可見字元: {total_chars:,}")
print(f"  ├─ 敘述字元: {narrative_chars:,} ({ratio:.1%})")
print(f"  └─ 表格字元: {table_chars_clean:,} ({1-ratio:.1%})")
print(f"\n敘述比例: {ratio:.1%}")
print("PASS" if ratio >= 0.55 else "FAIL (目標 ≥ 55%)")
PY
```

**Part B — 表格數 ≤ 10、行數 ≤ 8/張（§9 ≤ 16）**（搬自 DS Gate 10 碼，§11→§9 + cap 4→10）：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
tables = re.findall(r'<table[^>]*>.*?</table>', html, re.DOTALL)
print(f"表格數: {len(tables)}（cap 10）— {'OK' if len(tables) <= 10 else 'FAIL'}")
for i, t in enumerate(tables):
    tbody_m = re.search(r'<tbody>(.*?)</tbody>', t, re.DOTALL)
    tbody = tbody_m.group(1) if tbody_m else t
    rows = len(re.findall(r'<tr', tbody))
    # 判斷是否為 §9 ticker table（含 .id-tickers / .ds-tickers / depth pill）
    is_s9 = 'id-tickers' in t or 'ds-tickers' in t or 'tier-red' in t or 'depth-red' in t
    cap = 16 if is_s9 else 8
    status = 'OK' if rows <= cap else 'FAIL'
    print(f"  表 {i+1}: {rows} 行（cap {cap}）— {status}")
PY
```

**Fail action**：
- 文字 < 55%：把表格資訊轉敘述段落，或補 `.id-implication` 💡 段落 + lede。
- 表格 > 10 張：合併同類表 / 把次要表轉敘述。
- 單表超 8 行（非 §9）：合併 / 取捨。§9 超 16 行 → 把 🟢 邊緣 ticker 拆到表外文字。

---

## Gate 7 [必備 / 阻斷]｜推導鏈 regex（§4/§5/§7/§8/§9）

**規則**（搬自 DS Gate 13，章節對應改為 §4/§5/§7/§8/§9）：以下章節的結論數字必附「推導：」行或等效標記（「→」「換算」「計算」開頭的短行）：
- §4 TAM 三情境（base/bull/bear）+ CAGR + 三角驗證對帳缺口
- §5 三 horizon × 三 case 全部 cell；資本週期指標換算；phase 轉換量化閾值
- §7 估值分位、現價隱含成長假設的 reverse 推算（priced-in）
- §8 kill metric 的閾值換算
- §9 ticker depth 閾值；forward-looking 閾值須註明時間基準 + 當前 actual

**為何阻斷**：source-tag 標「數字來自哪裡」；推導行標「為什麼是這個數字而不是別的」。PM 看不出 bull case +20% 來自哪個 input 變動 → 無法獨立驗證。

**檢查碼**（搬自 DS Gate 13，`required` 改 `[4,5,7,8,9]`，匹配 v2 `<h2>§N` 標題）：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
# Locate each section by <h2>§N
sections = {}
for m in re.finditer(r'<h2[^>]*>§(\d+)\s*[^<]+</h2>(.*?)(?=<h2[^>]*>§|\Z)', html, re.DOTALL):
    sections[int(m.group(1))] = m.group(2)

required = [4, 5, 7, 8, 9]
any_fail = False
for sec in required:
    body = sections.get(sec, '')
    derive_count = len(re.findall(r'推導[：:]', body))
    arrow_count = len(re.findall(r'→', body))
    num_count = len(re.findall(r'\$\d|\d+%|\d+\s?GW|\d+\.\d+\s?倍|\d+\s?x\b', body))
    print(f"§{sec}: 量化數字 {num_count} 處, 推導行 {derive_count} 條, → 箭頭 {arrow_count} 個")
    if num_count > 3 and derive_count == 0 and arrow_count < num_count // 2:
        print(f"  FAIL §{sec}: 結論數字無對應推導行")
        any_fail = True
print("\nGate 7:", "FAIL" if any_fail else "PASS")
PY
```

**Fail action**：在結論數字鄰近段內補一行「推導：input1 + input2 → calc → implication」。例：
- ❌「bull case TAM $340B」
- ✅「bull case TAM $340B（推導：hyperscaler capex $720B × workload mix 35% × accelerator ratio 1.33 → $340B；對比 base $280B 的 +20% 來自 capex 兌現度從 100% 上修至 120%）」

---

## Gate 8 [必備 / 阻斷]｜aside 來源 + T1 占比 ≥ 60%

**規則**（搬自 DS Gate 12，T1 門檻 50%→60%）：
- 每個含量化斷言（%、$、GW、倍數、市占、增長率、TAM、用戶數、capex 等）的 `<section>` 末必有 `<aside class="ds-refs">` 且 ≥ 1 條 `<li>`。
- 全文所有 `.ds-refs` 條目的 T1 + T1-zh 占比 ≥ **60%**。
- 正文中**不應有** `<span class="source-tag">` — 視為遷移未完成的殘留，需清除。

**為何阻斷**：v2.0 來源全部走節末 aside、正文零 inline tag（深入淺出）；同時 ID 嚴謹性要求 T1 ≥ 60%（高於 DS 的 50%）。

**Part A — aside 條目 tier 分佈 + T1 占比 ≥ 60%**（搬自 DS Gate 12 Part A，門檻 0.50→0.60）：
```bash
python3 << 'PY'
import re
from collections import Counter
html = open("docs/id/ID_{Theme}_{Date}.html").read()

tiers = re.findall(r'<span class="tier">\[(T[12]|T3-[ABC]|T1-zh|T2-zh|T3-zh|T3\.5-zh|T4)\]</span>', html)
counts = Counter(tiers)
total = sum(counts.values())
t1 = counts.get('T1', 0) + counts.get('T1-zh', 0)
t1_share = t1 / total if total else 0
print(f"Aside refs total: {total}")
print(f"  T1+T1-zh: {t1} ({t1_share:.1%})")
print(f"  T2+T2-zh: {counts.get('T2',0)+counts.get('T2-zh',0)}")
print(f"  T3-A: {counts.get('T3-A',0)}, T3-B: {counts.get('T3-B',0)}, T3-C: {counts.get('T3-C',0)}, T3-zh: {counts.get('T3-zh',0)}")
print(f"  T4: {counts.get('T4',0)}")
print("PASS" if t1_share >= 0.60 else f"FAIL: T1 share {t1_share:.1%} < 60%")

inline_tags = re.findall(r'<span class="source-tag">', html)
if inline_tags:
    print(f"WARNING: {len(inline_tags)} inline source-tag 殘留 — 需遷移至 aside")
PY
```

**Part B — 每個含量化斷言的 `<section>` 都有 aside**（搬自 DS Gate 12 Part B 原文）：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
quant_pat = re.compile(r'\$\s?\d|\d+(\.\d+)?\s?%|\d+\s?(GW|TW|MW|B|T)|\d+(\.\d+)?\s?(倍|x|×)')
sections = re.finditer(r'<section[^>]*id="(s\d+)"[^>]*>(.*?)</section>', html, re.DOTALL)
missing_aside = []
for m in sections:
    sec_id = m.group(1)
    body = m.group(2)
    has_quant = bool(quant_pat.search(body))
    has_aside = bool(re.search(r'<aside class="ds-refs">', body))
    if has_quant and not has_aside:
        missing_aside.append(sec_id)
if missing_aside:
    print(f"FAIL: 以下節含量化斷言但無 aside: {missing_aside}")
else:
    print("PASS: 所有含量化斷言的節都有 aside")
PY
```

**Fail action**：每節末加 `<aside class="ds-refs">` 列來源（tier + URL + claim summary）。某數字真無 T1 可得 → 用 T2/T3 + 節末加 `<aside class="source-warning">` 警示。T1 占比 < 60% → 補 IR / earnings transcript / 行業協會 source 取代 T3 個股 report。

---

## Gate 9 [必備 / 阻斷]｜§1 歷史錨點（日期 + 量化）

**規則**（搬自 DS Gate 14 / DS-9，阻斷性質）：§1 中每個 inflection point 段落必須同時包含：
1. **具體日期或月份**：YYYY 或 YYYY-MM 格式（不允許「過去幾年」「最近」「近期」模糊表述）。
2. **至少一個量化錨點**：價格、性能指標（TFLOPS / GB / 頻寬）、市占、capacity（GW / wafers）、用戶數、營收。

**為何阻斷**：歷史敘事是 v2.0 因果骨架的起點；缺日期 + 量化的歷史段是「口語回憶」不是可用於 timing 的分析。

**檢查碼**（每段檢查 `\b(19|20)\d{2}\b` 日期 + 至少一個數字單位）：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
m = re.search(r'<section[^>]*id="s1"[^>]*>(.*?)</section>', html, re.DOTALL)
if not m:
    print("FAIL: §1 (s1) not found"); raise SystemExit
s1 = m.group(1)
# 抓 §1 內所有 <p> 段（排除 lede 與 implication / aside）
paras = re.findall(r'<p[^>]*>(.*?)</p>', s1, re.DOTALL)
date_pat = re.compile(r'\b(19|20)\d{2}\b')
num_pat = re.compile(r'\d+(\.\d+)?\s?(%|\$|x|×|倍|GW|TW|MW|TFLOPS|GB|TB|MAU|DAU|億|萬|B\b|M\b|nm)')
fails = []
checked = 0
for i, p in enumerate(paras):
    txt = re.sub(r'<[^>]+>', '', p)
    # 只檢查「敘事性」段落（含日期跡象或 >60 字的 inflection 段）
    if len(re.sub(r'\s+','',txt)) < 40:
        continue
    has_date = bool(date_pat.search(txt))
    has_num = bool(num_pat.search(txt)) or bool(re.search(r'\d', txt))
    # inflection 段判定：段落足夠長且似乎在講歷史事件
    is_inflection = has_date or len(re.sub(r'\s+','',txt)) > 120
    if is_inflection:
        checked += 1
        if not (has_date and has_num):
            fails.append((i, '缺日期' if not has_date else '缺量化錨點', txt[:50]))
print(f"§1 檢查 inflection 段: {checked} 段")
if fails:
    print("FAIL: 以下段落缺日期或量化錨點（阻斷）：")
    for idx, why, snip in fails:
        print(f"  段 {idx}: {why} — 「{snip}...」")
else:
    print("PASS: §1 所有 inflection 段含日期 + 量化錨點")
PY
```

**Fail action**：阻斷發布，返工補錨點。範例：
- ❌「ChatGPT 興起後，NVDA H100 變成稀缺品」
- ✅「**2022-11-30 ChatGPT 發布**，兩個月內 MAU 衝破 1 億；**2023-03 H100 launch** 時 hyperscaler 已大量採購；**2023-Q3 NVDA DC 營收同比 +279%**，第一次出現 12+ 個月 lead time 配給」

---

## Gate 10 [warning]｜供需裁決明確 + §9 depth 時間限定 + catalyst 雙路徑 + 原 ID warning gates 摘要

**性質**：warning（不阻斷，但 fail 須在 report 明列）。本 Gate 是多個 sub-check 的集合。

### 10-1｜供需裁決三選一明確（搬自 DS Gate 7）

**規則**：§5 必須有明確的供需結論 — 三選一字眼之一：
- 「供需平衡」/「balance」
- 「供給過剩」/「surplus」/「oversupply」
- 「供給短缺」/「shortage」/「undersupply」

或更細「平衡偏寬鬆 / 平衡偏緊」，但必須有明確方向。允許「短期 X 中長期 Y」分時間段結論，但每段必須明確。**不准騎牆**（「可能 X 也可能 Y」）。

```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
m = re.search(r'<section[^>]*id="s5"[^>]*>(.*?)</section>', html, re.DOTALL)
s5 = m.group(1) if m else ''
verdict = re.findall(r'過剩|平衡|短缺|surplus|oversupply|shortage|undersupply|balance|偏寬鬆|偏緊', s5)
print(f"§5 裁決字眼: {set(verdict) if verdict else '無'}")
print("PASS" if verdict else "WARN: §5 缺明確供需裁決")
PY
```

### 10-2｜§9 ticker depth 閾值時間限定（搬自 DS Gate 14）

**規則**：§9 caption 或表頭若含「>X%」「≥Y%」「by YYYY」「forecast」字樣 → 必須在同 caption 或下方 footnote 註明時間基準。若 forward-looking → 表格每行另列「current YYYY actual」對照欄。

```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
m = re.search(r'<section[^>]*id="s9"[^>]*>(.*?)</section>', html, re.DOTALL)
if not m:
    print("WARN: §9 not found"); raise SystemExit
s9 = m.group(1)
threshold_words = re.findall(r'≥\s*\d+%|>\s*\d+%|≥\s*\$\d+', s9)
time_markers = re.findall(r'as of \d{4}|by 20\d{2}|20\d{2}[Q-]?\d?\s?actual|current|當前|forward.looking|forecast|projected', s9, re.IGNORECASE)
print(f"§9 閾值字樣: {len(threshold_words)}  時間限定字樣: {len(time_markers)}")
if threshold_words and not time_markers:
    print("WARN: §9 有閾值但無時間限定")
else:
    print("PASS")
PY
```

### 10-3｜Catalyst 雙路徑齊備（QC-12）

**規則**：§8 Catalyst Timeline ≥ 5 個節點，每個含明確日期 + 事件類別 + 檢視指標 + **若達成 / 若落空雙路徑**。缺雙路徑 → warn。

```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html").read()
m = re.search(r'<section[^>]*id="s8"[^>]*>(.*?)</section>', html, re.DOTALL)
s8 = m.group(1) if m else ''
pos = len(re.findall(r'若達成|ds-path-positive', s8))
neg = len(re.findall(r'若落空|ds-path-negative', s8))
print(f"§8 catalyst 雙路徑: 若達成 {pos} / 若落空 {neg}")
print("PASS" if pos >= 3 and neg >= 3 else "WARN: catalyst 雙路徑不齊（<3 對）")
PY
```

### 10-4｜原 ID warning gates 摘要（人工抽查）

下列原 ID v1.x warning gates 在 v2.0 收斂為本 Gate 子項，發布前人工抽查、fail 記入 report（不阻斷）：

| 子項 | 原 ID Gate | 檢查 |
|:---|:---|:---|
| **cross-ID 定性偏差** | 3.1 | 同一 ticker 在 ≥2 份 ID 都被寫「獨家 / 首家 / lock-in / 最大受益者」→ red flag，套 Gate 2.1 獨立驗證；錯誤成立 → 同步修所有相關 ID |
| **unit / scope 一致** | 5 | ASP（$/wafer vs $/stack vs $/GB）、Revenue 口徑（全年 / 季 / annualized）、營收 scope（segment / AI-only / total）宣告齊全；§0 前後有 unit glossary（QC-19） |
| **cross-ID layer 消歧** | 6 | 同主題跨 ID 明確標層次（CPO switch-level vs chip-to-chip；UALink 規格 vs ramp vs 商用；AVGO AI-only vs total）；ticker 評級跨 ID 一致 |
| **子題 value-add** | 7 | 子題 ID（Liquid Cooling vs 母題 AI DC）須有獨立 value-add（技術 deep dive / TAM 拆分 / 次要玩家 / 獨立 thesis），不能只重複母題 + 加幾檔 non-obvious |

**輸出格式**：
```
## Gate 10: Warning Checks
10-1 供需裁決明確: ✅ {過剩/平衡/短缺} / ⚠ 騎牆
10-2 §9 depth 時間限定: ✅ / ⚠
10-3 catalyst 雙路徑: ✅ {pos}/{neg} / ⚠
10-4 cross-ID bias: ✅ / ⚠ {ticker}
10-4 unit/scope: ✅ / ⚠
10-4 layer 消歧: ✅ / ⚠
10-4 子題 value-add: ✅ / N/A（非子題）/ ⚠
→ Gate 10: ✅ PASS / ⚠ WARNED（list）
```

---

## Gate 11 [必備 / 阻斷]｜Dual-Output 完整性

**規則**（v2.5 新）：每跑一次 skill 必產**兩份**（見 `templates/lean_template.md`）：
- canonical `ID_{Theme}_{date}.html` — 精煉版決策卡，**必含 lean template marker**（可機器檢查：`class="masthead"` + `class="dsum"`）**且含 id-meta**（`<script id="id-meta">`）。
- `ID_{Theme}_{date}_full.html` — 完整考證版，**不含 id-meta**（validator 自動 skip、不重複列索引）。

**為何阻斷**：v2.4 首發只產一檔、視覺回退 v2.0 紫版（無 masthead/dsum 精煉版元件），既有 10 道 gate 全無一條檢查「兩檔皆在 + 精煉版皮 + id-meta 分工正確」，缺口整份漏過。

**檢查碼**：
```bash
python3 << 'PY'
import os, re
canon = "docs/id/ID_{Theme}_{Date}.html"
full  = canon.replace(".html", "_full.html")
ok = True
# 1. 兩檔皆存在
c_exists, f_exists = os.path.exists(canon), os.path.exists(full)
print(f"canonical 存在: {'✅' if c_exists else '❌'} {canon}")
print(f"_full 存在: {'✅' if f_exists else '❌'} {full}")
ok &= c_exists and f_exists
if c_exists:
    ch = open(canon, encoding='utf-8').read()
    # 2. canonical 含 lean template marker（masthead + dsum）
    marker = ('class="masthead"' in ch) and ('class="dsum"' in ch)
    print(f"canonical lean marker (masthead+dsum): {'✅' if marker else '❌ 視覺回退嫌疑'}")
    # 3. canonical 含 id-meta
    c_meta = bool(re.search(r'<script\s+id="id-meta"', ch))
    print(f"canonical 含 id-meta: {'✅' if c_meta else '❌'}")
    ok &= marker and c_meta
if f_exists:
    fh = open(full, encoding='utf-8').read()
    # 4. _full 不含 id-meta
    f_meta = bool(re.search(r'<script\s+id="id-meta"', fh))
    print(f"_full 不含 id-meta: {'✅' if not f_meta else '❌ 重複 id-meta 會雙列索引'}")
    ok &= not f_meta
print("\nGate 11:", "PASS" if ok else "BLOCKED")
PY
```

**Fail action**：只產一檔 → 補產缺的那份（canonical 走 `lean_template.md`、`_full` 走 `html_template.md`）。canonical 無 masthead/dsum → 視覺回退，重套精煉版皮。`_full` 帶了 id-meta → 移除（`<meta name="id-*">` + `<script id="id-meta">` 只放 canonical）。

---

## Gate 12 [必備 / 阻斷]｜kill_metrics 同步 + 三值一致

**規則**（v2.5 新）：
1. id-meta `kill_metrics[]` **≥3 條**，且與 §8 證偽表**逐條對得上**（metric 名與 bear 閾值一致，非另編一套）。
2. id-meta `sd_verdict` / `clock_phase` / `conviction` 與 §0 6-box 卡片、§5 供需裁決**一致**（機器欄位不得與散文結論打架）。

**為何阻斷**：v2.5 把證偽表 / 供需裁決 / 投資時鐘 / conviction 從散文升為機器欄位（position-thesis-monitor 直接掃 `kill_metrics`、跨 ID 趨勢排序讀三值）— 若 id-meta 與正文脫節，下游讀到的是假訊號。

**檢查碼**：
```bash
python3 << 'PY'
import re, json
html = open("docs/id/ID_{Theme}_{Date}.html", encoding='utf-8').read()
m = re.search(r'<script\s+id="id-meta"[^>]*>(.*?)</script>', html, re.DOTALL)
meta = json.loads(m.group(1)) if m else {}
km = meta.get("kill_metrics", [])
print(f"kill_metrics 條數: {len(km)}（need ≥3）— {'✅' if len(km) >= 3 else '❌'}")
# §8 證偽表逐條對齊（人工複核 metric 名 + bear 閾值；此處先列出供對照）
s8 = re.search(r'<section[^>]*id="s8"[^>]*>(.*?)</section>', html, re.DOTALL)
s8_txt = re.sub(r'<[^>]+>', ' ', s8.group(1)) if s8 else ''
for i, k in enumerate(km):
    metric = k.get("metric", "")
    hit = metric[:6] in s8_txt if metric else False
    print(f"  kill[{i}] metric={metric!r} bear={k.get('bear_threshold','')!r} → §8 對照 {'✅' if hit else '⚠ 人工複核'}")
# 三值一致（§0 6-box / §5 裁決 — 人工複核，此處列 id-meta 值供對照）
print(f"sd_verdict={meta.get('sd_verdict')} / clock_phase={meta.get('clock_phase')} / conviction={meta.get('conviction')}")
print("→ 對照 §0 6-box + §5 裁決是否一致（人工複核）")
print("\nGate 12:", "PASS（≥3）" if len(km) >= 3 else "BLOCKED（<3）")
PY
```

**Fail action**：`kill_metrics` < 3 → 補齊至對齊 §8 證偽表 3-5 條。metric 名 / bear 閾值與 §8 對不上 → 二擇一改到一致。三值與 §0/§5 打架 → 修 id-meta 或修正文，以正文裁決為準。（`validate_id_meta.py` 已對 `skill_version` ≥ v2.5 阻斷 <3 條與缺三值，本 gate 額外驗「與正文對齊」。）

---

## Gate 13 [warning]｜§9 purity_pct segment 推導

**規則**（v2.5 新）：§9 表每檔 `purity_pct` 必附一行 segment 營收推導（footnote 或敘事，「該檔 segment 營收 ÷ 總營收 → __%」式），比照 `demand_5y_multiple` 的推導鏈要求。

**為何 warning**：v2.4 首發 ASMPT purity 標 85%，但其近半營收是 SMT（表面貼裝）非半導體後段封裝 — 無推導行就沒被攔，純度被灌水。有推導行才逼作者面對「85% 哪來的」。

**檢查碼**（掃 §9 是否每個純度數字鄰近有推導標記）：
```bash
python3 << 'PY'
import re
html = open("docs/id/ID_{Theme}_{Date}.html", encoding='utf-8').read()
m = re.search(r'<section[^>]*id="s9"[^>]*>(.*?)</section>', html, re.DOTALL)
s9 = m.group(1) if m else ''
purity_hits = len(re.findall(r'純度|purity', s9))
derive_hits = len(re.findall(r'推導[：:]|÷|營收占比|segment', s9, re.IGNORECASE))
print(f"§9 純度提及: {purity_hits} / 推導標記（推導/÷/segment）: {derive_hits}")
print("PASS" if derive_hits >= 1 else "WARN: §9 purity 缺 segment 推導行")
PY
```

**Fail action**：在 §9 表下方 footnote 或敘事補每檔一行 segment 推導（「XXX：封裝段營收 \$__B ÷ 總營收 \$__B → __%」）。

---

## 輸出格式：pre_publish_report.md

每次 gate check 產出一份報告：

```markdown
# Pre-Publish Gate Report — {ID_Name} v{version}
發布日：{date}

## Gate 1: Core Ticker Financials
✅ PASS / ❌ FAIL
- NVDA Q4 FY26（2026-02-25）在 60 天內 ✅

## Gate 2: Event-Triggered Thesis
✅ PASS / ❌ FAIL
- Thesis 1 [event]：Samsung yield 55%（2026-04-14 TrendForce 最新）✅
- Thesis 2 [structural]：not checked ✅

## Gate 2.1: Thesis Cornerstone Fact Verification
✅ PASS / ❌ FAIL — {findings}

## Gate 3: Cross-ID Reconciliation
✅ PASS / ❌ FAIL — {inconsistencies}

## Gate 4: id-meta JSON Validation
✅ PASS / ❌ FAIL — {缺漏欄位列表}

## Gate 5: §0 PM Implication Existence + Conviction Consistency
綠卡 exists: ✅ / ❌ MISSING
Five bullets / j-logic / conviction / ticker-name: ...
→ Gate 5: ✅ PASS / ❌ BLOCKED

## Gate 6: 文字比 ≥55% + 表格 cap
敘述比例: {Y}% — {PASS/FAIL}
表格數 {n}/10、超行表: {list}

## Gate 7: 推導鏈 regex（§4/§5/§7/§8/§9）
{per-section counts} — {PASS/FAIL}

## Gate 8: aside 來源 + T1 ≥60%
T1 share {Z}% — {PASS/FAIL}；missing-aside sections: {list}

## Gate 9: §1 歷史錨點
{checked} 段，fails: {list} — {PASS/FAIL}

## Gate 10: Warning Checks
{10-1..10-4} — {PASS/WARNED}

## Gate 11: Dual-Output 完整性
canonical 存在 / _full 存在 / lean marker / id-meta 分工: ✅ / ❌
→ Gate 11: ✅ PASS / ❌ BLOCKED

## Gate 12: kill_metrics 同步 + 三值一致
kill_metrics {n} 條（≥3）/ §8 逐條對齊 / sd_verdict·clock_phase·conviction 一致 §0/§5: ✅ / ❌
→ Gate 12: ✅ PASS / ❌ BLOCKED

## Gate 13: §9 purity 推導
每檔 purity_pct 有 segment 推導行: ✅ / ⚠
→ Gate 13: ✅ PASS / ⚠ WARNED

## Final Status
✅ ALL BLOCKING GATES PASS - 允許發布
⚠ WARNINGS (Gate 10/13): {list}
❌ BLOCKED at Gate {n}: {reason}
```

---

## 版本歷史
- **v2.5（2026-07-05）**：新增 Gate 11（阻斷｜dual-output 完整性 — canonical + `_full.html` 皆存在、canonical 含 lean marker（masthead+dsum）+ id-meta、`_full` 不含 id-meta；治 v2.4 首發只產一檔 / 視覺回退）、Gate 12（阻斷｜kill_metrics 同步 — id-meta `kill_metrics[]` ≥3 對齊 §8 證偽表 + sd_verdict/clock_phase/conviction 一致 §0/§5）、Gate 13（warning｜§9 purity_pct segment 推導行）。共 10 → 13 道。配合 industry-analyst v2.5 趨勢結構化欄位 + `validate_id_meta.py` v2.5+ 阻斷。
- **v2.0（2026-06-11）**：配合 industry-analyst v2.0（合併 ID + DS）完整重寫為 10 道 gate。Gate 1/2/2.1/3 從 ID v1.x 原文搬入；Gate 4（id-meta validate，原 ID Gate 8）/ Gate 5（PM 綠卡，原 ID Gate 9）保留；Gate 6（文字比 ≥55% + 表格 cap，搬 DS Gate 11+10、門檻 80%→55% / 表格 4→10）/ Gate 7（推導 regex，搬 DS Gate 13、掃 §4/§5/§7/§8/§9）/ Gate 8（aside 來源 + T1 ≥60%，搬 DS Gate 12、門檻 50%→60%）/ Gate 9（§1 錨點，搬 DS Gate 14/DS-9、阻斷）為 DS 移植；Gate 10（warning：供需裁決 + §9 depth 時間限定 + catalyst 雙路徑 + 原 ID 3.1/5/6/7 warning gates 摘要）。輸出 pre_publish_report.md 格式照舊。
- v1.7（2026-05-03）：新增 Gate 9（§0.7 PM Implication 存在 + conviction 一致性）。
- v1.6（2026-04-27）：新增 Gate 8（id-meta JSON Validation）。
- v1.5（2026-04-21）：新增 Gate 2.1（cornerstone fact）+ Gate 3.1（cross-ID bias）。
- v1.0（2026-04-19）：基於 8 份 ID peer review 累積建立。
