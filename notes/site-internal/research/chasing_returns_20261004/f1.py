import pandas as pd, numpy as np, json
from base import shiller
s=shiller(); D=pd.read_pickle('q1_monthly.pkl')
P=s['P']; E=s['E']; C=s['CAPE']; CPI=s['CPI']
pe=P/E
k=36
df=pd.DataFrame({'dlogP':np.log(P/P.shift(k)),'dlogE':np.log(E/E.shift(k)),'dlogPE':np.log(pe/pe.shift(k)),'dlogCAPE':np.log(C/C.shift(k)),'dlogCPI':np.log(CPI/CPI.shift(k)),'pe':pe,'E':E})
df['dlogE10r']=df.dlogP-df.dlogCAPE-df.dlogCPI   # real 10y-avg earnings growth implied
D=D.join(df,how='left')
cut=D.tr36.quantile(0.8)
hot=D[(D.tr36>=cut)&D.dlogE.notna()&(D.E>0)&(D.E.shift(36)>0)].copy()
# share of price change from multiple expansion
hot['pe_share']=hot.dlogPE/hot.dlogP
hot['val_driven']=hot.dlogPE>hot.dlogE   # more from P/E than from EPS
hot['cape_up']=hot.dlogCAPE/3   # annualized CAPE log change
R={'cut':cut}
def st(x):
    return {'n':len(x),'f12':x.f12.mean(),'f36':x.f36.mean(),'f60':x.f60.mean(),'pos60':(x.f60.dropna()>0).mean(),'dd36':x.dd36.mean(),'p20':(x.dd12.dropna()<=-0.2).mean()}
for lab,m in [('盈餘驅動（EPS 成長 > 本益比擴張）',~hot.val_driven),('估值驅動（本益比擴張 > EPS 成長）',hot.val_driven)]:
    x=hot[m]; R[lab]=st(x)
    idx=np.where(m.values)[0]; ep=1+int(np.sum(np.diff(idx)>12)) if len(idx) else 0; R[lab]['ep']=ep
    print(lab,{k:(round(v*100,1) if isinstance(v,float) else v) for k,v in R[lab].items()})
# CAPE-change terciles within hot runs
hot['cq']=pd.qcut(hot.cape_up,3,labels=['CAPE 小幅上升或下降','CAPE 中度上升','CAPE 大幅上升'])
for lab,x in hot.groupby('cq',observed=True):
    R['cq_'+str(lab)]=st(x); R['cq_'+str(lab)]['range']=(float(x.cape_up.min()),float(x.cape_up.max()))
    print(lab, round(x.cape_up.min()*100,1), round(x.cape_up.max()*100,1), {k:(round(v*100,1) if isinstance(v,float) else v) for k,v in R['cq_'+str(lab)].items()})
# all months (not only hot): regress f60 on dlogE and dlogPE (annualized) 
a=D[['f60','dlogE','dlogPE','tr36']].dropna(); a=a[np.isfinite(a.dlogE)&np.isfinite(a.dlogPE)]
X=np.column_stack([np.ones(len(a)),a.dlogE/3,a.dlogPE/3]); b=np.linalg.lstsq(X,a.f60,rcond=None)[0]
print('f60 ~ EPS growth + PE change (ann.) coef',b.round(3),'n',len(a))
R['reg']=list(b)
# current decomposition: last available E
last=E.dropna().index[-1]; t0=last-36
cur={'end':str(last),'start':str(t0),'P0':float(P[t0]),'P1':float(P[last]),'E0':float(E[t0]),'E1':float(E[last]),'PE0':float(pe[t0]),'PE1':float(pe[last]),'CAPE0':float(C[t0]),'CAPE1':float(C[last])}
cur['price_ann']=(cur['P1']/cur['P0'])**(1/3)-1; cur['eps_ann']=(cur['E1']/cur['E0'])**(1/3)-1; cur['pe_ann']=(cur['PE1']/cur['PE0'])**(1/3)-1
cur['pe_share']=np.log(cur['PE1']/cur['PE0'])/np.log(cur['P1']/cur['P0'])
print('current',cur)
R['current']=cur
# historical episodes table: first month of each hot episode (gap>12) with decomposition
hot_all=D[(D.tr36>=cut)].copy(); idx=list(hot_all.index); eps=[]; start=prev=None; pos={k:i for i,k in enumerate(D.index)}
for k in idx:
    if start is None: start=k
    elif pos[k]-pos[prev]>12: eps.append((start,prev)); start=k
    prev=k
eps.append((start,prev))
rows=[]
for a_,b_ in eps:
    seg=D.loc[a_:b_]; seg=seg[seg.tr36>=cut]
    pk=seg.tr36.idxmax(); r=D.loc[pk]
    rows.append({'start':str(a_),'end':str(b_),'peak':str(pk),'tr36':float(r.tr36),'eps_ann':float(np.expm1(r.dlogE/3)) if np.isfinite(r.dlogE) else None,'pe_ann':float(np.expm1(r.dlogPE/3)) if np.isfinite(r.dlogPE) else None,
                 'f60':float(seg.f60.mean()) if seg.f60.notna().any() else None,'f12':float(seg.f12.mean()) if seg.f12.notna().any() else None})
R['episodes']=rows
for r in rows: print(r['start'],r['end'],round(r['tr36']*100,1),'EPS',None if r['eps_ann'] is None else round(r['eps_ann']*100,1),'PE',None if r['pe_ann'] is None else round(r['pe_ann']*100,1),'f60',None if r['f60'] is None else round(r['f60']*100,1))
json.dump(R,open('f1.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (bool(o) if isinstance(o,np.bool_) else float(o)),ensure_ascii=False)
# episode counts & member years per CAPE tercile
pos={k:i for i,k in enumerate(D.index)}
for lab,x in hot.groupby('cq',observed=True):
    ii=sorted(pos[k] for k in x.index); ep=1+int(np.sum(np.diff(ii)>12))
    yrs=sorted(set(k.year for k in x.index))
    R['cq_'+str(lab)]['ep']=ep; R['cq_'+str(lab)]['years']=yrs
    print(lab,'ep',ep,yrs)
now=D.iloc[-1]; print('now cape_up (ann log)', now.dlogCAPE/3, 'dlogPE/3',now.dlogPE/3 if np.isfinite(now.dlogPE) else None)
R['now_cape_up']=float(D.dlogCAPE.dropna().iloc[-1]/3)
json.dump(R,open('f1.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (bool(o) if isinstance(o,np.bool_) else float(o)),ensure_ascii=False)
