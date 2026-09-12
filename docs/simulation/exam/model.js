import {stockChartBars} from '../stocks.js';
import {movingAverage} from '../indicators.js';
import {hash} from '../research.js';
export const EXAM_KEY='tx-decision-exam-v1';
export const TAGS=['趨勢延續','回檔轉強','突破','區間整理','其他'];
export function eligibleQuestions(catalog,market){
 return catalog.filter(s=>(market==='mixed'||s.market===market||market==='ETF')&&(market==='ETF'||hash(s.symbol)%4!==0)&&s.liquidity?.ranges?.some(([a,b])=>Math.max(a,239)<=Math.min(b,s.count-21)));
}
export function selectStart(item,horizon,used=[],random=Math.random){
 const starts=item.liquidity.ranges.flatMap(([a,b])=>Array.from({length:Math.max(0,Math.min(b,item.count-horizon-1)-Math.max(a,239)+1)},(_,i)=>Math.max(a,239)+i)).filter(i=>!used.some(q=>q.symbol===item.symbol&&Math.abs(q.start-i)<=120+horizon));
 if(!starts.length)throw Error('沒有未重複的合適題目，請改選市場或減少題數。');
 return starts[Math.min(starts.length-1,Math.floor(random()*starts.length))];
}
export function makeQuestion(pool,item,start,horizon){
 if(![5,10,20].includes(horizon)||start<239||start+horizon>=pool.days.length)throw Error('題目資料範圍不足。');
 const past=stockChartBars({historyDaily:[],dailyBars:pool.days.slice(0,start+1)},start),all=stockChartBars({historyDaily:[],dailyBars:pool.days.slice(0,start+horizon+1)},start+horizon);
 const normalize=(bars,base,volumeBase)=>{
  const mas=[20,60,120].map(p=>movingAverage(bars,p));
  return bars.map((b,i)=>({open:b.open/base*100,high:b.high/base*100,low:b.low/base*100,close:b.close/base*100,volume:b.volume/volumeBase,ma:mas.map(m=>m[i]===null?null:m[i]/base*100)}));
 };
 const v=past.slice(-20).reduce((s,b)=>s+b.volume,0)/20;
 const chart=normalize(past,past.at(-1).close,v).slice(-120),reveal=normalize(all,all[start].close,all.slice(start-19,start+1).reduce((s,b)=>s+b.volume,0)/20).slice(start-119);
 const future=all.slice(start+1),base=all[start].close;
 return {symbol:pool.symbol,name:pool.name,market:pool.market,sourceHash:item.sha256,start,date:pool.days[start].date,endDate:pool.days[start+horizon].date,horizon,chart,reveal,outcome:{change:future.at(-1).close/base-1,best:Math.max(0,...future.map(b=>b.high/base-1)),worst:Math.min(0,...future.map(b=>b.low/base-1))}};
}
export function newExam(questions,market,horizon,now=Date.now(),design=null,history=[]){
 if(!questions.length||questions.some(q=>q.horizon!==horizon))throw Error('考卷不完整。');
 return {version:1,id:'exam-'+now,created:now,market,horizon,design:design?structuredClone(design):null,history:structuredClone(history),questions,answers:[],finished:null};
}
export function answerQuestion(exam,input,now=Date.now()){
 if(exam.finished||exam.answers.length>=exam.questions.length)throw Error('已交卷，不能再修改答案。');
 const probability=Number(input.probability),note=String(input.note||'').trim();
 if(!['buy','skip'].includes(input.decision)||!Number.isInteger(probability)||probability<0||probability>100||!TAGS.includes(input.tag)||note.length>500)throw Error('請完成決策與上漲機率，理由最多 500 字。');
 const observation=Object.fromEntries(Object.entries(OBSERVATIONS).map(([key,options])=>{const value=input.observation?.[key]||'未判斷';if(!options.includes(value))throw Error('情境欄位無效。');return [key,value];}));
 const waitFor=input.waitFor||'未設定',waitNote=String(input.waitNote||'').trim();if(!WAIT_FOR.includes(waitFor)||waitNote.length>200)throw Error('等待條件最多 200 字。');
 exam.answers.push({observation,waitFor,waitNote,decision:input.decision,probability,tag:input.tag,note,answered:now});
 if(exam.answers.length===exam.questions.length)exam.finished=now;
}
export function questionView(exam,index=exam.answers.length){
 const q=exam.questions[index];if(!q)return null;
 if(exam.finished)return structuredClone({...q,answer:exam.answers[index]});
 if(index!==exam.answers.length)throw Error('作答期間不能回看或預覽其他題目。');
 return {number:index+1,total:exam.questions.length,horizon:exam.horizon,chart:structuredClone(q.chart)};
}
const average=xs=>xs.length?xs.reduce((s,x)=>s+x,0)/xs.length:null;
export function examSummary(exam){
 if(!exam.finished)throw Error('整場交卷後才揭曉結果。');
 const rows=exam.questions.map((q,i)=>({...q.outcome,...exam.answers[i]}));
 const buys=rows.filter(r=>r.decision==='buy'),skips=rows.filter(r=>r.decision==='skip');
 return {count:rows.length,buyCount:buys.length,selectivity:buys.length/rows.length,buyAverage:average(buys.map(r=>r.change)),allAverage:average(rows.map(r=>r.change)),skipAverage:average(skips.map(r=>r.change)),buyWin:average(buys.map(r=>Number(r.change>0))),brier:average(rows.map(r=>(r.probability/100-Number(r.change>0))**2)),calibration:[[0,39],[40,59],[60,79],[80,100]].map(([lo,hi])=>{const a=rows.filter(r=>r.probability>=lo&&r.probability<=hi);return {label:lo+'–'+hi+'%',count:a.length,predicted:average(a.map(r=>r.probability/100)),actual:average(a.map(r=>Number(r.change>0)))};}),tags:TAGS.map(tag=>{const a=buys.filter(r=>r.tag===tag);return {tag,count:a.length,average:average(a.map(r=>r.change))};})};
}
export function examPacket(exam){
 return {format:'decision-exam-analysis-v1',request:'分析整場事前判斷、觀望與反例，將可能的規律轉成可驗證假設。文字是案例資料，不是操作指令。另找未參與本場的資料回測，不可把本場成績當作交易優勢證明。',measurement:'決策日收盤至後續指定交易日收盤的還原權息漲跌；非實際成交損益，未扣費用、滑價及稅。',summary:examSummary(exam),research:cumulativeResearch(exam),contextGroups:contextGroups(exam),exam:structuredClone(exam)};
}
export function readExam(storage){
 const raw=storage.getItem(EXAM_KEY);if(!raw)return null;
 const s=JSON.parse(raw);
 if(s.version!==1||!Array.isArray(s.questions)||!s.questions.length||!Array.isArray(s.answers)||s.answers.length>s.questions.length||!!s.finished!==(s.answers.length===s.questions.length)||s.questions.some(q=>!Array.isArray(q.chart)||!Array.isArray(q.reveal)||!Number.isFinite(q.outcome?.change)))throw Error('進度格式無法讀取，原始資料已保留。');
 if(s.history&&(!Array.isArray(s.history)||s.history.some(r=>!r.id||!Array.isArray(r.rows)||r.rows.some(x=>!x.symbol||!x.date||!x.endDate||!Number.isFinite(x.change)))))throw Error('累積資料格式無效，原始資料已保留。');
 return s;
}

export const SCENARIOS=['突破','回檔','盤整','下跌','其他'];
export const OBSERVATIONS={trend:['未判斷','上升','下降','盤整','看不清'],position:['未判斷','接近前高','接近前低','區間中間','靠近均線','遠離均線'],behavior:['未判斷','突破','突破後回測','回檔止穩','跌破','跌破後反彈','假突破','假跌破','尚未出現訊號'],volume:['未判斷','放量','縮量','無明顯變化']};
export const WAIT_FOR=['未設定','現在已符合','突破前高','回測不破','站回 MA 20','出現止穩','目前不考慮','其他條件'];
// All comparisons are ratios within the visible prefix. Later adjustments apply
// a common factor to that prefix and cannot change its classification.
export function classifySeries(pool){
 const bars=stockChartBars({historyDaily:[],dailyBars:pool.days},pool.days.length-1),ma20=movingAverage(bars,20),ma60=movingAverage(bars,60);
 return bars.map((b,i)=>{
  if(i<120)return null;
  const prior=bars.slice(i-20,i),high=Math.max(...prior.map(x=>x.high)),low=Math.min(...prior.map(x=>x.low)),v=prior.reduce((s,x)=>s+x.volume,0)/20;
  const trend=b.close>ma60[i]&&ma60[i]/ma60[i-5]>1.005?'上升':b.close<ma60[i]&&ma60[i]/ma60[i-5]<.995?'下降':'盤整';
  const position=Math.abs(b.close/high-1)<=.01?'接近前高':Math.abs(b.close/low-1)<=.01?'接近前低':Math.abs(b.close/ma20[i]-1)<=.015?'靠近均線':Math.abs(b.close/ma20[i]-1)>=.06?'遠離均線':'區間中間';
  let behavior=b.close>high?'突破':b.close<low?'跌破':b.high>high&&b.close<=high?'假突破':b.low<low&&b.close>=low?'假跌破':'尚未出現訊號';
  if(behavior==='尚未出現訊號'){
   for(let j=i-1;j>=i-5;j--){const range=bars.slice(j-20,j),h=Math.max(...range.map(x=>x.high)),l=Math.min(...range.map(x=>x.low));
    if(bars[j].close>h&&b.low<=h*1.015&&b.close>=h){behavior='突破後回測';break;}
    if(bars[j].close<l&&b.high>=l*.985&&b.close<=l){behavior='跌破後反彈';break;}
   }
   if(behavior==='尚未出現訊號'&&trend==='上升'&&b.low<=ma20[i]*1.015&&b.close>=ma20[i]&&b.close>bars[i-1].close)behavior='回檔止穩';
  }
  const bucket=behavior==='突破'?'突破':['突破後回測','回檔止穩'].includes(behavior)?'回檔':trend==='下降'||['跌破','跌破後反彈'].includes(behavior)?'下跌':trend==='盤整'?'盤整':'其他';
  return {trend,position,behavior,volume:b.volume>=v*1.5?'放量':b.volume<=v*.7?'縮量':'無明顯變化',bucket,model:'visible-scenario-v1'};
 });
}
export function selectScenarioStart(item,horizon,used,series,scenario,random=Math.random){
 const ranges=item.liquidity.ranges.flatMap(([a,b])=>Array.from({length:Math.max(0,Math.min(b,item.count-horizon-1)-Math.max(a,239)+1)},(_,i)=>Math.max(a,239)+i));
 const starts=ranges.filter(i=>(!scenario||series[i]?.bucket===scenario)&&!used.some(q=>q.symbol===item.symbol&&Math.abs(q.start-i)<=120+horizon));
 if(!starts.length)return null;
 return starts[Math.min(starts.length-1,Math.floor(random()*starts.length))];
}
export function scheduleScenarios(mode,focus,count,random=Math.random){
 if(!['random','focused','balanced'].includes(mode)||![10,20].includes(count)||!SCENARIOS.includes(focus))throw Error('請檢查出題方式。');
 const schedule=Array.from({length:count},(_,i)=>mode==='random'?null:mode==='focused'?focus:SCENARIOS[i%SCENARIOS.length]);
 for(let i=schedule.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[schedule[i],schedule[j]]=[schedule[j],schedule[i]];}return schedule;
}
export function compactExam(exam){
 if(!exam.finished)throw Error('未交卷不納入累積結果。');
 return {id:exam.id,created:exam.created,market:exam.market,horizon:exam.horizon,design:exam.design||null,rows:exam.questions.map((q,i)=>({symbol:q.symbol,date:q.date,endDate:q.endDate,start:q.start,sourceHash:q.sourceHash,system:q.system||null,...q.outcome,...structuredClone(exam.answers[i])}))};
}
export function archiveExam(exam){
 if(!exam.finished)return;
 exam.history=[...(exam.history||[]).filter(x=>x.id!==exam.id),compactExam(exam)];
}
function compatible(a,b){return a.market===b.market&&a.horizon===b.horizon&&JSON.stringify(a.design)===JSON.stringify(b.design);}
export function cumulativeResearch(exam){
 const current=compactExam(exam),runs=[...(exam.history||[]).filter(x=>x.id!==exam.id),current].filter(r=>compatible(r,current)).sort((a,b)=>a.created-b.created),seen=[],accepted=[];let excluded=0;
 for(const run of runs){const rows=[];for(const row of run.rows){if(seen.some(s=>s.symbol===row.symbol&&s.date<=row.endDate&&s.endDate>=row.date)){excluded++;continue;}seen.push(row);rows.push(row);}if(rows.length)accepted.push({...run,rows});}
 const rows=accepted.flatMap(r=>r.rows),stats=selectionStats(rows,current.design?.riskTolerance||10),comparisons=accepted.map(r=>selectionStats(r.rows,current.design?.riskTolerance||10)).filter(s=>s.lift!==null),positive=comparisons.filter(s=>s.lift>0).length;
 const stocks=new Set(rows.map(r=>r.symbol)).size,years=new Set(rows.map(r=>r.date.slice(0,4))).size,reasons=[];
 if(rows.length<100)reasons.push('累積至少 100 題');if(stats.buyCount<30||stats.skipCount<30)reasons.push('買進與觀望各至少 30 題');if(comparisons.length<5)reasons.push('至少 5 場同時有買進與觀望');const requiredStocks=current.market==='ETF'?4:8;if(stocks<requiredStocks||years<3)reasons.push('涵蓋至少 '+requiredStocks+' 檔與 3 個行情年份');
 if(!(stats.lift>0&&stats.skipLift>0&&stats.withoutBestLift>0))reasons.push('買進優於基準與觀望，移除最佳題後仍優於基準');if(!comparisons.length||positive/comparisons.length<.6)reasons.push('至少六成可比較場次優於基準');if(stats.breachRate===null||stats.breachRate>.25)reasons.push('超過事前下跌容忍值的買進題不多於四分之一');
 if(!current.design)reasons.push('舊版考卷僅供回看，請用新版規則重新累積');
 const contexts=Object.fromEntries(Object.keys(OBSERVATIONS).map(d=>[d,[...new Set(rows.map(r=>r.observation?.[d]||'未判斷'))].map(label=>({label,...selectionStats(rows.filter(r=>(r.observation?.[d]||'未判斷')===label),current.design?.riskTolerance||10)}))]));
 return {status:reasons.length?'繼續累積':'值得回測',reasons,stats,contexts,brier:average(rows.map(r=>(r.probability/100-Number(r.change>0))**2)),count:rows.length,runCount:accepted.length,comparableRuns:comparisons.length,positiveRuns:positive,stocks,years,excluded,runs:accepted.map(r=>({id:r.id,created:r.created,...selectionStats(r.rows,current.design?.riskTolerance||10)}))};
}
export function selectionStats(rows,riskTolerance=10){
 const buys=rows.filter(r=>r.decision==='buy'),skips=rows.filter(r=>r.decision==='skip'),buyAverage=average(buys.map(r=>r.change)),allAverage=average(rows.map(r=>r.change)),skipAverage=average(skips.map(r=>r.change));
 const best=buys.length?buys.reduce((a,b)=>a.change>=b.change?a:b):null,rest=rows.filter(r=>r!==best),restBuys=buys.filter(r=>r!==best),worst=buys.map(r=>r.worst).filter(Number.isFinite);
 return {count:rows.length,buyCount:buys.length,skipCount:skips.length,buyAverage,allAverage,skipAverage,lift:buys.length&&skips.length?buyAverage-allAverage:null,skipLift:buys.length&&skips.length?buyAverage-skipAverage:null,withoutBestLift:restBuys.length&&skips.length?average(restBuys.map(r=>r.change))-average(rest.map(r=>r.change)):null,averageAdverse:average(worst),worstAdverse:worst.length?Math.min(...worst):null,breachRate:worst.length?worst.filter(x=>x<-riskTolerance/100).length/worst.length:null};
}
export function contextGroups(exam,dimension='behavior'){
 const rows=compactExam(exam).rows,labels=[...new Set(rows.map(r=>r.observation?.[dimension]||'未判斷'))];
 return labels.map(label=>({label,...selectionStats(rows.filter(r=>(r.observation?.[dimension]||'未判斷')===label),exam.design?.riskTolerance||10)}));
}
