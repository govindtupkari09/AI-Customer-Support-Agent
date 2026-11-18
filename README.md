# 🤖 AI Customer Support Agent
### Intelligent AI-Powered Customer Support System

An AI-powered customer support application designed to answer user queries using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and document-based knowledge retrieval.

## 🚀 Project Overview

AI Customer Support Agent is a full-stack application that helps users interact with an AI assistant and get intelligent responses.

The system combines a Python FastAPI backend, React frontend, Google Gemini API, and vector-based document retrieval to provide context-aware responses.

## ✨ Key Features

- AI-powered conversational interface.
- Document upload and management.
- Retrieval-Augmented Generation (RAG).
- PDF and DOCX document processing.
- Text chunking and embedding generation.
- Semantic document retrieval.
- Google Gemini API integration.
- User registration and login.
- Secure authentication.
- Vector storage using ChromaDB.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python, JavaScript |
| Backend | FastAPI |
| Frontend | React.js, HTML, CSS |
| AI / LLM | Google Gemini API |
| AI Framework | LangChain |
| RAG | Embeddings, Text Chunking, Semantic Search |
| Vector Database | ChromaDB |
| Database | PostgreSQL |
| Document Processing | PyMuPDF, Python-docx |
| Tools | Git, GitHub, VS Code |

*Note: Verify each technology against the implemented code and requirements before publishing.*

## 📁 Project Structure

```text
AI-Customer-Support-Agent/
│
├── app/
│   ├── admin.py
│   ├── auth.py
│   ├── chat.py
│   ├── conversation.py
│   ├── database.py
│   ├── document.py
│   ├── embedding.py
│   ├── llm.py
│   ├── main.py
│   ├── models.py
│   ├── pdf_processor.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── security.py
│   ├── text_chunker.py
│   └── vector_store.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/govindtupkari09/AI-Customer-Support-Agent.git
```

### 2. Navigate to Project

```bash
cd AI-Customer-Support-Agent
```

### 3. Create Python Virtual Environment

```bash
python -m venv .venv
```

Activate environment on Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never upload your `.env` file or API keys to GitHub.

### 6. Run Backend

Use the actual FastAPI entry point configured in `app/main.py`:

```bash
uvicorn app.main:app --reload
```

### 7. Run Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

## 🧠 How RAG Works

1. Upload documents.
2. Extract text from documents.
3. Split text into smaller chunks.
4. Generate embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve relevant information based on user queries.
7. Generate responses using Google Gemini.

## 🔐 Security

- Environment variables for API credentials.
- Password hashing and authentication.
- Sensitive files excluded using `.gitignore`.

## 👨‍💻 Developer

**Govind Tupkari**

B.E. Electronics & Telecommunication Engineering

Pune, Maharashtra, India

GitHub: https://github.com/govindtupkari09

## 📌 GitHub Repository

https://github.com/govindtupkari09/AI-Customer-Support-Agent
