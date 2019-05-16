#!/usr/bin/env python3.7

from aiohttp import web


async def bad_creds_response():
    return web.Response(status=401,
                        text='{"msg": "Wrong email or password given."}',
                        content_type='application/json')


async def bad_request_response():
    return web.Response(status=400,
                        text='{"msg": "Invalid syntax in request."}',
                        content_type='application/json')


async def missing_body_keys_response():
    return web.Response(status=400,
                        text='{"msg": "Missing keys in request body."}',
                        content_type='application/json')


async def redirect_log_in_response(response_text):
    return web.Response(status=302,
                        text='{"msg": %s}' % response_text,
                        content_type='application/json')
