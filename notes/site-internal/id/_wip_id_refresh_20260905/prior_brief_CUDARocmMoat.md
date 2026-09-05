# prior_brief — ID_CUDARocmMoat_20260501.html（v2.3，judgment 2026-06-20 🔴）

禁讀全文；本檔只含 id-meta 決策欄、kill 表、非共識／分歧標題。

## id-meta（決策欄）
- **oneliner**：CUDA 護城河正在分層：推論層已裂（ROCm 7.2 出箱 parity），但 NCCL+NVLink 多卡訓練 scale-out 仍不可取代；2027-28 真贏家不是 GPU 廠，是控制抽象層的 framework owner（META PyTorch / GOOGL JAX / OpenAI Triton）。
- **now_state**：推論層 CUDA 護城河已開始裂——ROCm 7.2（2026-03）達 vLLM/llama.cpp/Ollama/SGLang 出箱 parity、PyTorch 2.7 ROCm ~95% 功能對等；但訓練多卡 scale-out（NCCL+NVLink）NVDA 仍獨家、TensorRT-LLM/FlashAttention 3 仍 CUDA-only。
- **future_state**：framework 抽象化把 GPU 變『可替換後端』——framework owner（META PyTorch / GOOGL JAX-Pallas / OpenAI Triton）掌握抽象治理權；推論層 AMD/ASIC 取份額、訓練層 NVDA 仍守；UALink 2.0 spec 2026 Q2 已發布、硬體 2026 H2 起初步商用，大規模採用 2027——採用速度是關鍵變數。
- **action**：護城河交易不是『永遠 long NVDA 軟體鎖定』——而是『訓練 scale-out 仍護城（NCCL/NVLink）、推論護城河蝕』；被低估的贏家是 framework owner（META/GOOGL）+ ROCm parity 的 AMD。盯 ROCm parity 里程碑 / UALink 進度 / framework 治理權。
- **sd_verdict**：balanced
- **clock_phase**：II
- **conviction**：high
- **priced_in**：None
- **demand_5y_multiple**：1.0
- **tam_usd_2030**：0
- **cagr_pct_5y**：0
- **thesis_type**：structural
- **mega**：semi
- **sub_group**：compute_demand
- **sister_ids**：['ID_AIAcceleratorDemand_20260419.html', 'ID_AIInferenceEconomics_20260430.html', 'ID_AIComputeCapexCycle_20260611.html']
- **related_tickers**：NVDA（🔴｜CUDA/cuDNN/NCCL/NVLink 護城河——訓練 scale-out 仍獨家，推論層護城河開始蝕）、AMD（🔴｜ROCm 7.2 達推論出箱 parity（vLLM/llama.cpp）；推論份額入口，訓練仍落後 NVLink）、META（🔴｜PyTorch 抽象層 owner——決定 GPU 是否可替換後端，2027-28 真贏家層）、GOOGL（🟡｜JAX/Pallas + TPU——自有抽象棧 + 自研矽，繞過 CUDA 最完整者）、AMZN（🟡｜Trainium + Neuron SDK——自有編譯棧降低 CUDA 依賴）、MSFT（🟡｜Azure + Maia + 自有推論棧；CUDA 依賴漸脫鉤）、AVGO（🟢｜ASIC 受惠於 framework 抽象化（GPU 變可替換後端利於 custom 矽））、INTC（🟢｜Gaudi + oneAPI——挑戰者但生態落後 ROCm）

## kill_metrics（前版）
- ROCm｜把 parity 從推論擴到訓練 + 高階核（TensorRT-LLM/FlashAttention 等價物出箱可用 = 護城河蝕擴大，by 2026 Q4）｜window=by 2026 Q4
- NVLink scale-out 替代進度｜UALink 2.0 spec 已出 + 2026 H2 初步商用 → 盯 hyperscaler 大規模採用速度 / MSCCL++ 出 research；訓練護城河的唯一硬威脅，2026 H2 起即須監測，非等 2027）｜window=2026 H2
- framework 治理權｜PyTorch / JAX 是否預設多後端（hardware-agnostic 成 default = GPU 商品化加速）｜window=
- hyperscaler 自研矽｜TPU/Trainium）production 滲透率（繞過 CUDA 的實證；GOOGL/AMZN 自用比例）｜window=

## 非共識／分歧標題（前版）
（無獨立分歧卡標題）

## NC 句（前版）
- NC#1（推論層護城河已裂）判 INTACT、NC#3（framework owner 是終局贏家）INTACT、NC#2（訓練 scale-out 護城河 2028 前不破）判「很可能但有 UALink 變數」——故 thesis mixed、conviction mid。

## 可證偽條件句（前版）
- UALink（開放 scale-out 互連）2.0 spec 已於 2026 Q2 發布、硬體 2026 H2 起初步商用；若 2027 hyperscaler 大規模採用、或 MSCCL++ 從 research 轉 production，則訓練 scale-out 護城河開始鬆動，NVDA 最硬的那層牆出現裂縫——故監測點 2 從 2026 H2 起即須盯（非等 2027）。