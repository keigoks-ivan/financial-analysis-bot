#!/usr/bin/env python3
"""實單頁的 Supertrend 區塊（HTML 片段）。只組版，不抓價、不算訊號：數字全部來自主腳本傳進來的
sigs（含 st 欄位）與執行層重放結果。文字依 zh-analyst-prose：結論先行、白話、數字不堆。

被 update_long_track_w52_adaptive.py 匯入；與主腳本之間用參數傳資料，不反向匯入主腳本。
"""
from __future__ import annotations

import supertrend_core as stc
from datetime import date as _date, timedelta as _td

_WD = "一二三四五六日"


def _wd(ds: str) -> str:
    """ISO 日期 -> 星期幾（一～日）。"""
    return _WD[_date.fromisoformat(ds).weekday()]


def _next_day_label(ds: str) -> str:
    """訊號日之後的下一個平日（不查休市日），回傳「MM-DD，週X」。"""
    d = _date.fromisoformat(ds) + _td(days=1)
    while d.weekday() >= 5:
        d += _td(days=1)
    return f"{d.strftime('%m-%d')}，週{_WD[d.weekday()]}"

PAGE_URL = "/backtest/supertrend_vs_live/"
CROSS_NOTE = "v7-backtest docs/Supertrend_Cross_Market_Results.md"


def _dir_pill(d: int) -> str:
    if d == 1:
        return '<span class="tag" style="background:var(--green-bg);color:var(--green-text)">多</span>'
    return '<span class="tag" style="background:var(--red-bg);color:var(--red-text)">空</span>'


def _fmt(x: float) -> str:
    return f"{x:,.2f}"


def trigger_text(st: dict) -> str:
    """一檔的「下一個會動的價位」純文字（頁面卡片與信件共用）。st 可以是主腳本的 sigs[t]["st"]
    （巢狀，含 confirmed／partial），也可以是 state.json 的 tickers[t]["st"]（扁平：w／m／w_thr／m_thr…）。"""
    parts = []
    for key, flat, lab, when in (("week", "w", "週線", "本週"), ("month", "m", "月線", "本月")):
        if "week" in st:
            t = stc.thresholds(st)[key]
            d, thr, exact = t["dir"], t["thr"], t["exact"]
        else:
            d, thr, exact = st[flat], st[flat + "_thr"], st[flat + "_exact"]
        verb = "跌破" if d == 1 else "站上"
        flip = "翻空" if d == 1 else "翻多"
        approx = "" if exact else "（新一根開始後會微調）"
        parts.append(f"{when}收盤{verb} {_fmt(thr)} {lab}{flip}{approx}")
    return "；".join(parts)


def status_card(sigs: dict, legs: list, exec_last: dict, mode: str, cutover: str) -> str:
    """每檔的週線／月線 Supertrend 狀態表。mode＝"preview"（切換前，僅預覽）或 "live"（已生效）。"""
    rows = ""
    moves = []
    for t in legs:
        st = sigs[t].get("st")
        if not st:
            rows += f'<tr><td><b>{t}</b></td><td colspan="8" style="color:var(--muted)">Supertrend 資料暫缺</td></tr>'
            continue
        th = stc.thresholds(st)
        w, m = st["week"], st["month"]
        lv = st["level_pct"]
        cur = exec_last.get(t)
        cur_lv = None if cur is None else cur * 2
        if cur_lv is not None and abs(cur_lv - lv) > 1e-9:
            moves.append(f"{t} {cur_lv:.0f}% → {lv}%")

        def cell(key, tf):
            x = th[key]
            verb = "跌破" if x["dir"] == 1 else "站上"
            approx = "" if x["exact"] else "＊"
            return (f'<td class="num">{_fmt(tf["line"])}</td>'
                    f'<td>{verb} <b>{_fmt(x["thr"])}</b>{approx}<br>'
                    f'<span style="color:var(--muted);font-size:.74rem">目前 {_fmt(x["close"])}，離 {x["gap_pct"]:+.1f}%</span></td>')
        rows += (f'<tr><td><b>{t}</b></td><td>{_dir_pill(w["dir"])}</td>{cell("week", w)}'
                 f'<td>{_dir_pill(m["dir"])}</td>{cell("month", m)}'
                 f'<td class="num"><b>{lv}%</b></td>'
                 + ('' if mode == "pure" else
                    f'<td class="num">{"—" if cur_lv is None else f"{cur_lv:.0f}%"}'
                    f'{"" if cur_lv is None or abs(cur_lv - lv) <= 1e-9 else f" → <b>{lv}%</b>"}</td>')
                 + '</tr>\n')
    if mode == "preview":
        title = f"Supertrend 預覽（{cutover} 收盤起實單照這套，現在還沒生效）"
        lead = (f"實單指數部四檔從 {cutover}（週{_wd(cutover)}）收盤的訊號起改看 Supertrend，下一個交易日下單；在那之前仍照 W52 規則。"
                "下表是用現在的價格算出來的結果，只供預覽。")
        if moves:
            lead += "如果今天就切換，要調整：" + "、".join(moves) + "。"
        elif any(sigs[t].get("st") for t in legs):
            lead += "如果今天就切換，這個市場的水位不用動。"
        lvl_hdr = "預覽水位"
    elif mode == "pure":
        title = "Supertrend 現況"
        lead = ("每檔水位＝70% 看週線、30% 看月線，各自多頭才持有；所以水位只會是 100／70／30／0%。"
                "週線在每週最後一個交易日收盤後判定、月線在月底收盤後判定，下一個交易日調整。")
        lvl_hdr = "水位"
    else:
        title = "Supertrend 現況"
        lead = ("每檔水位＝70% 看週線、30% 看月線，各自多頭才持有；所以水位只會是 100／70／30／0%。"
                "週線在每週最後一個交易日收盤後判定、月線在月底收盤後判定，下一個交易日調整。")
        lvl_hdr = "目標水位"
        if moves:
            lead += "下一個交易日要調整：" + "、".join(moves) + "（現持是下單前的水位）。"
    return f"""<div class="card" style="border:2px solid var(--brand);background:#f5f8ff">
<h3 style="color:var(--brand)">{title}</h3>
<p style="font-size:.82rem;color:var(--muted);margin-bottom:.7rem">{lead}</p>
<div class="tablewrap"><table>
<thead><tr><th>檔</th><th>週線</th><th class="num">線值</th><th>翻轉門檻</th><th>月線</th><th class="num">線值</th><th>翻轉門檻</th><th class="num">{lvl_hdr}</th>{'' if mode == "pure" else f'<th class="num">{"現持水位（下單前）" if mode != "preview" else "現持水位"}</th>'}</tr></thead>
<tbody>{rows}</tbody></table></div>
<div style="font-size:.76rem;color:var(--muted);margin-top:.5rem">多頭時線在價格下方、當作支撐；空頭時線在價格上方、當作壓力。門檻是進行中那根 K 棒目前的線值，收完前會小幅移動，以收盤為準。＊ 新的一根 K 棒還沒開始，先用上一根的線值近似。參數：美股 ATR 14、倍數 3，台股 ATR 14、倍數 2，用沒有調整股息的 K 線。</div>
</div>"""


def recent_table(t: str, st: dict | None) -> str:
    if not st or not st.get("recent"):
        return ""
    def tbl(key, lab):
        rows = ""
        for r in reversed(st["recent"][key]):
            tag = "" if r["done"] else ' <span style="color:var(--amber-text);font-size:.72rem">進行中</span>'
            rows += (f'<tr><td>{r["date"]}{tag}</td><td class="num">{_fmt(r["close"])}</td>'
                     f'<td class="num">{_fmt(r["line"])}</td><td>{_dir_pill(r["dir"])}</td></tr>\n')
        return (f'<table><thead><tr><th>{lab}（K 棒日）</th><th class="num">收盤</th><th class="num">線值</th><th>方向</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
    return f"""<div class="card">
<h3>{t} — Supertrend 近幾根 K 棒軌跡</h3>
<div class="grid2">{tbl("week", "週線")}{tbl("month", "月線")}</div>
</div>"""


def backtest_card(cutover: str) -> str:
    """Supertrend 回測數字（靜態轉錄自 /backtest/supertrend_vs_live/ 與 v7 跨標的結果，不隨每日資料重算）。"""
    return f"""<div class="card">
<h3>Supertrend 對原規則的回測（描述性比較，沒有事前登記）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
數字轉錄自 <a href="{PAGE_URL}">Supertrend 對實單</a> 頁（資料到 2026-10-16），兩套放進同一個回測引擎：每邊成本 7 個基點、現金有利息、收盤出訊號、下一個交易日成交；台股計入證交稅，美股兩套都加同一套公債黃金。「原規則」指 W52  × 自適應波動率 × 執行層（上限 100%，不借錢）。</p>
<div class="tablewrap"><table>
<thead><tr><th>市場與期間</th><th>規則</th><th class="num">年化</th><th class="num">最大跌幅</th><th class="num">Calmar</th><th class="num">每年下單次數</th></tr></thead>
<tbody>
<tr class="rowhl"><td rowspan="2">美股 2005-01 至 2026-10</td><td>Supertrend 70/30</td><td class="num">15.2%</td><td class="num">−19.9%</td><td class="num">0.78</td><td class="num">3.1</td></tr>
<tr><td>原規則（W52，已改為對照線）</td><td class="num">14.1%</td><td class="num">−18.5%</td><td class="num">0.76</td><td class="num">7.7</td></tr>
<tr class="rowhl"><td rowspan="2">台股 2006-09 至 2026-10</td><td>Supertrend 70/30</td><td class="num">15.2%</td><td class="num">−20.2%</td><td class="num">0.75</td><td class="num">5.5</td></tr>
<tr><td>原規則（W52，已改為對照線）</td><td class="num">12.9%</td><td class="num">−30.6%</td><td class="num">0.42</td><td class="num">8.1</td></tr>
<tr class="rowhl"><td rowspan="2">台股 2010 至 2026-10</td><td>Supertrend 70/30</td><td class="num">15.4%</td><td class="num">—</td><td class="num">0.76</td><td class="num">—</td></tr>
<tr><td>原規則（W52，已改為對照線）</td><td class="num">14.8%</td><td class="num">—</td><td class="num">0.83</td><td class="num">—</td></tr>
</tbody></table></div>
<div class="takeaway">美股打平：Supertrend 年化多 1.1 個百分點、最大跌幅深 1.4 個百分點，Calmar 差 0.02，下單次數少六成。台股 2006 到 2009 年那一次（2008 年金融海嘯）Supertrend 少賠很多，2010 年以後兩者接近，原規則的 Calmar 略高。兩邊的年化差距，統計上都分不出誰好（成對拔靴 90% 區間跨過 0）。<br>
<b>要保守看待的地方</b>：參數是持有人看過 9 格鄰近表之後才選的（美股 ATR 14／倍數 3 是 9 格裡 Calmar 最高的一格；台股 ATR 14／倍數 2 選擇當時是第二高），2014 年以後的數字是挑選後的上界；台股的優勢集中在一次大跌。
<b>債金也改 Supertrend 的版本</b>：上表美股兩列的債金疊加都是週線三條件。實單 {cutover} 起債金也改 Supertrend（指數部 Supertrend ＋ 債金 Supertrend，ATR 14／倍數 3，2005-01 至 2026-10）時，美股整體是年化 14.7%、最大跌幅 −19.9%、Calmar 0.74，債金每年變動約 15 次降到約 4 次。<br>
跨標的對照（33 檔從未看過的標的，{CROSS_NOTE}）：Supertrend 的 Calmar 高於原規則的只有 14 檔，Calmar 比值的中位數 0.88，最大跌幅中位數深 1.5 個百分點；差別主要在下單次數，中位數每年 1.9 次對 4.4 次。</div>
</div>"""


# ---------------------------------------------------------------- 頁面文字
def pre_notice(cutover: str, decision: str) -> str:
    """切換前（現在到 cutover 之前）置於頁首的說明橫幅。"""
    return f"""<div class="oos-banner" style="background:linear-gradient(135deg,#eef4ff 0%,#e3edfb 100%);border-color:var(--brand)">
  <span class="tag-loud" style="background:var(--brand)">{cutover} 收盤起改規則</span>
  <div style="font-size:.86rem">持有人 {decision} 決定，實單指數部四檔（QQQ、SMH、0050、2330）從 <b>{cutover}（週{_wd(cutover)}）收盤的訊號</b>起，由 W52 規則改為 <b>Supertrend</b>，下一個交易日（{_next_day_label(cutover)}）第一次照新規則下單。在那之前，下面的今天結論、水位與換倉提醒仍然是 W52 規則。債金疊加（美股公債 IEF、黃金 GLD）同一天也改成 Supertrend（見下方）。<br>
  切換當天的提醒信會列出每檔從現持水位一次調到 Supertrend 水位。現行的 W52 規則會繼續每天更新，放在<a href="/long-track-w52-adaptive/w52.html">對照線頁</a>，不寄信。Supertrend 的目前狀態與回測見下方「Supertrend 預覽」與「回測與統計」。</div>
</div>

"""


def banner_live(cutover: str, decision: str, shadow_url: str) -> str:
    return f"""<div class="oos-banner">
  <span class="tag-loud">實單主系統・{cutover} 收盤起：指數部四檔照 Supertrend・email 提醒換檔</span>
  <div style="font-size:.86rem">本頁是實單主系統。<b>{cutover} 起（持有人 {decision} 拍板）</b>指數部四檔（美股 QQQ、SMH，台股 0050、2330）改看 <b>Supertrend</b>：每檔 70% 看週線、30% 看月線，各自多頭才持有，所以每檔水位只有 100%、70%、30%、0% 四種。不借錢，也沒有調整門檻：週線在每週最後一個交易日收盤後判定、月線在月底收盤後判定，下一個交易日一次調到目標水位。
  <br><br><b>怎麼讀</b>：線在價格下方是多頭、當作支撐，收盤跌破就翻空；線在價格上方是空頭，收盤站上就翻多。美股用 ATR 14、倍數 3，台股用 ATR 14、倍數 2，K 線用沒有調整股息的價格。下方「Supertrend 現況」列出每檔目前的方向、線值，以及這一週、這個月收盤到哪個價位會翻。
  <br><br><b>債金疊加</b>：美股公債（IEF）與黃金（GLD）各最多 20%（占指數部淨值）同一天也改成 Supertrend，各自 70% 週線＋30% 月線，每項只有 20%、14%、6%、0% 四種水位；ATR 14、倍數 3。換倉方式不變，只是每次的量變成水位差。生效日前仍是週線三個條件。台股沒有債金。
  <br><br><b>為什麼改，以及要保守看的地方</b>：回測裡美股 Supertrend 與原規則打平（Calmar 0.78 對 0.76），下單次數少六成；台股領先主要來自 2008 年，2010 年以後兩者接近。參數是看過鄰近表才選的，跨標的檢驗 33 檔裡只有 14 檔的 Calmar 勝過原規則。數字在下方「回測與統計」。<b>退回條件目前尚未訂定</b>，由持有人另訂後寫進規則帳本。
  <br><br>原來的 W52 × 自適應波動率規則改為<a href="{shadow_url}">對照線</a>，每日照常更新、不寄信；生效日前的紀錄不改寫。</div>
</div>

"""


def rules_live(cutover: str, decision: str, shadow_url: str) -> str:
    return f"""<div class="card">
<details>
<summary style="cursor:pointer;font-weight:600;font-size:.9rem">規則說明（點開看 Supertrend 規則、債金疊加、沿革與揭露，白話版）</summary>
<div style="margin-top:.9rem">
<div class="card">
<h3>追蹤主系統規則（Supertrend；{cutover} 收盤起，持有人 {decision} 拍板）</h3>
<div class="rule-list">
① <b>四檔、兩市場</b>：美股 {{QQQ、SMH}}、台股 {{0050、2330}}，每檔各有自己的水位。兩檔各占各市場指數部的一半，所以水位 ÷ 2 就是該檔占指數部淨值的比例。個股部位不在這個系統內。<br>
② <b>Supertrend 是什麼</b>：一條依平均真實波幅（ATR，近 14 根 K 棒的平均波動）上下推開的追蹤線，算法照 TradingView 內建的 <code>ta.supertrend</code>，取 K 棒高低點中間價。收盤站上線是多頭，跌破線是空頭；倍數越大，線離價格越遠，訊號越慢。美股 ATR 14、倍數 3，台股 ATR 14、倍數 2；TradingView 預設是 ATR 10、倍數 3，要對照請先改成這兩組。K 線用沒有調整股息的價格（已調整拆股）。<br>
③ <b>水位</b>＝70% × 週線（多為 1、空為 0）＋30% × 月線（多為 1、空為 0），只做多，所以只有 100%、70%、30%、0% 四種。週線以週五為一週最後一天，月線以日曆月底；一根 K 棒要等那一期最後一個平日收盤後才算數，沒收完的那根只看門檻、不下單。<br>
④ <b>執行</b>：訊號日收盤判定，下一個交易日調到目標水位，一次到位，不分段、不設門檻、不取整。成本與回測一致（每邊 7 個基點）。不借錢，水位上限 100%。<br>
⑤ <b>債金疊加（美股）</b>：IEF 與 GLD 各最多 20%（占指數部淨值）。{cutover} 起各看 Supertrend，70% 週線＋30% 月線，水位 20／14／6／0%，週五或月底收盤判定、下一個交易日換倉；此前是週線三個條件（週收盤 &gt; 40 週均線、&gt; 52 週均線、&gt; 52 週前的收盤，每成立一條加三分之一）。台股沒有這一層。<br>
⑥ <b>資料</b>：yfinance 未調股息日 K；台股最新一兩根若 yfinance 晚到，用證交所官方日 K 補，補不上就標「資料延遲」、不換倉。<br>
<span style="color:var(--muted);font-size:.78rem">本頁每交易日更新（台股收盤後、美股收盤後各一次）。可行動變化＝任一檔目標水位和現持不同，或美股債金水位改變。週線或月線翻轉當天水位一定會變，會出現在換倉提醒裡；另有「Supertrend 週線／月線翻轉通知」在翻轉確認時，以及週五預警（K 棒還沒收完就站到線的另一邊）時另外寄信。</span>
</div>
</div>

<div class="card">
<details>
<summary style="cursor:pointer;font-weight:600;font-size:.9rem">規則沿革（歷次變更紀錄）</summary>
<div class="rule-list" style="font-size:.82rem;margin-top:.75rem">
• <b>2026-07-17</b>：W52 單線閘門 × 自適應 σ_t 定案；<b>2026-07-18</b> 起採為實單主系統（上限 150%）。<br>
• <b>2026-10-19</b>（持有人 10-17 拍板）：美股改債金版、台股改不借錢版，股票上限 100%。<br>
• <b>2026-10-30 收盤起</b>：執行層減碼門檻由兩格降為一格，加碼維持兩格。<br>
• <b>{cutover}</b>（持有人 {decision} 拍板）：<b>指數部四檔改 Supertrend</b>，週線 70%＋月線 30%；同日債金疊加（IEF、GLD）也改 Supertrend（14／3，水位 20／14／6／0%），依據是持有人看過比較後的決定。生效日起的紀錄帶 <code>rule: "st_live"</code>，生效日前的 history 不改寫；切換當日每檔從現持水位一次調到 Supertrend 水位。原 W52 規則以 <a href="{shadow_url}">對照線</a> 續跑，不寄信。state.json 的 <code>rule_changes</code> 有這一筆。<br>
</div>
</details>
</div>

<div class="card" style="border:2px solid var(--amber-border);background:var(--amber-bg)">
<h3 style="color:var(--amber-text)">誠實揭露（採用前必讀）</h3>
<div class="rule-list" style="font-size:.82rem">
① <b>參數是看過結果才選的</b>：持有人看過 9 格鄰近表之後選了美股 ATR 14／倍數 3、台股 ATR 14／倍數 2，回測數字是挑選後的上界，不是預期值。<br>
② <b>台股的優勢集中在一次大跌</b>：2006 年 9 月起的 20 年裡，Supertrend 領先主要來自 2007 到 2009 年；2010 年以後兩者接近，原規則的 Calmar 略高（0.83 對 0.76）。<br>
③ <b>跨標的沒有穩定勝出</b>：33 檔從未看過的標的，Supertrend 的 Calmar 勝過原規則的有 14 檔，比值中位數 0.88，最大跌幅中位數深 1.5 個百分點；它的好處在於下單次數少一半以上。<br>
④ <b>統計上分不出誰好</b>：成對區塊拔靴 2,000 次，美台年化差距的 90% 區間都跨過 0。<br>
⑤ <b>急跌時留三成</b>：月線那 30% 在急跌時不會賣，疫情那一段美股只用月線的版本跌幅和一直抱著幾乎一樣。<br>
⑥ <b>債金疊加只在美股測過</b>，債券與黃金在 2005 至 2026 年整體順風，升息期（2022 至 2023 年）沒有保護；債金改 Supertrend 後，2022 年債市與 2013 年黃金的出場比三條件慢。<br>
⑦ <b>前瞻紀錄有規則斷點</b>：記分板停在 2026-10-16，Supertrend 階段不在那裡判；退回條件尚未訂定。
</div>
</div>
</div>
</details>
</div>

"""


def shadow_banner(cutover: str, live_url: str) -> str:
    return f"""<div class="oos-banner">
  <span class="tag-loud">對照線・{cutover} 前的實單規則・不下單、不寄信</span>
  <div style="font-size:.86rem">本頁保留 {cutover} 前的實單規則（<b>W52 閘門 × 自適應波動率 × 執行層，上限 100%、不借錢，美股另加債金</b>），每交易日照常更新，用來和現行實單（<a href="{live_url}">Supertrend</a>）並排看。{cutover} 起實單改看 Supertrend；本頁的紀錄與實單在生效日前逐筆相同，之後各自往下走。以下規則說明與回測數字是 W52 規則的版本。</div>
</div>

"""


def banner_pure() -> str:
    """實單頁頂端說明（顯示層：整段歷史當作一直都是 Supertrend，不提舊規則）。"""
    return """<div class="oos-banner">
  <span class="tag-loud">實單主系統・指數部四檔照 Supertrend・email 提醒換檔</span>
  <div style="font-size:.86rem">本頁是實單主系統。指數部四檔（美股 QQQ、SMH，台股 0050、2330）每檔 <b>70% 看週線、30% 看月線</b>的 Supertrend，各自多頭才持有，所以每檔水位只有 100%、70%、30%、0% 四種。不借錢，也沒有調整門檻：週線在每週最後一個交易日收盤後判定、月線在月底收盤後判定，下一個交易日一次調到目標水位。
  <br><br><b>怎麼讀</b>：線在價格下方是多頭、當作支撐，收盤跌破就翻空；線在價格上方是空頭，收盤站上就翻多。美股用 ATR 14、倍數 3，台股用 ATR 14、倍數 2，K 線用沒有調整股息的價格。下方「Supertrend 現況」列出每檔目前的方向、線值，以及這一週、這個月收盤到哪個價位會翻。
  <br><br><b>債金疊加</b>：美股公債（IEF）與黃金（GLD）各最多 20%（占指數部淨值），同樣各自 70% 週線＋30% 月線，每項只有 20%、14%、6%、0% 四種水位；ATR 14、倍數 3。台股沒有債金。
  <br><br><b>要保守看的地方</b>：參數是看過鄰近表之後才選的，回測數字是挑選後的上界，不是預期值。</div>
</div>

"""


W52_LINE = ('<div style="font-size:.82rem;color:var(--muted);margin:.8rem 0 1rem">'
            '原規則（W52）的對照線見 <a href="/long-track-w52-adaptive/w52.html">/long-track-w52-adaptive/w52.html</a></div>')


def rules_pure() -> str:
    """規則說明（顯示層）：Supertrend 規則、債金疊加、揭露；不放沿革，結尾只留一行對照線連結。"""
    return f"""<div class="card">
<details>
<summary style="cursor:pointer;font-weight:600;font-size:.9rem">規則說明（點開看 Supertrend 規則、債金疊加與揭露，白話版）</summary>
<div style="margin-top:.9rem">
<div class="card">
<h3>追蹤主系統規則（Supertrend）</h3>
<div class="rule-list">
① <b>四檔、兩市場</b>：美股 {{QQQ、SMH}}、台股 {{0050、2330}}，每檔各有自己的水位。兩檔各占各市場指數部的一半，所以水位 ÷ 2 就是該檔占指數部淨值的比例。個股部位不在這個系統內。<br>
② <b>Supertrend 是什麼</b>：一條依平均真實波幅（ATR，近 14 根 K 棒的平均波動）上下推開的追蹤線，算法照 TradingView 內建的 <code>ta.supertrend</code>，取 K 棒高低點中間價。收盤站上線是多頭，跌破線是空頭；倍數越大，線離價格越遠，訊號越慢。美股 ATR 14、倍數 3，台股 ATR 14、倍數 2；TradingView 預設是 ATR 10、倍數 3，要對照請先改成這兩組。K 線用沒有調整股息的價格（已調整拆股）。<br>
③ <b>水位</b>＝70% × 週線（多為 1、空為 0）＋30% × 月線（多為 1、空為 0），只做多，所以只有 100%、70%、30%、0% 四種。週線以週五為一週最後一天，月線以日曆月底；一根 K 棒要等那一期最後一個平日收盤後才算數，沒收完的那根只看門檻、不下單。<br>
④ <b>執行</b>：訊號日收盤判定，下一個交易日調到目標水位，一次到位，不分段、不設門檻、不取整。成本與回測一致（每邊 7 個基點）。不借錢，水位上限 100%。<br>
⑤ <b>債金疊加（美股）</b>：IEF 與 GLD 各最多 20%（占指數部淨值），各看 Supertrend，70% 週線＋30% 月線，水位 20／14／6／0%，週五或月底收盤判定、下一個交易日換倉。台股沒有這一層。<br>
⑥ <b>資料</b>：yfinance 未調股息日 K；台股最新一兩根若 yfinance 晚到，用證交所官方日 K 補，補不上就標「資料延遲」、不換倉。<br>
<span style="color:var(--muted);font-size:.78rem">本頁每交易日更新（台股收盤後、美股收盤後各一次）。週線或月線翻轉當天水位一定會變，會出現在換倉提醒裡；另有「Supertrend 週線／月線翻轉通知」在翻轉確認時，以及週五預警（K 棒還沒收完就站到線的另一邊）時另外寄信。</span>
</div>
</div>

<div class="card" style="border:2px solid var(--amber-border);background:var(--amber-bg)">
<h3 style="color:var(--amber-text)">誠實揭露（採用前必讀）</h3>
<div class="rule-list" style="font-size:.82rem">
① <b>參數是看過結果才選的</b>：看過 9 格鄰近表之後選了美股 ATR 14／倍數 3、台股 ATR 14／倍數 2，回測數字是挑選後的上界，不是預期值。<br>
② <b>急跌時留三成</b>：月線那 30% 在急跌時不會賣，疫情那一段美股只用月線的版本跌幅和一直抱著幾乎一樣。<br>
③ <b>債金疊加只在美股測過</b>，債券與黃金在 2005 至 2026 年整體順風，升息期（2022 至 2023 年）沒有保護。
</div>
</div>
</div>
</details>
</div>
{W52_LINE}
"""


def backtest_card_pure() -> str:
    """Supertrend 回測（只放 Supertrend 與買進持有）。靜態轉錄自 v7-backtest results/supertrend_vs_live/results.json，
    資料到 2026-10-16，不隨每日資料重算。美股列為指數部 Supertrend 加債金 Supertrend（年化 14.7%、最大跌幅 −19.9%、Calmar 0.74）。"""
    return f"""<div class="card">
<h3>Supertrend 回測（資料到 2026-10-16）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
數字轉錄自 <a href="{PAGE_URL}">Supertrend 回測頁</a>（v7-backtest results/supertrend_vs_live/results.json，資料到 2026-10-16）。每邊成本 7 個基點、現金有利息、收盤出訊號、下一個交易日成交；台股計入證交稅；美股含公債黃金的 Supertrend。買進持有是兩檔各半、一直滿倉。</p>
<div class="tablewrap"><table>
<thead><tr><th>市場與期間</th><th>配置</th><th class="num">年化</th><th class="num">最大跌幅</th><th class="num">Calmar</th><th class="num">指數部每年下單次數</th></tr></thead>
<tbody>
<tr class="rowhl"><td rowspan="2">美股 2005-01 至 2026-10</td><td>Supertrend 70/30</td><td class="num">14.7%</td><td class="num">−19.9%</td><td class="num">0.74</td><td class="num">3.1</td></tr>
<tr class="rowbh"><td>買進持有</td><td class="num">17.0%</td><td class="num">−56.9%</td><td class="num">0.30</td><td class="num">0</td></tr>
<tr class="rowhl"><td rowspan="2">台股 2006-09 至 2026-10</td><td>Supertrend 70/30</td><td class="num">15.2%</td><td class="num">−20.2%</td><td class="num">0.75</td><td class="num">5.5</td></tr>
<tr class="rowbh"><td>買進持有</td><td class="num">19.8%</td><td class="num">−49.3%</td><td class="num">0.40</td><td class="num">0</td></tr>
</tbody></table></div>
<div class="takeaway">Supertrend 的年化比一直抱著少 2.3 個百分點（美股）與 4.7 個百分點（台股），換到最大跌幅從 −57%、−49% 縮到 −20% 上下，Calmar 約為買進持有的兩倍。<br>
<b>要保守看待的地方</b>：參數是看過鄰近表之後才選的，這些數字是挑選後的上界；台股的優勢集中在 2008 年那一次大跌。</div>
</div>"""
