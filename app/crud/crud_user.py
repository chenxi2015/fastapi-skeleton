from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash, verify_password
from app.models.f_users import FUsers
from app.schemas.user import UserCreate


class CRUDUser:
    async def get(self, db: AsyncSession, id: int) -> Optional[FUsers]:
        result = await db.execute(select(FUsers).filter(FUsers.id == id))
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[FUsers]:
        result = await db.execute(select(FUsers).filter(FUsers.email == email))
        return result.scalars().first()

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[FUsers]:
        result = await db.execute(select(FUsers).filter(FUsers.username == username))
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> FUsers:
        db_obj = FUsers(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[FUsers]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = CRUDUser()
