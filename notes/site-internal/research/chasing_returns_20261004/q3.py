import pandas as pd, numpy as np, json
def read_annual(fn):
    lines=open(fn).read().splitlines()
    i=[k for k,l in enumerate(lines) if 'Average Value Weighted Returns -- Annual' in l][0]
    hdr=lines[i+1].split(',')[1:]
    rows=[]
    for l in lines[i+2:]:
        if not l.strip(): break
        p=l.split(','); rows.append([int(p[0])]+[float(v) for v in p[1:]])
    df=pd.DataFrame(rows,columns=['year']+[h.strip() for h in hdr]).set_index('year')/100
    return df.replace(-0.9999,np.nan)
mkt=pd.read_csv('mkt_annual.csv',index_col=0)['ret']
def backtest(ind,bench,lookback=1,top=1,start=None):
    yrs=list(ind.index)
    rec=[]
    for i,y in enumerate(yrs):
        if i<lookback: continue
        past=(1+ind.loc[yrs[i-lookback]:yrs[i-1]]).prod()-1
        past=past.dropna()
        cur=ind.loc[y]
        avail=past.index[cur[past.index].notna()]
        past=past[avail]
        picks=past.sort_values(ascending=False).index[:top]
        r=cur[picks].mean()
        rank_next=cur[avail].rank(ascending=False)[picks].mean()
        rec.append({'year':y,'pick':','.join(picks),'ret':r,'bench':bench.get(y,np.nan),'ew':cur[avail].mean(),'rank_next':rank_next,'nsec':len(avail),
                    'worst_ret':cur[past.sort_values().index[:top]].mean()})
    R=pd.DataFrame(rec).set_index('year')
    if start: R=R[R.index>=start]
    return R
def stats(R,col='ret',b='bench'):
    ex=R[col]-R[b]
    cagr=(1+R[col]).prod()**(1/len(R))-1; bc=(1+R[b]).prod()**(1/len(R))-1
    t=ex.mean()/(ex.std(ddof=1)/np.sqrt(len(ex)))
    return {'n':len(R),'y0':int(R.index.min()),'y1':int(R.index.max()),'mean':R[col].mean(),'bmean':R[b].mean(),'cagr':cagr,'bcagr':bc,'ex_mean':ex.mean(),'hit':(ex>0).mean(),'t':t,'vol':R[col].std(),'bvol':R[b].std(),'worst':R[col].min(),'bworst':R[b].min(),'avg_rank_next':R['rank_next'].mean(),'nsec':R['nsec'].median()}
res={}
for name,fn in [('FF10','data/10_Industry_Portfolios.csv'),('FF12','data/12_Industry_Portfolios.csv'),('FF17','data/17_Industry_Portfolios.csv'),('FF30','data/30_Industry_Portfolios.csv')]:
    ind=read_annual(fn)
    for lb in [1,3]:
        for top in [1,3]:
            R=backtest(ind,mkt,lb,top)
            s=stats(R); s2=stats(R,'ret','ew')
            res[f'{name}_lb{lb}_top{top}']={'vs_mkt':s,'vs_ew':s2}
            print(f"{name} lb{lb} top{top}: {s['y0']}-{s['y1']} n={s['n']} CAGR {s['cagr']*100:.1f} vs mkt {s['bcagr']*100:.1f} | ex {s['ex_mean']*100:+.1f} t={s['t']:.2f} hit {s['hit']*100:.0f}% | vs EW ex {s2['ex_mean']*100:+.1f} t={s2['t']:.2f} | vol {s['vol']*100:.1f} vs {s['bvol']*100:.1f} | worst {s['worst']*100:.0f} vs {s['bworst']*100:.0f} | rank next {s['avg_rank_next']:.1f}/{s['nsec']:.0f}")
            if name=='FF10' and lb==1 and top==1:
                R.to_csv('q3_ff10_lb1_top1.csv')
                # sub-period
                for a,b in [(1927,1963),(1964,1999),(2000,2025)]:
                    Rs=R.loc[a:b]; ss=stats(Rs); print(f"    {a}-{b}: ex {ss['ex_mean']*100:+.1f} hit {ss['hit']*100:.0f}% cagr {ss['cagr']*100:.1f} vs {ss['bcagr']*100:.1f}")
                # rank distribution
                print('    next-year rank dist:',R['rank_next'].value_counts().sort_index().to_dict())
                print('    contrarian (worst last yr) mean',R['worst_ret'].mean()*100,'cagr',((1+R['worst_ret']).prod()**(1/len(R))-1)*100)
            if name=='FF10' and lb==1 and top==3: R.to_csv('q3_ff10_lb1_top3.csv')
json.dump(res,open('q3_res.json','w'),default=float)
# ---- SPDR sector ETFs
e=pd.read_csv('data/etf_monthly_adj.csv',index_col=0); e.index=pd.PeriodIndex(e.index,freq='M')
dec=e[e.index.month==12]; dec.index=dec.index.year
ann=dec.pct_change().loc[1999:2025]
spy=ann['SPY']; sec=ann.drop(columns='SPY')
# XLRE first full year 2016, XLC 2019
sec.loc[:2015,'XLRE']=np.nan; sec.loc[:2018,'XLC']=np.nan
print(sec.round(3).to_string())
for lb in [1,3]:
    for top in [1,3]:
        R=backtest(sec,spy,lb,top); s=stats(R); s2=stats(R,'ret','ew')
        print(f"SPDR lb{lb} top{top}: {s['y0']}-{s['y1']} n={s['n']} CAGR {s['cagr']*100:.1f} vs SPY {s['bcagr']*100:.1f} | ex {s['ex_mean']*100:+.1f} t={s['t']:.2f} hit {s['hit']*100:.0f}% | vs EW {s2['ex_mean']*100:+.1f} | rank next {s['avg_rank_next']:.1f}/{s['nsec']:.0f}")
        res[f'SPDR_lb{lb}_top{top}']={'vs_mkt':s,'vs_ew':s2}
        if lb==1 and top==1:
            R.to_csv('q3_spdr_lb1_top1.csv'); print(R[['pick','ret','bench','rank_next','nsec']].assign(ret=lambda d:d.ret*100,bench=lambda d:d.bench*100).round(1).to_string())
json.dump(res,open('q3_res.json','w'),default=float)
sec.to_csv('spdr_annual.csv'); spy.to_csv('spy_annual.csv')
