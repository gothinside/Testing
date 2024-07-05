from sqlalchemy import Column,Table, Integer, String, Date
from .database import Base

class Users(Base):
    Id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)

