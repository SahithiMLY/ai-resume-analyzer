import pandas as pd
import re


def load_skill_dictionary():
    return pd.read_csv("data/skill_dictionary.csv")


def extract_skills(text):
    df = load_skill_dictionary()

    found_skills = []

    text = text.lower()

    for skill in df["skill"]:
        skill_lower = skill.lower()

        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(dict.fromkeys(found_skills))