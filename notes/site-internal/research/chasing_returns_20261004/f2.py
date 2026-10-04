import pandas as pd, numpy as np, json
from base import shiller
s=shiller(); Q2=pd.read_pickle('q2_monthly.pkl')
ecy=s['ECY']; cape=s['CAPE']
d=pd.DataFrame({'ecy':ecy,'cape':cape,'gs10':s['GS10']}).join(Q2[['f10','f20','b10','b20']],how='left')
d['ex10']=d.f10-d.b10; d['ex20']=d.f20-d.b20
d['ey']=1/d.cape
# era-relative cape: ratio to trailing 360m median
d['cape_rel']=d.cape/d.cape.rolling(360,min_periods=240).median()
R={}
nowi=d.cape.last_valid_index(); now=d.loc[nowi]
R['now']={'date':str(nowi),'cape':now.cape,'ecy':now.ecy,'ey':now.ey,'cape_rel':now.cape_rel,'gs10':now.gs10}
for c in ['cape','ecy','cape_rel']:
    v=d[c].dropna(); R['pct_'+c]=float((v<now[c]).mean()) if c!='ecy' else float((v>now[c]).mean())  # for ecy, lower = more expensive -> pct of history cheaper
print('now',R['now']); print('pct cape (share of history lower)',R['pct_cape'],' ecy share of history with higher ECY (cheaper)',R['pct_ecy'],' cape_rel share lower',R['pct_cape_rel'])
print('ecy start',d.ecy.first_valid_index(), 'min ecy',d.ecy.min(), d.ecy.idxmin(), 'median',d.ecy.median())
# predictive power
def corr(x,y,a=None,b=None):
    z=d.loc[a:b,[x,y]].dropna(); 
    if x=='cape': return np.corrcoef(np.log(z[x]),z[y])[0,1],len(z)
    return z.corr().iloc[0,1],len(z)
P={}
for y in ['f10','f20','ex10','ex20']:
    for x in ['cape','ecy','cape_rel']:
        for a,b,l in [(None,None,'全期間'),('1881','1945','1881–1945'),('1946','1981','1946–1981'),('1982',None,'1982 以後')]:
            c,n=corr(x,y,a,b); P[f'{x}|{y}|{l}']={'c':c,'n':n}
for y in ['f10','ex10','f20','ex20']:
    print(y,' '.join(f"{x}:{P[f'{x}|{y}|全期間']['c']:+.2f}" for x in ['cape','ecy','cape_rel']),'| 1982+',' '.join(f"{x}:{P[f'{x}|{y}|1982 以後']['c']:+.2f}" for x in ['cape','ecy','cape_rel']))
R['pred']=P
# quintile results by ECY: forward 10y real and excess vs bonds
z=d[['ecy','f10','ex10','f20']].dropna(subset=['ecy']).copy(); z['q']=pd.qcut(z.ecy,5,labels=False)
rows=[]
for q in range(5):
    x=z[z.q==q]; rows.append({'q':q,'lo':x.ecy.min(),'hi':x.ecy.max(),'f10':x.f10.mean(),'ex10':x.ex10.mean(),'pos_ex10':(x.ex10.dropna()>0).mean(),'f20':x.f20.mean(),'n':int(x.f10.notna().sum())})
    print(q,round(x.ecy.min()*100,2),round(x.ecy.max()*100,2),'f10',round(x.f10.mean()*100,1),'ex10',round(x.ex10.mean()*100,1),'P(stock>bond)',round((x.ex10.dropna()>0).mean()*100),'n',int(x.f10.notna().sum()))
R['ecy_q']=rows; R['now_ecy_q']=int(np.searchsorted([r['hi'] for r in rows],now.ecy))
# analog: months with ECY <= now+0.5pp
an=d[(d.ecy<=now.ecy+0.005)&d.ecy.notna()]
R['ecy_analog_years']=sorted(set(int(k.year) for k in an.index))
print('ECY analog years (ECY <= now+0.5pp):',R['ecy_analog_years'])
g=an.groupby(an.index.year).agg(ecy=('ecy','mean'),cape=('cape','mean'),f10=('f10','mean'),ex10=('ex10','mean'),n=('ecy','size'))
print(g.round(3).to_string()); R['ecy_analog']=g.reset_index().rename(columns={'index':'year'}).to_dict('records')
json.dump(R,open('f2.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o),ensure_ascii=False)
