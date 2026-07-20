# Critic Report — ID_AIInferenceEconomics_20260720.html（v3.0 首發 pilot）

- Reviewer：id-review cold-review critic（Sonnet，跨模型冷讀）
- Mode：ID v2 checklist（`skill_version: v3.0` ≥ v2.0 → id-review v1.6.1 dispatch 進 v2 mode；v3.0 呈現層＝八段 sell-side＋§N 內容模組映射，按 industry-analyst SKILL.md 映射表定位章節）
- 對照：前身 `ID_AIInferenceEconomics_20260430.html`（v2.3）；`sd_verdict`/`clock_phase`/`conviction`/`quality_tier` 三/四值維持不變，用戶已知會此為刻意決策，本次不對此本身提出異議，僅檢查「機器欄與新版內文是否真的同步」與「v3.0 新增決策支援模組是否為真分析非裝飾」。
- Verdict：**AT_RISK**（非 BROKEN——核心敘事與個股 tier 判斷方向合理、來源充足；問題集中在決策支援模組（資本週期／TAM 三角對帳／priced-in 溯源／kill metric 防套套）的量化落地不足，以及機器欄與內文的同步瑕疵——恰是這份 v3.0 pilot 作為未來範本前最該抓的一類問題）

---

## 🔴 CHANGES_CONCLUSION（7 條，建議 patch 前先處理）

### 🔴①　conviction 機器欄與 §0 PM 綠卡自相矛盾（V2-12）
id-meta `"conviction": "high"`（+ rating-strip 顯示 `HIGH`）vs 同一份文件、同一 §0 摘要層內的 PM Implication judgment-card 徽章明寫 `conviction：mid`（`<span class="badge is-mid">`，line 596）。兩處相隔僅幾十行，讀者/下游系統會拿到互相矛盾的 sizing 訊號。
- 依 industry-analyst SKILL.md 自己定義的 conviction pill 規則：`high` 需 `§9 ≥2 個🔴 且 §8 falsification 距離 >2σ`；`mid` 需 `≥1🔴 + 至少1條kill未排除`。本 ID 明文寫「NC#2（frontier inference 毛利升 70%）AT_RISK」——一條 kill 明確未排除，比較符合 `mid` 的定義。
- **建議處置**：把 id-meta `conviction` 與 rating-strip 改成 `mid`（與 PM 綠卡對齊），而非反過來把 PM 綠卡徽章改成 high——因為 AT_RISK 的 NC#2 這個事實不會因為改欄位而消失。

### 🔴②　sd_verdict="shortage" 把報告自己講的「分裂」裁決壓扁成單一值（V2-12）
§1 thesis 原文明寫：「commodity 推論『過剩 / 零毛利』，frontier + 垂直整合 ASIC『稀缺 / 守毛利』」——這是一個按子層分裂的裁決，不是單一「短缺」。
- industry-analyst SKILL.md 與 `scripts/validate_id_meta.py` 都明文為這種情境設計了 `sd_verdict="split"` + 必填的 `sd_verdict_detail`（「商業段與政府段等分段結論不一致時填 split...一句寫清哪段短缺哪段過剩」）。本 ID 完全命中這個設計場景，卻填了扁平的 `shortage`，也沒有 `sd_verdict_detail` 欄位。
- judgment-playbook 條目 10「裁決錨定瓶頸層」也預期報告要「先指認 binding constraint 在哪一層，並解釋與產品報價方向的異同（token 價跌與算力短缺並存）」——本 ID 有做這個分析的實質內容（分層敘事很清楚），只是沒有把結論正確寫回機器欄。
- **建議處置**：`sd_verdict` 改 `"split"`，新增 `sd_verdict_detail`（例如：「commodity 推論過剩／零毛利；frontier 推論＋垂直整合 custom ASIC 稀缺／守毛利」），下游獵場篩選鍵（`sd_verdict==shortage ∧ ...`）目前會把這份 ID 算進「短缺」獵場，掩蓋了 commodity 層過剩的另一半事實。

### 🔴③　V2-10 資本週期證據全無量化數字
3.5「供需裁決與三視野推估」開頭的資本週期三指標——① capex/折舊比、② ROIC vs WACC、③ 新產能 lead time——**三項全部零具體數字**，只有一個 `[A: WACC ~10% proxy]` 假設標籤，沒有任何一項給出真實 ROIC%、capex/折舊比趨勢值或 lead time 天數。V2-10 rubric 明文：0-1 項有數字 → 🔴。
- 這不是小事：本 ID 正落在 `sd_verdict=shortage ∧ clock_phase=II` 這個歷史校準唯一系統性失效格（`knowledge/calibration_id_20260707.md`，n=25、勝率 7/25、清一色 AI 硬體）——V2-13 存在的目的就是逼這類報告在這格拿出真證據，而這份報告目前沒有。

### 🔴④　V2-13 熱產業時鐘三問未被回答
對 `shortage×Phase II` 強制三問：① Phase II 判定依據是否為基本面週期證據——目前只有 ③ 的敘事化陳述，無量化證據（見上）；② 該族群 26 週漲幅/擁擠度證據是否指向更晚相位——**全文找不到任何 crowding / momentum / 估值歷史分位的交叉檢查**，GOOGL/AVGO/NVDA 目前股價相對其歷史估值帶落在哪裡完全沒討論；③ priced_in=mid 是否誠實——尚可（沒有「短缺+超漲卻標 low」的明顯紅旗），但因為①②都沒做，這個「誠實」判斷本身缺乏可驗證的基礎。

### 🔴⑤　V2-9 需求三角對帳只有 top-down，沒有 bottom-up
3.1「推論支出 TAM 三情境」表只給了單一 top-down 推導（「推論占算力 2/3 × 加速器 TAM 軌跡 + 服務層」），全文找不到「下游客戶 capex/採購 guidance 加總」vs「上游廠商營收 consensus 加總」的獨立第二條估算路徑做對帳。3.1 開頭的「需求三角驗證」表其實是 P×Q 恆等式拆解（單價×每task token×任務量），不是 V2-9 要求的 top-down vs bottom-up TAM 對帳——兩者容易被誤認成同一件事，但不是。

### 🔴⑥　V2-11 priced-in 檢驗四條分歧全無溯源分位數字
Debate 1-3 各有一行「Priced-in：...」敘述，但**沒有一條**附上具體估值分位（percentile / band 位置）或引用來源；Debate 4（中國 open-weight）甚至**完全沒有獨立的 Priced-in 段落**（其他三條都有明確的 `<strong>Priced-in</strong>：` 標籤，Debate 4 沒有）。rating-strip 的 `Priced-in: MID` 因此缺乏可回溯的量化支撐。

### 🔴⑦　V2-14 kill_metrics 套套邏輯 + 無獨立市場撮合價指標
`kill_metrics[]`（＝§5.2 證偽表）四條：① token 支出指數（第三方指數，尚可）② AI lab inference 毛利軌跡——其 bull 閾值「≥70%」**直接就是 Anthropic/OpenAI 自己揭露的目標數字**（Anthropic 2027、OpenAI 2029），這是 V2-14 明文警告的套套邏輯（該當 meet/miss 監測而非獨立門檻）③ agentic 滲透率——無揭露來源、口徑不明 ④ 垂直整合者 inference 單位成本優勢——GOOGL/AMZN 從不揭露 TPU/Trainium 單位成本，這條實務上不可裁決。**四條裡沒有一條是市場撮合價/實測價**（租價、現貨價、depletions 等），不符合 V2-14「整表至少一條為市場觀測數」的要求。

---

## 🟡 PARTIAL_IMPACT（6 條）

1. **V2-1 表格數量 11 張 > 硬上限 10 張**（文字比例 91.2% 遠優於 55% 下限，只有數量超標）。易修：把「推論經濟 kingmaker 技術」（3 列小表）併入前段敘事，或合併「推論各層 unit economics」與「推論供給三層」兩張結構相近的表。
2. **NC#1/NC#2/NC#3 標籤是孤兒引用**：rating-strip 與 PM 綠卡都引用「NC#1/NC#2/NC#3」，但 v3.0 已把舊 §7 Non-Consensus 改名為「Key Debates」且擴充成 4 條（Debate 1-4），文中找不到任何地方明講「NC#1=Debate 1」這種對應，讀者只能自己猜；Debate 4（中國 open-weight）完全沒被編進 NC 編號，也沒被列入 AT_RISK 名單（雖然文字結論說它「強化而非推翻」，方向上說得通，但編號系統本身沒跟上 v3.0 改版）。
3. **kill_metrics[] 的 `bear_threshold` 欄位是斷句殘片**（例如 `"Silicon Data 等）是否續升（單價跌但總支出升 = Jevons 維持；若總支出停滯 = 悖論失效）"`，開頭缺主語、多一個孤立的右括號）——四條全部都有這個毛病，從 v2.3 沿用至今未修。任何直讀機器欄渲染的下游頁面會顯示破碎句子給使用者看。
4. **judgment-playbook 條目 8「讓利永久性四判準」命中但未系統性作答**——本 ID 主題（持續讓利/中國價格戰/token 通縮）明確觸發此條，四項判準（持續多久／採用是否不對稱／是否已錨定客戶預期／是否有制度管道固化）的素材其實散落在報告各處（enterprise 30-46% 份額、OpenRouter 61% 都可支撐②「不對稱採用」），但沒有被收斂成明確的「週期折扣 vs 永久 reset」四點判定。
5. **V2-7 TAM bull/bear 乘數（base×1.2 / base×0.65）具名但未量化輸入**——exhibit-note 有指出偏離來自「agentic 乘數能否續升」這一個 input，但沒說 base/bull/bear 情境下這個乘數具體值差多少，仍偏黑盒。
6. **三視野表 5Y+ 欄位 trigger（「agentic 乘數天花板是否出現」）未給可量化閾值**，與 12M/3Y 兩欄（有具體指數/百分比錨點）不一致。

---

## 🟢 COSMETIC（2 條）

1. Kimi K3 本身的 serving 記憶體門檻沒有實算，只引用同廠上一代 K2.x（1T 參數）的 959GB/1,347GB vRAM 數字做代理——報告有誠實標注「同廠上一代」，不算誤導，但若能按 2.8T/1T 的參數比例做一個粗略換算（推論约 2.5-2.8×，即約 2.4-2.7TB 級）會更精確。
2. GOOGL 18% / AVGO 49% / NVDA 92% 純度推導已逐一用 WebSearch 對照官方財報驗證：
   - GOOGL：Google Cloud $20.03B ÷ Alphabet 總營收 $109.9B（2026Q1）＝ 18.2% ✓
   - AVGO：AI 半導體 $10.8B ÷ 總營收 $22.2B（FY2026 Q2）＝ 48.6% ✓
   - NVDA：Data Center $75.2B ÷ 總營收 $81.6B（FQ1'27）＝ 92.2% ✓
   三者數字準確、口徑揭露誠實（GOOGL/NVDA 均附「保守上界/未計入」類caveat）。**此項 CLEAN，僅供 audit trail 記錄，不需 patch。**

---

## 附：新增內容（中國 open-weight §3.3 + Debate 4）事實查核結果 — CLEAN

WebSearch 逐項核對以下數字，**全部與外部來源一致，無矛盾**：
- OpenRouter 中國 open-weight token 份額 ~61%（2026-05）✓（KuCoin/techtimes 等多源印證，雖 4-5 月間有 51%-61% 的區間波動，報告標注的 as-of 日期在合理範圍內）
- 中西同級模型定價倍差 ~7-34×（GLM-5.2 vs GPT-5.5 output ≈6.8×≈1/7；DeepSeek V4 Pro vs GPT-5.5 output ≈34.5×≈1/34，算術自洽）✓
- Kimi K3：2.8T 總參數、896 expert／16 啟動（1.8% 稀疏度，16/896=1.79% 算術正確）、$3/$15 定價（較 K2.6 $0.95/$4.00 漲約 3.16×/3.75×，與文中「約3倍」一致）、2026-07-16 發布 ✓（Bloomberg/Tom's Hardware/官方 blog 印證）
- TrendForce 2026Q1 DRAM 合約價 QoQ +90-95%、SK hynix 短缺展望至 2030 ✓（TrendForce 官方稿與多家媒體印證）
- as-of 標注齊全，§3.3 與 Debate 4 之間的敘述（K3 定價反轉、記憶體門檻不降反升）互相一致、無重複矛盾。

本節內容（新增最多的一塊）本身事實查核**沒有問題**；本次 🔴 findings 集中在既有的 v3.0 決策支援模組（資本週期／TAM對帳／priced-in／kill metric）與機器欄同步，而非中國 open-weight 這塊新內容本身。
