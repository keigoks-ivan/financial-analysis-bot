import json, pandas as pd, numpy as np
from frags_v2 import table, tr, td, tdraw
A=json.load(open('tw_res.json')); M=json.load(open('tw_monthly.json')); S=json.load(open('tw_sector.json'))
D=pd.read_csv('tw_trail_fwd.csv',index_col=0)
rows=[tr(s['label'],[tdraw(str(s['n'])),td(s['f1']),td(s['f1_med']),tdraw(f"{s['f1_pos']*100:.0f}%"),td(s['f3']),td(s['f5'])]) for s in A['q1']]
t1=table(['條件（年底，價格指數）','年數','下一年平均','中位數','上漲機率','之後 3 年年化','之後 5 年年化'],rows)
rows=[tr(s['label'],[tdraw(f"{s['n']}／{s['ep'] if s['label']!='全部月份' else '—'}"),td(s['f12']),tdraw(f"{s['f12_pos']*100:.0f}%"),td(s['f36']),td(s['f60']),tdraw(f"{s['p_dd20']*100:.0f}%")]) for s in M['A']]
t2=table(['條件（月底，1993–2026）','月數／段數','之後 12 個月','上漲機率','之後 3 年年化','之後 5 年年化','12 個月內跌 ≥20%'],rows)
rows=[tr(r['q'],[tdraw(f"{r['lo']*100:.1f}%～{r['hi']*100:.1f}%"),td(r['f5']),td(r['f10']),tdraw(str(r['n10']))]) for r in A['q2']]
t3=table(['起點之前 10 年（名目，價格）','年化區間','之後 5 年年化','之後 10 年年化','10 年樣本數'],rows)
lab={'lb1_top1':'去年第 1 名','lb1_top3':'去年前 3 名','lb3_top1':'近 3 年第 1 名','lb3_top3':'近 3 年前 3 名','lb1_top1_contra':'反向：去年最後 1 名'}
rows=[tr(l,[tdraw(f"{S[k]['y0']}–{S[k]['y1']}"),td(S[k]['cagr']),td(S[k]['bcagr']),td(S[k]['ewcagr']),tdraw(f"{S[k]['hit']*100:.0f}%"),tdraw(f"{S[k]['t']:.1f}")]) for k,l in lab.items()]
t4=table(['做法（28 個類股，每年年底換）','期間','策略年化','加權指數年化','類股等權年化','贏加權指數的年份','t 值'],rows)
R=pd.read_csv('tw_sector_lb1.csv',index_col=0)
neg=lambda v: ' class="neg"' if v<0 else ''
rows_sec=''.join(f"<tr><th scope='row'>{y}</th><td>{r.pick}</td><td>{r.prev*100:.1f}%</td><td{neg(r.p)}>{r.p*100:.1f}%</td><td{neg(r.b)}>{r.b*100:.1f}%</td><td>{int(r['rank'])} / {int(r.n)}</td></tr>" for y,r in R.iterrows())
now=M['now']; yt=S['ytd2026']
card='<span class="chip fix">部分成立</span><p class="verdict">第 1、3 題成立，短期反轉比美國更明顯；第 2 題在台股看不到。</p><p class="ev">過去 12 個月漲超過 40% 後，之後 12 個月平均 −5.8%。現在台股近 12 個月 +86%、近 3 年年化 43%，是 1990 年以來最高。</p>'
an=D.loc[[1973,1987,1988,1989]]
rows=[tr(str(y),[tdraw(f"{r.tr1*100:.1f}%"),tdraw(f"{r.tr3*100:.1f}%"),td(r.f1),td(r.f3),td(r.f5)]) for y,r in an.iterrows()]
t5=table(['年底','當年','前 3 年年化','下一年','之後 3 年年化','之後 5 年年化'],rows)
section=f'''<section class="q" id="f7">
  <header><p class="eyebrow">追問 7</p><h2>台股適用嗎？</h2></header>
  <p class="oneline">部分適用。高報酬之後轉弱在台股更明顯，而且來得更快；追最強類股同樣贏不了大盤；但「冷起點長期較好」在台股看不到。</p>
  <p class="how">做法：臺灣證券交易所發行量加權股價指數（價格指數，不含股息）年資料 1967–2025、月資料 1990–2026；28 個類股指數 2009–2025（排除綜合類與 2023 年新設類股）。2003 年起的報酬指數顯示，股息每年約貢獻 3.7%，所以表中的報酬都比含息報酬低約 3–4 個百分點。找不到可用的台灣 CPI，第 2 題改用名目報酬。資料品質：1967–1989 年取自 Wikipedia，未經證交所核對；證交所的數字是透過網頁讀取工具轉錄，已和 Yahoo、臺灣指數公司等來源交叉核對。</p>
  <div class="angle"><h3>第 1 題（年資料）：一年大漲沒差，三年大漲之後轉弱</h3><p>前一年漲超過 30% 的 12 個年份，下一年平均仍有 19.8%；但之後 3 年年化只有 2.0%，全部年份是 11.9%。前三年年化超過 30% 的只有 1973、1977、1987–89 年，之後 5 年年化平均 1.3%。</p>{t1}</div>
  <div class="angle"><h3>第 1 題（月資料）：台股的反轉來得更快</h3><p>和美國不同，台股過去 12 個月漲超過 40% 之後，接下來 12 個月平均 −5.8%，上漲機率只有 45%，12 個月內跌 20% 以上的機率是 48%（全部月份 28%）。過去 36 個月最熱的 20% 之後 5 年年化只有 1.9%。台股波動大，大漲後的回吐也更快。</p>{t2}</div>
  <div class="angle"><h3>第 2 題：台股看不到長期的起點效應</h3><p>台股前 10 年報酬和後 10 年報酬的相關係數是 +0.03，幾乎為零；前 3 年對後 3 年是 −0.19。依前 10 年報酬分三組，之後 10 年反而是中間組最好、最冷組最差。台股只有 59 年資料，10 年窗口能形成的獨立樣本不到 6 個，這一題在台股無法得出結論。</p>{t3}</div>
  <div class="angle"><h3>第 3 題：追去年最強類股輸給加權指數</h3><p>每年年底換到去年最強的類股，2011–2025 年化 3.9%，加權指數 8.1%，15 年只贏 6 年。改成前 3 名或近 3 年最強，同樣落後。不過加權指數由半導體（台積電）主導，半導體在 16 年中有 13 年贏過大盤；和 28 個類股的等權平均（4.1%）相比，追逐大約打平。反向買去年最差的類股最差，年化 −8.9%。類股名次的年度相關係數是 0.03，幾乎沒有延續性。</p>{t4}
    <details><summary>逐年結果：去年最強類股在下一年的表現</summary><div class="tbl"><table><thead><tr><th scope="col" style="text-align:left">持有年度</th><th scope="col">去年最強類股</th><th scope="col">去年報酬</th><th scope="col">當年報酬</th><th scope="col">加權指數</th><th scope="col">當年名次</th></tr></thead><tbody>{rows_sec}</tbody></table></div></details>
    <p class="note">2025 年最強的玻璃陶瓷類，2026 年前 9 個月 +{yt['its_ytd']*100:.0f}%，加權指數 +{yt['taiex_ytd']*100:.0f}%，在 28 個類股中排第 {yt['rank_of_best25']}。</p></div>
  <div class="angle"><h3>現在的台股在歷史中的位置</h3><p>到 2026 年 9 月，加權指數近 12 個月 +86%（1990 年以來第 99 百分位），近 36 個月年化 43%，是 1990 年以來最高。2026 年前 9 個月上漲 66%。用年資料看，前 3 年年化比現在更高的只有 1973 年與 1987–89 年泡沫期。1987 年之後還漲了一年（+119%），1989 年之後一年 −53%；這四個年份之後 5 年年化介於 −6% 到 +8%。</p>{t5}</div>
  <div class="effect"><span class="chip fix">部分成立</span><p>第 1 題在台股成立，而且大漲之後的回吐來得更快、更深。第 3 題成立，不過要注意加權指數由半導體主導，「追類股」天生很難贏它。第 2 題在台股沒有證據，部分原因是資料太短。</p></div>
</section>'''
json.dump({'card':card,'section':section},open('frags_tw.json','w'),ensure_ascii=False)
print('ok',len(section))
