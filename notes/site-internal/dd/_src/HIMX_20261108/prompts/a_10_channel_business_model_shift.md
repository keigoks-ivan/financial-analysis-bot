你是 stock-analyst v20 DD 的證據採集子 agent。標的：HIMX。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 4 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[channel_business_model_shift] 通路／商業模式轉移
Q: 銷售通路或商業模式（如訂閱化、D2C、平台化）是否正在結構性轉變？
  - Himax Technologies distribution channel disruption OR shift 2026
  - HIMX Himax Technologies business model transition subscription OR platform 2026
  - Semiconductors channel disintermediation D2C 2026
  - Himax Technologies go-to-market change 2026


## 規則（嚴格遵守，違反視為無效輸出）
1. **只回 sourced claim**：每條 finding 必須有可查證的 source（URL 或明確可搜尋到的來源名＋標題）與 as_of（該資訊的發布/生效日期，非你查詢的日期）。
2. **查不到就 status="none"**，並列出你實際下過的 queries_run（至少 1 條，需與你實際搜尋詞一致，不得事後編造）。軸清單裡的 `queries` 是起點不是配額，同一次搜尋的來源可同時支撐多個軸。**不得因為查無所獲就用訓練知識/常識填 claim。**
3. **三種狀態不得混用**：found＝有 sourced claim；none＝軸適用於本標的業態、但搜尋查無來源；not_applicable＝該軸對本標的業態根本不成立（例：銀行沒有「最大客戶導入第二供應商」、零售商的客戶是終端消費者）。**軸對此業態不適用時回 not_applicable 並在 note 寫理由，不要回 none。**只有軸物件標 na_allowed=true 才可回 not_applicable，沒標的軸只能 found 或 none；拿不準是否適用就當適用、照常搜尋，不要用 not_applicable 省搜尋。
4. **不臆測、不外推**：claim 只寫你實際找到的事實，不要自己推論「這意味著」，那是判斷層的工作。
5. direction 欄：這條 finding 對本標的是正面(+)／中性(0)／負面(-)，僅標事實方向，不要寫成裁決語。
6. affects 欄：這條 finding 影響哪些判斷面（可填 moat_trend／thesis.H／thesis.R／decision_inputs.bear／valuation／triggers 等，可複選）。
7. **現價一律引 `numbers.price_at_dd`／`price_as_of`，不得自行寫「現價」數字**：市值、距 52 週高低點 %、目標價 vs 現價，一律引用該欄，不從聚合站另抓現價字面數字。
8. **原始證據與解讀分開存**：每條 finding 另填三欄——`url`（實際讀到的網址，沒有就填 null）、`excerpt`（從該來源**逐字複製**、支撐 claim 的原文，≤300 字，不得改寫或翻譯）、`excerpt_from`（`snippet`＝搜尋摘要／`page`＝WebFetch 讀到的頁面）。`claim` 是你對原文的精簡轉述；`excerpt` 是證據本身。找不到可逐字複製的原文就填 null，不要自己寫一句當原文。

## 程式已抓好的一手文件摘錄（本軸）
以下為程式抓取的一手文件摘錄，可直接逐字引用（附 url 與 as_of）：
- 引用時 finding 的 `url`、`as_of` 照該則標示填；`source` 寫「來源＋文件」；`excerpt` 從「<<<」「>>>」之間**逐字複製**（≤300 字，取最能支撐 claim 的連續一段，不改寫、不翻譯）；`excerpt_from` 填 `"page"`。
- 一手清單顯示沒有某類事件時（例如「標題含關鍵字者 0 則」），可據此寫一條「經查一手紀錄無此類事件」的 finding（status=found、direction=`"0"`），excerpt 用清單本身那一句統計；不要因為沒找到事件就標 none。
- 這些摘錄不算你的搜尋：`queries_run` 只記你自己實際下過的搜尋；摘錄仍可另外搜尋補充，但不必為了湊證據重搜摘錄已涵蓋的內容。
- 摘錄與本軸問題無關或不足以回答時，照常搜尋；仍查不到才記 none。

[1] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 4. Information on the Company｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
● Resolution and Number of Channels. Resolution refers to the number of pixels per line multiplied by the number of lines, which determines the level of fine detail within an image displayed on a panel. For example, a color display screen with 1,024 x 768 pixels has 1,024 red columns, 1,024 green columns and 1,024 blue columns for a total of 3,072 columns and 768 rows. The red, green and blue columns are commonly referred to as “RGB.” Therefore, the display drivers need to drive 3,072 column outputs and 768 row outputs. The number of display drivers required for each panel depends on the resolution of the panel and the number of channels per display driver. For example, an XGA (1,024 x 768 pixels) panel requires eight 384-channel source drivers (1,024 x 3 = 384 x 8) and three 256-channel gate drivers (768 = 256 x 3), while a full HD (1,920 x 1,080 pixels) panel requires eight 720-channel source drivers and four 270-channel gate drivers. The number of display drivers required can be reduced by using drivers with a higher number of channels. For example, a full HD panel can have six 960-channel source drivers instead of eight 720-channel source drivers.…

The following table summarizes the features of our Electronic Paper Display (EPD) solutions: ​ Product ​ ​ ​ Features Electronic Paper Display (EPD) Source Drivers ​ ● Features 320 to 1296 output channels ● output driving voltage ranging from 15 up to 55v ● input logic voltage ranging from standard 3.3V to low power 1.8V ● low power consumption and low EMI ● support TTL, mini-LVDS cascade modulated driver interface, or MIPI high-speed interface and customized interface technologies ● support COF and COG package types ​ ​ ​ Electronic Paper Display (EPD) Gate Drivers ​ ● 100 to 972 output channels ● output driving voltage ranging from 10 up to 70v ● input logic voltage ranging from standard 3.3V to low power 1.8V low power consumption ● support COF and COG package types ​ ​ ​ Electronic Paper Display (EPD) Timing Controller ​ ● Support MIPI 4 lane input interface ● Support TTL, mini-LVDS output interface ● Support maximum resolution 3840x2160 ● Use USB3.0/SPI/I2C control interface ● Fast full-color image update based on 32 palette colors ● Support LPDDR2 memory ​ ​ ​ Electronic Shelf Label (ESL) Integrated Drivers ​ ● Highly integrated chip embedded with source driver and gate driver, timing controller and power circuit ● Source driver output driving voltage ranging up to 30V ● Support COG package types ​ Touch Controller ICs We offer touch controller solutions for capacitive touch panels.…

34 Table of Contents Power Management ICs A power management IC integrates several power components to fulfill system power requirements. It may include step-up or step-down pulse width modulation, or PWM, DC-to-DC converters, low-dropout regulators, or LDO regulators, voltage detectors, operational amplifiers, p-gamma OP, level shifters, and/or other components. For panel module applications, a power management IC provides a reliable and precise voltage for source drivers, gate drivers, timing controllers, and panel cells. Moreover, its built-in over-temperature and over-current protections help prevent components from being damaged under certain abnormal conditions. As integrating an increasing number of components into a power management IC is likely to be a continuing trend, we believe power management ICs will continue to be critical components of a TFT-LCD and OLED panel module. The following table summarizes certain features of our power management IC products: ​ ​ Product ​ ​ ​ Features Integrated Multi-Channel Power Solutions for TFT-LCD and OLED Notebooks ​ ● PMIC, PGOP 2-in-1 and Level Shifter ● 2ch programmable gamma voltage inside ● PAVDD Synchronous Boost Converter ● NAVDD Synchronous Inverting Converter ● VGH / VGL Synchronous SIBO Converter ● 3ch Vint OP for OLED Panel ● built-in power MOSFET ● step-up PWM converter ● charge pump regulator ● LDO regulator ● programmable voltage detector ● gate pulse modulator ● Vcom operational amplifier ● I2C programmable ● low frame rate control for power saving solution ● built in UVLO, UVP, OVP, SCP and OTP protection ​ ​ ​ Integrated…

​ ​ Product ​ ​ ​ Features 10- channel output level shifter for GOA TFT-LCD ​ ● Support 1 or 2 or 6 input and 4/6/8/10 clock channel output ● 2 channel STV ● 2 channel LC ● Reset and charge sharing function ● OTP/ SCP and OCP function by I2C or Resistor adjustment ​ Mini LED Backlight Driver Mini LED backlight driver ICs play a critical role in controlling thousands or even tens of thousands of mini-LEDs within backlight system. Their core function is local dimming, enabling precise brightness control of individual zones to deliver high contrast, high brightness, wide color gamut, and energy saving. These driver ICs convert processor signals into current outputs to precisely regulate LED emission. They support high scanning rates, built-in MOSFETs, multi-channel operation, PWM dimming, and fault and error detection.

​ 46 Table of Contents We primarily sell our products through our direct sales teams located in Taiwan, China, South Korea. We also have dedicated sales teams for certain of our most important current or prospective customers. We have offices in Tainan, Hsinchu, Taipei, Taiwan; and Shenzen and Suzhou, China. We have other sales and technical support offices in Hefei, Beijing, Shanghai, Fuzhou, Foshan, Fuqing, Ningbo, Wuhan, Nanjing, Chongqing, Chengdu, Xi’an and Xiamen, China; Asan-si and Bundang-gu, South Korea and Irvine and San Jose, California, Minneapolis, Minnesota and Detroit, Michigan, USA, all in close proximity to our customers. For certain products or regions, we may sell our products through agents or distributors.
>>>

[2] 來源：SEC EDGAR｜文件：20-F（FY2025，申報 2026-03-27）｜章節：Item 5. Operating and Financial Review｜url：https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm｜as_of：2026-03-27
<<<
Product Mix The proportion of our revenues that is generated from the sale of different product types, also referred to as product mix, also affects our average selling prices, revenues and profitability. Our display driver products vary depending on, among other things, the number of output channels, the level of integration and the package type. Variations in each of these specifications could affect the average selling prices of such products. For example, the trend for display drivers for use in large-sized panels is toward products with a higher number of channels, which typically command higher average selling prices than traditional products with a lower number of channels. However, panels that use higher-channel display drivers typically require fewer display drivers per panel. As a result, our profitability will be adversely affected to the extent that the decrease in the number of display drivers required for each panel is not offset by increased total unit shipments and/or higher average selling prices for display drivers with a higher number of channels. The level of integration of our display drivers also affects average selling prices, as more highly integrated chips typically have higher selling prices. Additionally, average selling prices are affected by changes in the package types used by our customers.…
>>>


## 回傳格式（嚴格 JSON 契約，不得夾雜其他文字；一次 Write）
```json
{
  "coverage": {
    "<axis_id>": {
      "status": "found|none|not_applicable",
      "queries_run": ["...", "..."],
      "findings": [
        {"claim": "...", "source": "...", "url": "https://...", "excerpt": "逐字原文…", "excerpt_from": "snippet|page", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"]}
      ],
      "note": "",
      "clues": [
        {"claim": "...", "source": "...", "url": "https://...", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"], "match_terms": ["預期原文逐字出現的字串", "..."]}
      ]
    }
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到就升級成帶原文的 finding；找不到（或頁面打不開）就照 `excerpt_from: "snippet"`、`excerpt: null` 的 finding 保留，並標為未核原文。
- 只有 clues、findings 是空的時，`status` 填 `none`（程式核實到原文後會自動改成 `found`）。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/parts/axes_10.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 4 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
