# `decision_inputs`｜`scripts/dd_decision.py` 輸入契約（WP1b 交付物）

> 本檔定義 `dd_decision.py`（v16 決策矩陣機械路由器）的輸入 JSON 形狀。
> **權威來源仍是** `.claude/skills/stock-analyst/references/decision-layer.md`
> 的決策矩陣（rows 1-10）——本檔只是「這個腳本吃什麼欄位」的接線圖，欄名與
> 型別以本檔為準，但**判斷語意一律以 decision-layer.md 原文為準**，兩者衝突
> 時本檔是翻譯錯誤，不是新規則。WP1c（judgment.json 完整 schema）會把
> `decision_inputs` 收斂為 `judgment.json.decision_inputs` 子樹，欄名沿用本檔。

## 1. 整體形狀

```json
{ "decision_inputs": { ... 見下表 ... } }
```

`dd_decision.py run` 也接受直接餵 `decision_inputs` 本體（不包一層 `"decision_inputs"` key）——偵測邏輯：優先讀 `data["decision_inputs"]`，沒有就把整個檔案當 `decision_inputs`。

## 2. 欄位表

### 2.1 直接來自 dd-meta 的欄（v15 已在生產，型別/enum 見 `references/dd-meta-schema.md`）

| 欄名 | 型別 | dd-meta 來源欄名 | 備註 |
|---|---|---|---|
| `signal` | str enum `A+`\|`A`\|`B`\|`C`\|`X` | `signal` | QC-31 |
| `trap` | str enum 🟢/🟡/🔴 | `trap` | 決策矩陣 rows 1-10 未直接消費此欄（QC-31 用），但仍收進契約供未來擴充/audit 追溯 |
| `val` | str enum 🟢/🟡/🟠/🔴 | `val` | 附錄 A §D。**已知限制**：dd-meta 只存機械讀數，不含 §11 4b.1「分母爭議檢查」是否已判定此燈失效——見 §4 |
| `ma` | str enum 🟢/✅/🟡/🟠/❌/- | `ma` | 附錄 A §F |
| `runway_post_y5` | str enum 🟢/🟡/🔴 | `runway_post_y5` | §6.A'' |
| `moat_trend` | str enum ↑/→/↓ | `moat_trend` | §5 權威 |
| `moat` | str enum S/A/B/C/X | `moat`（**dd-meta 實際欄名確認為 `moat`，不是 `moat_grade`**——見 `dd-meta-schema.md` 與 `validate_dd_meta.py` `ENUM_FIELDS["moat"]`） | 決策矩陣 row 3／row 8b 用「moat 等級」時讀此欄 |
| `capalloc_grade` | str enum `A`\|`B`\|`C`，或缺 | `capalloc_grade`（選填欄，DD 未提供時整欄不存在→視為 N/A 不觸發 row 7b） | §9 |
| `archetype` | str（QC-43 七類 enum，或 blend 字串如「品質複利成長（primary）＋消費循環（secondary）」） | `archetype`（選填） | row 8b 判斷是否為循環子型時用 `CYCLICAL_RE = 循環\|商品\|EMS/ODM` 對此欄做 regex search，非精確 enum match（blend 字串會夾帶其他字） |
| `cycle_position` | str enum（`深谷投降`/`早循環`/`中循環`/`晚循環`/`過熱頂部`，或缺） | `cycle_position`（選填，非循環 archetype 不填） | row 8b 用 |
| `cycle_verdict` | str enum（`右側可追蹤`/`等回踩`/`頂部觀望`/`未觸發`，或缺） | `cycle_verdict`（選填） | 決策矩陣 rows 1-10 本身不消費此欄（附錄 B 自己的輸出，非矩陣輸入條件），收進契約供 audit 對照 |
| `asym_ratio` | number 或缺 | `asym_ratio`（選填） | 矩陣不直接消費（AR 是 row 8a 的「參考資訊，非資格條件」），收進契約供 audit 顯示 |
| `irr_base_pct` | number 或缺 | `irr_base_pct`（選填） | 同上，audit 用 |
| `ev5y_pct` | number | `ev5y_pct` | 同上，audit 用 |
| `price_at_dd` | number | `price_at_dd` | 同上，audit 用 |

### 2.2 dd-meta 沒有、v16 判斷物必填的欄（`null` = 未提供）

| 欄名 | 型別 | 對應矩陣條件 | 缺值時的保守方向 |
|---|---|---|---|
| `thesis_irreconcilable` | bool 或 `null` | row 2（Hard Veto）：§11 強制裁決 thesis 不可調和不成立 | **`null` → 視為不觸發**（不 manufacture 一個查不到證據的否決；缺值不得升級成迴避） |
| `valuation_dependent` | bool 或 `null` | row 7a（Soft Veto）：§10.6 估值依賴型 | `null` → 視為不觸發（row 7a 整條跳過，記 input_gap） |
| `market_wrong_reason_given` | bool 或 `null` | row 7a：§11 是否給出「市場錯在哪」 | 與 `valuation_dependent` 任一為 `null` → row 7a 整條跳過 |
| `week26_return_pct` | number 或 `null` | row 8a：26 週漲幅位置閘（<100 放行／>150 擋下／100-150 邊界帶裁量） | `null` → row 8a 視為無法確認，**不放行**（8a 是升級路徑，缺證據不得升級，對稱 QC-48 fail-safe 方向） |
| `momentum_overheated` | bool 或 `null` | row 5（節奏調節，非裁決閘）：RSI>70 或 4 週漂移>+10% | `null` → 視為不觸發（不加 pacing 註記） |
| `cycle_gates_pass` | bool 或 `null` | row 8b：QC-42 反動能五閘是否全過 | `null` → row 8b 視為無法確認，不放行（8b 同樣是升級路徑） |
| `consensus_rev_3m_pct` | number 或 `null` | QC-50（觀望裁決後的錯過成本反向 critic）觸發條件之二：FY1/FY2 共識近 3 月上修 ≥ +10% | `null` → 不觸發 `requires_critic` 的 QC-50 建議；**注意 QC-50 還有另一觸發條件**（前次同 ticker 觀望/迴避且 to-date 報酬 >+30%）**不在本契約內**（需要 q.py 歷史查詢，非單份報告的靜態輸入），本腳本只能用 `consensus_rev_3m_pct` 這一半 |

### 2.3 本腳本另外接受的選填欄（不在 v16 設計稿 §3.2 原始清單，是 WP1b 實作時發現必要的補充）

| 欄名 | 型別 | 用途 |
|---|---|---|
| `role_hint` | str（`核心`/`衛星`/`追蹤`/`不持有`）或 `null` | 決策矩陣 rows 1-10 只判定 **verdict**，不判定 **role**——14a 的角色分配（尤其 baseline rows 8/9/9b/10 的「核心 vs 衛星」、觀望 rows 的「追蹤 vs 衛星（既有持倉例外）」）依賴矩陣以外的資訊（是否為既有持倉、持有人偏好）。提供 `role_hint` 時腳本直接採用（優先序最高，蓋過 §2.4 的三個覆寫層對 role 的任何調整）；缺省時套用文件化的預設啟發式（見 §3）。**這不是矩陣的一部分，是呈現層需要的額外決策**，之所以放進 `decision_inputs` 是因為目前沒有更好的居所——WP1c 若把 `judgment.json.thesis`/`prior_dd` 結構化後，`role_hint` 應改為由 orchestrator 從 `prior_dd.role`／持倉狀態算出，不再是人工欄。 |

### 2.4 矩陣「之前／之後」的覆寫層欄位（2026-09 coordinator 追加，仍不改矩陣 rows 1-10 語意）

**覆蓋層順序（`evaluate()` 執行順序，見該函式 docstring）：§11 4b.1 分母爭議（矩陣求值本身的一部分，內建在 `_evaluate_matrix` 的 baseline 段）→ 矩陣 rows 1-10 → QC-49 裁決 hysteresis（矩陣輸出之後）→ held_now role 例外（最後，只影響 role 不影響 verdict）。**

| 欄名 | 型別 | 對應矩陣條件 | 缺值時的保守方向 |
|---|---|---|---|
| `val_denominator_disputed` | bool 或 `null` | §11 4b.1 分母爭議檢查成立時，`val` 燈機械讀數判定不可用——baseline rows 8/9/9b/10 的估值條件視為不可判，直接落 row8 觀望（`row_hit="8(val爭議)"`）。**只影響 baseline 8/9/9b/10**，不影響 row 8a 的 val 資格檢查（8a 本就要求 val 已偏貴，语意不同，coordinator 只要求覆寫 baseline） | `null` → 視為不觸發（沿用 `val` 機械讀數走正常矩陣） |
| `qc49_inherit_prior` | bool 或 `null` | QC-49：90 天內翻面且引不出前次已發火觸發器時承繼前次裁決。**本腳本不做觸發器查證**——這個 bool 是「已經查證過、確定引不出觸發器」的既成事實輸入，`true` 時搭配 `prior_verdict` 才會生效 | `null` → 視為不套用（維持矩陣機械輸出）——不 manufacture 一個「查無觸發器」的結論 |
| `prior_verdict` | str enum `進場`/`觀望`/`迴避` 或 `null` | 與 `qc49_inherit_prior` 搭配：`qc49_inherit_prior=true` 且 `prior_verdict` 與矩陣機械輸出方向不同時，最終 `verdict = prior_verdict`，`row_hit` 附註 `→QC-49(prior_verdict)` | `null` → 即使 `qc49_inherit_prior=true` 也不套用（無法承繼一個不存在的裁決），記 input_gap |
| `prior_role` | str（`核心`/`衛星`/`追蹤`/`不持有`）或 `null` | 供 QC-49 覆寫與 held_now 例外共用：QC-49 生效時 `role = prior_role`（缺則退回 §3 啟發式，用**新** verdict 重算）；`held_now=true` 時 `role = prior_role`（缺則記 gap、維持預設） | `null` → QC-49 分支退回角色啟發式；held_now 分支維持預設角色並記 gap |
| `held_now` | bool 或 `null` | 14a：「觀望 → 追蹤（既有持倉等觸發則衛星）」——最終 `verdict="觀望"` 時，若 `held_now=true` 則 `role` 沿用 `prior_role` 而非預設的「追蹤」（僅在未提供 `role_hint` 時生效） | `null` → 視為不觸發，`verdict="觀望"` 時 role 維持預設（追蹤，或 QC-49 已設定的角色） |

**已知不完整**：`held_now`/`prior_role` 機制只覆蓋「因既有持倉延續而給衛星/核心角色」這一種模式（`DD_MRVL_20260831.html` 案例）。backtest 中發現另一種**不同機制**也會讓觀望裁決得到衛星角色——`DD_TPR_20260806.html` 的衛星角色來自「§5.R 判定為現金產生器而非複利機器，不符核心持倉標準」的**候選品質分類**，與是否現持有無關，本次追加**不處理**這個模式（backtest 中仍是一個已知、文件化的 role mismatch，不影響 verdict 比對）。

## 3. Role 預設啟發式（`role_hint` 缺省時）

矩陣文字（decision-layer.md §14a）明確規定的部分：
- Hard Veto（迴避）→ `不持有`
- row 8a（爆發候選）→ `衛星`（14a 明文「禁核心」）
- row 8b（循環衛星）→ `衛星`（14a 明文「禁核心」）

矩陣文字**未**明確規定、本腳本補的啟發式（**非權威，僅預設值，`role_hint` 應優先，其次是 §2.4 的 QC-49/`held_now` 覆寫**）：
- Soft Veto 生效（觀望，rows 6/7/7a）／baseline row 8（觀望，估值卡關）／`val_denominator_disputed` 落 row8 → 預設 `追蹤`，除非 `held_now=true` 且 `prior_role` 有值（§2.4）→ 沿用 `prior_role`
- QC-49 生效時（§2.4）→ `role = prior_role`；`prior_role` 缺則退回本節啟發式，但用**覆寫後的新 verdict**（而非矩陣機械輸出）重算——backtest 中 `DD_SBUX_20260901.html` 正是此路徑：`prior_role` 未能從文字推斷，退回「以新 verdict=進場、signal=B、moat_trend=→ 算出 `衛星`」，結果與 dd-meta 一致
- baseline rows 9/9b/10（進場，且未被 QC-49 覆寫）→ `signal ∈ {A, A+}` 且 `moat_trend ≠ ↓` 時預設 `核心`，否則 `衛星`。**此為 backtest 回填得出的觀察式**（v15 corpus 31 檔中，baseline 進場的角色高度與 signal 相關：A/A+→核心是常態，B→衛星是常態；AVGO 是唯一反例，因 moat_trend=↓ 拉低角色但矩陣本身放行進場——啟發式已把這條反例內建），**不是決策矩陣條文**，只是沒有 `role_hint` 時的合理猜測。

**已知不完整**：`held_now`/`prior_role` 覆蓋不了所有「觀望但角色非追蹤」案例——見 §2.4 末段的 `DD_TPR_20260806.html` 反例（候選品質分類導致的衛星角色，與現持有與否無關）。

## 4. 已知範圍外（`dd_decision.py` 刻意不做的部分）

`check-all --infer-from-html` 對 31 份現行 v15 DD 回測：**30/31 dca_verdict 相同**（`check-all` 不開 `--infer-from-html` 時維持 27/31——§2.4 三個新欄位在 dd-meta 裡沒有對應來源，plain check-all 沒有管道取得它們，只有從報告正文推斷才拿得到，此為預期行為，非退步）。

2026-09 追加 §2.4 三組欄位（`val_denominator_disputed`／`qc49_inherit_prior`+`prior_verdict`+`prior_role`／`held_now`）後，原本 4 個 mismatch 中的 3 個（MELI／MRVL／SBUX）已可用這三組欄位機械重現最終裁決（見 `backtest_report.md` 逐案例核對，三案例都用報告自己寫出的「矩陣機械輸出＝X」文字核對過，證明腳本矩陣運算本身無誤，差異純粹是覆寫層的輸入）。剩下 1 個**刻意不解決**：

- **報告本身脫離矩陣字面（`DD_5398KL_20260811.html`）**——`signal="X"` 依 decision-layer.md row 1 文字應無條件迴避，但報告在 §13 明寫「無詐欺、無存續危機……故收斂於觀望而非迴避」，等於對 X 的觸發原因做了子類判斷（獲利品質崩壞 vs 詐欺/存續危機）並只對後者維持 Hard Veto。**decision-layer.md 原文沒有這個子類劃分**，這是報告作者的裁量，不是本腳本的翻譯錯誤（本腳本忠實照 row 1 字面翻譯：`signal=X` 無條件迴避，無例外）。**不得為了湊 31/31 給 row 1 加一個矩陣文字沒有的例外**——這正是「翻譯不是修訂」鐵律要擋的事。已提名進 `knowledge/rule_ledger.md` 2026-10 校準輪審計範圍（見 §5 矛盾點 #1），由持有人裁定是否要把這個子類劃分正式寫進 decision-layer.md row 1，裁定前腳本維持現狀。

## 5. `dd_decision.py` 發現的矩陣文字歧義（只列不改，供 2026-10 校準輪參考）

1. **row 1「signal = X」是否應區分 X 的觸發原因**——QC-31 定義 X 有四種觸發原因（重大治理問題/舞弊、結構性產業衰退、獲利品質崩壞、〔隱含〕陷阱🔴或AI風險🔴等 C 級以上失敗），decision-layer.md row 1 對這四種一視同仁「signal=X → 迴避」，但實務上（見 `DD_5398KL_20260811.html`）作者會對「獲利品質崩壞但無詐欺/存續危機」的 X 從輕發落到觀望。矩陣文字目前不支援這個區分。
2. **rows 9 與 10 的優先序未明文**——row 9（`signal≥B`）與 row 10（`signal≥A`）在 `signal∈{A,A+}` 且其餘條件相同時同時滿足，兩者輸出的 dd-meta `dca_verdict` 皆為「進場」故不影響裁決，但 row_hit 標籤該取哪個未明文規定。本腳本採「更具體者優先」（10 > 9b > 9），依據是 `DD_NVDA_20260831.html` 自身正文寫「→row10進場」（signal=A+ 時自稱 row10 而非 row9），與此推論一致，但矩陣表格本身沒有寫「9/10 互斥或以何者為準」這條規則。
3. **row 9b 在 dd-meta `dca_verdict` enum 中沒有獨立值**——`validate_dd_meta.py` 的 `V13_ENUM_FIELDS["dca_verdict"]` 只有 5 個值（進場／進場·條件式〔循環衛星〕／進場·條件式〔爆發候選〕／觀望／迴避），row 9b「進場·條件式（長波段佈局）」不在列，落地時一律降級寫成純「進場」（`DD_UBER_20260808.html`／`DD_CRM_20260831.html` 皆如此），row 9b 的條件式語意只活在 §13a 執行語（分批進場）裡，dd-meta 欄位本身分不出「row9 的一次建倉」與「row9b 的條件式分批」。這不影響本 WP 的 backtest（因為兩者 dd-meta 值相同），但下游若想機器讀出「這是不是條件式進場」會讀不到。
4. **§13a「觀望→追蹤（既有持倉等觸發則衛星）」的「等觸發」語意不只一種**——2026-09 追加 `held_now`/`prior_role` 只精確對映其中一種（既有持倉延續，`DD_MRVL_20260831.html`）；backtest 發現至少還有一種**不同機制**同樣讓觀望裁決落衛星角色（`DD_TPR_20260806.html`：候選品質分類「現金產生器而非複利機器，不符核心持倉標準」，與是否現持有無關）。矩陣文字的「等觸發」三字目前概括了至少兩種不同判準，未展開列舉。
5. **§13a「進場」角色（核心 vs 衛星）沒有矩陣層級的判定規則**——本檔 §3 的「signal∈{A,A+}→核心」啟發式是 backtest 回填的觀察式，decision-layer.md 本身在 rows 8/9/9b/10 只判定 verdict，14a 表格也只說「全部欄位完整填寫」，沒有一條規則指定核心/衛星的判準（對照 8a/8b 明文規定「衛星（禁核心）」）。

## 6. 型別備忘（給 WP1c 寫 judgment.json 用）

- 所有 emoji enum（`val`/`ma`/`trap`/`runway_post_y5`）必須是純 emoji，不得帶文字前綴（同 `dd-meta-schema.md` 既有規則）。
- `moat_trend` 必須是單一 Unicode 箭頭（↑/→/↓）。
- bool 欄一律三態（`true`/`false`/`null`），**不可用字串 `"unknown"` 代替 `null`**——`dd_decision.py` 的 gap 偵測邏輯是 `is None` 判斷，字串 `"unknown"` 會被當成 truthy 值誤判。
