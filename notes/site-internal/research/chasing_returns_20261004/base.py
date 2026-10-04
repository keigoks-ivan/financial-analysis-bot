import pandas as pd, numpy as np
D='data/'
def shiller():
    x=pd.read_excel(D+'ie_data_new.xls',sheet_name='Data',header=None).iloc[8:,:19]
    x.columns=['date','P','Dv','E','CPI','frac','GS10','rP','rD','rTRP','rE','rTRE','CAPE','_','TRCAPE','__','ECY','bondTR','rbondTR']
    x=x[pd.to_numeric(x['date'],errors='coerce').notna()].copy()
    x['date']=x['date'].astype(float); y=x['date'].astype(int); m=((x['date']-y)*100).round().astype(int)
    x.index=pd.PeriodIndex.from_fields(year=y,month=m,freq='M')
    for c in x.columns: x[c]=pd.to_numeric(x[c],errors='coerce')
    return x
def monthly():
    m=pd.read_csv('mkt_monthly.csv',index_col=0); m.index=pd.PeriodIndex(m.index,freq='M')
    s=shiller()
    m['cape']=s['CAPE']
    bond=s['bondTR']  # gross monthly total bond return (1+r)
    m['bond']=bond-1
    m['real']=(1+m['ret'])/(1+m['infl'])-1
    return m
ERAS=[(1871,1913,'1871–1913 金本位時代'),(1914,1945,'1914–1945 戰爭與大蕭條'),(1946,1981,'1946–1981 戰後到高通膨'),(1982,1999,'1982–1999 利率下行大多頭'),(2000,2026,'2000–2026 現代')]
def era_of(y):
    for a,b,l in ERAS:
        if a<=y<=b: return l
