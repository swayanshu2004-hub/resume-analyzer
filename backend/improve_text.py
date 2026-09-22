def improve_resume(resume_text):

    suggestions = []

    text = resume_text.lower()

    # -----------------------------
    # Contact Information
    # -----------------------------
    if "@" not in text:
        suggestions.append("Add a professional email address.")

    if "linkedin" not in text:
        suggestions.append("Add your LinkedIn profile link.")

    if "github" not in text:
        suggestions.append("Add your GitHub profile link.")

    # -----------------------------
    # Career Summary
    # -----------------------------
    if "summary" not in text and "objective" not in text and "profile" not in text:
        suggestions.append("Add a professional summary or career objective.")

    # -----------------------------
    # Education
    # -----------------------------
    if "education" not in text:
        suggestions.append("Include an Education section.")

    # -----------------------------
    # Skills
    # -----------------------------
    if "skill" not in text:
        suggestions.append("Add a Technical Skills section.")

    # -----------------------------
    # Projects
    # -----------------------------
    if "project" not in text:
        suggestions.append("Add academic or personal projects.")

    # -----------------------------
    # Experience
    # -----------------------------
    if "experience" not in text and "intern" not in text:
        suggestions.append("Add internship or work experience if available.")

    # -----------------------------
    # Certifications
    # -----------------------------
    if "certificate" not in text and "certification" not in text:
        suggestions.append("Add relevant certifications.")

    # -----------------------------
    # Achievements
    # -----------------------------
    if "achievement" not in text:
        suggestions.append("Include achievements or coding profiles.")

    # -----------------------------
    # Resume Length
    # -----------------------------
    if len(text) < 1200:
        suggestions.append("Your resume is short. Add more project details and technical information.")

    # -----------------------------
    # No Suggestions
    # -----------------------------
    if len(suggestions) == 0:
        suggestions.append("Excellent resume! Only minor formatting improvements are recommended.")

    return suggestions