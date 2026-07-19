# stock-analyst v14.12 — dd-meta-schema.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

### QC-32｜dd-meta JSON 硬性 schema（v14.7，validator 強制）

`scripts/validate_dd_meta.py` 對所有 v12/v13 DD 在 commit 階段強制檢查;違規 → push 失敗。LLM 必須在生成 HTML 前自我驗證 dd-meta JSON 區塊。

**v13 canonical schema（22 個 v12 必填欄 + 5 個 v13 必填欄 + 20 個選填欄）**：

```json
{
  "ticker": "NVDA",
  "schema": "v14.12",
  "date": "2026-06-21",
  "price_at_dd": 223.47,
  "signal": "A+",
  "trap": "🟢",
  "trap_label": "🟢 非陷阱",
  "moat": "S",
  "val": "🟢",
  "ma": "✅",
  "fpe_fy2": 19.21,
  "pct_5y": 22.0,
  "peg_fy2": 0.69,
  "upside_short_pct": 31.0,
  "upside_mid_pct": 66.0,
  "stress": {"pass": 2, "total": 2},
  "moat_score": 10.0,
  "growth_durability": 10.0,
  "quality_score": 10.0,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "A+",
  "oneliner": "≤ 200 chars 壓縮敘述",

  "dca_verdict": "進場",
  "dca_role": "核心",
  "moat_trend": "↑",
  "runway_post_y5": "🟢",
  "ev5y_pct": 88.0,
  "irr_base_pct": 13.5,
  "max_dd_pct": -45.0,
  "asym_ratio": 6.2,
  "bull_5y_price": 610.0,
  "bear_5y_price": 165.0,
  "p_bull_pct": 30.0,
  "p_bear_pct": 25.0,
  "archetype": "品質複利成長",
  "rearm_trigger": "估值回落至 Fwd PE 21x（$545）或 N2 量產如期",

  "catalysts": [{"date": "2026-09-10", "type": "product", "event": "Rubin CPX 出貨節點", "impact": "高", "watch": "若延後一季 → §11.5 Bull 機率下修"}],
  "base_eps_path": {"FY26": 4.95, "FY27": 6.00, "FY28": 7.25},
  "fy_end_month": 1,
  "eps_basis": "non-gaap-usd",

  "kill_metrics": [
    {"metric": "AI 加速器訓練份額", "bear_threshold": "跌破 65%（當前 ~73%）→ 減半", "window": "", "last_status": "ok"},
    {"metric": "DC 營收年成長", "bear_threshold": "掉到 < 6% 連兩季 → 減碼", "window": "2 季", "last_status": "ok"},
    {"metric": "CUDA 護城河", "bear_threshold": "被 custom ASIC 結構繞過（training 崩）→ 清倉", "window": ""}
  ]
}
```

**v12 沿用 22 欄的 Enum 白名單**（不變，validator 不放過）：
- `signal` / `verdict`：`A+` | `A` | `B` | `C` | `X`
- `moat`：`S` | `A` | `B` | `C` | `X`（**字母**，不是數字）
- `trap` / `ai_risk`：`🟢` | `🟡` | `🔴`（純 emoji）
- `val`：`🟢` | `🟡` | `🟠` | `🔴`
- `ma`：`🟢` | `✅` | `🟡` | `🟠` | `❌` | `-`
- `long_term_confidence`：`高` | `中` | `低`（單字）
- `growth_durability` / `moat_score` / `quality_score`：**number 1-10**

**v13 新增 5 個必填欄（schema 為 v13.x ∪ v14.x 時 validator 強制）+ Enum**：
- `dca_verdict`：`進場` | `觀望` | `迴避`（取自 §14 統一裁決，與頁首儀表板 + §14 裁決晶片三處一致）
- `dca_role`：`核心` | `衛星` | `追蹤` | `不持有`（v14.12 四值稅制，2026-07-10 持有人拍板「大道至簡」；取自 §14a，對齊 `aggregate_dca_stats.py` CATEGORY_ORDER）。**legacy 值**（`核心持倉`/`條件式核心持倉`/`衛星持倉`/`條件式衛星持倉`/`投機部位`/`不持有/迴避`/`候選/追蹤池`）僅為既有報告 dual-read 保留——新報告禁用，「條件式」語意一律改由 §14a 執行語承載
- `moat_trend`：`↑` | `→` | `↓`（**單一 Unicode 箭頭**，取自 §7 權威護城河趨勢;禁止寫「持平」「holding」等文字）
- `runway_post_y5`：`🟢` | `🟡` | `🔴`（取自 §6 Y5 後跑道）
- `ev5y_pct`：**number**（取自 §11.5 的 **5Y 累積機率加權期望值 %**，**不是**年化 IRR;下游 `compute_dca_irr` 會自行年化）

**v13 選填欄（present 時才驗型）**：
- `irr_base_pct`：number（§11.5/11.6 Base case 年化 IRR %）
- `max_dd_pct`：number（§13c Max DD 範圍取下界，負數，例 −45.0）
- `asym_ratio`：number（v14.3;§11.5 不對稱比 AR，1 位小數;Bear 5Y% ≥ 0 時省略此欄）
- `bull_5y_price` / `bear_5y_price`：number（v14.3 F4;§11.5 Bull/Bear 5Y 目標價，AR Live 掛單輸入）
- `p_bull_pct` / `p_bear_pct`：number（v14.3 F4;§11.5 Bull/Bear 機率 %，與 asym_ratio 同源）
- `catalysts`：list（2026-07-05 T-minus 鏈;§1/§15 已寫入的非財報 catalyst 日程，3-6 條）
- `base_eps_path`：dict（2026-07-05 T-minus 鏈;§6.I Base-case build 的 FY EPS 終值）
- `fy_end_month`：int（2026-07-05 T-minus 鏈;會計年度截止月 1-12）
- `eps_basis`：str（2026-07-05 T-minus 鏈;`{gaap|non-gaap}-{幣別小寫}`）
- `endo_growth_ceiling`：number（§6.D 內生成長天花板 %，供 §11.6 IRR sanity check;既有欄，v14.5 補登記）
- `capalloc_grade`：str（§10 資本配置等級 `A`｜`B`｜`C`，供 §14 row 7b;既有欄，v14.5 補登記）
- `moat_execution` / `moat_pricing_power`：number 1-10（§7 二維護城河 sub-scores;既有欄，v14.5 補登記）
- `upside_5y_pct`：number（§11.5 5Y 目標價 upside %，QC-36 四處一致;既有欄，v14.5 補登記）
- `archetype`：str（v14.5;QC-43 判定的 primary archetype，7 類 enum 之一，格式照 QC-43 詞彙;三軌路由需要它——grp_route 現以 moat 分軌，分不出衛星結構 vs 衛星循環）
- `rearm_trigger`：str ≤120 字（v14.5;§14a 觀望分支「觸發條件:___」的機器可讀版——在等什麼:事件／估值門檻／回檔位。觀望裁決建議填，soft，不進 validator 必填）
- `cycle_position`：str（v14.5;附錄 B B.1 循環位置 `深谷投降`｜`早循環`｜`中循環`｜`晚循環`｜`過熱頂部`;非循環 archetype 不填）
- `cycle_verdict`：str（v14.5;附錄 B B.3 `右側可追蹤`｜`等回踩`｜`頂部觀望`｜`未觸發`;非循環 archetype 不填）
- `industry_clock_phase`：str enum `I`｜`II`｜`III`｜`IV`（§9 產業時鐘，v14.12 全 archetype 必答;與 cycle_position 分工——那是循環股自身位置，本欄是產業層時鐘）
- `kill_metrics`：list（P2，2026-07-19;結構化證偽表——把 §14b 減碼／清倉條件 + §15 複審觸發抽成機器可讀條目，供市場偵測器 kill-watch 監控。**選填不阻斷**，但新 DD、**尤其裁決＝進場者，應填 3–5 條**。與 ID 的 `kill_metrics[]` 同結構;詳見下方「結構化證偽表」小節）

**常見 alias 錯誤**（沿用 v12，照 canonical 名稱，禁用別名）：`schema_version`→`schema`、`report_date`→`date`、`current_price`→`price_at_dd`、`peg`/`peg_3y`→`peg_fy2`、`fwd_pe`→`fpe_fy2`、`fwd_pe_5y_percentile`→`pct_5y`、`val_gate`→`val`、`ma_status`→`ma`;省略 `verdict`/`trap_label` 必補;帶文字 emoji（`🟢 受益`）→ 純 emoji;`中高`→`中`/`高` 擇一。**v13 新增 alias 警示**：`role`→`dca_role`、`verdict_human`→`dca_verdict`、`ev_5y`/`ev_pct`→`ev5y_pct`、`moat_arrow`→`moat_trend`、`runway`→`runway_post_y5`、`ar`/`asymmetry_ratio`→`asym_ratio`。

**生成 HTML 前自驗 checklist**（在輸出 JSON 前 LLM 心裡跑一遍）：
1. 22 個 v12 required field 名稱對得上 canonical
2. **5 個 v13 required field（`dca_verdict` / `dca_role` / `moat_trend` / `runway_post_y5` / `ev5y_pct`）全部存在**
3. 所有 enum 欄位值在白名單內（含 v13 五欄的 enum）
4. number 欄位是 int/float 不是 string / emoji（含 `ev5y_pct` / `irr_base_pct` / `max_dd_pct` / `asym_ratio`）
5. `moat_trend` 是單一箭頭 ↑/→/↓（非文字）
6. `dca_verdict` 與頁首儀表板 + §14 裁決晶片三處完全一致
7. `oneliner` ≤ 200 chars
8. `schema` = `v14.12`，且 HTML `<head>` 有 `<meta name="dd-schema-version" content="v14.12">`
9. `ev5y_pct` 是 5Y **累積** EV%（不是年化 IRR）

**JSON 字串內禁止 HTML**：嚴禁 `<a>`/`<strong>`/`<br>` 嵌入 JSON value（引號未跳脫會 parse error）;跨 ID 引用寫純文字檔名;換行用 `\n` 或全形分號 `；`。

**生成後自驗腳本**（HTML 寫完後跑一次）：
```bash
python3 -c "import json,re; t=open('docs/dd/DD_X_YYYYMMDD.html').read(); m=re.search(r'<script id=\"dd-meta\"[^>]*>(.*?)</script>', t, re.DOTALL); d=json.loads(m.group(1)); assert d['schema'].startswith(('v13','v14')); [d[k] for k in ('dca_verdict','dca_role','moat_trend','runway_post_y5','ev5y_pct')]; assert len(d['oneliner'])<=200"
python3 scripts/validate_dd_meta.py --report   # 確認 v13 欄位 + enum 全綠
```

#### T-minus 鏈選填欄（2026-07-05 新增）

四個選填欄（`catalysts` / `base_eps_path` / `fy_end_month` / `eps_basis`），additive-optional，validator 只驗型不驗形狀（跟 F4 群同級，不 bump schema）。落底稿規則:

- **`catalysts`**（list，3-6 條）：只收 §1 最關鍵監測指標表／§15 復審觸發表**已寫入**的、有明確日期的非財報事件。
  - `type` enum:`product` | `regulatory` | `capacity` | `guidance` | `macro` | `other`（**不含 `earnings`**——財報日由下游 yfinance 動態供給，不落底稿）。
  - `impact`:`高` | `中` | `低`。
  - `watch`:一句話寫「若怎樣 → 對 §11.5 情境的影響」。
  - 沒有合格事件就**整欄省略**（honest-fail，禁止為填欄位發明催化劑）。
  - 日期只到月/季精度時,`date` 填該期末日並加選填 `"date_precision": "month" | "quarter"`。
- **`base_eps_path`**（dict）：直接抄 §6.I Base-case build 的 FY EPS 終值,key 用 §6.I 原生 FY 標籤,**只填明文寫出的年份**（禁止內插）;幣別跟 DD 計價幣別走。
- **`fy_end_month`**（int，1-12）：會計年度截止月,從報告自身的季度標籤推（如「Q1 FY2026（2026-05-07 公布）」→ 1 月截止）;無法確定就省略。
- **`eps_basis`**（str）：格式 `{gaap|non-gaap}-{幣別小寫}`（如 `non-gaap-usd`、`gaap-twd`）,依 §6.I 用的 EPS 口徑判定。

**提醒**:yfinance 批量採集抓到的「下次財報日期」繼續**只進 §15，不進 dd-meta**（動態資料不落底稿）。

#### 結構化證偽表 `kill_metrics[]`（P2，2026-07-19 新增）

把散文裡的證偽／減碼／清倉條件抽成機器可讀條目,讓市場偵測器 kill-watch（`docs/detective/data/kill_registry.json` → `scripts/build_kill_watch.py`）能持續盯這檔的 thesis 是否被打破。與產業 ID 的 `kill_metrics[]` 同結構（`scripts/validate_id_meta.py`），validator 對 DD 端**只驗形狀、永遠選填、不設最少條數**——既有 v13/v14 全庫不受影響。

**何時填**:新 DD 都建議填;**裁決＝進場（`dca_verdict: "進場"`）者應填 3–5 條**——進場就等於押注 thesis，必須同時交出「什麼會證明我錯」。來源限本報告 §14b（加碼與減碼條件）、§15（複審觸發與保質期）、§11.5 Bear 情境已寫出的觸發點。

每條欄位（與 ID 端 byte 對齊）:
- `metric`（str ≤120，必填）：被監測量的短標籤，如 `"AI 加速器訓練份額"`。
- `bear_threshold`（str ≤120，必填）：證偽水位＋方向＋當前值，如 `"跌破 65%（當前 ~73%）→ 減半"`。可量化的把數字寫進來;純質性的直接寫結構性事件。
- `window`（str ≤60，必填）：報告給的時間窗，如 `"下次財報 ~2026-08-26"`、`"2 季"`;沒有就填 `""`。
- `source`（str ≤120，選填）：出處／series 提示。
- `last_status`（enum，選填）：`ok`｜`warning`｜`triggered`｜`unknown`。

**紀律**:每條必須來自報告原文寫過的觸發條件,**禁止為填欄位發明新的證偽門檻**（與 catalysts 的 honest-fail 同規）。可量化就給明確數字＋方向;純質性（如「CUDA 護城河被結構繞過」）照寫,不硬湊數字。寧缺勿造——3 條紮實勝過 5 條注水。

