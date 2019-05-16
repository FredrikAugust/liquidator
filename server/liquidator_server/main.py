#!/usr/bin/env python3.7

from aiohttp import web
from dotenv import load_dotenv
from logzero import logger
from os import getenv
from liquidator_server.database.database import init_db, close_db
from liquidator_server.utils.auth import load_key_files
from liquidator_server.routes.routes import setup_routes


async def init_app():
    load_dotenv(override=True)
    load_key_files()
    app = web.Application()
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    setup_routes(app)
    return app


def main():
    app = init_app()
    # Start the Web-server
    if getenv("ENVIRONMENT") == "development":
        logger.info("Starting application in 'development' mode.")

    web.run_app(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
