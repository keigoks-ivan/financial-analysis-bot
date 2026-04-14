# v8.1.2 品質管控補丁

**版本**:v8.1 → v8.1.2
**核心變更**:加入 8 條品質強制規則,解決兩份 Opus 審查發現的 6 個系統性問題 + 強制不中斷
**規模**:1 個插入點(frontmatter 之後),約 60 行新增,不動任何現有章節

---

## Claude Code 部署 prompt

把下面 ``` 包起來那段一次貼給 Claude Code:

```
v8.1.2 品質管控補丁。

核心變更:在 SKILL.md frontmatter 之後插入一個「品質管控區塊」,包含 8 條
強制規則。不動任何現有章節的內容、公式、結構。同時把 frontmatter version
從 v8.1 升到 v8.1.2。

========== 階段 A(全自動,一口氣跑完) ==========

依序執行以下所有步驟,全部完成後才停下回報。中間不要停頓問我。

--- Step 1:健康檢查 + 備份 ---

1. md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
   (應一致,當前 v8.1 hash f6016df57f243f50a4170348c1d72ab5)
2. cp docs/dd/skills/stock-analyst/SKILL.md docs/dd/skills/stock-analyst/SKILL.md.backup-v8.1
3. wc -l docs/dd/skills/stock-analyst/SKILL.md(應為 1280)

--- Step 2:修改 1 — frontmatter version 升級 ---

檔案:docs/dd/skills/stock-analyst/SKILL.md

Before:
version: v8.1
released: 2026-04-11

After:
version: v8.1.2
released: 2026-04-12

--- Step 3:修改 2 — 插入品質管控區塊 ---

檔案:docs/dd/skills/stock-analyst/SKILL.md

找到 frontmatter 結束的 --- 行(第 6 行),在它之後、現有內容之前,
插入以下整段文字。

用 Edit 工具:old_string = frontmatter 結尾的 --- 加上緊接其後的第一行
內容(可能是空行或章節標題),new_string = 同樣的 --- 和第一行,中間
插入品質管控區塊。

要插入的品質管控區塊完整內容:

---BEGIN INSERT---

## 【品質管控強制規則(v8.1.2)】

**執行原則**:本 skill 必須一口氣跑完整份 DD,不得中斷詢問使用者,
除非資料經 2 次 web_search 仍無法取得(此時直接停止並回報「資料不足」,
不要問「你能提供嗎」)。以下 8 條規則在每份 DD 執行時無條件強制遵守。

### QC-1｜B-1 業務權重必須引用 §5

§7.7 B-1 成長驅動分解的各業務段營收權重**必須**直接引用 §5 產業格局
的營收組成數字。禁止自行估算權重。所有超過 5% 營收占比的業務段必須
完整列出,權重加總必須 = 100%。若 §5 尚未完成,先完成 §5 再回來算 B-1。

### QC-2｜MA104w 必須查實際數據

MA104w（104 週移動均線）**必須**從 web_search 查詢實際數值。
搜尋查詢範例:
```
[TICKER] 104-week moving average
[TICKER] MA104 weekly TradingView
```
**禁止**使用「雙年均值外推」「起點終點平均」或任何估算法。
若 2 次搜尋無法取得 MA104w,可用 MA100w 或 MA520d 替代,
但必須在表格備注「替代指標:MA100w（非 MA104w）」。
同理,MA60 若無法取得而使用 MA50,必須備注「替代指標:MA50（非 MA60）」。

### QC-3｜下行風險基期 EPS 必須標示時點

§8 下行風險壓力測試的每個情境必須明確標示:
- 情境標題:「當前重定價」或「N 年後情境」
- 基期 EPS:明確寫出數值及來源（FY25 確數 / FY26E / 外推值）
- 若情境稱「3 年後」,基期 EPS = 當前 EPS × (1 + 採用 CAGR)^3,
  不得直接使用 FY26E 的 EPS
- 已公告的財年 EPS 標示為「確數」,不得標「估」

### QC-4｜Forward P/E 分位必須列公式

§7.1 的 Forward P/E 歷史分位必須用以下公式計算並顯示:
  分位 = (當前值 − 5Y 低) / (5Y 高 − 5Y 低) × 100%
不得使用「~70%」等概數,必須算到整數位（如 68%）。
§7.6 或 §8 引用 5Y 均值時,數字必須與 §7.1 完全一致,
禁止出現同一份 DD 內兩個不同的 5Y 均。

### QC-5｜§4 同業比較組必須與 §7.4 一致

§4 財務品質的同業比較表必須使用與 §7.4 橫向比較相同的對手組
（至少 3 家直接競爭對手）。禁止只放 1 家對手做比較。

### QC-6｜§6 治理必須涵蓋四項

§6 公司治理章節必須包含以下四項:
1. 股東/股權結構（含 dual-class 投票權說明）
2. 資本配置方向（Capex / 回購 / 分紅的優先順序與金額）
3. 管理層薪酬結構（固定薪 vs 績效獎金 vs 股權激勵的比例）
4. 過去 12 個月重大內部人交易（買入/賣出/金額/對象）
若 web_search 無法取得第 3 或第 4 項,在該小節標註「數據限制:
無法取得管理層薪酬/內部人交易資訊」,不得跳過整個小節。

### QC-7｜§7.7 與 §8 的 R:R 數字必須一致

§8 投資結論開頭引用的三層 R:R 數字必須與 §7.7 F 綜合解讀表的數字
**完全一致**（到小數點後兩位）。禁止在 §8 重新計算、四捨五入、
或使用不同版本的數字。直接從 §7.7 F 表格複製。

### QC-8｜執行不中斷

LLM 必須按上述 QC-1 到 QC-7 規則自動執行所有章節,不得中斷詢問
使用者任何問題,包括但不限於:
- 技術性細節（公式套用、單位換算、四捨五入）
- 評級判斷（§2.5 長期成長性、§3 護城河評分、§7.5 長期合理倍數）
- 數據來源選擇（用哪個 EPS、用哪個 P/E）

所有有客觀依據的判斷必須自行決定並在 HTML 內文說明依據。
若資料經 2 次 web_search 仍無法取得,標註「數據限制」後繼續執行
剩餘章節,不得停下。

---END INSERT---

--- Step 4:同步 global runtime ---

1. cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
2. md5 對比兩份(必須一致,新 hash 會跟 v8.1 的 f6016df5... 不同)
3. wc -l 對比兩份(預期 1280 + 約 60 行 ≈ 1340 左右)

--- Step 5:最終驗證 ---

1. grep -c "QC-" docs/dd/skills/stock-analyst/SKILL.md(預期 8,對應 8 條規則)
2. grep -c "v8.1.2" docs/dd/skills/stock-analyst/SKILL.md(預期 ≥ 2)
3. grep -c "品質管控" docs/dd/skills/stock-analyst/SKILL.md(預期 ≥ 1)
4. grep -c "不得中斷" docs/dd/skills/stock-analyst/SKILL.md(預期 ≥ 2)

--- 階段 A 完成,回報以下所有結果 ---

1. 健康檢查(md5 一致 + 備份成功 + baseline 行數)
2. 修改 1 frontmatter 升級(成功/失敗)
3. 修改 2 品質管控區塊插入(成功/失敗 + 插入位置行號)
4. 同步 runtime(新 md5 hash + 雙檔行數)
5. 最終驗證(4 個 grep 結果)

回報後停下,等我確認才進階段 B。

========== 階段 B(手動,等階段 A 確認後) ==========

告訴使用者:
1. v8.1.2 品質管控補丁已部署
2. 需要重啟 Claude Code session 才能載入新版 skill
3. 重啟後建議重跑 TSMC(分析 2330)做品質對比驗證
4. 不要自動重啟,等使用者手動操作

========== 階段 C(使用者驗收後回來 commit) ==========

使用者重啟、跑完測試 DD、滿意後回來指示。那時:

1. rm docs/dd/skills/stock-analyst/SKILL.md.backup-v8.1
2. rm tmp_v8.1.2_deploy.md(如果存在)
3. git add docs/dd/skills/stock-analyst/SKILL.md
4. commit 訊息:

   skill: v8.1.2 quality control patch
   
   基於 2 份 v8.1 DD (TSMC + GOOGL) 的 Opus 品質審查,
   加入 8 條強制品質管控規則(QC-1 到 QC-8):
   
   - QC-1: B-1 業務權重必須引用 §5 營收組成(修復權重不一致)
   - QC-2: MA104w 必須查實際數據(禁止估算外推)
   - QC-3: 下行風險基期 EPS 必須標示時點(修復基期混用)
   - QC-4: Forward P/E 分位必須列公式(禁止概數)
   - QC-5: §4 同業比較組必須與 §7.4 一致(至少 3 家)
   - QC-6: §6 治理必須涵蓋四項(含薪酬+內部人交易)
   - QC-7: §7.7 與 §8 R:R 數字必須一致(禁止重算)
   - QC-8: 執行不中斷(數據限制標註後繼續,不得停下)
   
   問題來源:TSMC(11 個問題)+ GOOGL(17 個問題),
   其中 6 個系統性問題 100% 重現率。

5. push 等使用者另外指示

========== 全程規則 ==========

- 階段 A 內部不停頓,一口氣跑完 Step 1-5 才回報
- 階段 B / C 各自停頓
- Edit 前先 grep 確認唯一性
- 不要動品質管控區塊以外的任何現有內容

階段 A 開始執行。
```

---

## 回滾保險

v8.1 永久保存:
- 本地 backup: SKILL.md.backup-v8.1
- Git commit: 05751df(v8.1 SKILL.md)

任何時候回到 v8.1:
```bash
cp docs/dd/skills/stock-analyst/SKILL.md.backup-v8.1 docs/dd/skills/stock-analyst/SKILL.md
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
```
