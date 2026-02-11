[English](README.md) | [中文](README_zh.md)

# FastAPI Skeleton

This is a robust, scalable, and production-ready FastAPI skeleton framework.

## Features

- **FastAPI**: Modern, fast (high-performance), web framework for building APIs with Python 3.10+.
- **SQLAlchemy 2.0 (Async)**: Modern ORM with async support.
- **MySQL**: Database backend.
- **Redis**: Caching and session storage.
- **JWT Authentication**: Secure authentication with OAuth2PasswordBearer.
- **DAO Pattern**: Clean separation of concerns with `crud/` layer.
- **Custom Middleware**: Request logging and CORS support.
- **Pydantic**: Data validation and settings management.
- **Alembic**: Database migrations.
- **uv**: Modern Python packaging and dependency management.

## Setup using `uv`

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd fastapi-skeleton
    ```

2.  **Install Dependencies with `uv`**:
    This project is managed by `uv`. It will automatically handle virtual environments and dependencies.
    ```bash
    # Install dependencies
    uv sync
    ```

3.  **Environment Variables**:
    Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
    Update `.env` with your database and Redis credentials.

4.  **Run the Application**:
    You can run the application directly using the project's entry point:
    ```bash
    uv run fastapi-skeleton
    ```
    Alternatively, you can use `uvicorn` manually:
    ```bash
    uv run uvicorn app.main:app --reload
    ```

5.  **Access Documentation**:
    Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger UI.

## Multi-Environment Configuration

This project supports dynamic loading of environment variables based on the `APP_ENV` variable.

- **Development (Default)**:
  ```bash
  uv run fastapi-skeleton
  ```
- **Test**:
  ```bash
  APP_ENV=test uv run fastapi-skeleton
  ```
- **Production**:
  ```bash
  APP_ENV=production uv run fastapi-skeleton
  ```

## Database Migrations

This project uses Alembic for database migrations with **fully automated model detection**.

### Adding a New Model (Fully Automated!)

**Just create the model file** - that's it! No manual imports needed.

1.  **Create Model File**:
    ```python
    # app/models/product.py
    from sqlalchemy import Column, Integer, String
    from app.db.base import Base
    
    class Product(Base):
        __tablename__ = "products"
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
    ```

2.  **Generate and Apply Migration**:
    ```bash
    uv run alembic revision --autogenerate -m "add products table"
    uv run alembic upgrade head
    ```

**That's it!** The model is automatically detected. No need to modify `__init__.py` or `env.py`.

### Useful Commands

- **Check current version**: `uv run alembic current`
- **View migration history**: `uv run alembic history`
- **Check database status**: `uv run alembic check`
- **Rollback migration**: `uv run alembic downgrade -1`

📚 **For detailed migration workflow, see [docs/alembic_workflow.md](docs/alembic_workflow.md)**

## Deployment

For production deployment details, see **[docs/deployment.md](docs/deployment.md)**.

## Testing

Run tests using `pytest`:
```bash
uv run pytest
```

## Utility Scripts

Helpful scripts located in the `scripts/` directory:

- **Create Test User**:
  ```bash
  uv run python scripts/create_test_user.py
  ```

## Project Structure

```
fastapi-skeleton/
├── app/
│   ├── api/                # API Endpoints (v1)
│   ├── core/               # Core config, constants & security
│   ├── db/                 # Database & Redis setup
│   ├── models/             # SQLAlchemy Models
│   ├── schemas/            # Pydantic Schemas
│   ├── crud/               # DAO / Repository Layer
│   ├── middleware/         # Custom Middleware (Logging, etc.)
│   └── main.py             # FastAPI Entrypoint
├── alembic/                # Migration scripts
├── scripts/                # Utility scripts (e.g., seeding)
├── tests/                  # Pytest test cases
├── .env.example            # Environment variables example
├── pyproject.toml          # Uv configuration & dependencies
└── requirements.txt        # Pip requirements (Exported via uv)
```
