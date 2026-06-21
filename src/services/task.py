from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.task import TaskRepository
from src.repositories.project import ProjectRepository
from src.schemas.task import TaskCreate, TaskUpdate
from src.models.user import User

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    def _verify_project_ownership(self, project_id: int, current_user: User):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return project

    def get_all_for_project(self, project_id: int, current_user: User):
        self._verify_project_ownership(project_id, current_user)
        return self.repo.get_all_by_project(project_id)

    def create(self, project_id: int, task_in: TaskCreate, current_user: User):
        self._verify_project_ownership(project_id, current_user)
        return self.repo.create(task_in, project_id)

    def _get_task_and_verify_ownership(self, task_id: int, current_user: User):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        self._verify_project_ownership(task.project_id, current_user)
        return task

    def get_by_id(self, task_id: int, current_user: User):
        return self._get_task_and_verify_ownership(task_id, current_user)

    def update(self, task_id: int, task_in: TaskUpdate, current_user: User):
        task = self._get_task_and_verify_ownership(task_id, current_user)
        return self.repo.update(task, task_in)

    def delete(self, task_id: int, current_user: User):
        task = self._get_task_and_verify_ownership(task_id, current_user)
        self.repo.delete(task)
