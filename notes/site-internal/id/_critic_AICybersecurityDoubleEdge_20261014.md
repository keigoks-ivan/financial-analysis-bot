# 冷讀審查：ID_AICybersecurityDoubleEdge_20261014（ID v4 mode，J1–J10）

審查日 2026-10-14。輸入：check_excerpt.md、check_report.md；整份 HTML 未讀，僅以 evidence.json 與 grep 補脈絡。機械閘（錨點、表格數、T1 占比等）未重做。

## 裁決

**THESIS_INTACT（結論站得住，但有 12 處需修的 🟡，無 🔴）。**

結論「需求更確定、單價更不確定、純資安估值先到頂、不追價」所依賴的承重數字，經查大多對得上：Gartner 3Q26 的 247.5B／372.8B／10.8%，CRWD 淨新增 ARR 3.33 億美元（+51%）與 Flex ARR 22.9 億美元（+101%），PANW FY27 指引（NGS ARR +22–23%、RPO 252–254 億美元），兩個三角對帳的算式也都算得回來。問題集中在口徑混用、一條事實性錯誤（CRWD 揭露 NRR）、一個過期數字（MSFT 資安營收），以及「估值在 5 年高位」被從少數幾檔外推到整個純資安籃。

計數：🔴 0／🟡 12／🟢 4（J1、J5、J6、J7 大致通過，附註於下）。

換格的考核（本版從 shortage×II 換成 balanced×II，三次判斷 II／III／II）：頁面沒有因新格基準率較好看而換格，附錄也明寫「不因 balanced×II 的基準率較好看而換格」，換格理由（產品層查不到交期或缺貨證據、新進供給增加）有證據包支撐。通過。

## 🟡 逐項

### 🟡1（J3／J2）CRWD 其實有揭露 NRR，頁面說「不揭露」
- 錯誤原文（debates 分歧 2「我們認為」）：「而且 CRWD 與 S 都不揭露 NRR（淨營收留存率）」；risks 開頭另寫「NRR、用量計價占比、AI 入侵頻率都查不到，未列入」。
- 正確值：CRWD FY2026 10-K 載明美元淨留存率（dollar-based net retention）115%（截至 2026-01-31），財報電話會議另給總留存率（gross retention）97%。出處：https://www.sec.gov/Archives/edgar/data/1535527/000153552726000010/crwd-20260131.htm ；https://www.fool.com/earnings/call-transcripts/2026/03/03/crowdstrike-crwd-q4-2026-earnings-transcript/ （as-of 2026-01-31／2026-03-03）。
- 證據包其實有：evidence.json D11 載 Q1 FY27 GRR 97%／NRR 115%（Hudson Labs 預覽稿，T3-B），寫稿時被捨棄；E11 註明 Q2 新聞稿只說「留存提高」未給數字。所以正確說法是「CRWD 年報揭露 NRR，但每季新聞稿不給」，不是「不揭露」。
- 影響：這條正是檢驗「錨下移會不會傷 ARR」最直接的指標，頁面卻說查不到並改用 NET DBNR 代打。建議把 CRWD NRR 115%／GRR 97% 補進分歧 2，並評估是否列入 kill 表。
- 欄位：judgment 的 debates[1].we_think、risks 導言（prose 層）。

### 🟡2（J1／J3）MSFT「資安營收 >200 億、占 6%」是過期分子配新分母
- 錯誤原文（stocks 推導行）：「MSFT 資安 >200 億／FY26 營收 3,318 億≈6%（期別不一致）」；id-meta `purity_pct: 6`。
- 查證：「>200 億美元」是 Microsoft 在較早年度公布的資安年營收（Cybersecurity Dive 報導 https://www.cybersecuritydive.com/news/microsoft-20b-security-revenue/641498/ ，距今約 3 年以上）；FY26 Q4 財報（2026-07-29，營收 3,318 億、+18%）未單獨揭露資安營收。證據包 B21 自己註記「疑為 FY2025 時期」。分子至少一年以上、分母是最新年度，6% 會系統性低估。頁面雖寫了「期別不一致」，但 purity_pct 仍以 6 入機器欄，下游直讀。
- 建議：purity_pct 標「≥6，分子過期」或改寫為「Microsoft 近年未更新資安營收揭露，占比下限約 6%」。我未能查到 FY26 新數字，列為未及查證。
- 欄位：related_tickers[MSFT].purity_pct。

### 🟡3（J3）由下而上三角對帳混用季成長與年規模，PANW 尤其失真
- 錯誤原文（mechanics 推導）：「PANW 11.48×34%＋CRWD 6.0×25%（ARR 代）＋FTNT 8.1×26%＋ZS 3.35×25%＋NET 2.87×36%…≈966/35.7≈27%；差距＝(27−13.6)/13.6≈99%」。
- 問題：PANW 的 34% 是 FY26 Q4 單季營收年增（含 CyberArk 併入，evidence E12：Q4 營收 3.41B，+34%），但乘的是全年營收 11.48B；PANW 全年營收年增只有 11,480／9,221−1≈24.5%（evidence 20）。FTNT 用 Q2 的 +26% 乘全年指引中點；ZS 用含 Red Canary 的 +25%（排除後 +20%）。若 PANW 改用全年 24.5%，加總由 966 降到約 857，由下而上約 24%，與 13.6% 的差距約 77%，不是 99%。
- 影響：不改「平台吃長尾份額＋併購墊高」的方向判斷，但「高約 1 倍」這句話的精確度是假的。建議改用同一口徑（全年或同一季）並寫明含不含併購。
- 欄位：judgment 的 mechanics.tam_reconcile／derive_note。

### 🟡4（J3）13.6% 是美元計價名目增速，與後面的 11.2% 不同口徑
- 錯誤原文（summary／thesis）：「資安支出年增 13.6%」「2027 年放緩到 11.2%」；Bull 情境「2026 年的 13.6% 延續到 2030，不減速」。
- 正確值：Gartner 3Q26 的 2026 年增 13.6% 是 current USD，固定匯率為 12.7%；2027 年的 11.2% 與 2030 年 9.6% 是固定匯率。出處：https://softwarestrategiesblog.com/2026/10/05/gartner-3q26-information-security-forecast-post-quantum-firewalls-2030/ （轉述 Gartner G00862059，2026-09-24；Gartner 原文本人未能取得）。
- 影響：同口徑的放緩幅度是 12.7%→11.2%（約 1.5pp），不是 13.6%→11.2%（2.4pp）；Bull 的 412 是把匯率墊高的增速外推 4 年，偏樂觀。正文只在 CAGR 處提了「差異來自匯率」，頭條數字與分歧 4 沒標。建議頭條補「（固定匯率 12.7%）」。
- 備註：Gartner 兩個月前的 2Q26 版（2026-06-25）為 2026 年 248.9B、+12.7%（固定匯率）、2030 年 372.6B，頁面把前一版寫成 1Q26（353.1B）而略過 2Q26，附註的「上修」幅度被誇大；3Q26 相對 2Q26 實際變動很小。
- 欄位：mechanics 三情境表假設欄、推導行。

### 🟡5（J6／J3）「純資安股估值在 5 年高位」由 1.5 檔外推到整個籃子
- 錯誤原文（summary 怎麼做、id-meta action）：「純資安股估值在 5 年高位，等回調」；valuation 傳導：「樂觀假設住在純資安倍數（PANW 分位 100、CRWD 92）」。
- 證據包（priced_block）：PANW 分位 100 是唯一乾淨的一檔；CRWD 的 Fwd P/E 137.4 被標「離群值，不當錨」，卻仍引用其分位 92；NET 同樣離群；S、ZS 查不到；FTNT 分位 69；CHKP 無。四檔核心 🔴 標的中兩檔（S、ZS）完全沒有估值數字。
- 影響：結論「不追價」大概率仍對（26 週 +135.8%～+148.2% 的動能與擁擠度是獨立證據），但「5 年高位」只有 PANW 一檔站得住，其餘是旁證。建議改寫為「PANW 在 5 年最高分位；CRWD、FTNT 26 週漲逾 135%；S、ZS 無估值數據」，並修正 CRWD 的處理（要嘛不引分位，要嘛說明分位的算法不受離群 P/E 影響）。
- 欄位：valuation 導言、id-meta action／oneliner。

### 🟡6（J9）第一頁用廠商遙測當主論據，附錄卻說「不這樣做」
- 錯誤原文（附錄「刻意不做的三件事」）：「不把廠商自有的攻擊遙測數字當成市場需求」；但 oneliner 與 thesis 以「88% 的漏洞利用在 PoC 公開後 48 小時內發動」撐住需求，這是 CrowdStrike 自家 Threat Hunting Report（evidence C16，僅讀到搜尋摘要，未讀全文）。同段還把這個 CRWD 的 48 小時，與 Verizon DBIR 的「中位修補 43 天」並列成「瓶頸在防守方的速度」，兩者母體不同（CRWD OverWatch 觀察樣本 vs DBIR 約 22,000 起確認外洩），不能直接相減。
- 建議：thesis 句子改成「CRWD 自家報告稱 88%…（廠商數字）；Verizon DBIR 另載中位修補 43 天」，並與附錄聲明對齊。
- 欄位：thesis 第一段、oneliner。

### 🟡7（J2）保護 AI 類別 2030 年規模，與姊妹篇相差約 2 倍，未對帳
- 本篇：Gartner 保護 AI 類別 2026 年約 30 億美元、2030 年約 160 億美元（evidence C14；出處同上 softwarestrategiesblog 3Q26 文）。
- 姊妹篇 ID_LLMVendorSecurityEconomics_20260423 的 id-meta：`tam_usd_2030: 30.0`、`demand_5y_multiple: 3.1`、`cagr_pct_5y: 25.0`。
- 頁面「與姊妹報告的差異」段只對帳了相位（balanced／I vs II），沒對帳 TAM。口徑可能不同（Gartner 狹義 vs 該篇廣義），但頁面應寫一句。同理，ID_CybersecurityPlatformConsolidation 等四篇姊妹仍是 tam 353、倍數 1.8，本篇改 373／1.7，頁面雖提到版本差，但沒說明姊妹篇是否需刷新。
- 其餘 J2 對帳（平台整併 balanced／II、Agentic split／II、Token shortage／II）與 INDEX 一致。

### 🟡8（J4）「市場最低估的風險」沒有量級
- 原文（debates 結尾）：「最被低估的是捆綁壓價：微軟免費的 SCU 打在 AI 分析師加購，而這正是純資安倍數裡最貴的那段成長。」
- 問題：全頁沒有任何一個數字說明「AI 分析師加購」占純資安廠 ARR 多少，也沒說明微軟免費額度（每千名用戶每月 400 SCU、上限 1 萬 SCU／月，evidence E10）相對實際 SOC 用量是多大。證據包 NF 列明 CRWD Charlotte AI、S Purple AI 都沒有單獨揭露。論斷「最貴的那段成長」是推論，應標為推論，並給一個可驗的代理（如 PANW XSIAM ARR 超過 7 億美元、+70%，evidence B5）。
- 分歧 3 的「市場最強版本」只是重述事實（PANW +63%、P/E 68.6），沒有賣方共識數字（如 FY27 共識 NGS ARR 增速），不算最強版本。

### 🟡9（J7）S 毛利率 kill 與「推論成本漏出」的因果有混淆
- 原文：kill 表「S GAAP 毛利率 72%（前年 75%）…連兩季 <70%」，姿態「AI 防禦變現論改判為成本漏出」；PM 行動 ④「代表推論成本已經漏進毛利」。
- 問題：同一批證據裡，NET GAAP 毛利率也由 74.9% 降到 71.8%（evidence B19），Check Point 的毛利率下滑被歸因於「記憶體晶片成本上升」（evidence B18）。同期多家同降，S 的降幅（−3pp）與 NET（−3.1pp）幾乎一樣，單憑 S 毛利率無法歸因到 AI 推論。門檻 70% 是整數線，非由資料推導，是否自證也沒說。
- 建議：姿態改為「毛利壓力」並在判讀欄註明可能的混淆因素（記憶體成本、雲端成本），或加一個可區分推論成本的輔助指標。其餘三條 kill 通過：CRWD 門檻 0% 刻意不取公司指引 34%（避免套套邏輯，優），第二條為市場撮合價且以週線程式輸入，第三條 13% 有 Gartner 軟體段年化推導。

### 🟡10（J8）判斷手冊命中三條，實答偏薄
- 條目 4（寫 mechanics 3.4 bear 情境）：三視野 bear 欄各只有一句話（「捆綁壓價疊加減速，倍數與預期雙殺」），沒有「誰先被砍、傳導幾季、每一環一個前例」的時序劇本。
- 條目 8（持續讓利永久性四判準）：debate 2 只說「已符合四判準中的兩項（綁進授權、捆綁者專用）」，另兩項（持續多久、是否已錨定客戶預期）沒答，也沒說「兩項」意味著 base case 取週期還是永久。手冊規則是「四中其三→按永久 reset 建 base case」，現在停在二，需要說清楚離門檻差哪一項、看什麼證據補上。
- 條目 15（反方吸收）、條目 6（樂觀假設定價位置）、條目 18（雙閘）、條目 17（防套套）、條目 2（至少一條撮合價）皆實答並有數字，通過。

### 🟡11（J9）NET 被當證據、卻被排除在個股表外
- 原文：stocks 導言「NET、CSCO、FFIV 的資安占比查不到，未列入」；但 NET 全部營收（2.87B，+36%）被計入「七家」由下而上對帳；debate 2 的勝負條件完全押在 NET DBNR（≥120%／回落到 114%）。
- 問題：Cloudflare 營收含 CDN、開發者平台與零信任，DBNR 是整家公司指標，不能代表「資安用量計價」；而 id-meta 的 7 檔（含 MSFT、CHKP，不含 NET）與對帳的 7 家（含 NET，不含 MSFT）不是同一批。建議對帳表改用 related_tickers 同一批，或在 debate 2 註明 NET DBNR 只是間接代理。
- 其他小處：NET DBNR 120%／114% 在 evidence D8 為 T1 原句；C11 註記同數字「來自媒體摘要」，來源有重複但不衝突。

### 🟡12（J10）白話抽查：多處縮寫未括號白話
抽 5 句主閱讀線：
1. 「NGS ARR +63%（含併購）」「RPO 指引 252–254 億美元」——NGS、RPO 在正文未白話（僅 cRPO 表內出現）。
2. 「NET DBNR 維持 ≥120%」——DBNR 沒有括號說明（同段 NRR 有）。
3. 「Flex ARR」「SSE」「PQC 換機」「SOC／SIEM」「XDR」——首次出現無白話。
4. 附錄「不因 balanced×II 的基準率較好看而換格」——「balanced×II」「基準率」是內部流程語彙，外洩到讀者文字。
5. 「Glasswing 夥伴」「Mythos／Fable 出口」——專有名詞缺一句說明。
命中即標 🟡，不到 🔴。

## 其他小處（不另列 tier）
- 3.4「capex 占營收 4–8%」：用證據包數字回算，FTNT 上半年 148.6／3,897.5≈3.8%，ZS 277.3／3,353≈8.3%，NET 約 8–9%，區間應為約 4–9%。
- risks kill 表「ZS +20%／S +22%（2026-09-03）」：S 的 as-of 是 2026-08-27，ZS 是 2026-09-03，合併標日不精確。
- 分歧 1「CRWD 當日 −8%，之後 26 週 +148.2%」：26 週窗是 2026-04 中至 10-12，不是 2 月之後；附錄的寫法（「到 10-12 為止的 26 週」）才準確，兩處不一致。
- 附錄時間軸 2026-06 出口管制只寫「6-26 部分豁免」，漏了 2026-06-30 商務部已取消管制、7-01 恢復存取（evidence E6，T3-A）；正文「曾讓模型全球停用」用過去式，尚可，時間軸建議補一行。
- 「3.4 供需判斷屬第二／第三階段交界」把供需裁決（balanced）與時鐘相位混在一句，`sd_verdict_detail` 為空；建議把「II／III 交界」只放在時鐘欄。
- check_id 的兩個 WARN（附錄歷史錨點 1/1、篇幅 71KB > 55KB）屬機械項，本審不計。

## 🟢 通過項
- **J1**：cornerstone 事實逐條對證據包與網路查證通過：CRWD 淨新增 ARR 3.33 億美元（+51%）、Flex ARR 22.9 億美元（+101%）、Ending ARR 58.4 億美元（+25%）、FY27 淨新增 ARR 指引上調 630bp 至中點 34%（https://www.nasdaq.com/press-release/crowdstrike-reports-second-quarter-fiscal-year-2027-financial-results-2026-08-26 ）；Gartner 3Q26 的 217.7B／247.5B／372.8B／CAGR 10.8%、保護 AI 3B→16B（見🟡4 連結）；PANW 第四季 NGS ARR 9.10B（+63%）與 FY27 指引（evidence 21、23，T1 一手）。未發現「獨家／唯一」類誇大。
- **J5**：燈號五格（balanced／II／mid／high／×1.7）與 thesis 文字、id-meta 一致；`clock_phase_boundary: II/III` 也如實反映三次判斷的 II／III／II 分歧，不是單值掩蓋。
- **J6**：shortage×II 不適用（本版 balanced×II）；仍檢查三問：Phase 判定有基本面證據（CRWD 加速、capex 看不到過度投資）、擁擠度（26 週 +135.8～148.2%）已被承認並寫成換相雙閘的價格面預警、`priced_in: high` 誠實。唯一保留：雙閘設計要求 CRWD 淨新增 ARR 轉負才算必要條件，這個條件在估值頂部通常是最後才亮的燈，頁面已誠實標示為「II 後段」，但讀者應知道 III 相的確認會很晚。
- **J7**：除🟡9，整表有市場撮合價一條、CRWD 門檻不與公司指引同源，通過。
- **算式複算**：Bull／Bear／Base 的 275／281／266／373／412／332、1.71 倍、Bear 服務段年化 7.6%、PANW RPO 指引隱含約 19%（25.3／21.2−1=19.3%）、PANW 倍數收斂 41.4 倍所需 EPS 年增約 11%（實算 10.6%）與約 22%（實算 21.7%）皆正確。

## 未能或未及查證（不臆測）
- Verizon DBIR 2026 的 31%／13%／43 天、CRWD Threat Hunting Report 的 88%／2.5 倍（本審只核對證據包，兩者在證據包均標僅讀到搜尋摘要）。
- Gartner 3Q26 原文（G00862059）：僅經 softwarestrategiesblog 轉述核實，原文需付費；頁面已標「二手轉述」，合規。
- PANW／CRWD／FTNT／CHKP／NET／S 的 Fwd P/E 與 5 年分位（來自內部 dd-screener，非公開來源）；PANW 併購 CyberArk 後 FY2 P/E 是否因攤銷與股數變動失真未查。
- Microsoft 近期的資安營收（見🟡2）、E5／E7 併入 Security Copilot 公告（MC1478465）、Google 完成 Wiz 收購（2026-03-11）、Gartner「AI 強化資安」204.5B：僅依證據包，未獨立重查。
- JPM「錯殺」評論與 Bloomberg 的 CRWD −8%：證據包註明各來源跌幅數字不一。
- 共使用網路查證 6 輪（上限 10）。

## 處置（2026-10-14，持有人授權：不改結論的錯直接修）

只改 `judgment.json`、`evidence.json`、`plan.json`／`priced_block.md`（估值輸入，見乙節），之後重跑 prose＋check，**check PASS**（check_id rc=0、validate rc=0，T1 占比 64.3%）。備份：`judgment.pre_critic.json`、`judgment.pre_priced.json`、`evidence.pre_critic.json`、`plan.pre_priced.json`、`priced_block.pre_priced.md`。sd_verdict、clock_phase、conviction、priced_in、`*_boundary`、base_rate.action 與 action 方向（不追價）都沒動。

查證 5 次（上限 6）：Gartner 3Q26 轉述頁、CRWD FY2026 10-K、MSFT 資安營收（搜尋 1 次＋Cybersecurity Dive 1 次）、CRWD NRR 搜尋 1 次。新增證據 X1–X3（note 都標「審稿補入」）：
- X1：Gartner 3Q26，2026 年美元計價年增 13.6%、固定匯率 12.7%，2027 年固定匯率 11.2%，2Q26 版的 2026 年總額 248.2B（T3-C，2026-09-24）。
- X2：CRWD 10-K，截至 2026-01-31 的美元淨留存率 115%（T1，直讀）。
- X3：Microsoft 最後一次揭露資安營收是 2023-01，過去 12 個月超過 200 億美元（T3-B，Cybersecurity Dive 2023-01-30）。

### 甲、審稿意見處置

**已修（10 項）**

| # | 欄位 | 改前 → 改後 | 依據 |
|---|---|---|---|
| 🟡1 | debates[1].priced_in；risks.lede；debates[1].cite＋X2 | 「CRWD 與 S 都不揭露 NRR」→「CRWD 只在年報揭露 NRR（2026-01 底 115%），季報新聞稿不給；S 的 NRR 查不到」。risks 導言改為 NRR 未列入每季 kill 表的原因 | X2（T1）；S 依 NF-D「查不到」，原文「不揭露」說得過頭 |
| 🟡2 | stocks.rows[5].derivation；stocks.nonobvious；valuation.derivations[3]；cite＋X3 | 「期別不一致」→「200 億為 2023-01 揭露，之後未更新，約 6% 屬下限」。`purity_pct` 仍為 6：validator 只收數字，且資安營收不低於 200 億時 6% 就是下限（200/3,318≈6.0%） | X3、B21 |
| 🟡3 | triangulation rows[1]、reconcile、gap_pct；tam.derivation | PANW 由第四季 34% 改為 FY26 全年 24.5%（11,480/9,221−1）；由下而上 27%→24%（≈857/35.7），差距 99%→76%（自算 (24−13.6)/13.6=76.5%，審稿寫的 77% 是四捨五入差），gap_pct 100→76；列名註明「PANW、ZS 全年，其餘最新一季」，並註明對帳七家與個股表不是同一批（併 🟡11） | B1、B11 |
| 🟡4 | now_state；thesis.points[0]；debates[3].our_view；current_points[0]；Bull 假設欄與 bull_case；tam.derivation；cite＋X1 | 13.6% 標為美元計價，固定匯率 12.7%；分歧 4 改成同口徑 12.7%→11.2%；Bull 只加口徑標籤，數字不動。版本附註改為防火牆 7.8% 是 2Q26 版，2Q26 的 2026 年總額 248.2 已與本版相近。審稿寫的 2Q26 版 248.9B 與 2030 年 372.6B，轉述頁分別是 248.2B 與查不到，未採用 | X1 |
| 🟡5 | oneliner；action；base_case；base_rate.differences[1]；valuation.passthrough | 「純資安股估值在 5 年高位」收窄到有數字的個股（併乙節估值重算）：現價估算下 PANW、FTNT 分位都是 100，CRWD 也是 100 但 P/E 為離群值只作旁證，S、ZS 無數據 | priced block（現價估算） |
| 🟡6 | oneliner；thesis.points[1] | 88% 標為「CRWD 自家遙測」，不再寫成撐住預算；與 DBIR 43 天並列時註明兩份樣本不同 | C16、A10 |
| 🟡8 | debates_extra.underpriced_risk | 「最貴的那段成長」標為我們的推論，附最接近的公開代理 PANW XSIAM ARR（超過 7 億美元、+70%，二手） | B5 |
| 🟡9 | kill_table[3].posture；pm_actions[3]；sister_reconcile[3]（＋B19） | 「改判為成本漏出／推論成本已漏進毛利」→「毛利壓力確認，先排除記憶體與雲端成本再歸因」；姊妹對帳句補「同期 NET 也降 3.1 個百分點」 | B18、B19 |
| 🟡12 | closing.not_doing[1] 與數處首見縮寫 | 「balanced×II 的基準率」→「不因歷史勝率較好看就改判供需格局」；Flex ARR、NGS ARR、SCU、PoC、RPO、DBNR、SOC、SIEM、SSE、XDR、PQC、Glasswing、Mythos／Fable 在首見處補白話 | — |
| 其他小處 | debates[0].market_view；kill_table[2].asof；appendix.turns[6]（＋E6） | 「之後 26 週」→「到 10-12 為止的 26 週」；ZS／S 的資料日改為「2026-09-03／08-27」；時間軸補「6-30 取消、7-01 恢復存取」 | E6、A8、B11 |

🟡11 也一併處理：debates[1].signal_pos 的 NET DBNR 註明是「全公司口徑，只是間接代理」，對帳批次與個股表不一致的問題已寫進 reconcile（見 🟡3 列）。

另把 🟡7 的保護 AI 規模差異寫進 sister_reconcile[1]：姊妹篇 2030 年 TAM 300 億美元，本篇引 Gartner 160 億，口徑可能不同，沒有逐項對帳（只揭露差異，不改任何數字）。

**跳過（判斷類，或查不到）**
- 🟡7 其餘部分：四篇姊妹仍用 353／1.8，要不要刷新屬於那幾篇的維護工作，本頁不是錯誤，本頁推導行已寫明版本差。
- 🟡10：bear 時序劇本與四判準的另兩項需要判斷層補內容，原文沒有說過頭，依規則不改。
- 🟡8 第二段：分歧 3 缺賣方共識數字，要補新資料，不是錯誤。
- 🟡9 的 70% 整數門檻：屬判斷，不改。
- capex 占營收 4–8%：FTNT 3.8%、ZS 8.3%，四捨五入後就是 4–8%；NET 證據包沒有上半年營收，算不出 8–9%，不改。
- 「3.4 供需判斷屬第二／第三階段交界」：屬 prose 層的交界字樣，由程式依票數產生。重跑後已只出現在時鐘欄，sd_verdict_detail 不動。

### 乙、估值輸入更正（協調者追加，同一授權）

舊版 `priced_inputs` 讀的是各股 DD 日的倍數快照，不是現價。修正後重產 `plan.priced` 與 `priced_block.md`，判斷 JSON 中所有倍數與分位改為現價估算的 FY2 Fwd P/E（dd-screener 2026-10-14），valuation 導言加註口徑。

| 個股 | 改前（DD 日快照） | 改後（現價估算） |
|---|---|---|
| PANW | 68.6 倍／100 | 95.9 倍／100 |
| CRWD | 137.4 倍／92 | 163.9 倍／100（離群值） |
| FTNT | 41.4 倍／69 | 50.7 倍／100 |
| MSFT | 20.4 倍／12.6 | 27.6 倍／71.7 |
| CSCO | 23.6 倍／90 | 22.3 倍／81 |
| NET | 208.4 倍／88 | 208.8 倍／88.3（離群值） |

重算（自行複核）：
- PANW 股價持平：95.9/50.7≈1.892，1.892^(1/5)−1≈13.6%，原 11% 改為約 14%。
- 年報酬 10%：1.1^5×1.892≈3.05，3.05^(1/5)−1≈25.0%，原 22% 改為約 25%，是市場 10.8% 的 2.3 倍。valuation.high 的「約 2 倍」改為「2 倍以上」。
- MSFT 雙殺示意：0.9×23/27.6≈0.75，仍為 −25%。

改寫內容：
- 「拿低分位 MSFT（12.6）對照、樂觀假設不在 MSFT」改為：純資安（PANW、FTNT、CRWD）分位都在 100。MSFT 分位升到 71.7，相對自身歷史已不便宜，但倍數 27.6 倍、26 週 +28.5% 都遠低於純資安，殺傷仍集中在純資安。
- 改動欄位：id_meta.action、thesis.points[5]、debates[2].market_view、valuation 的 lede、passthrough、sensitivity、implied_growth、high、derivations[0][1][3]、priced_rows、stocks.nonobvious。
- 新數字讓「純資安估值在高位」的證據變強（FTNT、CRWD 分位也到 100），所以 priced_in=high 與「不追價」都不受影響。

### 交持有人（不改結論，供選擇）
- 要不要把 CRWD NRR（年報 115%）放進 kill 表。它只有年度一手值，不能每季追蹤，本次沒有加。
- Bull 情境要不要改用固定匯率 12.7% 外推。現在的 412 是用含匯率的 13.6% 外推 4 年，偏樂觀，改了會動 TAM 三情境數字。
- MSFT 不再便宜以後，「替代威脅拿 MSFT 對照」只剩基本面意義（捆綁受益者），估值上已經不是避風港。要不要另找低估值對照組（例如 CSCO 分位 81，也不低），屬判斷層選擇。
