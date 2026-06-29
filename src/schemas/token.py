from pydantic import BaseModel, Field

class Token(BaseModel):
    """Schema for returning a JWT access token."""
    access_token: str = Field(..., title="Access Token", description="The JWT token string.", example="eyJhbGciOiJIUzI1NiIsInR...")
    token_type: str = Field(..., title="Token Type", description="The type of token returned. Typically 'bearer'.", example="bearer")
