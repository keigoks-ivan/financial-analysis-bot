import pandas as pd, numpy as np
def read_ff(fn, section='Average Value Weighted Returns -- Monthly'):
    lines=open(fn).read().splitlines()
    i=[k for k,l in enumerate(lines) if section in l][0]
    hdr=[h.strip() for h in lines[i+1].split(',')[1:]]
    rows=[]
    for l in lines[i+2:]:
        if not l.strip(): break
        p=l.split(','); rows.append([p[0].strip()]+[float(v) for v in p[1:]])
    df=pd.DataFrame(rows,columns=['d']+hdr).set_index('d')/100
    df=df.mask(df<=-0.99)
    if 'Monthly' in section: df.index=pd.PeriodIndex([f"{s[:4]}-{s[4:]}" for s in df.index],freq='M')
    else: df.index=df.index.astype(int)
    return df
def mkt_monthly():
    ff=pd.read_csv('data/F-F_Research_Data_Factors.csv',skiprows=4,nrows=1205,index_col=0)
    ff=ff[ff.index.astype(str).str.strip().str.len()==6]
    ff.index=pd.PeriodIndex([f"{s.strip()[:4]}-{s.strip()[4:]}" for s in ff.index.astype(str)],freq='M')
    ff=ff.astype(float)/100
    return ff['Mkt-RF']+ff['RF'], ff['RF']
