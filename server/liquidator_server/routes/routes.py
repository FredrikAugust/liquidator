
from aiohttp import web
from liquidator_server.handlers.auth import log_in


def setup_routes(app):
    app.add_routes([
        web.post('/api/v1/login', log_in)
    ])
