from rapidfuzz import fuzz
import re
import difflib

try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False


def normalize(text):
    """Normalize text: lowercase, remove punctuation, collapse spaces."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_language(text):
    """Detect BCP-47 language code for a text string."""
    if not LANGDETECT_AVAILABLE:
        return "unknown"
    try:
        return detect(text)
    except Exception:
        return "unknown"


def highlight_diff(a, b):
    """Return (a_html, b_html) with <mark> tags around changed words."""
    a_words, b_words = a.split(), b.split()
    matcher = difflib.SequenceMatcher(None, a_words, b_words)
    a_result, b_result = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        ac = ' '.join(a_words[i1:i2])
        bc = ' '.join(b_words[j1:j2])
        if tag == 'equal':
            if ac: a_result.append(ac)
            if bc: b_result.append(bc)
        elif tag == 'replace':
            if ac: a_result.append(f'<mark class="diff-del">{ac}</mark>')
            if bc: b_result.append(f'<mark class="diff-ins">{bc}</mark>')
        elif tag == 'delete':
            a_result.append(f'<mark class="diff-del">{ac}</mark>')
        elif tag == 'insert':
            b_result.append(f'<mark class="diff-ins">{bc}</mark>')
    return ' '.join(a_result), ' '.join(b_result)


def classify_mismatch(audio, subtitle, score, lang_audio, lang_sub):
    """
    Classify the root cause of a mismatch into one of:
      LANGUAGE_SWITCH | COMPLETE_MISMATCH | TRUNCATED | ADDED_TEXT
      | WORD_SUBSTITUTION | MINOR_VARIATION | OK
    """
    if (lang_audio not in ("unknown", "") and lang_sub not in ("unknown", "")
            and lang_audio != lang_sub):
        return "LANGUAGE_SWITCH"
    if score < 0.25:
        return "COMPLETE_MISMATCH"
    len_ratio = len(subtitle) / max(len(audio), 1)
    if len_ratio < 0.55:
        return "TRUNCATED"
    if len_ratio > 1.65:
        return "ADDED_TEXT"
    if score >= 0.90:
        return "OK"
    a_set = set(audio.lower().split())
    s_set = set(subtitle.lower().split())
    if len(a_set.symmetric_difference(s_set)) >= 2:
        return "WORD_SUBSTITUTION"
    return "MINOR_VARIATION"


def compare_entry(entry, threshold_ok=0.90, threshold_check=0.70):
    """
    Compare audio transcript vs subtitle text.
    Returns enriched dict with score, status, mismatch_type,
    language, diff highlights, and drift info.
    """
    audio_raw    = entry["audio"]
    subtitle_raw = entry["subtitle"]
    audio        = normalize(audio_raw)
    subtitle     = normalize(subtitle_raw)

    ratio_score = fuzz.ratio(audio, subtitle)
    token_score = fuzz.token_sort_ratio(audio, subtitle)
    final_score = (0.4 * ratio_score) + (0.6 * token_score)

    if abs(len(audio) - len(subtitle)) > 5:
        final_score -= 5
    final_score = max(0, min(100, final_score)) / 100.0

    # Timestamp drift (optional field)
    drift_ms, drift_flagged = None, False
    if "subtitle_timestamp" in entry:
        drift_ms = abs(entry["timestamp"] - entry["subtitle_timestamp"]) * 1000
        if drift_ms > 500:
            drift_flagged = True

    # Status
    if drift_flagged:
        status = "REVIEW"
    elif final_score >= threshold_ok:
        status = "OK"
    elif final_score >= threshold_check:
        status = "CHECK"
    else:
        status = "REVIEW"

    lang_audio = detect_language(audio_raw)
    lang_sub   = detect_language(subtitle_raw)
    mismatch_type = classify_mismatch(audio, subtitle, final_score, lang_audio, lang_sub)
    audio_diff, subtitle_diff = highlight_diff(audio_raw, subtitle_raw)

    return {
        "timestamp":     entry["timestamp"],
        "audio":         audio_raw,
        "subtitle":      subtitle_raw,
        "audio_diff":    audio_diff,
        "subtitle_diff": subtitle_diff,
        "score":         round(final_score, 2),
        "status":        status,
        "language":      lang_audio,
        "lang_sub":      lang_sub,
        "mismatch_type": mismatch_type,
        "drift_ms":      round(drift_ms, 1) if drift_ms is not None else None,
        "drift_flagged": drift_flagged,
        "source":        entry.get("_source", "data.json"),
    }