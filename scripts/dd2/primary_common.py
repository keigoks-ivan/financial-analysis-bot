#!/usr/bin/env python3
"""primary_docs 共用小工具：HTTP（節流＋重試＋計數）、文字計量／截斷、關鍵字挑段、item 組裝。

台股（primary_tw.py）與美股（primary_us.py）共用；零 LLM。契約見 primary_docs.py。
"""
from __future__ import annotations

import html as _html
import re
import time

HTTP_TIMEOUT = 20       # 秒；requests 的逾時是「兩次收到資料之間」，大檔下載不會被總時間砍
HTTP_RETRIES = 2        # 失敗再試 2 次（共 3 次）
HTTP_MIN_INTERVAL = 1.0  # 同一個程序內任兩次請求至少間隔（秒），含 SEC


class FetchError(Exception):
    """來源抓不到（網路、逾時、HTTP 錯誤）。上層記 note、略過該來源，不擋 DD。"""


class Http:
    """requests.Session 包一層：請求節流、逾時、重試、TLS reset 重建連線、請求計數。

    新版 MOPS 連打約 17 次會 TLS reset（探測實測），所以每次失敗都換新 Session 再試。
    """

    count = 0  # 整個程序的請求總數（開發期預算 300 次）

    def __init__(self, headers=None, min_interval=HTTP_MIN_INTERVAL):
        import requests
        self._requests = requests
        self.headers = dict(headers or {})
        self.min_interval = min_interval
        self._last = 0.0
        self.session = requests.Session()

    def _wait(self):
        gap = self.min_interval - (time.time() - self._last)
        if gap > 0:
            time.sleep(gap)

    def request(self, method, url, **kw):
        kw.setdefault("timeout", HTTP_TIMEOUT)
        hdrs = dict(self.headers)
        hdrs.update(kw.pop("headers", None) or {})
        last = None
        for attempt in range(HTTP_RETRIES + 1):
            self._wait()
            self._last = time.time()
            Http.count += 1
            try:
                r = self.session.request(method, url, headers=hdrs, **kw)
                self._last = time.time()
                if r.status_code >= 500 or r.status_code == 429:
                    last = FetchError("HTTP {0} {1}".format(r.status_code, url))
                else:
                    return r
            except self._requests.RequestException as e:
                last = FetchError("{0} {1}: {2}".format(type(e).__name__, url, str(e)[:100]))
                self.session = self._requests.Session()  # TLS reset 後舊連線不能再用
            time.sleep(2.0 * (attempt + 1))
        raise last

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        return self.request("POST", url, **kw)


# ---------------------------------------------------------------------------
# 文字計量：中文字一個單位、英文／數字詞一個單位（上限「約 2,500 中文字或 1,500 英文字」）
# ---------------------------------------------------------------------------

_UNIT_RE = re.compile(r"[㐀-鿿豈-﫿]|[A-Za-z0-9][A-Za-z0-9.,%'’\-/$]*")


def weight(text):
    return len(_UNIT_RE.findall(text or ""))


def clip_to_weight(text, limit, ellipsis="…"):
    """截到 limit 單位以內，盡量停在句號／換行；沒截就原樣回傳。"""
    text = text or ""
    if limit <= 0:
        return ""
    n = 0
    end = None
    for m in _UNIT_RE.finditer(text):
        n += 1
        if n > limit:
            end = m.start()
            break
    if end is None:
        return text
    cut = text[:end].rstrip()
    snap = max(cut.rfind("。"), cut.rfind("\n"), cut.rfind(". "), cut.rfind("；"))
    if snap > len(cut) * 0.6:
        cut = cut[:snap + 1].rstrip()
    return cut + ellipsis


def squash(text):
    """空白正規化：連續空白縮成一格，保留換行但去掉空行。"""
    lines = [re.sub(r"[ \t　\xa0]+", " ", ln).strip() for ln in (text or "").replace("\r", "").split("\n")]
    return "\n".join(ln for ln in lines if ln)


def one_line(text):
    return re.sub(r"\s+", " ", (text or "").replace("　", " ")).strip()


# ---------------------------------------------------------------------------
# item 與每軸預算
# ---------------------------------------------------------------------------

def mk_item(source, doc, url, as_of, section, text):
    return {"source": source, "doc": doc, "url": url, "as_of": as_of, "section": section, "text": text}


def enforce_budget(items, limit):
    """依序保留 item，累計超過 limit 單位就截斷當前這則、丟掉後面的。"""
    out = []
    used = 0
    for it in items:
        w = weight(it["text"])
        if used + w <= limit:
            out.append(it)
            used += w
            continue
        room = limit - used
        if room >= 60:  # 剩太少就不截半段，直接收尾
            it = dict(it)
            it["text"] = clip_to_weight(it["text"], room)
            out.append(it)
        break
    return out


# ---------------------------------------------------------------------------
# 關鍵字挑段
# ---------------------------------------------------------------------------

def score_text(text, rules):
    """rules＝[(compiled_regex, weight)]；每條規則最多算 3 次命中，避免長段落靠重複詞堆分。"""
    s = 0.0
    for rx, w in rules:
        s += w * min(3, len(rx.findall(text)))
    return s


def pick_paragraphs(paras, rules, budget, max_each=220, min_score=1.0, section_bonus=None, require=None, exclude=None,
                    max_sentence_words=None):
    """paras＝[(位置, 區段id, 文字)]；挑分數高的段落到 budget 單位為止，回傳依文件順序排列的
    [(區段id, 文字)]。每段超過 max_each 單位就截斷；區段加成用 section_bonus[區段id] 乘分；
    require／exclude 是段落必須符合／不得符合的 regex（濾掉「% of revenue」的獲利段、前瞻聲明等雜訊）；
    max_sentence_words：平均每句超過這個詞數的段落（沒標點的清單、圖表標題串在一起）直接略過。"""
    scored = []
    for pos, sec, text in paras:
        if section_bonus is not None and sec not in section_bonus:
            continue
        if require is not None and not require.search(text):
            continue
        if exclude is not None and exclude.search(text):
            continue
        if max_sentence_words:
            n_sent = max(1, len(re.findall(r"[.!?](?:\s|$)", text)))
            if weight(text) / n_sent > max_sentence_words:
                continue
        sc = score_text(text, rules) * (section_bonus or {}).get(sec, 1.0)
        if sc >= min_score:
            scored.append((sc, pos, sec, text))
    scored.sort(key=lambda t: (-t[0], t[1]))
    chosen, used = [], 0
    for sc, pos, sec, text in scored:
        t = clip_to_weight(text, max_each)
        w = weight(t)
        if used + w > budget:
            continue
        chosen.append((pos, sec, t))
        used += w
    chosen.sort(key=lambda t: t[0])
    return [(sec, t) for _pos, sec, t in chosen]


def html_to_text(raw):
    """HTML 轉純文字，保留段落換行（SEC 10-K／20-F 用）。"""
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    h = re.sub(r"(?is)<ix:header>.*?</ix:header>", " ", h)
    h = re.sub(r"(?i)</(p|div|tr|li|h[1-6]|table|section|ul|ol)>|<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</t[dh]>", "  ", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = _html.unescape(h)
    return squash(h)
