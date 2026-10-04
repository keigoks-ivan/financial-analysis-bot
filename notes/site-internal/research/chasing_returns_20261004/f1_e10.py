"""Follow-up 1 extras: real earnings vs their 10-year average, and what happened afterwards -> f1_e10.json, f1_e10b.json."""
import pandas as pd, numpy as np, json
from base import shiller
s=shiller(); rE=s['rE']; ratio=(rE/rE.rolling(120).mean())
r=ratio.dropna()
json.dump({'now':float(r.iloc[-1]),'date':str(r.index[-1]),'pct':float((r<r.iloc[-1]).mean()),'r1929':float(r[pd.Period('1929-09','M')]),'r1999':float(r[pd.Period('1999-12','M')]),'r2007':float(r[pd.Period('2007-06','M')])},open('f1_e10.json','w'))
D=pd.read_pickle('q1_monthly.pkl')
d=pd.DataFrame({'ratio':ratio,'fE3':rE.shift(-36)/rE-1,'fE5':rE.shift(-60)/rE-1}).join(D[['f36','f60']]).dropna(subset=['ratio'])
out={}
for lab,m in [('E/E10≥1.5',d.ratio>=1.5),('1.2–1.5',(d.ratio>=1.2)&(d.ratio<1.5)),('<1.2',d.ratio<1.2)]:
    x=d[m]; out[lab]={'n':len(x),'fE3':float(x.fE3.mean()),'pE3neg':float((x.fE3.dropna()<0).mean()),'f60':float(x.f60.mean()),'fE5':float(x.fE5.mean())}
    print(lab,out[lab])
json.dump(out,open('f1_e10b.json','w'))
