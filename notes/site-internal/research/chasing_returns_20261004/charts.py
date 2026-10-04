# Minimal inline-SVG chart helpers. Colors come from CSS custom properties on the page.
import html, math
def esc(s): return html.escape(str(s), quote=True)
def nice_ticks(lo, hi, n=5):
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag: step = m * mag; break
    t0 = math.floor(lo / step) * step
    ticks = []
    v = t0
    while v <= hi + 1e-9:
        ticks.append(round(v, 6)); v += step
    while ticks[-1] < hi - 1e-9:
        ticks.append(round(ticks[-1] + step, 6))
    return ticks

def grouped_columns(cats, series, fmt=lambda v: f"{v:.1f}%", height=300, ymin=None, ymax=None, tips=None, label_all=True, aria=""):
    """cats: list of str; series: list of (name, cssvar, values). tips[s][i] -> tooltip text"""
    W = 680; H = height; ml, mr, mt, mb = 44, 12, 24, 56
    vals = [v for _, _, vs in series for v in vs if v is not None]
    lo = min(0, min(vals) * 1.3) if ymin is None else ymin
    hi = max(vals) if ymax is None else ymax
    ticks = nice_ticks(lo, hi * 1.08)
    lo, hi = min(ticks[0], lo), ticks[-1]
    pw, ph = W - ml - mr, H - mt - mb
    y = lambda v: mt + ph * (hi - v) / (hi - lo)
    band = pw / len(cats)
    ns = len(series)
    bw = min(24, (band * 0.62) / ns)
    gap = 8 if label_all else 2
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{esc(aria)}">']
    for t in ticks:
        out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="{"base" if t==0 else "grid"}"/>')
        out.append(f'<text x="{ml-6}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t:g}%</text>')
    for i, c in enumerate(cats):
        cx = ml + band * i + band / 2
        x0 = cx - (ns * bw + (ns - 1) * gap) / 2
        for s, (name, var, vs) in enumerate(series):
            v = vs[i]
            if v is None: continue
            x = x0 + s * (bw + gap)
            y0, y1 = y(max(v, 0)), y(min(v, 0))
            h = max(y1 - y0, 0.5)
            r = min(4, h)
            # rounded data-end, square at baseline
            if v >= 0:
                d = f"M{x:.1f},{y1:.1f} V{y0+r:.1f} Q{x:.1f},{y0:.1f} {x+r:.1f},{y0:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y0:.1f} {x+bw:.1f},{y0+r:.1f} V{y1:.1f} Z"
            else:
                d = f"M{x:.1f},{y0:.1f} V{y1-r:.1f} Q{x:.1f},{y1:.1f} {x+r:.1f},{y1:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y1:.1f} {x+bw:.1f},{y1-r:.1f} V{y0:.1f} Z"
            tip = tips[s][i] if tips else f"{c}｜{name}：{fmt(v)}"
            out.append(f'<path d="{d}" style="fill:var({var})" class="mark" tabindex="0" data-tip="{esc(tip)}"/>')
            if label_all:
                ly = y0 - 6 if v >= 0 else y1 + 14
                out.append(f'<text x="{x+bw/2:.1f}" y="{ly:.1f}" class="val" text-anchor="middle">{fmt(v)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{H-mb+18}" class="cat" text-anchor="middle">{esc(c)}</text>')
    out.append('</svg>')
    legend = '' if ns < 2 else '<div class="legend">' + ''.join(f'<span><i style="background:var({v})"></i>{esc(n)}</span>' for n, v, _ in series) + '</div>'
    return legend + '<div class="chart-wrap">' + ''.join(out) + '</div>'

def wrap_cat(c):
    return c

def scatter(points, xlab, ylab, xref=None, xref_label="", height=380, aria="", hl=None):
    """points: list of (x, y, tip). values in %"""
    W = 680; H = height; ml, mr, mt, mb = 48, 16, 20, 46
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    xt = nice_ticks(min(xs), max(xs + ([xref] if xref is not None else [])))
    yt = nice_ticks(min(min(ys), 0), max(ys))
    xlo, xhi, ylo, yhi = xt[0], xt[-1], yt[0], yt[-1]
    pw, ph = W - ml - mr, H - mt - mb
    X = lambda v: ml + pw * (v - xlo) / (xhi - xlo)
    Y = lambda v: mt + ph * (yhi - v) / (yhi - ylo)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{esc(aria)}">']
    for t in yt:
        out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" class="{"base" if t==0 else "grid"}"/>')
        out.append(f'<text x="{ml-6}" y="{Y(t)+4:.1f}" class="tick" text-anchor="end">{t:g}%</text>')
    for t in xt:
        out.append(f'<text x="{X(t):.1f}" y="{H-mb+16}" class="tick" text-anchor="middle">{t:g}%</text>')
    out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{H-mb}" y2="{H-mb}" class="base"/>')
    out.append(f'<text x="{ml+pw/2:.1f}" y="{H-6}" class="axl" text-anchor="middle">{esc(xlab)}</text>')
    out.append(f'<text x="12" y="{mt+ph/2:.1f}" class="axl" text-anchor="middle" transform="rotate(-90 12 {mt+ph/2:.1f})">{esc(ylab)}</text>')
    if xref is not None:
        out.append(f'<line x1="{X(xref):.1f}" x2="{X(xref):.1f}" y1="{mt}" y2="{H-mb}" class="ref"/>')
        out.append(f'<text x="{X(xref)-6:.1f}" y="{mt+12}" class="reflab" text-anchor="end">{esc(xref_label)}</text>')
    for (x, yv, tip) in points:
        cls = "dot hl" if hl and hl(x, yv, tip) else "dot"
        out.append(f'<circle cx="{X(x):.1f}" cy="{Y(yv):.1f}" r="4.5" class="{cls}" tabindex="0" data-tip="{esc(tip)}"/>')
        if cls == "dot hl":
            right = X(x) > W - mr - 44
            out.append(f'<text x="{X(x)+(-8 if right else 8):.1f}" y="{Y(yv)+4:.1f}" class="val" text-anchor="{"end" if right else "start"}">{esc(tip[:4])}</text>')
    out.append('</svg>')
    return '<div class="chart-wrap">' + ''.join(out) + '</div>'

def columns_with_ref(cats, vals, ref, ref_label, fmt=lambda v: f"{v:g}", height=260, aria="", tips=None, var="--s1", ylab_suffix=""):
    W = 680; H = height; ml, mr, mt, mb = 40, 12, 22, 40
    lo0 = min(0, min(vals) * 1.35); hi0 = max(max(vals), ref)
    ticks = nice_ticks(lo0, hi0 * 1.1); lo, hi = ticks[0], ticks[-1]
    pw, ph = W - ml - mr, H - mt - mb
    y = lambda v: mt + ph * (hi - v) / (hi - lo)
    band = pw / len(cats); bw = min(24, band * 0.6)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{esc(aria)}">']
    for t in ticks:
        out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="{"base" if t==0 else "grid"}"/>')
        out.append(f'<text x="{ml-6}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t:g}{ylab_suffix}</text>')
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = ml + band * i + band / 2; x = cx - bw / 2
        y0, y1 = y(max(v, 0)), y(min(v, 0)); r = min(4, max(y1 - y0, 0))
        if v >= 0:
            d = f"M{x:.1f},{y1:.1f} V{y0+r:.1f} Q{x:.1f},{y0:.1f} {x+r:.1f},{y0:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y0:.1f} {x+bw:.1f},{y0+r:.1f} V{y1:.1f} Z"
            ly = y0 - 6
        else:
            d = f"M{x:.1f},{y0:.1f} V{y1-r:.1f} Q{x:.1f},{y1:.1f} {x+r:.1f},{y1:.1f} H{x+bw-r:.1f} Q{x+bw:.1f},{y1:.1f} {x+bw:.1f},{y1-r:.1f} V{y0:.1f} Z"
            ly = y1 + 14
        tip = tips[i] if tips else f"{c}：{fmt(v)}"
        out.append(f'<path d="{d}" style="fill:var({var})" class="mark" tabindex="0" data-tip="{esc(tip)}"/>')
        out.append(f'<text x="{cx:.1f}" y="{ly:.1f}" class="val" text-anchor="middle">{fmt(v)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{H-mb+18}" class="cat" text-anchor="middle">{esc(c)}</text>')
    out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y(ref):.1f}" y2="{y(ref):.1f}" class="ref"/>')
    if ref_label:
        out.append(f'<text x="{W-mr}" y="{y(ref)-6:.1f}" class="reflab" text-anchor="end">{esc(ref_label)}</text>')
    out.append('</svg>')
    return '<div class="chart-wrap">' + ''.join(out) + '</div>'

def lines(xs, series, height=300, aria="", fmt=lambda v: f"{v:.2f}", ylab="", xfmt=lambda x: f"{x} 年底", mr_=180):
    """series: list of (name, cssvar, values). x = years. end labels + hover per point."""
    W = 680; H = height; ml, mr, mt, mb = 44, mr_, 18, 32
    vals = [v for _, _, vs in series for v in vs]
    ticks = nice_ticks(min(0, min(vals)), max(vals))
    lo, hi = ticks[0], ticks[-1]
    pw, ph = W - ml - mr, H - mt - mb
    X = lambda i: ml + pw * (xs[i] - xs[0]) / (xs[-1] - xs[0])
    Y = lambda v: mt + ph * (hi - v) / (hi - lo)
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="{esc(aria)}">']
    for t in ticks:
        out.append(f'<line x1="{ml}" x2="{W-mr}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" class="{"base" if (t==0 or (lo>0 and t==lo)) else "grid"}"/>')
        out.append(f'<text x="{ml-6}" y="{Y(t)+4:.1f}" class="tick" text-anchor="end">{t:g}{ylab}</text>')
    step = max(1, len(xs) // 6)
    for i in range(0, len(xs), step):
        out.append(f'<text x="{X(i):.1f}" y="{H-mb+18}" class="tick" text-anchor="middle">{xs[i]}</text>')
    ends = []
    for name, var, vs in series:
        d = " ".join(f"{'M' if i==0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vs))
        out.append(f'<path d="{d}" class="line" style="stroke:var({var})"/>')
        ends.append((Y(vs[-1]), name, var, vs[-1]))
    # hover columns
    for i, x in enumerate(xs):
        tip = f"{xfmt(x)}｜" + "｜".join(f"{n}：{fmt(vs[i])}" for n, _, vs in series)
        x0 = X(i) - pw / (len(xs) - 1) / 2
        out.append(f'<rect x="{max(x0,ml):.1f}" y="{mt}" width="{pw/(len(xs)-1):.1f}" height="{ph}" class="hit" tabindex="-1" data-tip="{esc(tip)}"/>')
    ends.sort()
    last = -99
    for yv, name, var, v in ends:
        yy = max(yv, last + 16); last = yy
        out.append(f'<circle cx="{X(len(xs)-1):.1f}" cy="{yv:.1f}" r="4.5" class="enddot" style="fill:var({var})"/>')
        out.append(f'<text x="{X(len(xs)-1)+10:.1f}" y="{yy+4:.1f}" class="val" text-anchor="start">{esc(name)} {fmt(v)}</text>')
    out.append('</svg>')
    legend = '<div class="legend">' + ''.join(f'<span><i style="background:var({v})"></i>{esc(n)}</span>' for n, v, _ in series) + '</div>'
    return legend + '<div class="chart-wrap">' + ''.join(out) + '</div>'
