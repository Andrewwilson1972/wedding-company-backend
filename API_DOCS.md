# API Documentation

This document provides detailed documentation for all available API routes in the Wedding Backend application.

## Base URL

The API is served at `http://localhost:8000` (assuming default Uvicorn configuration).

## Authentication

Some endpoints require JWT authentication. Include the token in the `Authorization` header as `Bearer <token>`.

---

## Health Check

### GET /

Check the health status of the service.

**Tags:** health

**Response:**

- **200 OK**
  ```json
  {
    "status": "ok",
    "service": "Wedding Backend"
  }
  ```

**Example Request:**

```
GET http://localhost:8000/
```

**Example Response:**

```json
{
  "status": "ok",
  "service": "Wedding Backend"
}
```

---

## Authentication

### POST /admin/login

Authenticate an admin user and obtain a JWT access token.

**Tags:** auth

**Request Body:**

```json
{
  "email": "string (email format)",
  "password": "string"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "admin": {
      "email": "string",
      "organization_name": "string"
    }
  }
  ```
- **401 Unauthorized** - Invalid email or password
  ```json
  {
    "detail": "Invalid email or password"
  }
  ```

**Example Request:**

```
POST http://localhost:8000/admin/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "securepassword"
}
```

**Example Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "admin": {
    "email": "admin@example.com",
    "organization_name": "Example Org"
  }
}
```

---

## Organization Management

### POST /org/create

Create a new organization along with its admin user.

**Tags:** organization

**Request Body:**

```json
{
  "organization_name": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**

- **201 Created**
  ```json
  {
    "message": "Organization created successfully",
    "organization": {
      "organization_name": "string",
      "collection_name": "string",
      "admin_email": "string",
      "admin_id": "string"
    },
    "admin": {
      "email": "string"
    }
  }
  ```
- **400 Bad Request** - Organization already exists or other error
  ```json
  {
    "detail": "Organization already exists"
  }
  ```

**Example Request:**

```
POST http://localhost:8000/org/create
Content-Type: application/json

{
  "organization_name": "My Wedding Org",
  "email": "admin@mywedding.com",
  "password": "mypassword123"
}
```

**Example Response:**

```json
{
  "message": "Organization created successfully",
  "organization": {
    "organization_name": "My Wedding Org",
    "collection_name": "org_myweddingorg",
    "admin_email": "admin@mywedding.com",
    "admin_id": "507f1f77bcf86cd799439011"
  },
  "admin": {
    "email": "admin@mywedding.com"
  }
}
```

### GET /org/get

Retrieve organization details by name.

**Tags:** organization

**Query Parameters:**

- `organization_name` (string, required): The name of the organization.

**Response:**

- **200 OK**
  ```json
  {
    "organization_name": "string",
    "collection_name": "string",
    "admin_email": "string",
    "admin_id": "string"
  }
  ```
- **404 Not Found** - Organization not found
  ```json
  {
    "detail": "Organization not found"
  }
  ```

**Example Request:**

```
GET http://localhost:8000/org/get?organization_name=My%20Wedding%20Org
```

**Example Response:**

```json
{
  "organization_name": "My Wedding Org",
  "collection_name": "org_myweddingorg",
  "admin_email": "admin@mywedding.com",
  "admin_id": "507f1f77bcf86cd799439011"
}
```

### PUT /org/update

Update an organization's admin details. Requires authentication by the organization's admin.

**Tags:** organization

**Headers:**

- `Authorization: Bearer <jwt_token>`

**Request Body:**

```json
{
  "organization_name": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Organization updated successfully"
  }
  ```
- **400 Bad Request** - Organization not found or update error
  ```json
  {
    "detail": "Organization not found"
  }
  ```
- **401 Unauthorized** - Missing or invalid token
  ```json
  {
    "detail": "Missing or invalid token"
  }
  ```
- **403 Forbidden** - Not authorized to update this organization
  ```json
  {
    "detail": "You are not authorized to update this organization."
  }
  ```

**Example Request:**

```
PUT http://localhost:8000/org/update
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "organization_name": "My Wedding Org",
  "email": "newadmin@mywedding.com",
  "password": "newpassword123"
}
```

**Example Response:**

```json
{
  "message": "Organization updated successfully"
}
```

### DELETE /org/delete

Delete an organization and its associated data. Requires authentication by the organization's admin.

**Tags:** organization

**Headers:**

- `Authorization: Bearer <jwt_token>`

**Request Body:**

```json
{
  "organization_name": "string"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Organization deleted successfully"
  }
  ```
- **400 Bad Request** - Organization not found or unauthorized
  ```json
  {
    "detail": "Organization not found"
  }
  ```
- **401 Unauthorized** - Missing or invalid token
  ```json
  {
    "detail": "Missing or invalid token"
  }
  ```

**Example Request:**

```
DELETE http://localhost:8000/org/delete
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "organization_name": "My Wedding Org"
}
```

**Example Response:**

```json
{
  "message": "Organization deleted successfully"
}
```
