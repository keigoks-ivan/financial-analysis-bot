# Reference Card: Ticker 評級（跨 ID 一致性）

**最後更新**：2026-04-19  
**用途**：同一檔 ticker 在多份 ID 的評級（🔴 核心 / 🟡 次要 / 🟢 邊緣）必須一致。

---

## 評級定義

| 評級 | 定義 | 應用 |
|:---|:---|:---|
| 🔴 核心 | 營收 >40% 依賴此產業 OR 技術領導者（獨家 / 壟斷位置） | 單一 ID 內最多 5 檔 |
| 🟡 次要 | 營收 10-40%，重要但非主導 | — |
| 🟢 邊緣 | 營收 <10% 但被市場連動 | — |

---

## 主要 ticker 評級表（跨 8 份 ID）

### 🔴 核心級（在 ≥ 3 份 ID 是核心）

| Ticker | AI | AP | HBM | LEN | Net | AI DC | SiPho | LC |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| NVDA | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | — | 🔴 | — |
| 2330.TW | 🔴 | 🔴 | 🟢 | 🔴 | — | — | 🔴 | — |
| AVGO | 🔴 | 🔴 | — | — | 🔴 | — | 🟡 | — |
| ASML | 🟡 | — | 🟡 | 🔴 | — | — | — | — |

### 🔴 單一 ID 核心（其他 ID 未出現或 🟡/🟢）

| Ticker | 核心 ID | 其他 ID 評級 |
|:---|:---|:---|
| AMD | AI 🔴 | LEN 🟡 |
| MRVL | AI 🔴、Net 🔴 | SiPho 🟡 |
| MU | HBM 🔴 | — |
| LITE | SiPho 🟡（Networking 為 🟢） **⚠ 跨 ID 不一致** | 待統一 |
| COHR | SiPho 🔴（Networking 為 🟡） **⚠ 跨 ID 不一致** | 待統一 |
| VRT | AI DC 🔴、LC 🔴 | — |
| ETN | AI DC 🔴、LC 🔴 | — |
| GEV | AI DC 🔴 | — |
| CRDO | Net 🔴 | AP 🟢 |
| ONTO | AP 🔴 | LEN 🟡 |
| AMAT | AP 🟡、LEN 🔴 | — |
| LRCX | AP 🟡、LEN 🔴 | — |
| KLAC | AP 🟡、LEN 🟡 | — |
| Asetek | LC 🔴 | — |
| Nidec | LC 🟡、AI DC 未列 | — |

---

## 待處理的不一致（v1.4 必改）

| Ticker | 問題 | 建議 |
|:---|:---|:---|
| LITE | Networking 🟢 vs SiPho 🟡 | 統一為 🟡（SiPho 是 LITE 核心業務） |
| COHR | Networking 🟡 vs SiPho 🔴 | 統一為 🔴（NVDA $2B deal + InP 獨家） |
| BESI | 多 ID 都提但都是 non-obvious 附表（未列主清單）| 加入 AP ID §11 為 🔴 |

---

## 跨 ID 評級規則

1. 同一 ticker 在多份 ID 出現 → 評級**不得更動**超過 1 級（即 🔴 可變 🟡，不可直接變 🟢）
2. 若業務分層明顯（如 COHR：Networking 是 transceivers，SiPho 是 InP laser）→ 可在 note 欄解釋
3. 新增 ID 發布前，必須讀本檔 → 若新 ID 的評級會造成跨 ID 不一致 → 解釋 or 重新分類

---

## Change Log
- 2026-04-19 v1.0：初版，基於 8 份 ID peer review 整理。發現 LITE/COHR 兩檔跨 ID 評級不一致。
