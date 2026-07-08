# InvestMQuest Research 視覺與語調規範 v1（2026-07-07）

持有人裁決：機構研究風、nav/標題全面去 emoji、AI 揭露收進正式頁。本檔為全站樣式單一真相來源——改版 agent 與未來所有 generator 一律遵循。

## 1. 定位語

- 品牌名：**InvestMQuest Research**（不縮寫、不加 emoji）。
- 定位句（首頁 hero）：「獨立投資研究 —— 選股系統 × 個股與產業深度研究 × 市場狀態儀表」。
- 禁用詞（對外頁面）：「AI 驅動」「一鍵」「開站」「玩」「爽」等口語；「AI 自動生成僅供參考」滿版重複（收進 /disclosures.html）。

## 2. 色彩（tokens）

| token | 值 | 用途 |
|---|---|---|
| `--ink` | `#0f2a45` | 標題、主文字（深藍近黑） |
| `--body` | `#1e293b` | 內文 |
| `--sec` | `#5a7a9a` | 次要文字 |
| `--paper` | `#f6f8fb`（頁底）/ `#ffffff`（卡） | 背景 |
| `--line` | `#dce8f5` | 邊框 |
| `--accent` | `#1e3a5f` | 連結、強調（**單一 accent，不再混紫/橘/青做裝飾**） |
| `--pos / --neg / --warn` | `#166534` / `#991b1b` / `#92400e` | 僅限數據語意（漲跌/裁決/警示），不做裝飾 |

漸層限 nav（既有深藍漸層保留——已是機構感）與 hero 極淡底；卡片不再用彩色漸層 CTA 底。

## 3. 字體

- 標題（h1/h2 與 hero）：`'Noto Serif TC', Georgia, 'Times New Roman', serif`，色 `--ink`，字重 700，`letter-spacing:-.01em`。
- 內文/表格/UI：維持 `'Inter','Noto Sans TC',…` 無襯線。
- 數字：`'IBM Plex Mono'` 等寬照舊（tabular-nums）。

## 4. Emoji 政策

- **移除**：nav 選單標籤、頁面 `<title>`、h1–h3、卡片 tag/eyebrow、按鈕、section 標頭、subnav 標籤。
- **保留**（功能性資料語意）：表格內狀態燈 🟢🟡🟠🔴、趨勢 ↑↓→、單點旗標 ⚑、裁決/警示符號 ⚠⛔⏰——即「代表資料值」的符號留，「裝飾標題」的符號刪。
- 邊界判準：把 emoji 拿掉後語意有損＝保留；只是變樸素＝刪。

## 5. 頁尾（全站標準）

```html
<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
```
既有各頁滿版免責段落刪除，一律收斂為上述兩行＋連結。

## 6. 語調

- 賣方研究口吻：直述、可證偽、數字帶來源；不自我對話、不喊口號。
- 中文全形標點（既有規範）；中英夾雜時專有名詞保留英文。
- 頁面副標句式：「本頁提供……；資料來源……；更新頻率……」三要素。

## 7. 揭露

- `/disclosures.html`＝唯一正式揭露頁：研究方法論、AI 產製流程揭露、資料來源、免責聲明、利益衝突聲明。
- 各頁不再滿版重複；頁尾一行連過去。

## 9. 設計系統（v1.1 新增，2026-07-08「高級感」輪）

單一真相來源：**`docs/assets/imq-base.css`**（tokens + 元件基準）。所有 hub / generator 頁面：

1. `<head>` 內 `<link rel="stylesheet" href="/assets/imq-base.css">`（放在頁內 `<style>` 之前，讓局部可覆寫）。
2. 頁內 CSS 的顏色/圓角/陰影/字體**一律改引 var(--…)**，不得再寫死自己的藍色/紫色/陰影值。
3. 元件對齊基準：表格照 `.imq-table` 規格（無 zebra、細線、表頭 mono overline、數字 `.num` 右齊等寬）、卡片照 `.imq-card`（平面 1px 邊+極輕影；**刪除彩色漸層底與粗彩色左條**）、徽章照 `.imq-badge`（中性底+語意色字；刪彩色漸層 chip）、統計格照 `.imq-stat`、分節照 `.imq-sec`、頁尾照 `.imq-foot`。可以沿用既有 class 名（JS 依賴不破壞），但其樣式值要改成與基準一致。
4. 高級感負面清單（見到即改）：多彩漸層按鈕/卡底、每區一種主題色（v-purple/v-indigo/v-amber 這類裝飾色系）、粗陰影大位移 hover、超過兩種圓角、inline style 寫死的彩色、zebra 表格、彩色 pill 密度過高。
5. 間距節奏：section 間 `--sp-4`（2.5rem）、卡內 `--sp-3`、行內 `--sp-1/2`；不要出現 13px/17px/23px 這種隨手值。
6. 數據語意色只剩 `--pos/--neg/--warn` 三個；狀態燈 emoji 照 §4 保留。

## 8. 執行紀律（agent 適用）

- 改 baked 頁（pipeline/engine/catalyst/長線……）**必須同步改 generator 模板**，否則下次 cron 洗回去。
- 不碰外部四樹（weekly/briefing 內容頁/qgm/qgm-tw/backtest）——nav 由 snippet 同步機制處理。
- 不碰報告本體（docs/dd/DD_*、docs/id/ID_*、dca、ds、comparisons 個別報告、earnings 日報）——報告內文自有格式，僅站級 chrome（nav/頁尾）統一。
- JS 字串內的 emoji（如 cockpit chips label）視同標題類處理，但改完必過 `node --check`。
- Python generator 改完必過 `py_compile`。不跑 git。
