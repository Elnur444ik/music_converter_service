from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic.types import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from core.crud_layers.audiofiles import add_new_audio, get_audio_by_id, check_user_audio
from core.crud_layers.users import get_user_by_id, check_user_token
from core.database import get_async_session
from core.schemas.audiofiles import ReturnAudio, AddAudio, ReturnURL
from v1.utils.audiofiles import convert_audio

router = APIRouter(
    prefix='/',
    tags=['AudioFiles']
)


@router.get('/record?id={audio_id}&user={user_id}')
async def download_audio(audio_id: UUID4, user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    if not await get_user_by_id(session, user_id):
        raise HTTPException(status_code=404, detail=f'User not found')

    if not await get_audio_by_id(session, audio_id):
        raise HTTPException(status_code=404, detail=f'Audio not found')

    file = await check_user_audio(session, user_id, audio_id)

    if not file:
        raise HTTPException(status_code=403, detail=f'The user cannot download this audio file')
    return FileResponse(file.audiofile_path)


@router.post('/record', response_model=ReturnURL)
async def add_audiofile_rout(body: AddAudio, request: Request,
                             session: AsyncSession = Depends(get_async_session)) -> ReturnURL:
    if not await check_user_token(session, body.user_id, body.access_token):
        raise HTTPException(status_code=404, detail='User with such access token not found')
    new_path = convert_audio(body.audiofile)

    audio_id, user_id = await add_new_audio(session, body, new_path)

    return request.url_for('download_audio', audio_id=audio_id, user_id=user_id)

