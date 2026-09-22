import streamlit as st
import requests
from pathlib import Path


# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------
# Session State
# ---------------------------------------

if "analysis_data" not in st.session_state:
    st.session_state["analysis_data"] = None

if "role_analysis" not in st.session_state:
    st.session_state["role_analysis"] = None


# ---------------------------------------
# Custom CSS
# ---------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #EEF2FF 0%,
        #F8FAFC 45%,
        #E0F2FE 100%
    );
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Give normal Streamlit sections a cleaner appearance */
div[data-testid="stVerticalBlock"] {
    border-radius: 16px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.75);
    border-radius: 16px;
    padding: 10px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: bold;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 5px 15px rgba(37,99,235,0.25);
}

</style>
""", unsafe_allow_html=True)
# 👇 PASTE THE NEW BACKGROUND CODE HERE

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #EEF2FF 0%,
        #F8FAFC 45%,
        #E0F2FE 100%
    );
}

...
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Header
# ---------------------------------------

st.markdown("""
<style>

.main-header{
    background:linear-gradient(135deg,#2563EB,#4F46E5);
    padding:45px 30px;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:25px;
    box-shadow:0 8px 25px rgba(0,0,0,.15);
}
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:25px;
    box-shadow:0px 5px 20px rgba(0,0,0,.15);
}

.main-header h1{
    font-size:42px;
    margin-bottom:10px;
}

.main-header p{
    font-size:18px;
}

</style>

<div class="main-header">

<h1>📄 AI Resume Analyzer</h1>

<h3>Smart ATS Resume Screening System</h3>

<p>
Upload your resume to receive:
</p>

<p>
✅ ATS Score &nbsp;&nbsp; | &nbsp;&nbsp;
✅ Predicted Job Role &nbsp;&nbsp; | &nbsp;&nbsp;
✅ Technical Skills &nbsp;&nbsp; | &nbsp;&nbsp;
✅ Resume Suggestions
</p>

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------
# Upload Resume
# ---------------------------------------

st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 5px 20px rgba(0,0,0,.08);
margin-bottom:25px;
">

<h3>📂 Upload Your Resume</h3>

<p>Select your PDF resume and click <b>Analyze Resume</b>.</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["pdf"]
)

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

if analyze or st.session_state["analysis_data"] is not None:

    if uploaded_file is None:

        st.warning("Please upload a resume.")

    else:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )
        
        if response.status_code == 200:

                    data = response.json()
                    
                    st.session_state["analysis_data"] = data

                    st.success(data["message"])

                    # =======================================
                    # TWO COLUMN DASHBOARD
                    # =======================================

                    # =======================================
                    # ATS SCORE + PREDICTED JOB ROLE
                    # =======================================

                    left, right = st.columns([1, 1], gap="medium")
                    
                    # =======================================
                    # LEFT — AI RESUME ASSISTANT
                    # =======================================

    

                    # =======================================
                    # LEFT - ATS SCORE
                    # =======================================

                    with left:

                        score = data["score"]

                        if score >= 90:
                            grade = "🟢 Excellent"
                        elif score >= 80:
                            grade = "🟢 Very Good"
                        elif score >= 70:
                            grade = "🟡 Good"
                        elif score >= 60:
                            grade = "🟠 Average"
                        else:
                            grade = "🔴 Needs Improvement"

                        st.markdown("## 📊 ATS Resume Score")

                        st.metric(
                            label="Overall Score",
                            value=f"{score}/100"
                        )

                        if score >= 90:
                            grade = "🟢 Excellent"
                        elif score >= 80:
                            grade = "🟢 Very Good"
                        elif score >= 70:
                            grade = "🟡 Good"
                        elif score >= 60:
                            grade = "🟠 Average"
                        else:
                            grade = "🔴 Needs Improvement"

                        st.write(f"**Rating:** {grade}")

                        st.progress(score / 100)


                    # =======================================
                    # RIGHT - PREDICTED JOB ROLE
                    # =======================================

                    with right:

                        st.markdown("## 💼 Predicted Job Role")

                        st.info(
                            f"**{data['predicted_role']}**"
                        )
                        
                        st.markdown("### 🎯 Select Target Role")

                    selected_role = st.text_input(
                        "Enter the job role you want to target:",
                        placeholder="e.g. Python Developer, Java Developer, Data Analyst"
                    )

                    analyze_role = st.button(
                        "🔍 Analyze Resume for This Role",
                        use_container_width=True
                    )
                    
                    
                    if analyze_role:

                        if not selected_role.strip():

                            st.warning("Please enter a target role.")

                        elif st.session_state["analysis_data"] is None:

                            st.warning("Please analyze your resume first.")

                        else:

                            resume_text = st.session_state["analysis_data"]["resume_text"]

                            role_response = requests.post(
                                "http://127.0.0.1:8000/analyze-role",
                                json={
                                    "resume_text": resume_text,
                                    "target_role": selected_role.strip()
                                }
                            )

                            if role_response.status_code == 200:

                                role_data = role_response.json()

                                st.session_state["role_analysis"] = role_data

                            else:

                                st.error("Unable to analyze the selected role.")


                    # =======================================
                    # ROLE MATCH RESULT
                    # =======================================

                    if st.session_state.get("role_analysis") is not None:

                        role_data = st.session_state["role_analysis"]
                        
                        if role_data.get("role_correction"):
                             st.info(role_data["role_correction"])

                        st.markdown("### 🔎 Role Match Analysis")

                        match_percentage = role_data["match_percentage"]

                        st.metric(
                            "Role Match",
                            f"{match_percentage}%"
                        )

                        st.progress(match_percentage / 100)

                        st.markdown(
                            f"### 🎯 Target Role: "
                            f"{role_data['target_role'].title()}"
                        )

                        st.markdown("#### ✅ Matching Skills")

                        if role_data["matching_skills"]:

                            for skill in role_data["matching_skills"]:
                                st.success(skill)

                        else:

                            st.info("No matching skills found.")

                        st.markdown("#### ⚠️ Skills to Improve")

                        if role_data["missing_skills"]:

                            for skill in role_data["missing_skills"]:
                                st.warning(skill)

                        else:

                            st.success("No missing skills found.")

                        st.markdown("#### 💡 Suggestions")

                        if role_data["suggestions"]:

                            for suggestion in role_data["suggestions"]:
                                st.info(suggestion)

                        else:

                            st.success("No additional suggestions.")

                        st.markdown("### 📋 Eligibility")

                        if match_percentage >= 80:

                            st.success(role_data["eligibility"])

                        elif match_percentage >= 50:

                            st.warning(role_data["eligibility"])

                        else:

                            st.error(role_data["eligibility"])
                                    
                    
                    if analyze_role:

                        if not selected_role.strip():

                            st.warning("Please enter a target job role.")

                        elif st.session_state["analysis_data"] is None:

                            st.warning("Please analyze your resume first.")

                        else:

                            resume_text = st.session_state["analysis_data"]["resume_text"]

                            try:

                                role_response = requests.post(
                                    "http://127.0.0.1:8000/analyze-role",
                                    json={
                                        "resume_text": resume_text,
                                        "target_role": selected_role.strip()
                                    }
                                )

                                if role_response.status_code == 200:

                                    role_data = role_response.json()

                                    st.session_state["role_analysis"] = role_data

                                else:

                                    st.error(
                                        f"Role analysis failed. "
                                        f"Status code: {role_response.status_code}"
                                    )

                            except requests.exceptions.RequestException:

                                st.error(
                                    "Could not connect to the Resume Analyzer API."
                                )
                    
        

                    # =======================================
                    # TECHNICAL SKILLS
                    # =======================================

                    st.subheader("🛠 Technical Skills")

                    skills = data["skills"]

                    badge_colors = {
                        "Python": "#3776AB",
                        "Java": "#F89820",
                        "C": "#00599C",
                        "C++": "#00599C",
                        "HTML": "#E34F26",
                        "CSS": "#1572B6",
                        "JavaScript": "#F7DF1E",
                        "SQL": "#336791",
                        "MySQL": "#00758F",
                        "React": "#61DAFB",
                        "Git": "#F05032",
                        "GitHub": "#24292E",
                        "FastAPI": "#009688",
                        "Django": "#092E20",
                        "Spring": "#6DB33F",
                        "Spring Boot": "#6DB33F"
                    }

                    if skills:

                        cols = st.columns(2)

                        for i, skill in enumerate(skills):

                            color = badge_colors.get(skill, "#2563EB")

                            with cols[i % 2]:

                                st.markdown(f"""
                                <div style="
                                    background:{color};
                                    color:white;
                                    padding:12px;
                                    border-radius:12px;
                                    text-align:center;
                                    font-weight:bold;
                                    margin:6px 0;
                                    box-shadow:0px 3px 8px rgba(0,0,0,.15);
                                ">
                                    {skill}
                                </div>
                                """, unsafe_allow_html=True)

                                st.progress(score / 100)

                    else:

                        st.warning("No skills found.")


                    # =======================================
                    # ATS SCORE + BREAKDOWN
                    # =======================================

                    left, right = st.columns([1, 1], gap="medium")


                    with left:

                        # =======================================
                        # 🤖 AI RESUME ASSISTANT
                        # =======================================

                        st.markdown("""
                        <div style="
                            background:white;
                            padding:20px;
                            border-radius:15px;
                            box-shadow:0px 4px 12px rgba(0,0,0,.08;
                            margin-bottom:20px;
                        ">

                        <h2 style="color:#2563EB;margin:0;">
                        🤖 AI Resume Assistant
                        </h2>

                        <p style="color:#6B7280;margin-top:8px;">
                        Ask questions about your uploaded resume.
                        </p>

                        </div>
                        """, unsafe_allow_html=True)


                        # ---------------------------------------
                        # Chat History
                        # ---------------------------------------

                        if "chat_messages" not in st.session_state:
                            st.session_state["chat_messages"] = []


                        for message in st.session_state["chat_messages"]:

                            if message["role"] == "user":

                                st.markdown(
                                    f"""
                                    <div style="
                                        background:#EFF6FF;
                                        padding:10px;
                                        border-radius:10px;
                                        margin:8px 0;
                                    ">
                                    👤 <b>You:</b> {message["content"]}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            else:

                                st.markdown(
                                    f"""
                                    <div style="
                                        background:#F8FAFC;
                                        padding:10px;
                                        border-radius:10px;
                                        margin:8px 0;
                                    ">
                                    🤖 <b>AI:</b> {message["content"]}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


                        # ---------------------------------------
                        # Question Input
                        # ---------------------------------------

                        chat_question = st.text_input(
                            "Ask something about your resume:",
                            placeholder="e.g. What skills should I improve?",
                            key="chat_question_main"
                        )


                        ask_ai = st.button(
                            "🤖 Ask AI",
                            use_container_width=True,
                            key="ask_ai_main"
                        )


                        # ---------------------------------------
                        # Send Question
                        # ---------------------------------------

                        if ask_ai:

                            if not chat_question.strip():

                                st.warning("Please enter a question.")

                            elif st.session_state["analysis_data"] is None:

                                st.warning("Please analyze your resume first.")

                            else:

                                resume_text = st.session_state["analysis_data"]["resume_text"]

                                try:

                                    chat_response = requests.post(
                                        "http://127.0.0.1:8000/chat",
                                        json={
                                            "resume_text": resume_text,
                                            "question": chat_question.strip()
                                        }
                                    )

                                    if chat_response.status_code == 200:

                                        chat_data = chat_response.json()

                                        answer = chat_data["answer"]


                                        # Save user message

                                        st.session_state["chat_messages"].append({
                                            "role": "user",
                                            "content": chat_question
                                        })


                                        # Save AI response

                                        st.session_state["chat_messages"].append({
                                            "role": "assistant",
                                            "content": answer
                                        })


                                        st.rerun()

                                    else:

                                        st.error(
                                            f"AI Assistant error: "
                                            f"{chat_response.status_code}"
                                        )

                                except requests.exceptions.RequestException:

                                    st.error(
                                        "❌ Could not connect to the AI Assistant API."
                                    )


                    # =======================================
                    # RIGHT — ATS SCORE BREAKDOWN
                    # =======================================

                    with right:

                        st.markdown("""
                        <div style="
                            background:white;
                            padding:20px;
                            border-radius:15px;
                            box-shadow:0px 4px 12px rgba(0,0,0,.08);
                            margin-bottom:20px;
                        ">

                        <h2 style="color:#2563EB;margin:0;">
                        📊 ATS Score Breakdown
                        </h2>

                        </div>
                        """, unsafe_allow_html=True)

                        breakdown = data["breakdown"]

                        for section, marks in breakdown.items():

                            st.write(f"**{section}**")

                            st.progress(marks / 20)

                            st.write(f"{marks} / 20")

                    # =======================================
                    # RIGHT COLUMN
                    # =======================================

                    with right:

                        st.markdown("""
                            <div style="
                            background:white;
                            padding:20px;
                            border-radius:15px;
                            box-shadow:0px 4px 12px rgba(0,0,0,.08);
                            margin-bottom:15px;
                            ">

                            <h2 style="color:#2563EB;margin:0;">
                            📄 Resume Preview
                            </h2>

                            <p style="color:#6B7280;">
                            Extracted text from your uploaded resume
                            </p>

                            </div>
                            """, unsafe_allow_html=True)

                        st.text_area(
                            "Extracted Resume Text",
                            data["resume_text"],
                            height=560,
                            key="resume_preview"
                        )
                        
                        # =======================================
                        # RESUME SNAPSHOT
                        # =======================================

                        skills = data.get("skills", [])
                        breakdown = data.get("breakdown", {})

                        if breakdown:
                            strongest_section = max(breakdown, key=breakdown.get)
                            strongest_score = breakdown[strongest_section]
                        else:
                            strongest_section = "N/A"
                            strongest_score = 0

                        st.markdown("""
                        <div style="
                            background:white;
                            padding:20px;
                            border-radius:15px;
                            box-shadow:0px 4px 12px rgba(0,0,0,.08);
                            margin-top:20px;
                            margin-bottom:20px;
                        ">

                        <h2 style="color:#2563EB;margin-bottom:18px;">
                        📌 Resume Snapshot
                        </h2>

                        </div>
                        """, unsafe_allow_html=True)

                        snap1, snap2, snap3 = st.columns(3)

                        with snap1:
                            st.metric(
                                "🎯 Target Role",
                                data.get("predicted_role", "N/A")
                            )

                        with snap2:
                            st.metric(
                                "🛠 Skills Found",
                                len(skills)
                            )

                        with snap3:
                            st.metric(
                                "📊 Strongest Section",
                                f"{strongest_score}/20"
                            )

                        st.info(
                            f"💡 Your strongest resume section is **{strongest_section}** "
                            f"with a score of **{strongest_score}/20**."
                        )
                        
            
                    # =======================================
                    # RESUME SUGGESTIONS
                    # =======================================

                    st.subheader("💡 Resume Improvement Suggestions")

                    suggestions = data["suggestions"]

                    if suggestions:

                        for suggestion in suggestions:

                            st.markdown(f"""
                            <div style="
                                background:#FEF3C7;
                                border-left:6px solid #F59E0B;
                                padding:18px;
                                border-radius:12px;
                                margin-bottom:12px;
                            ">
                                <b>💡 {suggestion}</b>
                            </div>
                            """, unsafe_allow_html=True)

                    else:

                        st.success("✅ Your resume looks good.")

                    # =======================================
                    # DOWNLOAD REPORT
                    # =======================================

                    st.subheader("📥 Download Report")

                    try:

                        pdf_path = Path(__file__).resolve().parent.parent / "backend" / "resume_report.pdf"

                        with open(pdf_path, "rb") as pdf_file:

                            st.download_button(
                                label="📄 Download PDF Report",
                                data=pdf_file,
                                file_name="Resume_Report.pdf",
                                mime="application/pdf"
                            )

                    except FileNotFoundError:

                        st.warning("PDF report not found.")

       