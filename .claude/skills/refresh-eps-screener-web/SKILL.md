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
  // 前綴選擇器：Koyfin 的 CSS module 雜湊尾碼每次改版都會輪換，不要 hardcode 完整 class
  const heads = [...document.querySelectorAll('[class*="table__headerCell___"]')]
                  .map(h => h.innerText.replace(/\s+/g,' ').trim());
  const idx = {ticker:-1, fy1:-1, fy2:-1, fy3:-1, roic:-1, fcfm:-1, roic5y:-1};
  heads.forEach((h,i) => {
    const l = h.toLowerCase();
    if (l === 'ticker') idx.ticker = i;
    else if (l.includes('eps norm') && l.includes('fy1')) idx.fy1 = i;
    else if (l.includes('eps norm') && l.includes('fy2')) idx.fy2 = i;
    else if (l.includes('eps norm') && l.includes('fy3')) idx.fy3 = i;
    else if (l.includes('roic') && (l.includes('5y') || l.includes('5 yr') || l.includes('avg'))) idx.roic5y = i;  // 檢查順序在純 roic 之前，否則會被下一條攔截
    else if (l.includes('roic')) idx.roic = i;
    else if ((l.includes('fcf') && l.includes('margin')) || (l.includes('free cash flow') && l.includes('margin'))) idx.fcfm = i;
  });
  const countryIdx = heads.findIndex(h => h.toLowerCase()==='country');
  window.__epsIdx = idx;
  window.grabEps = function(){
    let n=0;
    document.querySelectorAll('[class*="table__row___"]').forEach(row=>{
      const cells=[...row.querySelectorAll('[class*="table__dataCell___"]')]
                    .map(c=>c.innerText.replace(/\s+/g,' ').trim());
      if (cells.length < heads.length) return;
      const m=(cells[idx.ticker]||'').match(TICK_RE);
      if(!m) return;
      window.__eps[m[1]] = {
        fy1: cells[idx.fy1], fy2: cells[idx.fy2], fy3: cells[idx.fy3],
        roic: idx.roic>=0 ? cells[idx.roic] : null,
        fcfm: idx.fcfm>=0 ? cells[idx.fcfm] : null,
        roic5y: idx.roic5y>=0 ? cells[idx.roic5y] : null,
        country: countryIdx>=0 ? cells[countryIdx] : ''
      };
      n++;
    });
    return n;
  };
  window.__epsSC = document.querySelector('[class*="table__scrollContainer___"]');
  return JSON.stringify({heads_found: idx, rows_class_seen: document.querySelectorAll('.table-styles__table__row___K6TSS').length});
})()
```

**Gate**：回傳的 `heads_found` 中 `ticker`／`fy1`／`fy2`／`fy3` 若有任一 = -1 → 表頭文字對不上，**先跑 Step 1.5 的橫向捲動再重試**（EPS 欄未渲染時表頭也讀不到）；橫向到底後仍 -1 才是 Koyfin 改欄名或欄位被移除，**停下**回報用戶。

`roic`／`fcfm`／`roic5y` 三欄是**選填（OPTIONAL）**——Koyfin watchlist 目前不一定已加這些欄，`heads_found.roic` / `heads_found.fcfm` / `heads_found.roic5y` = -1 **不擋 gate、不影響 EPS 抓取**；`grabEps()` 已對應把找不到的欄存 `null`。這些欄一旦頁面上有值，Step 6 會把它們一併寫進 xlsx（見下），沒有就照舊只寫 EPS 三欄。`roic5y` 對應 Koyfin 上「ROIC 5Y Avg」這類表頭（五年平均 ROIC，是 v3 席位資格核心席耐久判定用的欄，見 `scripts/load_eps_estimates_xlsx.py` docstring）。

**CSS class 雜湊會輪換**（2026-07-30 實測：`headerCell___gC361`→`___I7R3q`、`row___K6TSS`→`___RXyc3`、`dataCell___nRZp0`→`___V6mbY`、`scrollContainer___WBAWY`→`___E4YI-`，四個全換）。上面的程式碼已改用 `[class*="table__headerCell___"]` 這類**前綴選擇器**，對尾碼輪換免疫，不需要每次改版回來改 skill。若哪天連 `table__xxx___` 中段也變了（`rows_class_seen`=0），才用 `javascript_tool` 印出 scroll 容器內出現頻率最高的 class（≈ ticker 數）重新校準。

## Step 1.5 — 先把橫向捲到最右（**否則 EPS 三欄根本不存在於 DOM**）

這個表**不只縱向虛擬化，橫向也是**：EPS Norm 三欄位於表格右側，未捲到該位置時整欄不渲染，`heads_found` 會回 -1、`grabEps()` 會回 0。**縱向捲動前必須先做這步**：

```javascript
(() => {
  const sc = document.querySelector('[class*="table__scrollContainer___"]');
  sc.scrollLeft = sc.scrollWidth;                       // 推到最右
  sc.dispatchEvent(new Event('scroll',{bubbles:true}));  // 必須派發事件才重渲染
  return JSON.stringify({scrollLeft: sc.scrollLeft, scrollWidth: sc.scrollWidth});
})()
```

推到最右後**重跑 Step 1 的注入**（讓 `heads` 在 EPS 欄已渲染的狀態下重新建立索引），確認 `heads_found` 四個值都 ≥ 0 再往下。Step 2 縱向捲動期間**不要動 `scrollLeft`**——一旦回到最左，EPS 欄會再次消失，後續抓到的列會全是空值。

⚠️ Ticker 欄通常是凍結欄（sticky），橫向捲到最右後仍可見，所以 `idx.ticker` 依然有效；若實測發現 ticker 也被捲走，改用「先抓一輪 ticker→列索引對照，再橫捲抓 EPS」兩趟合併。

⚠️ **ROIC／FCF Margin／ROIC 5Y Avg 欄位可能不在最右側**——EPS 三欄固定在表格最右，但 `ROIC`／`FCF Margin`／`ROIC 5Y Avg` 這三欄的水平位置由 watchlist 欄位排列決定，不保證跟 EPS 欄相鄰。捲到最右後若 `heads_found.roic` / `heads_found.fcfm` / `heads_found.roic5y` 仍是 -1，**不要當成錯誤**（三欄皆選填，見 Step 1 gate）；若確認頁面上其實有這些欄只是還沒掃到，改採「左到右逐段捲動＋每段重讀 heads」的掃法找出實際欄位位置，再回頭捲到最右繼續 Step 2 的縱向抓取。

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

瀏覽器端（`roic`／`fcfm`／`roic5y` 一律併入指紋——欄位不存在時是 `null`／空字串，等同沒有訊息量，不影響既有檔案的指紋值）：
```javascript
(() => {
  const e=window.__eps, keys=Object.keys(e).sort();
  const canon = keys.map(k=>[k,e[k].fy1,e[k].fy2,e[k].fy3,e[k].roic||'',e[k].fcfm||'',e[k].roic5y||''].join('|')).join('\n');
  let h=5381; for(let i=0;i<canon.length;i++){h=((h<<5)+h+canon.charCodeAt(i))>>>0;}
  return JSON.stringify({rows:keys.length, bytes:canon.length, djb2:h});
})()
```
倒資料：`console.log('EPSROW|'+[k,fy1,fy2,fy3,roic||'',fcfm||'',roic5y||'',country].join('|'))` 逐檔，再 `read_console_messages{pattern:'EPSROW', limit:300}` 讀回全部。把 `EPSROW|` 後的 `ticker|fy1|fy2|fy3|roic|fcfm|roic5y`（**照 sorted 順序、無尾換行**）寫入 scratchpad `eps_raw_YYYYMMDD.txt`，Python 重算 djb2：
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

**ROIC／FCF Margin／ROIC 5Y Avg 合理範圍 gate（2026-09-09 新增，選填欄位適用）**：三欄數值須落在 **−100 至 200（%）** 之間，超出範圍視為**壞格**——不是整檔剔除，只把該欄**空白化**（EPS 三欄照留，該 ticker 繼續走 xlsx 主路徑，只有壞掉的那一格 fallback 回 QGM／yfinance，`roic5y` 缺值時 `durable_5y` 改由 QGM 五年穩定度判定）。逐檔判斷不需要 WebSearch 查證（跟 Step 5 的分割 gate 不同層級，這裡只做粗篩），單純數值落在區間外就空白。

## Step 6 — 建 xlsx

7 欄 schema（loader 只讀前 4，growth/CAGR 留空由 build 自算）**不變**，Sheet1「EPS Estimates」+ Sheet2「Notes」B2=snapshot 日期。`-` → 空格。**剔除清單**（Step 5 判定的壞值）不寫入。

**新增三欄（2026-09-09 起，選填；ROIC 5Y Avg 為 v3 席位資格核心席耐久判定用）**：若這一輪有抓到 ROIC／FCF Margin／ROIC 5Y Avg（Step 1 的 `roic`/`fcfm`/`roic5y`，通過 Step 5 合理範圍 gate），在第 7 欄之後**追加**「ROIC %」「FCF Margin %」「ROIC 5Y Avg %」三欄（數字、百分比單位；壞格或缺值 `-` → 留空，不寫字串）。前 7 欄的欄序與型別完全不動，`load_eps_estimates_xlsx.py` 是表頭驅動比對（見 loader docstring），加欄不影響既有 7 欄的回讀，向下相容：

```python
from openpyxl import Workbook
wb=Workbook(); ws=wb.active; ws.title="EPS Estimates"
header = ["Ticker","FY1E EPS","FY2E EPS","FY3E EPS","FY1->FY2 Growth %","FY2->FY3 Growth %","FY1->FY3 CAGR %"]
have_quality = any(roic or fcfm or roic5y for _,_,_,_,roic,fcfm,roic5y in rows)  # 有抓到才加欄
if have_quality:
    header += ["ROIC %", "FCF Margin %", "ROIC 5Y Avg %"]
ws.append(header)
for t,f1,f2,f3,roic,fcfm,roic5y in rows:  # rows 已排除 DROP 清單；roic/fcfm/roic5y 抓不到或未過 Step 5 範圍 gate 時為 None
    row = [t,f1,f2,f3,None,None,None]
    if have_quality:
        row += [roic, fcfm, roic5y]  # None（原 "-" 或壞格）-> 空格
    ws.append(row)
ws2=wb.create_sheet("Notes")
ws2["A2"]="Snapshot Date"; ws2["B2"]="YYYY-MM-DD"
if have_quality:
    ws2["A3"]="Quality Source"; ws2["B3"]="koyfin-web"
ws2["B5"]="split/exclusion notes here"
wb.save("data/eps-estimates/DD_universe_EPS_estimates_YYYYMMDD.xlsx")
```
落檔後**用 loader 回讀驗證**：`load_excel(path)` → ticker 數對、抽查 3-5 檔值、剔除的不在、`-` 正確變 None；有加 ROIC/FCF Margin/ROIC 5Y Avg 欄時另抽查每檔的 `roic_pct`/`fcf_margin_pct`/`roic_5y_avg_pct` 數值與頁面一致、Excel 快照物件的 `snap.quality_source == "koyfin-web"`（讀自 Notes!B3，跟下面 Step 7 latest.json 每檔的 `quality_source == "koyfin-xlsx"` 是兩個不同欄位，別混淆）。

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
- **有加 ROIC/FCF Margin 欄時（2026-09-09 起）**：build log 的 `quality (koyfin-xlsx path): rows=N roic=X fcf=Y` 這行，N 應約等於本輪有抓到 ROIC/FCF Margin 值的 ticker 數；抽查 3 檔 `latest.json` 的 `roic`/`fcf`/`quality_source` 與 Koyfin 頁面數值比對一致，`quality_source` 應為 `"koyfin-xlsx"`
- **有加 ROIC 5Y Avg 欄時（2026-09-09 起，v3 席位資格核心席耐久判定）**：抽查 3 檔 `latest.json` 的 `durable_5y`/`durable_source`——有抓到值的 ticker `durable_source` 應為 `"koyfin-xlsx"`，`durable_5y` 應等於「該值 ≥15 則 True」；沒抓到值但在 QGM 品質池內的 ticker `durable_source` 應 fallback 為 `"qgm"`

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
5. **表頭驅動取欄**（Step 1）——別 hardcode column index；class 一律用前綴選擇器（`[class*="table__row___"]`），Koyfin 雜湊尾碼輪換時免疫。
5b. **橫向先捲到底**（Step 1.5）——表格橫向也虛擬化，EPS 三欄未捲到就不在 DOM；縱向捲動全程不得動 `scrollLeft`。抓到整片空值時第一個要查的就是這條。
6. **Commit scope tight**——只 add dd-screener bundle，不 add docs/dd/。
7. **對帳 extra 應為空**——非空代表 universe 或別名沒同步。
7b. **ROIC／FCF Margin／ROIC 5Y Avg 三欄選填、不擋任何既有 gate**（2026-09-09）——Step 1 抓不到（`heads_found.roic`/`fcfm`/`roic5y` = -1）不擋 Step 1 gate、不擋 EPS 抓取；Step 5 合理範圍外只空白化該格，不剔除整檔；Step 6 沒抓到就不寫這三欄（沿用既有 7 欄 schema），dd-screener 品質欄與 `durable_5y`（v3 席位資格核心席耐久判定）自動 fallback 回 QGM／yfinance（見 `scripts/dd_screener_quality.py` 優先序）。
8. **白話呈現條款（2026-09-01 持有人拍板，全站適用，極簡版）**：本 skill 為機械層資料管線，產出中若出現顯示 label（如 variant 頁欄位名），遵守 `notes/site-internal/root/_plainlang_styleguide.md` 對照表白話主名。

## 與 refresh-eps-screener 的差異速查

| | refresh-eps-screener | refresh-eps-screener-web（本 skill） |
|---|---|---|
| 資料來源 | `DD_universe_EPS_estimates_*.xlsx` 檔 | Koyfin watchlist 畫面（Chrome 抓） |
| 為何存在 | 有現成 Excel | Koyfin Download 不含 FY 估值欄 |
| 驗證 gate | Excel Notes 第 8 列 spot-check | djb2 指紋 + 對帳 + 分割 gate |
| 下游 | 完全相同（snapshot / build / FX / variant 頁 / commit bundle） | 同左 |
