function fmtMoney(n) {
  if (!isFinite(n)) return '0.0';
  return n.toFixed(1);
}
function fmtPct(n) {
  if (!isFinite(n)) return '0.0';
  return n.toFixed(1);
}

initCalc('calc-fee-gap', function (values) {
  var startAmt = Number(values.startAmt) || 0;
  var annualReturn = Number(values.annualReturn) || 0;
  var years = Number(values.years) || 0;
  var feePP = Number(values.feePP) || 0;
  var gapPP = Number(values.gapPP) || 0;

  var grossRate = annualReturn / 100;
  var feeRate = (annualReturn - feePP) / 100;
  var gapRate = (annualReturn - feePP - gapPP) / 100;

  // Guard: a compounding base at or below -100% (rate <= -1) would go to zero or negative;
  // clamp the base at 0 so it never goes negative or produces NaN at extreme slider values.
  function grow(amt, rate, yrs) {
    var base = 1 + rate;
    if (base < 0) base = 0;
    var fv = amt * Math.pow(base, yrs);
    if (!isFinite(fv) || fv < 0) fv = 0;
    return fv;
  }

  var grossFV = grow(startAmt, grossRate, years);
  var feeFV = grow(startAmt, feeRate, years);
  var gapFV = grow(startAmt, gapRate, years);

  var shortfallPct = grossFV > 0 ? ((grossFV - gapFV) / grossFV) * 100 : 0;
  if (!isFinite(shortfallPct)) shortfallPct = 0;
  if (shortfallPct > 100) shortfallPct = 100;
  if (shortfallPct < 0) shortfallPct = 0;

  return {
    grossFV: fmtMoney(grossFV),
    feeFV: fmtMoney(feeFV),
    gapFV: fmtMoney(gapFV),
    shortfallPct: fmtPct(shortfallPct) + '%'
  };
});

initCalc('calc-diversification', function (values) {
  var stockSigma = Number(values.stockSigma) || 0;
  var bondSigma = Number(values.bondSigma) || 0;
  var stockWeight = Number(values.stockWeight);
  if (!isFinite(stockWeight)) stockWeight = 0;
  var corrRaw = Number(values.corr);
  if (!isFinite(corrRaw)) corrRaw = 0;

  var w1 = stockWeight / 100;
  var w2 = 1 - w1;
  var s1 = stockSigma / 100;
  var s2 = bondSigma / 100;

  function portfolioSigma(rho) {
    var variance = (w1 * w1 * s1 * s1) + (w2 * w2 * s2 * s2) + (2 * w1 * w2 * rho * s1 * s2);
    if (variance < 0) variance = 0; // guard against floating-point underflow at extreme correlation inputs
    var sigma = Math.sqrt(variance) * 100;
    if (!isFinite(sigma)) sigma = 0;
    return sigma;
  }

  var corr = corrRaw / 100;
  if (corr < -1) corr = -1;
  if (corr > 1) corr = 1;

  var sigmaP = portfolioSigma(corr);
  var sigmaNeg = portfolioSigma(-0.3);
  var sigmaZero = portfolioSigma(0);
  var sigmaPos = portfolioSigma(0.7);

  return {
    sigmaP: fmtPct(sigmaP) + '%',
    sigmaNeg: fmtPct(sigmaNeg) + '%',
    sigmaZero: fmtPct(sigmaZero) + '%',
    sigmaPos: fmtPct(sigmaPos) + '%'
  };
});
