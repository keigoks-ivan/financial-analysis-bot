initCalc('calc-tam-chain', function(values){
  var upstream = values.upstream || 0;
  var share = (values.share || 0) / 100;
  var attach = values.attach || 0;
  var current = values.current > 0 ? values.current : 1;
  var base = upstream * share * attach;
  var bear = base * 0.75;
  var bull = base * 1.2;
  var multiple = base / current;
  return {
    bear_tam: '$' + bear.toFixed(0) + 'B',
    base_tam: '$' + base.toFixed(0) + 'B',
    bull_tam: '$' + bull.toFixed(0) + 'B',
    multiple: multiple.toFixed(2) + 'x'
  };
});
