import streamlit as st
from utils import extract_text_from_pdf, detect_sections
from model import analyze_cv, predict_score, cv_level, cv_feedback, final_score

st.set_page_config(page_title="AI CV Analyzer", layout="wide")

st.title("📄 AI CV Analyzer Pro")

uploaded_file = st.file_uploader("CV yükle (PDF)", type=["pdf"])

if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)
    sections = detect_sections(text)

    analysis = analyze_cv(sections)

    ml_score = predict_score(text)
    final = final_score(analysis)
    level = cv_level(final)

    # ================= LEFT PANEL =================
    col1, col2 = st.columns([1, 2])

    with col1:

        st.subheader("📊 CV Score")
        st.metric("Final Score", f"{final}/100")
        st.metric("ML Score", f"{ml_score}/100")

        st.subheader("🏆 Level")
        st.success(level)

        st.subheader("🛠️ Skills")
        st.write(", ".join(analysis["skills_found"]) if analysis["skills_found"] else "Bulunamadı")

    # ================= RIGHT PANEL =================
    with col2:

        st.subheader("💼 Experience Summary")

        if analysis["experience_summary"]:
            for i, item in enumerate(analysis["experience_summary"], 1):
                st.markdown(f"**{i}.** {item}")
        else:
            st.info("Deneyim bulunamadı")

        st.subheader("📌 Sections Overview")

        st.markdown(f"""
        - 🎓 Education: {len(sections['education'])} satır
        - 💼 Experience: {len(sections['experience'])} satır
        - 🛠️ Skills: {len(sections['skills'])} satır
        - 📁 Projects: {len(sections['projects'])} satır
        """)

    # ================= FEEDBACK =================
    st.divider()
    st.subheader("💡 CV Improvement Suggestions")

    tips = cv_feedback(sections, analysis)

    if tips:
        for tip in tips:
            st.warning("⚠️ " + tip)
    else:
        st.success("CV iyi görünüyor!")

    # ================= RAW CV =================
    with st.expander("📄 Raw CV Text (debug)"):
        st.text_area("CV", text, height=400)