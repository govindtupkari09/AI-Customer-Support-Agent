from app.retriever import search_similar_chunks

query = "Tell me about Govind Tupkari's AWS skills and projects."

results = search_similar_chunks(
    query=query,
    user_id=1,
    top_k=4,
    similarity_threshold=0.0
)

print("\n========== RETRIEVAL TEST ==========")
print("Total Results:", len(results))

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Source:", result["source"])
    print("Chunk:", result["chunk_number"])
    print("Similarity:", result["similarity"])
    print("Content:", result["text"][:300])

print("\n===================================")
