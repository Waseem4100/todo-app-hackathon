from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate
from ..api.deps import hash_password, verify_password
from datetime import timedelta
from fastapi import HTTPException

class AuthService:
    @staticmethod
    def register_user(session: Session, user_data: UserCreate) -> User:
        # Check if user with email already exists
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")

        # Verify password confirmation matches
        if user_data.password != user_data.password_confirm:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Hash the password
        try:
            hashed_password = hash_password(user_data.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Create new user
        db_user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        # Find user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        # Verify user exists and password is correct
        if not user or not verify_password(password, user.password_hash):
            return None

        return user