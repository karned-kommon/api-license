# Authentication

The API License uses a dual-layer authentication system to ensure secure access to resources. Both authentication layers must be satisfied for a request to be processed.

## JWT Bearer Token Authentication

The first layer of authentication is JWT (JSON Web Token) Bearer token authentication.

### Token Requirements

- The token must be provided in the `Authorization` header with the `Bearer` prefix
- The token must be valid and not expired
- The token must be issued for the correct audience (API_NAME)
- The token must contain the necessary user information and roles

### Token Verification Process

1. The `TokenVerificationMiddleware` extracts the token from the `Authorization` header
2. The token is validated through Keycloak's introspection endpoint
3. Token information is cached in Redis for performance
4. User information from the token is stored in the request state for use in handlers

### Example Header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## License Header Authentication

The second layer of authentication is license verification.

### License Requirements

- A valid license UUID must be provided in the `licence` header
- The license must be associated with the authenticated user
- The license must be active (not expired)

### License Verification Process

1. The `LicenceVerificationMiddleware` extracts the license UUID from the `licence` header
2. The middleware verifies that the license exists in the user's list of licenses
3. The entity UUID associated with the license is extracted and stored in the request state
4. If the license is not found initially, the token cache is refreshed and checked again

### Example Header

```
licence: 123e4567-e89b-12d3-a456-426614174000
```

## Error Handling

Authentication errors will result in appropriate HTTP status codes:

- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Missing or invalid license

Error responses include a detail message explaining the issue:

```json
{
  "detail": "Token manquant ou invalide"
}
```

or

```json
{
  "detail": "Licence header missing"
}
```

## Unprotected Paths

Some paths may be configured as unprotected, allowing access without authentication. These paths are determined by the `is_unprotected_path` function in the `utils.path_util` module.

## Token Information

The token contains important user information that is used throughout the API:

- `user_uuid`: The UUID of the authenticated user
- `user_display_name`: The display name of the user
- `user_email`: The email address of the user
- `user_roles`: The roles assigned to the user
- `licenses`: The licenses associated with the user

This information is stored in the request state and can be accessed by handlers.