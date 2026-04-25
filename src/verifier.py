import json
from src.llm_client import ask
from src.prompts import VERIFIER_SYSTEM

VALID_OUTCOMES = {"correct", "correct_but_suboptimal", "partially_correct", "wrong_approach"}


def verify(problem: str, approach: str) -> dict:
    user_msg = f"Problem:\n\n{problem}\n\nStudent's approach:\n\n{approach}"
    raw = ask(system=VERIFIER_SYSTEM, user=user_msg, temperature=0.0)
    result = json.loads(_extract_json(raw))
    _validate(result)
    return result


def _extract_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines)
    return raw.strip()


def _validate(result: dict) -> None:
    if not isinstance(result, dict):
        raise ValueError(f"expected dict, got {type(result)}")
    if "outcome" not in result or result["outcome"] not in VALID_OUTCOMES:
        raise ValueError(f"invalid outcome: {result.get('outcome')}")
    if not isinstance(result.get("feedback"), str):
        raise ValueError("feedback must be string")
    if not isinstance(result.get("complexity"), str):
        raise ValueError("complexity must be string")