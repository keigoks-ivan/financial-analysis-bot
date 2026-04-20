# Reference Card: NVIDIA Rubin / Rubin Ultra Technology Stack

**最後更新**：2026-04-19  
**用途**：跨 ID 共用事實源。任何 ID 引用 Rubin / Rubin Ultra 細節必須連結回本檔。

---

## Rubin（R100）— 2026 H2 量產

| 項目 | 規格 | Source |
|:---|:---|:---|
| 製程節點 | TSMC N3P（3nm） | NVIDIA GTC 2026 keynote |
| 架構 | Dual-die（2 個 reticle-size compute chiplet） | Tom's Hardware 2026-03 |
| Transistor 數 | 336B（1.6x Blackwell 208B） | NVIDIA 官方 |
| HBM | HBM4 288 GB per GPU（8 stacks × 36 GB 12-high） | NVIDIA GTC 2026 |
| Memory Bandwidth | 22 TB/s per GPU | 同上 |
| 封裝 | CoWoS-L（3.3x reticle）+ SoIC base | TSMC + NVIDIA |
| Sampling | 2026-02 | NVIDIA Q4 FY26 earnings |
| Volume Production | 2026 H2 | NVIDIA guide |
| Q1 FY27 Rev guide | $78B（company-wide） | 2026-02-25 press release |

## Rubin Ultra — 2027 Q2 目標

| 項目 | 原規劃 | 修正後（2026-04） | Source |
|:---|:---|:---|:---|
| Die 架構 | 4-die CoWoS-L | **2-die + board-level integration** | Tom's Hardware 2026-03 / SemiAnalysis |
| 退讓原因 | Warping（熱膨脹 CTE 不匹配 + 4-die 封裝應力） | 有機基板物理極限 | 同上 |
| HBM | 16 stacks HBM4E × 48 GB = 768 GB per package | 保留相同 HBM 容量 | NVIDIA GTC 2026 |
| CPU die（Vera） | 2nm TSMC N2 | 仍 2nm | NVIDIA roadmap |
| Rack-level | NVL144（Rubin）→ NVL288（Rubin Ultra） | 2+2 topology 跨 board | NVIDIA |
| 量產 | 2027 Q2 | 可能延遲 6 個月（Warping fix） | 業界 |

## Feynman — 2028 E 目標

| 項目 | 規格 | Source |
|:---|:---|:---|
| 量產 | 2028 末 / 2029 H1 | NVIDIA GTC 2026 roadmap |
| 獨特性 | **首個 chip-level CPO GPU**（1.6T CPO micro-ring resonator） | NVIDIA 宣告 |
| 封裝 | CoPoS（TSMC 2028-2029 原訂 mass production） | TSMC OIP |
| 預期 HBM | HBM5（2029-2030 預期）或 HBM4E 強化版 | TBD |

## 關鍵註記（跨 ID 需一致）

1. **不要混淆 switch-level CPO 與 chip-level CPO**
   - Switch-level CPO（Quantum-X 2026 Q1、Spectrum-X Photonics 2026 H2）：已商用
   - Chip-level CPO（Feynman 2028）：GPU 本身 CPO 化，仍未到
2. **CoWoS-L 壽命**：CoWoS-S 享用 7 年（2015-2022），CoWoS-L 可能短於此（2024-2028 或 2029）
3. **HBM 分配**：Rubin HBM 主供 SK hynix（70%）+ Samsung（25%）+ Micron（5%）per UBS 2026
4. **CoWoS 分配 2026**：NVIDIA 60%（含 Rubin 595K wafers）+ AVGO 15% + AMD 11%

## 引用範本

```html
<span class="source-tag">[Reference: Rubin Ultra Card v2026-04-19]</span>
```

## Change Log
- 2026-04-19 v1.0：初版，基於八份 ID peer review 整理
