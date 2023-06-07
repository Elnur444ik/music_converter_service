from pydantic import BaseModel, UUID4


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str


class ReturnUser(TunedModel):
    user_id: UUID4
    access_token: UUID4
