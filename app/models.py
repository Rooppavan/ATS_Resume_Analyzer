from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    
class ResumeAnalysis(Base):
    
    __tablename__ = "resume_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    filename = Column(String)
    
    ats_score = Column(Integer)
    
    matched_skills = Column(String)
    
    missing_skills = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    