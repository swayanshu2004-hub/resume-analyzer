def predict_role(text):
    text = text.lower()

    java_score = 0
    python_score = 0
    frontend_score = 0
    data_score = 0

    # Java Developer
    for skill in ["java", "spring", "spring boot", "hibernate", "rest api"]:
        if skill in text:
            java_score += 1

    # Python Developer
    for skill in ["python", "django", "flask", "fastapi", "pandas", "numpy"]:
        if skill in text:
            python_score += 1

    # Frontend Developer
    for skill in ["html", "css", "javascript", "react", "angular"]:
        if skill in text:
            frontend_score += 1

    # Data Analyst
    for skill in ["sql", "power bi", "excel", "tableau", "pandas"]:
        if skill in text:
            data_score += 1

    scores = {
        "Java Developer": java_score,
        "Python Developer": python_score,
        "Frontend Developer": frontend_score,
        "Data Analyst": data_score
    }

    best_role = max(scores, key=scores.get)

    if scores[best_role] == 0:
        return "General Software Engineer"

    return best_role

