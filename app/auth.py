from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import User
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.dependencies import get_current_user

router = APIRouter()

# User Registration Request Schema
class UserRegister(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    # User Registration API
@router.post("/register")
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Step 1: Check existing email
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Step 2: Hash password
    hashed_password = hash_password(user_data.password)

    # Step 3: Create new user
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    # Step 4: Save user in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Step 5: Return response
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email
        }
        
    }
# User Login Request Schema
class UserLogin(BaseModel):

    email: EmailStr

    password: str

# User Login API
@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # Step 1: Find user by email
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    # Step 2: Verify credentials
    if not user or not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Step 3: Check account status
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    # Step 4: Generate JWT token
    access_token = create_access_token(
        data={"sub": user.email}
    )

    # Step 5: Return response
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }

# Protected User Profile API
@router.get("/profile")
def get_user_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "message": "Authenticated user profile",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email
        }
    }