from src.repositories.user import UserRepository
from src.schemas.user import UserCreate
from src.schemas.user import UserLogin
from src.core.security import verify_password, create_access_token
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.token import Token

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, user_in: UserCreate):
        existing_user = self.repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
        return self.repo.create(user_in)

    def login(self, user_in: UserLogin) -> Token:
        user = self.repo.get_by_email(user_in.email)
        if not user or not verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")
