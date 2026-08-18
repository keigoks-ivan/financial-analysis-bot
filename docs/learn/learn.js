/* ==========================================================================
   learn.js — shared JS for research.investmquest.com/learn/
   Bilingual toggle + quiz engine + progress tracker + slider-calc helper
   + predict-then-reveal + fill-blank faded examples + review deck.
   Vanilla JS, no dependencies. Defensive: every JSON.parse / DOM lookup
   is guarded so one malformed module page can't break the whole script.
   ========================================================================== */

/* ── language ─────────────────────────────────────────────────────────
   research.investmquest.com is Chinese-first, so the course defaults to zh.
   Own storage key so it does not collide with other sites' 'lang' key. */
var currentLang = (function(){
  try{ return localStorage.getItem('learn_lang') || 'zh'; }catch(e){ return 'zh'; }
})();

function elDisplay(el){
  // Return the natural display value for an element so CSS .lang-zh{display:none}
  // doesn't win when we clear the inline style on visible elements.
  var t = el.tagName;
  if(t==='SPAN'||t==='A'||t==='EM'||t==='STRONG'||t==='BR') return 'inline';
  if(t==='TR') return 'table-row';
  if(t==='TD'||t==='TH') return 'table-cell';
  return 'block';
}

function setLang(lang){
  if(lang!=='en' && lang!=='zh') lang='en';
  currentLang = lang;
  try{ localStorage.setItem('learn_lang', lang); }catch(e){}

  document.querySelectorAll('.lang-en').forEach(function(e){
    e.style.display = lang==='en' ? elDisplay(e) : 'none';
  });
  document.querySelectorAll('.lang-zh').forEach(function(e){
    e.style.display = lang==='zh' ? elDisplay(e) : 'none';
  });
  document.querySelectorAll('.lang-btn').forEach(function(b){
    b.classList.toggle('active', b.getAttribute('data-lang')===lang);
  });
  document.documentElement.setAttribute('lang', lang==='en' ? 'en' : 'zh-Hant');

  // quiz / predict blocks render their own bilingual markup per-question rather
  // than relying on the generic lang-en/lang-zh CSS toggle, so they must be
  // explicitly told to re-render whenever the language changes.
  renderAllQuizzes();
  renderAllPredicts();
}

/* ── small helpers ───────────────────────────────────────────────────── */
function lcPick(obj, lang){
  if(!obj) return '';
  if(typeof obj === 'string') return obj;
  return obj[lang] || obj.en || obj.zh || '';
}
function lcEsc(str){
  return String(str==null ? '' : str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ── quiz engine ─────────────────────────────────────────────────────────
   Usage: <div class="quiz-block" data-quiz='[
     {"q":{"en":"...","zh":"..."},
      "opts":[{"en":"..","zh":".."}, {"en":"..","zh":".."}],
      "a":0,
      "exp":{"en":"..","zh":".."}}
   ]'></div>
   - data-quiz is a JSON array; each item is one question.
   - "a" is the zero-based index of the correct option.
   - Optional data-quiz-id="module-slug-q1" groups a score into the
     progress tracker; falls back to an auto id if omitted.
   ------------------------------------------------------------------------ */
function initQuizzes(){
  var blocks = document.querySelectorAll('.quiz-block[data-quiz]');
  blocks.forEach(function(block, idx){
    if(block._quizData) return; // already initialized
    var raw = block.getAttribute('data-quiz');
    var data;
    try{ data = JSON.parse(raw); }catch(e){
      console.warn('learn.js: invalid data-quiz JSON, skipping block', e);
      return;
    }
    if(!Array.isArray(data)) data = [data];
    data = data.filter(function(item){ return item && item.q && Array.isArray(item.opts); });
    if(!data.length) return;

    block._quizData = data;
    block._quizState = data.map(function(){ return { selected: null }; });
    block._quizId = block.getAttribute('data-quiz-id') || ('quiz-' + idx + '-' + (location.pathname.split('/').pop() || 'page'));
    renderQuizBlock(block);
  });
}

function renderQuizBlock(block){
  if(!block || !block._quizData) return;
  var data = block._quizData, state = block._quizState, lang = currentLang;
  var html = '';

  data.forEach(function(item, qi){
    var st = state[qi];
    html += '<div class="quiz-q">';
    var fromTag = item.from ? ('<span class="quiz-from">' + (lang==='en' ? 'review · module ' : '複習：第 ') + lcEsc(item.from) + (lang==='en' ? '' : ' 課') + '</span>') : '';
    html += '<p class="quiz-question">' + (qi+1) + '. ' + lcEsc(lcPick(item.q, lang)) + fromTag + '</p>';
    html += '<div class="quiz-opts">';
    item.opts.forEach(function(opt, oi){
      var cls = 'quiz-opt';
      var answered = st.selected !== null;
      if(answered){
        if(oi === item.a) cls += ' correct';
        else if(oi === st.selected) cls += ' wrong';
      }
      html += '<button type="button" class="' + cls + '"' + (answered ? ' disabled' : '') +
        ' data-qi="' + qi + '" data-oi="' + oi + '">' + lcEsc(lcPick(opt, lang)) + '</button>';
    });
    html += '</div>';
    if(st.selected !== null){
      var correct = st.selected === item.a;
      var prefix = correct
        ? (lang==='en' ? '✓ Correct. ' : '✓ 答對了。')
        : (lang==='en' ? '✗ Not quite. ' : '✗ 不太對。');
      html += '<div class="quiz-explain">' + lcEsc(prefix) + lcEsc(lcPick(item.exp, lang)) + '</div>';
    }
    html += '</div>';
  });

  var answeredCount = state.filter(function(s){ return s.selected !== null; }).length;
  if(data.length && answeredCount === data.length){
    var score = state.filter(function(s, i){ return s.selected === data[i].a; }).length;
    var tail = lang==='en' ? ' — review the sections above for anything missed.' : ' — 如有答錯，回頭複習上方內容。';
    html += '<div class="quiz-score">' + score + '/' + data.length + tail + '</div>';
    recordQuizScore(block._quizId, score, data.length);
  }

  block.innerHTML = html;
  block.querySelectorAll('.quiz-opt').forEach(function(btn){
    btn.addEventListener('click', function(){
      var qi = parseInt(btn.getAttribute('data-qi'), 10);
      var oi = parseInt(btn.getAttribute('data-oi'), 10);
      if(isNaN(qi) || isNaN(oi)) return;
      if(block._quizState[qi].selected !== null) return;
      block._quizState[qi].selected = oi;
      recordQuestionResult(block._quizId, qi, oi === block._quizData[qi].a);
      renderQuizBlock(block);
    });
  });
}

function renderAllQuizzes(){
  document.querySelectorAll('.quiz-block[data-quiz]').forEach(renderQuizBlock);
}

/* ── progress tracker ─────────────────────────────────────────────────
   localStorage shape: { visited: { "01-basics.html": true, ... },
                          quizzes: { "quiz-id": { score, total } } } */
var LC_PROGRESS_KEY = 'invest_course_progress';

function lcGetProgress(){
  try{
    var raw = localStorage.getItem(LC_PROGRESS_KEY);
    var p = raw ? JSON.parse(raw) : null;
    if(!p || typeof p !== 'object') p = {};
    if(!p.visited) p.visited = {};
    if(!p.quizzes) p.quizzes = {};
    if(!p.qlog) p.qlog = {};
    if(!p.predicts) p.predicts = {};
    return p;
  }catch(e){
    return { visited:{}, quizzes:{}, qlog:{}, predicts:{} };
  }
}
function lcSaveProgress(p){
  try{ localStorage.setItem(LC_PROGRESS_KEY, JSON.stringify(p)); }catch(e){}
}
function markModuleVisited(page){
  if(!page) return;
  var p = lcGetProgress();
  p.visited[page] = true;
  lcSaveProgress(p);
}
function recordQuizScore(quizId, score, total){
  if(!quizId) return;
  var p = lcGetProgress();
  p.quizzes[quizId] = { score: score, total: total };
  lcSaveProgress(p);
}
// per-question log feeds the review deck (wrong answers come back sooner)
function recordQuestionResult(quizId, qi, ok){
  if(!quizId || quizId === 'review') return; // review deck logs by bank id itself
  var p = lcGetProgress();
  var key = quizId + '#' + qi;
  var prev = p.qlog[key] || { asked:0, wrong:0 };
  prev.asked += 1; if(!ok) prev.wrong += 1; prev.last = Date.now(); prev.ok = !!ok;
  p.qlog[key] = prev;
  lcSaveProgress(p);
}

// Auto-mark the current page visited, unless it's the course home or the
// module template (those aren't "modules completed").
function autoMarkVisited(){
  var page = (location.pathname.split('/').pop() || '').trim();
  if(!page) return;
  if(page === 'index.html' || page === '_template.html') return;
  if(!/^\d\d-.*\.html$/.test(page)) return;
  markModuleVisited(page);
}

// Course home page: stamp a done-badge on any .module-card whose href
// matches a visited module page.
function applyProgressToCourseMap(){
  var map = document.querySelector('.course-map');
  if(!map) return;
  var p = lcGetProgress();
  map.querySelectorAll('.module-card').forEach(function(card){
    var href = card.getAttribute('href') || '';
    var page = href.split('/').pop();
    if(page && p.visited[page]){
      card.classList.add('completed');
      if(!card.querySelector('.module-card-done')){
        var badge = document.createElement('span');
        badge.className = 'module-card-done';
        badge.textContent = '✓';
        card.appendChild(badge);
      }
    }
  });
}

/* ── slider-calculator helper ────────────────────────────────────────
   initCalc(id, computeFn)
   - id: the DOM id of the .calc-card element.
   - computeFn(values): receives { inputName: numericValue, ... } built
     from every input[type=range]/input[type=number] inside the card
     (keyed by name, falling back to id), returns { outKey: displayValue }.
   Each output key is written into a `[data-out="outKey"]` element in the
   card, and each input's live value is echoed into any
   `[data-echo="inputId"]` element (typically next to a slider). */
function initCalc(id, computeFn){
  var card = document.getElementById(id);
  if(!card || typeof computeFn !== 'function') return;
  var inputs = card.querySelectorAll('input[type=range], input[type=number]');
  if(!inputs.length) return;

  function update(){
    var values = {};
    inputs.forEach(function(inp){
      var key = inp.name || inp.id;
      if(!key) return;
      var n = parseFloat(inp.value);
      values[key] = isNaN(n) ? 0 : n;
      if(inp.id){
        var echo = card.querySelector('[data-echo="' + inp.id + '"]');
        if(echo) echo.textContent = inp.value;
      }
    });
    var outputs;
    try{
      outputs = computeFn(values) || {};
    }catch(e){
      console.warn('learn.js: initCalc computeFn threw', e);
      outputs = {};
    }
    Object.keys(outputs).forEach(function(key){
      var out = card.querySelector('[data-out="' + key + '"]');
      if(out) out.textContent = outputs[key];
    });
  }

  inputs.forEach(function(inp){
    inp.addEventListener('input', update);
  });
  update();
}

/* ── predict-then-reveal ─────────────────────────────────────────────
   Calibration exercise: the reader commits to a call BEFORE seeing what
   actually happened. There is no "correct" option scored — the point is to
   notice the gap between your prior and the outcome.
   Usage: <div class="predict-block" data-predict-id="05-p1" data-predict='{
     "q":{"en":"...","zh":"..."},
     "opts":[{"en":"..","zh":".."}, ...],
     "reveal":{"en":"...","zh":"..."}
   }'></div> */
function initPredicts(){
  document.querySelectorAll('.predict-block[data-predict]').forEach(function(block, idx){
    if(block._pdata) return;
    var data;
    try{ data = JSON.parse(block.getAttribute('data-predict')); }catch(e){
      console.warn('learn.js: invalid data-predict JSON, skipping block', e); return;
    }
    if(!data || !data.q || !Array.isArray(data.opts) || !data.reveal) return;
    block._pdata = data;
    block._pid = block.getAttribute('data-predict-id') || ('predict-' + idx + '-' + (location.pathname.split('/').pop() || 'page'));
    var p = lcGetProgress();
    block._pchosen = (p.predicts && typeof p.predicts[block._pid] === 'number') ? p.predicts[block._pid] : null;
    renderPredictBlock(block);
  });
}
function renderPredictBlock(block){
  if(!block || !block._pdata) return;
  var d = block._pdata, lang = currentLang, chosen = block._pchosen;
  var html = '<div class="predict-title">' + (lang==='en' ? 'Commit first, then reveal' : '先下判斷，再揭曉') + '</div>';
  html += '<p class="predict-question">' + lcEsc(lcPick(d.q, lang)) + '</p>';
  html += '<div class="predict-opts">';
  d.opts.forEach(function(opt, oi){
    var cls = 'predict-opt' + (chosen === oi ? ' chosen' : '');
    html += '<button type="button" class="' + cls + '"' + (chosen !== null ? ' disabled' : '') + ' data-oi="' + oi + '">' + lcEsc(lcPick(opt, lang)) + '</button>';
  });
  html += '</div>';
  if(chosen !== null){
    html += '<div class="predict-reveal"><div class="predict-you">' + (lang==='en' ? 'Your call: ' : '你的判斷：') + lcEsc(lcPick(d.opts[chosen], lang)) + '</div>' + lcEsc(lcPick(d.reveal, lang)) + '</div>';
  }
  block.innerHTML = html;
  block.querySelectorAll('.predict-opt').forEach(function(btn){
    btn.addEventListener('click', function(){
      if(block._pchosen !== null) return;
      var oi = parseInt(btn.getAttribute('data-oi'), 10);
      if(isNaN(oi)) return;
      block._pchosen = oi;
      var p = lcGetProgress(); p.predicts[block._pid] = oi; lcSaveProgress(p);
      renderPredictBlock(block);
    });
  });
}
function renderAllPredicts(){
  document.querySelectorAll('.predict-block[data-predict]').forEach(renderPredictBlock);
}

/* ── fill-blank faded worked example ─────────────────────────────────
   Usage: <div class="fill-blank"> ... <input class="fb-input" data-answer="12.5" data-tol="0.3"> ...
            <button type="button" class="fb-check">...</button><div class="fb-result"></div></div>
   data-answer is numeric; data-tol is absolute tolerance (default 1% of |answer| or 0.01). */
function initFillBlanks(){
  document.querySelectorAll('.fill-blank').forEach(function(box){
    var btn = box.querySelector('.fb-check');
    if(!btn || btn._wired) return;
    btn._wired = true;
    btn.addEventListener('click', function(){
      var inputs = box.querySelectorAll('.fb-input[data-answer]');
      var ok = 0, total = 0;
      inputs.forEach(function(inp){
        /* skip inputs inside the hidden language layer (each blank exists once per language) */
        var langWrap = inp.closest('.lang-en, .lang-zh');
        if(langWrap && !langWrap.classList.contains('lang-' + currentLang)) return;
        if(inp.offsetParent === null) return;
        total += 1;
        var ans = parseFloat(inp.getAttribute('data-answer'));
        var tolAttr = inp.getAttribute('data-tol');
        var tol = tolAttr ? parseFloat(tolAttr) : Math.max(Math.abs(ans) * 0.01, 0.01);
        var v = parseFloat(String(inp.value).replace(/[%,$,\s]/g,''));
        var good = !isNaN(v) && Math.abs(v - ans) <= tol;
        inp.classList.toggle('ok', good);
        inp.classList.toggle('bad', !good);
        if(good) ok += 1;
      });
      var res = box.querySelector('.fb-result');
      if(res){
        res.textContent = currentLang==='en'
          ? (ok + '/' + total + ' correct' + (ok===total ? ' — well done.' : ' — red boxes are off; re-read the worked example above.'))
          : (ok + '/' + total + ' 正確' + (ok===total ? '——很好。' : '——紅框的數字不對，回頭看上方的逐步範例。'));
      }
    });
  });
}

/* ── review deck (review.html) ───────────────────────────────────────
   Loads review-bank.json (built by scripts/learn/course.py review from every
   module's data-quiz), then draws N questions weighted toward: modules the
   reader has visited, questions answered wrong before, questions never seen.
   Spaced-retrieval in the cheapest possible form — no server, no accounts. */
function initReviewDeck(){
  var host = document.getElementById('review-deck');
  if(!host) return;
  var metaEl = document.getElementById('review-meta');
  var btnAll = document.getElementById('review-all');
  var btnVisited = document.getElementById('review-visited');
  var bank = null;

  function draw(scope){
    if(!bank) return;
    var p = lcGetProgress();
    var visited = Object.keys(p.visited || {}).map(function(f){ return f.slice(0,2); });
    var pool = bank.filter(function(q){ return scope==='all' || !visited.length || visited.indexOf(q.module) >= 0; });
    if(!pool.length) pool = bank.slice();
    // weight
    var weighted = pool.map(function(q){
      var log = p.qlog[q.id] || null;
      var w = 1;
      if(!log) w = 2;                 // never seen → likely
      else if(!log.ok) w = 3;         // last answer wrong → most likely
      else if(log.asked >= 3) w = 0.5; // known well → rare
      return { q:q, w:w };
    });
    var picked = [], N = Math.min(12, weighted.length);
    for(var i=0;i<N;i++){
      var tot = weighted.reduce(function(s,x){ return s + x.w; }, 0);
      var r = Math.random() * tot, acc = 0, idx = 0;
      for(var j=0;j<weighted.length;j++){ acc += weighted[j].w; if(r <= acc){ idx = j; break; } }
      picked.push(weighted[idx].q);
      weighted.splice(idx,1);
    }
    var data = picked.map(function(q){ return { q:q.q, opts:q.opts, a:q.a, exp:q.exp, from:q.module }; });
    host.innerHTML = '';
    var block = document.createElement('div');
    block.className = 'quiz-block';
    block.setAttribute('data-quiz-id', 'review-' + Date.now());
    block.setAttribute('data-quiz', JSON.stringify(data));
    host.appendChild(block);
    // per-question ids must map back to the bank ids for the log
    initQuizzes();
    block._quizId = 'review';
    // override recording so results are keyed by bank id
    block._bankIds = picked.map(function(q){ return q.id; });
    renderQuizBlock(block);
    // delegated capture listener survives re-renders (renderQuizBlock replaces innerHTML)
    block.addEventListener('click', function(ev){
      var btn = ev.target && ev.target.closest ? ev.target.closest('.quiz-opt') : null;
      if(!btn || btn.disabled) return;
      var qi = parseInt(btn.getAttribute('data-qi'), 10);
      var oi = parseInt(btn.getAttribute('data-oi'), 10);
      if(isNaN(qi)||isNaN(oi)) return;
      if(block._quizState[qi].selected !== null) return;
      var q = picked[qi]; if(!q) return;
      var pp = lcGetProgress();
      var prev = pp.qlog[q.id] || { asked:0, wrong:0 };
      prev.asked += 1; if(oi !== q.a) prev.wrong += 1; prev.last = Date.now(); prev.ok = (oi === q.a);
      pp.qlog[q.id] = prev;
      lcSaveProgress(pp);
    }, true);
    if(metaEl){
      metaEl.textContent = currentLang==='en'
        ? (picked.length + ' questions drawn from ' + (scope==='all' ? 'all modules' : 'modules you have visited') + ' (' + bank.length + ' in bank).')
        : ('本輪抽出 ' + picked.length + ' 題，來源：' + (scope==='all' ? '全部課程' : '你已讀過的課') + '（題庫共 ' + bank.length + ' 題）。');
    }
  }

  fetch('review-bank.json', { cache:'no-store' }).then(function(r){ return r.json(); }).then(function(b){
    bank = Array.isArray(b) ? b : (b.questions || []);
    draw('visited');
  }).catch(function(e){
    host.textContent = currentLang==='en' ? 'Review bank not available.' : '題庫載入失敗。';
  });
  if(btnAll) btnAll.addEventListener('click', function(){ draw('all'); });
  if(btnVisited) btnVisited.addEventListener('click', function(){ draw('visited'); });
}

/* ── boot ────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function(){
  initQuizzes();
  initPredicts();
  initFillBlanks();
  setLang(currentLang);
  autoMarkVisited();
  applyProgressToCourseMap();
  initReviewDeck();
});
