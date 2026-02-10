# ============================================
# 阶段 1: 构建阶段 - 安装依赖
# ============================================
FROM python:3.11-slim-bookworm AS builder

# 设置工作目录
WORKDIR /app

# 安装构建依赖（仅在构建阶段需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 从官方镜像安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 复制依赖定义文件
COPY pyproject.toml uv.lock ./

# 安装依赖到 .venv 目录（不安装开发依赖）
RUN uv sync --frozen --no-dev --no-cache

# ============================================
# 阶段 2: 运行阶段 - 最小化镜像
# ============================================
FROM python:3.11-slim-bookworm AS runtime

# 设置工作目录
WORKDIR /app

# 只安装运行时必需的系统依赖（如果有的话）
# 对于大多数 Python 应用，slim 镜像已经足够
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 设置环境变量
ARG APP_ENV=production
ENV APP_ENV=${APP_ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 从构建阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制项目代码（只复制必要的文件）
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# 复制环境配置文件（支持多环境）
COPY .env* ./

# 创建非 root 用户运行应用
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 运行应用
CMD ["gunicorn", "-c", "app/gunicorn_conf.py", "app.main:app"]
