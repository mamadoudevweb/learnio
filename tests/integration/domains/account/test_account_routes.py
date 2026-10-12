from uuid import uuid4


def test_create_account_route_success(client, auth_headers):
    res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={
            "first_name": "Mariama",
            "last_name": "Sow",
            "birth_date": "2004-03-12",
            "active": True,
        },
    )
    assert res.status_code == 201
    assert res.json["success"] is True
    assert res.json["data"]["first_name"] == "Mariama"
    assert "id" in res.json["data"]


def test_get_account_route_success(client, auth_headers):
    create_res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "GetTest", "last_name": "User"},
    )
    acc_id = create_res.json["data"]["id"]

    res = client.get(f"/api/v1/accounts/{acc_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["success"] is True
    assert res.json["data"]["id"] == acc_id


def test_get_account_route_not_found(client, auth_headers):
    fake_id = str(uuid4())
    res = client.get(f"/api/v1/accounts/{fake_id}", headers=auth_headers)
    assert res.status_code == 404
    assert res.json["success"] is False
    assert res.json["error"]["code"] == "ACCOUNT_NOT_FOUND"


def test_list_accounts_route_success(client, auth_headers):
    client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "ListSearchTest", "last_name": "User"},
    )
    res = client.get("/api/v1/accounts?search=ListSearchTest", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["success"] is True
    assert len(res.json["data"]) >= 1


def test_update_account_route_success(client, auth_headers):
    create_res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "BeforeUpdate", "last_name": "User"},
    )
    acc_id = create_res.json["data"]["id"]

    res = client.put(
        f"/api/v1/accounts/{acc_id}",
        headers=auth_headers,
        json={"first_name": "AfterUpdate"},
    )
    assert res.status_code == 200
    assert res.json["data"]["first_name"] == "AfterUpdate"


def test_assign_role_to_account_route_success(client, auth_headers):
    acc_res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "AssignRole", "last_name": "User"},
    )
    acc_id = acc_res.json["data"]["id"]

    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "assignable_role", "description": "Desc"},
    )
    role_id = role_res.json["data"]["id"]

    res = client.post(
        f"/api/v1/accounts/{acc_id}/roles/{role_id}",
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert role_id in res.json["data"]["role_ids"]


def test_revoke_role_from_account_route_success(client, auth_headers):
    acc_res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "RevokeRole", "last_name": "User"},
    )
    acc_id = acc_res.json["data"]["id"]

    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "revokable_role", "description": "Desc"},
    )
    role_id = role_res.json["data"]["id"]

    client.post(
        f"/api/v1/accounts/{acc_id}/roles/{role_id}",
        headers=auth_headers,
    )

    res = client.delete(
        f"/api/v1/accounts/{acc_id}/roles/{role_id}",
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert role_id not in res.json["data"]["role_ids"]


def test_delete_account_route_success(client, auth_headers):
    acc_res = client.post(
        "/api/v1/accounts",
        headers=auth_headers,
        json={"first_name": "ToDelete", "last_name": "User"},
    )
    acc_id = acc_res.json["data"]["id"]

    res = client.delete(f"/api/v1/accounts/{acc_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["success"] is True

    # Ensure it's deleted
    get_res = client.get(f"/api/v1/accounts/{acc_id}", headers=auth_headers)
    assert get_res.status_code == 404
