#!/usr/bin/env python3
"""用法：/tmp/ddvenv/bin/python returns.py OUT.md T1 T2 ...  —— 26W/52W 週線報酬 vs QQQ；優先 data/weekly_cache，缺的用 yfinance 週線。cwd 須為 repo 根。"""
import json,sys,os
out=sys.argv[1]; tickers=sys.argv[2:]
if 'QQQ' not in tickers: tickers.append('QQQ')
series={}; src={}
for t in tickers:
    p=f'data/weekly_cache/{t}.json'
    if os.path.exists(p):
        series[t]={x['week_end']:x['close'] for x in json.load(open(p))['weekly_bars']}; src[t]='weekly_cache'
missing=[t for t in tickers if t not in series]
if missing:
    import yfinance as yf, pandas as pd
    df=yf.download(missing,period='2y',interval='1wk',auto_adjust=True,progress=False)['Close']
    if isinstance(df,pd.Series): df=df.to_frame(missing[0])
    for t in missing:
        if t not in df: continue
        s=df[t].dropna(); series[t]={d.strftime('%Y-%m-%d'):float(v) for d,v in s.items()}; src[t]='yfinance(1wk)'
ref=max(k for k in series['QQQ'])
ref=min(ref, max(series[[t for t in tickers if src.get(t)=='weekly_cache'][0]]) if any(src.get(t)=='weekly_cache' for t in tickers) else ref)
def ret(t,w):
    s=series.get(t)
    if not s: return None,None
    keys=sorted(s); k=[k for k in keys if k<=ref][-1]; i=keys.index(k); j=i-w
    return (s[k]/s[keys[j]]-1 if j>=0 else None),k
q26,_=ret('QQQ',26); q52,_=ret('QQQ',52)
L=[f'# 26W／52W 報酬 vs QQQ（零 token 補件，週線收盤，as-of 週 {ref}）','','| Ticker | as-of | 26W | 52W | 26W−QQQ | 52W−QQQ | 來源 |','|---|---|---|---|---|---|---|']
f=lambda x:'—' if x is None else f'{x*100:+.1f}%'
for t in tickers:
    a,k=ret(t,26); b,_=ret(t,52)
    L.append(f'| {t} | {k} | {f(a)} | {f(b)} | {f(None if a is None else a-q26)} | {f(None if b is None else b-q52)} | {src.get(t,"缺")} |')
L.append('\n註：不在 data/weekly_cache 的 ticker 改用 yfinance 週線（auto_adjust）。')
open(out,'w').write('\n'.join(L)); print('\n'.join(L))
