initCalc('roic-calc', function(v){
  var margin = (v.margin || 0) / 100;
  var turnover = v.turnover || 0;
  var roic = margin * turnover * 100;
  return {
    roic: roic.toFixed(1) + '%'
  };
});

initCalc('fcf-calc', function(v){
  var ni = v.ni || 0;
  var da = v.da || 0;
  var capex = v.capex || 0;
  var dwc = v.dwc || 0;
  var cfo = ni + da - dwc;
  var fcf = cfo - capex;
  var ratio = ni !== 0 ? (fcf / ni) * 100 : 0;
  return {
    fcf: '$' + fcf.toFixed(0) + 'M',
    ratio: ratio.toFixed(0) + '%'
  };
});
