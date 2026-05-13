def get_fallback_response(job_role):

    return f"""
# ATS Resume Analysis

## ATS Score
75/100

## Strengths
- Resume structure is clean
- Relevant technical skills mentioned
- Good project experience
- Proper formatting

## Weaknesses
- Resume lacks measurable achievements
- Some sections are too short
- Missing strong action verbs

## Missing Skills
For the role of {job_role}, consider adding:
- Problem Solving
- Team Collaboration
- API Integration
- Deployment Skills
- Git/GitHub

## Improvement Suggestions
- Add quantified achievements
- Improve project descriptions
- Add certifications if available
- Optimize keywords for ATS systems

## Final Verdict
This resume has a solid foundation but needs optimization for better ATS ranking and recruiter impact.
"""