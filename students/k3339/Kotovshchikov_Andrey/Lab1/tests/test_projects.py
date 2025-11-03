from faker import Faker
from httpx import AsyncClient
from fastapi import status


async def test_create_project_flow(client: AsyncClient, faker: Faker) -> None:
    # Register user
    user = {
        "email": faker.email(),
        "password": faker.password(length=8),
    }

    response = await client.post(url="/users/sign-up", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    token = response.json()["token"]

    # Create project
    expected_project = {
        "name": "Test Project",
        "description": faker.text(max_nb_chars=50),
        "deadline": faker.date(),
    }

    response = await client.post(
        url="/projects/",
        json=expected_project,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    actual_project = response.json()

    assert actual_project["name"] == expected_project["name"]
    assert actual_project["description"] == expected_project["description"]
    assert actual_project["deadline"] == expected_project["deadline"]
