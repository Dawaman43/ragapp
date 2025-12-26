import os
from urllib.parse import urlparse
from pymongo import MongoClient

# Expect a MongoDB URI in DATABASE_URL (or MONGO_URI); default to local
MONGO_URI = os.getenv("DATABASE_URL") or os.getenv("MONGO_URI") or "mongodb://localhost:27017/ragapp"

client = MongoClient(MONGO_URI)

# Robustly determine database name from URI path, fallback to 'ragapp'
try:
    parsed = urlparse(MONGO_URI)
    path = (parsed.path or "").lstrip("/")
    db_name = path.split("?", 1)[0] if path else "ragapp"
    if not db_name:
        db_name = "ragapp"
except Exception:
    db_name = "ragapp"

db = client[db_name]

def init_db():
    # MongoDB creates collections on first insert; nothing to do here.
    return
