import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_text):
    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def get_job_recommendations(resume_text):
    jobs = pd.read_csv("data/job_roles.csv")

    results = []

    for _, job in jobs.iterrows():

        score = calculate_similarity(
            resume_text,
            job["skills"]
        )

        results.append({
            "role": job["role"],
            "score": score
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results