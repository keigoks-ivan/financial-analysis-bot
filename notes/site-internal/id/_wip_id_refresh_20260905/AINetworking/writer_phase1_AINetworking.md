# writer Phase 1 — ID_AINetworking（裁決級 refresh，目標檔 `docs/id/ID_AINetworking_20260905.html`）

writer＝opus｜skill＝industry-analyst v4.0｜mega=`semi`／sub_group=`networking`（taxonomy 表 2 確認為裸值 `networking`，非 `semi.networking`）｜T1 floor **60**
前版 `ID_AINetworking_20260419.html`（id_version v2.0，judgment 2026-06-21 🔴）——本檔只讀 prior_brief，未讀前版 HTML 全文。

---

## (a) thesis sketch

### A-0 這輪 refresh 的觸發事實（三個，全部是前版沒有的）

1. **26 週報酬在同一產業內部裂成兩半**（as-of 2026-08-31，vs QQQ）：鎖喉／scale-up 端 ALAB +140.2、MRVL +129.6、LITE +37.6、CRDO +35.1；系統／模組／連接器端 APH −57.3、FN −36.9、AVGO −11.5、CIEN −11.0、COHR −0.6。同一個「AI 互連」標籤下，前四名與後五名的 26 週價差超過 190 個百分點。**前版把這整片當成一個 shortage 格，這件事本身已被市場否證。**
2. **倍數壓縮與營收高成長同時發生**（站上 DD 決策欄，未讀全文）：CRDO forward P/E(FY2) 17.05 而 5 年分位 **0**、COHR 19.92／分位 **0**、NVDA 16.67／分位 10、AVGO 18.83／分位 15；同時 CRDO Q1 FY27 營收 +115%、FY27 指引 >85%。**市場不是在給短缺付溢價，而是在用「兩年後見頂」的倍數定價。** 反向的兩檔是 ANET（42.1／分位 100）與 LITE（43.8／分位 92）。
3. **系統端的 AI 營收停滯**：ANET DD（2026-08-05）記載 FY26 三度上調至 $12.6B（+40%），但 $1.1B 加碼全來自非 AI，AI 目標連三季停在 $3.5B。這是「Ethernet scale-out 吃兩端」敘事的第一個實測缺口。

### A-1 thesis 一句話（草稿，Phase 2 定稿）

> AI 互連的稀缺**換位了**：不再是「交換晶片 vs 光模組」的全面短缺，而是分裂成「機櫃內的銅與光引擎仍在鎖喉、交換矽與白牌系統已進入多供應商競爭」；而市場已經先一步用「見頂倍數」把整片定價完畢（多檔 forward P/E 落在自身 5 年最低分位）。真正還沒被定價的爭點只有一個——**每顆加速器的網路 dollar content 曲線**能不能在算力 capex 走上高原之後，仍靠 NVL 世代擴張與 800G→1.6T→3.2T 的速率跳代，把成長持續期再延三年。

### A-2 承重論證鏈（Phase 2 要用證據撐起來的四段）

| 段 | 主張 | 需要的承重數字 | 問題編號 |
|---|---|---|---|
| ① 分裂是真的 | 光引擎（EML／InP）與 rack 內高速銅仍鎖喉，交換矽／白牌／AEC 已多供應商化 | EML lead time 週數逐期、AEC 競爭者認證清單、Teralynx 10／Tomahawk 6 出貨日 | B5／B6／B1 |
| ② 定價已跑到基本面前面 | 倍數壓到 5 年低位＝市場假設 EPS 兩年內見頂 | 各檔 forward P/E 現值 vs 5 年帶、現價隱含成長 | D5 |
| ③ 唯一未定價的變數＝含量曲線 | 每顆 GPU 的網路金額隨世代上升，可吸收單位量放緩 | NVL72／NVL144／Rubin 機櫃互連 BOM 金額、每 GPU 光模組顆數 | C2 |
| ④ 持續期的兩個裂縫 | CPO 提前（吃掉 pluggable 利潤池）／開放 scale-up 生態（吃掉 NVLink 租金） | Quantum-X／Spectrum-X Photonics 出貨日、UALink 1.0 矽產品出貨 | E2／E5 |

### A-3 對前版三條非共識（NC）逐條表態

| 前版 NC | 前版判定 | **本版表態** | 理由（Phase 2 需證據補強） |
|---|---|---|---|
| **NC#1** scale-up／scale-out 非 zero-sum、兩家共同 re-rate | INTACT | **承接但降級（半翻面）** | 「非 zero-sum」在**營收**面仍成立，但在**利潤池**面已被否證：26 週 AVGO −11.5、ANET AI 目標凍在 $3.5B、AVGO 自家 DD 的護城河趨勢標 ↓。scale-out 是單位成長最快、但也是商用矽競爭最烈的一層（AVGO／MRVL／NVDA Spectrum-X／白牌四方混戰）；scale-up 才是每 GPU 金額成長最快且供應商最窄的一層。改寫為：**兩場戰爭並存為真，但兩邊的「錢」不再等速——單位在 scale-out，租金在 scale-up。** |
| **NC#2** UALink／CPO 商用被 price 太早 | AT_RISK | **翻面** | 到 2026-09，市場對這兩件事的定價方向已經反過來：pluggable 光模組供應商（COHR 分位 0、FN −36.9、CIEN −11.0）被定價成「CPO 一來就結束」，而 UALink 的實際矽產品仍未見量產出貨。本版新主張：**被 price 太早的不是商用時點，而是替代的「完全性」**——CPO 與 pluggable 的並存期、UALink 與 NVLink 的並存期，都比市場現在給的價格假設更長。此翻面的證偽物在 E2／E5。 |
| **NC#3** 零組件鎖喉＝被低估的稀缺 | INTACT | **承接，但要分兩半並自我糾錯** | 26 週實績支持鎖喉論（ALAB／MRVL／CRDO／LITE 全數大幅超額）——**但前版的行動句「非追高」把自己識別出的正確標的排除掉了，這是本版必須正面認的錯**（前版 action 寫「CRDO／ALAB／LITE 已大幅 re-rate、非追高」，其後 26 週分別 +35.1／+140.2／+37.6 vs QQQ）。同時鎖喉本身在分化：AEC 端已出現多供應商與價格壓力訊號（CRDO 財報後自高點 −45%），光引擎端仍緊（COHR 護城河趨勢 ↑）。 |

### A-4 新增非共識（本版候選，Phase 2 擇 2 條進 debates）

- **NC#4｜含量曲線 > 單位曲線**：AI 網路營收的驅動已從「多少顆 GPU」轉為「每顆 GPU 值多少網路錢」。若 NVL 世代的機櫃內互連 BOM 每代 +1.5～2×、光模組每 GPU 顆數隨 scale-out radix 上升，則網路營收可在算力 capex 高原期仍維持成長——這正是與姊妹報告 `ID_AIComputeCapexCycle_20260903` 的接縫，也是本版最重要的可證偽主張。
- **NC#5｜圈外威脅是需求方自供，不是中國替代**（外部威脅卡候選）：市場的替代討論集中在 CPO 與 UALink，但一階威脅其實是 hyperscaler 在**網路層**的垂直整合（自研 NIC／自研交換系統／光路交換 OCS／白牌 ODM 直採）。這條在前版完全缺席（前版 related_tickers 無任何白牌 ODM），本版擬補 2345.TW（智邦 Accton）作為「非顯而易見受益者／同時是威脅載體」。
- **NC#6（備選，資料若不足則降為折疊層一句）｜APH／FN 的報酬異常可能是資料假象**：APH 26W −37.1%／52W −24.8% 與其 DD（2026-07-30，進場｜核心｜護城河 ↑）方向嚴重矛盾，且幅度接近「2:1 分割未調整」的特徵值。**這是必須先驗證再解讀的資料完整性問題**（問題 D8），不可直接當成基本面訊號寫進報告。

### A-5 暫定五格燈號猜想（Phase 2 依證據可動）

| 格 | 前版 | **本版暫定** | 猜想理由 | 什麼證據會推翻我的暫定值 |
|---|---|---|---|---|
| 供需 | shortage | **split（分裂）** | 光引擎／rack 內銅＝短缺；交換矽／白牌系統／AEC＝平衡。26 週報酬 190pp 的內部價差就是分裂的市場證言 | 若 B5 顯示 EML lead time 已回 <12 週且 D6 顯示 800G ASP 年減 >15%，則整體改 **balance**；若 B6 顯示 AEC 競爭者仍無量產認證且 D3 全線 lead time 仍拉長，則回 **shortage** |
| 時鐘 | II | **II 末段**（傾向，備選 III 高原） | 營收動能仍在（CRDO FY27 指引 >85%），但倍數已用 III 的方式定價；capex／折舊與 lead time 是裁決依據 | D2 若顯示光模組廠 capex／折舊 >2.0 且擴產已排到 2027，判 II 末段；若 <1.3 且 D4 存貨天數上升，直接判 III |
| 信心 | mid | **mid** | 分裂判斷本身信心尚可，但含量曲線（NC#4）缺公開一手數字，是全報告最弱的一環 | C2 若能拿到官方或 T3-A 的機櫃互連 BOM 拆解，可升 mid-high |
| 已定價 | （前版空白，未填） | **mid（部分反映）** | 短缺與高成長已大多反映在 EPS 與股價；被折價的是**持續期**而非成長率 | D5 若顯示多數檔倍數其實在 5 年中位以上，改 high；若隱含成長已低於共識 CAGR 一半，改 low |
| 5 年需求倍數 | ×3.4 | **×2.8–3.2（暫填 3.0）** | 前版 3.4 建立在 2030 back-end switch >$100B；本版擬改用「AI 網路整體（back-end＋front-end＋光模組）」口徑並以三家獨立預測交叉 | C1 三家預測中位數落在哪一格決定最終值；口徑須在報告中寫明（前版未寫清） |

**校準自覺**：前版落在 shortage × Phase II（校準已知的唯一系統性失效格，勝率 7/25）。本版改 **split × II 末段** 不是為了避格而避格——分裂的市場證據（26 週 190pp 內部價差）、AEC 多供應商化、ANET AI 目標凍結三件事是獨立於校準結論的實證。但若 Phase 2 證據反而支持全面短缺，我會如實回到 shortage 並在報告內寫明「明知落在失效格仍如此判」的理由。

### A-6 站內 DD 裁決 × 其後報酬的矛盾（必須在 valuation／stocks 正面處理）

| Ticker | DD 日期 | 裁決／角色 | 26W vs QQQ | 矛盾性質 |
|---|---|---|---|---|
| APH | 2026-07-30 | 進場｜核心｜護城河 ↑ | **−57.3%** | 最嚴重。先驗證是否為分割未調整（D8），再論基本面 |
| ANET | 2026-08-05 | 觀望｜追蹤（IRR 3.9） | **+25.7%** | 觀望期間大漲；但倍數已到 5 年 100 分位，觀望的理由是估值不是生意 |
| LITE | 2026-08-12 | 觀望｜候選（IRR 7.5） | +37.6%（52W +464.2%） | 同上，且分位 92 |
| CRDO | 2026-09-04 | 進場｜衛星（EV5Y 98.2） | +35.1% | 一致，但「自高點 −45%」須在報告寫成「品類創造者遇到第一次多供應商衝擊」 |
| MRVL | 2026-08-31 | 觀望｜衛星 | +129.6% | 觀望期間翻倍以上，是本版最該解釋的一檔 |
| ALAB | 2026-05-22（v12.4 legacy） | 觀望 | +140.2% | 同上；legacy DD 已 105 天，屬 stale-judgment |
| AVGO | 2026-09-03 | 進場｜衛星｜**護城河 ↓** | −11.5% | 護城河趨勢向下＋報酬落後，支持 NC#1 的降級 |

---

## (b) id-meta 草稿欄位

```json
{
  "theme": "AI Networking",
  "skill_version": "v4.0",
  "id_version": "v4.0",
  "publish_date": "2026-09-05",
  "thesis_type": "mixed",
  "ai_exposure": "core",
  "oneliner": "AI 互連的稀缺換位了——不再是全面短缺，而是分裂成『機櫃內的銅與光引擎仍鎖喉、交換矽與白牌系統已進入多供應商競爭』；市場已用『兩年後見頂』的倍數把整片定價完（多檔 forward P/E 落在 5 年最低分位），唯一還沒被定價的是每顆加速器的網路含量曲線能不能把持續期再延三年。",
  "now_state": "【待證據填數】分裂：光引擎（EML／InP）與機櫃內高速銅連接仍供不應求，交換矽、白牌系統與 AEC 已進入多供應商競爭；營收仍高速成長（CRDO Q1 FY27 +115%、FY27 指引 >85%），但 forward P/E 壓縮至 5 年最低分位（CRDO 17.0x／分位 0、COHR 19.9x／分位 0，as-of 各自 DD 日）。",
  "future_state": "【待證據填數】未來 3–5 年決定成長斜率的不是 GPU 顆數而是每顆 GPU 的網路金額：NVL 世代機櫃互連 BOM 與 800G→1.6T→3.2T 速率跳代能否抵銷算力 capex 走上高原；兩條裂縫是 CPO 對 pluggable 的替代完全性與 UALink 對 NVLink 租金的侵蝕速度。",
  "action": "偏重『鎖喉仍在、但倍數已被壓到 5 年低位』的交集；避開『倍數在 5 年高位且 AI 營收動能停滯』的系統端；本版明確糾正前版把已識別的鎖喉標的以『非追高』排除的錯誤。",
  "sd_verdict": "split",
  "sd_verdict_detail": "光引擎與機櫃內銅＝短缺；交換矽／白牌系統／AEC＝平衡（轉競爭）",
  "clock_phase": "II",
  "conviction": "mid",
  "priced_in": "mid",
  "demand_5y_multiple": 3.0,
  "tam_usd_2030": "【待 C1 三家交叉後填】",
  "cagr_pct_5y": "【待 C1 後填】",
  "growth_phase": "expansion-late",
  "value_chain_position": "midstream",
  "industry_structure": "分層寡占（交換矽雙強／光引擎雙強／AEC 單強轉多強／系統多方）",
  "quality_tier": "A",
  "mega": "semi",
  "sub_group": "networking",
  "sister_ids": [
    "ID_SiliconPhotonicsCPO_20260419.html",
    "ID_AIComputeCapexCycle_20260903.html",
    "ID_AIAcceleratorDemand_20260905.html",
    "ID_HBM_Supercycle_20260904.html",
    "ID_AdvancedPackaging_20260905.html"
  ],
  "sections_refreshed": {"technical": "2026-09-05", "market": "2026-09-05", "judgment": "2026-09-05"}
}
```

### related_tickers 草稿（含前版對應核對結果）

**前版 ticker↔公司對應核對：10 檔全部正確**（NVDA=NVIDIA、AVGO=Broadcom、CRDO=Credo、MRVL=Marvell、ALAB=Astera Labs、ANET=Arista、COHR=Coherent、APH=Amphenol、LITE=Lumentum、FN=Fabrinet），無前版 6146.T 型的錯標。前版 `sister_ids` 全部指向 2026-04-19／06-11 舊版，本版全部改指最新版（見上）。前版 `priced_in` 欄為空（None）——本版必填。

| Ticker | 深度 | 角色（草稿） | 純度推導（Phase 2 要補實數） | 變動 |
|---|---|---|---|---|
| NVDA | 🔴 | scale-up NVLink 租金＋Spectrum-X／InfiniBand；networking 分部季營收為外部驗證器之一 | networking 分部占總營收 %（C5） | 承接 |
| AVGO | 🔴 | scale-out 交換矽主場（Tomahawk 6／Jericho 4／Tomahawk Ultra）；自家 DD 護城河趨勢 ↓ | AI networking 占 AI 半導體營收 %（B2） | 承接，敘述降級 |
| CRDO | 🔴 | AEC 品類創造者（份額 73–88%）＋光學第二曲線；本版的「鎖喉點正在多供應商化」測試檔 | AEC＋光 DSP 占營收 %（B6） | 承接 |
| MRVL | 🔴 | 光 DSP／SerDes＋自研 ASIC 互連＋Teralynx 交換矽＋Celestial AI | 資料中心互連相關占營收 %（B1／B8） | 承接 |
| ALAB | 🔴 | scale-up retimer／Scorpio fabric pure play；legacy DD 已 105 天 | 幾近 100%（B7 確認） | 由 🟡 升 🔴 |
| COHR | 🔴 | InP／EML 光引擎＋800G／1.6T 模組；本版「光層仍鎖喉」的主要證據載體 | Datacom 占營收 %（B5） | 由 🟡 升 🔴 |
| ANET | 🟡 | Ethernet 系統 OEM；AI 目標凍結＋倍數 5 年 100 分位 | AI 營收占總營收 %（B3） | 承接 |
| LITE | 🟡 | 200G/lane EML 供應商；倍數分位 92 | EML／datacom 占營收 %（B5） | 由 🟢 升 🟡 |
| APH | 🟡 | 高速連接器／機櫃內銅互連 | IT datacom 分部占營收 %；**先解 D8 分割疑點** | 承接（附資料警示） |
| CIEN | 🟡 | **新增**：DCI／相干光與 hyperscaler 直採；52W +149.7 vs QQQ 但 26W −11.0 | Cloud/DCI 占營收 %（B4） | **新增** |
| 2345.TW | 🟡 | **新增**：智邦 Accton，白牌交換器 ODM；同時是「需求方自供／白牌直採」威脅的載體 | 資料中心交換器占營收 %（E3） | **新增** |
| FN | 🟢 | 光學 ODM（NVDA／Ciena 代工）；CPO／pluggable 並存下的 picks-and-shovels | 光通訊占營收 %（B4） | 由 🟢 維持 |
| 3661.TW | 🟢 | **新增（低優先）**：世芯 Alchip，HPC／網路 ASIC 設計服務；純度低，若 B 軸拿不到網路類專案佔比證據就不進表 | 網路類 ASIC 專案占營收 %（B1） | **新增，可刪** |

（🔴 檔須補 `mcap_bucket`；`purity_pct` 一律要有一行推導，無來源則降定性。）

### kill_metrics 草稿（≥3，含 ≥1 撮合價、≥1 外部驗證器）

| # | 指標 | 類型 | 熊線（草稿） | 現值來源 | 頻率／領先 |
|---|---|---|---|---|---|
| K1 | 800G／1.6T 光模組 ASP 逐季 | **市場撮合價** | 年減 >15% 且非規格跳代所致 | LightCounting／Omdia 原始新聞稿或廠商法說引述（D6） | 季／領先 2–3 季 |
| K2 | EML／InP lead time 週數 | **市場撮合價（第二個，須確認與 K1 非同源）** | 回落至 <12 週 | COHR／LITE 法說逐字（B5／D3） | 季／領先 2 季 |
| K3 | AVGO＋ANET＋CRDO 網路營收 QoQ 合計 | **外部驗證器** | 連續兩季合計 QoQ <0 | 各家 10-Q（D7） | 季／同步 |
| K4 | NVDA networking 分部季營收 | 外部驗證器（承接前版） | 跌破 $12B | NVDA 10-Q（C5） | 季／同步 |
| K5 | UALink 1.0 矽產品量產出貨 | 外部驗證器（時鐘換相用） | 2027 Q1 前無任一 hyperscaler 規模部署＝NVLink 租金多守一年 | 官方新聞稿（E5） | 事件 |
| K6 | AEC 第二／第三供應商量產認證數 | 結構驗證器 | ≥2 家取得 top-2 hyperscaler 量產認證＝CRDO 份額租金結束 | 官方新聞稿／法說（B6） | 半年 |

**換相雙閘（3.4 用，草稿）**
- 必要條件：光引擎 lead time 回到正常（K2 破線）**或** 800G／1.6T ASP 進入年減 >15%（K1 破線）。
- 充分條件（須**兩個獨立訊號同時滿足**，一個撮合價＋一個外部驗證器）：**K1（撮合價：ASP 年減 >15%）∩ K3（外部驗證器：三家網路營收合計連兩季 QoQ 負）**。
  - 獨立性論證：K1 來自第三方模組報價／機構逐期序列，K3 來自各公司 10-Q 已實現營收；一為價、一為量×價之實現值，且來源機構不同。K2 與 K1 皆為供應鏈價量指標，**若 Phase 2 發現 K2 的唯一來源也是廠商法說引述的同一批報價，則 K2 不得與 K1 併列為兩個獨立訊號**（同源撮合價換品類不算兩個）。
  - 禁用：任何預估值（LightCounting 的 2027E 預測、賣方目標價）不得充當雙閘之一，只有實績可以。

---

## (c) 封閉式問題清單（給採集 agent，sonnet）

**通則**：每題回 `{題號}｜{數字或事實}｜{來源 URL}｜{as-of}｜{T級}`。承重數字（TAM／capex／分部營收／指引／lead time／ASP）**必須直讀 10-Q／10-K／8-K／官方新聞稿／法說逐字稿**，財經彙整站只能標 T2／T3 且不得作為承重數字唯一來源。查不到就寫「查不到」，**禁止用訓練知識推估**。所有數字須帶 as-of；跨年度比較須註明是 FY 還是 CY。中國／台灣來源標 `-zh` 後綴。

### Axis A — 歷史與 cycle 統計（附錄歷史錨點＋3.3 S 曲線）

- **A1**｜乙太網速率世代的 IEEE 標準批准年月與首次量產出貨年：10G／40G／100G／400G／800G／1.6T 各一組（標準批准日取 IEEE 802.3 官方；量產起點取廠商官方新聞稿）。
- **A2**｜InfiniBand vs Ethernet 在 TOP500 系統數占比：2010／2015／2020／2025／2026-06 榜各一組（top500.org 官方統計頁）。
- **A3**｜NVLink 每 GPU 雙向頻寬與機櫃域大小逐代：NVLink 2/3/4/5（及已公布的次代）——頻寬 GB/s、單一 NVLink 域最大 GPU 數、發表年（NVIDIA 官方白皮書或 GTC keynote 簡報）。
- **A4**｜前次光通訊資本週期的峰谷幅度：JDS Uniphase／Finisar／Lumentum 三家中任兩家，2000–2003 與 2017–2020 兩輪的營收峰值年、谷底年、峰到谷營收跌幅 %（10-K）。**這是本報告歷史類比表的承重資料，缺了就用 T2 產業統計替代並註明。**
- **A5**｜800G 光模組 ASP 的歷史落點：100G QSFP28（2018/2020）、400G（2021/2023）、800G（2024/2025/2026）各一個 ASP 數字，用來證明「速率跳代時 ASP 上跳、代內每年下滑」的規律（LightCounting／Omdia／Yole 原始新聞稿；廠商法說口徑亦可但須標明）。

### Axis B — 供給（玩家矩陣／利潤池／成本曲線／capex）

- **B1**｜交換矽產品與出貨時點：Broadcom Tomahawk 6（102.4T）、Tomahawk Ultra、Jericho 4；Marvell Teralynx 10（51.2T）；NVIDIA Spectrum-X／Spectrum-6——各給「發表日、量產出貨日（若已公告）、標稱總頻寬」（官方新聞稿）。
- **B2**｜**AVGO 最近四季**（含 2026-09 公布的 FY26 Q3）：總營收、AI 半導體營收、**networking 營收（若分列）**、下一季 AI 營收指引數字——直讀 10-Q 與法說逐字稿原話。**禁 Q×4 推年度**。
- **B3**｜**ANET 最近四季**：總營收、FY26 全年指引最新值、**AI 相關營收目標數字與其最近三次法說的表述原句**、遞延營收（deferred revenue）、採購承諾（purchase commitments）——10-Q。
- **B4**｜光模組／系統供給端最近一期：Innolight 中際旭創(300308.SZ)、Eoptolink 新易盛(300502.SZ)、Coherent、Lumentum、Fabrinet、Ciena——各給最近一季營收、YoY、以及**任一條關於 800G／1.6T 產能或交期的官方原話**（公司公告／法說；陸股用巨潮/交易所公告，標 T1-zh）。
- **B5**｜**光引擎鎖喉的現值**：Coherent 最近一季（FY26 Q4，2026-08 前後）與 Lumentum 最近一季法說中，關於 **InP／EML 產能、lead time 週數、datacom book-to-bill、售罄到哪一年** 的原句與數字，各至少一條（法說逐字稿）。**這是全報告最關鍵的單一證據，若拿不到請明確標「查不到」，不要用舊季度充當現值。**
- **B6**｜**AEC 競爭格局的現值**：(i) Credo 最近一季 AEC 相關營收與其在法說中對份額／價格的原句；(ii) 列出所有**已公告量產或客戶認證**的 AEC 競爭產品（Marvell、Astera Labs、Amphenol、TE Connectivity、Semtech CopperEdge、Spectra7、Point2 等），每家給產品名＋公告日＋是否已具名客戶（官方新聞稿）。
- **B7**｜retimer 供給：Astera Labs 最近一季營收、Aries／Scorpio 產品線營收占比（若有揭露）；競爭者（Broadcom PCIe retimer、Montage、Parade、Rambus）已公告的 PCIe 6.0／224G 產品與出貨狀態。
- **B8**｜**利潤池（總額占比，不是毛利率）**：2025 財年（或最近四季加總）各環節的營收與營業利益絕對金額——交換矽（AVGO 相關分部）／交換系統（ANET＋Cisco 相關分部＋Accton）／光模組（Innolight＋Eoptolink＋COHR datacom＋LITE）／DSP·retimer·AEC（MRVL 資料中心＋CRDO＋ALAB）／連接器與線纜（APH IT-datacom 分部＋TE 相關分部）。**每格都要有 10-K/10-Q/年報出處；拿不到營業利益就只給營收並標明，不要自行估算利潤率。**
- **B9**｜成本曲線素材：800G 光模組的 BOM 結構拆解（EML laser／DSP／封裝各占成本 %），任一可具名來源（T2 或 T3-A 皆可，須標機構名與日期）；以及各主要模組廠最近一季毛利率。

### Axis C — 需求（TAM 推導鏈與含量曲線）

- **C1**｜**AI 網路 TAM 三家獨立預測**：Dell'Oro Group、LightCounting、650 Group（或 Omdia／Yole 替代），各給「2026 與 2030（或其最遠年）的市場規模數字＋口徑定義（是否含 front-end／光模組／NIC）＋發布日」，來源須為**原始機構新聞稿**而非二手引用。三家口徑不同要如實並列，不要調和。
- **C2**｜**每顆加速器的網路含量（本報告最關鍵的新變數）**：(i) GB200 NVL72 機櫃的 NVLink 銅背板／線纜數量與（若有官方或具名拆解）金額；(ii) 每顆 GPU 對應的 800G 光模組顆數（scale-out 側）在 NVL72 與次代機櫃的差異；(iii) 任一具名機構對「每 GPU 網路支出美元」的估算與其口徑。**若只找得到 T3-A 拆解，照收但標明機構與日期；若完全查不到，明確回報「查不到」——這決定本報告的信心格。**
- **C3**｜800G 與 1.6T 光模組出貨量（單位：百萬顆或萬顆）：2024 實績、2025 實績、2026E、2027E，來源 LightCounting／Omdia 原始新聞稿，標明哪些是實績、哪些是預估。
- **C4**｜四大 hyperscaler（MSFT／GOOGL／AMZN／META）最近一季法說對 **2026 與 2027 capex** 的最新表述原句與數字（10-Q＋法說逐字稿）；若任一家有揭露「網路占資料中心投資比例」的口徑，一併給出。
- **C5**｜**NVDA networking 分部最近四季營收**（FY27 Q1、Q2 及前兩季），YoY 與 QoQ，直讀 10-Q。
- **C6**｜客戶集中度：CRDO、ALAB、COHR、LITE 各自最近一份 10-K／10-Q 揭露的「前兩大客戶占營收 %」。

### Axis D — 驗證（三角對帳／資本週期／撮合價／庫存／priced-in）

- **D1**｜三角對帳素材：2026 年四大 hyperscaler capex 指引合計（來自 C4）vs 本報告核心供應商（NVDA networking＋AVGO 網路＋ANET＋COHR datacom＋光模組四家）2026 營收共識合計——共識數字給來源與日期。兩條路徑差 >20% 時請如實回報差距，不要調和。
- **D2**｜**資本週期三指標**（至少要有兩個帶數字）：(i) COHR、LITE、Innolight、AVGO 最近一個完整財年的 **capex／折舊比**（10-K 現金流量表與折舊費用直讀）；(ii) 上述各家最近一個財年的 ROIC（或 ROIC 可算的分子分母原始數字）；(iii) 產業擴產 lead time（新建 InP 產線／模組產線從動工到量產的月數，任一公司官方說法）。
- **D3**｜**lead time 逐期序列**：EML／InP、800G 模組、交換 ASIC 三類，各給「現在」與「6 個月前」「12 個月前」的交期週數（法說原話或機構調查），**目的是判斷方向而不只是水位**。
- **D4**｜庫存與訂單：COHR datacom book-to-bill 最近兩季；ANET 遞延營收與採購承諾最近兩季；CRDO、ALAB 的 backlog 或能見度表述原句；光模組四家最近兩季存貨週轉天數。
- **D5**｜**priced-in 素材**：NVDA、AVGO、ANET、CRDO、MRVL、ALAB、COHR、LITE、APH、CIEN、2345.TW 各給 (i) 現行 forward P/E（FY1 或 FY2，註明哪一個）(ii) 過去 5 年 forward P/E 的區間與現在的分位 (iii) 現價與 as-of 日。來源須可查（不接受無出處數字）。
- **D6**｜**市場撮合價（雙閘之一，最高優先）**：800G 與 1.6T 光模組 **ASP 的逐季或逐年序列**（至少 2024／2025／2026 三點，能給到季更好），來源優先 LightCounting／Omdia／TrendForce **原始新聞稿**或廠商法說中引述的具體單價；若模組 ASP 完全查不到，改給 **AEC 每條單價**或 **EML 晶粒單價** 的序列作替代，並明說是替代品。**這條若拿不到任何逐期數字，請在回報最前面標紅，因為它會影響報告的換相雙閘能否成立。**
- **D7**｜**外部驗證器（雙閘之二）**：(i) AVGO、ANET、CRDO 三家過去 6 季的網路相關營收 **QoQ 序列**（10-Q）；(ii) 2026 年內公開宣布的 **Ethernet AI 叢集部署**（hyperscaler／neocloud，含規模 GPU 數與網路方案），至少 3 例＋官方新聞稿；(iii) UALink 1.0 相關**產品出貨**公告（有／無，若無請明說「截至 as-of 無公開量產出貨公告」）。
- **D8**｜**資料完整性查核（優先處理）**：APH 與 FN 在 2026-01-01 至 2026-08-31 間是否有**股票分割、股利以外的特別配息或資本重組**？若有，給生效日與比例（公司 8-K／官方新聞稿）。**理由：站內週線報酬顯示 APH 26 週 −37.1%、52 週 −24.8%，與其自身 DD（進場｜核心）方向矛盾，幅度接近 2:1 分割未調整的特徵，必須先排除資料假象再做基本面解讀。** 同時請給 APH 與 FN 在 2026-02-28 與 2026-08-31 兩日的**除權息調整後**收盤價。

### Axis E — 替代與圈外掃描（五條，**不得因「顯然無關」跳過，查無威脅也要回報掃描結論**）

- **E1**｜**中國替代／國產**：(i) 中國國產交換晶片（盛科 Centec、華為海思）已公告的最高頻寬產品與量產狀態；(ii) 中國 800G／1.6T 光模組廠在**海外產能**（泰國／越南／馬來西亞）的布局公告；(iii) 美國出口管制是否已將高速網路設備（InfiniBand／Spectrum-X／高階交換晶片）納入管制清單——給 BIS 官方規則文號與生效日。
- **E2**｜**替代技術跳躍**：(i) NVIDIA Quantum-X Photonics／Spectrum-X Photonics（CPO）的**實際出貨時點與已具名客戶**（官方新聞稿）；(ii) Google 光路交換（OCS／Apollo）的最新公開部署規模；(iii) LPO／LRO（線性可插拔）對 DSP 的取代是否已有量產客戶；(iv) 空芯光纖（hollow-core fiber）在資料中心的任一商用公告。
- **E3**｜**需求方自供／垂直整合**：(i) AWS、Google、Meta、Microsoft 各自已公開的**自研網路矽或自研 NIC**（產品名＋公告日）；(ii) 白牌交換器（Accton 智邦、Celestica、Quanta）在 hyperscaler 的採用公告；(iii) 任一 hyperscaler 公開表態自研 AEC 或自研光模組。
- **E4**｜**監管／地緣**：(i) 對 AVGO、NVDA 的任何進行中反壟斷／綁售調查（官方或監管機關文件）；(ii) 2026 年美國對光模組／網路設備的關稅或原產地規則變動（USTR／CBP 官方）；(iii) 台灣／馬來西亞／泰國光通訊產能的地緣集中度數字（若有官方統計）。
- **E5**｜**標準與生態**：(i) UALink 1.0 規格發布日與**已公告採用該規格的矽產品清單**；(ii) Ultra Ethernet Consortium 規格版本、發布日與**已公告符規產品**；(iii) OCP ESUN 或其他 scale-up over Ethernet 倡議的成員與時程；(iv) PCIe 7.0 規格發布狀態。**這一軸的空白結論同樣重要——若截至 as-of 仍無量產矽，請明確寫「無」，這是本報告時鐘判斷的直接輸入。**

### 回報尾段必附

1. **T1（含 T1-zh）自估占比**，以及仍缺官方一手來源的承重數字清單。
2. **D6（市場撮合價）與 D7（外部驗證器）的取得狀況單獨列一段**，這兩條決定換相雙閘能否成立。
3. 任何兩個 T1 來源給出不同數字的情形，明列衝突與各自口徑，**不要擇一不說**。

---

## (d) Phase 2 我自己要做的判斷性搜尋清單

1. **分歧的最強版本**：找 2026 H2 的賣方 AI networking primer／sector update（Morgan Stanley、Goldman、Jefferies、Citi、New Street、Bernstein）——重點不是他們的目標價，而是**多頭與空頭各自最強的量化論證**，尤其是「為什麼 CRDO 財報大 beat 卻 −45%」「為什麼 APH／FN／CIEN 落後」的賣方解釋。三家都同向時要在 debates 特別小心。
2. **priced-in 的獨立算法**：用 D5 的倍數與共識 EPS，自算各檔**現價隱含的 3 年 EPS CAGR**，與共識 CAGR 對照，收斂 low／mid／high。核心 🔴 檔至少四檔要有這一行。
3. **含量曲線的第二來源**：C2 若採集端只拿到單一 T3-A 拆解，我自己再找一個獨立來源交叉（例如機櫃層級的功耗／材料清單公開資料、或 NVIDIA 官方 rack 規格頁），避免整條 NC#4 靠單一來源。
4. **時鐘換相雙閘的獨立性複核**：親自確認 K1 與 K3 的來源機構不同、且 K1 不是由 K3 的公司法說反推出來的（同源撮合價換品類不算兩個獨立訊號）。若 D6 完全落空，改用「AEC 單價序列＋K3」，並在報告中明寫替代理由。
5. **DD 裁決 × 報酬矛盾的處理**：MRVL（觀望後 +129.6）與 ANET（觀望後 +25.7）要在 valuation 段正面解釋——判斷是「產業對、個股估值閘擋掉」還是「產業判斷本身漏了一軸」。APH 待 D8 結果才處理。
6. **歷史類比的可寫性**：確認 2000–2002 光通訊泡沫與 2017–2019 中國 5G 前傳週期兩個先例的量化錨可用；若 A4 落空，改用 T2 產業統計並在附錄註明降級。
7. **與姊妹報告的接縫**：`ID_AIComputeCapexCycle_20260903`（算力 capex 高原）、`ID_AIAcceleratorDemand_20260905`（單位需求）、`ID_SiliconPhotonicsCPO_20260419`（CPO 專題，已 4.5 個月，屬 stale）、`ID_HBM_Supercycle_20260904`、`ID_AdvancedPackaging_20260905`——只在 summary crosslink 與 debates 內連出，**不重做其內容**；CPO 那份因已 stale，本報告的 CPO 判斷要能獨立成立，不得只寫「見該份」。
8. **`docs/supply-chain/cpo.html`** 在 stocks 段作為節點層連結（不重做節點圖）。

---

## (e) T1 floor 聲明

**T1 floor＝60%**（含 T1-zh），依 `references/sources.md`【T1 floor 依 mega 分型】：本報告 `mega=semi`，落在「其餘 11 個 mega」組。

- **本輪不申請 `--t1-floor 45` 覆蓋**。理由：本主題的承重數字（分部營收、指引、capex／折舊、lead time、客戶集中度、NVLink 規格、IEEE 標準日期）幾乎全部存在於 10-Q／10-K／官方新聞稿／法說逐字稿，屬 T1 供給充足型主題；唯一天生偏 T2／T3 的是**光模組 ASP 與 TAM 預測**（D6／C1），這兩項本來就該標 T2，不構成整體 floor 下修的理由。
- 若 Phase 2 收稿時 T1 占比落在 45–60 之間，我會先回頭直讀官方源補齊承重數字，而**不是**改用覆蓋旗；若補齊後仍 <60，才會啟用 `--t1-floor 45` 並在 check 報告尾與 summary 折疊各寫一句理由。**低於 45 一律停下回報，不灌來源。**
