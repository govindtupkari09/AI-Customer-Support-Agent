from app.embedding import generate_embeddings
from app.vector_store import collection


def search_similar_chunks(
    query,
    user_id=None,
    top_k=5,
    similarity_threshold=0.30
):
    # Generate query embedding
    query_embedding = generate_embeddings([query])

    # Search across ALL users' documents
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    retrieved_chunks = []

    if not results["documents"] or not results["documents"][0]:
        return retrieved_chunks

    for i in range(len(results["documents"][0])):

        distance = results["distances"][0][i]
        similarity = 1 - distance

        if similarity < similarity_threshold:
            continue

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "document_id": results["metadatas"][0][i]["document_id"],
            "chunk_number": results["metadatas"][0][i]["chunk_number"],
            "distance": distance,
            "similarity": similarity
        })

    return retrieved_chunks