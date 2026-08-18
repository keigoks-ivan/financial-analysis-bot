initCalc('pricing-power-calc', function(v){
  var P0 = 100, C0 = 60; // baseline illustrative units: price 100, cost 60 -> 40% gross margin
  var costUpPct = v.costUp || 0;
  var passthroughPct = v.passthrough || 0;
  var elasticity = v.elasticity || 0;

  var deltaC = C0 * (costUpPct / 100);
  var deltaP = deltaC * (passthroughPct / 100);
  var P1 = P0 + deltaP;
  var C1 = C0 + deltaC;

  var priceChangePct = P0 > 0 ? (deltaP / P0) * 100 : 0;
  var volChangePct = -elasticity * priceChangePct;
  var Q1 = Math.max(0, 1 + (volChangePct / 100));

  var rev0 = P0 * 1;
  var rev1 = P1 * Q1;
  var revChangePct = rev0 > 0 ? ((rev1 - rev0) / rev0) * 100 : 0;

  var gm0 = P0 > 0 ? ((P0 - C0) / P0) * 100 : 0;
  var gm1 = P1 > 0 ? ((P1 - C1) / P1) * 100 : 0;

  function fmt1(n){ return (isFinite(n) ? n.toFixed(1) : '0.0'); }

  return {
    gmSummary: fmt1(gm0) + '% → ' + fmt1(gm1) + '%',
    volChange: (volChangePct >= 0 ? '+' : '') + fmt1(volChangePct) + '%',
    revChange: (revChangePct >= 0 ? '+' : '') + fmt1(revChangePct) + '%'
  };
});
