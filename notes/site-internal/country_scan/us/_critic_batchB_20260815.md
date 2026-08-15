# 美國國家掃描 batch B 冷讀報告（鏡頭五～九）

- **審閱者**：opus 冷讀 critic（writer＝sonnet，跨模型冷讀）
- **審閱日**：2026-08-15（DD 窗期錨點同此日）
- **審閱對象**：`docs/backtest/country_scan/us/{healthcare,financials,consumer,energy-industrials,hidden-champions}.html`
- **對照材料**：`_PLAN.md`（七鐵律＋§4 鏡頭定義）、`_universe.json`（1,590 檔快照）、`_dd_inventory.md`、`_structure_dossier.md`、`docs/dd/DD_*.html` dd-meta 原檔
- **工具限制**：WebSearch 配額零，頁外查證一律 WebFetch；打不到的標「無法覆核」不判錯
- **本報告不改任何 HTML**

## 總計

| 頁面 | 🔴 必修 | 🟡 建議 | 數字抽查 | dd-meta 逐字比對 |
|---|---|---|---|---|
| healthcare | 1 | 3 | ~40 點全對 | 16/16 全對 |
| financials | 4 | 5 | ~35 點全對 | 13/13 全對 |
| consumer | 4 | 3 | ~45 點，1 格損毀 | 12/12 連結有效 |
| energy-industrials | 3 | 6 | ~30 點全對 | 35 檔對帳算術全對 |
| hidden-champions | 5 | 3 | ~30 點，1 欄定義錯 | 9/9 全對，1 檔漏認 |
| **合計** | **17** | **20** | 62 條 DD 連結全數有效且為最新版 | |

跨頁機械檢查（五頁一致通過 🟢）：跨市場字串（台灣／台股／TWSE／日本／Japan／東證／TOPIX／馬來／Malaysia／Bursa／KLCI）在 nav 以外零命中；描述器紀律無買賣祈使句；Exhibit 各頁獨立連號無跳號；五頁之間無同一 ticker 雙頁深查（Exhibit 主表交集為空）；V／MA 歸鏡頭四在 financials §7 與 consumer §8 兩頁口徑一致；VRT 歸鏡頭二在 energy §8 明文切出且與 semis 頁不衝突。

---

## 一、healthcare（醫療保健）

77,878 bytes｜621 行｜§1–§8，`id="verdict"` 在 §8｜16 ddcards｜6 datanotes｜Exhibit 1–6

### 🔴 必修

**H-R1（L432、L447）Medicare Advantage 資金壓力軸整軸未查。**
§4 標題寫「MLR 壓力與 PBM 監管的雙向拉扯」，但全頁 Medicare Advantage 只以「DOJ upcoding 訴訟風險」出現兩次（L432 UNH 段、L447 保險段），完全沒有觸及資金端：CMS 年度費率通知（rate notice）、v28 風險調整模型分階段導入、術後利用率（utilization）回升、星級評等（star ratings）獎金。這四項才是 2024–2026 MA 業者 MLR 惡化的直接驅動，也是 UNH／ELV／CI 股價位置（UNH 52 週位置低檔）的主因。頁面把 MA 只當法律風險寫，等於整個資金軸沒查——依 critic 職責書 (a)，缺軸本身即 🔴，不需先證明結論錯。

### 🟡 建議

**H-Y1（L555）MCK ddcard 裁決被截斷。** 卡片渲染「A｜核心候選」，`DD_MCK_20260525.html` dd-meta 的 `verdict` 全文是「A 核心候選 / 觀望偏進場（pullback 中）」。截掉的正是時點限定語，違反 `_PLAN.md` 鐵律 7「逐字抄 dd-meta」。建議補全或改抄 `dca_verdict` 欄位並標明欄位來源。

**H-Y2（L347）錯字。** 「Ozempic／Rybelsub／Wegovy」應為 **Rybelsus**。同頁 L295 拼寫正確，屬單點手誤。

**H-Y3（kdstrip）178 檔母體定義未揭露。** 「醫療保健板塊 178 檔／US$7.121 兆」我以 `_universe.json` 重算為 GICS Health Care(163)＋Healthcare(12) ∪ yahoo Healthcare(177) 的聯集＝178 檔、$7.121 兆，數字完全正確，但頁面未說明是雙分類聯集。同批 financials 頁把同型聯集標成「GICS Financials」已出錯（見 F-R4），兩頁建議統一寫「GICS ∪ Yahoo 分類聯集」。

### 🟢 驗證通過

- **Exhibit 2/3/4 全數逐格覆核 `_universe.json`，零誤差**：LLY US$1.05 兆／24.9x／+47.7%／0.57%；ABBV US$4,408 億／15.3x／+10.2%／2.76%；JNJ、MRK、PFE、ISRG、SYK、MDT、UNH US$3,606 億／17.9x／+0.4%、CVS、ELV、CI、MCK、COR、CAH 全對。
- **16 檔 DD 逐字比對全對**：連結全部存在且為該 ticker 最新版；verdict／role／grade 抄錄無誤；窗期天數以 2026-08-15 重算全對（LLY 9、JNJ 30、ISRG 29、BSX 36、GILD／ABBV／MRK／TMDX／UNH／COR／CAH／EHC 82、MDT／CVS／OSCR 89），「16 檔全數窗內」成立。
- **PBM 頁外數字 WebFetch 覆核通過**：三大 PBM 合計約 80% 處方箋量、覆蓋約 2.7 億人、2024 年管理藥費約 US$6,000 億——與所引來源一致。
- **§7 切線處理為五頁最佳**：ISRG 歸鏡頭四並說明理由、JNJ 醫材與藥品雙屬性的歸屬邏輯明寫、且明列「刻意不設子鏡頭」的範圍，切線紀律完整。
- toc 五頁中唯一正確連 `#verdict`。標點全形、無簡體字、描述器紀律清潔。

---

## 二、financials（金融）

75,127 bytes｜662 行｜§1–§8，`<h2 id="verdict">` 在 L621｜13 ddcards｜Exhibit 1–5

### 🔴 必修

**F-R1 地區銀行整軸未查。** 全頁「地區銀行」零命中。本鏡頭核心問句是「四型的資本結構與利率敏感度；誰的 ROE 靠槓桿誰靠費用」——存款貝他（deposit beta）、NIM 對降息路徑的敏感度、存款外流，這些機制在 SP400／SP600 的地區銀行身上才是決定性的，大型行反而被交易與費用收入稀釋掉。母體有數十檔地區銀行，一檔未進表。

**F-R2 商用不動產（CRE）曝險整軸未查。** 「商用不動產」「CRE」零命中。這是目前坐在美國銀行資產負債表上最大的單一信用風險，且集中度恰好與 F-R1 的地區銀行重疊。頁面談 ROE 分解卻不談資產端最大的潛在減損來源。

**F-R3 私人信貸循環未成軸。** §3 把 BX／KKR／APO 純以「費用型 vs 保險型」的損益結構處理，APO 的 Athene 佔營收 85% 只被用來解釋利潤率視覺失真。private credit／direct lending 的循環位置（利差壓縮、PIK 比重、退出通道）完全沒展開。L403 datanote 承認「ARES 的私募信貸平台規模與 direct lending 市占率…列為缺口」——承認了單一數字查不到，但整條軸線並未因此被視為未覆蓋而在正文標示。

**F-R4（kdstrip L258）母體標籤與數字不符。** 頁面寫「母體金融股（GICS Financials）278 檔」。我以 `_universe.json` 重算：**GICS Financials ＝ 259 檔**，yahoo Financial Services ＝ 254 檔，兩者聯集 ＝ **278 檔**。278 是聯集數，不是 GICS 數。標籤與數字二選一必須改（建議改標籤為聯集，與 healthcare 178 檔的口徑一致）。

### 🟡 建議

**F-Y1 支付新規軸缺席。** interchange／Durbin／CFPB／穩定幣相關規範零命中。V／MA 正確切給鏡頭四，但 COF（發卡＋收單）與 PYPL／SEZL 都在本頁，交換費與 BNPL 監管直接打在它們的單位經濟上。

**F-Y2 資本適足軸僅有標籤無內容。** 「資本適足」出現 2 次皆為過場語，Basel III endgame／CET1／年度壓力測試（CCAR/DFAST）零展開。鏡頭問句字面就是「資本結構」，這是最貼題的監管軸。

**F-Y3（L495）datanote 出現讀者可見的編輯自語。** 原文：「BRK 現金儲備 US$365.5 億（原文誤植單位，應為 US$3,655 億）」。這是寫作過程的自我更正被留在成品裡（鷹架語言），應直接寫正確數字 US$3,655 億。

**F-Y4（toc §8）錨點不一致。** toc 的 §8 連 `#s8`，而 `id="verdict"` 掛在 §8 的 `<h2>`。功能上可達，但與 healthcare 的 `#verdict` 寫法不一致，建議統一。

**F-Y5（L460）FICO 營收成長雙數字未對帳。** 執行摘要第 4 點用 +24.1%（來源 stockanalysis.com，as-of 2026-06-30，datanote 已揭露），`_universe.json` 快照為 25.7%。兩者都誠實標了來源，但同頁兩個數字未在正文互相對帳，讀者會困惑。

### 🟢 驗證通過

- **Exhibit 1／2 全數逐格覆核，零誤差**：JPM ROE 17.79%／P/B 2.73x／P/E 14.5x／殖利率 1.65%／利潤率 30.4%；BAC、WFC、C 全對；四大行市值加總 964.5＋451.0＋268.6＋233.7 ＝ **US$1,917.8 億十億 ≈ US$1.92 兆** ✓；GS D/E 725、MS 517；MCO ROE 76.9%；AXP US$2,313 億／34.4%；SCHW、ARES、APO、KKR、IBKR、HOOD、PYPL、SEZL、SOFI 全對。
- **BRK-B P/B 0.001x 的資料失真被正確識別並標註**，未當成真實估值使用。
- **13 檔 DD 逐字比對全對**：連結有效且最新；窗期重算全對（SOFI 16、BX 22、IBKR 24、COF 24、MS 30、BLK 30、HOOD 32、FICO 36、PYPL 36、SEZL 36、GS 61、COIN 82、GLXY 82）。
- **DD 缺口宣稱逐檔 `ls` 覆核為真**：JPM／BAC／WFC／C／PGR／CB／BRK／KKR／APO／ARES／SCHW／AXP／CME／ICE／SPGI／MCO／MSCI 站內確實零 DD。
- §7 V／MA 歸鏡頭四，與 consumer 頁一致。標點全形、無簡體字、描述器紀律清潔。

---

## 三、consumer（消費特許經營）

80,613 bytes｜698 行｜§1–§9，`id="verdict"` 在 L677 的 `.basket`｜12 ddcards｜Exhibit 1–7

### 🔴 必修

**C-R1 關稅對進口成本的影響實質未查。** 全頁只有 L509 一處順帶提及，且是夾在 GLP-1 干擾因子清單裡的一句。本鏡頭問句是「定價權還剩多少」，而 2026 年美國消費品最大的單一成本衝擊就是關稅打在越南／中國製造的鞋服（NKE／LULU／DECK／TPR／RL）與低價零售（DG／DLTR）的進貨成本上——這正是「漲價轉嫁能力」的即時實測場。無專節、無 Exhibit、亦無缺口自陳。

**C-R2 自有品牌滲透率整軸未查。** 「自有品牌」「private label」零命中。這是衡量品牌定價權侵蝕最直接的量化指標，且頁面已經在寫 COST（Kirkland）／WMT（Great Value）／TJX 的故事，缺這一軸等於把該故事的度量衡拿掉。同樣無缺口自陳。

**C-R3（L419）Exhibit 3 的 CL 列資料格損毀。**
原文：`｜CL｜Colgate-Palmolive｜73.3｜36.2x｜22.4x｜4.9%｜36.2x 註：ROE>100%（股東權益基數低）｜站內無 DD｜`
ROE 欄被貼進了 P/E(TTM) 的值「36.2x」。註解本身（股東權益基數低導致 ROE 破百）是對的，但欄位值必須換成實際 ROE 或明確標「NM」。

**C-R4（L423、L431、L654）DECK 缺口宣稱不實。**
Exhibit 3 的 DECK 整列為「—」，L431 與 L654 兩處 datanote 皆稱「DECK 站內未見於 `_universe.json` 消費相關子產業篩選結果…市值與估值數字暫缺，列為缺口」。**DECK 確實在 `_universe.json` 裡**：市值 US$126.8 億、GICS Consumer Discretionary／Footwear、forward P/E 11.13、ROE 42.56%，欄位完整。是本頁的子產業篩選條件漏掉它，卻把漏失歸咎於資料源。這比單純缺數字嚴重——它是一則**假的誠實揭露**，會讓下游相信該欄位在母體裡不存在。

### 🟡 建議

**C-Y1（L668）切線把已裁定的事寫成未決。** §8 正確把 marketplace 名單歸鏡頭三，但接著寫「與本頁承接的切線指示不完全一致，此為分類 ambiguity…分歧留待鏡頭一／鏡頭三 writer 或 hub critic 裁定」。orchestrator 已裁定歸鏡頭三，主歸屬既已寫對，這段開放式懸置應收掉，改為單句說明歸屬理由即可。

**C-Y2（L511）簡體字。** 「部分卖方叙事認為…」應為「賣方敘事」。

**C-Y3 DECK ddcard 的 role 混用兩個欄位。** 卡片寫「衛星（逢回分批）」，dd-meta 的 `dca_role` 是「衛星持倉」，「逢回分批」來自 `verdict` 字串。可接受但建議欄位來源一致。

### 🟢 驗證通過

- **頭條宣稱獨立覆核為真**：`ls docs/dd/DD_{MCD,PG,PEP,YUM,ORLY,AZO}_*.html` 六檔全數 no matches，「站內零 DD」成立。Exhibit 7 六檔市值加總 193.1＋336.0＋192.3＋40.4＋73.7＋49.4 ＝ 884.9 ≈ **US$885B** ✓。
- **DD 對帳算術全對**：31 檔 ＝ 12 ddcards ＋ 19 列表格；逾窗 2 檔 ＝ LULU 91 天、DIS 91 天（皆正確判逾窗）；窗內 29 ✓；獵場覆蓋 10/16 ＝ 62.5% ✓。
- **Exhibit 3／4／5／6 約 45 個快照數字逐格覆核**，除 C-R3 的 CL 一格外全對。
- **頁外數字 WebFetch 覆核**：NAR 2026 年 7 月成屋銷售月減 1.7% 與來源一致（SAAR 410 萬戶未出現在可取得的節錄段落，該單一數字標「無法覆核」，頁面本身已正確標註來源）。
- §8 V／MA 歸鏡頭四，與 financials 一致。標點全形（僅 C-Y2 一處簡體）、描述器紀律清潔、Exhibit 連號。

---

## 四、energy-industrials（能源電力與再工業化）

91,742 bytes｜761 行｜§1–§9｜12 ddcards｜Exhibit 1–8

### 🔴 必修

**E-R1（全頁）`id="verdict"` 完全不存在。**
`grep -c 'id="verdict"'` ＝ **0**。全頁段落 id 只有 `s1`–`s9`，§9「本鏡頭的答案」掛在 `id="s9"`（L735），`.basket` 亦無 id，toc 九條連結全是 `#s1`–`#s9`。這違反 `_PLAN.md` §5 的固定骨架，且會打斷 hub 對答案節的深連結。**五頁中唯一一頁沒有此錨點。** 寫手自報屬實。

**E-R2 LNG 出口整軸未查。** 「LNG」「液化天然氣」「天然氣」全頁零命中。§4 油氣只寫資本紀律、頁岩成熟度、Permian。美國 LNG 出口建設（LNG／VG／SRE／NextDecade）是本土天然氣需求最大的結構性增量，且與本頁自己主張的「用電成長 × 再工業化」是同一條需求鏈——缺這一軸讓 §4 的能源需求圖像不完整。

**E-R3（L623）HUBB ddcard 裁決被截斷至反向。**
卡片渲染「A（legacy）配電與公用事業組件，基本面評級 A」。`DD_HUBB` dd-meta 的 `verdict` 全文是「A（核心候選進場，Fwd PE 22x 5Y 分位 0% ＋ post-earnings −13% drop 創 5 年難得 entry，是 PWR 同 thesis 便宜替代品）」。被截掉的「核心候選進場」正是站內對本鏡頭最強的一則裁決，讀者從卡片上完全看不到。違反鐵律 7。

### 🟡 建議

**E-Y1（L384）電網設備／變壓器交期軸僅以缺口收場。** datanote 誠實記載「多個官方來源皆無法讀取，列為缺口不捏造」——**此處給予正面評價，不捏造是對的**。但這是一個名字裡就有「電網設備」的鏡頭，而交期是該產業最硬的供給側約束。建議換源再試一輪（DOE 變壓器供應鏈報告、Hitachi Energy／Siemens Energy 法說與 IR、NEMA 產業統計）再決定是否落為永久缺口。

**E-Y2（L~120 §1.1）PJM 拍賣成本的「一年 8 倍」框架沿用來源的時序模糊。**
頁面寫「2024 年…約 22 億美元…最新一次…超過 160 億美元，漲幅接近 8 倍」。我 WebFetch 覆核來源（PJM 條目），原文確為「2024 auction: \$2.2 billion；2025 auction: over \$16 billion, eight times the previous year's cost」——**頁面忠實轉述，不是自造**。但實際序列橫跨兩個拍賣週期（\$2.2B → \$14.7B → 約 \$16.1B），「一年」的說法繼承了來源的壓縮。datanote 已聲明 \$/MW-day 與交付年度未覆核。建議加一句限定語（如「跨兩次拍賣週期」）而非改數字。

**E-Y3（§1、§4.3）TLN／FSLR／LEU／MP 正文未回指站內既有 DD。**
四檔在 §7 Exhibit 7 都已**正確列入對帳**（日期、天數、裁決 B 全對，此點 🟢），但正文 §1 Exhibit 1 與 §4.3 只用 `_universe.json` 數字論述，且 §4.3 寫 LEU／MP「站內既有知識背景…未逐一覆核」——而這四檔的 DD 都在窗內（TLN 64 天、FSLR 68 天、LEU 82 天、MP 82 天）。屬正文缺內部交叉引用，非對帳遺漏。

**E-Y4 LEU 表列裁決被截斷。** 表格只顯示「B」，dd-meta 全文為「B 觀望；等估值/MA 修復至 \$120–150 ＋ DOE final agreement ＋ Russia 2027 末 waiver 確認後再分批」。與 E-R3 同型但影響較小（方向未反轉），列 🟡。

**E-Y5 評級前綴渲染不一致。** TT 卡片寫「基本面評級 A」，但 GEV／PWR／HON／CAT／URI／BE／RKLB 的 dd-meta `signal` 皆為 B，卡片上未顯示等級。同頁內兩種寫法；financials 頁則是每張卡都顯示。建議統一。

**E-Y6（L334）簡體字。** 「标记未覆核」應為「標記」。

### 🟢 驗證通過

- **DD 對帳算術完全正確**：35 檔 ＝ 12 ddcards ＋ 23 列 Exhibit 7；逾窗 4 檔 ＝ BWXT 102、ETN 101、STRL 102、FIX 91；窗內 31 ✓。全部天數以 2026-08-15 重算無誤。
- **Exhibit 1 的 52 週位置我以 `(price − low)/(high − low)` 獨立重算全部命中**：GEV 80.1%、VST 17.7%、CEG 29.3%、NRG 17.7%、TLN 40.9%、BE 60.9%、FSLR 32.8%，與頁面 ~80／~18／~29／~18／~41／~61／~33 一致。
- **§9 分層名單重算全對**：≥80% 群 ETN 84.1、PH 88.5、URI 94.7、MMM 95.1、JCI 93.7、RTX 94.9；<40% 群 NOC 36.2、MLM 13.0、BWXT 19.0。汽車鏈 F ROE −18.3%、GM fPE 5.90、LEA +3.0%、BWA +0.3%；STRL 營收 +90.1%；XOM／CVX／COP fPE 14.97／15.25／13.47（頁面「13–15 倍」CVX 微幅超出，可忽略）。
- **Palisades §1.2 全數 WebFetch 覆核通過**：805 MWe ✓、2022 年 5 月關閉 ✓、2022 年 6 月 Holtec 收購 ✓、DOE US$15 億貸款 ✓、密西根州 US$3 億 ✓、2025-08-27 重啟運轉 ✓、三分之二產能售予 Wolverine ✓。七個要素零誤差。
- **12 檔候選名單零 DD 宣稱 `ls` 覆核為真**：VST／CEG／NRG／EMR／XOM／CVX／COP／LMT／RTX／NOC／MLM／VMC 站內確實無 DD。
- §8 VRT 切給鏡頭二、Cummins 切給鏡頭四，理由明寫，與 semis 頁無衝突。標點全形（僅 E-Y6 一處簡體）、描述器紀律清潔、Exhibit 1–8 連號。

---

## 五、hidden-champions（中小型隱形冠軍）

83,134 bytes｜683 行｜§1–§10，`id="verdict"` 存在｜9 ddcards｜8 datanotes｜Exhibit 1–9

### 🔴 必修

**HC-R1（Exhibit 7、Exhibit 1）「單位數占比」欄位定義錯誤，且與「負值占比」重複計數。**

我以 `_universe.json` 對 SP400＋SP600 按 GICS 子產業獨立重算：

| 子產業 | 檔數 | ROE 中位數 | 頁面「單位數占比」 | 實際單位數（0<ROE<10%） | 負值占比 |
|---|---|---|---|---|---|
| Semiconductor Materials & Equipment | 16 | 8.3% | 56.3% | **31.2%** (5/16) | 25.0% |
| Aerospace & Defense | 14 | 10.1% | 50.0% | **42.9%** (6/14) | 7.1% |
| Electronic Equipment & Instruments | 12 | 11.3% | 33.3% | **16.7%** (2/12) | 16.7% |
| Application Software | 24 | 13.6% | 41.7% | **37.5%** (9/24) | 4.2% |
| Industrial Machinery & Supplies | 29 | 14.7% | 31.0% | **27.6%** (8/29) | 3.4% |
| Electrical Components & Equipment | 11 | 17.4% | 27.3% | **18.2%** (2/11) | 9.1% |
| Systems Software | 7 | 18.6% | 14.3% | **0.0%** (0/7) | 14.3% |

**檔數、中位數、負值占比三欄全部逐格命中**，唯獨「單位數占比」系統性偏高——它算的是 **ROE < 10%（含負值）** 的占比。負 ROE 不是「單位數」，而旁邊的負值占比欄又把同一批公司再數一次。Exhibit 1 的「單位數 ROE 檔數」欄同錯（頁面 7／9／4／3／10／1／9 vs 實際 6／8／2／2／9／0／5）。Exhibit 1 的 ex-take「16 檔中有 9 檔落在單位數、4 檔為負值」讀起來是 16 檔裡 13 檔出問題，實際是 5 單位數 ＋ 4 負值。

其他三欄全對這件事本身就是證據：這是**欄位定義錯**，不是計算錯。

**HC-R2（L552、L664）兩則頭條宣稱因 HC-R1 連鎖失真，且其中一則連叢集數都算錯。**
- §7 thecall（L552）：「**五個叢集**裡有三個叢集…」——本頁是**七個**叢集，不是五個。
- §10 答案節（L664）：「**逾半數叢集**有三分之一以上成分股 ROE 掉在單位數」——即使照頁面自己（膨脹的）定義也只有 3/7，不是逾半；照正確的單位數定義只有 2/7。**這是本頁答案節的核心論述句，兩種定義下都不成立。**

**HC-R3（L459）VICR 缺口宣稱不實，連帶 §8 覆蓋統計失準。**
§4.3 datanote 稱「GGG／POWL／VICR／RBC／FLS／NPO／ZWS 七檔均無站內既有 DD」，§4.2 且把 Vicor 放進 §8 候選隊列。但 **`docs/dd/DD_VICR_20260524.html` 存在**（schema v12.4、verdict B、83 天、窗內）。§8「9 檔 DD／27 檔無 DD」的覆蓋統計因此差一檔，且違反鐵律 7（有 DD 的名字必須逐字抄 dd-meta 裁決，不得自撰）。
我把該清單其餘 20 檔逐檔 `ls` 覆核——ULS／EXPO／MIR／BRKR／RBC／NPO／HXL／MOG-A／ITT／GGG／POWL／FLS／ZWS／CGNX／NSSC／OSIS／MANH／BLKB／APPF／IDCC 確實全數零 DD，**VICR 是唯一的假陰性**。

**HC-R4（15 行）標點違規：CJK 後半形逗號 35 處。**
行號 352、359、374、376、400、401、408、416、418、535、570、610、617、**664**、668。其中 L664 就是 §10 答案節的標題句：「地位轉成報酬，是例外而非常態，必須逐檔驗算，不能用「隱形冠軍」四個字帶過。」違反鐵律 3，且會被 `scripts/qc.py` 擋下。另 L352 一處簡體：「三檔**认证**壁壘」應為「認證」。

**HC-R5 被併購方視角整軸未查。** 「併購」8 次命中全部是商譽／攤銷的會計討論（BRKR、MIR），沒有一次談 M&A 作為出場路徑。對一個「中小型利基龍頭」鏡頭，這是最結構性的價值地板——這批名字正是策略買家與 PE 溢價收購的標準獵物，本頁多檔（MWA、GHM、POWL、NSSC、EXPO）市值恰在典型 take-out 區間。無專節、無 Exhibit、無缺口自陳。

### 🟡 建議

**HC-Y1（L359 及 §10）「超過 160 檔」與實際 162 檔。** 我重算：小於 CRS（US$271 億）的 S&P 500 成分股 ＝ **162** 檔，小於 ATI（US$311 億）＝ **189** 檔。189 抄得精確，160 相形之下像是取整草率，建議一致寫實數。

**HC-Y2 SP400 市值中位數 US$8.98B vs 實際 US$8.96B。** 上界 US$39.28B 完全正確。

**HC-Y3 Exhibit 1 ex-take 的重複計數**（見 HC-R1 末段），隨欄位修正一併處理。

### 🟢 驗證通過

- **叢集統計除單位數欄外全數獨立重算命中**：七個叢集的檔數（16／14／12／24／29／11／7）、ROE 中位數（8.3／10.1／11.3／13.6／14.7／17.4／18.6）、負值占比（25.0／7.1／16.7／4.2／3.4／9.1／14.3）逐格無誤。
- **母體與個股數字全對**：1,002 檔 ＝ SP400 400 ＋ SP600 602 ✓；CRS US$270.6 億、ATI US$311.1 億、HXL US$78.7 億、MOG-A US$139.7 億全對；ROE：ULS 38.7、EXPO 31.2、MIR 1.5、BRKR 負值、MWA 21.7、RBC 9.7（營收 +19.2%）、NPO 2.9、ITT +51.5%、VICR 20.1 全對。
- **9 檔 DD 逐字比對全對**：連結有效且最新、裁決抄錄無誤、天數重算全對（83／89／78／43／32 等），「9 檔全數窗內」成立，「無一檔評級為進場｜核心」成立（WLDN 為進場｜衛星持倉，判讀正確）。
- **UL Solutions 一節是全批 sourcing 誠實度的範例**：明寫查無可驗證的市占率百分比、拒絕估一個數字充數。
- 跨市場字串零命中、描述器紀律清潔、Exhibit 1–9 連號、`id="verdict"` 存在。

---

## 修正工待辦清單（按頁分組）

### healthcare（1 🔴 / 3 🟡）
1. 🔴 補 Medicare Advantage 資金壓力軸：CMS 費率通知、v28 風險調整模型、利用率、星級評等；至少在 §4 增一小節或一張 Exhibit，不能只留 DOJ 訴訟視角（L432、L447）。
2. 🟡 L555 MCK ddcard 裁決補全為 dd-meta 原文「A 核心候選 / 觀望偏進場（pullback 中）」。
3. 🟡 L347 「Rybelsub」→「Rybelsus」。
4. 🟡 kdstrip 178 檔標明為 GICS ∪ Yahoo 聯集（與 financials 同步處理）。

### financials（4 🔴 / 5 🟡）
1. 🔴 補地區銀行軸（存款貝他／NIM 敏感度／存款結構）。
2. 🔴 補商用不動產曝險軸。
3. 🔴 把私人信貸循環寫成一條軸（利差、PIK、退出通道），不能只留 ARES 市占率的單點缺口自陳（L403）。
4. 🔴 L258 kdstrip：「GICS Financials 278 檔」改為「GICS ∪ Yahoo 聯集 278 檔」或把數字改為 259。
5. 🟡 補支付新規軸（interchange／Durbin／CFPB），錨在 COF／PYPL／SEZL。
6. 🟡 補資本適足實質內容（Basel III endgame／CET1／壓力測試）。
7. 🟡 L495 移除「原文誤植單位，應為…」的編輯自語，直接寫 US$3,655 億。
8. 🟡 toc §8 改連 `#verdict`。
9. 🟡 L460 FICO +24.1% 與快照 25.7% 在正文對帳一句。

### consumer（4 🔴 / 3 🟡）
1. 🔴 補關稅／進口成本軸——這是本鏡頭「定價權」問句的即時實測場（目前僅 L509 一處順帶）。
2. 🔴 補自有品牌滲透率軸。
3. 🔴 L419 修 CL 列 ROE 欄（現誤植 P/E 值「36.2x」），保留「股東權益基數低」註解或改標 NM。
4. 🔴 L423 補 DECK 完整數列（US$126.8 億／fPE 11.13／ROE 42.56%，來源 `_universe.json`），並刪除 L431、L654 兩處不實的「未見於 `_universe.json`」缺口宣稱。
5. 🟡 L668 收掉 marketplace「留待裁定」的懸置語，改為單句歸屬說明（orchestrator 已裁定鏡頭三）。
6. 🟡 L511 「卖方叙事」→「賣方敘事」。
7. 🟡 DECK ddcard role 統一取自 `dca_role`。

### energy-industrials（3 🔴 / 6 🟡）
1. 🔴 §9 加上 `id="verdict"`（現為 `id="s9"`，L735），toc 對應改連 `#verdict`。**全批唯一缺此錨點的頁面。**
2. 🔴 補 LNG 出口軸（出口建設、對本土氣價與需求的傳導），接回 §4 油氣。
3. 🔴 L623 HUBB ddcard 補全 dd-meta 原文，「核心候選進場」不可截掉。
4. 🟡 L384 變壓器／電網設備交期換源再試（DOE 供應鏈報告、Hitachi Energy／Siemens Energy IR、NEMA）再決定是否落為永久缺口。
5. 🟡 §1.1 PJM「一年 8 倍」加限定語（跨兩次拍賣週期），數字本身忠實不必改。
6. 🟡 §1、§4.3 對 TLN／FSLR／LEU／MP 加回指站內既有 DD 的交叉引用；§4.3「未逐一覆核」措辭需改（四檔 DD 皆在窗內）。
7. 🟡 LEU 表列裁決補全 dd-meta 原文。
8. 🟡 統一評級前綴渲染（GEV／PWR／HON／CAT／URI／BE／RKLB 應同 TT 顯示等級）。
9. 🟡 L334 「标记」→「標記」。

### hidden-champions（5 🔴 / 3 🟡）
1. 🔴 Exhibit 7「單位數占比」與 Exhibit 1「單位數 ROE 檔數」兩欄改為排除負值的真實單位數（正確值見 HC-R1 表），或改欄名為「ROE<10%（含負值）」並刪掉重複的負值欄。
2. 🔴 L552 「五個叢集」→「七個叢集」；隨欄位修正重算該句的三個叢集是否仍成立。
3. 🔴 L664 §10 答案節頭條「逾半數叢集…」重寫——兩種定義下皆不成立。
4. 🔴 L459 刪除 VICR 的零 DD 宣稱，補 `DD_VICR_20260524.html`（v12.4、B、窗內）的逐字裁決；§8 覆蓋統計由 9/27 改為 10/26（或依修正後重數）。
5. 🔴 15 行、35 處 CJK 後半形逗號改全形（352、359、374、376、400、401、408、416、418、535、570、610、617、664、668）；L352 「认证」→「認證」。跑一次 `python3 scripts/qc.py` 確認。
6. 🔴 補被併購方視角（策略買家／PE take-out 作為價值地板與出場路徑）。
7. 🟡 L359 及 §10 「超過 160 檔」→ 162 檔。
8. 🟡 SP400 市值中位數 US$8.98B → US$8.96B。
9. 🟡 Exhibit 1 ex-take「9 檔單位數 ＋ 4 檔負值」隨欄位修正改寫（真實為 5＋4）。

---

## 附記：本次未成立的疑點（避免下游重複追）

- **energy-industrials 的 TLN／FSLR／LEU／MP 曾被我懷疑漏出 DD 對帳——查證後撤回。** 四檔在 §7 Exhibit 7「其餘 23 檔」表中全部正確列出，日期、天數、裁決皆對。殘留問題僅是正文缺交叉引用（E-Y3，🟡）。
- **五頁 datanote 誠實度整體通過。** financials 與 consumer 用「列為缺口」「未覆核」措辭而非「缺口：」前綴，初次以 grep 掃「缺口：」得零是誤判，逐則展開後確認四頁的缺口自陳皆為實質揭露。唯二例外是 consumer 的 DECK（C-R4）與 hidden-champions 的 VICR（HC-R3）——這兩則是**假的誠實揭露**，比單純缺數字更需要修。
- **跨頁口徑無衝突**：V／MA 歸鏡頭四（financials §7 ＋ consumer §8 一致）、VRT 歸鏡頭二（energy §8 明文，semis 頁承接）、Cummins 歸鏡頭四；五頁 Exhibit 主表無同一 ticker 雙頁深查。
