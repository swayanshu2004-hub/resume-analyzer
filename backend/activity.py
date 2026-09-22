def extract_skills(text):

    skills = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Spring",
        "Spring Boot",
        "FastAPI",
        "Flask",
        "Django",
        "Git",
        "GitHub",
        "MySQL",
        "MongoDB",
        "Power BI",
        "Excel",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Pandas",
        "NumPy"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def analyze_role_match(resume_text, target_role):

    from difflib import get_close_matches

    role_skills = {
        "java developer": [
            "Java",
            "Spring",
            "Spring Boot",
            "SQL",
            "Git",
            "GitHub"
        ],

        "python developer": [
            "Python",
            "Django",
            "Flask",
            "FastAPI",
            "SQL",
            "Git",
            "GitHub"
        ],

        "web developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Git",
            "GitHub"
        ],

        "frontend developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git",
            "GitHub"
        ],

        "backend developer": [
            "Java",
            "Python",
            "Spring Boot",
            "FastAPI",
            "SQL",
            "Git",
            "GitHub"
        ],

        "data analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Pandas",
        "NumPy"
    ],

    "ai ml engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Pandas",
        "NumPy",
        "SQL",
        "Git"
    ],

    "machine learning engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Pandas",
        "NumPy",
        "SQL",
        "Git"
    ]
    }

    # ---------------------------------------
    # CLEAN TARGET ROLE
    # ---------------------------------------

    original_role = target_role.strip()

    target_role = original_role.lower()

    # Normalize AI/ML role variations
    target_role = (
        target_role
        .replace("&", "and")
        .replace("-", " ")
        .replace("/", " ")
    )

    target_role = " ".join(target_role.split())

    role_aliases = {
    "aiml engineer": "ai ml engineer",
    "ai ml engineer": "ai ml engineer",
    "ai and ml engineer": "ai ml engineer",
    "artificial intelligence engineer": "ai ml engineer",
    "machine learning engineer": "machine learning engineer"
    }

    target_role = role_aliases.get(
        target_role,
        target_role
    )

    # ---------------------------------------
    # CORRECT MINOR SPELLING MISTAKES
    # ---------------------------------------

    supported_roles = list(role_skills.keys())

    if target_role not in role_skills:

        close_roles = get_close_matches(
            target_role,
            supported_roles,
            n=1,
            cutoff=0.60
        )

        if close_roles:

            corrected_role = close_roles[0]

            target_role = corrected_role

            role_correction = (
                f"Did you mean **{corrected_role.title()}**? "
                f"Your input was **{original_role}**."
            )

        else:

            return {
                "target_role": original_role,
                "required_skills": [],
                "matching_skills": [],
                "missing_skills": [],
                "match_percentage": 0,
                "suggestions": [],
                "eligibility": (
                    "⚠️ This target role is not currently supported. "
                    "Please try one of the available roles."
                ),
                "role_correction": None
            }

    else:

        role_correction = None

    # ---------------------------------------
    # GET REQUIRED SKILLS
    # ---------------------------------------

    required_skills = role_skills[target_role]

    # ---------------------------------------
    # EXTRACT RESUME SKILLS
    # ---------------------------------------

    resume_skills = extract_skills(resume_text)

    # ---------------------------------------
    # MATCH SKILLS
    # ---------------------------------------

    matching_skills = [
        skill for skill in required_skills
        if skill.lower() in [
            resume_skill.lower()
            for resume_skill in resume_skills
        ]
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in matching_skills
    ]

    # ---------------------------------------
    # CALCULATE MATCH
    # ---------------------------------------

    if required_skills:

        match_percentage = round(
            (len(matching_skills) / len(required_skills)) * 100
        )

    else:

        match_percentage = 0

    # ---------------------------------------
    # ROLE-SPECIFIC SUGGESTIONS
    # ---------------------------------------

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            f"Consider learning or improving **{skill}** "
            f"for the **{target_role.title()}** role."
        )

    # ---------------------------------------
    # ELIGIBILITY
    # ---------------------------------------

    if match_percentage == 100:

        eligibility = (
            "🟢 You are eligible for this role. "
            "Your resume contains all the required skills."
        )

    elif match_percentage >= 80:

        eligibility = (
            "🟢 You are almost ready for this role. "
            "Only a few skills need improvement."
        )

    elif match_percentage >= 50:

        eligibility = (
            "🟡 Your resume has a reasonable match, "
            "but some important skills are missing."
        )

    else:

        eligibility = (
            "🔴 Your resume currently has a low match "
            "for this role. Consider improving the missing skills."
        )

    # ---------------------------------------
    # FINAL RESULT
    # ---------------------------------------

    return {
        "target_role": target_role,
        "required_skills": required_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "suggestions": suggestions,
        "eligibility": eligibility,
        "role_correction": role_correction
    }

    # Clean target role
    target_role = target_role.lower().strip()

    # Get skills required for selected role
    required_skills = role_skills.get(target_role, [])

    # Extract skills from uploaded resume
    resume_skills = extract_skills(resume_text)

    # Find matching skills
    matching_skills = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    # Find missing skills
    missing_skills = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    # Calculate role match percentage
    if required_skills:
        match_percentage = round(
            (len(matching_skills) / len(required_skills)) * 100
        )
    else:
        match_percentage = 0

    # Suggestions
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Consider learning or improving {skill} "
            f"for the {target_role.title()} role."
        )

    # Eligibility message
    if not required_skills:
        eligibility = (
            "⚠️ This target role is not currently supported."
        )

    elif match_percentage == 100:
        eligibility = (
            "🟢 You are eligible for this role. "
            "Your resume contains all the required skills."
        )

    elif match_percentage >= 80:
        eligibility = (
            "🟢 You are almost ready for this role. "
            "Only a few skills need improvement."
        )

    elif match_percentage >= 50:
        eligibility = (
            "🟡 Your resume has a reasonable match, "
            "but some important skills are missing."
        )

    else:
        eligibility = (
            "🔴 Your resume currently has a low match "
            "for this role. Consider improving the missing skills."
        )

    return {
        "target_role": target_role,
        "required_skills": required_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "suggestions": suggestions,
        "eligibility": eligibility
    }