import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from fastapi import HTTPException

from services.items_service import get_item, get_items

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
    repo.list_items.return_value = mock_items
    repo.get_item.return_value = mock_items[0]
    return repo

# Test get_items function
def test_get_items(mock_repo):
    # Test with empty filters
    items = get_items({}, mock_repo)
    assert items == mock_items
    mock_repo.list_items.assert_called_once_with({})

    # Reset mock
    mock_repo.reset_mock()

    # Test with filters
    filters = {"name": "Item 1"}
    items = get_items(filters, mock_repo)
    assert items == mock_items
    mock_repo.list_items.assert_called_once_with(filters)

# Test get_items function with name filter
def test_get_items_with_name_filter(mock_repo):
    # Test with name filter
    filters = {"name": "Item 1"}
    items = get_items(filters, mock_repo)
    assert items == mock_items

    # Verify that the repository's list_items method was called with the correct filter
    mock_repo.list_items.assert_called_once_with(filters)

# Test get_item function
def test_get_item(mock_repo):
    # Test with existing item
    item = get_item("item-1", mock_repo)
    assert item == mock_items[0]
    mock_repo.get_item.assert_called_once_with("item-1")

    # Reset mock
    mock_repo.reset_mock()

    # Test with non-existing item
    mock_repo.get_item.return_value = None

    # This should raise an HTTPException with status_code 404
    with pytest.raises(HTTPException) as excinfo:
        item = get_item("non-existing", mock_repo)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Item not found"
    mock_repo.get_item.assert_called_once_with("non-existing")
