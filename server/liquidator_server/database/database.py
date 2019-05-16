#!/usr/bin/env python3.7

from pymysql import MySQLError
from logzero import logger
from os import getenv
from aiomysql.sa import create_engine


async def init_db(app):
    try:
        logger.info("Try connecting to database...")
        engine = await create_engine(
            user=getenv("DB_USER"),
            db=getenv("DB_DB"),
            host=getenv("DB_HOST"),
            port=int(getenv("DB_PORT")),
            password=getenv("DB_PASSWORD"),
            maxsize=10)
        app['db'] = engine
        logger.info("Connected to database.")

    except MySQLError as e:
        logger.exception(e)
        logger.error("Connecting to database failed!")


async def close_db(app):
    engine = app['db']
    if engine is not None:
        logger.info("Waiting for database connections to close...")
        engine.close()
        await engine.wait_closed()
        logger.info("Database engine closed!")
