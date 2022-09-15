from sqlalchemy import  Column, Integer, String

from .database import Base


class Userdetail(Base):
    __tablename__ = "userdetails"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150) , index = True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
