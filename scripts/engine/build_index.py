#!/usr/bin/env python3
"""決策引擎 — 總覽/方法論頁（/engine/）。

v2（2026-07-04 持有人回饋「之前都有看沒有懂」）：改白話一頁版為主體——
一句話 → 五步漏斗（活數字）→ 權力分工 → 組合快照 → 三條鐵律；
深層架構（五層卡/分工表/紀律/路線圖）收在後段。活數字取自 arena/radar/cards JSON。

選股系統 v2（2026-09-02 持有人拍板「照推薦執行」）：方法論文案改寫——擁有層（own_score 排序、
品質閘含 capex 週期豁免）與時機層（R 上修降為燈號、P 位置閘）分離，DD 降為選配層只做
veto（迴避→剔除）與角色標籤（≤180 天）。依據 notes/site-internal/root/
_picks_first_principles_review_20260902.md Part D；頁面結構與活數字來源不變。

v5（2026-09-17 持有人拍板「品質派 ∩ 獲利上修 ∩ 突破還原權息歷史新高」，見
scripts/engine/grp.py 檔頭 v5 段／knowledge/rule_ledger.md「v5 席位引擎」列）：本頁文案
一併改寫——own_score 不再是排序鍵（降為「v4 對照」tooltip，只在 board.txt／_arena_body.html
逐檔顯示，不進本頁一句話／五步漏斗），排序改為上修（財報後錨定，缺值退回三個月）單一變數；
耐久與融券高從「分軌」升級為資格閘本體；衛星軌取消，池扣掉核心即「等待池」（無固定席次、
無 5% 倉上限）；核心席仍是池前 5，週遲滯（連 2/連 4）已由 v4 的月頻輪動取代。頁面結構
（五步漏斗／權力分工／組合快照／四個驅動力／三條鐵律／五層架構／路線圖）不變，只換內容。
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
    sat = [r["ticker"] for r in arena.get("sat_seats", [])]   # v5：sat_seats＝整個等待池，非固定 5 席
    core_slots = 5
    pool_n = arena.get("pool_size", len(sat) + len(core))
    buyable_n = len(arena.get("buyable_seats") or [])
    regime = arena.get("regime") or {}
    board_n = len(radar.get("grp_board") or [])
    scored_n = radar.get("scored_n", "—")
    n_cards = cards.get("n_cards", "—")
    n_claims = cards.get("n_claims", "—")
    n_alerts = sum(1 for d in arena.get("duels", []) if d.get("alert"))
    cap_b = f"{MKTCAP_MIN / 1e9:.0f}"

    funnel = f"""① 資格    品質派資格閘——雷達每週掃 S&P 500＋NDX＋中型股（{scored_n} 檔可算）
             品質閘 ROIC ≥15% ∧ FCF margin ≥10%（capex 週期豁免：ROIC ≥25% ∧ FCF ≥0）
             × 三年成長 FY1→FY3 EPS CAGR ≥15%（耐久者 10%）× 站上 52 週線 × 市值 ≥ ${cap_b} 億美元
             × 耐久一致性（QGM 五年穩定度 ≥75%，或 Koyfin 五年∧三年∧現值三者皆 ≥15%）
             財報後上修 ≤−5%（缺財報錨定退回三個月）／體質拒絕／衰退 ⛔／DD 迴避／
             融券占流通股比 >10% 皆整體排除——不耐久、融券高皆不進池，v5 沒有衛星軌可以收留
             母體＝DD 池 ∪ QGM 品質池（US／TW）∪ 快審卡 → 主榜（現 {board_n} 檔，按資格判定）

② 排序    上修單一變數——資格全過名字中，財報後上修（缺值退回三個月）≥+5% 者進「池」（現 {pool_n} 檔）
             池內依上修降冪排序，同值 tie-break implied_growth_pct、再 tie-break 盈餘殖利率
             own_score（v4 五百分位排序）保留一輪只做逐檔「v4 對照」tooltip，不參與本排序
             資格全過但上修未達 +5% 的名字列收合區供人工複審，不進池

③ 席位    核心＝池前 5，月頻整批重選；其餘池成員＝等待池（無固定席次、無 %倉上限）
             月頻輪動：每月第一次排程整批重選一次，期間僅七項硬否決（迴避／拒絕／⛔／
             財報後上修跌破 ≤−5%／市值不足／連兩週跌破 52 週線／融券轉高）能讓現任核心下席，
             空位由池遞補；其餘軟性失格沿用到下個月
             DD 降為選配層：不再是必經審查，只做迴避否決＋角色標籤（≤180 天內有效，僅供顯示）

④ 板機    距歷史新高（時機燈，每日重算）——池 {pool_n} 檔中今天可買 {buyable_n} 檔
             🟢 可進＝距還原權息全歷史新高 ≥−3% 且站上 200 日線；🟡 半倉＝−10%~−3%
             🔴 等板機＝距新高 <−10% 或跌破 200 日線；🟠 過熱＝動能 >150% 但仍在綠燈距離內，半倉
             核心席不代表現在該買——時機燈才回答「現在能不能買」

⑤ 守門    一席一卡（現 {n_cards} 張／{n_claims} 條宣稱）
             GRP 守門週更自動結算（成長跌破／轉下修／破線 → 卡片自己亮 ⛔）
             ＋ DD 深層宣稱帶期限（到期亮 ⏰ 人工結算）
             觀望也被盯：錯過成本／上修觸發 → 強制複審（複審對 DD 扳機，不因上修就追）"""

    body = f"""<div class="hero">
<h1>決策引擎</h1>
<div class="hero-sub" style="font-size:15px"><b>一句話：品質派資格閘（品質×三年成長×耐久一致性）決定進不進池——
上修排序（財報後錨定）決定池內排第幾、核心月頻換人；距歷史新高的時機燈只標示現在能不能買（不排序）；
DD 降為選配層只做 veto 與角色標籤。</b></div>
<div class="asof">研究層頁面，不含實際持倉 ｜ 日更（核心月頻換人）｜ 分工：本引擎＝<b>方式甲（結構長抱線）的排序主幹</b>——品質派資格×上修排序×歷史新高板機引擎（GRP v5）與席位（機器擂台）；流程與板機見 <a href="/dd-screener/pipeline.html">Pipeline</a>，對外成品榜見 <a href="/picks/">精選清單</a> ｜ 已結算 {sb.get('n_settled', '—')} 筆歷史裁決</div>
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
<tr><td class="left">先看誰</td><td class="left">選股看板（board.txt，市場活數據，日更）</td><td class="left"><a href="/engine/board.txt">看板</a>・<a href="/engine/radar.html">雷達</a></td></tr>
<tr><td class="left">能不能買</td><td class="left">資格閘＋DD veto（懂生意的否決權，DD 只剔除不排序）</td><td class="left"><a href="/engine/cards.html">決策卡</a></td></tr>
<tr><td class="left">核心還是等待池</td><td class="left">純比上修排序——池前 5 為核心，其餘為等待池（無 DD 角色路由、無護城河字母路由）</td><td class="left"><a href="/engine/arena.html">擂台</a></td></tr>
<tr><td class="left">何時買</td><td class="left">時機燈（距歷史新高＋200 日線）＋ regime 撥盤</td><td class="left"><a href="/dd-screener/sop-funnel.html">SOP Funnel</a>・<a href="/engine/arena.html">擂台</a></td></tr>
<tr><td class="left">何時複審／出場</td><td class="left">決策卡宣稱（帶數字帶期限）</td><td class="left"><a href="/engine/cards.html">決策卡</a></td></tr>
<tr><td class="left">規則能不能改</td><td class="left">記分板（91 天結算，季檢才調參）</td><td class="left"><a href="/engine/scoreboard.html">記分板</a></td></tr>
</tbody></table>
</div>

<div class="block">
<h2>組合快照（自動更新）</h2>
<div class="stat-row">
<div class="stat"><strong>{len(core)}/{core_slots}</strong><span>核心席</span></div>
<div class="stat"><strong>{len(sat)} 檔</strong><span>等待池</span></div>
<div class="stat"><strong>{escape(regime.get('label') or '—')}</strong><span>Regime 撥盤</span></div>
<div class="stat"><strong>{n_alerts}</strong><span>擂台警報</span></div>
</div>
<div class="block-sub">核心：{escape('、'.join(core) or '—')}　｜　等待池：{escape('、'.join(sat) or '—')}
（衛星軌已取消——池扣掉核心即等待池，無固定席次、無 %倉上限；核心空席是刻意的——審查放行率低＋市值門檻＋regime 中性下，空席就是倉位管理）</div>
</div>

<div class="block">
<h2>名單為什麼會變（四個驅動力，按力度排）</h2>
<table>
<thead><tr><th class="left">驅動力</th><th class="left">頻率</th><th class="left">影響</th></tr></thead>
<tbody>
<tr><td class="left"><b>財報後上修刷新</b></td><td class="left">每月（Koyfin snapshot，以個股自己最近一次財報日錨定）＋每日（時機燈重算）</td>
<td class="left">上修現在是<b>唯一排序鍵</b>（缺財報錨定退回三個月日曆窗）；≤−5% 否決資格（雙源皆缺才退回 FY+1
單月 ≤−10% fallback）。核心月頻整批重選，期間僅七項硬否決能立即換人，其餘軟性失格（例如成長跌出門檻）
沿用到下個月、空位由池遞補——不再是每次修正刷新就全體重排</td></tr>
<tr><td class="left"><b>財報季條件翻正</b></td><td class="left">季度</td>
<td class="left">觀望票的翻正條件與決策卡宣稱到期潮集中在財報季——池組成變動的主窗口</td></tr>
<tr><td class="left"><b>新 DD／快審補齊</b></td><td class="left">持續</td>
<td class="left">池內仍有大量無裁決名字＋主榜大型候選待審——每補一檔＝多一個挑戰者</td></tr>
<tr><td class="left"><b>距歷史新高（時機燈）</b></td><td class="left">每日</td>
<td class="left">不影響資格或排序，只決定「等待池」內誰被標「可買」（綠/橘燈）；破 52 週線＝資格閘失守（下個月才會真的下席，硬否決除外）</td></tr>
</tbody></table>
<div class="note"><b>月頻輪動（v4 起取代週遲滯）</b>：每月第一次排程整批重選一次核心席；期間只有
七項硬否決（DD 迴避／體質拒絕／衰退 ⛔／財報後上修跌破 ≤−5%／市值不足／連兩週跌破 52 週線／
融券占流通股比轉高 >10%）能讓現任核心立即下席，空位由池遞補。等待池不是持久化名單、沒有
「衛星快時鐘」這種軌別時鐘概念——池成員每次重算都是當下資格＋排序的結果。每次核心上席/下席都記入
<a href="/engine/arena.html">席位變動帳本</a>（append-only）——
2026-10 季檢時用帳本校準月頻輪動的節奏是否合適，不憑感覺預設。</div>
</div>

<div class="block">
<h2>三條鐵律</h2>
<div class="block-sub" style="font-size:13.5px;line-height:2">
1. <b>看得見 ≠ 能買</b>——雷達只給研究順序，資格永遠要過審查。<br>
2. <b>上修最猛處常是最危險處</b>——所以品質閘、耐久一致性與位置閘之上還要看基期效應與循環股守門；
<b>值不值得擁有跟現在能不能買是兩個問題</b>——排序純看上修，距歷史新高的時機燈只管買點，兩者刻意不互相污染。<br>
3. <b>每個判斷都會被結算</b>——觀望的錯過和進場的套牢同權重記帳；數據改規則，不是感覺改規則。
</div>
</div>

<div class="block">
<h2>深一層：五層架構與紀律</h2>
<div class="layers">
<div class="layer"><div class="lno">L0</div><h3>全市場雷達</h3>
<p>結構訊號批量 → 候選逐檔 EPS 修正確認。</p>
<a href="/engine/radar.html">→ 雷達</a></div>
<div class="layer"><div class="lno">L1</div><h3>資格閘＋上修排序</h3>
<p>品質閘＋三年成長＋耐久一致性＝資格，財報後上修排序決定池內名次與核心席；own_score（v4）保留一輪僅供逐檔對照。距歷史新高的時機燈獨立標示不排序。</p></div>
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
<b>紀律</b>：資格閘門檻數字（品質閘／成長閘／耐久一致性／市值門檻）PREREG 鎖定，季檢憑記分板數據才可調，
2026-09-02 v2 起已歷經 v3／v4／v4.1／v5 多輪修訂（見 <a href="/engine/scoreboard.html">記分板</a>與
knowledge/rule_ledger.md「席位引擎」各版列，每輪皆附證偽條件）；記分板 append-only、gate 變更畫分段線、
歷史不重算；樣本未熟（n&lt;20 或齡&lt;91 天）標「觀察期」不給結論。
<b>與 <a href="/dd-screener/pipeline.html">dd-screener Pipeline</a> 的關係</b>：同屬<b>方式甲（結構長抱線）</b>，
不是兩套並存的競爭排序——Pipeline 核心軌<b>已對齊本引擎的上修排序主幹</b>（DD 降為選配 veto／角色標籤）。
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
<tr><td class="left">B4②</td><td class="left">遲滯降權版：DD 180 天內裁決＝觀望的現任席，下席門檻 4→2 次不過閘</td><td class="left">✅ 2026-09-04</td></tr>
<tr><td class="left">v2 校準</td><td class="left">v2 首輪校準：甲軌前 15 對 p_clim（DD 池 365 天無條件基準 0.582）</td><td class="left">2026-12</td></tr>
<tr><td class="left">v3</td><td class="left">席位資格改綁三年期 Koyfin 成長（單年 fallback 不再入席）；DD 不再是入席前提，核心另需耐久（五年 ROIC 平均 ≥15% 或 QGM 五年穩定度 ≥75%）取代 DD 角色／護城河字母路由</td><td class="left">✅ 2026-09-09</td></tr>
<tr><td class="left">v4</td><td class="left">月頻輪動取代週遲滯（僅六項硬否決可換人）；上修否決改看三月（財報後另見下）；own_score 改五因子百分位排序（own_score_v4）；過熱／頂點拆分，過熱只排除核心候選；無產業集中度上限；時機燈（位置＋RS＋200 日線＋階段收斂成單一燈號）</td><td class="left">✅ 2026-09-17</td></tr>
<tr><td class="left">v4.1</td><td class="left">融券占流通股比 &gt;10% 只能衛星；基期效應（FY1→FY2 低基期跳增改用 FY2→FY3 成長）；循環股守門（毛利跨距／capex 佔比 × PEG 過低）</td><td class="left">✅ 2026-09-17</td></tr>
<tr><td class="left">v5</td><td class="left">品質派資格 × 上修排序 × 歷史新高板機：own_score_v4 退為對照 tooltip，排序改上修單一變數；耐久與融券高升級為整體資格閘（沒有衛星軌可退）；衛星軌取消，池扣掉核心即等待池；時機燈全面改讀距歷史新高（還原權息全歷史）＋200 日線</td><td class="left">✅ 2026-09-17</td></tr>
</tbody></table>
</div>"""
    # 2026-07-10 選股主控台整併：engine 總覽改輸出 nav-less 片段，供 /cockpit/#seats
    # 分頁 iframe 嵌入；/engine/index.html 已改為 redirect stub（見 site_nav SKIP_FILES）。
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "_index_body.html").write_text(
        page_embed_shell("決策引擎 · 席位排序", body,
                         "選股邏輯一頁版：品質派資格 × 上修排序 × 距歷史新高時機燈 × DD 選配（veto／角色標籤）× 月頻核心輪動 × 自動結算"),
        encoding="utf-8")
    print("engine/_index_body.html written (nav-less 片段，供主控台席位排序分頁)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
