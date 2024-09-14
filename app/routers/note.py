from typing import Annotated
from fastapi import APIRouter, Depends

from app.dto.note_dto import AddNoteForm, BaseNoteModel
from app.dto.user_dto import BaseUserModel
from app.services.note_service import NoteService
from app.services.note_tag_service import NoteTagService
from app.services.user_service import UserService
from app.utils.dependencies import (
    get_auth_service,
    get_current_user_dependency,
    get_note_service,
    get_note_tag_service,
    get_user_service,
)


router = APIRouter(
    prefix="/api/notes",
    tags=["notes"],
)


@router.post("/notes/add")
async def add_note(
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    notes_service: Annotated[NoteService, Depends(get_note_service)],
    note_tags_service: Annotated[
        NoteTagService, Depends(get_note_tag_service)
    ],
    form: AddNoteForm,
) -> BaseNoteModel:
    print(form.tags)
    user = await user_service.get_user(user.id, dump=False)
    form.tags = [
        await note_tags_service.get_tag(tag_id, dump=False)
        for tag_id in form.tags
    ]
    return await notes_service.add_note(user, form)
