import pandas as pd, numpy as np, json
from base import monthly
from f6lib import feats, gap_stat, corr_TF, nw_t
rng=np.random.default_rng(11)
m=monthly(); out=json.load(open('f6.json'))
# null means for Q1 gap and Q2 corr (full sample)
r=m['ret'].values; sims=np.array([gap_stat(rng.choice(r,size=len(r),replace=True),36,0.20)[0] for _ in range(1000)])
out['q1_full']['null_mean']=float(np.nanmean(sims)); out['q1_full']['null_q95']=float(np.nanquantile(sims,0.95))
print('Q1 full null mean',round(np.nanmean(sims)*100,2),'q95',round(np.nanquantile(sims,0.95)*100,2))
rr=m['real'].values
for T,H in [(10,120),(10,240),(15,180)]:
    c,_,_=corr_TF(rr,T*12,H); s=np.array([corr_TF(rng.choice(rr,size=len(rr),replace=True),T*12,H)[0] for _ in range(500)])
    out[f'q2_full_{T}_{H}']={'corr':c,'null_mean':float(s.mean()),'null_q05':float(np.quantile(s,0.05)),'p':float(np.mean(s<=c))}
    print('Q2 full T',T,'H',H/12,'corr',round(c,2),'null mean',round(s.mean(),2),'null 5%',round(np.quantile(s,0.05),2),'p',round(np.mean(s<=c),3))
json.dump(out,open('f6.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o))
