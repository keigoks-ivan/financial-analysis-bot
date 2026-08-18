initCalc('regulated-return-calc', function(values){
  var rateBase = Number(values.rateBase);
  var allowedRoe = Number(values.allowedRoe);
  var equityRatio = Number(values.equityRatio);
  var treasuryYield = Number(values.treasuryYield);
  var growthRate = Number(values.growthRate);

  if (isNaN(rateBase)) rateBase = 50;
  if (isNaN(allowedRoe)) allowedRoe = 10.6;
  if (isNaN(equityRatio)) equityRatio = 59.6;
  if (isNaN(treasuryYield)) treasuryYield = 1.5;
  if (isNaN(growthRate)) growthRate = 7;

  var regEarnings = rateBase * (equityRatio / 100) * (allowedRoe / 100);

  var equityRiskPremium = 4.5;
  var discountRate = treasuryYield + equityRiskPremium;

  var gap = discountRate - growthRate;
  var fairPeText;
  if (gap <= 0.1) {
    fairPeText = 'not meaningful ・ 無意義（growth ≥ discount rate）';
  } else {
    var fairPe = 100 / gap;
    if (!isFinite(fairPe) || isNaN(fairPe)) {
      fairPeText = 'not meaningful ・ 無意義';
    } else {
      fairPeText = fairPe.toFixed(1) + 'x';
    }
  }

  return {
    regEarnings: '$' + regEarnings.toFixed(2) + 'B',
    discountRate: discountRate.toFixed(1) + '%',
    fairPe: fairPeText
  };
});
