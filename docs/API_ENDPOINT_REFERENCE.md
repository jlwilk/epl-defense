# 📡 API Endpoint Reference

Complete reference for all EPL Defense API endpoints, including request/response examples, parameters, and usage instructions.

## 🏠 Base URL

- **Development**: `http://127.0.0.1:8001`
- **Production**: `https://api.epldefense.com`

## 🔑 Authentication

All endpoints require API key authentication. Set your key in environment variables:

```bash
# RapidAPI (recommended)
export RAPIDAPI_KEY="your_rapidapi_key"

# Or direct API-Football
export APIFOOTBALL_API_KEY="your_direct_api_key"
```

## 📊 Response Format

All endpoints return standardized responses:

```json
{
  "get": "endpoint_name",
  "parameters": {"param": "value"},
  "errors": null,
  "results": 1,
  "paging": {"current": 1, "total": 1},
  "response": [...]
}
```

---

## 🏟️ Teams Endpoints

### List Teams

**Endpoint**: `GET /teams/`

**Description**: Get teams with optional filtering by league, season, country, or search term.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39 (Premier League)
- `country` (optional): Filter by country name
- `search` (optional): Search team by name

**Example Request**:
```bash
curl "http://127.0.0.1:8001/teams/?season=2025&league=39"
```

**Example Response**:
```json
{
  "get": "teams",
  "parameters": {"season": "2025", "league": "39"},
  "errors": null,
  "results": 20,
  "paging": {"current": 1, "total": 1},
  "response": [
    {
      "id": 40,
      "name": "Liverpool",
      "code": "LIV",
      "country": "England",
      "founded": 1892,
      "national": false,
      "logo": "https://media.api-sports.io/football/teams/40.png",
      "venue_id": 550,
      "venue_name": "Anfield",
      "venue_address": "Anfield Road",
      "venue_city": "Liverpool",
      "venue_capacity": 53394,
      "venue_surface": "grass",
      "venue_image": "https://media.api-sports.io/football/venues/550.png"
    }
  ]
}
```

### Search Teams

**Endpoint**: `GET /teams/search`

**Description**: Search for teams by name with optional country filtering.

**Query Parameters**:
- `search` (required): Team name to search for
- `country` (optional): Filter by country

**Example Request**:
```bash
curl "http://127.0.0.1:8001/teams/search?search=Manchester&country=England"
```

**Example Response**:
```json
{
  "get": "teams",
  "parameters": {"search": "Manchester", "country": "England"},
  "errors": null,
  "results": 2,
  "paging": {"current": 1, "total": 1},
  "response": [
    {
      "id": 33,
      "name": "Manchester United",
      "code": "MUN",
      "country": "England",
      "founded": 1878,
      "national": false,
      "logo": "https://media.api-sports.io/football/teams/33.png"
    },
    {
      "id": 50,
      "name": "Manchester City",
      "code": "MCI",
      "country": "England",
      "founded": 1880,
      "national": false,
      "logo": "https://media.api-sports.io/football/teams/50.png"
    }
  ]
}
```

### Get Team Details

**Endpoint**: `GET /teams/{team_id}`

**Description**: Get detailed information about a specific team.

**Path Parameters**:
- `team_id` (required): Team ID

**Example Request**:
```bash
curl "http://127.0.0.1:8001/teams/40"
```

**Example Response**:
```json
{
  "get": "teams",
  "parameters": {"id": "40"},
  "errors": null,
  "results": 1,
  "paging": null,
  "response": [
    {
      "id": 40,
      "name": "Liverpool",
      "code": "LIV",
      "country": "England",
      "founded": 1892,
      "national": false,
      "logo": "https://media.api-sports.io/football/teams/40.png",
      "venue_id": 550,
      "venue_name": "Anfield",
      "venue_address": "Anfield Road",
      "venue_city": "Liverpool",
      "venue_capacity": 53394,
      "venue_surface": "grass",
      "venue_image": "https://media.api-sports.io/football/venues/550.png"
    }
  ]
}
```

### Get Team Statistics

**Endpoint**: `GET /teams/{team_id}/statistics`

**Description**: Get team statistics for a specific season and league.

**Path Parameters**:
- `team_id` (required): Team ID

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/teams/40/statistics?season=2025&league=39"
```

**Example Response**:
```json
{
  "get": "teams/statistics",
  "parameters": {"team": "40", "league": "39", "season": "2025"},
  "errors": null,
  "results": 1,
  "paging": null,
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
      "id": 40,
      "name": "Liverpool",
      "logo": "https://media.api-sports.io/football/teams/40.png"
    },
    "form": "WWDWL",
    "fixtures": {
      "played": {"home": 10, "away": 10, "total": 20},
      "wins": {"home": 8, "away": 6, "total": 14},
      "draws": {"home": 1, "away": 2, "total": 3},
      "loses": {"home": 1, "away": 2, "total": 3}
    },
    "goals": {
      "for": {
        "total": {"home": 25, "away": 18, "total": 43},
        "average": {"home": "2.5", "away": "1.8", "total": "2.15"}
      },
      "against": {
        "total": {"home": 8, "away": 12, "total": 20},
        "average": {"home": "0.8", "away": "1.2", "total": "1.0"}
      }
    },
    "biggest": {
      "streak": {"wins": 5, "draws": 2, "loses": 1},
      "wins": {"home": "3-0", "away": "2-1"},
      "loses": {"home": "0-1", "away": "1-2"}
    },
    "clean_sheet": {"home": 5, "away": 3, "total": 8},
    "failed_to_score": {"home": 1, "away": 2, "total": 3}
  }
}
```

---

## ⚽ Fixtures Endpoints

### List Fixtures

**Endpoint**: `GET /fixtures/`

**Description**: Get fixtures with comprehensive filtering options.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39
- `team` (optional): Team ID to filter fixtures
- `last` (optional): Return last N fixtures
- `next` (optional): Return next N fixtures
- `from_date` (optional): From date (YYYY-MM-DD)
- `to_date` (optional): To date (YYYY-MM-DD)
- `round` (optional): Round of the season
- `status` (optional): Fixture status

**Example Request**:
```bash
curl "http://127.0.0.1:8001/fixtures/?season=2025&league=39&team=40"
```

**Example Response**:
```json
{
  "get": "fixtures",
  "parameters": {"season": "2025", "league": "39", "team": "40"},
  "errors": null,
  "results": 38,
  "paging": {"current": 1, "total": 2},
  "response": [
    {
      "id": 1035037,
      "referee": "Michael Oliver",
      "timezone": "UTC",
      "date": "2025-08-16",
      "timestamp": 1734393600,
      "periods": {"first": 1734397200, "second": 1734400800},
      "venue": {
        "id": 550,
        "name": "Anfield",
        "city": "Liverpool"
      },
      "status": {"long": "Match Finished", "short": "FT", "elapsed": 90},
      "league": {
        "id": 39,
        "name": "Premier League",
        "country": "England",
        "logo": "https://media.api-sports.io/football/leagues/39.png",
        "flag": "https://media.api-sports.io/flags/gb.svg",
        "season": 2025,
        "round": "Regular Season - 1"
      },
      "teams": {
        "home": {
          "id": 40,
          "name": "Liverpool",
          "logo": "https://media.api-sports.io/football/teams/40.png",
          "winner": true
        },
        "away": {
          "id": 47,
          "name": "Tottenham",
          "logo": "https://media.api-sports.io/football/teams/47.png",
          "winner": false
        }
      },
      "goals": {"home": 3, "away": 1},
      "score": {
        "halftime": {"home": 2, "away": 0},
        "fulltime": {"home": 3, "away": 1},
        "extratime": {"home": null, "away": null},
        "penalty": {"home": null, "away": null}
      }
    }
  ]
}
```

### Get Live Fixtures

**Endpoint**: `GET /fixtures/live`

**Description**: Get currently live matches.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/fixtures/live?season=2025&league=39"
```

**Example Response**:
```json
{
  "get": "fixtures",
  "parameters": {"season": "2025", "league": "39"},
  "errors": null,
  "results": 2,
  "paging": null,
  "response": [
    {
      "id": 1035038,
      "referee": "Anthony Taylor",
      "timezone": "UTC",
      "date": "2025-08-17",
      "timestamp": 1734481200,
      "periods": {"first": 1734484800, "second": null},
      "venue": {
        "id": 556,
        "name": "Old Trafford",
        "city": "Manchester"
      },
      "status": {"long": "First Half", "short": "1H", "elapsed": 35},
      "league": {
        "id": 39,
        "name": "Premier League",
        "country": "England",
        "season": 2025,
        "round": "Regular Season - 2"
      },
      "teams": {
        "home": {
          "id": 33,
          "name": "Manchester United",
          "logo": "https://media.api-sports.io/football/teams/33.png",
          "winner": null
        },
        "away": {
          "id": 50,
          "name": "Manchester City",
          "logo": "https://media.api-sports.io/football/teams/50.png",
          "winner": null
        }
      },
      "goals": {"home": 1, "away": 0},
      "score": {
        "halftime": {"home": null, "away": null},
        "fulltime": {"home": null, "away": null},
        "extratime": {"home": null, "away": null},
        "penalty": {"home": null, "away": null}
      }
    }
  ]
}
```

### Get Fixtures by Date

**Endpoint**: `GET /fixtures/date/{date}`

**Description**: Get fixtures for a specific date.

**Path Parameters**:
- `date` (required): Date in YYYY-MM-DD format

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/fixtures/date/2025-08-16?season=2025&league=39"
```

---

## 🏆 Standings Endpoints

### Get League Standings

**Endpoint**: `GET /standings/`

**Description**: Get league standings with optional filtering.

**Query Parameters**:
- `league` (optional): League ID, defaults to 39
- `season` (optional): Season year, defaults to 2025

**Example Request**:
```bash
curl "http://127.0.0.1:8001/standings/?league=39&season=2025"
```

**Example Response**:
```json
{
  "get": "standings",
  "parameters": {"league": "39", "season": "2025"},
  "errors": null,
  "results": 20,
  "paging": null,
  "response": [
    {
      "league": {
        "id": 39,
        "name": "Premier League",
        "country": "England",
        "logo": "https://media.api-sports.io/football/leagues/39.png",
        "flag": "https://media.api-sports.io/flags/gb-eng.svg",
        "season": 2025,
        "standings": [
          [
            {
              "rank": 1,
              "team": {
                "id": 40,
                "name": "Liverpool",
                "logo": "https://media.api-sports.io/football/teams/40.png"
              },
              "points": 45,
              "goalsDiff": 25,
              "group": "Premier League",
              "form": "WWDWL",
              "status": "same",
              "description": "Promotion - Champions League (Group Stage)",
              "all": {
                "played": 20,
                "win": 14,
                "draw": 3,
                "lose": 3,
                "goals": {"for": 43, "against": 18}
              },
              "home": {
                "played": 10,
                "win": 8,
                "draw": 1,
                "lose": 1,
                "goals": {"for": 25, "against": 8}
              },
              "away": {
                "played": 10,
                "win": 6,
                "draw": 2,
                "lose": 2,
                "goals": {"for": 18, "against": 10}
              },
              "update": "2025-01-17T00:00:00+00:00"
            }
          ]
        ]
      }
    }
  ]
}
```

---

## 🏛️ Leagues Endpoints

### List Leagues

**Endpoint**: `GET /leagues/`

**Description**: Get available leagues with optional filtering.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `country` (optional): Filter by country
- `name` (optional): Search by league name

**Example Request**:
```bash
curl "http://127.0.0.1:8001/leagues/?season=2025&country=England"
```

**Example Response**:
```json
{
  "get": "leagues",
  "parameters": {"season": "2025", "country": "England"},
  "errors": null,
  "results": 5,
  "paging": null,
  "response": [
    {
      "id": 39,
      "name": "Premier League",
      "type": "League",
      "country": "England",
      "country_code": "GB",
      "logo": "https://media.api-sports.io/football/leagues/39.png",
      "flag": "https://media.api-sports.io/flags/gb-eng.svg",
      "season": 2025,
      "season_start": "2025-08-15",
      "season_end": "2026-05-23",
      "is_current": true,
      "coverage": "{\"fixtures\":{\"events\":true,\"lineups\":true,\"statistics\":true,\"players_statistics\":true},\"standings\":true,\"players\":true,\"top_scorers\":true,\"top_assists\":true,\"top_cards\":true,\"injuries\":false,\"predictions\":true,\"odds\":false}",
      "created_at": "2025-01-17T12:00:00Z",
      "updated_at": "2025-01-17T12:00:00Z"
    }
  ]
}
```

---

## 👥 Player Statistics Endpoints

### Get Player Statistics

**Endpoint**: `GET /player-stats/player/{player_id}`

**Description**: Get individual player season statistics.

**Path Parameters**:
- `player_id` (required): Player ID

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/player-stats/player/874?season=2025&league=39"
```

### Get Top Scorers

**Endpoint**: `GET /player-stats/top-scorers`

**Description**: Get top goal scorers leaderboard.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/player-stats/top-scorers?season=2025&league=39"
```

### Get Top Assists

**Endpoint**: `GET /player-stats/top-assists`

**Description**: Get top assist providers leaderboard.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/player-stats/top-assists?season=2025&league=39"
```

---

## 📥 Data Ingestion Endpoints

### Trigger Data Ingestion

**Endpoint**: `POST /ingestion/league/{league_id}/season/{season}`

**Description**: Start data ingestion for a specific league and season.

**Path Parameters**:
- `league_id` (required): League ID
- `season` (required): Season year

**Example Request**:
```bash
curl -X POST "http://127.0.0.1:8001/ingestion/league/39/season/2025"
```

**Example Response**:
```json
{
  "message": "Data ingestion started for league 39 season 2025",
  "league_id": 39,
  "season": 2025,
  "status": "started",
  "task_id": "background_task"
}
```

### Quick EPL Ingestion

**Endpoint**: `POST /ingestion/epl/2025`

**Description**: Quick start for EPL 2025 data ingestion.

**Example Request**:
```bash
curl -X POST "http://127.0.0.1:8001/ingestion/epl/2025"
```

### Check Ingestion Status

**Endpoint**: `GET /ingestion/status/{league_id}/{season}`

**Description**: Check the current ingestion status for a league/season.

**Path Parameters**:
- `league_id` (required): League ID
- `season` (required): Season year

**Example Request**:
```bash
curl "http://127.0.0.1:8001/ingestion/status/39/2025"
```

**Example Response**:
```json
{
  "league_id": 39,
  "season": 2025,
  "status": "completed",
  "progress": {
    "teams": "100%",
    "players": "100%",
    "fixtures": "100%"
  },
  "counts": {
    "teams": 20,
    "players": 550,
    "fixtures": 380
  },
  "last_updated": "2025-01-17T12:00:00Z"
}
```

---

## 🛡️ Defense Statistics Endpoints

### Get Defense Table

**Endpoint**: `GET /defense/table`

**Description**: Get defensive performance ranking table.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/defense/table?season=2025&league=39"
```

---

## 🏃‍♂️ Team Statistics Endpoints

### Get Team Statistics Overview

**Endpoint**: `GET /team-stats/overview`

**Description**: Get comprehensive team statistics overview.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/team-stats/overview?season=2025&league=39"
```

### Get Team Goal Statistics

**Endpoint**: `GET /team-stats/goals`

**Description**: Get detailed team goal statistics.

**Query Parameters**:
- `season` (optional): Season year, defaults to 2025
- `league` (optional): League ID, defaults to 39

**Example Request**:
```bash
curl "http://127.0.0.1:8001/team-stats/goals?season=2025&league=39"
```

---

## ❤️ Health Check

### Health Status

**Endpoint**: `GET /health`

**Description**: Check the health status of the EPL Defense API service.

**Example Request**:
```bash
curl "http://127.0.0.1:8001/health"
```

**Example Response**:
```json
{
  "status": "ok",
  "message": "EPL Defense API is running",
  "timestamp": "2025-01-17T12:00:00Z",
  "version": "1.0.0"
}
```

---

## 📚 Interactive Documentation

- **Swagger UI**: `http://127.0.0.1:8001/docs`
- **ReDoc**: `http://127.0.0.1:8001/redoc`
- **OpenAPI JSON**: `http://127.0.0.1:8001/openapi.json`

---

## ⚠️ Error Handling

### Common HTTP Status Codes

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (resource doesn't exist)
- **422**: Validation Error (parameter type mismatch)
- **500**: Internal Server Error
- **502**: Bad Gateway (external API error)

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Validation Error Format

```json
{
  "detail": [
    {
      "loc": ["query", "season"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

---

## 🔄 Rate Limiting

- **Free Tier**: 100 requests/day
- **Premium Tier**: 7,500 requests/day

### Rate Limit Headers

Response headers include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642502400
```

---

## 📱 Client Examples

### JavaScript/Node.js

```javascript
const response = await fetch('http://127.0.0.1:8001/teams/?season=2025&league=39');
const data = await response.json();

if (data.errors) {
  console.error('API Error:', data.errors);
  return;
}

const teams = data.response;
teams.forEach(team => {
  console.log(`${team.name} (${team.code})`);
});
```

### Python

```python
import requests

response = requests.get('http://127.0.0.1:8001/teams/', params={
    'season': 2025,
    'league': 39
})

data = response.json()

if data['errors']:
    print(f"API Error: {data['errors']}")
    return

teams = data['response']
for team in teams:
    print(f"{team['name']} ({team['code']})")
```

### cURL

```bash
# Get all Premier League teams for 2025
curl "http://127.0.0.1:8001/teams/?season=2025&league=39"

# Search for Manchester teams
curl "http://127.0.0.1:8001/teams/search?search=Manchester"

# Get Liverpool statistics
curl "http://127.0.0.1:8001/teams/40/statistics?season=2025&league=39"

# Get live fixtures
curl "http://127.0.0.1:8001/fixtures/live?season=2025&league=39"
```

---

This comprehensive endpoint reference provides all the information needed to integrate with the EPL Defense API. For additional examples and detailed schema information, refer to the interactive documentation at `/docs`.
