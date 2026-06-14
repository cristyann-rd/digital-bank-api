from httpx import AsyncClient


def assert_no_password_data(payload) -> None:
    serialized = str(payload).lower()
    assert "password_hash" not in serialized
    assert "password" not in serialized


async def test_create_user_success(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/users",
        json={
            "name": "Ana Souza",
            "email": "ANA@example.com",
            "password": "SenhaForte1!",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Ana Souza"
    assert response.json()["email"] == "ana@example.com"
    assert "id" in response.json()
    assert_no_password_data(response.json())


async def test_duplicate_email_is_blocked(client: AsyncClient) -> None:
    payload = {
        "name": "Ana Souza",
        "email": "ana@example.com",
        "password": "SenhaForte1!",
    }

    first_response = await client.post("/api/v1/users", json=payload)
    duplicate_response = await client.post("/api/v1/users", json=payload)

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409


async def test_weak_password_is_blocked(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/users",
        json={
            "name": "Ana Souza",
            "email": "ana@example.com",
            "password": "Senha123",
        },
    )

    assert response.status_code == 422
    assert "simbolo" in response.json()["detail"].lower()


async def test_password_hash_never_appears_in_responses(
    client: AsyncClient,
    registered_user: dict,
    access_token: str,
) -> None:
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    me_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert_no_password_data(login_response.json())
    assert_no_password_data(me_response.json())
