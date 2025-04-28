# Item Model

The `Item` model represents a license in the system. It contains all the information related to a license, including its type, validity period, assignment status, and related data.

## Schema

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | The unique identifier for the license |
| type_uuid | string | The unique identifier for the license type |
| name | string | The name of the license |
| auto_renew | boolean | Whether the license automatically renews (default: true) |
| iat | integer | The timestamp when the license was issued (issued at) |
| exp | integer | The timestamp when the license expires |
| user_uuid | string | The UUID of the user the license is assigned to (null if unassigned) |
| entity_uuid | string | The UUID of the entity that owns the license |
| credential_uuid | string | The UUID of the credential associated with the license |
| historical | array | A list of historical events related to the license |
| sales | array | A list of sales data related to the license |

## Example

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
  "historical": [
    {
      "timestamp": 1609459200,
      "action": "created",
      "user_uuid": "def67890-e89b-12d3-a456-426614174000"
    },
    {
      "timestamp": 1612137600,
      "action": "assigned",
      "user_uuid": "abc12345-e89b-12d3-a456-426614174000"
    }
  ],
  "sales": [
    {
      "timestamp": 1609459200,
      "amount": 99.99,
      "currency": "USD",
      "transaction_id": "txn_123456789"
    }
  ]
}
```

## Related Models

### HistoricalModel

The `HistoricalModel` represents an event in the license's history.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | integer | The timestamp when the event occurred |
| action | string | The action that was performed (e.g., "created", "assigned", "unassigned") |
| user_uuid | string | The UUID of the user who performed the action |

### SalesModel

The `SalesModel` represents sales data related to the license.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | integer | The timestamp when the sale occurred |
| amount | number | The amount of the sale |
| currency | string | The currency of the sale |
| transaction_id | string | The unique identifier for the transaction |

## Usage in the API

The `Item` model is used in the following endpoints:

- `GET /unassigned`: Returns a list of `Item` objects representing unassigned licenses
- `GET /license/{uuid}`: Returns a single `Item` object representing the specified license
- `GET /mine`: Returns a list of `Item` objects representing licenses assigned to the current user

## Implementation

The `Item` model is implemented using Pydantic's `BaseModel` class, which provides validation, serialization, and deserialization capabilities.

```python
class Item(BaseModel):
    uuid: str = Field(..., description="License : UUID")
    type_uuid: str = Field(..., description="Type : UUID")
    name: str = Field(..., description="License name")
    auto_renew: bool = Field(default=True, description="Auto renew")
    iat: int = Field(..., description="license iat")
    exp: int = Field(..., description="License exp")
    user_uuid: str = Field(..., description="User UUID")
    entity_uuid: str  = Field(..., description="Entity UUID")
    credential_uuid: str = Field(..., description="Credential UUID")
    historical: List[HistoricalModel] = Field(..., description="License assignment historical data")
    sales: List[SalesModel] = Field(..., description="License sales data")
```