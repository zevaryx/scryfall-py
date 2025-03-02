from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Ruling(BaseModel):
    object: Literal["ruling"]
    oracle_id: UUID
    source: Literal["wotc", "scryfall"]
    published_at: date
    comment: str
