---
name: refresh-eps-screener-web
description: 用 Chrome 直接讀取 Koyfin watchlist（dd_screener 分頁）的 FY1/FY2/FY3E EPS 估值，重組成 DD_universe_EPS_estimates_YYYYMMDD.xlsx 並跑 build 更新 https://research.investmquest.com/dd-screener/。與 refresh-eps-screener（吃 Excel 檔）並列——差別在**資料來源是網頁抓取**，因為 Koyfin 的 Download 匯出不含分析師 EPS 估值欄（只能從畫面讀）。觸發：用戶丟 Koyfin watchlist URL 並說「用 chrome 讀數值更新 dd-screener」/「網頁更新 screener」/「從 koyfin 頁面更新 EPS」/「screener 用截圖來源更新」，或說「更新 dd-screener」但手邊沒有新的 EPS Excel 檔。
version: v1.0
date: 2026-07-16
---

# Workflow: refresh-eps-screener-web

**定位**：`refresh-eps-screener` 的姊妹 skill。當用戶手邊**沒有** `DD_universe_EPS_estimates_YYYYMMDD.xlsx`（Koyfin Download 不含 FY 估值欄，用戶平常是「截圖轉 Excel」）時，改用 Chrome 直接抓 watchlist 畫面數值，重組出同一份 xlsx，再走既有 build pipeline。**下游完全共用** `refresh-eps-screener` 的機制（build_dd_screener.py、snapshot、FX、6 個 variant 頁）。

**模型**：Sonnet 可跑（機械層 script 為主）。唯一需要判斷的是 §Step 5 分割/異常 gate——那步是**硬 gate**，不准跳、不准想當然，必須逐檔查 corporate action。

## 先決條件（命中就先停下問用戶）

- 用戶未給 watchlist URL 且無法從對話推得 → 問 URL。
- Chrome 未登入 Koyfin（畫面停在 login）→ 請用戶先登入，不要代為輸入帳密（憲法禁止）。
- watchlist 幣別 toggle 不是 **USD**（右上角）→ 停下確認；本 pipeline 假設 Excel 為 USD，非美股由 build 的 FX 層換算。

否則照下列 8 步跑完。

---

## Step 0 — 開頁面，確認 dd_screener 分頁 + USD

1. `ToolSearch` 載入 browser 工具：`tabs_context_mcp, navigate, computer, javascript_tool, read_console_messages`。
2. `tabs_context_mcp{createIfEmpty:true}` → `navigate` 到 watchlist URL → `computer screenshot`。
3. 確認：作用分頁是 **dd_screener**（不是 dd_screener-temp 或其他）；右上角幣別是 **USD**。若分頁不對，點 dd_screener 分頁。

## Step 1 — 注入抓取器（表頭驅動，耐欄位重排）

用 `javascript_tool` 注入一次。**用表頭文字定位欄位**，不 hardcode index（用戶可能重排 watchlist 欄位）：

```javascript
(() => {
  window.__eps = window.__eps || {};
  const TICK_RE = /^[•\s]*([A-Z0-9]{1,6}(?:\.[A-Z]{1,3})?)$/;
  // header text -> we need Ticker + the three "EPS Norm - Est Avg (FYnE)" columns
  const heads = [...document.querySelectorAll('.table-styles__table__headerCell___gC361')]
                  .map(h => h.innerText.replace(/\s+/g,' ').trim());
  const idx = {ticker:-1, fy1:-1, fy2:-1, fy3:-1};
  heads.forEach((h,i) => {
    const l = h.toLowerCase();
    if (l === 'ticker') idx.ticker = i;
    else if (l.includes('eps norm') && l.includes('fy1')) idx.fy1 = i;
    else if (l.includes('eps norm') && l.includes('fy2')) idx.fy2 = i;
    else if (l.includes('eps norm') && l.includes('fy3')) idx.fy3 = i;
  });
  const countryIdx = heads.findIndex(h => h.toLowerCase()==='country');
  window.__epsIdx = idx;
  window.grabEps = function(){
    let n=0;
    document.querySelectorAll('.table-styles__table__row___K6TSS').forEach(row=>{
      const cells=[...row.querySelectorAll('.table-styles__table__dataCell___nRZp0')]
                    .map(c=>c.innerText.replace(/\s+/g,' ').trim());
      if (cells.length < heads.length) return;
      const m=(cells[idx.ticker]||'').match(TICK_RE);
      if(!m) return;
      window.__eps[m[1]] = {
        fy1: cells[idx.fy1], fy2: cells[idx.fy2], fy3: cells[idx.fy3],
        country: countryIdx>=0 ? cells[countryIdx] : ''
      };
      n++;
    });
    return n;
  };
  window.__epsSC = document.querySelector('.table-styles__table__scrollContainer___WBAWY');
  return JSON.stringify({heads_found: idx, rows_class_seen: document.querySelectorAll('.table-styles__table__row___K6TSS').length});
})()
```

**Gate**：回傳的 `heads_found` 若有任一 = -1 → 表頭文字對不上（Koyfin 改欄名或欄位被移除），**停下**，回報用戶要人工確認欄位。**類別名（`.table-styles__...___XXXXX` 雜湊尾碼）可能隨 Koyfin 改版變動**——若 `rows_class_seen`=0，先用 `javascript_tool` 印出 scroll 容器內出現頻率最高的 class（≈ ticker 數）重新校準 selector。

## Step 2 — 游標式捲動累積（虛擬列表關鍵）

這個表是**虛擬列表**：一次只渲染 ~23 列，且**不跟隨程式設定的 scrollTop**——必須 `scrollTop += step` 後**派發 `scroll` 事件**才會重渲染。每次 `javascript_tool` 呼叫約只跑 ~6-12 步就被超時砍掉，所以用**持久游標 `window.__y`**分多次呼叫續跑（每步即時寫入 `window.__eps`，超時被砍也保留進度）：

```javascript
(async () => {
  const sleep = ms => new Promise(r=>setTimeout(r,ms));
  const sc = window.__epsSC; const H = sc.scrollHeight;
  if(window.__y==null) window.__y=0;
  let iter=0;
  while(window.__y <= H+400 && iter < 12){
    sc.scrollTop = window.__y;
    sc.dispatchEvent(new Event('scroll',{bubbles:true}));
    await sleep(100); window.grabEps(); window.__y += 340; iter++;  // step 340px < ~630px viewport → 有重疊不漏列
  }
  return "";  // 回傳常被吞成 {}，正常
})()
```

**重複呼叫這段**（4-6 次）直到 `window.__y > scrollHeight`。每次呼叫後查進度：
```javascript
JSON.stringify({y:window.__y, H:window.__epsSC.scrollHeight, total:Object.keys(window.__eps).length})
```
到底後再從 `window.__y=0`（另設 `window.__y2`）**小步幅（160px）回掃一輪**補渲染空白幀漏抓的列。

## Step 3 — 對帳（找漏檔）

抓 latest.json 的 bare-ticker universe，與 `window.__eps` 做雙向差集：

```bash
python3 -c "
import json
d=json.load(open('docs/dd-screener/latest.json'))
sufs=('.TW','.T','.JP','.HK','.KS','.KQ','.SS','.SZ','.AX','.SW','.FR','.L','.DE','.PA','.MI','.TO','.SI')
def bare(t):
    for s in sufs:
        if t.endswith(s): return t[:-len(s)]
    return t
print(','.join(sorted(set(bare(s['ticker']) for s in d['stocks']))))
"
```
把清單餵進 `javascript_tool` 做差集（別名：universe `LVMH` ↔ watchlist `MC`）：
```javascript
(() => {
  const expected = "PASTE_BARE_LIST".split(',');
  const alias = {LVMH:'MC'};  // watchlist 用主掛牌代碼；有新別名往這加
  const have = new Set(Object.keys(window.__eps));
  const missing = expected.filter(t => !have.has(t) && !have.has(alias[t]||''));
  const extra = Object.keys(window.__eps).filter(t => !expected.includes(t) && !Object.values(alias).includes(t));
  return JSON.stringify({have:have.size, expected:expected.length, missing, extra});
})()
```
**已知合理漏檔**：Koyfin 對某些 US ADR / 冷門股不提供 FY 估值（歷來是 `BLK / KLIC / ROP / STZ`），這些會顯示 no-data 列、抓不到，是**正常**——它們走 yfinance fallback（比照 latest.json `eps_estimates_source.missing_us_adr_tickers`）。`extra` 應為空；非空代表 universe 有變或別名沒補。

## Step 4 — 指紋校驗（零轉抄保證）

資料只能經 console 逐行倒出（頁面數值截斷限制）。**先在瀏覽器算指紋，落檔後重算比對**，一致才算數：

瀏覽器端：
```javascript
(() => {
  const e=window.__eps, keys=Object.keys(e).sort();
  const canon = keys.map(k=>[k,e[k].fy1,e[k].fy2,e[k].fy3].join('|')).join('\n');
  let h=5381; for(let i=0;i<canon.length;i++){h=((h<<5)+h+canon.charCodeAt(i))>>>0;}
  return JSON.stringify({rows:keys.length, bytes:canon.length, djb2:h});
})()
```
倒資料：`console.log('EPSROW|'+[k,fy1,fy2,fy3,country].join('|'))` 逐檔，再 `read_console_messages{pattern:'EPSROW', limit:300}` 讀回全部。把 `EPSROW|` 後的 `ticker|fy1|fy2|fy3`（**照 sorted 順序、無尾換行**）寫入 scratchpad `eps_raw_YYYYMMDD.txt`，Python 重算 djb2：
```python
s=open(path).read().rstrip('\n'); h=5381
for ch in s: h=((h<<5)+h+ord(ch))&0xffffffff
# 必須 rows/bytes/djb2 三者與瀏覽器端一致，否則不准往下走
```
**三者不一致 → 停下**（漏行 / 轉抄錯 / 排序不同），重讀 console。

## Step 5 — 分割 / 異常 gate（**唯一判斷步驟，硬 gate，不准跳**）

用 loader 讀新舊兩份 xlsx（或對 baseline snapshot），掃 **|FY1 移動| ≥ 35% 或翻號** 的 ticker。每一檔都必須查明原因，**不可想當然**（教訓：2026-07-16 KLAC/CRWD 差 10x/4x，我一度誤判成「資料損毀」，其實是股票分割）：

**判斷決策樹**（對每個 flagged ticker）：
1. **三個 FY 一起呈乾淨整數倍縮放（≈ ÷10、÷4、÷2…）** → 極可能**股票分割**。`WebSearch "{ticker} stock split {year}"` 確認。若確認：
   - **保留** watchlist 的分割後值（那是正確的新基準）。
   - 把 **baseline snapshot（`2026-06.json` 等）該檔的絕對 EPS ÷ 分割比**（`eps_fy_curr/eps_fy_next/eps_fy3/eps_0y/eps_1y/trailing_eps`），revision 才誠實（否則假 -90%/-75% 下修污染 funnel_rank）。**改寫 baseline 前先備份到 scratchpad，並需用戶授權**（改既有歷史檔會被權限攔）。
2. **塌成近零 / 對明顯獲利公司變負 / Country 欄映射錯（如 ABB 顯示 CA）** → **Koyfin 壞資料**。從 xlsx **剔除**該檔 → 走 yfinance fallback。
3. **小額、方向一致、非乾淨倍率（如虧轉盈軌跡）** → **真實分析師修正**，保留。
4. 查不出原因 → 停下回報用戶，不要自行決定。

歐股 / ADR 特別注意 FX 與掛牌別名（LVMH→MC、SU、RMS 等）。

## Step 6 — 建 xlsx

7 欄 schema（loader 只讀前 4，growth/CAGR 留空由 build 自算），Sheet1「EPS Estimates」+ Sheet2「Notes」B2=snapshot 日期。`-` → 空格。**剔除清單**（Step 5 判定的壞值）不寫入：

```python
from openpyxl import Workbook
wb=Workbook(); ws=wb.active; ws.title="EPS Estimates"
ws.append(["Ticker","FY1E EPS","FY2E EPS","FY3E EPS","FY1->FY2 Growth %","FY2->FY3 Growth %","FY1->FY3 CAGR %"])
for t,f1,f2,f3 in rows:  # rows 已排除 DROP 清單
    ws.append([t,f1,f2,f3,None,None,None])
ws2=wb.create_sheet("Notes")
ws2["A2"]="Snapshot Date"; ws2["B2"]="YYYY-MM-DD"
ws2["B5"]="split/exclusion notes here"
wb.save("data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx")
```
落檔後**用 loader 回讀驗證**：`load_excel(path)` → ticker 數對、抽查 3-5 檔值、剔除的不在、`-` 正確變 None。

## Step 7 — 跑 build + 驗證

```bash
python3 scripts/build_dd_screener.py         # 全量 ~6-8 分鐘（背景跑），需 yfinance
```
log 要看到 `Excel EPS source: DD_universe_EPS_estimates_YYYYMMDD.xlsx (snapshot YYYY-MM-DD, covers N/N)`。build 完驗 `latest.json`：
- `universe_size` 合理、`as_of` = 今日
- **Step 5 分割檔的 revision ≈ 0%**（baseline 已調 → 不再是假下修）：查 `eps_fy_curr_revision_pct`
- 抽查幾檔 FY EPS 已更新成新值
- TW 檔 FX 有 fire（`eps_fx_rate` 非 None、`eps_display_currency`=TWD）
- 剔除檔 `eps_source` 應為 yfinance

## Step 8 — Commit + push（用戶說 push 才做）

**預設停下等用戶複審**；用戶說 push 才 commit。先 `git pull --rebase`。只 stage 本次 bundle（**不要 `git add -A`**——會誤掃並行 session 的 DD 新檔）：

```bash
git add \
  data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx \
  docs/dd-screener/eps-estimates-snapshots/PRIOR-MONTH.json \  # 若 Step 5 調過 baseline
  docs/dd-screener/latest.json \
  docs/dd-screener/alpha-rank.{json,html} docs/dd-screener/bottom-out.{json,html} \
  docs/dd-screener/breakout.{json,html} docs/dd-screener/earnings-acceleration.{json,html} \
  docs/dd-screener/entry-state.{json,html} docs/dd-screener/quality-entry.{json,html}
python3 scripts/qc.py    # QC gate 必過
git commit -m "dd-screener: YYYYMMDD web-scraped EPS (splits X/Y adjusted, Z excluded)"
git pull --rebase && git push origin main   # 抄 canonical rebase-retry（repo 有 20+ 夜間 cron 擠 main）
```
commit 訊息列出：universe 數、分割調整檔、剔除檔、baseline 日期。**不需跑 `update_dd_index.py`**（此 workflow 不動 docs/dd/）。

## 關鍵 invariants（每次 run 都 hold）

1. **指紋校驗不能跳**（Step 4）——瀏覽器 djb2 = 落檔 djb2，這是零轉抄的唯一保證。
2. **分割 gate 不准想當然**（Step 5）——|FY1|≥35% 或翻號的每一檔都要查 corporate action；乾淨倍率＝分割（保留+調 baseline），塌零/翻負＝壞值（剔除）。
3. **分割檔要調 baseline**——否則 revision 假下修污染 funnel_rank；改 baseline 需備份 + 用戶授權。
4. **Excel 一律 USD**——非美股 FX 由 build 換算，不手動轉。
5. **表頭驅動取欄**（Step 1）——別 hardcode column index；Koyfin 改版時 class 雜湊尾碼也可能變，`rows_class_seen`=0 要重新校準 selector。
6. **Commit scope tight**——只 add dd-screener bundle，不 add docs/dd/。
7. **對帳 extra 應為空**——非空代表 universe 或別名沒同步。

## 與 refresh-eps-screener 的差異速查

| | refresh-eps-screener | refresh-eps-screener-web（本 skill） |
|---|---|---|
| 資料來源 | `DD_universe_EPS_estimates_*.xlsx` 檔 | Koyfin watchlist 畫面（Chrome 抓） |
| 為何存在 | 有現成 Excel | Koyfin Download 不含 FY 估值欄 |
| 驗證 gate | Excel Notes 第 8 列 spot-check | djb2 指紋 + 對帳 + 分割 gate |
| 下游 | 完全相同（snapshot / build / FX / variant 頁 / commit bundle） | 同左 |
