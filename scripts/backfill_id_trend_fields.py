#!/usr/bin/env python3
"""Backfill trend/decision fields into v2.x canonical ID id-meta JSON blocks.

Adds (additive; never removes existing keys):
  - sd_verdict          : shortage / balanced / surplus / split
  - sd_verdict_detail   : only when sd_verdict == "split"
  - clock_phase         : I / II / III / IV
  - conviction          : high / mid / low
  - kill_metrics        : [{metric, bear_threshold, window, source?}, ...]
  - demand_5y_multiple  : round((1+cagr_pct_5y/100)**5, 1) when tam+cagr present
  - related_tickers[].mcap_bucket : mega/large/mid/small (curated, high-confidence only)
  - purity_pct          : only when report states an explicit revenue-dependence %

Sources in the v2.3 "精煉版 / 減法哲學" template:
  - sd_verdict / conviction / clock_phase : `.dsum-col.now` NOW box, `.timeline`
    first phase-title, scenario-set chapter-intro. Auto-extraction is heuristic;
    a hand-curated OVERRIDES table (built after reading each report) is authoritative.
  - kill_metrics : `.monitor-item` PM 監測點 blocks (falsification tripwires;
    "任一轉弱降一級 conviction"). Fallback: inline "⚠ 證偽" markers.

Workflow:
  1. python3 scripts/backfill_id_trend_fields.py --draft   # dump /tmp draft + evidence
  2. (human review; corrections captured in OVERRIDES below)
  3. python3 scripts/backfill_id_trend_fields.py --write    # inject into id-meta

skill_version is left untouched (backfill != version bump).
Style ref: scripts/backfill_id_meta.py
"""
from __future__ import annotations
import argparse, json, re, glob, os, sys, html
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"
DRAFT = Path("/tmp/id_trend_draft.json")
EXCLUDE = {"ID_BackEndPackagingEquipment_20260702.html"}

ID_META_RE = re.compile(r'(<script\s+id="id-meta"[^>]*>)(.*?)(</script>)', re.DOTALL)

# ---- curated market-cap buckets (early-2026; high-confidence only) ----------
# mega >$200B | large $10-200B | mid $2-10B | small <$2B.  Skip if unsure.
MCAP = {
 # --- mega (>$200B) ---
 "NVDA":"mega","MSFT":"mega","AAPL":"mega","AMZN":"mega","GOOGL":"mega","GOOG":"mega",
 "META":"mega","AVGO":"mega","TSLA":"mega","LLY":"mega","JPM":"mega","V":"mega","MA":"mega",
 "WMT":"mega","COST":"mega","ORCL":"mega","NFLX":"mega","ASML":"mega","2330.TW":"mega","TSM":"mega",
 "NVO":"mega","UNH":"mega","BAC":"mega","KO":"mega","AMD":"mega","CRM":"mega","HD":"mega",
 "PG":"mega","XOM":"mega","BABA":"mega","SAP":"mega","NKE":"mega","LIN":"mega","MC":"mega",
 "RMS":"mega","CSCO":"mega","IBM":"mega","GE":"mega","CAT":"mega","MCD":"mega","PEP":"mega",
 "AXP":"mega","MS":"mega","GS":"mega","RTX":"mega","QCOM":"mega","TXN":"mega","INTU":"mega",
 "AMGN":"mega","PDD":"mega","UBER":"mega","NOW":"mega","BLK":"mega","HON":"mega","ADBE":"mega",
 "PLTR":"mega","ARM":"mega","BX":"mega","SIE.DE":"mega","7203.T":"mega","NSRGY":"mega","SBUX":"mega",
 # --- large ($10-200B) ---
 "MRVL":"large","INTC":"large","MU":"large","VRT":"large","CRWD":"large","PANW":"large","FTNT":"large",
 "ETN":"large","AMAT":"large","LRCX":"large","KLAC":"large","005930.KS":"large","000660.KS":"large",
 "BKNG":"large","NET":"large","ZS":"large","SHOP":"large","DASH":"large","ABNB":"large","EXPE":"large",
 "DAL":"large","UAL":"large","BA":"large","LULU":"large","DECK":"large","HLT":"large","MAR":"large",
 "COF":"large","DPZ":"large","TXRH":"large","CMG":"large","DRI":"large","TSN":"large","YUM":"large",
 "APD":"large","MELI":"large","BESI.AS":"large","SU.PA":"large","AIR.PA":"large","ROK":"large",
 "COHR":"large","WDC":"large","WDAY":"large","TEAM":"large","HUBS":"large","OKTA":"large","S":"large",
 "PYPL":"large","FI":"large","GPN":"large","JD":"large","BAC":"large","IHG":"large","GD":"large",
 "LMT":"large","NOC":"large","CTVA":"large","NTR":"large","CF":"large","MOS":"large","LEN":"large",
 "DHI":"large","NVR":"large","BK":"large","GEV":"large","CCJ":"large","RCL":"large","NCLH":"large",
 "CCL":"large","CFR":"large","H":"large","C":"large","LUV":"large","ONON":"large","VIK":"large",
 "RvR":"large","TGT":"large","ORLY":"large","WPP":"large","NYT":"large","2454.TW":"large","2308.TW":"large",
 "HWM":"large","ADYEN":"large","SQ":"large","XYZ":"large","TOST":"large","FOUR":"large","UBER":"large",
 "SNDK":"large","TER":"large","6857.T":"large","6146.T":"large","3037.TW":"large","DE":"large",
 "AGCO":"large","CNH":"large","LIN":"large","BAYN.DE":"large","8035.T":"large","HSY":"large",
 "KHC":"large","MDLZ":"large","MET":"large","PRU":"large","SE":"large","CPNG":"large","NU":"large",
 "DELL":"large","ANET":"large","APH":"large","SMCI":"large","AMKR":"large","ON":"large","NXP":"large",
 "SNPS":"large","CDNS":"large","KEYS":"large","ZTS":"large","MNST":"large","KDP":"large","STZ":"large",
 "BUD":"large","DEO":"large","TAP":"large","MGM":"large","LVS":"large","WYNN":"large","DKNG":"large",
 "FLUT":"large","GIS":"large","CAG":"large","CPB":"large","MKC":"large","PFE":"large","HIMS":"large",
 "TJX":"large","ROST":"large","BURL":"large","DG":"large","DLTR":"large","WING":"large","CAVA":"large",
 "FCX":"large","SCCO":"large","BHP":"large","RIO":"large","VALE":"large","GLEN":"large","AMT":"large",
 "EQIX":"large","DLR":"large","CCI":"large","IRM":"large","O":"large","HEI":"large","TDG":"large",
 "SAF.PA":"large","RR.L":"large","RHM.DE":"large","BAESY":"large","GLW":"large","WFC":"large",
 "UBS":"large","HSBC":"large","BARC":"large","DB":"large","MUFG":"large","SMFG":"large","TPR":"large",
 "KER":"large","BRBY":"large","MONC":"large","ADM":"large","BG":"large","URI":"large","PCAR":"large",
 "ABB":"large","CMI":"large","EMR":"large","PH":"large","VST":"large","CEG":"large","NEE":"large",
 "BAM":"large","KKR":"large","SCHW":"large","NTRS":"large","AIG":"large","AFL":"large","ELV":"large",
 "CI":"large","CVS":"large","BLDP":"large","PLUG":"large","COIN":"large","HOOD":"large","SOFI":"large",
 "DDOG":"large","QSR":"large","TCOM":"large","SPOT":"large","MBLY":"large","GM":"large","CRWV":"large",
 "ADYEY":"large","DFS":"large","CPRI":"large","CPB":"large","TROW":"large","BEN":"large","RGA":"large",
 "SPR":"large","HII":"large","LDOS":"large","LHX":"large","TXT":"large","OSK":"large","BROS":"large",
 "6501.T":"large","6301.T":"large","FANUY":"large","HMC":"large","6506.T":"large","4063.T":"large",
 # --- mid ($2-10B) ---
 "CHKP":"mid","VRNS":"mid","RBRK":"mid","CRDO":"mid","ALAB":"mid","LITE":"mid","FN":"mid",
 "PSTG":"mid","NTAP":"large","ONTO":"mid","AS":"mid","SHAK":"mid","EAT":"mid","CAKE":"mid",
 "BLMN":"mid","JACK":"mid","PZZA":"mid","WEN":"mid","SG":"mid","BFI":"mid","KRUS":"mid",
 "FWRG":"mid","BROS":"mid","RHP":"mid","HST":"mid","KTOS":"mid","RKLB":"mid","AVAV":"mid",
 "BWXT":"mid","BAH":"mid","SAIC":"mid","MRCY":"mid","AMBA":"mid","SYNA":"mid","MOD":"mid",
 "CRS":"mid","ATI":"mid","RS":"mid","MTRN":"mid","HXL":"mid","AENA.MC":"mid","STNE":"mid",
 "PAGS":"mid","DLO":"mid","VTEX":"mid","BE":"mid","OKLO":"mid","SMR":"mid","NXE":"mid",
 "UEC":"mid","LEU":"mid","ASTS":"mid","IRDM":"mid","GSAT":"mid","LUNR":"mid","CRCL":"mid",
 "CALM":"mid","INGR":"mid","IPI":"large","BRKR":"mid","PLNT":"mid","PTON":"mid","GRMN":"large",
 "UNM":"mid","SJM":"mid","VKTX":"mid","OLLI":"mid","FIVE":"mid","NDLS":"small","LOCO":"mid",
 "CVLT":"mid","BXDC":"mid","SBAC":"large","DKS":"large","JWN":"mid","M":"mid","KSS":"mid",
 "GAP":"mid","URBN":"mid","ANF":"mid","AEO":"mid","LEVI":"mid","VFC":"mid","PVH":"mid",
 "BIRK":"large","WWW":"mid","SKX":"large","PPC":"mid","JBS":"large","HRL":"mid","BYND":"small",
 "CELH":"mid","FIZZ":"mid","SIX":"mid","PENN":"mid","BYD":"mid","CZR":"mid","BALY":"small",
 "ETSY":"mid","MTCH":"mid","BMBL":"small","YELP":"small","ROOT":"small","MGLU3.SA":"mid",
 "PL":"mid","BKSY":"small","IONQ":"mid","RGTI":"mid","QBTS":"mid","LAZR":"small","INVZ":"small",
 "AUR":"mid","LYFT":"large","PONY":"mid","WRD":"small","HSAI":"mid","AB":"mid","STVN":"mid",
 "FLEX":"large","NVTS":"small","ANDE":"mid","AGM":"mid","DAR":"mid","MOG-A":"mid","AMSC":"mid",
 "SAIL":"mid","LSPD":"mid","PAR":"mid","OLO":"small","VYX":"small","BG":"large","CMP":"small",
 "HBM":"mid","IVN":"large","FM":"large","ANTO":"large","TECK":"large","X":"mid","CSTM":"small",
 "ALT":"small","SMMT":"mid","GXI":"small","AENA":"large","DESP":"mid","MMYT":"mid","TRIP":"small",
 "TTD":"large","PINS":"large","ROKU":"mid","APP":"large","OMC":"large","IPG":"mid","TRI":"large",
 "CHGG":"small","TWLO":"mid","FFIV":"mid","DOCU":"mid","ZM":"mid","BOX":"small","DNUT":"small",
 "FOR":"small","MRP":"small","TOL":"large","KBH":"mid","TMHC":"mid","MTH":"mid","PHM":"large",
 "DHI":"large","NWS":"large","NWSA":"large","DJCO":"small","IAC":"mid","TGNA":"small","GCI":"small",
 "LEE":"small","BZFD":"small","SNDK":"large","BERY":"mid","AGM":"mid","CBRL":"small","WH":"mid",
 "CHH":"mid","WU":"mid","GENS.SI":"mid",
}

ROMAN = ["IV","III","II","I"]  # match longest first

def clean(s: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()

def trim(s: str) -> str:
    """Strip leading/trailing structural punctuation left over from prose splits."""
    s = s.strip()
    s = re.sub(r'^[：:（）()＝=、。，,\s]+', '', s)
    s = re.sub(r'[：:、，,\s]+$', '', s)
    # unwrap a single fully-parenthesised clause
    m = re.fullmatch(r'（(.+)）', s)
    if m:
        s = m.group(1)
    return s.strip()

def load_files():
    out = []
    for f in sorted(glob.glob(str(ID_DIR / "ID_*.html"))):
        b = os.path.basename(f)
        if b.endswith("_full.html") or b in EXCLUDE:
            continue
        t = open(f, encoding="utf-8", errors="ignore").read()
        m = ID_META_RE.search(t)
        if not m:
            continue
        try:
            j = json.loads(m.group(2))
        except json.JSONDecodeError:
            continue
        if not str(j.get("skill_version", "")).startswith("v2"):
            continue
        out.append((f, b, t, j))
    return out

# ---- extractors -------------------------------------------------------------
def now_box(t):
    m = re.search(r'dsum-col\s+now.*?<p>(.*?)</p>', t, re.DOTALL)
    return clean(m.group(1)) if m else ""

def first_phase_title(t):
    m = re.search(r'class="timeline".*?phase-title[^>]*>(.*?)</', t, re.DOTALL)
    return clean(m.group(1)) if m else ""

def extract_phase(t):
    pt = first_phase_title(t)
    for src in (pt, t):
        m = re.search(r'Phase\s*(IV|III|II|I)\b', src)
        if m:
            return m.group(1), pt
    return None, pt

def auto_sd(nowb, phase_title):
    """Best-effort keyword classification (authoritative = OVERRIDES)."""
    scope = nowb + " " + phase_title
    seg = re.search(r'(商業.*政府|政府.*商業|民用.*軍|分段|各段|兩段|子段)', scope)
    short = "短缺" in scope
    surp = ("過剩" in scope) or ("寬鬆" in scope) or ("超前" in scope) or ("萎縮" in scope)
    bal = "平衡" in scope
    if seg and short and surp:
        return "split"
    if short and not surp:
        return "shortage"
    if surp and not short:
        return "surplus"
    if bal:
        return "balanced"
    return None

def modal_conviction(t):
    tiers = re.findall(r'conviction[：:]\s*<?[^>]*>?\s*(中高|中低|中|高|低)', t)
    if not tiers:
        return None, []
    from collections import Counter
    c = Counter(tiers)
    return c.most_common(1)[0][0], tiers

def report_conviction(t):
    sm = re.search(r'class="scenario-set"', t)
    CW = r'(中高|中低|中|高|低)'
    if sm:
        pre = t[:sm.start()]
        im = list(re.finditer(r'<p class="chapter-intro">(.*?)</p>', pre, re.DOTALL))
        if im:
            cm = re.search(r'conviction\s*' + CW, clean(im[-1].group(1)))
            if cm:
                return cm.group(1), "scenario-intro"
    cm = re.search(r'(?:評級|thesis)[^。<]{0,24}conviction\s*' + CW, t)
    if cm:
        return cm.group(1), "rating"
    return None, None

CONV_MAP = {"高": "high", "中高": "high", "中": "mid", "中低": "mid", "低": "low"}

WINDOW_RE = re.compile(r'(by\s*20\d\d(?:\s*[HQ]\d)?|20\d\d\s*[HQ]\d|20\d\d-\d\d-\d\d|20\d\d\s*年|每週|每季|連\s*\d+\s*[季月週年])')

def extract_kill(t):
    items = re.findall(r'<div class="monitor-item">(.*?)</div>\s*</div>', t, re.DOTALL)
    out = []
    for it in items:
        bm = re.search(r'monitor-body">(.*)$', it, re.DOTALL)
        raw = bm.group(1) if bm else it
        # operate on the full cleaned body so thresholds/numbers in *any* <strong>
        # or trailing clause are never dropped.
        body = clean(raw)
        wm = WINDOW_RE.search(body)
        window = wm.group(1).strip() if wm else ""
        # split metric (monitored variable) from bear_threshold (the condition)
        metric, bear = "", body
        m2 = re.search(r'(是否|：|:|（)', body)
        if m2:
            sep = m2.group(1)
            idx = m2.start()
            metric = body[:idx]
            bear = body[idx:] if sep == "（" else body[idx + len(sep):]
        else:
            metric = body[:40]
            bear = body
        metric = trim(re.sub(r'是否$', '', metric))
        metric = re.sub(r'（[^）]*）$', '', metric).strip()  # drop trailing (每週) etc from label
        bear = trim(bear)
        if not metric:
            metric = trim(body)[:120]
        if not bear:
            bear = trim(body)[:120]
        # validator requires metric/bear_threshold/window keys on every item
        entry = {"metric": metric[:120], "bear_threshold": bear[:120], "window": window[:60]}
        out.append(entry)
    return out

def extract_kill_inline(t):
    """Fallback: inline '⚠ 證偽：' / '可證偽：' prose markers."""
    out = []
    for m in re.finditer(r'(?:⚠\s*)?(?:可證偽|證偽)[：:]\s*(.*?)(?:</p>|</div>|。)', t, re.DOTALL):
        txt = clean(m.group(1))
        if len(txt) < 8:
            continue
        wm = WINDOW_RE.search(txt)
        entry = {"metric": txt[:120], "bear_threshold": txt[:120],
                 "window": (wm.group(1)[:60] if wm else "")}
        out.append(entry)
    return out

def demand_multiple(j):
    tam = j.get("tam_usd_2030")
    cagr = j.get("cagr_pct_5y")
    try:
        cagr = float(cagr)
        return round((1 + cagr / 100.0) ** 5, 1)
    except (TypeError, ValueError):
        return None

# ---- OVERRIDES (authoritative, built after human review) --------------------
# key = filename. Only fields present here override auto-extraction.
# sd_verdict "balanced" here also encodes "no directional supply/demand tilt"
# for mature K-shape / competitive-share / platform-adoption themes whose §5 is a
# thesis verdict rather than a shortage/surplus call.
_S = "shortage"; _B = "balanced"; _U = "surplus"; _P = "split"
OVERRIDES: dict[str, dict] = {
  # --- auto-classification corrections ---
  "ID_CopperSupercycle_20260428.html": {"sd_verdict": _S},  # supercycle/deficit; "過剩" was in bear monitor only
  "ID_GrainsOilseeds_20260629.html": {"sd_verdict": _P,
    "sd_verdict_detail": "原穀（玉米／小麥）現貨寬鬆偏過剩、農民連年虧損；油籽－壓榨－biofuel 端結構偏緊（豆油 YTD ＋約 50％、盤面壓榨價差擴張），複合體裂解為兩速。",
    "conviction": "mid", "clock_phase": "II"},
  # --- manual sd_verdict (non keyword-classifiable) ---
  "ID_AIAcceleratorDemand_20260419.html": {"sd_verdict": _S},
  "ID_AIAdRetailMedia_20260429.html": {"sd_verdict": _B},
  "ID_AIComputeCapexCycle_20260611.html": {"sd_verdict": _S},
  "ID_AICrossDomainImpact_20260429.html": {"sd_verdict": _B},
  "ID_AICybersecurityDoubleEdge_20260423.html": {"sd_verdict": _S},
  "ID_AIInferenceEconomics_20260430.html": {"sd_verdict": _S},
  "ID_AgenticAIPlatform_20260424.html": {"sd_verdict": _B},
  "ID_AirlineLoyaltyRepricing_20260429.html": {"sd_verdict": _B},
  "ID_ApparelFootwear_20260427.html": {"sd_verdict": _B},
  "ID_AppleIntelligencePlatformThreat_20260429.html": {"sd_verdict": _B},
  "ID_AthleisureNewEntrants_20260427.html": {"sd_verdict": _B},
  "ID_AthleticFootwearSubsegments_20260427.html": {"sd_verdict": _B},
  "ID_BeverageEnergyDrink_20260428.html": {"sd_verdict": _B},
  "ID_BoomerTravelSupercycle_20260429.html": {"sd_verdict": _S},
  "ID_CUDARocmMoat_20260501.html": {"sd_verdict": _B},
  "ID_CardNetworkDuopoly_20260428.html": {"sd_verdict": _B},
  "ID_CasinoGamingIR_20260429.html": {"sd_verdict": _B},
  "ID_CasualDiningTurnaround_20260427.html": {"sd_verdict": _B},
  "ID_ChannelPowerReversion_20260427.html": {"sd_verdict": _B},
  "ID_ChinaSportswearRise_20260427.html": {"sd_verdict": _B},
  "ID_CobrandCardEcosystem_20260429.html": {"sd_verdict": _B, "clock_phase": "III"},
  "ID_CybersecurityPlatformConsolidation_20260423.html": {"sd_verdict": _B},
  "ID_DataSecurityBackupConvergence_20260423.html": {"sd_verdict": _B},
  "ID_DefenseModernization_20260430.html": {"sd_verdict": _S},
  "ID_DiscountRetailKShape_20260430.html": {"sd_verdict": _B},
  "ID_EdgeAI_20260427.html": {"sd_verdict": _B},  # report: "不是過剩也不是短缺"
  "ID_FastCasualBifurcation_20260427.html": {"sd_verdict": _B},
  "ID_FoundryGeography_20260427.html": {"sd_verdict": _S},
  "ID_FusionCommercialization_20260505.html": {"sd_verdict": _B},
  "ID_GLP1Master_20260429.html": {"sd_verdict": _P,
    "sd_verdict_detail": "治療端＝結構短缺（需求 ＞ 供給、LLY／NVO 雙寡占）；受衝擊食品端＝需求結構性萎縮（過剩壓力）；旅遊／健康／保險為早期外溢。"},
  "ID_GLP1RestaurantImpact_20260427.html": {"sd_verdict": _B},
  "ID_GLP1Treatment_20260428.html": {"sd_verdict": _S},
  "ID_GlassSubstrate_20260420.html": {"sd_verdict": _B},  # report: "過渡期"
  "ID_GlobalBankROE_20260428.html": {"sd_verdict": _B},
  "ID_GlobalEcommerce_20260427.html": {"sd_verdict": _B},
  "ID_GlobalLuxury_20260427.html": {"sd_verdict": _B},
  "ID_HeavyMachineryMining_20260427.html": {"sd_verdict": _S},
  "ID_HotelChains_20260429.html": {"sd_verdict": _B},
  "ID_HumanoidIndustrialRobotics_20260427.html": {"sd_verdict": _B},
  "ID_HydrogenFuelCell_20260505.html": {"sd_verdict": _P,
    "sd_verdict_detail": "綠氫／電解槽端＝需求未起、產能過剩（Nel 訂單 －73％、nucera 砍半）；燃料電池端（Bloom 供 AI 資料中心）＝需求拉力真實、營收加速。"},
  "ID_HyperscalerCloudBigThree_20260505.html": {"sd_verdict": _S},
  "ID_IdentityNewPerimeter_20260423.html": {"sd_verdict": _B},
  "ID_IndustrialAutomation_20260427.html": {"sd_verdict": _P,
    "sd_verdict_detail": "資料中心／電網自動化端＝需求強勁（ABB 訂單 ＋24％、Schneider 能源 ＋12.8％）；純廠房自動化端＝溫吞（ROK ARR ＋6％），需求雙速分化。"},
  "ID_LATAMEcommerce_20260427.html": {"sd_verdict": _B},
  "ID_LLMVendorSecurityEconomics_20260423.html": {"sd_verdict": _B},
  "ID_LuxuryTravelCruise_20260427.html": {"sd_verdict": _S},
  "ID_NuclearRenaissance_20260430.html": {"sd_verdict": _S},
  "ID_OTAandAITravel_20260429.html": {"sd_verdict": _B},
  "ID_ProductivityCopilot_20260427.html": {"sd_verdict": _B},
  "ID_PublicBuilderEntryLevel_20260629.html": {"sd_verdict": _P,
    "sd_verdict_detail": "新成屋層近端供給過剩（待售 10.3 個月、SAAR －6.8％ YoY）；3－5 年結構性短缺仍在（累計缺約 4M 戶），需 30Y 破 5.5％＋收入追趕才解鎖。",
    "conviction": "mid", "clock_phase": "III",
    "kill_metrics": [
      {"metric": "30 年房貸利率", "bear_threshold": "升破 7.5％ 連 6 月（現 6.49％）→ bear 路徑成立", "window": "連 6 月"},
      {"metric": "三巨頭加權毛利率", "bear_threshold": "跌破 18％（LEN Q2 已 15.6％）；buydown 永久 reset 至 12－15％", "window": ""},
      {"metric": "新成屋庫存月數", "bear_threshold": "未回落至 ≤7 月（現 10.3 月）", "window": ""},
      {"metric": "Sun Belt 房價", "bear_threshold": "－15～20％（疊加利率升破 7.5％）→ 大廠 GM 12－15％、P／B 近 1.0", "window": ""}]},
  "ID_PublishersStructuralReset_20260430.html": {"sd_verdict": _B},
  "ID_QuantumComputing_20260427.html": {"sd_verdict": _B},  # report: "不是短缺也不是過剩"
  "ID_RestaurantTechSaaS_20260427.html": {"sd_verdict": _B},
  "ID_RobotaxiAutonomous_20260429.html": {"sd_verdict": _B},
  "ID_SpaceEconomy_20260629.html": {"sd_verdict": _P,
    "sd_verdict_detail": "政府端＝需求確定且加速（撥款落地、prime 合約鎖定，結構偏短缺）；商業寬頻端＝多星系稀釋、公開市場利潤池薄（供給過剩壓力）。",
    "conviction": "mid", "clock_phase": "III",
    "kill_metrics": [
      {"metric": "Neutron 首飛", "bear_threshold": "未於目標 2026 Q4 首飛（RKLB 發射軸延後）", "window": "2026 Q4"},
      {"metric": "ASTS 在軌衛星數 ＋ 2026 營收", "bear_threshold": "年底在軌 ＜45 顆或營收未達 $150－200M guide", "window": "2026 年底"},
      {"metric": "Golden Dome SBI 撥款", "bear_threshold": "2026－2027 未由 OTA 研發轉為部署訂單", "window": "2026－2027"},
      {"metric": "RKLB Space Systems 成長（反向證偽）", "bear_threshold": "連兩季 ＞＋40％ 且 satellite-prime margin 拉到 service-level（＞20％）→ 公開市場利潤池改善、本判斷弱化", "window": "連 2 季"}]},
  "ID_StablecoinPayments_20260430.html": {"sd_verdict": _B},
  "ID_TokenEconomics_20260427.html": {"sd_verdict": _S},
  "ID_USRestaurantChains_20260427.html": {"sd_verdict": _B},
  "ID_WealthTransfer25Year_20260429.html": {"sd_verdict": _B},
}

def build_record(f, b, t, j):
    nowb = now_box(t)
    phase, ptitle = extract_phase(t)
    sd = auto_sd(nowb, ptitle)
    rconv, rsrc = report_conviction(t)
    mconv, tiers = modal_conviction(t)
    conv_token = rconv or mconv
    conv = CONV_MAP.get(conv_token) if conv_token else None
    kills = extract_kill(t)
    if len(kills) < 1:
        kills = extract_kill_inline(t)
    dm = demand_multiple(j)
    rec = {
        "file": b,
        "theme": j.get("theme"),
        "mega": j.get("mega"), "sub_group": j.get("sub_group"),
        "auto": {
            "sd_verdict": sd,
            "clock_phase": phase,
            "conviction": conv,
            "conviction_token": conv_token,
            "conviction_src": rsrc or "modal",
            "tier_tokens": tiers,
            "demand_5y_multiple": dm,
            "kill_metrics": kills,
        },
        "evidence": {
            "now_box": nowb[:240],
            "phase_title": ptitle,
        },
    }
    # apply overrides
    ov = OVERRIDES.get(b, {})
    final = {
        "sd_verdict": ov.get("sd_verdict", sd),
        "clock_phase": ov.get("clock_phase", phase),
        "conviction": ov.get("conviction", conv),
        "demand_5y_multiple": ov.get("demand_5y_multiple", dm),
        "kill_metrics": ov.get("kill_metrics", kills),
    }
    if final["sd_verdict"] == "split":
        final["sd_verdict_detail"] = ov.get("sd_verdict_detail", "")
    if "purity_pct" in ov:
        final["purity_pct"] = ov["purity_pct"]
    if "mcap_overrides" in ov:
        final["_mcap_overrides"] = ov["mcap_overrides"]
    rec["final"] = final
    return rec

# ---- id-meta writeback ------------------------------------------------------
# Insert new keys after `related_tickers` (keeps grouping tidy); mcap_bucket goes
# inside each related_tickers entry after "beneficiary".
NEW_ORDER = ["sd_verdict", "sd_verdict_detail", "clock_phase", "conviction",
             "kill_metrics", "demand_5y_multiple", "purity_pct"]

def inject(j: dict, final: dict) -> dict:
    # mcap_bucket into related_tickers
    mov = final.get("_mcap_overrides", {})
    for r in j.get("related_tickers", []):
        if not isinstance(r, dict):
            continue
        tk = r.get("ticker")
        bucket = mov.get(tk) or MCAP.get(tk)
        if bucket and "mcap_bucket" not in r:
            r["mcap_bucket"] = bucket
    # rebuild dict preserving original order, inserting trend keys after related_tickers
    out = {}
    for k, v in j.items():
        out[k] = v
        if k == "related_tickers":
            for nk in NEW_ORDER:
                if nk == "sd_verdict_detail":
                    if final.get("sd_verdict") == "split" and final.get("sd_verdict_detail"):
                        out["sd_verdict_detail"] = final["sd_verdict_detail"]
                    continue
                if nk == "purity_pct":
                    if final.get("purity_pct") is not None:
                        out["purity_pct"] = final["purity_pct"]
                    continue
                val = final.get(nk)
                if val is not None:
                    out[nk] = val
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--file")
    args = ap.parse_args()

    files = load_files()
    if args.file:
        files = [x for x in files if x[1] == os.path.basename(args.file)]

    records = [build_record(*x) for x in files]

    if args.draft or not args.write:
        DRAFT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        # summary
        n = len(records)
        sd = sum(1 for r in records if r["final"]["sd_verdict"])
        ph = sum(1 for r in records if r["final"]["clock_phase"])
        cv = sum(1 for r in records if r["final"]["conviction"])
        km = sum(1 for r in records if r["final"]["kill_metrics"])
        dm = sum(1 for r in records if r["final"]["demand_5y_multiple"] is not None)
        print(f"draft -> {DRAFT}  ({n} files)")
        print(f"  sd_verdict {sd}/{n}  clock_phase {ph}/{n}  conviction {cv}/{n} "
              f" kill_metrics {km}/{n}  demand_5y_multiple {dm}/{n}")
        need = [r["file"] for r in records if not r["final"]["sd_verdict"]]
        if need:
            print("  sd_verdict MISSING:", need)
        return

    if args.write:
        wrote = 0
        for f, b, t, j in files:
            rec = next(r for r in records if r["file"] == b)
            newj = inject(dict(j), rec["final"])
            block = json.dumps(newj, ensure_ascii=False, indent=2)
            m = ID_META_RE.search(t)
            newt = t[:m.start()] + m.group(1) + "\n" + block + "\n" + m.group(3) + t[m.end():]
            Path(f).write_text(newt, encoding="utf-8")
            wrote += 1
        print(f"wrote {wrote} files")

if __name__ == "__main__":
    main()
