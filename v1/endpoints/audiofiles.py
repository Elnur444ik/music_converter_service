from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud_layers.audiofiles import add_new_audio, get_audio_by_id
from core.crud_layers.users import get_user_by_id, check_user_token
from core.database import get_async_session
from core.schemas.audiofiles import ReturnAudio, AddAudio, ReturnURL
from v1.utils.audiofiles import convert_audio

router = APIRouter(
    prefix='/',
    tags=['AudioFiles']
)


@router.post('/record', response_model=ReturnURL)
async def add_audiofile_rout(body: AddAudio, session: AsyncSession = Depends(get_async_session)) -> ReturnURL:
    if not await check_user_token(session, body.user_id, body.access_token):
        raise HTTPException(status_code=403, detail='User with such access token not found')

    new_path = convert_audio(body.audiofile)

    audio_id, user_id = await add_new_audio(session, body, new_path)

    return f'http://host:port/record?id={audio_id}&user={user_id}'


@router.get('/record?id={audio_id}&user={user_id}')
async def download_audio(audio_id: UUID4, user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    if not await get_user_by_id(session, user_id):
        raise HTTPException(status_code=403, detail=f'User not found')

    if not await get_audio_by_id(session, audio_id):
        raise HTTPException(status_code=403, detail=f'Audio not found')

    if not await check_user_token(session, user_id, audio_id):
        raise HTTPException(status_code=403, detail=f'The user cannot download this audio file')

    
