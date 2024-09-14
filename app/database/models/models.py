from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str]
    password: Mapped[str]
    is_login: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[list['Note']] = relationship(back_populates="user", uselist=True)


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user_fk: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="notes", uselist=False)

    tags: Mapped[list['NoteTag']] = relationship(back_populates="note", uselist=True)


class NoteTag(Base):
    id: Mapped[int]


class NoteTage(Base):
    __tablename__ = 'notes_tags'

    note_fk: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    tag_fk: Mapped[int] = mapped_column(ForeignKey("tags.id"))
