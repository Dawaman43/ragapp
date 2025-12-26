from sqlalchemy.orm import Session
from . import models


def add_document(db: Session, filename: str | None, content: str, metadata: str | None = None):
    doc = models.Document(filename=filename, content=content, metadata=metadata)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def list_documents(db: Session):
    return db.query(models.Document).order_by(models.Document.uploaded_at.desc()).all()
