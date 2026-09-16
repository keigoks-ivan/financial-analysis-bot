# dd_simple 工作單：EPS 口徑在資料層統一（2026-09-12）

目的：下一檔不再出現「兩套 EPS 口徑混用」。不加模型規則，改在程式與資料層把口徑統一，模型不再需要選。

背景：2026-09-11 TSM 三次實跑，Opus 三次都卡在同一件事——Koyfin 匯出的 EPS 是普通股口徑（FY1 3.41），
台積電 ADR＝5 股普通股，正確 ADR 口徑約 17.05；另一來源（SimplyWallSt）直接給 ADR 口徑 15.91。
事實表把兩者並列成「衝突」交給模型，模型在基期與預測年各挑了一套，年增率就錯了。

## 任務 1：收證據端加 ADR 換算（單一權威、零模型）

1. 找出 Koyfin EPS 快照進入 DD 證據的讀取點：`scripts/dd_numbers_extra.py`（產 `numbers.consensus_revision`、
   `valuation_history.fwd_recent_window`）與 `scripts/build_dd_screener.py`（產 `eps_fy_curr/next/fy3`）。
   兩邊如果各自讀 Excel，抽成一個共用讀取函式；不要在兩處各寫一份換算。
2. 新增一張 ADR 換算表（純資料檔，例如 `data/adr_ratios.json`）：`{"TSM": {"ratio": 5, "basis": "1 ADR = 5 ordinary", "source": "…", "checked": "2026-09-12"}}`。
   只收「Koyfin 口徑 ≠ ADR 口徑」的 ticker。候選怎麼找：對 DD 母體逐檔比較 Koyfin FY1 與 yfinance trailing EPS，
   比值 > 2 或 < 0.5 的列出來，再逐一查證 ADR 比率後才寫進表；查不到來源的不寫、不猜。
3. 讀取函式套用換算後，輸出要帶 `eps_basis` 註記（如 `"adr-usd (koyfin ordinary ×5)"`），讓事實表與正文都看得到口徑。
4. 非 ADR ticker 一個 byte 都不能變。用既有 fixture 跑回歸證明。
5. **不重生 `docs/`、不 commit、不 push。** 公開篩選器 `latest.json` 這次不動。
6. 為 TSM 這個 run 補資料（零模型）：重跑 `dd_numbers_extra.py` 到 `.dd_build/runs/TSM_20260911/parts/numbers_extra.json`，
   用小腳本把 `evidence.json` 的 `numbers` 區塊與 `facts.json` 裡 `f_consensus_eps_fy1/fy2/fy3`、`f_fwd_pe_latest`、
   `f_consensus_rev_*` 對應更新，刪掉 `.dd_build/runs/TSM_20260911/source_snapshot.json`（讓下次研究重新凍結）。
   更新前先備份成 `*_pre_adr.json`。改完印出：TSM FY1/FY2/FY3 新值、fwd PE 新值（應約 25x，不是 125x）。

驗收（全部要印出來）：
- `python3 -m pytest scripts/tests -q -k "numbers_extra or screener or dd_simple"` 全過；新增測試至少覆蓋「ADR 換算」「非 ADR 不變」「eps_basis 註記」。
- TSM 事實表 f_consensus_eps_fy1 ≈ 17.05、f_fwd_pe_latest ≈ 25。
- `git status --short` 只列出你動的檔。

## 任務 2：`scripts/dd_simple.py` 把能算的數字改成程式填

現在 `inputs.json` 由模型填 `base_eps_path`、`scenario.price`、`scenario.start.eps/pe`。改成程式從事實表填，模型不碰：

1. `price` ＝ `f_price_at_dd`；`start.pe` ＝ `f_pe_current`；`start.eps` ＝ price ÷ pe（標 TTM）。
2. `base_eps_path` ＝ 基期實際（事實表若有年度 EPS 實際值就用，沒有就用 TTM 並標明）＋ FY+1E／FY+2E／FY+3E（f_consensus_eps_fy1/2/3，任務 1 換算後的口徑）＋ `source`。
3. 這些欄從 `INPUTS_SPEC` 拿掉，`validate_inputs` 不再要求；`cmd_calc` 組 scenario 時由程式注入；`_prose_prompt` 把這張 EPS 錨點表當已知數附給模型，並要求 §6 的 EPS 路徑表直接沿用。
4. `build_dd_meta` 的 `base_eps_path`／`eps_basis` 改讀程式填的值。
5. 離線測試：用 `.dd_build/runs/TSM_20260911_st/` 既有 fixture 跑 `calc` 與 `render`，確認情境樹、裁決、篩選器接線都還通；
   `scripts/tests/test_dd_skill_screener.py` 與 `test_dd_redesign.py` 不能退步。

驗收：印出程式填好的 EPS 錨點表（TSM），以及 `python3 scripts/dd_simple.py calc TSM 20260911_st` 與 `render` 的輸出。

## 不做

不改 `ddreport.py`、不改 skill 檔、不加任何「模型要注意 X」的規則句、不跑任何模型呼叫、不 commit、不 push。
改動集中在：Koyfin EPS 讀取函式、ADR 表、`dd_simple.py`、對應測試、TSM run 目錄的資料檔。

回報：每個任務改了哪些檔（路徑＋行數）、驗收輸出原文、沒做到的部分與原因。
