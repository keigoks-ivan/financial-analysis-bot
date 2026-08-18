initCalc('calc-opleverage', function (v) {
  var rev = v.rev || 32;
  var growth = v.growth || 18;
  var margin = v.margin || 20;
  var fixed = v.fixed || 7;

  var marginFrac = margin / 100;
  var growthFrac = growth / 100;

  var breakeven;
  if (marginFrac > 0) {
    breakeven = fixed / marginFrac;
  } else {
    breakeven = Infinity;
  }

  var years;
  if (!isFinite(breakeven)) {
    years = Infinity;
  } else if (rev >= breakeven) {
    years = 0;
  } else if (growthFrac <= 0) {
    years = Infinity;
  } else {
    years = Math.log(breakeven / rev) / Math.log(1 + growthFrac);
    if (!isFinite(years) || years < 0) years = Infinity;
  }

  var breakevenStr = isFinite(breakeven) ? ('$' + breakeven.toFixed(1) + 'B') : 'n/a';
  var yearsStr;
  if (!isFinite(years)) {
    yearsStr = '10+ yrs';
  } else if (years <= 0) {
    yearsStr = 'already there';
  } else {
    yearsStr = years.toFixed(1) + ' yrs';
  }

  return {
    breakeven: breakevenStr,
    years: yearsStr
  };
});
