# CP Assistant

An AI-powered coaching tool for competitive programming — classifies problems, delivers progressive hints, and verifies your approach without spoiling the solution.

<!-- Add a screenshot or GIF of the app here -->
<!-- ![CP Assistant Demo](docs/demo.png) -->

## What it does

Paste any competitive programming problem and CP Assistant will identify the algorithm category with a confidence score, retrieve similar problems from the CSES dataset, and guide you through up to four escalating hint levels. When you think you have an approach, describe it and the verifier will tell you whether it is correct, suboptimal, partially correct, or wrong — along with complexity feedback — without revealing the full solution.

## Features

- **Problem Classification** — categorises problems into 12 algorithm types (DP, graph, greedy, binary search, etc.) with reasoning and confidence score
- **Progressive Hints** — 4-level hint ladder that builds from structural observations to a plain-English algorithm, enforcing strict anti-spoiler rules
- **Approach Verification** — evaluates your proposed solution for correctness and complexity, giving targeted feedback
- **Semantic Similar-Problem Search** — uses sentence-transformers embeddings to surface related CSES problems

## Tech Stack

| Layer | Library |
|---|---|
| UI | Streamlit |
| LLM | Anthropic SDK — Claude Sonnet |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Numerics | numpy |
| Config | python-dotenv |

## Getting Started

**Prerequisites:** Python 3.8+, an [Anthropic API key](https://console.anthropic.com)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/cp-assistant.git
cd cp-assistant

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install streamlit anthropic python-dotenv sentence-transformers numpy

# 4. Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 5. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Usage

1. Paste a problem statement and click **Classify** — see the algorithm type, confidence, reasoning, and similar problems.
2. Click **Get hint level 1** for a structural observation about the problem.
3. Progress through levels 2 → 3 → 4 for increasingly specific guidance.
4. Type your proposed approach and click **Verify** — get a verdict (correct / suboptimal / partially correct / wrong) plus complexity analysis.

## Project Structure

```
cp-assistant/
├── app.py               # Streamlit UI — ties all modules together
├── src/
│   ├── classifier.py    # Problem classification with RAG context
│   ├── hint_engine.py   # Multi-turn progressive hint conversations
│   ├── verifier.py      # Approach evaluation and feedback
│   ├── llm_client.py    # Anthropic SDK wrapper (single & multi-turn)
│   ├── prompts.py       # All system prompts and problem-type definitions
│   └── rag.py           # Sentence-transformer semantic search
├── data/
│   └── cses_corpus.json # Reference CSES problem dataset for RAG
└── .env                 # ANTHROPIC_API_KEY (not committed)
```

## Development Log

| Day | What was built |
|---|---|
| 1 | LLM client wrapper, classifier prompt, problem-type classification |
| 2 | Progressive hint engine |
| 3 | Approach verifier |
| 4 | Streamlit UI integrating all modules |
| 5 | RAG with sentence-transformers and few-shot classification |

## License

MIT — see [LICENSE](LICENSE) for details.
