# Tattuu Backend API

FastAPI-based backend for the Tattuu tattoo artist discovery platform.

## Architecture

Based on the Medallion (Bronze-Silver-Gold) architecture as documented in `docs/doc.txt`:
- **Ingestão**: FastAPI REST API
- **Armazenamento**: PostgreSQL (operacional) + Data Lake (eventos brutos)
- **Processamento**: Pandas/PySpark transformations
- **Orquestração**: Airflow/cron scripts
- **Consumo**: Power BI + API endpoints

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)
- Kafka (optional, for events)

### Installation

1. Copy environment file:
```bash
cp .env.example .env
```

2. Update `.env` with your configuration

3. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create database tables:
```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Running

Start the development server:
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative docs: `http://localhost:8000/redoc` (ReDoc)

## Project Structure

```
backend-py/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security utilities (JWT, hashing)
│   ├── models/
│   │   └── models.py          # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py         # Pydantic validation schemas
│   ├── routes/
│   │   ├── users.py           # User endpoints
│   │   └── artists.py         # Artist endpoints
│   ├── database.py            # Database connection & session
│   └── main.py                # FastAPI application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## API Endpoints

### Users
- `POST /api/v1/users/register` - Register new user
- `GET /api/v1/users/{user_id}` - Get user details

### Artists
- `POST /api/v1/artists/` - Create artist profile
- `GET /api/v1/artists/` - List artists (with filters)
- `GET /api/v1/artists/{artist_id}` - Get artist details
- `PUT /api/v1/artists/{artist_id}` - Update artist profile

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## Database Migrations

Using Alembic for migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Environment Variables

- `DEBUG` - Enable debug mode (bool)
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string (optional)
- `KAFKA_BOOTSTRAP_SERVERS` - Kafka brokers (optional)
- `DATA_LAKE_PATH` - Path to data lake storage

## Next Steps

- Implement portfolio endpoints
- Implement rating/review endpoints
- Add authentication and authorization
- Implement event streaming to Kafka
- Add data validation and error handling
- Setup database migrations with Alembic
- Write comprehensive tests
- Deploy to production environment

## References

See `docs/doc.txt` for complete architecture documentation.
