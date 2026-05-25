---
name: refresh-eps-screener
description: 用新 Koyfin DD_universe_EPS_estimates_YYYYMMDD.xlsx 更新 https://research.investmquest.com/dd-screener/ — 同月內 5/20→5/25 這種 intra-month refresh 會自動保留前一份 snapshot 當 baseline，讓 FY1/FY2/FY3 EPS revision% 可以對照新分析師上修下修；非美股 (TW/JP/HK/KS/CN/CH) 走 FX pipeline 自動換成 local currency 顯示。觸發：用戶說「update eps screener」/「更新 dd-screener」/「DD screener 更新 EPS」/「跑新 Excel 更新 screener」/「refresh EPS estimates」/「{path}.xlsx 更新表格」，或丟下一份 `DD_universe_EPS_estimates_YYYYMMDD.xlsx` 並要 update。
version: v1.0
date: 2026-05-25
---

# Workflow: refresh-eps-screener

當用戶說以上任一觸發語、或直接丟新 `DD_universe_EPS_estimates_YYYYMMDD.xlsx` 路徑要 update，照下列 8 個 step 跑完，**不要中途等用戶確認**（除非命中 §Pre-flight gate 任一條件）。

## Pre-flight gate（命中任一就先問用戶）

- Excel 檔不存在於 user 給的路徑 → 先問 user 正確路徑
- Excel 檔名不符合 `DD_universe_EPS_estimates_YYYYMMDD.xlsx` regex → 問 user 是否要 rename / 是否確實是 DD universe export
- `data/eps-estimates/` 已存在**同一 YYYYMMDD** 的 Excel 且內容不同 → 問 user 是否覆蓋（罕見：同日重新 export）
- `docs/dd-screener/eps-estimates-snapshots/` 沒有任何 `YYYY-MM.json` → 首次部署，跳過 §Step 2 archive，commit 訊息加上 "(initial baseline)"

否則 — 不問，直接跑。

## Step 1 — Detect target month + current Excel snapshot

```bash
# Read new Excel filename YYYYMMDD → derive YYYY-MM
new_xlsx="$1"  # user-provided path or auto-detected from Downloads/
basename=$(basename "$new_xlsx")
# Validate regex
[[ ! "$basename" =~ ^DD_universe_EPS_estimates_([0-9]{8})\.xlsx$ ]] && exit
yyyymmdd="${BASH_REMATCH[1]}"
yyyy_mm="${yyyymmdd:0:4}-${yyyymmdd:4:2}"
```

讀 `docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}.json`（如存在），取其 `snapshot_date` 欄位 = 上一次的 Excel 日期（YYYY-MM-DD）。這就是 prior baseline。

如果該 snapshot 的 `snapshot_date` ≥ 新 Excel 的 YYYYMMDD → 用戶可能跑反方向，**停下確認**。

## Step 2 — Archive prior intra-month snapshot

**這步是整個流程的核心**。若 `2026-05.json` 存在且其 `snapshot_date` < 新 Excel 日期：

```bash
prior_date=$(python3 -c "import json; print(json.load(open('docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}.json'))['snapshot_date'])")
# prior_date = "2026-05-20"
prior_dd="${prior_date: -2}"  # "20"
cp docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}.json \
   docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}-${prior_dd}.json
```

這個 `${yyyy_mm}-${prior_dd}.json` 就是 baseline，會被 `build_dd_screener.py` 的 `_load_prev_month_snapshot` (Step 1 intra-month lookup) 撿到。

## Step 2.5 — Retrofit prior snapshot CAGR if formula changed

如果 prior snapshot 是 **早於 2026-05-25 寫入的**（即可能用舊 TTM→FY+1 CAGR 公式），跑這段把 `eps_cagr_2y` 重算成新 FY1→FY3 forward 公式，否則 `eps2y_revision_pp` 會是 apples-to-oranges 差值（NVDA 會顯示 fake -22pp）：

```python
import json
from pathlib import Path
p = Path(f'docs/dd-screener/eps-estimates-snapshots/{yyyy_mm}-{prior_dd}.json')
d = json.loads(p.read_text())
# Skip if already retrofitted
if d.get('eps_cagr_2y_formula') == 'fy1_fy3_forward':
    pass
else:
    for t, rec in d['tickers'].items():
        fy1 = rec.get('eps_fy_curr') or rec.get('eps_0y')
        fy3 = rec.get('eps_fy3')
        if fy1 and fy3 and fy1 > 0 and fy3 > 0:
            rec['eps_cagr_2y'] = round(((fy3 / fy1) ** 0.5 - 1) * 100, 2)
        else:
            rec['eps_cagr_2y'] = None
    d['eps_cagr_2y_formula'] = 'fy1_fy3_forward'
    d['eps_cagr_2y_retrofit'] = f'auto-retrofit on {YYYY-MM-DD}'
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
```

## Step 3 — Stage the new Excel

```bash
cp "$new_xlsx" data/eps-estimates/
```

`load_eps_estimates_xlsx.find_latest_excel()` 會自動挑日期最大那份 — Excel 命名固定 `DD_universe_EPS_estimates_YYYYMMDD.xlsx`，多份 Excel 共存沒問題。

## Step 4 — Run snapshot

```bash
python3 scripts/snapshot_eps_estimates.py
```

這會寫 `docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}.json`（**覆蓋** prior，但 §Step 2 已把 prior 另存為 `${yyyy_mm}-${prior_dd}.json` baseline，所以沒事）。

snapshot script 會自動：
- xlsx tickers → 直接讀 Excel FY1/FY2/FY3 + 算 `eps_cagr_2y = ((fy3/fy1)^0.5 - 1) × 100`
- 未涵蓋的 ticker（如 6146.T / 6857.T JP 股 — 新 Excel 沒 JP data）→ yfinance fallback
- 失敗 list 印在 stdout — 對照 Excel Notes 看是否合理

## Step 5 — Run build

```bash
python3 scripts/build_dd_screener.py
```

這會：
- 重 build `latest.json` + 6 個 variant `.json` / `.html`（alpha-rank / breakout / bottom-out / earnings-acceleration / entry-state / quality-entry）
- `_load_prev_month_snapshot` 撿到 `${yyyy_mm}-${prior_dd}.json` 當 baseline（log 印 `EPS baseline: intra-month {file}.json (current Excel YYYY-MM-DD)`）
- 對每個 ticker 算 FY1 / FY2 / FY3 revision% vs baseline
- 非美股 ticker（.TW / .T / .HK / .KS / .KQ / .SS / .SZ / .JP）→ FX pipeline 換成 local currency 顯示
- FX 優先 yfinance.earnings_estimate ÷ Excel USD；若 rate-limited fallback yfinance.info.epsCurrentYear ÷ Excel USD

## Step 6 — Spot-check vs Excel Notes

**最重要的 sanity gate**。Excel Notes sheet 第 8 列「Updated EPS vs YYYY-MM-DD」會列 5-10 個 ticker 帶舊→新值。用 build 結果對照：

```python
import json
d = json.load(open('docs/dd-screener/latest.json'))
stocks = {s['ticker']: s for s in d['stocks']}

# 從 Excel Notes 抄出 ticker + 預期 revision%
# 例：「TSM 3.09→3.11」→ expected revision = (3.11/3.09 - 1)*100 = 0.65%
checks = [
    ('NVDA', 6.68),    # 8.38 → 8.94
    ('TSM', 0.65),     # 3.09 → 3.11
    ('RL', 12.61),     # 16.33 → 18.39
    ('MSFT', -0.24),   # 16.85 → 16.81
]
for t, expected in checks:
    actual = stocks[t].get('eps_fy_curr_revision_pct')
    delta = abs(actual - expected)
    status = '✓' if delta < 0.1 else '✗'
    print(f'  {status} {t}: expected {expected}%, got {actual}% (delta {delta:.2f})')
```

任何一個 ✗ → 停下分析（可能 baseline 撈錯 / FX 套錯 / Excel column 順序變了）。

## Step 7 — Spot-check FX conversion

挑 1-2 個 TW ticker 看 FX 有 fire：

```python
for t in ['2330.TW', '2454.TW']:
    s = stocks.get(t, {})
    print(f'{t}: fx={s.get("eps_fx_rate")}, ccy={s.get("eps_display_currency")}, '
          f'fy1_display={s.get("eps_fy_curr")}, fy1_usd_orig={s.get("eps_fy_curr_usd_orig")}')
# Expected: fx ≈ 31.5, ccy=TWD, fy1_display ≈ fy1_usd_orig × 31.5
```

若 fx=None / ccy=USD → yfinance.earnings_estimate **和** yfinance.info 同時 rate-limited。**等 5-10 分鐘 rerun `python3 scripts/build_dd_screener.py`**（snapshot 不用重跑，只是 build 撈不到 FX）。

## Step 8 — Commit + push

只 stage 本次涉及的檔案（**不要 add -A** — 會誤抓其他 session 的 DD/DCA 新檔）：

```bash
git add \
  data/eps-estimates/DD_universe_EPS_estimates_${yyyymmdd}.xlsx \
  docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}.json \
  docs/dd-screener/eps-estimates-snapshots/${yyyy_mm}-${prior_dd}.json \
  docs/dd-screener/latest.json \
  docs/dd-screener/alpha-rank.json docs/dd-screener/alpha-rank.html \
  docs/dd-screener/bottom-out.json docs/dd-screener/bottom-out.html \
  docs/dd-screener/breakout.json docs/dd-screener/breakout.html \
  docs/dd-screener/earnings-acceleration.json docs/dd-screener/earnings-acceleration.html \
  docs/dd-screener/entry-state.json docs/dd-screener/entry-state.html \
  docs/dd-screener/quality-entry.json docs/dd-screener/quality-entry.html

git commit -m "$(cat <<EOF
dd-screener: ${yyyymmdd} Excel + EPS revision baseline ${prior_date}

- Universe: N tickers (xlsx covers X, yfinance fallback Y)
- Revision baseline: ${prior_date} ({age} days prior, intra-month)
- Sanity checks (vs Excel Notes line 8):
  NVDA +6.68% / TSM +0.65% / RL +12.61% / MSFT -0.24% ✓
- TW tickers TWD-converted (fx ≈ 31.5)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push origin main
```

**不需要跑 `update_dd_index.py`** — 此 workflow 不動 `docs/dd/` 或 `docs/dca/`。research 頁的 DD 組合快照與此更新無關。

## 關鍵 invariants（每次 run 都要 hold）

1. **Baseline 不能丟**：`${yyyy_mm}-${prior_dd}.json` 必須在 §Step 4 snapshot overwrite 之前 cp 出來。沒這步等於下次 build 看不到 prior baseline。
2. **CAGR 公式 retrofit**：prior snapshot 若早於 2026-05-25 寫入，必跑 §Step 2.5 retrofit，否則 `eps2y_revision_pp` 是 apples-to-oranges。
3. **Excel 一律假設 USD**：Koyfin export 規範如此（即使 reporting currency 不同，Koyfin 會 USD-translate）。FX pipeline 對 .TW/.T/.HK/.KS 從 yfinance back-compute local currency display；ADRs（如 LVMH→MC、AENA、BESI、RMS）留 USD（ADR 投資人本身就交易 USD）。
4. **Spot-check 不能跳**：§Step 6 是唯一能抓出 Excel column 順序變 / Koyfin export 規範變 / FX pipeline 套錯的 gate。任何 ✗ 不要 commit。
5. **Commit scope tight**：只 add §Step 8 列的 dd-screener bundle。**不要 add docs/dd/** 或 **docs/dca/** 新檔（那些是別 session 的成果，commit 規範另有流程）。
