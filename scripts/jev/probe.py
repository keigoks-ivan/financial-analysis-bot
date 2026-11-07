#!/usr/bin/env python3
"""Jev probe for the NVDA claim tree.

Sends one day's evidence pack (news items) plus the claim questions to
TypeSafe's System One endpoint and prints what the program would do with
each answer. Shadow mode only: nothing is written to the stock-dash data.

Usage:
  export TYPESAFE_API_KEY=...          # from https://console.typesafe.ai/keys
  # or save it once:  ~/.config/typesafe/api_key  (chmod 600)
  python3 scripts/jev/probe.py --pack neutral
  python3 scripts/jev/probe.py --pack break
  python3 scripts/jev/probe.py --pack ambiguous
  python3 scripts/jev/probe.py --pack break --dry-run    # print request, no call

Constants (questions, thresholds) live in questions_NVDA.json so they are
reviewed in one place, as TypeSafe's docs recommend.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"          # pinned; move on purpose, not via the alias
LOG = HERE / "probe_log.jsonl"

# Synthetic test packs. English on purpose (Jev's CJK accuracy is lower).
PACKS = {
    "neutral": [
        {"date": "2026-09-22", "source": "Company PR", "headline": "NVIDIA sets GTC 2027 keynote for March 16",
         "summary": "NVIDIA announced the date of its annual developer conference. No product details were given."},
        {"date": "2026-09-22", "source": "Sell-side note", "headline": "Broker raises NVDA price target to $300",
         "summary": "The analyst cites continued data-center demand and reiterates a buy rating."},
        {"date": "2026-09-22", "source": "Wire", "headline": "AMD reports quarterly results, data-center revenue up 50%",
         "summary": "AMD said data-center revenue rose 50% year over year, driven by MI-series GPUs."},
        {"date": "2026-09-22", "source": "Wire", "headline": "Fed holds rates steady",
         "summary": "The Federal Reserve left its policy rate unchanged."},
    ],
    "break": [
        {"date": "2026-09-22", "source": "Company blog", "headline": "OpenAI: our next flagship model was trained primarily on Google TPUs",
         "summary": "OpenAI said in a technical post that the majority of training compute for its next flagship model came from Google TPU v7 clusters, with NVIDIA GPUs used for a minority of runs."},
        {"date": "2026-09-22", "source": "Trade press", "headline": "TSMC to double CoWoS capacity in 2027; Broadcom said to secure 40% of it",
         "summary": "Supply-chain sources say Broadcom has locked in roughly 40% of TSMC's 2027 CoWoS output, similar in size to NVIDIA's allocation."},
        {"date": "2026-09-22", "source": "Wire", "headline": "Microsoft trims 2027 capex plan to $150B from $170B",
         "summary": "Microsoft lowered its fiscal 2027 capital-expenditure outlook, citing slower-than-expected enterprise AI adoption."},
        {"date": "2026-09-22", "source": "Wire", "headline": "Amazon lowers 2027 capital spending guidance",
         "summary": "Amazon cut its 2027 capex guidance by 8%, saying it will pace data-center builds to demand."},
        {"date": "2026-09-22", "source": "Wire", "headline": "DOJ sues to unwind NVIDIA's $20B Groq license, calls it a disguised merger",
         "summary": "The Justice Department filed a complaint seeking to unwind the agreement."},
    ],
    "ambiguous": [
        {"date": "2026-09-22", "source": "Company blog", "headline": "Anthropic expands AMD MI450 deployment to serve Claude; training stays on existing platforms",
         "summary": "Anthropic said the MI450 clusters will serve production traffic. It did not say which chips train its flagship models."},
        {"date": "2026-09-22", "source": "Trade press", "headline": "Report: Meta testing MI450 for training runs of a mid-sized model",
         "summary": "Two people familiar with the matter say Meta is evaluating AMD hardware for training a 70B-parameter model, not its largest models."},
        {"date": "2026-09-22", "source": "Wire", "headline": "China's SAMR says NVIDIA probe continues, no decision yet",
         "summary": "The regulator said its antitrust investigation is ongoing and declined to give a timeline."},
        {"date": "2026-09-22", "source": "Sell-side note", "headline": "Broker estimates NVIDIA holds about 68% of AI accelerator revenue in 2026",
         "summary": "The estimate includes custom ASICs in the denominator."},
    ],
}


def call(state, questions, key):
    body = json.dumps({"state": state, "model": MODEL, "questions": questions}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code in (429, 529) and attempt < 3:
                time.sleep(2 ** attempt); continue
            sys.exit(f"HTTP {e.code}: {msg}")


# Choice options grouped by what they mean for a claim. synthesize.py imports these,
# so there is one list, not two.
NEG_CHOICES = {"broken", "cut", "in_line_or_below", "below_60_percent"}
POS_CHOICES = {"holds", "raised_or_maintained", "above_consensus", "60_to_75_percent", "above_75_percent"}
MID_CHOICES = {"under_investigation"}  # evidence exists, but the claim is neither broken nor confirmed


def route(claim, ans, th):
    """What the program would do. Returns (action, detail)."""
    q = claim["jev"]
    if q["type"] == "noul":
        p = ans["noul"]
        if claim["weight"] == "risk":
            if p >= th["risk_noul_alert"]: return "ALERT human now", f"noul={p:.2f}"
            if p >= th["risk_noul_review"]: return "Opus review", f"noul={p:.2f}"
            return "nothing", f"noul={p:.2f}"
        if p >= th["choice_auto_flip_confidence"]: return "queue human: figure now available", f"noul={p:.2f}"
        return "nothing", f"noul={p:.2f}"
    c, conf = ans["choice"], ans["confidence"]
    neg, pos, mid = NEG_CHOICES, POS_CHOICES, MID_CHOICES
    if c in neg:
        if conf >= th["choice_auto_flip_confidence"]: return "FLIP claim to 否 + notify", f"{c} conf={conf:.2f}"
        if conf >= th["choice_review_confidence"]: return "Opus review", f"{c} conf={conf:.2f}"
        return "human queue", f"{c} conf={conf:.2f}"
    if c in pos:
        return "mark reconfirmed", f"{c} conf={conf:.2f}"
    if c in mid:
        return "mark 不明 (middle state)", f"{c} conf={conf:.2f}"
    return "nothing", f"{c} conf={conf:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", choices=PACKS, default="neutral")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--evidence", help="path to a cleaned evidence pack from clean_evidence.py "
                     "(data/jev/evidence/<TICKER>/<date>.json); overrides --pack")
    ap.add_argument("--top-n", type=int, default=6, help="with --evidence, how many cleaned items "
                     "each claim sees: those tagged as bearing on it, by importance (default 6)")
    a = ap.parse_args()

    spec = json.loads((HERE / "questions_NVDA.json").read_text())
    th = spec["thresholds"]
    jev_claims = [c for c in spec["claims"] if "jev" in c]
    items = PACKS[a.pack]
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        kf = Path.home() / ".config" / "typesafe" / "api_key"
        if kf.exists():
            key = kf.read_text().strip()

    # Step 1: relevance filter, one Noul per item (counting stays in code).
    filt_state = {"items": items}
    filt_q = {f"item_{i}": {**spec["relevance_filter"],
              "instructions": spec["relevance_filter"]["instructions"].replace("`item`", f"`items[{i}]`")}
              for i in range(len(items))}
    # Step 2: claim questions against the kept items.
    claim_q = {c["id"]: c["jev"] for c in jev_claims}

    if a.evidence:
        # Each claim sees only the items tagged as bearing on it (top-N by importance),
        # under its own key in one shared state: `news_A1`, `news_B6`, ...
        # A single global top-N let tie-breaking among equal-importance items decide
        # what every claim saw, so answers changed between identical runs.
        pack = json.loads(Path(a.evidence).read_text())
        ranked = sorted(pack["items"], key=lambda x: (x["importance"], x.get("relevance", 0)), reverse=True)
        per_claim, claim_q = {}, {}
        for c in jev_claims:
            its = [it for it in ranked if c["id"] in it.get("bearing", [])][:a.top_n]
            if not its:
                continue  # no evidence -> no question; synthesize keeps the prior state
            per_claim[c["id"]] = its
            q = json.loads(json.dumps(c["jev"]).replace("`news`", f"`news_{c['id']}`"))
            claim_q[c["id"]] = q
        top = [it for its in per_claim.values() for it in its]
        state = {"ticker": pack.get("ticker", "NVDA"), "as_of": pack.get("date", "")}
        for cid, its in per_claim.items():
            state[f"news_{cid}"] = [{"date": (it.get("published") or "")[:10], "source": it["source"],
                                     "headline": it["headline"], "summary": it.get("text") or it["headline"]}
                                    for it in its]
        if a.dry_run or not key:
            print(json.dumps({"evidence_state": state, "claim_questions": claim_q}, indent=1, ensure_ascii=False)[:6000])
            if not key: print("\n[no TYPESAFE_API_KEY in env; printed the request instead of calling]")
            return
        r2 = call(state, claim_q, key) if claim_q else {"model": MODEL, "answers": {}, "usage": {"input_tokens": 0}}
        print(f"evidence={a.evidence}  items_available={len(pack['items'])}  claims_with_evidence={len(claim_q)}/{len(jev_claims)}  "
              f"tokens={r2['usage']['input_tokens']}")
        print(f"{'id':4} {'pillar':6} {'weight':7} {'action':34} detail")
        for c in jev_claims:
            if c["id"] not in r2["answers"]:
                print(f"{c['id']:4} {c['pillar']:6} {c['weight']:7} {'no evidence today (not asked)':34}    {c['zh']}")
                continue
            act, det = route(c, r2["answers"][c["id"]], th)
            print(f"{c['id']:4} {c['pillar']:6} {c['weight']:7} {act:34} {det}   {c['zh']}  [{len(per_claim[c['id']])} items]")
        ans_path = HERE.parent.parent / "data" / "jev" / "answers" / state["ticker"] / f"{state['as_of']}.json"
        ans_path.parent.mkdir(parents=True, exist_ok=True)
        ans_path.write_text(json.dumps({"ticker": state["ticker"], "date": state["as_of"], "model": r2["model"],
                                        "evidence": a.evidence, "items_per_claim": {k: [it["id"] for it in v] for k, v in per_claim.items()},
                                        "answers": r2["answers"]}, ensure_ascii=False, indent=1))
        print(f"answers saved to {ans_path}")
        with LOG.open("a") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "evidence": a.evidence,
                                "model": r2["model"], "state": state, "answers": r2["answers"]},
                                ensure_ascii=False) + "\n")
        print(f"\nlogged to {LOG}")
        return

    if a.dry_run or not key:
        print(json.dumps({"step1": {"state": filt_state, "model": MODEL, "questions": filt_q},
                          "step2_questions": claim_q}, indent=1, ensure_ascii=False)[:6000])
        if not key: print("\n[no TYPESAFE_API_KEY in env; printed the request instead of calling]")
        return

    r1 = call(filt_state, filt_q, key)
    keep = [it for i, it in enumerate(items) if r1["answers"][f"item_{i}"]["noul"] >= th["relevance_noul_min"]]
    print(f"pack={a.pack}  model={r1['model']}  relevance: kept {len(keep)}/{len(items)}  tokens={r1['usage']['input_tokens']}")
    for i, it in enumerate(items):
        print(f"  {r1['answers'][f'item_{i}']['noul']:.2f}  {it['headline']}")

    state = {"ticker": "NVDA", "as_of": "2026-09-22", "news": keep}
    r2 = call(state, claim_q, key)
    print(f"\nclaims: tokens={r2['usage']['input_tokens']}")
    print(f"{'id':4} {'pillar':6} {'weight':7} {'action':34} detail")
    for c in jev_claims:
        act, det = route(c, r2["answers"][c["id"]], th)
        print(f"{c['id']:4} {c['pillar']:6} {c['weight']:7} {act:34} {det}   {c['zh']}")

    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "pack": a.pack, "model": r2["model"],
                            "state": state, "answers": r2["answers"]}, ensure_ascii=False) + "\n")
    print(f"\nlogged to {LOG}")


if __name__ == "__main__":
    main()
