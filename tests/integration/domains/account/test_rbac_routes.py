def test_create_permission_route_success(client, auth_headers):
    res = client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "curriculum", "resource": "lesson", "action": "publish"},
    )
    assert res.status_code == 201
    assert res.json["success"] is True
    assert "id" in res.json["data"]
    assert res.json["data"]["action"] == "publish"


def test_get_permission_route_success(client, auth_headers):
    create_res = client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "curriculum", "resource": "lesson", "action": "archive"},
    )
    perm_id = create_res.json["data"]["id"]

    res = client.get(f"/api/v1/permissions/{perm_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["data"]["id"] == perm_id


def test_list_permissions_route_success(client, auth_headers):
    client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "billing", "resource": "invoice", "action": "read"},
    )
    res = client.get("/api/v1/permissions?domain=billing", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json["data"]) >= 1


def test_delete_permission_route_success(client, auth_headers):
    create_res = client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "temp", "resource": "test", "action": "delete"},
    )
    perm_id = create_res.json["data"]["id"]

    res = client.delete(f"/api/v1/permissions/{perm_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["success"] is True


def test_create_role_route_success(client, auth_headers):
    res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "content_editor", "description": "Editor"},
    )
    assert res.status_code == 201
    assert res.json["success"] is True
    assert res.json["data"]["name"] == "content_editor"


def test_get_role_route_success(client, auth_headers):
    create_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "role_getter", "description": "Desc"},
    )
    role_id = create_res.json["data"]["id"]

    res = client.get(f"/api/v1/roles/{role_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["data"]["id"] == role_id


def test_list_roles_route_success(client, auth_headers):
    client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "list_target_role", "description": "Desc"},
    )
    res = client.get("/api/v1/roles?name=list_target_role", headers=auth_headers)
    assert res.status_code == 200
    assert any(r["name"] == "list_target_role" for r in res.json["data"])


def test_assign_permission_to_role_route_success(client, auth_headers):
    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "role_with_perm", "description": "Desc"},
    )
    role_id = role_res.json["data"]["id"]

    perm_res = client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "curriculum", "resource": "subject", "action": "manage"},
    )
    perm_id = perm_res.json["data"]["id"]

    res = client.post(
        f"/api/v1/roles/{role_id}/permissions/{perm_id}",
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert perm_id in res.json["data"]["permission_ids"]


def test_revoke_permission_from_role_route_success(client, auth_headers):
    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "role_revoke_perm", "description": "Desc"},
    )
    role_id = role_res.json["data"]["id"]

    perm_res = client.post(
        "/api/v1/permissions",
        headers=auth_headers,
        json={"domain": "curriculum", "resource": "subject", "action": "export"},
    )
    perm_id = perm_res.json["data"]["id"]

    client.post(
        f"/api/v1/roles/{role_id}/permissions/{perm_id}",
        headers=auth_headers,
    )

    res = client.delete(
        f"/api/v1/roles/{role_id}/permissions/{perm_id}",
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert perm_id not in res.json["data"]["permission_ids"]


def test_delete_role_route_success(client, auth_headers):
    role_res = client.post(
        "/api/v1/roles",
        headers=auth_headers,
        json={"name": "role_to_delete", "description": "Desc"},
    )
    role_id = role_res.json["data"]["id"]

    res = client.delete(f"/api/v1/roles/{role_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["success"] is True

    get_res = client.get(f"/api/v1/roles/{role_id}", headers=auth_headers)
    assert get_res.status_code == 404
