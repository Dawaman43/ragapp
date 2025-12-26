from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Header
from typing import List
import os

from app.db import SessionLocal, init_db
from app.crud import add_document
from app.services.retriever import refresh_index

router = APIRouter()


def _check_admin(key: str | None):
    expected = os.getenv("ADMIN_API_KEY")
    if expected is None:
        raise HTTPException(status_code=500, detail="ADMIN_API_KEY not configured on server")
    if key != expected:
        raise HTTPException(status_code=403, detail="invalid admin key")


@router.on_event("startup")
def _startup():
    init_db()


@router.post("/admin/ingest")
async def ingest(
    admin_key: str | None = Header(None, alias="X-Admin-Key"),
    text: str | None = Form(None),
    files: List[UploadFile] | None = File(None),
):
    # simple API-key check
    _check_admin(admin_key)

    db = SessionLocal()
    added = []
    try:
        if text:
            doc = add_document(db, filename=None, content=text)
            added.append(doc.id)

        if files:
            for f in files:
                content = (await f.read()).decode(errors="ignore")
                doc = add_document(db, filename=f.filename, content=content)
                added.append(doc.id)
    finally:
        db.close()

    # rebuild retriever index
    refresh_index()

    return {"ingested_ids": added}
