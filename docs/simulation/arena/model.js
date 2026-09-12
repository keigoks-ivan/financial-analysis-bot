import {createStockRun,StockReplayEngine,stockChartBars,stockPriceFactor,stockBudgetQty,stockExecution,stockRules} from '../stocks.js';
import {movingAverage} from '../indicators.js';
import {hash} from '../research.js';
export const ARENA_KEY='tx-strategy-arena-v1';
export const STRATEGIES=[{id:'hold',name:'持有基準',color:'#a7b0bf'},{id:'trend',name:'均線趨勢',color:'#d8fb70'},{id:'breakout',name:'高點突破',color:'#75baff'},{id:'pullback',name:'趨勢回檔',color:'#d6a4ff'}];
export function validateConfig(input){
 const c={market:input.market,days:Number(input.days),count:Number(input.count),capital:Number(input.capital),allocation:Number(input.allocation),ma:Number(input.ma),lookback:Number(input.lookback),band:Number(input.band),stop:Number(input.stop)};
 if(!['TW','US','ETF'].includes(c.market)||![60,120,240].includes(c.days)||![1,3,5].includes(c.count)||!Number.isFinite(c.capital)||c.capital<1000||c.capital>100000000||!Number.isFinite(c.allocation)||c.allocation<1||c.allocation>100||![20,60,120].includes(c.ma)||![20,60].includes(c.lookback)||!Number.isFinite(c.band)||c.band<.5||c.band>5||!Number.isFinite(c.stop)||c.stop<0||c.stop>30)throw Error('請檢查本金、部位比例與策略參數。');
 return c;
}
export function arenaUniverse(catalog,c){return catalog.filter(s=>(c.market==='ETF'||s.market===c.market&&hash(s.symbol)%4!==0)&&s.liquidity?.starts?.[c.days]>0);}
export function pickArenaPlan(item,days,used=[],random=Math.random){
 const starts=item.liquidity.ranges.flatMap(([a,b])=>Array.from({length:Math.max(0,Math.min(b,item.count-days-1)-Math.max(a,239)+1)},(_,i)=>Math.max(a,239)+i)).filter(start=>!used.some(p=>p.symbol===item.symbol&&Math.abs(p.start-start)<=days+120));
 if(!starts.length)return null;
 return {symbol:item.symbol,market:item.market,start:starts[Math.floor(random()*starts.length)],days,sourceHash:item.sha256};
}
export function strategySignal(bars,c,id){
 const b=bars.at(-1),ma=movingAverage(bars,c.ma),fast=movingAverage(bars,20),i=bars.length-1;
 if(!b||!ma[i-5])return {enter:false,exit:false};
 const trend=b.close>ma[i]&&ma[i]>ma[i-5],prior=bars.slice(-c.lookback-1,-1);
 return {enter:id==='hold'||(id==='trend'?trend:id==='breakout'?trend&&b.close>Math.max(...prior.map(x=>x.high)):trend&&Math.abs(b.close/fast[i]-1)<=c.band/100&&b.close>bars[i-1].close),exit:id!=='hold'&&b.close<ma[i]};
}
export function runStrategy(pool,plan,config,actions,id){
 if(!STRATEGIES.some(s=>s.id===id))throw Error('策略不存在。');
 const c=validateConfig(config),data=createStockRun(pool,c.days,{start:plan.start,days:c.days,symbol:pool.symbol,market:pool.market},()=>0,actions);
 data.rules={...data.rules,capital:c.capital};const e=new StockReplayEngine(data),curve=[{date:data.dailyBars[0].date,equity:e.equity}],decisions=[];let heldDays=0,reducing=false;
 while(!e.ended){
  const bars=stockChartBars(data,e.index),signal=strategySignal(bars,c,id);
  const stopped=id!=='hold'&&c.stop>0&&e.position>0&&e.last<=e.average*(1-c.stop/100);
  if(e.position>0&&(reducing||signal.exit||stopped)){const reason=reducing?'繼續完成減倉':stopped?'收盤跌至持倉成本停損線':'收盤跌破趨勢均線';reducing=true;e.submit({side:-1,qty:Math.min(100000,e.position),reason});decisions.push({date:data.dailyBars[e.index].date,side:-1,reason});}
  else if(!e.position&&signal.enter&&(id!=='hold'||!e.fills.some(f=>f.side===1))){
   const budget=Math.min(e.available,e.equity*c.allocation/100),qty=stockBudgetQty(pool.market,stockExecution(pool.market,1,e.last),budget);
   if(qty)e.submit({side:1,qty,budget,reason:id==='hold'?'首次開盤建立持有基準':STRATEGIES.find(s=>s.id===id).name+'收盤條件成立'});
   else decisions.push({date:data.dailyBars[e.index].date,side:0,reason:'現金或配置金額不足買進一股（含費用）'});
  }
  e.nextDay();if(!e.position)reducing=false;if(e.position)heldDays++;curve.push({date:data.dailyBars[e.index].date,equity:e.equity});
 }
 const end=data.dailyBars.at(-1).time,chart=stockChartBars(data,e.index).slice(-c.days-121),mas=[20,60,120].map(n=>movingAverage(stockChartBars(data,e.index),n));
 const offset=stockChartBars(data,e.index).length-chart.length;
 return {id,return:e.equity/c.capital-1,drawdown:e.maxDrawdown,endingEquity:e.equity,position:e.position,unrealized:e.unrealized,fees:e.fees,dividends:e.dividendIncome,receivables:e.receivables.filter(r=>!r.paid).reduce((s,r)=>s+r.amount,0),exposure:heldDays/c.days,entries:e.fills.filter(f=>f.side===1).length,curve,decisions,orders:structuredClone(e.orders),fills:e.fills.map(f=>({...f,chartPrice:f.price*stockPriceFactor(data,e.index,f.time,end)})),chart:chart.map((b,i)=>({time:b.time,openTime:b.openTime,date:b.date,open:b.open,high:b.high,low:b.low,close:b.close,volume:b.volume,ma:mas.map(m=>m[offset+i])}))};
}
export function runEpisode(pool,plan,config,actions){
 const strategies=STRATEGIES.map(s=>runStrategy(pool,plan,config,actions,s.id)),chart=strategies[0].chart;for(const s of strategies)delete s.chart;
 return {symbol:pool.symbol,name:pool.name,market:pool.market,currency:pool.currency,chart,plan:structuredClone(plan),startDate:pool.days[plan.start].date,endDate:pool.days[plan.start+config.days].date,strategies};
}
export function arenaSummary(episodes){
 if(!episodes.length)throw Error('沒有完成的對戰。');
 return STRATEGIES.map(s=>{const rows=episodes.map(e=>e.strategies.find(r=>r.id===s.id)),sum=k=>rows.reduce((v,r)=>v+r[k],0);return {...s,averageReturn:sum('return')/rows.length,averageDrawdown:sum('drawdown')/rows.length,worstDrawdown:Math.max(...rows.map(r=>r.drawdown)),entries:sum('entries'),exposure:sum('exposure')/rows.length,beatsHold:s.id==='hold'?null:episodes.filter(e=>e.strategies.find(r=>r.id===s.id).return>e.strategies[0].return).length};});
}
export function arenaPacket(battle){
 if(!battle?.episodes?.length||battle.episodes.length!==battle.config.count)throw Error('對戰尚未完整完成。');
 return {format:'strategy-arena-analysis-v1',request:'比較同組行情上已凍結的四套規則、成本、反例與期末持倉。參數重跑屬於探索，不能當成獨立驗證。先固定候選策略，再使用未參與調整的資料做含成本回測。',measurement:'各場使用獨立帳戶；平均報酬不是多標的投資組合報酬。期末按收盤估值，不強制賣出，未扣期末假設清算成本。',summary:arenaSummary(battle.episodes),battle:structuredClone(battle)};
}
export function readBattle(storage){
 const raw=storage.getItem(ARENA_KEY);if(!raw)return null;const b=JSON.parse(raw);validateConfig(b.config);
 if(b.version!==1||!Array.isArray(b.episodes)||b.episodes.length!==b.config.count||b.episodes.some(e=>!e.plan||!Array.isArray(e.chart)||!Array.isArray(e.strategies)||e.strategies.length!==4||e.strategies.some(s=>!Number.isFinite(s.return)||!Array.isArray(s.curve))))throw Error('對戰紀錄格式無效。');return b;
}
export {stockRules,hash as fingerprint};
