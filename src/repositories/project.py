from sqlalchemy.orm import Session
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate
from typing import List

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_all_by_owner(self, owner_id: int) -> List[Project]:
        return self.db.query(Project).filter(Project.owner_id == owner_id).all()

    def create(self, project_in: ProjectCreate, owner_id: int) -> Project:
        db_project = Project(
            name=project_in.name,
            description=project_in.description,
            owner_id=owner_id
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def update(self, db_project: Project, project_in: ProjectUpdate) -> Project:
        if project_in.name is not None:
            db_project.name = project_in.name
        if project_in.description is not None:
            db_project.description = project_in.description
        
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete(self, db_project: Project) -> None:
        self.db.delete(db_project)
        self.db.commit()
