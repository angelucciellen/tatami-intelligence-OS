# vX Rhythm Engine — Batch Analyzer

Run this after every batch to get a full statistical report, screenshot pattern analysis, and cascade detection automatically.

---

## Setup (one time only)

### 1. Install Python dependencies

Open Terminal and run:

```bash
pip3 install anthropic pillow pandas numpy
```

### 2. Set your Anthropic API key (for screenshot analysis)

```bash
export ANTHROPIC_API_KEY=your_key_here
```

To get your API key: https://console.anthropic.com

To make this permanent (so you don't need to set it every time), add it to your shell profile:
```bash
echo 'export ANTHROPIC_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```

### 3. Put the analyzer in your project folder

Place `analyze.py` inside your vX-Rhythm-Engine folder, e.g.:
```
vX-Rhythm-Engine/
├── analyzer/
│   └── analyze.py
├── data/
│   └── GC_5m_Batch3_E101-E150_2026-05-30.csv
│   └── GC_5m_Batch3_E101-E150_2026-05-30.zip
```

---

## Usage

### Basic (stats only, no screenshots)

```bash
cd vX-Rhythm-Engine/analyzer
python3 analyze.py \
  --csv ../data/GC_5m_Batch4_E151-E200_2026-06-15.csv \
  --batch 4
```

### Full analysis (stats + screenshot AI analysis)

```bash
python3 analyze.py \
  --csv ../data/GC_5m_Batch4_E151-E200_2026-06-15.csv \
  --zip ../data/GC_5m_Batch4_E151-E200_2026-06-15.zip \
  --batch 4
```

### With prior batch comparison

```bash
python3 analyze.py \
  --csv ../data/GC_5m_Batch4_E151-E200_2026-06-15.csv \
  --zip ../data/GC_5m_Batch4_E151-E200_2026-06-15.zip \
  --batch 4 \
  --prior ../data/GC_5m_Batch3_E101-E150_2026-05-30.csv
```

### Skip AI screenshot analysis (offline / faster)

```bash
python3 analyze.py \
  --csv ../data/GC_5m_Batch4_E151-E200.csv \
  --batch 4 \
  --no-ai
```

---

## Output

The script creates a `reports/` folder with:

- `vX_Batch4_Analysis_20260615_1430.html` — open this in your browser
- `vX_Batch4_stats_20260615_1430.json` — raw data if you need it
- `reports/history.json` — accumulates across all batches for longitudinal tracking

---

## What the report contains

### Level 1 — Statistical analysis (always runs)
- Overall LED rate with anomaly flags
- LED by state, session, sync state, context, day, hour
- Quality band analysis (Traversal only)
- All 12 filter previews vs unfiltered baseline
- Cascade pair detection with both-LED rate
- Open question tracker (Q-A through Q-L)

### Level 2 — Screenshot pattern analysis (requires --zip and API key)
- Rail zone vs LED rate (Lower/Mid/Upper)
- Channel width vs LED rate (Narrow/Expanding/Wide)
- Pre-signal coil presence vs LED rate
- Post-move trap detection
- Pattern matches (P7–P18) across all events
- New pattern suggestions flagged automatically

### Level 3 — Longitudinal tracking (builds across batches)
- LED rate trend across all batches
- State-level drift detection
- Cascade growth tracking
- Flags when any metric shifts more than 15 points

---

## Anomaly flags

The analyzer automatically flags:
- LED rate below 45% → critical
- LED rate below 50% → warning
- Traversal concentration above 65% → warning
- Exhaustion LED rate below 45% → warning
- Any state with n < 5 → info

---

## After each batch — your workflow

1. Export CSV + ZIP from tagger
2. Save both to `data/` folder with correct naming
3. Run the analyzer
4. Open the HTML report in your browser
5. Check anomaly flags and question tracker
6. Upload updated Ground Truth to Claude Project if any findings change rules
7. Git commit + push

---

## Cost estimate (screenshot AI analysis)

Each screenshot analysis costs approximately $0.002–0.005 with Claude Sonnet.
50 events per batch = ~$0.10–0.25 per batch.
Negligible.
