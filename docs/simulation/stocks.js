import {visibleDailyBars} from './analytics.js';
import {validateProtection,updateProtectionAfterFill,executeDailyProtection} from './protection.js';
import {settlementDate,lockedDirection,settleReceivables} from './settlement.js';
import {DailyReplayEngine,createDailyRun} from './daily.js';
import {active} from './engine.js';
export const stockRules=market=>market==='TW'?{capital:1000000,currency:'TWD',commissionRate:.001425,minCommission:20,sellTax:.003,slippage:.0005}:{capital:100000,currency:'USD',commissionPerShare:.005,minCommission:1,sellTax:0,slippage:.0005};
const round=n=>Math.round((n+Number.EPSILON)*100)/100;
export function stockFee(market,side,qty,price){const r=stockRules(market);return round(Math.max(r.minCommission,r.commissionRate?qty*price*r.commissionRate:qty*r.commissionPerShare)+(side===-1?qty*price*r.sellTax:0));}
export function stockExecution(market,side,price){
  const p=price*(1+side*.0005),tick=market==='US'?.01:p<10?.01:p<50?.05:p<100?.1:p<500?.5:p<1000?1:5;
  return round((side===1?Math.ceil(p/tick-1e-9):Math.floor(p/tick+1e-9))*tick);
}
export function pickStock(catalog,market,days,random=Math.random,previous=null){
  let pool=catalog.filter(s=>s.market===market&&s.count>=days+121);if(!pool.length)throw Error('這個市場沒有足夠的行情。');
  const other=pool.filter(s=>s.symbol!==previous?.symbol);if(other.length)pool=other;
  return pool[Math.min(pool.length-1,Math.floor(random()*pool.length))];
}
export function createStockRun(pool,days=120,plan=null,random=Math.random,actions=null){
  if(plan&&(plan.symbol!==pool.symbol||plan.market!==pool.market))throw Error('股票與儲存進度不符。');
  const data=createDailyRun(pool,days,plan,random);
  data.marketCalendar=actions?.calendars?.[pool.market]||pool.days.map(b=>b.date);data.actionDates=actions?.symbols?.[pool.symbol]||{};
  data.stock={symbol:pool.symbol,name:pool.name,market:pool.market,currency:pool.currency};
  data.dailyPlan={...data.dailyPlan,symbol:pool.symbol,market:pool.market};
  data.id=`stock:${pool.market}:${pool.symbol}:${data.dailyPlan.start}:${days}`;
  data.contract=pool.symbol;data.sessionLabel=`${pool.market==='TW'?'台股':'美股'}個股 ${days} 日`;data.rules=stockRules(pool.market);
  return data;
}
// Chart adjustment uses only splits already effective at the visible cutoff.
export function stockChartBars(data,index,cutoff=Infinity){
  const all=visibleDailyBars([...data.historyDaily,...data.dailyBars.slice(0,index+1)],cutoff);let factor=1;
  const result=[];
  for(let i=all.length-1;i>=0;i--){const b=all[i];result.push({...b,open:b.open/factor,high:b.high/factor,low:b.low/factor,close:b.close/factor,volume:b.volume*factor});factor*=b.split||1;}
  return result.reverse();
}
export class StockReplayEngine extends DailyReplayEngine{
  get unrealized(){return (this.last-this.average)*this.position;}
  get equity(){return this.cash+this.position*this.last+(this.receivables||[]).filter(r=>!r.paid).reduce((s,r)=>s+r.amount,0);}
  get reserved(){return this.orders.filter(o=>active(o)&&o.side===1).reduce((s,o)=>s+o.remaining*this.last*1.001+stockFee(this.data.stock.market,1,o.remaining,this.last),0);}
  get available(){return this.cash-this.reserved;}
  submit({side,qty,type='market',reduceOnly=false,reason='',system=false,protection=null}){
    if(this.ended)throw Error('本場已結束，請重新練習。');
    if(type!=='market')throw Error('個股日線只提供下一交易日開盤參考價撮合。');
    if(![1,-1].includes(side)||!Number.isInteger(qty)||qty<1||qty>100000)throw Error('請輸入 1–100,000 整數股數。');
    const o={protection:protection?validateProtection(side,this.last,protection.stop,protection.target):null,id:++this.sequence,side,qty,remaining:qty,type,price:null,reduceOnly:side===-1,reason:String(reason).slice(0,200),system,submitted:this.time,readyAt:this.time+1,status:'pending',filled:0,fillValue:0,message:'等待下一交易日開盤參考價'};
    const priorSells=this.orders.filter(p=>active(p)&&p.side===-1).reduce((s,p)=>s+p.remaining,0),cash=this.available;
    this.orders.push(o);
    if(side===-1&&qty>this.position-priorSells){o.status='rejected';o.message='現股只能賣出持有股數，尚未成交賣單也會預留股數';}
    if(side===1&&(reduceOnly||qty*this.last+stockFee(this.data.stock.market,1,qty,this.last)>cash)){o.status='rejected';o.message=reduceOnly?'現股只減倉不能買進':'可用現金不足';}
    return o;
  }
  fill(o,qty,price,time){
    const before=this.position,closing=o.side===-1?qty:0,pnl=closing*(price-this.average),fee=stockFee(this.data.stock.market,o.side,qty,price);
    if(o.side===1)this.average=(this.average*this.position+price*qty)/(this.position+qty);
    this.position+=o.side*qty;
    const date=this.currentBar?.date||new Date(time*1000).toISOString().slice(0,10);
    if(o.side===1)this.cash=round(this.cash-price*qty-fee);
    else this.receivables.push({kind:'sale',amount:round(price*qty-fee),due:settlementDate(this.data.stock.market,date,this.data.marketCalendar),created:date,paid:false});this.realized+=pnl;this.fees=round(this.fees+fee);if(!this.position)this.average=0;
    o.remaining-=qty;o.filled+=qty;o.fillValue+=price*qty;o.status=o.remaining?'partial':'filled';o.message='已按開盤參考價加計滑價成交';
    this.fills.push({positionAfter:this.position,orderId:o.id,time,side:o.side,qty,price,fee,realized:pnl,closing,reason:o.reason,system:o.system,reference:this.last,slippage:(price-this.last)*o.side});
    updateProtectionAfterFill(this,o,before);
  }
  executeOpen(o,price,time){
    if(this.currentBar?.unavailable||this.currentBar?.volume===0){o.status='expired';o.message='當日無可用成交資料，委託不成交';return;}
    if(this.data.stock.market==='TW'&&lockedDirection(this.currentBar||{},this.data.dailyBars[this.index])===o.side){o.status='expired';o.message='日線推估鎖住漲跌停，保守不成交（非官方限價資料）';return;}
    const execution=stockExecution(this.data.stock.market,o.side,price),qty=o.remaining;
    if(o.side===1&&execution*qty+stockFee(this.data.stock.market,1,qty,execution)>this.cash){o.status='rejected';o.message='開盤跳空後現金不足，整筆不成交';return;}
    if(o.side===-1&&qty>this.position){o.status='rejected';o.message='持股不足，整筆不成交';return;}
    this.fill(o,qty,execution,time);
  }
  advance(target){
    if(this.ended)return;
    if(this.index===-1){this.cash=this.data.rules.capital;this.peak=this.cash;this.dividendIncome=0;this.cashInLieu=0;this.receivables=[];this.currentBar=null;}
    while(this.index+1<this.data.dailyBars.length&&this.data.dailyBars[this.index+1].time<=target){
      const b=this.data.dailyBars[this.index+1];
      if(this.index>=0){
        this.time=b.openTime;this.last=b.open;this.currentBar=b;settleReceivables(this,b.date);
        const gap=this.data.marketCalendar.filter(d=>d>this.data.dailyBars[this.index].date&&d<b.date);
        if(gap.length){for(const o of this.orders)if(active(o)){o.status='expired';o.message='中間交易日缺資料，保守取消舊委託';}this.events.push({time:b.openTime,message:gap.length+' 個市場交易日無此股票行情；可能停牌或資料缺漏，未生成成交。'});}
        if(b.split!==1&&b.split){
          for(const o of this.orders)if(active(o)){o.status='cancelled';o.message='拆併股生效，舊委託取消，請重新設定股數';}
          if(this.position){
            const exact=this.position*b.split,shares=Math.floor(exact+1e-8),fraction=Math.max(0,exact-shares);this.average/=b.split;this.position=shares;if(this.protection){if(this.protection.stop)this.protection.stop/=b.split;if(this.protection.target)this.protection.target/=b.split;}
            const cash=round(fraction*b.open);this.cash+=cash;this.cashInLieu+=cash;this.realized+=fraction*(b.open-this.average);if(!shares)this.average=0;
          }
          this.events.push({time:b.openTime,message:`拆併股 ${b.split} 倍生效，股數與成本已調整；未成交委託取消。`});
        }
        if(b.dividend&&this.position){const amount=round(this.position*b.dividend),due=this.data.actionDates[b.date]?.paymentDate||null;this.dividendIncome+=amount;this.receivables.push({kind:'dividend',amount,due,created:b.date,paid:false});this.events.push({time:b.openTime,message:'取得股息應收款 '+this.data.stock.currency+' '+amount.toFixed(2)+(due?'，預定 '+due+' 發放。':'；發放日資料不足，暫不加入可用現金。')});settleReceivables(this,b.date);}
        for(const o of this.orders.filter(active))this.executeOpen(o,b.open,b.openTime);
        executeDailyProtection(this,b);
      }
      this.index++;this.time=b.time;this.last=b.close;this.volume+=b.volume;this.turnover+=b.close*b.volume;this.high=Math.max(this.high,b.high);this.low=Math.min(this.low,b.low);
      this.peak=Math.max(this.peak,this.equity);this.maxDrawdown=Math.max(this.maxDrawdown,(this.peak-this.equity)/this.peak);
      this.history.push({minute:Math.floor(b.time/60),time:b.time,equity:this.equity});
    }
    if(this.index===this.data.dailyBars.length-1)this.finish();
  }
}
