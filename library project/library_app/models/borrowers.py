
from sqlalchemy import Column,Integer,String

from library_app.db.database import Base



class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True)
    email = Column(String,unique=True , nullable=False)
    phone = Column(String,unique=True, nullable=False)

