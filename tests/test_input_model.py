import pytest
from pydantic import ValidationError

from models.input import LicenseUUID

def test_license_uuid_valid():
    # Test with valid UUID
    license_uuid = LicenseUUID(uuid="123e4567-e89b-12d3-a456-426614174000")
    assert license_uuid.uuid == "123e4567-e89b-12d3-a456-426614174000"
    
    # Test with valid string (not necessarily a UUID format)
    license_uuid = LicenseUUID(uuid="test-license-id")
    assert license_uuid.uuid == "test-license-id"
    
    # Test with model_dump() method
    license_uuid = LicenseUUID(uuid="test-license-id")
    data = license_uuid.model_dump()
    assert data == {"uuid": "test-license-id"}

def test_license_uuid_invalid():
    # Test with missing uuid
    with pytest.raises(ValidationError):
        LicenseUUID()
    
    # Test with None value
    with pytest.raises(ValidationError):
        LicenseUUID(uuid=None)
    
    # Test with wrong type
    with pytest.raises(ValidationError):
        LicenseUUID(uuid=123)  # Should be string, not int