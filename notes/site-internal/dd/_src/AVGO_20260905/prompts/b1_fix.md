你是 stock-analyst v17 判斷 agent，回來做一輪定點修正。標的 AVGO（20260905）。

`judge check` 的失敗原文如下，**只准改被點名的欄位**，改完一次 Write 整檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/judgment.json`，重跑：

```
python3 scripts/ddreport.py judge check AVGO 20260905
```

≤1 輪；仍 FAIL 就照實回報。

## judge check 失敗原文

```
[dd_scenario.py] rc=0
AVGO 情境樹（2026-09-05，現價 357.9，起始 FY2027E EPS 19.33 @ 18.51x，終端年 FY2031E）
----------------------------------------------------------------------------------------------------
[BULL ] 終端EPS=60.00  終端倍數=26.0x  5Y目標價=1,560.0  5Y%=+335.9%  不含息IRR=+34.2%/yr  機率=30%
         EPS貢獻=+25.4%/yr  re-rate=+7.0%/yr  股息回購=+1.0%/yr  不含息合計=+34.2%/yr  含息合計=+35.2%/yr
         依據：FY27 AI 營收超過 $115B 指引、FY28 $230B 如期；Google 訓練 TPU 主設計權延續至 v10；OpenAI／Anthropic 10GW＋8GW 承諾如約出貨；半導體分部營業利益率守 60%；終端 26x（低於 NVDA 現值溢價，反映客製代工形態折價）
[BASE ] 終端EPS=39.50  終端倍數=20.0x  5Y目標價=790.0  5Y%=+120.7%  不含息IRR=+17.2%/yr  機率=40%
         EPS貢獻=+15.4%/yr  re-rate=+1.6%/yr  股息回購=+1.0%/yr  不含息合計=+17.2%/yr  含息合計=+18.2%/yr
         依據：FY27 取共識 19.33；FY28 對 $230B 指引打八折（Google 份額 95→80→65 稀釋＋backlog 兌現時程）；FY29 起 AI 資本支出增速降至 15-20%、非 AI 半導體與軟體低雙位數；終端 20x＝成熟複利股倍數
[BEAR ] 終端EPS=15.00  終端倍數=12.0x  5Y目標價=180.0  5Y%=-49.7%  不含息IRR=-12.8%/yr  機率=30%
         EPS貢獻=-4.9%/yr  re-rate=-8.3%/yr  股息回購=+1.0%/yr  不含息合計=-12.8%/yr  含息合計=-11.8%/yr
         依據：2028 雲端 AI 資本支出消化期撞上 Google 推論份額轉 MediaTek／Marvell；OpenAI 融資斷鏈使 10GW 承諾縮水、XPV 表外平台信用惡化；EPS 自 FY27 高點回落至 15，市場改以循環股 12x 定價（依 searched durability：CoWoS 缺口 2026 底縮至 10%、供給可逆性高，非 pattern 外推）
----------------------------------------------------------------------------------------------------
機率加權：EV5y=+134.2%  年化=+18.5%/yr  AR=6.8
估值依賴型：否
Guardrail 自洽差：0.01pp（(1+EPS)(1+re-rate)-1 vs 不含息IRR，≤0.1pp 為自洽）
----------------------------------------------------------------------------------------------------
⚠ WARN：base 不含息 IRR 17.2%/yr > 15%——罕見，須檢查機率分配是否過度樂觀
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/tables/e11.html
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/scenario_meta.json

[dd_decision.py run] rc=0
{
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
}
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/judgment.json（輸入含既有 decision_out：已合併機械欄，rearm_trigger/exec_line/人工requires_critic保留）
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/tables/audit.html

[validate_judgment.py] rc=0
[J3 --fix] judgment.json：套用 1 項修正
  ✓ scenario_ref 相對路徑 'scenario.json' → '/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AVGO_20260905/scenario.json'
[FAIL] judgment.json（6 FAIL／12 WARN）
  ✗ $.contradictions[12].axis: 機器語言外洩 'QC-5'（詞表 'QC-\\d'）—「…ID 對帳（QC-52）…」
  ✗ $.contradictions[13].axis: 機器語言外洩 'QC-5'（詞表 'QC-\\d'）—「…同形狀 peer 對帳（QC-51）…」
  ✗ 漂移未歸因：bull_5y_price（本次=None／前份=1560.0）— judgment.contradictions[] 找不到 prior_field='bull_5y_price' 或 axis 含 'bull_5y_price' token 的條目
  ✗ 漂移未歸因：p_bull_pct（本次=None／前份=30.0）— judgment.contradictions[] 找不到 prior_field='p_bull_pct' 或 axis 含 'p_bull_pct' token 的條目
  ✗ 漂移未歸因：p_bear_pct（本次=None／前份=30.0）— judgment.contradictions[] 找不到 prior_field='p_bear_pct' 或 axis 含 'p_bear_pct' token 的條目
  ✗ 漂移未歸因：rearm_trigger（本次='FY27 本益比 <15x（約 $290）且半導體分部營業利益率 ≥55%、共識 FY28 未連 2 次下修→加碼至衛星上限'／前份=None）— judgment.contradictions[] 找不到 prior_field='rearm_trigger' 或 axis 含 'rearm_trigger' token 的條目
  ⚠ triggers[0].action '重審護城河等級；等級降至 B 即觸強制迴避' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[2].action '結構性壓縮警示、減碼 1/3' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[3].action 'H2 降級、減碼' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[4].action 'H1 核心假設削弱、凍結加碼' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[5].action '表外槓桿重審、減碼' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[9].action '依階梯' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[10].action '重算成本吸收（合併毛利率 −2pp 為吸收失敗判定閘）' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[12].action '併入觸發器 4' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[13].action '集中度升 🔴、減碼' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[15].action '重跑 DD' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ scenario_ref 交叉檢查：dd-meta 缺 scenario_tree，無法重算比對（v15.2.1 起建議由 dd_scenario.py 產出）
  ⚠ J2｜缺 price_at_dd／bear_5y_price／premortem.max_dd.lo 任一，Max DD 恆等式略過
```
