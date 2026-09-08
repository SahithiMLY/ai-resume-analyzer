def find_missing_skills(resume_skills, required_skills):

    resume_skills_lower = {
        skill.lower()
        for skill in resume_skills
    }

    missing = []

    for skill in required_skills:

        if skill.lower() not in resume_skills_lower:
            missing.append(skill)

    return missing