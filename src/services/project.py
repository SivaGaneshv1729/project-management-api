from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.project import ProjectRepository
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.models.user import User

class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def get_all(self, current_user: User):
        return self.repo.get_all_by_owner(current_user.id)

    def create(self, project_in: ProjectCreate, current_user: User):
        return self.repo.create(project_in, current_user.id)

    def _get_project_and_verify_owner(self, project_id: int, current_user: User):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return project

    def get_by_id(self, project_id: int, current_user: User):
        return self._get_project_and_verify_owner(project_id, current_user)

    def update(self, project_id: int, project_in: ProjectUpdate, current_user: User):
        project = self._get_project_and_verify_owner(project_id, current_user)
        return self.repo.update(project, project_in)

    def delete(self, project_id: int, current_user: User):
        project = self._get_project_and_verify_owner(project_id, current_user)
        self.repo.delete(project)
