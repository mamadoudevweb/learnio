from src.core.entities import generate_id


def test_lesson_crud(client, auth_headers):
    chapter_id = generate_id()

    # Create
    create_response = client.post(
        "/api/v1/lessons",
        json={
            "chapter_id": str(chapter_id),
            "title": "Leçon 1",
            "content": "Contenu complet de la leçon",
            "order": 1,
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    lesson_id = create_response.json["data"]["id"]

    # Get
    get_response = client.get(f"/api/v1/lessons/{lesson_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json["data"]["title"] == "Leçon 1"

    # List
    list_response = client.get(
        f"/api/v1/lessons?chapter_id={chapter_id}", headers=auth_headers
    )
    assert list_response.status_code == 200
    assert len(list_response.json["data"]) == 1

    # Update
    update_response = client.put(
        f"/api/v1/lessons/{lesson_id}",
        json={"title": "Leçon 1 - Modifié"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json["data"]["title"] == "Leçon 1 - Modifié"

    # Delete
    delete_response = client.delete(
        f"/api/v1/lessons/{lesson_id}", headers=auth_headers
    )
    assert delete_response.status_code == 200
