"""live_notify 每日確認：「有沒有變動」以資料日是否發生過可行動變化為準，不是這一班有沒有提醒檔。

fixture 是 2026-11-10 實際的 state.json（精簡版：只留確認用到的欄位）：台股 11-10 收盤有正二權重切換，
但確認那一步第一次跑時已經沒有提醒檔，當時貼出「沒有變動，不用下單」。
"""
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import live_notify as ln  # noqa: E402

REAL = json.loads((Path(__file__).parent / "fixtures" / "live_notify_state_20261110.json").read_text(encoding="utf-8"))
NOW = datetime(2026, 11, 10, 10, 0, tzinfo=timezone.utc)   # 台北 18:00：台股 11-10 已收盤，美股應有 11-09
ALERT_TW = "• 台股 00631L：權重切換\n"


def lines(state, alert=None, ns=None, now=NOW):
    ns = {} if ns is None else ns
    return ln.confirm_lines(state, alert, ns, now, sim=True), ns


def pick(out, name):
    return [x for x in out if name in x]


def quiet_state():
    s = copy.deepcopy(REAL)
    s["last_change_date"] = "2026-11-06"
    s["last_change_desc"] = "美股 QQQ：水位 100% → 50%; 台股 0050：水位 30% → 50%"
    s["overlay"].pop("last_change_date", None)
    return s


def test_real_case_no_alert_file_still_says_changed():
    out, _ = lines(REAL, alert=None)
    tw = pick(out, "台股")[0]
    assert "有變動，見實單信" in tw and "不用下單" not in tw
    assert "00631L" in tw                       # 帶出變了什麼
    assert "不用下單" in pick(out, "美股")[0]    # 美股 11-09 沒有變動，不受影響


def test_plain_no_change():
    out, _ = lines(quiet_state())
    assert all("沒有變動，不用下單" in x for x in out) and len(out) == 2


def test_first_run_with_alert():
    out, _ = lines(quiet_state(), alert=ALERT_TW)
    assert "有變動，見實單信" in pick(out, "台股")[0]
    assert "不用下單" in pick(out, "美股")[0]


def test_no_change_then_change_posts_correction_once():
    ns = {}
    out1, ns = lines(quiet_state(), ns=ns)
    assert "不用下單" in pick(out1, "台股")[0]
    out2, ns = lines(REAL, alert=None, ns=ns)           # 後一班才出現變動（水位字面不變也要更正）
    assert "有變動，見實單信" in pick(out2, "台股")[0] and not pick(out2, "美股")
    out3, ns = lines(REAL, alert=None, ns=ns)           # 再跑一班不重貼
    assert out3 == []


def test_changed_then_later_batch_without_alert_not_downgraded():
    ns = {}
    out1, ns = lines(REAL, alert=ALERT_TW, ns=ns)
    out2, ns = lines(REAL, alert=None, ns=ns)
    assert len(pick(out1, "台股")) == 1 and out2 == []


def test_unknown_when_cannot_tell():
    s = copy.deepcopy(REAL)
    s["last_change_desc"] = "（格式看不懂）"
    out, _ = lines(s)
    assert "可能有變動，請看實單信與主控台" in pick(out, "台股")[0]
    s2 = copy.deepcopy(REAL)
    del s2["last_change_date"]
    out2, _ = lines(s2)
    assert all("不用下單" not in x for x in out2)


def test_us_overlay_change_counts():
    s = quiet_state()
    s["overlay"]["last_change_date"] = "2026-11-09"
    s["overlay"]["last_change_desc"] = "公債 IEF Supertrend（目標 0.0% → 6.0%）"
    out, _ = lines(s)
    assert "有變動" in pick(out, "美股")[0] and "IEF" in pick(out, "美股")[0]
    assert "不用下單" in pick(out, "台股")[0]
