import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
from f3 import read_raw
from f4 import read_bm
mkt,rf=mkt_monthly(); am=(1+mkt).groupby(mkt.index.year).prod()-1
fn='data/10_Industry_Portfolios.csv'
vw=read_ff(fn); bm=read_bm(fn); nf=read_raw(fn,'Number of Firms in Portfolios'); sz=read_raw(fn,'Average Firm Size')
cap=(nf.where(nf>0)*sz.where(sz>0)); capdec=cap[cap.index.month==12]; capdec.index=capdec.index.year
a=(1+vw).groupby(vw.index.year).prod()-1; cnt=vw.groupby(vw.index.year).count(); a=a.where(cnt==12)
w=capdec.reindex([y-1 for y in bm.index]); w.index=bm.index; mbm=(bm*w).sum(axis=1,min_count=1)/w.where(bm.notna()).sum(axis=1)
rel=np.log(bm.div(mbm,axis=0)); lr=np.log1p(a).sub(np.log1p(am).reindex(a.index),axis=0)
# market cap share of HiTec
share=capdec.div(capdec.sum(axis=1),axis=0)
H=pd.DataFrame({'relbm':np.exp(rel['HiTec']),'share':share['HiTec'].reindex(rel.index)})
H['tr5']=np.expm1(lr['HiTec'].rolling(5).sum()/5).reindex(H.index); H['tr10']=np.expm1(lr['HiTec'].rolling(10).sum()/10).reindex(H.index)
f3=lr['HiTec'].rolling(3).sum().shift(-3); f5=lr['HiTec'].rolling(5).sum().shift(-5)
H['f3']=np.expm1(f3/3).reindex(H.index); H['f5']=np.expm1(f5/5).reindex(H.index)
print(H.loc[[1968,1972,1980,1983,1999,2000,2007,2014,2020,2021,2023,2024,2025,2026]].round(3).to_string())
H['q']=pd.qcut(H.relbm,4,labels=['最貴 25%','次貴','次便宜','最便宜 25%'])
g=H.groupby('q',observed=True).agg(lo=('relbm','min'),hi=('relbm','max'),f3=('f3','mean'),f5=('f5','mean'),n=('f3','count'))
print(g.round(3).to_string())
now=H.loc[2026]; print('HiTec now relbm pct (share of history cheaper=higher):',(H.relbm.dropna()>now.relbm).mean())
out={'hitec_now':{'relbm':float(now.relbm),'share':float(H.share.dropna().iloc[-1]),'share_year':int(H.share.dropna().index[-1]),'tr5':float(H.tr5.dropna().iloc[-1]),'tr10':float(H.tr10.dropna().iloc[-1]),'pct_cheaper':float((H.relbm.dropna()>now.relbm).mean())},
     'hitec_q':g.reset_index().to_dict('records'),
     'hitec_years':H.loc[[1968,1972,1980,1983,1999,2000,2007,2014,2020,2021,2023,2024,2025,2026]].reset_index().rename(columns={'index':'y'}).to_dict('records')}
# general rule across FF49: tr10 top 20% & rel B/M most expensive 20% -> f3, f5 relative
fn='data/49_Industry_Portfolios.csv'
vw=read_ff(fn); bm=read_bm(fn); nf=read_raw(fn,'Number of Firms in Portfolios'); sz=read_raw(fn,'Average Firm Size')
cap=(nf.where(nf>0)*sz.where(sz>0)); capdec=cap[cap.index.month==12]; capdec.index=capdec.index.year
a=(1+vw).groupby(vw.index.year).prod()-1; cnt=vw.groupby(vw.index.year).count(); a=a.where(cnt==12)
w=capdec.reindex([y-1 for y in bm.index]); w.index=bm.index; mbm=(bm*w).sum(axis=1,min_count=1)/w.where(bm.notna()).sum(axis=1)
rel=np.log(bm.div(mbm,axis=0)); lr=np.log1p(a).sub(np.log1p(am).reindex(a.index),axis=0)
tr10=lr.rolling(10,min_periods=10).sum(); f3=lr.rolling(3,min_periods=3).sum().shift(-3); f5=lr.rolling(5,min_periods=5).sum().shift(-5)
rows=[]
for y in rel.index:
    if y not in tr10.index: continue
    for c in lr.columns:
        rows.append({'y':y,'ind':c,'tr10':tr10.loc[y,c],'rb':rel.loc[y,c],'f3':f3.loc[y,c] if y in f3.index else np.nan,'f5':f5.loc[y,c] if y in f5.index else np.nan,'cap':capdec.loc[y,c] if y in capdec.index else np.nan})
P=pd.DataFrame(rows).dropna(subset=['tr10','rb'])
P['mom']=P.groupby('y').tr10.rank(pct=True); P['val']=P.groupby('y').rb.rank(pct=True)
grid={}
for ml,mm in [('過去 10 年前 20%',P.mom>=0.8),('其餘',P.mom<0.8)]:
    for vl,vm in [('最貴 20%',P.val<=0.2),('中間 60%',(P.val>0.2)&(P.val<0.8)),('最便宜 20%',P.val>=0.8)]:
        x=P[mm&vm]; grid[f'{ml}|{vl}']={'n3':int(x.f3.notna().sum()),'f3':float(np.expm1(x.f3.mean()/3)),'p3':float((x.f3.dropna()>0).mean()),'f5':float(np.expm1(x.f5.mean()/5)),'p5':float((x.f5.dropna()>0).mean())}
        print(ml,vl,{k:round(v,3) for k,v in grid[f'{ml}|{vl}'].items()})
out['grid49']=grid
json.dump(out,open('f4b.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (int(o) if isinstance(o,np.integer) else float(o)),ensure_ascii=False)
print(out['hitec_now'])
