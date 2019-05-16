# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from os import getenv
from liquidator_server.database.models import user, company, user_company, entry, entry_category
from liquidator_server.utils.auth import load_key_files, get_hashed_password

load_dotenv(override=True)

db_url = 'mysql+pymysql://' + getenv("DB_USER") +":"+ getenv("DB_PASSWORD") +"@"+ getenv("DB_HOST") \
        +":"+ getenv("DB_PORT") #+"/"+ getenv("DB_DB")

print("db_url:", db_url)

initial_engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
main_engine = create_engine(db_url + "/" + getenv("DB_DB"), isolation_level='AUTOCOMMIT')


def setup_db():
    print("Creating database...")
    conn = initial_engine.connect()

    conn.execute("DROP DATABASE IF EXISTS %s" % getenv("DB_DB"))
    conn.execute("CREATE DATABASE %s CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" % getenv("DB_DB"))
    conn.close()


def drop_tables(engine=main_engine):
    print("Dropping tables...")
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[user, company, user_company, entry, entry_category])


def create_tables(engine=main_engine):
    print("Creating tables...")
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user, company, user_company, entry, entry_category])


def sample_data(engine=main_engine):
    print("Populating database with sample data...")
    load_key_files()
    password = "password123"
    password_hash = get_hashed_password(password)
    conn = engine.connect()
    conn.execute(company.insert().values(
        name="The test company"
    ))

    conn.execute(entry_category.insert().values(
        name="Lønn",
        description="Utgifter av typen 'Lønn'."
    ))

    conn.execute(user.insert().values(
        first_name="Test1",
        last_name="Test",
        email="test1@test.com",
        hash=password_hash,
        verification_code="teststring",
        verified=True
    ))

    conn.execute(user.insert().values(
        first_name="Test2",
        last_name="Test2",
        email="test2@test.com",
        hash=password_hash,
        verification_code="teststring2",
        verified=False
    ))

    conn.execute(user_company.insert().values(
        user_id=1,
        company_id=1
    ))

    conn.execute(entry.insert().values(
        amount=-10000,
        description="Deltidsansatt Ørjan",
        start_date=datetime.date.today(),
        occurring=4,
        days_between=31,
        category_id=1,
        company_id=1
    ))

    conn.close()


if __name__ == '__main__':
    setup_db()
    create_tables()
    sample_data()
    # drop_tables()

