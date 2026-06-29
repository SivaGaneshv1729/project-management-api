from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.task import TaskRepository
from src.repositories.project import ProjectRepository
from src.schemas.task import TaskCreate, TaskUpdate
from src.models.user import User

class TaskService:
    """
    Service layer for task management logic.
    Ensures that tasks can only be managed by the owner of the project they belong to.
    """
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    def _verify_project_ownership(self, project_id: int, current_user: User):
        """
        Verify that the user is the owner of the given project.
        
        Raises:
            HTTPException (404): If the project does not exist.
            HTTPException (403): If the user is not the owner.
        """
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return project

    def get_all_for_project(self, project_id: int, current_user: User):
        """
        Retrieve all tasks for a given project, verifying project ownership.
        """
        self._verify_project_ownership(project_id, current_user)
        return self.repo.get_all_by_project(project_id)

    def create(self, project_id: int, task_in: TaskCreate, current_user: User):
        """
        Create a new task under a given project, verifying project ownership.
        """
        self._verify_project_ownership(project_id, current_user)
        return self.repo.create(task_in, project_id)

    def _get_task_and_verify_ownership(self, task_id: int, current_user: User):
        """
        Helper method to retrieve a task and verify its parent project is owned by the user.
        
        Raises:
            HTTPException (404): If the task does not exist.
            HTTPException (403): If the user is not the owner of the project.
        """
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        self._verify_project_ownership(task.project_id, current_user)
        return task

    def get_by_id(self, task_id: int, current_user: User):
        """
        Retrieve a specific task by its ID, verifying ownership.
        """
        return self._get_task_and_verify_ownership(task_id, current_user)

    def update(self, task_id: int, task_in: TaskUpdate, current_user: User):
        """
        Update a task's details, verifying ownership.
        """
        task = self._get_task_and_verify_ownership(task_id, current_user)
        return self.repo.update(task, task_in)

    def delete(self, task_id: int, current_user: User):
        """
        Delete a task, verifying ownership.
        """
        task = self._get_task_and_verify_ownership(task_id, current_user)
        self.repo.delete(task)
