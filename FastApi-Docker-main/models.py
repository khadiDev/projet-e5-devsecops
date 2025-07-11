from sqlalchemy import Column, Integer, String, Date
from database import Base

class Book(Base):
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    published_date = Column(Date)
    isbn = Column(String(20), unique=True, index=True)
