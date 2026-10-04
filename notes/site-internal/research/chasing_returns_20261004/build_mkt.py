import pandas as pd, numpy as np, json
D='data/'
# --- Shiller 1871-1926 monthly total return
x=pd.read_excel(D+'ie_data.xls',sheet_name='Data',header=None).iloc[8:,:5]
x.columns=['date','P','Dv','E','CPI']
x=x[pd.to_numeric(x['date'],errors='coerce').notna()].copy()
x['date']=x['date'].astype(float)
x['y']=x['date'].astype(int); x['m']=((x['date']-x['y'])*100).round().astype(int)
x['ym']=pd.PeriodIndex.from_fields(year=x['y'],month=x['m'],freq='M')
x=x.set_index('ym')
P=x['P'].astype(float); Dv=x['Dv'].astype(float)
sh=(P+Dv/12)/P.shift(1)-1
# --- French market 1926-07..
ff=pd.read_csv(D+'F-F_Research_Data_Factors.csv',skiprows=4,nrows=1205,index_col=0)
ff=ff[ff.index.astype(str).str.strip().str.len()==6]
ff.index=pd.PeriodIndex([f"{s.strip()[:4]}-{s.strip()[4:]}" for s in ff.index.astype(str)],freq='M')
ff=ff.astype(float)/100
mk=ff['Mkt-RF']+ff['RF']
r=pd.concat([sh[sh.index<pd.Period('1926-07','M')].dropna(),mk])
r.name='ret'
# CPI: Shiller pre-1913, FRED after
cpi=pd.read_csv(D+'cpi.csv'); cpi.index=pd.PeriodIndex(cpi['observation_date'],freq='M'); cpi=pd.to_numeric(cpi['CPIAUCNS'],errors='coerce')
cpi=np.exp(np.log(cpi).interpolate())  # 2025-10 CPI not published (US gov shutdown) -> log-interpolated
scpi=x['CPI'].astype(float)
cpi_all=pd.concat([scpi[scpi.index<pd.Period('1913-01','M')]*(cpi.iloc[0]/scpi[pd.Period('1913-01','M')]),cpi])
infl=cpi_all.pct_change()
df=pd.DataFrame({'ret':r,'infl':infl}).dropna()
df.to_csv('mkt_monthly.csv')
print(df.head(3)); print(df.tail(3)); print(len(df))
# annual
a=(1+df).groupby(df.index.year).prod()-1
a['real']=(1+a['ret'])/(1+a['infl'])-1
cnt=df.groupby(df.index.year).size()
a=a[cnt==12]
a.to_csv('mkt_annual.csv')
print(a.tail(8))
# sanity: compare a few years to known S&P total returns
for y in [1929,1931,1974,1987,2000,2008,2013,2022,2023,2024,2025]: print(y, round(a.loc[y,'ret']*100,1))
