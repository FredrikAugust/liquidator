#!/usr/bin/env python3.7

import datetime
from pymysql import MySQLError
from logzero import logger
import sqlalchemy as sa
import os
from aiomysql.sa import create_engine
from database.models import user, company, user_company, entry, entry_category
from utils.auth import get_hashed_password, check_password

engine = None


async def create_tables(conn):
    # Drop tables if exist
    await conn.execute('DROP TABLE IF EXISTS user_company')
    await conn.execute('DROP TABLE IF EXISTS entry')
    await conn.execute('DROP TABLE IF EXISTS user')
    await conn.execute('DROP TABLE IF EXISTS company')
    await conn.execute('DROP TABLE IF EXISTS entry_category')

    # Create tables
    await conn.execute('''CREATE TABLE user (user_id int NOT NULL AUTO_INCREMENT, 
                            first_name varchar(255) NOT NULL,
                            last_name varchar(255) NOT NULL,
                            email varchar(255) NOT NULL UNIQUE, 
                            hash varchar(255) NOT NULL,
                            verification_code varchar(255) NOT NULL,
                            verified bool,
                            PRIMARY KEY (user_id))''')

    await conn.execute('''CREATE TABLE company(
                            company_id int NOT NULL AUTO_INCREMENT,
                            name varchar(255) NOT NULL,
                            PRIMARY KEY (company_id)
                        )''')

    await conn.execute('''CREATE TABLE entry_category(
                            category_id int NOT NULL AUTO_INCREMENT,
                            name varchar(255) NOT NULL UNIQUE,
                            description varchar(255),
                            PRIMARY KEY (category_id)
                        )''')

    await conn.execute('''CREATE TABLE user_company(
                                company_id int NOT NULL,
                                user_id int NOT NULL,
                                PRIMARY KEY (company_id, user_id),
                                FOREIGN KEY (company_id) 
                                    REFERENCES company(company_id),
                                FOREIGN KEY (user_id)
                                    REFERENCES user(user_id)
                            )''')

    await conn.execute('''CREATE TABLE entry(
                        entry_id int NOT NULL AUTO_INCREMENT,
                        amount int NOT NULL,
                        description varchar(255),
                        start_date DATE NOT NULL,
                        occurring int NOT NULL,
                        days_between int,
                        category_id int NOT NULL,
                        company_id int NOT NULL,
                        PRIMARY KEY (entry_id),
                        FOREIGN KEY (category_id)
                            REFERENCES entry_category(category_id),
                        FOREIGN KEY (company_id)
                            REFERENCES company(company_id) 
                        )''')


async def fill_data(conn):
    password = 'password123'
    password_hash = get_hashed_password(password)
    async with conn.begin():
        await conn.execute(company.insert().values(
            name="The test company"
        ))

        await conn.execute(entry_category.insert().values(
            name="Lønn",
            description="Utgifter av typen 'Lønn'."
        ))

        await conn.execute(user.insert().values(
            first_name="Test1",
            last_name="Test",
            email="test1@test.com",
            hash=password_hash,
            verification_code="teststring",
            verified=True
        ))

        await conn.execute(user.insert().values(
            first_name="Test2",
            last_name="Test2",
            email="test2@test.com",
            hash=password_hash,
            verification_code="teststring2",
            verified=False
        ))

        await conn.execute(user_company.insert().values(
            user_id=1,
            company_id=1
        ))

        await conn.execute(entry.insert().values(
            amount=-10000,
            description="Deltidsansatt Ørjan",
            start_date=datetime.date.today(),
            occurring=4,
            days_between=31,
            category_id=1,
            company_id=1
        ))


async def test_password(password):
    conn = await engine.acquire()
    query = (sa.select([user], use_labels=True).select_from(user).where(user.c.email == 'orjan@hotmail.com'))
    result = await conn.execute(query)
    result_row = await result.fetchone()
    print(result_row.user_email)
    return check_password(password, result_row.user_hash)


async def show_users(conn):
    query = (sa.select([user], use_labels=True).select_from(user))
    async for row in conn.execute(query):
        print(row.user_id, row.email)
        print()


async def init_database_engine():
    global engine
    DB_DB = os.getenv("DB_DB")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_HOST = os.getenv("DB_HOST")
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    logger.info("Try connecting to database...")
    try:
        engine = await create_engine(user=DB_USER, db=DB_DB, host=DB_HOST, port=DB_PORT, password=DB_PASSWORD, maxsize=10)
        logger.info("Connected to database.")
        if ENVIRONMENT == "development":
            conn = await engine.acquire()
            logger.info("Setting up database")
            logger.info("Creating tables...")
            await create_tables(conn)
            logger.info("Inserting data...")
            await fill_data(conn)
            logger.info("Done!\n")
        engine.release(conn)
        return

    except MySQLError as e:
        logger.exception(e)
        logger.error("Connecting to database failed!")


def get_engine():
    try:
        return engine
    except MySQLError as e:
        raise MySQLError from e


async def tear_down_database():
    if engine is not None:
        logger.info("Waiting for database connections to close...")
        engine.close()
        await engine.wait_closed()
        logger.info("Database engine closed!")
