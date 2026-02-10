from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FSysRole(Base):
    __tablename__ = "f_sys_role"
    __table_args__ = (Index("name", "name", unique=True), {"comment": "角色表"})

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    mch_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, comment="商家ID 0:非商家"
    )
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="角色名称")
    code: Mapped[str] = mapped_column(
        VARCHAR(16), nullable=False, comment="角色唯一code"
    )
    desc: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="角色描述"
    )
    is_sys: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="是否系统角色 1：是 0：否",
    )
    role_type: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        comment="角色类型：1：平台类型 2：商家类型 3：代理商类型",
    )
    status: Mapped[int] = mapped_column(
        TINYINT, nullable=False, comment="状态：1正常(默认) 2停用"
    )
    created_at: Mapped[int] = mapped_column(INTEGER, nullable=False)
    updated_at: Mapped[int] = mapped_column(INTEGER, nullable=False)
