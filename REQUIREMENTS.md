# Pagila API Reflection Learning Roadmap

Use this document to track progress while building the API. Check an item by
changing `[ ]` to `[x]`. Uncheck it by changing `[x]` back to `[ ]`.

## Current Goal

Connect FastAPI to the existing Pagila PostgreSQL container, reflect its
schema with SQLAlchemy, and build a read-only actor endpoint:

```http
GET /actors/{actor_id}
```

## Phase 1: Application Foundation

- [x] Move application settings from `src/main.py` to `src/config.py`
- [x] Add an `app_name` setting
- [x] Add a `debug` setting
- [x] Add a `database_url` setting
- [x] Load settings from a `.env` file
- [ ] Add a safe `.env.example` without real credentials
- [x] Make sure `.env` is ignored by Git
- [ ] Cache and reuse one settings object
- [ ] Keep `src/main.py` focused on creating the FastAPI application
- [x] Add `GET /health`
- [x] Run the application locally
- [ ] Open and inspect `/docs`

### Phase 1 checkpoint

- [x] The application starts without errors
- [ ] `GET /health` returns HTTP 200
- [ ] Swagger UI loads at `/docs`

## Phase 2: Database Foundation

- [x] Confirm the PostgreSQL container is running
- [ ] Record the container name
- [x] Confirm the database name and PostgreSQL user
- [x] Confirm the PostgreSQL port is published to the host
- [x] Connect to the database with `psql` or another database client
- [x] List the existing schemas and tables
- [x] Confirm the `actor` table exists
- [x] Inspect the columns and primary key of the `actor` table
- [x] Add a PostgreSQL driver such as `psycopg[binary]`
- [x] Update `src/db/engine.py`
- [x] Create the engine using `settings.database_url`
- [x] Create a configured `sessionmaker`
- [x] Create `src/db/dependencies.py`
- [ ] Add a `get_db()` FastAPI dependency
- [x] Ensure every database session is closed after a request
- [x] Remove the hard-coded database URL
- [x] Verify the application can connect to Pagila
- [x] Do not call `create_all()` against the existing database

### Phase 2 checkpoint

- [ ] A simple `SELECT 1` succeeds
- [ ] A failed database connection produces a useful error
- [x] No database credentials are committed to Git
- [x] The application connects through the Docker-published host port
- [x] Starting the API does not create, alter, or delete any table

## Phase 3: Reflect the Existing Database

Reflection reads table metadata from the running database. `automap_base()`
can then generate mapped SQLAlchemy classes from that reflected metadata.

- [x] Create `src/models/`
- [x] Create `src/models/__init__.py`
- [x] Keep the reflection setup in `src/db/mirroring.py`
- [x] Create one `automap_base()`
- [x] Call `Base.prepare(autoload_with=engine)` once during startup/import
- [ ] Limit reflection to the intended PostgreSQL schema if necessary
- [ ] Inspect `Base.classes.keys()` to see the reflected mapped classes
- [x] Retrieve the generated `Actor` class from `Base.classes`
- [x] Confirm the reflected class exposes `actor_id`
- [x] Confirm the reflected class exposes `first_name`
- [x] Confirm the reflected class exposes `last_name`
- [ ] Confirm the reflected class exposes `last_update`
- [x] Query actors directly through a SQLAlchemy session
- [ ] Retrieve one actor by ID
- [ ] Document which tables were skipped because they lack a primary key
- [x] Avoid reflecting the database separately on every request

### Phase 3 checkpoint

- [x] SQLAlchemy discovers the existing tables without creating them
- [x] The reflected `Actor` class matches the existing Pagila table
- [x] SQLAlchemy can return a list of actors
- [ ] SQLAlchemy returns `None` for an unknown actor ID
- [ ] Restarting the API does not change the database schema

### Optional later exercise: explicit models

After reflection works, explicitly declaring a few important models is useful
for learning type-safe ORM mappings and controlling relationship names.

- [ ] Compare an explicit `Actor` model with the reflected `Actor` class
- [ ] Decide whether the project should use reflection, explicit models, or a hybrid
- [ ] Consider using `sqlacodegen` to generate a starting point for explicit models
- [ ] Review generated model code before adding it to the application

## Phase 4: Pydantic API Schemas

Use an explicit Pydantic response schema as the public API contract. The
SQLAlchemy class may be reflected automatically, but the API should
intentionally choose which database fields it exposes.

- [ ] Create `src/schemas/`
- [ ] Create `src/schemas/__init__.py`
- [ ] Create `src/schemas/actor.py`
- [ ] Create an `ActorResponse` schema
- [ ] Add `actor_id: int`
- [ ] Add `first_name: str`
- [ ] Add `last_name: str`
- [ ] Add `last_update: datetime`
- [ ] Add `ConfigDict(from_attributes=True)`
- [ ] Use appropriate types for every actor field
- [ ] Convert one reflected actor with `ActorResponse.model_validate(actor)`
- [ ] Convert multiple actors with a `list[ActorResponse]` response model
- [ ] Add `response_model=ActorResponse` to the single-actor route
- [ ] Add `response_model=list[ActorResponse]` to the actor-list route
- [ ] Let FastAPI convert returned reflected actors automatically
- [ ] Confirm an SQLAlchemy `Actor` can be serialized after its session closes
- [ ] Confirm only fields declared in `ActorResponse` are returned

### Phase 4 checkpoint

- [ ] The response schema produces valid JSON
- [ ] Internal SQLAlchemy state is not exposed in the response
- [ ] Swagger UI documents the actor response fields and their types
- [ ] Changing the reflected table does not silently expose a new API field

### Optional exercise: generate Pydantic schemas dynamically

Pydantic's `create_model()` and SQLAlchemy's `inspect()` can generate a schema
from reflected columns. Treat this as a learning exercise rather than the
default API design, because database changes could silently change the API.

- [ ] Use `inspect(Actor).columns` to list the reflected columns
- [ ] Read each column's Python type using `column.type.python_type`
- [ ] Represent nullable columns with `type | None`
- [ ] Generate an experimental schema with `pydantic.create_model()`
- [ ] Configure the generated schema with `from_attributes=True`
- [ ] Compare the generated schema with the explicit `ActorResponse`
- [ ] Test a PostgreSQL-specific type that lacks a simple `python_type`
- [ ] Confirm relationships are not accidentally serialized recursively
- [ ] Keep the explicit schema as the production response model

## Phase 5: Actor Service

- [ ] Create `src/services/`
- [ ] Create `src/services/__init__.py`
- [ ] Create `src/services/actor_service.py`
- [ ] Implement `get_actor(db, actor_id)`
- [ ] Implement `list_actors(db, limit, offset)`
- [ ] Add a reasonable maximum page size
- [ ] Keep SQLAlchemy queries out of route functions

### Phase 5 checkpoint

- [ ] The service retrieves an existing actor
- [ ] The service handles a missing actor
- [ ] The list service supports pagination

## Phase 6: Actor Routes

- [ ] Create `src/routes/`
- [ ] Create `src/routes/__init__.py`
- [ ] Create `src/routes/actors.py`
- [ ] Create an `APIRouter`
- [ ] Add `GET /actors`
- [ ] Add `GET /actors/{actor_id}`
- [ ] Inject the database session with `Depends`
- [ ] Declare response models
- [ ] Return HTTP 404 when an actor does not exist
- [ ] Register the actor router in `src/main.py`

### Phase 6 checkpoint

- [ ] `GET /actors` returns actors
- [ ] `GET /actors?limit=5&offset=0` returns at most five actors
- [ ] `GET /actors/1` returns one actor
- [ ] An unknown actor ID returns HTTP 404
- [ ] Both endpoints appear correctly in `/docs`

## Phase 7: Automated Tests

- [ ] Create `tests/`
- [ ] Add a test client fixture
- [ ] Add a test database strategy
- [ ] Override the `get_db()` dependency in tests
- [ ] Test `GET /health`
- [ ] Test listing actors
- [ ] Test retrieving one actor
- [ ] Test retrieving an unknown actor
- [ ] Test invalid pagination values
- [ ] Run the complete test suite successfully

## Phase 8: Films and Relationships

Only begin this phase after the actor feature is working.

- [ ] Locate the reflected `film` class
- [ ] Create film response schemas
- [ ] Add `GET /films`
- [ ] Add `GET /films/{film_id}`
- [ ] Add film title search
- [ ] Inspect the reflected `film_actor` association table
- [ ] Inspect relationships generated by automap
- [ ] Rename or customize unclear automap relationships if necessary
- [ ] Return actors for a film
- [ ] Return films for an actor
- [ ] Map categories
- [ ] Filter films by category

## Phase 9: Optional Write Operations

- [ ] Create a disposable copy of the Pagila database for write practice
- [ ] Never test writes against the only copy of important data
- [ ] Create request schemas for new records
- [ ] Add an actor creation service
- [ ] Add `POST /actors`
- [ ] Add actor update support
- [ ] Add `PATCH /actors/{actor_id}`
- [ ] Add actor deletion support
- [ ] Add `DELETE /actors/{actor_id}`
- [ ] Use transactions correctly
- [ ] Roll back failed transactions
- [ ] Return appropriate HTTP status codes

## Phase 10: Schema Ownership and Migrations

This API initially mirrors a database owned elsewhere. Reflection does not
require Alembic, and the API should not manage that existing schema.

- [ ] Document that the API is not initially the schema owner
- [ ] Keep Alembic disabled for the reflected schema
- [ ] Do not run `alembic revision --autogenerate` against the existing database
- [ ] Do not run `alembic upgrade` against the existing database
- [ ] Learn what Alembic migrations do
- [ ] If migration practice is desired, clone the database first
- [ ] Inspect any generated migration before applying it to the clone
- [ ] Apply and roll back a harmless migration only on the disposable clone

## Phase 11: Authentication

- [ ] Move token schemas out of `src/main.py`
- [ ] Keep password hashing utilities isolated
- [ ] Create a user model and schemas
- [ ] Verify hashed passwords
- [ ] Create JWT access tokens
- [ ] Add a login endpoint
- [ ] Add a current-user dependency
- [ ] Protect a route
- [ ] Test valid, invalid, and expired tokens

## Phase 12: Production Readiness

- [ ] Add structured logging
- [ ] Add centralized exception handling
- [ ] Configure CORS intentionally
- [ ] Add Docker Compose for the API only if it should join the database network
- [ ] Document the difference between connecting from the host and another container
- [ ] Add database connection pool settings
- [ ] Add linting and formatting
- [ ] Add static type checking
- [ ] Add continuous integration
- [ ] Document local setup in `README.md`
- [ ] Document all environment variables

## Existing Code Cleanup

- [x] Replace `Session = sessionmaker(get_engine)` with a sessionmaker bound to an engine
- [x] Replace the hard-coded `psycopg2` connection URL
- [x] Ensure the selected PostgreSQL driver is listed in `pyproject.toml`
- [x] Change `access_time_exp_in_mins = int` to a proper annotated setting
- [ ] Separate settings, token schemas, user schemas, and item schemas from `main.py`
- [x] Verify the FastAPI entry point works with the `src` package layout
- [x] Replace the incomplete code in `src/db/mirroring.py` with one reflection setup
- [x] Ensure reflection uses the configured engine
- [x] Ensure reflection happens once rather than once per request
- [ ] Remove unused imports and experiments after their concepts are understood

## Learning Notes

Record short explanations in your own words:

- [ ] Explain what the FastAPI application object does
- [ ] Explain the difference between a route and a service
- [ ] Explain the difference between a SQLAlchemy model and a Pydantic schema
- [ ] Explain what the SQLAlchemy engine does
- [ ] Explain what a database session does
- [ ] Explain the difference between reflection and an explicit ORM model
- [ ] Explain what `automap_base()` does
- [ ] Explain why reflected tables generally need primary keys for ORM mapping
- [ ] Explain why reflection does not require `create_all()`
- [ ] Explain how host and container database addresses differ
- [ ] Explain why a request should not share a global mutable session
- [ ] Explain what FastAPI dependency injection does
- [ ] Explain why `.env` must not be committed

## Progress Log

Add a new entry whenever you finish a meaningful piece of work.

| Date | Completed | What I learned | Next step |
| --- | --- | --- | --- |
| YYYY-MM-DD | Example: Added `/health` | Example: Routes map URLs to functions | Configure settings |
