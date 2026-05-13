import os
from dotenv import load_dotenv
from openai import OpenAI
from fallback_data import get_fallback_response
from ats_utils import calculate_ats_score, get_ats_feedback
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, job_role):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze this resume for the role of {job_role}.

Give response in this format:

## ATS Score

## Strengths

## Weaknesses

## Missing Skills

## Improvement Suggestions

## Final Verdict

Resume:
{resume_text}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Error:", e)

        return get_fallback_response(job_role)