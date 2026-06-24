# DS Taxonomy — pointer

DS 與 ID 共用同一套分類體系（mega × sub_group 白名單）。

**Source of truth**：[`../id/taxonomy.md`](../id/taxonomy.md)

**程式碼層共用**：`scripts/validate_ds_meta.py` 直接 import `scripts/validate_id_meta.py` 的 `TAXONOMY` 常數，不複製白名單。新增子群組 → 改 `docs/id/taxonomy.md` + `scripts/validate_id_meta.py` 的 `TAXONOMY` dict → DS 自動同步。
