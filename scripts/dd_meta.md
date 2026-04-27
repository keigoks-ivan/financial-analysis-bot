# DD metadata pipeline (dd-meta JSON, plan-A architecture)

**Goal**: 一勞永逸解決「下游工具反向 parse DD HTML 不穩」的問題。讓 stock-analyst skill
在生成 DD 時直接 emit 結構化 JSON，所有下游消費者（research index、PM skill、
morning-briefing、未來新工具）只 parse JSON，不再 regex HTML 內文。

## 架構

```
                ┌─────────────────────────┐
                │  stock-analyst skill    │
                │  (~/.claude/skills/...) │
                └────────────┬────────────┘
                             │ generates
                             ▼
       ┌───────────────────────────────────────────┐
       │  docs/dd/DD_*.html                        │
       │  ── <script id="dd-meta">{...}</script>   │
       │  ── (rest is presentation)                │
       └───────────────────┬───────────────────────┘
                           │
            ┌──────────────┼──────────────┬──────────────┐
            ▼              ▼              ▼              ▼
       update_dd_   portfolio-   morning-       custom
       index.py     manager      briefing       analysis
       (research    skill        (cross-repo)   scripts
       index sync)
```

**SSOT** = `dd-meta` JSON block. Schema 在 `validate_dd_meta.py` 的 `REQUIRED_FIELDS` /
`ENUM_FIELDS` / `NUMERIC_RANGES` 三組常數。

## Tooling

| Script | 用途 | 何時跑 |
|---|---|---|
| `dd_meta_reader.py` | Reusable Python module — `read_dd_meta()`, `iter_dd_metas()`, `filter_v12()`, `latest_per_ticker()`. Stdlib-only, 可 import 到任何工具 | Library，被其他 script import |
| `validate_dd_meta.py` | Schema 驗證器。檢查必填欄位、type、enum、numeric range、date format | CI gate (`.github/workflows/validate_dd_meta.yml`)；本地 sanity check |
| `backfill_dd_meta.py` | 對沒有 dd-meta block 的 v12 DD，用 regex 抽出可得欄位寫入 JSON。**部分填補**——抽不出的欄位省略 | 一次性，已對 56 個 legacy v12 DD 跑完 |
| `update_dd_index.py` | 從 dd-meta JSON 讀資料，**全自動重建** `docs/research/index.html` v12 表格（每次跑都重排序 + 重寫 row）。支援 `--dry-run` 預覽 diff | DD 產出後（手動）/ 未來 CI |

## 使用案例

### 看當前所有 DD 的 metadata 完整度

```bash
python scripts/validate_dd_meta.py --report
```

輸出：`✅ ok / ⚠ missing / ❌ invalid` 個數 + 每個 invalid 檔案的缺漏欄位清單。
`--report` 永遠 exit 0；不加 `--report` 是 strict mode（任何問題 exit 1，CI 用）。

### 規則：dd-meta JSON 是 SSOT

**不要直接編輯 `docs/research/index.html` 的 row。** `update_dd_index.py` 會在每次
跑的時候從 dd-meta JSON 重新產出整個 tbody。手動編輯的 row 會在下次跑被覆寫。

要修正 row 內容，編輯 DD HTML 內的 `<script id="dd-meta">` JSON 區塊，然後跑：

```bash
python scripts/update_dd_index.py --dry-run   # 預覽 diff
python scripts/update_dd_index.py             # 套用
```

排序順序固定為：訊號燈 desc (A+→X) → 陷阱 desc (🟢→🔴) → 中期 upside desc → 日期 desc。

### 在自訂 script 中讀 v12 DD 資料

```python
import sys
sys.path.insert(0, "/Users/ivanchang/financial-analysis-bot/scripts")
from dd_meta_reader import iter_dd_metas, filter_v12, latest_per_ticker

DD_DIR = "/Users/ivanchang/financial-analysis-bot/docs/dd"
metas = filter_v12([m for _, m in iter_dd_metas(DD_DIR)])
latest = latest_per_ticker(metas)

# 例：列出所有 A+ 訊號 + 中期 R:R 為正的標的
for m in latest:
    if m.get("signal") == "A+" and (m.get("upside_mid_pct") or 0) > 0:
        print(f'{m["ticker"]}: {m["upside_mid_pct"]:+.1f}% mid upside')
```

### 補完 legacy v12 DD 的 partial dd-meta

```bash
# Step 1: 看哪些 DD 缺哪些欄位
python scripts/validate_dd_meta.py --report

# Step 2: 對單一 DD 手動編輯 dd-meta JSON block（在 HTML <head> 內）
# 補上缺漏欄位（通常是 moat_score / quality_score / price_at_dd /
# upside_short_pct / ai_risk / long_term_confidence）

# Step 3: 重跑驗證確認
python scripts/validate_dd_meta.py --report
```

當所有 v12 DD 通過 strict 驗證後，可在 `.github/workflows/validate_dd_meta.yml`
拿掉 `--report` 旗標，啟用 CI 強制阻擋。

## dd-meta 必填欄位 quick reference

完整定義 + 驗證規則見 `validate_dd_meta.py`。摘要：

```json
{
  "ticker": "STRING",
  "schema": "v12.X",
  "date": "YYYY-MM-DD",
  "price_at_dd": NUMBER,
  "signal": "A+|A|B|C|X",
  "trap": "🟢|🟡|🔴",
  "trap_label": "🟢 非陷阱|🟡 觀察期|🔴 高風險",
  "moat": "S|A|B|C|X",
  "val": "🟢|🟡|🟠|🔴",
  "ma": "✅|🟡|🟠|❌|-",
  "fpe_fy2": NUMBER,
  "pct_5y": 0-100,
  "peg_fy2": NUMBER,
  "upside_short_pct": NUMBER,
  "upside_mid_pct": NUMBER,
  "stress": {"pass": INT, "total": INT},
  "moat_score": 1-10,
  "growth_durability": 1-10,
  "quality_score": 1-10,
  "ai_risk": "🟢|🟡|🔴",
  "long_term_confidence": "高|中|低",
  "verdict": "STRING",
  "oneliner": "≤ 200 chars"
}
```

## 設計決策記錄

- **為什麼選 `<script type="application/json">` 而不是 sidecar `.json` 檔？**
  單一檔案管理；DD HTML 本身自帶 metadata，避免兩檔不同步
- **為什麼不用 `<meta name="...">` 一堆 tag？**
  巢狀結構（如 `stress.pass`/`stress.total`）難表達；數值型別需 cast；字數限制；JSON 是現成 standard
- **為什麼 backfill 後仍 56 個 invalid？**
  舊 v12 DD 的 HTML 樣式不一致，regex 抽不出 7 個欄位（`moat_score / quality_score /
  growth_durability / price_at_dd / upside_short_pct / ai_risk / long_term_confidence`）。
  這些需手動補。**新 DD 由 stock-analyst skill 直接 emit 完整 JSON，不會再有這問題**。
