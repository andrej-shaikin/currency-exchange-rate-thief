from datetime import datetime
from distutils.util import strtobool
from logging import getLogger
from typing import Optional

import httpx
from fastapi_utils.httpx.logic.getters import get_httpx_request_proxies
from lxml import etree
from starlette import status

from apps.blacklist.dto import BlackListItemDto
from apps.blacklist.models import BlackList, BlackListSign

logger = getLogger(__name__)


async def get_blacklist_list_from_cbr() -> Optional[list[BlackListItemDto]]:
    """Получение списка организаций в черном списке ЦентроБанка"""
    async with httpx.AsyncClient(proxies=get_httpx_request_proxies()) as client:
        resp: httpx.Response = await client.get("http://www.cbr.ru/Queries/FileSource/123124/BlackList.xml")
        if resp.status_code != status.HTTP_200_OK:
            logger.warning(resp.reason_phrase)
            return
        black_list = []
        for rc in etree.fromstring(resp.text).findall("RC"):
            site = rc.find("Site").text
            black_list.append(
                BlackListItemDto(
                    dt=datetime.strptime(rc.find("DT").text, "%Y-%m-%d"),
                    name=rc.find("Name").text,
                    inn=rc.find("INN").text,
                    address=rc.find("ADDR").text,
                    sites=site and site.strip().split() or None,
                    sign=rc.find("Sign").text,
                    closed=bool(strtobool(rc.find("Closed").text)),
                )
            )
        return black_list


async def update_black_list() -> None:
    # TODO обновлять объекты, обойтись без удаления
    BlackList.objects.delete()

    for black_list_item in await get_blacklist_list_from_cbr():
        black_list_sign, _ = await BlackListSign.objects.update_or_create(name=black_list_item.name)
        await BlackList.objects.create(
            dt=black_list_item.dt,
            inn=black_list_item.inn,
            closed=black_list_item.closed,
            address=black_list_item.address,
            sites=','.join(black_list_item.sites),
            sign=black_list_sign,
            name=black_list_item.name,
        )
