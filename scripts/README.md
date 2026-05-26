# scripts/

## Git pre-commit hook（dd/id-meta validator + .nojekyll guard）

Repo 內建 pre-commit hook 在 `scripts/hooks/pre-commit`，commit 前自動跑 `validate_dd_meta.py` + `validate_id_meta.py` + `validate_supply_chain_meta.py` + `validate_cache_schema.py`，不過違反 schema 的檔案無法 push（鏡像 GitHub Actions strict gate 在本機提早攔截）。只在 staged files 觸及對應路徑或 validator script 本身時才跑，其他 commit 無感。

**.nojekyll guard**：每次 commit hook 一律檢查 `docs/.nojekyll` 存在 + 沒被刪除 staged。這檔讓 GitHub Pages 跳過 Jekyll，是站存活的硬性條件（2026-05-26 incident：1609-file `docs/` 把 Jekyll 跑到 timeout，連 3 個 build errored）。刪除會被擋。

**新機器 / 新 clone 啟用：**

```bash
bash scripts/install_hooks.sh
```

只跑這一次（會把 `core.hooksPath` 指向 `scripts/hooks/`）。Bypass：`git commit --no-verify`。Uninstall：`git config --unset core.hooksPath`。
