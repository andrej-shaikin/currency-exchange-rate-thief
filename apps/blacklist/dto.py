from datetime import date

from pydantic import BaseModel


class BlackListItemDto(BaseModel):
    """компания с выявленными признаками нелегальной деятельности на финансовом рынке"""

    dt: date
    name: str
    inn: str | None
    address: str | None
    sign: str
    sites: list[str] | None
    closed: bool
