from typing import Any, Literal

from pydantic import BaseModel, HttpUrl, ValidationError, model_validator

from scryfall.models.base import BaseAPIModel
from scryfall.models.cards import Card
from scryfall.models.rulings import Ruling
from scryfall.models.sets import Set
from scryfall.models.symbols import CardSymbol

CLASS_LOOKUP = {"card": Card, "card_symbol": CardSymbol, "ruling": Ruling, "set": Set}


class APIError(BaseModel):
    status: int
    code: str
    details: str
    type: str | None = None
    warnings: list[str] | None = None


class APIList(BaseAPIModel):
    object: Literal["list"]
    data: list[Card | CardSymbol | Ruling | Set]
    has_more: bool
    next_page: HttpUrl | None = None
    total_cards: int | None = None
    warnings: list[str] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, data: Any) -> Any:
        if data.get("object") == "list":
            for item in data.get("data"):
                item["_client"] = data["_client"]
                obj = item.get("object")
                if obj not in CLASS_LOOKUP:
                    raise ValidationError("Item missing object field")
                item = CLASS_LOOKUP[obj](**item)
        return data

    async def get_next_page(self) -> "APIList | None":
        if self.has_more and self.next_page is not None:
            params = dict(self.next_page.query_params())
            params.pop("format", None)
            return await self._client.search_cards(**params)  # type: ignore
        return None
