from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud_layers.audiofiles import add_new_audio
from core.crud_layers.users import get_user_by_id, check_user_token
from core.database import get_async_session
from core.schemas.audiofiles import ReturnAudio, AddAudio
from v1.utils.audiofiles import convert_audio

router = APIRouter(
    prefix='/',
    tags=['AudioFiles']
)


@router.post('/audio', response_model=ReturnAudio)
async def add_audiofile_rout(body: AddAudio, session: AsyncSession = Depends(get_async_session)):

    if not await check_user_token(session, body.user_id, body.access_token):
        raise HTTPException(status_code=403, detail='User with such access token not found')

    new_path = convert_audio(body.audiofile)

    audio_id, user_id = await add_new_audio(session, body, new_path)

    return


