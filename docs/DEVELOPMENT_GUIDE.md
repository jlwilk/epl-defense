# 🛠️ Development Guide

This guide provides comprehensive information for developers contributing to the EPL Defense API project.

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **Git**: For version control
- **API Keys**: RapidAPI or API-Football direct access
- **Database**: SQLite (included) or PostgreSQL

### Development Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/epl-defense.git
   cd epl-defense
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

4. **Environment Configuration**
   ```bash
   cp env.sample .env
   # Edit .env with your API keys and preferences
   ```

5. **Database Initialization**
   ```bash
   python init_database.py
   ```

## 🏗️ Project Architecture

### Directory Structure

```
epl-defense/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI application factory
│   ├── config.py          # Configuration management
│   ├── api/               # API route definitions
│   │   ├── __init__.py
│   │   ├── routes_leagues.py
│   │   ├── routes_teams.py
│   │   ├── routes_fixtures.py
│   │   ├── routes_standings.py
│   │   ├── routes_player_stats.py
│   │   ├── routes_team_stats.py
│   │   ├── routes_ingestion.py
│   │   └── routes_defense.py
│   ├── db/                # Database layer
│   │   ├── __init__.py
│   │   └── session.py     # Database session management
│   ├── models/            # SQLAlchemy data models
│   │   ├── __init__.py
│   ├── schemas/           # Pydantic response schemas
│   │   ├── __init__.py
│   │   └── api_responses.py
│   └── services/          # Business logic services
│       ├── __init__.py
│       ├── api_client.py  # External API client
│       └── ingestion.py   # Data ingestion service
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Test configuration and fixtures
│   ├── test_teams.py
│   ├── test_fixtures.py
│   ├── test_leagues.py
│   └── test_ingestion.py
├── docs/                  # Documentation
├── pyproject.toml         # Project configuration
├── pytest.ini            # Test configuration
├── init_database.py       # Database initialization script
└── README.md             # Project overview
```

### Key Components

#### 1. **FastAPI Application (`app/main.py`)**
- Application factory pattern
- Middleware configuration (CORS)
- Router registration
- Health check endpoint

#### 2. **Configuration (`app/config.py`)**
- Environment variable management
- Settings validation with Pydantic
- Default values and overrides

#### 3. **Database Layer (`app/db/`)**
- SQLAlchemy 2.0 ORM setup
- Session management
- Connection pooling

#### 4. **Data Models (`app/models/`)**
- SQLAlchemy model definitions
- Relationship mappings
- Database schema representation

#### 5. **API Routes (`app/api/`)**
- Endpoint definitions
- Request/response validation
- Error handling

#### 6. **Services (`app/services/`)**
- Business logic implementation
- External API integration
- Data processing

## 🔧 Development Workflow

### 1. **Feature Development**

```bash
# Create feature branch
git checkout -b feature/new-endpoint

# Make changes
# ... edit files ...

# Run tests
python -m pytest

# Commit changes
git add .
git commit -m "feat: add new endpoint for player rankings"

# Push and create PR
git push origin feature/new-endpoint
```

### 2. **Code Quality Standards**

#### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints throughout
- Maximum line length: 88 characters (Black formatter)

#### Code Formatting
```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with flake8
flake8 app/ tests/
```

#### Type Hints
```python
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

def get_teams(
    season: Optional[int] = None,
    league: Optional[int] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get teams with optional filtering."""
    pass
```

### 3. **Testing Strategy**

#### Test Structure
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database operations
- **Mock Tests**: Test external API interactions

#### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_teams.py

# Run with coverage
python -m pytest --cov=app tests/

# Run specific test
python -m pytest tests/test_teams.py::TestTeams::test_list_teams

# Run tests in parallel
python -m pytest -n auto
```

#### Test Naming Conventions
```python
class TestTeams:
    def test_list_teams_success(self, client):
        """Test successful team listing."""
        pass
    
    def test_list_teams_with_filters(self, client):
        """Test team listing with query parameters."""
        pass
    
    def test_list_teams_error_handling(self, client):
        """Test error handling in team listing."""
        pass
```

### 4. **Database Development**

#### Model Changes
1. **Update Model**: Modify `app/models/` files
2. **Create Migration**: Generate Alembic migration
3. **Test Migration**: Apply to test database
4. **Update Tests**: Ensure tests pass with new schema

#### Database Operations
```bash
# Initialize database
python init_database.py

# Drop and recreate (development only)
python init_database.py --drop

# Check database schema
sqlite3 epl_defense.db ".schema"
```

## 📡 API Development

### 1. **Adding New Endpoints**

#### Route Definition
```python
from fastapi import APIRouter, Depends, Query, Path
from app.schemas import ApiResponse
from app.db.session import get_db

router = APIRouter(prefix="/example", tags=["example"])

@router.get(
    "/{item_id}",
    summary="Get Item",
    description="Retrieve item by ID with detailed information.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "get": "example",
                        "parameters": {"id": "123"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": {...}
                    }
                }
            }
        }
    }
)
def get_item(
    item_id: int = Path(..., description="Item ID"),
    db: Session = Depends(get_db)
) -> ApiResponse:
    """Get item by ID."""
    pass
```

#### Response Schema
```python
from pydantic import BaseModel, Field
from typing import Optional, Any

class ExampleResponse(BaseModel):
    id: int = Field(description="Item identifier")
    name: str = Field(description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    metadata: Dict[str, Any] = Field(description="Additional metadata")
```

### 2. **Error Handling**

#### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (resource doesn't exist)
- **422**: Validation Error (parameter type mismatch)
- **500**: Internal Server Error
- **502**: Bad Gateway (external API error)

#### Error Response Format
```python
from fastapi import HTTPException

def get_item(item_id: int) -> Dict[str, Any]:
    if not item_exists(item_id):
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} not found"
        )
    return get_item_data(item_id)
```

### 3. **Parameter Validation**

#### Query Parameters
```python
def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Category filter")
):
    pass
```

#### Path Parameters
```python
def get_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
    version: Optional[str] = Path(None, description="API version")
):
    pass
```

## 🗄️ Database Development

### 1. **Model Definition**

#### Basic Model
```python
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

class Example(Base):
    __tablename__ = "examples"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True, 
        onupdate=func.now()
    )
```

#### Relationships
```python
# One-to-Many
class Team(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    players: Mapped[List["Player"]] = relationship("Player", back_populates="team")

class Player(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship("Team", back_populates="players")

# Many-to-Many
class Fixture(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teams: Mapped[List["Team"]] = relationship(
        "Team", 
        secondary="fixture_teams",
        back_populates="fixtures"
    )
```

### 2. **Database Operations**

#### Session Management
```python
from app.db.session import get_db
from sqlalchemy.orm import Session

def create_item(
    name: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    try:
        item = Example(name=name)
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"id": item.id, "name": item.name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
```

#### Query Examples
```python
# Basic queries
items = db.query(Example).all()
item = db.query(Example).filter(Example.id == item_id).first()

# Complex queries
items = db.query(Example).filter(
    Example.is_active == True,
    Example.name.contains(search_term)
).order_by(Example.created_at.desc()).limit(limit).offset(offset).all()

# Joins
teams_with_players = db.query(Team).join(Player).filter(
    Player.is_active == True
).all()
```

## 🧪 Testing

### 1. **Test Configuration**

#### Pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=app
    --cov-report=term-missing
    --cov-report=html
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

#### Test Fixtures (`tests/conftest.py`)
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.db.session import get_db

@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Create a test client with database override."""
    app = create_app()
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
```

### 2. **Test Examples**

#### Unit Tests
```python
def test_calculate_team_points():
    """Test team points calculation."""
    wins = 3
    draws = 2
    losses = 1
    
    points = calculate_team_points(wins, draws, losses)
    assert points == 11  # 3*3 + 2*1 + 1*0
```

#### API Tests
```python
def test_get_teams_success(client):
    """Test successful teams endpoint."""
    response = client.get("/teams/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["get"] == "teams"
    assert "response" in data
    assert isinstance(data["response"], list)

def test_get_teams_with_filters(client):
    """Test teams endpoint with query parameters."""
    response = client.get("/teams/?season=2025&league=39")
    assert response.status_code == 200
    
    data = response.json()
    assert data["parameters"]["season"] == "2025"
    assert data["parameters"]["league"] == "39"
```

#### Mock Tests
```python
from unittest.mock import patch, MagicMock

def test_external_api_call(client):
    """Test external API integration with mocking."""
    mock_response = {
        "get": "teams",
        "parameters": {"league": "39"},
        "errors": None,
        "results": 1,
        "response": [{"id": 40, "name": "Liverpool"}]
    }
    
    with patch('app.services.api_client.ApiClientV3.get') as mock_get:
        mock_get.return_value = mock_response
        
        response = client.get("/teams/?league=39")
        assert response.status_code == 200
        
        data = response.json()
        assert data["response"][0]["name"] == "Liverpool"
```

## 🔍 Debugging

### 1. **Logging**

#### Logging Configuration
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def some_function():
    logger.info("Function called")
    try:
        # ... function logic ...
        logger.info("Function completed successfully")
    except Exception as e:
        logger.error(f"Function failed: {e}")
        raise
```

### 2. **Development Tools**

#### FastAPI Debug Mode
```python
# In main.py
app = FastAPI(
    title="EPL Defense API",
    debug=True  # Enable debug mode
)
```

#### Database Debug
```python
# In session.py
engine = create_engine(
    database_url,
    echo=True,  # Enable SQL logging
    future=True
)
```

### 3. **Common Issues**

#### Import Errors
```bash
# Ensure you're in the right directory
cd /path/to/epl-defense

# Install in development mode
pip install -e .

# Check Python path
python -c "import app; print(app.__file__)"
```

#### Database Issues
```bash
# Check database file
ls -la *.db

# Verify database schema
sqlite3 epl_defense.db ".schema"

# Reset database
python init_database.py --drop
```

#### API Key Issues
```bash
# Check environment variables
echo $RAPIDAPI_KEY
echo $APIFOOTBALL_API_KEY

# Test API connection
curl -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
     -H "X-RapidAPI-Host: v3.football.api-sports.io" \
     "https://v3.football.api-sports.io/status"
```

## 🚀 Deployment

### 1. **Production Considerations**

#### Environment Variables
```bash
# Production environment
export DATABASE_URL="postgresql://user:pass@host:port/db"
export LOG_LEVEL="WARNING"
export CORS_ORIGINS="https://yourdomain.com"
export API_RATE_LIMIT="1000/hour"
```

#### Database Migration
```bash
# Run migrations
alembic upgrade head

# Check migration status
alembic current
alembic history
```

### 2. **Performance Optimization**

#### Database Indexes
```python
# Add indexes for frequently queried fields
class Team(Base):
    __table_args__ = (
        Index('idx_team_league_season', 'league_id', 'season'),
        Index('idx_team_name', 'name'),
    )
```

#### Caching Strategy
```python
# Implement Redis caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_team_statistics(team_id: int, season: int):
    """Cache team statistics for performance."""
    pass
```

## 📚 Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)

### Code Examples
- [FastAPI Examples](https://github.com/tiangolo/fastapi/tree/master/docs_src)
- [SQLAlchemy Examples](https://github.com/sqlalchemy/sqlalchemy/tree/main/examples)

### Community
- [FastAPI Discord](https://discord.gg/VQjSKpy)
- [SQLAlchemy Mailing List](https://groups.google.com/forum/#!forum/sqlalchemy)

---

This development guide should help you get started with contributing to the EPL Defense API project. For additional questions or clarifications, please refer to the project documentation or create an issue on GitHub.
