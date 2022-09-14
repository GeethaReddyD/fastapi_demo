from sqlalchemy import  Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150) , index = True)
    age = Column(Integer , index = True)
    location = Column(String , index = True)
