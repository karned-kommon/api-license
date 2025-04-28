# API Overview

The API License is a RESTful API that provides license management capabilities. This page gives an overview of the API structure, endpoints, and usage patterns.

## API Base URL

The API is accessible at the base URL of your deployment. For example:

```
https://your-domain.com/api/
```

## API Versioning

The current API version is 1.0.0. The version is specified in the OpenAPI schema.

## Authentication

All API endpoints are protected by two levels of authentication:

1. **JWT Bearer Token**: Must be provided in the `Authorization` header
2. **License Header**: Must be provided in the `licence` header

For more details, see the [Authentication](authentication.md) section.

## Common Response Formats

### Success Response

A successful response will typically include:

```json
{
  "data": [
    // Response data here
  ]
}
```

### Error Response

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Valid authentication but insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Available Endpoints

The API provides the following main endpoints:

### License Management

- `GET /unassigned`: Get unassigned licenses
- `GET /license/{uuid}`: Get a specific license by UUID
- `GET /mine`: Get licenses assigned to the current user

For detailed information about each endpoint, see the [Endpoints](endpoints/items.md) section.

## Request Examples

### Get Unassigned Licenses

```bash
curl -X GET "https://your-domain.com/api/unassigned" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "licence: YOUR_LICENSE_UUID"
```

### Get License by UUID

```bash
curl -X GET "https://your-domain.com/api/license/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "licence: YOUR_LICENSE_UUID"
```

### Get My Licenses

```bash
curl -X GET "https://your-domain.com/api/mine" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "licence: YOUR_LICENSE_UUID"
```