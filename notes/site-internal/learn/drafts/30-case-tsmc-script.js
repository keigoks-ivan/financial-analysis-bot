initCalc('pe-calc', function(v){
  var tr = (v.tr || 0) / 100;
  var div = (v.div || 0) / 100;
  var pe0 = v.pe0 || 1;
  var pe5 = v.pe5 || 1;
  var n = 5;
  var ratio = pe5 / pe0;
  var factor = Math.pow(ratio, 1 / n);
  var g = ((1 + tr - div) / factor - 1) * 100;
  return {
    impliedg: g.toFixed(1) + '%'
  };
});
