import os
from app.core.config import settings

# Gunicorn config variables
bind = settings.GUNICORN_BIND
workers = settings.GUNICORN_WORKERS
worker_class = settings.GUNICORN_WORKER_CLASS


def on_starting(server):
    """
    Server 启动前执行的钩子函数(Master 进程)
    只执行一次，用于打印环境信息
    """
    env = os.getenv("APP_ENV", "development")
    print("=" * 60)
    print(f"🚀 Starting {settings.PROJECT_NAME}")
    print("=" * 60)
    print(f"📌 Environment: {env.upper()}")
    print(f"📦 Project Name: {settings.PROJECT_NAME}")
    print(f"🔗 API Version: {settings.API_V1_STR}")
    print(
        f"🗄️ Database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
    )
    print(f"💾 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")
    print(f"👷 Workers: {settings.GUNICORN_WORKERS}")
    print("=" * 60)
