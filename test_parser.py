from resume_parser import extract_resume_text


pdf_path = "sample_resume.pdf"


# Open the PDF in binary mode
with open(pdf_path, "rb") as file:

    # Create a simple file-like object with a name
    class UploadedFile:
        def __init__(self, file_object, name):
            self.file_object = file_object
            self.name = name

        def read(self):
            return self.file_object.read()

    uploaded_file = UploadedFile(file, pdf_path)

    # Extract text
    text = extract_resume_text(uploaded_file)


print("\n==============================")
print("RESUME TEXT EXTRACTED")
print("==============================")

print("Characters extracted:", len(text))

print("\nFirst 2000 characters:")
print(text[:2000])