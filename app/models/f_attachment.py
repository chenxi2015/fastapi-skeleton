from sqlalchemy import text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.db.base import Base


class FAttachment(Base):
    __tablename__ = "f_attachment"
    __table_args__ = {"comment": "附件表"}

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, server_default=text("'0'"), comment="附件上传的用户id"
    )
    attach_name: Mapped[str] = mapped_column(
        VARCHAR(64), nullable=False, server_default=text("''"), comment="附件新名称"
    )
    attach_origin_name: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False, server_default=text("''"), comment="附件原名称"
    )
    attach_url: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False, comment="附件地址"
    )
    attach_type: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        server_default=text("'1'"),
        comment="附件类型 1：图片 2：视频 3：文件",
    )
    attach_mimetype: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, server_default=text("''"), comment="附件mime类型"
    )
    attach_extension: Mapped[str] = mapped_column(
        VARCHAR(16), nullable=False, server_default=text("''"), comment="附件后缀名"
    )
    attach_size: Mapped[str] = mapped_column(
        VARCHAR(32), nullable=False, server_default=text("''"), comment="附件大小"
    )
    status: Mapped[int] = mapped_column(
        TINYINT, nullable=False, comment="状态 1：正常 0：删除"
    )
    created_at: Mapped[int] = mapped_column(
        INTEGER, nullable=False, server_default=text("'0'")
    )
    updated_at: Mapped[int] = mapped_column(
        INTEGER, nullable=False, server_default=text("'0'")
    )
