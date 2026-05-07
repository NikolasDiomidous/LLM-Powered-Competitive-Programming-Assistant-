import json
from src.llm_client import ask
from src.prompts import CLASSIFIER_SYSTEM, PROBLEM_TYPES
from src.rag import retrieve_similar


def classify(problem_text: str, use_rag: bool = True) -> dict:
    if use_rag:
        examples = retrieve_similar(problem_text, k=3)
        user_msg = _build_user_msg_with_examples(problem_text, examples)
    else:
        user_msg = problem_text

    raw = ask(system=CLASSIFIER_SYSTEM, user=user_msg)
    result = json.loads(_extract_json(raw))
    _validate(result)
    if use_rag:
        result["retrieved_examples"] = examples
    return result


def _build_user_msg_with_examples(problem_text: str, examples: list[dict]) -> str:
    parts = ["Here are similar problems with known categories:\n"]
    for ex in examples:
        parts.append(f"- \"{ex['title']}\": {ex['statement']}")
        parts.append(f"  Categories: {ex['categories']}\n")
    parts.append(f"\nNow classify this new problem:\n\n{problem_text}")
    return "\n".join(parts)


def _extract_json(raw: str) -> str:
    import re
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON object found in response: {raw[:200]}")
    return match.group(0)


def _validate(result: dict) -> None:
    if not isinstance(result, dict):
        raise ValueError(f"expected dict, got {type(result)}")
    if "types" not in result or not isinstance(result["types"], list):
        raise ValueError("types must be a list")
    for t in result["types"]:
        if t not in PROBLEM_TYPES:
            raise ValueError(f"invalid type: {t}")
    if not isinstance(result.get("confidence"), (int, float)):
        raise ValueError("confidence must be numeric")
    if not 0 <= result["confidence"] <= 1:
        raise ValueError("confidence must be in [0,1]")
    if not isinstance(result.get("reasoning"), str):
        raise ValueError("reasoning must be string")