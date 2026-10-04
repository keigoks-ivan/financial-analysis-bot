"""Q1/Q2 extras: CAPE predictive power by era, and era-relative 'hot' definition -> q12_extra.json."""
import pandas as pd, numpy as np, json
D=pd.read_pickle('q1_monthly.pkl'); Q2=pd.read_pickle('q2_monthly.pkl')
out={}
for a,b in [('1881','1945'),('1946','1981'),('1982','2016'),('2000','2016')]:
    x=Q2.loc[a:b,['cape','f10']].dropna(); c=np.corrcoef(np.log(x.cape),x.f10)[0,1]
    out[f'cape_{a}']={'corr':c,'n':len(x)}; print('CAPE vs f10 real',a,b,round(c,2),len(x))
pr=D.tr36.rolling(360,min_periods=240).apply(lambda w: (w[:-1]<w[-1]).mean(),raw=True)
D['rel']=pr
for a,b,l in [('1901','1945','1901–1945'),('1946','1981','1946–1981'),('1982','1999','1982–1999'),('2000','2026','2000–2026')]:
    e=D.loc[a:b]; h=e[e.rel>=0.8]; r=e[e.rel<0.8]
    out['rel_'+l]={'hot_f12':h.f12.mean(),'rest_f12':r.f12.mean(),'hot_f36':h.f36.mean(),'rest_f36':r.f36.mean(),'hot_f60':h.f60.mean(),'rest_f60':r.f60.mean(),'n':len(h)}
allh=D[D.rel>=0.8]; allr=D[(D.rel<0.8)&D.rel.notna()]
out['rel_all']={'hot_f12':allh.f12.mean(),'rest_f12':allr.f12.mean(),'hot_f60':allh.f60.mean(),'rest_f60':allr.f60.mean(),'hot_f36':allh.f36.mean(),'rest_f36':allr.f36.mean(),'n':len(allh)}
out['now_rel']=D.rel.iloc[-1]
json.dump(out,open('q12_extra.json','w'),default=float)
