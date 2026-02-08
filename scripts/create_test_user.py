import asyncio
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.crud.crud_user import user_crud
from app.schemas.user import UserCreate


async def create_test_user():
    async with AsyncSessionLocal() as db:
        username = "admin"
        email = "admin@example.com"
        password = "admin888"

        # Check if user already exists
        user = await user_crud.get_by_email(db, email=email)
        if user:
            print(f"User {email} already exists.")
            return

        user_in = UserCreate(
            email=email, username=username, password=password, is_superuser=True
        )

        user = await user_crud.create(db, obj_in=user_in)
        print("Test user created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")


if __name__ == "__main__":
    asyncio.run(create_test_user())
