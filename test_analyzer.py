from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import get_job_recommendations


pdf_path = "sample_resume.pdf"


class UploadedFile:

    def __init__(self, file_object, name):
        self.file_object = file_object
        self.name = name

    def read(self):
        return self.file_object.read()


with open(pdf_path, "rb") as file:

    uploaded_file = UploadedFile(
        file,
        pdf_path
    )

    resume_text = extract_resume_text(
        uploaded_file
    )


print("\n==============================")
print("RESUME EXTRACTION")
print("==============================")

print("Characters:", len(resume_text))


print("\n==============================")
print("SKILLS")
print("==============================")

skills = extract_skills(resume_text)

print(skills)


print("\n==============================")
print("JOB RECOMMENDATIONS")
print("==============================")

recommendations = get_job_recommendations(
    resume_text
)

for item in recommendations:

    print(
        item["role"],
        "->",
        item["score"],
        "%"
    )


print("\n==============================")
print("TOP 3")
print("==============================")

for item in recommendations[:3]:

    print(
        item["role"],
        "->",
        item["score"],
        "%"
    )