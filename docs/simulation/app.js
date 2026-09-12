import {installResearch} from './research-ui.js';
import {aggregateCalendar,tradeStatistics,sizePosition,visibleDailyBars} from './analytics.js';
import {validateProtection} from './protection.js';
import {ReplayEngine,RULES,active} from './engine.js';
import {candleBucket,movingAverage,aggregateHistory,zoomViewport} from './indicators.js';
import {pickCampaign,assembleCampaign} from './campaigns.js';
import {DailyReplayEngine,createDailyRun} from './daily.js';
import {StockReplayEngine,createStockRun,pickStock,stockRules,stockFee,stockExecution,stockChartBars,stockPriceFactor,stockDrawingPrice} from './stocks.js';
const $=id=>document.getElementById(id), money=(n,d=0)=>Number(n).toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const signed=(n,d=0)=>(n>0?'+':'')+money(n,d), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const time=s=>{s=((Math.floor(s)%86400)+86400)%86400;return [Math.floor(s/3600),Math.floor(s/60)%60,s%60].map(v=>String(v).padStart(2,'0')).join(':');};
const STORE='tx-replay-v1', names={pending:'待成交',partial:'部分成交',filled:'已成交',cancelled:'已取消',rejected:'已拒絕',expired:'已失效'},types={market:'市價',limit:'限價',stop:'停損市價'};
let engine,manifest=[],playing=false,side=1,tab='position',frame=60,visible=70,lastFrame=0,lastPaint=0,lastSaved=0,loadId=0,reviewCursor=null;
let catalog=[],dailyPool=null,stockCatalog=null,stockActions=null;
let drawings=[],drawTool=null,drawStart=null,dragOverlay=null,chartGeometry=null,journalKey=null,lastProtectionForm=null;
const hiddenIdentity=()=>$('fullBlind').checked&&!engine?.ended;
const instrumentLabel=()=>hiddenIdentity()?'盲測標的':engine?.data.stock?engine.data.stock.name+' '+engine.data.stock.symbol:'TX '+(engine?.data.contract||'近月');
function workspaceState(){return {snapshot:engine.snapshot(),blind:$('blind').checked,fullBlind:$('fullBlind').checked,speed:$('speed').value,frame,visible,drawings,journalKey};}
function restoreWorkspace(saved){drawings=Array.isArray(saved?.drawings)?saved.drawings:[];journalKey=saved?.journalKey||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,7);if(saved){if([60,300,900,3600,86400,604800,2592000].includes(saved.frame))frame=saved.frame;$('fullBlind').checked=!!saved.fullBlind;$('blind').checked=saved.blind!==false;if(Number.isInteger(saved.visible))visible=Math.max(12,Math.min(300,saved.visible));}if($('fullBlind').checked)$('blind').checked=true;$('stopPrice').value=engine.protection?.stop??'';$('targetPrice').value=engine.protection?.target??'';drawTool=null;drawStart=null;dragOverlay=null;lastProtectionForm=null;configureInstrument();}
const isStock=()=>!!engine?.data.stock,unit=()=>isStock()?'股':'口',capital=()=>isStock()?engine.data.rules.capital:RULES.capital,multiplier=()=>isStock()?1:200,currencyLabel=()=>engine?.data.stock?.currency==='USD'?'US$':'NT$',price=n=>money(n,isStock()?2:0),modeValue=()=>engine?.data.stock?.market||(isDaily()?'daily':'tick');
const isDaily=()=>engine?.data.mode==='daily';
const isExpiryFill=f=>!isStock()&&!!f.system&&(f.closeReason==='expiry'||f.reason==='到期日前月資料結束，模擬平倉');
const fillAction=f=>isExpiryFill(f)?`到期平倉（${f.side===1?'買回':'賣出'}）`:f.side===1?'買進':'賣出';
const frameLabel=()=>frame===2592000?'月 K':frame===604800?'週 K':frame===86400?'日 K':`${frame/60} 分 K`;
function configureMode(daily,length,saved=null){
  $('replayMode').value=modeValue();
  $('runLength').innerHTML=(daily?[60,120,240]:[3,5,10]).map(n=>`<option value="${n}">${n} 個交易日</option>`).join('');$('runLength').value=String(length);
  $('speed').innerHTML=(daily?[.5,1,2,5]:[1,5,15,60,300]).map(n=>`<option value="${n}">${n}${daily?' 日／秒':'×'}</option>`).join('');
  $('speed').value=String((daily?[.5,1,2,5]:[1,5,15,60,300]).includes(Number(saved?.speed))?saved.speed:daily?1:15);
  $('sessionLabel').hidden=daily;
  if(daily)$('orderType').value='market';$('orderType').disabled=daily;
  text('reduceLabel',daily?'只減倉':'只減倉（保護性停損）');
  configureInstrument();
  text('dataMode',isStock()?`${research.explorationCatalog(stockCatalog).filter(s=>s.market===engine.data.stock.market&&s.liquidity?.starts[length]>0).length} 檔活躍個股 · 日 K`:daily?'真實分鐘行情聚合日 K':'真實逐筆資料');text('stepBtn',daily?'下一交易日 →':'＋10 秒');
  text('tapeTitle',daily?'近期日線收盤':'市場逐筆成交');
  text('ticketNote',isStock()?'以股數買賣、現金全額交易。下一交易日開盤參考價加計 0.05% 滑價撮合；不模擬盤中或零股專屬撮合。':daily?'收盤後決策，下一交易日開盤市價成交（通常從夜盤開始）。每邊估計滑價 2 點；僅於開收盤檢查風險。':'下一秒起撮合，成交價可能不同。時段收盤未成交單失效；連續模式保留持倉。');
  document.querySelectorAll('[data-frame]').forEach(b=>b.disabled=daily&&![86400,604800,2592000].includes(Number(b.dataset.frame)));
  frame=daily?([86400,604800,2592000].includes(saved?.frame)?saved.frame:86400):frame>=86400?60:frame;
  document.querySelectorAll('[data-frame]').forEach(b=>{b.classList.toggle('active',Number(b.dataset.frame)===frame);b.setAttribute('aria-pressed',String(Number(b.dataset.frame)===frame));});
}
async function loadDaily(plan=null,saved=null){
  const request=++loadId;loading=true;setPlaying(false);notify('正在載入日線波段行情…');
  try{
    if(!dailyPool){const r=await fetch('./data/daily.json');if(!r.ok)throw Error('日線資料載入失敗。');dailyPool=await r.json();}
    if(request!==loadId)return;
    const days=plan?.days??([60,120,240].includes(Number($('runLength').value))?Number($('runLength').value):120);
    const data=createDailyRun(dailyPool,days,plan,Math.random,engine?.data.dailyPlan);
    engine=new DailyReplayEngine(data,saved?.snapshot);configureMode(true,days,saved);$('orderPrice').value=engine.last;resetChart();restoreWorkspace(saved);loading=false;setTimeframe(frame);render();save();
    notify(saved?'已恢復同一局日線行情與帳戶。':`已隨機抽取 ${days} 個交易日，含至少 120 根前期日 K；按「下一交易日」逐日練習。`);
  }catch(e){loading=false;notify(e.message,true);renderControls();}
}
function configureInstrument(){
  const stock=engine?.data.stock;
  text('accountCurrency',stock?.currency||'TWD');text('availableLabel',stock?'可用現金':'可用保證金');
  text('instrumentSymbol',hiddenIdentity()?'?':stock?.symbol||'TX');text('instrumentName',hiddenIdentity()?'盲測標的':stock?stock.name+' · '+(stock.market==='TW'?'台股':'美股'):'臺股期貨 · 大台');
  text('watermark',hiddenIdentity()?'BLIND / REPLAY':stock?stock.symbol+' / REPLAY':'TX / REPLAY');text('quantityLabel',stock?'股數（整數股）':'口數');
  text('pointLabel',stock?'每股漲跌 1 元損益':'每點損益 / 口');text('pointValue',currencyLabel()+' '+multiplier());
  text('reserveLabel',stock?'預估買進金額':'預留練習保證金');text('tapeUnit',stock?'成交股數':'口數');
  text('timezoneNote',stock?'● 歷史日線 · 非即時行情 · 股票交易所當地日期':'● 歷史重播 · 非即時行情 · 台北時間');
  text('buySide',stock?'買進 · 現股':'買進 · 做多');text('sellSide',stock?'賣出 · 持股':'賣出 · 做空');
  $('qty').max=stock?'100000':'20';$('qty').setAttribute('aria-label',stock?'委託股數':'委託口數');
  if(!stock&&Number($('qty').value)>20)$('qty').value='1';
}
async function loadStock(market,plan=null,saved=null){
  const request=++loadId;loading=true;setPlaying(false);notify('正在抽取個股與歷史日期…');
  try{
    if(!stockCatalog){const r=await fetch('./data/stocks/catalog.json');if(!r.ok)throw Error('個股清單載入失敗。');stockCatalog=await r.json();}
    const days=plan?.days??([60,120,240].includes(Number($('runLength').value))?Number($('runLength').value):120);
    const selected=plan?stockCatalog.find(s=>s.symbol===plan.symbol&&s.market===market):pickStock(research.explorationCatalog(stockCatalog),market,days,Math.random,engine?.data.stock);
    if(!selected)throw Error('找不到這個股票的儲存進度。');
    const r=await fetch('./data/stocks/'+selected.symbol+'.json');if(!r.ok)throw Error('個股行情載入失敗。');const pool=await r.json();
    if(pool.sha256!==selected.sha256)throw Error('個股資料版本不一致，請重新整理。');if(request!==loadId)return;
    if(!stockActions){const ar=await fetch('./data/stocks/actions.json');if(!ar.ok)throw Error('交割與股息資料載入失敗。');stockActions=await ar.json();}
    if(request!==loadId)return;engine=new StockReplayEngine(createStockRun(pool,days,plan,Math.random,stockActions,selected.liquidity),saved?.snapshot);if(!saved){$('fullBlind').checked=true;$('blind').checked=true;}configureMode(true,days,saved);
    $('qty').value=market==='TW'?'100':'10';$('orderPrice').value=engine.last;resetChart();restoreWorkspace(saved);loading=false;setTimeframe(frame);render();save();
    notify(saved?'已恢復同一檔股票與同一局進度。':'已抽取 '+(hiddenIdentity()?'盲測標的':selected.name+'（'+selected.symbol+'）')+'，共 '+days+' 個交易日；開局前 60 日符合成交活躍度條件。買進扣現金，賣出須有持股。');
  }catch(e){loading=false;notify(e.message,true);renderControls();}
}
function switchMode(mode,preferredFrame=86400){
  if(mode===modeValue())return;$('replayMode').value=modeValue();
  const label=mode==='US'?'US$ 100,000':'NT$ 1,000,000';
  confirmAction('切換練習模式？','將開始新的隨機帳戶並取代目前進度，起始資金 '+label+'。',()=>{if(mode==='TW'||mode==='US')return loadStock(mode);if(mode==='daily')return loadDaily().then(()=>setTimeframe(preferredFrame));configureMode(false,5);return loadCampaign();});
}
let bars=[],barIndex=-1,chartHit=[],confirmCallback=null,loading=false;
let barsFrame=null,barsSource=null,chartOffset=0,chartTotal=0,chartWidth=1;
const pointers=new Map();let gesture=null;
const tint=n=>n>0?'up':n<0?'down':'muted';
const stamp=t=>{if(isDaily()){const all=[...engine.data.historyDaily,...engine.data.dailyBars],i=all.findIndex(b=>t>=b.openTime&&t<=b.time),b=all[i],n=i-engine.data.historyDaily.length;return ($('blind').checked?(n<0?`前 ${-n} 日`:n===0?'觀察日':`第 ${n} 日`):b?.date||new Date(t*1000).toISOString().slice(0,10))+(b&&t===b.openTime?' 開盤':'');}return (engine?.data.campaign?`D${Math.floor(t/86400)-Math.floor(engine.data.start/86400)+1} `:'')+time(t);};
function text(id,value,cls){$(id).textContent=value;if(cls!==undefined)$(id).className=cls;}
function maskMessage(message){return hiddenIdentity()?String(message).replace(/\d{4}-\d{2}-\d{2}/g,'日期隱藏'):message;}
function notify(message,error=false){text('notice',maskMessage(message));$('notice').className='notice'+(error?' error':'');}
function save(){if(!engine)return;try{localStorage.setItem(STORE,JSON.stringify(workspaceState()));text('saveStatus','進度已儲存於此瀏覽器');}catch{text('saveStatus','無法儲存；此瀏覽器儲存空間不可用');}}
function readSaved(){try{return JSON.parse(localStorage.getItem(STORE)||'null');}catch{return null;}}
function setPlaying(value){playing=!!value&&engine&&!engine.ended&&!loading;lastFrame=performance.now();renderControls();}
function resetChart(){bars=[];barIndex=-1;barsFrame=null;barsSource=null;chartOffset=0;reviewCursor=null;}
function setTimeframe(value){
  if(value>=86400&&!isDaily()){switchMode('daily',value);return;}
  if(!(isDaily()?[86400,604800,2592000]:[60,300,900,3600]).includes(value))return;
  frame=value;chartOffset=0;$('chartTooltip').hidden=true;
  document.querySelectorAll('[data-frame]').forEach(b=>{const selected=Number(b.dataset.frame)===frame;b.classList.toggle('active',selected);b.setAttribute('aria-pressed',String(selected));});
  drawChart();save();
}
function zoomChart(factor,anchor=0.5){
  const next=zoomViewport(visible,chartOffset,chartTotal,factor,anchor);
  visible=next.visible;chartOffset=next.offset;$('chartTooltip').hidden=true;drawChart();save();
}
async function loadSession(id,saved=null){
  if(id==='TW'||id==='US')return loadStock(id,saved?.snapshot?.dailyPlan,saved);
  if(id==='daily')return loadDaily(saved?.snapshot?.dailyPlan,saved);
  if(id==='random')return loadCampaign(saved?.snapshot?.campaign,saved);
  const request=++loadId;loading=true;setPlaying(false);document.querySelectorAll('#orderForm button').forEach(b=>b.disabled=true);
  try{
    const response=await fetch(`./data/${id}.json`);if(!response.ok)throw Error('行情資料載入失敗，請稍後重試。');
    const data=await response.json();if(request!==loadId)return;
    if(!Array.isArray(data.ticks)||!data.ticks.length)throw Error('這個場次沒有可用成交資料。');
    try{engine=new ReplayEngine(data,saved?.snapshot);}catch{engine=new ReplayEngine(data);notify('舊進度格式不符，已載入新的練習。',true);}
    configureMode(false,5,saved);$('sessionSelect').value=id;$('orderPrice').value=engine.last;resetChart();restoreWorkspace(saved);loading=false;
    document.querySelectorAll('#orderForm button').forEach(b=>b.disabled=false);
    notify(saved?'已恢復進度，重播維持暫停。':'已載入 30 分鐘觀察資料。下單後開始重播，委託才會撮合。');
    render();save();
  }catch(e){loading=false;notify(e.message,true);renderControls();}
}
async function loadCampaign(plan=null,saved=null){
  const request=++loadId;loading=true;setPlaying(false);renderControls();
  try{
    plan=plan??pickCampaign(catalog,Number($('runLength').value),Math.random,engine?.data.campaign);
    if(![3,5,10].includes(plan.days)||![0,1].includes(plan.segment)||!Number.isInteger(plan.minutes)||plan.minutes<30||plan.minutes>150||!Array.isArray(plan.ids)||plan.ids.length!==plan.days||!plan.ids.every(id=>catalog.some(c=>c.id===id)))throw Error('隨機練習設定無效，請重新抽取。');
    const firstIndex=catalog.findIndex(c=>c.id===plan.ids[0]);
    if(!plan.ids.every((id,i)=>catalog[firstIndex+i]?.id===id&&catalog[firstIndex+i]?.group===catalog[firstIndex].group))throw Error('資料日期或契約不連續，請重新抽取。');
    notify(`正在載入 ${plan.days} 個交易日的真實行情…`);
    const chunks=await Promise.all(plan.ids.map(async id=>{const r=await fetch(`./data/campaigns/${id}.json`);if(!r.ok)throw Error('行情載入失敗，請重新開局。');return r.json();}));
    if(request!==loadId)return;
    const data=assembleCampaign(chunks,plan);
    engine=new ReplayEngine(data,saved?.snapshot);configureMode(false,plan.days,saved);$('sessionSelect').value='random';
    $('orderPrice').value=engine.last;resetChart();restoreWorkspace(saved);loading=false;render();save();
    notify(saved?'已恢復同一局隨機行情與帳戶，重播維持暫停。':`已隨機抽取 ${plan.days} 個交易日。日夜盤接續、休市自動跳過；時段收盤撤銷未成交單。`);
  }catch(e){loading=false;notify(e.message,true);renderControls();}
}
function renderControls(){
  $('replayMode').disabled=loading;$('runLength').disabled=loading;$('resetBtn').disabled=loading;
  if(!engine){for(const id of ['playBtn','stepBtn','submitOrder','closeBtn','finishBtn','quickBuy','quickSell','quickFlatten'])$(id).disabled=true;return;}
  text('playBtn',engine.ended?'本場已結束':playing?'Ⅱ 暫停':'▶ 開始重播');
  text('playState',engine.ended?'練習結束':playing?'重播中':'已暫停');
  $('playBtn').disabled=loading||engine.ended;$('stepBtn').disabled=loading||engine.ended;
  $('submitOrder').disabled=loading||engine.ended||engine.liquidating;
  $('closeBtn').disabled=loading||engine.ended||!engine.position||engine.liquidating;
  $('quickBuy').disabled=$('submitOrder').disabled;
  $('quickSell').disabled=$('submitOrder').disabled||(isStock()&&engine.position<=0);
  $('quickFlatten').disabled=$('closeBtn').disabled;
  $('sessionSelect').disabled=loading;$('runLength').disabled=loading;$('resetBtn').disabled=loading;
  text('finishBtn',engine.ended?'查看復盤 ↗':'結束與復盤 ↗');
}
function renderTicket(){
  const qty=Number($('qty').value)||0;
  text('quickBuy',`買進 ${qty} ${unit()}`);text('quickSell',`賣出 ${isStock()?Math.min(qty,Math.max(0,engine.position)):qty} ${unit()}`);
  const pending=engine.orders.filter(active).length;
  text('quickPosition',`${engine.position?`${engine.position>0?'持有':'空單'} ${Math.abs(engine.position)} ${unit()}`:'目前空手'}${pending?` · ${pending} 筆委託待成交`:''}${engine.protection?' · 持倉停損停利已啟用':''}`);
  text('quickTradeNote',`${isDaily()?'市價委託，下一交易日開盤撮合。':'市價委託，重播後按成交量撮合。'}${isStock()?'賣出最多為目前持股。':'賣出可建立空單。'}進階欄位不套用到這兩個按鈕。`);
  $('buySide').className=side===1?'selected buy':'buy';$('sellSide').className=side===-1?'selected sell':'sell';
  $('submitOrder').className='submit '+(side===1?'buy':'sell');text('submitOrder',`${side===1?'買進':'賣出'} ${qty} ${unit()}`);
  $('priceLabel').hidden=$('orderType').value==='market';$('orderPrice').required=$('orderType').value!=='market';
  const reduce=$('reduceOnly').checked;
  if(isStock()){
    const execution=stockExecution(engine.data.stock.market,side,engine.last);
    text('requiredMargin',side===1?currencyLabel()+' '+money(qty*execution,2):'持有 '+engine.position+' 股');
    text('estimatedCost',currencyLabel()+' '+money(stockFee(engine.data.stock.market,side,qty,execution),2));
    text('bid',price(stockExecution(engine.data.stock.market,-1,engine.last)));text('ask',price(stockExecution(engine.data.stock.market,1,engine.last)));return;
  }
  text('requiredMargin',reduce?'只減倉，不新增':`NT$ ${money(qty*RULES.initialMargin)}`);
  text('estimatedCost',`NT$ ${money((RULES.commission+engine.last*200*RULES.taxRate)*qty,0)}`);
  text('bid',money(engine.last-1));text('ask',money(engine.last+1));
}
function syncBars(){
  if(isStock()){bars=aggregateCalendar(stockChartBars(engine.data,engine.index,reviewCursor??engine.time),frame);return;}
  if(isDaily()){bars=aggregateCalendar(visibleDailyBars([...engine.data.historyDaily,...engine.data.dailyBars.slice(0,engine.index+1)],reviewCursor??engine.time),frame);return;}
  if(barsFrame!==frame||barsSource!==engine.data||barIndex>engine.index){bars=aggregateHistory(engine.data.historyBars||[],frame);barIndex=-1;barsFrame=frame;barsSource=engine.data;}
  while(barIndex<engine.index){
    const t=engine.data.ticks[++barIndex],key=candleBucket(t[0],frame);
    let b=bars.at(-1);if(!b||b.time!==key){b={time:key,open:t[1],high:t[1],low:t[1],close:t[1],volume:0};bars.push(b);}
    b.high=Math.max(b.high,t[1]);b.low=Math.min(b.low,t[1]);b.close=t[1];b.volume+=t[2];
  }
}
function drawChart(){
  if(!engine)return;syncBars();
  const canvas=$('chart'),ctx=canvas.getContext('2d'),rect=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,w=rect.width,h=rect.height;
  if(!w||!h)return;if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);}
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
  const cutoff=reviewCursor??engine.time,history=bars.filter(b=>b.time<=cutoff);
  if(!history.length)return;
  // Review clicks rebuild the final visible bar from prints available at that second.
  if(reviewCursor!==null&&!isDaily()){const b={...history.at(-1)},ticks=engine.data.ticks.slice(0,engine.index+1).filter(t=>candleBucket(t[0],frame)===b.time&&t[0]<=cutoff);if(ticks.length){b.open=ticks[0][1];b.high=Math.max(...ticks.map(t=>t[1]));b.low=Math.min(...ticks.map(t=>t[1]));b.close=ticks.at(-1)[1];b.volume=ticks.reduce((s,t)=>s+t[2],0);history[history.length-1]=b;}}
  chartTotal=history.length;chartOffset=Math.max(0,Math.min(chartOffset,Math.max(0,history.length-visible)));
  const end=history.length-chartOffset,offset=Math.max(0,end-visible),shown=history.slice(offset,end);
  text('chartPeriod',frameLabel());$('chartBasis').hidden=!isStock();
  text('chartRange',`${shown[0].time<engine.data.start?'含前盤 · ':''}${stamp(shown[0].time)} — ${stamp(isDaily()?(shown.at(-1).endTime??shown.at(-1).time):Math.min(cutoff,shown.at(-1).time+frame))} · ${shown.length} 根`);
  $('chart').setAttribute('aria-label',`${hiddenIdentity()?'盲測標的':isStock()?engine.data.stock.name:'台指期'} ${isStock()?'還原權息 ':''}${frameLabel()} 線與成交量，可滾輪縮放或拖曳。`);
  $('chartLatest').hidden=!chartOffset&&reviewCursor===null;
  const averages=[{period:20,color:'#f1c66e'},{period:60,color:'#72b7ff'},{period:120,color:'#bc93ff'}].map(a=>({...a,values:movingAverage(history,a.period)}));
  for(const a of averages){const latest=a.values.at(-1);text(`ma${a.period}`,latest===null?'資料不足':money(latest,1));}
  const maPrices=averages.flatMap(a=>a.values.slice(offset,end).filter(v=>v!==null));
  const protectionPrices=reviewCursor===null&&chartOffset===0&&engine.position?[engine.protection?.stop,engine.protection?.target].filter(p=>p>0):[];
  const high=Math.max(...shown.map(b=>b.high),...maPrices,...protectionPrices),low=Math.min(...shown.map(b=>b.low),...maPrices,...protectionPrices),pad=Math.max(isStock()?.01:8,(high-low)*.13),hi=high+pad,lo=low-pad;
  const left=14,right=w-72,top=24,bottom=h*.72,volTop=h*.79,volBottom=h-27,slots=Math.max(12,shown.length),cw=(right-left)/slots,body=Math.min(30,cw*.64);
  chartWidth=right-left;
  const y=p=>top+(hi-p)/(hi-lo)*(bottom-top),x=i=>left+(i+.5)*cw;
  chartGeometry={left,right,top,bottom,hi,lo,shown,history,offset,cw,y,x};
  ctx.font='12px ui-monospace, monospace';ctx.lineWidth=1;
  for(let i=0;i<=4;i++){const value=hi-(hi-lo)*i/4,yy=y(value);ctx.strokeStyle='#242c37';ctx.beginPath();ctx.moveTo(left,yy);ctx.lineTo(right,yy);ctx.stroke();ctx.fillStyle='#929dab';ctx.fillText(price(value),right+9,yy+4);}
  const maxVol=Math.max(...shown.map(b=>b.volume),1);chartHit=[];
  shown.forEach((b,i)=>{
    const xx=x(i),color=b.close>=b.open?'#ff7d8b':'#51d6af';ctx.strokeStyle=color;ctx.fillStyle=color;
    ctx.beginPath();ctx.moveTo(xx,y(b.high));ctx.lineTo(xx,y(b.low));ctx.stroke();
    ctx.fillRect(xx-body/2,Math.min(y(b.open),y(b.close)),body,Math.max(1.5,Math.abs(y(b.open)-y(b.close))));
    ctx.globalAlpha=.5;ctx.fillRect(xx-body/2,volBottom-(volBottom-volTop)*b.volume/maxVol,body,(volBottom-volTop)*b.volume/maxVol);ctx.globalAlpha=1;
    if(i%Math.max(1,Math.floor(shown.length/5))===0){ctx.fillStyle='#929dab';ctx.fillText(isDaily()?stamp(b.time):engine.data.campaign?stamp(b.time).slice(0,-3):time(b.time).slice(0,5),xx-16,h-9);}
    chartHit.push({x:xx,b});
  });
  ctx.save();ctx.beginPath();ctx.rect(left,top,right-left,bottom-top);ctx.clip();
  for(const a of averages){ctx.strokeStyle=a.color;ctx.lineWidth=1.6;ctx.beginPath();let drawing=false;for(let i=0;i<shown.length;i++){const v=a.values[offset+i];if(v===null){drawing=false;continue;}if(drawing)ctx.lineTo(x(i),y(v));else{ctx.moveTo(x(i),y(v));drawing=true;}}ctx.stroke();}
  ctx.restore();ctx.lineWidth=1;
  const dayStart=shown.findIndex(b=>b.time===engine.data.start);if(dayStart>0){ctx.strokeStyle='#556373';ctx.setLineDash([2,5]);ctx.beginPath();ctx.moveTo(x(dayStart)-cw/2,top);ctx.lineTo(x(dayStart)-cw/2,volBottom);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#a4b2c2';ctx.fillText(engine.data.sessionLabel||'日盤',x(dayStart)+3,top+12);}
  const lastPrice=shown.at(-1).close,yy=y(lastPrice);ctx.strokeStyle='#adbd96';ctx.setLineDash([3,5]);ctx.beginPath();ctx.moveTo(left,yy);ctx.lineTo(right,yy);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#d4f779';ctx.fillRect(right+2,yy-10,68,20);ctx.fillStyle='#18210c';ctx.fillText(price(lastPrice),right+7,yy+4);
  for(const o of engine.orders.filter(o=>active(o)&&o.price&&o.submitted<=cutoff))if(o.price>=lo&&o.price<=hi){ctx.strokeStyle='#d3b66c';ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(left,y(o.price));ctx.lineTo(right,y(o.price));ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#d3b66c';ctx.fillText(`${types[o.type]} #${o.id} · ${o.price}`,left+5,y(o.price)-5);}
  const tradeLabels=new Map();
  for(const f of engine.fills.filter(f=>f.time<=cutoff)){
    const fillPrice=isStock()?f.price*stockPriceFactor(engine.data,engine.index,f.time,cutoff):f.price;
    const i=shown.findIndex(b=>isDaily()?f.time>=b.openTime&&f.time<=(b.endTime??b.time):candleBucket(f.time,frame)===b.time);if(i<0)continue;
    const expiry=isExpiryFill(f);tradeLabels.set(i+':'+f.side+':'+expiry,{i,side:f.side,expiry});
    if(fillPrice<lo||fillPrice>hi)continue;
    const xx=x(i),fy=y(fillPrice),dir=f.side===1?1:-1;ctx.fillStyle=expiry?'#f1c66e':f.side===1?'#ffb3bc':'#8aefce';ctx.beginPath();ctx.moveTo(xx,fy);ctx.lineTo(xx-5,fy+dir*9);ctx.lineTo(xx+5,fy+dir*9);ctx.closePath();ctx.fill();
  }
  if(reviewCursor===null&&engine.position&&engine.average>=lo&&engine.average<=hi){ctx.strokeStyle='#8daef8';ctx.setLineDash([7,4]);ctx.beginPath();ctx.moveTo(left,y(engine.average));ctx.lineTo(right,y(engine.average));ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#a5c0ff';ctx.fillText(`持倉均價 ${money(engine.average,1)}`,left+5,y(engine.average)-6);}
  ctx.save();ctx.font='bold 13px ui-monospace, monospace';ctx.textAlign='center';ctx.textBaseline='middle';
  for(const {i,side,expiry} of tradeLabels.values()){
    const b=shown[i],buy=side===1,width=expiry?64:16,xx=Math.max(left+width/2,Math.min(right-width/2,x(i)));
    const gap=17+(expiry&&tradeLabels.has(i+':'+side+':false')?20:0);
    const labelY=Math.max(top+9,Math.min(bottom-9,buy?y(b.low)+gap:y(b.high)-gap));
    ctx.fillStyle='#101319';ctx.fillRect(xx-width/2,labelY-8,width,16);
    ctx.fillStyle=expiry?'#f1c66e':buy?'#ffb3bc':'#8aefce';ctx.fillText(expiry?'到期平倉':buy?'B':'S',xx,labelY);
  }
  for(const mark of research.markers(journalKey).filter(m=>m.time<=cutoff)){const i=shown.findIndex(b=>isDaily()?mark.time>=b.openTime&&mark.time<=(b.endTime??b.time):candleBucket(mark.time,frame)===b.time);if(i<0)continue;const xx=x(i),yy=Math.max(top+10,Math.min(bottom-10,y(shown[i].high)-37));ctx.fillStyle='#101319';ctx.fillRect(xx-15,yy-9,30,18);ctx.fillStyle='#7bcde1';ctx.fillText(mark.label,xx,yy);}
  ctx.restore();drawOverlays(ctx);
}
function riskEstimate(){
  const percent=Number($('riskPercent').value);if(!Number.isFinite(percent)||percent<=0||percent>10)throw Error('每筆風險請設定為大於 0、最多 10%。');
  const entry=$('orderType').value==='market'?engine.last:Number($('orderPrice').value),stop=Number($('stopPrice').value),qty=Number($('qty').value)||1;
  const fees=isStock()?(stockFee(engine.data.stock.market,1,qty,entry)+stockFee(engine.data.stock.market,-1,qty,stop||entry))/qty+entry*.001:2*(RULES.commission+entry*200*RULES.taxRate)+(isDaily()?4:2)*200;
  return sizePosition({equity:engine.equity,riskPercent:Number($('riskPercent').value)||1,entry,stop,multiplier:multiplier(),available:engine.available,margin:isStock()?0:RULES.initialMargin,feePerUnit:fees,maxQty:isStock()?100000:20});
}
function renderRisk(){
  if(!engine)return;
  const signature=engine.position+':'+JSON.stringify(engine.protection);if(signature!==lastProtectionForm){if(engine.position){$('stopPrice').value=engine.protection?.stop??'';$('targetPrice').value=engine.protection?.target??'';}lastProtectionForm=signature;}
  const stop=Number($('stopPrice').value),target=Number($('targetPrice').value),entry=engine.position?engine.average:engine.last,qty=Math.abs(engine.position)||Number($('qty').value)||0;
  const direction=engine.position?Math.sign(engine.position):side,risk=stop?Math.max(0,(entry-stop)*direction)*multiplier()*qty:0,reward=target?Math.max(0,(target-entry)*direction)*multiplier()*qty:0;
  text('riskSummary',stop?`價差風險 ${currencyLabel()} ${money(risk,2)}${target&&risk?' · 報酬／風險 '+(reward/risk).toFixed(2):''} · 尚未含成本及跳空`:'設定停損，再依帳戶風險比例計算股／口數。');
  $('applyProtection').disabled=loading||!engine.position||engine.ended||engine.protection?.triggered;
  text('applyProtection',engine.protection?.triggered?'保護單已觸發，等待成交':engine.position?'套用至目前全部持倉':'進場委託會附帶停損停利');
  $('sizeBtn').disabled=loading||engine.ended;
}
function renderSettlement(){
  $('settlementInfo').hidden=!isStock();if(!isStock())return;
  const pending=(engine.receivables||[]).filter(r=>!r.paid),sales=pending.filter(r=>r.kind==='sale').reduce((s,r)=>s+r.amount,0),div=pending.filter(r=>r.kind==='dividend').reduce((s,r)=>s+r.amount,0),unknown=pending.filter(r=>!r.due).length;
  text('settlementInfo',`已交割現金 ${currencyLabel()} ${money(engine.cash,2)} · 待交割 ${money(sales,2)} · 應收股息 ${money(div,2)}${unknown?' · '+unknown+' 筆入帳日期資料不足':''}。應收款列入權益，入帳後才能買進。`);
}
function statisticsHTML(){
  const s=tradeStatistics(engine.fills),fmt=n=>n===null?'—':money(n,2);
  return '<h3>完整交易統計</h3><div class="statistics-grid">'+[['完成交易',s.count],['勝率',s.winRate===null?'—':(s.winRate*100).toFixed(1)+'%'],['獲利因子',s.profitFactor===Infinity?'∞（尚無虧損）':fmt(s.profitFactor)],['平均獲利',fmt(s.averageWin)],['平均虧損',fmt(s.averageLoss)],['最大連續虧損',s.maxLossStreak]].map(([label,value])=>`<div><span>${label}</span><strong>${value}</strong></div>`).join('')+'</div><p>由空手至再次空手算一筆，合併加碼與分批出場。股息及不足一股補償另列，不納入交易勝率；未平倉部位不列入。</p>';
}
function chartPoint(e){
  const g=chartGeometry,r=$('chart').getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-(r.top||0);if(!g||x<g.left||x>g.right||y<g.top||y>g.bottom)return null;
  const i=Math.max(0,Math.min(g.shown.length-1,Math.floor((x-g.left)/g.cw)));
  return {time:g.shown[i].time,price:Number((g.hi-(y-g.top)/(g.bottom-g.top)*(g.hi-g.lo)).toFixed(isStock()?2:0)),basis:reviewCursor??engine.time,adjustment:'total-return',x,y};
}
function adjustedPointPrice(p){
  return isStock()?stockDrawingPrice(engine.data,engine.index,p,reviewCursor??engine.time):p.price;
}

function pointX(p){
  const g=chartGeometry,a=g.history;let i=a.findIndex(b=>p.time>=(b.openTime??b.time)&&p.time<=(b.endTime??(isDaily()?b.time:b.time+frame-1)));
  if(i<0)i=p.time<a[0].time?-1:a.length;
  return g.left+(i-g.offset+.5)*g.cw;
}

function drawOverlays(ctx){
  const g=chartGeometry;if(!g)return;ctx.save();ctx.beginPath();ctx.rect(g.left,g.top,g.right-g.left,g.bottom-g.top);ctx.clip();ctx.lineWidth=1.5;ctx.font='12px ui-monospace, monospace';
  for(const d of drawings){
    if(d.points.some(p=>p.time>(reviewCursor??engine.time)))continue;
    ctx.strokeStyle='#7bcde1';ctx.setLineDash([]);ctx.beginPath();
    const a=d.points[0],ay=g.y(adjustedPointPrice(a));
    if(d.type==='horizontal'){ctx.moveTo(g.left,ay);ctx.lineTo(g.right,ay);ctx.fillStyle='#7bcde1';ctx.fillText('水平 '+price(adjustedPointPrice(a)),g.left+5,ay-5);}
    else{const b=d.points[1];ctx.moveTo(pointX(a),ay);ctx.lineTo(pointX(b),g.y(adjustedPointPrice(b)));}ctx.stroke();
  }
  if(drawStart){ctx.fillStyle='#7bcde1';ctx.fillRect(pointX(drawStart)-3,g.y(adjustedPointPrice(drawStart))-3,6,6);}
  if(reviewCursor===null){
    const p=engine.position?engine.protection:{stop:Number($('stopPrice').value),target:Number($('targetPrice').value)};
    for(const [key,label,color] of [['stop','SL 停損','#ff7d8b'],['target','TP 停利','#51d6af']])if(p?.[key]){
      const yy=g.y(p[key]);ctx.strokeStyle=color;ctx.fillStyle=color;ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(g.left,yy);ctx.lineTo(g.right,yy);ctx.stroke();ctx.fillText(`${label} ${price(p[key])}${engine.position?' · 拖曳調整':' · 待進場'}`,g.left+8,Math.max(g.top+13,Math.min(g.bottom-5,yy-6)));
    }
  }
  ctx.restore();
}
function selectDrawTool(tool){drawTool=drawTool===tool?null:tool;drawStart=null;text('drawingHint',drawTool==='trend'?'在圖上點選兩個位置':drawTool==='horizontal'?'在圖上點選水平價位':'拖曳平移 · 滾輪縮放');for(const [id,t] of [['drawHorizontal','horizontal'],['drawTrend','trend']])$(id).setAttribute('aria-pressed',String(drawTool===t));drawChart();}
function handleOverlayDown(e){
  const p=chartPoint(e);if(!p)return false;
  if(drawTool){
    setPlaying(false);
    if(drawings.length>=30){notify('每局最多 30 條畫線，請先刪除部分畫線。');return true;}
    if(drawTool==='horizontal'){drawings.push({type:drawTool,points:[p]});selectDrawTool(null);}
    else if(!drawStart){drawStart=p;text('drawingHint','再點選終點');}else{drawings.push({type:'trend',points:[drawStart,p]});selectDrawTool(null);}
    drawChart();save();return true;
  }
  if(engine.position&&engine.protection&&!engine.protection.triggered&&!engine.ended&&reviewCursor===null){
    const key=['stop','target'].find(k=>engine.protection[k]&&Math.abs(chartGeometry.y(engine.protection[k])-p.y)<12);
    if(key){setPlaying(false);dragOverlay={key,pointerId:e.pointerId,old:{...engine.protection}};$('chart').setPointerCapture(e.pointerId);return true;}
  }return false;
}
function handleOverlayMove(e){
  if(!dragOverlay||dragOverlay.pointerId!==e.pointerId)return false;const p=chartPoint(e);if(!p||p.price<=0)return true;
  try{const next={...engine.protection,[dragOverlay.key]:p.price};engine.protection=validateProtection(Math.sign(engine.position),engine.last,next.stop,next.target);$('stopPrice').value=engine.protection?.stop??'';$('targetPrice').value=engine.protection?.target??'';renderRisk();drawChart();}catch{}return true;
}
const JOURNAL='tx-replay-journal-v1';
function readJournal(){try{const a=JSON.parse(localStorage.getItem(JOURNAL)||'[]');return Array.isArray(a)?a:[];}catch{return [];}}
function storeJournal(entries){try{localStorage.setItem(JOURNAL,JSON.stringify(entries.slice(0,20)));return true;}catch{notify('紀錄空間不足，請先下載並刪除舊局。目前練習仍可繼續。',true);return false;}}
function archiveRun(){
  if(!engine||!journalKey)return;const entries=readJournal(),old=entries.find(e=>e.key===journalKey),workspace=workspaceState();
  const h=workspace.snapshot.state.history||[];workspace.snapshot.state.history=h.filter((v,i)=>i===h.length-1||i%Math.max(1,Math.ceil(h.length/250))===0);
  let chart=old?.chart||null;try{chart=$('chart').toDataURL?.('image/webp',.5)||chart;}catch{}
  const entry={key:journalKey,updated:Date.now(),label:instrumentLabel(),currency:engine.data.stock?.currency||'TWD',net:engine.equity-capital(),ended:engine.ended,stats:tradeStatistics(engine.fills),note:old?.note||'',chart,workspace};
  storeJournal([entry,...entries.filter(e=>e.key!==journalKey)]);
}
function showJournal(){
  setPlaying(false);archiveRun();renderJournal();$('journalDialog').showModal();
}
function renderJournal(){
  const entries=readJournal();$('journalContent').innerHTML='<p>最近 20 局保存在此瀏覽器，可恢復進度、記下檢討並下載紀錄。清除網站資料會刪除紀錄；台幣與美元分開顯示。</p>'+entries.map((e,i)=>`<article class="journal-card"><strong>${esc(e.label)} · ${e.ended?'已結束':'可繼續'}</strong><p>${e.currency} ${signed(e.net,2)} · ${e.stats.count} 筆完整交易 · 勝率 ${e.stats.winRate===null?'—':(e.stats.winRate*100).toFixed(1)+'%'}</p>${e.chart?.startsWith('data:image/')?`<img src="${esc(e.chart)}" alt="本局線圖與買賣位置" loading="lazy">`:''}<label>復盤筆記<textarea id="journal-note-${i}" maxlength="2000" rows="3">${esc(e.note)}</textarea></label><div class="journal-actions"><button data-journal="note" data-index="${i}">儲存筆記</button><button data-journal="restore" data-index="${i}">${e.ended?'開啟復盤':'恢復練習'}</button><button data-journal="export" data-index="${i}">下載紀錄</button><button data-journal="image" data-index="${i}" ${e.chart?'':'disabled'}>下載線圖</button><button data-journal="delete" data-index="${i}">刪除</button></div></article>`).join('');
}
function downloadData(content,name,type='application/json'){
  const a=document.createElement('a'),url=URL.createObjectURL(new Blob([content],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function journalAction(action,index){
  const entries=readJournal(),entry=entries[index];if(!entry)return;
  if(action==='note'){entry.note=$('journal-note-'+index).value.slice(0,2000);if(storeJournal(entries))notify('復盤筆記已儲存。');return;}
  if(action==='export'){if(entry.workspace.fullBlind&&!entry.ended){notify('完整盲測結束後才能匯出。');return;}downloadData(JSON.stringify(entry,null,2),'replay-'+entry.key+'.json');return;}
  if(action==='image'){if(entry.chart){const a=document.createElement('a');a.href=entry.chart;a.download='replay-'+entry.key+'.webp';a.click();}return;}
  if(action==='delete'){confirmAction('刪除這一局紀錄？','僅刪除所選復盤紀錄，無法復原。',()=>{storeJournal(readJournal().filter(e=>e.key!==entry.key));renderJournal();});return;}
  if(action==='restore'){
    $('journalDialog').close();confirmAction('恢復所選練習？','目前這局會先存入紀錄，接著載入所選帳戶與畫線。',async()=>{const s=entry.workspace.snapshot;await loadSession(s.dailyPlan?.market||(s.dailyPlan?'daily':s.campaign?'random':s.sessionId),entry.workspace);if(engine.ended)showReview();});
  }
}

function renderActivity(){
  document.querySelectorAll('[data-tab]').forEach(b=>{b.classList.toggle('active',b.dataset.tab===tab);b.setAttribute('aria-selected',String(b.dataset.tab===tab));});
  const empty=s=>`<div class="empty">${s}<span>所有委託與成交都會留下紀錄。</span></div>`;
  if(tab==='position'){
    $('activityBody').innerHTML=!engine.position?empty('目前沒有持倉'):`<table><thead><tr><th>契約</th><th>方向 / ${unit()}數</th><th>平均成本</th><th>未實現損益</th><th>${isStock()?'持倉市值':'占用練習保證金'}</th></tr></thead><tbody><tr><td>${hiddenIdentity()?'盲測標的':isStock()?esc(engine.data.stock.symbol):'TX '+($('blind').checked?'近月':(isDaily()?engine.data.dailyBars[engine.index].contract:engine.data.contract))}</td><td class="${engine.position>0?'up':'down'}">${engine.position>0?'多':'空'} ${Math.abs(engine.position)} ${unit()}</td><td class="num">${money(engine.average,1)}</td><td class="num ${tint(engine.unrealized)}">${signed(engine.unrealized)}</td><td class="num">${money(Math.abs(engine.position)*(isStock()?engine.last:RULES.initialMargin),isStock()?2:0)}</td></tr></tbody></table>`;
  }else if(tab==='orders'){
    $('activityBody').innerHTML=!engine.orders.length?empty('尚無委託'):`<table><thead><tr><th>時間 / 編號</th><th>方向</th><th>類型 / 價格</th><th>成交 / 委託</th><th>狀態</th><th>說明</th><th></th></tr></thead><tbody>${engine.orders.slice().reverse().map(o=>`<tr><td class="num">${stamp(o.submitted)} #${o.id}</td><td class="${o.side===1?'up':'down'}">${o.side===1?'買':'賣'}${o.reduceOnly?' · 減倉':''}</td><td>${types[o.type]} ${o.price??''}</td><td class="num">${o.filled} / ${o.qty}</td><td>${names[o.status]}</td><td>${esc(o.message)}</td><td>${active(o)&&!o.system?`<button data-cancel="${o.id}">取消</button>`:''}</td></tr>`).join('')}</tbody></table>`;
  }else{
    $('activityBody').innerHTML=!engine.fills.length?empty('尚無成交'):`<table><thead><tr><th>時間</th><th>方向</th><th>口數</th><th>成交價</th><th>手續費＋稅</th><th>平倉毛損益</th><th>委託</th></tr></thead><tbody>${engine.fills.slice().reverse().map(f=>`<tr><td class="num">${stamp(f.time)}</td><td class="${f.side===1?'up':'down'}">${f.side===1?'買':'賣'}</td><td>${f.qty}</td><td class="num">${price(f.price)}</td><td class="num">${money(f.fee,2)}</td><td class="num ${tint(f.realized)}">${f.closing?signed(f.realized):'—'}</td><td>#${f.orderId}${isExpiryFill(f)?' 到期平倉':f.system?' 風險平倉':''}</td></tr>`).join('')}</tbody></table>`;
  }
}
function render(){
  if(!engine)return;configureInstrument();renderRisk();renderSettlement();
  text('equity',money(engine.equity,isStock()?2:0));text('pnl',signed(engine.equity-capital(),isStock()?2:0),tint(engine.equity-capital()));
  text('available',money(engine.available,isStock()?2:0),engine.available<0?'up':'');text('unrealized',signed(engine.unrealized,isStock()?2:0),tint(engine.unrealized));text('drawdown',(engine.maxDrawdown*100).toFixed(2)+'%');
  text('last',price(engine.last));const reference=isStock()?(engine.data.dailyBars[engine.index-1]??engine.data.historyDaily.at(-1)).close/(engine.data.dailyBars[engine.index].split||1):engine.data.reference,delta=engine.last-reference;
  text('change',`${signed(delta,isStock()?2:0)} (${signed(delta/reference*100,2)}%)`,tint(delta));$('change').title=`相對${isStock()?'前一交易日收盤（拆股調整）':engine.data.referenceLabel} ${price(reference)}`;
  text('open',price(isDaily()?engine.data.dailyBars[engine.index].open:engine.data.ticks[0][1]));text('high',price(isStock()?engine.data.dailyBars[engine.index].high:engine.high));text('low',price(isStock()?engine.data.dailyBars[engine.index].low:engine.low));text('volume',money(engine.volume));
  const segment=engine.data.segments?.find(s=>engine.time>=s.start&&engine.time<=s.end);
  const sessionLabel=engine.data.campaign?`${engine.data.sessionLabel} · ${segment?.label||'休市'}`:engine.data.sessionLabel||'日盤';
  const nextDay=engine.data.campaign||isDaily()?'':engine.time>=86400?' · 翌日':'';
  text('clock',stamp(engine.time));text('sessionDate',($('blind').checked?`盲測練習 · ${sessionLabel}`:`${engine.data.date} 起 · ${sessionLabel}`)+nextDay);text('contract',isStock()?'現股':hiddenIdentity()||$('blind').checked?'近月':isDaily()?engine.data.dailyBars[engine.index].contract:engine.data.contract);
  text('positionCount',Math.abs(engine.position));text('orderCount',engine.orders.filter(active).length);
  const playStart=engine.data.playStart??engine.data.start+1800;
  const duration=until=>engine.data.segments?engine.data.segments.reduce((sum,s)=>sum+Math.max(0,Math.min(until,s.end)-Math.max(playStart,s.start)),0):Math.max(0,until-playStart);
  $('progress').style.width=(isDaily()?engine.index/engine.data.dailyPlan.days*100:duration(engine.time)/Math.max(1,duration(engine.data.end))*100)+'%';
  $('tapeRows').innerHTML=engine.data.ticks.slice(Math.max(0,engine.index-5),engine.index+1).map((t,i,a)=>`<div class="tape-row"><span>${isDaily()?stamp(t[0]):time(t[0])}</span><span class="${i?tint(t[1]-a[i-1][1]):''}">${price(t[1])}</span><span>${t[2]}</span></div>`).reverse().join('');
  manifest.forEach((m,i)=>$('sessionSelect').options[i+1].textContent=$('blind').checked?`${m.label} · ${m.sessionLabel||'日盤'}`:`${m.date} · ${m.sessionLabel||'日盤'}`);
  renderControls();renderTicket();renderActivity();drawChart();research.refresh();
}
function confirmAction(title,message,callback){setPlaying(false);text('confirmTitle',title);text('confirmText',message);confirmCallback=callback;$('confirmDialog').showModal();}
function placeOrder(input,useProtection=true){
  if(loading||!engine)throw Error('行情尚未載入。');
  if(useProtection&&!input.reduceOnly&&(!engine.position||Math.sign(engine.position)===input.side||input.qty>Math.abs(engine.position))&&(input.side===1||!isStock())){const stop=Number($('stopPrice').value),target=Number($('targetPrice').value);if(stop||target)input.protection=validateProtection(input.side,input.type==='market'?engine.last:input.price,stop,target);}
  const o=engine.submit(input);tab='orders';reviewCursor=null;render();save();notify(o.status==='rejected'?o.message:`委託 #${o.id} 已送出。${playing?'等待撮合。':'開始重播後才會撮合。'}`,o.status==='rejected');return{id:o.id,status:o.status,message:o.message};
}
function showStockRules(){
  const tw=engine.data.stock.market==='TW';
  $('rulesContent').innerHTML=`<p>使用 Yahoo Finance 歷史日 K、成交量、股息與拆併股資料。台股 ${stockCatalog.filter(s=>s.market==='TW'&&s.liquidity?.starts[120]>0).length} 檔、美股 ${stockCatalog.filter(s=>s.market==='US'&&s.liquidity?.starts[120]>0).length} 檔可抽取 120 日練習，是指定的多產業練習池，並非全市場或歷史成分股；有存續股票偏差，不能用來估算策略普遍績效。部分標的保留供研究室最終驗證，一般新局暫不抽取。每次隨機新局抽取不同股票與日期，可練習 60／120／240 個交易日。</p><h3>成交活躍度篩選</h3><p>開局採當時已完成的最近 60 個交易日：每日成交股數中位數至少 100 萬股；收盤價 × 成交股數的每日金額中位數，台股至少 NT$ 1 億、美股至少 US$ 2,500 萬。金額為日線估算，非交易所精確成交金額。60 筆資料須在 100 個日曆日內，避免抽到長期停牌或缺漏區間。只看開局已知資料，不用後續成交量決定起點；開局後活躍度仍會變動。舊局依原進度恢復。</p><h3>現股帳戶</h3><p>起始資金 ${currencyLabel()} ${money(capital())}，全額現金交易，委託以整數股計算，最多 100,000 股。不能放空、融資或超額賣出，也沒有期貨保證金。買單預留估計金額，開盤跳空導致現金不足時整筆拒絕。賣出價款先列應收交割款，入帳後才可再買進。台股採 T+2；美股依歷史制度採 T+3／T+2／T+1，2024-05-28 起 T+1。交割日使用資料池共同交易日曆估計，不是券商實際可用額度；不提供未交割資金買進。未模擬匯兌與借券。</p><h3>日線成交與費用</h3><p>收盤後決策，以下一個有成交資料的交易日開盤價加計 0.05% 不利滑價作為成交參考，並向不利方向對齊價格跳動。這是日線教學撮合，不是真實開盤市價委託或零股專屬撮合；不還原盤中路徑與開盤排隊。台股 2015 年 6 月起，若全天單一價且接近前收 ±10%，推估為鎖住漲跌停：鎖漲停不買、鎖跌停不賣。此為保守日線判定，並非官方漲跌停參考價；公司行動與特殊無漲跌幅日可能不適用。零量日不成交；共同交易日曆上缺此股票行情時，取消舊委託並提示可能停牌或資料缺漏，不冒充已確認停牌。</p><p>${tw?'台股練習成本：買賣手續費各 0.1425%，每筆最低 NT$ 20；賣出交易稅固定 0.3%，當日沖銷也採此保守練習費率，未套用歷史當沖優惠。實際券商折扣及最低手續費不同。一般整張單位是 1,000 股，本模式允許以股練習但不模擬零股撮合。':'美股練習成本：每股 US$ 0.005、每筆最低 US$ 1，沒有另計 SEC／FINRA、交易所或券商附加費，不代表特定券商報價。'}本場金額均為 ${engine.data.stock.currency}；最大回撤只採每日收盤權益。</p><h3>拆併股與股息</h3><p>價格先還原成當時名目價格，拆併股生效時才調整持股數及平均成本，並取消舊委託。不足一股以當日開盤參考價折算練習現金；這是簡化補償。個股日／週／月 K 與 MA20／60／120 採還原權息：以目前重播日的價格為基準，依已生效的拆併股與現金股息比例回調歷史開高低收，消除機械除權息缺口。只套用已發生事件，回看較早成交時也不使用之後的事件；不代表填息獲利。成交量只調整股數變動，股息不改成交量。</p><p>持有到除息日的股息以資料所列每股金額計入，當天新買進不領當次股息。除息取得應收股息，依 FinMind／Nasdaq 可查得的實際發放日入帳；目前 ${money(Object.values(stockActions.coverage).reduce((s,c)=>s+c.dividends,0))} 筆歷史除息事件中有 ${money(Object.values(stockActions.coverage).reduce((s,c)=>s+c.paymentDates,0))} 筆匹配發放日。查不到日期的款項保留在權益，但不加入可用現金。未扣股息稅或補充保費。B／S 位置與畫線同步換算為還原價；委託、持倉成本、停損停利與帳戶仍使用當時實際價格，股息只按應收與發放規則計一次。資料未涵蓋的現金增資、減資與其他複雜公司行動不自行補造。</p><p>資料可能有缺漏，無資料的日期不生成 K 線。完整盲測可同時隱藏股票名稱與日期，結束後揭露；資料仍下載至瀏覽器，不是防作弊競賽。進度及最近 20 局復盤保存在此瀏覽器。<a href="https://help.yahoo.com/kb/SLN28256.html" target="_blank" rel="noreferrer">Yahoo 還原價說明</a> · <a href="https://www.twse.com.tw/zh/about/company/guide.html" target="_blank" rel="noreferrer">證交所投資指南</a> · <a href="https://www.twse.com.tw/en/products/system/trading.html" target="_blank" rel="noreferrer">台股交易制度</a></p>`;
  $('rulesContent').insertAdjacentHTML('beforeend',practiceRules());$('rulesDialog').showModal();
}
function practiceRules(){return '<h3>圖上保護、畫線與復盤</h3><p>進場委託可附 SL／TP，成交後套用至全部持倉；可拖曳或輸入價位後按「套用」。清空兩價再套用會移除保護。逐筆模式觸發後至少延遲一秒、共用成交量容量；持倉保護跨時段保留。日線同根同時觸及先停損，跳空依開盤，屬保守區間估算。止損不能保證限制最大損失。</p><p>風險比例按目前帳戶權益估計數量，考慮費用緩衝與可用資金，實際跳空與滑價仍可能超出。水平線與趨勢線依時間及價格保存，切週期仍保留；拆股後按當時可見基準調整畫線。復盤按完整開倉至空手計算勝率、獲利因子及連續虧損，加碼與分批出場合併；股息另列。最近 20 局及筆記、線圖保存在此瀏覽器，可下載備份。</p>';}
function showRules(){
  setPlaying(false);
  if(isStock()){showStockRules();return;}
  if(isDaily()){
    $('rulesContent').innerHTML=`<p>日線波段使用本機封存的 TXFR1 近月 1 分鐘 OHLC，依資料交易日合併夜盤與日盤。排除補值、零量分鐘與到期日換月後尾段，沒有生成盤中路徑。可抽取 60／120／240 個交易日，另提供至少 120 根、最多 3,000 根可用歷史日 K 暖機。</p><h3>日 K 與交易時間</h3><p>每次「下一交易日」才揭露該日完整 K 線。可切換日／週／月 K；MA20／60／120 隨週期計算，週／月線僅合併目前已揭露的交易日，當期未完成會隨重播更新。歷史不足時不補造均線。夜盤歸入下一交易日；週五夜盤通常歸入週一。</p><h3>開盤成交模型</h3><p>僅接受市價單：收盤後送出，於下一交易日第一筆分鐘開盤參考價，加上每邊 2 點不利滑價成交；下一交易日通常從夜盤開始。沒有逐筆隊列或部分成交模型，限價請使用逐筆實戰模式；持倉 SL／TP 使用每日高低區間判定，同根同時觸及時先算停損，跳空採開盤參考價再加不利滑價。最多 20 口仍受保證金約束。</p><h3>資金與跨月</h3><p>初始資金 NT$ 1,000,000，大台每點 NT$ 200，練習原始／維持保證金每口 NT$ 400,000／300,000；每邊手續費 NT$ 50，交易稅按名目金額 × 0.00002 估算。以上為教學參數，非歷史公告費率。</p><p>僅於開盤與收盤檢查權益；收盤觸發風險處置時，在下一個可用開盤執行。日內追加保證金、漲跌停無法成交及盤中回撤未還原。最大回撤以每日收盤權益計算。持倉可跨日，未模擬逐日結算入帳。</p><p>到期日以舊契約最後分鐘收盤價加 2 點不利滑價模擬平倉並計費，下個交易日使用次月，需自行重新進場；不把換月接縫計入持倉損益。圖表與均線仍使用未調整的近月連續價，換月價差會影響均線。這不是交易所到期結算模型。</p><p>資料期間：${dailyPool.days[0].date} 至 ${dailyPool.days.at(-1).date}，${dailyPool.days.length} 個交易日。日期隱藏只供個人練習，資料會下載至瀏覽器。復盤可下載交易紀錄與本局抽樣設定。</p>`;
    $('rulesContent').insertAdjacentHTML('beforeend',practiceRules());$('rulesDialog').showModal();return;
  }
  $('rulesContent').innerHTML=`<p>價格與成交量來自你的本機期交所逐筆成交封存。圖表從已經重播的成交形成；沒有生成行情或虛構新聞。</p><h3>真實資料涵蓋到哪裡？</h3><p>本場 ${money(engine.data.count)} 筆 TX 單一近月契約成交。${$('blind').checked?'日期目前隱藏，結束後揭露。':esc(engine.data.date)+'，契約 '+engine.data.contract+'。'}時間精度為秒，同秒沿用來源順序；原始雙邊量除以 2 轉成單邊口數。固定場次於開盤後 30 分鐘開始；隨機連續模式抽取開盤後 30–150 分鐘的起點，起點之前的行情供觀察。日盤 08:45–13:45；夜盤 15:00–翌日 05:00，重播時間連續跨午夜。參考漲跌使用${engine.data.referenceLabel}，並非昨結算。</p><p>這是個人練習的盲測。資料在瀏覽器載入，並非防作弊競賽；刻意查看資料檔仍可取得完整走勢。</p><h3>K 線與均線</h3><p>1、5、15、60 分 K 以各時段開盤時間對齊。MA20、MA60、MA120 使用所選週期的收盤價簡單平均，包含形成中 K 線；使用同契約之前的真實行情暖機，根數不足時顯示「資料不足」。圖中的「前盤」可能是夜盤或更早交易時段，不影響本場帳戶及累計成交量。</p><h3>模擬成交</h3><ul><li>真實成交價不是買賣報價。畫面估計買／賣價＝最新成交價 ±1 點，沒有真實五檔或排隊資料。</li><li>送出後至少等 1 個模擬秒。所有訂單共享每筆真實成交量的 10% 估計可成交容量；可部分成交，同時委託按送出順序處理。</li><li>市價成交以當筆價格加減不利滑價，1 點起，每次成交每滿 3 口再加 1 點。未用完整容量不累積到下一筆。</li><li>限價需符合價格條件；僅觸價時，先扣除 3 口估計前方排隊量，不能保證成交。實際交易所的撮合與優先順序無法由此資料還原。</li><li>停損觸發後再等 1 秒按市價成交，跳空可能越過停損價。保護既有部位時，勾選「只減倉」。</li></ul><h3>練習帳戶與風險</h3><p>初始資金 NT$ 1,000,000；大台每點 NT$ 200。<strong>練習原始／維持保證金固定為每口 NT$ 400,000／300,000，並非該歷史日期的期交所公告金額。跨盤權益連續按市價計算；未模擬逐日結算入帳，平均成本不會於收盤重設。</strong>每口每邊手續費假設 NT$ 50，交易稅以成交名目金額 × 0.00002 估算。所有成本都會扣款。</p><p>一般新單保守預留每口原始保證金，只減倉單不另預留。低於練習維持保證金時取消其他委託，送出模擬強制平倉，仍受下一秒與流動性約束。此為教學風險規則，不代表期貨商的實際處置流程。</p><p>隨機連續模式可練習 3、5、10 個交易日，同一契約的日夜盤持倉接續保留，休市自動跳過，不混接不同日期的行情。每個時段收盤，一般未完成委託（含停損委託）失效，需在新時段重新設定。固定單場模式仍在該場結束。提前結束或收盤時，未成交單失效，剩餘持倉按最後可見成交價計算未實現損益，不虛構平倉成交。</p><p><a href="https://www.taifex.com.tw/cht/2/tX" target="_blank" rel="noreferrer">期交所臺股期貨契約規格 ↗</a> · <a href="https://www.taifex.com.tw/cht/3/dlFutPrevious30DaysSalesData" target="_blank" rel="noreferrer">期交所逐筆成交資料 ↗</a></p>`;
  $('rulesContent').insertAdjacentHTML('beforeend',practiceRules());$('rulesDialog').showModal();
}
function equitySVG(){
  const a=engine.history,w=690,h=140,vals=[capital(),...a.map(x=>x.equity)],hi=Math.max(...vals),lo=Math.min(...vals),range=Math.max(hi-lo,1000);
  const pts=a.map((v,i)=>`${12+i/(Math.max(1,a.length-1))*(w-24)},${15+(hi-v.equity)/range*(h-30)}`).join(' ');
  return `<svg class="review-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="本場帳戶權益曲線"><polyline points="${pts}" fill="none" stroke="#d4f779" stroke-width="2"/></svg>`;
}
function showReview(){
  setPlaying(false);archiveRun();
  const net=engine.equity-capital(),closed=engine.fills.filter(f=>f.closing),slip=engine.fills.reduce((s,f)=>s+Math.max(0,f.slippage)*f.qty*multiplier(),0);
  $('reviewContent').innerHTML=`<p>${hiddenIdentity()?'日期隱藏':engine.data.date} · ${esc(instrumentLabel())} · ${engine.data.sessionLabel||"日盤"} · ${stamp(engine.data.playStart??engine.data.start+1800)} — ${stamp(engine.time)}<br>結束時持倉：${engine.position?`${engine.position>0?'多':'空'} ${Math.abs(engine.position)} ${unit()}，以下權益包含未實現損益。`:'已空手。'}</p><div class="review-grid"><div><span>本場淨損益</span><strong class="${tint(net)}">${signed(net)}</strong></div><div><span>最大回撤</span><strong>${(engine.maxDrawdown*100).toFixed(2)}%</strong></div><div><span>手續費＋交易稅</span><strong>${money(engine.fees)}</strong></div><div><span>平倉毛損益</span><strong>${signed(engine.realized)}</strong></div><div><span>未實現損益</span><strong>${signed(engine.unrealized)}</strong></div><div><span>成交筆數 / ${unit()}數</span><strong>${engine.fills.length} / ${engine.fills.reduce((s,f)=>s+f.qty,0)}</strong></div></div>${statisticsHTML()}${equitySVG()}<p>相對成交參考價的不利滑價估算：${currencyLabel()} ${money(slip,2)}，已包含於成交價，未重複扣款。空手基準損益為 ${currencyLabel()} 0。${isStock()?'股息收入：'+currencyLabel()+' '+money(engine.dividendIncome,2)+'。':''}${closed.length?'統計按完整開倉至平倉合併，包含手續費；未結束部位不列入勝率。':'尚無完整平倉交易。'}</p>${engine.events.map(e=>`<p class="up">${stamp(e.time)} ${esc(maskMessage(e.message))}</p>`).join('')}<h3>逐筆回看</h3><p>點選成交時間，主圖會退回到當時可見的 K 線；帳戶總覽仍顯示本場結束值。</p>${engine.fills.length?engine.fills.map(f=>`<div class="review-trade"><button data-review-time="${f.time}">${stamp(f.time)} ↗</button> <span class="${f.side===1?'up':'down'}">${fillAction(f)} ${f.qty} ${unit()}</span> @ ${price(f.price)}<p>${esc(f.reason||'未記錄進場理由。')}</p><small>委託 #${f.orderId} · 成本 ${money(f.fee,2)} · ${f.closing?'平倉毛損益 '+signed(f.realized):'開倉 / 加碼'}</small></div>`).join(''):'<p>本場沒有成交。觀察市場、選擇不交易，也是一種決策。</p>'}<div class="dialog-actions"><button id="exportBtn">下載本場紀錄</button><button data-close="reviewDialog" class="primary">返回交易室</button></div>`;
  $('reviewDialog').showModal();
}
function exportSession(){
  if(hiddenIdentity()){notify('完整盲測進行中，結束後才可匯出揭露資料。');return;}
  const result={date:engine.data.date,contract:engine.data.contract,rules:isStock()?engine.data.rules:RULES,statistics:tradeStatistics(engine.fills),drawings,stock:engine.data.stock??null,dividendIncome:engine.dividendIncome??0,executionModel:isStock()?{timing:'next-day-open-reference',slippageRate:.0005,cashOnly:true}:isDaily()?{timing:'next-trading-day-open',slippagePoints:2,riskChecks:'open-and-close',roll:'expiry-close'}:{timing:'next-second'},source:engine.data.source,sha256:engine.data.sha256,campaign:engine.data.campaign??null,dailyPlan:engine.data.dailyPlan??null,asOf:stamp(engine.time),equity:engine.equity,unrealized:engine.unrealized,orders:engine.orders,fills:engine.fills,history:engine.history};
  const url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`${engine.data.stock?.symbol||'TX'}-${engine.data.date}-review.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
// Both UI and agent tools call the same validated actions.
function registerTools(){
  const context=document.modelContext;if(!context?.registerTool)return;const lifecycle=new AbortController();
  const tools=[{name:'read_replay_account',description:'Read the current simulated account and visible market state. Does not expose future prices.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:()=>({market:modeValue(),symbol:hiddenIdentity()?'hidden':engine.data.stock?.symbol||'TX',currency:engine.data.stock?.currency||'TWD',unit:unit(),time:stamp(engine.time),price:engine.last,equity:engine.equity,position:engine.position,available:engine.available,ended:engine.ended})},
    {name:'submit_simulated_order',description:'Submit a virtual order using the active market rules and the visible order form. Never places a real trade.',inputSchema:{type:'object',properties:{side:{type:'integer',enum:[1,-1]},qty:{type:'integer',minimum:1,maximum:100000},type:{type:'string',enum:['market','limit','stop']},price:{type:'integer',minimum:1},reduceOnly:{type:'boolean'}},required:['side','qty','type'],additionalProperties:false},annotations:{readOnlyHint:false},execute:input=>placeOrder(input)}];
  for(const tool of tools)try{Promise.resolve(context.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}
  window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}
$('submitOrder').insertAdjacentHTML('beforebegin','<label class="blind reduce-label"><input id="reduceOnly" type="checkbox"> <span id="reduceLabel">只減倉（保護性停損）</span></label>');
$('playBtn').onclick=()=>{reviewCursor=null;setPlaying(!playing);};
$('stepBtn').onclick=()=>{setPlaying(false);reviewCursor=null;const n=engine.fills.length,v=engine.events.length;if(isDaily())engine.nextDay();else engine.advanceBy(10);if(engine.fills.length>n){const f=engine.fills.at(-1);notify(`${stamp(f.time)} ${fillAction(f)} ${f.qty} ${unit()} @ ${price(f.price)}，成本 ${currencyLabel()} ${money(f.fee,2)}。`);}if(engine.events.length>v)notify(engine.events.at(-1).message,true);render();save();if(engine.ended)showReview();};
$('buySide').onclick=()=>{side=1;renderTicket();};$('sellSide').onclick=()=>{side=-1;renderTicket();};
for(const id of ['qty','orderType','reduceOnly'])$(id).addEventListener('input',()=>engine&&renderTicket());
$('qtyMinus').onclick=()=>{$('qty').value=Math.max(1,(Number($('qty').value)||1)-1);renderTicket();};
$('qtyPlus').onclick=()=>{$('qty').value=Math.min(isStock()?100000:20,(Number($('qty').value)||0)+1);renderTicket();};
$('orderForm').onsubmit=e=>{e.preventDefault();try{placeOrder({side,qty:Number($('qty').value),type:$('orderType').value,price:Number($('orderPrice').value),reduceOnly:$('reduceOnly').checked,reason:$('reason').value});}catch(error){notify(error.message,true);}};
$('closeBtn').onclick=()=>{try{const o=engine.flatten();tab='orders';notify(`平倉委託 #${o.id} 已送出，開始重播後按市場流動性成交。`);render();save();}catch(e){notify(e.message,true);}};
for(const [id,direction] of [['quickBuy',1],['quickSell',-1]])$(id).onclick=()=>{
  try{const qty=Number($('qty').value);if(!Number.isInteger(qty)||qty<1||qty>(isStock()?100000:20))throw Error('請輸入有效的整數數量。');
    placeOrder({side:direction,qty:isStock()&&direction===-1?Math.min(qty,engine.position):qty,type:'market',reduceOnly:isStock()&&direction===-1,reason:''},false);
  }catch(e){notify(e.message,true);}
};
$('quickFlatten').onclick=()=>$('closeBtn').onclick();
$('rulesBtn').onclick=showRules;
$('journalBtn').onclick=showJournal;
$('drawHorizontal').onclick=()=>selectDrawTool('horizontal');$('drawTrend').onclick=()=>selectDrawTool('trend');
$('undoDrawing').onclick=()=>{drawings.pop();drawStart=null;drawChart();save();};$('clearDrawings').onclick=()=>{drawings=[];drawStart=null;drawChart();save();};
for(const id of ['stopPrice','targetPrice','riskPercent','orderPrice','qty'])$(id).addEventListener('input',()=>{renderRisk();drawChart();});
$('sizeBtn').onclick=()=>{try{validateProtection(side,engine.last,Number($('stopPrice').value),null);if(!Number($('stopPrice').value))throw Error('請先輸入停損價。');const r=riskEstimate();$('qty').value=r.qty;renderTicket();renderRisk();notify('預估 '+r.qty+' '+unit()+'，含成本緩衝的風險 '+currencyLabel()+' '+money(r.risk,2)+'；跳空或流動性不足仍可能超過預算。');}catch(e){notify(e.message,true);}};
$('applyProtection').onclick=()=>{try{engine.protection=validateProtection(Math.sign(engine.position),engine.last,Number($('stopPrice').value),Number($('targetPrice').value));render();save();notify(engine.protection?'已更新全部持倉的停損停利，可拖曳圖上 SL／TP 線。':'持倉保護已移除。');}catch(e){notify(e.message,true);}};
$('blind').onchange=()=>{if($('fullBlind').checked)$('blind').checked=true;render();save();};
$('fullBlind').onchange=()=>{if($('fullBlind').checked)$('blind').checked=true;notify($('fullBlind').checked?'已隱藏標的與日期，結束後揭露。':'已顯示標的名稱。');render();save();};$('speed').onchange=save;
$('replayMode').onchange=()=>switchMode($('replayMode').value);
$('resetBtn').onclick=()=>confirmAction('隨機開啟新的一局？',`將重新抽取 ${$('runLength').value} 個交易日${isDaily()?'的日線行情':'與盤中起點'}。現在這局會存入復盤紀錄，資金回到 ${currencyLabel()} ${money(capital())}。`,()=>isStock()?loadStock(engine.data.stock.market):isDaily()?loadDaily():loadCampaign());
$('sessionSelect').onchange=()=>{const id=$('sessionSelect').value;$('sessionSelect').value=engine.data.campaign?'random':engine.data.id;confirmAction('切換交易場次？','切換後會開始新帳戶，並取代此瀏覽器目前儲存的進度。',()=>loadSession(id));};
$('runLength').onchange=()=>notify(`新局長度設為 ${$('runLength').value} 個交易日；按「隨機新局」開始。目前進度繼續保留。`);
$('finishBtn').onclick=()=>engine.ended?showReview():confirmAction('結束本場並復盤？','未成交委託將失效。持倉按當下價格計算未實現損益，不會虛構平倉成交。',()=>{engine.finish();render();save();showReview();});
$('confirmAction').onclick=()=>{$('confirmDialog').close();const cb=confirmCallback;confirmCallback=null;archiveRun();return cb?.();};
$('zoomIn').onclick=()=>zoomChart(.8,1);$('zoomOut').onclick=()=>zoomChart(1.25,1);
$('chartLatest').onclick=()=>{chartOffset=0;reviewCursor=null;drawChart();};
$('chart').addEventListener('pointerdown',e=>{
  if(e.button!==0&&e.pointerType==='mouse')return;
  if(handleOverlayDown(e))return;
  $('chart').setPointerCapture(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
  const pts=[...pointers.values()];
  gesture=pts.length===2?{kind:'pinch',distance:Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y),visible,offset:chartOffset}:{kind:'pan',x:e.clientX,offset:chartOffset};
  $('chartTooltip').hidden=true;
});
$('chart').addEventListener('pointermove',e=>{
  if(handleOverlayMove(e))return;
  if(pointers.has(e.pointerId)&&gesture){
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const pts=[...pointers.values()];
    if(gesture.kind==='pinch'&&pts.length>=2){const distance=Math.max(1,Math.hypot(pts[0].x-pts[1].x,pts[0].y-pts[1].y));const next=zoomViewport(gesture.visible,gesture.offset,chartTotal,gesture.distance/distance);visible=next.visible;chartOffset=next.offset;}
    else if(gesture.kind==='pan'){chartOffset=Math.max(0,Math.min(Math.max(0,chartTotal-visible),Math.round(gesture.offset+(e.clientX-gesture.x)*Math.min(visible,chartTotal)/chartWidth)));}
    drawChart();return;
  }
  if(!chartHit.length)return;const x=e.clientX-$('chart').getBoundingClientRect().left;const hit=chartHit.reduce((a,b)=>Math.abs(a.x-x)<Math.abs(b.x-x)?a:b).b;
  text('chartTooltip',`${isStock()?'還原權息 · ':''}${hit.time<engine.data.start?'前盤 ':''}${isDaily()?stamp(hit.time):time(hit.time)}　開 ${price(hit.open)}　高 ${price(hit.high)}　低 ${price(hit.low)}　收 ${price(hit.close)}　量 ${money(hit.volume)}`);$('chartTooltip').hidden=false;
});$('chart').addEventListener('pointerleave',()=>$('chartTooltip').hidden=true);
for(const event of ['pointerup','pointercancel','lostpointercapture'])$('chart').addEventListener(event,e=>{
  if(dragOverlay){if(event==='pointercancel'){engine.protection=dragOverlay.old;$('stopPrice').value=engine.protection?.stop??'';$('targetPrice').value=engine.protection?.target??'';}dragOverlay=null;renderRisk();drawChart();save();return;}
  pointers.delete(e.pointerId);const remaining=[...pointers.values()][0];gesture=remaining?{kind:'pan',x:remaining.x,offset:chartOffset}:null;save();
});
$('chart').addEventListener('wheel',e=>{e.preventDefault();const x=e.clientX-$('chart').getBoundingClientRect().left;zoomChart(Math.exp(Math.max(-.4,Math.min(.4,e.deltaY*.003))),(x-14)/chartWidth);},{passive:false});
$('chart').addEventListener('dblclick',()=>{visible=70;chartOffset=0;reviewCursor=null;drawChart();save();});
new ResizeObserver(drawChart).observe($('chart'));
$('chartInfo').onclick=()=>{if(reviewCursor!==null){reviewCursor=null;text('chartInfo','K 線與成交量 · 僅顯示已重播資料');drawChart();}};
 document.addEventListener('click',e=>{
  const j=e.target.closest('[data-journal]');if(j)journalAction(j.dataset.journal,Number(j.dataset.index));
  const close=e.target.closest('[data-close]');if(close)$(close.dataset.close).close();
  const t=e.target.closest('[data-tab]');if(t){tab=t.dataset.tab;renderActivity();}
  const cancel=e.target.closest('[data-cancel]');if(cancel){engine.cancel(Number(cancel.dataset.cancel));render();save();notify('委託已取消，預留保證金已釋放。');}
  const f=e.target.closest('[data-frame]');if(f)setTimeframe(Number(f.dataset.frame));
  const r=e.target.closest('[data-review-time]');if(r){reviewCursor=Number(r.dataset.reviewTime);$('reviewDialog').close();text('chartInfo',`成交回看 ${stamp(reviewCursor)} · 點此返回`);drawChart();$('chart').scrollIntoView({behavior:'smooth',block:'center'});}
  if(e.target.closest('#exportBtn'))exportSession();
 });
window.addEventListener('keydown',e=>{if(e.code==='Space'&&!['INPUT','TEXTAREA','SELECT','BUTTON'].includes(e.target.tagName)&&!document.querySelector('dialog[open]')){e.preventDefault();setPlaying(!playing);}});
window.addEventListener('pagehide',save);document.addEventListener('visibilitychange',()=>{if(document.hidden){setPlaying(false);save();}});
function loop(now){
  const elapsed=lastFrame?Math.min((now-lastFrame)/1000,.5):0;lastFrame=now;
  if(playing&&engine&&!loading){const n=engine.fills.length,events=engine.events.length;engine.advanceBy(elapsed*Number($('speed').value));
    if(engine.fills.length>n){const f=engine.fills.at(-1);notify(`${stamp(f.time)} ${fillAction(f)} ${f.qty} ${unit()} @ ${price(f.price)}，成本 ${currencyLabel()} ${money(f.fee,2)}。`);}
    if(engine.events.length>events)notify(engine.events.at(-1).message,true);
    if(now-lastPaint>180){render();lastPaint=now;}
    if(now-lastSaved>4000){save();lastSaved=now;}
    if(engine.ended){setPlaying(false);render();save();showReview();}
  }
  requestAnimationFrame(loop);
}
function researchContext(withImage=false){
 if(!engine)return null;
 const visible=isStock()?stockChartBars(engine.data,engine.index):isDaily()?[...engine.data.historyDaily,...engine.data.dailyBars.slice(0,engine.index+1)]:bars;
 let image=null;if(withImage)try{image=$('chart').toDataURL?.('image/webp',.35)||null;}catch{}
 return {run:journalKey,time:engine.time,mode:isStock()?'stock':isDaily()?'daily':'tick',market:engine.data.stock?.market||'TX',symbol:engine.data.stock?.symbol||null,unit:isDaily()?'交易日':`${frame/60} 分 K`,frame:isDaily()?86400:frame,blind:hiddenIdentity(),canCapture:!engine.ended&&!loading&&reviewCursor===null&&chartOffset===0&&visible.length>0,bars:visible,image};
}
const research=installResearch({document,storage:localStorage,fetch,context:researchContext,pause:()=>setPlaying(false),notify,download:downloadData,onChange:()=>drawChart()});
try{
  const r=await fetch('./data/manifest.json');if(!r.ok)throw Error('無法載入交易場次。');manifest=await r.json();
  const cr=await fetch('./data/campaigns/catalog.json');if(!cr.ok)throw Error('無法載入連續行情清單。');catalog=await cr.json();
  $('sessionSelect').innerHTML='<option value="random">隨機連續行情</option>'+manifest.map(x=>`<option value="${x.id}">${x.label} · ${x.sessionLabel||'日盤'}</option>`).join('');
  const saved=readSaved();if(saved){$('blind').checked=saved.blind!==false;if(['.5','0.5','1','2','5','15','60','300'].includes(saved.speed))$('speed').value=saved.speed;if([60,300,900,3600,86400,604800,2592000].includes(saved.frame))frame=saved.frame;if(Number.isInteger(saved.visible)&&saved.visible>=12&&saved.visible<=300)visible=saved.visible;}
  await loadSession(saved?.snapshot?.dailyPlan?.market|| (saved?.snapshot?.dailyPlan?'daily':saved?.snapshot?.campaign?'random':manifest.some(m=>m.id===saved?.snapshot?.sessionId)?saved.snapshot.sessionId:'random'),saved);
  setTimeframe(frame);
  registerTools();requestAnimationFrame(loop);
}catch(e){notify(e.message,true);$('playBtn').disabled=true;$('submitOrder').disabled=true;}
