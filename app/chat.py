from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.rag_pipeline import generate_rag_response
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


# Chat Request Schema
class ChatRequest(BaseModel):
    query: str
    top_k: int = 3


# Protected Chat API
@router.post("/ask")
async def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    # Step 1: Validate question
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Step 2: Validate top_k
    if not 1 <= request.top_k <= 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10"
        )

    try:
        # Step 3: Generate user-specific RAG response
        response = generate_rag_response(
            query=request.query,
            user_id=current_user.id,
            top_k=request.top_k
        )

        # Step 4: Return response
        return {
            "message": "Answer generated successfully",
            "user_id": current_user.id,
            "data": response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )