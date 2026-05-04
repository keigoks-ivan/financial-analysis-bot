# 30 Munger Mental Models — ported from design_handoff_mental_models/data.js
# All text preserved verbatim from source.

DISCIPLINES = {
    "psych": {"id": "psych", "zh": "心理學",    "en": "Psychology",        "glyph": "◼", "color": "#534AB7", "tint": "#F0EEFB", "count": 13, "roman": "I"},
    "micro": {"id": "micro", "zh": "微觀經濟",  "en": "Microeconomics",    "glyph": "▲", "color": "#0F6E56", "tint": "#E8F5EE", "count": 6,  "roman": "II"},
    "math":  {"id": "math",  "zh": "數學/統計", "en": "Math & Statistics", "glyph": "●", "color": "#1a56db", "tint": "#EBF2FA", "count": 5,  "roman": "III"},
    "eng":   {"id": "eng",   "zh": "工程/物理", "en": "Engineering",       "glyph": "◆", "color": "#B45309", "tint": "#FBF1DE", "count": 4,  "roman": "IV"},
    "bio":   {"id": "bio",   "zh": "生物學",    "en": "Biology",           "glyph": "✚", "color": "#C0392B", "tint": "#FBE9E7", "count": 2,  "roman": "V"},
}

MODELS = [
    # ── Psychology (13)
    {"id": "m1",  "d": "psych", "zh": "激勵偏誤",     "en": "Incentive-caused Bias", "short": "誰的激勵在驅動這個行為？", "tag": "行為動因",
     "body": "人的行為受個人激勵機制支配，利益驅動下判斷扭曲且難以察覺。設計激勵結構決定了個體行為。",
     "quote": '"Never, ever, think about something else when you should be thinking about the power of incentives." — Munger',
     "cases": ["Wells Fargo 銷售獎勵 → 350 萬假帳戶", "賣方分析師偏多報告 vs 承銷佣金", "外科醫生推薦手術 vs 復健"],
     "related": ["m6", "m2"], "ask": "這個分析師/管理層的激勵和我的利益一致嗎？"},

    {"id": "m2",  "d": "psych", "zh": "社會認同",     "en": "Social Proof", "short": "從眾不是看多的理由", "tag": "群體效應",
     "body": "不確定情況下，人傾向模仿多數人行為，認為「大眾選擇」即正確選擇。泡沫形成的核心機制之一。",
     "quote": '"The social proof situation is very, very powerful." — Munger',
     "cases": ["2000 科技泡沫：散戶從眾推高估值", "Bitcoin 2021 ATH 前 FOMO"],
     "related": ["m8", "m4", "m10"], "ask": "「大家都在買」是我看多的理由嗎？"},

    {"id": "m3",  "d": "psych", "zh": "權威偏誤",     "en": "Authority-misinfluence", "short": "無名小卒說同樣的話我還會信嗎？", "tag": "頭銜陷阱",
     "body": "過度信賴有頭銜或聲望的人，不加批判地接受其判斷。在層級組織中特別危險。",
     "quote": "副機長即使發現機長操作錯誤也不敢出言糾正",
     "cases": ["Boeing 737 MAX MCAS 兩次空難", "Cathie Wood 光環 → 散戶高點追 ARKK 跌 75%+"],
     "related": ["m2", "m4"], "ask": "這位「大師」如果是無名小卒說的，我還會信嗎？"},

    {"id": "m4",  "d": "psych", "zh": "喜好傾向",     "en": "Liking-Loving Tendency", "short": "喜愛使你高估", "tag": "品牌情感",
     "body": "偏愛喜歡的人、品牌或想法，並在評估中系統性高估其優點、忽略缺點。",
     "quote": '"We ignore the faults of those we like." — Munger',
     "cases": ["投資人因喜愛 Musk 而忽略 Tesla 估值風險", "Munger 對 Coca-Cola 品牌的喜愛"],
     "related": ["m6", "m3", "m23"], "ask": "如果我不喜歡這家管理層，估值還會一樣嗎？"},

    {"id": "m5",  "d": "psych", "zh": "互惠傾向",     "en": "Reciprocity Tendency", "short": "小好意換來大代價", "tag": "人情成本",
     "body": "收到好意後產生強烈回報衝動，即使原始好意成本極低，回報代價可能極高。",
     "quote": '"The human tendency to reciprocate favors is so powerful it can be used against you." — Munger',
     "cases": ["Amazon Prime 30 天試用 → 高轉換", "投行請客戶 → 客戶回報 IPO 業務"],
     "related": ["m4", "m1"], "ask": "我接受了對方的「好意」嗎？"},

    {"id": "m6",  "d": "psych", "zh": "確認偏誤",     "en": "Confirmation Bias", "short": "主動搜尋反面論據", "tag": "持倉之敵",
     "body": "傾向搜尋、解讀、偏好能確認既有信念的資訊，忽視矛盾證據。持倉後最容易觸發。",
     "quote": '"What the human mind does with a conclusion it has reached is to try to confirm it." — Munger',
     "cases": ["投資人持倉後只讀看多報告", "LTCM 忽略 1997-98 亞洲金融危機警訊"],
     "related": ["m1", "m8", "m16"], "ask": "我最近讀過幾篇對這個倉位的空方論點？"},

    {"id": "m7",  "d": "psych", "zh": "喪失過度反應", "en": "Loss Aversion", "short": "損失痛 = 2.5× 獲利樂", "tag": "損失厭惡",
     "body": "失去某物的痛苦遠超得到同等物品的快樂（Kahneman：約 2.5 倍）。",
     "quote": '"The quantity of sorrow from losing $100 far exceeds the joy from gaining $100." — Munger',
     "cases": ["SVB 擠兌：恐懼 > 收益期望", "disposition effect：散戶不肯賣虧損部位"],
     "related": ["m9", "m6", "m22"], "ask": "若今天手上是現金，我會以現價買入嗎？"},

    {"id": "m8",  "d": "psych", "zh": "可得性錯估",   "en": "Availability Misweighing", "short": "生動 ≠ 高機率", "tag": "記憶扭曲",
     "body": "對容易想起的事件高估其發生機率。記憶的可得性扭曲了機率判斷。",
     "quote": '"Vivid images dominate people\'s estimates of probabilities." — Munger',
     "cases": ["9/11 後改開車 → 開車死亡率更高", "FTX 崩潰 → 散戶高估加密全面失敗機率"],
     "related": ["m6", "m9"], "ask": "這個機率判斷是基於數據還是新聞密度？"},

    {"id": "m9",  "d": "psych", "zh": "對比錯誤反應", "en": "Contrast Misreaction", "short": "錨定 ≠ 絕對價值", "tag": "相對性陷阱",
     "body": "判斷時依賴相對比較而非絕對標準，前後對比框架顯著影響決策（錨定效應）。",
     "quote": '"People are influenced by contrast more than by actual value." — Munger',
     "cases": ["房仲先帶看高價爛房", "PE 60x 降至 40x：仍是天價"],
     "related": ["m7", "m8"], "ask": "我的「便宜」是對比上週高點還是絕對價值？"},

    {"id": "m10", "d": "psych", "zh": "多模型共振",   "en": "Lollapalooza Effect", "short": "多偏誤同向 = 災難級", "tag": "共振警報", "flagship": True,
     "body": "多個心理偏誤同時作用並相互強化，產生遠超單一偏誤的極端結果。",
     "quote": '"Lollapalooza effects come when multiple factors combine to push hard in the same direction." — Munger',
     "cases": ["Tupperware Party：社證+互惠+喜好+稀缺", "AA 戒酒：互惠+社證+承諾", "FTX 崩潰：4 偏誤同向"],
     "related": ["m1", "m2", "m4", "m6", "m21", "m22"], "ask": "這個決策同時觸發了哪幾個偏誤？三個以上同向 = 警報。"},

    {"id": "m21", "d": "psych", "zh": "過度自信",     "en": "Overconfidence Bias", "short": "90% 人覺得自己駕車高於平均", "tag": "最危險偏誤", "isNew": True,
     "body": "人系統性高估自身判斷能力、預測準確度與知識邊界。投資中最危險的單一偏誤。",
     "quote": '"The most important quality for an investor is temperament, not intellect." — Munger',
     "cases": ["85%+ 主動基金長期跑輸指數", "Lehman 30x 槓桿到崩潰", "創業者預估 70% 成功 vs 實際 50%"],
     "related": ["m6", "m8", "m16"], "ask": "若把握只有 60%，我的倉位該多大？"},

    {"id": "m22", "d": "psych", "zh": "承諾一致性",   "en": "Commitment & Consistency", "short": "沉沒成本的心理根源", "tag": "立場鎖定", "isNew": True,
     "body": "一旦做出承諾，人傾向保持後續行為與承諾一致，即使新資訊顯示原決策有誤。",
     "quote": '"Once you\'ve publicly committed to a position, the desire to remain consistent locks you in." — Munger',
     "cases": ["股票被套後越跌越買", "WeWork IPO 失敗後 SoftBank 繼續注資"],
     "related": ["m7", "m6"], "ask": "若今天第一次看，我還會做同樣的決定嗎？"},

    {"id": "m23", "d": "psych", "zh": "厭惡傾向",     "en": "Disliking-Hating Tendency", "short": "恨使你低估", "tag": "鏡像偏誤", "isNew": True,
     "body": "對不喜歡的對象系統性忽視優點、誇大缺點。喜好傾向的鏡像。",
     "quote": '"Just as loving causes you to overestimate, hating causes you to underestimate." — Munger',
     "cases": ["傳統車廠 2010-15 系統性低估 Tesla", "柯達高管厭惡數位 → 錯失自己的發明"],
     "related": ["m4", "m6", "m13"], "ask": "我對競爭對手的判斷是否因厭惡而低估？"},

    # ── Microeconomics (6)
    {"id": "m11", "d": "micro", "zh": "規模優勢",     "en": "Scale Advantages", "short": "單位成本下降的護城河", "tag": "成本曲線",
     "body": "隨產量規模擴大，單位成本下降，形成對小競爭者難以跨越的成本護城河。",
     "quote": '"Scale advantages come in many forms — purchasing, distribution, brand, R&D." — Munger',
     "cases": ["Costco 超大量採購 → 低毛利仍獲利", "Amazon FBA 倉儲物流邊際成本遞減"],
     "related": ["m12", "m15", "m29"], "ask": "規模優勢已建立還是仍在積累？"},

    {"id": "m12", "d": "micro", "zh": "護城河",       "en": "Economic Moats", "short": "5 大競爭壁壘", "tag": "長期優勢",
     "body": "企業長期維持高於資本成本的超額報酬的競爭壁壘：無形資產 / 轉換成本 / 網路效應 / 成本優勢 / 有效規模。",
     "quote": '"The key to investing is determining the competitive advantage of any given company." — Buffett',
     "cases": ["See's Candies 50 年累計 $2.1B+", "GEICO 低成本直銷", "Visa 雙邊網路效應"],
     "related": ["m11", "m13"], "ask": "若資本充裕的對手全力進攻，護城河能撐幾年？"},

    {"id": "m13", "d": "micro", "zh": "競爭毀滅",     "en": "Competitive Destruction", "short": "超額利潤吸引競爭", "tag": "長期回歸",
     "body": "長期而言，超額利潤吸引競爭者，技術顛覆與資本湧入侵蝕護城河。",
     "quote": '"Capitalism is brutal — the competitive forces that destroy value are relentless." — Munger',
     "cases": ["Kodak 被數位攝影毀滅", "Nokia 被 iPhone 顛覆，市佔 40% 歸零"],
     "related": ["m12", "m17", "m20"], "ask": "5 年後什麼技術可能取代它？"},

    {"id": "m14", "d": "micro", "zh": "市場先生",     "en": "Mr. Market", "short": "市場服務你，不指引你", "tag": "報價工具",
     "body": "市場每天提供一個報價，但你不必接受。市場是服務你的工具，而非應該跟隨的指引。",
     "quote": '"Mr. Market is there to serve you, not to instruct you." — Ben Graham',
     "cases": ["2020/3 COVID：Amazon 腰斬後漲回 $3,700+", "2022 Meta $88，Munger 買入"],
     "related": ["m7", "m18", "m24"], "ask": "報價是企業本質改變還是情緒波動？"},

    {"id": "m24", "d": "micro", "zh": "機會成本",     "en": "Opportunity Cost", "short": "hurdle rate 的根源", "tag": "資源稀缺", "isNew": True,
     "body": "任何決策都有被放棄的次佳選擇，其潛在價值即為真實成本。Munger 認為機會成本是最被低估的投資概念。",
     "quote": '"The most important thing I learned from Charlie is opportunity cost." — Buffett',
     "cases": ["波克夏現金的機會成本：跑輸 S&P 即虧", "Apple 高 ROIC 回購 vs 過度資本支出"],
     "related": ["m18", "m15", "m26"], "ask": "比 S&P 500 的期望值高出多少？差距夠大嗎？"},

    {"id": "m25", "d": "micro", "zh": "資訊不對稱",   "en": "Information Asymmetry", "short": "alpha 的源頭", "tag": "逆選擇", "isNew": True,
     "body": "交易雙方掌握的資訊量不同，導致市場失靈或定價偏差。投資中的 alpha 往往來自暫時性資訊優勢。",
     "quote": '"The most dangerous person in a negotiation knows what they don\'t know." — Munger',
     "cases": ["保險逆選擇：Akerlof 二手車", "小型股 alpha 最可能來源"],
     "related": ["m1", "m12", "m16"], "ask": "我的資訊優勢從哪裡來？"},

    # ── Math (5)
    {"id": "m15", "d": "math",  "zh": "複利",         "en": "Compound Interest", "short": "時間是最關鍵變數", "tag": "指數成長",
     "body": "收益再投入後持續以指數成長。72 法則：72 ÷ 年化報酬 = 翻倍年數。中斷複利是最大的隱性成本。",
     "quote": '"The first rule of compounding: Never interrupt it unnecessarily." — Munger',
     "cases": ["波克夏 1965-2023 年化 19.8% → $1 變 $43,000", "See's 1972 $25M → 累計 $2.1B+"],
     "related": ["m18", "m11", "m24"], "ask": "換股的摩擦成本需多高超額回報才值得？"},

    {"id": "m16", "d": "math",  "zh": "貝氏更新",     "en": "Bayesian Updating", "short": "更新觀點 ≠ 承認錯誤", "tag": "機率修正",
     "body": "依據既有信念建立假設，隨新資訊持續修正機率估計。確認偏誤的對立面。",
     "quote": '"The test of a first-rate intelligence is the ability to hold two opposed ideas." — Munger',
     "cases": ["波克夏 2016 從不碰航空 → 買入四大航空", "Phase 2 成功更新 Phase 3 機率"],
     "related": ["m6", "m13", "m21"], "ask": "上一次重大改變看法是什麼時候？"},

    {"id": "m17", "d": "math",  "zh": "均值回歸",     "en": "Mean Reversion", "short": "高 ROE 不要外推", "tag": "週期之力",
     "body": "極端表現往往向長期均值靠攏。週期投資與估值分析的基石。有護城河的公司能抗拒。",
     "quote": '"Regression to the mean is the most powerful force in finance." — Munger',
     "cases": ["2000 後 PE 100x+ 回歸 15-20x 失落十年", "能源股循環：油價→資本→供給"],
     "related": ["m14", "m13", "m12"], "ask": "當前 ROE 高於均值多少？是護城河還是週期高點？"},

    {"id": "m26", "d": "math",  "zh": "期望值",       "en": "Expected Value", "short": "EV = 機率 × 賠率", "tag": "加權決策", "isNew": True,
     "body": "所有可能結果乘以其發生機率的加權平均。頻率對不代表思維對，magnitude 同樣重要。",
     "quote": '"How often you\'re right matters less than what happens when you\'re right vs wrong." — Munger',
     "cases": ["保險精算：定價 > 期望損失即獲利", "VC：9 個零 + 1 個 100x = 正 EV"],
     "related": ["m24", "m18", "m27"], "ask": "若成功賺多少？若失敗虧多少？EV 為正嗎？"},

    {"id": "m27", "d": "math",  "zh": "冪次法則",     "en": "Power Law", "short": "20/80 而非常態分佈", "tag": "長尾分佈", "isNew": True,
     "body": "少數節點/事件產生絕大多數影響；結果不服從常態分佈而遵循冪次分佈。",
     "quote": '"The great majority of outcomes are driven by a tiny minority of causes." — Munger',
     "cases": ["AWS：營收 17% 但利潤 70%+", "Sequoia：3 筆貢獻 90%+", "S&P 500：4% 個股貢獻全部超額回報"],
     "related": ["m11", "m12", "m26"], "ask": "這市場是贏家通吃還是分散市場？"},

    # ── Engineering (4)
    {"id": "m18", "d": "eng",   "zh": "安全邊際",     "en": "Margin of Safety", "short": "估值折扣即緩衝", "tag": "核心概念",
     "body": "買入時要求充裕的估值折扣作為緩衝，抵禦錯誤假設與不可預見事件。",
     "quote": '"The margin of safety is the central concept of investment." — Ben Graham',
     "cases": ["BNSF 遠低於重置成本買入", "2022 Meta $88 FCF 收益率 15%+"],
     "related": ["m14", "m15", "m19"], "ask": "若假設全部錯 30%，這倉位還有意義嗎？"},

    {"id": "m19", "d": "eng",   "zh": "冗餘設計",     "en": "Backup & Redundancy", "short": "單點失敗即災難", "tag": "系統韌性",
     "body": "關鍵系統設置備援，單點失敗不造成全體失效。投資中體現為多元分散與壓力測試。",
     "quote": '"Engineers always build in redundancy." — Munger',
     "cases": ["Boeing MAX 單一 AoA 感測器 → 兩次墜機", "LTCM 槓桿 25x 無流動性緩衝"],
     "related": ["m18", "m17"], "ask": "組合有沒有「單點失敗」暴露？"},

    {"id": "m28", "d": "eng",   "zh": "倒推思考",     "en": "Inversion", "short": "Invert, always invert", "tag": "雅各比法則", "isNew": True,
     "body": "將問題反轉，思考「如何確保失敗」以識別應避免的錯誤。Munger 一生引用超過 50 次。",
     "quote": '"Invert, always invert. Turn a situation around. Think it backwards." — Carl Jacobi',
     "cases": ["「如何確保失敗？」→ 過高估值/不懂業務/無護城河/誠信問題 = 篩股反面", "Munger 評估合夥人從黑名單倒推"],
     "related": ["m18", "m19", "m10"], "ask": "這個決策如何確保失敗？我有沒有一一檢查？"},

    {"id": "m29", "d": "eng",   "zh": "臨界質量",     "en": "Critical Mass", "short": "閾值之上即爆炸性增長", "tag": "正回饋", "isNew": True,
     "body": "系統達到某個閾值後，自我強化的正回饋迴路使其爆炸性增長；低於閾值則萎縮。",
     "quote": '"Below critical mass, nothing happens; above it, everything happens." — Munger',
     "cases": ["eBay 雙邊市場飛輪", "WhatsApp/LINE 網路指數增長", "特斯拉超充網跨臨界後成護城河"],
     "related": ["m11", "m12", "m27"], "ask": "是否已跨越臨界？何時會跨越？"},

    # ── Biology (2)
    {"id": "m20", "d": "bio",   "zh": "紅皇后效應",   "en": "Red Queen Effect", "short": "靜止即退步", "tag": "持續演化",
     "body": "為了維持生存優勢，必須不斷演化奔跑，因為競爭者同樣在進化；靜止等同退步。",
     "quote": '"In business, you\'ve got to keep running just to stay in place." — Munger',
     "cases": ["Netflix：DVD→串流→原創→廣告訂閱", "Intel 製程被 TSMC 追上", "Costco 持續壓低毛利率"],
     "related": ["m13", "m19", "m30"], "ask": "這家公司今天比一年前更強還是更弱？"},

    {"id": "m30", "d": "bio",   "zh": "生態棲位",     "en": "Niche Dominance", "short": "專家勝過通才", "tag": "聚焦戰略", "isNew": True,
     "body": "在特定生態位中，高度專化的物種比廣泛競爭的通才更容易取得支配地位。",
     "quote": '"A company that tries to be everything to everybody usually ends up being nothing." — Munger',
     "cases": ["TSMC 純晶圓代工 vs 三星多角化", "Ferrari 毛利率 50%", "Bloomberg Terminal $24K/年仍 30 萬訂戶"],
     "related": ["m12", "m20", "m13"], "ask": "它的「生態位」夠清楚嗎？"},
]
