initCalc('dividend-breakeven-calc', function(values){
  var price = Number(values.price);
  var prod = Number(values.prod);
  var cost = Number(values.cost);
  var capex = Number(values.capex);
  var div = Number(values.div);

  if (isNaN(price)) price = 35;
  if (isNaN(prod) || prod <= 0) prod = 3.7;
  if (isNaN(cost)) cost = 20;
  if (isNaN(capex)) capex = 23;
  if (isNaN(div) || div <= 0) div = 14.9;

  // Annual production volume in billion barrels of oil equivalent.
  var annualVolumeB = (prod * 365) / 1000;
  if (annualVolumeB <= 0) annualVolumeB = 0.001;

  // Free cash flow after capex, in $ billion:
  // (price - cash cost) x annual volume (billion boe) - capex.
  var fcf = (price - cost) * annualVolumeB - capex;

  var coverage = fcf / div;

  // Oil price needed so that FCF exactly equals capex + dividend.
  var breakeven = cost + (capex + div) / annualVolumeB;

  var fcfStr = (fcf >= 0 ? '+' : '') + fcf.toFixed(1) + 'B';
  var coverageStr = isFinite(coverage) ? coverage.toFixed(2) + 'x' : 'n/a';
  var breakevenStr = isFinite(breakeven) ? '$' + breakeven.toFixed(0) : 'n/a';

  return {
    fcf: fcfStr,
    coverage: coverageStr,
    breakeven: breakevenStr
  };
});
