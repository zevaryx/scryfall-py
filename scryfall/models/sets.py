from datetime import date
from typing import Literal, TYPE_CHECKING
from uuid import UUID

from pydantic import HttpUrl

from scryfall.models.base import BaseAPIModel

if TYPE_CHECKING:
    from scryfall.models.api import APIList


class Set(BaseAPIModel):
    object: Literal["set"]
    id: UUID
    code: str
    mtgo_code: str | None = None
    arena_code: str | None = None
    tcgplayer_id: int | None = None
    name: str
    set_type: str
    released_at: date | None = None
    block_code: str | None = None
    block: str | None = None
    parent_set_code: str | None = None
    card_count: int
    printed_size: int | None = None
    digital: bool
    foil_only: bool
    nonfoil_only: bool
    scryfall_uri: HttpUrl
    uri: HttpUrl
    icon_svg_uri: HttpUrl
    search_uri: HttpUrl

    async def get_cards(self) -> "APIList":
        """Get a list of cards from the set."""
        params = dict(self.search_uri.query_params())
        return await self._client.search_cards(**params)  # type: ignore
