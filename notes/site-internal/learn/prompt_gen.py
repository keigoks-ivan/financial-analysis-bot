import json,sys
M=json.load(open('scripts/learn/manifest.json'))['modules']
READ={
 'start':'D `dd_skill_distillation.md` 的「## 1. North star」「## 3. 值得單獨開課的判斷概念」「## 6. 可做互動計算器的公式」「## 7. 詞彙表」；I `id_skill_distillation.md` 的「## 1. Philosophy」',
 'industry':'I `id_skill_distillation.md` 全文（重點 ## 1、## 2、## 4、## 5、## 7、## 8、## 9）；D `dd_skill_distillation.md` 的「## 5. 戰爭故事」表（只挑簡報點名的列）',
 'business':'D `dd_skill_distillation.md` 的「## 1」「## 3」「## 5」「## 6」「## 7」；I `id_skill_distillation.md` 的「### Profit pool」「### Value chain」「## 5. Judgment Playbook」',
 'market':'I `id_skill_distillation.md` 的「## 3. Priced-in」「## 5」「## 8」；D `dd_skill_distillation.md` 的「## 3」（priced-in／IRR／Max DD／矛盾裁決）「## 5」「## 6」',
 'judgment':'D `dd_skill_distillation.md` 的「## 3」「## 4」（只讀規則精神，不得出現代碼）「## 5」；I `id_skill_distillation.md` 的「## 4. Risk & Falsification」「## 5. Judgment Playbook」「## 7」',
 'portfolio':'A `alloc_backtest_distillation.md` 全文',
 'close':'BRIEFS.md 全部 29 段（你要收斂全部課程），以及 `docs/learn/*.html` 每一課的 `.module-goals` 區塊（用 grep 擷取即可，不必整頁讀）',
}
def prompt(num):
    m=next(x for x in M if x['num']==num)
    slug=m['file'][:-5]
    return f'''你是這門線上課程「股票分析完整框架」的一位課程寫手，負責**第 {num} 課「{m['zh']}｜{m['en']}」**（檔案 `docs/learn/{m['file']}`）。工作目錄：/Users/ivanchang/financial-analysis-bot。

請依序做：
1. 讀共同規格 `notes/site-internal/learn/WRITER_SPEC.md`（全部；這是硬規則）。
2. 讀 `notes/site-internal/learn/BRIEFS.md` 的檔頭說明＋「## {num} ·」那一段（你的簡報；其他課的簡報只需看標題，知道前後課講什麼，避免重複）。
3. 讀素材：{READ[m['part']]}。素材路徑都在 `notes/site-internal/learn/`。素材只是材料——**課程結構照 WRITER_SPEC §1，不照素材的報告結構**；素材裡的內部名稱／代碼／「裁決」口吻一律轉成一般讀者語言。
4. 想清楚這一課的敘事線（開場案例→概念→範例→實戰→陷阱→接回框架→測驗），然後寫。中文是主要語言（讀者是台灣投資人），英文是同等品質的另一版，不是翻譯腔。深入淺出＝機制講透、例子具體、數字有量級與年份、每個抽象詞立刻白話一次。
5. 照 WRITER_SPEC §6 分段寫入 drafts、inject、跑 qc 到 0 errors。目標大小 80–130KB。

品質標準（審稿人會照 WRITER_SPEC §3 逐條檢查並打回）：每個核心概念都要有機制＋正例＋反例／假訊號＋怎麼從公開資料看出來；至少一處說明工具的不適用邊界；至少一處反直覺結論；quiz 8–10 題其中 ≥3 題情境判斷、2 題 `from` 交錯複習（課號照簡報）；不寫廢話段；全形標點；去個人化；只用允許的連結。

最後用 5 行以內回報：大小、quiz 題數、試算器有無、qc 結果、你自認最弱的一段。'''
if __name__=='__main__':
    print(prompt(sys.argv[1]))
