/* 總經資料庫圖表：純 SVG，無外部套件。資料 json 由 render.py 產生。 */
(function(){
function tok(n,d){try{var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||d}catch(e){return d}}
var C={accent:tok('--accent','#0d2244'),gold:tok('--gold','#b8924a'),goldDeep:tok('--gold-deep','#8f6d2c'),sec:tok('--sec','#6b7a92'),muted:tok('--muted','#9aa7b8'),line:tok('--line','#e5dfd0'),lineSoft:tok('--line-soft','#efe9da'),neg:tok('--neg','#b91c1c'),pos:tok('--pos','#15803d')};
/* 主線深海軍藍，金作第二條點綴，其後取站上其他頁（etf-dash／stock-dash）已用的藍綠灰階 */
var PAL=[C.accent,C.gold,'#3f6a9c','#3d7a70','#8fb0cf','#2a78d6',C.sec,C.goldDeep,C.muted,'#173564'];
var NS='http://www.w3.org/2000/svg';
var W=640,H=270,ML=48,MR=48,MT=10,MB=24;
/* 畫布寬度跟著容器走（1 單位＝1 像素），軸字在手機與桌機都同樣大小 */
function dims(host){var w=Math.round(host.clientWidth||640);w=Math.max(280,w);return [w,Math.round(Math.min(360,Math.max(220,w*0.42)))]}
/* 軸刻度小數位依刻度間距決定，避免 0 顯示成 0.000 */
function tnd(ticks){var st=ticks.length>1?Math.abs(ticks[1]-ticks[0]):1;return st>=1?0:Math.min(4,Math.ceil(-Math.log10(st)-1e-9))}
function el(n,a,t){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(t!=null)e.textContent=t;return e}
var LIGHTS={1:'藍燈',2:'黃藍燈',3:'綠燈',4:'黃紅燈',5:'紅燈'};
function fmt(v,nd){if(v==null||isNaN(v))return '–';var a=Math.abs(v);
 if(nd==null)nd=(a>=1000||(a>=1&&v===Math.round(v)))?0:a>=100?1:a>=1?2:3;
 return v.toLocaleString('en-US',{minimumFractionDigits:nd,maximumFractionDigits:nd}).replace('-','−')}
function fmtS(s,v){return s.light?(LIGHTS[Math.round(v)]||fmt(v)):fmt(v,s.nd)}
function dstr(d){var t=new Date(d*86400000);return t.getUTCFullYear()+'-'+('0'+(t.getUTCMonth()+1)).slice(-2)+'-'+('0'+t.getUTCDate()).slice(-2)}
function nice(lo,hi,n){if(hi===lo){hi=lo+1;lo=lo-1}
 var span=hi-lo,step=Math.pow(10,Math.floor(Math.log10(span/n))),err=span/n/step;
 step*= err>=7.5?10:err>=3.5?5:err>=1.5?2:1;
 var a=Math.floor(lo/step)*step,b=Math.ceil(hi/step)*step,t=[];for(var v=a;v<=b+step/2;v+=step)t.push(+v.toFixed(10));return {lo:a,hi:b,ticks:t}}
function bisect(arr,x){var lo=0,hi=arr.length;while(lo<hi){var m=(lo+hi)>>1;if(arr[m]<x)lo=m+1;else hi=m}return lo}
function Chart(host,data,meta){
 this.host=host;this.data=data;this.meta=meta;this.range=meta.range||5;this.off={};
 var self=this;
 this.legend=host.parentNode.querySelector('.legend');
 this.buildLegend();
 var btns=host.parentNode.querySelectorAll('.rng button');
 btns.forEach(function(b){b.addEventListener('click',function(){btns.forEach(function(x){x.classList.remove('on')});b.classList.add('on');self.range=+b.getAttribute('data-r');self.draw()})});
 this.draw()}
Chart.prototype.buildLegend=function(){var self=this;if(!this.legend)return;this.legend.innerHTML='';
 this.data.series.forEach(function(s,i){var b=document.createElement('button');b.type='button';
  b.innerHTML='<i style="background:'+PAL[i%PAL.length]+'"></i>'+s.label;
  b.addEventListener('click',function(){self.off[s.id]=!self.off[s.id];b.classList.toggle('off',!!self.off[s.id]);self.draw()});self.legend.appendChild(b)})};
Chart.prototype.draw=function(){
 var WH=dims(this.host),W=WH[0],H=WH[1];this.w=W;
 var self=this,D=this.data,host=this.host;host.innerHTML='';
 var sc=D.scatter,series=D.series.filter(function(s){return !self.off[s.id]});
 var allMax=-1e12;D.series.forEach(function(s){if(s.d.length)allMax=Math.max(allMax,s.d[s.d.length-1])});
 var today=Math.floor(Date.now()/86400000);
 var endD=D.series.some(function(s){return s.future})?allMax:Math.min(allMax,Math.max(today,0));
 var latest=-1e12;D.series.forEach(function(s){s.d.forEach(function(x){if(x<=endD&&x>latest)latest=x})});
 if(latest<-1e11)latest=allMax;
 var t1=D.series.some(function(s){return s.future})?allMax:latest;
 var t0=this.range>0?t1-this.range*365.25:Math.min.apply(null,D.series.map(function(s){return s.d[0]}));
 if(sc){return this.drawScatter(series,t0,t1,W,H)}
 var pw=W-ML-MR,ph=H-MT-MB;
 var ax={L:[],R:[]},hasBar=false;
 series.forEach(function(s){var side=s.axis==='R'?'R':'L';
  var lo=1e18,hi=-1e18,sums={};
  for(var i=0;i<s.d.length;i++){if(s.d[i]<t0||s.d[i]>t1)continue;var v=s.v[i];if(v==null)continue;
   if(s.kind==='stack'){var k=s.d[i];sums[k]=sums[k]||[0,0];if(v>=0)sums[k][1]+=v;else sums[k][0]+=v}
   else{if(v<lo)lo=v;if(v>hi)hi=v}}
  if(s.kind==='stack'){for(var k in sums){lo=Math.min(lo,sums[k][0]);hi=Math.max(hi,sums[k][1])}}
  if(s.kind==='bar'||s.kind==='stack'){hasBar=true;lo=Math.min(lo,0);hi=Math.max(hi,0)}
  if(lo<=hi)ax[side].push([lo,hi])});
 var scale={};['L','R'].forEach(function(sd){if(!ax[sd].length)return;
  var lo=Math.min.apply(null,ax[sd].map(function(x){return x[0]})),hi=Math.max.apply(null,ax[sd].map(function(x){return x[1]}));
  var pad=(hi-lo)*0.04||1;scale[sd]=nice(lo-(lo===0?0:pad),hi+(hi===0?0:pad),5)});
 var svg=el('svg',{viewBox:'0 0 '+W+' '+H,preserveAspectRatio:'xMidYMid meet'});
 function X(d){return ML+(d-t0)/Math.max(1,(t1-t0))*pw}
 function Y(sd,v){var s=scale[sd];return MT+ph-(v-s.lo)/(s.hi-s.lo)*ph}
 var gs=scale.L||scale.R;
 gs.ticks.forEach(function(t){var y=MT+ph-(t-gs.lo)/(gs.hi-gs.lo)*ph;svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:y,y2:y,stroke:C.lineSoft,'stroke-width':1}))});
 ['L','R'].forEach(function(sd){if(!scale[sd])return;var s=scale[sd];
  var nd=tnd(s.ticks);s.ticks.forEach(function(t){var y=MT+ph-(t-s.lo)/(s.hi-s.lo)*ph;
   svg.appendChild(el('text',{x:sd==='L'?ML-5:W-MR+5,y:y+3.5,'text-anchor':sd==='L'?'end':'start','class':'axl'},fmt(t,nd)))})});
 /* x ticks */
 var span=(t1-t0)/365.25,d0=new Date(t0*86400000),y0=d0.getUTCFullYear();
 var stepY=span>30?10:span>14?5:span>6?2:1,ppy=pw/Math.max(span,0.01);
 [1,2,5,10,20,50].some(function(k){if(k>=stepY&&k*ppy>=44){stepY=k;return true}return false});
 var stepM=[2,3,4,6,12].filter(function(k){return k*ppy/12>=60})[0]||12;
 if(span<=1.6){for(var m=0;m<24;m++){var dd=Date.UTC(d0.getUTCFullYear(),d0.getUTCMonth()+m,1)/86400000;if(dd<t0||dd>t1)continue;var dt=new Date(dd*86400000);
   if(dt.getUTCMonth()%stepM)continue;svg.appendChild(el('text',{x:X(dd),y:H-6,'text-anchor':'middle','class':'axl'},dt.getUTCFullYear()+'-'+('0'+(dt.getUTCMonth()+1)).slice(-2)))}}
 else{for(var y=Math.ceil(y0/stepY)*stepY;y<=new Date(t1*86400000).getUTCFullYear();y+=stepY){var dd2=Date.UTC(y,0,1)/86400000;if(dd2<t0||dd2>t1)continue;
   svg.appendChild(el('line',{x1:X(dd2),x2:X(dd2),y1:MT,y2:MT+ph,stroke:C.lineSoft}));
   svg.appendChild(el('text',{x:X(dd2),y:H-6,'text-anchor':'middle','class':'axl'},''+y))}}
 /* zero line */
 ['L','R'].forEach(function(sd){var s=scale[sd];if(s&&s.lo<0&&s.hi>0&&sd===(scale.L?'L':'R'))svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(sd,0),y2:Y(sd,0),stroke:C.muted,'stroke-width':1}))});
 /* bars: common width */
 var dset={};series.forEach(function(s){if(s.kind==='bar'||s.kind==='stack')s.d.forEach(function(x){if(x>=t0&&x<=t1)dset[x]=1})});
 var nb=Object.keys(dset).length||1,bw=Math.max(1,Math.min(14,pw/nb*0.72));
 var stackAcc={};var soloBar=series.filter(function(q){return q.kind==='bar'}).length===1&&!series.some(function(q){return q.kind==='stack'});
 var idx={};D.series.forEach(function(s,i){idx[s.id]=i});
 series.forEach(function(s){var sd=s.axis==='R'?'R':'L';if(!scale[sd])return;var col=PAL[idx[s.id]%PAL.length];
  if(s.kind==='bar'||s.kind==='stack'){
   for(var i=0;i<s.d.length;i++){var d=s.d[i],v=s.v[i];if(v==null||d<t0||d>t1)continue;var y0v=0,y1v=v;
    if(s.kind==='stack'){var a=stackAcc[d]=stackAcc[d]||[0,0];if(v>=0){y0v=a[1];y1v=a[1]+v;a[1]=y1v}else{y0v=a[0];y1v=a[0]+v;a[0]=y1v}}
    var ya=Y(sd,y0v),yb=Y(sd,y1v);svg.appendChild(el('rect',{x:X(d)-bw/2,y:Math.min(ya,yb),width:bw,height:Math.max(0.5,Math.abs(ya-yb)),fill:(s.kind==='bar'&&soloBar)?(v>=0?C.pos:C.neg):col,opacity:s.kind==='stack'?0.85:0.9}))}
  }else{
   var p='',pen=false;
   for(var j=0;j<s.d.length;j++){var d2=s.d[j];if(d2<t0||d2>t1)continue;var v2=s.v[j];if(v2==null){pen=false;continue}
    p+=(pen?'L':'M')+X(d2).toFixed(1)+' '+Y(sd,v2).toFixed(1);pen=true}
   if(p)svg.appendChild(el('path',{d:p,fill:'none',stroke:col,'stroke-width':1.8,'stroke-linejoin':'round','stroke-dasharray':s.dash?'5 3':''}));
   /* 稀疏序列加點 */
   var cnt=0;for(var q=0;q<s.d.length;q++){if(s.d[q]>=t0&&s.d[q]<=t1)cnt++}
   if(cnt<=40){for(var q2=0;q2<s.d.length;q2++){if(s.d[q2]>=t0&&s.d[q2]<=t1&&s.v[q2]!=null)svg.appendChild(el('circle',{cx:X(s.d[q2]),cy:Y(sd,s.v[q2]),r:2.2,fill:col}))}}
  }});
 /* hover */
 var line=el('line',{y1:MT,y2:MT+ph,stroke:C.sec,'stroke-dasharray':'3 3',visibility:'hidden'});svg.appendChild(line);
 var tip=document.createElement('div');tip.className='tip';
 host.appendChild(svg);host.appendChild(tip);
 function move(ev){var r=svg.getBoundingClientRect();var px=(ev.clientX-r.left)/r.width*W;if(px<ML||px>W-MR){leave();return}
  var td=t0+(px-ML)/pw*(t1-t0);var rows=[],best=null,bd=1e9;
  series.forEach(function(s){var i=bisect(s.d,td);var c=[i-1,i].filter(function(k){return k>=0&&k<s.d.length&&s.v[k]!=null&&s.d[k]>=t0&&s.d[k]<=t1});
   if(!c.length)return;c.sort(function(a,b){return Math.abs(s.d[a]-td)-Math.abs(s.d[b]-td)});var k=c[0];
   if(Math.abs(s.d[k]-td)<bd){bd=Math.abs(s.d[k]-td);best=s.d[k]}
   rows.push([s,k])});
  if(best==null){leave();return}
  var h='<b>'+dstr(best)+'</b>';
  rows.forEach(function(r2){var s=r2[0],k=r2[1];if(Math.abs(s.d[k]-best)>Math.max(40,(t1-t0)/60))return;h+='<br><span style="color:'+PAL[idx[s.id]%PAL.length]+'">■</span> '+s.label+'　'+fmtS(s,s.v[k])+(s.u?(' '+s.u):'')});
  tip.innerHTML=h;tip.style.display='block';line.setAttribute('x1',X(best));line.setAttribute('x2',X(best));line.setAttribute('visibility','visible');
  var tw=tip.offsetWidth,left=(X(best)/W)*r.width+12;if(left+tw>r.width)left=(X(best)/W)*r.width-tw-12;tip.style.left=Math.max(0,left)+'px';tip.style.top='6px'}
 function leave(){tip.style.display='none';line.setAttribute('visibility','hidden')}
 svg.addEventListener('pointermove',move);svg.addEventListener('pointerleave',leave);svg.addEventListener('pointerdown',move)};
Chart.prototype.drawScatter=function(series,t0,t1,W,H){
 var host=this.host,xs=null,ys=null;
 this.data.series.forEach(function(s){if(s.axis==='X')xs=s;if(s.axis==='Y')ys=s});
 var ym={};ys.d.forEach(function(d,i){ym[d]=ys.v[i]});
 var pts=[];xs.d.forEach(function(d,i){if(d>=t0&&d<=t1&&ym[d]!=null&&xs.v[i]!=null)pts.push([d,xs.v[i],ym[d]])});
 var pw=W-ML-MR,ph=H-MT-MB;
 var sx=nice(Math.min.apply(null,pts.map(function(p){return p[1]})),Math.max.apply(null,pts.map(function(p){return p[1]})),5);
 var sy=nice(Math.min.apply(null,pts.map(function(p){return p[2]})),Math.max.apply(null,pts.map(function(p){return p[2]})),5);
 var svg=el('svg',{viewBox:'0 0 '+W+' '+H});
 function X(v){return ML+(v-sx.lo)/(sx.hi-sx.lo)*pw}function Y(v){return MT+ph-(v-sy.lo)/(sy.hi-sy.lo)*ph}
 var ndy=tnd(sy.ticks),ndx=tnd(sx.ticks);
 sy.ticks.forEach(function(t){svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(t),y2:Y(t),stroke:C.lineSoft}));svg.appendChild(el('text',{x:ML-5,y:Y(t)+3.5,'text-anchor':'end','class':'axl'},fmt(t,ndy)))});
 sx.ticks.forEach(function(t){svg.appendChild(el('text',{x:X(t),y:H-6,'text-anchor':'middle','class':'axl'},fmt(t,ndx)))});
 var p='';pts.forEach(function(q,i){p+=(i?'L':'M')+X(q[1]).toFixed(1)+' '+Y(q[2]).toFixed(1)});
 svg.appendChild(el('path',{d:p,fill:'none',stroke:C.muted,'stroke-width':1}));
 pts.forEach(function(q,i){var f=i/Math.max(1,pts.length-1);svg.appendChild(el('circle',{cx:X(q[1]),cy:Y(q[2]),r:i===pts.length-1?5:2.6,fill:i===pts.length-1?C.neg:C.accent,opacity:0.25+0.75*f}))});
 var tip=document.createElement('div');tip.className='tip';host.appendChild(svg);host.appendChild(tip);
 svg.addEventListener('pointermove',function(ev){var r=svg.getBoundingClientRect(),px=(ev.clientX-r.left)/r.width*W,py=(ev.clientY-r.top)/r.height*H,b=null,bd=1e9;
  pts.forEach(function(q){var dd=Math.pow(X(q[1])-px,2)+Math.pow(Y(q[2])-py,2);if(dd<bd){bd=dd;b=q}});
  if(!b)return;tip.innerHTML='<b>'+dstr(b[0])+'</b><br>'+xs.label+'　'+fmt(b[1])+'<br>'+ys.label+'　'+fmt(b[2]);tip.style.display='block';
  var left=X(b[1])/W*r.width+12;if(left+tip.offsetWidth>r.width)left-=tip.offsetWidth+24;tip.style.left=Math.max(0,left)+'px';tip.style.top='6px'});
 svg.addEventListener('pointerleave',function(){tip.style.display='none'})};
window.MacroDB={start:function(jsonUrl){
 fetch(jsonUrl).then(function(r){return r.json()}).then(function(J){
  var all=[];document.querySelectorAll('.chart[data-key]').forEach(function(h){var d=J.charts[h.getAttribute('data-key')];if(d)all.push(new Chart(h,d,{range:+h.getAttribute('data-range')||5}))});
  var tm=null;window.addEventListener('resize',function(){clearTimeout(tm);tm=setTimeout(function(){all.forEach(function(c){if(c.host.offsetParent!==null&&Math.abs(Math.round(c.host.clientWidth)-c.w)>8)c.draw()})},150)})
 }).catch(function(e){document.querySelectorAll('.chart[data-key]').forEach(function(h){h.innerHTML='<p class="note">圖表資料載入失敗，請重新整理。</p>'})})},
 country:function(){var tabs=document.querySelectorAll('[data-c]'),secs=document.querySelectorAll('[data-sec]');
  function show(c){secs.forEach(function(s){s.classList.toggle('hide',s.getAttribute('data-sec')!==c)});tabs.forEach(function(t){t.classList.toggle('on',t.getAttribute('data-c')===c)});try{history.replaceState(null,'','#'+c)}catch(e){}
   try{window.dispatchEvent(new Event('resize'))}catch(e){}}
  tabs.forEach(function(t){t.addEventListener('click',function(){if(!t.classList.contains('off'))show(t.getAttribute('data-c'))})});
  var h=(location.hash||'').slice(1);show(h==='tw'&&document.querySelector('[data-sec=tw]')?'tw':'us')}};
})();
