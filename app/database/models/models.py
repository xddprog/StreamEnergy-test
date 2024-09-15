from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_login: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", uselist=True, lazy="selectin"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        back_populates="tasks", uselist=False, lazy="selectin"
    )

    tags: Mapped[list["TaskTag"]] = relationship(
        back_populates="tasks",
        uselist=True,
        secondary="tasks_tags",
        lazy="selectin",
    )


class TaskTag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    value: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="tags",
        uselist=True,
        secondary="tasks_tags",
        lazy="selectin",
    )


class TasksTags(Base):
    __tablename__ = "tasks_tags"

    task_fk: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), primary_key=True
    )
    tag_fk: Mapped[int] = mapped_column(
        ForeignKey("tags.id"), primary_key=True
    )
