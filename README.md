# EPL Defense API 🏆⚽

A comprehensive English Premier League statistics and data API built with FastAPI, featuring intelligent data ingestion and caching from API-Football v3.

## ✨ Features

- **🏗️ Complete Data Model**: Comprehensive database schema for leagues, teams, players, fixtures, and statistics
- **📥 Smart Data Ingestion**: Bulk import teams and players with pagination handling and rate limiting
- **🔄 Background Processing**: Asynchronous data ingestion with progress tracking
- **⚡ Fast Responses**: Local database queries instead of external API calls
- **🔄 2025 Season Ready**: Defaults to current EPL season with easy override
- **📊 Rich Statistics**: Player stats, team performance, fixture details, and more
- **🔒 Rate Limit Aware**: Intelligent pagination and API call management
- **🎯 Comprehensive Player Stats**: Individual, team, and league-wide player performance metrics
- **⚽ Fixture Player Stats**: Detailed match-by-match player performance data
- **🏆 Leaderboards**: Top scorers, assist providers, and defensive leaders

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and setup
git clone <your-repo>
cd epl-defense
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Copy environment file
cp env.sample .env
# Edit .env with your API keys
```

### 2. Initialize Database

```bash
# Create all database tables
python init_database.py
```

### 3. Start FastAPI Server

```bash
# Development server with hot reload
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Or use the dev script
epl-fastapi
```

### 4. Ingest EPL Data

```bash
# Start ingesting all EPL 2025 data
curl -X POST 'http://127.0.0.1:8000/ingestion/epl/2025'

# Check ingestion status
curl 'http://127.0.0.1:8000/ingestion/status/39/2025'
```

## 🗄️ Database Schema

### Core Entities

- **League**: League information, seasons, coverage
- **Team**: Team details, venues, league membership
- **Player**: Player profiles, statistics, team membership
- **Fixture**: Match details, scores, status
- **FixtureEvent**: Goals, cards, substitutions
- **FixtureLineup**: Team formations, player positions
- **FixtureStatistics**: Match statistics, possession, shots
- **FixturePlayerStats**: Individual player performance in specific matches

### Relationships

```
League (1) ←→ (N) Team
Team (1) ←→ (N) Player
Team (1) ←→ (1) Venue
League (1) ←→ (N) Fixture
Fixture (1) ←→ (N) FixtureEvent
Fixture (1) ←→ (N) FixtureLineup
Fixture (1) ←→ (N) FixtureStatistics
Fixture (1) ←→ (N) FixturePlayerStats
```

## 📡 API Endpoints

### Data Ingestion

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/ingestion/epl/2025` | POST | Start EPL 2025 data ingestion |
| `/ingestion/league/{id}/season/{year}` | POST | Ingest specific league/season |
| `/ingestion/status/{id}/{year}` | GET | Check ingestion progress |

### Teams & Players

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/teams/` | GET | List all teams (defaults to 2025) |
| `/teams/{id}` | GET | Team details |
| `/teams/{id}/players` | GET | Team roster |
| `/teams/{id}/statistics` | GET | Team performance stats |
| `/teams/{id}/fixtures` | GET | Team fixtures |
| `/teams/search` | GET | Search teams by name |

### Fixtures & Matches

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/fixtures/` | GET | All fixtures (defaults to 2025) |
| `/fixtures/live` | GET | Live matches |
| `/fixtures/head-to-head` | GET | Head-to-head fixtures between teams |
| `/fixtures/{id}/players` | GET | Live player stats from API-Football |
| `/fixtures/{id}/players/stored` | GET | Stored fixture player statistics |

### Player Statistics (NEW! 🎯)

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/player-stats/player/{id}` | GET | Individual player season statistics |
| `/player-stats/team/{id}` | GET | All player stats for a team |
| `/player-stats/league/{id}` | GET | All player stats for a league |
| `/player-stats/top-scorers` | GET | Top goal scorers leaderboard |
| `/player-stats/top-assists` | GET | Top assist providers leaderboard |
| `/player-stats/defensive-leaders` | GET | Top defensive players by metric |
| `/player-stats/search` | GET | Search players by name |
| `/player-stats/countries` | GET | Available player countries |
| `/player-stats/player/{id}/seasons` | GET | All seasons for a player |

### Statistics & Analysis

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/standings/` | GET | League table (defaults to 2025) |
| `/defense/table` | GET | Defensive performance ranking |
| `/team-stats/overview` | GET | Team statistics overview |
| `/team-stats/goals` | GET | Team goal statistics |
| `/team-stats/fixtures` | GET | Team fixture statistics |
| `/team-stats/cards` | GET | Team card statistics |
| `/team-stats/lineups` | GET | Team lineup statistics |

## 📊 Data Coverage

### Player Performance Metrics

- **Basic Info**: Age, nationality, height, weight, position, number
- **Performance**: Appearances, lineups, minutes played, rating
- **Goals & Assists**: Goals scored, assists provided, penalty stats
- **Shots & Passing**: Total shots, shots on target, passes, accuracy, key passes
- **Defensive**: Tackles, blocks, interceptions, duels won
- **Attacking**: Dribbles, fouls drawn/committed, cards
- **Goalkeeper**: Saves, goals conceded, clean sheets

### Fixture Player Statistics

- **Match Performance**: Individual player stats for each fixture
- **Real-time Data**: Live statistics from API-Football
- **Stored Data**: Historical fixture player performance
- **Comprehensive Metrics**: All performance indicators per match

### Team & League Analysis

- **Team Performance**: Goals, fixtures, cards, lineups, statistics
- **League Standings**: Points, rankings, defensive metrics
- **Head-to-Head**: Team comparison and historical matchups
- **Live Updates**: Real-time match data and statistics

## 🔧 Configuration

### Environment Variables

```bash
# API Keys (choose one)
APIFOOTBALL_API_KEY=your_direct_api_key
RAPIDAPI_KEY=your_rapidapi_key

# League & Season Defaults
LEAGUE_ID=39          # EPL
SEASON_DEFAULT=2025   # Current season

# Database
DATABASE_URL=epl_defense.db  # SQLite file

# Ingestion Settings
INGESTION_BATCH_SIZE=100
INGESTION_RATE_LIMIT_DELAY=1.0
```

## 🏃‍♂️ Development

### Project Structure

```
epl-defense/
├── app/
│   ├── api/              # API routes
│   │   ├── routes_leagues.py
│   │   ├── routes_teams.py
│   │   ├── routes_standings.py
│   │   ├── routes_fixtures.py
│   │   ├── routes_defense.py
│   │   ├── routes_team_stats.py
│   │   ├── routes_player_stats.py    # NEW!
│   │   └── routes_ingestion.py
│   ├── db/               # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── init_database.py      # Database initialization
├── pyproject.toml        # Dependencies
└── README.md
```

### Database Setup

```bash
# Initialize tables
python init_database.py

# Reset database (⚠️ destructive)
python -c "from app.db.init_db import drop_db; drop_db()"
```

### Adding New Models

1. Create model in `app/models/`
2. Add to `app/models/__init__.py`
3. Update `app/db/init_db.py`
4. Run `python init_database.py`

## 📊 Data Ingestion

### How It Works

1. **League Setup**: Creates league record with season info
2. **Team Import**: Bulk imports all teams and venues
3. **Player Import**: Handles pagination, imports all players with stats
4. **Fixture Import**: Imports match schedule and results
5. **Fixture Player Stats**: Imports individual player performance data
6. **Smart Updates**: Only updates changed data, preserves history

### Rate Limiting

- **Teams**: Single API call (20 teams)
- **Players**: Paginated calls with 1-second delays
- **Fixtures**: Single API call (380+ matches)
- **Fixture Player Stats**: Individual fixture calls with rate limiting
- **Total API calls**: ~400-500 calls per full ingestion

### Monitoring

```bash
# Check ingestion status
curl 'http://127.0.0.1:8000/ingestion/status/39/2025'

# Response example:
{
  "league_id": 39,
  "season": 2025,
  "has_league": true,
  "teams_count": 20,
  "players_count": 550,
  "fixtures_count": 380,
  "player_stats_count": 240,
  "last_updated": "2025-01-14T11:00:00Z"
}
```

## 🚀 Production Deployment

### Docker Setup (Coming Soon)

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/epl
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=epl
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
  
  redis:
    image: redis:7-alpine
```

### Scheduled Ingestion

```python
# Background job setup (coming soon)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
    ingest_epl_data,
    'interval',
    hours=6,  # Update every 6 hours
    args=[39, 2025]
)
scheduler.start()
```

## 🎯 Use Cases

### Fantasy Football Applications
- Complete player performance data
- Season-long and match-by-match statistics
- Player rankings and leaderboards

### Sports Analytics Platforms
- Deep statistical analysis and comparisons
- Team performance tracking
- Player scouting and evaluation

### Fan Engagement Apps
- Player rankings and leaderboards
- Team analysis and statistics
- Match performance insights

### Data Journalism
- Comprehensive EPL statistics
- Historical performance data
- Real-time match updates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [API-Football](https://www.api-football.com/) for comprehensive football data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for robust ORM capabilities

---

**⚽ Ready to build the ultimate EPL analytics platform! 🚀**

**🎯 Now with comprehensive player statistics, fixture analysis, and leaderboards!**




