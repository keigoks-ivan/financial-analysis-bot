export function visibleDailyBars(bars,cutoff=Infinity){
  return bars.filter(b=>b.openTime<=cutoff).map(b=>b.time<=cutoff?b:{...b,time:b.openTime,high:b.open,low:b.open,close:b.open,volume:0});
}
export function aggregateCalendar(bars,frame){
  if(frame===86400)return bars;
  const result=[];
  for(const b of bars){
    const d=new Date((b.date&&/^\d{4}-/.test(b.date)?b.date:new Date(b.time*1000).toISOString().slice(0,10))+'T00:00:00Z');
    if(frame===604800)d.setUTCDate(d.getUTCDate()-(d.getUTCDay()+6)%7);else d.setUTCDate(1);
    const key=d.toISOString().slice(0,10);let a=result.at(-1);
    if(!a||a.key!==key){a={...b,key,openTime:b.openTime??b.time,time:b.time,endTime:b.time};result.push(a);}
    else{a.high=Math.max(a.high,b.high);a.low=Math.min(a.low,b.low);a.close=b.close;a.volume+=b.volume;a.endTime=b.time;}
  }
  return result;
}
// Flat-to-flat campaigns combine scale-ins and partial exits; never count fills as wins.
export function tradeStatistics(fills){
  const trades=[];let position=0,current=null;
  for(const f of fills){
    const closeQty=f.closing||0,openQty=f.qty-closeQty;
    if(!current&&openQty){current={start:f.time,end:f.time,side:f.side,net:0,gross:0,fees:0,qty:0,reason:f.reason||''};}
    if(current){const fraction=closeQty&&openQty?closeQty/f.qty:1;current.gross+=f.realized||0;current.fees+=f.fee*fraction;current.net=current.gross-current.fees;current.end=f.time;current.qty+=closeQty?0:Math.max(0,openQty);}
    // Quantity after splits is reconstructed from closing quantities where necessary.
    position+=f.side*f.qty;
    if(f.positionAfter!==undefined)position=f.positionAfter;
    if(current&&(position===0||(openQty&&closeQty))){trades.push(current);current=null;}
    if(openQty&&closeQty){position=f.side*openQty;current={start:f.time,end:f.time,side:f.side,net:-f.fee*openQty/f.qty,gross:0,fees:f.fee*openQty/f.qty,qty:openQty,reason:f.reason||''};}
  }
  const wins=trades.filter(t=>t.net>0),losses=trades.filter(t=>t.net<0),profit=wins.reduce((s,t)=>s+t.net,0),loss=-losses.reduce((s,t)=>s+t.net,0);
  let streak=0,maxLossStreak=0;for(const t of trades){streak=t.net<0?streak+1:0;maxLossStreak=Math.max(streak,maxLossStreak);}
  return {trades,count:trades.length,winRate:trades.length?wins.length/trades.length:null,averageWin:wins.length?profit/wins.length:null,averageLoss:losses.length?-loss/losses.length:null,profitFactor:loss?profit/loss:profit?Infinity:null,maxLossStreak,open:current};
}
export function sizePosition({equity,riskPercent,entry,stop,multiplier=1,available,margin=0,feePerUnit=0,maxQty=100000}){
  const risk=equity*riskPercent/100,perUnit=Math.abs(entry-stop)*multiplier+feePerUnit;
  if(!(risk>0&&perUnit>0&&entry>0&&stop>0))return {qty:0,risk:0,perUnit:0};
  const capacity=Math.floor(Math.max(0,available)/(margin||entry+feePerUnit));
  const qty=Math.max(0,Math.min(maxQty,capacity,Math.floor(risk/perUnit)));
  return {qty,risk:qty*perUnit,perUnit,budget:risk};
}
