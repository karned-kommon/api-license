import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from models.item_model import Item
from models.response_model import SuccessResponse

client = TestClient(app)

# Mock data for tests
mock_items = [
    {
        "uuid": "item-1",
        "name": "Item 1",
        "entity_uuid": "entity-1",
        "user_uuid": None,
        "iat": int(datetime.now().timestamp()) - 3600,  # 1 hour ago
        "exp": int(datetime.now().timestamp()) + 3600,  # 1 hour from now
    },
    {
        "uuid": "item-2",
        "name": "Item 2",
        "entity_uuid": "entity-1",
        "user_uuid": "user-1",
        "iat": int(datetime.now().timestamp()) - 3600,  # 1 hour ago
        "exp": int(datetime.now().timestamp()) + 3600,  # 1 hour from now
    }
]

@pytest.fixture
def mock_repo():
    # Create a mock repository
    repo = MagicMock()
    return repo

@pytest.fixture
def mock_get_items():
    # Create a patch for the get_items function
    with patch('routers.v1.get_items') as mock:
        mock.return_value = mock_items
        yield mock

@pytest.fixture
def mock_get_item():
    # Create a patch for the get_item function
    with patch('routers.v1.get_item') as mock:
        mock.return_value = mock_items[0]
        yield mock

@pytest.fixture
def mock_request_state():
    # Create a patch for request.state attributes
    with patch('starlette.requests.Request.state', create=True) as mock:
        mock.entity_uuid = "entity-1"
        mock.user_uuid = "user-1"
        yield mock

# Test purchase endpoint
def test_purchase_endpoint(mock_get_items):
    # Mock the dependency
    app.dependency_overrides = {}
    
    # Make request to the endpoint
    response = client.get("/license/v1/purchase")
    
    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

# Test unassigned_items endpoint
def test_unassigned_items_endpoint(mock_get_items, mock_request_state):
    # Mock the dependency
    app.dependency_overrides = {}
    
    # Make request to the endpoint
    response = client.get("/license/v1/unassigned")
    
    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

# Test read_item endpoint
def test_read_item_endpoint(mock_get_item, mock_request_state):
    # Mock the dependency
    app.dependency_overrides = {}
    
    # Make request to the endpoint
    response = client.get("/license/v1/license/item-1")
    
    # Check response
    assert response.status_code in (200, 401, 403, 404)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["uuid"] == "item-1"

# Test get_mine endpoint
def test_get_mine_endpoint(mock_get_items, mock_request_state):
    # Mock the dependency
    app.dependency_overrides = {}
    
    # Make request to the endpoint
    response = client.get("/license/v1/mine")
    
    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data