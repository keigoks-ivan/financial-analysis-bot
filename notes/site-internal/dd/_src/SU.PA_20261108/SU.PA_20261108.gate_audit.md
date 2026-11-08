# gate_audit（dd2 v20，sonnet，第 2 輪）

判斷級 🔴 = 0，🟡 = 1

- 🟢 ① `$.answers.q2_moat.verdict_values.moat.threats` 競爭／second-source／客戶集中的負向 finding（competitive_share_entrants#0/#1、customer_second_source#0、customer_concentration_credit#0）都已進 threats 並帶機率，沒有漏接。
- 🟢 ② `$.counter_evidence.blind_spots[0]` supply_demand_durability#0 與 #2 已被 blind_spots、R1、矛盾條目引用，供給可逆性（18–24 個月可擴產）也寫進 Bear 30% 的依據。
- 🟢 ③ `$.counter_evidence.triggers` 反壟斷罰款（R5、觸發 11）、關稅（R2、觸發 3）、固態變壓器／800V 替代（R4、觸發 9）、SERNAC 電池警示（觸發 10）都有接住，沒有無人處理的有 finding 軸。
- 🟡 ④ `$.decision_inputs.wait_for_price` market_wrong_reason_given 有具體數據，但 exec_line 與 q5 寫「首筆上限三分之一、不追高」，decision_inputs.wait_for_price 卻為 null，裁決又是觀望；evidence_dismissed 已解釋，屬表述不一致，不改裁決方向。
- 🟢 ⑤ `$.counter_evidence.blind_spots` 核心軸皆有證據或不適用，非核心軸也沒有空軸。 閘評論：12 軸皆 found，無空軸；缺口（客戶拆分、第三年共識、同業倍數）判斷都有寫明對結論的影響。
- 🟢 ⑥ `$.answers.q2_moat.verdict_values.moat.roic_durability` reinvest_rate 與 roiic 都有算式，我複算 17.5%×50%=8.75、PTC 9.0–11.3 億對 NOPAT 73.5 億皆對；endo_ceiling 8.75 低於共識 CAGR 的缺口已在 q3 拆解並標 endo_ceiling_exceeded；三情境 EPS 價差實質，irr_base 10.0、ev5y 51.7 與 scenario_meta 對帳一致。
- 🟢 ⑦ `$.answers.q1_business.reasoning` 引用的營運指標用 Q3 2026 與 H1 2026，不比 latest_quarter_kpis 舊；賣方目標價 2026-06-19 已明講過期且未當依據，consensus_rev_3m_pct 為 null。
- 🟢 ⑧ `$.counter_evidence.contradictions` 無前份（no_prior_dd），不適用漂移歸因，程式歸因條目已就位。
