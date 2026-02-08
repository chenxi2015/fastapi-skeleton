from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,  # Set to False in production
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定异步会话类
    expire_on_commit=False,  # 提交后不立即过期会话中的对象
    autoflush=False,  # 提交前不自动刷新
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
