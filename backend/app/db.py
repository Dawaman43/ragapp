import os
from pymongo import MongoClient

# Expect a MongoDB URI in DATABASE_URL (or MONGO_URI); default to local
MONGO_URI = os.getenv("DATABASE_URL") or os.getenv("MONGO_URI") or "mongodb://localhost:27017/ragapp"

client = MongoClient(MONGO_URI)

# Determine database name from URI or fallback to 'ragapp'
try:
    if "/" in MONGO_URI:
        db_name = MONGO_URI.rsplit("/", 1)[-1]
        if "?" in db_name:
            db_name = db_name.split("?", 1)[0]
    else:
        db_name = "ragapp"
except Exception:
    db_name = "ragapp"

db = client[db_name]

def init_db():
    # MongoDB creates collections on first insert; nothing to do here.
    return
