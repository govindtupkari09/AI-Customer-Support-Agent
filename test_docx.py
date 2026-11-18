from app.docx_processor import extract_text_from_docx

file_path = "documents/sample.docx"

result = extract_text_from_docx(file_path)

print("\n========== DOCX EXTRACTION ==========")

print("Total Paragraphs:", result["total_paragraphs"])

print("\nExtracted Text:")
print(result["extracted_text"])
