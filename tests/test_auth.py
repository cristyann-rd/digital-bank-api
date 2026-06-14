from httpx import AsyncClient


async def test_valid_login_returns_access_token(
    client: AsyncClient,
    registered_user: dict,
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


async def test_wrong_password_returns_401(
    client: AsyncClient,
    registered_user: dict,
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": "SenhaErrada1!",
        },
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


async def test_unknown_email_returns_generic_401(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "unknown@example.com",
            "password": "SenhaForte1!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos"


async def test_me_without_token_returns_401(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users/me")

    assert response.status_code == 401


async def test_me_with_invalid_token_returns_401(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


async def test_me_with_valid_token_returns_user(
    client: AsyncClient,
    registered_user: dict,
    access_token: str,
) -> None:
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == registered_user["id"]
    assert response.json()["email"] == registered_user["email"]
    assert "password_hash" not in response.json()
