import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL_NAME = "all-MiniLM-L6-v2"
_CORPUS_PATH = Path("data/cses_corpus.json")

_model = None
_corpus = None
_embeddings = None


def _load():
    global _model, _corpus, _embeddings
    if _model is not None:
        return
    _model = SentenceTransformer(_MODEL_NAME)
    with open(_CORPUS_PATH, encoding="utf-8") as f:
        _corpus = json.load(f)
    texts = [f"{p['title']}. {p['statement']}" for p in _corpus]
    _embeddings = _model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def retrieve_similar(problem: str, k: int = 3) -> list[dict]:
    _load()
    query_emb = _model.encode([problem], convert_to_numpy=True, normalize_embeddings=True)[0]
    scores = _embeddings @ query_emb
    top_k_idx = np.argsort(scores)[::-1][:k]
    return [
        {**_corpus[i], "score": float(scores[i])}
        for i in top_k_idx
    ]