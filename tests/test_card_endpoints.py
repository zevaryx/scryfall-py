import pytest

from scryfall import Scryfall

test_card_uuid = "1e90c638-d4b2-4243-bbc4-1cc10516c40f"
test_card_name = "Arcades, the Strategist"


@pytest.mark.asyncio
async def test_get_card_by_all_ids():
    client = Scryfall()
    card = await client.get_card_by_id(test_card_uuid)

    assert card.name == test_card_name
    assert card.arena_id is not None
    assert card.mtgo_id is not None
    assert card.tcgplayer_id is not None
    assert card.cardmarket_id is not None

    _ = await client.get_card_by_arena_id(card.arena_id)
    _ = await client.get_card_by_cardmarket_id(card.cardmarket_id)
    _ = await client.get_card_by_mtgo_id(card.mtgo_id)
    _ = await client.get_card_by_tcgplayer_id(card.tcgplayer_id)
    if card.multiverse_ids and len(card.multiverse_ids) > 0:
        _ = await client.get_card_by_multiverse_id(card.multiverse_ids[0])

    await client.close()


@pytest.mark.asyncio
async def test_get_card_rulings():
    client = Scryfall()
    card = await client.get_card_by_id(test_card_uuid)

    rulings = await card.get_rulings()
    assert len(rulings) > 0


@pytest.mark.asyncio
async def test_search_card_all():
    client = Scryfall()

    with pytest.raises(ValueError):
        _ = await client.search_cards(q="_" * 1001)

    with pytest.raises(ValueError):
        _ = await client.search_cards_named()

    cards = await client.search_cards(q="arcades, the strategist", unique="cards")
    assert any(str(x.id) == test_card_uuid for x in cards.data if x.object == "card")
    assert await cards.get_next_page() is None

    card = await client.search_cards_named(exact="arcades, the strategist")
    assert str(card.id) == test_card_uuid

    card = await client.search_cards_named(fuzzy="arcades the strategist")
    assert str(card.id) == test_card_uuid

    cards = await client.search_cards(q="angel")
    if cards.has_more:
        cards = await cards.get_next_page()


@pytest.mark.asyncio
async def test_cards_autocomplete():
    client = Scryfall()

    catalog = await client.cards_autocomplete(q="avacyn")

    assert "Avacyn, Angel of Hope" in catalog.data


@pytest.mark.asyncio
async def test_get_random_card():
    client = Scryfall()

    card = await client.get_random_card()
    assert card is not None


@pytest.mark.asyncio
async def test_card_set():
    client = Scryfall()
    card = await client.get_card_by_id(test_card_uuid)
    card_set = await card.get_set()

    assert card_set.code == "m19"
