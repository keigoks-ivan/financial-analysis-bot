#!/usr/bin/env python3
"""2026-10-19：/simulation/ 行情檔改存 .json.gz 的壓縮腳本與頁面解壓函式測試。"""
from __future__ import annotations

import gzip
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import gzip_simulation_data as gz  # noqa: E402


def _tree(root):
    for rel, obj in {
        "manifest.json": [{"id": "session-1"}],
        "daily.json": {"days": [1, 2, 3]},
        "session-1.json": {"ticks": list(range(100))},
        "stocks/catalog.json": [{"symbol": "2330.TW"}],
        "stocks/index-etfs.json": [{"symbol": "SPY"}],
        "stocks/actions.json": {"2330.TW": []},
        "stocks/2330.TW.json": {"symbol": "2330.TW", "days": [{"close": 1.5}] * 50},
        "campaigns/catalog.json": [{"id": "20260803"}],
        "campaigns/20260803.json": {"ticks": [[1, 2]] * 20},
    }.items():
        path = Path(root, rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))


def test_pack_compresses_everything_except_the_four_small_lists_and_round_trips(tmp_path):
    root = tmp_path / "data"
    _tree(root)
    originals = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*.json")}
    n, raw, packed = gz.pack(root)
    assert n == 5 and packed < raw
    for rel, content in originals.items():
        if rel in gz.PLAIN:
            assert (root / rel).read_bytes() == content
            assert not (root / (rel + ".gz")).exists()
        else:
            assert not (root / rel).exists()
            assert gzip.decompress((root / (rel + ".gz")).read_bytes()) == content
    assert gz.check(root) == []
    assert gz.pack(root)[0] == 0  # 重跑不動已壓縮的檔


def test_pack_output_is_deterministic(tmp_path):
    for name in ("a", "b"):
        _tree(tmp_path / name)
        gz.pack(tmp_path / name)
    assert (tmp_path / "a/stocks/2330.TW.json.gz").read_bytes() == (tmp_path / "b/stocks/2330.TW.json.gz").read_bytes()


def test_check_reports_uncompressed_and_broken_files(tmp_path):
    root = tmp_path / "data"
    _tree(root)
    problems = gz.check(root)
    assert "未壓縮：stocks/2330.TW.json" in problems
    gz.pack(root)
    (root / "daily.json.gz").write_bytes(b"not gzip")
    assert any(line.startswith("壞檔：daily.json.gz") for line in gz.check(root))
    (root / "manifest.json").unlink()
    assert "缺少清單檔：manifest.json" in gz.check(root)


def test_repo_simulation_data_is_fully_compressed():
    # 之後重新匯出行情檔、忘了跑 scripts/gzip_simulation_data.py 就會在這裡擋下。
    assert gz.check(gz.DATA) == []


@pytest.mark.skipif(shutil.which("node") is None, reason="需要 node 18 以上（fetch／DecompressionStream）")
def test_gzjson_reads_gzip_plain_text_and_mock_responses(tmp_path):
    payload = {"symbol": "2330.TW", "days": [{"close": 1.5}] * 20, "中文": "測試"}
    gz_path = tmp_path / "x.json.gz"
    gz_path.write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False).encode("utf-8"), 9, mtime=0))
    module = (REPO_ROOT / "docs" / "simulation" / "gzjson.js").as_uri()
    script = """
import {gzJson} from '%s';
import fs from 'node:fs';
const gz = fs.readFileSync(%s);
const a = await gzJson(new Response(gz));
const b = await gzJson(new Response(JSON.stringify(a)));
const c = await gzJson({json: async () => a});
let msg = '';
try { await gzJson(new Response(new Uint8Array([0x1f, 0x8b, 0, 1, 2]))); } catch (e) { msg = 'rejected'; }
console.log(JSON.stringify({a, same: JSON.stringify(a) === JSON.stringify(b) && JSON.stringify(a) === JSON.stringify(c), msg}));
""" % (module, json.dumps(str(gz_path)))
    run = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True, timeout=60)
    if run.returncode != 0 and "DecompressionStream" in run.stderr:
        pytest.skip("node 版本太舊")
    assert run.returncode == 0, run.stderr
    out = json.loads(run.stdout.strip().splitlines()[-1])
    assert out["a"] == payload and out["same"] is True and out["msg"] == "rejected"
