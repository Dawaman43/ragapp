from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from .db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(Text, nullable=True)
