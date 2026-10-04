import json, os
F=json.load(open('frags_f.json'))
TW=json.load(open('frags_tw.json')) if os.path.exists('frags_tw.json') else None
css=open('v2_css.txt').read(); head=open('v2_head.txt').read().replace('<title>追漲四問</title>','<title>追漲四問續篇</title>'); script=open('v2_script.txt').read()
extra='''<style>
td .t{display:block;font-size:.68rem;color:var(--muted);line-height:1.2}
.angle{display:grid;gap:12px;padding-top:22px;border-top:1px solid var(--rule)}
.angle h3{font-size:1.02rem}
.oneline{font-family:var(--f-display);font-size:1.18rem;line-height:1.6;font-weight:600}
.effect{display:grid;grid-template-columns:max-content 1fr;gap:10px 14px;align-items:baseline;background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:14px 16px}
.effect p{font-size:.95rem}
.chip{display:inline-block;font-size:.76rem;font-weight:700;letter-spacing:.04em;padding:2px 9px;border-radius:999px;border:1px solid currentColor;white-space:nowrap}
.chip.fix{color:var(--accent)} .chip.up{color:var(--neg)} .chip.down{color:var(--muted)} .chip.new{color:var(--ink-2)}
.ans .chip{justify-self:start}
.pos{border:1px solid var(--rule);border-radius:8px;background:var(--surface);overflow-x:auto}
.pos table{min-width:560px}
.meter{position:relative;height:8px;background:var(--grid);border-radius:4px;min-width:120px}
.meter i{position:absolute;left:0;top:0;bottom:0;border-radius:4px;background:var(--s2)}
.meter b{position:absolute;top:-3px;width:2px;height:14px;background:var(--ink)}
.pos td.m{width:40%}
</style>'''
def sec(id_,num,q,one,how,body,chip,chiptext,effect):
    return f'''<section class="q" id="{id_}">
  <header><p class="eyebrow">追問 {num}</p><h2>{q}</h2></header>
  <p class="oneline">{one}</p>
  <p class="how">{how}</p>
  {body}
  <div class="effect"><span class="chip {chip}">{chiptext}</span><p>{effect}</p></div>
</section>'''
def meter(p): return f'<div class="meter" aria-hidden="true"><i style="width:{p:.0f}%"></i></div>'
posrows=[('近 3 年報酬（年化 20.9%）',87,'2026-08'),('CAPE（40.6）',99,'2026-09'),('超額 CAPE 殖利率（1.0%，越低越貴）',81,'2026-09'),('CAPE 相對近 30 年中位數（1.47 倍）',83,'2026-09'),
        ('實質盈餘相對 10 年平均（1.58 倍）',98,'2026-06'),('漲勢集中度（市值加權領先等權 10.0 個百分點）',94,'2026-08'),('科技業相對估值（淨值市價比 0.51，越低越貴）',74,'2026')]
pos_html='<div class="pos"><table><thead><tr><th scope="col" style="text-align:left">指標（現值）</th><th scope="col">歷史百分位</th><th scope="col" style="text-align:left">位置</th><th scope="col">資料月份</th></tr></thead><tbody>'+''.join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td class='m'>{meter(b)}</td><td>{c}</td></tr>" for a,b,c in posrows)+'<tr><th scope="row">科技業佔美股市值（42%）</th><td>最高</td><td class="m">'+meter(100)+'</td><td>2025 年底</td></tr></tbody></table></div><p class="note">百分位＝歷史上比現在「更便宜／更低」的時間比例，越接近 100 代表越極端。</p>'

tw_card=TW['card'] if TW else '<p class="ev">台股資料整理中。</p>'
tw_sec=TW['section'] if TW else ''

html=head+css+extra+r'''
<div class="page">
<header>
  <p class="eyebrow">歷史回測筆記 · 續篇 · 資料截至 2026 年 9 月</p>
  <h1>七個追問</h1>
  <p class="lede">第一輪回測（<a href="https://claude.ai/artifact/BB2ajiy5edyV4dHsAHnpQt">追漲四問</a>）留下七個沒回答的問題。這一篇逐一回測，並標出每個答案讓原本的結論變強、變弱，還是需要修正。</p>
  <nav class="toc" aria-label="章節"><a href="#pos">現在在哪裡</a><a href="#f1">1 漲幅來源</a><a href="#f2">2 結構性估值</a><a href="#f3">3 漲勢寬度</a><a href="#f4">4 領先類股</a><a href="#f5">5 太早的代價</a><a href="#f6">6 樣本外檢驗</a><a href="#f7">7 台股</a><a href="#update">更新後的結論</a></nav>
</header>

<section class="big" id="pos" style="margin-top:30px;display:grid;gap:12px">
  <h2 style="font-size:1.3rem">現在在歷史中的位置</h2>
  <p>把七個追問用到的指標放在一起看。大多數指標都在歷史的前 20%，但程度不一：CAPE 和盈餘位置最極端，經利率或時代調整後的估值較溫和。</p>
''' + pos_html + r'''
</section>

<div class="answers">
  <article class="ans"><span class="qn">追問 1</span><p class="qq">近三年的漲幅是盈餘撐起來的，還是本益比？</p><span class="chip fix">修正</span>
    <p class="verdict">主要是盈餘；但盈餘本身在歷史高檔。</p><p class="ev">股價每年 +19.7%，其中盈餘 +17.7%、本益比 +1.7%。實質盈餘是 10 年平均的 1.58 倍（第 98 百分位）。</p><a href="#f1">看細節</a></article>
  <article class="ans"><span class="qn">追問 2</span><p class="qq">高 CAPE 有多少是結構性的？</p><span class="chip fix">修正</span>
    <p class="verdict">一部分。調整利率後從第 99 降到第 81 百分位，仍在最貴的 20%。</p><p class="ev">這一組歷史上之後 10 年，股票贏公債的機率只有 57%。</p><a href="#f2">看細節</a></article>
  <article class="ans"><span class="qn">追問 3</span><p class="qq">這次熱行情是窄還是寬？</p><span class="chip up">強化</span>
    <p class="verdict">很窄，而窄的熱行情之後最差。</p><p class="ev">窄的熱行情之後 5 年年化 2.1%。現在市值加權每年領先等權 10 個百分點，第 94 百分位。</p><a href="#f3">看細節</a></article>
  <article class="ans"><span class="qn">追問 4</span><p class="qq">領先多年的類股何時結束？</p><span class="chip new">新發現</span>
    <p class="verdict">3–5 年看，長期贏家平均會落後；估值只在短期有區辨力。</p><p class="ev">過去 10 年最強的產業，之後 5 年每年落後大盤 1.4–3.2 個百分點。科技業佔市值 42%，創新高。</p><a href="#f4">看細節</a></article>
  <article class="ans"><span class="qn">追問 5</span><p class="qq">「熱＋貴」訊號太早的代價？</p><span class="chip fix">修正</span>
    <p class="verdict">很高。通常還會再漲，而且多數時候不會給更低的買回點。</p><p class="ev">訊號後 3 年內中位數再漲 39%；8 次中只有 2 次跌到明顯低於訊號當時。</p><a href="#f5">看細節</a></article>
  <article class="ans"><span class="qn">追問 6</span><p class="qq">結果是不是事後挑出來的？</p><span class="chip down">弱化第 2 題</span>
    <p class="verdict">第 1、3 題樣本外方向成立；第 2 題的統計證據比看起來弱。</p><p class="ev">第 3 題產業動能在後半段 16 種設定全為正；第 2 題切半後 p 值 0.10 與 0.49。</p><a href="#f6">看細節</a></article>
  <article class="ans"><span class="qn">追問 7</span><p class="qq">台股適用嗎？</p>''' + tw_card + r'''<a href="#f7">看細節</a></article>
  <article class="ans"><span class="qn">總結</span><p class="qq">七個追問改變了什麼？</p>
    <p class="verdict">第 1、3、4 題維持；第 2 題降級；「現在」的描述更細。</p><p class="ev">現在的熱行情是盈餘推動、但非常窄；估值調整後仍在最貴的 20%。</p><a href="#update">看更新後的結論</a></article>
</div>
''' + sec('f1','1','近三年的漲幅，是盈餘成長撐起來的，還是本益比被推高？',
  '主要是盈餘。這次不像 1999 年靠本益比擴張；但盈餘本身已在歷史高檔，風險從「估值擴張」換到「盈餘能否維持」。',
  '做法：用 Shiller 的 S&amp;P 500 過去 12 個月盈餘，把每段 3 年的股價變化拆成「每股盈餘成長」和「本益比變化」。也用 CAPE（以 10 年平均盈餘計算的本益比）的上升速度，把歷史上的熱行情（近 3 年報酬最熱的 20%）分成三組。',
  '<div class="angle"><h3>現在：漲幅約九成來自盈餘</h3><p>2023 年 6 月到 2026 年 6 月，S&amp;P 500 股價每年 +19.7%。其中每股盈餘每年 +17.7%，本益比只從 24.0 倍升到 25.2 倍（每年 +1.7%），約九成漲幅來自盈餘成長。</p></div>'
  + '<div class="angle"><h3>歷史：CAPE 漲得越快的熱行情，之後越差</h3><p>CAPE 上升最快的三分之一（每年超過 14.5%，共 9 段，包括 1920 年代末、1997–2000）之後 5 年年化 −2.7%，只有 33% 為正，36 個月內平均最大回撤 −41%。CAPE 上升最慢的三分之一之後 5 年 12.3%，全部為正。現在 CAPE 每年上升約 10%，落在中間組（之後 5 年 8.9%，89% 為正）。用一般本益比區分也是同方向，但差距較小。</p>'
  + '<figure><figcaption><b>熱行情依 CAPE 上升速度分組，之後 5 年的年化報酬</b>橫線為全部月份的平均（9.6%）</figcaption>' + F['f1_c'] + '</figure>' + F['f1_t'] + '</div>'
  + '<div class="angle"><h3>但盈餘本身在高檔</h3><p>2026 年 6 月，實質盈餘是過去 10 年平均的 1.58 倍，歷史第 98 百分位，和 1929、2007、2021 年相近。這也是 CAPE（41 倍）遠高於一般本益比（25 倍）的原因：CAPE 用 10 年平均盈餘，等於假設盈餘會回到長期水準。歷史上盈餘超過 10 年平均 1.5 倍的 8 段時期，之後 3 年實質盈餘平均下降 33%，94% 的情況是下降。</p>' + F['f1_t2'] + '<p class="note">盈餘為 S&amp;P 公布的 GAAP 盈餘，最近幾個月含 Shiller 的估計值。8 段中有幾段（1916–17、1929–30）盈餘下降與戰爭、大蕭條有關。</p></div>',
  'fix','修正','這次的熱行情主要由盈餘推動，依歷史分組屬於中性，不是 1999 年那種估值型。需要注意的風險換了位置：盈餘已遠高於長期趨勢，它能不能維持，比估值是否繼續擴張更關鍵。'
) + sec('f2','2','現在的高 CAPE，有多少是結構性的？',
  '有一部分。用利率或時代調整後，現在從「史上第二貴」降到「歷史最貴的 20% 左右」，但仍在最貴的那一組。',
  '做法：兩種調整。超額 CAPE 殖利率（Shiller 提出）：以 CAPE 換算的盈餘殖利率，減去 10 年期實質公債殖利率，衡量股票相對公債的便宜程度。相對 CAPE：CAPE 除以前 30 年的中位數，衡量相對於當代標準有多貴。',
  '<div class="angle"><h3>調整後沒那麼極端，但仍偏貴</h3><p>CAPE 本身在第 99 百分位，只有 1999–2000 年比現在高。超額 CAPE 殖利率是 1.0%，比歷史上 81% 的時間貴；相對 CAPE 是 1.47 倍，在第 83 百分位。</p></div>'
  + '<div class="angle"><h3>三種指標的預測力相近，各有長處</h3><p>表中數值已轉成同方向，越高代表「越便宜，之後報酬越高」的關係越強。預測之後 10 年報酬時，三者相近（0.46–0.51）；1982 年以後相對 CAPE 最強（0.88）。預測「股票減公債」的超額報酬時，超額 CAPE 殖利率最好。</p>' + F['f2_t2'] + '</div>'
  + '<div class="angle"><h3>現在落在最貴的五分之一</h3><p>超額 CAPE 殖利率最低的 20%（≤1.1%）之後 10 年實質年化 4.2%，10 年內股票贏公債的機率只有 57%，其他各組是 84%–95%。這一組的成員包括 1880–90 年代（之後報酬不差）、1929、1960 年代末、1997–2002 和 2006–07。</p>' + F['f2_t'] + '</div>',
  'fix','修正','把利率和時代標準納入之後，現在的估值沒有 CAPE 單獨看起來那麼極端，「史上第二貴」的說法誇大了。但換成任何一種調整，現在仍在最貴的 20%，第一版的方向不變。'
) + sec('f3','3','這次熱行情是少數大型股帶動的嗎？窄和寬的熱行情之後有差嗎？',
  '這次非常窄，而窄的熱行情是三組中之後表現最差的一組。',
  '做法：用 Ken French 49 個產業的等權報酬與公司家數，重建「全市場等權」報酬，和市值加權大盤比較。過去 36 個月市值加權比等權多賺越多，代表漲勢越集中在大型股。2003 年以後另用 SPY 對 RSP（S&amp;P 500 等權 ETF）驗證。',
  '<div class="angle"><h3>窄的熱行情之後最差</h3><p>熱行情依寬度分三組。窄的一組（市值加權每年領先等權 3 到 17 個百分點）之後 5 年年化 2.1%，只有 55% 為正，36 個月內平均最大回撤 −34%。中間組 13.4%，寬的一組 7.6%。窄的熱行情共 6 段：1929–30、1954、1956、1985–87、1996–2000、2025–26。</p><figure><figcaption><b>熱行情依寬度分組，之後 5 年的年化報酬</b>橫線為全部月份的平均（9.6%）</figcaption>' + F['f3_c'] + '</figure>' + F['f3_t'] + '</div>'
  + '<div class="angle"><h3>現在：歷史上最窄的幾次之一</h3><p>到 2026 年 8 月的 36 個月，市值加權年化 20.9%，等權只有 10.9%，相差 10.0 個百分點，第 94 百分位。最窄的紀錄是 2024 年 6 月（相差 18.0 個百分點），超過 1999 年（16.5）。SPY 對 RSP 也一樣：近 3 年 22.8% 對 15.5%，相差 7.2 個百分點，是 2006 年以來第 96 百分位。</p></div>',
  'up','強化','窄的熱行情是三組中之後最差的一組，而現在屬於這一組，這加強了第一版對現況偏弱的描述。要注意等權報酬包含大量小型股，寬度的量法會受小型股表現影響；樣本也只有 6 段。'
) + sec('f4','4','領先多年的類股（現在是科技）什麼時候會結束？相對估值能提前看出來嗎？',
  '以 3–5 年來看，長期贏家平均會落後大盤；相對估值只在「隔年」有區辨力。科技業目前相對偏貴、權重創紀錄，但估值沒有 1968 或 2000 年那麼極端。',
  '做法：Ken French 的產業資料提供每個產業的淨值市價比（B/M，越低代表越貴）。用產業 B/M 除以全市場 B/M 得到相對估值，看「長期領先、而且相對很貴」的產業之後表現。也單獨檢查 10 大產業中的科技業。',
  '<div class="angle"><h3>長期贏家平均會回吐，估值幫助有限</h3><p>49 細產業中，過去 10 年相對報酬前 20% 的產業，之後 5 年每年落後大盤 1.4 到 3.2 個百分點，只有 36%–45% 贏大盤。最貴和最便宜的長期贏家，之後的表現差不多。</p>' + F['f4_t3'] + '</div>'
  + '<div class="angle"><h3>短期例外：最貴的近 5 年冠軍，隔年最差</h3><p>每年的「近 5 年冠軍產業」依當時相對估值分三組。最貴的一組隔年平均落後大盤 4.0（10 大產業）與 7.8（49 細產業）個百分點，是三組中最差的。但以 3 年來看，三組都大多落後大盤。</p>' + F['f4_t2'] + '</div>'
  + '<div class="angle"><h3>科技業本身</h3><p>科技業相對 B/M 最貴的 25% 年份（≤0.50），之後 3 年每年落後大盤 2.5 個百分點；最便宜的 25% 之後每年領先 2.6。2026 年科技業的相對 B/M 是 0.51，剛好在最貴 25% 的門檻上，但沒有 1968（0.37）和 2000 年（0.39）那麼極端。科技業佔美股市值 42%（2025 年底），是 1926 年以來最高，1999 年是 27%。</p>' + F['f4_t1'] + '<p class="note">10 大產業的「科技」包含電腦、軟體、半導體與電子設備；淨值市價比對軟體等輕資產產業會系統性偏低。</p></div>',
  'new','新發現','第一版發現現代的長期領先者延續得比過去久（以隔年來看）。這裡補上另一面：以 3–5 年來看，長期贏家平均會落後，這在歷史上相當一致。這份資料無法告訴你科技的長週期何時結束，只能說它目前偏貴、權重前所未見。'
) + sec('f5','5','「熱＋貴」的訊號出現後，太早行動的代價有多大？',
  '很高。訊號出現後，市場通常還會再漲一段，而且多數時候不會跌到比訊號當時更低的位置。',
  '做法：定義兩種訊號，每次第一次出現（與前一次相隔超過 12 個月）記一筆。S1：近 3 年年化 ≥20% 且 CAPE ≥30（嚴格版）。S2：近 3 年報酬在歷史最熱的 20%，且 CAPE 高於「當時已知歷史」的第 80 百分位（不使用未來資料）。看訊號後 5 年的走勢，並和改買公債比較。',
  '<div class="angle"><h3>S2：9 次訊號，多數太早</h3><p>8 次已有 5 年結果。訊號後 3 年內，股市的中位數還會再漲 39%，到高點的中位數是第 35 個月。5 年後股票贏公債 6 次、輸 2 次（1928、2005）。只有這 2 次跌到明顯低於訊號當時的位置（−77%、−35%）；其他 6 次最多只跌到訊號水準下方 0–16%。</p>' + F['f5_t2'] + '</div>'
  + '<div class="angle"><h3>S1：只有 4 次，結果兩極</h3><p>1929 年隔月就開始崩跌。1997 年之後還漲了 81%，33 個月後才見頂，5 年後仍輸公債。2021 年之後一年 −17.5%，三年後 +24%。2025 年 9 月的訊號目前仍在進行中，11 個月後的高點比訊號時高 15.5%。</p>' + F['f5_t1'] + '</div>',
  'fix','修正','「熱＋貴」之後長期平均偏弱是事實，但拿來當行動訊號的成本很高：通常太早，而且多數時候不會給更低的價格買回來。這支持第一版「下修預期、不擇時」的用法。'
) + sec('f6','6','這些規則是不是事後挑出來的？用樣本外檢驗重新確認',
  '第 3 題（產業動能）最穩健；第 1 題方向成立但後半段的幅度小很多；第 2 題的統計證據比第一版呈現的弱。',
  '做法：把資料切成兩半。在前半段找出效果最好的規則，原封不動拿到後半段驗證，也反過來做。另外把報酬順序完全打亂、重抽 1,000 次，計算「沒有任何預測力時」重疊窗口自然會產生多大的差距或相關係數，得到 p 值（越小越不像巧合）。',
  '<div class="angle"><h3>第 1 題：方向成立，幅度不穩</h3><p>前半段（1871–1950）找到的最佳規則是「過去 60 個月年化 ≥18.1%」，之後 5 年報酬比其他時候低 13.4 個百分點；拿到後半段只剩 3.9，p 值 0.18，單獨看後半段不顯著。12 種規則中有 9 種在後半段同方向。反過來做，12 種全部同方向，p 值 0.003。全期間的主結果（36 個月年化 &gt;20%）差距 6.4 個百分點，隨機情況下 95% 的時候不超過 3.8，p 值小於 0.001。</p>' + F['f6_t1'] + '</div>'
  + '<div class="angle"><h3>第 2 題：最弱的一環</h3><p>即使報酬完全隨機，因為 10–20 年的窗口在 150 年裡只有少數幾段，「之前」和「之後」的相關係數平均也會是 −0.08 到 −0.14，有 5% 的機率低到 −0.41 到 −0.51。全期間的實際值是 −0.34 到 −0.60，p 值 0.01 到 0.09，只算邊緣顯著；切成兩半後，p 值是 0.10 和 0.49。</p>' + F['f6_t2'] + '</div>'
  + f'<div class="angle"><h3>第 3 題：產業動能最穩健</h3><p>1927–1975 年選出的最佳設定（49 細產業、看過去 12 個月、持有 1 個月），在 1976–2026 年仍每年多 {F["f6_q3"]["best_res"]["test"]*100:.1f} 個百分點（t 值 {F["f6_q3"]["best_res"]["test_t"]:.1f}），16 種設定在後半段全部為正。打亂時間順序後，隨機情況幾乎不會出現這個結果（p 值小於 0.01）。第一版提到 2010 年後效果減弱，這個減弱發生在後半段的末端。</p></div>'
  + '<div class="angle"><h3>第 4 題：已用兩套獨立資料驗證</h3><p>EDHEC 和 Credit Suisse 兩套避險基金指數挑出的冠軍只有 14／24 年相同，但兩套的結論一致：追逐都落後平均。</p></div>',
  'down','弱化第 2 題','第 2 題的方向在美國前後兩段、16 國中的 15 國都一致，但統計可信度比第一版呈現的低。比較準確的說法是：「冷起點較好」的證據一致但不強，幅度不要當成精確數字。第 1、3 題的結論維持。'
) + tw_sec + r'''
<section class="synth" id="update">
  <h2>更新後的結論</h2>
  <ol>
    <li><b>第 1 題維持，但要加兩個條件。</b>連續多年高報酬之後，未來幾年平均偏低，這在樣本外同方向、全期間顯著。差異主要出現在「CAPE 快速上升」和「漲勢很窄」的熱行情。現在的熱行情是盈餘推動、但非常窄。</li>
    <li><b>第 2 題降級。</b>冷起點較好的方向一致（美國兩段、16 國中 15 國），但統計上只算邊緣顯著。</li>
    <li><b>第 3 題維持，而且產業動能是七個追問中最穩健的發現。</b>每年換「去年冠軍大類股」仍然無效；以 3–5 年看，長期贏家平均會落後。</li>
    <li><b>第 4 題不變。</b></li>
    <li><b>關於現在：</b>估值、盈餘位置、漲勢集中度都在歷史前 20%，經利率或時代調整後較溫和。歷史上，這類訊號出現後通常還有一段漲幅，而且多數時候不會給更低的買回點。這些是描述歷史基準的結果，不是擇時訊號。</li>
  </ol>
</section>

<section class="method" id="method">
  <h2>資料與方法</h2>
  <ul>
    <li><b>美股與估值：</b>Shiller 最新版資料（至 2026 年 9 月；盈餘至 2026 年 6 月，近月含估計值）；CRSP 美國全市場報酬（Ken French 資料庫）。超額 CAPE 殖利率直接採用 Shiller 檔案中的欄位。</li>
    <li><b>寬度：</b>以 Ken French 49 產業的等權報酬，依各產業公司家數加權，重建全市場等權報酬；SPY 與 RSP 為 Yahoo Finance 含息調整價。</li>
    <li><b>產業估值：</b>Ken French 產業資料的「市值加權平均 BE/ME」，年度、6 月更新；全市場 B/M 以前一年 12 月各產業市值加權。</li>
    <li><b>樣本外與 p 值：</b>前後兩段為 1871–1950、1951–2026（產業動能為 1927–1975、1976–2026）。p 值以 1,000 次（第 2 題 500 次、第 3 題 300 次）獨立重抽或打亂時間順序計算，比一般 t 值更能反映重疊窗口的問題。</li>
    <li><b>限制：</b>熱行情、窄行情、訊號等條件的獨立段數多在 4–18 段之間，任何一組的平均值都可能被一兩段主導。所有回測未計交易成本與稅。</li>
  </ul>
</section>
<footer>由 Claude 依公開資料回測整理，2026-10-04。內容是歷史基準的描述，不是投資建議。</footer>
</div>
''' + script
open('followups.html','w').write(html)
print(len(html), 'TW' if TW else 'noTW')
