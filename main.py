import json
import glob
import argparse
import os
from datetime import datetime

from comparator import compare_entry
from report import generate_html, generate_csv, generate_json


def parse_args():
    parser = argparse.ArgumentParser(
        description="Burn-in Subtitle Checker — Mismatch Detection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --input segments/*.json --output results/
  python main.py --filter review --format csv
  python main.py --threshold-ok 0.85 --threshold-check 0.65
        """
    )
    parser.add_argument(
        "--input", "-i", nargs="+", default=["data.json"],
        help="Input JSON file(s) or glob pattern (default: data.json)"
    )
    parser.add_argument(
        "--output", "-o", default=".",
        help="Output directory for reports (default: current directory)"
    )
    parser.add_argument(
        "--format", "-f", choices=["html", "csv", "json", "all"], default="all",
        help="Output format: html, csv, json, or all (default: all)"
    )
    parser.add_argument(
        "--filter", choices=["ok", "check", "review", "all"], default="all",
        help="Only include rows with this status in output (default: all)"
    )
    parser.add_argument(
        "--threshold-ok", type=float, default=0.90,
        help="Minimum score for OK status (default: 0.90)"
    )
    parser.add_argument(
        "--threshold-check", type=float, default=0.70,
        help="Minimum score for CHECK status (default: 0.70)"
    )
    return parser.parse_args()


def load_inputs(patterns):
    """Resolve glob patterns, load JSON files, tag each item with its source filename."""
    all_items, files_loaded = [], []
    for pattern in patterns:
        matched = glob.glob(pattern)
        if not matched:
            matched = [pattern]          # treat as literal path
        for filepath in matched:
            if not os.path.exists(filepath):
                print(f"[WARN] File not found: {filepath}")
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                item["_source"] = os.path.basename(filepath)
            all_items.extend(items)
            files_loaded.append(filepath)
    return all_items, files_loaded


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    # ── Load ─────────────────────────────────────────────────────────────────
    data, files = load_inputs(args.input)
    if not data:
        print("[ERROR] No data loaded. Check your --input paths.")
        return
    print(f"Loaded {len(data)} segment(s) from {len(files)} file(s).")

    # ── Compare ───────────────────────────────────────────────────────────────
    results = [
        compare_entry(item, args.threshold_ok, args.threshold_check)
        for item in data
    ]
    results.sort(key=lambda x: x["score"])  # worst mismatches first

    # ── Filter ────────────────────────────────────────────────────────────────
    if args.filter != "all":
        filtered = [r for r in results if r["status"].lower() == args.filter]
    else:
        filtered = results
    print(f"Showing {len(filtered)}/{len(results)} segments (filter: {args.filter})")

    gen_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Export ────────────────────────────────────────────────────────────────
    if args.format in ("html", "all"):
        path = os.path.join(args.output, "report.html")
        generate_html(filtered, path, all_results=results, generated_at=gen_at)
        print(f"  >> {path}")

    if args.format in ("csv", "all"):
        path = os.path.join(args.output, "report.csv")
        generate_csv(filtered, path)
        print(f"  >> {path}")

    if args.format in ("json", "all"):
        path = os.path.join(args.output, "report.json")
        generate_json(filtered, path, all_results=results, generated_at=gen_at)
        print(f"  >> {path}")

    print("Done!")


if __name__ == "__main__":
    main()