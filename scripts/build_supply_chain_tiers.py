#!/usr/bin/env python3
"""Render the cross-map **scarcity-bottleneck ranking** into the supply-chain hub
page docs/supply-chain/index.html, between the <!-- TIERS_AUTO_START --> /
<!-- TIERS_AUTO_END --> markers.

WHY THIS IS CURATED, NOT AUTO-DERIVED
-------------------------------------
The previous version of this script auto-grouped companies into 💎 satellite /
🐘 elephant / 🔒 uninvestable tiers straight from each map's `node_role` /
`single` fields. That answered "who is flagged?" — but NOT "how scarce is the
bottleneck really?". True scarcity (T0 = no qualified 2nd source anywhere,
disruption stops the whole industry … down to T3 = over-flagged market leader)
is an editorial judgement about substitutability, qualification time, capacity /
geographic concentration, and blast radius. It cannot be read off a single JSON
field, so the ranking lives here as the single source of truth (the
`T0` / `T1` / `T2` / `OVER` lists below).

The script still ENRICHES each row from the live data: it resolves a DD-report
link per ticker (from data/dd_links.json) and renders topic chips. Re-run after
editing the tier lists (the pre-commit hook also re-runs it, so the hub stays
static and the block never drifts from this file):

    python3 scripts/build_supply_chain_tiers.py

Source of the ranking: docs/supply-chain/audit-2026-06.json (full-site audit,
40 maps / 749 nodes / 67 ⚑, Part 1 deterministic + Part 2 9-cluster sub-agents;
earlier narrative pass: notes/site-internal/supply-chain/_audit_20260529.md, internal).
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SC = ROOT / "docs" / "supply-chain"
DATA = SC / "data"
INDEX = SC / "index.html"

FLAG = {
    "TW": "🇹🇼", "US": "🇺🇸", "JP": "🇯🇵", "KR": "🇰🇷", "CN": "🇨🇳", "NL": "🇳🇱",
    "DE": "🇩🇪", "EU": "🇪🇺", "IL": "🇮🇱", "HK": "🇭🇰", "SG": "🇸🇬", "CH": "🇨🇭",
    "UK": "🇬🇧", "FR": "🇫🇷", "AT": "🇦🇹", "DK": "🇩🇰", "SE": "🇸🇪", "GLOBAL": "🌐",
}

# ── Curated scarcity ranking ────────────────────────────────────────────────
# Each entry = one bottleneck (the NODE, not the company). `sup` lists the key
# supplier(s) as (name, ticker, country); ticker "" → private / no pure-play.
# `topics` = map ids it shows up in (rendered as chips, linked to the map).
# `verdict` = curated rationale: substitutability · qual time · blast radius · decay.

T0 = [
    {
        "name": "EUV 垂直線（光學 → 光源 → 曝光機）",
        "sup": [("ZEISS SMT", "", "DE"), ("Cymer / Trumpf", "", "US"), ("ASML", "ASML", "NL")],
        "topics": ["fe-equipment", "advanced", "hbm", "lpddr"],
        "verdict": "全站最純 T0。ZEISS 是唯一能做 sub-nm 多反射鏡系統者，重建替代路線 &gt;10 年；ASML 年產 ~90 台本身就是全行業擴產硬上限。不是「未認證」而是「第二產品線不存在」。真正脆弱點藏在 ASML 上游（光學 / 光源）。",
    },
    {
        "name": "Lasertec actinic EUV 光罩 / 光罩基板檢測",
        "sup": [("Lasertec", "6920.T", "JP")],
        "topics": ["metrology"],
        "verdict": "全站被漏掉的最純單點之一。actinic（13.5nm 波長）EUV 光罩檢測 ~100% + 光罩基板 actinic 檢測同為全球唯一商用機台 —— 地球上沒有第二家量產設備。常被拿來當替代的 Zeiss AIMS EUV 只是 R&D 級 aerial-image 工具、非產線缺陷篩檢，不構成二供。每座跑 EUV 的 fab（TSMC / Samsung / Intel）都依賴它，High-NA 量產（ACTIS A200HiT, 2025/10）同樣無檢測路徑可繞 —— 爆炸半徑等同 ASML / TEL 出貨歸零，卻長期被排在 ASML 級風險討論之外。唯一折價：日本單一國集中、多光束電子束檢測為遠期潛在替代。",
    },
    {
        "name": "Ajinomoto 味之素 ABF 增層膜",
        "sup": [("味之素 Ajinomoto", "2802.T", "JP")],
        "topics": ["cowos", "substrate", "plp", "hbm", "material"],
        "verdict": "5 圖共識的材料端最深單點，95–98%。<strong>耗材</strong>屬性使斷供數週內全 AI 載板停線；換膜＝全堆疊重認證 2–3 年。2026/5 宣布 Q3 漲價 30% 而零客戶流失，是壟斷定價力的行為證據。唯一不給「無限 T0」的理由：技術上有替代介電膜路線、且基板廠有庫存緩衝。",
    },
    {
        "name": "TSMC 先進製程（N3 / N2 + CoWoS）",
        "sup": [("台積電 TSMC", "2330.TW", "TW")],
        "topics": ["asic", "cowos", "dc-networking", "icdesign", "advanced", "hbm"],
        "verdict": "對已 tape-out 的設計零替代性（重 tape-out 18–30 月 + 數億美元 NRE）；先進產能 ~90% 集中台灣單一島嶼，地緣風險不可分散；40 張圖的主節點同時引爆。替代「架構」（EMIB / I-Cube）存在且委外生態已運轉，故 CoWoS 環節屬 T1。",
    },
    {
        "name": "鋰-6 同位素（D-T 融合氚增殖）",
        "sup": [("DOE / ORNL legacy（未上市）", "", "US")],
        "topics": ["fusion"],
        "verdict": "經查證成立：西方自 1963 年 COLEX 停運後無商業產能，新進者（Hexium AVLIS）僅實驗室示範；俄中存量受地緣封鎖。D-T 增殖毯物理上必須、建廠 5–10 年。唯一折價是引信遞延 — 硬約束在 2030 年代商業艦隊，2026–2030 需求量極小。",
    },
]

T1 = [
    {
        "name": "200G/lane EML 雷射",
        "sup": [("Lumentum", "LITE", "US"), ("Coherent", "COHR", "US")],
        "topics": ["transceiver", "cpo"],
        "verdict": "1.6T 模組唯一可行光源。實況比地圖寫的<strong>更緊</strong>：Lumentum 是目前唯一以 volume 出貨者、Coherent 仍在 ramp，全部容量被 LTA 鎖至 2027。對非 LTA 買家在 12 個月窗口內是<strong>功能性 T0</strong> — 全站唯一「現在就買不到」的節點。",
    },
    {
        "name": "TEL EUV coater / developer",
        "sup": [("Tokyo Electron", "8035.T", "JP")],
        "topics": ["fe-equipment", "advanced"],
        "verdict": "全球 ~88%、<strong>EUV 應用 ~100%</strong>，每台 EUV scanner 必配。SCREEN 僅低階機型，EUV track requalify 估 3–5 年。爆炸半徑等同 ASML 出貨歸零，卻很少被當成 ASML 級風險討論。",
    },
    {
        "name": "Advantest AI / GPU SoC 測試",
        "sup": [("Advantest", "6857.T", "JP")],
        "topics": ["metrology", "ate"],
        "verdict": "AI / GPU SoC 測試 ~70–80%（CY25 SoC 整體 56%→66%），NVIDIA Blackwell 量產指定 V93000 + ACS RTDI；GPU 運算 die 今日無合格二供，轉測需 socket 重設計 + test program 移植 + OSAT 重認證 12–24 月。<strong>carve-out</strong>：Teradyne Magnum 7H 在 <strong>HBM 記憶體測試</strong>為真二供且放量中 —— 故記憶體側屬 T2、GPU compute die 側才是 T1。lead time 已 &gt;6 個月、2026 機台產能 3K→5K 仍緊，是 AI 晶片 final test 的隱形咽喉。",
    },
    {
        "name": "Nittobo T-Glass 玻纖布",
        "sup": [("日東紡 Nittobo", "3110.T", "JP")],
        "topics": ["substrate", "ai-pcb"],
        "verdict": "~90%。同時掐住 AI ABF、BT（HBM4 載板）、M8/M9 CCL 三條線 — 2026「量」上最緊的瓶頸。2027 中產能 3 倍化後供需反轉路徑明確；低規 NE/E-glass 有降規逃生門。",
    },
    {
        "name": "台光電 NVIDIA AI CCL（客戶獨家）",
        "sup": [("台光電 Elite Material", "2383.TW", "TW")],
        "topics": ["ai-pcb"],
        "verdict": "M9 目前唯一合格供應商（獨家是<strong>現在進行式</strong>，非地圖寫的過去式）；M-grade 認證 + co-design &gt;18 月。M10 起 NVIDIA 已引入 2 家隱藏供應商（1 中 1 台），有明確 2027 衰減期限。",
    },
    {
        "name": "Soitec RF-SOI / FD-SOI 工程基板",
        "sup": [("Soitec", "SOI.PA", "FR")],
        "topics": ["wireless", "mature-node"],
        "verdict": "教科書級「專利（Smart Cut）＋物理產能」雙鎖。幾乎每支手機的 RF 開關 / 天線調諧 / FEM 必經；Shin-Etsu 有授權量產但規格 / 產能覆蓋不足，foundry requalify 18–30 月。",
    },
    {
        "name": "ASPEED 信驊 BMC 管理晶片",
        "sup": [("信驊 ASPEED", "5274.TWO", "TW")],
        "topics": ["dc-networking", "server"],
        "verdict": "「小晶片大鎖喉」典型：~70%，單價低但無 BMC 無法出貨任何伺服器。驗證週期 2–3 年 + 韌體深綁（OpenBMC 生態核心）。Nuvoton &lt;10% 為合格二供但產能 / 平台覆蓋遠不足。",
    },
    {
        "name": "TSMC HBM4 base die / COUPE PIC 代工",
        "sup": [("台積電 TSMC", "2330.TW", "TW")],
        "topics": ["memory", "cpo", "siph"],
        "verdict": "對 SK Hynix / Micron 的 HBM4 base die 為 100% 獨家（12nm-class logic）；NVIDIA / AMD 的 CPO COUPE 路線無第二家可移植。換 foundry＝redesign + qual &gt;24 月。Samsung 自家 turnkey 證明替代架構在產業層面存在，故非 T0。",
    },
    {
        "name": "Namics MR-MUF EMC（SK Hynix 客戶獨家）",
        "sup": [("Namics（未上市）", "", "JP")],
        "topics": ["hbm"],
        "verdict": "對 SK Hynix 的 MR-MUF 製程今日為零二供（材料與製程 co-developed）；半徑＝全球過半 HBM 供給的材料咽喉。但稀缺性衰減中：獨家合約 ~2027 到期、CXMT 已開始複製、HBM4E hybrid bonding 會結構性降低 EMC 依賴 — 「現在很硬、三年後變普通」。",
    },
    {
        "name": "Mitsui Chemicals EUV pellicle（光罩保護膜）",
        "sup": [("Mitsui Chemicals", "4183.T", "JP")],
        "topics": ["material", "advanced", "fe-equipment"],
        "verdict": "唯一獲 ASML / IMEC 授權的外供 EUV pellicle 廠（ASML 已把組裝 + 配銷轉給 Mitsui）。但這是<strong>衰減中</strong>的獨家：TSMC 自 Fab 3 已自製 CNT pellicle、Samsung 量產暫不用 pellicle 且規畫轉 FST / S&S Tech 韓系供應 —— 兩大 EUV 用戶各自絕緣後，斷供爆炸半徑遠小於 ABF，剩 Intel 為 swing client。耗材屬性（每 2–6 月換）使短期仍有供給風險、requalify 12–18 月；Mitsui 反攻點在岩國 CNT 廠（2025/12 完工、&gt;1kW、High-NA ready）。",
    },
    {
        "name": "Mitsui Mining HVLP 高速銅箔",
        "sup": [("Mitsui Mining & Smelting", "5706.T", "JP")],
        "topics": ["ai-pcb"],
        "verdict": "M9 級 Rz&lt;0.5μm 規格領先 ≥1 世代 + 與台光電 co-design 綁定。JX / Furukawa 有降規二供（故非字面 monopoly），但 12 個月 kill test 確實不過，&gt;18 月 qual。",
    },
    {
        "name": "Centrus HALEU 濃縮燃料",
        "sup": [("Centrus Energy", "LEU", "US")],
        "topics": ["nuclear"],
        "verdict": "西方唯一在產 HALEU 濃縮商屬實（Urenco USA 授權僅至 10% U-235、Capenhurst HALEU 2031）。但保鮮期 3–5 年（DOE 2024/10 已另授 Urenco / Orano / General Matter）；累計實際產量僅 ~900 kg 屬示範量級。爆炸半徑限 Gen-IV（Oklo / X-energy）。",
    },
    {
        "name": "P&W F135 發動機（F-35 唯一動力）",
        "sup": [("RTX（Pratt & Whitney）", "RTX", "US")],
        "topics": ["defense"],
        "verdict": "F-35 全機隊唯一發動機，GE XA100 替代案 2023 被否（ECU 路線鎖到 2070），&gt;1,300 架機隊無 12 月替代可能 — 國防三 ⚑ 中唯一真正的「供應」單點。折價：買方是單一 monopsony（DoD 有成本稽核權），sole-source ≠ 自由定價權。",
    },
    {
        "name": "Credo AEC 主動電纜晶片",
        "sup": [("Credo Technology", "CRDO", "US")],
        "topics": ["copper", "dc-networking"],
        "verdict": "~73%（650 Group Q2'25）領導，AWS/MSFT/xAI/Meta 多客。但 AEC 是<strong>方案層</strong>而非元件層瓶頸：短距可退 DAC、長距可上光模組；Marvell / Astera 切入中；6–12 月 qual 遠短於 foundry / BMC。Amazon 占比 86%→61% 反映需求端在分散。",
    },
]

T2 = [
    {
        "name": "大型燃氣渦輪機三強（自帶發電）",
        "sup": [("GE Vernova", "GEV", "US"), ("Siemens Energy", "ENR.DE", "DE"), ("三菱重工", "7011.T", "JP")],
        "topics": ["datacenter"],
        "verdict": "T2 中實際稀缺度最高 — backlog 已達 100GW、2029+2030 殘餘 slot 僅 ~10GW、預期 2026 年底前售罄至 2030；是美國 AI DC 動工的關鍵路徑（12GW 規劃僅 5GW 動工）。18–24 月無法 qualify 第四家、數十年無新進者。",
    },
    {
        "name": "HBM 三強 cartel",
        "sup": [("SK Hynix", "000660.KS", "KR"), ("Samsung", "005930.KS", "KR"), ("Micron", "MU", "US")],
        "topics": ["hbm", "memory", "neocloud", "lpddr"],
        "verdict": "本質是 cartel 不是單點：客戶可三家 dual-source（NVIDIA 三家都 qual），單一斷供半徑 ≤ 其市佔。$30B/fab 進入障礙真實、CXMT 5 年內做不出 HBM-grade。實際 Q3'25 市佔 SK ~57% / Samsung 22% / Micron 21%。",
    },
    {
        "name": "DDR5 RCD / DB 三雄（JEDEC cartel）",
        "sup": [("Montage 瀾起", "688008.SS", "CN"), ("Rambus", "RMBS", "US"), ("Renesas", "6723.T", "JP")],
        "topics": ["cxl"],
        "verdict": "每條 DDR5 RDIMM/LRDIMM 必裝 RCD；≥95%、DDR4 起十年無新進者。但三雄 drop-in 互換性高 — 任一斷供客戶數月內轉單其餘兩家。cartel 整體無可替代、cartel 內彈性比 DRAM 三強更大；中國籍 Montage 有出口管制暴露。",
    },
    {
        "name": "EUV mask blank 雙頭壟斷",
        "sup": [("AGC", "5201.T", "JP"), ("HOYA", "7741.T", "JP")],
        "topics": ["fe-equipment", "material", "metrology"],
        "verdict": "~93% 合計。互為二供但任一停供另一方產能無法吸收（EUV blank 良率極低、擴產以年計），S&S Tech 仍在 R&D。單一國家（日本）集中是真實地緣風險。龍頭排名隨統計口徑（金額 vs by-volume）互換。",
    },
    {
        "name": "BaTiO₃ 鈦酸鋇奈米粉",
        "sup": [("Sakai Chemical 堺化學", "4078.T", "JP"), ("Fuji Titanium", "", "JP")],
        "topics": ["passive"],
        "verdict": "高階 &lt;100nm 粉體雙寡占 &gt;70%。但 Murata 相當比例垂直整合自製、SEMCO 有備援，次梯隊（Nippon Chemical / Resonac）存在 → 「斷供影響所有 MLCC」屬高估。換粉重認證 1–2 年。",
    },
]

OVER = [
    {
        "name": "Broadcom 客製 ASIC 設計服務 70%+",
        "sup": [("Broadcom", "AVGO", "US")],
        "topics": ["asic", "dc-networking"],
        "verdict": "市場領導 ≠ 鎖喉點。Google 刻意三供應商策略、AWS 已從 Marvell 換到 Alchip（實際發生）；設計服務的「產能」是工程師 + IP 庫，無物理產能牆。70% 是贏來的不是鎖住的 → 應降為寡占龍頭 alpha。",
    },
    {
        "name": "NVIDIA NVLink scale-up",
        "sup": [("NVIDIA", "NVDA", "US")],
        "topics": ["dc-networking", "icdesign", "neocloud", "robot"],
        "verdict": "循環論證式 ⚑：自家產品內建元件，沒有第三方「採購 NVLink 斷供」的情境。UALink 1.0 規格 2025/4 已發 + NVLink Fusion 2025/5 開放第三方。屬<strong>平台護城河</strong>（NVDA 投資論點），非供應鏈單點 → 移出 ⚑ 池。",
    },
    {
        "name": "ARM 車用 CPU IP「唯一可行核心」",
        "sup": [("ARM Holdings", "ARM", "UK")],
        "topics": ["auto-soc", "icdesign", "mobile-ap", "asic"],
        "verdict": "headline thesis 級事實錯誤：Infineon AURIX = TriCore、Renesas RH850 自有核、NXP 傳統線 = Power e200，皆<strong>非 ARM 核</strong>，且與同檔 mc-mcu 節點自相矛盾。ARM 真強在高算力 ADAS / 座艙 SoC 層 → ⚑ 須限縮到該層。",
    },
    {
        "name": "Jericho 4「唯一商用解」",
        "sup": [("Broadcom", "AVGO", "US")],
        "topics": ["dc-networking"],
        "verdict": "已被事實推翻：Cisco 8223 / Silicon One P200（2025/10）與 NVIDIA Spectrum-XGS（2025/8）皆為商用 scale-across 競品（地圖自己引的來源正是報導此事）→ grade 改 oligopoly、撤 ⚑ 或改寫為「deep-buffer / HBM 架構先行者」。",
    },
    {
        "name": "SiC 200mm「雙占窗口」",
        "sup": [("Wolfspeed", "WOLF", "US"), ("Coherent", "COHR", "US")],
        "topics": ["auto-semi"],
        "verdict": "2026 中已弱化：ROHM/SiCrystal、ST（Catania 自製）、中國 SICC / 天科合達 200mm 已實際出貨，且整體 SiC 供過於求、價格戰。供過於求 + 龍頭剛走完破產重整，很難同時是「真單點窗口」→ 降「窗口關閉中、2026 重評」。",
    },
    {
        "name": "DNP TGV 玻璃 core substrate",
        "sup": [("DNP 大日本印刷", "7912.T", "JP")],
        "topics": ["substrate"],
        "verdict": "標 monopoly 但這是<strong>尚未存在的市場</strong>：DNP 試線、Absolics 2026 底量產目標、Intel/Amkor/LPKF/Corning 全在賽道上。五家以上競逐、零家量產＝emerging，無斷供爆炸半徑可言（今天沒人依賴它）。",
    },
    {
        "name": "F-35 / Lockheed（程序壟斷）",
        "sup": [("Lockheed Martin", "LMT", "US")],
        "topics": ["defense"],
        "verdict": "「唯一可出口 5th gen」是事實，但 ⚑ 框架問「斷供時下游無替代」— 這裡下游是主權買家，而美政府擁有 program + 設計資料權，且 FY26 砍單 ~36% 示範了議價權。是 program-structural monopoly，租值被 monopsony 捕獲，非 scarcity rent → T2/T3。",
    },
    {
        "name": "LEENO 超精密探針 >70%",
        "sup": [("LEENO Industrial", "058470.KQ", "KR")],
        "topics": ["ate"],
        "verdict": "&gt;70% 為自報數字；日系探針廠（Kita / Yokowo）與 socket 廠自製 pin 是現役替代，pin requalify 週期數月到一年、非多年。是「強寡占龍頭」不是「能力鎖喉」→ 移出 ⚑ 池。",
    },
    {
        "name": "NVIDIA 太空級 GPU",
        "sup": [("NVIDIA", "NVDA", "US")],
        "topics": ["spacedc"],
        "verdict": "「H100 首個入軌」事實成立，但這是<strong>需求端選型</strong>不是供給端稀缺：commercial GPU 是 COTS 商品，太空保護靠 shielding+ECC，無認證壁壘可言（與 rad-hard CPU 不同）→ 撤 ⚑，改掛生態系敘述。",
    },
]


LAG_SCORE = {">5y": 3, "2-5y": 2, "<2y": 1, "replaceable": 0}
LAG_LABEL = {">5y": ">5 年", "2-5y": "2-5 年", "<2y": "<2 年", "replaceable": "可替代"}


def load_mechanical():
    """機械層（2026-07-09 兩層制）：substitution_lags.json（替代難度，Opus 逐節點判定）
    × terminal_markets.json（終端封鎖值，每鏈最下游產出市場）→ 節點瓶頸強度分。
    任一 sidecar 缺 → 回傳 None（純 curated 模式，pre-commit 不受影響）。
    分數 = 替代難度(0-3) × 終端市場(USD B)——刻意不用節點自身 marketSize，
    防「小節點大封鎖」（味之素 ABF 型）被市場規模埋掉。"""
    tm_p = DATA / "terminal_markets.json"
    sl_p = DATA / "substitution_lags.json"
    if not (tm_p.exists() and sl_p.exists()):
        return None
    try:
        tm = {r["topic"]: r for r in json.loads(tm_p.read_text(encoding="utf-8"))["markets"]}
        sl = json.loads(sl_p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return None
    node_cache = {}
    def node_info(topic, nid):
        if topic not in node_cache:
            p = DATA / f"{topic}.json"
            try:
                node_cache[topic] = {n.get("id"): n for n in json.loads(p.read_text(encoding="utf-8")).get("nodes", [])}
            except Exception:
                node_cache[topic] = {}
        return node_cache[topic].get(nid) or {}
    rows = []
    for r in sl.get("lags", []):
        w = (tm.get(r["topic"]) or {}).get("terminal_market_usd_b") or 0
        score = LAG_SCORE.get(r.get("tier"), 0) * w
        if score <= 0:
            continue
        nd = node_info(r["topic"], r.get("node_id"))
        tickers = []
        for c in nd.get("companies", []):
            raw = (c.get("ticker") or "").strip()
            for tk in re.split(r"[/,、]", raw):
                tk = tk.strip()
                if tk and tk not in {"—", "-", "–", "N/A", "n/a", "未上市"}:
                    tickers.append(tk)
        rows.append({"topic": r["topic"], "node_id": r.get("node_id"),
                     "name": nd.get("name") or r.get("node_id"), "tier": r.get("tier"),
                     "note": r.get("note", ""), "terminal": w, "score": score,
                     "tickers": tickers[:4]})
    rows.sort(key=lambda x: -x["score"])
    return {"rows": rows, "as_of": sl.get("as_of", "?"), "n": len(rows)}


def curated_ticker_set():
    out = set()
    for e in T0 + T1 + T2:
        for _name, tk, _c in e.get("sup", []):
            if tk:
                out.add(tk.upper())
    return out


def mechanical_html(mech, dd_links) -> str:
    """機械層對帳段：top-15 分數表＋curated 收錄狀態。提名不自動入榜——
    「機械高分 × curated 未收」＝漏網提名（防小產業被編輯視野漏掉的系統性保險），
    由持有人複審後手動改 T0/T1/T2 清單。"""
    curated = curated_ticker_set()
    h = ['<h3 class="tier-mech"><span class="ico">⚙️</span>機械層對帳 · '
         f'替代難度 × 終端封鎖值（{mech["n"]} 節點打分，as-of {esc(mech["as_of"])}）</h3>']
    h.append('<p class="lede">上方分級是<strong>編輯判斷</strong>；本表是機械層挑戰者——'
             '分數 = 替代難度（>5 年 = 3 / 2-5 年 = 2 / <2 年 = 1）× 該鏈終端市場（USD B，'
             '刻意不用節點自身規模，防小節點大封鎖被埋）。'
             '<strong>「未收錄」= 漏網提名</strong>，複審後才入上方分級，不自動晉升。</p>')
    h.append('<div style="overflow-x:auto"><table class="tier-mech-tbl"><thead><tr>'
             '<th>節點</th><th>鏈</th><th>替代難度</th><th>終端市場</th><th>分數</th>'
             '<th>關鍵廠商</th><th>編輯層</th></tr></thead><tbody>')
    for r in mech["rows"][:15]:
        if not r["tickers"]:
            status = '私有/無 ticker（人工對帳）'
        elif any(tk.upper() in curated for tk in r["tickers"]):
            status = '✓ 已收錄'
        else:
            status = '<strong style="color:#b45309">未收錄 → 複審提名</strong>'
        h.append(f'<tr><td>{esc(r["name"])}<br><small>{esc(r["note"][:48])}</small></td>'
                 f'<td>{topic_chips([r["topic"]])}</td>'
                 f'<td>{esc(LAG_LABEL.get(r["tier"], r["tier"]))}</td>'
                 f'<td>${r["terminal"]:g}B</td><td><strong>{r["score"]:g}</strong></td>'
                 f'<td>{esc(" / ".join(r["tickers"]) or "—")}</td><td>{status}</td></tr>')
    h.append('</tbody></table></div>')

    # 公司級聚合：同公司跨鏈稀缺節點分數加總（分攤同節點多供應商），
    # 治「系統級瓶頸被節點×單鏈計分切碎」——TSMC 先進製程跨 N 鏈各算一次、
    # 每鏈分數不高，公司級加總才還原其全局瓶頸地位（與節點視圖互補）。
    comp = {}
    for r in mech["rows"]:
        n = max(len(r["tickers"]), 1)
        for tk in r["tickers"]:
            c = comp.setdefault(tk, {"score": 0.0, "chains": set(), "nodes": 0, "best": None})
            c["score"] += r["score"] / n
            c["chains"].add(r["topic"])
            c["nodes"] += 1
            if c["best"] is None or r["score"] > c["best"][1]:
                c["best"] = (r["name"], r["score"])
    top = sorted(comp.items(), key=lambda kv: -kv[1]["score"])[:10]
    h.append('<h4 class="tier-mech-co">公司級聚合 · 跨鏈瓶頸分加總 top-10（同節點多供應商分攤計分）</h4>')
    h.append('<div style="overflow-x:auto"><table class="tier-mech-tbl"><thead><tr>'
             '<th>公司</th><th>聚合分</th><th>跨鏈數</th><th>稀缺節點數</th><th>最大單一瓶頸</th><th>編輯層</th></tr></thead><tbody>')
    curated2 = curated
    for tk, c in top:
        status = '✓' if tk.upper() in curated2 else '<strong style="color:#b45309">未收錄</strong>'
        h.append(f'<tr><td><strong>{esc(tk)}</strong></td><td><strong>{c["score"]:.0f}</strong></td>'
                 f'<td>{len(c["chains"])}</td><td>{c["nodes"]}</td>'
                 f'<td>{esc(c["best"][0][:26])}（{c["best"][1]:g}）</td><td>{status}</td></tr>')
    h.append('</tbody></table></div>')
    return "\n".join(h)


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def load_dd_links() -> dict:
    p = DATA / "dd_links.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def supplier_html(sup, dd_links) -> str:
    out = []
    for name, tk, country in sup:
        flag = FLAG.get(country, "")
        tk = (tk or "").strip()
        tk_html = f'<span class="tk">{esc(tk)}</span>' if tk and tk != "—" else ""
        dd = dd_links.get(tk) if tk else None
        dd_btn = (f' <a href="{esc(dd)}" class="dd-link" target="_blank" rel="noopener" '
                  f'title="開啟 DD 報告">DD ↗</a>') if dd else ""
        out.append(f'<span class="gold-co"><span class="co-flag">{flag}</span>'
                   f'<strong>{esc(name)}</strong>{tk_html}</span>{dd_btn}')
    return f'<div class="sc-supp">{"".join(out)}</div>'


def topic_chips(topics) -> str:
    return "".join(
        f'<a class="gold-node-chip" href="{esc(t)}.html">{esc(t)}</a>' for t in topics
    )


def row_html(e, dd_links) -> str:
    return (f'<tr><td><div class="sc-bn">{e["name"]}</div>'
            f'{supplier_html(e["sup"], dd_links)}</td>'
            f'<td>{topic_chips(e["topics"])}</td>'
            f'<td><span class="gold-single">{e["verdict"]}</span></td></tr>')


def table_html(entries, cls, dd_links, head0) -> str:
    body = "".join(row_html(e, dd_links) for e in entries)
    return (f'<div class="gold-table-wrap"><table class="gold-table {cls}">'
            f'<thead><tr><th>{head0}</th><th>出現產業</th><th>替代性裁決</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def build_block(dd_links) -> str:
    h = []
    h.append('<h3 class="tier-t0"><span class="ico">🔴</span>T0 · 全球真單點 · '
             f'{len(T0)} 條 — 無合格二供，斷供即全產業停擺</h3>')
    h.append('<p class="lede">無 ANY 合格二供、替代路線需以「年」甚至「十年」計、'
             '產能與地理高度集中、斷供爆炸半徑直達整條 AI / 半導體經濟。'
             '<em>這五條是 PM 唯一必須持續盯的結構性斷點。</em></p>')
    h.append(table_html(T0, "tier-t0-tbl", dd_links, "瓶頸 / 關鍵供應商"))

    h.append('<h3 class="tier-t1"><span class="ico">🟠</span>T1 · 近單點 · '
             f'{len(T1)} 條 — 二供驗證中或產能遠不足（alpha 最濃的一層）</h3>')
    h.append('<p class="lede">結構壟斷真實，但存在「正在 ramp 的替代者」或「降規逃生門」，'
             '依「現在就買不到」的緊迫度排序。'
             '<em>投資上最有 alpha — 鎖喉強度足以推動 EPS，但須盯各自的衰減時間表。</em></p>')
    h.append(table_html(T1, "tier-t1-tbl", dd_links, "瓶頸 / 關鍵供應商"))

    h.append('<h3 class="tier-t2"><span class="ico">🟣</span>T2 · Cartel 結構鎖喉 · '
             f'{len(T2)} 條 — 整體無可替代，但 cartel 內可分流</h3>')
    h.append('<p class="lede">不是單一供應商獨佔，而是 3 家左右的寡占 / cartel。'
             '客戶可在 cartel 內 dual-source，單一廠斷供半徑 ≤ 其市佔；'
             '整體進入障礙（capex / 認證 / 數十年無新進者）才是真鎖喉。</p>')
    h.append(table_html(T2, "tier-t2-tbl", dd_links, "瓶頸 / 關鍵供應商"))

    h.append('<h3 class="tier-over"><span class="ico">⚪</span>過度標示 · '
             f'{len(OVER)} 條 — ⚑ 應降級（市場領導 ≠ 供應瓶頸）</h3>')
    h.append('<p class="lede">原圖打了 ⚑ / monopoly，但經冷讀後判定<strong>不是供應斷點</strong>：'
             '① 市場領導但客戶可換且正在換（Broadcom ASIC / NVLink / LEENO / 太空 GPU / F-35）；'
             '② 事實已被競品推翻（Jericho 4 / SiC 200mm / ARM 車用核）；'
             '③ 市場根本還不存在（DNP TGV）。<em>讀者不應據此 over-weight。</em></p>')
    h.append(table_html(OVER, "tier-over-tbl", dd_links, "被過度標示的節點"))

    mech = load_mechanical()
    if mech:
        h.append(mechanical_html(mech, dd_links))

    h.append('<p class="gold-foot">稀缺分級為<strong>編輯判斷</strong>（可替代性 · 認證 / 切換時間 · '
             '產能 / 地理集中度 · 斷供爆炸半徑），單一資料源在 '
             '<code>scripts/build_supply_chain_tiers.py</code> 的 <code>T0/T1/T2/OVER</code> 清單，'
             'DD 連結由 <code>data/dd_links.json</code> 自動解析；機械層輸入為 '
             '<code>data/terminal_markets.json</code> ＋ <code>data/substitution_lags.json</code>。'
             '完整審計（40 maps / 749 nodes / 67 ⚑）見 '
             '<code>docs/supply-chain/audit-2026-06.json</code>'
             '（早期敘述版存 repo 內部 notes/site-internal/supply-chain/）。</p>')
    return "\n".join(h)


def main() -> int:
    dd_links = load_dd_links()
    block = build_block(dd_links)
    txt = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r"(<!-- TIERS_AUTO_START -->).*?(<!-- TIERS_AUTO_END -->)", re.S)
    if not pat.search(txt):
        print("ERROR: markers not found in index.html")
        return 1
    new = pat.sub(lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}", txt)
    INDEX.write_text(new, encoding="utf-8")
    print(f"injected scarcity ranking: 🔴 {len(T0)} / 🟠 {len(T1)} / 🟣 {len(T2)} / "
          f"⚪ {len(OVER)} into {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
