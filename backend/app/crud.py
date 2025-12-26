from datetime import datetime
from typing import List
from pymongo.errors import PyMongoError
from app.db import db

# In-memory fallback when MongoDB is unavailable (allows local testing without Mongo)
_in_memory_docs: List[dict] = []
_use_memory = False

try:
    # quick connectivity check
    db.list_collection_names()
except Exception:
    _use_memory = True


def add_document(filename: str | None, content: str, metadata: str | None = None) -> dict:
    doc = {
        "filename": filename,
        "content": content,
        "metadata": metadata or "",
        "uploaded_at": datetime.utcnow(),
    }
    if _use_memory:
        _in_memory_docs.append(doc)
        return doc

    try:
        res = db.documents.insert_one(doc)
        doc["_id"] = res.inserted_id
        return doc
    except PyMongoError:
        _in_memory_docs.append(doc)
        return doc


def list_documents() -> List[dict]:
    if _use_memory:
        # return newest first to match previous behavior
        return list(reversed(_in_memory_docs))

    try:
        docs = list(db.documents.find().sort("uploaded_at", -1))
        return docs
    except PyMongoError:
        return list(reversed(_in_memory_docs))


