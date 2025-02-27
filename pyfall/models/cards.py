from datetime import date
from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, HttpUrl, field_validator
from pydantic.types import UUID

# from pyfall.models.api import APIList
from pyfall.models.base import BaseAPIModel
from pyfall.models.enums import Color

if TYPE_CHECKING:
    from pyfall.client import Pyfall
    from pyfall.models.rulings import Ruling
    from pyfall.models.sets import Set

class RelatedCard(BaseModel):
    id: UUID
    object: Literal["related_card"]
    component: Literal["token", "meld_part", "meld_result", "combo_piece"]
    name: str
    type_line: str
    uri: HttpUrl
    
class CardFace(BaseModel):
    artist: str | None = None
    artist_id: str | None = None
    cmc: float | None = None
    color_indicator: list[Color] | None = None
    colors: list[Color] | None = None
    defense: str | None = None
    flavor_text: str | None = None
    illustration_id: UUID | None = None
    image_uris: dict[Literal["small", "normal", "large", "png", "art_crop", "border_crop"], HttpUrl] | None = None
    layout: str | None = None
    loyalty: str | None = None
    mana_cost: str
    name: str
    object: Literal["card_face"]
    oracle_id: UUID | None = None
    oracle_text: str | None = None
    power: str | None = None
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    toughness: str | None = None
    type_line: str | None = None
    watermark: str | None = None
    
class Preview(BaseModel):
    previewed_at: date | None = None
    source_uri: HttpUrl | None = None
    source: str | None = None
    
    @field_validator("source_uri", mode="before")
    @classmethod
    def validate_source_uri(cls, value: Any) -> Any:
        if isinstance(value, str):
            if len(value) > 0:
                return HttpUrl(value)
        return None

class Card(BaseAPIModel):
    # Core fields
    arena_id: int | None = None
    id: UUID
    lang: str
    mtgo_id: int | None = None
    mtgo_foil_id: int | None = None
    multiverse_ids: list[int] | None = None
    tcgplayer_id: int | None = None
    tcgplayer_etched_id: int | None = None
    cardmarket_id: int | None = None
    object: Literal["card"]
    layout: str
    oracle_id: UUID | None = None
    prints_search_uri: HttpUrl
    rulings_uri: HttpUrl
    scryfall_uri: HttpUrl
    uri: HttpUrl
    
    # Gameplay fields
    all_parts: list[RelatedCard] | None = None
    card_faces: list[CardFace] | None = None
    cmc: float
    color_identity: list[Color]
    color_indicator: list[Color] | None = None
    colors: list[Color] | None = None
    defense: str | None = None
    edhrec_rank: int | None = None
    game_changer: bool | None = None
    hand_modifier: str | None = None
    keywords: list[str]
    legalities: dict[str, Literal["legal", "not_legal", "restricted", "banned"]]
    life_modifier: str | None = None
    loyalty: str | None = None
    mana_cost: str | None = None
    name: str
    oracle_text: str | None = None
    penny_rank: int | None = None
    power: str | None = None
    produced_mana: list[Color] | None = None
    reserved: bool
    toughness: str | None = None
    type_line: str
    
    # Print fields
    artist: str | None = None
    artist_ids: list[UUID] | None = None
    attraction_lights: list[int] | None = None
    booster: bool
    border_color: Literal["black", "white", "borderless", "yellow", "silver", "gold"]
    card_back_id: UUID | None = None
    collector_number: str
    content_warning: bool | None = None
    digital: bool
    finishes: list[Literal["foil", "nonfoil", "etched"]]
    flavor_name: str | None = None
    flavor_text: str | None = None
    frame_effects: list[str] | None = None
    frame: str
    full_art: bool
    games: list[Literal["paper", "arena", "mtgo"]]
    highres_image: bool
    illustration_id: UUID | None = None
    image_status: Literal["missing", "placeholder", "lowres", "highres_scan"]
    image_uris: dict[Literal["small", "normal", "large", "png", "art_crop", "border_crop"], HttpUrl] | None = None
    oversized: bool
    prices: dict[str, str | None]
    printed_name: str | None = None
    printed_text: str | None = None
    printed_type_line: str | None = None
    promo: bool
    promo_types: list[str] | None = None
    purchase_uris: dict[str, HttpUrl] | None = None
    rarity: Literal["common", "uncommon", "rare", "special", "mythic", "bonus"]
    related_uris: dict[str, HttpUrl]
    released_at: date
    reprint: bool
    scryfall_set_uri: HttpUrl
    set_name: str
    set_search_uri: HttpUrl
    set_type: str
    set_uri: HttpUrl
    set: str
    set_id: UUID
    story_spotlight: bool
    textless: bool
    variation: bool
    variation_of: UUID | None = None
    security_stamp: Literal["oval", "triangle", "acorn", "circle", "arena", "heart"] | None = None
    watermark: str | None = None
    preview: Preview | None = None
    
    async def get_set(self) -> "Set":
        """Get set card is a part of."""
        return await self._client.get_set_by_id(self.set_id)
    
    async def get_rulings(self) -> "Ruling":
        """Get rulings for card."""
        return await self._client.get_rulings_by_card_id(self.id)
        