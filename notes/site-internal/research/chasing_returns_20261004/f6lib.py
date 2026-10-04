import numpy as np, pandas as pd
def feats(r,W,H):
    lr=np.log1p(np.asarray(r,dtype=float)); n=len(lr)
    tr=np.expm1(pd.Series(lr).rolling(W).sum().values*12/W)
    cs=np.concatenate([[0],np.cumsum(lr)])
    f=np.full(n,np.nan); i=np.arange(n-H); f[:n-H]=np.expm1((cs[i+1+H]-cs[i+1])*12/H)
    return tr,f
def nw_t(y,x,lag):
    X=np.column_stack([np.ones(len(x)),x]); b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b
    XtX=np.linalg.inv(X.T@X); S=np.zeros((2,2))
    for l in range(lag+1):
        w=1 if l==0 else 1-l/(lag+1)
        G=(X[l:]*e[l:,None]).T@(X[:len(X)-l]*e[:len(X)-l,None])
        S+=w*(G if l==0 else G+G.T)
    V=XtX@S@XtX; return b[1],b[1]/np.sqrt(V[1,1])
def gap_stat(r,W,thr,H=60):
    tr,f=feats(r,W,H); ok=~np.isnan(tr)&~np.isnan(f)
    hot=(tr>=thr)&ok; rest=(~(tr>=thr))&ok
    if hot.sum()<6: return np.nan,int(hot.sum())
    return np.nanmean(f[rest])-np.nanmean(f[hot]),int(hot.sum())
def corr_TF(r,T,H=120):
    tr,f=feats(r,T,H); ok=~np.isnan(tr)&~np.isnan(f); return np.corrcoef(tr[ok],f[ok])[0,1],tr[ok],f[ok]
