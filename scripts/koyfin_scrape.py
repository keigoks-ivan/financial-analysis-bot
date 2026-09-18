#!/usr/bin/env python3
"""Koyfin watchlist browser scraper — automates the Chrome-by-hand steps of
.claude/skills/refresh-eps-screener-web/SKILL.md (Step 0/1/1.5/2/3/4) with
Playwright, so the owner runs one command instead of driving Chrome manually.

Requires python3 (3.9.6) + Playwright, NOT python3.12 (Playwright for Python
is only installed for python3 in this environment — see
scripts/koyfin_refresh_all.py, which shells out to `python3` for this script).

Two modes:

    python3 scripts/koyfin_scrape.py --login
        Opens a HEADED persistent browser profile at ~/.koyfin-playwright on
        https://app.koyfin.com/ and waits (polling, up to 10 minutes) for the
        user to log in manually. Never types credentials (constitution: never
        enter the user's credentials on their behalf). One-time setup step.

    python3 scripts/koyfin_scrape.py --watchlist {screener,smallcap,largecap} [--headless]
    python3 scripts/koyfin_scrape.py --all [--headless]
        Reuses the --login profile, navigates to the watchlist's URL, injects
        koyfin_scraper.js, runs the scrape, verifies the djb2 fingerprint in
        Python, and writes
        data/eps-estimates/raw/koyfin_<name>_raw_YYYYMMDD.txt (+ a
        .fingerprint.json sidecar) on match. Refuses to write on mismatch.

Exit codes: 0 ok; 1 generic failure (e.g. --login timed out); 3 not logged in
("請先跑 --login"); 4 wrong tab / currency not USD; 5 fingerprint mismatch
(browser vs. Python recompute disagree — zero-transcription guarantee, see
skill Step 4); 6 scrape produced 0 rows (grid never rendered / navigation
failed).

NAME here (--watchlist argument) is the short internal family key
("screener"/"smallcap"/"largecap"), not the Koyfin tab label — see
scripts/koyfin_families.py's module docstring for why (matches the existing
manual-run raw-filename convention).

2026-09-18：分頁作用中標記（kui-tabs-header-item--active／aria-selected）、表格
容器（table-styles__table__scrollContainer___*）、USD 按鈕（button.kui-button >
span.kui-button__text）三個選擇器已用登入中的 Chrome 對照真實頁面確認。整條
--watchlist 抓取流程（Playwright 持久 profile）要等第一次 --login 後才跑得到，
尚未端到端跑過。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIEWPORT = {"width": 1600, "height": 900}
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from koyfin_families import FAMILIES, FAMILY_ORDER, raw_txt_name, fingerprint_sidecar_name  # noqa: E402

DEFAULT_PROFILE_DIR = Path.home() / ".koyfin-playwright"
SCRAPER_JS_PATH = SCRIPTS_DIR / "koyfin_scraper.js"
RAW_DIR = ROOT / "data" / "eps-estimates" / "raw"
KOYFIN_HOME = "https://app.koyfin.com/"

LOGIN_POLL_SECS = 3
LOGIN_TIMEOUT_SECS = 600  # 10 minutes


def _djb2(s: str) -> int:
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return h


def _is_logged_out(page) -> bool:
    """登出訊號（2026-09-18 對照真實頁面後改）：三個任一成立就算登出——
    (1) 網址在 /login（Koyfin 未登入開 watchlist 會轉到 /login?prevUrl=...）；
    (2) 頁上有密碼欄；(3) 頁首有「Log In」按鈕（未登入的首頁沒有密碼欄，
    只有 Sign Up Free／Log In 兩顆按鈕，原本只看密碼欄會誤判成已登入）。"""
    try:
        if "/login" in (page.url or ""):
            return True
        if page.locator('input[type="password"]').count() > 0:
            return True
        return page.evaluate(
            "() => [...document.querySelectorAll('a,button')]"
            ".some(e => /^log ?in$/i.test(e.textContent.trim()))"
        )
    except Exception:
        return False


def _tabs_rendered(page) -> bool:
    try:
        return page.locator("span.kui-tabs-header-item__label-text").count() > 0
    except Exception:
        return False


def cmd_login(profile_dir: Path, headless: bool) -> int:
    """一次性人工登入：開 watchlist 網址（未登入會轉到 /login），等使用者自己登入。
    「已登入」的判準是登出訊號消失且 watchlist 分頁列真的渲染出來，不是「沒看到
    密碼欄」（首頁本來就沒有密碼欄，2026-09-18 第一次跑就因此秒關）。"""
    from playwright.sync_api import sync_playwright

    profile_dir.mkdir(parents=True, exist_ok=True)
    print(f"[login] persistent profile: {profile_dir}")
    target = FAMILIES[FAMILY_ORDER[0]]["url"]
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir), headless=headless,
            viewport=VIEWPORT,   # 1280 寬時 Koyfin 會收起工具列（USD 按鈕消失），見 2026-09-18 實測
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(target, wait_until="domcontentloaded")
        print("[login] 瀏覽器已開。請在視窗裡登入 Koyfin（本腳本不會輸入帳密）。"
              "登入後會自動回到 watchlist 頁，看到分頁列就算完成，最多等 10 分鐘。", flush=True)
        deadline = time.time() + LOGIN_TIMEOUT_SECS
        while time.time() < deadline:
            # 登入流程（尤其 Google／SSO）可能開新分頁，所以每一頁都看，不只盯原本那頁。
            for pg in list(context.pages):
                try:
                    if not _is_logged_out(pg) and _tabs_rendered(pg):
                        print("[login] 偵測到 watchlist 分頁列，登入完成；profile 已保存。", flush=True)
                        time.sleep(2)
                        context.close()
                        return 0
                except Exception:
                    continue
            time.sleep(LOGIN_POLL_SECS)
        print("[login] 10 分鐘內沒偵測到登入完成。")
        context.close()
        return 1


def _find_active_tab_label(page, expected_label: str) -> tuple[bool, str]:
    """作用中分頁檢查（2026-09-18 已對照真實頁面）：作用中的分頁是
    div.kui-tabs-header-item，帶 class kui-tabs-header-item--active 且
    aria-selected="true"，名稱在子元素 span.kui-tabs-header-item__label-text。
    下面前兩個選擇器都會命中；第三個與最後的「名稱有出現」只是保險。
    Returns (ok, detail)。"""
    sel_candidates = [
        f'[aria-selected="true"] .kui-tabs-header-item__label-text',
        f'.kui-tabs-header-item--active .kui-tabs-header-item__label-text',
        f'[class*="kui-tabs-header-item"][class*="active"] .kui-tabs-header-item__label-text',
    ]
    for sel in sel_candidates:
        try:
            loc = page.locator(sel)
            if loc.count() > 0:
                text = loc.first.inner_text().strip()
                return (text == expected_label, f"active-tab selector matched, text={text!r}")
        except Exception:
            continue
    # Fallback: just confirm the label is rendered somewhere in the tab bar.
    try:
        labels = page.locator("span.kui-tabs-header-item__label-text").all_inner_texts()
        labels = [t.strip() for t in labels]
        if expected_label in labels:
            return (True, f"FALLBACK (no active-tab selector matched): label present in tabs={labels}")
        return (False, f"label not found in rendered tabs={labels}")
    except Exception as e:
        return (False, f"could not read tab bar: {e}")


def _check_usd_toggle(page) -> bool:
    """幣別 toggle 檢查（2026-09-18 已對照真實頁面）：右上角是一顆
    button.kui-button，文字在 span.kui-button__text，內容 "USD"。先找這個精確
    結構，找不到再退回「頁面上任一可見的精確文字 USD」。"""
    try:
        loc = page.locator('button.kui-button span.kui-button__text', has_text="USD")
        if loc.count() > 0 and loc.first.inner_text().strip() == "USD" and loc.first.is_visible():
            return True
    except Exception:
        pass
    try:
        return page.get_by_text("USD", exact=True).first.is_visible()
    except Exception:
        return False


def scrape_one(context, family_key: str, date_str: str, timeout_sec: int) -> int:
    fam = FAMILIES[family_key]
    page = context.new_page()
    print(f"[{family_key}] navigating to {fam['url']}")
    page.goto(fam["url"], wait_until="domcontentloaded")

    # 等到「轉去 /login」或「分頁列出現」其中一個，最多 20 秒，再判登入狀態。
    for _ in range(40):
        if _is_logged_out(page) or _tabs_rendered(page):
            break
        page.wait_for_timeout(500)
    if _is_logged_out(page):
        print(f"[{family_key}] 請先跑 --login（未登入：轉到 /login 或頁首有 Log In 按鈕）")
        page.close()
        return 3

    page.wait_for_timeout(1500)  # let tab bar / grid settle

    ok_tab, detail_tab = _find_active_tab_label(page, fam["watchlist_tab"])
    if not ok_tab:
        print(f"[{family_key}] active tab is not '{fam['watchlist_tab']}': {detail_tab}")
        page.close()
        return 4
    print(f"[{family_key}] tab check: {detail_tab}")

    if not _check_usd_toggle(page):
        print(f"[{family_key}] currency toggle does not show USD — stop (pipeline assumes USD)")
        page.close()
        return 4

    try:
        page.wait_for_selector('[class*="table__scrollContainer___"]', timeout=30_000)
    except Exception as e:
        print(f"[{family_key}] grid never rendered: {e}")
        page.close()
        return 6

    page.add_script_tag(path=str(SCRAPER_JS_PATH))
    page.set_default_timeout(timeout_sec * 1000)
    result = page.evaluate("(opts) => window.__koyfinScrape(opts)", {})

    if not result or result.get("error"):
        print(f"[{family_key}] scrape failed: {result}")
        page.close()
        return 6

    rows = result["rows"]
    lines = result["lines"]
    if rows == 0:
        print(f"[{family_key}] scraped 0 rows — grid empty or scraper mis-targeted")
        page.close()
        return 6

    # Python-side djb2 recompute (Step 4, zero-transcription guarantee):
    # same algorithm as the browser side, over the same newline-joined canon.
    canon = "\n".join(lines)
    py_rows = len(lines)
    py_bytes = len(canon)
    py_djb2 = _djb2(canon)

    js_rows, js_bytes, js_djb2 = result["rows"], result["bytes"], result["djb2"]
    if (py_rows, py_bytes, py_djb2) != (js_rows, js_bytes, js_djb2):
        print(
            f"[{family_key}] FINGERPRINT MISMATCH — refusing to write.\n"
            f"  browser: rows={js_rows} bytes={js_bytes} djb2={js_djb2}\n"
            f"  python:  rows={py_rows} bytes={py_bytes} djb2={py_djb2}"
        )
        page.close()
        return 5

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / raw_txt_name(family_key, date_str)
    raw_path.write_text(canon, encoding="utf-8")

    sidecar_path = RAW_DIR / fingerprint_sidecar_name(family_key, date_str)
    sidecar_path.write_text(
        json.dumps(
            {
                "family": family_key,
                "watchlist_tab": fam["watchlist_tab"],
                "date": date_str,
                "rows": py_rows,
                "bytes": py_bytes,
                "djb2": py_djb2,
                "header_count": result.get("headerCount"),
                "ticker_column_count": result.get("tickerColumnCount"),
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # Step 3 reconciliation: grid ticker-column count vs. rows captured.
    missing = result.get("missingTickers") or []
    tcol = result.get("tickerColumnCount")
    recon = "OK" if not missing else f"MISSING {len(missing)}: {missing}"
    print(
        f"[{family_key}] rows={py_rows} bytes={py_bytes} djb2={py_djb2} "
        f"headerCount={result.get('headerCount')} tickerColumn={tcol} recon={recon} "
        f"-> {raw_path}"
    )
    page.close()
    return 0


def cmd_scrape(profile_dir: Path, names: list[str], date_str: str, headless: bool, timeout_sec: int) -> int:
    from playwright.sync_api import sync_playwright

    if not profile_dir.exists():
        print(f"[scrape] no persistent profile at {profile_dir} — run --login first")
        return 3

    worst = 0
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir), headless=headless,
            viewport=VIEWPORT,   # 1280 寬時 Koyfin 會收起工具列（USD 按鈕消失），見 2026-09-18 實測
        )
        try:
            for name in names:
                rc = scrape_one(context, name, date_str, timeout_sec)
                worst = max(worst, rc)
                if rc != 0:
                    print(f"[{name}] stopped (exit {rc}) — not proceeding to remaining watchlists is NOT "
                          f"automatic here; continuing to next watchlist so a single bad tab doesn't block "
                          f"the others (koyfin_refresh_all.py enforces the hard stop at the fingerprint/"
                          f"gate level per family).")
        finally:
            context.close()
    return worst


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--login", action="store_true", help="One-time manual login (headed).")
    mode.add_argument("--watchlist", choices=FAMILY_ORDER, help="Scrape a single watchlist family.")
    mode.add_argument("--all", action="store_true", help="Scrape all three watchlists in order.")
    ap.add_argument("--headless", action="store_true", help="Run headless (Koyfin may block this).")
    ap.add_argument("--profile-dir", type=Path, default=DEFAULT_PROFILE_DIR)
    ap.add_argument("--date", default=None, help="YYYYMMDD override for the raw filename (default: today).")
    ap.add_argument("--timeout-sec", type=int, default=1800,
                     help="Max seconds to wait for a single watchlist's full scrape (default 1800).")
    args = ap.parse_args()

    if args.login:
        return cmd_login(args.profile_dir, args.headless)

    date_str = args.date or datetime.now().strftime("%Y%m%d")
    names = FAMILY_ORDER if args.all else [args.watchlist]
    return cmd_scrape(args.profile_dir, names, date_str, args.headless, args.timeout_sec)


if __name__ == "__main__":
    raise SystemExit(main())
