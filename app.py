import streamlit as st
from resume_utils import extract_text_from_pdf
from ai_utils import analyze_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI-based feedback.")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

job_role = st.text_input("Enter Target Job Role", placeholder="Example: Python Developer")

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
    elif job_role.strip() == "":
        st.error("Please enter a job role.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text.strip():
                st.error("Could not extract text from this PDF.")
            else:
                result = analyze_resume(resume_text, job_role)
                st.success("Analysis Complete!")
                st.markdown(result)