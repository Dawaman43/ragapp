#!/usr/bin/env python3
"""Migration helper: copy `documents` from sqlite (data.db) to MongoDB.

Usage: python scripts/migrate_sqlite_to_mongo.py

This will look for a sqlite file at `./data.db` relative to `backend/`.
"""
import sqlite3
import os
from pymongo import MongoClient
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
SQLITE_PATH = os.path.join(ROOT, "data.db")

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("DATABASE_URL") or "mongodb://localhost:27017/ragapp"
client = MongoClient(MONGO_URI)
db = client.get_default_database()


def migrate():
    if not os.path.exists(SQLITE_PATH):
        print("No sqlite DB found at", SQLITE_PATH)
        return

    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, filename, content, metadata, uploaded_at FROM documents")
    except Exception as e:
        print("Error reading documents table:", e)
        return

    rows = cur.fetchall()
    if not rows:
        print("No rows found to migrate.")
        return

    inserted = []
    for r in rows:
        _id, filename, content, metadata, uploaded_at = r
        if isinstance(uploaded_at, str):
            try:
                uploaded = datetime.fromisoformat(uploaded_at)
            except Exception:
                uploaded = datetime.utcnow()
        else:
            uploaded = datetime.utcnow()

        doc = {
            "filename": filename,
            "content": content,
            "metadata": metadata or "",
            "uploaded_at": uploaded,
            "source_sqlite_id": _id,
        }
        res = db.documents.insert_one(doc)
        inserted.append(str(res.inserted_id))

    print(f"Migrated {len(inserted)} documents. Mongo IDs: {inserted}")


if __name__ == "__main__":
    migrate()
