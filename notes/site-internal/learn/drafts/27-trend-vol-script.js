initCalc('exposure-calc', function(v){
  var target = parseFloat(v.target) || 0;
  var realized = Math.max(parseFloat(v.realized) || 0, 1);
  var cap = parseFloat(v.cap) || 1.5;
  var threshold = parseFloat(v.threshold) || 20;
  var grid = parseFloat(v.grid) || 10;
  var current = parseFloat(v.current) || 0;

  var rawPP = Math.min(cap * 100, (target / realized) * 100);
  var gapPP = Math.round(rawPP) - Math.round(current);

  var finalPP;
  if (Math.abs(gapPP) < threshold) {
    finalPP = current;
  } else {
    var rounded = Math.round(rawPP / grid) * grid;
    finalPP = Math.min(Math.max(rounded, 0), cap * 100);
  }

  var leverage = finalPP / 100;
  var loss30 = leverage * -30;

  return {
    raw: rawPP.toFixed(1) + '%',
    gap: (gapPP >= 0 ? '+' : '') + gapPP.toFixed(0) + 'pp',
    final: finalPP.toFixed(0) + '%',
    leverage: leverage.toFixed(2) + '×',
    loss30: loss30.toFixed(1) + '%'
  };
});
