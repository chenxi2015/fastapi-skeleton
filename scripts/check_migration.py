"""Check alembic migration version in database."""

import asyncio
from sqlalchemy import text
from app.db.session import AsyncSessionLocal


async def check_migration_version():
    """Check current migration version in database."""
    async with AsyncSessionLocal() as session:
        # Check if alembic_version table exists
        result = await session.execute(text("SHOW TABLES LIKE 'alembic_version'"))
        table_exists = result.fetchone()

        if not table_exists:
            print("❌ alembic_version 表不存在！")
            print("这意味着数据库从未运行过迁移。")
            return

        print("✅ alembic_version 表存在")

        # Get current version
        result = await session.execute(text("SELECT version_num FROM alembic_version"))
        version = result.fetchone()

        if version:
            print(f"📌 当前数据库版本: {version[0]}")
        else:
            print("⚠️  alembic_version 表为空，没有记录任何版本")

        # Show all tables
        print("\n📋 数据库中的所有表:")
        result = await session.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        for table in tables:
            print(f"  - {table[0]}")


if __name__ == "__main__":
    asyncio.run(check_migration_version())
