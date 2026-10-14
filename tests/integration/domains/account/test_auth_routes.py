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


def test_password_reset_request_route_success(client, app):
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
    assert "token" not in res.json["data"]
    assert "message" in res.json["data"]

    email_sender = app.extensions["email_sender"]
    assert len(email_sender.outbox) == 1
    sent = email_sender.outbox[0]
    assert sent.to == "reset_req@learnio.app"
    assert sent.html_body is not None
    assert "<!DOCTYPE html>" in sent.html_body
    assert "LEARNIO" in sent.html_body
    assert "Votre code à usage unique" in sent.html_body
    token = sent.metadata["token"]
    assert token in sent.body
    assert token in sent.html_body


def test_password_reset_confirm_route_success(client, app):
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
    assert req_res.status_code == 200
    assert "token" not in req_res.json["data"]

    sent = app.extensions["email_sender"].outbox[-1]
    token = sent.metadata["token"]

    # Verify GET endpoint with token as query parameter
    verify_res = client.get(f"/api/v1/auth/password-reset/confirm?token={token}")
    assert verify_res.status_code == 200
    assert verify_res.json["data"]["valid"] is True

    # Confirm with token as query parameter
    confirm_res = client.post(
        f"/api/v1/auth/password-reset/confirm?token={token}",
        json={
            "new_password": "NewSecretPassword123!",
        },
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json["success"] is True


def test_password_reset_confirm_with_path_parameter_success(client, app):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "ResetPath",
            "last_name": "User",
            "email": "reset_path@learnio.app",
            "password": "OldPassword123!",
        },
    )
    client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "reset_path@learnio.app"},
    )
    sent = app.extensions["email_sender"].outbox[-1]
    token = sent.metadata["token"]

    # Confirm with token in URL path
    confirm_res = client.post(
        f"/api/v1/auth/password-reset/confirm/{token}",
        json={
            "new_password": "PathPassword123!",
        },
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json["success"] is True


def test_password_reset_confirm_without_token_fails(client):
    res = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={"new_password": "MissingTokenPassword123!"},
    )
    assert res.status_code == 422
    assert res.json["success"] is False
    assert res.json["error"]["code"] == "VALIDATION_FAILED"


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
