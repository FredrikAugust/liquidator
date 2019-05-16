#!/usr/bin/env python3.7

import sqlalchemy as sa
from aiohttp import web
from pymysql import MySQLError
from jwt import InvalidTokenError
from logzero import logger
from liquidator_server.handlers.responses import bad_request_response, bad_creds_response, missing_body_keys_response
from liquidator_server.database.models import user, user_company
from liquidator_server.utils.auth import check_password, create_jwt, validate_jwt


async def log_in(request):
    body = await request.json()
    engine = None

    if not all(k in body for k in ("email", "password")):
        return await missing_body_keys_response()

    try:
        engine = request.app['db']
        conn = await engine.acquire()
        query_user = (sa.select([user], use_labels=True).select_from(user).where(user.c.email == body['email']))
        result = await conn.execute(query_user)
        user_db = await result.fetchone()

        if result.rowcount != 1 or not check_password(body['password'], user_db.user_hash):
            return await bad_creds_response()

        else:
            query_user_companies = (sa.select([user_company], use_labels=True)
                                    .select_from(user_company).where(user_company.c.user_id == user_db.user_user_id))
            companies_result = await conn.execute(query_user_companies)
            user_company_rows = await companies_result.fetchall()

            user_companies = []
            for row in user_company_rows:
                user_companies.append(row.user_company_company_id)
            payload = {"user_id": user_db.user_user_id, "user_company": user_companies}
            token = create_jwt(payload)
            return web.Response(status=200,
                                text='{"X-CSRF-Token": "%s"}' % token,
                                content_type='application/json')

    except MySQLError as e:
        logger.exception(e)
        return web.Response(status=500)
    except InvalidTokenError as e:
        logger.exception(e)
        return web.Response(status=500)
    finally:
        if engine is not None:
            engine.release(conn)
