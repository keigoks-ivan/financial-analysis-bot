import pandas as pd, numpy as np, json
from base import monthly
rng=np.random.default_rng(7)
m=monthly()
from f6lib import feats, nw_t, gap_stat, corr_TF
R={"q1":{}}
periods={'A':('1871-02','1950-12'),'B':('1951-01','2026-08')}
r_all=m['ret']
for disc,test in [('A','B'),('B','A')]:
    rd=r_all.loc[periods[disc][0]:periods[disc][1]].values; rt=r_all.loc[periods[test][0]:periods[test][1]].values
    best=None; table=[]
    for W in [12,24,36,60]:
        trd,_=feats(rd,W,60)
        for p in [0.7,0.8,0.9]:
            thr=np.nanquantile(trd,p)
            g,nh=gap_stat(rd,W,thr); gt,nht=gap_stat(rt,W,thr)
            table.append({'W':W,'p':p,'thr':thr,'gap_disc':g,'gap_test':gt,'n_test':int(nht)})
            if best is None or g>best['gap_disc']: best=table[-1]
    # significance of chosen rule in test: NW t and iid bootstrap
    W,thr=best['W'],best['thr']; tr,f=feats(rt,W,60); ok=~np.isnan(tr)&~np.isnan(f)
    dummy=(tr[ok]>=thr).astype(float); b,t=nw_t(f[ok],dummy,lag=72)
    sims=[]
    for _ in range(1000):
        rs=rng.choice(rt,size=len(rt),replace=True); g,_=gap_stat(rs,W,thr); sims.append(g)
    sims=np.array(sims); p_boot=float(np.nanmean(sims>=best['gap_test']))
    pos_cnt=sum(1 for x in table if x['gap_test']==x['gap_test'] and x['gap_test']>0)
    R['q1'][f'{disc}->{test}']={'best':best,'nw_t':t,'nw_b':b,'p_boot':p_boot,'pos_rules':pos_cnt,'n_rules':len(table),'table':table}
    print(f"Q1 discover {disc} test {test}: best W={W} p={best['p']} thr={thr*100:.1f}% gap disc {best['gap_disc']*100:.1f} -> test {best['gap_test']*100:.1f} (n {best['n_test']}) NW t(hot dummy) {t:.2f} boot p {p_boot:.3f} | rules w/ positive test gap {pos_cnt}/{len(table)}")
    for x in table: print('    W',x['W'],'p',x['p'],'thr',round(x['thr']*100,1),'disc',round(x['gap_disc']*100,1),'test',round(x['gap_test']*100,1) if x['gap_test']==x['gap_test'] else None)
# full-sample significance for main Q1 result (W=36, thr=20%)
r=r_all.values; g,nh=gap_stat(r,36,0.20); tr,f=feats(r,36,60); ok=~np.isnan(tr)&~np.isnan(f); b,t=nw_t(f[ok],(tr[ok]>=0.2).astype(float),72)
sims=np.array([gap_stat(rng.choice(r,size=len(r),replace=True),36,0.20)[0] for _ in range(1000)])
R['q1_full']={'gap':g,'nw_t':t,'p_boot':float(np.nanmean(sims>=g))}
print('Q1 full sample W36 thr20: gap',round(g*100,1),'NW t',round(t,2),'boot p',R['q1_full']['p_boot'])
# ---- Q2: trailing T years real -> forward 10y real; discovery choose T by most negative corr; test corr + NW + bootstrap
rr=m['real']
R['q2']={}
for disc,test in [('A','B'),('B','A')]:
    rd=rr.loc[periods[disc][0]:periods[disc][1]].values; rt=rr.loc[periods[test][0]:periods[test][1]].values
    res={T:corr_TF(rd,T*12)[0] for T in [5,10,15,20]}
    T=min(res,key=res.get)
    c,x,y=corr_TF(rt,T*12); b,t=nw_t(y,x,lag=144)
    sims=np.array([corr_TF(rng.choice(rt,size=len(rt),replace=True),T*12)[0] for _ in range(500)])
    p=float(np.mean(sims<=c))
    tests={TT:corr_TF(rt,TT*12)[0] for TT in [5,10,15,20]}
    R['q2'][f'{disc}->{test}']={'disc_corrs':res,'T':T,'test_corr':c,'nw_t':t,'p_boot':p,'test_all':tests,'boot_q05':float(np.quantile(sims,0.05))}
    print(f"Q2 discover {disc}: corrs {{{', '.join(f'{k}:{v:+.2f}' for k,v in res.items())}}} -> T={T}y; test corr {c:+.2f} NW t {t:.2f} boot p {p:.3f} (null 5% quantile {np.quantile(sims,0.05):+.2f}); test all T {{{', '.join(f'{k}:{v:+.2f}' for k,v in tests.items())}}}")
json.dump(R,open('f6.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else (int(o) if isinstance(o,np.integer) else float(o)))
