"""FRED：fredgraph.csv，逗號一次抓多條。不自訂 User-Agent。"""
import csv
import io
import time
import zipfile

from ._http import get, to_float

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
# FRED 一次回多條時，同頻率的檔案最多只給前 6 條，其餘悄悄丟掉；所以一批只放 5 條，缺的再逐條補抓。
CHUNK = 5


def parse(text, ids):
    """多欄 CSV -> {id: [(date, float)]}。第一欄是日期（observation_date 或 DATE）。"""
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise ValueError("空檔")
    head = rows[0]
    out = {}
    for fid in ids:
        if fid not in head:
            continue
        j = head.index(fid)
        obs = []
        for r in rows[1:]:
            if len(r) <= j:
                continue
            v = to_float(r[j])
            if v is None:
                continue
            obs.append((r[0][:10], v))
        out[fid] = obs
    return out


def parse_payload(raw, ids):
    """FRED 一次抓多條：頻率相同回 CSV；頻率混合時回 zip（每種頻率一個 csv + README）。"""
    if raw[:2] == b"PK":
        out = {}
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for name in z.namelist():
                if name.lower().endswith(".csv"):
                    out.update(parse(z.read(name).decode("utf-8-sig", "replace"), ids))
        return out
    return parse(raw.decode("utf-8-sig", "replace"), ids)


def _fetch_ids(ids):
    raw = get(URL + "?id=" + ",".join(ids), ua=None, binary=True, retries=2)
    out = parse_payload(raw, ids)
    if not out:
        raise RuntimeError("FRED 回傳內容讀不到任何請求的序列（開頭：%r）" % raw[:60])
    return out


def fetch(specs):
    res = {}
    ids_by_sid = {s["sid"]: s["params"]["id"] for s in specs}
    sids = list(ids_by_sid)
    for i in range(0, len(sids), CHUNK):
        if i:
            time.sleep(0.5)
        chunk = sids[i:i + CHUNK]
        ids = [ids_by_sid[x] for x in chunk]
        try:
            parsed = _fetch_ids(ids)
        except Exception as e:  # noqa: BLE001  整批失敗：改逐條試一次
            parsed = {}
            for sid in chunk:
                fid = ids_by_sid[sid]
                try:
                    parsed.update(_fetch_ids([fid]))
                except Exception as e2:  # noqa: BLE001
                    res[sid] = {"error": str(e2)[:200]}
        for sid in chunk:
            if sid in res:
                continue
            fid = ids_by_sid[sid]
            if fid not in parsed:  # 批次漏掉的，單獨再抓一次
                try:
                    parsed.update(_fetch_ids([fid]))
                except Exception as e2:  # noqa: BLE001
                    res[sid] = {"error": str(e2)[:200]}
                    continue
            obs = parsed.get(fid)
            if not obs:
                res[sid] = {"error": "FRED 回傳無資料：%s" % fid}
            else:
                res[sid] = {"obs": obs}
    return res
