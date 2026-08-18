initCalc('growth-value-calc', function(v){
  var g = (v.g || 0) / 100;
  var roic = (v.roic || 0) / 100;
  var wacc = (v.wacc || 6) / 100;
  if (wacc <= 0) wacc = 0.06;
  var years = v.years || 5;
  var spread = roic - wacc;
  var ratio = spread / wacc;
  var term = 1 + g * ratio;
  if (term < 0.01) term = 0.01;
  var multiple = Math.pow(term, years);
  var annualized = (Math.pow(multiple, 1 / years) - 1) * 100;
  return {
    multiple: multiple.toFixed(2) + '×',
    annualized: annualized.toFixed(1) + '%'
  };
});
