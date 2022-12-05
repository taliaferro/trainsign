import pytest
import os
from open511 import Open511Client
from .visit_stream import visit_stream


@pytest.fixture
def client():
    return Open511Client(api_key=os.getenv("TRAIN_SIGN_KEY"))


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_visit_stream(client):
    index = 0
    async for visit in visit_stream(client=client, agency="SF"):
        assert visit
        index += 1
        if index > 9:
            break

@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_filtertron(client):
    index = 0
    async for visit in visit_stream(client=client, agency="SF"):
        assert visit
        index += 1
        if index > 9:
            break

@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_sign_display(client):
    index = 0
    async for visit in visit_stream(client=client, agency="SF"):
        assert visit
        index += 1
        if index > 9:
            break
