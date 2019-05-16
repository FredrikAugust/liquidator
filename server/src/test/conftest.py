import pytest
from app import app_factory


@pytest.fixture
async def cli(loop, aiohttp_client):
    app = await app_factory()
    return await aiohttp_client(app)
