from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from src.services.project import ProjectService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ProjectService(db)
    return service.create(project_in, current_user)

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ProjectService(db)
    return service.get_all(current_user)

@router.get("/{id}", response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ProjectService(db)
    return service.get_by_id(id, current_user)

@router.put("/{id}", response_model=ProjectResponse)
def update_project(id: int, project_in: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ProjectService(db)
    return service.update(id, project_in, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ProjectService(db)
    service.delete(id, current_user)
    return None
