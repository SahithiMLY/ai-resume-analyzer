import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
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

    pdf_bytes = file.read()

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

    if text:

        document.close()

        return "\n".join(text)

    # -----------------------------------------------------
    # SECOND ATTEMPT: OCR
    # -----------------------------------------------------

    tesseract_available = shutil.which("tesseract")

    if os.name == "nt":

        windows_tesseract_path = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        tesseract_available = os.path.exists(
            windows_tesseract_path
        )

    if not tesseract_available:

        document.close()

        return ""

    # -----------------------------------------------------
    # OCR EACH PDF PAGE
    # -----------------------------------------------------

    ocr_text = []

    for page in document:

        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

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

    First uses python-docx to read:
        - normal paragraphs
        - tables

    If no text is found, falls back to reading
    the DOCX XML directly.
    """

    # -----------------------------------------------------
    # READ UPLOADED DOCX INTO MEMORY
    # -----------------------------------------------------

    docx_bytes = file.read()

    text = []

    # -----------------------------------------------------
    # FIRST METHOD: PYTHON-DOCX
    # -----------------------------------------------------

    try:

        document = Document(
            BytesIO(docx_bytes)
        )

        # -------------------------------------------------
        # READ NORMAL PARAGRAPHS
        # -------------------------------------------------

        for paragraph in document.paragraphs:

            paragraph_text = paragraph.text.strip()

            if paragraph_text:

                text.append(
                    paragraph_text
                )

        # -------------------------------------------------
        # READ TABLES
        # -------------------------------------------------

        for table in document.tables:

            for row in table.rows:

                row_text = []

                for cell in row.cells:

                    cell_text = cell.text.strip()

                    if cell_text:

                        row_text.append(
                            cell_text
                        )

                if row_text:

                    text.append(
                        " | ".join(row_text)
                    )

    except Exception:

        text = []

    # -----------------------------------------------------
    # IF PYTHON-DOCX FOUND TEXT
    # -----------------------------------------------------

    if text:

        return "\n".join(text)

    # -----------------------------------------------------
    # SECOND METHOD: DIRECT DOCX XML EXTRACTION
    # -----------------------------------------------------

    try:

        with zipfile.ZipFile(
            BytesIO(docx_bytes)
        ) as docx_zip:

            xml_data = docx_zip.read(
                "word/document.xml"
            )

        root = ET.fromstring(
            xml_data
        )

        # Correct Microsoft Word XML namespace
        namespace = {
            "w": (
                "http://schemas.openxmlformats.org/"
                "wordprocessingml/2006/main"
            )
        }

        xml_text = []

        # -------------------------------------------------
        # READ EVERY PARAGRAPH FROM XML
        # -------------------------------------------------

        for paragraph in root.findall(
            ".//w:p",
            namespace
        ):

            words = []

            for text_node in paragraph.findall(
                ".//w:t",
                namespace
            ):

                if text_node.text:

                    words.append(
                        text_node.text
                    )

            if words:

                paragraph_text = "".join(
                    words
                ).strip()

                if paragraph_text:

                    xml_text.append(
                        paragraph_text
                    )

        return "\n".join(
            xml_text
        )

    except Exception:

        return ""


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