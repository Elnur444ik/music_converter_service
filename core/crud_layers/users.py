from typing import Union

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.models import User
from core.schemas.users import CreateUser, ReturnUser


async def get_user_by_username(db: AsyncSession, username: str) -> Union[UUID4, None]:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# async def get_user_by_id(db: AsyncSession, user_id: UUID4) -> Union[UUID4, None]:
#     query = select(User).where(User.id == user_id)
#     result = await db.execute(query)
#     return result.scalar_one_or_none()

async def check_user_token(db: AsyncSession, user_id: UUID4, access_token: UUID4) -> Union[UUID4, None]:
    query = select(User).filter_by(User.id == user_id, User.token == access_token)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: CreateUser) -> ReturnUser:
    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    return new_user.id, new_user.token
