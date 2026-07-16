> 本檔為 `multi-stock-comparator-v1` SKILL.md 的條件載入 reference（v1.10 結構拆分）。**載入時點：第五／六步 寫 HTML 前**（見核心路由表）；CSS 完整樣板另見 skill 根目錄 `HTML_TEMPLATE.md`。 內容自 SKILL.md v1.9 原文零語意變更搬移。

## 【HTML 輸出協議】

### 視覺規格(對齊 InvestMQuest research.investmquest.com 風格)

CSS 規格詳見 `HTML_TEMPLATE.md`。核心要點：

- **背景**:`#ffffff`(白底)
- **主文字**:`#1a1d24`
- **強調**:`#000000`(粗體)
- **強調色**:藍 `#1565c0`、橘 `#c2410c`、綠 `#15803d`、紅 `#991b1b`
- **表格邊框**:`#d0d8e0`
- **字型**:`-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", Roboto, sans-serif`
- **章節錨點**:`#sA`、`#sA1`、`#sA2`、`#sA3`、`#sB1`、`#sB2`、`#sB3`、`#sB4`、`#sC`、`#sD`、`#sE`
- **頂部導航**:固定 sticky,提供快速跳轉
- **手機優化**:`@media (max-width: 768px)` 內字級放大、padding 縮小

### 訊號燈規範

四種主要訊號燈(對齊 v13/v14 DD):
- 🟢 高確信 / 寬 / 便宜
- 🟡 中性 / 中等 / 觀察期
- 🔴 警示 / 窄 / 昂貴
- ⚫ X(迴避)

排序視覺：
- 🥇 第一名(綠底)
- 🥈 第二名(灰底)
- 🥉 第三名(橘底)
- (4 檔以上續用數字)

### 結論卡片格式

§A Dashboard 頂部必須有「綜合裁決卡片」:

```
推薦標的：[Ticker]
適用時間框架：3-5 年
主要理由(三條):
1. [一行]
2. [一行]
3. [一行]
進場條件：[Pure MA 確認 / 拐點催化 / 等等]
```

