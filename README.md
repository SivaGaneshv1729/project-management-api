# Project Management API

A containerized RESTful API for project and task management, built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.

## Features
- JWT Authentication
- Strict Layered Architecture (Controllers, Services, Repositories)
- Project CRUD operations
- Task CRUD operations (nested and standalone)
- Docker integration with pg_isready health checks

## Quickstart

1. Make sure you have Docker and Docker Compose installed.
2. Clone this repository and navigate to the root directory.
3. Start the application:
   ```bash
   docker-compose up -d --build
   ```

4. The API will be available at `http://localhost:8000`. You can view the automatically generated Swagger UI at `http://localhost:8000/docs`.

## Testing the API

You can register a new user:
`POST /api/auth/register`
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Then login to get a token:
`POST /api/auth/login`
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Use the `access_token` returned to authenticate future requests using the `Authorization: Bearer <token>` header.
