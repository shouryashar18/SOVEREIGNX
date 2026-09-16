import os
from docx import Document
from pypdf import PdfReader


SUPPORTED_DOCUMENTS = [".txt", ".docx", ".pdf"]


def read_file_content(file_path: str) -> str:
    """
    Extract text from TXT, DOCX, or PDF files.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in SUPPORTED_DOCUMENTS:
        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    text = ""

    try:

        # TXT
        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        # DOCX
        elif extension == ".docx":
            document = Document(file_path)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            text = "\n".join(paragraphs)

        # PDF
        elif extension == ".pdf":
            reader = PdfReader(file_path)

            pages = []

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    pages.append(page_text)

            text = "\n".join(pages)

    except Exception as e:
        raise RuntimeError(
            f"Error reading file: {str(e)}"
        )

    return text.strip()