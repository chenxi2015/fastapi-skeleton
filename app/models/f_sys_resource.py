from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FSysResource(Base):
    __tablename__ = "f_sys_resource"
    __table_args__ = (
        Index("backend_menu_alias_title_unique", "alias", unique=True),
        {"comment": "后台配置资源菜单表"},
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="名称")
    alias: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="别名")
    desc: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="描述")
    f_url: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="前端路由"
    )
    b_url: Mapped[str] = mapped_column(VARCHAR(64), nullable=False, comment="后端接口")
    redirect: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, server_default=text("''"), comment="重定向地址"
    )
    comp_path: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, server_default=text("''"), comment="组件路径"
    )
    icon: Mapped[str] = mapped_column(
        VARCHAR(32), nullable=False, server_default=text("''"), comment="菜单icon"
    )
    c_icon: Mapped[str] = mapped_column(
        VARCHAR(32),
        nullable=False,
        server_default=text("''"),
        comment="自定义icon(优先)",
    )
    parent_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, server_default=text("'0'"), comment="父级ID"
    )
    path: Mapped[str] = mapped_column(
        VARCHAR(64),
        nullable=False,
        server_default=text("''"),
        comment="ID路径 1-2-3...",
    )
    resource_type: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'1'"),
        comment="类型 1：目录 2：菜单 3：操作",
    )
    is_hidden: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="是否隐藏 1:是 0：不是",
    )
    is_cache: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="是否缓存 1:是 0：不是",
    )
    is_external: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="是否外链 1:是 0:不是",
    )
    always_show: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="总是显示 1:是 0:不是",
    )
    breadcrumb_show: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="面包屑显示 1:是 0:不是",
    )
    is_affix: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'0'"),
        comment="是否固定在tab栏 1：是 0：不是",
    )
    res_type: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'1'"),
        comment="资源类型：1：平台型 2：商家型 3：代理商型 4：通用型",
    )
    status: Mapped[int] = mapped_column(
        TINYINT, nullable=False, comment="状态：1：正常 2：停用"
    )
    sort_order: Mapped[int] = mapped_column(
        SMALLINT, nullable=False, server_default=text("'50'"), comment="排序"
    )
    created_at: Mapped[int] = mapped_column(BIGINT, nullable=False)
    updated_at: Mapped[int] = mapped_column(BIGINT, nullable=False)
