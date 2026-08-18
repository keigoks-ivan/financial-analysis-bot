initCalc('implied-growth-sim', function(values){
  var pe = values.currentPE;
  var years = values.years;
  var termMult = values.terminalMultiple;
  var r = values.requiredReturn / 100;

  if (!(termMult > 0)) termMult = 1;   // guard: avoid divide-by-zero
  if (!(years > 0)) years = 1;          // guard: avoid divide-by-zero exponent
  if (!(pe > 0)) pe = 0;

  var growthFactor = pe * Math.pow(1 + r, years) / termMult;
  if (!(growthFactor >= 0) || !isFinite(growthFactor)) growthFactor = 0; // guard: NaN/Infinity

  var cagr;
  if (growthFactor <= 0) {
    cagr = -1;
  } else {
    cagr = Math.pow(growthFactor, 1 / years) - 1;
  }
  if (!isFinite(cagr)) cagr = 0;

  return {
    growthFactor: growthFactor.toFixed(2) + 'x',
    impliedCAGR: (cagr * 100).toFixed(1) + '%'
  };
});
