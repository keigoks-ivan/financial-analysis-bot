import pandas as pd, numpy as np, json, os, sys
T='tw/'
R={}
# ---------- annual TAIEX (price) ----------
a=pd.read_csv(T+'taiex_annual.csv')
a.columns=[c.strip().lower() for c in a.columns]
ycol=[c for c in a.columns if 'year' in c][0]; ccol=[c for c in a.columns if 'close' in c][0]
a=a.set_index(ycol)[ccol].astype(float).sort_index(); a=a.loc[1967:2025]
ret=a.pct_change().dropna()
# dividend yield gross-up if available
dy=None
if os.path.exists(T+'tw_div_yield.csv'):
    d=pd.read_csv(T+'tw_div_yield.csv'); d.columns=[c.strip().lower() for c in d.columns]
    dy=d.set_index([c for c in d.columns if 'year' in c][0]).iloc[:,0].astype(float)
    if dy.max()>1: dy=dy/100
R['years']=(int(ret.index.min()),int(ret.index.max()))
def ann(s,y0,y1): seg=s.loc[y0:y1]; return (1+seg).prod()**(1/len(seg))-1
rows=[]
for t in ret.index:
    d={'year':t,'tr1':ret[t]}
    for k in [2,3,5,10]:
        if t-k+1>=ret.index.min(): d[f'tr{k}']=ann(ret,t-k+1,t)
    for h in [1,3,5,10]:
        if t+h<=ret.index.max(): d[f'f{h}']=ann(ret,t+1,t+h)
    rows.append(d)
D=pd.DataFrame(rows).set_index('year')
def st(mask,lab):
    x=D[mask.fillna(False)]
    return {'label':lab,'n':int(len(x)),'years':[int(y) for y in x.index],'f1':x.f1.mean(),'f1_med':x.f1.median(),'f1_pos':(x.f1.dropna()>0).mean(),'f3':x.f3.mean(),'f5':x.f5.mean(),'f5_pos':(x.f5.dropna()>0).mean(),'n5':int(x.f5.notna().sum())}
conds=[('全部年份',D.tr1.notna()),('前 1 年 >30%',D.tr1>0.30),('前 1 年 >50%',D.tr1>0.50),('連 2 年 >20%',(D.tr1>0.2)&(D.tr1.shift(1)>0.2)),('前 3 年年化 >20%',D.tr3>0.20),('前 3 年年化 >30%',D.tr3>0.30),('前 3 年年化 <0%',D.tr3<0)]
R['q1']=[st(m,l) for l,m in conds]
for s in R['q1']: print(f"{s['label']:<12} n={s['n']:2d} f1 {s['f1']*100:6.1f} med {s['f1_med']*100:6.1f} pos {s['f1_pos']*100:3.0f}% f3 {s['f3']*100:5.1f} f5 {s['f5']*100:5.1f} pos5 {s['f5_pos']*100:3.0f}% n5 {s['n5']}  {s['years'] if s['n']<15 else ''}")
for tr_,f_ in [('tr1','f1'),('tr3','f3'),('tr3','f5'),('tr5','f5'),('tr10','f10')]:
    z=D[[tr_,f_]].dropna(); R[f'corr_{tr_}_{f_}']={'c':z.corr().iloc[0,1],'n':len(z)}; print('corr',tr_,f_,round(z.corr().iloc[0,1],2),len(z))
# Q2 quintiles trailing 10y -> forward 10y (nominal price)
z=D[['tr10','f10','f5']].dropna(subset=['tr10']).copy()
if len(z)>=15:
    z['q']=pd.qcut(z.tr10,3,labels=['最冷三分之一','中間','最熱三分之一'])
    R['q2']=[{'q':str(k),'lo':v.tr10.min(),'hi':v.tr10.max(),'f10':v.f10.mean(),'f5':v.f5.mean(),'n10':int(v.f10.notna().sum()),'years':[int(y) for y in v.index]} for k,v in z.groupby('q',observed=True)]
    for r in R['q2']: print(r['q'],round(r['lo']*100,1),round(r['hi']*100,1),'f5',round(r['f5']*100,1),'f10',None if r['f10']!=r['f10'] else round(r['f10']*100,1),r['n10'])
R['now']={'last_year':int(a.index.max()),'tr1':float(D.tr1.iloc[-1]),'tr3':float(D.tr3.iloc[-1]) if 'tr3' in D else None,'tr10':float(D.tr10.iloc[-1]) if 'tr10' in D else None}
print('now',R['now'])
D.to_csv('tw_trail_fwd.csv')
json.dump(R,open('tw_res.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o),ensure_ascii=False)
