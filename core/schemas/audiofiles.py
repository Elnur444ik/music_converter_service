from pydantic import BaseModel, UUID4, FilePath, FileUrl


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
    audiofile_url: FileUrl
