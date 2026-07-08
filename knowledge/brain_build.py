#!/usr/bin/env python3
"""
brain_build.py — 第二大腦 orchestrator（衍生物全部 gitignore，本機重建）。

一條 pipeline 三形態輸出：
  1. knowledge/vault/auto/**.md   Obsidian vault（[[wiki-link]] 互連）
  2. knowledge/brain.db           FTS5 全文索引（q.py --search 用）
  3. knowledge/wiki/**.html       本機 wiki（brain_wiki.py 渲染，存在才跑）

增量：brain_cache.json 記每個來源檔 mtime+size 與 note 摘要，未變檔直接跳過
（hub 頁 / FTS notes 表 / wiki index 從 cache 摘要重生，不需重讀全文）。
來源消失 → 對應筆記 / FTS row / wiki 頁一併清掉。

用法：
  python knowledge/brain_build.py            # 增量 build（vault + FTS + wiki）
  python knowledge/brain_build.py --stats    # build + 各家族計數 / 解析降級統計
  python knowledge/brain_build.py --full     # 忽略 cache 全量重抽
  python knowledge/brain_build.py --no-wiki  # 跳過 wiki 渲染
"""
import json
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

KDIR = Path(__file__).resolve().parent
REPO = KDIR.parent
sys.path.insert(0, str(KDIR))
import brain_extract as bx  # noqa: E402

VAULT = KDIR / "vault"
AUTO = VAULT / "auto"
NOTES_DIR = VAULT / "notes"          # 用戶手寫筆記（committed），build 不動它
CACHE = KDIR / "brain_cache.json"
DB = KDIR / "brain.db"
GRAPH = KDIR / "graph.json"
CACHE_VERSION = 4  # v4: extra 擴為全覆蓋體質欄（moat 三分/品質/持久度/倍數/分位）

# note type → vault/auto 下的子目錄
TYPE_DIR = {
    "dd": "dd", "dca": "dca", "id": "id", "earnings": "earnings",
    "comparison": "comparisons", "synthesis": "synthesis", "monitor": "monitors",
    "supplychain": "supply-chain", "briefing": "briefing", "weekly": "weekly",
    "qgm": "qgm", "strategy": "strategy", "internal-note": "internal",
    "whitepaper": "kb", "repo-doc": "kb", "tools": "kb", "property": "kb",
    "mental-model": "mental-models",
}
KB_TYPES = {"whitepaper", "repo-doc", "tools", "property"}


# ─────────────────────────── helpers ───────────────────────────

def _safe_name(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r'[\\/:*?"<>|\s]+', "_", s).strip("_") or "untitled"


def _yaml_str(v):
    s = str(v)
    if re.search(r'[:#\[\]{}"\'\n]|^\s|\s$', s) or s in ("true", "false", "null", ""):
        return json.dumps(s, ensure_ascii=False)
    return s


def _write_if_changed(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.write_text(text, encoding="utf-8")
    return True


def _load_graph():
    if not GRAPH.exists():
        subprocess.run([sys.executable, str(KDIR / "build_knowledge.py")],
                       check=True, capture_output=True)
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def note_rel_path(note):
    sub = TYPE_DIR.get(note["type"], "misc")
    if note["type"] in KB_TYPES:
        sub = f"kb/{note.get('repo', 'misc')}"
        if note.get("kbrel"):  # 保留子目錄結構（us/demand vs tw/demand 防撞名）
            sub += "/" + note["kbrel"]
    if note["type"] == "internal-note":
        area = (note.get("tags") or ["root"])[0]
        sub = f"internal/{area}"
    base = os.path.basename(note["source"])
    stem = re.sub(r"\.(html|md|py|json)$", "", base)
    if note["type"] == "strategy":
        stem = _safe_name(note["id"])
    if note.get("note_stem"):  # 多筆記共用一個來源檔（mental models）
        stem = note["note_stem"]
    return f"auto/{sub}/{_safe_name(stem)}.md"


# ─────────────────────────── vault 筆記渲染 ───────────────────────────

def render_note(note, entity_themes):
    fm = ["---"]
    for k in ("id", "type", "entity", "theme", "title", "date", "verdict",
              "grade", "oneliner", "repo", "source", "url", "parse_level"):
        if note.get(k) not in (None, ""):
            fm.append(f"{k}: {_yaml_str(note[k])}")
    tags = note.get("tags") or []
    if tags:
        fm.append("tags: [" + ", ".join(_yaml_str(t) for t in tags) + "]")
    for k, v in (note.get("extra") or {}).items():
        fm.append(f"{k}: {_yaml_str(v)}")
    fm.append("---")

    head = f"# {note['title']}"
    meta_bits = [b for b in (note.get("date"),
                             f"裁決：{note['verdict']}" if note.get("verdict") else None,
                             f"評級：{note['grade']}" if note.get("grade") else None) if b]
    if meta_bits:
        head += "\n" + " · ".join(meta_bits)

    links = []
    ent = note.get("entity")
    if ent:
        links.append(f"[[{ent}]]")
        for th in entity_themes.get(ent, [])[:6]:
            links.append(f"[[Theme_{_safe_name(th)}]]")
    if note.get("theme") and note["type"] in ("id", "supplychain"):
        links.append(f"[[Theme_{_safe_name(note['theme'])}]]")
    for tk in (note.get("related_tickers") or note.get("tickers") or [])[:20]:
        links.append(f"[[{tk}]]")
    seen, uniq = set(), []
    for l in links:
        if l not in seen:
            seen.add(l)
            uniq.append(l)
    link_line = ("所屬：" + " · ".join(uniq) + "\n\n") if uniq else ""

    body = []
    for _sid, heading, text in note["sections"]:
        if heading:
            body.append(f"## {heading}\n")
        if text:
            body.append(text + "\n")
    return "\n".join(fm) + "\n\n" + head + "\n\n" + link_line + "\n".join(body).rstrip() + "\n"


def render_entity_hub(ticker, graph_node, notes_for, entity_themes, supplies):
    lines = ["---", f"id: entity-{_safe_name(ticker)}", "type: entity",
             f"title: {_yaml_str(ticker)}", "---", "", f"# {ticker}", ""]
    c = (graph_node or {}).get("canonical")
    if c:
        lines.append(f"**現裁決：{c.get('verdict') or '—'}**（基本面 {c.get('fundamental_grade') or '—'}，"
                     f"{c.get('date') or '—'}，{c.get('freshness') or '—'}）")
        lines.append("")
    themes = entity_themes.get(ticker, [])
    if themes:
        lines.append("所屬主題：" + " · ".join(f"[[Theme_{_safe_name(t)}]]" for t in themes))
        lines.append("")
    if supplies:
        lines.append("供應鏈位置：")
        for tid, proc in supplies:
            lines.append(f"- [[Theme_{_safe_name(tid)}]]：{proc}")
        lines.append("")
    if notes_for:
        lines.append(f"## 報告（{len(notes_for)}）")
        for n in sorted(notes_for, key=lambda n: (n.get("date") or "", n["id"]), reverse=True):
            stem = Path(n["note"]).stem
            bits = [n.get("date") or "", n["type"].upper(),
                    n.get("verdict") or n.get("grade") or ""]
            lines.append(f"- [[{stem}]] {' '.join(b for b in bits if b)}")
    return "\n".join(lines).rstrip() + "\n"


def render_theme_hub(theme, graph_node, id_notes, members, sc_members):
    lines = ["---", f"id: theme-{_safe_name(theme)}", "type: theme",
             f"title: {_yaml_str(theme)}", "---", "", f"# {theme}", ""]
    g = graph_node or {}
    if g.get("oneliner"):
        lines.append(g["oneliner"])
        lines.append("")
    if g.get("action"):
        lines.append(f"▸ action: {g['action']}")
        lines.append("")
    if id_notes:
        lines.append("## 產業報告")
        for n in sorted(id_notes, key=lambda n: n.get("date") or "", reverse=True):
            lines.append(f"- [[{Path(n['note']).stem}]] {n.get('date') or ''} "
                         f"{n.get('verdict') or ''}")
        lines.append("")
    if members:
        lines.append(f"## 成員（{len(members)}）")
        for t in sorted(members):
            lines.append(f"- [[{t}]]")
        lines.append("")
    if sc_members:
        lines.append(f"## 供應鏈節點廠商（{len(sc_members)}）")
        for t, proc in sorted(sc_members):
            lines.append(f"- [[{t}]]：{proc}")
    return "\n".join(lines).rstrip() + "\n"


# ─────────────────────────── FTS ───────────────────────────

def rebuild_fts(summaries):
    """從 vault .md 全量重灌 brain.db（HTML parse 才貴；這步幾秒內）。"""
    tmp = DB.with_suffix(".db.tmp")
    tmp.unlink(missing_ok=True)
    con = sqlite3.connect(tmp)
    con.execute("""CREATE TABLE notes(
        id TEXT PRIMARY KEY, path TEXT, type TEXT, entity TEXT, title TEXT,
        date TEXT, verdict TEXT, source TEXT, url TEXT, tags TEXT)""")
    fts5 = True
    try:
        con.execute("""CREATE VIRTUAL TABLE chunks USING fts5(
            note_id UNINDEXED, section_id UNINDEXED, heading, text,
            tokenize='trigram')""")
    except sqlite3.OperationalError:
        fts5 = False
        con.execute("""CREATE TABLE chunks(
            note_id TEXT, section_id TEXT, heading TEXT, text TEXT)""")
    con.execute("CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT)")
    con.execute("INSERT INTO meta VALUES('fts5', ?)", ("1" if fts5 else "0",))

    for s in summaries:
        con.execute("INSERT OR REPLACE INTO notes VALUES(?,?,?,?,?,?,?,?,?,?)", (
            s["id"], s["note"], s["type"], s.get("entity"), s.get("title"),
            s.get("date"), s.get("verdict") or s.get("grade"),
            s.get("source"), s.get("url"),
            json.dumps(s.get("tags") or [], ensure_ascii=False)))
        p = VAULT / s["note"]
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        body = text.split("---", 2)[-1]
        cur_h, buf, idx = "", [], 0
        rows = []
        for line in body.splitlines():
            m = re.match(r"##\s+(.*)", line)
            if m and not line.startswith("###"):
                if buf:
                    rows.append((s["id"], f"s{idx}", cur_h, "\n".join(buf).strip()))
                    idx += 1
                cur_h, buf = m.group(1).strip(), []
            else:
                buf.append(line)
        if buf:
            rows.append((s["id"], f"s{idx}", cur_h, "\n".join(buf).strip()))
        con.executemany(
            "INSERT INTO chunks(note_id, section_id, heading, text) VALUES(?,?,?,?)",
            [(a, b, unicodedata.normalize("NFKC", c),
              unicodedata.normalize("NFKC", d)) for a, b, c, d in rows if d])
    con.commit()
    con.close()
    tmp.replace(DB)
    return fts5


def build_falsifiers():
    """掃 vault/notes/**（用戶手寫真相）抽「殺手假設」與獵場認領 →
    knowledge/falsifiers.json（衍生，gitignore），供 q.py --falsifiers 與
    position-thesis-monitor Check 8 機械對帳。"""
    from datetime import date as _date
    items = []
    base = VAULT / "notes"
    if base.is_dir():
        for p in sorted(base.rglob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            fm = {}
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) == 3:
                    for line in parts[1].splitlines():
                        m = re.match(r"(\w[\w-]*):\s*(.*)", line)
                        if m:
                            fm[m.group(1)] = m.group(2).strip().strip('"')
            rel = str(p.relative_to(KDIR.parent))
            for m in re.finditer(r"殺手假設[：:]\s*(.+)", text):
                items.append({"kind": "falsifier", "ticker": fm.get("ticker"),
                              "date": fm.get("date"), "verdict": fm.get("verdict"),
                              "text": m.group(1).strip()[:400], "source": rel})
            # 獵場日誌：## [[TK]]（鏡頭，日期 認領…）+ 解釋段
            for m in re.finditer(
                    r"^##\s+\[\[([^\]]+)\]\]（([^）]*)）\s*\n+(.+?)(?=\n##\s|\n---|\Z)",
                    text, re.S | re.M):
                items.append({"kind": "hunt-claim", "ticker": m.group(1),
                              "date": fm.get("date"), "meta": m.group(2),
                              "text": m.group(3).strip()[:400], "source": rel})
    (KDIR / "falsifiers.json").write_text(
        json.dumps({"as_of": _date.today().isoformat(), "items": items},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    return len(items)


# ─────────────────────────── main ───────────────────────────

def main():
    args = set(sys.argv[1:])
    full = "--full" in args
    stats = "--stats" in args
    no_wiki = "--no-wiki" in args

    cache = {"version": CACHE_VERSION, "files": {}}
    if CACHE.exists() and not full:
        try:
            loaded = json.loads(CACHE.read_text(encoding="utf-8"))
            if loaded.get("version") == CACHE_VERSION:
                cache = loaded
        except json.JSONDecodeError:
            pass
    files_cache = cache["files"]

    graph = _load_graph()
    gnodes = {n["id"]: n for n in graph.get("nodes", [])}
    aliases = graph.get("aliases", {})
    entity_themes, supplies_by_ent = {}, {}
    theme_members, theme_sc = {}, {}
    for e in graph.get("edges", []):
        if e.get("rel") == "belongs_to":
            lst = entity_themes.setdefault(e["from"], [])
            if e["to"] not in lst:
                lst.append(e["to"])
            theme_members.setdefault(e["to"], set()).add(e["from"])
        elif e.get("rel") == "supplies":
            supplies_by_ent.setdefault(e["from"], []).append((e["to"], e.get("node") or ""))
            theme_sc.setdefault(e["to"], set()).add((e["from"], e.get("node") or ""))

    specs = bx.discover()
    missing_repos = [os.path.basename(p) for p, fam, _ in specs if fam == "__missing_repo__"]
    specs = [(p, fam, ex) for p, fam, ex in specs if fam != "__missing_repo__"]

    n_new, n_cached, n_err = 0, 0, 0
    fam_count, level_count = Counter(), Counter()
    seen_sources = set()

    for path, family, ex in specs:
        rel_key = os.path.relpath(path, REPO) if str(REPO) in path \
            else path.replace(str(Path.home()), "~")
        seen_sources.add(rel_key)
        try:
            st = os.stat(path)
        except OSError:
            continue
        ent = files_cache.get(rel_key)
        if ent and ent.get("mtime") == st.st_mtime and ent.get("size") == st.st_size \
                and all((VAULT / n["note"]).exists() for n in ent.get("notes", [])):
            n_cached += 1
            for n in ent["notes"]:
                fam_count[n["type"]] += 1
                level_count[n.get("parse_level") or "?"] += 1
            continue
        try:
            notes = ex(path)
        except Exception as e:
            n_err += 1
            print(f"  WARN extract fail {rel_key}: {e}")
            continue
        summaries = []
        for note in notes:
            if note.get("entity"):
                note["entity"] = aliases.get(note["entity"], note["entity"])
            if note.get("vault_rel"):  # 用戶筆記本身就在 vault，絕不覆寫
                rel_note = note["vault_rel"]
            else:
                rel_note = note_rel_path(note)
                _write_if_changed(VAULT / rel_note, render_note(note, entity_themes))
            s = {k: note.get(k) for k in
                 ("id", "type", "entity", "theme", "title", "date", "verdict",
                  "grade", "oneliner", "tags", "url", "source", "parse_level",
                  "repo", "related_tickers", "tickers", "extra")}
            s = {k: v for k, v in s.items() if v not in (None, [], "")}
            s["note"] = rel_note
            summaries.append(s)
            fam_count[note["type"]] += 1
            level_count[note.get("parse_level") or "?"] += 1
        files_cache[rel_key] = {"mtime": st.st_mtime, "size": st.st_size,
                                "notes": summaries}
        n_new += 1

    # 孤兒清理：來源不見了 → 筆記刪掉、cache 移除
    n_pruned = 0
    for key in sorted(set(files_cache) - seen_sources):
        for n in files_cache[key].get("notes", []):
            p = VAULT / n["note"]
            if p.exists():
                p.unlink()
                n_pruned += 1
        del files_cache[key]

    all_summaries = [n for ent in files_cache.values() for n in ent.get("notes", [])]

    # entity / theme hub（每次由 cache 摘要＋graph 重生，冪等）
    notes_by_entity = {}
    for s in all_summaries:
        if s.get("entity"):
            notes_by_entity.setdefault(s["entity"], []).append(s)
    id_notes_by_theme = {}
    for s in all_summaries:
        if s["type"] in ("id", "supplychain") and s.get("theme"):
            id_notes_by_theme.setdefault(s["theme"], []).append(s)

    hub_entities = set(notes_by_entity) | {
        n["id"] for n in graph.get("nodes", []) if n.get("type") == "company"}
    for t in sorted(hub_entities):
        _write_if_changed(
            VAULT / "auto/entities" / f"{_safe_name(t)}.md",
            render_entity_hub(t, gnodes.get(t), notes_by_entity.get(t, []),
                              entity_themes, sorted(set(supplies_by_ent.get(t, [])))))

    hub_themes = set(id_notes_by_theme) | set(theme_members) | set(theme_sc)
    for th in sorted(hub_themes):
        _write_if_changed(
            VAULT / "auto/themes" / f"Theme_{_safe_name(th)}.md",
            render_theme_hub(th, gnodes.get(th), id_notes_by_theme.get(th, []),
                             theme_members.get(th, set()), theme_sc.get(th, set())))

    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    n_fals = build_falsifiers()

    # 無變動且 DB 已在 → 跳過 FTS 重灌（post-commit/post-merge hook 常態路徑）
    if n_new or n_pruned or not DB.exists():
        fts5 = rebuild_fts(all_summaries)
    else:
        try:
            con = sqlite3.connect(DB)
            fts5 = con.execute("SELECT v FROM meta WHERE k='fts5'").fetchone()[0] == "1"
            con.close()
        except sqlite3.Error:
            fts5 = rebuild_fts(all_summaries)

    if not no_wiki and (KDIR / "brain_wiki.py").exists():
        r = subprocess.run([sys.executable, str(KDIR / "brain_wiki.py")],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  WARN wiki render fail: {r.stderr.strip()[:300]}")

    print(f"🧠 brain: {n_new} extracted, {n_cached} cached, {n_pruned} pruned, "
          f"{n_err} errors；notes {len(all_summaries)}＋hubs "
          f"{len(hub_entities)} entities/{len(hub_themes)} themes；"
          f"FTS={'trigram' if fts5 else 'fallback'}；falsifiers {n_fals}")
    if missing_repos:
        print(f"  ⚠ 外部 repo 不在本機（跳過）：{', '.join(missing_repos)}")
    if stats:
        print("\n家族計數：")
        for k, v in fam_count.most_common():
            print(f"  {k:14s} {v}")
        print("\n解析等級（h2=正常 / sectitle=舊版 / body=整篇 fallback）：")
        for k, v in level_count.most_common():
            print(f"  {k:14s} {v}")


if __name__ == "__main__":
    main()
