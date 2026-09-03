# stock-analyst v16 — coverage-axes.md（WP1a 覆蓋矩陣，機器可讀）

> 狀態：**v16-draft**，隨 `_v16_design_spec_20260903.md` §3.3 定稿。本檔是 Stage 0b 覆蓋矩陣 fan-out
> 派工與 `validate_evidence.py` 的**唯一權威資料**——不得在 skill 條文或 agent prompt 裡另抄一份軸清單。
> 判斷語意不變（QC-39／QC-19／archetype gate-set 原條文仍是解讀依據），本檔只是把「哪些軸必須查」
> 從散文變成可被 `scripts/dd_evidence.py` 解析展開的結構。
>
> 抽取方式：檔內唯一一個 ` ```json ` fenced block，`dd_evidence.py` 與 `validate_evidence.py` 用正則
> `` r"```json\s*(.*?)\s*```" ``（DOTALL）取出後 `json.loads`。**改動本檔時務必保持只有一個 json block**，
> 且區塊內容須是合法 JSON（無註解、無尾逗號）。

## 使用說明（人讀）

- **`common`**：全部 7 個 archetype 皆強制的通用軸（對應 §3.3「通用（全 archetype）」段，＋ QC-19
  重大事件五組查詢原文照搬）。`品質複利成長`（default archetype）**只用 common，無額外軸**——它本身
  就是全站的預設尺，circular/金融/未獲利/轉機/公用/EMS 才需要換尺加軸。
- **`by_archetype`**：依 QC-43 七類 archetype 各自的**加項**（不含 common，展開時 common＋加項聯集）。
  循環/商品、未獲利高成長、金融三類的加項逐字對應設計稿 §3.3；轉機/特殊情境、受監管公用/穩定內需、
  EMS/ODM 三類設計稿未列，本稿依 `references/archetype-gatesets.md`（QC-44/45/46）與 QC-43 EMS/ODM
  段的换尺邏輯補上，屬 WP1a 新增裁量（非判斷類規則變動——只是把既有 gate-set 換尺邏輯翻譯成搜尋軸，
  QC-44/45/46 的判準文字本身一字不動）。
- **`per_segment: true`**（僅 `end_markets` 一軸）：實際軸數由 evidence 的 `numbers.segments`（採集包
  的營收段清單）或 `dd_evidence.py --segments a,b,c` 展開，`axis_id` 變成 `end_markets__{slug}`。
  展開前只在此檔留一個模板列。
- **`na_allowed`**：預設 `false`（不得用「不適用」逃避查證）。目前唯一 `true` 的是
  `regulatory_antitrust`——反壟斷對多數小型股/利基市場確實不適用，其餘軸即使查無所獲也必須落
  `status:"none"` 附 `queries_run`，不得標 `not_applicable`。
- **`na_needs_reason`**：全部軸皆 `true`——即使 `na_allowed` 的軸，標 `not_applicable` 時 `note` 仍必須
  非空且講出「為何不適用」（如「市值 $8B、無反壟斷判例先例，2026 年無主管機關動作」），不得只寫
  `"note":"n/a"`。
- **佔位符**：`queries` 模板用 `{TICKER}` `{COMPANY}` `{INDUSTRY}` `{CUSTOMERS}` `{SEGMENT}`（僅
  `end_markets` 展開後可用）——`dd_evidence.py axes --ticker --company --industry --customers` 會逐一
  替換；未提供的參數保留原樣佔位符，供子 agent 自行代入。
- **`affects`**：這一軸的發現最終會回填哪些判斷欄位/裁決輸入（對齊 `judgment.json` 的
  `decision_inputs` / `thesis.H` / `thesis.R` / `moat.trend` / `valuation` / `triggers` 等 key 前綴），
  給 orchestrator 做「這軸缺了會擋哪個裁決欄位」的快速判斷，非強制 schema。

```json
{
  "version": "v16-draft",
  "common": [
    {
      "id": "competitive_share_entrants",
      "name": "競爭份額／新進入者",
      "question": "本標的與主要對手的份額消長方向為何？是否有新進入者或替代供應商在搶單？",
      "queries": [
        "{TICKER} {COMPANY} market share gaining OR losing 2026",
        "{COMPANY} new entrant OR displace threat {INDUSTRY} 2026",
        "{TICKER} competitor design win 2026",
        "{COMPANY} vs {INDUSTRY} peers market share trend 2025 2026"
      ],
      "affects": ["moat_trend", "thesis.H", "thesis.R"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "customer_second_source",
      "name": "客戶 second-source 與 in-house",
      "question": "最大客戶是否正在導入第二供應商，或將此環節自製（in-house）？",
      "queries": [
        "{TICKER} {COMPANY} largest customer second-source OR in-house 2026",
        "{CUSTOMERS} custom chip OR component second source agreement 2026",
        "{COMPANY} single-source risk customer diversify supplier",
        "{CUSTOMERS} in-house design OR insourcing {INDUSTRY} 2026"
      ],
      "affects": ["moat_trend", "thesis.R", "decision_inputs.bear"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "customer_concentration_credit",
      "name": "客戶集中度與客戶信用",
      "question": "前幾大客戶占營收比重多高？該客戶自身信用/財務狀況是否惡化？",
      "queries": [
        "{TICKER} {COMPANY} top customer revenue concentration 10-K 2026",
        "{CUSTOMERS} credit rating OR balance sheet stress 2026",
        "{COMPANY} customer concentration risk disclosure",
        "{CUSTOMERS} bankruptcy OR downgrade OR guidance cut 2026"
      ],
      "affects": ["thesis.R", "decision_inputs.bear", "triggers"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "supply_demand_durability",
      "name": "供需 durability",
      "question": "當前供需失衡（緊缺或過剩）是結構性還是週期性？能撐多久？",
      "queries": [
        "{INDUSTRY} shortage OR oversupply structural OR cyclical 2026 2027",
        "{INDUSTRY} supply discipline new capacity timeline",
        "{TICKER} {COMPANY} product demand durability structural 2026",
        "{INDUSTRY} demand outlook 2027 2028 consensus"
      ],
      "affects": ["decision_inputs.bear", "valuation", "moat_trend"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "regulatory_antitrust",
      "name": "法規／反壟斷",
      "question": "本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？",
      "queries": [
        "{TICKER} {COMPANY} antitrust OR monopoly investigation 2026",
        "{COMPANY} regulation OR regulatory scrutiny {INDUSTRY} 2026",
        "{TICKER} {COMPANY} DOJ OR FTC OR EU competition 2026"
      ],
      "affects": ["thesis.R", "decision_inputs.bear"],
      "na_allowed": true,
      "na_needs_reason": true
    },
    {
      "id": "reg_tariff_export",
      "name": "關稅／出口管制",
      "question": "本標的的產品、供應鏈或客戶是否暴露在關稅或出口管制變動下？",
      "queries": [
        "{TICKER} {COMPANY} tariff section 232 2026",
        "{COMPANY} export control OR entity list {INDUSTRY} 2026",
        "{TICKER} {COMPANY} China tariff OR trade restriction 2026",
        "{INDUSTRY} tariff exposure supply chain 2026"
      ],
      "affects": ["thesis.R", "decision_inputs.bear", "valuation"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "geo_supply_chain",
      "name": "地緣與供應鏈單點",
      "question": "生產地或關鍵供應鏈環節是否集中在地緣風險區域？是否有單點失效風險？",
      "queries": [
        "{TICKER} {COMPANY} manufacturing location geopolitical risk 2026",
        "{COMPANY} supply chain single point of failure {INDUSTRY}",
        "{TICKER} {COMPANY} Taiwan OR China OR geopolitical exposure 2026",
        "{INDUSTRY} supply chain concentration risk 2026"
      ],
      "affects": ["thesis.R", "decision_inputs.bear"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "end_markets",
      "name": "各主要終端市場",
      "question": "此營收段的需求動能、市佔與價格走向為何（依 §3 營收段逐一列，per_segment 展開）？",
      "queries": [
        "{TICKER} {COMPANY} {SEGMENT} segment revenue growth 2026",
        "{SEGMENT} end market demand outlook 2026 2027",
        "{COMPANY} {SEGMENT} market share OR pricing trend 2026",
        "{SEGMENT} {INDUSTRY} TAM growth consensus"
      ],
      "affects": ["thesis.H", "growth", "valuation"],
      "na_allowed": false,
      "na_needs_reason": true,
      "per_segment": true
    },
    {
      "id": "substitute_technology",
      "name": "替代技術",
      "question": "是否存在正在崛起、可能取代本標的核心產品/技術的替代方案？",
      "queries": [
        "{COMPANY} product substitute technology threat 2026",
        "{INDUSTRY} alternative technology disruption 2026 2027",
        "{TICKER} {COMPANY} technology obsolescence risk",
        "{INDUSTRY} next-generation technology roadmap 2026"
      ],
      "affects": ["moat_trend", "thesis.R"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "channel_business_model_shift",
      "name": "通路／商業模式轉移",
      "question": "銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？",
      "queries": [
        "{COMPANY} distribution channel disruption OR shift 2026",
        "{TICKER} {COMPANY} business model transition subscription OR platform 2026",
        "{INDUSTRY} channel disintermediation D2C 2026",
        "{COMPANY} go-to-market change 2026"
      ],
      "affects": ["moat_trend", "thesis.H"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "capital_markets_pricing",
      "name": "資本市場定價",
      "question": "當前市場共識 vs 公司自身 guidance 是否有落差？分析師目標價的 as-of 與分布為何？",
      "queries": [
        "{TICKER} {COMPANY} analyst consensus vs guidance 2026",
        "{TICKER} price target analyst consensus 2026",
        "{TICKER} {COMPANY} guidance raise OR cut 2026",
        "{TICKER} sell-side estimate revision 2026"
      ],
      "affects": ["valuation", "decision_inputs.signal"],
      "na_allowed": false,
      "na_needs_reason": true
    },
    {
      "id": "major_events",
      "name": "重大事件（QC-19）",
      "question": "近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？",
      "queries": [
        "{TICKER} {COMPANY} acquisition merger 2025 2026",
        "{TICKER} {COMPANY} class action lawsuit securities fraud",
        "{TICKER} {COMPANY} clinical trial FDA approval 2025 2026",
        "{TICKER} {COMPANY} product launch recall warning letter",
        "{TICKER} {COMPANY} SEC investigation restatement"
      ],
      "affects": ["thesis.R", "decision_inputs", "triggers"],
      "na_allowed": false,
      "na_needs_reason": true
    }
  ],
  "by_archetype": {
    "品質複利成長": [],
    "循環/商品": [
      {
        "id": "cyclical_supply_discipline_capacity",
        "name": "供給紀律與新產能時程",
        "question": "同業是否有紀律地控制新增產能？未來 12-24 個月的新產能開出時程為何？",
        "queries": [
          "{INDUSTRY} new capacity timeline 2026 2027",
          "{INDUSTRY} supply discipline capex plan 2026",
          "{COMPANY} peers capacity expansion announcement 2026"
        ],
        "affects": ["decision_inputs.bear", "valuation"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "cyclical_inventory_price_position",
        "name": "庫存與價格週期位置",
        "question": "當前處於庫存去化/回補的哪個階段？現貨/合約價格趨勢方向為何？",
        "queries": [
          "{INDUSTRY} inventory destocking OR restocking 2026",
          "{INDUSTRY} spot price OR contract price trend 2026",
          "{COMPANY} channel inventory level 2026"
        ],
        "affects": ["decision_inputs.bear", "valuation"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "cyclical_prior_downcycle_behavior",
        "name": "上一輪下行的實際價格行為",
        "question": "上一次產業下行時，價格/毛利率實際跌到什麼程度、持續多久？",
        "queries": [
          "{INDUSTRY} previous downturn price decline history",
          "{COMPANY} margin trough previous cycle",
          "{INDUSTRY} cycle length historical pattern"
        ],
        "affects": ["decision_inputs.bear"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ],
    "未獲利高成長": [
      {
        "id": "unprofitable_nrr_rule40_band",
        "name": "NRR／Rule of 40 同業帶",
        "question": "本標的 NRR 與 Rule of 40 在同業帶中排名為何？",
        "queries": [
          "{TICKER} {COMPANY} net revenue retention NRR 2026",
          "{COMPANY} Rule of 40 peers comparison 2026",
          "{INDUSTRY} SaaS peers NRR benchmark 2026"
        ],
        "affects": ["thesis.H", "decision_inputs"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "unprofitable_dilution_trajectory",
        "name": "稀釋軌跡",
        "question": "股數年增率與 SBC 佔營收比重的走向為何？是否有失控跡象？",
        "queries": [
          "{TICKER} {COMPANY} share count dilution SBC 2026",
          "{COMPANY} stock-based compensation revenue percent 2026",
          "{TICKER} diluted shares outstanding trend 2026"
        ],
        "affects": ["decision_inputs.bear", "triggers"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "unprofitable_path_to_profitability",
        "name": "轉正路徑",
        "question": "FCF/GAAP 轉正的具體時程與依據為何（guidance／模型推導）？",
        "queries": [
          "{TICKER} {COMPANY} path to profitability FCF positive timeline",
          "{COMPANY} guidance breakeven OR profitable 2026 2027",
          "{TICKER} cash runway burn rate 2026"
        ],
        "affects": ["thesis.H", "decision_inputs.bear"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ],
    "金融": [
      {
        "id": "financial_capital_credit_cycle",
        "name": "資本／信用週期",
        "question": "當前信用循環處於哪個階段？NPL/NCO 走向與撥備覆蓋是否惡化？",
        "queries": [
          "{TICKER} {COMPANY} NPL NCO credit quality trend 2026",
          "{INDUSTRY} credit cycle stage 2026",
          "{COMPANY} loan loss provision coverage 2026"
        ],
        "affects": ["decision_inputs.bear", "triggers"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "financial_regulatory_capital_rules",
        "name": "監管資本規則變動",
        "question": "CET1／Solvency II 等監管資本要求是否有變動風向？",
        "queries": [
          "{TICKER} {COMPANY} CET1 ratio regulatory requirement 2026",
          "{INDUSTRY} Basel OR Solvency II rule change 2026",
          "{COMPANY} regulatory capital buffer 2026"
        ],
        "affects": ["decision_inputs.bear", "triggers"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ],
    "轉機/特殊情境": [
      {
        "id": "turnaround_catalyst_timeline",
        "name": "重整／資產處分催化劑真實性與時程",
        "question": "重整/處分/新管理層等催化劑是否已有具體時程與進度證據，而非管理層口頭承諾？",
        "queries": [
          "{TICKER} {COMPANY} restructuring OR divestiture progress 2026",
          "{COMPANY} new management turnaround plan milestone 2026",
          "{TICKER} {COMPANY} debt restructuring timeline 2026"
        ],
        "affects": ["thesis.H", "triggers"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "turnaround_liquidation_floor",
        "name": "清算價值／資產底下修風險",
        "question": "資產底/清算價值估計是否穩固，還是本身也有下修風險（減損、資產品質惡化）？",
        "queries": [
          "{TICKER} {COMPANY} asset impairment OR write-down 2026",
          "{COMPANY} liquidation value OR book value quality 2026",
          "{TICKER} {COMPANY} balance sheet asset quality 2026"
        ],
        "affects": ["decision_inputs.bear", "valuation"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ],
    "受監管公用/穩定內需": [
      {
        "id": "regulated_rate_case_roe",
        "name": "費率案（rate case）結果與時程／准許 ROE 風向",
        "question": "近期或待決的費率案結果、准許 ROE 走向為何？是否有下修跡象？",
        "queries": [
          "{TICKER} {COMPANY} rate case decision 2026",
          "{COMPANY} allowed ROE regulatory outcome 2026",
          "{TICKER} {COMPANY} rate base growth filing 2026"
        ],
        "affects": ["thesis.H", "decision_inputs.bear"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ],
    "EMS/ODM": [
      {
        "id": "ems_utilization_capex_cycle",
        "name": "稼動率與資本支出週期",
        "question": "當前產能稼動率位置與資本支出週期階段為何？是否有新產能開出稀釋 ROIC 的風險？",
        "queries": [
          "{TICKER} {COMPANY} capacity utilization rate 2026",
          "{COMPANY} capex plan new facility 2026",
          "{INDUSTRY} EMS ODM utilization trend 2026"
        ],
        "affects": ["decision_inputs.bear", "valuation"],
        "na_allowed": false,
        "na_needs_reason": true
      },
      {
        "id": "ems_roic_asset_turnover_benchmark",
        "name": "ROIC 與資產週轉同業對比",
        "question": "本標的 ROIC 與資產週轉率在 EMS/ODM 同業中排名為何（毛利結構性薄，不用毛利率當品質基準）？",
        "queries": [
          "{TICKER} {COMPANY} ROIC asset turnover peers comparison 2026",
          "{INDUSTRY} EMS ODM ROIC benchmark 2026",
          "{COMPANY} CCC cash conversion cycle 2026"
        ],
        "affects": ["decision_inputs", "moat_trend"],
        "na_allowed": false,
        "na_needs_reason": true
      }
    ]
  }
}
```
