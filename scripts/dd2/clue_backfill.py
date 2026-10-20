#!/usr/bin/env python3
"""dd2 線索補原文：Stage 0 查證 agent 留下的線索（clues），由程式打開網頁補逐字原文。

病因（2026-10-19 台股五檔空軸普查）：每軸查證 agent 只收「可逐字引用原文」的 finding，98 個空軸裡
43 個的 note 寫著「有線索但沒拿到原文／日期」。持有人不加 agent 輪數（成本），改由程式零 LLM 成本補抓。

契約：
  agent 在 parts/axes_{k}.json 的 coverage.{axis}.clues 放
      {"claim","source"?,"url","as_of","direction"?,"affects"?,"match_terms":[2～5 個預期原文逐字出現的字串]}
  backfill(run_dir)：
    1. GET url（HTML 去 script／style；PDF 走 pdftotext；Big5／UTF-8／GB 自動判；跟隨轉址），快取在 run_dir/fetch_cache/。
    2. 在全文找一段（約 400 字窗）同時含 match_terms 的多數（≥2 且 ≥ 一半；數字精確比對，容許全形半形與千分位差異）。
    3. 命中：升級為 finding——excerpt＝那段原文（不改寫）、excerpt_from="page"、excerpt_source="program_fetch"；
       該軸原為 none 則改 found。頁面有可解析的發布日期（meta／JSON-LD，或開頭的日期＋時分戳記）且與 agent 填的不同，
       用頁面日期並記 as_of_note。
    4. 沒命中：丟棄。每個處理過線索的軸，note 末尾追加「線索 N 條，程式核實 M 條」。
  clues 一律從 part 拿掉（核實不了的線索不進證據包）；原始 part 備份在 parts/_pre_backfill/。
  每次執行最多處理 20 個不同網址；網址請求間隔 ≥1 秒、逾時 15 秒。寧缺勿錯：不確定就丟。

另有 rescue_undated(part, cache_dir)：stage0 驗 part 之前先救「有 url、沒有可解析 as_of」的 finding——
  抓頁、讀頁面上真有的發布日（meta／JSON-LD／開頭日期戳記）填進 as_of 並加 as_of_note；讀不到就照舊交給
  run.py 的 _drop_undated_findings 丟棄。不推估日期、不用抓取當天。每次執行最多 15 個網址（與 backfill 的 20 分開算）。

用法（手動）：python3 scripts/dd2/clue_backfill.py RUN_DIR
Python 3.9 相容（不用 `match`、不用 `X | None`）。
"""
import codecs
import datetime
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from bisect import bisect_left
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_evidence  # noqa: E402  finding 必填欄位／日期解析的單一來源

MAX_URLS = 20            # 每次執行最多處理幾個不同網址
RESCUE_MAX_URLS = 15     # 補 as_of 的網址上限（與 MAX_URLS 分開算；整個 stage0 共用）
FETCH_TIMEOUT = 15       # 單次請求逾時（秒）
FETCH_DEADLINE = 30      # 一個網址從連線到讀完的總上限（秒），防慢速滴灌
MIN_INTERVAL = 1.0       # 兩次網路請求最短間隔（秒）
WINDOW = 400             # 比對窗（原文字元數）
MIN_EXCERPT = 150        # 摘錄至少約這麼長（命中句太短時往後補句）
MIN_CACHE_CHARS = 150    # 頁面文字少於此數不快取
MAX_BYTES = 20 * 1024 * 1024
MAX_TEXT = 2000000
PDF_TIMEOUT = 60
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

_last_request = [0.0]
_ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad"))  # 看不見的字元：不影響閱讀，會擋掉比對


# ---------------------------------------------------------------------------
# 抓取：HTML／PDF → 純文字
# ---------------------------------------------------------------------------

_BLOCK_TAGS = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article",
               "table", "ul", "ol", "dl", "dt", "dd", "blockquote", "pre", "hr", "header", "main",
               "figure", "figcaption"}
_ALWAYS_SKIP = {"script", "style", "noscript", "template", "svg", "head", "iframe", "ix:header"}  # ix:header＝SEC iXBRL 隱藏標籤區
_VOID_TAGS = {"br", "hr", "img", "input", "meta", "link", "source", "area", "base", "col", "embed", "wbr"}
_HIDDEN_STYLE = re.compile(r"display\s*:\s*none", re.I)
_BOILER_SKIP = {"nav", "footer", "aside"}
_DATE_META_KEYS = {"article:published_time", "og:article:published_time", "pubdate", "publishdate",
                   "publish_date", "date", "dc.date", "dc.date.issued", "article.published",
                   "parsely-pub-date", "sailthru.date", "datepublished"}


class _TextExtractor(HTMLParser):
    """HTML → 純文字；順便撈 meta／time 裡的發布日期。"""

    def __init__(self, skip_boilerplate):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.skip = set(_ALWAYS_SKIP) | (_BOILER_SKIP if skip_boilerplate else set())
        self.depth = {}
        self.parts = []
        self.date_candidates = []
        self.hidden = None  # [標籤名／巢狀深度]：display:none／hidden 屬性的元素內文不算頁面內容

    def _skipping(self):
        return self.hidden is not None or any(v > 0 for v in self.depth.values())

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (a.get("property") or a.get("name") or a.get("itemprop") or "").strip().lower()
            if key in _DATE_META_KEYS and a.get("content"):
                self.date_candidates.append(a["content"])
        elif tag == "time" and a.get("itemprop", "").lower() == "datepublished" and a.get("datetime"):
            self.date_candidates.append(a["datetime"])
        if self.hidden is not None:
            if tag == self.hidden[0]:
                self.hidden[1] += 1
            return
        if tag not in _VOID_TAGS and ("hidden" in a or _HIDDEN_STYLE.search(a.get("style", ""))):
            self.hidden = [tag, 1]
            return
        if tag == "body":  # 沒閉合的 <head> 不能吞掉整個 body
            self.depth["head"] = 0
        if tag in self.skip:
            self.depth[tag] = self.depth.get(tag, 0) + 1
        elif not self._skipping():
            if tag in _BLOCK_TAGS:
                self.parts.append("\n")
            elif tag in ("td", "th"):
                self.parts.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag == "br" and not self._skipping():
            self.parts.append("\n")
        elif tag == "meta":
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self.hidden is not None:
            if tag == self.hidden[0]:
                self.hidden[1] -= 1
                if self.hidden[1] == 0:
                    self.hidden = None
            return
        if tag in self.skip and self.depth.get(tag, 0) > 0:
            self.depth[tag] -= 1
        elif not self._skipping() and tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skipping():  # 原始碼裡的換行只是空白，真正的分段由區塊標籤產生
            self.parts.append(re.sub(r"[ \t\r\n\u00a0\u3000]+", " ", data.translate(_ZERO_WIDTH)))

    def text(self):
        return _squeeze("".join(self.parts))


def _squeeze(text):
    """行內空白收成一格、丟空行（保留換行當句界）。"""
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t\u00a0\u3000]+", " ", line.translate(_ZERO_WIDTH)).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def _parse_page_date(s):
    """頁面發布日：只認完整年月日；晚於明天的視為壞值。回 YYYY-MM-DD 或 None。"""
    if not isinstance(s, str):
        return None
    m = (re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
         or re.search(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日", s))
    if not m:
        return None
    try:
        d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    if d > datetime.date.today() + datetime.timedelta(days=1):
        return None
    return d.isoformat()


_MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
           "nov": 11, "dec": 12}
_DATELINE_RES = [
    re.compile(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\s*,?\s*\d{1,2}:\d{2}"),
    re.compile(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日\s*(?:\(?[週周星期一二三四五六日]{1,3}\)?\s*)?\d{1,2}:\d{2}"),
]
_DATELINE_EN = re.compile(r"\b([A-Z][a-z]{2,8})\.?\s+(\d{1,2}),\s*(\d{4})\s+\d{1,2}:\d{2}")


def _dateline(text):
    """沒有 meta 日期時，認頁面開頭 600 字內『日期＋時分』的時間戳記（新聞頁標題後面幾乎都有）。"""
    head = text[:600]
    hits = []
    for rx in _DATELINE_RES:
        m = rx.search(head)
        if m:
            hits.append((m.start(), m.group(0)))
    m = _DATELINE_EN.search(head)
    if m and m.group(1)[:3].lower() in _MONTHS:
        hits.append((m.start(), "{0}-{1}-{2}".format(m.group(3), _MONTHS[m.group(1)[:3].lower()], m.group(2))))
    for _, raw in sorted(hits):
        d = _parse_page_date(raw)
        if d:
            return d
    return None


def html_to_text(html_text):
    """回 (純文字／頁面發布日或 None)。先去 nav／footer／aside；若去完只剩不到三成（標籤沒閉合）就退回不去。"""
    full = _TextExtractor(False)
    full.feed(html_text)
    full.close()
    lean = _TextExtractor(True)
    lean.feed(html_text)
    lean.close()
    text = lean.text()
    full_text = full.text()
    if len(text) < 0.3 * len(full_text):
        text = full_text
    cands = list(full.date_candidates)
    cands += re.findall(r'"datePublished"\s*:\s*"([^"]+)"', html_text)
    page_date = None
    for c in cands:
        page_date = _parse_page_date(c)
        if page_date:
            break
    return text, page_date or _dateline(text)


_BIG5 = ("big5", "big5-hkscs", "big5hkscs", "cp950", "ms950")
_GB = ("gb2312", "gbk", "gb18030")


def _canon_charset(cs):
    cs = (cs or "").strip().strip("\"'").lower()
    if not cs:
        return []
    if cs in _BIG5:
        return ["cp950", "big5hkscs"]
    if cs in _GB:
        return ["gb18030"]
    if cs in ("iso-8859-1", "latin1", "latin-1", "us-ascii", "ascii", "windows-1252"):
        return []  # 預設值常是謊話，不當證據
    try:
        return [codecs.lookup(cs).name]
    except LookupError:
        return []


def decode_body(body, header_charset=None):
    """BOM → HTTP 標頭 → meta charset → 猜（utf-8 嚴格，再 Big5／GB）；都不行才 utf-8 容錯。"""
    if body.startswith(b"\xef\xbb\xbf"):
        return body[3:].decode("utf-8", "replace")
    declared = list(_canon_charset(header_charset))
    m = re.search(rb"<meta[^>]+charset\s*=\s*[\"']?\s*([A-Za-z0-9_\-]+)", body[:8192], re.I)
    if m:
        declared += _canon_charset(m.group(1).decode("ascii", "ignore"))
    for enc in declared + ["utf-8", "cp950", "big5hkscs", "gb18030"]:
        try:
            return body.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return body.decode(declared[0] if declared else "utf-8", "replace")


def _url_ok(url):
    """只放行 http／https，擋 localhost 與內網字面 IP（網址來自 LLM 輸出，不能被拿去打內部服務）。"""
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return False
    host = p.hostname.lower()
    if host == "localhost" or host.endswith(".local"):
        return False
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_global
    except ValueError:
        return True


def _clean_url(url):
    """去頭尾空白、去 #fragment；沒寫 scheme 但像網域路徑的補 https://。"""
    u = (url or "").strip()
    if u and not re.match(r"^[A-Za-z][A-Za-z0-9+.\-]*://", u) and re.match(r"^[\w\-]+(\.[\w\-]+)+(/|$)", u):
        u = "https://" + u
    return urldefrag(u)[0]


def _url_key(url):
    """比對『是不是同一網址』用：host 小寫、去尾端斜線與 fragment。"""
    p = urlparse(_clean_url(url))
    return (p.hostname or "").lower() + (p.path or "").rstrip("/") + ("?" + p.query if p.query else "")


def _throttle():
    wait = MIN_INTERVAL - (time.monotonic() - _last_request[0])
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()


def _pdf_to_text(body):
    exe = shutil.which("pdftotext")
    if not exe:
        return None, "找不到 pdftotext"
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
        tf.write(body)
        tmp = tf.name
    try:
        r = subprocess.run([exe, "-enc", "UTF-8", "-nopgbrk", tmp, "-"], capture_output=True, timeout=PDF_TIMEOUT)
        if r.returncode != 0:
            return None, "pdftotext 失敗 rc={0}".format(r.returncode)
        return r.stdout.decode("utf-8", "replace"), None
    except subprocess.TimeoutExpired:
        return None, "pdftotext 逾時"
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _headers_for(url):
    host = (urlparse(url).hostname or "").lower()
    if host.endswith("sec.gov"):  # SEC 要求帶聯絡資訊的 UA，沿用 numbers 抓取同一組
        try:
            from dd_numbers_extra import SEC_HEADERS
            return dict(SEC_HEADERS)
        except Exception:
            pass
    return {"User-Agent": UA, "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.5"}


def fetch_text(url, cache_dir=None):
    """抓一個網址 → {"ok","text","page_date","final_url","kind","cached","error"}。成功的結果快取。"""
    url = _clean_url(url)
    cache_path = None
    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_path = cache_dir / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ".json")
        if cache_path.exists():
            try:
                c = json.loads(cache_path.read_text(encoding="utf-8"))
                c.update(ok=True, cached=True)
                return c
            except (OSError, ValueError):
                pass
    out = {"ok": False, "text": "", "page_date": None, "final_url": url, "kind": None, "cached": False,
           "error": None}
    if not _url_ok(url):
        out["error"] = "網址不合規（非 http/https 或內網）"
        return out
    try:
        import requests
        _throttle()
        deadline = time.monotonic() + FETCH_DEADLINE
        r = requests.get(url, headers=_headers_for(url), timeout=FETCH_TIMEOUT, allow_redirects=True, stream=True)
        try:
            out["final_url"] = r.url
            if r.status_code != 200:
                out["error"] = "HTTP {0}".format(r.status_code)
                return out
            ctype = (r.headers.get("Content-Type") or "").lower()
            m = re.search(r"charset\s*=\s*([^\s;]+)", ctype)
            charset = m.group(1) if m else None
            buf = bytearray()
            for chunk in r.iter_content(65536):
                buf += chunk
                if len(buf) > MAX_BYTES or time.monotonic() > deadline:
                    break
        finally:
            r.close()
        body = bytes(buf)
        if "application/pdf" in ctype or body[:5] == b"%PDF-":
            text, err = _pdf_to_text(body)
            if text is None:
                out["error"] = err
                return out
            out.update(kind="pdf", text=_squeeze(text)[:MAX_TEXT])
        else:
            decoded = decode_body(body, charset)
            if "text/plain" in ctype:
                out.update(kind="text", text=_squeeze(decoded)[:MAX_TEXT])
            else:
                text, page_date = html_to_text(decoded)
                out.update(kind="html", text=text[:MAX_TEXT], page_date=page_date)
    except Exception as exc:  # 逾時、連線失敗、解析失敗一律記錄，不往上炸
        out["error"] = "{0}: {1}".format(type(exc).__name__, str(exc)[:120])
        return out
    out["ok"] = bool(out["text"].strip())
    if not out["ok"]:
        out["error"] = "頁面沒有可讀文字"
        return out
    if cache_path and len(out["text"]) >= MIN_CACHE_CHARS:  # 文字太少多半是 JS 外殼頁（Loading...），不快取，下次重抓
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            rec = {k: out[k] for k in ("text", "page_date", "final_url", "kind")}
            rec["url"] = url
            rec["fetched_at"] = datetime.datetime.now().isoformat(timespec="seconds")
            cache_path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
    return out


# ---------------------------------------------------------------------------
# 比對：在全文找同時含多數 match_terms 的一段
# ---------------------------------------------------------------------------

def _isd(c):
    return "0" <= c <= "9"


def _norm_char(ch):
    o = ord(ch)
    if 0xFF01 <= o <= 0xFF5E:  # 全形 ASCII → 半形
        ch = chr(o - 0xFEE0)
    elif o == 0x3000:
        ch = " "
    low = ch.lower()
    return low if len(low) == 1 else ch


def _normalize(text):
    """回 (norm, idx)：norm 去空白、全形轉半形、轉小寫、去數字間千分位逗號；idx[i]＝norm[i] 在原文的位置。"""
    out, idx = [], []
    n = len(text)
    for i, ch in enumerate(text):
        c = _norm_char(ch)
        if c.isspace() or ord(c) in _ZERO_WIDTH:
            continue
        if c == "," and out and _isd(out[-1]) and i + 3 < n \
                and all(_isd(_norm_char(text[i + k])) for k in (1, 2, 3)) \
                and not (i + 4 < n and _isd(_norm_char(text[i + 4]))):
            continue
        out.append(c)
        idx.append(i)
    return "".join(out), idx


def _boundary_ok(norm, start, end, term):
    """數字詞要精確：39 不能是 139、3.9、39.5 的一部分。"""
    if _isd(term[0]) and start > 0:
        p = norm[start - 1]
        if _isd(p) or (p == "." and start > 1 and _isd(norm[start - 2])):
            return False
    if _isd(term[-1]) and end < len(norm):
        nx = norm[end]
        if _isd(nx) or (nx == "." and end + 1 < len(norm) and _isd(norm[end + 1])):
            return False
    return True


def _weak_term(t):
    """單字、單純年份、1～2 位裸數字：到處都有，不能當核實依據。"""
    return len(t) < 2 or bool(re.fullmatch(r"(19|20)\d{2}", t)) or bool(re.fullmatch(r"\d{1,2}", t))


_SENT_END = re.compile(r"[。！？；\n]|[.!?;](?=\s|$)")
_CLAUSE_END = re.compile(r"[，、：,:]|\s")  # 找不到句界時退而求其次，至少不從字中間切


def find_window(text, terms, window=WINDOW):
    """回 {"start","end","hits","total"} 或 None。start／end 是 text 原文座標。
    規則：去掉弱詞（見 _weak_term）後至少 2 個詞；窗內命中 ≥2 且 ≥ 一半。"""
    uniq = {}
    for t in terms:
        if not isinstance(t, str):
            continue
        nt = _normalize(t)[0]
        if nt and not _weak_term(nt) and nt not in uniq:
            uniq[nt] = t.strip()
    if len(uniq) < 2:
        return None
    norm, idx = _normalize(text)
    occ = {}
    for nt in uniq:
        lst, pos = [], 0
        while len(lst) < 3000:
            j = norm.find(nt, pos)
            if j < 0:
                break
            e = j + len(nt)
            if _boundary_ok(norm, j, e, nt):
                lst.append((idx[j], idx[e - 1] + 1))
            pos = j + 1
        if lst:
            occ[nt] = lst
    if len(occ) < 2:
        return None
    starts = {nt: [s for s, _ in lst] for nt, lst in occ.items()}
    best = None  # (命中數／-起點) 越大越好：命中數最多者取最早的，內文通常在頁尾標籤／相關新聞之前
    for lst in occ.values():
        for s, _ in lst:
            chosen = {}
            for nt, lst2 in occ.items():
                k = bisect_left(starts[nt], s)
                while k < len(lst2) and lst2[k][0] - s <= window:
                    if lst2[k][1] - s <= window:
                        chosen[nt] = lst2[k]
                        break
                    k += 1
            if len(chosen) < 2 or len(chosen) * 2 < len(uniq):
                continue
            span_end = max(e for _, e in chosen.values())
            key = (len(chosen), -s)
            if best is None or key > best[0]:
                best = (key, s, span_end, sorted(uniq[nt] for nt in chosen))
    if best is None:
        return None
    _, s, span_end, hits = best
    return {"start": s, "end": span_end, "hits": hits, "total": len(uniq)}


def make_excerpt(text, start, end, window=WINDOW):
    """以命中範圍為中心補前後文到約 window 字，起訖貼到句界；只截取不改寫（換行併成空格）。"""
    pad = max(0, (window - (end - start)) // 2)
    a, b = max(0, start - pad), min(len(text), end + pad)
    last = None
    for m in _SENT_END.finditer(text, a, start):
        last = m
    if last is not None:
        a = last.end()
    elif a > 0:
        m = _CLAUSE_END.search(text, a, start)
        if m is not None:
            a = m.end()
    limit = b
    m = _SENT_END.search(text, end, b)
    if m is not None:
        b = m.end()
    elif b < len(text):
        last = None
        for last in _CLAUSE_END.finditer(text, end, b):
            pass
        if last is not None:
            b = last.start()
    while b - a < MIN_EXCERPT and b < limit:  # 命中句太短（例如只有標題）就往後多取幾句，不超過窗
        m = _SENT_END.search(text, b, limit)
        if m is None:
            break
        b = m.end()
    return re.sub(r"\s*\n\s*", " ", text[a:b]).strip()


# ---------------------------------------------------------------------------
# backfill 主流程
# ---------------------------------------------------------------------------

def _num_key(p):
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def _atomic_write_json(path, obj):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _axis_affects(run_dir):
    """axes.json 的各軸 affects，給沒填 affects 的線索當預設。"""
    try:
        axes = json.loads((run_dir / "axes.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if isinstance(axes, dict):
        axes = axes.get("axes") or []
    return {a.get("id"): a.get("affects") for a in axes if isinstance(a, dict) and a.get("affects")}


def _host(url):
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def _full_date(s):
    m = re.match(r"\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s or "")
    return "{0}-{1:02d}-{2:02d}".format(*(int(x) for x in m.groups())) if m else None


def _pick_as_of(agent_as_of, page_date):
    """回 (as_of, as_of_note)。頁面有完整發布日且與 agent 不同 → 用頁面日期並註記；
    agent 日期缺漏或只到月／年（頁面日期落在其內）時，頁面日期只是補全，不註記。"""
    if not page_date:
        return agent_as_of, None
    agent_full = _full_date(agent_as_of)
    if agent_full == page_date:
        return agent_as_of, None
    if validate_evidence.parse_date(agent_as_of) is None \
            or (agent_full is None and page_date.startswith((agent_as_of or "").strip().replace("/", "-"))):
        return page_date, None
    return page_date, "agent 原填 {0}，採頁面日期".format(agent_as_of)


def _build_finding(clue, axis_id, hit_text, page_date, default_affects):
    """線索＋命中原文 → finding；欄位不齊回 (None, 原因)。"""
    as_of, as_of_note = _pick_as_of(clue.get("as_of"), page_date)
    if validate_evidence.parse_date(as_of) is None:
        return None, "no_date"
    direction = clue.get("direction") if clue.get("direction") in validate_evidence.VALID_DIRECTIONS else "0"
    affects = clue.get("affects")
    if not (isinstance(affects, list) and affects and all(isinstance(x, str) and x for x in affects)):
        affects = list(default_affects or [axis_id])
    source = clue.get("source") if isinstance(clue.get("source"), str) and clue.get("source").strip() \
        else _host(_clean_url(clue["url"]))
    f = {"claim": clue["claim"].strip(), "source": source, "url": _clean_url(clue["url"]),
         "excerpt": hit_text, "excerpt_from": "page", "excerpt_source": "program_fetch",
         "as_of": as_of, "direction": direction, "affects": affects}
    if as_of_note:
        f["as_of_note"] = as_of_note
    return f, None


_KEEP_AS_SNIPPET = ("no_match", "fetch_failed", "over_limit")


def _keep_as_snippet(clue, axis_id, axis_obj, existing, default_affects):
    """核實不到的線索 → snippet finding（excerpt=null、excerpt_source=search_summary）；
    日期不可解析、網址已在 findings 就不收。回是否收進。"""
    if not _valid_clue(clue) or not _url_ok(_clean_url(clue["url"])):
        return False
    key = _url_key(_clean_url(clue["url"]))
    if key in existing or validate_evidence.parse_date(clue.get("as_of")) is None:
        return False
    f, _ = _build_finding(clue, axis_id, None, None, default_affects)
    if f is None:
        return False
    f.update({"excerpt": None, "excerpt_from": "snippet", "excerpt_source": "search_summary"})
    axis_obj.setdefault("findings", []).append(f)
    existing.add(key)
    if axis_obj.get("status") == "none":
        axis_obj["status"] = "found"
    return True


def _valid_clue(c):
    return (isinstance(c, dict) and isinstance(c.get("url"), str) and c["url"].strip()
            and isinstance(c.get("claim"), str) and c["claim"].strip()
            and isinstance(c.get("match_terms"), list))


def backfill(run_dir, max_urls=MAX_URLS, fetch=None):
    """處理 run_dir/parts/axes_*.json 的 clues，回傳統計 dict（見檔頭契約）。
    fetch(url)->fetch_text 同形 dict，測試注入用；預設真的上網（快取在 run_dir/fetch_cache/）。"""
    run_dir = Path(run_dir)
    parts_dir = run_dir / "parts"
    cache_dir = run_dir / "fetch_cache"
    if fetch is None:
        def fetch(u):
            return fetch_text(u, cache_dir)
    stats = {"clues": 0, "urls": 0, "fetched": 0, "cache_hits": 0, "fetch_failed": 0, "verified": 0,
             "kept_snippet": 0, "discarded": 0, "duplicate": 0, "over_limit": 0, "axes_upgraded": [], "details": []}
    if not parts_dir.exists():
        return stats
    loaded = []  # (part_path, obj, [(axis_id, axis_obj, [clue,...])])
    for p in sorted(parts_dir.glob("axes_*.json"), key=_num_key):
        if not re.fullmatch(r"axes_\d+\.json", p.name):
            continue
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        axes = []
        for axis_id, axis_obj in ((obj.get("coverage") or {}) if isinstance(obj, dict) else {}).items():
            if isinstance(axis_obj, dict) and isinstance(axis_obj.get("clues"), list) and axis_obj["clues"]:
                axes.append((axis_id, axis_obj, axis_obj["clues"]))
        if axes:
            loaded.append((p, obj, axes))
    if not loaded:
        return stats
    default_affects = _axis_affects(run_dir)

    seen_urls = {}  # url_key → 處理順位；超過 max_urls 的網址不處理
    results = {}    # url_key → fetch 結果
    for p, obj, axes in loaded:
        for axis_id, axis_obj, clues in axes:
            n_clues = len(clues)
            stats["clues"] += n_clues
            verified = 0
            kept = 0
            existing = {_url_key(f.get("url")) for f in (axis_obj.get("findings") or [])
                        if isinstance(f, dict) and isinstance(f.get("url"), str)}
            for clue in clues:
                detail = {"axis": axis_id, "url": clue.get("url") if isinstance(clue, dict) else None}
                stats["details"].append(detail)
                try:
                    outcome = _process_clue(clue, axis_id, axis_obj, existing, seen_urls, results, fetch,
                                            stats, max_urls, default_affects, detail)
                except Exception as exc:  # 單條線索炸掉＝丟棄，不影響其他
                    outcome = "error"
                    detail["error"] = "{0}: {1}".format(type(exc).__name__, str(exc)[:120])
                detail["outcome"] = outcome
                if outcome == "verified":
                    verified += 1
                    stats["verified"] += 1
                elif outcome in _KEEP_AS_SNIPPET and _keep_as_snippet(clue, axis_id, axis_obj, existing,
                                                                     default_affects.get(axis_id)):
                    # 只加不減：核實不到的線索照改版前的 snippet finding 保留（excerpt=null），
                    # 不因改走 clues 而比改版前少證據（2383.TW 2026-10-20：28→16 條）
                    kept += 1
                    stats["kept_snippet"] += 1
                    detail["kept_as"] = "snippet"
                else:
                    stats["discarded"] += 1
            if verified and axis_id not in stats["axes_upgraded"]:
                stats["axes_upgraded"].append(axis_id)
            note = (axis_obj.get("note") or "").rstrip()
            axis_obj["note"] = (note + " " if note else "") + "線索 {0} 條，程式核實 {1} 條".format(n_clues, verified) \
                + ("，{0} 條以搜尋摘要保留（未核原文）".format(kept) if kept else "")
            del axis_obj["clues"]  # 核實不了的線索不進證據包
            # agent 只交 clues 卻填 found（2383.TW 2026-10-20 供需軸）：線索全沒核實就是空軸，
            # 留 found＋空 findings 會被 validate_evidence 判不合格、整軸記成 incomplete
            if axis_obj.get("status") == "found" and not axis_obj.get("findings"):
                axis_obj["status"] = "none"

    backup_dir = parts_dir / "_pre_backfill"
    for p, obj, axes in loaded:
        backup_dir.mkdir(exist_ok=True)
        if not (backup_dir / p.name).exists():  # 重跑不覆蓋最初的原檔
            shutil.copy2(str(p), str(backup_dir / p.name))
        _atomic_write_json(p, obj)
    try:
        cache_dir.mkdir(exist_ok=True)
        _atomic_write_json(cache_dir / "backfill_log.json", stats["details"])
    except OSError:
        pass
    stats["urls"] = len(results)
    return stats


def _process_clue(clue, axis_id, axis_obj, existing, seen_urls, results, fetch, stats, max_urls,
                  default_affects, detail):
    """處理單條線索；命中就把 finding 加進 axis_obj。回 outcome 字串。"""
    if not _valid_clue(clue):
        return "invalid"
    url = _clean_url(clue["url"])
    key = _url_key(url)
    if not _url_ok(url):
        return "bad_url"
    if key in existing:
        stats["duplicate"] += 1
        return "duplicate"
    if key not in seen_urls:
        if len(seen_urls) >= max_urls:
            stats["over_limit"] += 1
            return "over_limit"
        seen_urls[key] = len(seen_urls)
        res = fetch(url) or {"ok": False, "error": "fetch 無回傳"}
        results[key] = res
        if res.get("ok"):
            stats["cache_hits" if res.get("cached") else "fetched"] += 1
        else:
            stats["fetch_failed"] += 1
    res = results[key]
    if not res.get("ok"):
        detail["error"] = res.get("error")
        return "fetch_failed"
    text = res.get("text") or ""
    win = find_window(text, clue["match_terms"])
    if win is None:
        return "no_match"
    excerpt = make_excerpt(text, win["start"], win["end"])
    f, why = _build_finding(clue, axis_id, excerpt, res.get("page_date"), default_affects.get(axis_id))
    if f is None:
        return why
    detail["hits"] = win["hits"]
    findings = axis_obj.setdefault("findings", [])
    if any(isinstance(x, dict) and x.get("excerpt") == excerpt for x in findings):
        stats["duplicate"] += 1
        return "duplicate"
    findings.append(f)
    if axis_obj.get("status") == "none":
        axis_obj["status"] = "found"
    return "verified"


_rescue_seen = {}  # str(cache_dir) → 已處理的網址 key；同一個 python 程序（一次 stage0）共用上限


def _rescuable(f):
    """有網址、as_of 缺或無法解析、其餘必填欄位齊全的 finding 才值得救（欄位不齊救了也過不了驗證）。"""
    if not isinstance(f, dict) or validate_evidence.parse_date(f.get("as_of")) is not None:
        return False
    url = f.get("url")
    if not isinstance(url, str) or not _url_ok(_clean_url(url)):
        return False
    return bool(f.get("claim") and f.get("source")
                and f.get("direction") in validate_evidence.VALID_DIRECTIONS
                and isinstance(f.get("affects"), list) and f["affects"])


def rescue_undated(part, cache_dir=None, fetch=None, max_urls=RESCUE_MAX_URLS):
    """救 part 裡沒有可解析 as_of 的 finding：抓頁、取頁面發布日填 as_of（加 as_of_note）。
    取不到頁面日期的不動，留給 _drop_undated_findings。回統計 dict；原檔備份在 parts/_pre_backfill/。"""
    part = Path(part)
    stats = {"rescued": 0, "no_date": 0, "fetch_failed": 0, "over_limit": 0, "details": []}
    try:
        d = json.loads(part.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return stats
    cands = []
    for key in ("coverage", "events"):
        for axis_id, v in ((d.get(key) or {}) if isinstance(d, dict) else {}).items():
            for f in (v.get("findings") or []) if isinstance(v, dict) else []:
                if _rescuable(f):
                    cands.append((axis_id, f))
    if not cands:
        return stats
    if fetch is None:
        def fetch(u):
            return fetch_text(u, cache_dir)
    seen = _rescue_seen.setdefault(str(cache_dir), {})
    for axis_id, f in cands:
        url = _clean_url(f["url"])
        key = _url_key(url)
        detail = {"axis": axis_id, "url": url}
        stats["details"].append(detail)
        if key not in seen:
            if len(seen) >= max_urls:
                stats["over_limit"] += 1
                detail["outcome"] = "over_limit"
                continue
            try:
                seen[key] = fetch(url) or {"ok": False, "error": "fetch 無回傳"}
            except Exception as exc:
                seen[key] = {"ok": False, "error": "{0}: {1}".format(type(exc).__name__, str(exc)[:120])}
        res = seen[key]
        if not res.get("ok"):
            stats["fetch_failed"] += 1
            detail["outcome"] = "fetch_failed"
            detail["error"] = res.get("error")
        elif not res.get("page_date"):
            stats["no_date"] += 1
            detail["outcome"] = "no_date"
        else:
            f["as_of"] = res["page_date"]
            f["as_of_note"] = "頁面發布日（程式補）"
            stats["rescued"] += 1
            detail["outcome"] = "rescued"
            detail["as_of"] = res["page_date"]
    if stats["rescued"]:
        backup_dir = part.parent / "_pre_backfill"
        backup_dir.mkdir(exist_ok=True)
        if not (backup_dir / part.name).exists():
            shutil.copy2(str(part), str(backup_dir / part.name))
        _atomic_write_json(part, d)
    return stats


def main(argv):
    if len(argv) != 1:
        print("用法：clue_backfill.py RUN_DIR")
        return 2
    st = backfill(argv[0])
    print(json.dumps({k: v for k, v in st.items() if k != "details"}, ensure_ascii=False, indent=2))
    for d in st["details"]:
        print("  {axis:36s} {outcome:12s} {url}".format(axis=d["axis"], outcome=d.get("outcome", "?"),
                                                      url=d.get("url")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
