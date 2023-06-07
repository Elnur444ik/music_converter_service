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