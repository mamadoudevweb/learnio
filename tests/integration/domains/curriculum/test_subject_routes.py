def test_create_and_get_subject(client, auth_headers):
    # Create
    create_response = client.post(
        "/api/v1/subjects",
        json={"name": "Informatique", "code": "INFO"},
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    data = create_response.json["data"]
    assert data["name"] == "Informatique"
    assert data["code"] == "INFO"
    subject_id = data["id"]

    # Get
    get_response = client.get(f"/api/v1/subjects/{subject_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json["data"]["name"] == "Informatique"

    # List
    list_response = client.get("/api/v1/subjects?code=INFO", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json["data"]) == 1

    # Update
    update_response = client.put(
        f"/api/v1/subjects/{subject_id}",
        json={"name": "Science Info"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json["data"]["name"] == "Science Info"

    # Delete
    delete_response = client.delete(
        f"/api/v1/subjects/{subject_id}", headers=auth_headers
    )
    assert delete_response.status_code == 200

    # Get after delete (404)
    get_after_delete = client.get(
        f"/api/v1/subjects/{subject_id}", headers=auth_headers
    )
    assert get_after_delete.status_code == 404
    assert get_after_delete.json["error"]["code"] == "CURRICULUM_SUBJECT_NOT_FOUND"


def test_create_subject_validation_error(client, auth_headers):
    response = client.post(
        "/api/v1/subjects",
        json={"name": "Informatique"},  # Missing code
        headers=auth_headers,
    )
    assert response.status_code == 422
    assert response.json["error"]["code"] == "VALIDATION_FAILED"
