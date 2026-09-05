你是 stock-analyst v17 判斷 agent，回來做**一輪定點修補**。標的 AVGO（20260905）。判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件：**針對被點名的欄位做最小修正**，不重寫判斷。

## 讀（僅此一個檔，一次讀完；其餘輸入已在下方 findings 內）

`.dd_build/runs/AVGO_20260905/judgment.json`

不要重讀 bundle、evidence.json、gate_audit.md、`docs/dd/` 任何檔，也不要回讀你等一下寫出的新版 judgment。你需要的稽核意見全文已附在下方。

## 閘的發現（gate findings）

### 發現 1：3 其他結構變數 🔴
- **依據**：substitute_technology#2（光學／光子 AI 加速器，2027-2031 商用，affects moat_trend、thesis.R）與 reg_tariff_export#2（BIS 2026-01-15 對中先進 AI 晶片改逐案審查）在 coverage 有料，judgment 全文無對應條目，亦未列入 evidence_dismissed[]
- **建議改法**：moat.threats 增「替代技術：光子計算 2027-2031」一條並在 premortem.blind_spots 記為 Y5 後假設；reg_tariff_export#2 併入 triggers[n=11] metric，或入 evidence_dismissed[] 寫明理由
- **指向欄位**：moat.threats／evidence_dismissed[]／triggers[n=11]

**受影響子樹原文**：

`moat.threats`：
```json
[
  {
    "level": "🔴 生態攻擊",
    "text": "Google 四夥伴供應鏈：MediaTek 推論 Zebrafish（Q4 2026 量產、成本低 20-30%）、Marvell 商業協議（2026-07-29）、Intel 處理器；Google 藉此取得定價與產能槓桿",
    "p": "60-70%（份額稀釋已在發生）",
    "evidence_refs": [
      "competitive_share_entrants#3",
      "customer_second_source#0",
      "customer_second_source#1"
    ]
  },
  {
    "level": "🔴 生態攻擊",
    "text": "MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場（$80B 估計），2026 資料中心營收 >$2B",
    "p": "50%",
    "evidence_refs": [
      "competitive_share_entrants#2"
    ]
  },
  {
    "level": "🟡 點對點",
    "text": "六大客戶各自投資內部設計能力，關係「深而黏但非永久」；風險因子明列客戶可能改採自有工具鏈（COT）或租賃模式",
    "p": "3-5 年 30%",
    "evidence_refs": [
      "customer_second_source#2",
      "customer_concentration_credit#2",
      "substitute_technology#1"
    ]
  },
  {
    "level": "🟡 點對點",
    "text": "VMware 資安事件（Aria Operations 零日遭中國國家背景組織利用；Clop 經 Oracle EBS 零日入侵 Broadcom 內部）削弱軟體信任",
    "p": "20%（信任型流失）",
    "evidence_refs": [
      "major_events#1",
      "major_events#2",
      "product_recall_warning#0",
      "product_recall_warning#1"
    ]
  }
]
```

**相關 evidence finding 原文**：

`substitute_technology#2`：
```json
{
  "claim": "光學 AI 加速器（optical/photonic computing）市場正快速成長，Ayar Labs、LightOn、Luminous Computing、Q.ANT、Salience Labs、Lightmatter、Optalysys 等新創正開發顛覆性架構，光學矩陣乘法引擎可在晶片層級以皮秒等級完成神經網路核心線性代數運算、耗能遠低於等效 GPU 運算，商用部署預期落在 2027-2031 年區間；Broadcom 本身也將光子能力納入其 AI 產品組合（如封裝內光學 I/O）。",
  "source": "GlobeNewswire, \"Optical AI Accelerator Market, 2026-2040 Industry Trends and Global Forecasts\"; yieldWerx, \"2026 Trends and Challenges in Photonics & Optical I/O Innovations\"",
  "as_of": "2026-05-13",
  "direction": "0",
  "affects": [
    "moat_trend",
    "thesis.R"
  ],
  "id": "substitute_technology#2"
}
```

`reg_tariff_export#2`：
```json
{
  "claim": "BIS (Bureau of Industry and Security) published a final rule effective January 15, 2026 revising export license review policy for advanced AI/computing semiconductors destined for China and Macau: applications now reviewed case-by-case instead of under a presumption of denial, but exporters must still confirm no restricted/Entity List/Military End-User parties are involved.",
  "source": "Morgan Lewis, \"BIS Revises Export Review Policy for Advanced AI Chips Destined for China and Macau\"",
  "as_of": "2026-01-15",
  "direction": "0",
  "affects": [
    "thesis.H",
    "decision_inputs.bear",
    "triggers"
  ],
  "id": "reg_tariff_export#2"
}
```


## 修補紀律

1. **只准改被點名的欄位**——findings 的「指向欄位」是你的動刀範圍。沒被點名的欄位一字不動，包含 `decision_out`（由 `dd_decision.py` 回填，你不要手改）與未涉及的 `reasoning` 段。
2. **裁決方向不由你主動翻**——修正欄位後若 `judge check` 重算出的 `decision_out.verdict` 自己翻面，那是機械層的結果，照實接受並在回報點名；但你不得為了配合閘的語氣直接改寫裁決字串。
3. **可以不採納**——閘的意見不是命令。判斷你認為原判正確時，該條不改欄位，改為在頂層 `evidence_dismissed[]` 補一條 `{"ref": "<閘點名的 finding ref 或欄位路徑>", "reason": "<不採納的具體理由>"}`。理由要指得出證據或推導本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代、閘誤讀了哪個欄位…），不得寫「影響不大」這類無內容句。**每一條 🔴 都必須有處置**：要嘛改欄位，要嘛進 `evidence_dismissed[]`，不得沉默略過。
4. **🟡 選擇性處理**——能一句話補上就補（通常是 `contradictions[]`／`triggers[]` 加一條或補 `formula_note`），代價過大就依第 3 條寫不採納理由。
5. **不得編造數字**——證據包未涵蓋的數字不准補；該欄位標「證據包未涵蓋」並在回報請 orchestrator 判斷是否回 Stage 0 補軸。
6. 禁 WebSearch／WebFetch。

## 寫（一次 Write 整檔）

改完後把**完整的 judgment.json**一次 `Write` 回 `.dd_build/runs/AVGO_20260905/judgment.json`（不要分次 Edit、不要只寫片段），接著跑：

```
python3 scripts/ddreport.py judge check AVGO 20260905
```

這支會依序重跑 `dd_scenario.py`、`dd_decision.py run`、`validate_judgment.py --evidence --fix --report`，一次把結果回給你；你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改 FAIL 訊息點名的欄位**，重跑同一條 `judge check`，**≤1 輪**。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置，不得為湊過驗證而改動判斷實質。

**輪次上限 `6` 輪。** 逼近上限時停下並照實回報。

## 回報（≤200 字）

① 逐條列閘的發現與你的處置（改了哪個欄位／或進 `evidence_dismissed[]` 及理由摘要）
② `judge check` 最後一次的 `validate_judgment.py --report` 原文
③ `decision_out.verdict`／`role`／`row_hit`，以及是否與修補前不同（翻面要明講）


## 判斷物全文（附於下方，**不要 Read 檔案**；改完把整份 JSON 一次 Write 到 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/judgment.json，然後跑一次 `python3 scripts/validate_judgment.py .dd_build/runs/AVGO_20260905/judgment.json --evidence .dd_build/runs/AVGO_20260905/evidence.json --fix --report`，FAIL 只准再改一次）

```json
{
  "meta": {
    "ticker": "AVGO",
    "date": "2026-09-05",
    "schema": "v15.0",
    "company_name": "Broadcom Inc."
  },
  "oneliner": "客製 AI ASIC 龍頭＋AI 網通＋VMware 三引擎；Q3 FY26 AI 營收 $16.7B（+221%）、FY27／FY28 AI 指引 $115B／$230B；財報後回檔至 FY27 本益比 18.5x、PEG 0.31；惟 Google 刻意四夥伴分單、MediaTek 推論晶片 Q4 量產，護城河趨勢↓；裁決進場｜衛星、上限 3%。",
  "archetype": {
    "primary": "品質複利成長",
    "secondary": null,
    "confidence": "高",
    "fingerprint": "FCF 利潤率 46%、非 GAAP 營業利益率 67.9%、資本支出占營收 <2%、營收 YoY +86%：輕資產設計＋高黏性軟體的複利體質，惟成長由 AI 資本週期驅動帶循環色彩"
  },
  "thesis": {
    "headline": "六客戶客製 XPU 平台把雲端自研晶片的利潤池搬到 Broadcom 手上；風險不在需求而在 Google 分單與 2028 後資本週期",
    "holding_period": {
      "horizon": "中期 2-5 年（長期持有信心低，護城河趨勢↓且 Max DD 🔴）",
      "driver": "FY27／FY28 AI 營收指引兌現度＋Google 份額路徑＋半導體分部營業利益率",
      "signal_vs_noise": "訊號＝年度 AI 營收兌現度、Google 世代設計權歸屬、分部營業利益率趨勢；噪音＝單季指引與街頭差 <1%、單季合併毛利率 mix 波動"
    },
    "H": [
      {
        "id": "H1",
        "text": "客製 AI ASIC 設計領導地位維持：六大客戶群持續放量，客戶分散化抵銷 Google 單一客戶份額稀釋",
        "2y": "FY27 AI 半導體營收落在 $115B 指引 ±10%；OpenAI 2027 出貨 ≥1.3GW 合約量",
        "5y": "FY28 AI 營收 ≥$185B（指引 $230B 打八折）；Anthropic／OpenAI／Meta 合計占 AI 營收 ≥40%",
        "10y": "客製 ASIC 對 merchant GPU 出貨份額維持 30% 以上（產業層級），Broadcom 設計夥伴份額 ≥50%",
        "threshold": "TTM AI 營收落後指引路徑逾 10% 連 2 季→削弱；連 3 季逾 10%→反轉",
        "source": "公司財報／法說（每季）＋Counterpoint／TrendForce 份額研究（每年）",
        "drift_rule": "2Y 假設連 2 季 TTM 偏離 ≥5% 削弱、連 3 季 ≥10% 反轉；5Y 假設連 4 季 ≥5% 削弱"
      },
      {
        "id": "H2",
        "text": "VMware 訂閱制轉換完成後，基礎設施軟體以低雙位數成長提供跨週期現金流",
        "2y": "基礎設施軟體營收 YoY ≥10%（Q3 FY26 $8.75B、+29%）；VCF ARR 年增不跌破 12%",
        "5y": "軟體占總營收 20-30%、分部營業利益率維持 70% 以上；VCF 成為企業私有 AI 推論控制平面",
        "10y": "軟體現金流足以覆蓋全部股息＋淨回購，成為半導體循環的緩衝",
        "threshold": "ARR 年增連 2 季 <10%→削弱；EU／美反壟斷裁定強制改授權模式→反轉",
        "source": "公司財報分部數字（每季）＋歐盟／DOJ 公告",
        "drift_rule": "2Y 假設連 2 季偏離 ≥5% 削弱；反壟斷裁定屬離散事件，命中即重審 H2"
      },
      {
        "id": "H3",
        "text": "市場以複利股而非循環股給倍數：FY+2 本益比維持 15-25x 區間，PEG 不系統性偏離 1 以下",
        "2y": "FY+2 本益比不連 4 季 <14x 且無基本面惡化；共識 FY28 EPS 不連續下修",
        "5y": "5 年後估值倍數 normalize 至 18-22x 仍反映護城河與成長持續期",
        "10y": "—",
        "threshold": "FY+2 本益比連 4 季 <14x 且非 EPS 上修驅動→削弱（市場已切換循環股框架）",
        "source": "本站共識快照 data/eps-estimates（每兩週）",
        "drift_rule": "連 4 季 FY+2 本益比偏離 15-25x 區間逾 10%→削弱"
      }
    ],
    "R": [
      {
        "id": "R1",
        "text": "Google 端份額稀釋快於預期：Google 刻意建四夥伴供應鏈（Broadcom 訓練 Sunfish、MediaTek 推論 Zebrafish 成本低 20-30%、Marvell 2026-07-29 簽約、Intel 處理器），MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場、Zebrafish Q4 2026 量產。反向證據：Broadcom 與 Google 多世代 TPU 長約、Counterpoint 估 2027 仍持 60% 設計夥伴份額",
        "h_ref": "H1",
        "clock": "🔥",
        "threshold": "Google 份額較 95→80→65 路徑低逾 10pp，或 2027 年度 <75%；Broadcom 未取得 TPU v9／v10 訓練晶片設計權",
        "evidence_refs": [
          "competitive_share_entrants#2",
          "competitive_share_entrants#3",
          "customer_second_source#0",
          "customer_second_source#1",
          "customer_second_source#2",
          "substitute_technology#1"
        ]
      },
      {
        "id": "R2",
        "text": "AI 客戶信用與資本週期：OpenAI 2026-05 無法關閉約 $18B 融資、Broadcom 被報導只願出資第一階段並放寬對等出資要求；XPV 平台（Apollo／Blackstone）首批 $35B、20GW 全量名目上看 $370B；四大雲端 AI 資本支出若 2028 進入消化期，backlog 兌現度不如指引",
        "h_ref": "H1／H3",
        "clock": "🔥",
        "threshold": "OpenAI／Anthropic 實際出貨 GW 低於公司自身指引逾 20%；XPV 信用展望連 2 季負向",
        "evidence_refs": [
          "customer_concentration_credit#3",
          "customer_concentration_credit#4",
          "customer_concentration_credit#0",
          "customer_concentration_credit#2"
        ]
      },
      {
        "id": "R3",
        "text": "VMware 監管與通路：歐盟 2026-02 正式反壟斷調查、Broadcom 敗訴文件請求案、美國另開授權調查；2026-01 終止 400 餘家 VCSP 夥伴合約引發被迫遷移；中國以國安為由要求移除 VMware 並禁用 Broadcom 資安方案",
        "h_ref": "H2",
        "clock": "🐢",
        "threshold": "歐盟發異議書或裁定強制改授權模式；ARR 年增連 2 季 <10%",
        "evidence_refs": [
          "regulatory_antitrust#0",
          "regulatory_antitrust#1",
          "regulatory_antitrust#2",
          "channel_business_model_shift#1",
          "regulatory_antitrust#4",
          "regulatory_antitrust#5"
        ]
      }
    ],
    "single_thing": {
      "description": "Google 公告下一代主力訓練 TPU（v9 Triggerfish 或 v10）主設計權授予 MediaTek 或其他夥伴，Broadcom 失去 Google 訓練晶片主設計權",
      "why_fatal": "Google 是 AI 營收最大單一來源且訓練晶片是最高價值環節；失去主設計權＝護城河等級由 A 直接重審至 B 以下，且觸發護城河趨勢↓＋等級 ≤B 的強制迴避",
      "if_happens": "清倉級：不等財報，先減至 0 並重跑 DD；市場會把估值框架從複利股切到循環代工股（12-15x）",
      "how_monitor": "Google 法說／TSMC 2nm 投片報導／TrendForce、Counterpoint 設計夥伴研究（每季），公司法說對「多世代協議」措辭變化",
      "probability": "12-24 個月內 20-25%（多世代長約至 2031 為反向錨；但 Google 已明示要每個環節都有合格替代者）"
    }
  },
  "industry": {
    "clock_phase": "II",
    "sd_verdict_source": "產業物理供需＝shortage（ID：AI Accelerator Demand，as-of 2026-09-05；機械選出的 primary 為 Hyperscaler 雲端三巨頭 as-of 2026-05-05 亦為 shortage／Phase II，惟前者較貼題，建議覆核 primary）。Phase II 已經自身位置閘交叉驗證：AI 訂單 backlog >$73B（來源：摘要）、供給能見度延至 2028、CoWoS 缺口 20%→10%（供給正在追上，屬擴張後段而非過熱頂部）",
    "bargaining": {
      "up": "對上游弱：先進製程與 CoWoS 近乎單一來源 TSMC（先進節點 >90%），NVIDIA 已預訂 2026-27 過半 CoWoS-L；Broadcom 稱 26-28 年晶圓／HBM／基板產能已鎖定（來源：摘要），但雷射與 PCB 缺口蔓延",
      "down": "對下游中等偏弱：前五大終端客戶占營收 45%（10-Q，2026-05-03；前一年 40%）、經銷商單一客戶 42%；Google 明示以多夥伴取得議價槓桿；反向：多年期承諾（Google 至 2031、OpenAI 10GW 至 2029、Meta 3GW 至 2028）",
      "geo": "生產 100% 依賴台灣先進節點與封裝；美國 Section 232 對高階半導體課 25% 關稅（產品分類決定是否涵蓋）；中國禁 Broadcom 資安方案、要求移除 VMware；美國禁中國光收發器可能壓 DSP 需求"
    },
    "profit_pool_dir": "流入：自研 ASIC 把原屬 merchant GPU 的利潤池分一塊給設計夥伴（ID 供給側：AVGO 客製加速器 +140% YoY、ASIC 出貨 2024-27 三倍）；但 Google 內部以多夥伴壓縮設計夥伴分潤，池在放大、單一夥伴份額在縮",
    "tam_table": [
      {
        "segment": "客製 AI 加速器（XPU）",
        "tam_now": "2027E 約 $80B（MediaTek 引用之客製 AI 晶片市場估計）",
        "tam_5y": "證據包未涵蓋（公司 SAM 口徑不在本輪證據包）",
        "sam": "六客戶多年期承諾：OpenAI 10GW、Anthropic 3.5GW＋5GW、Meta 3GW、Google 多世代",
        "penetration": "設計夥伴份額約 60%（Counterpoint，2027E）",
        "cagr": "FY26 $58B→FY27 $115B→FY28 $230B（公司指引，含網通）",
        "position": "設計＋IP 平台（SerDes／CoWoS 整合），客戶擁有架構",
        "pool_shift": "5 年前 ~0→現為半導體分部主體；流向設計夥伴與雲端自身",
        "ceiling": "天花板＝雲端資本支出 ROI 兌現；被替代路徑＝客戶自有工具鏈（COT）與 MediaTek 低成本設計"
      },
      {
        "segment": "AI 網通（Tomahawk 6／DSP／光學）",
        "tam_now": "Q1 FY26 約占 AI 營收三分之一、YoY +60%（來源：摘要）",
        "tam_5y": "證據包未涵蓋",
        "sam": "AI 交換器 backlog >$10B（來源：摘要）",
        "penetration": "自稱 CPO／DSP 事實標準（來源：摘要，未第三方驗證）",
        "cagr": "隨 XPU 集群同步；矽光子「尚未到位」",
        "position": "Ethernet 陣營標準制定者",
        "pool_shift": "自 InfiniBand 向 Ethernet 流入",
        "ceiling": "NVIDIA Spectrum-X 與客戶自研交換晶片"
      },
      {
        "segment": "基礎設施軟體（VMware VCF）",
        "tam_now": "Q3 FY26 $8.75B（+29% YoY）",
        "tam_5y": "證據包未涵蓋",
        "sam": "前 10,000 大客戶逾 90% 已轉訂閱制 VCF",
        "penetration": "已轉換帳戶為主，成長轉為 ARR 擴張",
        "cagr": "管理層：低雙位數；VCF ARR +17%（2026-06 報導口徑）",
        "position": "私有雲控制平面，訂閱制每核心計價",
        "pool_shift": "自通路夥伴與舊授權模式流向 Broadcom 直銷",
        "ceiling": "歐盟／美國反壟斷、客戶遷移至 Nutanix／公有雲"
      },
      {
        "segment": "非 AI 半導體（寬頻／無線／儲存／企業網通）",
        "tam_now": "Q1 FY26 $4.1B 季度、YoY 持平",
        "tam_5y": "證據包未涵蓋",
        "sam": "Q2 FY26 訂單 >$6B、管理層稱循環復甦中（來源：摘要）",
        "penetration": "成熟寡占",
        "cagr": "低個位數，循環性",
        "position": "多品類寡占者",
        "pool_shift": "持平",
        "ceiling": "無線客戶集中（Apple）與消費電子週期"
      }
    ]
  },
  "moat": {
    "execution": 9.0,
    "pricing": 8.0,
    "combined": 8.5,
    "grade": "A",
    "score": 8.5,
    "trend": "↓",
    "trend_evidence": "12 個月內 sourced：Google 2026-08-20 報導刻意組四夥伴供應鏈、MediaTek Zebrafish Q4 2026 量產且成本低 20-30%、Marvell 2026-07-29 與 Google 簽約。執行面擴大（六客戶、供給鎖定至 2028、AI 營收 +221%），定價面縮減（最大客戶明示要每環節有替代者）；取對論點更關鍵的定價／份額維度→↓。閘 A：最大客戶份額路徑 95→80→65 下滑（sourced）→不得標↑。三分解：方向未受損（設計夥伴份額仍 ~60%）、速度放緩（Google 新增量分給對手）、失守範圍＝Google 推論晶片。攻擊者資本量級：MediaTek 資料中心營收 2026E >$2B，約為 AVGO AI 營收 3%，屬點對點而非生態級；但 Google 本身資本無上限。記帳紀律：負面證據只記在趨勢，等級維持 A 不重複扣",
    "spread_table": [
      {
        "metric": "營業利益率（GAAP TTM）",
        "self": 44.06,
        "peer": "MRVL 16.41（最直接客製 ASIC 對手）",
        "spread_pp": 27.65,
        "trend": "MRVL 三年趨勢證據包未涵蓋；AVGO 半導體分部營業利益率 +440bp YoY→視為擴大",
        "note": "NVDA 64.02 為 merchant GPU 不同層級，不作等級門檻對照"
      },
      {
        "metric": "FCF 利潤率（TTM）",
        "self": 43.41,
        "peer": "MRVL 19.06；AMD 20.34；QCOM 23.64",
        "spread_pp": 24.35,
        "trend": "擴大（AVGO Q3 FCF 占營收 46.2%，QoQ 持平於高檔）",
        "note": "來源 peer_financials"
      },
      {
        "metric": "毛利率（GAAP TTM）",
        "self": 68.28,
        "peer": "NVDA 74.15；MRVL 51.5；AMD 53.2",
        "spread_pp": 16.78,
        "trend": "合併毛利率因 XPU mix 下滑（管理層：金額升、比率降，來源：摘要）；同業擴張而本標的下滑→閘二對照：屬 mix 非結構，記管理層承諾列入監測",
        "note": "R&D 強度 15.89% 低於 MRVL 25.46／AMD 22.74，反映規模攤薄"
      }
    ],
    "threats": [
      {
        "level": "🔴 生態攻擊",
        "text": "Google 四夥伴供應鏈：MediaTek 推論 Zebrafish（Q4 2026 量產、成本低 20-30%）、Marvell 商業協議（2026-07-29）、Intel 處理器；Google 藉此取得定價與產能槓桿",
        "p": "60-70%（份額稀釋已在發生）",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "customer_second_source#0",
          "customer_second_source#1"
        ]
      },
      {
        "level": "🔴 生態攻擊",
        "text": "MediaTek 目標 2027 搶 15-20% 客製 AI 晶片市場（$80B 估計），2026 資料中心營收 >$2B",
        "p": "50%",
        "evidence_refs": [
          "competitive_share_entrants#2"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "六大客戶各自投資內部設計能力，關係「深而黏但非永久」；風險因子明列客戶可能改採自有工具鏈（COT）或租賃模式",
        "p": "3-5 年 30%",
        "evidence_refs": [
          "customer_second_source#2",
          "customer_concentration_credit#2",
          "substitute_technology#1"
        ]
      },
      {
        "level": "🟡 點對點",
        "text": "VMware 資安事件（Aria Operations 零日遭中國國家背景組織利用；Clop 經 Oracle EBS 零日入侵 Broadcom 內部）削弱軟體信任",
        "p": "20%（信任型流失）",
        "evidence_refs": [
          "major_events#1",
          "major_events#2",
          "product_recall_warning#0",
          "product_recall_warning#1"
        ]
      }
    ],
    "competitors": [
      {
        "name": "MRVL（Marvell）",
        "rev_growth": "證據包未涵蓋",
        "gm": 51.5,
        "om": 16.41,
        "rd_intensity": 25.46,
        "fcf_margin": 19.06,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "Trainium base die ~55-60% 份額（ID 供給側），2026-07-29 取得 Google 客製協議（推論／周邊）；營業利益率不到 AVGO 四成，R&D 強度高＝以投入換份額，經濟體質弱但攻擊意願強"
      },
      {
        "name": "NVDA（NVIDIA）",
        "rev_growth": "證據包未涵蓋",
        "gm": 74.15,
        "om": 64.02,
        "rd_intensity": 8.22,
        "fcf_margin": 46.97,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "merchant GPU 主供，預訂 2026-27 過半 CoWoS-L；與 AVGO 爭封裝產能而非設計案；Rubin 若 TCO 大幅領先會削弱自研 ASIC 經濟性（ID 可證偽條件）"
      },
      {
        "name": "AMD",
        "rev_growth": "證據包未涵蓋",
        "gm": 53.2,
        "om": 15.71,
        "rd_intensity": 22.74,
        "fcf_margin": 20.34,
        "net_cash": "證據包未涵蓋",
        "strategy_note": "雙來源 GPU；市場傳聞洽談 Google v10，屬未證傳聞"
      },
      {
        "name": "MediaTek",
        "rev_growth": "證據包未涵蓋",
        "gm": "證據包未涵蓋",
        "om": "證據包未涵蓋",
        "rd_intensity": "證據包未涵蓋",
        "fcf_margin": "證據包未涵蓋",
        "net_cash": "證據包未涵蓋",
        "strategy_note": "Google 推論 TPU Zebrafish Q4 2026 量產、成本低 20-30%；2027 目標 15-20% 份額。財務數字不在 peer_financials，體質判斷留待補軸"
      }
    ],
    "roic_durability": {
      "quadrant": "高利益率×低周轉（VMware 商譽與無形資產墊高投入資本；剔除收購無形資產後屬高利益率×高周轉）",
      "checkpoints": [
        {
          "name": "需求基礎值",
          "light": "🟢",
          "evidence": "需要型：雲端算力受限（ID：Azure $80B backlog 受電力限、GCP RPO >$70B）；Broadcom AI backlog >$73B、能見度至 2028（來源：摘要）。惟急迫≠持久：需求是 ROI 兌現的函數",
          "proxy": "多年期承諾 GW 數（OpenAI 10GW／Anthropic 8.5GW／Meta 3GW）"
        },
        {
          "name": "決策層級",
          "light": "🟡",
          "evidence": "客戶在架構層決策（自有架構＋Broadcom 設計平台），切換需 18-24 個月 tape-out 週期；但 Google 已示範同架構下多夥伴分單，替代性在「世代」層級而非「產品」層級",
          "proxy": "各客戶世代設計權歸屬（v8 Sunfish／Zebrafish 分拆）"
        },
        {
          "name": "價值鏈分配",
          "light": "🟡",
          "evidence": "利益留在 Broadcom（非 GAAP 營業利益率 67.9%、半導體分部 +440bp YoY）；但買方集中（前五大 45%、單一經銷商 42%）且客戶自建能力上升，Google 明示以替代者取得議價槓桿",
          "proxy": "半導體分部營業利益率、前五大集中度"
        },
        {
          "name": "社會容忍度",
          "light": "🟡",
          "evidence": "半導體端低敏感；軟體端高敏感：VMware 漲價已引來歐盟正式調查、美國授權調查、CISPE 投訴與中國移除令；經濟上限與政治上限已相交",
          "proxy": "歐盟程序階段（調查→異議書→裁定）"
        }
      ],
      "roiic": 80,
      "reinvest_rate": 6,
      "endo_ceiling": 5.0,
      "formula_note": "ROIIC(3Y) 代理≈ΔNOPAT÷Δ投入資本：非 GAAP 營業利益年化自 FY23 約 $22B 升至 Q3 FY26 年化 $80B（Δ≈$58B），Δ投入資本以 VMware $69B＋有機約 $3B 計≈$72B→約 80%。再投資率＝(資本支出−折舊攤銷＋ΔWC＋收購淨額)÷NOPAT：年化資本支出約 $2.1B 對 NOPAT 約 $65B≈3%，加營運資金約 6%（收購攤銷不計）。內生天花板≈80%×6%≈5%。Base EPS CAGR 15.4% 超出天花板⚠→Bear 機率下限 30%；缺口歸因＝客戶承擔產能資本的新 S 曲線（XPU backlog sourced）＋營業槓桿，非 re-rate"
    }
  },
  "growth": {
    "runway_years": "5-7 年（AI 營收 FY26 $58B→FY28 $230B 指引後，2029 起增速取決於雲端資本支出第二輪；非 AI 與軟體提供低雙位數底盤）",
    "runway_post_y5": "🟡",
    "seven_questions": [
      "①結構性或週期反彈：結構性（雲端自研 ASIC 滲透 25-30% 且升）疊加資本週期（capex $380B+ ROI 未證）——兩者同時為真",
      "②資本投入：極低，資本支出占營收 <2%，產能資本由 TSMC 與客戶承擔",
      "③增量 ROIC >資金成本：是，代理 ROIIC 約 80%",
      "④成長變現金流或被吃掉：變現金流，Q3 FCF $13.7B 占營收 46%；但 XPV 表外平台把部分資本承諾移到平台",
      "⑤競爭者是否被吸引：是——MediaTek、Marvell、Intel 已進 Google 供應鏈，這是最弱的一題",
      "⑥股價反映多少期待：FY27 本益比 18.5x、PEG 0.31，反映的是「成長會在 2028 後急降」而非「指引兌現」",
      "⑦成長率下修估值撐得住嗎：成長降至 15% 給 20x 仍有正報酬；降至 5% 給 12x 則 −50%"
    ],
    "segments": [
      {
        "name": "AI 半導體（XPU＋網通）",
        "fy0": "FY26E $58B（指引，+186%）",
        "driver": "量：GW 部署（OpenAI 1.3GW 2027、Anthropic 3GW+5GW、Meta 3GW）；價：系統級含量提升",
        "fy1e": "FY27 $115B（指引；本檔 Base 取 100%）",
        "fy2e": "FY28 $230B 指引；本檔 Base 取 $185B（八折）",
        "fy3e": "FY29 +15-20%",
        "om_path": "半導體分部 61%→58-60%（mix）",
        "eps_contrib_pct": "約 75%"
      },
      {
        "name": "基礎設施軟體",
        "fy0": "Q3 FY26 $8.75B（+29%）",
        "driver": "訂閱制轉換完成後 ARR 擴張（VCF ARR +17%，2026-06 口徑）",
        "fy1e": "低雙位數",
        "fy2e": "低雙位數",
        "fy3e": "高個位數至低雙位數",
        "om_path": "70%+ 維持",
        "eps_contrib_pct": "約 20%"
      },
      {
        "name": "非 AI 半導體",
        "fy0": "Q1 FY26 $4.1B 季度、持平",
        "driver": "循環復甦（Q2 訂單 >$6B，來源：摘要）",
        "fy1e": "低個位數至中個位數",
        "fy2e": "低個位數",
        "fy3e": "低個位數",
        "om_path": "持平",
        "eps_contrib_pct": "約 5%"
      }
    ],
    "decay_signals": [
      "合併毛利率連季 YoY 下滑（XPU／系統 mix，管理層稱非結構性，來源：摘要）——亮燈但歸因 mix",
      "核心客戶份額縮減（Google 份額路徑 95→80→65，MediaTek／Marvell 進場）——亮燈",
      "SBC／營收 6.8%（Q3 FY26）>5% 但季比下降（9.4%→6.8%）——不亮燈",
      "其餘七項未亮燈（FCF／NI、TAM、產業倍數、維持性資本支出）"
    ],
    "trap_rating": "🟡（2 訊號：合併毛利率下滑屬 mix、Google 份額稀釋屬真實侵蝕）"
  },
  "quality": {
    "three_year": [
      {
        "metric": "FCF 利潤率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "43.41（TTM 至 2026-04）／Q3 FY26 46.2",
        "peer_median": "MRVL 19.06／AMD 20.34／QCOM 23.64／NVDA 46.97",
        "assessment": "頂尖，僅次 NVDA"
      },
      {
        "metric": "營業利益率",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "GAAP 44.06（TTM）／Q3 FY26 GAAP 53.9、非 GAAP 67.9",
        "peer_median": "MRVL 16.41／AMD 15.71／QCOM 23.28／NVDA 64.02",
        "assessment": "Q3 非 GAAP 營業利益率 QoQ +60bp；營收 YoY +86% 對營業利益 YoY 更高＝營業槓桿為正（發散 <0）"
      },
      {
        "metric": "SBC／營收",
        "fy23": "證據包未涵蓋",
        "fy24": "證據包未涵蓋",
        "fy25_ttm": "Q3 FY26 6.8%（Q2 9.4%）",
        "peer_median": "證據包未涵蓋",
        "assessment": "金額持平 $2.0B／季，比率因營收放大而降"
      }
    ],
    "dupont": [
      {
        "component": "NOPAT 利潤率",
        "value": "非 GAAP 營業利益率 67.9%（Q3 FY26）；GAAP 53.9%",
        "note": "GAAP 與非 GAAP 差距主要為收購無形資產攤銷與 SBC"
      },
      {
        "component": "投入資本周轉率",
        "value": "證據包未涵蓋（投入資本明細不在本輪數字包）",
        "note": "VMware $69B 商譽／無形資產使帳面周轉率低；剔除後為高周轉輕資產"
      }
    ],
    "ccc": [
      {
        "metric": "DSO／DIO／DPO／CCC 三年逐年",
        "value": "證據包未涵蓋",
        "note": "10-Q 提及 AI 與無線客戶大單造成季度營收波動；營運資金結構須回補軸"
      }
    ],
    "buyback": {
      "authorization": "剩餘 $7.5B（至 2026 年底）＋2026-03 加碼 $10B（來源：摘要）",
      "q1_capital_return": "Q1 FY26 回饋股東 $10.9B（股息＋回購，來源：摘要）",
      "buyback_to_fcf": "Q1 回饋 $10.9B 對 Q1 FCF 證據包未涵蓋；以 Q3 FCF $13.7B 為尺，回饋比率約 60-80% 區間，未觸 >80% 警示",
      "avg_price_vs_now": "證據包未涵蓋",
      "eps_cagr_ex_buyback": "淨回購約 0.3%／年，對 EPS CAGR 貢獻 <1pp，剔除後差距遠低於 5pp 警示"
    },
    "lumpiness": {
      "fcf_5y": "證據包未涵蓋（僅有 Q2 $10.26B、Q3 $13.67B）",
      "maint_capex_method": "以季度資本支出 $532M 全數視為維持性（保守法）",
      "owner_earnings": "Q3 營運現金流 $14.2B − $0.53B ≈ $13.7B",
      "verdict": "🟢 正常（資本支出占 FCF <4%）"
    }
  },
  "governance": {
    "capalloc_grade": "A",
    "scorecard": [
      {
        "item": "M&A 已實現 ROIIC（VMware $69B，2023-11）",
        "value": "基礎設施軟體 Q3 FY26 營收 $8.75B、分部營業利益率約 70%+→年化營業利益約 $25B÷$69B≈35%",
        "pass": true
      },
      {
        "item": "回購買入收益率",
        "value": "回購均價證據包未涵蓋；以現價 FY27 盈餘殖利率 5.4%（1÷18.5）近似 ≥ 10Y 殖利率＋2%",
        "pass": true
      },
      {
        "item": "SBC 淨稀釋率",
        "value": "SBC 年化約 $8B 對市值約 $1.68T≈0.5%／年，加 $17.5B 回購額度後為淨減少",
        "pass": true
      }
    ],
    "capital_returns": [
      {
        "type": "股息",
        "detail": "季配 $0.65（FY26 +10%，來源：摘要）；殖利率約 0.7%"
      },
      {
        "type": "回購",
        "detail": "剩餘 $7.5B＋新增 $10B 至 2026 年底（來源：摘要）"
      },
      {
        "type": "表外",
        "detail": "XPV 平台首批 $35B（Apollo）、目標 20GW 至 2028（來源：摘要）；自陳曝險 $29B、BofA 模型 $42B、全量名目 $370B（前份報告口徑）"
      }
    ],
    "sbc": {
      "pct_revenue": 6.8,
      "pct_gaap_oi": 12.7,
      "trend": "Q2 9.4%→Q3 6.8%（金額持平 $2.0-2.1B）",
      "note": "CFO 交接：Kirsten Spears 2026-06-12 退休、Amie Thuener 接任（來源：摘要）→ 2026-12-09 為新 CFO 首個完整季度複審點；內部人交易近 12 個月：證據包未涵蓋"
    }
  },
  "valuation": {
    "tier": "Turnkey ASIC／IP 平台＋基礎設施軟體混合；同 tier 直接 peer＝MRVL，NVDA 為 merchant GPU 不同 tier，⚠ 無 ideal peer group，溢折價獨立推導",
    "peers": [
      {
        "name": "MRVL",
        "fwd_pe": "證據包未涵蓋",
        "note": "營業利益率 16.41 vs AVGO 44.06，倍數不可比"
      },
      {
        "name": "NVDA",
        "fwd_pe": "證據包未涵蓋",
        "note": "不同 tier"
      },
      {
        "name": "AMD",
        "fwd_pe": "證據包未涵蓋",
        "note": "—"
      },
      {
        "name": "QCOM",
        "fwd_pe": "證據包未涵蓋",
        "note": "—"
      }
    ],
    "fwd_pe": 30.77,
    "peg": 0.51,
    "percentile_5y": 24.4,
    "val_light": "🟢",
    "val_light_derivation": "五年分位：trailing 本益比 45.48 對 4 個年度樣本點高 135.24／低 16.57→(45.48−16.57)÷(135.24−16.57)＝24.4%（樣本僅 4 點，標「年度樣本」）；短窗 fwd 本益比 30.77 位於 2026-05 起 9 份快照最低（0 分位，非五年）。PEG：FY26 基準 30.77÷60.6%（FY26→FY28 共識 2 年 CAGR）＝0.51；FY27 基準 18.51÷60.6%＝0.31。分位 <30% 且 PEG <1.0→兩尺皆 🟢，取較嚴仍 🟢。分母爭議：FY27 共識 19.33 受 $73B backlog 覆蓋，非本章爭點；FY28 起才是",
    "targets": {
      "short_1y": {
        "eps": 19.33,
        "pe": 22,
        "price": 425,
        "upside_pct": 18.8,
        "basis": "FY27 共識 EPS × 合理 22x（護城河 A 但趨勢↓折價）"
      },
      "mid_2y": {
        "eps": 26.0,
        "pe": 22,
        "price": 572,
        "upside_pct": 59.8,
        "basis": "本檔 Base FY28 EPS 26.0（指引八折）× 22x"
      },
      "five_y": {
        "eps": 39.5,
        "pe": 20,
        "price": 790,
        "upside_pct": 120.7,
        "basis": "Base 情境 FY31 EPS × 長期 20x"
      },
      "bear_anchor": {
        "eps": 17.4,
        "pe": 15,
        "price": 261,
        "downside_pct": -27.0,
        "basis": "Bear EPS＝FY27 共識×0.9；Bear 本益比＝成長降至 10% 情境 15x；下行 27% >15% 正常可用"
      },
      "sell_side": "57 位分析師目標價均值 $520（過去 3 個月上修 9.3%，買進評等 84%）；財報後 BMO $575、Cantor $600、Raymond James $475。現價低於均值 31%→支持本裁決；全距 max／min 證據包未涵蓋"
    },
    "upside_short_pct": 18.8,
    "upside_mid_pct": 59.8
  },
  "trap_analysis": {
    "pattern": "最可能的陷阱模式＝「週期頂部的低 PEG」：AI 資本週期在 2028 見頂，FY28 EPS 30 成為峰值盈餘，低倍數反映的是市場已把它當循環股",
    "evidence_against": "Q3 FY26 營收 +86%、AI 營收 +221%、FCF $13.7B（46%）、非 GAAP 營業利益率 67.9% 續升；backlog >$73B 覆蓋 18 個月；共識 FY28 EPS 近一週上修 13.5% 至 30.0、90 天 +17%——盈餘與現金同步、且共識仍在追指引而非下修",
    "evidence_for": "前五大客戶 45%、單一經銷商 42%；Google 刻意分單、MediaTek Q4 量產；OpenAI 融資 $18B 未關閉、XPV 名目 $370B；合併毛利率因 mix 下滑——這些都是「峰值盈餘品質」的典型前兆",
    "bear_case": "空頭最強一擊（18 個月 −30%+）：2027 中雲端下修 2028 資本支出＋Google 公布 v9 訓練晶片交 MediaTek→FY28 共識自 30 砍至 22、倍數自 18.5x 壓至 12x→股價 $260（−27%）至 $230（−36%）。監測：Google 世代設計權公告、四大雲端 capex 指引、半導體分部營業利益率",
    "monitor": [
      "共識 FY28 EPS 方向（連 2 次下修＝陷阱正在發生）",
      "半導體分部營業利益率跌破 55% 連 2 季",
      "Google 份額路徑與 v9／v10 設計權",
      "XPV 平台信用展望與 OpenAI 融資關閉進度"
    ],
    "verdict": "🟢",
    "label": "🟢 非陷阱（2 個衰退訊號皆有 sourced 反駁：mix 與份額稀釋被絕對金額 +221% 覆蓋；觀察期指標已列）"
  },
  "appendix_a": {
    "signal": "A+",
    "moat_score": 8.5,
    "growth_durability": 8.0,
    "quality_score": 8.3,
    "ai_risk": "🟢",
    "long_term_confidence": "低",
    "val": "🟢",
    "ma": "✅",
    "fpe_fy2": 18.51,
    "pct_5y": 24.4,
    "peg_fy2": 0.31,
    "upside_short_pct": 18.8,
    "upside_mid_pct": 59.8,
    "stress": {
      "pass": 2,
      "total": 2
    },
    "verdict": "A+"
  },
  "scenario_ref": "/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/scenario.json",
  "eps_meta": {
    "base_eps_path": {
      "FY26": 11.63,
      "FY27": 19.33,
      "FY28": 30.0
    },
    "fy_end_month": 11,
    "eps_basis": "non-gaap-usd"
  },
  "catalysts": [
    {
      "date": "2026-12-09",
      "type": "guidance",
      "event": "Q4 FY26 財報＋FY27 展望更新（新 CFO 首個完整季度）",
      "impact": "高",
      "watch": "Q4 AI 營收 ≥$21.7B 指引兌現；FY27 $115B 是否維持或上修；半導體分部營業利益率"
    },
    {
      "date": "2026-12-31",
      "date_precision": "quarter",
      "type": "product",
      "event": "MediaTek Google 推論 TPU Zebrafish 量產",
      "impact": "高",
      "watch": "量產規模與 Google 推論採購分配；Broadcom 對 Google 出貨是否同步下修"
    },
    {
      "date": "2027-03-31",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "歐盟 VMware 反壟斷調查程序進展（異議書與否）",
      "impact": "中",
      "watch": "若發異議書→軟體 ARR 與毛利率下修風險；程序階梯對應減碼"
    },
    {
      "date": "2027-06-30",
      "date_precision": "quarter",
      "type": "product",
      "event": "OpenAI Jalapeño 首代 XPU 2027 出貨 1.3GW 合約量兌現",
      "impact": "高",
      "watch": "融資關閉進度、Microsoft 承購結構是否落地"
    },
    {
      "date": "2027-06-30",
      "date_precision": "quarter",
      "type": "capacity",
      "event": "TSMC CoWoS 供需缺口 2026 底縮至 10% 後 2027 續改善",
      "impact": "中",
      "watch": "缺口收斂＝供給可逆性上升，Bear 機率不得下調"
    },
    {
      "date": "2027-12-31",
      "date_precision": "quarter",
      "type": "product",
      "event": "Google TPU v8 Sunfish（2nm）投產、v9 Triggerfish 設計權歸屬明朗",
      "impact": "高",
      "watch": "Broadcom 是否同步取得 v9／v10 訓練晶片設計權；命中即為清倉級觸發"
    },
    {
      "date": "2026-12-31",
      "date_precision": "quarter",
      "type": "regulatory",
      "event": "Section 232 高階半導體 25% 關稅產品分類細則",
      "impact": "低",
      "watch": "Broadcom XPU 是否被列入涵蓋範圍"
    },
    {
      "date": "2027-12-31",
      "date_precision": "quarter",
      "type": "other",
      "event": "Anthropic IPO 與 XPV 平台第二批融資",
      "impact": "中",
      "watch": "改善或惡化表外平台信用結構"
    }
  ],
  "decision_inputs": {
    "signal": "A+",
    "trap": "🟢",
    "val": "🟢",
    "ma": "✅",
    "runway_post_y5": "🟡",
    "moat_trend": "↓",
    "moat": "A",
    "capalloc_grade": "A",
    "archetype": "品質複利成長",
    "cycle_position": null,
    "cycle_verdict": null,
    "asym_ratio": 6.76,
    "irr_base_pct": 18.2,
    "ev5y_pct": 134.1,
    "price_at_dd": 357.89,
    "thesis_irreconcilable": false,
    "valuation_dependent": false,
    "market_wrong_reason_given": true,
    "week26_return_pct": 8.7,
    "momentum_overheated": false,
    "cycle_gates_pass": null,
    "consensus_rev_3m_pct": 1.42,
    "val_denominator_disputed": false,
    "qc49_inherit_prior": false,
    "prior_verdict": "進場",
    "prior_role": "衛星",
    "held_now": null
  },
  "decision_out": {
    "verdict": "進場",
    "role": "衛星",
    "row_hit": "10",
    "pacing": [],
    "holding_cap": null,
    "requires_critic": [
      "QC-41 產業態勢：裁決強方向（進場）＋護城河趨勢方向性（↓）＋B2B 客戶集中型（前五大 45%）——三條件皆命中，必跑；重點覆核 Google 分單是否已從「推論」蔓延到「訓練」世代",
      "QC-41 附帶：本輪證據包未含最新一季（Q3 FY26）逐字稿與週線均線資料，均線狀態沿用前份 2026-09-03 量測，請閘覆核"
    ],
    "audit_rows": [
      {
        "row": "1",
        "condition": "基本面評級 signal = X → 迴避",
        "hit": false,
        "basis": "signal='A+'"
      },
      {
        "row": "2",
        "condition": "§11 強制裁決：thesis 不可調和不成立 → 迴避",
        "hit": false,
        "basis": "thesis_irreconcilable=False"
      },
      {
        "row": "3",
        "condition": "moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避",
        "hit": false,
        "basis": "moat_trend='↓', moat='A'"
      },
      {
        "row": "4",
        "condition": "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）",
        "hit": false,
        "basis": "ma='✅'"
      },
      {
        "row": "5",
        "condition": "動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）",
        "hit": false,
        "basis": "momentum_overheated=False"
      },
      {
        "row": "6",
        "condition": "基本面評級 signal = C → ≥ 觀望",
        "hit": false,
        "basis": "signal='A+'"
      },
      {
        "row": "7",
        "condition": "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）",
        "hit": false,
        "basis": "runway_post_y5='🟡'"
      },
      {
        "row": "7a",
        "condition": "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
        "hit": false,
        "basis": "valuation_dependent=False, market_wrong_reason_given=True"
      },
      {
        "row": "7b",
        "condition": "dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）",
        "hit": false,
        "basis": "capalloc_grade='A'"
      },
      {
        "row": "8a",
        "condition": "無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）",
        "hit": false,
        "basis": "signal='A+', runway='🟡', val='🟢', moat_trend='↓', week26=8.7, valuation_dependent=False"
      },
      {
        "row": "8b",
        "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        "hit": false,
        "basis": "archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↓', cycle_gates_pass=None"
      },
      {
        "row": "11.4b-denom",
        "condition": "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
        "hit": false,
        "basis": "val_denominator_disputed=False"
      },
      {
        "row": "8",
        "condition": "無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）",
        "hit": false,
        "basis": "signal='A+', val='🟢'"
      },
      {
        "row": "9",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
        "hit": false,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "9b",
        "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
        "hit": false,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "10",
        "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
        "hit": true,
        "basis": "signal='A+', val='🟢', ma='✅'"
      },
      {
        "row": "10-verdict",
        "condition": "命中 row10 → 進場",
        "hit": true,
        "basis": "row_hit=10"
      },
      {
        "row": "QC-49",
        "condition": "qc49_inherit_prior=False，不套用",
        "hit": false,
        "basis": "qc49_inherit_prior=False"
      }
    ],
    "rearm_trigger": "FY27 本益比 <15x（約 $290）且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修→加碼至衛星上限",
    "exec_line": "新資金：現價建 1.5%（衛星上限 3% 之半），其餘掛 12-09 財報論點增強或 <$290 回檔。已持有：維持（不加碼至 Google 份額數據點證偽前；不減碼因無 thesis 級觸發；清倉僅限 Google 訓練晶片設計權移轉）"
  },
  "triggers": [
    {
      "n": 1,
      "text": "Google 客製晶片份額（相對 95→80→65 路徑）",
      "type": "風險",
      "maps_to": "R1／H1",
      "metric": "Broadcom 於 Google TPU 採購份額",
      "threshold": "較路徑低逾 10pp，或 2027 年度 <75%",
      "action": "重審護城河等級；等級降至 B 即觸強制迴避",
      "source_freq": "TrendForce／Counterpoint／每年",
      "date": "2027-06-30",
      "evidence_refs": [
        "competitive_share_entrants#2",
        "competitive_share_entrants#3",
        "customer_second_source#0",
        "customer_second_source#1"
      ]
    },
    {
      "n": 2,
      "text": "FY27 AI 半導體營收兌現度",
      "type": "假設驗證",
      "maps_to": "H1",
      "metric": "TTM AI 營收對 $115B 路徑進度",
      "threshold": "連 2 季落後逾 10%",
      "action": "減碼至衛星上限之半",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 3,
      "text": "半導體分部營業利益率（管理層 mix 歸因託管閘）",
      "type": "風險",
      "maps_to": "財務品質／H3",
      "metric": "半導體分部營業利益率",
      "threshold": "跌破 55%（現 61%）連 2 季→mix 歸因證偽",
      "action": "結構性壓縮警示、減碼 1/3",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 4,
      "text": "VMware ARR 年增率與通路重構",
      "type": "假設驗證",
      "maps_to": "H2／R3",
      "metric": "VCF ARR YoY",
      "threshold": "跌破 10% 連 2 季",
      "action": "H2 降級、減碼",
      "source_freq": "公司財報／每季",
      "date": "",
      "evidence_refs": [
        "channel_business_model_shift#1"
      ]
    },
    {
      "n": 5,
      "text": "OpenAI／Anthropic 實際出貨 GW 對公司指引",
      "type": "假設驗證",
      "maps_to": "H1／R2",
      "metric": "實際部署 GW（OpenAI 2027 合約 1.3GW）",
      "threshold": "低於自身指引逾 20%，或 OpenAI 融資關閉延後逾 2 季",
      "action": "H1 核心假設削弱、凍結加碼",
      "source_freq": "公司法說＋融資報導／每季",
      "date": "2027-06-30",
      "evidence_refs": [
        "customer_concentration_credit#3",
        "customer_concentration_credit#4"
      ]
    },
    {
      "n": 6,
      "text": "XPV 表外平台信用",
      "type": "風險",
      "maps_to": "R2",
      "metric": "XPV 名目擔保規模與信用展望",
      "threshold": "20GW 全量名目達 $370B 且信用展望連 2 季負向",
      "action": "表外槓桿重審、減碼",
      "source_freq": "BofA 模型／評等機構／每季",
      "date": "",
      "evidence_refs": [
        "customer_concentration_credit#3"
      ]
    },
    {
      "n": 7,
      "text": "Google 主力訓練 TPU 設計權移轉（唯一清倉級）",
      "type": "Single Thing",
      "maps_to": "單一致命事件",
      "metric": "v9 Triggerfish／v10 訓練晶片設計權歸屬",
      "threshold": "Google 公告主設計權授予 MediaTek 或其他夥伴",
      "action": "清倉並重跑 DD",
      "source_freq": "Google 法說／產業研究／每季",
      "date": "2027-12-31",
      "evidence_refs": [
        "competitive_share_entrants#3",
        "customer_second_source#0"
      ]
    },
    {
      "n": 8,
      "text": "上行：取得 v10 或 GW 出貨超前",
      "type": "加碼",
      "maps_to": "H1",
      "metric": "設計權公告／GW 出貨",
      "threshold": "Broadcom 取得 v10，或 GW 出貨超前指引逾 10%（論點增強，非價格）",
      "action": "重審角色可回核心、加碼至衛星上限",
      "source_freq": "公司法說／每季",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 9,
      "text": "估值回補",
      "type": "估值rearm",
      "maps_to": "H3",
      "metric": "FY+2 本益比",
      "threshold": "<15x（約 $290）且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修",
      "action": "加碼至衛星上限 3%",
      "source_freq": "自算／每兩週",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 10,
      "text": "歐盟／美國 VMware 反壟斷程序階梯",
      "type": "風險",
      "maps_to": "R3／H2",
      "metric": "程序階段",
      "threshold": "異議書→trim 1/3；裁定強制改授權模式或裁罰→H2 重審、減碼至半",
      "action": "依階梯",
      "source_freq": "歐盟／DOJ 公告",
      "date": "2027-03-31",
      "evidence_refs": [
        "regulatory_antitrust#0",
        "regulatory_antitrust#1",
        "regulatory_antitrust#2"
      ]
    },
    {
      "n": 11,
      "text": "關稅、出口管制與中國政策",
      "type": "風險",
      "maps_to": "R3／地緣",
      "metric": "Section 232 分類、光收發器禁令、中國 VMware 移除令",
      "threshold": "Broadcom XPU 納入 25% 關稅；中國軟體營收流失可量化",
      "action": "重算成本吸收（合併毛利率 −2pp 為吸收失敗判定閘）",
      "source_freq": "商務部／CBP／每季",
      "date": "2026-12-31",
      "evidence_refs": [
        "reg_tariff_export#0",
        "reg_tariff_export#3",
        "regulatory_antitrust#4",
        "regulatory_antitrust#5"
      ]
    },
    {
      "n": 12,
      "text": "TSMC／CoWoS 供給鏈與台灣風險",
      "type": "風險",
      "maps_to": "供給",
      "metric": "CoWoS 分配、雷射／PCB 缺口、台海事件",
      "threshold": "供給約束使季度 AI 營收落後指引逾 10%；台海衝突為 thesis 已破",
      "action": "前者列入兌現度追蹤；後者清倉",
      "source_freq": "TSMC 法說／每季",
      "date": "",
      "evidence_refs": [
        "geo_supply_chain#0",
        "geo_supply_chain#1",
        "geo_supply_chain#2",
        "supply_demand_durability#2"
      ]
    },
    {
      "n": 13,
      "text": "資安事件與軟體信任",
      "type": "風險",
      "maps_to": "H2",
      "metric": "重大漏洞／入侵事件與客戶流失",
      "threshold": "事件導致 ARR 年增跌破 10%",
      "action": "併入觸發器 4",
      "source_freq": "CISA／公司公告",
      "date": "",
      "evidence_refs": [
        "major_events#1",
        "major_events#2",
        "product_recall_warning#0",
        "product_recall_warning#1"
      ]
    },
    {
      "n": 14,
      "text": "客戶集中度與自研能力",
      "type": "風險",
      "maps_to": "R1／R2",
      "metric": "前五大占營收（10-Q 45%）、客戶自有工具鏈進展",
      "threshold": "前五大 >55% 且任一客戶宣布自有工具鏈取代 Broadcom",
      "action": "集中度升 🔴、減碼",
      "source_freq": "10-Q／每季",
      "date": "",
      "evidence_refs": [
        "customer_concentration_credit#0",
        "customer_concentration_credit#2",
        "customer_second_source#2",
        "substitute_technology#1"
      ]
    },
    {
      "n": 15,
      "text": "估值 trim 天花板",
      "type": "減碼",
      "maps_to": "H3",
      "metric": "FY+2 本益比",
      "threshold": ">30x（自身短窗高點 39x 下修校準）",
      "action": "最多 trim 1/3，不單獨清倉",
      "source_freq": "自算／每兩週",
      "date": "",
      "evidence_refs": []
    },
    {
      "n": 16,
      "text": "Q4 FY26 財報＋新 CFO 首季",
      "type": "複審日期",
      "maps_to": "—",
      "metric": "—",
      "threshold": "—",
      "action": "重跑 DD",
      "source_freq": "公司財報／一次性",
      "date": "2026-12-09",
      "evidence_refs": []
    }
  ],
  "contradictions": [
    {
      "axis": "共識清單",
      "side_a": "方向一致：AI 需求真實且受供給約束（backlog >$73B、能見度 2028、CoWoS 售罄）；現金轉換頂尖（FCF 46%）；資本配置紀律 A；估值兩尺皆便宜",
      "side_b": "矛盾拓撲＝集中單一軸：Google 分單與客戶自研（護城河軸），其餘軸為程度差異",
      "ruling": "爭議集中→點名護城河軸為 binding 軸，信心不整體下修但角色降衛星",
      "evidence_level": "L1",
      "settle_metric": "Google 世代設計權歸屬",
      "if_then": [
        "若 Broadcom 取得 v9／v10 訓練設計權→角色回核心",
        "若 v9 訓練交 MediaTek→清倉"
      ]
    },
    {
      "axis": "AI 指引加速 vs Google 份額稀釋",
      "side_a": "FY27 $115B／FY28 $230B 指引、Q3 +221%——絕對金額爆發",
      "side_b": "Google 刻意四夥伴、MediaTek 成本低 20-30%、Marvell 簽約——份額路徑 95→80→65",
      "ruling": "可調和（程度差異）：份額稀釋與絕對金額成長同時為真；Base 對 FY28 指引打八折吸收稀釋，不採全額指引",
      "evidence_level": "L1 財報 vs L2 產業報導",
      "settle_metric": "Google 於 AI 營收占比與 FY28 AI 營收實績",
      "if_then": [
        "若 FY27 AI 營收 ≥$115B 且 Google 占比降但金額升→維持",
        "若 FY27 落後指引逾 10% 連 2 季→減碼"
      ],
      "evidence_refs": [
        "competitive_share_entrants#2",
        "competitive_share_entrants#3"
      ]
    },
    {
      "axis": "合約承諾 vs 客戶融資能力（不可調和）",
      "side_a": "OpenAI 1.3GW 2027 合約承諾、Anthropic 8.5GW、Meta 3GW；Q3 營收 $29.6B 已印",
      "side_b": "OpenAI 2026-05 無法關閉 $18B 融資、2026 預虧 $14B；Broadcom 只願出資第一階段、放寬對等出資；XPV 名目 $370B",
      "ruling": "選 A 側：L1（已實現營收＋合約）高於 L2（融資報導，已 4 個月且其後 Q3 仍超標）；但把出貨 GW 與融資關閉列為獨立觸發器，Bear 機率因此守 30% 不降",
      "evidence_level": "L1 vs L2",
      "settle_metric": "OpenAI 2027 實際部署 GW 與融資關閉公告",
      "if_then": [
        "若 2027 上半年 OpenAI 融資關閉且首批出貨→其餘 1/2 倉位解鎖",
        "若融資延後逾 2 季或 Broadcom 出資比例再升→減碼至衛星上限之半"
      ],
      "evidence_refs": [
        "customer_concentration_credit#3",
        "customer_concentration_credit#4"
      ]
    },
    {
      "axis": "Steelman：現在就賣的最強論證",
      "side_a": "①最大客戶已公開要每個環節都有替代者，而替代者成本低 20-30%，這是護城河定價面的結構性上限；②FY28 EPS 30 若是資本週期峰值，18.5x 是循環股頂部倍數不是便宜；③前五大 45%＋單一經銷商 42%＋$370B 表外名目，任一環節斷鏈都是 −50% 級；④合併毛利率已在下滑，管理層要求「分開建模」是敘事管理的典型前兆",
      "side_b": "逐點回應：①份額稀釋已計入 Base 八折與 Bear 30%，且執行面（六客戶、供給鎖定）在擴大，記帳在趨勢不在等級；②共識 FY28 一週上修 13.5% 至 30、90 天 +17%，峰值論尚無下修證據，Bear 錨（15×12）已定價週期回落；③集中度是衛星角色與 3% 上限的原因，不是迴避的原因——迴避須 thesis 級失敗證據；④半導體分部營業利益率 +440bp YoY、非 GAAP 營業利益率 QoQ 續升，mix 歸因暫採信並託管於觸發器 3",
      "ruling": "進場維持，但賣方論證 ①③ 直接決定角色與上限，非僅記錄",
      "evidence_level": "L1／L2 混合",
      "settle_metric": "半導體分部營業利益率與 Google 設計權",
      "if_then": [
        "若分部營業利益率 <55% 連 2 季→賣方論證 ④ 成立，減碼 1/3",
        "若 FY28 共識連 2 次下修→賣方論證 ② 成立，減碼至半"
      ]
    },
    {
      "axis": "與前份報告（2026-09-03）交叉：裁決與方法",
      "side_a": "本次：進場｜衛星、上限 3%",
      "side_b": "前份：進場｜衛星（自 2026-06-23 核心降衛星）",
      "ruling": "方向與角色一致，未翻面；90 天內無觸發器發火，亦無承繼需求。差異僅在倉位上限明示 3%（前份未明示）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若 12-09 財報論點增強→上限可回 5%",
        "若 Google 份額數據點證偽→維持 3% 並凍結"
      ]
    },
    {
      "axis": "前份漂移：price_at_dd",
      "prior_field": "price_at_dd",
      "side_a": "本次 357.89（2026-09-04 收盤）",
      "side_b": "前份 367.24",
      "ruling": "主因＝價格變了（−2.5%，財報後續回檔）；基本面未變；方法論未變",
      "evidence_level": "L1",
      "settle_metric": "—",
      "if_then": [
        "若價格續跌至 $290→估值回補觸發",
        "若反彈逾 $450→停止加碼"
      ]
    },
    {
      "axis": "前份漂移：ev5y_pct",
      "prior_field": "ev5y_pct",
      "side_a": "本次 134.1%",
      "side_b": "前份 125.1%",
      "ruling": "主因排序：①基本面（共識 FY28 EPS 26.43→30.0 上修 13.5%，Base 路徑終端 38.47→39.5）②價格（−2.5% 使同一終端價報酬率升）③方法論未變（同三情境、同機率）",
      "evidence_level": "L2 共識",
      "settle_metric": "FY28 共識方向",
      "if_then": [
        "若共識 FY28 續升→Base 上修",
        "若下修→回 125% 以下"
      ]
    },
    {
      "axis": "前份漂移：irr_base_pct",
      "prior_field": "irr_base_pct",
      "side_a": "本次約 18.2%（含息）",
      "side_b": "前份 15.9%",
      "ruling": "主因＝基本面（FY28 共識上修帶動 Base 終端 EPS 39.5 vs 38.47）與價格（−2.5%）；方法論未變。注意：Base 不含息 IRR >15% 觸發罕見警示，機率分配已守 30／40／30 未放寬",
      "evidence_level": "L2",
      "settle_metric": "FY28 共識",
      "if_then": [
        "若 FY27 兌現→維持",
        "若落後→重算"
      ]
    },
    {
      "axis": "前份漂移：asym_ratio",
      "prior_field": "asym_ratio",
      "side_a": "本次 6.76",
      "side_b": "前份 6.0",
      "ruling": "主因＝價格（現價較低使 Bull 上行放大、Bear 下行縮小）；Bear 終端 180 vs 170 屬方法論微調（Bear 本益比 10x→12x，因共識未下修、Bear 地板尚平穩）。護城河趨勢↓下，此比率僅作參考、不作進場依據",
      "evidence_level": "—",
      "settle_metric": "共識 FY28 是否連續下修（Bear 地板是否下移）",
      "if_then": [
        "若共識連 2 次下修→比率標失效",
        "否則維持參考"
      ]
    },
    {
      "axis": "前份漂移：bear_5y_price",
      "prior_field": "bear_5y_price",
      "side_a": "本次 180（15×12）",
      "side_b": "前份 170（17×10）",
      "ruling": "主因＝方法論（Bear 終端 EPS 15 較前份 17 更深，但終端倍數 12x 較 10x 高：Bear 故事改為「循環股定價」而非「無成長折價」；淨效果 +$10）；基本面與價格非主因",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若 2028 資本週期見頂訊號出現→Bear 倍數回 10x",
        "否則維持"
      ]
    },
    {
      "axis": "前份漂移：pct_5y",
      "prior_field": "pct_5y",
      "side_a": "本次 24.4%",
      "side_b": "前份 15.0%",
      "ruling": "主因＝方法論（本輪以 valuation_history trailing 年度 4 點樣本計算；前份口徑不同）；燈號結論不變（皆 🟢）",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "若分位 >30% 且 PEG >1→燈號降",
        "否則維持"
      ]
    },
    {
      "axis": "均線狀態沿用",
      "prior_field": "ma",
      "side_a": "本次 ✅（沿用前份 2026-09-03 量測）",
      "side_b": "前份 ✅",
      "ruling": "本輪證據包未含週線 W52／W104／W250 資料，價僅較前份低 2.5%，狀態視為未變；標「證據包未涵蓋」請閘覆核",
      "evidence_level": "—",
      "settle_metric": "週線資料",
      "if_then": [
        "若價 <W52→狀態改 🟢或🟠，節奏調節不改裁決",
        "否則維持"
      ]
    },
    {
      "axis": "ID 對帳",
      "side_a": "ID：AI Accelerator Demand（as-of 2026-09-05）shortage／Phase II／priced_in mid；ID：Hyperscaler（2026-05-05）shortage／Phase II",
      "side_b": "本檔：Phase II、供需 durability 裁決＝供給可逆性高（CoWoS 缺口 2026 底縮至 10%，緊缺脆弱、下行更猛）",
      "ruling": "一致，無分歧；priced_in mid 與本檔估值 🟢 略有張力，以本檔自身估值尺為準（ID 為產業層）",
      "evidence_level": "L2",
      "settle_metric": "CoWoS 缺口與雲端 capex 指引",
      "if_then": [
        "若 ID 更新為 Phase III→Bear 機率上調",
        "否則維持"
      ]
    },
    {
      "axis": "同形狀 peer 對帳",
      "side_a": "證據包無 30 天內 NVDA／MRVL／AMD 裁決紀錄",
      "side_b": "—",
      "ruling": "一句帶過：無近期 peer 裁決可對帳，不阻斷",
      "evidence_level": "—",
      "settle_metric": "—",
      "if_then": [
        "—",
        "—"
      ]
    },
    {
      "axis": "賣方共識對照",
      "side_a": "57 位分析師目標價均值 $520、財報後多家上修；現價低於均值 31%",
      "side_b": "本檔 1 年目標 $425 較均值保守 18%",
      "ruling": "現價低於共識均值→續漲不需共識上修＝結構順風，支持進場；本檔更保守之處在 Google 份額與 2028 資本週期假設；市場錯在哪：共識把 FY28 $230B 指引近乎全額印進 EPS 30，卻同時給 18.5x——隱含「2028 後急降」；本檔認為錯的是倍數而非盈餘方向，故 Base 八折盈餘配 20x",
      "evidence_level": "L2",
      "settle_metric": "FY28 實績與倍數",
      "if_then": [
        "若 FY28 兌現 ≥$185B→re-rate 至 22-25x",
        "若 FY28 <$150B→共識對、本檔錯，減碼"
      ],
      "evidence_refs": [
        "customer_concentration_credit#0"
      ]
    },
    {
      "axis": "樞紐變數與共同顯影指標",
      "side_a": "雲端 AI 資本支出 ROI 兌現同時打 H1（量）與 H3（倍數框架）；R1 與 R2 兩條失敗向量非獨立（Google 分單與客戶融資皆由「客戶議價與資本壓力」驅動）",
      "side_b": "共同財報級顯影指標＝半導體分部營業利益率（份額稀釋與客戶壓價都先在此顯影）",
      "ruling": "監測首位＝半導體分部營業利益率（觸發器 3）；Bear 機率不以獨立事件相乘，直接取 30%",
      "evidence_level": "L1",
      "settle_metric": "半導體分部營業利益率",
      "if_then": [
        "若 <55% 連 2 季→減碼 1/3",
        "若 ≥60% 續 4 季→凍結解除"
      ]
    },
    {
      "axis": "監管量化與程序階梯",
      "side_a": "歐盟正式調查（2026-02）、文件案敗訴（2026-08）、美國授權調查（2026-07）、中國移除令",
      "side_b": "受影響營收：歐洲基礎設施軟體占比證據包未涵蓋，無法量化",
      "ruling": "標「證據包未涵蓋」；程序階梯寫入觸發器 10（異議書→trim 1/3；裁定→減至半）；不以定性一句話帶過",
      "evidence_level": "L1 程序",
      "settle_metric": "歐盟異議書",
      "if_then": [
        "異議書→trim 1/3",
        "無異議書且 ARR ≥12%→維持"
      ],
      "evidence_refs": [
        "regulatory_antitrust#0",
        "regulatory_antitrust#1",
        "regulatory_antitrust#2",
        "regulatory_antitrust#4",
        "regulatory_antitrust#5"
      ]
    },
    {
      "axis": "利空新鮮度與倉位",
      "side_a": "Google 四夥伴（2026-08-20）、MediaTek 目標上修（2026-07-31）皆 <1 季",
      "side_b": "賣方財報後（2026-09-03）仍上修目標價→已部分進入模型",
      "ruling": "初始倉位仍下修一級（首階 1/2 而非全額）並凍結加碼至 Zebrafish 量產後首個份額數據點",
      "evidence_level": "L2",
      "settle_metric": "Q4 2026 Google 份額數據點",
      "if_then": [
        "數據點未證偽→解凍",
        "證偽→維持凍結並減碼"
      ],
      "evidence_refs": [
        "competitive_share_entrants#3",
        "competitive_share_entrants#2"
      ]
    },
    {
      "axis": "精英指標未穿越週期",
      "side_a": "非 GAAP 營業利益率 67.9% 與 FCF 46% 處歷史高檔，未穿越完整 AI 資本週期",
      "side_b": "結構性成分＝軟體 70%+ 分部與規模攤薄 R&D 15.9%；週期性成分＝XPU 系統含量與客戶預付；殘差無法拆",
      "ruling": "殘差不選邊，定價進 Bear 30% 與衛星角色；品質分不滿額（成長持久性 8.0 非 8.5）",
      "evidence_level": "L1",
      "settle_metric": "2028 後分部營業利益率",
      "if_then": [
        "若 2028 分部營業利益率守 58%+→品質分回 8.5",
        "若 <55%→降"
      ]
    },
    {
      "axis": "前份漂移：rearm_trigger",
      "side_a": "前份 2026-09-03 報告未填再進場條件（前一版格式沒有這個欄位）",
      "side_b": "本次填入衛星加碼條件（FY27 本益比 <15x 約 $290 且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修）",
      "ruling": "方法論驅動：欄位由空變有，非資訊變化；歸因主因＝方法論（v17 必填），次因＝無",
      "evidence_level": "前後兩份報告的機器欄逐欄對照",
      "settle_metric": "不適用",
      "if_then": [
        "若前份實有再進場條件而擷取遺漏 → 改列資訊變化並重新歸因"
      ],
      "prior_field": "rearm_trigger",
      "evidence_refs": []
    }
  ],
  "premortem": {
    "blind_spots": [
      {
        "text": "假設①Google 多世代長約（至 2031）保證訓練晶片主設計權——若協議是份額制而非固定量（管理層拒答金額與結構，來源：摘要），前提不成立則 Google 營收在 2028 可能減半",
        "evidence_refs": [
          "competitive_share_entrants#3",
          "customer_second_source#0"
        ]
      },
      {
        "text": "假設②OpenAI／Anthropic 承諾可融資——若融資市場對 AI 基建轉冷，10GW＋8.5GW 承諾縮水、XPV 平台成為 Broadcom 表外信用曝險",
        "evidence_refs": [
          "customer_concentration_credit#3",
          "customer_concentration_credit#4"
        ]
      },
      {
        "text": "假設③TSMC／CoWoS 供給能如期擴張且台海無事——供給鏈 100% 集中台灣，雷射／PCB 缺口已蔓延；NVIDIA 預訂過半 CoWoS-L",
        "evidence_refs": [
          "geo_supply_chain#0",
          "geo_supply_chain#1",
          "geo_supply_chain#2",
          "supply_demand_durability#2"
        ]
      },
      {
        "text": "假設④管理層對合併毛利率下滑的 mix 歸因為真——若客戶壓價已在半導體分部顯影，則 61% 分部營業利益率是峰值",
        "evidence_refs": []
      },
      {
        "text": "本輪證據缺口：最新一季（Q3 FY26）逐字稿未親讀，只有財報數字與前三季摘要；週線均線資料、投入資本與營運資金明細、同業前瞻本益比皆未涵蓋",
        "evidence_refs": []
      },
      {
        "text": "敏感度排序：Google 份額每低 10pp 對 FY28 EPS 約 −8%；雲端 capex 2028 下修 20% 對 FY28 EPS 約 −15%；分部營業利益率 −5pp 對 EPS 約 −8%——最大單一敏感度為 capex 週期，但其為漸進非離散事件，故單一致命事件取 Google 設計權（第二大且離散）",
        "evidence_refs": []
      }
    ],
    "failure_story": "五年後虧 50%：2028 雲端資本支出進入消化期，同時 Google 把訓練世代也交 MediaTek、OpenAI 融資斷鏈使 10GW 縮至 3GW；AI 營收 2028 停在 $150B 後回落，EPS 自 27 跌回 15，市場改給 12x。與單一致命事件關係：⚠ 部分重疊（Google 為主軸、融資為次軸）→ 次軸已補為觸發器 5／6",
    "second_failure": "thesis 完全兌現但以「系統／機架與客戶自有 IP 代工」形態兌現：AI 營收達 $230B，但半導體分部營業利益率自 61% 壓至 50%、Broadcom 被市場重新歸類為客製代工而非設計 IP 平台，估值框架自 25x 切換到 15x，5 年報酬約 +40% 而非 +120%。機率不可忽略→Bull 終端倍數壓在 26x（非 30x）",
    "max_dd": {
      "lo": -58.0,
      "hi": -40.0,
      "path_risk": "🔴",
      "trigger_time": "最可能觸發：2027 下半年至 2028 上半年（雲端 FY28 capex 指引與 Google v9 設計權明朗期重疊）；恢復峰值：若 thesis 完整需 18-30 個月，若 Google 訓練設計權移轉則 thesis 已破不假設恢復。🔴 且 thesis 脆弱（護城河趨勢↓）→倉位上限自 6% 下修至 3%、持有年限標中期並警示中途出場風險"
    }
  },
  "kill_metrics": [
    {
      "metric": "Broadcom 於 Google 客製晶片份額（相對路徑 95→80→65）",
      "bear_threshold": "較路徑低逾 10pp，或 2027 年度 <75%→護城河重審",
      "window": "每年",
      "source": "TrendForce／Counterpoint",
      "last_status": "ok"
    },
    {
      "metric": "FY27 AI 半導體營收兌現度（指引 $115B）",
      "bear_threshold": "連 2 季落後指引進度逾 10%→減碼",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "半導體分部營業利益率",
      "bear_threshold": "跌破 55%（現 61%）連 2 季→結構性壓縮警示",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "VMware VCF ARR 年增率",
      "bear_threshold": "跌破 10% 連 2 季→H2 降級",
      "window": "2 季",
      "source": "公司財報",
      "last_status": "ok"
    },
    {
      "metric": "OpenAI／Anthropic 實際出貨 GW 對指引",
      "bear_threshold": "低於自身指引逾 20%→H1 削弱",
      "window": "每季",
      "source": "公司法說",
      "last_status": "ok"
    },
    {
      "metric": "XPV 平台名目擔保與信用展望",
      "bear_threshold": "名目達 $370B 且信用展望連 2 季負向→表外槓桿重審",
      "window": "每季",
      "source": "BofA 模型／評等",
      "last_status": "ok"
    },
    {
      "metric": "Google v9／v10 訓練晶片設計權歸屬",
      "bear_threshold": "主設計權授予 MediaTek 或其他夥伴→清倉",
      "window": "每季",
      "source": "Google 法說／產業研究",
      "last_status": "ok"
    }
  ],
  "reasoning": {
    "archetype": "輸入：FCF 利潤率 46%（Q3 FY26）、非 GAAP 營業利益率 67.9%、資本支出 $532M 對營收 $29.6B（1.8%）、營收 YoY +86%→輕資產高現金複利體質，非循環商品定價（無 spot 價格）、非金融、已獲利→品質複利成長，信心高；AI 資本週期色彩以 Bear 機率 30% 與供給可逆性裁決承接，不換尺",
    "thesis": "H1 門檻取自指引 $115B／$230B（capital_markets_pricing#1）與 Google 份額路徑 95→80→65；H2 取自 Q3 軟體 $8.75B（+29%）與 VCF ARR +17%（2026-06 口徑）；H3 取自 FY27 本益比 18.5x 與短窗高點 39x→15-25x 區間。單一致命事件由敏感度排序取第二大但唯一離散者（Google 設計權），機率 20-25% 以多世代長約為反向錨",
    "industry": "Phase II 由 ID（AI Accelerator Demand 2026-09-05）載入，經自身位置閘：backlog >$73B、能見度 2028、CoWoS 缺口 20%→10%→擴張後段非過熱頂部。供需 durability 裁決＝供給可逆性高（缺口正在閉合、NVIDIA 預訂過半 CoWoS-L 顯示競爭產能）→Bear 機率 30% 不得下調。議價權：上游弱（TSMC 單一）、下游中偏弱（前五大 45%、單一經銷商 42%，10-Q 2026-05-03）",
    "moat": "執行 9（六客戶、供給鎖定至 2028、AI 營收 +221%、設計夥伴份額 ~60%）×定價 8（Google 明示替代者、MediaTek 成本低 20-30%、合併毛利率 mix 下滑閘二扣 0 至 −0.5）→合併 8.5→等級 A（執行加權 0.6 得 8.6 進位 9）。趨勢：一擴一縮取論點更關鍵的份額維度→↓；閘 A 因最大客戶份額下滑不得↑。閘一：營業利益率對 MRVL 差 +27.7pp、分部 +440bp YoY→擴大，可打 ≥8。閘三：對手絕對美元新增（MediaTek 2026E >$2B）遠低於 AVGO AI 新增（YoY +$11.5B）→未觸規模質變。記帳一次：負面證據記趨勢不記等級→不觸強制迴避",
    "growth": "Runway 5-7 年：AI 營收 $58B→$230B（FY28 指引）後增速取決於第二輪 capex；Y5 末客製 ASIC 對雲端加速器滲透估 35-50%（ID：自研 25-30% 且升）且無 sourced 第二 S 曲線（矽光子「尚未到位」，來源：摘要）→🟡。內生天花板：ROIIC 代理 80%×再投資率 6%≈5%；Base EPS CAGR 15.4% 超出⚠→Bear ≥30%；缺口歸因＝客戶承擔資本的 XPU 新 S 曲線（backlog sourced）＋營業槓桿，非 re-rate。衰退訊號 2 個（mix 毛利率、Google 份額）→🟡觀察、五問後定性 🟢 非陷阱",
    "quality": "Q3 FY26：FCF $13,665M÷營收 $29,591M＝46.2%（Q2 46.0%，持平高檔）；非 GAAP 營業利益 $20,095M÷$29,591M＝67.9%（Q2 67.3%）；SBC $2,019M＝營收 6.8%、GAAP 營業利益 12.7%（Q2 9.4%／19.4%）。營收 YoY +86% 對 GAAP 營業利益率 48.6%→53.9% QoQ 擴張→發散 <0（營業槓桿正）。三年逐年、DuPont 投入資本、CCC 不在證據包→標未涵蓋，品質分以 TTM 與最新季替代並在分數扣 0.2",
    "governance": "計分卡：VMware ROIIC≈軟體年化營業利益 $25B÷$69B≈35% 過；回購收益率以 FY27 盈餘殖利率 5.4%（1÷18.5）近似過（均價未涵蓋）；SBC 淨稀釋≈$8B÷$1.68T≈0.5%／年過→3／3→A。股息 +10%、回購額度 $17.5B 至 2026 底（來源：摘要）。CFO 交接（Spears→Thuener，2026-06-12）設 2026-12-09 有日期複審；內部人交易未涵蓋標數據限制。無併購、無重編、無證券集體訴訟（events 軸）→🟢",
    "valuation": "FY27 本益比＝357.89÷19.33＝18.51；FY26 基準 30.77。3Y EPS CAGR 以 FY26→FY28 共識（11.63→30.0）2 年化 60.6%（無 FY29 共識，標 2 年口徑）→PEG 0.31（FY27）／0.51（FY26）。五年分位 24.4%（trailing 4 年度樣本）。兩尺 🟢。1 年目標 19.33×22＝$425（+18.8%）；2 年 26.0×22＝$572（+59.8%）；Bear 錨 17.4×15＝$261（−27%）。Base 5Y：39.5×20＝$790（+120.7%）、IRR 不含息 17.2%＋息 1.0%；EPS 貢獻 15.4%／年、re-rate 1.6%／年（20÷18.51）→re-rate 占比約 9% <40%→非估值依賴型",
    "trap_analysis": "低 PEG 的三種解釋：週期峰值盈餘、份額侵蝕帳單、市場錯價。反證：共識 FY28 一週 +13.5%、90 天 +17%（consensus_revision，stale=false），FCF 與盈餘同步，backlog 覆蓋 18 個月→前兩者尚無數據支持；正證：前五大 45%、Google 分單、OpenAI 融資→列觀察期指標。空頭一擊路徑：FY28 共識 30→22 且倍數 18.5x→12x→$260-230（−27% 至 −36%）。定性 🟢 非陷阱，2 訊號記為 🟡 觀察",
    "premortem": "Max DD：AVGO 自身 2022 與 2025 上半年回撤約 −30% 至 −40%（前份口徑），疊加 thesis 級事件（Google 設計權）估 −40% 至 −58%（寬度 18pp ≥10）→🔴；觸發時點 2027H2-2028H1；🔴且趨勢↓→上限 6%→3%。失敗故事與單一致命事件部分重疊→次軸補觸發器 5／6。第二敗局（代工化）反映在 Bull 終端 26x 非 30x。Bull 30／Base 40／Bear 30：Bear 依 searched durability（CoWoS 缺口閉合、供給可逆）與內生天花板超出，非 pattern 外推"
  },
  "evidence_dismissed": [
    {
      "ref": "customer_concentration_credit#1",
      "reason": "FY2025 10-K（2025-12-18）前五大 40%／經銷商 48% 已被 2026-05-03 10-Q 更新一季數字（45%／56%）取代，依最新一季優先序不重複引用"
    },
    {
      "ref": "reg_tariff_export#1",
      "reason": "8-K 制式風險因子文字，無新增量化資訊，內容已由 reg_tariff_export#0 的 Section 232 具體條款覆蓋，屬重複計"
    },
    {
      "ref": "reg_tariff_export#4",
      "reason": "「中國占營收 meaningful portion」未給占比數字，且 edgar_concentrations 未揭露地區集中度，口徑不可回溯無法量化"
    },
    {
      "ref": "regulatory_antitrust#3",
      "reason": "來源為單一二手彙整（Simply Wall St），未附 ITC docket 編號與涉案產品線，Broadcom 為多被告之一且屬記憶體模組專利，無法對應到營收軸"
    },
    {
      "ref": "major_events#3",
      "reason": "員工資料經供應商外洩，資料出現於 2024-12（12 個月窗外），屬人資資料非客戶或產品層事件，與 thesis 無接線"
    },
    {
      "ref": "substitute_technology#0",
      "reason": "與 competitive_share_entrants#2 為同一篇報導的中文轉述（MediaTek 15-20% 目標），已在 R1 與觸發器 1 記帳一次，避免重複扣分"
    }
  ],
  "plain": {
    "verdict_line": "進場，但只當衛星，倉位不超過三分之一的常規上限",
    "verdict_sub": "現價先建一半，另一半等十二月財報確認或股價跌到二百九十以下再補。",
    "five": {
      "how_it_makes_money": "幫 Google、Meta、OpenAI 這些雲端巨頭設計專屬 AI 晶片，再加上網路晶片與 VMware 軟體訂閱。客戶出架構，博通出設計與整合，工廠由台積電代工。",
      "why_now": "財報剛超標卻回檔，用明年盈餘算本益比只有十八倍多。共識還在上修，市場給的是循環股價格。",
      "why_this_size": "最大客戶 Google 正刻意扶植第二、第三家設計夥伴。這件事已經在發生，所以只能當衛星，不當核心。",
      "biggest_fear": "Google 把下一代訓練晶片的主設計權交給聯發科。這是唯一會讓我直接清倉的事。",
      "how_to_act": "現價買一半，十二月九日財報若 AI 營收達標再補另一半。跌破二百九十且基本面沒壞也可補。"
    },
    "business": {
      "what_to_whom": "賣客製 AI 加速器與網路晶片給六家雲端與模型公司，賣私有雲軟體訂閱給大型企業。前五大客戶占營收快一半。",
      "why_customers_stay": "換設計夥伴要重跑一到兩年的晶片流程，而且博通手上有台積電先進封裝與高速傳輸的整合能力。軟體端則是換掉 VMware 的遷移成本很高。",
      "moat_direction": "等級 A，方向往下。最弱的地方在定價：Google 已公開要每個環節都有替代者，聯發科的推論晶片還便宜兩三成。"
    },
    "bets": [
      {
        "claim": "明年 AI 晶片營收能兌現一千一百五十億的指引，六家客戶一起放量。",
        "wrong_when": "連續兩季進度落後指引一成以上，我就錯了。"
      },
      {
        "claim": "Google 分單只影響推論晶片，訓練晶片主設計權還在博通手上。",
        "wrong_when": "Google 公告下一代訓練晶片交給別人，我就錯了。"
      },
      {
        "claim": "毛利率下滑只是產品組合，半導體部門獲利率守得住。",
        "wrong_when": "半導體部門營業利益率連兩季跌破五成五，我就錯了。"
      }
    ],
    "fears": [
      {
        "clock": "🔥",
        "text": "Google 份額比預期掉得快，二〇二七年低於七成五，或下一代訓練晶片易主。"
      },
      {
        "clock": "🔥",
        "text": "OpenAI 融資關不了，一百八十億缺口拖累十 GW 承諾，表外平台名目上看三千七百億。"
      },
      {
        "clock": "🐢",
        "text": "歐盟反壟斷調查發異議書，VMware 被迫改授權模式，軟體現金流變薄。"
      }
    ],
    "market_wrong": "共識把二〇二八年兩千三百億的指引幾乎全額算進盈餘，卻只給十八倍多。這等於同時相信指引又相信之後會急跌。我認為盈餘該打八折，但倍數該回到二十倍。錯的是倍數，不是方向。",
    "growth_funding": "公司自己幾乎不用花錢擴產，內生成長天花板約百分之五。共識盈餘年增一成五以上，差額來自客戶出錢的專屬晶片新曲線，不靠估值上修。",
    "stories": {
      "bull": "六家客戶如期部署，博通連下一代 Google 訓練晶片也拿到。二〇三一年盈餘六十美元，市場給二十六倍。",
      "base": "指引兌現八成，Google 份額慢慢從九成五降到六成五，但金額仍在漲。二〇三一年盈餘近四十美元，倍數二十倍。",
      "bear": "二〇二八年雲端資本支出進入消化期，Google 推論轉聯發科，OpenAI 承諾縮水。盈餘退回十五美元，市場當循環股給十二倍。"
    },
    "change_my_mind": [
      {
        "what": "Google 下一代訓練晶片主設計權",
        "threshold": "公告交給聯發科或其他夥伴",
        "then": "清倉並重跑研究",
        "when": "2027-12-31 前明朗"
      },
      {
        "what": "明年 AI 晶片營收進度",
        "threshold": "連兩季落後指引一成以上",
        "then": "減碼到衛星上限的一半",
        "when": "2026-12-09 起逐季"
      },
      {
        "what": "半導體部門營業利益率",
        "threshold": "跌破五成五連兩季",
        "then": "減碼三分之一",
        "when": "—"
      }
    ],
    "prior_compare_reason": "與兩天前的報告裁決相同，都是進場加衛星。差別只在價格再低了兩個多百分點，以及後年共識盈餘上修，五年期望報酬略升。",
    "how_to_lose": "第一種死法是雲端資本支出二〇二八年見頂，同時 Google 把訓練晶片也分出去，盈餘與倍數一起縮。第二種是論點全對但博通變成低毛利的代工角色，賺到營收卻賺不到估值。第三種是台海事件，那不是風險是結束。",
    "evidence_quality": "十七軸都有查到，數字用到剛公布的本季財報。逐字稿只有前三季摘要，本季法說沒親讀；週線均線與營運資金明細這輪沒拿到。"
  }
}

```
