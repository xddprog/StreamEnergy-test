import requests as req
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.tasks_keyboards import (
    get_all_tasks_keyboard,
    get_task_menu_keyboard,
    get_tasks_tags_keyboard,
)
from lexicon.texts import (
    menu_text,
    task_texts,
    tasks_check_page_text,
    create_task_texts,
)
from states.task_states import CreateTask


router = Router()


@router.callback_query(F.data == "create_task_success")
async def create_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    task = req.post(
        "http://localhost:8000/api/tasks",
        headers={"Authorization": f'Bearer {data.get("token")}'},
        json={
            "title": data.get("title"),
            "description": data.get("description"),
            "tags": data.get("selected_task_tags"),
        },
    )

    await callback.message.edit_text(
        text=task_texts["task"].format(**task.json()),
        reply_markup=await get_task_menu_keyboard(),
    )


@router.callback_query(F.data == "create_task")
async def creted_tasks(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CreateTask.title)

    await callback_query.message.edit_text(text=create_task_texts["title"])


@router.message(CreateTask.title, F.text)
async def create_task_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)

    await state.set_state(CreateTask.description)

    await message.answer(text=create_task_texts["description"])


@router.message(CreateTask.description, F.text)
async def create_task_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)

    await state.set_state(CreateTask.tags)

    data = await state.get_data()

    tasks_tags = req.get(
        "http://app:8000/api/tasks_tags/all",
        headers={"Authorization": f'Bearer {data.get("token")}'},
    )
    tasks_tags = tasks_tags.json()

    await state.update_data(
        selected_task_tags=[],
        all_tasks_tags=tasks_tags,
        selected_tasks_tags_names=[],
    )

    await message.answer(
        text=task_texts["choose_tags"],
        reply_markup=await get_tasks_tags_keyboard(tasks_tags),
    )


@router.callback_query(CreateTask.tags, F.data != "back_to_menu")
async def tasks_by_tags(callback: CallbackQuery, state: FSMContext):
    tag_id = callback.data.split("_")[-1]
    data = await state.get_data()

    selected_task_tags = data.get("selected_task_tags")
    selected_task_tags.append(tag_id)

    all_tasks_tags = data.get("all_tasks_tags")

    selected_tag = [tag for tag in all_tasks_tags if tag["id"] != int(tag_id)][
        0
    ]

    selected_task_tags_names = data.get("selected_tasks_tags_names")
    selected_task_tags_names.append(selected_tag["value"])

    all_tasks_tags.remove(selected_tag)

    await state.update_data(
        selected_task_tags=[*selected_task_tags],
        all_tasks_tags=all_tasks_tags,
        selected_task_tags_names=selected_task_tags_names,
    )

    await callback.message.edit_text(
        text=task_texts["selected_tags"].format(
            tags=", ".join(selected_task_tags_names)
        ),
        reply_markup=await get_tasks_tags_keyboard(
            all_tasks_tags, create=True
        ),
    )


@router.callback_query(F.data == "tasks_by_tags")
async def tasks_by_tags(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tasks_tags = req.get(
        "http://app:8000/api/tasks_tags/all",
        headers={"Authorization": f'Bearer {data.get("token")}'},
    )
    tasks_tags = tasks_tags.json()

    await state.update_data(
        selected_task_tags=[],
        all_tasks_tags=tasks_tags,
        selected_tasks_tags_names=[],
    )

    await callback.message.edit_text(
        text=task_texts["choose_tags"],
        reply_markup=await get_tasks_tags_keyboard(tasks_tags),
    )


@router.callback_query(F.data.startswith("tasks_tag"))
async def tasks_by_tags(callback: CallbackQuery, state: FSMContext):
    tag_id = callback.data.split("_")[-1]
    data = await state.get_data()

    selected_task_tags = data.get("selected_task_tags")
    selected_task_tags.append(tag_id)

    all_tasks_tags = data.get("all_tasks_tags")

    selected_tag = [tag for tag in all_tasks_tags if tag["id"] != int(tag_id)][
        0
    ]
    print(selected_tag)

    selected_task_tags_names = data.get("selected_tasks_tags_names")
    selected_task_tags_names.append(selected_tag["value"])

    all_tasks_tags.remove(selected_tag)

    await state.update_data(
        selected_task_tags=[*selected_task_tags],
        all_tasks_tags=all_tasks_tags,
        selected_task_tags_names=selected_task_tags_names,
    )

    await callback.message.edit_text(
        text=task_texts["selected_tags"].format(
            tags=", ".join(selected_task_tags_names)
        ),
        reply_markup=await get_tasks_tags_keyboard(
            all_tasks_tags, search=True
        ),
    )


@router.callback_query(F.data == "search")
async def search(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tasks = req.get(
        "http://app:8000/api/tasks/filter",
        headers={"Authorization": f'Bearer {data.get("token")}'},
        params={"tags": data.get("selected_task_tags")},
    )

    await callback.message.edit_text(
        text=tasks_check_page_text,
        reply_markup=await get_all_tasks_keyboard(tasks.json()),
    )


@router.callback_query(F.data == "all_tasks")
async def all_tasks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tasks = req.get(
        "http://app:8000/api/user/tasks/all",
        headers={"Authorization": f'Bearer {data.get("token")}'},
    )

    await callback.message.edit_text(
        text=menu_text,
        reply_markup=await get_all_tasks_keyboard(tasks.json()),
    )


@router.callback_query(F.data.split("_")[0] == "task")
async def one_task(callback: CallbackQuery, state: FSMContext):
    task_id = callback.data.split("_")[-1]
    data = await state.get_data()
    await state.update_data(task_id=task_id)

    task = req.get(
        f"http://app:8000/api/tasks/{task_id}",
        headers={"Authorization": f'Bearer {data.get("token")}'},
    )

    await callback.message.edit_text(
        text=task_texts["task"].format(**task.json()),
        reply_markup=await get_task_menu_keyboard(),
    )


@router.callback_query(F.data == "delete")
async def delete_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")

    req.delete(
        f"http://app:8000/api/tasks/{task_id}",
        headers={"Authorization": f'Bearer {data.get("token")}'},
    )

    await callback.message.edit_text(text=task_texts["delete"])
