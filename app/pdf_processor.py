from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(file_path: str):

    pdf = PdfReader(file_path)

    extracted_text = ""

    for page_number, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        if text:
            extracted_text += f"\n{text}"

    return {
        "total_pages": len(pdf.pages),
        "extracted_text": extracted_text
    }