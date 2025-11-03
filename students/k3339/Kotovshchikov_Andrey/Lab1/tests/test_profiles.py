from faker import Faker
from fastapi import status
from httpx import AsyncClient


async def test_create_user_profile_success(client: AsyncClient, faker: Faker) -> None:
    user = {
        "email": faker.email(),
        "password": faker.password(length=8),
    }

    response = await client.post(url="/users/sign-up", json=user)
    assert response.status_code == 201
    token = response.json()["token"]

    # Create user profile
    expected_profile = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birthdate": faker.date(),
        "about_me": faker.text(max_nb_chars=50),
        "work_experience": 12,
    }

    response = await client.post(
        url="/profiles/me",
        json=expected_profile,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    actual_profile = response.json()

    assert expected_profile["first_name"] == actual_profile["first_name"]
    assert expected_profile["last_name"] == actual_profile["last_name"]
    assert expected_profile["birthdate"] == actual_profile["birthdate"]
    assert expected_profile["about_me"] == actual_profile["about_me"]
    assert expected_profile["work_experience"] == actual_profile["work_experience"]


async def test_create_user_profile_when_unauthorized(
    client: AsyncClient,
    faker: Faker,
) -> None:
    profile = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birthdate": faker.date(),
        "about_me": faker.text(max_nb_chars=50),
        "work_experience": 3,
    }

    response = await client.post(url="/profiles/me", json=profile)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
