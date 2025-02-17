# DIO Blog

DIO Blog is a Flask-based web application that provides authentication and role management functionalities. This project uses SQLAlchemy for database interactions and JWT for secure authentication.

## Project Structure
```
dio-bank/
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
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
│   │   ├── role_view.py
│   │   └── user_view.py
│   └── wsgi.py
├── tests/
│   ├── __init__.py
│   ├── integration/
│   └── unit/
```

## Features

- Add, update, delete, and query user, posts and role data.
- Authenticate users and manage roles.
- Custom responses for listing users with related information (roles).
- Graceful handling of duplicate entries with descriptive error messages.
- (in progress) Documentation available via Swagger UI.
- Web interface for managing users and posts.

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
ENVIRONMENT=development poetry run flask --app src.app run --debug
```

## API Endpoints

### Authentication

- `POST /auth/login`: Authenticate a user and return a JWT.
- `POST /auth/register`: Register a new user.

### Roles

- `POST /roles/`: Create a new role.

### Users

- `GET /users/list`: Retrieve all users.
- `GET /users/<id>`: Retrieve a specific user by ID.
- `PATCH /users/<id>`: Update a specific user by ID.
- `DELETE /users/<id>`: Delete a specific user by ID.

### Posts
- `POST /create/`: Create a new post.
- (in progress) `GET /posts/`: Retrieve all posts.
- (in progress) `GET /posts/<id>`: Retrieve a specific post by ID.
- `PATCH /update/<id>`: Update a specific post by ID.
- `DELETE /delete/<id>`: Delete a specific post by ID.


## Web Interface

Access the web interface at [http://127.0.0.1:5000](http://127.0.0.1:5000) to manage users and posts through a user-friendly UI.

## Testing

Run tests using pytest:

```bash
pytest
```

## Work in Progress

- Documentation via Swagger UI.
- API Endpoints: POSTS `GET /posts/`: Retrieve all posts.
- API Endpoints: POSTS `GET /posts/<id>`: Retrieve a specific post by ID.


## References

- [Flask Documentation](https://flask.palletsprojects.com/en/latest/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/latest/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/en/latest/)
- [Flask-Swagger-UI Documentation](https://github.com/swagger-api/swagger-ui)
- [Pytest Documentation](https://docs.pytest.org/en/latest/)

