"""
scoring.py — Dynamic skill extraction, ATS scoring, and job match calculation.
All scores are computed from actual resume content — never hardcoded.
"""

import re
from typing import List, Dict, Tuple


# ─────────────────────────────────────────────
# SKILL DICTIONARY (50+ skills, 8 categories)
# ─────────────────────────────────────────────

SKILL_CATEGORIES: Dict[str, List[str]] = {
    "Programming Languages": [
        "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript",
        "Ruby", "Go", "Rust", "Kotlin", "Swift", "PHP", "Scala", "R",
        "MATLAB", "Perl", "Bash", "Shell", "SQL",
    ],
    "Web & Frameworks": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js",
        "Streamlit", "Flask", "FastAPI", "Django", "Express.js",
        "REST API", "GraphQL", "Spring Boot", "Laravel",
    ],
    "AI / ML / Data": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
        "PyTorch", "Keras", "OpenCV", "Hugging Face", "LangChain",
        "Data Analysis", "Data Science", "Statistics", "Matplotlib", "Seaborn",
        "Tableau", "Power BI", "Jupyter",
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Firebase", "SQLite",
        "Redis", "Oracle", "DynamoDB", "Cassandra", "Elasticsearch",
    ],
    "DevOps & Cloud": [
        "Git", "GitHub", "Docker", "Kubernetes", "Linux", "AWS",
        "Azure", "GCP", "CI/CD", "Jenkins", "Terraform", "Ansible",
        "Heroku", "Vercel", "Nginx",
    ],
    "Cybersecurity": [
        "OWASP", "Burp Suite", "Penetration Testing", "Vulnerability Assessment",
        "API Security", "Network Security", "Kali Linux", "Metasploit",
        "Wireshark", "Nmap", "Ethical Hacking", "Cryptography", "Firewalls",
        "Incident Response", "SIEM",
    ],
    "Mobile": [
        "Android", "iOS", "React Native", "Flutter", "Kotlin", "Swift",
    ],
    "Soft Skills": [
        "Communication", "Teamwork", "Problem Solving", "Leadership",
        "Critical Thinking", "Time Management", "Project Management",
        "Agile", "Scrum", "Presentation",
    ],
}

# Flatten all skills into one searchable list
ALL_SKILLS: List[str] = []
for skills in SKILL_CATEGORIES.values():
    ALL_SKILLS.extend(skills)

# Deduplicate (preserving order)
seen = set()
UNIQUE_SKILLS: List[str] = []
for s in ALL_SKILLS:
    if s.lower() not in seen:
        seen.add(s.lower())
        UNIQUE_SKILLS.append(s)


# ─────────────────────────────────────────────
# ROLE-BASED DEFAULT SKILL SETS
# ─────────────────────────────────────────────

ROLE_SKILLS: Dict[str, List[str]] = {
    "Software Engineer": [
        "Python", "Java", "JavaScript", "C++", "Git", "GitHub",
        "REST API", "SQL", "Docker", "Linux", "Agile", "Problem Solving",
    ],
    "AI/ML Engineer": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Scikit-learn", "Pandas", "NumPy", "NLP", "Data Science",
        "SQL", "Git", "Jupyter", "Matplotlib",
    ],
    "Data Analyst": [
        "Python", "SQL", "Pandas", "NumPy", "Tableau", "Power BI",
        "Excel", "Data Analysis", "Statistics", "Matplotlib", "Seaborn",
        "MySQL", "PostgreSQL", "Communication",
    ],
    "Python Developer": [
        "Python", "Flask", "Django", "FastAPI", "Streamlit", "REST API",
        "SQL", "PostgreSQL", "Git", "Docker", "Linux", "Pandas",
    ],
    "Cybersecurity Intern": [
        "Penetration Testing", "OWASP", "Burp Suite", "Kali Linux",
        "Network Security", "Vulnerability Assessment", "Nmap", "Wireshark",
        "Python", "Linux", "Ethical Hacking", "API Security",
    ],
    "Custom": [],
}


# ─────────────────────────────────────────────
# SKILL EXTRACTION
# ─────────────────────────────────────────────

def extract_skills(text: str, extra_skills: List[str] = None) -> List[str]:
    """
    Case-insensitively find all known skills present in the resume text.
    Returns deduplicated list of matched skill names (canonical casing).
    """
    text_lower = text.lower()
    found = []
    skill_pool = UNIQUE_SKILLS + (extra_skills or [])

    for skill in skill_pool:
        # Use word-boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            if skill not in found:
                found.append(skill)

    return found


def extract_job_skills(job_description: str) -> List[str]:
    """Extract skills mentioned in a job description."""
    return extract_skills(job_description)


# ─────────────────────────────────────────────
# JOB MATCH PERCENTAGE
# ─────────────────────────────────────────────

def calculate_job_match(
    resume_skills: List[str],
    required_skills: List[str],
    resume_text: str = "",
    job_description: str = "",
) -> Tuple[int, List[str], List[str]]:
    """
    Calculate job match percentage dynamically.
    Returns: (match_percentage, matched_skills, missing_skills)
    """
    if not required_skills:
        # No required skills defined — use resume length/richness heuristic
        base = min(50 + len(resume_skills) * 2, 75)
        return base, resume_skills, []

    resume_skills_lower = {s.lower() for s in resume_skills}
    matched = [s for s in required_skills if s.lower() in resume_skills_lower]
    missing = [s for s in required_skills if s.lower() not in resume_skills_lower]

    base_score = (len(matched) / len(required_skills)) * 100

    # Bonus points for resume richness
    bonus = 0
    text_lower = (resume_text + " " + job_description).lower()

    # Experience keywords
    experience_keywords = ["experience", "worked", "developed", "built", "designed", "implemented", "led"]
    bonus += sum(2 for kw in experience_keywords if kw in text_lower)

    # Education keywords
    education_keywords = ["bachelor", "master", "phd", "degree", "university", "college", "diploma"]
    bonus += sum(2 for kw in education_keywords if kw in text_lower)

    # Project keywords
    project_keywords = ["project", "deployed", "launched", "published", "github.com"]
    bonus += sum(2 for kw in project_keywords if kw in text_lower)

    # Certification keywords
    cert_keywords = ["certification", "certified", "certificate", "course", "udemy", "coursera"]
    bonus += sum(1 for kw in cert_keywords if kw in text_lower)

    final_score = min(int(base_score + bonus), 100)
    return final_score, matched, missing


# ─────────────────────────────────────────────
# ATS SCORE CALCULATION
# ─────────────────────────────────────────────

def calculate_ats_score(
    resume_text: str,
    job_description: str = "",
    required_skills: List[str] = None,
) -> Tuple[int, Dict[str, int]]:
    """
    Calculate ATS score (0-100) based on resume content.
    Returns: (total_score, breakdown_dict)

    Scoring breakdown:
    - Contact information:  10 points
    - Skills section found: 20 points
    - Education section:    15 points
    - Experience/Projects:  20 points
    - Job keyword match:    25 points
    - Readable text:        10 points
    Total:                 100 points
    """
    text_lower = resume_text.lower()
    breakdown = {}

    # 1. Contact Information (10 pts)
    contact_score = 0
    if re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text_lower):  # email
        contact_score += 4
    if re.search(r'(\+?\d[\d\s\-().]{7,}\d)', resume_text):   # phone
        contact_score += 3
    if any(kw in text_lower for kw in ["linkedin", "github", "portfolio", "website"]):
        contact_score += 3
    breakdown["Contact Information"] = min(contact_score, 10)

    # 2. Skills Section (20 pts)
    skills_score = 0
    if any(kw in text_lower for kw in ["skills", "technical skills", "core skills", "competencies"]):
        skills_score += 10
    found_skills = extract_skills(resume_text)
    skills_score += min(len(found_skills) * 2, 10)
    breakdown["Skills Section"] = min(skills_score, 20)

    # 3. Education Section (15 pts)
    edu_score = 0
    edu_keywords = ["education", "academic", "bachelor", "master", "phd", "degree",
                    "university", "college", "school", "diploma", "cgpa", "gpa"]
    hits = sum(1 for kw in edu_keywords if kw in text_lower)
    edu_score = min(hits * 3, 15)
    breakdown["Education"] = edu_score

    # 4. Experience / Projects (20 pts)
    exp_score = 0
    exp_keywords = ["experience", "work experience", "employment", "internship",
                    "project", "projects", "worked at", "developed", "built",
                    "implemented", "designed", "led", "managed"]
    hits = sum(1 for kw in exp_keywords if kw in text_lower)
    exp_score = min(hits * 2, 20)
    breakdown["Experience/Projects"] = exp_score

    # 5. Keyword / Job Match (25 pts)
    kw_score = 0
    if required_skills:
        matched = [s for s in required_skills if s.lower() in text_lower]
        ratio = len(matched) / len(required_skills)
        kw_score = int(ratio * 25)
    elif job_description:
        job_words = set(re.findall(r'\b\w{4,}\b', job_description.lower()))
        resume_words = set(re.findall(r'\b\w{4,}\b', text_lower))
        common = job_words & resume_words
        ratio = len(common) / max(len(job_words), 1)
        kw_score = min(int(ratio * 50), 25)
    else:
        # No job description — score based on general tech keywords
        tech_words = ["python", "sql", "git", "api", "data", "machine", "learning",
                      "web", "database", "framework", "algorithm", "cloud"]
        hits = sum(1 for kw in tech_words if kw in text_lower)
        kw_score = min(hits * 2, 20)
    breakdown["Keyword Match"] = kw_score

    # 6. Readability / Formatting (10 pts)
    read_score = 0
    word_count = len(resume_text.split())
    if word_count >= 400:
        read_score += 5
    elif word_count >= 200:
        read_score += 3
    elif word_count >= 100:
        read_score += 1
    # Check for action verbs
    action_verbs = ["developed", "created", "built", "managed", "designed",
                    "implemented", "improved", "analyzed", "led", "achieved"]
    hits = sum(1 for v in action_verbs if v in text_lower)
    read_score += min(hits, 5)
    breakdown["Readability/Formatting"] = min(read_score, 10)

    total = sum(breakdown.values())
    return min(total, 100), breakdown


def get_ats_feedback(score: int) -> str:
    """Return human-readable ATS feedback based on score."""
    if score >= 85:
        return "🟢 Excellent! Your resume is highly ATS-optimized and ready for top-tier applications."
    elif score >= 70:
        return "🟡 Good. Your resume is fairly ATS-friendly. A few targeted improvements will make it stronger."
    elif score >= 50:
        return "🟠 Average. Your resume needs better keyword coverage, sections, and structure."
    else:
        return "🔴 Weak ATS score. Improve formatting, add missing sections, include relevant keywords."
