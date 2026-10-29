"""Anthropic 上市想法頁（/ideas/anthropic-ipo.html）的圖表資料。

重跑：python3 -I docs/ideas/data/anthropic-ipo/build_data.py
輸出：同目錄 data.json。頁面只讀這份 json 畫圖，前端不計算。
只用標準函式庫。不抓網路，資料全部來自同目錄的八個 CSV 與本檔常數。

單位：data.json 一律是「億美元」（CSV 的 USD_m 除以 100，USD bn 乘以 10），百分比是 %。
每個序列都附 source（出處）與 asof（資料日期）。

CSV（研究過程整理，原檔名照舊）：
- report_a_pl_quarterly.csv：S-1 季度損益（未經查核），圖 1、2、13。
- report_a_pl_annual.csv：S-1 年度損益，只做驗算。
- report_a_balance_cashflow.csv：資產負債、票據公允價值滾動表、承諾，圖 3、4。
- report_b_commitments.csv：逐筆算力承諾，圖 5。
- report_c_arr_timeline.csv：年化營收（run-rate）里程碑，圖 9。
- report_d_backlog_dependency.csv：供應商積壓訂單，圖 10。
- report_d_circular.csv：循環融資，圖 11。
- report_e_valuation_path.csv：估值路徑，圖 12。

本檔常數（CSV 沒有、頁面正文有的數字）：
- 3Q26 營收：S-1 只寫「是 4Q24（1.97 億美元）的 86 倍」，這裡用 86 × 197 百萬美元推算。
- 票據本金逐年餘額：S-1 附註 9（F-40 至 F-42）的發行與轉換紀錄。
- 年消費 10 萬美元以上客戶數、前五大占比、單一客戶占比：S-1 p.135、p.143、F-16。
- 2027–2030 付款階梯：研究報告依 S-1 合約期間平均攤提的推算。
- 積壓訂單裡各模型公司的金額：各供應商 SEC 文件與 S-1；Oracle 的 OpenAI 金額是媒體報導。
- 循環融資：Google 2026 年 Series G-2 的 100 億美元（S-1 附註 4、附註 10），CSV 沒列，這裡補上。
- 圖 14 的 OpenAI 數字：2026 年預估營收 360 億、到 2030 年支出計畫 8,560 億，媒體報導（二手）；平均攤四年是假設。
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data.json"
ASOF_PAGE = "2026-10-29"
S1 = "Anthropic S-1（2026-10-26 申報，SEC）"
S1_URL = "https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm"


def read(name):
    with open(HERE / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(s):
    s = (s or "").strip().replace(",", "")
    return float(s) if s else None


def yi_m(v):
    """百萬美元 → 億美元。"""
    return None if v is None else round(v / 100.0, 2)


def yi_b(v):
    """十億美元 → 億美元。"""
    return None if v is None else round(v * 10.0, 1)


def check(cond, msg):
    if not cond:
        raise SystemExit("驗算失敗：" + msg)


# ---------------------------------------------------------------- 季度損益
def quarterly():
    rows = {r["period"]: r for r in read("report_a_pl_quarterly.csv")}
    qs = ["1Q25", "2Q25", "3Q25", "4Q25", "1Q26", "2Q26"]
    rev = {q: num(rows[q]["revenue"]) for q in qs}
    rev["4Q24"] = num(rows["4Q24"]["revenue"])
    rev_3q26 = 86 * rev["4Q24"]  # S-1：3Q26 營收是 4Q24 的 86 倍（推算）
    labels = qs + ["3Q26"]
    revs = [rev[q] for q in qs] + [rev_3q26]
    prev = [rev["4Q24"]] + revs[:-1]
    qoq = [round((a / b - 1) * 100, 1) for a, b in zip(revs, prev)]
    yoy_3q26 = round(rev_3q26 / rev["3Q25"], 2)

    op, fv, other, inttax, net, compute, adj = [], [], [], [], [], [], []
    for q in qs:
        r = rows[q]
        o, i, f, x, t, n = (num(r[k]) for k in ("operating_income_loss", "interest_income",
                                               "fv_change_notes_derivatives_safes",
                                               "other_income_expense_net", "income_tax", "net_loss"))
        check(abs(o + i + f + x - t - n) < 0.6, q + " 淨損拆解對不上")
        op.append(yi_m(o)); fv.append(yi_m(f)); other.append(yi_m(x))
        inttax.append(yi_m(i - t)); net.append(yi_m(n))
        compute.append(round(num(r["compute_infrastructure"]) / num(r["revenue"]) * 100, 1))
        adj.append(yi_m(num(r["adj_operating_income_loss"])))
    q_src = S1 + " MD&A 季度經營成果（p.158–161，未經查核）"
    return {
        "revenue_q": {
            "source": q_src + "；3Q26 依 S-1「3Q26 營收是 4Q24（1.97 億美元）的 86 倍」推算",
            "asof": "2026-09-30", "unit": "億美元",
            "labels": labels, "revenue": [yi_m(v) for v in revs], "qoq_pct": qoq,
            "estimated": [False] * len(qs) + [True],
            "increment": [yi_m(a - b) for a, b in zip(revs, prev)],
            "yoy_3q26_x": yoy_3q26,
            "note": "1Q25 的季增以 4Q24 的 1.97 億美元計算",
        },
        "netloss_q": {
            "source": q_src, "asof": "2026-06-30", "unit": "億美元", "labels": qs,
            "operating": op, "fair_value": fv, "other": other, "interest_less_tax": inttax, "net": net,
            "note": "四段相加等於淨損；其他收支 2Q26 含票據購買協議資產損失",
        },
        "compute_share_q": {
            "source": q_src + "；占比自算", "asof": "2026-06-30", "unit": "%", "labels": qs,
            "values": compute, "ref_1h26": round(8945 / 16286 * 100, 1), "adj_operating": adj,
        },
        "_rev": {"4Q24": rev["4Q24"], "3Q26": rev_3q26, "q": rev},
    }


# ---------------------------------------------------------------- 票據本金與公允價值
def notes():
    rows = read("report_a_balance_cashflow.csv")
    fv = {r["period"]: num(r["value"]) for r in rows
          if r["category"] == "fair_value_level3" and r["item"] == "convertible_notes"}
    principal_total = [num(r["value"]) for r in rows
                       if r["category"] == "amazon_notes" and r["item"] == "principal_outstanding_total"][0]
    dates = ["2023-12-31", "2024-12-31", "2025-12-31", "2026-06-30"]
    # S-1 附註 9（F-40 至 F-42）：已發行、尚未轉換的本金（百萬美元）
    amazon = {"2023-12-31": 1200, "2024-12-31": 1200 + 3400 + 1300,
              "2025-12-31": 2600 + 4000, "2026-06-30": principal_total}
    google = {"2023-12-31": 500, "2024-12-31": 500 + 750 + 1300,
              "2025-12-31": 750, "2026-06-30": 0}
    shares = [num(r["value"]) for r in rows
              if r["category"] == "amazon_notes" and r["item"] == "shares_issuable_class_N_millions"][0]
    return {
        "source": S1 + " 附註 4 公允價值滾動表（F-33）、附註 9 票據發行與轉換（F-40–F-42）、MD&A p.165",
        "asof": "2026-06-30", "unit": "億美元", "dates": dates,
        "principal_amazon": [yi_m(amazon[d]) for d in dates],
        "principal_google": [yi_m(google[d]) for d in dates],
        "fair_value": [yi_m(fv[d]) for d in dates],
        "shares_issuable_m": shares,
        "note": "公允價值是全部可轉換票據；2025 年底以前含 Google 票據，2026 年起只剩 Amazon",
    }


# ---------------------------------------------------------------- 現金對承諾
def cash_vs_commit():
    rows = read("report_a_balance_cashflow.csv")
    get = lambda cat, item, per: [num(r["value"]) for r in rows
                                  if r["category"] == cat and r["item"] == item and r["period"] == per][0]
    cash = get("balance_sheet", "cash_and_equivalents", "2026-06-30")
    sti = get("balance_sheet", "short_term_investments", "2026-06-30")
    pc = get("commitments", "purchase_commitments_fixed_or_minimum_total", "2026-06-30")
    lease = get("commitments", "leases_not_yet_commenced_undiscounted", "2026-06-30")
    new = get("commitments", "new_agreements_signed_after_2026-06-30_min_payments", "as of 2026-10-26")
    short = 21000  # S-1 附註 17：短期不可取消最低付款約 210 億美元
    total = pc + lease + new + short
    check(abs(total - 853000) < 1, "承諾加總不是 8,530 億")
    check(abs(cash + sti - 131651) < 1, "現金加短投不是 1,316.51 億")
    return {
        "source": S1 + " 附註 7（F-36）、附註 13（F-59）、附註 16、附註 17（F-66）、資產負債表（F-6）；加總為推算，S-1 總額欄空白",
        "asof": "2026-10-26", "unit": "億美元",
        "commit_segments": [
            {"name": "6/30 固定或最低購買承諾", "value": yi_m(pc), "asof": "2026-06-30"},
            {"name": "6/30 尚未開始的租賃", "value": yi_m(lease), "asof": "2026-06-30"},
            {"name": "6/30 後到 10/26 新簽", "value": yi_m(new), "asof": "2026-10-26"},
            {"name": "短期不可取消", "value": yi_m(short), "asof": "2026-10-26"},
        ],
        "commit_total": yi_m(total),
        "tpu_extra": {"name": "TPU 追加採購（2028–2031，條件未定）", "lo": 1250.0, "hi": 1500.0},
        "cash_segments": [
            {"name": "現金及約當現金", "value": yi_m(cash)},
            {"name": "短期投資", "value": yi_m(sti)},
        ],
        "cash_total": yi_m(cash + sti),
        "coverage_pct_0630": round((cash + sti) / (pc + lease) * 100, 1),
        "coverage_pct_total": round((cash + sti) / total * 100, 1),
    }


# ---------------------------------------------------------------- 逐筆承諾
CANCEL = {  # 依 S-1 MD&A p.171–173 的終止條件分類
    "A03": "noncancel", "G02": "noncancel", "M02": "noncancel", "B01": "noncancel",
    "B02": "noncancel", "D01": "noncancel", "N02": "after_initial", "N03": "on_delivery",
    "N04": "on_delivery",
}
NAMES = {"A03": "Amazon（Trainium）", "G02": "Google（TPU）", "M02": "Microsoft（Nvidia GPU）",
         "B01": "Broadcom 2026 年設備租約（TPU）", "B02": "Broadcom 其他設備租約（TPU）",
         "D01": "AMD（MI450，首批預估）", "N02": "SpaceXAI（Nvidia GPU，上限）",
         "N03": "Lambda（Nvidia GPU）", "N04": "Nscale（Nvidia GPU，上限）"}


def contracts():
    rows = [r for r in read("report_b_commitments.csv") if r["counted_in_s1_named_total"] == "Y"]
    items = []
    for r in rows:
        items.append({"id": r["id"], "name": NAMES[r["id"]], "value": yi_b(num(r["amount_usd_bn"])),
                      "period": r["period"], "cancel": CANCEL[r["id"]]})
    items.sort(key=lambda x: -x["value"])
    total = round(sum(x["value"] for x in items), 1)
    check(abs(total - 6570) < 0.5, "九筆點名合約不是 6,570 億")
    return {
        "source": S1 + " MD&A「Infrastructure Service Arrangements」與「Infrastructure Equipment Leases」（p.171–173）；Broadcom 其他租約＝1,612 億減 1,252 億",
        "asof": "2026-10-26", "unit": "億美元", "items": items, "total": total,
        "cancel_labels": {"noncancel": "不可取消", "after_initial": "初始期後可取消",
                          "on_delivery": "交付驗收後才累計"},
    }


# ---------------------------------------------------------------- 付款階梯
def ladder():
    years = [2027, 2028, 2029, 2030]
    base = [623, 828, 828, 828]          # 有最低金額的合約（Microsoft、Google、Amazon、Nscale、Lambda、Broadcom、AMD）
    with_x = [995, 1200, 1258, 828]       # ＋SpaceXAI（初始期後可取消）
    with_tpu_lo = [995, 1513, 1571, 1141]  # ＋TPU 追加（1,250 億平均攤 2028–2031）
    with_tpu_hi = [995, 1575, 1633, 1203]  # ＋TPU 追加（1,500 億）
    share = 0.55
    return {
        "source": "研究推算：S-1 各合約金額依其期間平均攤提（Broadcom 兩筆租約分別 2026 年中與 2027 年中起算五年、Nscale 2027 年底起、Lambda 2027 年初起、AMD 2027 年中起五年、SpaceXAI 滿載每月 31 億自 2026-12 起到上限為止、TPU 追加平均攤 2028–2031）；算力占營收 55% 為 S-1 1H26 實績（89.45 億 ÷ 162.86 億）",
        "asof": "2026-10-26", "unit": "億美元", "years": years,
        "base": base,
        "spacexai": [a - b for a, b in zip(with_x, base)],
        "tpu_lo": [a - b for a, b in zip(with_tpu_lo, with_x)],
        "tpu_range": [a - b for a, b in zip(with_tpu_hi, with_tpu_lo)],
        "need_base": [round(v / share) for v in base],
        "need_all": [round(v / share) for v in with_tpu_hi],
        "compute_share": share,
        "ref_3q26_annualized": None,  # main() 填入
    }


# ---------------------------------------------------------------- 承諾要求的營收對目前年化（圖 14）
OPENAI_REV_2026 = 360    # OpenAI 2026 年全年預估營收，媒體報導（二手）
OPENAI_SPEND = 8560      # OpenAI 到 2030 年的支出計畫，媒體報導（二手）
OPENAI_YEARS = 4         # 平均攤四年（假設）


def required_revenue(lad):
    share = lad["compute_share"]
    now_a = lad["ref_3q26_annualized"]
    need_a_lo = lad["need_base"][lad["years"].index(2028)]
    need_a_hi = lad["need_all"][lad["years"].index(2028)]
    need_o = round(OPENAI_SPEND / OPENAI_YEARS / share)
    check(need_a_lo == 1505 and need_a_hi == 2864, "2028 年需要營收不是 1,505／2,864 億")
    check(need_o == 3891, "OpenAI 每年需要營收不是 3,891 億")
    rows = [
        {"company": "Anthropic", "name": "3Q26 年化", "kind": "now", "value": now_a,
         "tick": ["Anthropic", "3Q26 年化"],
         "how": "3Q26 營收（4Q24 的 86 倍，推算）乘 4"},
        {"company": "Anthropic", "name": "2028 年需要：只算有最低金額的合約", "kind": "need", "value": need_a_lo,
         "tick": ["Anthropic", "2028 需要", "最低金額", "合約"],
         "how": "2028 年付款 828 億 ÷ 55%"},
        {"company": "Anthropic", "name": "2028 年需要：含 SpaceXAI 與 TPU 追加", "kind": "need", "value": need_a_hi,
         "tick": ["Anthropic", "2028 需要", "含 SpaceXAI", "與 TPU 追加"],
         "how": "2028 年付款上端 1,575 億 ÷ 55%"},
        {"company": "OpenAI", "name": "2026 年預估", "kind": "now", "value": OPENAI_REV_2026,
         "tick": ["OpenAI", "2026 預估"],
         "how": "媒體報導（二手）"},
        {"company": "OpenAI", "name": "每年需要：8,560 億攤四年", "kind": "need", "value": need_o,
         "tick": ["OpenAI", "每年需要", "8,560 億", "攤四年"],
         "how": "8,560 億 ÷ 4 年 ÷ 55%"},
    ]
    for r in rows:
        ref = now_a if r["company"] == "Anthropic" else OPENAI_REV_2026
        r["multiple"] = round(r["value"] / ref, 1)
    return {
        "source": "研究推算。Anthropic：3Q26 年化依 S-1 倍數推算，2028 年需要＝付款階梯（圖 11）÷ 算力占營收 55%（S-1 1H26 實績）。"
                  "OpenAI：2026 年預估營收 360 億與到 2030 年的支出計畫 8,560 億為媒體報導（二手），每年需要＝8,560 億平均攤四年 ÷ 55%（借用 Anthropic 的算力占比，假設）",
        "asof": "2026-10-29", "unit": "億美元",
        "rows": rows,
    }


# ---------------------------------------------------------------- 客戶數與集中度
def customers():
    pts = [("2023-12-31", 20, "約"), ("2024-12-31", 200, "約"), ("2025-03-31", 400, "約"),
           ("2025-06-30", 600, "超過"), ("2025-09-30", 950, "超過"), ("2025-12-31", 1500, "約"),
           ("2026-06-30", 6000, "超過"), ("2026-09-30", 11900, "超過")]
    return {
        "source": S1 + " MD&A p.143、業務章節（近 12 個月營收 10 萬美元以上的客戶）",
        "asof": "2026-09-30", "unit": "家",
        "dates": [p[0] for p in pts], "values": [p[1] for p in pts], "qualifier": [p[2] for p in pts],
        "big": {"over_1m": 1900, "over_10m": 250},
    }


def concentration():
    return {
        "source": S1 + " F-16（單一客戶占營收 10% 以上）、MD&A p.143（前五大以外營收占比：1Q26 約 64%、3Q26 約 79%）、風險因素 p.57（前九個月前五大約 25%）；2Q26 為推算",
        "asof": "2026-09-30", "unit": "%",
        "labels": ["2023", "2025", "1Q26", "2Q26", "3Q26"],
        "single": [43, 12, None, None, None],
        "top5": [None, None, 36, 26, 21],
        "estimated": [False, False, False, True, False],
        "notes": {"2023": "客戶 C 43%、客戶 D 11%", "2025": "客戶 A、客戶 B 各 12%",
                  "1H25": "客戶 B 18%", "1H26": "客戶 C 11%",
                  "2Q26": "由前九個月 25%、1Q26 36%、3Q26 21% 反推，誤差約 ±2 個百分點"},
    }


# ---------------------------------------------------------------- 年化營收對 GAAP
DATE_FIX = {"2024-12": "2024-12-31", "2025-03": "2025-03-15", "2025-08": "2025-08-31", "2025-12": "2025-12-31"}


def runrate(revq):
    rows = read("report_c_arr_timeline.csv")
    company, media, seen = [], [], set()
    for r in rows:
        basis, grade, v = r["basis"], r["primary_secondary"], num(r["number"])
        if v is None or "Claude Code" in basis or "預測" in basis or "YipitData" in basis:
            continue
        if r["date"] == "2024-01":  # 單一分析師列出、原始出處未核實，不畫
            continue
        d = DATE_FIX.get(r["date"], r["date"])
        key = (round(v, 1), "p" if grade.startswith("primary") else "s")
        if key in seen:  # 同一數字重述（2026-04-20 重述 300 億）只畫一次
            continue
        seen.add(key)
        pt = {"date": d, "value": yi_b(v), "url": r["source_url"]}
        (company if grade.startswith("primary") else media).append(pt)
    mids = {"4Q24": "2024-11-15", "1Q25": "2025-02-14", "2Q25": "2025-05-16", "3Q25": "2025-08-15",
            "4Q25": "2025-11-15", "1Q26": "2026-02-14", "2Q26": "2026-05-16", "3Q26": "2026-08-15"}
    q = dict(revq["q"]); q["3Q26"] = revq["3Q26"]
    gaap = [{"q": k, "date": mids[k], "value": yi_m(q[k] * 4), "estimated": k == "3Q26"} for k in mids]
    return {
        "source": "年化營收：Anthropic 公告（一手）與 Reuters、Bloomberg、The Information 等媒體（二手），整理自研究時間線；GAAP 季營收：" + S1 + " 季度表，3Q26 為推算",
        "asof": "2026-09-30", "unit": "億美元",
        "company": company, "media": media, "gaap_x4": gaap,
        "note": "不畫 Claude Code 單項、2023 年的預測值、YipitData 估計（795 億）與未核實的 2024-01 數字；GAAP 季營收乘 4 畫在季中",
    }


# ---------------------------------------------------------------- 積壓依賴
SPLIT = {  # 億美元；區間取低端
    "Oracle": {"label": "Oracle", "openai": 3000, "anthropic": 0, "meta": 0, "microsoft": 0},
    "Microsoft": {"label": "Microsoft", "openai": 2180, "anthropic": 449, "meta": 0, "microsoft": 0},
    "Amazon（AWS）": {"label": "AWS", "openai": 1380, "anthropic": 1000, "meta": 0, "microsoft": 0},
    "Alphabet（Google Cloud）": {"label": "Google Cloud", "openai": 0, "anthropic": 1145, "meta": 0, "microsoft": 0},
    "CoreWeave": {"label": "CoreWeave", "openai": 184, "anthropic": 0, "meta": 210, "microsoft": 0},
    "Nscale": {"label": "Nscale", "openai": 0, "anthropic": 446, "meta": 0, "microsoft": 438},
}


def backlog():
    rows = {r["supplier"]: r for r in read("report_d_backlog_dependency.csv")}
    out = []
    for key, s in SPLIT.items():
        r = rows[key]
        total = yi_b(num(r["total_backlog_usd_bn"]))
        named = s["openai"] + s["anthropic"] + s["meta"] + s["microsoft"]
        low = yi_b(num(r["top5_llm_named_low_usd_bn"]))
        check(abs(named - low) < 1, key + " 歸屬金額與 CSV 低端不符")
        out.append({"name": s["label"], "total": total, "asof": r["as_of"], "metric": r["backlog_metric"],
                    "openai": s["openai"], "anthropic": s["anthropic"], "meta": s["meta"],
                    "microsoft": s["microsoft"], "other": round(total - named, 1),
                    "share_low": num(r["top5_llm_share_low_pct"]), "share_high": num(r["top5_llm_share_high_pct"])})
    big5 = [x for x in out if x["name"] != "Nscale"]
    denom = sum(x["total"] for x in big5)
    return {
        "source": "Oracle 10-Q（2026-08-31）、Microsoft 10-Q（2026-09-30）、Amazon 10-Q（2026-06-30）、Alphabet 10-Q（2026-06-30）、CoreWeave 10-Q（2026-06-30）、Nscale S-1（2026-08-31）與 Anthropic S-1；Oracle 的 OpenAI 3,000 億為媒體報導（二手）",
        "asof": "2026-09-30", "unit": "億美元", "suppliers": out,
        "big5_total": round(denom, 1),
        "note": "區間取低端：Microsoft 的 OpenAI 取 2,180 億（上端 2,810 億）、AWS 的 Anthropic 取 AWS 10-Q 的 1,000 億（S-1 為 1,100 億）、CoreWeave 的 Meta 取 210 億（上端 352 億）",
    }


# ---------------------------------------------------------------- 循環融資
CIRC_PICK = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "B5", "C1", "C3", "C4"]


def circular():
    rows = {r["id"]: r for r in read("report_d_circular.csv")}
    flows = []
    for i in CIRC_PICK:
        r = rows[i]
        flows.append({"id": i, "cat": r["category"][0], "from": r["from_party"], "to": r["to_party"],
                      "value": yi_b(num(r["amount_usd_bn"])), "what": r["instrument"]})
    # CSV 的 A3 只算 Google 票據 33 億加 Series H 100 億。S-1 附註 4、附註 10：Google 依 2026 NPA
    # 另以每股 259.1364 美元買了 3,860 萬股 Series G-2（約 100 億美元，2026 年第二季完成），補一列。
    flows.append({"id": "A3b", "cat": "A", "from": "Google", "to": "Anthropic", "value": 100.0,
                  "what": "Series G-2 特別股 3,860 萬股（S-1 附註 4、附註 10）"})
    order = ["Nvidia", "Broadcom", "Amazon", "Google", "Microsoft", "AMD"]
    sup = []
    for name in order:
        fs = [f for f in flows if f["from"] == name]
        sup.append({"name": name,
                    "A": round(sum(f["value"] for f in fs if f["cat"] == "A"), 1),
                    "B": round(sum(f["value"] for f in fs if f["cat"] == "B"), 1),
                    "C": round(sum(f["value"] for f in fs if f["cat"] == "C"), 1),
                    "detail": [f["to"] + "：" + f["what"] + " " + format(f["value"], ",.0f") + " 億" for f in fs]})
    tot = {k: round(sum(s[k] for s in sup), 1) for k in "ABC"}
    return {
        "source": "Amazon、Microsoft、Broadcom、Nvidia 的 10-Q 與 8-K，Anthropic S-1；整理自研究循環融資表，Google Series G-2 依 S-1 補列；只列流向 OpenAI 與 Anthropic（含替兩家租約作保）的金額",
        "asof": "2026-10-27", "unit": "億美元", "suppliers": sup, "totals": tot,
        "labels": {"A": "已出資", "B": "已簽未出資", "C": "擔保與包底上限"},
        "note": "未計入：Nvidia 對 OpenAI 的 300 億股權（二手）、Microsoft 與 Nvidia 對 Anthropic 的投資（S-1 未列金額）、Google 對 Fluidstack 租約的包底（金額未揭露）、對新雲的出資。Broadcom 的包底客戶是推論",
    }


# ---------------------------------------------------------------- 估值路徑
def valuation():
    rows = read("report_e_valuation_path.csv")
    pick = {"Series C-1/C-2": ("2023-06-30", "C 輪"), "Series D-1/D-3": ("2024-05-31", "D 輪"),
            "Series E-1": ("2025-03-31", "E 輪"), "Series F-1": ("2025-09-02", "F 輪"),
            "Series G-1 (+G-2 Q1)": ("2026-02-12", "G 輪"), "Series H-1 / H-2": ("2026-05-28", "H 輪")}
    rounds, marks = [], []
    for r in rows:
        rd = r["round"]
        if rd in pick:
            v = num(r["post_money_usd_b"].replace("~", ""))
            d, lab = pick[rd]
            rounds.append({"date": d, "label": lab, "value": yi_b(v),
                           "basis": "媒體報導" if lab in ("C 輪", "D 輪") else "公司公告"})
    mk = {"Microsoft up to $5B ": ("2025-11-18", "Microsoft、Nvidia 投資（媒體）"),
          "Forge Global implied": ("2026-04-23", "Forge 次級市場"),
          "Caplight / Rainmaker": ("2026-07-09", "Caplight 次級市場")}
    for r in rows:
        for k, (d, lab) in mk.items():
            if r["round"].startswith(k.strip()):
                marks.append({"date": d, "label": lab, "value": yi_b(num(r["post_money_usd_b"].replace("~", "")))})
    check(len(rounds) == 6 and len(marks) == 3, "估值路徑列數不對")
    return {
        "source": "S-1（每股價格與金額，一手）；投後估值：E 到 H 輪為公司公告，C、D 輪與次級市場報價、IPO 估值為媒體報導（二手）",
        "asof": "2026-10-26", "unit": "億美元", "rounds": rounds, "marks": marks,
        "ipo_talk": {"lo": 15000.0, "hi": 20000.0, "from": "2026-10-01", "to": "2026-11-30",
                     "label": "IPO 傳聞 1.5～2 兆（媒體）"},
        "bear": [{"label": "Chamath：1 兆以下", "value": 10000.0}, {"label": "New Constructs：1,500 億", "value": 1500.0}],
    }


def clean(o):
    """頁面會把部分字串放進提示框；全形分號改成逗號，和正文的標點規則一致。"""
    if isinstance(o, str):
        return o.replace("；", "，")
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    return o


def main():
    q = quarterly()
    rev = q.pop("_rev")
    lad = ladder()
    lad["ref_3q26_annualized"] = yi_m(rev["3Q26"] * 4)
    d = {
        "generated": ASOF_PAGE,
        "page": "/ideas/anthropic-ipo.html",
        "s1_url": S1_URL,
        **q,
        "notes": notes(),
        "cash_vs_commit": cash_vs_commit(),
        "contracts": contracts(),
        "ladder": lad,
        "required_revenue": required_revenue(lad),
        "customers": customers(),
        "concentration": concentration(),
        "runrate": runrate(rev),
        "backlog": backlog(),
        "circular": circular(),
        "valuation": valuation(),
    }
    # 年度損益只做驗算：四季加總要等於年度
    ann = {r["period"]: r for r in read("report_a_pl_annual.csv")}
    s25 = sum(rev["q"][k] for k in ("1Q25", "2Q25", "3Q25", "4Q25"))
    check(abs(s25 - num(ann["FY2025"]["revenue"])) < 1, "2025 四季營收加總不等於年度")
    s1h = rev["q"]["1Q26"] + rev["q"]["2Q26"]
    check(abs(s1h - num(ann["1H2026"]["revenue"])) < 1, "1H26 營收加總不等於半年度")
    OUT.write_text(json.dumps(clean(d), ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("wrote", OUT.name, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
