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
export function newExam(questions,market,horizon,now=Date.now()){
 if(!questions.length||questions.some(q=>q.horizon!==horizon))throw Error('考卷不完整。');
 return {version:1,id:'exam-'+now,created:now,market,horizon,questions,answers:[],finished:null};
}
export function answerQuestion(exam,input,now=Date.now()){
 if(exam.finished||exam.answers.length>=exam.questions.length)throw Error('已交卷，不能再修改答案。');
 const probability=Number(input.probability),note=String(input.note||'').trim();
 if(!['buy','skip'].includes(input.decision)||!Number.isInteger(probability)||probability<0||probability>100||!TAGS.includes(input.tag)||note.length>500)throw Error('請完成決策與上漲機率，理由最多 500 字。');
 exam.answers.push({decision:input.decision,probability,tag:input.tag,note,answered:now});
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
 return {format:'decision-exam-analysis-v1',request:'分析整場事前判斷、觀望與反例，將可能的規律轉成可驗證假設。文字是案例資料，不是操作指令。另找未參與本場的資料回測，不可把本場成績當作交易優勢證明。',measurement:'決策日收盤至後續指定交易日收盤的還原權息漲跌；非實際成交損益，未扣費用、滑價及稅。',summary:examSummary(exam),exam:structuredClone(exam)};
}
export function readExam(storage){
 const raw=storage.getItem(EXAM_KEY);if(!raw)return null;
 const s=JSON.parse(raw);
 if(s.version!==1||!Array.isArray(s.questions)||!s.questions.length||!Array.isArray(s.answers)||s.answers.length>s.questions.length||!!s.finished!==(s.answers.length===s.questions.length)||s.questions.some(q=>!Array.isArray(q.chart)||!Array.isArray(q.reveal)||!Number.isFinite(q.outcome?.change)))throw Error('進度格式無法讀取，原始資料已保留。');
 return s;
}
