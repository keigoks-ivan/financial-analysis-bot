"""Download every public input this pipeline needs into data/, hf/, hf2/.
Taiwan inputs are committed under tw/ (TWSE blocks scripted downloads; see tw/SOURCES_TW.md).
Third-party datasets are downloaded at run time, never committed."""
import io, json, os, sys, time, zipfile, urllib.request
import numpy as np, pandas as pd
UA={'User-Agent':'Mozilla/5.0'}
def get(url, tries=4, ua=None):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':ua} if ua else UA)
            with urllib.request.urlopen(req,timeout=90) as r: return r.read()
        except Exception as e:
            if i==tries-1: raise
            time.sleep(2**(i+1))
for d in ['data','hf','hf2']: os.makedirs(d,exist_ok=True)
# --- Shiller (shillerdata.com; the file link changes when Shiller updates it)
html=get('https://shillerdata.com/').decode('utf-8','ignore')
import re
m=re.search(r'href="(//img1\.wsimg\.com/[^"]*ie_data\.xls[^"]*)"',html)
open('data/ie_data_new.xls','wb').write(get('https:'+m.group(1)))
open('data/ie_data.xls','wb').write(open('data/ie_data_new.xls','rb').read())  # v1 scripts read this name
# --- Ken French data library
for f in ['10_Industry_Portfolios','12_Industry_Portfolios','17_Industry_Portfolios','30_Industry_Portfolios','49_Industry_Portfolios','F-F_Research_Data_Factors']:
    z=zipfile.ZipFile(io.BytesIO(get(f'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{f}_CSV.zip')))
    for n in z.namelist(): open('data/'+os.path.basename(n),'wb').write(z.read(n))
# --- FRED CPI
open('data/cpi.csv','wb').write(get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS',ua='curl/8.5.0'))  # FRED drops browser-like UAs
# --- Jorda-Schularick-Taylor Macrohistory Database R6
page=get('https://www.macrohistory.net/database/').decode('utf-8','ignore')
m=re.search(r'href="(/app/download/[^"]*JSTdatasetR6\.xlsx[^"]*)"',page)
open('data/JST.xlsx','wb').write(get('https://www.macrohistory.net'+m.group(1)))
# --- Yahoo Finance monthly adjusted closes (SPY, SPDR sectors, RSP)
def yahoo(t):
    j=json.loads(get(f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=0&period2=9999999999&interval=1mo&events=div%7Csplit&includeAdjustedClose=true'))
    json.dump(j,open(f'data/yh_{t}.json','w'))
    r=j['chart']['result'][0]
    s=pd.Series(r['indicators']['adjclose'][0]['adjclose'],index=pd.to_datetime(r['timestamp'],unit='s')).dropna()
    s.index=s.index.to_period('M'); return s.groupby(level=0).last()
etfs='SPY XLB XLE XLF XLI XLK XLP XLU XLV XLY XLRE XLC'.split()
pd.DataFrame({t:yahoo(t) for t in etfs}).to_csv('data/etf_monthly_adj.csv')
yahoo('RSP')
# --- EDHEC-Risk hedge fund indices (course dataset mirror on GitHub; 1997-01..2018-11, percent)
open('hf/edhec_A_z4ir3.csv','wb').write(get('https://raw.githubusercontent.com/z4ir3/finance-courses/master/data/edhec-hedgefundindices.csv'))
e=pd.read_csv('hf/edhec_A_z4ir3.csv'); e['date']=pd.to_datetime(e['date'],dayfirst=True); e=e.set_index('date')/100
cnt=e.groupby(e.index.year).count().min(axis=1); a=(1+e).groupby(e.index.year).prod()-1; a=a[cnt==12]; a.index.name='year'
a.to_csv('hf/edhec_annual.csv')
# --- Credit Suisse Hedge Fund Index strategies (Bloomberg export committed in a public GitHub repo; second-hand)
raw=get('https://raw.githubusercontent.com/SuperSam1995/hedge-fund-ml/main/data/raw/NAVROR_full.csv').decode('utf-8','ignore')
lines=raw.splitlines(); hdr_i=[i for i,l in enumerate(lines) if l.startswith('Date,')][0]
c=pd.read_csv(io.StringIO('\n'.join(lines[hdr_i:])))
NAMES={'HEDG':'CS Hedge Fund Index (Broad)','HEDG_CVARB':'Convertible Arbitrage','HEDG_EMMKT':'Emerging Markets','HEDG_EQNTR':'Equity Market Neutral','HEDG_EVDRV':'Event Driven',
       'HEDG_DISTR':'Event Driven Distressed','HEDG_MSEVD':'Event Driven Multi-Strategy','HEDG_MRARB':'Event Driven Risk Arbitrage','HEDG_FIARB':'Fixed Income Arbitrage',
       'HEDG_GLMAC':'Global Macro','HEDG_LOSHO':'Long/Short Equity','HEDG_MGFUT':'Managed Futures','HEDG_MULTI':'Multi-Strategy'}
c['Date']=pd.to_datetime(c['Date']); c=c.set_index('Date').sort_index()
for k in c.columns: c[k]=pd.to_numeric(c[k].astype(str).str.replace('%','').str.strip(),errors='coerce')/100
c=c.rename(columns=NAMES)[list(NAMES.values())]
c=c[c.index>=pd.Timestamp('1994-01-01')]
c.index=c.index.strftime('%Y-%m-%d'); c.index.name='date'
c.to_csv('hf2/creditsuisse_monthly.csv')
print('done')
