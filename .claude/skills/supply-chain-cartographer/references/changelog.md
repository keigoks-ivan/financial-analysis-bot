# 預期效益 · 已知限制 · 版本沿革

> 條件載入：修改本 skill 規則、或需要理解 skill 存在動機／已知 gap 時載入。寫報告時不需載入。內容自 v1.1 原文零語意變更搬移（新增版本沿革一節）。

## 預期效益（為什麼這個 skill 存在）

每個 topic 平均 60-120 分鐘研究 + 30 分鐘寫入 + 10 分鐘驗證 = ~2 小時內完成一份高品質供應鏈圖。

15 個 topic 全部上線後：
- 全站建立**第三種產業視角**（補 ID 表格 + DS 敘述的盲點）
- 每個 topic 平均揭露 5-10 個被市場忽略的 single-point（TW 小型股）
- 自動 cross-link 既有 DD universe，highlight 沒做過 DD 的 ticker 作為 PM 後續工作清單

## v1.0 已知限制 + 未來改進

1. **無 pre-commit validator**（像 dd / id / ds 有 validate_*.py）— 目前靠 commit 前手跑 audit script。v1.1 可加 `scripts/validate_supply_chain_meta.py`。
2. **dd_links.json 沒有 sync hook** — DD 新增/重命名後要記得手動跑 `build_supply_chain_dd_index.py`。可考慮把它整進 `update_dd_index.py` 一起跑。
3. **無 critic gate**（像 id-review）— 目前靠雙源規則 (Gate G3) 自我約束。v1.1 可加 spawn sub-agent 抽查單點主張。
4. **Topic 之間沒交叉**（HBM 的 TSMC 跟 CoWoS 的 TSMC 是同一個節點概念但獨立 JSON）— 可接受重複，每個 topic 從自己視角描述 TSMC 角色。

→ 這些都是「能做更好但目前不阻斷」的 nice-to-have，v1.0 不處理。

## 版本沿革

- v1.2 結構拆分：核心＋references/ 條件載入，內容零變動
- v1.1 機械層瓶頸兩層制：新 topic 必餵 sidecar（terminal_markets.json 終端封鎖值＋substitution_lags.json 替代難度四檔）；hub 稀缺分級為編輯層（curated T0-T2/OVER）＋機械層對帳（漏網提名）
- v1.0 首發：互動式節點圖 skill，⚑ Single-Point Framework、💎 Top Picks、三層 Tier、5 輪研究 + 4 步輸出
