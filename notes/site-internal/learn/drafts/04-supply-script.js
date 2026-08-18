initCalc('supply-gap-calc', function(values){
  var g = values.demand / 100;
  var lead = Math.round(values.lead);
  var capG = values.capgrowth / 100;
  var util0 = values.util;
  var n = 7;
  var D = 100, C = 100;
  var utilArr = [];
  for (var t = 0; t < n; t++) {
    if (t > 0) {
      D = D * (1 + g);
      if (t > lead) { C = C * (1 + capG); }
    }
    utilArr.push(util0 * (D / C));
  }
  var peak = 0;
  for (var i = 0; i < utilArr.length; i++) { if (utilArr[i] > peak) peak = utilArr[i]; }
  var gapYears = 0;
  for (var i = 0; i < utilArr.length; i++) { if (utilArr[i] > 95) gapYears++; }
  var blocks = '▁▂▃▄▅▆▇█';
  var spark = '';
  for (var i = 0; i < utilArr.length; i++) {
    var idx = Math.round((utilArr[i] - 60) / 6);
    if (idx < 0) idx = 0;
    if (idx > blocks.length - 1) idx = blocks.length - 1;
    if (!isFinite(idx)) idx = 0;
    spark += blocks[idx];
  }
  var peakStr = isFinite(peak) ? Math.round(peak) + '%' : '--';
  return { peakUtil: peakStr, gapYears: gapYears + ' / ' + n, sparkline: spark };
});
