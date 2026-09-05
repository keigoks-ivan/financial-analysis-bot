#!/usr/bin/env python3
"""假 `claude` binary，供 test_dd_headless.py 經 `DD_CLAUDE_BIN` 指到這裡。

行為：
- 讀 stdin（dd_headless.spawn 把 prompt 內容從 stdin 餵進來）。
- 若 stdin 內容第一行是 `SLEEP:<seconds>`，先 sleep 該秒數再回應——用來
  在 spawn_many 的平行測試裡刻意製造「後送出的先完成」，驗證回傳順序
  仍照 specs 原始順序而非完成順序。
- 若環境變數 `FAKE_CLAUDE_RESPONSE` 有設，直接把該路徑檔案內容原樣印到
  stdout（用來餵固定 fixture，如已知回傳形狀樣本／is_error 樣本）。
- 若環境變數 `DD_REPLAY_FROM` 有設（v17 WP1d `ddreport.py run --replay-from`），
  進入 **replay 模式**：見下方「Replay 模式」。
- 否則印一個預設的成功回應，`result` 欄位回填收到的 stdin 全文，方便
  測試比對「這個結果是哪一個 spec 送出去的」。
- 若有設 `FAKE_CLAUDE_LOG`，把這次呼叫的 argv 與 stdin 追加寫入該檔
  （每行一個 JSON），供需要時檢查實際傳給 claude 的參數。

Replay 模式
-----------
`ddreport.py` 在 `--replay-from DIR` 時，會在每個 prompt 檔尾附加一行
`<!-- DD_REPLAY {json} -->` marker（`_append_replay_marker`），內容依 spawn
種類而異（`kind` 為 `coverage`／`numbers`／`digest`／`transcripts`／
`judgment`／`gate`）。本檔不去猜測散文措辭，只認這個 marker：解析出
`kind` 與對應欄位後，直接把 `DD_REPLAY_FROM` fixture 目錄裡的既有產物
複製／改寫到 marker 指定的輸出路徑，模擬「子 agent 已經把答案寫好了」。
沒有 marker（或 marker 解析失敗）時，寫一個通用的空白合法產物並在
`result` 裡註記，不讓呼叫端當機。

fixture 目錄形狀（`notes/site-internal/dd/_src/{T}_{D}/`，見該目錄
`README.md`）：
    parts/batch*.json          — Stage 0 覆蓋軸 part 檔（`{"coverage": {...}}`，
                                  major_events 那批另帶頂層 `"events"`）
    parts/numbers_agent.json 或
    parts/numbers_collect.json — 數字採集 part（`{"numbers": {...}}`）
    {T}_{D}.transcript_digest.json — 逐字稿摘要（WP7d 起依 `file` 欄拆篇，
                                  充當各 a2_{k} 單篇片段的來源）
    parts/transcripts.json     — Koyfin 路徑清單 part
    {T}_{D}.judgment.json／{T}_{D}.scenario.json — 判斷 agent 產物
    （gate 用的稽核檔在 fixture 目錄的**上一層**：`_audit_{T}_{D}.md`）
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

REPLAY_MARKER_RE = re.compile(r"<!--\s*DD_REPLAY\s+(\{.*?\})\s*-->", re.S)


def _replay_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _replay_copy_first(replay_dir, out_path, candidates, empty_fallback="{}"):
    """依序試 candidates（相對 replay_dir 的路徑），第一個存在的就整檔複製到
    out_path；都沒有就寫一個合法但空的 JSON 佔位並回報。"""
    for rel in candidates:
        cand = replay_dir / rel
        if cand.exists():
            _replay_write(out_path, cand.read_text(encoding="utf-8"))
            return "{0} <- {1}".format(Path(out_path).name, rel)
    _replay_write(out_path, empty_fallback)
    return "{0}: 無對應 fixture，寫入空白佔位".format(Path(out_path).name)


def _replay_coverage(replay_dir, obj):
    """合併 fixture `parts/` 下所有 batch*.json（排除 `*.axes.json` 軸清單
    元資料檔）的 coverage，再依這一批實際要的軸清單挑出對應軸寫入——fixture
    當時的分批方式與這次重跑不一定相同（見 WP1d 派工單 6.）。"""
    axes_wanted = obj.get("axes") or []
    is_major = bool(obj.get("major"))
    out_path = Path(obj["out"])

    merged_coverage = {}
    merged_events = None
    parts_dir = replay_dir / "parts"
    if parts_dir.exists():
        for f in sorted(parts_dir.glob("*.json")):
            if f.name.endswith(".axes.json") or f.name == "_all_axes.json":
                continue
            if not re.match(r"^(batch\d+|axes_\d+)\.json$", f.name):
                continue
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            merged_coverage.update(d.get("coverage") or {})
            if "events" in d:
                merged_events = d["events"]
    # SNOW dry-run fixture 把 events 拆成獨立檔
    if merged_events is None and (parts_dir / "events.json").exists():
        try:
            ev = json.loads((parts_dir / "events.json").read_text(encoding="utf-8"))
            merged_events = ev.get("events", ev)
        except Exception:
            pass

    coverage_out = {}
    missing = []
    for axis_id in axes_wanted:
        if axis_id in merged_coverage:
            coverage_out[axis_id] = merged_coverage[axis_id]
        else:
            missing.append(axis_id)
            coverage_out[axis_id] = {
                "status": "none",
                "queries_run": ["replay fallback：fixture 未涵蓋此軸（1/2）",
                                 "replay fallback：fixture 未涵蓋此軸（2/2）"],
                "findings": [],
                "note": "replay 模式：fixture 無此軸資料，機械補 none 佔位",
            }

    result = {"coverage": coverage_out}
    if is_major and merged_events is not None:
        result["events"] = merged_events

    _replay_write(out_path, json.dumps(result, ensure_ascii=False, indent=2))
    return "coverage {0} 軸（fixture 缺 {1}：{2}）".format(len(axes_wanted), len(missing), missing)


def _replay_numbers(replay_dir, obj):
    """`numbers_agent.json`／`numbers_collect.json` fixture 常是**清理前的原
    始草稿**（見 `numbers.md.tmpl` 鐵律「若某項查無，整筆省略而非填造」）——
    比對 `{T}_{D}.evidence.json`（strict 通過的最終版）發現，最終版
    `latest_quarter_kpis.items[]` 確實比原始 part 少了幾筆全 null 的
    佔位項（`value`／`as_of`／`source` 三者皆 None，帶 `_gap_note`）。
    replay 模式在寫回前補做這道原本該由子 agent 自己做的過濾，讓重放結果
    對齊「子 agent 有照規則做」的情境，而不是照抄未清理的草稿去踩一個
    fixture 本身的已知瑕疵。"""
    out_path = Path(obj["out"])
    for rel in ("parts/numbers_agent.json", "parts/numbers_collect.json", "parts/numbers_flat.json"):
        cand = replay_dir / rel
        if not cand.exists():
            continue
        try:
            data = json.loads(cand.read_text(encoding="utf-8"))
        except Exception:
            continue
        items = (((data or {}).get("numbers") or {}).get("latest_quarter_kpis") or {}).get("items")
        dropped = 0
        if isinstance(items, list):
            kept = [
                it for it in items
                if not (isinstance(it, dict) and it.get("value") is None
                        and it.get("as_of") is None and it.get("source") is None)
            ]
            dropped = len(items) - len(kept)
            data["numbers"]["latest_quarter_kpis"]["items"] = kept
        _replay_write(out_path, json.dumps(data, ensure_ascii=False, indent=2))
        return "{0} <- {1}（過濾全 null 佔位項 {2} 筆）".format(Path(out_path).name, rel, dropped)
    _replay_write(out_path, json.dumps({"numbers": {}}, ensure_ascii=False))
    return "{0}: 無對應 fixture，寫入空白佔位".format(Path(out_path).name)


def _replay_digest(replay_dir, obj):
    """WP7d：`obj` 帶 `file` 時（一篇一個 spawn 的 a2_{k}）從 fixture 的
    `{T}_{D}.transcript_digest.json` 依 `file` 的 basename 拆出對應那篇的
    items/qa_flags，寫成單篇片段（形狀與合併後 digest.json 相同）；不帶
    `file`（舊的單一 a2_digest 呼叫方式，理論上已不再由 ddreport.py 產生，
    保留供其他呼叫端相容）則整檔複製。"""
    out_path = Path(obj["out"])
    cand = replay_dir / "{0}.transcript_digest.json".format(replay_dir.name)
    target_file = obj.get("file")
    if target_file:
        target_base = Path(target_file).name
        if cand.exists():
            try:
                data = json.loads(cand.read_text(encoding="utf-8"))
            except Exception:
                data = None
            if isinstance(data, dict):
                items = [
                    it for it in (data.get("items") or [])
                    if isinstance(it, dict) and Path(it.get("file") or "").name == target_base
                ]
                qa_flags = [
                    q for q in (data.get("qa_flags") or [])
                    if isinstance(q, dict) and Path(q.get("file") or "").name == target_base
                ]
                result = {
                    "source_files": [target_file] if items else [],
                    "items": items,
                    "qa_flags": qa_flags,
                }
                _replay_write(out_path, json.dumps(result, ensure_ascii=False, indent=2))
                return "{0} <- {1}（拆 file={2}，{3} items）".format(
                    Path(out_path).name, cand.name, target_base, len(items))
        empty = json.dumps({"source_files": [], "items": [], "qa_flags": []}, ensure_ascii=False)
        _replay_write(out_path, empty)
        return "{0}: fixture 無 {1} 對應片段，寫入空白佔位".format(Path(out_path).name, target_base)
    if cand.exists():
        _replay_write(out_path, cand.read_text(encoding="utf-8"))
        return "digest.json <- {0}".format(cand.name)
    empty = json.dumps({"source_files": [], "items": [], "qa_flags": []}, ensure_ascii=False)
    _replay_write(out_path, empty)
    return "digest.json: 無 fixture transcript_digest，寫入空白佔位"


def _replay_judgment(replay_dir, obj):
    msgs = []
    jout = obj.get("judgment_out")
    if jout:
        jcand = replay_dir / "{0}.judgment.json".format(replay_dir.name)
        msg = _replay_copy_first(replay_dir, jout, [jcand.name])
        # fixture 的 judgment.json 是舊命名慣例產物，`scenario_ref` 內文字面
        # 存的是 `{T}_{D}.scenario_meta.json`（legacy 扁平慣例），但這次重放
        # 落在 v17 per-run 目錄，`judge check` 實際把 scenario_meta 寫在同目錄
        # 的 `scenario_meta.json`（無 ticker/date 前綴）。這個欄位不對齊只是
        # 新舊檔名慣例差異，不是判斷內容問題——改成這次 run 實際會寫出的檔名，
        # 才是忠實的 replay（`validate_judgment.py` 的漂移檢查要靠它才能讀到
        # scenario_meta 算出 current_meta，否則會誤判成憑空的漂移）。
        try:
            out_path = Path(jout)
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("scenario_ref"):
                data["scenario_ref"] = "scenario_meta.json"
                out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
        msgs.append(msg)
    sout = obj.get("scenario_out")
    if sout:
        scand = replay_dir / "{0}.scenario.json".format(replay_dir.name)
        msgs.append(_replay_copy_first(replay_dir, sout, [scand.name]))
    return "; ".join(msgs)


def _replay_gate(replay_dir, obj):
    out_path = Path(obj["out"])
    # fixture 目錄形狀：.../notes/site-internal/dd/_src/{T}_{D}/，稽核檔在
    # `_src/` 的上一層（.../dd/_audit_{T}_{D}.md），即 replay_dir 的
    # **上兩層**，不是 replay_dir.parent（那還在 `_src/` 裡）。
    cand = replay_dir.parent.parent / "_audit_{0}.md".format(replay_dir.name)
    if cand.exists():
        _replay_write(out_path, cand.read_text(encoding="utf-8"))
        return "gate_audit.md <- {0}".format(cand.name)
    default_audit = (
        "## AUDIT: 判斷級🔴 = 0\n\n"
        "| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |\n"
        "|---|---|---|---|---|---|\n"
    )
    _replay_write(out_path, default_audit)
    return "gate_audit.md: 無 fixture audit，寫入預設 0 紅燈"


def _handle_replay(stdin_text, replay_from):
    m = None
    for mm in REPLAY_MARKER_RE.finditer(stdin_text):
        m = mm  # 若有多個 marker（理論上不該發生），取最後一個
    if not m:
        return "[replay] 找不到 DD_REPLAY marker，未寫入任何檔案"
    try:
        obj = json.loads(m.group(1))
    except Exception as e:
        return "[replay] marker JSON 解析失敗：{0}".format(e)

    replay_dir = Path(replay_from)
    kind = obj.get("kind")
    try:
        if kind == "coverage":
            return "[replay] " + _replay_coverage(replay_dir, obj)
        if kind == "numbers":
            return "[replay] " + _replay_numbers(replay_dir, obj)
        if kind == "digest":
            return "[replay] " + _replay_digest(replay_dir, obj)
        if kind == "transcripts":
            return "[replay] " + _replay_copy_first(
                replay_dir, obj["out"], ["parts/transcripts.json"],
                empty_fallback=json.dumps({"transcripts": {"selected": {
                    "recent_four_quarters": [], "high_signal_optional": []},
                    "koyfin_session_status": "folder_missing"}}, ensure_ascii=False),
            )
        if kind == "judgment":
            return "[replay] " + _replay_judgment(replay_dir, obj)
        if kind == "gate":
            return "[replay] " + _replay_gate(replay_dir, obj)
        return "[replay] 未知 kind={0}，未寫入任何檔案".format(kind)
    except Exception as e:
        return "[replay] 處理 kind={0} 時發生例外：{1}".format(kind, e)


def main():
    data = sys.stdin.read()

    if data.startswith("SLEEP:"):
        first_line = data.splitlines()[0] if data.splitlines() else data
        try:
            sleep_s = float(first_line.split(":", 1)[1].strip())
        except (IndexError, ValueError):
            sleep_s = 0.0
        if sleep_s > 0:
            time.sleep(sleep_s)

    log_path = os.environ.get("FAKE_CLAUDE_LOG")
    if log_path:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"argv": sys.argv[1:], "stdin": data}, ensure_ascii=False) + "\n")

    resp_path = os.environ.get("FAKE_CLAUDE_RESPONSE")
    replay_from = os.environ.get("DD_REPLAY_FROM")

    if resp_path:
        with open(resp_path, "r", encoding="utf-8") as fh:
            sys.stdout.write(fh.read())
    elif replay_from:
        result_text = _handle_replay(data, replay_from)
        payload = {
            "type": "result",
            "is_error": False,
            "num_turns": 1,
            "duration_ms": 100,
            "total_cost_usd": 0.001,
            "result": result_text,
            "usage": {
                "input_tokens": 1,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "output_tokens": 1,
            },
            "modelUsage": {
                "claude-sonnet-5": {
                    "inputTokens": 1,
                    "outputTokens": 1,
                    "cacheReadInputTokens": 0,
                    "cacheCreationInputTokens": 0,
                    "webSearchRequests": 0,
                    "costUSD": 0.001,
                }
            },
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    else:
        payload = {
            "type": "result",
            "is_error": False,
            "num_turns": 1,
            "duration_ms": 100,
            "total_cost_usd": 0.001,
            "result": data,
            "usage": {
                "input_tokens": 1,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "output_tokens": 1,
            },
            "modelUsage": {
                "claude-sonnet-5": {
                    "inputTokens": 1,
                    "outputTokens": 1,
                    "cacheReadInputTokens": 0,
                    "cacheCreationInputTokens": 0,
                    "webSearchRequests": 0,
                    "costUSD": 0.001,
                }
            },
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
