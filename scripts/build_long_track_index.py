#!/usr/bin/env python3
"""前瞻追蹤總覽頁 /long-track/ 產生器（fab）。

家族地圖：實單主系統／影子對照／前瞻 OOS 候選／已退役・凍結對照 四分類卡片。
nav 用 full_nav_block("system","lthub")（追蹤總覽）。靜態內容、
無資料層；系統狀態變動時更新此檔重跑。中文全形標點。

用法：python3 scripts/build_long_track_index.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "lthub")
OUT = HERE.parent / "docs" / "long-track" / "index.html"

# 每組＝(分類、色、突出、系統清單)；系統 dict：name／url／one／status／freq／email
GROUPS = [
    ("實單主系統", "live", True, [
        {"name": "W52 × 自適應波動率 cap 1.5（美 + 台）", "url": "/long-track-w52-adaptive/",
         "one": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層。"
                "<b>2026-07-18 起接棒為實單主系統</b>。",
         "status": ("實單", "live"), "freq": "每交易日 × 2（台／美收盤後）", "email": "✅ 有"},
    ]),
    ("影子對照（同引擎、不上槓桿）", "shadow", False, [
        {"name": "W52 × 自適應波動率 cap 1.0 影子", "url": "/long-track-w52-adaptive/leverage.html",
         "one": "同引擎的 cap 1.0（不上槓桿）影子線，供槓桿 vs 不槓桿對照。",
         "status": ("影子對照", "shadow"), "freq": "每交易日 × 2", "email": "❌（併入主系統通知）"},
    ]),
    ("前瞻 OOS 候選（決策前研究通過、尚非實單）", "cand", False, [
        {"name": "🥇 GLD 金 sleeve", "url": "/long-track-gld/",
         "one": "非股票 sleeve 決策前研究通過後的前瞻紙上追蹤（單腿 GLD、cap 1.0、"
                "W52×自適應＋A2）。長樣本 1976-2026 含 20 年熊市壓力測試通過。<b>尚非實單</b>。",
         "status": ("前瞻 OOS・候選", "cand"), "freq": "每交易日（美股收盤後）", "email": "✅（可行動變化）"},
        {"name": "🐢 商品 Sleeve（80/20 組合）", "url": "/turtle-sleeve/",
         "one": "GLD/USO→期貨 商品 sleeve 疊上 STX50 的 80/20 組合曝險，OOS 並行追蹤。",
         "status": ("前瞻 OOS・候選", "cand"), "freq": "每交易日", "email": "—"},
    ]),
    ("已退役・凍結對照（被 W52×自適應取代）", "ret", False, [
        {"name": "STX50（SMH/QQQ 美股）", "url": "/long-track-smh/",
         "one": "2026-07-18 由 W52×自適應接棒、2026-07-23 停更（cron 已移除）。",
         "status": ("已凍結・2026-07-23 停更", "ret"), "freq": "已停更（僅手動）", "email": "—"},
        {"name": "E3（0050/2330 台股）", "url": "/long-track-tw/",
         "one": "2026-07-18 由 W52×自適應接棒、2026-07-23 停更（cron 已移除）。",
         "status": ("已凍結・2026-07-23 停更", "ret"), "freq": "已停更（僅手動）", "email": "—"},
        {"name": "0050 + 2330 固定 σ（歸檔）", "url": "/long-track-tw-vt/",
         "one": "固定 σ 版波動率目標，vt 家族早期研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "自適應美台總覽（歸檔）", "url": "/long-track-adaptive-vt/",
         "one": "自適應 σ 美台總覽，vt 家族研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "QQQ + SMH 長軌 × 套袖（歸檔）", "url": "/long-track-qs-vt/",
         "one": "週線長軌閘門 × 波動率套袖組合，vt 家族研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "六狀態機（SMH/QQQ）", "url": "/backtest/six_state/status/",
         "one": "早期六態機引擎，已退役、僅手動；被 W52×自適應取代。",
         "status": ("凍結對照", "ret"), "freq": "手動", "email": "—"},
    ]),
]

PLAIN = ('這個家族的沿革（白話）：早期實單主線用「六狀態機」與「STX50／E3」兩套引擎；'
         '<b>2026-07-18 起改由「W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層」接棒為實單主系統</b>'
         '（美台兩市場各 70% 指數部），舊引擎降為凍結對照。'
         'GLD 金 sleeve 與商品 sleeve 是決策前研究通過後的<b>前瞻候選</b>——還在紙上測、尚未進實單。')

CSS = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e;--grey:#9ca3af}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.6rem 0 1.1rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.88rem;margin-top:.25rem;max-width:76ch}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.plain-box{display:flex;gap:.6rem;background:#f0f7ff;border:1px solid #cfe3fb;border-left:4px solid #3b82f6;border-radius:8px;padding:.8rem 1rem;margin:1.1rem 0 .3rem;font-size:.88rem;line-height:1.7}
.pb-tag{flex:0 0 auto;font-size:.72rem;font-weight:700;color:#1e40af;background:#dbeafe;border-radius:6px;padding:.15rem .45rem;height:fit-content;white-space:nowrap}
.pb-body{color:#1e3a5f}.pb-body b{color:#1e40af}
.grp{margin-top:1.6rem}
.grp-h{font-size:.78rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin-bottom:.6rem;padding-left:.6rem;border-left:4px solid var(--grey)}
.grp.live .grp-h{border-left-color:var(--green);color:var(--green-text)}
.grp.cand .grp-h{border-left-color:var(--amber);color:var(--amber-text)}
.grp.shadow .grp-h{border-left-color:#6366f1}
.sys{display:block;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.95rem 1.15rem;margin-bottom:.7rem;color:inherit}
.sys:hover{border-color:var(--brand);text-decoration:none;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.grp.live .sys{border-width:2px;border-color:var(--green)}
.sys-top{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-bottom:.35rem}
.sys-name{font-size:1.02rem;font-weight:700;color:var(--text)}
.grp.live .sys-name{color:var(--green-text)}
.pill{font-size:.68rem;font-weight:700;padding:.12rem .55rem;border-radius:99px;white-space:nowrap}
.pill.live{background:var(--green);color:#fff}
.pill.shadow{background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe}
.pill.cand{background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.pill.ret{background:#f3f4f6;color:var(--muted);border:1px solid var(--border)}
.sys-one{font-size:.86rem;color:#374151;line-height:1.6}
.sys-meta{display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:.5rem;font-size:.76rem;color:var(--muted)}
.sys-meta b{color:#374151;font-weight:600}
.arr{margin-left:auto;color:var(--brand);font-weight:700}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
"""


def render() -> str:
    groups_html = ""
    for title, cls, prominent, systems in GROUPS:
        rows = ""
        for s in systems:
            st_txt, st_cls = s["status"]
            rows += (
                f'<a class="sys" href="{s["url"]}">'
                f'<div class="sys-top"><span class="sys-name">{s["name"]}</span>'
                f'<span class="pill {st_cls}">{st_txt}</span><span class="arr">→</span></div>'
                f'<div class="sys-one">{s["one"]}</div>'
                f'<div class="sys-meta"><span>更新頻率：<b>{s["freq"]}</b></span>'
                f'<span>Email 通知：<b>{s["email"]}</b></span></div></a>')
        groups_html += f'<div class="grp {cls}"><div class="grp-h">{title}</div>{rows}</div>\n'

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>前瞻追蹤總覽 | InvestMQuest Research</title>
<style>{CSS}</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 前瞻追蹤</div>
  <h1>前瞻追蹤總覽</h1>
  <div class="sub">實單主系統 · 影子對照 · 前瞻 OOS 候選 · 已退役凍結對照 — 一頁看清整個追蹤家族的定位與現況。</div>
</div></div>
<div class="container">
<div class="plain-box"><span class="pb-tag">💬 白話</span><span class="pb-body">{PLAIN}</span></div>
{groups_html}</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 前瞻追蹤總覽 · 僅供研究參考</div></footer>
</body>
</html>"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
