def calculate_ats_score(resume_text, job_role):
    score = 0

    resume_text = resume_text.lower()
    job_role = job_role.lower()

    important_sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    action_words = [
        "developed",
        "created",
        "built",
        "managed",
        "designed",
        "implemented",
        "improved",
        "analyzed"
    ]

    technical_keywords = [
        "python",
        "javascript",
        "html",
        "css",
        "react",
        "api",
        "database",
        "sql",
        "git",
        "github",
        "machine learning",
        "ai"
    ]

    # Check job role keyword
    if job_role in resume_text:
        score += 15

    # Check important resume sections
    for section in important_sections:
        if section in resume_text:
            score += 8

    # Check action words
    for word in action_words:
        if word in resume_text:
            score += 3

    # Check technical keywords
    for keyword in technical_keywords:
        if keyword in resume_text:
            score += 3

    # Resume length check
    word_count = len(resume_text.split())

    if word_count >= 300:
        score += 10
    elif word_count >= 150:
        score += 5

    if score > 100:
        score = 100

    return score


def get_ats_feedback(score):
    if score >= 85:
        return "Excellent resume. It is highly ATS-friendly."
    elif score >= 70:
        return "Good resume. Some improvements can make it stronger."
    elif score >= 50:
        return "Average resume. It needs better keywords and structure."
    else:
        return "Weak resume. Improve formatting, skills, keywords, and sections."