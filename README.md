# DIO Bank

DIO Bank is a Flask-based web application that provides authentication and role management functionalities. This project uses SQLAlchemy for database interactions and JWT for secure authentication.

## Project Structure
```
dio-bank/
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 40598c136642_initial_migration.py
├── pyproject.toml
├── src/
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── role_controller.py
│   │   └── user_controller.py
│   ├── models/
│   │   ├── role.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── role_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── role_schema.py
│   │   └── user_schema.py
│   ├── utils.py
│   ├── views/
│   └── wsgi.py
├── tests/
│   ├── __init__.py
│   ├── integration/
│   └── unit/
```

## Features

- Add, update, delete, and query user and role data.
- Authenticate users and manage roles.
- Custom responses for listing users with related information (roles).
- Graceful handling of duplicate entries with descriptive error messages.
- Documentation available via Swagger UI.

## Technology Stack

- Flask: For building the web application.
- SQLAlchemy: For database interaction.
- Alembic: For managing database migrations.
- Marshmallow: For data validation and serialization.
- Flask-Swagger-UI: For API documentation.
- Pytest: For testing.

## Setup Instructions

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.9 or higher

### Installation

Install the dependencies:

```bash
poetry install
```

### Running the Application

To create a new migration, execute:

```bash
poetry run alembic revision --autogenerate -m "migration_name"
```

To apply migrations and create the database, execute:

```bash
poetry run alembic upgrade head
```

Run the application:

```bash
poetry run flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API Endpoints

### Authentication

- `POST /auth/login`: Authenticate a user and return a JWT.
- `POST /auth/register`: Register a new user.

### Roles

- `POST /roles/`: Create a new role.
- `GET /roles/`: Retrieve all roles.
- `GET /roles/<id>`: Retrieve a specific role by ID.
- `PUT /roles/<id>`: Update a specific role by ID.
- `DELETE /roles/<id>`: Delete a specific role by ID.

### Users

- `GET /users/`: Retrieve all users.
- `GET /users/<id>`: Retrieve a specific user by ID.
- `PUT /users/<id>`: Update a specific user by ID.
- `DELETE /users/<id>`: Delete a specific user by ID.

## Testing

Run tests using pytest:

```bash
pytest
```

## References

- [Flask Documentation](https://flask.palletsprojects.com/en/latest/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/latest/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/en/latest/)
- [Flask-Swagger-UI Documentation](https://github.com/swagger-api/swagger-ui)
- [Pytest Documentation](https://docs.pytest.org/en/latest/)
