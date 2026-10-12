import uuid


def test_document_routes_crud(client, auth_headers):
    subject_id = str(uuid.uuid4())
    chapter_id = str(uuid.uuid4())

    # 1. Create document
    create_response = client.post(
        "/api/v1/documents",
        json={
            "title": "Cours d'Économie - La Monnaie",
            "file_path": "uploads/eco_monnaie.pdf",
            "file_name": "eco_monnaie.pdf",
            "file_size_bytes": 204800,
            "mime_type": "application/pdf",
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "document_type": "course",
            "source": "user",
            "year": 2024,
            "extracted_text": "Définition et fonctions de la monnaie",
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    assert create_response.json["success"] is True
    doc_id = create_response.json["data"]["id"]
    assert create_response.json["data"]["title"] == "Cours d'Économie - La Monnaie"
    assert create_response.json["data"]["is_text_extracted"] is True

    # 2. Get document
    get_response = client.get(f"/api/v1/documents/{doc_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json["data"]["id"] == doc_id
    assert get_response.json["data"]["document_type"] == "course"

    # 3. List documents with filter
    list_response = client.get(
        f"/api/v1/documents?subject_id={subject_id}&document_type=course",
        headers=auth_headers,
    )
    assert list_response.status_code == 200
    assert len(list_response.json["data"]) == 1
    assert list_response.json["meta"]["total"] == 1

    # 4. Update document metadata
    update_response = client.put(
        f"/api/v1/documents/{doc_id}",
        json={
            "title": "Cours d'Économie - La Monnaie et le Crédit",
            "year": 2025,
        },
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json["data"]["title"] == "Cours d'Économie - La Monnaie et le Crédit"
    assert update_response.json["data"]["year"] == 2025

    # 5. Delete document
    delete_response = client.delete(f"/api/v1/documents/{doc_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    # 6. Verify 404 after delete
    get_after_delete = client.get(f"/api/v1/documents/{doc_id}", headers=auth_headers)
    assert get_after_delete.status_code == 404
    assert get_after_delete.json["success"] is False
    assert get_after_delete.json["error"]["code"] == "LIBRARY_DOCUMENT_NOT_FOUND"
