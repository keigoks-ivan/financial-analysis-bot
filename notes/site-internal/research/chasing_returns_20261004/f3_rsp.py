"""Follow-up 3 modern check: SPY vs equal-weight RSP, trailing 36-month spread -> f3_rsp.json."""
import json, pandas as pd, numpy as np
j=json.load(open('data/yh_RSP.json'))['chart']['result'][0]
s=pd.Series(j['indicators']['adjclose'][0]['adjclose'],index=pd.to_datetime(j['timestamp'],unit='s')).dropna(); s.index=s.index.to_period('M'); s=s.groupby(level=0).last()
e=pd.read_csv('data/etf_monthly_adj.csv',index_col=0); e.index=pd.PeriodIndex(e.index,freq='M'); spy=e['SPY']
d=pd.DataFrame({'rsp':s,'spy':spy}).dropna().loc[:'2026-09']
r36=(d/d.shift(36))**(1/3)-1; sp=(r36.spy-r36.rsp).dropna()
print('spread',sp.iloc[-1],'pct',(sp<sp.iloc[-1]).mean())
json.dump({'spread':float(sp.iloc[-1]),'pct':float((sp<sp.iloc[-1]).mean()),'max':float(sp.max()),'max_date':str(sp.idxmax()),'spy3':float(r36.spy.iloc[-1]),'rsp3':float(r36.rsp.iloc[-1]),'start':str(d.index[0])},open('f3_rsp.json','w'))
