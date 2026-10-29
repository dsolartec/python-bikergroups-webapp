# AGENTS.md — Project Guidelines & Architecture Reference

This document defines the architectural patterns, business rules, coding conventions, and testing standards for `python-bikergroups-webapp`. Any AI agent or developer contributing to this repository must follow these guidelines.

---

## 1. Tech Stack & Environment

- **Language**: Python `>=3.14`
- **Dependency Management**: Poetry (`>=2.4.1`)
- **Web Framework**: Flask (`>=3.1.3`) with Jinja2 templates
- **ORM & Database**: SQLAlchemy 2.0 (`Mapped`, `mapped_column`, `DeclarativeBase`) + PostgreSQL (`>=18`, `psycopg2-binary`)
- **Validation & Domain Models**: Pydantic v2 (`BaseModel`)
- **Dependency Injection**: `dependency-injector` (`Container`)
- **Password Hashing**: `argon2-cffi` (`PasswordHasher`)
- **Styling**: SCSS (`app/static/scss/`) compiled to `app/static/css/main.css`
- **Testing**: `pytest` and `unittest` (`unittest.TestCase` + `unittest.mock`)

---

## 2. Architecture Rules (Hexagonal / Ports & Adapters + CQRS Command Bus)

The codebase strictly follows **Hexagonal Architecture (Ports and Adapters)** combined with the **Command Pattern**, **Message Bus**, and **Unit of Work (UoW)**.

```text
app/
├── __init__.py                 # Flask app factory (create_app) & global error_middleware
├── bootstrap.py                # Wires Container dependencies into COMMAND_HANDLERS -> MessageBus
├── config.py                   # Environment configuration (development via local_settings.py vs production)
├── domain/                     # Core business layer (NO Flask or SQLAlchemy imports allowed here)
│   ├── commands/               # Immutable @dataclass commands inheriting from BaseCommand[T]
│   ├── enums/                  # Domain enumerations (PermissionEnum, AuditLogActionEnum)
│   ├── exceptions/             # Domain HTTP exceptions inheriting from BaseHTTPException
│   ├── models/                 # Pydantic v2 domain models
│   ├── ports/                  # Abstract interfaces (ABC) for Container, MessageBus, UoW, Repositories, Libraries
│   └── types.py                # Custom domain types (FormattedDateTime, TypeVar T)
├── application/
│   └── usecases/               # Application service classes containing @staticmethod command handlers
└── adapters/
    ├── container.py            # Concrete Dependency Injector Container
    ├── handlers.py             # COMMAND_HANDLERS dictionary mapping BaseCommand -> UseCase method
    ├── message_bus.py          # Concrete MessageBus dispatching commands
    ├── inputs/                 # Driving adapters (Flask Blueprints: web_views.py, admin_views.py)
    └── outputs/                # Driven adapters
        ├── datasources/        # SQLAlchemy UnitOfWork, Entities (*_entity.py), and PostgreSQL Repositories
        ├── decorators/         # Flask route access-control decorators (require_permissions, require_unlogged)
        └── libraries/          # Concrete utilities (Encription with Argon2, Utils)
```

### Key Architectural Invariants

1. **Direction of Dependencies**:
   - `app/domain/` must **never** depend on `app/application/` or `app/adapters/` or external frameworks like Flask/SQLAlchemy.
   - `app/application/usecases/` depends only on `app/domain/` ports, models, commands, enums, and exceptions.
   - `app/adapters/inputs/` (Flask views) never calls repositories or `UnitOfWork` directly; views must always dispatch a `BaseCommand` through `message_bus.handle(command)`.

2. **Commands & Message Bus**:
   - Every operation is represented by a `@dataclass` command in `app/domain/commands/` inheriting from `BaseCommand[ReturnType]`.
   - Every command is registered in `COMMAND_HANDLERS` (`app/adapters/handlers.py`) pointing to a `@staticmethod` on a UseCase class in `app/application/usecases/`.
   - `bootstrap()` (`app/bootstrap.py`) inspects handler signatures and automatically injects `container` into handlers that declare it.

3. **Unit of Work & Persistence**:
   - All database operations inside use cases must run inside `with container.unit_of_work() as uow:`.
   - Exiting the `with` block automatically calls `uow.rollback()` and closes the session unless `self._session.commit()` was explicitly called inside the repository method.
   - SQLAlchemy entities (`app/adapters/outputs/datasources/postgresql_entities/`) are strictly confined to the datasource adapter layer. Every entity must implement:
     - `@staticmethod def from_model(model: DomainModel) -> Entity` (converting string UUIDs to `uuid.UUID`)
     - `def to_model(self) -> DomainModel` (converting `uuid.UUID` back to `str`)
   - Primary keys use PostgreSQL's `func.uuidv7()` server default.

---

## 3. Business Rules

### 3.1. Users & Authentication
- **Phone Number**:
  - Used as the unique login identifier (`users.phone` unique constraint `users_phone_key`).
  - Must be exactly **10 characters** long and start with `"3"` (Colombian mobile format, e.g., `3001234567`).
  - Duplicate phone registration raises `PhoneAlreadyExistsException` (`HTTPStatus.CONFLICT`).
- **Display Name**:
  - Must be between **4 and 100 characters**.
- **Password Policy**:
  - Length between **8 and 80 characters**.
  - Must contain at least **1 uppercase letter**, **1 lowercase letter**, and **1 numeric digit**.
  - Passwords are hashed using Argon2 (`Encription.hash_password`) and verified via `Encription.verify_hash_password`.
  - `UserModel` excludes `password` and `permissions` when serialized via `model_dump()` (`Field(exclude=True)`).
  - Failed login (either phone not found or wrong password) always raises `WrongCredentialsException` (`HTTPStatus.BAD_REQUEST`) to avoid leaking user existence.

### 3.2. Permissions & Access Control (Housekeeping / Admin Panel)
- Defined in `PermissionEnum`:
  - `CAN_CREATE_ROADTRIP = "create_roadtrip"`
  - `CAN_UPDATE_ROADTRIP = "update_roadtrip"`
- On every request (`before_request` hook in `web_views` and `admin_views`):
  - If `session["user_id"]` is present, the user is loaded with permissions (`with_permissions=True`).
  - If the user no longer exists in DB (`NotFoundException`), the session is cleared.
  - `g.can_hk` is set to `True` if the user holds at least one of `[CAN_CREATE_ROADTRIP, CAN_UPDATE_ROADTRIP]`.
  - `g.in_hk` is `True` on `admin_views` (`/admin/*`) and `False` on `web_views`.
- Decorators:
  - `@require_unlogged()`: Redirects logged-in users away from `/login` and `/register`.
  - `@require_permissions(permissions=[...])`:
    - Redirects unauthenticated users.
    - If `permissions=[]` (e.g., `/logout`), any authenticated user is allowed.
    - If `permissions` is non-empty, the user must have **at least one** of the specified `PermissionEnum` values.

### 3.3. Roadtrips Management
- A roadtrip (`RoadTripModel`) consists of:
  - `display_name` (up to 120 chars)
  - `start_at` (`datetime`)
  - `start_coordinates` & `end_coordinates` (`CoordinatesModel`: `latitude`, `longitude`, `name`)
  - System audit fields: `created_at`, `created_by`, `updated_at`, `updated_by`
- **Roadtrip Cover Photo**:
  - Stored on disk at `./app/static/images/roadtrips/{roadtrip_id}.jpeg` and served at `/static/images/roadtrips/{roadtrip_id}.jpeg`.
  - Only `.jpeg` files are allowed (`Utils.is_allowed_image_extension`).
  - Maximum upload size is **16 MB** (`MAX_CONTENT_LENGTH = 16 * 1000 * 1000`).
  - Deleting a roadtrip (`RoadTripsUseCases.delete_one`) deletes both the database record and its `.jpeg` file on disk if present.

### 3.4. Audit Logging
- Every state-changing action must record an `AuditLogModel` via `uow.audit_log_repository.save(...)` inside the same Unit of Work context:
  - `AuditLogActionEnum.SIGN_IN` on user login
  - `AuditLogActionEnum.SIGN_UP` on user registration
  - `AuditLogActionEnum.ROADTRIP_CREATED` on roadtrip creation (with roadtrip metadata)
  - `AuditLogActionEnum.ROADTRIP_UPDATED` on roadtrip update (with roadtrip metadata)
  - `AuditLogActionEnum.ROADTRIP_DELETED` on roadtrip deletion (with roadtrip metadata)
  - `AuditLogActionEnum.ROADTRIP_PHOTO_UPDATED` on roadtrip cover photo update
- `PostgreSQLAuditLogRepository.save` catches exceptions, logs them, and returns `None` so audit failures never crash user flows.

### 3.5. Pagination
- Paginated use cases (`get_all_paginated` in `RoadTripsUseCases` and `UsersUseCases`):
  - Raise `BadRequestException("Current page is invalid")` if `current_page < 1`.
  - Compute `max_pages = (total_count // limit) + (1 if total_count % limit != 0 else 0)`.
  - Return `([], total_count, max_pages)` if `current_page > max_pages`.
  - Return `(items, total_count, max_pages)` otherwise.

---

## 4. Frontend & Styling Rules

- **SCSS Compilation**:
  - Styles live in `app/static/scss/` using BEM naming (`.hk`, `.hk__form`, `.roadtrip`, etc.).
  - Whenever any `.scss` file is modified, recompile `app/static/css/main.css`:
    ```bash
    sass app/static/scss/main.scss app/static/css/main.css
    ```
- **Maps Integration**:
  - Roadtrip creation and edition forms (`app/templates/admin/roadtrip_form.html` + `app/static/js/admin.js`) use **Leaflet** and **OpenStreetMap Nominatim** for geocoding and reverse-geocoding start/end locations.

---

## 5. Testing Rules & Conventions

1. **1-to-1 Mirror Structure**:
   - Every Python file in `app/` must have a corresponding test file in `tests/` mirroring its path (e.g., `app/application/usecases/roadtrips_usecases.py` -> `tests/application/usecases/test_roadtrips_usecases.py`).
   - All subdirectories inside `tests/` must contain an `__init__.py` file so `unittest` discovery works alongside `pytest`.

2. **Dual Compatibility (`pytest` + `unittest`)**:
   - Write test classes inheriting from `unittest.TestCase` and use `unittest.mock` (`MagicMock`, `patch`) for isolating external dependencies.
   - You may also add `@pytest.mark.parametrize` functions or use fixtures from `tests/conftest.py`.
   - All tests must pass under **both** runners without requiring a running PostgreSQL instance:
     ```bash
     poetry run pytest -v
     poetry run python -m unittest discover -s tests
     ```

3. **Mocking Guidelines**:
   - **Use Cases**: Mock `container.unit_of_work()` using context-manager mocks (`mock_uow.__enter__.return_value = mock_uow`) and assert repository calls and audit log creation.
   - **Repositories**: Mock SQLAlchemy `Session` (`scalar`, `scalars`, `add`, `delete`, `commit`, `refresh`, `query`) and test both happy paths and domain exceptions (`NotFoundException`, `BadRequestException`, `PhoneAlreadyExistsException`).
   - **Flask Views**: Use `app.test_request_context(...)` and `@patch("app.adapters.inputs.<view_module>.message_bus")` to test request parsing, flash messages, session state, `g` context attributes, and redirects.

