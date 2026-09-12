import {ARENA_KEY,STRATEGIES,validateConfig,arenaUniverse,pickArenaPlan,runEpisode,arenaSummary,arenaPacket,readBattle,stockRules,fingerprint} from './model.js';
const $=id=>document.getElementById(id),pct=n=>(n*100).toFixed(2)+'%',money=n=>n.toLocaleString('en-US',{maximumFractionDigits:2}),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let battle=null,busy=false,storageBlocked=false,visible=120;
try{battle=readBattle(localStorage);}catch{storageBlocked=true;$('storageStatus').textContent='舊紀錄無法讀取，原始資料已保留。本次可計算與下載，但不覆寫舊資料。';}
const keys=['market','days','count','capital','allocation','ma','lookback','band','stop'];
function configure(c){for(const key of keys)$(key).value=String(c[key]);$('currency').textContent=c.market==='TW'?'TWD':'USD';}
if(battle)configure(battle.config);
$('market').onchange=()=>{const market=$('market').value;$('capital').value=stockRules(market==='TW'?'TW':'US').capital;$('currency').textContent=market==='TW'?'TWD':'USD';};
async function json(path){const r=await fetch(path);if(!r.ok)throw Error('行情載入失敗，請稍後重試。');return r.json();}
async function start(same){
 if(busy)return;
 try{
  const config=validateConfig(Object.fromEntries(keys.map(k=>[k,$(k).value]))),prediction=$('prediction').value;
  if(same&&(!battle||['market','days','count'].some(k=>config[k]!==battle.config[k])))throw Error('同組重跑請保持市場、長度與組數；要改這些設定，請抽新行情。');
  busy=true;$('settings').disabled=true;$('start').disabled=true;$('rerun').disabled=true;$('status').textContent='準備相同的行情與交易條件…';
  const folder='../data/stocks/',catalog=await json(folder+(config.market==='ETF'?'index-etfs':'catalog')+'.json'),actions=await json(folder+(config.market==='ETF'?'index-actions':'actions')+'.json'),actionsHash=fingerprint(JSON.stringify(actions));
  if(same&&battle.actionsHash!==actionsHash)throw Error('公司行動資料已更新，請抽新行情，避免重跑時資料口徑改變。');
  const eligible=arenaUniverse(catalog,config),plans=[],episodes=[];
  for(let i=0;i<config.count;i++){
   let item,plan;
   if(same){plan=battle.episodes[i].plan;item=eligible.find(s=>s.symbol===plan.symbol);if(!item||item.sha256!==plan.sourceHash)throw Error('行情來源已改變，請抽新行情。');}
   else{const shuffled=eligible.map(s=>({s,r:Math.random()})).sort((a,b)=>a.r-b.r);for(const x of shuffled){plan=pickArenaPlan(x.s,config.days,plans);if(plan){item=x.s;break;}}}
   if(!item||!plan)throw Error('沒有足夠且不重疊的行情，請減少組數或改選市場。');
   plans.push(plan);const pool=await json(folder+encodeURIComponent(item.symbol)+'.json');
   $('status').textContent=`第 ${i+1}／${config.count} 組：四套規則使用同一段行情計算中…`;
   await new Promise(resolve=>setTimeout(resolve,0));episodes.push(runEpisode(pool,plan,config,actions));
  }
  const result={version:1,id:same?battle.id:'arena-'+Date.now(),created:Date.now(),attempt:same?battle.attempt+1:1,config,actionsHash,prediction,episodes};
  battle=result;visible=120;
  if(!storageBlocked){try{localStorage.setItem(ARENA_KEY,JSON.stringify(result));$('storageStatus').textContent='';}catch{$('storageStatus').textContent='本機空間不足，本次結果仍可下載。請先下載再離開，舊紀錄未被清空。';}}
  render();$('status').textContent='對戰完成。請同時看報酬、回撤與交易內容。';$('results').scrollIntoView({block:'start',behavior:'smooth'});
 }catch(e){$('status').textContent=e.message;}finally{busy=false;$('settings').disabled=false;$('start').disabled=false;$('rerun').disabled=!battle;}
}
$('start').onclick=()=>start(false);$('rerun').onclick=()=>start(true);
$('download').onclick=()=>{try{const packet=arenaPacket(battle),url=URL.createObjectURL(new Blob([JSON.stringify(packet,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=battle.id+'-attempt-'+battle.attempt+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(e){$('status').textContent=e.message;}};
function table(head,rows){return '<table><thead><tr>'+head.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(c=>'<td>'+esc(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
function render(){
 $('results').hidden=!battle;$('rerun').disabled=!battle;if(!battle)return;
 const rows=arenaSummary(battle.episodes).sort((a,b)=>b.averageReturn-a.averageReturn),c=battle.config,winners=rows.filter(r=>Math.abs(r.averageReturn-rows[0].averageReturn)<1e-10);
 $('headline').textContent=winners.length===1?rows[0].name+'，本次平均報酬最高':'本次最高報酬並列：'+winners.map(r=>r.name).join('、');
 $('frozen').textContent=`本次已凍結：${c.market} · ${c.count} 組 × ${c.days} 日 · 每帳戶 ${c.market==='TW'?'TWD':'USD'} ${money(c.capital)} · 部位 ${c.allocation}% · MA ${c.ma} · 前高 ${c.lookback} 日 · 回檔 ${c.band}% · 收盤停損 ${c.stop}%（持有基準不設） · 同組第 ${battle.attempt} 次計算。`;
 $('predictionResult').textContent=battle.prediction?'事前預測：'+STRATEGIES.find(s=>s.id===battle.prediction)?.name+'；'+(winners.some(s=>s.id===battle.prediction)?'本次符合預測。':'本次由其他規則領先。'):'本次未記錄事前預測。排名只描述這組行情，不代表已找到穩定優勢。';
 $('ranking').innerHTML=table(['策略','平均報酬','平均回撤','最差場回撤','勝過持有','進場次數','收盤持倉比例'],rows.map(r=>[r.name,pct(r.averageReturn),pct(r.averageDrawdown),pct(r.worstDrawdown),r.beatsHold===null?'基準':r.beatsHold+'／'+c.count,r.entries,pct(r.exposure)]));
 $('episode').replaceChildren();battle.episodes.forEach((e,i)=>{const option=document.createElement('option');option.value=String(i);option.textContent=`${i+1}. ${e.name} (${e.symbol}) · ${e.startDate} → ${e.endDate}`;$('episode').append(option);});$('episode').value='0';
 $('legend').innerHTML=STRATEGIES.map(s=>`<span style="color:${s.color}">━ ${esc(s.name)}</span>`).join('');detail();
}
function selection(){const episode=battle.episodes[Number($('episode').value)||0],strategy=episode.strategies.find(s=>s.id===$('strategy').value)||episode.strategies[0];return {episode,strategy};}
function detail(){
 if(!battle)return;const {episode:e,strategy:s}=selection();
 $('account').innerHTML=[['期末權益',money(s.endingEquity)+' '+e.currency],['期末持股／未實現',s.position+' 股／'+money(s.unrealized)],['已計成本',money(s.fees)],['未到帳應收款',money(s.receivables)]].map(([k,v])=>`<div class="metric"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`).join('');
 const fills=new Map(s.fills.map(f=>[f.orderId,f])),rows=s.orders.map(o=>{const f=fills.get(o.id);return [new Date((f?.time||o.submitted)*1000).toISOString().slice(0,10),o.side===1?'B 買進':'S 賣出',f?.qty??o.qty,f?money(f.price):'—',f?money(f.fee):'—',f?'已成交':o.status,o.reason+'；'+o.message];});
 for(const d of s.decisions.filter(d=>d.side===0))rows.push([d.date,'略過',0,'—','—','未送單',d.reason]);
 $('trades').innerHTML=rows.length?table(['日期','方向','股數','原始成交價','費用','狀態','原因'],rows):'<p>本段行情沒有符合規則的進場，帳戶持有現金。</p>';
 draw();
}
$('episode').onchange=()=>{visible=120;detail();};$('strategy').onchange=()=>detail();
function canvas(id){const el=$(id),w=el.clientWidth,h=el.clientHeight,d=window.devicePixelRatio||1;el.width=w*d;el.height=h*d;const c=el.getContext('2d');c.scale(d,d);c.font='11px system-ui';return {c,w,h,el};}
function draw(){
 if(!battle)return;const {episode:e,strategy:s}=selection();
 {
 const {c,w,h}=canvas('equityChart'),all=e.strategies.flatMap(s=>s.curve.map(p=>p.equity/battle.config.capital*100)),min=Math.min(...all),max=Math.max(...all),pad=(max-min)*.1||1,lo=min-pad,hi=max+pad,x=i=>12+i/(battle.config.days)*(w-75),y=v=>20+(hi-v)/(hi-lo)*(h-55);
 for(let i=0;i<=4;i++){const v=lo+(hi-lo)*i/4;c.strokeStyle='#303745';c.beginPath();c.moveTo(12,y(v));c.lineTo(w-60,y(v));c.stroke();c.fillStyle='#a7b0bf';c.fillText(v.toFixed(1),w-54,y(v)+3);}
 e.strategies.forEach(s=>{c.strokeStyle=STRATEGIES.find(r=>r.id===s.id).color;c.lineWidth=2;c.beginPath();s.curve.forEach((p,i)=>{if(i)c.lineTo(x(i),y(p.equity/battle.config.capital*100));else c.moveTo(x(i),y(p.equity/battle.config.capital*100));});c.stroke();});c.fillStyle='#a7b0bf';c.fillText(e.startDate,12,h-5);c.textAlign='right';c.fillText(e.endDate,w-60,h-5);
 }
 {
 const {c,w,h,el}=canvas('priceChart'),bars=e.chart.slice(-visible),fills=s.fills.filter(f=>f.time>=bars[0].openTime),values=[...bars.flatMap(b=>[b.high,b.low,...b.ma.filter(Number.isFinite)]),...fills.map(f=>f.chartPrice)],low=Math.min(...values),high=Math.max(...values),pad=(high-low)*.12||1,lo=low-pad,hi=high+pad,step=(w-74)/bars.length,x=i=>10+(i+.5)*step,y=v=>25+(hi-v)/(hi-lo)*(h-65);
 for(let i=0;i<=4;i++){const v=lo+(hi-lo)*i/4;c.strokeStyle='#303745';c.beginPath();c.moveTo(10,y(v));c.lineTo(w-60,y(v));c.stroke();c.fillStyle='#a7b0bf';c.fillText(v.toFixed(1),w-55,y(v)+3);}
 bars.forEach((b,i)=>{c.fillStyle=c.strokeStyle=b.close>=b.open?'#f17c87':'#5cc6aa';c.beginPath();c.moveTo(x(i),y(b.high));c.lineTo(x(i),y(b.low));c.stroke();c.fillRect(x(i)-step*.32,Math.min(y(b.open),y(b.close)),Math.max(1,step*.64),Math.max(1,Math.abs(y(b.close)-y(b.open))));});
 ['#d8fb70','#75baff','#d6a4ff'].forEach((color,k)=>{c.strokeStyle=color;c.beginPath();let begun=false;bars.forEach((b,i)=>{if(!Number.isFinite(b.ma[k]))return;if(begun)c.lineTo(x(i),y(b.ma[k]));else{c.moveTo(x(i),y(b.ma[k]));begun=true;}});c.stroke();});
 c.textAlign='center';for(const f of fills){const i=bars.findIndex(b=>f.time>=b.openTime&&f.time<=b.time);if(i<0)continue;c.fillStyle=f.side===1?'#ff9aa4':'#70e3c4';c.fillText(f.side===1?'B':'S',x(i),y(f.chartPrice)+(f.side===1?16:-10));}c.fillStyle='#a7b0bf';c.textAlign='left';c.fillText(bars[0].date,10,h-8);c.textAlign='right';c.fillText(bars.at(-1).date,w-60,h-8);el.setAttribute('aria-label',`${e.symbol} 還原權息日 K，${STRATEGIES.find(r=>r.id===s.id).name} 共 ${fills.length} 筆可見成交標記。`);
 }
}
function zoom(delta){if(!battle)return;visible=Math.max(30,Math.min(selection().episode.chart.length,visible+delta));draw();}
$('zoomIn').onclick=()=>zoom(-30);$('zoomOut').onclick=()=>zoom(30);$('priceChart').addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY>0?15:-15);},{passive:false});
new ResizeObserver(()=>draw()).observe($('equityChart'));render();
