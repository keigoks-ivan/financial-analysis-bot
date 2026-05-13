# DS Pre-Publish Check — 14 道閘門（v1.1）

寫稿完成後、commit 前、Step 8.7 critic gate 前，逐項跑過。任一 fail → 返工，不可發布。

每道閘門包含：**Why**（為什麼這個 gate 存在）、**How to check**（如何驗證）、**Fail action**（fail 時怎麼修）。

---

## Gate 1 — 章節完整性 + 順序

**Why**：DS 11 章節骨架是脊椎。少一章 / 順序顛倒 → 整篇結構崩潰。

**How**：
```bash
grep -E '<h2>§(0|1|2|3|4|5|6|7|8|9|10|11) ' docs/ds/DS_{Theme}_{Date}.html | awk -F'§' '{print $2}' | awk '{print $1}'
```
應依序輸出：`0 1 2 3 4 5 6 7 8 9 10 11`。

**Fail action**：補章節，或重排到正確順序。

---

## Gate 2 — 事件型 claim 鮮度

**Why**：DS 引用具體 yield、訂單、capex 數字 → 14 天內 refresh 才算 fresh。逾期數字會被 critic flag。

**How**：對每個引述「20XX-Y QX earnings」「20XX-MM-DD 公告」「YoY +X%」格式的數字，confirm 來源 URL 是過去 14 天內。

**Fail action**：取新數字、或改寫成 structural 表述（不引絕對值）、或標 `[stale: dated 20XX-MM, verify before action]`。

---

## Gate 3 — ds-meta validator pass

**Why**：欄位完整、enum 在白名單、ticker 結構正確 → 索引腳本才能正確讀取。

**How**：
```bash
python3 scripts/validate_ds_meta.py docs/ds/DS_{Theme}_{Date}.html
```
應 exit 0、status: ok。

**Fail action**：依 validator output 訊息逐項修。

---

## Gate 4 — mega + sub_group 在 taxonomy 白名單

**Why**：分類體系與 ID 共用 → 寫入未知 mega/sub_group → index.html 找不到 anchor → 卡片插不進去。

**How**：對照 `docs/id/taxonomy.md` 表 1 + 表 2。Validator 也會檢查（Gate 3 已含）。

**Fail action**：選一個白名單值；若認為需要新分類，**先 commit 一個 PR 加新 sub_group 到 `docs/id/taxonomy.md` + `scripts/validate_id_meta.py` 的 TAXONOMY**，再寫 DS。

---

## Gate 5 — `related_ids[]` 指向真實存在的 ID

**Why**：DS 與 ID 互補設計依賴 cross-link 有效。指向不存在的 ID → 讀者點擊 404、stock-analyst dedup 失敗。

**How**：
```bash
for id_stem in $(jq -r '.[].related_ids[]?' < <(python3 -c "import json,re,sys;t=open(sys.argv[1]).read();m=re.search(r'<script id=\"ds-meta\".*?>(.*?)</script>',t,re.S);print(json.dumps([json.loads(m.group(1))]))" docs/ds/DS_{Theme}_{Date}.html)); do
  test -f "docs/id/${id_stem}.html" || echo "MISSING: ${id_stem}.html"
done
```
無 MISSING 行 → pass。

**Fail action**：
- 若是手誤打錯 stem → 改回正確的
- 若該 ID 已被 archive / rename → 從 related_ids[] 移除或更新 stem
- 若 DS §0 callout 寫到該 ID → 同步移除 callout

---

## Gate 6 — §1 → §3 / §5 / §6 因果鏈可追溯

**Why**：DS 核心是因果敘事。若 §1 寫完歷史、§3/§5/§6 完全不引用歷史推導 → 讀者無法理解「為何今天到這裡 → 未來會去哪裡」。

**How**（人工檢查）：
- 從 §1 找出 2-3 個關鍵歷史事件 / 模式
- 在 §3 / §5 / §6 內 grep 是否有顯式引用（不需 verbatim，可改寫但要點到）
- 例：§1 寫了「2012 年 CUDA 從硬體公司變平台公司」→ §3 / §5 / §6 中至少一處要回應「軟體棧今天是否仍是 binding moat」

**Fail action**：補敘述橋段，明確把歷史事件連到當代供給 / 需求 / 推估。

---

## Gate 7 — §3 + §5 → 供需平衡結論明確（過剩 / 平衡 / 短缺）

**Why**：DS 最大價值是把供需兩端合在一起、給出**明確結論**。模稜兩可 → §6 推估缺基礎。

**How**：在 §5 末尾或 §6 開頭尋找 `.ds-bridge` 段落，確認該段落出現以下三選一字眼：
- 「供需平衡」/「balance」
- 「供給過剩」/「surplus」/「oversupply」
- 「供給短缺」/「shortage」/「undersupply」

或更細緻的「平衡偏寬鬆 / 平衡偏緊」也接受，但必須有明確方向。

**Fail action**：返工 §5 結尾，寫明確結論。允許「短期 X 中長期 Y」這種分時間段的結論，但每個時間段必須明確。

---

## Gate 8 — §6 三 horizon × 三情境 + trigger 完整

**Why**：DS §6 是唯一允許 scenario 表格的章節，必須完整否則就失去意義。

**How**：在 §6 找到表格，確認：
- 三列：短期（12M）、中期（3Y）、長期（5Y+）
- 三欄：base / bull / bear（除了 horizon 與 trigger 欄外）
- Trigger 欄非空（每個 horizon 一個可量化 metric）
- 表外有 ≥ 3 段敘述展開三個 horizon 的邏輯

**Fail action**：補缺漏的 cell / trigger / 敘述段落。

---

## Gate 9 — §11 ≥ 3 ticker + depth + DD link

**Why**：§11 是 stock-analyst 自動讀取的 hook。少於 3 檔 → DS 的個股關聯太薄、stock-analyst 找不到對應引用。

**How**：
```bash
grep -c '<tr>' docs/ds/DS_{Theme}_{Date}.html | head -1
# 應 ≥ 3 (扣掉 thead 的 <tr>)
```
或人工數 §11 表格行數（不含表頭）≥ 3。

每筆必有：ticker、role、depth（🔴/🟡/🟢）、beneficiary（受益 / 受害）、對應 DD（若有）。

**Fail action**：補 ticker；若該 theme 真的相關個股太少 → 重新評估 theme 是否適合做 DS。

---

## Gate 10 — 表格數 ≤ 4、行數 ≤ 8/張（§11 例外可至 16）

**Why**：80/20 文字表格比的 hard cap。表格過多 → 失去 DS 敘述本色。**例外**：§11 ticker reference table 是 stock-analyst hook，要列出完整 ticker 清單，允許至 16 行。

**How**：
```bash
python3 -c "
import re,sys
html = open(sys.argv[1]).read()
tables = re.findall(r'<table[^>]*>.*?</table>', html, re.DOTALL)
print(f'表格數: {len(tables)}')
for i, t in enumerate(tables):
    tbody_m = re.search(r'<tbody>(.*?)</tbody>', t, re.DOTALL)
    tbody = tbody_m.group(1) if tbody_m else t
    rows = len(re.findall(r'<tr', tbody))
    # 判斷是否為 §11 ticker table（含 .ds-tickers class 或 ticker 欄位）
    is_s11 = 'ds-tickers' in t or 'depth-red' in t or 'depth-yellow' in t
    cap = 16 if is_s11 else 8
    status = 'OK' if rows <= cap else 'FAIL'
    print(f'  表 {i+1}: {rows} 行（cap {cap}）— {status}')
" docs/ds/DS_{Theme}_{Date}.html
```

**Fail action**：把多餘的表格資訊轉為敘述段落；單表行數超標 → 合併 / 取捨。§11 若超過 16 行 → 把邊緣 ticker（🟢 深度）拆到表外文字描述。

---

## Gate 11 — 文字比例 ≥ 80%

**Why**：DS 最核心的硬性規則。低於 80% → DS 與 ID 區隔模糊，會被誤當「加長版 ID」。

**How**：
```bash
python3 << 'PY'
import re, sys

path = "docs/ds/DS_{Theme}_{Date}.html"
html = open(path).read()

# 1. 移除 <script>...</script>、<style>...</style>、<!-- comments -->
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)

# 2. 抓所有 <table>...</table> 區塊
tables = re.findall(r'<table[^>]*>.*?</table>', clean, flags=re.DOTALL)
table_chars = sum(len(re.sub(r'<[^>]+>', '', t)) for t in tables)

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
print(f"PASS" if ratio >= 0.80 else f"FAIL (目標 ≥ 80%)")
PY
```

**Fail action**：
- 若 78-80%：再寫一些 `.ds-implication` 段落（每章末），補足缺口
- 若 < 78%：檢查是否有可轉敘述的表格、是否某些 §X 章節敘述太薄

---

## Gate 12（v1.1 新）— 量化斷言必附 source-tag + T1 占比 ≥ 50%

**Why**：DS v1.0 沒強制 source-tag；DS_AIAcceleratorDemand 全文 0 個 source-tag，所有量化斷言（McKinsey CAGR、AVGO 60%、NVDA top-5 55-60%、FERC 1500-2000 GW）無出處 → PM 無法獨立驗證。v1.1 移植 ID 的 `<span class="source-tag">[T1:]` 設計，每個量化斷言必附 tag。

**規則**（QC-DS13）：
- 任何 % / $ / GW / 倍數 / 市占 / 增長率 / TAM / 用戶數 / 訂單數 / capex / 員工數 數字 → 鄰近 80 字符內必須有 `<span class="source-tag">`
- 全文 T1 + T1-zh 占比 ≥ 50%
- 免標：純結構性敘述（"NVDA 主導 GPU 市場"）、廣為人知歷史事件（"ChatGPT 2022-11 發布"）、純定性判斷、引用自前段已標的同一數字

**How（兩段檢查）**：

```bash
# Part A: 算 source-tag 總數 + tier 分佈
python3 << 'PY'
import re, sys
html = open("docs/ds/DS_{Theme}_{Date}.html").read()
tags = re.findall(r'<span class="source-tag">\[(T[12]|T3-[ABC]|T1-zh|T2-zh|T3-zh|T4)[:：]', html)
from collections import Counter
counts = Counter(tags)
total = sum(counts.values())
t1 = counts.get('T1', 0) + counts.get('T1-zh', 0)
t1_share = t1 / total if total else 0
print(f"Source-tag total: {total}")
print(f"  T1+T1-zh: {t1} ({t1_share:.1%})")
print(f"  T2+T2-zh: {counts.get('T2',0)+counts.get('T2-zh',0)}")
print(f"  T3-A: {counts.get('T3-A',0)}, T3-B: {counts.get('T3-B',0)}, T3-C: {counts.get('T3-C',0)}, T3-zh: {counts.get('T3-zh',0)}")
print(f"  T4: {counts.get('T4',0)}")
print("PASS" if t1_share >= 0.50 else f"FAIL: T1 share {t1_share:.1%} < 50%")
PY

# Part B: 找量化數字附近 80 字符內是否有 source-tag
python3 << 'PY'
import re
html = open("docs/ds/DS_{Theme}_{Date}.html").read()
# 剝 script/style/source-tag 內含 URL 的數字
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<span class="source-tag">.*?</span>', 'XSRCTAGX', clean, flags=re.DOTALL)
# 找關鍵量化模式
patterns = [
    (r'\$\s?\d+(\.\d+)?\s?[BMK]?', '$amount'),
    (r'\d+(\.\d+)?\s?%', 'percentage'),
    (r'\d+(\.\d+)?\s?(GW|TW|MW)', 'capacity'),
    (r'\d+(\.\d+)?\s?(倍|x|×)', 'multiple'),
]
missing = 0
samples = []
for pat, label in patterns:
    for m in re.finditer(pat, clean):
        # check 80 char window
        start = max(0, m.start() - 80)
        end = min(len(clean), m.end() + 80)
        window = clean[start:end]
        if 'XSRCTAGX' not in window:
            missing += 1
            if len(samples) < 5:
                samples.append((label, m.group(), clean[max(0,m.start()-30):min(len(clean),m.end()+30)]))
print(f"量化斷言無 source-tag 鄰近: {missing} 處")
for label, num, ctx in samples:
    print(f"  [{label}] {num} — ...{ctx}...")
print("PASS (≤ 3 misses allowed for non-quantitative context)" if missing <= 3 else "FAIL")
PY
```

**Fail action**：補 source-tag。若某數字真無 T1 可得 → 用 T2/T3 + 在文末加 ⚠️ source-warning aside。T1 占比過低 → 補 IR / earnings transcript / 行業協會 source 取代 T3 個股 report。

---

## Gate 13（v1.1 新）— §5/§6/§7/§9/§11 推導可追溯性

**Why**：DS v1.0 §5/§6 bull/bear case 給絕對數字但不寫推導 — PM 看不出 bull case +20% 來自哪個 input 變動。v1.1 從 stock-analyst v12.2 移植「推導可追溯性原則」 — 任何結論數字必附 ≤ 3 行推導（input → calculation → implication）。

**規則**（QC-DS16）：以下章節的結論數字必附「推導：」行或等效標記（如「→」「換算」「計算」開頭的短行）：
- §5 TAM 三情境（base/bull/bear）+ CAGR
- §6 三 horizon × 三 case 全部 cell
- §7 phase 轉換的量化閾值
- §9 三條 Kill Scenario 的 trigger metric
- §11 ticker depth 閾值

**How**：

```bash
python3 << 'PY'
import re
html = open("docs/ds/DS_{Theme}_{Date}.html").read()
# Locate each section
sections = {}
for m in re.finditer(r'<h2[^>]*>§(\d+)\s*[^<]+</h2>(.*?)(?=<h2[^>]*>§|\Z)', html, re.DOTALL):
    sections[int(m.group(1))] = m.group(2)

required = [5, 6, 7, 9, 11]
for sec in required:
    body = sections.get(sec, '')
    # count derivation markers
    derive_count = len(re.findall(r'推導[：:]', body))
    arrow_count = len(re.findall(r'→', body))
    # count quantitative claims
    num_count = len(re.findall(r'\$\d|\d+%|\d+ GW|\d+\.\d+ 倍', body))
    print(f"§{sec}: 量化數字 {num_count} 處, 推導行 {derive_count} 條, → 箭頭 {arrow_count} 個")
    if num_count > 3 and derive_count == 0 and arrow_count < num_count // 2:
        print(f"  FAIL §{sec}: 結論數字無對應推導行")
PY
```

**Fail action**：在結論數字鄰近段內補一行「推導：input1 + input2 → calc → implication」。例：
- ❌ 「bull case TAM $340B」
- ✅ 「bull case TAM $340B（推導：hyperscaler capex $720B × workload mix 35% × accelerator ratio 1.33 → $340B；對比 base $280B 的 +20% 來自 capex 兌現度從 100% 上修至 120%）」

---

## Gate 14（v1.1 新）— §11 ticker depth 閾值時間限定

**Why**：DS v1.0 §11 caption 寫「🔴 = AI rev ≥ 40%」沒指明 current vs forward-looking → AMD 當前 ~8% AI rev 被標 🔴（forecast 2027-2028）讓讀者困惑。v1.1 強制時間基準明示 + forward-looking 必附 current actual 對照欄。

**規則**（QC-DS18）：§11 caption 或表頭如有「>X%」「≥Y%」「by YYYY」「forecast」字樣 → 必須在同 caption 或下方 footnote 註明時間基準。若是 forward-looking → 表格每行另列「current YYYY actual」欄。

**How**：

```bash
python3 << 'PY'
import re
html = open("docs/ds/DS_{Theme}_{Date}.html").read()
# 抓 §11 整段
m = re.search(r'<h2[^>]*>§11[^<]*</h2>(.*?)(?=<h2|\Z)', html, re.DOTALL)
if not m:
    print("FAIL: §11 not found")
    exit()
s11 = m.group(1)
# 找閾值字樣
threshold_words = re.findall(r'≥\s*\d+%|>\s*\d+%|≥\s*\$\d+', s11)
# 找時間限定字樣
time_markers = re.findall(r'as of \d{4}|by 20\d{2}|2026[Q-]?\d?\s?actual|current|forward.looking|forecast', s11, re.IGNORECASE)
print(f"§11 閾值字樣: {len(threshold_words)} 個 ({threshold_words[:3]})")
print(f"§11 時間限定字樣: {len(time_markers)} 個 ({time_markers[:3]})")
if threshold_words and not time_markers:
    print("FAIL: §11 有閾值但無時間限定")
elif threshold_words:
    # check current actual column
    has_current_col = bool(re.search(r'current.*actual|當前.*實際|2026.*actual', s11, re.IGNORECASE))
    if 'by 20' in s11.lower() or 'forecast' in s11.lower() or 'projected' in s11.lower():
        print(f"§11 forward-looking 閾值: {'有' if has_current_col else '無'} current actual 對照欄")
        if not has_current_col:
            print("FAIL: forward-looking 閾值但無對照欄")
PY
```

**Fail action**：
- 若是 current actual 閾值 → caption 加「as of 2026-Q1」
- 若是 forward-looking 閾值 → caption 加「by 2028 forecast」+ 表格加 current actual 對照欄
- 範例：`🔴 = projected AI rev ≥ 40% by 2028。AMD 雖 current 8%，但 projected 45% → 標 🔴`

---

## Gate 8.7（不在編號內，但 mandatory）— Critic gate

完成 Gate 1-11 後，**強制呼叫 id-review skill --mode ds**：

```
Agent({
  description: "Cold review DS draft {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the id-review sub-agent in DS mode. \
Read spec at /Users/ivanchang/.claude/skills/id-review/SKILL.md. \
Mode: --mode ds. DS file: docs/ds/DS_{Theme}_{Date}.html. \
Save critic report to docs/ds/_critic_{Theme}_{Date}.md."
})
```

Critic 額外檢查（在 Gate 1-14 之外）：
- DS-specific anti-patterns（見 SKILL.md「常見錯誤」段）
- §8 三條 Non-Consensus thesis 是否真有市場差異（不是 strawman）
- §9 三條 Kill Scenario 是否真正能 falsify thesis（不是稻草人）
- §10 Catalyst 是否真有具體日期 + 雙路徑
- **DS-2 升級（v1.1）**：§1 inflection 必須閉合在 §3 或 §5，不可延後到 §8
- **DS-7（v1.1）**：抽 5 個量化斷言驗 source-tag + tier + URL 可達；計算 T1 占比
- **DS-8（v1.1）**：抽 §6 base/bull/bear 各一格驗推導 input 可追到 §2-§5
- **DS-9（v1.1）**：§1 每段含日期 + 量化錨點

Critic 結果：
- 🔴 **CHANGES_CONCLUSION**：阻擋發布
- 🟡 **PARTIAL_ERROR**：呈現給 user 互動式 patch
- 🟢 **COSMETIC**：紀錄但不阻擋

---

## Quick reference — 全部 14 Gates（v1.1）

| Gate | 檢查內容 | Auto / Manual |
|:---:|:---|:---:|
| 1 | 11 章節完整 + 順序 | Auto (grep) |
| 2 | 事件型 claim 14 天內 refresh | Manual |
| 3 | ds-meta validator pass | Auto (validate_ds_meta.py) |
| 4 | mega + sub_group 在白名單 | Auto (含於 Gate 3) |
| 5 | related_ids 對應 ID 存在 | Auto (shell loop) |
| 6 | §1 → §3 / §5 / §6 因果鏈（v1.1 強化：閉合在 §3/§5） | Manual |
| 7 | §3 + §5 供需平衡明確結論 | Manual + grep |
| 8 | §6 三 horizon × 三情境 + trigger 完整 | Manual |
| 9 | §11 ≥ 3 ticker + depth + DD link | Auto (grep) |
| 10 | 表格 ≤ 4 張 + 行數 ≤ 8 | Auto (inline Python) |
| 11 | 文字比例 ≥ 80% | Auto (inline Python) |
| **12** | source-tag 完整性 + T1 占比 ≥ 50% | Auto (inline Python) |
| **13** | §5/§6/§7/§9/§11 推導可追溯性 | Auto (inline Python) |
| **14** | §11 ticker depth 閾值時間限定 | Auto (inline Python) |
| 8.7 | id-review --mode ds critic（含 DS-7/8/9） | Mandatory spawn |
