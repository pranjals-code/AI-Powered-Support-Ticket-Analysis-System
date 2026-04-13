# AI Tracking System Backend

Backend service for the AI-driven support ticket platform. It exposes a FastAPI API for authentication, user management, and ticket operations, uses PostgreSQL for persistence, Alembic for schema migrations, and Celery + Redis for asynchronous ticket classification.

## What This Backend Does

- Registers users with role-based access control.
- Requires email verification with OTP before login.
- Issues JWT access tokens for authenticated requests.
- Lets users create support tickets with optional photo and file attachments.
- Uses an external AI service to classify ticket priority and category asynchronously.
- Assigns tickets to agents after AI classification.
- Supports ticket listing, filtering, pagination, status updates, and deletion rules.

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Celery
- Redis
- Pydantic Settings
- Uvicorn

## Project Structure

```text
backend/
├── app/
│   ├── auth/          # signup, login, OTP verification, password reset
│   ├── core/          # config, DB, security, email, Celery, AI client
│   ├── tasks/         # background jobs
│   ├── tickets/       # ticket models, schemas, routes
│   └── users/         # user models, schemas, routes
├── alembic/           # DB migrations
├── tests/             # unit and integration tests
├── Makefile           # common dev commands
├── requirements.txt   # Python dependencies
└── README.md
```

## Key Features

### Authentication

- `POST /auth/signup` creates an account and sends a verification OTP.
- `POST /auth/verify-email` verifies the account.
- `POST /auth/resend-verification` resends the OTP.
- `POST /auth/login` returns a bearer token.
- `POST /auth/forgot-password` sends a password reset OTP.
- `POST /auth/reset-password` resets the password with OTP.
- `POST /auth/logout` validates the current token and returns success.

### Users

- `GET /users/me` returns the current authenticated user.
- `PATCH /users/role` lets admins update another user's role.

### Tickets

- `POST /tickets` creates a ticket.
- `GET /tickets` returns paginated tickets with search and filters.
- `GET /tickets/{ticket_id}` returns a single ticket.
- `PATCH /tickets/{ticket_id}` updates text fields and attachments.
- `PATCH /tickets/{ticket_id}/status` updates status with RBAC checks.
- `DELETE /tickets/{ticket_id}` deletes a closed ticket for manager/admin roles only.

### Async AI Classification

After ticket creation, the backend queues a Celery task that calls the external AI service. If classification succeeds:

- `priority` is set
- `category` is set
- `status` becomes `ASSIGNED`
- an agent may be auto-assigned

If Redis or the AI service is unavailable, ticket creation still succeeds. Classification is skipped or delayed rather than blocking the API.

## Roles and Access Rules

Supported roles:

- `ADMIN`
- `MANAGER`
- `AGENT`
- `USER`

Ticket access behavior:

- `ADMIN` and `MANAGER` can view all tickets.
- `AGENT` can view only tickets assigned to them.
- `USER` can view only tickets they created.

Ticket mutation behavior:

- Only the ticket creator, admins, or managers can edit title and description.
- Only the ticket creator can add or remove attachments.
- `ADMIN` and `MANAGER` can update any ticket status.
- `AGENT` can update status only for tickets assigned to them.
- Only `ADMIN` and `MANAGER` can delete tickets.
- Tickets must be in `CLOSED` status before deletion.

## Ticket Model Notes

Each ticket stores:

- `title`
- `description`
- `status`
- `priority`
- `category`
- `created_by`
- `assigned_agent_id`
- `created_at`
- `updated_at`
- optional `photo` and `file` binary attachments

Attachment limits enforced by the API:

- photo: 6 MB
- file: 10 MB

## Prerequisites

Install or make available:

- Python 3.10+
- PostgreSQL
- Redis

Optional but recommended for full functionality:

- SMTP credentials for sending real OTP emails
- External AI service reachable at the configured `AI_SERVICE_URL`

## Environment Variables

The backend loads configuration from `backend/.env`.

Required settings:

```env
APP_NAME=AI Support Ticket System
ENVIRONMENT=development

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_tracking
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Optional settings:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=AI Support Ticket System

AI_SERVICE_URL=http://localhost:8001
AI_SERVICE_TIMEOUT_SECONDS=3.0

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Also supported outside the settings model:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Notes:

- If SMTP values are empty, OTP emails fall back to console output.
- Do not commit a real `.env` file with secrets.

## Local Setup

### 1. Create and activate a virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create `backend/.env` with the values shown above.

### 4. Start PostgreSQL and Redis

Make sure both services are reachable using the values in `.env`.

### 5. Run database migrations

```bash
make upgrade
```

### 6. Start the API

```bash
make run
```

The API will be available at:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

### 7. Start the Celery worker

In a second terminal:

```bash
cd backend
source venv/bin/activate
make celery
```

## Common Commands

```bash
make run          # FastAPI in reload mode
make run-prod     # FastAPI without reload
make celery       # Celery worker
make upgrade      # Apply Alembic migrations
make downgrade    # Roll back one migration
make migration msg="add new field"
make db-current   # Show current DB revision
make db-history   # Show migration history
make format       # Run black on app/
make lint         # Run pylama on app/
make clean        # Remove cache files
```

## API Usage

### Authentication flow

1. `POST /auth/signup`
2. Read OTP from email or console output
3. `POST /auth/verify-email`
4. `POST /auth/login`
5. Use `Authorization: Bearer <token>` for protected endpoints

### Example signup request

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "role": "USER"
  }'
```

### Example verify email request

```bash
curl -X POST http://localhost:8000/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "otp": "123456"
  }'
```

### Example login request

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Example create ticket request

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Authorization: Bearer <token>" \
  -F "title=Cannot access dashboard" \
  -F "description=The page keeps returning an error" \
  -F "photo=@/path/to/screenshot.png" \
  -F "file=@/path/to/log.txt"
```

### Example list tickets request

```bash
curl "http://localhost:8000/tickets?page=1&size=10&sort_by=created_at&order=desc&status=CREATED&search=dashboard" \
  -H "Authorization: Bearer <token>"
```

## Pagination and Filtering

`GET /tickets` supports:

- `page`
- `size`
- `sort_by` with supported fields: `created_at`, `updated_at`, `title`, `status`, `priority`
- `order`: `asc` or `desc`
- `status`
- `search`

## Database Migrations

Alembic is already configured. To create a new migration:

```bash
make migration msg="describe change"
```

Then apply it:

```bash
make upgrade
```

Existing migrations include:

- user table creation
- ticket table creation
- email verification and password reset fields
- ticket attachment fields and default user role updates

## Background AI Service Contract

The backend expects the AI classifier to expose:

- `POST {AI_SERVICE_URL}/predict`

Expected response shape:

```json
{
  "priority": "LOW",
  "category": "TECHNICAL",
  "team": "support",
  "confidence": 0.92
}
```

Valid enum values used by this backend:

- priority: `LOW`, `MEDIUM`, `HIGH`
- category: `BILLING`, `TECHNICAL`, `ACCOUNT`, `OTHER`

## Email Behavior

If SMTP is configured, verification and reset OTP emails are sent through the configured SMTP server.

If SMTP is not configured, the backend prints the email content to the console. That is useful for local development and testing.

## Testing

Run tests with:

```bash
pytest
```

Or:

```bash
pytest -q
```

Current test suite layout:

- `tests/unit/` for schema and core logic tests
- `tests/integration/` for API behavior tests

## Troubleshooting

### API fails to start

Check:

- `.env` exists in `backend/`
- PostgreSQL credentials are correct
- required Python dependencies are installed

### OTP emails are not being sent

If SMTP is not configured, the backend intentionally prints OTP content to the console instead of sending real mail.

### Tickets are created but never classified

Check:

- Redis is running
- Celery worker is running
- `AI_SERVICE_URL` is reachable

### CORS issues in local development

Set `CORS_ORIGINS` to a comma-separated list such as:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Test collection error with `TestClient`

In the current repository state, `pytest -q` fails during collection in `tests/integration/test_tickets_api.py` with:

```text
TypeError: Client.__init__() got an unexpected keyword argument 'app'
```

That points to a dependency mismatch around the testing client stack rather than a README issue.

## Development Notes

- App entrypoint: [app/main.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/main.py)
- Settings model: [app/core/config.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/core/config.py)
- Celery app: [app/core/celery_app.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/core/celery_app.py)
- Ticket routes: [app/tickets/router.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/tickets/router.py)
- Auth routes: [app/auth/router.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/auth/router.py)
- User routes: [app/users/router.py](/home/dev/AI-TRACKING-SYSTEM-TICKET/backend/app/users/router.py)

## License

Add your project license here if needed.
