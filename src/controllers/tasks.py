from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task import TaskService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api", tags=["tasks"])

@router.post("/projects/{projectId}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(projectId: int, task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TaskService(db)
    return service.create(projectId, task_in, current_user)

@router.get("/projects/{projectId}/tasks", response_model=List[TaskResponse])
def list_tasks(projectId: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TaskService(db)
    return service.get_all_for_project(projectId, current_user)

@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TaskService(db)
    return service.get_by_id(id, current_user)

@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TaskService(db)
    return service.update(id, task_in, current_user)

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = TaskService(db)
    service.delete(id, current_user)
    return None
