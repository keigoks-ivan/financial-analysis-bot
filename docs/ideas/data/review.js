/* 每月檢視元件：讀 data/review.json，把本頁最新一筆渲染進 #review，其餘收進「歷次檢視」。無依賴；失敗時 #review 保持空白。 */
(function(){
  var box=document.getElementById('review');
  if(!box) return;
  var id=window.IDEA;
  if(!id){var m=location.pathname.split('/').pop()||'';id=m.replace(/\.html$/,'');}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  var VCLS={'成立':'ok','動搖':'warn','被推翻':'bad'};
  function badge(v){return '<span class="rv-badge rv-'+(VCLS[v]||'warn')+'">'+esc(v)+'</span>';}

  var css='.review-wrap{margin:14px 0 22px}'
   +'.review-wrap:empty{display:none}'
   +'.rv-card{background:var(--card,transparent);border:1px solid var(--line,#ccd);border-radius:10px;padding:14px 16px}'
   +'.rv-head{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem .7rem;margin-bottom:.5rem}'
   +'.rv-title{font-weight:700;color:var(--ink,inherit);font-size:.98rem}'
   +'.rv-action{font-size:.76rem;color:var(--sec,#667)}'
   +'.rv-badge{display:inline-block;font-size:.76rem;font-weight:600;line-height:1;padding:.28em .65em;border-radius:999px;border:1px solid currentColor;background:color-mix(in srgb,currentColor 12%,transparent)}'
   +'.rv-ok{color:var(--pos,#1a7f4b)}.rv-warn{color:var(--warn,#c98a0b)}.rv-bad{color:var(--neg,#c0392b)}'
   +'.review-wrap dl{margin:0}'
   +'.review-wrap dt{font-size:.78rem;font-weight:600;color:var(--sec,#667);margin-top:.7rem}'
   +'.review-wrap dd{margin:.12rem 0 0;font-size:.9rem;line-height:1.65}'
   +'.rv-list{margin:.12rem 0 0;padding-left:1.1rem;font-size:.88rem;line-height:1.6}'
   +'.rv-list li{margin:.15rem 0}'
   +'.rv-d{font-family:var(--mono,monospace);font-size:.76rem;color:var(--sec,#667);margin-right:.35rem}'
   +'.rv-src{font-size:.76rem;color:var(--muted,#889);margin-left:.3rem}'
   +'.rv-sc{width:100%;border-collapse:collapse;font-size:.84rem;margin-top:.2rem}'
   +'.rv-sc th,.rv-sc td{text-align:left;padding:.3rem .5rem;border-bottom:1px solid var(--line-soft,#eef)}'
   +'.rv-sc th{font-size:.74rem;color:var(--sec,#667);font-weight:600}'
   +'.rv-sc td.n,.rv-sc th.n{text-align:right;font-family:var(--mono,monospace);white-space:nowrap}'
   +'.rv-up{color:var(--pos,#1a7f4b)}.rv-dn{color:var(--neg,#c0392b)}'
   +'.rv-sc-wrap{overflow-x:auto}'
   +'.rv-more{margin-top:.6rem;font-size:.84rem}'
   +'.rv-more summary{cursor:pointer;color:var(--sec,#667)}'
   +'.rv-old{border-top:1px solid var(--line,#ccd);margin-top:.6rem;padding-top:.5rem}'
   +'@media(max-width:480px){.rv-card{padding:12px}}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

  function scen(list){
    if(!list||!list.length) return '';
    var rows=list.map(function(s){
      var d=(s.prev==null)?null:s.prob-s.prev;
      var dt=d==null?'—':(d===0?'±0pp':(d>0?'<span class="rv-up">+'+d+'pp</span>':'<span class="rv-dn">−'+Math.abs(d)+'pp</span>'));
      return '<tr><td>'+esc(s.name)+'</td><td class="n">'+esc(s.prob)+'%</td><td class="n">'+(s.prev==null?'—':esc(s.prev)+'%')+'</td><td class="n">'+dt+'</td></tr>';
    }).join('');
    return '<dt>情境機率</dt><dd><div class="rv-sc-wrap"><table class="rv-sc"><thead><tr><th>情境</th><th class="n">現在</th><th class="n">上次</th><th class="n">差異</th></tr></thead><tbody>'+rows+'</tbody></table></div></dd>';
  }
  function facts(l){
    if(!l||!l.length) return '';
    return '<dt>這個月變了什麼</dt><dd><ul class="rv-list">'+l.map(function(f){
      return '<li><span class="rv-d">'+esc(f.date)+'</span>'+esc(f.text)+(f.source?'<span class="rv-src">（'+esc(f.source)+'）</span>':'')+'</li>';}).join('')+'</ul></dd>';
  }
  function watch(l){
    if(!l||!l.length) return '';
    return '<dt>下個月看什麼</dt><dd><ul class="rv-list">'+l.map(function(f){
      return '<li>'+(f.date?'<span class="rv-d">'+esc(f.date)+'</span>':'')+esc(f.text)+'</li>';}).join('')+'</ul></dd>';
  }
  function body(r){
    return '<dl>'
      +(r.thesis?'<dt>主張還對不對</dt><dd>'+esc(r.thesis)+'</dd>':'')
      +facts(r.facts)
      +(r.counter?'<dt>反方多強</dt><dd>'+esc(r.counter)+'</dd>':'')
      +(r.money?'<dt>對錢的意義</dt><dd>'+esc(r.money)+'</dd>':'')
      +watch(r.watch)+scen(r.scenarios)+'</dl>';
  }
  fetch('data/review.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null;}).then(function(j){
    if(!j||!j.reviews) return;
    var rs=j.reviews.filter(function(r){return r.idea===id;}).sort(function(a,b){return String(b.date).localeCompare(String(a.date));});
    if(!rs.length) return;
    var r=rs[0];
    var html='<div class="rv-card"><div class="rv-head"><span class="rv-title">最近檢視 '+esc(r.date)+'</span>'+badge(r.verdict)
      +(r.action?'<span class="rv-action">處置：'+esc(r.action)+'</span>':'')+'</div>'+body(r);
    if(rs.length>1){
      html+='<details class="rv-more"><summary>歷次檢視（'+(rs.length-1)+'）</summary>'+rs.slice(1).map(function(o){
        return '<div class="rv-old"><div class="rv-head"><span class="rv-title">'+esc(o.date)+'</span>'+badge(o.verdict)
          +(o.action?'<span class="rv-action">處置：'+esc(o.action)+'</span>':'')+'</div>'+body(o)+'</div>';}).join('')+'</details>';
    }
    box.innerHTML=html+'</div>';
  }).catch(function(){});
})();
