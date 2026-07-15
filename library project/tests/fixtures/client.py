# tests/conftest.py

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from library_app.main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as client:
        yield client

















# @pytest.mark.async
# async def test_create_order(client):
#     response = await client.post(
#         "/orders",
#         json={"product_id": 1}
#     )

#     assert response.status_code == 201



# async def test_create_order(client, account_with_token):
#     response = await client.post(
#         "/orders",
#         headers=account_with_token.headers,
#         json={}
#     )

# async def test_create_order(client, authenticated_user):
#     response = await client.post(
#         "/orders",
#         json={"product_id": 1},
#         headers=authenticated_user["headers"]
#     )

#     assert response.status_code == 201