from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_report(filename, score, role, skills, suggestions):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Resume Analysis Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Resume Score:</b> {score}/100", styles["BodyText"]))
    story.append(Paragraph(f"<b>Predicted Role:</b> {role}", styles["BodyText"]))

    story.append(Paragraph("<b>Skills:</b>", styles["Heading2"]))

    for skill in skills:
        story.append(Paragraph(f"• {skill}", styles["BodyText"]))

    story.append(Paragraph("<b>Improvement Suggestions:</b>", styles["Heading2"]))

    for suggestion in suggestions:
        story.append(Paragraph(f"• {suggestion}", styles["BodyText"]))

    doc.build(story)


def calculate_score(resume_text):

    score = 0

    text = resume_text.lower()

    # -----------------------------
    # Contact Information (10)
    # -----------------------------
    if "@" in text:
        score += 5

    if "linkedin" in text or "github" in text:
        score += 5

    # -----------------------------
    # Professional Summary (10)
    # -----------------------------
    if "summary" in text or "profile" in text:
        score += 10

    # -----------------------------
    # Education (10)
    # -----------------------------
    education_keywords = [
        "b.tech",
        "btech",
        "mca",
        "bca",
        "degree",
        "education",
        "college"
    ]

    if any(word in text for word in education_keywords):
        score += 10

    # -----------------------------
    # Technical Skills (20)
    # -----------------------------
    skill_keywords = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "spring",
        "mysql",
        "git"
    ]

    score += min(20, len([s for s in skill_keywords if s in text]) * 2)

    # -----------------------------
    # Projects (20)
    # -----------------------------
    if "project" in text:
        score += 10

    if "github" in text:
        score += 5

    if "demo" in text:
        score += 5

    # -----------------------------
    # Experience / Internship (10)
    # -----------------------------
    if "experience" in text or "intern" in text:
        score += 10

    # -----------------------------
    # Certifications (10)
    # -----------------------------
    if "certificate" in text or "certification" in text:
        score += 10

    # -----------------------------
    # Resume Length (10)
    # -----------------------------
    if len(text) > 800:
        score += 10

    if score > 100:
        score = 100

    return score