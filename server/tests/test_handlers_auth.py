#!/usr/bin/env python3.7

import json


async def test_log_in_successful(cli):
    resp = await cli.post('/api/v1/login', data=json.dumps({"email": "test1@test.com", "password": "password123"}))
    assert resp.status == 200
    json_response = json.loads(await resp.text())
    assert json_response["X-CSRF-Token"] is not None


async def test_log_in_missing_email_key_in_request_body(cli):
    resp = await cli.post('/api/v1/login', data=json.dumps({"password": "password123"}))
    assert resp.status == 400
    json_response = json.loads(await resp.text())
    assert json_response["msg"] == "Missing keys in request body."


async def test_log_in_nonexistent_email(cli):
    resp = await cli.post('/api/v1/login', data=json.dumps({"email": "nonexistent@test.com", "password": "password123"}))
    assert resp.status == 401
    json_response = json.loads(await resp.text())
    assert json_response["msg"] == "Wrong email or password given."


async def test_log_in_wrong_password(cli):
    resp = await cli.post('/api/v1/login', data=json.dumps({"email": "test1@test.com", "password": "wrongpassword"}))
    assert resp.status == 401
    json_response = json.loads(await resp.text())
    assert json_response["msg"] == "Wrong email or password given."
