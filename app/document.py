import os
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)
from pydantic import BaseModel

from app.text_chunker import split_text_into_chunks
from app.pdf_processor import extract_text_from_pdf
from app.docx_processor import extract_text_from_docx
from app.embedding import generate_embeddings

from app.vector_store import (
    store_embeddings,
    get_all_documents,
    get_document_details,
    delete_document_vectors,
    search_documents
)

from app.retriever import search_similar_chunks
from app.dependencies import get_current_user
from app.models import User


router = APIRouter()

UPLOAD_DIR = Path("documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Extract document text
def extract_document_text(file_path: str, filename: str):

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        result = extract_text_from_pdf(file_path)

        return {
            "extracted_text": result["extracted_text"],
            "total_pages": result["total_pages"],
            "file_type": "PDF"
        }

    elif extension == ".docx":
        result = extract_text_from_docx(file_path)

        return {
            "extracted_text": result["extracted_text"],
            "total_pages": None,
            "total_paragraphs": result["total_paragraphs"],
            "file_type": "DOCX"
        }

    raise HTTPException(
        status_code=400,
        detail="Only PDF and DOCX files are supported"
    )


# Process and upload document
@router.post("/process-document")
async def process_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    filename = Path(file.filename).name
    extension = Path(filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if extension == ".pdf" and not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # Unique physical filename prevents collisions
    stored_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = UPLOAD_DIR / stored_filename

    try:
        file_path.write_bytes(content)

        result = extract_document_text(
            str(file_path),
            filename
        )

        extracted_text = result["extracted_text"]

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text found in document"
            )

        chunks = split_text_into_chunks(extracted_text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated"
            )

        embeddings = generate_embeddings(chunks)

        storage_result = store_embeddings(
            chunks,
            embeddings,
            filename,
            current_user.id
        )

        return {
            "message": "Document processed successfully",
            "document_id": storage_result["document_id"],
            "filename": filename,
            "file_type": result["file_type"],
            "total_chunks": len(chunks),
            "embedding_dimensions": int(embeddings.shape[1]),
            "embedding_shape": list(embeddings.shape),
            "storage": storage_result
        }

    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise

    except Exception as e:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )


# List documents
@router.get("/list-documents")
async def list_documents(
    current_user: User = Depends(get_current_user)
):

    try:
        result = get_all_documents(
            user_id=current_user.id
        )

        return {
            "message": "Documents retrieved successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Document details
@router.get("/document-details")
async def document_details(
    document_id: str,
    current_user: User = Depends(get_current_user)
):

    try:
        result = get_document_details(
            document_id,
            user_id=current_user.id
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "message": "Document details retrieved successfully",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Delete document
@router.delete("/delete-document")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):

    try:
        document = get_document_details(
            document_id,
            user_id=current_user.id
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        result = delete_document_vectors(
            document_id,
            user_id=current_user.id
        )

        if not result["deleted"]:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "filename": document["filename"],
            "deleted_chunks": result["deleted_chunks"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Document statistics
@router.get("/document-stats")
async def document_stats(
    current_user: User = Depends(get_current_user)
):

    try:
        result = get_all_documents(
            user_id=current_user.id
        )

        total_chunks = sum(
            document["total_chunks"]
            for document in result["documents"]
        )

        return {
            "message": "Document statistics retrieved successfully",
            "total_documents": result["total_documents"],
            "total_chunks": total_chunks
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Search documents
@router.get("/search-documents")
async def search_user_documents(
    search_query: str = None,
    file_type: str = None,
    current_user: User = Depends(get_current_user)
):

    try:
        result = search_documents(
            user_id=current_user.id,
            search_query=search_query,
            file_type=file_type
        )

        return {
            "message": "Documents searched successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Similarity search
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/search")
async def search_document_chunks(
    request: SearchRequest,
    current_user: User = Depends(get_current_user)
):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    try:
        results = search_similar_chunks(
            query=request.query,
            user_id=current_user.id,
            top_k=request.top_k
        )

        return {
            "message": "Similarity search completed successfully",
            "query": request.query,
            "total_results": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
