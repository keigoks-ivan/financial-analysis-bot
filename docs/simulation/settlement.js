export function settlementDate(market,date,calendar){
  const days=market==='TW'?2:date>='2024-05-28'?1:date>='2017-09-05'?2:3;
  const next=calendar.filter(d=>d>date);return next[days-1]||null;
}
export function lockedDirection(bar,previous){
  if(!previous||bar.date<'2015-06-01'||bar.high!==bar.low)return 0;
  const reference=previous.close/(bar.split||1)-(bar.dividend||0);
  if(reference<=0)return 0;const change=bar.open/reference-1;
  return change>=.098?1:change<=-.098?-1:0;
}
export function settleReceivables(e,date){
  for(const r of e.receivables)if(!r.paid&&r.due&&r.due<=date){e.cash=Math.round((e.cash+r.amount)*100)/100;r.paid=true;e.events.push({time:e.time,message:(r.kind==='dividend'?'股息':'交割款')+'已入帳 '+e.data.stock.currency+' '+r.amount.toFixed(2)+'。'});}
}
