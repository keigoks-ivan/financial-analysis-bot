initCalc('capital-cycle-sim', function(values){
  var spread = values.currentSpread;
  var capexG = values.capexGrowth;
  var demG = values.demandGrowth;
  var lead = values.leadTime;

  var gap = capexG - demG;      // pp/yr excess capacity growth chasing the return
  if (gap < 0) gap = 0;         // capacity growth below demand growth: no glut building in this toy model

  var overbuild = gap * lead;   // cumulative % overbuild by the time the committed capacity lands
  var decay = 0.9;              // illustrative: pp of spread compression per 1% cumulative overbuild

  var troughSpread = spread - overbuild * decay;
  if (troughSpread < -25) troughSpread = -25; // floor: model does not try to depict distress beyond this

  var recoveryRate = 6; // fixed constant (% overbuild absorbed per year via demand catch-up + capacity exit)
  var reversionYears = overbuild / recoveryRate;
  if (reversionYears < 0.5) reversionYears = 0.5;
  if (reversionYears > 8) reversionYears = 8;

  var troughStr = (troughSpread >= 0 ? '+' : '') + troughSpread.toFixed(1) + 'pp';

  return {
    overbuild: overbuild.toFixed(0) + '%',
    troughSpread: troughStr,
    reversionYears: reversionYears.toFixed(1)
  };
});
