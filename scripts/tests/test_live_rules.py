"""實盤規則正本（knowledge/live_rules.toml、scripts/live_rules.py）的單元測試。

- 乾淨的正本 check 通過；supertrend_core 的常數由正本算出，名稱、型別、鍵的順序照舊。
- check／load 擋下：不認得的鍵、改動日期倒序、權重相加不是 10000 bps、全史參數設某日起生效、程式寫死的值被改、
  只支援一次切換的鍵被別條改、型別錯、別名單獨設權重、權重不是整數 bps、帳本標題對不上、讀不到檔、TOML 語法錯。
- at() 在每個生效日的前一天、當天、後一天。
- 環境變數覆寫生效日（同一行程與新行程 import supertrend_core 兩種）；正本壞掉時 import supertrend_core 直接失敗。
數值不寫死在測試裡：預期值從正本推，改規則不用改這支測試（數值不變由黃金重播 scripts/tests/golden 把關）。
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import live_rules as lr  # noqa: E402
import supertrend_core as stc  # noqa: E402

TEXT = lr.PATH.read_text(encoding="utf-8")
R = lr.load()
ENV_NAMES = [c["env_override"] for c in R["change"] if c.get("env_override")]


def shift(d: str, n: int) -> str:
    return (date.fromisoformat(d) + timedelta(days=n)).isoformat()


def mutated(tmp_path, *reps, append=""):
    s = TEXT
    for a, b in reps:
        assert s.count(a) == 1, f"測試樣板在正本裡找不到（或不只一處）：{a!r}"
        s = s.replace(a, b)
    p = tmp_path / "live_rules.toml"
    p.write_text(s + append, encoding="utf-8")
    return p


@pytest.fixture
def no_env(monkeypatch):
    for n in ENV_NAMES:
        monkeypatch.delenv(n, raising=False)


# ---------------------------------------------------------------- 乾淨的正本
def test_clean_rules_pass_check():
    assert lr.check() == []
    assert lr.main(["check"]) == 0


def test_core_constants_come_from_rules():
    st, z = R["params"]["supertrend"], R["params"]["zband"]
    assert stc.ST_PARAMS == {k: tuple(v) for k, v in st["atr"].items()}
    assert list(stc.ST_PARAMS) == list(st["atr"])
    assert all(type(n) is int and type(f) is float for n, f in stc.ST_PARAMS.values())
    assert (stc.W_WEEK, stc.W_MONTH) == (st["w_week"], st["w_month"])
    assert type(stc.W_WEEK) is float and type(stc.W_MONTH) is float
    assert stc.TF == {"week": (st["week_rule"], "週線"), "month": (st["month_rule"], "月線")}
    for const, dec, cid in (("ST_CUTOVER_DATE", "ST_CUTOVER_DECISION_DATE", "st-index"),
                            ("LEG_WEIGHTS_CUTOVER_DATE", "LEG_WEIGHTS_DECISION_DATE", "us-weights-70-30"),
                            ("TW_L2_CUTOVER_DATE", "TW_L2_DECISION_DATE", "tw-l2-20-40-40"),
                            ("BB_TAKEBACK_CUTOVER_DATE", "BB_TAKEBACK_DECISION_DATE", "takeback")):
        assert getattr(stc, const) == lr.effective(cid) and type(getattr(stc, const)) is str
        assert getattr(stc, dec) == lr.change(cid)["decided"] and type(getattr(stc, dec)) is str
    l2 = R["params"]["l2"]
    assert stc.TW_L2_WEIGHT == lr.change("tw-l2-20-40-40")["set"]["weights"][l2["symbol"]]
    assert type(stc.TW_L2_WEIGHT) is float
    assert (stc.TW_L2_TB_LEVEL, stc.TW_L2_MULT) == (l2["takeback_level"], l2["exposure_multiple"])
    assert type(stc.TW_L2_TB_LEVEL) is int and type(stc.TW_L2_MULT) is int
    assert (stc.BB_K, stc.BB_REARM, stc.BB_LEVEL, stc.BB_WIN) == (-z["trigger"], z["rearm"], R["params"]["takeback"]["level"],
                                                                  z["window_weeks"])
    assert [type(x) for x in (stc.BB_K, stc.BB_REARM, stc.BB_LEVEL, stc.BB_WIN)] == [float, float, int, int]
    assert list(stc.leg_weights("2026-01-01")) == ["QQQ", "SMH", "SMH.L", "0050.TW", "2330.TW"]


def test_param_handles_dotted_symbols():
    assert lr.param("params.supertrend.atr.0050.TW") == list(stc.ST_PARAMS["0050.TW"])
    assert lr.param("params.supertrend.atr.SMH.L") == list(stc.ST_PARAMS["SMH.L"])
    with pytest.raises(lr.RulesError):
        lr.param("params.zband.nope")


# ---------------------------------------------------------------- at()：生效日前後
def _expected(day: str) -> dict:
    """獨立重算：第一段值，生效日 <= day 的改動依檔案順序覆蓋（正本已驗證依生效日排序）。"""
    s = {sec: dict(kv) for sec, kv in R["timeline"].items()}
    for c in R["change"]:
        if c.get("set") and c["effective"] <= day:
            for sec, kv in c["set"].items():
                s[sec].update(kv)
    for a, t in R["markets"]["us"]["alias"].items():
        s["weights"][a] = s["weights"][t]
    return s


@pytest.mark.parametrize("cid", [c["id"] for c in R["change"] if c.get("set")])
def test_at_day_before_on_and_after_effective(cid, no_env):
    ch = lr.change(cid)
    eff = ch["effective"]
    for day in (shift(eff, -1), eff, shift(eff, 1)):
        got = lr.at(day)
        assert got == _expected(day), day
        assert lr.weights(day) == got["weights"]
        assert stc.leg_weights(day) == {k: got["weights"][k] for k in stc.leg_weights(day)}
    for sec, kv in ch["set"].items():
        for k, v in kv.items():
            assert lr.at(shift(eff, -1))[sec][k] != v, f"{cid} {sec}.{k} 生效前一天就已經是新值"
            assert lr.at(eff)[sec][k] == v and lr.at(shift(eff, 1))[sec][k] == v
    alias = R["markets"]["us"]["alias"]
    for day in (shift(eff, -1), eff):
        w = lr.weights(day)
        assert all(w[a] == w[t] for a, t in alias.items())


def test_at_accepts_timestamps_and_datetimes(no_env):
    import pandas as pd
    eff = lr.effective("tw-l2-20-40-40")
    assert lr.at(pd.Timestamp(eff)) == lr.at(eff) == lr.at(date.fromisoformat(eff))
    assert stc.leg_weights(f"{eff} 00:00:00") == stc.leg_weights(eff)


# ---------------------------------------------------------------- 環境變數覆寫
def test_env_override_in_process(monkeypatch):
    """環境變數在讀正本那一刻取一次（跟改版前 import 時讀一次同語意）：之後才設的不影響已讀的那份。"""
    ch = lr.change("tw-l2-20-40-40")
    env, eff = ch["env_override"], ch["effective"]
    later = shift(eff, 3)
    leg = R["markets"]["tw"]["legs"][0]
    monkeypatch.setenv(env, later)
    r2 = lr.load(fresh=True)
    assert lr.effective("tw-l2-20-40-40", r2) == later
    assert lr.weights(shift(later, -1), r2)[leg] == R["timeline"]["weights"][leg]
    assert lr.weights(later, r2)[leg] == ch["set"]["weights"][leg]
    assert lr.load() is R and lr.effective("tw-l2-20-40-40") == stc.TW_L2_CUTOVER_DATE   # 已讀的那份不變
    assert stc.leg_weights(shift(later, -1)) == {k: lr.weights(shift(later, -1))[k] for k in stc.leg_weights(eff)}
    monkeypatch.setenv(env, "")               # 空字串＝沒設（跟改版前 os.environ.get(...) or 日期 同語意）
    r3 = lr.load(fresh=True)
    assert lr.effective("tw-l2-20-40-40", r3) == eff
    assert lr.weights(eff, r3)[leg] == ch["set"]["weights"][leg]


def test_env_override_new_process():
    tw, tb = lr.change("tw-l2-20-40-40"), lr.change("takeback")
    env = {k: v for k, v in os.environ.items() if k not in ENV_NAMES}
    env.update({tw["env_override"]: "2026-11-13", tb["env_override"]: "2026-11-20"})
    code = ("import json, supertrend_core as s; print(json.dumps([s.TW_L2_CUTOVER_DATE, s.BB_TAKEBACK_CUTOVER_DATE, "
            "s.ST_CUTOVER_DATE, s.leg_weights('2026-11-12')['0050.TW'], s.leg_weights('2026-11-13')['0050.TW']]))")
    out = subprocess.run([sys.executable, "-c", code], cwd=SCRIPTS, env=env, capture_output=True, text=True, check=True)
    got = json.loads(out.stdout.strip().splitlines()[-1])
    assert got == ["2026-11-13", "2026-11-20", lr.change("st-index")["effective"],
                   R["timeline"]["weights"]["0050.TW"], tw["set"]["weights"]["0050.TW"]]


def test_broken_rules_stop_supertrend_core(tmp_path):
    """正本格式錯：import supertrend_core 直接失敗，沒有程式內備援常數。"""
    (tmp_path / "scripts").mkdir()
    for f in ("supertrend_core.py", "live_rules.py"):
        shutil.copy(SCRIPTS / f, tmp_path / "scripts" / f)
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "knowledge" / "live_rules.toml").write_text(TEXT.replace('"0050.TW" = 0.4', '"0050.TW" = 0.41'),
                                                            encoding="utf-8")
    r = subprocess.run([sys.executable, "-c", "import supertrend_core"], cwd=tmp_path / "scripts",
                       capture_output=True, text=True)
    assert r.returncode != 0 and "RulesError" in r.stderr and "10100 bps" in r.stderr
    (tmp_path / "knowledge" / "live_rules.toml").unlink()
    r = subprocess.run([sys.executable, "-c", "import supertrend_core"], cwd=tmp_path / "scripts",
                       capture_output=True, text=True)
    assert r.returncode != 0 and "讀不到實盤規則正本" in r.stderr


# ---------------------------------------------------------------- check 擋下的寫法
TW_L2_W = '"0050.TW" = 0.4\n"2330.TW" = 0.4\n"00631L.TW" = 0.2\n'
BAD = {
    "不認得的鍵（最上層、之後階段的段落）": (dict(append="\n[lint]\nx = 1\n"), "lint：不認得的鍵"),
    "不認得的鍵（巢狀）": (dict(reps=[("rearm = -1.0", "rearm = -1.0\nrearn = -1.0")]), "params.zband.rearn：不認得的鍵"),
    "改動日期倒序": (dict(reps=[("effective = 2026-11-06\nfirst_trade = 2026-11-09",
                              "effective = 2026-11-03\nfirst_trade = 2026-11-09")]), "早於上一條"),
    "權重相加不是 10000 bps": (dict(reps=[(TW_L2_W, TW_L2_W.replace("0.4\n\"2330", "0.41\n\"2330"))]), "台股權重相加 10100 bps"),
    "權重不是整數 bps": (dict(reps=[('"QQQ" = 0.7\n"SMH" = 0.3\n', '"QQQ" = 0.70005\n"SMH" = 0.29995\n')]), "整數 bps"),
    "權重帶浮點尾數": (dict(reps=[('"QQQ" = 0.7\n"SMH" = 0.3\n', '"QQQ" = 0.7\n"SMH" = 0.30000000000000004\n')]), "不帶浮點尾數"),
    "別名單獨設權重": (dict(reps=[('"QQQ" = 0.7\n"SMH" = 0.3\n', '"QQQ" = 0.7\n"SMH" = 0.3\n"SMH.L" = 0.3\n')]), "別名"),
    "全史參數寫進 set（某日起生效）": (dict(append="[change.set.zband]\ntrigger = -2.4\n"), "全史參數不能設某日起生效"),
    "全史參數改動沒標 whole_history": (dict(append='[change.params]\n"params.zband.trigger" = -2.5\n'),
                                  "全史參數不能設某日起生效"),
    "whole_history 紀錄跟現值不符": (dict(reps=[('"params.capital.tw_index_share" = 1.0', '"params.capital.tw_index_share" = 0.7')]),
                                 "要等於現值"),
    "程式寫死的值被改": (dict(reps=[("exit = 0.0 ", "exit = 0.5 ")]), "params.zband.exit：程式只支援"),
    "只支援一次切換的鍵被別條改": (dict(append='\n[[change]]\nid = "takeback-off"\ntitle = "x"\neffective = 2026-11-20\n'
                                       'decided = 2026-11-20\n[change.set.takeback]\nenabled = false\n'),
                                 "程式只支援由 change 'takeback' 改一次"),
    "型別錯（1 不算小數）": (dict(reps=[("tw_index_share = 1.0 ", "tw_index_share = 1 ")]), "型別要是 float"),
    "週月權重驗算": (dict(reps=[("levels = [100, 70, 30, 0]", "levels = [100, 60, 40, 0]")]), "levels：依週月權重應為"),
    "資金換算驗算": (dict(reps=[("us_seat_pct = 6.0 ", "us_seat_pct = 6.5 ")]), "要等於 10000"),
    "帳本標題對不上": (dict(reps=[('ledger = "2026-11-06：指數部加「下軌接回」"', 'ledger = "2026-11-06：沒有這條"')]), "帳本"),
    "TOML 語法錯": (dict(reps=[("w_week = 0.7\n", "w_week = 0.7.1\n")]), "格式錯"),
}


@pytest.mark.parametrize("case", list(BAD))
def test_check_rejects(case, tmp_path):
    kw, msg = BAD[case]
    p = mutated(tmp_path, *kw.get("reps", []), append=kw.get("append", ""))
    errs = "\n".join(lr.check(p))
    assert msg in errs, errs
    assert lr.main(["check", "--path", str(p)]) == 1
    if case != "帳本標題對不上":           # 帳本只在 check 驗；其他問題 load() 也要擋（程式 import 時就停）
        with pytest.raises(lr.RulesError):
            lr.load(p, fresh=True)


def test_missing_file_rejected(tmp_path, monkeypatch):
    assert "讀不到實盤規則正本" in "\n".join(lr.check(tmp_path / "nope.toml"))
    monkeypatch.setattr(lr, "PATH", tmp_path / "nope.toml")
    with pytest.raises(lr.RulesError, match="讀不到實盤規則正本"):
        lr.load(fresh=True)
