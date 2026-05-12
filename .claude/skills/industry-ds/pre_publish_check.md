# DS Pre-Publish Check — 11 道閘門

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

## Gate 10 — 表格數 ≤ 4、行數 ≤ 8/張

**Why**：80/20 文字表格比的 hard cap。表格過多 → 失去 DS 敘述本色。

**How**：
```bash
python3 -c "
import re,sys
html = open(sys.argv[1]).read()
tables = re.findall(r'<table[^>]*>.*?</table>', html, re.DOTALL)
print(f'表格數: {len(tables)}')
for i, t in enumerate(tables):
    rows = len(re.findall(r'<tr[^>]*>', t)) - 1  # -1 for header
    print(f'  表 {i+1}: {rows} 行')
" docs/ds/DS_{Theme}_{Date}.html
```

**Fail action**：把多餘的表格資訊轉為敘述段落；單表行數超標 → 合併 / 取捨。

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

Critic 額外檢查（在 Gate 1-11 之外）：
- DS-specific anti-patterns（見 SKILL.md「常見錯誤」段）
- §8 三條 Non-Consensus thesis 是否真有市場差異（不是 strawman）
- §9 三條 Kill Scenario 是否真正能 falsify thesis（不是稻草人）
- §10 Catalyst 是否真有具體日期 + 雙路徑

Critic 結果：
- 🔴 **CHANGES_CONCLUSION**：阻擋發布
- 🟡 **PARTIAL_ERROR**：呈現給 user 互動式 patch
- 🟢 **COSMETIC**：紀錄但不阻擋

---

## Quick reference — 全部 11 Gates

| Gate | 檢查內容 | Auto / Manual |
|:---:|:---|:---:|
| 1 | 11 章節完整 + 順序 | Auto (grep) |
| 2 | 事件型 claim 14 天內 refresh | Manual |
| 3 | ds-meta validator pass | Auto (validate_ds_meta.py) |
| 4 | mega + sub_group 在白名單 | Auto (含於 Gate 3) |
| 5 | related_ids 對應 ID 存在 | Auto (shell loop) |
| 6 | §1 → §3 / §5 / §6 因果鏈 | Manual |
| 7 | §3 + §5 供需平衡明確結論 | Manual + grep |
| 8 | §6 三 horizon × 三情境 + trigger 完整 | Manual |
| 9 | §11 ≥ 3 ticker + depth + DD link | Auto (grep) |
| 10 | 表格 ≤ 4 張 + 行數 ≤ 8 | Auto (inline Python) |
| 11 | 文字比例 ≥ 80% | Auto (inline Python) |
| 8.7 | id-review --mode ds critic | Mandatory spawn |
