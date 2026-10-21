/* 席位表欄位組切換的「記住上次選擇」（美股 /cockpit/、擂台 iframe、台股 /cockpit-tw/ 共用）。
   切換本身是純 CSS（radio ＋ :has()，見 build_arena._BOARD_CSS）；這支只負責 localStorage：
   使用者按下時存起來，看板片段被塞進頁面（innerHTML）時把存的選擇還原。
   讀寫都包 try/catch，讀不到就維持預設「時機」。 */
(function () {
  "use strict";
  var KEY = "imq-seat-view";
  var VALID = { timing: 1, fund: 1, all: 1 };
  function load() {
    try { var v = localStorage.getItem(KEY); return VALID[v] ? v : null; } catch (e) { return null; }
  }
  function save(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* 無痕或封鎖：略過 */ }
  }
  function restore() {
    var v = load();
    if (!v) return;
    var radios = document.querySelectorAll('.sv-bar input[type="radio"][value="' + v + '"]');
    for (var i = 0; i < radios.length; i++) radios[i].checked = true;
  }
  document.addEventListener("change", function (e) {
    var t = e.target;
    if (t && t.matches && t.matches('.sv-bar input[type="radio"]') && VALID[t.value]) save(t.value);
  });
  function hasBar(n) {
    return n.nodeType === 1 && (n.matches(".sv-bar") || n.querySelector(".sv-bar"));
  }
  new MutationObserver(function (ms) {
    for (var i = 0; i < ms.length; i++) {
      for (var j = 0; j < ms[i].addedNodes.length; j++) {
        if (hasBar(ms[i].addedNodes[j])) { restore(); return; }
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState !== "loading") restore();
  else document.addEventListener("DOMContentLoaded", restore);
})();
