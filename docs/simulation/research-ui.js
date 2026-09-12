import {RESEARCH_KEY,hash,newResearch,addIdea,reserveUniverse,markSeen,beginTrial,addOpportunity,addQuickObservation,analysisPacket,resolveOpportunities,evaluateStock,researchStats} from './research.js';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct=n=>n===null||n===undefined?'—':(n*100).toFixed(2)+'%';
export function installResearch({document,storage,fetch,context,pause,notify,download,onChange=()=>{}}){
 const $=id=>document.getElementById(id);let state,failed=false,busy=false,pauseRequested=false,editing=null,catalog=null,actions=null,selected=null,lastContext=null,lastRefresh=null,launching=false,quickContext=null;
 try{
  const raw=storage.getItem(RESEARCH_KEY);state=raw?JSON.parse(raw):newResearch();
  if(state.version!==1||!['ideas','cases','trials','seen','used'].every(k=>Array.isArray(state[k]))||!(state.heldouts===null||Array.isArray(state.heldouts)))throw Error('研究紀錄格式無效');
  const current=JSON.parse(storage.getItem('tx-replay-v1')||'null'),journal=JSON.parse(storage.getItem('tx-replay-journal-v1')||'[]');
  for(const w of [current,...journal.map(j=>j.workspace)])markSeen(state,w?.snapshot?.dailyPlan?.symbol);
  storage.setItem(RESEARCH_KEY,JSON.stringify(state));
 }catch{state=newResearch();failed=true;}
 const persist=()=>{storage.setItem(RESEARCH_KEY,JSON.stringify(state));};
 const change=fn=>{if(failed)throw Error('研究紀錄無法讀寫，已停用研究操作；交易練習仍可使用。');const before=JSON.stringify(state);try{const result=fn();if(result!==false)persist();return result;}catch(e){state=JSON.parse(before);throw e;}};
 const version=()=>state.ideas.flatMap(i=>i.versions).find(v=>v.id===selected);
 const note=(message,error=false)=>{$('researchStatus').textContent=message;$('researchStatus').className='notice'+(error?' error':'');};
 const guard=fn=>async(...args)=>{try{return await fn(...args);}catch(e){note(e.message,true);notify(e.message,true);}};
 const request=async path=>{const r=await fetch(path);if(!r.ok)throw Error('研究行情載入失敗，可稍後繼續同一批驗證。');return r.json();};
 async function universe(){if(!catalog)catalog=await request('./data/stocks/catalog.json');change(()=>reserveUniverse(state,catalog));return catalog;}
 function fillEditor(v=null){
  editing=v?state.ideas.find(i=>i.versions.some(x=>x.id===v.id)).id:null;
  const defaults={market:context()?.market==='US'?'US':'TW',setup:'pullback',trend:60,band:1,lookback:20,volume:'shrink',hold:10,stop:5,allocation:10};
  for(const [id,value] of Object.entries({ideaTitle:v?.title||'',ideaHypothesis:v?.hypothesis||'',ideaFailure:v?.invalidation||''}))$(id).value=value;
  for(const [key,value] of Object.entries(v?.rules||defaults))$('rule-'+key).value=String(value);
  $('ideaSave').textContent=v?'儲存為新版本':'建立想法';$('researchEditor').hidden=false;$('exploreIdea').disabled=true;$('finalIdea').disabled=true;
 }
 function renderFocus(){
  const notes=state.cases.filter(c=>c.quick);if(notes.length){$('ideaFocus').textContent=notes.at(-1).reason;$('ideaProgress').textContent=`${notes.length} 筆快速觀察 · 先累積案例，再整理規則` ;return;}
  const v=version(),cases=state.cases.filter(c=>c.versionId===v?.id),ready=cases.filter(c=>Number.isFinite(c.outcomes[10]?.return)).length;
  $('ideaFocus').textContent=v?v.title+' · v'+v.number:'找到值得重複驗證的現象';
  $('ideaProgress').textContent=v?`${cases.length} 個案例 · ${ready} 個已揭露後 10 根結果`:'先留下判斷，往後重播再看結果。';
 }
 function render(){
  renderFocus();
  $('observationCount').textContent=state.cases.length+' 個已保存案例';
  $('observationList').innerHTML=state.cases.slice().reverse().map(c=>`<details class="research-case"><summary>${c.direction===1?'看漲':c.direction===-1?'看跌':'先觀察'} · ${esc(c.reason.slice(0,80))}</summary><p>${esc(c.reason)}</p><p class="muted">${c.blind?'盲測標的':esc(c.symbol||'台指期')} · ${esc(c.unit)}${c.quick?'':' · 既有研究版本案例'}</p>${c.image?.startsWith('data:image/webp;base64,')?`<img src="${c.image}" alt="記錄當下可見的圖表">`:''}<div class="research-outcomes">${[5,10,20].map(n=>{const o=c.outcomes[n];return `<span>後 ${n} 根<b>${o?.unavailable?'不適用':o?pct(c.direction===0?o.change:o.return):'尚未揭露'}</b><small>${c.direction===0?'價格漲跌':'依看漲／看跌方向計算'} · 未扣交易成本</small></span>`;}).join('')}</div></details>`).join('')||'<p class="muted">看到值得研究的現象，按「標記目前圖表」，留一句話即可。</p>';
  const versions=state.ideas.flatMap(i=>i.versions),v=version();
  for(const id of ['researchVersion','captureVersion']){$(id).innerHTML='<option value="">選擇想法版本</option>'+versions.map(v=>`<option value="${v.id}">${esc(v.title)} · v${v.number}</option>`).join('');$(id).value=selected||'';}
  $('researchCount').textContent=`${state.ideas.length} 個想法 · ${state.cases.length} 個案例`;
  $('researchSelected').innerHTML=v?`<h3>${esc(v.title)} <small>v${v.number}${state.trials.some(t=>t.versionId===v.id&&t.kind==='final')?' · 已凍結':''}</small></h3><p>${esc(v.hypothesis)}</p><p class="muted">失效條件：${esc(v.invalidation)}</p><p>${ruleText(v.rules)}</p>`:'<p>先建立一個想法，再回到圖表按「記錄機會」。所有修訂另存版本，原始判斷與試驗保留。</p>';
  $('ideaRevise').disabled=!v||busy;$('exploreIdea').disabled=!v||busy||failed||!$('researchEditor').hidden;$('finalIdea').disabled=!v||busy||failed||!$('researchEditor').hidden||state.trials.some(t=>t.versionId===v.id&&t.kind==='final');
  $('researchPause').hidden=!busy;
  const cases=state.cases.filter(c=>c.versionId===selected),h=Number($('caseHorizon').value)||10;
  const groups=[...new Set(cases.map(c=>c.market+' · '+c.unit))];
  const rows=groups.flatMap(group=>['trade','skip','observe'].map(decision=>{const all=cases.filter(c=>c.market+' · '+c.unit===group&&c.decision===decision),done=all.filter(c=>Number.isFinite(c.outcomes[h]?.return));return `<tr><td>${esc(group)}</td><td>${{trade:'打算交易',skip:'選擇不做',observe:'只觀察'}[decision]}</td><td>${done.length} / ${all.length}</td><td>${done.length?pct(done.reduce((s,c)=>s+c.outcomes[h].return,0)/done.length):'—'}</td><td>${done.length?pct(done.filter(c=>c.outcomes[h].return>0).length/done.length):'—'}</td></tr>`;}));
  $('caseStatistics').innerHTML=`<table><thead><tr><th>市場／時間單位</th><th>當時決策</th><th>已揭露 / 全部</th><th>平均方向報酬</th><th>正報酬比例</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  $('researchCases').innerHTML=cases.slice().reverse().map(c=>`<details class="research-case"><summary>${c.blind?'盲測案例':esc(c.symbol||'台指期')} · ${c.direction===1?'看漲':'看跌'} · ${esc(c.unit)} · ${new Date(c.created).toLocaleDateString('zh-TW')}</summary><p>${esc(c.reason)}</p><p>失效：${esc(c.failure)}</p>${c.image?.startsWith('data:image/webp;base64,')?`<img src="${c.image}" alt="記錄當下可見的圖表">`:''}<div class="research-outcomes">${[5,10,20].map(n=>{const o=c.outcomes[n];return `<span>${n} ${esc(c.unit)}<b>${o?.unavailable?'不適用':o?pct(o.return):'待揭露'}</b><small>${o?.unavailable?esc(o.unavailable):o?'有利 '+pct(o.favorable)+' / 不利 '+pct(o.adverse):'繼續同一局、同一週期後更新'}</small></span>`;}).join('')}</div></details>`).join('')||'<p class="muted">尚未記錄案例。案例只在重播走到對應位置後結算，不提前讀取未來。</p>';
  $('researchTrials').innerHTML=state.trials.filter(t=>t.versionId===selected).slice().reverse().map(t=>trialHTML(t)).join('')||'<p class="muted">尚未試驗。探索使用 12 檔；最終驗證凍結此版本，使用 8 檔尚未揭露的預留股票。</p>';
  if(failed)note('研究紀錄無法讀寫，已停用驗證，避免把已看過的行情誤認為陌生資料。',true);
 }
 function ruleText(r){return `${r.market==='TW'?'台股':'美股'}現股做多；收盤高於 MA${r.trend}，且該均線高於 5 日前。${r.setup==='pullback'?`距 MA20 不超過 ${r.band}%`:r.setup==='breakout'?`收盤突破前 ${r.lookback} 日最高價`:'趨勢條件成立即為訊號'}。${r.volume==='any'?'不加量能條件':r.volume==='shrink'?'成交量 ≤ 前 20 日均量的 0.8 倍':'成交量 ≥ 前 20 日均量的 1.5 倍'}。隔日開盤參考價進場，投入起始資金 ${r.allocation}%；持有 ${r.hold} 日後下一開盤出場${r.stop?`，另設訊號收盤價下方 ${r.stop}% 的停損`:''}。`;}
 function trialHTML(t){
  const trades=t.results.flatMap(r=>r.trades),controls=t.results.flatMap(r=>r.controls),s=researchStats(trades),b=researchStats(controls),complete=t.status==='complete';
  const count=t.results.length;
  return `<article class="research-trial"><h3>${t.kind==='final'?'凍結版本・未見標的驗證':'探索批次'} <small>${complete?'已完成':t.status==='running'?'執行中':'可繼續'} · ${count} / ${t.symbols.length} 檔</small></h3><p>${t.kind==='final'?'此版本僅能建立一次最終驗證；失敗或中斷仍占用同一批標的。':'結果屬探索資料，不能視為陌生行情成績。'} 本想法已保留 ${state.trials.filter(x=>state.ideas.find(i=>i.versions.some(v=>v.id===x.versionId))?.id===state.ideas.find(i=>i.versions.some(v=>v.id===t.versionId))?.id).length} 次試驗。</p>${s.count?`<div class="statistics-grid"><div><span>完成交易</span><strong>${s.count}</strong></div><div><span>平均每筆淨報酬</span><strong>${pct(s.mean)}</strong></div><div><span>正報酬比例</span><strong>${pct(s.winRate)}</strong></div><div><span>同條件對照 ${b.count} 筆</span><strong>${pct(b.mean)}</strong></div><div><span>成本加倍估算</span><strong>${pct(s.stress)}</strong></div><div><span>前 5 筆占正報酬合計</span><strong>${pct(s.top5)}</strong></div></div><p>${s.interval?`按進場月份重抽樣的 95% 參考區間：${pct(s.interval[0])} ～ ${pct(s.interval[1])}（${s.months} 個月份）。`:'月份群組不足，暫不估計不確定區間。'}${s.interval&&s.interval[0]>0?'此批平均報酬為正，仍須檢查對照、集中度與重複試驗偏誤。':'目前不足以認定具有穩定優勢。'}</p><details><summary>分年與分標的結果</summary>${groupTable(s.years)}${groupTable(s.symbols)}</details>`:'<p>尚無完成交易；不把沒有訊號當成零報酬的勝利。</p>'}<p>拒單／無法進場 ${t.results.reduce((s,r)=>s+r.rejected,0)} 次；未能在延長 5 日內平倉 ${t.results.reduce((s,r)=>s+r.unclosed,0)} 次（不列入完成交易報酬）。</p>${Object.keys(t.errors).length?`<p class="down">${Object.keys(t.errors).length} 檔資料未完成；結果尚非整批。可繼續重試同一批。</p>`:''}<div class="journal-actions">${!complete?`<button data-research="resume" data-id="${t.id}" ${busy?'disabled':''}>繼續此批</button>`:''}<button data-research="export-trial" data-id="${t.id}" ${busy?'disabled':''}>下載逐筆試驗紀錄</button></div></article>`;
 }
 const groupTable=groups=>`<table><thead><tr><th>分組</th><th>交易數</th><th>平均淨報酬</th></tr></thead><tbody>${groups.map(g=>`<tr><td>${esc(g.label)}</td><td>${g.count}</td><td>${pct(g.mean)}</td></tr>`).join('')}</tbody></table>`;
 async function execute(trial){
  if(busy)return;busy=true;pauseRequested=false;render();
  try{
   if(!actions)actions=await request('./data/stocks/actions.json');
   if(trial.model!=='stock-daily-study-v1'||trial.actionsHash!==hash(JSON.stringify(actions)))throw Error('驗證模型或權息附檔已改變，不能混用這批凍結資料；請保留原紀錄。');
   for(const symbol of trial.symbols){
    if(pauseRequested)break;
    if(trial.results.some(r=>r.symbol===symbol))continue;
    note(`正在驗證第 ${trial.results.length+1} / ${trial.symbols.length} 檔；規則已固定，請稍候。`);
    try{
     const pool=await request('./data/stocks/'+symbol+'.json');if(pool.sha256!==trial.hashes[symbol])throw Error('行情版本已改變，不能混用本次凍結資料。');
     const meta=(await universe()).find(s=>s.symbol===symbol);if(!meta||hash(JSON.stringify(meta.liquidity))!==trial.liquidityHashes?.[symbol])throw Error('成交活躍度篩選已改變，不能混用凍結批次。');
     const result=await evaluateStock(pool,meta.liquidity,trial.rules,actions,()=>new Promise(resolve=>setTimeout(resolve,0)));
     change(()=>{trial=state.trials.find(t=>t.id===trial.id);trial.results.push(result);delete trial.errors[symbol];});
    }catch(e){change(()=>{trial=state.trials.find(t=>t.id===trial.id);trial.errors[symbol]=e.message;});}
    render();await new Promise(resolve=>setTimeout(resolve,0));
   }
   change(()=>{trial=state.trials.find(t=>t.id===trial.id);trial.status=trial.results.length===trial.symbols.length?'complete':'paused';});
   note(trial.status==='complete'?'本批驗證完成，所有試驗與規則已保存。':'已保存目前進度，稍後可繼續同一批。');
  }catch(e){change(()=>{state.trials.find(t=>t.id===trial.id).status='paused';});throw e;}finally{busy=false;render();}
 }
 $('researchBtn').onclick=guard(()=>{pause();render();$('researchDialog').showModal();});
 $('quickResearch').onclick=()=>$('researchBtn').onclick();
 $('quickIdeaNew').onclick=()=>$('recordOpportunity').onclick();
 $('ideaNew').onclick=()=>fillEditor();$('ideaRevise').onclick=()=>{if(version())fillEditor(version());};
 $('researchVersion').onchange=()=>{selected=$('researchVersion').value;$('researchEditor').hidden=true;render();};$('caseHorizon').onchange=render;
 $('ideaForm').onsubmit=guard(e=>{e.preventDefault();const rules=Object.fromEntries(['market','setup','trend','band','lookback','volume','hold','stop','allocation'].map(k=>[k,$('rule-'+k).value]));const v=change(()=>addIdea(state,{title:$('ideaTitle').value,hypothesis:$('ideaHypothesis').value,invalidation:$('ideaFailure').value,rules},editing));selected=v.id;$('researchEditor').hidden=true;render();note('想法版本已保存。可回到圖表記錄機會，或先跑探索批次。');});
 $('recordStructured').onclick=guard(()=>{pause();lastContext=context(true);if(!lastContext?.canCapture)throw Error('請回到未結束的最新行情，再記錄機會。');if(!state.ideas.length){fillEditor();render();$('researchDialog').showModal();note('先建立想法，再記錄當下機會。');return;}render();$('captureVersion').value=selected||state.ideas.at(-1).versions.at(-1).id;$('captureReason').value='';$('captureFailure').value=state.ideas.flatMap(i=>i.versions).find(v=>v.id===$('captureVersion').value)?.invalidation||'';$('captureDecision').value='observe';$('captureDirection').value='1';$('captureDialog').showModal();});
 $('captureForm').onsubmit=guard(e=>{e.preventDefault();const now=context();if(now?.run!==lastContext?.run||now?.time!==lastContext?.time||!now.canCapture)throw Error('行情已移動，請重新記錄機會。');const v=state.ideas.flatMap(i=>i.versions).find(v=>v.id===$('captureVersion').value);if(!v)throw Error('請選擇想法版本。');change(()=>addOpportunity(state,v,lastContext,{decision:$('captureDecision').value,direction:Number($('captureDirection').value),reason:$('captureReason').value,failure:$('captureFailure').value}));selected=v.id;$('captureDialog').close();render();onChange();notify('機會已保存；後續只在行情揭露後更新結果。');});
 $('recordOpportunity').onclick=guard(()=>{pause();quickContext=context(true);if(!quickContext?.canCapture)throw Error('請回到未結束的最新行情，再標記想法。');$('quickNoteText').value='';$('quickNoteDirection').value='0';$('quickNoteDialog').showModal();});
 $('newObservation').onclick=guard(async()=>{$('researchDialog').close();await $('recordOpportunity').onclick();});
 $('quickNoteForm').onsubmit=guard(e=>{e.preventDefault();const now=context();if(!now?.canCapture||now.run!==quickContext?.run||now.time!==quickContext?.time||now.frame!==quickContext?.frame)throw Error('行情已移動，請重新標記圖表。');change(()=>addQuickObservation(state,quickContext,{reason:$('quickNoteText').value,direction:Number($('quickNoteDirection').value)}));$('quickNoteDialog').close();render();onChange();notify('想法與當下圖表已保存。可以繼續看圖，之後一起交給我分析。');});
 for(const id of ['prepareAnalysis','prepareAnalysisDialog'])$(id).onclick=()=>{pause();$('analysisDialog').showModal();};
 $('downloadAnalysis').onclick=guard(()=>{if(busy)throw Error('請先暫停規則試驗，再匯出分析檔。');const packet=analysisPacket(state,context());download(JSON.stringify(packet,null,2),'trading-idea-analysis.json');notify('分析檔已準備下載；請附到目前對話，我就能接著整理與回測。');});
 async function launch(kind){
  if(busy||launching)return;launching=true;
  try{pause();const v=version();if(!v)return;const c=await universe();if(!actions)actions=await request('./data/stocks/actions.json');const trial=change(()=>{const t=beginTrial(state,v,c,kind);t.actionsHash=hash(JSON.stringify(actions));return t;});await execute(trial);}finally{launching=false;}
 }
 $('exploreIdea').onclick=guard(()=>launch('explore'));
 $('finalIdea').onclick=guard(()=>{if(!version())return;$('finalConfirmText').textContent='此版本將固定規則並使用 8 檔預留股票。啟動後，這批資料永久視為已使用；即使結果不佳或中斷，也不能重抽同一版本的考題。';$('finalResearchDialog').showModal();});
 $('finalResearchStart').onclick=guard(async()=>{$('finalResearchDialog').close();await launch('final');});
 $('researchPause').onclick=()=>{pauseRequested=true;note('本檔完成後暫停，已完成結果會保存。');};
 $('researchExport').onclick=guard(()=>{if(busy||context()?.blind)throw Error('請先結束目前盲測與試驗，再下載完整研究紀錄。');download(JSON.stringify(state,null,2),'trading-research.json');});
 $('researchDialog').addEventListener('click',guard(async e=>{const b=e.target.closest('[data-research]');if(!b)return;const trial=state.trials.find(t=>t.id===b.dataset.id);if(!trial)return;if(b.dataset.research==='resume'){await universe();await execute(trial);}else if(!busy)download(JSON.stringify(trial,null,2),'research-'+trial.id+'.json');}));
 fillEditor();if(state.ideas.length){selected=state.ideas.at(-1).versions.at(-1)?.id;$('researchEditor').hidden=true;}render();
 return {
  explorationCatalog(c){catalog=c;if(failed)throw Error('研究隔離紀錄無法讀取，暫停抽取新股票。');return change(()=>reserveUniverse(state,c));},
  markers(run){return state.cases.filter(c=>c.run===run).map((c,i)=>({time:c.time,label:'想'+(i+1)}));},
  refresh(){
   const c=context();if(!c||failed)return;
   const signature=c.run+':'+c.frame+':'+c.bars.at(-1)?.time+':'+c.canCapture;if(signature===lastRefresh)return;lastRefresh=signature;
   try{const unseen=c.symbol&&!state.seen.includes(c.symbol),pending=state.cases.some(x=>x.run===c.run&&Object.keys(x.outcomes).length<3);if(unseen||pending)change(()=>{markSeen(state,c.symbol);return resolveOpportunities(state,c)||unseen;});$('recordOpportunity').disabled=!c.canCapture;$('recordStructured').disabled=!c.canCapture;renderFocus();}catch(e){failed=true;note('研究紀錄儲存失敗；請先備份，暫停研究操作。',true);}
  }
 };
}
