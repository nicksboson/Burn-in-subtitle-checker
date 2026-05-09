# Burn-in Subtitle Checker (Mismatch Detection)

A Python-based utility to detect and flag mismatches between audio transcriptions and burnt-in subtitle text. Automates quality control for video content, ensuring that what is spoken matches what is displayed on screen.

---

## Preview

![Report Preview](./report.png)

---

## Features

| Feature | Details |
|---|---|
| **Text Normalization** | Strips punctuation, normalises casing, collapses spaces for fair comparison |
| **Hybrid Scoring** | Combines `fuzz.ratio` + `fuzz.token_sort_ratio` with a length penalty |
| **Automated Grading** | `OK` (≥90%) · `CHECK` (70–89%) · `REVIEW` (<70%) |
| **Word-Level Diff Highlighting** | Changed words shown in red/green inline in the report (stdlib `difflib`) |
| **Language Detection** | Auto-tags each segment's language (Hindi, Kannada, English, …) via `langdetect` |
| **Per-Language Stats** | Summary breakdown table grouped by detected language |
| **Inline Score Bar** | Colour-coded progress bar next to each score for at-a-glance severity |
| **Timestamp Drift Detection** | Optional `subtitle_timestamp` field; flags segments with >500ms sync drift |
| **CSV Export** | UTF-8 BOM CSV (Excel-compatible) via `--format csv` or the in-browser button |
| **JSON Export** | Structured `report.json` with summary + full result array |
| **HTML Report** | Filter buttons, clickable column sort, browser-side CSV export |
| **CLI with argparse** | `--input`, `--output`, `--format`, `--filter`, `--threshold-ok/check` |
| **Batch Processing** | Pass multiple files or a glob: `--input segments/*.json` |

---

## Tech Stack

* **Python 3.x**
* **RapidFuzz** — high-performance fuzzy string matching
* **langdetect** — language identification
* **difflib** — word-level diff highlighting (stdlib, zero extra deps)
* **HTML / CSS / Vanilla JS** — static dashboard report

---

## Getting Started

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic run (default — processes `data.json`, writes HTML + CSV + JSON)

```bash
python main.py
```

### Filter to REVIEW segments only, output CSV

```bash
python main.py --filter review --format csv
```

### Batch mode — process all JSON files in a directory

```bash
python main.py --input segments/*.json --output results/
```

### Custom thresholds

```bash
python main.py --threshold-ok 0.85 --threshold-check 0.65
```

### Full help

```bash
python main.py --help
```

---

## Input Format (`data.json`)

```json
[
  {
    "timestamp": 88.0,
    "audio": "This is a complete disaster",
    "subtitle": "यह पूरी तरह से एक आपदा है",
    "subtitle_timestamp": 91.5
  }
]
```

| Field | Required | Description |
|---|---|---|
| `timestamp` | ✅ | Audio segment start time (seconds) |
| `audio` | ✅ | Transcribed speech text |
| `subtitle` | ✅ | OCR-extracted burnt-in subtitle text |
| `subtitle_timestamp` | ❌ | Subtitle fire time — enables drift detection |

---

## Output Files

| File | Description |
|---|---|
| `report.html` | Interactive dashboard with filters, sort, diff highlights, score bars |
| `report.csv` | Flat CSV — open in Excel/Sheets, filter, annotate |
| `report.json` | Structured JSON with summary + full results (API-ready) |

---

## HTML Report Features

- **Filter buttons** — instantly show only OK / CHECK / REVIEW rows
- **Clickable column sort** — sort by Timestamp or Score
- **Browser-side CSV export** — "⬇ Export CSV" button respects active filter
- **Word diff** — changed words highlighted red (deleted) / green (inserted)
- **Score bar** — colour-coded progress bar per row
- **Drift badge** — ⏱ DRIFT badge when subtitle timestamp is >500ms off
- **Language column** — auto-detected per segment

---

## Limitations

* **Simulated input:** Input text is read from `data.json`. ASR (Whisper) and OCR (Tesseract/EasyOCR) integration is a future step.
* **Fuzzy similarity only:** Does not capture semantic equivalence (e.g. "Yeah" ≈ "Yes") — see Future Improvements.

---

## Future Improvements

* **ASR & OCR integration** — Directly process video files via OpenAI Whisper + Tesseract/EasyOCR
* **Semantic similarity** — `paraphrase-multilingual-MiniLM-L12-v2` supports Hindi, Kannada, and 50+ languages
* **Time-window alignment** — sliding-window comparison to handle subtitle sync drift gracefully
