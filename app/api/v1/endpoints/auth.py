from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from app.db.redis import get_redis
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud.crud_user import user_crud
from app.schemas.user import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # 自动从请求体中提取表单数据
    db: AsyncSession = Depends(deps.get_db),  # 自动从连接池获取一个数据库会话
    redis: Redis = Depends(get_redis),  # 自动从连接池获取一个 Redis 客户端
) -> Any:
    user = await user_crud.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )

    # Store token in Redis
    # Key: token:{access_token} -> user_id
    await redis.set(
        f"token:{access_token}",
        str(user.id),
        ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    # Key: user:{user_id}:token -> access_token (Latest token)
    await redis.set(
        f"user:{user.id}:token",
        access_token,
        ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"access_token": access_token, "token_type": "bearer"}
