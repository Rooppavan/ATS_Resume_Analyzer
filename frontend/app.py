import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "ATS Analyzer",
        "Resume History"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "AI Powered ATS Resume Analyzer"
)

st.sidebar.markdown(
    """
    ## 🚀 Features

    ✅ ATS Analysis  
    ✅ JD Match Score  
    ✅ AI Suggestions  
    ✅ Resume Intelligence  
    ✅ Resume History Dashboard  
    """
)
# -----------------------------------
# MAIN TITLE
# -----------------------------------

st.markdown(
    """
    <h1 style='text-align:center;
    font-size:55px;
    color:#4F8BF9;'>

    🚀 AI Resume Analyzer

    </h1>

    <p style='text-align:center;
    font-size:22px;
    color:gray;'>

    Analyze your resume with AI-powered ATS intelligence

    </p>
    """,
    unsafe_allow_html=True
)

# ===================================
# ATS ANALYZER PAGE
# ===================================

if page == "ATS Analyzer":

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste Job Description (Optional)",
        height=200
    )

    if uploaded_file is not None:

        st.success(
            "Resume uploaded successfully"
        )

        if st.button("Submit", use_container_width=True):

            files = {
                "file": uploaded_file
            }

            with st.spinner(
                "🤖 AI is analyzing your resume..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/Upload-Resume",
                    files=files,
                    data={
                        "job_description":
                            job_description
                    }
                )

            result = response.json()

            if "analysis" in result:

                analysis = result["analysis"]

                # -----------------------------------
                # TABS
                # -----------------------------------

                tab1, tab2, tab3 = st.tabs(
                    [
                        "ATS Analysis",
                        "JD Match",
                        "Suggestions"
                    ]
                )

                # ===================================
                # TAB 1 — ATS ANALYSIS
                # ===================================

                with tab1:

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(
                            f"""
                            <div style="
                                background-color:#111827;
                                padding:25px;
                                border-radius:18px;
                                border:1px solid #374151;
                                text-align:center;
                            ">

                            <h3 style="color:white;">
                                🎯 ATS Score
                            </h3>

                            <h1 style="color:#22c55e;
                            font-size:50px;">

                                {analysis['ats_score']}%

                            </h1>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:

                        st.metric(
                            "Resume Sections",
                            len(
                                analysis[
                                    "detected_sections"
                                ]
                            )
                        )

                    st.progress(
                        analysis["ats_score"] / 100
                    )
                    
                    st.divider()

                    st.markdown(
                        "## 📑 Resume Sections Found"
                    )
                    
                    st.divider()
                    
                    st.markdown("## 🤖 AI Resume Verdict")
                    
                    st.info(analysis["ai_verdict"])

                    cols = st.columns(4)

                    for i, section in enumerate(
                        analysis["detected_sections"]
                    ):

                        cols[i % 4].success(
                            section.title()
                        )

                    st.markdown(
                        "## 💪 Resume Strengths"
                    )

                    for strength in analysis[
                        "strengths"
                    ]:

                        st.success(strength)

                # ===================================
                # TAB 2 — JD MATCH
                # ===================================

                with tab2:

                    if analysis[
                        "job_match_score"
                    ] > 0:

                        st.metric(
                            "JD Match Score",
                            f"{analysis['job_match_score']}%"
                        )

                        st.markdown(
                            "## 🔍 Matched Keywords"
                        )

                        matched_cols = st.columns(4)

                        for i, keyword in enumerate(
                            analysis[
                                "matched_keywords"
                            ]
                        ):

                            matched_cols[
                                i % 4
                            ].success(keyword)

                    else:

                        st.info(
                            "No Job Description provided."
                        )

                # ===================================
                # TAB 3 — SUGGESTIONS
                # ===================================

                with tab3:

                    st.markdown(
                        "## 💡 Suggestions To Improve"
                    )

                    for suggestion in analysis[
                        "suggestions"
                    ]:

                        st.warning(suggestion)
                    st.markdown("## 🤖 AI Resume Improvements")
                    
                    if analysis["ai_rewrite_suggestions"]:
                        for item in analysis["ai_rewrite_suggestions"]:
                            st.info(item)
                    else:
                        st.success("Your resume already uses strong action-oriented language.")

            else:

                st.error(
                    "Something went wrong"
                )

# ===================================
# RESUME HISTORY PAGE
# ===================================

if page == "Resume History":

    st.header("📊 Resume Analysis History")

    history_response = requests.get(
        "http://127.0.0.1:8000/resume-history"
    )

    history_data = history_response.json()

    if history_data:

        df = pd.DataFrame(history_data)

        # -----------------------------------
        # METRICS
        # -----------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Resumes",
                len(df)
            )

        with col2:

            st.metric(
                "Highest ATS Score",
                df["ats_score"].max()
            )

        # -----------------------------------
        # TABLE
        # -----------------------------------

        st.dataframe(
            df[
                [
                    "filename",
                    "ats_score"
                ]
            ],
            use_container_width=True
        )

        # -----------------------------------
        # CHART
        # -----------------------------------

        fig = px.bar(
            df,
            x="filename",
            y="ats_score",
            title="ATS Score History"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "No resume history found."
        )

st.markdown(
    """
    <hr>

    <center>

    Built with ❤️ using FastAPI + Streamlit

    </center>
    """,
    unsafe_allow_html=True
)