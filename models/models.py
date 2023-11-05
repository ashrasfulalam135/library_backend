from sqlalchemy import JSON, Column, Integer, String, Text
from sqlalchemy.sql.sqltypes import Integer
from db.database import Base

class Books(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(length=255))
    author = Column(String(length=255))
    description = Column(String(length=255))
    rating = Column(Integer)