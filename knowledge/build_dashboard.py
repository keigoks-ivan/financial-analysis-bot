#!/usr/bin/env python3
"""
build_dashboard.py — 把 decisions.jsonl + graph.json 烤成一份「自包含、離線可開」的
本機視覺儀表板 knowledge/dashboard.html（資料內嵌，不需 server、不發布）。

用法：python knowledge/build_dashboard.py   →   open knowledge/dashboard.html
衍生物，gitignore；改了資料就重跑。
"""
import json
from pathlib import Path
from datetime import date

KDIR = Path(__file__).resolve().parent
DECISIONS = KDIR / "decisions.jsonl"
GRAPH = KDIR / "graph.json"
OUT = KDIR / "dashboard.html"


def _safe(obj):
    # 防止 thesis 裡的 </script> 破壞內嵌 script 標籤
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main():
    if not DECISIONS.exists() or not GRAPH.exists():
        import subprocess, sys
        subprocess.run([sys.executable, str(KDIR / "build_knowledge.py")], check=True)
    decisions = [json.loads(l) for l in DECISIONS.read_text(encoding="utf-8").splitlines() if l.strip()]
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    html = (TEMPLATE
            .replace("%%GENERATED%%", date.today().isoformat())
            .replace("%%NDEC%%", str(len(decisions)))
            .replace("%%DECISIONS%%", _safe(decisions))
            .replace("%%GRAPH%%", _safe(graph)))
    OUT.write_text(html, encoding="utf-8")
    print(f"✅ {OUT.relative_to(KDIR.parent)} 已生成（{len(decisions)} 決策 / "
          f"{len(graph['nodes'])} 節點）。開啟：open {OUT.relative_to(KDIR.parent)}")


TEMPLATE = r"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>知識層儀表板</title>
<style>
  :root{--bg:#0f1419;--panel:#1a2129;--line:#2a333d;--txt:#d8dee6;--mut:#8a96a3;
        --buy:#2bb673;--watch:#d9a020;--avoid:#e05555;--accent:#4a9eff;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,"PingFang TC",Segoe UI,sans-serif}
  header{padding:16px 22px;border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  header h1{font-size:18px;margin:0;font-weight:650}
  header .sub{color:var(--mut);font-size:12px}
  .cards{display:flex;gap:10px;flex-wrap:wrap;padding:14px 22px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:96px}
  .card .n{font-size:22px;font-weight:700}.card .l{color:var(--mut);font-size:11px;margin-top:2px}
  nav.tabs{display:flex;gap:6px;padding:0 22px;border-bottom:1px solid var(--line)}
  nav.tabs button{background:none;border:none;color:var(--mut);padding:10px 14px;cursor:pointer;font-size:14px;border-bottom:2px solid transparent}
  nav.tabs button.on{color:var(--txt);border-bottom-color:var(--accent)}
  main{padding:16px 22px;max-width:1180px}
  section{display:none}section.on{display:block}
  .controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
  input[type=text]{background:var(--panel);border:1px solid var(--line);color:var(--txt);padding:7px 11px;border-radius:8px;font-size:14px;min-width:220px}
  .chip{background:var(--panel);border:1px solid var(--line);color:var(--mut);padding:5px 11px;border-radius:20px;cursor:pointer;font-size:12px}
  .chip.on{color:#fff;border-color:var(--accent)}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
  th{color:var(--mut);font-weight:600;position:sticky;top:0;background:var(--bg);cursor:pointer;user-select:none}
  tr.drow{cursor:pointer}tr.drow:hover{background:#19222c}
  .tk{font-weight:650;color:var(--accent)}
  .v{padding:1px 8px;border-radius:11px;font-size:11px;font-weight:650;white-space:nowrap}
  .v.進場{background:rgba(43,182,115,.16);color:var(--buy)}
  .v.觀望{background:rgba(217,160,32,.16);color:var(--watch)}
  .v.迴避{background:rgba(224,85,85,.16);color:var(--avoid)}
  .v.none{background:#222b34;color:var(--mut)}
  .num{font-variant-numeric:tabular-nums}
  .thesis{color:var(--mut);max-width:560px}
  .full{display:none;color:var(--txt);padding:4px 9px 12px}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}
  .box h3{margin:0 0 10px;font-size:13px;color:var(--mut);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
  .row{display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--line);gap:10px}
  .row:last-child{border:none}
  .muted{color:var(--mut)}.small{font-size:12px}
  .pill{display:inline-block;background:#202a34;border:1px solid var(--line);border-radius:6px;padding:2px 7px;margin:2px 3px 0 0;font-size:12px}
  .bar{height:8px;border-radius:4px;background:var(--accent);display:inline-block}
  #entityOut .ev{margin:3px 0}
  .hint{color:var(--mut);font-size:12px;margin:8px 0}
</style></head><body>
<header>
  <h1>知識層儀表板</h1>
  <span class="sub">decision ledger + entity graph · 生成於 %%GENERATED%% · 本機檔，不發布</span>
</header>
<div class="cards" id="cards"></div>
<nav class="tabs">
  <button data-tab="ledger" class="on">決策帳本</button>
  <button data-tab="entity">Entity 探索</button>
  <button data-tab="coverage">覆蓋 / 缺口</button>
</nav>
<main>
  <section id="tab-ledger" class="on">
    <div class="controls">
      <input type="text" id="q" placeholder="搜 ticker 或 thesis…">
      <span class="chip on" data-v="all">全部</span>
      <span class="chip" data-v="進場">進場</span>
      <span class="chip" data-v="觀望">觀望</span>
      <span class="chip" data-v="迴避">迴避</span>
      <span class="chip" data-v="none">無裁決</span>
      <span class="hint" id="lcount"></span>
    </div>
    <table id="ledger"><thead><tr>
      <th data-k="date">日期</th><th data-k="entity">Ticker</th><th data-k="verdict">裁決</th>
      <th data-k="fundamental_grade">評級</th><th data-k="price_at_decision">價位</th><th>一句 thesis</th>
    </tr></thead><tbody></tbody></table>
  </section>

  <section id="tab-entity">
    <div class="controls">
      <input type="text" id="eq" placeholder="輸入 ticker（如 NVDA、TSM、2330.TW、AVGO）按 Enter">
      <span class="hint">查歷次裁決 + 所屬產業/主題 + 供應鏈位置（含別名合併）</span>
    </div>
    <div id="entityOut"></div>
  </section>

  <section id="tab-coverage">
    <div class="grid2">
      <div class="box"><h3>最新裁決分布</h3><div id="vdist"></div></div>
      <div class="box"><h3>該重跑 DD（aging/stale）</h3><div id="stale"></div></div>
      <div class="box"><h3>中樞：被最多主題引用</h3><div id="hubs"></div></div>
      <div class="box"><h3>DD 缺口：🔴 高信念但無 DD</h3><div id="gaps"></div></div>
    </div>
  </section>
</main>
<script>
const DECISIONS = %%DECISIONS%%;
const GRAPH = %%GRAPH%%;
const NODES = GRAPH.nodes, EDGES = GRAPH.edges, ALIASES = GRAPH.aliases||{};
const nodeById = {}; NODES.forEach(n=>nodeById[n.id]=n);
const companies = NODES.filter(n=>n.type==='company');
const vClass = v => v==='進場'?'進場':v==='觀望'?'觀望':v==='迴避'?'迴避':'none';
const esc = s => (s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

// ---- summary cards ----
function cards(){
  const vc={進場:0,觀望:0,迴避:0};
  companies.forEach(n=>{const v=n.canonical&&n.canonical.verdict; if(vc[v]!=null)vc[v]++;});
  const sc=NODES.filter(n=>n.type==='supplychain').length;
  const ind=NODES.filter(n=>n.type==='industry').length;
  const C=[['決策事件',DECISIONS.length],['公司',companies.length],['產業 ID',ind],
           ['供應鏈 topic',sc],['進場',vc.進場],['觀望',vc.觀望],['迴避',vc.迴避]];
  document.getElementById('cards').innerHTML=C.map(([l,n])=>
    `<div class="card"><div class="n">${n}</div><div class="l">${l}</div></div>`).join('');
}

// ---- ledger ----
let sortK='date', sortAsc=false, filtV='all';
function ledger(){
  const q=document.getElementById('q').value.trim().toLowerCase();
  let rows=DECISIONS.filter(d=>{
    if(filtV==='none'){if(d.verdict)return false;} else if(filtV!=='all'){if(d.verdict!==filtV)return false;}
    if(q){return (d.entity||'').toLowerCase().includes(q)||(d.thesis_one_line||'').toLowerCase().includes(q);}
    return true;
  });
  rows.sort((a,b)=>{let x=a[sortK]||'',y=b[sortK]||''; if(typeof x==='number'||typeof y==='number'){x=x||0;y=y||0;}
    return (x<y?-1:x>y?1:0)*(sortAsc?1:-1);});
  document.getElementById('lcount').textContent=`${rows.length} 筆`;
  const tb=document.querySelector('#ledger tbody');
  tb.innerHTML=rows.map((d,i)=>{
    const v=d.verdict||'—', exp=d.expected||{};
    const tag=exp.irr_base_pct!=null?` <span class="muted small">IRR~${exp.irr_base_pct}%</span>`:'';
    return `<tr class="drow" data-i="${i}"><td class="num">${esc(d.date)}</td>
      <td class="tk">${esc(d.entity)}</td>
      <td><span class="v ${vClass(d.verdict)}">${esc(v)}</span></td>
      <td>${esc(d.fundamental_grade||'—')}</td>
      <td class="num">${d.price_at_decision!=null?esc(d.price_at_decision):'—'}</td>
      <td class="thesis">${esc((d.thesis_one_line||'').slice(0,90))}${(d.thesis_one_line||'').length>90?'…':''}${tag}</td></tr>
      <tr class="full" id="f${i}"><td colspan="6">${esc(d.thesis_one_line||'（無）')}</td></tr>`;
  }).join('');
  tb.querySelectorAll('tr.drow').forEach(tr=>tr.onclick=()=>{
    const f=document.getElementById('f'+tr.dataset.i); f.style.display=f.style.display==='table-row'?'none':'table-row';});
}

// ---- entity ----
function entity(name){
  name=(name||'').trim().toUpperCase(); if(!name)return;
  const canon=ALIASES[name]||name;
  const members=new Set([canon]); for(const a in ALIASES)if(ALIASES[a]===canon)members.add(a);
  const mine=DECISIONS.filter(d=>members.has((d.entity||'').toUpperCase())).sort((a,b)=>(a.date||'')<(b.date||'')?-1:1);
  const node=nodeById[canon];
  const out=document.getElementById('entityOut');
  if(!mine.length&&!node){out.innerHTML=`<div class="box">找不到 ${esc(name)}</div>`;return;}
  const an=members.size>1?` <span class="muted small">(含別名 ${[...members].filter(x=>x!==canon).join(', ')})</span>`:'';
  const c=node&&node.canonical;
  let h=`<div class="box"><div style="font-size:16px"><span class="tk">${esc(canon)}</span>${an} `+
    (c?`<span class="v ${vClass(c.verdict)}">${esc(c.verdict||'—')}</span> <span class="muted small">基本面 ${esc(c.fundamental_grade||'—')} · ${esc(c.date||'')} · ${esc(c.freshness)}</span>`:`<span class="muted">（無 DD，僅在圖中被引用）</span>`)+`</div>`;
  if(mine.length){h+=`<h3 style="margin-top:14px">決策史（${mine.length}）</h3>`;
    mine.forEach(d=>{h+=`<div class="ev"><span class="num muted">${esc(d.date)}</span> `+
      `<span class="v ${vClass(d.verdict)}">${esc(d.verdict||'—')}</span> `+
      `<span class="num">$${esc(d.price_at_decision)}</span> — ${esc(d.thesis_one_line||'')}`+
      (d.outcome?` <span style="color:var(--buy)">▸ OUTCOME: ${esc(d.outcome.lesson||'')}</span>`:'')+`</div>`;});}
  const themes=[...new Set(EDGES.filter(e=>e.from===canon&&e.rel==='belongs_to').map(e=>e.to))].sort();
  if(themes.length){h+=`<h3 style="margin-top:14px">所屬產業/主題（${themes.length}）</h3>`+themes.map(t=>`<span class="pill">${esc(t)}</span>`).join('');}
  const sup=[...new Set(EDGES.filter(e=>e.from===canon&&e.rel==='supplies').map(e=>e.to+' · '+(e.node||'')))].sort();
  if(sup.length){h+=`<h3 style="margin-top:14px">供應鏈位置（${sup.length}）</h3>`+sup.map(s=>`<span class="pill">${esc(s)}</span>`).join('');}
  out.innerHTML=h+`</div>`;
}

// ---- coverage ----
function coverage(){
  const vc={}; companies.forEach(n=>{const v=(n.canonical&&n.canonical.verdict)||'（無裁決/舊版）';vc[v]=(vc[v]||0)+1;});
  const mx=Math.max(...Object.values(vc));
  document.getElementById('vdist').innerHTML=Object.entries(vc).sort((a,b)=>b[1]-a[1]).map(([k,v])=>
    `<div class="row"><span><span class="v ${vClass(k)}">${esc(k)}</span></span><span class="num">${v} <span class="bar" style="width:${v/mx*80}px"></span></span></div>`).join('');

  const stale=companies.filter(n=>n.canonical&&['aging','stale'].includes(n.canonical.freshness))
    .sort((a,b)=>(a.canonical.date||'')<(b.canonical.date||'')?-1:1);
  document.getElementById('stale').innerHTML=stale.length?stale.map(n=>
    `<div class="row"><span class="tk" onclick="goEntity('${n.id}')" style="cursor:pointer">${n.id}</span><span class="muted small">${n.canonical.date} · ${n.canonical.freshness}</span></div>`).join(''):'<div class="muted">無</div>';

  const tc={}; EDGES.filter(e=>e.rel==='belongs_to').forEach(e=>tc[e.from]=(tc[e.from]||0)+1);
  document.getElementById('hubs').innerHTML=Object.entries(tc).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([tk,c])=>{
    const v=(nodeById[tk]&&nodeById[tk].canonical&&nodeById[tk].canonical.verdict)||'—';
    return `<div class="row"><span class="tk" onclick="goEntity('${tk}')" style="cursor:pointer">${tk}</span><span><span class="v ${vClass(v)}">${esc(v)}</span> <span class="num muted">${c} 主題</span></span></div>`;}).join('');

  const red={}; EDGES.forEach(e=>{if(e.depth==='🔴'&&e.rel==='belongs_to'){const n=nodeById[e.from];
    if(!(n&&n.canonical)){(red[e.from]=red[e.from]||[]).push(e.to);}}});
  const rk=Object.entries(red).sort((a,b)=>b[1].length-a[1].length).slice(0,14);
  document.getElementById('gaps').innerHTML=rk.map(([tk,th])=>
    `<div class="row"><span class="tk">${esc(tk)}</span><span class="muted small">${th.length} 個🔴主題 · ${esc(th[0].slice(0,22))}</span></div>`).join('');
}

function goEntity(tk){document.querySelector('[data-tab=entity]').click();document.getElementById('eq').value=tk;entity(tk);}

// ---- wiring ----
document.querySelectorAll('nav.tabs button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
  document.querySelectorAll('main section').forEach(s=>s.classList.remove('on'));
  document.getElementById('tab-'+b.dataset.tab).classList.add('on');});
document.getElementById('q').oninput=ledger;
document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{
  document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));c.classList.add('on');filtV=c.dataset.v;ledger();});
document.querySelectorAll('#ledger th[data-k]').forEach(th=>th.onclick=()=>{
  const k=th.dataset.k; if(sortK===k)sortAsc=!sortAsc;else{sortK=k;sortAsc=false;}ledger();});
document.getElementById('eq').addEventListener('keydown',e=>{if(e.key==='Enter')entity(e.target.value);});
cards();ledger();coverage();
</script></body></html>"""


if __name__ == "__main__":
    main()
