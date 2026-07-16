# 💎 Top Picks Framework + 三層 Tier

> 條件載入：寫 JSON 標註 `core_business` / `supply_chain_lock` / `node_role`（決定 💎 / 🐘 / 🔒 分層）時載入。核心 SKILL.md 保留 ⚑ Single-Point Framework（掛旗閘），本檔為坐在 ⚑ 節點上的公司如何分投資層級。內容自 v1.1 原文零語意變更搬移。

## 💎 Top Picks Framework — v1.3 收緊（3 條件 AND + 每 topic 上限 3-5）

> **v1.3 變更**：(1) `supply_chain_lock="tight"` 從「5 訊號任一」改「**≥2 訊號**」；(2) `core_business` 砍掉「管理層公開定位 flagship」敘事後門，只留可查的 ≥20% rev / pure-play；(3) **每 topic 💎 硬上限 3-5 檔**（validator 在 `single_point_framework:"v1.3"` 下強制 ≤5）；(4) **禁止把「第二供應源 / oligopoly 互打的一員 / 大集團一小 segment」標 💎** — 即使所在節點是 ⚑。hbm 三宗實例：Amkor（CoWoS 第二來源）、欣興/南電/景碩（互打 oligopoly）、Ajinomoto（食品集團）。根因都是「把**受惠於鎖喉的人**，誤當**鎖喉本身**」— 兩者投資 thesis 可能都成立，但 supply-chain map 的 💎 只標後者。

⚑ 是「strategic single-point」但**單獨用會把 TSMC / Corning / Broadcom 也標出來** — 那些是「太大太分散，部位推不動 EPS」的大象。投資視角需要更嚴格的篩子：

**isGolden(node, company) = node.single AND company.core_business AND company.supply_chain_lock == "tight"**

三條件同時滿足才是 💎 Top Pick，缺一不可。引擎 (`engine.js`) 自動算交集、在頁面底部 hero section 列表，drawer 公司表的 Top Pick row 加 💎 prefix + 淡金色背景。

**為何用 `supply_chain_lock` 取代之前的 `growth_trajectory`**：YoY 高成長是 momentum 信號（股價已漲完？），不是「供應鏈緊俏」信號。ASML 整體 +15% YoY 但 EUV backlog $30B+ 全球必經，TSMC corporate +25% YoY 但 N2/CoWoS sold out 到 2027 — 這些是「客戶離不開」的結構性 lock，比 YoY 強得多。換成 lock 後 false negatives 大幅下降。

### 判準（明確化、減少主觀）

**`core_business: true` 的條件（任一即過）**：
- 當前 ≥ **20% revenue** 來自此 segment（從財報 / 法說資料）
- **Pure-play** 純玩家（整家公司就做這個，如 Lumentum / Coherent / FOCI / Browave）
- ~~公司管理層公開定位 flagship / 未來主成長引擎~~ **（v1.3 移除：純敘事後門，管理層永遠這樣講；要 forward 例外走下方 Forward-Core 三 hard gate）**

**`core_business: false` 的條件（任一即否決）**：
- 大集團一小 segment（如 TSMC COUPE 占 <1%、Corning AI fiber 占 <20%、Broadcom CPO 占 <5%）
- 主業在別處（味之素 Ajinomoto 雖然 ABF 膜 95% 獨佔，但味之素是大食品/化工集團）

**Forward-Core 例外（用 `core_business_trajectory: "high"`）**：

預設規則：用「**今天**的 segment revenue %」判 `core_business`。但少數高確信案例可開 forward 例外 — 即使 segment 當前 <20% rev，仍可標 `core_business: true` + 加 `core_business_trajectory: "high"` 升 💎。

**三條件必須全過**（任一缺 → 不開 forward 例外）：

1. **管理層公開 guide 具體金額** — 必須是「2027 ASIC > $10 億美元」這種**具體數字** + 時間點，不是「策略佈局」「未來重點」這類空話。
2. **已 signed 多年合約 ≥3 年** — 必須是公開揭露的 binding contract、非 MOU / LOI。
3. **已有 named hyperscaler 級客戶** — Apple / NVIDIA / Google / AWS / Meta / MSFT / OpenAI / Anthropic / Tesla 任一具名 + 公開承諾。

**已批准的 forward-core 案例**：
- **MediaTek 2454 (asic ds-mtk-others)**：(i) 自報 ASIC 2026 >$10 億、2027 target $10B+；(ii) Google TPU v8i 合約鎖到 2031；(iii) Google + AWS 公開命名。當前 ASIC ~10% MTK 營收，三條件全過 → forward 例外升 💎。

**不通過的反例**（即使 narrative 漂亮）：
- **鴻海 2317 humanoid**：humanoid <1% Foxconn 營收、Foxconn 集團 $200B → 要做到 20% 需 humanoid 業務 $40B，數學上 5 年內不可能。
- **Hoya 7741 EUV mask blank**：沒具體金額 guide、沒 signed 合約、客戶經 ASML 中介非直接 named。
- **京鼎 3413 AMAT OEM**：80%+ 已經 AMAT 營收（current core 過），但結構是 supplier-captive（AMAT 可換 OEM）不是 customer-exclusive，是 ⚑ 框架誤用不是 forward 問題。

→ Forward-core **是「升級加分項」**、不是「萬用救生圈」。三條件 hard gate。寧可漏 alpha 也不要 false positive。

**`supply_chain_lock: "tight"` 的條件（v1.3：**≥2 訊號**過 — 舊版「任一即過」太鬆，2026 半導體隨便一家緊俏廠都有「訂單能見 ≥12 月」這條）**：
1. 📅 **訂單能見度 ≥ 12 個月** — ASML EUV backlog $30B+；京鼎 3413 訂單看到 9 個月；Apple 鎖 TSMC N2 三年
2. 🚫 **Sold out / capacity-constrained** — TSMC CoWoS 2026 月產能 120K 仍緊；SK Hynix HBM sold out through 2026
3. 🤝 **多年 exclusive 公開命名** — NVIDIA → Navitas 800V Kyber；Meta → Broadcom 1GW（2031 合約）；Anthropic → Google TPU 3.5GW；Tesla → Samsung AI6 ₩22 兆
4. 💰 **Pricing power demonstrated** — HBM3E → HBM4 ASP \$300 → \$500/stack；EUV pellicle 每片 \$300-500K
5. 🎯 **客戶公開多代 supplier** — AWS → Alchip Trainium 3+4；Apple → TSMC N2/N2P/A16；NVIDIA Rubin → 健策/AVC/Cooler Master/Delta（centralized procurement）

**`supply_chain_lock: "med"`**：有部分鎖喉但沒過 5 訊號（如雙占之一非絕對 lead、補位廠商）
**`supply_chain_lock: "loose"`**：替代源多、紅海、無多年 visibility

### 標註時機

寫 JSON 時，**只在你已有具體證據時才標 `core_business` / `supply_chain_lock`**。Missing 視為 false / unknown — 不會誤判為 💎。寧可漏標也不要錯標。Validator (`scripts/validate_supply_chain_meta.py`) 會驗 enum 值合法（`tight` / `med` / `loose`）。

### 為什麼這個交集有 alpha

- ⚑ 單獨 → 把大象（broad 集團）也標出來
- ⚑ + core_business → 排除「side bet」非核心業務
- + supply_chain_lock=tight → 排除「YoY 高但客戶可換」的雜訊 + 抓「YoY 普通但 backlog 鎖死」的真緊俏（如 ASML）
- 三個 AND → 留下 **真客戶離不開、EPS 推力結構性 high-conviction 的 5-15 檔**

worked example 的 💎 池：
- **HBM（v1.3 re-graded：⚑ 11→5、💎 12→4）**：ASML（EUV 唯一）/ SK Hynix + Micron（DRAM cartel 鎖定者，pricing power + sold-out）/ 欣興 Unimicron（AI-grade ABF #2，NVDA Blackwell 命名、結構性缺口）。砍掉的 8 檔多是 demoted-node 連帶（Lam/Disco/BESI/Onto/GUC）或第二源/oligopoly 互打（Amkor/南電/景碩）。
- **CoWoS（6 檔，**仍 v1.2 未 re-grade**）**：健策 3653 / 家登 3680 / 弘塑 3131 / 新應材 4749 / 萬潤 6187 / Amkor AMKR — 待 v1.3 雙軸 + critic 重評（含 Amkor 是否為第二源的同類檢查）。

這些正好是 sell-side / activist（Hunterbrook、Ming-Chi Kuo、Citrini）反覆推的標的 — 不是巧合，他們用類似框架。

## 三層 Tier — 鎖喉 ≠ 可買（v1.4 起，2026-05-29）

> **動機**：💎 單獨用會把「最不可或缺的節點 owner」誤判 — 因為最深的鎖喉（TSMC、Ajinomoto、ZEISS）往往**太大或不可投資**，反而過不了 💎 的 core_business gate。但「不是 💎」不代表「不重要」。v1.4 把坐在 ⚑ 節點上的公司分三層，讓「最不可或缺」與「最 top pick」**分開呈現**。

| Tier | 判準 | 怎麼評 | 範例 |
|---|---|---|---|
| 💎 **Satellite** | ⚑ 節點 × `core_business:true` × `supply_chain_lock:"tight"` — 鎖喉**推得動該股 EPS**（純玩家 / 純度高） | satellite alpha，部位推得動 | ASML、家登、台光電、ASPEED |
| 🐘 **Elephant** | `node_role:"elephant"` — **它就是鎖喉本身**（壟斷／近獨佔）但身處大型多角化集團，單節點 <~30% 營收推不動 EPS | **core-holding 框架**（估值/整體成長/週期），非 single-point | TSMC、Ajinomoto、Mitsui Chemicals |
| 🔒 **Uninvestable** | `node_role:"uninvestable"` — sole-source 但**買不到純曝險**：未上市，或已是某上市母體的次組件 | 透過母體 / 客戶玩 | ZEISS+Cymer+Trumpf（→ ASML）、Namics、Crusoe |

**標註規則**：
- `node_role` 是 optional enum（`elephant` / `uninvestable`），**只標在 ⚑ 節點**上的公司。
- 與 💎 satellite **互斥**：標了 `node_role` 就不能同時 `core_business:true`+`tight`（validator 強制；標 node_role 時應移除 cb/lock）。
- 💎 satellite **不另設欄位**，仍由 `isGolden()` = `core_business`×`supply_chain_lock` 推導。
- 判斷「elephant vs satellite」的關鍵問句：**「這個鎖喉節點占這家公司營收多少 %？」** ≥~30% 或純玩家 → satellite；個位數 %（大集團一小塊）→ elephant。
- 判斷「uninvestable」：沒有可買的獨立 equity（ticker `—`／私人／已併入母體）。
- engine 在頁尾 `#goldBlock` **分三區渲染**（💎 / 🐘 / 🔒），各自獨立表格與顏色。
