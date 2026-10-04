import pandas as pd, numpy as np, json
from base import monthly
m=monthly(); D=pd.read_pickle('q1_monthly.pkl')
tri=(1+m['ret']).cumprod(); bnd=(1+m['bond'].fillna(0)).cumprod()
cape=m['cape']
cape_pct=cape.expanding(min_periods=120).apply(lambda w:(w[:-1]<w[-1]).mean(),raw=True)  # no look-ahead
cut=D.tr36.quantile(0.8)
SIG={'S1 近3年年化≥20% 且 CAPE≥30':(D.tr36>=0.20)&(cape>=30),
     'S2 近3年最熱20% 且 CAPE≥當時歷史第80百分位':(D.tr36>=cut)&(cape_pct>=0.8),
     'S3 近3年最熱20% 且 CAPE≥25':(D.tr36>=cut)&(cape>=25)}
idx=list(m.index); pos={k:i for i,k in enumerate(idx)}
R={}
for name,mask in SIG.items():
    mask=mask.reindex(m.index).fillna(False)
    on=[k for k in m.index if mask[k]]
    firsts=[]; last=None
    for k in on:
        if last is None or pos[k]-pos[last]>12: firsts.append(k)
        last=k
    rows=[]
    for k in firsts:
        i=pos[k]; n=len(idx)
        path=tri.iloc[i:min(i+61,n)]/tri.iloc[i]; bpath=bnd.iloc[i:min(i+61,n)]/bnd.iloc[i]
        h=len(path)-1
        w36=path.iloc[:37]; mx=w36.max(); tmx=int(np.argmax(w36.values))
        # drawdown from the max (within 60m after the peak month)
        after=path.iloc[tmx:]; dd=(after/after.cummax()-1).min()
        below=np.where(path.values[1:]<1.0)[0]; first_below=int(below[0]+1) if len(below) else None
        # first month after which it stays above? measure: months until path first falls below 1 (signal level) after the peak
        mn=float(path.min()-1); tmn=int(np.argmin(path.values))
        r={'min60':mn,'months_to_min':tmn,'date':str(k),'cape':float(cape[k]),'tr36':float(D.tr36.get(k,np.nan)),'horizon':h,'max_gain36':float(mx-1),'months_to_max':tmx,'dd_after_peak':float(dd),
           'first_below':first_below,'r12':float(path.iloc[12]-1) if h>=12 else None,'r36':float(path.iloc[36]-1) if h>=36 else None,'r60':float(path.iloc[60]-1) if h>=60 else None,
           'b12':float(bpath.iloc[12]-1) if h>=12 else None,'b36':float(bpath.iloc[36]-1) if h>=36 else None,'b60':float(bpath.iloc[60]-1) if h>=60 else None}
        rows.append(r)
    R[name]=rows
    done=[r for r in rows if r['r60'] is not None]
    print('\n',name,'episodes',len(rows),'with 5y',len(done))
    for r in rows: print(' ',r['date'],'CAPE',round(r['cape'],1),'maxgain36',round(r['max_gain36']*100,1),'@',r['months_to_max'],'m; dd after peak',round(r['dd_after_peak']*100,1),'; below signal at m',r['first_below'],'; r12',None if r['r12'] is None else round(r['r12']*100,1),'r36',None if r['r36'] is None else round(r['r36']*100,1),'r60',None if r['r60'] is None else round(r['r60']*100,1),'min',round(r['min60']*100,1),'@',r['months_to_min'],'| bond60',None if r['b60'] is None else round(r['b60']*100,1))
    if done:
        print('  summary: median maxgain',round(np.median([r['max_gain36'] for r in done])*100,1),'median months to max',np.median([r['months_to_max'] for r in done]),
              'share stocks beat bonds 5y',np.mean([r['r60']>r['b60'] for r in done]).round(2),'median r60',round(np.median([r['r60'] for r in done])*100,1),'median b60',round(np.median([r['b60'] for r in done])*100,1),
              'share fell below signal level within 5y',np.mean([r['first_below'] is not None for r in done]).round(2))
json.dump(R,open('f5.json','w'),ensure_ascii=False,default=float)
