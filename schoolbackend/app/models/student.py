from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Student(Base):
    
    __tablename__ = "students"


    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False) 
    last_name = Column(String(100), nullable=False)
    last_name2 = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, index=True) 
