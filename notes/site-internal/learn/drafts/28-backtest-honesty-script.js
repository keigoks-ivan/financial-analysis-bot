initCalc('mc-calc', function(v){
  var n = v.n || 1;
  var p = (v.p || 0) / 100;
  var probLuckyEach = 1 - p;
  var probNoneLucky = Math.pow(probLuckyEach, n);
  var probAtLeastOne = 1 - probNoneLucky;
  var pct = probAtLeastOne * 100;
  if (pct < 0) pct = 0;
  if (pct > 100) pct = 100;
  return {
    prob: pct.toFixed(1) + '%'
  };
});
