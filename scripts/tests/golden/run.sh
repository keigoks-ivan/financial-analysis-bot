#!/usr/bin/env bash
# 黃金重播測試（P0）入口：改前抓快照 → 改後重播 → 比對。快照與結果放 /Volumes/X10 Data/fab_golden/，不進 repo。
#
#   scripts/tests/golden/run.sh capture [capture.py 選項…]
#       改程式之前跑一次：在目前 repo 的程式上抓價格快照（只連網這一次），印出快照目錄。
#   scripts/tests/golden/run.sh check <快照目錄> [compare.py 選項…]
#       改程式之後跑：快照當時的 commit（git archive）與目前工作樹（含未提交改動）各重播一次，逐格比對，不同就 exit 1。
#       純重構不加選項（全部要一樣）；改規則加 --expect-same-before <生效日> --signals-only。
#   scripts/tests/golden/run.sh selftest <快照目錄>
#       自我檢驗：同一 commit 重播兩次要全同；四種故意破壞（權重、下軌門檻、浮點尾數、主控台 idx_share）要被抓到；
#       快照 commit 早於規則正本（P1）就改程式常數，晚於 P1 就改 knowledge/live_rules.toml（樣板找不到的那組略過）；
#       環境變數覆寫生效日要看得到差異、且生效日前訊號不變。
#
# 不寫受測 repo、不連網（重播時封鎖 socket）、不寄信：子行程的環境變數從零組起，不帶任何通知金鑰。
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
PY="${GOLDEN_PY:-$HOME/.venvs/v7bt/bin/python}"
cmd="${1:-}"; shift || true

src_commit() { "$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]+"/meta.json"))["source_commit"])' "$1"; }

case "$cmd" in
  capture)
    "$PY" "$HERE/capture.py" --src "$REPO" "$@"
    ;;
  check)
    SNAP="$1"; shift
    TS="$(date +%Y%m%d-%H%M%S)"; OUT="$SNAP/results"
    BASE="$(src_commit "$SNAP")"
    "$PY" "$HERE/replay.py" --snapshot "$SNAP" --commit "$BASE" --repo "$REPO" --out "$OUT/check_${TS}_base.json"
    "$PY" "$HERE/replay.py" --snapshot "$SNAP" --src "$REPO" --out "$OUT/check_${TS}_cand.json"
    "$PY" "$HERE/compare.py" "$OUT/check_${TS}_base.json" "$OUT/check_${TS}_cand.json" \
      --report "$OUT/check_${TS}_diff.tsv" "$@"
    ;;
  selftest)
    SNAP="$1"; OUT="$SNAP/results"; TS="$(date +%Y%m%d-%H%M%S)"
    BASE="$(src_commit "$SNAP")"
    WORK="/Volumes/X10 Data/fab_golden/_work/selftest-$TS"; mkdir -p "$WORK"
    trap 'rm -rf "$WORK"' EXIT
    ok=0; bad=0
    pass() { echo "  [通過] ${1}"; ok=$((ok+1)); }
    fail() { echo "  [失敗] ${1}"; bad=$((bad+1)); }
    echo "== 1. 同一 commit 重播兩次必須全同"
    "$PY" "$HERE/replay.py" --snapshot "$SNAP" --commit "$BASE" --repo "$REPO" --out "$OUT/self_${TS}_a.json" >/dev/null
    "$PY" "$HERE/replay.py" --snapshot "$SNAP" --commit "$BASE" --repo "$REPO" --out "$OUT/self_${TS}_b.json" >/dev/null
    if "$PY" "$HERE/compare.py" "$OUT/self_${TS}_a.json" "$OUT/self_${TS}_b.json" | tail -1; then pass "兩次全同"; else fail "兩次不同（測試不穩定）"; fi
    echo "== 2. 故意破壞（拋棄式副本）必須被抓到"
    for case in "w041|supertrend_core.py|tw = 0.4 if str(ds)[:10] >= TW_L2_CUTOVER_DATE else 0.5|tw = 0.41 if str(ds)[:10] >= TW_L2_CUTOVER_DATE else 0.5" \
                "bbk24|supertrend_core.py|BB_K, BB_REARM, BB_LEVEL, BB_WIN = 2.5,|BB_K, BB_REARM, BB_LEVEL, BB_WIN = 2.4," \
                "tail|supertrend_core.py|\"SMH\": 0.3 if new else 0.5|\"SMH\": (1 - 0.7) if new else 0.5" \
                "idx071|build_long_track_index.py|\"idx_share\": 0.7,|\"idx_share\": 0.71," \
                "w041t|../knowledge/live_rules.toml|\"0050.TW\" = 0.4\\n\"2330.TW\" = 0.4|\"0050.TW\" = 0.41\\n\"2330.TW\" = 0.39" \
                "bbk24t|../knowledge/live_rules.toml|trigger = -2.5|trigger = -2.4" \
                "tailt|../knowledge/live_rules.toml|\"SMH\" = 0.3|\"SMH\" = 0.30000000000000004" \
                "idx071t|../knowledge/live_rules.toml|us_index_share = 0.70|us_index_share = 0.71"; do
      IFS='|' read -r name file old new <<<"$case"
      mkdir -p "$WORK/$name"; git -C "$REPO" archive "$BASE" scripts | tar -x -C "$WORK/$name"
      if git -C "$REPO" cat-file -e "$BASE:knowledge/live_rules.toml" 2>/dev/null; then    # P1 起程式讀規則正本
        git -C "$REPO" archive "$BASE" knowledge/live_rules.toml | tar -x -C "$WORK/$name"
      fi
      if ! "$PY" - "$WORK/$name/scripts/$file" "$old" "$new" <<'EOF'
import os
import sys
p, old, new = sys.argv[1:4]
old, new = old.replace("\\n", "\n"), new.replace("\\n", "\n")     # 樣板裡的 \n（兩個字元）＝換行
if not os.path.exists(p):
    sys.exit(f"這個 commit 沒有 {os.path.normpath(p)}（P1 以前沒有規則正本）")
s = open(p, encoding="utf-8").read()
if s.count(old) != 1:
    sys.exit(f"樣板找不到（程式已改寫？）：{old}")
open(p, "w", encoding="utf-8").write(s.replace(old, new))
EOF
      then echo "  [略過] ${name}"; continue; fi
      "$PY" "$HERE/replay.py" --snapshot "$SNAP" --src "$WORK/$name" --out "$OUT/self_${TS}_$name.json" >/dev/null
      if "$PY" "$HERE/compare.py" "$OUT/self_${TS}_a.json" "$OUT/self_${TS}_$name.json" --show 3 | sed -n '/失敗/,$p'; then
        fail "${name} 沒被抓到"; else pass "${name} 被抓到（見上面最早的差異）"; fi
    done
    echo "== 3. 環境變數覆寫 W52_TW_L2_CUTOVER_DATE=2026-11-13：結果要跟著變，且 11-10 前的訊號不變"
    "$PY" "$HERE/replay.py" --snapshot "$SNAP" --commit "$BASE" --repo "$REPO" --env W52_TW_L2_CUTOVER_DATE=2026-11-13 \
      --out "$OUT/self_${TS}_env.json" >/dev/null
    if "$PY" "$HERE/compare.py" "$OUT/self_${TS}_a.json" "$OUT/self_${TS}_env.json" --show 0 >/dev/null; then
      fail "覆寫後結果沒變（測試沒讀到生效日）"; else pass "覆寫後結果改變"; fi
    if "$PY" "$HERE/compare.py" "$OUT/self_${TS}_a.json" "$OUT/self_${TS}_env.json" --expect-same-before 2026-11-10 \
         --signals-only --show 5 | tail -1; then pass "2026-11-10 之前訊號逐格相同"; else fail "2026-11-10 之前就有差異"; fi
    echo "自我檢驗：通過 ${ok}、失敗 ${bad}"
    [ "${bad}" -eq 0 ]
    ;;
  *)
    sed -n '2,12p' "$0"; exit 2 ;;
esac
