# DD v19 完整版版面規格（2026-09-11 持有人定案）

樣稿：`_v19_layout/TSM_mockup.dc.html`（含免費資料區）、`_v19_layout/FIX_mockup.dc.html`；線上預覽 https://claude.ai/code/artifact/b38f5f86-d85d-44e7-8ec6-ac55aefec8f7 。樣稿是 Design Component 格式（外層 `<x-dc>`），實作時只取 `<helmet><style>` 與 `<div>` 內容，接進 `render_dd.py` 的站台 chrome（nav／footer／dd-meta／列印鈕）。

## 風格

外資報告：深入淺出、條列式、白話。每段＝標題＋一句粗體結論＋2–4 條條列理由（每條一句、帶數字）＋表格（可折疊）。不用比喻、不堆數字、不用 emoji；燈號用 CSS 色點（綠 #16A34A／黃 #D97706／紅 #DC2626／灰 #94A3B8）並附完整白話句；機器代號降為 `.mach` 小字放段尾。詞彙依 `notes/site-internal/root/_plainlang_styleguide.md`（同店→本業成長（不含併購）等）。

## 條列規則（2026-09-11 持有人補）

能條列就條列，文字不得擠成一段。頁首摘要段改 2–3 條條列；每段 lead 只准一句、不超過 40 字；每條條列只放一句，不用「；」串兩件事，要講兩件就拆兩條；條列可多到 5–6 條，寧可多條短的不要少條長的；矛盾裁定、賠錢路徑、行動條件同樣拆。

## 版面

- 寬 1200，左側固定目錄 208px（`nav.toc`），右側正文 `main.page` max 900px；手機單欄、目錄收合（H2 補 media query）。
- 字型 Noto Sans TC（站台既有），正文 15.5px／行高 1.75，h2 21px，lead 16.5px 粗體，表格 14px。色：ink #1E3A5F、mut #64748B、bg #F8FAFC、card #FFF、accent #3B82F6（站台既有 tokens）。
- 列印：目錄隱藏、折疊區展開、A4。

## 區塊與 canonical id（順序固定）

| 區塊 | id | 內容 |
|---|---|---|
| 頁首 | `dashboard` | 一行 meta（ticker・公司・產業／日期・收盤價）；h1 一句主張；一段 2–3 句摘要（oneliner）；**五張卡**：裁決（深藍：裁決／角色／一句執行語）、五年機率加權報酬（＋三情境機率）、基本情境年化（＋一句判讀）、最大回撤範圍（＋路徑風險色點）、本益比（＋分位色點）；**篩選器資料列**（24 格，見下）；**什麼會讓我改變主意**三條 |
| §1 結論 | `s1` | lead＋3–4 條＋`.mach`（訊號／估值燈／護城河／陷阱／矩陣列） |
| §2 我押的事 | `s2` | lead＋H1–H3 表（假設／要看到／什麼時候算錯）＋最怕的一件事＋持有期 |
| §3 產業 | `s3` | lead＋3–4 條；折疊：市場空間與利潤池表 |
| §4 商模與唯一致命數字 | `s4` | lead（致命數字）＋3–4 條 |
| §5 護城河 | `s5` | lead＋3–4 條；折疊：對手對照、節點良率、市佔方向、持續期四檢查點 |
| §6 成長 | `s6` | lead＋3 條；折疊：分部前瞻或 EPS 路徑表 |
| §7 財務 | `s7` | lead＋3–4 條；折疊：三到四年財務表、ROE 拆解 |
| §8 最新一季 | `s8` | lead＋3–4 條；折疊：法說原話 |
| §9 治理與資本配置 | `s9` | lead＋3–4 條；折疊：資本配置四年表 |
| §10 估值與三種未來 | `s10` | lead＋3 條＋**情境表常駐**（情境／機率／五年目標價／相對現價／故事）＋`.mach`；折疊：終端 EPS 與倍數依據、同業對照 |
| §11 矛盾裁定 | `s11` | lead＋每條「問句粗體＋裁定」 |
| §12 最可能怎麼賠 | `s12` | lead＋三視角各一條（粗體視角名）＋反向一條＋`.mach`（Max DD 推導） |
| §13 怎麼行動 | `decision` | lead＋新資金／已持有／清倉／放寬四條；折疊：觸發器全表、致命指標、催化劑、加減出場；折疊：決策矩陣逐列檢核與審查紀錄 |
| §14 複審 | `s14` | lead＋日期條列 |
| 附錄 A 擇時 | `appA` | 折疊：位置／階段／均線，一句「只是燈號不進裁決」 |
| 附錄 B 證據清單 | `appB` | 折疊：方向色點／發現／來源／日期 |
| 附錄 C 跟上一份比 | `appC` | 折疊：欄位／上一份／本份／原因 |
| 版本紀錄 | `revlog` | 表＋資料來源一句 |

## 篩選器資料列（24 格，全部由 dd-meta 渲染）

基本面評級（verdict）、訊號（signal＋白話）、估值燈（val）、均線（ma）、陷阱（trap）、五年後跑道（runway_post_y5）／護城河（moat＋moat_trend＋execution・pricing）、品質分（quality_score）、成長持久（growth_durability）、資本配置（capalloc_grade）、原型（archetype）、產業時鐘（industry_clock_phase＋cycle_position）／本益比 FY2（fpe_fy2）、PEG（peg）、五年分位（pct_5y＋口徑註）、一年合理價（upside_short_pct 推算）、兩年合理價（upside_mid_pct 推算）、五年基本情境（upside_5y_pct 推算）／牛市五年價（bull_5y_price＋p_bull）、熊市五年價（bear_5y_price＋p_bear）、不對稱比（asym_ratio）、內生成長上限（endo_growth_ceiling）、AI 風險（ai_risk，缺則「—」）、重啟或加碼門檻（rearm_trigger）。推算值一律標「由 X% 推算」。

## 免費資料區（程式從已收資料渲染，不花模型）

三到四年財務表、ROE 拆解、資本配置表、法說原話（digest 已摘）、情境樹逐項、同業對照、觸發器與致命指標全表、催化劑、證據清單（evidence findings 帶方向／來源／as-of）、跟上一份的差異（DRIFT_WATCH 20 欄＋cause）。

## 硬接點（不得動）

`<script id="dd-meta">` 欄位集合不變；canonical id 不變；頁面數字只准來自 judgment／facts／scenario_meta／evidence，散文不得新增數字（`validate_prose.py`）；快速版退役後 `docs/dd/brief/` 不再產出。
