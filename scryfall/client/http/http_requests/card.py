from typing import Any, Literal
from uuid import UUID

from scryfall.models.catalogs import Catalog
from scryfall.client.route import Route
from scryfall.models.cards import Card
from scryfall.models.api import APIList
from scryfall.models.rulings import Ruling
from scryfall.models.internal.protocols import CanRequest


class CardRequests(CanRequest):
    async def get_card_by_id(self, id: str | UUID) -> Card:
        """
        Get a card by ID.

        Args:
            id: UUID of card

        """
        result = await self.request(Route("GET", f"/cards/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_card_by_tcgplayer_id(self, id: int) -> Card:
        """
        Get card by TCGPlayer ID

        Args:
            id: TCGPlayer ID

        """
        result = await self.request(Route("GET", f"/cards/tcgplayer/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_card_by_multiverse_id(self, id: int) -> Card:
        """
        Get card by Multiverse ID

        Args:
            id: Multiverse ID

        """
        result = await self.request(Route("GET", f"/cards/multiverse/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_card_by_mtgo_id(self, id: int) -> Card:
        """
        Get card by MTGO ID

        Args:
            id: MTGO ID

        """
        result = await self.request(Route("GET", f"/cards/mtgo/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_card_by_arena_id(self, id: int) -> Card:
        """
        Get card by MTG Arena ID

        Args:
            id: MTG Arena ID

        """
        result = await self.request(Route("GET", f"/cards/arena/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_card_by_cardmarket_id(self, id: int) -> Card:
        """
        Get card by Cardmarket ID

        Args:
            id: Cardmarket ID

        """
        result = await self.request(Route("GET", f"/cards/cardmarket/{id}"))
        result["_client"] = self
        return Card(**result)

    async def get_rulings_by_card_id(self, id: str | UUID) -> list[Ruling]:
        """
        Get card rulings by card ID.

        Args:
            id: UUID of card

        """
        result = await self.request(Route("GET", f"/cards/{id}/rulings"))
        return [Ruling(**x) for x in result["data"]]

    async def search_cards(
        self,
        q: str,
        unique: Literal["cards", "art", "prints"] = "cards",
        order: Literal[
            "name",
            "set",
            "released",
            "rarity",
            "color",
            "usd",
            "tix",
            "eur",
            "cmc",
            "power",
            "toughness",
            "edhrec",
            "penny",
            "artist",
            "review",
        ] = "name",
        dir: Literal["auto", "asc", "desc"] = "auto",
        include_extras: bool = False,
        include_multilingual: bool = False,
        include_variations: bool = False,
        page: int = 1,
    ) -> APIList:
        """
        Search for a card using a fulltext string search.

        Args:
            q: A fulltext search query. Max length: 1000 Unicode characters
            unique: The strategy for omitting cards. Default `cards`
            order: The method to sort returned cards. Default `name`
            dir: Direction to sort cards. Default `auto`
            include_extras: If true, extra cards (tokens, planes, etc) will be included. Equivalent to adding `include:extras` to the fulltext search. Default `false`
            include_multilingual: If true, cards in every language supported by Scryfall will be included. Default `false`
            include_variations: If true, rare card variants will by included. Default `false`
            page: Page number to return. Default `1`

        """
        if len(q) > 1000:
            raise ValueError("Query can only be max of 1000 Unicode characters")

        params = {
            "q": q,
            "unique": unique,
            "order": order,
            "dir": dir,
            "include_extras": include_extras,
            "include_multilingual": include_multilingual,
            "include_variations": include_variations,
            "page": page,
        }

        result = await self.request(
            Route(
                "GET",
                "/cards/search",
            ),
            params=params,
        )

        result["_client"] = self
        return APIList(**result)

    async def search_cards_named(
        self, exact: str | None = None, fuzzy: str | None = None, set: str | None = None
    ) -> Card:
        """
        Search for a card using name search.

        Args:
            exact: Exact string to search for
            fuzzy: Fuzzy string to search for
            set: Set to search in

        """
        if (not exact and not fuzzy) or (exact and fuzzy):
            raise ValueError("Either exact or fuzzy needs provided")

        params = {"set": set}
        if exact:
            params["exact"] = exact
        elif fuzzy:
            params["fuzzy"] = fuzzy

        result = await self.request(
            Route(
                "GET",
                "/cards/named",
            ),
            params=params,
        )

        result["_client"] = self
        return Card(**result)

    async def cards_autocomplete(self, q: str, include_extras: bool = False) -> Catalog:
        """
        Returns a Catalog containing up to 20 full English card names for autocomplete purposes.

        Args:
            q: The string to autocomplete
            include_extras: If true, extra cards (tokens, planes, vanguards, etc) will be included. Default False

        """
        params = {"q": q, "include_extras": include_extras}

        result = await self.request(
            Route("GET", "/cards/autocomplete"),
            params=params,
        )

        return Catalog(**result)

    async def get_random_card(
        self,
        q: str | None = None,
    ) -> Card:
        params = {"q": q}

        result = await self.request(
            Route("GET", "/cards/random"),
            params=params,
        )

        result["_client"] = self
        return Card(**result)

    async def get_card_collection(self, identifiers: list[dict[str, Any]]):
        raise NotImplementedError("This endpoint has not been implemented")

    async def get_card_by_set_code_and_collector_number(self, code: str, number: str, lang: str | None = None) -> Card:
        result = await self.request(Route("GET", f"/cards/{code}/{number}{f'/{lang}' if lang else ''}"))

        result["_client"] = self
        return Card(**result)
