from typing import Optional
from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FSysCasbinRule(Base):
    __tablename__ = "f_sys_casbin_rule"
    __table_args__ = (
        Index(
            "idx_casbin_rule", "ptype", "v0", "v1", "v2", "v3", "v4", "v5", unique=True
        ),
        {"comment": "角色菜单权限表"},
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    v6: Mapped[str] = mapped_column(
        VARCHAR(25), nullable=False, server_default=text("''")
    )
    v7: Mapped[str] = mapped_column(
        VARCHAR(25), nullable=False, server_default=text("''")
    )
    ptype: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v0: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v1: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v2: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v3: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v4: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    v5: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
