# Flow Cockpit · 自用投資流程儀表板

> `research.investmquest.com/flow/`
>
> Ivan 的 5 步投資流程儀表板。對應馬斯克五步原則第一、二、三步:質疑需求 → 刪減 → 簡化。

---

## 設計哲學

### 為什麼存在
現有 research.investmquest.com 主站是「投研平台」(展示型),內容齊全但**首頁不對焦**。本入口專為 Ivan 個人**日常工作流**設計,只服務以下 5 步:

```
[1] 篩 ATH 股票
       ↓
[2] DD 看品質(五條件框架)
       ↓
[3] 馬上建倉 vs 等回測建倉
       ↓
[4] 持有 + 等大盤修正
       ↓
[5] 修正時加碼最強勢的(RS 線新高,非絕對抗跌)
```

主站不動,本入口獨立。等本入口用熟之後,再回頭刪主站冗餘。

### 三條鐵律
1. **預設視圖 = 早上打開時最想看的那一個**(狀態列 + Action Queue)。
2. **點擊深度 ≤ 2**(從首頁到任何決策答案不超過兩次點擊)。
3. **沒有資料寧可空白也不放假數據**(誠實 > 完整)。

### 不該做的
- ❌ 不放每日新聞簡報(IBKR / X 已經有)
- ❌ 不放週報 10 主題(訊噪比低)
- ❌ 不放 Markets / Sectors 即時行情(任何券商 App 都有)
- ❌ 不放多市場 Screener 並排(統一一個入口即可)

---

## 檔案結構

```
flow/
├── index.html         # 主入口(狀態列 + Action Queue + 4 模組 + QQQ 軌)
├── ath-hunter.html    # 1 · ATH 候選掃描(Base/Cont/Extended 分類)
├── timing-board.html  # 2 · 進場決策樹(可進場/等回踩/過熱)
├── cockpit.html       # 3 · 持倉狀態 + 季度三題 Review + 證偽條件監控
├── rs-board.html      # 4 · 修正期 RS Board(休眠/觸發兩種狀態)
├── flow.css           # 共用樣式(黑白為主 + 警訊橙黃)
├── data.json          # 主資料來源(GitHub Actions 每日寫入)
└── README.md          # 本檔
```

---

## 部署

### 1. 放到 financial-analysis-bot/docs/flow/
```bash
cd ~/Desktop/financial-analysis-bot/docs/
mkdir -p flow
# 把這個資料夾的內容複製進去
git add flow/
git commit -m "feat(flow): add cockpit entry v1.0"
git push
```

### 2. GitHub Pages 自動部署到 `research.investmquest.com/flow/`

### 3. 主站連結
在 `research.investmquest.com/index.html` 加一個入口:
```html
<a href="/flow/">🎯 Flow Cockpit(自用)</a>
```

---

## 資料接入計畫(分階段)

### Phase 1 · 靜態 Demo(現在)
所有頁面用 hardcoded 範例資料,讓 Ivan 先試用一週,確認流程對不對。

### Phase 2 · GitHub Actions 寫入 data.json
用既有 `morning-briefing` repo 的架構,新增一個 daily job:
- 06:00 TPE 觸發
- 跑 yfinance / FMP API 抓資料
- 套用五條件篩選 + ATH 分類邏輯
- 寫入 `flow/data.json`
- index.html 用 `fetch("./data.json")` 讀取(已實作 fallback 機制)

---

## 資料定義(全站統一)

### 🔑 價格定義:還原權息(Adjusted Close)

**所有頁面、所有欄位的價格 / ATH / DMA / RS / P&L 計算,一律使用還原權息收盤價。**

#### 為什麼

| 類型 | 名目價(Close) | 還原權息(Adj. Close) |
|---|---|---|
| 含義 | 收盤價 | 配息再投資後的累積總報酬 |
| 對 MSFT 2014–2016 | 看起來沒創 ATH | 已創多次 ATH |
| 對長抱者 | 漏掉真正在賺錢的好公司 | ✅ 正確訊號 |

對「長抱 outperformer」目標(配息再投資 + 長期持有)來說,**還原權息才是真實的累積總報酬**。

#### 技術實作

```python
import yfinance as yf

# yfinance >= 0.2.x 預設 auto_adjust=True
df = yf.download("MSFT", period="max", auto_adjust=True)

# df['Close'] 已經是 adjusted close
ath = df['Close'].max()                  # Adj. ATH
current = df['Close'].iloc[-1]           # Adj. current price
dma_50 = df['Close'].rolling(50).mean()  # Adj. 50DMA
dma_200 = df['Close'].rolling(200).mean()  # Adj. 200DMA

# 距 ATH
distance_from_ath = (current / ath - 1) * 100

# RS vs SPY (30-day momentum ratio)
stock_ret = df['Close'].iloc[-1] / df['Close'].iloc[-30] - 1
spy_ret = spy_df['Close'].iloc[-1] / spy_df['Close'].iloc[-30] - 1
rs_score = (stock_ret - spy_ret) * 100
```

#### 對應到 UI

所有欄位標示為 `Adj. Price` / `距 Adj. ATH` / `Adj. P&L`,並在每頁頂部用藍色橫幅明確提示。

#### 與 IBKR / TradingView 對照

- **IBKR 報價** 通常顯示**名目價**(配息以現金分配,股價會除息下跌)
- **TradingView K 線**有 "Adjusted for dividends" 選項,預設開啟
- **本系統** 與 TradingView 的 Adjusted 模式一致
- 操作時的盤中監看仍可用 IBKR 名目價(差距通常 < 5%,不影響進場決策)

---

### Phase 3 · 各子頁的 data
每個子頁讀對應的 `data-{module}.json`:
- `data-ath.json` — Base/Cont/Extended 三層清單
- `data-timing.json` — 可進場/等回踩/過熱三層清單
- `data-cockpit.json` — 持倉狀態 + Review 待答清單 + 證偽監控
- `data-rs.json` — 持倉/觀察清單 RS 計算結果

### Phase 4 · IBKR Flex Query 整合
持倉 Cockpit 從 IBKR Flex Query 自動同步真實持倉(已有 token-based 設計)。

### Phase 5 · 推播
LINE Notify 在以下事件觸發:
- 修正期 RS Board 從休眠 → 啟動(SPY drawdown 跨過 −7%)
- 證偽條件被觸發
- 新的 Base Breakout ATH 候選

---

## data.json Schema

```typescript
{
  timestamp_tpe: string,                    // "2026-05-10 06:00 TPE"
  last_update_minutes_ago: number,

  market: {
    spy_drawdown_from_ath_pct: number,      // 負數 = 距 ATH 跌幅
    qqq_six_state: string,                  // "S1 巡航" / "S2 防守" / "S5 重啟"
    qqq_grid_triggered: boolean,
    pure_ma_state: string,                  // "站上 50DMA" / "跌破 50DMA"
    pure_ma_color: "green" | "yellow" | "red",
    rs_board_dormant: boolean,
    rs_board_trigger_threshold_pct: number  // 預設 -7.0
  },

  actions: [
    {
      type: "ATH" | "REVIEW" | "TIMING" | "FALSIFICATION" | "RS",
      ticker: string,
      desc: string,
      link: string                          // 相對路徑
    }
  ],

  module_summaries: {
    ath_hunter: { base_count, continuation_count, extended_count, new_today_count, recent_buys[] },
    timing_board: { ready_to_enter_count, wait_pullback_count, overheated_count, active_signals_count },
    cockpit: { tier1_count, tier2_count, tier3_count, falsification_triggered_count, pending_review_tickers[] },
    rs_board: { is_active, current_drawdown_pct, needed_to_trigger_pct }
  }
}
```

---

## 後續可能的迭代

### 已知短板(等用一週後再決定要不要做)
- [ ] 季度 Thesis Review 三題的回答,目前無持久化機制(需要表單 + 寫回 GitHub)
- [ ] RS Board 觸發後的「加碼順序」演算法尚未實作
- [ ] 持倉 P&L 即時更新(需要 IBKR API)
- [ ] 證偽條件的自動監控 cron job

### 馬斯克第四、第五步(等架構穩定再做)
- 第四步 加速:把 Pipeline B 的 daily job 整合到 GitHub Actions,單一 repo 管理
- 第五步 自動化:LINE Notify 推播 + Discord webhook + Email weekly digest

---

## 哲學提醒

> 「**如果你刪掉一些東西之後,沒有至少 10% 的情況是需要把那些東西加回來的,那你一開始刪減得還不夠多。**」 — Elon Musk

- 第一週用完之後,**主動問自己哪些東西沒用上**,刪掉。
- 不是先全部保留然後一輩子在複雜度裡打轉。
- 不是先優化才質疑。**先質疑,再優化。**
