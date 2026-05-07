# CP Assistant

LLM-powered competitive programming coach for Codeforces and CSES problems. Built with Anthropic's Claude API and local sentence-transformers embeddings for retrieval-augmented classification.

## Features

- **Problem classifier** — multi-label classification across 12 algorithmic categories (DP, graph, greedy, binary search, etc.) with RAG-augmented few-shot prompting from a curated CSES corpus.
- **Progressive hint engine** — 4-level escalating hints (observation → category → skeleton → full approach) that build on previous hints and never reveal pseudocode.
- **Approach verifier** — classifies a proposed solution as correct, correct-but-suboptimal, partially correct, or wrong, with targeted feedback that hints rather than fixes.
- **Streamlit UI** — single-page interface integrating all three modules.

## Architecture
cp-assistant/
├── app.py                  # Streamlit UI
├── data/
│   └── cses_corpus.json    # 20 hand-labeled CSES problems for RAG
├── src/
│   ├── llm_client.py       # Anthropic API wrapper (ask, ask_multi)
│   ├── prompts.py          # System prompts for all 3 modules
│   ├── classifier.py       # Multi-label classification with RAG
│   ├── hint_engine.py      # Stateless 4-level hint generation
│   ├── verifier.py         # Approach verification
│   └── rag.py              # sentence-transformers embedding retrieval
└── requirements.txt
**Design principles:**
- Single source of truth for the LLM SDK in `llm_client.py`
- Stateless hint engine: state lives in the caller (Streamlit session)
- Strict JSON validation post-parse (fail fast, loud)
- RAG with similarity threshold (0.45) to prevent irrelevant examples from polluting the prompt

## Setup

```bash
git clone https://github.com/<your-user>/cp-assistant.git
cd cp-assistant
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

Create a `.env` file at the project root:
ANTHROPIC_API_KEY=sk-ant-...
Get a key from https://console.anthropic.com.

## Usage

```bash
streamlit run app.py
```

The browser will open at `http://localhost:8501`. Paste a problem statement, classify it, request progressive hints, and verify your approach.

## Tech stack

- **LLM:** Claude Sonnet 4.5 (`claude-sonnet-4-5`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local, ~80MB)
- **UI:** Streamlit
- **Language:** Python 3.13

## Limitations

- Hint engine has occasional leaks at level 1 for textbook problems with strong LLM priors (e.g. LIS).
- Verifier may misclassify problems that have a famous "trap" sibling in standard CP curricula (e.g. Coin Combinations I vs II).
- The CSES corpus is small (20 problems) — RAG retrieval falls back gracefully when no relevant examples exist.

## Author

Nikolas D., 2nd year ECE student at NTUA, IEEE NTUA Competitive Programming team.
