import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
mkt,rf=mkt_monthly()
SETS={'FF10':'data/10_Industry_Portfolios.csv','FF12':'data/12_Industry_Portfolios.csv','FF17':'data/17_Industry_Portfolios.csv','FF30':'data/30_Industry_Portfolios.csv','FF49':'data/49_Industry_Portfolios.csv'}
def annual(ind):
    a=(1+ind).groupby(ind.index.year).prod()-1; cnt=ind.groupby(ind.index.year).count(); a=a.where(cnt==12); return a.dropna(how='all')
am=(1+mkt).groupby(mkt.index.year).prod()-1
e=pd.read_csv('data/etf_monthly_adj.csv',index_col=0); e.index=pd.PeriodIndex(e.index,freq='M'); e=e.loc[:'2025-12']
dec=e[e.index.month==12]; dec.index=dec.index.year; sa=dec.pct_change().loc[1999:2025]; spy=sa['SPY']; sa=sa.drop(columns='SPY')
sa.loc[:2015,'XLRE']=np.nan; sa.loc[:2018,'XLC']=np.nan
def cal(a,bench,lb,top,start=None):
    rec=[]; yrs=list(a.index)
    for i,y in enumerate(yrs):
        if i<lb: continue
        past=(1+a.loc[yrs[i-lb]:yrs[i-1]]).prod(min_count=lb)-1; cur=a.loc[y]; ok=past.notna()&cur.notna()
        p=past[ok].sort_values(ascending=False); pk=list(p.index[:top]); wk=list(p.index[-top:])
        rk=cur[ok].rank(ascending=False)
        rec.append({'year':y,'pick':pk[0],'p':cur[pk].mean(),'w':cur[wk].mean(),'b':bench.get(y,np.nan),'ew':cur[ok].mean(),'rank':rk[pk].mean(),'n':int(ok.sum())})
    R=pd.DataFrame(rec).set_index('year')
    return R[R.index>=start] if start else R
def st(R):
    ex=R.p-R.b; n=len(R)
    return {'y0':int(R.index.min()),'y1':int(R.index.max()),'n':n,'cagr':(1+R.p).prod()**(1/n)-1,'bcagr':(1+R.b).prod()**(1/n)-1,'ex':ex.mean(),'hit':(ex>0).mean(),
            't':ex.mean()/ex.std()*np.sqrt(n),'vol':R.p.std(),'bvol':R.b.std(),'worst':R.p.min(),'bworst':R.b.min(),'w_cagr':(1+R.w).prod()**(1/n)-1,'rank':R['rank'].mean(),'nsec':R.n.median()}
out={}
for lb in [1,3,5]:
    for top in [1,3]:
        R=cal(sa,spy,lb,top); out[f'SPDR_lb{lb}_top{top}']=st(R)
        if lb==1 and top==1: R.to_csv('q3v2_spdr.csv')
for k,f in SETS.items():
    a=annual(read_ff(f))
    for lb in [1,3,5]:
        for top in [1,3]:
            R=cal(a,am,lb,top,start=1928 if lb==1 else None); out[f'{k}_lb{lb}_top{top}']=st(R)
            if k=='FF10' and lb==1 and top==1: R.to_csv('q3v2_ff10.csv')
for k,v in out.items(): print(f"{k:16s} {v['y0']}-{v['y1']} CAGR {v['cagr']*100:5.1f} vs {v['bcagr']*100:5.1f} ex {v['ex']*100:+5.1f} t {v['t']:5.2f} hit {v['hit']*100:3.0f}% vol {v['vol']*100:4.1f}/{v['bvol']*100:4.1f} worst {v['worst']*100:4.0f} loserCAGR {v['w_cagr']*100:5.1f} rank {v['rank']:.1f}/{v['nsec']:.0f}")
R=pd.read_csv('q3v2_ff10.csv',index_col=0); out['ff10_rankdist']=R['rank'].value_counts().sort_index().to_dict(); print(out['ff10_rankdist'])
json.dump(out,open('q3_cal.json','w'),default=float)
