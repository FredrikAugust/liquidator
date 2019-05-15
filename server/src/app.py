#!/usr/bin/env python3.7

from aiohttp import web
from dotenv import load_dotenv
from logzero import logger
from os import getenv
from database.database import init_database_engine, tear_down_database
from utils.auth import load_key_files
from handlers.auth import log_in


async def app_factory():
    load_dotenv(override=True)
    load_key_files()
    await init_database_engine()
    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.add_routes([web.post('/api/v1/login', log_in)])
    return app


async def on_shutdown(app):
    logger.info("Shuting down server...")
    await tear_down_database()
    logger.info("Server shut down gracefully")


def main():
    # Load environment variables
    load_dotenv(override=True)

    # Start the Web-server
    if getenv("ENVIRONMENT") == "development":
        logger.info("Starting application in 'development' mode.")

    web.run_app(app_factory(), host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
