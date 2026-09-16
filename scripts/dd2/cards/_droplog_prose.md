# prose_card.md 丟棄紀錄

濃縮 `render-rules.md`（v16）／`prose.md.tmpl`（v19）／設計稿 §4.4／CLAUDE.md 篇幅預算 為
`scripts/dd2/cards/prose_card.md`（≤10,000 bytes）時丟掉的段落，逐條列一句理由。

1. **補寫輪整套機制**（prose.tmpl 的 `{check_cmd}`／`{prose_fix_path}`／「FAIL→改→再check≤1次」；render-rules §10 的 `dd_gates.sh` 七步驗證）——v20 散文 agent 只有 Write 工具，沒有 Bash，design §4.4 明訂「不補寫輪」，這套機制在 v20 不存在，留著只會誤導 agent 去找不存在的工具。

2. **render-rules §2b 表格注入標記完整 17 列對照表**（E2/E3/E6/E7/E8/E9B/ROE/QUOTES/E10/E11/STREE/PEERS/E12 逐一列注入段與折疊與否）——卡片只需要 agent 知道「表格已由程式生成、只放註解標記、不自己寫表格內容」這個結論（已保留於第 3 節），markers 放對放錯是組裝腳本 fallback 的事，不影響散文動筆判準；逐列細節留給程式對照，不佔 prose agent 的 context。

3. **render-rules §2b 為什麼 §5/§6 不沿用舊 e7.html/e8.html 的 WP-H2-2 診斷細節、E5 雙形狀相容說明、td.num 屬性新增的 stash diff 驗證過程**——純技術債務/沿革記錄，對本輪動筆沒有操作意義。

4. **render-rules §8 視覺規格 class 對照清單**（`.topbar`／`.status-bar`／`.sb-cell`／`.thesis`／`.hypothesis-box`／`.sec-assume`／`.sec-trap`／`.sec-contra`／`.sec-premortem`／`.sec-irr`／`.g`/`.y`/`.r`/`.b` 等）——設計稿未明講 v20 是否沿用同一份 `dd.css`／模板，且此清單屬機械 CSS 對照非口吻或判斷規則；只保留操作上必要的 decision chip 色碼（進場/觀望/迴避三色，第 3 節）。

5. **render-rules §9 dd-meta／`<head>`／版本一號到底契約**（schema `v15.0` 字串、`<head>` 由 `render_dd.py` 組裝、目錄導覽列自動生成）——散文 agent 不寫 head／toc／dd-meta，不需要知道版號字串本身，屬程式組裝層事實。

6. **render-rules §6 QC-37 裁決單一居所的同源明細**（`kill_metrics[]`＝E12表哪一列、`rearm_trigger`＝哪一列、trap 定性兩處掛鉤）——只保留最上位一句「裁決只完整陳述於頁首＋decision，其餘見§X」（第5節已留），逐項同源對映屬程式/判斷層的對照表，非散文下筆時要做的判斷。

7. **prose.md.tmpl 的「bundle 全文已附」「不讀任何檔」「禁 WebSearch/WebFetch/Read」等 token 紀律段落**——v20 工具本來就只有 Write，沒有 Read/WebSearch/WebFetch 可用，這些禁令在新工具集下是恆真命題，不必重申。

8. **zh-analyst-prose 二～六節**（範本改前改後全文對照、各區塊字數規範表、四、不變的硬規則、五、審稿流程、六、檢定句怎麼寫）——任務只要求把「一、AI 痕跡清單」壓縮進卡；其餘節服務的是「審既有文字」與「新寫長文教學」場景，v20 散文 agent 是一次性生成任務，不做審稿流程。

9. **render-rules §4「QC-54 白話呈現」中儀表板收斂的逐項清單**（不放「基本面評級A+/A/B/C/X」整列、5Y EV·IRR 列不得出現 AR 或路徑對帳句等）——頁首儀表板在 v20 已是純機械段（第3節「機械禁寫」已涵蓋），agent 不寫這段，細節不需要進卡。

10. **CLAUDE.md 篇幅預算表中 v13/v14/v12/legacy DCA 三列**（非 v15/v20 schema 的 floor／warn 數字）——本卡只服務 v20（承接 v15 schema 的篇幅帶），其餘 legacy 列與本輪散文 agent 無關。
