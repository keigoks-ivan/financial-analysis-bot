initCalc('runway-calc', function(v) {
  var cash = v.cash;
  var burn0 = v.burn;
  var growth = v.growth / 100;
  var margin = v.margin / 100;

  if (burn0 <= 0) {
    return { runway: 'n/a', breakeven: '0.0' };
  }

  var monthlyStep = burn0 * (growth * margin) / 12;
  var maxMonths = 600;

  var remainingCash = cash;
  var burn = burn0;
  var runwayMonths = null;
  var breakevenMonths = null;

  for (var m = 1; m <= maxMonths; m++) {
    burn = Math.max(0, burn0 - monthlyStep * (m - 1));
    if (runwayMonths === null) {
      remainingCash -= burn;
      if (remainingCash <= 0) {
        runwayMonths = m;
      }
    }
    if (breakevenMonths === null && burn <= 0) {
      breakevenMonths = m;
    }
    if (runwayMonths !== null && breakevenMonths !== null) {
      break;
    }
  }

  var runwayOut = runwayMonths === null ? (maxMonths + '+') : String(runwayMonths);
  var breakevenOut;
  if (breakevenMonths === null) {
    breakevenOut = (maxMonths / 12).toFixed(1) + '+';
  } else {
    breakevenOut = (breakevenMonths / 12).toFixed(1);
  }

  return {
    runway: runwayOut,
    breakeven: breakevenOut
  };
});
