# Items Endpoints

The Items API provides endpoints for managing license items. These endpoints allow you to retrieve information about licenses, including unassigned licenses, specific licenses by UUID, and licenses assigned to the current user.

## Endpoints

### Get Unassigned Licenses

```
GET /unassigned
```

Retrieves a list of unassigned licenses for the current entity.

#### Authentication Required

- JWT Bearer Token
- License Header

#### Request Parameters

None

#### Response

Returns a list of unassigned license items.

**Status Code**: 200 OK

**Response Model**: `List[Item]`

**Example Response**:

```json
[
  {
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "type_uuid": "456e7890-e89b-12d3-a456-426614174000",
    "name": "Premium License",
    "auto_renew": true,
    "iat": 1609459200,
    "exp": 1640995200,
    "user_uuid": null,
    "entity_uuid": "789e0123-e89b-12d3-a456-426614174000",
    "credential_uuid": "012e3456-e89b-12d3-a456-426614174000",
    "historical": [],
    "sales": []
  }
]
```

#### Implementation Details

This endpoint filters licenses based on the following criteria:
- Belongs to the current entity
- Has no assigned user (user_uuid is null)
- Is currently active (current time is between iat and exp)

### Get License by UUID

```
GET /license/{uuid}
```

Retrieves a specific license by its UUID.

#### Authentication Required

- JWT Bearer Token
- License Header

#### Path Parameters

- `uuid` (string, required): The UUID of the license to retrieve

#### Response

Returns the license item with the specified UUID.

**Status Code**: 200 OK

**Response Model**: `Item`

**Example Response**:

```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "type_uuid": "456e7890-e89b-12d3-a456-426614174000",
  "name": "Premium License",
  "auto_renew": true,
  "iat": 1609459200,
  "exp": 1640995200,
  "user_uuid": "abc12345-e89b-12d3-a456-426614174000",
  "entity_uuid": "789e0123-e89b-12d3-a456-426614174000",
  "credential_uuid": "012e3456-e89b-12d3-a456-426614174000",
  "historical": [],
  "sales": []
}
```

**Error Responses**:

- 404 Not Found: If the license with the specified UUID does not exist

### Get My Licenses

```
GET /mine
```

Retrieves licenses assigned to the current user.

#### Authentication Required

- JWT Bearer Token
- License Header

#### Request Parameters

None

#### Response

Returns a list of license items assigned to the current user.

**Status Code**: 200 OK

**Response Model**: `List[Item]`

**Example Response**:

```json
[
  {
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "type_uuid": "456e7890-e89b-12d3-a456-426614174000",
    "name": "Premium License",
    "auto_renew": true,
    "iat": 1609459200,
    "exp": 1640995200,
    "user_uuid": "abc12345-e89b-12d3-a456-426614174000",
    "entity_uuid": "789e0123-e89b-12d3-a456-426614174000",
    "credential_uuid": "012e3456-e89b-12d3-a456-426614174000",
    "historical": [],
    "sales": []
  }
]
```

#### Implementation Details

This endpoint filters licenses based on the following criteria:
- Belongs to the current entity
- Is assigned to the current user
- Is currently active (current time is between iat and exp)