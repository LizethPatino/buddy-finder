# API

> **Planned API.** These endpoints are being built now; this is the contract we build against.

All endpoints live under `/api` and take and return JSON. When the app is running, the interactive documentation (Swagger) is at `/api/docs`.

**Authentication:** protected endpoints need the header `Authorization: Bearer <token>`. You get the token from `POST /api/auth/login`. It expires after 1 hour.

- `401 Unauthorized` — no token, or the token is invalid or expired
- `403 Forbidden` — the token is valid, but your role or ownership doesn't allow this

> This is our contract. If you need to change a path, a field or a response code, update this file in the same pull request and tell the team.

## Endpoints

| Method and path | Who | Success | Errors |
| --- | --- | --- | --- |
| `GET /api/health` | Public | 200, includes the pod name | — |
| `POST /api/auth/register` | Public | 201 user | 400 invalid · 409 email taken |
| `POST /api/auth/login` | Public | 200 token + user | 400 · 401 wrong credentials · 429 too many attempts |
| `GET /api/me` | Logged in | 200 | 401 |
| `GET /api/interests` | Public | 200 fixed list | — |
| `GET /api/events?from=&to=&page=&per_page=` | Public | 200 page of events | 400 bad filter |
| `GET /api/events/{id}` | Public | 200 event with weather | 404 |
| `POST /api/events` | Staff | 201 event | 400 · 401 · 403 |
| `PUT /api/events/{id}` | Staff | 200 | 400 · 401 · 403 · 404 |
| `DELETE /api/events/{id}` | Staff | 204 | 401 · 403 · 404 |
| `POST /api/webhooks/native/ticket-claimed` | Native (shared secret header) | 201 ticket | 401 bad secret · 404 unknown user or event · 409 already claimed |
| `GET /api/me/tickets` | Logged in | 200 | 401 |
| `POST /api/events/{id}/optin` | Ticket holder | 201 opt-in + group | 400 bad interests · 401 · 403 no ticket · 404 · 409 already in |
| `PATCH /api/events/{id}/optin` | Opted-in student | 200 | 400 · 401 · 404 |
| `DELETE /api/events/{id}/optin` | Opted-in student | 204 (leaves the group) | 401 · 404 |
| `GET /api/me/groups` | Logged in | 200 | 401 |
| `GET /api/groups/{id}` | Group member | 200 members + meeting point | 401 · 403 not a member · 404 |
| `PATCH /api/groups/{id}/membership` | Group member | 200 accepted or declined | 400 · 401 · 403 · 404 |
| `GET /api/admin/stats` | Staff | 200 totals and per-event counts | 401 · 403 |
| `GET /api/admin/users` | Staff | 200 | 401 · 403 |
| `DELETE /api/admin/users/{id}` | Staff | 204 | 401 · 403 · 404 |

Each event also returns `looking_count` (students still looking for a group) and `native_url` (where to get a ticket).

## Error format

Every error, from every endpoint, has the same shape:

```json
{ "error": "no_ticket", "message": "You need a ticket for this event to join Buddy Finder." }
```

## Example: opting in

```http
POST /api/events/12/optin
Authorization: Bearer <token>
Content-Type: application/json

{ "interests": ["music", "first_year"] }
```

```json
201 Created
{
  "optin_id": 87,
  "event_id": 12,
  "interests": ["music", "first_year"],
  "group": {
    "id": 31,
    "size": 3,
    "meeting_point": "Hub entrance, 20 min before",
    "members": [
      { "first_name": "Sara", "avatar_url": "https://api.dicebear.com/...", "interests": ["music", "sport"] }
    ]
  }
}
```
