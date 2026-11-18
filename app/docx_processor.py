from docx import Document


def extract_text_from_docx(file_path: str):

    doc = Document(file_path)

    extracted_text = ""

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            extracted_text += paragraph.text + "\n"

    return {
        "total_paragraphs": len(doc.paragraphs),
        "extracted_text": extracted_text
    }