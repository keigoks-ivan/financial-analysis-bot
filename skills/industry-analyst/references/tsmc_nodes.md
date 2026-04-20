# Reference Card: TSMC 製程節點 Roadmap

**最後更新**：2026-04-19  
**用途**：TSMC 節點 / 時程 / 客戶跨 ID 一致。

---

## TSMC 節點 Roadmap

| 節點 | Risk Production | Mass Production (HVM) | 關鍵客戶 | Backside Power |
|:---|:---|:---|:---|:---|
| N3 / N3P / N3E | 2022 | 2022-2024 逐步 | Apple M3/M4、NVDA Rubin、AVGO ASIC | ❌ |
| N2（首個 GAA） | 2025 H2 | **2025-Q4 / 2026-Q1（Fab 20/22 已量產）** | Apple M5+、AMD Zen 6、Qualcomm、MediaTek | ❌ |
| N2P | 2026 H2 | 2027 | — | ❌ |
| **A16（1.6nm）** | 2026 H1 | **2026 H2（risk）→ HVM 2027 Q4** | NVDA Rubin Ultra 2027 Q2 | ✅ **首個 Super Power Rail (BSPDN)** |
| A14（1.4nm） | 2027 | 2028 | TBD | ✅ BSPDN + High-NA EUV |
| A10 | 2029-2030 | TBD | — | — |

## 2026 年 2nm 客戶分配（已 sold out）

| 客戶 | 預估 % |
|:---|:---|
| Apple（M5/M6/A20） | >50% |
| AMD（Zen 6、MI400 部分 die） | ~15% |
| NVIDIA（Rubin Ultra Vera CPU die） | ~10% |
| Qualcomm（SD 8 Gen 5） | ~10% |
| MediaTek（Dimensity 9500+） | ~8% |
| 其他（HPC / 自駕） | ~7% |

## 2026 CoWoS 分配

| 客戶 | 預估 %（~130K WPM total） |
|:---|:---|
| NVIDIA | 60%（Rubin 595K wafers） |
| AVGO | 15%（~150K wafers，Google TPU 90K / Meta 50K / OpenAI 10K） |
| AMD | 11%（~105K，MI350/400） |
| MRVL | 3-5%（AWS Trainium、自研 ASIC） |
| 其他 | ~10% |

## TSMC 市佔（leading-edge foundry，2026）

| Foundry | 市佔 |
|:---|:---|
| TSMC | ~72-75% |
| Samsung Foundry | ~7-12%（2026 期望翻身 但 SF2 yield 55-60% 未達 threshold） |
| Intel Foundry | <2%（18A ramp + Microsoft/AWS 外部客戶） |

## 跨 ID 引用規則

- 引用 TSMC 節點時程 **必須標 risk vs HVM 區別**
- A16 常被誤寫為「2026 量產」，實際是 **risk 2026 H2 / HVM 2027 Q4**
- Backside power 是 A16 最關鍵差異化（Super Power Rail）— 非 2nm 能力範圍

## Change Log
- 2026-04-19 v1.0：初版，基於 LEN / AP / HBM peer review 整理
