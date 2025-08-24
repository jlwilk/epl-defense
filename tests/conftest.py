import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.db.session import get_db
from app.models.base import Base


@pytest.fixture
def test_db():
    """Create a test database in memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Create a database session for testing."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(test_db, db_session):
    """Create a test client with a test database."""
    app = create_app()
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_api_response():
    """Mock API response for testing."""
    return {
        "get": "test_endpoint",
        "parameters": {"test": "value"},
        "errors": None,
        "results": 1,
        "paging": None,
        "response": [{"id": 1, "name": "Test"}]
    }


@pytest.fixture
def mock_team_statistics_response():
    """Mock team statistics API response for testing."""
    return {
        "get": "teams/statistics",
        "parameters": {"team": "33", "league": "39", "season": "2025"},
        "errors": None,
        "results": 1,
        "paging": None,
        "response": {
            "league": {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://media.api-sports.io/football/leagues/39.png",
                "flag": "https://media.api-sports.io/flags/gb-eng.svg",
                "season": 2025
            },
            "team": {
                "id": 33,
                "name": "Manchester United",
                "logo": "https://media.api-sports.io/football/teams/33.png"
            },
            "form": "L",
            "fixtures": {
                "played": {"home": 1, "away": 0, "total": 1},
                "wins": {"home": 0, "away": 0, "total": 0},
                "draws": {"home": 0, "away": 0, "total": 0},
                "loses": {"home": 1, "away": 0, "total": 1}
            },
            "goals": {
                "for": {"total": {"home": 0, "away": 0, "total": 0}},
                "against": {"total": {"home": 1, "away": 0, "total": 1}}
            },
            "biggest": {
                "streak": {"wins": 0, "draws": 0, "loses": 1},
                "wins": {"home": None, "away": None},
                "loses": {"home": "0-1", "away": None},
                "goals": {"for": {"home": 0, "away": 0}, "against": {"home": 1, "away": 0}}
            },
            "clean_sheet": {"home": 0, "away": 0, "total": 0},
            "failed_to_score": {"home": 1, "away": 0, "total": 1},
            "penalty": {
                "scored": {"total": 0, "percentage": "0%"},
                "missed": {"total": 0, "percentage": "0%"},
                "total": 0
            },
            "lineups": [
                {"formation": "3-4-2-1", "played": 1}
            ],
            "cards": {
                "yellow": {
                    "0-15": {"total": None, "percentage": None},
                    "16-30": {"total": None, "percentage": None},
                    "31-45": {"total": None, "percentage": None},
                    "46-60": {"total": None, "percentage": None},
                    "61-75": {"total": None, "percentage": None},
                    "76-90": {"total": 1, "percentage": "100.00%"},
                    "91-105": {"total": None, "percentage": None},
                    "106-120": {"total": None, "percentage": None}
                },
                "red": {
                    "0-15": {"total": None, "percentage": None},
                    "16-30": {"total": None, "percentage": None},
                    "31-45": {"total": None, "percentage": None},
                    "46-60": {"total": None, "percentage": None},
                    "61-75": {"total": None, "percentage": None},
                    "76-90": {"total": None, "percentage": None},
                    "91-105": {"total": None, "percentage": None},
                    "106-120": {"total": None, "percentage": None}
                }
            }
        }
    }


@pytest.fixture
def mock_player_stats_response():
    """Mock player statistics API response for testing."""
    return {
        "get": "players",
        "parameters": {"player": "152982", "season": "2025", "league": "39"},
        "errors": None,
        "results": 1,
        "paging": None,
        "response": [{
            "player": {
                "id": 152982,
                "name": "Erling Haaland",
                "firstname": "Erling",
                "lastname": "Haaland",
                "age": 24,
                "nationality": "Norway",
                "height": "194 cm",
                "weight": "88 kg",
                "injured": False,
                "photo": "https://media.api-sports.io/football/players/152982.png"
            },
            "statistics": [{
                "team": {
                    "id": 50,
                    "name": "Manchester City",
                    "logo": "https://media.api-sports.io/football/teams/50.png"
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb-eng.svg",
                    "season": 2025
                },
                "games": {
                    "appearences": 15,
                    "lineups": 15,
                    "minutes": 1350,
                    "number": 9,
                    "position": "Attacker",
                    "rating": "7.8",
                    "captain": False
                },
                "substitutes": {
                    "in": 0,
                    "out": 2,
                    "bench": 0
                },
                "shots": {
                    "total": 45,
                    "on": 28
                },
                "goals": {
                    "total": 18,
                    "conceded": 0,
                    "assists": 5,
                    "saves": None
                },
                "passes": {
                    "total": 450,
                    "key": 12,
                    "accuracy": 85
                },
                "tackles": {
                    "total": 8,
                    "blocks": 2,
                    "interceptions": 3
                },
                "duels": {
                    "total": 45,
                    "won": 28
                },
                "dribbles": {
                    "attempts": 15,
                    "success": 8,
                    "past": None
                },
                "fouls": {
                    "drawn": 12,
                    "committed": 8
                },
                "cards": {
                    "yellow": 2,
                    "red": 0
                },
                "penalty": {
                    "won": 1,
                    "commited": 0,
                    "scored": 2,
                    "missed": 0,
                    "saved": None
                }
            }]
        }]
    }


@pytest.fixture
def mock_league_player_stats_response():
    """Mock league player statistics API response for testing."""
    return {
        "get": "players",
        "parameters": {"league": "39", "season": "2025", "team": "33"},
        "errors": None,
        "results": 2,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 152982,
                    "name": "Erling Haaland",
                    "firstname": "Erling",
                    "lastname": "Haaland"
                },
                "statistics": [{
                    "team": {"id": 50, "name": "Manchester City"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 15, "goals": {"total": 18}}
                }]
            },
            {
                "player": {
                    "id": 874,
                    "name": "Mohamed Salah",
                    "firstname": "Mohamed",
                    "lastname": "Salah"
                },
                "statistics": [{
                    "team": {"id": 40, "name": "Liverpool"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 16, "goals": {"total": 15}}
                }]
            }
        ]
    }


@pytest.fixture
def mock_team_player_stats_response():
    """Mock team player statistics API response for testing."""
    return {
        "get": "players",
        "parameters": {"team": "33", "season": "2025", "league": "39"},
        "errors": None,
        "results": 2,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 874,
                    "name": "Marcus Rashford",
                    "firstname": "Marcus",
                    "lastname": "Rashford"
                },
                "statistics": [{
                    "team": {"id": 33, "name": "Manchester United"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 14, "goals": {"total": 8}}
                }]
            },
            {
                "player": {
                    "id": 875,
                    "name": "Bruno Fernandes",
                    "firstname": "Bruno",
                    "lastname": "Fernandes"
                },
                "statistics": [{
                    "team": {"id": 33, "name": "Manchester United"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 15, "goals": {"total": 6}}
                }]
            }
        ]
    }


@pytest.fixture
def mock_player_seasons_response():
    """Mock player seasons API response for testing."""
    return {
        "get": "players/seasons",
        "parameters": {"player": "152982"},
        "errors": None,
        "results": 3,
        "paging": None,
        "response": [2023, 2024, 2025]
    }


@pytest.fixture
def mock_player_countries_response():
    """Mock player countries API response for testing."""
    return {
        "get": "players/countries",
        "parameters": {},
        "errors": None,
        "results": 3,
        "paging": None,
        "response": [
            {"name": "England", "code": "GB"},
            {"name": "Brazil", "code": "BR"},
            {"name": "France", "code": "FR"}
        ]
    }


@pytest.fixture
def mock_player_search_response():
    """Mock player search API response for testing."""
    return {
        "get": "players",
        "parameters": {"search": "Haaland", "league": "39", "season": "2025"},
        "errors": None,
        "results": 1,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 152982,
                    "name": "Erling Haaland",
                    "firstname": "Erling",
                    "lastname": "Haaland",
                    "age": 24,
                    "nationality": "Norway"
                }
            }
        ]
    }


@pytest.fixture
def mock_top_scorers_response():
    """Mock top scorers API response for testing."""
    return {
        "get": "players",
        "parameters": {"league": "39", "season": "2025", "limit": "10"},
        "errors": None,
        "results": 3,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 152982,
                    "name": "Erling Haaland",
                    "firstname": "Erling",
                    "lastname": "Haaland"
                },
                "statistics": [{
                    "team": {"id": 50, "name": "Manchester City"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 15, "goals": {"total": 18}}
                }]
            },
            {
                "player": {
                    "id": 874,
                    "name": "Mohamed Salah",
                    "firstname": "Mohamed",
                    "lastname": "Salah"
                },
                "statistics": [{
                    "team": {"id": 40, "name": "Liverpool"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 16, "goals": {"total": 15}}
                }]
            },
            {
                "player": {
                    "id": 875,
                    "name": "Ollie Watkins",
                    "firstname": "Ollie",
                    "lastname": "Watkins"
                },
                "statistics": [{
                    "team": {"id": 66, "name": "Aston Villa"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 15, "goals": {"total": 12}}
                }]
            }
        ]
    }


@pytest.fixture
def mock_top_assists_response():
    """Mock top assists API response for testing."""
    return {
        "get": "players",
        "parameters": {"league": "39", "season": "2025"},
        "errors": None,
        "results": 2,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 875,
                    "name": "Bruno Fernandes",
                    "firstname": "Bruno",
                    "lastname": "Fernandes"
                },
                "statistics": [{
                    "team": {"id": 33, "name": "Manchester United"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 15, "goals": {"assists": 8}}
                }]
            },
            {
                "player": {
                    "id": 876,
                    "name": "Kevin De Bruyne",
                    "firstname": "Kevin",
                    "lastname": "De Bruyne"
                },
                "statistics": [{
                    "team": {"id": 50, "name": "Manchester City"},
                    "league": {"id": 39, "name": "Premier League"},
                    "games": {"appearences": 12, "goals": {"assists": 7}}
                }]
            }
        ]
    }


@pytest.fixture
def mock_defensive_leaders_response():
    """Mock defensive leaders API response for testing."""
    return {
        "get": "players",
        "parameters": {"league": "39", "season": "2025"},
        "errors": None,
        "results": 2,
        "paging": None,
        "response": [
            {
                "player": {
                    "id": 877,
                    "name": "Virgil van Dijk",
                    "firstname": "Virgil",
                    "lastname": "van Dijk"
                },
                "statistics": [{
                    "team": {"id": 40, "name": "Liverpool"},
                    "league": {"id": 39, "name": "Premier League"},
                    "tackles": {"total": 45},
                    "interceptions": {"total": 12}
                }]
            },
            {
                "player": {
                    "id": 878,
                    "name": "Ruben Dias",
                    "firstname": "Ruben",
                    "lastname": "Dias"
                },
                "statistics": [{
                    "team": {"id": 50, "name": "Manchester City"},
                    "league": {"id": 39, "name": "Premier League"},
                    "tackles": {"total": 38},
                    "interceptions": {"total": 15}
                }]
            }
        ]
    }
