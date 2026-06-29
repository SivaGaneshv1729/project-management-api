from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from src.services.project import ProjectService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    response_description="The created project."
)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new project with the authenticated user as the owner.
    """
    service = ProjectService(db)
    return service.create(project_in, current_user)

@router.get(
    "",
    response_model=List[ProjectResponse],
    summary="List all projects",
    response_description="A list of projects owned by the user."
)
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all projects that belong to the currently authenticated user.
    """
    service = ProjectService(db)
    return service.get_all(current_user)

@router.get(
    "/{id}",
    response_model=ProjectResponse,
    summary="Get a project by ID",
    response_description="The requested project."
)
def get_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a specific project by its ID.
    
    Users can only access their own projects.
    """
    service = ProjectService(db)
    return service.get_by_id(id, current_user)

@router.put(
    "/{id}",
    response_model=ProjectResponse,
    summary="Update a project",
    response_description="The updated project."
)
def update_project(id: int, project_in: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update the details of an existing project.
    
    Only the owner of the project can update it.
    """
    service = ProjectService(db)
    return service.update(id, project_in, current_user)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    response_description="No content upon successful deletion."
)
def delete_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a project and all of its associated tasks permanently.
    
    Only the owner of the project can delete it.
    """
    service = ProjectService(db)
    service.delete(id, current_user)
    return None
