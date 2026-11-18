from app.vector_store import debug_user_documents

result = debug_user_documents(user_id=1)

print("Total Chunks:", result["total_chunks"])
print("Metadata:", result["metadatas"])
print("Documents:", result["documents"])