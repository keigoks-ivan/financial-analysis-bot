"""Placeholder layer for the merged page: every table / chart / data block as its own key.

Reads frags_v2.json, frags_f.json, frags_tw.json (built earlier by run_all.sh) and the
hard-coded data markup in page_v2.py / page_f.py, writes frags_merged.json.
Fragment HTML is byte-identical to what chasing.html / followups.html contain, except
Taiwan, which is split out of its monolithic section (prose dropped).
Run after frags_v2.py, frags_f.py, frags_tw.py.
"""
import json, os, re

F = json.load(open('frags_v2.json'))
G = json.load(open('frags_f.json'))
TW = json.load(open('frags_tw.json'))
SRC_V2 = open('page_v2.py').read()
SRC_F = open('page_f.py').read()
out = {}

# ---- 1. ready HTML fragments, same key names -------------------------------------------
V2_HTML = ['q1_cA','q1_cB','q1_cE','q1_tA','q1_tC','q1_tD','q1_tE','q1_tF','q1_tG',
           'q2_cB','q2_scatter','q2_tA','q2_tB','q2_tC','q2_tD','q2_tE','q2_tF','q2_tF2','q2_tG','q2_tH',
           'q3_cA','q3_cE','q3_tA','q3_tB10','q3_tB49','q3_tC','q3_tD','q3_tH','q3_tI',
           'q4_cum','q4_rank','q4_tA','q4_tB1','q4_tB3','q4_tBcs','q4_tC','q4_tD','q4_tE']
F_HTML = ['f1_c','f1_t','f1_t2','f2_t','f2_t2','f3_c','f3_t','f4_t1','f4_t2','f4_t3',
          'f5_t1','f5_t2','f6_t1','f6_t2']
for k in V2_HTML: out[k] = F[k]
for k in F_HTML: out[k] = G[k]

# ---- 2. row-data keys: same wrapping page_v2.py applies (header copied from its source) ---
pat = re.compile(r"<summary>(.*?)</summary>(<div class=\"tbl\"><table><thead>.*?<tbody>)' \+ F\['(\w+)'\] \+ '(</tbody></table></div>)</details>")
RENAME = {'q1_rows_ep': 'q1_ep_table', 'q3_rows_spdr': 'q3_spdr_table', 'q4_rows': 'q4_edhec_table'}
found = pat.findall(SRC_V2)
assert sorted(m[2] for m in found) == sorted(RENAME), found
for _summary, head, key, tail in found:
    out[RENAME[key]] = head + F[key] + tail
# q2_country: chip spans, wrapped in the container page_v2.py puts them in
out['q2_country_chips'] = '<div class="chips" aria-label="各國相關係數">' + F['q2_country'] + '</div>'

# ---- 3. hard-coded data markup in page_v2.py -------------------------------------------
m = re.search(r'<div class="now-grid">.*?\n  </div>', SRC_V2, re.S); assert m
out['top_years'] = m.group(0)
m = re.search(r'<div class="era"><table>.*?</table></div>', SRC_V2, re.S); assert m
out['era_table'] = m.group(0)

# ---- 4. hard-coded data markup in page_f.py (ported verbatim: posrows / meter / pos table) -
def meter(p): return f'<div class="meter" aria-hidden="true"><i style="width:{p:.0f}%"></i></div>'
posrows=[('近 3 年報酬（年化 20.9%）',87,'2026-08'),('CAPE（40.6）',99,'2026-09'),('超額 CAPE 殖利率（1.0%，越低越貴）',81,'2026-09'),('CAPE 相對近 30 年中位數（1.47 倍）',83,'2026-09'),
        ('實質盈餘相對 10 年平均（1.58 倍）',98,'2026-06'),('漲勢集中度（市值加權領先等權 10.0 個百分點）',94,'2026-08'),('科技業相對估值（淨值市價比 0.51，越低越貴）',74,'2026')]
now_pos='<div class="pos"><table><thead><tr><th scope="col" style="text-align:left">指標（現值）</th><th scope="col">歷史百分位</th><th scope="col" style="text-align:left">位置</th><th scope="col">資料月份</th></tr></thead><tbody>'+''.join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td class='m'>{meter(b)}</td><td>{c}</td></tr>" for a,b,c in posrows)+'<tr><th scope="row">科技業佔美股市值（42%）</th><td>最高</td><td class="m">'+meter(100)+'</td><td>2025 年底</td></tr></tbody></table></div>'
out['now_pos'] = now_pos

# ---- 5. Taiwan: split the monolithic section into its tables ----------------------------
sec = TW['section']
tbls = re.findall(r'<div class="tbl"><table>.*?</table></div>', sec, re.S)
assert len(tbls) == 6, len(tbls)
for key, t in zip(['tw_year_cond','tw_month_cond','tw_start10','tw_sector_chase','tw_sector_yearly','tw_now_years'], tbls):
    out[key] = t

# ---- 6. self-check against the rendered pages (when present) ---------------------------
if os.path.exists('chasing.html') and os.path.exists('followups.html'):
    H = {'chasing': open('chasing.html').read(), 'followups': open('followups.html').read()}
    for k, v in out.items():
        n = sum(h.count(v) for h in H.values())
        if n != 1: print('WARN', k, 'occurs', n, 'times in rendered pages')
json.dump(out, open('frags_merged.json', 'w'), ensure_ascii=False)
print('frags_merged.json:', len(out), 'placeholders')
