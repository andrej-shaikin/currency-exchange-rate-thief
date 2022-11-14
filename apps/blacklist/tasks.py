import asyncio

from apps.blacklist.logic.actions import update_black_list


def update_black_list_task() -> None:
    asyncio.run(update_black_list())
