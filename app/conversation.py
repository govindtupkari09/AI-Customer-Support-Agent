from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import Conversation, ChatMessage, User
from app.dependencies import get_current_user

router = APIRouter()


# Create Conversation Schema
class ConversationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


# 1. Create New Conversation
@router.post("/create")
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    title = request.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Conversation title cannot be empty"
        )

    conversation = Conversation(
        user_id=current_user.id,
        title=title
    )

    try:
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return {
            "message": "Conversation created successfully",
            "conversation_id": conversation.id,
            "title": conversation.title
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create conversation"
        )


# 2. Get All Conversations
@router.get("/list")
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return {
        "total_conversations": len(conversations),
        "conversations": [
            {
                "conversation_id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at
            }
            for conversation in conversations
        ]
    }


# 3. Get Conversation Messages
@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "total_messages": len(messages),
        "messages": [
            {
                "message_id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }
            for message in messages
        ]
    }


# 4. Delete Conversation
@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    try:
        db.query(ChatMessage).filter(
            ChatMessage.conversation_id == conversation_id
        ).delete(synchronize_session=False)

        db.delete(conversation)
        db.commit()

        return {
            "message": "Conversation deleted successfully",
            "conversation_id": conversation_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete conversation"
        )