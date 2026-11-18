from app.retriever import search_similar_chunks
from app.llm import generate_answer


def generate_rag_response(
    query: str,
    user_id: int,
    top_k: int = 3
):

    # Step 1: Retrieve relevant chunks for current user
    retrieved_chunks = search_similar_chunks(
        query=query,
        user_id=user_id,
        top_k=top_k
    )

    # Step 2: Debug retrieved results
    print("\n========== RAG DEBUG ==========")
    print("User ID:", user_id)
    print("Query:", query)
    print("Retrieved Chunks:", len(retrieved_chunks))

    for chunk in retrieved_chunks:
        print("Source:", chunk["source"])
        print("Chunk Number:", chunk["chunk_number"])
        print("Similarity:", chunk["similarity"])

    print("================================")

    # Step 3: Check retrieved results
    if not retrieved_chunks:
        return {
            "query": query,
            "answer": "No relevant information found in your documents.",
            "sources": []
        }

    # Step 4: Prepare context with source labels
    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        context_parts.append(f"""
[Source {index}]
Filename: {chunk['source']}
Chunk Number: {chunk['chunk_number']}

Content:
{chunk['text']}
""")

    context = "\n".join(context_parts)

    print("\nSending context to Gemini...")
    print("Context Length:", len(context))

    # Step 5: Create RAG prompt
    prompt = f"""
You are a Company Knowledge Assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer is unavailable in the context, say so clearly.
3. Add source labels like [Source 1] wherever you use information.
4. Do not invent source labels.
5. Keep the answer clear and easy to understand.
6. If multiple sources contain relevant information, combine them.
7. Do not make assumptions beyond the provided context.

Context:
{context}

User Question:
{query}

Answer:
"""

    # Step 6: Generate answer using Gemini
    try:
        answer = generate_answer(prompt)

        if not answer:
            answer = "The AI model could not generate an answer. Please try again."

        print("\n========== GEMINI RESULT ==========")
        print("Gemini Answer:", answer)
        print("===================================")

    except Exception as e:
        print("\nGemini Generation Error:", str(e))
        raise

    # Step 7: Prepare source citations
    sources = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        sources.append({
            "source_id": index,
            "document_id": chunk["document_id"],
            "filename": chunk["source"],
            "chunk_number": chunk["chunk_number"],
            "similarity_score": round(chunk["similarity"], 4),
            "distance": round(chunk["distance"], 4)
        })

    # Step 8: Return final response
    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }