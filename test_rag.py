from app.rag_pipeline import generate_rag_response

query = "What is an LLM?"

response = generate_rag_response(
    query=query,
    top_k=3
)

print("\n========== RAG RESPONSE ==========")

print("\nQuestion:")
print(response["query"])

print("\nAI Answer:")
print(response["answer"])

print("\nSources:")
for source in response["sources"]:
    print(
        f"File: {source['filename']} | "
        f"Chunk: {source['chunk_number']}"
    )
    