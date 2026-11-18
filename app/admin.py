from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import User, Conversation, ChatMessage
from app.dependencies import get_admin_user
from app.vector_store import collection

router = APIRouter()


# ==========================================
# PYDANTIC SCHEMAS
# ==========================================

class UserStatusUpdate(BaseModel):
    is_active: bool


class UserRoleUpdate(BaseModel):
    role: str = Field(pattern="^(admin|user)$")


# ==========================================
# ADMIN DASHBOARD API
# ==========================================

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):

    try:

        # ======================================
        # 1. USER STATISTICS
        # ======================================

        total_users = db.query(User).count()

        active_users = db.query(User).filter(
            User.is_active == True
        ).count()

        inactive_users = total_users - active_users


        # ======================================
        # 2. CONVERSATION STATISTICS
        # ======================================

        total_conversations = db.query(Conversation).count()


        # ======================================
        # 3. CHAT MESSAGE STATISTICS
        # ======================================

        total_messages = db.query(ChatMessage).count()


        # ======================================
        # 4. DOCUMENT STATISTICS
        # ======================================

        all_documents = collection.get(
            include=["metadatas"]
        )

        document_map = {}

        for metadata in all_documents["metadatas"]:

            document_id = metadata["document_id"]

            if document_id not in document_map:

                document_map[document_id] = {
                    "document_id": document_id,
                    "filename": metadata["source"],
                    "user_id": metadata.get("user_id"),
                    "total_chunks": metadata["total_chunks"]
                }

        total_documents = len(document_map)

        total_chunks = len(all_documents["ids"])


        # ======================================
        # 5. FINAL DASHBOARD RESPONSE
        # ======================================

        return {
            "message": "Dashboard statistics retrieved successfully",

            "admin": {
                "admin_id": current_user.id,
                "admin_name": current_user.full_name,
                "admin_email": current_user.email,
                "role": current_user.role
            },

            "dashboard": {

                "users": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "inactive_users": inactive_users
                },

                "documents": {
                    "total_documents": total_documents,
                    "total_chunks": total_chunks
                },

                "conversations": {
                    "total_conversations": total_conversations,
                    "total_messages": total_messages
                }
            }
        }

    except Exception as e:

        print("Admin Dashboard Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dashboard statistics"
        )

# ==========================================
# GET ALL USERS
# ==========================================

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    users = db.query(User).order_by(User.id.desc()).all()

    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at
            }
            for user in users
        ]
    }


# ==========================================
# GET USER DETAILS
# ==========================================

@router.get("/users/{user_id}")
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at
    }


# ==========================================
# UPDATE USER STATUS
# ==========================================

@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    request: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id and not request.is_active:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot deactivate their own account"
        )

    user.is_active = request.is_active
    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated successfully",
        "user_id": user.id,
        "is_active": user.is_active
    }


# ==========================================
# UPDATE USER ROLE
# ==========================================

@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    request: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id and request.role != "admin":
        raise HTTPException(
            status_code=400,
            detail="Admin cannot remove their own admin role"
        )

    user.role = request.role
    db.commit()
    db.refresh(user)

    return {
        "message": "User role updated successfully",
        "user_id": user.id,
        "role": user.role
    }


# ==========================================
# DELETE USER
# ==========================================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete their own account"
        )

    try:
        db.query(ChatMessage).filter(
            ChatMessage.conversation_id.in_(
                db.query(Conversation.id).filter(
                    Conversation.user_id == user_id
                )
            )
        ).delete(synchronize_session=False)

        db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).delete(synchronize_session=False)

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully",
            "user_id": user_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )