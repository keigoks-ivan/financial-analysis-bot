import pandas as pd, numpy as np, json
from scipy.stats import spearmanr
s=pd.read_csv('tw/tw_sector_yearend.csv',index_col=0).drop(columns=['last_session_date'])
bench=s['發行量加權股價指數']
excl=['發行量加權股價指數','未含金融指數','未含電子指數','未含金融電子指數','水泥窯製類指數','塑膠化工類指數','機電類指數','化學生技醫療類指數','電子工業類指數','綠能環保類指數','數位雲端類指數','運動休閒類指數','居家生活類指數']
sec=s.drop(columns=excl)
sec.columns=[c.replace('類指數','') for c in sec.columns]
full=s.loc[2009:2025]
r=sec.loc[2009:2025].pct_change().dropna(how='all'); b=bench.loc[2009:2025].pct_change().dropna()
print('sectors',r.shape, list(r.columns))
def cal(lb,top,contra=False):
    rec=[]; yrs=list(r.index)
    for i,y in enumerate(yrs):
        if i<lb: continue
        past=(1+r.loc[yrs[i-lb]:yrs[i-1]]).prod()-1; cur=r.loc[y]; ok=past.notna()&cur.notna()
        p=past[ok].sort_values(ascending=contra); pk=list(p.index[:top])
        rk=cur[ok].rank(ascending=False)
        rec.append({'year':y,'pick':' / '.join(pk),'p':cur[pk].mean(),'b':b[y],'ew':cur[ok].mean(),'rank':rk[pk].mean(),'n':int(ok.sum()),'prev':p.iloc[0]})
    return pd.DataFrame(rec).set_index('year')
out={}
for lb in [1,3]:
    for top in [1,3]:
        for contra in [False,True]:
            R=cal(lb,top,contra); ex=R.p-R.b; n=len(R)
            k=f"lb{lb}_top{top}{'_contra' if contra else ''}"
            out[k]={'y0':int(R.index.min()),'y1':int(R.index.max()),'n':n,'cagr':(1+R.p).prod()**(1/n)-1,'bcagr':(1+R.b).prod()**(1/n)-1,'ex':ex.mean(),'hit':(ex>0).mean(),'t':ex.mean()/ex.std()*np.sqrt(n),'rank':R['rank'].mean(),'nsec':R.n.median(),'ewcagr':(1+R.ew).prod()**(1/n)-1}
            print(k,f"{out[k]['y0']}-{out[k]['y1']} CAGR {out[k]['cagr']*100:.1f} vs TAIEX {out[k]['bcagr']*100:.1f} (EW sectors {out[k]['ewcagr']*100:.1f}) ex {out[k]['ex']*100:+.1f} t {out[k]['t']:.2f} hit {out[k]['hit']*100:.0f}% rank {out[k]['rank']:.1f}/{out[k]['nsec']:.0f}")
            if k=='lb1_top1': R.to_csv('tw_sector_lb1.csv'); print(R.assign(p=R.p*100,b=R.b*100,prev=R.prev*100)[['pick','prev','p','b','rank','n']].round(1).to_string())
rc={y:spearmanr(r.loc[y-1],r.loc[y],nan_policy='omit').correlation for y in r.index[1:]}
out['rankcorr']=float(np.nanmean(list(rc.values()))); print('rank corr mean',out['rankcorr'])
# 2026 YTD: last year's (2025) best sector vs TAIEX
y26=(sec.loc[2026]/sec.loc[2025]-1).dropna(); b26=bench.loc[2026]/bench.loc[2025]-1
best25=r.loc[2025].idxmax(); out['ytd2026']={'best2025':best25,'its_ytd':float(y26[best25]),'taiex_ytd':float(b26),'top_ytd':y26.sort_values(ascending=False).head(3).to_dict(),'rank_of_best25':int(y26.rank(ascending=False)[best25]),'n':int(len(y26))}
print('2026 YTD',out['ytd2026'])
# semiconductors weight context: semis return vs TAIEX by year
print((r['半導體']-b).round(3).to_dict())
json.dump(out,open('tw_sector.json','w'),default=lambda o: None if (isinstance(o,float) and np.isnan(o)) else float(o),ensure_ascii=False)
