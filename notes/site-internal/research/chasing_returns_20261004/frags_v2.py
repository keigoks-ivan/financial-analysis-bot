import json, pandas as pd, numpy as np
from charts import grouped_columns, columns_with_ref, lines, esc
L=lambda f: json.load(open(f))
q1=L('q1_deep.json'); q1x=L('q12_extra.json'); q2=L('q2_deep.json'); q2i=L('q2_intl.json'); q3=L('q3_deep.json'); q3c=L('q3_cal.json'); q4=L('q4_deep.json'); q4cs=L('q4_cs.json'); q4o=L('q4_res.json')
OLD=L('parts_q123.json'); OLD4=L('parts_q4.json')
F={}
def pc(v,d=1,sign=False):
    if v is None or (isinstance(v,float) and np.isnan(v)): return '—'
    return f"{v*100:+.{d}f}%" if sign else f"{v*100:.{d}f}%"
def pp(v,d=1):
    if v is None: return '—'
    return f"{v*100:+.{d}f}"
def neg(v): return ' class="neg"' if (v is not None and not (isinstance(v,float) and np.isnan(v)) and v<0) else ''
def shade(v,scale):
    if v is None: return ''
    a=min(abs(v)/scale,1)*38
    var='--s1' if v>0 else '--s2'
    return f' style="background:color-mix(in srgb, var({var}) {a:.0f}%, transparent)"'
def table(head,rows,first_left=True):
    LEFT=' style="text-align:left"'
    h=''.join(f'<th scope="col"{LEFT if (i==0 and first_left) else ""}>{c}</th>' for i,c in enumerate(head))
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
def tr(th,cells): return f"<tr><th scope='row'>{th}</th>{''.join(cells)}</tr>"
def td(v,fmt=pc,**k): return f"<td{neg(v)}>{fmt(v,**k) if k else fmt(v)}</td>"
def tdraw(s): return f"<td>{s}</td>"

# ================= Q1 =================
A=q1['A']
cats=['全部月份','12個月>20%','12個月>30%','24個月>20%','36個月>20%','60個月>20%','36個月<0']
pick={'全部月份':'全部月份','12個月>20%':'過去12個月>20%','12個月>30%':'過去12個月>30%','24個月>20%':'過去24個月年化>20%','36個月>20%':'過去36個月年化>20%','60個月>20%':'過去60個月年化>20%','36個月<0':'過去36個月年化<0%'}
byl={a['label']:a for a in A}
sel=[byl[pick[c]] for c in cats]
F['q1_cA']=grouped_columns(cats,[('之後 12 個月（平均）','--s1',[s['f12']*100 for s in sel]),('之後 5 年（年化平均）','--s2',[s['f60']*100 for s in sel])],
   tips=[[f"{c}｜之後 12 個月平均 {s['f12']*100:.1f}%（中位數 {s['f12_med']*100:.1f}%、上漲機率 {s['f12_pos']*100:.0f}%）" for c,s in zip(cats,sel)],[f"{c}｜之後 5 年年化平均 {s['f60']*100:.1f}%（5 年後為正 {s['f60_pos']*100:.0f}%）" for c,s in zip(cats,sel)]],aria='不同「高報酬」定義下，之後 12 個月與 5 年的平均報酬')
rows=[]
for a in A:
    rows.append(tr(a['label'],[tdraw(f"{a['n']}"),tdraw('—' if a['label']=='全部月份' else str(a['ep'])),td(a['f12']),td(a['f12_med']),tdraw(f"{a['f12_pos']*100:.0f}%"),td(a['f36']),td(a['f60']),tdraw(f"{a['f60_pos']*100:.0f}%")]))
F['q1_tA']=table(['條件（觀察月當時）','月數','獨立段數','之後 12 個月平均','中位數','上漲機率','之後 3 年年化','之後 5 年年化','5 年後為正'],rows)
# B horizon
B=q1['B']; hz=['1','3','6','12','24','36','60']; hzl=['1 個月','3 個月','6 個月','1 年','2 年','3 年','5 年']
s12=[(B['tr12']['q']['4'][h]-B['tr12']['base'][h])*100 for h in hz]; s36=[(B['tr36']['q']['4'][h]-B['tr36']['base'][h])*100 for h in hz]
F['q1_cB']=grouped_columns(hzl,[('過去 12 個月最熱 20%','--s1',s12),('過去 36 個月最熱 20%','--s2',s36)],fmt=lambda v:f"{v:+.1f}",
   tips=[[f"過去 12 個月最熱 20% 之後 {l}：比全部月份平均 {v:+.1f} 個百分點（年化）" for l,v in zip(hzl,s12)],[f"過去 36 個月最熱 20% 之後 {l}：比全部月份平均 {v:+.1f} 個百分點（年化）" for l,v in zip(hzl,s36)]],aria='最熱的起點之後，不同期間的報酬與平均的差距',height=280)
F['q1_cuts']=(B['tr12']['cut'][4],B['tr36']['cut'][4])
# C eras
rows=[]
for r in q1['C']:
    a,h=r['all'],r['hot36']
    rows.append(tr(r['era'],[td(a['f12']),td(a['f60']),tdraw(f"{h['n']}／{r['ep36']}"),td(h['f12']),td(h['f36']),td(h['f60']),tdraw(f"{r['c36_60']:+.2f}")]))
F['q1_tC']=table(['時期','全部：之後 12 個月','全部：之後 5 年年化','熱：月數／段數','熱：之後 12 個月','熱：之後 3 年年化','熱：之後 5 年年化','相關係數（過去3年→之後5年）'],rows)
# D era-relative
rows=[]
for k,l in [('rel_1901–1945','1901–1945'),('rel_1946–1981','1946–1981'),('rel_1982–1999','1982–1999'),('rel_2000–2026','2000–2026'),('rel_all','全期間')]:
    r=q1x[k]; rows.append(tr(l,[tdraw(str(int(r['n']))),td(r['hot_f12']),td(r['rest_f12']),td(r['hot_f36']),td(r['rest_f36']),td(r['hot_f60']),td(r['rest_f60'])]))
F['q1_tD']=table(['時期','相對熱的月數','熱：之後 12 個月','其餘：之後 12 個月','熱：之後 3 年年化','其餘：之後 3 年年化','熱：之後 5 年年化','其餘：之後 5 年年化'],rows)
# E risk chart
ecats=['全部月份','12個月>20%','36個月>20%','60個月>20%','36個月<0']
es=[byl[pick[c]] for c in ecats]
F['q1_cE']=columns_with_ref(ecats,[round(s['p_dd20']*100) for s in es],es[0]['p_dd20']*100,'',fmt=lambda v:f"{v}%",tips=[f"{c}｜之後 12 個月內曾從起點下跌 20% 以上的機率 {s['p_dd20']*100:.0f}%；之後 36 個月內平均最大回撤 {s['dd36']*100:.1f}%" for c,s in zip(ecats,es)],aria='之後 12 個月內出現 20% 以上回撤的機率',ylab_suffix='%',height=240)
rows=[tr(c,[tdraw(f"{s['p_dd10']*100:.0f}%"),tdraw(f"{s['p_dd20']*100:.0f}%"),td(s['dd36']),tdraw(f"{s['p_dd36_30']*100:.0f}%")]) for c,s in zip(ecats,es)]
F['q1_tE']=table(['條件','12 個月內跌 ≥10%','12 個月內跌 ≥20%','36 個月內平均最大回撤','36 個月內跌 ≥30%'],rows)
# F CAPE cross
rows=[]
for e in q1['E']:
    rows.append(tr(f"{e['label']}｜{e['cape']}",[tdraw(f"{e['n']}／{e['ep']}"),td(e['f12']),td(e['f36']),td(e['f60']),tdraw('—' if e['f60_pos'] is None else f"{e['f60_pos']*100:.0f}%"),td(e['dd36'])]))
F['q1_tF']=table(['過去 36 個月｜當時 CAPE','月數／段數','之後 12 個月','之後 3 年年化','之後 5 年年化','5 年後為正','36 個月內平均最大回撤'],rows)
# G analogs
rows=[]
for a in q1['F']:
    rows.append(tr(f"{a['start']} 至 {a['end']}",[tdraw(str(a['months'])),tdraw(f"{a['tr36_max']*100:.1f}%"),tdraw(f"{a['cape_max']:.1f}"),td(a['f12']),td(a['f36']),td(a['f60']),td(a['dd36'])]))
F['q1_tG']=table(['期間（同時符合）','月數','過去 3 年年化最高','CAPE 最高','之後 12 個月','之後 3 年年化','之後 5 年年化','36 個月內平均最大回撤'],rows)

# ================= Q2 =================
A2=q2['A']
rows=[tr(f"過去 {t} 年",[f"<td{shade(A2[f'{t}_{f}']['c'],0.7)}>{A2[f'{t}_{f}']['c']:+.2f}</td>" for f in [5,10,15,20]]) for t in [5,10,15,20]]
F['q2_tA']=table(['起點之前的報酬','之後 5 年','之後 10 年','之後 15 年','之後 20 年'],rows)
cuts=q2['cuts10']; qn=['最冷 20%','次冷','中間','次熱','最熱 20%']
B2=q2['B']
F['q2_cB']=grouped_columns(qn,[('之後 10 年（實質年化）','--s1',[b['10']['mean']*100 for b in B2]),('之後 20 年（實質年化）','--s2',[b['20']['mean']*100 for b in B2])],
   tips=[[f"{qn[i]}（前 10 年實質年化 {cuts[i]*100:.1f}%～{cuts[i+1]*100:.1f}%）｜之後 10 年平均 {b['10']['mean']*100:.1f}%，最差 10% 的情況 {b['10']['p10']*100:.1f}%" for i,b in enumerate(B2)],
         [f"{qn[i]}｜之後 20 年平均 {b['20']['mean']*100:.1f}%，最差 10% 的情況 {b['20']['p10']*100:.1f}%" for i,b in enumerate(B2)]],aria='依起點之前 10 年報酬分五組的之後報酬',height=280)
rows=[]
for i,b in enumerate(B2):
    rows.append(tr(qn[i],[tdraw(f"{cuts[i]*100:.1f}%～{cuts[i+1]*100:.1f}%"),td(b['10']['mean']),td(b['10']['p10']),tdraw(f"{b['10']['pos']*100:.0f}%"),td(b['20']['mean']),td(b['20']['p10']),td(b['20']['min']),tdraw(f"{b['20']['gt5']*100:.0f}%")]))
F['q2_tB']=table(['起點之前 10 年','實質年化區間','之後 10 年平均','之後 10 年：較差的 10%','10 年後為正','之後 20 年平均','之後 20 年：較差的 10%','之後 20 年最差','20 年年化 >5% 的機率'],rows)
rows=[]
for c in q2['C']:
    r10,r20=c['10'],c['20']
    rows.append(tr(c['era'],[tdraw('—' if r10['corr'] is None else f"{r10['corr']:+.2f}"),tdraw('—' if r20['corr'] is None else f"{r20['corr']:+.2f}"),td(r10['cold']),td(r10['hot']),td(r20['cold']),td(r20['hot']),tdraw(f"{r10['ncold']}／{r10['nhot']}")]))
F['q2_tC']=table(['起點所在時期','相關係數（前10年→後10年）','相關係數（前10年→後20年）','最冷組：之後 10 年','最熱組：之後 10 年','最冷組：之後 20 年','最熱組：之後 20 年','冷／熱起點月數'],rows)
rows=[]
for i,d in enumerate(q2['DCA']):
    rows.append(tr(qn[i],[td(d['10']['lump']),td(d['10']['dca']),td(d['10']['dca_min']),td(d['20']['lump']),td(d['20']['dca']),td(d['20']['dca_min'])]))
F['q2_tD']=table(['起點之前 10 年','單筆：之後 10 年','定期定額：10 年','定期定額 10 年最差','單筆：之後 20 年','定期定額：20 年','定期定額 20 年最差'],rows)
rows=[]
for i,e in enumerate(q2['E']):
    rows.append(tr(qn[i],[td(e['10']['stock']),td(e['10']['bond']),tdraw(f"{e['10']['p_stock_win']*100:.0f}%"),td(e['20']['stock']),td(e['20']['bond']),tdraw(f"{e['20']['p_stock_win']*100:.0f}%")]))
F['q2_tE']=table(['起點之前 10 年','股票：之後 10 年','公債：之後 10 年','10 年股贏債的機率','股票：之後 20 年','公債：之後 20 年','20 年股贏債的機率'],rows)
rows=[]
for f in q2['F']:
    rows.append(tr(f"{f['tr']}｜{f['cape']}",[tdraw(f"{f['10']['n']}"),td(f['10']['mean']),tdraw('—' if f['10']['pos'] is None else f"{f['10']['pos']*100:.0f}%"),tdraw(f"{f['20']['n']}"),td(f['20']['mean'])]))
F['q2_tF']=table(['起點之前 10 年｜當時 CAPE','10 年樣本月數','之後 10 年實質年化','10 年後為正','20 年樣本月數','之後 20 年實質年化'],rows)
rows=[]
for k,l in [('cape_1881','1881–1945'),('cape_1946','1946–1981'),('cape_1982','1982–2016'),('cape_2000','2000–2016')]:
    rows.append(tr(l,[tdraw(f"{q1x[k]['corr']:+.2f}"),tdraw(str(int(q1x[k]['n'])))]))
F['q2_tF2']=table(['起點所在時期','CAPE（取對數）與之後 10 年實質報酬的相關係數','樣本月數'],rows)
rows=[]
for r in q2i['nonUS']:
    rows.append(tr(qn[r['q']],[tdraw(f"{r['lo']*100:.1f}%～{r['hi']*100:.1f}%"),td(r['f10']),tdraw(f"{r['pos10']*100:.0f}%"),td(r['f20']),tdraw(f"{r['pos20']*100:.0f}%"),tdraw(f"{r['n10']}")]))
F['q2_tG']=table(['起點之前 10 年（美國以外 15 國合併）','實質年化區間','之後 10 年平均','10 年後為正','之後 20 年平均','20 年後為正','國家·年 樣本'],rows)
CN={'AUS':'澳洲','BEL':'比利時','CHE':'瑞士','DEU':'德國','DNK':'丹麥','ESP':'西班牙','FIN':'芬蘭','FRA':'法國','GBR':'英國','ITA':'義大利','JPN':'日本','NLD':'荷蘭','NOR':'挪威','PRT':'葡萄牙','SWE':'瑞典','USA':'美國'}
per=q2i['per']; order=sorted(per,key=lambda k: per[k]['c10'])
F['q2_country']=''.join(f"<span class='chip'>{CN[k]} <b>{per[k]['c10']:+.2f}</b></span>" for k in order)
rows=[]
for g in q2['G']:
    rows.append(tr(str(int(g.get('year',g.get('index')))),[tdraw(f"{g['tr10']*100:.1f}%"),tdraw(f"{g['cape']:.1f}"),td(g['f10']),td(g['f20']),tdraw(str(int(g['n'])))]))
F['q2_tH']=table(['年份（符合月份平均）','前 10 年實質年化','CAPE','之後 10 年實質年化','之後 20 年實質年化','符合月數'],rows)

# ================= Q3 =================
def q3row(key,lab):
    s=q3c[key]; return tr(lab,[tdraw(f"{s['y0']}–{s['y1']}"),td(s['cagr']),td(s['bcagr']),tdraw(f"{s['hit']*100:.0f}%"),tdraw(f"{s['t']:.1f}"),tdraw(f"{s['vol']*100:.0f}% / {s['bvol']*100:.0f}%"),td(s['worst'])])
rows=[q3row('SPDR_lb1_top1','標普類股 ETF｜去年第 1 名'),q3row('SPDR_lb3_top1','標普類股 ETF｜近 3 年第 1 名'),q3row('SPDR_lb5_top1','標普類股 ETF｜近 5 年第 1 名'),q3row('SPDR_lb1_top3','標普類股 ETF｜去年前 3 名'),
      q3row('FF10_lb1_top1','10 大產業｜去年第 1 名'),q3row('FF10_lb3_top1','10 大產業｜近 3 年第 1 名'),q3row('FF10_lb5_top1','10 大產業｜近 5 年第 1 名'),q3row('FF10_lb1_top3','10 大產業｜去年前 3 名'),
      q3row('FF49_lb1_top1','49 細產業｜去年第 1 名'),q3row('FF49_lb1_top3','49 細產業｜去年前 3 名')]
F['q3_tA']=table(['做法（每年年底換一次）','期間','策略年化','大盤年化','贏大盤的年份','t 值','年波動 策略／大盤','最差一年'],rows)
rd=q3c['ff10_rankdist']; n=sum(rd.values())
F['q3_cA']=columns_with_ref([f"第 {i} 名" for i in range(1,11)],[int(rd.get(str(i),rd.get(f'{i}.0',0))) for i in range(1,11)],n/10,'',fmt=lambda v:f"{v}",
   tips=[f"去年冠軍產業隔年排第 {i} 名：{int(rd.get(str(i),rd.get(f'{i}.0',0)))} 次（共 {n} 年）" for i in range(1,11)],aria='去年冠軍產業的隔年名次',ylab_suffix=' 次',height=240)
g=q3['grid']
def gridtable(name,top):
    rows=[]
    for J in [1,3,6,12]:
        cells=[]
        for K in [1,3,6,12]:
            s=g[f'{name}_J{J}_K{K}']; cells.append(f"<td{shade(s['ex_ann'],0.07)}>{s['ex_ann']*100:+.1f}<span class='t'>t {s['t']:.1f}</span></td>")
        rows.append(tr(f"看過去 {J} 個月",cells))
    return table([f'{top}（每年超額，百分點）','持有 1 個月','持有 3 個月','持有 6 個月','持有 12 個月'],rows)
F['q3_tB10']=gridtable('FF10','10 大產業買前 3 名'); F['q3_tB49']=gridtable('FF49','49 細產業買前 5 名')
gr=q3['gran']; rows=[]
for k,l in [('FF10','10 大產業'),('FF12','12 產業'),('FF17','17 產業'),('FF30','30 產業'),('FF49','49 細產業')]:
    s=gr[k+'_mom']; rows.append(tr(f"{l}（買前 {int(gr[k+'_top'])} 名）",[tdraw('1927–2026'),f"<td{shade(s['ex_ann'],0.07)}>{s['ex_ann']*100:+.1f}</td>",tdraw(f"{s['t']:.1f}"),tdraw(f"{s['vol']*100:.0f}% / {s['bvol']*100:.0f}%")]))
s=gr['SPDR_mom']; rows.append(tr('標普類股 ETF（買前 3 名）',[tdraw('2000–2026'),f"<td{shade(s['ex_ann'],0.07)}>{s['ex_ann']*100:+.1f}</td>",tdraw(f"{s['t']:.1f}"),tdraw(f"{s['vol']*100:.0f}% / {s['bvol']*100:.0f}%")]))
F['q3_tC']=table(['分類方式（每月依過去 12 個月、略過最近 1 個月）','期間','每年超額（百分點）','t 值','年波動 策略／大盤'],rows)
rows=[]
for l,r in q3['eras'].items():
    rows.append(tr(l,[tdraw(f"{r['cal_ex']*100:+.1f}"),tdraw(f"{r['cal_hit']*100:.0f}%"),f"<td{shade(r['m10_ex'],0.07)}>{r['m10_ex']*100:+.1f}<span class='t'>t {r['m10_t']:.1f}</span></td>",f"<td{shade(r['m49_ex'],0.07)}>{r['m49_ex']*100:+.1f}<span class='t'>t {r['m49_t']:.1f}</span></td>"]))
F['q3_tD']=table(['時期','年度換冠軍（10 大產業）：每年超額','贏大盤的年份','月度動能（10 大產業前 3 名）','月度動能（49 細產業前 10 名）'],rows)
rl=q3['roll']
def ser(d): 
    ks=sorted(d.keys()); return [int(k[:4]) for k in ks],[d[k]*100 for k in ks]
x10,y10=ser(rl['m10']); x49,y49=ser(rl['m49'])
common=[x for x in x10 if x in x49]
y10c=[y10[x10.index(x)] for x in common]; y49c=[y49[x49.index(x)] for x in common]
F['q3_cE']=lines(common,[('10 大產業前 3 名','--s1',y10c),('49 細產業前 10 名','--s2',y49c)],fmt=lambda v:f"{v:+.1f}",ylab='',xfmt=lambda x:f"截至 {x} 年的 10 年",aria='產業動能策略的滾動 10 年每年超額報酬',mr_=150)
rows=[]
for l,r in q3['rankcorr'].items():
    rows.append(tr(l,[tdraw(f"{r['ff10']:+.2f}"),tdraw(f"{r['ff49']:+.2f}"),tdraw('—' if r['spdr'] is None else f"{r['spdr']:+.2f}")]))
F['q3_tH']=table(['時期','10 大產業','49 細產業','標普類股 ETF'],rows)
rows=[]
for k,l in [('FF10','10 大產業'),('FF12','12 產業'),('FF17','17 產業'),('FF30','30 產業'),('FF49','49 細產業')]:
    s=q3['G'][k]; rows.append(tr(l,[td(s['win_cagr']),td(s['lose_cagr']),td(s['mkt_cagr']),tdraw(f"{s['lose_hit']*100:.0f}%")]))
s=q3c['SPDR_lb1_top1']; rows.append(tr('標普類股 ETF（2000–2025）',[td(s['cagr']),td(s['w_cagr']),td(s['bcagr']),tdraw('—')]))
F['q3_tI']=table(['分類方式（1928–2025）','買去年第 1 名','買去年最後 1 名','大盤','最後 1 名贏大盤的年份'],rows)

# ================= Q4 =================
def r4(s,lab,src):
    return tr(lab,[tdraw(src),tdraw(f"{s['y0']}–{s['y1']}"),td(s['mean']),td(s['avg']),tdraw(f"{s['ex']*100:+.1f}"),tdraw(f"{s['hit']*100:.0f}%"),td(s['worst_mean'] if 'worst_mean' in s else s['worst'])])
e=q4o
rows=[r4(e['nonover']['lb1_top1'],'去年第 1 名','EDHEC 10 策略'),r4(e['nonover']['lb1_top3'],'去年前 3 名','EDHEC 10 策略'),r4(e['nonover']['lb3_top1'],'近 3 年第 1 名','EDHEC 10 策略'),r4(e['nonover_noSS']['lb1_top1'],'去年第 1 名（去掉放空）','EDHEC 9 策略'),
      r4(q4cs['cal']['lb1_top1'],'去年第 1 名','CS 11 策略'),r4(q4cs['cal']['lb1_top3'],'去年前 3 名','CS 11 策略'),r4(q4cs['cal']['lb3_top1'],'近 3 年第 1 名','CS 11 策略'),r4(q4cs['cal']['lb3_top3'],'近 3 年前 3 名','CS 11 策略')]
F['q4_tA']=table(['做法（每年年底換一次）','資料','期間','追逐組年報酬','全部策略平均','每年差距（百分點）','贏過平均的年份','對照：買去年最差'],rows)
gd=q4['grid']
def g4(top):
    rows=[]
    for J in [3,6,12,24]:
        cells=[f"<td{shade(gd[f't{top}_J{J}_K{K}']['ex_ann'],0.07)}>{gd[f't{top}_J{J}_K{K}']['ex_ann']*100:+.1f}<span class='t'>t {gd[f't{top}_J{J}_K{K}']['t']:.1f}</span></td>" for K in [1,3,6,12]]
        rows.append(tr(f"看過去 {J} 個月",cells))
    return table([f'EDHEC 買前 {top} 名（每年超額，百分點）','持有 1 個月','持有 3 個月','持有 6 個月','持有 12 個月'],rows)
F['q4_tB1']=g4(1); F['q4_tB3']=g4(3)
cg=q4cs['grid']
rows=[tr(f"看過去 {J} 個月",[f"<td{shade(cg[f't{t}_J{J}_K{K}']['ex_ann'],0.07)}>{cg[f't{t}_J{J}_K{K}']['ex_ann']*100:+.1f}<span class='t'>t {cg[f't{t}_J{J}_K{K}']['t']:.1f}</span></td>" for t in [1,3] for K in [1,12]]) for J in [3,6,12]]
F['q4_tBcs']=table(['CS 11 策略（每年超額，百分點）','前 1 名・持有 1 個月','前 1 名・持有 12 個月','前 3 名・持有 1 個月','前 3 名・持有 12 個月'],rows)
b=q4['B']
rows=[]
for k,l in [('ret_top1','依過去 12 個月報酬｜第 1 名'),('sharpe_top1','依過去 12 個月夏普值｜第 1 名'),('ret_top3','依過去 12 個月報酬｜前 3 名'),('sharpe_top3','依過去 12 個月夏普值｜前 3 名'),('contra_top1','反向：過去 12 個月最差 1 名'),('contra_top3','反向：過去 12 個月最差 3 名')]:
    rows.append(tr(l,[f"<td{shade(b[k+'_K12']['ex_ann'],0.07)}>{b[k+'_K12']['ex_ann']*100:+.1f}<span class='t'>t {b[k+'_K12']['t']:.1f}</span></td>",td(b[k+'_K12']['cagr']),td(b[k+'_K12']['cagr_avg']),tdraw(f"{b[k+'_K12']['vol']*100:.1f}% / {b[k+'_K12']['vol_avg']*100:.1f}%")]))
F['q4_tC']=table(['挑選方式（EDHEC，持有 12 個月）','每年超額（百分點）','策略年化','10 策略平均年化','年波動 策略／平均'],rows)
c=q4['C']; cs=q4cs['cal']['lb1_top1']
rows=[tr('EDHEC｜每月更新、持有 12 個月、第 1 名',[tdraw(f"{c['J12K12_top1_1998']['ex_ann']*100:+.1f}"),tdraw(f"{c['J12K12_top1_2008']['ex_ann']*100:+.1f}")]),
      tr('EDHEC｜每月更新、持有 12 個月、前 3 名',[tdraw(f"{c['J12K12_top3_1998']['ex_ann']*100:+.1f}"),tdraw(f"{c['J12K12_top3_2008']['ex_ann']*100:+.1f}")]),
      tr('EDHEC｜依夏普值、第 1 名',[tdraw(f"{c['sharpe_J12K12_top1_1998']['ex_ann']*100:+.1f}"),tdraw(f"{c['sharpe_J12K12_top1_2008']['ex_ann']*100:+.1f}")]),
      tr('CS｜年底換、去年第 1 名',[tdraw(f"{cs['ex_1995']*100:+.1f}"),tdraw(f"{cs['ex_2008']*100:+.1f}")]),
      tr('CS｜年底換、近 3 年第 1 名',[tdraw(f"{q4cs['cal']['lb3_top1']['ex_1995']*100:+.1f}"),tdraw(f"{q4cs['cal']['lb3_top1']['ex_2008']*100:+.1f}")])]
F['q4_tD']=table(['做法（與全部策略平均的每年差距，百分點）','2007 年以前','2008 年以後'],rows)
d=q4['D']; rows=[]
for k,l in [('directional5_top1','只在 5 個方向性策略中追第 1 名'),('arb5_top1','只在 5 個套利型策略中追第 1 名'),('ten_noSS_top1','9 策略（去掉放空）追第 1 名')]:
    rows.append(tr(l,[f"<td{shade(d[k]['ex_ann'],0.07)}>{d[k]['ex_ann']*100:+.1f}<span class='t'>t {d[k]['t']:.1f}</span></td>",td(d[k]['cagr']),td(d[k]['cagr_avg'])]))
F['q4_tE']=table(['EDHEC 子集合（每月更新、持有 12 個月）','每年超額（百分點）','策略年化','子集合平均年化'],rows)
F['q4_cum']=OLD4['c5']; F['q4_rank']=OLD4['c6']; F['q4_rows']=OLD4['rows4']
F['q2_scatter']=OLD['c2']; F['q1_rows_ep']=OLD['rows_ep']; F['q3_rows_spdr']=OLD['rows_spdr']
json.dump(F,open('frags_v2.json','w'),ensure_ascii=False,default=str)
print({k:len(v) if isinstance(v,str) else v for k,v in F.items()})
