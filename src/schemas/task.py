from pydantic import BaseModel
from src.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class TaskResponse(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True
