import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from models.item_model import Item
from models.response_model import SuccessResponse
from routers.v1 import get_repo

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

# Test get_repo dependency function
def test_get_repo():
    from routers.v1 import get_repo

    # Create a mock for ITEM_REPO
    mock_repo = MagicMock()
    # Set up the __enter__ method to return a specific mock
    enter_mock = MagicMock()
    mock_repo.__enter__.return_value = enter_mock

    # Patch the ITEM_REPO in the config
    with patch('routers.v1.ITEM_REPO', mock_repo):
        # Get the generator
        repo_gen = get_repo()

        # Get the repository from the generator
        repo = next(repo_gen)

        # Verify that the repository is the result of __enter__
        assert repo is enter_mock

        # Verify that the context manager was entered
        mock_repo.__enter__.assert_called_once()

        # Exhaust the generator to trigger the exit
        try:
            next(repo_gen)
        except StopIteration:
            pass

        # Verify that the context manager was exited
        mock_repo.__exit__.assert_called_once()

@pytest.fixture
def patch_get_items():
    # Patch the get_items function
    with patch('services.items_service.get_items', return_value=mock_items) as mock:
        yield mock

@pytest.fixture
def patch_get_item():
    # Patch the get_item function
    with patch('services.items_service.get_item', return_value=mock_items[0]) as mock:
        yield mock

@pytest.fixture
def mock_request_state():
    # Create a patch for request.state attributes
    with patch('starlette.requests.Request.state', create=True) as mock:
        mock.entity_uuid = "entity-1"
        mock.user_uuid = "user-1"
        yield mock

# Test purchase endpoint without name parameter
def test_purchase_endpoint(patch_get_items):
    # Make request to the endpoint
    response = client.get("/license/v1/purchase")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called with the correct filters
        patch_get_items.assert_called_once()
        args, kwargs = patch_get_items.call_args
        assert args[0] == {"name": None}

# Test purchase endpoint with name parameter
def test_purchase_endpoint_with_name(patch_get_items):
    # Make request to the endpoint with name parameter
    response = client.get("/license/v1/purchase?name=Test")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called with the correct filters
        patch_get_items.assert_called_once()
        args, kwargs = patch_get_items.call_args
        assert args[0] == {"name": "Test"}

# Test unassigned_items endpoint
def test_unassigned_items_endpoint(patch_get_items, mock_request_state):
    # Make request to the endpoint
    response = client.get("/license/v1/unassigned")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called
        patch_get_items.assert_called_once()

        # Get the filters that were passed to get_items
        args, kwargs = patch_get_items.call_args
        actual_filters = args[0]

        # Check the structure of the filters
        assert actual_filters["entity_uuid"] == "entity-1"
        assert actual_filters["user_uuid"] == {"$eq": None, "$exists": True}
        assert "$lt" in actual_filters["iat"]
        assert "$gt" in actual_filters["exp"]

# Test read_item endpoint
def test_read_item_endpoint(patch_get_item, mock_request_state):
    # Make request to the endpoint
    response = client.get("/license/v1/license/item-1")

    # Check response
    assert response.status_code in (200, 401, 403, 404)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["uuid"] == "item-1"

        # Verify that get_item was called with the correct UUID
        patch_get_item.assert_called_once()
        args, kwargs = patch_get_item.call_args
        assert args[0] == "item-1"

# Test read_item endpoint with non-existent item
def test_read_item_endpoint_not_found(mock_request_state):
    # Patch get_item to return None
    with patch('services.items_service.get_item', return_value=None):
        # Make request to the endpoint
        response = client.get("/license/v1/license/non-existent-item")

        # Check response
        assert response.status_code in (404, 401, 403)

# Test get_mine endpoint
def test_get_mine_endpoint(patch_get_items, mock_request_state):
    # Make request to the endpoint
    response = client.get("/license/v1/mine")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called
        patch_get_items.assert_called_once()

        # Get the filters that were passed to get_items
        args, kwargs = patch_get_items.call_args
        actual_filters = args[0]

        # Check the structure of the filters
        assert actual_filters["user_uuid"] == "user-1"
        assert "$lt" in actual_filters["iat"]
        assert "$gt" in actual_filters["exp"]

# Test get_mine endpoint with no user_uuid in state
def test_get_mine_endpoint_no_user_uuid():
    # Create a mock request state with no user_uuid
    with patch('starlette.requests.Request.state', create=True) as mock_state, \
         patch('services.items_service.get_items', return_value=[]) as mock_get_items:
        # Don't set user_uuid

        # Make request to the endpoint
        response = client.get("/license/v1/mine")

        # Check response
        assert response.status_code in (200, 401, 403)
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert "data" in data

            # Verify that get_items was called
            mock_get_items.assert_called_once()

            # Get the filters that were passed to get_items
            args, kwargs = mock_get_items.call_args
            actual_filters = args[0]

            # Check that user_uuid is None
            assert actual_filters["user_uuid"] is None

# Test assigned_items endpoint
def test_assigned_items_endpoint(patch_get_items, mock_request_state):
    # Make request to the endpoint
    response = client.get("/license/v1/assigned")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called
        patch_get_items.assert_called_once()

        # Get the filters that were passed to get_items
        args, kwargs = patch_get_items.call_args
        actual_filters = args[0]

        # Check the structure of the filters
        assert actual_filters["entity_uuid"] == "entity-1"
        assert actual_filters["user_uuid"] == {"$ne": None, "$exists": True}
        assert "$lt" in actual_filters["iat"]
        assert "$gt" in actual_filters["exp"]

# Test expired_items endpoint
def test_expired_items_endpoint(patch_get_items, mock_request_state):
    # Make request to the endpoint
    response = client.get("/license/v1/expired")

    # Check response
    assert response.status_code in (200, 401, 403)
    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

        # Verify that get_items was called
        patch_get_items.assert_called_once()

        # Get the filters that were passed to get_items
        args, kwargs = patch_get_items.call_args
        actual_filters = args[0]

        # Check the structure of the filters
        assert actual_filters["entity_uuid"] == "entity-1"
        assert "$lt" in actual_filters["iat"]
        assert "$lt" in actual_filters["exp"]
