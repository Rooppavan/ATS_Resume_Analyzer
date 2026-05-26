import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    layout="centered"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "ATS Analyzer",
        "Resume History"
    ]
)

st.title("AI Resume ATS Analyzer")

st.write(
    "Upload your resume and get ATS analysis instantly."
)

if page == "ATS Analyzer":

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        files = {
            "file": uploaded_file
        }

        response = requests.post(
            "https://ats-resume-analyzer-88kv.onrender.com/Upload-Resume",
            files=files
        )

        result = response.json()

        if "analysis" in result:

            analysis = result["analysis"]

            st.success(
                result["message"]
            )

            st.subheader("ATS Score")

            st.progress(
                analysis["ats_score"] / 100
            )

            st.metric(
                label="ATS Score",
                value=f'{analysis["ats_score"]}%'
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Matched Skills")

                for skill in analysis["matched_skills"]:
                    st.success(skill)

            with col2:

                st.subheader("Missing Skills")

                for skill in analysis["missing_skills"]:
                    st.error(skill)

        else:

            st.error(result)


if page == "Resume History":

    st.header("Resume Analysis History")

    history_response = requests.get(
        "https://ats-resume-analyzer-88kv.onrender.com/resume-history"
    )

    history_data = history_response.json()
    
    st.write(history_data)

    if history_data:

        df = pd.DataFrame(history_data)

        st.dataframe(df)

        fig = px.bar(
            df,
            x="filename",
            y="ats_score",
            title="ATS Score History"
        )

        st.plotly_chart(fig)

    else:

        st.warning("No resume history found.")