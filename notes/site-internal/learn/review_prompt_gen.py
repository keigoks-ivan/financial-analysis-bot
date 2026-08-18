import json,sys
M=json.load(open('scripts/learn/manifest.json'))['modules']
def prompt(num):
    m=next(x for x in M if x['num']==num)
    return f'''你是線上課程「股票分析完整框架」的審稿人（cold review＋直接修稿），負責第 {num} 課「{m['zh']}｜{m['en']}」，檔案 `docs/learn/{m['file']}`。工作目錄 /Users/ivanchang/financial-analysis-bot。你不是寫這課的人。

步驟：
1. 讀 `notes/site-internal/learn/REVIEW_SPEC.md`（你的規格，全部）、`notes/site-internal/learn/WRITER_SPEC.md`（寫手規格）、`notes/site-internal/learn/BRIEFS.md` 檔頭＋「## {num} ·」段（這課本該涵蓋什麼）。
2. 完整讀 `docs/learn/{m['file']}`（可分段讀）。需要驗證數字／案例時對照 `notes/site-internal/learn/` 下的三份素材（用 grep 定位，不必全讀）。
3. 照 REVIEW_SPEC 的 A–H 逐條審，**直接修**（Edit 工具；只動 BODY／SCRIPT 區與 meta description，其他一個字元都不准動）。正確性錯誤必修；覆蓋缺口要補到同等深度；薄段擴寫；廢話刪；中文要是通順的台灣中文；quiz 答案索引逐題核對；試算器極端值核對。**特別**：quiz 裡帶 `from` 的交錯複習題，寫手寫的時候看不到前面那課的內容，請 grep 對應課 `docs/learn/MM-*.html` 的 module-goals／h2／key-term，把題目改成真的考那課的具體概念（用本課情境），答案與 exp 要對。
4. 修完跑 `python3 scripts/learn/course.py qc docs/learn/{m['file']}` 到 0 errors。
5. 依 REVIEW_SPEC 的回報格式回報（≤12 行）。'''
if __name__=='__main__': print(prompt(sys.argv[1]))
