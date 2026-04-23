import json
from src.llm_client import ask
from src.prompts import CLASSIFIER_SYSTEM, PROBLEM_TYPES

def _extract_json(raw: str) -> str:
    text = raw.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    return text.strip()
def classify(problem_text: str) -> dict:
    raw_response = ask(
        system=CLASSIFIER_SYSTEM,
        user=problem_text,
    )

    result = json.loads(_extract_json(raw_response))

    _validate(result)

    return result


def _validate(result: dict) -> None:
    if not isinstance(result.get("types"), list):
        raise ValueError(f"'types' must be a list, got {type(result.get('types'))}")

    for t in result["types"]:
        if t not in PROBLEM_TYPES:
            raise ValueError(f"Unknown category '{t}'. Allowed: {PROBLEM_TYPES}")

    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
        raise ValueError(f"'confidence' must be float in [0, 1], got {confidence}")

    if not isinstance(result.get("reasoning"), str):
        raise ValueError("'reasoning' must be a string")