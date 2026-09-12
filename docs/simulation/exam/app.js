import {EXAM_KEY,eligibleQuestions,selectStart,makeQuestion,newExam,answerQuestion,questionView,examSummary,examPacket,readExam} from './model.js';
const $=id=>document.getElementById(id),pct=n=>n===null?'—':(n*100).toFixed(1)+'%',esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let exam=null,review=0,visible=120,busy=false,storageBlocked=false;
try{exam=readExam(localStorage);}catch{$('storageStatus').textContent='無法讀取本機進度，原始資料已保留。本次可練習並下載，但不會覆寫舊資料。';storageBlocked=true;}
function save(){
 if(storageBlocked)return;
 try{localStorage.setItem(EXAM_KEY,JSON.stringify(exam));$('storageStatus').textContent='';}
 catch{$('storageStatus').textContent='本機儲存失敗，本場答案仍在畫面中。請保持此頁開啟，交卷後下載分析檔；重新整理可能回到較早的進度。';}
}
async function json(path){const r=await fetch(path);if(!r.ok)throw Error('行情載入失敗，請稍後重試。');return r.json();}
$('start').onclick=async()=>{
 if(busy)return;busy=true;$('start').disabled=true;$('status').textContent='正在隨機準備考卷…';
 try{
  const market=$('market').value,horizon=Number($('horizon').value),count=Number($('count').value),catalog=await json('../data/stocks/'+(market==='ETF'?'index-etfs':'catalog')+'.json');
  const candidates=eligibleQuestions(catalog,market),questions=[],cache=new Map();
  if(!candidates.length)throw Error('目前沒有合適的題庫。');
  for(let n=0;n<count;n++){
   const shuffled=candidates.map(s=>({s,r:Math.random()})).sort((a,b)=>a.r-b.r);let item,start;
   for(const x of shuffled){try{start=selectStart(x.s,horizon,questions);item=x.s;break;}catch{}}
   if(!item)throw Error('合適題目不足，請減少題數。');
   if(!cache.has(item.symbol))cache.set(item.symbol,await json('../data/stocks/'+encodeURIComponent(item.symbol)+'.json'));
   questions.push(makeQuestion(cache.get(item.symbol),item,start,horizon));$('status').textContent=`正在準備第 ${n+1}／${count} 題…`;
  }
  exam=newExam(questions,market,horizon);review=0;visible=120;save();resetAnswer();render();$('status').textContent='';$('questionTitle').scrollIntoView({block:'start',behavior:'smooth'});
 }catch(e){$('status').textContent=e.message;}finally{busy=false;$('start').disabled=false;}
};
function resetAnswer(){$('answerForm').reset();$('probabilityValue').textContent='50%';}
$('probability').oninput=()=>{$('probabilityValue').textContent=$('probability').value+'%';};
$('answerForm').onsubmit=e=>{
 e.preventDefault();if(busy||!exam||exam.finished)return;
 try{
  const decision=new FormData($('answerForm')).get('decision');
  answerQuestion(exam,{decision,probability:Number($('probability').value),tag:$('tag').value,note:$('note').value});
  save();resetAnswer();visible=120;render();$('status').textContent=exam.finished?'整場已交卷，可以回看各題與下載分析檔。':'答案已鎖定。';
  if(exam.finished)$('results').scrollIntoView({block:'start',behavior:'smooth'});
 }catch(e){$('status').textContent=e.message;}
};
$('new').onclick=()=>{
 if(!exam?.finished)return;
 if(!confirm('開始下一場會取代此裝置的考卷。已下載需要保留的分析檔嗎？'))return;
 exam=null;render();$('status').textContent='選好題庫後即可開始。上一場仍保存到新考卷準備完成為止。';$('setup').scrollIntoView({block:'start',behavior:'smooth'});
};
$('download').onclick=()=>{
 try{const packet=examPacket(exam),blob=new Blob([JSON.stringify(packet,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=exam.id+'-analysis.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(e){$('status').textContent=e.message;}
};
function table(head,rows){return '<table><thead><tr>'+head.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(c=>'<td>'+esc(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
function render(){
 $('setup').hidden=!!exam;$('exam').hidden=!exam;$('results').hidden=!exam?.finished;
 if(!exam)return;
 $('answerForm').hidden=!!exam.finished;$('progressBar').max=exam.questions.length;$('progressBar').value=exam.answers.length;
 const q=questionView(exam,exam.finished?review:exam.answers.length);
 $('progress').textContent=exam.finished?`第 ${review+1}／${exam.questions.length} 題 · 已揭曉`:`第 ${q.number}／${q.total} 題 · 身分隱藏`;
 $('questionTitle').textContent=exam.finished?q.name+' · '+q.symbol:'這個位置，你會買進嗎？';
 $('period').textContent='後 '+exam.horizon+' 個交易日';
 $('chartCaption').textContent=exam.finished?`${q.date} → ${q.endDate} · 虛線為決策日；右側為後續走勢。${q.answer.decision==='buy'?'買進':'觀望'}，預估上漲機率 ${q.answer.probability}%。理由：${q.answer.note||'未填寫'}。`:'價格以決策日收盤＝100 呈現；下方為相對成交量。紅漲綠跌。';
 $('submit').textContent=exam.answers.length===exam.questions.length-1?'鎖定最後一題，交卷揭曉 →':'鎖定答案，下一題 →';
 if(exam.finished){
  const s=examSummary(exam);
  $('summary').innerHTML=[['選擇買進',s.buyCount+'／'+s.count+' 題'],['買進題目平均',pct(s.buyAverage)],['全部題目平均',pct(s.allAverage)],['觀望題目平均',pct(s.skipAverage)]].map(([k,v])=>`<div class="metric"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`).join('');
  $('calibration').innerHTML=table(['預估機率區間','題數','平均預估','實際上漲'],s.calibration.map(c=>[c.label,c.count,pct(c.predicted),pct(c.actual)]));
  $('brier').textContent=`機率誤差（Brier）${s.brier.toFixed(3)}，越低越好；每題都猜 50% 的基準為 0.250。買進題目上漲比例 ${pct(s.buyWin)}。`;
  $('tags').innerHTML=table(['情境','買進題數','平均漲跌'],s.tags.map(t=>[t.tag,t.count,pct(t.average)]));
  $('reviewList').replaceChildren();
  exam.questions.forEach((q,i)=>{const a=exam.answers[i],b=document.createElement('button');b.className=i===review?'selected':'';b.textContent=`${i+1}. ${q.name} (${q.symbol}) · ${a.decision==='buy'?'買進':'觀望'} · ${pct(q.outcome.change)}｜最高 ${pct(q.outcome.best)}／最低 ${pct(q.outcome.worst)}`;b.onclick=()=>{review=i;visible=120;render();$('questionTitle').scrollIntoView({block:'start',behavior:'smooth'});};$('reviewList').append(b);});
 }
 draw();
}
function draw(){
 if(!exam)return;
 const view=questionView(exam,exam.finished?review:exam.answers.length),all=exam.finished?view.reveal:view.chart,extra=exam.finished?exam.horizon:0,start=Math.max(0,120-visible),bars=all.slice(start),canvas=$('chart'),w=canvas.clientWidth,h=canvas.clientHeight,dpr=window.devicePixelRatio||1;
 canvas.width=w*dpr;canvas.height=h*dpr;const c=canvas.getContext('2d');c.scale(dpr,dpr);c.clearRect(0,0,w,h);
 const left=10,right=w-54,top=22,bottom=h-85,values=bars.flatMap(b=>[b.high,b.low,...b.ma.filter(v=>v!==null)]),min=Math.min(...values),max=Math.max(...values),pad=(max-min)*.07||1,low=min-pad,high=max+pad,y=p=>top+(high-p)/(high-low)*(bottom-top),step=(right-left)/bars.length,x=i=>left+(i+.5)*step;
 c.font='11px system-ui';c.textAlign='left';
 for(let i=0;i<=4;i++){const price=low+(high-low)*i/4,yy=y(price);c.strokeStyle='#303745';c.beginPath();c.moveTo(left,yy);c.lineTo(right,yy);c.stroke();c.fillStyle='#a7b0bf';c.fillText(price.toFixed(1),right+6,yy+4);}
 const maxVolume=Math.max(1,...bars.map(b=>b.volume));
 bars.forEach((b,i)=>{c.strokeStyle=c.fillStyle=b.close>=b.open?'#f17c87':'#5cc6aa';c.beginPath();c.moveTo(x(i),y(b.high));c.lineTo(x(i),y(b.low));c.stroke();c.fillRect(x(i)-Math.max(1,step*.65)/2,Math.min(y(b.open),y(b.close)),Math.max(1,step*.65),Math.max(1,Math.abs(y(b.open)-y(b.close))));c.globalAlpha=.45;c.fillRect(x(i)-step*.32,h-25-b.volume/maxVolume*42,Math.max(1,step*.65),b.volume/maxVolume*42);c.globalAlpha=1;});
 ['#d8fb70','#75baff','#d6a4ff'].forEach((color,k)=>{c.strokeStyle=color;c.lineWidth=1.3;c.beginPath();let started=false;bars.forEach((b,i)=>{if(b.ma[k]===null)return;if(!started){c.moveTo(x(i),y(b.ma[k]));started=true;}else c.lineTo(x(i),y(b.ma[k]));});c.stroke();});
 if(extra){const at=119-start,xx=x(at)+step/2;c.fillStyle='#d8fb700b';c.fillRect(xx,top,right-xx,h-top-20);c.strokeStyle='#d8fb70';c.setLineDash([4,4]);c.beginPath();c.moveTo(xx,top);c.lineTo(xx,h-23);c.stroke();c.setLineDash([]);c.fillStyle='#d8fb70';c.textAlign='right';c.fillText('決策日',xx-4,15);}
 c.fillStyle='#a7b0bf';c.textAlign='left';c.fillText('−'+(119-start)+' 日',left,h-7);c.textAlign='right';c.fillText(extra?'＋'+extra+' 交易日':'決策日',right,h-7);
 canvas.setAttribute('aria-label',`${exam.finished?'已揭曉':'盲測'}日 K，共 ${bars.length} 根，MA 20／60／120，決策日價格 100。`);
}
function zoom(delta){visible=Math.max(40,Math.min(120,visible+delta));draw();}
$('zoomIn').onclick=()=>zoom(-20);$('zoomOut').onclick=()=>zoom(20);
$('chart').addEventListener('wheel',e=>{if(!exam)return;e.preventDefault();zoom(e.deltaY>0?10:-10);},{passive:false});
new ResizeObserver(()=>draw()).observe($('chart'));
render();
