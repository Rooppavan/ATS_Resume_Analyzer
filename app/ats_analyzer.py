import re

SECTIONS = [
    "experience",
    "projects",
    'education',
    "skills",
    "certifications"
]

ACTION_WORDS = [

    "developed",
    "designed",
    "implemented",
    "optimized",
    "created",
    "built",
    "improved",
    "managed",
    "led"
]

WEAK_PHRASES = {

    "worked on": [
        "developed",
        "implemented",
        "engineered"
    ],

    "helped": [
        "collaborated",
        "contributed",
        "supported"
    ],

    "responsible for": [
        "managed",
        "led",
        "executed"
    ],

    "made": [
        "built",
        "created",
        "developed"
    ]
}

def analyze_resume(resume_text, job_description):
    
    resume_text = resume_text.lower()
    
    resume_words = set(resume_text.lower().split())
    
    matched_keywords = []
    
    job_match_score = 0
    
    job_description_words = set()
    
    if job_description.strip():
        
        job_description_words = set(job_description.lower().split())
        
        matched_keywords = list(resume_words.intersection(job_description_words))
        
        if len(job_description_words) > 0:
            job_match_score = int(
            (
                len(matched_keywords)
                /
                len(job_description_words)
            ) * 100
        )
            
    
    detected_sections = []
    
    suggestions = []
    
    strengths = []
    
    ai_rewrite_suggestions = []
    
    ats_score = 0
            
    for section in SECTIONS:
        
        if section.lower() in resume_text:
            detected_sections.append(section)  
    
    word_count = len(resume_text.split())        
    
    if word_count < 250:
        
        suggestions.append("Resume content is too short")
        
    elif word_count > 1200:
        suggestions.append("Resume is too lengthy")
        
    else:
        strengths.append("Good Resume length")
        
        
    action_word_count = 0
    
    for word in ACTION_WORDS:
        
        if word in resume_text:
            action_word_count+= 1
        
    if action_word_count <3:
        suggestions.append("Use more strong action verbs")
        
    else:
        strengths.append("Good use of action verbs")
    
    metrics = re.findall(r'\d+%|\d+\s',resume_text)
    
    if len(metrics) < 2:
        suggestions.append("Add measurable achievements")
    
    else:
        strengths.append("Good quntified achievements")
    
    if "github" not in resume_text:
        suggestions.append("Add Github profile link")
        
    else:
        strengths.append("Github profile detected")
    
    if "linkedin" not in resume_text:
        suggestions.append("Add LinkedIn profile link")
    
    else:
        strengths.append("LinkedIn profile detected")
    
    if "projects" not in detected_sections:
        suggestions.append("Add Projects section")
        
    if "certifications" not in detected_sections:
        suggestions.append("Add certification section")
        
    for weak_phrase, strong_words in WEAK_PHRASES.items():
        
        if weak_phrase in resume_text:
            ai_rewrite_suggestions.append(f'Try replacing "{weak_phrase}" with stronger action words like: {", ".join(strong_words)}')
  
    ats_score +=(len(detected_sections)/ len(SECTIONS)) * 30
    
    if word_count >= 250 and word_count <= 1200:
        ats_score += 15
    
    if action_word_count >= 3:
        ats_score += 20
    
    if len(metrics) >= 2:
        
        ats_score += 20
    
    if "github" in resume_text:
        
        ats_score += 7
    
    if "linkedin" in resume_text:
        
        ats_score += 8
    
    ats_score = int(ats_score)
    
    if ats_score >= 80:
        ai_verdict = ("Excellent resume with strong ATS alignment.")
    elif ats_score >= 65:
        ai_verdict = ("Good resume with a few areas for imporvements.")
    elif ats_score >= 50:
        ai_verdict = ("Average resume. Improve projects and achievements.")
    else:
        ai_verdict = ("Resume needs major improvements for ATS optimization.")    
    return{
        "ats_score": ats_score,
        "job_match_score": job_match_score,
        "matched_keywords": matched_keywords[:20],
        "detected_sections": detected_sections,
        "suggestions": suggestions,
        "strengths" : strengths,
        "ai_rewrite_suggestions" : ai_rewrite_suggestions,
        "ai_verdict": ai_verdict
    }