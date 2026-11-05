"""席位規則卡（2026-11-06）：美股看板、台股席位、精選榜三套規則各一張卡，頁面上的規則說明只有這一份正本。

純文字產生器，不讀寫狀態、不連網，也不影響任何選席或倉位行為。門檻、倉位、日期一律從 grp／seat_st／seat_tm／
seat_valhold 的常數讀，常數改了卡跟著變。規則的程式依據：
  進池 grp.grp_score／grp.quality_gate／grp.valuation_gate；補席 build_arena.select_hold_roster；
  賣法 seat_st.apply_overlay（已切換）、seat_tm.select_roster（未切換、大盤多頭續抱）、seat_valhold（估值偏貴現任）；
  台股差異 build_seats_tw；精選榜 build_tenbagger。
版本史來自 knowledge/rule_ledger.md 與各程式檔頭；帳本缺 v5.3～v5.6 的專屬列，這幾列依程式檔頭整理。
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path

from engine import grp, seat_st, seat_tm, seat_valhold

CARD_ID = "seat-rules"
PICKS_MARK = ("<!--RULECARD-->", "<!--/RULECARD-->")


def _g(x) -> str:
    return f"{x:g}"


def _fold(title: str, body: str, open_: bool = False) -> str:
    return (f'<details class="bw-fold"{" open" if open_ else ""}><summary>{title}</summary>'
            f'<div class="rc-body">{body}</div></details>')


_CSS = """<style>
.rc-card{border:1px solid var(--line,var(--border,#ddd));border-radius:6px;padding:10px 12px;margin:10px 0}
.rc-card .bw-sec{margin-top:0}
.rc-card .rc-body{font-size:12.5px;line-height:1.7}
.rc-card .rc-body ul{margin:.3rem 0 .3rem 1.2rem;padding:0}
.rc-card table{width:100%;border-collapse:collapse;font-size:12px;margin:.4rem 0}
.rc-card th,.rc-card td{padding:5px 7px;border-bottom:1px solid var(--line-soft,var(--border,#eee));text-align:left;white-space:normal;vertical-align:top}
.rc-card th{font-weight:700}
.rc-card .rc-scroll{overflow-x:auto;max-width:100%}
.rc-card .rc-sell th:first-child,.rc-card .rc-sell td:first-child{position:sticky;left:0;background:var(--card,#fff);min-width:92px}
.rc-card .rc-sell td.sell{color:var(--neg,#b91c1c);font-weight:700}
.rc-card .rc-sell td.keep{color:var(--pos,#15803d)}
</style>"""


def _cls(cell: str) -> str:
    return ' class="sell"' if cell.startswith("賣") else (' class="keep"' if cell.startswith("不賣") else "")


def _table(head: list, rows: list, cls: str = "") -> str:
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td{_cls(c) if cls == 'rc-sell' and i else ''}>{c}</td>" for i, c in enumerate(r)) + "</tr>"
                for r in rows)
    tag = f'<table class="{cls or "rc-t"}">'
    return f'<div class="rc-scroll">{tag}<thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def market_line(market, label: str = "SPY 還原收盤", bear_extra: str = "") -> str:
    """目前大盤狀態一行（美股，資料來自 seat_tm.market_state）。"""
    st = (market or {}).get("status")
    d = escape((market or {}).get("data_date") or "—")
    if not market or st in ("stale", "missing"):
        return (f'<div class="bw-note-line">大盤資料未更新，本週照空頭處理，用「時機燈轉紅就賣」（最近一筆資料日期 {d}）。</div>')
    nums = f"{label} {market['close']:,.2f}"
    nums += (f"，{seat_tm.MKT_MA} 日線 {market['ma200']:,.2f}" if market.get("ma200") is not None
             else f"，{seat_tm.MKT_MA} 日線資料不足，算多頭")
    word, way = (("多頭", "本週未切換的持股，紅燈不賣") if st == "bull" else ("空頭", "本週未切換的持股，時機燈轉紅就賣"))
    return f'<div class="bw-note-line">大盤狀態（{d} 收盤）：{nums}，<b>{word}</b>。{way}。</div>'


def _lamp_defs() -> str:
    g, r = abs(grp.ATH_GREEN_DIST), abs(grp.ATH_RED_DIST)
    return (f"綠＝距歷史新高 {_g(g)}% 以內；黃＝距新高 {_g(g)}% 到 {_g(r)}%；橘＝條件同綠，但近 12 個月（扣最近一個月）漲幅超過 "
            f"{_g(grp.MOM_12_1_OVERHEAT)}%；紅＝距新高超過 {_g(r)}%，或跌破 200 日線；不合格＝股價在 52 週線之下。"
            "綠、黃、橘都要站上 200 日線。")


def _versions(rows: list) -> str:
    return _table(["日期", "改了什麼", "回測"], rows)


US_VERSIONS = [
    ["2026-09-17", "席位引擎改品質派資格（品質、三年成長、價位、否決、融券），核心席月頻輪動", "持有人拍板"],
    ["2026-09-18", "加估值條件（PEG 大於 2.0，或相對五年均值超過 1.75 倍）；新增「③b 太貴不入池」區", "持有人拍板，不是回測"],
    ["2026-10-09", "三年成長門檻統一 15%；耐久降為旗標；核心席改每週六依亮燈選席，可空席", "持有人拍板"],
    ["2026-10-18", "黃燈由半倉改滿倉；美股品質條件改自由現金流大於 0", "持有人拍板；黃燈滿倉在台股回測屬「無法分辨」"],
    ["2026-10-21", "拿掉「上修 5% 才進池」，上修只排序", "未通過，持有人裁量"],
    ["2026-10-21", "美股改「大盤空頭才看紅燈」", "未通過，持有人裁量（大型股回測變好，但登記母體是中小型）"],
    ["2026-10-30", "池內排序改 PEG 由低到高", "未通過，持有人裁量（前半段輸隨機，PEG 口徑與回測不同）"],
    ["2026-10-30", "現任抱著，不因排名被換掉", "持有人拍板，把網站改回與回測一致"],
    ["2026-11-07 起（11-05 拍板）", "盤整突破或停損線高過買進價，改看週線 Supertrend；之後只在翻空或基本面不合格時賣",
     "未通過，持有人裁量：美股看板 Calmar 0.38 對 0.36，台股 0.78 對 0.78，打平；17 組試驗都是看過結果才挑"],
    ["2026-11-07 起（11-05 拍板）", "還沒切換的現任若只有估值不過，繼續坐席但不加碼", "無回測，持有人拍板"],
    ["2026-11-05", "實作漏接修正（不是規則變更）：已切換持股原本沒吃 yfinance 下修否決，現在一併吃；「太貴不入池」原本誤列市值不足的名字，現已排除",
     "不適用"],
]

TW_VERSIONS = [
    ["2026-10-10", "台股核心席上線，美股核心席規則跑台股池", "持有人拍板"],
    ["2026-10-18", "看大盤切換出場；黃燈滿倉", "切換出場：登記結論「現行維持」，台股通過四項，持有人破例；黃燈滿倉屬「無法分辨」"],
    ["2026-10-21", "大盤空頭週不補新席；拿掉上修門檻", "不補新席：登記結論「現行維持」，台股通過四項，持有人破例；拿掉上修門檻：未通過，持有人裁量"],
    ["2026-10-21 至 10-23", "加上每月依波動分配，三天後撤回", "撤回是持有人決定"],
    ["2026-11-07 起", "同美股：切換 Supertrend、估值偏貴現任續抱不加碼", "同美股"],
]

PICKS_VERSIONS = [
    ["2026-09-17", "爆發組退役，十倍組改成沿用席位資格規則、跑在小市值帶", "持有人拍板"],
    ["2026-10-21", "做成 10 席，每週六重選；拿掉上修門檻", "未通過，持有人裁量（台股前段只有 46%）"],
    ["2026-11-07 起", "賣法不變，不套用 Supertrend 與估值例外", "比較頁裡精選榜換成 Supertrend 賣法後比現行差"],
]


def us_card_html(market=None) -> str:
    """美股看板規則卡。market＝seat_tm.market_state() 的結果（可為 None）。"""
    cut = seat_st.CUTOVER_DATE
    vcut = seat_valhold.CUTOVER_DATE
    n = seat_st.SLOTS
    sell = _table(
        ["持股狀態", "週線 Supertrend 翻空", "距新高跌超過 10%", "跌破 200 日線", "跌破 52 週線", "估值偏貴", "融券超過 10%",
         "市值低於 200 億", "基本面不合格"],
        [["已切換 Supertrend", "賣", "不賣", "不賣", "不賣", "不賣", "不賣", "不賣", "賣"],
         ["未切換，大盤多頭", "不適用", "不賣（續抱）", "不賣（續抱）", "賣", f"不賣，不加碼（{vcut} 起）", "賣", "賣", "賣"],
         ["未切換，大盤空頭", "不適用", "賣", "賣", "賣", f"不賣，不加碼（{vcut} 起）", "賣", "賣", "賣"]],
        cls="rc-sell")
    top = (
        f'<div class="bw-note-line"><b>一句話</b>：看板固定 {n} 席，每週六依週五收盤判斷一次。進場看資格和時機燈，排隊看 PEG 由低到高。'
        '持股分兩種賣法：已切換成 Supertrend 的，只在週線 Supertrend 翻空或基本面不合格時賣；還沒切換的，照時機燈和大盤多空處理。'
        f'（{cut} 週六席位排程起）</div>'
        f'<div class="bw-note-line"><b>什麼時候賣</b>：判斷都在週六做。週中燈號轉紅，未切換持股的倉位當天降到 0'
        '（大盤多頭續抱的例外除外），席位等週六才下。</div>'
        + sell
        + '<div class="bw-note-line">基本面不合格＝三年成長沒過、品質沒過、'
          f'財報後上修在 {_g(grp.EPS_REV_3M_VETO)}% 以下、yfinance 30 天明年預估下修 {_g(abs(grp.R_VETO_FY1))}% 以上、'
          f'體質拒絕、衰退訊號 ⛔、{grp.DD_FRESH_DAYS} 天內 DD 迴避。已切換的持股只看這幾項；未切換的再加看價位、融券、市值。'
          f'估值偏貴的例外只給還沒切換、其他資格全過的現任；空席照樣不補估值偏貴的名字，這些名字只列在「③b 太貴不入池」。</div>'
        + '<div class="bw-note-line">大盤多頭＝SPY 還原收盤在 '
          f'{seat_tm.MKT_MA} 日線之上（等於也算多頭）。SPY 資料缺或比決策日早超過 {seat_tm.MKT_STALE_DAYS} 天，當週照空頭處理。'
          '美股的多頭例外很寬，所有只因時機燈轉紅的持股都續抱，連跌破自己 200 日線的也續抱；台股比較嚴，見台股席位的規則卡。</div>'
        + market_line(market))
    g, r = abs(grp.ATH_GREEN_DIST), abs(grp.ATH_RED_DIST)
    admit = _fold("1 誰能進池", (
        '<p>下面八項全過才進池，資料缺漏一律視為沒過（估值例外：兩項資料都缺不算偏貴）。</p>'
        + _table(["項目", "門檻"], [
            ["市值", f"{_g(grp.MKTCAP_MIN / 1e8)} 億美元以上；查不到市值也不過"],
            ["品質", f"投入資本報酬率（ROIC）{_g(grp.Q_ROIC_MIN)}% 以上，且自由現金流利潤率大於 0（剛好 0 不過）。金融股兩項資料都缺，不進池"],
            ["三年成長", f"Koyfin 預估的每股盈餘（EPS）今年到後年的年化成長 {_g(grp.G_MIN_CAGR)}% 以上；沒有第三年預估就不過。"
                         f"遇基期失真（明年預估是今年的 {_g(grp.BASE_EFFECT_STEP12_X)} 倍以上，而且後年再成長不到 "
                         f"{_g(grp.BASE_EFFECT_STEP23_CAP * 100)}%），改用明年到後年的成長率"],
            ["價位", "股價在 52 週均線之上，而且有距 52 週高點的資料"],
            ["財報後上修", f"最近一次財報後的 EPS 預估修正大於 {_g(grp.EPS_REV_3M_VETO)}%；缺財報錨定時看近三個月；"
                          f"兩者都缺，改看明年預估單月是否在 {_g(grp.R_VETO_FY1)}% 以下。另外 yfinance 的 30 天明年預估下修到 "
                          f"{_g(grp.R_VETO_FY1)}% 以下，也排除"],
            ["基本面否決", f"體質評級「拒絕」、衰退訊號 ⛔、{grp.DD_FRESH_DAYS} 天內的 DD 裁決為「迴避」（DD 年齡不明也算），任一項成立就排除"],
            ["融券", f"融券占流通股比超過 {_g(grp.SI_CORE_EXCLUDE_PCT)}% 排除"],
            ["估值", f"PEG 大於 {_g(grp.VAL_PEG_MAX)}，或預估本益比相對自己五年均值超過 {_g(grp.VAL_PE_VS_5Y_MAX)} 倍，任一項成立就是估值偏貴"],
        ])
        + '<p>PEG ＝ 現價 ÷ 明年預估 EPS ÷ 三年 EPS 年化成長。</p>'
        '<p>不影響資格：耐久只是旗標；過熱只讓時機燈變橘燈、半倉；頂點、內部人買賣只是備註；DD 不是必要條件，只能否決或標角色。</p>'
        '<p>池內排序：PEG 由低到高，PEG 缺值或不大於 0 的排最後；同值再比財報後上修（高者在前）、隱含成長、盈餘殖利率。</p>'))
    fill = _fold("2 空席怎麼補", (
        '<ul><li>每週六（台北）依週五收盤判斷。平日只更新燈號、倉位和排隊名單，不換人。</li>'
        '<li>現任先保留，不會因為池裡有排名更前的名字而被換掉。</li>'
        '<li>空席從池內「亮燈」且還沒在席的名字，依池內排序補到滿。</li>'
        f'<li>亮燈指時機燈是綠、黃或橘：距還原權息後歷史新高在 {_g(r)}% 以內，且站上 200 日線。資料缺距新高的黃燈也算亮燈，倉位只給一半。</li>'
        '<li>亮燈的不夠，就讓席位空著放現金，不拿紅燈的湊數。</li>'
        '<li>大盤空頭週，美股看板照樣補席（台股不補）。</li>'
        '<li>被 Supertrend 翻空賣掉的名字，同一週不會補回；下一週起若仍亮燈、在池內，可以重新入席，當作新買進。</li></ul>'))
    size = _fold("3 每檔抱多少", (
        f'<p>倉位係數 1.0 代表這一席放滿。每席占看板資金的 1/{n}，空席是現金。</p>'
        + _table(["持股狀態", "倉位"], [
            ["已切換 Supertrend", "固定 1.0，不看燈號"],
            ["未切換，時機燈綠 / 黃", "1.0"],
            ["未切換，時機燈橘 / 黃（資料缺）", "0.5"],
            ["未切換，時機燈紅 / 不合格", "0"],
            ["未切換，大盤多頭，時機燈轉紅（離新高太遠或跌破 200 日線）", "續抱，沿用最近一次非紅燈的倉位"],
            [f"未切換，估值轉紅（{vcut} 起）", "繼續坐席但不加碼：取「照燈號算出的倉位」與「估值轉紅前最後一週的倉位」較小者"],
        ])
        + f'<p>{_lamp_defs()}</p>'))
    switch = _fold("5 什麼時候切換成 Supertrend", (
        '<p>每週五收盤，用還原權息的週 K 判斷一次。任一條成立就切換，切換後不回頭，資料抓不到也不退回舊規則。</p>'
        f'<ul><li>盤整突破：這週收盤高於之前所有週的收盤，而且距上一次創新高至少 {seat_st.GAP_WEEKS} 週。剛上市沒有上一次新高的不算。從進場那一週（含）起算。</li>'
        f'<li>停損線高過買進價：這檔週線 Supertrend（{seat_st.N_ATR} 週平均波動幅度、倍數 {_g(seat_st.FACT)}，畫在價格下方的追蹤停損線）為多方，'
        '且停損線高於買進價。只從進場之後的週起算。</li></ul>'
        f'<p>買進價＝進席日（帳本快照日）的還原收盤。{cut} 第一次判斷時，現任持股用帳本裡連續在席的第一個快照日當買進日回推。</p>'))
    cadence = _fold("6 每天做什麼、每週六做什麼", (
        '<p>每天（週二到週六，台北 09:00）：重算資格、池和排序，更新時機燈和倉位。席位名單沿用上週六的結果。</p>'
        '<p>每週六（台北）依週五收盤：</p><ol>'
        '<li>判斷哪些現任持股切換成 Supertrend。</li><li>判斷大盤多空。</li>'
        '<li>現任持股逐檔過一遍：已切換看週線 Supertrend 與基本面，未切換看時機燈與資格。</li>'
        '<li>有空席就補。</li><li>記下新規則名單與舊規則對照名單的週淨值。</li></ol>'
        '<p>美股看板在台北 11:00 的週排程跑；台股席位和精選榜在 09:00 的每日排程裡、週六那一班跑。</p>'))
    back = _fold("7 退回條件與回顧日", _table(["規則", "退回條件", "回顧日"], [
        [f"盤整突破或停損線高過買進價就切換 Supertrend", "新規則實際名單的報酬落後舊規則對照線，而且最大跌幅比對照線深，兩者同時成立就改回舊規則；"
         "中途不因落後而改。美股看板與台股席位各自判斷", seat_st.REVIEW_DATE],
        ["美股大盤空頭才看紅燈", "與「紅燈就賣」的反事實比較，結果交持有人決定", "2027-10-21"],
        ["池內不設上修 5% 門檻", "與保留門檻的假想名單比較，結果交持有人決定", "2027-10-21"],
        ["排序改 PEG 由低到高、現任抱著", "Koyfin 改寫檢查判定「會改寫舊預估」，排序退回上修；上線後 13 週內平均每週換掉超過 1 席，提交持有人複審",
         "約 2027-01-29（13 週）；改寫檢查不定期"],
        [f"估值偏貴的現任繼續坐席但不加碼（{vcut} 起）", "待持有人訂", "2027-03 估值閘兩季回顧時一起看"],
    ]))
    hist = _fold("8 版本史",
                 '<p>回測欄的意思：「通過」＝事前登記的判準通過；「未通過，持有人裁量」＝登記結論不成立或沒登記，持有人知情後採用。</p>'
                 + _versions(US_VERSIONS))
    return ('<section class="rc-card" id="' + CARD_ID + '">' + _CSS
            + '<h3 class="bw-sec">席位規則（美股看板）</h3>' + top + admit + fill + size + switch + cadence + back + hist
            + '<div class="bw-note-line">這是研究名單，不是帳戶持倉。台股席位與精選榜的規則見各自頁面上的規則卡。</div></section>')


def tw_card_html(market_html: str = "") -> str:
    cut = seat_st.CUTOVER_DATE
    vcut = seat_valhold.CUTOVER_DATE
    sell = _table(
        ["持股狀態", "週線 Supertrend 翻空", "距新高跌超過 10%", "跌破自己的 200 日線", "跌破 52 週線", "估值偏貴", "基本面不合格"],
        [["已切換 Supertrend", "賣", "不賣", "不賣", "不賣", "不賣", "賣"],
         ["未切換，大盤多頭", "不適用", "不賣（續抱）", "賣", "賣", f"不賣，不加碼（{vcut} 起）", "賣"],
         ["未切換，大盤空頭", "不適用", "賣", "賣", "賣", f"不賣，不加碼（{vcut} 起）", "賣"]],
        cls="rc-sell")
    body = (
        f'<div class="bw-note-line"><b>一句話</b>：台股席位用美股看板的同一套規則（{cut} 起：持股盤整突破或停損線高過買進價就改看週線 Supertrend，'
        '之後只在翻空或基本面不合格時賣；其餘照時機燈與大盤多空）。下面只列和美股不同的地方，完整規則見'
        '<a href="/cockpit/#seats-arena">主控台席位排序分頁的「席位規則」</a>。</div>'
        + sell
        + '<div class="bw-note-line">大盤＝加權報酬指數對 200 日線。資料缺或早於決策日超過 '
          f'{seat_tm.MKT_STALE_DAYS} 天，賣法照空頭，但照常補席。基本面不合格的內容同美股，品質條件改看營業現金流（見下）。</div>'
        + market_html
        + _fold("和美股看板不同的地方", (
            '<ul><li>池：台股 Koyfin 池（市值 10 億美元以上，不含金融保險與興櫃）。席位不另設 200 億美元門檻。融券資料沒有，這一項等於不設。</li>'
            f'<li>品質：ROIC {_g(grp.Q_ROIC_MIN)}% 以上且營業現金流利潤率 {_g(grp.Q_FCF_MIN)}% 以上；或 ROIC {_g(grp.Q_ROIC_EXEMPT)}% 以上且營業現金流利潤率不為負。'
            '美股看自由現金流，台股資本支出重，看營業現金流。</li>'
            '<li>排序：財報後上修由高到低，同值比隱含成長、盈餘殖利率。沒有改成 PEG 低先。</li>'
            '<li>賣法，未切換、大盤多頭：只因離新高超過 10% 而轉紅、仍在池內的續抱；跌破自己 200 日線就賣（美股連這項也續抱）。其餘同美股。</li>'
            '<li>賣法，未切換、大盤空頭：紅燈就賣，而且週六不補新席，空席放現金。現任只在出池或轉紅時離席，不會被新名字換掉。'
            '大盤回到多頭的下一個週六照常補席。</li>'
            '<li>已切換的持股、估值偏貴現任續抱不加碼、切換條件、倉位：同美股。</li></ul>'), open_=False)
        + _fold("退回條件與回顧日", (
            f'<p>折衷組：{seat_st.REVIEW_DATE}，台股自行判斷（條件同美股）。上修門檻與大盤例外：2027-10-21。'
            '估值偏貴現任續抱不加碼：退回條件待持有人訂，2027-03 估值閘兩季回顧時一起看。</p>'))
        + _fold("版本史", _versions(TW_VERSIONS)))
    return ('<section class="rc-card" id="' + CARD_ID + '">' + _CSS + '<h3 class="bw-sec">席位規則（台股席位）</h3>' + body + '</section>')


def picks_card_html() -> str:
    """精選榜規則卡（靜態頁的 <details class="fold"> 樣式）。"""
    cap_lo = _g(1e9 / 1e8)
    cap_hi = _g(grp.MKTCAP_MIN / 1e8)
    body = (
        f'<p class="transparency"><b>一句話</b>：精選榜用美股看板同一套進場規則，跑在市值 {cap_lo} 億到 {cap_hi} 億美元的中小型股，'
        '設 10 席，每週六（台北）依週五收盤重選。賣法沒有改：時機燈轉紅就賣，或出池就賣。沒有 Supertrend，也沒有大盤多頭續抱。</p>'
        '<ul class="transparency">'
        f'<li>資格：同美股看板（品質、三年成長 {_g(grp.G_MIN_CAGR)}%、站上 52 週線、上修否決、體質／衰退／DD 否決、融券 {_g(grp.SI_CORE_EXCLUDE_PCT)}%、估值），'
        '市值改為 10 億到 200 億美元。另加持有人手動剔除名單，優先於所有規則。</li>'
        '<li>排序：財報後上修由高到低，缺值排最後；不用 PEG。</li>'
        '<li>補席：現任抱著，不被排名更高的新名字換掉；空席從池內亮燈（綠／黃／橘）的名字依排序補，亮燈不足就空席。</li>'
        '<li>出池包括：資格不成立、估值偏貴、市值離開 10 億到 200 億美元的帶子（長大超過 200 億也算出池）、被手動剔除。'
        '估值偏貴的現任不適用美股看板的續抱例外，仍然出池。</li>'
        '<li>倉位：綠 1.0、黃 1.0、橘 0.5，紅與不合格 0；資料缺的黃燈 0.5。空席放現金。</li>'
        '<li>回顧日：2027-10-21，與 IJH（S&amp;P 中型股）比較；連續 26 週平均在席不到 3 席，提早回顧。</li></ul>'
        '<p class="transparency">版本史</p>' + _versions(PICKS_VERSIONS))
    return ('<details class="fold" id="seat-rules"><summary>席位規則（精選榜）</summary>' + body + '</details>')


def refresh_picks_embed(path) -> bool:
    """把 docs/picks/_embed.html 標記之間的規則卡換成最新產出。回傳是否有改檔。找不到標記就不動。"""
    p = Path(path)
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError:
        return False
    a, b = PICKS_MARK
    if a not in txt or b not in txt:
        return False
    new = re.sub(re.escape(a) + r".*?" + re.escape(b), lambda m: a + picks_card_html() + b, txt, count=1, flags=re.S)
    if new == txt:
        return False
    p.write_text(new, encoding="utf-8")
    return True
