import json
import re


def save_transcript(data):
    with open("transcript.json", "w") as f:
        json.dump(data, f, indent=4)


def save_evaluation(data):
    with open("evaluation.json", "w") as f:
        json.dump(data, f, indent=4)


def extract_score(text):
    """
    Extract score from AI response.
    Example:
    Score: 8/10
    """
    match = re.search(r"(\d+)/10", text)

    if match:
        return int(match.group(1))

    return 0


def calculate_total(scores):
    return sum(scores)


def calculate_average(scores):
    if len(scores) == 0:
        return 0
    return round(sum(scores) / len(scores), 2)


def hiring_recommendation(total):
    if total >= 40:
        return "Strong Hire ✅"
    elif total >= 30:
        return "Hire 👍"
    elif total >= 20:
        return "Consider 🤔"
    else:
        return "Not Recommended ❌"