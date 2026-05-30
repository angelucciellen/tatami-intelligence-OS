#!/usr/bin/env python3
"""
vX Rhythm Engine — Batch Analyzer
==================================
Usage:
    python analyze.py --csv path/to/events.csv --zip path/to/bundle.zip

Options:
    --csv       Path to the exported events CSV
    --zip       Path to the exported ZIP bundle (contains screenshots)
    --batch     Batch number being analyzed (e.g. 3)
    --prior     Path to prior batch CSV for comparison (optional)
    --no-ai     Skip Claude screenshot analysis (faster, offline)
    --out       Output folder for the HTML report (default: ./reports)

Requirements:
    pip install anthropic pillow pandas numpy

Set your API key:
    export ANTHROPIC_API_KEY=your_key_here
"""

import argparse
import base64
import json
import os
import sys
import zipfile
import tempfile
import shutil
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from PIL import Image
import io

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

# Patterns from Ground Truth v1.10
PATTERNS = {
    "P7":  "Quality-Rail interaction — mid-channel signals underperform rail signals",
    "P8":  "Failed Traversal Quality inversion — high Q on FAILED = suspect",
    "P9":  "Exhaustion failure modes — Type A (low prior Q) / Type B (pullback in trend)",
    "P10": "Expansion timing — score can't distinguish early vs late burst",
    "P11": "Post-move trap — large move already complete to the left",
    "P12": "Zone type diversity — multi-type zones predict reversal quality",
    "P13": "STRONG_SYNC Traversal — consistent visual signature, all LED",
    "P14": "Failed Traversal at HTF structural level — cleanest reversals",
    "P15": "Micro-compression before Exhaustion — 3-5 bars narrowing",
    "P16": "Bar-arrow-conflict — depends on rail position",
    "P17": "Expansion Burst timing anatomy — channel tight vs wide at signal",
    "P18": "Direction Conflict is genuine structural condition",
}

CASCADE_PAIRS = [
    ("FAILED", "EXHAUSTION"),
    ("COMPRESSION", "TRAVERSAL"),
    ("TRAVERSAL", "EXPANSION"),
    ("EXHAUSTION", "TRAVERSAL"),
    ("FAILED", "TRAVERSAL"),
]

FILTER_DEFS = {
    "F1":  ("Rail proximity", lambda df: df),  # visual only
    "F3":  ("Zones ≥ 10", lambda df: df[df["memory"] >= 10]),
    "F3b": ("Zones ≥ 8", lambda df: df[df["memory"] >= 8]),
    "F4":  ("FAILED Q ≤ 50", lambda df: df[(df["ltf_state"]=="FAILED") & (df["quality"]<=50)]),
    "F5":  ("EXHAUST dual-cond", lambda df: df[(df["ltf_state"]=="EXHAUSTION") & (df["exhaust"]>=60)]),
    "F6":  ("NY only", lambda df: df[df["session"]=="NY"]),
    "F7":  ("Excl Dir+TRANS", lambda df: df[~((df["context"].str.contains("Conflict", na=False)) & (df["sync"]=="TRANSITION"))]),
    "F8":  ("Excl Q 61-70 TRAV", lambda df: df[~((df["ltf_state"]=="TRAVERSAL") & (df["quality"]>=61) & (df["quality"]<=70))]),
    "F9":  ("HTF rail (notes)", lambda df: df[df["notes"].str.contains("htf-rail: yes", case=False, na=False)]),
    "F10": ("Zone diversity (notes)", lambda df: df[df["notes"].str.contains("zone-type-diversity: multi", case=False, na=False)]),
    "F11": ("MIXED sync", lambda df: df[df["sync"]=="MIXED"]),
    "F12": ("Excl CONFLICT sync", lambda df: df[df["sync"]!="CONFLICT"]),
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

def load_csv(path):
    df = pd.read_csv(path)
    df["dt"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["hour"] = df["dt"].dt.hour
    df["day_name"] = df["dt"].dt.day_name()
    df["notes"] = df["notes"].fillna("")
    df["context"] = df["context"].fillna("")
    df["sync"] = df["sync"].fillna("")
    return df

def extract_screenshots(zip_path):
    """Extract screenshots to a temp dir. Returns path."""
    tmp = tempfile.mkdtemp(prefix="vx_screens_")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(tmp)
    return tmp

def find_screenshot(base_dir, event_id, kind="signal"):
    """Find signal or outcome screenshot for an event."""
    patterns = [
        f"event_{event_id:03d}_{kind}.jpg",
        f"event_{event_id:03d}_{kind}.png",
        f"E{event_id:03d}_{kind}.jpg",
    ]
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            for p in patterns:
                if f.lower() == p.lower():
                    return os.path.join(root, f)
    return None

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 1 — STATISTICAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def led_rate(df):
    if len(df) == 0:
        return 0, 0, 0.0
    led = len(df[df["tag"] == "LED"])
    return led, len(df), round(led / len(df) * 100, 1)

def analyze_stats(df, prior_df=None):
    results = {}

    # Overall
    l, t, r = led_rate(df)
    results["overall"] = {"led": l, "total": t, "rate": r,
                          "wrong": len(df[df["tag"]=="WRONG"]),
                          "confirmed": len(df[df["tag"]=="CONFIRMED"]),
                          "lagged": len(df[df["tag"]=="LAGGED"])}

    # By state
    results["by_state"] = {}
    for state in df["ltf_state"].unique():
        sub = df[df["ltf_state"]==state]
        l, t, r = led_rate(sub)
        results["by_state"][state] = {"led": l, "total": t, "rate": r}

    # By session
    results["by_session"] = {}
    for sess in ["Tokyo", "London", "NY"]:
        sub = df[df["session"]==sess]
        l, t, r = led_rate(sub)
        results["by_session"][sess] = {"led": l, "total": t, "rate": r}

    # By sync
    results["by_sync"] = {}
    for sync in df["sync"].unique():
        if not sync:
            continue
        sub = df[df["sync"]==sync]
        l, t, r = led_rate(sub)
        results["by_sync"][sync] = {"led": l, "total": t, "rate": r}

    # By context
    results["by_context"] = {}
    for ctx in df["context"].unique():
        if not ctx:
            continue
        sub = df[df["context"]==ctx]
        l, t, r = led_rate(sub)
        results["by_context"][ctx] = {"led": l, "total": t, "rate": r}

    # By day
    results["by_day"] = {}
    for day in ["Monday","Tuesday","Wednesday","Thursday","Friday"]:
        sub = df[df["day_name"]==day]
        if len(sub) == 0:
            continue
        l, t, r = led_rate(sub)
        results["by_day"][day] = {"led": l, "total": t, "rate": r}

    # By hour
    results["by_hour"] = {}
    for h in sorted(df["hour"].dropna().unique()):
        sub = df[df["hour"]==h]
        l, t, r = led_rate(sub)
        results["by_hour"][int(h)] = {"led": l, "total": t, "rate": r}

    # Memory zone
    results["zone_analysis"] = {}
    for label, fn in [("≥10", lambda d: d[d["memory"]>=10]),
                       ("8-9", lambda d: d[(d["memory"]>=8)&(d["memory"]<10)]),
                       ("<8", lambda d: d[d["memory"]<8])]:
        sub = fn(df)
        l, t, r = led_rate(sub)
        results["zone_analysis"][label] = {"led": l, "total": t, "rate": r}

    # Quality bands on Traversal
    trav = df[df["ltf_state"]=="TRAVERSAL"]
    results["quality_bands"] = {}
    for label, fn in [("55-60", lambda d: d[(d["quality"]>=55)&(d["quality"]<=60)]),
                       ("61-70", lambda d: d[(d["quality"]>=61)&(d["quality"]<=70)]),
                       ("71-75", lambda d: d[(d["quality"]>=71)&(d["quality"]<=75)]),
                       ("76+",   lambda d: d[d["quality"]>=76])]:
        sub = fn(trav)
        l, t, r = led_rate(sub)
        results["quality_bands"][label] = {"led": l, "total": t, "rate": r}

    # Filters
    results["filters"] = {}
    base_l, base_t, base_r = led_rate(df)
    for fid, (fname, ffn) in FILTER_DEFS.items():
        try:
            sub = ffn(df[df["tag"].isin(["LED","WRONG","CONFIRMED","LAGGED"])])
            l, t, r = led_rate(sub)
            delta = round(r - base_r, 1)
            results["filters"][fid] = {"name": fname, "led": l, "total": t,
                                        "rate": r, "delta": delta}
        except Exception as e:
            results["filters"][fid] = {"name": fname, "error": str(e)}

    # Cascade detection
    results["cascades"] = detect_cascades(df)

    # Prior batch comparison
    if prior_df is not None:
        results["prior_comparison"] = compare_batches(df, prior_df)

    # Anomalies
    results["anomalies"] = detect_anomalies(df, results)

    # Question tracker
    results["questions"] = check_questions(df, results)

    return results

def detect_cascades(df):
    df_s = df.sort_values("dt").reset_index(drop=True)
    pairs = []
    for i in range(len(df_s)-1):
        e1, e2 = df_s.iloc[i], df_s.iloc[i+1]
        dt1, dt2 = e1["dt"], e2["dt"]
        if pd.isna(dt1) or pd.isna(dt2):
            continue
        diff = (dt2 - dt1).total_seconds() / 60
        if diff > 65:
            continue
        pair = (e1["ltf_state"], e2["ltf_state"])
        if pair in CASCADE_PAIRS:
            pairs.append({
                "e1_id": int(e1["event_id"]),
                "e2_id": int(e2["event_id"]),
                "type": f"{e1['ltf_state']}→{e2['ltf_state']}",
                "e1_tag": e1["tag"], "e2_tag": e2["tag"],
                "both_led": e1["tag"]=="LED" and e2["tag"]=="LED",
                "session": e1["session"],
                "day": e1["day_name"],
                "hour": int(e1["hour"]) if not pd.isna(e1["hour"]) else 0,
                "gap_min": round(diff),
                "e1_q": int(e1["quality"]) if pd.notna(e1["quality"]) else 0,
                "e1_mfe": float(e1["outcome_atr"]) if pd.notna(e1["outcome_atr"]) else 0,
                "e2_mfe": float(e2["outcome_atr"]) if pd.notna(e2["outcome_atr"]) else 0,
                "e1_mem": int(e1["memory"]) if pd.notna(e1["memory"]) else 0,
            })

    both_led = [p for p in pairs if p["both_led"]]
    from collections import Counter
    type_counts = Counter(p["type"] for p in pairs)
    both_by_type = Counter(p["type"] for p in both_led)

    return {
        "pairs": pairs,
        "total": len(pairs),
        "both_led": len(both_led),
        "both_led_rate": round(len(both_led)/len(pairs)*100, 1) if pairs else 0,
        "by_type": {t: {"n": n, "both_led": both_by_type.get(t,0)} for t, n in type_counts.items()},
        "avg_mfe_both_led": round(np.mean([p["e1_mfe"]+p["e2_mfe"] for p in both_led]), 2) if both_led else 0,
    }

def compare_batches(current, prior):
    c_l, c_t, c_r = led_rate(current)
    p_l, p_t, p_r = led_rate(prior)
    drift = round(c_r - p_r, 1)
    anomaly = abs(drift) > 15

    by_state = {}
    for state in set(list(current["ltf_state"].unique()) + list(prior["ltf_state"].unique())):
        cs = current[current["ltf_state"]==state]
        ps = prior[prior["ltf_state"]==state]
        cl, ct, cr = led_rate(cs)
        pl, pt, pr = led_rate(ps)
        by_state[state] = {"current": cr, "prior": pr, "delta": round(cr-pr, 1)}

    return {"current_rate": c_r, "prior_rate": p_r, "drift": drift,
            "anomaly": anomaly, "by_state": by_state}

def detect_anomalies(df, stats):
    anomalies = []
    overall_rate = stats["overall"]["rate"]

    # Batch LED rate divergence
    if overall_rate < 45:
        anomalies.append({"level": "critical", "msg": f"LED rate {overall_rate}% is critically low — below 45%. Review methodology."})
    elif overall_rate < 50:
        anomalies.append({"level": "warning", "msg": f"LED rate {overall_rate}% is low — below 50%. Review batch for systematic issues."})

    # State concentration
    trav_n = stats["by_state"].get("TRAVERSAL", {}).get("total", 0)
    total = stats["overall"]["total"]
    if total > 0 and trav_n/total > 0.65:
        anomalies.append({"level": "warning", "msg": f"Traversal concentration {trav_n/total*100:.0f}% — above 65%. Phase B will be Traversal-dominated."})

    # Exhaustion rate drop
    exhaust = stats["by_state"].get("EXHAUSTION", {})
    if exhaust.get("total", 0) >= 10 and exhaust.get("rate", 100) < 45:
        anomalies.append({"level": "warning", "msg": f"Exhaustion LED rate dropped to {exhaust['rate']}% — investigate cause."})

    # Low n states
    for state, data in stats["by_state"].items():
        if data["total"] < 5:
            anomalies.append({"level": "info", "msg": f"{state} has only {data['total']} events — insufficient for conclusions."})

    # Filter dead zones
    q_dead = stats["quality_bands"].get("61-70", {})
    if q_dead.get("total", 0) >= 15 and q_dead.get("rate", 100) > 55:
        anomalies.append({"level": "info", "msg": f"Quality dead zone (61-70) performing at {q_dead['rate']}% — reconsider Filter 8."})

    return anomalies

def check_questions(df, stats):
    """Check which open questions can be partially answered by current data."""
    updates = []

    # Q-A: Context Macro Aligned vs Direction Conflict
    ctx = stats.get("by_context", {})
    ma = ctx.get("Macro Aligned", {})
    dc = ctx.get("Direction Conflict", {})
    if ma.get("total", 0) >= 15 and dc.get("total", 0) >= 15:
        spread = round(ma.get("rate", 0) - dc.get("rate", 0), 1)
        updates.append({"q": "Q-A", "status": "partial" if abs(spread) < 20 else "answered",
                        "finding": f"Macro Aligned {ma.get('rate')}% vs Direction Conflict {dc.get('rate')}% — spread: {spread}pts"})

    # Q-B: STRONG_SYNC LED rate
    ss = stats.get("by_sync", {}).get("STRONG_SYNC", {})
    if ss.get("total", 0) >= 15:
        updates.append({"q": "Q-B", "status": "partial" if ss.get("total",0) < 30 else "answered",
                        "finding": f"STRONG_SYNC LED rate: {ss.get('rate')}% (n={ss.get('total')})"})

    # Q-D: Zone count inflection point
    z = stats.get("zone_analysis", {})
    dense = z.get("≥10", {})
    sparse = z.get("<8", {})
    if dense.get("total", 0) >= 30 and sparse.get("total", 0) >= 30:
        updates.append({"q": "Q-D", "status": "partial",
                        "finding": f"Dense ≥10: {dense.get('rate')}% vs Sparse <8: {sparse.get('rate')}%"})

    # Q-G: Distortion events
    dist = stats.get("by_state", {}).get("DISTORTION", {})
    if dist.get("total", 0) == 0:
        updates.append({"q": "Q-G", "status": "partial",
                        "finding": "Zero Distortion events — consistent with session-filter suppression hypothesis"})

    # Cascade questions
    casc = stats.get("cascades", {})
    if casc.get("total", 0) >= 15:
        updates.append({"q": "Q-I", "status": "partial",
                        "finding": f"Cascade total: {casc.get('total')} pairs, {casc.get('both_led')} both-LED"})

    return updates

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 2 — CLAUDE AI SCREENSHOT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

SCREENSHOT_PROMPT = """You are analyzing a TradingView Bar Replay screenshot for the vX Rhythm Engine research project.

This is a signal bar screenshot — the bar where a state change was detected.

Analyze the chart and return ONLY a JSON object with these fields:

{
  "rail_zone": "LOWER_RAIL" | "UPPER_RAIL" | "MID_CHANNEL",
  "channel_width": "NARROW" | "EXPANDING" | "WIDE",
  "pre_signal_coil": true | false,
  "coil_bars": 0-5,
  "large_move_left": true | false,
  "zone_density": "LOW" | "MEDIUM" | "HIGH",
  "pattern_matches": ["P7", "P11", "P15"],
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "notes": "brief observation"
}

Definitions:
- rail_zone: Is price within 0.5 ATR of the lower channel rail (LOWER_RAIL), upper rail (UPPER_RAIL), or more than 0.5 ATR from both (MID_CHANNEL)?
- channel_width: Is the channel narrow and parallel (NARROW), actively widening (EXPANDING), or already wide and flaring (WIDE)?
- pre_signal_coil: Are there 2-4 bars of decreasing range immediately before the signal bar?
- coil_bars: How many bars of compression are visible before the signal?
- large_move_left: Is there a large completed move visible to the left of the signal bar (post-move trap indicator)?
- zone_density: How many zone types are overlapping at signal level? LOW=1 type, MEDIUM=2, HIGH=3+
- pattern_matches: Which patterns from P7-P18 are visually evident?
- confidence: Your confidence in this analysis

Return ONLY valid JSON. No preamble, no explanation."""

def analyze_screenshot_with_claude(img_path, event_data):
    """Send screenshot to Claude API for analysis."""
    try:
        import anthropic
        client = anthropic.Anthropic()

        with open(img_path, "rb") as f:
            img_bytes = f.read()

        # Resize if too large
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size
        if w > 800:
            ratio = 800/w
            img = img.resize((800, int(h*ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=70)
            img_bytes = buf.getvalue()

        b64 = base64.b64encode(img_bytes).decode()

        # Add event context to the prompt
        context = f"Event #{event_data.get('event_id')} | State: {event_data.get('ltf_state')} {event_data.get('ltf_dir')} | Q:{event_data.get('quality')} | Sync:{event_data.get('sync')} | Tag:{event_data.get('tag')}"

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                    {"type": "text", "text": f"Context: {context}\n\n{SCREENSHOT_PROMPT}"}
                ]
            }]
        )

        raw = response.content[0].text.strip()
        # Clean JSON if wrapped in backticks
        raw = re.sub(r"```json\s*|\s*```", "", raw).strip()
        return json.loads(raw)

    except Exception as e:
        return {"error": str(e), "confidence": "FAILED"}

def analyze_all_screenshots(df, screens_dir, batch_size=50, no_ai=False):
    """Analyze screenshots for all events. Returns dict keyed by event_id."""
    if no_ai or not screens_dir:
        return {}

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ⚠  ANTHROPIC_API_KEY not set — skipping screenshot analysis")
        print("     Set it with: export ANTHROPIC_API_KEY=your_key")
        return {}

    print(f"\n  Analyzing screenshots with Claude AI...")
    results = {}
    events = df.to_dict("records")
    total = min(len(events), batch_size)

    for i, ev in enumerate(events[:total]):
        eid = int(ev["event_id"])
        img_path = find_screenshot(screens_dir, eid, "signal")

        if not img_path:
            continue

        sys.stdout.write(f"\r  Event {eid} ({i+1}/{total})...")
        sys.stdout.flush()

        analysis = analyze_screenshot_with_claude(img_path, ev)
        analysis["event_id"] = eid
        analysis["tag"] = ev.get("tag", "")
        analysis["ltf_state"] = ev.get("ltf_state", "")
        results[eid] = analysis

    print(f"\r  Screenshot analysis complete. {len(results)} events analyzed.")
    return results

def extract_screenshot_patterns(screenshot_results):
    """Find patterns across screenshot analyses."""
    if not screenshot_results:
        return {}

    analyses = list(screenshot_results.values())

    # Rail zone vs LED
    rail_led = {}
    for zone in ["LOWER_RAIL", "UPPER_RAIL", "MID_CHANNEL"]:
        subset = [a for a in analyses if a.get("rail_zone")==zone]
        led = sum(1 for a in subset if a.get("tag")=="LED")
        rail_led[zone] = {"n": len(subset), "led": led,
                          "rate": round(led/len(subset)*100,1) if subset else 0}

    # Channel width vs LED
    width_led = {}
    for w in ["NARROW", "EXPANDING", "WIDE"]:
        subset = [a for a in analyses if a.get("channel_width")==w]
        led = sum(1 for a in subset if a.get("tag")=="LED")
        width_led[w] = {"n": len(subset), "led": led,
                        "rate": round(led/len(subset)*100,1) if subset else 0}

    # Pre-signal coil vs LED
    coil_yes = [a for a in analyses if a.get("pre_signal_coil")]
    coil_no  = [a for a in analyses if not a.get("pre_signal_coil")]
    coil_led = {
        "coil_yes": {"n": len(coil_yes), "led": sum(1 for a in coil_yes if a.get("tag")=="LED"),
                     "rate": round(sum(1 for a in coil_yes if a.get("tag")=="LED")/len(coil_yes)*100,1) if coil_yes else 0},
        "coil_no":  {"n": len(coil_no), "led": sum(1 for a in coil_no if a.get("tag")=="LED"),
                     "rate": round(sum(1 for a in coil_no if a.get("tag")=="LED")/len(coil_no)*100,1) if coil_no else 0},
    }

    # Post-move trap
    trap_yes = [a for a in analyses if a.get("large_move_left")]
    trap_led = sum(1 for a in trap_yes if a.get("tag")=="LED")
    trap_analysis = {"n": len(trap_yes), "led": trap_led,
                     "rate": round(trap_led/len(trap_yes)*100,1) if trap_yes else 0}

    # Pattern frequency
    from collections import Counter
    all_patterns = []
    for a in analyses:
        all_patterns.extend(a.get("pattern_matches", []))
    pattern_freq = dict(Counter(all_patterns).most_common())

    # New pattern suggestions — combinations not in GT
    suggestions = []
    # Narrow channel + rail = strong LED indicator
    narrow_rail = [a for a in analyses if a.get("channel_width")=="NARROW"
                   and a.get("rail_zone") in ["LOWER_RAIL","UPPER_RAIL"]]
    if narrow_rail:
        r = round(sum(1 for a in narrow_rail if a.get("tag")=="LED")/len(narrow_rail)*100,1)
        if r > 70 and len(narrow_rail) >= 5:
            suggestions.append(f"Narrow channel + Rail position: {r}% LED (n={len(narrow_rail)}) — consider as composite filter")

    # Wide channel + mid = strong WRONG
    wide_mid = [a for a in analyses if a.get("channel_width")=="WIDE"
                and a.get("rail_zone")=="MID_CHANNEL"]
    if wide_mid:
        r = round(sum(1 for a in wide_mid if a.get("tag")=="WRONG")/len(wide_mid)*100,1)
        if r > 65 and len(wide_mid) >= 5:
            suggestions.append(f"Wide channel + Mid-channel: {r}% WRONG (n={len(wide_mid)}) — strong skip signal")

    return {
        "rail_led": rail_led,
        "width_led": width_led,
        "coil_led": coil_led,
        "trap_analysis": trap_analysis,
        "pattern_freq": pattern_freq,
        "suggestions": suggestions,
        "total_analyzed": len(analyses),
    }

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 3 — LONGITUDINAL TRACKING
# ─────────────────────────────────────────────────────────────────────────────

def load_history(history_path="reports/history.json"):
    if os.path.exists(history_path):
        with open(history_path) as f:
            return json.load(f)
    return []

def save_history(history, stats, batch_num, history_path="reports/history.json"):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    entry = {
        "batch": batch_num,
        "date": datetime.now().isoformat(),
        "total_events": stats["overall"]["total"],
        "led_rate": stats["overall"]["rate"],
        "by_state": {k: v["rate"] for k,v in stats["by_state"].items()},
        "by_session": {k: v["rate"] for k,v in stats["by_session"].items()},
        "cascade_total": stats["cascades"]["total"],
        "cascade_both_led": stats["cascades"]["both_led"],
    }
    history.append(entry)
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)
    return history

def detect_longitudinal_patterns(history):
    """Detect trends across batches."""
    if len(history) < 2:
        return []

    insights = []

    # LED rate trend
    rates = [h["led_rate"] for h in history]
    if len(rates) >= 3:
        trend = rates[-1] - rates[0]
        if trend < -10:
            insights.append({"type": "warning", "msg": f"LED rate declining: {rates[0]}% → {rates[-1]}% across {len(rates)} batches"})
        elif trend > 10:
            insights.append({"type": "positive", "msg": f"LED rate improving: {rates[0]}% → {rates[-1]}% across {len(rates)} batches"})

    # Exhaustion tracking
    exhaust_rates = [(h["batch"], h["by_state"].get("EXHAUSTION", 0)) for h in history if "EXHAUSTION" in h["by_state"]]
    if len(exhaust_rates) >= 2:
        drift = exhaust_rates[-1][1] - exhaust_rates[0][1]
        if abs(drift) > 15:
            insights.append({"type": "warning", "msg": f"Exhaustion LED rate shifted {drift:+.1f}pts across batches — review"})

    # Cascade growth
    cascade_totals = [h["cascade_total"] for h in history]
    if len(cascade_totals) >= 2:
        insights.append({"type": "info", "msg": f"Cascade pairs: {cascade_totals[0]} → {cascade_totals[-1]} ({cascade_totals[-1]-cascade_totals[0]:+d} across batches)"})

    return insights

# ─────────────────────────────────────────────────────────────────────────────
# HTML REPORT GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def build_report(stats, screenshot_patterns, history, batch_num, csv_path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    long_insights = detect_longitudinal_patterns(history)
    total = stats["overall"]["total"]
    led_rate_overall = stats["overall"]["rate"]

    # Color helpers
    def rate_color(r):
        if r >= 70: return "#4ADE80"
        if r >= 60: return "#60A5FA"
        if r >= 50: return "#FACC15"
        return "#F87171"

    def bar(rate, color, label="", n=0):
        w = min(rate, 100)
        n_str = f" (n={n})" if n else ""
        return f'<div class="bar-row"><div class="bl">{label}{n_str}</div><div class="bt"><div class="bf" style="width:{w}%;background:{color}"></div></div><div class="bv" style="color:{color}">{rate}%</div></div>'

    # Build state rows
    state_rows = ""
    for state, data in sorted(stats["by_state"].items(), key=lambda x: -x[1]["rate"]):
        color = {"TRAVERSAL":"#60A5FA","EXHAUSTION":"#FB923C","FAILED":"#F87171",
                 "EXPANSION":"#4ADE80","COMPRESSION":"#FACC15"}.get(state,"#6B6B6B")
        delta = ""
        if "prior_comparison" in stats and state in stats["prior_comparison"]["by_state"]:
            d = stats["prior_comparison"]["by_state"][state]["delta"]
            delta = f'<span style="color:{"#4ADE80" if d>=0 else "#F87171"};font-size:10px;margin-left:6px">{d:+.1f}pts</span>'
        state_rows += f'''<tr>
          <td><span style="color:{color};font-weight:500">{state}</span></td>
          <td style="font-family:\'JetBrains Mono\',monospace">{data["led"]}/{data["total"]}</td>
          <td style="color:{rate_color(data["rate"])};font-family:\'JetBrains Mono\',monospace;font-weight:600">{data["rate"]}%{delta}</td>
        </tr>'''

    # Build filter rows
    filter_rows = ""
    base_rate = stats["overall"]["rate"]
    for fid, data in stats["filters"].items():
        if "error" in data:
            continue
        delta = data["delta"]
        dc = "#4ADE80" if delta >= 3 else "#F87171" if delta <= -3 else "#6B6B6B"
        delta_str = f'<span style="color:{dc}">{delta:+.1f}pts</span>'
        filter_rows += f'''<tr>
          <td style="font-family:\'JetBrains Mono\',monospace;color:#6B6B6B">{fid}</td>
          <td>{data["name"]}</td>
          <td style="font-family:\'JetBrains Mono\',monospace">{data["led"]}/{data["total"]}</td>
          <td style="color:{rate_color(data["rate"])};font-family:\'JetBrains Mono\',monospace;font-weight:500">{data["rate"]}%</td>
          <td>{delta_str}</td>
        </tr>'''

    # Anomaly blocks
    anomaly_html = ""
    for a in stats["anomalies"]:
        color = {"critical":"#F87171","warning":"#FACC15","info":"#60A5FA"}.get(a["level"],"#6B6B6B")
        bg = {"critical":"rgba(248,113,113,.06)","warning":"rgba(250,204,21,.06)","info":"rgba(96,165,250,.06)"}.get(a["level"],"")
        anomaly_html += f'<div style="padding:8px 12px;background:{bg};border:1px solid {color}33;border-radius:3px;margin-bottom:5px;font-size:11px"><span style="color:{color};font-weight:500">{a["level"].upper()}</span> — {a["msg"]}</div>'

    # Question updates
    q_html = ""
    if stats["questions"]:
        for q in stats["questions"]:
            color = "#4ADE80" if q["status"]=="answered" else "#FACC15"
            q_html += f'<div style="padding:7px 10px;background:rgba(74,222,128,.04);border:1px solid rgba(74,222,128,.2);border-radius:3px;margin-bottom:4px;font-size:11px"><span style="font-family:\'JetBrains Mono\',monospace;color:{color}">{q["q"]}</span> <span style="color:#9CA3AF;margin:0 6px">—</span> {q["finding"]}</div>'
    else:
        q_html = '<div style="font-size:11px;color:#6B6B6B">No questions answered at current sample size.</div>'

    # Screenshot pattern section
    screen_html = ""
    if screenshot_patterns:
        sp = screenshot_patterns
        screen_html = f'''
        <div class="sec">Screenshot pattern analysis — {sp["total_analyzed"]} events analyzed by Claude AI</div>
        <div class="grid2" style="margin-bottom:12px">
          <div class="card">
            <div style="font-size:11px;font-weight:500;color:#D4A853;margin-bottom:10px">Rail zone vs LED outcome</div>
            {bar(sp["rail_led"].get("LOWER_RAIL",{}).get("rate",0), "#4ADE80", "Lower Rail", sp["rail_led"].get("LOWER_RAIL",{}).get("n",0))}
            {bar(sp["rail_led"].get("UPPER_RAIL",{}).get("rate",0), "#4ADE80", "Upper Rail", sp["rail_led"].get("UPPER_RAIL",{}).get("n",0))}
            {bar(sp["rail_led"].get("MID_CHANNEL",{}).get("rate",0), "#F87171", "Mid Channel", sp["rail_led"].get("MID_CHANNEL",{}).get("n",0))}
          </div>
          <div class="card">
            <div style="font-size:11px;font-weight:500;color:#D4A853;margin-bottom:10px">Channel width vs LED outcome</div>
            {bar(sp["width_led"].get("NARROW",{}).get("rate",0), "#4ADE80", "Narrow", sp["width_led"].get("NARROW",{}).get("n",0))}
            {bar(sp["width_led"].get("EXPANDING",{}).get("rate",0), "#FACC15", "Expanding", sp["width_led"].get("EXPANDING",{}).get("n",0))}
            {bar(sp["width_led"].get("WIDE",{}).get("rate",0), "#F87171", "Wide/Flaring", sp["width_led"].get("WIDE",{}).get("n",0))}
          </div>
        </div>
        <div class="grid2" style="margin-bottom:12px">
          <div class="card">
            <div style="font-size:11px;font-weight:500;color:#D4A853;margin-bottom:10px">Pre-signal coil vs LED</div>
            {bar(sp["coil_led"]["coil_yes"]["rate"], "#4ADE80", "Coil present", sp["coil_led"]["coil_yes"]["n"])}
            {bar(sp["coil_led"]["coil_no"]["rate"], "#F87171", "No coil", sp["coil_led"]["coil_no"]["n"])}
          </div>
          <div class="card">
            <div style="font-size:11px;font-weight:500;color:#D4A853;margin-bottom:10px">Post-move trap detection</div>
            <div style="font-size:11px;color:#9CA3AF">Events with large prior move visible: <span style="color:#F87171;font-family:\'JetBrains Mono\',monospace">{sp["trap_analysis"]["n"]}</span></div>
            <div style="font-size:11px;color:#9CA3AF;margin-top:4px">LED rate in those events: <span style="color:#FACC15;font-family:\'JetBrains Mono\',monospace">{sp["trap_analysis"]["rate"]}%</span></div>
            <div style="font-size:10px;color:#3A3A3A;margin-top:6px">Pattern 11 (post-move trap) — events with large prior move should be skipped</div>
          </div>
        </div>
        {"".join(f'<div style="padding:8px 12px;background:rgba(74,222,128,.05);border:1px solid rgba(74,222,128,.2);border-radius:3px;margin-bottom:5px;font-size:11px"><span style="color:#4ADE80;font-weight:500">★ New pattern suggestion:</span> {s}</div>' for s in sp.get("suggestions",[]))}
        '''

    # Cascade section
    casc = stats["cascades"]
    casc_rows = ""
    for p in [p for p in casc["pairs"] if p["both_led"]][:10]:
        casc_rows += f'''<tr style="background:rgba(74,222,128,.04)">
          <td style="font-family:\'JetBrains Mono\',monospace">E{p["e1_id"]}→E{p["e2_id"]}</td>
          <td>{p["type"]}</td>
          <td>{p["session"]}</td>
          <td>{p["day"]}</td>
          <td>{p["hour"]:02d}:xx</td>
          <td style="color:#4ADE80;font-family:\'JetBrains Mono\',monospace">{p["e1_mfe"]+p["e2_mfe"]:.1f} ATR</td>
        </tr>'''

    # Longitudinal section
    long_html = ""
    if long_insights:
        for ins in long_insights:
            color = {"positive":"#4ADE80","warning":"#FACC15","info":"#60A5FA"}.get(ins["type"],"#6B6B6B")
            long_html += f'<div style="padding:7px 10px;border:1px solid {color}33;border-radius:3px;margin-bottom:4px;font-size:11px;color:#9CA3AF"><span style="color:{color}">▸</span> {ins["msg"]}</div>'
    else:
        long_html = '<div style="font-size:11px;color:#6B6B6B">Need 2+ batches for longitudinal analysis.</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>vX Batch Analysis — Batch {batch_num}</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--black:#000;--surface:#0D0D0D;--surface2:#141414;--border:#1F1F1F;--white:#fff;--muted:#6B6B6B;--dim:#3A3A3A;--gold:#D4A853;--led:#4ADE80;--wrong:#F87171}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000;color:#fff;font-family:Inter,sans-serif;font-size:13px;-webkit-font-smoothing:antialiased}}
.page{{max-width:1100px;margin:0 auto;padding:24px 20px}}
.hdr{{border-bottom:1px solid var(--border);padding-bottom:14px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:flex-end}}
.hdr h1{{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:500}}
.hdr p{{font-size:11px;color:var(--muted);margin-top:3px}}
.sec{{font-size:10px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:18px 0 10px;display:flex;align-items:center;gap:8px}}
.sec::after{{content:'';flex:1;height:1px;background:var(--border)}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:14px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.stat{{background:var(--surface2);border:1px solid var(--border);border-radius:3px;padding:10px 12px}}
.stat .sv{{font-size:24px;font-weight:600;font-family:'JetBrains Mono',monospace;line-height:1}}
.stat .sl{{font-size:10px;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:.06em}}
.bar-row{{display:flex;align-items:center;gap:8px;margin-bottom:5px}}
.bl{{font-size:10px;color:var(--muted);width:110px;flex-shrink:0;text-align:right}}
.bt{{flex:1;background:var(--surface2);border-radius:2px;height:14px;overflow:hidden}}
.bf{{height:100%;border-radius:2px}}
.bv{{font-size:11px;font-family:'JetBrains Mono',monospace;width:44px;flex-shrink:0}}
table{{width:100%;border-collapse:collapse;font-size:11px}}
th{{font-size:9px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:5px 8px;border-bottom:1px solid var(--border);text-align:left}}
td{{padding:6px 8px;border-bottom:1px solid var(--border);color:var(--muted)}}
tr:last-child td{{border-bottom:none}}
</style>
</head>
<body>
<div class="page">

<div class="hdr">
  <div>
    <h1>vX Rhythm Engine™ — Batch {batch_num} Analysis</h1>
    <p>GC 5m · {csv_path} · Generated {now}</p>
  </div>
  <div style="font-size:10px;color:var(--dim);font-family:'JetBrains Mono',monospace;text-align:right">
    {total} events · LED {led_rate_overall}%
  </div>
</div>

<div class="sec">Summary</div>
<div class="grid4" style="margin-bottom:12px">
  <div class="stat"><div class="sv">{total}</div><div class="sl">total events</div></div>
  <div class="stat"><div class="sv" style="color:{rate_color(led_rate_overall)}">{led_rate_overall}%</div><div class="sl">LED rate</div></div>
  <div class="stat"><div class="sv" style="color:#F87171">{stats["overall"]["wrong"]}</div><div class="sl">WRONG</div></div>
  <div class="stat"><div class="sv" style="color:#FACC15">{casc["total"]}</div><div class="sl">cascade pairs</div></div>
</div>

{"<div class='sec'>Anomalies</div>" + anomaly_html if stats["anomalies"] else ""}

<div class="sec">LED by state</div>
<div class="card" style="margin-bottom:12px">
  <table><thead><tr><th>State</th><th>LED/Total</th><th>Rate</th></tr></thead>
  <tbody>{state_rows}</tbody></table>
</div>

<div class="grid2" style="margin-bottom:12px">
  <div>
    <div class="sec">By session</div>
    <div class="card">
      {"".join(bar(v["rate"], rate_color(v["rate"]), f"{k} (n={v['total']})", 0) for k,v in stats["by_session"].items())}
    </div>
  </div>
  <div>
    <div class="sec">By sync state</div>
    <div class="card">
      {"".join(bar(v["rate"], rate_color(v["rate"]), f"{k} (n={v['total']})", 0) for k,v in sorted(stats["by_sync"].items(), key=lambda x: -x[1]["rate"]))}
    </div>
  </div>
</div>

<div class="grid2" style="margin-bottom:12px">
  <div>
    <div class="sec">By context</div>
    <div class="card">
      {"".join(bar(v["rate"], rate_color(v["rate"]), f"{k[:18]} (n={v['total']})", 0) for k,v in sorted(stats["by_context"].items(), key=lambda x: -x[1]["rate"]))}
    </div>
  </div>
  <div>
    <div class="sec">Quality bands (Traversal only)</div>
    <div class="card">
      {"".join(bar(v["rate"], rate_color(v["rate"]), f"Q {k} (n={v['total']})", 0) for k,v in stats["quality_bands"].items())}
    </div>
  </div>
</div>

<div class="sec">Filter preview (vs baseline {base_rate}%)</div>
<div class="card" style="margin-bottom:12px">
  <table><thead><tr><th>Filter</th><th>Name</th><th>LED/Total</th><th>Rate</th><th>vs baseline</th></tr></thead>
  <tbody>{filter_rows}</tbody></table>
</div>

<div class="sec">Cascade analysis</div>
<div class="card" style="margin-bottom:12px">
  <div class="grid4" style="margin-bottom:10px">
    <div class="stat"><div class="sv">{casc["total"]}</div><div class="sl">pairs detected</div></div>
    <div class="stat"><div class="sv" style="color:var(--led)">{casc["both_led"]}</div><div class="sl">both LED</div></div>
    <div class="stat"><div class="sv" style="color:#FACC15">{casc["both_led_rate"]}%</div><div class="sl">both LED rate</div></div>
    <div class="stat"><div class="sv" style="color:var(--gold)">{casc["avg_mfe_both_led"]}</div><div class="sl">avg ATR (both LED)</div></div>
  </div>
  {"<table><thead><tr><th>Pair</th><th>Type</th><th>Session</th><th>Day</th><th>Hour</th><th>Total MFE</th></tr></thead><tbody>" + casc_rows + "</tbody></table>" if casc_rows else "<div style='font-size:11px;color:var(--muted)'>No both-LED cascade pairs in this batch.</div>"}
</div>

{screen_html}

<div class="sec">Open question tracker</div>
<div class="card" style="margin-bottom:12px">
  {q_html}
</div>

<div class="sec">Longitudinal trends</div>
<div class="card" style="margin-bottom:12px">
  {long_html}
</div>

<div style="border-top:1px solid var(--border);margin-top:16px;padding-top:10px;font-size:10px;color:var(--dim);display:flex;justify-content:space-between">
  <span>vX Rhythm Engine™ · Batch Analyzer · Phase C</span>
  <span style="font-family:'JetBrains Mono',monospace">Generated {now}</span>
</div>

</div>
</body>
</html>"""

    return html

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="vX Rhythm Engine — Batch Analyzer")
    parser.add_argument("--csv", required=True, help="Path to events CSV")
    parser.add_argument("--zip", default=None, help="Path to ZIP bundle with screenshots")
    parser.add_argument("--batch", default="?", help="Batch number")
    parser.add_argument("--prior", default=None, help="Prior batch CSV for comparison")
    parser.add_argument("--no-ai", action="store_true", help="Skip Claude screenshot analysis")
    parser.add_argument("--out", default="reports", help="Output folder")
    args = parser.parse_args()

    print(f"\n  vX Batch Analyzer — starting")
    print(f"  CSV: {args.csv}")

    # Load data
    print("  Loading CSV...")
    df = load_csv(args.csv)
    prior_df = load_csv(args.prior) if args.prior else None
    print(f"  {len(df)} events loaded")

    # Extract screenshots
    screens_dir = None
    tmp_dir = None
    if args.zip:
        print("  Extracting screenshots...")
        tmp_dir = extract_screenshots(args.zip)
        screens_dir = tmp_dir
        print(f"  Screenshots extracted")

    # Level 1: Stats
    print("  Running statistical analysis...")
    stats = analyze_stats(df, prior_df)
    print(f"  LED rate: {stats['overall']['rate']}%")

    # Level 2: Screenshots
    screenshot_results = {}
    screenshot_patterns = {}
    if not args.no_ai and screens_dir:
        screenshot_results = analyze_all_screenshots(df, screens_dir)
        if screenshot_results:
            screenshot_patterns = extract_screenshot_patterns(screenshot_results)
            print(f"  Pattern analysis: {len(screenshot_results)} events")

    # Level 3: History
    history_path = os.path.join(args.out, "history.json")
    history = load_history(history_path)
    history = save_history(history, stats, args.batch, history_path)

    # Build report
    print("  Building HTML report...")
    report_html = build_report(stats, screenshot_patterns, history, args.batch, args.csv)

    # Save
    os.makedirs(args.out, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = os.path.join(args.out, f"vX_Batch{args.batch}_Analysis_{timestamp}.html")
    with open(out_path, "w") as f:
        f.write(report_html)

    # Save full stats JSON
    json_path = os.path.join(args.out, f"vX_Batch{args.batch}_stats_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump({"stats": stats, "screenshot_patterns": screenshot_patterns}, f, indent=2, default=str)

    # Cleanup
    if tmp_dir:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n  ✓ Report saved: {out_path}")
    print(f"  ✓ Stats JSON:   {json_path}")
    print(f"\n  Open the HTML report in your browser to view results.\n")

if __name__ == "__main__":
    main()
