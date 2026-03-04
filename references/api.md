# Memos API Reference

Based on: https://usememos.com/docs/api

## Base URL

```
https://your-memos-instance.com/api/v1
```

## Authentication

Bearer token in Authorization header:
```
Authorization: Bearer <YOUR_ACCESS_TOKEN>
```

## Endpoints

### CreateMemo

**URL:** `POST /api/v1/memos`

**Request Body:**
```json
{
  "content": "string (required) - The memo content",
  "visibility": "string (optional) - PRIVATE | PROTECTED | PUBLIC, default: PRIVATE",
  "tags": ["array", "of", "strings"]
}
```

**Response:**
```json
{
  "name": "memos/123",
  "content": "Note content",
  "visibility": "PRIVATE",
  "tags": [],
  "createTime": "2024-01-01T00:00:00Z",
  "updateTime": "2024-01-01T00:00:00Z"
}
```

### ListMemos

**URL:** `GET /api/v1/memos?pageSize=10&filter=...`

**Query Parameters:**
- `pageSize`: Number of memos to return
- `filter`: Filter expression (Google AIP-160 format)
  - `content.contains('keyword')` - Search in content

**Response:**
```json
{
  "memos": [
    {
      "name": "memos/xxx",
      "content": "...",
      "tags": [],
      "createTime": "...",
      "pinned": false
    }
  ]
}
```

### GetMemo

**URL:** `GET /api/v1/memos/{name}`

**Response:** Full memo object with all fields

### DeleteMemo

**URL:** `DELETE /api/v1/memos/{name}`

**Response:** Empty object `{}`

## Environment Variables Required

- `MEMOS_API_URL` - Base URL of Memos instance (e.g., `https://memos.example.com`)
- `MEMOS_API_TOKEN` - API access token from Memos settings

## Getting API Token

1. Go to your Memos instance
2. Open Settings → API
3. Generate a new access token
4. Copy the token for use with this skill
