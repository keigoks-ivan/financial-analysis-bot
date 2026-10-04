import json
F=json.load(open('frags_v2.json'))
css=open('v2_css.txt').read(); head=open('v2_head.txt').read(); script=open('v2_script.txt').read()
extra_css='''<style>
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:baseline;gap:5px;padding:3px 9px;border:1px solid var(--rule);border-radius:999px;font-size:.8rem;background:var(--surface);color:var(--ink-2)}
.chip b{font-family:var(--f-data);font-weight:500;color:var(--ink)}
td .t{display:block;font-size:.68rem;color:var(--muted);line-height:1.2}
.angle{display:grid;gap:12px;padding-top:22px;border-top:1px solid var(--rule)}
.angle h3{font-size:1.05rem;display:flex;gap:10px;align-items:baseline}
.angle h3 .tag{font-family:var(--f-data);font-size:.74rem;color:var(--muted);font-weight:400;letter-spacing:.05em;flex:none}
.angle p{font-size:.97rem}
.oneline{font-family:var(--f-display);font-size:1.22rem;line-height:1.6;font-weight:600}
.angles-index{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.85rem;color:var(--muted)}
.angles-index span b{font-family:var(--f-data);font-weight:500;color:var(--ink-2);margin-right:4px}
.vs{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:18px 18px 8px;display:grid;gap:4px}
.vs h3{font-size:1rem;margin-bottom:6px}
.vs dl{margin:0;display:grid;grid-template-columns:minmax(6.5em,max-content) 1fr;gap:0}
.vs dt,.vs dd{padding:10px 0;border-top:1px solid var(--grid);margin:0}
.vs dt{font-size:.82rem;color:var(--muted);padding-right:14px}
.vs dd{font-size:.95rem}
.era{overflow-x:auto;border:1px solid var(--rule);border-radius:6px;background:var(--surface)}
.big{margin-top:30px;display:grid;gap:12px}
.big h2{font-size:1.3rem}
.synth table td{white-space:normal;text-align:left;font-family:var(--f-body);font-size:.86rem;min-width:11em;vertical-align:top}
.synth table{min-width:640px}
@media (max-width:520px){.vs dl{grid-template-columns:1fr}.vs dt{padding-bottom:0;border-top:1px solid var(--grid)}.vs dd{border-top:0;padding-top:4px}}
</style>'''
def angle(tag,title,body): return f'<div class="angle"><h3><span class="tag">{tag}</span>{title}</h3>{body}</div>'
def fig(title,sub,chart,legend=''):
    return f'<figure><figcaption><b>{title}</b>{sub}</figcaption>{legend}{chart}</figure>'
def vs(rows):
    return '<div class="vs"><h3>現在 vs 長期平均</h3><dl>'+''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a,b in rows)+'</dl></div>'

html=head+css+extra_css+r'''
<div class="page">
<header>
  <p class="eyebrow">歷史回測筆記 · 第二版 · 資料截至 2026 年 9 月</p>
  <h1>追漲四問</h1>
  <p class="lede">追逐過去的高報酬有沒有用？四個問題各自從 6 到 9 個面向重新回測，並把「現代時期」和長期平均分開看。資料涵蓋 1871 年起的美股、1926 年起的美國產業組合、18 國長期報酬、標普類股 ETF，以及兩套避險基金策略指數。</p>
  <p class="note">續篇：<a href="https://claude.ai/artifact/36p9Uiz9WRhATeypLy2QhN">七個追問</a>（漲幅來源、結構性估值、漲勢寬度、領先類股、太早的代價、樣本外檢驗、台股）。</p>
  <nav class="toc" aria-label="章節"><a href="#now">現在有什麼不同</a><a href="#q1">1 高報酬之後</a><a href="#q2">2 長期投資的起點</a><a href="#q3">3 追最強類股</a><a href="#q4">4 追最強避險策略</a><a href="#synth">總表</a><a href="#method">資料與方法</a></nav>
</header>

<div class="now" aria-label="目前的位置">
  <div class="now-grid">
    <div><b>+26.2%</b><span>2023 年</span></div>
    <div><b>+24.9%</b><span>2024 年</span></div>
    <div><b>+17.7%</b><span>2025 年</span></div>
    <div><b>+12.7%</b><span>2026 年 1–9 月</span></div>
    <div><b>40.6</b><span>CAPE（2026-09）</span></div>
    <div><b>4.75%</b><span>10 年期美債</span></div>
  </div>
  <small>年度與今年報酬為 SPY 含息報酬（至 2026-09-30）；CAPE 與殖利率取自 Shiller 資料。近 3 年年化約 21%，落在 1871 年以來的第 87 百分位；CAPE 落在第 99 百分位，只有 1999–2000 年比現在高。</small>
</div>

<section class="big" id="now">
  <h2>現在跟長期平均差在哪</h2>
  <p>你的直覺是對的：現代的美股和長期平均差很多。最大的差別是估值的基準。2000 年以後 CAPE 的中位數是 26.9，1999 年以前只有 15.2。2009 年後實質年化報酬 12.1%，只有 1982–1999 年的大多頭能相比。所以下面每一題都分時期檢查，看「現代」的結果是否和長期平均一致。</p>
  <div class="era"><table>
    <thead><tr><th scope="col" style="text-align:left">時期</th><th scope="col">名目年化</th><th scope="col">實質年化</th><th scope="col">年波動</th><th scope="col">年通膨</th><th scope="col">CAPE 中位數</th></tr></thead>
    <tbody>
      <tr><th scope="row">1871–1913 金本位時代</th><td>6.6%</td><td>7.1%</td><td>11.1%</td><td>−0.5%</td><td>16.5</td></tr>
      <tr><th scope="row">1914–1945 戰爭與大蕭條</th><td>7.9%</td><td>5.9%</td><td>23.4%</td><td>1.9%</td><td>11.5</td></tr>
      <tr><th scope="row">1946–1981 戰後到高通膨</th><td>10.2%</td><td>5.3%</td><td>14.2%</td><td>4.7%</td><td>15.1</td></tr>
      <tr><th scope="row">1982–1999 利率下行大多頭</th><td>17.9%</td><td>14.1%</td><td>15.1%</td><td>3.3%</td><td>17.8</td></tr>
      <tr><th scope="row">2000–2026 現代</th><td>8.5%</td><td>5.8%</td><td>15.7%</td><td>2.6%</td><td>26.9</td></tr>
      <tr><th scope="row">2009–2026 金融海嘯後</th><td>15.0%</td><td>12.1%</td><td>15.4%</td><td>2.7%</td><td>28.4</td></tr>
    </tbody></table></div>
</section>

<div class="answers">
  <article class="ans"><span class="qn">Q1</span><p class="qq">美股在最近幾年創下高報酬之後，表現如何？</p>
    <p class="verdict">只漲一年沒差；連漲多年之後平均變差、回撤變大，搭配高估值時最明顯。</p>
    <p class="ev">過去 36 個月年化 &gt;20%：之後 5 年年化 4.1%（平均 9.6%）。再加上 CAPE ≥30：之後 5 年年化 0.1%，但只有 4 段樣本。</p><a href="#q1">看 7 個面向</a></article>
  <article class="ans"><span class="qn">Q2</span><p class="qq">在長期高或低報酬之後開始投資 5–20 年，會比較好嗎？</p>
    <p class="verdict">冷起點較好，現代更明顯；定期定額也躲不掉起點效應。</p>
    <p class="ev">最熱 20% 起點，之後 20 年實質年化 4.3%，最冷 20% 是 8.8%。熱起點之後 10 年，股票只有一半機率贏公債。</p><a href="#q2">看 8 個面向</a></article>
  <article class="ans"><span class="qn">Q3</span><p class="qq">每年換到最近表現最好的標普類股，會贏大盤嗎？</p>
    <p class="verdict">每年換「去年冠軍大類股」沒有優勢；細產業、每月更新的動能長期有效，但在現代變弱。</p>
    <p class="ev">標普類股 ETF 追去年冠軍：7.5% 對 8.0%。49 細產業月度動能：1927–2026 每年 +4.8 個百分點，2010 年後降到 +2.0。</p><a href="#q3">看 9 個面向</a></article>
  <article class="ans"><span class="qn">Q4</span><p class="qq">近幾年最好的避險基金策略，隔年會贏過所有策略的平均嗎？</p>
    <p class="verdict">不會；兩套指數都落後平均，2008 年後更差。</p>
    <p class="ev">EDHEC：追去年第一名年化 −1.4%，平均 5.8%。Credit Suisse：4.9% 對 7.0%，2008 年後每年落後 3.3 個百分點。</p><a href="#q4">看 7 個面向</a></article>
</div>

<!-- ================= Q1 ================= -->
<section class="q" id="q1">
  <header><p class="eyebrow">Question 1 · 美股月資料 1871–2026</p><h2>美國股市在最近幾年創下高報酬之後，表現如何？</h2></header>
  <p class="oneline">一年的大漲沒有資訊量；三到五年的連續高報酬才有。它讓之後幾年的平均報酬變低、大跌機率變高，而且在估值偏高時最明顯。</p>
  <p class="how">做法：每個月底都是一個觀察點（1874 年起約 1,830 個），看當時「過去 12／24／36／60 個月」的報酬，再看之後 1 個月到 5 年的報酬與回撤。1926 年以前用 Shiller 的 S&amp;P 綜合指數，之後用 CRSP 美國全市場，皆為名目含息報酬。相鄰月份高度重疊，所以表中同時列出「獨立段數」（相隔超過 12 個月才算新的一段）。</p>
  <div class="angles-index"><span><b>A</b>定義</span><span><b>B</b>預測期</span><span><b>C</b>分時期</span><span><b>D</b>相對定義</span><span><b>E</b>回撤風險</span><span><b>F</b>估值交叉</span><span><b>G</b>現況類比</span></div>
  ''' + angle('面向 A','「高報酬」怎麼定義，結論差很多',
    '<p>只看過去 12 個月，即使漲超過 30%，之後 12 個月平均仍有 9.8%，和全部月份的 11.1% 差不多。把觀察窗拉長，效果就出現了：過去 36 個月年化 &gt;20% 之後 5 年年化 4.1%；過去 60 個月年化 &gt;20% 之後 5 年只有 2.5%，5 年後還在賺錢的機率只有 56%。反過來，過去 36 個月是負報酬時，之後 5 年年化 12.7%，98% 為正。</p>'
    + fig('不同定義下，之後的平均報酬','滑過長條可看中位數與上漲機率',F['q1_cA']) + F['q1_tA']) + angle('面向 B','預測期：短期延續，長期反轉',
    f'<p>把最熱的 20% 月份（過去 12 個月 ≥{F["q1_cuts"][0]*100:.1f}%，或過去 36 個月年化 ≥{F["q1_cuts"][1]*100:.1f}%）拿出來，看之後各期間比平均多或少多少（年化百分點）。過去 12 個月很熱時，接下來幾個月略好於平均（短期動能），一年後轉為落後。過去 36 個月很熱時，從 3 個月起就落後，期間越長落後越多，到 3–5 年約每年少 4 個百分點。</p>'
    + fig('最熱起點之後，各期間與平均的差距','單位：年化百分點；正值代表優於全部月份的平均',F['q1_cB'])) + angle('面向 C','分時期：均值回歸不是每個時代都一樣',
    '<p>「熱」用同一個門檻（過去 36 個月年化 ≥18.1%）。1914–1945 和 1982–1999 兩段反轉最強，熱行情之後 5 年年化只有 −3.0% 和 6.9%。1946–1981 正好相反，熱行情之後 5 年年化 13.4%，比平時還好。現代（2000–2026）熱行情後的下一年平均只有 0.5%，平時是 10.2%；但 5 年報酬 7.7%，只比平時略低。2009 年後也一樣：下一年明顯變差（3.1% 對 15.7%），5 年差距不大（12.1% 對 13.9%）。</p>'
    + F['q1_tC'] + '<p class="note">每個時期的熱行情只有 3–7 段，時期內的比較只能看方向。</p>') + angle('面向 D','用「相對於近 30 年」重新定義熱',
    '<p>現代的報酬和估值基準都比過去高，固定門檻可能不公平。這裡改用相對定義：過去 36 個月報酬落在「前 30 年」分布的前 20%，才算熱。結果和固定門檻一致：全期間熱行情之後 5 年年化 6.2%，其餘 11.1%。2000–2026 熱行情之後的下一年平均 −2.5%，其餘月份 11.6%。2026 年 8 月正好落在這個相對門檻之上（第 87 百分位）。</p>'
    + F['q1_tD']) + angle('面向 E','回撤風險：平均值之外更重要的事',
    '<p>過去 36 個月年化 &gt;20% 之後，12 個月內從起點跌 20% 以上的機率是 22%，平時是 14%；過去 60 個月年化 &gt;20% 時升到 37%。之後 36 個月內的平均最大回撤從 −19.9% 擴大到 −27.4%～−32.8%。高報酬之後最明顯的變化，是結果分布的左尾變厚。</p>'
    + fig('之後 12 個月內跌 20% 以上的機率','橫線為全部月份的機率（14%）',F['q1_cE']) + F['q1_tE']) + angle('面向 F','估值交叉：熱行情加上高估值才是關鍵',
    '<p>把熱行情依當時的 CAPE 分開，差異很大。熱行情發生在 CAPE &lt;20 時，之後 5 年年化 8.2%，與平時相近。CAPE 20–30 時只剩 2.5%，CAPE ≥30 時是 0.1%，5 年後為正的機率只有 40%。同樣是 CAPE ≥30，如果前面沒有熱行情，之後 5 年仍有 8.9%。不過 CAPE ≥30 的熱行情只有 4 段，其中有 5 年結果的只有 1929 和 1997–2000 兩段。</p>'
    + F['q1_tF']) + angle('面向 G','現況類比：同時「近 3 年年化 ≥20%」且「CAPE ≥30」',
    '<p>歷史上同時符合的只有三段，現在是第四段。1929 年之後是大蕭條；1997–2000 年之後 5 年年化約 −1%；2021–22 年之後 12 個月約 −15%，但之後 3 年年化回到 +9.5%。三段都比全期平均差，但三段的路徑完全不同，不能拿來推算時間點。</p>'
    + F['q1_tG'] + '<details><summary>年度資料：前 3 年年化 &gt;20% 的每一個年底</summary><div class="tbl"><table><thead><tr><th scope="col" style="text-align:left">年底</th><th scope="col">前 3 年年化</th><th scope="col">下一年</th><th scope="col">之後 3 年年化</th><th scope="col">之後 5 年年化</th></tr></thead><tbody>' + F['q1_rows_ep'] + '</tbody></table></div></details>') + vs([
    ('長期平均','連續 3–5 年高報酬之後，之後 1–5 年的平均報酬約低 3–5 個百分點，大跌機率較高。'),
    ('現代時期','2000 年後熱行情的下一年明顯更差（0.5% 對 10.2%），但 5 年報酬恢復得比過去快；2009 年後熱行情的 5 年報酬仍有 12.1%。'),
    ('對現在的意義','現在同時是熱行情（第 87 百分位）和極高估值（CAPE 第 99 百分位）。歷史上這個組合的結果都偏弱，但只有 3 段可比，無法估計機率。')]) + r'''
</section>

<!-- ================= Q2 ================= -->
<section class="q" id="q2">
  <header><p class="eyebrow">Question 2 · 美股實質報酬 1871–2026 ＋ 18 國 1870–2020</p><h2>在長期高或低報酬之後開始長期投資（5–20 年），績效會比較好嗎？</h2></header>
  <p class="oneline">會。冷起點長期明顯較好，投資期間越長越明顯。現代的效果比過去更強，定期定額也躲不掉；但持有 20 年，美國歷史上沒有實質虧損過。</p>
  <p class="how">做法：每個月底都是一個起點，用「起點之前 10 年的實質年化報酬」分成五組，看之後 5、10、15、20 年的實質年化報酬（已扣通膨）。另外比較定期定額、公債與 16 個國家的資料。</p>
  <div class="angles-index"><span><b>A</b>回看期×投資期</span><span><b>B</b>五組分布</span><span><b>C</b>分時期</span><span><b>D</b>定期定額</span><span><b>E</b>相對公債</span><span><b>F</b>估值</span><span><b>G</b>16 國</span><span><b>H</b>現況類比</span></div>
  ''' + angle('面向 A','回看期 × 投資期：都越長越明顯',
    '<p>16 個組合全部是負相關：之前漲越多，之後越少。回看 5 年對之後 5 年只有 −0.21；回看 15 年對之後 15 年達到 −0.60。短期的過去報酬幾乎沒有參考價值，長期的才有。</p>' + F['q2_tA'] + '<p class="note">月資料大量重疊：獨立的 20 年窗口只有六、七個，相關係數的精確度有限。</p>') + angle('面向 B','五組的完整分布：熱起點差在「上檔」',
    '<p>最熱組（起點之前 10 年實質年化 ≥10.9%）之後 20 年平均 4.3%，最冷組 8.8%。兩組最差的 10% 情況分別是 1.9% 和 5.7%，20 年年化超過 5% 的機率是 37% 和 93%。持有 10 年時，最熱組有 18% 的起點是實質虧損。2026 年 8 月的前 10 年實質年化是 11.5%，屬於最熱組。</p>'
    + fig('依起點之前 10 年報酬分五組，之後的實質年化報酬','月資料起點；滑過長條可看較差 10% 的情況',F['q2_cB']) + F['q2_tB']
    + fig('起點之前 10 年 vs 之後 20 年','年度資料，每一點是一個起始年（1881–2005）；橘點為標註年份',F['q2_scatter'],'<div class="legend"><span><i class="dotkey" style="background:var(--s1)"></i>起始年份</span><span><i class="dotkey" style="background:var(--s2)"></i>標註：1920、1928、1967、1974、1979、1999</span></div>')) + angle('面向 C','分時期：現代的效果反而最強',
    '<p>1881–1913 年沒有任何冷起點，熱起點之後也沒有變差（相關係數為正）。1914 年以後每一段都是負相關。1982 年以後的起點最明顯：前 10 年對後 20 年的相關係數 −0.84，熱起點之後 10 年實質年化 3.9%，冷起點 11.7%。現代並沒有讓「起點」變得不重要。</p>' + F['q2_tC']) + angle('面向 D','定期定額能不能躲掉起點效應？不能',
    '<p>改成每月投入同樣金額 10 或 20 年，用內部報酬率比較。最冷組和最熱組的差距，定期定額是 5.0（10 年）與 4.7（20 年）個百分點，單筆是 5.0 與 4.6，幾乎一樣。原因是起點效應反映的是之後整段期間的報酬偏低，不只是第一天的價格。定期定額 10 年的最差情況反而比單筆更差（−9.1% 對 −5.0%），因為後段投入的錢最多，最怕期末大跌。</p>' + F['q2_tD']) + angle('面向 E','相對公債：熱起點之後 10 年，股票只有一半機率贏',
    '<p>最冷組起點之後 10 年，股票贏過 10 年期公債的機率是 93%；最熱組只有 52%，平均只多 1.3 個百分點。拉長到 20 年，最熱組仍有 96% 的機率贏公債。熱起點對「該不該長期持有股票」影響不大，但對「股票在未來 10 年能多賺多少」影響很大。</p>' + F['q2_tE']) + angle('面向 F','估值：熱起點加高估值最差，而且現代沒有失效',
    '<p>熱起點且 CAPE ≥25 時，之後 10 年實質年化 −0.9%，這些起點全部集中在 1928–1930 和 1997–2001 年。熱起點但 CAPE 15–25 時是 5.3%。另一個問題是「CAPE 在估值整體偏高的現代還有沒有用」。以 CAPE 預測之後 10 年報酬，相關係數在 2000–2016 年起點是 −0.84，比過去任何時期都強。</p>' + F['q2_tF'] + F['q2_tF2']) + angle('面向 G','16 國驗證：冷起點較好是普遍現象，熱起點最差則主要是美國',
    '<p>用 Jordà-Schularick-Taylor 資料庫的 16 國股票實質報酬（1870–2020）檢查。各國自己的時間序列中，16 國有 15 國是負相關，只有瑞典略正。把美國以外 15 國合併，最冷組之後 10 年實質年化 5.8%，明顯最好；但最熱組 3.9% 並不是最差，中間組只有 2.9%。國際資料支持「冷起點較好」，對「熱起點最差」的支持較弱。</p>'
    + '<div class="chips" aria-label="各國相關係數">' + F['q2_country'] + '</div><p class="note">上方為各國「前 10 年 → 後 10 年」實質報酬的相關係數。</p>' + F['q2_tG']) + angle('面向 H','現況類比：前 10 年實質 ≥10% 且 CAPE ≥28',
    '<p>符合條件且已有結果的起點只有 1929 和 1997–2001 年：之後 10 年實質年化介於 −3.3% 到 +4.3%，之後 20 年介於 +0.8% 到 +6.9%。2018 年以後符合的起點還沒有 10 年結果。</p>' + F['q2_tH']) + vs([
    ('長期平均','熱起點之後 20 年實質年化約 4%，冷起點約 9%；20 年都為正。'),
    ('現代時期','1982 年以後的起點，起點效應更強；CAPE 的預測力也沒有因為估值基準上移而失效。'),
    ('對現在的意義','現在屬於最熱組，CAPE 41。歷史上的可比起點，之後 10 年實質年化大約落在 −3% 到 +4%，20 年約 1% 到 7%。')]) + r'''
</section>

<!-- ================= Q3 ================= -->
<section class="q" id="q3">
  <header><p class="eyebrow">Question 3 · 美國產業 1927–2026 ＋ 標普類股 ETF 2000–2026</p><h2>每年將投資轉換為近年來績效最佳的類股，會比大盤好嗎？</h2></header>
  <p class="oneline">照題目的做法（每年換到去年第一名的大類股）沒有穩定優勢。真正有效的是「細分產業、每月更新」的產業動能，但它在現代明顯變弱。現代比較特別的是：長期領先的類股延續得更久。</p>
  <p class="how">做法：Ken French 的 10／12／17／30／49 產業組合（1926–2026 月資料）與 SPDR 類股 ETF（2000–2026）。年度版每年底換一次；月度版每月依過去 1–12 個月報酬選股，持有 1–12 個月（重疊持有）。都和大盤（CRSP 全市場或 SPY）比較，未計成本與稅。</p>
  <div class="angles-index"><span><b>A</b>題目原意</span><span><b>B</b>回看×持有</span><span><b>C</b>產業粗細</span><span><b>D</b>分時期</span><span><b>E</b>滾動 10 年</span><span><b>F</b>長回看期</span><span><b>G</b>成本</span><span><b>H</b>名次延續</span><span><b>I</b>反向</span></div>
  ''' + angle('面向 A','題目原意：每年年底換到「近年」最強類股',
    '<p>標普類股 ETF 追去年第一名，2000–2025 年化 7.5%，SPY 8.0%，26 年只贏 11 年。10 大產業追去年第一名，1928–2025 年化 10.7%，大盤 10.1%，只有一半年份贏，t 值 1.0。改看近 3 年第一名反而變差（7.9%）。49 細產業的去年冠軍有 +2.3 的 t 值，但年波動高達 44%。去年冠軍隔年的名次接近隨機，平均排第 5.6 名。</p>'
    + F['q3_tA'] + fig('去年冠軍產業，隔年在 10 大產業中排第幾？','1928–2025 共 98 年；橫線為完全隨機時的期望次數（9.8 次）',F['q3_cA'])
    + '<details><summary>標普類股 ETF：每年追去年冠軍的逐年結果</summary><div class="tbl"><table><thead><tr><th scope="col" style="text-align:left">持有年度</th><th scope="col">持有類股（去年冠軍）</th><th scope="col">類股報酬</th><th scope="col">SPY 報酬</th><th scope="col">當年名次</th></tr></thead><tbody>' + F['q3_rows_spdr'] + '</tbody></table></div></details>') + angle('面向 B','回看期 × 持有期：月度更新的產業動能長期有效',
    '<p>改成每月更新，結果完全不同。10 大產業買過去表現最好的 3 個，16 種回看與持有組合全部贏大盤，每年多 1.1 到 3.9 個百分點，多數 t 值超過 2。49 細產業的效果更強，最好的組合（看過去 12 個月、持有 1 個月）每年多 7.0 個百分點。關鍵差別在兩點：每月更新而不是一年一次，而且同時持有好幾個產業，而不是押單一冠軍。</p>' + F['q3_tB10'] + F['q3_tB49']) + angle('面向 C','產業切得越細，動能越強；標普 ETF 版本最弱',
    '<p>用學術上常見的「過去 12 個月、略過最近 1 個月」選前 20%：10 大產業每年 +3.3、49 細產業 +4.8 個百分點。同樣做法套在標普類股 ETF（2000–2026）只有 +1.0，t 值 0.6，和運氣分不開。標普的 11 個大類股太粗，而且這段時期正好是動能減弱的現代。</p>' + F['q3_tC']) + angle('面向 D','分時期：現代的產業動能明顯變弱',
    '<p>49 細產業月度動能，1927–1945 年每年 +6.5、1946–1981 年 +5.8，2010 年後只剩 +2.0（t 值 1.0）。標普類股 ETF 版本在 2000–2009 年每年 +4.0，2010 年後 −0.8。年度換冠軍的做法在 2010 年後平均 +5.0，但只有一半年份贏，主要靠 2020 年科技、2021 與 2024 年耐久財、2022 年能源等少數大勝。</p>' + F['q3_tD'] + '<p class="note">10 大產業的「耐久財」在 2020 年後大部分由 Tesla 主導，近年的結果有很強的單一個股成分。</p>') + angle('面向 E','滾動 10 年：細產業的優勢在 2010 年後縮小',
    fig('產業動能策略的滾動 10 年每年超額報酬','單位：百分點；每月更新、持有 1 個月',F['q3_cE']) + '<p>49 細產業的滾動 10 年超額報酬，在 1960–1980 年代和 2000 年代大約每年 +7 個百分點，2010 年後降到 +2 到 +3。10 大產業過去大多落在每年 +2 到 +4 之間。截至 2026 年中，兩者都只剩約 +1.6。「變弱」在細產業最明顯，大類股的動能本來就比較小。</p>') + angle('面向 F','現代的特殊之處：長期領先者延續更久',
    '<p>這是現代和長期平均最不一樣的地方。用「近 5 年最強」的標普類股，2004–2025 年化 16.0%，SPY 10.6%，t 值 2.3，68% 的年份贏。但這幾乎全來自兩個長週期：2005–2011 年的能源（原物料超級週期）與 2018–2025 年的科技。同一做法在 1932–1999 年的 10 大產業每年落後 1.5 個百分點，2000 年後轉為 +3.7。現代的贏家延續性確實比過去強，但樣本只有兩個週期，下一個週期何時開始與結束都無法事先知道。</p>') + angle('面向 G','成本與稅：月度動能可行，但稅會吃掉一大塊',
    '<p>年度換冠軍有 84% 的年份會換類股；以 10 大產業的超額報酬計算，每次單邊交易成本要超過約 110 個基點才會吃光優勢。月度動能（10 大產業前 3 名）每年單邊週轉約 221%，損益兩平的成本約每次 62 個基點。用 ETF 交易時，一般交易成本遠低於這個水準，但在需要繳資本利得稅的帳戶，頻繁換股的稅負可能吃掉大部分優勢。</p>') + angle('面向 H','名次延續：年度名次幾乎不相關',
    '<p>用等級相關係數衡量「今年的產業名次和明年像不像」：10 大產業平均 0.04，49 細產業 0.10，標普類股 ETF 0.04。只有 1982–1999 年略高（0.15）。年度名次接近隨機，這也是「每年換冠軍」無效的直接原因。</p>' + F['q3_tH']) + angle('面向 I','反向：去年最差的細產業最好避開',
    '<p>大類股的去年最後一名，隔年表現和大盤差不多（10 大產業 9.4% 對 10.1%）。但細分到 49 個產業時，去年最後一名的年化只有 2.8%。動能在「避開輸家」這一側比「追贏家」更穩定。</p>' + F['q3_tI']) + vs([
    ('長期平均','年度換冠軍大類股沒有優勢；每月更新的細產業動能每年多 3–5 個百分點。'),
    ('現代時期','月度動能減弱到每年約 +2 個百分點，統計上已不顯著；標普 ETF 版本 2010 年後為負。長回看期的領先者（能源、科技）延續了很久。'),
    ('對現在的意義','2018 年以來的科技領先是「長回看期有效」的主要來源。歷史上這種長週期最終都會結束，但這份資料無法判斷結束的時間。')]) + r'''
</section>

<!-- ================= Q4 ================= -->
<section class="q" id="q4">
  <header><p class="eyebrow">Question 4 · EDHEC 1997–2018 ＋ Credit Suisse 1994–2021</p><h2>近幾年績效最佳的避險基金策略，績效是否優於當年度所有策略的平均？</h2></header>
  <p class="oneline">不會。兩套獨立的指數都顯示，追去年或近三年的最佳策略會落後平均，2008 年後更明顯。唯一看起來有效的是「每月追最近幾個月的贏家」，但那主要是指數報酬被平滑的假象。</p>
  <p class="how">做法：EDHEC-Risk 10 個互不重疊的策略（1997–2018 月資料）與 Credit Suisse 11 個策略（1994–2021 月資料，含事件驅動的 3 個子策略）。和當年所有策略的等權平均比較。兩套指數挑出的「去年最佳策略」只有 14／24 年相同，所以兩套結果可以互相驗證。</p>
  <div class="angles-index"><span><b>A</b>題目原意</span><span><b>B</b>月度追逐</span><span><b>C</b>夏普值</span><span><b>D</b>分時期</span><span><b>E</b>策略類型</span><span><b>F</b>名次延續</span><span><b>G</b>最新兩年</span></div>
  ''' + angle('面向 A','題目原意：每年年底換到去年或近 3 年最佳策略',
    '<p>EDHEC：追去年第一名，年報酬平均 −0.1%，所有策略平均 5.9%，1 元變 0.75 元。Credit Suisse：追去年第一名 5.7%，平均 7.3%，年化 4.9% 對 7.0%，26 年只贏 12 年。改看近 3 年第一名或前 3 名，八種組合全部落後或打平。</p>'
    + F['q4_tA'] + fig('1997 年底投入 1 元的累積價值（EDHEC）','滑過圖表可看每年數值',F['q4_cum']) + fig('去年冠軍策略，隔年在 10 個策略中排第幾？（EDHEC）','1998–2017 共 20 年；橫線為完全隨機時的期望次數（2 次）',F['q4_rank'])
    + '<details><summary>逐年結果：EDHEC 去年冠軍策略在下一年的表現</summary><div class="tbl"><table><thead><tr><th scope="col" style="text-align:left">持有年度</th><th scope="col">去年冠軍策略</th><th scope="col">去年報酬</th><th scope="col">今年報酬</th><th scope="col">10 策略平均</th><th scope="col">今年名次</th></tr></thead><tbody>' + F['q4_rows'] + '</tbody></table></div></details>') + angle('面向 B','月度追逐：看起來有效，其實多半是平滑假象',
    '<p>每月依過去 3–6 個月選前 3 名、持有 1 個月，EDHEC 每年多 4.6–4.8 個百分點（t 值約 4），Credit Suisse 也有 +2.7。但持有期一拉長到 12 個月，優勢就消失或轉負。原因是避險基金指數的月報酬有明顯的序列相關：基金持有的資產流動性差、估價會延後反映，報酬被平滑了。而且實際的避險基金通常要求提前 30–90 天申請贖回，每月換策略做不到。</p>' + F['q4_tB3'] + F['q4_tB1'] + F['q4_tBcs']) + angle('面向 C','改用夏普值挑：比較不差，但仍沒有贏',
    '<p>用過去 12 個月的夏普值（報酬除以波動）挑，可以避開「去年大漲但波動極大」的策略。第 1 名的落後從每年 −2.2 縮小到 −0.4 個百分點，但仍沒有贏過平均。反向買去年最差的策略也沒有比較好。</p>' + F['q4_tC']) + angle('面向 D','分時期：2008 年後更差',
    '<p>兩套資料都顯示，2008 年後追逐的結果更差。Credit Suisse 追去年第一名，1995–2007 年每年 +0.4 個百分點，2008–2021 年 −3.3；追近 3 年第一名，從 +3.4 變成 −4.0。名次的延續性也消失了：Credit Suisse 的年度等級相關係數全期 0.12，2008 年後 −0.04。</p>' + F['q4_tD']) + angle('面向 E','策略類型：輸的幾乎都是方向性策略',
    '<p>EDHEC 中，去年冠軍是方向性策略（新興市場、放空、股票多空、管理期貨、全球宏觀）的 13 年，隔年平均落後 10.6 個百分點；冠軍是套利型策略的 7 年，平均領先 2.4 個百分點。只在 5 個套利型策略中追第一名，每年 +0.9（t 值 1.6）；只在方向性策略中追，−1.6。另外，在股市方向反轉的 4 年（前一年漲、今年跌，或相反），追逐平均落後 28 個百分點；其餘 16 年只落後 0.6。Credit Suisse 的結果相同：方向性冠軍平均落後 2.6，套利型約打平。</p>' + F['q4_tE']) + angle('面向 F','名次延續：幾乎沒有',
    '<p>EDHEC 策略的年度等級相關係數平均 0.05；以每月滾動的「過去 12 個月 vs 之後 12 個月」計算是 0.11，只有 56% 的月份為正。策略之間的領先順序，一年後幾乎重新洗牌。</p>') + angle('面向 G','最新兩年：HFR 公告的四大策略',
    '<p>2018 年以後找不到完整的策略指數。HFR 年底公告的四大策略中，2024 年最好的是股票多空（Equity Hedge，+12.3%），2025 年仍是第一（+17.3%）。這和面向 E 一致：股市方向沒有反轉時，方向性冠軍可以延續。只有一個年度的觀察，數字也是初值。</p>') + vs([
    ('長期平均','追去年最佳策略每年落後平均約 1.6（CS）到 6.1（EDHEC）個百分點。'),
    ('現代時期','2008 年後落後更多，名次延續性轉為零或負。'),
    ('對現在的意義','輸的主要是方向性策略在市場反轉的年份。2024–2025 年股票多空連兩年領先，延續與否取決於股市方向，不取決於它去年的成績。')]) + r'''
</section>

<section class="synth" id="synth">
  <h2>總表：四題 × 長期平均 vs 現代</h2>
  <div class="tbl"><table>
    <thead><tr><th scope="col" style="text-align:left">題目</th><th scope="col" style="text-align:left">長期平均的答案</th><th scope="col" style="text-align:left">現代時期有何不同</th><th scope="col" style="text-align:left">最有力的證據</th></tr></thead>
    <tbody>
      <tr><th scope="row">1 高報酬之後</th><td>一年大漲無影響；連 3–5 年高報酬後，1–5 年報酬偏低、回撤風險上升</td><td>熱行情後的下一年更差，但 5 年恢復較快</td><td>熱行情加 CAPE ≥30：之後 5 年年化 0.1%（僅 4 段）</td></tr>
      <tr><th scope="row">2 長期起點</th><td>冷起點 20 年實質約 9%，熱起點約 4%；20 年皆為正</td><td>起點效應更強；CAPE 預測力沒有失效</td><td>16 國中 15 國同方向；定期定額也躲不掉</td></tr>
      <tr><th scope="row">3 追最強類股</th><td>年度換冠軍大類股無優勢；月度細產業動能有效</td><td>動能減弱到不顯著；但長週期領先者（能源、科技）延續很久</td><td>49 細產業動能 +4.8（t 5.5），2010 年後 +2.0（t 1.0）</td></tr>
      <tr><th scope="row">4 追最強避險策略</th><td>落後平均，冠軍常隔年墊底</td><td>2008 年後更差</td><td>兩套獨立指數、八種組合都落後</td></tr>
    </tbody></table></div>
  <ol>
    <li><b>過去報酬的資訊量，取決於看多長。</b>一年的冠軍（大盤、類股、避險策略）隔年接近隨機；三到十年的累積才有預測力，而且主要透過估值傳導。</li>
    <li><b>現代確實和長期平均不同，但不同的方向不是「這次不一樣」。</b>估值基準上移、報酬偏高，但均值回歸與估值的預測力在現代並沒有變弱，反而更強。真正變弱的是短中期的產業動能。</li>
    <li><b>追逐最常換來的是集中與波動。</b>換到單一冠軍類股或策略，主要結果是波動與單年虧損加大，報酬沒有穩定提高。</li>
    <li><b>這些是歷史基準，不是擇時訊號。</b>現在同時處於熱行情與極高估值，歷史上可比的只有 3 段，結果都偏弱，但路徑各不相同。比較實際的用法是下修未來幾年的報酬預期，並確認部位撐得住更寬的結果分布，而不是預測轉折點。</li>
  </ol>
</section>

<section class="method" id="method">
  <h2>資料與方法</h2>
  <ul>
    <li><b>美股：</b>1871 年至 1926 年 6 月用 Shiller S&amp;P 綜合指數價格與股息；1926 年 7 月至 2026 年 8 月用 Ken French 資料庫的 Mkt-RF 加 RF（CRSP 美國全市場，含息）。CAPE、10 年期公債殖利率與公債總報酬取自 Shiller 最新版資料（<a href="https://shillerdata.com/">shillerdata.com</a>，至 2026 年 9 月）。通膨用 Shiller CPI（1913 年前）與 FRED CPIAUCNS；2025 年 10 月 CPI 因美國政府停擺未公布，以前後月份做對數內插。</li>
    <li><b>國際：</b>Jordà-Schularick-Taylor Macrohistory Database R6（<a href="https://www.macrohistory.net/database/">macrohistory.net</a>）16 國股票總報酬與 CPI，1870–2020。只用於第 2 題的 10–20 年期比較。</li>
    <li><b>產業與類股：</b>Ken French 10／12／17／30／49 Industry Portfolios 市值加權月報酬（1926–2026）；SPDR Select Sector ETF 含息調整價（Yahoo Finance，2000–2026；XLRE 自 2016、XLC 自 2019 納入）。月度動能採重疊持有的 Jegadeesh–Titman 方法。</li>
    <li><b>避險基金：</b>EDHEC-Risk Alternative Indexes（1997 年 1 月至 2018 年 11 月，EDHEC 課程公開資料集的 GitHub 鏡像）；Credit Suisse Hedge Fund Index 各策略月報酬（1994 年 1 月至 2022 年 4 月，來自公開 GitHub 專案中的 Bloomberg 匯出檔，屬二手資料、未與官方表格核對）；HFR 年底新聞稿中的 2024、2025 年四大策略初值。兩套指數都不可直接投資，有存活者與回填偏差，報酬已扣基金費用。HFRX 資料有不得轉載的條款，未使用。</li>
    <li><b>統計：</b>月度觀察點高度重疊，表中的月數遠大於獨立樣本；「段數」以相隔超過 12 個月為新的一段。t 值為超額報酬平均除以標準誤，未校正重疊與多重檢定，實際顯著性比表面低。所有回測未計交易成本與稅。</li>
  </ul>
</section>

<footer>由 Claude 依公開資料回測整理，2026-10-04（第二版）。內容是歷史基準的描述，不是投資建議。</footer>
</div>
''' + script
open('chasing.html','w').write(html)
print(len(html))
