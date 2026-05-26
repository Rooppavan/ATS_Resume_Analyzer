from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import hash_password
from fastapi import HTTPException
from app.auth import(verify_password, create_access_token)
from fastapi import UploadFile, File
import shutil
from app.resume_parser import extract_resume_text
from app.ats_analyzer import analyze_resume
from app.models import (User, ResumeAnalysis)
from app.auth import verify_token

from app.database import get_db
from app.models import User
from app.schemas import UserSchema

router = APIRouter()

@router.get("/resume-history")
def get_resume_history(
    db: Session = Depends(get_db)
):

    resumes = db.query(
        ResumeAnalysis
    ).all()

    history = []

    for resume in resumes:

        history.append({
            "id": resume.id,
            "filename": resume.filename,
            "ats_score": resume.ats_score,
            "matched_skills": resume.matched_skills,
            "missing_skills": resume.missing_skills
        })

    return history

@router.post("/register")
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(username= user.username, email= user.email, password=hash_password(user.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return{
        "message": "User registered successfully"
    }
    
@router.post("/login")
def login_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user:
        raise HTTPException(status_code= 401, detail= "Invalid usename")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code= 401, detail= "Invalid password")
    
    access_token = create_access_token(data={ "sub": db_user.username})
    
    return{
        "accesstoken": access_token,
        "token_type": "bearer"
    }
    
@router.post("/Upload-Resume")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"app/uploads/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    resume_text = extract_resume_text(file_path)
    
    analysis_result = analyze_resume(resume_text)
    
    resume_record = ResumeAnalysis( filename = file.filename, ats_score = analysis_result["ats_score"], 
                                   matched_skills = ", ".join(analysis_result["matched_skills"]),
                                   missing_skills = ", ".join(analysis_result["missing_skills"]), user_id = 1)
    
    db.add(resume_record)
    
    db.commit()
    
    return{
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "analysis": analysis_result
    }    