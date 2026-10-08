"""series CSV 與 status.json 的讀寫、合併。

合併規則：新抓到的日期覆蓋舊值（吸收修正）；舊檔有、新抓沒有的日期保留。
這樣只給近 12 個月的序列（成屋銷售、台灣三大法人等）會自己累積歷史。
內容沒變就不重寫檔案。
"""
import csv
import datetime as dt
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "macro_db"


def series_path(sid, data_dir=None):
    return Path(data_dir or DATA) / "series" / (sid + ".csv")


def fmt(v):
    """固定小數寫法：最多 6 位、去尾零，避免每次抓都因浮點尾數而改檔。"""
    s = ("%.6f" % float(v)).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def read(sid, data_dir=None):
    p = series_path(sid, data_dir)
    if not p.exists():
        return []
    out = []
    with p.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) >= 2 and row[1] != "":
                out.append((row[0], float(row[1])))
    return out


def merge(old, new):
    """old、new 皆為 [(date, value)]；回傳依日期排序的合併結果。"""
    d = {k: v for k, v in old}
    for k, v in new:
        d[k] = float(v)
    return sorted(d.items())


def _render(obs):
    buf = io.StringIO()
    buf.write("date,value\n")
    for d, v in obs:
        buf.write("%s,%s\n" % (d, fmt(v)))
    return buf.getvalue()


def write_merged(sid, new_obs, data_dir=None):
    """合併後寫檔。回傳 (合併後 obs, 是否改了檔, 是否為新檔)。"""
    p = series_path(sid, data_dir)
    existed = p.exists()
    old = read(sid, data_dir)
    merged = merge(old, new_obs)
    text = _render(merged)
    if existed and p.read_text(encoding="utf-8") == text:
        return merged, False, False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="")
    return merged, True, not existed


def load_status(data_dir=None):
    p = Path(data_dir or DATA) / "status.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def save_status(status, data_dir=None):
    """status 內容沒變就不重寫（時間戳記只在序列有動作時才更新，見 update_status）。"""
    p = Path(data_dir or DATA) / "status.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(status, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if p.exists() and p.read_text(encoding="utf-8") == text:
        return False
    p.write_text(text, encoding="utf-8")
    return True


def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def update_status(status, sid, merged, error=None, changed=False, first_time=False, now=None):
    """成功：last_ok 更新、last_error 清掉；失敗：保留 last_ok，只記 last_error。
    advanced＝最新資料日期變大的時間（供「最近公布」使用；第一次建檔不算）。"""
    now = now or now_iso()
    e = dict(status.get(sid) or {})
    if error is None:
        prev_last = e.get("last_date")
        new_last = merged[-1][0] if merged else None
        e["last_ok"] = now
        e["last_error"] = None
        e["last_date"] = new_last
        e["n"] = len(merged)
        if prev_last and new_last and new_last > prev_last:
            e["advanced"] = now
        e.setdefault("advanced", None)
    else:
        e["last_error"] = str(error)[:300]
        e.setdefault("last_ok", None)
        e.setdefault("last_date", merged[-1][0] if merged else None)
        e.setdefault("n", len(merged))
        e.setdefault("advanced", None)
    status[sid] = e
    return e
