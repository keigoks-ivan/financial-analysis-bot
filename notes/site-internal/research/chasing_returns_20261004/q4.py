import pandas as pd, numpy as np, json, sys, glob
def run(df, label, exclude=('Funds Of Funds',), lbs=(1,3), tops=(1,3)):
    df=df.drop(columns=[c for c in df.columns if c in exclude],errors='ignore')
    yrs=list(df.index); res={}
    for lb in lbs:
        for top in tops:
            rec=[]
            for i,y in enumerate(yrs):
                if i<lb: continue
                past=((1+df.loc[yrs[i-lb]:yrs[i-1]]).prod()-1)
                cur=df.loc[y]; avail=[c for c in df.columns if pd.notna(cur[c]) and pd.notna(past[c])]
                p=past[avail].sort_values(ascending=False)
                picks=list(p.index[:top]); worst=list(p.index[-top:])
                rk=cur[avail].rank(ascending=False)
                rec.append({'year':y,'pick':' / '.join(picks),'ret':cur[picks].mean(),'avg':cur[avail].mean(),'med':cur[avail].median(),
                            'rank':rk[picks].mean(),'n':len(avail),'worst_ret':cur[worst].mean(),'prev':p.iloc[0]})
            R=pd.DataFrame(rec).set_index('year'); ex=R.ret-R.avg
            s={'n':len(R),'y0':int(R.index.min()),'y1':int(R.index.max()),'mean':R.ret.mean(),'avg':R.avg.mean(),'ex':ex.mean(),
               'hit':(ex>0).mean(),'t':ex.mean()/(ex.std(ddof=1)/np.sqrt(len(ex))),'rank':R['rank'].mean(),'nstrat':int(R.n.median()),
               'cagr':(1+R.ret).prod()**(1/len(R))-1,'cagr_avg':(1+R.avg).prod()**(1/len(R))-1,'worst_mean':R.worst_ret.mean(),
               'below_median':(R.ret<R.med).mean()}
            res[f'lb{lb}_top{top}']=s
            print(f"{label} lb{lb} top{top}: {s['y0']}-{s['y1']} n={s['n']} pick mean {s['mean']*100:.1f} vs avg {s['avg']*100:.1f} ex {s['ex']*100:+.1f} t={s['t']:.2f} hit {s['hit']*100:.0f}% | rank {s['rank']:.1f}/{s['nstrat']} | CAGR {s['cagr']*100:.1f} vs {s['cagr_avg']*100:.1f} | contrarian {s['worst_mean']*100:.1f}")
            if lb==1 and top==1:
                R.to_csv(f'q4_{label}_lb1_top1.csv'); print(R.assign(ret=R.ret*100,avg=R.avg*100,prev=R.prev*100)[['pick','prev','ret','avg','rank','n']].round(1).to_string())
                print('rank dist', R['rank'].value_counts().sort_index().to_dict())
    return res
if __name__=='__main__':
    out={}
    for f in sys.argv[1:]:
        df=pd.read_csv(f,index_col=0); lab=f.split('/')[-1].replace('_annual.csv','')
        out[lab]=run(df,lab)
    json.dump(out,open('q4_res.json','w'),default=float)
