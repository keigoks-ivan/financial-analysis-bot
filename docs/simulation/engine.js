import {validateProtection,updateProtectionAfterFill,triggerTickProtection} from './protection.js';
// The tape is real; execution is an explicit deterministic training model.
export const RULES = Object.freeze({capital:1000000, multiplier:200, initialMargin:400000,
  maintenanceMargin:300000, commission:50, taxRate:0.00002, latency:1, participation:0.1});
export const active = o => o.status === 'pending' || o.status === 'partial';
export class ReplayEngine {
  constructor(data, saved=null) {
    this.data=data; this.index=-1; this.time=data.start; this.last=data.ticks[0][1];
    this.cash=RULES.capital; this.position=0; this.average=0; this.realized=0; this.fees=0;
    this.orders=[]; this.fills=[]; this.history=[]; this.events=[]; this.sequence=0;
    this.peak=RULES.capital; this.maxDrawdown=0; this.liquidating=false; this.ended=false;
    this.volume=0; this.turnover=0; this.high=this.last; this.low=this.last; this.flow=0;
    this.closedSegments=0;this.protection=null;this.marginLimitPercent=100;
    this.advance(Math.min(data.playStart??data.start+1800,data.end));
    if(saved) this.restore(saved);
  }
  get unrealized(){return (this.last-this.average)*this.position*RULES.multiplier;}
  get equity(){return this.cash+this.unrealized;}
  get reserved(){return this.orders.filter(o=>active(o)&&!o.reduceOnly).reduce((s,o)=>s+o.remaining*RULES.initialMargin,0);}
  get available(){return this.equity-Math.abs(this.position)*RULES.initialMargin-this.reserved;}
  get marginUsed(){return Math.abs(this.position)*RULES.initialMargin;}
  get marginCapacity(){return Math.max(0,this.equity*this.marginLimitPercent/100-this.marginUsed-this.reserved);}
  setMarginLimit(percent){
    if(!Number.isFinite(percent)||percent<5||percent>100)throw Error('保證金使用上限請設定為 5–100%。');
    this.marginLimitPercent=percent;
  }
  marginFits(o,qty,after,equity){
    if(o.reduceOnly||Math.abs(after)<=Math.abs(this.position))return true;
    const remainingReserve=Math.max(0,this.reserved-qty*RULES.initialMargin);
    return Math.abs(after)*RULES.initialMargin+remainingReserve<=Math.max(0,equity)*this.marginLimitPercent/100;
  }
  get vwap(){return this.volume?this.turnover/this.volume:this.last;}
  submit({side,qty,type='market',price=null,reduceOnly=false,reason='',system=false,protection=null}) {
    if(this.ended) throw Error('本場已結束，請重新練習。');
    if(this.data.segments&&!system&&!this.data.segments.some(s=>this.time>=s.start&&this.time<s.end))throw Error('目前休市，下一個交易時段開盤後才能下單。');
    if(![1,-1].includes(side)||!Number.isInteger(qty)||qty<1||qty>20) throw Error('請輸入 1–20 的整數口數。');
    if(!['market','limit','stop'].includes(type)) throw Error('不支援此委託類型。');
    if(type!=='market'&&(!Number.isInteger(price)||price<=0)) throw Error('價格必須是正整數，最小跳動為 1 點。');
    const o={id:++this.sequence,side,qty,remaining:qty,type,price,reduceOnly:!!reduceOnly,
      protection:protection?validateProtection(side,type==='market'?this.last:price,protection.stop,protection.target):null,reason:String(reason).slice(0,200),system,submitted:this.time,readyAt:this.time+RULES.latency,
      status:'pending',filled:0,fillValue:0,queue:3,triggered:false,message:'等待下一秒起撮合'};
    this.orders.push(o);
    const reject=message=>{o.status='rejected';o.message=message;return o;};
    if(this.liquidating&&!system) return reject('風險處置中，暫停接受新委託。');
    if(reduceOnly && (!this.position||Math.sign(this.position)===side||qty>Math.abs(this.position)))
      return reject('只減倉委託必須與持倉反向，且不能超過持倉口數。');
    const estimate=(RULES.commission+this.last*RULES.multiplier*RULES.taxRate)*qty;
    if(!reduceOnly && this.available < estimate) return reject('可用保證金不足，已拒絕委託。');
    if(!reduceOnly&&this.marginCapacity<estimate){o.status='rejected';o.message='超過設定的保證金使用上限（含待成交委託）';}
    return o;
  }
  cancel(id,message='使用者取消') {const o=this.orders.find(o=>o.id===id);if(o&&active(o)&&!o.system){o.status='cancelled';o.message=message;return true;}return false;}
  flatten() {
    if(!this.position) throw Error('目前沒有可平倉部位。');
    this.orders.forEach(o=>this.cancel(o.id,'平倉前取消其他委託'));
    return this.submit({side:-Math.sign(this.position),qty:Math.abs(this.position),reduceOnly:true,reason:'市價平倉'});
  }
  fill(o,qty,price,t) {
    const before=this.position, direction=Math.sign(before), closing=before&&direction!==o.side?Math.min(qty,Math.abs(before)):0;
    const pnl=closing*(price-this.average)*direction*RULES.multiplier;
    const fee=Math.round((RULES.commission+price*RULES.multiplier*RULES.taxRate)*qty*100)/100;
    const after=before+o.side*qty;
    if(!before||direction===o.side) this.average=(this.average*Math.abs(before)+price*qty)/Math.abs(after);
    else if(!after) this.average=0;
    else if(Math.sign(after)!==direction) this.average=price;
    this.position=after;this.cash+=pnl-fee;this.realized+=pnl;this.fees+=fee;
    o.remaining-=qty;o.filled+=qty;o.fillValue+=price*qty;o.status=o.remaining?'partial':'filled';
    o.message=o.remaining?'部分成交，其餘等待流動性':'已成交';
    this.fills.push({orderId:o.id,time:t,side:o.side,qty,price,fee,realized:pnl,closing,
      positionAfter:this.position,reason:o.reason,system:o.system,...(o.closeReason?{closeReason:o.closeReason}:{}),reference:this.last,slippage:(price-this.last)*o.side});
    updateProtectionAfterFill(this,o,before);
  }
  tick(t,index) {
    const [time,price,volume]=t; this.time=time;this.index=index;this.last=price;
    this.closeSessions(time,false);
    triggerTickProtection(this,time,price);
    this.volume+=volume;this.turnover+=price*volume;this.high=Math.max(this.high,price);this.low=Math.min(this.low,price);
    // Fractional participation carries across prints; whole unused capacity expires per print.
    this.flow=this.flow%1+volume*RULES.participation;
    let capacity=Math.floor(this.flow);
    for(const o of this.orders){
      if(!active(o)||time<o.readyAt) continue;
      if(o.reduceOnly&&(!this.position||Math.sign(this.position)===o.side)) {o.status='cancelled';o.message='已無可減倉部位';continue;}
      if(o.type==='stop'&&!o.triggered){
        if((o.side===1&&price>=o.price)||(o.side===-1&&price<=o.price)){
          o.triggered=true;o.readyAt=time+RULES.latency;o.message='停損已觸發，下一秒起按市價撮合';
        }
        continue;
      }
      if(!capacity)continue;
      const reducing=o.reduceOnly?Math.abs(this.position):o.remaining;
      let qty=Math.min(o.remaining,capacity,reducing);
      const adverse=1+Math.floor(qty/3);
      let execution=price+o.side*adverse;
      if(o.type==='limit') {
        const marketable=o.side===1?execution<=o.price:execution>=o.price;
        const touched=o.side===1?price<=o.price:price>=o.price;
        if(!touched) continue;
        if(!marketable){
          const used=Math.min(o.queue,capacity);o.queue-=used;capacity-=used;
          if(o.queue||!capacity)continue;
          qty=Math.min(qty,capacity);execution=o.price;
        }
        execution=o.side===1?Math.min(execution,o.price):Math.max(execution,o.price);
      }
      const after=this.position+o.side*qty;
      const increases=Math.abs(after)>Math.abs(this.position);
      const fee=(RULES.commission+execution*RULES.multiplier*RULES.taxRate)*qty;
      const impact=(execution-price)*o.side*qty*RULES.multiplier;
      if(!o.reduceOnly&&increases&&this.equity-fee-impact < Math.abs(after)*RULES.initialMargin){
        o.status='rejected';o.message='成交前權益不足，取消剩餘口數';continue;
      }
      if(!this.marginFits(o,qty,after,this.equity-fee-impact)){o.status='rejected';o.message='成交前超過保證金使用上限，取消剩餘委託';continue;}
      this.fill(o,qty,execution,time);capacity-=qty;
    }
    this.peak=Math.max(this.peak,this.equity);
    this.maxDrawdown=Math.max(this.maxDrawdown,(this.peak-this.equity)/this.peak);
    if(this.position&&this.equity<Math.abs(this.position)*RULES.maintenanceMargin&&!this.liquidating){
      this.liquidating=true;
      for(const o of this.orders)if(active(o)){o.status='cancelled';o.message='低於練習維持保證金，取消委託';}
      this.events.push({time,message:'權益低於練習維持保證金，啟動模擬強制平倉。'});
      this.submit({side:-Math.sign(this.position),qty:Math.abs(this.position),reduceOnly:true,system:true,reason:'模擬風險平倉'});
    }
    if(!this.position)this.liquidating=false;
    const minute=Math.floor(time/60);
    if(!this.history.length||this.history.at(-1).minute!==minute)this.history.push({minute,time,equity:this.equity});
    else this.history[this.history.length-1]={minute,time,equity:this.equity};
  }
  advance(target) {
    if(this.ended) return;
    target=Math.min(Math.max(this.time,target),this.data.end);
    while(this.index+1<this.data.ticks.length&&this.data.ticks[this.index+1][0]<=target)
      this.tick(this.data.ticks[this.index+1],this.index+1);
    this.time=target;
    this.closeSessions(target,true);
    if(target>=this.data.end)this.finish();
  }
  closeSessions(time,inclusive){
    const segments=this.data.segments;
    while(segments&&this.closedSegments<segments.length&&(inclusive?segments[this.closedSegments].end<=time:segments[this.closedSegments].end<time)){
      const segment=segments[this.closedSegments++];let expired=0;
      for(const o of this.orders)if(active(o)&&!o.system){o.status='expired';o.message='交易時段收盤，剩餘委託失效';expired++;}
      this.flow=0;
      if(expired)this.events.push({time:segment.end,message:`${segment.label}收盤，${expired} 筆未完成委託失效；持倉保留。`});
    }
  }
  advanceBy(seconds){
    if(!this.data.segments){this.advance(this.time+seconds);return;}
    let left=Math.max(0,seconds);
    while(left>0&&!this.ended){
      const segment=this.data.segments.find(s=>s.end>this.time);
      if(!segment){this.advance(this.data.end);break;}
      if(this.time<segment.start)this.advance(segment.start);
      const amount=Math.min(left,segment.end-this.time);
      this.advance(this.time+amount);left-=amount;
    }
  }
  finish(){this.ended=true;for(const o of this.orders)if(active(o)){o.status='expired';o.message='練習結束，剩餘委託失效';}}
  snapshot(){
    const {data,...state}=this;
    return {version:1,sourceHash:data.sha256,sessionId:data.id,state,...(data.campaign?{campaign:data.campaign}:{})};
  }
  restore(saved){
    if(saved.version!==1||saved.sourceHash!==this.data.sha256||saved.sessionId!==this.data.id)throw Error('儲存版本與資料不一致。');
    const s=saved.state;
    if(s?.marginLimitPercent!==undefined)this.setMarginLimit(s.marginLimitPercent);
    if(!s||!Number.isInteger(s.index)||s.index<0||s.index>=this.data.ticks.length||!Number.isFinite(s.time)||s.time<this.data.start||s.time>this.data.end)throw Error('進度格式無效。');
    for(const k of ['cash','position','average','realized','fees','peak','maxDrawdown','volume','turnover','high','low','flow','sequence','last'])if(!Number.isFinite(s[k]))throw Error('帳戶格式無效。');
    for(const k of ['orders','fills','history','events'])if(!Array.isArray(s[k]))throw Error('紀錄格式無效。');
    for(const k of Object.keys(this))if(k!=='data'&&Object.hasOwn(s,k))this[k]=s[k];
  }
}
