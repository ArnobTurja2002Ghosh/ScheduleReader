import json
from difflib import SequenceMatcher
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()
def match_employee_name(ocr_text, employees, threshold=0.6):

    best = None
    best_score = 0

    for name in employees:
        score = similarity(ocr_text, name)
        if score > best_score:
            best = name
            best_score = score

    return {
        "original": ocr_text,
        "matched": best if best_score >= threshold else None,
        "score": round(best_score, 2),
        "uncertain": best_score < threshold
    }

def load_employee_names(path="data/names.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data["employees"]
