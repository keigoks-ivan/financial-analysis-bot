initCalc('calc-portfolio-structure', function (values) {
  var cashPct = Number(values.cashPct) || 0;
  var indexPct = Number(values.indexPct) || 0;
  var coreCount = Number(values.coreCount) || 1;
  var satCount = Number(values.satCount) || 0;
  var satCap = Number(values.satCap) || 0;

  var investable = 100 - cashPct;
  if (investable < 0) investable = 0;

  var indexSleevePct = investable * (indexPct / 100);
  var stockSleevePct = investable - indexSleevePct;

  var satTotalPct = satCount * satCap;
  var coreBudgetPct = stockSleevePct - satTotalPct;
  var coreAvgPct = coreCount > 0 ? coreBudgetPct / coreCount : 0;
  var clusterPct = 2 * satCap;

  var lang = (typeof currentLang !== 'undefined' && currentLang === 'zh') ? 'zh' : 'en';
  var warning = '';
  if (coreBudgetPct < 0) {
    warning = lang === 'zh'
      ? '核心預算為負 — 光是衛星部位就已超過個股部'
      : 'Core budget negative — satellites alone exceed the stock sleeve.';
  } else if (stockSleevePct > 0 && clusterPct > stockSleevePct * 0.3) {
    warning = lang === 'zh'
      ? '兩檔衛星同群聚會超過個股部的 30%'
      : 'A two-satellite cluster would exceed 30% of the stock sleeve.';
  } else {
    warning = lang === 'zh' ? '無' : 'None';
  }

  function fmt(n) {
    if (!isFinite(n)) return '0.0';
    return n.toFixed(1);
  }

  return {
    indexSleevePct: fmt(indexSleevePct) + '%',
    stockSleevePct: fmt(stockSleevePct) + '%',
    satTotalPct: fmt(satTotalPct) + '%',
    coreAvgPct: fmt(coreAvgPct) + '%',
    clusterPct: fmt(clusterPct) + '%',
    warning: warning
  };
});
