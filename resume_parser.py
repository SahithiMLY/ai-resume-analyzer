import os
import shutil
import zipfile
from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image
from docx import Document


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

WINDOWS_TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if os.name == "nt":

    if os.path.exists(WINDOWS_TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = (
            WINDOWS_TESSERACT_PATH
        )

else:

    if shutil.which("tesseract"):
        pytesseract.pytesseract.tesseract_cmd = "tesseract"


def tesseract_available():
    """Return True when Tesseract OCR is available."""

    if os.name == "nt":
        return os.path.exists(
            WINDOWS_TESSERACT_PATH
        )

    return shutil.which("tesseract") is not None


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(file):

    """
    Extract text from a PDF.

    First attempts normal PDF text extraction.
    If no usable text is found, OCR is used.
    """

    pdf_bytes = file.read()

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    # -----------------------------------------------------
    # FIRST ATTEMPT: NORMAL PDF TEXT
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

    if not tesseract_available():

        document.close()

        return ""

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

    Supports:

    1. Normal DOCX paragraphs
    2. DOCX tables
    3. Direct DOCX XML extraction
    4. OCR of images embedded inside DOCX

    The fourth method is important for scanned/image
    resumes saved inside a DOCX file.
    """

    docx_bytes = file.read()

    # -----------------------------------------------------
    # FIRST METHOD: PYTHON-DOCX
    # -----------------------------------------------------

    text = []

    try:

        document = Document(
            BytesIO(docx_bytes)
        )

        # Read paragraphs

        for paragraph in document.paragraphs:

            paragraph_text = paragraph.text.strip()

            if paragraph_text:

                text.append(
                    paragraph_text
                )

        # Read tables

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

    # If normal DOCX text exists, return it

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

        from xml.etree import ElementTree as ET

        root = ET.fromstring(
            xml_data
        )

        namespace = {

            "w": (
                "http://schemas.openxmlformats.org/"
                "wordprocessingml/2006/main"
            )

        }

        xml_text = []

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

        if xml_text:

            return "\n".join(
                xml_text
            )

    except Exception:

        pass

    # -----------------------------------------------------
    # THIRD METHOD: OCR EMBEDDED DOCX IMAGES
    # -----------------------------------------------------

    if not tesseract_available():

        return ""

    ocr_text = []

    try:

        with zipfile.ZipFile(
            BytesIO(docx_bytes)
        ) as docx_zip:

            media_files = [

                name

                for name in docx_zip.namelist()

                if name.startswith(
                    "word/media/"
                )

            ]

            for media_file in media_files:

                try:

                    image_bytes = (
                        docx_zip.read(
                            media_file
                        )
                    )

                    image = Image.open(
                        BytesIO(image_bytes)
                    ).convert("RGB")

                    image_text = (
                        pytesseract.image_to_string(
                            image
                        )
                    )

                    if (
                        image_text
                        and image_text.strip()
                    ):

                        ocr_text.append(
                            image_text
                        )

                except Exception:

                    continue

    except Exception:

        return ""

    return "\n".join(
        ocr_text
    )


# =========================================================
# MAIN RESUME TEXT EXTRACTION FUNCTION
# =========================================================

def extract_resume_text(file):

    """
    Detect resume file type and extract its text.

    Supported formats:

    PDF
    DOCX
    """

    file_name = file.name.lower()

    # PDF

    if file_name.endswith(".pdf"):

        return extract_pdf_text(file)

    # DOCX

    if file_name.endswith(".docx"):

        return extract_docx_text(file)

    raise ValueError(
        "Unsupported file format. "
        "Please upload a PDF or DOCX resume."
    )