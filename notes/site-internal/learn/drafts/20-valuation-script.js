initCalc('scenario-tree-sim', function(values){
  var startPE = values.startPe;
  if (startPE < 5) startPE = 5;

  function irr5(cagrPct, peEnd) {
    var mult = Math.pow(1 + cagrPct/100, 5);
    var ret5y = mult * (peEnd/startPE) - 1;
    var base = 1 + ret5y;
    if (base < 0) base = 0; // floor: this toy model does not model a total wipeout path
    return { ret5y: ret5y, irr: Math.pow(base, 1/5) - 1 };
  }

  var base = irr5(values.baseCagr, startPE); // Base case: terminal multiple held flat at startPE
  var bull = irr5(values.bullCagr, values.bullPe);
  var bear = irr5(values.bearCagr, values.bearPe);

  // Multiple-change contribution to the Bull case, annualized
  var multAnn = Math.pow(values.bullPe/startPE, 1/5) - 1;
  var multContribPct = 0;
  if (bull.irr > 0.0001) {
    multContribPct = (multAnn / bull.irr) * 100;
    if (multContribPct < 0) multContribPct = 0;
    if (multContribPct > 100) multContribPct = 100;
  }

  var bullMag = Math.abs(bull.ret5y);
  var bearMag = Math.abs(bear.ret5y);
  var probBull = values.probBull/100;
  var probBear = values.probBear/100;

  var ar;
  if (bearMag < 0.001 || probBear <= 0) {
    ar = 99; // denominator effectively zero: display as an off-the-chart illusion, not Infinity
  } else {
    ar = (probBull * bullMag) / (probBear * bearMag);
    if (ar > 99) ar = 99;
  }

  return {
    baseIRR: (base.irr*100).toFixed(1) + '%',
    bullIRR: (bull.irr*100).toFixed(1) + '%',
    bearIRR: (bear.irr*100).toFixed(1) + '%',
    multContrib: multContribPct.toFixed(0) + '%',
    ar: ar.toFixed(1) + '×'
  };
});
