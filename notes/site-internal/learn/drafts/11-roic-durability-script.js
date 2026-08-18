initCalc('endogenous-growth-calc', function (values) {
  var incrRoic = values.incrRoic;
  var reinvRate = values.reinvRate;
  var consensusG = values.consensusG;

  if (
    typeof incrRoic !== 'number' || typeof reinvRate !== 'number' || typeof consensusG !== 'number' ||
    !isFinite(incrRoic) || !isFinite(reinvRate) || !isFinite(consensusG)
  ) {
    return { ceiling: 'n/a', gap: 'n/a', verdict: 'n/a' };
  }

  var ceiling = (incrRoic / 100) * (reinvRate / 100) * 100;
  var gap = consensusG - ceiling;

  var verdict;
  if (gap > 3) {
    verdict = 'Needs outside funding or a re-rating of incremental ROIC / 需要外部資金或重新評估增量 ROIC';
  } else if (gap < -3) {
    verdict = 'Ceiling exceeds consensus — check if the reinvestment opportunity is real / 天花板高於共識，檢查再投資機會是否真實';
  } else {
    verdict = 'Roughly self-funded at this reinvestment rate / 在此再投資率下大致可自我支應';
  }

  return {
    ceiling: ceiling.toFixed(1) + '%',
    gap: (gap >= 0 ? '+' : '') + gap.toFixed(1) + 'pp',
    verdict: verdict
  };
});
