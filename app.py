# app.py
import streamlit as st
from utils import (extract_text_from_pdf, calculate_match_score,
                   skill_gap, check_sections)

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer & Job Match Scorer")
st.write("Upload your resume and paste a job description to see how well you match.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste the job description here", height=250)

if st.button("Analyze"):
    if uploaded_file is None or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error("Could not read text from this PDF. It may be a scanned image.")
        else:
            text_score = calculate_match_score(resume_text, jd_text)
            matched, missing, skill_score = skill_gap(resume_text, jd_text)
            final_score = round(0.4 * text_score + 0.6 * skill_score, 2)

            st.subheader("Overall Match Score")
            st.progress(min(int(final_score), 100))
            st.metric("Match", f"{final_score}%")

            col1, col2 = st.columns(2)
            col1.metric("Text similarity", f"{text_score}%")
            col2.metric("Skill match", f"{skill_score}%")

            st.subheader("✅ Matched Skills")
            st.write(", ".join(matched) if matched else "No matching skills found.")

            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "You cover all required skills!")

            st.subheader("📑 Resume Sections")
            sections = check_sections(resume_text)
            for name, present in sections.items():
                st.write(f"{'✅' if present else '⚠️'} {name.title()}")

            report = (
                f"RESUME ANALYSIS REPORT\n"
                f"Overall Match: {final_score}%\n"
                f"Text Similarity: {text_score}%\n"
                f"Skill Match: {skill_score}%\n\n"
                f"Matched Skills: {', '.join(matched)}\n"
                f"Missing Skills: {', '.join(missing)}\n"
            )
            st.download_button("Download Report", report, file_name="report.txt")