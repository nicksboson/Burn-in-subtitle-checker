from rapidfuzz import fuzz

def compare_entry(entry):
    score = fuzz.ratio(entry["audio"], entry["subtitle"])

    if score >= 85:
         status = "OK"
    else:
        status = "REVIEW"

    return {
        "timestamp": entry["timestamp"],
        "audio": entry["audio"],
        "subtitle": entry["subtitle"],
        "score": round(score, 2),
        "status": status
    }