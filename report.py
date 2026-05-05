def generate_html(results):
    html = """
    <html>
    <head>
    <style>
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid black; padding: 8px; text-align: center; }
    .ok { background-color: #c8f7c5; }
    .review { background-color: #f7c5c5; }
    </style>
    </head>
    <body>
    <h2>Mismatch Report</h2>
    <table>
    <tr>
        <th>Timestamp</th>
        <th>Audio</th>
        <th>Subtitle</th>
        <th>Score</th>
        <th>Status</th>
    </tr>
    """

    for r in results:
        row_class = "ok" if r["status"] == "OK" else "review"

        html += f"""
        <tr class="{row_class}">
            <td>{r['timestamp']}</td>
            <td>{r['audio']}</td>
            <td>{r['subtitle']}</td>
            <td>{r['score']}</td>
            <td>{r['status']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)