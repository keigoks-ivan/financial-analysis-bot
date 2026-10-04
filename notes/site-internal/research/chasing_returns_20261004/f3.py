import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
f='data/49_Industry_Portfolios.csv'
vw=read_ff(f,'Average Value Weighted Returns -- Monthly'); ew=read_ff(f,'Average Equal Weighted Returns -- Monthly')
# number of firms (monthly) — read raw (values not /100)
def read_raw(fn,section):
    lines=open(fn).read().splitlines(); i=[k for k,l in enumerate(lines) if section in l][0]
    hdr=[h.strip() for h in lines[i+1].split(',')[1:]]; rows=[]
    for l in lines[i+2:]:
        if not l.strip(): break
        p=l.split(','); rows.append([p[0].strip()]+[float(v) for v in p[1:]])
    df=pd.DataFrame(rows,columns=['d']+hdr).set_index('d'); df.index=pd.PeriodIndex([f"{s[:4]}-{s[4:]}" for s in df.index],freq='M'); return df
if __name__=="__main__":
    nf=read_raw(f,'Number of Firms in Portfolios'); sz=read_raw(f,'Average Firm Size')
    nf=nf.where(nf>0); ewm=(ew*nf).sum(axis=1,min_count=1)/nf.where(ew.notna()).sum(axis=1)
    mkt,rf=mkt_monthly()
    D=pd.read_pickle('q1_monthly.pkl')
    lv=np.log1p(mkt); le=np.log1p(ewm)
    spread36=np.expm1(lv.rolling(36).sum()/3)-np.expm1(le.rolling(36).sum()/3)  # VW minus EW annualized
    D['spread36']=spread36
    D['ew36']=np.expm1(le.rolling(36).sum()/3)
    R={}
    print('EW vs VW full-period CAGR', ((1+ewm.loc['1927':]).prod()**(12/len(ewm.loc['1927':]))-1), ((1+mkt.loc['1927':]).prod()**(12/len(mkt.loc['1927':]))-1))
    cut=D.tr36.quantile(0.8)
    hot=D[(D.tr36>=cut)&D.spread36.notna()].copy()
    hot['nq']=pd.qcut(hot.spread36,3,labels=['寬（等權跟上或領先）','中間','窄（市值加權大幅領先）'])
    pos={k:i for i,k in enumerate(D.index)}
    for lab,x in hot.groupby('nq',observed=True):
        ii=sorted(pos[k] for k in x.index); ep=1+int(np.sum(np.diff(ii)>12))
        R[str(lab)]={'lo':x.spread36.min(),'hi':x.spread36.max(),'n':len(x),'ep':ep,'f12':x.f12.mean(),'f36':x.f36.mean(),'f60':x.f60.mean(),'pos60':(x.f60.dropna()>0).mean(),'dd36':x.dd36.mean(),'p20':(x.dd12.dropna()<=-0.2).mean(),
                     'years':sorted(set(k.year for k in x.index))}
        print(lab,round(x.spread36.min()*100,1),round(x.spread36.max()*100,1),'n',len(x),'ep',ep,'f12',round(x.f12.mean()*100,1),'f36',round(x.f36.mean()*100,1),'f60',round(x.f60.mean()*100,1),'pos60',round((x.f60.dropna()>0).mean()*100),'dd36',round(x.dd36.mean()*100,1), R[str(lab)]['years'])
    # all months: narrow (top quintile spread) vs rest regardless of hot
    a=D[D.spread36.notna()].copy(); a['sq']=pd.qcut(a.spread36,5,labels=False)
    for q in range(5):
        x=a[a.sq==q]; R[f'allq{q}']={'lo':x.spread36.min(),'hi':x.spread36.max(),'f12':x.f12.mean(),'f60':x.f60.mean(),'n':len(x)}
        print('all q',q,round(x.spread36.min()*100,1),round(x.spread36.max()*100,1),'f12',round(x.f12.mean()*100,1),'f60',round(x.f60.mean()*100,1))
    now=D.spread36.dropna(); R['now']={'date':str(now.index[-1]),'spread36':float(now.iloc[-1]),'pct':float((now<now.iloc[-1]).mean()),'tr36':float(D.tr36.iloc[-1]),'ew36':float(D.ew36.dropna().iloc[-1])}
    print('now',R['now'])
    # narrowest episodes historically
    top=now.sort_values(ascending=False); seen=[]
    for k,v in top.items():
        if all(abs(k.year-y)>3 for y in seen): seen.append(k.year); print('narrow peak',k,round(v*100,1))
        if len(seen)>=8: break
    R['narrow_peaks']=seen
    # modern check RSP vs SPY
    e=pd.read_csv('data/etf_monthly_adj.csv',index_col=0); e.index=pd.PeriodIndex(e.index,freq='M')
    import subprocess
    json.dump(R,open('f3.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (int(o) if isinstance(o,np.integer) else float(o)),ensure_ascii=False)
    D[['spread36','ew36']].to_pickle('f3_series.pkl')
