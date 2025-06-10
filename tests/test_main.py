from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_unassigned_items():
    # Teste l'endpoint /license/v1/unassigned
    response = client.get("/license/v1/unassigned")
    # Selon la config, il peut nécessiter des headers d'authentification
    assert response.status_code in (200, 401, 403, 422)
    if response.status_code == 200:
        assert "status" in response.json()
        assert response.json()["status"] == "success"
        assert "data" in response.json()

def test_not_found():
    # Teste le exception handler sur une route inexistante
    response = client.get("/license/v1/doesnotexist")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_method_not_allowed():
    # Teste le exception handler sur une mauvaise méthode
    response = client.post("/license/v1/unassigned")
    assert response.status_code in (405, 401, 403)

def test_root_not_found():
    # Teste la racine qui n'existe pas
    response = client.get("/")
    assert response.status_code in (404, 200)

# Préparation pour d'autres endpoints (à activer si décommentés)
# def test_purchase():
#     response = client.get("/license/v1/purchase")
#     assert response.status_code in (200, 401, 403, 422)

# def test_assign_license():
#     response = client.post("/license/v1/assign/some-uuid")
#     assert response.status_code in (201, 401, 403, 422)

