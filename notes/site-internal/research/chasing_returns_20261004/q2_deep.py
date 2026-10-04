import pandas as pd, numpy as np, json
from base import *
m=monthly(); n=len(m)
lr=np.log1p(m['real']); lb=np.log1p(m['bond']-m['infl']).where(m['bond'].notna())  # approx real bond: (1+b)/(1+i)-1
lb=np.log((1+m['bond'])/(1+m['infl']))
def tr(k): return np.expm1(lr.rolling(k).sum()*12/k)
def fw(s,k): return np.expm1(s.rolling(k).sum().shift(-k)*12/k)
D=pd.DataFrame(index=m.index)
for y in [5,10,15,20]: D[f'tr{y}']=tr(12*y)
for y in [5,10,15,20]: D[f'f{y}']=fw(lr,12*y); D[f'b{y}']=fw(lb,12*y)
D['cape']=m['cape']; D['year']=D.index.year
R={}
# A: correlation matrix (monthly starts, overlapping)
A={}
for t in [5,10,15,20]:
    for f in [5,10,15,20]:
        s=D[[f'tr{t}',f'f{f}']].dropna(); A[f'{t}_{f}']={'c':s.corr().iloc[0,1],'n':len(s)}
R['A']=A
print('corr matrix'); print(pd.DataFrame({t:{f:round(A[f'{t}_{f}']['c'],2) for f in [5,10,15,20]} for t in [5,10,15,20]}).T)
# B: quintile by tr10 → distribution of f10, f20
v=D['tr10'].notna(); sub=D[v].copy(); sub['q']=pd.qcut(sub.tr10,5,labels=False); cuts=[sub[sub.q==q].tr10.min() for q in range(5)]+[sub.tr10.max()]
R['cuts10']=cuts
B=[]
for q in range(5):
    s=sub[sub.q==q]; row={'q':q}
    for h in [5,10,20]:
        x=s[f'f{h}'].dropna()
        row[h]={'mean':x.mean(),'p10':x.quantile(.1),'med':x.median(),'p90':x.quantile(.9),'min':x.min(),'pos':(x>0).mean(),'gt5':(x>0.05).mean(),'n':len(x)}
    B.append(row)
    print(q,[round(c*100,1) for c in cuts[q:q+2]],{h:(round(row[h]['mean']*100,1),round(row[h]['p10']*100,1),round(row[h]['pos']*100),round(row[h]['gt5']*100)) for h in [5,10,20]})
R['B']=B
# C: eras of start date (global quintile cut: hot = q4, cold = q0)
C=[]
for a,b,l in [(1881,1913,'1881–1913'),(1914,1945,'1914–1945'),(1946,1981,'1946–1981'),(1982,2016,'1982 以後')]:
    e=sub[(sub.year>=a)&(sub.year<=b)]
    row={'era':l}
    for h in [10,20]:
        x=e[[f'f{h}','tr10','q']].dropna()
        row[h]={'all':x[f'f{h}'].mean(),'hot':x[x.q==4][f'f{h}'].mean() if (x.q==4).any() else None,'cold':x[x.q==0][f'f{h}'].mean() if (x.q==0).any() else None,
                'nhot':int((x.q==4).sum()),'ncold':int((x.q==0).sum()),'corr':x[['tr10',f'f{h}']].corr().iloc[0,1] if len(x)>24 else None,'n':len(x)}
    C.append(row); print(l,{h:{k:(round(v*100,1) if isinstance(v,float) and k not in('corr',) else (round(v,2) if k=='corr' and v is not None else v)) for k,v in row[h].items()} for h in [10,20]})
R['C']=C
# D: DCA vs lump sum (real), monthly contributions of 1 for H years; IRR by start quintile
def irr_dca(start,H):
    k=12*H; r=m['real'].values[start:start+k]
    if len(r)<k: return np.nan
    # terminal value of contributing 1 at start of each month
    tv=0.0
    for x in r: tv=(tv+1)*(1+x)
    # solve monthly IRR: sum (1+g)^(k-i) for i in 0..k-1 = tv
    lo,hi=-0.05,0.05
    for _ in range(60):
        g=(lo+hi)/2; val=((1+g)**np.arange(k,0,-1)).sum()
        if val>tv: hi=g
        else: lo=g
    return (1+g)**12-1
idx=list(D.index)
dca={10:[],20:[]}
for i in range(len(idx)):
    for H in [10,20]:
        dca[H].append(irr_dca(i,H) if i%3==0 else np.nan)  # every quarter to save time
D['dca10']=dca[10]; D['dca20']=dca[20]
sub=D[v].copy(); sub['q']=pd.qcut(sub.tr10,5,labels=False)
DC=[]
for q in range(5):
    s=sub[sub.q==q]; row={'q':q}
    for H in [10,20]:
        x=s[[f'dca{H}',f'f{H}']].dropna(); row[H]={'dca':x[f'dca{H}'].mean(),'lump':x[f'f{H}'].mean(),'dca_min':x[f'dca{H}'].min(),'lump_min':x[f'f{H}'].min(),'n':len(x)}
    DC.append(row); print('DCA q',q,{H:(round(row[H]['dca']*100,1),round(row[H]['lump']*100,1),round(row[H]['dca_min']*100,1),round(row[H]['lump_min']*100,1)) for H in [10,20]})
R['DCA']=DC
# spread hot-cold
for H in [10,20]: print('spread',H,'dca',round((DC[0][H]['dca']-DC[4][H]['dca'])*100,1),'lump',round((DC[0][H]['lump']-DC[4][H]['lump'])*100,1))
# E: vs bonds
E=[]
for q in range(5):
    s=sub[sub.q==q]; row={'q':q}
    for H in [10,20]:
        x=s[[f'f{H}',f'b{H}']].dropna(); d=x[f'f{H}']-x[f'b{H}']; row[H]={'stock':x[f'f{H}'].mean(),'bond':x[f'b{H}'].mean(),'ex':d.mean(),'p_stock_win':(d>0).mean(),'n':len(x)}
    E.append(row); print('bond q',q,{H:(round(row[H]['stock']*100,1),round(row[H]['bond']*100,1),round(row[H]['p_stock_win']*100)) for H in [10,20]})
R['E']=E
# F: CAPE 2-way (tr10 hot = top quintile)
hot=sub.q==4
F=[]
for lab,hm in [('前 10 年最熱 20%',hot),('其餘 80%',~hot)]:
    for cl,cm in [('CAPE<15',sub.cape<15),('CAPE 15–25',(sub.cape>=15)&(sub.cape<25)),('CAPE≥25',sub.cape>=25)]:
        s=sub[hm&cm]; row={'tr':lab,'cape':cl}
        for H in [10,20]:
            x=s[f'f{H}'].dropna(); row[H]={'mean':x.mean() if len(x) else None,'pos':(x>0).mean() if len(x) else None,'n':len(x)}
        row['n']=len(s); F.append(row); print(lab,cl,'n',len(s),{H:(round(row[H]['mean']*100,1) if row[H]['mean'] is not None else None,row[H]['n']) for H in [10,20]})
R['F']=F
# G: analogs now: tr10>=10% & CAPE>=28
mk=(D.tr10>=0.10)&(D.cape>=28)
G=D[mk.fillna(False)][['tr10','cape','f10','f20']]
g=G.groupby(G.index.year).agg(tr10=('tr10','mean'),cape=('cape','mean'),f10=('f10','mean'),f20=('f20','mean'),n=('cape','size'))
print(g.round(3)); R['G']=g.reset_index().to_dict('records')
R['now']={'tr10':float(D.tr10.iloc[-1]),'tr20':float(D.tr20.iloc[-1]),'cape':float(D.cape.iloc[-1])}
print(R['now'])
D.to_pickle('q2_monthly.pkl')
json.dump(R,open('q2_deep.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o))
