from src.repositories.user import UserRepository
from src.schemas.user import UserCreate
from src.schemas.user import UserLogin
from src.core.security import verify_password, create_access_token
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.token import Token

class AuthService:
    """
    Service layer for authentication and user registration logic.
    Handles business validation and interfaces with the UserRepository.
    """
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, user_in: UserCreate):
        """
        Register a new user.

        Checks if the email is already in use. If it is, raises a 409 Conflict.
        Otherwise, delegates to the repository to hash the password and create the user.

        Args:
            user_in (UserCreate): The user registration details.

        Returns:
            User: The newly created User model instance.
        """
        existing_user = self.repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
        return self.repo.create(user_in)

    def login(self, user_in: UserLogin) -> Token:
        """
        Authenticate a user and generate a JWT access token.

        Validates the provided email and password against the database.
        If validation fails, raises a 401 Unauthorized.

        Args:
            user_in (UserLogin): The user's login credentials.

        Returns:
            Token: A Pydantic model containing the JWT and token type.
        """
        user = self.repo.get_by_email(user_in.email)
        if not user or not verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")
