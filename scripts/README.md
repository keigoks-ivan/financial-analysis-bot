# scripts/

## Git pre-commit hook（dd/id-meta validator）

Repo 內建 pre-commit hook 在 `scripts/hooks/pre-commit`，commit 前自動跑 `validate_dd_meta.py` + `validate_id_meta.py`，不過違反 schema 的檔案無法 push（鏡像 GitHub Actions strict gate 在本機提早攔截）。只在 staged files 觸及 `docs/dd/DD_*.html` / `docs/id/ID_*.html` / validator script 本身時才跑，其他 commit 無感。

**新機器 / 新 clone 啟用：**

```bash
bash scripts/install_hooks.sh
```

只跑這一次（會把 `core.hooksPath` 指向 `scripts/hooks/`）。Bypass：`git commit --no-verify`。Uninstall：`git config --unset core.hooksPath`。
