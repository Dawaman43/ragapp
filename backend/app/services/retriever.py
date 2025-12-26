from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .db import SessionLocal
from .crud import list_documents

_vectorizer: TfidfVectorizer | None = None
_doc_texts: List[str] = []
_doc_ids: List[int] = []
_matrix = None


def _rebuild_index():
    global _vectorizer, _doc_texts, _doc_ids, _matrix
    with SessionLocal() as db:
        docs = list_documents(db)
    _doc_texts = [d.content for d in docs]
    _doc_ids = [d.id for d in docs]
    if _doc_texts:
        _vectorizer = TfidfVectorizer().fit(_doc_texts)
        _matrix = _vectorizer.transform(_doc_texts)
    else:
        _vectorizer = None
        _matrix = None


def retrieve(query: str, top_k: int = 3) -> List[Tuple[int, str, float]]:
    """Return top_k documents as (id, text, score)."""
    global _vectorizer, _matrix, _doc_texts, _doc_ids
    if _vectorizer is None or _matrix is None:
        _rebuild_index()
    if _vectorizer is None or _matrix is None:
        return []

    qv = _vectorizer.transform([query])
    sims = cosine_similarity(qv, _matrix)[0]
    idxs = sims.argsort()[::-1][:top_k]
    results = []
    for i in idxs:
        results.append((_doc_ids[i], _doc_texts[i], float(sims[i])))
    return results


def refresh_index():
    _rebuild_index()
