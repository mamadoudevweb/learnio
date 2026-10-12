def test_auth_and_account_routes(client, auth_headers):
    # 1. Register endpoint
    reg_res = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Fatou",
            "last_name": "Bah",
            "email": "fatou@learnio.app",
            "password": "Password123!",
            "birth_date": "2006-02-20",
        },
    )
    assert reg_res.status_code == 201
    assert reg_res.json["success"] is True
    account_id = reg_res.json["data"]["id"]

    # 2. Login endpoint
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "fatou@learnio.app",
            "password": "Password123!",
        },
    )
    assert login_res.status_code == 200
    assert login_res.json["success"] is True
    assert "token" in login_res.json["data"]

    # 3. Account routes
    get_acc_res = client.get(f"/api/v1/accounts/{account_id}", headers=auth_headers)
    assert get_acc_res.status_code == 200
    assert get_acc_res.json["data"]["first_name"] == "Fatou"

    # 4. Roles routes
    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "student", "description": "Student role"},
    )
    assert role_res.status_code == 201
    assert role_res.json["data"]["name"] == "student"
