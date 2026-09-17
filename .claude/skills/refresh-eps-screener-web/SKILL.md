---
name: refresh-eps-screener-web
description: 用 Chrome 直接讀取 Koyfin watchlist（dd_screener 分頁）的**全部欄位**（EPS 估值＋35 個體質/衰退/估值機械閘欄位＋2 個籌碼面欄位，共 56 欄），重組成 DD_universe_EPS_estimates_YYYYMMDD.xlsx 並跑 build 更新 https://research.investmquest.com/dd-screener/。與 refresh-eps-screener（吃 Excel 檔）並列——差別在**資料來源是網頁抓取**，因為 Koyfin 的 Download 匯出不含分析師 EPS 估值欄（只能從畫面讀）。觸發：用戶丟 Koyfin watchlist URL 並說「用 chrome 讀數值更新 dd-screener」/「網頁更新 screener」/「從 koyfin 頁面更新 EPS」/「screener 用截圖來源更新」，或說「更新 dd-screener」但手邊沒有新的 EPS Excel 檔。
version: v2.0
date: 2026-09-17
---

# Workflow: refresh-eps-screener-web

**定位**：`refresh-eps-screener` 的姊妹 skill。當用戶手邊**沒有** `DD_universe_EPS_estimates_YYYYMMDD.xlsx`（Koyfin Download 不含 FY 估值欄，用戶平常是「截圖轉 Excel」）時，改用 Chrome 直接抓 watchlist 畫面數值，重組出同一份 xlsx，再走既有 build pipeline。**下游完全共用** `refresh-eps-screener` 的機制（build_dd_screener.py、snapshot、FX、6 個 variant 頁）。

**v2.0（2026-09-17）與 v1.0 的差異**：v1.0 只逐一具名索引 EPS 三欄＋ROIC／FCF Margin／ROIC 5Y Avg 三個選填欄（`idx.fy1`/`idx.roic` 這種寫法）。2026-09-17 同一天兩輪擴欄（先加 35 個體質/衰退/估值機械閘欄位，再加 2 個籌碼面欄位）證明「逐一具名索引」的寫法已不敷使用——v2.0 全面改成**表頭驅動、抓全部欄位**（`grabAll()` 對任何表頭一視同仁存值），watchlist 現在加到幾欄都不用改抓取器程式碼，只需要在 Step 6 的**欄序清單 F** 與 xlsx header 契約表補一行。下游 loader（`load_eps_estimates_xlsx.py`）的「選填、缺欄一律 None、舊 xlsx 零影響」相容性保證從 v1.0 延續到 v2.0 沒有變。

**模型**：Sonnet 可跑（機械層 script 為主）。唯一需要判斷的是 §Step 5 分割/異常 gate——那步是**硬 gate**，不准跳、不准想當然，必須逐檔查 corporate action。

## 先決條件（命中就先停下問用戶）

- 用戶未給 watchlist URL 且無法從對話推得 → 問 URL。
- Chrome 未登入 Koyfin（畫面停在 login）→ 請用戶先登入，不要代為輸入帳密（憲法禁止）。
- watchlist 幣別 toggle 不是 **USD**（右上角）→ 停下確認；本 pipeline 假設 Excel 為 USD，非美股由 build 的 FX 層換算。

否則照下列 8 步跑完。

---

## Step 0 — 開頁面，確認 dd_screener 分頁 + USD

1. `ToolSearch` 載入 browser 工具：`tabs_context_mcp, navigate, computer, find, javascript_tool, read_console_messages, tabs_close_mcp`。
2. `tabs_context_mcp{createIfEmpty:true}` → `navigate` 到 watchlist URL → `computer screenshot`。
3. 確認：作用分頁是 **dd_screener**（不是 dd_screener-temp 或其他）；右上角幣別是 **USD**。若分頁不對，點 dd_screener 分頁。

## Step 0.5 — （選用）用「Columns」對話框新增欄位

只在這輪要**新增 watchlist 欄位**時才需要這步（例如本次新增「短線利空/內部人」兩欄）；watchlist 欄位不變時直接跳到 Step 1。

1. `find` 「Columns button」（`role="dialog"` 開關鈕），`computer.left_click` 開啟「Column Selection」對話框。
2. 在對話框的搜尋框（`input[placeholder*="Search available"]`）打關鍵字（如 "Short Interest"、"Insider"），用下面 helper 設值＋派發 `input` 事件（**必須派發事件**，直接設 `.value` 不會觸發 React 重渲染）：
   ```js
   window.__search2 = async (q) => {
     const inp = document.querySelector('input[placeholder*="Search available"]');
     const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
     set.call(inp, q);
     inp.dispatchEvent(new Event('input', { bubbles: true }));
     await new Promise(r => setTimeout(r, 900));
     return 'searched:' + q;
   };
   await window.__search2('Short Interest');
   ```
3. 有些指標（如 Short Interest／Insider）會先給一個**分類節點**（例：「Short Interest」本身沒有加入動作，點下去會展開「% / M / FQH / FYH / HA / HGQOQ / HGYOY / TG」子選單），要先進子選單，再點真正的葉節點（如「% Of Shares Outstanding」）。子選單有無由該行是否帶 `>` 箭頭決定，箭頭本身不能點（是純顯示），要點整行文字。
4. ⚠️ **「加入」的點擊目標必須是最內層的 label 節點，不是外層整列 div——這是本次實測踩到的坑**：Koyfin 這個對話框的每一列是巢狀 `<div>`，外層整列 div 也掛了 `onclick`（但那個 handler 只是「預覽/高亮」，不會真的把欄位加進「Selected Columns」），只有内层文字 label 的 `onclick` 才會真正觸發「加入」動作。座標點擊（`computer.left_click` 給 x,y）點到的常常是外層 wrapper，看起來有反應（那一列會變藍色高亮）但欄位其實沒被加入——**唯一可靠的做法是用文字精準比對＋點擊清單中最後一個匹配的 DOM 節點**（`querySelectorAll` 依文件順序回傳，同一段文字若巢狀出現多次，最後一個通常是最深層、真正掛加入動作的節點）：
   ```js
   window.__ct2 = (txt) => {
     const els = [...document.querySelectorAll('[role="dialog"] div,[role="dialog"] span')]
       .filter(e => e.innerText && e.innerText.trim() === txt && e.getBoundingClientRect().width > 0);
     if (!els.length) return 'NOTFOUND:' + txt;
     els[els.length - 1].click();
     return 'ok:' + txt + ' count=' + els.length;
   };
   window.__ct2('% Of Shares Outstanding');   // 加入子選單葉節點
   ```
   加入是否成功用「Selected Columns」清單的筆數變化驗證（不要只看有沒有變藍）：
   ```js
   const container = document.querySelector('[class*="koyDataSourceResults__draggableItem"]')?.closest('[class*="koyDataSourceResults___"]');
   ```
   更穩妥的作法是直接數 `.koy-data-source-results__koyDataSourceResults__draggableItem___*` 這個 class 前綴（雜湊尾碼會變，見下方 CSS hash 輪換說明）的節點數，加入前後應該 +1。
5. ⚠️ **這整段（搜尋＋展開子選單＋點加入）必須在同一次 `javascript_tool` 呼叫內同步跑完，不要拆成好幾次呼叫中間穿插等待**——對話框是彈出層，跨呼叫之間如果分頁被判定為背景分頁，DOM 節點的 event listener 綁定可能因為 re-render 時機被打散（實測：拆呼叫時偶爾會出現「這次呼叫看到的高亮列」跟「上次呼叫加入的列」對不上的情況）。單次呼叫預算 30 秒內綽綽有餘（`__search2` 的 900ms 等待＋兩三次點擊）。
6. 全部欄位加完後，`find` 「close X button」→ `computer.left_click` 關閉對話框，**重新整理頁面**（`navigate` 同一個 URL），等表格重新載入，再用下面指令確認新表頭真的出現在表格裡（不要只信對話框裡「Selected Columns」清單，重整後表格是否真的渲染出來才算數）：
   ```js
   const sc = document.querySelector('[class*="table__scrollContainer___"]');
   const maxScroll = sc.scrollWidth - sc.clientWidth;
   const out = new Set();
   for (let left = 0; left <= maxScroll + 1200; left += 1200) {
     sc.scrollLeft = left; sc.dispatchEvent(new Event('scroll', { bubbles: true }));
     await new Promise(r => setTimeout(r, 300));
     document.querySelectorAll('[class*="table__headerCell___"]').forEach(h => {
       const t = h.innerText.replace(/\s+/g, ' ').trim(); if (t) out.add(t);
     });
   }
   JSON.stringify({ headerCount: out.size, hasNewCol: [...out].some(t => t.includes('關鍵字')) });
   ```
   2026-09-17 實測：加兩欄前 78 欄、加完 80 欄（見文末「欄位盤點」表）。

## Step 1 — 注入抓取器（表頭驅動，v2.0 抓全部欄位）

用 `javascript_tool` 注入一次（**同步、快，< 1 秒**）。v2.0 不 hardcode 任何具名欄位，一律用**目前畫面上實際渲染出來的表頭文字**當 key：

```js
window.__eps = {}; window.__hdrs = new Set();
window.__epsSC = document.querySelector('[class*="table__scrollContainer___"]');
window.__TICK_RE = /^[•\s]*([A-Z0-9]{1,8}(?:\.[A-Z]{1,3})?)$/;   // 8 碼：99SMART、TAKAFUL 這類長 ticker
window.grabAll = function () {
  const heads = [...document.querySelectorAll('[class*="table__headerCell___"]')]
    .map(h => h.innerText.replace(/\s+/g, ' ').trim());
  heads.forEach(h => h && window.__hdrs.add(h));
  const ti = heads.indexOf('Ticker'); if (ti < 0) return -1; let n = 0;
  document.querySelectorAll('[class*="table__row___"]').forEach(row => {
    const cells = [...row.querySelectorAll('[class*="table__dataCell___"]')]
      .map(c => c.innerText.replace(/\s+/g, ' ').trim());
    if (cells.length < heads.length) return;
    const m = (cells[ti] || '').match(window.__TICK_RE); if (!m) return;
    const rec = window.__eps[m[1]] || (window.__eps[m[1]] = {});
    heads.forEach((h, i) => { if (h && h !== 'Ticker' && cells[i] !== undefined && cells[i] !== '') rec[h] = cells[i]; });
    n++;
  }); return n;
};
window.__pass = async function (left, step) {   // 一段橫向位置、整條縱向掃完
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const sc = window.__epsSC; const H = sc.scrollHeight;
  sc.scrollLeft = left; sc.dispatchEvent(new Event('scroll', { bubbles: true })); await sleep(400);
  window.__curLeft = left; window.__y = 0;
  while (window.__y <= H + 400) {
    sc.scrollTop = window.__y; sc.dispatchEvent(new Event('scroll', { bubbles: true }));
    await sleep(120); window.grabAll(); window.__y += 340;   // step 340px < ~630px viewport → 有重疊不漏列
  }
};
```

**CSS class 雜湊會輪換**（歷次實測：`headerCell___gC361`→`___I7R3q`→`___xxxxx`……、`row___K6TSS`、`dataCell___nRZp0`、`scrollContainer___WBAWY` 尾碼每次改版都會換，四個全換過）。上面已一律用 `[class*="table__headerCell___"]` 這類**前綴選擇器**，對尾碼輪換免疫，不需要每次改版回來改 skill。若哪天連 `table__xxx___` 中段也變了（全部抓到 0 列），才用 `javascript_tool` 印出 scroll 容器內出現頻率最高的 class（≈ ticker 數）重新校準。

**（沿革，v1.0 世代）**：v1.0 的 `grabEps()` 具名索引 `idx.fy1`/`idx.roic`/`idx.fcfm`/`idx.roic5y` 四五個特定欄位，把 ROIC／FCF Margin／ROIC 5Y Avg 三欄當「選填」特判（抓不到就存 `null`，不擋 Ticker/EPS 三欄的 gate）。v2.0 的 `grabAll()` 對**任何**表頭一視同仁存值，「選填」的概念不再存在於抓取器層——不管畫面上有幾欄都照樣存，真正的「選填」語意留給下游 `load_eps_estimates_xlsx.py`（缺欄一律 `None`，不擋任何既有邏輯，這個相容性保證沒有變）。

## Step 1.5 — 橫向多段掃描（取代 v1.0「先捲到底再抓 EPS 三欄」）

v2.0 目標是抓**全部欄位**（現在 80 欄，橫向寬度早已數倍於可視寬度），不能只捲到最右一次讀——必須**分段**：每段先定橫向位置，在該段內做一次完整縱向掃描（`__pass()`），抓到的欄位會因橫向位置不同而不同，全部累積寫進同一個 `window.__eps[ticker]` 物件，跑完所有段才會集滿 80 欄。

**段數計算**（用實際 `clientWidth` 校正最後一段，避免超出可捲範圍——比單純 `ceil(scrollWidth/1500)+1` 準確）：

```js
const sc = window.__epsSC;
const maxScroll = sc.scrollWidth - sc.clientWidth;
const segs = []; for (let l = 0; l < maxScroll; l += 1500) segs.push(l); segs.push(maxScroll);
```

2026-09-17 實測：`scrollWidth=7696`、`clientWidth=1838` → `maxScroll=5858` → 5 段 `[0, 1500, 3000, 4500, 5858]`（等同 `ceil(7696/1500)+1=6` 段的近似值，但最後一段用實際可捲範圍取代死板的 `5*1500=7500`，避免捲過頭卡在空白區）。

**啟動（fire-and-forget，不要在同一次呼叫裡等它跑完）**：

```js
window.__running = true; window.__passLog = [];
(async () => {
  for (const L of segs) {
    await window.__pass(L, 340);
    window.__passLog.push([L, Object.keys(window.__eps).length, window.__hdrs.size]);
  }
  window.__running = false;
})();
```

**⚠️ Gotcha — background 分頁計時器節流（2026-09-17 實測，務必解釋給後續操作者）**：這一步橫跨數十次 `setTimeout`。Chrome 對非前景分頁（本工具用自動化操作，分頁不一定是使用者視覺焦點）的計時器會嚴重節流——名目 120ms 的縱向捲動間隔實測常常變成 5-60 秒一步，全部 5 段跑完（每段縱向約 27 步）可能耗時 **15-30 分鐘**。這是**正常現象，不是卡死**：

- 用 `computer.wait{duration:10}` 分批等待，搭配輪詢確認進度前進：
  ```js
  JSON.stringify({ running: window.__running, total: Object.keys(window.__eps).length,
                    hdrs: window.__hdrs.size, log: window.__passLog, y: window.__y, curLeft: window.__curLeft })
  ```
- 只要 `y` 或 `total` 持續前進（即使很慢），**不要重新注入 Step 1 或中斷重跑**——`window.__eps` 是累積寫入的全域物件，中途查詢不影響背景 loop，重新注入反而會清空已抓的資料重來。
- 等待期間可以並行處理其他不需要瀏覽器的步驟（本次任務即示範：一邊等 scrape、一邊改 loader/screener/engine 程式碼與跑單元測試）。
- `window.__running === false` 且 `Object.keys(window.__eps).length` 等於預期母體數（見 Step 3 對帳）才算完成；若卡在某個 `total` 數字不再變且 `y` 也不再變超過 2-3 分鐘，才需要懷疑是不是真的卡死（少見，通常是分頁被導航掉或 tab 被關閉）。

## Step 2 — 倒出＋落檔（KROW 格式，取代 v1.0 的 EPSROW）

`window.__running === false` 後，用**欄序清單 F**（= xlsx header 契約表「Koyfin 表頭」欄，依文末表格順序排列——**必須是 Koyfin 畫面上的原文字**，因為 `grabAll()` 是拿這個字串當 key 存值，跟 xlsx 欄名不同名會全部抓空）逐檔印出：

```js
const F = [ /* 見文末「Step 6 xlsx 表頭契約」表格的「Koyfin 表頭」欄，依序列出 53 個 */ ];
const keys = Object.keys(window.__eps).sort();
keys.forEach(k => {
  const rec = window.__eps[k];
  console.log('KROW|' + [k, ...F.map(f => rec[f] || '')].join('|'));
});
```

`read_console_messages{pattern:'KROW\\|', limit:320}` 讀回全部（母體 ~300 檔時 `limit` 給夠餘裕，別讓後面的訊息把前面的擠出緩衝區）。把 `KROW|` 後的整行（含 ticker，逐檔、**照 sorted 順序、無尾換行**）寫入 scratchpad `koyfin_raw_YYYYMMDDb.txt`（`b` 尾碼區分同日第二輪抓取；若整天只抓一次沿用無尾碼檔名）。

## Step 3 — 對帳（找漏檔，不變）

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

## Step 4 — 指紋校驗（KROW 版，取代 v1.0 的 EPSROW，零轉抄保證）

資料只能經 console 逐行倒出（頁面數值截斷限制）。**先在瀏覽器算指紋，落檔後重算比對**，一致才算數。瀏覽器端（含 Step 2 用的完整欄序 `F`，不只 EPS 三欄）：

```js
(() => {
  const keys = Object.keys(window.__eps).sort();
  const canon = keys.map(k => [k, ...F.map(f => window.__eps[k][f] || '')].join('|')).join('\n');
  let h = 5381; for (let i = 0; i < canon.length; i++) { h = ((h << 5) + h + canon.charCodeAt(i)) >>> 0; }
  return JSON.stringify({ rows: keys.length, bytes: canon.length, djb2: h });
})()
```

落檔後 Python 重算 djb2（同演算法，逐字元）：
```python
s=open(path).read().rstrip('\n'); h=5381
for ch in s: h=((h<<5)+h+ord(ch))&0xffffffff
# 必須 rows/bytes/djb2 三者與瀏覽器端一致，否則不准往下走
```
**三者不一致 → 停下**（漏行 / 轉抄錯 / 排序不同），重讀 console。

## Step 5 — 分割 / 異常 gate（**唯一判斷步驟，硬 gate，不准跳**）

用 loader 讀新舊兩份 xlsx（或對 baseline snapshot），掃 **|FY1 移動| ≥ 35% 或翻號** 的 ticker。每一檔都必須查明原因，**不可想當然**（教訓：2026-07-16 KLAC/CRWD 差 10x/4x，一度誤判成「資料損毀」，其實是股票分割）：

**判斷決策樹**（對每個 flagged ticker）：
1. **三個 FY 一起呈乾淨整數倍縮放（≈ ÷10、÷4、÷2…）** → 極可能**股票分割**。`WebSearch "{ticker} stock split {year}"` 確認。若確認：
   - **保留** watchlist 的分割後值（那是正確的新基準）。
   - 把 **baseline snapshot（`2026-06.json` 等）該檔的絕對 EPS ÷ 分割比**（`eps_fy_curr/eps_fy_next/eps_fy3/eps_0y/eps_1y/trailing_eps`），revision 才誠實（否則假 -90%/-75% 下修污染 funnel_rank）。**改寫 baseline 前先備份到 scratchpad，並需用戶授權**（改既有歷史檔會被權限攔）。
2. **塌成近零 / 對明顯獲利公司變負 / Country 欄映射錯（如 ABB 顯示 CA）** → **Koyfin 壞資料**。從 xlsx **剔除**該檔 → 走 yfinance fallback。
3. **小額、方向一致、非乾淨倍率（如虧轉盈軌跡）** → **真實分析師修正**，保留。
4. 查不出原因 → 停下回報用戶，不要自行決定。

歐股 / ADR 特別注意 FX 與掛牌別名（LVMH→MC、SU、RMS 等）。

**35 個機械閘欄位＋2 個籌碼面欄位的合理範圍 gate**（2026-09-17 新增，選填欄位適用，比照既有的 ROIC／FCF Margin／ROIC 5Y Avg 範圍 gate）：百分比類欄位（Rev YoY／Gross Margin／Sales Growth／Op Income Growth／Price Chg 6M／Est CAGR／Below 52W High／**Short Interest % Float**）須落在 **−100 至 200（%）** 之間，超出範圍視為**壞格**——不是整檔剔除，只把該欄**空白化**（其餘欄位照留，該 ticker 繼續走 xlsx 主路徑）。倍數類（`x` 尾碼）與金額/股數類（含 **Insider Net Buy 3M**）欄位沒有統一範圍 gate，逐檔目視抓明顯異常值（如 PE NTM 出現負數或三位數以上、Insider Net Buy 3M 出現超過該公司流通股本量級的天文數字）。逐檔判斷不需要 WebSearch 查證（跟 Step 5 的分割 gate 不同層級，這裡只做粗篩），單純數值落在區間外就空白。

## Step 6 — 建 xlsx（`scripts/koyfin_xlsx_from_raw.py`）

2026-09-17 起改用 repo 內腳本（原本是每次手刻 openpyxl 片段，`koyfin_xlsx_from_raw.py` 把它固化並加上 argparse，同一份程式碼可重跑、可版本控制、可單元測試）：

```bash
python3 scripts/koyfin_xlsx_from_raw.py \
  --raw /path/to/koyfin_raw_YYYYMMDDb.txt \
  --out data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx \
  --snapshot-date YYYY-MM-DD
```

腳本內容：讀 Step 4 驗證過指紋的 raw txt（pipe-separated，每列 `ticker|f1|f2|...`），依下表「xlsx 欄名」順序建 56 欄 Sheet「EPS Estimates」＋ Sheet「Notes」（`B2`=snapshot 日期、`B3`="koyfin-web"、`B5`=欄位/單位/剔除紀錄）。`-`/空白/`—`/`N/A` 一律轉 `None`。**剔除清單**（Step 5 判定的壞值）不寫入。

### 完整表頭契約（56 欄：Koyfin 表頭 → xlsx 欄名 → loader 欄位 → 單位）

「比對方式」＝`exact`（`load_eps_estimates_xlsx.py` 的 `_NEW_FUND_HEADER_MAP` 精確字串比對，Koyfin 表頭文字改變或欄位重排都不影響，因為抓取器與 xlsx 建構都是同一份程式碼跑出來的，比對的是 xlsx 欄名不是 Koyfin 表頭）或 `loose`（loader 用 `"roic" in lv` 這類子字串規則，較舊、較寬鬆，但也較容易誤觸）。

| # | Koyfin 表頭（`grabAll()` 抓取 key） | xlsx 欄名 | loader 欄位 | 單位 | 比對方式 |
|---|---|---|---|---|---|
| 1 | Ticker | Ticker | `ticker` | — | exact |
| 2 | EPS Norm - Est Avg (FY1E) | FY1E EPS | `fy1` | EPS（原始貨幣，ADR 換算見 `apply_adr_ratio`） | loose (`fy1`+`eps`) |
| 3 | EPS Norm - Est Avg (FY2E) | FY2E EPS | `fy2` | EPS | loose |
| 4 | EPS Norm - Est Avg (FY3E) | FY3E EPS | `fy3` | EPS | loose |
| 5 | （build 自算，不從 Koyfin 讀） | FY1->FY2 Growth % | `growth_fy1_fy2_pct` | % | — |
| 6 | （build 自算） | FY2->FY3 Growth % | `growth_fy2_fy3_pct` | % | — |
| 7 | （build 自算） | FY1->FY3 CAGR % | `cagr_fy1_fy3_pct` | % | — |
| 8 | ROIC (LTM) | ROIC % | `roic_pct` | %（已含 % 記號，不做 ratio 換算） | loose (`roic`) |
| 9 | FCF Margin % (LTM) | FCF Margin % | `fcf_margin_pct` | % | loose (`fcf`+`margin`) |
| 10 | ROIC (5YAVG) | ROIC 5Y Avg % | `roic_5y_avg_pct` | % | loose (`roic`+`5y`) |
| 11 | EBIT Margin % (LTM) | EBIT Margin % | `ebit_margin_pct` | % | loose (`ebit`+`margin`) |
| 12 | ROIC (3YAVG) | ROIC 3Y Avg % | `roic_3y_avg_pct` | % | loose (`roic`+`3y`) |
| 13 | Effective Tax Rate - (Ratio) (FY) | Tax Rate % | `tax_rate_pct` | %（超出 [0,50%] 視為缺資料，downstream 預設 21%） | loose (`tax`+`rate`) |
| 14 | Total Revenues (FY) | Revenue FY | `rev_fy` | USD mm | loose (`revenue`+`fy`) |
| 15 | Total Revenues (-3FY) | Revenue FY-3 | `rev_fy3` | USD mm | loose |
| 16 | EBIT (FY) | EBIT FY | `ebit_fy` | USD mm（可能為負） | loose (`ebit`+`fy`) |
| 17 | EBIT (-3FY) | EBIT FY-3 | `ebit_fy3` | USD mm | loose |
| 18 | Inv. Cap. (FY) | Invested Capital FY | `ic_fy` | USD mm | loose (`invested`+`capital`) |
| 19 | Inv. Cap. (-3FY) | Invested Capital FY-3 | `ic_fy3` | USD mm | loose |
| 20 | Country（QA/對帳用，不寫入 xlsx） | — | — | — | — |
| 21 | Total Revenues (-0FQYoYFQ) | Rev YoY FQ0 % | `rev_yoy_fq0_pct` | % | **exact** |
| 22 | Total Revenues (-1FQYoYFQ) | Rev YoY FQ-1 % | `rev_yoy_fq1_pct` | % | **exact** |
| 23 | Total Revenues (-2FQYoYFQ) | Rev YoY FQ-2 % | `rev_yoy_fq2_pct` | % | **exact** |
| 24 | Total Revenues (-3FQYoYFQ) | Rev YoY FQ-3 % | `rev_yoy_fq3_pct` | % | **exact** |
| 25 | Gross Profit Margin % (LTM) | Gross Margin LTM % | `gm_ltm_pct` | % | **exact** |
| 26 | Gross Profit Margin % (-1FY) | Gross Margin FY-1 % | `gm_fy1_pct` | % | **exact** |
| 27 | Gross Profit Margin % (-2FY) | Gross Margin FY-2 % | `gm_fy2_pct` | % | **exact** |
| 28 | Gross Profit Margin % (-3FY) | Gross Margin FY-3 % | `gm_fy3_pct` | % | **exact** |
| 29 | Total Revenues (LTM) | Sales LTM | `sales_ltm` | USD mm | **exact** |
| 30 | EBIT (LTM) | Op Income LTM | `ebit_ltm` | USD mm | **exact** |
| 31 | Net Debt / EBITDA (LTM) | Net Debt / EBITDA x | `net_debt_ebitda_x` | x（淨現金或負 EBITDA 時空白） | **exact** |
| 32 | Total Revenues (-0FYYoYFQ) | Sales Growth YoY % | `sales_growth_fy_pct` | % | **exact** |
| 33 | EBIT (-0FYYoYFQ) | Op Income Growth YoY % | `ebit_growth_fy_pct` | % | **exact** |
| 34 | Avg Diluted Shares Out (FY) | Diluted Shares FY | `dil_shares_fy` | 股數（原始，非千股） | **exact** |
| 35 | Avg Diluted Shares Out (-3FY) | Diluted Shares FY-3 | `dil_shares_fy3` | 股數 | **exact** |
| 36 | Total Stock-Based Compensation (LTM) | SBC LTM | `sbc_ltm` | USD mm | **exact** |
| 37 | Capital Expenditure (LTM) | Capex LTM | `capex_ltm` | USD mm（負值） | **exact** |
| 38 | FCF (LTM) | FCF LTM | `fcf_ltm` | USD mm | **exact** |
| 39 | Net Debt (LTM) | Net Debt LTM | `net_debt_ltm` | USD mm（負＝淨現金） | **exact** |
| 40 | Cash Conversion Cycle (Average Days) (LTM) | CCC Days | `ccc_days` | 天數（負＝供應商融資） | **exact** |
| 41 | P/E (NTM) | PE NTM x | `pe_ntm_x` | x | **exact** |
| 42 | P/E (5YAVGNTM) | PE NTM 5Y Avg x | `pe_ntm_5y_avg_x` | x | **exact** |
| 43 | P/B (LTM) | PB x | `pb_x` | x | **exact** |
| 44 | P/B (5YAVG) | PB 5Y Avg x | `pb_5y_avg_x` | x | **exact** |
| 45 | RSI | RSI 14 | `rsi14` | 0-100 | **exact** |
| 46 | Price Chg. % (6M) | Price Chg 6M % | `price_chg_6m_pct` | % | **exact** |
| 47 | Repurchase of Common Stock (LTM) | Buyback LTM | `buyback_ltm` | USD mm（負值＝有回購） | **exact** |
| 48 | Price Target - High | Target High | `target_high` | 當地掛牌貨幣 | **exact** |
| 49 | Price Target - Low | Target Low | `target_low` | 當地掛牌貨幣 | **exact** |
| 50 | Price Target | Target Avg | `target_avg` | 當地掛牌貨幣 | **exact** |
| 51 | Net Income Margin % (LTM) | Net Income Margin LTM % | `ni_margin_ltm_pct` | % | **exact** |
| 52 | Est Rev CAGR (3Y) | Est Rev CAGR 3Y % | `est_rev_cagr_3y_pct` | % | **exact** |
| 53 | Est EPS CAGR (3Y) | Est EPS CAGR 3Y % | `est_eps_cagr_3y_pct` | % | **exact** |
| 54 | Below 52W High %, Adj | Below 52W High % | `below_52w_high_pct` | %（負值） | **exact** |
| 55 | Last Price | Last Price Local | `last_price_local` | 當地掛牌貨幣 | **exact** |
| 56 | Short Int. (%)（Columns 對話框長名：`Short Interest > % Of Shares Outstanding`） | Short Interest % Float | `short_interest_pct_float` | %（已含 % 記號，不做 ratio 換算） | **exact** |
| 57 | Insider Tr Shrs Net 3M（Columns 對話框長名：`Insider Transactions, Shares (Net) - 3M`） | Insider Net Buy 3M | `insider_net_buy_3m` | 股數（訊號，正＝淨買、負＝淨賣） | **exact** |

**本表全數逐字核對自 2026-09-17 實跑的 `window.__hdrs`**（80 欄全集，見 Step 1.5 的 `grabAll()` 累積結果），不是猜測或重建——`grabAll()` 存值用的 key 是**表格實際渲染的表頭文字**，這常常跟 Columns 對話框裡看到的完整描述性名稱不同（Koyfin 為了省版面會截短，例：對話框顯示「Insider Transactions, Shares (Net) - 3M」，但表格表頭實際渲染成「Insider Tr Shrs Net 3M」；「Short Interest > % Of Shares Outstanding」在表格渲染成「Short Int. (%)」）——**Step 2 的欄序清單 F 必須用表格渲染出來的短版字串，不是對話框的長版描述**，否則 `grabAll()` 全部抓空。部分欄名字面上有點奇怪（如「Total Revenues (-0FQYoYFQ)」／「EBIT (-0FYYoYFQ)」），這是 Koyfin 自訂期間選擇器產生的原始命名，照抄即可、不需要理解其命名邏輯。下次重跑此 skill 若 Koyfin 改版導致任一欄抓不到值，用 Step 0.5 的表頭列舉指令重新印出 `window.__hdrs` 全集，肉眼核對本表對應列並回填修正。

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
- **35 個機械閘欄位**：build log 的 `quality (koyfin-xlsx path): rows=N roic=X fcf=Y` 這行；抽查 3 檔 `latest.json` 的 `fund.*` 與 `quality_veto_level`/`decline_signal_light` 與 Koyfin 頁面數值比對一致
- **2026-09-17b 新增（籌碼面兩欄）**：抽查 3-5 檔 `latest.json` 的 `short_interest_pct_float`／`short_squeeze_flag`（>10 才 True）／`insider_net_buy_3m`／`insider_signal`（正→買、負→賣、0 或缺值→None）與 Koyfin 頁面數值一致；同時檢查 `docs/dd-screener/index.html` 的「籌碼」欄有正確渲染（SI% 上色、▲/▼ badge）
- **有加 ROIC 5Y Avg 欄時**：抽查 3 檔 `latest.json` 的 `durable_5y`/`durable_source`——有抓到值的 ticker `durable_source` 應為 `"koyfin-xlsx"`

Part 3（席位引擎）改動後另需：
```bash
python3 scripts/build_dd_screener.py --include-non-dd   # 若同時要更新席位引擎母體
python3.12 scripts/engine/build_arena.py                # 不帶 --ledger（手動跑唯讀帳本）
```
驗 `docs/engine/arena.json` 的 `core_seats`/`sat_seats` 有正確反映 `high_short_interest`（>10% 的名字應只出現在衛星，不在核心）、`base_effect`（三年 CAGR 因低基期跳增而改算的名字）、`cyclical`/`cycle_guard`（循環股 PEG 過低時分位封頂 50）。

## Step 8 — Commit + push（用戶說 push 才做）

**預設停下等用戶複審**；用戶說 push 才 commit。先 `git pull --rebase`。只 stage 本次 bundle（**不要 `git add -A`**——會誤掃並行 session 的 DD 新檔或其他排程寫入的檔案）：

```bash
git add \
  data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx \
  scripts/koyfin_xlsx_from_raw.py \
  scripts/load_eps_estimates_xlsx.py \
  scripts/build_dd_screener.py \
  scripts/engine/grp.py scripts/engine/build_arena.py \
  scripts/tests/test_grp_v4.py scripts/tests/test_fundamental_gates.py scripts/tests/test_arena_rotation_v4.py \
  knowledge/rule_ledger.md \
  docs/dd-screener/eps-estimates-snapshots/PRIOR-MONTH.json \  # 若 Step 5 調過 baseline
  docs/dd-screener/latest.json docs/dd-screener/index.html \
  docs/dd-screener/alpha-rank.{json,html} docs/dd-screener/bottom-out.{json,html} \
  docs/dd-screener/breakout.{json,html} docs/dd-screener/earnings-acceleration.{json,html} \
  docs/dd-screener/entry-state.{json,html} docs/dd-screener/quality-entry.{json,html} \
  docs/engine/arena.json docs/engine/board.txt docs/engine/_arena_body.html docs/engine/_board_body.html
python3 scripts/qc.py    # QC gate 必過
git commit -m "dd-screener: YYYYMMDD web-scraped EPS + 籌碼面兩欄（splits X/Y adjusted, Z excluded）"
git pull --rebase && git push origin main   # 抄 canonical rebase-retry（repo 有 20+ 夜間 cron 擠 main）
```
commit 訊息列出：universe 數、分割調整檔、剔除檔、baseline 日期、新增欄位。**`scripts/koyfin_xlsx_from_raw.py` 只在腳本本身有改動時才加進 commit**（第一次建立算改動）。**不需跑 `update_dd_index.py`**（此 workflow 不動 docs/dd/）。

## 關鍵 invariants（每次 run 都 hold）

1. **指紋校驗不能跳**（Step 4）——瀏覽器 djb2 = 落檔 djb2，這是零轉抄的唯一保證。
2. **分割 gate 不准想當然**（Step 5）——|FY1|≥35% 或翻號的每一檔都要查 corporate action；乾淨倍率＝分割（保留+調 baseline），塌零/翻負＝壞值（剔除）。
3. **分割檔要調 baseline**——否則 revision 假下修污染 funnel_rank；改 baseline 需備份 + 用戶授權。
4. **Excel 一律 USD**——非美股 FX 由 build 換算，不手動轉。
5. **表頭驅動取欄**（Step 1）——別 hardcode column index；class 一律用前綴選擇器（`[class*="table__row___"]`），Koyfin 雜湊尾碼輪換時免疫。
5b. **橫向多段掃描，不是「捲到底再抓」**（Step 1.5，v2.0 起）——80 欄橫向寬度數倍於可視寬度，只捲到底一次讀只能看到最右一段的欄位；必須用 `maxScroll/1500` 分段、每段各自完整縱向掃描、累積寫入同一個 `window.__eps`。
5c. **背景分頁計時器節流是常態，不是故障**（Step 1.5）——名目 120ms 的 sleep 實測可能變成數十秒一步，全程可能 15-30 分鐘；用輪詢＋耐心等待，不要中斷重跑。
5d. **Column Selection 對話框的「加入」動作，點擊目標必須是最內層 label 節點**（Step 0.5）——外層整列 div 的 `onclick` 只是預覽高亮，不會真的加入欄位；用文字精準比對＋點最後一個匹配節點（`els[els.length-1].click()`），且整段搜尋＋點擊要在同一次 `javascript_tool` 呼叫內同步跑完。
6. **精確表頭契約，不得用子字串規則接新欄**（Step 6，2026-09-17 起）——35+2 個新欄一律 EXACT 字串比對（`_NEW_FUND_HEADER_MAP`），**新增的 xlsx 欄名必須避開會被舊 loose 規則攔截的子字串**（尤其 `"revenue"` 與同時含 `"ebit"`+`"fy"`——這正是曾經讓 AAPL 的 `ebit_fy` 誤讀成 9.58〔一格 `"Op Income Growth YoY %"` 的雜訊〕而非 133050〔真正的 `"EBIT FY"`〕的那個 bug）；本次新增的「Short Interest % Float」／「Insider Net Buy 3M」皆已檢查過不含這些子字串。
7. **Commit scope tight**——只 add dd-screener／engine bundle，不 add docs/dd/，不 `git add -A`。
8. **對帳 extra 應為空**——非空代表 universe 或別名沒同步。
9. **35+2 個新欄一律選填、不擋任何既有 gate**（2026-09-17）——Step 1 抓不到某欄不擋 Ticker/EPS 三欄的抓取；Step 5 合理範圍外只空白化該格，不剔除整檔；沒抓到就不寫該欄（loader 對應欄位為 `None`），dd-screener 品質欄與相關旗標（`quality_veto_level`／`decline_signal_light`／`short_squeeze_flag`／`insider_signal`）全部 fail-open 顯示 `None`／`—`，不影響其餘欄位判定。
10. **融券高／內部人買賣不進 GRP 排序**（2026-09-17，見 `knowledge/rule_ledger.md`「v4.1 融券比 >10% 只能衛星」列）——`short_interest_pct_float > 10` 只排除核心候選資格（衛星照樣能坐），內部人訊號純粹是席位表備註 badge；兩者都**不是** `own_score_v4()` 的排序輸入，改動席位引擎時不要誤把這兩個籌碼面欄位當成第六個排名因子加回去。
11. **白話呈現條款**（2026-09-01 持有人拍板，全站適用，極簡版）：本 skill 為機械層資料管線，產出中若出現顯示 label（如 variant 頁欄位名），遵守 `notes/site-internal/root/_plainlang_styleguide.md` 對照表白話主名。

## Koyfin watchlist 欄位盤點（2026-09-17：78 → 80 欄）

| 項目 | 值 |
|---|---|
| 加欄前（35 個機械閘欄位已在，籌碼面欄位尚未加） | 78 欄 |
| 加欄後 | 80 欄 |
| 新增欄 1 | `Short Interest > % Of Shares Outstanding`（Columns 對話框路徑：搜尋 "Short Interest" → 子選單 "%" → "% Of Shares Outstanding"；表格短標籤 `Short Int. (%)`） |
| 新增欄 2 | `Insider Transactions, Shares (Net) - 3M`（Columns 對話框路徑：搜尋 "Insider" → 直接列出多個週期/口徑的葉節點，選 "Insider Transactions, Shares (Net) - 3M"；表格短標籤 `Insider Tr Shrs Net 3M`） |
| Short Interest 分類下的其他子選項（未選用） | `% Of Shares Outstanding`（選用）／`Amount of Shares`／`FQ History`／`FY History`／`Historic Average`／`Historic Growth QoQ`／`Historic Growth YoY`／`Trailing Growth`（皆帶子選單，本次只取當期 % 值） |
| Insider 分類下的其他候選（未選用） | `Insider Buy-Sell Ratio`（12M/1M/3M/6M）／`Insider Transactions, # (Buy/Sell/Net/Total)`（各期別）／`Insider Transactions, Shares (Buy/Sell/Total)`（各期別）——皆為計數或比率，唯獨 `Shares (Net)` 直接給「淨股數」這個最貼近「內部人淨買賣方向」語意的數字，且沒有 USD 金額版本可選（Koyfin 這組指標只有股數/次數兩種單位，沒有金額單位） |

## 與 refresh-eps-screener 的差異速查

| | refresh-eps-screener | refresh-eps-screener-web（本 skill） |
|---|---|---|
| 資料來源 | `DD_universe_EPS_estimates_*.xlsx` 檔 | Koyfin watchlist 畫面（Chrome 抓） |
| 為何存在 | 有現成 Excel | Koyfin Download 不含 FY 估值欄 |
| 驗證 gate | Excel Notes 第 8 列 spot-check | djb2 指紋 + 對帳 + 分割 gate |
| 下游 | 完全相同（snapshot / build / FX / variant 頁 / commit bundle） | 同左 |
