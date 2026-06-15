# vX Rhythm Engine — Ground Truth
**Version:** 1.18 | **Last Updated:** 2026-06-07 | **Rubric:** v2
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
| Instruments | GC 5m (active) · NQ 5m (active) |
| Tagging source | TradingView Bar Replay |
| HTFs | 60m · 240m |
| GC 5m | Batch 1 locked (events 1–50) · Batch 2 locked (events 51–100) · Batch 3 locked (events 101–150) · Batch 4 next |
| NQ 5m | Batch 5 locked (events 201–300) · Batch 6 next |
| Combined main total | GC: 150 locked · NQ: 81 PRIMARY locked / 350–400 target per instrument |
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
| Batch 5 | 201–300 | Dec 31 2025 – Jan 9 2026 (wk1+wk2) | ✅ LOCKED 2026-06-07. 81 PRIMARY taggable. LED 45/81 = 55.6%. Session anomaly: London strongest (60%) vs Tokyo weakest (50%) — instrument-specific reversal vs GC pattern. Filter 7 (Dir Conflict+TRANSITION) reversed: 61% LED on NQ vs 44.7% GC — instrument-specific, cannot apply as universal filter. EXPANSION 0% LED (n=4) — Pattern 17 confirmed cross-instrument. HTF rail YES: 79% LED (n=14). FAILED Q≤50: 62% vs Q>50: 25% — Pattern 8 confirmed NQ. Zone density: all events 1–4 — holiday overlap period (NY/London), not representative of standard NQ zone density; ≥10 filter inapplicable to this batch. Sampling: Dec 31 start covered wk1+wk2 through Jan 9 — sampling rule satisfied. Corrections applied: E272 cascade→COMP_TRAV, E286 rail_zone→LOWER_RAIL, timezone audit closed (all UTC+9 confirmed), outcome_atr filled for 19 events (verify in Batch 6 review). |
| Batch 6 | 301–350 | Feb 2026 wk2 | — |
| Batch 7 | 351–400 | Mar 2026 wk2 | — |
| Batch 8 | 401–450 | TBD | — |

**NQ methodology note:** NQ has no filtered batch. Tagging starts unfiltered and session-only from event 1. GC Batch 1 (filtered) has no NQ equivalent by design — the filtered batch on GC was necessary to build the methodology from scratch. On NQ the methodology is proven. NQ Batch 1 is the direct comparison baseline to GC Batch 2 (unfiltered). Any LED rate difference between GC and NQ reflects instrument behavior, not methodology artifacts.

**What's next:** Complete GC 5m tagging (Batches 4–8, second week per month) → continue NQ 5m (Batch 6 onward, same methodology) → Phase B strategy harness when both datasets complete.

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

**outcome_atr definition (locked):** The `outcome_atr` field captures the Maximum Favorable Excursion (MFE) in ATR units — the maximum price reached in the expected direction within bars 1–6 from the signal bar close, measured using bar highs (for UP signals) or bar lows (for DOWN signals). It is the primary quantitative outcome measurement. Record to one decimal place.

**MFE/MAE notes format:** Track both in notes field for every event.
Example: `"MFE 1.8 ATR up, MAE 1.4 ATR down before bounce"`

Measure in ATR (primary). Points/ticks can be added as supplementary notes.

### 3.3b Screenshot Anatomy (Locked 2026-06-03)

*Critical for any AI agent reading screenshots — including the Session Companion and Batch Analyzer. Misidentifying the signal bar produces wrong MFE measurements and wrong pattern identifications.*

**signal.jpg — signal bar identification:**
- The signal bar is always the **last visible bar** on the chart
- A white arrow below the bar confirms the exact signal bar
- Do not use the engine panel badge to find the bar — use the arrow
- Everything to the LEFT of the signal bar is pre-signal context — read it for pattern identification only
- The signal bar's own body movement is pre-signal price action — do not include it in MFE measurement

**outcome.jpg — outcome measurement:**
- The chart is advanced exactly **6 bars** from the signal bar close
- This is the end of the MFE measurement window
- The signal bar from signal.jpg is now visible somewhere in the middle-left of the chart
- Count 6 bars forward from the signal bar close — that is the measurement window
- MFE: the maximum favorable price reached within bars 1–6 (measured from signal bar close using bar highs/lows in the expected direction)
- MAE: the maximum adverse price reached within bars 1–6 (measured from signal bar close using bar highs/lows against the expected direction)

**What the agents must never do:**
- Never measure MFE from the signal bar open or the bar before the signal
- Never treat bars to the LEFT of the signal bar as part of the measurement window
- Never identify a bar in the middle of the chart as the signal bar — it is always the last bar
- Never use outcome bar count from the left edge of the chart — always count 6 forward from the signal bar close

**ATR reference:** Use the ATR value shown in the engine panel at the time of the signal bar, not a retrospective ATR from the outcome screenshot.

### 3.4 State-Specific Cautions (Locked)

**Failed Traversal + High Quality:** A Failed Traversal with Quality > 50 is likely a continuation mislabel, not a genuine failure. If the move is clean (high Q), it did not structurally fail — the engine misclassified a strong directional move. Tag honestly by outcome, but flag with `Q-HIGH` and treat the signal with low confidence. Visual confirmation at a structural zone is required to trust a high-Q Failed Traversal.

**Exhaustion + Low Quality:** Exhaustion of a low-quality (messy, grinding) move is unreliable. Exhaust score alone is insufficient. The prior move needs Quality ≥ 45 for the reversal signal to carry weight. Flag low-quality exhaustion signals with `unstable: state flip` if the state environment was also choppy.

**Exhaustion + Pullback in Trend context:** When Context shows "Pullback in Trend" and both HTFs are aligned in the prior direction, Exhaustion is fighting the macro flow. These signals require higher Exhaust threshold (≥ 65) and a clear extreme rail position before trusting the reversal.

**Expansion Burst:** The Expansion score cannot distinguish a burst at its origin from one that is already well extended. Both produce similar X scores. Always visually confirm that the burst is just beginning at the signal bar. If the large move is already visible well to the left of the signal bar, the channel is wide and flaring, and pre-signal bars are small-bodied — skip or downweight.

### 3.5 Special Cases

**Equilibrium Drift (updated v1.16):**
- `obs_type = RESEARCH_OBS` — excluded from PRIMARY LED rate
- Tag using DRIFT_COMMIT / DRIFT_NEUTRAL / DRIFT_TRAP (not LED/WRONG)
- `outcome_dir` = UP / DOWN / FLAT based on what price actually did
- Note: `drift-transition: [next state]` if state changes within 6 bars
- Note: `drift-at-rail: yes/no` if Drift appears at visible HTF structural level
- Skip window rule: any state change inside the Drift window is significant — close the Drift measurement at that bar, tag the new state as a separate event with its own fresh 6-bar window

**Volatility Distortion (locked v1.16):**
- `obs_type = RESEARCH_OBS` — excluded from PRIMARY LED rate
- No LED/WRONG/CONFIRMED/LAGGED tag — these events are not directional signals
- `outcome_dir` = UP / DOWN / FLAT based on what price did after the distortion
- Note: `macro-distortion: [type]` — record the macro event type (CPI, NFP, FOMC, etc.)
- Note: `distortion-duration: N bars` — how many bars the chaotic behavior lasted
- Minimum n for Phase B analysis: 10 Distortion events
- Research question: does Distortion resolve with directional bias by session? (Tokyo vs London vs NY)

**High-Quality Failed Traversal:** Flag events with Quality > 50 using `Q-HIGH` in notes. Analyse separately when n ≥ 10 FAILED events.

**Multi-state cascades:** When a rapid state cascade occurs (e.g., Failed Traversal → Exhaustion → Memory Zone), tag each state change as a separate event. Cross-reference in notes: `cascade: see E[N]`.

**Exhaustion timing:** Tag at the bar where Exhaustion state FIRST appears, not at the swing high/low.

**Multi-day structural observations (added v1.18):** Some structural patterns (Rail Cycle P19, Dual-Rail Convergence P22, Post-Rail-Break Consolidation P23) operate across 4–12+ hour timeframes that the standard 6-bar PRIMARY measurement window cannot capture. These must always be tagged as `obs_type = RESEARCH_OBS`. Do not assign LED/WRONG/CONFIRMED/LAGGED tags to these events. Record detailed notes using the appropriate logging convention for each pattern. These observations are Phase C2 / post-Phase B research candidates — they are not Phase B filter candidates at current sample sizes.

### 3.6 Special Flags (use in notes field)

**Notes format standard (locked v1.16):** Use `key: value` format separated by ` · ` for multiple entries. Consistent formatting makes notes searchable and Phase B analysis reliable.

```
Good:    macro-event: CPI · drift-transition: COMPRESSION · Q-HIGH
Good:    cascade: see E112 · pre-signal coil: yes, 3 bars
Bad:     "CPI today, looks like compression forming, high quality"
```

**Locked flag formats:**

| Flag | Format | When to use |
|---|---|---|
| `macro-event: [type]` | `macro-event: CPI` | Signal fired during known macro event week |
| `drift-transition: [state]` | `drift-transition: COMPRESSION` | Equilibrium Drift that resolved into a new state within 6 bars |
| `drift-at-rail: [yes/no]` | `drift-at-rail: yes` | Drift at visible HTF structural level |
| `cascade: see E[N]` | `cascade: see E112` | Cross-reference cascade partner event |
| `pre-signal coil: yes, N bars` | `pre-signal coil: yes, 4 bars` | ATR contraction visible before signal bar |
| `Q-HIGH` | `Q-HIGH` | Quality > 50 and outcome WRONG or ambiguous |
| `bar-arrow-conflict` | `bar-arrow-conflict` | Signal bar body direction contradicts state arrow (use dir_conflict field too) |
| `macro-distortion: [type]` | `macro-distortion: NFP` | Volatility Distortion state — see 3.5 |
| `time-filter: pre-session` | `time-filter: pre-session` | Signal fired in low-quality time window |
| `time-filter: end-session` | `time-filter: end-session` | Signal fired at session close |
| `unstable: state flip` | `unstable: state flip` | State changed multiple times around signal bar |
| `htf-rail: yes` | `htf-rail: yes` | Legacy flag — use htf_rail_align field in v5.1+ |
| `zone-type-diversity: multi` | `zone-type-diversity: multi` | Legacy flag — use zone_diversity field in v5.1+ |
| `NY-open: first bar` | Signal fires on the first 1–2 bars after 22:00 NY open — highest volatility transition point |
| `bar-arrow-conflict` | Signal bar body direction contradicts state arrow direction |
| `confidence: high/medium/low` | Tagger's confidence in the tag — use when a judgment call was made |
| `macro-event: [type]` | Signal fired during a known macro event week (FOMC, CPI, NFP) |
| `htf-rail: yes/no` | Signal fires at a visible HTF (60m or 240m) structural level — not just the 5m rail. Log from this point forward for all Failed Traversal and Exhaustion events. *(Pattern 14)* |
| `zone-type-diversity: single/multi` | Whether 2+ different zone colours (red, orange, blue) overlap at signal level. Multi-type = higher reversal quality. *(Pattern 12)* |
| `liquidity-sweep: [session]-[high/low]` | `liquidity-sweep: tokyo-high` | FAILED or EXHAUSTION signal fires at or within 0.5 ATR of the prior session's extreme high or low. Log session and direction: tokyo-high / tokyo-low / london-high / london-low. *(Pattern 20)* |
| `rail-cycle: [leg]` | `rail-cycle: origin` | RESEARCH_OBS event at a rail-touch point within a documented full-cycle structure. Values: origin / peak / return. *(Pattern 19)* |

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
- [ ] Confirm tagger is on correct version: v5.1 for E201+ (GC) · v6 for NQ E001+
- [ ] Confirm instrument and timeframe are set correctly (GC or NQ · 5m)
- [ ] Confirm HTFs are set (60m · 240m)
- [ ] Confirm session windows are correctly set in TradingView (UTC+9 reference)
- [ ] Note any known macro events in the selected week in the batch log before starting
- [ ] Confirm Ground Truth version in use matches the current uploaded version
- [ ] Reminder: check mid_window_change at bar 3 of every measurement window — update original event if sync or context changed
- [ ] Reminder: Equilibrium Drift → obs_type = RESEARCH_OBS · use DRIFT_COMMIT / DRIFT_NEUTRAL / DRIFT_TRAP tags
- [ ] Reminder: Volatility Distortion → obs_type = RESEARCH_OBS · no LED/WRONG tag · note macro-event type in notes
- [ ] Reminder: outcome_atr is required for every tagged event — fill at the time of tagging, not retrospectively

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
- [ ] **Q-N** — Does the LED rate at rail-touch events within a documented Rail Cycle (P19) exceed the LED rate at isolated rail-touch events without prior cycle context? Log `rail-cycle: [origin/peak/return]` on future RESEARCH_OBS events. Answer when: 10 documented cycles with ≥1 tagged event per leg (both instruments).
- [ ] **Q-O** — Does a `liquidity-sweep` context (P20) on FAILED/EXHAUSTION produce a materially higher LED rate than FAILED/EXHAUSTION at non-liquidity-sweep levels? Answer when: n=20 events with `liquidity-sweep` note logged.
- [ ] **Q-P** — Do TRAVERSAL events starting at one rail systematically reach the opposite rail? What is the typical state sequence across a full rail-to-rail move? Answer when: n=50 rail-touch events per state (rail_zone field + state transitions + outcome_atr).
- [ ] **Q-Q** — Do certain states (NEUTRAL/DRIFT) cluster in mid-channel? Is mid-channel TRAVERSAL systematically different from rail TRAVERSAL in terms of LED rate? Answer when: n=30 mid-channel events per state. Related to P5 (mid-channel TRAVERSAL Q60–70 = WRONG).
- [ ] **Q-R** — When price reaches a rail, what predicts bounce vs breakthrough? Does HTF alignment or Quality score at the rail-touch predict the next move direction? Answer when: n=50 rail-touch events (rail_zone + htf_rail_align + quality + outcome_dir).
- [ ] **Q-S** — How often do lower rail touches produce full cycles vs directional breakouts? What predicts cycle completion vs a sustained break? Answer when: n=30 lower rail touch events. *Note: requires multi-day tracking beyond the standard 6-bar framework — RESEARCH_OBS tagging only.*
- [ ] **Q-T** — Does EXHAUSTION at the opposite rail reliably mark cycle reversal? What E-score threshold predicts cycle completion vs continuation? Answer when: n=20 EXHAUSTION events at rails. Related to P19 (Rail Cycle) and P9A (Exhaustion Type A).
- [ ] **Q-U** — Do rail cycles correlate with session boundaries? Does the gap open predict cycle initiation? What is the average cycle duration? Answer when: n=20 complete documented cycles (session field + datetime + multi-day tracking).
- [ ] **Q-V** — When HTF rails converge (60m + 240m within ~50pts), does the convergence zone create stronger support/resistance than single-rail? Do bounces from convergence zones produce larger MFE? Answer when: n=20 rail convergence events (requires custom note field tracking rail spacing). Related to P22.
- [ ] **Q-W** — When price breaks through HTF rail support, how long does consolidation last? Does dual-rail break produce longer consolidation than single-rail? Does consolidation duration predict resolution direction? Answer when: n=20 rail break events (time-series tracking of rail break events + consolidation duration + resolution direction). Related to P23.

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
| 2026-06-07 | Batch 5 | NQ 5m | 81 PRIMARY (+8 DRIFT +2 FD) | 45 (55.6%) | 6 (7.4%) | 5 (6.2%) | 25 (30.9%) | ✅ LOCKED. Session-only, unfiltered. Dec 31 2025–Jan 9 2026 (wk1+wk2, holiday overlap). London strongest session (60%), Tokyo weakest (50%) — reversed vs GC. Filter 7 instrument-specific: Dir Conflict+TRANSITION = 61% LED on NQ vs 44.7% GC. EXPANSION 0% (n=4) — Pattern 17 confirmed cross-instrument. HTF rail YES: 79% LED. FAILED Q≤50: 62% — Pattern 8 confirmed NQ. Zone density 1–4 throughout (holiday period, not representative). Corrections applied: E272 COMP_TRAV, E286 LOWER_RAIL, timezone closed, outcome_atr filled (verify Batch 6). |

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

---

**NQ 5m — Batch 5 locked (E201–E300, 81 PRIMARY taggable):**

| State | n | LED | CONFIRMED | LAGGED | WRONG | LED % |
|---|---|---|---|---|---|---|
| TRAVERSAL | 45 | 29 | 4 | 3 | 9 | 64.4% |
| FAILED | 20 | 11 | 1 | 1 | 7 | 55.0% |
| EXHAUSTION | 10 | 5 | 1 | 0 | 4 | 50.0% |
| EXPANSION | 4 | 0 | 0 | 1 | 3 | 0% — Pattern 17 confirmed |
| COMPRESSION | 2 | 0 | 0 | 0 | 2 | 0% — n too small |
| **TOTAL** | **81** | **45 (55.6%)** | **6 (7.4%)** | **5 (6.2%)** | **25 (30.9%)** | **55.6%** |

**NQ session breakdown (Batch 5, 81 PRIMARY taggable):**

| Session | n | LED% | GC equivalent | Note |
|---|---|---|---|---|
| London | 25 | 60% | GC 47.1% | ⚠ Strongest on NQ — reversed vs GC |
| NY | 30 | 57% | GC 63.8% | Consistent but lower than GC |
| Tokyo | 26 | 50% | GC 57.7% | Weakest on NQ — structurally expected for US equity index |

**NQ filter preview (Batch 5 — directional only, n too small for conclusions):**

| Filter | n | LED% | vs GC | Note |
|---|---|---|---|---|
| Rail any (UPPER+LOWER) | 47 | 66% | GC ~70% | ✅ Rail proximity confirmed cross-instrument |
| LOWER_RAIL only | 21 | 71% | — | Strongest single filter in batch |
| HTF rail YES (FAILED+EXHAUST) | 14 | 79% | — | Pattern 14 confirmed NQ — directionally very strong |
| FAILED Q≤50 | 16 | 62% | GC 56% | Pattern 8 confirmed NQ |
| Dir Conflict + TRANSITION | 23 | 61% | GC 44.7% | ⚠ REVERSED — instrument-specific, cannot apply as universal filter |
| MID_CHANNEL | 33 | 42% | — | Pattern 7 confirmed NQ — mid-channel penalty |
| EXPANSION all | 4 | 0% | GC 25% | Pattern 17 confirmed cross-instrument |

**⚠ Zone density note (NQ Batch 5):** All 81 events have zone_density 1–4. This reflects the NY/London holiday overlap period (Dec 31 – Jan 9) — reduced institutional activity produces fewer zone accumulations. This is a period characteristic, not a data error or instrument difference. The GC ≥10 filter is inapplicable to this batch. Monitor zone density in Batch 6 (Feb wk2) to establish a standard NQ baseline.

**NQ Batch 5 corrections — all resolved:**
- ✅ E272 cascade: corrected to COMP_TRAV
- ✅ E286 rail_zone: corrected to LOWER_RAIL
- ✅ Timezone audit: closed — all events confirmed correctly recorded in UTC+9
- ✅ outcome_atr: filled for 19 events — verify against corrected CSV in Batch 6 review
- ✅ Sampling rule: Dec 31–Jan 9 covers wk1+wk2 — sampling rule satisfied

**Targets:**
- GC 5m total events: 350–400
- NQ 5m total events: 350–400
- Minimum per state: n ≥ 30 (events below this threshold flagged INSUFFICIENT DATA in Phase B — not used in go/no-go calculation)
- Rare state capture rule: when Expansion or Compression appears, tag full transition sequence — do not allow skip window to suppress rare state events

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

### 5.3 Batch 3 Screenshot Review Log

*Full 145-event screenshot review completed 2026-05-30. 145/145 signals reviewed across Batches 1–3. 4 new patterns found. 4 existing patterns confirmed. 2 tag flags raised. 2 corrections needed. 8 notes updates needed.*

---

**PATTERN CONFIRMATIONS — strongly confirmed across full dataset**

| Pattern | Confirmation | Key evidence |
|---|---|---|
| P7 — Quality-rail interaction | ✅ Confirmed strongly | E16, E38, E91, E96, E102, E103, E136 are clear mid-channel WRONG examples. Visible without exception across all 3 batches. |
| P11 — Post-move trap | ✅ Confirmed strongly | Single most visible WRONG visual signature in Batch 3. E51, E60, E62, E65, E84, E85, E86, E102, E103, E109, E136, E144 all show large move complete to left, channel wide and flaring. |
| P15 — Micro-compression before Exhaustion | ✅ Confirmed strongly | LED Exhaustion events across all 3 batches show 3–5 bars narrowing range before signal bar. E24, E25, E30, E31, E34, E45, E48, E49, E52, E56, E61, E72, E79, E115, E127, E129, E141. |
| P13 — STRONG_SYNC Traversal visual signature | ✅ Confirmed | All STRONG_SYNC Macro Aligned Traversal events share one visual: rail-walking, consistent small same-coloured candles, channel narrowing or parallel, no opposite wicks. E19, E35, E36, E42, E53, E54. All LED. Visually distinct from every TRANSITION Traversal in the dataset. **Refinement v1.14:** STRONG_SYNC alone is insufficient. One WRONG event observed June 2026 with STRONG_SYNC + BAR_OPPOSE direction mismatch (dir_conflict = BAR_OPPOSE). Engine direction badge opposed visual candle direction despite strong sync — outcome was WRONG. STRONG_SYNC must be accompanied by direction coherence (dir_conflict = NONE) to carry full LED probability. Track via dir_conflict field in tagger v5. |

**NEW PATTERNS — not previously documented (added to Section 5.4)**

| Pattern | Summary |
|---|---|
| P12 — Zone type diversity | LED Exhaustion + Failed Traversal: 2–3 different zone types overlapping (red + orange + blue simultaneously). WRONG: only one type. Diversity stronger predictor than count alone. Evidence: E12, E24, E31, E45, E49, E58, E120, E122, E125, E127, E129, E130, E141, E143. |
| P14 — Failed Traversal at HTF structural level | LED Failed Traversal consistently fires at 60m or 240m channel boundary — not merely 5m rail. Fast clean reversals, large MFE. Evidence: E11, E21, E22, E39, E43, E58, E75, E83, E89, E118, E120, E122, E124, E125, E130, E143. All LED. |
| P17 — Expansion Burst timing anatomy | LED Expansion: channel tight and parallel at signal bar. WRONG Expansion: channel already wide and flaring, large move visible before signal. E37 (WRONG, STRONG_SYNC) confirms timing is a score architecture limitation, not a filter issue. |
| P18 — Direction Conflict is genuine structural condition | Direction Conflict + TRANSITION (n=47, 44.7% LED) = single largest WRONG cluster. E64–E70, E84–E86 show consecutive sessions of Direction Conflict with consistently mixed outcomes. |

---

**TAG FLAGS — ACTION REQUIRED**

**E145 — ✅ RESOLVED — LED confirmed**
Failed Traversal flat arrow (—). Prior move = UP (price ran up into the ~4492 area before failing). FLAT direction rule applied: infer direction from prior move → direction = UP → expected outcome = DOWN. MFE: ~26 points DOWN within 6 bars. Price never moved UP by 1 ATR before dropping. LED tag confirmed correct. Flag closed 2026-05-31.
→ *Note to add to E145: "FLAT arrow — direction inferred as UP (prior move). Expected outcome DOWN. MFE ~26pts DOWN within 6 bars. LED confirmed."*

**E63 — ⚠ Anomaly logged**
Expansion Burst DOWN, CONFLICT sync, tagged LED. Engine documentation states CONFLICT = red-light condition. LED tag appears correct by 6-bar MFE rule. Log as anomaly: "Pattern 17 anomaly — Expansion LED under CONFLICT sync. Engine documentation contradiction. Log for Phase A review." Do not change tag — MFE rule governs. Note the contradiction for Phase A.

---

**CORRECTIONS NEEDED — factual errors**

**E90 — Tag correction: EXHAUSTION → TRAVERSAL**
Tag confirmed EXHAUSTION. Screenshot clearly shows STATE = Exhaustion, not Failed Traversal. Note flag was mislabelled — this is an Exhaustion event (Q53, Exhaust 60) in Pullback in Trend context, tagged WRONG correctly. Flag should read "Exhaust-type-A: prior Q below 45 threshold." Remove `E-HIGH FAILED` flag. Replace with `exhaust-type-A: prior Q below 45 threshold`.

**E91 — State correction: FAILED → TRAVERSAL**
Q-HIGH FAILED state with Quality > 60 but this is a Clean Traversal event, not FAILED. Q-HIGH flag is correct — Q62 WRONG Traversal is exactly what Pattern 7/8 describes — but the note text misidentified the state. Visual confirms: Clean Traversal DOWN, mid-channel, sparse zones, large bearish move already underway before signal. Classic Pattern 11 post-move trap combined with Pattern 5 mid-channel.
→ *Correction: change state note from "FAILED state" to "TRAVERSAL state." Add "Pattern 5: mid-channel · Pattern 11 candidate."*

---

**NOTES UPDATE NEEDED — tags confirmed, notes require clarification**

| Event | Current tag | Issue | Correction |
|---|---|---|---|
| E99 | WRONG | Note mislabel — same error as E91. Says "FAILED state" but is TRAVERSAL. | Change to "TRAVERSAL state. Pattern 11: large move already complete, post-move trap." |
| E102 | WRONG ✅ | Pattern 11 confirmed. Both E102 and E103 consecutive Traversal DOWN, channel wide/flaring. Bar-arrow-conflict flag appropriate. | Add: "Pattern 11 confirmed — channel wide/flaring, large move complete to left. Verify skip window between E102 and E103." |
| E117 | LED ✅ | Bar-arrow-conflict flag correct. Bearish bar but engine direction UP. Conflict did NOT produce WRONG — direction prevailed. | Add: "bar-arrow-conflict: engine direction prevailed over bar body. Valid evidence for P16 bar-arrow-conflict analysis." |
| E126 | WRONG ✅ | Exhaustion with flat arrow (—), Q70, Exhaust 61. Prior move DOWN. Dual-condition technically met. No reversal in 6-bar window. Memory zones failed to hold. | Add: "exhaust-type-B: dual-condition met but macro flow overwhelmed local exhaustion. Memory zones failed to hold." |
| E131 | LAGGED ✅ | Note says "Q-HIGH: SIDEWAYS state" — SIDEWAYS is not a valid state label. Market was likely consolidating. | Clarify note: replace "SIDEWAYS state" with "post-move consolidation — engine fired late after UP move complete." |
| E132 | WRONG ✅ | Clean Traversal UP, Q62, pre-NY session (40 min before open). Sparse zones (11 present). Pre-session filter appropriate. | Note is correct. Add: "pre-session filter — this is exactly the kind of signal the session filter should eliminate." |
| E134, E136 | E134 LED ✅ · E136 WRONG ✅ | Both bar-arrow-conflict Pattern 16 candidates. E134 bearish bar, price moved UP — LED. E136 bearish bar, mid-channel — WRONG. Contrast between these two events is valuable: bar-arrow-conflict + rail support = can still LED. bar-arrow-conflict + mid-channel = WRONG. | Add to both notes: "P16 candidate: bar-arrow-conflict + [rail/mid-channel]." |
| E138 | LED ✅ | Failed Traversal with flat arrow (—). Prior trend clearly UP. Direction should be logged as DOWN per the FLAT direction rule: infer from prior move. | Add: "FLAT arrow — direction inferred from prior UP move. Direction = DOWN. Note 'update direction field from FLAT to DOWN.'" |
| E144 | WRONG ✅ | Clean Traversal UP, Q70, TRANSITION sync, Direction Conflict context. Screenshot shows price in clear downtrend — UP signal fires against macro flow, mid-channel. All three negative conditions simultaneously: bar-arrow-conflict, direction conflict, mid-channel position. Strong Pattern 11 + Pattern 5 combination. | Add: "Pattern 11 + Pattern 5 combination. bar-arrow-conflict, direction conflict, mid-channel — triple negative condition." |

---

**CONFIRMED — no action needed**

| Event | Tag | Notes |
|---|---|---|
| E92 | CONFIRMED ✅ | End-of-session note appropriate. Pattern 5 observation (60m channel interaction) useful to keep. |
| E99 | WRONG ✅ | Tag correct by outcome. Note correction only (see above). |
| E134 | LED ✅ | Bar-arrow-conflict, engine direction prevailed. Valid P16 evidence. Note addition only. |
| E136 | WRONG ✅ | Bar-arrow-conflict + mid-channel = WRONG. Valid P16 evidence. Note addition only. |

---

*Review complete: 145/145 signals · 4 new patterns · 4 confirmed · 2 flags raised (both resolved) · 2 corrections · 8 notes updates*

### 5.4 Visual Pattern Observations — Unconfirmed Hypotheses

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

**⚠ NQ instrument note (Batch 5):** Direction Conflict + TRANSITION produced 61% LED on NQ (n=23) — a complete reversal of the GC pattern. Filter 7 cannot be applied as a universal cross-instrument filter. Must be tested and applied instrument-specifically in Phase B.

---

**Pattern 19 — Rail Cycle: Full HTF Rail-to-Rail Traversal**

*First observed NQ Batch 5 (E201–E300) · Added v1.18 · 2026-06-07. n=3 at this sample size. Not confirmed — minimum n=10 required before conclusions.*

On NQ 5m, a recurring macro-scale structure is observable across sessions: price initiates at one channel rail (lower or upper), traverses to the opposite rail where an Exhaustion or Neutral state fires, then returns to the origin rail — completing a full cycle. The cycle can span 8–12+ hours across session boundaries. Within the 6-bar MFE window, individual signal bars at rail-touch points (particularly EXHAUSTION and NEUTRAL at an extreme rail) show LED outcomes. The significance is structural: the engine correctly identifies the rail-touch events within a larger cycle it cannot see as a whole.

E227 is the clearest example — annotated on the screenshot: "The price touches 60M rail to the down side" — full rail-to-rail-to-rail cycle, signal at lower rail touch, peak at upper rail exhaustion, return to lower rail ~12 hours later. E235 (EXHAUSTION LED at cycle peak) and E256 (DRIFT_COMMIT at lower rail return) are supporting events.

*Relationship to existing patterns:* Extends Pattern 14 (HTF structural level on FAILED/EXHAUSTION) to a dynamic cycle framing rather than a static level. The rail-touch event is the same; what is new is the recognition that it occurs as part of a predictable full-cycle structure. The cycle context may increase the LED probability at the touch point — this is Q-N.

*Logging convention (from this batch forward):* For RESEARCH_OBS events at a visible rail-touch point within a documented full cycle, add to notes: `rail-cycle: [origin/peak/return]`.

*Minimum n for Phase B conclusions:* 10 documented cycles with at least one tagged event per cycle leg (both instruments combined).

*Evidence:* E227 (NQ, lower rail touch → CONFIRMED), E235 (NQ, upper rail exhaustion → LED), E256 (NQ, lower rail return → DRIFT_COMMIT).

**Sub-observation (Session Companion 2026-01-07/09):** EXHAUSTION at the opposite rail (E≥70, Q≤40) appears to be the primary turning point marker within a full Rail Cycle — the state that confirms the cycle is reversing toward the origin rail. This is consistent with P9A (Exhaustion of a low-quality move) firing at the structural extreme. Log as Q-T (EXHAUSTION as cycle turning point) until n=20 EXHAUSTION-at-rail events are accumulated.

---

**Pattern 20 — Session Liquidity Sweep: Prior Session High/Low Taken Before Continuation**

*First observed NQ Batch 5 (E271, E277) · Added v1.18 · 2026-06-07. n=2 at this sample size. Not confirmed — minimum n=20 required before conclusions.*

At London open (16:00 UTC+9) on NQ, price frequently sweeps the high or low established during the Tokyo session before reversing in the direction of the prevailing macro flow. The mechanism: stops accumulated at the Tokyo session extreme are taken in a fast spike, triggering a Failed Traversal or Exhaustion state at or just beyond the Tokyo level, followed by a clean reversal continuation. The engine correctly detects the structural rejection at the liquidity level as a Failed Traversal.

E271 is the clearest example — annotated on the screenshot: "Tokyo liquidity taken," "Rejection," "Target: Tokyo low + memory zone." Failed Traversal UP, Q33, TRANSITION sync, price spiked above the Tokyo range then reversed sharply to the downside. LED confirmed. E277 adds a second observation: NY session sweeping Tokyo session liquidity before continuation upside.

*What this means for the engine:* A Failed Traversal that coincides with a prior session's extreme high or low is a higher-conviction reversal candidate than a Failed Traversal mid-session with no prior-session level. The `htf_rail_align` field does not currently distinguish prior-session extremes from 60m/240m channel rails — this is a sub-category of HTF structural confluence.

*Logging convention (from this batch forward):* For FAILED and EXHAUSTION events that fire at or within 0.5 ATR of the prior session's extreme high or low, add to notes: `liquidity-sweep: [session]-[high/low]` (e.g., `liquidity-sweep: tokyo-high`).

*Minimum n for Phase B conclusions:* 20 events with `liquidity-sweep` note, split by session transition (Tokyo→London, London→NY).

*Evidence:* E271 (NQ, London open, Tokyo high swept → FAILED UP → LED DOWN), E277 (NQ, NY session, Tokyo low swept → continuation UP).

---

**Pattern Name Reservation — P21: Direction Mismatch (BAR_OPPOSE)** *(moved from P20 — 2026-06-07)*

*Added v1.14 as P20. Moved to P21 to accommodate P20 Session Liquidity Sweep — 2026-06-07.*

**The observation:** When the engine direction badge (UP/DOWN arrow) opposes the visual signal bar candle direction (bullish/bearish close), the outcome appears to be reliably WRONG. Two observations at n=2 show 0% LED rate. Both involved BAR_OPPOSE direction mismatch.

**Current status:** NOISE — n=2. Cannot distinguish from random variation. No conclusions permitted at this sample size.

**How it is already captured:** `dir_conflict = BAR_OPPOSE` in tagger v5 captures this observation mechanically on every event. P21 will be fully testable when BAR_OPPOSE events reach n≥20 in the cumulative dataset.

**What P21 will test at n≥20:**
- LED rate for BAR_OPPOSE vs NONE events
- Whether PULLBACK_IN_TREND context moderates the pattern
- Interaction with P5 (mid-channel Q60-70) — compound risk
- Interaction with P13 (STRONG_SYNC) — already confirmed one case

**Name reservation rule:** P21 is reserved. It will be formally added to the pattern library when BAR_OPPOSE events reach n≥20 and LED rate difference vs NONE events is ≥10 percentage points.

**Session Companion instruction:** Do not report P21 as a confirmed pattern. Report as "P21 candidate — n=[current BAR_OPPOSE count], minimum 20 required before conclusions."

---

**Pattern Name Reservation — P22: Dual-Rail Convergence Resistance**

*First observed NQ Batch 5 session research (Jan 7–9, 2026) · Added v1.18 · 2026-06-07. n=1. Not confirmed — minimum n=20 required before conclusions.*

When the 60m and 240m channel rails converge to within approximately 50 points of each other at the same price level, the resulting dual-timeframe zone appears to create meaningfully stronger support or resistance than a single-rail level. In the first observation, price required a "VERY STRONG" directional move to break through the convergence zone, suggesting that converged rails produce compounded structural resistance. Bounces from dual-rail convergence zones may produce larger MFE than single-rail bounces — this is Q-V.

*Relationship to existing patterns:* Extension of Pattern 14 (HTF structural level on FAILED/EXHAUSTION). A dual-rail convergence zone is a sub-category of HTF structural confluence where two independent timeframes agree precisely on a level.

*Logging convention:* For FAILED, EXHAUSTION, or TRAVERSAL events near a visible HTF rail convergence, add to notes: `rail-convergence: [approx pts spacing]` (e.g., `rail-convergence: ~40pts`).

*Minimum n:* 20 events at documented convergence zones. Requires manual identification — no current engine metric captures rail spacing directly.

*Evidence:* Single NQ observation Jan 7–9, 2026 (session research, not a PRIMARY tagged event).

---

**Pattern Name Reservation — P23: Post-Rail-Break Extended Consolidation**

*First observed NQ Batch 5 session research (Jan 9, 2026) · Added v1.18 · 2026-06-07. n=1. Not confirmed — minimum n=20 required before conclusions.*

When price breaks through HTF rail support (particularly a dual-rail convergence zone per P22), an extended consolidation period of 4+ hours may follow before directional resolution. In the first observation: dual-rail break → ~6-hour consolidation → resolution UP to mid-rail, which may represent a false breakdown signal. The consolidation duration and resolution direction may be predictable from context at the break — this is Q-W.

*Important scope note:* This pattern operates on a multi-hour timeframe that the standard 6-bar PRIMARY measurement framework cannot capture. Events related to P23 should be logged as RESEARCH_OBS with detailed notes. They are not Phase B filter candidates at current n. This is a Phase C2 / post-Phase B research area.

*Logging convention:* For RESEARCH_OBS events at an HTF rail break with visible consolidation, add to notes: `rail-break: [single/dual] · consolidation: [duration in hours] · resolution: [up/down/pending]`.

*Minimum n:* 20 rail-break events with consolidation duration documented.

*Evidence:* Single NQ observation Jan 9, 2026 (session research, not a PRIMARY tagged event). Dual-rail break → 6-hour consolidation → UP resolution.

---

**Candidate Observation — POC Coincidence (Q-M) · Post-Phase B validation study**

*Added v1.13 · 2026-06-02. Observed live on GC 5m and NQ during active session. Not a tagging variable. Not a Phase C research item. Logged as a post-Phase B validation candidate.*

**The observation:** Memory zone density clusters on GC 5m and NQ 5m appear to systematically coincide with Volume Profile Point of Control (POC) levels. On multiple NQ sessions, the highest-density memory zone area sits at or within a few ticks of the session POC. The same pattern is visible on GC intraday charts.

**Why this is structurally meaningful:** The POC is where the most volume traded over a given period — the level of maximum price acceptance by both buyers and sellers. The engine's memory zones spawn at state transitions — moments where behavioral character changed. Both methods are independently identifying the same structural phenomenon: price levels where the market concentrated activity and participants built the strongest positional memory. The POC measures this through volume. The memory zone layer measures it through behavioral state transitions. Their convergence is evidence that the zone layer is detecting structural significance without requiring volume data.

**Why this matters for the engine's validity:** The GC volume limitation documented in Section 6 (TradingView reports exchange volume only — excludes OTC gold and ETF arbitrage flows) means volume-based analysis on GC is structurally incomplete. If the memory zone layer reliably approximates what volume profile identifies independently — and does so on OHLC data alone — that is a meaningful architectural validation. It suggests the state transition logic is finding real structural levels, not noise.

**Instrument consistency note:** The observation holds on both GC and NQ. GC is macro-driven (USD, rates, geopolitical risk). NQ is equity-correlated (Fed policy, tech earnings). The fact that POC-zone coincidence appears on both structurally different instruments suggests this is a universal property of price structure, not an instrument-specific artifact.

**What this does NOT mean:**
- This observation does not require adding POC as a tagger field during Phase C
- This observation does not change any locked methodology decisions
- This does not constitute a new filter for Phase B (volume data is excluded from the OHLC-only validation methodology)

**Post-Phase B study design (when relevant):**
If Phase B confirms OHLC-only engine edge, design a dedicated POC validation study:
1. Export 50 GC and 50 NQ sessions with both the memory zone layer output and volume profile data
2. Measure: what % of zone_density ≥ 10 cluster midpoints fall within X ticks of the session POC?
3. Compare: POC proximity for LED events vs WRONG events
4. If POC-zone coincidence is systematic (>70% alignment): document as independent validation of the memory zone architecture in the methodology summary (Section 9.11)

**Phase B Analyst note:** This study does not block the go/no-go decision. It runs after Phase B closes, as a validation addendum, not a filter test.

---

**Pattern Name Reservation — P20: Direction Mismatch (BAR_OPPOSE)**

*Added v1.14 · 2026-06-03. Reserved pattern name. Not yet confirmed. Minimum n=20 required before any conclusions.*

**The observation:** When the engine direction badge (UP/DOWN arrow) opposes the visual signal bar candle direction (bullish/bearish close), the outcome appears to be reliably WRONG. Two observations at n=2 show 0% LED rate. Both involved BAR_OPPOSE direction mismatch.

**Current status:** NOISE — n=2. Cannot distinguish from random variation. No conclusions permitted at this sample size.

**How it is already captured:** `dir_conflict = BAR_OPPOSE` in tagger v5 captures this observation mechanically on every event. No new fields are needed. P20 will be fully testable when BAR_OPPOSE events reach n≥20 in the cumulative dataset.

**What P20 will test at n≥20:**
- LED rate for BAR_OPPOSE vs NONE events
- Whether PULLBACK_IN_TREND context moderates the pattern
- Interaction with P5 (mid-channel Q60-70) — compound risk
- Interaction with P13 (STRONG_SYNC) — already confirmed one case

**Name reservation rule:** P20 is reserved. It will be formally added to the pattern library when BAR_OPPOSE events reach n≥20 and LED rate difference vs NONE events is ≥10 percentage points.

**Session Companion instruction:** Do not report P20 as a confirmed pattern. Report as "P20 candidate — n=[current BAR_OPPOSE count], minimum 20 required before conclusions."

---

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

**Cannot be tested in Phase B from current data:**
- Pattern 10 (Expansion timing) and Pattern 11 (post-move trap) require channel-width velocity — v0.5 component
- Pattern 17 (Expansion timing anatomy) — same issue, same v0.5 solution
- Pattern 13 (STRONG_SYNC visual signature) — insufficient n (8 events at 145 total), needs more data

---

### 5.5 Phase B — Known Gaps and High-Priority Analyses

*Added v1.8. Seven analytical gaps identified — these fields are captured in the dataset but not yet in the Phase B test plan. Two are potentially more impactful than any of the 10 current filters.*

---

**🔴 GAP 1 — Context label is captured but never analyzed (HIGH PRIORITY)**

Every event has a Context label (Macro Aligned, Direction Conflict, Pullback in Trend, Counter-Trend, Mixed). The engine's own documentation states Context = Macro Aligned + STRONG_SYNC is the green light and Counter-Trend = red light. That hypothesis is sitting in the dataset unexamined.

Phase B question: does LED rate on Macro Aligned events significantly outperform LED rate on Counter-Trend events? If yes → Context becomes a mandatory filter. If no → it's a UX feature, not an edge feature.

Current data preview (150 events): Macro Aligned → 66.7% LED (n=12). Direction Conflict → 46.0% + TRANSITION. This gap is already visible.

**→ Add to Phase B: LED rate by every Context label. Treat as a potential primary filter, not a secondary analysis.**

---

**🔴 GAP 2 — Sync state is captured but never formally tested (HIGH PRIORITY)**

STRONG_SYNC, MIXED, CONFLICT, TRANSITION are on every event. The engine claims STRONG_SYNC is the highest-edge regime. At 150 events there is already enough data for a basic comparison.

Current data (150 events): MIXED 70.8% LED (n=24) · STRONG_SYNC 62.5% (n=8) · CONFLICT 56.5% (n=23) · TRANSITION 51.1% (n=94).

If STRONG_SYNC reaches 75%+ at 350+ events and CONFLICT stays near 35–40%, that single filter transforms the strategy. It is potentially the most powerful filter in the entire dataset. It is not in the Phase B plan.

**→ Add to Phase B as Filter 11: STRONG_SYNC only · and Filter 12: exclude CONFLICT. Treat as priority equal to Filter 7.**

---

**🟡 GAP 3 — Score values used as binary thresholds only**

Quality, Compress, Expansion, Exhaust scores are recorded as exact numbers (0–100) but treated as binary — did they cross the threshold? A Quality of 87 is structurally different from a Quality of 56. Both cross 55 and are classified identically.

Phase B should treat score values as continuous variables: does LED rate improve as Quality increases above 55? Is there a secondary threshold at 70+ or 80+ that further separates LED from WRONG? Current preview: TRAVERSAL Q≥76 → 100% LED at n=4 (too small to confirm but directionally strong).

**→ Add to Phase B: plot LED rate by Quality decile (55–60, 61–70, 71–80, 81+) for TRAVERSAL. Run same analysis for Exhaust score on EXHAUSTION events.**

---

**🟡 GAP 4 — Memory zone count threshold chosen visually, not empirically**

The ≥10 threshold was updated from ≥8 based on data but the exact inflection point has not been formally tested. The field contains exact counts (6, 9, 12, 14). Phase B should test whether the optimal threshold is 8, 10, or 12, and whether there is a continuous relationship where every additional zone above 6 incrementally improves LED rate.

**→ Add to Phase B: plot LED rate by memory zone count in bands (≤6, 7–9, 10–12, 13+). Find the actual inflection point empirically.**

---

**🟡 GAP 5 — Volatility Distortion absence needs explicit acknowledgment**

Volatility Distortion appears zero or near-zero in the 150-event dataset. Two explanations: either it genuinely fires rarely on GC 5m (useful information) or the session filter is suppressing it because chaotic price action happens mostly outside session windows. Either way Phase B will have nothing to say about Distortion.

**→ Add to End of Instrument Review: explicitly document Distortion event count and note whether absence reflects instrument behavior or session scope.**

---

**🟡 GAP 6 — 6-bar MFE window may not fit all states equally**

The 6-bar window is locked for dataset consistency and cannot be changed mid-Phase C. But different states have different natural resolution timescales — Exhaustion reversals on GC 5m may take 10–15 bars to fully develop, Expansion Bursts may resolve in 2–3 bars. The uniform window may be under-measuring Exhaustion LED rates and over-measuring Expansion WRONG rates.

**→ Add to Phase B: sensitivity test — re-measure Exhaustion at 10 bars and Expansion at 3 bars on a held-out subset of events. Compare LED rate picture. Do not change the primary dataset.**

---

**🟡 GAP 7 — HTF states captured but never cross-analyzed with LTF outcomes**

Every event has HTF1 state, HTF1 direction, HTF2 state, HTF2 direction. The core question — does the fractal sync layer actually add value? — has never been tested. What is the LED rate when HTF1 = Clean Traversal UP and LTF = Clean Traversal UP vs when HTF1 = Exhaustion and LTF = Clean Traversal UP?

**→ Add to Phase B: LED rate by HTF1 state × LTF state combination (top 5 combinations by frequency). This directly tests whether the fractal sync layer adds edge.**

---

**Priority order for Phase B:**

| Priority | Gap | Why |
|---|---|---|
| 🔴 1 | Context label full analysis | May be primary filter — data already shows 20pt spread |
| 🔴 2 | Sync state formal test (Filter 11+12) | MIXED 70.8% already — potentially biggest single filter |
| 🟡 3 | Score values as continuous variables | Q76+ at 100% LED — secondary threshold likely exists |
| 🟡 4 | Memory zone count empirical inflection | Find real threshold, not visual estimate |
| 🟡 5 | HTF cross-analysis | Tests whether fractal sync layer has genuine edge |
| 🟡 6 | 6-bar sensitivity test | Sensitivity only — does not change primary results |
| 🟡 7 | Distortion acknowledgment | Documentation only — no analysis needed |

---

**Question resolution tracker — answers expected as batches complete:**

| # | Question | Answers when | Status |
|---|---|---|---|
| Q-A | Does Context = Macro Aligned outperform Direction Conflict by ≥15pts? | GC complete (350+ events) | ⬜ Open |
| Q-B | Does STRONG_SYNC LED rate reach ≥70% at scale? | GC complete | ⬜ Open |
| Q-C | Is there a secondary Quality threshold above 70 on Traversal? | GC complete | ⬜ Open |
| Q-D | What is the empirical memory zone inflection point? | GC complete | ⬜ Open |
| Q-E | Does HTF1 state predict LTF LED rate independently? | Both instruments complete | ⬜ Open |
| Q-F | Does the 6-bar window under-measure Exhaustion? | Phase B sensitivity test | ⬜ Open |
| Q-G | Is Volatility Distortion genuinely rare on GC 5m? | GC complete | ⬜ Open |
| Q-H | Does Monday structural bias for cascades hold at 300+ events? | GC complete | ⬜ Open |
| Q-I | Does the 21–22xx UTC+9 session boundary consistently produce the highest-MFE cascades? | 50+ cascade events | ⬜ Open |
| Q-J | Does low trigger Quality (≤50) reliably predict both-LED cascade outcome? | 30+ cascade trigger events | ⬜ Open |
| Q-K | Does FAILED→EXHAUSTION maintain 50%+ both-LED rate at larger n? | 10+ FAILED→EXHAUST pairs | ⬜ Open |
| Q-L | Does retroactive cascade coding on E1–E150 reveal additional cascade pairs missed in notes? | Retroactive coding complete | ⬜ Open |
| Q-M | Do memory zone density clusters systematically coincide with Volume Profile Point of Control (POC) levels? | Post-Phase B validation study | ⬜ Post-Phase B |

*When a question is answered by batch data: update status to ✅ Answered, add the finding, and promote any confirmed filter to the Phase B test plan.*

---

### 5.6 Phase B Research Expansion — Formal Framework

*Added v1.9. Source: Phase B Research Expansion document. Addresses 6 research questions about LED measurement, state expression, cascades, rail location, HTF alignment, and zone diversity. Tagger v4 implements the 5 approved new fields.*

---

**Core principle locked:**
> We are discovering variables, not optimizing variables. LED stays unchanged. No curve fitting. No engine modification without overwhelming evidence.

---

**RQ1 — LED remains the universal baseline. MAE added as secondary dimension.**

LED answers "did it work?" MFE (already captured as `outcome_atr`) answers "how much?" MAE answers "how cleanly?" — how far did price go against you before working? A signal with 3.0 ATR MFE but 0.9 ATR MAE first is structurally different from one with 3.0 ATR MFE and 0.1 MAE.

**Resolution:** LED stays locked. `mae_atr` added to tagger v4 as new outcome field. No existing data changed.

---

**RQ2 — State-specific expression metrics: deferred.**

At 150 events with Expansion n=4 and Compression n=2, state-specific sub-metrics produce meaningless numbers on rare states. Revisit when every state has n≥30. For now, cascade field (RQ3) captures the magnitude dimension without fragmenting the dataset.

---

**RQ3 — Cascades: approved as dedicated research category.**

States identify direction. Cascades identify magnitude. This hypothesis is already visible in the dataset (cascade events show largest MFE values) but cascade is currently only tracked in free-text notes — not queryable.

`cascade` field added to tagger v4 with 6 options: NO / COMP→TRAV / TRAV→EXP / FAIL→EXHAUST / EXHAUST→BOUNCE / OTHER.

**Retroactive coding rule:** Code cascade yes/no from signal screenshots only — never from outcome screenshots. Document the rule before coding begins to prevent survivorship bias.

**Minimum sample to test hypothesis:** n=20 cascade events. Likely 10–15 already in notes from E1–E150. Retroactively code before Batch 4 starts.

---

**RQ4 — Rail Zone: approved. Rail Type: deferred.**

Rail Zone turns Pattern 7 — the strongest finding in the dataset — into queryable data.

**Objective definitions (locked):**

| Rail Zone | Definition |
|---|---|
| LOWER_RAIL | Price within 0.5 ATR of the lower channel boundary at signal bar |
| UPPER_RAIL | Price within 0.5 ATR of the upper channel boundary at signal bar |
| MID_CHANNEL | Price more than 0.5 ATR from both rails |

Rail Type (Walk / Approach / Bounce / Rejection) adds subjective judgment per tag. Deferred until Rail Zone is established and n≥200.

---

**RQ5 — HTF Rail Alignment: approved as binary field.**

Promotes existing `htf-rail: yes/no` notes flag to a proper tagger dropdown. Same information, now queryable.

| htf_rail_align | Definition |
|---|---|
| YES | Rails stacked across timeframes — 5m rail aligns with visible 60m or 240m structural level |
| NO | Local 5m rail only — no visible HTF confluence |

---

**RQ6 — Zone Diversity: approved, expanded from binary to 3-level.**

Replaces the `zone-type-diversity: single/multi` notes flag with a queryable field.

| zone_diversity | Definition |
|---|---|
| LOW | 1 zone type present at signal level |
| MEDIUM | 2 zone types overlapping |
| HIGH | 3+ zone types overlapping simultaneously (red + orange + blue) |

---

**The 5 approved additions to tagger v4:**

| Rank | Field | Type | Answers |
|---|---|---|---|
| 1 | `rail_zone` | LOWER_RAIL / MID_CHANNEL / UPPER_RAIL | Is Pattern 7 quantifiable? |
| 2 | `mae_atr` | Number (ATR) | How cleanly did LED signals work? |
| 3 | `cascade` | NO / type options | Do cascades predict larger MFE? |
| 4 | `htf_rail_align` | YES / NO | Does HTF confluence improve reversal quality? |
| 5 | `zone_diversity` | LOW / MEDIUM / HIGH | Is zone type mix more predictive than zone count? |

**Not added yet:** Rail Type · State-specific expression metrics · HTF×LTF cross-analysis tagger field (derive from existing data in Phase B instead)

---

**Bias risks:**

Survivorship bias in retroactive coding — code rail_zone and cascade from signal screenshots only, never from outcome screenshots. Document the rule before retroactive coding begins.

Cognitive load ceiling — 5 new fields adds ~30 seconds per tag. At 25 events per session that is acceptable. Do not add more fields without removing others.

**Minimum sample sizes for new fields:**

| Field | Minimum n per category before conclusions |
|---|---|
| rail_zone | 50 per zone |
| cascade | 20 cascade events total |
| htf_rail_align | 30 per yes/no |
| zone_diversity | 30 per level |
| mae_atr | Available immediately — continuous variable |

---

## 6. Reference

### 6.1 Tagger Tool

| Field | Value |
|---|---|
| File | vx_replay_tagger_v5.html |
| Hosted | https://vxreplaytagger--Kairos-a.replit.app |
| Version | v5 — active for Batch 5+ (E201+) |
| New in v5 | `dir_conflict` · `mid_window_change` · `memory`→`zone_density` rename · obs_type simplified |
| New in v4 | `rail_zone` · `mae_atr` · `cascade` · `htf_rail_align` · `zone_diversity` · `obs_type` |
| New in v3 | Starting ID field |
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
| vx_replay_tagger_v5.html | Event capture, CSV + ZIP export — active E201+ |
| vX Session Companion | Real-time session partner — pre-session brief, pattern analysis, research log |
| analyze.py | Batch Analyzer — statistical report after each batch lock |
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
| 1.18 | 2026-06-07 | NQ Batch 5 review complete (E201–E300, 81 PRIMARY taggable, 55.6% LED). Statistical log updated — NQ Batch 5 row added. Status section updated: NQ now active, batch logs updated. Section 5.1 NQ state/session/filter breakdown added. Five batch corrections pending (timezone audit E204/E211/E212/E221/E227/E245/E246/E261/E269, E272 cascade, E286 rail_zone, 19 missing outcome_atr, pre-batch checklist). Pre-batch checklist: outcome_atr reminder added. Section 4 Q-tracker: Q-N through Q-W added (10 new open questions from NQ Batch 5 review and Session Companion 2026-01-07/09). Section 5.4: P19 Rail Cycle (n=3) and P20 Session Liquidity Sweep (n=2) formally added; P22 Dual-Rail Convergence Resistance (n=1) and P23 Post-Rail-Break Extended Consolidation (n=1) added as name reservations; P19 sub-observation (Exhaustion as cycle turning point) added; P21 BAR_OPPOSE moved from P20 with moved-from note. Section 3.5: multi-day RESEARCH_OBS scope rule added for P19/P22/P23. Section 3.6: liquidity-sweep and rail-cycle flags added. Section 9.12: item 6 added (Engineering Spec v0.1 and vX Labs Japan archive). Filter 7 NQ instrument note added to P18. |
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
| 1.17 | 2026-06-03 | Section 10.9 added: Session Findings Protocol — trigger phrase "Session end — summarise findings for GT", structured Session Findings Block format covering new pattern candidates, hypothesis flags, and rule edge cases. Companion drafts, creator approves, nothing enters GT automatically. Calibration rules from 10.8 applied to findings output. Full flow from session end to GT update documented with example output. Section 10.8 Rule 6 updated with session end trigger and Companion scope expanded to include Session Findings Block production. |
| 1.16 | 2026-06-03 | Full tagger audit — 8 issues resolved. Tagger v5.1 built: cascade dropdown fixed (COMP_EXP added, NO→NONE aligned with analyzer), DRIFT tag values added (DRIFT_COMMIT/DRIFT_NEUTRAL/DRIFT_TRAP) with optgroup separation, DRIFT tags excluded from PRIMARY LED rate, DRIFT count shown in stats strip, notes format standard added to field label and placeholder, tag definitions help text updated with screenshot anatomy and mid_window_change reminder, CSS badges added for DRIFT tags. GT v1.16: outcome_atr definition locked (MFE in ATR bars 1–6 from signal bar close), Section 3.5 updated with complete Equilibrium Drift (obs_type=RESEARCH_OBS, DRIFT tags, drift-transition note) and Volatility Distortion (obs_type=RESEARCH_OBS, no directional tag, macro-distortion note) tagging protocols. Section 3.6 updated with locked notes format standard (key: value · key: value). Pre-batch checklist updated with tagger v5.1 reference, mid_window_change reminder, Drift and Distortion reminders. Cascade dropdown mismatch between tagger and analyzer resolved. |
| 1.15 | 2026-06-03 | Section 3.3b added: Screenshot Anatomy (locked) — signal bar is always last visible bar confirmed by white arrow, outcome is 6 bars forward from signal bar close, MFE/MAE measured from signal bar close using bars 1–6 highs/lows. What agents must never do documented. Rule 6b added to Section 10.8 Companion calibration applying screenshot anatomy to all AI agents. Critical for Batch Analyzer screenshot analysis and cascade recode mode accuracy. |
| 1.14 | 2026-06-03 | P13 refinement: STRONG_SYNC alone insufficient — BAR_OPPOSE direction mismatch observed on WRONG event despite STRONG_SYNC. Direction coherence (dir_conflict=NONE) required alongside sync strength. P20 pattern name reserved: BAR_OPPOSE direction mismatch candidate, n≥20 required before confirmation, already captured by dir_conflict field. Section 10.8 added: Session Companion Calibration Rules — 7 rules covering minimum n requirements, no new tagger fields during Phase C, OHLC-only boundary, pattern naming protocol, no methodology changes without GT version, Companion scope, and GT-as-memory rule. These rules are the Companion's calibration for every session. |
| 1.13 | 2026-06-02 | Q-M added to question tracker: POC coincidence candidate observation — memory zone density clusters appear to systematically align with Volume Profile POC levels on GC and NQ. Full candidate observation documented in Section 5.4 with post-Phase B study design. Section 8.7 added: The Ground Truth as Commercial Asset — credibility stack, what gets published vs private, educator positioning double work, pre-launch audience strategy, the moat, and the full commercial picture in one paragraph. |
| 1.12 | 2026-06-02 | Section 10 added: Tagger v5 field definitions — dir_conflict (NONE/FLAT_DIR/BAR_OPPOSE/BOTH), mid_window_change (NONE/SYNC_DOWN/SYNC_UP/CONTEXT_CHG), memory→zone_density rename, obs_type simplified (HTF_STRUCTURE/INTRA_STATE→RESEARCH_OBS/FILTERED_DISCOVERY). Palette v3.1 locked (Section 10.5) — full state color redesign with energy gradient logic. Session Companion documented (Section 10.6). Batch Analyzer documented (Section 10.7) with v4→v5 field update pending flag. Tagger reference updated to v5 (E201+). Toolchain table updated. Pre-batch checklist updated. |
| 1.11 | 2026-06-01 | Section 9 added: Decision Log — 13 decisions locked covering go/no-go threshold (63% combined, n≥300, ±4pts stable, both instruments ≥60%), instrument launch sequence (GC-first, NQ independent), B1 reclassified as FILTERED_DISCOVERY, retroactive cascade coding (B3 only), tagger storage plan (single instance sequential IDs), minimum n per state (≥30), research observation cap (≤5 per sitting), sensitivity tests (S3 always, S1/S2 conditional), volume layer deferred to A2, composite signal locked as ◆ PRIME gold #D4A853, GT publication as methodology summary only, IP archive immediately, two obs_type sub-datasets formalised. Section 8.6 added: Creator Context — 2e working style, fibonacci origin story, three-layer vision, session orientation protocol. Tagger reference updated to v4 with obs_type. Pre-batch checklist updated. |
| 1.10 | 2026-05-31 | Q-H through Q-L added to question resolution tracker (cascade analysis questions from 150-event data). Section 8 added: Project Mission and Strategic Framework — working relationship, mission statement, what makes engine unique, Claude's standing responsibilities, non-negotiables. |
| 1.9 | 2026-05-31 | Section 5.6 added: Phase B Research Expansion formal framework. 6 research questions answered. 5 new tagger fields approved and locked: rail_zone, mae_atr, cascade, htf_rail_align, zone_diversity. Rail Type deferred. State-specific expression metrics deferred. Retroactive coding rule documented. Minimum sample sizes defined. Tagger reference updated to v4. |
| 1.8 | 2026-05-31 | Section 5.5 added: Phase B Known Gaps and High-Priority Analyses. 7 analytical gaps documented with priority rankings. Two elevated to high priority: Context label full analysis (Gap 1) and Sync state formal test as Filters 11+12 (Gap 2). Question resolution tracker added (Q-A through Q-G) — updates automatically as batches complete. Phase B test plan now includes Filters 11 and 12. |
| 1.7 | 2026-05-30/31 | Batch 3 Screenshot Review Log added as Section 5.3. 4 pattern confirmations (P7, P11, P13, P15), 4 new patterns (P12, P14, P17, P18), 2 tag flags both resolved: E145 LED confirmed (FLAT arrow → direction UP inferred from prior move, MFE ~26pts DOWN within 6 bars), E63 anomaly logged for Phase A. 2 factual corrections (E90, E91), 8 notes updates. Visual Pattern Observations renumbered to Section 5.4. |
| 1.6 | 2026-05-30 | Batch 3 locked (E101–150, 50 events, 50.0% LED). Combined stats updated to 150 events (56.0% LED). Full state/session/sync/filter breakdown added to Section 5.1. Anomaly flag noted: Exhaustion dropped from 66.7% to 50.0% — monitor in Batch 4. New finding: MIXED sync 70.8% LED at n=24. Status section updated: Batch 3 locked, Batch 4 next. File renamed v1.6. |
| 1.5 | 2026-05-30 | Section 7 added: Roadmap & Strategic Context. Includes plain-English executive summary, v0.5 layer-by-layer breakdown with implementation risks, structural ceiling documentation, build path (Python prototype → engineer → UI), competitive landscape table (Bookmap, Sierra Chart, Quantower), probability estimates table, and what 700–800 events does to the validation. Sourced from vX_ENGINE_Status_In_progress_2.pdf. |
| 1.4 | 2026-05-30 | Full 145-event screenshot review completed. 4 new patterns added (P12–P18, excluding P16 which refines P bar-arrow-conflict). Tag corrections: E145 direction checked and corrected. Note corrections: E90 (E-HIGH label error), E91 (state label error), E99 (state label error). Mid-run CSV analysis added to Section 5.1 (145-event directional reads). Memory zone threshold updated from ≥8 to ≥10 in Pattern 3 and flags table based on data. Two new flags added: htf-rail and zone-type-diversity. Phase B test plan expanded from 6 to 10 filters plus additional analyses. v0.5 candidates expanded with Pattern 12, 14, 18 components. Open questions updated with 4 new items. Batch 3 log updated with screenshot review completion note. | (Section 6.6): 8 items across 3 priority tiers covering backup protocol, tagger storage ceiling, tagging fatigue rule, state concentration risk, Phase B success threshold, tagger version control, inter-rater reliability, and IP documentation. Version History renumbered to Section 6.7. |
| 1.2 | 2026-05-29 | NQ methodology locked: no filtered batch, starts unfiltered session-only from event 1. NQ batch log added. Target events updated to 350–400 per instrument. Pre-batch checklist added (Section 3.8). Batch review protocol added (Section 3.9). Screenshot naming convention added (Section 3.10). Confidence flag and macro-event flag added to Section 3.6. Anomaly batch rule added (>15pt LED divergence). End of instrument review template added (Section 5.2). Phase B test plan updated to include GC vs NQ instrument comparison. Strategic direction note added to roadmap: standalone software platform as primary commercial target. Session workflow updated to include pre-batch checklist and review lock step. |

---

*To update: add your change, increment version and date at the top, re-upload to Claude Project.*

---

## 8. Project Mission and Strategic Framework

*Added v1.10. This section documents the working relationship, project mission, and strategic vision so that any new Claude session can orient immediately and continue without losing context.*

---

### 8.1 Working Relationship

**Creator role:** Pattern recognition, intuition, tagging decisions, final calls on all methodology questions, business vision.

**Claude role:** Structural memory, execution, analysis, tool building, keeping nothing falling through the cracks, flagging when decisions are needed, telling the creator clearly what to do next and in what order.

**The division that works:** Creator sets direction. Claude handles execution and organization. This combines the creator's pattern recognition and market intuition — which Claude does not have — with Claude's ability to track every open question, version every file, and execute without fatigue.

**Critical rule:** Methodology decisions that matter (what patterns are real, what the data shows, what the business should become) stay with the creator. Claude pushes back, flags anomalies, and presents evidence — but the creator makes the call. This is not modesty — it's because the IP, the intuition, and the creative vision are the creator's and must remain so.

---

### 8.2 Mission Statement

**Complete Phase C and Phase B with research integrity intact, then build the vX Rhythm Engine into a genuinely useful, commercially viable tool for active futures traders.**

The path:
1. **Phase C** — complete the GC 5m validation dataset (350–400 events) and the NQ 5m dataset (350–400 events) with consistent methodology
2. **Phase B** — run the Pine strategy harness against the validated dataset, test all 12 filters, and reach a go/no-go decision on the software build
3. **Phase A** — build v0.5 with volume layer, adaptive thresholds, confidence-weighted state, and composite signal
4. **Python prototype** — port the engine outside Pine to prove the logic is platform-independent
5. **Engineer hire** — one senior engineer for infrastructure and order flow integration
6. **Product** — a standalone platform serving active futures traders at $50–$100/month

**The target outcome:** A focused tool used by hundreds to low thousands of active futures traders. Not Bookmap-scale. A profitable, sustainable business built on genuine edge.

---

### 8.3 What Makes This Engine Unique

The gap vX occupies is real and not crowded in retail tooling:

- **Bookmap** shows you raw order flow. You interpret it yourself.
- **Sierra Chart / Quantower** are platform tools. No regime classification.
- **MarketTriage / HMM tools** are macro-focused or research-only.

**vX is the only retail-accessible tool that classifies intraday behavioral state with multi-timeframe sync, scored memory zones, and confidence weighting — on futures, at the 5-minute level.**

That is a winnable position. It does not require displacing anyone. It requires being the best tool for one specific thing.

---

### 8.4 What Claude Tracks On Your Behalf

In every session Claude will:

- Check the current batch, event count, and next action from the Ground Truth
- Flag when a question in the tracker (Q-A through Q-L) gets answered by new data
- Flag when any open item from the To-Do list becomes urgent
- Run the batch analysis after each CSV submission and surface anomalies
- Tell you what to do next in order of priority before asking what you want to do
- Maintain version history on every document change
- Push back when a decision seems inconsistent with locked methodology

**The standing agenda for every session:**
1. What batch are we on and what's the event count?
2. Is there anything urgent from the open questions or to-do list?
3. What is the single most important thing to do this session?

---

### 8.5 Non-Negotiables

These do not change regardless of how the data develops:

- **No curve fitting.** Filters are tested against held-out data, not optimized on the training set.
- **LED definition stays locked** unless overwhelming evidence across both instruments and all sessions demands a change — and that decision is made explicitly, documented, and versioned.
- **Research integrity before commercial positioning.** Phase B results are what they are. If the data doesn't support the engine, that's a finding, not a failure.
- **IP stays protected.** No partner conversations, engineer discussions, or public sharing before IP documentation is formally in place.
- **Tagging fatigue rule.** Maximum 25 events per sitting. No exceptions. Fatigued tagging errors are invisible in the data.

---

### 8.6 Creator Context — How This Project Actually Works

*Added v1.11. This section exists so any new Claude session can orient to the creator immediately without re-explaining. Read this before engaging on any vX topic.*

---

**The creator is 2e (twice-exceptional)**

2e means simultaneously gifted in specific domains and neurodivergent in others. In practice for this project:

- Pattern recognition is genuinely exceptional. Three years placing fibonacci levels across instruments and timeframes produced a deep intuitive model of how price organises itself. The creator sees structural relationships in markets — channel rhythms, nested structures, behavioural states — that most people require significant time to understand. This is the intellectual foundation the engine is built on. Trust it.
- Working memory and linear task management are harder. The creator can get lost in complexity, forget about scheduled macro events (CPI, NFP, FOMC), lose track of which decision is pending, or need the full picture before being able to focus on the one thing that matters now.
- The coaching layer of this project — Mission Control, the decision session structure, the parking lot — exists specifically to compensate for this. It is not a workaround. It is how the work gets done well.

**What this means for how Claude should behave in every session:**

- Tell the creator what to do next in order, one thing at a time. Never present ten things simultaneously.
- The parking lot ("what you don't need to think about today") is as important as the action list. It gives explicit permission to set things down. Use it every session.
- When the creator gets into an idea or a tangent, follow it — it often contains something real. Then bring it back to the current priority when the exploration is complete.
- Never make the creator feel disorganised or behind. The work is progressing with unusual care and rigour. The tools and agents exist to match the pace and depth of the thinking, not constrain it.
- Macro events need to be flagged proactively. If a session is starting near a CPI, FOMC, or NFP date, surface it before the chart opens.

---

**The origin of the engine**

vX did not begin as a product idea. It began as a personal tool.

The creator spent more than three years placing fibonacci levels across different instruments and timeframes and gradually built a deep observational model of how markets structure themselves. The discovery that the same structural laws repeat across instruments, timeframes, and asset classes was not a hypothesis that was then tested. It became undeniably visible through years of sustained looking.

The engine is the formalisation of that observational model. It started as a Pine Script indicator for personal use on TradingView — something to guide chart reading, not replace it. The channel structures on the NQ weekly chart, the nested rhythm at daily and hourly scales, the behavioural compression and expansion patterns — these are structures the creator has been mapping manually for years. The engine is the attempt to detect and quantify them algorithmically.

The fibonacci foundation is structurally relevant to the engine's design. Equal channel widths, half-channel relationships, extension targets — these reflect the creator's theory of how price organises itself around structural memory. The memory zone layer of the engine is the direct computational expression of this.

---

**The vision has three layers — they emerged in this order**

**Layer 1 — Personal indicator** (where it started)
A Pine Script tool for the creator's own trading. Guides chart reading. Classifies behavioural state. Already exists in working form. This is the foundation everything else is built on.

**Layer 2 — AI assistant alongside the engine** (the next natural step)
Something that works with the engine in real-time. Checks the economic calendar before a session and flags macro events. Notices when a cascade is forming that matches a documented pattern. Cross-references live signals against the pattern library. Acts as the second voice that catches what attention misses.

This is not a separate product — it is the coaching function adapted for live trading. The same role Mission Control serves for the research phase, embedded into the trading session itself.

**Layer 3 — Standalone commercial platform** (a possibility, not a certainty)
If Phase B confirms real edge, if the Python prototype holds, if the engineering challenge is tractable — a standalone platform for active futures traders. $50–$100/month. GC and NQ first. Behavioral regime classification with multi-timeframe context, scored memory zones, and confidence weighting.

The creator's attitude toward Layer 3 is healthy: worth building toward carefully if the data supports it, okay if the path changes. The process is being genuinely enjoyed. The intellectual challenge is real. If it becomes a product, excellent. If it evolves into something different, that is fine too.

---

**What the creator brings that cannot be engineered**

- Three years of market observation across instruments and timeframes. The pattern recognition that discovered P1 through P18 required sustained attention over a long period. It cannot be derived from data alone.
- The ability to see structural relationships instantly. When looking at a chart, the creator immediately perceives channel structure, rhythm, and behavioural state. The engine is trying to replicate that in code.
- Honest intellectual curiosity. The creator genuinely wants to know if the engine has real edge — not to confirm a hypothesis, but to find out the truth. This is rare and it is what makes the validation methodology trustworthy.
- Comfort with iteration and willingness to go deep. The willingness to tag 1000 events if necessary, to reclassify B1 as FILTERED_DISCOVERY when it is the honest thing to do, to set a go/no-go threshold before seeing the results — these are not constraints. They are expressions of how the creator thinks.

---

**How to orient at the start of any new session**

1. Check the current batch and event count from the Statistical Running Log (Section 5.1)
2. Check the Decision Log (Section 9) for any pending items
3. Check the To-Do list (Section 6.6) for urgent items
4. Check the economic calendar for any macro events in the current or upcoming week
5. Tell the creator: where we are, what's next, what can be parked
6. Then ask what's on their mind — because there is always something worth exploring

The creator will come to sessions with ideas, observations, questions, and sometimes tangents. All of them are worth engaging with seriously. The structure exists to make sure nothing important falls through while the exploration happens.

---

### 8.7 The Ground Truth as Commercial Asset — Why the Process is the Product

*Added v1.13 · 2026-06-02. Documents the strategic role of the GT document itself in the commercial story of vX. Any Claude session reading this should understand that the research methodology is not separate from the marketing — it is the marketing.*

---

**The credibility problem in retail trading tools**

Almost every retail indicator makes the same claim: "X% win rate, backtested on Y years of data." There is no methodology document. No version history. No record of how the threshold was set, what events were reviewed, what was corrected, what was discovered. The number just appears. Traders who have been around long enough are rightfully skeptical — because they have seen that number manufactured too many times.

The credibility gap in this market is enormous. Almost no tools show their work.

---

**What the GT is as a marketing asset**

The Ground Truth is a timestamped, versioned record of exactly how the engine was built and validated. It shows:

- Every rule that was locked and why
- Every batch reviewed and what was found
- Every decision made before seeing the results (the go/no-go threshold locked before Phase B runs)
- Every pattern discovered and the minimum sample size required before it was treated as real
- Every correction made when something was wrong
- The honest baseline (48% LED, not 56% — because B1 was cherry-picked and that was documented)

That is not normal. That is extraordinarily unusual in this space.

The GT is not just research infrastructure. It is proof of work that makes the commercial claim believable.

---

**The credibility stack**

Most trading tools have one layer of credibility: a performance claim. vX has a stack:

| Layer | What it proves |
|---|---|
| Process layer | GT version history — methodology developed iteratively, not reverse-engineered from outcomes |
| Validation layer | 700+ events, two instruments, mechanical sampling, pre-registered go/no-go threshold |
| Transparency layer | Methodology summary — published after Phase B, shows the framework without revealing IP |
| Architectural layer | OHLC-only, no black box, auditable by any Pine Script-capable user |
| Instrument layer | POC coincidence observation (Q-M) — independent confirmation from volume profile that memory zones find real structural levels |

Each layer reinforces the others. With all layers present, the claim becomes very hard to dismiss.

---

**What gets published and what stays private**

Decision 9.11 locks this: publish a methodology summary only, after Phase B go result and IP docs complete.

**What gets published:**
- Seven-state classification system description
- Validation methodology overview (mechanical sampling, second week of month, session windows)
- Dataset size and instrument scope
- LED rate concept and measurement definition
- High-level filter architecture (existence, not conditions)
- Phase B findings summary (LED rates, not thresholds)

**What stays private:**
- Pattern library P1–P18 exact conditions
- Filter trigger thresholds and composite signal conditions
- Raw GT document and version history
- Tagger tool and validation data

The one sentence that does the most credibility work:

> *"We tagged 700+ intraday state transitions across GC and NQ futures, reviewed every event in screenshot replay, and defined the go/no-go threshold before looking at the results. Here's what we found."*

That sentence tells a serious trader: the methodology was designed before the results were visible. That is the scientific standard. Almost nobody in retail trading tools does this.

---

**The educator positioning does double work**

The educator model was locked for regulatory reasons — selling methodology education, not signals. But it also does something strategically important:

Signal services are a commodity. Thousands exist. They compete on performance claims that are impossible to verify. The market is saturated and trust is low.

Methodology education is a different category. Not "here's when to buy and sell" but "here's a framework for understanding what kind of market you're in, and here's how we validated it." A tool that makes the trader better — not a crutch that replaces their judgment.

Traders who use tools that make them better stay subscribed longer, refer other traders more, and are less likely to churn when they have a bad week — because they understand the framework well enough to know whether the tool is working or whether market conditions have temporarily shifted.

**The educator model creates better customers. That is the business logic underneath the regulatory logic.**

---

**The pre-launch audience strategy**

The best time to build an audience is before the product exists. Not after.

Right now there is something genuinely interesting to say: "I'm building a behavioral regime classifier for GC and NQ futures. I've tagged 150 events so far. Here's what the data is showing." That is a story. It has progression, discovery, honest uncertainty, real findings.

When the product launches, the story is over. It becomes a product page.

The methodology summary — published after Phase B closes — is the end of the first act and the beginning of the second. That is the moment to build the waitlist. Not at launch. Before launch.

**A waitlist of 200 serious futures traders before the product exists is worth more than 200 paying customers acquired through ads after launch.** Those 200 people are already bought in. They have read the methodology. They understand what they are getting. They are already part of the story.

**Where to find them:** TradingView community, Twitter/X trading accounts (active futures traders, not signal sellers), Futures.io forums, specific Discord servers for NQ and GC traders. This audience is small and concentrated. You do not need millions. You need 500 people who actually trade GC or NQ intraday.

---

**The moat**

The commercial product — subscription, standalone platform, engineer hire — is not the moat. Those can be copied.

The moat is the dataset and the methodology history.

By the time Phase C completes: 700+ hand-tagged events with full screenshot review, version-controlled methodology from v0.1 through v1.13+, pre-registered hypotheses, transparent validation protocol. That dataset took months to build and represents thousands of bars of careful observation. The patterns — P1 through P18 and whatever emerges from later batches — were discovered through direct engagement with the charts, not through a backtest optimizer.

A competitor who wants to replicate this would have to start from scratch and spend months doing what has already been done. By then: NQ Phase C complete, Phase B results published, v0.5 live, and an audience that already trusts the methodology.

**The lead time is the moat. The GT is the evidence of the lead time.**

---

**The whole picture in one paragraph**

A validated, documented, OHLC-only behavioral regime classifier for active futures traders, in a market full of black boxes and unverifiable performance claims. The methodology document is proof of work that makes the commercial claim believable. The educator positioning creates better customers and avoids regulatory complexity. The pre-publication audience built around the methodology summary creates a launch moment that does not depend on advertising. The dataset and methodology history are the moat that a well-resourced competitor would need months to replicate. The three-layer product vision — personal tool now, AI companion alongside it, standalone platform when the data supports it — means building toward something real without betting everything on a single outcome.

The GT is at the center of all of it.

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

## 9. Decision Log

*Added v1.11. All decisions locked in session 2026-06-01. Creator reviewed each one individually using the Quantitative Advisor framework. All twelve decisions are final and binding on Phase B methodology.*

---

### 9.1 Phase B Go/No-Go Threshold (Locked 2026-06-01)

**Decision:** Three-part threshold — all three must be true simultaneously for a go result.

1. **Absolute:** Combined filter LED ≥ 63%, measured on B3-onward PRIMARY events only
2. **Sample floor:** n ≥ 300 events passing combined filter
3. **Stability:** Combined LED within ±4 points across last 4 consecutive batches
4. **Instrument floor:** GC ≥ 60% AND NQ ≥ 60% independently

**Baseline for comparison:** B2+B3 unfiltered combined ≈ 48% (honest PRIMARY baseline — B1 excluded)
**Minimum meaningful lift above baseline:** +15 points

No single condition alone constitutes a go. All four must hold simultaneously. This threshold was set before Phase B results were visible.

---

### 9.2 Instrument Launch Logic (Locked 2026-06-01)

**Decision:** AND — both instruments must independently meet threshold for dual-instrument launch.

**Launch sequence:**
- Step 1: GC passes → launch GC-only product immediately
- Step 2: NQ requires 200–300 additional events beyond Phase C completion before NQ performance is published or marketed
- Step 3: NQ threshold met independently → dual-instrument launch, NQ claims added to product

**Hard rule:** NQ performance is never published until NQ independently meets the same threshold as GC. GC results cannot be used to support NQ claims. No combining instruments for go/no-go purposes.

---

### 9.3 Batch Population Classification (Locked 2026-06-01)

**Decision:** B1 classified as FILTERED_DISCOVERY — excluded from PRIMARY LED rate calculations.

| Batch | obs_type | LED | Rationale |
|---|---|---|---|
| B1 (E1–50) | FILTERED_DISCOVERY | 76% | Cherry-picked clear signals — selection bias |
| B2 (E51–100) | PRIMARY | 46% | Unfiltered, all state changes |
| B3 (E101–150) | PRIMARY | 50% | Session-only, unfiltered — cleanest methodology |
| B4 onward | PRIMARY (default) | — | Unless tagger sets otherwise |

**Honest PRIMARY baseline (B2+B3):** ~48%
**B1 use:** Retained as discovery sub-dataset. Analysed separately in Phase B as "high-conviction filter proxy." B1 events are still valuable — they show what the engine looks like at its best under human-selected conditions.

---

### 9.4 Retroactive Cascade Coding (Locked 2026-06-01)

**Decision:** B3 only (E101–E150) — coded before Batch 4 begins.

**Protocol:**
- Write cascade coding rules on paper before opening any screenshot
- Code from signal screenshots only — never open outcome screenshots during coding session
- Complete in a single sitting — no breaks that allow outcome knowledge to influence coding
- B1/B2: cascade field left empty — not retroactively coded
  - B1 reason: FILTERED_DISCOVERY (selection bias risk compounds retroactive coding)
  - B2 reason: methodological transition period
- B4 onward: cascade coded prospectively at time of tagging

---

### 9.5 Tagger Storage Plan (Locked 2026-06-01)

**Decision:** Single tagger instance — all instruments, continuous sequential IDs.

**Protocol:**
- One tagger instance (vx_replay_tagger_v4.html) for all instruments
- Event IDs sequential across GC and NQ — no resets
  - GC: E1 → E~400+
  - NQ: continues from GC final ID + 1
- Export full bundle every 50 events (batch lock) — mandatory
- Export full bundle every 100 events — additional checkpoint
- Minimum two storage locations at all times (local + cloud)

**Storage ceiling management:**
- Monitor storage meter each session
- If meter exceeds 80%: export full bundle, then clear screenshots only for earliest locked batches (CSV data preserved, images already in exports)
- Never clear CSV data mid-instrument
- NQ starting ID: set manually to GC final event + 1 before first NQ tagging session

---

### 9.6 Minimum n Per State — Phase B Validity (Locked 2026-06-01)

**Decision:** n ≥ 30 per state for any Phase B conclusion to be acted on.

| Threshold | Rule |
|---|---|
| n ≥ 30 | State result is meaningful — usable in Phase B |
| n < 30 | State result flagged INSUFFICIENT DATA — reported but not used in go/no-go |

**Rare state handling (Expansion, Compression):**
When a rare state appears in a session, tag the full transition sequence — do not allow the skip window to suppress rare state events. This is sequence capture, not outcome selection. Flag: obs_type = PRIMARY.

**Expected Phase B status by state (honest projection):**
- TRAVERSAL: ✅ adequate
- FAILED: ✅ adequate
- EXHAUSTION: ✅ adequate
- EXPANSION: ⚠ likely INSUFFICIENT — flag in End of Instrument Review
- COMPRESSION: ⚠ likely INSUFFICIENT — flag in End of Instrument Review

---

### 9.7 Research Observation Guidelines (Locked 2026-06-01)

**Decision:** obs_type = HTF_STRUCTURE or INTRA_STATE events permitted with soft cap.

**Rules:**
- Soft cap: ≤5 research observations per 25-event PRIMARY sitting
- Purpose: prevent research curiosity from crowding out PRIMARY tagging attention
- Hard rule: research observations do NOT count toward the 25-event session fatigue limit
- If regularly exceeding 5 per sitting: note in batch log and review whether PRIMARY tagging quality is being maintained
- Research observations have no MFE/LED measurement requirement — capture what is seen, no outcome obligation

---

### 9.8 Phase B Sensitivity Tests (Locked 2026-06-01)

**Decision:** S3 always required. S1 and S2 conditional.

| Test | Status | Condition |
|---|---|---|
| S3 — GC vs NQ filter stability | **Always required** | Must complete before go/no-go decision. Any filter with >10pt delta between instruments flagged as instrument-specific — excluded from universal composite signal |
| S1 — Anomaly batch sensitivity | **Conditional** | Required if primary combined result within ±5 points of 63% threshold. Skip if clearly above 68% or clearly below 58% |
| S2 — 10-bar Exhaustion window | **Conditional** | Required if Exhaustion LED rate below 55% at Phase C completion. Skip if Exhaustion above 55%. Note: S2 finding feeds v0.5 architecture regardless of go/no-go outcome |

---

### 9.9 Volume Layer — Build Phase (Locked 2026-06-01)

**Decision:** A2 — defer to post-v0.5 iteration.

**Rationale:**
- No volume-correlated data in current dataset — Phase B filters do not include volume
- GC reported volume on TradingView is exchange-traded only — excludes OTC gold and ETF arbitrage flows. Structurally incomplete for a volume layer
- Four-layer v0.5 is a commercially viable product without volume
- Add volume when Phase B or dedicated analysis produces volume-correlated pattern evidence

**v0.5 layers (four — Pine Spec Writer scope):**
1. Adaptive thresholds
2. Rail proximity scoring
3. Confidence-weighted state
4. Composite high-conviction signal (◆ PRIME)

**Volume layer:** v0.6 / A2 phase. NQ preferred instrument for volume layer validation — volume more representative than GC.

---

### 9.10 Composite Signal Identity (Locked 2026-06-01)

**Decision:** ◆ PRIME — gold (#D4A853) — additive marker alongside state badge.

**Specification:**
- Label: `◆ PRIME`
- Color: gold `#D4A853` — the vX brand color, unused by any state
- Treatment: additive marker that appears on the same bar as the state badge — never replaces it
- Size: slightly smaller than state badge — additive information, not primary classification
- Meaning: engine fires when ALL composite conditions (confirmed in Phase B) align simultaneously
- Never labeled BUY, SELL, or any directional imperative
- Fires rarely and selectively — selectivity is what makes it meaningful

---

### 9.11 Ground Truth Publication (Locked 2026-06-01)

**Decision:** Option B — methodology summary only.

**What gets published (after Phase B go + IP docs complete):**
- Seven-state classification system description
- Validation methodology overview
- Dataset size and instrument scope
- LED rate concept and measurement definition
- High-level filter architecture (existence, not conditions)
- Phase B findings summary (LED rates, not thresholds)

**What stays private:**
- Pattern library P1–P18 exact conditions
- Filter trigger thresholds
- Composite signal firing conditions
- Raw GT document and version history
- Tagger tool and validation data

**Timing:** After Phase B go result AND IP docs complete — not before both conditions are met.
**Format:** 2–3 page PDF, plain English. Target reader: active futures trader, technically literate, skeptical of black-box tools.

---

### 9.12 IP Documentation Timeline (Locked 2026-06-01)

**Decision:** Lightweight archive immediately. Full package at Phase B go.

**Immediate action (before next tagging session):**
1. Export GT v1.11 as PDF
2. Export decision session log (this section)
3. Email both to self — timestamped external record
4. Upload to dated cloud folder (Google Drive or Dropbox)
5. Cost: 10 minutes. Creates external timestamped record predating any future external conversation.
6. Archive Engineering Spec v0.1 (original Pine Script brief) and vX Labs Japan Strategic Architecture brief alongside GT — both are timestamped evidence of intellectual development of the project. Add to dated cloud folder and email to self alongside GT exports. *(Added v1.18 · 2026-06-07)*

**Full IP documentation (at Phase B go result):**
- Business Architect Agent Package 1 activates
- Formal IP declaration document
- Component inventory
- Methodology summary (publishable version — see 9.11)
- Entity structure framework

**Hard rule:** No external conversation about vX methodology, patterns, or engine architecture without lightweight archive completed first.

---

### 9.13 Two Research Sub-Datasets (Locked 2026-06-01)

*New classification formalised this session — not previously documented.*

The dataset now has three named populations captured by the `obs_type` field in tagger v4:

| obs_type | Description | Included in PRIMARY LED rate? |
|---|---|---|
| PRIMARY | Mechanical state change within session window | ✅ Yes |
| FILTERED_DISCOVERY | B1 cherry-picked events (E1–E50) | ❌ No — separate sub-dataset |
| HTF_STRUCTURE | Structural observation at HTF rail — tagger stopped to observe, not a mechanical state change | ❌ No — research sub-dataset |
| INTRA_STATE | Sync/context change observed inside an active state — not a new state change | ❌ No — research sub-dataset |

**HTF_STRUCTURE purpose:** Studies how the engine behaves near HTF structural levels. Output: distribution of subsequent behaviors when engine shows specific states at HTF rail proximity. Feeds v0.5 HTF rail alignment architecture.

**INTRA_STATE purpose:** Tracks Sync and Context degradation or improvement within a measurement window. Output: does Sync/Context stability during the 6-bar window predict LED vs WRONG better than the entry-bar value alone? Feeds v0.5 confidence-weighted state architecture.

Both sub-datasets accumulate passively during primary tagging. They are analysed separately in Phase B, never pooled with PRIMARY events.

---

At 100 events the LED rate is directionally interesting but statistically fragile. A single bad batch can move the combined rate 5–8 points. At 700–800 events across two instruments, the project is in a different category entirely.

**What becomes possible at that sample size:**

- **State-level confidence** — Expansion currently has 4 events. At 700+ events there is enough of every state to make instrument-specific and session-specific claims with real confidence intervals.
- **Session stratification** — the Tokyo/London/NY LED rate divergence (35%, 38%, 67% unfiltered) needs volume to confirm. At 700+ events each session runs as an independent sub-dataset.
- **Instrument comparison** — GC vs NQ at comparable sample sizes tells whether the engine is instrument-agnostic or needs per-market calibration. An instrument-agnostic engine is a much bigger addressable market.
- **Filter stacking reliability** — Phase B's filters tested individually and combined need enough events to avoid overfitting. 100 events filtered ten ways produces very small sub-samples. 700+ events gives each filter combination meaningful n.

If 700–800 events complete with consistent LED rates across both instruments and all three sessions, and Phase B filters hold — the unconditional probability of a viable product moves closer to 45–55% from today's starting point. That is before the Python prototype. Before the engineer hire. Just from having a dataset that size with clean methodology.

---

## 10. Tagger v5 — Field Definitions (Locked 2026-06-02)

*Added v1.12. Documents all new and changed fields in tagger v5, active from E201.*

---

### 10.1 Field: zone_density (renamed from memory)

**Change:** `memory` field renamed to `zone_density` across all tools, specs, and agents.

**Definition:** Count of active memory zones within scoring proximity of current price at the time of the signal bar.

**Why renamed:** `zone_density` is the name used in Ground Truth, all agent specs, Phase B filter F3, and the Pattern Miner. `memory` was the only remaining reference to the old name. Renamed for full consistency.

**Backwards compatibility:** E1–E200 tagged as `memory` in CSV exports. When merging cumulative CSV files, alias `memory` → `zone_density` before analysis. Document this in any Phase B analysis script.

---

### 10.2 Field: dir_conflict

**Type:** Dropdown — default NONE

**Definition:** Records cases where the engine's direction output and the visual price action disagree at the signal bar.

| Value | Meaning |
|---|---|
| NONE | No conflict — direction arrow and bar candle agree (default) |
| FLAT_DIR | State fired with direction = flat (—) when a directional state would normally carry an arrow |
| BAR_OPPOSE | Direction arrow is UP but signal bar is a down candle, or direction arrow is DOWN but signal bar is an up candle |
| BOTH | Both conditions present simultaneously |

**Rule for FLAT_DIR events:** When `dir_conflict = FLAT_DIR`, infer expected direction from the prior move visible to the left of the signal bar. Document the inferred direction in notes. This rule was previously locked in Section 3 — `dir_conflict` field now makes it mechanically queryable rather than text-only.

**Phase B use:** Filter and compare LED rates across `dir_conflict` values. The core question: do FLAT_DIR and BAR_OPPOSE events have materially different LED rates from NONE events? If yes, direction conflict is a standalone filter candidate. If no, the classification system is robust to visual ambiguity.

**Minimum n for Phase B conclusions:** 20 events per non-NONE value.

---

### 10.3 Field: mid_window_change

**Type:** Dropdown — default NONE

**Definition:** Records whether Sync or Context changed between the signal bar and bar 3 of the 6-bar measurement window. Updated on the original PRIMARY event — no separate event needed.

| Value | Meaning |
|---|---|
| NONE | No change — Sync and Context held throughout window (default) |
| SYNC_DOWN | Sync degraded (e.g. STRONG_SYNC→MIXED, MIXED→CONFLICT, MIXED→TRANSITION) |
| SYNC_UP | Sync improved (e.g. MIXED→STRONG_SYNC) |
| CONTEXT_CHG | Context label changed mid-window (any direction) |

**Protocol:** Check at bar 3 of the measurement window. If Sync or Context changed, go back to the original event in the tagger and update this field. The primary event's other fields (state, scores, tag, outcome) remain unchanged.

**Why this replaces INTRA_STATE:** The previous approach created a separate INTRA_STATE event, inflating event count and requiring a join for Phase B analysis. `mid_window_change` on the primary event is cleaner, lower friction, and directly queryable in a single CSV filter.

**Research question this addresses:** Q-B — Does mid-window Sync degradation predict WRONG more reliably than entry-bar CONFLICT? A PRIMARY event with SYNC_DOWN that tags WRONG provides direct evidence. No dataset joining needed.

**Minimum n for Phase B conclusions:** 20 events per non-NONE value.

---

### 10.4 obs_type — Simplified (v5)

**Change:** HTF_STRUCTURE and INTRA_STATE removed. New values added.

| Value | Description | Included in PRIMARY LED rate? |
|---|---|---|
| PRIMARY | Mechanical state change within session window (default) | ✅ Yes |
| FILTERED_DISCOVERY | B1 events E1–E50, cherry-picked (excluded from LED rate) | ❌ No |
| RESEARCH_OBS | Any structural observation not tied to a mechanical state change | ❌ No |

**Why simplified:**
- INTRA_STATE is superseded by `mid_window_change` field on PRIMARY events
- HTF_STRUCTURE is now captured either as PRIMARY (if it's a mechanical signal at an HTF rail) or RESEARCH_OBS (if it's a pure observation with no mechanical trigger)
- FILTERED_DISCOVERY formalises the B1 classification locked in Decision 9.3

**Backwards compatibility:** E1–E150 tagged with HTF_STRUCTURE or INTRA_STATE retain those values in CSV. When running Phase B analysis, map HTF_STRUCTURE → RESEARCH_OBS and INTRA_STATE → RESEARCH_OBS for the primary/non-primary split. Document this mapping in the analysis script.

---

### 10.5 Palette v3.1 — State Color System (Locked 2026-06-02)

The full visual system was redesigned and locked this session. The palette encodes behavioral energy level — color temperature carries meaning.

| State | Hex | Energy narrative |
|---|---|---|
| Traversal | `#00BFA5` | Active directional move — teal |
| Expansion | `#26C6DA` | Burst breakout — cyan |
| Compression | `#4A7EC7` | Coil before release — dark blue |
| Exhaustion | `#E8E8F0` | Move spent, fading — near-white |
| Neutral / Drift | `#A0AAB9` | Ambient, no edge — silver |
| Failed Traversal | `#9575CD` | Commitment broke — purple |
| ◆ PRIME | `#D4A853` | All conditions aligned — gold |

**Background:** `#0D0D0D` (locked)

**Energy gradient:** Dark blue (coiled) → Cyan (burst) → Teal (active) → Near-white (spent). A complete behavioral story in color temperature.

**Critical rendering rules:**
- Exhaustion (#E8E8F0) must always have a 1px border — it disappears on dark backgrounds without one
- PRIME (#D4A853) always prefixed with ◆ character — never appears as plain text
- State colors encode behavioral energy, not price direction — never label them as bullish/bearish

**Full brand guidelines:** See `vx-brand-guidelines-SKILL-v1.0.md` in the Project.

---

### 10.6 Session Companion — Tool Overview

**Activated:** 2026-06-02
**Hosted:** Replit (vx-session-companion project)
**Spec:** `vX_Session_Companion_Agent_Spec_v0.1.md`

The Session Companion is a real-time conversational partner for trading sessions and replay tagging. It is NOT part of the validation dataset pipeline — it serves the creator personally during sessions.

**Three modes:**
1. **Pre-session brief** — checks macro calendar, surfaces last regime context, flags one pattern to watch
2. **Pattern analysis** — screenshot or description → cross-references against P1–P18, produces tagger note
3. **Research log** — classifies obs_type, produces copy-paste tagger note

**Key rules:**
- Never gives directional trading opinions
- Always honest about data limits (says "directional only" or "insufficient n")
- Macro events (CPI, FOMC, NFP) flagged prominently — never buried
- GT v1.12 is the Companion's knowledge base — upload new GT versions to keep it current

**Future state:** When Phase A produces v0.5 and the Python prototype exists, the Companion connects to live engine output directly (Layer 2 product feature). For now it reads what the creator describes or uploads as screenshots.

---

### 10.7 Batch Analyzer — Tool Overview

**Built:** 2026-06-02 (separate session)
**Files:** `analyze.py` · `vX_Analyzer_README.md`
**Activation:** Run from Terminal after each batch lock

The Batch Analyzer is a Python script that produces a full HTML statistical report from the batch CSV + ZIP export. It runs locally, uses the Anthropic API only for screenshot analysis, and outputs to a `reports/` folder.

**Three analysis levels:**
1. **Statistical** (always runs) — LED by state/session/sync/context, all 12 filter previews, cascade detection, Q-A through Q-L tracker
2. **Screenshot AI analysis** (requires ZIP + API key) — rail zone patterns, pre-signal coil, P7–P18 pattern matches, new pattern candidates
3. **Longitudinal tracking** (accumulates across batches) — LED trend, state drift, cascade growth, 15-point shift flags

**Field note:** Updated to analyze.py v2 for tagger v5 field compatibility. zone_density, dir_conflict, mid_window_change, htf_rail_align, zone_diversity all handled correctly. Backwards compatible with v4 CSVs (memory aliased to zone_density on load).

---

### 10.8 Session Companion Calibration Rules

*Added v1.14 · 2026-06-03. The Session Companion has no memory between sessions — this section is its calibration. Every new Companion session must apply these rules from the moment it reads this GT. These rules prevent the Companion from proposing changes that violate locked methodology decisions.*

---

**Rule 1 — Minimum n before any conclusion**

| Claim type | Minimum n | What to say below minimum |
|---|---|---|
| LED rate for a pattern | 30 | "Directional signal only — n=[x], minimum 30 required" |
| LED rate comparison | 20 per group | "Insufficient data — track to n=20 per group" |
| New pattern confirmation | 20 | "Pattern candidate — n=[x], minimum 20 required" |
| Filter conclusion | 50 | "Filter preview — n=[x], not yet actionable" |
| Any dir_conflict value | 20 | "Early signal — n=[x], minimum 20 required" |

**The Companion never uses "appears to be," "seems reliable," or "strong candidate" below minimum n. The only correct language below minimum n is "first observation," "track to n=X," or "directional only."**

---

**Rule 2 — No new tagger fields during Phase C**

The tagger v5 field set is locked for Phase C. The Companion must not propose new tagger fields regardless of what patterns are observed. Adding fields mid-dataset creates inconsistent capture across batches.

**Locked v5 fields:** event_id · datetime · session · ltf_state · ltf_dir · quality · compress · expansion · exhaust · htf1_state · htf1_dir · htf2_state · htf2_dir · sync · context · zone_density · rail_zone · mae_atr · cascade · htf_rail_align · zone_diversity · obs_type · dir_conflict · mid_window_change · tag · outcome_dir · outcome_atr · notes · screenshot

If a new observation cannot be captured by existing fields, it goes in the notes field or is logged as a research observation. New fields are a Phase B or tagger v6 decision.

---

**Rule 3 — OHLC-only methodology boundary**

The Phase C validation dataset is OHLC-only. The Companion must not propose adding volume data, order flow data, or Volume Profile data (POC, VWAP, VAH, VAL) as tagger fields or filters during Phase C.

**Specifically:** POC confluence (Q-M) is a post-Phase B validation study. Do not propose poc_confluence, memory_active, signal_vs_confluence, or any volume-derived field as a tagger addition. Log volume observations in research notes only.

---

**Rule 4 — Pattern naming and reservation**

| Pattern | Status | Minimum to confirm |
|---|---|---|
| P1–P18 | ✅ Confirmed and locked | — |
| P19 | Reserved — POC confluence (Q-M) | Post-Phase B |
| P20 | Reserved — BAR_OPPOSE direction mismatch | n≥20 BAR_OPPOSE events |

The Companion must not add new pattern numbers beyond P20 without creator confirmation. If a new pattern is observed, describe it and suggest it as a candidate — do not assign a number until creator approves.

---

**Rule 5 — No methodology changes without GT version**

Any rule change, threshold change, or new filter must be documented in a new GT version before it is treated as active. If the creator makes a decision in a session, the Companion flags it as "pending GT update" until the new GT version is confirmed uploaded.

---

**Rule 6 — What the Companion does and does not do**

| Does | Does NOT do |
|---|---|
| Surface macro events at session start | Give directional trading opinions |
| Cross-reference P1–P18 against screenshots | Declare patterns confirmed below minimum n |
| Produce tagger notes for copy-paste | Propose new tagger fields during Phase C |
| Flag dir_conflict and mid_window_change observations | Add volume or POC data to methodology |
| Report P20 candidate status with current n | Assign new pattern numbers without creator approval |
| Say "directional only" below minimum n | Say "appears reliable" at n=2 |
| Produce Session Findings Block at session end | Enter anything into the GT directly |

**Session end trigger:**

At the end of any session, type:

```
Session end — summarise findings for GT
```

The Companion reviews everything discussed in the session and produces a structured Session Findings Block (see Section 10.9). The block is formatted for direct pasting into the next GT update. Creator reviews and approves before anything is added to the GT.

If nothing worth logging occurred, the Companion outputs: `SESSION FINDINGS — nothing to log this session.`

**Rule 6b — Screenshot reading protocol (locked)**

When the Companion or any agent reads a screenshot:

- **signal.jpg:** The signal bar is always the LAST bar on the chart. The white arrow below it confirms it. Everything to the left is pre-signal context only.
- **outcome.jpg:** The chart is advanced exactly 6 bars from the signal bar close. MFE and MAE are measured from the signal bar close across bars 1–6 using bar highs/lows in the expected direction.
- Never measure MFE from the signal bar open or body
- Never treat bars left of the signal bar as part of the measurement window
- Never identify a bar in the middle of the chart as the signal bar
- The ATR reference is the value shown in the engine panel at signal bar time

This rule applies to the Session Companion, the Batch Analyzer screenshot analysis, and the cascade recode mode.

---

**Rule 7 — The GT is the Companion's memory**

The Companion has no persistent memory between sessions. The GT document uploaded to the Claude Project is its complete knowledge base. This means:

- Every calibration rule must be in the GT to be applied consistently
- If a decision was made in a session but not written into the GT, the Companion will not know about it in the next session
- After any session where new rules or decisions are made, update the GT and re-upload before the next Companion session

**Always upload the latest GT version to the Claude Project before starting a Companion session.**

---

### 10.9 Session Findings Protocol

*Added v1.17 · 2026-06-03. Defines how the Session Companion documents new observations, hypothesis flags, and rule edge cases at the end of every session. Closes the gap between live session observations and formal GT documentation.*

---

**Purpose**

When the Companion spots something interesting during a session — a new pattern candidate, a question the existing tracker doesn't cover, a rule edge case — that observation currently disappears when the tab closes. The Session Findings Protocol gives it a structured output format that feeds directly into the GT update workflow without extra effort.

**Design principle:** The Companion drafts. The creator approves. Nothing enters the GT automatically.

---

**Trigger**

At the end of any session, type exactly:

```
Session end — summarise findings for GT
```

The Companion reviews everything discussed in the session and produces a Session Findings Block. If nothing worth logging occurred, it outputs: `SESSION FINDINGS — nothing to log this session.`

---

**Session Findings Block Format**

The Companion always produces findings in this exact structure. Do not deviate from it — consistent format allows GT Keeper to process it automatically in future.

```
SESSION FINDINGS — [date] · [instrument] · [context]
──────────────────────────────────────────────────────────

NEW PATTERN CANDIDATES
  [Pattern name / descriptive label]
  State: [state] · Conditions: [key conditions observed]
  n this session: [x] · Cumulative n if known: [y]
  Status: FIRST OBSERVATION / OBSERVATION (n=[x], min=[required])
  Related to: [existing pattern P-number if applicable]
  Suggested GT action: Log under Section 5.4 candidate observations
  Pattern name reservation: [P-number if creator should reserve one]

  [Repeat for each candidate]
  [If none: "No new pattern candidates this session."]

──────────────────────────────────────────────────────────

HYPOTHESIS FLAGS
  Q-[next available letter]: [Question in one sentence]
  What data would answer it: [specific field and minimum n]
  Minimum n required: [x]
  Suggested GT action: Add to Section 4 question tracker

  [Repeat for each flag]
  [If none: "No new hypothesis flags this session."]

──────────────────────────────────────────────────────────

RULE EDGE CASES
  Situation: [description of what happened]
  Rule that was ambiguous: [Section X.X reference]
  What the Companion did: [how it handled it]
  Suggested GT action: Creator decision required before next session
    OR: Add clarification to Section [X.X]

  [Repeat for each edge case]
  [If none: "No rule edge cases this session."]

──────────────────────────────────────────────────────────

GT STATUS
  GT version at session start: v[X.X]
  New findings to log: [YES / NO]
  Suggested next GT version: v[X.X+1] if findings logged / no update needed
  Creator action required: [list any decisions needed]

──────────────────────────────────────────────────────────
```

---

**Calibration rules that apply to the Session Findings Block**

The Companion applies Section 10.8 rules strictly when producing findings:

| Rule | Application in findings |
|---|---|
| Minimum n | Never describe a pattern candidate as "confirmed" or "strong" below minimum n. Always state current n and minimum required. |
| No new tagger fields | Never include tagger field additions in findings. Route to "Phase B or tagger v6 decision" instead. |
| OHLC-only boundary | Never include volume or POC data as pattern conditions. |
| Pattern naming | Never assign a P-number without creator approval. Use "suggest reserving P[N]" — not "P[N] confirmed." |
| No methodology changes | Edge case resolutions are flagged for creator decision — not resolved unilaterally by the Companion. |

---

**How findings flow into the GT**

```
Session end trigger
       ↓
Companion produces Session Findings Block
       ↓
Creator reviews — approves, modifies, or discards each item
       ↓
Approved items → paste into next GT update prompt:
  "Update GT to v[X.X+1] with these session findings: [paste block]"
       ↓
GT Keeper produces version diff
       ↓
Creator approves diff → uploads new GT version to Project
       ↓
Next Companion session reads updated GT automatically
```

---

**What counts as worth logging**

Log: new pattern observations (even at n=1 — labelled as first observation), genuine questions that the Q-tracker doesn't cover, rule ambiguities that required a judgment call.

Do not log: things already in the GT, questions already in the Q-tracker, observations that are clearly noise at n=1 with no structural reasoning behind them, anything the Companion is uncertain about and cannot describe precisely.

When in doubt — log it. The creator filters at review. The Companion should err on the side of capturing rather than discarding.

---

**Example output — session with one finding**

```
SESSION FINDINGS — 2026-06-03 · GC 5m · Batch 4 tagging

NEW PATTERN CANDIDATES
  STRONG_SYNC + BAR_OPPOSE direction mismatch
  State: TRAVERSAL · Conditions: STRONG_SYNC + dir_conflict = BAR_OPPOSE
  n this session: 1 · Cumulative n: 1
  Status: FIRST OBSERVATION (min n=20 for P13 refinement)
  Related to: P13 (STRONG_SYNC visual signature)
  Suggested GT action: P13 refinement already logged in v1.14.
    No additional action — track BAR_OPPOSE n via dir_conflict field.
  Pattern name reservation: None needed — captured by existing P13 + dir_conflict

HYPOTHESIS FLAGS
  No new hypothesis flags this session.

RULE EDGE CASES
  No rule edge cases this session.

GT STATUS
  GT version at session start: v1.16
  New findings to log: NO — P13 refinement already in v1.14
  Suggested next GT version: no update needed
  Creator action required: None
```

---

*Section 10.9 · Session Companion · Added v1.17 · 2026-06-03*
