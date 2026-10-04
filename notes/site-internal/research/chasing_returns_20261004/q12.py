import pandas as pd, numpy as np, json
a=pd.read_csv('mkt_annual.csv',index_col=0)
m=pd.read_csv('mkt_monthly.csv',index_col=0)
R=a['ret']; RR=a['real']
yrs=a.index.values
def ann(s,y0,y1):  # annualized over years y0..y1 inclusive
    seg=s.loc[y0:y1]; return (1+seg).prod()**(1/len(seg))-1
out={}
# trailing & forward for each year-end t
rows=[]
for t in yrs:
    d={'year':t}
    for k in [1,2,3,5,10]:
        if t-k+1>=yrs[0]: d[f'tr{k}']=ann(R,t-k+1,t); d[f'trr{k}']=ann(RR,t-k+1,t)
    for h in [1,3,5,10,15,20]:
        if t+h<=yrs[-1]: d[f'f{h}']=ann(R,t+1,t+h); d[f'fr{h}']=ann(RR,t+1,t+h)
    rows.append(d)
T=pd.DataFrame(rows).set_index('year')
T.to_csv('trail_fwd_annual.csv')
print("Years:",yrs[0],yrs[-1],len(yrs))
print("Unconditional nominal 1y mean/median/pos:",R.mean(),R.median(),(R>0).mean())
print("geo nominal all:",ann(R,yrs[0],yrs[-1]), "real:",ann(RR,yrs[0],yrs[-1]))
def summ(mask,label,cols=('f1','f3','f5')):
    sub=T[mask]
    res={'label':label,'n':int(mask.sum()),'years':list(map(int,sub.index))}
    for c in cols:
        v=sub[c].dropna()
        res[c]={'n':len(v),'mean':v.mean(),'median':v.median(),'pos':(v>0).mean(),'min':v.min(),'max':v.max()}
    return res
base=summ(T.index==T.index,'全部年份')
conds={
 'tr1>20':T['tr1']>0.20,
 'tr1>25':T['tr1']>0.25,
 'two_yrs>20': (T['tr1']>0.20)&(T['tr1'].shift(1)>0.20),
 'tr3>15':T['tr3']>0.15,
 'tr3>20':T['tr3']>0.20,
 'tr5>15':T['tr5']>0.15,
 'tr1<-10':T['tr1']<-0.10,
 'tr3<0':T['tr3']<0,
}
res={'base':base}
for k,v in conds.items(): res[k]=summ(v,k)
for k,v in res.items():
    print(f"\n== {k}  n={v['n']}")
    if k!='base': print(v['years'])
    for c in ('f1','f3','f5'):
        s=v[c]; print(f"  {c}: n={s['n']} mean={s['mean']*100:.1f} med={s['median']*100:.1f} pos={s['pos']*100:.0f}% min={s['min']*100:.1f} max={s['max']*100:.1f}")
json.dump(res,open('q1_res.json','w'),default=float)
# quintiles of trailing 3y -> fwd 1,3,5 nominal
for tr in ['tr1','tr3','tr5']:
    sub=T[[tr,'f1','f3','f5']].dropna(subset=[tr])
    q=pd.qcut(sub[tr],5,labels=['Q1低','Q2','Q3','Q4','Q5高'])
    g=sub.groupby(q,observed=True).agg(trmin=(tr,'min'),trmax=(tr,'max'),f1=('f1','mean'),f1med=('f1','median'),f3=('f3','mean'),f5=('f5','mean'),n=(tr,'size'))
    print('\n',tr); print((g*[100,100,100,100,100,100,1]).round(1))
    print(' corr f1',sub[tr].corr(sub['f1']).round(3),' f3',sub[tr].corr(sub['f3']).round(3),' f5',sub[tr].corr(sub['f5']).round(3))
