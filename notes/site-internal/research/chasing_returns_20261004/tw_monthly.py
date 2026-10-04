import pandas as pd, numpy as np, json
m=pd.read_csv('tw/taiex_monthly.csv'); m.index=pd.PeriodIndex(m.month,freq='M'); p=m.close.astype(float)
lr=np.log(p/p.shift(1)).dropna()
def tr(k): return np.expm1(lr.rolling(k).sum()*12/k) if k>=12 else np.expm1(lr.rolling(k).sum())
def fw(k): s=lr.rolling(k).sum().shift(-k); return np.expm1(s*12/k)
D=pd.DataFrame({'tr12':tr(12),'tr36':tr(36),'f12':fw(12),'f36':fw(36),'f60':fw(60)})
w=np.exp(lr.cumsum()).values; n=len(w)
dd=np.full(n,np.nan)
for i in range(n-12):
    path=w[i:i+13]; dd[i]=(path/np.maximum.accumulate(path)-1).min()
D['dd12']=dd
R={}
v=D.tr36.notna()
def st(mask,lab):
    x=D[mask&v]; idx=np.where((mask&v).values)[0]; ep=1+int(np.sum(np.diff(idx)>12)) if len(idx) else 0
    return {'label':lab,'n':int(len(x)),'ep':ep,'f12':x.f12.mean(),'f12_pos':(x.f12.dropna()>0).mean(),'f36':x.f36.mean(),'f60':x.f60.mean(),'n60':int(x.f60.notna().sum()),'p_dd20':(x.dd12.dropna()<=-0.2).mean(),'years':sorted(set(int(k.year) for k in x.index))}
q=D.tr36[v].quantile(0.8); R['cut36']=q
conds=[('全部月份',v),('過去 12 個月 >40%',D.tr12>0.40),('過去 36 個月年化 >20%',D.tr36>0.20),(f'過去 36 個月最熱 20%',D.tr36>=q),('過去 36 個月年化 <0%',D.tr36<0)]
R['A']=[st(mk.fillna(False),l) for l,mk in conds]
for s in R['A']: print(f"{s['label']:<16} n={s['n']} ep={s['ep']} f12 {s['f12']*100:5.1f} pos {s['f12_pos']*100:3.0f}% f36 {s['f36']*100:5.1f} f60 {s['f60']*100:5.1f} (n60 {s['n60']}) P(dd20) {s['p_dd20']*100:3.0f}% {s['years'] if s['n']<200 else ''}")
R['now']={'date':str(D.index[-1]),'tr12':float(D.tr12.iloc[-1]),'tr36':float(D.tr36.iloc[-1]),'pct36':float((D.tr36.dropna()<D.tr36.iloc[-1]).mean()),'pct12':float((D.tr12.dropna()<D.tr12.iloc[-1]).mean()),'max36':float(D.tr36.max()),'max36_date':str(D.tr36.idxmax())}
print('now',R['now'])
# top tr36 episodes
s=D.tr36.dropna().sort_values(ascending=False); seen=[]
for k,val in s.items():
    if all(abs(k.year-y)>2 for y in seen): seen.append(k.year); print('hot peak',k,round(val*100,1),'f12',None if np.isnan(D.f12[k]) else round(D.f12[k]*100,1),'f36',None if np.isnan(D.f36[k]) else round(D.f36[k]*100,1))
    if len(seen)>=7: break
json.dump(R,open('tw_monthly.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o),ensure_ascii=False)
