from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.database.database import get_session
from src.models.user import UserCreate, UserRead
from src.services.auth_service import AuthService
from src.api.deps import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from typing import Dict

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=201)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        user = AuthService.register_user(session, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    """
    Login user and return access token
    """
    user = AuthService.authenticate_user(session, email, password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at
        }
    }

@router.post("/logout")
def logout():
    """
    Logout user (currently just a placeholder)
    """
    return {"message": "Logged out successfully"}