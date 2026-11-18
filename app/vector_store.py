import chromadb
from pathlib import Path
import uuid
from datetime import datetime, timezone


# Persistent ChromaDB storage
CHROMA_DB_PATH = Path("chroma_db")

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

# Create collection
collection = client.get_or_create_collection(
    name="company_documents",
    metadata={"hnsw:space": "cosine"}
)


# Store document embeddings
def store_embeddings(chunks, embeddings, filename, user_id):

    if not chunks:
        raise ValueError("No document chunks available")

    document_id = str(uuid.uuid4())
    uploaded_at = datetime.now(timezone.utc).isoformat()

    filename = Path(filename).name
    file_type = Path(filename).suffix.replace(".", "").upper()

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    vectors = embeddings.tolist()

    # Keep user_id consistent in ChromaDB
    normalized_user_id = str(user_id)

    metadatas = [
        {
            "document_id": document_id,
            "user_id": normalized_user_id,
            "source": filename,
            "file_type": file_type,
            "uploaded_at": uploaded_at,
            "total_chunks": len(chunks),
            "chunk_number": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=vectors,
        metadatas=metadatas
    )

    return {
        "document_id": document_id,
        "user_id": normalized_user_id,
        "filename": filename,
        "file_type": file_type,
        "uploaded_at": uploaded_at,
        "total_chunks": len(chunks),
        "collection_name": collection.name
    }


# Get all documents
def get_all_documents(user_id=None):

    if user_id is not None:
        results = collection.get(
            where={"user_id": str(user_id)},
            include=["metadatas"]
        )
    else:
        results = collection.get(
            include=["metadatas"]
        )

    documents = {}

    for metadata in results["metadatas"] or []:

        document_id = metadata["document_id"]

        if document_id not in documents:

            documents[document_id] = {
                "document_id": document_id,
                "user_id": metadata.get("user_id"),
                "filename": metadata["source"],
                "file_type": metadata["file_type"],
                "uploaded_at": metadata["uploaded_at"],
                "total_chunks": metadata["total_chunks"]
            }

    document_list = list(documents.values())

    return {
        "total_documents": len(document_list),
        "documents": document_list
    }


# Get document details
def get_document_details(document_id: str, user_id=None):

    results = collection.get(
        where={"document_id": document_id},
        include=["metadatas", "documents"]
    )

    if not results["ids"]:
        return None

    first_metadata = results["metadatas"][0]

    if (
        user_id is not None
        and str(first_metadata.get("user_id")) != str(user_id)
    ):
        return None

    chunks = []

    for metadata, document in zip(
        results["metadatas"],
        results["documents"]
    ):
        chunks.append({
            "chunk_number": metadata["chunk_number"],
            "content": document
        })

    return {
        "document_id": document_id,
        "user_id": first_metadata.get("user_id"),
        "filename": first_metadata["source"],
        "file_type": first_metadata["file_type"],
        "uploaded_at": first_metadata["uploaded_at"],
        "total_chunks": first_metadata["total_chunks"],
        "chunks": chunks
    }


# Delete document vectors
def delete_document_vectors(document_id: str, user_id=None):

    results = collection.get(
        where={"document_id": document_id},
        include=["metadatas"]
    )

    if not results["ids"]:
        return {
            "deleted": False,
            "deleted_chunks": 0
        }

    document_owner = results["metadatas"][0].get("user_id")

    if (
        user_id is not None
        and str(document_owner) != str(user_id)
    ):
        return {
            "deleted": False,
            "deleted_chunks": 0
        }

    total_chunks = len(results["ids"])

    collection.delete(
        where={"document_id": document_id}
    )

    return {
        "deleted": True,
        "deleted_chunks": total_chunks
    }


# Debug user documents
def debug_user_documents(user_id):

    results = collection.get(
        where={"user_id": str(user_id)},
        include=["metadatas", "documents"]
    )

    return {
        "total_chunks": len(results["ids"]),
        "ids": results["ids"],
        "metadatas": results["metadatas"],
        "documents": results["documents"]
    }


# Search documents
def search_documents(
    user_id,
    search_query=None,
    file_type=None
):

    result = get_all_documents(user_id=user_id)

    document_list = result["documents"]

    if search_query:

        document_list = [
            doc for doc in document_list
            if search_query.lower() in doc["filename"].lower()
        ]

    if file_type:

        document_list = [
            doc for doc in document_list
            if doc["file_type"].lower() == file_type.lower()
        ]

    return {
        "total_documents": len(document_list),
        "documents": document_list
    }
