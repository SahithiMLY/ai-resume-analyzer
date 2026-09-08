ROADMAP = {

    "Python":
        "Learn Python programming fundamentals",

    "SQL":
        "Practice SQL queries and database concepts",

    "Excel":
        "Learn Excel formulas, functions and data analysis",

    "Pandas":
        "Learn data manipulation using Pandas",

    "NumPy":
        "Learn numerical computing using NumPy",

    "Machine Learning":
        "Study supervised and unsupervised learning",

    "Scikit-learn":
        "Practice machine learning using Scikit-learn",

    "FastAPI":
        "Learn REST API development using FastAPI",

    "Docker":
        "Learn Docker images, containers and deployment",

    "AWS":
        "Learn basic cloud deployment using AWS",

    "NLP":
        "Learn NLP preprocessing and text classification",

    "Transformers":
        "Study transformer architecture and applications",

    "Hugging Face":
        "Learn Hugging Face models and pipelines",

    "Git":
        "Learn Git version control",

    "GitHub":
        "Learn GitHub repositories and collaboration"
}


def generate_roadmap(missing_skills):

    roadmap = []

    for week, skill in enumerate(
        missing_skills,
        start=1
    ):

        topic = ROADMAP.get(
            skill,
            f"Learn {skill}"
        )

        roadmap.append({
            "week": week,
            "skill": skill,
            "topic": topic
        })

    return roadmap