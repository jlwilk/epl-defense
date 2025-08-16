# EPL Defense - FastAPI Backend

English Premier League stats API using API-Football v3 with FastAPI, SQLAlchemy, and comprehensive caching.

**API Documentation**: [API-Football v3](https://www.api-football.com/documentation-v3)

## Features

- 🚀 **FastAPI backend** with automatic OpenAPI documentation
- 🗄️ **SQLAlchemy 2.0** with Alembic migrations (ready for Postgres)
- 🔑 **Dual API key support**: Direct API-Football or RapidAPI
- 📊 **EPL endpoints**: standings, teams, fixtures, defense stats
- 🐳 **Docker ready** with docker-compose for local development
- 📝 **Type hints** throughout with Pydantic schemas

## Quick Start

### 1. Setup Environment

```bash
# Clone and setup
git clone <your-repo>
cd epl-defense

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure API Keys

Copy the example environment file and configure your API key:

```bash
cp env.sample .env
# Edit .env and set either:
# Option A - Direct API-Football key:
APIFOOTBALL_API_KEY=your_direct_key_here
APIFOOTBALL_BASE_URL=https://v3.football.api-sports.io

# Option B - RapidAPI key (recommended):
RAPIDAPI_KEY=your_rapidapi_key_here
APIFOOTBALL_BASE_URL=https://api-football-v1.p.rapidapi.com/v3
```

### 3. Start the API Server

```bash
# Start FastAPI server
epl-fastapi

# Or run directly
python -m app.main

# Server runs on http://127.0.0.1:8001
```

### 4. Explore the API

- **Interactive docs**: http://127.0.0.1:8001/docs
- **ReDoc**: http://127.0.0.1:8001/redoc
- **Health check**: http://127.0.0.1:8001/health

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | API health status |
| `/leagues` | GET | List all leagues |
| `/teams` | GET | Teams by season/league |
| `/standings` | GET | League standings |
| `/fixtures` | GET | Match fixtures |
| `/defense/table` | GET | Goals conceded per team |

### Example Requests

```bash
# Get EPL 2024 standings
curl 'http://127.0.0.1:8001/standings/?season=2024'

# Get teams in EPL 2024
curl 'http://127.0.0.1:8001/teams/?season=2024'

# Get recent fixtures
curl 'http://127.0.0.1:8001/fixtures/?season=2024&last=10'

# Get defense table (goals conceded)
curl 'http://127.0.0.1:8001/defense/table?season=2024'
```

## Project Structure

```
epl-defense/
├── app/                    # FastAPI application
│   ├── api/              # API route handlers
│   │   ├── routes_*.py   # Endpoint definitions
│   ├── config.py         # Configuration management
│   ├── db/               # Database setup
│   ├── main.py           # FastAPI app factory
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── epl_defense/          # Legacy CLI (deprecated)
├── alembic/              # Database migrations
├── docker-compose.yml    # Local development
├── pyproject.toml        # Python packaging
└── README.md
```

## Development

### Database Setup

```bash
# Initialize Alembic (when ready for DB)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Docker Development

```bash
# Start Postgres and Redis
docker-compose up -d

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost:5432/epl_defense
```

### Testing

```bash
# Run tests (when added)
pytest

# Run with coverage
pytest --cov=app
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APIFOOTBALL_API_KEY` | - | Direct API-Football key |
| `RAPIDAPI_KEY` | - | RapidAPI key (alternative) |
| `APIFOOTBALL_BASE_URL` | `https://v3.football.api-sports.io` | API base URL |
| `DATABASE_URL` | `sqlite:///./epl.db` | Database connection |
| `HOST` | `127.0.0.1` | Server host |
| `PORT` | `8001` | Server port |
| `DEBUG` | `false` | Debug mode |

## API Rate Limits

- **Direct API-Football**: 7500 requests/day (Pro plan)
- **RapidAPI**: Varies by plan
- **Local caching**: Implemented to minimize API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Your License Here]

## Support

- **API Documentation**: [API-Football v3](https://www.api-football.com/documentation-v3)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/




