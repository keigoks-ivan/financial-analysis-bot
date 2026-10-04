import pandas as pd, json, numpy as np
from charts import grouped_columns, scatter, columns_with_ref, esc
P=lambda v,d=1: f"{v*100:+.{d}f}%"
p=lambda v,d=1: f"{v*100:.{d}f}%"
q1=json.load(open('q1_res.json')); q3=json.load(open('q3_res.json')); q4=json.load(open('q4_res.json'))
T=pd.read_csv('trail_fwd_annual.csv',index_col=0)

# ---------- Q1 chart
conds=[('base','全部年份'),('tr1>20','前 1 年 >20%'),('two_yrs>20','連 2 年 >20%'),('tr3>20','前 3 年年化 >20%'),('tr3<0','前 3 年為負')]
f1=[q1[k]['f1']['mean']*100 for k,_ in conds]; f5=[q1[k]['f5']['mean']*100 for k,_ in conds]
tips1=[[f"{lab}｜下一年平均 {q1[k]['f1']['mean']*100:.1f}%（中位數 {q1[k]['f1']['median']*100:.1f}%，上漲機率 {q1[k]['f1']['pos']*100:.0f}%，n={q1[k]['f1']['n']}）" for k,lab in conds],
       [f"{lab}｜之後 5 年年化平均 {q1[k]['f5']['mean']*100:.1f}%（5 年後為正的機率 {q1[k]['f5']['pos']*100:.0f}%，n={q1[k]['f5']['n']}）" for k,lab in conds]]
c1=grouped_columns([l for _,l in conds],[('下一年報酬（平均）','--s1',f1),('之後 5 年年化（平均）','--s2',f5)],tips=tips1,aria='不同條件下，美股下一年與之後五年的平均報酬')
rows1=''.join(f"<tr><th scope='row'>{lab}</th><td>{q1[k]['n']}</td><td>{q1[k]['f1']['mean']*100:.1f}%</td><td>{q1[k]['f1']['median']*100:.1f}%</td><td>{q1[k]['f1']['pos']*100:.0f}%</td><td>{q1[k]['f1']['min']*100:.0f}%</td><td>{q1[k]['f5']['mean']*100:.1f}%</td><td>{q1[k]['f5']['pos']*100:.0f}%</td></tr>" for k,lab in conds)
ep=T[T.tr3>0.20]
NEG=' class="neg"'
def neg(v): return NEG if (v is not None and not pd.isna(v) and v<0) else ''
def cell(v): return '—' if pd.isna(v) else f"{v*100:.1f}%"
def cls(v): return '' if pd.isna(v) else (' class="neg"' if v<0 else '')
rows_ep=''.join(f"<tr><th scope='row'>{y}</th><td>{r.tr3*100:.1f}%</td><td{cls(r.f1)}>{cell(r.f1)}</td><td{cls(r.f3)}>{cell(r.f3)}</td><td{cls(r.f5)}>{cell(r.f5)}</td></tr>" for y,r in ep.iterrows())

# ---------- Q2 charts
sub=T[['trr10','fr20']].dropna()
pts=[(r.trr10*100,r.fr20*100,f"{y} 年底起投入｜前 10 年實質年化 {r.trr10*100:.1f}%｜之後 20 年實質年化 {r.fr20*100:.1f}%") for y,r in sub.iterrows()]
cur10=T.loc[2025,'trr10']*100
c2=scatter(pts,'起點前 10 年的實質年化報酬','之後 20 年的實質年化報酬',xref=cur10,xref_label=f'2025 年底：{cur10:.1f}%',aria='起點前十年報酬與之後二十年報酬的散布圖',
           hl=lambda x,y,t: t.startswith(('1920','1928','1967','1974','1979','1999')))
tq=T.dropna(subset=['trr10']).copy(); tq['q']=pd.qcut(tq['trr10'],5,labels=['最低 20%','次低','中間','次高','最高 20%'])
g=tq.groupby('q',observed=True)
qcat=list(g.groups.keys())
m10=list(g['fr10'].mean()*100); m20=list(g['fr20'].mean()*100)
rng=[(g['trr10'].min()[k]*100,g['trr10'].max()[k]*100) for k in qcat]
tips2=[[f"前 10 年實質年化 {a:.1f}%～{b:.1f}% 的起點｜之後 10 年實質年化平均 {v:.1f}%" for (a,b),v in zip(rng,m10)],
       [f"前 10 年實質年化 {a:.1f}%～{b:.1f}% 的起點｜之後 20 年實質年化平均 {v:.1f}%" for (a,b),v in zip(rng,m20)]]
c3=grouped_columns([str(c) for c in qcat],[('之後 10 年（實質年化）','--s1',m10),('之後 20 年（實質年化）','--s2',m20)],tips=tips2,height=280,aria='依起點前十年報酬分五組，之後十年與二十年的實質年化報酬')
rows2=''
for k,(a,b) in zip(qcat,rng):
    s=g.get_group(k)
    rows2+=f"<tr><th scope='row'>{k}</th><td>{a:.1f}%～{b:.1f}%</td>"
    for h in (5,10,20):
        v=s[f'fr{h}'].dropna(); rows2+=f"<td>{v.mean()*100:.1f}%</td><td{neg(v.min())}>{v.min()*100:.1f}%</td>"
    rows2+="</tr>"

# ---------- Q3
R=pd.read_csv('q3_ff10_lb1_top1.csv',index_col=0)
rk=R['rank_next'].value_counts().sort_index()
c4=columns_with_ref([f"第 {int(i)} 名" for i in range(1,11)],[int(rk.get(i,0)) for i in range(1,11)],len(R)/10,'',fmt=lambda v:f"{v}",
    tips=[f"去年冠軍產業隔年排第 {i} 名：{int(rk.get(i,0))} 次（共 {len(R)} 年）" for i in range(1,11)],aria='去年冠軍產業在隔年的名次分布',ylab_suffix=' 次')
def q3row(key,lab):
    s=q3[key]['vs_mkt']
    return f"<tr><th scope='row'>{lab}</th><td>{s['y0']}–{s['y1']}</td><td>{s['cagr']*100:.1f}%</td><td>{s['bcagr']*100:.1f}%</td><td>{s['hit']*100:.0f}%</td><td>{s['t']:.1f}</td><td>{s['vol']*100:.0f}% / {s['bvol']*100:.0f}%</td></tr>"
rows3=''.join([q3row('SPDR_lb1_top1','SPDR 類股 ETF：去年第 1 名'),q3row('SPDR_lb3_top1','SPDR 類股 ETF：近 3 年第 1 名'),
               q3row('FF10_lb1_top1','10 大產業：去年第 1 名'),q3row('FF10_lb1_top3','10 大產業：去年前 3 名'),q3row('FF10_lb3_top1','10 大產業：近 3 年第 1 名'),
               q3row('FF12_lb1_top1','12 大產業：去年第 1 名'),q3row('FF30_lb1_top1','30 細產業：去年第 1 名'),q3row('FF30_lb1_top3','30 細產業：去年前 3 名')])
S=pd.read_csv('q3_spdr_lb1_top1.csv',index_col=0)
names={'XLB':'原物料','XLE':'能源','XLF':'金融','XLI':'工業','XLK':'科技','XLP':'必需消費','XLU':'公用事業','XLV':'醫療保健','XLY':'非必需消費','XLRE':'不動產','XLC':'通訊服務'}
rows_spdr=''.join(f"<tr><th scope='row'>{y}</th><td>{names.get(r.pick,r.pick)}（{r.pick}）</td><td{neg(r.ret)}>{r.ret*100:.1f}%</td><td{neg(r.bench)}>{r.bench*100:.1f}%</td><td>{int(r.rank_next)} / {int(r.nsec)}</td></tr>" for y,r in S.iterrows())

json.dump({'c1':c1,'c2':c2,'c3':c3,'c4':c4,'rows1':rows1,'rows_ep':rows_ep,'rows2':rows2,'rows3':rows3,'rows_spdr':rows_spdr},open('parts_q123.json','w'),ensure_ascii=False)
print('ok', len(c1),len(c2),len(c3),len(c4))
