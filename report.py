import csv
import json
from datetime import datetime
from collections import Counter

from _html_assets import CSS, JS

LANG_NAMES = {
    "hi": "Hindi", "kn": "Kannada", "en": "English", "ta": "Tamil",
    "te": "Telugu", "mr": "Marathi", "bn": "Bengali", "gu": "Gujarati",
    "pa": "Punjabi", "ml": "Malayalam", "ur": "Urdu", "unknown": "Unknown",
}

_TYPE_META = {
    "LANGUAGE_SWITCH":   ("t-ls", "Lang Switch"),
    "COMPLETE_MISMATCH": ("t-cm", "Complete MM"),
    "TRUNCATED":         ("t-tr", "Truncated"),
    "ADDED_TEXT":        ("t-at", "Added Text"),
    "WORD_SUBSTITUTION": ("t-ws", "Word Sub"),
    "MINOR_VARIATION":   ("t-mv", "Minor Var"),
    "OK":                ("t-ok", "OK"),
}


def _lang_name(code):
    return LANG_NAMES.get(code, (code or "?").upper())


def _donut_svg(ok, chk, rev):
    """Return inline SVG donut chart. JS can update it via IDs."""
    tot = ok + chk + rev or 1
    okP  = round(ok  / tot * 100, 2)
    chkP = round(chk / tot * 100, 2)
    revP = round(rev / tot * 100, 2)
    ok_off  = 25
    chk_off = round(25 - okP, 2)
    rev_off = round(25 - okP - chkP, 2)
    ok_pct  = round(ok / tot * 100)
    return (
        f'<svg viewBox="0 0 42 42" width="130" height="130" role="img" '
        f'aria-label="Score distribution: {ok_pct}% OK">'
        f'<circle cx="21" cy="21" r="15.9155" fill="none" stroke="#eee" stroke-width="5"/>'
        f'<circle id="donut-ok"  cx="21" cy="21" r="15.9155" fill="none" stroke="#27ae60" stroke-width="5" '
        f'stroke-dasharray="{okP} {100-okP}" stroke-dashoffset="{ok_off}"/>'
        f'<circle id="donut-chk" cx="21" cy="21" r="15.9155" fill="none" stroke="#e67e22" stroke-width="5" '
        f'stroke-dasharray="{chkP} {100-chkP}" stroke-dashoffset="{chk_off}"/>'
        f'<circle id="donut-rev" cx="21" cy="21" r="15.9155" fill="none" stroke="#e74c3c" stroke-width="5" '
        f'stroke-dasharray="{revP} {100-revP}" stroke-dashoffset="{rev_off}"/>'
        f'<text x="21" y="19.5" text-anchor="middle" font-size="5.5" font-weight="700" fill="#111" id="donut-lbl">{ok_pct}% OK</text>'
        f'<text x="21" y="25"   text-anchor="middle" font-size="3.2" fill="#aaa">distribution</text>'
        f'</svg>'
    )


# ─── CSV ──────────────────────────────────────────────────────────────────────

def generate_csv(results, path="report.csv"):
    """Export results to UTF-8 BOM CSV (Excel-compatible)."""
    fields = ["timestamp", "audio", "subtitle", "score", "status",
              "mismatch_type", "language", "drift_ms", "drift_flagged", "source"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in results:
            w.writerow({
                "timestamp":     f"{r['timestamp']:.2f}",
                "audio":         r["audio"],
                "subtitle":      r["subtitle"],
                "score":         f"{r['score']:.2f}",
                "status":        r["status"],
                "mismatch_type": r.get("mismatch_type", ""),
                "language":      _lang_name(r.get("language", "unknown")),
                "drift_ms":      r.get("drift_ms", ""),
                "drift_flagged": r.get("drift_flagged", False),
                "source":        r.get("source", ""),
            })


# ─── JSON ─────────────────────────────────────────────────────────────────────

def generate_json(results, path="report.json", all_results=None, generated_at=None):
    """Export structured JSON with summary + full result array."""
    all_r = all_results or results
    total = len(all_r)
    ok_c  = sum(1 for r in all_r if r["status"] == "OK")
    chk_c = sum(1 for r in all_r if r["status"] == "CHECK")
    rev_c = sum(1 for r in all_r if r["status"] == "REVIEW")
    avg   = round(sum(r["score"] for r in all_r) / total, 3) if total else 0
    lang_c = Counter(r.get("language", "unknown") for r in all_r)
    type_c = Counter(r.get("mismatch_type", "") for r in all_r)
    out = {
        "generated_at": generated_at or datetime.now().isoformat(),
        "summary": {
            "total": total, "ok": ok_c, "check": chk_c,
            "review": rev_c, "avg_score": avg,
            "by_language": {_lang_name(k): v for k, v in lang_c.most_common()},
            "by_mismatch_type": dict(type_c.most_common()),
        },
        "results": [{
            "timestamp":     r["timestamp"],
            "audio":         r["audio"],
            "subtitle":      r["subtitle"],
            "score":         r["score"],
            "status":        r["status"],
            "mismatch_type": r.get("mismatch_type", ""),
            "language":      _lang_name(r.get("language", "unknown")),
            "drift_ms":      r.get("drift_ms"),
            "drift_flagged": r.get("drift_flagged", False),
            "source":        r.get("source", ""),
        } for r in results],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


# ─── HTML ─────────────────────────────────────────────────────────────────────

def generate_html(results, path="report.html", all_results=None, generated_at=None):
    """Generate the full interactive HTML dashboard."""
    all_r   = all_results or results
    total   = len(all_r)
    ok_cnt  = sum(1 for r in all_r if r["status"] == "OK")
    chk_cnt = sum(1 for r in all_r if r["status"] == "CHECK")
    rev_cnt = sum(1 for r in all_r if r["status"] == "REVIEW")
    avg     = sum(r["score"] for r in all_r) / total if total else 0

    # ── language breakdown table ──────────────────────────────────────────────
    lang_rows = ""
    for code, cnt in Counter(r.get("language", "unknown") for r in all_r).most_common():
        lo = sum(1 for r in all_r if r.get("language") == code and r["status"] == "OK")
        lc = sum(1 for r in all_r if r.get("language") == code and r["status"] == "CHECK")
        lr = sum(1 for r in all_r if r.get("language") == code and r["status"] == "REVIEW")
        lang_rows += (f"<tr><td>{_lang_name(code)}</td><td>{cnt}</td>"
                      f"<td class='ok-text'>{lo}</td>"
                      f"<td class='chk-text'>{lc}</td>"
                      f"<td class='rev-text'>{lr}</td></tr>")

    # ── multi-source column ───────────────────────────────────────────────────
    multi = len(set(r.get("source", "") for r in all_r)) > 1
    src_th  = "<th>Source</th>" if multi else ""
    score_ci = 5 if multi else 4      # column index for score sort

    # ── table rows ────────────────────────────────────────────────────────────
    rows_html = ""
    for r in results:
        st  = r["status"]
        cls = st.lower()
        pct = int(r["score"] * 100)
        bar_col = {"OK": "#27ae60", "CHECK": "#e67e22", "REVIEW": "#e74c3c"}[st]
        drift_b = (f'<span class="badge drift" title="{r["drift_ms"]:.0f}ms drift">⏱ DRIFT</span>'
                   if r.get("drift_flagged") else "")
        mt      = r.get("mismatch_type", "")
        mt_cls, mt_lbl = _TYPE_META.get(mt, ("t-mv", mt))
        type_b  = f'<span class="badge {mt_cls}">{mt_lbl}</span>'
        src_td  = f"<td class='src'>{r.get('source','')}</td>" if multi else ""
        ts_key  = str(r["timestamp"]).replace(".", "_")
        r_ts    = r["timestamp"]
        r_sc    = r["score"]
        rows_html += (
            f'<tr class="{cls}" data-status="{cls}" data-score="{r_sc}" '
            f'tabindex="0" role="row" aria-label="Timestamp {r_ts}s score {r_sc}">'
            f"<td class='ts'>{r_ts:.2f}s</td>"
            f"{src_td}"
            f"<td class='lang'>{_lang_name(r.get('language','?'))}</td>"
            f"<td>{r.get('audio_diff', r['audio'])}</td>"
            f"<td>{r.get('subtitle_diff', r['subtitle'])}</td>"
            f"<td class='sc-cell'>"
            f"<div class='sc-num'>{r['score']:.2f}</div>"
            f"<div class='sc-bar-wrap'><div class='sc-bar' style='width:{pct}%;background:{bar_col}'></div></div>"
            f"</td>"
            f"<td><span class='badge sb {cls}'>{st}</span>{drift_b}</td>"
            f"<td>{type_b}</td>"
            f"<td class='note-cell' contenteditable='true' data-ts='{ts_key}' "
            f"aria-label='Reviewer note for timestamp {r_ts}s'></td>"
            f"</tr>"
        )

    shown  = len(results)
    gen_at = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    donut  = _donut_svg(ok_cnt, chk_cnt, rev_cnt)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta name="description" content="Burn-in subtitle mismatch detection report — {total} segments analysed"/>
<title>Mismatch Detection Report</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<div class="hdr">
  <div>
    <h1>🎬 Mismatch Detection Report</h1>
    <p class="sub">Sorted by score — lowest first &bull; {total} segments &bull; {gen_at}</p>
  </div>
  <div class="hdr-btns">
    <button class="icon-btn" onclick="window.print()" title="Print / Save as PDF">🖨 Print</button>
    <button class="icon-btn" onclick="toggleDark()" title="Toggle dark mode">🌙 Dark</button>
  </div>
</div>

<div class="summary">
  <div class="stat"><div class="stat-label">Total</div><div class="stat-value">{total}</div></div>
  <div class="stat ok"><div class="stat-label">OK</div><div class="stat-value" id="cnt-ok">{ok_cnt}</div></div>
  <div class="stat chk"><div class="stat-label">Check</div><div class="stat-value" id="cnt-chk">{chk_cnt}</div></div>
  <div class="stat rev"><div class="stat-label">Review</div><div class="stat-value" id="cnt-rev">{rev_cnt}</div></div>
  <div class="stat"><div class="stat-label">Avg Score</div><div class="stat-value">{avg:.2f}</div></div>
  <div class="donut-wrap">
    {donut}
    <div class="donut-legend">
      <span><div class="dot" style="background:#27ae60"></div>OK</span>
      <span><div class="dot" style="background:#e67e22"></div>Check</span>
      <span><div class="dot" style="background:#e74c3c"></div>Review</span>
    </div>
  </div>
</div>

<div class="sliders">
  <h3>Live Threshold Tuner — drag to reclassify rows instantly</h3>
  <div class="slider-row">
    <label>OK threshold</label>
    <input type="range" id="okSlider" min="0" max="1" step="0.01" value="0.90" oninput="reclassify()" aria-label="OK score threshold"/>
    <span class="slider-val" id="okVal">0.90</span>
  </div>
  <div class="slider-row">
    <label>CHECK threshold</label>
    <input type="range" id="chkSlider" min="0" max="1" step="0.01" value="0.70" oninput="reclassify()" aria-label="CHECK score threshold"/>
    <span class="slider-val" id="chkVal">0.70</span>
  </div>
</div>

<div class="section-title">By Language</div>
<div class="lang-wrap">
  <table class="lt" role="table" aria-label="Breakdown by language">
    <thead><tr><th>Language</th><th>Total</th><th>OK</th><th>CHECK</th><th>REVIEW</th></tr></thead>
    <tbody>{lang_rows}</tbody>
  </table>
</div>

<div class="toolbar">
  <span>Filter:</span>
  <button class="fbtn active" id="btn-all"    onclick="filterTable('all',this)"    aria-pressed="true">All ({total})</button>
  <button class="fbtn"        id="btn-ok"     onclick="filterTable('ok',this)"     aria-pressed="false">OK ({ok_cnt})</button>
  <button class="fbtn"        id="btn-check"  onclick="filterTable('check',this)"  aria-pressed="false">Check ({chk_cnt})</button>
  <button class="fbtn"        id="btn-review" onclick="filterTable('review',this)" aria-pressed="false">Review ({rev_cnt})</button>
  <input  type="search" class="search-box" placeholder="Search audio or subtitle…" oninput="searchTable(this.value)" aria-label="Search segments"/>
  <div class="ml-auto">
    <button class="action-btn btn-red"  onclick="jumpToWorst()"  title="Scroll to the lowest-scored visible row">⚠ Worst</button>
    <button class="action-btn btn-blue" onclick="exportCSV()"    title="Download visible rows as CSV">⬇ CSV</button>
  </div>
</div>

<div class="table-wrap">
  <table id="mainTable" role="grid" aria-label="Subtitle mismatch results" aria-rowcount="{total}">
    <thead>
      <tr role="row">
        <th class="sortable" onclick="sortTable(0)" aria-sort="none" scope="col">Timestamp ↕</th>
        {src_th}
        <th scope="col">Language</th>
        <th scope="col">Audio</th>
        <th scope="col">Subtitle</th>
        <th class="sortable" onclick="sortTable({score_ci})" aria-sort="none" scope="col">Score ↕</th>
        <th scope="col">Status</th>
        <th scope="col">Mismatch Type</th>
        <th scope="col">Reviewer Notes</th>
      </tr>
    </thead>
    <tbody id="tbody" role="rowgroup">{rows_html}</tbody>
  </table>
</div>

<div class="footer">
  OK {ok_cnt} &middot; CHECK {chk_cnt} &middot; REVIEW {rev_cnt}
  &middot; Avg {avg:.2f} &middot; Showing {shown}/{total}
  &middot; Notes auto-saved in browser
</div>

</div>
<script>{JS}</script>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)