#!/usr/bin/env python3
"""
harvest_kill_watch.py — 把 docs/detective/data/kill_watch.json 的 monitor 型門檻擬成
knowledge/forecasts.jsonl 草案（forecast v2 §9 row F3 套件；設計稿
notes/site-internal/root/_market_cockpit_design_20260902.md §9／
notes/site-internal/root/_forecast_v2_design_20260902.md §9 conditional-frequency method）。

kill_watch.json 的 12 條引信（items[]）分兩類：data_source.type="monitor"（可直接對到
docs/monitor/data/latest.json 的某個 key，如 fx/dxy → dxy）與 type="internals"（由偵探
pipeline 另外算，不在 monitor latest.json 的扁平 key 清單內，如 macro/core_pce_yoy）。本檔
**只處理 monitor 型**（設計稿原文：「items with data_source.type == "monitor" and numeric
value；skip internals-type and non-numeric」）——internals 型一律跳過並印 stderr 原因，即使
其中一條（macro:MACRO_USEconomy_20260708:5，10Y breakeven，data_source.key=macro/bei10y）
概念上與本檔新建的 T10YIE climatology 序列相關：kill_watch.json 目前把它標成 internals（非
monitor latest.json 的既有 key，該檔目前也確實沒有 bei10y／t10yie 這個 key），所以照這條
明文規則會被跳過，不會產生新草案。這與「若 kill_watch 改標該筆為 monitor 型（或 monitor
latest.json 未來新增 bei10y／t10yie key）即可機械收案」的設計意圖並不衝突——bei10y/t10yie
→ T10YIE 的 climatology 映射已經就緒（見 scripts/build_macro_base_rates.py），只是「現在」
這筆資料本身的 type 標記還沒讓它符合資格。不在此按經驗猜測繞過 type 過濾器，見本檔尾端
main() 之後的執行紀錄／harvest() 回傳的 skipped 列表可稽核。

resolver＝`monitor:<key>`，key 取 data_source.key 斜線後的最後一段（如 fx/dxy → dxy；照抄
設計稿 §9 row F3 原文「key 取 data_source.key 的斜線後段」），並驗證該 key 確實存在於
docs/monitor/data/latest.json（否則跳過，不猜測）。current 一律取 monitor latest.json 的
「現在」值（非 kill_watch.json 自己快照的 current 欄——kill_watch.json 的 generated_at 常常
落後 monitor 的 as_of，用 monitor 現值才符合 resolver=monitor:<key> 的語意，且與
harvest_macro_falsifiers.py 一致：那支腳本的 delta 也是拿 monitor 現值算，不是報告內文的
snapshot）。

單位換算（僅 sofr_iorb 需要）：kill_watch.json 把 SOFR−IORB 門檻記成「百分點」（value=0.05，
unit="百分點（=+5bp）"），但 climatology() 的 sofr_iorb 序列、monitor latest.json 的顯示值
（"3bps"）、以及 knowledge/forecasts.jsonl 既有的 sofr_iorb resolver.value（5.0，unit="bp"）
全部是 bp 尺度——這是 settle_forecasts.py 說的「resolver.value 一律採顯示單位落帳」
（v2 起，見該檔案「單位注意」段）。故本檔對 key=sofr_iorb 的 value 做 ×100 換算（0.05 pp →
5.0 bp）才拿去跟 climatology／既有 ledger 列比對，其餘 5 個 key（dxy／usdcny／hy_oas／
tp10y／dgs30）kill_watch 的 value／unit 本來就是顯示單位，不需要換算。

p 值：`--p-mode conditional` 直接 import scripts/harvest_macro_falsifiers.py 的
conditional_p()（§9 條件式歷史頻率法，PREREG 凍結常數 252/21/90/10/70/60/0.01，不重寫一份）。
conditional_p() 內部的 LVL_BUCKET 只登記了原 6 條 macro-falsifier 草案用到的 5 個 key
（dgs10/dgs30/tp10y/hy_oas/sofr_iorb）；本檔新增的 4 個 key（dxy/usdcny/bei10y/t10yie）用
`hmf.LVL_BUCKET.setdefault(key, (">=", 90))` 在**執行期**補登記（不修改
harvest_macro_falsifiers.py 檔案本身——那支腳本不在本套件所有權範圍內；setdefault 是
"in-memory 擴充一個 import 進來的 dict"，不動對方原始碼一個字元）。桶方向 (">=", 90) 沿用
原表對「breach_above 型門檻」的既有慣例（dgs10/dgs30/tp10y 皆是 ">=90 分位"）：dxy／usdcny
在 kill_watch 的門檻語意都是「站上／突破」，故採同一慣例；bei10y/t10yie 目前不會被觸發（見
上一段），僅為未來就緒而登記。

查重：與既有 status="open" 的 macro-falsifier 列以 (resolver.series, op 方向, resolver.value)
比對（tolerance 1e-6）——op 方向正規化（>=/> 都算 ">"，<=/< 都算 "<"）是必要的，因為既有
ledger 的 6 筆 macro-falsifier 列全部用裸 ">" / "<"（harvest_macro_falsifiers.py 的
_direction() 一律吐裸符號），但 kill_watch.json 對同一批門檻慣用 ">=" / "<="——若逐字比對
op 字串，dgs30／hy_oas／tp10y(>=1.0) 三筆會誤判成「新」而重複落帳。resolver.value 也需先做
上述 sofr_iorb 單位換算才能對上既有列的 5.0。

用法
----
  python scripts/harvest_kill_watch.py --p-mode conditional
                                                    # dry-run，p 由條件式歷史頻率法算出
  python scripts/harvest_kill_watch.py --p-mode conditional --ledger /tmp/scratch.jsonl
                                                    # dry-run，繞過真帳簿查重（測試用）
  python scripts/harvest_kill_watch.py --p-mode conditional --write
                                                    # 落帳：p 由條件式歷史頻率法算出後直接
                                                    # append（含哨兵 twin，經 forecast_lib.append）

跳過原因、每筆診斷（current／threshold／delta／p_clim／p／查重結果）印到 stderr，不混進
stdout 的 JSONL。
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KILL_WATCH = ROOT / "docs" / "detective" / "data" / "kill_watch.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

# 同套件內 sibling module（scripts/ 底下，執行 `python scripts/harvest_kill_watch.py` 時
# sys.path[0] 就是 scripts/，直接 import 即可）。
import build_macro_base_rates as bmr
import harvest_macro_falsifiers as hmf

SOURCE = "macro-falsifier"
CLAIM_TEMPLATE = "macro_threshold"
HORIZON_DAYS = 90          # PREREG（設計稿 §9 row F3）：固定 90 曆日，不取 kill_watch 的 window 欄
ID_PREFIX = "kw"
DEDUPE_TOL = 1e-6

# 執行期擴充 conditional_p() 的 LVL_BUCKET（見檔頭「p 值」段——不修改 harvest_macro_falsifiers.py
# 原始檔，只在 import 進來的 dict 上 setdefault）。
for _key in ("dxy", "usdcny", "bei10y", "t10yie"):
    hmf.LVL_BUCKET.setdefault(_key, (">=", 90))

# kill_watch value → series 顯示單位的換算倍率；僅 sofr_iorb 非 1（pp → bp，見檔頭「單位換算」段）。
KEY_VALUE_SCALE = {"sofr_iorb": 100.0}
# resolver.unit 覆寫（僅 sofr_iorb 需要——kill_watch 原始 unit 文字「百分點（=+5bp）」不是
# 乾淨的顯示單位字串）；其餘 key 直接沿用 kill_watch 自己的 unit 欄位。
RESOLVER_UNIT_OVERRIDE = {"sofr_iorb": "bp"}


def warn(msg: str) -> None:
    print(f"[harvest-kill-watch][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[harvest-kill-watch] {msg}", file=sys.stderr)


def _op_dir(op):
    """">=" 與 ">" 都算 ">"；"<=" 與 "<" 都算 "<"（查重與 climatology 的方向正規化，見檔頭）。"""
    return ">" if op in (">", ">=") else "<"


def _load_kill_watch():
    try:
        return json.loads(KILL_WATCH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"[harvest-kill-watch][ERROR] 無法讀取 {KILL_WATCH}: {e}")


def _existing_forecasts(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _dup_index(existing_rows):
    """回傳 [(series, op_dir, value, id), ...]，來自 status=open 的既有 macro-falsifier 列。"""
    out = []
    for r in existing_rows:
        if r.get("source") != SOURCE or r.get("status") != "open":
            continue
        res = r.get("resolver") or {}
        series, op, val = res.get("series"), res.get("op"), res.get("value")
        if series is None or op is None or val is None:
            continue
        try:
            out.append((series, _op_dir(op), float(val), r.get("id")))
        except (TypeError, ValueError):
            continue
    return out


def _find_dup(dup_index, series, op, value):
    d = _op_dir(op)
    for s, dop, v, rid in dup_index:
        if s == series and dop == d and abs(v - value) <= DEDUPE_TOL:
            return rid
    return None


def _next_id(today_str, seq_state):
    n = seq_state.get(today_str, 0) + 1
    seq_state[today_str] = n
    return f"fc_{today_str.replace('-', '')}_{ID_PREFIX}_{n:02d}"


def _raw_cache_built_at():
    try:
        return json.loads(bmr.RAW_CACHE.read_text(encoding="utf-8")).get("meta", {}).get("built_at")
    except (OSError, json.JSONDecodeError):
        return None


def harvest(p_mode=None, ledger_path=None):
    """回傳 (drafts, skipped, diagnostics)。diagnostics 涵蓋每一筆「type=monitor 且 value 為
    數字、resolver key 存在」的 kill_watch item（含最終被判定為重複而未落 drafts 的），供
    main() 印 stderr 的逐項診斷表；skipped 是 (kill_watch_id, reason) 列表（internals-type／
    非數字／op 不合法／key 對不到 monitor latest.json／查重重複，都算 skipped 的一種原因）。"""
    ledger_path = Path(ledger_path) if ledger_path else FORECASTS
    kw = _load_kill_watch()
    monitor_keys = hmf._load_monitor_keys()
    existing = _existing_forecasts(ledger_path)
    dup_index = _dup_index(existing)

    seq_state = {}
    for r in existing:
        m = re.match(r"fc_(\d{8})_kw_(\d+)$", r.get("id", ""))
        if m:
            ymd = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}"
            seq_state[ymd] = max(seq_state.get(ymd, 0), int(m.group(2)))

    today = date.today()
    today_str = today.isoformat()
    resolve_by = (today + timedelta(days=HORIZON_DAYS)).isoformat()
    block_key = today_str[:7]

    drafts, skipped, diagnostics = [], [], []

    for item in kw.get("items", []):
        iid = item.get("id", "?")
        ds = item.get("data_source") or {}
        dtype, dkey = ds.get("type"), ds.get("key")

        if dtype != "monitor":
            skipped.append((iid, f"data_source.type={dtype!r}（非 monitor，internals-type 或缺失），跳過"))
            continue

        value_raw = item.get("value")
        if not isinstance(value_raw, (int, float)) or isinstance(value_raw, bool):
            skipped.append((iid, f"value={value_raw!r} 非數字，跳過"))
            continue

        op = item.get("op")
        if op not in (">", "<", ">=", "<="):
            skipped.append((iid, f"op={op!r} 不是可判斷符號（僅支援 >／<>=／<=），跳過"))
            continue

        if not dkey or "/" not in dkey:
            skipped.append((iid, f"data_source.key={dkey!r} 格式不符 <family>/<key>，無法取斜線後段，跳過"))
            continue
        key = dkey.rsplit("/", 1)[-1]

        mitem = monitor_keys.get(key)
        if mitem is None:
            skipped.append((iid, f"monitor key={key!r}（來自 data_source.key={dkey!r}）在 "
                                  "docs/monitor/data/latest.json 找不到，跳過"))
            continue

        cur = hmf._parse_monitor_num(mitem.get("val"))
        if cur is None:
            skipped.append((iid, f"monitor {key} 目前值（{mitem.get('val')!r}）無法解析出數字，跳過"))
            continue

        scale = KEY_VALUE_SCALE.get(key, 1.0)
        value = round(value_raw * scale, 6)
        resolver_unit = RESOLVER_UNIT_OVERRIDE.get(key, item.get("unit") or "")
        series = f"monitor:{key}"

        delta = round(value - cur, 6)
        clim = bmr.climatology(key, op, delta, HORIZON_DAYS)
        p_clim = clim.get("p")
        p_clim_ref = (f"climatology(key={key!r}, op={op!r}, delta={delta}, horizon_days={HORIZON_DAYS}) | "
                      f"{clim.get('window')} | n={clim.get('n')}")

        p_value, p_table_built_at, cond = None, None, None
        if p_mode == "conditional":
            cond = hmf.conditional_p(key, op, delta, HORIZON_DAYS, p_clim)
            p_value = cond.get("p")
            if p_value is not None:
                p_table_built_at = _raw_cache_built_at()

        dup_id = _find_dup(dup_index, series, op, value)

        diagnostics.append({
            "id": iid, "key": key, "current": cur, "threshold": value, "unit": resolver_unit,
            "delta": delta, "p_clim": p_clim, "n": clim.get("n"),
            "p_conditional": (cond.get("p") if cond else None),
            "outcome": f"skip(duplicate of {dup_id})" if dup_id else "new",
        })

        if dup_id:
            skipped.append((iid, f"與既有 {SOURCE} open 命題重複：resolver=(series={series!r}, "
                                  f"op_dir={_op_dir(op)!r}, value={value}) 已存在於 id={dup_id}"
                                  "（這些門檻先前已由 harvest_macro_falsifiers.py 的報告本文 harvest "
                                  "落帳過，見設計稿 §9 row F3「與既有 macro-falsifier open 命題以 "
                                  "(series, op, value) 查重」），跳過"))
            continue

        theme = item.get("theme", "")
        metric_text = item.get("metric_text", "")
        item_unit = item.get("unit") or ""
        claim = f"{resolve_by} 前（90 曆日內）：{metric_text} {op} {value_raw}{item_unit}"
        episode_id = f"macro:{theme}:{hmf._collapse_ws(metric_text)}"

        if p_value is not None:
            note_parts = [cond["method"]]
        else:
            note_parts = ["need_human_p（p_clim 已由 climatology 算出，p 待人工或改用 "
                          "--p-mode conditional 補值）"]
        note_parts += [
            f"kill_watch id={iid}（theme={theme}, as_of={item.get('value_as_of')}, "
            f"confidence={item.get('confidence')}, status={item.get('status')}, "
            f"doc={item.get('doc')}）",
            f"kill_watch 原始門檻：{op} {value_raw}{item_unit}" +
            (f"（換算為 series 顯示單位：{value}{resolver_unit}，"
             "kill_watch 以百分點記、series 以 bp 記，見本檔檔頭「單位換算」段）" if scale != 1.0 else ""),
            f"monitor {key} 目前值＝{mitem.get('date')} {mitem.get('val')}"
            f"（delta={delta}{resolver_unit} vs threshold={value}{resolver_unit}）",
        ]

        drafts.append({
            "id": _next_id(today_str, seq_state),
            "ts": today_str,
            "source": SOURCE,
            "source_ref": f"docs/detective/data/kill_watch.json｜{iid}",
            "claim": claim,
            "p": p_value,
            "horizon_days": HORIZON_DAYS,
            "resolve_by": resolve_by,
            "resolver": {"series": series, "op": op, "value": value, "window": "any_close",
                         "unit": resolver_unit},
            "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
            "note": "｜".join(note_parts),
            "schema": "fc-v2",
            "claim_template": CLAIM_TEMPLATE,
            "p_clim": (round(p_clim, 4) if isinstance(p_clim, float) else p_clim),
            "p_clim_ref": p_clim_ref,
            "p_table_built_at": p_table_built_at,
            "episode_id": episode_id,
            "block_key": block_key,
            "twin_of": None,
        })
        dup_index.append((series, _op_dir(op), value, drafts[-1].get("id")))  # 同批次同門檻只落一張（2026-09-02 整合定案：DXY 102 兩份報告各一筆）

    return drafts, skipped, diagnostics


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="落帳：只 append p 非 null 的草案（含哨兵 twin）")
    ap.add_argument("--p-mode", choices=["conditional"], default=None,
                     help="conditional：p 由 §9 條件式歷史頻率法算出（import "
                          "harvest_macro_falsifiers.conditional_p，不重寫），取代 need_human_p")
    ap.add_argument("--ledger", default=None,
                     help="覆寫查重／落帳目標路徑（預設 knowledge/forecasts.jsonl）；測試或繞過"
                          "真帳簿查重時指向 scratch 檔")
    args = ap.parse_args()

    ledger_path = Path(args.ledger) if args.ledger else FORECASTS
    drafts, skipped, diagnostics = harvest(p_mode=args.p_mode, ledger_path=ledger_path)

    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    for diag in diagnostics:
        cond_part = f" p_conditional={diag['p_conditional']}" if diag.get("p_conditional") is not None else ""
        print(f"[harvest-kill-watch] {diag['id']} key={diag['key']}: current={diag['current']}{diag['unit']} "
              f"threshold={diag['threshold']}{diag['unit']} delta={diag['delta']}{diag['unit']} "
              f"p_clim={diag['p_clim']} n={diag['n']}{cond_part} outcome={diag['outcome']}",
              file=sys.stderr)

    if skipped:
        print(f"\n# 跳過 {len(skipped)} 筆：", file=sys.stderr)
        for name, reason in skipped:
            print(f"#   {name}: {reason}", file=sys.stderr)

    if not args.write:
        n_p = sum(1 for d in drafts if d.get("p") is not None)
        print(f"\n# dry-run：共 {len(drafts)} 筆草案，{n_p} 筆已賦 p（--p-mode conditional，其餘 "
              f"need_human_p）。--write 才會落帳，且只落 p 非 null 的草案。ledger={ledger_path}",
              file=sys.stderr)
        return

    to_write = [d for d in drafts if d.get("p") is not None]
    if not to_write:
        print(f"\n# --write：{len(drafts)} 筆草案 p 皆為 null（need_human_p），依規則全數不寫入。"
              "需先用 --p-mode conditional 賦 p。", file=sys.stderr)
        return

    # 只有 --write 才 import knowledge/forecast_lib.py（同 harvest_macro_falsifiers.py 慣例：
    # dry-run 不 import，降低耦合）。
    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl
    except ImportError as e:
        print(f"[harvest-kill-watch][ERROR] knowledge/forecast_lib.py 尚未建立或無法 import（{e}）。",
              file=sys.stderr)
        sys.exit(2)

    n_written, n_twins = fl.append(to_write, path=ledger_path, write=True)
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵"
          f"（{len(drafts) - len(to_write)} 筆 p=null 被跳過，need_human_p）。ledger={ledger_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
