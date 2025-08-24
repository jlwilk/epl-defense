# 📊 API Response Format Documentation

This document describes the standardized response format used across all EPL Defense API endpoints.

## 🔄 Standard Response Structure

All API endpoints return responses in a consistent format:

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

## 📋 Response Field Descriptions

### Core Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `get` | string | Endpoint identifier that was called | `"teams"`, `"fixtures"`, `"standings"` |
| `parameters` | object | Query parameters used in the request | `{"season": "2025", "league": "39"}` |
| `errors` | object/null | Error information (null if no errors) | `null` or `{"detail": "Error message"}` |
| `results` | integer | Number of results returned | `20`, `1`, `0` |
| `paging` | object/null | Pagination information (null if not applicable) | `{"current": 1, "total": 5}` |
| `response` | array/object | Actual data payload | Array of items or single object |

### Error Field Details

The `errors` field can contain various error types:

```json
{
  "errors": {
    "required": "At least one parameter is required.",
    "season": "The Season field need another parameter.",
    "team": "The Team field is required."
  }
}
```

### Paging Field Details

The `paging` field provides pagination information:

```json
{
  "paging": {
    "current": 1,
    "total": 5
  }
}
```

- `current`: Current page number
- `total`: Total number of pages available

## 📚 Endpoint-Specific Response Examples

### 1. Teams Endpoint (`/teams/`)

**Request**: `GET /teams/?season=2025&league=39`

**Response**:
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

### 2. Team Statistics Endpoint (`/teams/{id}/statistics`)

**Request**: `GET /teams/40/statistics?season=2025&league=39`

**Response**:
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

### 3. Fixtures Endpoint (`/fixtures/`)

**Request**: `GET /fixtures/?season=2025&league=39&team=40`

**Response**:
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

### 4. Standings Endpoint (`/standings/`)

**Request**: `GET /standings/?league=39&season=2025`

**Response**:
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

## ⚠️ Error Response Examples

### 1. Validation Error (422)

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

### 2. Bad Request Error (400)

```json
{
  "detail": "Invalid league ID or season parameter"
}
```

### 3. Not Found Error (404)

```json
{
  "detail": "Team not found"
}
```

### 4. External API Error (502)

```json
{
  "detail": "External API service unavailable"
}
```

## 🔍 Response Field Handling

### Empty Fields

Some fields may be empty or null in certain scenarios:

- **Empty Errors**: `"errors": []` is converted to `"errors": null`
- **Empty Paging**: `"paging": {}` is converted to `"paging": null`
- **Missing Data**: Fields may be `null` if data is not available

### Data Types

- **IDs**: Always integers
- **Names**: Strings (may be null if unavailable)
- **Dates**: ISO 8601 format strings
- **Timestamps**: Unix timestamps (seconds since epoch)
- **Percentages**: String format (e.g., "75%")
- **Ratings**: Float values (e.g., 7.5)

## 📱 Client Implementation Tips

### 1. Always Check Response Structure

```javascript
// Good practice
if (response.errors) {
  // Handle errors
  console.error('API Error:', response.errors);
  return;
}

if (response.results === 0) {
  // No data available
  console.log('No results found');
  return;
}

// Process data
const data = response.response;
```

### 2. Handle Pagination

```javascript
if (response.paging && response.paging.total > 1) {
  // Multiple pages available
  const currentPage = response.paging.current;
  const totalPages = response.paging.total;
  
  // Implement pagination controls
  showPagination(currentPage, totalPages);
}
```

### 3. Validate Required Fields

```javascript
// Check for required response structure
if (!response.get || !response.response) {
  console.error('Invalid response format');
  return;
}

// Validate data type
if (Array.isArray(response.response)) {
  // Handle array response
  response.response.forEach(item => processItem(item));
} else {
  // Handle single object response
  processItem(response.response);
}
```

## 🔄 Response Consistency

All endpoints maintain this consistent structure, making it easy to:

- **Build Generic Handlers**: Create reusable response processing functions
- **Implement Error Handling**: Standardized error response format
- **Support Pagination**: Consistent paging information across endpoints
- **Validate Responses**: Predictable data structure for client validation

This standardized format ensures a consistent developer experience across all EPL Defense API endpoints.
