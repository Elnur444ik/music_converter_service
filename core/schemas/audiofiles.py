from typing import Optional

from pydantic import BaseModel, UUID4, FilePath, FileUrl, HttpUrl


class AddAudio(BaseModel):
    user_id: UUID4
    access_token: UUID4
    audiofile: FilePath


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ReturnAudio(TunedModel):
    audio_id: UUID4
    user_id: UUID4


class ReturnURL(TunedModel):
    audiofile_url: HttpUrl


class ReturnAudioRow(TunedModel):
    user_id: UUID4
    access_token: UUID4
    audiofile_path: FilePath
    title: Optional[str] = 'Unnamed'
