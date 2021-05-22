from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.db import Base


class Message(Base):
    __tablename__ = "messages"
    rowid = Column(Integer, primary_key=True, autoincrement=True)
    mid = Column(Integer)
    uid = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    text = Column(String)
    file_id = Column(String)
    file_unique_id = Column(String)
