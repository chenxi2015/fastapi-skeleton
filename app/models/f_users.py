from typing import Optional
from sqlalchemy import Index, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FUsers(Base):
    __tablename__ = "f_users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_id", "id"),
        Index("ix_users_username", "username", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50, "utf8mb4_unicode_ci"), nullable=False)
    username: Mapped[str] = mapped_column(
        String(50, "utf8mb4_unicode_ci"), nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(100, "utf8mb4_unicode_ci"), nullable=False
    )
    is_active: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    is_superuser: Mapped[Optional[int]] = mapped_column(TINYINT(1))
