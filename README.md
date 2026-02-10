[English](#fastapi-skeleton) | [中文](#fastapi-skeleton-中文)

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
    Use `uv run` to execute commands within the project's environment.
    ```bash
    uv run uvicorn app.main:app --reload
    ```

5.  **Access Documentation**:
    Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger UI.

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

---

# FastAPI Skeleton (中文)

这是一个健壮、可扩展且已准备好投入生产的 FastAPI 脚手架框架。

## 功能特性

- **FastAPI**: 现代、高性能的 Python 3.10+ Web 框架。
- **SQLAlchemy 2.0 (Async)**: 支持异步的现代 ORM。
- **MySQL**: 数据库后端。
- **Redis**: 缓存和会话存储。
- **JWT 认证**: 使用 OAuth2PasswordBearer 的安全认证。
- **DAO 模式**: 使用 `crud/` 层实现清晰的关注点分离。
- **自定义中间件**: 请求日志记录和 CORS 支持。
- **Pydantic**: 数据验证和设置管理。
- **Alembic**: 数据库迁移。
- **uv**: 现代 Python 包管理工具。

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

本项目使用 Alembic 进行数据库迁移，支持**完全自动化的模型检测**。

### 添加新模型（完全自动化！）

**只需创建模型文件** - 就这样！无需手动导入。

1.  **创建模型文件**:
    ```python
    # app/models/product.py
    from sqlalchemy import Column, Integer, String
    from app.db.base import Base
    
    class Product(Base):
        __tablename__ = "products"
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
    ```

2.  **生成并应用迁移**:
    ```bash
    uv run alembic revision --autogenerate -m "添加 products 表"
    uv run alembic upgrade head
    ```

**就这样！** 模型会被自动检测。无需修改 `__init__.py` 或 `env.py`。

### 常用命令

- **查看当前版本**: `uv run alembic current`
- **查看迁移历史**: `uv run alembic history`
- **检查数据库状态**: `uv run alembic check`
- **回滚迁移**: `uv run alembic downgrade -1`

📚 **详细的迁移工作流程请参考 [docs/alembic_workflow.md](docs/alembic_workflow.md)**

## 测试

使用 `pytest` 运行测试：
```bash
uv run pytest
```

## 工具脚本

位于 `scripts/` 目录下的实用脚本：

- **创建测试用户**:
  ```bash
  uv run python scripts/create_test_user.py
  ```

## 项目结构

```
fastapi-skeleton/
├── app/
│   ├── api/                # API 端点
│   ├── core/               # 核心配置和安全
│   ├── db/                 # 数据库和 Redis 设置
│   ├── models/             # SQLAlchemy 模型
│   ├── schemas/            # Pydantic 模式
│   ├── crud/               # DAO / 仓库层
│   ├── middleware/         # 自定义中间件
│   └── main.py             # 入口点
├── alembic/                # 迁移脚本
├── scripts/                # 工具脚本
├── tests/                  # 测试用例
├── .env.example            # 环境变量示例
├── pyproject.toml          # Uv 配置
└── requirements.txt        # Pip 依赖
```

