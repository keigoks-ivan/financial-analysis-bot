#!/usr/bin/env python3
"""選股系統 v2 原型（純本地資料；DD 為選配層）。
輸入：docs/dd-screener/latest.json（252，機械欄）＋ docs/qgm/latest.json（80，無 DD 亦可）＋ data/weekly_cache。
輸出：甲 複利軌排序、乙 循環軌名單、與現任 GRP 席位／DD 裁決對照。"""
import json,os,glob,sys,datetime as dt
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
S=os.environ.get('SEL_OUT',os.path.dirname(os.path.abspath(__file__)))
today=dt.date(2026,9,2)
def f(v):
    try:
        x=float(v); return x if x==x else None
    except: return None
# ---------- 週線結構（不依賴 DD）----------
def bars(t):
    for c in (t,t.replace('.TW','TW')):
        p=f'{ROOT}/data/weekly_cache/{c}.json'
        if os.path.exists(p): return [b['close'] for b in json.load(open(p))['weekly_bars']]
    return None
def structure(t):
    c=bars(t)
    if not c or len(c)<60: return {}
    last=c[-1]; ma40=sum(c[-40:])/40; ma52=sum(c[-52:])/52; hi52=max(c[-52:]); hi250=max(c[-250:]) if len(c)>=250 else max(c)
    r26=last/c[-27]-1; r52=last/c[-53]-1 if len(c)>53 else None
    # 26 週最大回撤（過熱／崩跌對稱）
    return dict(px=last,above_40w=last>ma40,above_52w=last>ma52,dist_hi52=(last/hi52-1)*100,dist_ath=(last/hi250-1)*100,r26=r26*100,r52=(r52*100 if r52 is not None else None))
# ---------- 甲 複利軌 ----------
ROIC_MIN,FCF_MIN,G_MIN,G_CAP,CAP_MIN=15.0,10.0,12.0,30.0,20e9
def compounder(row):
    """row: 統一欄位 dict。回傳 (資格, 排序分, 註記[])"""
    why=[]
    roic,fcf,g,peg,de=row.get('roic'),row.get('fcf'),row.get('g'),row.get('peg'),row.get('de')
    ok=True
    if roic is None and fcf is None: ok=False; why.append('金融／無品質欄→另軌')
    else:
        if roic is None or roic<ROIC_MIN: ok=False; why.append(f'ROIC {roic}')
        if fcf is None or fcf<FCF_MIN: ok=False; why.append(f'FCF {fcf}')
    if g is None or g<G_MIN: ok=False; why.append(f'成長 {g}')
    # 排序鍵＝「擁有什麼」：5 年報酬代理 = 成長（封頂）+ FY2 盈餘殖利率 − 倍數風險
    ey=row.get('ey0')
    score=None
    if ey is not None and g is not None:
        score=min(g,G_CAP)+ey
        if peg is not None and peg>2.0: score-=5; why.append('PEG>2')
        if roic is not None and roic>=30: score+=2   # 持續期 tilt：高 ROIC 加 2 分
    if de is not None and de>0.7: why.append('D/E 警示')
    return ok,score,why,ey
def timing(st):
    if not st: return '無價格資料'
    if st.get('src')=='qgm-tt': return '🟢 趨勢內(QGM MA)' if st['above_52w'] else '🔴 趨勢外(QGM MA)'
    if not st['above_52w']: return '🔴 52 週線下'
    if st.get('r26') and st['r26']>80: return '🟠 過熱（26 週 >+80%）'
    if st['dist_hi52']>=-5: return '🟢 突破帶'
    if -25<=st['dist_hi52']<=-8: return '🟢 回踩'
    return '🟡 趨勢內'
# ---------- 載入 ----------
D=json.load(open(f'{ROOT}/docs/dd-screener/latest.json'))['stocks']
Q=json.load(open(f'{ROOT}/docs/qgm/latest.json'))
caps=json.load(open(f'{ROOT}/data/engine/mktcap.json'))
arena=json.load(open(f'{ROOT}/docs/engine/arena.json'))
seats={x['ticker']:('核心席' if x in arena['core_seats'] else '衛星席') for x in arena['core_seats']+arena['sat_seats']}
rows={}
for s in D:
    t=s['ticker']; st=structure(t)
    ddage=s.get('dd_age_days'); v=s.get('dca_verdict')
    dd_tag=(f"DD {v}" + (f"·{s.get('dca_role')}" if s.get('dca_role') else '') + (f"（{ddage}d）" if ddage is not None else '')) if v else ('DD 舊版無裁決' if s.get('dd_path') else '無 DD')
    if v and ddage is not None and ddage>180: dd_tag+='⚠過期'
    g13=f(s.get('eps_fy1_fy3_cagr_pct')); g2=f(s.get('eps2y_live')) or f(s.get('eps2y')); flags=[]
    g=g13
    if g13 is None or (g13<0 and g2 is not None and g2>0): g=g2; flags.append('成長欄衝突→用 2Y')
    fpe=f(s.get('live_fpe_est')); px0=st.get('px') or f((s.get('ma') or {}).get('price'))
    ey=(100/fpe) if fpe and fpe>0 else None
    if ey is None and f(s.get('eps_fy_next')) and px0: ey=f(s.get('eps_fy_next'))/px0*100
    if s.get('roic') is None and s.get('sector','').lower().startswith(('fin','')) and f(s.get('fcf')) is None: flags.append('金融另軌')
    rows[t]=dict(t=t,src='dd-screener',roic=f(s.get('roic')),fcf=f(s.get('fcf')),g=g,flags=flags,
        peg=f(s.get('live_peg')) or f(s.get('peg')),de=f(s.get('de')),ey0=ey,px=px0,
        rev1m=f(s.get('eps_fy_next_revision_pct')),rev2y=f(s.get('eps2y_revision_pp')),cap=caps.get(t),st=st,dd=dd_tag,verdict=v,moat=f"{s.get('moat_grade')}{s.get('moat_trend') or ''}")
for k in ('candidates','watch_list','quality_pool'):
    for x in Q[k]:
        t=x['ticker']
        if t in rows: continue
        h=x['hard_filter_details']; g=h.get('eps_cagr_2y_fwd',{}).get('value'); st=structure(t)
        fy1,fy2=f(x.get('fy1_eps')),f(x.get('fy2_eps'))
        g1=((fy2/fy1-1)*100) if fy1 and fy2 and fy1>0 else None   # QGM 的 cagr2y 以 FY0 為基期會膨脹，改用 FY1→FY2 單年
        per1=f(x.get('fy1_per')); ey=(100/per1) if per1 and per1>0 else None
        conds=(x.get('trend_template') or {}).get('conditions',{})
        c1=conds.get('condition_1',{}).get('pass'); c3=conds.get('condition_3',{}).get('pass')
        if not st: st={'px':f(x.get('price')),'above_52w':bool(c1 and c3),'above_40w':bool(c1),'dist_hi52':-10.0,'r26':None,'r52':None,'src':'qgm-tt'}
        rows[t]=dict(t=t,src='qgm',roic=(h['roic']['value'] or 0)*100 if h.get('roic') else None,fcf=(h['fcf_margin']['value'] or 0)*100 if h.get('fcf_margin') else None,
            g=g1,flags=['QGM 成長=FY1→FY2 單年'],peg=(per1/g1) if per1 and g1 and g1>0 else None,de=h.get('debt_to_equity',{}).get('value'),ey0=ey,px=f(x.get('price')),
            rev1m=None,rev2y=None,cap=(x.get('market_cap_b') or 0)*1e9,st=st,dd='無 DD',verdict=None,moat='—')
# ---------- 甲 ----------
out=[]
for t,r in rows.items():
    ok,score,why,ey=compounder(r)
    r.update(ok=ok,score=score,why=why,ey=ey,timing=timing(r['st']))
    if r['verdict']=='迴避': r['ok']=False; r['why'].append('DD 迴避')
    if r['rev1m'] is not None and r['rev1m']<=-10: r['ok']=False; r['why'].append(f'FY1 單月下修 {r["rev1m"]}%')
    out.append(r)
core=[r for r in out if r['ok'] and r['score'] is not None and (r['cap'] or 0)>=CAP_MIN]
core.sort(key=lambda r:-r['score'])
print(f"甲 複利軌｜資格：ROIC≥{ROIC_MIN} FCF≥{FCF_MIN} 成長≥{G_MIN} 市值≥$20B｜排序＝min(成長,30)+FY2 盈餘殖利率(+2 if ROIC≥30, −5 if PEG>2)｜時機獨立顯示不進排序")
print(f"母體 {len(rows)}（dd-screener {sum(1 for r in rows.values() if r['src']=='dd-screener')}＋QGM 獨有 {sum(1 for r in rows.values() if r['src']=='qgm')}）→ 過閘 {len(core)}")
print(f"{'#':>2} {'ticker':8} {'分':>5} {'成長':>6} {'EY':>5} {'ROIC':>5} {'PEG':>5} {'1M修':>6} {'時機':10} {'席位':6} {'DD':28} {'moat':5} 註記")
for i,r in enumerate(core[:40],1):
    print(f"{i:>2} {r['t']:8} {r['score']:5.1f} {r['g']:6.1f} {r['ey']:5.1f} {(r['roic'] or 0):5.1f} {str(r['peg'])[:5]:>5} {str(r['rev1m'])[:6]:>6} {r['timing']:10} {seats.get(r['t'],''):6} {r['dd']:28} {r['moat']:5} {'；'.join(r['why']+r.get('flags',[]))}")
json.dump({r['t']:{k:(v if k!='st' else v) for k,v in r.items()} for r in out},open(f'{S}/selection_v2_rows.json','w'),ensure_ascii=False,indent=1,default=str)
# ---------- 對照 ----------
print("\n== 現任 GRP 席位在甲軌的位置")
rank={r['t']:i for i,r in enumerate(core,1)}
for t,s in seats.items():
    r=rows.get(t); print(f"  {t:6} {s} → {'甲軌 #'+str(rank[t]) if t in rank else '未過閘：'+'；'.join(r['why']) if r else '不在母體'}  時機 {r['timing'] if r else ''}")
print("\n== 48 檔 DD 進場 vs 機械資格")
ent=[r for r in out if r['verdict']=='進場']
passed=[r for r in ent if r['ok']]; failed=[r for r in ent if not r['ok']]
print(f"  進場 {len(ent)}：過閘 {len(passed)}／未過 {len(failed)}")
for r in failed: print(f"   ✗ {r['t']:8} {'；'.join(r['why'])}  時機 {r['timing']}")
print("\n== 無 DD 而機械過閘的名字（DD 選配層的候選）")
for r in core:
    if r['dd']=='無 DD': print(f"   {r['t']:8} 分 {r['score']:.1f} 成長 {r['g']:.1f} ROIC {r['roic']:.1f} PEG {r['peg']} 時機 {r['timing']}")
# ---------- 乙 循環軌 ----------
print("\n乙 循環軌｜資格：trailing 品質閘不過（ROIC<15 或 FCF<10）∩ FY1 單月上修 ≥+5% ∩ 站上 52 週線｜峰頂守門：12M >+150% 或 26W >+80% → 標『晚段』")
cyc=[]
for r in out:
    if r['src']!='dd-screener' or not r['st']: continue
    qfail=(r['roic'] is None or r['roic']<ROIC_MIN) or (r['fcf'] is None or r['fcf']<FCF_MIN)
    if qfail and r['rev1m'] is not None and r['rev1m']>=5 and r['st'].get('above_52w'):
        late=(r['st'].get('r52') or 0)>150 or (r['st'].get('r26') or 0)>80
        cyc.append((r,late))
cyc.sort(key=lambda x:-(x[0]['rev1m'] or 0))
for r,late in cyc[:20]:
    print(f"   {r['t']:8} FY1 1M修 {r['rev1m']:+.1f}% 12M {r['st'].get('r52') and round(r['st']['r52'])}% 26W {round(r['st']['r26'])}% 距高 {r['st']['dist_hi52']:.0f}% {'⚠晚段' if late else '早/中段'} {r['dd']}")
