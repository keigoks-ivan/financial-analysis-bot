"""國家統計局「國家數據」新平台（data.stats.gov.cn）。中國區主來源。

流程：GET queryIndexTreeAsync?pid=&code=1|2 取月／季樹根 → 對每個 cid GET queryIndicatorsByCid 取指標清單
→ 依「指標名稱」比對指標 id（不寫死 id）→ 同一 cid 的指標合併成一次 POST stream/esData。
同一網站請求間隔 ≥ 1 秒、用同一個 Session（帶 cookie）。回應不是 JSON（被網站防護擋成挑戰頁）就整批回 error，不繞過。

params：
  tree      "M"（月度樹，預設）或 "Q"（季度樹）
  cid + name  單一來源；name 為平台上的指標名稱（簡體，空白不拘）
  parts     [{"cid":…, "name":…}, …] 依基期拆表的序列（CPI），排在前面的優先；日期重疊時取前者
  scale     選填，乘以此數後再存
  overlay   選填：平台落後時，用較新的官方來源補在平台最後一個月之後。{"pbc": "m2_level"}（人行貨幣供應量表）或
            {"nbs_pmi": {"sheet": "制造业", "col": "PMI"}}（統計局 PMI 新聞稿附件）
  probe_url 完整網址（CI probe 用，fetcher 不讀）
"""
from __future__ import annotations

import re

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

B = "https://data.stats.gov.cn/dg/website/publicrelease/web/external"
ROOT_FALLBACK = {"M": "fc982599aa684be7969d7b90b1bd0e84", "Q": "a94b8b7365a94874968cabbe392cf679"}
TREE_CODE = {"M": 1, "Q": 2}
DTS = {"M": "199001MM-203012MM", "Q": "199001SS-203004SS"}


def code_to_date(code: str):
    """'202608MM' -> '2026-08-01'；'202602SS'（第 2 季）-> '2026-04-01'；'2025SS'／'2025YY' -> '2025-01-01'。"""
    m = re.match(r"^(\d{4})(\d{2})?([A-Z]{2})$", str(code))
    if not m:
        return None
    y, n, kind = m.group(1), m.group(2), m.group(3)
    if kind == "MM" and n:
        return "%s-%s-01" % (y, n)
    if kind == "SS" and n:
        q = int(n)
        return "%s-%02d-01" % (y, (q - 1) * 3 + 1) if 1 <= q <= 4 else None
    if n is None:
        return "%s-01-01" % y
    return None


def parse_rows(data: list, ids_by_key: dict) -> dict:
    """esData 的 data[]（每期一列）-> {指標 id: [(date, float)]}。空字串＝無資料，略過。"""
    out = {i: [] for i in ids_by_key.values()}
    for row in data or []:
        d = code_to_date(row.get("code"))
        if not d:
            continue
        for v in row.get("values", []):
            i = v.get("_id")
            if i in out:
                x = C.to_float(v.get("value"))
                if x is not None:
                    out[i].append((d, x))
    return out


def match_indicator(lst: list, name: str):
    want = C.clean(name)
    hit = [x for x in lst if C.clean(x.get("i_showname")) == want]
    return hit[0]["_id"] if len(hit) == 1 else None


def parts_of(p: dict) -> list:
    return p.get("parts") or [{"cid": p["cid"], "name": p["name"]}]


def merge_parts(chunks: list) -> list:
    """chunks 由優先到次要排列；同日取先出現者。"""
    d = {}
    for ch in chunks:
        for k, v in ch:
            d.setdefault(k, v)
    return sorted(d.items())


def fetch(specs: list[dict]) -> dict:
    res: dict = {}
    if not specs:
        return res
    s = C.session()
    overlay_cache: dict = {}
    trees = sorted({sp["params"].get("tree", "M") for sp in specs})
    roots = {}
    blocked = None
    try:
        for t in trees:
            try:
                j = C.http_json(s, "GET", "%s/new/queryIndexTreeAsync?pid=&code=%d" % (B, TREE_CODE[t]))
                roots[t] = j["data"][0]["_id"]
            except C.Blocked:
                raise
            except Exception:  # noqa: BLE001
                roots[t] = ROOT_FALLBACK[t]
        # cid -> tree、需要的名稱
        need: dict = {}
        for sp in specs:
            t = sp["params"].get("tree", "M")
            for part in parts_of(sp["params"]):
                need.setdefault((part["cid"], t), set()).add(part["name"])
        got: dict = {}   # (cid, name) -> {"obs":…} 或 {"error":…}
        for (cid, t), names in sorted(need.items()):
            try:
                j = C.http_json(s, "GET", "%s/new/queryIndicatorsByCid?cid=%s&dt=&name=" % (B, cid))
                lst = j["data"]["list"]
            except C.Blocked:
                raise
            except Exception as e:  # noqa: BLE001
                for n in names:
                    got[(cid, n)] = {"error": "指標清單取得失敗：%s" % str(e)[:120]}
                continue
            ids = {}
            for n in sorted(names):
                i = match_indicator(lst, n)
                if i is None:
                    got[(cid, n)] = {"error": "指標清單裡找不到名稱「%s」（cid %s…）" % (n, cid[:6])}
                else:
                    ids[n] = i
            if not ids:
                continue
            try:
                body = {"cid": cid, "indicatorIds": sorted(set(ids.values())), "daCatalogId": "",
                        "das": [{"text": "全国", "value": "000000000000"}], "showType": "1",
                        "dts": [DTS[t]], "rootId": roots[t]}
                j = C.http_json(s, "POST", B + "/stream/esData", json=body)
                parsed = parse_rows(j["data"], ids)
                for n, i in ids.items():
                    got[(cid, n)] = {"obs": parsed[i]} if parsed[i] else {"error": "平台沒有回傳這個指標的數值（%s）" % n}
            except C.Blocked:
                raise
            except Exception as e:  # noqa: BLE001
                for n in ids:
                    got[(cid, n)] = {"error": "esData 失敗：%s" % str(e)[:120]}
    except C.Blocked as e:
        blocked = str(e)
    for sp in specs:
        p = sp["params"]
        if blocked:
            res[sp["sid"]] = {"error": "國統局平台疑似擋下請求，整批略過：" + blocked}
            continue
        chunks, errs = [], []
        for part in parts_of(p):
            r = got.get((part["cid"], part["name"]), {"error": "未取得"})
            if "obs" in r:
                chunks.append(r["obs"])
            else:
                errs.append(r["error"])
        if errs:
            res[sp["sid"]] = {"error": "；".join(errs)}
            continue
        obs = merge_parts(chunks)
        if p.get("overlay"):
            try:
                obs = overlay(obs, p["overlay"], s, overlay_cache)
            except Exception:  # noqa: BLE001  補最新月失敗不影響平台資料本身；只是最新月會晚一個月
                pass
        sc = p.get("scale")
        if sc:
            obs = [(k, v * sc) for k, v in obs]
        res[sp["sid"]] = {"obs": obs}
    return res


def overlay(obs: list, cfg: dict, s, cache: dict) -> list:
    """平台資料之後的月份，由較新的官方來源補上（只補平台沒有的日期，不覆蓋平台值）。
    cfg：{"pbc": "m2_level"}（人行貨幣供應量表）或 {"nbs_pmi": {"sheet":…, "col":…}}（統計局 PMI 新聞稿附件）。"""
    if "pbc" in cfg:
        try:
            from . import cn_pbc
        except ImportError:
            import cn_pbc
        extra = cn_pbc.latest_for(cfg["pbc"], s)
    else:
        try:
            from . import cn_nbs_pmi
        except ImportError:
            import cn_nbs_pmi
        extra = cn_nbs_pmi.latest(cfg["nbs_pmi"], s, cache)
    last = obs[-1][0] if obs else ""
    return sorted(obs + [(k, v) for k, v in extra if k > last])
