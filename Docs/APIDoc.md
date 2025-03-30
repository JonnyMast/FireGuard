
# Todo write about how to use the FireGuard API

# POST REQUESTS

# Authentication API Documentation

The Authentication API provides endpoints for obtaining JWT tokens for client and user access.

## Endpoints

### Client Token Endpoint
`POST /auth/token/client`

Authenticates an API client and returns a JWT token for accessing protected endpoints.

### User Token Endpoint
`POST /auth/token/user`

Authenticates a user and returns a JWT token for accessing user-specific endpoints.

## Request Bodies

### ClientCredentials
- `client_id`: string - The API client identifier
- `client_secret`: string - The API client secret key

### UserCredentials
- `username`: string - User's username
- `password`: string - User's password

## Responses
Successful authentication returns a JSON object with:
- `access_token`: The JWT token
- `token_type`: The token type (always "bearer")

## How to Use

### Using cURL

**For Client Authentication:**