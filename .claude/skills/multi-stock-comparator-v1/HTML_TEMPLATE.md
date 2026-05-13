# HTML_TEMPLATE.md — Multi-Stock Comparator v1.1 視覺規格

本文件提供 multi-stock-comparator-v1 的 HTML 輸出規格。

**v1.1 更新(2026-05-13)**:配色從深色背景翻轉為**白底深字**,符合一般網頁閱讀習慣,iOS dark mode/降低白點值等任何環境都清晰可讀。

---

## 【視覺規格 — 白底深字配色】

### 主色票

| 用途 | 顏色 | 說明 |
|:---|:---|:---|
| 主背景 | `#ffffff` | 純白 |
| 主文字 | `#1a1d24` | 近黑(段落、表格內文) |
| 強調文字 | `#000000` | 純黑(strong、callout 重點) |
| 主標題 | `#0a1628` | 深藍黑(h1、h2) |
| 次要文字 | `#4a5568` | 中灰(meta、label、footer) |
| 表格分隔 | `#d0d8e0` / `#e2e8f0` | 淺灰 border |

### 強調色

| 用途 | 顏色 | 說明 |
|:---|:---|:---|
| 主強調(連結、§A border) | `#1565c0` | 深藍 |
| 推薦/第一名/正向 | `#15803d` | 森林綠 |
| 警示/第三名 | `#c2410c` | 深橘 |
| 第二名/中性 | `#475569` | 深灰藍 |
| 紅色警示 | `#991b1b` | 深紅 |

### 訊號燈(淺底深字,WCAG AA 對比合格)

| 訊號 | 背景 | 文字 |
|:---|:---|:---|
| 🟢 高確信/便宜/正向 | `#dcfce7` 淺綠 | `#166534` 深綠 |
| 🟡 觀察/中等 | `#fef3c7` 淺黃 | `#92400e` 深棕 |
| 🔴 警示/拒絕 | `#fee2e2` 淺紅 | `#991b1b` 深紅 |
| ⚪ 中性 | `#e2e8f0` 淺灰 | `#475569` 深灰 |

### Callout 三色

| 類型 | 背景 | 左 border |
|:---|:---|:---|
| 一般(資訊) | `#eff6ff` 淺藍 | `#1565c0` 深藍 |
| 警示(callout-warn) | `#fff7ed` 淺橘 | `#c2410c` 深橘 |
| 關鍵(callout-key) | `#f0fdf4` 淺綠 | `#15803d` 森林綠 |

### IRR Bar 顏色(白底上用深色)

| 段別 | 顏色 |
|:---|:---|
| EPS 複利(正向) | `#15803d` 森林綠 |
| PE re-rate 正(順風) | `#1565c0` 深藍 |
| PE re-rate 負(逆風) | `#b91c1c` 深紅 |
| 股息+回購 | `#c2410c` 深橘 |

所有 IRR segment 文字為白色 `#ffffff`。

---

## 【完整 CSS 區塊】(直接複製進 HTML)

```css
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", Roboto, sans-serif;
  background: #ffffff;
  color: #1a1d24;
  line-height: 1.8;
  font-size: 16px;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
p { color: #1a1d24; margin: 14px 0; font-weight: 400; }
li { color: #1a1d24; font-weight: 400; }
strong { color: #000000; font-weight: 700; }
.container { max-width: 1200px; margin: 0 auto; padding: 24px 20px 60px; }
.report-header { border-bottom: 2px solid #d0d8e0; padding-bottom: 16px; margin-bottom: 24px; }
.report-header h1 { font-size: 28px; color: #0a1628; margin: 0 0 8px; font-weight: 700; }
.report-meta { font-size: 14px; color: #4a5568; font-weight: 500; }
.report-meta span { margin-right: 16px; }
.toc-nav {
  position: sticky; top: 0;
  background: #ffffff;
  padding: 14px 20px;
  border-bottom: 2px solid #d0d8e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin: 0 -20px 28px; z-index: 100;
}
.toc-nav a {
  color: #1565c0;
  text-decoration: none;
  margin-right: 16px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
  padding: 4px 2px;
}
.toc-nav a:hover { color: #c2410c; }
section { margin-bottom: 36px; padding-top: 16px; }
h2 { font-size: 24px; color: #0a1628; border-left: 4px solid #1565c0; padding-left: 12px; margin: 0 0 18px; font-weight: 700; }
h3 { font-size: 18px; color: #c2410c; margin: 22px 0 12px; font-weight: 700; }
h4 { font-size: 16px; color: #15803d; margin: 16px 0 10px; font-weight: 700; }
.verdict-card {
  background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
  border: 1px solid #90caf9; border-left: 4px solid #15803d;
  border-radius: 8px; padding: 22px 26px; margin-bottom: 22px;
}
.verdict-card .verdict-label { font-size: 13px; color: #4a5568; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; font-weight: 700; }
.verdict-card .verdict-pick { font-size: 32px; font-weight: 700; color: #15803d; margin-bottom: 10px; }
.verdict-card .verdict-timeframe { font-size: 15px; color: #c2410c; margin-bottom: 14px; font-weight: 600; }
.verdict-card ul { margin: 8px 0 0; padding-left: 22px; }
.verdict-card li { margin-bottom: 10px; font-size: 15px; color: #1a1d24; line-height: 1.7; }
.verdict-card p { color: #1a1d24; }
table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 15px; background: #ffffff; border: 1px solid #d0d8e0; border-radius: 6px; overflow: hidden; }
th { background: #f1f5f9; color: #0a1628; padding: 12px 14px; text-align: left; border-bottom: 2px solid #cbd5e1; font-weight: 700; font-size: 14px; }
td { padding: 12px 14px; border-bottom: 1px solid #e2e8f0; color: #1a1d24; vertical-align: top; font-weight: 400; }
tr:hover { background: #f8fafc; }
tr:last-child td { border-bottom: none; }
.rank-1 { color: #15803d; font-weight: 700; }
.rank-2 { color: #475569; font-weight: 700; }
.rank-3 { color: #c2410c; font-weight: 700; }
.signal { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 13px; font-weight: 700; }
.signal-green { background: #dcfce7; color: #166534; }
.signal-yellow { background: #fef3c7; color: #92400e; }
.signal-red { background: #fee2e2; color: #991b1b; }
.signal-grey { background: #e2e8f0; color: #475569; }
.callout {
  background: #eff6ff;
  border-left: 4px solid #1565c0;
  padding: 16px 20px;
  margin: 18px 0;
  border-radius: 4px;
  font-size: 15px;
  color: #1a1d24;
  line-height: 1.75;
}
.callout strong { color: #000000; font-weight: 700; }
.callout-warn { background: #fff7ed; border-left-color: #c2410c; }
.callout-key { background: #f0fdf4; border-left-color: #15803d; }
.irr-bar { display: flex; height: 40px; border-radius: 4px; overflow: hidden; margin: 10px 0 4px; background: #e2e8f0; border: 1px solid #cbd5e1; }
.irr-segment { display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: #ffffff; white-space: nowrap; padding: 0 8px; }
.irr-eps { background: #15803d; }
.irr-rerate-pos { background: #1565c0; }
.irr-rerate-neg { background: #b91c1c; color: #ffffff; }
.irr-buyback { background: #c2410c; }
.irr-legend { font-size: 14px; color: #334155; margin-bottom: 16px; line-height: 1.7; }
.timeframe-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 18px 0; }
.tf-card { background: #f8fafc; border: 1px solid #d0d8e0; border-radius: 6px; padding: 16px 18px; }
.tf-card .tf-label { font-size: 12px; color: #4a5568; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-weight: 700; }
.tf-card .tf-winner { font-size: 20px; font-weight: 700; color: #15803d; margin-bottom: 10px; }
.tf-card .tf-reason { font-size: 14px; color: #1a1d24; line-height: 1.65; font-weight: 400; }
.report-footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #d0d8e0; font-size: 13px; color: #4a5568; text-align: center; line-height: 1.7; }
@media print { body { background: #ffffff; color: #000000; } .toc-nav { display: none; } }
@media (max-width: 768px) {
  body { font-size: 17px; line-height: 1.85; }
  .container { padding: 16px 16px 40px; }
  .report-header h1 { font-size: 22px; }
  h2 { font-size: 21px; }
  h3 { font-size: 18px; }
  h4 { font-size: 17px; }
  p, li { font-size: 16px; }
  table { font-size: 14px; }
  th, td { padding: 12px 10px; }
  .toc-nav { padding: 14px 16px; margin: 0 -16px 24px; }
  .toc-nav a { margin-right: 14px; font-size: 14px; padding: 6px 2px; }
  .callout, .verdict-card { font-size: 15px; }
  .verdict-card li { font-size: 15px; }
  .irr-segment { font-size: 12px; }
  .tf-card .tf-reason { font-size: 14px; }
}
```

---

## 【HTML 骨架結構】

完整骨架見 v1.0 版本(章節 §A-§E 結構未變),只是 CSS 改為白底深字。

關鍵章節:
- §A Dashboard:verdict-card(綠 border)+ 基本資料表 + 四層排序速覽
- §B.1-B.4:四層時間框架,每層獨立排序 + 判斷邏輯
- §C IRR Composition:irr-bar 視覺化拆解
- §D Bear / MaxDD:執行風險 vs 範式風險標籤
- §E 最終裁決:推薦標的 + 不選他檔理由 + 時間軸敏感度測試

---

## 【字元數估計】

| 檔數 | HTML 大小 |
|:---|:---|
| 2 檔對比 | 18-25K 字元 |
| 3 檔對比 | 25-45K 字元 |
| 4 檔對比 | 40-55K 字元 |
| 5 檔對比 | 50-65K 字元 |

單次 create_file 可容納 3 檔。**4-5 檔需要分段追加**,以 str_replace 補完。

---

## 【完成檢核】

HTML 生成後內部檢核:

1. ✅ 所有 [TICKER1/2/3] 都已替換為實際 ticker
2. ✅ 所有 [YYYY-MM-DD] 都是當前日期
3. ✅ 所有表格欄位填滿(無 ... 殘留)
4. ✅ 五大章節(§A-§E)全寫完
5. ✅ §A 推薦卡片有明確推薦標的(綠色 verdict-pick)
6. ✅ §B 每層都有 1-N 排序(rank-1/rank-2/rank-3 css)
7. ✅ §C IRR Bar 已 render(寬度比例正確,白色文字)
8. ✅ §D 風險類型已標籤(執行/範式)
9. ✅ §E 不選其他檔的理由已點名每一檔
10. ✅ §E 時間軸敏感度測試已寫
11. ✅ 配色為白底深字(主文 #1a1d24,背景 #ffffff)

---

## 【v1.0 → v1.1 變更紀錄】

- **配色翻轉**:深色背景 → 白底深字(主文 #1a1d24 on #ffffff)
- **字級加大**:body 15px → 16px(手機 17px)
- **行距加寬**:line-height 1.7 → 1.8(手機 1.85)
- 加 `text-rendering: optimizeLegibility` + `-webkit-font-smoothing: antialiased`
- 表格 td padding 加大(10px → 12px),touch friendly
- 訊號燈改為淺底深字(WCAG AA 對比合格)
- IRR Bar 配色用深色版森林綠/深藍/深紅/深橘
- Sticky nav 改純白背景 + 淺陰影區隔
- Mobile 版 padding 加大(12px → 16px)
- 強化 strong 為純黑 #000000(原 #ffffff)
