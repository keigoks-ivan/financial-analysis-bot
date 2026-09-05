import re,json,sys
fn,out=sys.argv[1],sys.argv[2]
h=open(fn).read()
d=json.loads(re.search(r'<script[^>]*id="id-meta"[^>]*>(.*?)</script>',h,re.S).group(1))
plain=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)
heads=[re.sub(r'<[^>]+>','',t).strip() for _,t in re.findall(r'<(h[2-4])[^>]*>(.*?)</\1>',plain,re.S)]
nc=[t for t in heads if re.search(r'非共識|NC|分歧|辯論|爭點',t)]
ncp=[re.sub(r'<[^>]+>','',x).strip()[:300] for x in re.findall(r'NC#\d[^<]{0,200}',plain)][:6]
fals=[re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'可證偽條件：</strong>(.*?)</p>',plain,re.S)]
o=[f'# prior_brief — {fn.split("/")[-1]}（{d.get("skill_version")}，judgment {d.get("sections_refreshed",{}).get("judgment")} 🔴）','','禁讀全文；本檔只含 id-meta 決策欄、kill 表、非共識／分歧標題。','','## id-meta（決策欄）']
for k in ['oneliner','now_state','future_state','action','sd_verdict','clock_phase','conviction','priced_in','demand_5y_multiple','tam_usd_2030','cagr_pct_5y','thesis_type','mega','sub_group','sister_ids']:
    o.append(f'- **{k}**：{d.get(k)}')
o.append('- **related_tickers**：'+'、'.join(f"{t['ticker']}（{t.get('depth','')}｜{t.get('role','')[:60]}）" for t in d['related_tickers']))
o.append('\n## kill_metrics（前版）')
for k in d.get('kill_metrics',[]): o.append(f"- {k.get('metric')}｜{k.get('bear_threshold')}｜window={k.get('window','')}")
o.append('\n## 非共識／分歧標題（前版）'); o+=['- '+t for t in nc] or ['（無獨立分歧卡標題）']
o.append('\n## NC 句（前版）'); o+=['- '+t for t in ncp]
o.append('\n## 可證偽條件句（前版）'); o+=['- '+x for x in fals]
open(out,'w').write('\n'.join(o)); print('\n'.join(o)[:2500]); print('...tickers:',[t['ticker'] for t in d['related_tickers']])
