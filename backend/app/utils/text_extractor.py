import PyPDF2
from docx import Document
from fastapi import UploadFile
import io

async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    file_obj = io.BytesIO(content)
    
    if file.content_type == "application/pdf":
        return extract_text_from_pdf(file_obj)
    elif file.content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        return extract_text_from_docx(file_obj)
    else:
        raise ValueError(f"Unsupported file format: {file.content_type}")

def extract_text_from_pdf(file_obj: io.BytesIO) -> str:
    reader = PyPDF2.PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_obj: io.BytesIO) -> str:
    document = Document(file_obj)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text