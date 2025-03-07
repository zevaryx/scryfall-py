from datetime import date
from typing import Any, Literal, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator

from scryfall.models.base import BaseAPIModel
from scryfall.models.enums import Color

if TYPE_CHECKING:
    from scryfall.models.rulings import Ruling
    from scryfall.models.sets import Set


class RelatedCard(BaseModel):
    """A card that's related to the current card"""

    id: UUID
    """The UUID of the related card"""

    object: Literal["related_card"]
    """The object type, literally `related_card`"""

    component: Literal["token", "meld_part", "meld_result", "combo_piece"]
    """How the card is related"""

    name: str
    """The name of the related card"""

    type_line: str
    """The type line of the related card"""

    uri: HttpUrl
    """The URL of the related card"""


class CardFace(BaseModel):
    """A card face, for multi-faced cards"""

    artist: str | None = None
    """The face artist"""

    artist_id: str | None = None
    """The ID of the face artist"""

    cmc: float | None = None
    """Card Mana Cost"""

    color_indicator: list[Color] | None = None
    """The color indicator(s) of the face"""

    colors: list[Color] | None = None
    """The color(s) of the face"""

    defense: str | None = None
    """The toughness of the face, if it exists"""

    flavor_text: str | None = None
    """The face's flavor text"""

    illustration_id: UUID | None = None
    """The face's illustration UUID"""

    image_uris: dict[Literal["small", "normal", "large", "png", "art_crop", "border_crop"], HttpUrl] | None = None
    """URLs for the image face for different formats."""

    layout: str | None = None
    """Layout of the face."""

    loyalty: str | None = None
    """Face loyalty"""

    mana_cost: str
    """Face mana cost"""

    name: str
    """Name of the face"""

    object: Literal["card_face"]
    """Object type, literally `card_face`"""

    oracle_id: UUID | None = None
    """Oracle ID of the face"""

    oracle_text: str | None = None
    """Oracle text of the face"""

    power: str | None = None
    """The face's power"""

    printed_name: str | None = None
    """The printed name of the face"""

    printed_text: str | None = None
    """The printed text of the face"""

    printed_type_line: str | None = None
    """The printed type line of the face"""

    toughness: str | None = None
    """The toughness of the face"""

    type_line: str | None = None
    """The type line of the face"""

    watermark: str | None = None
    """The watermark of the face"""


class Preview(BaseModel):
    """Object for defining when the card was previewed."""

    previewed_at: date | None = None

    """When it was previewed"""

    source_uri: HttpUrl | None = None
    """The URL of where it was previewed"""

    source: str | None = None
    """The source of the preview"""

    @field_validator("source_uri", mode="before")
    @classmethod
    def validate_source_uri(cls, value: Any) -> Any:
        if isinstance(value, str):
            if len(value) > 0:
                return HttpUrl(value)
        return None


class Card(BaseAPIModel):
    """Main Card model."""

    # Core fields
    arena_id: int | None = None
    """MTG Arena ID"""

    id: UUID
    """Scryfall card UUID"""

    lang: str
    """Card language"""

    mtgo_id: int | None = None
    """MTG Online ID"""

    mtgo_foil_id: int | None = None
    """MTG Online Foil ID"""

    multiverse_ids: list[int] | None = None
    """MTG Multiverse IDs"""

    tcgplayer_id: int | None = None
    """TCGPlayer ID"""

    tcgplayer_etched_id: int | None = None
    """TCGPlayer Etched ID"""

    cardmarket_id: int | None = None
    """Cardmarket ID"""

    object: Literal["card"]
    """Object type, literally `card`"""

    layout: str
    """Card layout"""

    oracle_id: UUID | None = None
    """Oracle UUID"""

    prints_search_uri: HttpUrl
    """Print search URL for other printings"""

    rulings_uri: HttpUrl
    """Rulings URL"""

    scryfall_uri: HttpUrl
    """Scryfall URL"""

    uri: HttpUrl
    """Card URL"""

    # Gameplay fields
    all_parts: list[RelatedCard] | None = None
    """If this card is closely related to other cards, this property will be an array with Related Card objects."""
    card_faces: list[CardFace] | None = None
    """All faces of the card"""
    cmc: float
    """Card mana value"""
    color_identity: list[Color]
    """Card color identity"""
    color_indicator: list[Color] | None = None
    """Card color indicator, if any"""
    colors: list[Color] | None = None
    """Card colors, if any. Colors may be on the card's faces instead"""
    defense: str | None = None
    """Toughness"""
    edhrec_rank: int | None = None
    """EDHRec card rank/popularity"""
    game_changer: bool | None = None
    """If this car is on the Commander Game Changer list"""
    hand_modifier: str | None = None
    """Vanguard card hand modifier"""
    keywords: list[str]
    """List of keywords, such as `Flying` or `Cumulative upkeep`"""
    legalities: dict[str, Literal["legal", "not_legal", "restricted", "banned"]]
    """List of legalitites across different formats"""
    life_modifier: str | None = None
    """The card's life modifier, if it is a Vanguard card. This value will contain a delta, such as `+2`."""
    loyalty: str | None = None
    """This loyalty if any. Note that some cards have loyalties that are not numeric, such as X."""
    mana_cost: str | None = None
    """The mana cost for this card. This value will be any empty string `""` if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of `{0}` are different values. Multi-faced cards will report this value in card faces."""
    name: str
    """The name of this card. If this card has multiple faces, this field will contain both names separated by `␣//␣`."""
    oracle_text: str | None = None
    """The Oracle text for this card, if any."""
    penny_rank: int | None = None
    """This card's rank/popularity on Penny Dreadful. Not all cards are ranked."""
    power: str | None = None
    """This card's power, if any. Note that some cards have powers that are not numeric, such as `*`."""
    produced_mana: list[Color] | None = None
    """Colors of mana that this card could produce."""
    reserved: bool
    """True if this card is on the Reserved List."""
    toughness: str | None = None
    """This card's toughness, if any. Note that some cards have toughnesses that are not numeric, such as `*`."""
    type_line: str
    """The type line of this card."""

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

    async def get_rulings(self) -> list["Ruling"]:
        """Get rulings for card."""
        return await self._client.get_rulings_by_card_id(self.id)
