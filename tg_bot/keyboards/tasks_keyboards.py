from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.buttons import task_buttons


async def get_all_tasks_keyboard(tasks: list[dict]) -> InlineKeyboardMarkup:
    print(tasks)
    buttons = [
        [
            InlineKeyboardButton(
                text=task["title"], callback_data=f"task_{task["id"]}"
            )
        ]
        for task in tasks
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_task_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in task_buttons.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_tasks_tags_keyboard(
    tags: list[dict], search: bool = False, create: bool = False
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=tag["value"], callback_data=f"tasks_tag_{tag['id']}"
            )
        ]
        for tag in tags
    ]

    if search:
        buttons.append(
            [InlineKeyboardButton(text="Начать поиск", callback_data="search")]
        )
    if create:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Создать", callback_data="create_task_success"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
