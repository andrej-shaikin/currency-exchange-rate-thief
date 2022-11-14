from apps.blacklist.logic.actions import get_blacklist_list_from_cbr
from apps.blacklist.models import BlackList, BlackListSign


async def update_black_list_task() -> None:
    # TODO обновлять объекты, обойтись без удаления
    await BlackList.objects.all().delete()

    for black_list_item in await get_blacklist_list_from_cbr():
        black_list_sign, _ = BlackListSign.objects.update_or_create(name=black_list_item.name)
        BlackList.objects.create(
            dt=black_list_item.dt,
            inn=black_list_item.inn,
            closed=black_list_item.closed,
            address=black_list_item.address,
            sites=','.join(black_list_item.sites),
            sign=black_list_sign,
            name=black_list_item.name,
        )
