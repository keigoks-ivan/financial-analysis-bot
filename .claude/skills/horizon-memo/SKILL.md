---
name: horizon-memo
description: CEO 關注清單（/horizon/）的每週幕僚備忘。讀 docs/horizon/data/horizon.json 的證據包，寫一頁備忘：這週變了什麼、連起來看、一個等擁有者決定的問題、一個盲點。雲端 routine `horizon-memo-auto` 每週一 08:30 台北執行並 commit push；使用者說「寫幕僚備忘」「horizon memo」「更新 CEO 備忘」時也可手動執行。
---

# horizon-memo：CEO 關注清單的每週幕僚備忘

## 定位

`/horizon/` 是全自動的機械層：九個大問題、押注分組、壓力測試、盲點、60 天日程、今天要處理的事，每天由 `scripts/build_horizon.py` 重算，不呼叫模型。

機械層只會列出來。本 skill 補上「所以呢」：像一個資深幕僚，每週一讀完整頁，告訴 CEO 這週最重要的變化、這些變化連起來代表什麼、有哪一個問題需要他本人決定、還有哪裡沒人在看。

擁有者的定位原話：「把它當作一個厲害的輔助者」、「身為 CEO 的角度，不要被網站限制住」。

本 skill 只提問題、不下結論。不寫買賣、不寫加減碼、不給目標價（全站描述器紀律；最終投資判定走 DD 統一裁決與決策三錨，不歸本頁）。

## 輸入

1. `python3 scripts/check_horizon_memo.py --brief`：證據包。九題現況與 7 天變化、押注分組、方法成績、壓力測試、盲點、今天要處理、方向衝突、60 天日程、市況判讀標題、上一份備忘。**只讀這份**，需要細節再開 `docs/horizon/data/horizon.json`。
2. `docs/horizon/data/memo_history.jsonl`：過去的備忘（避免每週問同一個問題；上週問過的問題若沒有新資料，不重問）。

## 輸出：`docs/horizon/data/memo.json`

```json
{
  "schema": "horizon-memo-v1",
  "as_of": "寫的日期（台北）",
  "data_as_of": "horizon.json 的 as_of，必須一致",
  "headline": "一句主張，≤ 40 字",
  "changed": [{"text": "≤ 90 字", "refs": ["far.ai_compute.metrics.gain.eps_rev_3m"]}],
  "chain": "連起來看，≤ 180 字（可省略）",
  "decision": {"question": "問句，≤ 60 字", "why": "為什麼現在要決定，≤ 180 字", "refs": ["..."]},
  "blind_spot": {"text": "≤ 140 字", "refs": ["blind_spots.0.title"]},
  "review": {"model": "冷讀模型", "rounds": 1, "findings": []}
}
```

`refs` 是 horizon.json 裡的路徑，用點連接。清單可用序號（`stress.0.live_tw_hold`），`far` 可用題目 id（`far.memory.metrics.gain.self_funded`）。每一條主張至少一個 ref。

## 四個欄位怎麼寫

- **headline**：這週最重要的一件事，寫成主張。不是摘要，是判斷。例：「九題裡有四題其實是同一個押注，12 個席位都壓在上面」。
- **changed**：2～4 條，這週真的變了的事，按重要性排。沒有 7 天前的紀錄時，寫「目前最值得注意的狀態」。沒變的事不寫。
- **chain**：把兩三個數字連成一條因果或連動。例：殖利率 5.11% 和私募信貸贖回壓力，會讓資料中心的融資變貴，這直接打到第一題。只能連資料裡看得到的東西；推論要寫成「可能」「如果」，不寫成事實。
- **decision.question**：一個只有擁有者能回答的問題，而且要是這週答比下週答好的。好的問題是「要不要替 AI 硬體這個押注設一個上限？」「台股 130% 的曝險，在台積電財報前要維持嗎？」。不好的問題是「該不該買 NVDA」（這是買賣指令換句話說）或「AI 會不會繼續成長」（這不是他能決定的）。why 講清楚：哪個數字讓這個問題變急。
- **blind_spot**：一件九題都沒涵蓋、但可能影響公司的事。優先從證據包「盲點」挑，也可以指出九題本身的漏洞（例如某題的籃子沒資料）。講清楚它可能打到哪裡。

## 寫作規則（擁有者要求：白話、外資報告口吻、結論先行、不要 AI 感）

1. 一句一個意思，句號收。不用破折號「——」串句子，少用分號。
2. 每個強烈的句子後面跟一個數字。數字**只能抄證據包裡出現的值**，照原本位數；不自己算差距或加總（檢查程式會擋找不到的小數）。要表達差距就把兩個數字都寫出來。
3. 不用比喻：天花板、引擎、雙刃劍、骨牌、風暴、踩煞車、火上加油都不要。
4. 「不是 A，是 B」整份最多一次。不要每條結尾都收一句金句。
5. 英文縮寫第一次出現寫中文加括號，例：Sahm 指標（失業率快速上升的衰退訊號）。
6. 中文與數字之間半形空格；中文標點全形。
7. 不寫「本備忘」「值得注意的是」「綜上所述」這類自我說明。
8. 禁用詞（檢查程式會擋）：買進、買入、賣出、加碼、減碼、建倉、清倉、出場、進場、停損、停利、目標價、應該買、應該賣、建議買、建議賣。

## 步驟

1. `bash scripts/install_hooks.sh`；`git pull --rebase origin main`。
2. `python3 scripts/check_horizon_memo.py --brief`，讀完；讀 `memo_history.jsonl` 最後 4 行。
3. 寫 `docs/horizon/data/memo.json`。
4. **冷讀**：用 `Agent` 工具開一個 subagent（模型見下表，寫與審永不同模型），職責書逐字如下，subagent 只回報不改稿：

   > 你是冷讀者。讀 `docs/horizon/data/memo.json` 和 `python3 scripts/check_horizon_memo.py --brief` 的輸出。逐項回報，每項給 🔴（必須改）或 🟢：
   > (a) 有沒有任何句子等於在叫人買或賣、加或減部位，即使沒用禁用詞。
   > (b) 每條主張的數字，在證據包裡找得到嗎？有沒有把相關當成因果、把「可能」寫成「會」。
   > (c) decision.question 是不是只有擁有者能回答、而且這週答比下週答好？是不是換句話說的買賣建議？
   > (d) 有沒有更重要、但備忘漏掉的事（對照證據包的「今天先看」「方向一致嗎」「最怕什麼」）？
   > (e) 白話：有沒有看不懂的行話、比喻、破折號串句、每段結尾金句。
   > 輸出 JSON：{"model": "...", "verdict": "pass" 或 "fix", "findings": [{"item": "a", "level": "🔴", "note": "..."}]}

5. 依 findings 修稿，最多 2 輪；第 2 輪後仍有 🔴 → 失敗處置。
6. `python3 scripts/check_horizon_memo.py` 必須 PASS；把最後一輪冷讀結果寫進 `memo.json.review`。
7. append 一行到 `docs/horizon/data/memo_history.jsonl`（整份 memo.json 壓成一行）。
8. `python3 scripts/qc.py` 必須 PASS。
9. 只 stage `docs/horizon/data/memo.json`、`docs/horizon/data/memo_history.jsonl`、`docs/horizon/data/memo_status.json`，不得 `git add -A`、不得 `--no-verify`。commit 訊息：`horizon-memo {as_of}：{headline 前 30 字}`。`git pull --rebase origin main` 後 push，失敗重試 3 次。

**失敗處置**：不改 `memo.json`，只寫 `docs/horizon/data/memo_status.json` = `{"as_of": ..., "status": "failed", "stage": "<哪一關>", "reasons": [...]}`，單獨 commit push。成功時寫 `{"as_of": ..., "status": "ok"}`。

## 模型配對（寫與審永不同模型）

| 寫備忘（routine 的 session model） | 冷讀（Agent subagent） |
|---|---|
| `claude-opus-5-5` | `claude-sonnet-5` |
| 手動由 orchestrator（opus）跑 | `claude-sonnet-5` |

## 不做的事

- 不改 `horizon.json`、`questions.json`、`build_horizon.py` 或任何機械層檔案。想加第十題、改籃子，寫進 blind_spot 讓擁有者決定。
- 不上網搜尋。備忘只根據站內證據包；證據包沒有的事不寫。
- 不改 routine 排程。

## 版本

- v1.0 2026-09-24：初版。擁有者選「程式算的五件事＋每週幕僚備忘」。
