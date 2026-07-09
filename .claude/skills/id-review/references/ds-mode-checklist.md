# id-review v1.6.1 — ds-mode-checklist.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-09 v1.6.1 結構拆分，內容自 v1.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 【DS Mode 檢查清單】（v1.3 新增）

當 `--mode ds`，跑 Step 1-7 patch flow 但 **檢查清單改用以下 6 條**（取代 ID 模式的 §12/§13/cornerstone/thesis-box 檢查）。

DS 沒有 §12 Non-Consensus（DS 有 §8 Non-Consensus 但敘述形式不是 tag 體系）、沒有 §13 Falsification metric table、沒有 §10.5 catalyst table（DS 的 catalyst 是 §10 敘述形式），所以原本 ID critic 的核心鎖點全部不適用。DS 改驗以下「敘述結構正確性」鎖點。

### DS-1：表格比例硬限制

| 項目 | Pass | Fail |
|:---|:---|:---|
| 表格數量 | ≤ 4 張 | > 4 張 |
| 單表行數 | 每張 ≤ 8 行（不含表頭）| 任一張 > 8 行 |
| 文字字元比例 | ≥ 80% | < 80% |

**檢查方式**：
```bash
python3 << 'PY'
import re
html = open("docs/ds/DS_X.html").read()
clean = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
tables = re.findall(r'<table[^>]*>.*?</table>', clean, flags=re.DOTALL)
text_total = len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',clean)))
table_text = sum(len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',t))) for t in tables)
print(f"tables: {len(tables)}, ratio: {1-table_text/text_total:.1%}")
PY
```

**Fail 處置**：🔴 CHANGES_CONCLUSION。表格 > 4 張或文字 < 78% → 大錯。78-80% → 🟡 PARTIAL（補敘述）。

### DS-2：§1 → §3 / §5 / §6 因果鏈（v1.4 升級：必須閉合在 §3 或 §5）

**Why**：DS 核心是因果敘事。§1 歷史寫完後，必須在 §3（未來供給）或 §5（未來需求）中有顯式回應 — 「歷史告訴我們 X，所以未來 Y」。**v1.4 升級**：v1.3 critic 只抓「§1 是否被 §3/§5/§6 引用」，但 AI Accelerator DS v1.0 暴露漏網之魚 — CUDA 護城河答案延後到 §8 Non-Consensus（不是 §3 或 §5），破壞了「歷史 → 未來」因果 spine。v1.4 改為「§1 inflection 必須在 §3 或 §5 找到對應回答段（≥ 50 字符）；若答案出現在 §6/§7/§8/§9 → 仍 fail」。

**檢查方式**：
1. 人工讀 §1 提煉 2-3 個關鍵 inflection point（歷史事件 / 技術代際 / 護城河形成節點）
2. 對每個 inflection，在 §3（未來供給）+ §5（未來需求）中 grep 是否有顯式回應段（≥ 50 字符）
3. 若 §3/§5 均無回應、但 §6/§7/§8/§9 有回答 → 標 PARTIAL_ERROR（破壞 spine 但非完全脫節）

**範例 fail**：§1 寫「2012 年 CUDA 把 NVDA 變平台公司」→ §3 / §5 完全沒回應「CUDA 在 inference 階段是否仍是 binding moat」，卻把答案放在 §8 Non-Consensus（「市場認為 CUDA 不可動搖、我們認為 ROCm 已縮短差距」）→ 🟡 PARTIAL_ERROR：要求把 §8 內容前置一部分到 §3。

**Fail 處置**：
- 🔴 CHANGES_CONCLUSION：§6 推估完全脫離 §1 歷史（無任何 trace）
- 🟡 PARTIAL_ERROR（v1.4 新）：§1 → §3/§5 不閉合但 §8/§9 有回應 → 要求把答案前置到 §3 或 §5
- 🟢 COSMETIC：部分連結但不顯式 → 補敘述橋段

### DS-3：§3 + §5 → 供需平衡明確結論

**Why**：DS 最大價值 — 把供需兩端合在一起、給出明確結論。模稜兩可 → §6 推估缺基礎。

**檢查方式**：在 §5 結尾或 §6 開頭尋找 `.ds-bridge` 段落（或等價 prose 段落），確認出現以下三選一：
- 「過剩 / surplus / oversupply」
- 「平衡 / balance」
- 「短缺 / shortage / undersupply」

允許分時間段（「短期 X 中長期 Y」），但每段必須明確。

**Fail 處置**：🔴 — 缺結論 → 阻擋發布。

### DS-4：§6 三 horizon × 三情境 + trigger 完整

**檢查項**：
- 表格三列：12M / 3Y / 5Y+
- 表格三欄：base / bull / bear
- Trigger 欄非空（每 horizon 一個可量化 metric）
- 表外有 ≥ 3 段敘述展開三個 horizon 的邏輯

**Fail 處置**：🔴（缺 horizon 或 trigger）/ 🟡（敘述太薄）

### DS-5：§10 Catalyst 雙路徑

**Why**：catalyst 不只是列日期。每個節點必須寫「若達成 → X」「若落空 → Y」雙路徑，否則 catalyst 變單純時間表，喪失 falsification 價值。

**檢查方式**：grep `<time>` 或 `class="ds-time"` 標記後 30 字內是否含「若達成 / 若落空」「if hit / if miss」「達成 / 落空」字眼。

**Fail 處置**：🟡（部分節點有單路徑）/ 🔴（全部單路徑）

### DS-6：§11 ticker 與 §3 / §5 敘述一致

**Why**：§11 是 stock-analyst hook。若 §3 寫供給過剩、§11 把所有供應商標 🔴 beneficiary，邏輯不通。

**檢查方式**：
- 找 §11 標 🔴 beneficiary=true 的 ticker
- 對每個這樣的 ticker，確認 §3（未來供給）或 §5（未來需求）有敘述支持「為何此 ticker 受益」
- 同理對 🔴 beneficiary=false 的 ticker，確認有敘述支持「為何受害」

**Fail 處置**：🟡（個別 ticker 缺對應）/ 🔴（系統性矛盾）

### DS-7：已移除（v1.4.1，2026-05-13）

原 v1.4 source-tag 抽查 + T1 占比 + 黑名單檢查。industry-ds v1.2 把 inline source-tag 改為 §末 `<aside class="ds-refs">`，pre-publish Gate 12 已更新為 aside 結構檢查 + T1 占比，DS-7 與 Gate 12 重疊度 ~80%，剩 20% 為 redundancy → 移除。編號保留 gap，不 renumber DS-8/DS-9（git 歷史看得出 DS-7 曾存在）。

### DS-8（v1.4 新）：§6 推導可追溯性抽查

**Why**：DS v1.0 §5/§6 bull/bear case 給絕對數字但不寫推導 — PM 無法獨立判斷 bull case +20% 來自哪個 input 變動。v1.1 從 stock-analyst v12.2 移植「推導可追溯性原則」 — §6 三 case 必須附 input → calc → implication 推導。

**檢查方式**：
1. 從 §6 表格中**隨機抽 base / bull / bear 各一格**
2. 對每個抽到的 cell：
   - 表外緊鄰段落（同 horizon 的敘述展開段）是否有「推導：」字串或等效推導行（「→」「換算」「計算」開頭的短行）
   - 推導行中提到的 input 數字（如「hyperscaler capex $600B」「workload mix 35%」「accelerator ratio 1.33」），是否能在 §2/§3/§4/§5 找到對應出處（不是憑空假設）
   - bull / bear 偏離 base 的程度是否由「某個 input 假設改變」推出（不是無理由的 ±20%）

**範例 fail**：
- 表格寫「base case 2028 NVDA share 60-65%」、「bull 70-75%」、「bear 45-50%」
- 表外段落只寫「base 假設 ASIC 滲透率穩定、bull 假設 CUDA inference 護城河持續、bear 假設 ASIC 加速」
- 但沒寫「ASIC 滲透率 30% → NVDA 62% / 20% → NVDA 72% / 45% → NVDA 47%」這種具體映射
- → 🟡 PARTIAL_ERROR：要求把每個 case 對應的 input 數字寫出來

**Fail 處置**：
- 🔴：§6 完全沒有推導行（所有 cell 都是黑盒）
- 🟡：部分 cell 有推導但 input 數字無法追到 §2-§5
- 🟢：推導存在但不夠精確

### DS-9（v1.4 新）：§1 雙錨點（日期 + 量化）

**Why**：DS v1.0 §1 只要求「2-3 個歷史轉折點」但沒規定錨點精度。AI Accelerator DS v1.0 出現「ChatGPT-Hopper 配給」這種口語式錨點 — 沒有 H100 launch 具體日期（2023-03）、沒有 ChatGPT MAU 100M 達成時間（2023-01-31）、沒有當時的 lead time 數字。v1.1 強制每個 inflection 段必含具體日期 + 量化錨點。

**檢查方式**：對 §1 每個 inflection point 段落（通常 2-4 段）正則檢查：
```python
import re
# 抓 §1 全文
s1 = re.search(r'<h2[^>]*>§1[^<]*</h2>(.*?)(?=<h2|\Z)', html, re.DOTALL).group(1)
# 拆段落
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', s1, re.DOTALL)
for i, p in enumerate(paragraphs):
    text = re.sub(r'<[^>]+>', '', p)
    has_date = bool(re.search(r'\b(19|20)\d{2}(-\d{2})?\b', text))
    has_number = bool(re.search(r'\d+\s*%|\$\s?\d+|\d+\s?(GW|TFLOPS|GB|MAU|B|M)|\d+x|\d+\s?倍', text))
    if not (has_date and has_number):
        print(f"§1 段 {i+1}: 缺 {'日期' if not has_date else ''} {'量化錨點' if not has_number else ''}")
```

**範例 fail**：
- ❌「過去幾年 AI 加速器需求快速成長」← 無日期、無量化
- ❌「ChatGPT 興起後，H100 變稀缺品」← 有事件但無日期 + 無量化
- ✅「**2022-11-30 ChatGPT 發布**，兩個月內 **MAU 衝破 1 億**；**2023-03 H100 launch** 時 hyperscaler 已開始大量採購；**2023-Q3 NVDA DC 營收同比 +279%**，第一次出現 **12+ 個月 lead time 配給**」

**Fail 處置**：
- 🔴：§1 完全無日期錨點（所有段都是「過去」「最近」這類模糊表述）
- 🟡：部分段有日期但無量化錨點（或反之）
- 🟢：有日期但精度太低（只到 decade）
