#!/usr/bin/env python3
"""scripts/ddreport.py — v17 WP1a：per-run 目錄、manifest、`plan`、`status`。

只動 `.dd_build/runs/{TICKER}_{DATE}/` 這個新的 per-run 慣例，不改任何既有腳本的
行為或路徑。`plan` 呼叫既有零 LLM 工具（`dd_prior.py`／`dd_evidence.py`／
`dd_numbers_extra.py`，皆原樣呼叫、不改語意）取得證據骨架與軸清單，再依軸分批寫出
子 agent 派工用的 prompt 檔＋`spawn_list.json`。`status` 印 manifest 與各產物存在／
大小，供人工或 orchestrator 檢視進度。

3.9 相容（`from __future__ import annotations`，不用 3.10+ 語法）。

用法：
    python3 scripts/ddreport.py plan TICKER [--date YYYYMMDD] [--archetype X]
        [--peers a,b] [--segments a,b] [--axes-per-batch 2] [--offline]
    python3 scripts/ddreport.py status TICKER DATE

見 notes/site-internal/dd/_wp_spec_v17_20260905.md「共同約定」與「WP1a」段。
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_headless  # noqa: E402  （WP1c 無頭執行器，import 呼叫，不改其內部）
import dd_meta_reader  # noqa: E402  （WP7a peers 來源③：讀 id-meta related_tickers，不改其內部）

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
BUILD_DIR = REPO_ROOT / ".dd_build"
RUNS_DIR = BUILD_DIR / "runs"
PROMPTS_TMPL_DIR = SCRIPTS_DIR / "dd_prompts"

# ---------------------------------------------------------------------------
# WP1d: run 目錄狀態機（Stage 0 → 判斷 → 閘 → 快速版）串接常數
# ---------------------------------------------------------------------------
STAGE_ORDER = ["stage0", "judged", "gated", "brief"]
DEFAULT_JUDGMENT_MODEL = "fable"
# 判斷模型↔閘模型對調表（跨模型冷讀，見 _wp_spec_v17_batch2_20260905.md WP1d §4）
GATE_MODEL_FOR = {"fable": "opus", "opus": "sonnet", "sonnet": "opus"}
JUDGE_MAX_TURNS = 10  # 2026-09-05：AVGO／WDAY 第 9 輪才寫完，8 太緊
# WP7b #1（_wp_spec_v17_batch5_20260905.md）：bundle 改內嵌進 prompt（不再讓
# agent 自己 Read 240KB 檔）後，fix agent 仍要讀 77KB judgment.json＋改＋
# 寫＋judge check，4 輪不夠，實測至少 4 步驟＋緩衝，上調為 6。
JUDGE_FIX_MAX_TURNS = 6
GATE_MAX_TURNS = 6
GATE_PATCH_MAX_TURNS = 6
JUDGE_BUDGET_CACHE_READ = 1_200_000
GATE_BUDGET_CACHE_READ = 2_500_000

# 最後手段的預設 archetype：coverage-axes.md 裡 by_archetype 附加軸數為 0 的
# 那一類（即「只查 common 軸」的基準情境），在 --archetype 未給、且前份 DD
# 是不含 archetype 欄位的 legacy schema（v14.x 以前）時使用。此為刻意的工程
# 折衷，非隨意猜測——見 notes/site-internal/dd/_wp_spec_v17_20260905.md 驗收
# 段對此邊界案例（CRDO 20260904，prior 為 v14.2、無 archetype 欄）的討論。
DEFAULT_ARCHETYPE = "品質複利成長"

AXES_PER_BATCH_DEFAULT = 2

SPAWN_TOOLS_COVERAGE = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_NUMBERS = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_DIGEST = ["Read", "Write", "Bash"]

# WP7a #5：Stage 0 預算重校（AVGO 2026-09-05 實測），Stage 0 段總目標 ≤6M
# （母稿 §4 表同步改，不在本檔範圍）。
BUDGET_CACHE_READ_COVERAGE = 900_000
BUDGET_CACHE_READ_NUMBERS = 1_200_000

# WP7d：摘要子 agent 拆成一篇逐字稿一個 spawn（HPE 第二次真跑實測：一人讀三篇
# 17 輪撞 16 上限、cache_read 2.54M 超 1.5M 預算——單篇合計約 0.5M×3≈1.5M 且
# 可平行，見 _wp_spec_v17_batch5_20260905.md WP7d）。
DIGEST_PER_FILE_MAX_TURNS = 8
BUDGET_CACHE_READ_DIGEST_PER_FILE = 700_000

# WP7a #1：Koyfin 步驟改零 LLM，plan 內直接 subprocess 呼叫，不再走 spawn。
KOYFIN_DIR = Path.home() / "scripts" / "koyfin-downloader"
KOYFIN_DOWNLOADER = KOYFIN_DIR / "koyfin_downloader.py"
KOYFIN_SELECTOR = KOYFIN_DIR / "transcripts_for_dd.py"
KOYFIN_VENV_PYTHON = KOYFIN_DIR / ".venv" / "bin" / "python"
KOYFIN_DOWNLOAD_TIMEOUT = 300
KOYFIN_SELECTOR_TIMEOUT = 60
KOYFIN_DRIVE_GLOB = "Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股"

# ---------------------------------------------------------------------------
# WP6a: finish／index-row 用的固定路徑（模組層常數，供測試 monkeypatch 覆寫）
# ---------------------------------------------------------------------------
DD_DIR = REPO_ROOT / "docs" / "dd"
INDEX_MD_PATH = DD_DIR / "INDEX.md"
RESEARCH_BODY_PATH = REPO_ROOT / "docs" / "research" / "_body.html"
DD_SCREENER_LATEST_PATH = REPO_ROOT / "docs" / "dd-screener" / "latest.json"
PICKS_CANDIDATES_PATH = REPO_ROOT / "docs" / "picks" / "candidates.json"
SRC_ARCHIVE_DIR = REPO_ROOT / "notes" / "site-internal" / "dd" / "_src"
ID_DIR = REPO_ROOT / "docs" / "id"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _pick_python():
    """優先 /tmp/ddvenv/bin/python（若存在且 import yfinance 成功），否則 python3。"""
    venv_py = Path("/tmp/ddvenv/bin/python")
    if venv_py.exists():
        try:
            r = subprocess.run(
                [str(venv_py), "-c", "import yfinance"],
                capture_output=True, timeout=15,
            )
            if r.returncode == 0:
                return str(venv_py)
        except Exception:
            pass
    return "python3"


def _run_dir(ticker, date):
    return RUNS_DIR / "{0}_{1}".format(ticker, date)


def _atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _render_template(tmpl_path, mapping):
    text = Path(tmpl_path).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def _axis_block(axes):
    lines = []
    for a in axes:
        lines.append("[{0}] {1}".format(a.get("id"), a.get("name", "")))
        lines.append("Q: {0}".format(a.get("question", "")))
        for q in a.get("queries", []) or []:
            lines.append("  - {0}".format(q))
        if a.get("na_allowed"):
            lines.append("  (na_allowed=true)")
        lines.append("")
    text = "\n".join(lines).rstrip()
    return text + "\n" if text else ""


EVENTS_ADDENDUM = """## major_events 軸另交頂層 events 五組（QC-19）
`validate_evidence.py` 的 strict 檢查讀的是 evidence.json **頂層** `events` 物件，
不是 `coverage.major_events`——這兩個是分開的鍵，只填前者會漏掉後者。

你除了（a）對 `major_events` 這一軸本身作答（寫進 `coverage.major_events`），
**還要**（b）把同一批查證結果拆成下列五組，寫進回傳 JSON 的**頂層** `events` 鍵：
`ma_merger`（併購）／`lawsuit_class_action`（訴訟／集體訴訟）／`clinical_fda`
（臨床／FDA，非藥品器材業務可用 not_applicable）／`product_recall_warning`
（產品召回／警告）／`sec_investigation_restatement`（SEC 調查／重編財報）。

每組欄位規則與 `coverage.<axis>` 相同：found 需 ≥1 條帶 source／as_of／
direction／affects 的 finding；none 需 ≥2 條 queries_run；不適用（如非藥品業務
的 `clinical_fda`）用 `status:"none"`＋queries_run 說明「非藥品/器材業務，已查
證無相關監管動作」，**不得省略該組鍵**。
"""

EVENTS_JSON_SAMPLE = """{
    "ma_merger": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "lawsuit_class_action": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "clinical_fda": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "product_recall_warning": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "sec_investigation_restatement": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""}
  }"""


def _resolve_archetype(cli_archetype, prior):
    """回傳 (archetype, source)。source 只供 log／回報用途。"""
    if cli_archetype:
        return cli_archetype, "cli"
    if isinstance(prior, dict):
        try:
            a = (prior.get("prior_dd") or {}).get("prior_meta", {}).get("archetype")
            if a:
                return a, "prior.prior_dd.prior_meta.archetype"
        except Exception:
            pass
        a = prior.get("archetype_hint")
        if a:
            return a, "prior.archetype_hint"
    return None, None


# ---------------------------------------------------------------------------
# WP7a #3：peers 來源優先順序 --peers → SRC_ARCHIVE_DIR 前份 evidence.json 的
# numbers.peer_financials → docs/id/ID_*.html id-meta related_tickers[] →
# 都沒有則交由呼叫端印錯誤退出（strict 會擋 <2 對手，早停比晚停省）。
# ---------------------------------------------------------------------------

def _peers_from_archive(ticker):
    """從 `SRC_ARCHIVE_DIR/{T}_*/` 找最新一份 evidence.json 的
    `numbers.peer_financials` 鍵，去自身與 `_` 開頭的鍵（如 `_note`）。
    回傳 list 或 None（找不到／無可用鍵）。"""
    if not SRC_ARCHIVE_DIR.exists():
        return None
    candidates = sorted(
        (p for p in SRC_ARCHIVE_DIR.glob("{0}_*".format(ticker)) if p.is_dir()),
        key=lambda p: p.name, reverse=True,
    )
    for cand in candidates:
        ev_path = cand / "{0}.evidence.json".format(cand.name)
        if not ev_path.exists():
            ev_path = cand / "evidence.json"
        if not ev_path.exists():
            continue
        try:
            evidence = _load_json(ev_path)
        except Exception:
            continue
        pf = (evidence.get("numbers") or {}).get("peer_financials") or {}
        peers = [k for k in pf.keys() if k != ticker and not k.startswith("_")]
        if peers:
            return peers
    return None


def _peers_from_id_meta(ticker):
    """`docs/id/ID_*.html` id-meta `related_tickers[]` 含 {T} 的那份，取前 4 檔
    （去自身）。回傳 list 或 None。"""
    if not ID_DIR.exists():
        return None
    try:
        matches = dd_meta_reader.find_ids_for_ticker(ID_DIR, ticker)
    except Exception:
        return None
    if not matches:
        return None
    _, meta = matches[0]
    related = meta.get("related_tickers") or []
    tickers = []
    target = ticker.strip().upper()
    for r in related:
        t = (r.get("ticker") or "").strip().upper()
        if t and t != target and t not in tickers:
            tickers.append(t)
    return tickers[:4] or None


def _resolve_peers(cli_peers, ticker):
    """回傳 (peers_str_or_None, source)。優先序：--peers → archive →
    id-meta → (None, None)（呼叫端負責印錯誤退出）。"""
    if cli_peers:
        return cli_peers, "cli"
    from_archive = _peers_from_archive(ticker)
    if from_archive:
        return ",".join(from_archive), "archive"
    from_id_meta = _peers_from_id_meta(ticker)
    if from_id_meta:
        return ",".join(from_id_meta), "id_meta"
    return None, None


# ---------------------------------------------------------------------------
# WP7a #1：Koyfin 步驟改零 LLM——plan 內直接呼叫，不再走 spawn。
# ---------------------------------------------------------------------------

def _koyfin_python():
    if KOYFIN_VENV_PYTHON.exists():
        return str(KOYFIN_VENV_PYTHON)
    return "python3"


def _find_koyfin_drive_folder(drive_ticker):
    """`~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{T}/` glob 找
    第一個存在的資料夾；找不到回傳 None。"""
    home = Path.home()
    for m in sorted(home.glob(KOYFIN_DRIVE_GLOB + "/" + drive_ticker)):
        if m.is_dir():
            return m
    return None


def _replay_koyfin_transcripts(replay_dir):
    """`--replay-from` 生效時（`DD_REPLAY_FROM` 環境變數）：跳過真的
    Koyfin 網路呼叫，改讀 fixture 既有的 `parts/transcripts.json`，沒有就
    退回 fixture 已合併 evidence.json 內嵌的 `transcripts` 區塊；都沒有則
    回傳空清單＋`koyfin_session_status:"folder_missing"`。"""
    cand = replay_dir / "parts" / "transcripts.json"
    if cand.exists():
        try:
            data = _load_json(cand)
            if isinstance(data, dict) and data.get("transcripts"):
                return data
        except Exception:
            pass
    ev_cand = replay_dir / "{0}.evidence.json".format(replay_dir.name)
    if not ev_cand.exists():
        ev_cand = replay_dir / "evidence.json"
    if ev_cand.exists():
        try:
            evidence = _load_json(ev_cand)
            t = evidence.get("transcripts")
            if t:
                return {"transcripts": t}
        except Exception:
            pass
    return {
        "transcripts": {
            "selected": {"recent_four_quarters": [], "high_signal_optional": []},
            "koyfin_session_status": "folder_missing",
            "must_read_all": [],
            "optional_read_all": [],
        }
    }


def _run_koyfin_step(ticker, date, run_dir, evidence_dest, manifest, drive_ticker=None):
    """WP7a #1：跑增量下載＋逐字稿必讀/可略讀清單，寫 `parts/transcripts.json`
    並立刻 merge 進 evidence.json。失敗（下載逾時／腳本缺席／session 過期）
    只 warn 標記 `koyfin_session_status`，不 abort plan。`--replay-from` 生效
    時（`DD_REPLAY_FROM` 環境變數）改讀 fixture，不打真實網路。"""
    drive_ticker = drive_ticker or ticker
    parts_dir = run_dir / "parts"
    transcripts_out = parts_dir / "transcripts.json"

    replay_from = os.environ.get("DD_REPLAY_FROM")
    if replay_from:
        transcripts_obj = _replay_koyfin_transcripts(Path(replay_from))
        _atomic_write_json(transcripts_out, transcripts_obj)
        if evidence_dest.exists():
            py = _pick_python()
            subprocess.run(
                [py, str(SCRIPTS_DIR / "dd_evidence.py"), "merge",
                 str(evidence_dest), str(transcripts_out)],
                capture_output=True, text=True,
            )
        sel = (transcripts_obj.get("transcripts") or {}).get("selected") or {}
        status = (transcripts_obj.get("transcripts") or {}).get("koyfin_session_status")
        print("koyfin: replay 模式（{0}）session={1} 必讀={2} 可略讀={3}".format(
            replay_from, status,
            len(sel.get("recent_four_quarters") or []),
            len(sel.get("high_signal_optional") or []),
        ))
        manifest["koyfin_session_status"] = status
        return transcripts_obj

    session_status = "ok"

    if not KOYFIN_DOWNLOADER.exists():
        session_status = "downloader_missing"
    else:
        try:
            r = subprocess.run(
                [_koyfin_python(), str(KOYFIN_DOWNLOADER), "--tickers", ticker],
                cwd=str(KOYFIN_DIR), capture_output=True, text=True,
                timeout=KOYFIN_DOWNLOAD_TIMEOUT,
            )
            manifest["steps"].append({"step": "koyfin_download", "returncode": r.returncode})
            if r.returncode != 0:
                session_status = "expired"
                print(
                    "[warn] koyfin_downloader.py 失敗（exit {0}），改用磁碟既有逐字稿：{1}".format(
                        r.returncode, (r.stderr or "").strip()[-300:]),
                    file=sys.stderr,
                )
        except subprocess.TimeoutExpired:
            session_status = "expired"
            print(
                "[warn] koyfin_downloader.py 逾時（{0}s），改用磁碟既有逐字稿".format(
                    KOYFIN_DOWNLOAD_TIMEOUT),
                file=sys.stderr,
            )
        except Exception as e:
            session_status = "expired"
            print("[warn] koyfin_downloader.py 執行失敗：{0}".format(e), file=sys.stderr)

    selected = {"recent_four_quarters": [], "high_signal_optional": []}
    must_read_all = []
    optional_read_all = []
    must_read_tokens_total = None
    mode = None

    if not KOYFIN_SELECTOR.exists():
        if session_status == "ok":
            session_status = "folder_missing"
    else:
        try:
            r = subprocess.run(
                ["python3", str(KOYFIN_SELECTOR), drive_ticker, "--full", "--n", "4"],
                capture_output=True, text=True, timeout=KOYFIN_SELECTOR_TIMEOUT,
            )
            manifest["steps"].append({"step": "koyfin_transcripts_for_dd", "returncode": r.returncode})
            data = None
            for line in reversed((r.stdout or "").splitlines()):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            if data is None:
                if session_status == "ok":
                    session_status = "folder_missing"
                print(
                    "[warn] transcripts_for_dd.py 無 JSON 輸出：{0}".format(
                        (r.stdout or r.stderr or "").strip()[-300:]),
                    file=sys.stderr,
                )
            else:
                must = data.get("must_read") or []
                optional = data.get("optional_read") or []
                must_read_all = must
                optional_read_all = optional
                mode = data.get("mode")
                must_read_tokens_total = data.get("must_read_tokens_total")
                drive_dir = _find_koyfin_drive_folder(drive_ticker)

                def _abs(fname):
                    if drive_dir is None:
                        return None
                    p = drive_dir / fname
                    return str(p) if p.exists() else None

                for fname in must:
                    ap = _abs(fname)
                    if ap:
                        selected["recent_four_quarters"].append(ap)
                    else:
                        print("[warn] 找不到必讀逐字稿檔：{0}".format(fname), file=sys.stderr)
                for fname in optional:
                    ap = _abs(fname)
                    if ap:
                        selected["high_signal_optional"].append(ap)
        except subprocess.TimeoutExpired:
            if session_status == "ok":
                session_status = "folder_missing"
            print("[warn] transcripts_for_dd.py 逾時", file=sys.stderr)
        except Exception as e:
            if session_status == "ok":
                session_status = "folder_missing"
            print("[warn] transcripts_for_dd.py 執行失敗：{0}".format(e), file=sys.stderr)

    transcripts_obj = {
        "transcripts": {
            "selected": selected,
            "koyfin_session_status": session_status,
            "must_read_all": must_read_all,
            "optional_read_all": optional_read_all,
        }
    }
    if mode is not None:
        transcripts_obj["transcripts"]["mode"] = mode
    if must_read_tokens_total is not None:
        transcripts_obj["transcripts"]["must_read_tokens_total"] = must_read_tokens_total

    _atomic_write_json(transcripts_out, transcripts_obj)

    # 立刻 merge 進 evidence.json：evidence.json 需在 plan 結束時就含
    # transcripts.selected，不必等到 stage0 finalize 才看得到（下游 a2_{k}
    # 直接讀這次 plan 算出的 transcripts_obj，這裡的 merge 主要供
    # evidence.json 本身的一致性與後續 finalize 冪等）。
    if evidence_dest.exists():
        py = _pick_python()
        subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_evidence.py"), "merge",
             str(evidence_dest), str(transcripts_out)],
            capture_output=True, text=True,
        )

    n_recent = len(selected["recent_four_quarters"])
    n_hi = len(selected["high_signal_optional"])
    print("koyfin: session={0} 必讀={1} 可略讀={2}".format(session_status, n_recent, n_hi))
    manifest["koyfin_session_status"] = session_status
    return transcripts_obj


def _run_subprocess(cmd, manifest, step_name, cwd=None):
    r = subprocess.run(
        [str(c) for c in cmd], cwd=str(cwd or REPO_ROOT),
        capture_output=True, text=True,
    )
    manifest["steps"].append({
        "step": step_name,
        "cmd": " ".join(str(c) for c in cmd),
        "returncode": r.returncode,
    })
    return r


# ---------------------------------------------------------------------------
# plan
# ---------------------------------------------------------------------------

def cmd_plan(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    run_dir = _run_dir(ticker, date)
    parts_dir = run_dir / "parts"
    prompts_dir = run_dir / "prompts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    py = _pick_python()

    manifest = {
        "ticker": ticker,
        "date": date,
        "state": "planning",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "steps": [],
        "agents": [],
    }

    # 1. dd_prior.py（零 LLM，前份 DD／q.py 帳本／canonical ID／逐字稿路徑）
    prior_out = parts_dir / "prior.json"
    r = _run_subprocess(
        [py, SCRIPTS_DIR / "dd_prior.py", ticker, "--date", date, "--out", prior_out],
        manifest, "dd_prior",
    )
    prior = {}
    if r.returncode != 0:
        print("[warn] dd_prior.py 失敗（exit {0}）：{1}".format(
            r.returncode, r.stderr.strip()[-500:]), file=sys.stderr)
    elif prior_out.exists():
        try:
            prior = _load_json(prior_out)
        except Exception as e:
            print("[warn] prior.json 解析失敗：{0}".format(e), file=sys.stderr)

    # 2. archetype 解析
    archetype, src = _resolve_archetype(args.archetype, prior)
    if not archetype:
        archetype = DEFAULT_ARCHETYPE
        src = "default_fallback"
        print(
            "[warn] 未給 --archetype 且 prior.json 無可用 archetype_hint（前份 DD "
            "可能是不含 archetype 欄位的 legacy schema），退回基準 archetype={0!r}"
            "（coverage-axes.md by_archetype 附加軸數=0，即僅 common 軸）".format(archetype),
            file=sys.stderr,
        )
    print("archetype={0!r}（來源：{1}）".format(archetype, src))
    manifest["archetype"] = archetype
    manifest["archetype_source"] = src

    # 3. dd_evidence.py init（既有腳本固定寫到 .dd_build/{T}_{D}.evidence.json，
    #    搬一份進 run 目錄；不改該腳本行為）
    init_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "init", ticker, date,
        "--archetype", archetype,
    ]
    if args.segments:
        init_cmd += ["--segments", args.segments]
    r = _run_subprocess(init_cmd, manifest, "dd_evidence_init")
    if r.returncode != 0:
        print("[error] dd_evidence.py init 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    evidence_flat = BUILD_DIR / "{0}_{1}.evidence.json".format(ticker, date)
    evidence_dest = run_dir / "evidence.json"
    if evidence_flat.exists():
        evidence_dest.write_text(evidence_flat.read_text(encoding="utf-8"), encoding="utf-8")

    # 4. dd_evidence.py axes --json
    axes_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "axes",
        "--archetype", archetype, "--json", "--ticker", ticker,
    ]
    if args.segments:
        axes_cmd += ["--segments", args.segments]
    r = _run_subprocess(axes_cmd, manifest, "dd_evidence_axes")
    if r.returncode != 0:
        print("[error] dd_evidence.py axes 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    try:
        axes = json.loads(r.stdout)
    except Exception as e:
        print("[error] axes --json 輸出不是合法 JSON：{0}".format(e), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    _atomic_write_json(run_dir / "axes.json", axes)

    # 5. numbers_extra（--offline 時跳過；失敗只 warn 不 abort）
    if args.offline:
        manifest["steps"].append({"step": "dd_numbers_extra", "skipped": "offline"})
    else:
        peers_str, peers_src = _resolve_peers(args.peers, ticker)
        if not peers_str:
            print(
                "[error] 找不到可用對手清單（--peers 未給、{0}/{1}_*/ 無歷史 "
                "numbers.peer_financials、docs/id/ID_*.html 無含 {1} 的 "
                "related_tickers）：請帶 --peers a,b 手動指定（strict 會擋 <2 "
                "對手，早停比晚停省）".format(SRC_ARCHIVE_DIR, ticker),
                file=sys.stderr,
            )
            _atomic_write_json(run_dir / "manifest.json", manifest)
            return 1
        print("peers={0!r}（來源：{1}）".format(peers_str, peers_src))
        manifest["peers"] = peers_str
        manifest["peers_source"] = peers_src
        numbers_extra_out = parts_dir / "numbers_extra.json"
        ne_cmd = [py, SCRIPTS_DIR / "dd_numbers_extra.py", ticker, date, "--out", numbers_extra_out,
                  "--peers", peers_str]
        if evidence_dest.exists():
            ne_cmd += ["--evidence", evidence_dest]
        r = _run_subprocess(ne_cmd, manifest, "dd_numbers_extra")
        if r.returncode != 0:
            print("[warn] dd_numbers_extra.py 失敗（不 abort）：{0}".format(
                r.stderr.strip()[-500:]), file=sys.stderr)

    # 5b. Koyfin 逐字稿（WP7a #1：零 LLM，plan 內直接跑，立刻 merge 進
    # evidence.json；失敗只 warn，不 abort）
    transcripts_obj = _run_koyfin_step(ticker, date, run_dir, evidence_dest, manifest)

    # 6. 軸分批：major_events 單獨一批，其餘每 --axes-per-batch 軸一批
    axis_list = axes if isinstance(axes, list) else []
    major = [a for a in axis_list if a.get("id") == "major_events"]
    rest = [a for a in axis_list if a.get("id") != "major_events"]
    batches = []
    if major:
        batches.append(major)
    step = max(1, args.axes_per_batch)
    for i in range(0, len(rest), step):
        batches.append(rest[i:i + step])

    spawn_list = []
    for k, batch in enumerate(batches, start=1):
        is_major = any(a.get("id") == "major_events" for a in batch)
        part_rel = "parts/axes_{0}.json".format(k)
        part_path = run_dir / part_rel
        mapping = {
            "TICKER": ticker,
            "N_AXES": str(len(batch)),
            "AXES_BLOCK": _axis_block(batch),
            "PART_PATH": str(part_path),
            "EVENTS_BLOCK": EVENTS_ADDENDUM if is_major else "",
            "EVENTS_JSON_KEY": (',\n  "events": ' + EVENTS_JSON_SAMPLE) if is_major else "",
        }
        prompt_text = _render_template(PROMPTS_TMPL_DIR / "coverage.md.tmpl", mapping)
        prompt_rel = "prompts/a_{0}.md".format(k)
        (run_dir / prompt_rel).write_text(prompt_text, encoding="utf-8")
        spawn_list.append({
            "id": "a_{0}".format(k),
            "model": "sonnet",
            "prompt": prompt_rel,
            "out": part_rel,
            "tools": SPAWN_TOOLS_COVERAGE,
            "max_turns": 8,  # 2026-09-05：覆蓋子 agent 實測 8–13 輪、0.4–0.8M，是 Stage 0 最大項；壓到 8 逼它每軸 ≤3 輪搜尋
            "budget_cache_read": BUDGET_CACHE_READ_COVERAGE,
        })

    # a1_numbers
    numbers_mapping = {
        "TICKER": ticker,
        "DATE": date,
        "PART_PATH": str(parts_dir / "numbers_collect.json"),
        "NUMBERS_EXTRA_PATH": str(parts_dir / "numbers_extra.json"),
    }
    (prompts_dir / "a1_numbers.md").write_text(
        _render_template(PROMPTS_TMPL_DIR / "numbers.md.tmpl", numbers_mapping), encoding="utf-8")
    spawn_list.append({
        "id": "a1_numbers", "model": "sonnet", "prompt": "prompts/a1_numbers.md",
        "out": "parts/numbers_collect.json", "tools": SPAWN_TOOLS_NUMBERS,
        "max_turns": 15, "budget_cache_read": BUDGET_CACHE_READ_NUMBERS,
    })

    # a2_{k}（WP7d：一篇逐字稿一個 spawn，取代原本一人讀全部的 a2_digest——
    # HPE 實測一人讀三篇 17 輪撞 16 上限、cache_read 2.54M 超 1.5M 預算；
    # 拆開後單篇約 0.5M×3≈1.5M 且可平行）。範圍＝
    # transcripts.selected.recent_four_quarters[:-1]（去掉最後一篇＝最新一
    # 季，留給判斷 agent 親讀）＋ high_signal_optional[]（若有），順序與
    # digest.md.tmpl 既有規則一致。
    sel = ((transcripts_obj or {}).get("transcripts") or {}).get("selected") or {}
    recent4 = sel.get("recent_four_quarters") or []
    optional = sel.get("high_signal_optional") or []
    digest_targets = list(recent4[:-1]) + list(optional)

    digest_targets_meta = []
    for k, file_path in enumerate(digest_targets, start=1):
        part_rel = "parts/digest_{0}.json".format(k)
        digest_mapping = {
            "TICKER": ticker,
            "DATE": date,
            "TRANSCRIPT_FILE": str(file_path),
            "PART_PATH": str(run_dir / part_rel),
        }
        prompt_rel = "prompts/a2_{0}.md".format(k)
        (run_dir / prompt_rel).write_text(
            _render_template(PROMPTS_TMPL_DIR / "digest.md.tmpl", digest_mapping), encoding="utf-8")
        spawn_id = "a2_{0}".format(k)
        spawn_list.append({
            "id": spawn_id, "model": "sonnet", "prompt": prompt_rel,
            "out": part_rel, "tools": SPAWN_TOOLS_DIGEST,
            "max_turns": DIGEST_PER_FILE_MAX_TURNS,
            "budget_cache_read": BUDGET_CACHE_READ_DIGEST_PER_FILE,
        })
        digest_targets_meta.append({"id": spawn_id, "file": str(file_path), "out": part_rel})
    _atomic_write_json(run_dir / "digest_targets.json", digest_targets_meta)

    # digest.json 路徑本身零 LLM、plan 當下就確定，直接寫成 part（WP1b
    # _select_parts 固定會挑 parts/digest_path.json 合併進 evidence.json 的
    # transcripts.digest_path，strict 驗證靠它判斷「>1 篇逐字稿時 0e 摘要是否
    # 已接線」；不必等 a2_{k} agent 交稿才知道這個路徑——finalize 前
    # `_merge_digest_parts` 會把 parts/digest_*.json 合併成這個檔）。
    _atomic_write_json(parts_dir / "digest_path.json",
                        {"transcripts": {"digest_path": str(run_dir / "digest.json")}})

    _atomic_write_json(run_dir / "spawn_list.json", spawn_list)

    # WP1d：另存每批軸清單（batch id → axis_ids／is_major），供 --replay-from
    # 重放時比對「這一批該回填哪幾個軸」，不用去反解析 prompt 文字。
    batches_meta = []
    for k, batch in enumerate(batches, start=1):
        batches_meta.append({
            "id": "a_{0}".format(k),
            "axis_ids": [a.get("id") for a in batch],
            "is_major": any(a.get("id") == "major_events" for a in batch),
        })
    _atomic_write_json(run_dir / "batches.json", batches_meta)

    manifest["state"] = "planned"
    manifest["agents"] = [s["id"] for s in spawn_list]
    _atomic_write_json(run_dir / "manifest.json", manifest)

    print("\n{0:14s} {1:8s} {2:10s} {3}".format("id", "model", "max_turns", "out"))
    for s in spawn_list:
        print("{0:14s} {1:8s} {2:<10d} {3}".format(s["id"], s["model"], s["max_turns"], s["out"]))
    print("\n共 {0} 個 spawn，寫入 {1}".format(len(spawn_list), run_dir))
    return 0


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

_TOP_LEVEL_FILES = [
    "evidence.json", "axes.json", "spawn_list.json", "digest.json",
    "judgment.json", "scenario.json", "scenario_meta.json",
]
_SUBDIRS = ["parts", "prompts", "agents", "tables", "prose", "bundles"]


def cmd_status(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        print("[error] 找不到 run 目錄或 manifest：{0}".format(manifest_path), file=sys.stderr)
        return 1
    manifest = _load_json(manifest_path)
    print("ticker={0} date={1} state={2} created={3}".format(
        manifest.get("ticker"), manifest.get("date"), manifest.get("state"), manifest.get("created")))
    print("archetype={0!r}（來源：{1}）".format(manifest.get("archetype"), manifest.get("archetype_source")))
    print("steps={0} agents={1}".format(len(manifest.get("steps", [])), len(manifest.get("agents", []))))

    print()
    for name in _TOP_LEVEL_FILES:
        p = run_dir / name
        if p.exists():
            print("[ok      ] {0:24s} {1:>10d} bytes".format(name, p.stat().st_size))
        else:
            print("[missing ] {0:24s} —".format(name))

    for sub in _SUBDIRS:
        d = run_dir / sub
        if d.exists():
            files = sorted(f for f in d.iterdir() if f.is_file())
            print("\n{0}/ （{1} 檔）".format(sub, len(files)))
            for f in files:
                print("  {0:30s} {1:>10d} bytes".format(f.name, f.stat().st_size))
        else:
            print("\n{0}/  missing".format(sub))
    return 0


# ---------------------------------------------------------------------------
# WP1d small helpers：時間戳、format_map 安全渲染、replay marker、log 印格式
# ---------------------------------------------------------------------------

def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


class _SafeFormatDict(dict):
    """`str.format_map` 用：缺的變數給空字串，不 KeyError。

    judge.md.tmpl／gate.md.tmpl／judge_patch.md.tmpl 用單括號 `{var}`（其他
    大括號已在檔內寫成 `{{ }}`），依協調者指示改走 format_map，不再用
    `plan` 那組舊模板的 `{{VAR}}` 字面取代法。
    """

    def __missing__(self, key):
        return ""


def _render_format_template(tmpl_path, mapping):
    text = Path(tmpl_path).read_text(encoding="utf-8")
    return text.format_map(_SafeFormatDict(mapping))


BUNDLE_SEPARATOR = "\n\n===== BUNDLE =====\n\n"


def _write_inline_prompt(prompt_path, extra_content_path):
    """WP7b #1：judge／gate／patch 三種 prompt 渲染完模板後，把 bundle
    （或修補時的 judgment.json 全文）整段接在 prompt 之後（分隔行
    `===== BUNDLE =====`），寫成一個新的 `*_inline.md` 檔給 `dd_headless.spawn`
    當真正的 prompt（經 stdin 餵給 `claude -p`，無長度上限）。模板本身的
    「讀」段已改為「不要 Read 任何檔」，原本較短的 `prompt_path` 仍保留
    （供人工核對渲染結果），不再是實際餵給 agent 的內容。

    理由：Fable 判斷 agent 曾為了讀 240KB 的 judge bundle 花到撞 8 輪
    上限（見 notes/site-internal/dd/_wp_spec_v17_batch5_20260905.md
    WP7b #1 的 AVGO 實測記錄）。
    """
    prompt_path = Path(prompt_path)
    extra_path = Path(extra_content_path)
    extra_text = extra_path.read_text(encoding="utf-8") if extra_path.exists() else ""
    combined = prompt_path.read_text(encoding="utf-8") + BUNDLE_SEPARATOR + extra_text
    inline_path = prompt_path.with_name(prompt_path.stem + "_inline" + prompt_path.suffix)
    inline_path.write_text(combined, encoding="utf-8")
    return inline_path


def _print_step_status(step, actual, target, status):
    print("{0}／實測={1}／目標={2}／{3}".format(step, actual, target, status))


def _print_resume_hint(ticker, date, stage):
    print(
        "中斷於 {0}。可用 --resume 從此處接續：\n"
        "  python3 scripts/ddreport.py run {1} --date {2} --resume".format(
            stage, ticker, date
        )
    )


def _load_json_or(path, default):
    path = Path(path)
    if not path.exists():
        return default
    try:
        return _load_json(path)
    except Exception:
        return default


REPLAY_FAKE_CLAUDE = SCRIPTS_DIR / "tests" / "fake_claude.py"


def _ensure_replay_env(replay_from):
    """`--replay-from DIR` 啟用時：設 `DD_CLAUDE_BIN` 指向假 binary、
    `DD_REPLAY_FROM` 指向 fixture 目錄（皆轉絕對路徑，因 spawn 可能以
    run_dir 為 cwd 呼叫子行程）。回傳絕對化後的 Path，或 None。"""
    if not replay_from:
        return None
    replay_dir = Path(replay_from).resolve()
    os.environ["DD_CLAUDE_BIN"] = str(REPLAY_FAKE_CLAUDE.resolve())
    os.environ["DD_REPLAY_FROM"] = str(replay_dir)
    return replay_dir


def _append_replay_marker(prompt_path, obj):
    """把 `<!-- DD_REPLAY {json} -->` 附在 prompt 檔尾——`fake_claude.py`
    的 replay 模式只認這個 marker（不去猜測散文措辭），marker 只在
    `--replay-from` 生效時附加，正式跑（真 claude）不受影響。"""
    prompt_path = Path(prompt_path)
    if not prompt_path.exists():
        return
    text = prompt_path.read_text(encoding="utf-8")
    marker = "\n\n<!-- DD_REPLAY {0} -->\n".format(json.dumps(obj, ensure_ascii=False))
    prompt_path.write_text(text + marker, encoding="utf-8")


def _apply_replay_markers_stage0(run_dir, replay_dir):
    """Stage 0 三類 spawn（覆蓋軸批次／數字／逐字稿摘要）prompt 逐一附
    replay marker。批次的軸清單讀 `batches.json`（`plan` 時已寫出）；摘要的
    逐篇清單讀 `digest_targets.json`（WP7d：一篇一個 spawn，`plan` 時已寫
    出）。Koyfin 已於 WP7a 改零 LLM，plan 內直接跑，不再是 spawn，不需要
    marker。"""
    if not replay_dir:
        return
    prompts_dir = run_dir / "prompts"
    batches = _load_json_or(run_dir / "batches.json", [])
    for b in batches:
        bid = b["id"]
        k = bid.split("_", 1)[1]
        out_path = run_dir / "parts" / "axes_{0}.json".format(k)
        _append_replay_marker(prompts_dir / "{0}.md".format(bid), {
            "kind": "coverage", "axes": b.get("axis_ids") or [],
            "major": bool(b.get("is_major")), "out": str(out_path),
        })
    _append_replay_marker(prompts_dir / "a1_numbers.md", {
        "kind": "numbers", "out": str(run_dir / "parts" / "numbers_collect.json"),
    })
    digest_targets = _load_json_or(run_dir / "digest_targets.json", [])
    for dt in digest_targets:
        out_path = run_dir / dt["out"]
        _append_replay_marker(prompts_dir / "{0}.md".format(dt["id"]), {
            "kind": "digest", "file": dt.get("file"), "out": str(out_path),
        })


# ---------------------------------------------------------------------------
# WP1d stage0：plan（未 plan 時，Koyfin 於 plan 內零 LLM 完成）→ spawn_many
# 覆蓋/數字/摘要 → finalize（WP7a #4：resume 時只重派需要的部分）
# ---------------------------------------------------------------------------

_DIGEST_PART_RE = re.compile(r"^digest_(\d+)\.json$")


def _merge_digest_parts(run_dir):
    """WP7d：零 LLM 合併 `parts/digest_{k}.json`（每篇逐字稿一個 spawn 交回
    的片段，形狀同 `digest.json`：`{source_files, items, qa_flags}`）成單一
    `digest.json`（形狀不變，`validate_digest.py` 直接吃）。依檔名數字序合
    併，`source_files` 依序去重、`items`／`qa_flags` 直接接尾。沒有任何
    `digest_*.json`（例如 Koyfin 找不到逐字稿）時寫出空殼，維持既有
    fallback 語意。"""
    parts_dir = Path(run_dir) / "parts"
    digest_files = []
    if parts_dir.exists():
        for f in parts_dir.iterdir():
            m = _DIGEST_PART_RE.match(f.name)
            if m:
                digest_files.append((int(m.group(1)), f))
    digest_files.sort(key=lambda t: t[0])

    source_files, items, qa_flags = [], [], []
    seen = set()
    for _, f in digest_files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for sf in d.get("source_files") or []:
            if sf not in seen:
                seen.add(sf)
                source_files.append(sf)
        items.extend(d.get("items") or [])
        qa_flags.extend(d.get("qa_flags") or [])

    merged = {"source_files": source_files, "items": items, "qa_flags": qa_flags}
    _atomic_write_json(Path(run_dir) / "digest.json", merged)
    return merged


def _finalize_run_dir(run_dir):
    """跑 `dd_evidence.py finalize --run-dir DIR`，回傳
    (returncode, 原始輸出全文, 需重派的 part 檔名 set)。finalize 前先零
    LLM 合併 `parts/digest_{k}.json` 成 `digest.json`（WP7d）——digest 不在
    `dd_evidence.py` 的 merge 範圍內（那是 evidence.json 的 merge），故在
    這裡自己補做，確保每次 finalize（含 resume／retry）看到的 digest.json
    都是最新片段的合併結果。"""
    _merge_digest_parts(run_dir)
    py = _pick_python()
    r = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_evidence.py"), "finalize", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    needs = set()
    in_block = False
    for line in (r.stdout or "").splitlines():
        if line.startswith("需重派"):
            in_block = True
            continue
        if in_block:
            m = re.match(r"\s*✗\s+(\S+)", line)
            if m:
                needs.add(m.group(1))
            elif not line.startswith("      "):
                in_block = False
    return r.returncode, out, needs


def _spec_out_basename(spec):
    return Path(spec.get("out", "")).name


def _spawn_spec_for(spec, run_dir):
    """把 `spawn_list.json` 一筆 spec 轉成餵給 `dd_headless.spawn_many` 的呼叫
    參數。**刻意不把 `spec["out"]`（子 agent 應該用 Write 工具寫入的實際產物
    路徑，如 `parts/axes_1.json`）當作 `dd_headless.spawn` 的 `out_json`**——
    `out_json` 存的是 `claude -p` 子行程的原始回傳 JSON（`result`／usage 等
    metadata），跟子 agent 用 Write 工具寫出的工作產物是兩個不同的檔；兩者
    共用同一路徑會讓 dd_headless 收工時把原始回傳包整個蓋掉子 agent 真正寫
    的內容（replay 模式下觀測到此問題）。原始回傳改存 `agents/{id}.json`
    供除錯用，`spec["out"]` 只作為「finalize 後去哪裡找這批產物」的紀錄，
    不動它的語意。"""
    s = dict(spec)
    s["run_dir"] = str(run_dir)
    s["out"] = str(Path(run_dir) / "agents" / "{0}.json".format(spec.get("id", "spawn")))
    return s


def _do_stage0(ticker, date, plan_kwargs, replay_dir, accept_over_budget, manifest):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = {"state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False}
    manifest.setdefault("stages", {})["stage0"] = stage
    manifest["state"] = "stage0_running"
    _atomic_write_json(manifest_path, manifest)

    if not (run_dir / "spawn_list.json").exists():
        plan_args = argparse.Namespace(
            ticker=ticker, date=date,
            archetype=plan_kwargs.get("archetype"),
            peers=plan_kwargs.get("peers"),
            segments=plan_kwargs.get("segments"),
            axes_per_batch=plan_kwargs.get("axes_per_batch") or AXES_PER_BATCH_DEFAULT,
            offline=plan_kwargs.get("offline", False),
        )
        rc = cmd_plan(plan_args)
        if rc != 0:
            manifest = _load_json(manifest_path)
            stage = manifest.setdefault("stages", {}).setdefault("stage0", stage)
            stage["state"] = "FAIL"
            stage["ended"] = _now()
            stage["note"] = "plan 失敗"
            _atomic_write_json(manifest_path, manifest)
            _print_step_status("stage0", "plan_rc={0}".format(rc), "PASS", "FAIL")
            return 1
        manifest = _load_json(manifest_path)
        manifest.setdefault("stages", {})["stage0"] = stage

    # offline + replay：零 LLM 的 dd_numbers_extra.py 在 plan 時被 --offline 跳過，
    # 但 finalize 仍需要這份歷史快照才能 strict 通過——from fixture 直接補進
    # parts/（這是刻意的 replay-only 補洞，不影響非 replay 的正常 plan 行為）。
    if replay_dir and plan_kwargs.get("offline"):
        src = replay_dir / "parts" / "numbers_extra.json"
        dst = run_dir / "parts" / "numbers_extra.json"
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    if replay_dir:
        _apply_replay_markers_stage0(run_dir, replay_dir)
        # 回溯重放時，「今天」常常等於 fixture 原本的報告日期（甚至該日期
        # 已有上站報告），這時 plan 剛跑的**即時** dd_prior.py 會把「同一天
        # 已上站的那份報告自己」誤當成 prior（自我參照），judge check 的
        # QC-49 漂移歸因因此對不上。改用 fixture 當時真正捕捉到的
        # parts/prior.json（產這份報告當下、報告本身還不存在時的歷史快照）
        # 才是對的 replay 語意——這只在 --replay-from 生效，不影響正常路徑。
        fixture_prior = replay_dir / "parts" / "prior.json"
        if fixture_prior.exists():
            (run_dir / "parts" / "prior.json").write_text(
                fixture_prior.read_text(encoding="utf-8"), encoding="utf-8")

    spawn_list = _load_json_or(run_dir / "spawn_list.json", [])

    # WP7a #4：重派真的重派——resume 情境（此 run_dir 已有部分 part 檔，代表
    # 先前跑過一輪 stage0 但未整體 PASS）不盲目重派全部：先問一次 finalize
    # 拿「需重派」清單，只重派清單內＋完全沒產出過的 spec；全新 run（尚無
    # 任何本批產物）才維持「全部 spawn」。`--resume` 進到 stage0 時走的是
    # 同一個 `_do_stage0` 入口，故也吃到這條路徑，不是只重跑 finalize。
    has_existing_output = any(
        (run_dir / s.get("out", "")).exists() for s in spawn_list
    )
    if has_existing_output:
        _, _, needs0 = _finalize_run_dir(run_dir)
        to_spawn = [
            s for s in spawn_list
            if _spec_out_basename(s) in needs0 or not (run_dir / s.get("out", "")).exists()
        ]
        if to_spawn:
            print("[stage0] resume：只重派 {0}".format(
                ", ".join(s["id"] for s in to_spawn)))
    else:
        to_spawn = spawn_list

    other_specs = [_spawn_spec_for(s, run_dir) for s in to_spawn]
    if other_specs:
        stage["agent_usage"].extend(dd_headless.spawn_many(other_specs, max_parallel=4))

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget

    rc, out_text, needs = _finalize_run_dir(run_dir)
    retries = 0
    while needs and rc != 0 and retries < 2:
        retry_specs = [
            _spawn_spec_for(s, run_dir)
            for s in spawn_list
            if _spec_out_basename(s) in needs
        ]
        if not retry_specs:
            break
        stage["agent_usage"].extend(dd_headless.spawn_many(retry_specs, max_parallel=4))
        rc, out_text, needs = _finalize_run_dir(run_dir)
        retries += 1
    stage["finalize_retries"] = retries
    stage["finalize_tail"] = out_text[-3000:]

    ok = (rc == 0) and (over_budget is False or accept_over_budget)
    stage["state"] = "PASS" if ok else ("FAIL" if rc != 0 else "OVER_BUDGET")
    stage["ended"] = _now()
    manifest["stages"]["stage0"] = stage
    manifest["state"] = "stage0_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "stage0",
        "finalize_rc={0} retries={1} over_budget={2}".format(rc, retries, over_budget),
        "finalize PASS",
        stage["state"],
    )
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "stage0")
    return 0 if stage["state"] == "PASS" else 1


# ---------------------------------------------------------------------------
# WP1d judge：bundle → prompt(judge.md.tmpl) → spawn → judge check → 修一輪
# ---------------------------------------------------------------------------

def _judge_check(ticker, date):
    """`ddreport.py judge check TICKER DATE`：依序跑 dd_scenario.py／
    dd_decision.py run／validate_judgment.py --fix --report，回傳
    (ok, report_text)。`validate_judgment.py --report` 恆 exit 0，PASS/FAIL
    要從輸出的 `[PASS]`／`[FAIL]` 首行判斷，不能只看 returncode。"""
    run_dir = _run_dir(ticker, date)
    py = _pick_python()
    scenario_path = run_dir / "scenario.json"
    judgment_path = run_dir / "judgment.json"
    evidence_path = run_dir / "evidence.json"
    tables_dir = run_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    parts = []
    ok = True

    if not scenario_path.exists():
        parts.append("[error] 找不到 {0}".format(scenario_path))
        ok = False
    else:
        r1 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_scenario.py"), str(scenario_path),
             "--html", str(tables_dir / "e11.html"), "--meta", str(run_dir / "scenario_meta.json")],
            capture_output=True, text=True,
        )
        parts.append("[dd_scenario.py] rc={0}\n{1}".format(r1.returncode, (r1.stdout + r1.stderr).strip()))
        ok = ok and (r1.returncode == 0)

    if not judgment_path.exists():
        parts.append("[error] 找不到 {0}".format(judgment_path))
        ok = False
    else:
        r2 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_decision.py"), "run", str(judgment_path),
             "--html", str(tables_dir / "audit.html"), "--json", str(judgment_path)],
            capture_output=True, text=True,
        )
        parts.append("[dd_decision.py run] rc={0}\n{1}".format(r2.returncode, (r2.stdout + r2.stderr).strip()))
        ok = ok and (r2.returncode == 0)

        vj_cmd = [py, str(SCRIPTS_DIR / "validate_judgment.py"), str(judgment_path),
                  "--evidence", str(evidence_path), "--fix", "--report"]
        if os.environ.get("DD_J1_WARN") == "1":
            vj_cmd.append("--j1-warn")
        r3 = subprocess.run(vj_cmd, capture_output=True, text=True)
        vj_out = (r3.stdout + r3.stderr).strip()
        parts.append("[validate_judgment.py] rc={0}\n{1}".format(r3.returncode, vj_out))
        if re.search(r"^\[FAIL\]", vj_out, re.M):
            ok = False
        elif not re.search(r"^\[PASS\]", vj_out, re.M):
            ok = False

    return ok, "\n\n".join(parts)


def cmd_judge_check(args):
    ok, report = _judge_check(args.ticker.strip().upper(), args.date)
    print(report)
    return 0 if ok else 1


def _read_decision_verdict(run_dir):
    j = _load_json_or(run_dir / "judgment.json", {})
    return ((j.get("decision_out") or {}).get("verdict"))


def _do_judge(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = {"state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False}
    manifest.setdefault("stages", {})["judged"] = stage
    manifest["judgment_model"] = judgment_model
    manifest["state"] = "judged_running"
    _atomic_write_json(manifest_path, manifest)

    py = _pick_python()
    bundle_path = run_dir / "bundles" / "judge.md"
    rb = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_bundle.py"), "judge", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    if rb.returncode != 0:
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_bundle.py judge 失敗：{0}".format((rb.stdout + rb.stderr)[-1000:])
        manifest["stages"]["judged"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("judged", "bundle_rc={0}".format(rb.returncode), "PASS", "FAIL")
        _print_resume_hint(ticker, date, "judged")
        return 1

    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    prompt_path = run_dir / "prompts" / "b1_judge.md"
    mapping = {
        "run_dir": str(run_dir), "bundle_path": str(bundle_path),
        "judgment_path": str(judgment_path), "scenario_path": str(scenario_path),
        "ticker": ticker, "date": date, "max_turns": str(JUDGE_MAX_TURNS),
    }
    prompt_path.write_text(_render_format_template(PROMPTS_TMPL_DIR / "judge.md.tmpl", mapping), encoding="utf-8")
    if replay_dir:
        _append_replay_marker(prompt_path, {
            "kind": "judgment", "judgment_out": str(judgment_path), "scenario_out": str(scenario_path),
        })

    inline_prompt_path = _write_inline_prompt(prompt_path, bundle_path)

    agents_dir = run_dir / "agents"
    r_spawn = dd_headless.spawn(
        prompt_path=inline_prompt_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
        max_turns=JUDGE_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
        out_json=agents_dir / "judge_1.json", cwd=run_dir,
    )
    stage["agent_usage"].append(r_spawn)

    ok, report = _judge_check(ticker, date)
    return _judge_finalize_after_check(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        agents_dir, ok, report, fix_suffix="1",
    )


def _judge_finalize_after_check(ticker, date, judgment_model, replay_dir, accept_over_budget,
                                 manifest, stage, agents_dir, ok, report, fix_suffix="1"):
    """判斷物已寫出（或沿用既有）、`judge check` 剛跑過一次的結果為
    `(ok, report)`：FAIL 時派一輪『定點修正』agent、重跑一次 check；把結果
    收斂進 `stage` 並回寫 manifest。共用於 `_do_judge`（首次判斷後）與
    WP7b #5 的 `--resume`（`judged_fail` 狀態先重跑 judge check，FAIL 才
    派修補 agent，不重派整段判斷）。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    stage.setdefault("agent_usage", [])

    if not ok:
        fix_path = run_dir / "prompts" / "b1_fix.md"
        fix_text = (
            "你是 stock-analyst v17 判斷 agent，回來做一輪定點修正。標的 {0}（{1}）。\n\n"
            "`judge check` 的失敗原文如下，**只准改被點名的欄位**，改完一次 Write 整檔 "
            "`{2}`，重跑：\n\n"
            "```\npython3 scripts/ddreport.py judge check {0} {1}\n```\n\n"
            "≤1 輪；仍 FAIL 就照實回報。\n\n## judge check 失敗原文\n\n```\n{3}\n```\n"
        ).format(ticker, date, judgment_path, report)
        fix_path.write_text(fix_text, encoding="utf-8")
        if replay_dir:
            _append_replay_marker(fix_path, {
                "kind": "judgment", "judgment_out": str(judgment_path), "scenario_out": str(scenario_path),
            })
        r_spawn2 = dd_headless.spawn(
            prompt_path=fix_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
            max_turns=JUDGE_FIX_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
            out_json=agents_dir / "judge_fix_{0}.json".format(fix_suffix), cwd=run_dir,
        )
        stage["agent_usage"].append(r_spawn2)
        ok, report = _judge_check(ticker, date)

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget
    stage["check_report_tail"] = report[-4000:]
    j1_warn = None
    m = re.search(r"（(\d+) FAIL／(\d+) WARN）", report)
    if m:
        j1_warn = {"fail": int(m.group(1)), "warn": int(m.group(2))}
    stage["validate_summary"] = j1_warn

    final_ok = ok and (over_budget is False or accept_over_budget)
    stage["state"] = "PASS" if final_ok else ("OVER_BUDGET" if (ok and over_budget) else "FAIL")
    stage["ended"] = _now()
    manifest.setdefault("stages", {})["judged"] = stage
    manifest["state"] = "judged_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "judged", "ok={0} over_budget={1} validate={2}".format(ok, over_budget, j1_warn),
        "validate PASS", stage["state"],
    )
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "judged")
    return 0 if stage["state"] == "PASS" else 1


def _resume_judge_stage(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest):
    """WP7b #5：`--resume` 落在 `judged_fail`（或 judged 段先前狀態為
    FAIL）時的專用入口。判斷物可能已被機械層（`validate_judgment.py --fix`）
    或人工直接修正過，先重跑一次 `judge check`——PASS 就不再燒一次完整
    判斷 agent，直接把 judged 標成功；FAIL 才派一輪『定點修正』agent
    （沿用 `_judge_finalize_after_check` 的 fix 流程），仍然不重派整段判斷
    agent。見 notes/site-internal/dd/_wp_spec_v17_batch5_20260905.md WP7b #5。
    """
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = manifest.setdefault("stages", {}).get("judged") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    stage.setdefault("agent_usage", [])
    stage["resume_precheck"] = True
    agents_dir = run_dir / "agents"

    ok, report = _judge_check(ticker, date)
    if ok:
        stage["state"] = "PASS"
        stage["ended"] = _now()
        stage["check_report_tail"] = report[-4000:]
        stage["resume_note"] = "resume：judge check 免修即過（判斷物已由機械或人工修正），未派任何 agent"
        manifest["stages"]["judged"] = stage
        manifest["state"] = "judged_pass"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("judged", "resume judge check", "validate PASS", "PASS")
        return 0

    return _judge_finalize_after_check(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        agents_dir, ok, report, fix_suffix="resume",
    )


# ---------------------------------------------------------------------------
# WP1d gate：dd_gate.py／dd_brief.py 由 WP3／WP4a 並行交付；不存在時印警告跳過
# ---------------------------------------------------------------------------

def _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, _depth=0):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    dd_gate_path = SCRIPTS_DIR / "dd_gate.py"
    stage = manifest.setdefault("stages", {}).get("gated") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_running"
    _atomic_write_json(manifest_path, manifest)

    if not dd_gate_path.exists():
        print("[warn] scripts/dd_gate.py 不存在（WP3 尚未交付），gate 步驟跳過")
        stage["state"] = "SKIPPED"
        stage["ended"] = _now()
        stage["note"] = "dd_gate.py missing"
        manifest["stages"]["gated"] = stage
        manifest["state"] = "gated_skipped"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "dd_gate.py missing", "PASS", "SKIPPED")
        return 0

    py = _pick_python()
    rb = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_bundle.py"), "gate", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    if rb.returncode != 0:
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_bundle.py gate 失敗：{0}".format((rb.stdout + rb.stderr)[-1000:])
        manifest["stages"]["gated"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "bundle_rc={0}".format(rb.returncode), "PASS", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    audit_path = run_dir / "gate_audit.md"
    gate_bundle_path = run_dir / "bundles" / "gate.md"
    gate_prompt_path = run_dir / "prompts" / "g_gate.md"
    mapping = {
        "run_dir": str(run_dir), "bundle_path": str(gate_bundle_path),
        "ticker": ticker, "date": date, "audit_path": str(audit_path),
        "max_turns": str(GATE_MAX_TURNS),
    }
    gate_prompt_path.write_text(_render_format_template(PROMPTS_TMPL_DIR / "gate.md.tmpl", mapping), encoding="utf-8")
    if replay_dir:
        _append_replay_marker(gate_prompt_path, {"kind": "gate", "out": str(audit_path)})

    inline_gate_prompt_path = _write_inline_prompt(gate_prompt_path, gate_bundle_path)

    gate_model = GATE_MODEL_FOR.get(judgment_model, "opus")
    agents_dir = run_dir / "agents"
    r_spawn = dd_headless.spawn(
        prompt_path=inline_gate_prompt_path, model=gate_model, allowed_tools=["Read", "Write"],
        max_turns=GATE_MAX_TURNS, budget_cache_read=GATE_BUDGET_CACHE_READ,
        out_json=agents_dir / "gate_{0}.json".format(_depth + 1), cwd=run_dir,
    )
    stage["agent_usage"].append(r_spawn)
    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget

    if not audit_path.exists():
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "spawn 未產出 gate_audit.md"
        manifest["stages"]["gated"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "no_audit_file", "PASS", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    return _gate_finalize_from_audit(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        audit_path, _depth=_depth,
    )


def _gate_finalize_from_audit(ticker, date, judgment_model, replay_dir, accept_over_budget,
                               manifest, stage, audit_path, _depth=0):
    """`gate_audit.md` 已存在（剛 spawn 產出，或 WP7b #5 `--resume` 在
    `gated_fail`／`gated_running` 時發現既有稽核檔）：parse 它、red>0 才派
    修補 agent（inline judgment.json 全文，不重跑一次 gate spawn），
    red=0 直接收斂為 PASS／OVER_BUDGET。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    py = _pick_python()
    dd_gate_path = SCRIPTS_DIR / "dd_gate.py"
    agents_dir = run_dir / "agents"
    stage.setdefault("agent_usage", [])

    r_parse = subprocess.run(
        [py, str(dd_gate_path), "parse", str(audit_path), "--json"],
        capture_output=True, text=True,
    )
    parsed = None
    if r_parse.returncode == 0:
        try:
            parsed = json.loads(r_parse.stdout)
        except Exception:
            parsed = None
    stage["gate_parsed"] = parsed

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    red = (parsed or {}).get("red", 0)
    if red and red > 0:
        prior_verdict = _read_decision_verdict(run_dir)
        judgment_path = run_dir / "judgment.json"
        patch_prompt_path = run_dir / "prompts" / "b1_patch.md"
        rp = subprocess.run(
            [py, str(dd_gate_path), "patch-prompt",
             "--audit", str(audit_path), "--judgment", str(judgment_path),
             "--evidence", str(run_dir / "evidence.json"), "--out", str(patch_prompt_path)],
            capture_output=True, text=True,
        )
        if rp.returncode != 0 or not patch_prompt_path.exists():
            stage["state"] = "FAIL"
            stage["ended"] = _now()
            stage["note"] = "dd_gate.py patch-prompt 失敗：{0}".format((rp.stdout + rp.stderr)[-1000:])
            manifest["stages"]["gated"] = stage
            _atomic_write_json(manifest_path, manifest)
            _print_step_status("gated", "patch_prompt_rc={0}".format(rp.returncode), "PASS", "FAIL")
            _print_resume_hint(ticker, date, "gated")
            return 1
        if replay_dir:
            _append_replay_marker(patch_prompt_path, {
                "kind": "judgment", "judgment_out": str(judgment_path),
            })
        inline_patch_prompt_path = _write_inline_prompt(patch_prompt_path, judgment_path)
        r_spawn2 = dd_headless.spawn(
            prompt_path=inline_patch_prompt_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
            max_turns=GATE_PATCH_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
            out_json=agents_dir / "gate_patch_{0}.json".format(_depth + 1), cwd=run_dir,
        )
        stage["agent_usage"].append(r_spawn2)
        over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
        stage["over_budget"] = over_budget

        ok_check, report_check = _judge_check(ticker, date)
        stage["patch_check_tail"] = report_check[-3000:]
        new_verdict = _read_decision_verdict(run_dir)

        if new_verdict != prior_verdict and _depth < 1:
            manifest["stages"]["gated"] = stage
            _atomic_write_json(manifest_path, manifest)
            print("[gate] verdict 翻面（{0} → {1}），重跑一次 gate".format(prior_verdict, new_verdict))
            return _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, _depth=_depth + 1)

        final_ok = ok_check and (over_budget is False or accept_over_budget)
        stage["state"] = "PASS" if final_ok else ("OVER_BUDGET" if (ok_check and over_budget) else "FAIL")
    else:
        stage["over_budget"] = over_budget
        final_ok = (over_budget is False) or accept_over_budget
        stage["state"] = "PASS" if final_ok else "OVER_BUDGET"

    stage["ended"] = _now()
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "gated", "red={0} yellow={1} over_budget={2}".format(
            (parsed or {}).get("red"), (parsed or {}).get("yellow"), stage["over_budget"]),
        "red=0", stage["state"],
    )
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "gated")
    return 0 if stage["state"] == "PASS" else 1


def _resume_gate_stage(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest):
    """WP7b #5：`--resume` 落在 `gated_fail`／`gated_running` 時的專用入口。
    既有 `gate_audit.md` 可能是上一輪已經跑完的稽核結果（只是後續
    parse／patch 步驟中斷），先直接 parse 它，不重新花一次 gate spawn；
    parse 不到（audit 檔不存在）才退回完整 `_do_gate`。"""
    run_dir = _run_dir(ticker, date)
    audit_path = run_dir / "gate_audit.md"
    if not audit_path.exists():
        return _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest)

    stage = manifest.setdefault("stages", {}).get("gated") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    stage.setdefault("agent_usage", [])
    stage["resume_precheck"] = True
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_running"
    _atomic_write_json(run_dir / "manifest.json", manifest)

    return _gate_finalize_from_audit(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage, audit_path,
    )


# ---------------------------------------------------------------------------
# WP1d brief：dd_brief.py（WP4a 交付）零 LLM 渲染；不存在時印警告跳過
# ---------------------------------------------------------------------------

def _do_brief(ticker, date, do_full, manifest, dry_run=False):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    dd_brief_path = SCRIPTS_DIR / "dd_brief.py"
    stage = {"state": "RUNNING", "started": _now()}
    manifest.setdefault("stages", {})["brief"] = stage
    manifest["state"] = "brief_running"
    _atomic_write_json(manifest_path, manifest)

    if not dd_brief_path.exists():
        print("[warn] scripts/dd_brief.py 不存在（WP4a 尚未交付），brief 步驟跳過")
        stage["state"] = "SKIPPED"
        stage["ended"] = _now()
        stage["note"] = "dd_brief.py missing"
        manifest["stages"]["brief"] = stage
        manifest["state"] = "brief_skipped"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("brief", "dd_brief.py missing", "PASS", "SKIPPED")
    else:
        py = _pick_python()
        # WP7a #6：--dry-run 時輸出到 run 目錄內的 brief.html，不寫
        # docs/dd/brief/（避免 dry-run 汙染會上站/被 git 追蹤的目錄）。
        if dry_run:
            out_path = run_dir / "brief.html"
        else:
            out_path = REPO_ROOT / "docs" / "dd" / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            [py, str(dd_brief_path), "--run-dir", str(run_dir), "--out", str(out_path)],
            capture_output=True, text=True,
        )
        stage["out_path"] = str(out_path)
        stage["state"] = "PASS" if r.returncode == 0 else "FAIL"
        stage["ended"] = _now()
        stage["note"] = (r.stdout + r.stderr)[-1000:]
        manifest["stages"]["brief"] = stage
        manifest["state"] = "brief_{0}".format(stage["state"].lower())
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("brief", "rc={0}".format(r.returncode), "PASS", stage["state"])
        if stage["state"] != "PASS":
            _print_resume_hint(ticker, date, "brief")

    if do_full:
        print("[warn] --full 本輪未實作（WP4b 未交付），略過快速版之外的完整渲染")

    return 0 if stage["state"] in ("PASS", "SKIPPED") else 1


# ---------------------------------------------------------------------------
# WP6a: index-row — 從最終 HTML 的 dd-meta 生成 docs/dd/INDEX.md 一列
# ---------------------------------------------------------------------------

_DD_META_RE = re.compile(
    r'<script id="dd-meta"[^>]*>(.*?)</script>', re.S
)
_SUB_P_RE = re.compile(r'<p class="sub[^"]*">(.*?)</p>', re.S)
_TAG_RE = re.compile(r"<[^>]+>")


def _extract_dd_meta(html_text):
    m = _DD_META_RE.search(html_text)
    if not m:
        raise ValueError("dd-meta script block 找不到")
    return json.loads(m.group(1))


def _extract_sub_text(html_text):
    """取 `<p class="sub...">…</p>`（`dd_brief.py render_header` 已把
    `plain.verdict_sub`（有）或 `oneliner`（無，class 多帶 fallback）決定好
    優先序寫進這段），HTML entity 反轉義＋防禦性剝標籤。"""
    m = _SUB_P_RE.search(html_text)
    if not m:
        return None
    text = html_lib.unescape(m.group(1))
    text = _TAG_RE.sub("", text)
    return text.strip()


def _fmt_signed_pct(v, decimals=1):
    if v is None:
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    sign = "+" if v > 0 else ("−" if v < 0 else "")
    return "{0}{1:.{2}f}%".format(sign, abs(v), decimals)


def _index_row_fields(html_path):
    """回傳 dict：`row`（INDEX.md 一列 markdown）＋各拆解欄位，供
    `cmd_index_row`／`_do_finish` 共用（後者拿 meta 組 commit 訊息）。"""
    html_path = Path(html_path)
    text = html_path.read_text(encoding="utf-8")
    meta = _extract_dd_meta(text)
    sub_text = _extract_sub_text(text)

    ticker = meta.get("ticker") or "—"
    date_disp = meta.get("date") or "—"
    schema = meta.get("schema") or "—"

    verdict = meta.get("dca_verdict") or "—"
    role = meta.get("dca_role")
    rearm = meta.get("rearm_trigger")
    verdict_cell = verdict
    if role:
        verdict_cell += "｜" + role
    if rearm:
        verdict_cell += "·rearm＝" + rearm

    trap_label = meta.get("trap_label") or "—"

    moat = meta.get("moat_grade") or meta.get("moat") or "—"
    moat_trend = meta.get("moat_trend") or ""
    val = meta.get("val") or "—"
    trap = meta.get("trap") or "—"
    col6 = "{0}{1}/{2}/{3}".format(moat, moat_trend, val, trap)

    is_brief = bool(meta.get("brief"))
    try:
        rel = html_path.resolve().relative_to(DD_DIR.resolve())
        file_cell = str(rel)
    except ValueError:
        file_cell = html_path.name

    note_lead = sub_text or meta.get("oneliner") or "—"
    number_parts = []
    ev5y = _fmt_signed_pct(meta.get("ev5y_pct"), decimals=1)
    irr = _fmt_signed_pct(meta.get("irr_base_pct"), decimals=1)
    maxdd = _fmt_signed_pct(meta.get("max_dd_pct"), decimals=0)
    if ev5y is not None:
        number_parts.append("EV5y {0}".format(ev5y))
    if irr is not None:
        number_parts.append("IRR {0}/yr".format(irr))
    if maxdd is not None:
        number_parts.append("Max DD {0}".format(maxdd))
    note = note_lead
    if number_parts:
        note += "（{0}）".format("／".join(number_parts))
    suffix = (
        "**v17 快速版（sonnet 收證據→Fable 判斷→opus 閘→零 LLM 渲染）**"
        if is_brief else "**v17 完整版**"
    )
    note += "。" + suffix

    row = "| {date} | {ticker} | {schema} | {verdict} | {trap} | {col6} | {file} | {note} |".format(
        date=date_disp, ticker=ticker, schema=schema, verdict=verdict_cell,
        trap=trap_label, col6=col6, file=file_cell, note=note,
    )
    return {
        "meta": meta,
        "row": row,
        "file_cell": file_cell,
        "ticker": ticker,
        "date": date_disp,
        "is_brief": is_brief,
        "verdict": verdict,
        "role": role,
    }


def _append_index_row(row, file_cell):
    """append 到 INDEX.md 末尾；冪等——同檔名（`file_cell`）已存在則跳過。"""
    INDEX_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = INDEX_MD_PATH.read_text(encoding="utf-8") if INDEX_MD_PATH.exists() else ""
    if file_cell and file_cell in text:
        print("[skip] INDEX.md 已含 {0}，冪等不重複 append".format(file_cell))
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    text += row + "\n"
    INDEX_MD_PATH.write_text(text, encoding="utf-8")
    print("[ok] appended to {0}".format(INDEX_MD_PATH))
    return True


def cmd_index_row(args):
    fields = _index_row_fields(args.html)
    print(fields["row"])
    if args.append:
        _append_index_row(fields["row"], fields["file_cell"])
    return 0


# ---------------------------------------------------------------------------
# WP6a: finish — index-row append → update_dd_index.py → 存查 → commit → push
# ---------------------------------------------------------------------------

def _model_bucket(model_id):
    m = (model_id or "").lower()
    if "opus" in m:
        return "opus"
    if "fable" in m:
        return "fable"
    if "sonnet" in m:
        return "sonnet"
    if "haiku" in m:
        return "haiku"
    return "other"


def _empty_bucket():
    return {"cache_read": 0, "cache_creation": 0, "output": 0}


def _sum_usage_by_model(usage_list):
    buckets = {}
    for u in usage_list or []:
        by_model = (u or {}).get("by_model") or {}
        for mid, vals in by_model.items():
            b = buckets.setdefault(_model_bucket(mid), _empty_bucket())
            b["cache_read"] += (vals or {}).get("cacheReadInputTokens", 0) or 0
            b["cache_creation"] += (vals or {}).get("cacheCreationInputTokens", 0) or 0
            b["output"] += (vals or {}).get("outputTokens", 0) or 0
    return buckets


def _build_token_ledger(manifest):
    """從 manifest 的 `stages.*.agent_usage` 彙總三欄（fable/opus/sonnet，
    另有 haiku/other 兜底）＋每段輪次，回傳 `{totals, by_stage}`。"""
    totals = {}
    by_stage = {}
    for stage_name, stage in (manifest.get("stages") or {}).items():
        usage_list = (stage or {}).get("agent_usage") or []
        buckets = _sum_usage_by_model(usage_list)
        turns = sum((u or {}).get("num_turns", 0) or 0 for u in usage_list)
        by_stage[stage_name] = dict(buckets, turns=turns)
        for k, v in buckets.items():
            t = totals.setdefault(k, _empty_bucket())
            for kk in ("cache_read", "cache_creation", "output"):
                t[kk] += v[kk]
    return {"totals": totals, "by_stage": by_stage}


def _ledger_cache_read_total(ledger, models=("fable", "opus", "sonnet", "other", "haiku")):
    return sum((ledger["totals"].get(m) or {}).get("cache_read", 0) for m in models)


def _ledger_summary_line(ledger):
    total = _ledger_cache_read_total(ledger)
    fable = (ledger["totals"].get("fable") or {}).get("cache_read", 0)
    opus = (ledger["totals"].get("opus") or {}).get("cache_read", 0)
    sonnet = (ledger["totals"].get("sonnet") or {}).get("cache_read", 0)
    return "全帳 {0:.1f}M（fable {1:.1f}M／opus {2:.1f}M／sonnet {3:.1f}M）".format(
        total / 1_000_000.0, fable / 1_000_000.0, opus / 1_000_000.0, sonnet / 1_000_000.0,
    )


def _finish_target_html(ticker, date, manifest):
    """本次 run 實際產出的報告檔——優先信 manifest 的 `stages.brief.out_path`
    （這個 run 自己寫過什麼就是什麼，不用檔案系統猜；`--full` 一旦交付、
    `_do_brief` 把 out_path 換成完整版路徑時，這裡不用跟著改）。只有
    out_path 缺失或已不存在時才退回按檔名慣例猜測（先 brief 再完整版——
    brief 是 v17 現行預設產物，缺 out_path 多半代表這次跑的正是它）。"""
    brief_stage = (manifest.get("stages") or {}).get("brief") or {}
    out_path = brief_stage.get("out_path")
    if out_path and Path(out_path).exists():
        return Path(out_path)
    brief_default = DD_DIR / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date)
    if brief_default.exists():
        return brief_default
    return DD_DIR / "DD_{0}_{1}.html".format(ticker, date)


def _finish_file_set(ticker, date, file_cell):
    return [
        DD_DIR / file_cell,
        INDEX_MD_PATH,
        RESEARCH_BODY_PATH,
        DD_SCREENER_LATEST_PATH,
        PICKS_CANDIDATES_PATH,
        SRC_ARCHIVE_DIR / "{0}_{1}".format(ticker, date),
    ]


def _archive_run_dir(run_dir, archive_dir):
    """把 run 目錄的固定產物複製到 `notes/site-internal/dd/_src/{T}_{D}/`，
    檔名照既有慣例加 `{T}_{D}.` 前綴；`parts/`／`prompts/`／`agents/` 各自
    整個目錄複製（子目錄內原檔名不變）。回傳複製項目清單。"""
    run_dir = Path(run_dir)
    archive_dir = Path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    stem = archive_dir.name

    renamed = {
        "evidence.json": "{0}.evidence.json".format(stem),
        "digest.json": "{0}.transcript_digest.json".format(stem),
        "judgment.json": "{0}.judgment.json".format(stem),
        "scenario.json": "{0}.scenario.json".format(stem),
        "scenario_meta.json": "{0}.scenario_meta.json".format(stem),
        "gate_audit.md": "{0}.gate_audit.md".format(stem),
    }
    copied = []
    for src_name, dst_name in renamed.items():
        src = run_dir / src_name
        if src.exists():
            shutil.copy2(str(src), str(archive_dir / dst_name))
            copied.append(dst_name)

    for sub in ("parts", "prompts", "agents"):
        src_dir = run_dir / sub
        if src_dir.exists():
            dst_dir = archive_dir / sub
            if dst_dir.exists():
                shutil.rmtree(str(dst_dir))
            shutil.copytree(str(src_dir), str(dst_dir))
            copied.append(sub + "/")

    manifest_src = run_dir / "manifest.json"
    if manifest_src.exists():
        shutil.copy2(str(manifest_src), str(archive_dir / "manifest.json"))
        copied.append("manifest.json")

    print("[archive] {0} → {1}（{2} 項）".format(run_dir, archive_dir, len(copied)))
    return copied


def _git(args, cwd=None):
    """git 呼叫的唯一入口——測試 monkeypatch 這支即可隔離真實 git。"""
    return subprocess.run(["git"] + list(args), cwd=str(cwd or REPO_ROOT), capture_output=True, text=True)


def _git_ahead_behind():
    """回傳 (ahead, behind)；behind>0 代表遠端領先（先 fetch 再比）。"""
    _git(["fetch", "origin", "main"])
    r = _git(["rev-list", "--left-right", "--count", "HEAD...origin/main"])
    if r.returncode != 0:
        return (0, 0)
    parts = (r.stdout or "").strip().split()
    if len(parts) != 2:
        return (0, 0)
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return (0, 0)


def _do_finish(ticker, date, dry_run=False, no_push=False, skip_dd_screener=False):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    manifest = _load_json_or(manifest_path, None)
    if manifest is None:
        print("[error] 找不到 manifest：{0}".format(manifest_path), file=sys.stderr)
        return 1
    brief_stage = (manifest.get("stages") or {}).get("brief") or {}
    if brief_stage.get("state") != "PASS":
        print(
            "[error] brief 段尚未 PASS（現況：{0}），finish 中止".format(
                brief_stage.get("state")
            ),
            file=sys.stderr,
        )
        return 1

    html_path = _finish_target_html(ticker, date, manifest)
    if not html_path.exists():
        print("[error] 找不到報告檔：{0}".format(html_path), file=sys.stderr)
        return 1

    fields = _index_row_fields(html_path)
    meta = fields["meta"]

    files = _finish_file_set(ticker, date, fields["file_cell"])
    print("[plan] 檔案集：")
    for f in files:
        print("  - {0}".format(f))

    ledger = _build_token_ledger(manifest)
    ledger_line = _ledger_summary_line(ledger)
    print(ledger_line)

    if dry_run:
        print("[dry-run] 不寫 INDEX、不跑 update_dd_index、不 commit、不 push")
        return 0

    _append_index_row(fields["row"], fields["file_cell"])

    py = _pick_python()
    cmd = [py, str(SCRIPTS_DIR / "update_dd_index.py")]
    if skip_dd_screener:
        cmd.append("--skip-dd-screener")
    r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print(
            "[warn] update_dd_index.py 失敗（rc={0}），僅警告不中止：\n{1}".format(
                r.returncode, (r.stdout + r.stderr)[-1000:]
            )
        )
    else:
        print("[ok] update_dd_index.py rc=0")

    archive_dir = SRC_ARCHIVE_DIR / "{0}_{1}".format(ticker, date)
    _archive_run_dir(run_dir, archive_dir)
    token_path = archive_dir / "token.json"
    _atomic_write_json(token_path, ledger)
    print(ledger_line)

    verdict = meta.get("dca_verdict") or "—"
    role = meta.get("dca_role") or "—"
    label = "DD 快速版" if meta.get("brief") else "DD 完整版"
    total_m = _ledger_cache_read_total(ledger) / 1_000_000.0
    commit_subject = (
        "Add {0} {1} {2}（{3}｜{4}；v17 全帳 {5:.1f}M）; "
        "resync research+screener".format(ticker, label, date, verdict, role, total_m)
    )
    trailer = os.environ.get("DD_COMMIT_TRAILER")
    commit_msg = commit_subject if not trailer else "{0}\n\n{1}".format(commit_subject, trailer)

    existing_files = [f for f in files if Path(f).exists()]
    add_r = _git(["add"] + [str(f) for f in existing_files])
    if add_r.returncode != 0:
        print("[error] git add 失敗：\n{0}".format((add_r.stdout or "") + (add_r.stderr or "")), file=sys.stderr)
        return 1
    commit_r = _git(["commit", "-m", commit_msg])
    if commit_r.returncode != 0:
        print(
            "[error] git commit 失敗：\n{0}".format(
                (commit_r.stdout or "") + (commit_r.stderr or "")
            ),
            file=sys.stderr,
        )
        return 1
    print("[ok] committed: {0}".format(commit_subject))

    status_r = _git(["status", "--porcelain"])
    modified_paths = [ln[3:] for ln in (status_r.stdout or "").splitlines() if ln.strip()]
    whitelist_set = set()
    for f in files:
        try:
            whitelist_set.add(str(Path(f).resolve().relative_to(REPO_ROOT)))
        except ValueError:
            whitelist_set.add(str(f))
    skipped = [p for p in modified_paths if p not in whitelist_set]
    print("[skip] 略過 {0} 個非白名單變動檔".format(len(skipped)))

    if no_push:
        print("[ok] --no-push，未推送")
        return 0

    ahead, behind = _git_ahead_behind()
    if behind > 0:
        print(
            "[HOLD] 遠端領先 {0}，請 orchestrator "
            "用 worktree cherry-pick 推".format(behind)
        )
        return 2
    push_r = _git(["push", "origin", "main"])
    if push_r.returncode != 0:
        print(
            "[error] git push 失敗：\n{0}".format(
                (push_r.stdout or "") + (push_r.stderr or "")
            ),
            file=sys.stderr,
        )
        return 1
    print("[ok] pushed to origin/main")
    return 0


def cmd_finish(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    return _do_finish(
        ticker, date,
        dry_run=args.dry_run, no_push=args.no_push, skip_dd_screener=args.skip_dd_screener,
    )


# ---------------------------------------------------------------------------
# WP1d run：串接 stage0 → judged → gated → brief，支援 --until／--resume
# ---------------------------------------------------------------------------

def cmd_run(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"

    replay_dir = _ensure_replay_env(args.replay_from)

    until_explicit = args.until is not None
    until = args.until or "brief"
    if until not in STAGE_ORDER:
        print("[error] --until 必須是 {0} 之一".format(STAGE_ORDER), file=sys.stderr)
        return 2
    until_idx = STAGE_ORDER.index(until)

    manifest = _load_json_or(manifest_path, {
        "ticker": ticker, "date": date, "state": "new", "created": _now(),
        "steps": [], "agents": [], "stages": {},
    })
    manifest.setdefault("stages", {})

    judgment_model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL

    start_idx = 0
    if args.resume:
        for i, name in enumerate(STAGE_ORDER):
            st = manifest["stages"].get(name, {})
            if st.get("state") in ("PASS", "SKIPPED"):
                start_idx = i + 1
            else:
                break

    plan_kwargs = {
        "archetype": args.archetype, "peers": args.peers, "segments": None,
        "axes_per_batch": args.axes_per_batch, "offline": args.offline,
    }

    rc = 0
    for i in range(start_idx, until_idx + 1):
        stage_name = STAGE_ORDER[i]
        # WP7b #5：`--resume` 落在這一段先前狀態為 FAIL（judged）或
        # FAIL／RUNNING（gated，涵蓋中斷於 spawn 之後、parse 之前的
        # gated_running）時，先重跑機械檢查（judge check／parse 既有
        # gate_audit.md）而非直接重派整段判斷／閘 agent。只在「--resume
        # 接續的第一段」判定，往後正常推進的段仍走全套流程。
        resuming_this_stage = (
            args.resume and i == start_idx
            and manifest["stages"].get(stage_name, {}).get("state")
            in (("FAIL",) if stage_name == "judged" else ("FAIL", "RUNNING"))
        )
        if stage_name == "stage0":
            rc = _do_stage0(ticker, date, plan_kwargs, replay_dir, args.accept_over_budget, manifest)
        elif stage_name == "judged":
            if resuming_this_stage:
                rc = _resume_judge_stage(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
            else:
                rc = _do_judge(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
        elif stage_name == "gated":
            if resuming_this_stage:
                rc = _resume_gate_stage(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
            else:
                rc = _do_gate(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
        elif stage_name == "brief":
            rc = _do_brief(ticker, date, args.full, manifest, dry_run=args.dry_run)
        manifest = _load_json_or(manifest_path, manifest)
        st = manifest.get("stages", {}).get(stage_name, {})
        if st.get("state") not in ("PASS", "SKIPPED"):
            return rc if rc != 0 else 1

    # WP6a：run 預設接 finish；--no-finish／--dry-run／明講 --until 皆不接
    # （含明講 `--until brief`——語意上等同「就跑到這裡，先別 finish」）。
    if (not until_explicit) and until == "brief" and not args.no_finish and not args.dry_run:
        return _do_finish(
            ticker, date,
            dry_run=False, no_push=args.no_push, skip_dd_screener=args.skip_dd_screener,
        )

    return rc


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="ddreport.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("ticker")
    pl.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    pl.add_argument("--archetype", default=None)
    pl.add_argument("--peers", default=None)
    pl.add_argument("--segments", default=None)
    pl.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    pl.add_argument("--offline", action="store_true")
    pl.set_defaults(func=cmd_plan)

    st = sub.add_parser("status")
    st.add_argument("ticker")
    st.add_argument("date")
    st.set_defaults(func=cmd_status)

    rn = sub.add_parser("run")
    rn.add_argument("ticker")
    rn.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    rn.add_argument("--archetype", default=None)
    rn.add_argument("--peers", default=None)
    rn.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    rn.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    rn.add_argument("--full", action="store_true", help="WP4b 未交付，本輪僅印警告")
    rn.add_argument("--replay-from", default=None, metavar="DIR")
    rn.add_argument("--until", default=None, choices=STAGE_ORDER,
                     help="預設跑到 brief 並自動接 finish；明講此旗標（含 --until brief）視為"
                          "刻意要求停在該段，不自動接 finish")
    rn.add_argument("--resume", action="store_true")
    rn.add_argument("--offline", action="store_true")
    rn.add_argument("--accept-over-budget", action="store_true")
    rn.add_argument("--no-finish", action="store_true", help="brief 完成後不自動接 finish")
    rn.add_argument("--dry-run", action="store_true", help="同 --no-finish；WP6a 精神對齊")
    rn.add_argument("--no-push", action="store_true", help="finish 時 commit 但不 push")
    rn.add_argument("--skip-dd-screener", action="store_true",
                     help="finish 時透傳給 update_dd_index.py")
    rn.set_defaults(func=cmd_run)

    s0 = sub.add_parser("stage0")
    s0.add_argument("ticker")
    s0.add_argument("--date", default=None)
    s0.add_argument("--archetype", default=None)
    s0.add_argument("--peers", default=None)
    s0.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    s0.add_argument("--offline", action="store_true")
    s0.add_argument("--replay-from", default=None, metavar="DIR")
    s0.add_argument("--accept-over-budget", action="store_true")

    def _cmd_stage0(args):
        ticker = args.ticker.strip().upper()
        date = args.date or time.strftime("%Y%m%d")
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        plan_kwargs = {"archetype": args.archetype, "peers": args.peers, "segments": None,
                       "axes_per_batch": args.axes_per_batch, "offline": args.offline}
        return _do_stage0(ticker, date, plan_kwargs, replay_dir, args.accept_over_budget, manifest)

    s0.set_defaults(func=_cmd_stage0)

    jg = sub.add_parser("judge")
    jg.add_argument("ticker")
    jg.add_argument("date")
    jg.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    jg.add_argument("--replay-from", default=None, metavar="DIR")
    jg.add_argument("--accept-over-budget", action="store_true")

    def _cmd_judge(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL
        return _do_judge(ticker, date, model, replay_dir, args.accept_over_budget, manifest)

    jg.set_defaults(func=_cmd_judge)

    ga = sub.add_parser("gate")
    ga.add_argument("ticker")
    ga.add_argument("date")
    ga.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    ga.add_argument("--replay-from", default=None, metavar="DIR")
    ga.add_argument("--accept-over-budget", action="store_true")

    def _cmd_gate(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL
        return _do_gate(ticker, date, model, replay_dir, args.accept_over_budget, manifest)

    ga.set_defaults(func=_cmd_gate)

    br = sub.add_parser("brief")
    br.add_argument("ticker")
    br.add_argument("date")
    br.add_argument("--full", action="store_true")
    br.add_argument("--dry-run", action="store_true",
                     help="輸出到 run 目錄內 brief.html，不寫 docs/dd/brief/")

    def _cmd_brief(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        return _do_brief(ticker, date, args.full, manifest, dry_run=args.dry_run)

    br.set_defaults(func=_cmd_brief)

    ir = sub.add_parser("index-row")
    ir.add_argument("--html", required=True, metavar="FILE")
    ir.add_argument("--append", action="store_true")
    ir.set_defaults(func=cmd_index_row)

    fi = sub.add_parser("finish")
    fi.add_argument("ticker")
    fi.add_argument("date")
    fi.add_argument("--dry-run", action="store_true")
    fi.add_argument("--no-push", action="store_true")
    fi.add_argument("--skip-dd-screener", action="store_true")
    fi.set_defaults(func=cmd_finish)

    return p


def main(argv):
    argv = list(argv)
    # `judge check TICKER DATE` 是給 spawn 出去的判斷 agent（透過 Bash 工具）與
    # orchestrator 共用的獨立子命令，前置獨立判斷比硬塞進 argparse 巢狀
    # subparsers（`judge`／`judge check` 位置參數數量會互相打架）簡單可靠。
    if len(argv) >= 3 and argv[0] == "judge" and argv[1] == "check":
        ns = argparse.Namespace(ticker=argv[2], date=argv[3] if len(argv) > 3 else None)
        return cmd_judge_check(ns)

    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
