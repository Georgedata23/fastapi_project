from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base



class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now())


class Documents_text(Base):
    __tablename__ = "documents_text"

    id = Column(Integer, primary_key=True)
    id_doc = Column(Integer, ForeignKey('documents.id', ondelete="CASCADE"))
    text = Column(String)