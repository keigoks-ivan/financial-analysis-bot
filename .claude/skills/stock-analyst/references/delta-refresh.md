# stock-analyst v15.0 — delta-refresh.md（條件載入 reference）

> 例行複審的 **delta 模式**：不重寫報告，只重驗假設。載入時點見 SKILL.md 條件載入路由表與【執行協議】的 Refresh 路由段。kill condition 已登記 `knowledge/rule_ledger.md`（2026-08-07 兩條）。
>
> **存在理由**：一份全套 DD 實測 620–645k tokens，而例行複審多數時候的產出是「三個核心假設仍成立、數字更新、裁決維持」。delta 把複審收斂成「假設表重驗 × 漂移分級 × 維持或升級」，**研究深度不是被砍，是被導向真正變動的那一面**；一旦發現實質漂移立刻中止升級全套，不做「省一半的 DD」。

---

## 一、資格閘（逐項判；任一不過 → 全套重跑）

| # | 閘 | 判法 |
|---|---|---|
| 1 | **schema 必須是 v15** | `grep -c '"schema": *"v15' {舊檔}` ≥1。legacy v12/v13/v14 → 全套並順勢升 v15（章序／§5.R／篇幅帶都要改，本質是新報告） |
| 2 | **例行複審，非事件驅動** | 用戶因具體事件（財報暴雷／併購／法規裁定／CEO 更迭／guidance 撤回）要求重看 ＝ 事件驅動 → 全套 |
| 3 | **距上次報告 ≥45 天** | 以檔名日期戳算，不信 INDEX。<45 天＝方法論 churn，回報「無須重跑」而非產 delta |
| 4 | **上次裁決非翻面邊界檔** | 前份 §13／§11 自陳接近 QC-49/QC-50 邊界（「差一點就進場」「傾向翻面但依 QC-49 承繼」「QC-50 建議升級未採納」）→ 全套 |
| 5 | **連續 delta ≤2 次，且距上次全套 ≤9 個月** | 從版本修訂紀錄數 delta 標記。超過任一 → 強制全套（Part I 的產業與護城河判斷本來就會過期，而 delta 不更新那一層） |
| 6 | **非「升 opus writer 四情境」** | repo CLAUDE.md：①多文獻主張漂移 ②裁決可能翻面 ③特殊 archetype 首建（金融／轉機／循環）④核心持倉年度大修 → 全套 |
| 7 | **用戶未明示全套** | 「全套」「重寫」「重跑完整 DD」→ 全套 |

**出口只有兩個**：`維持（delta）` 或 `升級全套`。**delta 內嚴禁翻面裁決**——翻面是判斷級變化，必須有全套研究支撐。**Writer 模型**：sonnet（預設道）；delta 的產出是對帳與數字刷新，不是新判斷。

---

## 二、執行流程

### 步驟 1｜採集數字包
照 `data-collection.md` 既有模板 spawn 一個 sonnet 採集 agent，取回結構化數字包（≤6KB）。**不簡化派工單**——delta 的價值全建立在「現值是真的」上，採集是唯一不能省的一環。

### 步驟 2｜區段擷取讀舊檔（QC-17 機制，嚴禁整檔 Read）
用 `grep -n` 定位 ＋ `sed -n '起,迄p'` 取段：

| 取什麼 | 用途 |
|---|---|
| §2.B 假設表 H1/H2/H3（含數字門檻、漂移觸發欄） | 步驟 3 逐項對現值 |
| §2.C 風險 R1/R2/R3（警戒閾值欄）＋§2.F Single Thing | 步驟 3 觸發判定 |
| §1 最關鍵監測指標表 | 現值刷新 |
| §13 裁決晶片＋倉位角色＋`rearm_trigger` | 維持／升級判定的基準 |
| §14 複審觸發表＋保質期 | 步驟 6 順延 |
| 版本修訂紀錄＋【假設驗證對照】（若有） | 數 delta 次數、append |
| dd-meta JSON `<script>` 區塊 | 欄位刷新來源 |

**禁止讀取**：§3–§7 敘事層、§10 舊估值推導、§12 全文——delta 不重寫那些，讀進來只是付 token。

### 步驟 3｜逐項對現值
- **H1/H2/H3**：各判 `成立／弱化／破壞`，判準走 **QC-35 漂移分級**（2Y／5Y／10Y 各自的削弱與反轉門檻，禁止同一閾值套所有時間軸）。每一判定必須落在 sourced 數字上，禁止「大致上仍成立」這種無錨句。
- **R1/R2/R3 與 §2.F**：逐條判「已觸發／未觸發」，對照原報告寫下的警戒閾值原文，不重新定義閾值。
- **§1 監測指標表**：三項現值全部刷新，標 as-of。

### 步驟 4｜消化新一季財報（有才做）
只重寫 §8 該節（beat/miss ＋ guidance 變化，≤3KB），關鍵數字**必須回驗 H1/H2/H3**——財報是假設表最便宜的證偽來源，抓不到矛盾多半是沒真的對。§8.5 在 delta 不新增（有新文獻 ＝ 素材級變化 → 全套）。

### 步驟 5｜升級觸發（任一命中 → 中止 delta，改跑全套）
| # | 觸發 | 為什麼 |
|---|---|---|
| 1 | 任一假設判為 **L2/L3 級漂移**（QC-35 削弱以上） | 假設動了，Part I 推導不再有效 |
| 2 | 任一 R1–R3 或 §2.F binary trigger **已觸發** | 報告自己寫下的證偽點發火了 |
| 3 | 對帳後**傾向翻面裁決** | delta 不得翻面；傾向翻面本身即升級訊號 |
| 4 | 現價相對上次報告 **±20% 以上** | 估值層失錨，情境樹需重建而非重算 |
| 5 | 重大 thesis 級事件（M&A／CEO 更迭／guidance 撤回／監管裁定） | 判斷級輸入變了 |

中止時**數字包與步驟 3 對帳結果全部沿用**，全套流程從 SKILL.md【執行協議】步驟 1.5 接手（採集不重跑）；最終回報說明「delta 升級全套，觸發＝第 N 條」。

### 步驟 6｜產出 delta 複審版
`cp` 舊檔為 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`（今日日期），**保留其餘全文**，只 patch 下列：

| 位置 | 改什麼 |
|---|---|
| 頁首儀表板 | 現價／估值燈與 Fwd PE·PEG／R:R 三時距／as-of；**QC-7 一致性照守** |
| 頁首 badge（**必加**） | `delta 複審版：數據層 as-of {今日}｜全套重寫 as-of {上次全套日期}` |
| §1 監測指標表 | 三項現值＋as-of |
| §8 | 有新財報 → 重寫該節；無 → 不動 |
| §10 | 關鍵倍數刷新；現價 ±20% 帶內**沿用原情境樹**，只重算 IRR 現價項。**QC-36 四處一致照守**（附錄 A R:R 長期格／頁首／§10.5／dd-meta `upside_5y_pct`） |
| §13 裁決晶片 | 標「複審維持（delta）」；裁決文字／倉位角色／`rearm_trigger` 不動 |
| §14 保質期 | 順延至「下次財報日」與「今日 +90 天」**孰早**，且不晚於「上次全套日期 +9 個月」（呼應資格閘 5） |
| 版本修訂紀錄 | append：`{今日}　delta 複審（數據層刷新，敘事層 as-of {上次全套日期}）：H1/H2/H3 全部成立、R1-R3 未觸發、裁決維持 {裁決}`。section 不存在時先建 |
| 【假設驗證對照】 | append 一列組：H1/H2/H3 上次→本次→邊際變化、R1–R3 是否觸發、裁決變化欄寫「維持（delta）」 |
| dd-meta | `date`／`price_at_dd`／`fpe_fy2`／`pct_5y`／`peg_fy2`／`upside_short_pct`／`upside_mid_pct`／`ev5y_pct`／`irr_base_pct`／`kill_metrics[].last_status`。**`verdict`／`dca_verdict`／`dca_role`／`moat`／`moat_trend`／`runway_post_y5` 一律不動**（判斷級欄位，delta 無權改） |

**patch 手法（token 紀律，v15.2）**：`python3 scripts/dd_sections.py extract FILE ID` 取待換段原文（canonical id，多個可逗號分隔一次取）→ 在 context 內改寫 → 寫暫存檔 → `python3 scripts/dd_sections.py replace FILE ID NEWFILE` 就地覆寫（命中須恰 1，否則 exit 2 不寫檔，印「ID 舊 bytes → 新 bytes」）。**禁止整檔 Read**、禁止整檔重寫（重寫＝把省下的 token 全部退回去）。

**誠實標示原則（不可退讓）**：讀者必須一眼看出「Part I 敘事層 as-of 是上次全套日期、數據層是今日」。badge ＋ 版本修訂紀錄雙標示，缺一即違規，**不得把 delta 版包裝成全新報告**。（與 memory「報告資料更新要無痕」不衝突——那條講全套 refresh 時新數據融入敘事；delta 沒重寫敘事，隱藏落差就是誤導。）

### 步驟 7｜不跑寫稿後 critic
delta 版**不跑 QC-41／QC-48／QC-50／row 8b**：裁決未變、無新判斷產出物，critic 的冷讀對象不存在。**升級全套時全部 critic gate 照跑，一個不減。** 此免除已登記 kill condition（`rule_ledger.md` 2026-08-07）——被發現含 critic 本可攔下的整軸級錯誤 ≥1 例，即改掛輕量單軸抽查 critic。

### 步驟 8｜同步鏈
`python scripts/update_dd_index.py`（連鎖 research 頁／dd-screener／picks／supply-chain dd_links），與全套完全相同不簡化。commit 前照 repo CLAUDE.md 跑 `python3 scripts/qc.py` 與並行 session git hygiene 四步。

---

## 三、與既有機制的介面

1. **dd-meta 不新增 `refresh_mode` 欄**。`validate_dd_meta.py` 對 v13+ 的 unknown-key sweep 是 **warn-only 不擋 commit**，但 `WHITELIST_KEYS` **刻意留空**（讓 schema drift 保持可見），加欄會讓每份 delta 永久噴一條 `unknown dd-meta key` 警告、稀釋該訊號。delta 標記因此只走 **badge ＋ 版本修訂紀錄**；日後要落機器欄須同時改 validator 的 `V13_OPTIONAL_TYPES`。
2. **pre-commit size gate**：delta 產出是 added 檔且帶 `"schema":"v15`，走 **70／80／115KB**。delta 只加不減，起點是已過關的 75–105KB 全套檔，必然過 floor；若 patch 後 <70KB ＝ 誤刪章節，**先查刪了什麼再談 commit**。基檔含 §8.5 逼近 115KB 時可能觸上界警告——上界只警告不擋，delta 不是重寫時機，不因此壓縮。
4. **qc.py 機器語言檢查（v15.2）**：`cp` 自 v15.0／15.1 舊檔的 delta 版沒有 `<meta name="dd-render">` 標記，`dd_sections.py leaks` 命中只列 warning 不擋 push；基檔本身由 `render_dd.py` 產出（含標記）時，delta 版仍是整檔新增，leaks 命中會 error——patch 段落請維持零機器語言。
3. **QC-17／QC-18 沿用**：只讀最近一份、只讀指定區塊、一律區段擷取。delta 沒放寬讀取紀律，只把「讀完之後做什麼」從重寫改成對帳。

---

## 四、成本推算（供後續實測校準）

| 項 | 全套 | delta |
|---|---|---|
| 採集 fan-out | 數字包 ≤6KB | 同（不簡化） |
| 判斷性搜尋 | QC-39 三軸 ≥9＋QC-12＋Munger＋QC-19 | 只查假設門檻與監測現值，10–15 輪 |
| 舊檔讀取 | 區段擷取 ~8–15k | 同 |
| 章節 output | ~150k | patch 約 15–25k |
| 寫稿後 critic | 3 gate 合併載具 ~197k | **0** |
| **合計推估** | **620–645k** | **約 120–180k（≈ 20–28%，省 72–80%）** |

推估未經實測，**前三份 delta 必須把實際 token 用量寫進最終回報**，作為 2026-10 校準輪判斷「省幅可量測」的依據（kill condition 反向條件）。

---

## 五、最終回報（≤400 字）

路徑＋KB／delta 或升級全套（升級時寫觸發第幾條）／H1-H3 判定與 R1-R3 觸發狀態／裁決維持與否／監測指標現值／保質期新日期／實際 token 用量／INDEX 行。**不複述報告內容。**
