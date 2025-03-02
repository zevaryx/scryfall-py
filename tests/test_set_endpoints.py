import pytest

from pyfall import Pyfall

test_set_uuid = "2f5f2509-56db-414d-9a7e-6e312ec3760c"
test_set_name = "Core Set 2019"
test_set_code = "m19"


@pytest.mark.asyncio
async def test_get_all_sets():
    client = Pyfall()
    _ = await client.get_all_sets()


@pytest.mark.asyncio
async def test_get_set():
    client = Pyfall()

    set_ = await client.get_set_by_id(test_set_uuid)
    assert set_.name == test_set_name

    if set_.tcgplayer_id is not None:
        assert (await client.get_set_by_tcgplayer_id(set_.tcgplayer_id)) is not None

    assert str((await client.get_set_by_code("m19")).id) == test_set_uuid
