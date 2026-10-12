def test_register_route_success(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Fatou",
            "last_name": "Bah",
            "email": "fatou_reg@learnio.app",
            "password": "Password123!",
            "birth_date": "2006-02-20",
        },
    )
    assert res.status_code == 201
    assert res.json["success"] is True
    assert "id" in res.json["data"]
    assert res.json["data"]["first_name"] == "Fatou"


def test_register_route_duplicate_email_conflict(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Fatou",
            "last_name": "Bah",
            "email": "fatou_dup@learnio.app",
            "password": "Password123!",
        },
    )
    dup_res = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Other",
            "last_name": "Person",
            "email": "fatou_dup@learnio.app",
            "password": "Password123!",
        },
    )
    assert dup_res.status_code == 409
    assert dup_res.json["success"] is False


def test_register_route_invalid_data_validation_error(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"first_name": "", "email": "invalid"},
    )
    assert res.status_code == 422
    assert res.json["success"] is False


def test_login_route_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Login",
            "last_name": "User",
            "email": "login_ok@learnio.app",
            "password": "Password123!",
        },
    )
    res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_ok@learnio.app",
            "password": "Password123!",
        },
    )
    assert res.status_code == 200
    assert res.json["success"] is True
    assert "token" in res.json["data"]


def test_login_route_invalid_credentials(client):
    res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@learnio.app",
            "password": "WrongPassword!",
        },
    )
    assert res.status_code == 401
    assert res.json["success"] is False


def test_password_reset_request_route_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "ResetReq",
            "last_name": "User",
            "email": "reset_req@learnio.app",
            "password": "Password123!",
        },
    )
    res = client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "reset_req@learnio.app"},
    )
    assert res.status_code == 200
    assert res.json["success"] is True
    assert "token" in res.json["data"]


def test_password_reset_confirm_route_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "ResetConf",
            "last_name": "User",
            "email": "reset_conf@learnio.app",
            "password": "OldPassword123!",
        },
    )
    req_res = client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "reset_conf@learnio.app"},
    )
    token = req_res.json["data"]["token"]

    confirm_res = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": token,
            "new_password": "NewSecretPassword123!",
        },
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json["success"] is True


def test_logout_route_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Logout",
            "last_name": "User",
            "email": "logout_route@learnio.app",
            "password": "Password123!",
        },
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logout_route@learnio.app",
            "password": "Password123!",
        },
    )
    token = login_res.json["data"]["token"]

    logout_res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_res.status_code == 200
    assert logout_res.json["success"] is True
