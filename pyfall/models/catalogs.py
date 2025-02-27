from typing import Literal

from pydantic import BaseModel, HttpUrl

class Catalog(BaseModel):
    object: Literal["catalog"]
    uri: HttpUrl | None = None
    total_values: int
    data: list[str]