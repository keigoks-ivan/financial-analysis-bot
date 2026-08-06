# PLTR A/B 測試裁定（2026-08-06）

A＝DD_PLTR_20260805.html（opus-writer，139.9KB，站上版）
B＝_abtest_DD_PLTR_20260806_B_sonnet.html（sonnet-writer，93.3KB，本檔同目錄）
裁判＝opus 獨立 agent，外部查核 stockanalysis.com＋MarketBeat（08-06）

## 總裁定：A 留站，從 B／查核補五項 patch（已於同日執行）

A 勝的欄位（餵下游判斷的四個關鍵全是 A）：
- endo_growth_ceiling 127 vs 37：A 按 roic-durability.md 經濟資本口徑真算（研發資本化，222%×57%）；B §5.R 未算、推給 §6.D、再投資率「估計約10-15%」無推導，且 37% 低於自身共識 CAGR 68.6%＝sanity check 失敗未處理
- max_dd −65 vs −53.5：B 的 −53.5% 與其 Bear 5Y 終點報酬相同＝把終點混淆為路徑回撤；A 錨定已實現 −44%
- 情境樹：B 的 Bull FY30 EPS 只比 Base +3.6%（Bull 幾乎全靠終端倍數）＝退化；A $8.10/$5.63/$2.73 是真價差
- moat 8.75/8.0 vs 9.0/9.0：A 以 sourced 能力進入（OpenAI Presence／MSFT Agent 365）降等級不降趨勢；B 要求已實現客戶流失（滯後指標）

B 勝的欄位（已 patch 進 A）：
- fpe_fy2：共識 FY27 $2.09（stockanalysis＋MarketBeat 雙源）；A 原用 yfinance $2.264 單源離群 → A 已改 77.8（自身 as-of $162.66÷2.09）
- peg_fy2 口徑：A 原欄位填 NTM 值 1.36 與 fpe_fy2 口徑不符 → 已改 FY+2 口徑 1.28
- upside_short/mid：A 原 meta 與自身附錄錯位 → 已按修正共識重算 −50/−29
- §10.6 內部對帳：A 有交叉項可對帳；B 10.5 vs 10.6 IRR 不一致、10Y「7.5x＝12.9%/yr」自相矛盾

連鎖修正（A 內）：救援② 上修 +11.8% 經雙源查核為 +3.2% 未達門檻 → 估值 🟡 改靠救援① 單道成立（燈不變）；機會成本三閘「上修閘勝出」下修為溫和正向；Bear anchor $26→$24；base_eps_path 1.47/2.09/3.10；新增 rearm_trigger 欄。

B 的承重缺失（若 B 上站會發生的監測損失，記錄供組態治理）：
- 無 US 政府營收 YoY kill metric；全文零德國/歐盟內容（A 有 18/11 處）→ §5.R 社會容忍度誤判 🟢
- 無 Rule of 40／毛利率絆線 → 自身 §12b'「成功但劣化」敗局無監測
- 德國聯邦國防軍決標催化劑缺；NHS break clause 只在散文不在 catalysts[]（monitor 看不見）
- kill metric「US 商業 YoY<100%×2Q」基數效應必然觸發＝校準錯誤

## 組態治理 read-through（TSM 轉正決定的補充證據）
sonnet-writer 篇幅紀律真實（93KB 帶內 vs opus 140-229KB 全超帶），裁決方向與 opus 一致；但本案顯示其研究覆蓋有系統性缺口（整個歐盟軸缺失）且量化模組會退化（§5.R 未算、情境樹退化、內部不對帳）。「sonnet-writer＋opus-critic」組態的 critic 端必須明確承擔：①覆蓋面掃描（缺什麼軸）②量化模組完整性抽查，不只挑錯字面。單一 TSM＋PLTR 兩點證據，2026-10 校準前不宜再擴大結論。
