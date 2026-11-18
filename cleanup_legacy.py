import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="company_documents"
)

# Get all existing records
results = collection.get(
    include=["metadatas"]
)

legacy_ids = []

# Find records without document_id
for record_id, metadata in zip(
    results["ids"],
    results["metadatas"]
):
    if "document_id" not in metadata:
        legacy_ids.append(record_id)

# Delete old-format records
if legacy_ids:
    collection.delete(ids=legacy_ids)

print("Legacy records deleted:", len(legacy_ids))
print("Remaining records:", collection.count())