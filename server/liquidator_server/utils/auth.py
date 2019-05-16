#!/usr/bin/env python3.7

import pathlib
import bcrypt
import jwt
import os
from logzero import logger
import time
from functools import wraps
from os import path
from liquidator_server.handlers.responses import redirect_log_in_response


TTL = 3600


ROOTDIR = pathlib.Path(__file__).parent.parent.parent


def load_key_files():
    try:
        global public_key, private_key
        public_key_name = os.getenv("PUBLIC_KEY_NAME")
        private_key_name = os.getenv("PRIVATE_KEY_NAME")

        public_key = open(path.abspath(path.join(ROOTDIR, public_key_name)), "r").read()
        private_key = open(path.abspath(path.join(ROOTDIR, private_key_name)), "r").read()

    except FileNotFoundError as e:
        logger.exception(e)
        logger.warning("Token creation and validation will not work without RSA-keys.")


def get_base_claims():
    base_claims = {
        "exp": 900,
        "iss": "Kodeworks:Liquidator",
        "aud": "Kodeworks:Liquidator"
    }
    return base_claims


def get_hashed_password(password_string):
    try:
        hashed_password = bcrypt.hashpw(password_string.encode(), bcrypt.gensalt(12))
        return hashed_password
    except Exception as e:
        logger.exception(e)
        return None


def check_password(password_string, hashed_password):
    try:
        if type(hashed_password) is str:
           hashed_password = hashed_password.encode()

        return bcrypt.checkpw(password_string.encode(), hashed_password)
    except Exception as e:
        logger.exception(e)
        return False


def create_jwt(additional_payload):
    try:
        payload = get_base_claims()
        payload["exp"] += time.time()
        for key in additional_payload:
            payload[key] = additional_payload[key]
        encoded = jwt.encode(payload, private_key, algorithm='RS256').decode("UTF8")
        return encoded

    except Exception as e:
        logger.exception(e)
        logger.error("Error creating token.")
        return None


def validate_jwt(token):
    try:
        payload = jwt.decode(token.encode("UTF8"), public_key, algorithms='RS256',
                             issuer='Kodeworks:Liquidator', audience='Kodeworks:Liquidator')
        return payload

    except jwt.exceptions.ExpiredSignatureError as e:
        logger.exception(e)
        return None


def requires_auth(func):
    """
    A decorator to use on aiohttp endpoints to run authentication on all
    requests before calling the endpoint function.
    :param func: The function to wrap
    :return: The decorated function
    """
    def decorator(f):
        @wraps(f)
        async def wrapper(request):
            token = request.headers.get('X-CSRF-Token')
            verified = validate_jwt(token)
            if verified is None:
                return await redirect_log_in_response("Your token has expired or you're not logged in. Please log in and try again")
            request['token-claims'] = verified
            return await f(request)

        return wrapper

    return decorator(func) if func else decorator

