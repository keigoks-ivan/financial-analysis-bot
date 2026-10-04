import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
mkt,rf=mkt_monthly()
SETS={'FF10':'data/10_Industry_Portfolios.csv','FF12':'data/12_Industry_Portfolios.csv','FF17':'data/17_Industry_Portfolios.csv','FF30':'data/30_Industry_Portfolios.csv','FF49':'data/49_Industry_Portfolios.csv'}
IND={k:read_ff(v) for k,v in SETS.items()}
# SPDR monthly
e=pd.read_csv('data/etf_monthly_adj.csv',index_col=0); e.index=pd.PeriodIndex(e.index,freq='M'); e=e.loc[:'2026-09']
er=e.pct_change(); spy=er['SPY']; spdr=er.drop(columns='SPY')
spdr.loc[:'2015-10','XLRE']=np.nan; spdr.loc[:'2018-06','XLC']=np.nan
def jt(ret,bench,J,K,top,skip=0,contra=False):
    """Jegadeesh-Titman: each month form on past J months (skipping `skip`), hold K months, overlapping cohorts equal-weighted."""
    lr=np.log1p(ret)
    form=lr.rolling(J,min_periods=J).sum().shift(skip)   # formation return known at end of month t
    idx=ret.index; n=len(idx)
    picks=[]
    for t in range(n):
        f=form.iloc[t]; nxt_ok=ret.iloc[t+1].notna() if t+1<n else f.notna()
        f=f[f.notna()&nxt_ok]
        if len(f)<max(5,top+2): picks.append(None); continue
        s=f.sort_values(ascending=contra)
        picks.append(list(s.index[:top]))
    port=pd.Series(np.nan,index=idx)
    for t in range(1,n):
        cohorts=[picks[t-k] for k in range(1,K+1) if t-k>=0 and picks[t-k] is not None]
        if len(cohorts)<K: continue
        r=np.mean([ret.iloc[t][c].mean() for c in cohorts])
        port.iloc[t]=r
    df=pd.DataFrame({'p':port,'b':bench.reindex(idx),'ew':ret.mean(axis=1)}).dropna()
    # turnover approx: fraction of names changed per month for K=1
    return df,picks
def summ(df,col='p',b='b'):
    ex=df[col]-df[b]
    yrs=len(df)/12
    cagr=(1+df[col]).prod()**(1/yrs)-1; bc=(1+df[b]).prod()**(1/yrs)-1
    t=ex.mean()/ex.std(ddof=1)*np.sqrt(len(ex))
    w=(1+df[col]).cumprod(); mdd=(w/w.cummax()-1).min(); wb=(1+df[b]).cumprod(); mddb=(wb/wb.cummax()-1).min()
    return {'y0':str(df.index.min()),'y1':str(df.index.max()),'cagr':cagr,'bcagr':bc,'ex_ann':ex.mean()*12,'t':t,'vol':df[col].std()*np.sqrt(12),'bvol':df[b].std()*np.sqrt(12),'mdd':mdd,'bmdd':mddb,
            'hit12':None}
R={}
# ---- A: J x K grid on FF10 top-3 and FF49 top-5 (monthly, 1927+)
grid={}
for name,top in [('FF10',3),('FF49',5)]:
    ind=IND[name]
    for J in [1,3,6,12]:
        for K in [1,3,6,12]:
            df,_=jt(ind,mkt,J,K,top,skip=0); s=summ(df.loc['1927-07':])
            grid[f'{name}_J{J}_K{K}']=s
        print(name,'J',J,' '.join(f"K{K}:{grid[f'{name}_J{J}_K{K}']['ex_ann']*100:+.1f}(t{grid[f'{name}_J{J}_K{K}']['t']:.1f})" for K in [1,3,6,12]))
R['grid']=grid
# ---- B: granularity — annual calendar top1 (formation Dec, hold 12m) == J12 K12? Use calendar version from annual data + monthly 12-1 top 20%
gran={}
for name in SETS:
    ind=IND[name]; nind=ind.shape[1]; top=max(1,round(nind*0.2))
    df,_=jt(ind,mkt,12,1,top,skip=1); s=summ(df.loc['1927-07':]); gran[name+'_mom']=s
    # calendar-year top1: only form in December, hold Jan-Dec
    gran[name+'_n']=nind; gran[name+'_top']=top
    print(name,'12-1 top',top,f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f} vol {s['vol']*100:.0f}/{s['bvol']*100:.0f} mdd {s['mdd']*100:.0f}/{s['bmdd']*100:.0f}")
df,_=jt(spdr,spy,12,1,3,skip=1); s=summ(df); gran['SPDR_mom']=s; print('SPDR 12-1 top3',s['y0'],f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f}")
df,_=jt(spdr,spy,12,12,3,skip=0); s=summ(df); gran['SPDR_J12K12']=s; print('SPDR J12K12 top3',f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f}")
R['gran']=gran
# ---- C: eras for 3 strategies: (i) calendar top1 FF10 (annual), (ii) FF10 12-1 top3 monthly, (iii) FF49 12-1 top10
ERA=[('1927','1945','1927–1945'),('1946','1981','1946–1981'),('1982','1999','1982–1999'),('2000','2026','2000–2026'),('2010','2026','2010–2026')]
def calendar(ind,bench,lb_years=1,top=1):
    a=(1+ind).groupby(ind.index.year).prod()-1; cnt=ind.groupby(ind.index.year).count().max(axis=1); a=a[cnt==12]
    ab=(1+bench).groupby(bench.index.year).prod()-1
    rec=[]
    yrs=list(a.index)
    for i,y in enumerate(yrs):
        if i<lb_years: continue
        past=(1+a.loc[yrs[i-lb_years]:yrs[i-1]]).prod()-1; cur=a.loc[y]; ok=past.notna()&cur.notna()
        p=past[ok].sort_values(ascending=False); pk=list(p.index[:top]); wk=list(p.index[-top:])
        rec.append({'year':y,'p':cur[pk].mean(),'b':ab.get(y),'w':cur[wk].mean(),'pick':pk[0]})
    return pd.DataFrame(rec).set_index('year')
strategies={
 'cal_FF10_top1': lambda: calendar(IND['FF10'],mkt,1,1),
}
eras={}
cal=calendar(IND['FF10'],mkt,1,1)
m1,_=jt(IND['FF10'],mkt,12,1,3,skip=1)
m2,_=jt(IND['FF49'],mkt,12,1,10,skip=1)
for a,b,l in ERA:
    c=cal.loc[int(a):int(b)]; ex=c.p-c.b
    r1=m1.loc[a:b]; r2=m2.loc[a:b]
    eras[l]={'cal_ex':ex.mean(),'cal_hit':(ex>0).mean(),'cal_n':len(c),'m10_ex':(r1.p-r1.b).mean()*12,'m10_t':(r1.p-r1.b).mean()/(r1.p-r1.b).std()*np.sqrt(len(r1)),
             'm49_ex':(r2.p-r2.b).mean()*12,'m49_t':(r2.p-r2.b).mean()/(r2.p-r2.b).std()*np.sqrt(len(r2))}
    print(l,{k:round(v*100,1) if 'ex' in k or 'hit' in k else (round(v,2) if isinstance(v,float) else v) for k,v in eras[l].items()})
R['eras']=eras
# SPDR eras
for a,b in [('2000','2009'),('2010','2026')]:
    df,_=jt(spdr,spy,12,1,3,skip=1); r=df.loc[a:b]; print('SPDR mom',a,b,round((r.p-r.b).mean()*1200,1))
# ---- D: rolling 10y excess (annualized) for cal FF10 top1 and m49
cal['ex']=cal.p-cal.b
roll_cal=cal['ex'].rolling(10).mean()
m2['ex']=m2.p-m2.b; roll_m49=m2['ex'].rolling(120).mean()*12
m1['ex']=m1.p-m1.b; roll_m10=m1['ex'].rolling(120).mean()*12
R['roll']={'cal':{int(k):v for k,v in roll_cal.dropna().items()},'m49':{str(k):v for k,v in roll_m49.dropna().iloc[11::12].items()},'m10':{str(k):v for k,v in roll_m10.dropna().iloc[11::12].items()}}
print('rolling cal last', roll_cal.dropna().tail(5).round(3).to_dict()); print('rolling m49 last', roll_m49.dropna().iloc[-1], 'm10 last',roll_m10.dropna().iloc[-1])
# ---- E: costs: turnover & breakeven for cal top1 (switch frequency) and monthly 12-1
sw=(cal.pick!=cal.pick.shift(1)).mean()
R['cost']={'cal_switch_rate':sw,'cal_ex':cal.ex.mean(),'cal_breakeven_bp':cal.ex.mean()/(2*sw)*1e4 if sw>0 else None}
# monthly FF10 top3 12-1 turnover
_,pk=jt(IND['FF10'],mkt,12,1,3,skip=1)
ch=[];prev=None
for p in pk:
    if p is None: prev=None; continue
    if prev is not None: ch.append(len(set(p)-set(prev))/3)
    prev=p
to=np.mean(ch)*12  # annual one-way turnover
R['cost']['m10_turnover']=to; R['cost']['m10_ex']=(m1.p-m1.b).mean()*12; R['cost']['m10_breakeven_bp']=R['cost']['m10_ex']/(2*to)*1e4
print('cost',R['cost'])
# ---- F: rank persistence: Spearman corr of annual industry returns year t vs t+1 (FF10, FF49), by era
from scipy.stats import spearmanr
def rankcorr(ind):
    a=(1+ind).groupby(ind.index.year).prod()-1; cnt=ind.groupby(ind.index.year).count().max(axis=1); a=a[cnt==12]
    out={}
    for y in a.index[1:]:
        x=a.loc[y-1]; z=a.loc[y]; ok=x.notna()&z.notna()
        out[y]=spearmanr(x[ok],z[ok]).correlation
    return pd.Series(out)
rc10=rankcorr(IND['FF10']); rc49=rankcorr(IND['FF49']); rcS=None
a=(1+spdr).groupby(spdr.index.year).prod()-1; a=a.loc[1999:2025]
rs={}
for y in range(2000,2026):
    x=a.loc[y-1];z=a.loc[y];ok=x.notna()&z.notna(); rs[y]=spearmanr(x[ok],z[ok]).correlation
rcS=pd.Series(rs)
F={}
for a_,b_,l in ERA:
    F[l]={'ff10':rc10.loc[int(a_):int(b_)].mean(),'ff49':rc49.loc[int(a_):int(b_)].mean(),'spdr':rcS.loc[int(a_):int(b_)].mean() if int(b_)>=2000 else None}
F['全期間']={'ff10':rc10.mean(),'ff49':rc49.mean(),'spdr':rcS.mean()}
print('rank corr',{k:{kk:(round(vv,3) if vv is not None else None) for kk,vv in v.items()} for k,v in F.items()})
R['rankcorr']=F
# transition: FF10 top-tercile? use rank of last year's #1 by era
ranks=[]
a10=(1+IND['FF10']).groupby(IND['FF10'].index.year).prod()-1; a10=a10[IND['FF10'].groupby(IND['FF10'].index.year).count().max(axis=1)==12]
for y in a10.index[1:]:
    best=a10.loc[y-1].idxmax(); ranks.append({'year':y,'rank':int(a10.loc[y].rank(ascending=False)[best])})
rk=pd.DataFrame(ranks).set_index('year')
R['rank_by_era']={l:rk.loc[int(a_):int(b_),'rank'].value_counts().sort_index().to_dict() for a_,b_,l in ERA}
print({l:rk.loc[int(a_):int(b_),'rank'].mean().round(2) for a_,b_,l in ERA})
# ---- G: contrarian (calendar worst) and top1 summary by granularity (calendar)
G={}
for name in SETS:
    c=calendar(IND[name],mkt,1,1); ex=c.p-c.b; exw=c.w-c.b
    G[name]={'win_ex':ex.mean(),'win_hit':(ex>0).mean(),'lose_ex':exw.mean(),'lose_hit':(exw>0).mean(),'n':len(c),
             'win_cagr':(1+c.p).prod()**(1/len(c))-1,'lose_cagr':(1+c.w).prod()**(1/len(c))-1,'mkt_cagr':(1+c.b).prod()**(1/len(c))-1}
    print(name,{k:round(v*100,1) if isinstance(v,float) else v for k,v in G[name].items()})
R['G']=G
json.dump(R,open('q3_deep.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (int(o) if isinstance(o,(np.integer,)) else float(o)))
