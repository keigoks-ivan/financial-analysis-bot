import {executeDailyProtection} from './protection.js';
import {ReplayEngine,RULES,active} from './engine.js';

export function createDailyRun(pool,days=120,plan=null,random=Math.random,previous=null){
  if(![60,120,240].includes(days))throw Error('日線練習請選擇 60、120 或 240 個交易日。');
  const min=120,max=pool.days.length-days-1;
  if(max<min)throw Error('日線資料不足。');
  if(!plan){
    const choices=Array.from({length:max-min+1},(_,i)=>i+min).filter(i=>i!==previous?.start);
    plan={start:choices[Math.min(choices.length-1,Math.floor(random()*choices.length))],days};
  }
  if(plan.days!==days||!Number.isInteger(plan.start)||plan.start<min||plan.start>max)throw Error('日線進度設定無效。');
  const selected=pool.days.slice(plan.start,plan.start+days+1),first=selected[0];
  return {id:`daily:${plan.start}:${days}`,mode:'daily',dailyPlan:plan,dailyBars:selected,
    historyDaily:pool.days.slice(Math.max(0,plan.start-3000),plan.start),
    ticks:selected.map(b=>[b.time,b.close,b.volume]),start:first.time,playStart:first.time,end:selected.at(-1).time,
    date:first.date,contract:'近月連續',count:selected.slice(1).reduce((s,b)=>s+b.minutes,0),
    reference:first.close,referenceLabel:'練習開始前收盤',sessionLabel:`日線波段 ${days} 日`,
    source:pool.source,sha256:pool.sha256};
}

// Daily decisions use completed bars. No invented intraday price path or tick queue.
export class DailyReplayEngine extends ReplayEngine{
  constructor(data,saved=null){super(data,saved);this.dayClock=0;}
  submit(input){
    if(input.type&&input.type!=='market')throw Error('日線模式只接受下一交易日開盤市價單；限價與停損請使用逐筆模式。');
    const o=super.submit(input);if(active(o))o.message='等待下一交易日開盤';return o;
  }
  snapshot(){return {...super.snapshot(),dailyPlan:this.data.dailyPlan};}
  executeOpen(o,price,time){
    if(o.reduceOnly&&(!this.position||Math.sign(this.position)===o.side)){o.status='cancelled';o.message='已無可減倉部位';return;}
    const qty=Math.min(o.remaining,o.reduceOnly?Math.abs(this.position):o.remaining),execution=price+o.side*2;
    const after=this.position+o.side*qty,fee=(RULES.commission+execution*RULES.multiplier*RULES.taxRate)*qty;
    if(!o.reduceOnly&&Math.abs(after)>Math.abs(this.position)&&this.equity-fee-2*qty*RULES.multiplier<Math.abs(after)*RULES.initialMargin){o.status='rejected';o.message='開盤跳空後保證金不足';return;}
    this.fill(o,qty,execution,time);
  }
  advance(target){
    if(this.ended)return;
    while(this.index+1<this.data.dailyBars.length&&this.data.dailyBars[this.index+1].time<=target){
      const b=this.data.dailyBars[this.index+1];
      if(this.index>=0){
        this.time=b.openTime;this.last=b.open;
        this.checkRisk();
        for(const o of this.orders.filter(active))this.executeOpen(o,b.open,b.openTime);
        executeDailyProtection(this,b);
      }
      this.index++;this.time=b.time;this.last=b.close;
      this.volume+=b.volume;this.turnover+=b.close*b.volume;this.high=Math.max(this.high,b.high);this.low=Math.min(this.low,b.low);
      // Close expiring positions at the last old-contract quote, never carry roll gaps into P&L.
      if(b.rollOut&&this.position){
        for(const o of this.orders)if(active(o)){o.status='cancelled';o.message='到期練習平倉，取消委託';}
        const o=super.submit({side:-Math.sign(this.position),qty:Math.abs(this.position),type:'market',reduceOnly:true,system:true,reason:'到期日前月資料結束，模擬平倉'});
        o.closeReason='expiry';
        this.executeOpen(o,b.close,b.time);
        this.events.push({time:b.time,message:'本月契約資料結束，已按末筆收盤參考價加計 2 點滑價模擬平倉；下個交易日使用次月。'});
      }
      this.checkRisk();
      this.peak=Math.max(this.peak,this.equity);this.maxDrawdown=Math.max(this.maxDrawdown,(this.peak-this.equity)/this.peak);
      this.history.push({minute:Math.floor(b.time/60),time:b.time,equity:this.equity});
    }
    if(this.index===this.data.dailyBars.length-1)this.finish();
  }
  checkRisk(){
    if(!this.position){this.liquidating=false;return;}
    if(this.equity<Math.abs(this.position)*RULES.maintenanceMargin&&!this.liquidating){
      this.liquidating=true;
      for(const o of this.orders)if(active(o)){o.status='cancelled';o.message='低於練習維持保證金';}
      this.events.push({time:this.time,message:'開收盤權益低於練習維持保證金，送出下一可用開盤的模擬風險平倉。'});
      this.submit({side:-Math.sign(this.position),qty:Math.abs(this.position),reduceOnly:true,system:true,reason:'日線模擬風險平倉'});
    }
  }
  nextDay(){if(!this.ended)this.advance(this.data.dailyBars[this.index+1].time);}
  advanceBy(days){this.dayClock+=days;while(this.dayClock>=1&&!this.ended){this.nextDay();this.dayClock--;}}
}
