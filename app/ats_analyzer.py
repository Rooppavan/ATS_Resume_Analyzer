SKILLS_DB = [
    "python",
    "fastapi",
    "docker",
    "sql",
    "postgresql",
    "redis",
    "kubernetes",
    "aws",
    "git",
    "linux",
    "react"
]


def analyze_resume(resume_text):
    
    resume_text = resume_text.lower()
    
    matched_skills = []
    
    missing_skills = []
    
    for skill in SKILLS_DB:
        
        if skill in resume_text:
            matched_skills.append(skill)
            
        else:
            missing_skills.append(skill)
            
    ats_score = int((len(matched_skills) / len(SKILLS_DB)) * 100)
    
    return{
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }