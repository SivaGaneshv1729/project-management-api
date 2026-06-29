from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.controllers import auth_router, users_router, projects_router, tasks_router
from src.database import engine, Base

# In a real app, use Alembic for migrations.
Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "users",
        "description": "Operations to manage user profiles.",
    },
    {
        "name": "projects",
        "description": "Manage projects. Create, read, update, and delete projects.",
    },
    {
        "name": "tasks",
        "description": "Manage tasks within projects. Create, read, update, and delete tasks.",
    },
]

app = FastAPI(
    title="Project Management API",
    description="A containerized RESTful API for project and task management, featuring a strict layered architecture.",
    version="1.0.0",
    contact={
        "name": "Support",
        "url": "http://example.com/contact",
        "email": "support@example.com",
    },
    openapi_tags=tags_metadata
)

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database integrity error, possibly a duplicate entry or missing relation."}
    )

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
