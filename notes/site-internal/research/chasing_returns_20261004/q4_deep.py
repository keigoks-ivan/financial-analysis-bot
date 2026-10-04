import pandas as pd, numpy as np, json
from scipy.stats import spearmanr
raw=pd.read_csv('hf/edhec_A_z4ir3.csv'); raw['date']=pd.to_datetime(raw['date'],dayfirst=True)
M=raw.set_index('date')/100; M.index=M.index.to_period('M')
ZH={'Convertible Arbitrage':'可轉債套利','CTA Global':'管理期貨','Distressed Securities':'困境證券','Emerging Markets':'新興市場','Equity Market Neutral':'股票中性','Fixed Income Arbitrage':'固收套利','Global Macro':'全球宏觀','Long/Short Equity':'股票多空','Merger Arbitrage':'併購套利','Short Selling':'放空'}
TEN=list(ZH.keys())
DIR=['CTA Global','Emerging Markets','Global Macro','Long/Short Equity','Short Selling']
ARB=['Convertible Arbitrage','Distressed Securities','Equity Market Neutral','Fixed Income Arbitrage','Merger Arbitrage']
mk=pd.read_csv('mkt_monthly.csv',index_col=0); mk.index=pd.PeriodIndex(mk.index,freq='M'); mkt=mk['ret']
def jt(ret,J,K,top,score='ret',contra=False):
    lr=np.log1p(ret); form=lr.rolling(J).sum()
    if score=='sharpe': form=ret.rolling(J).mean()/ret.rolling(J).std()
    idx=ret.index; n=len(idx); picks=[]
    for t in range(n):
        f=form.iloc[t].dropna()
        if len(f)<len(ret.columns): picks.append(None); continue
        picks.append(list(f.sort_values(ascending=contra).index[:top]))
    p=pd.Series(np.nan,index=idx)
    for t in range(1,n):
        co=[picks[t-k] for k in range(1,K+1) if t-k>=0 and picks[t-k] is not None]
        if len(co)<K: continue
        p.iloc[t]=np.mean([ret.iloc[t][c].mean() for c in co])
    df=pd.DataFrame({'p':p,'avg':ret.mean(axis=1)}).dropna()
    return df
def summ(df):
    ex=df.p-df.avg; yrs=len(df)/12
    return {'y0':str(df.index.min()),'y1':str(df.index.max()),'ex_ann':ex.mean()*12,'t':ex.mean()/ex.std()*np.sqrt(len(ex)),'cagr':(1+df.p).prod()**(1/yrs)-1,'cagr_avg':(1+df.avg).prod()**(1/yrs)-1,
            'vol':df.p.std()*np.sqrt(12),'vol_avg':df.avg.std()*np.sqrt(12),'n':len(df)}
if __name__=="__main__":
    R={}
    ret=M[TEN]
    # A: J x K grid (monthly formation), top1 and top3
    grid={}
    for top in [1,3]:
        for J in [3,6,12,24]:
            for K in [1,3,6,12]:
                s=summ(jt(ret,J,K,top)); grid[f't{top}_J{J}_K{K}']=s
            print(f'top{top} J{J}',' '.join(f"K{K}:{grid[f't{top}_J{J}_K{K}']['ex_ann']*100:+.1f}(t{grid[f't{top}_J{J}_K{K}']['t']:.1f})" for K in [1,3,6,12]))
    R['grid']=grid
    # B: selection by Sharpe vs by return (J12 K12 & J12 K1), contrarian
    B={}
    for lab,kw in [('ret_top1',dict(top=1)),('ret_top3',dict(top=3)),('sharpe_top1',dict(top=1,score='sharpe')),('sharpe_top3',dict(top=3,score='sharpe')),('contra_top1',dict(top=1,contra=True)),('contra_top3',dict(top=3,contra=True))]:
        for K in [1,12]:
            s=summ(jt(ret,12,K,**kw)); B[f'{lab}_K{K}']=s; print(lab,'K',K,f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f} cagr {s['cagr']*100:.1f} vs {s['cagr_avg']*100:.1f} vol {s['vol']*100:.1f}/{s['vol_avg']*100:.1f}")
    R['B']=B
    # C: eras for J12K12 top1, J12K1 top1, sharpe top1 K12
    C={}
    for lab,kw in [('J12K12_top1',dict(J=12,K=12,top=1)),('J12K1_top1',dict(J=12,K=1,top=1)),('J12K12_top3',dict(J=12,K=12,top=3)),('sharpe_J12K12_top1',dict(J=12,K=12,top=1,score='sharpe'))]:
        df=jt(ret,**kw)
        for a,b in [('1998','2007'),('2008','2018')]:
            s=summ(df.loc[a:b]); C[f'{lab}_{a}']=s; print(lab,a,b,f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f}")
    R['C']=C
    # D: subsets
    D={}
    for lab,cols in [('directional5',DIR),('arb5',ARB),('ten_noSS',[c for c in TEN if c!='Short Selling'])]:
        for top in [1,2]:
            s=summ(jt(M[cols],12,12,top)); D[f'{lab}_top{top}']=s; print(lab,'top',top,f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f} cagr {s['cagr']*100:.1f} vs {s['cagr_avg']*100:.1f}")
    R['D']=D
    # E: rank persistence (annual calendar)
    A=(1+ret).groupby(ret.index.year).prod()-1; A=A.loc[1997:2017]
    rc={y:spearmanr(A.loc[y-1],A.loc[y]).correlation for y in range(1998,2018)}
    R['rankcorr']=rc; print('rank corr mean',np.mean(list(rc.values())), 'by era', np.mean([rc[y] for y in range(1998,2008)]), np.mean([rc[y] for y in range(2008,2018)]))
    # monthly 12m rolling ranks: corr between past-12m and next-12m ranks
    lr=np.log1p(ret); p12=lr.rolling(12).sum(); n12=lr.rolling(12).sum().shift(-12)
    rcm=[spearmanr(p12.iloc[t],n12.iloc[t]).correlation for t in range(len(ret)) if p12.iloc[t].notna().all() and n12.iloc[t].notna().all()]
    R['rankcorr_monthly']=float(np.mean(rcm)); R['rankcorr_monthly_pos']=float(np.mean(np.array(rcm)>0)); print('monthly 12->12 rank corr',np.mean(rcm),'share>0',np.mean(np.array(rcm)>0))
    # F: link to equity market direction (annual calendar top1)
    am=(1+mkt).groupby(mkt.index.year).prod()-1
    rec=[]
    for y in range(1998,2018):
        best=A.loc[y-1].idxmax(); rec.append({'year':y,'pick':best,'ex':A.loc[y,best]-A.loc[y].mean(),'mkt_prev':am[y-1],'mkt':am[y],'dir':best in DIR})
    F=pd.DataFrame(rec).set_index('year'); F['flip']=np.sign(F.mkt)!=np.sign(F.mkt_prev)
    print(F.groupby('flip').ex.agg(['mean','count'])); print(F.groupby('dir').ex.agg(['mean','count']))
    R['F']={'flip':F.groupby('flip').ex.agg(['mean','count']).to_dict(),'dir':F.groupby('dir').ex.agg(['mean','count']).to_dict()}
    # G: pick frequency
    R['pick_freq']=F.pick.value_counts().to_dict()
    json.dump(R,open('q4_deep.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (bool(o) if isinstance(o,(np.bool_,)) else float(o)))
