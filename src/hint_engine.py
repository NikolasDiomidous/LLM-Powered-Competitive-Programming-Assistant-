from src.llm_client import ask_multi
from src.prompts import HINT_SYSTEM


def get_hint(problem: str, level: int, previous_hints: list[str]) -> str:
    if not 1 <= level <= 4:
        raise ValueError(f"level must be 1-4, got {level}")
    if len(previous_hints) != level - 1:
        raise ValueError(
            f"level {level} requires exactly {level - 1} previous hints, "
            f"got {len(previous_hints)}"
        )

    messages = [
        {"role": "user", "content": f"Problem:\n\n{problem}\n\nGive me hint level 1."}
    ]
    for i, hint in enumerate(previous_hints):
        messages.append({"role": "assistant", "content": hint})
        messages.append({"role": "user", "content": f"Give me hint level {i + 2}."})

    return ask_multi(
        system=HINT_SYSTEM,
        messages=messages,
        temperature=0.4,
    )
