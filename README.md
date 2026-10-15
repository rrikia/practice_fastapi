**This project is for learning and practicing API development with FastAPI**

A RESTful API built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, CRUD operations, post voting, automated testing, and Docker-based development.

## Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Validation & Configuration:** Pydantic, pydantic-settings
- **Database:** PostgreSQL, SQLAlchemy, Alembic, psycopg2-binary
- **Authentication:** JWT, python-jose, Passlib, bcrypt
- **Testing:** pytest, FastAPI TestClient, HTTPX
- **Containerization:** Docker, Docker Compose
- **Deployment:** Render *(planned)*
- **CI/CD:** GitHub Actions *(planned)*

## Features

- **CRUD operations** for users and posts
- **JWT authentication** with password hashing
- **Voting system** that prevents duplicate votes per user and post
- **SQL joins and aggregations** for dynamic vote counts
- **Database migrations** managed with Alembic
- **Automated tests** using pytest
- **Interactive API documentation** at `/docs`

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Docker Desktop and Docker Compose
- PostgreSQL, if running the application outside Docker

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi
SECRET_KEY=your_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use `DATABASE_HOSTNAME=db` when connecting from the application container through Docker Compose. 

### 3. Install dependencies

```bash
uv sync
```

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

### 5. Start the application

```bash
uv run uvicorn app.main:app --reload
```

Alternatively, run the application and PostgreSQL with Docker Compose:

```bash
docker compose up --build
```

### 6. Run tests

```bash
uv run pytest -v
```

To run the test suite using the dedicated Docker test service, if configured:

```bash
docker -f compose.test.yaml compose run --build --rm tests
```

## API Documentation

Once the application is running, visit:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

## Planned actions

- Deploy the application to Render
- Set up CI/CD with GitHub Actions