from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from pyfall.client import Pyfall


class BaseAPIModel(BaseModel):
    """Base API model for base API calls."""

    _client: "Pyfall"

    def __init__(self, **data):
        client: "Pyfall" = data["_client"]
        super().__init__(**data)
        self._client = client
