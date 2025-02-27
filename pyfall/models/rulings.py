from datetime import date
from typing import Literal

from pydantic import BaseModel
from pydantic.types import UUID

class Ruling(BaseModel):
    object: Literal["ruling"]
    oracle_id: UUID
    source: Literal["wotc", "scryfall"]
    published_at: date
    comment: str