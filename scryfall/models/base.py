from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from scryfall.client import Scryfall


class BaseAPIModel(BaseModel):
    """Base API model for base API calls."""

    _client: "Scryfall"
    """Internal Scryfall client"""

    def __init__(self, **data):
        client: "Scryfall" = data["_client"]
        super().__init__(**data)
        self._client = client
