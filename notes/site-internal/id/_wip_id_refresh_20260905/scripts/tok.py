#!/usr/bin/env python3
"""Sum token usage per JSONL transcript: per message.id take max of each usage field (streaming chunks), then sum."""
import json,sys,collections
def tally(path):
    per=collections.defaultdict(lambda: collections.defaultdict(int)); model={}
    with open(path) as f:
        for line in f:
            try: o=json.loads(line)
            except Exception: continue
            m=o.get('message') if isinstance(o,dict) else None
            if not isinstance(m,dict): continue
            u=m.get('usage'); mid=m.get('id')
            if not u or not mid: continue
            for k in ('input_tokens','output_tokens','cache_creation_input_tokens','cache_read_input_tokens'):
                per[mid][k]=max(per[mid][k],u.get(k) or 0)
            model[mid]=m.get('model','')
    tot=collections.defaultdict(int)
    for mid,u in per.items():
        for k,v in u.items(): tot[k]+=v
    tot['rounds']=len(per); tot['total']=sum(tot[k] for k in ('input_tokens','output_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
    tot['ex_cache_read']=tot['total']-tot['cache_read_input_tokens']
    models=collections.Counter(model.values())
    return dict(tot),dict(models)
if __name__=='__main__':
    grand=collections.defaultdict(int)
    for p in sys.argv[1:]:
        t,m=tally(p)
        print(f"{p.split('/')[-1][:24]:24s} rounds={t.get('rounds',0):4d} total={t.get('total',0)/1e6:6.2f}M  cache_read={t.get('cache_read_input_tokens',0)/1e6:6.2f}M  out={t.get('output_tokens',0)/1e3:6.1f}K  ex_cache={t.get('ex_cache_read',0)/1e6:5.2f}M  {m}")
        for k,v in t.items(): grand[k]+=v
    print(f"GRAND rounds={grand['rounds']} total={grand['total']/1e6:.2f}M cache_read={grand['cache_read_input_tokens']/1e6:.2f}M out={grand['output_tokens']/1e3:.1f}K ex_cache={grand['ex_cache_read']/1e6:.2f}M")
