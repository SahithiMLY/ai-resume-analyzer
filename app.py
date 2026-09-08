import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import get_job_recommendations
from skill_gap import find_missing_skills
from roadmap_generator import generate_roadmap


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Resume Analyzer")

st.subheader(
    "Resume Analysis & Job Recommendation System"
)

st.write(
    "Upload your resume to identify skills, "
    "find suitable job roles, analyze skill gaps, "
    "and generate a personalized learning roadmap."
)


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "📤 Upload your Resume",
    type=["pdf", "docx"]
)


# =====================================================
# APPLICATION
# =====================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded successfully: {uploaded_file.name}"
    )

    # =================================================
    # RESUME EXTRACTION
    # =================================================

    with st.spinner(
        "🔍 Reading and analyzing your resume..."
    ):

        resume_text = extract_resume_text(
            uploaded_file
        )

    if not resume_text.strip():

        st.error(
            "❌ Could not extract text from the resume."
        )

        st.stop()


    # =================================================
    # TEXT CLEANING
    # =================================================

    cleaned_text = clean_text(
        resume_text
    )


    # =================================================
    # SKILL EXTRACTION
    # =================================================

    skills = extract_skills(
        cleaned_text
    )


    st.divider()

    st.header("📌 Extracted Skills")

    if skills:

        cols = st.columns(3)

        for index, skill in enumerate(skills):

            with cols[index % 3]:

                st.success(
                    f"✓ {skill}"
                )

    else:

        st.warning(
            "No skills were detected."
        )


    # =================================================
    # JOB RECOMMENDATIONS
    # =================================================

    st.divider()

    st.header("💼 Job Recommendations")

    recommendations = get_job_recommendations(
        cleaned_text
    )

    top_3 = recommendations[:3]


    # -------------------------------------------------
    # TOP 3 CARDS
    # -------------------------------------------------

    for index, recommendation in enumerate(top_3):

        role = recommendation["role"]
        score = recommendation["score"]

        if index == 0:
            medal = "🥇"
        elif index == 1:
            medal = "🥈"
        else:
            medal = "🥉"

        st.subheader(
            f"{medal} {role}"
        )

        st.progress(
            min(int(score), 100)
        )

        st.write(
            f"TF-IDF Match Score: **{score:.2f}%**"
        )


    # =================================================
    # JOB SCORE CHART
    # =================================================

    st.subheader("📊 Job Role Similarity")

    score_df = pd.DataFrame(
        recommendations
    )

    score_df["score"] = score_df["score"].round(2)

    fig = px.bar(
        score_df,
        x="score",
        y="role",
        orientation="h",
        title="Resume-to-Job Similarity",
        labels={
            "score": "Similarity (%)",
            "role": "Job Role"
        }
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =================================================
    # TARGET ROLE ANALYSIS
    # =================================================

    st.divider()

    st.header("🎯 Target Role Analysis")


    jobs = pd.read_csv(
        "data/job_roles.csv"
    )


    target_role = st.selectbox(
        "Select your target job role:",
        jobs["role"].tolist()
    )


    selected_job = jobs[
        jobs["role"] == target_role
    ].iloc[0]


    # -------------------------------------------------
    # TF-IDF SCORE
    # -------------------------------------------------

    tfidf_score = 0

    for recommendation in recommendations:

        if recommendation["role"] == target_role:

            tfidf_score = recommendation["score"]

            break


    # -------------------------------------------------
    # REQUIRED SKILLS
    # -------------------------------------------------

    required_skills = [
        skill.strip()
        for skill in selected_job["skills"].split(",")
    ]


    # -------------------------------------------------
    # SKILL GAP
    # -------------------------------------------------

    missing_skills = find_missing_skills(
        skills,
        required_skills
    )


    matched_skills = [
        skill
        for skill in required_skills
        if skill.lower()
        in {s.lower() for s in skills}
    ]


    # -------------------------------------------------
    # SKILL MATCH %
    # -------------------------------------------------

    if required_skills:

        skill_match_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        skill_match_score = 0


    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Skill Match",
            f"{skill_match_score:.1f}%"
        )


    with col2:

        st.metric(
            "TF-IDF Similarity",
            f"{tfidf_score:.2f}%"
        )


    with col3:

        st.metric(
            "Skills Matched",
            f"{len(matched_skills)}/{len(required_skills)}"
        )


    # =================================================
    # REQUIRED SKILLS
    # =================================================

    st.subheader("Required Skills")

    st.write(
        ", ".join(required_skills)
    )


    # =================================================
    # MATCHED SKILLS
    # =================================================

    st.subheader("✅ Matched Skills")

    if matched_skills:

        st.write(
            ", ".join(matched_skills)
        )

    else:

        st.info(
            "No required skills were detected."
        )


    # =================================================
    # MISSING SKILLS
    # =================================================

    st.divider()

    st.header("🧩 Skill Gap Analysis")


    if missing_skills:

        st.write(
            "Skills recommended for improving "
            "your readiness for this role:"
        )

        for skill in missing_skills:

            st.warning(
                f"❌ {skill}"
            )

    else:

        st.success(
            "🎉 You have all the required skills!"
        )


    # =================================================
    # SKILL MATCH CHART
    # =================================================

    st.subheader("📈 Target Role Skill Coverage")


    chart_data = pd.DataFrame({
        "Category": [
            "Matched Skills",
            "Missing Skills"
        ],
        "Count": [
            len(matched_skills),
            len(missing_skills)
        ]
    })


    fig2 = px.pie(
        chart_data,
        names="Category",
        values="Count",
        title="Required Skill Coverage"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # =================================================
    # LEARNING ROADMAP
    # =================================================

    st.divider()

    st.header(
        "📚 Personalized Learning Roadmap"
    )


    roadmap = generate_roadmap(
        missing_skills
    )


    if roadmap:

        roadmap_df = pd.DataFrame(
            roadmap
        )

        st.dataframe(
            roadmap_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No additional learning required."
        )


    # =================================================
    # DOWNLOAD REPORT
    # =================================================

    st.divider()

    st.header("📥 Download Analysis Report")


    report = StringIO()


    report.write(
        "AI RESUME ANALYZER\n"
    )

    report.write(
        "==============================\n\n"
    )


    report.write(
        f"Resume: {uploaded_file.name}\n\n"
    )


    report.write(
        "EXTRACTED SKILLS\n"
    )

    report.write(
        "------------------------------\n"
    )

    report.write(
        ", ".join(skills)
    )

    report.write("\n\n")


    report.write(
        "TOP 3 JOB RECOMMENDATIONS\n"
    )

    report.write(
        "------------------------------\n"
    )


    for index, recommendation in enumerate(top_3, start=1):

        report.write(
            f"{index}. "
            f"{recommendation['role']} - "
            f"{recommendation['score']:.2f}%\n"
        )


    report.write("\n")


    report.write(
        "TARGET ROLE ANALYSIS\n"
    )

    report.write(
        "------------------------------\n"
    )

    report.write(
        f"Target Role: {target_role}\n"
    )

    report.write(
        f"Skill Match: {skill_match_score:.2f}%\n"
    )

    report.write(
        f"TF-IDF Similarity: {tfidf_score:.2f}%\n"
    )


    report.write("\n")


    report.write(
        "MATCHED SKILLS\n"
    )

    report.write(
        "------------------------------\n"
    )

    report.write(
        ", ".join(matched_skills)
    )


    report.write("\n\n")


    report.write(
        "MISSING SKILLS\n"
    )

    report.write(
        "------------------------------\n"
    )


    for skill in missing_skills:

        report.write(
            f"- {skill}\n"
        )


    report.write("\n")


    report.write(
        "LEARNING ROADMAP\n"
    )

    report.write(
        "------------------------------\n"
    )


    for item in roadmap:

        report.write(
            f"Week {item['week']}: "
            f"{item['skill']} - "
            f"{item['topic']}\n"
        )


    st.download_button(
        label="📄 Download Resume Analysis Report",
        data=report.getvalue(),
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )


    # =================================================
    # EXTRACTED RESUME TEXT
    # =================================================

    st.divider()

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text(
            resume_text
        )


else:

    st.info(
        "👆 Upload a PDF or DOCX resume to begin."
    )