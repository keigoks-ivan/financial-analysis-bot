# stock-analyst v14.7 — archetype-gatesets.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

### QC-44｜金融 archetype gate-set（v14.1 Stage 2;JPM 原型驗證;bank / insurer / broker 子型）

**WHY**:成長股 gate 對 balance-sheet 金融**整組失效**——JPM 實證:FCF = **−$148B**（成長銀行 OCF 結構性為負）、`debtToEquity` None（算不出;raw debt $1.3T 是存款/funding）、`enterpriseToEbitda` None、grossMargins 0、Capex 不在表上、ROA 1.27%「看似差」實為銀行常態。**唯一能用的右錨是 P/TBV**（P/B 2.58）+ ROE 16.5%，而 §11 主錨卻是 PE/PEG/EV-EBITDA。

當 §0 archetype = 金融，§5/§11/QC-31/§6 **改用下列 gate-set**（明寫在報告，QC-43 路由）:

**§5 門檻組（金融）**:
| 成長股 gate | 金融替代 | 達標基準 |
|:---|:---|:---|
| FCF Margin | **ROTCE 有形權益報酬** | > 15%（穿越循環） |
| ROIC | **ROE 且 > 權益成本（COE ~10%）** | ROE > 12-15% |
| 10Y ROIC 穩定 | **跨信用循環 ROTCE 穩定**（含 2008/2020 壓力年） | 壓力年仍正 / 不破底 |
| 毛利率定價 | **NIM 趨勢 + 效率比（cost/income）** | 效率比 < ~60% |
| Capex/Rev | **不適用** → operating leverage / 效率比改善 | — |
| EPS CAGR > 20% | **EPS + TBVPS 複合 + 股息（總回報）** | ~10-12% 即優（金融非 20% 機器） |
| PEG | **P/TBV vs ROTCE**:Warranted P/TBV =（ROTCE−g）/（COE−g） | 實際 P/TBV ≤ warranted |
| D/E < 0.7 | **不適用** → **CET1 ratio** | > 監管要求 + 緩衝（~11-13%） |
| 負債安全性 | **NPL/NCO 趨勢 + 撥備覆蓋 + CET1 緩衝** | 信用品質穩、撥備足 |

**§11 估值主錨（金融）**:**P/TBV 分位 + P/E**;用 Warranted P/TBV 判貴賤;**EV/EBITDA 拿掉**（銀行 None）。
**QC-31 signal（金融）**:X 觸發改 ROTCE 跨循環 < COE / CET1 跌破監管 / NPL·NCO 結構惡化 / 重大舞弊;移除 FCF·NI、EV-EBITDA、Capex 觸發。
**§6 跑道（金融）**:放款·存款·AUM 成長 + 費收業務（財管/IB）+ 市佔，非 TAM 滲透。

**子型（§0 secondary 細分）**:
- **bank**（JPM）:CET1 / NIM / 效率比 / NPL·NCO / ROTCE / P-TBV
- **insurer**（如 PGR / CB / Allianz `ALV.DE`;**注意:US 掛牌 `ALV` = Autoliv 汽車安全件＝循環工業，非保險，勿誤歸**）:**combined ratio < 100%** / float / Solvency II ratio / book value / ROE;**不看 NIM/CET1**
- **broker·交易所**（HOOD）:ARPU / AUC / take rate / 活躍戶;偏 fintech，常與「未獲利高成長」blend
- **支付網絡**（MA）:**不歸金融**——資產輕高複利，走 `品質複利`

**batch script 補搜**（金融 archetype 啟動時加一組強制 web/10-K，類 QC-19）:`[ticker] CET1 ratio NIM efficiency ratio ROTCE`（bank）/ `[ticker] combined ratio Solvency II book value`（insurer）。yfinance `.info` 給 ROE/ROA/P-B/股息，但 CET1/NIM/效率比/NPL/ROTCE/TBV **給不出**。

**反灌水**:金融 gate-set 不是新增冗章，是**把 §5/§11/QC-31 既有格子換成金融正確指標**;產出長度同等，只是尺對了。

### QC-45｜未獲利高成長 archetype gate-set（v14.1 Stage 3;MDB 原型驗證）

**WHY**:成長股 gate 對 GAAP 未獲利的高成長 SaaS 失效——MDB 實證:trailing EPS −$0.37 / Diluted EPS −1（負）→ §5 EPS-CAGR 負基期 undefined、PEG undefined、trailingPE None、EV/EBITDA −304、ROE/ROA 負;**但公司健康**:GM 72%、FCF +$500M（margin 20.3%）、營收成長 25.2% → Rule-of-40 = 45.5%。**最毒的是 QC-31 X 觸發 FCF/NI<0.5:NI 負 → FCF/NI = −7.0 < 0.5 → 機械把健康公司判迴避。**

當 §0 archetype = 未獲利高成長，§5/§11/QC-31/§6 **改用下列 gate-set**（QC-43 路由）:

**§5 門檻組（未獲利高成長）**:
| 成長股 gate | 替代 | 達標基準 |
|:---|:---|:---|
| EPS CAGR > 20% | **Rule-of-40**（營收成長% + FCF margin%） | ≥ 40 |
| PEG < 2 | **EV/S ÷ 營收成長**（growth-adjusted）或 EV/gross-profit | growth-adjusted 合理 |
| ROIC > 15%（GAAP 負無意義） | **NRR + 毛利率 + 增量 OI margin 改善軌跡** | NRR > 110% / GM > 65-70% |
| FCF Margin > 15% | **FCF margin + 轉正軌跡**（已正:看 margin 升;未正:現金跑道 + 明確轉正路徑） | FCF 升軌或跑道足 |
| 體質 FCF/NI | **NI 負時 FCF/NI 比無意義** → 改看 FCF margin 絕對值 + 淨現金 + 跑道 | FCF 正 或 跑道 > 12 個月 |

**§11 估值主錨（未獲利）**:**EV/S（+ EV/gross-profit）+ Rule-of-40-adjusted**;轉正後接 forward P/E;**trailing PE / PEG 拿掉**（負 EPS undefined）。
**QC-31 signal（未獲利）**:**不因 GAAP NI 負觸發 X**;X 改:NRR 跌破 100% / Rule-of-40 < 20 連 2 季 / 毛利結構崩 / 現金跑道 < 12 個月且無轉正路徑 / SBC 稀釋失控（股數 > 10%/yr 無營收槓桿）。
**§6 跑道（未獲利）**:NRR + 淨增客戶 + TAM 滲透 + SBC-adjusted 轉正時程（非 EPS 外推）。
**blend 提醒**:fintech broker（HOOD）常 = 金融 × 未獲利，兩套都跑、標背離。
**反灌水**:換尺不增章;Rule-of-40 / NRR / FCF margin 須 sourced 真數字。

### QC-46｜轉機 + 受監管公用事業 gate-set（v14.1 Stage 4;低密度，模型 prose 為主）

**WHY**:這兩類較少且模型 prose 已能處理八成，故給**輕量尺**不展開大表;重點是別硬套成長複利 gate。

**轉機/特殊情境**（深度價值 / 重整 / 分拆 / activist）:
- §5/§11 主錨 → **資產重估 / SOTP（分部加總）/ normalized earning power / P-TBV**，非成長外推;EPS-CAGR/PEG 不適用（盈餘受抑或為負）。
- §3.F Single Thing → **轉機觸發**（債務重組完成 / 出售虧損部門 / 新管理層 / catalyst 里程碑），非「moat 擴張」。
- §6/§7 → 「為何現在會轉」的 catalyst + 下行保護（資產底 / 清算價值），非 TAM/runway。
- QC-31 X → 流動性危機（跑道 < 12 個月 + 無再融資）/ 重整失敗 / 治理舞弊。

**受監管公用 / 穩定內需**（utility / regulated / staple）:
- §5/§11 主錨 → **DDM / 殖利率 + 股息成長 / regulated ROE（rate base × allowed ROE）/ P/B**;PEG/高成長門檻不適用（個位數成長為常態）。
- §6 成長 → **rate base 成長 + 費率案（rate case）+ 准許 ROE**，非 TAM 滲透。
- §7 護城河 → 監管特許 / 天然獨佔（single-axis，同 QC-44 §7 單軸 escape）。
- 產業態勢 → QC-39「態勢靜態」即可（已有）。
- QC-31 X → 准許 ROE 結構下調 / 費率案連敗 / 監管轉敵 / 過度槓桿（利率敏感）。

**反灌水**:此兩類**不強制長表**，但換尺與 catalyst/下行保護必須 sourced。模型若判標的明顯屬此兩類，§0 標明並用上述主錨，不硬跑成長 gate。

