from typing import Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud_layers.users import get_user_by_username, create_user
from core.database import get_async_session
from core.models.models import User
from core.schemas.users import CreateUser, ReturnUser

router = APIRouter(
    prefix='/user',
    tags=['Users'],
)


@router.post('/', response_model=ReturnUser)
async def create_user_rout(body: CreateUser, session: AsyncSession = Depends(get_async_session)) -> ReturnUser:
    if await get_user_by_username(session, body.username):
        raise HTTPException(status_code=400, detail='Username already registered')
    return await create_user(session, body)


