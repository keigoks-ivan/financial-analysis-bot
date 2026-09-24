// Evaluate a Yuanta Nuxt.js SSR "window.__NUXT__=(function(a,b,...){...})(v1,v2,...)"
// payload (extracted from the 0050 fund detail page's HTML by
// build_etf_dash.py::parse_yuanta_0050_holdings) and print its `.data` array as JSON.
//
// 安全：payload 來自外部網站，視為不可信。只在獨立的 vm context 內執行（context 內
// 自建 window，不傳入任何 host 物件 → 摸不到 require／process／fs），關閉字串產碼
// （eval／new Function 在 context 內失效），5 秒逾時；payload 由 stdin 讀入，結果以
// JSON 字串（primitive）帶出。呼叫端另以精簡環境變數啟動本行程。
//
// Usage: node _yuanta_nuxt_extract.js < payload.js
'use strict';
const vm = require('vm');

let src = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (c) => { src += c; });
process.stdin.on('end', () => {
  const ctx = vm.createContext(Object.create(null), {
    codeGeneration: { strings: false, wasm: false },
  });
  let out;
  try {
    vm.runInContext('var window = {};', ctx, { timeout: 1000 });
    vm.runInContext(src, ctx, { timeout: 5000 });
    out = vm.runInContext(
      'window.__NUXT__ ? JSON.stringify(window.__NUXT__.data || []) : null', ctx, { timeout: 5000 });
  } catch (e) {
    console.error('EVAL_ERROR: ' + (e && e.message));
    process.exit(1);
  }
  if (typeof out !== 'string') {
    console.error('NO_NUXT_STATE');
    process.exit(1);
  }
  process.stdout.write(out);
});
