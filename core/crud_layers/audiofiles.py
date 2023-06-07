from typing import Union
from sqlalchemy import select
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.models import AudioFile
from core.schemas.audiofiles import AddAudio, ReturnAudio


async def add_new_audio(db: AsyncSession, body: AddAudio, new_path: str) -> tuple[UUID4, UUID4]:
    title = new_path.split('/')[-1][:-4]
    new_audio = AudioFile(audiofile_path=new_path, user_id=body.user_id, title=title)
    db.add(new_audio)
    await db.commit()
    return new_audio.id, new_audio.user_id


async def check_user_audio(db: AsyncSession, user_id: UUID4, audio_id: UUID4) -> Union[UUID4, None]:
    query = select(AudioFile).filter_by(AudioFile.id == audio_id, AudioFile.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_audio_by_id(db: AsyncSession, audio_id: UUID4) -> Union[UUID4, None]:
    query = select(AudioFile).where(AudioFile.id == audio_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
