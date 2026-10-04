import pandas as pd, json
from charts import lines, columns_with_ref, esc
q4=json.load(open('q4_res.json'))
R=pd.read_csv('q4_nonover_lb1_top1.csv',index_col=0)
zh={'Convertible Arbitrage':'可轉債套利','CTA Global':'管理期貨 CTA','Distressed Securities':'困境證券','Emerging Markets':'新興市場','Equity Market Neutral':'股票市場中性','Fixed Income Arbitrage':'固定收益套利','Global Macro':'全球宏觀','Long/Short Equity':'股票多空','Merger Arbitrage':'併購套利','Short Selling':'放空'}
xs=[1997]+list(R.index)
a=[1.0]; b=[1.0]
for y,r in R.iterrows(): a.append(a[-1]*(1+r.ret)); b.append(b[-1]*(1+r.avg))
c5=lines(xs,[('追去年第 1 名','--s2',a),('10 策略等權平均','--s1',b)],aria='1 元投入追逐去年最佳策略與等權平均的累積價值',fmt=lambda v:f"{v:.2f} 元",ylab='')
rk=R['rank'].value_counts().sort_index()
c6=columns_with_ref([f"第 {i} 名" for i in range(1,11)],[int(rk.get(i,0)) for i in range(1,11)],len(R)/10,'',fmt=lambda v:f"{v}",
    tips=[f"去年冠軍策略隔年排第 {i} 名：{int(rk.get(i,0))} 次（共 {len(R)} 年）" for i in range(1,11)],aria='去年冠軍策略在隔年 10 個策略中的名次分布',ylab_suffix=' 次')
NEG=' class="neg"'
neg=lambda v: NEG if v<0 else ''
rows=''.join(f"<tr><th scope='row'>{y}</th><td>{zh[r.pick]}</td><td>{r.prev*100:.1f}%</td><td{neg(r.ret)}>{r.ret*100:.1f}%</td><td{neg(r.avg)}>{r.avg*100:.1f}%</td><td>{int(r['rank'])} / {int(r.n)}</td></tr>" for y,r in R.iterrows())
def vrow(set_, key, lab):
    s=q4[set_][key]
    return f"<tr><th scope='row'>{lab}</th><td>{s['y0']}–{s['y1']}</td><td>{s['mean']*100:.1f}%</td><td>{s['avg']*100:.1f}%</td><td>{s['ex']*100:+.1f}</td><td>{s['hit']*100:.0f}%</td><td>{s['worst_mean']*100:.1f}%</td></tr>"
vrows=''.join([vrow('nonover','lb1_top1','10 策略：去年第 1 名'),vrow('nonover','lb1_top3','10 策略：去年前 3 名'),vrow('nonover','lb3_top1','10 策略：近 3 年第 1 名'),vrow('nonover','lb3_top3','10 策略：近 3 年前 3 名'),
               vrow('nonover_noSS','lb1_top1','去掉放空（9 策略）：去年第 1 名'),vrow('nonover_noSS','lb1_top3','去掉放空：去年前 3 名'),vrow('nonover_noSS','lb3_top1','去掉放空：近 3 年第 1 名'),vrow('all12','lb1_top1','12 指數全放（含重疊綜合指數）：去年第 1 名')])
json.dump({'c5':c5,'c6':c6,'rows4':rows,'vrows4':vrows,'end_a':a[-1],'end_b':b[-1]},open('parts_q4.json','w'),ensure_ascii=False)
print(a[-1],b[-1])
