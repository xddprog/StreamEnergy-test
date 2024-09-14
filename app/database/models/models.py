from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_login: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[list["Note"]] = relationship(
        back_populates="user", uselist=True, lazy="selectin"
    )


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        back_populates="notes", uselist=False, lazy="selectin"
    )

    tags: Mapped[list["NoteTag"]] = relationship(
        back_populates="notes",
        uselist=True,
        secondary="notes_tags",
        lazy="selectin",
    )


class NoteTag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    value: Mapped[str] = mapped_column(unique=True)

    notes: Mapped[list["Note"]] = relationship(
        back_populates="tags",
        uselist=True,
        secondary="notes_tags",
        lazy="selectin",
    )


class NoteTage(Base):
    __tablename__ = "notes_tags"

    note_fk: Mapped[int] = mapped_column(
        ForeignKey("notes.id"), primary_key=True
    )
    tag_fk: Mapped[int] = mapped_column(
        ForeignKey("tags.id"), primary_key=True
    )
