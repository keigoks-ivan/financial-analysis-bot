#!/bin/bash
# dd_gates.sh — v16.2 一次複合驗證閘（(b2) 散文 agent 專用；見 references/v16/agent-prompts.md (b2)）
#
# WHY：CRDO 2026-09-04 實測，散文 agent 把 render_dd.py --assemble 與六支驗證拆成多輪個別
# Bash 呼叫（第一輪只跑 validate_prose、漏掉其餘五支；第二輪才補齊），驗證輪次因此吃到 3 輪，
# 且中途因不確定某支閘的規則跑去 grep 腳本原始碼另花一輪。本檔把六支閘順序執行、彙總輸出，
# (b2) 只需呼叫這一支，把驗證輪次壓回 ≤2。
#
# 用法：scripts/dd_gates.sh TICKER DATE OUT_HTML
#   例：scripts/dd_gates.sh CRDO 20260904 docs/dd/DD_CRDO_20260904.html
#
# 路徑慣例（沿用既有 .dd_build/{TICKER}_{DATE}.* 命名，不另創新慣例）：
#   prose    = .dd_build/{TICKER}_{DATE}.prose
#   tables   = .dd_build/{TICKER}_{DATE}.tables
#   judgment = .dd_build/{TICKER}_{DATE}.judgment.json
#   evidence = .dd_build/{TICKER}_{DATE}.evidence.json（選填，缺檔則 validate_prose 只用 judgment）
#
# gate 語意不變（只是集中呼叫，不改各腳本既有 pass/warn/fail 規則）：
#   render_dd assemble／validate_prose／qc.py／verify_dd_math.py 的既有 exit code 直接採信；
#   dd_sections.py bytes 維持既有「WARN 不擋」設計（不加 --strict，篇幅上下界仍由 pre-commit
#   size-floor gate 與人工複審把關，這裡只彙整輸出）；
#   dd_sections.py leaks 本身恆 exit 0（只印命中數），本腳本改讀輸出的「總數: N」自行判定 N>0 為 FAIL；
#   validate_dd_meta.py 沿用既有 --report 慣例（診斷用，不擋，同 render-rules.md 現行流程）。
set -uo pipefail

T="${1:?用法: dd_gates.sh TICKER DATE OUT_HTML}"
D="${2:?用法: dd_gates.sh TICKER DATE OUT_HTML}"
OUT_HTML="${3:?用法: dd_gates.sh TICKER DATE OUT_HTML}"

PY="${DD_PYTHON:-/tmp/ddvenv/bin/python}"
cd "$(dirname "$0")/.."

PROSE=".dd_build/${T}_${D}.prose"
TABLES=".dd_build/${T}_${D}.tables"
JUDGMENT=".dd_build/${T}_${D}.judgment.json"
EVIDENCE=".dd_build/${T}_${D}.evidence.json"

FAIL=0

echo "=== 1/7 render_dd --assemble ==="
"$PY" scripts/render_dd.py --assemble "$PROSE" --tables "$TABLES" --judgment "$JUDGMENT" -o "$OUT_HTML"
[ $? -ne 0 ] && FAIL=1

echo "=== 2/7 validate_prose ==="
if [ -f "$EVIDENCE" ]; then
  "$PY" scripts/validate_prose.py "$PROSE" --judgment "$JUDGMENT" --evidence "$EVIDENCE"
else
  "$PY" scripts/validate_prose.py "$PROSE" --judgment "$JUDGMENT"
fi
[ $? -ne 0 ] && FAIL=1

echo "=== 3/7 dd_sections bytes（WARN 不擋，篇幅另由 size-floor gate 把關）==="
"$PY" scripts/dd_sections.py bytes "$OUT_HTML"

echo "=== 4/7 dd_sections leaks ==="
LEAKS_OUT=$("$PY" scripts/dd_sections.py leaks "$OUT_HTML")
echo "$LEAKS_OUT"
if ! echo "$LEAKS_OUT" | grep -q "^總數: 0$"; then
  FAIL=1
fi

echo "=== 5/7 qc ==="
"$PY" scripts/qc.py "$OUT_HTML"
[ $? -ne 0 ] && FAIL=1

echo "=== 6/7 validate_dd_meta（--report 診斷用，不擋，同既有流程慣例）==="
"$PY" scripts/validate_dd_meta.py "$OUT_HTML" --report

echo "=== 7/7 verify_dd_math ==="
"$PY" scripts/verify_dd_math.py "$OUT_HTML"
[ $? -ne 0 ] && FAIL=1

echo "----------------------------------------"
if [ "$FAIL" -ne 0 ]; then
  echo "—— dd_gates.sh：至少一支擋下（見上方 ✗/FAIL），FAIL"
  exit 1
fi
echo "—— dd_gates.sh：六支全過"
exit 0
