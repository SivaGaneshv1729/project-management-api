from sqlalchemy.orm import Session
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from typing import List

class TaskRepository:
    """
    Data access layer for Task entities.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by its primary key ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_by_project(self, project_id: int) -> List[Task]:
        """Retrieve all tasks associated with a specific project."""
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def create(self, task_in: TaskCreate, project_id: int) -> Task:
        """Create a new task record in the database."""
        db_task = Task(
            title=task_in.title,
            description=task_in.description,
            status=task_in.status,
            project_id=project_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, db_task: Task, task_in: TaskUpdate) -> Task:
        """Update an existing task record."""
        if task_in.title is not None:
            db_task.title = task_in.title
        if task_in.description is not None:
            db_task.description = task_in.description
        if task_in.status is not None:
            db_task.status = task_in.status
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, db_task: Task) -> None:
        """Delete a task record from the database."""
        self.db.delete(db_task)
        self.db.commit()
