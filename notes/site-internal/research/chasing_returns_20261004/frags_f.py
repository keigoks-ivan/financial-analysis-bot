import json, numpy as np
from charts import grouped_columns, columns_with_ref, esc
from frags_v2 import table, tr, td, tdraw, pc, shade
L=lambda f: json.load(open(f))
f1=L('f1.json'); e10=L('f1_e10.json'); e10b=L('f1_e10b.json'); f2=L('f2.json'); f3=L('f3.json'); f3r=L('f3_rsp.json'); f4=L('f4.json'); f4b=L('f4b.json'); f5=L('f5.json'); f6=L('f6.json'); f6c=L('f6c.json')
F={}
# ---- F1
cq=['CAPE 小幅上升或下降','CAPE 中度上升','CAPE 大幅上升']; lab=['CAPE 小升或下降','CAPE 中度上升','CAPE 大幅上升']
vals=[f1['cq_'+k]['f60']*100 for k in cq]
F['f1_c']=columns_with_ref(lab,[round(v,1) for v in vals],9.6,'',fmt=lambda v:f"{v:+.1f}%",tips=[f"{l}（每年 {f1['cq_'+k]['range'][0]*100:.1f}%～{f1['cq_'+k]['range'][1]*100:.1f}%）｜之後 5 年年化 {f1['cq_'+k]['f60']*100:.1f}%，5 年後為正 {f1['cq_'+k]['pos60']*100:.0f}%，{f1['cq_'+k]['ep']} 段" for l,k in zip(lab,cq)],aria='熱行情依 CAPE 上升速度分組的之後 5 年報酬',ylab_suffix='%',height=240)
rows=[]
for l,k in zip(lab,cq):
    x=f1['cq_'+k]; rows.append(tr(l,[tdraw(f"{x['range'][0]*100:.1f}%～{x['range'][1]*100:.1f}%"),tdraw(f"{x['n']}／{x['ep']}"),td(x['f12']),td(x['f60']),tdraw(f"{x['pos60']*100:.0f}%"),td(x['dd36'])]))
for k,l in [('盈餘驅動（EPS 成長 > 本益比擴張）','以本益比區分｜盈餘驅動'),('估值驅動（本益比擴張 > EPS 成長）','以本益比區分｜估值驅動')]:
    x=f1[k]; rows.append(tr(l,[tdraw('—'),tdraw(f"{x['n']}／{x['ep']}"),td(x['f12']),td(x['f60']),tdraw(f"{x['pos60']*100:.0f}%"),td(x['dd36'])]))
F['f1_t']=table(['熱行情的成因','CAPE 每年上升幅度','月數／段數','之後 12 個月','之後 5 年年化','5 年後為正','36 個月內平均最大回撤'],rows)
rows=[]
for k,l in [('E/E10≥1.5','實質盈餘 ≥ 10 年平均的 1.5 倍'),('1.2–1.5','1.2～1.5 倍'),('<1.2','低於 1.2 倍')]:
    x=e10b[k]; rows.append(tr(l,[tdraw(str(x['n'])),td(x['fE3']),tdraw(f"{x['pE3neg']*100:.0f}%"),td(x['fE5']),td(x['f60'])]))
F['f1_t2']=table(['當時的盈餘位置','月數','之後 3 年實質盈餘變化','3 年後盈餘較低的機率','之後 5 年實質盈餘變化','股票之後 5 年年化'],rows)
# ---- F2
q=f2['ecy_q']; ql=['最貴 20%','次貴','中間','次便宜','最便宜 20%']
rows=[tr(ql[r['q']],[tdraw(f"{r['lo']*100:.1f}%～{r['hi']*100:.1f}%"),td(r['f10']),td(r['ex10']),tdraw(f"{r['pos_ex10']*100:.0f}%"),td(r['f20'])]) for r in q]
F['f2_t']=table(['依超額 CAPE 殖利率分組','區間','之後 10 年實質年化','之後 10 年股票減公債','10 年股贏債的機率','之後 20 年實質年化'],rows)
P=f2['pred']; rows=[]
for x,l in [('cape','CAPE（取對數，符號反向）'),('ecy','超額 CAPE 殖利率'),('cape_rel','CAPE 相對近 30 年中位數（符號反向）')]:
    def g(y,per):
        c=P[f'{x}|{y}|{per}']['c']; c=-c if x!='ecy' else c; return f"<td{shade(c,0.9)}>{c:+.2f}</td>"
    rows.append(tr(l,[g('f10','全期間'),g('f10','1982 以後'),g('ex10','全期間'),g('ex10','1982 以後'),g('f20','全期間')]))
F['f2_t2']=table(['估值指標','→之後 10 年報酬（全期間）','→之後 10 年報酬（1982 以後）','→10 年股減債（全期間）','→10 年股減債（1982 以後）','→之後 20 年報酬'],rows)
# ---- F3
nl=['寬（等權跟上或領先）','中間','窄（市值加權大幅領先）']; nlab=['寬','中間','窄']
F['f3_c']=columns_with_ref(nlab,[round(f3[k]['f60']*100,1) for k in nl],9.6,'',fmt=lambda v:f"{v:+.1f}%",tips=[f"{k}｜市值加權減等權每年 {f3[k]['lo']*100:.1f}%～{f3[k]['hi']*100:.1f}%｜之後 5 年年化 {f3[k]['f60']*100:.1f}%，{f3[k]['ep']} 段" for k in nl],aria='熱行情依寬度分組的之後 5 年報酬',ylab_suffix='%',height=230)
rows=[tr(k,[tdraw(f"{f3[k]['lo']*100:+.1f}～{f3[k]['hi']*100:+.1f}"),tdraw(f"{f3[k]['n']}／{f3[k]['ep']}"),td(f3[k]['f12']),td(f3[k]['f36']),td(f3[k]['f60']),tdraw(f"{f3[k]['pos60']*100:.0f}%"),td(f3[k]['dd36'])]) for k in nl]
F['f3_t']=table(['熱行情的寬度','市值加權減等權（每年，百分點）','月數／段數','之後 12 個月','之後 3 年年化','之後 5 年年化','5 年後為正','36 個月內平均最大回撤'],rows)
# ---- F4
hq=f4b['hitec_q']; rows=[tr(r['q'],[tdraw(f"{r['lo']:.2f}～{r['hi']:.2f}"),td(r['f3']),td(r['f5']),tdraw(str(int(r['n'])))]) for r in hq]
F['f4_t1']=table(['科技業相對淨值市價比（越低越貴）','區間','之後 3 年相對大盤（每年）','之後 5 年相對大盤（每年）','年數'],rows)
rows=[]
for nm,l in [('FF10','10 大產業'),('FF49','49 細產業')]:
    for k in ['最貴三分之一','中間','最便宜三分之一']:
        x=f4[nm]['leaders'][k]; rows.append(tr(f"{l}｜{k}",[td(x['f1']),tdraw(f"{x['p_f1pos']*100:.0f}%"),td(x['f3']),tdraw(f"{x['p_f3pos']*100:.0f}%"),tdraw(str(x['n']))]))
F['f4_t2']=table(['近 5 年冠軍產業｜當時相對估值','隔年相對大盤','隔年贏大盤的機率','之後 3 年相對大盤（每年）','3 年贏大盤的機率','年數'],rows)
g=f4b['grid49']; rows=[]
for ml in ['過去 10 年前 20%','其餘']:
    rows.append(tr(ml,[f"<td{shade(g[f'{ml}|{vl}']['f5'],0.04)}>{g[f'{ml}|{vl}']['f5']*100:+.1f}<span class='t'>贏 {g[f'{ml}|{vl}']['p5']*100:.0f}%</span></td>" for vl in ['最貴 20%','中間 60%','最便宜 20%']]))
F['f4_t3']=table(['49 細產業｜過去 10 年相對報酬','當時最貴 20%','中間 60%','最便宜 20%'],rows)
# ---- F5
def f5rows(key):
    rows=[]
    for r in f5[key]:
        rows.append(tr(r['date'],[tdraw(f"{r['cape']:.1f}"),td(r['max_gain36'],sign=True),tdraw(f"{r['months_to_max']}"),td(r['min60']),td(r['r12'],sign=True),td(r['r60'],sign=True),td(r['b60'],sign=True)]))
    return table(['訊號首次出現','CAPE','之後 3 年內最多再漲','幾個月後到高點','5 年內最低點（相對訊號當時）','之後 1 年','之後 5 年（股票）','之後 5 年（公債）'],rows)
F['f5_t1']=f5rows('S1 近3年年化≥20% 且 CAPE≥30'); F['f5_t2']=f5rows('S2 近3年最熱20% 且 CAPE≥當時歷史第80百分位')
# ---- F6
q1=f6['q1']; rows=[]
for k,l in [('A->B','1871–1950 找規則 → 1951–2026 驗證'),('B->A','1951–2026 找規則 → 1871–1950 驗證')]:
    x=q1[k]; b=x['best']
    rows.append(tr(l,[tdraw(f"過去 {b['W']} 個月 ≥{b['thr']*100:.1f}%"),tdraw(f"{b['gap_disc']*100:+.1f}"),tdraw(f"{b['gap_test']*100:+.1f}"),tdraw('&lt;0.01' if x['p_boot']<0.01 else f"{x['p_boot']:.2f}"),tdraw(f"{x['pos_rules']}／{x['n_rules']}")]))
F['f6_t1']=table(['第 1 題：熱行情之後 5 年報酬的差距','找到的最佳規則','找規則期間的差距（百分點）','驗證期間的差距','驗證期間 p 值','12 種規則在驗證期同方向'],rows)
rows=[]
for k,l in [('A->B','1871–1950 → 1951–2026'),('B->A','1951–2026 → 1871–1950')]:
    x=f6['q2'][k]; rows.append(tr(l,[tdraw(f"前 {x['T']} 年"),tdraw(f"{x['disc_corrs'][str(x['T'])]:+.2f}"),tdraw(f"{x['test_corr']:+.2f}"),tdraw(f"{x['boot_q05']:+.2f}"),tdraw(f"{x['p_boot']:.2f}")]))
for T,H,l in [(10,120,'全期間｜前 10 年 → 後 10 年'),(10,240,'全期間｜前 10 年 → 後 20 年'),(15,180,'全期間｜前 15 年 → 後 15 年')]:
    x=f6[f'q2_full_{T}_{H}']; rows.append(tr(l,[tdraw('—'),tdraw('—'),tdraw(f"{x['corr']:+.2f}"),tdraw(f"{x['null_q05']:+.2f}"),tdraw(f"{x['p']:.2f}")]))
F['f6_t2']=table(['第 2 題：起點之前與之後報酬的相關係數','選到的回看期','找規則期間','驗證期間（或全期間）','完全隨機時的 5% 門檻','p 值'],rows)
F['f6_q3']=f6c
F['f6_q1full']=f6['q1_full']
json.dump(F,open('frags_f.json','w'),ensure_ascii=False,default=float)
print({k:len(v) if isinstance(v,str) else '' for k,v in F.items()})
