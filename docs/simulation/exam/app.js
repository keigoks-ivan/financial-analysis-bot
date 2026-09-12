import {EXAM_KEY,eligibleQuestions,selectStart,makeQuestion,newExam,answerQuestion,questionView,examSummary,examPacket,readExam,classifySeries,selectScenarioStart,scheduleScenarios,archiveExam,cumulativeResearch,selectionStats,contextGroups} from './model.js';
const $=id=>document.getElementById(id),pct=n=>n===null?'—':(n*100).toFixed(1)+'%',esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let exam=null,review=0,visible=120,busy=false,storageBlocked=false,history=[];
try{exam=readExam(localStorage);}catch{$('storageStatus').textContent='無法讀取本機進度，原始資料已保留。本次可練習並下載，但不會覆寫舊資料。';storageBlocked=true;}
if(exam?.finished)archiveExam(exam);history=exam?.history||[];
function save(){
 if(exam?.finished)archiveExam(exam);history=exam?.history||history;
 if(storageBlocked)return;
 try{localStorage.setItem(EXAM_KEY,JSON.stringify(exam));$('storageStatus').textContent='';}
 catch{$('storageStatus').textContent='本機儲存失敗，本場答案仍在畫面中。請保持此頁開啟，交卷後下載分析檔；重新整理可能回到較早的進度。';}
}
async function json(path){const r=await fetch(path);if(!r.ok)throw Error('行情載入失敗，請稍後重試。');return r.json();}
$('examMode').onchange=()=>{$('focusLabel').hidden=$('examMode').value!=='focused';$('modeHelp').textContent={random:'依股票與時間隨機抽題，用來觀察整體判斷。',focused:'指定一類情境集中練習；具體分類細節在交卷後揭曉。',balanced:'五類情境各占相同題數，順序隨機；交卷前不透露每題分類。'}[$('examMode').value];};
$('waitFor').onchange=()=>{$('waitNoteLabel').hidden=$('waitFor').value!=='其他條件';};
$('groupDimension').onchange=()=>render();
$('start').onclick=async()=>{
 if(busy)return;busy=true;$('start').disabled=true;$('status').textContent='正在隨機準備考卷…';
 try{
  const market=$('market').value,horizon=Number($('horizon').value),count=Number($('count').value),catalog=await json('../data/stocks/'+(market==='ETF'?'index-etfs':'catalog')+'.json');
  const mode=$('examMode').value,focus=$('focus').value,riskTolerance=Number($('riskTolerance').value),schedule=scheduleScenarios(mode,focus,count);
  const design={version:2,classification:'visible-scenario-v1',mode,focus:mode==='focused'?focus:null,riskTolerance};
  const candidates=eligibleQuestions(catalog,market),questions=[],cache=new Map(),series=new Map(),prior=history.flatMap(r=>r.rows);
  if(!candidates.length)throw Error('目前沒有合適的題庫。');
  for(let n=0;n<count;n++){
   const shuffled=candidates.map(s=>({s,r:Math.random()})).sort((a,b)=>a.r-b.r);let item,start;
   for(const x of shuffled){
    if(!cache.has(x.s.symbol)){const pool=await json('../data/stocks/'+encodeURIComponent(x.s.symbol)+'.json');cache.set(x.s.symbol,pool);series.set(x.s.symbol,classifySeries(pool));}
    start=selectScenarioStart(x.s,horizon,[...prior,...questions],series.get(x.s.symbol),schedule[n]);
    if(start!==null){item=x.s;break;}
   }
   if(!item)throw Error('此情境的未重複題目不足，請改選市場、模式或題數。');
   const q=makeQuestion(cache.get(item.symbol),item,start,horizon);q.system=series.get(item.symbol)[start];questions.push(q);$('status').textContent=`正在準備第 ${n+1}／${count} 題…`;
  }
  exam=newExam(questions,market,horizon,Date.now(),design,history);review=0;visible=120;save();resetAnswer();render();$('status').textContent='';$('questionTitle').scrollIntoView({block:'start',behavior:'smooth'});
 }catch(e){$('status').textContent=e.message;}finally{busy=false;$('start').disabled=false;}
};
function resetAnswer(){$('answerForm').reset();$('probabilityValue').textContent='50%';$('waitNoteLabel').hidden=true;}
$('probability').oninput=()=>{$('probabilityValue').textContent=$('probability').value+'%';};
$('answerForm').onsubmit=e=>{
 e.preventDefault();if(busy||!exam||exam.finished)return;
 try{
  const decision=new FormData($('answerForm')).get('decision');
  answerQuestion(exam,{decision,probability:Number($('probability').value),tag:'其他',observation:Object.fromEntries(['trend','position','behavior','volume'].map(k=>[k,$(k).value])),waitFor:$('waitFor').value,waitNote:$('waitFor').value==='其他條件'?$('waitNote').value:'',note:$('note').value});
  save();resetAnswer();visible=120;render();$('status').textContent=exam.finished?'整場已交卷，可以回看各題與下載分析檔。':'答案已鎖定。';
  if(exam.finished)$('results').scrollIntoView({block:'start',behavior:'smooth'});
 }catch(e){$('status').textContent=e.message;}
};
$('new').onclick=()=>{
 if(!exam?.finished)return;
 if(!confirm('下一場保留跨場摘要，但不保留上一場完整圖表。已下載需要保留的分析檔嗎？'))return;
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
  const s=examSummary(exam),cumulative=cumulativeResearch(exam),risk=selectionStats(exam.questions.map((q,i)=>({...q.outcome,...exam.answers[i]})),exam.design?.riskTolerance||10);
  $('researchState').textContent=cumulative.status;
  $('researchDetail').textContent=`同規則 ${cumulative.runCount} 場、${cumulative.count} 題，${cumulative.stocks} 檔、${cumulative.years} 個行情年份；買進 ${cumulative.stats.buyCount} 題、觀望 ${cumulative.stats.skipCount} 題。`;
  $('researchNext').textContent=cumulative.reasons.length?'下一步：'+cumulative.reasons.join('；')+'。':'已達研究排程門檻。下載整場與跨場摘要，先固定交易規則，再用新資料計入成本回測。這仍不是已驗證優勢。';
  $('riskSummary').innerHTML=table(['本場指標','結果'],[['買進比全部多（百分點）',pct(risk.lift)],['買進比觀望多（百分點）',pct(risk.skipLift)],['移除最佳題後加分（百分點）',pct(risk.withoutBestLift)],['買進平均途中下跌',pct(risk.averageAdverse)],['買進最深途中下跌',pct(risk.worstAdverse)],['超過事前 '+(exam.design?.riskTolerance||10)+'% 下跌容忍',pct(risk.breachRate)]]);
  $('consistency').innerHTML=table(['累積指標','結果'],[['選擇加分（百分點）',pct(cumulative.stats.lift)],['優於全部題目的場次',cumulative.positiveRuns+'／'+cumulative.comparableRuns],['移除最佳題後加分（百分點）',pct(cumulative.stats.withoutBestLift)]]);
  $('historyInfo').textContent=`只比較相同出題模式、題庫、期間及風險容忍值。已排除 ${cumulative.excluded} 題重疊行情；同時期不同股票仍可能相關。`;
  $('summary').innerHTML=[['選擇買進',s.buyCount+'／'+s.count+' 題'],['買進題目平均',pct(s.buyAverage)],['全部題目平均',pct(s.allAverage)],['觀望題目平均',pct(s.skipAverage)]].map(([k,v])=>`<div class="metric"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`).join('');
  $('calibration').innerHTML=table(['預估機率區間','題數','平均預估','實際上漲'],s.calibration.map(c=>[c.label,c.count,pct(c.predicted),pct(c.actual)]));
  $('brier').textContent=`機率誤差（Brier）${s.brier.toFixed(3)}，越低越好；每題都猜 50% 的基準為 0.250。買進題目上漲比例 ${pct(s.buyWin)}。同規則累積機率誤差 ${cumulative.brier===null?'—':cumulative.brier.toFixed(3)}。`;
  $('tags').innerHTML=table(['事前情境','買／觀望','買進漲跌','選擇加分'],(cumulative.contexts[$('groupDimension').value]||[]).map(t=>[t.label,t.buyCount+'／'+t.skipCount,pct(t.buyAverage),pct(t.lift)]));
  const keys=['trend','position','behavior','volume'];
  $('scenarioComparison').innerHTML=table(['層次','你的判斷','系統描述'],keys.map((key,i)=>[['大方向','位置','價格行為','量能'][i],q.answer.observation?.[key]||'未判斷',q.system?.[key]||'舊題未分類']).concat([['等待條件',q.answer.waitFor||'未設定',q.answer.waitNote||'—']]));
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
