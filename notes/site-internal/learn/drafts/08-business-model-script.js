initCalc('calc-oplev', function(v){
  var fixedCost = v.fixedCost || 0;
  var varRate = (v.varRate || 0) / 100;
  var baseRev = v.baseRev || 0;
  var revChangePct = v.revChange || 0;

  var baseGP = baseRev * (1 - varRate);
  var baseOI = baseGP - fixedCost;
  var newRev = baseRev * (1 + revChangePct / 100);
  var newGP = newRev * (1 - varRate);
  var newOI = newGP - fixedCost;

  var oiChangeStr, dolStr;
  if (Math.abs(baseOI) < 1e-6 || revChangePct === 0) {
    oiChangeStr = '—';
    dolStr = '—';
  } else {
    var oiChangePct = ((newOI - baseOI) / Math.abs(baseOI)) * 100;
    oiChangeStr = (oiChangePct >= 0 ? '+' : '') + oiChangePct.toFixed(1) + '%';
    var dol = oiChangePct / revChangePct;
    dolStr = dol.toFixed(2) + 'x';
  }

  return {
    newOI: '$' + newOI.toFixed(1) + 'M',
    oiChangePct: oiChangeStr,
    dol: dolStr
  };
});
