#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural validator for the asset rotation radar payload.

Validates docs/rotation/data/radar.json and each daily snapshot
(docs/rotation/data/snapshots/*.json) against the contract emitted by
scripts/build_rotation_radar.py.  Both files carry the identical payload schema,
so one check runs over every target.

Checks (per file)
-----------------
  * top-level keys present: as_of, frames, method, universes
  * as_of is YYYY-MM-DD
  * frames is a non-empty list of frame keys (strings)
  * method is a dict
  * universes is a non-empty array; each has key / label / benchmark / members
    - benchmark has ticker + label
    - each member has ticker + label + status
    - each status=="ok" member has a frames dict covering every top-level frame,
      each frame carrying a trail array of {d, r, m}
    - r / m are finite numbers inside a sane 80-120 band; d is YYYY-MM-DD

Exit non-zero (with per-error messages) on any violation.

CLI
---
  python scripts/validate_rotation_radar.py <file.json> [<file.json> ...]
  python scripts/validate_rotation_radar.py            # no args -> radar.json
                                                       # + all snapshots (sweep)
"""
from __future__ import annotations

import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADAR = os.path.join(ROOT, "docs", "rotation", "data", "radar.json")
SNAP_DIR = os.path.join(ROOT, "docs", "rotation", "data", "snapshots")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
R_MIN, R_MAX = 80.0, 120.0  # sane band for the z-score-normalized rs_ratio / rs_mom


def _is_finite_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def validate_payload(obj, label, errors):
    """Append human-readable messages to `errors` for every violation in obj."""
    def err(msg):
        errors.append(f"{label}: {msg}")

    if not isinstance(obj, dict):
        err("payload is not a JSON object")
        return

    for k in ("as_of", "frames", "method", "universes"):
        if k not in obj:
            err(f"missing top-level key '{k}'")

    as_of = obj.get("as_of")
    if not isinstance(as_of, str) or not DATE_RE.match(as_of):
        err(f"as_of not YYYY-MM-DD: {as_of!r}")

    frames = obj.get("frames")
    if not isinstance(frames, list) or not frames or not all(isinstance(f, str) for f in frames):
        err(f"frames must be a non-empty list of strings: {frames!r}")
        frames = []

    if not isinstance(obj.get("method"), dict):
        err("method must be an object")

    universes = obj.get("universes")
    if not isinstance(universes, list) or not universes:
        err("universes must be a non-empty array")
        return

    for i, uni in enumerate(universes):
        uni_label = f"universe[{i}]"
        if not isinstance(uni, dict):
            err(f"{uni_label} is not an object")
            continue
        for k in ("key", "label", "benchmark", "members"):
            if k not in uni:
                err(f"{uni_label} missing '{k}'")
        ukey = uni.get("key")
        if isinstance(ukey, str) and ukey:
            uni_label = f"universe '{ukey}'"

        bench = uni.get("benchmark")
        if not isinstance(bench, dict) or not bench.get("ticker") or not bench.get("label"):
            err(f"{uni_label} benchmark must have ticker + label: {bench!r}")

        members = uni.get("members")
        if not isinstance(members, list) or not members:
            err(f"{uni_label} members must be a non-empty array")
            continue

        for j, m in enumerate(members):
            mlabel = f"{uni_label} member[{j}]"
            if not isinstance(m, dict):
                err(f"{mlabel} is not an object")
                continue
            for k in ("ticker", "label", "status"):
                if k not in m:
                    err(f"{mlabel} missing '{k}'")
            tk = m.get("ticker")
            if isinstance(tk, str) and tk:
                mlabel = f"{uni_label} member {tk}"
            status = m.get("status")
            if status not in ("ok", "insufficient"):
                err(f"{mlabel} status must be 'ok' or 'insufficient': {status!r}")
            if status != "ok":
                continue

            mframes = m.get("frames")
            if not isinstance(mframes, dict):
                err(f"{mlabel} status=ok but frames is not an object")
                continue
            for fk in frames:
                if fk not in mframes:
                    err(f"{mlabel} missing frame '{fk}'")
                    continue
                fobj = mframes[fk]
                if not isinstance(fobj, dict) or "trail" not in fobj:
                    err(f"{mlabel} frame '{fk}' must be an object with a trail")
                    continue
                trail = fobj["trail"]
                if not isinstance(trail, list) or not trail:
                    err(f"{mlabel} frame '{fk}' trail must be a non-empty array")
                    continue
                for p, pt in enumerate(trail):
                    plabel = f"{mlabel} frame '{fk}' trail[{p}]"
                    if not isinstance(pt, dict):
                        err(f"{plabel} is not an object")
                        continue
                    d = pt.get("d")
                    if not isinstance(d, str) or not DATE_RE.match(d):
                        err(f"{plabel} d not YYYY-MM-DD: {d!r}")
                    for coord in ("r", "m"):
                        v = pt.get(coord)
                        if not _is_finite_number(v):
                            err(f"{plabel} {coord} not a finite number: {v!r}")
                        elif not (R_MIN <= float(v) <= R_MAX):
                            err(f"{plabel} {coord}={v} outside sane band "
                                f"[{R_MIN}, {R_MAX}]")


def _targets_from_args(argv):
    if argv:
        return argv
    targets = []
    if os.path.exists(RADAR):
        targets.append(RADAR)
    if os.path.isdir(SNAP_DIR):
        targets += sorted(
            os.path.join(SNAP_DIR, f)
            for f in os.listdir(SNAP_DIR) if f.endswith(".json")
        )
    return targets


def main():
    targets = _targets_from_args(sys.argv[1:])
    if not targets:
        print("[radar-validate] no target files found (radar.json / snapshots) — nothing to check")
        return 0

    errors = []
    for path in targets:
        label = os.path.relpath(path, ROOT)
        if not os.path.exists(path):
            errors.append(f"{label}: file does not exist")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                obj = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"{label}: could not parse JSON: {e}")
            continue
        validate_payload(obj, label, errors)

    if errors:
        print("❌ rotation radar validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   - {e}", file=sys.stderr)
        print(f"   ({len(errors)} error(s) across {len(targets)} file(s))", file=sys.stderr)
        return 1

    print(f"✅ rotation radar OK — {len(targets)} file(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
