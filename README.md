[English](#fastapi-skeleton) | [中文](#fastapi-skeleton-中文)

# FastAPI Skeleton

This is a robust, scalable, and production-ready FastAPI skeleton framework.

## Features

- **FastAPI**: Modern, fast (high-performance), web framework for building APIs with Python 3.10+.
- **SQLAlchemy 2.0 (Async)**: Modern ORM with async support.
- **MySQL**: Database backend.
- **Redis**: Caching and session storage.
- **JWT Authentication**: Secure authentication with OAuth2PasswordBearer.
- **Pydantic**: Data validation and settings management.
- **Alembic**: Database migrations.
- **Docker Compose**: Easy local development setup.

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
    Use `uv run` to execute commands within the project's environment.
    ```bash
    uv run uvicorn app.main:app --reload
    ```

5.  **Access Documentation**:
    Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger UI.

## Database Migrations

This project uses Alembic for database migrations.

1.  **Generate Migration**:
    After modifying models in `app/models`, run:
    ```bash
    uv run alembic revision --autogenerate -m "Description of changes"
    ```

2.  **Apply Migration**:
    To apply changes to the database:
    ```bash
    uv run alembic upgrade head
    ```

## Project Structure

```
fastapi-skeleton/
├── app/
│   ├── api/                # API Endpoints
│   ├── core/               # Core config & security
│   ├── db/                 # Database setup
│   ├── models/             # SQLAlchemy Models
│   ├── schemas/            # Pydantic Schemas
│   ├── crud/               # DAO / Repository
│   ├── middleware/         # Custom Middleware
│   └── main.py             # Entrypoint
├── alembic/                # Migration scripts
├── tests/                  # Tests
├── .env.example            # Environment variables example
├── pyproject.toml          # Uv config
└── requirements.txt        # Pip requirements (Generated via uv export)
```

---

# FastAPI Skeleton (中文)

这是一个健壮、可扩展且已准备好投入生产的 FastAPI 脚手架框架。

## 功能特性

- **FastAPI**: 现代、高性能的 Python 3.10+ Web 框架。
- **SQLAlchemy 2.0 (Async)**: 支持异步的现代 ORM。
- **MySQL**: 数据库后端。
- **Redis**: 缓存和会话存储。
- **JWT 认证**: 使用 OAuth2PasswordBearer 的安全认证。
- **Pydantic**: 数据验证和设置管理。
- **Alembic**: 数据库迁移。
- **Docker Compose**: 简易的本地开发环境设置。

## 使用 `uv` 进行设置

1.  **克隆仓库**:
    ```bash
    git clone <repo_url>
    cd fastapi-skeleton
    ```

2.  **使用 `uv` 安装依赖**:
    本项目使用 `uv` 进行管理。它将自动处理虚拟环境和依赖项。
    ```bash
    # 安装依赖
    uv sync
    ```

3.  **环境变量**:
    将 `.env.example` 复制为 `.env`:
    ```bash
    cp .env.example .env
    ```
    更新 `.env` 中的数据库和 Redis 凭据。

4.  **运行应用程序**:
    使用 `uv run` 在项目环境中执行命令。
    ```bash
    uv run uvicorn app.main:app --reload
    ```

5.  **访问文档**:
    打开 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 Swagger UI。

## 数据库迁移

本项目使用 Alembic 进行数据库迁移。

1.  **生成迁移脚本**:
    在修改 `app/models` 中的模型后，运行：
    ```bash
    uv run alembic revision --autogenerate -m "修改描述"
    ```

2.  **应用迁移**:
    将更改应用到数据库：
    ```bash
    uv run alembic upgrade head
    ```

## 项目结构

```
fastapi-skeleton/
├── app/
│   ├── api/                # API 端点
│   ├── core/               # 核心配置和安全
│   ├── db/                 # 数据库设置
│   ├── models/             # SQLAlchemy 模型
│   ├── schemas/            # Pydantic 模式
│   ├── crud/               # DAO / 仓库层
│   ├── middleware/         # 自定义中间件
│   └── main.py             # 入口点
├── tests/                  # 测试
├── .env.example            # 环境变量示例
├── pyproject.toml          # Uv 配置
└── requirements.txt        # Pip 依赖 (通过 uv export 生成)
```
