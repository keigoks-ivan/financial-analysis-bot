#!/usr/bin/env python3
"""個股研究（精簡版）一鍵指令：備資料 → 點名同業＋寫稿＋渲染＋文字檢查 → 發布到網站。

用法：python3 scripts/dd5/dd.py TICKER [--date YYYYMMDD] [--peers A,B,C] [--reuse] [--dry-run] [--no-push]
  --date     預設今天（台北時間）
  --peers    手動指定同業代號，逗號分隔（蓋過模型點名）
  --reuse    run 目錄已有 article.md 時，跳過備資料與 LLM 步驟，只重跑 render,lint（零花費；測試與補發用）
  --dry-run  做到「寫檔、注入導覽列、qc」為止，輸出到 ~/dd5-pilot/preview/<T>/，不建 worktree、不 commit、不 push
  --no-push  做到 commit 為止，不推送，並把那個 commit 丟掉（只印 git show --stat）

發布一律在暫時 worktree（從 origin/main 開、detached）裡做，不碰任何人的主工作區。
exit code：0 成功；3 文字檢查（lint）有 block；4 發布前 qc 或 commit hook 擋下；5 推送失敗。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent  # 本檔所在的 repo（worktree）根目錄
for p in (str(HERE.parent), str(HERE.parent / "dd2"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import lint  # noqa: E402
import publish as pub  # noqa: E402

PILOT = Path.home() / "dd5-pilot"
WT_BASE = Path("/Volumes/X10 Data/worktrees")
SITE = "https://research.investmquest.com"
MAX_PUSH_TRIES = 3


def sh(args, cwd=None, check=False, env=None):
    r = subprocess.run(args, cwd=str(cwd) if cwd else None, capture_output=True, text=True, env=env)
    if check and r.returncode != 0:
        raise RuntimeError("{0} 失敗（{1}）：{2}".format(" ".join(map(str, args)), r.returncode, (r.stderr or r.stdout).strip()))
    return r


def git(args, cwd, check=True):
    return sh(["git"] + list(args), cwd=cwd, check=check)


def say(msg):
    print(msg, flush=True)


def taipei_today():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d")
    except Exception:
        return (dt.datetime.utcnow() + dt.timedelta(hours=8)).strftime("%Y%m%d")


def run_py(script, args):
    env = dict(os.environ)
    env.setdefault("DD5_RUN_LIMIT", "5")
    r = subprocess.run([sys.executable, str(HERE / script)] + args, cwd=str(REPO), env=env)
    if r.returncode != 0:
        raise SystemExit("{0} 失敗（exit {1}）".format(script, r.returncode))


# ---------- 暫時 worktree ----------
def make_worktree(t):
    git(["fetch", "origin"], REPO)
    stamp = dt.datetime.now().strftime("%H%M%S")
    if WT_BASE.is_dir():
        wt = WT_BASE / "fab-dd5pub-{0}-{1}".format(t, stamp)
    else:
        wt = Path(tempfile.mkdtemp(prefix="fab-dd5pub-{0}-{1}-".format(t, stamp)))
        wt.rmdir()  # worktree add 要一個不存在（或空）的路徑
    git(["worktree", "add", "--detach", str(wt), "origin/main"], REPO)
    return wt


def drop_worktree(wt):
    if wt is None:
        return
    r = git(["worktree", "remove", "--force", str(wt)], REPO, check=False)
    if r.returncode != 0:
        say("警告：暫時 worktree 沒移除乾淨：{0}".format((r.stderr or r.stdout).strip()))
    if Path(wt).exists():
        shutil.rmtree(str(wt), ignore_errors=True)
    git(["worktree", "prune"], REPO, check=False)


# ---------- 發布步驟 2～5 ----------
def qc_check(root, files):
    r = sh([sys.executable, str(Path(root) / "scripts" / "qc.py")] + [str(f) for f in files], cwd=root)
    if r.returncode != 0:
        say("發布前檢查（qc）沒過，不發布：")
        say((r.stderr or "") + (r.stdout or ""))
        raise SystemExit(4)
    say("qc：" + (r.stdout.strip().splitlines() or ["通過"])[-1])


def write_and_commit(t, d, wt):
    """在 wt 寫檔、注入導覽、qc、commit。回傳 (publish 結果, commit hash)；沒有差異回傳 (結果, None)。"""
    try:
        r = pub.publish(t, d, wt, scripts_dir=Path(wt) / "scripts")
    except pub.LintBlocked as e:
        report_blocks(t, e.blocks)
    qc_check(wt, [r["page"], r["index"]])
    paths = ["docs/stock-dash/research/{0}_{1}.html".format(t, d), "docs/stock-dash/research/index.json"] + r["removed"]
    if git(["status", "--porcelain", "--"] + paths, wt).stdout.strip() == "":
        return r, None
    git(["add", "-A", "--"] + paths, wt)
    msg = "個股研究（精簡版）：{0} {1}-{2}-{3}".format(t, d[:4], d[4:6], d[6:])
    c = git(["commit", "-m", msg, "--"] + paths, wt, check=False)
    if c.returncode != 0:
        say("commit 被擋（多半是 pre-commit hook）：")
        say((c.stdout or "") + (c.stderr or ""))
        raise SystemExit(4)
    h = git(["rev-parse", "HEAD"], wt).stdout.strip()
    return r, h


def report_blocks(t, blocks):
    say("{0} 文字檢查有 {1} 個 block，未發布：".format(t, len(blocks)))
    for h in blocks:
        say("  [block] {0} L{1}: {2}".format(h["rule"], h["line"], h["text"]))
    raise SystemExit(3)


def push_with_retry(t, d, wt):
    """推到 origin/main；被拒就 fetch＋rebase 再推，最多 3 次；rebase 衝突就丟掉這次 commit、從最新 origin/main 重做。"""
    for i in range(1, MAX_PUSH_TRIES + 1):
        r = git(["push", "--no-verify", "origin", "HEAD:main"], wt, check=False)
        if r.returncode == 0:
            return git(["rev-parse", "HEAD"], wt).stdout.strip()
        say("推送被拒（第 {0}/{1} 次）：{2}".format(i, MAX_PUSH_TRIES, (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else ""))
        if i == MAX_PUSH_TRIES:
            break
        git(["fetch", "origin"], wt)
        rb = git(["rebase", "origin/main"], wt, check=False)
        if rb.returncode != 0:
            say("rebase 衝突（多半是 index.json），丟掉這次 commit，從最新 origin/main 重新發布")
            git(["rebase", "--abort"], wt, check=False)
            git(["reset", "--hard", "origin/main"], wt)
            _, h = write_and_commit(t, d, wt)
            if h is None:
                say("最新 origin/main 上內容已經一樣，不用發布")
                return None
        else:
            try:  # rebase 乾淨但仍確認 index.json 是合法 JSON
                json.loads((Path(wt) / "docs/stock-dash/research/index.json").read_text(encoding="utf-8"))
            except Exception:
                say("rebase 後 index.json 不是合法 JSON，丟掉 commit 重新發布")
                git(["reset", "--hard", "origin/main"], wt)
                _, h = write_and_commit(t, d, wt)
                if h is None:
                    return None
    raise SystemExit(5)


def ff_main_workspace():
    common = git(["rev-parse", "--path-format=absolute", "--git-common-dir"], REPO).stdout.strip()
    main = Path(common).parent
    if git(["rev-parse", "--abbrev-ref", "HEAD"], main, check=False).stdout.strip() != "main":
        say("主工作區 {0} 不在 main 分支，沒有 fast-forward".format(main))
        return
    if git(["status", "--porcelain"], main, check=False).stdout.strip():
        say("主工作區 {0} 有未提交的改動，沒有 fast-forward（要的話自己 git merge --ff-only origin/main）".format(main))
        return
    r = git(["merge", "--ff-only", "origin/main"], main, check=False)
    say("主工作區 fast-forward：" + ("完成" if r.returncode == 0 else "失敗（{0}）".format((r.stderr or r.stdout).strip())))


# ---------- 回報 ----------
def in_screener(t):
    r = git(["show", "origin/main:docs/dd-screener/latest.json"], REPO, check=False)
    try:
        txt = r.stdout if r.returncode == 0 else (REPO / "docs/dd-screener/latest.json").read_text(encoding="utf-8")
        return any((s.get("ticker") or "").upper() == t for s in json.loads(txt).get("stocks", []))
    except Exception:
        return None


def peers_summary(run, given):
    if given:
        return "手動指定：{0}".format("、".join(given))
    pp = run / "peers_pick.json"
    if not pp.exists():
        return "沒有點名紀錄（peers_pick.json 不存在）"
    rec = json.loads(pp.read_text(encoding="utf-8"))
    final = "、".join(rec.get("final", []))
    kept = [v for v in rec.get("verify", []) if v.get("kept")]
    if rec.get("error") or not kept:
        return "{0}（模型點名失敗或全數驗證不過，已退回自動名單）".format(final)
    if rec.get("auto_filled"):
        return "{0}（模型點名驗過 {1} 家，另 {2} 家由程式自動補）".format(final, len(kept), len(rec["auto_filled"]))
    return "{0}（模型點名，程式驗過）".format(final)


def final_report(t, d, run, r, commit, mode, reused, given_peers):
    mf = json.loads((run / "manifest.json").read_text(encoding="utf-8")) if (run / "manifest.json").exists() else {}
    total = mf.get("total_cost_usd")
    hits = r["lint_hits"]
    warns = [h for h in hits if h["severity"] == "warn"]
    say("")
    say("===== 回報：{0} {1} =====".format(t, d))
    say("結果：" + mode)
    say("儀表板：{0}/stock-dash/?t={1}".format(SITE, t))
    say("全文頁：{0}/stock-dash/research/{1}_{2}.html".format(SITE, t, d))
    if reused:
        say("花費：這次沒有新花費（--reuse）；這個 run 目錄先前累計 ${0}".format(total))
    else:
        say("花費：這個 run 目錄累計 ${0}（含這次）".format(total))
    say("文字檢查：block 0 個、warn {0} 個".format(len(warns)))
    for h in warns:
        say("  [warn] {0} L{1}: {2}".format(h["rule"], h["line"], h["text"]))
    say("同業：" + peers_summary(run, given_peers))
    sc = in_screener(t)
    if sc is False:
        say("儀表板沒有這檔的頁面，摘要看不到，只能用全文頁網址。")
    elif sc is None:
        say("（讀不到 dd-screener/latest.json，沒辦法確認這檔在不在儀表板名單）")
    else:
        say("這檔在儀表板名單（dd-screener/latest.json 的 stocks）裡。")
    say("commit：" + (commit or "無"))


def main():
    ap = argparse.ArgumentParser(description="個股研究（精簡版）一鍵指令")
    ap.add_argument("ticker")
    ap.add_argument("--date", default=None, help="YYYYMMDD，預設今天（台北時間）")
    ap.add_argument("--peers", default=None, help="同業代號，逗號分隔")
    ap.add_argument("--reuse", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    t = a.ticker.upper()
    d = a.date or taipei_today()
    if len(d) != 8 or not d.isdigit():
        raise SystemExit("--date 要 YYYYMMDD")
    given = [x.strip().upper() for x in a.peers.split(",") if x.strip()] if a.peers else []
    run = PILOT / "runs" / "{0}_{1}".format(t, d)

    # 1. 備資料與寫稿
    reused = a.reuse and (run / "article.md").exists()
    if a.reuse and not reused:
        say("--reuse 但 {0} 沒有 article.md，改走完整流程（會花錢）".format(run))
    if reused:
        if given:
            say("注意：--reuse 不重新點名同業，--peers 被忽略")
            given = []
        say("== 沿用 {0}，只重跑 render,lint ==".format(run))
        run_py("run.py", [t, "--date", d, "--out", str(run / "article.html"), "--steps", "render,lint"])
    else:
        say("== 備資料 ==")
        run_py("pack.py", [t, "--date", d])
        say("== 點名同業、寫稿、渲染、文字檢查 ==")
        args = [t, "--date", d, "--out", str(run / "article.html"), "--steps", "peers,lite,moat,render,lint"]
        if given:
            args += ["--peers", ",".join(given)]
        run_py("run.py", args)

    # 2. lint 關卡（發布前再算一次，block 就停）
    out = lint.lint_run(run)
    blocks = [h for h in out["hits"] if h["severity"] == "block"]
    if blocks:
        report_blocks(t, blocks)

    # 3. 發布
    if a.dry_run:
        prev = PILOT / "preview" / t
        shutil.rmtree(str(prev), ignore_errors=True)
        rdir = prev / "docs/stock-dash/research"
        rdir.mkdir(parents=True)
        git(["fetch", "origin"], REPO, check=False)
        g = git(["show", "origin/main:docs/stock-dash/research/index.json"], REPO, check=False)
        (rdir / "index.json").write_text(g.stdout if g.returncode == 0 else "{}\n", encoding="utf-8")
        r = pub.publish(t, d, prev, scripts_dir=REPO / "scripts")
        qc_check(REPO, [r["page"], r["index"]])
        say("dry-run：輸出在 {0}（不 commit、不 push）".format(prev))
        say("  新頁：{0}".format(r["page"]))
        say("  索引：{0}（將刪除舊頁：{1}）".format(r["index"], r["removed"] or "無"))
        final_report(t, d, run, r, None, "dry-run（沒有發布）", reused, given)
        return

    wt = None
    try:
        wt = make_worktree(t)
        say("暫時 worktree：{0}".format(wt))
        r, h = write_and_commit(t, d, wt)
        if h is None:
            say("內容沒有變化，不用發布")
            final_report(t, d, run, r, None, "內容沒有變化，不用發布", reused, given)
            return
        if a.no_push:
            say(git(["show", "--stat", "--format=commit %H%n%s", "HEAD"], wt).stdout)
            say("--no-push：這個 commit 不推送，移除暫時 worktree 後就丟掉了")
            final_report(t, d, run, r, h + "（已丟棄，未推送）", "--no-push（沒有發布）", reused, given)
            return
        h2 = push_with_retry(t, d, wt)
        if h2 is None:
            final_report(t, d, run, r, None, "內容沒有變化，不用發布", reused, given)
            return
        ff_main_workspace()
        final_report(t, d, run, r, h2, "已發布（推到 origin/main）", reused, given)
    finally:
        drop_worktree(wt)


if __name__ == "__main__":
    main()
