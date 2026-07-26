# Pagila API

A learning project built with FastAPI, SQLAlchemy, Pydantic, and PostgreSQL.
The API connects to an existing Pagila database running locally in Docker and
uses SQLAlchemy reflection to map its tables.

## Current features

- FastAPI application with interactive API documentation
- Environment-based configuration
- Connection to a PostgreSQL database running in Docker
- SQLAlchemy reflection with `automap_base()`
- Read-only actor listing
- Pydantic response validation
- Ruff linting and formatting

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- Docker
- A running PostgreSQL container containing the Pagila database

The PostgreSQL port must be published to the host if the API is run outside
Docker.

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd pagila_api
```

Install the project dependencies:

```bash
uv sync
```

## Configuration

Copy the environment template:

```bash
cp .env.template .env
```

Add your local values to `.env`:

```env
SECRET_KEY=replace-me
ALGORITHM=HS256
ACCESS_TIME_EXPIRATION_IN_MINS=30

DEBUG=true
APP_NAME=Pagila API

DATABASE_USER=postgres
DATABASE_PASSWORD=replace-me
DATABASE_URL=localhost
DATABASE_PORT=5432
DATABASE_DB=pagila
```

Never commit `.env`. It may contain database credentials and application
secrets.

## Running the API

Start the development server:

```bash
uv run fastapi dev
```

The application is available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Current endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Basic welcome response |
| `GET` | `/health` | Application health check |
| `GET` | `/list_actors` | Returns the first actors from Pagila |

Example:

```bash
curl http://127.0.0.1:8000/list_actors
```

## Code quality

Check the code with Ruff:

```bash
uv run ruff check .
```

Apply safe lint fixes and format the code:

```bash
uv run ruff check . --fix
uv run ruff format .
```

Verify formatting without changing files:

```bash
uv run ruff format . --check
```

## Project structure

```text
src/
├── config.py          # Environment-based settings
├── main.py            # FastAPI application and current routes
├── db/
│   ├── engine.py      # SQLAlchemy engine and sessionmaker
│   ├── dependencies.py
│   └── mirroring.py   # Existing database reflection
├── models/
│   └── actor.py       # Reflected database classes
└── sign_up/
    └── pass_utils.py  # Password hashing helpers
```

## Development roadmap

Progress is tracked in [REQUIREMENTS.md](REQUIREMENTS.md). The next planned
steps include database-session dependency injection, separate Pydantic
schemas, services, routers, pagination, and automated tests.

## Database safety

This project currently reflects an existing database. Reflection reads the
schema; it does not require `Base.metadata.create_all()`. Avoid running schema
migrations or write operations against important data until a disposable
development database is available.
