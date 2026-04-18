# PM Report HTML 視覺規格

## 檔名格式
`docs/pm/PM_YYYYMMDD.html`

## HTML 結構

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="pm-schema-version" content="v1.0">
<title>PM 複盤｜YYYY-MM-DD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>/* 沿用 DD v12 樣式，略 */</style>
</head>
<body>
<div class="topbar">
<div class="left"><b>組合複盤</b> ｜ YYYY-MM-DD</div>
<div class="right">
  <span>NAV: $X.XM</span> ｜
  <span>現金: XX%</span> ｜
  <span>核心 _/5</span> ｜
  <span>衛星 _/3</span> ｜
  <span>PM Skill v1.0</span>
</div>
</div>

<div class="container">
<h1>組合複盤報告 — YYYY-MM-DD</h1>

<!-- §1 組合快照 -->
<h2>§1｜組合快照</h2>
...

<!-- §2 個股複盤表 -->
<h2>§2｜個股複盤表</h2>
<table>
  <tr><th>Ticker</th><th>Tier</th><th>現倉</th><th>DD 版本/日期</th><th>Signal</th><th>Trap</th><th>Gate</th><th>現價 vs 目標</th><th>PM 裁決</th><th>Override</th></tr>
  ...
</table>

<!-- §3 賣出/減碼 -->
<h2>§3｜🔴 賣出 / 減碼清單</h2>
...

<!-- §4 加碼 -->
<h2>§4｜🟢 加碼清單</h2>
...

<!-- §5 新進候選池 -->
<h2>§5｜🟡 新進候選池</h2>
...

<!-- §6 維持 -->
<h2>§6｜⚪ 維持名單</h2>
...

<!-- §7 組合風險敘述 -->
<h2>§7｜組合風險敘述</h2>
...

<!-- §8 Override 清單 -->
<h2>§8｜Override 清單</h2>
...

<!-- §9 Rebalance 建議 -->
<h2>§9｜Rebalance 建議配置</h2>
...

<button class="print-btn" onclick="window.print()">列印為 PDF</button>
</div>
</body>
</html>
```

## 視覺規格（沿用 DD v12）

- 主背景 #F8FAFC，卡片白底 #FFFFFF
- 章節標題深藍 #1E3A5F + 4px accent 線 #3B82F6
- 字型：Noto Sans TC（內文）+ IBM Plex Mono（數字）
- 表格：白底交替 #F1F5F9，標題列 #1E3A5F 白字

## PM 裁決專屬配色

| 裁決 | 底色 | 字色 |
|:---|:---|:---|
| 🔴 賣出 | #FEE2E2 | #991B1B |
| 🟠 減碼 | #FFEDD5 | #9A3412 |
| 🟢 加碼 | #DCFCE7 | #166534 |
| 🟡 新進 | #FEF9C3 | #92400E |
| ⚪ 維持 | #F1F5F9 | #475569 |

## Override 標記配色

| 級別 | 配色 |
|:---|:---|
| L1 Sizing | 綠 #16A34A |
| L2 Horizon | 黃 #EAB308 |
| L3 Information | 橘 #F97316 |
| L4 Thesis | 紅 #DC2626（禁止）|

## §9 Rebalance 配置表範例

```html
<table>
<tr><th>Ticker</th><th>Tier</th><th>當前 %</th><th>目標 %</th><th>Delta</th><th>動作</th></tr>
<tr><td>NVDA</td><td>core</td><td>18.0%</td><td>20.0%</td><td>+2.0</td><td class="green-cell">加碼</td></tr>
<tr><td>MSFT</td><td>core</td><td>15.5%</td><td>15.0%</td><td>−0.5</td><td>維持</td></tr>
<tr><td>FN</td><td>satellite</td><td>5.5%</td><td>0.0%</td><td>−5.5</td><td class="red-cell">清倉</td></tr>
<tr><td>COHR（新進）</td><td>satellite</td><td>0.0%</td><td>6.0%</td><td>+6.0</td><td class="yellow-cell">新進</td></tr>
...
<tr style="font-weight:bold"><td>現金</td><td>—</td><td>15.0%</td><td>12.0%</td><td>−3.0</td><td>縮減</td></tr>
</table>
```

## 字體段落

- H1：28px 深藍 + 4px accent 線
- H2：22px 白字 + 深藍底（section header）
- H3：18px 深藍 + accent 線
- 內文：14px
- 表格：14px，單元格 padding 10px
