from sqlalchemy.dialects.mysql import BIGINT, TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FSysRoleAuth(Base):
    __tablename__ = "f_sys_role_auth"
    __table_args__ = {"comment": "角色权限表"}

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    role_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="角色ID")
    resource_ids: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="菜单id列表 1,2,3..."
    )
