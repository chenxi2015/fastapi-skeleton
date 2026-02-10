from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FSysAdmin(Base):
    __tablename__ = "f_sys_admin"
    __table_args__ = (
        Index("account_index", "account", unique=True),
        Index("dept_id_index", "dept_id"),
        {"comment": "后台管理员表"},
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    uuid: Mapped[str] = mapped_column(VARCHAR(32), nullable=False, comment="唯一id号")
    dept_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="部门ID")
    nick_name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="昵称")
    real_name: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="真实姓名"
    )
    desc: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="描述"
    )
    gender: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="性别 1:男 2:女 0:未知",
    )
    account: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="账号")
    password: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="密码"
    )
    phone: Mapped[str] = mapped_column(
        VARCHAR(16), nullable=False, server_default=text("''"), comment="手机号"
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, server_default=text("''"), comment="邮箱"
    )
    avatar: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, server_default=text("''"), comment="头像"
    )
    salt: Mapped[str] = mapped_column(VARCHAR(32), nullable=False, comment="密码")
    role_ids: Mapped[str] = mapped_column(
        VARCHAR(32), nullable=False, server_default=text("''"), comment="角色IDs"
    )
    type: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'1'"),
        comment="类型：1：平台 2：商家 3：代理商",
    )
    is_main: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'2'"),
        comment="是否主账号 1：是 2：不是",
    )
    is_auth: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'1'"),
        comment="是否认证 1:未认证 2:已认证",
    )
    mfa_secret: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="mfa密钥"
    )
    status: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="状态 1：正常 2：禁用",
    )
    created_by: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, comment="创建者"
    )
    created_at: Mapped[int] = mapped_column(INTEGER, nullable=False)
    updated_by: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, comment="编辑者"
    )
    updated_at: Mapped[int] = mapped_column(INTEGER, nullable=False)
