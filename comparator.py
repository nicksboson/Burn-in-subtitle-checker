from rapidfuzz import fuzz
import re

def normalize(text):
    """
    Normalizes text by converting to lowercase, removing punctuation,
    and collapsing multiple spaces into a single space.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def compare_entry(entry):
    """
    Compares the audio transcript and subtitle text from an entry dictionary,
    calculates a hybrid similarity score, and assigns a review status.
    """
    audio = normalize(entry["audio"])
    subtitle = normalize(entry["subtitle"])

    ratio_score = fuzz.ratio(audio, subtitle)
    token_score = fuzz.token_sort_ratio(audio, subtitle)

    final_score = (0.4 * ratio_score) + (0.6 * token_score)

    # length penalty
    length_diff = abs(len(audio) - len(subtitle))
    if length_diff > 5:
        final_score -= 5

    final_score = max(0, min(100, final_score))

    if final_score >= 90:
        status = "OK"
    elif final_score >= 70:
        status = "CHECK"
    else:
        status = "REVIEW"

    return {
        "timestamp": entry["timestamp"],
        "audio": entry["audio"],
        "subtitle": entry["subtitle"],
        "score": round(final_score, 2),
        "status": status
    }