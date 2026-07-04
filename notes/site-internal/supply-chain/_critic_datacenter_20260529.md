# single-point-critic report — datacenter (AI 資料中心實體建置)

日期：2026-05-29 · 框架：v1.5（雙軸 + 經濟 gate + Kill Test）· 裁決者：cold-review sub-agent（與寫 ⚑ 的 agent 分離）

## 裁決總結：**零結構性變更**（map 的單點保守度校準正確）

| 項目 | 裁決 | 理由（含具名替代源） |
|---|---|---|
| **b-turbine ⚑ 大型燃氣渦輪機** | **KEEP ⚑** | H/J-class 重型機組全球僅 GE Vernova／Siemens Energy／三菱動力能造（~2/3 產能、slot 售罄至 2030）。唯一可名之候選 Ansaldo 為 GE 授權方、技術受制無法 18-24 月獨立認證；東方/上海電氣僅中國內需且地緣排除。S1∧S2∧M2 全過，Kill Test = NO。 |
| **🐘 GEV / Siemens Energy / 三菱** | **KEEP 🐘（GEV 不升 💎）** | 框架明文禁止把卡特爾成員標 💎，即使燃氣電力是 GEV 最大段（~60% 營收）。卡特爾成員上行被三家均分、無衛星 EPS 不對稱性。 |
| GOES 電工鋼（premium HiB） | DEMOTE（維持無 ⚑） | 可名 3 家同級（日本製鐵／POSCO／JFE）+ 寶武，未達 ≤3≥90%；POSCO 光陽、日鐵 Hirohata 各自擴產，12-18 月可認證替代。Cleveland-Cliffs 美國本土唯一屬政策/關稅風險非能力獨佔。 |
| GIS / 中興電 | DEMOTE | 可名 5 家（Hitachi/Siemens/GE/三菱電機/ABB/Hyundai）；中興電國內獨佔屬客戶配置。 |
| Chiller / LV switchgear / Busway | DEMOTE | 各可名 4-6 家替代源；無 S1。 |
| Corning 光纖（s-fiber） | 正確排除 | Prysmian + Sumitomo 皆產 ULL 單模光纖、9-18 月可換；且 AI 光纖 <20% GLW 營收，連經濟 gate 都不過。 |
| 華城 1519 on g-lpt（core+tight） | KEEP | 變壓器 ~70% 營收（core ✓）；lock=tight 反映 frame 合約能見度，但 g-lpt 正確非 ⚑（6+ 家），故華城留為一般優勢公司、非 💎。 |
| 高力 8996 on c-cdu（core+med） | KEEP | 液冷 ~50% 營收（core ✓）；lock=med 正確（Vertiv/Boyd/Nortek 可替代）→ 不升 💎。 |

## 一句話定位（critic 認可）
此 facility-buildout 層的故事是「**結構卡特爾產能稀缺 + 全鏈寡占定價權**」，不是「多個單點鎖喉」——與 CoWoS/CPO 藏著 TW 小型股單點的結構截然不同。單一 ⚑（燃氣渦輪機）且owner 全為 🐘 mega-cap，0 💎 satellite 是誠實且正確的結論。
