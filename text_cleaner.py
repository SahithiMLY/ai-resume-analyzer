import re


def clean_text(text):
    """
    Clean extracted resume text for analysis.
    """

    # Convert text to lowercase
    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Keep letters, numbers and common programming symbols
    text = re.sub(r"[^\w\s+#.-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()