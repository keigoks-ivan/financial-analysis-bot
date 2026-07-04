#!/usr/bin/env python3
"""決策引擎 — 總覽/方法論頁（/engine/）。內容準靜態；nav 變更時重跑即可。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, page_shell  # noqa: E402

RADAR_JSON = OUT_DIR / "radar.json"
SB_JSON = OUT_DIR / "scoreboard.json"


def main() -> int:
    radar_stat = sb_stat = ""
    try:
        r = json.loads(RADAR_JSON.read_text(encoding="utf-8"))
        radar_stat = (f'週掃 {r["scored_n"]} 檔 ｜ 形狀命中 '
                      f'{sum(r["shape_counts"].values())} ｜ 池外 {r["blind_total"]}')
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    try:
        s = json.loads(SB_JSON.read_text(encoding="utf-8"))
        sb_stat = f'已結算 {s["n_settled"]} 筆裁決'
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    cards_stat = ""
    try:
        c = json.loads((OUT_DIR / "cards.json").read_text(encoding="utf-8"))
        cards_stat = f'{c["n_cards"]} 張卡／{c["n_claims"]} 條宣稱。'
    except (OSError, json.JSONDecodeError, KeyError):
        pass

    body = f"""<div class="hero">
<h1>⚙ 決策引擎</h1>
<div class="hero-sub">結算驅動的選股決策機器 — 研究淺進深、判斷小而可證偽、每個判斷都被記分、
記分改變下一輪規則。與 <a href="/dd-screener/pipeline.html">現行漏斗（Pipeline）</a>並存分工：
引擎管「發現」與「校準」，進場資格仍由 DD 裁決＋sop-funnel 板機把守。研究層頁面，不含實際持倉。</div>
</div>

<div class="block">
<h2>設計原則（為什麼長這樣）</h2>
<div class="block-sub">出發點是三個第一性事實，全部來自本站自己的驗屍數據。</div>
<table>
<thead><tr><th class="left">事實</th><th class="left">設計回應</th></tr></thead>
<tbody>
<tr><td class="left">決策帶寬一年只有 10–15 次（10 席、1–3 年持有），<br>但研究系統一季能生產 388 個判斷</td>
<td class="left"><b>廣掃自動化、深挖只給候選</b>——人只出現在「裁決」與「擂台」兩個點</td></tr>
<tr><td class="left">1–3 年大贏家只有四種出身：循環反轉（MU/SNDK）、動能重估（PLTR/APP）、<br>長基期突破、主題中小型下沉（ICHR/UCTT）</td>
<td class="left"><b>形狀路由取代單一資格閘</b>——四形狀各有入場檢查表、各自記分</td></tr>
<tr><td class="left">池外贏家稽核：12M top 50 有 <b>54% 不在研究池內</b>，集中於主題中小型；<br>結算所建立前，388 筆判斷的 outcome 回填數＝0</td>
<td class="left"><b>宇宙全掃（大中型 ~920 檔）＋結算所置於中心</b>——每個判斷自動對答案，季度校準改規則</td></tr>
</tbody></table>
</div>

<div class="block">
<h2>五層架構</h2>
<div class="layers">
<div class="layer"><div class="lno">L0</div><h3>全市場雷達</h3>
<p>S&amp;P 500＋NDX 100＋S&amp;P 400 週掃：結構訊號批量 → 候選逐檔 EPS 修正確認。{radar_stat}</p>
<span class="status st-live">✅ 上線</span> <a href="/engine/radar.html">→ 雷達</a></div>
<div class="layer"><div class="lno">L1</div><h3>形狀路由</h3>
<p>突破帶／循環轉折／動能重估／主題下沉——四形狀分欄，門檻 PREREG 鎖定季檢。</p>
<span class="status st-live">✅ 上線（雷達內）</span></div>
<div class="layer"><div class="lno">L2</div><h3>一頁決策卡</h3>
<p>一席一卡：thesis ≤5 句＋3–5 條帶期限的可證偽宣稱（抽自 DD §13/§14）＋pre-mortem。價格宣稱週更自動結算。{cards_stat}</p>
<span class="status st-live">✅ 上線</span> <a href="/engine/cards.html">→ 決策卡</a></div>
<div class="layer"><div class="lno">L3</div><h3>席位擂台</h3>
<p>核心 5＋衛星 5 各配同形狀挑戰者，⚔ 警報進每月人工擂台；regime 撥盤＋產業集中度警戒。</p>
<span class="status st-live">✅ 上線</span> <a href="/engine/arena.html">→ 擂台</a></div>
<div class="layer"><div class="lno">L4</div><h3>結算所</h3>
<p>每筆裁決 × 週線自動結算，按形狀分桶記分。{sb_stat}。季度校準以此為據。</p>
<span class="status st-live">✅ 上線</span> <a href="/engine/scoreboard.html">→ 記分板</a></div>
</div>
</div>

<div class="block">
<h2>與現行漏斗的分工</h2>
<table>
<thead><tr><th class="left"></th><th class="left">決策引擎（本區）</th><th class="left">現行漏斗（dd-screener）</th></tr></thead>
<tbody>
<tr><td class="left">宇宙</td><td class="left">S&amp;P 500＋NDX 100＋S&amp;P 400 全掃（發現池外）</td><td class="left">240 檔 DD 策展池（深研）</td></tr>
<tr><td class="left">單位</td><td class="left">形狀 × 可證偽 claim</td><td class="left">DD 報告 × 統一裁決</td></tr>
<tr><td class="left">進場資格</td><td class="left">不給——命中只代表「該研究」</td><td class="left">DD §14 裁決＋sop-funnel 板機（A1/B/C）</td></tr>
<tr><td class="left">回饋迴路</td><td class="left">形狀記分板（本區 L4）</td><td class="left">knowledge 結算所＋觀望複審隊列＋板機對照組</td></tr>
</tbody></table>
<div class="note">雷達池外名字的正確用法：值得的話 → 入 DD 池補報告 → 拿裁決 → 走板機。
引擎不提供任何「直接買」的路徑，這是刻意的。</div>
</div>

<div class="block">
<h2>紀律</h2>
<div class="block-sub">
① 形狀門檻與確認閾值 PREREG 鎖定（2026-07-04），季檢憑記分板數據才可調，禁止盤中調參。
② 記分板 append-only、gate 變更畫分段線、歷史不重算。
③ 觀望／迴避同樣被結算——錯過成本與套牢成本同權重。
④ 樣本未熟（n&lt;20 或齡&lt;91 天）標示「觀察期」，不給結論。
</div>
</div>

<div class="block">
<h2>路線圖</h2>
<table>
<thead><tr><th class="left">Phase</th><th class="left">內容</th><th class="left">狀態</th></tr></thead>
<tbody>
<tr><td class="left">1</td><td class="left">雷達（L0+L1）＋形狀記分板（L4）＋週更 workflow</td><td class="left">✅ 2026-07-04 上線</td></tr>
<tr><td class="left">2</td><td class="left">一頁決策卡（L2 schema＋產卡流程）＋席位擂台（L3）＋regime 撥盤</td><td class="left">規劃中</td></tr>
<tr><td class="left">3</td><td class="left">卡餵擂台、形狀檢查表首次季度校準（記分板滿 91 天後）</td><td class="left">2026-10—</td></tr>
</tbody></table>
</div>"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(
        page_shell("決策引擎 · 總覽", "/engine/", body,
                   "結算驅動的選股決策機器 — 全市場雷達、形狀路由、決策卡、擂台、結算所"),
        encoding="utf-8")
    print("engine/index.html written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
