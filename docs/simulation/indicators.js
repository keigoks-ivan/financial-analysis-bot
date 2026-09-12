// Taiwan futures sessions anchor intraday bars at 08:45 and 15:00.
export function candleBucket(second, frame) {
  let adjusted=second;
  const tod=((second%86400)+86400)%86400;
  if(tod===18000||tod===49500)adjusted-=0.001;
  const day=Math.floor(adjusted/86400)*86400;
  const clock=adjusted-day;
  const start=clock>=31500&&clock<49500?day+31500:clock>=54000?day+54000:day-86400+54000;
  return start+Math.floor((adjusted-start)/frame)*frame;
}
export function movingAverage(bars,period) {
  let sum=0;
  return bars.map((b,i)=>{
    sum+=b.close;
    if(i>=period)sum-=bars[i-period].close;
    return i+1>=period?sum/period:null;
  });
}
export function aggregateHistory(history,frame){
  const result=[];
  for(const row of history){
    const [time,open,high,low,close,volume]=row,key=candleBucket(time,frame);
    let b=result.at(-1);
    if(!b||b.time!==key){b={time:key,open,high,low,close,volume:0};result.push(b);}
    b.high=Math.max(b.high,high);b.low=Math.min(b.low,low);b.close=close;b.volume+=volume;
  }
  return result;
}

export function zoomViewport(visible,offset,total,factor,anchor=0.5){
  const next=Math.max(12,Math.min(300,Math.round(visible*factor)));
  const right=Math.round(offset+(visible-next)*(1-Math.max(0,Math.min(1,anchor))));
  return {visible:next,offset:Math.max(0,Math.min(Math.max(0,total-next),right))};
}
