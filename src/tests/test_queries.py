import json
import pytest
from httpx import AsyncClient

from app.api.avito_tools import get_top5_deals
from app.main import app


@pytest.mark.asyncio
async def test_create_query(test_db):
    test_request_payload = {'text': 'bmx', 'region': 'moskva'}
    test_response_payload = {'id': 1}

    async with AsyncClient(app=app, base_url='http://localhost:8002') as client:
        response = await client.post('/add', data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.asyncio
async def test_create_query_invalid_json(test_db):
    async with AsyncClient(app=app, base_url='http://localhost:8002') as client:
        response = await client.post('/add', data=json.dumps({'text': 'bmx'}))

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_query_not_found(test_db):
    async with AsyncClient(app=app, base_url='http://localhost:8002') as client:
        response = await client.get('/stat/21')

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_top5_deals(test_db):
    test_request_payload = {'text': 'bmx', 'region': 'moskva'}

    async with AsyncClient(app=app, base_url='http://localhost:8002') as client:
        await client.post('/add', data=json.dumps(test_request_payload))
        response = await client.get('/top5_deals/1')

    expected = get_top5_deals(test_request_payload['text'], test_request_payload['region'])

    assert response.status_code == 200
    assert set(response.json()) == set(expected)
