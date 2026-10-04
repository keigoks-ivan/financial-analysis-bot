import pandas as pd, numpy as np, json
from ind import read_ff, mkt_monthly
from f6lib import nw_t
rng=np.random.default_rng(3)
mkt,rf=mkt_monthly()
ind=read_ff('data/49_Industry_Portfolios.csv'); mk=mkt.reindex(ind.index)
R=ind.values; B=mk.values; T,N=R.shape
def mom(R,B,J,K,top,skip=0):
    lr=np.log1p(R)
    form=pd.DataFrame(lr).rolling(J,min_periods=J).sum().shift(skip).values
    nxt=np.vstack([~np.isnan(R[1:]),np.zeros((1,R.shape[1]),bool)])
    sc=np.where(np.isnan(form)|~nxt,-np.inf,form)
    order=np.argsort(-sc,axis=1)[:,:top]
    mask=np.zeros_like(R,dtype=bool); rows=np.arange(R.shape[0])[:,None]; mask[rows,order]=True
    valid_form=(np.isfinite(sc).sum(axis=1)>=top+2)
    mask[~valid_form]=False
    Rz=np.nan_to_num(R)
    port=np.zeros(R.shape[0]); cnt=np.zeros(R.shape[0])
    for k in range(1,K+1):
        mk_=np.zeros_like(mask); mk_[k:]=mask[:-k]
        ok=np.zeros(R.shape[0],bool); ok[k:]=valid_form[:-k]
        port+=np.where(ok,(mk_*Rz).sum(axis=1)/top,0); cnt+=ok
    p=np.where(cnt==K,port/K,np.nan)
    return p-B
idx=ind.index
A=(idx>=pd.Period('1927-07','M'))&(idx<=pd.Period('1975-12','M')); Bm=(idx>=pd.Period('1976-01','M'))
res={}
for J in [1,3,6,12]:
    for K in [1,3,6,12]:
        ex=mom(R,B,J,K,5)
        a=ex[A]; b=ex[Bm]; a=a[~np.isnan(a)]; b=b[~np.isnan(b)]
        res[(J,K)]={'disc':a.mean()*12,'disc_t':a.mean()/a.std()*np.sqrt(len(a)),'test':b.mean()*12,'test_t':b.mean()/b.std()*np.sqrt(len(b))}
best=max(res,key=lambda k:res[k]['disc'])
print('FF49 top5 grid: discover 1927-1975 -> test 1976-2026')
for k,v in res.items(): print(' J',k[0],'K',k[1],f"disc {v['disc']*100:+.1f} (t{v['disc_t']:.1f}) test {v['test']*100:+.1f} (t{v['test_t']:.1f})")
print('best in discovery',best,res[best])
# time-shuffle bootstrap in test period for best config (K=1 if best K>1 still fine): shuffle months of industry+market rows jointly
J,K=best; Rt=R[Bm]; Bt=B[Bm]; obs=res[best]['test']
sims=[]
for _ in range(300):
    perm=rng.permutation(len(Rt)); ex=mom(Rt[perm],Bt[perm],J,K,5); sims.append(np.nanmean(ex)*12)
sims=np.array(sims); p=float(np.mean(sims>=obs)); print('test-period shuffle null mean',round(sims.mean()*100,2),'q95',round(np.quantile(sims,0.95)*100,2),'p',p)
pos=sum(1 for v in res.values() if v['test']>0)
out={'grid':{f'J{k[0]}K{k[1]}':v for k,v in res.items()},'best':f'J{best[0]}K{best[1]}','best_res':res[best],'p_shuffle':p,'null_mean':float(sims.mean()),'pos_test':pos}
# reverse: discover 1976-2026, test 1927-1975
best2=max(res,key=lambda k:res[k]['test']); out['reverse']={'best':f'J{best2[0]}K{best2[1]}','disc':res[best2]['test'],'test':res[best2]['disc'],'test_t':res[best2]['disc_t']}
print('reverse: best in 1976-2026',best2,'-> 1927-1975',round(res[best2]['disc']*100,1),'t',round(res[best2]['disc_t'],1))
print('configs positive in test period',pos,'/16')
json.dump(out,open('f6c.json','w'),default=float)
