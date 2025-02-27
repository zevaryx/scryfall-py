from typing import Literal

from pydantic import BaseModel, HttpUrl

from pyfall.models.enums import Color

class CardSymbol(BaseModel):
    object: Literal["card_symbol"]
    symbol: str
    loose_variant: str | None = None
    english: str
    transposable: bool
    represents_mana: bool
    mana_value: float | None = None
    appears_in_mana_costs: bool
    funny: bool
    colors: list[Color]
    hybrid: bool
    phyrexian: bool
    gatherer_alternatives: str | None = None
    svg_uri: HttpUrl | None = None