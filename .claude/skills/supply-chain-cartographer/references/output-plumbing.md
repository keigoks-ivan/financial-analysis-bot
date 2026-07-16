# 輸出機械層（Step 3 / 3.5 / 4 / 5）

> 條件載入：Step 2 完成後、進入 manifest 翻牌 → hub 入口更新 → build → commit/push → live URL 驗證階段時載入。核心 SKILL.md 的 Step 1 / 1.5 留在核心，本檔為 Step 3 之後的完整機械層程序。內容自 v1.1 原文零語意變更搬移。

## Step 3：翻 `docs/supply-chain/data/topics.json` 中該 topic 的 `active`

```json
{ "id": "{topic}", "tab": "...", "title": "...", "active": true }
```

## Step 3.5：更新 hub 入口頁 `docs/supply-chain/index.html`（**必做、容易漏**）

`index.html` 是 **hardcoded HTML**（不是從 `topics.json` 動態渲染），所以新 topic 的 `passive.html` / `passive.json` / `active: true` 都備齊後，如果不手動補入口，從 https://research.investmquest.com/supply-chain/ 進來看不到連結 — 用戶會問「為什麼沒看到」。歷史踩雷：MLCC commit 230bcff1 漏這一步，靠 bfab4e82 補救。

對於落在 **8 功能模組 × 5 終端市場** 框架內的 topic（多數情況），改 4 處：

1. **Hero meta**（檔頭附近的 `<div class="meta">`）：
   - `<b id="liveCount">N</b>` → N+1
   - `<b id="soonCount">M</b>` → M-1

2. **覆蓋矩陣 cell**（`<div class="matrix">` 內，定位到該 topic 所屬的 row × col 格子）：
   ```html
   <!-- before -->
   <div class="cell lvl-soon"><div class="c-tag"><span class="dot"></span>規劃中</div><div class="c-title">{title}</div><div class="c-sub">{vendors}</div></div>
   <!-- after -->
   <div class="cell lvl-on"><a href="{topic}.html"><div class="c-tag"><span class="dot"></span>已上線</div><div class="c-title">{title}</div><div class="c-sub">{vendors}</div><div class="arrow">→</div></a></div>
   ```

3. **Module 卡片**（`<div class="module-block">` 的 `.card-grid` 內）：
   ```html
   <!-- before -->
   <div class="tcard soon">
     <span class="t-tag"><span class="dot"></span>規劃中</span>
     <h4>{title}</h4>
     <div class="t-en">{title_en}</div>
     <div class="t-vendors">{vendors}</div>
     <div class="t-foot">即將推出</div>
   </div>
   <!-- after -->
   <a class="tcard live" href="{topic}.html">
     <span class="t-tag"><span class="dot"></span>已上線</span>
     <h4>{title}</h4>
     <div class="t-en">{title_en}</div>
     <div class="t-vendors">{vendors}</div>
     <div class="t-foot">查看供應鏈地圖 →</div>
   </a>
   ```

4. **Module 計數**（`<div class="module-head">` 內的 `.mod-count`）：
   - `<b>K</b> 子產業 · <b>X</b> 已上線` → X+1

對於 **跨主題 topic**（robot / leosat / spacedc / siph 等，落在底部「跨主題地圖」section）：只改 hero `liveCount`，並在 `<!-- Topical / cross-cutting maps -->` section 的 `<div class="card-grid">` 內 append 一張 `<a class="tcard live" href="{topic}.html">` 卡片（不用動矩陣與模組計數）。

`index.html` 也要併進 Step 4 的 `git add` 清單。

## Step 4：跑 build script + 本機驗證 + commit + push

```bash
# 重建 dd_links（DD 新增過就要跑）
python3 scripts/build_supply_chain_dd_index.py

# 【必跑】重生 hub 跨站統整（💎/🐘/🔒 三層）— 任何 ⚑/💎/node_role 改動都要刷新，
# 否則 /supply-chain/ 的「全站 Top Picks 統整」會 stale。會改寫 index.html。
python3 scripts/build_supply_chain_tiers.py

# 本機測試
python3 -m http.server 8765 --directory docs &
# 開瀏覽器訪問 http://localhost:8765/supply-chain/{topic}.html
# 或用 chrome headless
"$CHROME_PATH" --headless --window-size=2200,1800 --screenshot=/tmp/sc_{topic}.png "http://localhost:8765/supply-chain/{topic}.html"
pkill -f "http.server 8765"

# JSON schema audit（手寫小 Python 腳本，或拷 cpo audit pattern）
python3 -c "
import json
d = json.load(open('docs/supply-chain/data/{topic}.json'))
node_ids = {n['id'] for n in d['nodes']}
for e in d['edges']:
    assert e[0] in node_ids and e[1] in node_ids, f'edge {e}'
single_count = sum(1 for n in d['nodes'] if n.get('single'))
assert single_count == d['stats'][2]['v'], f'single count mismatch'
print(f'OK: {len(d[\"nodes\"])} nodes / {len(d[\"edges\"])} edges / {single_count} single')
"

# 提交（用 HEREDOC 維持格式）
git add docs/supply-chain/{topic}.html docs/supply-chain/data/{topic}.json docs/supply-chain/data/topics.json docs/supply-chain/index.html
git commit -m "$(cat <<'EOF'
supply-chain: add {Topic} topic — {N} nodes, {K} single-points

<3-5 句說明本 topic 的 thesis、row 結構、最重要的 single-points>

Row structure: {row1} / {row2} / {row3} ...

K single-points (⚑) with confidence levels:
  - {single-point 1}  <bucket>  <confidence>  <evidence>
  ...

DD cross-link coverage: {X} of {N} nodes' companies have ≥1 DD match.
Tickers without DD coverage (candidates for future DD work): <list>

Flipped {topic}.active=true in topics.json.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push origin main
```

## Step 5（必）：Live URL 驗證

deploy 完後（GitHub Pages 通常 1-2 min），跑：

```bash
for url in /supply-chain/{topic}.html /supply-chain/data/{topic}.json; do
  echo "$(curl -sI -o /dev/null -w '%{http_code}' https://research.investmquest.com${url}) $url"
done
```

兩個都要 **200**。
