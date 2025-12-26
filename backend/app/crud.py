from datetime import datetime
from typing import List
from bson.objectid import ObjectId
from .db import db


def add_document(filename: str | None, content: str, metadata: str | None = None) -> dict:
    doc = {
        "filename": filename,
        "content": content,
        "metadata": metadata or "",
        "uploaded_at": datetime.utcnow(),
    }
    res = db.documents.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc


def list_documents() -> List[dict]:
    docs = list(db.documents.find().sort("uploaded_at", -1))
    return docs

