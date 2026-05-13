"""
app.py — AI Resume Analyzer — Smart ATS & Job Match Assistant
Complete Streamlit frontend with professional UI, all features integrated.
"""

import os
import streamlit as st
from datetime import datetime

from resume_parser import parse_resume
from ai_utils import analyze_resume, get_api_status
from scoring import (
    extract_skills, calculate_ats_score, calculate_job_match,
    get_ats_feedback, ROLE_SKILLS, extract_job_skills
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer — Smart ATS & Job Match",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Gradient Header */
.hero-header {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero-header h1 {
    color: #ffffff;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero-header p {
    color: #c0c0e0;
    font-size: 1.05rem;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-top: 0.8rem;
    backdrop-filter: blur(4px);
}

/* Feature cards row */
.feature-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.feature-card {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    color: #e0e0f0;
}
.feature-card .icon { font-size: 1.6rem; margin-bottom: 6px; }
.feature-card .label { font-size: 0.78rem; font-weight: 500; color: #a0a0c0; }

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 1.5rem 0;
}
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3);
}
.metric-card.green { background: linear-gradient(135deg, #11998e, #38ef7d); }
.metric-card.orange { background: linear-gradient(135deg, #f7971e, #ffd200); }
.metric-card.red { background: linear-gradient(135deg, #eb3349, #f45c43); }
.metric-card.blue { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
.metric-val { font-size: 2rem; font-weight: 700; line-height: 1; }
.metric-lbl { font-size: 0.75rem; opacity: 0.9; margin-top: 4px; font-weight: 500; }

/* Skill badges */
.skill-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px;
    font-weight: 500;
}
.skill-badge-missing {
    display: inline-block;
    background: linear-gradient(135deg, #eb3349, #f45c43);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px;
    font-weight: 500;
}
.skill-badge-matched {
    display: inline-block;
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px;
    font-weight: 500;
}

/* Progress bar wrapper */
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 4px;
    color: #374151;
}

/* Section headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    border-left: 4px solid #667eea;
    padding-left: 10px;
    margin: 1.2rem 0 0.8rem 0;
}

/* Analyze button */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29, #302b63) !important;
}
section[data-testid="stSidebar"] * {
    color: #e0e0f0 !important;
}

/* Note box */
.note-box {
    background: rgba(102,126,234,0.1);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.83rem;
    color: #4b5563;
    margin-top: 0.8rem;
}

/* Voice / feedback card */
.feedback-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-size: 1rem;
    line-height: 1.7;
    color: #e0e0f0;
    font-style: italic;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f3f4f6;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 AI Resume Analyzer")
    st.markdown("**Smart ATS & Job Match Assistant**")
    st.markdown("---")

    st.markdown("### 📋 How to Use")
    st.markdown("""
1. Upload your resume (PDF/DOCX/TXT)
2. Paste a job description **or** select a role
3. Click **Analyze Resume**
4. View your complete analysis!
    """)
    st.markdown("---")

    # API Status
    st.markdown("### ⚡ API Status")
    api_status = get_api_status()
    if api_status["api_available"]:
        st.success("✅ Groq API connected")
    else:
        st.warning("⚠️ No API key found — using fallback analysis")

    st.markdown("---")
    st.markdown("### 📁 Supported Formats")
    st.markdown("📄 PDF &nbsp;|&nbsp; 📝 DOCX &nbsp;|&nbsp; 📃 TXT")
    st.markdown("---")
    st.markdown("### 🏆 Features")
    st.markdown("""
- ✅ Skill Extraction
- ✅ Job Match %
- ✅ ATS Score
- ✅ Missing Skills
- ✅ Interview Questions
- ✅ AI Feedback Summary
- ✅ Download Report
    """)
    st.markdown("---")
    st.caption("💡 Scores are AI + keyword based and reflect actual resume content.")


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🚀 AI Resume Analyzer</h1>
    <p>Smart ATS Scoring · Job Match Analysis · Interview Prep · AI Feedback</p>
    <span class="hero-badge">✨ Powered by AI — Dynamic Analysis for Every Resume</span>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="feature-row">
    <div class="feature-card"><div class="icon">🎯</div><div class="label">Job Match %</div></div>
    <div class="feature-card"><div class="icon">🤖</div><div class="label">ATS Score</div></div>
    <div class="feature-card"><div class="icon">🧠</div><div class="label">Skill Analysis</div></div>
    <div class="feature-card"><div class="icon">❓</div><div class="label">Interview Prep</div></div>
    <div class="feature-card"><div class="icon">💡</div><div class="label">AI Feedback</div></div>
    <div class="feature-card"><div class="icon">📥</div><div class="label">Download Report</div></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Drop your resume here",
        type=["pdf", "docx", "txt"],
        help="Supports PDF, DOCX, and TXT formats",
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}**  ({round(uploaded_file.size/1024, 1)} KB)")

with col_right:
    st.markdown("### 🎯 Target Role")
    role_options = list(ROLE_SKILLS.keys())
    selected_role = st.selectbox(
        "Select role",
        role_options,
        index=0,
        label_visibility="collapsed",
    )

st.markdown("### 📋 Job Description *(optional but recommended)*")
job_description = st.text_area(
    "Paste the full job description here for precise analysis",
    height=160,
    placeholder="Paste job description here for accurate match scoring...\n\nLeave empty to use default requirements for the selected role.",
    label_visibility="collapsed",
)

if not job_description.strip():
    if selected_role != "Custom":
        req_skills = ROLE_SKILLS.get(selected_role, [])
        st.markdown(
            f'<div class="note-box">ℹ️ No job description provided. '
            f'Analysis will use default <strong>{selected_role}</strong> requirements: '
            f'{", ".join(req_skills[:6])}{"..." if len(req_skills) > 6 else ""}.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="note-box">⚠️ Custom role selected with no job description. '
            'Please paste a job description for accurate results.</div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True)

# ─────────────────────────────────────────────
# ANALYSIS & RESULTS
# ─────────────────────────────────────────────
if analyze_btn:
    # Validate inputs
    if uploaded_file is None:
        st.error("❌ Please upload a resume file (PDF, DOCX, or TXT).")
        st.stop()
    if selected_role == "Custom" and not job_description.strip():
        st.error("❌ For Custom role, please paste a job description.")
        st.stop()

    # ── 1. Parse resume ──────────────────────────────
    with st.spinner("📄 Extracting text from your resume..."):
        try:
            resume_text = parse_resume(uploaded_file)
        except RuntimeError as e:
            st.error(f"❌ {str(e)}")
            st.stop()

    # ── 2. Run AI analysis ───────────────────────────
    with st.spinner("🤖 Analyzing your resume with AI..."):
        result = analyze_resume(resume_text, job_description, selected_role)

    st.success("✅ Analysis complete!")
    st.markdown("---")

    # ── 3. Metric Cards ──────────────────────────────
    match_pct    = result.get("job_match_percentage", 0)
    ats_score    = result.get("ats_score", 0)
    skills_found = len(result.get("extracted_skills", []))
    missing_count = len(result.get("missing_skills", []))

    def metric_color(val):
        if val >= 75: return "green"
        if val >= 50: return "orange"
        return "red"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card {metric_color(match_pct)}">
            <div class="metric-val">{match_pct}%</div>
            <div class="metric-lbl">🎯 Job Match</div>
        </div>
        <div class="metric-card {metric_color(ats_score)}">
            <div class="metric-val">{ats_score}</div>
            <div class="metric-lbl">🤖 ATS Score /100</div>
        </div>
        <div class="metric-card blue">
            <div class="metric-val">{skills_found}</div>
            <div class="metric-lbl">🧠 Skills Found</div>
        </div>
        <div class="metric-card {"red" if missing_count > 5 else "orange" if missing_count > 2 else "green"}">
            <div class="metric-val">{missing_count}</div>
            <div class="metric-lbl">⚠️ Missing Skills</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bars
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f'<div class="progress-label"><span>🎯 Job Match</span><span>{match_pct}%</span></div>', unsafe_allow_html=True)
        st.progress(match_pct / 100)
    with col_p2:
        st.markdown(f'<div class="progress-label"><span>🤖 ATS Score</span><span>{ats_score}/100</span></div>', unsafe_allow_html=True)
        st.progress(ats_score / 100)

    # ATS feedback banner
    st.markdown(f"> {get_ats_feedback(ats_score)}")
    st.markdown("---")

    # ── 4. TABS ──────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Summary",
        "🧠 Skills Analysis",
        "🤖 ATS Report",
        "⚠️ Missing Skills",
        "❓ Interview Questions",
        "📄 Text Preview",
    ])

    # ── TAB 1: SUMMARY ───────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">👤 Candidate Summary</div>', unsafe_allow_html=True)
        st.markdown(result.get("candidate_summary", "—"))

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown('<div class="section-header">💪 Strengths</div>', unsafe_allow_html=True)
            for s in result.get("strengths", []):
                st.markdown(f"✅ {s}")
        with col_s2:
            st.markdown('<div class="section-header">🔧 Weaknesses / Gaps</div>', unsafe_allow_html=True)
            for w in result.get("weaknesses", []):
                st.markdown(f"⚠️ {w}")

        st.markdown('<div class="section-header">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
        for i, suggestion in enumerate(result.get("improvement_suggestions", []), 1):
            st.markdown(f"**{i}.** {suggestion}")

        # AI Feedback Summary (replaces voice)
        voice_text = result.get("voice_feedback_text", "")
        if voice_text:
            st.markdown('<div class="section-header">🗣️ AI Feedback Summary</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="feedback-card">{voice_text}</div>',
                unsafe_allow_html=True,
            )

        if result.get("_used_fallback"):
            st.caption("ℹ️ Analysis performed using keyword-based engine (API unavailable).")
        elif result.get("_model_used"):
            st.caption(f"✨ Analysis powered by AI model: `{result['_model_used']}`")

        # Developer expandable section for API debugging
        with st.expander("🔧 Developer Details", expanded=False):
            if result.get("_model_used"):
                st.markdown(f"**Model used:** `{result['_model_used']}`")
            if result.get("_used_fallback"):
                st.markdown("**Mode:** Local keyword-based fallback")
            if st.session_state.get("_api_errors_log"):
                st.markdown("**API attempt log:**")
                for log_entry in st.session_state["_api_errors_log"]:
                    st.code(log_entry, language="text")
            if st.session_state.get("_api_error_detail"):
                st.markdown("**Last error traceback:**")
                st.code(st.session_state["_api_error_detail"], language="text")

    # ── TAB 2: SKILLS ANALYSIS ───────────────────────
    with tab2:
        extracted_skills = result.get("extracted_skills", [])
        required_skills  = ROLE_SKILLS.get(selected_role, [])
        if job_description.strip():
            required_skills = extract_job_skills(job_description) or required_skills

        matched_skills   = [s for s in extracted_skills if s.lower() in {r.lower() for r in required_skills}]
        unmatched_skills = [s for s in extracted_skills if s.lower() not in {r.lower() for r in required_skills}]

        st.markdown('<div class="section-header">✅ Matched Skills (in resume & job)</div>', unsafe_allow_html=True)
        if matched_skills:
            badges = "".join(f'<span class="skill-badge-matched">{s}</span>' for s in matched_skills)
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No direct skill matches found against the job description.")

        st.markdown('<div class="section-header">🧠 All Extracted Skills</div>', unsafe_allow_html=True)
        if extracted_skills:
            badges = "".join(f'<span class="skill-badge">{s}</span>' for s in extracted_skills)
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.warning("No recognizable skills found in the resume.")

        if unmatched_skills:
            st.markdown('<div class="section-header">➕ Other Skills (not in job desc)</div>', unsafe_allow_html=True)
            badges = "".join(
                f'<span class="skill-badge" style="background:linear-gradient(135deg,#4b6cb7,#182848)">{s}</span>'
                for s in unmatched_skills
            )
            st.markdown(badges, unsafe_allow_html=True)

    # ── TAB 3: ATS REPORT ────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🤖 ATS Score Breakdown</div>', unsafe_allow_html=True)
        req_skills_for_ats = ROLE_SKILLS.get(selected_role, [])
        _, ats_breakdown = calculate_ats_score(resume_text, job_description, req_skills_for_ats)

        max_scores = {
            "Contact Information": 10,
            "Skills Section": 20,
            "Education": 15,
            "Experience/Projects": 20,
            "Keyword Match": 25,
            "Readability/Formatting": 10,
        }

        for category, score in ats_breakdown.items():
            max_s = max_scores.get(category, 10)
            pct = score / max_s if max_s > 0 else 0
            emoji = "🟢" if pct >= 0.7 else ("🟡" if pct >= 0.4 else "🔴")
            st.markdown(f"**{emoji} {category}** &nbsp; `{score}/{max_s}`")
            st.progress(pct)

        st.markdown("---")
        st.markdown(f"**Total ATS Score: `{ats_score}/100`**")
        st.markdown(f"> {get_ats_feedback(ats_score)}")
        st.markdown(
            '<div class="note-box">💡 ATS scores are estimated based on keyword coverage, '
            'resume structure, and content quality. Actual recruiter ATS systems may vary.</div>',
            unsafe_allow_html=True,
        )

    # ── TAB 4: MISSING SKILLS ────────────────────────
    with tab4:
        missing_skills = result.get("missing_skills", [])
        st.markdown('<div class="section-header">⚠️ Skills to Add for This Role</div>', unsafe_allow_html=True)

        if missing_skills:
            badges = "".join(f'<span class="skill-badge-missing">{s}</span>' for s in missing_skills)
            st.markdown(badges, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**📚 Learning Resources:**")
            for skill in missing_skills[:5]:
                query = skill.replace(" ", "+")
                st.markdown(
                    f"- **{skill}**: "
                    f"[YouTube](https://youtube.com/results?search_query={query}+tutorial) · "
                    f"[Coursera](https://coursera.org/search?query={query}) · "
                    f"[Docs](https://google.com/search?q={query}+official+docs)"
                )
        else:
            st.success("🎉 Great! Your resume covers all the key skills for this role!")

    # ── TAB 5: INTERVIEW QUESTIONS ───────────────────
    with tab5:
        st.markdown('<div class="section-header">❓ Personalized Interview Questions</div>', unsafe_allow_html=True)
        questions = result.get("interview_questions", [])

        q_types = ["💻 Technical", "🔬 Technical (Advanced)", "🗂️ Project-Based", "📖 Skill Gap", "🤝 HR / Behavioral"]
        for i, question in enumerate(questions):
            q_label = q_types[i] if i < len(q_types) else f"Q{i+1}"
            with st.expander(f"{q_label}: {question[:80]}{'...' if len(question) > 80 else ''}", expanded=(i == 0)):
                st.markdown(f"**{question}**")
                st.caption("Prepare a structured answer using the STAR method: Situation → Task → Action → Result")

    # ── TAB 6: EXTRACTED TEXT PREVIEW ────────────────
    with tab6:
        st.markdown('<div class="section-header">📄 Extracted Resume Text</div>', unsafe_allow_html=True)
        st.caption(f"Total extracted: **{len(resume_text.split())} words**, {len(resume_text)} characters")
        st.markdown("<br>", unsafe_allow_html=True)
        st.text_area(
            "Full extracted text",
            value=resume_text,
            height=400,
            label_visibility="collapsed",
        )
        st.caption("ℹ️ This is the raw text extracted from your resume file. Verify it looks correct — if it appears garbled, your PDF may be image-based (not supported).")

    # ── 5. DOWNLOAD REPORT ───────────────────────────
    st.markdown("---")
    st.markdown("### 📥 Download Full Report")

    report_lines = [
        "=" * 60,
        "  AI RESUME ANALYZER — FULL ANALYSIS REPORT",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"  Target Role: {selected_role}",
        "=" * 60,
        "",
        "CANDIDATE SUMMARY",
        "-" * 40,
        result.get("candidate_summary", "—"),
        "",
        "SCORES",
        "-" * 40,
        f"  Job Match Percentage : {match_pct}%",
        f"  ATS Score            : {ats_score}/100",
        f"  Skills Found         : {skills_found}",
        f"  Missing Skills       : {missing_count}",
        "",
        "EXTRACTED SKILLS",
        "-" * 40,
        ", ".join(result.get("extracted_skills", [])) or "None identified",
        "",
        "STRENGTHS",
        "-" * 40,
        *[f"  + {s}" for s in result.get("strengths", [])],
        "",
        "WEAKNESSES / GAPS",
        "-" * 40,
        *[f"  - {w}" for w in result.get("weaknesses", [])],
        "",
        "MISSING SKILLS",
        "-" * 40,
        ", ".join(result.get("missing_skills", [])) or "None",
        "",
        "IMPROVEMENT SUGGESTIONS",
        "-" * 40,
        *[f"  {i+1}. {s}" for i, s in enumerate(result.get("improvement_suggestions", []))],
        "",
        "INTERVIEW QUESTIONS",
        "-" * 40,
        *[f"  Q{i+1}. {q}" for i, q in enumerate(result.get("interview_questions", []))],
        "",
        "AI FEEDBACK SUMMARY",
        "-" * 40,
        result.get("voice_feedback_text", "—"),
        "",
        "=" * 60,
        "  Note: Scores are estimated using AI + keyword matching.",
        "  Results reflect actual resume content analysis.",
        "=" * 60,
    ]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="📥 Download Report as TXT",
        data=report_text,
        file_name=f"resume_analysis_{selected_role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown(
        '<div class="note-box">📌 <strong>Demo Note:</strong> '
        'Scores are estimated using AI + keyword matching and reflect actual resume content. '
        'Results will differ for every uploaded CV.</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#9ca3af;font-size:0.8rem;">'
    '🚀 AI Resume Analyzer · Built with Streamlit + Groq AI · '
    'Smart ATS & Job Match Assistant'
    '</div>',
    unsafe_allow_html=True,
)