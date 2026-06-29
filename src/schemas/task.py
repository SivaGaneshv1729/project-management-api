from pydantic import BaseModel, Field
from src.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., title="Task Title", description="The title of the task.", example="Update documentation")
    description: str | None = Field(None, title="Task Description", description="A detailed description of what needs to be done.", example="Rewrite the README file to include setup instructions.")
    status: TaskStatus = Field(TaskStatus.TODO, title="Task Status", description="The current status of the task.", example="TODO")

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str | None = Field(None, title="Task Title", description="The new title of the task.", example="Update documentation")
    description: str | None = Field(None, title="Task Description", description="The new description of the task.", example="Rewrite the README file.")
    status: TaskStatus | None = Field(None, title="Task Status", description="The new status of the task.", example="IN_PROGRESS")

class TaskResponse(TaskBase):
    """Schema for returning a task."""
    id: int = Field(..., title="Task ID", description="The unique identifier of the task.", example=10)
    project_id: int = Field(..., title="Project ID", description="The unique identifier of the project this task belongs to.", example=1)

    class Config:
        from_attributes = True
