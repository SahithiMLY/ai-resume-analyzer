import os
import shutil
from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image
from docx import Document


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

if os.name == "nt":
    # Windows
    windows_tesseract_path = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    if os.path.exists(windows_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = (
            windows_tesseract_path
        )

else:
    # Linux / Streamlit Cloud
    if shutil.which("tesseract"):
        pytesseract.pytesseract.tesseract_cmd = "tesseract"


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(file):
    """
    Extract text from a PDF resume.

    First attempts normal PDF text extraction.
    If no usable text is found, attempts OCR using Tesseract.
    """

    # Read uploaded PDF into memory

    pdf_bytes = file.read()

    # Open PDF
    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    # -----------------------------------------------------
    # FIRST ATTEMPT: NORMAL PDF TEXT EXTRACTION
    # -----------------------------------------------------

    text = []

    for page in document:

        page_text = page.get_text("text")

        if page_text and page_text.strip():
            text.append(page_text)

    # If normal extraction worked, return the text
    if text:
        document.close()
        return "\n".join(text)

    # -----------------------------------------------------
    # SECOND ATTEMPT: OCR
    # -----------------------------------------------------

    tesseract_available = shutil.which("tesseract")

    # Windows check
    if os.name == "nt":

        windows_tesseract_path = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        tesseract_available = os.path.exists(
            windows_tesseract_path
        )

    # If Tesseract is not installed, return empty text
    if not tesseract_available:
        document.close()
        return ""

    # -----------------------------------------------------
    # OCR EACH PDF PAGE
    # -----------------------------------------------------

    ocr_text = []

    for page in document:

        # Render PDF page as image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        # Convert PyMuPDF image to PIL image
        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # Perform OCR
        page_text = pytesseract.image_to_string(
            image
        )

        if page_text and page_text.strip():
            ocr_text.append(page_text)

    document.close()

    return "\n".join(ocr_text)


# =========================================================
# DOCX TEXT EXTRACTION
# =========================================================

def extract_docx_text(file):
    """
    Extract text from a DOCX resume.

    Reads both normal paragraphs and tables.
    """

    # -----------------------------------------------------
    # READ UPLOADED DOCX INTO MEMORY
    # -----------------------------------------------------

    
    docx_bytes = file.read()

    # Open DOCX from memory
    document = Document(
        BytesIO(docx_bytes)
    )

    text = []

    # -----------------------------------------------------
    # READ NORMAL PARAGRAPHS
    # -----------------------------------------------------

    for paragraph in document.paragraphs:

        paragraph_text = paragraph.text.strip()

        if paragraph_text:
            text.append(paragraph_text)

    # -----------------------------------------------------
    # READ TABLES
    # -----------------------------------------------------

    for table in document.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                text.append(
                    " | ".join(row_text)
                )

    return "\n".join(text)


# =========================================================
# MAIN RESUME TEXT EXTRACTION FUNCTION
# =========================================================

def extract_resume_text(file):
    """
    Detect the resume file type and extract its text.

    Supported formats:
        PDF
        DOCX
    """

    file_name = file.name.lower()

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if file_name.endswith(".pdf"):

        return extract_pdf_text(file)

    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    elif file_name.endswith(".docx"):

        return extract_docx_text(file)

    # -----------------------------------------------------
    # UNSUPPORTED FILE
    # -----------------------------------------------------

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX resume."
        )
