initCalc('cyclical-position-calc', function(values){
  var sig1 = Number(values.sig1);
  var sig2 = Number(values.sig2);
  var sig3 = Number(values.sig3);
  var sig4 = Number(values.sig4);
  var sig5 = Number(values.sig5);
  var sig6 = Number(values.sig6);
  var score = sig1 + sig2 + sig3 + sig4 + sig5 + sig6;
  if (isNaN(score)) score = 0;

  var stage;
  if (score <= 2) {
    stage = 'Deep Trough ・ 深度谷底';
  } else if (score <= 4) {
    stage = 'Early Cycle ・ 早期循環';
  } else if (score <= 7) {
    stage = 'Mid Cycle ・ 循環中段';
  } else if (score <= 9) {
    stage = 'Late Cycle ・ 晚期循環';
  } else {
    stage = 'Overheating Peak ・ 過熱頂部';
  }

  return {
    score: score.toFixed(0) + ' / 12',
    stage: stage
  };
});
