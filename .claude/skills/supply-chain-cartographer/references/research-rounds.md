# 標準 5 輪研究細則（Round 0-5）

> 條件載入：研究階段（Round 0 開始）時載入。核心 SKILL.md 只保留 5 輪骨架，本檔為每輪的搜尋詞範本、TW 中文源清單與 DD universe 對照指令。內容自 v1.1 原文零語意變更搬移。

## 工作流（標準 5 輪研究 + 4 步輸出）

### Round 0：先看現況

```
# 1. 確認 topic 在 manifest（不在就要加）
grep '"id": "{topic}"' docs/supply-chain/data/topics.json

# 2. 看既有 topic 範例
ls docs/supply-chain/data/   # cowos.json, cpo.json

# 3. 估計研究時間
- 半導體製造 topic（HBM、先進製程、ASIC）：~60-90 min
- 跨產業 topic（機器人、衛星、軍工）：~90-120 min
```

### Round 1：產業 Overview + 主玩家（4-5 平行 WebSearch）

英文 sources 優先（覆蓋面廣、行業報告多）。

```python
parallel_search([
    "{topic} supply chain 2026 主要玩家 architecture",
    "{topic} market size 2026 2030 IDTechEx Yole forecast",
    "{topic} key technology 鎖喉點 single-source bottleneck",
    "{topic} hyperscaler customer adoption timeline",
    "{topic} TSMC Samsung foundry partner 2026",
])
```

抓出：
- 產業骨架（哪幾個製程環節、產品段）
- 全球 majors（美/日/歐/韓大廠）
- 預期上量時間（2025/2026/2027）
- 關鍵客戶（hyperscaler、AI 晶片廠）

### Round 2：TW 中文供應鏈（5-8 中文 WebSearch）

**這是 stingtao 種子最強、純自研最弱的環節**。必須用中文搜尋找 TW 小型股的客戶獨家。

優先源：
1. **TechNews 科技新報**（technews.tw）
2. **Money Weekly 理財周刊**（moneyweekly.com.tw）
3. **TrendForce**（中文版報導）
4. **Digitimes**（digitimes.com）
5. **工商時報** / **經濟日報**（chinatimes.com / udn.com）
6. **數位時代**（bnext.com.tw）
7. **鉅亨網**（cnyes.com）
8. **Vocus** / **Pocket** / **StatementDog**（個股法說會整理）

```python
parallel_search([
    "{TW player 1} {topic} TSMC NVIDIA 供應鏈 2026",
    "{TW player 2} {topic} 獨家 客戶 送樣",
    "{TW player 3} {topic} 法說 市佔",
    # 通用詞
    "{topic} 台廠 受惠股 供應鏈",
    "{topic} 客戶獨家 鎖喉點 台灣",
])
```

抓出：
- TW 小/中型股對 TSMC / NVDA / AMD 的客戶獨家狀態
- 法說會公開數字（最強信心度來源）
- 送樣 / 驗證 / 量產時程

### Round 3：垂直深度（3-5 平行 WebSearch）

針對 topic 特定的關鍵環節做深掘。例：
- HBM → DRAM 三強市佔 / TC bonder / HBM4 base die
- CPO → DFB 雷射 / III-V epi / MLA / FAU
- ASIC → EDA / 設計服務 / IP / chiplet
- 機器人 → 致動器 / 減速機 / 感測器

```python
parallel_search([
    "{topic} 關鍵環節 1 supplier market share 2026",
    "{topic} 關鍵環節 2 bottleneck monopoly",
    "{topic} downstream demand hyperscaler",
    "{topic} new entrant disruptor 2026",
    "{topic} OFC SEMICON {year} announcement",  # 重大會議
])
```

### Round 4：競爭驗證（2-3 focused WebSearch）

對每個你打算標 ⚑ 的 single-point，**強制找第二個獨立來源**驗證。

```python
parallel_search([
    "{single-point 1} confirmed 2026 sole supplier",
    "{single-point 2} 法說 確認",
    "{single-point 3} second source alternative challenger",
])
```

**規則**：
- 高信心 ⚑：≥2 來源（含 1 個權威源 = 法說會 / 公司公告 / 大行報告）
- 中信心 ⚑：1 個權威源 或 2 個次要源 — 在 single 欄位明標「送樣中 / 待量產 / 單一來源」
- 低信心 ⚑（謠傳 / 單一 substack）：**不要標 ⚑**，放主表但不打旗

### Round 5：DD universe 對照

```bash
# 跑 build script 確保 dd_links.json 是最新
python3 scripts/build_supply_chain_dd_index.py

# 列出本 topic 涵蓋的 ticker 中哪些有 DD
for t in <list of tickers>; do
  f=$(ls docs/dd/DD_${t}_*.html 2>/dev/null | sort -r | head -1)
  if [ -n "$f" ]; then echo "✓ $t → $(basename $f)"; else echo "✗ $t (no DD)"; fi
done
```

→ 沒有 DD 的小型 ticker **不是問題**（supply chain map 就是要 surface 這些 gap）。但要在 commit message 列出來，作為未來 DD 工作的待補清單。
