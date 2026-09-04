initCalc('zoom-reverse-calc', function(values){
  var marketCap = Number(values.marketCap);
  var currentRevenue = Number(values.currentRevenue);
  var terminalMargin = Number(values.terminalMargin);
  var terminalPE = Number(values.terminalPE);
  var years = Number(values.years);

  if (isNaN(marketCap) || marketCap <= 0) marketCap = 150;
  if (isNaN(currentRevenue) || currentRevenue <= 0) currentRevenue = 2.4;
  if (isNaN(terminalMargin) || terminalMargin <= 0) terminalMargin = 25;
  if (isNaN(terminalPE) || terminalPE <= 0) terminalPE = 25;
  if (isNaN(years) || years <= 0) years = 10;

  var terminalIncome = marketCap / terminalPE;
  var terminalRevenue = terminalIncome / (terminalMargin / 100);
  var ratio = terminalRevenue / currentRevenue;

  var cagrText;
  if (!isFinite(ratio) || ratio <= 0) {
    cagrText = 'not meaningful ・ 無意義';
  } else {
    var cagr = Math.pow(ratio, 1 / years) - 1;
    if (!isFinite(cagr) || isNaN(cagr)) {
      cagrText = 'not meaningful ・ 無意義';
    } else {
      cagrText = (cagr * 100).toFixed(1) + '%';
    }
  }

  return {
    terminalIncome: '$' + terminalIncome.toFixed(1) + 'B',
    terminalRevenue: '$' + terminalRevenue.toFixed(1) + 'B',
    requiredCagr: cagrText
  };
});
