from faker import Faker
import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize(
    "user",
    (
        {
            "email": "example@gmail.com",
            "password": "12345",
        },
    ),
)
async def test_sign_up_firstly_success(client: AsyncClient, user: dict) -> None:
    # Resister new user
    response = await client.post(url="/users/sign-up", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    sign_up_response = dict(response.json())
    assert sign_up_response["user"]["email"] == user["email"]

    # Sign in with registered credentials
    response = await client.post(url="/users/sign-in", json=user)
    assert response.status_code == status.HTTP_200_OK
    sign_in_response = dict(response.json())
    assert sign_in_response["user"] == sign_up_response["user"]


async def test_sign_up_when_email_occupied(client: AsyncClient, faker: Faker) -> None:
    # Resister user
    user = {
        "email": faker.email(),
        "password": faker.password(length=8),
    }

    response = await client.post(url="/users/sign-up", json=user)
    assert response.status_code == 201

    # Check email conflict response
    response = await client.post(url="/users/sign-up", json=user)
    assert response.status_code == status.HTTP_409_CONFLICT
