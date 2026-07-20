# ID Schema — §0-§9 內容模組必填 / 選填欄位 + 字數 target

每章列出：**必填元素**（lede / 強制表 / 強制模組 / 💡 / aside；critic + pre-publish gate 會檢查）、**選填強化**、**字數 target**（照 SKILL.md 骨架表）。

> **v3.0 呈現映射（2026-07-20）**：本檔 §0–§9 為**內容模組規格**——必填元素與字數義務一條不減，但呈現落點按 SKILL.md【章節骨架：sell-side 八段架構】映射表落入單一輸出檔的八段機器錨點：§0→`summary`（＋`thesis`）、§1→`appendix`、§2→`mechanics` 3.3、§3→`mechanics` 3.2、§4→`mechanics` 3.1、§5→`mechanics` 3.4、§6→`valuation`、§7→`debates`、§8→`risks`、§9→`stocks`。HTML 錨點一律用新 id（不再有 `id="s0"`~`id="s9"`）；逐節來源（`.ds-refs`）與長考證段收 `<details class="evidence-fold">` 折疊；視覺樣板見 `templates/report_template.md`。
> 全文可見字數 target：**16,000–22,000 字**（v2.1 上修，低於 14,000 視為偷懶）。本檔逐章字數＝SKILL.md【章節骨架】表的展開，兩處必須同步（歷史教訓：v2.1 上修時本檔漏更，兩套字數並存一年）。
> 順序硬性（v3.0）：呈現層八段 summary → thesis → debates → mechanics → valuation → risks → stocks → appendix 不可重排；§N 內容模組不可刪節，只能按上方映射換位。

---

## §0 決策摘要層 + id-meta（500-800 字）

| 欄位 | 必填 / 選填 | 內容規格 |
|:---|:---:|:---|
| `<meta name="id-skill-version">` | 必填 | content="{當前 skill 版本，見 SKILL.md frontmatter}" |
| `<meta name="id-theme">` / `id-publish-date` | 必填 | CamelCase theme / YYYY-MM-DD |
| `<script id="id-meta">` JSON | 必填 | 見下方 schema；`<title>` 後、第一個 `<style>` 前 |
| Claim Taxonomy reader banner | 必填 | `.claim-banner`，v2 必加 |
| Unit glossary | 必填 | `.unit-glossary`（QC-19）：ASP 單位 / Revenue 口徑 / 營收 scope |
| 6-box TL;DR 卡片 | 必填 | TAM / 5Y CAGR / 投資時鐘 Phase / **供需裁決（過剩/平衡/短缺三選一）** / conviction pill / top picks |
| 一句話 thesis box | 必填 | `.id-thesis` ≤200 字，**必帶 [I:] 或 [X:] tag**；同步寫入 id-meta `oneliner` |
| legacy cross-link callout | 條件必填 | 若同 theme 有 legacy ID/DS → `.id-crosslink`，標本份為 v2 敘事版 |
| **PM Implication 綠卡** | **必填（Gate 5 阻斷）** | `judgment-card`（樣式見 templates/report_template.md；Gate 5 認 class 不認色票）：五 bullet + ①②③④ 四行動 + conviction pill；§7/§8/§9 完成後才寫 |

**PM 綠卡五 bullet（缺任一 = 未完成）**：thesis 方向 / 個股 conviction tier 變化（點名 ticker）/ 關鍵新監測點（可量化）/ multiple·估值·週期定位風險（含當前 Phase + 下個 Phase 轉換條件）/ Entry 時機（現在 / 等 catalyst / 等回調三選一）。
**conviction pill**：high（§9 ≥2 🔴 + §8 falsification 距離 >2 sigma）/ mid（≥1 🔴 + ≥1 kill 未排除）/ low（thesis AT_RISK/BROKEN）。

### id-meta JSON 欄位（v2.0 時點基礎欄速查；**權威 schema ＝ `references/id-meta-schema.md`**，v2.4–v2.6 新增欄位與必填升級只在該檔維護。validator **不** reject unknown key——實測，僅 `sections_refreshed` 子鍵走白名單）

| key | 型別 | 必填 | 規格 |
|:---|:---|:---:|:---|
| `theme` | str | 必 | 產業主題 |
| `skill_version` | str | 必 | 填當前 skill 版本（見 SKILL.md frontmatter；validator regex 驗 vN.N） |
| `id_version` | str | 必 | 此 ID 自身版本（`"v1.0"` 初版） |
| `publish_date` | str | 必 | YYYY-MM-DD |
| `thesis_type` | enum | 必 | `structural` / `event-triggered` / `mixed`（禁複合如 `structural+event`） |
| `ai_exposure` | enum | 必 | 🟢 / 🟡 / 🔴 |
| `oneliner` | str | 必 | **≤ 200 chars**（寫完 `len()` 自測，>180 立刻精簡） |
| `related_tickers` | list | 必 | ≥1 筆，每筆 `{ticker, role, depth, beneficiary}` |
| `quality_tier` | enum | 選（流程建議填） | `Q0` / `Q1` / `Q2`（影響 Claim Taxonomy enforcement + Step 8.7 blocking 強度） |
| `mega` | enum | validator 選 / **流程必填** | 15 mega 白名單（`docs/id/taxonomy.md`） |
| `sub_group` | enum | validator 選 / **流程必填** | mega 對應 sub_group 白名單 |
| `tam_usd_2030` / `cagr_pct_5y` | number | 選 | 2030 TAM (B USD) / 5Y CAGR % |
| `growth_phase` | enum | 選 | `early` / `mid` / `late` / `declining`（禁自創長字串） |
| `value_chain_position` | enum | 選 | `upstream` / `midstream` / `downstream` / `cross-tier` |
| `industry_structure` | enum | 選 | `monopoly` / `duopoly` / `oligopoly` / `fragmented` |
| `sections_refreshed` | dict | 選 | keys `technical`（→§1-§2）/ `market`（→§3-§5）/ `judgment`（→§6-§9），values YYYY-MM-DD |
| `sister_ids` | list | 選 | 兄弟 ID 檔名列表 |

---

## §1 產業白話定義 + 歷史脈絡（1,800-2,800 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | `.id-lede` 2-3 句人話導讀（賣什麼 / 誰付錢 / 為何現在重要） |
| 白話開場 | 第一段不准出現未解釋行話；術語首現一行白話 |
| 邊界界定 | in-scope vs out-of-scope 收斂為敘事一段（不立表） |
| 歷史轉折 2-3 點 | 每個強制 **具體日期（YYYY/YYYY-MM）+ ≥1 量化錨點**（Gate 9 阻斷）；禁「過去幾年/最近/近期」 |
| 歷史類比 1-2 個 | 年份 + 主角 + 當年數據 + 多頭/空頭錯在哪 + 本次量化差異（QC-16；非「這次不一樣」） |
| **歷史 cycle 統計表**（模組 §1） | ≥2 輪 cycle 強制（QC-M5）；無 cycle → 刪表並註明「本產業尚無可統計的完整 cycle」 |
| 💡 對投資的意義 | `.id-implication`（DS 綠） |
| aside | `.ds-refs`（含量化斷言時必出） |

**cycle 統計表欄位**：`Cycle｜起訖｜長度(月)｜ASP peak-to-trough｜股價領先/落後基本面(月)`。來源：cycle 長度/振幅優先 T1/T2，股價領先落後可 T3-A primer（註資料窗口）。

---

## §2 技術成熟度 + S 曲線（1,200-1,800 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | 2-3 句：為什麼是現在，不是三年前也不是三年後 |
| 「為什麼是現在」敘事 | bottleneck 剛被解 / 成本曲線剛跨拐點的因果鏈 |
| **S-curve 圖**（QC-4 強制） | `.scurve-ascii`（IBM Plex Mono）為主；複雜情境改 inline SVG；優先官方 roadmap 數據 |
| kingmaker 小表 | 子技術 × 良率卡點 × 專利持有者，只放最關鍵 3-5 子技術 |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs`（S 曲線核心數字必 T1） |

**kingmaker 小表欄位**：`子技術｜良率卡點｜專利/領導者｜kingmaker?`。

---

## §3 供給側 + 利潤池（2,400-3,600 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | 2-3 句：誰在供給 / 瓶頸在哪 / 利潤被誰賺走 |
| **玩家矩陣表** | top players × **T-2 / 現在 / T+1 三時間欄**（DS 趨勢三欄）；新興供給 <3 年改 T-1/當年/T+1 + footnote；QC-17 禁 Q×4 |
| **利潤池遷移表**（模組 §3-1，強制） | 取代靜態毛利率表；% 必 source 或降定性（QC-18） |
| 成本曲線（模組 §3-2） | 週期/大宗強制；結構成長型可省須註明理由（QC-M4） |
| 未供敘事 | capex pipeline / 新進入者門檻 / 地緣政策 / 供給彈性 |
| **因果閉合**（DS-2） | §1 結構變數須在 §3 或 §4 ≥50 字回應是否仍 binding；**不准推到 §7** |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs` |

**玩家矩陣欄位**：`玩家｜share T-2｜現在｜T+1｜角色/護城河`。
**利潤池欄位**：`環節｜利潤池占比 T-2｜現在｜遷移方向｜搶/被搶`。

---

## §4 需求側 + 三角驗證（2,000-3,000 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | 2-3 句：誰在買 / 為何買 / 哪塊需求最不可替代 |
| 現需敘事 | end-market mix / 地域 / 客戶集中度 / pricing power |
| **TAM 三情境表含推導鏈** | base/bull/bear，每個數字「推導：A×B→C」可回溯（Gate 7）；bull/bear 偏離 base 必由「假設改了什麼」推出 |
| **需求三角驗證**（模組 §4，硬規則） | top-down vs bottom-up 對帳；**差 >20% 必解釋缺口 + 採信哪邊**（QC-M2） |
| 因果閉合 | §1 需求驅動在 §4 回應 5-10Y 走向 / 拐點 |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs`（bottom-up capex guidance 必 T1） |

**TAM 三情境欄位**：`情境｜TAM｜核心假設｜推導`。

---

## §5 供需裁決 + 推估 + 投資時鐘（2,400-3,600 字）

| 必填元素 | 規格 |
|:---|:---|
| 判斷層 banner | `.judgment-banner` |
| lede | 2-3 句先給結論方向（過剩/平衡/短缺） |
| **資本週期證據**（模組 §5-1） | capex/折舊比 / ROIC vs WACC / 新產能 lead time — **至少引 2 項**（QC-M1） |
| **強制裁決**（DS bridge） | `.id-bridge`「未來 X 年是 **過剩/平衡/短缺**，因為…」**三選一不騎牆**（Gate 10-1） |
| **三視野 × 三情境表** | 12M/3Y/5Y+ × base/bull/bear + **可量化 trigger + 推導**（Gate 7）；trigger 禁模糊詞 |
| 投資時鐘 phase 判定 | 當前 Phase I/II/III/IV + 各 phase 贏家切換 + 換 phase 必要∩充分條件 |
| **庫存/訂單指標**（模組 §5-2） | 產業適用時強制；軟體服務改 NRR/RPO 並說明替代理由（QC-M6） |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs` |

**三視野×三情境欄位**：`Horizon｜Base｜Bull｜Bear｜Trigger metric（推導）`。

---

## §6 產業經濟學 + 估值傳導（1,400-2,200 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | 2-3 句：錢怎麼賺 / 估值跟著什麼變數動 |
| unit economics / ASP 表 | ROIC / Gross / Capex cycle + ASP 過去 5Y + 未來 2Y + 抗 commoditization |
| 估值傳導敘事 | 產業變數 → Fwd PE/PEG pass-through + 敏感度錨點（+1pp 毛利 ⇒ ? 倍數） |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs` |

**unit economics 表欄位**：`指標｜過去 5Y｜未來 2Y｜抗 commoditization`。

---

## §7 Non-Consensus + Priced-in + Kill（1,800-2,800 字）

| 必填元素 | 規格 |
|:---|:---|
| 判斷層 banner | `.judgment-banner` |
| lede | 2-3 句：市場主流怎麼看 / 我們哪裡不同 / 為何還能賺錢 |
| **3 個分歧** | 共識 X（引 ≥1 T3）/ 我們 Y / 證據 Z（§1-§6）/ **市場 price 多少**；每條 [F:] cornerstone + [X:] 三情境（QC-10）；禁「本 ID 也認同 X」 |
| **Priced-in 檢驗**（模組 §7，每分歧強制） | sector 估值歷史分位 + 現價隱含成長假設 reverse 推算（Gate 7）；對但已 priced → 標「不可操作」（QC-M3） |
| **3 個 steel-man 反方** | 具體路徑 + 當前證據 + 證偽窗口；想不出 3 條 = 返工（QC-11） |
| 風險矩陣 | 降級為敘事素材；點名「市場最低估的風險」 |
| 💡 對投資的意義 | `.id-implication`（哪條最可操作：對 + 未 priced） |
| aside | `.ds-refs` |

---

## §8 Catalyst Timeline + 證偽表（1,000-1,600 字）

| 必填元素 | 規格 |
|:---|:---|
| 判斷層 banner | `.judgment-banner` |
| lede | 2-3 句：盯哪些節點 / 哪些數字一破就要砍 |
| **Catalyst Timeline**（bullet 並列） | 18M 內 5-8 節點，每個 明確日期 + 類別 + 指標 + **若達成/若落空雙路徑**（QC-12，Gate 10-3） |
| **證偽表** | 3-5 kill metric + base/bull/bear 閾值 + 時間窗；bear 閾值即作廢點，真 falsification 非 strawman，數字用 range（QC-13） |
| 💡 對投資的意義 | `.id-implication`（最該盯的 1-2 leading indicator） |
| aside | `.ds-refs` |

**證偽表欄位**：`Metric｜Base｜Bull｜Bear（thesis 作廢）｜時間窗`。

---

## §9 關聯個股（800-1,400 字）

| 必填元素 | 規格 |
|:---|:---|
| lede | 2-3 句：誰是純度玩家 / 誰是沒注意到的二次受益者 |
| **🔴🟡🟢 表**（≤16 行） | ticker × 角色 × 深度 × 受益/受害 × DD 連結 + **caption 時間限定**（current actual vs forward-looking；forward-looking 每行列 current actual 對照欄，Gate 10-2 / DS-18） |
| **1-2 非顯而易見受益者**（強制） | e.g. 本產業需某設備 → 該設備供應商 |
| 深度說明 | 🔴 >40% 依賴 OR 技術領導 ｜ 🟡 10-40% ｜ 🟢 <10% 被連動 |
| 同步 id-meta | `related_tickers[]`（下游 hook）；對每檔查 `docs/dd/INDEX.md`，已有 DD 附連結，否則標「DD 未建」 |
| 💡 對投資的意義 | `.id-implication` |
| aside | `.ds-refs` |

**ticker 表欄位**：`Ticker｜深度｜受益/受害｜營收曝險(current actual)｜角色｜DD 連結`。

---

## 全文配額（Gate 對應）

| 配額項 | 上限 / 下限 | Gate |
|:---|:---|:---|
| 總可見字數 | 16,000–22,000 字 | — |
| 文字字元比例 | ≥ **55%** | Gate 6 / QC-2 |
| 表格數 | ≤ **10** 張 | Gate 6 / QC-2 |
| 每張表行數 | ≤ **8** 行（不含表頭）；**§9 例外 ≤ 16** | Gate 6 / QC-2 |
| 🟡 判斷 bullet 比例 | ≤ 20% | QC-1 |
| T1 + T1-zh aside 占比 | ≥ **60%** | Gate 8 / QC-6 |
| 💡 `.id-implication` | §1-§9 每章 1 個（共 9 個） | QC-8 |
| 每章開頭 lede | §1-§9 每章 1 個（2-3 句） | 可讀性規則層 |
| 每張表三句話 | 表前 1 句 + 表後 2 句（`.tbl-why` / `.tbl-read`） | 可讀性規則層 |
