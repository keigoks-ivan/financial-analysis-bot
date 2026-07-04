# single-point-critic — auto-semi (2026-05-29)

Framework: v1.5（Axis 1 能力非替代性為唯一合格軸 + Kill Test + 經濟 gate）。
Critic = Sonnet sub-agent（與作者 Opus 分離，Boris verify pattern）。

## 裁決

| 項目 | 候選 | 裁決 | 具名替代源 / 理由 |
|---|---|---|---|
| s-mems | Bosch 車用 MEMS「近乎獨佔」 | **DEMOTE** | Murata SCHA600（ASIL-D ESC/ESP）、ST ASM330LHB（ASIL-D）、TDK-InvenSense（$1.3B 併購擴張）皆已 AEC-Q100 + ASIL-D 認證、可供同級應用。Bosch ~33% 車用 MEMS / ~46% 慣性子段 = 規模龍頭非能力壟斷；既有產線換供應商 3-5 年屬客戶配置鎖，不是 Axis 1。competition monopoly→oligopoly，移除 ⚑。 |

## 漏標掃描（全 26 節點）

無漏標。每個可能候選都因「已有多家合格供應商」或「地圖本文已具名替代」而 FAIL Axis 1：
c-mcu（NXP/Renesas/Microchip/ST 皆 ASIL-D 合格、車廠政策性 dual-source）、c-adas（NVIDIA/Qualcomm/Mobileye 三強競爭）、s-cis（onsemi/Sony/OmniVision 競爭升溫）、s-radar（NXP/Infineon/TI/ADI 四強）、p-sic-dev（ST/Infineon/onsemi/ROHM，Tesla 自己 dual-source）、f-foundry-auto（多家合格代工）。

## 朋程 Actron（borderline）

~53-65% 全球車用發電機整流二極體、過經濟 gate（pure-play core），但 Axis 1 FAIL — 整流二極體為 commodity discrete，onsemi/Diodes 能力可做；且 ICE 整流子隨 EV 衰退。→ 不打 ⚑、不升 💎，保留 core_business+lock=med 當設計鎖佐證。

## 💎 / tier 標籤

Infineon / NXP / UMC / 漢磊 / 朋程 的 core_business + supply_chain_lock 標籤正確（寡占設計鎖），但所在節點皆非 ⚑ → 不會轉成 💎。正確。

## 結論

**0 ⚑ / 0 💎。** 這是車用半導體的**誠實且預期**結果 — 產業結構性 dual-source 強制 + ASIL 設計鎖，使真能力單點極稀少。護城河存在（設計鎖、生命週期 10+ 年、認證壁壘）但屬寡占競爭層級，非可標 ⚑ 的能力壟斷。地圖 subtitle 已正確點出此產業特性。
