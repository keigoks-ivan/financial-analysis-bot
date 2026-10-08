"""財政部（預算司）月度「財政收支情況」新聞稿（gks.mof.gov.cn/tongjishuju）。

新聞稿只有文字、沒有表格或 API，所以做法是：
  1. 抓統計數據列表頁（index.htm；回補時加 index_1.htm…），標題「2026年1-8月财政收支情况」「2026年上半年…」等 → 該期（累計到哪個月）
  2. 抓內頁，去標籤後用句型取「全国一般公共预算收入 X 亿元，同比增长 Y%」這類句子
輸出皆為「年初至當月累計」：金額（億元）與同比（%）。catalog 以同比為主（field = yoy_pct），金額用 field = ytd_amount。
日期：累計到 N 月的那一期，存成該年 N 月 1 日（1-2 月合併稿存 2 月）。

平常只看列表第 1 頁，只抓 store 還沒有的期別（每次最多 3 篇，連續 2 篇失敗就停）；回補模式 MACRO_DB_BACKFILL=1 抓列表全部頁、
since_year 以後的全部期別。財政部網站常回 502，每次請求退避重試 3 次，仍失敗的期別留到下一次。
2022 年有 6 篇（4、5、7、8、10、11 月）改用「扣除留抵退稅因素後增長…按自然口徑計算下降」的句型，解析不出來，缺月就缺（不寫專用規則）。
頁面改版、最新一篇解析不到任何項目時，整批回 error 並寫明原因，不會靜默回空。

params：
  metric      rev｜tax｜nontax｜exp｜vat｜cit｜pit｜deed｜lvat｜stamp｜fund_rev｜fund_exp｜land
  field       yoy_pct（累計同比，%）或 ytd_amount（累計金額，億元）
  since_year  回補起始年（預設 2020）
  index_url   列表頁網址（CI probe 用）
"""
from __future__ import annotations

import html as _html
import re
import sys

try:
    from . import cn_common as C
    from .. import store
except ImportError:
    import cn_common as C
    import store

BASE = "https://gks.mof.gov.cn/tongjishuju/"
MAX_PER_RUN = 3
NUM = r"(\d+(?:\.\d+)?)"
# metric -> 句首。句型：<句首>X亿元，(同比|比上年同期|比上年)(增长|下降|减少)Y%（全年稿用「比上年」）
LEAD = {
    "rev": "全国一般公共预算收入", "tax": "税收收入", "nontax": "非税收入", "exp": "全国一般公共预算支出",
    "vat": "国内增值税", "cit": "企业所得税", "pit": "个人所得税", "deed": "契税", "lvat": "土地增值税",
    "stamp": "印花税", "fund_rev": "全国政府性基金预算收入", "fund_exp": "全国政府性基金预算支出",
    "land": "国有土地使用权出让收入",
}
FIELDS = {"ytd_amount": 0, "yoy_pct": 1}


class Restructured(RuntimeError):
    pass


# ---------- 解析 ----------
def period_of(title: str):
    """標題 -> (年, 累計到幾月)；不是財政收支稿回 None。"""
    t = re.sub(r"\s+", "", title)
    m = re.match(r"^(\d{4})年(?:1-)?(\d{1,2})月财政收支情况$", t)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r"^(\d{4})年(上半年|一季度|前三季度)财政收支情况$", t)
    if m:
        return int(m.group(1)), {"一季度": 3, "上半年": 6, "前三季度": 9}[m.group(2)]
    m = re.match(r"^(\d{4})年财政收支情况$", t)
    if m:
        return int(m.group(1)), 12
    return None


def parse_list(html: str) -> dict:
    """列表頁 -> {'YYYY-MM': 絕對網址}（同一期只留第一個）。"""
    out = {}
    for m in re.finditer(r'<a\s[^>]*href="([^"]+)"[^>]*title="([^"]+)"', html):
        p = period_of(_html.unescape(m.group(2)))
        if p:
            href = m.group(1)
            url = href if href.startswith("http") else BASE + href.lstrip("./")
            out.setdefault("%04d-%02d" % p, url)
    return out


def page_count(html: str) -> int:
    m = re.search(r"var\s+countPage\s*=\s*(\d+)", html)
    return int(m.group(1)) if m else 1


def page_text(html: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    t = _html.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"[\s　]+", "", t)


def parse_article(text: str) -> dict:
    """內文 -> {metric: (累計金額, 累計同比%)}；找不到的項目不放。"""
    out = {}
    for key, lead in LEAD.items():
        m = re.search(re.escape(lead) + NUM + r"亿元，?(?:同比|比上年同期|比上年)(增长|下降|减少)" + NUM + "%", text)
        if m:
            sign = -1.0 if m.group(2) in ("下降", "减少") else 1.0
            out[key] = (float(m.group(1)), sign * float(m.group(3)))
    return out


def values_for(p: dict, parsed: dict) -> list:
    i = FIELDS[p["field"]]
    return [("%s-01" % ym, v[p["metric"]][i]) for ym, v in sorted(parsed.items()) if p["metric"] in v]


# ---------- 抓取 ----------
def _get(s, url):
    # 平常退避重試 3 次；回補是一次性的，財政部又常連續 502，多試幾次（單次最多等 15 秒）
    kw = dict(retries=8, base=3.0, cap=15.0) if C.backfill_mode() else dict(retries=3, base=3.0)
    return C.http_backoff(s, "GET", url, **kw).content.decode("utf-8", "replace")


def collect_periods(s, backfill: bool, since_year: int) -> dict:
    first = _get(s, BASE + "index.htm")
    found = parse_list(first)
    if backfill:
        for n in range(1, page_count(first)):
            try:
                found.update({k: v for k, v in parse_list(_get(s, BASE + "index_%d.htm" % n)).items() if k not in found})
            except RuntimeError as e:
                print("cn_mof 列表第 %d 頁失敗：%s" % (n, str(e)[:100]), file=sys.stderr)
    return {k: v for k, v in found.items() if int(k[:4]) >= since_year}


def fetch(specs: list[dict]) -> dict:
    if not specs:
        return {}
    backfill = C.backfill_mode()
    since = min(int(sp["params"].get("since_year", 2020)) for sp in specs)
    s = C.session()
    try:
        listing = collect_periods(s, backfill, since)
        if not listing:
            raise Restructured("列表頁找不到任何「財政收支情況」標題（頁面可能改版）")
    except Exception as e:  # noqa: BLE001
        return {sp["sid"]: {"error": "財政部列表頁失敗：%s" % str(e)[:160]} for sp in specs}
    stored = {sp["sid"]: dict(store.read(sp["sid"])) for sp in specs}
    todo = [ym for ym in sorted(listing, reverse=True)
            if not any(("%s-01" % ym) in stored[sp["sid"]] for sp in specs)]
    if not backfill:
        todo = todo[:MAX_PER_RUN]
    newest = max(listing)
    parsed: dict = {}
    failed: list = []
    streak = 0
    for ym in todo:
        try:
            got = parse_article(page_text(_get(s, listing[ym])))
            streak = 0
        except Exception as e:  # noqa: BLE001
            failed.append("%s：%s" % (ym, str(e)[:100]))
            streak += 1
            if streak >= 2 and not backfill:
                break
            continue
        if got:
            parsed[ym] = got
        else:
            failed.append("%s：解析不到任何項目" % ym)
            if ym == newest:
                return {sp["sid"]: {"error": "財政部最新一篇（%s）解析不到任何項目，句型可能改版" % ym} for sp in specs}
    if failed:
        print("cn_mof 未收的期別：" + "；".join(failed), file=sys.stderr)
    if todo and not parsed:
        return {sp["sid"]: {"error": "財政部內頁全部失敗（%s）；沿用舊資料" % failed[0]} for sp in specs}
    res = {}
    for sp in specs:
        merged = dict(stored[sp["sid"]])
        merged.update(dict(values_for(sp["params"], parsed)))
        res[sp["sid"]] = {"obs": sorted(merged.items())} if merged else {"error": "財政部這個項目（%s）沒有解析到數值" % sp["params"]["metric"]}
    return res
