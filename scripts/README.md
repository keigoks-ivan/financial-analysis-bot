# scripts/

## Git pre-commit hook（dd/id-meta validator + .nojekyll guard）

Repo 內建 pre-commit hook 在 `scripts/hooks/pre-commit`，commit 前自動跑 `validate_dd_meta.py` + `validate_id_meta.py` + `validate_supply_chain_meta.py` + `validate_cache_schema.py`，不過違反 schema 的檔案無法 push（鏡像 GitHub Actions strict gate 在本機提早攔截）。只在 staged files 觸及對應路徑或 validator script 本身時才跑，其他 commit 無感。

**.nojekyll guard**：每次 commit hook 一律檢查 `docs/.nojekyll` 存在 + 沒被刪除 staged。這檔讓 GitHub Pages 跳過 Jekyll，是站存活的硬性條件（2026-05-26 incident：1609-file `docs/` 把 Jekyll 跑到 timeout，連 3 個 build errored）。刪除會被擋。

**新機器 / 新 clone 啟用：**

```bash
bash scripts/install_hooks.sh
```

只跑這一次（會把 `core.hooksPath` 指向 `scripts/hooks/`）。Bypass：`git commit --no-verify`。Uninstall：`git config --unset core.hooksPath`。

## `dd_sections.py`（v15.2 DD 章節工具，唯一權威）

`docs/dd/DD_*.html`（v15）canonical section id 的單一 source of truth：`s1`…`s14`（§13 用 `decision`）、`s85`（§8.5，選填）、`appA`/`appB`、`revlog`/`sources`（選填）、`dashboard`（`<div class="topbar">` 到 `<nav class="dd-toc">` 之前）、`dd-meta`。舊檔缺 canonical id（例：SE 系列的 §1-§14 落在 `<h2 id="sN">` 而非 `<section id="sN">`、附錄用 `id="appxA"` 而非 `appA`）時，`bytes`/`text`/`extract` 會用 `<h2>`／`<summary>` 文字中的 `§N`／「附錄 A」推斷位置；`replace` 只認實際 `id=` 屬性、恰好命中 1 次才動手，找不到就 exit 2，不做危險猜測。

```bash
python3 scripts/dd_sections.py bytes FILE [--json] [--strict]   # 每段 bytes/預算/狀態 + §2.1 彙總列
python3 scripts/dd_sections.py text FILE [IDS]                  # 可讀純文字（critic/patch 用），IDS 逗號分隔可省略
python3 scripts/dd_sections.py extract FILE IDS                 # 原始 HTML 片段（含外層 wrapper），多個 id 用逗號分隔
python3 scripts/dd_sections.py replace FILE ID NEWFILE          # 整段替換（NEWFILE 須含相同 id wrapper）
python3 scripts/dd_sections.py leaks FILE                       # 可見正文機器語言掃描（QC-40 sweep 的唯一權威詞表）
```

同時是可 import 的模組（`qc.py` 用 `section_bytes()`／`leak_hits()` 做 v15 DD 的 warning/error 判定）：`section_bytes(html)`、`leak_hits(html)`、`split_sections(html)`、`readable_text(html, ids=None)`、`extract(html, ids)`、`replace(html, id, new_block)`。KB 換算採本 repo既有慣例（1 KB = 1000 bytes，對齊 `scripts/hooks/pre-commit` 的 70000/80000/115000）。

## `render_dd.py`（v15.2 BODY ↔ 完整 HTML 組裝器）

```bash
python3 scripts/render_dd.py BODY -o docs/dd/DD_{T}_{D}.html [--no-postprocess]
python3 scripts/render_dd.py --to-body docs/dd/DD_X.html -o BODY   # 既有完整 HTML -> BODY（含 legacy id 正規化）
python3 scripts/render_dd.py --check docs/dd/DD_X.html             # 回歸測試：to-body 再 render，diff 可讀文字
```

Writer 只產出 BODY 檔（放 `.dd_build/`，已 gitignore）：`dd-meta` script → `<!-- TITLE: ... -->` → `<!-- SOURCES: ... -->` → dashboard 區 → `s1`…`appB`/`revlog`/`sources`。`render_dd.py` 補齊 `<head>`（含內嵌 `scripts/dd_template/dd.css`）、自動產生 `<nav class="dd-toc">`、頁尾與列印按鈕，預設接著依序跑三個 post-process 注入器：`site_nav.process()`（全站導覽）、`inject_report_primer.inject_one()`（怎麼讀導讀塊）、`inject_dd_livebar.inject_one()`（即時失效條）——三者皆冪等、單檔可重跑。`--to-body` 反向拆解既有報告時，若章節 id 落在 `<h2>`（無 `<section>` 包裹）或用了非 canonical 的 `id`（如 `appxA`），會就地正規化成 `<section id="sN">`／`<details id="appA">`。`--check` 用可見文字（`dd_sections.readable_text`）比對而非逐 byte diff，容許 toc 文字措辭與頁尾格式差異（見對應 skill 文件）。

**Exit code 語意**：render 本體（BODY 組裝失敗，如缺 dd-meta／找不到任何 section id／BODY 混入完整 HTML 骨架）失敗＝`exit 2`。post-process 三步（`site_nav`／`primer`／`livebar`）永遠不會讓整支腳本失敗——本機 `python3` 若是 3.9（`site_nav.py` 的 f-string 語法需要 3.12+），會自動 fallback 成 `subprocess` 呼叫候選直譯器（依序：`/tmp/ddvenv/bin/python`、`/opt/homebrew/bin/python3.12`、PATH 上的 `python3.12`）在子行程內 import 該模組並呼叫同一個單檔函式（三支腳本都沒有真正的單檔 CLI，不能加、也不准改 `site_nav.py` 本身，所以 fallback 走 `python3.12 -c "import ...; 模組.函式(path)"` 而非走 argparse）；三個候選都不可用時印 `WARN: post-process {name} skipped（需 py3.12）` 到 stderr 並繼續，仍是 `exit 0`（nav／primer／livebar 之後可由 `update_dd_index.py` 或 site_nav 全站 apply 補上）。

**`dd-render` provenance marker**：`render_dd.py` 組出的 `<head>` 一律含 `<meta name="dd-render" content="render_dd-v15.2">`（刻意不含「stock-analyst v」／「DD Schema v」字樣，避免撞 `verify_dd_math.py` 檢查 D 的版本戳 regex；已用 `python3 scripts/verify_dd_math.py` 對 render 產物驗證仍 pass）。`qc.py` check 6 用它區分「這份 v15 新檔真的是 render_dd.py 剛組出來的」vs「delta-refresh `cp` 舊 v15.0 檔到新日期檔名再 patch」——後者雖然對 git 來說也是整檔新增，但正文是舊報告的、本來就帶 25–40 筆既有 leaks，不該被當成「全新報告」擋下；只有「changed 模式＋整檔新增＋帶 `dd-render` marker」三者同時成立才會把 leaks 升級為 error，其餘一律 warning。
