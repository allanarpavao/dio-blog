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
│   │   └── role.py
│   ├── models/
│   ├── repositories/
│   ├── utils.py
│   ├── views/
│   └── wsgi.py
├── tests/
│   ├── __init__.py
│   ├── integration/
│   └── unit/
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install the dependencies:

```bash
poetry install
```

Run the application:

```bash
poetry run flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API Endpoints

### Authentication

- `POST /auth/login`: Authenticate a user and return a JWT.

### Roles

- `POST /roles/`: Create a new role.

## Testing

Run tests using pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.