"""
ai_utils.py — AI integration for resume analysis.
Supports OpenAI and Gemini APIs with a dynamic keyword-based fallback.
API key loaded from st.secrets first, then os.getenv.
"""

import os
import json
import re
import streamlit as st
from typing import Dict, Any

from scoring import (
    extract_skills,
    extract_job_skills,
    calculate_job_match,
    calculate_ats_score,
    get_ats_feedback,
    ROLE_SKILLS,
)


# ─────────────────────────────────────────────
# API KEY LOADING
# ─────────────────────────────────────────────

def _get_api_key(name: str) -> str:
    """Load API key from st.secrets first, then environment variables."""
    try:
        val = st.secrets.get(name, "")
        if val:
            return val
    except Exception:
        pass
    return os.getenv(name, "")


OPENAI_API_KEY = _get_api_key("OPENAI_API_KEY")
GEMINI_API_KEY = _get_api_key("GEMINI_API_KEY")

# Determine which API to use
USE_OPENAI = bool(OPENAI_API_KEY)
USE_GEMINI = bool(GEMINI_API_KEY) and not USE_OPENAI


def get_api_status() -> Dict[str, Any]:
    """Return API availability status for display in sidebar."""
    return {
        "openai_available": USE_OPENAI,
        "gemini_available": USE_GEMINI,
        "api_available": USE_OPENAI or USE_GEMINI,
        "provider": "OpenAI" if USE_OPENAI else ("Gemini" if USE_GEMINI else "None"),
    }


# ─────────────────────────────────────────────
# AI PROMPT BUILDER
# ─────────────────────────────────────────────

def build_prompt(resume_text: str, job_description: str, role: str) -> str:
    """
    Build a structured prompt that forces the AI to analyze THIS specific resume
    and return a JSON object with dynamic, resume-specific values.
    """
    return f"""You are an expert ATS Resume Analyzer and career coach.

IMPORTANT INSTRUCTIONS:
- Analyze ONLY the resume text provided below — do NOT use generic or placeholder content.
- Every score, skill, and suggestion must be based on EVIDENCE from the actual resume text.
- Do NOT return the same output for every resume. Your output MUST reflect the specific candidate.
- Return ONLY valid JSON, no explanation text before or after.

RESUME TEXT:
\"\"\"
{resume_text[:6000]}
\"\"\"

TARGET JOB DESCRIPTION / ROLE:
\"\"\"
{job_description or f"General {role} role"}
\"\"\"

Analyze this specific resume and return ONLY this JSON structure (no markdown, no backticks):
{{
  "candidate_summary": "2-3 sentence summary of THIS specific candidate based on their actual resume",
  "extracted_skills": ["list", "of", "skills", "ACTUALLY", "found", "in", "this", "resume"],
  "strengths": ["3-5 specific strengths with EVIDENCE from the resume text"],
  "weaknesses": ["2-4 specific weaknesses or gaps observed in THIS resume"],
  "job_match_percentage": <integer 0-100 based on skill overlap with job description>,
  "ats_score": <integer 0-100 based on resume structure, keywords, sections>,
  "missing_skills": ["skills mentioned in job description but NOT found in this resume"],
  "improvement_suggestions": ["3-5 specific, actionable suggestions for THIS candidate"],
  "interview_questions": [
    "Technical question based on candidate's actual listed skills",
    "Technical question based on a missing skill they should learn",
    "Project-based question about a specific project mentioned in their resume",
    "Question probing a weakness or gap in their resume",
    "HR/soft-skills question relevant to their target role"
  ],
  "voice_feedback_text": "A 3-4 sentence encouraging but honest verbal summary of this candidate's resume for their target role"
}}

SCORING RULES:
- job_match_percentage: Count how many skills from the job description appear in the resume. Divide by total required skills. Adjust ±10 for experience level, project quality, education match. Do NOT default to 75.
- ats_score: Check for: contact info (+10), skills section (+20), education (+15), work experience/projects (+20), keyword density matching job description (+25), readability and action verbs (+10). Do NOT default to 75.
- missing_skills: Only list skills explicitly mentioned in the job description that are clearly absent from the resume.
- interview_questions: Make questions SPECIFIC to this candidate — reference their actual skills, projects, and gaps.
"""


# ─────────────────────────────────────────────
# OPENAI CALL
# ─────────────────────────────────────────────

def _call_openai(prompt: str) -> str:
    """Call OpenAI API and return raw response text."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use gpt-4o-mini — widely available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=2000,
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────────
# GEMINI CALL
# ─────────────────────────────────────────────

def _call_gemini(prompt: str) -> str:
    """Call Gemini API and return raw response text."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# ─────────────────────────────────────────────
# JSON PARSER WITH REPAIR
# ─────────────────────────────────────────────

def _parse_json_response(raw: str) -> Dict[str, Any]:
    """
    Safely parse JSON from AI response.
    Handles: markdown code fences, trailing commas, truncated JSON.
    """
    # Strip markdown code fences
    raw = raw.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    # Try direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON object
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not parse AI response as JSON")


# ─────────────────────────────────────────────
# DYNAMIC KEYWORD FALLBACK
# ─────────────────────────────────────────────

def _dynamic_fallback(
    resume_text: str,
    job_description: str,
    role: str,
    required_skills: list,
) -> Dict[str, Any]:
    """
    Fully dynamic fallback analysis using local keyword scoring.
    NEVER returns hardcoded values — everything is derived from resume + job desc.
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_job_skills(job_description) if job_description else required_skills

    match_pct, matched_skills, missing_skills = calculate_job_match(
        resume_skills, job_skills, resume_text, job_description
    )
    ats_score, ats_breakdown = calculate_ats_score(resume_text, job_description, job_skills)

    # Build dynamic strengths
    strengths = []
    if len(resume_skills) >= 8:
        strengths.append(f"Broad technical skill set with {len(resume_skills)} identified skills")
    if any(kw in resume_text.lower() for kw in ["project", "built", "developed", "created"]):
        strengths.append("Demonstrates hands-on project experience")
    if any(kw in resume_text.lower() for kw in ["bachelor", "master", "degree", "university"]):
        strengths.append("Formal academic education in a relevant field")
    if any(kw in resume_text.lower() for kw in ["internship", "experience", "worked"]):
        strengths.append("Has professional or internship experience")
    if len(matched_skills) > 0:
        strengths.append(f"Matches {len(matched_skills)} of {len(job_skills)} required skills for the role")
    if not strengths:
        strengths = ["Has foundational skills relevant to the field"]

    # Build dynamic weaknesses
    weaknesses = []
    if len(missing_skills) > 3:
        weaknesses.append(f"Missing {len(missing_skills)} key skills required for the {role} role")
    if not re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', resume_text):
        weaknesses.append("No email address detected — contact info may be missing")
    if len(resume_text.split()) < 300:
        weaknesses.append("Resume appears short — consider adding more detail to experience/projects")
    if not any(kw in resume_text.lower() for kw in ["project", "built", "developed"]):
        weaknesses.append("No clear project experience mentioned")
    if not weaknesses:
        weaknesses = ["Resume could benefit from more quantified achievements"]

    # Build interview questions based on actual skills and gaps
    interview_questions = []
    if matched_skills:
        interview_questions.append(
            f"Can you walk us through a project where you used {matched_skills[0]}?"
        )
    if len(matched_skills) > 1:
        interview_questions.append(
            f"How have you applied {matched_skills[1]} to solve a real-world problem?"
        )
    if missing_skills:
        interview_questions.append(
            f"The role requires {missing_skills[0]} — what is your experience with it, "
            f"and how quickly could you get up to speed?"
        )
    interview_questions.append(
        f"What interests you most about the {role} role and why are you the right fit?"
    )
    interview_questions.append(
        "Describe a challenging technical problem you solved and how you approached it."
    )

    # Voice feedback text
    match_word = "strong" if match_pct >= 70 else ("moderate" if match_pct >= 45 else "limited")
    voice_text = (
        f"Your resume shows a {match_word} match of {match_pct}% for the {role} role. "
        f"You have demonstrated skills in {', '.join(resume_skills[:4]) if resume_skills else 'various areas'}. "
        f"To improve your chances, focus on acquiring: {', '.join(missing_skills[:3]) if missing_skills else 'more advanced skills in your field'}. "
        f"Your ATS score is {ats_score} out of 100, which means your resume is "
        f"{'well-optimized' if ats_score >= 70 else 'needs optimization'} for applicant tracking systems."
    )

    return {
        "candidate_summary": (
            f"Candidate targeting the {role} role. "
            f"Resume contains {len(resume_skills)} identifiable technical skills including "
            f"{', '.join(resume_skills[:3]) if resume_skills else 'general competencies'}. "
            f"Resume text is approximately {len(resume_text.split())} words."
        ),
        "extracted_skills": resume_skills,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "job_match_percentage": match_pct,
        "ats_score": ats_score,
        "missing_skills": missing_skills[:10],
        "improvement_suggestions": [
            f"Add these missing skills to your resume: {', '.join(missing_skills[:3])}" if missing_skills else
            "Your skill set is well-aligned with the role — maintain it",
            "Quantify your achievements with numbers and metrics",
            "Add a professional summary at the top of your resume",
            "Ensure contact information (email, phone, LinkedIn) is clearly visible",
            "Use strong action verbs like 'Developed', 'Implemented', 'Led' in bullet points",
        ],
        "interview_questions": interview_questions,
        "voice_feedback_text": voice_text,
        "_used_fallback": True,
    }


# ─────────────────────────────────────────────
# MAIN ANALYSIS FUNCTION
# ─────────────────────────────────────────────

def analyze_resume(
    resume_text: str,
    job_description: str,
    role: str,
) -> Dict[str, Any]:
    """
    Main entry point for resume analysis.
    Tries AI API first; falls back to dynamic keyword analysis.
    Returns a structured dict — never the same for different resumes.
    """
    required_skills = ROLE_SKILLS.get(role, [])

    # Build effective job description for analysis
    effective_job_desc = job_description.strip()
    if not effective_job_desc and required_skills:
        effective_job_desc = (
            f"Looking for a {role} with skills in: " + ", ".join(required_skills)
        )

    # Try AI API
    if USE_OPENAI or USE_GEMINI:
        try:
            prompt = build_prompt(resume_text, effective_job_desc, role)

            if USE_OPENAI:
                raw_response = _call_openai(prompt)
            else:
                raw_response = _call_gemini(prompt)

            result = _parse_json_response(raw_response)

            # Validate essential fields exist
            required_fields = [
                "candidate_summary", "extracted_skills", "job_match_percentage",
                "ats_score", "missing_skills",
            ]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing field in AI response: {field}")

            # Ensure numeric types
            result["job_match_percentage"] = int(result.get("job_match_percentage", 0))
            result["ats_score"] = int(result.get("ats_score", 0))
            result["_used_fallback"] = False
            return result

        except Exception as e:
            st.warning(
                f"⚠️ AI API call failed ({str(e)[:80]}). "
                f"Using dynamic keyword analysis as fallback. "
                f"Results are still based on your actual resume content."
            )

    # Dynamic fallback (also used when no API key is configured)
    if not USE_OPENAI and not USE_GEMINI:
        st.info(
            "ℹ️ No API key configured. "
            "Running dynamic keyword-based analysis on your resume."
        )

    return _dynamic_fallback(resume_text, effective_job_desc, role, required_skills)