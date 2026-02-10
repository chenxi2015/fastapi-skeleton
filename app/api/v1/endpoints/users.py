from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud.crud_user import user_crud
from app.models.f_users import FUsers
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: FUsers = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_crud.create(db, obj_in=user_in)
    return user
