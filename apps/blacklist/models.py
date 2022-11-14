from datetime import date

import ormar
from fastapi_utils.db.models import BaseModel, BaseModelMeta


class BlackListSign(BaseModel):
    """Признаки, установленные Банком России."""

    name: str = ormar.String(max_length=512, index=True, unique=True)

    class Meta(BaseModelMeta):
        tablename = "black_list_signs"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: <{self.id}> {self.name}"

    def __str__(self) -> str:
        return f"{self.name}"


class BlackList(BaseModel):
    """Список компаний с выявленными признаками нелегальной деятельности на финансовом рынке"""

    dt: date = ormar.Date(info={"verbose_name": 'Дата внесения в реестр'})
    inn: str = ormar.String(max_length=512, index=True, info={"verbose_name": "ИНН организации"})
    closed: bool = ormar.Boolean(default=False, info={"verbose_name": "Деятельность прекращена"})
    address: str = ormar.String(max_length=512, info={"verbose_name": "Адрес предоставления лицом услуг"})
    sites: dict = ormar.JSON(default=dict, nullable=True, info={"verbose_name": "Сайт в сети «Интернет»"})
    sign: BlackListSign = ormar.ForeignKey(
        to=BlackListSign,
        index=True,
        related_name="black_lists",
        info={"verbose_name": "Признаки, установленные Банком России"},
    )
    name: str = ormar.String(
        max_length=512,
        index=True,
        unique=True,
        info={
            "verbose_name": (
                'Наименование, знак обслуживания, коммерческое обозначение и иные средства индивидуализации лица'
            )
        }
    )

    class Meta(BaseModelMeta):
        tablename = "black_lists"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: <{self.id}> {self.name}"

    def __str__(self) -> str:
        return f"{self.name}"
