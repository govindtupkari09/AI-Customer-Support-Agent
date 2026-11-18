from app.llm import generate_answer

response = generate_answer(
    "What is Large Language Model? Explain in simple English."
)

print("\nGemini Response:")
print(response)
