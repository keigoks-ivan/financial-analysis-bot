"""實單頁（公開）不得寫帳戶結構。帳戶怎麼換倉只寫在寄給持有人的提醒信（2026-10-19 持有人決定）。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE_DIR = ROOT / "docs" / "long-track-w52-adaptive"
FORBIDDEN = ["帳戶", "XNAS", "CBU0", "IGLN", "UCITS", "IBKR", "券商", "account"]


def test_live_page_and_state_have_no_account_terms():
    for name in ("_body.html", "state.json", "cap15.html"):
        text = (PAGE_DIR / name).read_text(encoding="utf-8")
        hits = [w for w in FORBIDDEN if w in text]
        assert not hits, (name, hits)


def test_live_page_has_no_mnq():
    # 舊規則對照頁（cap15.html）談期貨加曝險的研究段落可以提 MNQ；實單頁不行
    for name in ("_body.html", "state.json"):
        assert "MNQ" not in (PAGE_DIR / name).read_text(encoding="utf-8"), name
