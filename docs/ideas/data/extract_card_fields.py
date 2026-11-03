#!/usr/bin/env python3
"""從各想法頁抽出卡片用的 conclusion／caution，寫回 docs/ideas/ideas.json。

conclusion：頁面 <div class="thesis"> 的原句；超過 90 字截到第一個句號。
caution：頁面 <ul class="kill"> 第一條裡含「若」的那句起，到該條結束（「若 X，收回」）。
只加欄位，不動其他欄位。抽不到的列在輸出，手動補進 ideas.json。
用法：python3 docs/ideas/data/extract_card_fields.py [--force]
預設只補沒有這兩個欄位的想法；--force 全部重抽（會蓋掉手動補的值）。
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDEAS_DIR = os.path.dirname(HERE)
PATH = os.path.join(IDEAS_DIR, "ideas.json")
LIMIT = 90


def text_of(frag):
    frag = re.sub(r"<[^>]+>", "", frag)
    return re.sub(r"\s+", " ", html.unescape(frag)).strip()


def sentences(s):
    return [x for x in re.findall(r"[^。！？]+[。！？]?", s) if x.strip()]


def conclusion(page):
    m = re.search(r'<div class="thesis">(.*?)</div>', page, re.S)
    if not m:
        return None
    t = text_of(m.group(1))
    if len(t) <= LIMIT:
        return t
    return sentences(t)[0].strip()


def caution(page):
    m = re.search(r'<ul class="kill">(.*?)</ul>', page, re.S)
    if not m:
        return None
    lis = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
    if not lis:
        return None
    t = text_of(lis[0])
    ss = sentences(t)
    for i, s in enumerate(ss):
        if s.lstrip().startswith("若"):
            return "".join(ss[i:]).strip()
    return None


def main():
    force = "--force" in sys.argv
    data = json.load(open(PATH, encoding="utf-8"))
    miss = []
    for it in data["ideas"]:
        if not force and it.get("conclusion") and it.get("caution"):
            continue
        fp = os.path.join(IDEAS_DIR, os.path.basename(it["url"].rstrip("/")))
        if not fp.endswith(".html"):
            fp += ".html"
        if not os.path.exists(fp):
            miss.append((it["id"], "找不到頁面 " + fp))
            continue
        page = open(fp, encoding="utf-8").read()
        c, w = conclusion(page), caution(page)
        if c:
            it["conclusion"] = c
        else:
            miss.append((it["id"], "conclusion"))
        if w:
            it["caution"] = w
        else:
            miss.append((it["id"], "caution"))
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for i, w in miss:
        print("抽不到：", i, w)
    print("完成，抽不到 %d 項" % len(miss))


if __name__ == "__main__":
    main()
