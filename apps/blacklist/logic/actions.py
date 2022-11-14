from datetime import datetime
from distutils.util import strtobool
from logging import getLogger
from typing import Optional

import httpx
from fastapi_utils.httpx.logic.getters import get_httpx_request_proxies
from lxml import etree
from starlette import status

from apps.blacklist.dto import BlackListItemDto

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
