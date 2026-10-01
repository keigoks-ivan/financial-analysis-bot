"""Shared section builders for /backtest/ system pages (hero-stats family).

Standard sections added 2026-06-12, inspired by the slope_filter page:
    月報酬分布     section_monthly_dist()   — histogram of monthly returns
    滾動 12 月報酬 section_rolling12()      — rolling 12-month return line
    曝險時間軸     section_exposure()       — net exposure over time (stepped)

Each builder returns a dict {"html": ..., "js": ...}; generators insert the
html inside <div class="container"> (typically right after the NAV/DD charts)
and append the js inside the page's <script> block.  Canvas ids are fixed
(chart-mdist / chart-roll12 / chart-expo) — one of each per page.

Series are passed as (label, color, equity_series) tuples; the first entry is
the system line, later entries are comparison lines.  All computation is
monthly-resampled so the embedded JSON stays small.
"""
from __future__ import annotations
import json

import numpy as np
import pandas as pd

# fixed histogram bin edges (%, monthly returns); outliers clamp to end bins
DIST_EDGES = list(range(-12, 13, 2))


def monthly_returns(eq: pd.Series) -> pd.Series:
    m = eq.resample("ME").last()
    return (m.pct_change().dropna() * 100).round(3)


def _dist_counts(eq: pd.Series) -> list[int]:
    r = monthly_returns(eq).clip(DIST_EDGES[0] + 1e-9, DIST_EDGES[-1] - 1e-9)
    counts, _ = np.histogram(r, bins=DIST_EDGES)
    return [int(c) for c in counts]


def section_monthly_dist(series: list[tuple[str, str, pd.Series]],
                         note: str = "") -> dict:
    labels = [f"{DIST_EDGES[i]}~{DIST_EDGES[i+1]}%" for i in range(len(DIST_EDGES) - 1)]
    datasets = []
    for i, (label, color, eq) in enumerate(series):
        datasets.append({
            "label": label, "data": _dist_counts(eq),
            "backgroundColor": color + ("cc" if i == 0 else "55"),
            "borderColor": color, "borderWidth": 1, "borderRadius": 2,
        })
    stats_rows = ""
    for label, _, eq in series:
        r = monthly_returns(eq)
        pos = float((r > 0).mean() * 100)
        stats_rows += (f"<tr><td>{label}</td><td>{r.mean():+.2f}%</td>"
                       f"<td>{r.median():+.2f}%</td><td>{pos:.1f}%</td>"
                       f"<td style=\"color:var(--red)\">{r.min():+.2f}%</td>"
                       f"<td style=\"color:var(--green)\">{r.max():+.2f}%</td></tr>")
    html = f"""
<div class="section">
<h2 class="section-title">月報酬分布</h2>
<div class="chart-card">
  <div class="chart-wrap-sm"><canvas id="chart-mdist"></canvas></div>
</div>
<div class="card">
<table>
<thead><tr><th>序列</th><th>月均</th><th>月中位</th><th>正月比例</th><th>最差月</th><th>最佳月</th></tr></thead>
<tbody>{stats_rows}</tbody>
</table>
{f'<div class="takeaway">{note}</div>' if note else ''}
</div>
</div>
"""
    js = f"""
new Chart(document.getElementById('chart-mdist'),{{
  type:'bar',
  data:{{labels:{json.dumps(labels)},datasets:{json.dumps(datasets)}}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'rect',padding:14}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y+' 個月'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{font:{{size:9}}}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{font:{{size:10}}}},title:{{display:true,text:'月數',font:{{size:10}}}}}}}}
  }}
}});
"""
    return {"html": html, "js": js}


def rolling12(eq: pd.Series) -> tuple[list, list]:
    m = eq.resample("ME").last()
    r = (m.pct_change(12).dropna() * 100).round(2)
    return [str(k.date())[:7] for k in r.index], [float(v) for v in r.values]


def section_rolling12(series: list[tuple[str, str, pd.Series]],
                      note: str = "") -> dict:
    labels, _ = rolling12(series[0][2])
    datasets = []
    for i, (label, color, eq) in enumerate(series):
        lb, vals = rolling12(eq)
        # align on the first series' label axis
        d = dict(zip(lb, vals))
        datasets.append({
            "label": label, "data": [d.get(k) for k in labels],
            "borderColor": color, "borderWidth": 2.2 if i == 0 else 1.3,
            "pointRadius": 0, "pointHoverRadius": 3, "tension": 0.1,
            **({"borderDash": [6, 3]} if i > 0 else {}),
        })
    html = f"""
<div class="section">
<h2 class="section-title">滾動 12 月報酬</h2>
<div class="section-sub">任一時點往回看 12 個月的報酬；低於 0 的區段 = 持有一年仍虧損的進場時點。</div>
<div class="chart-card">
  <div class="chart-wrap-sm"><canvas id="chart-roll12"></canvas></div>
</div>
{f'<div class="card"><div class="takeaway" style="margin-top:0">{note}</div></div>' if note else ''}
</div>
"""
    js = f"""
new Chart(document.getElementById('chart-roll12'),{{
  type:'line',
  data:{{labels:{json.dumps(labels)},datasets:{json.dumps(datasets)}}},
  options:{{responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.parsed.y==null?null:c.dataset.label+': '+(c.parsed.y>0?'+':'')+c.parsed.y.toFixed(2)+'%'}}}}}}}},
    scales:{{x:{{grid:{{color:'rgba(0,0,0,0.04)'}},ticks:{{maxTicksLimit:21,font:{{size:10}}}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});
"""
    return {"html": html, "js": js}


def exposure_monthly(pos_daily: pd.Series) -> tuple[list, list]:
    m = pos_daily.resample("ME").last().dropna()
    return [str(k.date())[:7] for k in m.index], [round(float(v), 3) for v in m.values]


def section_exposure(series: list[tuple[str, str, pd.Series]],
                     note: str = "",
                     title: str = "曝險時間軸",
                     sub: str = "月底淨曝險(+1 = 滿倉做多，0 = 空手，-1 = 滿倉做空)。") -> dict:
    labels, _ = exposure_monthly(series[0][2])
    datasets = []
    for i, (label, color, pos) in enumerate(series):
        lb, vals = exposure_monthly(pos)
        d = dict(zip(lb, vals))
        datasets.append({
            "label": label, "data": [d.get(k) for k in labels],
            "borderColor": color, "backgroundColor": color + "22",
            "borderWidth": 1.5 if i == 0 else 1.1, "pointRadius": 0,
            "stepped": True, "fill": "origin" if i == 0 else False,
        })
    html = f"""
<div class="section">
<h2 class="section-title">{title}</h2>
<div class="section-sub">{sub}</div>
<div class="chart-card">
  <div class="chart-wrap-sm"><canvas id="chart-expo"></canvas></div>
</div>
{f'<div class="card"><div class="takeaway" style="margin-top:0">{note}</div></div>' if note else ''}
</div>
"""
    js = f"""
new Chart(document.getElementById('chart-expo'),{{
  type:'line',
  data:{{labels:{json.dumps(labels)},datasets:{json.dumps(datasets)}}},
  options:{{responsive:true,maintainAspectRatio:false,
    interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.parsed.y==null?null:c.dataset.label+': '+c.parsed.y.toFixed(2)}}}}}}}},
    scales:{{x:{{grid:{{color:'rgba(0,0,0,0.04)'}},ticks:{{maxTicksLimit:21,font:{{size:10}}}}}},
      y:{{min:-1.15,max:1.15,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{font:{{size:10}}}}}}}}
  }}
}});
"""
    return {"html": html, "js": js}
