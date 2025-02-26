# API Key Management System

A FastAPI-based API key management system that allows users to create, manage, and monitor API keys for authentication and access control.

## Features

- User authentication and authorization
- API key generation and management
- Request logging and monitoring
- Rate limiting
- Key expiration and rotation
- Secure key storage with hashing
- Detailed usage analytics

## Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **API Documentation**: Swagger/OpenAPI

## Project Structure

```
api_key_manager/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   ├── api_keys.py
│   │       │   └── auth.py
│   │       └── router.py
│   │
│   ├── core/
│   │   ├── security.py
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── api_key.py
│   │   └── api_key_log.py
│   │
│   └── schemas/
│       ├── user.py
│       ├── api_key.py
│       └── token.py
│
├── requirements.txt
└── .env
```

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/api-key-manager.git
cd api-key-manager
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database:
```sql
CREATE DATABASE api_key_manager;
```

5. Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/api_key_manager
SECRET_KEY=your-secret-key-here
PROJECT_NAME="API Key Manager"
```

6. Initialize the database:
```bash
python -m alembic upgrade head
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### API Keys
- `POST /api/v1/api-keys/` - Create new API key
- `GET /api/v1/api-keys/` - List user's API keys
- `DELETE /api/v1/api-keys/{key_id}` - Delete an API key

### Usage Analytics
- `GET /api/v1/api-keys/{key_id}/logs` - Get API key usage logs
- `GET /api/v1/api-keys/{key_id}/stats` - Get API key usage statistics

## Database Schema

The system uses three main tables:

1. `users` - Stores user information
2. `api_keys` - Stores API keys linked to users
3. `api_key_logs` - Tracks API key usage

## Security Features

- API keys are hashed before storage
- JWT-based authentication
- Rate limiting per API key
- Request logging and monitoring
- Automatic key expiration
- IP address tracking

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```

## Production Deployment

1. Set proper environment variables
2. Use a production-grade ASGI server like Uvicorn with Gunicorn
3. Set up proper SSL/TLS certificates
4. Configure rate limiting and monitoring

Example production start command:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- PostgreSQL documentation