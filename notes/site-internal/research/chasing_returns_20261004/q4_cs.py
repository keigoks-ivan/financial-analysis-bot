import pandas as pd, numpy as np, json
from scipy.stats import spearmanr
from q4_deep import jt, summ
m=pd.read_csv('hf2/creditsuisse_monthly.csv',index_col=0); m.index=pd.PeriodIndex(pd.to_datetime(m.index),freq='M')
ZH={'Convertible Arbitrage':'可轉債套利','Emerging Markets':'新興市場','Equity Market Neutral':'股票中性','Event Driven Distressed':'困境證券','Event Driven Multi-Strategy':'事件驅動多策略','Event Driven Risk Arbitrage':'併購套利','Fixed Income Arbitrage':'固收套利','Global Macro':'全球宏觀','Long/Short Equity':'股票多空','Managed Futures':'管理期貨','Multi-Strategy':'多策略'}
S=list(ZH.keys())
ret=m[S].loc['1994-04':'2021-12']  # Multi-Strategy starts after early NaNs
DIR=['Emerging Markets','Global Macro','Long/Short Equity','Managed Futures']
A=(1+ret).groupby(ret.index.year).prod()-1; cnt=ret.groupby(ret.index.year).count().min(axis=1); A=A[cnt==12]
print('annual years',A.index.min(),A.index.max())
R={}
def cal(A,lb=1,top=1,contra=False):
    rec=[]; yrs=list(A.index)
    for i,y in enumerate(yrs):
        if i<lb: continue
        past=(1+A.loc[yrs[i-lb]:yrs[i-1]]).prod()-1; p=past.sort_values(ascending=contra); pk=list(p.index[:top])
        rk=A.loc[y].rank(ascending=False)
        rec.append({'year':y,'pick':pk[0],'prev':p.iloc[0],'p':A.loc[y,pk].mean(),'avg':A.loc[y].mean(),'rank':rk[pk].mean(),'n':len(A.columns)})
    return pd.DataFrame(rec).set_index('year')
C={}
for lb in [1,3]:
    for top in [1,3]:
        c=cal(A,lb,top); ex=c.p-c.avg; w=cal(A,lb,top,contra=True)
        s={'y0':int(c.index.min()),'y1':int(c.index.max()),'mean':c.p.mean(),'avg':c.avg.mean(),'ex':ex.mean(),'hit':(ex>0).mean(),'t':ex.mean()/ex.std()*np.sqrt(len(ex)),
           'cagr':(1+c.p).prod()**(1/len(c))-1,'cagr_avg':(1+c.avg).prod()**(1/len(c))-1,'worst':w.p.mean(),'n':len(c)}
        for a,b in [(1995,2007),(2008,2021)]:
            cc=c.loc[a:b]; e=cc.p-cc.avg; s[f'ex_{a}']=e.mean(); s[f'hit_{a}']=(e>0).mean()
        C[f'lb{lb}_top{top}']=s
        print(f"CS lb{lb} top{top} {s['y0']}-{s['y1']}: pick {s['mean']*100:.1f} vs avg {s['avg']*100:.1f} ex {s['ex']*100:+.1f} t {s['t']:.2f} hit {s['hit']*100:.0f}% cagr {s['cagr']*100:.1f}/{s['cagr_avg']*100:.1f} | 95-07 {s['ex_1995']*100:+.1f} 08-21 {s['ex_2008']*100:+.1f} | contra {s['worst']*100:.1f}")
        if lb==1 and top==1:
            c.to_csv('q4_cs_lb1_top1.csv'); print(c.assign(prev=c.prev*100,p=c.p*100,avg=c.avg*100).round(1).to_string()); print('rank dist',c['rank'].value_counts().sort_index().to_dict())
R['cal']=C
# monthly JT grid top1/top3
G={}
for top in [1,3]:
    for J in [3,6,12]:
        for K in [1,12]:
            s=summ(jt(ret,J,K,top)); G[f't{top}_J{J}_K{K}']=s
        print('CS JT top',top,'J',J,' '.join(f"K{K}:{G[f't{top}_J{J}_K{K}']['ex_ann']*100:+.1f}(t{G[f't{top}_J{J}_K{K}']['t']:.1f})" for K in [1,12]))
R['grid']=G
# eras monthly J12K12 top1 / J6K1 top3
for lab,kw in [('J12K12_top1',dict(J=12,K=12,top=1)),('J6K1_top3',dict(J=6,K=1,top=3))]:
    df=jt(ret,**kw)
    for a,b in [('1995','2007'),('2008','2021')]:
        s=summ(df.loc[a:b]); R[f'era_{lab}_{a}']=s; print('CS',lab,a,b,f"ex {s['ex_ann']*100:+.1f} t {s['t']:.1f}")
# rank corr
rc={y:spearmanr(A.loc[y-1],A.loc[y]).correlation for y in A.index[1:]}
R['rankcorr']=float(np.mean(list(rc.values()))); R['rankcorr_2008']=float(np.mean([rc[y] for y in rc if y>=2008])); print('CS rank corr',R['rankcorr'],R['rankcorr_2008'])
# directional
c=pd.read_csv('q4_cs_lb1_top1.csv',index_col=0); c['dir']=c.pick.isin(DIR); c['ex']=c.p-c.avg
R['dir']=c.groupby('dir').ex.agg(['mean','count']).to_dict(); print(c.groupby('dir').ex.agg(['mean','count']))
json.dump(R,open('q4_cs.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o))
