import {randomFloat,randomInt} from './random.js';

function asPlans(value){return (Array.isArray(value)?value:[value]).filter(Boolean).map(x=>x.campaign??x.snapshot?.campaign??x);}
function overlap(aStart,aDays,bStart,bDays){const overlapDays=Math.max(0,Math.min(aStart+aDays-1,bStart+bDays-1)-Math.max(aStart,bStart)+1);return overlapDays/Math.min(aDays,bDays)>=.5;}
export function pickCampaign(catalog,days,random=randomFloat,previous=null){
  if(![3,5,10].includes(days))throw Error('請選擇 3、5 或 10 個交易日。');
  const windows=[];
  for(let i=0;i<=catalog.length-days;i++){
    const selected=catalog.slice(i,i+days);
    if(selected.every(d=>d.group===selected[0].group&&d.contract===selected[0].contract))windows.push(selected);
  }
  if(!windows.length)throw Error('現有連續資料不足以支援這個長度。');
  const recent=asPlans(previous).filter(p=>Array.isArray(p.ids)&&p.days===days).slice(0,5),positions=new Map(catalog.map((c,i)=>[c.id,i]));
  const fresh=windows.filter(w=>{const start=positions.get(w[0].id);return !recent.some(p=>{const prior=positions.get(p.ids[0]),priorBlock=Number.isInteger(prior)?catalog[prior]:null;return Number.isInteger(start)&&Number.isInteger(prior)&&priorBlock?.group===w[0].group&&priorBlock?.contract===w[0].contract&&overlap(start,days,prior,Number(p.days)||days);});});
  const fallback=windows.filter(w=>w[0].id!==recent[0]?.ids?.[0]),pool=fresh.length?fresh:fallback.length?fallback:windows;
  const blocks=pool[randomInt(pool.length,random)],segment=randomInt(2,random),minutes=30+randomInt(121,random);
  return {days,ids:blocks.map(b=>b.id),segment,minutes};
}
export function assembleCampaign(chunks,plan){
  if(chunks.length!==plan.days||chunks.some((c,i)=>c.id!==plan.ids[i])||chunks.some(c=>c.contract!==chunks[0].contract))throw Error('連續行情資料不一致。');
  const first=chunks[0],base=first.anchor;
  const ticks=[],segments=[];
  for(const c of chunks){
    const shift=c.anchor-base;
    for(const t of c.ticks)ticks.push([t[0]+shift,t[1],t[2]]);
    for(const s of c.segments)segments.push({...s,start:s.start+shift,end:s.end+shift});
  }
  if(ticks.some((t,i)=>i&&t[0]<ticks[i-1][0]))throw Error('行情時間不連續。');
  const playStart=segments[plan.segment].start+plan.minutes*60;
  const sourceHash=chunks.map(c=>c.sha256).join(':');
  return {id:'random:'+plan.ids.join('-')+':'+plan.segment+':'+plan.minutes,
    date:first.date,contract:first.contract,tradingDate:first.tradingDate,
    start:ticks[0][0],end:ticks.at(-1)[0],playStart,ticks,segments,historyBars:first.historyBars,
    sha256:sourceHash,count:ticks.length,reference:first.historyBars.at(-1)?.[4]??ticks[0][1],
    referenceLabel:'練習起點前參考價',sessionLabel:`隨機 ${plan.days} 日`,
    source:chunks.map(c=>c.source).join(', '),campaign:plan};
}
