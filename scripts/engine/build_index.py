#!/usr/bin/env python3
"""決策引擎 — 總覽/方法論頁（/engine/）。

v2（2026-07-04 持有人回饋「之前都有看沒有懂」）：改白話一頁版為主體——
一句話 → 五步漏斗（活數字）→ 權力分工 → 組合快照 → 三條鐵律；
深層架構（五層卡/分工表/紀律/路線圖）收在後段。活數字取自 arena/radar/cards JSON。

選股系統 v2（2026-09-02 持有人拍板「照推薦執行」）：方法論文案改寫——擁有層（own_score 排序、
品質閘含 capex 週期豁免）與時機層（R 上修降為燈號、P 位置閘）分離，DD 降為選配層只做
veto（迴避→剔除）與角色標籤（≤180 天）。依據 notes/site-internal/root/
_picks_first_principles_review_20260902.md Part D；頁面結構與活數字來源不變。
"""
from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, page_embed_shell  # noqa: E402
from engine.grp import MKTCAP_MIN  # noqa: E402


def _load(name):
    try:
        return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def main() -> int:
    radar = _load("radar.json")
    arena = _load("arena.json")
    cards = _load("cards.json")
    sb = _load("scoreboard.json")

    core = [r["ticker"] for r in arena.get("core_seats", [])]
    sat = [r["ticker"] for r in arena.get("sat_seats", [])]
    core_slots, sat_slots = 5, 5
    regime = arena.get("regime") or {}
    board_n = len(radar.get("grp_board") or [])
    scored_n = radar.get("scored_n", "—")
    n_cards = cards.get("n_cards", "—")
    n_claims = cards.get("n_claims", "—")
    n_alerts = sum(1 for d in arena.get("duels", []) if d.get("alert"))
    cap_b = f"{MKTCAP_MIN / 1e9:.0f}"

    funnel = f"""① 發現    雷達每週掃 S&P 500＋NDX＋中型股（{scored_n} 檔可算）
             擁有層資格：品質閘 ROIC ≥15% ∧ FCF margin ≥10%（capex 週期豁免：ROIC ≥25% ∧ FCF ≥0）
             × 成長閘 FY1→FY3 EPS CAGR ≥15% × 市值 ≥ ${cap_b} 億美元
             排序＝own_score＝min(成長,30)＋FY1 盈餘殖利率%（ROIC ≥30 → +2；PEG >2 → −5）
             母體＝DD 池 ∪ QGM 品質池（US／TW）∪ 快審卡 → 主榜（現 {board_n} 檔，按擁有層分排）

② 資格    DD 降為選配層——不再是必經審查
             只做兩件事：veto（DD 裁決＝迴避 → 剔除）與角色標籤（核心／衛星，≤180 天內有效）
             無 DD 名字照樣同場排序，標「待 DD」——不卡進度，值得深挖再補
             ⚠ 品質閘與成長閘已擋掉舊三閘看不見的：週期頂點假象、會計假成長、基期效應

③ 分軌    DD 角色優先，無 DD 走護城河字母
             DD 角色核心／衛星（≤180 天）優先於護城河字母；過期或無 DD → 護城河 S/A 級（非↓）→ 核心席，
             {core_slots} 席 × 上限 10%（QGM 5 年 ROIC 穩定度 ≥75% 亦可核心，待 DD 確認）
             其餘 → 衛星席，{sat_slots} 席 × 上限 5%，寧缺勿濫

④ 執行    席位 ≠ 買點
             時點看板機（A1 突破／B 回踩／C 冷卻完成）＋ regime 撥盤（現 {escape(regime.get('label') or '—')}）

⑤ 守門    一席一卡（現 {n_cards} 張／{n_claims} 條宣稱）
             遲滯：新席需連 2 次週跑過閘才上席；現任連 4 次不過閘才下席（硬 veto 除外，即刻下席）
             GRP 守門週更自動結算（成長跌破／轉下修／破線 → 卡片自己亮 ⛔）
             ＋ DD 深層宣稱帶期限（到期亮 ⏰ 人工結算）
             觀望也被盯：錯過成本／上修觸發 → 強制複審（複審對 DD 扳機，不因上修就追）"""

    body = f"""<div class="hero">
<h1>決策引擎</h1>
<div class="hero-sub" style="font-size:15px"><b>一句話：擁有層（品質閘 × 成長閘，排序＝own_score）決定值不值得擁有、排第幾——
時機燈（位置＋上修）只標示現在能不能動，DD 降為選配層只做 veto 與角色標籤。</b></div>
<div class="asof">研究層頁面，不含實際持倉 ｜ 週更 ｜ 分工：本引擎＝<b>方式甲（結構長抱線）的排序主幹</b>——擁有層×時機層引擎（GRP v2）排序與席位（機器擂台）；流程與板機見 <a href="/dd-screener/pipeline.html">Pipeline</a>，對外成品榜見 <a href="/picks/">精選清單</a> ｜ 已結算 {sb.get('n_settled', '—')} 筆歷史裁決</div>
</div>

<div class="block">
<h2>五步漏斗</h2>
<pre style="font-size:13px;line-height:1.8;overflow-x:auto;background:var(--line-soft);border:1px solid var(--line);border-radius:8px;padding:14px 16px">{funnel}</pre>
</div>

<div class="block">
<h2>權力分工（誰說了算）</h2>
<table>
<thead><tr><th class="left">問題</th><th class="left">權威</th><th class="left">在哪看</th></tr></thead>
<tbody>
<tr><td class="left">先看誰</td><td class="left">擁有層看板（board.txt，市場活數據，週更）</td><td class="left"><a href="/engine/board.txt">看板</a>・<a href="/engine/radar.html">雷達</a></td></tr>
<tr><td class="left">能不能買</td><td class="left">品質閘＋DD veto（懂生意的否決權，DD 只剔除不排序）</td><td class="left"><a href="/engine/cards.html">決策卡</a></td></tr>
<tr><td class="left">核心還是衛星</td><td class="left">DD 角色優先，無 DD 用護城河（S/A＝核心、其餘＝衛星）</td><td class="left"><a href="/engine/arena.html">擂台</a></td></tr>
<tr><td class="left">何時買</td><td class="left">板機（A1/B/C）＋ regime 撥盤</td><td class="left"><a href="/dd-screener/sop-funnel.html">SOP Funnel</a>・<a href="/engine/arena.html">擂台</a></td></tr>
<tr><td class="left">何時複審／出場</td><td class="left">決策卡宣稱（帶數字帶期限）</td><td class="left"><a href="/engine/cards.html">決策卡</a></td></tr>
<tr><td class="left">規則能不能改</td><td class="left">記分板（91 天結算，季檢才調參）</td><td class="left"><a href="/engine/scoreboard.html">記分板</a></td></tr>
</tbody></table>
</div>

<div class="block">
<h2>組合快照（自動更新）</h2>
<div class="stat-row">
<div class="stat"><strong>{len(core)}/{core_slots}</strong><span>核心席</span></div>
<div class="stat"><strong>{len(sat)}/{sat_slots}</strong><span>衛星席</span></div>
<div class="stat"><strong>{escape(regime.get('label') or '—')}</strong><span>Regime 撥盤</span></div>
<div class="stat"><strong>{n_alerts}</strong><span>擂台警報</span></div>
</div>
<div class="block-sub">核心：{escape('、'.join(core) or '—')}　｜　衛星：{escape('、'.join(sat) or '—')}
（空席是刻意的——審查放行率低＋市值門檻＋regime 中性下，空席就是倉位管理）</div>
</div>

<div class="block">
<h2>名單為什麼會變（四個驅動力，按力度排）</h2>
<table>
<thead><tr><th class="left">驅動力</th><th class="left">頻率</th><th class="left">影響</th></tr></thead>
<tbody>
<tr><td class="left"><b>月度 EPS 修正刷新</b></td><td class="left">每月（Koyfin snapshot）＋每週（yfinance，雷達候選）</td>
<td class="left">上修現在是<b>燈號不是排序鍵</b>；只有 FY+1 單月 ≤-10%（任一源）才否決。席位主要隨品質閘／成長閘／
價格位置與遲滯變動，不再因每次修正刷新就全體重排。
<b>兩源主源規則</b>：DD 池認 Koyfin、池外認 yfinance，計分不混用；重下修 ≤-10% 的否決<b>任一源觸發即生效</b>
（源吵架時聽壞消息），方向相反標 ⚠ 源分歧供人工判讀</td></tr>
<tr><td class="left"><b>財報季條件翻正</b></td><td class="left">季度</td>
<td class="left">觀望票的翻正條件與決策卡宣稱到期潮集中在財報季——席位變動的主窗口</td></tr>
<tr><td class="left"><b>新 DD／快審補齊</b></td><td class="left">持續</td>
<td class="left">池內仍有大量無裁決名字＋主榜大型候選待審——每補一檔＝多一個挑戰者</td></tr>
<tr><td class="left"><b>價格位置（P 閘）</b></td><td class="left">每週</td>
<td class="left">破 52 週線下席、站回來回席——趨勢破壞的名字自動失格，修復自動恢復資格</td></tr>
</tbody></table>
<div class="note">變動是<b>不對稱設計</b>：衛星席＝快時鐘（爆發型，預期高輪動）；核心席＝慢時鐘
（S/A 護城河是慢變數，若核心每週換人＝bug）。<b>遲滯已上線</b>：新席需連 2 次週跑過閘才上席，
現任連 4 次不過閘才下席（硬 veto 除外，即刻生效）。每次上席/下席都記入
<a href="/engine/arena.html">席位變動帳本</a>（append-only，含 gate_history 逐週過閘紀錄）——
2026-10 季檢時用帳本 gate_history 校準遲滯厚度是否合適，不憑感覺預設。</div>
</div>

<div class="block">
<h2>三條鐵律</h2>
<div class="block-sub" style="font-size:13.5px;line-height:2">
1. <b>看得見 ≠ 能買</b>——雷達只給研究順序，資格永遠要過審查。<br>
2. <b>上修最猛處常是最危險處</b>——所以品質閘與位置閘之上必有週期位置判定（MU 檢查）；
<b>時機訊號不排長抱席位</b>——上修降為燈號，排序改用擁有層分。<br>
3. <b>每個判斷都會被結算</b>——觀望的錯過和進場的套牢同權重記帳；數據改規則，不是感覺改規則。
</div>
</div>

<div class="block">
<h2>深一層：五層架構與紀律</h2>
<div class="layers">
<div class="layer"><div class="lno">L0</div><h3>全市場雷達</h3>
<p>結構訊號批量 → 候選逐檔 EPS 修正確認。</p>
<a href="/engine/radar.html">→ 雷達</a></div>
<div class="layer"><div class="lno">L1</div><h3>擁有層準則＋軌別路由</h3>
<p>品質閘＋成長閘＝擁有層資格，own_score 排序；DD 角色優先、無 DD 走 moat 分軌。時機燈（位置＋上修）獨立標示不排序。</p></div>
<div class="layer"><div class="lno">L2</div><h3>決策卡</h3>
<p>一席一卡：GRP 守門自動結算＋DD 深層宣稱帶期限。</p>
<a href="/engine/cards.html">→ 決策卡</a></div>
<div class="layer"><div class="lno">L3</div><h3>席位擂台</h3>
<p>席位 vs 同軌最強挑戰者，警報進每月人工擂台；席位變動帳本 append-only。</p>
<a href="/engine/arena.html">→ 擂台</a></div>
<div class="layer"><div class="lno">L4</div><h3>結算所</h3>
<p>每筆裁決 × 週線自動結算、按形狀分桶——判斷函數的季度校準依據。</p>
<a href="/engine/scoreboard.html">→ 記分板</a></div>
</div>
<div class="note" style="margin-top:12px">
<b>紀律</b>：擁有層品質閘／成長閘與市值門檻（2026-09-02 持有人拍板 v2）PREREG 鎖定，季檢憑記分板數據才可調；
記分板 append-only、gate 變更畫分段線、歷史不重算；樣本未熟（n&lt;20 或齡&lt;91 天）標「觀察期」不給結論。
<b>與 <a href="/dd-screener/pipeline.html">dd-screener Pipeline</a> 的關係</b>：同屬<b>方式甲（結構長抱線）</b>，
不是兩套並存的競爭排序——Pipeline 核心軌<b>已對齊擁有層排序主幹</b>（DD 降為選配 veto／角色標籤，2026-09-02 mandate）。
本區＝甲線排序主幹的機器擂台視圖，Pipeline＝同一條甲線的流程與板機視圖，兩者互指不重複。
</div>
</div>

<div class="block">
<h2>路線圖</h2>
<table>
<thead><tr><th class="left">Phase</th><th class="left">內容</th><th class="left">狀態</th></tr></thead>
<tbody>
<tr><td class="left">1-2</td><td class="left">雷達＋GRP 主榜＋擂台＋決策卡＋記分板＋快審層＋市值門檻＋系統測試（32 斷言）</td><td class="left">✅ 2026-07-04 上線</td></tr>
<tr><td class="left">3</td><td class="left">形狀檢查表與 GRP 閾值首次季度校準（記分板滿 91 天後）</td><td class="left">2026-10—</td></tr>
<tr><td class="left">v2</td><td class="left">擁有層×時機層分離：own_score 排序、品質閘（含 capex 週期豁免）、R 降為燈號、DD 只做 veto／角色標籤、遲滯 2/4</td><td class="left">✅ 2026-09-02</td></tr>
<tr><td class="left">v2 校準</td><td class="left">v2 首輪校準：甲軌前 15 對 p_clim（DD 池 365 天無條件基準 0.582）</td><td class="left">2026-12</td></tr>
</tbody></table>
</div>"""
    # 2026-07-10 選股主控台整併：engine 總覽改輸出 nav-less 片段，供 /cockpit/#seats
    # 分頁 iframe 嵌入；/engine/index.html 已改為 redirect stub（見 site_nav SKIP_FILES）。
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "_index_body.html").write_text(
        page_embed_shell("決策引擎 · 席位排序", body,
                         "選股邏輯一頁版：擁有層排序（own_score）× 時機燈 × DD 選配（veto／角色標籤）× 席位擂台 × 自動結算"),
        encoding="utf-8")
    print("engine/_index_body.html written (nav-less 片段，供主控台席位排序分頁)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
