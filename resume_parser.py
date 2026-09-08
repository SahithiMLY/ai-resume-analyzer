import pymupdf
import pytesseract
from PIL import Image
from docx import Document


# Tell pytesseract where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_pdf_text(file):
    """
    Extract text from a PDF resume.

    First tries normal PDF text extraction.
    If no usable text is found, uses OCR with Tesseract.
    """

    # Open PDF from uploaded file
    document = pymupdf.open(
        stream=file.read(),
        filetype="pdf"
    )

    text = []

    # First attempt: normal text extraction
    for page in document:
        page_text = page.get_text("text")

        if page_text and page_text.strip():
            text.append(page_text)

    # If normal extraction worked, return the text
    if text:
        document.close()
        return "\n".join(text)

    # -------------------------------------------------
    # OCR FALLBACK
    # -------------------------------------------------

    ocr_text = []

    for page in document:

        # Render PDF page as an image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        # Convert image to PIL format
        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # Perform OCR
        page_text = pytesseract.image_to_string(image)

        if page_text and page_text.strip():
            ocr_text.append(page_text)

    document.close()

    return "\n".join(ocr_text)


def extract_docx_text(file):
    """
    Extract text from a DOCX resume.
    """

    document = Document(file)

    text = []

    # Read normal paragraphs
    for paragraph in document.paragraphs:

        paragraph_text = paragraph.text.strip()

        if paragraph_text:
            text.append(paragraph_text)

    # Read tables
    for table in document.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                text.append(" | ".join(row_text))

    return "\n".join(text)


def extract_resume_text(file):
    """
    Detect the resume file type and extract its text.

    Supports PDF and DOCX files.
    """

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):

        return extract_pdf_text(file)

    elif file_name.endswith(".docx"):

        return extract_docx_text(file)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX resume."
        )