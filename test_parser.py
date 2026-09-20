from resume_parser import extract_resume_text


class UploadedFile:

    def __init__(self, file_object, name):

        self.file_object = file_object
        self.name = name

    def read(self):

        return self.file_object.read()


def test_file(file_path):

    print("\n==============================")
    print(f"TESTING: {file_path}")
    print("==============================")

    with open(file_path, "rb") as file:

        uploaded_file = UploadedFile(
            file,
            file_path
        )

        text = extract_resume_text(
            uploaded_file
        )

    print(
        "Characters extracted:",
        len(text)
    )

    print("\nFirst 1000 characters:")
    print(text[:1000])

    if text.strip():

        print("\n✅ EXTRACTION SUCCESS")

    else:

        print("\n❌ EXTRACTION FAILED")


# Test PDF
test_file("sample_resume.pdf")

# Test DOCX
test_file("sample_resume.docx")