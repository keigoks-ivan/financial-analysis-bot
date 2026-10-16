"""越線通知：任一條狀態改變（未越→越線、越線→未越）才通知；首跑（無舊狀態）不發。

照 /fear-greed/ 的做法：寫 alert 檔，workflow 讀檔後寄信＋Discord。
"""
from __future__ import annotations

import html
from pathlib import Path

PAGE_URL = "https://research.investmquest.com/ai-credit/"


def build_alerts(prev_breached: dict | None, inds: list[dict], test: bool = False) -> list[dict]:
    """prev_breached：{指標編號字串: bool|None}；None（整個檔不存在）代表首跑，不發通知。

    舊狀態是 None（先前沒有資料）或新狀態是 None（這次沒有資料）的指標一律不通知。
    """
    out = []
    if test:
        for x in inds:
            if x["breached"] is True:
                out.append({"id": x["id"], "old": True, "new": True, "ind": x})
        return out
    if prev_breached is None:
        return []
    for x in inds:
        old = prev_breached.get(str(x["id"]))
        new = x["breached"]
        if old is None or new is None or old == new:
            continue
        out.append({"id": x["id"], "old": old, "new": new, "ind": x})
    return out


def _state(b: bool) -> str:
    return "越線" if b else "未越線"


def alert_text(alerts: list[dict], inds: list[dict], test: bool = False) -> tuple[str, str]:
    n_b = sum(1 for x in inds if x["breached"] is True)
    if test:
        title = f"【測試】AI 信用監測：12 條裡 {n_b} 條越線"
    else:
        parts = []
        for a in alerts:
            parts.append(f"第 {a['id']} 條{'進入越線' if a['new'] else '解除越線'}")
        title = "AI 信用監測：" + "；".join(parts) + f"（12 條裡 {n_b} 條越線）"
    lines = []
    for a in alerts:
        x = a["ind"]
        if test:
            lines.append(f"第 {x['id']} 條 {x['name']}：目前越線。現值 {x['value_text']}，門檻 {x['threshold']}，資料日期 {x['date_text']}。")
        else:
            lines.append(f"第 {x['id']} 條 {x['name']}：{_state(a['old'])} → {_state(a['new'])}。")
            lines.append(f"現值 {x['value_text']}，門檻 {x['threshold']}，資料日期 {x['date_text']}。")
        lines.append(x["plain"])
        lines.append("")
    lines.append(f"目前 12 條裡 {n_b} 條越線：" + ("、".join(f"第 {x['id']} 條" for x in inds if x["breached"] is True) or "無") + "。")
    lines.append(f"完整頁面：{PAGE_URL}")
    return title, "\n".join(lines)


def alert_mail_html(title: str, body: str) -> str:
    esc = html.escape
    paras = "".join(f'<p style="margin:0 0 10px 0;">{esc(l)}</p>' if l else "" for l in body.split("\n"))
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title></head>
<body style="margin:0;padding:0;background-color:#f6f5f2;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f6f5f2;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background-color:#ffffff;border:1px solid #e6e2d8;border-radius:8px;font-family:-apple-system,'PingFang TC','Noto Sans TC','Segoe UI',sans-serif;">
<tr><td style="background-color:#0f1f3d;color:#ffffff;padding:18px 24px;font-size:16px;font-weight:700;">{esc(title)}</td></tr>
<tr><td style="padding:18px 24px;font-size:14px;line-height:1.7;color:#1c1c1c;">{paras}</td></tr>
<tr><td style="padding:0 24px 22px 24px;text-align:center;"><a href="{PAGE_URL}" style="display:inline-block;background-color:#0f1f3d;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 28px;border-radius:6px;">查看 AI 信用監測頁</a></td></tr>
<tr><td style="padding:0 24px 20px 24px;font-size:12px;color:#6b6b6b;text-align:center;">InvestMQuest · AI 信用風險監測（只在狀態改變時寄出）</td></tr>
</table></td></tr></table></body></html>
"""


def write_alert_files(root: Path, alerts: list[dict], inds: list[dict], test: bool = False) -> str:
    title, body = alert_text(alerts, inds, test)
    if test:
        body = "這是測試訊息，不是真實狀態改變。\n\n" + body
    (root / "aic_title.txt").write_text(title + "\n", encoding="utf-8")
    (root / "aic_alert.txt").write_text(body + "\n", encoding="utf-8")
    (root / "aic_mail.html").write_text(alert_mail_html(title, body), encoding="utf-8")
    return title
