# vX Rhythm Engine — Ground Truth
**Version:** 1.6 | **Last Updated:** 2026-05-30 | **Rubric:** v2
**System:** vX Rhythm Engine · TradingView Pine Script v5 · Research stage
**Model:** Educator platform — methodology + tagger + Pine code + AI assistant access
**Regulatory note:** NOT a signal service. Educator model deliberately chosen.

> **How to use this file:** This is the authoritative record. Upload to Claude Project after any session where a rule is locked, an edge case is resolved, or stats are updated. When in doubt, this wins over chat memory.

> **Skill creation trigger:** When Batch 3 is locked AND open questions in Section 4 are down to ≤ 3 unresolved items, flag to creator that a custom vX review skill is ready to build.

---

## 1. Status

**Current phase:** C — Validation Dataset (active)

| What | Detail |
|---|---|
| Activity | Manual tagging of 350–400 state-transition events per instrument |
| Instruments | GC 5m (active) · NQ 5m (not yet started) |
| Tagging source | TradingView Bar Replay |
| HTFs | 60m · 240m |
| GC 5m | Batch 1 locked (events 1–50) · Batch 2 locked (events 51–100) · Batch 3 locked (events 101–150) · Batch 4 next |
| NQ 5m | 0 events — starts unfiltered, session-only (no filtered batch by design) |
| Combined main total | 150 locked / 350–400 target per instrument |
| Constraint | NOT trading live during validation. Dataset must stay honest. |

**Timestamp reference:** All event timestamps are recorded in **UTC+9 (Tokyo local time)** regardless of which session the event occurred in. A London open event will show a Tokyo time. This is the reference frame for the entire dataset across all batches and both instruments.

**Session windows (UTC+9):**

| Session | Window UTC+9 | Character | Tag? |
|---|---|---|---|
| Tokyo | 09:00 — 15:00 | Directional or compressive, lower volatility | ✅ |
| Gap | 15:00 — 16:00 | Dead zone between Tokyo close and London open | ❌ Skip |
| London | 16:00 — 22:00 | Primary trend establishment, most reliable Clean Traversal | ✅ |
| NY | 22:00 — 05:00 | Continuation or reversal of London move — character can shift dramatically at open | ✅ |
| Off-session | Before 09:00 · After 05:00 | Pre-market / overnight | ❌ Skip |

**Session-only tagging scope (Batch 3 onward — locked):** Tag all signals inside the windows above. Skip everything outside — before 09:00, the 15:00–16:00 gap, and after 05:00. This is a scope decision, not a quality filter. All signals inside session windows get tagged regardless of quality or visual clarity.

Note: The London-NY overlap (22:00 onward) is treated as the NY session. London establishes direction; NY either continues or reverses it. The 22:00 bar is the highest-consequence transition in the GC trading day.

Note: Batches 1 and 2 included pre-market and off-session signals flagged with `time-filter: pre-session`. Those events remain in the dataset and are valid for comparative analysis in Phase B.

**Sampling methodology (Batch 3 onward):** One week per month, mechanically selected. Do not select weeks by visual inspection of the chart — pick the sampling rule before looking at the data and hold it consistently. Recommended default: second full trading week of each month. If a selected week contains a known scheduled macro event (FOMC, CPI, NFP), note it in the batch log but do not swap it out — event-driven weeks are part of Gold's and NQ's behavioral range and belong in the dataset.

**Batch date log — GC 5m:**

| Batch | Events | Week(s) sampled | Regime notes |
|---|---|---|---|
| Batch 1 | 1–50 | — | Filtered, clear signals only |
| Batch 2 | 51–100 | — | Unfiltered, all state changes |
| Batch 3 | 101–150 | Jan 2026 wk2 | ✅ LOCKED 2026-05-30. 50 events. LED 25/50 = 50.0%. Screenshot review completed. Tag corrections: E145 direction checked. Note corrections: E90, E91, E99. 4 new patterns (P12–P18). Anomaly flag: LED 9pts below combined rate — expected, unfiltered conditions. |
| Batch 4 | 151–200 | Feb 2026 wk2 | — |
| Batch 5 | 201–250 | Mar 2026 wk2 | — |
| Batch 6 | 251–300 | Apr 2026 wk2 | — |
| Batch 7 | 301–350 | May 2026 wk2 | — |
| Batch 8 | 351–400 | TBD | — |

**Batch date log — NQ 5m:**

| Batch | Events | Week(s) sampled | Regime notes |
|---|---|---|---|
| Batch 1 | 1–50 | Jan 2026 wk2 | Unfiltered — session only. No filtered batch by design. Direct comparison baseline to GC Batch 2. |
| Batch 2 | 51–100 | Feb 2026 wk2 | — |
| Batch 3 | 101–150 | Mar 2026 wk2 | — |
| Batch 4 | 151–200 | Apr 2026 wk2 | — |
| Batch 5 | 201–250 | May 2026 wk2 | — |
| Batch 6–8 | 251–400 | TBD | — |

**NQ methodology note:** NQ has no filtered batch. Tagging starts unfiltered and session-only from event 1. GC Batch 1 (filtered) has no NQ equivalent by design — the filtered batch on GC was necessary to build the methodology from scratch. On NQ the methodology is proven. NQ Batch 1 is the direct comparison baseline to GC Batch 2 (unfiltered). Any LED rate difference between GC and NQ reflects instrument behavior, not methodology artifacts.

**What's next:** Complete GC 5m tagging (Batches 3–8, second week per month Jan–present) → start NQ 5m (same methodology, same calendar period) → Phase B strategy harness when both datasets complete.

---

## 2. The Engine

A market regime classifier. It does not predict direction. It classifies behavioral state — trending cleanly, coiling, expanding, reversing, drifting, or breaking down — so the trader can choose the right strategy for the current environment.

### States (7 + Neutral)

| State | Description |
|---|---|
| Clean Traversal | Smooth directional movement between channel rails |
| Compression Coil | Price tightening before expansion; potential energy building |
| Expansion Burst | Volatility expansion, directional surge |
| Exhaustion | Move running out of energy; reversal likely |
| Failed Traversal | Attempted channel traverse that was rejected |
| Equilibrium Drift | Low-energy drift, range-bound behavior |
| Volatility Distortion | Chaotic, unclassifiable, noise-dominant |
| Neutral | No classifiable regime — do NOT tag |

### Scores (4 dimensions, 0–100 each)

| Score | Measures |
|---|---|
| Quality | Signal clarity and regime confidence |
| Compress | Compression intensity |
| Expansion | Expansion force |
| Exhaust | Exhaustion signature strength |

### Architecture layers

Adaptive channels · ATR normalization · Traversal scoring · Momentum cadence · Liquidity memory zones · Exhaustion detector · Fractal sync (5m / 60m / 240m)

---

## 3. Tagging Rules (Locked)

### 3.1 Core Rule

> **Tag at the bar where STATE first changes.**

- Not later bars in the same state
- Not the bar that changes TO Neutral
- Tag EVERY state change regardless of outcome — WRONG events are equally valuable
- Tag every signal even in low-quality time windows (pre-session, dead zones) — use notes to flag them. Filters are validated from data, not assumed.

### 3.2 State Direction Conventions

| State | Arrow shows | Expected outcome direction |
|---|---|---|
| Clean Traversal | Direction of trend | Same as arrow |
| Expansion Burst | Direction of burst | Same as arrow |
| Compression Coil | Bias (if shown) | Same as arrow if shown; else FLAT |
| Exhaustion | Direction of the exhausted move | **OPPOSITE** of arrow |
| Failed Traversal | Direction that failed | **OPPOSITE** of arrow |
| Volatility Distortion | (chaos — no direction) | FLAT — no directional expectation |
| Equilibrium Drift | Drift bias | FLAT — measure as range hold/break |
| Neutral | n/a | Do NOT tag |

**Memory aid for Exhaustion and Failed Traversal:** Arrow = direction of the thing that's over. Outcome = opposite.

**FLAT direction rule (locked):** Never log FLAT for Exhaustion or Failed Traversal. If the engine shows no arrow (—), look at the preceding move on the chart and log the direction of that move — the direction being exhausted, or the direction that attempted and failed. FLAT is only valid for Compression Coil, Equilibrium Drift, and Volatility Distortion.

### 3.3 Tag Rubric

Measure using **Maximum Favorable Excursion (MFE)** within 6 bars from the signal bar, using bar high/low (not closing prices).

| Tag | Condition |
|---|---|
| **LED** | MFE ≥ 1.0 ATR in expected direction |
| **CONFIRMED** | MFE 0.5–1.0 ATR in expected direction |
| **LAGGED** | Engine fired after 80%+ of move was already complete |
| **WRONG** | MFE < 0.5 ATR, OR MAE ≥ 0.5 ATR in opposite direction |

**Honesty check:** If you're between two tags, pick the worse one.

**MFE/MAE notes format:** Track both in notes field for every event.
Example: `"MFE 1.8 ATR up, MAE 1.4 ATR down before bounce"`

Measure in ATR (primary). Points/ticks can be added as supplementary notes.

### 3.4 State-Specific Cautions (Locked)

**Failed Traversal + High Quality:** A Failed Traversal with Quality > 50 is likely a continuation mislabel, not a genuine failure. If the move is clean (high Q), it did not structurally fail — the engine misclassified a strong directional move. Tag honestly by outcome, but flag with `Q-HIGH` and treat the signal with low confidence. Visual confirmation at a structural zone is required to trust a high-Q Failed Traversal.

**Exhaustion + Low Quality:** Exhaustion of a low-quality (messy, grinding) move is unreliable. Exhaust score alone is insufficient. The prior move needs Quality ≥ 45 for the reversal signal to carry weight. Flag low-quality exhaustion signals with `unstable: state flip` if the state environment was also choppy.

**Exhaustion + Pullback in Trend context:** When Context shows "Pullback in Trend" and both HTFs are aligned in the prior direction, Exhaustion is fighting the macro flow. These signals require higher Exhaust threshold (≥ 65) and a clear extreme rail position before trusting the reversal.

**Expansion Burst:** The Expansion score cannot distinguish a burst at its origin from one that is already well extended. Both produce similar X scores. Always visually confirm that the burst is just beginning at the signal bar. If the large move is already visible well to the left of the signal bar, the channel is wide and flaring, and pre-signal bars are small-bodied — skip or downweight.

### 3.5 Special Cases

**Equilibrium Drift:** Exclude from main dataset. Tag separately with note `"drift sub-dataset — range break UP/DOWN"`. Analyse separately when n ≥ 15.

**High-Quality Failed Traversal:** Flag events with Quality > 50 using `"Q-HIGH"` in notes. Analyse separately when n ≥ 10 FAILED events.

**Multi-state cascades:** When a rapid state cascade occurs (e.g., Failed Traversal → Exhaustion → Memory Zone), tag each state change as a separate event. Cross-reference in notes: `"cascade: see event #14"`.

**Exhaustion timing:** Tag at the bar where Exhaustion state FIRST appears, not at the swing high/low.

### 3.6 Special Flags (use in notes field)

| Flag | When to use |
|---|---|
| `time-filter: pre-session` | Signal fired in low-quality time window |
| `time-filter: end-session` | Signal fired at session close |
| `unstable: state flip` | State changed multiple times in quick succession around signal bar |
| `drift sub-dataset — range break UP/DOWN` | Equilibrium Drift event — excluded from main stats |
| `Q-HIGH` | Any state where Quality > 50 and outcome was WRONG or ambiguous |
| `pre-signal coil: yes/no, N bars` | Whether 2–4 bars of ATR contraction preceded signal |
| `memory zones at signal: dense/sparse` | Zone density at signal bar (dense = ≥ 10, sparse = ≤ 8) — updated from ≥ 8 / ≤ 6 based on 145-event CSV analysis |
| `NY-open: first bar` | Signal fires on the first 1–2 bars after 22:00 NY open — highest volatility transition point |
| `bar-arrow-conflict` | Signal bar body direction contradicts state arrow direction |
| `confidence: high/medium/low` | Tagger's confidence in the tag — use when a judgment call was made |
| `macro-event: [type]` | Signal fired during a known macro event week (FOMC, CPI, NFP) |
| `htf-rail: yes/no` | Signal fires at a visible HTF (60m or 240m) structural level — not just the 5m rail. Log from this point forward for all Failed Traversal and Exhaustion events. *(Pattern 14)* |
| `zone-type-diversity: single/multi` | Whether 2+ different zone colours (red, orange, blue) overlap at signal level. Multi-type = higher reversal quality. *(Pattern 12)* |

### 3.7 Skip Window Rule (Locked)

After tagging a signal bar, skip the next 6 bars **unless a structurally significant state change occurs.** If it does, tag it immediately regardless of where you are in the window. This keeps each event's 6-bar MFE measurement window independent and prevents double-counting the same price action.

**Significant — tag immediately regardless of window position:**

| Transition | Reason |
|---|---|
| Traversal → Exhaustion | Regime shift — direction story has reversed |
| Traversal → Failed Traversal | Regime shift — commitment has broken down |
| Compression Coil → Expansion Burst | Regime shift — energy releasing |
| Exhaustion → Expansion | Regime shift — new directional energy |
| Failed → Exhaustion | Cascade — second layer of the same structural event |
| Traversal DOWN → Traversal UP (or reverse) | Same state label, opposite direction — new story |

**Not significant — skip:**

| Transition | Reason |
|---|---|
| Traversal → Traversal (same direction) | Engine re-confirming same regime |
| Any state → Neutral → same state back | Engine flickering, no regime change |
| Same state repeating without intervening change | Continuous state, not a new event |

**Neutral** is never tagged regardless of position in the window.

**Cascade handling:** When a significant transition fires inside the window, tag it and note `cascade: see event #N` on both events. The new event starts its own fresh 6-bar measurement window. If another significant change fires inside that new window, the same rule applies.

**The test:** Ask at each bar — *"Is this a different story, or the same story continuing?"* Different story = tag. Same story = skip.

---

### 3.8 Pre-Batch Checklist (Locked)

Complete before opening TradingView for any new batch. Takes 2 minutes. Prevents errors that only surface 30 events in.

- [ ] Confirm the week selected matches the sampling rule (second full trading week) before looking at the chart
- [ ] Confirm prior batch review is fully closed and locked in the Statistical Running Log
- [ ] Confirm tagger is on correct rubric version (v2)
- [ ] Confirm instrument and timeframe are set correctly (GC or NQ · 5m)
- [ ] Confirm HTFs are set (60m · 240m)
- [ ] Confirm session windows are correctly set in TradingView (UTC+9 reference)
- [ ] Note any known macro events in the selected week in the batch log before starting
- [ ] Confirm Ground Truth version in use matches the current uploaded version

**Do not start tagging until all boxes are checked.**

---

### 3.9 Batch Review Protocol (Locked)

Every completed batch undergoes a formal review before the next batch begins. Review is **mandatory** — not optional — and must complete before the batch is logged as locked in the Statistical Running Log.

**Review has three components:**

**1. Statistical review**
Submit the batch CSV to Claude for sanity-check and LED rate analysis. Flag any anomalies in state distribution, session breakdown, or LED rate divergence from prior batches. Resolve or note all flagged items before locking.

If batch LED rate diverges more than 15 points from the running combined rate — flag as **anomaly batch** in the batch log with a brief note on probable cause. Keep in dataset. Phase B will run sensitivity tests with and without anomaly batches.

**2. Screenshot review**
Review every screenshot in the batch ZIP against its tagged event. Confirm:
- State label matches what is visible on the chart
- Direction is correct
- Signal bar is correctly identified (not a continuation bar)
- Skip window was applied correctly
- Cascade relationships are noted on both events where applicable (`cascade: see event #N`)
- Rail position is noted where relevant (mid-channel vs near-rail)

**3. Notes audit**
Review the notes field on every event. Flag any event where:
- A pattern flag is missing that should be present (`mid-channel`, `sparse zones`, `Q-HIGH`, `bar-arrow-conflict`, `pre-signal coil`, `memory zones at signal`)
- A cascade cross-reference is missing
- A confidence flag is absent on a known judgment-call event
- The notes are ambiguous or incomplete in a way that would affect Phase B filter analysis

Missing notes may be added retroactively and logged as `"notes updated post-review"`.

**Corrections policy:**
- Factual errors (wrong state, wrong direction, wrong bar) — correct and log the correction in the batch notes with event ID and reason
- Missing notes — add retroactively, log as `"notes updated post-review"`
- Judgment calls — do not change. If the tag was defensible at the time, it stays. Retroactive judgment changes contaminate the dataset.

**Review timing:** Complete within one week of finishing the batch. Do not start the next batch until review is closed.

---

### 3.10 Screenshot Naming Convention (Locked)

All screenshots must follow this naming format before export:

> `[INSTRUMENT]_E[EventID]_[YYYYMMDD]_[STATE].png`

Examples:
- `GC_E147_20260514_TRAV.png`
- `GC_E203_20260521_EXHAUST.png`
- `NQ_E012_20260110_COMP.png`

**State abbreviations:**

| State | Abbreviation |
|---|---|
| Clean Traversal | TRAV |
| Compression Coil | COMP |
| Expansion Burst | EXP |
| Exhaustion | EXHAUST |
| Failed Traversal | FAILED |
| Equilibrium Drift | DRIFT |
| Volatility Distortion | DIST |

Consistent naming makes screenshot review at 350+ events feasible. Inconsistent naming makes it very difficult.

---

## 4. Open Questions

- [ ] Quality dead zone (61–70 on Traversal) — why does this band underperform Quality 55–60? Hypothesis: mid-channel signals in this range cross threshold without rail commitment. Test in Phase B with rail proximity filter applied specifically to this Q band.
- [ ] STRONG_SYNC is too rare to confirm at 145 events (n=8, 62.5% LED). Monitor as dataset grows. If STRONG_SYNC events remain sparse at 350 events, this is a significant gap — the engine's highest-confidence state cannot be validated.
- [ ] Direction Conflict + CONFLICT unexpectedly decent (n=10, 70% LED). Counterintuitive — engine documentation flags this as a stand-aside condition. Too small to conclude but worth watching.
- [ ] E63 anomaly — Expansion Burst LED under CONFLICT sync. Engine documentation says CONFLICT = stand aside. Tag is correct by 6-bar MFE rule. Log as Phase A review item: does CONFLICT sync on Expansion mean something structurally different from CONFLICT on Traversal?
- [ ] EXPANSION LED rate is 25% from 4 events (still low n). Watch as more EXPANSION events accumulate. Current hypothesis: timing is the primary variable, not sync state.
- [ ] Session filter hypothesis — Tokyo and London LED rates collapse significantly in unfiltered conditions (35% and 38%). NY holds at 67% unfiltered. Test whether a session filter meaningfully improves combined LED rate in Phase B.
- [ ] Quality-Rail interaction — does requiring price within X% of a channel rail at signal time separate LED from WRONG TRAVERSAL? Confirmed visually; needs quantification in Phase B.
- [ ] Failed Traversal Quality threshold — does Q ≤ 50 filter significantly improve FAILED LED rate? Visual evidence strong; test in Phase B.
- [ ] Exhaustion dual-condition — does requiring Exhaust ≥ 60 AND prior-move Quality ≥ 45 improve EXHAUSTION LED rate? Test in Phase B.
- [ ] Memory zone minimum threshold — dense (≥ 8) zones appear consistently in LED events, sparse (≤ 6) in WRONG. Test minimum zone count as a filter in Phase B.
- [ ] Post-move trap — engine fires on residual drift after a completed move (wide/flaring channel, small-bodied pre-signal bars, big move already visible to the left). No current metric captures this. Candidate for v0.5 channel-width-velocity component.

**Resolved:**
- ~~Back-to-back same-state repeats~~ → **RESOLVED.** Skip window rule (Section 3.7): same state = skip, significant regime shift = tag immediately regardless of window position.
- ~~CONFIRMED rate (2%) and LAGGED rate (2%) very low~~ → **RESOLVED.** CONFIRMED 4%, LAGGED 1% at 100 events. Consistent with honesty-check approach.

---

## 5. Data

### 5.1 Statistical Running Log

| Date | Batch | Instrument | Events (main) | LED | CONFIRMED | LAGGED | WRONG | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-05-24 | Batch 1 | GC 5m | 50 (+2 DRIFT sub) | 38 (76%) | 1 (2%) | 0 | 11 (22%) | Filtered — clear signals only. DRIFT sub: 2 events, both LED range break UP. Event 8 corrected LAGGED→LED post visual review. |
| 2026-05-26 | Batch 2 | GC 5m | 50 | 23 (46%) | 3 (6%) | 1 (2%) | 23 (46%) | Unfiltered — all state changes. Event 56 corrected CONFIRMED→LED post visual review. Filter effect confirmed: 30pt LED rate gap vs Batch 1. |
| 2026-05-30 | Batch 3 | GC 5m | 50 | 25 (50%) | 2 (4%) | 0 | 23 (46%) | ✅ LOCKED. Session-only, unfiltered. Jan 2026 wk2. Anomaly flag: LED 9pts below combined rate — expected unfiltered conditions. Full screenshot review + CSV analysis completed. |

**Combined main total (GC 5m, 150 events — Batches 1+2+3 locked):**

| State | n | LED | CONFIRMED | LAGGED | WRONG | LED % |
|---|---|---|---|---|---|---|
| TRAVERSAL | 88 | 53 | 5 | 2 | 28 | 60.2% |
| EXHAUSTION | 24 | 12 | 2 | 0 | 10 | 50.0% |
| FAILED | 30 | 16 | 2 | 1 | 11 | 53.3% |
| EXPANSION | 4 | 1 | 0 | 0 | 3 | 25.0% |
| COMPRESSION | 2 | 0 | 0 | 0 | 2 | 0% — n too small |
| DRIFT (sub) | 2 | 2 | 0 | 0 | 0 | — sub-dataset |
| **TOTAL** | **150** | **84 (56.0%)** | **9 (6%)** | **3 (2%)** | **54 (36%)** | **56.0%** |

**⚠️ Exhaustion note:** LED rate dropped from 66.7% (100 events) to 50.0% (150 events). Monitor closely in Batch 4. Hypothesis: B1 filtered batch inflated the early rate. Unfiltered B3 Exhaustion was 2/6 = 33.3% — very small n. Not alarming yet but watch.

**Session breakdown (combined 150 locked events):**

| Session | n | LED% |
|---|---|---|
| Tokyo | 52 | 57.7% |
| London | 51 | 47.1% |
| NY | 47 | 63.8% |

**Note:** London weakest at 47.1% — session filter (NY-only or Tokyo+NY) becomes higher priority Phase B test.

**Sync breakdown (combined 150):**

| Sync | n | LED% |
|---|---|---|
| STRONG_SYNC | 8 | 62.5% |
| MIXED | 24 | 70.8% ← strongest |
| CONFLICT | 23 | 56.5% |
| TRANSITION | 94 | 51.1% |
| EQUIL_ALIGN | 1 | 100% — n too small |

**⚠️ MIXED sync note:** 70.8% LED at n=24 — unexpectedly strong, matches zone density filter. Not visible at 100 events. Watch in Batch 4.

**Filter preview (150 events — directional, not locked Phase B findings):**

| Filter | n | LED% | Notes |
|---|---|---|---|
| Zones ≥ 10 | 48 | **70.8%** | Strongest single filter — confirmed |
| MIXED sync | 24 | **70.8%** | New finding at 150 events |
| TRAVERSAL Q≥76 | 4 | **100%** | n too small to conclude |
| NY only | 47 | **63.8%** | Consistent with prior data |
| Dir Conflict + TRANSITION | 50 | 46.0% | Single largest WRONG cluster confirmed |
| TRAVERSAL Q 61–70 | 38 | 47.4% | Dead zone confirmed |
| FAILED Q≤50 | 25 | 56.0% | Modest improvement vs all FAILED (53.3%) |
| EXHAUSTION exhaust≥60 | 24 | 50.0% | No improvement — all EXHAUSTION same threshold |

*These are directional reads, not locked findings. Phase B with full 350–400 event dataset will confirm or revise.*

**Targets:**
- GC 5m total events: 350–400
- NQ 5m total events: 350–400
- Minimum per state: TBD (aim for representational balance)

### 5.2 End of Instrument Review

*To be completed when each instrument's dataset is fully locked and before Phase B handoff.*

**Template (complete for GC when all batches locked, then again for NQ):**

| Field | GC 5m | NQ 5m |
|---|---|---|
| Total events | — | — |
| Final combined LED rate | — | — |
| Best performing state (LED%) | — | — |
| Weakest performing state (LED%) | — | — |
| Best performing session (LED%) | — | — |
| Weakest performing session (LED%) | — | — |
| Patterns confirmed at scale | — | — |
| Patterns that weakened at scale | — | — |
| Threshold observations | — | — |
| Open questions for Phase B | — | — |
| Anomaly batches flagged | — | — |
| Handoff date to Phase B | — | — |

This document becomes the formal handoff from Phase C to Phase B for each instrument.

### 5.3 Visual Pattern Observations — Unconfirmed Hypotheses

*Observed from visual review of all 290 screenshots (145 signal + 145 outcome) across Batches 1, 2, and 3. Not locked rules. To be tested in Phase B.*

*Patterns 1–11 were documented from Batches 1+2. Patterns 12–18 were added from the full 145-event screenshot review completed 2026-05-30.*

**Pattern 1 — Signal location on channel**
LED signals consistently fire at one of three structural locations: price walking a rail (Clean Traversal), price touching an extreme rail (Exhaustion), or price rejecting a rail (Failed Traversal). WRONG events frequently fire mid-channel with no clear rail relationship.

**Pattern 2 — Pre-signal micro-coil**
In most LED events, 2–4 smaller-bodied, lower-range bars immediately precede the signal bar. This micro-compression is visible even when the state classifier does not report COMPRESSION. WRONG events often lack this pre-signal tightening — price is already moving messily when the signal fires.

**Pattern 3 — Memory zone density**
Every LED signal bar sits inside or adjacent to a cluster of overlapping memory zones. WRONG events frequently show sparse zones or no zones. Log `"memory zones at signal: dense/sparse"` in notes. Dense = ≥ 10 active zones; sparse = ≤ 8.

**Threshold update (v1.4):** The original threshold was ≥ 8 (dense) / ≤ 6 (sparse), set visually during Batch 1 review. CSV analysis at 145 events shows the real inflection is at 10, not 8: zones ≥ 10 produce 70.8% LED rate (n=48) vs 53.3% below 8. The ≥ 8 threshold remains as the Phase B filter test baseline for comparison. The recommended Phase B filter test for zone density is ≥ 10, not ≥ 8. Dense and sparse flag definitions updated accordingly.

**Pattern 4 — Channel width predicts regime**
Three visual channel states are readable within 2 seconds: (a) narrow = energy stored, precedes strongest LED moves; (b) expanding = breakout in progress, Expansion Burst fires here, late entry risk; (c) wide flaring = chaotic, Distortion or Exhaustion, fade territory. Channel width transition rate may be more informative than width alone — a v0.5 candidate.

**Pattern 5 — WRONG event visual signature**
WRONG events cluster around: price mid-channel, mixed candles before signal, sparse memory zones, channel in transition. Engine fires because scores crossed thresholds, but price action lacks structural commitment.

**Pattern 6 — Cascade sequences are visually obvious**
Multi-state cascades (e.g., Failed Traversal → Exhaustion → memory zone bounce) produce the cleanest, highest-ATR outcomes in the dataset. A composite high-conviction signal triggering on full cascade confirmation is a Phase A v0.5 target.

**Pattern 7 — Quality-Rail Interaction (TRAVERSAL)**
Quality score alone does not separate LED from WRONG in Clean Traversal. Quality 60–70 mid-channel = WRONG. Quality 60–70 at a channel rail = LED. Rail position is the missing dimension that Quality does not capture. LED Traversal requires BOTH Quality ≥ 55 AND price at or near a rail. Either condition alone is insufficient.

**Pattern 8 — Failed Traversal Quality Inversion**
LED Failed Traversal events consistently show Quality 20–35. WRONG Failed Traversal events consistently show Quality 60–75. The relationship is inverted relative to all other states. A high Quality reading on a Failed Traversal signal indicates the move was actually clean and strong — meaning the engine likely mislabeled a continuation. Quality > 50 on FAILED = treat as suspect.

**Pattern 9 — Exhaustion Failure Modes (two distinct types)**
Type A: Low Quality (≤ 40) + High Exhaust (≥ 60). The prior move was messy. Exhaustion of a low-quality move is unreliable — there is no clean structure to reverse from.
Type B: High Exhaust in "Pullback in Trend" context with both HTFs aligned in the prior direction. The engine correctly identifies local exhaustion but the macro flow overwhelms it. Requires either a higher Exhaust threshold or a context filter.

**Pattern 10 — Expansion Timing Problem**
The Expansion score cannot distinguish a burst at its origin from one that is already well extended. Both produce X ≥ 55. LED Expansion fires at the exact bar where the burst begins — channel tight before, spike just starting. WRONG Expansion fires when the burst is already underway — large move visible to the left, channel already wide. No current dashboard metric captures this distinction. A time-since-expansion-began metric is a v0.5 candidate.

**Pattern 11 — Post-Move Trap**
Distinct from Pattern 5 (mid-channel). After a large impulsive move completes, price consolidates and begins drifting back toward the channel center. The engine detects this residual drift as a new Clean Traversal in the original direction. Visual tells: the large move is already complete and visible well to the left of the signal bar; the channel is wide and flaring; pre-signal bars are small-bodied and directionless. The engine fired correctly by score threshold, but the structural energy is spent. No current metric captures channel-width velocity or post-move decay. v0.5 candidate.

*Confirmed strongly at 145 events. Visible in Batches 1, 2, and 3 without exception. E51, E60, E62, E65, E84, E85, E86, E102, E103, E109, E136, E144 are clear examples.*

**Pattern 12 — Zone type diversity predicts reversal quality**
LED Exhaustion and Failed Traversal events consistently show 2–3 different zone types overlapping at signal level: red, orange, and blue zones present simultaneously. WRONG events at similar locations show only one zone type or zones of the same colour stacked. Zone type diversity is a stronger predictor than zone count alone. The current density filter (≥ 10 zones) should be supplemented by a zone type diversity check. Log `zone-type-diversity: single/multi` on all Exhaustion and Failed Traversal events from this point forward.

*New from 145-event screenshot review. Evidence: E12, E24, E31, E45, E49, E58, E120, E122, E125, E127, E129, E130, E141, E143.*

**Pattern 13 — STRONG_SYNC Traversal has a distinct visual signature**
All STRONG_SYNC Macro Aligned Traversal events share one visual: price walking a rail with consistent small same-coloured candles, channel narrowing or parallel, no opposite wicks breaking the structure. The contrast with TRANSITION Traversal is immediate and consistent across the entire dataset. STRONG_SYNC events are rare (n=8 at 145 events) but visually unmistakable and all LED.

*Confirmed at 145 events. Evidence: E19, E35, E36, E42, E53, E54. All LED. Volume in later batches needed to confirm statistically.*

**Pattern 14 — Failed Traversal at HTF structural level vs 5m rail only**
A consistent subset of LED Failed Traversal events fire at a visually distinct HTF structural level — the 60m or 240m channel boundary visible behind the 5m action — not merely the 5m rail. These produce fast, clean reversals with large MFE. Failed Traversal at a purely 5m structural level without visible HTF confluence has lower LED rate. This HTF confluence is visible in screenshots but not captured in any current data field. Log `htf-rail: yes/no` on all Failed Traversal and Exhaustion events from this point forward.

*New from 145-event screenshot review. Evidence: E11, E21, E22, E39, E43, E58, E75, E83, E89, E118, E120, E122, E124, E125, E130, E143. All LED.*

**Pattern 15 — Micro-compression before Exhaustion predicts LED**
LED Exhaustion events across all three batches show 3–5 bars of narrowing range immediately before the signal bar — even when the engine does not classify COMPRESSION. WRONG Exhaustion events fire into active, volatile price action with no visible pre-signal compression. This is one of the most consistent visual patterns in the dataset across all batches.

*Confirmed strongly at 145 events. Evidence: E24, E25, E30, E31, E34, E45, E48, E49, E52, E56, E61, E72, E79, E115, E127, E129, E141.*

**Pattern 16 — Bar-arrow-conflict refinement**
Bar-arrow-conflict alone does not reliably predict WRONG. It is a compound signal that depends on position: bar-arrow-conflict + rail support = can still LED (engine direction prevailed over the bar body). Bar-arrow-conflict + mid-channel = reliably WRONG (no structural support). The `bar-arrow-conflict` flag should always be noted alongside `rail: yes/no` to be analytically useful.

*New from 145-event screenshot review. Evidence: E117 (bar-arrow-conflict + rail support → LED), E134 (same → LED), E136 (bar-arrow-conflict + mid-channel → WRONG), E144 (same → WRONG).*

**Pattern 17 — Expansion Burst timing anatomy**
LED Expansion events show channel tight and parallel at the signal bar — the burst originates there. WRONG Expansion events show the channel already wide and flaring with the large move visible before the signal. The distinction is visually clear but the Expansion score cannot capture it. Even STRONG_SYNC highest-conviction setups (E37, WRONG) show late-entry anatomy — confirming this is a score architecture limitation, not a filter issue. A channel-width velocity metric is the v0.5 solution.

*New from 145-event screenshot review. Evidence: E37 (WRONG — already extended despite STRONG_SYNC), E63 (LED — channel tight at signal), E81 (LED — channel tight at signal). E63 is a special case: LED under CONFLICT sync, contradicting engine documentation — logged as Phase A anomaly.*

**Pattern 18 — Direction Conflict context is a genuine structural condition**
Events with Direction Conflict context consistently show 60m and 240m HTF arrows pointing in opposite directions in the dashboard. This is structural ambiguity, not noise. The engine's 49% LED rate under Direction Conflict directly reflects a real market condition where no timeframe agrees. Direction Conflict + TRANSITION sync (n=47 at 145 events, 44.7% LED) is the single largest WRONG cluster in the dataset. Filtering out this combination would materially improve the combined LED rate.

*New from 145-event screenshot review. Evidence: systematic across Batch 3. E64, E65, E66, E67, E68, E69, E70, E84, E85, E86 show consecutive sessions of Direction Conflict with consistently mixed outcomes.*

### 5.4 Phase B Test Plan

Ten filter variants to run against unfiltered baseline:

- **Filter 1 — Rail proximity:** Only signals where price is within X% of a channel rail *(Pattern 7)*
- **Filter 2 — Pre-signal compression:** Only signals where 2–4 bars before show ATR contraction *(Pattern 2)*
- **Filter 3 — Memory zone density ≥ 10:** Only signals where memory zone count ≥ 10 *(Pattern 3, updated threshold)*
- **Filter 3b — Memory zone density ≥ 8:** Run as comparison baseline against Filter 3 *(original threshold)*
- **Filter 4 — Failed Traversal Quality threshold:** Only FAILED signals where Quality ≤ 50 *(Pattern 8)*
- **Filter 5 — Exhaustion dual-condition:** Only EXHAUSTION signals where Exhaust ≥ 60 AND prior-move Quality ≥ 45 *(Pattern 9)*
- **Filter 6 — Session filter:** Test NY-only vs all sessions *(session data)*
- **Filter 7 — Context + Sync filter:** Exclude Direction Conflict + TRANSITION combination *(Pattern 18, CSV analysis — 47 events, 44.7% LED at 145 events)*
- **Filter 8 — Quality band filter:** Test excluding Quality 61–70 band on Traversal *(CSV analysis — dead zone, 50% LED at 145 events)*
- **Filter 9 — HTF structural level:** Only Failed Traversal + Exhaustion where htf-rail = yes *(Pattern 14)*
- **Filter 10 — Zone type diversity:** Only Exhaustion + Failed Traversal where zone-type-diversity = multi *(Pattern 12)*
- **Combined:** All applicable filters active simultaneously

Compare LED rates across: unfiltered baseline · each filter alone · all combined · GC vs NQ instrument comparison · anomaly batches included vs excluded.

**Priority filters for Phase B (highest expected impact based on 145-event data):**
1. Filter 7 — Direction Conflict + TRANSITION exclusion (largest single WRONG cluster, n=47)
2. Filter 3 — Zone density ≥ 10 (70.8% LED above threshold vs 53.3% below)
3. Filter 1 — Rail proximity (Pattern 7, visually consistent across all 145 events)
4. Filter 9 — HTF structural level (Pattern 14, cleanest LED reversals in dataset)

**Cannot be tested in Phase B from current data:**
- Pattern 10 (Expansion timing) and Pattern 11 (post-move trap) require channel-width velocity — v0.5 component
- Pattern 17 (Expansion timing anatomy) — same issue, same v0.5 solution
- Pattern 13 (STRONG_SYNC visual signature) — insufficient n (8 events at 145 total), needs more data

**Additional analyses to run at Phase B:**
- LED rate by Context label (Macro Aligned vs Direction Conflict vs Pullback in Trend vs Mixed)
- LED rate by Sync state (STRONG_SYNC vs MIXED vs CONFLICT vs TRANSITION)
- Quality score as continuous variable — does LED rate increase above Q70?
- HTF1 state vs LTF LED rate — does Macro Aligned HTF1 predict LED regardless of LTF state?
- 6-bar window sensitivity test for Exhaustion — re-measure at 10 bars on a subset
- Instrument comparison GC vs NQ for all of the above

---

## 6. Reference

### 6.1 Tagger Tool

| Field | Value |
|---|---|
| File | vx_replay_tagger_v2.html |
| Hosted | https://vxreplaytagger--Kairos-a.replit.app |
| Version | v2 |
| New in v2 | `rubric_version` field added |
| Storage | localStorage (events) · IndexedDB (screenshots) |
| Export | CSV + ZIP bundle with screenshots |

**Session workflow:**
1. Complete pre-batch checklist (Section 3.8) before opening TradingView
2. Tag events in TradingView Replay
3. Export CSV + ZIP bundle from tagger
4. Send batch to Claude for sanity-check and statistical review (Section 3.9)
5. Send chart screenshots for edge cases or pattern analysis
6. Claude reviews, flags anomalies, pushes back — creator makes final decisions
7. Lock batch in Statistical Running Log only after review is fully closed

### 6.2 Toolchain

| Tool | Role |
|---|---|
| TradingView Replay | State-transition tagging source |
| vx_replay_tagger_v2.html | Event capture, CSV + ZIP export |
| Claude Project | Primary AI memory, document storage, batch review |
| This file | Authoritative record of locked rules and decisions |

**Claude's role:** Research partner. Creator makes all decisions. Claude reviews, sanity-checks, and pushes back.

### 6.3 Research Roadmap

| Phase | Status | Description |
|---|---|---|
| C — Validation Dataset | 🔴 Active | Manual tagging, 350–400 events per instrument, GC + NQ 5m |
| B — Strategy Harness | ⬜ Next | Pine strategy() backtest of validated signals — both instruments |
| A — v0.5 Indicator | ⬜ After B | Volume layer, adaptive thresholds, confidence-weighted state, composite signal |
| Software — Standalone Platform | ⬜ Future | Python prototype → engineer hire → production build with order flow integration |

**Strategic direction note (locked 2026-05-29):** The long-term commercial destination is a standalone software product in the class of Bookmap, Sierra Chart, and Quantower — not an educator platform. Pine Script v5 is the validation environment. The engine's classification logic, once validated through Phase C and B, will be ported to Python (prototype) and then to a production software stack with real-time order flow integration. This decision was made after Phase C validated the engine's structural design. The educator platform model remains a secondary possibility but is not the primary build target.

**v0.5 candidates from visual analysis:**
- Channel-width velocity component — rate of change of channel width *(addresses Pattern 10, 11, 17)*
- Rail proximity scoring *(addresses Pattern 7)*
- Cascade detection for composite high-conviction signal *(Pattern 6)*
- Directional bias tagging on memory zones
- Post-move decay metric — time/width since expansion peak *(Pattern 11)*
- Zone type diversity scoring — red/orange/blue zone mix at signal level *(Pattern 12)*
- HTF structural level detection — 60m/240m rail confluence flag *(Pattern 14)*
- Context + Sync composite filter — Direction Conflict + TRANSITION exclusion logic *(Pattern 18)*

### 6.4 Instrument Thresholds (Fixed for Phase C)

Thresholds are fixed per instrument for the entire dataset. Do not adjust mid-instrument — it makes batches incomparable and invalidates running LED rates.

| Instrument | Clean Traversal | Compression Coil | Expansion Burst | Exhaustion | Status |
|---|---|---|---|---|---|
| GC 5m | 55 | 55 | 55 | 60 | 🔴 Active — locked for all GC batches |
| NQ 5m | 55 | 55 | 55 | 60 | ⬜ Not started — thresholds locked |

**GC note:** Exhaustion at 60 vs 55 for other states is intentional — fading a move carries higher consequence and the asymmetry is supported by the 66.7% LED rate on Exhaustion being the best of the three main states.

**NQ note:** Same thresholds as GC by design — keeps datasets directly comparable. If NQ LED rates differ significantly from GC at identical thresholds, the difference reflects instrument behavior, not a threshold artifact. Watch signal frequency in the first 10–15 NQ events — if state changes are firing every 2–3 bars consistently, note it in the batch log but do not adjust thresholds mid-instrument.

### 6.5 Pine Script v5 Constraints

- No repainting · Replay-safe · Low rendering load
- Dark-theme optimized (minimal, institutional, non-cluttered)
- ATR normalization on all threshold values
- Adaptive (not fixed) channel detection

### 6.6 To-Do List

Items identified as gaps or risks not yet addressed in the project. Work through these in order of priority. Check off when complete and log resolution in version history.

---

**🔴 URGENT — Act before next tagging session**

- [ ] **1. Backup protocol** — Export CSV + ZIP bundle from the tagger right now. Store in minimum two locations (local folder + cloud storage e.g. Google Drive or Dropbox). Repeat after every tagging session without exception. A browser data clear, device failure, or accidental "Clear all data" click at event 150+ destroys months of work with no recovery. This is the highest-consequence operational risk in the project.

---

**🟡 HIGH — Address before Phase C completes**

- [ ] **2. Tagger storage ceiling** — The tagger has a 200MB soft ceiling for localStorage + IndexedDB combined. At 400 GC + 400 NQ events with two screenshots each, this ceiling may be approached. Document a plan: at what storage % do you export-and-clear? Do you run GC and NQ in separate tagger instances? Decide and document before NQ tagging begins.

- [ ] **3. Tagging fatigue rule** — No rule currently exists for maximum session length or mandatory break frequency. Fatigue-induced errors are invisible in the data. Add a rule: maximum 25 events per sitting, mandatory break before continuing. Protects data quality in the second half of long sessions.

- [ ] **4. State concentration risk** — Traversal is currently ~58% of all events. If this holds at 350–400 events, Phase B's composite signal will be heavily dependent on one state. Document minimum target event counts per state required for Phase B to be statistically meaningful. If any state falls below minimum at end of Phase C, note it explicitly in the End of Instrument Review.

- [ ] **5. Phase B success threshold** — Phase B currently has no documented go/no-go decision threshold. Before Phase B begins, define explicitly: what filtered LED rate, across which states, across both instruments, constitutes a successful result that justifies proceeding to the Python prototype and software build? Define this threshold before looking at Phase B results — not after.

---

**🟢 STANDARD — Address before external conversations begin**

- [ ] **6. Tagger version control** — If the tagger is updated mid-Phase C (new fields, changed dropdowns, bug fixes), events tagged on different tagger versions may not be directly comparable. Document the current tagger version (v2) as locked for Phase C. Any update requires a version bump, a note in the batch log, and a review of whether prior events need re-checking.

- [ ] **7. Inter-rater reliability** — The entire dataset is tagged by one person. This is a known limitation but is not documented as such. Add an explicit acknowledgment in the dataset notes. Additionally: at end of Phase C, re-tag 10 events from Batch 1 blind (without looking at original tags) and compare results. This basic self-consistency check adds credibility to the dataset when shared with partners or reviewers.

- [ ] **8. Intellectual property documentation** — The methodology, tagging protocol, pattern observations, and composite signal logic are not formally documented as proprietary anywhere. The Ground Truth version history provides timestamped evidence of development. Before any partner conversation, engineer hire, or commercial discussion: confirm the version history is archived with timestamps in a location you control (not just the Claude Project). Consider a simple IP declaration document noting the methodology's development origin and date.

---

*When a to-do item is completed: check the box, add a note with the resolution date, and log the change in Section 6.7 Version History.*

---

### 6.7 Version History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-05-24 | Initial draft from project spec and session context |
| 0.2 | 2026-05-24 | Batch 1 locked (GC 5m, 48 main events). Added FLAT direction rule, DRIFT sub-dataset rule, session filter rule, Q-HIGH flag. Updated stats log. |
| 0.3 | 2026-05-25 | Added visual pattern observations from Batch 1 screenshot review. Added new note flags for Batch 2. Added Phase B test plan. Added v0.5 candidates. |
| 0.4 | 2026-05-26 | Structural pass. Reorganized by reading priority: Status → Engine → Rules → Open Questions → Data → Reference. Edge cases dissolved into rules. Project Identity compressed to header. |
| 0.5 | 2026-05-26 | Batch 2 locked (GC 5m, 50 events, unfiltered). Two tag corrections applied (events 8 and 56). Combined stats updated to 100 events, 61% LED. Added Patterns 7–11 from visual analysis. Added state-specific cautions to rules. Q-HIGH flag broadened. bar-arrow-conflict flag added. Phase B filters expanded to 6. Open questions resolved/updated. Skill creation trigger added. |
| 0.6 | 2026-05-26 | GC 5m state thresholds locked (TRAV/COMP/EXP 55, EXHAUST 60). NQ threshold placeholder added. Section 6.4 added. |
| 0.7 | 2026-05-26 | NQ 5m thresholds locked identical to GC. Rationale: direct comparability across instruments. |
| 0.8 | 2026-05-26 | Sampling methodology added: one week per month, mechanical selection, second full trading week default. Batch date log table added. Macro event rule documented. |
| 0.9 | 2026-05-29 | Timestamp reference locked: all events in UTC+9 (Tokyo local time) across all batches. Session windows defined in UTC+9. Session-only tagging scope locked for Batch 3+. |
| 1.0 | 2026-05-29 | Session windows finalized: Tokyo 09:00–15:00, gap 15:00–16:00 (skip), London 16:00–22:00, NY 22:00–05:00. Three-session structure locked. NY-open first-bar flag added. |
| 1.1 | 2026-05-29 | Skip window rule locked (Section 3.7): 6-bar skip after signal unless significant regime shift occurs. Significant transitions defined. Cascade handling documented. Direction reversal within window = significant. Back-to-back same-state open question resolved. |
| 1.6 | 2026-05-30 | Batch 3 locked (E101–150, 50 events, 50.0% LED). Combined stats updated to 150 events (56.0% LED). Full state/session/sync/filter breakdown added to Section 5.1. Anomaly flag noted: Exhaustion dropped from 66.7% to 50.0% — monitor in Batch 4. New finding: MIXED sync 70.8% LED at n=24. Status section updated: Batch 3 locked, Batch 4 next. File renamed v1.6. |
| 1.5 | 2026-05-30 | Section 7 added: Roadmap & Strategic Context. Includes plain-English executive summary, v0.5 layer-by-layer breakdown with implementation risks, structural ceiling documentation, build path (Python prototype → engineer → UI), competitive landscape table (Bookmap, Sierra Chart, Quantower), probability estimates table, and what 700–800 events does to the validation. Sourced from vX_ENGINE_Status_In_progress_2.pdf. |
| 1.4 | 2026-05-30 | Full 145-event screenshot review completed. 4 new patterns added (P12–P18, excluding P16 which refines P bar-arrow-conflict). Tag corrections: E145 direction checked and corrected. Note corrections: E90 (E-HIGH label error), E91 (state label error), E99 (state label error). Mid-run CSV analysis added to Section 5.1 (145-event directional reads). Memory zone threshold updated from ≥8 to ≥10 in Pattern 3 and flags table based on data. Two new flags added: htf-rail and zone-type-diversity. Phase B test plan expanded from 6 to 10 filters plus additional analyses. v0.5 candidates expanded with Pattern 12, 14, 18 components. Open questions updated with 4 new items. Batch 3 log updated with screenshot review completion note. | (Section 6.6): 8 items across 3 priority tiers covering backup protocol, tagger storage ceiling, tagging fatigue rule, state concentration risk, Phase B success threshold, tagger version control, inter-rater reliability, and IP documentation. Version History renumbered to Section 6.7. |
| 1.2 | 2026-05-29 | NQ methodology locked: no filtered batch, starts unfiltered session-only from event 1. NQ batch log added. Target events updated to 350–400 per instrument. Pre-batch checklist added (Section 3.8). Batch review protocol added (Section 3.9). Screenshot naming convention added (Section 3.10). Confidence flag and macro-event flag added to Section 3.6. Anomaly batch rule added (>15pt LED divergence). End of instrument review template added (Section 5.2). Phase B test plan updated to include GC vs NQ instrument comparison. Strategic direction note added to roadmap: standalone software platform as primary commercial target. Session workflow updated to include pre-batch checklist and review lock step. |

---

*To update: add your change, increment version and date at the top, re-upload to Claude Project.*

---

## 7. Roadmap & Strategic Context

*Added in v1.5 from Roadmap document (vX_ENGINE_Status_In_progress_2.pdf). This section captures the strategic context, build path, competitive landscape, and probability estimates that inform all decisions beyond Phase C.*

---

### 7.1 What the Engine Is — Plain English

Most trading tools tell you what price did. The vX Rhythm Engine asks a different question: **what kind of market is this right now?**

Think of it like a weather report for price action. Is the market in a clean trend? Is it quietly coiling like a spring before a big move? Is a breakout already running out of steam? Or is it random noise where no strategy works well?

The engine reads those conditions and gives you a label — one of seven named states — so you know whether to follow the trend, wait for a breakout, step aside, or be careful that a move is almost over. It does not tell you which direction to trade. It tells you what kind of environment you are in.

**For technical reviewers:** The vX Rhythm Engine is a deterministic, multi-layer market regime classifier implemented in TradingView Pine Script v5. It does not generate directional signals — it classifies behavioral state. Four orthogonal normalized scores (Quality, Compress, Expansion, Exhaust, each 0–100) map to one of seven regime states via a deterministic priority cascade. The key design choice is decomposition — rather than collapsing regime into a single score, the four dimensions can be simultaneously true, which lets the engine distinguish regimes that single-score tools conflate.

---

### 7.2 What v0.5 Becomes — Layer by Layer

**1. Volume layer → the engine gains a second sense**
Right now the engine reads price only — like watching a crowd move with the sound off. Volume tells you why the crowd is moving. High volume on compression means absorption — institutional activity inside the coil. Low volume on compression is drift. The engine currently cannot tell the difference. With the volume layer, Compression Coil and Expansion Burst become behaviorally validated states, not just geometric readings.

*Implementation risk:* Volume data in Pine Script is reported volume, not true tape flow. On GC futures, reported volume can be thin and unrepresentative between sessions. Volume confirmation should be optional or session-gated initially — test it as a filter in Phase B before embedding into the classifier.

**2. Adaptive thresholds → the engine becomes instrument-aware**
Today, GC quiet week and GC CPI week run the same Quality ≥ 55 threshold. That is structurally wrong — behavioral distribution shifts dramatically with volatility regime. Percentile-based rolling thresholds (200-bar window) mean the engine recalibrates continuously. It stops asking "did this score cross a fixed line" and starts asking "is this score unusual for this instrument in this current environment."

*Implementation risk:* Percentile-based rolling thresholds must use only confirmed historical bars. A single indexing error using current bar data in the percentile calculation introduces repainting. Strict use of `[1]` offset on any rolling calculation feeding threshold logic. This needs explicit code review.

**3. Confidence-weighted state → binary labels become a spectrum**
The current priority cascade picks one state and discards everything else. A bar scoring Traversal 0.62 and Expansion 0.58 gets called Expansion and the Traversal information disappears. With confidence output, the engine preserves that ambiguity: "Expansion Burst — 62% conviction" instead of just "Expansion Burst." Position sizing, visual rendering, and alert logic can all track conviction rather than treating every signal as equally valid.

*Implementation risk:* "62% conviction" sounds more precise than the underlying math warrants. Label it clearly as a relative conviction score, not a win probability. Documentation must be explicit about this distinction before any commercial release.

**4. Composite high-conviction signal → the engine gets an opinion**
Instead of seven states firing independently, the engine produces one additional output: a single alert that only fires when the specific combinations empirically proven to have the highest edge all co-occur simultaneously. That is not a new state — it is the engine making a selective judgment call based on measured evidence. A qualitative shift from classifier to decision-support tool.

*Implementation risk:* The composite signal is built from Phase C's highest-edge combinations. If Phase C over-represents specific market conditions, the composite signal is optimized to those conditions and degrades in different regimes. Out-of-sample testing on a separate held-out dataset is required before the composite signal is promoted to primary alert status.

**5. Phase A2 additions → the memory layer grows intelligence**
Session-aware decay: a zone from a high-volume NY session persists longer than one from a quiet Tokyo session. Directional bias tagging: a zone that rejected price from below is labeled structurally differently from one that rejected from above. The memory layer goes from a passive record of where things happened to an active map of how they happened and which direction they matter.

---

### 7.3 The Structural Ceiling

The engine operates on OHLC candle data only. Pine Script v5 does not expose tape-level data — no delta, no aggressor side, no footprint. This is a **platform ceiling, not a design choice.**

Even a perfect v0.5 implementation cannot see what institutional order flow is doing beneath the candle. The engine can be excellent within that ceiling, but it cannot be a substitute for platforms with actual order flow access (Bookmap, Sierra Chart, Quantower).

**What building outside Pine unlocks:**
- Tape data — aggressive vs passive delta, absorption, stop-run footprints, volume-at-price per bar
- Tick-level resolution — state transitions detected before the bar closes, meaningful for entries
- Real-time order book context — liquidity above and below current price, visible imbalances
- Unconstrained computation — adaptive thresholds on 200-bar window is feasible in Pine; machine learning on 50,000 bars of labeled state data feeding back into threshold calibration is not

---

### 7.4 Build Path

**The sequence that matters:**
> Finish Phase C → Phase B → Python prototype → hire engineer → production build

**Stage 1 — Python prototype (you + Claude)**
Before hiring anyone, build a backtesting and replay version in Python. No live data. Feed it existing CSV exports and historical data. Implement the state classifier, memory zones, and fractal sync in Python. This proves the logic ports correctly and gives something concrete to show an engineer.

**Stage 2 — Hire one senior engineer**
Not a team. One person who has specifically built trading tools or financial data applications. Their job is infrastructure and order flow integration — the parts requiring production experience. Creator owns the product logic. Engineer owns the plumbing.

**Stage 3 — UI when the engine is proven**
Do not build the UI until the engine is validated in Python. Many projects fail because they invest in a beautiful interface before confirming the underlying logic works outside its original environment.

**The biggest risk is sequence.** Building full software before Phase C and B complete means building on an unvalidated engine. The Python prototype stage is cheap to build, fast to test, and tells you whether the engine holds up outside Pine before investing in production infrastructure.

If Phase B results come back strong → validated engine + working prototype = a fundable, hirable position.
If they come back mixed → you have spent weeks on a Python script, not months on a production system.

---

### 7.5 Competitive Landscape

| Competitor | What it does | Price | Gap vX fills |
|---|---|---|---|
| Bookmap | Real-time order flow visualization — depth of market, liquidity zones, hidden institutional orders | $49–$99/month | Does not classify behavioral state — shows raw data, user interprets |
| Sierra Chart | Professional charting + order flow | $36/month | Same — data display, not regime classification |
| Quantower | Multi-broker platform + order flow | $70/month | Same |
| MarketTriage | Regime classification across 29 markets | — | Macro/multi-asset focused — not intraday futures |
| HMM-based detectors | Probabilistic regime research tools | Free/open source | Research tools, not trader-facing products |

**The gap vX occupies:** Intraday behavioral state classification with multi-timeframe sync, scored memory zones, and confidence weighting, on futures, at the 5-minute level. This is genuinely not a crowded space in retail tooling.

The market has clearly demonstrated willingness to pay $50–$100/month for specialized trading software. vX at v0.5 — with validated edge, order flow integration, and confidence-weighted states — would be a differentiated product in that price range. It does not need to beat Bookmap. It needs to serve the trader who wants behavioral regime context that Bookmap does not provide.

---

### 7.6 Probability Estimates

*Honest assessments as of the Roadmap document. These numbers move as Phase C and B complete.*

| Question | Probability | Reasoning |
|---|---|---|
| Engine has genuine edge after Phase C + B | 55–65% | Structural reasoning sound. Early LED rates encouraging. But 100 events is not enough to be confident, and Patterns 10 and 11 are unresolved. Goes up significantly if Phase B filters produce consistent improvement across GC and NQ. |
| Validated engine becomes working standalone software | 40–55% | Execution risk. Most research-stage tools with proven logic never become products — builder runs out of momentum, funding, or engineering support. Python prototype stage is the critical filter. |
| Reaches Bookmap-level market presence | 10–20% | Honest ceiling for almost any indie trading software. Bookmap has deep broker integrations, exchange-direct data feeds, a marketplace, and an education ecosystem. That took years and significant capital. |
| **Builds something genuinely useful generating real revenue at smaller scale** | **60–70%** | **The number worth focusing on.** A focused tool used by hundreds or low thousands of active futures traders, subscription-based, profitable as a business without needing to be Bookmap. Realistic, achievable, worth building toward. |

**The number worth focusing on is 60–70%.** It does not require displacing anyone. It requires being the best tool for one specific thing: telling a futures trader what behavioral regime they are in and how much to trust the signal. That is a winnable position. The question is whether the data supports it.

---

### 7.7 What 700–800 Events Does to the Validation

At 100 events the LED rate is directionally interesting but statistically fragile. A single bad batch can move the combined rate 5–8 points. At 700–800 events across two instruments, the project is in a different category entirely.

**What becomes possible at that sample size:**

- **State-level confidence** — Expansion currently has 4 events. At 700+ events there is enough of every state to make instrument-specific and session-specific claims with real confidence intervals.
- **Session stratification** — the Tokyo/London/NY LED rate divergence (35%, 38%, 67% unfiltered) needs volume to confirm. At 700+ events each session runs as an independent sub-dataset.
- **Instrument comparison** — GC vs NQ at comparable sample sizes tells whether the engine is instrument-agnostic or needs per-market calibration. An instrument-agnostic engine is a much bigger addressable market.
- **Filter stacking reliability** — Phase B's filters tested individually and combined need enough events to avoid overfitting. 100 events filtered ten ways produces very small sub-samples. 700+ events gives each filter combination meaningful n.

If 700–800 events complete with consistent LED rates across both instruments and all three sessions, and Phase B filters hold — the unconditional probability of a viable product moves closer to 45–55% from today's starting point. That is before the Python prototype. Before the engineer hire. Just from having a dataset that size with clean methodology.
