import uuid
from typing import Optional

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    token: Mapped[UUID] = mapped_column(default=uuid.uuid4)


class AudioFile(Base):
    __tablename__ = 'audiofiles_mp3'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audiofile_path: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[Optional[str]]

    user: Mapped[User] = relationship(User, lazy="joined")
