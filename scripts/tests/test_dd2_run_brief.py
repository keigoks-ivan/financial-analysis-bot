#!/usr/bin/env python3
"""測試 `scripts/dd2/run.py` 的 `do_brief`（2026-09-29：快速版停產上站）。

持有人拍板：dd2 v20 的每一輪還是要跑零 LLM 的 brief 渲染（`_finish_required_stages`
仍要求 `brief` PASS 才准 finish），但輸出的 HTML 不准再落在 `docs/dd/brief/`——
只有 `ddreport.py run`（舊鏈）／獨立 `brief` 子命令才寫那裡。本檔只驗證 dd2 這端
確實把 `publish=False` 傳給 `ddreport._do_brief`，不重測 `_do_brief` 本身的路徑
邏輯（那支已在 `test_ddreport_finish.py` 覆蓋）。

Python 3.9 相容。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

from dd2 import run as dd2_run  # noqa: E402


def test_do_brief_calls_ddreport_with_publish_false(tmp_path, monkeypatch):
    captured = {}

    def _fake_do_brief(ticker, date, do_full, manifest, dry_run=False, publish=True):
        captured["ticker"] = ticker
        captured["date"] = date
        captured["do_full"] = do_full
        captured["dry_run"] = dry_run
        captured["publish"] = publish
        manifest.setdefault("stages", {})["brief"] = {"state": "PASS"}
        return 0

    monkeypatch.setattr(dd2_run.ddreport, "_do_brief", _fake_do_brief)
    monkeypatch.setattr(dd2_run, "_run_dir", lambda ticker, date: tmp_path / "{0}_{1}".format(ticker, date))

    args = argparse.Namespace(dry_run=False, judgment_model=None)
    ctx = dd2_run.Ctx("ZBRIEF3", "20260929", args)
    ctx.manifest = {"ticker": "ZBRIEF3", "date": "20260929", "stages": {}}

    ok = dd2_run.do_brief(ctx)

    assert ok is True
    assert captured["publish"] is False
    assert captured["ticker"] == "ZBRIEF3"
    assert captured["date"] == "20260929"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
