你是 stock-analyst v17 判斷 agent，回來做一輪定點修正。標的 TXN（20260907）。

`judge check` 的失敗原文如下，**只准改被點名的欄位**，改完一次 Write 整檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/judgment.json`，重跑：

```
python3 scripts/ddreport.py judge check TXN 20260907
```

≤1 輪；仍 FAIL 就照實回報。

## judge check 失敗原文

```
[error] 找不到 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/scenario.json

[dd_decision.py run] rc=0
{
  "verdict": "進場",
  "role": "核心",
  "row_hit": "10",
  "pacing": [],
  "holding_cap": null,
  "requires_critic": [
    "QC-41 產業態勢：裁決強方向（進場）＋moat_trend ↑＋法規敏感（中國關稅原產地規則、SAMR 審 SLAB）＋競爭動態（中國本土替代）→ 需跨模型複核；本檔三軸裁決＝雙向拉鋸偏結構轉好（B 軸 durability 週期性、C 軸法規變數活躍）"
  ],
  "audit_rows": [
    {
      "row": "1",
      "condition": "基本面評級 signal = X → 迴避",
      "hit": false,
      "basis": "signal='A'"
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
      "basis": "moat_trend='↑', moat='A'"
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
      "basis": "signal='A'"
    },
    {
      "row": "7",
      "condition": "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）",
      "hit": false,
      "basis": "runway_post_y5='🟢'"
    },
    {
      "row": "7a",
      "condition": "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
      "hit": false,
      "basis": "valuation_dependent=False, market_wrong_reason_given=市場（尤以 Goldman 空方為代表）把 2025 毛利低谷讀成 300mm 產能策略的結構性拖累；本檔認定那是稼動率與折舊時點問題——capex 已由 $4.6B 降至 $2–3B、Q2 GM 季增 340bp、營益率 42.3%，2026 FCF/share ≥$8 兌現時爭點會從『產能拖累』改寫成『產能變現』"
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
      "basis": "signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=35.12, valuation_dependent=False"
    },
    {
      "row": "8b",
      "condition": "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
      "hit": false,
      "basis": "archetype='品質複利成長', cycle_position='中循環', moat='A', moat_trend='↑', cycle_gates_pass=None"
    },
    {
      "row": "11.4b-denom",
      "condition": "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
      "hit": false,
      "basis": "輸入缺(val_denominator_disputed=null)，依保守方向處理：不視為觸發（沿用 val 機械讀數）",
      "input_gap": [
        "val_denominator_disputed"
      ]
    },
    {
      "row": "8",
      "condition": "無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）",
      "hit": false,
      "basis": "signal='A', val='🟡'"
    },
    {
      "row": "9",
      "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場",
      "hit": false,
      "basis": "signal='A', val='🟡', ma='✅'"
    },
    {
      "row": "9b",
      "condition": "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
      "hit": false,
      "basis": "signal='A', val='🟡', ma='✅'"
    },
    {
      "row": "10",
      "condition": "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場",
      "hit": true,
      "basis": "signal='A', val='🟡', ma='✅'"
    },
    {
      "row": "10-verdict",
      "condition": "命中 row10 → 進場",
      "hit": true,
      "basis": "row_hit=10"
    },
    {
      "row": "QC-49",
      "condition": "90 天內翻面須引前次已發火觸發器，否則承繼前次裁決",
      "hit": false,
      "basis": "輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）",
      "input_gap": [
        "qc49_inherit_prior"
      ]
    }
  ],
  "rearm_trigger": "已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8",
  "exec_line": "持有中：三選一取『維持＋掛回檔加碼』——不清倉（無 thesis 級觸發、FCF 收割期剛開始）、不主動加碼（26 週 +35% 後 FY1 30.4x 非便宜，等 $230–245 或 Q3 確認）。新資金：首階 1/2 現價，1/2 掛觸發"
}
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/judgment.json（輸入含既有 decision_out：已合併機械欄，rearm_trigger/exec_line/人工requires_critic保留）
已寫 /Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/tables/audit.html

[validate_judgment.py] rc=0
[J3 --fix] judgment.json：套用 0 項修正
  無可自動修正項
[FAIL] judgment.json（11 FAIL／12 WARN）
  ✗ $.oneliner: length 240 > maxLength 200
  ✗ $.valuation.val_light_derivation: 機器語言外洩 'archetype'（詞表 'archetype'）—「…區。依多尺矛盾規則，品質複利 archetype 以 Fwd P/E 與 PEG…」
  ✗ $.contradictions[6].side_a: 機器語言外洩 'archetype'（詞表 'archetype'）—「…證據包內無 30 天內同 archetype 或同產業鏈 peer 的裁決紀…」
  ✗ $.reasoning.archetype: 機器語言外洩 'gate'（詞表 '\\bgate\\b'）—「…，只用來定位置（中循環）不換 gate。
信心高：兩尺同時跑，無背離需標待確認。…」
  ✗ 漂移未歸因：asym_ratio（本次=None／前份=4.7）— judgment.contradictions[] 找不到 prior_field='asym_ratio' 或 axis 含 'asym_ratio' token 的條目
  ✗ 漂移未歸因：ev5y_pct（本次=None／前份=44.6）— judgment.contradictions[] 找不到 prior_field='ev5y_pct' 或 axis 含 'ev5y_pct' token 的條目
  ✗ 漂移未歸因：irr_base_pct（本次=None／前份=8.5）— judgment.contradictions[] 找不到 prior_field='irr_base_pct' 或 axis 含 'irr_base_pct' token 的條目
  ✗ 漂移未歸因：bull_5y_price（本次=None／前份=546.0）— judgment.contradictions[] 找不到 prior_field='bull_5y_price' 或 axis 含 'bull_5y_price' token 的條目
  ✗ 漂移未歸因：bear_5y_price（本次=None／前份=208.0）— judgment.contradictions[] 找不到 prior_field='bear_5y_price' 或 axis 含 'bear_5y_price' token 的條目
  ✗ 漂移未歸因：p_bull_pct（本次=None／前份=25）— judgment.contradictions[] 找不到 prior_field='p_bull_pct' 或 axis 含 'p_bull_pct' token 的條目
  ✗ 漂移未歸因：p_bear_pct（本次=None／前份=30）— judgment.contradictions[] 找不到 prior_field='p_bear_pct' 或 axis 含 'p_bear_pct' token 的條目
  ⚠ triggers[0].action '未達 → 暫停加碼；達標且價未漲 → 補第二階' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[1].action '監測升級；連 2 季 −2pp → 減碼 1/3' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[3].action '加碼 1/3' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[5].action '停止加碼並減碼 1/3' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[7].action 'H1 削弱 → 暫停加碼' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[8].action '拒絕 → 中性（現金留用）；附條件損及中國業務 → 減碼 1/3' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[9].action 'H3 削弱；Bull 機率下修' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[10].action '減碼 1/3，護城河趨勢改 →' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ triggers[11].action '護城河 pricing 分下修、Bear 終端倍數下修' 不含 E12 動作詞幹 ('加碼至', '減碼至', '清倉', '重跑DD', '進場首倉', '維持觀望', 'trim回目標倉位', 'trim')（soft，real-world 觸發器文字常改寫，不擋）
  ⚠ scenario_ref 'scenario.json' 指向的檔案不存在（/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/scenario.json），略過交叉檢查
  ⚠ J2｜scenario_ref 'scenario.json' 指向的檔案不存在（/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20260907/scenario.json），J2 略過
  ⚠ J4：plain 內出現 judgment 其他欄位查無的數字：['19.5', '3.4', '92031']
```
