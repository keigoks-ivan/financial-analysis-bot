#!/usr/bin/env python3
"""scripts/ddreport.py — v17 WP1a：per-run 目錄、manifest、`plan`、`status`。

只動 `.dd_build/runs/{TICKER}_{DATE}/` 這個新的 per-run 慣例，不改任何既有腳本的
行為或路徑。`plan` 呼叫既有零 LLM 工具（`dd_prior.py`／`dd_evidence.py`／
`dd_numbers_extra.py`，皆原樣呼叫、不改語意）取得證據骨架與軸清單，再依軸分批寫出
子 agent 派工用的 prompt 檔＋`spawn_list.json`。`status` 印 manifest 與各產物存在／
大小，供人工或 orchestrator 檢視進度。

3.9 相容（`from __future__ import annotations`，不用 3.10+ 語法）。

用法：
    python3 scripts/ddreport.py plan TICKER [--date YYYYMMDD] [--archetype X]
        [--peers a,b] [--segments a,b] [--axes-per-batch 2] [--offline]
    python3 scripts/ddreport.py status TICKER DATE

見 notes/site-internal/dd/_wp_spec_v17_20260905.md「共同約定」與「WP1a」段。
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_bundle  # noqa: E402  （WP-C：delta 判斷 prompt 沿用 `_transcript_section` 抓最新一季逐字稿，只 import 不改其內部）
import dd_headless  # noqa: E402  （WP1c 無頭執行器，import 呼叫，不改其內部）
import dd_meta_reader  # noqa: E402  （WP7a peers 來源③：讀 id-meta related_tickers，不改其內部）
import dd_project  # noqa: E402  （WP-H2-1：v19 判斷檔的形狀正規化與投影，唯一轉接）
import dd_metric_resolver  # noqa: E402  （2026-09-07：batch 摘要 Max DD 改用共用 helper，只 import 不改其內部）
import dd_sections  # noqa: E402  （2026-09-06 WP4b：leak_hits／split_sections，gates 用來把 FAIL 歸因到 sid）
import dd_prose_budget  # noqa: E402  （2026-09-08：散文段深度下限閘沿用同一份目標區間，不另定義門檻）
import gen_dd_tables as gdt  # noqa: E402  （2026-09-06 WP4b：C-1 機械段生成＋E12 說明句，不改其內部語意）
import verify_dd_math  # noqa: E402  （2026-09-07：finish 三方一致性沿用同一組權威容差）

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
BUILD_DIR = REPO_ROOT / ".dd_build"
RUNS_DIR = BUILD_DIR / "runs"
PROMPTS_TMPL_DIR = SCRIPTS_DIR / "dd_prompts"
FINISH_MAXDD_EPSILON = 0.01  # 2026-09-07：Max DD 是 judgment 直拷值，只容許序列化微差。

# ---------------------------------------------------------------------------
# WP1d: run 目錄狀態機（Stage 0 → 判斷 → 閘 → 快速版 → 散文〔--full〕）串接常數
# ---------------------------------------------------------------------------
# 2026-09-06 WP4b：`prose` 加在 `brief` 之後。
# 2026-09-11 WP-H2-1：`cmd_run` 的預設 `--until` 改為 "prose"——v19 的產物就是
# 完整版，`--full` 降為 no-op 相容旗標。**快速版（brief）暫不退役**：仍在序列
# 內照跑照產，等 H2 驗收通過由持有人拍板停產（計劃書第十一節）。
STAGE_ORDER = ["stage0", "judged", "gated", "brief", "prose"]
DEFAULT_JUDGMENT_MODEL = "fable"
# 判斷模型↔閘模型對調表（跨模型冷讀，見 _wp_spec_v17_batch2_20260905.md WP1d §4）
GATE_MODEL_FOR = {"fable": "opus", "opus": "sonnet", "sonnet": "opus"}
JUDGE_MAX_TURNS = 10  # 2026-09-05：AVGO／WDAY 第 9 輪才寫完，8 太緊
# WP7b #1（_wp_spec_v17_batch5_20260905.md）：bundle 改內嵌進 prompt（不再讓
# agent 自己 Read 240KB 檔）後，fix agent 仍要讀 77KB judgment.json＋改＋
# 寫＋judge check，4 輪不夠，實測至少 4 步驟＋緩衝，上調為 6。
JUDGE_FIX_MAX_TURNS = 6
# 2026-09-06 判斷段短迴圈（short）：判斷 agent 只拿 Write 工具、≤4 輪——各一次
# Write 寫 judgment／scenario 就停，judge check 與定點修正的派工由 orchestrator
# 代跑（FIX 實測舊 loop 10 輪、cache_read 1.23M；每輪重讀的是整包 bundle）。
# 曾試「無工具單輪回兩個 fenced JSON」：Fable 一次規劃全部會思考 40K token，
# 連同 33K 正文撞 64K 輸出上限被切段，`result` 只剩尾段，故改 Write 短迴圈
# （思考分攤到各輪、產物走工具不走回覆文字）。fenced JSON 解析保留為備援。
# 判斷規則、schema、驗證三支腳本一字不動；只改「誰操作工具」。
# `--judge-mode loop`／`DD_JUDGE_MODE=loop` 回舊路（A/B 用）；replay 模式一律 loop。
JUDGE_MODE_DEFAULT = "short"
# 2026-09-06（FIX_20260908 opus 當判斷模型實測缺口）：緊湊 JSON 輸出偶爾不合法
# （如 `Expecting ',' delimiter`），原 4 輪只夠 Write judgment → Write scenario
# → DONE；加一輪 Bash 語法自檢（`judge_oneshot_tail.md.tmpl` 步驟③）後最壞情況
# 是自檢報錯→整檔重寫一次→再自檢一次→DONE，故上調為 6，留一輪餘裕。
JUDGE_SHORT_MAX_TURNS = 6
JUDGE_SHORT_FIX_MAX_TURNS = 3  # （保留給 loop 回退路徑參考；short 的修正是無工具單輪 patch map）
# 2026-09-06：`_normalize_judge_outputs` 仍解析失敗時的「語法修復」短迴圈上限
# ——一次 Write 整檔修好、一次 Bash 自檢、（若還錯）一次重寫、一次再自檢、回
# DONE；與判斷段主迴圈用同一顆模型，見 `_repair_judge_json_file`。
JUDGE_JSON_REPAIR_MAX_TURNS = 4
_JUDGE_MODE_OVERRIDE = None
GATE_MAX_TURNS = 6
GATE_PATCH_MAX_TURNS = 6
JUDGE_BUDGET_CACHE_READ = 1_200_000
GATE_BUDGET_CACHE_READ = 2_500_000

# 2026-09-06 閘 🔴 修補改 patch map（比照判斷段 short 模式）：CDNS／HPE 實測
# 舊 loop 修補（agent 自己 Read／Write／Bash、重跑 judge check）要 6–9 輪；
# 改無工具單輪回 patch map、orchestrator 代套用＋代跑 check，同樣的修補動作
# 省掉逐輪重讀整包判斷物的 cache_read。`--gate-patch-mode loop`／
# `DD_GATE_PATCH_MODE=loop` 回舊路；replay 模式一律 loop（與判斷段 short/loop
# 對調同一理由：fake_claude.py 的 replay marker 目前只認得 loop 那套逐輪腳本）。
GATE_PATCH_MODE_DEFAULT = "patchmap"
_GATE_PATCH_MODE_OVERRIDE = None

# 2026-09-06 WP4b：散文（prose）agent——只給 Write／Bash（同判斷段 short 模式
# 的 `_spawn_short`），母稿 §4 目標 ≤1.5M cache_read／≤7 輪，熔斷線＝目標 2×
# （由 `dd_headless.spawn` 的 `over_budget` 統一算，不在這裡重算）。
PROSE_MAX_TURNS = 12  # 2026-09-08：TXN 實測 terminal_reason=max_turns——散文段最少需
# 2 次大 Write ＋1 次 check ＋1 次修補 Write ＋1 次 recheck，長段的單次 Write 本身就會
# 跨輪；7 輪下只寫完 prose_A（18.5KB）就被砍，prose_B 整個沒寫出來，切割時撿到上一輪
# 殘留檔，於是被誤讀成「agent 不肯寫長」。同檔的 JUDGE_MAX_TURNS 與
# DIGEST_PER_FILE_MAX_TURNS 都在 2026-09-05 因同一種失效由 8 調到 10，散文段當時沒跟上。
PROSE_BUDGET_CACHE_READ = 1_500_000
# split 時忽略散文 agent 誤寫的這三段（C-1 機械段，`prose prepare` 已生成）。
_PROSE_MECHANICAL_SIDS = ("revlog", "s14", "appA")

# 2026-09-08：與 scripts/hooks/pre-commit 的 v15 DD hard floor 同值（該檔
# `check_report_size "$f" 70000 80000 "DD" 115000`）。改這裡務必同時改那裡，
# 否則 in-loop 閘與發布閘會各說各話。
DD_FULL_FLOOR_BYTES = 70000
# `prose split` 依序處理這三個來源檔；`prose_fix.html` 只在 FAIL 後的補寫輪
# 才會出現，且刻意排最後——同一個 sid 若三個檔都有，後面的覆蓋前面的，讓
# 「只重寫命中的 sid、合成一個小檔再 Write」的補寫語意（見 render-rules.md
# 慣例）不需要散文 agent 重讀或重寫整份 prose_A/B。
_PROSE_SOURCE_FILES = ("prose_A.html", "prose_B.html", "prose_fix.html")

# 最後手段的預設 archetype：coverage-axes.md 裡 by_archetype 附加軸數為 0 的
# 那一類（即「只查 common 軸」的基準情境），在 --archetype 未給、且前份 DD
# 是不含 archetype 欄位的 legacy schema（v14.x 以前）時使用。此為刻意的工程
# 折衷，非隨意猜測——見 notes/site-internal/dd/_wp_spec_v17_20260905.md 驗收
# 段對此邊界案例（CRDO 20260904，prior 為 v14.2、無 archetype 欄）的討論。
DEFAULT_ARCHETYPE = "品質複利成長"

AXES_PER_BATCH_DEFAULT = 2
REUSE_DAYS_DEFAULT = 30

# 2026-09-06：Stage 0 平行度預設 8（CLI 環境變數仍可調）——既有 manifest
# 無法證明「所有軸一軸一 agent」不增成本，故一般軸仍維持每批 2 軸；只有
# 實測容易撞輪次的 per_segment 展開軸逐軸派工。
# 這只影響牆鐘時間（同時開幾個子行程），不影響 token 用量（token 是逐 agent
# 累計、與平行度無關）；若跑批次時撞 rate limit，設回 4（`DD_MAX_PARALLEL=4`）。
STAGE0_MAX_PARALLEL = int(os.environ.get("DD_MAX_PARALLEL", "8"))

# 2026-09-06：軸分批輪次上限常數化（原本硬編在 spawn_list 組裝處）。
# AXES_MAX_TURNS_DEFAULT 沿用既有實測值 10，不改數值；AXES_MAX_TURNS_SEGMENTED
# 給獨立成批的 per_segment 展開軸（如 end_markets）用——FIX 2026-09-06 的
# a_5 批同時含 geo_supply_chain＋end_markets（依 §3 營收段逐一展開）三次在
# 10 輪上限被砍、兩軸全 pending 導致 finalize FAIL，手動改 16 才 13 輪收完；
# 獨立成批後只剩 per_segment 展開軸，14 輪為新實測折衷。
AXES_MAX_TURNS_DEFAULT = 10
AXES_MAX_TURNS_SEGMENTED = 14

SPAWN_TOOLS_COVERAGE = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_NUMBERS = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_DIGEST = ["Read", "Write", "Bash"]
# WP-H2-1（2026-09-11）：六問事實表 agent——只整理事實、不上網（證據不足是缺口，
# 記進 gaps 回報，不自搜補洞），故無 WebSearch／WebFetch。輪次與預算比照逐字稿
# 摘要（同樣是「讀定稿材料寫一份結構化 JSON」的工作），未經真跑校準。
SPAWN_TOOLS_FACTS = ["Read", "Write", "Bash"]
FACTS_MAX_TURNS = 8
BUDGET_CACHE_READ_FACTS = 900_000

# WP7a #5：Stage 0 預算重校（AVGO 2026-09-05 實測），Stage 0 段總目標 ≤6M
# （母稿 §4 表同步改，不在本檔範圍）。
BUDGET_CACHE_READ_COVERAGE = 900_000
BUDGET_CACHE_READ_NUMBERS = 1_200_000

# WP7d：摘要子 agent 拆成一篇逐字稿一個 spawn（HPE 第二次真跑實測：一人讀三篇
# 17 輪撞 16 上限、cache_read 2.54M 超 1.5M 預算——單篇合計約 0.5M×3≈1.5M 且
# 可平行，見 _wp_spec_v17_batch5_20260905.md WP7d）。
DIGEST_PER_FILE_MAX_TURNS = 10  # 2026-09-05：CDNS 長稿一半在第 9 輪被砍
BUDGET_CACHE_READ_DIGEST_PER_FILE = 700_000

# WP7a #1：Koyfin 步驟改零 LLM，plan 內直接 subprocess 呼叫，不再走 spawn。
KOYFIN_DIR = Path.home() / "scripts" / "koyfin-downloader"
KOYFIN_DOWNLOADER = KOYFIN_DIR / "koyfin_downloader.py"
KOYFIN_SELECTOR = KOYFIN_DIR / "transcripts_for_dd.py"
KOYFIN_VENV_PYTHON = KOYFIN_DIR / ".venv" / "bin" / "python"
KOYFIN_DOWNLOAD_TIMEOUT = 300
KOYFIN_SELECTOR_TIMEOUT = 60
KOYFIN_DRIVE_GLOB = "Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股"

# ---------------------------------------------------------------------------
# WP6a: finish／index-row 用的固定路徑（模組層常數，供測試 monkeypatch 覆寫）
# ---------------------------------------------------------------------------
DD_DIR = REPO_ROOT / "docs" / "dd"
INDEX_MD_PATH = DD_DIR / "INDEX.md"
RESEARCH_BODY_PATH = REPO_ROOT / "docs" / "research" / "_body.html"
DD_SCREENER_LATEST_PATH = REPO_ROOT / "docs" / "dd-screener" / "latest.json"
PICKS_CANDIDATES_PATH = REPO_ROOT / "docs" / "picks" / "candidates.json"
TICKER_HUB_DIR = REPO_ROOT / "docs" / "t"  # build_ticker_hubs.py 輸出（update_dd_index 連鎖重生）
SRC_ARCHIVE_DIR = REPO_ROOT / "notes" / "site-internal" / "dd" / "_src"
ID_DIR = REPO_ROOT / "docs" / "id"

# ---------------------------------------------------------------------------
# WP-C（2026-09-10）：例行複審 delta 判斷路由——`_do_judge` 開頭先問
# `dd_delta.py`（零 LLM 差異引擎）本輪跟 prior 存查比起來改了什麼，決定
# Fable 要整份重寫（full）、只補被點名欄位（delta），還是完全不必進 Fable
# （reuse，見下方 DELTA_NOCHANGE_MAX_AGE_DAYS）。規則表列在這裡（repo
# governance：判斷類規則寫在腳本頂部常數），實作見 `_judge_delta_route`／
# `_do_judge_delta`／`_judge_reuse_prior`。
# ---------------------------------------------------------------------------

# (f)：<45 天且 delta 三塊（numbers_changed／coverage_changed／events_changed）
# 皆空 → 不進 Fable，直接複製 prior 判斷物當本輪判斷（只補 meta.date／
# delta_of）。上界刻意比 dd_delta.py 自身的 full_rewrite_required 年限
# （180 天）短很多——這條只想抓「同一週內幾乎零資訊增量」的重跑，不是要
# 放寬到一般複審間隔（例行複審通常是季度、`numbers.price_at_dd` 幾乎必變，
# 這條路徑在真實用量下預期少見，多半靠人工短間隔重跑或測試觸發）。
DELTA_NOCHANGE_MAX_AGE_DAYS = 45

# (b)：evidence.events 目前只有 QC-19 addendum 定義的五個固定類別（見
# `EVENTS_ADDENDUM`）——現行 schema 沒有「guidance 撤回」或「CEO 更迭」
# 專屬事件類別（兩者若被查到，會落在 coverage.capital_markets_pricing 或
# 治理相關軸的 finding 裡，走一般 judgment_fields_to_review 路徑，不在本表
# 管轄——WP-C 未新增這兩類的抓取，已知缺口，見任務回報）。本表只回答
# 「evidence.events 五類裡，新 finding 出現在哪些類別時足以判定為重大事件、
# 直接升級全套」：`ma_merger`（併購，任務指示原文即含）／
# `sec_investigation_restatement`（SEC 調查／重編財報，治理重定價等級，
# 最貼近「法規裁定」語意）／`clinical_fda`（多數非藥品業務為 not_applicable，
# 一旦真的 found 就是監管裁定等級）。`lawsuit_class_action`／
# `product_recall_warning` 留給 delta 正常欄位路由（見 `dd_delta.py` 的
# `EVENTS_CATEGORY_FALLBACK`），不自動升級——範圍畫太廣會讓 delta 路徑名存
# 實亡（任何一條新聞都能把每輪都打回全套）。
EVENTS_MAJOR_CATEGORIES = ("ma_merger", "sec_investigation_restatement", "clinical_fda")

# (d)：`kill_metrics[]`／`triggers[]` 的 `bear_threshold`／`threshold` 是自由
# 文字複合門檻（見 TXN_20260906 實檔，如「連 4 季 <60% 減碼；連 4 季 <58%
# 且 FCF/share 未達→清倉」），沒有統一「metric 標籤 → evidence.numbers 欄位」
# 映射，無法安全機械比對新證據是否已越線——誤判（漏判或假判）都會讓 delta
# 路由靜默錯誤，代價比省下的 Fable 成本高。固定回報這個字串，不嘗試 regex
# 硬猜；未來若要做，需要先把 schema 改成結構化門檻（metric_key/comparator/
# value 三欄），這是本 WP 的已知範圍缺口，見任務回報。
TRIGGER_MECHANICAL_CHECK = "not_mechanizable"

# delta 判斷 agent 的輪次與熔斷線——Fable 單輪（Write judgment／Write
# scenario／Bash 自檢，同 `judge_oneshot_tail.md.tmpl` 精神但輸入小很多，
# 只帶 prior 判斷物＋delta.json＋受影響軸節錄，不帶整包 evidence／digest／
# judgment-rules.md）。budget 目前是未經真實案例校準的估計值——見任務回報。
JUDGE_DELTA_MAX_TURNS = 4
JUDGE_DELTA_BUDGET_CACHE_READ = 500_000


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _pick_python():
    """優先 /tmp/ddvenv/bin/python（若存在且 import yfinance 成功），否則 python3。"""
    venv_py = Path("/tmp/ddvenv/bin/python")
    if venv_py.exists():
        try:
            r = subprocess.run(
                [str(venv_py), "-c", "import yfinance"],
                capture_output=True, timeout=15,
            )
            if r.returncode == 0:
                return str(venv_py)
        except Exception:
            pass
    return "python3"


def _run_dir(ticker, date):
    return RUNS_DIR / "{0}_{1}".format(ticker, date)


def _atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _render_template(tmpl_path, mapping):
    text = Path(tmpl_path).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def _is_segmented_axis(axis):
    """2026-09-06：判定一個（已展開的）軸是否來自 coverage-axes.md 的
    `per_segment: true` 軸（現行唯一一條是 `end_markets`，見
    `.claude/skills/stock-analyst/references/coverage-axes.md`）。直接讀
    `dd_evidence.py::resolve_axes()` 留在 axis dict 上的 `per_segment` 旗標
    ——這是機械可得的既有欄位，不需要另猜 axis id 字面（segments 展開時 id
    會變成 `end_markets__xxx`，只比對字面 `== "end_markets"` 反而漏掉展開後
    的情況；未展開／`_template_only` 情況 id 仍是 `end_markets` 本身，兩種
    情況這個旗標都在）。"""
    return bool(axis.get("per_segment"))


def _axis_block(axes):
    lines = []
    for a in axes:
        lines.append("[{0}] {1}".format(a.get("id"), a.get("name", "")))
        lines.append("Q: {0}".format(a.get("question", "")))
        for q in a.get("queries", []) or []:
            lines.append("  - {0}".format(q))
        if a.get("na_allowed"):
            lines.append("  (na_allowed=true)")
        lines.append("")
    text = "\n".join(lines).rstrip()
    return text + "\n" if text else ""


EVENTS_ADDENDUM = """## major_events 軸另交頂層 events 五組（QC-19）
`validate_evidence.py` 的 strict 檢查讀的是 evidence.json **頂層** `events` 物件，
不是 `coverage.major_events`——這兩個是分開的鍵，只填前者會漏掉後者。

你除了（a）對 `major_events` 這一軸本身作答（寫進 `coverage.major_events`），
**還要**（b）把同一批查證結果拆成下列五組，寫進回傳 JSON 的**頂層** `events` 鍵：
`ma_merger`（併購）／`lawsuit_class_action`（訴訟／集體訴訟）／`clinical_fda`
（臨床／FDA，非藥品器材業務可用 not_applicable）／`product_recall_warning`
（產品召回／警告）／`sec_investigation_restatement`（SEC 調查／重編財報）。

每組欄位規則與 `coverage.<axis>` 相同：found 需 ≥1 條帶 source／as_of／
direction／affects 的 finding；none 需 ≥2 條 queries_run；不適用（如非藥品業務
的 `clinical_fda`）用 `status:"none"`＋queries_run 說明「非藥品/器材業務，已查
證無相關監管動作」，**不得省略該組鍵**。
"""

EVENTS_JSON_SAMPLE = """{
    "ma_merger": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "lawsuit_class_action": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "clinical_fda": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "product_recall_warning": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "sec_investigation_restatement": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""}
  }"""


def _resolve_archetype(cli_archetype, prior):
    """回傳 (archetype, source)。source 只供 log／回報用途。"""
    if cli_archetype:
        return cli_archetype, "cli"
    if isinstance(prior, dict):
        try:
            a = (prior.get("prior_dd") or {}).get("prior_meta", {}).get("archetype")
            if a:
                return a, "prior.prior_dd.prior_meta.archetype"
        except Exception:
            pass
        a = prior.get("archetype_hint")
        if a:
            return a, "prior.archetype_hint"
    return None, None


# ---------------------------------------------------------------------------
# WP7a #3：peers 來源優先順序 --peers → SRC_ARCHIVE_DIR 前份 evidence.json 的
# numbers.peer_financials → docs/id/ID_*.html id-meta related_tickers[] →
# 都沒有則交由呼叫端印錯誤退出（strict 會擋 <2 對手，早停比晚停省）。
# ---------------------------------------------------------------------------

def _peers_from_archive(ticker):
    """從 `SRC_ARCHIVE_DIR/{T}_*/` 找最新一份 evidence.json 的
    `numbers.peer_financials` 鍵，去自身與 `_` 開頭的鍵（如 `_note`）。
    回傳 list 或 None（找不到／無可用鍵）。"""
    if not SRC_ARCHIVE_DIR.exists():
        return None
    candidates = sorted(
        (p for p in SRC_ARCHIVE_DIR.glob("{0}_*".format(ticker)) if p.is_dir()),
        key=lambda p: p.name, reverse=True,
    )
    for cand in candidates:
        ev_path = cand / "{0}.evidence.json".format(cand.name)
        if not ev_path.exists():
            ev_path = cand / "evidence.json"
        if not ev_path.exists():
            continue
        try:
            evidence = _load_json(ev_path)
        except Exception:
            continue
        pf = (evidence.get("numbers") or {}).get("peer_financials") or {}
        peers = [k for k in pf.keys() if k != ticker and not k.startswith("_")]
        if peers:
            return peers
    return None


def _peers_from_id_meta(ticker):
    """`docs/id/ID_*.html` id-meta `related_tickers[]` 含 {T} 的那份，取前 4 檔
    （去自身）。回傳 list 或 None。"""
    if not ID_DIR.exists():
        return None
    try:
        matches = dd_meta_reader.find_ids_for_ticker(ID_DIR, ticker)
    except Exception:
        return None
    if not matches:
        return None
    _, meta = matches[0]
    related = meta.get("related_tickers") or []
    tickers = []
    target = ticker.strip().upper()
    for r in related:
        t = (r.get("ticker") or "").strip().upper()
        if t and t != target and t not in tickers:
            tickers.append(t)
    return tickers[:4] or None


def _resolve_peers(cli_peers, ticker):
    """回傳 (peers_str_or_None, source)。優先序：--peers → archive →
    id-meta → (None, None)（呼叫端負責印錯誤退出）。"""
    if cli_peers:
        return cli_peers, "cli"
    from_archive = _peers_from_archive(ticker)
    if from_archive:
        return ",".join(from_archive), "archive"
    from_id_meta = _peers_from_id_meta(ticker)
    if from_id_meta:
        return ",".join(from_id_meta), "id_meta"
    return None, None


# ---------------------------------------------------------------------------
# 2026-09-06：Stage 0 證據沿用——只沿用仍在時效內的結構軸；數字與事件每次重抓。
# 2026-09-10（WP-B）：coverage 軸沿用改按軸失效，取代單一 30 天窗——軸 id 取自
# `.claude/skills/stock-analyst/references/coverage-axes.md` 的 12 個 common
# 軸（by_archetype 附加軸不在表上，一律退回下方 `default_reuse_days`）：
#   - `major_events`：永遠重抓（QC-19 重大事件，時效最敏感）。
#   - 財報失效組（`end_markets`／`customer_concentration_credit`／
#     `supply_demand_durability`／`channel_business_model_shift`）：快照之後
#     若已出現新一季逐字稿（比對 `transcripts.selected.recent_four_quarters`
#     最後一篇檔名內的日期 vs 快照日），新財報代表這幾軸的數字/敘事可能已
#     過時，一律不沿用；否則沿用上限維持既有 `REUSE_DAYS_DEFAULT`（30 天）。
#   - `capital_markets_pricing`：市場定價/共識落差變動快，縮到 7 天。
#   - 結構組（`competitive_share_entrants`／`customer_second_source`／
#     `regulatory_antitrust`／`reg_tariff_export`／`geo_supply_chain`／
#     `substitute_technology`）：結構性慢變量，放寬到 90 天。
# `--reuse-days`／`REUSE_DAYS_DEFAULT` 改為「表上沒列的軸」的預設上限；
# 傳 0（或 `DD_REPLAY_FROM` 場景）仍是全域關閉——不管在不在表上，一律不沿用
# （沿用既有語意，見 `_axis_reuse_decision`）。
# ---------------------------------------------------------------------------

COVERAGE_REUSE_POLICY = {
    "major_events": {"mode": "never"},
    "end_markets": {"mode": "earnings_gated", "reuse_days": REUSE_DAYS_DEFAULT},
    "customer_concentration_credit": {"mode": "earnings_gated", "reuse_days": REUSE_DAYS_DEFAULT},
    "supply_demand_durability": {"mode": "earnings_gated", "reuse_days": REUSE_DAYS_DEFAULT},
    "channel_business_model_shift": {"mode": "earnings_gated", "reuse_days": REUSE_DAYS_DEFAULT},
    "capital_markets_pricing": {"mode": "fixed_days", "reuse_days": 7},
    "competitive_share_entrants": {"mode": "fixed_days", "reuse_days": 90},
    "customer_second_source": {"mode": "fixed_days", "reuse_days": 90},
    "regulatory_antitrust": {"mode": "fixed_days", "reuse_days": 90},
    "reg_tariff_export": {"mode": "fixed_days", "reuse_days": 90},
    "geo_supply_chain": {"mode": "fixed_days", "reuse_days": 90},
    "substitute_technology": {"mode": "fixed_days", "reuse_days": 90},
}

_TRANSCRIPT_DATE_RE = re.compile(r"(\d{8})\.md$")


def _latest_transcript_date(transcripts_obj):
    """`recent_four_quarters` 依日期由舊到新排列（koyfin 選檔慣例），取最後
    一篇檔名尾端的 8 碼日期；缺檔或格式不符回傳 None。"""
    sel = ((transcripts_obj or {}).get("transcripts") or {}).get("selected") or {}
    recent4 = sel.get("recent_four_quarters") or []
    if not recent4:
        return None
    m = _TRANSCRIPT_DATE_RE.search(Path(recent4[-1]).name)
    return m.group(1) if m else None


def _new_quarter_since_snapshot(snapshot, transcripts_obj):
    """財報失效組專用：快照之後是否已出現更新一季的逐字稿。查無資訊（koyfin
    失敗、無逐字稿）時保守回傳 False，不因為查不到就強制重抓——與既有
    `_prepare_digest_reuse` 的容錯精神一致。"""
    if not snapshot:
        return False
    latest = _latest_transcript_date(transcripts_obj)
    if not latest:
        return False
    return latest > snapshot["source_date"]


def _axis_reuse_decision(axis_id, snapshot, transcripts_obj, default_reuse_days):
    """回傳 `(允許沿用, 原因, 這次用的沿用天數)`，供 `_prepare_coverage_reuse`
    逐軸決定。`default_reuse_days<=0`（即 `--reuse-days 0` 或 replay 場景）
    是全域關閉，不管軸在不在政策表上都不沿用——保留舊行為。"""
    if default_reuse_days <= 0:
        return False, "default_reuse_days<=0，全域關閉沿用", 0
    if axis_id == "major_events":
        return False, "major_events 恆重抓（QC-19）", 0
    policy = COVERAGE_REUSE_POLICY.get(axis_id)
    if policy is None:
        days = default_reuse_days
        if snapshot["age_days"] > days:
            return False, "不在政策表，退回預設 {0} 天，已過期".format(days), days
        return True, "不在政策表，退回預設 {0} 天".format(days), days
    days = policy.get("reuse_days", default_reuse_days)
    mode = policy["mode"]
    if mode == "fixed_days":
        if snapshot["age_days"] > days:
            return False, "固定 {0} 天窗，已過期".format(days), days
        return True, "固定 {0} 天窗".format(days), days
    if mode == "earnings_gated":
        if snapshot["age_days"] > days:
            return False, "財報失效組 {0} 天窗，已過期".format(days), days
        if _new_quarter_since_snapshot(snapshot, transcripts_obj):
            return False, "財報失效組，快照後已出現新一季逐字稿", days
        return True, "財報失效組 {0} 天窗內且無新季報".format(days), days
    return False, "未知政策模式 {0!r}".format(mode), days


# ---------------------------------------------------------------------------
# 2026-09-10（WP-B）：逐字稿摘要改內容雜湊永久快取，不受 30 天沿用窗限制——
# 同一份逐字稿檔一字未變，永遠不重新摘要。key＝逐字稿檔 SHA-256 前 16 碼＋
# `dd_prompts/digest.md.tmpl` 內容 SHA-256 前 8 碼，prompt 改版即自動失效，
# 不需要手動清快取。
# ---------------------------------------------------------------------------

DIGEST_CACHE_DIR = BUILD_DIR / "digest_cache"
DIGEST_TMPL_PATH = PROMPTS_TMPL_DIR / "digest.md.tmpl"


def _digest_cache_key(file_path):
    """檔案讀不到（搬移／刪除）時回傳 None，呼叫端視為 cache miss。"""
    try:
        file_hash = hashlib.sha256(Path(file_path).read_bytes()).hexdigest()[:16]
    except OSError:
        return None
    try:
        tmpl_hash = hashlib.sha256(DIGEST_TMPL_PATH.read_bytes()).hexdigest()[:8]
    except OSError:
        tmpl_hash = "notmpl00"
    return "{0}_{1}".format(file_hash, tmpl_hash)


def _digest_cache_path(file_path):
    key = _digest_cache_key(file_path)
    return (DIGEST_CACHE_DIR / "{0}.json".format(key)) if key else None


def _digest_cache_lookup(file_path):
    """查永久快取；命中回傳 `{items, qa_flags}`（`file` 改指到這次的路徑、
    `reused_from` 標 `"digest_cache"`），未命中回傳 None。"""
    cache_path = _digest_cache_path(file_path)
    if cache_path is None or not cache_path.exists():
        return None
    try:
        cached = _load_json(cache_path)
    except Exception:
        return None
    items = []
    for item in cached.get("items") or []:
        if not isinstance(item, dict):
            continue
        copied = dict(item)
        copied["file"] = str(file_path)
        copied["reused_from"] = "digest_cache"
        items.append(copied)
    qa_flags = []
    for flag in cached.get("qa_flags") or []:
        if not isinstance(flag, dict):
            continue
        copied = dict(flag)
        copied["file"] = str(file_path)
        copied["reused_from"] = "digest_cache"
        qa_flags.append(copied)
    return {"items": items, "qa_flags": qa_flags}


def _digest_cache_store(file_path, items, qa_flags):
    """把某篇逐字稿的 items／qa_flags 依內容雜湊寫進永久快取，先剝掉
    `reused_from`／`age_days`（那是『這次沿用』的暫時標記，不是摘要本身的
    內容）。檔案讀不到時放棄寫入、不報錯（冪等、可重複呼叫）。"""
    cache_path = _digest_cache_path(file_path)
    if cache_path is None:
        return False
    strip_keys = ("reused_from", "age_days")
    clean_items = [
        {k: v for k, v in item.items() if k not in strip_keys}
        for item in items if isinstance(item, dict)
    ]
    clean_flags = [
        {k: v for k, v in flag.items() if k not in strip_keys}
        for flag in qa_flags if isinstance(flag, dict)
    ]
    DIGEST_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(cache_path, {
        "source_file": str(file_path),
        "cached_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "items": clean_items,
        "qa_flags": clean_flags,
    })
    return True


def _iso_date(date):
    """`20260911` → `2026-09-11`（facts.schema 只收帶連字號的形狀）；已帶連字號
    或形狀不符就原樣回傳，不猜。"""
    s = str(date or "").strip()
    return "{0}-{1}-{2}".format(s[:4], s[4:6], s[6:8]) if re.match(r"^\d{8}$", s) else s


def _parse_yyyymmdd(value):
    try:
        return time.strptime(str(value).replace("-", "")[:8], "%Y%m%d")
    except (TypeError, ValueError):
        return None


def _archive_snapshot(ticker, date):
    """找不晚於報告日的最近存查 evidence／digest，供 plan 做機械式沿用。"""
    target = _parse_yyyymmdd(date)
    if target is None or not SRC_ARCHIVE_DIR.exists():
        return None
    target_epoch = time.mktime(target)
    candidates = []
    prefix = "{0}_".format(ticker)
    for archive_dir in SRC_ARCHIVE_DIR.glob(prefix + "*"):
        if not archive_dir.is_dir():
            continue
        suffix = archive_dir.name[len(prefix):]
        m = re.match(r"(\d{8})", suffix)
        if not m:
            continue
        source_date = _parse_yyyymmdd(m.group(1))
        if source_date is None:
            continue
        source_epoch = time.mktime(source_date)
        if source_epoch > target_epoch:
            continue
        evidence_path = archive_dir / "{0}.evidence.json".format(archive_dir.name)
        if not evidence_path.exists():
            evidence_path = archive_dir / "evidence.json"
        if not evidence_path.exists():
            # 2026-09-06：SNOW dryrun 類存查目錄名帶後綴，實檔仍用 T_DATE stem。
            matches = sorted(archive_dir.glob("*.evidence.json"))
            evidence_path = matches[0] if len(matches) == 1 else evidence_path
        if not evidence_path.exists():
            continue
        digest_path = archive_dir / "{0}.transcript_digest.json".format(archive_dir.name)
        if not digest_path.exists():
            digest_path = archive_dir / "digest.json"
        if not digest_path.exists():
            # 2026-09-06：與 evidence 同理，容納目錄後綴和歸檔檔名不同的舊 fixture。
            matches = sorted(archive_dir.glob("*.transcript_digest.json"))
            digest_path = matches[0] if len(matches) == 1 else digest_path
        candidates.append((source_epoch, archive_dir, evidence_path, digest_path, m.group(1)))
    if not candidates:
        return None
    source_epoch, archive_dir, evidence_path, digest_path, source_date = max(candidates, key=lambda x: x[0])
    return {
        "archive_dir": archive_dir,
        "evidence_path": evidence_path,
        "digest_path": digest_path if digest_path.exists() else None,
        "source_date": source_date,
        "age_days": max(0, int((target_epoch - source_epoch) // 86400)),
    }


def _prior_judgment_archive(ticker, date):
    """WP-C：複審 delta 路由用——找不晚於報告日、且**真的跑完判斷段**（存查
    有 `{stem}.judgment.json`）的最近存查包。與 `_archive_snapshot` 共用同一套
    「掃 `{ticker}_{date}` 資料夾、取不晚於目標日期最近一份」找法，但：

    1. 額外要求該筆存查有 judgment.json——只有 evidence 沒有判斷物的存查
       （例如中途失敗的舊 run）不能當複審 prior，否則 `dd_delta.py generate`
       會在開頭直接報錯缺檔。
    2. 目錄名須**嚴格**符合 `{ticker}_{8碼日期}`（不像 `_archive_snapshot`
       只要求前綴是 8 碼數字）——`dd_delta.py` 自己的 `--prior` 目錄名規則
       （`_PRIOR_DIRNAME_RE`）要求整段字串就是這個形狀，`SNOW_20260904_dryrun`
       這類測試 fixture 目錄不符合，直接排除，避免呼叫 `dd_delta.py generate`
       時因目錄名不符而報錯。
    3. 排除「本輪自己」（同 ticker 同 date）——重跑同一天的既有報告時，若
       archive 已存在（例如同日二次執行），不得把它當成自己的 prior（見
       `_do_stage0` 對 replay 自我參照的同款防呆）。

    回傳 `{"archive_dir": Path, "judgment_path": Path, "source_date": str,
    "age_days": int}` 或 None（找不到）。"""
    target = _parse_yyyymmdd(date)
    if target is None or not SRC_ARCHIVE_DIR.exists():
        return None
    target_epoch = time.mktime(target)
    self_name = "{0}_{1}".format(ticker, date)
    candidates = []
    prefix = "{0}_".format(ticker)
    for archive_dir in SRC_ARCHIVE_DIR.glob(prefix + "*"):
        if not archive_dir.is_dir() or archive_dir.name == self_name:
            continue
        suffix = archive_dir.name[len(prefix):]
        m = re.match(r"^(\d{8})$", suffix)
        if not m:
            continue
        source_date = m.group(1)
        source_date_struct = _parse_yyyymmdd(source_date)
        if source_date_struct is None:
            continue
        source_epoch = time.mktime(source_date_struct)
        if source_epoch > target_epoch:
            continue
        judgment_path = archive_dir / "{0}.judgment.json".format(archive_dir.name)
        if not judgment_path.exists():
            continue
        candidates.append((source_epoch, archive_dir, judgment_path, source_date))
    if not candidates:
        return None
    source_epoch, archive_dir, judgment_path, source_date = max(candidates, key=lambda x: x[0])
    return {
        "archive_dir": archive_dir,
        "judgment_path": judgment_path,
        "source_date": source_date,
        "age_days": max(0, int((target_epoch - source_epoch) // 86400)),
    }


def _prepare_coverage_reuse(axis_list, snapshot, default_reuse_days, parts_dir, transcripts_obj=None):
    """把可沿用的結構軸寫成 part，回傳 `(沿用軸 id 清單, decisions)`。
    2026-09-10（WP-B）：逐軸決定改交給 `_axis_reuse_decision`（見
    `COVERAGE_REUSE_POLICY`），不再是單一 30 天窗；`decisions` 記每軸的
    `{reused, reason, reuse_days}`，供 `manifest["coverage_reuse"]` 落地。"""
    if not snapshot:
        return [], {}
    try:
        old = _load_json(snapshot["evidence_path"])
    except Exception:
        return [], {}
    old_coverage = old.get("coverage") or {}
    reused = {}
    decisions = {}
    source_label = snapshot["archive_dir"].name
    for axis in axis_list:
        axis_id = axis.get("id")
        if not axis_id or axis_id not in old_coverage:
            continue
        allow, reason, days_used = _axis_reuse_decision(
            axis_id, snapshot, transcripts_obj, default_reuse_days)
        decisions[axis_id] = {"reused": allow, "reason": reason, "reuse_days": days_used}
        if not allow:
            continue
        # 2026-09-06：舊存查偶有保留已拆分母軸的 pending 骨架；這種不是證據，
        # 不能沿用後又跳過 agent，應留給本次重新收集。
        if not isinstance(old_coverage[axis_id], dict) or old_coverage[axis_id].get("status") == "pending":
            decisions[axis_id]["reused"] = False
            decisions[axis_id]["reason"] += "；舊存查為 pending 骨架非證據"
            continue
        axis_obj = json.loads(json.dumps(old_coverage[axis_id], ensure_ascii=False))
        axis_obj["reused_from"] = source_label
        axis_obj["age_days"] = snapshot["age_days"]
        for finding in axis_obj.get("findings") or []:
            if isinstance(finding, dict):
                finding["reused_from"] = source_label
                finding["age_days"] = snapshot["age_days"]
        reused[axis_id] = axis_obj
    if reused:
        _atomic_write_json(Path(parts_dir) / "reused_coverage.json", {"coverage": reused})
    return list(reused.keys()), decisions


def _prepare_digest_reuse(targets, snapshot, reuse_days, parts_dir):
    """相同逐字稿沿用舊 digest；新出現的檔案才回傳給摘要 agent。2026-09-10
    （WP-B）：先查內容雜湊永久快取（`_digest_cache_lookup`，不受
    `reuse_days` 限制——同一份逐字稿一字未變就永遠沿用，prompt 樣板改版才
    失效）；未命中才退回既有『同 ticker 舊存查 N 天內、依檔名比對』的路徑。
    `DD_REPLAY_FROM` 生效時整個跳過永久快取查詢（比照 `_run_koyfin_step`／
    `cmd_plan` 對 `reuse_days` 的同一慣例）——replay 要如實重放原始 Stage 0
    分工，不能被『上一次 replay 已把摘要寫進永久快取』短路掉 a2_{k} spawn，
    否則同一份 fixture 跑兩次的結果會不一樣，破壞測試可重現性。"""
    replay_mode = bool(os.environ.get("DD_REPLAY_FROM"))
    cache_hits = []
    cache_misses = []
    reused_files = []
    reused_items = []
    reused_flags = []

    if replay_mode:
        cache_misses = list(targets)
    else:
        for target in targets:
            cached = _digest_cache_lookup(target)
            if cached is None:
                cache_misses.append(target)
                continue
            cache_hits.append(target)
            reused_files.append(str(target))
            reused_items.extend(cached["items"])
            reused_flags.extend(cached["qa_flags"])

    if cache_hits:
        print("digest_cache：命中 {0} 篇（內容雜湊一字未變，永久沿用）".format(len(cache_hits)))
    if cache_misses and not replay_mode:
        print("digest_cache：未命中 {0} 篇，退回既有存查沿用規則".format(len(cache_misses)))

    pending = list(cache_misses)
    if (cache_misses and snapshot and reuse_days > 0
            and snapshot["age_days"] <= reuse_days and snapshot.get("digest_path")):
        try:
            old = _load_json(snapshot["digest_path"])
        except Exception:
            old = None
        if old is not None:
            old_items = old.get("items") or []
            old_flags = old.get("qa_flags") or []
            source_label = snapshot["archive_dir"].name
            still_pending = []
            for target in cache_misses:
                target_base = Path(target).name
                matched = [
                    item for item in old_items
                    if isinstance(item, dict) and Path(item.get("file") or "").name == target_base
                ]
                if not matched:
                    still_pending.append(target)
                    continue
                reused_files.append(str(target))
                for item in matched:
                    copied = dict(item)
                    copied["file"] = str(target)
                    copied["reused_from"] = source_label
                    copied["age_days"] = snapshot["age_days"]
                    reused_items.append(copied)
                for flag in old_flags:
                    if isinstance(flag, dict) and Path(flag.get("file") or "").name == target_base:
                        copied_flag = dict(flag)
                        copied_flag["file"] = str(target)
                        copied_flag["reused_from"] = source_label
                        copied_flag["age_days"] = snapshot["age_days"]
                        reused_flags.append(copied_flag)
            pending = still_pending

    if reused_files:
        _atomic_write_json(Path(parts_dir) / "digest_0.json", {
            "source_files": reused_files,
            "items": reused_items,
            "qa_flags": reused_flags,
        })
    return pending, reused_files


# ---------------------------------------------------------------------------
# WP7a #1：Koyfin 步驟改零 LLM——plan 內直接呼叫，不再走 spawn。
# ---------------------------------------------------------------------------

def _koyfin_python():
    if KOYFIN_VENV_PYTHON.exists():
        return str(KOYFIN_VENV_PYTHON)
    return "python3"


def _find_koyfin_drive_folder(drive_ticker):
    """`~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/{T}/` glob 找
    第一個存在的資料夾；找不到回傳 None。"""
    home = Path.home()
    for m in sorted(home.glob(KOYFIN_DRIVE_GLOB + "/" + drive_ticker)):
        if m.is_dir():
            return m
    return None


def _replay_koyfin_transcripts(replay_dir):
    """`--replay-from` 生效時（`DD_REPLAY_FROM` 環境變數）：跳過真的
    Koyfin 網路呼叫，改讀 fixture 既有的 `parts/transcripts.json`，沒有就
    退回 fixture 已合併 evidence.json 內嵌的 `transcripts` 區塊；都沒有則
    回傳空清單＋`koyfin_session_status:"folder_missing"`。"""
    cand = replay_dir / "parts" / "transcripts.json"
    if cand.exists():
        try:
            data = _load_json(cand)
            if isinstance(data, dict) and data.get("transcripts"):
                return data
        except Exception:
            pass
    ev_cand = replay_dir / "{0}.evidence.json".format(replay_dir.name)
    if not ev_cand.exists():
        ev_cand = replay_dir / "evidence.json"
    if ev_cand.exists():
        try:
            evidence = _load_json(ev_cand)
            t = evidence.get("transcripts")
            if t:
                return {"transcripts": t}
        except Exception:
            pass
    return {
        "transcripts": {
            "selected": {"recent_four_quarters": [], "high_signal_optional": []},
            "koyfin_session_status": "folder_missing",
            "must_read_all": [],
            "optional_read_all": [],
        }
    }


def _run_koyfin_step(ticker, date, run_dir, evidence_dest, manifest, drive_ticker=None):
    """WP7a #1：跑增量下載＋逐字稿必讀/可略讀清單，寫 `parts/transcripts.json`
    並立刻 merge 進 evidence.json。失敗（下載逾時／腳本缺席／session 過期）
    只 warn 標記 `koyfin_session_status`，不 abort plan。`--replay-from` 生效
    時（`DD_REPLAY_FROM` 環境變數）改讀 fixture，不打真實網路。"""
    drive_ticker = drive_ticker or ticker
    parts_dir = run_dir / "parts"
    transcripts_out = parts_dir / "transcripts.json"

    replay_from = os.environ.get("DD_REPLAY_FROM")
    if replay_from:
        transcripts_obj = _replay_koyfin_transcripts(Path(replay_from))
        _atomic_write_json(transcripts_out, transcripts_obj)
        if evidence_dest.exists():
            py = _pick_python()
            subprocess.run(
                [py, str(SCRIPTS_DIR / "dd_evidence.py"), "merge",
                 str(evidence_dest), str(transcripts_out)],
                capture_output=True, text=True,
            )
        sel = (transcripts_obj.get("transcripts") or {}).get("selected") or {}
        status = (transcripts_obj.get("transcripts") or {}).get("koyfin_session_status")
        print("koyfin: replay 模式（{0}）session={1} 必讀={2} 可略讀={3}".format(
            replay_from, status,
            len(sel.get("recent_four_quarters") or []),
            len(sel.get("high_signal_optional") or []),
        ))
        manifest["koyfin_session_status"] = status
        return transcripts_obj

    session_status = "ok"

    if not KOYFIN_DOWNLOADER.exists():
        session_status = "downloader_missing"
    else:
        try:
            r = subprocess.run(
                [_koyfin_python(), str(KOYFIN_DOWNLOADER), "--tickers", ticker],
                cwd=str(KOYFIN_DIR), capture_output=True, text=True,
                timeout=KOYFIN_DOWNLOAD_TIMEOUT,
            )
            manifest["steps"].append({"step": "koyfin_download", "returncode": r.returncode})
            if r.returncode != 0:
                session_status = "expired"
                print(
                    "[warn] koyfin_downloader.py 失敗（exit {0}），改用磁碟既有逐字稿：{1}".format(
                        r.returncode, (r.stderr or "").strip()[-300:]),
                    file=sys.stderr,
                )
        except subprocess.TimeoutExpired:
            session_status = "expired"
            print(
                "[warn] koyfin_downloader.py 逾時（{0}s），改用磁碟既有逐字稿".format(
                    KOYFIN_DOWNLOAD_TIMEOUT),
                file=sys.stderr,
            )
        except Exception as e:
            session_status = "expired"
            print("[warn] koyfin_downloader.py 執行失敗：{0}".format(e), file=sys.stderr)

    selected = {"recent_four_quarters": [], "high_signal_optional": []}
    must_read_all = []
    optional_read_all = []
    must_read_tokens_total = None
    mode = None

    if not KOYFIN_SELECTOR.exists():
        if session_status == "ok":
            session_status = "folder_missing"
    else:
        try:
            r = subprocess.run(
                ["python3", str(KOYFIN_SELECTOR), drive_ticker, "--full", "--n", "4"],
                capture_output=True, text=True, timeout=KOYFIN_SELECTOR_TIMEOUT,
            )
            manifest["steps"].append({"step": "koyfin_transcripts_for_dd", "returncode": r.returncode})
            data = None
            for line in reversed((r.stdout or "").splitlines()):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            if data is None:
                if session_status == "ok":
                    session_status = "folder_missing"
                print(
                    "[warn] transcripts_for_dd.py 無 JSON 輸出：{0}".format(
                        (r.stdout or r.stderr or "").strip()[-300:]),
                    file=sys.stderr,
                )
            else:
                must = data.get("must_read") or []
                optional = data.get("optional_read") or []
                must_read_all = must
                optional_read_all = optional
                mode = data.get("mode")
                must_read_tokens_total = data.get("must_read_tokens_total")
                drive_dir = _find_koyfin_drive_folder(drive_ticker)

                def _abs(fname):
                    if drive_dir is None:
                        return None
                    p = drive_dir / fname
                    return str(p) if p.exists() else None

                for fname in must:
                    ap = _abs(fname)
                    if ap:
                        selected["recent_four_quarters"].append(ap)
                    else:
                        print("[warn] 找不到必讀逐字稿檔：{0}".format(fname), file=sys.stderr)
                for fname in optional:
                    ap = _abs(fname)
                    if ap:
                        selected["high_signal_optional"].append(ap)
        except subprocess.TimeoutExpired:
            if session_status == "ok":
                session_status = "folder_missing"
            print("[warn] transcripts_for_dd.py 逾時", file=sys.stderr)
        except Exception as e:
            if session_status == "ok":
                session_status = "folder_missing"
            print("[warn] transcripts_for_dd.py 執行失敗：{0}".format(e), file=sys.stderr)

    transcripts_obj = {
        "transcripts": {
            "selected": selected,
            "koyfin_session_status": session_status,
            "must_read_all": must_read_all,
            "optional_read_all": optional_read_all,
        }
    }
    if mode is not None:
        transcripts_obj["transcripts"]["mode"] = mode
    if must_read_tokens_total is not None:
        transcripts_obj["transcripts"]["must_read_tokens_total"] = must_read_tokens_total

    _atomic_write_json(transcripts_out, transcripts_obj)

    # 立刻 merge 進 evidence.json：evidence.json 需在 plan 結束時就含
    # transcripts.selected，不必等到 stage0 finalize 才看得到（下游 a2_{k}
    # 直接讀這次 plan 算出的 transcripts_obj，這裡的 merge 主要供
    # evidence.json 本身的一致性與後續 finalize 冪等）。
    if evidence_dest.exists():
        py = _pick_python()
        subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_evidence.py"), "merge",
             str(evidence_dest), str(transcripts_out)],
            capture_output=True, text=True,
        )

    n_recent = len(selected["recent_four_quarters"])
    n_hi = len(selected["high_signal_optional"])
    print("koyfin: session={0} 必讀={1} 可略讀={2}".format(session_status, n_recent, n_hi))
    manifest["koyfin_session_status"] = session_status
    return transcripts_obj


def _run_subprocess(cmd, manifest, step_name, cwd=None):
    r = subprocess.run(
        [str(c) for c in cmd], cwd=str(cwd or REPO_ROOT),
        capture_output=True, text=True,
    )
    manifest["steps"].append({
        "step": step_name,
        "cmd": " ".join(str(c) for c in cmd),
        "returncode": r.returncode,
    })
    return r


# ---------------------------------------------------------------------------
# plan
# ---------------------------------------------------------------------------

def cmd_plan(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    run_dir = _run_dir(ticker, date)
    parts_dir = run_dir / "parts"
    prompts_dir = run_dir / "prompts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    py = _pick_python()
    # 2026-09-06：replay 必須重放原始 Stage 0 分工，不能被同日 archive 沿用短路。
    reuse_days = 0 if os.environ.get("DD_REPLAY_FROM") else max(
        0, int(getattr(args, "reuse_days", REUSE_DAYS_DEFAULT))
    )

    manifest = {
        "ticker": ticker,
        "date": date,
        "state": "planning",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "steps": [],
        "agents": [],
    }

    # 1. dd_prior.py（零 LLM，前份 DD／q.py 帳本／canonical ID／逐字稿路徑）
    prior_out = parts_dir / "prior.json"
    r = _run_subprocess(
        [py, SCRIPTS_DIR / "dd_prior.py", ticker, "--date", date, "--out", prior_out],
        manifest, "dd_prior",
    )
    prior = {}
    if r.returncode != 0:
        print("[warn] dd_prior.py 失敗（exit {0}）：{1}".format(
            r.returncode, r.stderr.strip()[-500:]), file=sys.stderr)
    elif prior_out.exists():
        try:
            prior = _load_json(prior_out)
        except Exception as e:
            print("[warn] prior.json 解析失敗：{0}".format(e), file=sys.stderr)

    # 2. archetype 解析
    archetype, src = _resolve_archetype(args.archetype, prior)
    if not archetype:
        archetype = DEFAULT_ARCHETYPE
        src = "default_fallback"
        print(
            "[warn] 未給 --archetype 且 prior.json 無可用 archetype_hint（前份 DD "
            "可能是不含 archetype 欄位的 legacy schema），退回基準 archetype={0!r}"
            "（coverage-axes.md by_archetype 附加軸數=0，即僅 common 軸）".format(archetype),
            file=sys.stderr,
        )
    print("archetype={0!r}（來源：{1}）".format(archetype, src))
    manifest["archetype"] = archetype
    manifest["archetype_source"] = src

    # 3. dd_evidence.py init（既有腳本固定寫到 .dd_build/{T}_{D}.evidence.json，
    #    搬一份進 run 目錄；不改該腳本行為）
    init_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "init", ticker, date,
        "--archetype", archetype,
    ]
    if args.segments:
        init_cmd += ["--segments", args.segments]
    r = _run_subprocess(init_cmd, manifest, "dd_evidence_init")
    if r.returncode != 0:
        print("[error] dd_evidence.py init 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    evidence_flat = BUILD_DIR / "{0}_{1}.evidence.json".format(ticker, date)
    evidence_dest = run_dir / "evidence.json"
    if evidence_flat.exists():
        evidence_dest.write_text(evidence_flat.read_text(encoding="utf-8"), encoding="utf-8")

    # 4. dd_evidence.py axes --json
    axes_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "axes",
        "--archetype", archetype, "--json", "--ticker", ticker,
    ]
    if args.segments:
        axes_cmd += ["--segments", args.segments]
    r = _run_subprocess(axes_cmd, manifest, "dd_evidence_axes")
    if r.returncode != 0:
        print("[error] dd_evidence.py axes 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    try:
        axes = json.loads(r.stdout)
    except Exception as e:
        print("[error] axes --json 輸出不是合法 JSON：{0}".format(e), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    _atomic_write_json(run_dir / "axes.json", axes)

    axis_list = axes if isinstance(axes, list) else []

    # 5b. Koyfin 逐字稿（WP7a #1：零 LLM，plan 內直接跑，立刻 merge 進
    # evidence.json；失敗只 warn，不 abort）。2026-09-10（WP-B）：提前到
    # 這裡（原本排在 numbers_extra 之後）——coverage 沿用改按軸失效後，
    # 財報失效組要拿 `transcripts_obj` 判斷「快照之後是否已出現新一季逐字
    # 稿」，必須在 `_prepare_coverage_reuse` 之前就有這份資料；對
    # evidence.json 的 merge 行為本身不變，只是呼叫時間點提前。
    transcripts_obj = _run_koyfin_step(ticker, date, run_dir, evidence_dest, manifest)

    # 2026-09-06：數字與事件仍每次重抓；只有 coverage 結構軸在時效內沿用。
    # 2026-09-10（WP-B）：沿用政策改按軸失效（COVERAGE_REUSE_POLICY），見該
    # 常數區塊註解；`reuse_days`（來自 `--reuse-days`）現為「表上沒列的軸」
    # 的預設上限，傳 0 仍是全域關閉。
    snapshot = _archive_snapshot(ticker, date)
    reused_axis_ids, coverage_reuse_decisions = _prepare_coverage_reuse(
        axis_list, snapshot, reuse_days, parts_dir, transcripts_obj,
    )
    manifest["evidence_reuse"] = {
        "reuse_days": reuse_days,
        "source": snapshot["archive_dir"].name if snapshot else None,
        "age_days": snapshot["age_days"] if snapshot else None,
        "reused_axis_ids": reused_axis_ids,
    }
    manifest["coverage_reuse"] = {
        "default_reuse_days": reuse_days,
        "source": snapshot["archive_dir"].name if snapshot else None,
        "age_days": snapshot["age_days"] if snapshot else None,
        "reused_axis_ids": reused_axis_ids,
        "decisions": coverage_reuse_decisions,
    }
    if reused_axis_ids:
        print("reuse：沿用 {0} 個結構軸（來源 {1}，{2} 天）".format(
            len(reused_axis_ids), snapshot["archive_dir"].name, snapshot["age_days"]))

    # 5. numbers_extra（--offline 時跳過；失敗只 warn 不 abort）
    if args.offline:
        manifest["steps"].append({"step": "dd_numbers_extra", "skipped": "offline"})
    else:
        peers_str, peers_src = _resolve_peers(args.peers, ticker)
        if not peers_str:
            print(
                "[error] 找不到可用對手清單（--peers 未給、{0}/{1}_*/ 無歷史 "
                "numbers.peer_financials、docs/id/ID_*.html 無含 {1} 的 "
                "related_tickers）：請帶 --peers a,b 手動指定（strict 會擋 <2 "
                "對手，早停比晚停省）".format(SRC_ARCHIVE_DIR, ticker),
                file=sys.stderr,
            )
            _atomic_write_json(run_dir / "manifest.json", manifest)
            return 1
        print("peers={0!r}（來源：{1}）".format(peers_str, peers_src))
        manifest["peers"] = peers_str
        manifest["peers_source"] = peers_src
        numbers_extra_out = parts_dir / "numbers_extra.json"
        ne_cmd = [py, SCRIPTS_DIR / "dd_numbers_extra.py", ticker, date, "--out", numbers_extra_out,
                  "--peers", peers_str]
        if evidence_dest.exists():
            ne_cmd += ["--evidence", evidence_dest]
        r = _run_subprocess(ne_cmd, manifest, "dd_numbers_extra")
        if r.returncode != 0:
            print("[warn] dd_numbers_extra.py 失敗（不 abort）：{0}".format(
                r.stderr.strip()[-500:]), file=sys.stderr)

    # 6. 軸分批：先排除已沿用軸；一般軸預設兩軸一 agent，CLI 仍可調批次大小。
    #    major_events 單獨一批；per_segment 展開軸逐軸獨立，避免一批塞五個
    #    終端市場後撞輪次上限（2026-09-06：FIX／CAMT 實跑事故）。
    #    機械判定用 `resolve_axes()`（dd_evidence.py）保留下來的 `per_segment`
    #    旗標本身——`dict(axis)` 複製時這個鍵原樣留著，不需要另外用 axis id
    #    字串比對猜測（segments 展開時 id 會變成 `end_markets__xxx`，id 相等
    #    判斷法反而抓不到）。
    refresh_axes = [a for a in axis_list if a.get("id") not in set(reused_axis_ids)]
    major = [a for a in refresh_axes if a.get("id") == "major_events"]
    segmented = [a for a in refresh_axes if a.get("id") != "major_events" and _is_segmented_axis(a)]
    rest = [a for a in refresh_axes if a.get("id") != "major_events" and not _is_segmented_axis(a)]
    batches = []
    if major:
        batches.append(major)
    for axis in segmented:
        batches.append([axis])
    step = max(1, args.axes_per_batch)
    for i in range(0, len(rest), step):
        batches.append(rest[i:i + step])

    spawn_list = []
    for k, batch in enumerate(batches, start=1):
        is_major = any(a.get("id") == "major_events" for a in batch)
        is_segmented = (not is_major) and any(_is_segmented_axis(a) for a in batch)
        part_rel = "parts/axes_{0}.json".format(k)
        part_path = run_dir / part_rel
        mapping = {
            "TICKER": ticker,
            "N_AXES": str(len(batch)),
            "AXES_BLOCK": _axis_block(batch),
            "PART_PATH": str(part_path),
            "EVENTS_BLOCK": EVENTS_ADDENDUM if is_major else "",
            "EVENTS_JSON_KEY": (',\n  "events": ' + EVENTS_JSON_SAMPLE) if is_major else "",
        }
        prompt_text = _render_template(PROMPTS_TMPL_DIR / "coverage.md.tmpl", mapping)
        prompt_rel = "prompts/a_{0}.md".format(k)
        (run_dir / prompt_rel).write_text(prompt_text, encoding="utf-8")
        # 2026-09-05：8 太緊（CDNS 六個子 agent 全在第 9 輪被砍），10 是實測
        # 8–13 輪的折衷；2026-09-06：per_segment 展開批（如 end_markets）改用
        # 更寬的 AXES_MAX_TURNS_SEGMENTED（見上方常數註解）。
        batch_max_turns = AXES_MAX_TURNS_SEGMENTED if is_segmented else AXES_MAX_TURNS_DEFAULT
        spawn_list.append({
            "id": "a_{0}".format(k),
            "model": "sonnet",
            "prompt": prompt_rel,
            "out": part_rel,
            "tools": SPAWN_TOOLS_COVERAGE,
            "max_turns": batch_max_turns,
            "budget_cache_read": BUDGET_CACHE_READ_COVERAGE,
        })

    # a1_numbers
    numbers_mapping = {
        "TICKER": ticker,
        "DATE": date,
        "PART_PATH": str(parts_dir / "numbers_collect.json"),
        "NUMBERS_EXTRA_PATH": str(parts_dir / "numbers_extra.json"),
    }
    (prompts_dir / "a1_numbers.md").write_text(
        _render_template(PROMPTS_TMPL_DIR / "numbers.md.tmpl", numbers_mapping), encoding="utf-8")
    spawn_list.append({
        "id": "a1_numbers", "model": "sonnet", "prompt": "prompts/a1_numbers.md",
        "out": "parts/numbers_collect.json", "tools": SPAWN_TOOLS_NUMBERS,
        "max_turns": 15, "budget_cache_read": BUDGET_CACHE_READ_NUMBERS,
    })

    # a2_{k}（WP7d：一篇逐字稿一個 spawn，取代原本一人讀全部的 a2_digest——
    # HPE 實測一人讀三篇 17 輪撞 16 上限、cache_read 2.54M 超 1.5M 預算；
    # 拆開後單篇約 0.5M×3≈1.5M 且可平行）。範圍＝
    # transcripts.selected.recent_four_quarters[:-1]（去掉最後一篇＝最新一
    # 季，留給判斷 agent 親讀）＋ high_signal_optional[]（若有），順序與
    # digest.md.tmpl 既有規則一致。
    sel = ((transcripts_obj or {}).get("transcripts") or {}).get("selected") or {}
    recent4 = sel.get("recent_four_quarters") or []
    optional = sel.get("high_signal_optional") or []
    digest_targets_all = list(recent4[:-1]) + list(optional)
    digest_targets, reused_digest_files = _prepare_digest_reuse(
        digest_targets_all, snapshot, reuse_days, parts_dir,
    )
    manifest["transcript_reuse"] = {
        "source": snapshot["archive_dir"].name if snapshot else None,
        "reused_files": reused_digest_files,
        "refresh_files": [str(p) for p in digest_targets],
    }
    if reused_digest_files:
        print("reuse：沿用 {0} 篇逐字稿摘要，新摘要 {1} 篇".format(
            len(reused_digest_files), len(digest_targets)))

    digest_targets_meta = []
    for k, file_path in enumerate(digest_targets, start=1):
        part_rel = "parts/digest_{0}.json".format(k)
        digest_mapping = {
            "TICKER": ticker,
            "DATE": date,
            "TRANSCRIPT_FILE": str(file_path),
            "PART_PATH": str(run_dir / part_rel),
        }
        prompt_rel = "prompts/a2_{0}.md".format(k)
        (run_dir / prompt_rel).write_text(
            _render_template(PROMPTS_TMPL_DIR / "digest.md.tmpl", digest_mapping), encoding="utf-8")
        spawn_id = "a2_{0}".format(k)
        spawn_list.append({
            "id": spawn_id, "model": "sonnet", "prompt": prompt_rel,
            "out": part_rel, "tools": SPAWN_TOOLS_DIGEST,
            "max_turns": DIGEST_PER_FILE_MAX_TURNS,
            "budget_cache_read": BUDGET_CACHE_READ_DIGEST_PER_FILE,
        })
        digest_targets_meta.append({"id": spawn_id, "file": str(file_path), "out": part_rel})
    _atomic_write_json(run_dir / "digest_targets.json", digest_targets_meta)

    # digest.json 路徑本身零 LLM、plan 當下就確定，直接寫成 part（WP1b
    # _select_parts 固定會挑 parts/digest_path.json 合併進 evidence.json 的
    # transcripts.digest_path，strict 驗證靠它判斷「>1 篇逐字稿時 0e 摘要是否
    # 已接線」；不必等 a2_{k} agent 交稿才知道這個路徑——finalize 前
    # `_merge_digest_parts` 會把 parts/digest_*.json 合併成這個檔）。
    _atomic_write_json(parts_dir / "digest_path.json",
                        {"transcripts": {"digest_path": str(run_dir / "digest.json")}})

    _atomic_write_json(run_dir / "spawn_list.json", spawn_list)

    # WP1d：另存每批軸清單（batch id → axis_ids／is_major），供 --replay-from
    # 重放時比對「這一批該回填哪幾個軸」，不用去反解析 prompt 文字。
    # 2026-09-06：多記 is_segmented，供人工核對／未來重放區分這批是否吃
    # AXES_MAX_TURNS_SEGMENTED（不是覆蓋規則，純分批與輪數記錄）。
    batches_meta = []
    for k, batch in enumerate(batches, start=1):
        b_is_major = any(a.get("id") == "major_events" for a in batch)
        batches_meta.append({
            "id": "a_{0}".format(k),
            "axis_ids": [a.get("id") for a in batch],
            "is_major": b_is_major,
            "is_segmented": (not b_is_major) and any(_is_segmented_axis(a) for a in batch),
        })
    _atomic_write_json(run_dir / "batches.json", batches_meta)

    manifest["state"] = "planned"
    manifest["agents"] = [s["id"] for s in spawn_list]
    _atomic_write_json(run_dir / "manifest.json", manifest)

    print("\n{0:14s} {1:8s} {2:10s} {3}".format("id", "model", "max_turns", "out"))
    for s in spawn_list:
        print("{0:14s} {1:8s} {2:<10d} {3}".format(s["id"], s["model"], s["max_turns"], s["out"]))
    print("\n共 {0} 個 spawn，寫入 {1}".format(len(spawn_list), run_dir))
    return 0


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

_TOP_LEVEL_FILES = [
    "evidence.json", "axes.json", "spawn_list.json", "digest.json",
    "judgment.json", "scenario.json", "scenario_meta.json",
]
_SUBDIRS = ["parts", "prompts", "agents", "tables", "prose", "bundles"]


def cmd_status(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        print("[error] 找不到 run 目錄或 manifest：{0}".format(manifest_path), file=sys.stderr)
        return 1
    manifest = _load_json(manifest_path)
    print("ticker={0} date={1} state={2} created={3}".format(
        manifest.get("ticker"), manifest.get("date"), manifest.get("state"), manifest.get("created")))
    print("archetype={0!r}（來源：{1}）".format(manifest.get("archetype"), manifest.get("archetype_source")))
    print("steps={0} agents={1}".format(len(manifest.get("steps", [])), len(manifest.get("agents", []))))
    # 2026-09-07：status 明列 finish／延後同步狀態，讓中斷後的 pending 可見。
    finish_state = manifest.get("finish") or {}
    site_sync = finish_state.get("site_sync") or {}
    if finish_state or site_sync:
        print("finish={0} site_sync={1} deferred={2}".format(
            finish_state.get("state", "—"), site_sync.get("state", "—"),
            site_sync.get("deferred", False)))
        # 2026-09-07（P1-5）：validated／archived／commit sha／pushed sha 一併
        # 印出，讓「已產出」與「已發布」在 status 一行內就能分辨，不必手翻
        # manifest.json 原始欄位。
        print("validated={0} archived={1} commit_sha={2} pushed_sha={3}".format(
            finish_state.get("validated", False), finish_state.get("archived", False),
            (finish_state.get("report_commit_sha") or "—")[:12],
            (finish_state.get("report_pushed_sha") or "—")[:12],
        ))

    print()
    for name in _TOP_LEVEL_FILES:
        p = run_dir / name
        if p.exists():
            print("[ok      ] {0:24s} {1:>10d} bytes".format(name, p.stat().st_size))
        else:
            print("[missing ] {0:24s} —".format(name))

    for sub in _SUBDIRS:
        d = run_dir / sub
        if d.exists():
            files = sorted(f for f in d.iterdir() if f.is_file())
            print("\n{0}/ （{1} 檔）".format(sub, len(files)))
            for f in files:
                print("  {0:30s} {1:>10d} bytes".format(f.name, f.stat().st_size))
        else:
            print("\n{0}/  missing".format(sub))
    return 0


# ---------------------------------------------------------------------------
# WP1d small helpers：時間戳、format_map 安全渲染、replay marker、log 印格式
# ---------------------------------------------------------------------------

def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


class _SafeFormatDict(dict):
    """`str.format_map` 用：缺的變數給空字串，不 KeyError。

    judge.md.tmpl／gate.md.tmpl／judge_patch.md.tmpl 用單括號 `{var}`（其他
    大括號已在檔內寫成 `{{ }}`），依協調者指示改走 format_map，不再用
    `plan` 那組舊模板的 `{{VAR}}` 字面取代法。
    """

    def __missing__(self, key):
        return ""


def _render_format_template(tmpl_path, mapping):
    text = Path(tmpl_path).read_text(encoding="utf-8")
    return text.format_map(_SafeFormatDict(mapping))


BUNDLE_SEPARATOR = "\n\n===== BUNDLE =====\n\n"


def _write_inline_prompt(prompt_path, extra_content_path):
    """WP7b #1：judge／gate／patch 三種 prompt 渲染完模板後，把 bundle
    （或修補時的 judgment.json 全文）整段接在 prompt 之後（分隔行
    `===== BUNDLE =====`），寫成一個新的 `*_inline.md` 檔給 `dd_headless.spawn`
    當真正的 prompt（經 stdin 餵給 `claude -p`，無長度上限）。模板本身的
    「讀」段已改為「不要 Read 任何檔」，原本較短的 `prompt_path` 仍保留
    （供人工核對渲染結果），不再是實際餵給 agent 的內容。

    理由：Fable 判斷 agent 曾為了讀 240KB 的 judge bundle 花到撞 8 輪
    上限（見 notes/site-internal/dd/_wp_spec_v17_batch5_20260905.md
    WP7b #1 的 AVGO 實測記錄）。
    """
    prompt_path = Path(prompt_path)
    extra_path = Path(extra_content_path)
    extra_text = extra_path.read_text(encoding="utf-8") if extra_path.exists() else ""
    combined = prompt_path.read_text(encoding="utf-8") + BUNDLE_SEPARATOR + extra_text
    inline_path = prompt_path.with_name(prompt_path.stem + "_inline" + prompt_path.suffix)
    inline_path.write_text(combined, encoding="utf-8")
    return inline_path


def _print_step_status(step, actual, target, status):
    print("{0}／實測={1}／目標={2}／{3}".format(step, actual, target, status))


def _print_resume_hint(ticker, date, stage):
    print(
        "中斷於 {0}。可用 --resume 從此處接續：\n"
        "  python3 scripts/ddreport.py run {1} --date {2} --resume".format(
            stage, ticker, date
        )
    )


def _load_json_or(path, default):
    path = Path(path)
    if not path.exists():
        return default
    try:
        return _load_json(path)
    except Exception:
        return default


REPLAY_FAKE_CLAUDE = SCRIPTS_DIR / "tests" / "fake_claude.py"


def _ensure_replay_env(replay_from):
    """`--replay-from DIR` 啟用時：設 `DD_CLAUDE_BIN` 指向假 binary、
    `DD_REPLAY_FROM` 指向 fixture 目錄（皆轉絕對路徑，因 spawn 可能以
    run_dir 為 cwd 呼叫子行程）。回傳絕對化後的 Path，或 None。"""
    if not replay_from:
        return None
    replay_dir = Path(replay_from).resolve()
    os.environ["DD_CLAUDE_BIN"] = str(REPLAY_FAKE_CLAUDE.resolve())
    os.environ["DD_REPLAY_FROM"] = str(replay_dir)
    return replay_dir


def _append_replay_marker(prompt_path, obj):
    """把 `<!-- DD_REPLAY {json} -->` 附在 prompt 檔尾——`fake_claude.py`
    的 replay 模式只認這個 marker（不去猜測散文措辭），marker 只在
    `--replay-from` 生效時附加，正式跑（真 claude）不受影響。"""
    prompt_path = Path(prompt_path)
    if not prompt_path.exists():
        return
    text = prompt_path.read_text(encoding="utf-8")
    marker = "\n\n<!-- DD_REPLAY {0} -->\n".format(json.dumps(obj, ensure_ascii=False))
    prompt_path.write_text(text + marker, encoding="utf-8")


def _apply_replay_markers_stage0(run_dir, replay_dir):
    """Stage 0 三類 spawn（覆蓋軸批次／數字／逐字稿摘要）prompt 逐一附
    replay marker。批次的軸清單讀 `batches.json`（`plan` 時已寫出）；摘要的
    逐篇清單讀 `digest_targets.json`（WP7d：一篇一個 spawn，`plan` 時已寫
    出）。Koyfin 已於 WP7a 改零 LLM，plan 內直接跑，不再是 spawn，不需要
    marker。"""
    if not replay_dir:
        return
    prompts_dir = run_dir / "prompts"
    batches = _load_json_or(run_dir / "batches.json", [])
    for b in batches:
        bid = b["id"]
        k = bid.split("_", 1)[1]
        out_path = run_dir / "parts" / "axes_{0}.json".format(k)
        _append_replay_marker(prompts_dir / "{0}.md".format(bid), {
            "kind": "coverage", "axes": b.get("axis_ids") or [],
            "major": bool(b.get("is_major")), "out": str(out_path),
        })
    _append_replay_marker(prompts_dir / "a1_numbers.md", {
        "kind": "numbers", "out": str(run_dir / "parts" / "numbers_collect.json"),
    })
    digest_targets = _load_json_or(run_dir / "digest_targets.json", [])
    for dt in digest_targets:
        out_path = run_dir / dt["out"]
        _append_replay_marker(prompts_dir / "{0}.md".format(dt["id"]), {
            "kind": "digest", "file": dt.get("file"), "out": str(out_path),
        })


# ---------------------------------------------------------------------------
# WP1d stage0：plan（未 plan 時，Koyfin 於 plan 內零 LLM 完成）→ spawn_many
# 覆蓋/數字/摘要 → finalize（WP7a #4：resume 時只重派需要的部分）
# ---------------------------------------------------------------------------

_DIGEST_PART_RE = re.compile(r"^digest_(\d+)\.json$")


def _merge_digest_parts(run_dir):
    """WP7d：零 LLM 合併 `parts/digest_{k}.json`（每篇逐字稿一個 spawn 交回
    的片段，形狀同 `digest.json`：`{source_files, items, qa_flags}`）成單一
    `digest.json`（形狀不變，`validate_digest.py` 直接吃）。依檔名數字序合
    併，`source_files` 依序去重、`items`／`qa_flags` 直接接尾。沒有任何
    `digest_*.json`（例如 Koyfin 找不到逐字稿）時寫出空殼，維持既有
    fallback 語意。

    2026-09-10（WP-B）：合併完成後，把每篇來源逐字稿的 items／qa_flags 依
    `file` 欄位拆開，回寫進 `_digest_cache_store`（內容雜湊永久快取）——
    不論這篇本次是新摘要還是沿用來的，都重新落一次（冪等，供下次任何
    ticker 遇到同一份逐字稿直接命中，見 `_prepare_digest_reuse`）。逐字稿
    檔案本身若已不在磁碟（搬移／刪除）會被 `_digest_cache_store` 靜默略過，
    不影響 digest.json 本身的合併結果。"""
    parts_dir = Path(run_dir) / "parts"
    digest_files = []
    if parts_dir.exists():
        for f in parts_dir.iterdir():
            m = _DIGEST_PART_RE.match(f.name)
            if m:
                digest_files.append((int(m.group(1)), f))
    digest_files.sort(key=lambda t: t[0])

    source_files, items, qa_flags = [], [], []
    seen = set()
    for _, f in digest_files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for sf in d.get("source_files") or []:
            if sf not in seen:
                seen.add(sf)
                source_files.append(sf)
        items.extend(d.get("items") or [])
        qa_flags.extend(d.get("qa_flags") or [])

    merged = {"source_files": source_files, "items": items, "qa_flags": qa_flags}
    _atomic_write_json(Path(run_dir) / "digest.json", merged)

    for sf in source_files:
        file_items = [it for it in items if isinstance(it, dict) and it.get("file") == sf]
        file_flags = [fl for fl in qa_flags if isinstance(fl, dict) and fl.get("file") == sf]
        if file_items or file_flags:
            _digest_cache_store(sf, file_items, file_flags)

    return merged


def _finalize_run_dir(run_dir):
    """跑 `dd_evidence.py finalize --run-dir DIR`，回傳
    (returncode, 原始輸出全文, 需重派的 part 檔名 set)。finalize 前先零
    LLM 合併 `parts/digest_{k}.json` 成 `digest.json`（WP7d）——digest 不在
    `dd_evidence.py` 的 merge 範圍內（那是 evidence.json 的 merge），故在
    這裡自己補做，確保每次 finalize（含 resume／retry）看到的 digest.json
    都是最新片段的合併結果。"""
    _merge_digest_parts(run_dir)
    py = _pick_python()
    r = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_evidence.py"), "finalize", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    needs = set()
    in_block = False
    for line in (r.stdout or "").splitlines():
        if line.startswith("需重派"):
            in_block = True
            continue
        if in_block:
            m = re.match(r"\s*✗\s+(\S+)", line)
            if m:
                needs.add(m.group(1))
            elif not line.startswith("      "):
                in_block = False
    return r.returncode, out, needs


def _spec_out_basename(spec):
    return Path(spec.get("out", "")).name


def _respawn_candidates(spawn_list, needs, run_dir):
    """回傳需要重派的 spec 清單——依「需重派」清單（part 檔存在但驗證內容
    不合格）**或**該 spec 對應的 part 檔完全不存在（子 agent 撞輪次上限、
    從未 Write 出產物）。resume 與首跑共用這支，修補「首跑 finalize FAIL
    但缺件檔案根本沒被寫出、`_finalize_run_dir` 的『需重派』清單只涵蓋
    『檔案在但內容不合格』一類、不含『整批沒交出來』一類」這個缺洞——
    WP8 待補 #4（STRL 首跑 a_2／a_5 撞輪次上限 → finalize FAIL 直接停、
    retries=0；根因即此）。"""
    return [
        s for s in spawn_list
        if _spec_out_basename(s) in needs or not (run_dir / s.get("out", "")).exists()
    ]


def _spawn_spec_for(spec, run_dir):
    """把 `spawn_list.json` 一筆 spec 轉成餵給 `dd_headless.spawn_many` 的呼叫
    參數。**刻意不把 `spec["out"]`（子 agent 應該用 Write 工具寫入的實際產物
    路徑，如 `parts/axes_1.json`）當作 `dd_headless.spawn` 的 `out_json`**——
    `out_json` 存的是 `claude -p` 子行程的原始回傳 JSON（`result`／usage 等
    metadata），跟子 agent 用 Write 工具寫出的工作產物是兩個不同的檔；兩者
    共用同一路徑會讓 dd_headless 收工時把原始回傳包整個蓋掉子 agent 真正寫
    的內容（replay 模式下觀測到此問題）。原始回傳改存 `agents/{id}.json`
    供除錯用，`spec["out"]` 只作為「finalize 後去哪裡找這批產物」的紀錄，
    不動它的語意。"""
    s = dict(spec)
    s["run_dir"] = str(run_dir)
    s["out"] = str(Path(run_dir) / "agents" / "{0}.json".format(spec.get("id", "spawn")))
    return s


def _fresh_stage_preserving_prior(manifest, stage_name):
    """2026-09-06：`_do_stage0`／`_do_judge`／`_do_gate` 重建某段 `stage` 字典時
    共用——若 manifest 既有同名 stage 且帶 `agent_usage`（如 `--resume` 前一輪
    已燒過 token 但沒 PASS），把它（連同它可能已帶的 `agent_usage_prior`，
    支援多次 resume 累積）搬進新 stage 的 `agent_usage_prior`，新 stage 自己
    的 `agent_usage` 從空開始收這一輪。不這樣做的話，`_do_stage0`／`_do_judge`
    原本無條件蓋掉舊 stage 字典，`--resume` 後 finish 算的『全帳 X.XM』只計
    這次重跑燒的量，漏記前面失敗但已花掉的 token（實例：FIX 早上 stage0
    失敗三次共燒 8M，resume 後全帳完全沒算進這段）。回傳全新的 RUNNING
    狀態 stage 字典，只有真的有東西可搬時才帶 `agent_usage_prior` 鍵。"""
    old = (manifest.get("stages") or {}).get(stage_name) or {}
    prior = list(old.get("agent_usage_prior") or []) + list(old.get("agent_usage") or [])
    stage = {"state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False}
    if prior:
        stage["agent_usage_prior"] = prior
    return stage


def _do_facts(ticker, date, run_dir, replay_dir, stage):
    """WP-H2-1（2026-09-11）：六問事實表。兩步——

    1. `dd_facts.py extract`（零 LLM）從定稿 evidence／digest 抽機械可抽的部分，
       落 `facts_draft.json`，抽不到的題留 `needs_sonnet` ＋一句缺什麼。
    2. sonnet 事實表 agent 讀初稿＋證據包＋摘要＋最新一季逐字稿全文，只補
       `needs_sonnet` 的題與承重條目的原文片段，寫 `facts.json`；跑完
       `dd_facts.py check`。

    **降級而非阻斷**：agent 沒寫出檔、或寫出的檔過不了 check 時，退回機械初稿
    當 `facts.json`（初稿本身合格，且六題都帶 `needs_sonnet: true` 明說「這題沒
    補齊」）並把失敗原文記進 manifest。理由：初稿是誠實的不完整，不是編造；讓
    判斷層看得到「這題事實未補齊」比讓整條 run 停在一次 agent 抖動上好。
    `--replay-from` 一律只用機械初稿（回溯重放不打 API，fixture 也沒有事實表
    的 replay marker）。

    回傳一個 dict 記在 `stages.stage0.facts`：`ok`／`fallback`／`check_tail`。"""
    py = _pick_python()
    draft_path = run_dir / "facts_draft.json"
    facts_path = run_dir / "facts.json"
    out = {"ok": False, "fallback": False, "draft": str(draft_path), "out": str(facts_path)}

    r_ex = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_facts.py"), "extract", "--run-dir", str(run_dir),
         "--date", _iso_date(date), "--out", str(draft_path)],
        capture_output=True, text=True,
    )
    out["extract_tail"] = (r_ex.stdout + r_ex.stderr).strip()[-800:]
    if r_ex.returncode != 0 or not draft_path.exists():
        out["note"] = "dd_facts.py extract 失敗，無事實表可用"
        _print_step_status("stage0.facts", "extract_rc={0}".format(r_ex.returncode), "PASS", "FAIL")
        return out

    if replay_dir:
        out["fallback"] = True
        out["note"] = "replay：只用機械初稿，不派事實表 agent"
    else:
        prompt_path = run_dir / "prompts" / "a_facts.md"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        evidence = _load_json_or(run_dir / "evidence.json", {})
        transcript = dd_bundle._find_transcript_path(
            ticker,
            (((evidence.get("transcripts") or {}).get("selected") or {})
             .get("recent_four_quarters") or [None])[-1],
        )
        prompt_path.write_text(_render_template(PROMPTS_TMPL_DIR / "facts.md.tmpl", {
            "TICKER": ticker, "DATE": date,
            "EVIDENCE_PATH": str(run_dir / "evidence.json"),
            "DIGEST_PATH": str(run_dir / "digest.json"),
            "FACTS_DRAFT_PATH": str(draft_path),
            "FACTS_OUT_PATH": str(facts_path),
            "TRANSCRIPT_PATH": str(transcript) if transcript else "（證據包未帶最新一季逐字稿，略過）",
            "TRANSCRIPT_BASENAME": transcript.name if transcript else "",
            "MAX_TURNS": str(FACTS_MAX_TURNS),
        }), encoding="utf-8")
        r_spawn = dd_headless.spawn(
            prompt_path=prompt_path, model="sonnet", allowed_tools=SPAWN_TOOLS_FACTS,
            max_turns=FACTS_MAX_TURNS, budget_cache_read=BUDGET_CACHE_READ_FACTS,
            out_json=run_dir / "agents" / "a_facts.json", cwd=run_dir,
        )
        stage.setdefault("agent_usage", []).append(r_spawn)

    if facts_path.exists():
        r_ck = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_facts.py"), "check", str(facts_path), "--report"],
            capture_output=True, text=True,
        )
        check_out = (r_ck.stdout + r_ck.stderr).strip()
        out["check_tail"] = check_out[-1500:]
        if re.search(r"^\[PASS\]", check_out, re.M):
            out["ok"] = True
            _print_step_status("stage0.facts", "check PASS", "PASS", "PASS")
            return out
        out["note"] = "事實表 agent 的產物未通過 dd_facts check，退回機械初稿"
    else:
        out["note"] = out.get("note") or "事實表 agent 未寫出 facts.json，退回機械初稿"

    shutil.copyfile(draft_path, facts_path)
    out["fallback"] = True
    # WP-H2-3（2026-09-11，Codex 裁定 1）：**失手退回初稿 ≠ 完整輸入**。初稿是
    # 誠實的不完整（六題都帶 `needs_sonnet`），但判斷層拿它當唯一數字來源會在
    # 「這題沒補齊」上做判斷而不自知——所以這裡多記一筆 `incomplete`，由
    # `_do_stage0` 升到 manifest 頂層 `facts_incomplete`，判斷段見到就停，交指揮者。
    # **`--replay-from` 例外**：回溯重放本來就刻意只用機械初稿（不打 API、fixture
    # 也沒有事實表的 replay marker），那是設計不是失手，不標 incomplete。
    out["incomplete"] = not bool(replay_dir)
    r_ck2 = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_facts.py"), "check", str(facts_path), "--report"],
        capture_output=True, text=True,
    )
    check_out2 = (r_ck2.stdout + r_ck2.stderr).strip()
    out["check_tail"] = check_out2[-1500:]
    out["ok"] = bool(re.search(r"^\[PASS\]", check_out2, re.M))
    _print_step_status("stage0.facts", "fallback＝機械初稿（{0}）".format(out.get("note")),
                       "PASS", "PASS" if out["ok"] else "FAIL")
    return out


def _do_stage0(ticker, date, plan_kwargs, replay_dir, accept_over_budget, manifest):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = _fresh_stage_preserving_prior(manifest, "stage0")
    manifest.setdefault("stages", {})["stage0"] = stage
    manifest["state"] = "stage0_running"
    _atomic_write_json(manifest_path, manifest)

    if not (run_dir / "spawn_list.json").exists():
        plan_args = argparse.Namespace(
            ticker=ticker, date=date,
            archetype=plan_kwargs.get("archetype"),
            peers=plan_kwargs.get("peers"),
            segments=plan_kwargs.get("segments"),
            axes_per_batch=plan_kwargs.get("axes_per_batch") or AXES_PER_BATCH_DEFAULT,
            offline=plan_kwargs.get("offline", False),
            # 2026-09-06：replay 強制 0，正式 run 才套 CLI 的沿用天數。
            reuse_days=0 if replay_dir else plan_kwargs.get("reuse_days", REUSE_DAYS_DEFAULT),
        )
        rc = cmd_plan(plan_args)
        if rc != 0:
            manifest = _load_json(manifest_path)
            stage = manifest.setdefault("stages", {}).setdefault("stage0", stage)
            stage["state"] = "FAIL"
            stage["ended"] = _now()
            stage["note"] = "plan 失敗"
            _atomic_write_json(manifest_path, manifest)
            _print_step_status("stage0", "plan_rc={0}".format(rc), "PASS", "FAIL")
            return 1
        manifest = _load_json(manifest_path)
        manifest.setdefault("stages", {})["stage0"] = stage

    # offline + replay：零 LLM 的 dd_numbers_extra.py 在 plan 時被 --offline 跳過，
    # 但 finalize 仍需要這份歷史快照才能 strict 通過——from fixture 直接補進
    # parts/（這是刻意的 replay-only 補洞，不影響非 replay 的正常 plan 行為）。
    if replay_dir and plan_kwargs.get("offline"):
        src = replay_dir / "parts" / "numbers_extra.json"
        dst = run_dir / "parts" / "numbers_extra.json"
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    if replay_dir:
        _apply_replay_markers_stage0(run_dir, replay_dir)
        # 回溯重放時，「今天」常常等於 fixture 原本的報告日期（甚至該日期
        # 已有上站報告），這時 plan 剛跑的**即時** dd_prior.py 會把「同一天
        # 已上站的那份報告自己」誤當成 prior（自我參照），judge check 的
        # QC-49 漂移歸因因此對不上。改用 fixture 當時真正捕捉到的
        # parts/prior.json（產這份報告當下、報告本身還不存在時的歷史快照）
        # 才是對的 replay 語意——這只在 --replay-from 生效，不影響正常路徑。
        fixture_prior = replay_dir / "parts" / "prior.json"
        if fixture_prior.exists():
            (run_dir / "parts" / "prior.json").write_text(
                fixture_prior.read_text(encoding="utf-8"), encoding="utf-8")

    spawn_list = _load_json_or(run_dir / "spawn_list.json", [])

    # WP7a #4：重派真的重派——resume 情境（此 run_dir 已有部分 part 檔，代表
    # 先前跑過一輪 stage0 但未整體 PASS）不盲目重派全部：先問一次 finalize
    # 拿「需重派」清單，只重派清單內＋完全沒產出過的 spec；全新 run（尚無
    # 任何本批產物）才維持「全部 spawn」。`--resume` 進到 stage0 時走的是
    # 同一個 `_do_stage0` 入口，故也吃到這條路徑，不是只重跑 finalize。
    has_existing_output = any(
        (run_dir / s.get("out", "")).exists() for s in spawn_list
    )
    if has_existing_output:
        _, _, needs0 = _finalize_run_dir(run_dir)
        to_spawn = _respawn_candidates(spawn_list, needs0, run_dir)
        if to_spawn:
            print("[stage0] resume：只重派 {0}".format(
                ", ".join(s["id"] for s in to_spawn)))
    else:
        to_spawn = spawn_list

    other_specs = [_spawn_spec_for(s, run_dir) for s in to_spawn]
    if other_specs:
        stage["agent_usage"].extend(dd_headless.spawn_many(other_specs, max_parallel=STAGE0_MAX_PARALLEL))

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget

    rc, out_text, needs = _finalize_run_dir(run_dir)
    retries = 0
    while rc != 0 and retries < 2:
        retry_candidates = _respawn_candidates(spawn_list, needs, run_dir)
        if not retry_candidates:
            break
        retry_specs = [_spawn_spec_for(s, run_dir) for s in retry_candidates]
        stage["agent_usage"].extend(dd_headless.spawn_many(retry_specs, max_parallel=STAGE0_MAX_PARALLEL))
        rc, out_text, needs = _finalize_run_dir(run_dir)
        retries += 1
    stage["finalize_retries"] = retries
    stage["finalize_tail"] = out_text[-3000:]

    # WP-H2-1（2026-09-11）：Stage 0 末尾的事實表——證據 finalize 過了才做
    # （事實要從定稿的 evidence／digest 抽，不然抽到半成品）。刻意**不新增
    # STAGE_ORDER 段**：新增段會動到 `--resume` 的索引語意與既有 manifest 的
    # 相容判斷，而事實表在語意上就是 Stage 0 的最後一件收集工作。
    if rc == 0:
        stage["facts"] = _do_facts(ticker, date, run_dir, replay_dir, stage)
        if not stage["facts"].get("ok"):
            rc = 1
        # WP-H2-3：事實表未補齊時在 manifest 頂層留一面旗，讓判斷段（可能是另一
        # 個 process、另一天 `--resume`）看得到，不必再去翻 stage 結構。
        manifest["facts_incomplete"] = bool(stage["facts"].get("incomplete"))
        over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
        stage["over_budget"] = over_budget

    ok = (rc == 0) and (over_budget is False or accept_over_budget)
    stage["state"] = "PASS" if ok else ("FAIL" if rc != 0 else "OVER_BUDGET")
    stage["ended"] = _now()
    manifest["stages"]["stage0"] = stage
    manifest["state"] = "stage0_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "stage0",
        "finalize_rc={0} retries={1} over_budget={2}".format(rc, retries, over_budget),
        "finalize PASS",
        stage["state"],
    )
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "stage0")
    return 0 if stage["state"] == "PASS" else 1


# ---------------------------------------------------------------------------
# WP1d judge：bundle → prompt(judge.md.tmpl) → spawn → judge check → 修一輪
# ---------------------------------------------------------------------------

# v19 的 decision_out：只把矩陣機械欄與 requires_critic 併回原檔。
# `rearm_trigger`／`exec_line` 在 v19 住 `counter_evidence.action_conditions`
# 一處（投影時才進 decision_out），併回來會讓同一件事兩邊都有，validate 會擋。
_V19_DECISION_OUT_KEYS = ("verdict", "role", "row_hit", "pacing", "holding_cap",
                          "audit_rows", "requires_critic")


def _judge_check_v19(run_dir, judgment_path, evidence_path, tables_dir, py):
    """WP-H2-1（2026-09-11）：v19 判斷檔的 judge check。

    `dd_decision.py`（依派工單不動）只讀 `decision_inputs`，而 v19 原檔只有
    judge-owned 九欄——所以這條路徑是：**格式正規化 → `dd_project view` 產投影
    檔 → `dd_project scenario` 產 dd_scenario 的輸入檔 → `dd_scenario` →
    `dd_decision run`（對投影檔）→ 把 `decision_out` 併回原檔 → validate 原檔**。
    validate 自己會再投影一次（單一轉接），所以驗的仍是同一份視圖。

    正規化只修形狀（路徑／欄名映射／單物件包陣列），不補任何判斷值——見
    `dd_project.normalize` 的界線註解。"""
    parts, ok = [], True

    raw = _load_json(judgment_path)
    normalized, changes = dd_project.normalize(raw, judgment_path)
    if changes:
        _atomic_write_json(judgment_path, normalized)
        parts.append("[dd_project normalize] 修了 {0} 項形狀：\n{1}".format(
            len(changes), "\n".join("  · " + c for c in changes)))

    scenario_path = run_dir / "scenario.json"
    r0 = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_project.py"), "scenario", str(judgment_path),
         "--out", str(scenario_path)],
        capture_output=True, text=True,
    )
    parts.append("[dd_project.py scenario] rc={0}\n{1}".format(
        r0.returncode, (r0.stdout + r0.stderr).strip()))
    ok = ok and (r0.returncode == 0)

    view_path = run_dir / "judgment_view.json"
    r1 = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_project.py"), "view", str(judgment_path),
         "--out", str(view_path)],
        capture_output=True, text=True,
    )
    parts.append("[dd_project.py view] rc={0}\n{1}".format(
        r1.returncode, (r1.stdout + r1.stderr).strip()))
    ok = ok and (r1.returncode == 0)

    if scenario_path.exists():
        r2 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_scenario.py"), str(scenario_path),
             "--html", str(tables_dir / "e11.html"),
             "--meta", str(run_dir / "scenario_meta.json")],
            capture_output=True, text=True,
        )
        parts.append("[dd_scenario.py] rc={0}\n{1}".format(
            r2.returncode, (r2.stdout + r2.stderr).strip()))
        ok = ok and (r2.returncode == 0)

    if view_path.exists():
        r3 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_decision.py"), "run", str(view_path),
             "--html", str(tables_dir / "audit.html"), "--json", str(view_path)],
            capture_output=True, text=True,
        )
        parts.append("[dd_decision.py run] rc={0}\n{1}".format(
            r3.returncode, (r3.stdout + r3.stderr).strip()))
        ok = ok and (r3.returncode == 0)
        if r3.returncode == 0:
            view = _load_json(view_path)
            merged = dict(_load_json(judgment_path).get("decision_out") or {})
            for k in _V19_DECISION_OUT_KEYS:
                if k in (view.get("decision_out") or {}):
                    merged[k] = (view["decision_out"])[k]
            cur = _load_json(judgment_path)
            cur["decision_out"] = merged
            _atomic_write_json(judgment_path, cur)

    vj_cmd = [py, str(SCRIPTS_DIR / "validate_judgment.py"), str(judgment_path),
              "--evidence", str(evidence_path), "--fix", "--report"]
    if os.environ.get("DD_J1_WARN") == "1":
        vj_cmd.append("--j1-warn")
    r4 = subprocess.run(vj_cmd, capture_output=True, text=True)
    vj_out = (r4.stdout + r4.stderr).strip()
    parts.append("[validate_judgment.py] rc={0}\n{1}".format(r4.returncode, vj_out))
    if re.search(r"^\[FAIL\]", vj_out, re.M):
        ok = False
    elif not re.search(r"^\[PASS\]", vj_out, re.M):
        ok = False
    return ok, parts


def _judge_check(ticker, date):
    """`ddreport.py judge check TICKER DATE`：依序跑 dd_scenario.py／
    dd_decision.py run／validate_judgment.py --fix --report，回傳
    (ok, report_text)。`validate_judgment.py --report` 恆 exit 0，PASS/FAIL
    要從輸出的 `[PASS]`／`[FAIL]` 首行判斷，不能只看 returncode。

    2026-09-11（WP-H2-1）：判斷檔標了 `meta.contract="v19"` 時改走
    `_judge_check_v19`（多一步投影與 scenario 產生）。判別只看**實際寫出來的
    那份判斷檔**，不看流程預期——replay 重放舊 fixture 時仍走舊路徑。"""
    run_dir = _run_dir(ticker, date)
    py = _pick_python()
    scenario_path = run_dir / "scenario.json"
    judgment_path = run_dir / "judgment.json"
    evidence_path = run_dir / "evidence.json"
    tables_dir = run_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    if judgment_path.exists():
        try:
            if dd_project.is_v19(_load_json(judgment_path)):
                ok, parts = _judge_check_v19(run_dir, judgment_path, evidence_path, tables_dir, py)
                return ok, "\n\n".join(parts)
        except (json.JSONDecodeError, ValueError) as e:
            return False, "[error] judgment.json 不是合法 JSON：{0}".format(e)

    parts = []
    ok = True

    if not scenario_path.exists():
        parts.append("[error] 找不到 {0}".format(scenario_path))
        ok = False
    else:
        r1 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_scenario.py"), str(scenario_path),
             "--html", str(tables_dir / "e11.html"), "--meta", str(run_dir / "scenario_meta.json")],
            capture_output=True, text=True,
        )
        parts.append("[dd_scenario.py] rc={0}\n{1}".format(r1.returncode, (r1.stdout + r1.stderr).strip()))
        ok = ok and (r1.returncode == 0)

    if not judgment_path.exists():
        parts.append("[error] 找不到 {0}".format(judgment_path))
        ok = False
    else:
        r2 = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_decision.py"), "run", str(judgment_path),
             "--html", str(tables_dir / "audit.html"), "--json", str(judgment_path)],
            capture_output=True, text=True,
        )
        parts.append("[dd_decision.py run] rc={0}\n{1}".format(r2.returncode, (r2.stdout + r2.stderr).strip()))
        ok = ok and (r2.returncode == 0)

        vj_cmd = [py, str(SCRIPTS_DIR / "validate_judgment.py"), str(judgment_path),
                  "--evidence", str(evidence_path), "--fix", "--report"]
        if os.environ.get("DD_J1_WARN") == "1":
            vj_cmd.append("--j1-warn")
        r3 = subprocess.run(vj_cmd, capture_output=True, text=True)
        vj_out = (r3.stdout + r3.stderr).strip()
        parts.append("[validate_judgment.py] rc={0}\n{1}".format(r3.returncode, vj_out))
        if re.search(r"^\[FAIL\]", vj_out, re.M):
            ok = False
        elif not re.search(r"^\[PASS\]", vj_out, re.M):
            ok = False

    return ok, "\n\n".join(parts)


def cmd_judge_check(args):
    ok, report = _judge_check(args.ticker.strip().upper(), args.date)
    print(report)
    return 0 if ok else 1


def _read_decision_verdict(run_dir):
    j = _load_json_or(run_dir / "judgment.json", {})
    return ((j.get("decision_out") or {}).get("verdict"))


def _judge_mode():
    m = _JUDGE_MODE_OVERRIDE or os.environ.get("DD_JUDGE_MODE") or JUDGE_MODE_DEFAULT
    return m if m in ("short", "loop") else JUDGE_MODE_DEFAULT


def _gate_patch_mode():
    """2026-09-06：閘 🔴 修補跑法選擇，同 `_judge_mode()` 的三層優先序
    （CLI 旗標 > 環境變數 > 預設）。"""
    m = _GATE_PATCH_MODE_OVERRIDE or os.environ.get("DD_GATE_PATCH_MODE") or GATE_PATCH_MODE_DEFAULT
    return m if m in ("patchmap", "loop") else GATE_PATCH_MODE_DEFAULT


_JUDGE_LOOP_WRITE_MARKER = "## 寫（一次 Write"


def _render_oneshot_judge_prompt(mapping):
    """judge.md.tmpl 的規則段（「## 寫」之前）原樣沿用，只把「寫／禁／最終回報」
    三段換成 judge_oneshot_tail.md.tmpl——規則文字單一來源，不複製一份。"""
    tmpl = (PROMPTS_TMPL_DIR / "judge.md.tmpl").read_text(encoding="utf-8")
    idx = tmpl.find(_JUDGE_LOOP_WRITE_MARKER)
    if idx < 0:
        raise RuntimeError("judge.md.tmpl 找不到分段標記 {0!r}".format(_JUDGE_LOOP_WRITE_MARKER))
    tail = (PROMPTS_TMPL_DIR / "judge_oneshot_tail.md.tmpl").read_text(encoding="utf-8")
    return (tmpl[:idx] + tail).format_map(_SafeFormatDict(mapping))


_FENCE_RE = re.compile(r"```json:(judgment|scenario)[ \t]*\n(.*?)\n```", re.S)
_FENCE_ANY_RE = re.compile(r"```(?:json)?[ \t]*\n(.*?)\n```", re.S)


def _parse_oneshot_judgment(text):
    """從一次性呼叫的回覆抽出 judgment（＋舊形狀的 scenario）JSON。回傳 dict 或
    None（解析失敗算 None，由呼叫端決定回退）。優先認 `json:judgment`／
    `json:scenario` 標記；沒標記時退而取回覆內的 JSON 區塊——兩個就依序視為
    judgment／scenario，**一個就當 judgment**（2026-09-11 WP-H2-1：v19 只交一個
    檔，回覆備援也只會有一塊）。"""
    text = text or ""
    found = {}
    for tag, body in _FENCE_RE.findall(text):
        found.setdefault(tag, body)
    if "judgment" not in found:
        blocks = _FENCE_ANY_RE.findall(text)
        if len(blocks) == 2:
            found = {"judgment": blocks[0], "scenario": blocks[1]}
        elif len(blocks) == 1:
            found = {"judgment": blocks[0]}
    if "judgment" not in found:
        return None
    out = {}
    for tag in ("judgment", "scenario"):
        if tag not in found:
            continue
        try:
            obj = json.loads(found[tag])
        except (json.JSONDecodeError, ValueError):
            return None
        if not isinstance(obj, dict):
            return None
        out[tag] = obj
    return out


_JSONPATH_TOKEN_RE = re.compile(r"\.?([^.\[\]]+)|\[(\d+)\]")


def _set_json_path(obj, path, value):
    """把 `$.a.b[2].c` 這種（validate_judgment.py 報錯用的）路徑設成 value；
    中途缺的 dict 鍵自動建立，list 索引越界則 raise。回傳 True。"""
    p = path.strip()
    if p.startswith("$"):
        p = p[1:]
    toks = []
    for m in _JSONPATH_TOKEN_RE.finditer(p):
        toks.append(int(m.group(2)) if m.group(2) is not None else m.group(1))
    if not toks:
        raise ValueError("空路徑 {0!r}".format(path))
    cur = obj
    for t in toks[:-1]:
        if isinstance(t, int):
            cur = cur[t]
        else:
            if not isinstance(cur, dict):
                raise TypeError("路徑 {0!r} 在 {1!r} 處不是物件".format(path, t))
            cur = cur.setdefault(t, {})
    last = toks[-1]
    if isinstance(last, int):
        cur[last] = value
    else:
        if not isinstance(cur, dict):
            raise TypeError("路徑 {0!r} 末端不是物件".format(path))
        cur[last] = value
    return True


_PATCH_FENCE_RE = re.compile(r"```json:patch[ \t]*\n(.*?)\n```", re.S)


def _parse_patch_map(text):
    """從修正回覆抽 ```json:patch``` 區塊：{"judgment": {path: value}, "scenario": {path: value}}。
    解析不到回 None。"""
    m = _PATCH_FENCE_RE.search(text or "")
    if not m:
        return None
    try:
        obj = json.loads(m.group(1))
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(obj, dict):
        return None
    out = {}
    for k in ("judgment", "scenario"):
        v = obj.get(k) or {}
        if not isinstance(v, dict):
            return None
        out[k] = v
    return out


def _apply_patch_map(run_dir, patches):
    """把 patch map 套到 judgment.json／scenario.json；回傳 (套用筆數, 錯誤清單)。

    2026-09-06（FIX_20260908 opus 實測缺口）：底檔存在但解析失敗（如 short
    模式寫出的緊湊 JSON 被截斷）時，該檔**一筆都不套、不寫檔**——舊版用
    `_load_json_or(path, {})` 讀不成就從空物件開始，16 筆 patch 套完直接把
    整份判斷物覆寫成只剩 16 個欄位（資料破壞，不是修補）。錯誤訊息含檔名與
    `JSONDecodeError` 原文，讓呼叫端可以判斷「這份 patch 其實整檔沒套到」。
    """
    applied, errors = 0, []
    for name in ("judgment", "scenario"):
        pm = patches.get(name) or {}
        if not pm:
            continue
        path = run_dir / "{0}.json".format(name)
        if path.exists():
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError) as e:
                errors.append("{0} ({1}) 底檔解析失敗，本檔 patch 全數跳過未套用：{2}".format(name, path, e))
                continue
        else:
            obj = {}
        for jp, val in pm.items():
            try:
                _set_json_path(obj, jp, val)
                applied += 1
            except (KeyError, IndexError, TypeError, ValueError) as e:
                errors.append("{0} {1}: {2}".format(name, jp, e))
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return applied, errors


def _spawn_oneshot(prompt_path, model, out_json, cwd, budget):
    """無工具、單輪的 `claude -p`（`--tools ""`）：回覆全文在 result_text。
    只用於輸出很小的場合（定點修正的 patch map）；整份判斷物太大會撞輸出上限。"""
    return dd_headless.spawn(
        prompt_path=prompt_path, model=model, allowed_tools=None, max_turns=1,
        budget_cache_read=budget, out_json=out_json, cwd=cwd,
        extra_args=["--tools", ""],
    )


def _spawn_short(prompt_path, model, out_json, cwd, budget, max_turns):
    """只給 Write／Bash 的短迴圈 `claude -p`（slim 前綴下 `--tools Write,Bash`
    帶兩個工具 schema）。產物由 agent 用 Write 落檔，orchestrator 之後自己跑
    check。2026-09-06（FIX_20260908）：新增 Bash，僅供模板內建的一條 JSON
    語法自檢指令用（見 `judge_oneshot_tail.md.tmpl`／`judge_json_repair.md.tmpl`）
    ——不是給 agent 自由跑腳本或驗證內容。"""
    return dd_headless.spawn(
        prompt_path=prompt_path, model=model, allowed_tools=["Write", "Bash"], max_turns=max_turns,
        budget_cache_read=budget, out_json=out_json, cwd=cwd,
    )


def _short_outputs_ready(run_dir, started_at, result_text):
    """短迴圈收工判定：該交的檔都在且 mtime 晚於本輪開跑 → True；否則退而解析
    回覆內的 fenced JSON（備援），有就落檔回 True；都沒有 → False。

    2026-09-11（WP-H2-1）：v19 只交 `judgment.json` 一個檔（`scenario.json` 由
    程式從 `scenario_inputs` 產生），所以 scenario 的新鮮度只對舊形狀要求。"""
    jp = run_dir / "judgment.json"
    sp = run_dir / "scenario.json"
    if jp.exists() and jp.stat().st_mtime >= started_at:
        if sp.exists() and sp.stat().st_mtime >= started_at:
            return True
        try:
            single_file = dd_project.is_v19(_load_json(jp))
        except (json.JSONDecodeError, ValueError):
            # 壞 JSON 判不出形狀。v19 是現行預設、且只交一個檔——當作已交件，
            # 讓既有的「語法修復」短迴圈去修，比整段回退 loop 便宜。
            single_file = True
        if single_file:
            return True
    parsed = _parse_oneshot_judgment(result_text)
    if parsed:
        _write_oneshot_outputs(run_dir, parsed)
        return True
    return False


def _write_oneshot_outputs(run_dir, parsed):
    (run_dir / "judgment.json").write_text(
        json.dumps(parsed["judgment"], ensure_ascii=False, indent=2), encoding="utf-8")
    if "scenario" in parsed:  # v19 不交這個檔（由 scenario_inputs 產生）
        (run_dir / "scenario.json").write_text(
            json.dumps(parsed["scenario"], ensure_ascii=False, indent=2), encoding="utf-8")


def _judge_syntax_check_cmd(*paths):
    """2026-09-06（FIX_20260908）：`judge_oneshot_tail.md.tmpl`（步驟②）與
    `judge_json_repair.md.tmpl`（修復後自檢）共用同一條 Bash 語法自檢指令
    ——`json.load` 掃過傳入的判斷物，任一份不是合法 JSON 就丟
    `JSONDecodeError`（有輸出）、都過就沒有任何輸出。路徑走 `sys.argv`
    （不內嵌進 `-c` 字串），避免路徑含空白或特殊字元被誤拆。

    2026-09-11（WP-H2-1）：改收可變長度路徑——v19 只有 `judgment.json` 一個檔，
    把不存在的 `scenario.json` 一起丟進去會變成 FileNotFoundError 假警報。"""
    return (
        "python3 -c \"import json,sys; [json.load(open(p, encoding='utf-8')) "
        "for p in sys.argv[1:]]\" {0}"
    ).format(" ".join(str(p) for p in paths))


def _normalize_judge_outputs(run_dir):
    """2026-09-06：short 模式的判斷 agent 只被要求輸出緊湊 JSON（省輸出
    token，見 judge_oneshot_tail.md.tmpl），落檔後這裡轉回縮排格式，讓下游
    （judge check／人工複審/patch）讀到的仍是原本排版；不改鍵名或內容。
    解析失敗（不是合法 JSON）就保留原檔不動、不吞錯，讓後面的 judge check
    照常報錯——呼叫端把回傳的 errors 記進 manifest stage["normalize_error"]。
    回傳 (已正規化的檔名清單, 錯誤訊息清單)。"""
    normalized, errors = [], []
    for name in ("judgment", "scenario"):
        path = run_dir / "{0}.json".format(name)
        if not path.exists():
            continue
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError) as e:
            errors.append("{0}: {1}".format(name, e))
            continue
        _atomic_write_json(path, obj)
        normalized.append(name)
    return normalized, errors


def _compact_json_text(text):
    """2026-09-06：把落檔的縮排 JSON 轉回緊湊格式再嵌進修正輪 prompt（省輸入
    token）；讀不成 JSON（理論上不該發生，因為套用這裡的檔案先前已通過
    `_normalize_judge_outputs`）就原樣退回，不炸。"""
    try:
        return json.dumps(json.loads(text), ensure_ascii=False, separators=(",", ":"))
    except (json.JSONDecodeError, ValueError):
        return text


def _repair_judge_json_file(run_dir, name, err_msg, ticker, date, judgment_model, agents_dir, budget):
    """2026-09-06（FIX_20260908）：對單一壞檔（`judgment.json`／`scenario.json`）
    派一輪『只修語法』的短迴圈修復——不當成判斷段的定點修正（patch map）
    處理，因為連 JSON 都解析不了就沒有『欄位路徑』可指。

    Write 工具拒絕覆寫本 session 未 Read 過的檔，而修復 agent（`_spawn_short`）
    沒有 Read 工具，故寫檔前先把原檔（連同其壞內容）搬去 `agents/` 備份、
    原路徑清空，讓 agent 能對同一路徑重新整檔 Write；agent 沒寫回、或寫回的
    仍不是合法 JSON，就從備份還原（不留半殘檔）。

    回傳 (repaired: bool, agent_usage: dict|None)。"""
    run_dir = Path(run_dir)
    agents_dir = Path(agents_dir)
    path = run_dir / "{0}.json".format(name)
    if not path.exists():
        return False, None
    original_text = path.read_text(encoding="utf-8")
    backup_path = agents_dir / "{0}_broken_backup.json".format(name)
    backup_path.write_text(original_text, encoding="utf-8")
    path.unlink()

    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    prompt_path = agents_dir / "{0}_repair.md".format(name)
    prompt_path.write_text(
        _render_format_template(PROMPTS_TMPL_DIR / "judge_json_repair.md.tmpl", {
            "ticker": ticker, "date": date, "name": name, "path": str(path),
            "error": err_msg,
            # 2026-09-11（WP-H2-1）：只掃**這一輪真的存在或即將被重寫**的檔——
            # v19 沒有 scenario.json，硬掃會變成 FileNotFoundError 假警報。
            "check_cmd": _judge_syntax_check_cmd(*(
                [str(judgment_path)] + ([str(scenario_path)] if scenario_path.exists() else []))),
            "max_turns": str(JUDGE_JSON_REPAIR_MAX_TURNS),
        }),
        encoding="utf-8",
    )
    # 原檔全文（壞內容）走 `_write_inline_prompt` 接在分隔行之後——同 bundle／
    # 修補全文的既有作法，避免 JSON 裡的大括號被 `.format_map` 誤判成佔位符。
    inline_prompt_path = _write_inline_prompt(prompt_path, backup_path)
    usage = _spawn_short(
        inline_prompt_path, judgment_model, agents_dir / "{0}_repair_1.json".format(name),
        run_dir, budget, JUDGE_JSON_REPAIR_MAX_TURNS,
    )

    if not path.exists():
        path.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")
        return False, usage
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return False, usage
    return True, usage


def _repair_broken_judge_files(run_dir, ticker, date, judgment_model, agents_dir, budget, normalize_errors):
    """2026-09-06（FIX_20260908）：對 `_normalize_judge_outputs` 回報的每一個
    壞檔各派一次 `_repair_judge_json_file`。回傳
    `{"files": [{"name": ..., "repaired": bool}, ...], "ok": bool,
    "agent_usage": [...]}`（`ok` 為 True 僅當所有回報的壞檔事後都能重新
    `json.loads`）。"""
    files_result = []
    agent_usage = []
    for name in ("judgment", "scenario"):
        err_msg = None
        for e in normalize_errors:
            if e.startswith(name + ":"):
                err_msg = e
                break
        if err_msg is None:
            continue
        repaired, usage = _repair_judge_json_file(
            run_dir, name, err_msg, ticker, date, judgment_model, agents_dir, budget,
        )
        files_result.append({"name": name, "repaired": repaired})
        if usage is not None:
            agent_usage.append(usage)
    ok = bool(files_result) and all(f["repaired"] for f in files_result)
    return {"files": files_result, "ok": ok, "agent_usage": agent_usage}


# ---------------------------------------------------------------------------
# WP-C（2026-09-10）：複審 delta 判斷——路由決定＋delta 判斷 spawn＋零 Fable
# 沿用。三個出口共用同一顆「判斷級🔴一律走 opus 跨模型冷讀」的下游閘
# （`_do_gate` 不因判斷是 full／delta／reuse 產出而改行為，見任務點 3）。
# ---------------------------------------------------------------------------

def _judge_delta_route(ticker, date, run_dir, no_delta):
    """回傳本輪判斷要走 `full`／`delta`／`reuse`，附帶決策理由與（若算過）
    delta.json 路徑：`{"mode", "reasons", "delta_path", "prior_archive_dir",
    "prior_date"}`。任何一步找不到東西或子行程失敗都保守回退 `full`（既有
    行為的超集，不會因為這條新路由讓判斷「漏做」，只會讓它「多做」）。"""
    if no_delta:
        return {"mode": "full", "reasons": ["cli --no-delta"], "delta_path": None}

    prior = _prior_judgment_archive(ticker, date)
    if not prior:
        return {"mode": "full", "reasons": ["no_prior_judgment_archive"], "delta_path": None}

    evidence_path = run_dir / "evidence.json"
    if not evidence_path.exists():
        return {"mode": "full", "reasons": ["evidence_missing_for_delta"], "delta_path": None}

    delta_path = run_dir / "delta.json"
    py = _pick_python()
    cmd = [py, str(SCRIPTS_DIR / "dd_delta.py"), ticker, date,
           "--prior", str(prior["archive_dir"]), "--evidence", str(evidence_path),
           "--out", str(delta_path)]
    digest_path = run_dir / "digest.json"
    if digest_path.exists():
        cmd += ["--digest", str(digest_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return {"mode": "full",
                "reasons": ["dd_delta_generate_failed: {0}".format((r.stdout + r.stderr).strip()[-500:])],
                "delta_path": None}

    delta = _load_json_or(delta_path, None)
    if delta is None:
        return {"mode": "full", "reasons": ["delta_json_unreadable"], "delta_path": str(delta_path)}

    base = {"delta_path": str(delta_path), "prior_archive_dir": str(prior["archive_dir"]),
            "prior_date": prior["source_date"]}

    # (a)：dd_delta.py 自己算的 full_rewrite_required（price_at_dd >40%／prior
    # >180 天／archetype_hint 與 prior 判斷 archetype 不同）——(c) 的 180 天
    # 門檻已內含在這裡，不另外重算一次年限。
    full_req = delta.get("full_rewrite_required") or {}
    if full_req.get("required"):
        reasons = ["full_rewrite_required: {0}".format(x) for x in (full_req.get("reasons") or [])]
        return dict(base, mode="full", reasons=reasons or ["full_rewrite_required"])

    # (b)：events 五類裡的重大類（見 EVENTS_MAJOR_CATEGORIES 常數註解）出現
    # 新 finding。
    events_changed = delta.get("events_changed") or {}
    major_hits = sorted(
        cat for cat in events_changed
        if cat in EVENTS_MAJOR_CATEGORIES and (events_changed.get(cat) or {}).get("new_findings")
    )
    if major_hits:
        return dict(base, mode="full",
                    reasons=["events_major_category_changed: {0}".format(", ".join(major_hits))])

    # (f)：<45 天且三塊皆空 → 不進 Fable，直接沿用 prior。
    no_change = (
        not delta.get("numbers_changed")
        and not delta.get("coverage_changed")
        and not delta.get("events_changed")
    )
    if no_change and prior["age_days"] < DELTA_NOCHANGE_MAX_AGE_DAYS:
        return dict(base, mode="reuse",
                    reasons=["no_material_change age_days={0}<{1}".format(
                        prior["age_days"], DELTA_NOCHANGE_MAX_AGE_DAYS)])

    return dict(base, mode="delta", reasons=["delta_mode age_days={0}".format(prior["age_days"])])


def _delta_has_new_quarter(prior_evidence, new_evidence):
    """WP-C：判斷本輪 evidence 的最新一季逐字稿是否與 prior 不同——沿用
    `dd_bundle.py::_transcript_section` 的同一條規則（`recent_four_quarters`
    依日期由舊到新，`[-1]` 是最新那篇）。只比檔名，不比內容。"""
    def _latest(ev):
        rec = ((ev or {}).get("transcripts") or {}).get("selected") or {}
        files = rec.get("recent_four_quarters") or []
        return files[-1] if files else None
    new_latest = _latest(new_evidence)
    return bool(new_latest) and new_latest != _latest(prior_evidence)


def _delta_evidence_excerpt(evidence, delta):
    """WP-C：只把 delta.json 標為『有變動』的 evidence 節錄接進 judge_delta
    bundle——不是整份 evidence.json，也不只是新增的 finding。`coverage_changed`／
    `events_changed` 的軸／類別鍵直接對回 `evidence.coverage[axis]`／
    `evidence.events[category]` **整段現況**（不只 delta 裡的 `new_findings`），
    讓 Fable 看得到該軸完整現況才判斷得出裁決；`numbers_changed` 的路徑第二段
    是 `numbers.<subkey>`，同樣對回整個子鍵現況。沒被 delta 點名的軸／子鍵
    視為維持 prior 認定，不附。"""
    lines = []
    numbers_subkeys = sorted({
        (rec.get("path") or "").split(".")[1]
        for rec in (delta.get("numbers_changed") or [])
        if len((rec.get("path") or "").split(".")) > 1
    })
    if numbers_subkeys:
        excerpt = {k: (evidence.get("numbers") or {}).get(k) for k in numbers_subkeys}
        lines.append("### numbers（僅列有變動的子鍵：{0}）\n\n```json\n{1}\n```".format(
            ", ".join(numbers_subkeys), json.dumps(excerpt, ensure_ascii=False, indent=2)))
    cov_axes = sorted((delta.get("coverage_changed") or {}).keys())
    if cov_axes:
        excerpt = {a: (evidence.get("coverage") or {}).get(a) for a in cov_axes}
        lines.append("### coverage（僅列有變動的軸，含完整現況非只新增 finding：{0}）\n\n```json\n{1}\n```".format(
            ", ".join(cov_axes), json.dumps(excerpt, ensure_ascii=False, indent=2)))
    ev_cats = sorted((delta.get("events_changed") or {}).keys())
    if ev_cats:
        excerpt = {c: (evidence.get("events") or {}).get(c) for c in ev_cats}
        lines.append("### events（僅列有變動的類別，含完整現況非只新增 finding：{0}）\n\n```json\n{1}\n```".format(
            ", ".join(ev_cats), json.dumps(excerpt, ensure_ascii=False, indent=2)))
    if not lines:
        lines.append("（delta.json 三塊皆無變動——理論上不會走到 delta 分支，見 `_judge_delta_route` 的 reuse 出口）")
    return "\n\n".join(lines)


def _judge_delta_bundle_text(prior_judgment_text, prior_scenario_text, delta, evidence_excerpt, transcript_section):
    """WP-C：delta 判斷 bundle——比照 `judge.md.tmpl` 的 bundle-after-separator
    慣例（見 `_write_inline_prompt`），大段原文（可能含大括號）一律走這裡，
    不經 `.format_map`。"""
    parts = [
        "## prior judgment.json 全文\n\n```json\n{0}\n```".format(
            _compact_json_text(prior_judgment_text)),
        "## prior scenario.json 全文（`dd_scenario.py` 輸入格式；delta 沒有涉及"
        "估值輸入時原樣照抄這份）\n\n```json\n{0}\n```".format(
            _compact_json_text(prior_scenario_text) if prior_scenario_text else "null"),
        "## delta.json 全文\n\n```json\n{0}\n```".format(
            json.dumps(delta, ensure_ascii=False, separators=(",", ":"))),
        "## evidence 節錄（僅列有變動的軸／子鍵）\n\n{0}".format(evidence_excerpt),
        "## 最新一季逐字稿\n\n{0}".format(transcript_section),
    ]
    return "\n\n---\n\n".join(parts) + "\n"


def _do_judge_delta(ticker, date, judgment_model, accept_over_budget, manifest, stage, route):
    """WP-C：Fable 單輪只改 `delta.judgment_fields_to_review` 涉及欄位。輸出
    經 `judge check`＋`dd_delta.py check` 雙重驗算；任一 FAIL、或裁決相對
    prior 翻面，本輪 delta 判斷作廢（保留在 `judgment_delta_rejected.json`），
    自動升級全套（呼叫 `_do_judge_full`，延續同一個 `stage` 物件累計成本，
    不歸零重算）。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    agents_dir = run_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    prior_archive_dir = Path(route["prior_archive_dir"])
    prior_stem = prior_archive_dir.name
    prior_judgment_path = prior_archive_dir / "{0}.judgment.json".format(prior_stem)
    prior_evidence_path = prior_archive_dir / "{0}.evidence.json".format(prior_stem)
    prior_scenario_path = prior_archive_dir / "{0}.scenario.json".format(prior_stem)
    delta_path = Path(route["delta_path"])

    evidence = _load_json_or(run_dir / "evidence.json", {})
    prior_evidence = _load_json_or(prior_evidence_path, {})
    delta = _load_json_or(delta_path, {})
    prior_judgment_text = prior_judgment_path.read_text(encoding="utf-8")
    prior_judgment = json.loads(prior_judgment_text)
    prior_scenario_text = prior_scenario_path.read_text(encoding="utf-8") if prior_scenario_path.exists() else None

    transcript_section = (
        dd_bundle._transcript_section(evidence, None)
        if _delta_has_new_quarter(prior_evidence, evidence)
        else "（delta 判定本輪最新一季與 prior 相同，沿用 prior 既有親讀結論，不重附全文）"
    )
    evidence_excerpt = _delta_evidence_excerpt(evidence, delta)

    bundle_text = _judge_delta_bundle_text(
        prior_judgment_text, prior_scenario_text, delta, evidence_excerpt, transcript_section)
    bundle_path = run_dir / "bundles" / "judge_delta.md"
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(bundle_text, encoding="utf-8")

    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    prompt_path = run_dir / "prompts" / "b1_judge_delta.md"
    review_fields = delta.get("judgment_fields_to_review") or []
    prior_date_display = (prior_judgment.get("meta") or {}).get("date") or route.get("prior_date")
    mapping = {
        "ticker": ticker, "date": date, "prior_date": prior_date_display,
        "judgment_path": str(judgment_path), "scenario_path": str(scenario_path),
        "max_turns": str(JUDGE_DELTA_MAX_TURNS),
        "review_fields_block": "\n".join("- `{0}`".format(p) for p in review_fields)
            or "（無——理論上不會走到這裡，delta_fields 至少恆含 `contradictions`）",
        "check_cmd": _judge_syntax_check_cmd(str(judgment_path), str(scenario_path)),
    }
    prompt_path.write_text(
        _render_format_template(PROMPTS_TMPL_DIR / "judge_delta.md.tmpl", mapping), encoding="utf-8")
    inline_prompt_path = _write_inline_prompt(prompt_path, bundle_path)

    t0 = time.time()
    r = _spawn_short(inline_prompt_path, judgment_model, agents_dir / "judge_delta_1.json",
                      run_dir, JUDGE_DELTA_BUDGET_CACHE_READ, JUDGE_DELTA_MAX_TURNS)
    stage["agent_usage"].append(r)
    _atomic_write_json(manifest_path, manifest)

    if r.get("quota_exhausted"):
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "delta：訂閱額度耗盡"
        manifest["stages"]["judged"] = stage
        manifest["state"] = "judged_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("judged", "delta quota_exhausted", "validate PASS", "FAIL")
        _print_resume_hint(ticker, date, "judged")
        return 1

    ready = _short_outputs_ready(run_dir, t0, r.get("result_text"))
    if not ready:
        stage["judge_route_reasons"] = list(stage.get("judge_route_reasons") or []) + ["delta_no_output_escalate_full"]
        stage["delta_mode"] = "full"
        print("[judged] delta 判斷未寫出兩檔，升級全套")
        return _do_judge_full(ticker, date, judgment_model, None, accept_over_budget, manifest, stage)

    _, normalize_errors = _normalize_judge_outputs(run_dir)
    if normalize_errors:
        stage["normalize_error"] = normalize_errors
        repair = _repair_broken_judge_files(
            run_dir, ticker, date, judgment_model, agents_dir,
            JUDGE_DELTA_BUDGET_CACHE_READ, normalize_errors,
        )
        stage["json_repair"] = repair
        stage["agent_usage"].extend(repair["agent_usage"])
        if not repair["ok"]:
            stage["judge_route_reasons"] = list(stage.get("judge_route_reasons") or []) + ["delta_json_unrepairable_escalate_full"]
            stage["delta_mode"] = "full"
            print("[judged] delta 判斷 JSON 修復失敗，升級全套")
            return _do_judge_full(ticker, date, judgment_model, None, accept_over_budget, manifest, stage)
        _, normalize_errors = _normalize_judge_outputs(run_dir)
        stage["normalize_error"] = normalize_errors

    # ---- 雙重驗算：judge check（一般機械驗算）＋ dd_delta.py check（delta 專屬：
    # 改動範圍是否越界、DRIFT_WATCH 漂移是否都有歸因）----
    ok, report = _judge_check(ticker, date)
    delta_ok, delta_report = True, ""
    if ok:
        py = _pick_python()
        rc_check = subprocess.run(
            [py, str(SCRIPTS_DIR / "dd_delta.py"), "check", str(delta_path),
             "--judgment", str(judgment_path), "--prior-judgment", str(prior_judgment_path)],
            capture_output=True, text=True,
        )
        delta_ok = (rc_check.returncode == 0)
        delta_report = (rc_check.stdout + rc_check.stderr).strip()
        stage["dd_delta_check"] = {"ok": delta_ok, "tail": delta_report[-4000:]}

    prior_verdict = (prior_judgment.get("decision_out") or {}).get("verdict")
    new_verdict = _read_decision_verdict(run_dir) if (ok and delta_ok) else None
    verdict_flipped = bool(ok and delta_ok and prior_verdict and new_verdict and new_verdict != prior_verdict)

    if (not ok) or (not delta_ok) or verdict_flipped:
        reject_path = run_dir / "judgment_delta_rejected.json"
        if judgment_path.exists():
            reject_path.write_text(judgment_path.read_text(encoding="utf-8"), encoding="utf-8")
        if not ok:
            reason = "judge_check_fail"
        elif not delta_ok:
            reason = "dd_delta_check_fail"
        else:
            reason = "verdict_flip prior={0} new={1}".format(prior_verdict, new_verdict)
        stage["delta_rejected"] = {
            "reason": reason, "rejected_path": str(reject_path),
            "judge_check_tail": report[-2000:], "dd_delta_check_tail": delta_report[-2000:],
        }
        stage["judge_route_reasons"] = list(stage.get("judge_route_reasons") or []) + ["delta_rejected: {0}".format(reason)]
        stage["delta_mode"] = "full"
        manifest["stages"]["judged"] = stage
        _atomic_write_json(manifest_path, manifest)
        print("[judged] delta 判斷作廢（{0}），升級全套".format(reason))
        return _do_judge_full(ticker, date, judgment_model, None, accept_over_budget, manifest, stage)

    # delta 判斷通過（judge check PASS、dd_delta check PASS、裁決未翻面）——
    # 補 meta 兩欄後直接收尾，不重跑 judge check（內容除 meta 外未再變動）。
    judgment = _load_json(judgment_path)
    judgment.setdefault("meta", {})["judge_mode"] = "delta"
    judgment["meta"]["delta_of"] = prior_stem
    judgment_path.write_text(json.dumps(judgment, ensure_ascii=False, indent=2), encoding="utf-8")

    return _judge_finalize_after_check(
        ticker, date, judgment_model, None, accept_over_budget, manifest, stage,
        agents_dir, True, report, fix_suffix="delta", fix_mode="short",
    )


def _judge_reuse_prior(ticker, date, judgment_model, accept_over_budget, manifest, stage, route):
    """WP-C (f)：<45 天且 delta 三塊皆無變動——不進 Fable，直接複製 prior 判斷物
    當本輪判斷（只改 `meta.date`、補 `meta.judge_mode`/`meta.delta_of`），跑
    一次 `judge check` 確認在新日期下仍自洽（`tables/`／`scenario_meta.json`
    也要在本輪 run_dir 重新產生，不能沿用 prior 那份路徑已失效的檔）。prior
    存查缺 `scenario.json`（理論上不會，判斷段的必要輸出）時保守降級走
    delta 模式，不強行沿用半殘的存查。"""
    run_dir = _run_dir(ticker, date)
    (run_dir / "agents").mkdir(parents=True, exist_ok=True)
    (run_dir / "prompts").mkdir(parents=True, exist_ok=True)
    prior_archive_dir = Path(route["prior_archive_dir"])
    prior_stem = prior_archive_dir.name
    prior_judgment_path = prior_archive_dir / "{0}.judgment.json".format(prior_stem)
    prior_scenario_path = prior_archive_dir / "{0}.scenario.json".format(prior_stem)

    if not prior_scenario_path.exists():
        stage["judge_route_reasons"] = list(stage.get("judge_route_reasons") or []) + [
            "reuse_missing_prior_scenario_fallback_delta"]
        stage["delta_mode"] = "delta"
        print("[judged] reuse：prior 存查缺 scenario.json，回退 delta 模式")
        return _do_judge_delta(ticker, date, judgment_model, accept_over_budget, manifest, stage, route)

    judgment = _load_json(prior_judgment_path)
    judgment.setdefault("meta", {})
    judgment["meta"]["date"] = "{0}-{1}-{2}".format(date[0:4], date[4:6], date[6:8])
    judgment["meta"]["judge_mode"] = "delta"
    judgment["meta"]["delta_of"] = prior_stem
    (run_dir / "judgment.json").write_text(
        json.dumps(judgment, ensure_ascii=False, indent=2), encoding="utf-8")

    scenario = _load_json(prior_scenario_path)
    scenario["date"] = judgment["meta"]["date"]
    (run_dir / "scenario.json").write_text(
        json.dumps(scenario, ensure_ascii=False, indent=2), encoding="utf-8")

    ok, report = _judge_check(ticker, date)
    return _judge_finalize_after_check(
        ticker, date, judgment_model, None, accept_over_budget, manifest, stage,
        run_dir / "agents", ok, report, fix_suffix="reuse", fix_mode="short",
    )


# WP-H2-3（2026-09-11）：TSM 成對測試用的判斷契約覆寫。`ddreport.py judge
# --contract v18` 讓**同一份證據**再跑一次舊契約的判斷包，好回答「v19 的分工有
# 沒有漏掉 v18 看得到的東西、省了多少」。兩次跑共用同一個 run 目錄（證據只收一
# 次，這正是成對測試的重點），**產物以檔名區分**：跑完把 `judgment.json` 等四件
# 快照成 `*_v19.json`／`*_v18.json`，下一次換契約跑不會蓋掉上一次的結果。
# 活檔（`judgment.json`）永遠是最後一次跑出來的那份，下游 prose／gate／finish
# 的語意不變——要比較就比兩份快照，不要去猜活檔是誰。
_JUDGE_CONTRACT_OVERRIDE = None
_JUDGE_SNAPSHOT_FILES = ("judgment.json", "scenario.json", "scenario_meta.json", "judgment_view.json")


def _judge_contract():
    return _JUDGE_CONTRACT_OVERRIDE or "v19"


def _snapshot_judge_outputs(run_dir, contract):
    """把本輪判斷產物複製成帶契約字尾的快照。複製不是搬移——活檔留在原位，
    下游不受影響。回傳已快照的檔名清單。"""
    done = []
    for name in _JUDGE_SNAPSHOT_FILES:
        src = Path(run_dir) / name
        if not src.exists():
            continue
        stem, _, ext = name.rpartition(".")
        dst = Path(run_dir) / "{0}_{1}.{2}".format(stem, contract, ext)
        shutil.copyfile(src, dst)
        done.append(dst.name)
    return done


def _do_judge(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, no_delta=False):
    """WP-C（2026-09-10）：判斷段總入口。先建立/接續 `judged` stage，再問一次
    `_judge_delta_route` 決定本輪要 `full`（既有整份判斷流程，改名
    `_do_judge_full` 承接，行為完全不變）、`delta`（`_do_judge_delta`：Fable
    單輪只補被點名欄位）還是 `reuse`（`_judge_reuse_prior`：<45 天且零實質
    變動，不進 Fable）。`replay_dir` 一律走 full（回溯重放的既有語意不變、
    也沒有「prior 存查」這個概念可比）。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"

    # WP-H2-3（2026-09-11，Codex 裁定 1）：事實表 spawn 失手、退回機械初稿時
    # **判斷段不准開跑**。理由：v19 的判斷層只看事實表，初稿的六題全帶
    # `needs_sonnet`（＝這題沒補齊），拿它去判斷等於在半份輸入上定案，而事實
    # 檢查對「摘要裡才有的反證沒被抬進來」是查不到的（0 FAIL、0 WARN）。
    # 便宜的修法是重跑 Stage 0 的事實表，不是讓判斷層硬吞。
    if manifest.get("facts_incomplete"):
        print("[judged] 事實表未完成，交指揮者：Stage 0 的事實表 agent 失手、"
              "目前 facts.json 是機械初稿（六題皆 needs_sonnet）。"
              "先重跑 `ddreport.py stage0 {0} {1}` 補齊事實表，再進判斷段。".format(ticker, date))
        _print_step_status("judged", "facts_incomplete=true", "facts PASS", "BLOCKED")
        return 1

    stage = _fresh_stage_preserving_prior(manifest, "judged")
    manifest.setdefault("stages", {})["judged"] = stage
    manifest["judgment_model"] = judgment_model
    manifest["state"] = "judged_running"
    _atomic_write_json(manifest_path, manifest)

    contract = _judge_contract()
    manifest["judge_contract"] = contract
    route = {"mode": "full", "reasons": ["replay_from"] if replay_dir else ["no_prior_judgment_archive"],
             "delta_path": None}
    if contract != "v19":
        # 成對測試要的是「同證據、整份重判」——走 delta 或 reuse 會把 v19 那輪的
        # 結論帶進來，比出來的差異就不算數了。
        route["reasons"] = ["contract_override_{0}".format(contract)]
    elif not replay_dir:
        route = _judge_delta_route(ticker, date, run_dir, no_delta)
    stage["delta_mode"] = route["mode"]
    stage["judge_route_reasons"] = route["reasons"]
    stage["trigger_check"] = TRIGGER_MECHANICAL_CHECK  # (d)：見常數區塊註解，恆定回報，不影響路由
    if route.get("delta_path"):
        stage["delta_path"] = route["delta_path"]
    manifest["stages"]["judged"] = stage
    _atomic_write_json(manifest_path, manifest)

    if route["mode"] == "reuse":
        rc = _judge_reuse_prior(ticker, date, judgment_model, accept_over_budget, manifest, stage, route)
    elif route["mode"] == "delta":
        rc = _do_judge_delta(ticker, date, judgment_model, accept_over_budget, manifest, stage, route)
    else:
        rc = _do_judge_full(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage)

    if rc == 0:
        snapped = _snapshot_judge_outputs(run_dir, contract)
        if snapped:
            stage["contract_snapshot"] = snapped
            manifest["stages"]["judged"] = stage
            _atomic_write_json(manifest_path, manifest)
            print("[judged] 契約 {0} 產物快照：{1}".format(contract, "、".join(snapped)))
    return rc


def _do_judge_full(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage):
    """WP-C 抽出：v17 既有整份判斷流程（bundle → judge.md.tmpl → spawn →
    judge check → 修正輪），原本是 `_do_judge` 本體，行為完全不變——只是改成
    接受已建好的 `stage` 物件，讓 `_do_judge`（一般全套路徑）與
    `_do_judge_delta`（delta 判斷作廢後升級全套）共用同一支函式與同一個
    `stage`（累計成本不因升級而歸零）。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"

    py = _pick_python()
    contract = _judge_contract()
    bundle_path = run_dir / "bundles" / ("judge.md" if contract == "v19"
                                         else "judge_{0}.md".format(contract))
    rb = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_bundle.py"), "judge", "--run-dir", str(run_dir),
         "--contract", contract, "--out", str(bundle_path)],
        capture_output=True, text=True,
    )
    if rb.returncode != 0:
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_bundle.py judge 失敗：{0}".format((rb.stdout + rb.stderr)[-1000:])
        manifest["stages"]["judged"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("judged", "bundle_rc={0}".format(rb.returncode), "PASS", "FAIL")
        _print_resume_hint(ticker, date, "judged")
        return 1

    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    prompt_path = run_dir / "prompts" / "b1_judge.md"
    mapping = {
        "run_dir": str(run_dir), "bundle_path": str(bundle_path),
        "judgment_path": str(judgment_path), "scenario_path": str(scenario_path),
        "ticker": ticker, "date": date, "max_turns": str(JUDGE_MAX_TURNS),
        # 2026-09-06（FIX_20260908）：short 模板步驟②與語法修復模板共用同一條
        # 自檢指令，這裡先算好塞進 mapping，兩邊模板都直接取用同一份字串。
        # 2026-09-11（WP-H2-1）：v19 只交 judgment.json，自檢只掃這一份。
        "check_cmd": _judge_syntax_check_cmd(str(judgment_path)),
    }
    prompt_path.write_text(_render_format_template(PROMPTS_TMPL_DIR / "judge.md.tmpl", mapping), encoding="utf-8")
    if replay_dir:
        _append_replay_marker(prompt_path, {
            "kind": "judgment", "judgment_out": str(judgment_path), "scenario_out": str(scenario_path),
        })

    inline_prompt_path = _write_inline_prompt(prompt_path, bundle_path)

    agents_dir = run_dir / "agents"
    mode = "loop" if replay_dir else _judge_mode()
    stage["judge_mode"] = mode
    if mode == "short":
        os_prompt_path = run_dir / "prompts" / "b1_judge_short.md"
        mapping_short = dict(mapping, max_turns=str(JUDGE_SHORT_MAX_TURNS))
        os_prompt_path.write_text(_render_oneshot_judge_prompt(mapping_short), encoding="utf-8")
        inline_os_path = _write_inline_prompt(os_prompt_path, bundle_path)
        t0 = time.time()
        r_os = _spawn_short(inline_os_path, judgment_model, agents_dir / "judge_1.json",
                            run_dir, JUDGE_BUDGET_CACHE_READ, JUDGE_SHORT_MAX_TURNS)
        stage["agent_usage"].append(r_os)
        ready = _short_outputs_ready(run_dir, t0, r_os.get("result_text")) if not r_os.get("quota_exhausted") else False
        json_ready_ok = False
        if ready:
            # 2026-09-06（FIX_20260908 opus 實測缺口）：agent 寫的是緊湊 JSON
            # （省輸出 token），check 前先轉回縮排格式；解析失敗不直接放給
            # judge check 去報錯——先派一輪「語法修復」短迴圈補救（見
            # `_repair_broken_judge_files`），仍失敗才真的回退 loop。
            _, normalize_errors = _normalize_judge_outputs(run_dir)
            if normalize_errors:
                stage["normalize_error"] = normalize_errors
                repair = _repair_broken_judge_files(
                    run_dir, ticker, date, judgment_model, agents_dir,
                    JUDGE_BUDGET_CACHE_READ, normalize_errors,
                )
                stage["json_repair"] = repair
                stage["agent_usage"].extend(repair["agent_usage"])
                if repair["ok"]:
                    _, normalize_errors = _normalize_judge_outputs(run_dir)
                    stage["normalize_error"] = normalize_errors
                json_ready_ok = repair["ok"] and not normalize_errors
            else:
                json_ready_ok = True

        if ready and json_ready_ok:
            ok, report = _judge_check(ticker, date)
            return _judge_finalize_after_check(
                ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
                agents_dir, ok, report, fix_suffix="1", fix_mode="short",
            )
        if ready and not json_ready_ok:
            # 語法修復仍失敗：不能假裝有修就跑 judge check——直接回退 loop，
            # 讓下面既有的 loop-mode 判斷 agent 重新整段來過。
            stage["short_fallback"] = "short：JSON 語法修復後仍無法解析（{0}），回退 loop 模式".format(
                stage.get("normalize_error"))
            print("[judged] " + stage["short_fallback"])
            _atomic_write_json(manifest_path, manifest)
        elif r_os.get("quota_exhausted"):
            stage["state"] = "FAIL"
            stage["ended"] = _now()
            stage["note"] = "short：訂閱額度耗盡"
            manifest["stages"]["judged"] = stage
            manifest["state"] = "judged_fail"
            _atomic_write_json(manifest_path, manifest)
            _print_step_status("judged", "short quota_exhausted", "validate PASS", "FAIL")
            _print_resume_hint(ticker, date, "judged")
            return 1
        else:
            stage["short_fallback"] = "短迴圈未寫出 judgment／scenario 兩檔、回覆也無可解析 JSON（ok={0} turns={1}），回退 loop 模式".format(
                r_os.get("ok"), r_os.get("num_turns"))
            print("[judged] " + stage["short_fallback"])
            _atomic_write_json(manifest_path, manifest)

    r_spawn = dd_headless.spawn(
        prompt_path=inline_prompt_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
        max_turns=JUDGE_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
        out_json=agents_dir / "judge_1{0}.json".format("_loop" if mode == "short" else ""), cwd=run_dir,
    )
    stage["agent_usage"].append(r_spawn)

    ok, report = _judge_check(ticker, date)
    return _judge_finalize_after_check(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        agents_dir, ok, report, fix_suffix="1", fix_mode="loop",
    )


def _judge_finalize_after_check(ticker, date, judgment_model, replay_dir, accept_over_budget,
                                 manifest, stage, agents_dir, ok, report, fix_suffix="1",
                                 fix_mode=None):
    """判斷物已寫出（或沿用既有）、`judge check` 剛跑過一次的結果為
    `(ok, report)`：FAIL 時派一輪『定點修正』agent、重跑一次 check；把結果
    收斂進 `stage` 並回寫 manifest。共用於 `_do_judge`（首次判斷後）與
    WP7b #5 的 `--resume`（`judged_fail` 狀態先重跑 judge check，FAIL 才
    派修補 agent，不重派整段判斷）。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    judgment_path = run_dir / "judgment.json"
    scenario_path = run_dir / "scenario.json"
    stage.setdefault("agent_usage", [])
    if fix_mode is None:
        fix_mode = "loop" if replay_dir else _judge_mode()

    # WP-H2-1（2026-09-11）：v19 的修補上限是**一次 patch map**。修不了就停、
    # 印「交指揮者」，不再回退 loop 修正 agent——loop 那條路是「讓模型自己整段
    # 再想一次」，與「判斷一回合」的設計直接衝突，而且真正修不掉的多半是缺判斷
    # 值（程式不准補、模型再跑一次也只會編一個），該由人裁定。
    v19_one_shot_fix = False
    if judgment_path.exists():
        try:
            v19_one_shot_fix = dd_project.is_v19(_load_json(judgment_path))
        except (json.JSONDecodeError, ValueError):
            v19_one_shot_fix = False

    if not ok and fix_mode == "short":
        # 定點修正＝patch map：失敗原文＋目前兩檔全文進 prompt、無工具單輪，
        # 回覆只列「路徑 → 新值」，orchestrator 套用後再跑 check。
        # 不整檔重寫：FIX A/B 實測整檔重寫一次 32K 輸出 token（$3.2），比省下的
        # cache_read 還貴——判斷段的錢在輸出，不在上下文。
        fix_os_path = run_dir / "prompts" / "b1_fix_short.md"
        fix_os_path.write_text(
            "你是 stock-analyst v17 判斷 agent，回來做一輪定點修正。標的 {0}（{1}）。"
            "本輪沒有任何工具、只回覆一次。\n\n"
            "`judge check` 的失敗原文如下，**只准改被點名的欄位**，其餘一字不動。"
            "回覆**只含一個** ```json:patch 程式碼區塊，內容形狀固定：\n\n"
            "```json:patch\n{{\n  \"judgment\": {{\"$.section.field\": <該欄位修正後的完整新值>, ...}},\n"
            "  \"scenario\": {{\"$.路徑\": <新值>, ...}}\n}}\n```\n\n"
            "- 路徑用失敗原文裡的寫法（`$.a.b[2].c`）；值是**該路徑整個欄位**的新值"
            "（字串就給整段新字串，物件就給整個物件），不是差異描述。\n"
            "- 沒被點名的欄位不要出現在 patch 裡；某一檔沒有要改就給空物件 {{}}。\n"
            "- 不得為湊過驗證而編造缺證據的數字（FAIL 通常指欄位缺失或內部恆等式不符）；"
            "不得整段改寫判斷；區塊外不寫任何文字。\n\n"
            "## judge check 失敗原文\n\n```\n{2}\n```\n\n"
            "## 目前 judgment.json 全文（緊湊格式，僅省空白、內容與縮排版相同）\n\n```json\n{3}\n```\n\n"
            "## 目前 scenario.json 全文（緊湊格式，僅省空白、內容與縮排版相同）\n\n```json\n{4}\n```\n".format(
                ticker, date, report,
                _compact_json_text(judgment_path.read_text(encoding="utf-8")) if judgment_path.exists() else "{}",
                _compact_json_text(scenario_path.read_text(encoding="utf-8")) if scenario_path.exists() else "{}",
            ),
            encoding="utf-8")
        r_fix = _spawn_oneshot(fix_os_path, judgment_model,
                               agents_dir / "judge_fix_{0}.json".format(fix_suffix),
                               run_dir, JUDGE_BUDGET_CACHE_READ)
        stage["agent_usage"].append(r_fix)
        patches = _parse_patch_map(r_fix.get("result_text")) if (r_fix.get("ok") and not r_fix.get("quota_exhausted")) else None
        if patches is not None:
            n, errs = _apply_patch_map(run_dir, patches)
            stage["short_fix_patch"] = {"applied": n, "errors": errs}
            print("[judged] patch map 套用 {0} 筆，錯誤 {1}".format(n, len(errs)))
            if errs and n == 0:
                # 2026-09-06（FIX_20260908）：底檔解析失敗等情形讓 patch 整批
                # 一筆都沒套到——不能假裝修過就跑 judge check，直接回退 loop
                # （見 `_apply_patch_map` 註解：套不到就不寫檔，原檔保持不變）。
                stage["short_fix_fallback"] = "patch map 全數未套用（errors={0}），改派 loop 修正 agent".format(errs)
                print("[judged] " + stage["short_fix_fallback"])
                fix_mode = "loop"
                fix_suffix = "{0}_loop".format(fix_suffix)
            else:
                ok, report = _judge_check(ticker, date)
        else:
            stage["short_fix_fallback"] = "patch map 回覆無法解析（ok={0}），改派 loop 修正 agent".format(r_fix.get("ok"))
            print("[judged] " + stage["short_fix_fallback"])
            fix_mode = "loop"
            fix_suffix = "{0}_loop".format(fix_suffix)
        if v19_one_shot_fix and fix_mode == "loop":
            # v19：patch map 是唯一一次修補機會，不回退 loop。
            stage["short_fix_fallback"] = (stage.get("short_fix_fallback") or "") \
                + "｜v19：patch map 上限 1 輪，不回退 loop，停下交指揮者"
            fix_mode = "stop"

    if not ok and fix_mode == "loop":
        fix_path = run_dir / "prompts" / "b1_fix.md"
        fix_text = (
            "你是 stock-analyst v17 判斷 agent，回來做一輪定點修正。標的 {0}（{1}）。\n\n"
            "`judge check` 的失敗原文如下，**只准改被點名的欄位**，改完一次 Write 整檔 "
            "`{2}`，重跑：\n\n"
            "```\npython3 scripts/ddreport.py judge check {0} {1}\n```\n\n"
            "≤1 輪；仍 FAIL 就照實回報。\n\n## judge check 失敗原文\n\n```\n{3}\n```\n"
        ).format(ticker, date, judgment_path, report)
        fix_path.write_text(fix_text, encoding="utf-8")
        if replay_dir:
            _append_replay_marker(fix_path, {
                "kind": "judgment", "judgment_out": str(judgment_path), "scenario_out": str(scenario_path),
            })
        r_spawn2 = dd_headless.spawn(
            prompt_path=fix_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
            max_turns=JUDGE_FIX_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
            out_json=agents_dir / "judge_fix_{0}.json".format(fix_suffix), cwd=run_dir,
        )
        stage["agent_usage"].append(r_spawn2)
        ok, report = _judge_check(ticker, date)

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget
    stage["check_report_tail"] = report[-4000:]
    j1_warn = None
    m = re.search(r"（(\d+) FAIL／(\d+) WARN）", report)
    if m:
        j1_warn = {"fail": int(m.group(1)), "warn": int(m.group(2))}
    stage["validate_summary"] = j1_warn

    final_ok = ok and (over_budget is False or accept_over_budget)
    stage["state"] = "PASS" if final_ok else ("OVER_BUDGET" if (ok and over_budget) else "FAIL")
    stage["ended"] = _now()
    manifest.setdefault("stages", {})["judged"] = stage
    manifest["state"] = "judged_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "judged", "ok={0} over_budget={1} validate={2}".format(ok, over_budget, j1_warn),
        "validate PASS", stage["state"],
    )
    if v19_one_shot_fix and not ok:
        # WP-H2-1：v19 用完一輪 patch map 仍 FAIL＝多半是缺判斷值，程式不准補、
        # 模型再想一次只會編一個。停在這裡、不發布，交指揮者裁定。
        print("[judged] **交指揮者**：v19 判斷物已用完一輪 patch map 仍未通過 "
              "judge check，不繼續往下跑、不發布。失敗原文見上方與 manifest 的 "
              "stages.judged.check_report_tail。", file=sys.stderr)
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "judged")
    return 0 if stage["state"] == "PASS" else 1


def _resume_judge_stage(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest):
    """WP7b #5：`--resume` 落在 `judged_fail`（或 judged 段先前狀態為
    FAIL）時的專用入口。判斷物可能已被機械層（`validate_judgment.py --fix`）
    或人工直接修正過，先重跑一次 `judge check`——PASS 就不再燒一次完整
    判斷 agent，直接把 judged 標成功；FAIL 才派一輪『定點修正』agent
    （沿用 `_judge_finalize_after_check` 的 fix 流程），仍然不重派整段判斷
    agent。見 notes/site-internal/dd/_wp_spec_v17_batch5_20260905.md WP7b #5。
    """
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = manifest.setdefault("stages", {}).get("judged") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    stage.setdefault("agent_usage", [])
    stage["resume_precheck"] = True
    agents_dir = run_dir / "agents"

    ok, report = _judge_check(ticker, date)
    if ok:
        stage["state"] = "PASS"
        stage["ended"] = _now()
        stage["check_report_tail"] = report[-4000:]
        stage["resume_note"] = "resume：judge check 免修即過（判斷物已由機械或人工修正），未派任何 agent"
        manifest["stages"]["judged"] = stage
        manifest["state"] = "judged_pass"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("judged", "resume judge check", "validate PASS", "PASS")
        return 0

    return _judge_finalize_after_check(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        agents_dir, ok, report, fix_suffix="resume",
    )


# ---------------------------------------------------------------------------
# WP1d gate：dd_gate.py／dd_brief.py 由 WP3／WP4a 並行交付。
# ---------------------------------------------------------------------------

def _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, _depth=0):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    dd_gate_path = SCRIPTS_DIR / "dd_gate.py"
    # 2026-09-06：既有「gated」stage（同一次 run 內的 _depth 遞迴、或
    # --resume 落回這裡）直接沿用同一物件、不重建——`agent_usage` 本來就
    # 累積在同一 list，不會漏記；只有完全沒有既有 stage 時才走
    # `_fresh_stage_preserving_prior`（此時 old 必空，等同純新建，回傳值不帶
    # `agent_usage_prior`），三段重建處理式維持一致。
    stage = manifest.setdefault("stages", {}).get("gated") or _fresh_stage_preserving_prior(manifest, "gated")
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_running"
    _atomic_write_json(manifest_path, manifest)

    if not dd_gate_path.exists():
        # 2026-09-07：v17 的 critic gate 是必要段，腳本遺失不可再以
        # SKIPPED 偽裝成功；保留失敗狀態供 --resume 修正後重跑。
        print("[error] scripts/dd_gate.py 不存在，critic gate 無法執行", file=sys.stderr)
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_gate.py missing"
        manifest["stages"]["gated"] = stage
        manifest["state"] = "gated_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "dd_gate.py missing", "腳本存在", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    py = _pick_python()
    rb = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_bundle.py"), "gate", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    if rb.returncode != 0:
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_bundle.py gate 失敗：{0}".format((rb.stdout + rb.stderr)[-1000:])
        manifest["stages"]["gated"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "bundle_rc={0}".format(rb.returncode), "PASS", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    audit_path = run_dir / "gate_audit.md"
    gate_bundle_path = run_dir / "bundles" / "gate.md"
    gate_prompt_path = run_dir / "prompts" / "g_gate.md"
    mapping = {
        "run_dir": str(run_dir), "bundle_path": str(gate_bundle_path),
        "ticker": ticker, "date": date, "audit_path": str(audit_path),
        "max_turns": str(GATE_MAX_TURNS),
    }
    gate_prompt_path.write_text(_render_format_template(PROMPTS_TMPL_DIR / "gate.md.tmpl", mapping), encoding="utf-8")
    if replay_dir:
        _append_replay_marker(gate_prompt_path, {"kind": "gate", "out": str(audit_path)})

    inline_gate_prompt_path = _write_inline_prompt(gate_prompt_path, gate_bundle_path)

    gate_model = GATE_MODEL_FOR.get(judgment_model, "opus")
    agents_dir = run_dir / "agents"
    r_spawn = dd_headless.spawn(
        prompt_path=inline_gate_prompt_path, model=gate_model, allowed_tools=["Read", "Write"],
        max_turns=GATE_MAX_TURNS, budget_cache_read=GATE_BUDGET_CACHE_READ,
        out_json=agents_dir / "gate_{0}.json".format(_depth + 1), cwd=run_dir,
    )
    stage["agent_usage"].append(r_spawn)
    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget

    if not audit_path.exists():
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "spawn 未產出 gate_audit.md"
        manifest["stages"]["gated"] = stage
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", "no_audit_file", "PASS", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    return _gate_finalize_from_audit(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage,
        audit_path, _depth=_depth,
    )


def _gate_finalize_from_audit(ticker, date, judgment_model, replay_dir, accept_over_budget,
                               manifest, stage, audit_path, _depth=0):
    """`gate_audit.md` 已存在（剛 spawn 產出，或 WP7b #5 `--resume` 在
    `gated_fail`／`gated_running` 時發現既有稽核檔）：parse 它、red>0 才派
    修補 agent（inline judgment.json 全文，不重跑一次 gate spawn），
    red=0 直接收斂為 PASS／OVER_BUDGET。"""
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    py = _pick_python()
    dd_gate_path = SCRIPTS_DIR / "dd_gate.py"
    agents_dir = run_dir / "agents"
    stage.setdefault("agent_usage", [])

    r_parse = subprocess.run(
        [py, str(dd_gate_path), "parse", str(audit_path), "--json"],
        capture_output=True, text=True,
    )
    parsed = None
    parse_error = None
    if r_parse.returncode != 0:
        parse_error = "parse rc={0}".format(r_parse.returncode)
    else:
        try:
            parsed = json.loads(r_parse.stdout)
        except (TypeError, ValueError) as exc:
            parse_error = "stdout 不是合法 JSON：{0}".format(exc)
        if parse_error is None and not isinstance(parsed, dict):
            parse_error = "stdout JSON 不是 dict"
        elif parse_error is None and "red" not in parsed:
            parse_error = "stdout JSON 缺少必要欄位 red"
        elif parse_error is None and (
                isinstance(parsed["red"], bool) or not isinstance(parsed["red"], int)):
            parse_error = "stdout JSON 的 red 不是整數"
    stage["gate_parsed"] = parsed

    if parse_error is not None:
        # 2026-09-07：parser 自身失敗或輸出契約損壞時必須 fail-closed；
        # 原始輸出保留尾端供定位，但不讓無法解析的結果退化成 red=0。
        raw_stdout = (r_parse.stdout or "")[-4000:]
        raw_stderr = (r_parse.stderr or "")[-4000:]
        print("[error] critic gate 解析失敗：{0}".format(parse_error), file=sys.stderr)
        print("[gate-parse] stdout：\n{0}".format(raw_stdout or "（空）"), file=sys.stderr)
        print("[gate-parse] stderr：\n{0}".format(raw_stderr or "（空）"), file=sys.stderr)
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "critic gate 解析失敗：{0}".format(parse_error)
        manifest["stages"]["gated"] = stage
        manifest["state"] = "gated_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("gated", parse_error, "合法 JSON dict 且含 red", "FAIL")
        _print_resume_hint(ticker, date, "gated")
        return 1

    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    red = parsed["red"]
    if red and red > 0:
        prior_verdict = _read_decision_verdict(run_dir)
        judgment_path = run_dir / "judgment.json"
        scenario_path = run_dir / "scenario.json"
        # 2026-09-06：閘 🔴 修補模式（patchmap／loop）——replay 模式一律 loop
        # （fake_claude.py 的 replay marker 目前只認 loop 那套逐輪腳本）。
        mode = "loop" if replay_dir else _gate_patch_mode()
        stage["gate_patch_mode"] = mode
        patched_by_map = False

        if mode == "patchmap":
            patch_short_path = run_dir / "prompts" / "b1_gate_patch_short.md"
            patch_short_path.write_text(
                _render_format_template(PROMPTS_TMPL_DIR / "gate_patch_short.md.tmpl", {
                    "ticker": ticker, "date": date,
                    "audit_text": audit_path.read_text(encoding="utf-8") if audit_path.exists() else "",
                    "judgment_compact": (
                        _compact_json_text(judgment_path.read_text(encoding="utf-8"))
                        if judgment_path.exists() else "{}"
                    ),
                    "scenario_compact": (
                        _compact_json_text(scenario_path.read_text(encoding="utf-8"))
                        if scenario_path.exists() else "{}"
                    ),
                    # 2026-09-11：閘 ⑧ 前份漂移歸因要看得到前份裁決與 rearm；
                    # v19 判斷包首跑漏帶 prior_dd，修補 agent 也得拿到才補得了。
                    "prior_compact": _compact_json_text(json.dumps(
                        (_load_json_or(run_dir / "evidence.json", {}) or {}).get("prior_dd") or {},
                        ensure_ascii=False)),
                }),
                encoding="utf-8",
            )
            r_fix = _spawn_oneshot(
                patch_short_path, judgment_model,
                agents_dir / "gate_patch_{0}.json".format(_depth + 1),
                run_dir, JUDGE_BUDGET_CACHE_READ,
            )
            stage["agent_usage"].append(r_fix)
            patches = (
                _parse_patch_map(r_fix.get("result_text"))
                if (r_fix.get("ok") and not r_fix.get("quota_exhausted")) else None
            )
            if patches is not None:
                n, errs = _apply_patch_map(run_dir, patches)
                stage["gate_patch_patch"] = {"applied": n, "errors": errs}
                print("[gate] patch map 套用 {0} 筆，錯誤 {1}".format(n, len(errs)))
                if errs and n == 0:
                    # 2026-09-06（FIX_20260908）：同判斷段——底檔解析失敗讓整批
                    # patch 一筆都沒套到，不能當作修過，直接回退 loop（`mode`
                    # 一併切回 loop，否則下面 `if mode == "loop"` 判斷會被跳過）。
                    stage["gate_patch_fallback"] = "patch map 全數未套用（errors={0}），改派 loop 修補 agent".format(errs)
                    print("[gate] " + stage["gate_patch_fallback"])
                    mode = "loop"
                else:
                    patched_by_map = True
            else:
                stage["gate_patch_fallback"] = "patch map 回覆無法解析（ok={0}），改派 loop 修補 agent".format(
                    r_fix.get("ok"))
                print("[gate] " + stage["gate_patch_fallback"])
                mode = "loop"

        if mode == "loop" and not patched_by_map:
            patch_prompt_path = run_dir / "prompts" / "b1_patch.md"
            rp = subprocess.run(
                [py, str(dd_gate_path), "patch-prompt",
                 "--audit", str(audit_path), "--judgment", str(judgment_path),
                 "--evidence", str(run_dir / "evidence.json"), "--out", str(patch_prompt_path)],
                capture_output=True, text=True,
            )
            if rp.returncode != 0 or not patch_prompt_path.exists():
                stage["state"] = "FAIL"
                stage["ended"] = _now()
                stage["note"] = "dd_gate.py patch-prompt 失敗：{0}".format((rp.stdout + rp.stderr)[-1000:])
                manifest["stages"]["gated"] = stage
                _atomic_write_json(manifest_path, manifest)
                _print_step_status("gated", "patch_prompt_rc={0}".format(rp.returncode), "PASS", "FAIL")
                _print_resume_hint(ticker, date, "gated")
                return 1
            if replay_dir:
                _append_replay_marker(patch_prompt_path, {
                    "kind": "judgment", "judgment_out": str(judgment_path),
                })
            inline_patch_prompt_path = _write_inline_prompt(patch_prompt_path, judgment_path)
            r_spawn2 = dd_headless.spawn(
                prompt_path=inline_patch_prompt_path, model=judgment_model, allowed_tools=["Read", "Write", "Bash"],
                max_turns=GATE_PATCH_MAX_TURNS, budget_cache_read=JUDGE_BUDGET_CACHE_READ,
                out_json=agents_dir / "gate_patch_{0}.json".format(_depth + 1), cwd=run_dir,
            )
            stage["agent_usage"].append(r_spawn2)

        over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
        stage["over_budget"] = over_budget

        ok_check, report_check = _judge_check(ticker, date)
        stage["patch_check_tail"] = report_check[-3000:]
        new_verdict = _read_decision_verdict(run_dir)

        if new_verdict != prior_verdict and _depth < 1:
            manifest["stages"]["gated"] = stage
            _atomic_write_json(manifest_path, manifest)
            print("[gate] verdict 翻面（{0} → {1}），重跑一次 gate".format(prior_verdict, new_verdict))
            return _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, _depth=_depth + 1)

        final_ok = ok_check and (over_budget is False or accept_over_budget)
        stage["state"] = "PASS" if final_ok else ("OVER_BUDGET" if (ok_check and over_budget) else "FAIL")
    else:
        stage["over_budget"] = over_budget
        final_ok = (over_budget is False) or accept_over_budget
        stage["state"] = "PASS" if final_ok else "OVER_BUDGET"

    stage["ended"] = _now()
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_{0}".format(stage["state"].lower())
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "gated", "red={0} yellow={1} over_budget={2}".format(
            (parsed or {}).get("red"), (parsed or {}).get("yellow"), stage["over_budget"]),
        "red=0", stage["state"],
    )
    if stage["state"] != "PASS":
        _print_resume_hint(ticker, date, "gated")
    return 0 if stage["state"] == "PASS" else 1


def _resume_gate_stage(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest):
    """WP7b #5：`--resume` 落在 `gated_fail`／`gated_running` 時的專用入口。
    既有 `gate_audit.md` 可能是上一輪已經跑完的稽核結果（只是後續
    parse／patch 步驟中斷），先直接 parse 它，不重新花一次 gate spawn；
    parse 不到（audit 檔不存在）才退回完整 `_do_gate`。"""
    run_dir = _run_dir(ticker, date)
    audit_path = run_dir / "gate_audit.md"
    if not audit_path.exists():
        return _do_gate(ticker, date, judgment_model, replay_dir, accept_over_budget, manifest)

    stage = manifest.setdefault("stages", {}).get("gated") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    stage.setdefault("agent_usage", [])
    stage["resume_precheck"] = True
    manifest["stages"]["gated"] = stage
    manifest["state"] = "gated_running"
    _atomic_write_json(run_dir / "manifest.json", manifest)

    return _gate_finalize_from_audit(
        ticker, date, judgment_model, replay_dir, accept_over_budget, manifest, stage, audit_path,
    )


# ---------------------------------------------------------------------------
# WP1d brief：dd_brief.py（WP4a 交付）零 LLM 渲染。
# 2026-09-07：快速版為必經產物，renderer 缺失須 fail-closed。
# ---------------------------------------------------------------------------

def _do_brief(ticker, date, do_full, manifest, dry_run=False):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    dd_brief_path = SCRIPTS_DIR / "dd_brief.py"
    stage = {"state": "RUNNING", "started": _now()}
    manifest.setdefault("stages", {})["brief"] = stage
    manifest["state"] = "brief_running"
    _atomic_write_json(manifest_path, manifest)

    if not dd_brief_path.exists():
        # 2026-09-07：快速版是 v17 預設產物，renderer 遺失不可用
        # SKIPPED 偽裝成功；留下 FAIL 供修正檔案後重跑。
        print("[error] scripts/dd_brief.py 不存在，快速版無法產出", file=sys.stderr)
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "dd_brief.py missing"
        manifest["stages"]["brief"] = stage
        manifest["state"] = "brief_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("brief", "dd_brief.py missing", "腳本存在", "FAIL")
        _print_resume_hint(ticker, date, "brief")
    else:
        py = _pick_python()
        # WP7a #6：--dry-run 時輸出到 run 目錄內的 brief.html，不寫
        # docs/dd/brief/（避免 dry-run 汙染會上站/被 git 追蹤的目錄）。
        if dry_run:
            out_path = run_dir / "brief.html"
        else:
            out_path = REPO_ROOT / "docs" / "dd" / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            [py, str(dd_brief_path), "--run-dir", str(run_dir), "--out", str(out_path)],
            capture_output=True, text=True,
        )
        stage["out_path"] = str(out_path)
        stage["state"] = "PASS" if r.returncode == 0 else "FAIL"
        stage["ended"] = _now()
        stage["note"] = (r.stdout + r.stderr)[-1000:]
        manifest["stages"]["brief"] = stage
        manifest["state"] = "brief_{0}".format(stage["state"].lower())
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("brief", "rc={0}".format(r.returncode), "PASS", stage["state"])
        if stage["state"] != "PASS":
            _print_resume_hint(ticker, date, "brief")

    # 2026-09-06：`--full` 完整版現由獨立的 `prose` 段負責（見下方 WP4b），
    # 不再是這裡的旁支——`do_full` 參數保留給呼叫端相容（`cmd_run`／`brief`
    # 子命令與既有測試皆仍傳這個位置參數），本函式對它不再做任何事。
    del do_full

    return 0 if stage["state"] == "PASS" else 1


# ---------------------------------------------------------------------------
# WP4b（2026-09-06）：散文層（`--full` 完整版）
#
# `prose prepare` — 生成 C-1 機械段（revlog／s14／appA）到 run_dir/prose/、
#   跑 gen_dd_tables.py 產表、組 bundles/prose.md、寫 prompts/b2_prose.md。
# `prose split`   — 把 prose_A.html／prose_B.html（＋補寫輪的 prose_fix.html）
#   依 `<!-- SID:sX -->` 標記切成 prose/{sid}.html；機械段不被覆寫；decision
#   段落地後在 `<!-- E12 -->` 標記後接一句機械說明（`render_e12_note_html`）。
# `gates`         — `dd_gates.sh` 六支驗證的 Python 化版本，回 (ok, [(sid,
#   原因)])，供 `prose check` 與最終定案組裝共用。
# `prose check`   — split ＋ gates 一次跑完，給散文 agent 自己在 Bash 裡呼叫。
# `prose run`     — spawn 散文 agent（sonnet／Write,Bash／≤7 輪／預算 1.5M）
#   → check → PASS 時組出 docs/dd/DD_{T}_{D}.html。
# ---------------------------------------------------------------------------

def _do_prose_prepare(ticker, date):
    """`prose prepare TICKER DATE`：C-1 機械段 → gen_dd_tables 產表 →
    bundles/prose.md → prompts/b2_prose.md。可重複呼叫（每步驟都是覆寫式，
    非累加），供 `prose run` 在 bundle／prompt 不存在時自動補跑一次。"""
    run_dir = _run_dir(ticker, date)
    judgment_path = run_dir / "judgment.json"
    evidence_path = run_dir / "evidence.json"
    scenario_meta_path = run_dir / "scenario_meta.json"
    tables_dir = run_dir / "tables"
    prose_dir = run_dir / "prose"
    py = _pick_python()

    if not judgment_path.exists():
        print("[error] 找不到 {0}".format(judgment_path), file=sys.stderr)
        return 1

    tables_dir.mkdir(parents=True, exist_ok=True)
    gen_cmd = [
        py, str(SCRIPTS_DIR / "gen_dd_tables.py"), str(judgment_path),
        "--out", str(tables_dir),
        "--scenario-html", str(tables_dir / "e11.html"),
    ]
    if scenario_meta_path.exists():
        gen_cmd += ["--scenario-meta", str(scenario_meta_path)]
    r1 = subprocess.run(gen_cmd, capture_output=True, text=True)
    if r1.returncode != 0:
        print("[error] gen_dd_tables.py 失敗：\n{0}".format((r1.stdout + r1.stderr)[-1000:]), file=sys.stderr)
        return 1
    print(r1.stdout.strip())

    # C-1 機械段（revlog／s14／appA）——直接 import 呼叫（見檔頭 `import
    # gen_dd_tables as gdt`），不另外幫 gen_dd_tables.py 的 CLI 加旗標。
    judgment = _load_json(judgment_path)
    evidence = _load_json_or(evidence_path, {})
    # 2026-09-07：完整版 revlog 必須拿到 scenario_meta，不能再只讀 null judgment。
    scenario_meta = _load_json_or(scenario_meta_path, {})
    written_mech = gdt.write_mechanical_prose(
        judgment, evidence.get("prior_dd"), prose_dir, scenario_meta=scenario_meta)
    print("[ok] C-1 機械段：{0}".format(", ".join(written_mech)))

    bundle_path = run_dir / "bundles" / "prose.md"
    r2 = subprocess.run(
        [py, str(SCRIPTS_DIR / "dd_bundle.py"), "prose", "--run-dir", str(run_dir)],
        capture_output=True, text=True,
    )
    if r2.returncode != 0:
        print("[error] dd_bundle.py prose 失敗：\n{0}".format((r2.stdout + r2.stderr)[-1000:]), file=sys.stderr)
        return 1
    print(r2.stdout.strip())

    prompt_path = run_dir / "prompts" / "b2_prose.md"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    mapping = {
        "ticker": ticker, "date": date, "max_turns": str(PROSE_MAX_TURNS),
        "check_cmd": "python3 scripts/ddreport.py prose check {0} {1}".format(ticker, date),
        "prose_a_path": str(run_dir / "prose_A.html"),
        "prose_b_path": str(run_dir / "prose_B.html"),
        "prose_fix_path": str(run_dir / "prose_fix.html"),
    }
    prompt_path.write_text(_render_format_template(PROMPTS_TMPL_DIR / "prose.md.tmpl", mapping), encoding="utf-8")
    print("[ok] prose prepare 完成：bundle={0}／prompt={1}".format(bundle_path, prompt_path))
    return 0


def cmd_prose_prepare(args):
    return _do_prose_prepare(args.ticker.strip().upper(), args.date)


_SID_MARKER_RE = re.compile(r"<!--\s*SID:([A-Za-z0-9]+)\s*-->")


def _split_sid_markers(text):
    """把含 `<!-- SID:sX -->` 標記的文字切成 {sid: chunk}——chunk 不含標記
    本身，從標記結尾到下一個標記（或檔尾）之間的內容，去頭尾換行。"""
    matches = list(_SID_MARKER_RE.finditer(text))
    out = {}
    for i, m in enumerate(matches):
        sid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[start:end].strip("\n")
        if chunk.strip():
            out[sid] = chunk + "\n"
    return out


def _inject_e12_note(run_dir, prose_dir):
    """decision 段仍是散文 agent 寫的，但 `<!-- E12 -->` 標記之後那句機械
    說明（觸發器件數／重啟條件）由這裡接線注入——`<!-- E12_NOTE -->` 是
    冪等 guard，重跑 split 不會疊加第二次。"""
    decision_path = prose_dir / "decision.html"
    if not decision_path.exists():
        return
    text = decision_path.read_text(encoding="utf-8")
    if "<!-- E12 -->" not in text or "<!-- E12_NOTE -->" in text:
        return
    judgment = _load_json_or(run_dir / "judgment.json", {})
    note_html = gdt.render_e12_note_html(judgment)
    text = text.replace("<!-- E12 -->", "<!-- E12 -->\n<!-- E12_NOTE -->\n" + note_html, 1)
    decision_path.write_text(text, encoding="utf-8")


def _do_prose_split(ticker, date):
    """回傳 (written_sids, errors)。依序處理 `_PROSE_SOURCE_FILES`（prose_A
    → prose_B → prose_fix，若存在）——同一 sid 後面的檔覆蓋前面的，讓 FAIL
    後的補寫輪只需要 Write 一個小的 `prose_fix.html`。機械段
    （`_PROSE_MECHANICAL_SIDS`）只在 `prose/{sid}.html` **已經存在**（即
    `prose prepare` 的 `gdt.write_mechanical_prose` 已生成）時才拒絕覆寫、
    記一筆警告；尚未存在時仍照樣寫入——這讓 split 本身是一支不失真的純
    SID-marker 切割器（回溯考卷需要「合併再切回去逐位元組相同」），保護的
    是「不被散文 agent 事後蓋掉機械產物」，不是「這三個 sid 永遠不能來自
    A/B/fix 檔」。"""
    run_dir = _run_dir(ticker, date)
    prose_dir = run_dir / "prose"
    prose_dir.mkdir(parents=True, exist_ok=True)

    written, errors = [], []
    any_source = False
    for name in _PROSE_SOURCE_FILES:
        p = run_dir / name
        if not p.exists():
            continue
        any_source = True
        chunks = _split_sid_markers(p.read_text(encoding="utf-8"))
        for sid, chunk in chunks.items():
            dest = prose_dir / "{0}.html".format(sid)
            if sid in _PROSE_MECHANICAL_SIDS and dest.exists():
                errors.append("{0}：機械段已存在，忽略 {1} 內寫入的內容".format(sid, name))
                continue
            dest.write_text(chunk, encoding="utf-8")
            if sid not in written:
                written.append(sid)
    if not any_source:
        errors.append("找不到 prose_A.html／prose_B.html，split 無來源可切")
    if "decision" in written:
        _inject_e12_note(run_dir, prose_dir)
    return written, errors


def cmd_prose_split(args):
    written, errors = _do_prose_split(args.ticker.strip().upper(), args.date)
    print("[split] 寫入 {0} 段：{1}".format(len(written), ", ".join(written) if written else "（無）"))
    for e in errors:
        print("[warn] " + e)
    return 0 if not errors else 1


def _sid_for_line(html_text, lineno, markers):
    for mk in markers:
        start_line = html_text.count("\n", 0, mk["start"]) + 1
        end_line = html_text.count("\n", 0, mk["end"]) + 1
        if start_line <= lineno <= end_line:
            return mk["id"]
    return None


def _run_gates(run_dir, ticker, date, out_html=None, postprocess=False):
    """`dd_gates.sh` 的 Python 化版本（見設計稿 §3.5／§8 C-1）：render_dd
    組裝 → validate_prose（依 sid 歸因）→ dd_sections leaks（依行號歸因到
    sid）→ dd_sections bytes（WARN 不擋，只印不回報）→ qc → validate_dd_meta
    （診斷用，不擋）→ verify_dd_math。回傳 `(ok, [(sid, 原因), ...])`——
    無法歸因到特定 sid 的失敗用 `_assemble`／`_validate_prose`／`_qc`／
    `_math` 這類前綴 sid 代替（機械層或跨段問題，散文 agent 改不動）。"""
    run_dir = Path(run_dir)
    py = _pick_python()
    prose_dir = run_dir / "prose"
    tables_dir = run_dir / "tables"
    judgment_path = run_dir / "judgment.json"
    evidence_path = run_dir / "evidence.json"
    out_path = Path(out_html) if out_html else run_dir / "DD_preview.html"

    findings = []
    ok = True

    assemble_cmd = [
        py, str(SCRIPTS_DIR / "render_dd.py"), "--assemble", str(prose_dir),
        "--tables", str(tables_dir), "--judgment", str(judgment_path),
        "-o", str(out_path),
    ]
    # WP-H2-3（2026-09-11）：正式流程對 v19 判斷檔組頁時要傳 `--layout v19`——
    # H2-2 把新版面做出來了但這條呼叫沒接上，v19 run 會靜靜地組成舊版面（既有
    # 檔案都在、不會報錯，只是頁首五張卡與 24 格全部不見）。判別看**判斷檔實際
    # 的 contract**，與 `_judge_check` 同一條原則：replay 重放舊 fixture 仍走舊版面。
    if judgment_path.exists():
        try:
            if dd_project.is_v19(_load_json(judgment_path)):
                assemble_cmd += ["--layout", "v19"]
        except (json.JSONDecodeError, ValueError):
            pass
    if not postprocess:
        assemble_cmd.append("--no-postprocess")
    r_asm = subprocess.run(assemble_cmd, capture_output=True, text=True)
    if r_asm.returncode != 0:
        findings.append(("_assemble", (r_asm.stdout + r_asm.stderr).strip()[-500:]))
        return False, findings

    vp_cmd = [py, str(SCRIPTS_DIR / "validate_prose.py"), str(prose_dir),
              "--judgment", str(judgment_path), "--json"]
    if evidence_path.exists():
        vp_cmd += ["--evidence", str(evidence_path)]
    r_vp = subprocess.run(vp_cmd, capture_output=True, text=True)
    try:
        vp_json = json.loads(r_vp.stdout) if r_vp.stdout.strip() else None
    except (json.JSONDecodeError, ValueError):
        vp_json = None
    if vp_json is None:
        ok = False
        findings.append(("_validate_prose", (r_vp.stdout + r_vp.stderr).strip()[-500:]))
    else:
        for sid, misses in (vp_json.get("by_section") or {}).items():
            sample = "；".join("{0}（{1}）".format(m.get("raw"), m.get("context")) for m in misses[:3])
            findings.append((sid, "validate_prose：{0} 個未覆蓋數字：{1}".format(len(misses), sample)))
        if vp_json.get("total_uncovered"):
            ok = False

    out_html_text = out_path.read_text(encoding="utf-8") if out_path.exists() else ""

    hits = dd_sections.leak_hits(out_html_text) if out_html_text else []
    if hits:
        ok = False
        markers = dd_sections.split_sections(out_html_text)
        for lineno, word, ctx in hits:
            sid = _sid_for_line(out_html_text, lineno, markers) or "_global"
            findings.append((sid, "leaks：{0}（…{1}…）".format(word, ctx)))

    # bytes：既有 WARN 慣例（不擋，只給人看），這裡跑一次只為了留在 stdout
    # 讓呼叫端（人工核對）看得到，不納入 ok 判定、不進 findings。
    subprocess.run([py, str(SCRIPTS_DIR / "dd_sections.py"), "bytes", str(out_path)],
                   capture_output=True, text=True)

    # 2026-09-08：帶 --escalate——不加的話 `qc.py FILE` 屬 explicit 範圍、
    # 一律不把新增行的違規升級成 error，這道閘結構上不可能失敗（TXN
    # 20260907 實例：513 個中文後接半形標點一路綠燈到 pre-push 才被擋）。
    r_qc = subprocess.run([py, str(SCRIPTS_DIR / "qc.py"), "--escalate", str(out_path)],
                          capture_output=True, text=True)
    if r_qc.returncode != 0:
        ok = False
        findings.append(("_qc", (r_qc.stdout + r_qc.stderr).strip()[-500:]))

    # validate_dd_meta：診斷用 --report，同既有慣例不擋。
    subprocess.run([py, str(SCRIPTS_DIR / "validate_dd_meta.py"), str(out_path), "--report"],
                   capture_output=True, text=True)

    r_math = subprocess.run([py, str(SCRIPTS_DIR / "verify_dd_math.py"), str(out_path)],
                             capture_output=True, text=True)
    if r_math.returncode != 0:
        ok = False
        findings.append(("_math", (r_math.stdout + r_math.stderr).strip()[-500:]))

    return ok, findings


def cmd_gates(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    run_dir = _run_dir(ticker, date)
    ok, findings = _run_gates(run_dir, ticker, date, out_html=args.out, postprocess=args.postprocess)
    print("PASS" if ok else "FAIL")
    for sid, reason in findings:
        print("- {0}：{1}".format(sid, reason))
    return 0 if ok else 1


# 2026-09-08：散文段只有上限閘，沒有下限閘——`dd_sections.py bytes` 對
# 單一預算段是 `WARN if nbytes > budget else OK`，寫到目標的兩成也是 OK，
# 整檔下限也只是 WARN。唯一會擋的是 pre-commit 的 70KB 深度閘，但那在
# 錢與時間都花完之後才響（TXN 20260907 實跑：散文交出 61,280B，s5 寫
# 2,592B／目標 7,558-10,797B，s6 寫 1,405B／目標 7,451-10,645B，全段
# 顯示 OK，commit 才被擋）。CLAUDE.md 的設計意圖是「下界＝深度閘門（擋）、
# 上界＝成本預算（只警告）」，這裡把缺的那一半補上，讓散文 agent 在自己
# 的修補回合內就看得到，而不是留給 commit 才擋。
# 機械段（revlog／s14／appA）由腳本生成、agent 不寫，不列入本閘。
_PROSE_MECHANICAL_SIDS = ("revlog", "s14", "appA")


def _is_v19_layout(html_path) -> bool:
    """組裝出來的頁面是不是 v19 版面。判別看**產物自己**的 `dd-layout` meta
    （`scripts/dd_templates/v19.html` 寫的），不看流程預期——與 `_judge_check`
    的判別原則一致：replay 重放舊 fixture 時該走舊路徑就走舊路徑。"""
    try:
        head = Path(html_path).read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return False
    return 'name="dd-layout" content="v19"' in head


def _v19_structure_findings(run_dir, preview):
    """跑 `scripts/validate_report_v19.py --json`，把 findings 原樣轉成
    `(sid, 原因)`。腳本本身跑不起來時回一條 `_v19_structure` 的 finding——
    **不靜默放行**：驗收閘跑不動和驗收不過一樣要擋。"""
    run_dir = Path(run_dir)
    cmd = [_pick_python(), str(SCRIPTS_DIR / "validate_report_v19.py"), str(preview),
           "--judgment", str(run_dir / "judgment.json"), "--json"]
    for flag, name in (("--facts", "facts.json"), ("--scenario-meta", "scenario_meta.json")):
        if (run_dir / name).exists():
            cmd += [flag, str(run_dir / name)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        payload = json.loads(r.stdout) if r.stdout.strip() else None
    except (json.JSONDecodeError, ValueError):
        payload = None
    if payload is None:
        return [("_v19_structure", "v19 結構驗收跑不起來：{0}".format(
            (r.stdout + r.stderr).strip()[-400:]))]
    return [(f.get("sid") or "_v19_structure", "v19 結構驗收：" + str(f.get("reason")))
            for f in (payload.get("findings") or [])]


def _prose_depth_findings(run_dir, ticker, date):
    """回傳 [(sid, reason), ...]：整檔深度未達發布底線時擋下，並附偏低段清單。

    2026-09-08 二次修正：門檻直接用 `scripts/hooks/pre-commit` 的 v15 DD
    hard floor（70000B，見該檔 `check_report_size "$f" 70000 ...`），量的是
    `_run_gates()` 剛組裝出來的 `DD_preview.html`——也就是**真正要上站的那
    份檔**。

    前一版把門檻設成「各段 prose_target_lo 的總和」（45394B），那是我自己
    發明的、比發布標準嚴得多的線：TXN 實測散文 42156B → 組裝後 77671B，
    早就過了 70000B floor、也在 75-105KB 帶內，卻仍被擋。**in-loop 的閘不
    該比發布閘嚴**，否則會逼出為了過閘而生的重跑與灌水，正是 CLAUDE.md
    QC-38 明講要避免的事。各段 prose_target_lo 仍拿來列「偏低段」當寫作
    指引，但不再單獨構成阻斷。
    """
    preview = Path(run_dir) / "DD_preview.html"
    if not preview.exists():
        return []  # 組裝失敗由 _run_gates 的 _assemble finding 負責回報

    # WP-H2-3（2026-09-11，Codex 裁定 3）：v19 版面改走**結構與內容驗收**，
    # 不用 bytes。v19 的散文是條列白話（lead ≤40 字＋2–6 條短條列），寫得好反
    # 而短；沿用 70KB 整檔 floor 只會逼出灌水。70KB floor 留給 legacy 版面。
    if _is_v19_layout(preview):
        return _v19_structure_findings(run_dir, preview)

    total = preview.stat().st_size
    if total >= DD_FULL_FLOOR_BYTES:
        return []

    # 只有真的沒過底線時才去算偏低段，給 agent 指出該補哪幾章。
    shortfalls = []
    judgment = _load_json_or(Path(run_dir) / "judgment.json", None)
    tables_dir = Path(run_dir) / "tables"
    if isinstance(judgment, dict) and tables_dir.exists():
        try:
            rows = dd_prose_budget.build_rows(tables_dir, judgment)
        except Exception:
            rows = []
        for row in rows:
            sid = row.get("section")
            lo = row.get("prose_target_lo")
            if not sid or lo is None or sid in _PROSE_MECHANICAL_SIDS:
                continue
            path = Path(run_dir) / "prose" / "{0}.html".format(sid)
            nbytes = path.stat().st_size if path.exists() else 0
            if nbytes < lo:
                shortfalls.append("{0} {1}B<{2}B".format(sid, nbytes, lo))
    detail = "；偏低段：" + "、".join(shortfalls) if shortfalls else ""
    return [("prose-depth",
             "整檔深度不足：{0}B < 發布底線 {1}B（差 {2}B）{3}"
             "——把 reasoning 裡已推導但沒寫進正文的內容補上，不要灌水填充句".format(
                 total, DD_FULL_FLOOR_BYTES, DD_FULL_FLOOR_BYTES - total, detail))]


def _prose_check(ticker, date):
    """`prose check TICKER DATE`＝split＋gates 一次跑完，輸出只有 sid 清單
    ＋原因（不吐六支腳本全文）——散文 agent 在自己的 Bash 呼叫裡用這支。"""
    written, split_errors = _do_prose_split(ticker, date)
    run_dir = _run_dir(ticker, date)
    ok, findings = _run_gates(run_dir, ticker, date)
    # 2026-09-08：深度下限與既有六支閘併列，同樣以 sid 歸因，讓 agent 的
    # 那一輪修補能一起處理。
    depth_findings = _prose_depth_findings(run_dir, ticker, date)
    if depth_findings:
        ok = False
        findings = list(findings) + depth_findings
    lines = []
    if split_errors:
        for e in split_errors:
            lines.append("[split] " + e)
    if ok and not split_errors:
        lines.append("PASS")
    else:
        lines.append("FAIL")
        for sid, reason in findings:
            lines.append("- {0}：{1}".format(sid, reason))
    return (ok and not split_errors), "\n".join(lines)


def cmd_prose_check(args):
    ok, report = _prose_check(args.ticker.strip().upper(), args.date)
    print(report)
    return 0 if ok else 1


def _resume_prose_stage(ticker, date, manifest, accept_over_budget=False, dry_run=False):
    """2026-09-08：`--resume` 落在 prose FAIL 時，先跑一次零成本的
    `prose check`——過了就直接標 PASS，不重派散文 agent。

    比照 `_resume_judge_stage` 既有做法（判斷段與閘段早有這條路徑，散文段
    當時漏了）。實際代價：TXN 20260907 的散文本身合格，只是被一條設得比
    發布標準更嚴的 in-loop 閘擋下；閘修好後若沒有這條 precheck，resume 會
    再燒一次完整散文 agent（約 $1／17 分）去重寫一份已經可用的稿。
    """
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = manifest.setdefault("stages", {}).get("prose") or {
        "state": "RUNNING", "started": _now(), "agent_usage": [], "over_budget": False,
    }
    stage.setdefault("agent_usage", [])
    stage["resume_precheck"] = True

    ok, report = _prose_check(ticker, date)
    if not ok:
        print("[prose] resume precheck 未過，改派散文 agent：")
        print(report)
        return _do_prose_run(ticker, date, manifest,
                             accept_over_budget=accept_over_budget, dry_run=dry_run)

    out_html = DD_DIR / "DD_{0}_{1}.html".format(ticker, date)
    rc_render, findings = _run_gates(run_dir, ticker, date, out_html=str(out_html),
                                     postprocess=True)
    if not rc_render:
        print("[prose] resume precheck 過，但最終組裝仍有問題：")
        for sid, reason in findings:
            print("- {0}：{1}".format(sid, reason))
        return _do_prose_run(ticker, date, manifest,
                             accept_over_budget=accept_over_budget, dry_run=dry_run)

    stage["state"] = "PASS"
    stage["ended"] = _now()
    stage["out_path"] = str(out_html)
    stage["resume_note"] = "resume：prose check 免修即過（現有散文已合格），未派任何 agent"
    manifest["stages"]["prose"] = stage
    manifest["state"] = "prose_pass"
    _atomic_write_json(manifest_path, manifest)
    print("[ok] 完整版（resume 免重寫）：{0}".format(out_html))
    _print_step_status("prose", "resume prose check", "PASS", "PASS")
    return 0


def _do_prose_run(ticker, date, manifest, accept_over_budget=False, dry_run=False):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    stage = _fresh_stage_preserving_prior(manifest, "prose")
    manifest.setdefault("stages", {})["prose"] = stage
    manifest["state"] = "prose_running"
    _atomic_write_json(manifest_path, manifest)

    bundle_path = run_dir / "bundles" / "prose.md"
    prompt_path = run_dir / "prompts" / "b2_prose.md"
    if not bundle_path.exists() or not prompt_path.exists():
        rc = _do_prose_prepare(ticker, date)
        if rc != 0:
            stage["state"] = "FAIL"
            stage["ended"] = _now()
            stage["note"] = "prose prepare 失敗（rc={0}）".format(rc)
            manifest["stages"]["prose"] = stage
            manifest["state"] = "prose_fail"
            _atomic_write_json(manifest_path, manifest)
            _print_step_status("prose", "prepare_rc={0}".format(rc), "PASS", "FAIL")
            _print_resume_hint(ticker, date, "prose")
            return 1

    agents_dir = run_dir / "agents"
    inline_prompt_path = _write_inline_prompt(prompt_path, bundle_path)
    r_spawn = _spawn_short(
        inline_prompt_path, "sonnet", agents_dir / "prose_1.json",
        run_dir, PROSE_BUDGET_CACHE_READ, PROSE_MAX_TURNS,
    )
    stage["agent_usage"].append(r_spawn)
    over_budget = any(r.get("over_budget") for r in stage["agent_usage"])
    stage["over_budget"] = over_budget
    _atomic_write_json(manifest_path, manifest)

    if r_spawn.get("quota_exhausted"):
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "訂閱額度耗盡"
        manifest["stages"]["prose"] = stage
        manifest["state"] = "prose_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("prose", "quota_exhausted", "PASS", "FAIL")
        _print_resume_hint(ticker, date, "prose")
        return 1

    ok, report = _prose_check(ticker, date)
    stage["check_report"] = report

    final_ok = ok and (over_budget is False or accept_over_budget)
    if not ok:
        stage["state"] = "FAIL"
    elif over_budget and not accept_over_budget:
        stage["state"] = "OVER_BUDGET"
    else:
        stage["state"] = None  # 下面組最終 HTML 後才定案

    if not final_ok:
        stage["ended"] = _now()
        manifest["stages"]["prose"] = stage
        manifest["state"] = "prose_{0}".format(stage["state"].lower())
        _atomic_write_json(manifest_path, manifest)
        _print_step_status(
            "prose", "cache_read={0}".format(r_spawn.get("cache_read")),
            PROSE_BUDGET_CACHE_READ, stage["state"],
        )
        if stage["state"] == "FAIL":
            print(report)
        _print_resume_hint(ticker, date, "prose")
        return 1

    # PASS：組出最終定案 HTML（`--dry-run` 落在 run 目錄內，不寫 docs/）。
    if dry_run:
        out_path = run_dir / "DD_full_preview.html"
    else:
        out_path = DD_DIR / "DD_{0}_{1}.html".format(ticker, date)
    ok2, findings2 = _run_gates(run_dir, ticker, date, out_html=out_path, postprocess=not dry_run)
    if not ok2:
        stage["state"] = "FAIL"
        stage["ended"] = _now()
        stage["note"] = "最終定案組裝 FAIL：{0}".format(findings2)
        manifest["stages"]["prose"] = stage
        manifest["state"] = "prose_fail"
        _atomic_write_json(manifest_path, manifest)
        _print_step_status("prose", "final_assemble FAIL", "PASS", "FAIL")
        _print_resume_hint(ticker, date, "prose")
        return 1

    stage["state"] = "PASS"
    stage["ended"] = _now()
    stage["out_path"] = str(out_path)
    manifest["stages"]["prose"] = stage
    manifest["state"] = "prose_pass"
    _atomic_write_json(manifest_path, manifest)
    _print_step_status(
        "prose", "cache_read={0}".format(r_spawn.get("cache_read")), PROSE_BUDGET_CACHE_READ, "PASS",
    )
    print("[ok] 完整版：{0}".format(out_path))
    return 0


def cmd_prose_run(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
        "ticker": ticker, "date": date, "state": "new", "created": _now(),
        "steps": [], "agents": [], "stages": {},
    })
    return _do_prose_run(ticker, date, manifest, accept_over_budget=getattr(args, "accept_over_budget", False),
                          dry_run=args.dry_run)


_PROSE_HELP = (
    "usage: ddreport.py prose {prepare,split,check,run} TICKER DATE [--dry-run] [--accept-over-budget]\n\n"
    "  prepare  產生 C-1 機械段（revlog／s14／appA）到 run 目錄 prose/，\n"
    "           跑 gen_dd_tables.py 產表，組 bundles/prose.md、prompts/b2_prose.md。\n"
    "  split    把 prose_A.html／prose_B.html（／prose_fix.html，補寫輪）依\n"
    "           <!-- SID:sX --> 標記切成 prose/{sid}.html（機械段不覆寫）。\n"
    "  check    split ＋ gates 一次跑完，只回 sid 清單＋原因（散文 agent 用）。\n"
    "  run      spawn 散文 agent（sonnet，Write/Bash，≤7 輪，預算 1.5M cache_read，\n"
    "           熔斷 3.0M）→ check → PASS 時組出 docs/dd/DD_{T}_{D}.html\n"
    "           （--dry-run 時輸出到 run 目錄內、不寫 docs/）。\n"
)


# ---------------------------------------------------------------------------
# WP6a: index-row — 從最終 HTML 的 dd-meta 生成 docs/dd/INDEX.md 一列
# ---------------------------------------------------------------------------

_DD_META_RE = re.compile(
    r'<script id="dd-meta"[^>]*>(.*?)</script>', re.S
)
_SUB_P_RE = re.compile(r'<p class="sub[^"]*">(.*?)</p>', re.S)
_TAG_RE = re.compile(r"<[^>]+>")


def _extract_dd_meta(html_text):
    m = _DD_META_RE.search(html_text)
    if not m:
        raise ValueError("dd-meta script block 找不到")
    return json.loads(m.group(1))


def _extract_sub_text(html_text):
    """取 `<p class="sub...">…</p>`（`dd_brief.py render_header` 已把
    `plain.verdict_sub`（有）或 `oneliner`（無，class 多帶 fallback）決定好
    優先序寫進這段），HTML entity 反轉義＋防禦性剝標籤。"""
    m = _SUB_P_RE.search(html_text)
    if not m:
        return None
    text = html_lib.unescape(m.group(1))
    text = _TAG_RE.sub("", text)
    return text.strip()


def _fmt_signed_pct(v, decimals=1):
    if v is None:
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    sign = "+" if v > 0 else ("−" if v < 0 else "")
    return "{0}{1:.{2}f}%".format(sign, abs(v), decimals)


def _index_row_fields(html_path):
    """回傳 dict：`row`（INDEX.md 一列 markdown）＋各拆解欄位，供
    `cmd_index_row`／`_do_finish` 共用（後者拿 meta 組 commit 訊息）。"""
    html_path = Path(html_path)
    text = html_path.read_text(encoding="utf-8")
    meta = _extract_dd_meta(text)
    sub_text = _extract_sub_text(text)

    ticker = meta.get("ticker") or "—"
    date_disp = meta.get("date") or "—"
    schema = meta.get("schema") or "—"

    verdict = meta.get("dca_verdict") or "—"
    role = meta.get("dca_role")
    rearm = meta.get("rearm_trigger")
    verdict_cell = verdict
    if role:
        verdict_cell += "｜" + role
    if rearm:
        verdict_cell += "·rearm＝" + rearm

    trap_label = meta.get("trap_label") or "—"

    moat = meta.get("moat_grade") or meta.get("moat") or "—"
    moat_trend = meta.get("moat_trend") or ""
    val = meta.get("val") or "—"
    trap = meta.get("trap") or "—"
    col6 = "{0}{1}/{2}/{3}".format(moat, moat_trend, val, trap)

    is_brief = bool(meta.get("brief"))
    try:
        rel = html_path.resolve().relative_to(DD_DIR.resolve())
        file_cell = str(rel)
    except ValueError:
        file_cell = html_path.name

    note_lead = sub_text or meta.get("oneliner") or "—"
    number_parts = []
    ev5y = _fmt_signed_pct(meta.get("ev5y_pct"), decimals=1)
    irr = _fmt_signed_pct(meta.get("irr_base_pct"), decimals=1)
    maxdd = _fmt_signed_pct(meta.get("max_dd_pct"), decimals=0)
    if ev5y is not None:
        number_parts.append("EV5y {0}".format(ev5y))
    if irr is not None:
        number_parts.append("IRR {0}/yr".format(irr))
    if maxdd is not None:
        number_parts.append("Max DD {0}".format(maxdd))
    note = note_lead
    if number_parts:
        note += "（{0}）".format("／".join(number_parts))
    suffix = (
        "**v17 快速版（sonnet 收證據→Fable 判斷→opus 閘→零 LLM 渲染）**"
        if is_brief else "**v17 完整版**"
    )
    note += "。" + suffix

    row = "| {date} | {ticker} | {schema} | {verdict} | {trap} | {col6} | {file} | {note} |".format(
        date=date_disp, ticker=ticker, schema=schema, verdict=verdict_cell,
        trap=trap_label, col6=col6, file=file_cell, note=note,
    )
    return {
        "meta": meta,
        "row": row,
        "file_cell": file_cell,
        "ticker": ticker,
        "date": date_disp,
        "is_brief": is_brief,
        "verdict": verdict,
        "role": role,
    }


def _append_index_row(row, file_cell):
    """append 到 INDEX.md 末尾；冪等——同檔名（`file_cell`）已存在則跳過。"""
    INDEX_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = INDEX_MD_PATH.read_text(encoding="utf-8") if INDEX_MD_PATH.exists() else ""
    if file_cell and file_cell in text:
        print("[skip] INDEX.md 已含 {0}，冪等不重複 append".format(file_cell))
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    text += row + "\n"
    INDEX_MD_PATH.write_text(text, encoding="utf-8")
    print("[ok] appended to {0}".format(INDEX_MD_PATH))
    return True


def _remove_index_row(row):
    """2026-09-07：同步失敗時只移除本輪 append 列，保留其他 session 的內容。"""
    if not INDEX_MD_PATH.exists():
        return False
    text = INDEX_MD_PATH.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    target = row.rstrip("\n")
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].rstrip("\r\n") == target:
            del lines[i]
            tmp = INDEX_MD_PATH.with_suffix(INDEX_MD_PATH.suffix + ".tmp")
            tmp.write_text("".join(lines), encoding="utf-8")
            os.replace(str(tmp), str(INDEX_MD_PATH))
            print("[rollback] 已移除本輪 INDEX.md 列")
            return True
    return False


def _snapshot_file(path):
    """2026-09-07：同步前保存衍生主表原貌，供失敗路徑精確回復。"""
    path = Path(path)
    try:
        return {"exists": True, "content": path.read_bytes()}
    except FileNotFoundError:
        return {"exists": False, "content": b""}


def _restore_file_snapshot(path, snapshot):
    """2026-09-07：以原子替換還原檔案，避免 INDEX 與 research 主表半套。"""
    path = Path(path)
    if snapshot.get("exists"):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(snapshot.get("content", b""))
        os.replace(str(tmp), str(path))
    elif path.exists():
        path.unlink()
    print("[rollback] 已還原 {0}".format(path))


def _set_finish_site_sync(manifest, manifest_path, state, deferred, note=None):
    """2026-09-07：立即同步與 --sync-later 共用同一份可恢復 finish state。"""
    finish_state = manifest.setdefault("finish", {})
    site_sync = finish_state.setdefault("site_sync", {})
    site_sync.update({"state": state, "deferred": bool(deferred), "updated_at": _now()})
    if note is not None:
        site_sync["note"] = note
    elif "note" in site_sync:
        del site_sync["note"]
    if state in ("PENDING", "FAIL", "GENERATED", "COMMITTED"):
        finish_state["state"] = "PENDING_SITE_SYNC"
    _atomic_write_json(manifest_path, manifest)


def _mark_sync_rows(rows, state, note=None, no_push=False):
    """2026-09-07：批尾／補同步把每一檔 run manifest 推進同一狀態機。"""
    for row in rows:
        manifest_path = _run_dir(row["ticker"], row["date"]) / "manifest.json"
        manifest = _load_json_or(manifest_path, None)
        if not isinstance(manifest, dict):
            continue
        _set_finish_site_sync(manifest, manifest_path, state, True, note=note)
        if state == "PASS":
            manifest["finish"]["state"] = "COMPLETE_NO_PUSH" if no_push else "COMPLETE"
            _atomic_write_json(manifest_path, manifest)


def _pending_site_sync_rows():
    """2026-09-07：掃描硬當掉後仍未結清的延後同步，不依賴 batch 記憶體。"""
    rows = []
    for manifest_path in sorted(RUNS_DIR.glob("*/manifest.json")):
        manifest = _load_json_or(manifest_path, None)
        if not isinstance(manifest, dict):
            continue
        site_sync = ((manifest.get("finish") or {}).get("site_sync") or {})
        if site_sync.get("deferred") and site_sync.get("state") in (
                "PENDING", "FAIL", "GENERATED", "COMMITTED"):
            ticker, date = manifest.get("ticker"), manifest.get("date")
            if ticker and date:
                rows.append({
                    "ticker": ticker, "date": date, "rc": 0,
                    "manifest_path": str(manifest_path),
                })
    return rows


def _print_pending_sync_escape(rows, skipped=False):
    """2026-09-07：列出鎖住開工的 pending 與明確、安全的處置方式。"""
    prefix = "[warn] 已略過" if skipped else "[error] 無法補完"
    print("{0} {1} 檔 pending 網站同步：".format(prefix, len(rows)), file=sys.stderr)
    for row in rows:
        print(
            "  - {0}_{1}；manifest={2}".format(
                row.get("ticker"), row.get("date"), row.get("manifest_path", "—")),
            file=sys.stderr,
        )
    print("修復報告檔或 screener 後重跑原命令，程式會先再次補同步。", file=sys.stderr)
    print(
        "若須先處理其他標的，本次命令加 --skip-pending-sync；"
        "此旗標不會清除 pending，之後仍須修復並重跑。",
        file=sys.stderr,
    )


def _recover_pending_site_sync(no_push=False):
    """2026-09-07：新 run／batch 開工前先補完上次 --sync-later 的 pending。"""
    rows = _pending_site_sync_rows()
    if not rows:
        return 0
    print("[pending-sync] 發現 {0} 檔未結同步，先補完再開工".format(len(rows)))
    by_date = {}
    for row in rows:
        by_date.setdefault(row["date"], []).append(row)
    for date, date_rows in sorted(by_date.items()):
        rc = _sync_batch_site(date_rows, date, no_push=no_push, skip_dd_screener=False)
        if rc != 0:
            # 2026-09-07：一筆壞 pending 預設仍 fail-closed，但錯誤必須可定位，
            # 並提供只略過本次開工、不竄改狀態的逃生口。
            _print_pending_sync_escape(date_rows)
            return rc
    return 0


def _pending_sync_preflight(skip_pending_sync=False, no_push=False):
    """2026-09-07：run／batch 共用 pending 補償與明示逃生口。"""
    if skip_pending_sync:
        rows = _pending_site_sync_rows()
        if rows:
            _print_pending_sync_escape(rows, skipped=True)
        return 0
    return _recover_pending_site_sync(no_push=no_push)


def cmd_index_row(args):
    fields = _index_row_fields(args.html)
    print(fields["row"])
    if args.append:
        _append_index_row(fields["row"], fields["file_cell"])
    return 0


# ---------------------------------------------------------------------------
# WP6a: finish — index-row append → update_dd_index.py → 存查 → commit → push
# ---------------------------------------------------------------------------

def _model_bucket(model_id):
    m = (model_id or "").lower()
    if "opus" in m:
        return "opus"
    if "fable" in m:
        return "fable"
    if "sonnet" in m:
        return "sonnet"
    if "haiku" in m:
        return "haiku"
    return "other"


def _empty_bucket():
    # 2026-09-10（WP-B）：加 `input`＝`inputTokens`＋`cacheCreationInputTokens`
    # ——真成本（尤其判斷段 Fable）主要燒在輸出＋非快取輸入，只報
    # `cache_read` 會低估；`cache_read`／`cache_creation` 兩欄原樣保留供既有
    # 呼叫端相容，`input` 是新增的疊加視角，不取代前兩者。
    return {"cache_read": 0, "cache_creation": 0, "input": 0, "output": 0, "cost_usd": 0.0}


def _sum_usage_by_model(usage_list):
    buckets = {}
    for u in usage_list or []:
        by_model = (u or {}).get("by_model") or {}
        for mid, vals in by_model.items():
            b = buckets.setdefault(_model_bucket(mid), _empty_bucket())
            b["cache_read"] += (vals or {}).get("cacheReadInputTokens", 0) or 0
            cache_creation = (vals or {}).get("cacheCreationInputTokens", 0) or 0
            b["cache_creation"] += cache_creation
            b["input"] += ((vals or {}).get("inputTokens", 0) or 0) + cache_creation
            b["output"] += (vals or {}).get("outputTokens", 0) or 0
            b["cost_usd"] += (vals or {}).get("costUSD", 0) or 0
    return buckets


def _stage_elapsed_seconds(stage):
    """2026-09-06：用 manifest ISO 時戳算段落牆鐘；缺任一端就回 None。"""
    try:
        started = time.mktime(time.strptime(stage["started"], "%Y-%m-%dT%H:%M:%S"))
        ended = time.mktime(time.strptime(stage["ended"], "%Y-%m-%dT%H:%M:%S"))
        return max(0.0, ended - started)
    except (KeyError, TypeError, ValueError):
        return None


def _usage_observation(stage):
    usage = list((stage or {}).get("agent_usage") or []) + list((stage or {}).get("agent_usage_prior") or [])
    return {
        "cache_read": sum((u or {}).get("cache_read", 0) or 0 for u in usage),
        "output": sum((u or {}).get("output_tokens", 0) or 0 for u in usage),
        "cost_usd": sum((u or {}).get("cost_usd", 0) or 0 for u in usage),
        "agent_seconds": sum(((u or {}).get("duration_ms", 0) or 0) / 1000.0 for u in usage),
    }


def _record_stage_observation(manifest, stage_name):
    """2026-09-06：段落結束時把時間、token、成本寫回 manifest 並印一行。"""
    stage = (manifest.get("stages") or {}).get(stage_name) or {}
    obs = _usage_observation(stage)
    elapsed = _stage_elapsed_seconds(stage)
    if elapsed is not None:
        obs["elapsed_seconds"] = elapsed
    stage["observation"] = obs
    print("[段落] {0} 結束 {1}／牆鐘 {2}／cache_read {3}／output {4}／cost ${5:.2f}".format(
        stage_name, stage.get("ended") or _now(),
        "{0:.1f}s".format(elapsed) if elapsed is not None else "—",
        obs["cache_read"], obs["output"], obs["cost_usd"],
    ))
    return obs


def _build_token_ledger(manifest):
    """從 manifest 的 `stages.*.agent_usage` 彙總三欄（fable/opus/sonnet，
    另有 haiku/other 兜底）＋每段輪次，回傳 `{totals, by_stage}`。2026-09-06：
    一併疊入 `stages.*.agent_usage_prior`（見 `_fresh_stage_preserving_prior`）
    ——`--resume` 前一輪已燒但未 PASS 的段搬到這裡，全帳（totals／by_stage）
    才是真正的整趟花費，不是只算本次重跑那一段。"""
    totals = {}
    by_stage = {}
    total_cost = 0.0
    total_stage_wall = 0.0
    for stage_name, stage in (manifest.get("stages") or {}).items():
        usage_list = list((stage or {}).get("agent_usage") or []) + list((stage or {}).get("agent_usage_prior") or [])
        buckets = _sum_usage_by_model(usage_list)
        turns = sum((u or {}).get("num_turns", 0) or 0 for u in usage_list)
        observation = _usage_observation(stage)
        wall_seconds = _stage_elapsed_seconds(stage)
        by_stage[stage_name] = dict(
            buckets, turns=turns, wall_seconds=wall_seconds,
            agent_seconds=observation["agent_seconds"], cost_usd=observation["cost_usd"],
            cache_read=observation["cache_read"], output=observation["output"],
        )
        total_cost += observation["cost_usd"]
        total_stage_wall += wall_seconds or 0.0
        for k, v in buckets.items():
            t = totals.setdefault(k, _empty_bucket())
            for kk in ("cache_read", "cache_creation", "input", "output", "cost_usd"):
                t[kk] += v[kk]
    return {
        "totals": totals,
        "by_stage": by_stage,
        "summary": {"cost_usd": total_cost, "stage_wall_seconds": total_stage_wall},
    }


def _ledger_cache_read_total(ledger, models=("fable", "opus", "sonnet", "other", "haiku")):
    return sum((ledger["totals"].get(m) or {}).get("cache_read", 0) for m in models)


def _ledger_output_total(ledger, models=("fable", "opus", "sonnet", "other", "haiku")):
    """2026-09-10（WP-B）：同 `_ledger_cache_read_total`，但加總 output——
    判斷段（Fable）的錢主要燒在輸出，只報 cache_read 看不出這塊。"""
    return sum((ledger["totals"].get(m) or {}).get("output", 0) for m in models)


def _prior_usage_cache_read_total(manifest):
    """2026-09-06：只加總 `stages.*.agent_usage_prior`（--resume 前先前失敗
    但已燒的段）的 cache_read，供 `_ledger_summary_line` 附註用；沒有任何
    prior 段時回傳 0（呼叫端據此決定要不要印附註）。"""
    total = 0
    for stage in (manifest.get("stages") or {}).values():
        buckets = _sum_usage_by_model((stage or {}).get("agent_usage_prior") or [])
        total += sum((b or {}).get("cache_read", 0) for b in buckets.values())
    return total


def _ledger_summary_line(ledger, prior_total=0):
    """2026-09-06：`prior_total`（cache_read，來自 `_prior_usage_cache_read_total`）
    非零時附一句「（含先前段 Y.YM）」，讓 --resume 後的全帳行看得出這次數字
    有沒有含前面失敗但已燒的段；`total` 本身已經含 prior（見
    `_build_token_ledger`），這裡只是額外標註來源，不重複相加。

    2026-09-10（WP-B）：只報 cache_read 低估真成本——判斷段（Fable）的錢
    主要燒在輸出，不是快取讀取。改印 cache_read／output／$ 總額，並列
    fable／opus／sonnet 三模型各自的美元成本（cost_usd 直接來自
    `by_model.*.costUSD` 加總，不是 token 數換算，見 `_sum_usage_by_model`）。
    舊 manifest 缺 `input`／`cost_usd` 欄位時 `_empty_bucket` 已補 0，這裡
    不需要另外容錯。"""
    total_cache_read = _ledger_cache_read_total(ledger)
    total_output = _ledger_output_total(ledger)
    total_cost = (ledger.get("summary") or {}).get("cost_usd", 0.0)
    fable_cost = (ledger["totals"].get("fable") or {}).get("cost_usd", 0.0)
    opus_cost = (ledger["totals"].get("opus") or {}).get("cost_usd", 0.0)
    sonnet_cost = (ledger["totals"].get("sonnet") or {}).get("cost_usd", 0.0)
    line = (
        "全帳 cache_read {0:.1f}M／output {1:.1f}K／${2:.2f}"
        "（fable ${3:.2f}／opus ${4:.2f}／sonnet ${5:.2f}）"
    ).format(
        total_cache_read / 1_000_000.0, total_output / 1_000.0, total_cost,
        fable_cost, opus_cost, sonnet_cost,
    )
    if prior_total:
        line += "（含先前段 cache_read {0:.1f}M）".format(prior_total / 1_000_000.0)
    return line


def _finish_target_html(ticker, date, manifest):
    """本次 run 實際產出的報告檔——優先信 manifest 的
    `stages.prose.out_path`（2026-09-06 WP4b 交付：`--full` 跑完後這是
    完整版，比快速版更接近「這次真正要上站的東西」），沒有才退回
    `stages.brief.out_path`（這個 run 自己寫過什麼就是什麼，不用檔案系統
    猜）。兩者都缺失或已不存在時才退回按檔名慣例猜測（先 brief 再完整版
    ——brief 是 v17 現行預設產物，缺 out_path 多半代表這次跑的正是它）。

    2026-09-07（P1-2）：prose 只在該 stage state＝PASS 時才可被選中——
    out_path 指到的檔即使仍實際存在於磁碟（例如上一輪 FAIL 前的殘留產出），
    未 PASS 的 prose 也不算數，一律退回 brief。`_do_finish` 已在呼叫本函式
    前用 `_finish_required_stages` 擋過一次；這裡是第二層防線，讓任何直接
    呼叫本函式的路徑（如批尾同步 `_sync_batch_site`）也不會選錯檔。"""
    stages = manifest.get("stages") or {}
    prose_stage = stages.get("prose") or {}
    prose_out = prose_stage.get("out_path")
    if prose_stage.get("state") == "PASS" and prose_out and Path(prose_out).exists():
        return Path(prose_out)
    brief_stage = stages.get("brief") or {}
    out_path = brief_stage.get("out_path")
    if out_path and Path(out_path).exists():
        return Path(out_path)
    brief_default = DD_DIR / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date)
    if brief_default.exists():
        return brief_default
    return DD_DIR / "DD_{0}_{1}.html".format(ticker, date)


def _finish_required_stages(manifest):
    """2026-09-07（P1-2）：finish 發布前逐一驗必要 stage，不再只信 brief
    一段——公開的 `finish` 子命令可以繞過 `cmd_run` 的 stage loop 直接呼叫，
    那條序列保證因此不能只靠正常 run 路徑撐著。

    brief 發布固定要求 stage0／judged／gated／brief 全 PASS；manifest 只要
    記錄過 `prose` 這個 stage（代表這輪跑過 `--full`），就再加驗 prose PASS
    ——不論 prose 最後有沒有真的被 `_finish_target_html` 選中，未 PASS 的
    prose 都不該讓 finish 帶著任何一段失敗往下走。

    這裡刻意不比照 `cmd_run` 的 `--resume` 相容邏輯（該邏輯為了向後相容舊
    manifest，允許 gated／brief 以外的段以 SKIPPED 視為「可以繼續跑」）——
    finish 問的是「可不可以發布」，門檻要嚴格：SKIPPED 一律不算 PASS，
    比照 gated／brief 現行處置（3.9 相容、無 walrus）。"""
    stages = manifest.get("stages") or {}
    required = list(STAGE_ORDER[:4])  # stage0, judged, gated, brief
    if "prose" in stages:
        required.append("prose")
    missing = []
    for name in required:
        state = (stages.get(name) or {}).get("state")
        if state != "PASS":
            missing.append((name, state))
    return required, missing


def _load_finish_manifest(run_dir, manifest_path, ticker, date):
    """2026-09-07（P1-4）：manifest 併入同一套 source resolver——`.dd_build`
    整輪被清掉、run 目錄的 manifest 讀不到時，退回存查
    `notes/site-internal/dd/_src/{T}_{D}/manifest.json`（archive 流程本就
    會複製一份，見 `_archive_run_dir`），讓 finish 能由此續行而不是立刻
    結束。

    archive 裡各 stage 的 `out_path` 是『當時那台機器 run 目錄』寫下的絕對
    路徑，換一台機器或換一個 clone 就可能不存在或（更危險）恰好撞到別的
    檔——不可直接信；回傳前一律按 ticker／date／輸出型態，用這台機器現行
    的 `DD_DIR` 重新解出 docs 目標，只覆寫 out_path，其餘欄位（state／
    agent_usage 等）原樣保留，不改變任何判斷或機械驗算的輸入。

    回傳 `(manifest, fallback_info)`；兩者來源都讀不到時 `manifest` 為
    `None`、`fallback_info` 為 `None`。"""
    manifest = _load_json_or(manifest_path, None)
    if manifest is not None:
        return manifest, None
    archive_manifest_path = SRC_ARCHIVE_DIR / run_dir.name / "manifest.json"
    manifest = _load_json_or(archive_manifest_path, None)
    if manifest is None:
        return None, None
    manifest = json.loads(json.dumps(manifest, ensure_ascii=False))  # 深拷貝，不動存查原檔
    stages = manifest.get("stages") or {}
    recomputed_out_path = {
        "brief": DD_DIR / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date),
        "prose": DD_DIR / "DD_{0}_{1}.html".format(ticker, date),
    }
    for stage_name, out_default in recomputed_out_path.items():
        stage = stages.get(stage_name)
        if isinstance(stage, dict) and stage.get("out_path"):
            stage["out_path"] = str(out_default)
    return manifest, {
        "source": "manifest",
        "run_path": str(manifest_path),
        "path": str(archive_manifest_path),
    }


def _finish_file_set(ticker, date, file_cell, include_sync=True):
    files = [
        DD_DIR / file_cell,
        # 2026-09-06 WP4b：`--full` 跑完時 `file_cell` 會是完整版
        # `DD_{T}_{D}.html`（見 `_finish_target_html`），但同一次 run 通常也
        # 產出了快速版 `brief/BRIEF_{T}_{D}.html`——兩個檔案都上站，一併納入
        # 白名單；`existing_files` 過濾只留真的存在的檔，不存在時這行是無害
        # 多餘項。
        DD_DIR / "brief" / "BRIEF_{0}_{1}.html".format(ticker, date),
        SRC_ARCHIVE_DIR / "{0}_{1}".format(ticker, date),
    ]
    if include_sync:
        files.extend([
            INDEX_MD_PATH,
            RESEARCH_BODY_PATH,
            DD_SCREENER_LATEST_PATH,
            PICKS_CANDIDATES_PATH,
            TICKER_HUB_DIR / "{0}.html".format(ticker),
            TICKER_HUB_DIR / "index.html",
        ])
    return files


def _ignore_inline_prompt_files(dirpath, names):
    """`shutil.copytree(ignore=...)` callback：略過 `*_inline.md`（bundle
    內嵌版 prompt，見 `_write_inline_prompt`），只留模板渲染版存查。"""
    return [n for n in names if n.endswith("_inline.md")]


def _archive_run_dir(run_dir, archive_dir):
    """把 run 目錄的固定產物複製到 `notes/site-internal/dd/_src/{T}_{D}/`，
    檔名照既有慣例加 `{T}_{D}.` 前綴；`parts/`／`prompts/`／`agents/`／
    `prose/`（2026-09-06 WP4b：`--full` 產出的逐段 prose/{sid}.html，C-1
    機械段與散文 agent 寫的段落都在裡面）各自整個目錄複製（子目錄內原檔名
    不變）。回傳複製項目清單。"""
    run_dir = Path(run_dir)
    archive_dir = Path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    stem = archive_dir.name

    renamed = {
        "evidence.json": "{0}.evidence.json".format(stem),
        "digest.json": "{0}.transcript_digest.json".format(stem),
        "judgment.json": "{0}.judgment.json".format(stem),
        "scenario.json": "{0}.scenario.json".format(stem),
        "scenario_meta.json": "{0}.scenario_meta.json".format(stem),
        "gate_audit.md": "{0}.gate_audit.md".format(stem),
    }
    copied = []
    for src_name, dst_name in renamed.items():
        src = run_dir / src_name
        if src.exists():
            shutil.copy2(str(src), str(archive_dir / dst_name))
            copied.append(dst_name)

    for sub in ("parts", "prompts", "agents", "prose"):
        src_dir = run_dir / sub
        if src_dir.exists():
            dst_dir = archive_dir / sub
            if dst_dir.exists():
                shutil.rmtree(str(dst_dir))
            # WP8 待補 #5：`prompts/` 底下的 `*_inline.md`（judge／gate／patch
            # 把 bundle 全文接在模板之後另存的內嵌版，見 `_write_inline_prompt`）
            # 只是餵子 agent 用的一次性大檔（bundle 內嵌證據原文，體積大且
            # 半形標點未正規化），存查只需留模板渲染版，故存檔時略過。
            ignore = _ignore_inline_prompt_files if sub == "prompts" else None
            shutil.copytree(str(src_dir), str(dst_dir), ignore=ignore)
            copied.append(sub + "/")

    manifest_src = run_dir / "manifest.json"
    if manifest_src.exists():
        shutil.copy2(str(manifest_src), str(archive_dir / "manifest.json"))
        copied.append("manifest.json")

    print("[archive] {0} → {1}（{2} 項）".format(run_dir, archive_dir, len(copied)))
    return copied


def _git(args, cwd=None):
    """git 呼叫的唯一入口——測試 monkeypatch 這支即可隔離真實 git。"""
    return subprocess.run(["git"] + list(args), cwd=str(cwd or REPO_ROOT), capture_output=True, text=True)


def _git_ahead_behind():
    """回傳 (ahead, behind)；behind>0 代表遠端領先（先 fetch 再比）。"""
    _git(["fetch", "origin", "main"])
    r = _git(["rev-list", "--left-right", "--count", "HEAD...origin/main"])
    if r.returncode != 0:
        return (0, 0)
    parts = (r.stdout or "").strip().split()
    if len(parts) != 2:
        return (0, 0)
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return (0, 0)


DD_WORKTREE_DIR = Path("/tmp/dd_wt")


def _push_head_via_worktree(commit_sha):
    """遠端領先時的自救推送：開一個 detached worktree（`origin/main`），
    只把本次 finish 產生的那顆 commit（`commit_sha`）cherry-pick 上去再推，
    本地 main（目前所在 working tree／分支）完全不動——不 update-ref、
    不 checkout 任何檔。回傳 (ok: bool, reason: str)；ok=False 時 reason
    說明是 cherry-pick 衝突還是 push 被擋（例如 pre-push QC gate）。
    """
    wt = DD_WORKTREE_DIR
    # 清掉可能殘留的舊 worktree 註冊（不假設乾淨環境）
    _git(["worktree", "remove", "--force", str(wt)])
    if wt.exists():
        shutil.rmtree(str(wt), ignore_errors=True)
    _git(["worktree", "prune"])

    add_r = _git(["worktree", "add", "--detach", str(wt), "origin/main"])
    if add_r.returncode != 0:
        return False, "worktree add 失敗：{0}".format(
            ((add_r.stdout or "") + (add_r.stderr or "")).strip()
        )

    cp_r = _git(["cherry-pick", commit_sha], cwd=wt)
    if cp_r.returncode != 0:
        _git(["cherry-pick", "--abort"], cwd=wt)
        _git(["worktree", "remove", "--force", str(wt)])
        return False, "cherry-pick 衝突：{0}".format(
            ((cp_r.stdout or "") + (cp_r.stderr or "")).strip()
        )

    push_r = _git(["push", "origin", "HEAD:main"], cwd=wt)
    if push_r.returncode != 0:
        _git(["worktree", "remove", "--force", str(wt)])
        return False, "push 被擋（可能 pre-push QC gate）：{0}".format(
            ((push_r.stdout or "") + (push_r.stderr or "")).strip()
        )

    _git(["worktree", "remove", "--force", str(wt)])
    return True, ""


def _finish_source_path(run_dir, source_name):
    """2026-09-07：run 來源不存在時，回退到同一輪 DD 的 committed 存查。"""
    run_dir = Path(run_dir)
    run_path = run_dir / "{0}.json".format(source_name)
    if run_path.exists():
        return run_path, None
    stem = run_dir.name
    archive_path = SRC_ARCHIVE_DIR / stem / "{0}.{1}.json".format(stem, source_name)
    if archive_path.exists():
        return archive_path, {
            "source": source_name,
            "run_path": str(run_path),
            "path": str(archive_path),
        }
    return archive_path, None


def _finish_consistency_sources(run_dir, html_path):
    """2026-09-07：讀 finish 的三個數字來源；結構性 N/A 必須明列。"""
    run_dir = Path(run_dir)
    judgment_path, judgment_fallback = _finish_source_path(run_dir, "judgment")
    scenario_meta_path, scenario_fallback = _finish_source_path(run_dir, "scenario_meta")
    judgment = _load_json_or(judgment_path, None)
    scenario_meta = _load_json_or(scenario_meta_path, None)
    html_meta = dd_meta_reader.read_dd_meta(html_path)
    fallback_items = [item for item in (judgment_fallback, scenario_fallback) if item]
    source_errors = []
    for label, path, obj in (
        ("judgment", judgment_path, judgment),
        ("scenario_meta", scenario_meta_path, scenario_meta),
        ("HTML dd-meta", Path(html_path), html_meta),
    ):
        if not isinstance(obj, dict):
            source_errors.append("{0}：找不到或不是合法 JSON（{1}）".format(label, path))

    source_paths = {
        "judgment": str(judgment_path),
        "scenario_meta": str(scenario_meta_path),
        "html_dd_meta": str(html_path),
    }
    if source_errors:
        return None, source_errors, [], source_paths, fallback_items

    decision_inputs = judgment.get("decision_inputs") or {}
    max_dd = (judgment.get("premortem") or {}).get("max_dd") or {}
    lo, hi = max_dd.get("lo"), max_dd.get("hi")
    if (isinstance(lo, (int, float)) and not isinstance(lo, bool)
            and isinstance(hi, (int, float)) and not isinstance(hi, bool)):
        judgment_max_dd = min(lo, hi)
    elif lo is not None and hi is not None:
        # 2026-09-07：保留非數字原值交給下一層列成 mismatch，不讓 min() 先崩潰。
        judgment_max_dd = {"lo": lo, "hi": hi}
    else:
        judgment_max_dd = lo
    values = {}
    na_items = []
    for field in ("ev5y_pct", "irr_base_pct", "asym_ratio"):
        judgment_value = decision_inputs.get(field)
        scenario_value = scenario_meta.get(field)
        values[field] = {
            "judgment": judgment_value,
            "scenario_meta": scenario_value,
            "html_dd_meta": html_meta.get(field),
        }
        # 2026-09-07：主判斷 prompt 明定三欄留 null；scenario 有值時明列 N/A，
        # 但 key 缺失或 scenario 也缺值仍交給 mismatch 擋下。
        if field in decision_inputs and judgment_value is None and scenario_value is not None:
            na_items.append({
                "field": field, "source": "judgment",
                "path": str(judgment_path),
                "reason": "judgment 依設計填 null；權威值由 scenario_meta 機械計算",
            })
    values["max_dd_pct"] = {
        "judgment": judgment_max_dd,
        "scenario_meta": None,
        "html_dd_meta": html_meta.get("max_dd_pct"),
    }
    na_items.append({
        "field": "max_dd_pct", "source": "scenario_meta",
        "path": str(scenario_meta_path),
        "reason": "scenario_meta 結構性不產此欄；Max DD 恆等式由 verify_dd_math.py 驗證",
    })
    return values, [], na_items, source_paths, fallback_items


def _finish_consistency_mismatches(values, na_items=None):
    """2026-09-07：前三欄沿用權威容差；Max DD 直拷欄只容許極小 epsilon。"""
    tolerances = {
        "ev5y_pct": verify_dd_math.EV_TOL,
        "irr_base_pct": verify_dd_math.IRR_TOL,
        "asym_ratio": verify_dd_math.AR_TOL,
        "max_dd_pct": FINISH_MAXDD_EPSILON,
    }
    expected_sources = {
        "ev5y_pct": ("judgment", "scenario_meta", "html_dd_meta"),
        "irr_base_pct": ("judgment", "scenario_meta", "html_dd_meta"),
        "asym_ratio": ("judgment", "scenario_meta", "html_dd_meta"),
        "max_dd_pct": ("judgment", "html_dd_meta"),
    }
    structural_na = {
        (item.get("field"), item.get("source")) for item in (na_items or [])
    }
    mismatches = []
    for field, source_values in values.items():
        reasons = []
        numeric = []
        for source in expected_sources[field]:
            if (field, source) in structural_na:
                continue
            value = source_values.get(source)
            if value is None:
                reasons.append("{0} 缺值".format(source))
            elif isinstance(value, bool) or not isinstance(value, (int, float)):
                reasons.append("{0} 非數字：{1!r}".format(source, value))
            else:
                numeric.append((source, float(value)))
        tolerance = tolerances[field]
        for i, (left_source, left_value) in enumerate(numeric):
            for right_source, right_value in numeric[i + 1:]:
                if abs(left_value - right_value) > tolerance:
                    reasons.append("{0} vs {1} 差 {2:.4g} > 容差 {3}".format(
                        left_source, right_source, abs(left_value - right_value), tolerance,
                    ))
        if reasons:
            mismatches.append({
                "field": field,
                "tolerance": tolerance,
                "judgment": source_values.get("judgment"),
                "scenario_meta": source_values.get("scenario_meta"),
                "html_dd_meta": source_values.get("html_dd_meta"),
                "reasons": reasons,
            })
    return mismatches


def _run_finish_consistency_gate(run_dir, manifest, manifest_path, html_path,
                                 accept_mismatch=False):
    """2026-09-07：finish 發布硬閘；回傳 True 才能寫 INDEX／commit／push。"""
    py = _pick_python()
    math_cmd = [py, str(SCRIPTS_DIR / "verify_dd_math.py"), str(html_path)]
    math_result = subprocess.run(math_cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    math_output = ((math_result.stdout or "") + (math_result.stderr or "")).strip()

    values, source_errors, na_items, source_paths, fallback_items = (
        _finish_consistency_sources(run_dir, html_path)
    )
    mismatches = _finish_consistency_mismatches(values, na_items) if values is not None else []
    if fallback_items:
        print("[finish-check] 使用存查 fallback：")
        for item in fallback_items:
            print("  - {0}：{1} 不存在，改讀 {2}".format(
                item["source"], item["run_path"], item["path"]))
    if na_items:
        print("[finish-check] 結構性 N/A（明列、不靜默跳過）：")
        for item in na_items:
            print("  - {0}／{1}（{2}）：{3}".format(
                item["field"], item["source"], item["path"], item["reason"]))

    if source_errors:
        print("[HOLD] 發布前一致性檢查無法讀取來源：", file=sys.stderr)
        for error in source_errors:
            print("  - " + error, file=sys.stderr)

    if mismatches:
        mismatch_tag = "[accept-mismatch]" if accept_mismatch else "[HOLD]"
        print("{0} 發布前三方數字不一致：".format(mismatch_tag), file=sys.stderr)
        for item in mismatches:
            print(
                "  - {0}：judgment（{1}）={2!r}／scenario_meta（{3}）={4!r}／"
                "HTML dd-meta（{5}）={6!r}（容差 {7}；{8}）".format(
                    item["field"], source_paths["judgment"], item["judgment"],
                    source_paths["scenario_meta"], item["scenario_meta"],
                    source_paths["html_dd_meta"], item["html_dd_meta"],
                    item["tolerance"], "；".join(item["reasons"]),
                ),
                file=sys.stderr,
            )

    # 2026-09-07：旗標本身也留痕；只放行三方差異，不能繞過權威 verifier FAIL。
    if accept_mismatch:
        manifest.setdefault("finish_mismatch_acceptances", []).append({
            "accepted_at": _now(),
            "html_path": str(html_path),
            "verifier_passed": math_result.returncode == 0,
            "proceeded": math_result.returncode == 0 and not source_errors,
            "fields": mismatches,
            "structural_na": na_items,
            "fallback_sources": fallback_items,
            "source_paths": source_paths,
        })
        _atomic_write_json(manifest_path, manifest)

    if math_result.returncode != 0:
        print("[HOLD] verify_dd_math.py 未通過（rc={0}）：".format(
            math_result.returncode), file=sys.stderr)
        if math_output:
            print(math_output, file=sys.stderr)
        print("下一步：修正來源後重跑驗證；不得用旗標繞過。", file=sys.stderr)
        return False
    print("[finish-check] verify_dd_math.py PASS")

    if source_errors:
        print("下一步：修正來源後重跑驗證；不得用旗標繞過。", file=sys.stderr)
        return False
    if mismatches and not accept_mismatch:
        print("下一步：修正來源後重跑驗證；不得加旗標繞過，除非持有人明確放行。", file=sys.stderr)
        return False
    if mismatches:
        print("[accept-mismatch] 持有人明確放行 {0} 個欄位；原值已寫入 manifest".format(
            len(mismatches)))
    else:
        print("[finish-check] 三方數字一致")
    return True


def _do_finish(ticker, date, dry_run=False, no_push=False, skip_dd_screener=False,
               sync_later=False, accept_mismatch=False):
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    # 2026-09-07（P1-4）：manifest 缺失時併入同一套 source resolver 退回存查。
    manifest, manifest_fallback = _load_finish_manifest(run_dir, manifest_path, ticker, date)
    if manifest is None:
        print("[error] 找不到 manifest（run 目錄與存查皆無）：{0}".format(manifest_path), file=sys.stderr)
        return 1
    if manifest_fallback:
        print("[finish-check] 使用存查 fallback：manifest：{0} 不存在，改讀 {1}".format(
            manifest_fallback["run_path"], manifest_fallback["path"]))

    # 2026-09-07（P1-2）：任何副作用與 HTML 選擇之前，逐一驗必要 stage 皆
    # PASS——不再只信 brief 一段，SKIPPED 也不算數。
    required_stages, missing_stages = _finish_required_stages(manifest)
    if missing_stages:
        print(
            "[error] finish 必要 stage 未全數 PASS，中止（必要段：{0}；未過：{1}）".format(
                "＋".join(required_stages),
                "；".join("{0}={1}".format(name, state or "—") for name, state in missing_stages),
            ),
            file=sys.stderr,
        )
        return 1

    html_path = _finish_target_html(ticker, date, manifest)
    if not html_path.exists():
        print("[error] 找不到報告檔：{0}".format(html_path), file=sys.stderr)
        return 1

    # 2026-09-07：任何發布副作用前先跑權威驗算＋三方一致性；dry-run 也不略過。
    if not _run_finish_consistency_gate(
            run_dir, manifest, manifest_path, html_path,
            accept_mismatch=accept_mismatch):
        return 1
    # 2026-09-07（P1-5）：機械閘通過即記 validated——manifest 的『這份 HTML
    # 有沒有過三方一致性與 verify_dd_math』狀態，不必再從有沒有錯誤輸出反推。
    manifest.setdefault("finish", {})["validated"] = True
    _atomic_write_json(manifest_path, manifest)

    fields = _index_row_fields(html_path)
    meta = fields["meta"]

    # 2026-09-06：batch 每檔只收報告與存查；研究頁／screener 留到批尾一次同步。
    files = _finish_file_set(ticker, date, fields["file_cell"], include_sync=not sync_later)
    print("[plan] 檔案集：")
    for f in files:
        print("  - {0}".format(f))

    ledger = _build_token_ledger(manifest)
    ledger_line = _ledger_summary_line(ledger, _prior_usage_cache_read_total(manifest))  # 2026-09-06：含先前段附註
    print(ledger_line)

    if dry_run:
        print("[dry-run] 不寫 INDEX、不跑 update_dd_index、不 commit、不 push")
        return 0

    if skip_dd_screener and not sync_later:
        # 2026-09-07：latest.json 是發布必要集合；人工 maintenance 旗標不可
        # 讓 finish 宣稱完成卻略過 screener。
        print("[error] finish 不允許 --skip-dd-screener；必要同步包含 latest.json",
              file=sys.stderr)
        return 1

    if sync_later:
        _set_finish_site_sync(manifest, manifest_path, "PENDING", True)
        print("[sync-later] 本檔不寫 INDEX、不跑 update_dd_index；交由 batch 結尾一次同步")
    else:
        _set_finish_site_sync(manifest, manifest_path, "PENDING", False)
        appended = _append_index_row(fields["row"], fields["file_cell"])
        # 2026-09-07：update_dd_index 先寫 research 主表再建 screener；後者
        # 失敗時必須把兩邊一起回復，不能只撤 INDEX。
        research_snapshot = _snapshot_file(RESEARCH_BODY_PATH)

        py = _pick_python()
        cmd = [py, str(SCRIPTS_DIR / "update_dd_index.py")]
        r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        sync_output = ((r.stdout or "") + (r.stderr or "")).strip()
        if r.returncode != 0:
            if appended:
                _remove_index_row(fields["row"])
            _restore_file_snapshot(RESEARCH_BODY_PATH, research_snapshot)
            _set_finish_site_sync(
                manifest, manifest_path, "FAIL", False,
                note="update_dd_index.py rc={0}".format(r.returncode))
            print(
                "[error] update_dd_index.py 失敗（rc={0}），停止發布：\n{1}".format(
                    r.returncode, sync_output[-4000:] or "（無輸出）"
                ),
                file=sys.stderr,
            )
            return 1
        _set_finish_site_sync(manifest, manifest_path, "PASS", False)
        # 2026-09-07：把 optional cascade 的彙總搬到 finish 尾端可見位置。
        for line in sync_output.splitlines():
            if line.startswith("[sync-summary]"):
                print(line)
        print("[ok] update_dd_index.py rc=0")

    archive_dir = SRC_ARCHIVE_DIR / "{0}_{1}".format(ticker, date)
    _archive_run_dir(run_dir, archive_dir)
    token_path = archive_dir / "token.json"
    _atomic_write_json(token_path, ledger)
    print(ledger_line)

    verdict = meta.get("dca_verdict") or "—"
    role = meta.get("dca_role") or "—"
    label = "DD 快速版" if meta.get("brief") else "DD 完整版"
    total_m = _ledger_cache_read_total(ledger) / 1_000_000.0
    total_cost = (ledger.get("summary") or {}).get("cost_usd", 0.0)
    # 2026-09-10（WP-B）：「v17 全帳 X.XM」只算 cache_read 低估真成本，改成
    # 「v17 $Z.ZZ／X.XM」——$ 在前（真成本），cache_read 仍留在後面當量級參考。
    commit_subject = "Add {0} {1} {2}（{3}｜{4}；v17 ${5:.2f}／{6:.1f}M）".format(
        ticker, label, date, verdict, role, total_cost, total_m,
    )
    if not sync_later:
        commit_subject += "; resync research+screener"
    trailer = os.environ.get("DD_COMMIT_TRAILER")
    commit_msg = commit_subject if not trailer else "{0}\n\n{1}".format(commit_subject, trailer)

    existing_files = [f for f in files if Path(f).exists()]
    add_r = _git(["add"] + [str(f) for f in existing_files])
    if add_r.returncode != 0:
        print("[error] git add 失敗：\n{0}".format((add_r.stdout or "") + (add_r.stderr or "")), file=sys.stderr)
        return 1
    commit_r = _git(["commit", "-m", commit_msg])
    if commit_r.returncode != 0:
        combined = (commit_r.stdout or "") + (commit_r.stderr or "")
        # 2026-09-07（P1-5）：resume 撞上「這份報告先前已 commit 成功，只是
        # 後續步驟（push／同步）中斷」時，nothing-to-commit 是預期狀態、
        # 不是錯誤——比照 `_sync_batch_site` 既有對批尾同步 commit 的同一種
        # 容忍；沒有這條，resume 會把已完成的副作用（commit）誤判成失敗，
        # 永遠卡在這一步、走不到重試 push。
        if "nothing to commit" in combined or "沒有要提交的變更" in combined:
            print("[finish] 無新變動可提交（先前已 commit 過），視為已完成，略過重複 commit")
        else:
            print("[error] git commit 失敗：\n{0}".format(combined), file=sys.stderr)
            return 1
    else:
        print("[ok] committed: {0}".format(commit_subject))
    # 2026-09-07：commit 後立即把 SHA 寫進 gitignored run manifest；
    # sync-later 仍保持 PENDING_SITE_SYNC，供下次開工補同步。
    commit_sha_r = _git(["rev-parse", "HEAD"])
    commit_sha = (commit_sha_r.stdout or "").strip() if commit_sha_r.returncode == 0 else ""
    manifest["finish"]["report_commit_sha"] = commit_sha or None
    manifest["finish"]["archived"] = True
    if not sync_later:
        manifest["finish"]["state"] = "COMMITTED"
    _atomic_write_json(manifest_path, manifest)

    status_r = _git(["status", "--porcelain"])
    modified_paths = [ln[3:] for ln in (status_r.stdout or "").splitlines() if ln.strip()]
    whitelist_set = set()
    for f in files:
        try:
            whitelist_set.add(str(Path(f).resolve().relative_to(REPO_ROOT)))
        except ValueError:
            whitelist_set.add(str(f))
    skipped = [p for p in modified_paths if p not in whitelist_set]
    print("[skip] 略過 {0} 個非白名單變動檔".format(len(skipped)))

    if no_push:
        manifest["finish"]["state"] = (
            "PENDING_SITE_SYNC" if sync_later else "COMPLETE_NO_PUSH")
        _atomic_write_json(manifest_path, manifest)
        print("[ok] --no-push，未推送")
        return 0

    ahead, behind = _git_ahead_behind()
    if behind > 0:
        if not commit_sha:
            rev_r = _git(["rev-parse", "HEAD"])
            commit_sha = (rev_r.stdout or "").strip()
        ok, reason = _push_head_via_worktree(commit_sha)
        if ok:
            manifest["finish"]["report_pushed_sha"] = commit_sha
            manifest["finish"]["state"] = (
                "PENDING_SITE_SYNC" if sync_later else "COMPLETE")
            _atomic_write_json(manifest_path, manifest)
            print(
                "[ok] 遠端領先 {0}，已透過 worktree cherry-pick 推送 "
                "origin/main（commit {1}）".format(behind, commit_sha[:12])
            )
            return 0
        print(
            "[HOLD] 遠端領先 {0}，worktree cherry-pick 推送失敗：{1}".format(
                behind, reason
            ),
            file=sys.stderr,
        )
        return 2
    push_r = _git(["push", "origin", "main"])
    if push_r.returncode != 0:
        print(
            "[error] git push 失敗：\n{0}".format(
                (push_r.stdout or "") + (push_r.stderr or "")
            ),
            file=sys.stderr,
        )
        return 1
    manifest["finish"]["report_pushed_sha"] = commit_sha or None
    manifest["finish"]["state"] = "PENDING_SITE_SYNC" if sync_later else "COMPLETE"
    _atomic_write_json(manifest_path, manifest)
    print("[ok] pushed to origin/main")
    return 0


def cmd_finish(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    return _do_finish(
        ticker, date,
        dry_run=args.dry_run, no_push=args.no_push, skip_dd_screener=args.skip_dd_screener,
        sync_later=getattr(args, "sync_later", False),
        accept_mismatch=getattr(args, "accept_mismatch", False),
    )


# ---------------------------------------------------------------------------
# WP1d run：串接 stage0 → judged → gated → brief → prose，支援 --until／--resume
# ---------------------------------------------------------------------------

def cmd_run(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"

    # 2026-09-07：獨立 run 開工前先補上次硬當留下的延後同步；batch 子行程
    # 由父 batch 在批首／批尾統一處理，避免退化成每檔重生一次。
    if not getattr(args, "dry_run", False) and os.environ.get("DD_BATCH_CHILD") != "1":
        # 2026-09-07：逃生口只略過本次開工，不修改或清除 pending state。
        pending_rc = _pending_sync_preflight(
            skip_pending_sync=getattr(args, "skip_pending_sync", False),
            no_push=getattr(args, "no_push", False),
        )
        if pending_rc != 0:
            return pending_rc

    replay_dir = _ensure_replay_env(args.replay_from)

    until_explicit = args.until is not None
    # 2026-09-11（WP-H2-1，計劃書第十一節）：**預設終點改 "prose"**——v19 的
    # 產物就是完整版，不再需要 `--full` 才跑散文層。`--full` 旗標保留但已成
    # no-op（既有呼叫端、batch 轉送與測試都還在傳它）。快速版（brief 段）
    # **暫不退役**：仍在 STAGE_ORDER 內照跑照產，等 H2 驗收通過由持有人拍板
    # 停產；在那之前 `--until brief` 仍是有效的停點。
    until = args.until or "prose"
    if until not in STAGE_ORDER:
        print("[error] --until 必須是 {0} 之一".format(STAGE_ORDER), file=sys.stderr)
        return 2
    until_idx = STAGE_ORDER.index(until)

    manifest = _load_json_or(manifest_path, {
        "ticker": ticker, "date": date, "state": "new", "created": _now(),
        "steps": [], "agents": [], "stages": {},
    })
    manifest.setdefault("stages", {})
    # 2026-09-07：已完成發布的 resume 是冪等 no-op，不再重做 archive／commit。
    if args.resume and (manifest.get("finish") or {}).get("state") in (
            "COMPLETE", "COMPLETE_NO_PUSH"):
        print("[resume] finish 已完成，無需重跑")
        return 0

    judgment_model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL
    global _JUDGE_MODE_OVERRIDE, _GATE_PATCH_MODE_OVERRIDE
    _JUDGE_MODE_OVERRIDE = getattr(args, "judge_mode", None)
    _GATE_PATCH_MODE_OVERRIDE = getattr(args, "gate_patch_mode", None)  # 2026-09-06
    no_delta = getattr(args, "no_delta", False)  # WP-C（2026-09-10）：強制整份重寫，不問 delta 路由

    start_idx = 0
    if args.resume:
        for i, name in enumerate(STAGE_ORDER):
            st = manifest["stages"].get(name, {})
            # 2026-09-07：v17 critic gate 與預設 brief 產物都不適用
            # SKIPPED；舊 manifest 若曾如此記錄，resume 必須重跑該段。
            stage_completed = st.get("state") == "PASS" or (
                name not in ("gated", "brief") and st.get("state") == "SKIPPED")
            if stage_completed:
                start_idx = i + 1
            else:
                break

    plan_kwargs = {
        "archetype": args.archetype, "peers": args.peers, "segments": None,
        "axes_per_batch": args.axes_per_batch, "offline": args.offline,
        "reuse_days": getattr(args, "reuse_days", REUSE_DAYS_DEFAULT),
    }

    rc = 0
    for i in range(start_idx, until_idx + 1):
        stage_name = STAGE_ORDER[i]
        # 2026-09-06：每段起訖與花費都在主 log 可見；結束值另寫回 manifest。
        print("[段落] {0} 開始 {1}".format(stage_name, _now()))
        # WP7b #5：`--resume` 落在這一段先前狀態為 FAIL（judged）或
        # FAIL／RUNNING（gated，涵蓋中斷於 spawn 之後、parse 之前的
        # gated_running）時，先重跑機械檢查（judge check／parse 既有
        # gate_audit.md）而非直接重派整段判斷／閘 agent。只在「--resume
        # 接續的第一段」判定，往後正常推進的段仍走全套流程。
        resuming_this_stage = (
            args.resume and i == start_idx
            and manifest["stages"].get(stage_name, {}).get("state")
            in (("FAIL",) if stage_name == "judged" else ("FAIL", "RUNNING"))
        )
        if stage_name == "stage0":
            rc = _do_stage0(ticker, date, plan_kwargs, replay_dir, args.accept_over_budget, manifest)
        elif stage_name == "judged":
            if resuming_this_stage:
                rc = _resume_judge_stage(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
            else:
                rc = _do_judge(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest,
                                no_delta=no_delta)
        elif stage_name == "gated":
            if resuming_this_stage:
                rc = _resume_gate_stage(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
            else:
                rc = _do_gate(ticker, date, judgment_model, replay_dir, args.accept_over_budget, manifest)
        elif stage_name == "brief":
            rc = _do_brief(ticker, date, args.full, manifest, dry_run=args.dry_run)
        elif stage_name == "prose":
            if resuming_this_stage:
                # 2026-09-08：比照 judged／gated，先跑零成本 prose check
                rc = _resume_prose_stage(ticker, date, manifest,
                                         accept_over_budget=args.accept_over_budget,
                                         dry_run=args.dry_run)
            else:
                rc = _do_prose_run(ticker, date, manifest, accept_over_budget=args.accept_over_budget, dry_run=args.dry_run)
        manifest = _load_json_or(manifest_path, manifest)
        st = manifest.get("stages", {}).get(stage_name, {})
        _record_stage_observation(manifest, stage_name)
        _atomic_write_json(manifest_path, manifest)
        # 2026-09-07：執行中的 gated／brief 只接受 PASS；SKIPPED 不得讓
        # 主鏈繼續到發布。其他真正 N/A 的段維持既有語意。
        stage_succeeded = st.get("state") == "PASS" or (
            stage_name not in ("gated", "brief") and st.get("state") == "SKIPPED")
        if not stage_succeeded:
            return rc if rc != 0 else 1

    # WP6a：run 預設接 finish；--no-finish／--dry-run／明講 --until 皆不接
    # （含明講 `--until brief`——語意上等同「就跑到這裡，先別 finish」）。
    # 2026-09-11（WP-H2-1）：預設終點已是 "prose"（完整版）。`until_explicit`
    # 仍是唯一的「使用者刻意要求停在這裡」判準；`--until prose` 明講時同樣
    # 不自動接 finish。
    if (not until_explicit) and until in ("brief", "prose") and not args.no_finish and not args.dry_run:
        return _do_finish(
            ticker, date,
            dry_run=False, no_push=args.no_push, skip_dd_screener=args.skip_dd_screener,
            sync_later=getattr(args, "sync_later", False),
            accept_mismatch=getattr(args, "accept_mismatch", False),
        )

    return rc


# ---------------------------------------------------------------------------
# 2026-09-06 batch：一條指令排一串 ticker 依序（不平行，避免 finish 的 git
# 互撞）各走一次完整 `run`（含 finish／push），持有人不需開互動 session 盯
# 進度、跑完只讀摘要。每檔用子行程呼叫本檔自己的 `run` 子命令（而不是同行程
# 內直接呼叫 `cmd_run`）——這樣每檔的 stdout／stderr 能乾淨分檔導出、且
# `_JUDGE_MODE_OVERRIDE`／`_GATE_PATCH_MODE_OVERRIDE` 這類 module-level
# override 不會跨檔互相污染。
# ---------------------------------------------------------------------------

def _resolve_batch_tickers(positional, from_file):
    """位置參數＋`--from-file` 合併、保序去重（大小寫正規化為大寫）。
    `--from-file` 每行一個 ticker，`#` 開頭整行略過，空行略過。"""
    items = list(positional or [])
    if from_file:
        text = Path(from_file).read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items.append(line)
    seen = set()
    out = []
    for t in items:
        tt = t.strip().upper()
        if not tt or tt in seen:
            continue
        seen.add(tt)
        out.append(tt)
    return out


def _manifest_has_quota_exhausted(manifest):
    """掃 manifest 每個 stage 的 `agent_usage`／`agent_usage_prior`（見
    `_fresh_stage_preserving_prior`），任一筆帶 `quota_exhausted: true`
    （見 `dd_headless.py` 對『訂閱額度耗盡』回覆的判定）即算命中。"""
    for stage in (manifest.get("stages") or {}).values():
        usage_list = list((stage or {}).get("agent_usage") or []) + list((stage or {}).get("agent_usage_prior") or [])
        for u in usage_list:
            if (u or {}).get("quota_exhausted"):
                return True
    return False


def _fmt_pct(v):
    return "{0:.1f}%".format(v) if isinstance(v, (int, float)) else "—"


def _batch_row_from_run_dir(ticker, date, run_dir, rc, elapsed_min, log_path):
    """讀一檔跑完後留在 run 目錄的 manifest／judgment／scenario_meta，收斂成
    一列摘要用的 dict。任一檔缺，對應欄位就是「—」（見 `_fmt_pct`），不是
    ddreport.py 這輪四項機械改動要動的『覆蓋規則』——單純讀值失敗容忍。"""
    run_dir = Path(run_dir)
    manifest = _load_json_or(run_dir / "manifest.json", {})
    judgment = _load_json_or(run_dir / "judgment.json", {})
    scenario_meta = _load_json_or(run_dir / "scenario_meta.json", {})
    decision_out = judgment.get("decision_out") or {}
    decision_inputs = judgment.get("decision_inputs") or {}
    verdict = decision_out.get("verdict") or "—"
    role = decision_out.get("role") or "—"
    ev5y = scenario_meta.get("ev5y_pct")
    if ev5y is None:
        ev5y = decision_inputs.get("ev5y_pct")
    irr_base = scenario_meta.get("irr_base_pct")
    if irr_base is None:
        irr_base = decision_inputs.get("irr_base_pct")
    # 2026-09-07（P2-3）：改用與 finish／HTML 發布契約同一個共用 helper
    # （`min(lo, hi)`），不再直取 `.lo`——lo／hi 次序異常時 batch 摘要才不會
    # 跟上站 dd-meta 兜不起來；不新增任何門檻，純換算法來源。
    max_dd = dd_metric_resolver.resolve_max_dd_pct(judgment)
    ledger = _build_token_ledger(manifest)
    ledger_line = _ledger_summary_line(ledger, _prior_usage_cache_read_total(manifest))
    # 2026-09-06：batch 摘要直接列分段牆鐘與列表成本，不必再逐檔翻 token.json。
    stage_times = []
    for stage_name in STAGE_ORDER:
        seconds = (ledger.get("by_stage", {}).get(stage_name) or {}).get("wall_seconds")
        if seconds is not None:
            stage_times.append("{0} {1:.1f}m".format(stage_name, seconds / 60.0))
    return {
        "ticker": ticker, "date": date,
        "state": manifest.get("state") or "—",
        "verdict": verdict, "role": role,
        "ev5y_pct": ev5y, "irr_base_pct": irr_base, "max_dd_pct": max_dd,
        "ledger": ledger, "ledger_line": ledger_line,
        "stage_times": "／".join(stage_times) or "—",
        "output_tokens": _ledger_output_total(ledger),  # 2026-09-10（WP-B）
        "cost_usd": (ledger.get("summary") or {}).get("cost_usd", 0.0),
        "elapsed_min": elapsed_min, "rc": rc,
        "log_path": str(log_path),
        "quota_hit": _manifest_has_quota_exhausted(manifest),
    }


def _build_batch_summary_md(rows, date, quota_stopped_ticker=None, remaining=None):
    lines = [
        "# DD batch 摘要 {0}".format(date), "",
        # 2026-09-10（WP-B）：加 output 欄（判斷段 Fable 的錢主要燒在輸出，
        # 只看 cache_read 會低估）；cost 欄原本就存在，來源不變
        # （`ledger.summary.cost_usd`，見 `_batch_row_from_run_dir`）。
        "| ticker | state | 裁決／角色 | 5Y EV | IRR base | Max DD | 全帳 | output | cost | 分段耗時 | 耗時(分) | rc | 備註 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    total_cache_read = 0
    total_output = 0
    total_elapsed = 0.0
    total_cost = 0.0
    ok_n = 0
    fail_n = 0
    for r in rows:
        verdict_role = "{0}／{1}".format(r["verdict"], r["role"])
        note = ""
        if r["rc"] != 0:
            note = "`python3 scripts/ddreport.py run {0} --date {1} --resume`".format(r["ticker"], r["date"])
        lines.append(
            "| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7:.1f}K | ${8:.2f} | {9} | {10:.1f} | {11} | {12} |".format(
                r["ticker"], r["state"], verdict_role,
                _fmt_pct(r["ev5y_pct"]), _fmt_pct(r["irr_base_pct"]), _fmt_pct(r["max_dd_pct"]),
                r["ledger_line"], r.get("output_tokens", 0) / 1000.0, r["cost_usd"],
                r["stage_times"], r["elapsed_min"], r["rc"], note,
            )
        )
        total_cache_read += _ledger_cache_read_total(r["ledger"])
        total_output += r.get("output_tokens", 0)
        total_elapsed += r["elapsed_min"]
        total_cost += r["cost_usd"]
        if r["rc"] == 0:
            ok_n += 1
        else:
            fail_n += 1
    lines.append("")
    lines.append(
        "總計：成功 {0}／失敗 {1}／總耗時 {2:.1f} 分／全帳合計 {3:.1f}M／output 合計 {4:.1f}K／"
        "列表成本 ${5:.2f}".format(
            ok_n, fail_n, total_elapsed, total_cache_read / 1_000_000.0,
            total_output / 1000.0, total_cost,
        )
    )
    if quota_stopped_ticker:
        lines.append("")
        lines.append(
            "⚠️ 訂閱額度耗盡，整批於 `{0}` 中斷。剩餘未跑：{1}。額度重置後接續（該檔先 `--resume`，"
            "其餘照跑）：".format(quota_stopped_ticker, "、".join(remaining or []) or "（無）")
        )
        lines.append("```")
        lines.append("python3 scripts/ddreport.py run {0} --date {1} --resume".format(quota_stopped_ticker, date))
        for t in (remaining or []):
            lines.append("python3 scripts/ddreport.py run {0} --date {1}".format(t, date))
        lines.append("```")
    return "\n".join(lines) + "\n"


def _write_batch_summary(rows, date, quota_stopped_ticker=None, remaining=None):
    md = _build_batch_summary_md(rows, date, quota_stopped_ticker=quota_stopped_ticker, remaining=remaining)
    path = BUILD_DIR / "batch_{0}.md".format(time.strftime("%Y%m%d_%H%M"))
    path.write_text(md, encoding="utf-8")
    return path


def _sync_batch_site(rows, date, no_push=False, skip_dd_screener=False):
    """2026-09-07：批尾與崩潰補償共用的可恢復網站同步。"""
    completed = [r for r in rows if r.get("rc") == 0]
    if not completed:
        return 0
    if skip_dd_screener:
        # 2026-09-07：latest.json 是發布必要集合，批尾不得用 maintenance
        # 旗標把它略過；pending 保留供下次正常補同步。
        _mark_sync_rows(completed, "FAIL", note="--skip-dd-screener 不允許於發布同步")
        print("[error] batch-sync 不允許 --skip-dd-screener；必要同步包含 latest.json",
              file=sys.stderr)
        return 1

    tickers = []
    appended_rows = []
    # 2026-09-07：批尾同步的 research 主表也要與 INDEX 一起具備失敗回復。
    research_snapshot = _snapshot_file(RESEARCH_BODY_PATH)
    _mark_sync_rows(completed, "PENDING")
    resolved = []
    for row in completed:
        ticker = row["ticker"]
        manifest = _load_json_or(_run_dir(ticker, row["date"]) / "manifest.json", {})
        html_path = _finish_target_html(ticker, row["date"], manifest)
        if not html_path.exists():
            # 2026-09-07：已標完成的報告若不存在，不能產生缺頁連結後仍把
            # pending 清成 PASS；保留 FAIL 讓下一次補同步重試。
            note = "找不到待同步報告：{0}".format(html_path)
            _mark_sync_rows(completed, "FAIL", note=note)
            print("[error] {0}".format(note), file=sys.stderr)
            return 1
        resolved.append((row, ticker, html_path))

    for _row, ticker, html_path in resolved:
        fields = _index_row_fields(html_path)
        if _append_index_row(fields["row"], fields["file_cell"]):
            appended_rows.append(fields["row"])
        if ticker not in tickers:
            tickers.append(ticker)

    py = _pick_python()
    cmd = [py, str(SCRIPTS_DIR / "update_dd_index.py")]
    r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    sync_output = ((r.stdout or "") + (r.stderr or "")).strip()
    if r.returncode != 0:
        for appended_row in reversed(appended_rows):
            _remove_index_row(appended_row)
        _restore_file_snapshot(RESEARCH_BODY_PATH, research_snapshot)
        _mark_sync_rows(
            completed, "FAIL", note="update_dd_index.py rc={0}".format(r.returncode))
        print("[error] batch 尾 update_dd_index.py 失敗（rc={0}）：\n{1}".format(
            r.returncode, sync_output[-4000:] or "（無輸出）"), file=sys.stderr)
        return 1
    _mark_sync_rows(completed, "GENERATED")
    # 2026-09-07：optional cascade 的失敗彙總在 batch-sync 尾端重印。
    for line in sync_output.splitlines():
        if line.startswith("[sync-summary]"):
            print(line)

    files = [INDEX_MD_PATH, RESEARCH_BODY_PATH, PICKS_CANDIDATES_PATH,
             TICKER_HUB_DIR / "index.html"]
    if not skip_dd_screener:
        files.append(DD_SCREENER_LATEST_PATH)
    files.extend(TICKER_HUB_DIR / "{0}.html".format(t) for t in tickers)
    existing_files = [f for f in files if Path(f).exists()]
    add_r = _git(["add"] + [str(f) for f in existing_files])
    if add_r.returncode != 0:
        for appended_row in reversed(appended_rows):
            _remove_index_row(appended_row)
        _mark_sync_rows(completed, "FAIL", note="batch-sync git add 失敗")
        print("[error] batch-sync git add 失敗：\n{0}".format(
            (add_r.stdout or "") + (add_r.stderr or "")), file=sys.stderr)
        return 1

    subject = "Sync DD batch {0}（{1} 檔；research+screener once）".format(date, len(tickers))
    commit_r = _git(["commit", "-m", subject])
    sync_commit_sha = ""
    if commit_r.returncode != 0:
        combined = (commit_r.stdout or "") + (commit_r.stderr or "")
        if "nothing to commit" in combined or "沒有要提交的變更" in combined:
            print("[batch-sync] 無新衍生變動，略過 commit")
        else:
            for appended_row in reversed(appended_rows):
                _remove_index_row(appended_row)
            _mark_sync_rows(completed, "FAIL", note="batch-sync git commit 失敗")
            print("[error] batch-sync git commit 失敗：\n{0}".format(combined), file=sys.stderr)
            return 1
    else:
        print("[ok] batch-sync committed: {0}".format(subject))
    # 2026-09-07：commit 與 nothing-to-commit 復原路徑都記 HEAD，讓 push
    # 中斷可由同一個 COMMITTED state 接續。
    rev_r = _git(["rev-parse", "HEAD"])
    if rev_r.returncode == 0:
        sync_commit_sha = (rev_r.stdout or "").strip()
    _mark_sync_rows(completed, "COMMITTED", note=sync_commit_sha or None)

    if no_push:
        _mark_sync_rows(completed, "PASS", no_push=True)
        print("[ok] batch-sync --no-push，未推送")
        return 0
    ahead, behind = _git_ahead_behind()
    if behind > 0:
        rev_r = _git(["rev-parse", "HEAD"])
        commit_sha = (rev_r.stdout or "").strip()
        ok, reason = _push_head_via_worktree(commit_sha)
        if ok:
            _mark_sync_rows(completed, "PASS")
            print("[ok] batch-sync 遠端領先 {0}，worktree 推送完成".format(behind))
            return 0
        print("[HOLD] batch-sync 遠端領先 {0}：{1}".format(behind, reason), file=sys.stderr)
        return 2
    push_r = _git(["push", "origin", "main"])
    if push_r.returncode != 0:
        print("[error] batch-sync git push 失敗：\n{0}".format(
            (push_r.stdout or "") + (push_r.stderr or "")), file=sys.stderr)
        return 1
    _mark_sync_rows(completed, "PASS")
    print("[ok] batch-sync pushed to origin/main")
    return 0


def cmd_batch(args):
    tickers = _resolve_batch_tickers(args.tickers, args.from_file)
    if not tickers:
        print("[error] 沒有任何 ticker（位置參數與 --from-file 都是空的）", file=sys.stderr)
        return 1

    date = args.date or time.strftime("%Y%m%d")
    # 2026-09-07：批次開工前先清掉上輪崩潰留下的 pending，同一狀態機
    # 隨後也供本批批尾結清。
    # 2026-09-07：batch 與單跑共用逃生語意；不清除既有 pending。
    pending_rc = _pending_sync_preflight(
        skip_pending_sync=args.skip_pending_sync, no_push=args.no_push)
    if pending_rc != 0:
        return pending_rc
    log_dir = BUILD_DIR / "batch_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    py = _pick_python()
    script_path = str(Path(__file__).resolve())
    n = len(tickers)
    rows = []

    for i, t in enumerate(tickers, start=1):
        print("[batch] {0}/{1} {2} 開始 {3}".format(i, n, t, time.strftime("%H:%M")))
        log_path = log_dir / "{0}_{1}.log".format(t, date)
        cmd = [py, script_path, "run", t, "--date", date]
        # 2026-09-06：每檔只 finish 報告；聚合頁在整批結尾同步一次。
        cmd.append("--sync-later")
        if args.full:
            cmd.append("--full")
        if args.judgment_model:
            cmd += ["--judgment-model", args.judgment_model]
        if args.judge_mode:
            cmd += ["--judge-mode", args.judge_mode]
        if args.gate_patch_mode:
            cmd += ["--gate-patch-mode", args.gate_patch_mode]
        if args.no_push:
            cmd.append("--no-push")
        if args.resume:
            cmd.append("--resume")

        t0 = time.time()
        with open(log_path, "w", encoding="utf-8") as lf:
            child_env = dict(os.environ)
            child_env["DD_BATCH_CHILD"] = "1"
            r = subprocess.run(
                cmd, stdout=lf, stderr=subprocess.STDOUT, cwd=str(REPO_ROOT), env=child_env)
        elapsed_min = (time.time() - t0) / 60.0

        run_dir = _run_dir(t, date)
        row = _batch_row_from_run_dir(t, date, run_dir, r.returncode, elapsed_min, log_path)
        rows.append(row)
        print("[batch] {0}/{1} {2} 結束 rc={3} state={4}".format(i, n, t, r.returncode, row["state"]))

        try:
            log_text = log_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            log_text = ""
        if row["quota_hit"] or "訂閱額度耗盡" in log_text:
            remaining = tickers[i:]
            sync_rc = _sync_batch_site(
                rows, date, no_push=args.no_push,
                skip_dd_screener=getattr(args, "skip_dd_screener", False),
            )
            summary_path = _write_batch_summary(rows, date, quota_stopped_ticker=t, remaining=remaining)
            print("[batch] 額度耗盡，整批停下（{0}）".format(t))
            print(summary_path)
            if sync_rc != 0:
                return sync_rc
            return 3

    sync_rc = _sync_batch_site(
        rows, date, no_push=args.no_push,
        skip_dd_screener=getattr(args, "skip_dd_screener", False),
    )
    summary_path = _write_batch_summary(rows, date)
    print(summary_path)
    if sync_rc != 0:
        return sync_rc
    return 0 if all(r["rc"] == 0 for r in rows) else 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="ddreport.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("ticker")
    pl.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    pl.add_argument("--archetype", default=None)
    pl.add_argument("--peers", default=None)
    pl.add_argument("--segments", default=None)
    pl.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    pl.add_argument("--reuse-days", type=int, default=REUSE_DAYS_DEFAULT,
                    help="表上未列軸的預設沿用上限（見 COVERAGE_REUSE_POLICY）；0＝全部不沿用（2026-09-06；2026-09-10 改按軸失效）")
    pl.add_argument("--offline", action="store_true")
    pl.set_defaults(func=cmd_plan)

    st = sub.add_parser("status")
    st.add_argument("ticker")
    st.add_argument("date")
    st.set_defaults(func=cmd_status)

    rn = sub.add_parser("run")
    rn.add_argument("ticker")
    rn.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    rn.add_argument("--archetype", default=None)
    rn.add_argument("--peers", default=None)
    rn.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    rn.add_argument("--reuse-days", type=int, default=REUSE_DAYS_DEFAULT,
                    help="表上未列軸的預設沿用上限（見 COVERAGE_REUSE_POLICY）；0＝全部不沿用（2026-09-06；2026-09-10 改按軸失效）")
    rn.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    rn.add_argument("--judge-mode", default=None, choices=["short", "loop"],
                    help="判斷段跑法：short（預設，只給 Write、≤4 輪，check 由 orchestrator 跑）／loop（舊：agent 自己 Write＋check＋修）")
    rn.add_argument("--gate-patch-mode", default=None, choices=["patchmap", "loop"],
                    help="閘 🔴 修補跑法：patchmap（預設，無工具單輪回 patch map）／loop（舊：agent 自己 Read／Write／Bash＋重跑 check）")  # 2026-09-06
    rn.add_argument("--full", action="store_true",
                     help="（2026-09-11 起 no-op）預設終點已是 prose 完整版；旗標保留只為"
                          "相容既有呼叫端與 batch 轉送，不再改變行為")
    rn.add_argument("--replay-from", default=None, metavar="DIR")
    rn.add_argument("--until", default=None, choices=STAGE_ORDER,
                     help="預設跑到 prose（完整版）並自動接 finish；明講此旗標（含 --until prose）"
                          "視為刻意要求停在該段，不自動接 finish")
    rn.add_argument("--resume", action="store_true")
    rn.add_argument("--offline", action="store_true")
    rn.add_argument("--accept-over-budget", action="store_true")
    rn.add_argument("--no-finish", action="store_true", help="跑到預設終點（prose）後不自動接 finish")
    rn.add_argument("--dry-run", action="store_true", help="同 --no-finish；WP6a 精神對齊")
    rn.add_argument("--no-push", action="store_true", help="finish 時 commit 但不 push")
    rn.add_argument("--skip-dd-screener", action="store_true",
                     help="maintenance 相容旗標；發布 finish 會拒絕")  # 2026-09-07
    rn.add_argument("--sync-later", action="store_true",
                    help="只 commit／push 本檔與存查；INDEX／研究頁／screener 延後同步")  # 2026-09-06
    rn.add_argument("--skip-pending-sync", action="store_true",
                    help="只略過本次開工前的 pending 補同步；不清除 pending")  # 2026-09-07
    rn.add_argument("--accept-mismatch", action="store_true",
                    help="僅持有人明確放行時使用；三方原值會寫入 manifest")  # 2026-09-07
    rn.add_argument("--no-delta", action="store_true",
                     help="WP-C：判斷段強制整份重寫（有 prior 存查時預設改走複審 delta 路由；"
                          "見 _judge_delta_route）")
    rn.set_defaults(func=cmd_run)

    s0 = sub.add_parser("stage0")
    s0.add_argument("ticker")
    s0.add_argument("--date", default=None)
    s0.add_argument("--archetype", default=None)
    s0.add_argument("--peers", default=None)
    s0.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    s0.add_argument("--reuse-days", type=int, default=REUSE_DAYS_DEFAULT,
                    help="表上未列軸的預設沿用上限（見 COVERAGE_REUSE_POLICY）；0＝全部不沿用（2026-09-06；2026-09-10 改按軸失效）")
    s0.add_argument("--offline", action="store_true")
    s0.add_argument("--replay-from", default=None, metavar="DIR")
    s0.add_argument("--accept-over-budget", action="store_true")

    def _cmd_stage0(args):
        ticker = args.ticker.strip().upper()
        date = args.date or time.strftime("%Y%m%d")
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        plan_kwargs = {"archetype": args.archetype, "peers": args.peers, "segments": None,
                       "axes_per_batch": args.axes_per_batch, "offline": args.offline,
                       "reuse_days": args.reuse_days}
        return _do_stage0(ticker, date, plan_kwargs, replay_dir, args.accept_over_budget, manifest)

    s0.set_defaults(func=_cmd_stage0)

    jg = sub.add_parser("judge")
    jg.add_argument("ticker")
    jg.add_argument("date")
    jg.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    jg.add_argument("--judge-mode", default=None, choices=["short", "loop"])
    jg.add_argument("--replay-from", default=None, metavar="DIR")
    jg.add_argument("--accept-over-budget", action="store_true")
    jg.add_argument("--no-delta", action="store_true",
                     help="WP-C：強制整份重寫，不問複審 delta 路由（即使有 prior 存查）")
    jg.add_argument("--contract", default="v19", choices=["v19", "v18"],
                     help="判斷契約（WP-H2-3 成對測試用）：v19＝預設瘦身包；v18＝同一份證據"
                          "改用舊包再判一次。兩次共用同一個 run 目錄，產物以 *_v19.json／"
                          "*_v18.json 快照區分；v18 一律整份重判（不走 delta／reuse）。")

    def _cmd_judge(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL
        global _JUDGE_MODE_OVERRIDE, _JUDGE_CONTRACT_OVERRIDE
        _JUDGE_MODE_OVERRIDE = args.judge_mode
        _JUDGE_CONTRACT_OVERRIDE = getattr(args, "contract", None)
        return _do_judge(ticker, date, model, replay_dir, args.accept_over_budget, manifest,
                          no_delta=args.no_delta)

    jg.set_defaults(func=_cmd_judge)

    ga = sub.add_parser("gate")
    ga.add_argument("ticker")
    ga.add_argument("date")
    ga.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    ga.add_argument("--gate-patch-mode", default=None, choices=["patchmap", "loop"],
                     help="閘 🔴 修補跑法：patchmap（預設，無工具單輪回 patch map，orchestrator 代套用＋代跑 check）"
                          "／loop（舊：agent 自己 Read／Write／Bash＋重跑 check）")  # 2026-09-06
    ga.add_argument("--replay-from", default=None, metavar="DIR")
    ga.add_argument("--accept-over-budget", action="store_true")

    def _cmd_gate(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        replay_dir = _ensure_replay_env(args.replay_from)
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        model = args.judgment_model or manifest.get("judgment_model") or DEFAULT_JUDGMENT_MODEL
        global _GATE_PATCH_MODE_OVERRIDE
        _GATE_PATCH_MODE_OVERRIDE = args.gate_patch_mode  # 2026-09-06
        return _do_gate(ticker, date, model, replay_dir, args.accept_over_budget, manifest)

    ga.set_defaults(func=_cmd_gate)

    br = sub.add_parser("brief")
    br.add_argument("ticker")
    br.add_argument("date")
    br.add_argument("--full", action="store_true",
                     help="v17 WP4b 起此旗標在獨立的 brief 子命令上不生效（見 `_do_brief`）；"
                          "完整版另跑 `python3 scripts/ddreport.py prose run TICKER DATE`")
    br.add_argument("--dry-run", action="store_true",
                     help="輸出到 run 目錄內 brief.html，不寫 docs/dd/brief/")

    def _cmd_brief(args):
        ticker = args.ticker.strip().upper()
        date = args.date
        manifest = _load_json_or(_run_dir(ticker, date) / "manifest.json", {
            "ticker": ticker, "date": date, "state": "new", "created": _now(),
            "steps": [], "agents": [], "stages": {},
        })
        return _do_brief(ticker, date, args.full, manifest, dry_run=args.dry_run)

    br.set_defaults(func=_cmd_brief)

    ir = sub.add_parser("index-row")
    ir.add_argument("--html", required=True, metavar="FILE")
    ir.add_argument("--append", action="store_true")
    ir.set_defaults(func=cmd_index_row)

    fi = sub.add_parser("finish")
    fi.add_argument("ticker")
    fi.add_argument("date")
    fi.add_argument("--dry-run", action="store_true")
    fi.add_argument("--no-push", action="store_true")
    fi.add_argument("--skip-dd-screener", action="store_true")
    fi.add_argument("--sync-later", action="store_true",
                    help="只 commit／push 本檔與存查；INDEX／研究頁／screener 延後同步")  # 2026-09-06
    fi.add_argument("--accept-mismatch", action="store_true",
                    help="僅持有人明確放行時使用；三方原值會寫入 manifest")  # 2026-09-07
    fi.set_defaults(func=cmd_finish)

    # 2026-09-06：batch——一條指令排一串 ticker 依序各跑一次完整 `run`。
    ba = sub.add_parser("batch")
    ba.add_argument("tickers", nargs="*", help="依序跑的 ticker 清單（可與 --from-file 合併去重）")
    ba.add_argument("--from-file", default=None, metavar="LIST.txt",
                     help="每行一個 ticker，# 開頭整行略過")
    ba.add_argument("--date", default=None, help="YYYYMMDD；預設今天，所有 ticker 共用同一天")
    ba.add_argument("--full", action="store_true")
    ba.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    ba.add_argument("--judge-mode", default=None, choices=["short", "loop"])
    ba.add_argument("--gate-patch-mode", default=None, choices=["patchmap", "loop"])
    ba.add_argument("--no-push", action="store_true")
    ba.add_argument("--skip-dd-screener", action="store_true",
                    help="maintenance 相容旗標；發布 batch-sync 會拒絕")  # 2026-09-07
    ba.add_argument("--skip-pending-sync", action="store_true",
                    help="只略過本次批首 pending 補同步；不清除 pending")  # 2026-09-07
    ba.add_argument("--resume", action="store_true",
                     help="透傳給每一檔的 `run --resume`（批次本身不記自己的續跑點，續跑靠各檔 manifest）")
    ba.set_defaults(func=cmd_batch)

    # 2026-09-06 WP4b：`gates` 是單一 ticker/date 直達命令（同 `finish`／
    # `brief`），不像 `prose` 底下還分 prepare/split/check/run 四個動作，故
    # 正常掛進 argparse 即可，不需要 `prose` 那種 pre-dispatch。
    ga2 = sub.add_parser("gates", help="v17 WP4b：dd_gates.sh 的 Python 化版本，回 sid 清單＋原因")
    ga2.add_argument("ticker")
    ga2.add_argument("date")
    ga2.add_argument("--out", default=None, help="輸出 HTML 路徑（預設 run 目錄內 DD_preview.html）")
    ga2.add_argument("--postprocess", action="store_true",
                      help="組裝後跑 site_nav/primer/livebar（預設關，只在最終定案輸出到 docs/ 時開）")
    ga2.set_defaults(func=cmd_gates)

    return p


def main(argv):
    argv = list(argv)
    # `judge check TICKER DATE` 是給 spawn 出去的判斷 agent（透過 Bash 工具）與
    # orchestrator 共用的獨立子命令，前置獨立判斷比硬塞進 argparse 巢狀
    # subparsers（`judge`／`judge check` 位置參數數量會互相打架）簡單可靠。
    if len(argv) >= 3 and argv[0] == "judge" and argv[1] == "check":
        ns = argparse.Namespace(ticker=argv[2], date=argv[3] if len(argv) > 3 else None)
        return cmd_judge_check(ns)

    # 2026-09-06 WP4b：`prose {prepare,split,check,run} TICKER DATE` 同樣
    # 前置獨立判斷——`prose` 底下四個子動作若掛進 argparse 巢狀 subparsers
    # 會與「ticker 剛好叫 check/split/…」這種邊界案例打架（同上 `judge
    # check` 的理由），且 `prose --help`／裸 `prose` 需要一段可讀的說明，
    # 這裡直接印，不強求擠進 argparse 的 --help 機制。
    if argv[:1] == ["prose"]:
        rest = argv[1:]
        if not rest or rest[0] in ("-h", "--help"):
            print(_PROSE_HELP)
            return 0
        sub_cmd = rest[0]
        fn = {"prepare": cmd_prose_prepare, "split": cmd_prose_split,
              "check": cmd_prose_check, "run": cmd_prose_run}.get(sub_cmd)
        if fn is None:
            print("prose：未知子命令 {0!r}（可用：prepare/split/check/run）".format(sub_cmd), file=sys.stderr)
            return 2
        if len(rest) < 3:
            print("用法：ddreport.py prose {0} TICKER DATE".format(sub_cmd), file=sys.stderr)
            return 2
        ticker, date = rest[1], rest[2]
        extra = rest[3:]
        ns = argparse.Namespace(
            ticker=ticker, date=date,
            dry_run=("--dry-run" in extra),
            accept_over_budget=("--accept-over-budget" in extra),
        )
        return fn(ns)

    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
