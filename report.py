def generate_html(results):
    """
    Generate a clean HTML report for subtitle mismatch detection results.

    Args:
        results (list[dict]): Each dict contains:
            - timestamp (float): Time position in the media.
            - audio     (str):   Transcribed audio text.
            - subtitle  (str):   Burnt-in subtitle text.
            - score     (float): Similarity score (0–100).
            - status    (str):   "OK", "CHECK", or "REVIEW".

    Output:
        Writes 'report.html' (UTF-8) to the current working directory.
    """
    # Sort by score ascending (worst mismatches first)
    sorted_results = sorted(results, key=lambda x: x["score"])

    total   = len(sorted_results)
    ok_cnt  = sum(1 for r in sorted_results if r["status"] == "OK")
    chk_cnt = sum(1 for r in sorted_results if r["status"] == "CHECK")
    rev_cnt = sum(1 for r in sorted_results if r["status"] == "REVIEW")

    # Build table rows
    rows_html = ""
    for r in sorted_results:
        status = r["status"]
        if status == "OK":
            row_cls = "ok"
        elif status == "CHECK":
            row_cls = "check"
        else:
            row_cls = "review"

        rows_html += f"""
            <tr class="{row_cls}">
                <td class="ts">{r['timestamp']:.2f}s</td>
                <td>{r['audio']}</td>
                <td>{r['subtitle']}</td>
                <td class="score">{r['score']:.1f}</td>
                <td><span class="badge {row_cls}">{status}</span></td>
            </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mismatch Detection Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: #f5f5f5;
            color: #222;
            margin: 0;
            padding: 2rem 1rem;
        }}

        .wrap {{
            max-width: 1100px;
            margin: 0 auto;
        }}

        h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #111;
        }}

        .subtitle {{
            font-size: 0.85rem;
            color: #777;
            margin-bottom: 1.75rem;
        }}

        /* Summary */
        .summary {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.75rem;
            flex-wrap: wrap;
        }}

        .stat {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 0.85rem 1.25rem;
            min-width: 120px;
        }}

        .stat-label {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #888;
            margin-bottom: 0.3rem;
        }}

        .stat-value {{
            font-size: 1.6rem;
            font-weight: 600;
            color: #111;
            line-height: 1;
        }}

        .stat.ok    .stat-value {{ color: #2d7a2d; }}
        .stat.check .stat-value {{ color: #8a6200; }}
        .stat.review .stat-value {{ color: #c0392b; }}

        /* Table */
        .table-wrap {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }}

        thead {{
            position: sticky;
            top: 0;
            background: #fafafa;
            border-bottom: 2px solid #ddd;
        }}

        th {{
            padding: 0.75rem 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #555;
        }}

        td {{
            padding: 0.75rem 1rem;
            border-top: 1px solid #eee;
            vertical-align: top;
            color: #333;
        }}

        .ts {{
            font-family: monospace;
            font-size: 0.82rem;
            color: #888;
            white-space: nowrap;
        }}

        .score {{
            font-weight: 500;
            white-space: nowrap;
        }}

        /* Row backgrounds */
        tr.ok     {{ background: #f0faf0; }}
        tr.check  {{ background: #fffbf0; }}
        tr.review {{ background: #fff5f5; }}

        tr:hover {{ filter: brightness(0.97); }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.04em;
        }}

        .badge.ok     {{ background: #d4edda; color: #1e5c1e; }}
        .badge.check  {{ background: #fff3cd; color: #7a5500; }}
        .badge.review {{ background: #f8d7da; color: #a11; }}

        /* Footer */
        .footer {{
            margin-top: 1.5rem;
            font-size: 0.78rem;
            color: #aaa;
            text-align: right;
        }}
    </style>
</head>
<body>
<div class="wrap">

    <h1>Mismatch Detection Report</h1>
    <p class="subtitle">Sorted by score &mdash; lowest first. {total} segments analysed.</p>

    <div class="summary">
        <div class="stat">
            <div class="stat-label">Total</div>
            <div class="stat-value">{total}</div>
        </div>
        <div class="stat ok">
            <div class="stat-label">OK</div>
            <div class="stat-value">{ok_cnt}</div>
        </div>
        <div class="stat check">
            <div class="stat-label">Check</div>
            <div class="stat-value">{chk_cnt}</div>
        </div>
        <div class="stat review">
            <div class="stat-label">Review</div>
            <div class="stat-value">{rev_cnt}</div>
        </div>
    </div>

    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Audio</th>
                    <th>Subtitle</th>
                    <th>Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>

    <div class="footer">
        OK {ok_cnt} &nbsp;&middot;&nbsp; CHECK {chk_cnt} &nbsp;&middot;&nbsp; REVIEW {rev_cnt}
    </div>

</div>
</body>
</html>"""

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)