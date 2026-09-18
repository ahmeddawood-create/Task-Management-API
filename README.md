# FastAPI Task API

A FastAPI CRUD service for managing tasks. Tasks are stored in PostgreSQL through SQLModel, and Supabase provides authentication for the user-related endpoints.

## Requirements

- Python 3.13 or Docker
- A Supabase project for authentication

## Configuration

Create a `.env` file in the project root. It is ignored by Git.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_DB=tasks
POSTGRES_PORT=5432

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

When using Docker Compose, `DATABASE_URL` is assembled automatically from the PostgreSQL values above. For a local process, add the connection string explicitly:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your-postgres-password@localhost:5432/tasks
```

## Run With Docker

```powershell
docker compose up --build
```

The API is available at `http://localhost:8000`. Stop the containers with:

```powershell
docker compose down
```

## Run Locally

Create a virtual environment, install the dependencies, and start Uvicorn from the `app` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### General

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns the API name, version, and main endpoint path. |
| `GET` | `/health` | Returns the service health status. |

### Tasks

| Method | Path | Description | Success |
| :--- | :--- | :--- | :--- |
| `GET` | `/tasks` | Returns all tasks. | `200 OK` |
| `GET` | `/tasks/{id}` | Returns one task by integer ID. | `200 OK` |
| `POST` | `/tasks` | Creates a task with a `title`. | `201 Created` |
| `PUT` | `/tasks/{id}` | Updates `title`, `done`, or both. | `200 OK` |
| `DELETE` | `/tasks/{id}` | Deletes a task by ID. | `204 No Content` |

Task objects have this shape:

```json
{
    "id": 1,
    "title": "Pack your bag",
    "done": false
}
```

Create a task:

```powershell
curl -X POST http://localhost:8000/tasks `
    -H "Content-Type: application/json" `
    -d '{"title":"Read the documentation"}'
```

Update a task:

```powershell
curl -X PUT http://localhost:8000/tasks/1 `
    -H "Content-Type: application/json" `
    -d '{"done":true}'
```

### Authentication

| Method | Path | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | Creates a Supabase user. | None |
| `POST` | `/auth/login` | Signs in a user and returns access tokens. | None |
| `POST` | `/auth/logout` | Signs out the current user. | Bearer token |
| `GET` | `/public/info` | Returns public information. | None |
| `GET` | `/protected/profile` | Returns the authenticated user profile. | Bearer token |

Sign up or log in with this request body:

```json
{
    "email": "user@example.com",
    "password": "your-password"
}
```

For protected endpoints, send the access token returned by `/auth/login`:

```powershell
curl http://localhost:8000/protected/profile `
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database

The application creates the `tasks` table on startup and seeds three tasks when the table is empty. PostgreSQL data is persisted in the `postgres_data` Docker volume.

