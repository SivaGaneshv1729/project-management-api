from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.user import UserCreate, UserResponse, UserLogin
from src.schemas.token import Token
from src.services.auth import AuthService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])
users_router = APIRouter(prefix="/api/users", tags=["users"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="The created user object."
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user by providing a valid email and password.
    
    The password will be securely hashed before saving.
    If the email is already registered, a 400 Bad Request error will be returned.
    """
    service = AuthService(db)
    return service.register(user_in)

@router.post(
    "/login",
    response_model=Token,
    summary="Login for access token",
    response_description="A JWT bearer token."
)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JSON Web Token (JWT).
    
    This token should be used in the `Authorization` header as a Bearer token
    for subsequent requests to protected endpoints.
    """
    service = AuthService(db)
    return service.login(user_in)

@users_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user details",
    response_description="Details of the currently authenticated user."
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the profile information of the currently logged-in user.
    """
    return current_user
