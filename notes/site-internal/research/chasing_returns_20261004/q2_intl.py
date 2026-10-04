import pandas as pd, numpy as np, json
j=pd.read_excel('data/JST.xlsx')
j=j[j.eq_tr.notna()&j.cpi.notna()][['iso','country','year','eq_tr','cpi']].copy()
out=[]; per={}
for iso,g in j.groupby('iso'):
    g=g.set_index('year').sort_index()
    g=g.reindex(range(g.index.min(),g.index.max()+1))
    infl=g.cpi/g.cpi.shift(1)-1
    rr=np.log((1+g.eq_tr)/(1+infl))
    t10=np.expm1(rr.rolling(10).sum()/10); f10=np.expm1(rr.rolling(10).sum().shift(-10)/10); f20=np.expm1(rr.rolling(20).sum().shift(-20)/20)
    t5=np.expm1(rr.rolling(5).sum()/5); f5=np.expm1(rr.rolling(5).sum().shift(-5)/5)
    d=pd.DataFrame({'t10':t10,'f10':f10,'f20':f20,'t5':t5,'f5':f5}); d['iso']=iso; d['year']=d.index
    out.append(d)
    s=d[['t10','f10']].dropna(); s2=d[['t10','f20']].dropna()
    per[iso]={'n10':len(s),'c10':s.corr().iloc[0,1] if len(s)>10 else None,'c20':s2.corr().iloc[0,1] if len(s2)>10 else None}
P=pd.concat(out,ignore_index=True)
nonus=P[P.iso!='USA']
R={'per':per}
for lab,df in [('nonUS',nonus),('all',P)]:
    s=df.dropna(subset=['t10']).copy(); s['q']=pd.qcut(s.t10,5,labels=False)
    rows=[]
    for q in range(5):
        x=s[s.q==q]; rows.append({'q':q,'lo':x.t10.min(),'hi':x.t10.max(),'f10':x.f10.mean(),'f20':x.f20.mean(),'pos10':(x.f10.dropna()>0).mean(),'pos20':(x.f20.dropna()>0).mean(),'n10':int(x.f10.notna().sum()),'n20':int(x.f20.notna().sum())})
    R[lab]=rows
    c10=s[['t10','f10']].dropna().corr().iloc[0,1]; c20=s[['t10','f20']].dropna().corr().iloc[0,1]; c5=s[['t5','f5']].dropna().corr().iloc[0,1]
    R[lab+'_corr']={'c10':c10,'c20':c20,'c5':c5}
    print(lab, 'corr t10-f10',round(c10,2),'t10-f20',round(c20,2),'t5-f5',round(c5,2))
    for r in rows: print('  q',r['q'],round(r['lo']*100,1),round(r['hi']*100,1),'f10',round(r['f10']*100,1),'pos10',round(r['pos10']*100),'f20',round(r['f20']*100,1),'pos20',round(r['pos20']*100),r['n10'],r['n20'])
    # post-1950 only
    s2=s[s.year>=1950]; print('  post1950 corr t10-f10',round(s2[['t10','f10']].dropna().corr().iloc[0,1],2),'t10-f20',round(s2[['t10','f20']].dropna().corr().iloc[0,1],2))
    R[lab+'_post1950']={'c10':s2[['t10','f10']].dropna().corr().iloc[0,1],'c20':s2[['t10','f20']].dropna().corr().iloc[0,1]}
neg=sum(1 for k,v in per.items() if v['c10'] is not None and v['c10']<0)
print('countries with negative c10:',neg,'of',sum(1 for v in per.values() if v['c10'] is not None))
print({k:(round(v['c10'],2),round(v['c20'],2) if v['c20'] is not None else None) for k,v in per.items()})
R['neg_count']=neg; R['ncountries']=sum(1 for v in per.values() if v['c10'] is not None)
json.dump(R,open('q2_intl.json','w'),default=float)
