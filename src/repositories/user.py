from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            password_hash=get_password_hash(user_in.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
