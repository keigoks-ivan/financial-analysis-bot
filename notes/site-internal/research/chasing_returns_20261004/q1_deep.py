import pandas as pd, numpy as np, json
from base import *
m=monthly()
lr=np.log1p(m['ret']); n=len(m)
def trail(k): return np.expm1(lr.rolling(k).sum()*(12/k)) if k>=12 else np.expm1(lr.rolling(k).sum())
def fwd(k,ann=True):
    s=lr.rolling(k).sum().shift(-k)
    return np.expm1(s*(12/k)) if (ann and k>=12) else np.expm1(s)
D=pd.DataFrame({'tr12':trail(12),'tr24':trail(24),'tr36':trail(36),'tr60':trail(60),'cape':m['cape']})
for k in [1,3,6,12,24,36,60]: D[f'f{k}']=fwd(k)
# forward max drawdown within next k months (from start value)
w=np.exp(lr.cumsum()).values
def fmdd(k):
    out=np.full(n,np.nan)
    for i in range(n-k):
        path=w[i:i+k+1]; peak=np.maximum.accumulate(path); out[i]=(path/peak-1).min()
    return out
D['dd12']=fmdd(12); D['dd36']=fmdd(36)
D['year']=D.index.year; D['era']=D['year'].map(era_of)
D.to_pickle('q1_monthly.pkl')
R={}
def episodes(mask):
    idx=np.where(mask.values)[0]
    if len(idx)==0: return 0
    return 1+int(np.sum(np.diff(idx)>12))
def stats(sub):
    o={'n':int(len(sub))}
    for k in ['f12','f36','f60']:
        v=sub[k].dropna(); o[k]=v.mean() if len(v) else np.nan; o[k+'_n']=int(len(v))
    v=sub['f12'].dropna(); o['f12_med']=v.median() if len(v) else np.nan; o['f12_pos']=(v>0).mean() if len(v) else np.nan
    v=sub['f60'].dropna(); o['f60_pos']=(v>0).mean() if len(v) else np.nan
    v=sub['dd12'].dropna(); o['p_dd10']=(v<=-0.10).mean() if len(v) else np.nan; o['p_dd20']=(v<=-0.20).mean() if len(v) else np.nan
    v=sub['dd36'].dropna(); o['dd36']=v.mean() if len(v) else np.nan; o['p_dd36_30']=(v<=-0.30).mean() if len(v) else np.nan
    return o
valid=D['tr36'].notna()
# ---- A: threshold sensitivity (monthly)
conds=[('全部月份',valid),('過去12個月>20%',D.tr12>0.20),('過去12個月>30%',D.tr12>0.30),('過去24個月年化>20%',D.tr24>0.20),
       ('過去36個月年化>15%',D.tr36>0.15),('過去36個月年化>20%',D.tr36>0.20),('過去60個月年化>15%',D.tr60>0.15),('過去60個月年化>20%',D.tr60>0.20),
       ('過去36個月年化<0%',D.tr36<0)]
A=[]
for lab,mask in conds:
    mask=mask.fillna(False)&valid; s=stats(D[mask]); s['label']=lab; s['ep']=episodes(mask); A.append(s)
R['A']=A
for s in A: print(f"{s['label']:<16} n={s['n']:4d} ep={s['ep']:3d} f12 {s['f12']*100:5.1f} med {s['f12_med']*100:5.1f} pos {s['f12_pos']*100:3.0f}% | f36 {s['f36']*100:5.1f} f60 {s['f60']*100:5.1f} pos60 {s['f60_pos']*100:3.0f}% | P(dd12<=-20) {s['p_dd20']*100:3.0f}% dd36 {s['dd36']*100:5.1f}")
# ---- B: horizon profile by tr36 quintile & tr12 quintile (global quintiles)
B={}
for tr in ['tr12','tr36']:
    sub=D[valid].copy(); sub['q']=pd.qcut(sub[tr],5,labels=False)
    prof={}
    base={k:sub[f'f{k}'].mean() for k in [1,3,6,12,24,36,60]}
    for q in range(5):
        ss=sub[sub.q==q]
        prof[q]={k:(ss[f'f{k}'].mean()) for k in [1,3,6,12,24,36,60]}
    # convert to annualized for all horizons for comparability
    def ann(v,k): return (1+v)**(12/k)-1 if k<12 else v
    B[tr]={'base':{k:ann(base[k],k) for k in base},'q':{q:{k:ann(prof[q][k],k) for k in prof[q]} for q in prof},
           'cut':[float(sub[sub.q==q][tr].min()) for q in range(5)]+[float(sub[tr].max())]}
    print(tr,'cuts',[round(c*100,1) for c in B[tr]['cut']])
    for q in range(5): print('  q',q,' '.join(f"{k}m:{(B[tr]['q'][q][k]-B[tr]['base'][k])*100:+.1f}" for k in [1,3,6,12,24,36,60]))
R['B']=B
# ---- C: eras: unconditional vs tr36 top quintile (global cut) vs tr12>20
cut36=B['tr36']['cut'][4]
C=[]
for a,b,l in ERAS+[(2009,2026,'2009–2026 QE 以後')]:
    em=(D.year>=a)&(D.year<=b)&valid
    row={'era':l,'all':stats(D[em]),'hot36':stats(D[em&(D.tr36>=cut36)]),'hot12':stats(D[em&(D.tr12>0.20)]),'ep36':episodes(em&(D.tr36>=cut36))}
    # autocorrelation measures within era (monthly obs): corr tr12 vs f12, tr36 vs f36
    e=D[em]
    row['c12']=e[['tr12','f12']].dropna().corr().iloc[0,1]; row['c36']=e[['tr36','f36']].dropna().corr().iloc[0,1]; row['c36_60']=e[['tr36','f60']].dropna().corr().iloc[0,1]
    C.append(row)
    print(f"{l:<22} all f12 {row['all']['f12']*100:5.1f} f60 {row['all']['f60']*100:5.1f} | hot36 n={row['hot36']['n']:3d} ep={row['ep36']} f12 {row['hot36']['f12']*100:5.1f} f36 {row['hot36']['f36']*100:5.1f} f60 {row['hot36']['f60']*100:5.1f} | hot12 n={row['hot12']['n']} f12 {row['hot12']['f12']*100:5.1f} | corr12 {row['c12']:.2f} corr36 {row['c36']:.2f} corr36→60 {row['c36_60']:.2f}")
R['C']=C; R['cut36']=cut36
# ---- E: CAPE cross (only months with CAPE)
E=[]
cv=D['cape'].notna()&valid
for lab,mk in [('過去36個月 前20%熱',D.tr36>=cut36),('其餘',D.tr36<cut36)]:
    for clab,cm in [('CAPE<20',D.cape<20),('CAPE 20–30',(D.cape>=20)&(D.cape<30)),('CAPE≥30',D.cape>=30)]:
        mask=(mk&cm&cv).fillna(False); s=stats(D[mask]); s['label']=lab; s['cape']=clab; s['ep']=episodes(mask); E.append(s)
        print(f"{lab} {clab}: n={s['n']} ep={s['ep']} f12 {s['f12']*100:.1f} f36 {s['f36']*100:.1f} f60 {s['f60']*100:.1f} pos60 {s['f60_pos']*100 if s['f60_pos']==s['f60_pos'] else float('nan'):.0f}% dd36 {s['dd36']*100:.1f}")
R['E']=E
# ---- F: analogs: tr36>=20% & CAPE>=30
mask=((D.tr36>=0.20)&(D.cape>=30)).fillna(False)
idx=D.index[mask]; runs=[]; start=prev=None; pos={k:i for i,k in enumerate(D.index)}
for k in idx:
    if start is None: start=k
    elif pos[k]-pos[prev]>12: runs.append((start,prev)); start=k
    prev=k
if start is not None: runs.append((start,prev))
F=[]
for a,b in runs:
    seg=D.loc[a:b]; seg=seg[(seg.tr36>=0.20)&(seg.cape>=30)]
    F.append({'start':str(a),'end':str(b),'months':int(len(seg)),'cape_max':float(seg.cape.max()),'tr36_max':float(seg.tr36.max()),
              'f12':float(seg.f12.mean()) if seg.f12.notna().any() else None,'f36':float(seg.f36.mean()) if seg.f36.notna().any() else None,
              'f60':float(seg.f60.mean()) if seg.f60.notna().any() else None,'dd36':float(seg.dd36.mean()) if seg.dd36.notna().any() else None})
    print(F[-1])
R['F']=F
cur=D.iloc[-1]; R['now']={'date':str(D.index[-1]),'tr12':cur.tr12,'tr36':cur.tr36,'tr60':cur.tr60,'cape':cur.cape}
print('now',R['now'])
# CAPE percentile
cp=D['cape'].dropna(); R['cape_pct']=float((cp<cur.cape).mean()); print('cape pct',R['cape_pct'], 'max',cp.max(), cp.idxmax())
json.dump(R,open('q1_deep.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o))
