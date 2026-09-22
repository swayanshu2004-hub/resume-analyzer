import re

def calculate_score(resume_text):

    text = resume_text.lower()
    breakdown = {}

    # -----------------------------
    # Contact Information (10)
    # -----------------------------
    contact = 0

    # Email
    if "@" in text:
        contact += 4

    # Phone Number
    phone_pattern = r"\b\d{10}\b"
    if re.search(phone_pattern, text):
        contact += 3

    # LinkedIn
    if "linkedin" in text:
        contact += 2

    # GitHub
    if "github" in text:
        contact += 1

    breakdown["Contact Information"] = contact

    # -----------------------------
    # Professional Summary (10)
    # -----------------------------
    summary = 0

    if "summary" in text or "objective" in text or "profile" in text:

        if len(text) > 1200:
            summary = 10
        else:
            summary = 6

    breakdown["Professional Summary"] = summary

    # -----------------------------
    # Education (10)
    # -----------------------------
    education = 0

    education_keywords = [
        "education",
        "college",
        "university",
        "b.tech",
        "btech",
        "mca",
        "bca",
        "degree"
    ]

    found = sum(1 for word in education_keywords if word in text)

    if found >= 3:
        education = 10
    elif found == 2:
        education = 8
    elif found == 1:
        education = 5

    breakdown["Education"] = education

    # -----------------------------
    # Technical Skills (20)
    # -----------------------------
    skill_keywords = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "node",
        "spring",
        "spring boot",
        "fastapi",
        "flask",
        "django",
        "git",
        "github",
        "mysql",
        "mongodb",
        "power bi",
        "excel",
        "tensorflow",
        "pandas",
        "numpy"
    ]

    skill_count = sum(
        1 for skill in skill_keywords
        if skill in text
    )

    if skill_count >= 10:
        technical = 20
    elif skill_count >= 8:
        technical = 16
    elif skill_count >= 6:
        technical = 12
    elif skill_count >= 4:
        technical = 8
    elif skill_count >= 2:
        technical = 5
    else:
        technical = 0

    breakdown["Technical Skills"] = technical

    # -----------------------------
    # Projects (20)
    # -----------------------------
    project_keywords = [
        "project",
        "developed",
        "created",
        "built",
        "implemented",
        "designed"
    ]

    project_count = sum(
        1 for word in project_keywords
        if word in text
    )

    if project_count >= 5:
        projects = 20
    elif project_count >= 3:
        projects = 15
    elif project_count >= 2:
        projects = 10
    elif project_count >= 1:
        projects = 5
    else:
        projects = 0

    breakdown["Projects"] = projects

    # -----------------------------
    # Experience (10)
    # -----------------------------
    experience = 0

    if "intern" in text:
        experience += 5

    if "experience" in text:
        experience += 5

    breakdown["Experience"] = experience

    # -----------------------------
    # Certifications (10)
    # -----------------------------
    cert_count = 0

    cert_count += text.count("certificate")
    cert_count += text.count("certification")

    if cert_count >= 2:
        certification = 10
    elif cert_count == 1:
        certification = 5
    else:
        certification = 0

    breakdown["Certifications"] = certification

    # -----------------------------
    # Resume Quality (10)
    # -----------------------------
    quality = 0

    if len(text) > 1800:
        quality = 10
    elif len(text) > 1400:
        quality = 8
    elif len(text) > 1000:
        quality = 6
    else:
        quality = 4

    breakdown["Resume Quality"] = quality

    # -----------------------------
    # Final Score
    # -----------------------------
    total_score = sum(breakdown.values())

    # Cap maximum score
    if total_score > 95:
        total_score = 95

    # Prevent unrealistically low score for a decent resume
    if total_score < 35:
        total_score = 35

    return total_score, breakdown