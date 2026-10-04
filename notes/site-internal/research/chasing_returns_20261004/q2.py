import pandas as pd, numpy as np
T=pd.read_csv('trail_fwd_annual.csv',index_col=0)
x=pd.read_excel('data/ie_data.xls',sheet_name='Data',header=None).iloc[8:,[0,12]]
x.columns=['date','cape']; x=x[pd.to_numeric(x['date'],errors='coerce').notna()]
x['date']=x['date'].astype(float); x=x[((x['date']*100).round()%100)==12]  # December
x['year']=x['date'].astype(int); cape=x.set_index('year')['cape'].astype(float)
T['cape']=cape
print(T.loc[[2021,2023,2024,2025],['tr1','tr3','tr5','tr10','trr10','cape']])
for tr in ['trr5','trr10']:
  for h in [5,10,15,20]:
    c=f'fr{h}'; sub=T[[tr,c]].dropna()
    print(tr,c,'n',len(sub),'corr',round(sub[tr].corr(sub[c]),3))
print()
for tr in ['trr10','trr5']:
    sub=T.dropna(subset=[tr]).copy()
    sub['q']=pd.qcut(sub[tr],5,labels=['Q1最低','Q2','Q3','Q4','Q5最高'])
    agg={}
    for h in [5,10,15,20]:
        c=f'fr{h}'
        g=sub.groupby('q',observed=True)[c]
        agg[f'mean{h}']=g.mean()*100; agg[f'min{h}']=g.min()*100; agg[f'pos{h}']=g.apply(lambda v:(v.dropna()>0).mean()*100); agg[f'n{h}']=g.count()
    G=pd.DataFrame(agg); G.insert(0,'trmax',sub.groupby('q',observed=True)[tr].max()*100); G.insert(0,'trmin',sub.groupby('q',observed=True)[tr].min()*100)
    print(tr); print(G.round(1).to_string())
# CAPE vs trailing as predictor of fwd 10y real
sub=T[['trr10','cape','fr10','fr20']].dropna()
print('\nCAPE sample',sub.index.min(),sub.index.max(),len(sub))
print('corr cape-fr10',round(sub['cape'].corr(sub['fr10']),3),' trr10-fr10',round(sub['trr10'].corr(sub['fr10']),3),' cape-trr10',round(sub['cape'].corr(sub['trr10']),3))
sub2=T[['trr10','cape','fr20']].dropna(); print('corr cape-fr20',round(sub2['cape'].corr(sub2['fr20']),3),'trr10-fr20',round(sub2['trr10'].corr(sub2['fr20']),3))
# regression fr10 ~ trr10 + log(cape)
import numpy.linalg as la
X=np.column_stack([np.ones(len(sub)),sub['trr10'],np.log(sub['cape'])]); y=sub['fr10'].values
b=la.lstsq(X,y,rcond=None)[0]; print('fr10 ~ trr10 + logCAPE coef',b.round(3))
X1=np.column_stack([np.ones(len(sub)),sub['trr10']]); b1=la.lstsq(X1,y,rcond=None)[0]; r1=1-((y-X1@b1)**2).sum()/((y-y.mean())**2).sum()
X2=np.column_stack([np.ones(len(sub)),np.log(sub['cape'])]); b2=la.lstsq(X2,y,rcond=None)[0]; r2=1-((y-X2@b2)**2).sum()/((y-y.mean())**2).sum()
r3=1-((y-X@b)**2).sum()/((y-y.mean())**2).sum()
print('R2 trailing only',round(r1,3),' CAPE only',round(r2,3),' both',round(r3,3))
# overall ranges of fwd real returns
for h in [5,10,15,20]:
    v=T[f'fr{h}'].dropna(); print(h,'n',len(v),'mean',round(v.mean()*100,1),'min',round(v.min()*100,1),'max',round(v.max()*100,1),'pos',round((v>0).mean()*100,1), 'worst start', v.idxmin(),'best start',v.idxmax())
T.to_csv('trail_fwd_annual.csv')
