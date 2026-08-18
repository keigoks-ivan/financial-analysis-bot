initCalc('calc-dupont', function (v) {
  var margin = parseFloat(v.margin);
  var turnover = parseFloat(v.turnover);
  var leverage = parseFloat(v.leverage);
  var roe = (margin / 100) * turnover * leverage * 100;
  return { roe: roe.toFixed(1) + '%' };
});
