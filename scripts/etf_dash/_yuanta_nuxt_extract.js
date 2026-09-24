// Evaluate a Yuanta Nuxt.js SSR "window.__NUXT__=(function(a,b,...){...})(v1,v2,...)"
// payload (extracted verbatim from the 0050 fund detail page's HTML by
// build_etf_dash.py::parse_yuanta_0050_holdings — see the comment block
// above fetch_yuanta_holdings_page() in that file for why this is needed)
// and print its `.data` array as JSON on stdout.
//
// This is static data assignment, not page rendering: no network access, no
// DOM/browser APIs are used or required. Called as a short-lived subprocess
// from build_etf_dash.py, never as a standalone script against untrusted
// input beyond what that one caller writes to the temp file it passes in.
//
// Usage: node _yuanta_nuxt_extract.js <path-to-payload.js>
'use strict';
const fs = require('fs');

const payloadPath = process.argv[2];
if (!payloadPath) {
  console.error('usage: node _yuanta_nuxt_extract.js <payload.js>');
  process.exit(1);
}

const src = fs.readFileSync(payloadPath, 'utf-8');
global.window = {};
try {
  // eslint-disable-next-line no-eval
  eval(src);
} catch (e) {
  console.error('EVAL_ERROR: ' + (e && e.message));
  process.exit(1);
}
if (!global.window.__NUXT__) {
  console.error('NO_NUXT_STATE');
  process.exit(1);
}
process.stdout.write(JSON.stringify(global.window.__NUXT__.data || []));
