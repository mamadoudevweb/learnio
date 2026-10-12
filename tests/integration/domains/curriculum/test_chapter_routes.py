from src.core.entities import generate_id


def test_chapter_crud(client, auth_headers):
    subject_id = generate_id()

    # Create
    create_response = client.post(
        "/api/v1/chapters",
        json={
            "subject_id": str(subject_id),
            "title": "Chapitre 1",
            "order": 1,
            "description": "Intro",
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    chapter_id = create_response.json["data"]["id"]

    # Get
    get_response = client.get(f"/api/v1/chapters/{chapter_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json["data"]["title"] == "Chapitre 1"

    # List
    list_response = client.get(
        f"/api/v1/chapters?subject_id={subject_id}", headers=auth_headers
    )
    assert list_response.status_code == 200
    assert len(list_response.json["data"]) == 1

    # Update
    update_response = client.put(
        f"/api/v1/chapters/{chapter_id}",
        json={"title": "Chapitre 1 - Modifié"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json["data"]["title"] == "Chapitre 1 - Modifié"

    # Delete
    delete_response = client.delete(
        f"/api/v1/chapters/{chapter_id}", headers=auth_headers
    )
    assert delete_response.status_code == 200
