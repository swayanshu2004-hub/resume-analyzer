import streamlit as st
import requests

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------
# Custom CSS
# ---------------------------------------

st.markdown("""
<style>

.stApp{
    background:#F4F7FC;
}

.title{
    background:linear-gradient(90deg,#2563EB,#1E40AF);
    padding:30px;
    border-radius:15px;
    color:white;
    text-align:center;
    margin-bottom:25px;
}

.upload-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,.08);
}

.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1E40AF;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Header
# ---------------------------------------

st.markdown("""
<div class="title">

<h1>📄 AI Resume Analyzer</h1>

<h4>Smart ATS Resume Screening System</h4>

Upload your resume to receive:

✔ ATS Score

✔ Predicted Job Role

✔ Skills Analysis

✔ Resume Suggestions

</div>
""", unsafe_allow_html=True)

# ---------------------------------------
# Upload Section
# ---------------------------------------

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose Resume (PDF)",
    type=["pdf"]
)

analyze = st.button("🚀 Analyze Resume")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# Analyze Resume
# ---------------------------------------

if analyze:

    if uploaded_file is None:

        st.warning("Please upload a resume first.")

    else:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        try:

            with st.spinner("Analyzing Resume..."):

                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/upload",
                        files=files,
                        timeout=30
                    )

                    st.write("Status Code:", response.status_code)

                    st.write("Response:", response.text)

                except Exception as e:
                    st.error(str(e))

            if response.status_code == 200:

                data = response.json()

                st.success(data["message"])

                score = data["score"]

                st.markdown("""
                <style>

                .score-card{
                background:#2563EB;
                padding:25px;
                border-radius:15px;
                text-align:center;
                color:white;
                margin-top:20px;
                margin-bottom:20px;
                box-shadow:0px 5px 20px rgba(0,0,0,.15);
                }

                .score{
                font-size:55px;
                font-weight:bold;
                }

                .score-text{
                font-size:22px;
                }

                </style>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="score-card">

                <div class="score">{score}/100</div>

                <div class="score-text">
                ATS Resume Score
                </div>

                </div>
                """, unsafe_allow_html=True)

                st.progress(score/100)

                st.subheader("💼 Predicted Job Role")

                st.info(data["predicted_role"])
                # -----------------------------
                # Extracted Skills
                # -----------------------------

                st.subheader("🛠 Technical Skills")

                skills = data["skills"]

                if len(skills) > 0:

                    cols = st.columns(4)

                    for i, skill in enumerate(skills):

                        with cols[i % 4]:

                            st.markdown(
                                f"""
                                <div style="
                                    background:#2563EB;
                                    color:white;
                                    padding:12px;
                                    border-radius:12px;
                                    text-align:center;
                                    margin:8px;
                                    font-weight:bold;
                                    box-shadow:0 3px 10px rgba(0,0,0,.15);
                                ">
                                {skill}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:

                    st.warning("No skills found.")
                    # -----------------------------
                    # Resume Improvement Suggestions
                    # -----------------------------

                    st.subheader("💡 Resume Improvement Suggestions")

                    suggestions = data["suggestions"]

                    if len(suggestions) > 0:

                        for suggestion in suggestions:
                            st.warning(suggestion)

                    else:
                        st.success("Your resume looks good.")
                        # -----------------------------
                        # ATS Score Breakdown
                        # -----------------------------

                        st.subheader("📊 ATS Score Breakdown")

                        breakdown = data["breakdown"]

                        for section, marks in breakdown.items():

                            color = "#22C55E"

                            if marks < 10:
                                color = "#EF4444"
                            elif marks < 16:
                                color = "#F59E0B"

                            st.markdown(f"""
                            <div style="
                                background:white;
                                padding:15px;
                                border-radius:12px;
                                margin-bottom:12px;
                                box-shadow:0 2px 10px rgba(0,0,0,.08);
                                display:flex;
                                justify-content:space-between;
                                align-items:center;
                            ">
                                <div>
                                    <b>{section}</b>
                                </div>

                                <div style="
                                    background:{color};
                                    color:white;
                                    padding:6px 15px;
                                    border-radius:20px;
                                    font-weight:bold;
                                ">
                                    {marks}
                                </div>

                            </div>
                            """, unsafe_allow_html=True)
                            # -----------------------------
                            # Resume Preview
                            # -----------------------------

                            st.subheader("📄 Resume Preview")

                            st.text_area(
                                "Extracted Resume Text",
                                data["resume_text"],
                                height=350
                            )
                            # -----------------------------
                    # Download PDF Report
                    # -----------------------------

                    st.subheader("📥 Download Report")

                    try:
                        with open("../backend/resume_report.pdf", "rb") as pdf_file:

                            st.download_button(
                                label="📄 Download PDF Report",
                                data=pdf_file,
                                file_name="Resume_Report.pdf",
                                mime="application/pdf"
                            )

                    except FileNotFoundError:

                        st.warning("PDF report not found.")

            else:

                st.error("Backend Error")
                st.write(response.text)

        except Exception as e:

            st.error(f"Connection Error: {e}")