from pydantic import BaseModel, Field
from typing import List

class ProjectBase(BaseModel):
    name: str = Field(..., title="Project Name", description="The name of the project.", example="Website Redesign")
    description: str | None = Field(None, title="Project Description", description="A detailed description of the project goals.", example="Redesigning the company website for better UX.")

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass

class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""
    name: str | None = Field(None, title="Project Name", description="The new name of the project.", example="Website Redesign v2")
    description: str | None = Field(None, title="Project Description", description="The new description of the project.", example="Redesigning the company website for better UX in 2024.")

class ProjectResponse(ProjectBase):
    """Schema for returning a project."""
    id: int = Field(..., title="Project ID", description="The unique identifier of the project.", example=1)
    owner_id: int = Field(..., title="Owner ID", description="The unique identifier of the user who owns this project.", example=42)

    class Config:
        from_attributes = True
