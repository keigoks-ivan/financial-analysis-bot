/* 總經資料庫圖表：純 SVG，無外部套件。資料 json 由 render.py 產生。 */
(function(){
function tok(n,d){try{var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||d}catch(e){return d}}
var C={accent:tok('--accent','#0d2244'),gold:tok('--gold','#b8924a'),goldDeep:tok('--gold-deep','#8f6d2c'),sec:tok('--sec','#6b7a92'),muted:tok('--muted','#9aa7b8'),line:tok('--line','#e5dfd0'),lineSoft:tok('--line-soft','#efe9da'),neg:tok('--neg','#b91c1c'),pos:tok('--pos','#15803d')};
/* 配色同 myproperty report 頁；須與 render.py 的 PAL 同一組、同順序 */
var PAL=['#0d2244','#b8924a','#b91c1c','#1d4ed8','#15803d','#a16207','#6b7a92','#d4b576','#234a86','#173564'];
var GRID='#ece5d4',uid=0;
/* 柱漸層：海軍藍、金用指定色對，其餘取同色系由淺到深 */
function lite(h){var n=parseInt(h.slice(1),16),r=n>>16,g=(n>>8)&255,b=n&255;function m(x){return Math.round(x+(255-x)*0.3)}return '#'+((1<<24)|(m(r)<<16)|(m(g)<<8)|m(b)).toString(16).slice(1)}
var BARG={'#0d2244':'#234a86','#b8924a':'#cda85f'};
/* 單調三次插值（同 d3 curveMonotoneX），不超調；pts 為 [x,y] 且 x 遞增，回傳不含起點 M 的路徑字串 */
function sgn(x){return x<0?-1:1}
function sl3(x0,y0,x1,y1,x2,y2){var h0=x1-x0,h1=x2-x1,s0=(y1-y0)/(h0||1),s1=(y2-y1)/(h1||1),p=(s0*h1+s1*h0)/((h0+h1)||1);return (sgn(s0)+sgn(s1))*Math.min(Math.abs(s0),Math.abs(s1),0.5*Math.abs(p))||0}
function sl2(x0,y0,x1,y1,t){var h=x1-x0;return h?(3*(y1-y0)/h-t)/2:t}
function mono(P){var n=P.length,t=[],i,o='';if(n<2)return '';
 if(n===2){var k=(P[1][1]-P[0][1])/((P[1][0]-P[0][0])||1);t=[k,k]}
 else{for(i=1;i<n-1;i++)t[i]=sl3(P[i-1][0],P[i-1][1],P[i][0],P[i][1],P[i+1][0],P[i+1][1]);
  t[0]=sl2(P[0][0],P[0][1],P[1][0],P[1][1],t[1]);t[n-1]=sl2(P[n-1][0],P[n-1][1],P[n-2][0],P[n-2][1],t[n-2])}
 for(i=0;i<n-1;i++){var dx=(P[i+1][0]-P[i][0])/3;o+='C'+(P[i][0]+dx).toFixed(1)+' '+(P[i][1]+dx*t[i]).toFixed(1)+' '+(P[i+1][0]-dx).toFixed(1)+' '+(P[i+1][1]-dx*t[i+1]).toFixed(1)+' '+P[i+1][0].toFixed(1)+' '+P[i+1][1].toFixed(1)}
 return o}
var NS='http://www.w3.org/2000/svg';
var W=640,H=270,MT=10,MB=24;
/* 軸字寬度：離屏 canvas 量測（字型同 .axl），左右邊距跟著最長刻度字走 */
var CV=document.createElement('canvas').getContext('2d');
function tw(a){CV.font="11px Inter,'Noto Sans TC',sans-serif";var m=0;a.forEach(function(t){m=Math.max(m,CV.measureText(t).width)});return m}
function tl(sc,pc){return sc?sc.ticks.map(function(t){return fmt(t,tnd(sc.ticks))+(pc?'%':'')}):[]}
function marg(l,r){return [Math.max(28,Math.ceil(tw(l))+8),r&&r.length?Math.max(28,Math.ceil(tw(r))+8):12]}
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
 var ph=H-MT-MB;
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
  var pad=(hi-lo)*0.04||1;scale[sd]=nice(lo>=0?Math.max(0,lo-pad):lo-pad,hi+(hi===0?0:pad),5)});
 /* 某側軸上所有可見序列單位都是 % 才給刻度加 % */
 var pct={};['L','R'].forEach(function(sd){var ss=series.filter(function(q){return (q.axis==='R'?'R':'L')===sd});pct[sd]=ss.length>0&&ss.every(function(q){return q.u==='%'&&!q.light})});
 var mg=marg(tl(scale.L,pct.L),tl(scale.R,pct.R)),ML=mg[0],MR=mg[1],pw=W-ML-MR;
 /* bars: common width；有柱時繪圖範圍左右各內縮半根柱寬＋2px，頭尾柱不溢出 */
 var dset={};series.forEach(function(s){if(s.kind==='bar'||s.kind==='stack')s.d.forEach(function(x){if(x>=t0&&x<=t1)dset[x]=1})});
 var nb=Object.keys(dset).length||1,nbar=series.filter(function(q){return q.kind==='bar'}).length,side=nbar>=2&&!series.some(function(q){return q.kind==='stack'}),bw=Math.max(1,Math.min(side?nbar*8:14,pw/nb*0.72)),pad=hasBar?bw/2+2:0,pwi=pw-2*pad;
 var svg=el('svg',{viewBox:'0 0 '+W+' '+H,preserveAspectRatio:'xMidYMid meet'});
 function X(d){return ML+pad+(d-t0)/Math.max(1,(t1-t0))*pwi}
 function Y(sd,v){var s=scale[sd];return MT+ph-(v-s.lo)/(s.hi-s.lo)*ph}
 var gs=scale.L||scale.R;
 /* 只留水平虛線格線；時間軸底線 */
 gs.ticks.forEach(function(t){var y=MT+ph-(t-gs.lo)/(gs.hi-gs.lo)*ph;svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:y,y2:y,stroke:GRID,'stroke-width':1,'stroke-dasharray':'3 3'}))});
 svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:MT+ph,y2:MT+ph,stroke:C.line,'stroke-width':1}));
 ['L','R'].forEach(function(sd){if(!scale[sd])return;var s=scale[sd];
  var nd=tnd(s.ticks);s.ticks.forEach(function(t){var y=MT+ph-(t-s.lo)/(s.hi-s.lo)*ph;
   svg.appendChild(el('text',{x:sd==='L'?ML-5:W-MR+5,y:y+3.5,'text-anchor':sd==='L'?'end':'start','class':'axl'},fmt(t,nd)+(pct[sd]?'%':'')))})});
 /* x ticks */
 var span=(t1-t0)/365.25,d0=new Date(t0*86400000),y0=d0.getUTCFullYear();
 var stepY=span>30?10:span>14?5:span>6?2:1,ppy=pw/Math.max(span,0.01);
 [1,2,5,10,20,50].some(function(k){if(k>=stepY&&k*ppy>=44){stepY=k;return true}return false});
 var stepM=[2,3,4,6,12].filter(function(k){return k*ppy/12>=60})[0]||12;
 if(span<=1.6){for(var m=0;m<24;m++){var dd=Date.UTC(d0.getUTCFullYear(),d0.getUTCMonth()+m,1)/86400000;if(dd<t0||dd>t1)continue;var dt=new Date(dd*86400000);
   if(dt.getUTCMonth()%stepM)continue;svg.appendChild(el('text',{x:X(dd),y:H-6,'text-anchor':'middle','class':'axl axx'},dt.getUTCFullYear()+'-'+('0'+(dt.getUTCMonth()+1)).slice(-2)))}}
 else{for(var y=Math.ceil(y0/stepY)*stepY;y<=new Date(t1*86400000).getUTCFullYear();y+=stepY){var dd2=Date.UTC(y,0,1)/86400000;if(dd2<t0||dd2>t1)continue;
   svg.appendChild(el('text',{x:X(dd2),y:H-6,'text-anchor':'middle','class':'axl axx'},''+y))}}
 /* zero line */
 ['L','R'].forEach(function(sd){var s=scale[sd];if(s&&s.lo<0&&s.hi>0&&sd===(scale.L?'L':'R'))svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(sd,0),y2:Y(sd,0),stroke:C.muted,'stroke-width':1}))});
 var stackAcc={},bi=0;var soloBar=series.filter(function(q){return q.kind==='bar'}).length===1&&!series.some(function(q){return q.kind==='stack'});
 var idx={};D.series.forEach(function(s,i){idx[s.id]=i});
 /* 堆疊柱只有最外層那段圓角：先找出每個日期正、負向最後一段 */
 var outP={},outN={};series.forEach(function(s){if(s.kind!=='stack')return;for(var i=0;i<s.d.length;i++){if(s.v[i]==null)continue;(s.v[i]>=0?outP:outN)[s.d[i]]=s.id}});
 var defs=el('defs',{}),gid={},uq=++uid;svg.insertBefore(defs,svg.firstChild);
 function grad(c,x2,a1,a2,o1,o2){var k=c+x2+o1,id=gid[k];if(id)return id;id=gid[k]='g'+uq+'_'+(++uid);
  var g=el('linearGradient',{id:id,x1:0,y1:0,x2:0,y2:1});g.appendChild(el('stop',{offset:0,'stop-color':a1,'stop-opacity':o1}));g.appendChild(el('stop',{offset:1,'stop-color':a2,'stop-opacity':o2}));defs.appendChild(g);return id}
 function barFill(c){return 'url(#'+grad(c,'b',BARG[c]||lite(c),c,1,1)+')'}
 /* 柱：朝外端圓角（正值上、負值下），另一端直角 */
 function barPath(x,w,yt,yb,pos){var h=yb-yt,r=Math.min(5,w/2,h);
  return pos?'M'+x+' '+yb+'L'+x+' '+(yt+r)+'Q'+x+' '+yt+' '+(x+r)+' '+yt+'L'+(x+w-r)+' '+yt+'Q'+(x+w)+' '+yt+' '+(x+w)+' '+(yt+r)+'L'+(x+w)+' '+yb+'Z'
   :'M'+x+' '+yt+'L'+x+' '+(yb-r)+'Q'+x+' '+yb+' '+(x+r)+' '+yb+'L'+(x+w-r)+' '+yb+'Q'+(x+w)+' '+yb+' '+(x+w)+' '+(yb-r)+'L'+(x+w)+' '+yt+'Z'}
 var ends=[],firstLine=true,nLine=series.filter(function(q){return q.kind!=='bar'&&q.kind!=='stack'}).length;
 series.forEach(function(s){var sd=s.axis==='R'?'R':'L';if(!scale[sd])return;var col=PAL[idx[s.id]%PAL.length];
  if(s.kind==='bar'||s.kind==='stack'){
   /* 多條非堆疊柱：同日期左右並排，柱間留 1px */
   var bws=side?(bw-(nbar-1))/nbar:bw,bo=side?bi*(bws+1):0;if(s.kind==='bar')bi++;
   for(var i=0;i<s.d.length;i++){var d=s.d[i],v=s.v[i];if(v==null||d<t0||d>t1)continue;var y0v=0,y1v=v;
    if(s.kind==='stack'){var a=stackAcc[d]=stackAcc[d]||[0,0];if(v>=0){y0v=a[1];y1v=a[1]+v;a[1]=y1v}else{y0v=a[0];y1v=a[0]+v;a[0]=y1v}}
    var ya=Y(sd,y0v),yb=Y(sd,y1v),bx=+(X(d)-bw/2+bo).toFixed(1),yt=Math.min(ya,yb),yh=Math.max(0.5,Math.abs(ya-yb));
    var fc=(s.kind==='bar'&&soloBar)?(v>=0?C.pos:C.neg):col,rnd=s.kind==='bar'||(v>=0?outP:outN)[d]===s.id;
    if(rnd)svg.appendChild(el('path',{d:barPath(bx,+bws.toFixed(1),+yt.toFixed(1),+(yt+yh).toFixed(1),v>=0),fill:barFill(fc)}));
    else svg.appendChild(el('rect',{x:bx,y:yt,width:bws,height:yh,fill:barFill(fc)}))}
  }else{
   var runs=[],cur=null;
   for(var j=0;j<s.d.length;j++){var d2=s.d[j];if(d2<t0||d2>t1)continue;var v2=s.v[j];if(v2==null){cur=null;continue}
    if(!cur){cur=[];runs.push(cur)}cur.push([X(d2),Y(sd,v2)])}
   var p='',ap='';
   var sc2=scale[sd],zy=(sc2.lo<0&&sc2.hi>0)?Y(sd,0):MT+ph;
   runs.forEach(function(r){if(r.length<2)return;var seg='M'+r[0][0].toFixed(1)+' '+r[0][1].toFixed(1)+mono(r);p+=seg;
    ap+=seg+'L'+r[r.length-1][0].toFixed(1)+' '+zy.toFixed(1)+'L'+r[0][0].toFixed(1)+' '+zy.toFixed(1)+'Z'});
   /* 無柱且目前只畫一條線時，線下方加垂直漸層面積 */
   if(nLine===1&&!hasBar&&ap)svg.appendChild(el('path',{d:ap,fill:'url(#'+grad(col,'a',col,col,col==='#0d2244'?0.10:0.18,0)+')',stroke:'none'}));
   if(p)svg.appendChild(el('path',{d:p,fill:'none',stroke:col,'stroke-width':firstLine?2.8:2,'stroke-linejoin':'round','stroke-linecap':'round','stroke-dasharray':s.dash?'5 3':''}));
   firstLine=false;
   for(var e=s.d.length-1;e>=0;e--){if(s.d[e]<=t1&&s.d[e]>=t0&&s.v[e]!=null){ends.push(el('circle',{cx:X(s.d[e]),cy:Y(sd,s.v[e]),r:3.2,fill:col,stroke:'#fff','stroke-width':1.5}));break}}
   /* 稀疏序列加點 */
   var cnt=0;for(var q=0;q<s.d.length;q++){if(s.d[q]>=t0&&s.d[q]<=t1)cnt++}
   if(cnt<=40){for(var q2=0;q2<s.d.length;q2++){if(s.d[q2]>=t0&&s.d[q2]<=t1&&s.v[q2]!=null)svg.appendChild(el('circle',{cx:X(s.d[q2]),cy:Y(sd,s.v[q2]),r:2.5,fill:col}))}}
  }});
 ends.forEach(function(c){svg.appendChild(c)});
 /* hover */
 var line=el('line',{y1:MT,y2:MT+ph,stroke:'#c9bfa8','stroke-dasharray':'3 3',visibility:'hidden'});svg.appendChild(line);var hg=el('g',{});svg.appendChild(hg);
 var tip=document.createElement('div');tip.className='tip';
 host.appendChild(svg);host.appendChild(tip);
 function move(ev){var r=svg.getBoundingClientRect();var px=(ev.clientX-r.left)/r.width*W;if(px<ML||px>W-MR){leave();return}
  var td=t0+(px-ML-pad)/pwi*(t1-t0);var rows=[],best=null,bd=1e9;
  series.forEach(function(s){var i=bisect(s.d,td);var c=[i-1,i].filter(function(k){return k>=0&&k<s.d.length&&s.v[k]!=null&&s.d[k]>=t0&&s.d[k]<=t1});
   if(!c.length)return;c.sort(function(a,b){return Math.abs(s.d[a]-td)-Math.abs(s.d[b]-td)});var k=c[0];
   if(Math.abs(s.d[k]-td)<bd){bd=Math.abs(s.d[k]-td);best=s.d[k]}
   rows.push([s,k])});
  if(best==null){leave();return}
  var h='<b>'+dstr(best)+'</b>';hg.innerHTML='';
  rows.forEach(function(r2){var s=r2[0],k=r2[1];if(Math.abs(s.d[k]-best)>Math.max(40,(t1-t0)/60))return;
   if(s.kind!=='bar'&&s.kind!=='stack'&&scale[s.axis==='R'?'R':'L'])hg.appendChild(el('circle',{cx:X(s.d[k]),cy:Y(s.axis==='R'?'R':'L',s.v[k]),r:4,fill:PAL[idx[s.id]%PAL.length],stroke:'#fff','stroke-width':2}));h+='<br><i class="dot" style="background:'+PAL[idx[s.id]%PAL.length]+'"></i>'+s.label+'　'+fmtS(s,s.v[k])+(s.u?(' '+s.u):'')});
  tip.innerHTML=h;tip.style.display='block';line.setAttribute('x1',X(best));line.setAttribute('x2',X(best));line.setAttribute('visibility','visible');
  var tw=tip.offsetWidth,left=(X(best)/W)*r.width+12;if(left+tw>r.width)left=(X(best)/W)*r.width-tw-12;tip.style.left=Math.max(0,left)+'px';tip.style.top='6px'}
 function leave(){hg.innerHTML='';tip.style.display='none';line.setAttribute('visibility','hidden')}
 svg.addEventListener('pointermove',move);svg.addEventListener('pointerleave',leave);svg.addEventListener('pointerdown',move)};
Chart.prototype.drawScatter=function(series,t0,t1,W,H){
 var host=this.host,xs=null,ys=null;
 this.data.series.forEach(function(s){if(s.axis==='X')xs=s;if(s.axis==='Y')ys=s});
 var ym={};ys.d.forEach(function(d,i){ym[d]=ys.v[i]});
 var pts=[];xs.d.forEach(function(d,i){if(d>=t0&&d<=t1&&ym[d]!=null&&xs.v[i]!=null)pts.push([d,xs.v[i],ym[d]])});
 var ph=H-MT-MB;
 var sx=nice(Math.min.apply(null,pts.map(function(p){return p[1]})),Math.max.apply(null,pts.map(function(p){return p[1]})),5);
 var sy=nice(Math.min.apply(null,pts.map(function(p){return p[2]})),Math.max.apply(null,pts.map(function(p){return p[2]})),5);
 var mg=marg(tl(sy)),ML=mg[0],MR=mg[1],pw=W-ML-MR;
 var svg=el('svg',{viewBox:'0 0 '+W+' '+H});
 function X(v){return ML+(v-sx.lo)/(sx.hi-sx.lo)*pw}function Y(v){return MT+ph-(v-sy.lo)/(sy.hi-sy.lo)*ph}
 var ndy=tnd(sy.ticks),ndx=tnd(sx.ticks);
 sy.ticks.forEach(function(t){svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(t),y2:Y(t),stroke:GRID,'stroke-width':1,'stroke-dasharray':'3 3'}));svg.appendChild(el('text',{x:ML-5,y:Y(t)+3.5,'text-anchor':'end','class':'axl'},fmt(t,ndy)))});
 svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:MT+ph,y2:MT+ph,stroke:C.line,'stroke-width':1}));
 sx.ticks.forEach(function(t){svg.appendChild(el('text',{x:X(t),y:H-6,'text-anchor':'middle','class':'axl axx'},fmt(t,ndx)))});
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
  var h=(location.hash||'').slice(1);show(/^[a-z]{2}$/.test(h)&&document.querySelector('[data-sec='+h+']')?h:'us')}};
})();
