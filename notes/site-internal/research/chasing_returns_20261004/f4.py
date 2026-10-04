import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
from f3 import read_raw
def read_bm(fn):
    lines=open(fn).read().splitlines(); i=[k for k,l in enumerate(lines) if 'Value-Weighted Average of BE/ME' in l][0]
    hdr=[h.strip() for h in lines[i+1].split(',')[1:]]; rows=[]
    for l in lines[i+2:]:
        if not l.strip() or 'Copyright' in l: break
        p=l.split(','); rows.append([int(p[0])]+[float(v) for v in p[1:]])
    df=pd.DataFrame(rows,columns=['y']+hdr).set_index('y'); return df.mask(df<=-99)
mkt,rf=mkt_monthly()
am=(1+mkt).groupby(mkt.index.year).prod()-1
if __name__=="__main__":
    out={}
    for name,fn in [('FF10','data/10_Industry_Portfolios.csv'),('FF49','data/49_Industry_Portfolios.csv')]:
        vw=read_ff(fn); bm=read_bm(fn); nf=read_raw(fn,'Number of Firms in Portfolios'); sz=read_raw(fn,'Average Firm Size')
        cap=(nf.where(nf>0)*sz.where(sz>0))
        capdec=cap[cap.index.month==12]; capdec.index=capdec.index.year  # Dec t
        a=(1+vw).groupby(vw.index.year).prod()-1; cnt=vw.groupby(vw.index.year).count(); a=a.where(cnt==12)
        # market BE/ME for label t: weights cap at Dec t-1
        w=capdec.shift(1).reindex(bm.index)
        mbm=(bm*w).sum(axis=1,min_count=1)/w.where(bm.notna()).sum(axis=1)
        rel=np.log(bm.div(mbm,axis=0))   # >0 cheaper than market, <0 more expensive
        lr=np.log1p(a).sub(np.log1p(am).reindex(a.index),axis=0)  # relative log return
        rows=[]
        yrs=[y for y in a.index if y>=1931 and y<=2025]
        for t in yrs:
            tr5=lr.loc[t-4:t].sum(min_count=5)
            f1=lr.loc[t+1] if t+1 in lr.index else pd.Series(np.nan,index=lr.columns)
            f3=lr.loc[t+1:t+3].sum(min_count=3) if t+3<=lr.index.max() else pd.Series(np.nan,index=lr.columns)
            rb=rel.loc[t] if t in rel.index else pd.Series(np.nan,index=lr.columns)
            for c in lr.columns:
                rows.append({'y':t,'ind':c,'tr5':tr5[c],'rb':rb[c],'f1':f1[c],'f3':f3[c]})
        P=pd.DataFrame(rows).dropna(subset=['tr5','rb'])
        # leaders: top trailing 5y each year
        P['rank5']=P.groupby('y').tr5.rank(ascending=False)
        L=P[P.rank5==1].copy()
        # relative valuation of leader vs its own cross-section: percentile of rb within year (low = expensive)
        P['rb_pct']=P.groupby('y').rb.rank(pct=True)
        L=L.merge(P[['y','ind','rb_pct']],on=['y','ind'])
        L['exp']=pd.qcut(L.rb,3,labels=['最貴三分之一','中間','最便宜三分之一'])
        res={}
        for lab,x in L.groupby('exp',observed=True):
            res[str(lab)]={'n':len(x),'rb_lo':float(np.exp(x.rb.min())),'rb_hi':float(np.exp(x.rb.max())),'f1':float(np.expm1(x.f1.mean())),'f3':float(np.expm1(x.f3.mean()/3)),'p_f3pos':float((x.f3.dropna()>0).mean()),'p_f1pos':float((x.f1.dropna()>0).mean())}
            print(name,lab,res[str(lab)])
        # panel regression fwd3 ~ tr5 + rb  (all industries)
        Z=P.dropna(subset=['f3'])
        X=np.column_stack([np.ones(len(Z)),Z.tr5,Z.rb]); b=np.linalg.lstsq(X,Z.f3,rcond=None)[0]
        print(name,'panel f3 ~ tr5 + rb:',b.round(3),'n',len(Z))
        # among high-momentum industries (top 20% tr5): split by rb
        H=Z[Z.groupby('y').tr5.rank(pct=True)>=0.8].copy(); H['e']=pd.qcut(H.rb,2,labels=['較貴','較便宜'])
        hm={str(k):{'f3':float(np.expm1(v.f3.mean()/3)),'p':float((v.f3>0).mean()),'n':len(v)} for k,v in H.groupby('e',observed=True)}
        print(name,'top20% momentum split',hm)
        cur=L[L.y==L.y.max()].iloc[0]; allrb=L.rb
        out[name]={'leaders':res,'coef':list(b),'hm':hm,'current':{'y':int(cur.y),'ind':cur.ind,'rel_bm':float(np.exp(cur.rb)),'pct_among_leaders':float((allrb<cur.rb).mean()),'tr5':float(np.expm1(cur.tr5/5))}}
        print(name,'current leader',out[name]['current'])
        # list of most expensive leaders historically
        ex=L.sort_values('rb').head(8)[['y','ind','rb','f1','f3']]; ex['relbm']=np.exp(ex.rb); ex['f3a']=np.expm1(ex.f3/3); ex['f1a']=np.expm1(ex.f1)
        print(ex[['y','ind','relbm','f1a','f3a']].round(3).to_string())
        out[name]['most_exp']=ex[['y','ind','relbm','f1a','f3a']].to_dict('records')
    json.dump(out,open('f4.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (int(o) if isinstance(o,np.integer) else float(o)),ensure_ascii=False)
