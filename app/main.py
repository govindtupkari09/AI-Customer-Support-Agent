from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.document import router as document_router
from app.chat import router as chat_router
from app.auth import router as auth_router
from app.conversation import router as conversation_router
from app.admin import router as admin_router


# Initialize FastAPI
app = FastAPI(
    title="Company AI Knowledge Assistant",
    description="AI-powered company document question answering system",
    version="1.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to Company AI Knowledge Assistant"
    }


# Health Check API
@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }


# Register Routers
app.include_router(
    document_router,
    prefix="/api/documents",
    tags=["Documents"]
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"]
)

app.include_router(
    conversation_router,
    prefix="/api/conversations",
    tags=["Conversation History"]
)

app.include_router(
    admin_router,
    prefix="/api/admin",
    tags=["Admin Dashboard"]
)