"""印尼銀行（Bank Indonesia）SEKI 印尼經濟金融統計表（免金鑰，固定網址 xls）。

網址：https://www.bi.go.id/SEKI/tabel/TABEL<表號>.xls，用 xlrd 讀（BIFF 格式）。
HTTP 一律走 _http（NAMED_UA：名稱＋網址 UA，不偽裝瀏覽器）；同一個檔一次下載、多條序列共用，
不同檔之間隔 1 秒。

工作表與欄位版面：
  - 每檔有多張工作表，舊期間在前、最新期間在最後一張；預設讀最後一張。
  - 表頭：年份列（數值 1990～2040）下一列為期別列（Jan～Dec 或 Q1～Q4，後面可帶 * 表示暫定）。
    年份標籤的位置各表不一（有的放該年最後一欄、有的放第一欄），所以改用「期別遇到 Jan／Q1 就換年」
    的順序對應年份標籤；對不起來的整張表報錯，不猜。
  - 項次號在最左欄或最右欄（浮點數），英文標籤在其左一欄或同列字串欄。空白欄是年合計，略過。
  - 同一張工作表內項次號可能重複（例如 I.4 的 121、122），重複時必須用 params.label 指定標籤子字串。

params：
  table     表號，如 "TABEL1_1"（必填）
  item      項次號（必填）
  label     選填。列內任一字串欄含此子字串（不分大小寫）才算；項次重複時必填
  sheet     選填，工作表名稱；預設最後一張
  start     選填，'YYYY-MM'；早於此月的值丟掉（用在基期改版、舊基期不能接的指數，例如 CPI 2024-01 起改 2022=100）
  scale     選填，乘以此數後再存（例：SEKI 的外貿以千美元計，轉百萬美元給 0.001）
  history   選填，舊工作表接續清單 [{"sheet":…, "item":…, "label":…}, …]：
            2025-01 起部分銀行表分組改版，最新表只從 2025-01 開始，舊歷史在 'Th 2010-2024' 等舊表。
            只有人工比對過接合處沒有口徑跳動的序列才設 history。接法：新表有值的日期用新表，
            新表第一個日期之前用舊表（依清單順序，先出現的優先）。
  probe_url 選填（fetcher 不讀）

注意：最近幾個月是暫定值（期別帶 *），BI 事後會修；store 會用新抓到的值覆蓋舊值。
回補模式：本來源每次下載就含完整歷史，不需要 MACRO_DB_BACKFILL。
"""
from __future__ import annotations

import io
import re
import time

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

URL = "https://www.bi.go.id/SEKI/tabel/%s.xls"
_GAP = 1.0  # 同一站請求間隔（秒）


def _sheet_cols(sh) -> dict:
    """{欄索引: 'YYYY-MM-01'}；月表與季表皆可。"""
    year_row, labels = None, []
    for r in range(0, min(sh.nrows, 10)):
        ys = [(j, int(c.value)) for j, c in enumerate(sh.row(r))
              if isinstance(c.value, float) and 1989 < c.value < 2041 and c.value == int(c.value)]
        if len(ys) >= 1 and r + 1 < sh.nrows:
            nxt = [str(c.value).strip().rstrip("*").strip() for c in sh.row(r + 1)]
            if any(A.month_num(x) and len(x) <= 9 or re.fullmatch(r"Q[1-4]", x) for x in nxt if x):
                year_row, labels = r, sorted(ys)
                break
    if year_row is None:
        raise ValueError("找不到年份列／期別列")
    prow = year_row + 1
    periods = []  # (col, kind, n)
    for j in range(sh.ncols):
        v = sh.cell_value(prow, j)
        if not isinstance(v, str):
            continue
        p = v.strip().rstrip("*").strip()
        if re.fullmatch(r"Q[1-4]", p):
            periods.append((j, "Q", int(p[1])))
        elif len(p) <= 9 and A.month_num(p) and p[:3].lower() in A.MONTHS:
            periods.append((j, "M", A.month_num(p)))
    if not periods:
        raise ValueError("期別列沒有月或季標籤")
    # 依「期別回頭（n 變小）」切年
    groups, cur, last = [], [], 0
    for item in periods:
        if cur and item[2] <= last:
            groups.append(cur)
            cur = []
        cur.append(item)
        last = item[2]
    groups.append(cur)
    years = [y for _, y in labels]
    if len(years) == len(groups):
        ymap = years
    elif len(years) > len(groups):
        ymap = years[-len(groups):]
    else:
        # 年份標籤少於期別群：以最後一年往回連續推（僅在年份連續時可信）
        ymap = [years[-1] - (len(groups) - 1 - i) for i in range(len(groups))]
    out = {}
    for g, y in zip(groups, ymap):
        for j, kind, n in g:
            out[j] = A.ym_date(y, n) if kind == "M" else A.yq_date(y, n)
    return out


def _row_strings(sh, i) -> str:
    return " ".join(str(c.value) for c in sh.row(i) if isinstance(c.value, str)).lower()


def _find_row(sh, item, label=None) -> int:
    hits = []
    for i in range(sh.nrows):
        for j in (0, sh.ncols - 1):
            v = sh.cell_value(i, j)
            if isinstance(v, float) and v == float(item):
                hits.append(i)
                break
    if label:
        hits = [i for i in hits if label.lower() in _row_strings(sh, i)]
    if not hits:
        raise KeyError("工作表 %s 找不到項次 %s%s" % (sh.name, item, "（%s）" % label if label else ""))
    if len(hits) > 1:
        raise KeyError("工作表 %s 項次 %s 重複 %d 列，需指定 label" % (sh.name, item, len(hits)))
    return hits[0]


def read_sheet_series(sh, item, label=None) -> dict:
    cols = _sheet_cols(sh)
    i = _find_row(sh, item, label)
    out = {}
    for j, d in cols.items():
        v = sh.cell_value(i, j)
        if isinstance(v, float):
            out[d] = v
    return out


def _pick_sheet(wb, name=None):
    if name is None:
        return wb.sheets()[-1]
    for s in wb.sheets():
        if s.name.strip() == name.strip():
            return s
    raise KeyError("找不到工作表 %s" % name)


def read_spec(wb, p: dict) -> list:
    main = read_sheet_series(_pick_sheet(wb, p.get("sheet")), p["item"], p.get("label"))
    merged = dict(main)
    for h in p.get("history", []):
        old = read_sheet_series(_pick_sheet(wb, h["sheet"]), h["item"], h.get("label"))
        first = min(merged) if merged else "9999"
        for d, v in old.items():
            if d < first and d not in merged:
                merged[d] = v
    if p.get("start"):
        cut = p["start"][:7] + "-01"
        merged = {d: v for d, v in merged.items() if d >= cut}
    scale = float(p.get("scale", 1.0))
    return sorted((d, v * scale) for d, v in merged.items())


def fetch(specs: list[dict]) -> dict:
    import xlrd

    books: dict = {}
    state = {"last": 0.0}

    def book(table):
        if table not in books:
            wait = _GAP - (time.time() - state["last"])
            if wait > 0 and books:
                time.sleep(wait)
            try:
                raw = _http.get(URL % table, binary=True)
                books[table] = xlrd.open_workbook(file_contents=raw)
            except Exception as e:  # noqa: BLE001
                books[table] = e
            state["last"] = time.time()
        if isinstance(books[table], Exception):
            raise books[table]
        return books[table]

    def one(s):
        p = s["params"]
        return read_spec(book(p["table"]), p)

    return A.run_specs(specs, one, workers=1)
