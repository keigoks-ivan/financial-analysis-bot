#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_picks.py — 精選清單「候選區」生成器（現況：兩組皆已退役，本檔只維持 frozen 輸出）。

2026-09-17 起（持有人拍板「精選榜改版」，見 knowledge/rule_ledger.md「精選榜改版：
爆發組退役、十倍組改 v5 小市值池」列／設計稿 notes/site-internal/root/
_picks_v5_smallcap_20260917.md）：**爆發（循環拐點型）組亦退役**，理由與長熬同源——
與 v5 thesis（品質派 ∩ 獲利上修 ∩ 還原歷史新高）互相矛盾，站上記分板顯示循環轉折
形狀 n=20 中位 −2.8%、虧損率 55%（輸家形狀）。退役方式比照長熬（2026-07-29）：
不重建，本檔停止產生 official_baofa/baofa 的實際內容，改寫死輸出空陣列＋
`retired_groups.baofa` 留痕（保留 key 而非整個刪除，讓既有讀 official_baofa/baofa
兩個 key 的下游消費端（scripts/build_rotation.py／scripts/build_crowding.py／
scripts/generate_list_forecasts.py）拿到空陣列而非 KeyError，過渡一輪）。原本餵給
爆發組判定的整套 pipeline（build_trigger_map／build_grp_set／parse_id_themes／
build_trend_resolver／late_cycle／build_baofa 及相關常數，讀 cyclical-track／
sop-funnel／radar／arena／ID 主題產業趨勢閘）**已一併移除，勿重建**——十倍組現在
直接讀 GRP 席位同一套 v5 規則（scripts/build_tenbagger.py），不再需要本檔的機械判定。

本檔仍掛在 DD/DCA 同步鏈（scripts/update_dd_index.py 每次呼叫一次）繼續執行，純粹
是為了讓 candidates.json 的 as_of／retired_groups 標記保持新鮮，不代表還有實質內容
在產生；獨立的每週排程步驟已移除（見 .github/workflows/weekly-market-update.yml）。

長熬・品質成長（已於 2026-07-29 退役，勿重建）：
  原規則＝DD 進場 ∩ 護城河閘 ∩ 產業趨勢「對」。**退役理由是與 GRP 席位職能重疊**——
  它是三組裡唯一跟甲線 GRP 搶同一塊地的組（當日實測 5 檔中 3 檔與核心席重複：
  ASML／NVDA／APH），而甲線的權威答案本來就歸 GRP 席位（陣容）。持有人裁決「不整合、
  直接拿掉」，理由見對話：把長熬的產業寬度閘搬進 GRP 會誤殺 LLY（寬度 72.2）與
  TSM（74.6）兩個現任核心席，且該閘鑑別力弱（GRP 過閘 48 檔中 65% 判「對」）、
  21% 因 ID 未覆蓋而「樣本不足」＝資料缺失被當負面訊號。
  下游若需甲線名單，一律讀 docs/engine/arena.json 的 core_seats / sat_seats。

爆發・循環上修（已於 2026-09-17 退役，勿重建）：
  原規則＝cyclical-track 全數合格名單 ∩ 非過熱（🔥）∩ 站上年線 → 自動上榜，兩道
  v2 守門（12M >+150% 或 26W >+80% 標晚段、FY+2 共識低於 FY+1 標共識路徑下彎）只
  列候選、不進正式榜。退役理由見上檔頭段。

Fail-safe：
  本檔現在不讀任何會失敗的候選來源（cyclical-track／sop-funnel／radar／arena／ID
  皆已不讀）；唯一的讀取（dd-screener latest.json 取 as_of）失敗時 fallback 今天
  日期，仍照常寫出 frozen 輸出（exit 0）。
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")

LATEST = os.path.join(DOCS, "dd-screener", "latest.json")
OUT = os.path.join(DOCS, "picks", "candidates.json")

TW8 = timezone(timedelta(hours=8))


def warn(msg):
    print(f"[build_picks] WARN: {msg}", file=sys.stderr)


def load_json(path, label):
    """Return parsed JSON or None (with warning) — never raises."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(f"{label} 檔案不存在，跳過：{path}")
    except (json.JSONDecodeError, OSError) as e:
        warn(f"{label} 無法解析，跳過：{path}（{e}）")
    return None


def main():
    latest = load_json(LATEST, "latest.json (DD screener，僅取 as_of)")
    as_of = (latest or {}).get("as_of") or datetime.now(TW8).strftime("%Y-%m-%d")

    payload = {
        "as_of": as_of,
        "generated_at": datetime.now(TW8).isoformat(),
        "note": ("兩組皆已退役（見 retired_groups）：長熬 2026-07-29、爆發 2026-09-17。"
                 "甲線（結構長抱）權威名單讀 docs/engine/arena.json 的 core_seats／"
                 "sat_seats；十倍組現讀 docs/picks/tenbagger.json（v5 小市值池，同一套 "
                 "GRP 席位規則跑在 $10億–$200億市值帶）。official_baofa／baofa 兩個 "
                 "key 保留為空陣列，供既有下游消費端（scripts/build_rotation.py／"
                 "scripts/build_crowding.py／scripts/generate_list_forecasts.py）"
                 "過渡一輪不因 key 消失而出錯，尚未清空刪除。"),
        "retired_groups": {
            "changhao": {
                "retired_on": "2026-07-29",
                "reason": "與三閘評分席位（engine/arena.json core_seats）職能重疊，三閘評分結構線權威歸三閘評分",
                "successor": "docs/engine/arena.json → core_seats / sat_seats",
            },
            "baofa": {
                "retired_on": "2026-09-17",
                "reason": "與 v5 thesis（品質派 ∩ 獲利上修 ∩ 還原歷史新高）矛盾——站上記分板顯示循環轉折形狀 n=20 中位 −2.8%、虧損率 55%（輸家形狀）",
                "successor": "docs/picks/tenbagger.json（v5 小市值池：同一套 GRP 席位 v5 規則跑在 $10億–$200億市值帶）",
            },
        },
        "counts": {
            "official_baofa": 0,
            "baofa": 0,
        },
        "official_baofa": [],
        "baofa": [],
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[build_picks] wrote {OUT}（兩組皆已退役，frozen 輸出，as_of={as_of}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
