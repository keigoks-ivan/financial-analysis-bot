initCalc('cycle-gauge-calc', function(values){
  var inv = Number(values.inv);
  var capex = Number(values.capex);
  var price = Number(values.price);
  if (isNaN(inv)) inv = 8;
  if (isNaN(capex)) capex = 1.5;
  if (isNaN(price)) price = 0;

  var invPt;
  if (inv <= 6) { invPt = 1; }
  else if (inv >= 12) { invPt = -1; }
  else { invPt = 0; }

  var capexPt;
  if (capex >= 1.8) { capexPt = 1; }
  else if (capex < 1.0) { capexPt = -1; }
  else { capexPt = 0; }

  var pricePt;
  if (price >= 20) { pricePt = 1; }
  else if (price <= -20) { pricePt = -1; }
  else { pricePt = 0; }

  var sum = invPt + capexPt + pricePt;
  if (isNaN(sum)) sum = 0;
  var display = sum + 3;

  var stage;
  if (display <= 1) {
    stage = 'Deep Trough ・ 深度谷底';
  } else if (display === 2) {
    stage = 'Mixed, Leaning Trough ・ 混合，偏谷底';
  } else if (display === 3) {
    stage = 'Mixed ・ 混合訊號';
  } else if (display === 4) {
    stage = 'Mixed, Leaning Peak ・ 混合，偏頂部';
  } else {
    stage = 'Peak Danger Zone ・ 頂部風險區';
  }

  return {
    score: display.toFixed(0) + ' / 6',
    stage: stage
  };
});
