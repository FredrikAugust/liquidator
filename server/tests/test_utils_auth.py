#!/usr/bin/env python3.7


from liquidator_server.utils.auth import get_base_claims, get_hashed_password, \
     check_password, create_jwt, validate_jwt, load_key_files


async def test_get_base_claims(cli):
    base_claims = get_base_claims()
    assert all(k in base_claims for k in ("exp", "iss", "aud"))
    assert base_claims["iss"] == "Kodeworks:Liquidator"
    assert base_claims["aud"] == "Kodeworks:Liquidator"


async def test_password_hashing_and_checking(cli):
    password = "testpassword"
    pwd_hash = get_hashed_password(password)
    assert pwd_hash is not None
    assert check_password(password, pwd_hash) is True
    assert check_password(password + "4", pwd_hash) is False


async def test_jwt_creation_and_validation(cli):
    load_key_files()
    additional_payload = {"user_id": 1, "user_companies": [1, 2]}
    token = create_jwt(additional_payload)
    assert token is not None
    validated = validate_jwt(token)
    assert validated is not False
    assert all(k in validated for k in ("exp", "iss", "aud", "user_id", "user_companies"))
    assert validated["user_id"] == 1
    assert validated["user_companies"][1] == 2
