> 本檔為 `multi-stock-comparator-v1` SKILL.md 的條件載入 reference（v1.10 結構拆分）。**載入時點：第三步 Read source DD、抽取對比維度前**（見核心路由表）。 內容自 SKILL.md v1.9 原文零語意變更搬移。

## 【數據抽取對照表】(v1.8 — v13/v14 DD 為主，legacy 為 fallback)

**主要來源 = v13/v14 單一 DD**（已含基本面 Part I + 決策層 Part II）。下表「v13/v14 DD 抽取自」是**預設**讀取位置；「legacy 抽取自」僅在某 ticker 是純舊架構（無 v13/v14 DD，只有舊 DCA Phase A / 舊 v12 DD §舊編號）時使用。**注意 v13 對 v12 DD 做了 −2 章節位移**（舊 §9 護城河→§7、舊 §13 估值→§11、舊 §8 成長→§6、舊 §2 擇時→附錄 A），下表第 2 欄已是 v13/v14 編號。

| 對比維度 | v13/v14 DD 抽取自（主要） | legacy 抽取自（舊 DCA / 舊 v12 DD，僅 fallback） |
|:---|:---|:---|
| 統一裁決（進場/觀望/迴避）+ 倉位角色 | **§14**（dd-meta `dca_verdict` / `dca_role`） | 舊 DCA §7 裁決 |
| 護城河評分 + 權威趨勢 ↑→↓ | **§7 護城河**（dd-meta `moat` / `moat_trend` / `moat_execution` / `moat_pricing_power`） | 舊 DCA Phase A1 / 舊 v12 §9 |
| 護城河二維(execution / pricing power) | **§7 二維拆解** | 舊 DCA Phase A1 / 舊 v12 §9 |
| 威脅三級分類(🟡/🔴/⛔) | **§7 QC-23 威脅分類** | 舊 DCA §6b / 舊 v12 §9 |
| Runway 跑道 + Y5 後跑道 | **§6.A Runway / §6.A'' Y5 後跑道**（dd-meta `runway_post_y5`） | 舊 DCA Phase A2 / 舊 v12 §8.A |
| EPS CAGR 預估 | **§5 門檻檢核 + §11.2 PEG** | 舊 DCA EPS 表+§4 / 舊 v12 §7+§8.E |
| 5Y IRR(Bull/Base/Bear)+ 機率加權 EV | **§11.5 不對稱報酬**（dd-meta `ev5y_pct` / `irr_base_pct`） | 舊 DCA §4 Asymmetry / 舊 v12 §8.E+§13 |
| IRR 三分量拆解(EPS / re-rate / 股息回購) | **§11.6 IRR 三分量** | 舊 DCA §4 IRR composition |
| Pattern Match(歷史相似 case) | **§11.7 Pattern match** | 舊 DCA §4 Pattern Match |
| Max DD 評級 + 路徑風險 | **§13c 路徑壓力測試**（dd-meta `max_dd_pct`） | 舊 DCA §6c / 舊 v12 §13 |
| 估值 + PEG + 5Y 分位 | **§11.1 分位 / §11.2 PEG / 附錄 A 估值燈**（dd-meta `val` / `fpe_fy2` / `pct_5y` / `peg_fy2`） | 舊 DCA EPS 表+§4 / 舊 v12 §2.D+§13.2 |
| Pure MA 狀態 | **附錄 A Pure MA**（dd-meta `ma`） | 舊 DCA §7c / 舊 v12 §2.F |
| 5 年後護城河預判 | **§7 護城河趨勢 + §13b pre-mortem** | 舊 DCA §6b+Phase A1 / 舊 v12 §9.D |
| Single Thing(binary trigger) | **§3.F** | 舊 DCA §5 / 舊 v12 §5.F |
| 三大風險(過程性) | **§3.C 三大風險** | 舊 v12 §5.C |
| FCF Margin / ROIC | **§5 門檻檢核 / §8 財務品質** | 舊 DCA Phase A3 / 舊 v12 §10+§7 |
| 成長質量拆解(價 vs 量) | **§6.B 成長品質** | 舊 DCA Phase A3 / 舊 v12 §8.B |
| 客戶結構(top1/5/10、NRR、dual-track) | **§6.H 客戶結構深度** | 舊 DCA Phase A3 / 舊 v12 §8.H |
| 議價權三段(上游 / 下游 / 地緣) | **§9 議價權三段獨立** | 舊 DCA Phase A3 / 舊 v12 §11 |
| 利潤池位置 / 逐段 TAM/SAM | **§9 利潤池 / §9.F 逐段 TAM/SAM** | 舊 DCA Phase A2 / 舊 v12 §12 |
| 分部前瞻建模(量×價 build) | **§6.I 分部前瞻** | 舊 v12 §8.I |
| 對手 P&L 對照 | **§7.F 對手財務深度對照** | 舊 v12 §9.F |
| DuPont / CCC / 營運資金 | **§8.E** | 舊 v12 §10.E |
| 資本配置 / SBC / buyback | **§10 / §10.D 10Y track / §10.E FCF 去向** | 舊 DCA Phase A3 / 舊 v12 §10+§12 |
| Guidance 兌現紀錄(beat/miss) | **§4 即時財報 / §8** | 舊 DCA Phase A3/§6c / 舊 v12 §8+§12 |
| 基本面評級 signal / 陷阱定性 trap | **dd-meta `signal` / `trap` + §1 trap 四問** | 舊 v12 §1 |
| 循環交易讀數（循環/商品股） | **附錄 B**（僅循環 archetype 觸發；明標投機，與 §14 投資軌分開比較） | n/a |

**v13/v14 DD 是單一完整來源** — IRR composition（§11.6）、Pattern Match（§11.7）、Max DD（§13c）、統一裁決（§14）都在同一份檔內，**不再需要「混合 DCA + DD」**。優先讀 dd-meta JSON 取結構化數值（`dca_verdict`/`ev5y_pct`/`irr_base_pct`/`max_dd_pct`/`moat_trend`/`runway_post_y5`/`val`/`peg_fy2` 等），敘事細節再回對應 § 章節抽取。**只有當某 ticker 是 legacy（無 v13/v14 DD）時**，才用第 3 欄 legacy 位置；legacy 缺二維拆解 / 議價權三段時，從舊 §9 / Phase A1 內文推導並在表格 footnote 標「推導自內文，非報告原生欄位」。

