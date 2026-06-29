from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(..., title="Email Address", description="The user's email address, which is used for login.", example="user@example.com")

class UserCreate(UserBase):
    """Schema for registering a new user."""
    password: str = Field(..., title="Password", description="A strong password for the account.", min_length=8, example="strongpassword123")

class UserResponse(UserBase):
    """Schema for returning user profile details."""
    id: int = Field(..., title="User ID", description="The unique identifier of the user.", example=42)
    created_at: datetime = Field(..., title="Created At", description="The timestamp when the user account was created.")
    updated_at: datetime | None = Field(None, title="Updated At", description="The timestamp when the user account was last updated.")

    class Config:
        from_attributes = True

class UserLogin(UserBase):
    """Schema for user login credentials."""
    password: str = Field(..., title="Password", description="The user's password.", example="strongpassword123")
