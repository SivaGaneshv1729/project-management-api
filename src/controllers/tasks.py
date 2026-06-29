from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task import TaskService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api", tags=["tasks"])

@router.post(
    "/projects/{projectId}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The created task."
)
def create_task(projectId: int, task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new task within a specific project.
    
    The user must be the owner of the project to add a task to it.
    """
    service = TaskService(db)
    return service.create(projectId, task_in, current_user)

@router.get(
    "/projects/{projectId}/tasks",
    response_model=List[TaskResponse],
    summary="List all tasks for a project",
    response_description="A list of tasks belonging to the project."
)
def list_tasks(projectId: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all tasks associated with a specific project.
    
    The user must be the owner of the project to view its tasks.
    """
    service = TaskService(db)
    return service.get_all_for_project(projectId, current_user)

@router.get(
    "/tasks/{id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    response_description="The requested task."
)
def get_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a specific task by its ID.
    
    The user must be the owner of the project this task belongs to.
    """
    service = TaskService(db)
    return service.get_by_id(id, current_user)

@router.put(
    "/tasks/{id}",
    response_model=TaskResponse,
    summary="Update a task",
    response_description="The updated task."
)
def update_task(id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update the details or status of an existing task.
    
    The user must be the owner of the project this task belongs to.
    """
    service = TaskService(db)
    return service.update(id, task_in, current_user)

@router.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    response_description="No content upon successful deletion."
)
def delete_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Permanently delete a task.
    
    The user must be the owner of the project this task belongs to.
    """
    service = TaskService(db)
    service.delete(id, current_user)
    return None
