export function validateProtection(side,entry,stop,target){
  stop=Number(stop)||null;target=Number(target)||null;
  if(stop!==null&&(!Number.isFinite(stop)||stop<=0||(stop-entry)*side>=0))throw Error('停損必須在進場價的不利方向。');
  if(target!==null&&(!Number.isFinite(target)||target<=0||(target-entry)*side<=0))throw Error('停利必須在進場價的有利方向。');
  return stop||target?{stop,target,triggered:false}:null;
}
export function updateProtectionAfterFill(e,o,before){
  if(!e.position){e.protection=null;return;}
  if(!before||Math.sign(before)!==Math.sign(e.position))e.protection=o.protection?{...o.protection,triggered:false}:null;
  else if(o.protection)e.protection={...o.protection,triggered:false};
}
export function protectionHit(p,side,b){
  if(!p||p.triggered)return null;
  const stopGap=p.stop&&(b.open-p.stop)*side<=0,targetGap=p.target&&(b.open-p.target)*side>=0;
  if(stopGap)return {price:b.open,kind:'停損跳空',atOpen:true};
  if(targetGap)return {price:b.open,kind:'停利跳空',atOpen:true};
  const stop=p.stop&&(side===1?b.low<=p.stop:b.high>=p.stop),target=p.target&&(side===1?b.high>=p.target:b.low<=p.target);
  if(stop)return {price:p.stop,kind:target?'同根觸及停損與停利，保守先停損':'停損',atOpen:false};
  if(target)return {price:p.target,kind:'停利',atOpen:false};
  return null;
}
export function executeDailyProtection(e,b){
  if(!e.position||!e.protection)return;
  const hit=protectionHit(e.protection,Math.sign(e.position),b);if(!hit)return;
  for(const o of e.orders)if(o.status==='pending'||o.status==='partial'){o.status='cancelled';o.message='持倉保護觸發，取消其他委託';}
  const time=hit.atOpen?b.openTime:b.time;e.time=time;e.last=hit.price;
  const o=e.submit({side:-Math.sign(e.position),qty:Math.abs(e.position),reduceOnly:true,system:true,reason:hit.kind});
  if(e.position)e.executeOpen(o,hit.price,time);
  e.events.push({time,message:hit.kind+(o.status==='filled'?'；日線區間估算成交，未推定盤中先後。':'未成交；'+o.message)});
}
export function triggerTickProtection(e,time,price){
  if(!e.position||!e.protection||e.protection.triggered)return;
  const hit=protectionHit(e.protection,Math.sign(e.position),{open:price,low:price,high:price});if(!hit)return;
  e.protection.triggered=true;
  for(const o of e.orders)if(!o.system&&(o.status==='pending'||o.status==='partial')){o.status='cancelled';o.message='持倉保護觸發，取消其他委託';}
  e.submit({side:-Math.sign(e.position),qty:Math.abs(e.position),reduceOnly:true,system:true,reason:hit.kind.replace('跳空','觸發')});
  e.events.push({time,message:'持倉保護觸發，下一秒起依真實成交量撮合。'});
}
