import pytest
from liquidator_server.main import init_app


@pytest.fixture
async def cli(loop, aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)
